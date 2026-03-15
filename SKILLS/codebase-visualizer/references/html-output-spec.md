# HTML Output Specification

The generated output must be a single, self-contained `.html` file with no external dependencies (all CSS and JS inlined).

## Required Sections

### 1. Architecture Layers Panel
- Render a visually stacked diagram showing 3–5 horizontal layers (e.g., "User Interface", "Business Logic", "Data Storage", "External Services").
- Each layer uses a distinct background color band.
- Components inside each layer are represented as labeled cards/bubbles.
- Clicking a card highlights all arrows connecting to it.
- Layer labels appear vertically on the left margin.
- **Plain-language rule:** Every layer name must have a parenthetical everyday analogy in smaller text. Example: "Business Logic (the kitchen where orders get cooked)".

### 2. Component Communication Flow Panel
- Use a chat/messaging metaphor: render each service-to-service call as a speech bubble conversation between two labeled "avatars" (simple colored circles with initials).
- Show the top 3–5 most important interaction scenarios, ranked by criticality.
- Each scenario has a title (e.g., "When a user logs in") and a numbered step-by-step chat thread.
- Technical terms (HTTP, REST, queue, event) must be replaced or annotated with a plain-language tooltip on hover.
- A glossary icon (?) beside each technical term opens a small inline tooltip with an analogy.

### 3. SaaS Toolbox Panel
- List every detected third-party service/library in card format.
- Each card contains: service logo placeholder (colored circle with initials), service name, one-line plain-language role description, and a "connects to" tag linking to other cards.
- Cards are grouped by category: "Storage", "Auth", "Messaging", "AI/ML", "Payments", "Other".
- A relationship diagram (simple lines between cards) shows inter-service dependencies.

## Visual Style Rules
- Dark-mode default with a toggle button (light/dark).
- Font: system-ui stack (no external font loads).
- Color palette: deep navy background (#0f172a), card background (#1e293b), accent colors per layer (teal, amber, rose, violet, emerald).
- All section headers use large emoji icons for visual anchoring.
- Animations: subtle fade-in on scroll for each card (CSS only, no JS libraries).
- Fully responsive: works on mobile viewport.

## Language Rules
- Zero jargon without explanation.
- Every technical concept explained on first appearance with a "like [everyday analogy]" parenthetical.
- Tone: friendly, curious, like explaining to a smart friend over coffee.
- Use "talks to", "sends a message to", "asks for", "stores in" instead of "calls", "requests", "writes to".
