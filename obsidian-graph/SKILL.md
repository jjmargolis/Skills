---
name: obsidian-graph
description: Compile an Obsidian vault into one read-only HTML page (touch-friendly force graph, filters, note reader with links and backlinks) and publish it as a private artifact. Use when asked to view, browse or refresh a vault's graph.
---

# Obsidian graph

The page is a snapshot of an Obsidian vault: a force-directed graph of every note that can be dragged, panned and pinch-zoomed, glyphs chosen by `type` or another property, filters by folder, glyph value, any frontmatter property and search text, a Files sidebar with the vault's folder tree, a Labels toggle that names every node, and a reader that shows a tapped note's properties, rendered text, links and backlinks, with navigation between notes and a Close button (×, or Escape) that closes the note and leaves the view where it is; Reset in the header zooms out to the whole graph. Toolbar buttons are icons with labels for touch and screen readers. `build.py` writes it from the vault; `viewer.html` is the page template. The page is read-only; to update it, rebuild and republish.

## Steps

1. **Get the vault.** A git repo: clone or pull it. A folder on the person's computer: stage the `.md` files into the container with the device tools, keeping the folder structure. Attachments are not needed.
2. **Build.**
   ```bash
   python3 build.py VAULT -o vault.html --title "Name" [--exclude "archive/*" ...]
   ```
   It skips what Obsidian skips: the folders in Settings › Files and links › Excluded files and the templates folder, both read from `.obsidian/`. `--hide-links up` starts a property's links hidden (the Links filter can show them); use it for a property every note carries, such as a parent map, which otherwise lays a tree over the real graph.
   It prints notes, links and size. Over about 15 MB, exclude bulky folders (source dumps, archives) with `--exclude`.
3. **Publish.** Publish `vault.html` with the Artifact tool, icon `graph`. To refresh a page published in an earlier conversation, find its URL with `action: "list"` (the title is the `--title` value), read it, and publish with that `url` so the link stays the same.
4. **Check once.** Note the counts in the reply: notes, links, unresolved links if many.

## What counts as a link

| Source | Edge kind | Drawn |
|---|---|---|
| `[[note]]`, `[[note\|alias]]`, `[[note#heading]]` in the body | body | solid |
| `[text](relative/path.md)` in the body; a link to a folder resolves to its `README.md` or `index.md` | body | solid |
| `[[note]]` inside a frontmatter property value | the property's name | dashed, named in the reader |

Resolution follows Obsidian: exact path first, then file name, preferring the same folder, then the shortest path. Unresolved links are listed at the foot of the note.

Each note shows its last-updated date: an `updated` (or `modified`, `last_updated`) property if set, else the file's last git commit, else its modification time. Node size follows backlinks, the distinct notes that link to it, so a note many others cite is large and a note that only cites others stays small. Links to images and other files render as plain text, since the page cannot load them. A note's title is its `title` property, else its first `# heading`, else its first alias, else its file name (a `README` or `index` takes its folder's name).

## Glyphs

Each note is drawn as a vector glyph. The Glyphs controls in Filters set three things:

| Control | Choices | Effect |
|---|---|---|
| Shape | `type`, or any property with 2 to 12 values | One glyph per value; its legend chips hide or show that value, with Show all and Hide all |
| Fill | by shape, or a second such property | Each value drawn filled or outlined; values like open, draft and proposed start outlined; tap to switch |
| Size | backlinks, all links, equal | Node radius |

`type` values have fixed glyphs: map (ring and dot), spec (cross), report (square), design (hexagon), decision (diamond), question (question mark), risk (triangle), org (columned building), company (flag), source (open book), note (circle). Other values take the simplest unused shapes, filled and then outlined; notes without a value are a grey dot. `--glyph person=triangle:open` sets a type's glyph; the shape library is `SHAPES` in `build.py`, each glyph a list of filled and stroked SVG paths in a [-1, 1] box.

## Style

Text panels follow carovision: Times body (Tinos as the web fallback), Libre Bodoni Bold titles, small-caps labels, hairline rules, black on white, inverted in dark mode. The graph is ink only: glyphs as above, node size by backlinks, the selected note ringed with its neighbours in full ink and the rest faded, labels shown when zoomed in.

## Rules

- Read-only: the page never edits notes, and says nothing about saving.
- Keep the page self-contained: data inline, libraries from jsDelivr pinned to exact versions (force-graph, marked, DOMPurify).
- Note bodies are sanitised with DOMPurify before rendering; external links open in a new tab.
- Tested on a 363-note vault with 1,088 links and at 2,000 notes and 7,000 links: 60 fps on a phone-sized viewport.

Requires Python 3.9+ and PyYAML.
