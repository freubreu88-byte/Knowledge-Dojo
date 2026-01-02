# Knowledge-Dojo 🥋
> **Stop collecting. Start building reflexes.**

Knowledge-Dojo is a **Trainer-First** learning system designed for Obsidian. It bridges the gap between *consuming* content (YouTube, Blogs, Reddit) and *mastering* it through AI-driven active recall and spaced repetition.
![Generated Image January 02, 2026 - 2_01PM](https://github.com/user-attachments/assets/973d8438-389b-4207-af87-9495a3c0cecc)
---

## 🚀 Quick Start: From Zero to Dojo

### 1. Installation
```bash
# Clone the repository
git clone https://github.com/freubreu88-byte/Knowledge-Dojo.git
cd Knowledge-Dojo

# Setup environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Unix/macOS

# Install package
pip install -e "."
```

### ⚡ Windows One-Click (Recommended)
If you are on Windows, you can simply run the included batch file:
- **`start_dojo.bat`**: This will automatically setup the environment, check for dependencies, and guide you through creating or opening a vault. It's the fastest way to get training.

### 2. Connect to Obsidian
Knowledge-Dojo lives inside your Obsidian vault.
1. Create a new folder in Obsidian (e.g., `MyBrain`).
2. Initialize the Dojo in that folder:
   ```bash
   dojo init-vault "C:\Path\To\Your\Vault"
   ```
3. Open Obsidian. You will see several new folders (Inbox, Drills, Mastery, etc.) and a `Home.md` dashboard.

### 3. Configure AI
Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your_key_here
```

---

## 🛠️ The Workflow: How to Train

Knowledge-Dojo follows a strict **"Raw → Challenge → Mastery"** pipeline.

### Step A: Capture (The Ingest)
Found a great YouTube video or article? Don't just bookmark it.
```bash
dojo capture https://www.youtube.com/watch?v=...
```
*This saves a lean source note in `00_Inbox` with the full transcript/content attached.*

### Step B: Distill (The Transformation)
Turn your raw notes into practice.
```bash
dojo distill-inbox
```
*The AI analyzes your inbox and creates atomic, high-signal Drills in `01_Drills`.*

### Step C: Practice (The Dojo Loop)
This is where the learning happens.
```bash
dojo next
```
*This starts an interactive session. The Dojo presents you with your most urgent drills based on your past performance.*

### Step D: Mastery
Once you consistently pass a drill, Knowledge-Dojo **promotes** that concept to `10_Mastery`.
* Your **Dashboard (`Home.md`)** and **Topics (`11_Topics`)** update automatically to show your expertise level.

---

## 📂 Vault Structure

| Folder | Purpose |
| :--- | :--- |
| `00_Inbox` | Raw captures and transcripts. Your "To-Process" list. |
| `01_Drills` | AI-generated challenges (Flashcards/Prompts). |
| `10_Mastery` | Your verified knowledge base. Concepts you have proven you know. |
| `11_Topics` | **Auto-generated Index**. Maps of Content showing pass-rates per topic. |
| `20_Quick_Reference` | Cheat sheets and high-density guides. |

---

## 🤖 Agentic Advantage
Knowledge-Dojo is built to be **AI-Native**. You can use agents (like Cursor, Claude, or Antigravity) to:
- *"Create a cheat sheet for Python decorators based on my Mastery notes."*
- *"Analyze my practice logs and tell me why I'm failing the Security drills."*

---

## 🤝 Community & Support
- **Issues**: Found a bug? Open an issue!
- **Discussions**: Want to share your learning workflow? Start a thread.

**Enter the Dojo. Level up your mind.**
