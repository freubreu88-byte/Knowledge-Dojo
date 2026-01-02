---
created: 2026-01-02 11:59:46.492565
id: 01KDZ5T3NWG3M1RMXMS9GS2DV3
next_review: '2026-01-09'
prereqs: []
review_count: 1
source_id: 01KDZ5S2Y8EJZ7GGJVMF3SGP85
status: passed
timebox_min: 15
topics:
- LLM Prompting
- Code Generation
- Performance Optimization
- Workflow Integration
type: drill
---

# Control LLM Response Depth for Coding Tasks

## Pattern
- Provide a coding task to an LLM.
- Explicitly instruct the LLM to prioritize either 'speed/conciseness' or 'thoroughness/detail' in its response.
- Compare the output and (simulated) latency for tasks with different prioritization instructions.
- Reflect on the trade-offs between speed and detail in LLM-assisted development.

## Drill
**Goal:** Practice prompting an LLM to generate code solutions that are either fast and concise or detailed and explanatory, based on explicit instructions, simulating the 'think fast or slow' capability.

**Steps:**
1. Choose a common, moderately complex coding task (e.g., 'Implement a simple REST API endpoint for user management' or 'Write a Python script to parse CSV data').
2. First, prompt a capable LLM (like Gemini 3 Pro, Claude, or GPT-4/5) for the task, explicitly requesting a 'fast and concise' solution, focusing only on the code. Note the (simulated) generation time.
3. Next, prompt the *same LLM* for the *same task*, but this time explicitly request a 'thorough and detailed' solution, including explanations, best practices, and error handling. Note the (simulated) generation time.
4. Compare the two responses: evaluate the difference in code verbosity, explanation depth, and observed generation speed.
5. Reflect on when each type of response would be most beneficial in a real-world development workflow (as discussed at 11:17).

## Snippet
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

## Validation
- [ ] The 'fast and concise' response primarily contains code and minimal explanation.
- [ ] The 'thorough and detailed' response includes extensive comments, explanations, and potentially more robust error handling or examples.
- [ ] You observe a noticeable difference in the generation speed between the two prompts (even if simulated, acknowledging the 'think fast or slow' feature at 10:38, 10:51).
- [ ] Both responses provide a functional solution to the coding task.
- [ ] You can articulate scenarios where each response style would be preferred for different parts of your workflow.

## Failure Modes
- Common pitfall 1
- Common pitfall 2

## Next Variation
- Try variation 1
- Try variation 2
