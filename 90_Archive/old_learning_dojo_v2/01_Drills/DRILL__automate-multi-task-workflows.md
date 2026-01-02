---
created: 2026-01-01 22:01:39.159889
id: 01KDXNVEYQHE1XSN7NYP6GAZD9
next_review: '2026-01-08'
prereqs: []
review_count: 1
source_id: 01KDXNTGVMFV48AEW859NA7T76
status: passed
timebox_min: 10
topics:
- claude-code
- automation
- productivity
type: drill
---

# Automate Multi-Task Workflows

## Pattern
- Auto-Accept Mode (Shift + Tab) bypasses manual confirmation for file edits
- The Message Queue allows stacking prompts to run sequentially while you are away
- Sequential execution prevents context collisions during complex refactors

## Drill
**Goal:** Queue multiple documentation and testing tasks to run fully unattended

**Steps:**
1. Toggle Auto-Accept mode by pressing 'Shift + Tab' (verify 'accept Edits on' appears)
2. Enter a prompt to generate unit tests for a specific file
3. Immediately enter a second prompt to generate a README.md for the current directory
4. Observe Claude adding the second task to the 'Message Queue'
5. Wait for both tasks to complete without pressing any confirmation buttons

## Snippet
```prompt
[Shift+Tab]
Create unit tests for @auth-service.ts using Vitest.
Generate a detailed README.md for the /services folder explaining the architecture.
```

## Validation
- [ ] Auto-Accept mode status is visible in the UI
- [ ] Second prompt is successfully added to the queue while the first is running
- [ ] Files are created/modified without manual 'Yes' confirmations
- [ ] Both tasks finish sequentially and correctly

## Failure Modes
- Common pitfall 1
- Common pitfall 2

## Next Variation
- Try variation 1
- Try variation 2
