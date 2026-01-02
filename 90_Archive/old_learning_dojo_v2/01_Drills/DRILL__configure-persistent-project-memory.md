---
created: 2026-01-01 22:01:39.158465
id: 01KDXNVEYPF44RHSTX2JY1PZDZ
next_review: '2026-01-08'
prereqs: []
review_count: 1
source_id: 01KDXNTGVMFV48AEW859NA7T76
status: passed
timebox_min: 10
topics:
- claude-code
- configuration
- project-management
type: drill
---

# Configure Persistent Project Memory

## Pattern
- CLAUDE.md acts as a long-term memory and rule set for your project
- Claude automatically loads this configuration at the start of every session
- Rules can be added manually or by asking Claude to update its own memory

## Drill
**Goal:** Create a CLAUDE.md file that enforces specific coding standards and project structure

**Steps:**
1. Create a file named 'CLAUDE.md' in your project root
2. Add a section for 'Coding Standards' (e.g., 'Use functional components', 'Prefer Tailwind for styling')
3. Launch Claude Code in the terminal
4. Ask Claude to generate a new component and observe if it follows the rules in CLAUDE.md
5. Prompt Claude to 'Add a rule to CLAUDE.md that all utility functions must have JSDoc' and verify the file update

## Snippet
```code
# CLAUDE.md

## Project Context
This is a React/TypeScript weather dashboard.

## Coding Standards
- Use Arrow Functions for all components
- Use lucide-react for icons
- Strictly use TypeScript interfaces instead of types

## Commands
- Build: npm run build
- Test: npm test
```

## Validation
- [ ] CLAUDE.md file exists in root directory
- [ ] Claude references the file when starting a session
- [ ] Generated code adheres to the defined standards
- [ ] New rules are successfully appended to the file via prompt

## Failure Modes
- Common pitfall 1
- Common pitfall 2

## Next Variation
- Try variation 1
- Try variation 2
