# Comparison: two things

The job is **discrimination**, not description. A good comparison leaves the reader able to say, in one sentence, *what actually separates* A from B and *when that difference decides things*. Two parallel fact sheets glued together is a failure. A feature table with 15 rows is a failure.

Exactly two things. If the user names three or more, ask which two matter, or pick the pair the question actually turns on and say why.

## Think before writing
Answer these first. If you can't, you're not ready to lay out a page.
1. **The one sentence.** "A does X by doing P; B does it by doing Q; so A wins when C, B wins when not-C." Write it down; it becomes the title/subtitle or the boxed claim.
2. **Why they get compared.** What do they share: same goal, same inputs, same problem? This common ground is what makes the difference meaningful. Open with the shared question, not with A's definition.
3. **The pivotal difference.** The one underlying mechanism or assumption that most of the surface differences flow from. Most comparisons have 1, sometimes 2. Everything else is a consequence; show it as one, or cut it.
4. **The deciding condition.** The variable (scale, time horizon, risk, cost of error, data size…) on which the choice flips. If there's a crossover point, find it and compute it.
5. **The confusion.** What do people get wrong: treat them as the same, think one strictly dominates, misattribute a difference? Name it.
6. **The fair case for each.** State B's best case as its advocates would. If one really dominates, say so plainly, but only after steelmanning the loser. No manufactured "it depends" when it doesn't.

## Principles
- **One shared example.** Run *the same* concrete scenario through both A and B, with the same numbers. That is the comparison. Introduce a second scenario only to show the case where the winner flips.
- **Parallel structure.** Whatever you say about A, say the matching thing about B, in the same order, same length, same position on the page. Asymmetric treatment reads as bias.
- **Fixed colors.** A gets one color, B another, everywhere: text highlights, chart series, panel borders, legend. Never reuse either for anything else.
- **The chart shows the difference, not the two things.** Prefer: both on the same axes against the deciding variable (crossover visible), a difference/ratio plot, or a side-by-side of the shared example's outcome. Not two separate charts. A reader skimming title + chart should know who wins where.
- **A short contrast table is allowed, not required.** Max ~5 rows, only dimensions that matter, the pivotal one first and visually marked. If a row doesn't change a decision, drop it.
- **Headline sentences, bold signposts** ("What they share.", "Where they split.", "When B wins.").
- **Define each term once, at first use.**
- **End on the decision rule,** not a summary: "Use A if…; use B if…", or, if neither is a choice (two concepts), the lesson the contrast teaches.

## Levels
Same structure, different depth: **shared question → shared example → the one sentence → pivotal difference + chart → when each wins (crossover) → the confusion → decision rule.**

- **Graduate.** Formal statement of each with explicit assumptions; show where the assumptions diverge; notation, conditions under which they coincide (nesting/special cases); worked example with functional forms, every number computed; crossover derived analytically if possible; chart with labeled regions ("A preferred" / "B preferred"); technical caveats; short reference list. Serif, 10pt, grayscale with two distinguishable patterns/line styles for A and B.
- **Undergraduate.** Plain-English boxed one-sentence contrast; a concrete textbook scenario run through both; math through multivariable calculus (derivatives, integrals, partials, constrained optimization), no linear algebra or multi-step proofs; same-axes chart with axes in words, two colors, legend; compact contrast table (≤5 rows); 2–3 intuitive "when the answer flips" cases. Serif, 11pt, two accent colors (A, B).
- **General (ELI5).** Two named characters (one per approach) facing the same everyday problem; dollar amounts or counts only; side-by-side illustrated panels walking through what each does; a simple bar chart of the outcome; one "but if…" panel where the other one wins. Minimal text, large type. Sans, A color + B color + one neutral.

## Honesty
- Compute the crossover yourself, with the same functions the chart uses.
- Don't tilt the example to favor a side. If you must choose parameters, pick ones near the crossover or state why they're typical.
- If the comparison is empirically contested (e.g., which policy works better), say so on the page and show the range, not a verdict.

## Build
Define colors once: `\definecolor{colA}{...}` / `\definecolor{colB}{...}` and macros `\A{}` / `\B{}` that typeset each name in its color, so text and chart can't drift.

- **Mirrored columns:** two equal `minipage`s (`[t]{0.48\textwidth}`, each starting `\vspace{0pt}`) for A and B, then a full-width chart and decision rule below. Best for ELI5 and undergrad. Text beside chart is best for graduate.
- **Mirror precisely.** A and B columns use identical widths, identical heading macros, and the same section order, so matching sections can land on the same baseline. Put the two columns in a `tcbraster` with `raster equal height` (or `equal height group=ab` on paired boxes) rather than padding with `\vspace`.
- **Table:** `booktabs`, numbers in `siunitx` `S` columns, A and B as the two data columns in the same left/right order as the mirrored columns above.
- Shade the A-wins / B-wins regions with `fillbetween` at low opacity.

## Alignment pass
On a comparison page, misalignment between A and B reads as imbalance. On top of the shared checks:
- **Block tops:** matching A/B section headings share a y value (within ~1pt) in the `check.py` output.
- **Mirror symmetry:** A and B columns have the same width, start on the same line, and their matching headings/sections sit at the same height. Bottoms end within about one line of each other; if one side is much longer, that's also a parallel-structure problem in the content, so fix the text, not just the spacing.
- **Colors:** A and B colors consistent everywhere; shaded regions start at the computed crossover, not near it.

## Clarity pass
Reread the rendered page as the target reader:
- Can I state the one-sentence contrast from title + chart alone?
- Is the pivotal difference a *mechanism*, not a list of features?
- Is the deciding condition (and crossover, if any) on the page?
- Are A and B treated in parallel: same depth, same order, steelmanned?
- Is the confusion named?
- Does every table row / sentence change a decision? Cut the rest.
