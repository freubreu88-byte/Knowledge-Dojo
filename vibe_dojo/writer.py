"""Markdown note writer."""

from datetime import datetime
from pathlib import Path

from ulid import ULID


def create_drill_note(
    vault_path: Path,
    title: str,
    pattern: list[str] = None,
    drill_goal: str = "",
    drill_steps: list[str] = None,
    validation: list[str] = None,
    snippet_type: str = "code",
    snippet_content: str = "",
    topics: list[str] = None,
    prereqs: list[str] = None,
    timebox_min: int = 10,
    source_id: str = "",
) -> Path:
    """Create a drill note in 01_Drills/.

    Args:
        vault_path: Path to vault
        title: Drill title
        pattern: List of pattern bullets
        drill_goal: Goal description
        drill_steps: List of steps
        validation: List of validation checks
        snippet_type: Type of snippet (code/prompt/commands)
        snippet_content: Snippet content
        topics: List of topics
        prereqs: List of prerequisites
        timebox_min: Timebox in minutes
        source_id: Source note ID

    Returns:
        Path to created drill note
    """
    from .ingestor import slugify

    drill_id = str(ULID())
    created_at = datetime.now().isoformat()
    next_review = datetime.now().date().isoformat()  # Available immediately

    # Defaults
    pattern = pattern or ["Pattern to be filled in"]
    drill_steps = drill_steps or ["Step to be filled in"]
    validation = validation or ["Validation check to be filled in"]
    topics = topics or []
    prereqs = prereqs or []

    slug = slugify(title)

    frontmatter = f"""---
id: {drill_id}
type: drill
status: untried
created: {created_at}
source_id: {source_id}
next_review: {next_review}
review_count: 0
timebox_min: {timebox_min}
topics: {topics}
prereqs: {prereqs}
---

# {title}

## Pattern
{chr(10).join(f"- {p}" for p in pattern)}

## Drill
**Goal:** {drill_goal or "To be defined"}

**Steps:**
{chr(10).join(f"{i+1}. {s}" for i, s in enumerate(drill_steps))}

## Snippet
```{snippet_type}
{snippet_content or "# Code/prompt to be added"}
```

## Validation
{chr(10).join(f"- [ ] {v}" for v in validation)}

## Failure Modes
- Common pitfall 1
- Common pitfall 2

## Next Variation
- Try variation 1
- Try variation 2
"""

    drill_dir = vault_path / "01_Drills"
    drill_dir.mkdir(parents=True, exist_ok=True)
    
    drill_file = drill_dir / f"DRILL__{slug}.md"
    drill_file.write_text(frontmatter, encoding="utf-8")

    return drill_file
