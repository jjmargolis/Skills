---
name: voronoi-treemap
description: Draw a circular Voronoi treemap (disc of cells sized by value, grouped by colour and rim arcs) from a 2- or 3-level dataset. Use when asked for this chart form or a "bubble/cell pie" of parts of a whole.
---

# Voronoi treemap

Turns a table of parts of a whole into a disc of convex cells whose areas are proportional to value, nested by group and optionally subgroup, as PNG and SVG.

## 1. Source the data

- Read primary sources directly (the publishing agency's own table or API). Record the table name, URL and as-of date.
- All figures in one chart share one as-of date or period.
- Add the rows up. The sum must equal the source's published total; write the sum and the published total into the CSV header. If they differ, state the difference and its cause.
- Publish only numbers the source prints. A number obtained by subtracting two published figures is marked `derived` in the header. Apply no shares or estimates; if a figure is not published, say so.
- Every value must be positive, because area cannot be negative. Where a published line is negative, draw its parent at the parent's published net total, or leave the line out and name it and its amount in the subtitle.
- Tell the user which numbers were read today and which are recalled from memory.

## 2. Write the CSV

```
# title: Who holds the US federal debt
# subtitle: One or two sentences; wraps automatically.
# source: Publisher, table name
# source_url: https://...
# as_of: 2025-03-31
# prefix: $
# scale: 1e9
# reconciliation: a + b + c = total; published total
group,label,value
Foreign holders,Japan,1135.1
```

- Columns are `group,label,value` (2 levels) or `group,subgroup,label,value` (3 levels). Quote any field that contains a comma.
- Optional last column `icon`: an image path relative to the CSV, or empty.
- `#` lines are metadata. The script uses `title`, `subtitle`, `source`, `as_of`, `prefix` and `scale`; other keys are for the reader of the file.
- `scale` is what one CSV unit stands for (`1e6` if values are in millions). Values print with three significant figures and k, m, bn or tn.
- Groups take colours in CSV order: red, blue, yellow, pink, green, violet, aqua, orange. At most 8 groups; merge the smallest before running if there are more.
- Rows keep CSV order within their group. One row per leaf; no totals rows.

## 3. Run

```
pip install numpy matplotlib
python voronoi_treemap.py data.csv
```

Writes `data.png` (300 dpi) and `data.svg` beside the CSV and prints the cell count, the largest area error and how the labels were placed. About 5 seconds for 50 cells, 2 minutes for 200; allow a 5-minute timeout. The same CSV always gives the same picture.

## 4. What the script guarantees

Full statement and proofs are in `PROOF.md`.

- **Size.** Area is linear in value at every level. The script measures each finished cell and fails if any is more than 0.1% off.
- **Placement.** Each parent region is cut into power-diagram cells, so cells are convex, do not overlap, leave no gaps and stay inside their group. Position carries no data.
- **Labels.** Name over bold value, at the largest font that keeps the block inside the cell. An icon goes above or below the text, whichever allows the larger font, and is dropped where it does not fit.
- **Small cells.** A cell too small for 4.5pt text shows a key number; its name and value are in the key under the chart. A cell too small for the number is listed in the key with a dot.
- **Arcs.** Each group has a heavy arc outside the rim with its total and name. In a 3-level chart each subgroup has a thin arc inside the group's. A subgroup that touches no rim is named in the key with its members.

## 5. Check the picture

Open the PNG and look at it before showing the user. Fix the CSV and rerun until all of these hold:

1. No label crosses a cell edge or overlaps another label.
2. Arc labels and leaders do not collide with each other or run off the page. If they do, shorten group or subgroup names.
3. Title and subtitle fit the page width.
4. The printed total matches the reconciled total, and the group totals match the source.
5. The largest cells are the largest values. If a group looks wrong, re-add its rows.
6. Nothing a reader would take as a part of the whole is missing without the subtitle saying so.

Report the printed area error and label counts to the user with the chart.
