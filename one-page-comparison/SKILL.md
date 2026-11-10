---
name: "one-page-comparison"
description: "Make a one-page PDF comparing two things (concepts, methods, policies, tools), with at least one chart, at graduate, undergraduate, or general (ELI5) level."
---

# One-page comparison

The job is **discrimination**, not description. A good comparison leaves the reader able to say, in one sentence, *what actually separates* A from B and *when that difference decides things*. Two parallel fact sheets glued together is a failure. A feature table with 15 rows is a failure.

Exactly two things. If the user names three or more, ask which two matter, or pick the pair the question actually turns on and say why.

## 1. Think before writing
Answer these first. If you can't, you're not ready to lay out a page.
1. **The one sentence.** "A does X by doing P; B does it by doing Q; so A wins when C, B wins when not-C." Write it down; it becomes the title/subtitle or the boxed claim.
2. **Why they get compared.** What do they share: same goal, same inputs, same problem? This common ground is what makes the difference meaningful. Open with the shared question, not with A's definition.
3. **The pivotal difference.** The one underlying mechanism or assumption that most of the surface differences flow from. Most comparisons have 1, sometimes 2. Everything else is a consequence; show it as one, or cut it.
4. **The deciding condition.** The variable (scale, time horizon, risk, cost of error, data size…) on which the choice flips. If there's a crossover point, find it and compute it.
5. **The confusion.** What do people get wrong: treat them as the same, think one strictly dominates, misattribute a difference? Name it.
6. **The fair case for each.** State B's best case as its advocates would. If one really dominates, say so plainly, but only after steelmanning the loser. No manufactured "it depends" when it doesn't.

## 2. Principles of a clear comparison
- **One shared example.** Run *the same* concrete scenario through both A and B, with the same numbers. That is the comparison. Introduce a second scenario only to show the case where the winner flips.
- **Parallel structure.** Whatever you say about A, say the matching thing about B, in the same order, same length, same position on the page. Asymmetric treatment reads as bias.
- **Fixed colors.** A gets one color, B another, everywhere: text highlights, chart series, panel borders, legend. Never reuse either for anything else.
- **The chart shows the difference, not the two things.** Prefer: both on the same axes against the deciding variable (crossover visible), a difference/ratio plot, or a side-by-side of the shared example's outcome. Not two separate charts. A reader skimming title + chart should know who wins where.
- **A short contrast table is allowed, not required.** Max ~5 rows, only dimensions that matter, the pivotal one first and visually marked. If a row doesn't change a decision, drop it.
- **Headline sentences, bold signposts** ("What they share.", "Where they split.", "When B wins.").
- **Define each term once, at first use.**
- **End on the decision rule,** not a summary: "Use A if…; use B if…", or, if neither is a choice (two concepts), the lesson the contrast teaches.

## 3. Three levels
Same structure, different depth: **shared question → shared example → the one sentence → pivotal difference + chart → when each wins (crossover) → the confusion → decision rule.**

- **Graduate.** Formal statement of each with explicit assumptions; show where the assumptions diverge; notation, conditions under which they coincide (nesting/special cases); worked example with functional forms, every number computed; crossover derived analytically if possible; chart with labeled regions ("A preferred" / "B preferred"); technical caveats; short reference list. Serif, 10pt, grayscale with two distinguishable patterns/line styles for A and B.
- **Undergraduate.** Plain-English boxed one-sentence contrast; a concrete textbook scenario run through both; numbers, no calculus; same-axes chart with axes in words, two colors, legend; compact contrast table (≤5 rows); 2–3 intuitive "when the answer flips" cases. Serif, 11pt, two accent colors (A, B).
- **General (ELI5).** Two named characters (one per approach) facing the same everyday problem; dollar amounts or counts only; side-by-side illustrated panels walking through what each does; a simple bar chart of the outcome; one "but if…" panel where the other one wins. Minimal text, large type. Sans, A color + B color + one neutral.

No fake textbook labels unless asked. Write in the language the user asked in.

## 4. Honesty
- Compute every number yourself (Python if non-trivial), including the crossover. The chart uses the same functions/data.
- Don't tilt the example to favor a side. If you must choose parameters, pick ones near the crossover or state why they're typical.
- If the comparison is empirically contested (e.g., which policy works better), say so on the page and show the range, not a verdict.
- In the reply, say which facts and citations came from memory vs. a search; flag memory-only numbers and page references as worth checking.
- At simpler levels, say in one line what nuance was sacrificed.

## 5. Build
LaTeX + pgfplots/TikZ. Preamble basics: `geometry` (0.6–0.8in margins), `mathpazo` or `helvet` (sans), `microtype`, `amsmath`, `xcolor`, `pgfplots` + `fillbetween`, `tcolorbox` for the boxed claim, `booktabs` for the contrast table, `enumitem` with `nosep`, `\pagestyle{empty}`, `\parindent 0pt`.

Define colors once: `\definecolor{colA}{...}` / `\definecolor{colB}{...}` and macros `\A{}` / `\B{}` that typeset each name in its color, so text and chart can't drift.

Layouts that work:
- **Mirrored columns:** two equal `minipage`s (`[t]{0.48\textwidth}`, each starting `\vspace{0pt}`) for A and B, then a full-width chart and decision rule below. Best for ELI5 and undergrad.
- **Text beside chart:** `[t]{0.52\textwidth}` / `[t]{0.45\textwidth}`, chart `width=\linewidth`. Best for graduate.
- Avoid `wrapfig`. If curve labels collide, legend below the axis and `forget plot` on fills. Shade the A-wins / B-wins regions with `fillbetween` at low opacity.
- ELI5 icons as simple TikZ shapes; no symbols from unloaded packages (they render blank).

Build for alignment from the start (cheaper than fixing it later):
- **One spacing scale.** Define `\newlength\gap \setlength\gap{6pt}` (and at most `\biggap = 2\gap`) and use only those between blocks. No ad-hoc `\vspace{3.5pt}`.
- **Mirror precisely.** A and B columns use identical widths, identical heading macros, and the same section order, so matching sections can land on the same baseline. Put the two columns in a `tcbraster` with `raster equal height` (or `equal height group=ab` on paired boxes) rather than padding with `\vspace`.
- **Charts flush to the text edge.** pgfplots puts tick labels *outside* `width`, so the visible chart overhangs its column. Use `scale only axis` with a width that leaves room for labels, or `trim axis left`/`trim axis right`, so the axis line sits on the column edge.
- **Boxes match the text block.** `tcolorbox` with `width=\linewidth`, `left skip=0pt, right skip=0pt`.
- **Fixed gutter.** Columns separated by one `\hfill`, widths summing to ≤ 0.97\textwidth; every row of columns/panels uses the same widths.
- **Table:** `booktabs`, numbers in `siunitx` `S` columns, A and B as the two data columns in the same left/right order as the mirrored columns above.
- **Chart text matches body.** `every axis label/.style={font=\small}`, tick labels `\footnotesize`; same font family as the page.

## 6. Check, then deliver
```bash
pdflatex -interaction=nonstopmode F.tex | grep -E "Output written|^! |Overfull"
pdfinfo F.pdf | grep Pages
pdftoppm -png -r 80 F.pdf preview   # Read the PNG and look at it
```
Layout pass: 1 page, no errors, no overlaps or clipping, A/B colors consistent everywhere.

**Alignment pass** (do this every time; on a comparison page, misalignment between A and B reads as imbalance):
1. Compile once with `\usepackage{showframe}` added, render at `-r 150`, and Read it. Nothing should poke outside the text block (chart tick labels and box borders are the usual offenders). Remove `showframe` after.
2. Measure edges instead of eyeballing them:
```bash
pdftotext -bbox-layout F.pdf bbox.html
python3 - <<'EOF'
import re, collections
h = open('bbox.html').read()
blocks = re.findall(r'<block xMin="([\d.]+)" yMin="([\d.]+)"', h)
print('left edges:')
for x, n in sorted(collections.Counter(round(float(x)) for x, _ in blocks).items()): print(' ', x, n)
print('block tops (y):')
for y, n in sorted(collections.Counter(round(float(y)) for _, y in blocks).items()): print(' ', y, n)
EOF
```
Left edges: exactly one x per column; a value 1–4pt off a cluster is a misalignment (stray indent, box padding) to fix. Tops: matching A/B section headings should share a y value (within ~1pt). Isolated values inside a chart's range are tick labels and are fine.
3. Check by eye on the 150dpi render:
- **Mirror symmetry:** A and B columns have the same width, start on the same line, and their matching headings/sections sit at the same height. Bottoms end within about one line of each other; if one side is much longer, that's also a parallel-structure problem in the content, so fix the text, not just the spacing.
- **Gutters & margins:** the same gutter between every column pair; equal left/right page margins; full-width elements (title rule, boxed claim, chart, decision rule) span exactly the text block.
- **Vertical rhythm:** the same gap between every section; headings closer to what follows than to what precedes; no double gaps.
- **Internal alignment:** bullets align with paragraph edges; table numbers decimal-aligned; legend and labels clear of curves and the frame; A/B shaded regions start at the computed crossover, not near it.
- **Panels (ELI5):** paired panels equal height, captions on the same baseline, icons centered.

**Clarity pass** (reread the rendered page as the target reader):
- Can I state the one-sentence contrast from title + chart alone?
- Is the pivotal difference a *mechanism*, not a list of features?
- Is the deciding condition (and crossover, if any) on the page?
- Are A and B treated in parallel: same depth, same order, steelmanned?
- Is the confusion named?
- Does every table row / sentence change a decision? Cut the rest.

Iterate until all three passes are clean. Send with SendUserFile (`display: render`). Reply in a few lines: the one-sentence contrast, memory vs. sources, and one honest trade-off.