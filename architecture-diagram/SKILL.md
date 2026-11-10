---
name: "architecture-diagram"
description: "Draw clean architecture or data-flow diagrams in Mermaid: right-angle lines, every node and edge labeled, legend inside, checked by eye."
---

System Architecture Diagram Skill. Concise, Deliberate, Professional. Mermaid, rendered to SVG, under strict rules.

- **Right angles only.** Render with Mermaid's ELK layout and straight segments: config `"layout": "elk"`, `"flowchart": { "curve": "linear", "htmlLabels": false }`, using a pinned Mermaid CLI that bundles ELK (11.14+). Never ship the default curved layout.
- **Top to bottom, in layers.** `flowchart TB`, with things laid out in the order data moves through them. Group by boundary (e.g. trust zones) in subgraphs.
- **As small as possible while comprehensive and accurate.** Every real component and flow, nothing decorative. Split into an overview plus focused diagrams only when one diagram can't stay readable.
- **Everything labeled, briefly.** Every edge reads `what | format | cadence | auth` (omit what doesn't apply; keep the label in quotes so the pipes are literal). Node: name, then one key fact.
- **One meaning per shape, colour and line style,** the same in every diagram. Solid = automated, dotted = manual.
- **Legend inside the diagram:** a `direction LR` subgraph of sample nodes and edges, placed at the bottom with `lastNode ~~~ Legend`.
- **Titles above lines:** Mermaid paints edges over subgraph titles, so move the `cluster-label` groups to the end of the SVG and give their text a white halo.
- **Look before you ship.** Render to SVG, screenshot it, and remove every crossing or overlap that reordering could fix. Commit the `.mmd` source next to the SVG.
- **Draw what the code does,** not what the spec says.