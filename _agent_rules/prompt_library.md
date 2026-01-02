# quick copy for the user: for my vault, run @agent_master.md for the folder @fabsvault 

# 🎯 Vibe-Dojo: Agent Prompt Library

Copy and paste these prompts into your AI Assistant (Antigravity/Claude) to trigger smart workflows.

---

## ⚡ Master Cheat-Sheet Update
Use this when you want to refresh your knowledge reference.

**Prompt:**
> You are the **Vibe-Dojo Sensei**. Your task is to update or create a Cheat Sheet for a specific topic.
> 
> **1. Target Dojo:** `[FOLDER_PATH]` (e.g., C:/Users/Fabian/Desktop/AI Projekte/Lernplattform)
> **2. Topic:** `[TOPIC_NAME]` (e.g., Cursor, Git, React)
> 
> **Instructions:**
> - First, read the **Governance Rules** in `[FOLDER_PATH]/_agent_rules/cheatsheet_rules.md`.
> - Then, follow the **Workflow** defined there to extract data from `10_Mastery/` and update `20_Quick_Reference/`.
> - Ensure you replace all placeholders in the `_templates/cheatsheet_template.md`.
> - Do not guess commands; only use verified knowledge from the vault.
> 
> Proceed with updating the `[TOPIC_NAME]` reference now.

---

## 🧠 Knowledge Consolidation
Use this when you have several notes on one topic and want to merge them.

**Prompt:**
> I need to consolidate my knowledge on `[TOPIC]`.
> 
> **Dojo Path:** `[FOLDER_PATH]`
> 
> **Instructions:**
> 1. Scan `10_Mastery/` for all notes related to `[TOPIC]`.
> 2. Analyze them for overlapping concepts, duplicates, or missing links.
> 3. Create a single, comprehensive **Mastery Note** that combines the best parts.
> 4. Ensure the new note is saved back to `10_Mastery/` with a high-quality structure.
> 5. Move the original smaller notes to `90_Archive/` once the master note is created.
> 
> Read the files first and propose the new structure before writing.

---

## 📎 Smart Cross-Linking
Use this to build the "Mental Map" of your Dojo.

**Prompt:**
> Act as a **Knowledge Architect** for my Vibe-Dojo at `[FOLDER_PATH]`.
> 
> **Task:** Analyze all files in `20_Quick_Reference/` and `11_Topics/`.
> 
> **Goal:** Create semantic links between them. If a cheat sheet mentions a concept that has its own topic or reference page, add a `[[Wiki-Link]]` in a "Related References" section at the bottom.
> 
> Give me a summary of the links you added.

---

## 🚀 How to use these prompts
1. **Open a new chat** or use your current session.
2. **Replace the bracketed variables** like `[FOLDER_PATH]` and `[TOPIC]`.
3. **Send the prompt**.
4. The Agent will use its file access to read your rules and execute the task perfectly.
