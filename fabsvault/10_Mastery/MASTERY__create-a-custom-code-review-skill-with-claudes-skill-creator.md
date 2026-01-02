---
type: mastery
source_drill_id: 01KDZ9P4ZE6MMDXJ0QZHK1TTGY
topics: ['Code Review', 'Custom AI Skills', 'Software Engineering', 'Claude Skills', 'Automation']
verified_at: 2026-01-02T13:14:54.224824
---

# Create A Custom Code Review Skill With Claudes Skill Creator

## 💡 Concept Definition
- Utilize a meta-skill (Skill Creator) to define and build new, custom Claude Skills.
- Automate the process of converting research and best practices into actionable AI skills.
- Structure a new skill to perform multi-faceted tasks, such as code reviews from various perspectives.

## 🎯 When to Use
- **Primary Use Case:** [Identify when this pattern is the most effective solution]
- **Constraints:** [When is this NOT the right tool?]

## 💻 Minimal Working Example
```prompt
# Step 1: Conduct deep research on code review best practices.
# This prompt will guide Claude to gather information and output it, ideally to a file like 'research.md'.
Perform a deep research on the best way to review code, including technical review, architecture patterns (especially for NestJS, React, TypeScript), multi-perspective reviews (architect, PM, QA, UX), code review methodologies (top-down, time allocation), documentation review, product/user experience focus, mobile experience, and usability. Conclude this research into a single MD file.

# Step 2: Use the Skill Creator to build a new skill based on the research.
# Assumes the research output from Step 1 is available as 'research.md' in the current context.
Using the skill creator skill, please create a code review skill based on the research file 'research.md' that we have done.
```

## ⚠️ Pitfalls & Gotchas
- Common pitfall 1
- Common pitfall 2

## 🛠️ Verification Protocol
**Goal:** Develop a new Claude Skill for automated code reviews, incorporating deep research on best practices and various review perspectives, using the Skill Creator skill.

**Steps:**
1. Prompt Claude to perform deep research on code review best practices (e.g., technical, architecture, multi-perspective, methodologies) and summarize it into an MD file (see 18:07 - 19:34).
2. Ensure the research output is saved as an accessible file (e.g., 'research.md') within your Claude session.
3. Prompt Claude to use the 'skill creator' skill to build a new code review skill based on the 'research.md' file (see 19:42).
4. Examine the newly created skill folder within your Claude project's 'skills' directory (see 20:09).
5. Review the generated `skill.md` file and other reference files to understand the structure and phases of the new code review skill (see 20:23).

## 🔗 Knowledge Graph
- **Related Topics:** [[Code Review]], [[Custom AI Skills]], [[Software Engineering]], [[Claude Skills]], [[Automation]]
- **Proof:** [[DRILL__create-a-custom-code-review-skill-with-claudes-skill-creator.md]]
- **Harder Variation:** - Try variation 1
- Try variation 2

---
*Automatically promoted on 2026-01-02*
