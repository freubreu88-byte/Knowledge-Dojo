# Knowledge-Dojo 🥋
> **Stop collecting notes. Start building reflexes.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Built for Obsidian](https://img.shields.io/badge/Built%20for-Obsidian-purple.svg)](https://obsidian.md/)

## 🌊 The Vision: Kill the "Collector's Fallacy"

Most "Second Brain" systems are digital graveyards. We bookmark, we highlights, and we archive—but we rarely **learn**. Knowledge-Dojo transforms your static Obsidian vault into a **dynamic gym for your mind**.

Knowledge-Dojo is a **Trainer-First** learning system. It doesn't just store information; it distills it into active challenges (Drills) and forces you to perform before it grants you "Mastery."

---

## ✨ Key Features

- **⚡ Instant Ingestion**: Feed the Dojo a YouTube URL, a blog post, or a Reddit thread. It extracts the core insights automatically.
- **🧠 AI Distillation**: Powered by Gemini, the Dojo transforms raw content into atomic, high-signal Drills.
- **🔄 Performance-Based Repetition**: Your "Practice" loop is driven by your success rate. Concepts you struggle with appear more often; mastered ones fade into your permanent knowledge base.
- **📊 Automatic Topic Indexing (MOCs)**: The Dojo automatically clusters your knowledge into Topics, showing you a real-time "Pass Rate" for every skill tree.
- **🤖 Agent-Native Workflow**: Specifically designed to work alongside AI Agents. Ask your agent to "generate a cheat sheet" from your mastery notes, and watch it happen.

---

## 🛠️ Getting Started

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/freubreu88-byte/Knowledge-Dojo.git
cd Knowledge-Dojo

# 2. Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Unix/macOS

# 3. Install dependencies
pip install -e ".[dev]"
```

### Usage

```bash
# Initialize your first vault
dojo init-vault ./my-vault

# Capture a new source (YouTube, Blog, etc.)
dojo capture https://www.youtube.com/watch?v=example

# Distill your inbox into active drills
dojo distill-inbox

# Start your daily practice session
dojo next
```

---

## 🏗️ The Dojo Architecture

A Knowledge-Dojo vault is organized to move information from **Raw** to **Reflex**:

1.  **00_Inbox**: Raw capture and transcripts.
2.  **01_Drills**: Atomic AI-generated challenges.
3.  **02_Practice_Logs**: Your performance history.
4.  **10_Mastery**: Verified knowledge (Promoted only after passing drills).
5.  **11_Topics**: Automated MOCs (Maps of Content) tracking your progress per topic.
6.  **20_Quick_Reference**: Agent-generated cheat sheets and guides.

---

## 🚀 Why Knowledge-Dojo?

The market is flooded with "Note Taking" apps. Knowledge-Dojo is a **"Note Doing"** app. It’s for developers, researchers, and lifelong learners who want to move past passive consumption into actual expertise.

**Become the master of your own knowledge. Enter the Dojo.**

---

## 🤝 Contributing

We welcome contributions! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
