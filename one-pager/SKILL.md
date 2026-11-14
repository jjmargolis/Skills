---
name: "one-pager"
description: "Make a one-page PDF, with at least one chart, that explains one concept or compares two things (concepts, methods, policies, tools), at graduate, undergraduate, or general (ELI5) level."
---

# One-pager

A single page that leaves the reader able to restate the idea in one sentence. Two modes; read the mode file before anything else:

- **Explain one concept:** `explainer.md`
- **Compare two things:** `comparison.md`

Each mode file gives the thinking steps, the principles, the three levels and the clarity pass. Honesty, build and checks below are shared.

Level sets vocabulary and math, not substance. Anything that bears on the conclusion (how a headline number was built, a contested assumption, a live empirical dispute) appears at every level, explained in that level's terms.

No fake textbook labels (chapter/figure numbers, running heads) unless asked. Write the page in the language the user asked in.

## Honesty
- Compute every number yourself (Python if non-trivial). The chart uses the same functions/data.
- In the reply, say which facts and citations came from memory vs. a search; flag memory-only numbers and page references as worth checking.
- At simpler levels, say in one line what formalism was simplified.

## Build
LaTeX + pgfplots/TikZ. Copy `onepager.sty` from this skill's folder to beside the `.tex` and start from:
```latex
\documentclass[11pt]{article}  % 10pt graduate, 11pt undergraduate, 12pt ELI5
\usepackage{onepager}          % [sans] for ELI5
```
The package sets 0.7in margins (`\geometry{margin=...}` to move within 0.6–0.8in), no page number and no paragraph indent. It puts text, math and chart labels in one family (Palatino, or Helvetica with `sans`) and loads `amsmath`, `xcolor`, `pgfplots` + `fillbetween`, `tcolorbox` with `tcbraster`, `booktabs`, `siunitx` and `enumitem` with `nosep`. A character the font lacks is a compile error. Add no other font package.

For a language outside Latin script, compile with `xelatex` instead of `pdflatex`. The package then loads `fontspec`, and the document names a font that covers the script: `\setmainfont{...}` (add `polyglossia` for right-to-left scripts).

Layout that works:
- Text beside chart: two top-aligned `minipage`s (`[t]{0.52\textwidth}` / `[t]{0.45\textwidth}`, each beginning with `\vspace{0pt}`), chart `width=\linewidth`. Avoid `wrapfig`.
- If curve labels collide, use a legend below the axis and `forget plot` on fills.
- Draw ELI5 icons as simple TikZ shapes. Keep full-width banners within the panels' x-range.

Build for alignment from the start (cheaper than fixing it later):
- **One spacing scale.** Use only `\vspace{\gap}` (6pt) and `\vspace{\biggap}` (12pt) between blocks. No ad-hoc `\vspace{3.5pt}`.
- **Charts flush to the text edge.** pgfplots puts tick labels *outside* `width`, so the visible chart overhangs its column. Use `scale only axis` with a width that leaves room for labels, or wrap the `tikzpicture` with `trim axis left`/`trim axis right` so the axis line sits on the column edge.
- **Boxes match the text block.** `tcolorbox` with `width=\linewidth` and `left skip=0pt, right skip=0pt`; text inside the box uses the same font size as body unless it's the boxed claim.
- **Fixed gutter.** Columns are separated by one `\hfill` with widths summing to ≤ 0.97\textwidth; every row of columns/panels uses the same widths.
- **Equal-height panels** (ELI5 step panels): `tcbraster` with `raster equal height`, not hand-tuned `\vspace`.
- **Chart text matches body.** The package sets axis labels `\small` and tick labels `\footnotesize` in the page's family; leave them.

## Check, then deliver
Commands assume a Linux shell with pdfLaTeX, poppler-utils and Python 3.
```bash
pdflatex -interaction=nonstopmode F.tex >/dev/null   # equal-height boxes settle on the second run
pdflatex -interaction=nonstopmode F.tex | grep -E "Output written|^! |Overfull"
pdftoppm -png -r 80 F.pdf preview   # look at the PNG
```
Layout pass: 1 page, no errors, no overlaps or clipping.

**Alignment pass** (do this every time; it's where pages look amateur):
1. Compile once with `\usepackage{showframe}` added, render at `-r 150`, and look at it. The frame shows the true text block; nothing should poke outside it (chart tick labels and box borders are the usual offenders). Remove `showframe` after.
2. Measure edges instead of eyeballing them, with `check.py` from this skill's folder:
```bash
python3 check.py F.pdf
```
It prints the page count, then how many text blocks start at each left edge (x) and each top (y). Left edges should fall on exactly one x per column. A value 1–4pt off a cluster is a misalignment (stray indent, box padding, `\noindent` missing); find and fix it. Isolated values inside a chart's range are tick labels and are fine.
3. Check by eye on the 150dpi render:
- **Tops:** side-by-side columns start on the same line: first text baseline level with the chart's top edge / the other column's heading.
- **Bottoms:** columns end within about one line of each other, or the difference is clearly intentional. A long ragged gap under one column means rebalance (move a paragraph, resize chart).
- **Gutters & margins:** the same gutter between every column pair; equal left/right page margins; full-width elements (title rule, banner, boxed claim) span exactly the text block.
- **Vertical rhythm:** the same gap between every section; headings sit closer to what follows than to what precedes. No double gaps from a `\vspace` plus a paragraph break.
- **Internal alignment:** list bullets align with paragraph text edges; table numbers right- or decimal-aligned (`siunitx` `S` columns); legend and labels not touching curves or the frame.
- **Panels:** step panels equal height, captions on the same baseline, icons centered in their panels.

**Chart integrity pass** (every chart must be rigorous and impossible to misread):
- Bar charts start at zero. A line chart with a truncated y-axis marks the break.
- Log scale only when data span orders of magnitude or the claim is about ratios or growth rates; the axis says "log scale"; charts being compared use the same scale type.
- Panels being compared share axis ranges and units. No dual y-axes.
- Every axis has units; dollars state nominal or real and the base year; data charts name their source.
- Size and area encode value linearly; no icons scaled by height.
- Aspect ratio neither exaggerates nor flattens the trend.
- Plotted values match the computed numbers and the text exactly.

**Clarity pass:** the questions at the end of the mode file.

Iterate until all four passes are clean. Deliver the PDF so the user can open it. Reply in a few lines: the one sentence, memory vs. sources, and one honest trade-off.
