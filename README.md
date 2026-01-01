# Vibe-Dojo

**Trainer-first learning system**: URLs → Drills → Practice → Mastery

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

# 3. (Coming soon) Ingest content
dojo ingest <url>

# 4. (Coming soon) Practice
dojo next
dojo mark passed
```

## Development Workflow

After every change, run:
```bash
ruff check . && pytest -q && dojo --help
```

## Project Structure

```
Lernplattform/
├── vibe_dojo/          # Main package
│   ├── cli.py          # CLI commands
│   ├── config.py       # Configuration
│   ├── ingestor.py     # (Coming) URL → Source Note
│   ├── extractor.py    # (Coming) LLM → Drill JSON
│   ├── writer.py       # (Coming) JSON → Markdown
│   └── trainer.py      # (Coming) next/mark/promote
├── tests/              # Tests
├── templates/          # Note templates
└── pyproject.toml      # Dependencies
```

## Vault Structure

```
vault/
├── 00_Inbox/           # Raw sources
│   └── _attachments/   # Large transcripts
├── 01_Drills/          # Practice drills
├── 02_Practice_Logs/   # Practice history
├── 10_Mastery/         # Verified knowledge
└── 90_Archive/         # Deprecated content
```

## Status

- [x] Step A: Scaffold + init-vault
- [ ] Step B: ingest + create-drill
- [ ] Step C: next + mark (trainer loop)
- [ ] Step D: LLM distill
- [ ] Step E: Polish
