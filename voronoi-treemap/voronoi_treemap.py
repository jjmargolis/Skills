#!/usr/bin/env python3
"""Circular Voronoi treemap: a disc cut into convex cells whose areas are
proportional to value, nested by group (and optionally subgroup).

    python voronoi_treemap.py data.csv        ->  data.png, data.svg

CSV columns: group,label,value  or  group,subgroup,label,value.
Lines starting with '#' are 'key: value' metadata: title, subtitle, source,
as_of, prefix (e.g. $), scale (number one CSV unit stands for, e.g. 1e6).
"""
import csv
import functools
import itertools
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties
from matplotlib.textpath import TextPath

# Page geometry, in points. One data unit is one point, so font sizes and
# cell sizes share a unit and label fit is exact.
W, R, MARGIN = 780, 265, 36
RIM_N = 360               # disc as a regular polygon: 0.005% short of a circle
SPLIT_TOL = 3e-4          # relative area error allowed in one subdivision
LEAF_TOL = 1e-3           # relative area error allowed on a finished leaf
F_MAX, F_MIN, PAD, PITCH = 15.0, 4.5, 1.5, 1.18
INK, MUTED = "#1a1a19", "#5f5e58"
STROKE = (0.6, 1.5, 2.8)  # leaf, subgroup, group
# Group colours in fixed order (never cycled): fill tint, arc colour.
PALETTE = [("#ea7676", "#e34948"), ("#5f9ae0", "#2a78d6"), ("#f2b840", "#eda100"),
           ("#ee9cbb", "#e87ba4"), ("#40a240", "#008300"), ("#897ce0", "#6250d6"),
           ("#54c39b", "#1baf7a"), ("#f08e67", "#eb6834")]
REG, BOLD = FontProperties(family="DejaVu Sans"), FontProperties(family="DejaVu Sans", weight="bold")


# ---------- geometry ----------

def area(p):
    x, y = p[:, 0], p[:, 1]
    return 0.5 * abs(x @ np.roll(y, -1) - y @ np.roll(x, -1))


def centroid(p):
    x, y = p[:, 0], p[:, 1]
    xn, yn = np.roll(x, -1), np.roll(y, -1)
    c = x * yn - xn * y
    return np.array([((x + xn) * c).sum(), ((y + yn) * c).sum()]) / (3 * c.sum())


def clip(p, n, d):
    """Part of convex polygon p where n.x <= d. The kept vertices of a convex
    polygon form one cyclic run, so the cut adds exactly two points."""
    if len(p) == 0:
        return p
    s = p @ n - d
    inside = s <= 0
    if inside.all():
        return p
    if not inside.any():
        return p[:0]
    k = len(p)
    first = np.flatnonzero(inside & ~np.roll(inside, 1))[0]
    run = (first + np.arange(inside.sum())) % k
    a, b = (run[0] - 1) % k, run[0]
    c, e = run[-1], (run[-1] + 1) % k
    cut = lambda i, j: p[i] + (p[j] - p[i]) * s[i] / (s[i] - s[j])
    return np.vstack([cut(a, b), p[run], cut(c, e)])


def power_cells(P, S, w):
    """Cell i = points of P whose power distance |x-s_i|^2 - w_i is smallest."""
    sq = (S ** 2).sum(1)
    cells = []
    for i in range(len(S)):
        c = P
        for j in np.argsort(((S - S[i]) ** 2).sum(1))[1:]:
            c = clip(c, 2 * (S[j] - S[i]), sq[j] - sq[i] + w[i] - w[j])
        cells.append(c)
    return cells


def split(P, targets, rng):
    """Cut convex polygon P into convex cells with the given areas."""
    k = len(targets)
    if k == 1:
        return [P]
    lo, hi = P.min(0), P.max(0)
    edges = np.roll(P, -1, 0) - P
    S = np.empty((0, 2))
    while len(S) < k:  # seeded random points inside P
        x = rng.uniform(lo, hi)
        if (edges[:, 0] * (x - P)[:, 1] - edges[:, 1] * (x - P)[:, 0] >= 0).all():
            S = np.vstack([S, x])
    w = np.zeros(k)
    for it in range(4000):
        cells = power_cells(P, S, w)
        A = np.array([area(c) if len(c) > 2 else 0.0 for c in cells])
        if np.abs(A / targets - 1).max() < SPLIT_TOL:
            return cells
        if it < 150:  # Lloyd steps round the cells; then sites stay fixed
            S = np.array([centroid(c) if a > 0 else s for c, a, s in zip(cells, A, S)])
        w += 0.5 * (targets - A)  # concave ascent: grow cells that are too small
    raise RuntimeError(f"layout did not reach {SPLIT_TOL:.0e} for a {k}-way split")


def rim_runs(p, c):
    """Angular intervals (start, end), end > start, where polygon p lies on the rim."""
    rad = np.hypot(*(p - c).T)
    on = rad > R * (1 - 1e-4)
    nxt = np.roll(np.arange(len(p)), -1)
    chord = 2 * R * np.sin(np.pi / RIM_N) * 1.01
    edge = on & on[nxt] & (np.hypot(*(p[nxt] - p).T) <= chord)
    if edge.all():
        return [(0.0, 2 * np.pi)]
    ang = np.arctan2(p[:, 1] - c[1], p[:, 0] - c[0])
    runs, start = [], np.flatnonzero(edge & ~np.roll(edge, 1))
    for i in start:
        j = i
        while edge[j]:
            j = (j + 1) % len(p)
        a, b = ang[i], ang[j]
        runs.append((a, b + 2 * np.pi if b <= a else b))
    return runs


# ---------- data ----------

class Node:
    def __init__(self, name):
        self.name, self.children, self.value, self.poly = name, [], 0.0, None

    def child(self, name):
        for c in self.children:
            if c.name == name:
                return c
        self.children.append(Node(name))
        return self.children[-1]

    def leaves(self):
        return [self] if not self.children else [l for c in self.children for l in c.leaves()]


def read(path):
    meta, rows = {}, []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.startswith("#"):
            key, _, val = line[1:].partition(":")
            meta[key.strip()] = val.strip()
        elif line.strip():
            rows.append(line)
    header, *data = csv.reader(rows)
    if len(header) not in (3, 4):
        sys.exit("CSV needs columns group,label,value or group,subgroup,label,value")
    root = Node("")
    for *path_, value in data:
        node = root
        for name in path_:
            node.value += float(value)
            node = node.child(name.strip())
        if node.value or float(value) <= 0:
            sys.exit(f"duplicate or non-positive row: {path_}")
        node.value = float(value)
    if len(root.children) > len(PALETTE):
        sys.exit(f"{len(root.children)} groups; the palette distinguishes {len(PALETTE)}. Merge groups.")
    return meta, root, len(header) - 1


def layout(node, rng):
    if node.children:
        t = area(node.poly) * np.array([c.value for c in node.children]) / node.value
        for c, poly in zip(node.children, split(node.poly, t, rng)):
            c.poly = poly
            layout(c, rng)


# ---------- text ----------

@functools.lru_cache(None)
def width(s, bold=False):
    return TextPath((0, 0), s, size=1, prop=BOLD if bold else REG).get_extents().width if s.strip() else 0.0


def fit(poly, lines):
    """Largest font size at which the centred block of lines stays inside the
    convex polygon, PAD clear of every edge."""
    c = centroid(poly)
    e = np.roll(poly, -1, 0) - poly
    length = np.hypot(*e.T)
    keep = length > 1e-9
    n = np.c_[e[:, 1], -e[:, 0]][keep] / length[keep, None]  # outward normals
    slack = ((poly[keep] - c) * n).sum(1) - PAD
    half_w, half_h = max(width(*l) for l in lines) / 2, len(lines) * PITCH / 2
    return (slack / (np.abs(n[:, 0]) * half_w + np.abs(n[:, 1]) * half_h)).min()


def wraps(words, max_lines):
    for m in range(1, min(max_lines, len(words)) + 1):
        for cuts in itertools.combinations(range(1, len(words)), m - 1):
            b = [0, *cuts, len(words)]
            yield [" ".join(words[i:j]) for i, j in zip(b, b[1:])]


def wrap_to(s, size, max_w, bold=False):
    lines, cur = [], ""
    for word in s.split():
        if cur and width(cur + " " + word, bold) * size > max_w:
            lines.append(cur)
            cur = word
        else:
            cur = (cur + " " + word).strip()
    return lines + [cur]


def money(v, meta):
    x = v * float(meta.get("scale", 1))
    for div, suf in ((1, ""), (1e3, "k"), (1e6, "m"), (1e9, "bn"), (1e12, "tn")):
        r = float(f"{x / div:.3g}")
        if r < 1000:
            break
    return f"{meta.get('prefix', '')}{r:g}{suf}"


# ---------- drawing ----------

def spread(items, lo, hi, gap=4):
    """Move label centres y apart vertically, keeping order, within [lo, hi]."""
    items.sort(key=lambda d: -d["y"])
    top = hi
    for d in items:
        d["y"] = min(d["y"], top - d["h"] / 2)
        top = d["y"] - d["h"] / 2 - gap
    bottom = lo
    for d in reversed(items):
        d["y"] = max(d["y"], bottom + d["h"] / 2)
        bottom = d["y"] + d["h"] / 2 + gap


def main(path):
    meta, root, depth = read(path)
    rng = np.random.default_rng(0)
    c0 = np.zeros(2)
    th = 2 * np.pi * np.arange(RIM_N) / RIM_N
    root.poly = R * np.c_[np.cos(th), np.sin(th)]
    layout(root, rng)
    disc = area(root.poly)
    err = max(abs(area(l.poly) / (disc * l.value / root.value) - 1) for l in root.leaves())
    assert err < LEAF_TOL, err

    # Leaf labels: name + bold value at the largest size that fits; else a key number.
    key, n_key, tiers = [], 0, [0, 0, 0]
    texts = []  # (x, y, string, size, bold, colour, ha)
    for g in root.children:
        g_lines = []
        for sub in (g.children if depth == 3 else [g]):
            s_lines = []
            for leaf in sub.leaves():
                val, c = money(leaf.value, meta), centroid(leaf.poly)
                best = max(((fit(leaf.poly, [(s, False) for s in w] + [(val, True)]), -len(w), w)
                            for w in wraps(leaf.name.split(), 3)), key=lambda t: t[:2])
                f, lines = min(best[0], F_MAX), [(s, False) for s in best[2]] + [(val, True)]
                if f < F_MIN:
                    f = fit(leaf.poly, [(str(n_key + 1), False)])
                    mark = "·"
                    if f >= F_MIN:
                        n_key += 1
                        mark = str(n_key)
                        lines, f = [(mark, False)], min(f, 7.0)
                    else:
                        lines = []
                    tiers[1 if lines else 2] += 1
                    s_lines.append((f"{mark}  {leaf.name}  {val}", False))
                else:
                    tiers[0] += 1
                for i, (s, bold) in enumerate(lines):
                    y = c[1] + ((len(lines) - 1) / 2 - i) * PITCH * f
                    texts.append((c[0], y, s, f, bold, INK, "center"))
            sub.arc = max(rim_runs(sub.poly, c0), key=lambda r: r[1] - r[0], default=None)
            if depth == 3 and (s_lines or sub.arc is None):
                head = f"{sub.name}  {money(sub.value, meta)}"
                if sub.arc is None:  # no rim arc to carry the name: list members here
                    head += ": " + ", ".join(l.name for l in sub.leaves())
                g_lines += [(head, False)] + [("   " + s, b) for s, b in s_lines]
            else:
                g_lines += s_lines
        g.arc = max(rim_runs(g.poly, c0), key=lambda r: r[1] - r[0], default=None)
        if g_lines or g.arc is None:
            key += [(f"{g.name}  {money(g.value, meta)}", True)] + g_lines

    # Key under the disc: one column up to 12 lines, then three.
    col_w, key_f = (W - 2 * MARGIN - 2 * 18) / 3, 6.5
    key_lines = []
    for s, bold in key:
        indent = len(s) - len(s.lstrip())
        for i, part in enumerate(wrap_to(s, key_f, col_w - 8, bold)):
            key_lines.append(((" " * indent if i == 0 else "      ") + part, bold))
    rows = max(12, -(-len(key_lines) // 3))  # lines per column
    key_h = min(rows, len(key_lines)) * key_f * 1.4 + (20 if key_lines else 0)

    r_sub, r_grp = R + 7, R + (15 if depth == 3 else 7)
    r_lab = r_grp + 20
    wrap_w = W / 2 - r_lab - 16  # room beside the disc at its widest
    top = 100 if meta.get("subtitle") else 76
    H = top + 2 * (r_lab + 30) + key_h + 44
    cy = H - top - (r_lab + 30)
    centre = np.array([W / 2, cy])

    fig = plt.figure(figsize=(W / 72, H / 72))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set(xlim=(0, W), ylim=(0, H))
    ax.axis("off")
    put = lambda x, y, s, size, bold=False, color=INK, ha="left", va="center": ax.text(
        x, y, s, fontsize=size, fontproperties=BOLD if bold else REG, color=color, ha=ha, va=va)

    put(MARGIN, H - 44, meta.get("title", ""), 20, True)
    put(MARGIN, H - 70, meta.get("subtitle", ""), 10.5, color=MUTED)
    source = " · ".join(filter(None, [meta.get("source") and "Source: " + meta["source"],
                                      meta.get("as_of") and "as of " + meta["as_of"]]))
    put(MARGIN, 20, source, 6.5, color=MUTED)

    # Cells, then heavier white strokes for each level above.
    for gi, g in enumerate(root.children):
        for leaf in g.leaves():
            ax.fill(*(leaf.poly + centre).T, fc=PALETTE[gi][0], ec="white", lw=STROKE[0], joinstyle="round")
    for g in root.children:
        if depth == 3:
            for sub in g.children:
                ax.fill(*(sub.poly + centre).T, fc="none", ec="white", lw=STROKE[1], joinstyle="round")
        ax.fill(*(g.poly + centre).T, fc="none", ec="white", lw=STROKE[2], joinstyle="round")
    for x, y, s, f, bold, color, ha in texts:
        put(x + centre[0], y + centre[1], s, f, bold, color, ha)

    # Dimension arcs outside the rim: subgroups on the inner ring, groups on
    # the outer ring, each with a leader to its name and total.
    callouts = []
    def arc(node, r, color, lw, group):
        if node.arc is None:
            return
        a, b = node.arc
        pad = min(2.5 / r, (b - a) / 4)  # gap between neighbouring arcs
        t = np.linspace(a + pad, b - pad, max(2, int((b - a) * 60)))
        ax.plot(*(r * np.c_[np.cos(t), np.sin(t)] + centre).T, color=color, lw=lw, solid_capstyle="butt")
        for e in (t[0], t[-1]):  # end ticks, as on a dimension line
            u = np.array([np.cos(e), np.sin(e)])
            ax.plot(*np.c_[(r - 2.5) * u + centre, (r + 2.5) * u + centre], color=color, lw=lw)
        mid = (a + b) / 2
        total = money(node.value, meta)
        if group:
            lines = [(total, 11.0, True)] + [(s, 8.5, False) for s in wrap_to(node.name, 8.5, wrap_w)]
        else:
            lines = [(s, 6.5, False) for s in wrap_to(f"{node.name}  {total}", 6.5, wrap_w)]
        callouts.append(dict(mid=mid, r=r, color=color, lines=lines, side=1 if np.cos(mid) >= 0 else -1,
                             y=r_lab * np.sin(mid), h=sum(f for _, f, _ in lines) * PITCH))
    for gi, g in enumerate(root.children):
        if depth == 3:
            for sub in g.children:
                arc(sub, r_sub, PALETTE[gi][1], 0.7, False)
        arc(g, r_grp, PALETTE[gi][1], 1.6, True)
    for side in (1, -1):
        items = [d for d in callouts if d["side"] == side]
        spread(items, -(r_lab + 26), r_lab + 26)
        for d in items:
            x = side * (np.sqrt(max(r_lab ** 2 - d["y"] ** 2, 0)) + 6)
            p0 = d["r"] * np.array([np.cos(d["mid"]), np.sin(d["mid"])]) + centre
            p1 = np.array([x - side * 3, d["y"]]) + centre
            ax.plot(*np.c_[p0, p1], color=MUTED, lw=0.4)
            ax.plot(*p0, "o", ms=2.6, color=d["color"])
            y = d["y"] + d["h"] / 2
            for s, f, bold in d["lines"]:
                y -= f * PITCH / 2
                put(x + centre[0], y + centre[1], s, f, bold, ha="left" if side > 0 else "right")
                y -= f * PITCH / 2

    for i, (s, bold) in enumerate(key_lines):
        col, row = divmod(i, rows)
        put(MARGIN + col * (col_w + 18), cy - (r_lab + 30) - 14 - row * key_f * 1.4, s, key_f, bold)

    out = Path(path).with_suffix("")
    fig.savefig(f"{out}.png", dpi=300, facecolor="white")
    fig.savefig(f"{out}.svg", facecolor="white")
    print(f"{len(root.leaves())} cells in {len(root.children)} groups, total {money(root.value, meta)}")
    print(f"max area error {err:.2e} (limit {LEAF_TOL:.0e})")
    print(f"labels: {tiers[0]} in cell, {tiers[1]} by key number, {tiers[2]} key only")
    print(f"wrote {out}.png {out}.svg")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
