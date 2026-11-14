# Proof: 2026 midterm donors

This file records the checks behind `donors.png` and `donors.svg`. The layout method and its proofs are in [voronoi-treemap/PROOF.md](../../voronoi-treemap/PROOF.md).

## Data

There are 50 donors and organisations, totalling $2.77bn, with values in $ millions as of 26 October 2026. The source is Federal Election Commission filings, as compiled by Al Jazeera (AJ Labs). That compilation doesn't publish a total to reconcile against, so the total shown is the sum of the rows.

## Areas match values

Output of `python voronoi_treemap.py donors.csv`:

```
50 cells in 3 groups, total $2.77bn
max area error 2.78e-04 (limit 1e-03)
labels: 49 in cell, 1 by key number, 0 key only
```

Every finished cell was measured with the shoelace formula. The worst one is 0.028% off its target area, and the script fails above 0.1%.
