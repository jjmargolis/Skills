#!/usr/bin/env python3
"""Compile an Obsidian vault into one read-only HTML page: a force-directed
graph of its notes with filters and a reader for each note.

    python3 build.py VAULT -o vault.html [--title NAME] [--exclude GLOB ...] [--hide-links PROPERTY ...]

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
        title = str(props.get("title") or (h1.group(1) if h1 else "") or name)
        if h1 and h1.group(1) == title:  # the reader prints the title; drop the duplicate
            body = body.replace(h1.group(0), "", 1)
        if name.lower() in ("readme", "index") and not props.get("title") and not h1:
            title = posixpath.basename(posixpath.dirname(p)) or name
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
    ap.add_argument("--exclude", action="append", default=[], help="glob on vault-relative paths; repeatable")
    a = ap.parse_args()
    vault = os.path.abspath(a.vault)
    data = build(vault, a.exclude)
    data["hide"] = a.hide_links
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
