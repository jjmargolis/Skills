# Why the layout is correct

The chart is a disc cut into convex cells, one per leaf of a 2- or 3-level
tree. This file states the rules `voronoi_treemap.py` implements and why each
holds. Section 6 says which results are cited from memory.

## 1. Value to size

Leaves carry values v > 0; a parent's value is the sum of its children's. The
disc Ω is the root's region. Every node u gets a region of area

    a(u) = |Ω| · v(u) / v(root).

a(u)/v(u) is the same constant for every node, so area is linear in value with
zero intercept. Children tile their parent exactly (section 2), so a parent's
area is the sum of its children's and the rule holds at every level once it
holds for the leaves.

The areas are reached by iteration, so the script measures every finished leaf
polygon with the shoelace formula and stops with an error if any is more than
0.1% from a(u). The guarantee is checked on each run.

## 2. Placement

Apply this to each parent, top down. The parent has a convex region P and k
children with target areas tᵢ, Σtᵢ = |P|. Child i gets a site sᵢ ∈ P and a
weight wᵢ. Its cell is the power cell

    Cᵢ = { x ∈ P : |x − sᵢ|² − wᵢ ≤ |x − sⱼ|² − wⱼ for all j }.

The quadratic terms cancel, so each condition is a half-plane,
2(sⱼ − sᵢ)·x ≤ |sⱼ|² − |sᵢ|² + wᵢ − wⱼ, and Cᵢ is P clipped by k − 1 half-planes.

- **Convex.** An intersection of convex sets is convex. The disc is a regular
  360-gon, 0.005% short of a circle.
- **No overlap.** A point interior to both Cᵢ and Cⱼ would have i's power
  distance strictly below j's and the reverse.
- **No gaps.** Every x ∈ P has an i that minimises the power distance.
- **Inside its group.** Cᵢ ⊆ P by construction. Each Cᵢ is convex, so it is a
  valid P for its own children; by induction leaf ⊆ subgroup ⊆ group ⊆ disc.
  Nothing depends on k or on depth.

## 3. Reaching the target areas

For fixed distinct sites there are weights, unique up to an added constant,
with |Cᵢ(w)| = tᵢ for all i. They maximise the concave function

    Φ(w) = Σᵢ ∫ over Cᵢ(w) of (|x − sᵢ|² − wᵢ) dx + Σᵢ wᵢ tᵢ,   ∂Φ/∂wᵢ = tᵢ − |Cᵢ(w)|.

Φ is concave because the first sum is a minimum, over all ways of assigning
points to sites, of functions linear in w.

Raising wᵢ by δ moves the edge shared with neighbour j outward by δ / (2|sᵢ − sⱼ|),
so with ℓᵢⱼ the length of that edge,

    ∂|Cᵢ|/∂wⱼ = −ℓᵢⱼ / (2|sᵢ − sⱼ|),   ∂|Cᵢ|/∂wᵢ = Σⱼ ℓᵢⱼ / (2|sᵢ − sⱼ|).

The script solves this linear system for a Newton step (one weight pinned,
since only differences matter) and halves the step until two things hold: no
cell falls below half of the smaller of the smallest target and the smallest
starting area, and the area error shrinks by the factor 1 − t/2 for step
fraction t. Equal weights give the Voronoi diagram, where every cell contains
its own site, so the iteration always has a start with no empty cell.

Between solves each site moves to the centroid of its cell (25 rounds). The
centroid of a convex cell lies inside it, so sites stay in P and stay distinct.
This step only rounds the cells; the final solve, with sites fixed, is the
concave problem above and is run to a relative area error of 0.03%.

Sites start at seeded random points, so one CSV always gives one picture.
Position carries no data.

## 4. Label fit

A label is the name, broken into up to five lines, over the value in bold. At
font size f it is a rectangle of width f·ω and height f·L·λ, where ω is the
widest line per unit font size (from font metrics), L the number of lines and
λ the line pitch. With an icon of aspect ratio ρ, the block is two stacked
rectangles: the text, and an icon of height 3.5f and width 3.5ρf, with a gap
of 0.3f. The block is centred on the cell centroid c.

- **Fit test.** A rectangle is inside a convex cell exactly when its four
  corners are. So the block fits when all its corners do: four for a label,
  eight with an icon.
- **Largest font, closed form.** Each corner sits at c + f·u for a fixed
  offset u. For a cell edge with outward unit normal n and offset d (the cell
  is n·x ≤ d), the corner is inside when f·(n·u) ≤ d − n·c − pad. Hence

      f* = min over edges of (d − n·c − pad) / max over corners of (n·u).

- **Line breaks.** Every way of breaking the name at spaces is tried and the
  one with the largest f* is kept; ties go to fewer lines.
- **Icon above or below.** The two arrangements have different corner sets
  because text and icon differ in width. Both are evaluated and the one with
  the larger f* is drawn. If neither reaches the minimum font size, the icon
  is left out and the label is fitted alone.
- **Small cells.** Below the minimum font size (4.5pt on the 780pt page) the
  cell keeps its true area and shows a key number; name and value go in the
  key under the chart. A cell too small for the number is listed in the key
  with a dot. Every leaf is named somewhere.
- Font size is capped at 15pt.

## 5. Arcs outside the rim

A region touches the rim along the polygon edges whose two ends lie on the
circle and that are no longer than one side of the 360-gon; a longer edge
between two rim points is a cut across the disc. Consecutive rim edges form a
run. Each group gets a heavy arc over its longest run, on the outer ring, with
a leader to its total and name. In a 3-level chart each subgroup gets a thin
arc on the inner ring. A subgroup that touches no rim has no arc; the key
lists it with its members.

## 6. Sources

Cited from memory, not re-read while writing this:

- Aurenhammer, Hoffmann and Aronov (1998), "Minkowski-type theorems and
  least-squares clustering": existence and uniqueness of the weights, and the
  concave function in section 3.
- Kitagawa, Mérigot and Thibert (2019): convergence of the damped Newton
  iteration with the no-empty-cell condition.
- Balzer and Deussen (2005); Nocaj and Brandes (2012): Voronoi treemaps by
  centroid relaxation of a power diagram.

Sections 1, 2, 4 and 5 are proved in full above. Section 3 relies on the cited
results for convergence; the measured area check in section 1 does not.
