# Vibe-Dojo

**Trainer-first learning system**: URLs → Drills → Practice → Mastery

## 🧘 Core Philosophy

Vibe-Dojo is built on the principle that **doing is learning**. 
Most "second brain" systems are libraries of dead notes. Vibe-Dojo is a **gym for your mind**.

- **Trainer-First**: We prioritize drills over passive reading. Every source must eventually become an action.
- **Lean Capture**: Don't collect notes; collect challenges.
- **Mastery Protocol**: Only promoted to Mastery after verified performance.
- **Vibe-Driven**: Lightweight, command-line focused, and powered by LLM distillation.

## Installation

```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (Unix/macOS)
source .venv/bin/activate

# Install
pip install -e ".[dev]"
```

## Quick Start

```bash
# 1. Initialize a vault
dojo init-vault ./my-vault

# 2. Add your Gemini API key
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# 3. Capture & Process
dojo capture <url>       # Quick add
dojo distill-inbox       # Batch process (Fetch + AI Distill)

# 4. Mastery & Knowledge
dojo status              # Check vault dashboard
dojo topics              # See knowledge clusters (MOCs)
dojo next                # Practice next due drill (Interactive!)
dojo insights            # Get AI coaching on your progress
```

## Knowledge Layer

Vibe-Dojo now transforms your practice into an evergreen knowledge base:
- **Rich Mastery Notes**: Auto-generated deep-dives into concepts after you pass them.
- **Topic Index (MOCs)**: Automatic clustering in `11_Topics/` that shows your "Pass Rate" per topic.
- **AI Insights**: A dedicated coach that analyzes your logs to find blind spots.

## 🤖 Agentic Workflows

Some features are **Agent-Native**, meaning they are best performed by an AI Agent (like Antigravity or Claude) interacting directly with your vault using the rules in `_agent_rules/`.

- **Cheat Sheets**: Automatically generate at-a-glance summaries from Mastery Notes.
- **Consolidation**: Merge multiple related drills or notes into one guide.

### How to use
Simply ask your AI Assistant:
> *"Update the Cursor cheat sheet following the rules."*

The Agent will:
1. Read `_agent_rules/cheatsheet_rules.md`.
2. Extract unique commands and snippets from `10_Mastery/`.
3. Update `20_Quick_Reference/`.

## Project Structure

```
Lernplattform/
├── vibe_dojo/          # Main package
│   ├── cli.py          # CLI commands
│   ├── distiller.py    # LLM → Drills & Insights
│   └── trainer.py      # Spaced Repetition & Topic Indexing
...
```

## Vault Structure

```
vault/
├── 00_Inbox/           # Raw sources
├── 01_Drills/          # Practice drills
├── 02_Practice_Logs/   # Practice history
├── 10_Mastery/         # Verified knowledge
├── 11_Topics/          # Topic MOCs (Auto-indexed)
└── 90_Archive/         # Deprecated content
```

## Configuration

Customize your Dojo experience in `config.yaml`:

```yaml
defaults:
  max_drills_per_day: 5    # Prevent burnout with a daily cap
  timebox_min: 10          # Default practice length
  confidence_threshold: 0.6
llm:
  model: "gemini-3-flash-preview"
  temperature: 0.3
```

## Status

- [x] Step A: Scaffold + init-vault
- [x] Step B: ingest + create-drill
- [x] Step C: next + mark (trainer loop)
- [x] Step D: LLM distill
- [x] Step E: Polish (Dashboard + UX)

## Troubleshooting

### Startup Issues
If `start_dojo.bat` fails immediately:
1. Ensure you have run `python -m venv .venv`.
2. Ensure you have installed dependencies: `pip install -e .`.
3. Check the error message in the console.

### YouTube Errors
If you see `YouTubeTranscriptApi has no attribute list_transcripts`:
1. Your dependency version is too old.
2. Run: `.venv\Scripts\pip install --upgrade --force-reinstall youtube-transcript-api` to fix it.
