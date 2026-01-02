---
type: mastery
source_drill_id: 01KDXNVEYQHE1XSN7NYP6GAZD9
topics: ['claude-code', 'automation', 'productivity']
verified_at: 2026-01-01T22:04:21.758402
---

# Automate Multi Task Workflows

## 💡 Concept Definition
shift tab works wonders

## 🎯 When to Use
- **Primary Use Case:** [Identify when this pattern is the most effective solution]
- **Constraints:** [When is this NOT the right tool?]

## 💻 Minimal Working Example
```prompt
[Shift+Tab]
Create unit tests for @auth-service.ts using Vitest.
Generate a detailed README.md for the /services folder explaining the architecture.
```

## ⚠️ Pitfalls & Gotchas
- Common pitfall 1
- Common pitfall 2

## 🛠️ Verification Protocol
**Goal:** Queue multiple documentation and testing tasks to run fully unattended

**Steps:**
1. Toggle Auto-Accept mode by pressing 'Shift + Tab' (verify 'accept Edits on' appears)
2. Enter a prompt to generate unit tests for a specific file
3. Immediately enter a second prompt to generate a README.md for the current directory
4. Observe Claude adding the second task to the 'Message Queue'
5. Wait for both tasks to complete without pressing any confirmation buttons

## 🔗 Knowledge Graph
- **Related Topics:** [[claude-code]], [[automation]], [[productivity]]
- **Proof:** [[DRILL__automate-multi-task-workflows.md]]
- **Harder Variation:** - Try variation 1
- Try variation 2

---
*Automatically promoted on 2026-01-01*
