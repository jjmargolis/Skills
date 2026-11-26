---
name: obsidian-graph
description: Compile an Obsidian vault into one read-only HTML page (touch-friendly force graph, filters, note reader with links and backlinks) and publish it as a private artifact. Use when asked to view, browse or refresh a vault's graph.
---

# Obsidian graph

The page is a snapshot of an Obsidian vault: a force-directed graph of every note that can be dragged, panned and pinch-zoomed, filters by folder, `type`, any frontmatter property and search text, a Files sidebar with the vault's folder tree, a Labels toggle that names every node, and a reader that shows a tapped note's properties, rendered text, links and backlinks, with navigation between notes and a Reset button that closes the note and fits the whole graph back in view. `build.py` writes it from the vault; `viewer.html` is the page template. The page is read-only; to update it, rebuild and republish.

## Steps

1. **Get the vault.** A git repo: clone or pull it. A folder on the person's computer: stage the `.md` files into the container with the device tools, keeping the folder structure. Attachments are not needed.
2. **Build.**
   ```bash
   python3 build.py VAULT -o vault.html --title "Name" [--exclude "archive/*" ...]
   ```
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

Each note shows its last-updated date: an `updated` (or `modified`, `last_updated`) property if set, else the file's last git commit, else its modification time. Node size follows backlinks, the distinct notes that link to it, so a note many others cite is large and a note that only cites others stays small. Links to images and other files render as plain text, since the page cannot load them. A note's title is its `title` property, else its first `# heading`, else its file name (a `README` takes its folder's name).

## Style

Text panels follow carovision: Times body (Tinos as the web fallback), Libre Bodoni Bold titles, small-caps labels, hairline rules, black on white, inverted in dark mode. The graph is ink only: node size by backlinks, the selected note ringed with its neighbours in full ink and the rest faded, labels shown when zoomed in.

## Rules

- Read-only: the page never edits notes, and says nothing about saving.
- Keep the page self-contained: data inline, libraries from jsDelivr pinned to exact versions (force-graph, marked, DOMPurify).
- Note bodies are sanitised with DOMPurify before rendering; external links open in a new tab.
- Tested at 2,000 notes and 7,000 links: 60 fps on a phone-sized viewport.

Requires Python 3.9+ and PyYAML.
