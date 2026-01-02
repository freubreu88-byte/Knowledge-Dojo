"""Tests for trainer statistics and logic."""

from pathlib import Path
from datetime import datetime, timedelta
from vibe_dojo.trainer import get_vault_stats, get_streak, create_practice_log
from vibe_dojo.writer import create_drill_note

def test_vault_stats(tmp_path):
    # Setup folders
    (tmp_path / "01_Drills").mkdir()
    (tmp_path / "10_Mastery").mkdir()
    (tmp_path / "00_Inbox").mkdir()

    # Create some drills
    create_drill_note(tmp_path, title="Drill 1") # untried
    create_drill_note(tmp_path, title="Drill 2") # untried
    
    # Create a mastery note
    (tmp_path / "10_Mastery" / "MASTERY__test.md").write_text("mastery", encoding="utf-8")
    
    # Create a source note
    (tmp_path / "00_Inbox" / "SOURCE__test.md").write_text("source", encoding="utf-8")

    stats = get_vault_stats(tmp_path)
    
    assert stats["drills"]["untried"] == 2
    assert stats["drills"]["total"] == 2
    assert stats["mastery"] == 1
    assert stats["sources"] == 1

def test_streak_calculation(tmp_path):
    logs_path = tmp_path / "02_Practice_Logs"
    logs_path.mkdir()
    
    # Create some dummy drill path
    drill_path = tmp_path / "DRILL__test.md"
    drill_path.write_text("---\nid: test\n---\n# Test", encoding="utf-8")

    # No logs -> streak 0
    assert get_streak(tmp_path) == 0

    # Practice today -> streak 1
    today = datetime.now().strftime("%Y-%m-%d")
    (logs_path / f"{today}__test.md").write_text("log", encoding="utf-8")
    assert get_streak(tmp_path) == 1

    # Practice yesterday -> streak 2
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    (logs_path / f"{yesterday}__test.md").write_text("log", encoding="utf-8")
    assert get_streak(tmp_path) == 2

    # Break streak (day before yesterday missing)
    # Actually streak is 0 if not today/yesterday. 
    # But if we have yesterday and today, it's 2.
    # Let's add day-3. It should not increase streak if day-2 is missing.
    day3 = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")
    (logs_path / f"{day3}__test.md").write_text("log", encoding="utf-8")
    assert get_streak(tmp_path) == 2

def test_topic_stats(tmp_path):
    drills_path = tmp_path / "01_Drills"
    drills_path.mkdir()
    mastery_path = tmp_path / "10_Mastery"
    mastery_path.mkdir()
    
    # Create drills with topics
    create_drill_note(tmp_path, title="Python 1", topics=["Python", "Basics"])
    create_drill_note(tmp_path, title="Python 2", topics=["Python"])
    
    # Manually mark Python 1 as passed
    from vibe_dojo.trainer import update_frontmatter
    update_frontmatter(drills_path / "DRILL__python-1.md", {"status": "passed"})
    
    # Create a mastery note for Python
    (mastery_path / "MASTERY__python-basics.md").write_text("---\ntopics: ['Python']\n---\n# Python Basics", encoding="utf-8")
    
    from vibe_dojo.trainer import get_topics_stats
    stats = get_topics_stats(tmp_path)
    
    python_stats = next(s for s in stats if s["name"] == "Python")
    assert python_stats["total"] == 2
    assert python_stats["passed"] == 1
    assert python_stats["mastery"] == 1
    
    basics_stats = next(s for s in stats if s["name"] == "Basics")
    assert basics_stats["total"] == 1

def test_daily_cap(tmp_path):
    (tmp_path / "01_Drills").mkdir()
    (tmp_path / "02_Practice_Logs").mkdir()
    
    # Create config with cap of 2
    (tmp_path / "config.yaml").write_text("defaults:\n  max_drills_per_day: 2")
    
    # Create 3 drills
    create_drill_note(tmp_path, title="Drill 1")
    create_drill_note(tmp_path, title="Drill 2")
    create_drill_note(tmp_path, title="Drill 3")
    
    from vibe_dojo.trainer import get_next_drill, mark_drill, count_today_logs
    
    # Check count initially
    assert count_today_logs(tmp_path) == 0

    # 1. First drill should be available
    d1 = get_next_drill(tmp_path)
    assert d1 is not None
    
    # Practice 1st drill
    mark_drill(tmp_path, d1, "passed")
    assert count_today_logs(tmp_path) == 1
    
    # 2. Second drill should be available (Drill 1 is now 'passed' and not due yet)
    d2 = get_next_drill(tmp_path)
    assert d2 is not None
    assert d2.name != d1.name
    
    # Practice 2nd drill
    mark_drill(tmp_path, d2, "passed")
    assert count_today_logs(tmp_path) == 2
    
    # 3. Third drill should return None because cap (2) is reached
    d3 = get_next_drill(tmp_path)
    assert d3 is None

def test_drill_rating(tmp_path):
    (tmp_path / "01_Drills").mkdir()
    (tmp_path / "02_Practice_Logs").mkdir()
    
    drill_path = create_drill_note(tmp_path, title="Test Drill", topics=["UX"])
    
    from vibe_dojo.trainer import mark_drill, get_topics_stats
    
    # Mark with rating 4
    mark_drill(tmp_path, drill_path, "passed", rating=4)
    
    stats = get_topics_stats(tmp_path)
    ux_stats = next(s for s in stats if s["name"] == "UX")
    assert ux_stats["avg_rating"] == 4.0
