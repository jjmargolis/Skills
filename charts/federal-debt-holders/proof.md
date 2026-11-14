# Proof: who holds the US federal debt

This file records the checks behind `debt.png` and `debt.svg`. The layout method and its proofs are in [voronoi-treemap/PROOF.md](../../voronoi-treemap/PROOF.md).

## Data reconciles to the published total

All figures are at 31 March 2025, in $ billions.

| Holder class | Source | $ billions |
|---|---|---:|
| Foreign and international | TIC major foreign holders | 9,052.0 |
| Domestic private investors | Treasury Bulletin OFS-2 | 15,641.1 |
| Federal Reserve | derived, see below | 4,218.8 |
| US government accounts | MSPD Table III | 7,304.8 |
| **Sum of cells** | | **36,216.7** |
| Published total public debt | MSPD Table I | 36,214.3 |

The sum is 2.4 higher than the published total. TIC has since revised March 2025 foreign holdings to 9,052.0, up from the 9,049.5 printed in OFS-2. With the OFS-2 figure, the sum is 36,214.2, which matches to rounding.

The Federal Reserve figure is derived. OFS-2 prints Federal Reserve and government accounts together as 11,523.6. Taking away MSPD intragovernmental holdings of 7,304.8 leaves 4,218.8, because Treasury doesn't publish the Federal Reserve figure separately.

Seven government funds are left out because MSPD reports them as zero or under $500,000. Their area would be zero at this scale.

## Grouping

The chart has three levels: holder class, then subgroup, then holder. The subgroups are a classification made for this chart, and Treasury doesn't publish them.

- **Foreign and international holders** are grouped by region: Europe, Asia and Pacific, Americas, Middle East, and all other countries. TIC records holdings by the country where the securities are held in custody, so custody centres such as Belgium, Luxembourg and the Cayman Islands look larger than their own investors' holdings. This caveat about TIC is recalled from memory and wasn't re-read for this chart.
- **Domestic private investors** are grouped as funds and institutions, state and local, and individuals and others. The holder categories are as published in OFS-2.
- **US government accounts** are grouped by program: Social Security, Medicare, military and veterans, civilian retirement and benefits, insurance and guarantee funds, transport and environment, unemployment insurance, and other accounts. Within each program, funds under $5bn are summed into one cell, "Smaller funds (N)". [government-accounts.csv](government-accounts.csv) lists all 143 funds with their program and value, so every folded total can be checked.

Summing published values adds no estimate. Each folded cell is the exact sum of the funds listed for it.

## Areas match values

Output of `python voronoi_treemap.py debt.csv`:

```
83 cells in 4 groups, total $36.2tn
max area error 2.43e-04 (limit 1e-03)
labels: 28 in cell, 34 by key number, 21 key only
```

Every finished cell was measured with the shoelace formula. The worst one is 0.024% off its target area, and the script fails above 0.1%. Rendering takes about 13 seconds, and the same CSV always gives the same picture.

## Sources

- Treasury Bulletin, September 2025, Table OFS-2: [b2025-3.pdf](https://fiscal.treasury.gov/system/files/files/reports-statements/treasury-bulletin/2025/b2025-3.pdf)
- Monthly Statement of the Public Debt, Tables I and III, 31 March 2025: [Table I](https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/debt/mspd/mspd_table_1?filter=record_date:eq:2025-03-31), [Table III](https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/debt/mspd/mspd_table_3_nonmarket?filter=record_date:eq:2025-03-31)
- Treasury International Capital, major foreign holders of Treasury securities: [mfhhis01.txt](https://ticdata.treasury.gov/resource-center/data-chart-center/tic/Documents/mfhhis01.txt)
