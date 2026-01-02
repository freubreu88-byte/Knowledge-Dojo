"""Interactive CLI mode for Vibe-Dojo."""

import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich.markdown import Markdown

from .global_config import get_last_vault_path, set_last_vault_path

console = Console()


class InteractiveApp:
    def __init__(self):
        self.vault_path: Optional[Path] = get_last_vault_path()

    def start(self):
        """Start the interactive loop."""
        self._ensure_vault_path()
        
        while True:
            self._show_menu()
            choice = IntPrompt.ask("Choose an option", choices=["0", "1", "2", "3", "4", "5", "6"], default=3)
            
            try:
                if choice == 0:
                    self._do_create_vault()
                elif choice == 1:
                    self._do_ingest()
                elif choice == 2:
                    self._do_distill_inbox()
                elif choice == 3:
                    self._do_practice_next()
                elif choice == 4:
                    self._do_view_stats()
                elif choice == 5:
                    self._do_topics()
                elif choice == 6:
                    console.print("[bold blue]👋 Keep vibing![/bold blue]")
                    break
                    
                # Pause after action before returning to menu, unless it was just a quick check
                if choice != 6:
                    Prompt.ask("\n[dim]Press Enter to continue...[/dim]")
                    
            except Exception as e:
                console.print(f"\n[bold red]💥 Error:[/bold red] {e}")
                Prompt.ask("\n[dim]Press Enter to continue...[/dim]")

    def _ensure_vault_path(self):
        """Ensure we have a valid vault path."""
        if self.vault_path and self.vault_path.exists():
            console.print(f"[dim]Using vault: {self.vault_path}[/dim]")
            return

        console.print("[bold blue]🥋 Welcome to Vibe-Dojo![/bold blue]")
        path_str = Prompt.ask("Enter your vault path (or '.' for current dir)", default=".")
        path = Path(path_str).resolve()
        
        if not path.exists():
            create = Prompt.ask("Path does not exist. Create new vault here?", choices=["y", "n"], default="y")
            if create == "y":
                from .cli import init_vault
                init_vault(path)
            else:
                console.print("[red]Cannot proceed without a vault.[/red]")
                sys.exit(1)
        
        self.vault_path = path
        set_last_vault_path(path)

    def _show_menu(self):
        """Display the main menu."""
        console.clear()
        
        from .config import Config
        config = Config(self.vault_path).config
        model = config.get("llm", {}).get("model", "unknown")
        
        menu_text = f"""[bold blue]🥋 VIBE-DOJO CONTROL CENTER[/bold blue] [dim]| {self.vault_path.name}[/dim]
[dim]🤖 Model: {model}[/dim]

[0] 🆕 [bold]Create New Vault[/bold]
[1] 📥 [bold]Add Content[/bold] (URL/Text)
[2] 🧠 [bold]Process Inbox[/bold] (Distill pending)
[3] 💪 [bold]Practice Next[/bold] (Get smarter)
[4] 📊 [bold]View Stats[/bold] (Check streak)
[5] 🏆 [bold]Browse Topics[/bold] (Knowledge map)
[6] ❌ [bold]Exit[/bold]
"""
        console.print(Panel(menu_text, border_style="blue", expand=False))

    def _do_ingest(self):
        """Interactive ingestion."""
        console.print("\n[bold]📥 Add Content[/bold]")
        url = Prompt.ask("Enter URL (YouTube, Reddit, Blog) or Text")
        
        if not url:
            return

        from .cli import ingest
        # We call the CLI function directly. 
        # Note: Typer commands can be tricky to invoke directly if they use Context, 
        # but our ingest is simple. We might need to handle args manually if we want strictly 100% reuse,
        # but re-implementing the call wrapper is cleaner.
        
        console.print(f"[dim]Ingesting: {url}...[/dim]")
        # We must explicitly pass default values because calling a Typer command function directly 
        # doesn't trigger the default value logic from decorators in the same way if arguments are missing,
        # or worse, might act unexpectedly. 
        # Actually, Typer functions are just functions. The issue is likely that when we call it here, 
        # we are keeping it simple.
        try:
             # Pass explicit defaults to avoid Typer injection issues
             ingest(url, vault=self.vault_path, title=None, no_fetch=False)
             
             # Chained Flow: Ask to distill immediately
             if Prompt.ask("\n[bold]Generate drills from this source?[/bold]", choices=["y", "n"], default="y") == "y":
                 # We need the ID of the source we just created.
                 # Since ingest doesn't return the ID easily (prints it), we finds the most recent source note.
                 inbox_path = self.vault_path / "00_Inbox"
                 # Find newest file
                 sources = list(inbox_path.glob("SOURCE__*.md"))
                 if sources:
                     newest = max(sources, key=lambda p: p.stat().st_mtime)
                     content = newest.read_text(encoding="utf-8")
                     
                     # Extract ID
                     import re
                     id_match = re.search(r"id: ([\w\d]+)", content)
                     if id_match:
                         source_id = id_match.group(1)
                         self._propose_and_select_drills(source_id)
                         
        except SystemExit:
             pass # Typer raises SystemExit on exit
             
    def _propose_and_select_drills(self, source_id: str):
        """Analyze content and let user select drills."""
        from .config import Config
        from .distiller import distill_drills
        from .writer import create_drill_note
        from .distiller import load_source_content, get_existing_context
        
        config = Config(self.vault_path).config
        model = config.get("llm", {}).get("model", "gemini-1.5-flash")
        
        console.print(f"\n[bold blue]🧠 Analyzing content with {model}...[/bold blue]")
        
        # 1. Get Proposals
        try:
             # Manually loading content here to pass to distill_drills
             # This duplicates logic in create_drills_from_source but gives us the raw list first
             source_content, source_metadata = load_source_content(self.vault_path, source_id)
             existing_context = get_existing_context(self.vault_path)
             
             with console.status("[bold green]Designing drills...[/bold green]"):
                 proposals = distill_drills(
                     source_content, 
                     source_metadata, 
                     model_name=model, 
                     existing_context=existing_context
                 )
        except Exception as e:
            console.print(f"[red]Failed to generate proposals: {e}[/red]")
            return

        if not proposals:
            console.print("[yellow]No drills found in this content.[/yellow]")
            return

        # 2. Display Proposals
        from rich.table import Table
        table = Table(title=f"Proposed Drills from Content", show_header=True, header_style="bold magenta")
        table.add_column("#", style="dim", width=4)
        table.add_column("Confidence", justify="center", width=12)
        table.add_column("Drill", style="bold")
        table.add_column("Est. Time", justify="right")

        for idx, drill in enumerate(proposals, 1):
            confidence_val = drill.get('confidence_score', 3)
            # Ensure int for safety
            try:
                confidence_val = int(confidence_val)
            except:
                confidence_val = 3
                
            stars = "⭐" * confidence_val
            table.add_row(
                str(idx), 
                stars, 
                f"{drill['title']}\n[dim]{drill.get('drill_goal', 'No goal')}[/dim]", 
                f"{drill.get('timebox_min', 15)} min"
            )

        console.print(table)
        console.print("\n[dim]Tip: Enter numbers separated by commas (e.g. 1,3) or range (1-3).[/dim]")
        
        # 3. Selection
        selection = Prompt.ask(
            "[bold]Select drills to create[/bold] ([A]ll / [N]one)", 
            default="A"
        )
        
        selected_indices = []
        if selection.lower() == 'a':
            selected_indices = list(range(len(proposals)))
        elif selection.lower() == 'n':
            return
        else:
            # Parse "1,3, 5-7"
            parts = selection.split(',')
            for part in parts:
                part = part.strip()
                if '-' in part:
                    try:
                        start, end = map(int, part.split('-'))
                        # user input is 1-based, convert to 0-based
                        selected_indices.extend(range(start-1, end))
                    except ValueError:
                        pass
                else:
                    try:
                        idx = int(part) - 1
                        if 0 <= idx < len(proposals):
                            selected_indices.append(idx)
                    except ValueError:
                        pass
                        
        # 4. Create Files
        created_count = 0
        for idx in selected_indices:
            if idx >= len(proposals): continue
            
            drill = proposals[idx]
            create_drill_note(
                vault_path=self.vault_path,
                title=drill["title"],
                pattern=drill.get("pattern", []),
                drill_goal=drill.get("drill_goal", ""),
                drill_steps=drill.get("drill_steps", []),
                validation=drill.get("validation", []),
                snippet_type=drill.get("snippet_type", "code"),
                snippet_content=drill.get("snippet_content", ""),
                topics=drill.get("topics", []),
                timebox_min=drill.get("timebox_min", 15),
                source_id=source_id,
            )
            created_count += 1
            
        console.print(f"\n[bold green]✓ Created {created_count} drills![/bold green]")

    def _do_distill_inbox(self):
        """Interactive inbox distillation."""
        from .cli import distill_inbox, distill
        
        inbox_path = self.vault_path / "00_Inbox"
        pending = list(inbox_path.glob("SOURCE__pending__*.md"))
        
        if pending:
            console.print(f"\n[bold blue]📦 Found {len(pending)} pending captures.[/bold blue]")
            if Prompt.ask("Process all pending captures?", choices=["y", "n"], default="y") == "y":
                num_str = Prompt.ask("How many drills per source?", default="3")
                try:
                     num = int(num_str)
                except ValueError:
                     num = 3
                try:
                     distill_inbox(vault=self.vault_path, num_drills=num)
                except SystemExit:
                     pass
            return

        # If no pending, allow processing existing sources
        all_sources = sorted(list(inbox_path.glob("SOURCE__*.md")))
        # Filter out "SOURCE__.md" which might be a placeholder/artifact
        all_sources = [s for s in all_sources if s.stem != "SOURCE__"]

        if not all_sources:
            console.print("\n[yellow]Inbox is empty! Go 'Add Content' first.[/yellow]")
            return

        console.print("\n[bold blue]📥 No new pending captures, but found existing sources:[/bold blue]")
        
        from rich.table import Table
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="dim", width=4)
        table.add_column("Title", style="bold")
        table.add_column("ID", style="cyan")

        source_info = []
        for idx, source_file in enumerate(all_sources, 1):
            content = source_file.read_text(encoding="utf-8")
            import re
            id_match = re.search(r"id: ([\w\d]+)", content)
            source_id = id_match.group(1) if id_match else "unknown"
            title = source_file.stem.replace("SOURCE__", "").replace("-", " ").title()
            table.add_row(str(idx), title, source_id)
            source_info.append(source_id)

        console.print(table)
        
        choice = Prompt.ask("\n[bold]Select a source ID or # to re-distill[/bold] (or [N]one)", default="N")
        if choice.lower() == 'n':
            return

        target_id = None
        # Try numeric index first
        try:
            val = int(choice)
            if 1 <= val <= len(source_info):
                target_id = source_info[val-1]
        except ValueError:
            target_id = choice # Assume it's a direct ID

        if target_id:
            # Using the direct distill logic
            self._propose_and_select_drills(target_id)


    def _do_practice_next(self):
        """Interactive practice session."""
        from .cli import next_drill
        from .trainer import get_upcoming_drills
        from datetime import datetime
        import time
        
        while True:
            console.clear()
            console.print("\n[bold blue]💪 Vibe-Dojo: Practice Session[/bold blue]")
            
            # 1. Get available drills (showing up to 15 for selection)
            available = get_upcoming_drills(self.vault_path, count=15)
            
            if not available:
                console.print("[yellow]No drills available for practice right now.[/yellow]")
                return

            # 2. Show Table
            from rich.table import Table
            table = Table(title="Choose your Dojo Task", show_header=True, header_style="bold magenta")
            table.add_column("#", style="dim", width=4)
            table.add_column("Status", width=12)
            table.add_column("Topic", style="gold1")
            table.add_column("Drill", style="bold")
            table.add_column("Due Date", justify="right")

            today = datetime.now().date()
            for idx, d in enumerate(available, 1):
                status_style = {"passed": "green", "failed": "red", "untried": "cyan"}.get(d["status"], "white")
                due_val = d["next_review"]
                
                if due_val <= today:
                    due_str = "[bold green]NOW[/bold green]"
                else:
                    days = (due_val - today).days
                    due_str = f"in {days}d"
                
                topic = d["topics"][0] if d["topics"] else "General"
                table.add_row(
                    str(idx),
                    f"[{status_style}]{d['status'].upper()}[/{status_style}]",
                    f"{topic}",
                    d["title"],
                    due_str
                )
            
            console.print(table)
            console.print("\n[dim][Index #] Select | [ENTER] Recommended (#1) | [Q] Exit Dojo[/dim]")
            
            choice = Prompt.ask("Action", default="1")
            
            if choice.lower() == 'q':
                break
            
            selected_drill_name = None
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(available):
                    selected_drill_name = available[idx]["path"].name
                else:
                    console.print(f"[red]Invalid index: {choice}[/red]")
                    time.sleep(1)
                    continue
            except ValueError:
                console.print("[red]Please enter a number or 'q'.[/red]")
                time.sleep(1)
                continue
            
            if selected_drill_name:
                try:
                    next_drill(vault=self.vault_path, drill=selected_drill_name)
                    
                    # After finishing one, ask if they want more
                    cont = Prompt.ask("\n[bold]Keep training?[/bold] [green](y)es[/green] / [dim](n)o[/dim]", choices=["y", "n"], default="y")
                    if cont == "n":
                        break
                except typer.Exit:
                    break
                except Exception as e:
                    console.print(f"[red]Error: {e}[/red]")
                    break


    def _do_view_stats(self):
        """View dashboard."""
        from .cli import status
        console.clear()
        status(vault=self.vault_path)

    def _do_topics(self):
        """View topics."""
        from .cli import topics
        console.clear()
        topics(vault=self.vault_path)


    def _do_create_vault(self):
        """Create a new vault."""
        console.print("\n[bold]🆕 Create New Vault[/bold]")
        name = Prompt.ask("Enter vault name (folder will be created in current dir)")
        if not name:
            return

        new_path = Path.cwd() / name
        if new_path.exists():
            console.print(f"[red]Error: Folder '{name}' already exists![/red]")
            return
            
        from .cli import init_vault
        init_vault(new_path)
        
        self.vault_path = new_path
        set_last_vault_path(new_path)
        console.print(f"[bold green]Switched to new vault: {name}[/bold green]")
