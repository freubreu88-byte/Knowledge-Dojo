"""LLM-powered drill generation from source content."""

import json
import os
from pathlib import Path
from typing import Optional

from google import genai
from google.genai import types


def get_client() -> genai.Client:
    """Initialize and return the Gen AI client."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY not found in environment. "
            "Create a .env file with your API key."
        )
    return genai.Client(api_key=api_key)


def load_source_content(vault_path: Path, source_id: str) -> tuple[str, dict]:
    """Load source content and metadata.

    Args:
        vault_path: Path to vault
        source_id: Source note ID

    Returns:
        Tuple of (content_text, metadata_dict)
    """
    # Find source note by ID
    inbox_path = vault_path / "00_Inbox"
    source_files = list(inbox_path.glob("SOURCE__*.md"))

    source_note = None
    for file in source_files:
        content = file.read_text(encoding="utf-8")
        if f"id: {source_id}" in content:
            source_note = file
            break

    if not source_note:
        raise ValueError(f"Source note with ID {source_id} not found")

    # Parse frontmatter
    content = source_note.read_text(encoding="utf-8")
    lines = content.split("\n")

    metadata = {}
    in_frontmatter = False
    for line in lines:
        if line.strip() == "---":
            if not in_frontmatter:
                in_frontmatter = True
            else:
                break
        elif in_frontmatter and ":" in line:
            key, value = line.split(":", 1)
            metadata[key.strip()] = value.strip()

    # Load full content from attachment
    transcript_path = metadata.get("transcript_path", "")
    if transcript_path:
        # Handle relative paths properly
        if transcript_path.startswith("/") or transcript_path.startswith("\\"):
             transcript_path = transcript_path.lstrip("/\\")

        full_content_path = vault_path / transcript_path
        if full_content_path.exists():
            full_content = full_content_path.read_text(encoding="utf-8")
        else:
            # Fallback to note content but warn
            print(f"[WARN] Transcript not found at {full_content_path}, using note content.")
            full_content = content
    else:
        full_content = content

    return full_content, metadata


def distill_drills(
    source_content: str,
    source_metadata: dict,
    model_name: str = "gemini-1.5-flash",
    existing_context: str = "",
    num_drills: Optional[int] = None, # Kept for backward compat but unused in prompt
) -> list[dict]:
    """Use Gemini to extract drills from source content.

    Args:
        source_content: Full source text
        source_metadata: Source metadata (url, kind, etc)
        model_name: Gemini model to use
        existing_context: String summarizing user's known concepts
        num_drills: Deprecated, unused.

    Returns:
        List of drill dictionaries with structure matching create_drill_note
    """
    client = get_client()

    # Prepare prompt
    # Prepare prompt
    metadata_text = ""
    if source_metadata:
        import yaml
        metadata_text = yaml.dump(source_metadata, sort_keys=False)

    prompt = f"""You are an expert learning designer creating practice drills from educational content.

**Source Metadata:**
{metadata_text}

**User Context (DO NOT CREATE DUPLICATE DRILLS FOR THESE):**
{existing_context if existing_context else "No prior knowledge context available."}

**Content (Timestamped Context):**
{source_content}  # Full content with timestamps

---

**Your Task:**
Identify ALL distinct, actionable practice drills from this content (maximum 10). Do not limit yourself to a small number if the content is rich.

For each drill:
1. Focus on ONE specific skill/pattern/concept
2. Be immediately actionable (can be practiced in 5-20 minutes)
3. Include concrete steps and validation criteria
4. Be trainer-first: emphasize DOING, not just reading
5. **Reference specific timestamps** where the concept is explained (e.g., "See 12:45")

{f"**Hint:** Use the provided chapters (if available) to organize drills by key topics." if source_metadata.get('chapters') else ""}

**Output Format (JSON):**
Return a JSON array of drill objects. Each drill must have:
- title: Clear, action-oriented title (e.g., "Implement OAuth Flow", not "Learn OAuth")
- pattern: Array of 2-4 bullet points describing the core pattern/concept
- drill_goal: One sentence describing what you'll achieve
- drill_steps: Array of 3-6 concrete, numbered steps
- validation: Array of 3-5 checkboxes to verify success
- snippet_type: "code", "prompt", or "commands"
- snippet_content: Actual code/prompt/commands to practice with
- topics: Array of 1-3 relevant topic tags
- timebox_min: Estimated minutes (5-20)
- confidence_score: Integer 1-5 (5 = Highly actionable/clear, 1 = Vague/Theoretical)

**Important:**
- Return ONLY valid JSON, no markdown code fences
- Focus on ACTIONABLE drills, not theory
- Make steps specific enough to follow without the original source
- Validation should be objective (pass/fail, not subjective)

Generate the drill proposal list now:"""

    # Call Gemini (1M token window allows full transcripts)
    try:
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.7,
                top_p=0.95,
                top_k=40,
                max_output_tokens=8192,
                response_mime_type='application/json',
            ),
        )
    except genai.errors.ClientError as e:
        print(f"\n[ERROR] Gemini API Refused: {e}")
        print(f"Model used: {model_name}")
        print("Note: If you get a 404, the model might not be enabled for your API key's project or region.")
        raise

    # Parse JSON response
    response_text = response.text.strip()

    # Remove markdown code fences if present
    if response_text.startswith("```json"):
        response_text = response_text[7:]
    if response_text.startswith("```"):
        response_text = response_text[3:]
    if response_text.endswith("```"):
        response_text = response_text[:-3]

    response_text = response_text.strip()

    try:
        drills = json.loads(response_text)
    except json.JSONDecodeError:
        # SALVAGE LOGIC: Try to recover complete drills from a truncated array
        try:
            # 1. Try to find the last occurrence of a closing brace for an object in the array
            # We look for "}," followed by anything or just "}" at the end of a mostly complete array
            last_valid_object = response_text.rfind("},")
            if last_valid_object == -1:
                # Try finding just a closing brace if it's the very last one
                last_valid_object = response_text.rfind("}")
            
            if last_valid_object != -1:
                # Cut the string at the end of the last complete object
                salvaged_text = response_text[:last_valid_object + 1]
                # Ensure it's a valid array
                if salvaged_text.startswith("["):
                    salvaged_text += "]"
                elif not salvaged_text.startswith("[") and "[" in response_text:
                    # In case the start was also messy
                    salvaged_text = "[" + salvaged_text + "]"
                
                drills = json.loads(salvaged_text)
                print(f"[INFO] Salvaged {len(drills)} drills from truncated response.")
            else:
                raise ValueError(f"Failed to parse or salvage Gemini response as JSON.\n\n{response_text[:500]}...")
        except Exception as e_inner:
             raise ValueError(f"Failed to parse Gemini response as JSON and salvage failed: {e_inner}\n\n{response_text[:500]}...")

    return drills



def get_existing_context(vault_path: Path, query_text: str = "") -> str:
    """Scan vault for existing mastery and drills to provide context.
    
    Uses semantic search if query_text is provided, otherwise falls back 
    to recent items or specific list if small enough.
    """
    from .semantic import SemanticIndex
    
    context_lines = []
    
    # Initialize index
    index = SemanticIndex(vault_path)
    
    # 1. Semantic Search (if query provided)
    if query_text:
        # Index vault if needed/empty? 
        # For performance, we assume index is reasonably up to date or we might miss fresh things.
        # But we can try to index blindly? No, distracting.
        # Just use what we have.
        
        similar_items = index.find_similar(query=query_text, limit=10, threshold=0.6)
        
        if similar_items:
            context_lines.append("RELATED EXISTING CONTENT (DO NOT DUPLICATE):")
            for item in similar_items:
                path = item["path"]
                # Clean path to title
                # e.g. 10_Mastery/MASTERY__Foo.md -> Foo
                name = Path(path).stem.replace("MASTERY__", "").replace("DRILL__", "").replace("-", " ")
                type_label = "Mastered" if item["type"] == "mastery" else "In Progress Drill"
                context_lines.append(f"- [{type_label}] {name}")
            return "\n".join(context_lines)

    # 2. Fallback: Recent Mastery (if no query or no matches)
    # Just list the last 20 mastery notes
    mastery_path = vault_path / "10_Mastery"
    if mastery_path.exists():
        # Get all mastery notes
        all_mastery = list(mastery_path.glob("MASTERY__*.md"))
        # Sort by mtime desc
        all_mastery.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        mastered = [f.stem.replace("MASTERY__", "").replace("-", " ") for f in all_mastery[:20]]
        if mastered:
            context_lines.append(f"RECENTLY MASTERED: {', '.join(mastered)}")

    return "\n".join(context_lines)


def create_drills_from_source(
    vault_path: Path,
    source_id: str,
    num_drills: int = 3,
    model_name: str = "gemini-1.5-flash",
) -> list[Path]:
    """Load source, distill drills with LLM, and create drill notes.

    Args:
        vault_path: Path to vault
        source_id: Source note ID
        num_drills: Number of drills to generate
        model_name: Gemini model to use

    Returns:
        List of paths to created drill notes
    """
    from .writer import create_drill_note

    # Load source
    source_content, source_metadata = load_source_content(vault_path, source_id)
    
    # Get existing context to avoid duplicates
    # Use first 2000 chars of source content for semantic query to save tokens/time
    query_preview = source_content[:2000] if source_content else ""
    existing_context = get_existing_context(vault_path, query_text=query_preview)

    # Distill drills
    drill_data = distill_drills(
        source_content, 
        source_metadata, 
        model_name,
        existing_context=existing_context
    )

    # Create drill notes
    created_drills = []
    for drill in drill_data:
        drill_path = create_drill_note(
            vault_path=vault_path,
            title=drill["title"],
            pattern=drill.get("pattern", []),
            drill_goal=drill.get("drill_goal", ""),
            drill_steps=drill.get("drill_steps", []),
            validation=drill.get("validation", []),
            snippet_type=drill.get("snippet_type", "code"),
            snippet_content=drill.get("snippet_content", ""),
            topics=drill.get("topics", []),
            timebox_min=drill.get("timebox_min", 10),
            source_id=source_id,
        )
        created_drills.append(drill_path)

    return created_drills


def analyze_insights(vault_path: Path, model_name: str = "gemini-3-flash-preview") -> str:
    """Use Gemini to analyze practice logs and mastery notes for insights."""
    client = get_client()

    # 1. Gather context
    mastery_path = vault_path / "10_Mastery"
    logs_path = vault_path / "02_Practice_Logs"
    
    mastery_titles = []
    if mastery_path.exists():
        mastery_titles = [f.stem.replace("MASTERY__", "") for f in mastery_path.glob("*.md")]
    
    recent_logs = []
    if logs_path.exists():
        # Get last 20 logs for context
        log_files = sorted(list(logs_path.glob("*.md")), reverse=True)[:20]
        for lf in log_files:
            content = lf.read_text(encoding="utf-8")
            # Extract result and description/notes
            recent_logs.append(content[:500]) # Snippet is enough

    if not mastery_titles and not recent_logs:
        return "Not enough data yet. Complete some drills to get insights!"

    prompt = f"""You are a high-level learning coach. Analyze the user's progress in their "Vibe-Dojo" vault.

**Mastery Notes (What they know):**
{", ".join(mastery_titles)}

**Recent Practice Logs (What they've been doing):**
{"".join(recent_logs)}

---
**Your Task:**
Provide a concise, motivating "Coach's Briefing" (max 300 words).
1. Identify **Strong Areas** (where they are succeeding).
2. Spot **Blind Spots** or recurring failures.
3. Suggest **Next Steps** (topics to explore or types of drills to focus on).
4. Give a **Dojo Quote** (a custom motivating quote for a "Vibe-Dojo").

Format with bullet points and bold text for readability. No specific student name, just address "The Student".
"""

    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.7,
        ),
    )

    return response.text.strip()
