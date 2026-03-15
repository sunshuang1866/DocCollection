---
name: codebase-visualizer
description: Analyzes a code project and generates a self-contained interactive HTML page that explains technical architecture, component communication, and third-party service dependencies in plain language for non-technical readers. Produces layered architecture diagrams, chat-metaphor service communication flows, and a SaaS toolbox section—all using everyday analogies and conversational language. Use when a developer wants to create an accessible project overview for non-programmers, showcase how system components interact, or produce educational visualizations after completing a project. Don't use for generating developer-facing API references, technical code documentation, unit test generation, or changelogs.
---

# Codebase Visualizer

Generates a single self-contained interactive HTML page that lets non-technical readers explore how a code project works—what parts exist, how they talk to each other, and what outside tools they rely on.

## Procedures

**Step 1: Locate and validate the project root**

1. If the user provided a directory path, use it. Otherwise, use the current working directory.
2. Execute `python3 scripts/detect-project-root.py <directory>` to confirm the directory contains a recognizable project and to identify the tech ecosystem.
3. If the script exits with an error, ask the user to confirm the correct project root before proceeding.
4. Note the detected `ecosystems` and `infra` files from the script output for use in Step 2.

**Step 2: Analyze the codebase**

1. Read `references/codebase-analysis-guide.md` to understand the full analysis methodology.
2. Scan the project using the following sequence:
   - Read manifest files (`package.json`, `requirements.txt`, `go.mod`, `docker-compose.yml`, etc.) to extract dependencies and service definitions.
   - Glob for entry-point files: `**/main.*`, `**/index.*`, `**/app.*`, `**/server.*` (exclude `node_modules`, `.git`, `dist`, `build`).
   - Glob for structural directories: `routes/`, `controllers/`, `services/`, `models/`, `components/`, `pages/`, `workers/`.
   - Search for third-party service indicators: API keys in `.env.example`, import statements matching known service SDKs.
3. Synthesize findings into four data structures (keep in working memory):
   - **Layer Map**: 3–5 named architecture layers, each containing a list of component names.
   - **Scenario List**: top 3–5 user-facing interaction scenarios with step-by-step communication chains.
   - **Service Registry**: list of third-party services with name, category, plain-language role, and inter-service connections.
   - **Glossary**: all technical terms found, each paired with a plain-language analogy.

**Step 3: Draft plain-language content**

1. For each item in the Layer Map, write a parenthetical everyday analogy for the layer name. Example: "API Layer (the front desk that takes your order)".
2. For each scenario in the Scenario List, rewrite every step using plain verbs: replace "sends HTTP request" with "asks", "queries the database" with "looks up in the notebook", "publishes an event" with "posts a message in the group chat".
3. For each service in the Service Registry, write a one-sentence plain-language role. No jargon without a tooltip definition.
4. Flag any component or service name that has no plain-language equivalent—add it to the Glossary with a creative analogy.

**Step 4: Generate the interactive HTML page**

1. Read `references/html-output-spec.md` to apply all layout, color, language, and interaction requirements.
2. Construct a single `.html` file with all CSS and JavaScript inlined (no external URLs). Structure:
   ```
   <html>
     <head> — inlined styles, dark/light theme toggle logic </head>
     <body>
       Section 1: Hero — project name, one-sentence plain-language summary, dark/light toggle button
       Section 2: 🏗️ Architecture Layers — stacked colored bands with component cards
       Section 3: 💬 How They Talk — chat-bubble scenarios with avatar icons
       Section 4: 🧰 SaaS Toolbox — service cards grouped by category with relationship lines
       Section 5: 📖 Glossary — expandable term list with analogies
     </body>
   </html>
   ```
3. Implement interactivity using vanilla JavaScript only:
   - Clicking a component card in Section 2 highlights connected service cards in Section 4.
   - Hovering over a technical term shows a tooltip from the Glossary.
   - Dark/light mode toggle persists via `localStorage`.
   - Scroll-triggered fade-in animation on each card (CSS `@keyframes`, no JS animation libraries).
4. Save the output as `codebase-overview.html` in the project root.
5. Confirm the file path to the user with a brief summary of what was detected (number of layers, scenarios, and services).

## Error Handling

- If `scripts/detect-project-root.py` fails: ask the user to confirm the project directory, then re-run with the corrected path.
- If fewer than 2 architecture layers can be identified: default to a two-layer structure ("Frontend / Backend") and note the uncertainty to the user.
- If no third-party services are detected: omit Section 4 from the output and add a note: "No external services detected — this project runs entirely on its own."
- If the project is a monorepo with multiple sub-projects: ask the user which sub-project to visualize before proceeding.
- If any glob or file read returns no results for structural directories: widen the search to any file containing `router`, `controller`, `service`, or `model` in its name.
