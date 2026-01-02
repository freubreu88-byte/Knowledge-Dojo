# Quick Reference: LLM Prompting

> **Last Updated:** 2026-01-02
> **Sources:** 2 Mastery Notes

## ⚡ Essential Commands
| Command | Action | Context |
| :--- | :--- | :--- |
| "Prioritize speed" | Request fast/concise code | Prototyping |
| "Prioritize thoroughness" | Request detailed/robust code | Production preparation |

## 🛠️ Common Snippets

### Control Response Depth
```prompt
"Implement a [Task]. Prioritize completeness and detail over response speed. Include iterative solutions and time complexity analysis."
```

### Metadata Enhancement
```prompt
"I need to enhance the metadata for a [Video Title]. Please generate an engaging description with relevant hashtags and 10-15 discoverability tags."
```

## ⚠️ Pitfalls & Gotchas
- ❌ **Don't:** Accept shallow LLM responses for complex architectural tasks without asking for thoroughness.
- ✅ **Do:** Provide specific context (e.g., atmosphere, target audience) when generating marketing or metadata content.

## 🧠 Core Concepts (One-Liners)
- **Response Depth Control:** Explicitly instructing the LLM to 'think fast or slow' based on current needs.
- **Metadata Optimization:** Using LLMs to transform minimal context into SEO-friendly descriptions and tags.

## 🔗 Related Drills
- [[DRILL__control-llm-response-depth-for-coding-tasks.md]]
- [[DRILL__generate-enhanced-video-metadata-with-an-llm.md]]
- [[MASTERY__control-llm-response-depth-for-coding-tasks.md]]
- [[MASTERY__generate-enhanced-video-metadata-with-an-llm.md]]

---
*Auto-generated from Mastery Notes*
