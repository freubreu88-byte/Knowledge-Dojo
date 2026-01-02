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
            choice = IntPrompt.ask("Choose an option", choices=["1", "2", "3", "4", "5", "6"], default=3)
            
            try:
                if choice == 1:
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
                         
                         num_str = Prompt.ask("How many drills?", default="3")
                         try:
                             num = int(num_str)
                         except ValueError:
                             num = 3
                             
                         from .cli import distill
                         distill(source_id=source_id, vault=self.vault_path, num_drills=num)
                         
        except SystemExit:
             pass # Typer raises SystemExit on exit

    def _do_distill_inbox(self):
        """Interactive inbox distillation."""
        from .cli import distill_inbox
        
        # Check if there are pending files first to give better UX
        inbox_path = self.vault_path / "00_Inbox"
        pending = list(inbox_path.glob("SOURCE__pending__*.md"))
        
        if not pending:
            console.print("\n[yellow]Inbox is empty! Go 'Add Content' first.[/yellow]")
            return

        num_str = Prompt.ask("How many drills per source?", default="3")
        try:
             num = int(num_str)
        except ValueError:
             num = 3
        try:
             # Explicitly calling command function
             distill_inbox(vault=self.vault_path, num_drills=num)
        except SystemExit:
             pass

    def _do_practice_next(self):
        """Interactive practice session."""
        from .cli import next_drill
        
        # next_drill acts as a persistent session until user quits or runs out
        # We loop here to allow "just one more" flow naturally
        while True:
            try:
                next_drill(vault=self.vault_path)
                
                # If next_drill returns (meaning skipped or marked), ask to continue
                cont = Prompt.ask("\n[bold]Practice another?[/bold] [green](y)es[/green] / [dim](n)o[/dim]", choices=["y", "n"], default="y")
                if cont == "n":
                    break
                console.clear()
            except typer.Exit:
                break
            except Exception as e:
                console.print(f"[red]Error in practice session: {e}[/red]")
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
