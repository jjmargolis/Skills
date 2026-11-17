---
name: reading-packet
description: Bind excerpts from several PDFs into one reading packet with a cover, contents, a divider page per reading, source-page stamps and bookmarks. Use when asked for a course pack, reading packet or bound excerpts.
---

# Reading packet

A reading packet is one PDF made of excerpts from several source PDFs, in a set order, sized so each reading fits a time budget. `packet.py` builds it from a TOML manifest.

## Steps

1. **Collect the sources** into one folder. Download what is public; for sites that refuse scripts, use files the person saved (Drive, a synced folder) or a browser. Print a web page to PDF with Playwright (`page.pdf`, Letter, 0.6 in margins).
2. **Map each source.** `pymupdf.open(f).get_toc()` gives chapter starts as PDF pages when the file has bookmarks. Without them, find chapter boundaries from running headers or footers, and figures from their captions (`Figure 3-2`, `Fig 4`). For scanned files with no text layer, render the contents pages and work out the offset between printed and PDF page numbers from two known pages.
3. **Look before choosing.** Render a contact sheet of the candidate range (pages at about 60 dpi in a grid, page numbers in red) and read it. It shows figure pages, blank pages from failed scans, and where a section really starts.
4. **Choose pages to a time budget.** Pages an hour: standards and handbooks 25, guides and reports 40, papers 15, mathematical text 12, mostly graphics 100. Take the whole document when it fits; otherwise take the chapters that carry the argument, plus the charts and diagrams worth keeping from elsewhere in the source. Drop pages whose figures did not survive and say so in a note.
5. **Write the manifest** (format in the docstring of `packet.py`). Every reading has `title`, `source`, `file`, `pages`, `kind` and `why`; `link`, `note` and `section` are optional. `why` says what this excerpt gives the reader, not what the source is.
6. **Check, then build.** `python3 packet.py manifest.toml --check` prints pages and time per reading; fix any reading over budget. Then run without `--check`. Set `image_dpi = 150` in the manifest when the packet is over about 20 MB; scans stay legible at 150.
7. **Inspect the result.** Render the cover, contents, one divider and a stamped figure page. Confirm the bookmarks with `get_toc()`.

## What the packet contains

- Cover with title, subtitle, date, reading count, page count and total time, and an intro paragraph from the manifest.
- Contents grouped by `section`, with the packet page and time for each reading.
- For each reading, a divider page (source, pages taken out of the total, time, why, note, link), then the pages, each stamped in the bottom margin with the packet page, reading number and source page.
- PDF bookmarks for the cover, contents and every reading.

## Rules

- Excerpts stay faithful: whole pages, in source order, never edited.
- Say on the divider page what is missing and why (failed scan, paywall, site down).
- Keep the manifest beside the packet so it can be rebuilt or extended.
- Large packets: the Drive connector takes about 3 MB, and a device file copy about 25 MB.

Requires `pymupdf` (`pip install pymupdf`) and Python 3.11 or later for `tomllib`.
