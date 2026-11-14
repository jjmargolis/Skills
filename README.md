# Skills

Claude skills, one folder each. The copy saved in the Claude account is the one Claude uses; this repo is the version history.

| Skill | Purpose |
|---|---|
| [architecture-diagram](architecture-diagram/) | Architecture and data-flow diagrams in Mermaid under strict layout rules |
| [bpmn](bpmn-skills/bpmn/) | Business process diagrams in full BPMN 2.0.2, with the spec distilled in [spec.md](bpmn-skills/bpmn/spec.md) |
| [bpmn-light](bpmn-skills/bpmn-light/) | Business process diagrams in the small BPMN subset anyone can read |
| [bpmn-mermaid](bpmn-skills/bpmn-mermaid/) | BPMN-style process sketches in Mermaid, for GitHub and Copilot |
| [carovision](carovision/) | Typeset documents as a classic trade-book PDF (Times, Bodoni Bold) |
| [one-pager](one-pager/) | One-page PDF, with a chart, explaining one concept or comparing two things |
| [political-spectrum-heatmap](political-spectrum-heatmap/) | Sourced chart of where voter guides agree and disagree on a ballot |
| [voronoi-treemap](voronoi-treemap/) | Circular Voronoi treemap of a 2- or 3-level dataset: a disc of cells sized by value, grouped by colour and rim arcs |

The OMG BPMN 2.0.2 spec that `bpmn/spec.md` was distilled from is in [bpmn-skills/source/](bpmn-skills/source/). It is a source, not part of any skill.

Charts made with voronoi-treemap are in [charts/](charts/): 2026 midterm donors, FY2025 federal outlays and holders of the federal debt. Each folder holds the data CSV, the PNG and SVG, and `proof.md`, which reconciles the data to its published total and records the measured area error.

Packaged copies of carovision and one-pager, ready to upload to the Claude account, are in [dist/](dist/).
