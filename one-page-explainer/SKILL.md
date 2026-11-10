---
name: "one-page-explainer"
description: "Make a clear one-page PDF explainer of a concept, with at least one chart, pitched at graduate, undergraduate, or general (ELI5) level."
---

# One-page explainer

The job is **understanding**, not coverage. A good explainer leaves the reader able to restate the idea in one sentence and explain *why* it's true. Everything below serves that.

## 1. Think before writing
Answer these in your head first. If you can't, you're not ready to lay out a page.
1. **The one sentence.** What should the reader be able to say afterwards? Write it down; it becomes the title/subtitle or the boxed claim.
2. **The question it answers.** What puzzle or tension makes this idea worth knowing? Open with that, not a definition.
3. **The why.** What mechanism makes it true? An explainer that states a result without its mechanism is a fact sheet.
4. **The misconception.** What do people usually get wrong, or what's the surprising part? Name it. This is often the most valuable line on the page.
5. **The limit.** When does it stop being true? Understanding includes the boundary.

## 2. Principles of a clear explainer
- **Concrete before abstract.** Start with a specific situation (named people, real numbers), then generalize. Never open with the formal statement.
- **One running example.** Use a single example from start to finish. Don't introduce a second unless it's the "limit" case contrasting with the first.
- **The chart carries the argument.** It should show the mechanism or the result, not decorate. A reader skimming only the title and chart should get the gist. If the chart could be deleted without loss, redesign it.
- **Text and chart agree exactly.** Same numbers, same names, same colors for the same actors in both.
- **Headline sentences.** Each paragraph's first sentence says its point; the rest supports it. Bold lead-ins ("How it works.", "The catch.") act as signposts.
- **Every element earns its place.** Cut anything that doesn't advance the one sentence: history, tangents, extra caveats. White space is fine. Under a page is fine.
- **Define each term once, at first use,** in plain words, even at graduate level if it's not universal.
- **End on why it matters,** framed as the idea's real lesson, not a summary.

## 3. Three levels
Same structure, different depth: **question → example → core claim → mechanism + chart → limit → why it matters.**

- **Graduate.** Formal statement with explicit assumptions; notation, optimality conditions, a proof sketch; worked example with functional forms and every number computed; analytical chart with labeled regions; limits include technical caveats; short reference list. Serif, 10pt, grayscale.
- **Undergraduate.** Plain-English boxed statement; a concrete textbook story; numbers but no calculus; the same analytical chart with axes in words, color, and a legend; 3 intuitive limits. Serif, 11pt, one accent color.
- **General (ELI5).** Everyday story with named characters; dollar amounts or counts only; a simple bar chart plus illustrated panels that walk through the cases step by step; one "catch"; minimal text, large type. Sans, 3–4 colors.

No fake textbook labels (chapter/figure numbers, running heads) unless asked. Write the page in the language the user asked in.

## 4. Honesty
- Compute every number yourself (Python if non-trivial). The chart uses the same functions/data.
- In the reply, say which facts and citations came from memory vs. a search; flag memory-only page numbers as worth checking.
- At simpler levels, say in one line what intuition was sacrificed.

## 5. Build
LaTeX + pgfplots/TikZ. Preamble basics: `geometry` (0.6–0.8in margins), `mathpazo` or `helvet` (sans), `microtype`, `amsmath`, `xcolor`, `pgfplots` + `fillbetween`, `tcolorbox` for a boxed claim, `enumitem` with `nosep`, `\pagestyle{empty}`, `\parindent 0pt`.

Layout that works:
- Text beside chart: two top-aligned `minipage`s (`[t]{0.52\textwidth}` / `[t]{0.45\textwidth}`, each beginning with `\vspace{0pt}`), chart `width=\linewidth`. Avoid `wrapfig`.
- If curve labels collide, use a legend below the axis and `forget plot` on fills.
- Draw ELI5 icons as simple TikZ shapes; avoid symbols from unloaded packages (they render blank). Keep full-width banners within the panels' x-range.

Build for alignment from the start (cheaper than fixing it later):
- **One spacing scale.** Define `\newlength\gap \setlength\gap{6pt}` (and at most `\biggap = 2\gap`) and use only those between blocks. No ad-hoc `\vspace{3.5pt}`.
- **Charts flush to the text edge.** pgfplots puts tick labels *outside* `width`, so the visible chart overhangs its column. Use `scale only axis` with a width that leaves room for labels, or wrap the `tikzpicture` with `trim axis left`/`trim axis right` so the axis line sits on the column edge.
- **Boxes match the text block.** `tcolorbox` with `width=\linewidth` and `left skip=0pt, right skip=0pt`; text inside the box uses the same font size as body unless it's the boxed claim.
- **Fixed gutter.** Columns are separated by one `\hfill` with widths summing to ≤ 0.97\textwidth; every row of columns/panels uses the same widths.
- **Equal-height panels** (ELI5 step panels): `tcbraster` with `raster equal height`, not hand-tuned `\vspace`.
- **Chart text matches body.** `every axis label/.style={font=\small}`, tick labels `\footnotesize`; same font family as the page.

## 6. Check, then deliver
```bash
pdflatex -interaction=nonstopmode F.tex | grep -E "Output written|^! |Overfull"
pdfinfo F.pdf | grep Pages
pdftoppm -png -r 80 F.pdf preview   # Read the PNG and look at it
```
Layout pass: 1 page, no errors, no overlaps or clipping.

**Alignment pass** (do this every time; it's where pages look amateur):
1. Compile once with `\usepackage{showframe}` added, render at `-r 150`, and Read it. The frame shows the true text block; nothing should poke outside it (chart tick labels and box borders are the usual offenders). Remove `showframe` after.
2. Measure left edges instead of eyeballing them:
```bash
pdftotext -bbox-layout F.pdf bbox.html
python3 - <<'EOF'
import re, collections
h = open('bbox.html').read()
xs = [round(float(x)) for x in re.findall(r'<block xMin="([\d.]+)"', h)]
for x, n in sorted(collections.Counter(xs).items()): print(x, n)
EOF
```
Text left edges should fall on exactly one x per column. A value 1–4pt off a cluster is a misalignment (stray indent, box padding, `\noindent` missing); find and fix it. Isolated values inside a chart's x-range are tick labels and are fine.
3. Check by eye on the 150dpi render:
- **Tops:** side-by-side columns start on the same line: first text baseline level with the chart's top edge / the other column's heading.
- **Bottoms:** columns end within about one line of each other, or the difference is clearly intentional. A long ragged gap under one column means rebalance (move a paragraph, resize chart).
- **Gutters & margins:** the same gutter between every column pair; equal left/right page margins; full-width elements (title rule, banner, boxed claim) span exactly the text block.
- **Vertical rhythm:** the same gap between every section; headings sit closer to what follows than to what precedes. No double gaps from a `\vspace` plus a paragraph break.
- **Internal alignment:** list bullets align with paragraph text edges; table numbers right- or decimal-aligned (`siunitx` `S` columns); legend and labels not touching curves or the frame.
- **Panels:** step panels equal height, captions on the same baseline, icons centered in their panels.

**Clarity pass** (reread the rendered page as the target reader):
- Can I state the one sentence from the title + chart alone?
- Is the mechanism (the why) on the page, not just the result?
- Is the misconception or surprise named?
- Does anything not serve the one sentence? Cut it.
- Is any term used before it's defined?

Iterate until all three passes are clean. Send with SendUserFile (`display: render`). Reply in a few lines: what's on the page, memory vs. sources, and one honest trade-off.