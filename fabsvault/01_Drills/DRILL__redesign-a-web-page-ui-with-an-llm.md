---
id: 01KDZ5T3NS10S4TBFKYXNSYVDZ
type: drill
status: untried
created: 2026-01-02T11:59:46.489955
source_id: 01KDZ5S2Y8EJZ7GGJVMF3SGP85
next_review: 2026-01-02
review_count: 0
timebox_min: 15
topics: ['UI/UX Design', 'LLM Prompting', 'Web Development', 'Responsive Design']
prereqs: []
---

# Redesign a Web Page UI with an LLM

## Pattern
- Provide an LLM with the current state of a simple web page (e.g., HTML structure, description of issues).
- Instruct the LLM to completely redesign the page, focusing on modern, component-driven UI.
- Emphasize responsiveness across devices (desktop, mobile).
- Request unique, non-AI-driven component designs.

## Drill
**Goal:** Use an AI model to generate a complete, responsive, and visually appealing redesign for a given web page's UI.

**Steps:**
1. Select a simple existing web page (e.g., a personal project, a basic template, or even the provided 'old ViewCreator' description from the content).
2. Identify key areas for improvement in its UI, such as plain design, poor responsiveness, or lack of engaging components.
3. Craft a prompt for a capable LLM (like Gemini 3 Pro, Claude Opus/Sonnet, or GPT-4/5) asking for a complete UI redesign. Include details about the current page's purpose and the desired modern aesthetic.
4. Specifically request component-driven design, animations, and full responsiveness (e.g., a 'fantastic mobile menu' as mentioned at 03:55).
5. Implement the generated HTML/CSS code locally and review the changes.

## Snippet
```prompt
I need a complete UI redesign for a simple marketing landing page for a SaaS product called 'ViewCreator'. The current page is very plain, text-heavy, and has issues with responsiveness, especially on mobile. It looks 'AI-typical' and lacks engaging components.

**Current Page Description:**
- Header: Logo, Home, Features, Pricing, Contact links.
- Hero Section: Large title 'Grow Your Social Media', a simple slider for images, a 'Get Started' button.
- Features Section: Lists features with bullet points, text-heavy.
- Testimonials: Basic text quotes.
- Footer: Copyright info.

**Desired Redesign Goals:**
- Modern, component-driven design (e.g., interactive demos, engaging cards, like those shown at 03:19, 04:41).
- Visually appealing, not generic or 'AI-driven.'
- Fully responsive, with a 'fantastic mobile menu' (03:58).
- Incorporate subtle animations or hover effects (03:32, 04:23).
- Improve the overall user experience and visual flow.

Please provide the HTML and CSS for the redesigned page. Focus on the main sections and provide placeholder content where necessary. Make sure the navbar is impressive and the mobile menu is fantastic.
```

## Validation
- [ ] The generated UI looks significantly different and more modern than the original.
- [ ] The page features new, unique components that don't appear generic or 'AI-driven.'
- [ ] The navigation bar (if applicable) is improved and functional, including a mobile menu.
- [ ] The page layout and elements adapt well when viewed on different screen sizes (responsive design).
- [ ] The overall design is visually appealing and enhances user experience.

## Failure Modes
- Common pitfall 1
- Common pitfall 2

## Next Variation
- Try variation 1
- Try variation 2
