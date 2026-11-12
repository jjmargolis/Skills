---
name: "carovision"
description: "Typeset prose (book, report, essay, memo) as a classic trade-book PDF: Times body, Bodoni Bold display, small-caps lead-ins, monochrome charts. Use when a document is wanted in this style."
---

# Classic trade-book interior

The spec is the source of truth; `carovision.sty` in this skill's folder implements it for XeLaTeX. For any other output format, apply the spec by hand.

## Spec

| Element | Setting |
|---|---|
| Page | 6.125 x 9.25 in; text 27 pc wide, 39 lines; justified, hyphenated |
| Body | Times (TeX Gyre Termes) 11/13.6 pt, old-style figures, 1.5 em paragraph indent, no space between paragraphs |
| Display | Bodoni Bold (Libre Bodoni), centered, black only |
| Chapter opener | number 17 pt, 2.2 pc gap, title 21 pt, 3.5 pc gap, text; no running head or folio |
| Part page | own right-hand page: "Part I" 17 pt, then title 25 pt in letterspaced caps; blank back |
| First words | chapter and post-break paragraphs: no indent, first 2-3 words in caps and small caps |
| Section break | two blank lines; a major break adds a centered 5 pc hairline; no ornaments, no subheads |
| Running heads | centered; left page: part title in 8 pt letterspaced small caps (no part: chapter title in italic); right page: chapter title in italic; folio at outer edge |
| Block quote | body size, 1.5 pc indent both sides, one blank line above and below |
| Contents | no leaders; "PART I" small caps hanging left; chapter numbers right-aligned; front matter in italic |
| Figure (inline) | full measure between two 0.4 pt rules; above the image "FIGURE 1" in 8 pt letterspaced small caps, then a one-sentence italic caption at 10 pt, centered |
| Plate (own page) | image alone at full measure, no running head, folio, rules or number; caption beneath, flush right, 14 pc wide, ragged, italic 10 pt in the body face |
| Never | sans-serif anywhere, bold or underline in text, color, boxes, bullet lists where prose works |

## Build

1. Copy `carovision.sty` and `LibreBodoni-Bold.ttf` from this skill's folder to beside the new `.tex`.
2. Write the document from the Example. Do not add packages or redefine anything.
3. Compile twice, then render the pages and look at them before delivering:
   ```bash
   xelatex -interaction=nonstopmode F.tex | grep -E "Output written|^! |Overfull"
   pdftoppm -png -r 80 F.pdf page
   ```
   Fix an `Overfull` line by rewording it or adding a `\-` hyphenation point.

Commands assume a Linux shell with XeLaTeX, poppler-utils and Python 3.

## Commands

- `\part{}`, `\chapter{}`, `\front{}` (unnumbered: Introduction, Preface). No `\section`.
- `\lead{As late as}` opens every chapter. `\scene{No radio}` opens a section after a break; `\scene*{It is not merely}` for a major break. Mixed case inside all three.
- `quote` environment for quotations longer than three lines.
- `\exhibit{file}{Caption.}`: inline figure at the top of a page (`\exhibit[b]` for bottom). Numbered; put `\label{f:x}` in the caption and cite as `Figure~\ref{f:x}`.
- `\plate{file}{Caption.}`: for a figure needing more than half the page height, or any photograph; it takes the next page alone. `\plate[l]` turns that page landscape, for wide figures with fine detail. Unnumbered; refer to it in the text by position.
- Keep at least a page of text between two figure commands.
- Short documents: skip `\part` and `\tableofcontents`.
- Text: ``` ``double'' ``` quotes, unspaced `---`, italics for titles and emphasis.

## Charts

Matplotlib, saved as PDF at final size so type is never rescaled: 4.5 in wide for an exhibit or portrait plate, 7 in for a landscape plate. Black and grays only; distinguish series by dash pattern and label them directly at the line ends; no legend box, gridlines or chart title (the caption is the title). Photographs grayscale.

```python
import subprocess, matplotlib as mpl
from matplotlib import font_manager as fm
for f in ("regular", "italic"):
    fm.fontManager.addfont(subprocess.check_output(["kpsewhich", f"texgyretermes-{f}.otf"], text=True).strip())
mpl.rcParams.update({"font.family": "TeX Gyre Termes", "font.size": 9, "axes.linewidth": .5,
    "axes.spines.top": False, "axes.spines.right": False, "xtick.major.width": .5,
    "ytick.major.width": .5, "xtick.major.size": 3, "ytick.major.size": 3, "lines.linewidth": 1.1,
    "axes.prop_cycle": mpl.cycler(color=["black", "0.45", "0.7"]), "pdf.fonttype": 42,
    "savefig.transparent": True, "savefig.bbox": "tight", "savefig.pad_inches": .02})
```

## Example

```latex
\documentclass[11pt,twoside,openright]{book}
\usepackage{carovision}
\begin{document}
\frontmatter
\tableofcontents
\front{Introduction}
\lead{Opening words} of the introduction.
\scene*{It is not} merely a pause; a major break carries a short rule.
\mainmatter
\part{The First Part}
\chapter{A Chapter Title}
\lead{As late as} 1935, text with ``quotes''---and unspaced em dashes.

Indented paragraph, leading into a quotation,
\begin{quote}
set as a block, indented on both sides.
\end{quote}
Text resumes, citing Figure~\ref{f:a}.
\exhibit{chart.pdf}{One-sentence caption.\label{f:a}}
\scene{No radio}; no movies; a section after a break.
\plate{photo.jpg}{Short caption for the plate.}
\end{document}
```

The titletoc warning `Unknown TOC type front` is expected.
