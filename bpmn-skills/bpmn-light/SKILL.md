---
name: "bpmn-light"
description: "Draw a business process in BPMN light: the small standard subset anyone can read, from BPMN XML, right-angle flows, linted and checked by eye."
---

BPMN Process Diagram Skill, light notation. Concise, Deliberate, Readable. BPMN 2.0 XML, rendered to SVG, under strict rules. Light means the Descriptive conformance sub-class of BPMN 2.0.2 (Table 2.1): valid BPMN that a reader needs no training for.

- **The palette, and nothing else.** Pool, lane. Task, user task, service task, sub-process, call activity. Exclusive (X) and parallel (+) gateways. Start events: plain, message, timer. End events: plain, message, terminate. Sequence flow, message flow. Data object, data store, text annotation, group, association. If the process needs anything more, use the full `bpmn` skill instead of bending these.
- **Real BPMN, not a lookalike.** Write a `.bpmn` file (model plus `BPMNDiagram`) and render it with bpmn-js: `npm i bpmn-js bpmnlint`, then `node render.cjs x.bpmn`. Never draw BPMN shapes in Mermaid or by hand in SVG.
- **Pools are participants, lanes are roles.** One pool for the organisation, with outside parties as empty black-box pools. Sequence flow never leaves a pool; only message flow crosses, and never inside one pool.
- **Left to right, on a grid.** Happy path on one straight row; alternatives drop below it. Tasks 100×80, events 36×36, gateways 50×50, about 150 between centres, pool name band 30 wide, lanes at least 120 tall. Stack pools vertically so message flows run straight up and down.
- **Right angles only.** You place every `dc:Bounds` and `di:waypoint` yourself, and each pair of consecutive waypoints shares an x or a y.
- **One page, 7 to 15 tasks.** Fewer steps at a higher level beats a wall of boxes. Push detail into a call activity that points to its own diagram.
- **Everything labeled, briefly.** Tasks: verb plus object. Events: the state reached ("Order received"). Exclusive splits: a question, with every outgoing flow labeled as an answer. Message flows: the message. Give each event, gateway and flow label its own bounds so it sits clear of the lines.
- **Honest flow.** Every path runs from a start event to an end event. X splits to one path and merges without waiting; + splits to all paths and waits for all. Close each split with the same gateway type. Always draw the X in an exclusive gateway (`isMarkerVisible="true"`).
- **Lint clean.** List `<incoming>` and `<outgoing>` on every flow node, then run `npx bpmnlint x.bpmn` with `{"extends": "bpmnlint:recommended"}` in `.bpmnlintrc`. Zero errors, and no warnings from the renderer.
- **Look before you ship.** Open the PNG and remove every crossing, overlap and clipped label that moving a shape could fix. Commit the `.bpmn` source next to the SVG.
- **Draw what happens,** not what the policy says.
