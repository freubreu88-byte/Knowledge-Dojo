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


def get_next_drill(vault_path: Path) -> Optional[Path]:
    """Get the next drill to practice.

    Priority:
    1. untried drills
    2. failed drills (due for review)
    3. passed drills (due for review)

    Returns:
        Path to drill file or None if no drills available
    """
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
    vault_path: Path, drill_path: Path, result: str, notes: str = ""
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


def mark_drill(vault_path: Path, drill_path: Path, result: str, notes: str = "") -> None:
    """Mark a drill with a result and update its status.

    Args:
        vault_path: Vault path
        drill_path: Path to drill file
        result: Result (passed/failed/bullshit/outdated)
        notes: Optional notes
    """
    # Create practice log
    create_practice_log(vault_path, drill_path, result, notes)

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


def promote_to_mastery(vault_path: Path, drill_path: Path) -> Path:
    """Promote a passed drill to Mastery.

    Args:
        vault_path: Vault path
        drill_path: Path to drill file

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

    # Extract sections from body
    pattern_match = re.search(r"## Pattern\n(.*?)(?=\n##|$)", body, re.DOTALL)
    drill_match = re.search(r"## Drill\n(.*?)(?=\n##|$)", body, re.DOTALL)
    snippet_match = re.search(r"## Snippet\n(.*?)(?=\n##|$)", body, re.DOTALL)

    pattern_text = pattern_match.group(1).strip() if pattern_match else ""
    drill_text = drill_match.group(1).strip() if drill_match else ""
    snippet_text = snippet_match.group(1).strip() if snippet_match else ""

    # Create mastery note
    mastery_content = f"""---
type: mastery
source_drill_id: {frontmatter.get('id', '')}
topics: {frontmatter.get('topics', [])}
verified_at: {datetime.now().isoformat()}
---

# {drill_title}

## Definition
{pattern_text}

## When to Use
- Use when: [to be filled]
- Don't use when: [to be filled]

## Minimal Example
{snippet_text}

## Pitfalls & Checks
{drill_text}

## Links
- Source Drill: [[{drill_path.name}]]
- Practice Logs: Search for `drill_id: {frontmatter.get('id', '')}`
"""

    mastery_file = mastery_path / f"MASTERY__{slugify(drill_title)}.md"
    mastery_file.write_text(mastery_content, encoding="utf-8")

    return mastery_file
