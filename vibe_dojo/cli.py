"""CLI interface for Vibe-Dojo."""

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from .config import Config

app = typer.Typer(help="Vibe-Dojo: Trainer-first learning system")
console = Console()


@app.command()
def init_vault(
    path: Optional[Path] = typer.Argument(None, help="Vault path (default: current directory)"),
):
    """Initialize a new Vibe-Dojo vault with folder structure."""
    vault_path = path or Path.cwd()
    vault_path = vault_path.resolve()

    # Create folder structure
    folders = [
        "00_Inbox",
        "00_Inbox/_attachments",
        "01_Drills",
        "02_Practice_Logs",
        "10_Mastery",
        "90_Archive",
    ]

    console.print(f"[bold blue]Initializing vault at:[/bold blue] {vault_path}")

    for folder in folders:
        folder_path = vault_path / folder
        folder_path.mkdir(parents=True, exist_ok=True)
        console.print(f"  ✓ Created {folder}/")

    # Create config.yaml
    config = Config(vault_path)
    config.save()
    console.print("  ✓ Created config.yaml")

    # Create Home.md
    home_path = vault_path / "Home.md"
    home_content = """# Vibe-Dojo

Welcome to your trainer-first learning vault!

## Quick Start
```bash
dojo ingest <url>        # Add a source
dojo next                # Get next drill
dojo mark passed         # Mark drill as passed
```

## Folders
- `00_Inbox/` - Raw sources
- `01_Drills/` - Practice drills
- `02_Practice_Logs/` - Your practice history
- `10_Mastery/` - Verified knowledge
- `90_Archive/` - Deprecated content
"""
    home_path.write_text(home_content, encoding="utf-8")
    console.print("  ✓ Created Home.md")

    console.print("\n[bold green]✓ Vault initialized successfully![/bold green]")


@app.command()
def ingest(
    url_or_text: str = typer.Argument(..., help="URL to fetch or text content"),
    vault: Optional[Path] = typer.Option(None, help="Vault path (default: current directory)"),
    title: Optional[str] = typer.Option(None, help="Custom title for source note"),
    no_fetch: bool = typer.Option(False, "--no-fetch", help="Don't fetch URL, treat as text"),
):
    """Ingest content from URL or text and create a source note."""
    from .ingestor import create_source_note

    vault_path = vault or Path.cwd()
    vault_path = vault_path.resolve()

    try:
        if no_fetch or not url_or_text.startswith("http"):
            # Treat as text
            note_path = create_source_note(
                vault_path, text=url_or_text, title=title, no_fetch=True
            )
        else:
            # Fetch URL
            note_path = create_source_note(vault_path, url=url_or_text, title=title)

        console.print(f"[bold green]✓ Source note created:[/bold green] {note_path.name}")
        console.print(f"  Path: {note_path.relative_to(vault_path)}")

    except Exception as e:
        console.print(f"[bold red]✗ Error:[/bold red] {e}")
        raise typer.Exit(1)


@app.command()
def create_drill(
    title: str = typer.Option(..., "--title", help="Drill title"),
    vault: Optional[Path] = typer.Option(None, help="Vault path (default: current directory)"),
    source_id: Optional[str] = typer.Option(None, help="Source note ID"),
):
    """Create an empty drill from template."""
    from .writer import create_drill_note

    vault_path = vault or Path.cwd()
    vault_path = vault_path.resolve()

    try:
        drill_path = create_drill_note(vault_path, title=title, source_id=source_id or "")

        console.print(f"[bold green]✓ Drill created:[/bold green] {drill_path.name}")
        console.print(f"  Path: {drill_path.relative_to(vault_path)}")
        console.print("\n[dim]Edit the drill to add pattern, steps, and validation.[/dim]")

    except Exception as e:
        console.print(f"[bold red]✗ Error:[/bold red] {e}")
        raise typer.Exit(1)


@app.command()
def next(
    vault: Optional[Path] = typer.Option(None, help="Vault path (default: current directory)"),
):
    """Show the next drill to practice."""
    from .trainer import get_next_drill, parse_frontmatter

    vault_path = vault or Path.cwd()
    vault_path = vault_path.resolve()

    drill_path = get_next_drill(vault_path)

    if not drill_path:
        console.print("[yellow]No drills available for practice.[/yellow]")
        console.print("\n[dim]Create a drill with: dojo create-drill --title \"...\"[/dim]")
        return

    # Display drill
    content = drill_path.read_text(encoding="utf-8")
    frontmatter, body = parse_frontmatter(content)

    console.print(f"\n[bold blue]Next Drill:[/bold blue] {drill_path.name}")
    console.print(f"[dim]Status: {frontmatter.get('status', 'unknown')}[/dim]")
    console.print(f"[dim]Timebox: {frontmatter.get('timebox_min', 10)} minutes[/dim]")
    console.print(f"[dim]Topics: {', '.join(frontmatter.get('topics', []))}[/dim]\n")

    # Show body
    console.print(body)

    console.print("\n[bold green]Ready to practice?[/bold green]")
    console.print("When done, run: [bold]dojo mark passed[/bold] (or failed/bullshit/outdated)")


@app.command()
def mark(
    result: str = typer.Argument(..., help="Result: passed/failed/bullshit/outdated"),
    vault: Optional[Path] = typer.Option(None, help="Vault path (default: current directory)"),
    notes: Optional[str] = typer.Option(None, help="Optional notes about the practice"),
):
    """Mark the last shown drill with a result."""
    from .trainer import get_next_drill, mark_drill, promote_to_mastery

    vault_path = vault or Path.cwd()
    vault_path = vault_path.resolve()

    # Validate result
    valid_results = {"passed", "failed", "bullshit", "outdated"}
    if result not in valid_results:
        console.print(f"[bold red]✗ Invalid result:[/bold red] {result}")
        console.print(f"Valid options: {', '.join(valid_results)}")
        raise typer.Exit(1)

    # Get the drill (same as next would show)
    drill_path = get_next_drill(vault_path)

    if not drill_path:
        console.print("[yellow]No drill to mark.[/yellow]")
        return

    try:
        # Mark the drill
        mark_drill(vault_path, drill_path, result, notes or "")

        console.print(f"[bold green]✓ Drill marked as:[/bold green] {result}")

        # Auto-promote if passed
        if result == "passed":
            mastery_path = promote_to_mastery(vault_path, drill_path)
            console.print(f"[bold green]✓ Promoted to Mastery:[/bold green] {mastery_path.name}")

    except Exception as e:
        console.print(f"[bold red]✗ Error:[/bold red] {e}")
        raise typer.Exit(1)


@app.command()
def promote(
    drill_name: str = typer.Argument(..., help="Drill filename (e.g., DRILL__test.md)"),
    vault: Optional[Path] = typer.Option(None, help="Vault path (default: current directory)"),
):
    """Manually promote a drill to Mastery."""
    from .trainer import promote_to_mastery

    vault_path = vault or Path.cwd()
    vault_path = vault_path.resolve()

    drill_path = vault_path / "01_Drills" / drill_name

    if not drill_path.exists():
        console.print(f"[bold red]✗ Drill not found:[/bold red] {drill_name}")
        raise typer.Exit(1)

    try:
        mastery_path = promote_to_mastery(vault_path, drill_path)
        console.print(f"[bold green]✓ Promoted to Mastery:[/bold green] {mastery_path.name}")

    except Exception as e:
        console.print(f"[bold red]✗ Error:[/bold red] {e}")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
