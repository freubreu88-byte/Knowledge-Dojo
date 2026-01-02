---
type: mastery
source_drill_id: 01KDZ5T3NWG3M1RMXMS9GS2DV3
topics: ['LLM Prompting', 'Code Generation', 'Performance Optimization', 'Workflow Integration']
verified_at: 2026-01-02T13:14:47.954962
---

# Control Llm Response Depth For Coding Tasks

## 💡 Concept Definition
- Provide a coding task to an LLM.
- Explicitly instruct the LLM to prioritize either 'speed/conciseness' or 'thoroughness/detail' in its response.
- Compare the output and (simulated) latency for tasks with different prioritization instructions.
- Reflect on the trade-offs between speed and detail in LLM-assisted development.

## 🎯 When to Use
- **Primary Use Case:** [Identify when this pattern is the most effective solution]
- **Constraints:** [When is this NOT the right tool?]

## 💻 Minimal Working Example
```prompt
// Prompt 1 (Fast & Concise)
"Implement a simple Python function to calculate the Nth Fibonacci number using recursion. Prioritize speed of response and conciseness, provide only the necessary code."

// Prompt 2 (Thorough & Detailed)
"Implement a Python function to calculate the Nth Fibonacci number. Provide a thorough and detailed response, including:
1.  The recursive solution.
2.  An iterative solution (for comparison).
3.  An explanation of the time and space complexity for both.
4.  Considerations for large N values (e.g., memoization or dynamic programming concept).
5.  Example usage.
Prioritize completeness and detail over response speed."
```

## ⚠️ Pitfalls & Gotchas
- Common pitfall 1
- Common pitfall 2

## 🛠️ Verification Protocol
**Goal:** Practice prompting an LLM to generate code solutions that are either fast and concise or detailed and explanatory, based on explicit instructions, simulating the 'think fast or slow' capability.

**Steps:**
1. Choose a common, moderately complex coding task (e.g., 'Implement a simple REST API endpoint for user management' or 'Write a Python script to parse CSV data').
2. First, prompt a capable LLM (like Gemini 3 Pro, Claude, or GPT-4/5) for the task, explicitly requesting a 'fast and concise' solution, focusing only on the code. Note the (simulated) generation time.
3. Next, prompt the *same LLM* for the *same task*, but this time explicitly request a 'thorough and detailed' solution, including explanations, best practices, and error handling. Note the (simulated) generation time.
4. Compare the two responses: evaluate the difference in code verbosity, explanation depth, and observed generation speed.
5. Reflect on when each type of response would be most beneficial in a real-world development workflow (as discussed at 11:17).

## 🔗 Knowledge Graph
- **Related Topics:** [[LLM Prompting]], [[Code Generation]], [[Performance Optimization]], [[Workflow Integration]]
- **Proof:** [[DRILL__control-llm-response-depth-for-coding-tasks.md]]
- **Harder Variation:** - Try variation 1
- Try variation 2

---
*Automatically promoted on 2026-01-02*
