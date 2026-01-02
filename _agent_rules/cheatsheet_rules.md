# Vibe-Dojo Agent Rules: Cheat Sheet Generation

**Purpose**: Guide AI Agents in creating Quick Reference Cheat Sheets from Mastery Notes.

## Trigger
Use when user says:
- "Update the [Topic] cheat sheet"
- "Create cheat sheet for [Topic]"
- "Refresh quick refs"

## Workflow

1. **Identify Topic**: Determine target (e.g., "Cursor", "Git", "React")

2. **Scan Source Material**:
   - Read all files in `10_Mastery/[Topic]/` (or search for `MASTERY__*.md` related to it)
   - Check frontmatter: `topics: [...]`

3. **Extract Content**:
   - **Commands**: Code blocks or inline code (backticks)
   - **Snippets**: "Minimal Example" sections
   - **Pitfalls**: "Failure Modes" or "Common Mistakes"
   - **Concepts**: "Definition" sections

4. **Validate Content**:
   - ✅ **Only include info from source files**
   - ❌ **Never invent or guess commands**
   - If uncertain, mark: `⚠️ [Item] - Verify`
   - If no sources exist:
     ```
     # Quick Reference: [Topic]
     > No mastery notes yet. Complete drills first!
     ```

5. **Deduplicate**:
   - No identical commands
   - Keep most descriptive version

6. **Format**:
   - Use template: `_templates/cheatsheet_template.md`
   - **Replace placeholders:**
     * `{{TOPIC}}` → actual name (e.g., "Cursor")
     * `{{DATE}}` → YYYY-MM-DD
     * `{{NUMBER_OF_MASTERY_NOTES}}` → count of source files
     * `{{LANGUAGE}}` → code language (e.g. bash, python)
   - Save as: `20_Quick_Reference/[Topic].md`
   - Update timestamp

## Style Guidelines
- **Concise**: Bullets, no paragraphs
- **Actionable**: "Run: `npm start`" not "You can run..."
- **Visual**: Use emojis (⚠️, ✅, 🔗)

## Handling Growth
- If >500 lines, suggest split (e.g., `Git_Basics.md`, `Git_Advanced.md`)
- Prefer single file unless clearly separable

## ⚠️ Do Not Modify
Never touch:
- `01_Drills/` (managed by CLI)
- `02_Practice_Logs/` (managed by CLI)
- `config.yaml` (system config)
- Files with `status:` frontmatter (drills)

Only write to: `20_Quick_Reference/`
