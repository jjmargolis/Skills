#!/usr/bin/env python3
"""Compile an Obsidian vault into one read-only HTML page: a force-directed
graph of its notes with filters and a reader for each note.

    python3 build.py VAULT -o vault.html [--title NAME] [--exclude GLOB ...] [--hide-links PROPERTY ...]
                     [--glyph TYPE=SHAPE[:STYLE] ...]

Notes are the vault's .md files. Edges come from [[wikilinks]] and relative
markdown links in the body (kind "body") and from [[wikilinks]] inside
frontmatter properties (kind = the property name). Requires PyYAML.
"""
import argparse, fnmatch, json, os, posixpath, re, subprocess, sys
from datetime import date, datetime
from urllib.parse import unquote

import yaml

SKIP_DIRS = {".git", ".obsidian", ".trash", "node_modules", "__pycache__"}
FRONT = re.compile(r"\A---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|\Z)", re.S)
CODE = re.compile(r"(^```.*?^```[ \t]*$|^~~~.*?^~~~[ \t]*$|`[^`\n]+`)", re.S | re.M)
WIKI = re.compile(r"(!?)\[\[([^\]|#^]*)([#^][^\]|]*)?(?:\|([^\]]*))?\]\]")
MDLINK = re.compile(r"(!?)\[([^\]]*)\]\(<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\)")
H1 = re.compile(r"^#[ \t]+(.+?)[ \t#]*$", re.M)


def obsidian_ignores(vault):
    """Paths Obsidian itself leaves out: Excluded files (app.json) and the templates folder."""
    def load(name):
        try:
            with open(os.path.join(vault, ".obsidian", name), encoding="utf-8") as fh:
                return json.load(fh)
        except (OSError, ValueError):
            return {}
    rules = list(load("app.json").get("userIgnoreFilters", []))
    folder = load("templates.json").get("folder")
    if folder:
        rules.append(folder.strip("/") + "/")
    return rules


def ignored(rel, rules):
    for r in rules:
        if len(r) > 2 and r.startswith("/") and r.endswith("/"):
            if re.search(r[1:-1], rel):
                return True
        elif rel == r or rel.startswith(r if r.endswith("/") else r + "/"):
            return True
    return False


def scan(vault, excludes):
    """Yield vault-relative POSIX paths of every note."""
    rules = obsidian_ignores(vault)
    for root, dirs, files in os.walk(vault):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and not d.startswith("."))
        for f in sorted(files):
            if f.lower().endswith(".md"):
                rel = os.path.relpath(os.path.join(root, f), vault).replace(os.sep, "/")
                if not ignored(rel, rules) and not any(fnmatch.fnmatch(rel, g) for g in excludes):
                    yield rel


def plain(v):
    """Frontmatter value as JSON-safe data."""
    if isinstance(v, dict):
        return {str(k): plain(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [plain(x) for x in v]
    if isinstance(v, (date, datetime)):
        return v.isoformat()
    return v


class Resolver:
    """Obsidian's link resolution: full path first, then file name, nearest wins."""

    def __init__(self, paths):
        self.by_path, self.by_name, self.dirs = {}, {}, {}
        for i, p in enumerate(paths):
            stem = p[:-3].lower()
            self.by_path[stem] = i
            self.by_name.setdefault(posixpath.basename(stem), []).append(i)
            folder, name = posixpath.split(stem)
            if name in ("readme", "index"):
                self.dirs.setdefault(folder, i)
        self.paths = paths

    def wiki(self, target, src):
        t = target.strip().lower().removesuffix(".md")
        if not t:
            return src
        if t in self.by_path:
            return self.by_path[t]
        hits = [i for i in self.by_name.get(posixpath.basename(t), [])
                if self.paths[i][:-3].lower().endswith(t)]
        if not hits:
            return None
        here = posixpath.dirname(self.paths[src])
        return min(hits, key=lambda i: (posixpath.dirname(self.paths[i]) != here, len(self.paths[i])))

    def rel(self, href, src):
        if re.match(r"^[a-z][a-z0-9+.-]*:", href, re.I) or href.startswith("#"):
            return None
        path = unquote(href.split("#")[0].split("?")[0])
        if path.startswith("/"):
            full = path.lstrip("/")
        else:
            full = posixpath.normpath(posixpath.join(posixpath.dirname(self.paths[src]), path))
        key = full.lower().rstrip("/")
        key = "" if key == "." else key
        if key.endswith(".md"):
            return self.by_path.get(key[:-3])
        if key in self.by_path:
            return self.by_path[key]
        return self.dirs.get(key)


def rewrite(body, i, res, edges, missing):
    """Turn every note link into [text](#n=ID); drop links the page cannot follow."""

    def wiki(m):
        bang, target, frag, alias = m.groups()
        text = alias or (target.strip() + (frag or "").replace("#", " › ").replace("^", " › "))
        if bang and re.search(r"\.(png|jpe?g|gif|svg|webp|pdf|mp4|mp3)$", target, re.I):
            return f"*[{target.strip()}]*"
        j = res.wiki(target, i)
        if j is None:
            missing.add(target.strip())
            return f"<span class=missing>{text}</span>"
        if j != i:
            edges.add((i, j, "body"))
        return f"[{text}](#n={j})"

    def md(m):
        bang, text, href = m.groups()
        if bang:
            return f"*[{text or 'image'}]*"
        j = res.rel(href, i)
        if j is None:
            return m.group(0) if re.match(r"^(https?|mailto):", href, re.I) else text
        if j != i:
            edges.add((i, j, "body"))
        return f"[{text}](#n={j})"

    # Park code in placeholders so links inside it stay literal, while a link
    # whose text is code, [`spec.md`](spec.md), still matches.
    code = []
    def park(m):
        code.append(m.group(0))
        return f"\x00{len(code) - 1}\x00"
    body = MDLINK.sub(md, WIKI.sub(wiki, CODE.sub(park, body)))
    return re.sub(r"\x00(\d+)\x00", lambda m: code[int(m.group(1))], body)


def prop_links(props, i, res, edges):
    def walk(v, key):
        if isinstance(v, str):
            for m in WIKI.finditer(v):
                j = res.wiki(m.group(2), i)
                if j is not None and j != i:
                    edges.add((i, j, key))
        elif isinstance(v, list):
            for x in v:
                walk(x, key)
        elif isinstance(v, dict):
            for x in v.values():
                walk(x, key)
    for k, v in props.items():
        walk(v, k)


# Glyph library: each glyph is a list of (paint, path) parts in a [-1, 1] box.
# Paint "f" is a filled silhouette, "s" a stroked line. Drawn filled (settled)
# or outlined (open); the viewer's Fill control switches between them.
SHAPES = {
    "circle": [("f", "M1 0A1 1 0 1 1-1 0A1 1 0 1 1 1 0Z")],
    "square": [("f", "M-.85-.85H.85V.85H-.85Z")],
    "diamond": [("f", "M0-1.2L1.2 0 0 1.2-1.2 0Z")],
    "triangle": [("f", "M0-1.2L1.04 .6H-1.04Z")],
    "hexagon": [("f", "M.935 .54L0 1.08-.935 .54V-.54L0-1.08 .935-.54Z")],
    "plus": [("f", "M-.36-1.1H.36V-.36H1.1V.36H.36V1.1H-.36V.36H-1.1V-.36H-.36Z")],
    "hub": [("s", "M.9 0A.9 .9 0 1 1-.9 0A.9 .9 0 1 1 .9 0Z"), ("f", "M.42 0A.42 .42 0 1 1-.42 0A.42 .42 0 1 1 .42 0Z")],
    "question": [("s", "M-.5-.5C-.5-1.15 .55-1.15 .55-.5C.55-.05 0-.05 0 .4"), ("f", "M.2 .92A.2 .2 0 1 1-.2 .92A.2 .2 0 1 1 .2 .92Z")],
    "portico": [("f", "M-1.1-.4L0-1.15 1.1-.4Z M-.95-.25H-.55V.7H-.95Z M-.2-.25H.2V.7H-.2Z M.55-.25H.95V.7H.55Z M-1.1 .82H1.1V1.1H-1.1Z")],
    "flag": [("f", "M-.9-1.15H-.66V1.15H-.9Z M-.66-1.1L1.1-.6-.66-.1Z")],
    "book": [("f", "M-.08-.62C-.4-.95-.85-.95-1.15-.78V.85C-.85 .68-.4 .68-.08 .98Z M.08-.62C.4-.95 .85-.95 1.15-.78V.85C.85 .68 .4 .68 .08 .98Z")],
}

# Glyph for common `type` values: (shape, style). Types not listed take unused
# shapes in order of frequency; override with --glyph.
GLYPHS = {
    "map": ("hub", "fill"), "moc": ("hub", "fill"), "index": ("hub", "fill"),
    "spec": ("plus", "fill"), "report": ("square", "fill"), "design": ("hexagon", "fill"),
    "decision": ("diamond", "fill"), "question": ("question", "fill"), "risk": ("triangle", "fill"),
    "org": ("portico", "fill"), "company": ("flag", "fill"),
    "source": ("book", "fill"), "note": ("circle", "fill"),
}
STYLES = {"fill", "open"}


def glyph_arg(text):
    """Parse TYPE=SHAPE[:STYLE] from --glyph."""
    t, _, g = text.partition("=")
    shape, _, style = g.partition(":")
    if not t or shape not in SHAPES or (style or "fill") not in STYLES:
        raise argparse.ArgumentTypeError(f"expected TYPE=SHAPE[:STYLE], shape in {sorted(SHAPES)}, style in {sorted(STYLES)}")
    return t, (shape, style or "fill")


UPDATED_KEYS = ("updated", "modified", "last_updated", "last-updated", "date_modified")


def git_dates(vault):
    """Last commit date (YYYY-MM-DD) of every file under the vault, or {} outside git."""
    try:
        log = subprocess.run(["git", "-C", vault, "log", "--format=%x00%cs", "--name-only", "--relative", "--", "."],
                             capture_output=True, text=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        return {}
    dates = {}
    for block in log.split("\0")[1:]:
        day, *files = block.strip().split("\n")
        for f in files:
            if f:
                dates.setdefault(f.strip('"'), day)  # log runs newest first
    return dates


def updated(props, path, vault, dates):
    """Last-updated date: a frontmatter property, else the last commit, else the file's mtime."""
    for k in UPDATED_KEYS:
        if props.get(k):
            return str(props[k])[:10]
    if path in dates:
        return dates[path]
    return date.fromtimestamp(os.path.getmtime(os.path.join(vault, path))).isoformat()


def build(vault, excludes):
    paths = list(scan(vault, excludes))
    res = Resolver(paths)
    notes, edges, dates = [], set(), git_dates(vault)
    for i, p in enumerate(paths):
        with open(os.path.join(vault, p), encoding="utf-8", errors="replace") as fh:
            text = fh.read()
        props, m = {}, FRONT.match(text)
        if m:
            try:
                loaded = yaml.safe_load(m.group(1))
                props = plain(loaded) if isinstance(loaded, dict) else {}
            except yaml.YAMLError as e:
                print(f"warning: bad frontmatter in {p}: {e.__class__.__name__}", file=sys.stderr)
            text = text[m.end():]
        missing = set()
        body = rewrite(text, i, res, edges, missing)
        prop_links(props, i, res, edges)
        h1 = H1.search(CODE.sub("", body))
        name = posixpath.basename(p)[:-3]
        aliases = props.get("aliases") or []
        alias = aliases[0] if isinstance(aliases, list) and aliases else aliases if isinstance(aliases, str) else ""
        generic = name.lower() in ("readme", "index")
        title = str(props.get("title") or (h1.group(1) if h1 else "") or alias
                    or (posixpath.basename(posixpath.dirname(p)) if generic else "") or name)
        if h1 and h1.group(1) == title:  # the reader prints the title; drop the duplicate
            body = body.replace(h1.group(0), "", 1)
        notes.append({"p": p, "t": title, "f": posixpath.dirname(p), "y": str(props.get("type", "")),
                      "m": props, "b": body, "u": sorted(missing),
                      "d": updated(props, p, vault, dates)})
    links = [[s, t, k] for s, t, k in sorted(edges)]
    return {"notes": notes, "links": links}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("vault")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--title", help="page title (default: the vault folder's name)")
    ap.add_argument("--hide-links", action="append", default=[], metavar="PROPERTY",
                    help="property whose links start hidden (the viewer can show them); repeatable")
    ap.add_argument("--glyph", action="append", default=[], type=glyph_arg, metavar="TYPE=SHAPE[:STYLE]",
                    help=f"glyph for a note type, e.g. person=triangle:open; shapes: {', '.join(SHAPES)}; repeatable")
    ap.add_argument("--exclude", action="append", default=[], help="glob on vault-relative paths; repeatable")
    a = ap.parse_args()
    vault = os.path.abspath(a.vault)
    data = build(vault, a.exclude)
    data["hide"] = a.hide_links
    data["glyphs"] = {**GLYPHS, **dict(a.glyph)}
    data["shapes"] = SHAPES
    title = a.title or os.path.basename(vault.rstrip("/"))
    blob = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    template = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "viewer.html"), encoding="utf-8").read()
    esc = title.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    html = template.replace("__TITLE__", esc).replace("__DATA__", blob)
    with open(a.out, "w", encoding="utf-8") as fh:
        fh.write(html)
    n, e = len(data["notes"]), len(data["links"])
    print(f"{n} notes, {e} links, {len(html) / 1e6:.1f} MB -> {a.out}")
    if len(html) > 15e6:
        print("warning: over the 16 MB artifact limit; use --exclude", file=sys.stderr)


if __name__ == "__main__":
    main()
