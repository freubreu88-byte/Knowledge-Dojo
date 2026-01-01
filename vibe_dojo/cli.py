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



if __name__ == "__main__":
    app()
