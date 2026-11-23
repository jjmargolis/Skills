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
| [reading-packet](reading-packet/) | One PDF of excerpts from many sources, each sized to a time budget, with divider pages, source-page stamps and bookmarks |
| [voronoi-treemap](voronoi-treemap/) | Circular Voronoi treemap of a 2- or 3-level dataset: a disc of cells sized by value, grouped by colour and rim arcs |

`bpmn/spec.md` is distilled from the OMG BPMN 2.0.2 specification, available from [omg.org/spec/BPMN/2.0.2](https://www.omg.org/spec/BPMN/2.0.2/).

Charts made with voronoi-treemap are in [charts/](charts/): 2026 midterm donors, FY2025 federal outlays and holders of the federal debt. Each folder holds the data CSV, the PNG, SVG and PDF, and `proof.md`, which reconciles the data to its published total and records the measured area error. [charts/poster](charts/poster/) sets the federal outlays and debt charts on one A2 sheet as a print-ready vector PDF, with every source cited and linked; `poster.py` rebuilds it.

Packaged copies of carovision and one-pager, ready to upload to the Claude account, are in [dist/](dist/).

## License

Licensed under [CC BY 4.0](LICENSE): use, adapt and share anything here, including commercially, with credit to Jacob Margolis and a link to this repo.
