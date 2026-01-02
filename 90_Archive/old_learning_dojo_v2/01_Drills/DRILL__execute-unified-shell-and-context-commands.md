---
id: 01KDXNVEYQHE1XSN7NYP6GAZD8
type: drill
status: untried
created: 2026-01-01T22:01:39.159224
source_id: 01KDXNTGVMFV48AEW859NA7T76
next_review: 2026-01-01
review_count: 0
timebox_min: 5
topics: ['claude-code', 'cli-efficiency', 'context-management']
prereqs: []
---

# Execute Unified Shell and Context Commands

## Pattern
- Use '!' prefix to pass commands directly to the terminal without consuming excessive tokens
- Use '@' symbol to provide explicit file context and reduce search time
- Combine both to maintain a single-window developer workflow

## Drill
**Goal:** Run a local development server and refactor a specific file without leaving the Claude CLI

**Steps:**
1. Open Claude Code in an existing project
2. Run your development command using the bash prefix: '!npm run dev' (or equivalent)
3. While the server is running (or in a new Claude session), use the '@' symbol to select a specific file
4. Issue a refactor prompt targeting that specific file to save context tokens
5. Use '/model' to switch to 'sonnet' for faster, cheaper edits if the task is simple

## Snippet
```commands
!npm run dev
/model sonnet
Add error handling to @src/api/weather.ts using a try-catch block.
```

## Validation
- [ ] Bash command executes successfully via the '!' prefix
- [ ] Claude identifies the specific file linked via '@'
- [ ] Token usage is minimized by avoiding a full project scan
- [ ] Server remains running or accessible within the workflow

## Failure Modes
- Common pitfall 1
- Common pitfall 2

## Next Variation
- Try variation 1
- Try variation 2
