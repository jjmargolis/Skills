---
name: "bpmn"
description: "Draw a business process in full BPMN 2.0.2: real notation from BPMN XML, right-angle flows, every element labeled, linted and checked by eye."
---

BPMN Process Diagram Skill, full notation. Concise, Deliberate, Standard. BPMN 2.0 XML, rendered to SVG, under strict rules. `spec.md` beside this file is the whole standard distilled; look a rule up there before you rely on it.

- **Real BPMN, not a lookalike.** Write a `.bpmn` file (model plus `BPMNDiagram`) and render it with bpmn-js: `npm i bpmn-js bpmnlint`, then `node render.cjs x.bpmn`. Never draw BPMN shapes in Mermaid or by hand in SVG.
- **Simplest construct that is true.** Start from the light palette (tasks, XOR and AND gateways, plain events). Reach for boundary events, event sub-processes, inclusive or event-based gateways, compensation, or multi-instance only when the process really behaves that way.
- **Pools are participants, lanes are roles.** One pool per organisation, with outside parties as empty black-box pools. Sequence flow never leaves a pool; only message flow crosses, and never inside one pool.
- **Left to right, on a grid.** Happy path on one straight row; exceptions drop below it. Tasks 100×80, events 36×36, gateways 50×50, about 150 between centres, pool name band 30 wide, lanes at least 120 tall. Stack pools vertically so message flows run straight up and down.
- **Right angles only.** You place every `dc:Bounds` and `di:waypoint` yourself, and each pair of consecutive waypoints shares an x or a y. No automatic layout: none of them handles pools, lanes or message flows.
- **Everything labeled, briefly.** Tasks: verb plus object. Events: the state reached ("Order received"). Splitting gateways: a question, with every outgoing flow labeled as an answer. Message flows: the message. Give each event, gateway and flow label its own bounds so it sits clear of the lines.
- **Honest semantics.** Every path runs from a start event to an end event. Split and join with the same gateway type. Catch markers are unfilled, throw markers filled; a dashed event border means non-interrupting. Give each exclusive or inclusive split a default flow, and a condition on every other flow.
- **Keep markers readable.** Make an activity 160 wide when it carries boundary events, and put those near its corners, clear of the bottom-centre markers. Use a call activity when the detail lives in another diagram, and a sub-process only when you draw its inside.
- **Lint clean.** List `<incoming>` and `<outgoing>` on every flow node, then run `npx bpmnlint x.bpmn` with `{"extends": "bpmnlint:recommended"}` in `.bpmnlintrc`. Zero errors, and no warnings from the renderer.
- **Look before you ship.** Open the PNG and remove every crossing, overlap and clipped label that moving a shape could fix. Commit the `.bpmn` source next to the SVG.
- **Draw what happens,** not what the policy says.
