# Proof: FY2025 federal outlays

This file records the checks behind `budget.png` and `budget.svg`. The layout method and its proofs are in [voronoi-treemap/PROOF.md](../../voronoi-treemap/PROOF.md).

## Data reconciles to the published total

| | $ millions |
|---|---:|
| Sum of the 53 cells | 7,189,490 |
| Commerce and housing credit, net negative, no area | −28,131 |
| Undistributed offsetting receipts, net negative, no area | −150,254 |
| **Total** | **7,011,105** |
| OMB Historical Table 3.1, total outlays FY2025 | 7,011,105 |

The total matches exactly. As a cross-check, the September 2025 Monthly Treasury Statement (Table 9) prints 7,009,974, which is 1,131 lower. OMB's actuals came out later and are the final figures.

A function with any negative subfunction is drawn as one cell at its published net total, so every cell is a net amount and every area is positive.

## Areas match values

Output of `python voronoi_treemap.py budget.csv`:

```
53 cells in 5 groups, total $7.19tn
max area error 2.34e-04 (limit 1e-03)
labels: 16 in cell, 29 by key number, 8 key only
```

Every finished cell was measured with the shoelace formula. The worst one is 0.023% off its target area, and the script fails above 0.1%. Rendering takes about 8 seconds, and the same CSV always gives the same picture.

## Sources

- OMB Historical Tables 3.1 and 3.2, Budget of the US Government FY2027 (actuals for FY2025): [hist03z1_fy2027.xlsx](https://www.whitehouse.gov/wp-content/uploads/2026/04/hist03z1_fy2027.xlsx), [hist03z2_fy2027.xlsx](https://www.whitehouse.gov/wp-content/uploads/2026/04/hist03z2_fy2027.xlsx)
