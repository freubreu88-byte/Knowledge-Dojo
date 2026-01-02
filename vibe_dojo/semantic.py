"""Semantic analysis and deduplication using Gemini Embeddings."""

import json
import os
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import hashlib

from google import genai
from google.genai import types
import numpy as np

CACHE_DIR_NAME = ".dojo_cache"
INDEX_FILE_NAME = "embeddings_index.json"
EMBEDDING_MODEL = "models/text-embedding-004"


def get_client() -> genai.Client:
    """Initialize and return the Gen AI client."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment.")
    return genai.Client(api_key=api_key)


def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    """Compute cosine similarity between two vectors."""
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    if norm_v1 == 0 or norm_v2 == 0:
        return 0.0
    return dot_product / (norm_v1 * norm_v2)


class SemanticIndex:
    """Manages a local vector index for vault content."""

    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self.cache_dir = vault_path / CACHE_DIR_NAME
        self.index_file = self.cache_dir / INDEX_FILE_NAME
        self.index: Dict[str, Dict] = {}  # Map of file_path -> {hash, embedding, type, ...}
        self.client = None
        self._load_index()

    def _get_client(self):
        if not self.client:
            self.client = get_client()
        return self.client

    def _load_index(self):
        """Load index from disk."""
        if self.index_file.exists():
            try:
                with open(self.index_file, "r", encoding="utf-8") as f:
                    self.index = json.load(f)
            except json.JSONDecodeError:
                self.index = {}
        else:
            self.index = {}

    def _save_index(self):
        """Save index to disk."""
        self.cache_dir.mkdir(exist_ok=True)
        with open(self.index_file, "w", encoding="utf-8") as f:
            json.dump(self.index, f, indent=2)

    def _compute_file_hash(self, file_path: Path) -> str:
        """Compute MD5 hash of file content."""
        content = file_path.read_bytes()
        return hashlib.md5(content).hexdigest()

    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for text using Gemini."""
        if not text.strip():
            return []
            
        client = self._get_client()
        try:
            result = client.models.embed_content(
                model=EMBEDDING_MODEL,
                contents=text
            )
            return result.embeddings[0].values
        except Exception as e:
            print(f"[ERROR] Embedding generation failed: {e}")
            return []

    def update_file(self, file_path: Path, doc_type: str) -> bool:
        """Update embedding for a file if it changed. Returns True if updated."""
        abs_path = file_path.absolute()
        rel_path = str(file_path.relative_to(self.vault_path))
        
        if not file_path.exists():
             if rel_path in self.index:
                 del self.index[rel_path]
                 return True
             return False

        current_hash = self._compute_file_hash(file_path)
        
        # Check if already indexed and unchanged
        if rel_path in self.index and self.index[rel_path]["hash"] == current_hash:
            return False

        # Read content
        try:
            content = file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            return False

        # Generate embedding
        # For markdown, we might want to focus on headers or specific sections, 
        # but for now, we'll strip frontmatter and index the rest (truncated to limit)
        # Simple frontmatter stripping (rough)
        if content.startswith("---"):
            try:
                _, content = content.split("---", 2)[1:]
            except ValueError:
                pass # structure incorrect, use whole content
        
        # Truncate content to avoid token limits behavior (though Gemini handles large contexts, 
        # embeddings usually have limits around 2048 or 3072 tokens depending on model)
        # text-embedding-004 supports 2048 input tokens.
        embedding = self.generate_embedding(content[:8000]) # approximate char limit safe for token limit

        if not embedding:
            return False

        self.index[rel_path] = {
            "hash": current_hash,
            "type": doc_type,
            "embedding": embedding,
            "updated_at": os.path.getmtime(abs_path)
        }
        return True

    def index_vault(self) -> int:
        """Scan vault and update index. Returns number of updated files."""
        updated_count = 0
        
        # Index Mastery Notes
        mastery_path = self.vault_path / "10_Mastery"
        if mastery_path.exists():
            for f in mastery_path.glob("MASTERY__*.md"):
                if self.update_file(f, "mastery"):
                    updated_count += 1
                    print(f"Indexing: {f.name}")

        # Index Drills
        drills_path = self.vault_path / "01_Drills"
        if drills_path.exists():
            for f in drills_path.glob("DRILL__*.md"):
                if self.update_file(f, "drill"):
                    updated_count += 1
                    print(f"Indexing: {f.name}")

        if updated_count > 0:
            self._save_index()
            
        return updated_count

    def find_similar(self, query: str = "", query_embedding: Optional[List[float]] = None, limit: int = 5, threshold: float = 0.7) -> List[Dict]:
        """Find similar items in the index."""
        if query_embedding is None:
            if not query:
                return []
            query_embedding = self.generate_embedding(query)
            
        if not query_embedding:
            return []

        results = []
        for path, data in self.index.items():
            score = cosine_similarity(query_embedding, data["embedding"])
            if score >= threshold:
                results.append({
                    "path": path,
                    "score": score,
                    "type": data["type"]
                })

        # Sort by score desc
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:limit]
