"""Trainer loop: next, mark, promote."""

import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import yaml


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Parse YAML frontmatter from markdown content.

    Returns:
        Tuple of (frontmatter_dict, body_content)
    """
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", content, re.DOTALL)
    if not match:
        return {}, content

    frontmatter_str = match.group(1)
    body = match.group(2)

    frontmatter = yaml.safe_load(frontmatter_str) or {}
    return frontmatter, body


def update_frontmatter(file_path: Path, updates: dict) -> None:
    """Update frontmatter in a markdown file."""
    content = file_path.read_text(encoding="utf-8")
    frontmatter, body = parse_frontmatter(content)

    # Update frontmatter
    frontmatter.update(updates)

    # Rebuild file
    new_content = f"---\n{yaml.dump(frontmatter, default_flow_style=False)}---\n{body}"
    file_path.write_text(new_content, encoding="utf-8")


def count_today_logs(vault_path: Path) -> int:
    """Count how many drills were practiced today."""
    logs_path = vault_path / "02_Practice_Logs"
    if not logs_path.exists():
        return 0
    today_str = datetime.now().strftime("%Y-%m-%d")
    return len(list(logs_path.glob(f"{today_str}__*.md")))


def get_next_drill(vault_path: Path) -> Optional[Path]:
    """Get the next drill to practice, respecting daily limits."""
    from .config import Config
    config = Config(vault_path).config
    max_per_day = config.get("defaults", {}).get("max_drills_per_day", 5)
    
    if count_today_logs(vault_path) >= max_per_day:
        return None

    drills_path = vault_path / "01_Drills"
    if not drills_path.exists():
        return None

    today = datetime.now().date()
    candidates = []

    for drill_file in drills_path.glob("DRILL__*.md"):
        content = drill_file.read_text(encoding="utf-8")
        frontmatter, _ = parse_frontmatter(content)

        status = frontmatter.get("status", "untried")
        next_review_str = frontmatter.get("next_review", "")

        # Parse next_review
        if next_review_str:
            next_review = datetime.fromisoformat(str(next_review_str)).date()
        else:
            next_review = today

        # Check if due
        is_due = status in {"untried", "failed", "passed"} and next_review <= today

        if is_due:
            # Priority: untried > failed > passed
            priority = {"untried": 0, "failed": 1, "passed": 2}.get(status, 3)
            candidates.append((priority, drill_file))

    if not candidates:
        return None

    # Sort by priority, then by filename
    candidates.sort(key=lambda x: (x[0], x[1].name))
    return candidates[0][1]


def create_practice_log(
    vault_path: Path, drill_path: Path, result: str, notes: str = "", rating: int = 0
) -> Path:
    """Create a practice log entry.

    Args:
        vault_path: Vault path
        drill_path: Path to drill file
        result: Result (passed/failed/bullshit/outdated)
        notes: Optional notes

    Returns:
        Path to created log file
    """
    from .ingestor import slugify

    logs_path = vault_path / "02_Practice_Logs"
    logs_path.mkdir(parents=True, exist_ok=True)

    # Get drill info
    content = drill_path.read_text(encoding="utf-8")
    frontmatter, _ = parse_frontmatter(content)
    drill_id = frontmatter.get("id", "unknown")
    drill_title = drill_path.stem.replace("DRILL__", "")

    # Create log
    timestamp = datetime.now().isoformat()
    date_str = datetime.now().strftime("%Y-%m-%d")

    log_content = f"""---
drill_id: {drill_id}
drill_title: {drill_title}
result: {result}
rating: {rating}
timestamp: {timestamp}
---

# Practice Log: {drill_title}

**Date:** {date_str}
**Result:** {result}

## Notes
{notes or "No notes provided."}

---
*Drill: [[{drill_path.name}]]*
"""

    log_file = logs_path / f"{date_str}__{slugify(drill_title)}.md"
    log_file.write_text(log_content, encoding="utf-8")

    return log_file


def mark_drill(vault_path: Path, drill_path: Path, result: str, notes: str = "", rating: int = 0) -> None:
    """Mark a drill with a result and update its status.

    Args:
        vault_path: Vault path
        drill_path: Path to drill file
        result: Result (passed/failed/bullshit/outdated)
        notes: Optional notes
    """
    # Create practice log
    create_practice_log(vault_path, drill_path, result, notes, rating)

    # Update drill frontmatter
    content = drill_path.read_text(encoding="utf-8")
    frontmatter, _ = parse_frontmatter(content)

    review_count = frontmatter.get("review_count", 0)

    if result == "passed":
        # Spaced repetition intervals
        intervals = [7, 21, 60]
        if review_count < len(intervals):
            next_review = (datetime.now() + timedelta(days=intervals[review_count])).date()
        else:
            next_review = (datetime.now() + timedelta(days=90)).date()

        updates = {
            "status": "passed",
            "review_count": review_count + 1,
            "next_review": next_review.isoformat(),
        }

    elif result == "failed":
        # Review tomorrow
        next_review = (datetime.now() + timedelta(days=1)).date()
        updates = {
            "status": "failed",
            "next_review": next_review.isoformat(),
        }

    elif result in {"bullshit", "outdated"}:
        # Move to archive
        updates = {"status": result}
        archive_path = vault_path / "90_Archive"
        archive_path.mkdir(parents=True, exist_ok=True)
        new_path = archive_path / drill_path.name
        update_frontmatter(drill_path, updates)
        drill_path.rename(new_path)
        return

    else:
        raise ValueError(f"Invalid result: {result}")

    update_frontmatter(drill_path, updates)


def promote_to_mastery(vault_path: Path, drill_path: Path, reflection: str = "") -> Path:
    """Promote a passed drill to Mastery with rich details.

    Args:
        vault_path: Vault path
        drill_path: Path to drill file
        reflection: Optional reflection from practice log

    Returns:
        Path to created mastery note
    """
    from .ingestor import slugify

    mastery_path = vault_path / "10_Mastery"
    mastery_path.mkdir(parents=True, exist_ok=True)

    # Read drill
    content = drill_path.read_text(encoding="utf-8")
    frontmatter, body = parse_frontmatter(content)

    drill_title = drill_path.stem.replace("DRILL__", "").replace("-", " ").title()

    # Extract sections from body with more precision
    def extract_section(name: str) -> str:
        # Match from "## Name" to the next "##" or end of file
        pattern = rf"## {name}\n(.*?)(?=\n##|$)"
        match = re.search(pattern, body, re.DOTALL)
        return match.group(1).strip() if match else ""

    pattern_text = extract_section("Pattern")
    drill_text = extract_section("Drill")
    snippet_text = extract_section("Snippet")
    failure_modes = extract_section("Failure Modes")
    next_variation = extract_section("Next Variation")

    # Create mastery note with richer template
    mastery_content = f"""---
type: mastery
source_drill_id: {frontmatter.get('id', '')}
topics: {frontmatter.get('topics', [])}
verified_at: {datetime.now().isoformat()}
---

# {drill_title}

## 💡 Concept Definition
{reflection if reflection else pattern_text}

## 🎯 When to Use
- **Primary Use Case:** [Identify when this pattern is the most effective solution]
- **Constraints:** [When is this NOT the right tool?]

## 💻 Minimal Working Example
{snippet_text}

## ⚠️ Pitfalls & Gotchas
{failure_modes if failure_modes else "- Check for early exit conditions\\n- Ensure all dependencies are initialized"}

## 🛠️ Verification Protocol
{drill_text}

## 🔗 Knowledge Graph
- **Related Topics:** {", ".join([f"[[{t}]]" for t in frontmatter.get('topics', [])])}
- **Proof:** [[{drill_path.name}]]
- **Harder Variation:** {next_variation if next_variation else "Try combining this with another pattern"}

---
*Automatically promoted on {datetime.now().date()}*
"""

    mastery_file = mastery_path / f"MASTERY__{slugify(drill_title)}.md"
    mastery_file.write_text(mastery_content, encoding="utf-8")

    # Update topic index after promotion
    update_topic_indices(vault_path)

    return mastery_file


def update_topic_indices(vault_path: Path) -> None:
    """Rebuild Topic Index notes in 11_Topics/."""
    topics_path = vault_path / "11_Topics"
    topics_path.mkdir(parents=True, exist_ok=True)

    # Map topics to mastery notes and drills
    topic_map = {}

    # 1. Collect from Mastery
    mastery_path = vault_path / "10_Mastery"
    if mastery_path.exists():
        for master_file in mastery_path.glob("MASTERY__*.md"):
            content = master_file.read_text(encoding="utf-8")
            fm, _ = parse_frontmatter(content)
            topics = fm.get("topics", [])
            for topic in topics:
                if topic not in topic_map:
                    topic_map[topic] = {"mastery": [], "drills": []}
                topic_map[topic]["mastery"].append(master_file.name)

    # 2. Collect from Drills (for stats)
    drills_path = vault_path / "01_Drills"
    if drills_path.exists():
        for drill_file in drills_path.glob("DRILL__*.md"):
            content = drill_file.read_text(encoding="utf-8")
            fm, _ = parse_frontmatter(content)
            topics = fm.get("topics", [])
            for topic in topics:
                if topic not in topic_map:
                    topic_map[topic] = {"mastery": [], "drills": []}
                topic_map[topic]["drills"].append({
                    "name": drill_file.name,
                    "status": fm.get("status", "untried"),
                    "title": drill_file.stem.replace("DRILL__", "").replace("-", " ").title()
                })

    # 3. Write Topic Notes
    for topic, data in topic_map.items():
        topic_slug = topic.replace(" ", "_").replace("/", "_")
        topic_file = topics_path / f"{topic_slug}.md"
        
        # Calculate stats
        total_drills = len(data["drills"])
        passed_drills = len([d for d in data["drills"] if d["status"] == "passed"])
        pass_rate = (passed_drills / total_drills * 100) if total_drills > 0 else 0

        m_links = "\n".join([f"- [[{m}]]" for m in data["mastery"]])
        d_links = "\n".join([f"- [[{d['name']}]] ({d['status']})" for d in data["drills"]])

        content = f"""---
type: topic
name: {topic}
pass_rate: {pass_rate:.1f}%
---

# Topic Index: {topic}

## 📖 Definition
[Add a 1-2 sentence definition of {topic} here]

## 🎓 Mastery Notes
{m_links if m_links else "*No mastery notes yet.*"}

## 🏋️ Practice Drills
**Pass Rate:** {pass_rate:.1f}% ({passed_drills}/{total_drills})

{d_links if d_links else "*No drills found for this topic.*"}

## 🗺️ Learning Path
1. **Beginner:** {data['drills'][0]['title'] if data['drills'] else "N/A"}
2. **Intermediate:** ...
3. **Advanced:** ...

---
*Index updated: {datetime.now().isoformat()}*
"""
        topic_file.write_text(content, encoding="utf-8")


def get_topics_stats(vault_path: Path) -> list[dict]:
    """Get statistics for all topics."""
    # We can reuse the logic from update_topic_indices but just return data
    mastery_path = vault_path / "10_Mastery"
    drills_path = vault_path / "01_Drills"
    
    topic_data = {}

    def get_topics(fm):
        t = fm.get("topics", [])
        if isinstance(t, str):
            return [t.strip()]
        return t

    if drills_path.exists():
        for f in drills_path.glob("DRILL__*.md"):
            fm, _ = parse_frontmatter(f.read_text(encoding="utf-8"))
            for t in get_topics(fm):
                if t not in topic_data:
                    topic_data[t] = {"drills": 0, "passed": 0, "mastery": 0, "last_practiced": None}
                topic_data[t]["drills"] += 1
                if fm.get("status") == "passed":
                    topic_data[t]["passed"] += 1

    if mastery_path.exists():
        for f in mastery_path.glob("MASTERY__*.md"):
            fm, _ = parse_frontmatter(f.read_text(encoding="utf-8"))
            for t in get_topics(fm):
                if t in topic_data:
                    topic_data[t]["mastery"] += 1
                else:
                    topic_data[t] = {"drills": 0, "passed": 0, "mastery": 1, "last_practiced": None}

    # Collect ratings and last practiced per drill ID
    drill_to_metrics = {}
    logs_path = vault_path / "02_Practice_Logs"
    if logs_path.exists():
        for log_file in logs_path.glob("*.md"):
            fm, _ = parse_frontmatter(log_file.read_text(encoding="utf-8"))
            d_id = fm.get("drill_id")
            if d_id:
                if d_id not in drill_to_metrics:
                    drill_to_metrics[d_id] = {"ratings": [], "last": None}
                
                rating = fm.get("rating", 0)
                if rating > 0:
                    drill_to_metrics[d_id]["ratings"].append(rating)
                
                match = re.match(r"(\d{4}-\d{2}-\d{2})", log_file.name)
                if match:
                    log_date = datetime.fromisoformat(match.group(1)).date()
                    if not drill_to_metrics[d_id]["last"] or log_date > drill_to_metrics[d_id]["last"]:
                        drill_to_metrics[d_id]["last"] = log_date

    # Now we need to map drills to their topics to aggregate ratings
    for f in drills_path.glob("DRILL__*.md"):
        fm, _ = parse_frontmatter(f.read_text(encoding="utf-8"))
        d_id = fm.get("id")
        if d_id in drill_to_metrics:
            for t in get_topics(fm):
                if t in topic_data:
                    if "all_ratings" not in topic_data[t]:
                        topic_data[t]["all_ratings"] = []
                    topic_data[t]["all_ratings"].extend(drill_to_metrics[d_id]["ratings"])

    results = []
    for topic, stats in topic_data.items():
        ratings = stats.get("all_ratings", [])
        avg_rating = sum(ratings) / len(ratings) if ratings else 0
        
        results.append({
            "name": topic,
            "mastery": stats["mastery"],
            "passed": stats["passed"],
            "total": stats["drills"],
            "avg_rating": avg_rating
        })
    
    return sorted(results, key=lambda x: x["mastery"], reverse=True)


def get_vault_stats(vault_path: Path) -> dict:
    """Calculate vault statistics."""
    stats = {
        "drills": {"untried": 0, "passed": 0, "failed": 0, "total": 0},
        "mastery": 0,
        "sources": 0,
    }

    # Drills
    drills_path = vault_path / "01_Drills"
    if drills_path.exists():
        for drill_file in drills_path.glob("DRILL__*.md"):
            stats["drills"]["total"] += 1
            content = drill_file.read_text(encoding="utf-8")
            frontmatter, _ = parse_frontmatter(content)
            status = frontmatter.get("status", "untried")
            if status in stats["drills"]:
                stats["drills"][status] += 1

    # Mastery
    mastery_path = vault_path / "10_Mastery"
    if mastery_path.exists():
        stats["mastery"] = len(list(mastery_path.glob("MASTERY__*.md")))

    # Sources
    inbox_path = vault_path / "00_Inbox"
    if inbox_path.exists():
        stats["sources"] = len(list(inbox_path.glob("SOURCE__*.md")))

    return stats


def get_streak(vault_path: Path) -> int:
    """Calculate current practice streak in days."""
    logs_path = vault_path / "02_Practice_Logs"
    if not logs_path.exists():
        return 0

    # Get all unique dates from log filenames (YYYY-MM-DD__slug.md)
    log_dates = set()
    for log_file in logs_path.glob("*.md"):
        # Match YYYY-MM-DD at the start
        match = re.match(r"(\d{4}-\d{2}-\d{2})", log_file.name)
        if match:
            log_dates.add(datetime.fromisoformat(match.group(1)).date())

    if not log_dates:
        return 0

    sorted_dates = sorted(list(log_dates), reverse=True)
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)

    # If haven't practiced today or yesterday, streak is 0
    if sorted_dates[0] < yesterday:
        return 0

    streak = 0
    current_date = sorted_dates[0]

    # Handle case where user practiced today
    if current_date == today:
        streak = 1
        expected_date = today - timedelta(days=1)
        for date in sorted_dates[1:]:
            if date == expected_date:
                streak += 1
                expected_date -= timedelta(days=1)
            else:
                break
    # Handle case where user practiced yesterday but not today yet
    elif current_date == yesterday:
        streak = 1
        expected_date = yesterday - timedelta(days=1)
        for date in sorted_dates[1:]:
            if date == expected_date:
                streak += 1
                expected_date -= timedelta(days=1)
            else:
                break

    return streak


def get_upcoming_drills(vault_path: Path, count: int = 3) -> list[dict]:
    """Get the next few drills due for practice."""
    drills_path = vault_path / "01_Drills"
    if not drills_path.exists():
        return []

    today = datetime.now().date()
    candidates = []

    for drill_file in drills_path.glob("DRILL__*.md"):
        content = drill_file.read_text(encoding="utf-8")
        frontmatter, _ = parse_frontmatter(content)

        status = frontmatter.get("status", "untried")
        next_review_str = frontmatter.get("next_review", "")

        if next_review_str:
            next_review = datetime.fromisoformat(str(next_review_str)).date()
        else:
            next_review = today

        # Priority score (lower is higher priority)
        priority = {"untried": 0, "failed": 1, "passed": 2}.get(status, 3)
        
        candidates.append({
            "path": drill_file,
            "title": drill_file.stem.replace("DRILL__", "").replace("-", " ").title(),
            "status": status,
            "next_review": next_review,
            "priority": priority,
            "topics": frontmatter.get("topics", []),
            "is_due": next_review <= today
        })

    # Sort: due first, then by priority, then by date, then by title
    candidates.sort(key=lambda x: (not x["is_due"], x["priority"], x["next_review"], x["title"]))
    
    return candidates[:count]


def update_obsidian_dashboard(vault_path: Path) -> Path:
    """Generate or update the _Dashboard.md note for Obsidian."""
    dashboard_path = vault_path / "_Dashboard.md"
    
    stats = get_vault_stats(vault_path)
    streak = get_streak(vault_path)
    
    # Mastery Level Badge
    mastery_count = stats['mastery']
    level = "Beginner 👶"
    if mastery_count >= 16:
        level = "Expert 🏆"
    elif mastery_count >= 6:
        level = "Apprentice ⚔️"

    content = f"""# 🥋 Vibe-Dojo Dashboard

## 📊 Quick Stats
- **Rank:** {level}
- **Mastery:** {mastery_count} notes verified
- **Streak:** {streak} days 🔥
- **Total Drills:** {stats['drills']['total']}

---

## 📅 Due for Practice
```dataview
TABLE 
    status as Status, 
    next_review as "Next Review",
    topics as Topics
FROM "01_Drills"
WHERE next_review <= date(today) 
  AND status != "passed"
  AND status != "bullshit"
  AND status != "outdated"
SORT next_review ASC, status ASC
```

## 🧠 Knowledge Topics
```dataview
TABLE 
    pass_rate as "Mastery %",
    length(file.outlinks) as "Mastery Notes"
FROM "11_Topics"
SORT pass_rate DESC
```

## 🕒 Recent Activity
```dataview
LIST
FROM "02_Practice_Logs"
SORT file.ctime DESC
LIMIT 10
```

---
*Dashboard updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""
    dashboard_path.write_text(content, encoding="utf-8")
    return dashboard_path
