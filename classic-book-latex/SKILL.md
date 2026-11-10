---
name: classic-book-latex
description: Typeset any prose document (book, report, essay, memo) as a classic American trade-book page - Times body, Bodoni Bold display, small-caps lead-ins, monochrome charts. Use when a PDF is wanted in this style.
---

# Classic trade-book interior

The spec is the source of truth; `assets/tradebook.sty` implements it for XeLaTeX. For any other output format, apply the spec by hand.

## Spec

| Element | Setting |
|---|---|
| Page | 6.125 x 9.25 in; text 27 pc wide, 39 lines; justified, hyphenated |
| Body | Times (TeX Gyre Termes) 11/13.6 pt, old-style figures, 1.5 em paragraph indent, no space between paragraphs |
| Display | Bodoni Bold (Libre Bodoni), centered, black only |
| Chapter opener | number 17 pt, 2.2 pc gap, title 21 pt, 3.5 pc gap, text; no running head or folio |
| Part page | own right-hand page: "Part I" 17 pt, then title 25 pt in letterspaced caps; blank back |
| First words | chapter and post-break paragraphs: no indent, first 2-3 words in caps and small caps |
| Section break | two blank lines; no ornament, no subheads |
| Running heads | left page: part title (else document title) in 8 pt letterspaced small caps; right page: chapter title in italic; both centered; folio at outer edge |
| Block quote | body size, 1.5 pc indent both sides, one blank line above and below |
| Contents | no leaders; "PART I" small caps hanging left; chapter numbers right-aligned; front matter in italic |
| Never | bold or underline in text, color, rules, boxes, sans-serif, bullet lists where prose works |

## Build

1. Copy everything in `assets/` beside the new `.tex`. If `assets/` is missing, fetch the files from `https://raw.githubusercontent.com/jjmargolis/Skills/main/classic-book-latex/assets/`.
2. Start from `example.tex`; write only the body. Do not add packages or redefine anything in the `.sty`.
3. Run `xelatex` twice. Render a page to an image and look at it before delivering.

## Commands

- `\booktitle{...}` once in the preamble.
- `\part{}`, `\chapter{}`, `\front{}` (unnumbered front matter). No `\section`.
- `\lead{As late as}` opens every chapter; `\scene{No radio}` opens every section after a break. Mixed case inside both.
- `quote` environment for quotations longer than three lines.
- Short documents: skip `\part` and `\tableofcontents`; one `\chapter` per major division, or `\front{Title}` for a single untitled-number piece.
- Text: ``` ``double'' ``` quotes, unspaced `---`, italics for titles and emphasis.

## Figures and charts

- Full measure, at the top or bottom of a page (`figure` with `[t]` or `[b]`), never wrapped by text.
- Caption below: `\caption*{\small\itshape ...}`, one sentence, no number.
- Charts: `import chart_style` (in `assets/`), `fig, ax = chart_style.figure(height=2.5)`, save as PDF. Black and grays only; distinguish series by dash pattern and label them directly at the line ends; no legend box, gridlines, or chart title (the caption is the title).
- Photographs: grayscale.
