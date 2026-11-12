---
name: "architecture-diagram"
description: "Draw clean architecture or data-flow diagrams in Mermaid: right-angle lines, every node and edge labeled, legend inside, checked by eye."
---

System Architecture Diagram Skill. Concise, Deliberate, Professional. Mermaid, rendered to SVG, under strict rules.

- **Right angles only.** Render with Mermaid's ELK layout and straight segments: config `"layout": "elk"`, `"flowchart": { "curve": "linear", "htmlLabels": false }`, using a pinned Mermaid CLI that bundles ELK (11.14+). Never ship the default curved layout.
- **Top to bottom, in layers.** `flowchart TB`, with things laid out in the order data moves through them. Group by boundary (e.g. trust zones) in subgraphs.
- **Split a shared store by direction of flow.** A store that many nodes read and write pulls every edge back up the page. Draw the part written upstream and the part written downstream as two subgraphs, each named for the store, so every edge still runs downward.
- **One C4 level per diagram.** Name the level in the title (context, container or component) and keep every node at that level. Go one level down in a separate diagram.
- **As small as possible while comprehensive and accurate.** Every real component and flow, nothing decorative. Split into an overview plus focused diagrams only when one diagram can't stay readable.
- **Everything labeled, briefly.** Every edge reads `what | format | cadence | auth` (omit what doesn't apply; keep the label in quotes so the pipes are literal). Node: name, then type and technology, then one key fact (`Desk app`, `Container: FastAPI, DuckDB`, `serves the map`).
- **One meaning per shape, colour and line style,** the same in every diagram. Solid = automated, dotted = manual.
- **Legend inside the diagram:** a `direction LR` subgraph of sample nodes and edges, placed at the bottom with `lastNode ~~~ Legend`.
- **Titles above lines:** Mermaid paints edges over subgraph titles, so move the `cluster-label` groups to the end of the SVG and give their text a white halo.
- **Look before you ship.** Render to SVG, screenshot it, and remove every crossing or overlap that reordering could fix. Commit the `.mmd` source next to the SVG.
- **Draw what the code does,** not what the spec says.