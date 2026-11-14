#!/usr/bin/env python3
"""A2 poster of two voronoi-treemap charts, as one vector PDF.

    python poster.py out.pdf first.csv second.csv

Each chart is drawn afresh from its CSV by voronoi_treemap.py, with the short
key that leaves out cells too small to number, so the key fits beside a
second chart. The two charts are placed at the largest common scale that fits A2, either
side by side on a landscape sheet or stacked on a portrait one, whichever
scale is larger. Under the charts, each chart's '# source:', '# source_url:'
and '# as_of:' lines are cited in full, with the URLs as live links. The
'# title:' and '# subtitle:' lines of out.csv, if it exists, head the poster.
"""
import sys
import tempfile
from pathlib import Path

from pypdf import PdfReader, PdfWriter, Transformation
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "voronoi-treemap"))
import voronoi_treemap  # noqa: E402

MM = 72 / 25.4
A2 = (420 * MM, 594 * MM)       # portrait, in points
MARGIN, GUTTER = 15 * MM, 8 * MM
HEAD = 34 * MM                  # heading band, sheet edge margin to rule
INK, MUTED, RULE = HexColor("#1a1a19"), HexColor("#5f5e58"), HexColor("#c9c8c2")
FONTS = Path("/usr/share/fonts/truetype/dejavu")  # the face the charts use
pdfmetrics.registerFont(TTFont("Sans", FONTS / "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("Sans-Bold", FONTS / "DejaVuSans-Bold.ttf"))
CITE = [("Sans-Bold", 11, INK), ("Sans", 9, MUTED), ("Sans", 7.5, MUTED)]  # name, source, URL
LEAD = 1.4                      # line height, in font sizes


def meta(path):
    """'# key: value' header lines; a repeated key collects into a list."""
    out = {}
    if Path(path).exists():
        for line in Path(path).read_text(encoding="utf-8").splitlines():
            if line.startswith("#"):
                k, _, v = line[1:].partition(":")
                out.setdefault(k.strip(), []).append(v.strip())
    return out


def wrap(text, font, size, width):
    """Greedy word wrap; a word wider than the line (a URL) breaks by character."""
    fits = lambda s: pdfmetrics.stringWidth(s, font, size) <= width
    lines, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if fits(trial):
            line = trial
            continue
        if line:
            lines.append(line)
        line = ""
        for ch in word:
            if not fits(line + ch):
                lines.append(line)
                line = ""
            line += ch
    return lines + [line] if line else lines


def citation(m, width):
    """Lines (text, style index, url or None) citing one chart."""
    one = lambda k: m.get(k, [""])[0]
    out = [(s, 0, None) for s in wrap(one("title"), *CITE[0][:2], width)]
    text = " ".join(filter(None, ["Source: " + "; ".join(m["source"]) + "." if "source" in m else "",
                                  f"Data as of {one('as_of')}." if "as_of" in m else ""]))
    out += [(s, 1, None) for s in wrap(text, *CITE[1][:2], width)]
    for url in m.get("source_url", []):
        out += [(s, 2, url) for s in wrap(url, *CITE[2][:2], width)]
    return out


def height(lines):
    return sum(CITE[i][1] * LEAD for _, i, _ in lines)


def placement(sizes, foot):
    """Sheet size, scale and lower-left corner of each chart, for whichever of
    side-by-side landscape or stacked portrait gives the larger scale."""
    (w1, h1), (w2, h2) = sizes
    options = []
    W, H = A2[1], A2[0]  # landscape: charts in a row, tops aligned
    box_w, box_h = W - 2 * MARGIN - GUTTER, H - 2 * MARGIN - HEAD - foot
    s = min(box_w / (w1 + w2), box_h / max(h1, h2))
    x0, top = (W - s * (w1 + w2) - GUTTER) / 2, H - MARGIN - HEAD
    options.append((s, (W, H), [(x0, top - s * h1), (x0 + s * w1 + GUTTER, top - s * h2)]))
    W, H = A2  # portrait: charts in a column
    box_w, box_h = W - 2 * MARGIN, H - 2 * MARGIN - HEAD - foot - GUTTER
    s = min(box_w / max(w1, w2), box_h / (h1 + h2))
    top = H - MARGIN - HEAD
    options.append((s, (W, H), [((W - s * w1) / 2, top - s * h1),
                                ((W - s * w2) / 2, top - s * h1 - GUTTER - s * h2)]))
    return max(options, key=lambda o: o[0])


def main(out, *csvs):
    out = Path(out)
    tmp = Path(tempfile.mkdtemp())
    pages = []
    for i, path in enumerate(csvs):
        voronoi_treemap.main(path, tmp / str(i), short_key=True, formats=("pdf",))
        pages.append(PdfReader(tmp / f"{i}.pdf").pages[0])
    sizes = [(float(p.mediabox.width), float(p.mediabox.height)) for p in pages]
    head = {k: v[0] for k, v in meta(out.with_suffix(".csv")).items()}

    # The source band is sized for the narrower (landscape) columns, the worst case.
    col_w = (A2[1] - 2 * MARGIN - GUTTER) / 2
    foot = max(height(citation(meta(c), col_w)) for c in csvs) + 12 * MM
    scale, (W, H), corners = placement(sizes, foot)
    col_w = (W - 2 * MARGIN - GUTTER) / 2
    cites = [citation(meta(c), col_w) for c in csvs]

    # Heading, rules and citations on one reportlab page; the charts merge onto it.
    frame = tmp / "frame.pdf"
    c = canvas.Canvas(str(frame), pagesize=(W, H), invariant=1, initialFontName="Sans")
    c.setTitle(head.get("title", out.stem))
    c.setFillColor(INK)
    c.setFont("Sans-Bold", 44)
    c.drawString(MARGIN, H - MARGIN - 40, head.get("title", ""))
    c.setFillColor(MUTED)
    c.setFont("Sans", 20)
    c.drawString(MARGIN, H - MARGIN - 72, head.get("subtitle", ""))
    c.setStrokeColor(RULE)
    c.setLineWidth(0.8)
    for y in (H - MARGIN - HEAD + 4 * MM, MARGIN + foot - 6 * MM):
        c.line(MARGIN, y, W - MARGIN, y)

    for i, lines in enumerate(cites):
        x, y = MARGIN + i * (col_w + GUTTER), MARGIN + foot - 8 * MM
        for text, style, url in lines:
            font, size, color = CITE[style]
            y -= size * LEAD
            c.setFont(font, size)
            c.setFillColor(color)
            c.drawString(x, y, text)
            if url:
                w = pdfmetrics.stringWidth(text, font, size)
                c.linkURL(url, (x, y - 2, x + w, y + size), relative=0)
    c.setFont("Sans", 8)
    c.setFillColor(MUTED)
    c.drawRightString(W - MARGIN, MARGIN - 4,
                      "Cell areas are proportional to value. Drawn with voronoi-treemap, "
                      "github.com/jjmargolis/Skills; the area and reconciliation checks are in "
                      "each chart's proof.md.")
    c.save()

    writer = PdfWriter()
    sheet = writer.add_page(PdfReader(frame).pages[0])
    for page, (x, y) in zip(pages, corners):
        sheet.merge_transformed_page(page, Transformation().scale(scale).translate(x, y))
    writer.add_metadata({"/Title": head.get("title", out.stem)})
    writer.compress_identical_objects()
    with open(out, "wb") as f:
        writer.write(f)
    for f in tmp.iterdir():
        f.unlink()
    tmp.rmdir()
    orient = "landscape" if W > H else "portrait"
    print(f"wrote {out}: A2 {orient}, charts at {scale:.2f}x")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(*sys.argv[1:])
