---
name: carovision
description: Typeset prose (book, report, essay, memo) as a classic trade-book PDF: Times body, Bodoni Bold display, small-caps lead-ins, monochrome charts. Use when a document is wanted in this style.
---

# Classic trade-book interior

The spec is the source of truth; the package below implements it for XeLaTeX. For any other output format, apply the spec by hand.

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

1. Save the Package block as `carovision.sty` beside the new `.tex`.
2. Get the display font into the same folder (without it headings fall back to Times Bold, with a warning; tell the user):
   ```bash
   curl -sLo vf.ttf "https://raw.githubusercontent.com/google/fonts/main/ofl/librebodoni/LibreBodoni%5Bwght%5D.ttf"
   python3 -m fontTools.varLib.instancer vf.ttf wght=700 -o LibreBodoni-Bold.ttf  # pip install fonttools
   ```
3. Write the document from the Example. Do not add packages or redefine anything.
4. Run `xelatex` twice. Render a page to an image and look at it before delivering.

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

## Package

```latex
% carovision.sty -- compile with xelatex
\ProvidesPackage{carovision}
\RequirePackage[paperwidth=6.125in,paperheight=9.25in,textwidth=27pc,lines=39,
  inner=.8in,top=.85in,headsep=1.2pc,headheight=14pt]{geometry}
\RequirePackage{fontspec,microtype,titletoc,fancyhdr,graphicx,afterpage,pdflscape}
\RequirePackage[newparttoc]{titlesec}

% type
\setmainfont{texgyretermes}[Extension=.otf,UprightFont=*-regular,ItalicFont=*-italic,
  BoldFont=*-bold,BoldItalicFont=*-bolditalic,Numbers=OldStyle]
\IfFontExistsTF{LibreBodoni-Bold.ttf}
  {\newfontfamily\display{LibreBodoni-Bold.ttf}[WordSpace=1.5]}
  {\PackageWarningNoLine{carovision}{LibreBodoni-Bold.ttf not found; using Times Bold}%
   \newcommand\display{\bfseries}}
\newcommand\spacedcaps[1]{{\addfontfeature{LetterSpace=18}\textsc{\MakeLowercase{#1}}}}
\raggedbottom

% running heads
\pagestyle{fancy}\fancyhf{}\renewcommand\headrulewidth{0pt}
\fancyhead[CE]{\edef\tb@l{\leftmark}\ifx\tb@l\empty\textit{\rightmark}\else
  {\footnotesize\spacedcaps{\leftmark}}\fi}
\fancyhead[CO]{\textit{\rightmark}}\fancyhead[LE,RO]{\thepage}
\renewcommand\chaptermark[1]{\markright{#1}}\markboth{}{}

% part and chapter
\newcommand\tb@part[1]{\markboth{#1}{}\MakeUppercase{#1}}
\titleclass{\part}{page}\assignpagestyle{\part}{empty}
\titleformat{\part}[display]{\display\centering}{\LARGE Part\enspace\thepart}{2.5pc}
  {\Huge\addfontfeature{LetterSpace=12}\tb@part}
\titlespacing*{\part}{0pt}{7pc}{0pt}
\assignpagestyle{\chapter}{empty}
\titleformat{\chapter}[display]{\display\centering}{\LARGE\thechapter}{2.2pc}{\huge}
\titlespacing*{\chapter}{0pt}{2pc}{3.5pc}

% contents
\newcommand\tb@lab[1]{\makebox[0pt][r]{#1\hspace{1pc}}}
\newcommand\tb@pg{\hfill\thecontentspage\hspace*{2pc}}
\contentsmargin{0pt}
\titlecontents{part}[6pc]{\addvspace{.9pc}}
  {\tb@lab{\textsc{part\enspace\MakeLowercase{\thecontentslabel}}}\MakeUppercase}
  {\MakeUppercase}{\tb@pg}[\vspace{.2pc}]
\titlecontents{chapter}[6pc]{}{\tb@lab{\thecontentslabel}}{}{\tb@pg}
\titlecontents{front}[6pc]{\itshape}{}{}{\tb@pg}[\vspace{.3pc}]
\let\tb@toc\tableofcontents\renewcommand\tableofcontents{\tb@toc\markboth{}{Contents}}

% text
\newcommand\front[1]{\chapter*{#1}\markright{#1}\addcontentsline{toc}{front}{#1}}
\newcommand\lead[1]{\noindent{\addfontfeature{LetterSpace=4}\textsc{#1}}}
\newcommand\scene{\@ifstar\tb@major\tb@minor}
\newcommand\tb@minor[1]{\par\vspace{2\baselineskip}\lead{#1}}
\newcommand\tb@major[1]{\par\vspace{1.4\baselineskip}{\centering\rule{5pc}{.4pt}\par}%
  \vspace{1.4\baselineskip}\lead{#1}}
\renewenvironment{quote}{\list{}{\leftmargin1.5pc\rightmargin1.5pc
  \topsep\baselineskip\partopsep0pt\parsep0pt}\item\relax}{\endlist}

% figures
\counterwithout{figure}{chapter}
\newcommand\tb@rule{\hrule height .4pt}
\newcommand\exhibit[3][t]{\begin{figure}[#1]\tb@rule\vspace{.6pc}{\centering
  \refstepcounter{figure}{\footnotesize\spacedcaps{Figure \thefigure}}\par\vspace{.2pc}
  {\small\itshape #3\par}\vspace{.6pc}\includegraphics[width=\textwidth]{#2}\par}%
  \vspace{.5pc}\tb@rule\end{figure}}
\newcommand\tb@plate[2]{\thispagestyle{empty}{\centering\includegraphics[width=\linewidth,
  height=\dimexpr\textheight-6pc\relax,keepaspectratio]{#1}\par}\vspace{.6pc}%
  \noindent\hfill\begin{minipage}[t]{14pc}\raggedright\small\itshape #2\end{minipage}}
\newcommand\plate[3][p]{\afterpage{\if l#1\begin{landscape}\tb@plate{#2}{#3}\end{landscape}%
  \else\clearpage\tb@plate{#2}{#3}\clearpage\fi}}
```

The titletoc warning `Unknown TOC type front` is expected.
