---
created: 2026-01-02 13:07:31.053714
id: 01KDZ9P4ZD5PHXKZXGAHHFFZZA
next_review: '2026-01-09'
prereqs: []
review_count: 1
source_id: 01KDZ88G6ZWHXK367H6888PJRH
status: passed
timebox_min: 10
topics:
- Project Planning
- Domain Names
- Claude Skills
- Business Strategy
type: drill
---

# Brainstorm Domain Names with Claude's Domain Name Brainstormer Skill

## Pattern
- Utilize Claude Skills to generate creative and relevant suggestions for project naming.
- Discover how to integrate custom skills by manually adding skill folders to a Claude project.
- Evaluate AI-generated suggestions based on criteria like availability, target audience, and key features.

## Drill
**Goal:** Generate a list of suitable and available domain names for a hypothetical project using the Domain Name Brainstormer skill, complete with rankings and justifications.

**Steps:**
1. Download the 'domain name brainstormer' skill folder (as described around 09:32).
2. Add the downloaded skill folder to your Claude project's 'skills' directory (see 09:41).
3. Restart your Claude session to ensure the new skill is recognized (see 09:52).
4. Prompt Claude to brainstorm domain names for your project, providing a brief description of the project (see 09:56).
5. Review the generated domain name suggestions, their availability, and the rationale provided by Claude (see 11:51).

## Snippet
```prompt
# Assumes the 'domain name brainstormer' skill folder has been added to your Claude project's skills directory and your Claude session has been restarted.
# Replace 'this project' with a concise description of your project (e.g., 'a new bookkeeping application that tracks receipts and bank statements').
Based on this project, can you use the domain name brainstormer skill to basically help me to brainstorm the right domain name for this project?
```

## Validation
- [ ] Claude successfully triggers the 'domain name brainstormer' skill (see 10:07).
- [ ] A list of domain name suggestions is provided (see 11:56).
- [ ] Suggestions include different domain extensions (.AI, .com, .io) (see 12:00).
- [ ] Each suggestion is accompanied by an availability status and a brief explanation of its suitability (see 12:08).
- [ ] The output includes a link to real-time results for availability (see 12:10).

## Failure Modes
- Common pitfall 1
- Common pitfall 2

## Next Variation
- Try variation 1
- Try variation 2
