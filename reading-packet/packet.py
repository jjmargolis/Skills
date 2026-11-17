#!/usr/bin/env python3
"""Bind excerpts from several PDFs into one reading packet.

The manifest is a TOML file:

    title = "Packet title"
    subtitle = "One line under the title"
    date = "2026-11-17"
    source_dir = "src"            # relative to the manifest; optional
    output = "packet.pdf"         # relative to the manifest; optional
    image_dpi = 150               # downsample images above this; optional

    [pace]                        # pages read per hour, by kind; optional
    standard = 25
    guide = 40
    math = 12

    [[reading]]
    title = "MIL-HDBK-1388, Logistic Support Analysis"
    source = "US Army Materiel Command, draft 1994"
    file = "mil-hdbk-1388.pdf"
    pages = "3,5-6,9-12"          # PDF page numbers, 1-based; "all" for the whole file
    kind = "standard"             # key into [pace]
    why = "Why this reading matters."
    link = "https://..."
    note = "Optional caveat shown on the divider page."
    section = "Stage 1. The record"   # optional; starts a new part in the contents

Each reading gets a divider page (title, source, pages taken, estimated
time, why it matters, link), then its pages, each stamped with the packet
page, the reading number and the source page. The packet opens with a
cover and a contents page, and carries PDF bookmarks for every reading.

Usage: python3 packet.py manifest.toml [--check]
  --check  prints the page plan and time per reading without writing a PDF.
"""

import argparse
import html
import sys
import tomllib
from pathlib import Path

import pymupdf

LETTER = pymupdf.paper_rect("letter")
DEFAULT_PACE = {"standard": 25, "guide": 40, "report": 40, "math": 12, "paper": 15}
CSS = """
* { font-family: serif; color: #1a1a1a; }
h1 { font-size: 26pt; margin: 0 0 6pt 0; }
h2 { font-size: 18pt; margin: 0 0 10pt 0; }
p, li, td { font-size: 11pt; line-height: 1.35; }
.k { font-size: 9pt; color: #666; text-transform: uppercase; letter-spacing: 1pt; }
.m { font-size: 10pt; color: #444; }
.sec td { font-size: 10pt; font-weight: bold; padding-top: 8pt; }
td { padding: 2pt 6pt 2pt 0; vertical-align: top; }
a { color: #1a4f8b; }
"""


def parse_pages(spec: str, n: int) -> list[int]:
    """Turn "3,5-6,9-12" into 0-based page indexes, checked against n pages."""
    if spec.strip().lower() == "all":
        return list(range(n))
    out = []
    for part in spec.split(","):
        part = part.strip()
        a, _, b = part.partition("-")
        lo, hi = int(a), int(b or a)
        if not 1 <= lo <= hi <= n:
            raise ValueError(f"page range {part} outside 1-{n}")
        out.extend(range(lo - 1, hi))
    return out


def ranges(idx: list[int]) -> str:
    """Compress 0-based indexes back into a 1-based "3, 5-6" string."""
    out, start = [], None
    for i, p in enumerate(idx):
        if start is None:
            start = p
        if i + 1 == len(idx) or idx[i + 1] != p + 1:
            out.append(f"{start + 1}" if start == p else f"{start + 1}–{p + 1}")
            start = None
    return ", ".join(out)


def minutes(n_pages: int, kind: str, pace: dict) -> int:
    per_hour = pace.get(kind, pace["guide"])
    return max(5, round(n_pages / per_hour * 60 / 5) * 5)


def fmt_time(m: int) -> str:
    return f"{m} min" if m < 60 else f"{m // 60} h {m % 60:02d} min".replace(" 00 min", "")


def text_page(doc: pymupdf.Document, body: str) -> None:
    page = doc.new_page(width=LETTER.width, height=LETTER.height)
    box = pymupdf.Rect(72, 72, LETTER.width - 72, LETTER.height - 72)
    spare, _ = page.insert_htmlbox(box, body, css=CSS)
    if spare < 0:
        raise ValueError("text does not fit on one page; shorten it")


def stamp(page: pymupdf.Page, label: str) -> None:
    r = page.rect
    # Stamp in the bottom margin, rotated pages included.
    box = pymupdf.Rect(r.x0 + 18, r.y1 - 16, r.x1 - 18, r.y1 - 4) * page.derotation_matrix
    page.insert_textbox(box, label, fontsize=6.5, fontname="helv", color=(0.45, 0.45, 0.45),
                        align=pymupdf.TEXT_ALIGN_RIGHT, rotate=page.rotation)


def build(manifest: Path, check: bool) -> None:
    cfg = tomllib.loads(manifest.read_text(encoding="utf-8"))
    base = manifest.parent
    src = base / cfg.get("source_dir", ".")
    pace = {**DEFAULT_PACE, **cfg.get("pace", {})}
    readings = cfg["reading"]

    plan = []
    for n, r in enumerate(readings, 1):
        doc = pymupdf.open(src / r["file"])
        idx = parse_pages(str(r.get("pages", "all")), len(doc))
        mins = minutes(len(idx), r.get("kind", "guide"), pace)
        plan.append((n, r, doc, idx, mins))
        print(f"{n:2d}. {len(idx):3d} pp {fmt_time(mins):>12}  {r['title'][:70]}")
    total = sum(p[4] for p in plan)
    print(f"    {sum(len(p[3]) for p in plan)} pages, {fmt_time(total)}")
    if check:
        return

    out = pymupdf.open()
    # Cover and contents come first; their page count is fixed at 2 so that
    # packet page numbers can be computed before the contents are written.
    front = 2
    starts, cursor = [], front
    for n, r, doc, idx, mins in plan:
        starts.append(cursor + 1)          # divider page, 1-based
        cursor += 1 + len(idx)

    e = html.escape
    text_page(out, f"""
      <p class="k">Reading packet</p>
      <h1>{e(cfg['title'])}</h1>
      <p class="m">{e(cfg.get('subtitle', ''))}</p>
      <p class="m">{e(cfg.get('date', ''))} · {len(plan)} readings · {cursor - front - len(plan)} source pages ·
      about {fmt_time(total)}</p>
      <p>{e(cfg.get('intro', ''))}</p>""")

    rows, last_section = [], None
    for (n, r, doc, idx, mins), start in zip(plan, starts):
        if r.get("section") and r["section"] != last_section:
            last_section = r["section"]
            rows.append(f'<tr class="sec"><td colspan="3">{e(last_section)}</td></tr>')
        rows.append(f"<tr><td>{n}.</td><td>{e(r['title'])}<br/><span class='m'>{e(r['source'])}</span></td>"
                    f"<td class='m'>p.&nbsp;{start}<br/>{fmt_time(mins)}</td></tr>")
    text_page(out, f"<h2>Contents</h2><table>{''.join(rows)}</table>")

    toc = [[1, "Cover", 1], [1, "Contents", 2]]
    for (n, r, doc, idx, mins), start in zip(plan, starts):
        note = f"<p class='m'><b>Note.</b> {e(r['note'])}</p>" if r.get("note") else ""
        link = f"<p class='m'>Source: <a href='{e(r['link'])}'>{e(r['link'])}</a></p>" if r.get("link") else ""
        text_page(out, f"""
          <p class="k">Reading {n}{' · ' + e(r['section']) if r.get('section') else ''}</p>
          <h2>{e(r['title'])}</h2>
          <p class="m">{e(r['source'])}</p>
          <p class="m">Pages {ranges(idx)} of {len(doc)} · {len(idx)} pages · about {fmt_time(mins)}</p>
          <p>{e(r.get('why', ''))}</p>{note}{link}""")
        toc.append([1, f"{n}. {r['title']}", start])
        # Insert each reading in one call so shared fonts and images are
        # copied once, not once per page.
        first = len(out)
        sub = pymupdf.open()
        sub.insert_pdf(doc, links=False, annots=False)
        sub.select(idx)
        out.insert_pdf(sub, links=False, annots=False)
        for k, i in enumerate(idx):
            stamp(out[first + k], f"Packet p. {start + k + 1}  ·  Reading {n}  ·  source p. {i + 1}")
    out.set_toc(toc)
    out.set_metadata({"title": cfg["title"], "subject": cfg.get("subtitle", "")})
    if cfg.get("image_dpi"):
        # Downsample scans and photos above the target resolution to keep
        # the packet small enough to sync and read on a phone.
        dpi = int(cfg["image_dpi"])
        out.rewrite_images(dpi_threshold=dpi + 20, dpi_target=dpi, quality=80)
    dest = base / cfg.get("output", "packet.pdf")
    out.save(dest, garbage=4, deflate=True, use_objstms=1)
    print(f"wrote {dest} ({len(out)} pages, {dest.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("manifest", type=Path)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    try:
        build(a.manifest, a.check)
    except (ValueError, FileNotFoundError, KeyError) as err:
        sys.exit(f"error: {err}")
