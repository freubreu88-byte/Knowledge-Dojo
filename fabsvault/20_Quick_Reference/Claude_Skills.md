# Quick Reference: Claude Skills

> **Last Updated:** 2026-01-02
> **Sources:** 2 Mastery Notes

## ⚡ Essential Commands
| Command | Action | Context |
| :--- | :--- | :--- |
| `/plugin install marketplace` | Install Claude marketplace | Claude environment |
| `/plugin install [skill-name]` | Install specific skill | Marketplace interaction |

## 🛠️ Common Snippets

### Domain Name Brainstormer
```prompt
Based on this project, can you use the domain name brainstormer skill to basically help me to brainstorm the right domain name for this project?
```

### Custom Code Review Skill Creation
```prompt
Using the skill creator skill, please create a code review skill based on the research file 'research.md' that we have done.
```

## ⚠️ Pitfalls & Gotchas
- ❌ **Don't:** Forget to restart your Claude session after adding a local skill manually.
- ✅ **Do:** Organize custom skills in a `skills/` directory within your project root.

## 🧠 Core Concepts (One-Liners)
- **Claude Skills:** Modular AI capabilities that can be installed or define custom workflows.
- **Skill Creator:** A meta-skill that converts research docs into actionable Claude skills.
- **Local Integration:** Skills can be added locally via a `skill.md` file in a project folder.

## 🔗 Related Drills
- [[DRILL__brainstorm-domain-names-with-claudes-domain-name-brainstormer-skill.md]]
- [[DRILL__create-a-custom-code-review-skill-with-claudes-skill-creator.md]]
- [[MASTERY__brainstorm-domain-names-with-claudes-domain-name-brainstormer-skill.md]]
- [[MASTERY__create-a-custom-code-review-skill-with-claudes-skill-creator.md]]

---
*Auto-generated from Mastery Notes*
