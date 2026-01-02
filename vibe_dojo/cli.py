"""CLI interface for Vibe-Dojo."""

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from .config import Config
from dotenv import load_dotenv

load_dotenv()

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
        "11_Topics",
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
dojo list-sources        # Find source IDs
dojo distill <id>        # Auto-generate drills
dojo status              # Check vault dashboard
dojo topics              # See knowledge by topic
dojo next                # Get next drill (interactive!)
dojo insights            # Get AI learning coaching
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
def capture(
    url: str = typer.Argument(..., help="URL to capture"),
    vault: Optional[Path] = typer.Option(None, help="Vault path (default: current directory)"),
):
    """Quick-capture a URL to the inbox without fetching immediately."""
    from .ingestor import slugify
    from datetime import datetime
    from ulid import ULID

    vault_path = vault or Path.cwd()
    vault_path = vault_path.resolve()
    
    source_id = str(ULID())
    captured_at = datetime.now().isoformat()
    
    note_content = f"""---
id: {source_id}
source_kind: pending
url: {url}
captured_at: {captured_at}
status: pending
---

# Captured: {url}

Pending distillation. Run `dojo distill-inbox` to process.
"""
    inbox_path = vault_path / "00_Inbox"
    inbox_path.mkdir(parents=True, exist_ok=True)
    
    note_file = inbox_path / f"SOURCE__pending__{source_id}.md"
    note_file.write_text(note_content, encoding="utf-8")
    
    console.print(f"[bold green]✓ URL Captured:[/bold green] {url}")
    console.print(f"[dim]Run 'dojo distill-inbox' later to process.[/dim]")


@app.command()
def listen(
    port: int = typer.Option(8080, help="Port to listen on"),
    vault: Optional[Path] = typer.Option(None, help="Vault path (default: current directory)"),
):
    """Start a local server to capture URLs from a bookmarklet."""
    from http.server import HTTPServer, BaseHTTPRequestHandler
    from urllib.parse import urlparse, parse_qs

    vault_path = vault or Path.cwd()
    vault_path = vault_path.resolve()

    class CaptureHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            query = parse_qs(urlparse(self.path).query)
            urls = query.get("url")
            url = urls[0] if urls else None
            
            if url:
                # Call capture logic
                capture(url=url, vault=vault_path)
                
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(b"<html><body><h1>Captured!</h1><script>setTimeout(window.close, 1000)</script></body></html>")
            else:
                self.send_response(400)
                self.end_headers()

        def log_message(self, format, *args):
            return # Silent logs

    console.print(f"[bold blue]👂 Vibe-Capture Listening on port {port}...[/bold blue]")
    console.print(f"[dim]Bookmarklet URL: http://localhost:{port}/?url=[/dim]")
    
    bookmarklet_js = f"javascript:location.href='http://localhost:{port}/?url='+encodeURIComponent(location.href);"
    console.print(f"\n[bold green]Bookmarklet JS:[/bold green]\n{{bookmarklet_js}}\n")
    
    try:
        server = HTTPServer(("localhost", port), CaptureHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        console.print("\n[yellow]Stopping listener...[/yellow]")


@app.command()
def list_sources(
    vault: Optional[Path] = typer.Option(None, help="Vault path (default: current directory)"),
):
    """List all source notes with their IDs."""
    vault_path = vault or Path.cwd()
    vault_path = vault_path.resolve()

    inbox_path = vault_path / "00_Inbox"
    source_files = sorted(inbox_path.glob("SOURCE__*.md"))

    if not source_files:
        console.print("[yellow]No source notes found.[/yellow]")
        console.print("\n[dim]Create one with: dojo ingest <url>[/dim]")
        return

    console.print(f"[bold blue]Source Notes ({len(source_files)}):[/bold blue]\n")

    for source_file in source_files:
        content = source_file.read_text(encoding="utf-8")
        lines = content.split("\n")

        # Parse frontmatter
        source_id = None
        source_kind = None
        url = None
        in_frontmatter = False

        for line in lines:
            if line.strip() == "---":
                if not in_frontmatter:
                    in_frontmatter = True
                else:
                    break
            elif in_frontmatter:
                if line.startswith("id:"):
                    source_id = line.split(":", 1)[1].strip()
                elif line.startswith("source_kind:"):
                    source_kind = line.split(":", 1)[1].strip()
                elif line.startswith("url:"):
                    url = line.split(":", 1)[1].strip()

        # Extract title from filename or frontmatter
        title = source_file.stem.replace("SOURCE__", "").replace("-", " ").title()

        console.print(f"[bold]{title}[/bold]")
        console.print(f"  ID: [cyan]{source_id}[/cyan]")
        console.print(f"  Type: {source_kind or 'unknown'}")
        if url:
            console.print(f"  URL: {url}")
        console.print()

    console.print("[dim]To generate drills: dojo distill <source-id>[/dim]")


@app.command()
def status(
    vault: Optional[Path] = typer.Option(None, help="Vault path (default: current directory)"),
):
    """Show vault statistics and practice dashboard."""
    from rich.panel import Panel
    from rich.table import Table
    from .trainer import get_vault_stats, get_streak, get_upcoming_drills

    vault_path = vault or Path.cwd()
    vault_path = vault_path.resolve()

    stats = get_vault_stats(vault_path)
    streak = get_streak(vault_path)
    upcoming = get_upcoming_drills(vault_path)
    
    # Auto-update Obsidian dashboard
    from .trainer import update_obsidian_dashboard
    update_obsidian_dashboard(vault_path)

    # Header
    console.print(f"\n[bold blue]🥋 Vibe-Dojo Dashboard[/bold blue] [dim]| {vault_path.name}[/dim]\n")

    # Stats Row
    stats_table = Table.grid(expand=True)
    stats_table.add_column(justify="center", ratio=1)
    stats_table.add_column(justify="center", ratio=1)
    stats_table.add_column(justify="center", ratio=1)

    # Drill counts
    d = stats["drills"]
    total = d["total"]
    
    drill_stats = f"[bold white]{total}[/bold white] Total Drills\n" \
                  f"[green]{d['passed']} Passed[/green] | " \
                  f"[red]{d['failed']} Failed[/red] | " \
                  f"[yellow]{d['untried']} New[/yellow]"

    # Calculate Level
    mastery_count = stats['mastery']
    if mastery_count >= 16:
        level = "Expert 🏆"
        level_style = "bold gold1"
    elif mastery_count >= 6:
        level = "Apprentice ⚔️"
        level_style = "bold cyan"
    else:
        level = "Beginner 👶"
        level_style = "bold green"

    # Calculate Streak Emoji
    streak_emoji = ""
    if streak >= 30:
        streak_emoji = " 🔥🔥🔥"
    elif streak >= 7:
        streak_emoji = " 🔥🔥"
    elif streak >= 3:
        streak_emoji = " 🔥"

    stats_table.add_row(
        Panel(drill_stats, title="[bold]Drills[/bold]", border_style="blue"),
        Panel(f"[{level_style}]{level}[/{level_style}]\n{mastery_count} Mastered Drills", title="[bold]Rank[/bold]", border_style="gold1"),
        Panel(f"[bold orange_red1]{streak} days{streak_emoji}[/bold orange_red1]\nPractice Streak", title="[bold]Streak[/bold]", border_style="orange_red1")
    )
    console.print(stats_table)

    # Upcoming Drills
    upcoming_table = Table(title="\n[bold]Next Practice Sessions[/bold]", show_header=True, header_style="bold magenta", expand=True)
    upcoming_table.add_column("Drill", style="white")
    upcoming_table.add_column("Status", justify="center")
    upcoming_table.add_column("Next Review", justify="center")
    upcoming_table.add_column("Topics", style="dim")

    for drill in upcoming:
        status_color = {"untried": "yellow", "failed": "red", "passed": "green"}.get(drill["status"], "white")
        due_str = "[bold red]DUE NOW[/bold red]" if drill["is_due"] else f"[dim]{drill['next_review']}[/dim]"
        
        upcoming_table.add_row(
            drill["title"],
            f"[{status_color}]{drill['status']}[/{status_color}]",
            due_str,
            ", ".join(drill["topics"])
        )

    if not upcoming:
        console.print("[yellow]No drills found to practice. Go ingest some content![/yellow]")
    else:
        console.print(upcoming_table)

    # Footer Advice
    if d["untried"] > 5:
        console.print("\n[dim italic]💡 Pro-tip: You have many untried drills. Focus on clearing the inbox before distilling more.[/dim italic]")
    elif streak < 1:
        console.print("\n[dim italic]💡 Start a new streak today! Run 'dojo next' to practice.[/dim italic]")


@app.command()
def distill_inbox(
    vault: Optional[Path] = typer.Option(None, help="Vault path (default: current directory)"),
    num_drills: int = typer.Option(2, "--num", help="Number of drills per source"),
):
    """Process all pending/captured URLs in the inbox."""
    from .ingestor import create_source_note
    from .distiller import create_drills_from_source
    from .trainer import parse_frontmatter

    vault_path = vault or Path.cwd()
    vault_path = vault_path.resolve()

    inbox_path = vault_path / "00_Inbox"
    pending_files = list(inbox_path.glob("SOURCE__pending__*.md"))

    if not pending_files:
        console.print("[yellow]No pending captures found in inbox.[/yellow]")
        return

    console.print(f"[bold blue]📦 Processing {len(pending_files)} pending captures...[/bold blue]\n")

    for pending_file in pending_files:
        content = pending_file.read_text(encoding="utf-8")
        frontmatter, _ = parse_frontmatter(content)
        url = frontmatter.get("url")

        if not url:
            continue

        console.print(f"🌐 [bold]Ingesting:[/bold] {url}")
        try:
            # 1. Ingest (Fetch full content)
            new_note_path = create_source_note(vault_path, url=url)
            
            # Get the new ID from the actual note created
            new_content = new_note_path.read_text(encoding="utf-8")
            new_fm, _ = parse_frontmatter(new_content)
            source_id = new_fm.get("id")

            # 2. Distill (Generate drills)
            console.print(f"  🧠 Distilling drills...")
            create_drills_from_source(vault_path, source_id, num_drills=num_drills)

            # 3. Clean up
            pending_file.unlink()
            console.print(f"  [green]✓ Success![/green]\n")

        except Exception as e:
            console.print(f"  [red]✗ Failed:[/red] {e}\n")

    console.print("[bold green]✓ Inbox processing complete![/bold green]")


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


@app.command(name="next")
def next_drill(
    vault: Optional[Path] = typer.Option(None, help="Vault path (default: current directory)"),
):
    """Show the next drill to practice."""
    from .trainer import get_next_drill, parse_frontmatter

    vault_path = vault or Path.cwd()
    vault_path = vault_path.resolve()

    drill_path = get_next_drill(vault_path)

    if not drill_path:
        from .trainer import count_today_logs
        from .config import Config
        config = Config(vault_path).config
        max_per_day = config.get("defaults", {}).get("max_drills_per_day", 5)
        
        if count_today_logs(vault_path) >= max_per_day:
            console.print("\n[bold green]🧘 Daily goal complete! Come back tomorrow.[/bold green]")
            console.print("[dim]Focus on integration and rest today.[/dim]")
        else:
            console.print("[yellow]No drills available for practice.[/yellow]")
            console.print("\n[dim]Create a drill with: dojo create-drill --title \"...\"[/dim]")
        return

    # Display drill
    content = drill_path.read_text(encoding="utf-8")
    frontmatter, body = parse_frontmatter(content)

    from rich.markdown import Markdown
    from rich.panel import Panel
    from rich.prompt import Prompt
    from .trainer import mark_drill, promote_to_mastery, get_topics_stats

    # Calculate Context
    status = frontmatter.get("status", "untried")
    topics = frontmatter.get("topics", [])
    topic_str = "General"
    if topics:
        # Get progress for the first topic
        ts = get_topics_stats(vault_path)
        topic_data = next((t for t in ts if t["name"] == topics[0]), None)
        if topic_data:
            topic_str = f"{topics[0]}: {topic_data['passed']}/{topic_data['total']} mastered"

    if status == "untried":
        reason = "New drill added to your inbox"
    elif status == "failed":
        reason = "Scheduled review after previous failure"
    else:
        reason = "Spaced repetition review"

    timebox = frontmatter.get('timebox_min', 10)

    # Show Context Panel
    console.print(Panel(
        f"[bold cyan]Reason:[/bold cyan] {reason}\n"
        f"[bold gold1]Topic:[/bold gold1] {topic_str}\n"
        f"[bold yellow]Timebox:[/bold yellow] {timebox} mins",
        title="[bold]CONTEXT[/bold]",
        border_style="dim"
    ))

    console.print(Panel(Markdown(content), title=f"[bold blue]NEXT DRILL[/bold blue]", border_style="blue"))
    console.print("[dim]Focus deeply. Do the work. Verify against validation steps.[/dim]\n")

    # Interactive Loop
    action = Prompt.ask(
        "Action? [bold green](p)assed[/bold green] / [bold red](f)ailed[/bold red] / [dim](s)kip / (q)uit[/dim]",
        choices=["p", "f", "s", "q"],
        default="p"
    )

    if action == "q":
        raise typer.Exit()
    elif action == "s":
        console.print("[dim]Skipped. Use 'dojo next' to see another.[/dim]")
        return

    result_map = {"p": "passed", "f": "failed"}
    result = result_map[action]

    notes = ""
    if result == "passed":
        notes = Prompt.ask("Reflection: [italic]What did you learn? (optional)[/italic]", default="")

    rating = Prompt.ask("Rate this drill quality (1-5)", choices=["1", "2", "3", "4", "5"], default="5")

    try:
        mark_drill(vault_path, drill_path, result, notes, rating=int(rating))
        
        if result == "passed":
            # AUTO-PROMOTE ON PASS
            promote_to_mastery(vault_path, drill_path, reflection=notes)
            
            # ASCII Celebration
            console.print("""
      .   *   .
    *   .   *   .
  .   🎉 SUCCESS 🎉  .
    *   .   *   .
      .   *   .
""", style="bold yellow")
            
            console.print("[bold green]✓ Drill promoted to Mastery![/bold green]")
            # Look up stats for motivational feedback
            from .trainer import get_vault_stats
            stats = get_vault_stats(vault_path)
            mastery_count = stats["mastery"]
            
            # Topic promotion feedback
            topics = frontmatter.get("topics", [])
            if topics:
                console.print(f"[bold gold1]🏆 NEW MASTERY UNLOCKED in: {', '.join(topics)}[/bold gold1]")
            
            console.print(f"[dim]Total Mastery Notes: {mastery_count}[/dim]")
        else:
            console.print("\n[yellow]Keep at it! This drill will reappear tomorrow for another shot.[/yellow]")

        # Update Obsidian dashboard
        from .trainer import update_obsidian_dashboard
        update_obsidian_dashboard(vault_path)

    except Exception as e:
        console.print(f"[bold red]✗ Error marking drill:[/bold red] {e}")
        raise typer.Exit(1)


@app.command()
def topics(
    vault: Optional[Path] = typer.Option(None, help="Vault path (default: current directory)"),
):
    """Show all topics and knowledge statistics."""
    from rich.table import Table
    from .trainer import get_topics_stats, update_topic_indices

    vault_path = vault or Path.cwd()
    vault_path = vault_path.resolve()

    # Rebuild indices to ensure freshness
    update_topic_indices(vault_path)
    
    topics_data = get_topics_stats(vault_path)

    if not topics_data:
        console.print("[yellow]No topics found yet. Topics are extracted from drills.[/yellow]")
        return

    table = Table(title="🥋 Vibe-Dojo: Knowledge Topics", expand=True)
    table.add_column("Topic", style="bold cyan")
    table.add_column("Mastery Notes", justify="center", style="gold1")
    table.add_column("Drills (Passed/Total)", justify="center")
    table.add_column("Quality", justify="center")
    table.add_column("Status", justify="center")

    for t in topics_data:
        progress = (t["passed"] / t["total"] * 100) if t["total"] > 0 else 0
        status = "🟢 Solid" if progress > 80 else "🟡 Growing" if progress > 30 else "🔴 Early"
        
        rating_stars = "⭐" * round(t["avg_rating"]) if t["avg_rating"] > 0 else "[dim]N/A[/dim]"
        
        table.add_row(
            t["name"],
            str(t["mastery"]),
            f"{t['passed']}/{t['total']}",
            rating_stars,
            status
        )

    console.print(table)
    console.print(f"\n[dim]Total Topics: {len(topics_data)}[/dim]")


@app.command()
def insights(
    vault: Optional[Path] = typer.Option(None, help="Vault path (default: current directory)"),
    model: str = typer.Option("gemini-3-flash-preview", help="Gemini model to use"),
):
    """Get AI-powered coaching insights on your learning progress."""
    from .distiller import analyze_insights
    from rich.panel import Panel

    vault_path = vault or Path.cwd()
    vault_path = vault_path.resolve()

    console.print(f"[bold magenta]🧠 Dojo Coach is analyzing your vault...[/bold magenta]")
    
    with console.status("[bold green]Synthesizing logs and mastery...[/bold green]"):
        try:
            insight_text = analyze_insights(vault_path, model_name=model)
            from rich.markdown import Markdown
            console.print("\n")
            console.print(Panel(Markdown(insight_text), title="🥋 Coach's Briefing", border_style="magenta"))
        except Exception as e:
            console.print(f"[bold red]✗ Insight Generation Failed:[/bold red] {e}")
            raise typer.Exit(1)


@app.command()
def dashboard(
    vault: Optional[Path] = typer.Option(None, help="Vault path (default: current directory)"),
):
    """Update the Obsidian dashboard note."""
    from .trainer import update_obsidian_dashboard
    vault_path = vault or Path.cwd()
    vault_path = vault_path.resolve()
    
    path = update_obsidian_dashboard(vault_path)
    console.print(f"[bold green]✓ Dashboard updated:[/bold green] {path.name}")


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
def distill(
    source_id: str = typer.Argument(..., help="Source note ID to distill drills from"),
    vault: Optional[Path] = typer.Option(None, help="Vault path (default: current directory)"),
    num_drills: int = typer.Option(3, "--num", help="Number of drills to generate"),
    model: str = typer.Option("gemini-3-flash-preview", help="Gemini model to use"),
):
    """Use LLM to auto-generate drills from a source note."""
    from .distiller import create_drills_from_source

    vault_path = vault or Path.cwd()
    vault_path = vault_path.resolve()

    console.print(f"[bold blue]🧠 Distilling drills from source:[/bold blue] {source_id}")
    console.print(f"[dim]Using model: {model}[/dim]")
    console.print(f"[dim]Generating {num_drills} drill(s)...[/dim]\n")

    try:
        drill_paths = create_drills_from_source(
            vault_path, source_id, num_drills=num_drills, model_name=model
        )

        console.print(f"[bold green]✓ Generated {len(drill_paths)} drill(s):[/bold green]")
        for drill_path in drill_paths:
            console.print(f"  • {drill_path.name}")

        console.print("\n[dim]Run 'dojo next' to start practicing![/dim]")

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
    import sys
    # launch interactive mode if no arguments provided
    if len(sys.argv) == 1:
        from .interactive import InteractiveApp
        try:
            InteractiveApp().start()
        except KeyboardInterrupt:
            print("\n👋 Bye!")
    else:
        app()
