
import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
import json
import os
from vibe_dojo.semantic import SemanticIndex, cosine_similarity

@pytest.fixture
def mock_vault(tmp_path):
    """Create a temporary vault structure."""
    (tmp_path / "10_Mastery").mkdir()
    (tmp_path / "01_Drills").mkdir()
    (tmp_path / ".dojo_cache").mkdir()
    return tmp_path

@pytest.fixture
def mock_genai():
    """Mock the genai client."""
    with patch("vibe_dojo.semantic.get_client") as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        
        # Mock embedding response
        mock_response = MagicMock()
        # Mocking a 3-dimensional vector for simplicity
        mock_response.embeddings = [MagicMock(values=[0.1, 0.2, 0.3])] 
        mock_client.models.embed_content.return_value = mock_response
        
        yield mock_client

def test_cosine_similarity():
    """Test vector similarity calculation."""
    v1 = [1, 0, 0]
    v2 = [1, 0, 0]
    # Identical vectors = 1.0
    assert cosine_similarity(v1, v2) == pytest.approx(1.0)
    
    v3 = [0, 1, 0]
    # Orthogonal vectors = 0.0
    assert cosine_similarity(v1, v3) == pytest.approx(0.0)
    
    v4 = [-1, 0, 0]
    # Opposite vectors = -1.0
    assert cosine_similarity(v1, v4) == pytest.approx(-1.0)

def test_index_initialization(mock_vault):
    """Test index creation and loading."""
    index = SemanticIndex(mock_vault)
    assert index.index == {}
    assert index.index_file.name == "embeddings_index.json"

def test_embed_content(mock_vault, mock_genai):
    """Test embedding generation wrapper."""
    index = SemanticIndex(mock_vault)
    embedding = index.generate_embedding("test content")
    
    assert len(embedding) == 3
    assert embedding == [0.1, 0.2, 0.3]
    mock_genai.models.embed_content.assert_called_once()

def test_update_file(mock_vault, mock_genai):
    """Test file indexing."""
    index = SemanticIndex(mock_vault)
    
    # Create a dummy mastery note
    note_path = mock_vault / "10_Mastery" / "MASTERY__Test.md"
    note_path.write_text("# Test Content", encoding="utf-8")
    
    # First update should return True (indexed)
    updated = index.update_file(note_path, "mastery")
    assert updated is True
    
    rel_path = str(note_path.relative_to(mock_vault))
    assert rel_path in index.index
    assert index.index[rel_path]["type"] == "mastery"
    
    # Second update with no changes should return False
    updated = index.update_file(note_path, "mastery")
    assert updated is False

def test_find_similar(mock_vault, mock_genai):
    """Test similarity search."""
    index = SemanticIndex(mock_vault)
    
    # Manually populate index with mock data
    index.index = {
        "file1.md": {"embedding": [1.0, 0.0, 0.0], "type": "mastery"},
        "file2.md": {"embedding": [0.0, 1.0, 0.0], "type": "drill"},
        "file3.md": {"embedding": [0.9, 0.1, 0.0], "type": "mastery"} # Similar to file1
    }
    
    # Search for something similar to file1 ([1, 0, 0])
    # file1 match should be 1.0, file3 should be high, file2 should be 0
    
    # We pass query_embedding directly to skip API mock for this specific check logic if we want,
    # but let's strictly test the finding logic.
    
    results = index.find_similar(query_embedding=[1.0, 0.0, 0.0], threshold=0.5)
    
    assert len(results) == 2 # file1 and file3
    assert results[0]["path"] == "file1.md"
    assert results[1]["path"] == "file3.md"
