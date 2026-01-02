---
id: 01KDZ5DTJNQYMED2P313FNQD5E
type: drill
status: untried
created: 2026-01-02T11:53:03.957474
source_id: 01KDZ5CN2FNRKJSVEW715XBFV5
next_review: 2026-01-02
review_count: 0
timebox_min: 15
topics: ['UI Development', 'Responsive Design', 'AI Code Generation']
prereqs: []
---

# AI-Powered Responsive Navigation Bar & Content Section

## Pattern
- Using a single, clear prompt to guide an AI model in generating complex, responsive UI components.
- Iterating on the generated code to refine design and functionality.
- Prioritizing component-driven architecture over plain text.

## Drill
**Goal:** Generate a responsive navigation bar and a feature section for a website using an AI model, demonstrating its UI generation capabilities.

**Steps:**
1. Choose your preferred AI coding assistant (e.g., Cursor, GitHub Copilot Chat, ChatGPT with code interpreter, or similar).
2. Provide a prompt requesting a modern, responsive navigation bar with specific links (e.g., Home, Features, Pricing, Contact) and a mobile menu toggle (See 03:39).
3. Follow up with a prompt to create a 'Hero Section' or 'Feature Section' that includes a title, a brief description, an image placeholder, and a call-to-action button, ensuring it's component-driven (See 04:41).
4. Copy the generated HTML/CSS/JS into a local `index.html` file and save it.
5. Open the `index.html` in your browser and test its responsiveness by resizing the window from desktop to mobile width.
6. (Optional) Ask the AI to refine the styling (e.g., color scheme, font choices) or add a simple hover effect to navigation links (See 04:23).

## Snippet
```prompt
Create a modern, responsive navigation bar for a web application. It should include links for 'Home', 'Features', 'Pricing', and 'Contact'. Ensure it has a hamburger menu for mobile views that toggles navigation visibility. Use Tailwind CSS for styling if possible, otherwise plain CSS.

Next, create a 'Hero Section' directly below the navigation. This section should include a large, engaging title, a concise subtitle explaining the app's value, a placeholder for an image or animation on one side, and a prominent call-to-action button (e.g., 'Get Started'). Make sure the layout is responsive and visually appealing and component-driven.
```

## Validation
- [ ] [ ] The generated navigation bar appears correctly with all specified links on a desktop view.
- [ ] [ ] The navigation bar includes a functional mobile menu toggle (e.g., hamburger icon) that reveals/hides links when the browser window is resized to a mobile width.
- [ ] [ ] The feature section displays a clear title, description, and button, with a responsive layout.
- [ ] [ ] The overall generated code structure reflects a component-driven approach rather than a monolithic block of text-heavy HTML.

## Failure Modes
- Common pitfall 1
- Common pitfall 2

## Next Variation
- Try variation 1
- Try variation 2
