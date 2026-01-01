"""Test ingest and create-drill functionality."""


from vibe_dojo.ingestor import create_source_note, slugify
from vibe_dojo.writer import create_drill_note


def test_slugify():
    """Test slugify function."""
    assert slugify("Hello World") == "hello-world"
    assert slugify("Test-123") == "test-123"
    assert slugify("Special!@#$%Characters") == "specialcharacters"
    assert slugify("  Multiple   Spaces  ") == "multiple-spaces"


def test_create_source_note_manual(tmp_path):
    """Test creating a source note from manual text."""
    vault_path = tmp_path
    (vault_path / "00_Inbox" / "_attachments").mkdir(parents=True)

    text = "This is test content for the source note."
    note_path = create_source_note(vault_path, text=text, title="Test Source")

    assert note_path.exists()
    assert note_path.name.startswith("SOURCE__test-source")

    content = note_path.read_text(encoding="utf-8")
    assert "id:" in content
    assert "source_kind: manual" in content
    assert "fetch_method: manual" in content
    assert "Test Source" in content

    # Check attachment was created
    attachments = list((vault_path / "00_Inbox" / "_attachments").glob("*.txt"))
    assert len(attachments) == 1
    assert attachments[0].read_text(encoding="utf-8") == text


def test_create_drill_note(tmp_path):
    """Test creating a drill note."""
    vault_path = tmp_path
    (vault_path / "01_Drills").mkdir(parents=True)

    drill_path = create_drill_note(
        vault_path,
        title="Test Drill",
        pattern=["Pattern 1", "Pattern 2"],
        drill_goal="Learn something",
        drill_steps=["Step 1", "Step 2"],
        validation=["Check 1", "Check 2"],
        topics=["testing", "python"],
        timebox_min=15,
    )

    assert drill_path.exists()
    assert drill_path.name.startswith("DRILL__test-drill")

    content = drill_path.read_text(encoding="utf-8")
    assert "id:" in content
    assert "status: untried" in content
    assert "timebox_min: 15" in content
    assert "Pattern 1" in content
    assert "Step 1" in content
    assert "Check 1" in content
    assert "testing" in content


def test_create_drill_with_defaults(tmp_path):
    """Test creating a drill with minimal args (defaults)."""
    vault_path = tmp_path
    (vault_path / "01_Drills").mkdir(parents=True)

    drill_path = create_drill_note(vault_path, title="Minimal Drill")

    assert drill_path.exists()
    content = drill_path.read_text(encoding="utf-8")
    assert "status: untried" in content
    assert "Pattern to be filled in" in content
