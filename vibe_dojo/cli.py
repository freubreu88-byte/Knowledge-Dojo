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


if __name__ == "__main__":
    app()
