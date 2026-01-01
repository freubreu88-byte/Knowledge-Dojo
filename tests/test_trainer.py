"""Test trainer loop functionality."""

from datetime import datetime, timedelta

from vibe_dojo.trainer import (
    create_practice_log,
    get_next_drill,
    mark_drill,
    parse_frontmatter,
    promote_to_mastery,
    update_frontmatter,
)
from vibe_dojo.writer import create_drill_note


def test_parse_frontmatter():
    """Test YAML frontmatter parsing."""
    content = """---
id: test123
status: untried
---

# Test Content
"""
    frontmatter, body = parse_frontmatter(content)

    assert frontmatter["id"] == "test123"
    assert frontmatter["status"] == "untried"
    assert "# Test Content" in body


def test_get_next_drill_untried(tmp_path):
    """Test getting next untried drill."""
    vault_path = tmp_path
    (vault_path / "01_Drills").mkdir(parents=True)

    # Create an untried drill
    drill = create_drill_note(vault_path, title="Test Drill 1")

    # Drill should be due (next_review is set to tomorrow by default, but untried should still show)
    next_drill = get_next_drill(vault_path)
    assert next_drill is not None
    assert next_drill == drill


def test_get_next_drill_priority(tmp_path):
    """Test drill priority: untried > failed > passed."""
    vault_path = tmp_path
    (vault_path / "01_Drills").mkdir(parents=True)

    # Create drills with different statuses
    drill1 = create_drill_note(vault_path, title="Passed Drill")
    drill2 = create_drill_note(vault_path, title="Failed Drill")
    drill3 = create_drill_note(vault_path, title="Untried Drill")

    # Update statuses
    today = datetime.now().date().isoformat()
    update_frontmatter(drill1, {"status": "passed", "next_review": today})
    update_frontmatter(drill2, {"status": "failed", "next_review": today})

    # Should get untried first (drill3)
    next_drill = get_next_drill(vault_path)
    assert next_drill is not None
    assert next_drill == drill3


def test_create_practice_log(tmp_path):
    """Test creating a practice log."""
    vault_path = tmp_path
    (vault_path / "01_Drills").mkdir(parents=True)
    (vault_path / "02_Practice_Logs").mkdir(parents=True)

    drill_path = create_drill_note(vault_path, title="Test Drill")

    log_path = create_practice_log(vault_path, drill_path, "passed", "Great practice!")

    assert log_path.exists()
    content = log_path.read_text(encoding="utf-8")
    assert "result: passed" in content
    assert "Great practice!" in content


def test_mark_drill_passed(tmp_path):
    """Test marking a drill as passed."""
    vault_path = tmp_path
    (vault_path / "01_Drills").mkdir(parents=True)
    (vault_path / "02_Practice_Logs").mkdir(parents=True)

    drill_path = create_drill_note(vault_path, title="Test Drill")

    mark_drill(vault_path, drill_path, "passed", "Good job!")

    # Check drill was updated
    content = drill_path.read_text(encoding="utf-8")
    frontmatter, _ = parse_frontmatter(content)

    assert frontmatter["status"] == "passed"
    assert frontmatter["review_count"] == 1
    assert "next_review" in frontmatter

    # Check log was created
    logs = list((vault_path / "02_Practice_Logs").glob("*.md"))
    assert len(logs) == 1


def test_mark_drill_failed(tmp_path):
    """Test marking a drill as failed."""
    vault_path = tmp_path
    (vault_path / "01_Drills").mkdir(parents=True)
    (vault_path / "02_Practice_Logs").mkdir(parents=True)

    drill_path = create_drill_note(vault_path, title="Test Drill")

    mark_drill(vault_path, drill_path, "failed", "Need more practice")

    content = drill_path.read_text(encoding="utf-8")
    frontmatter, _ = parse_frontmatter(content)

    assert frontmatter["status"] == "failed"
    # Should be due tomorrow
    next_review = datetime.fromisoformat(frontmatter["next_review"]).date()
    expected = (datetime.now() + timedelta(days=1)).date()
    assert next_review == expected


def test_mark_drill_archive(tmp_path):
    """Test marking a drill as bullshit/outdated moves it to archive."""
    vault_path = tmp_path
    (vault_path / "01_Drills").mkdir(parents=True)
    (vault_path / "02_Practice_Logs").mkdir(parents=True)

    drill_path = create_drill_note(vault_path, title="Test Drill")
    original_name = drill_path.name

    mark_drill(vault_path, drill_path, "bullshit")

    # Should be in archive
    assert not drill_path.exists()
    archived = vault_path / "90_Archive" / original_name
    assert archived.exists()


def test_promote_to_mastery(tmp_path):
    """Test promoting a drill to mastery."""
    vault_path = tmp_path
    (vault_path / "01_Drills").mkdir(parents=True)
    (vault_path / "10_Mastery").mkdir(parents=True)

    drill_path = create_drill_note(
        vault_path,
        title="Test Drill",
        pattern=["Pattern 1"],
        drill_goal="Learn something",
        topics=["testing"],
    )

    mastery_path = promote_to_mastery(vault_path, drill_path)

    assert mastery_path.exists()
    assert mastery_path.name.startswith("MASTERY__")

    content = mastery_path.read_text(encoding="utf-8")
    assert "type: mastery" in content
    assert "Pattern 1" in content
    assert "testing" in content
