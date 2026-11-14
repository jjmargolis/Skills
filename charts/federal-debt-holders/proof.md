# Proof: who holds the US federal debt

This file records the checks behind `debt.png` and `debt.svg`. The layout method and its proofs are in [voronoi-treemap/PROOF.md](../../voronoi-treemap/PROOF.md).

## Data reconciles to the published total

All figures are at 31 March 2025, in $ billions.

| Holder class | Source | $ billions |
|---|---|---:|
| Foreign and international | TIC major foreign holders | 9,052.0 |
| Domestic private investors | OFS-2 categories, split by Z.1 L.210 and MSPD | 15,641.3 |
| Federal Reserve | derived, see below | 4,218.8 |
| US government accounts | MSPD Table III | 7,304.8 |
| **Sum of cells** | | **36,216.9** |
| Published total public debt | MSPD Table I | 36,214.3 |

The sum is 2.6 higher than the published total. TIC has since revised March 2025 foreign holdings to 9,052.0, up from the 9,049.5 printed in OFS-2 (+2.5). Z.1 prints one decimal, so two OFS-2 categories rebuilt from Z.1 sectors come out 0.1 high each (+0.2). The published figures themselves round (−0.1).

The Federal Reserve figure is derived. OFS-2 prints Federal Reserve and government accounts together as 11,523.6. Taking away MSPD intragovernmental holdings of 7,304.8 leaves 4,218.8, because Treasury doesn't publish the Federal Reserve figure separately.

Seven government funds are left out because MSPD reports them as zero or under $500,000. Their area would be zero at this scale.

## Grouping

The chart has three levels: holder class, then subgroup, then holder. The subgroups are a classification made for this chart, and Treasury doesn't publish them.

- **Foreign and international holders** are grouped by region: Europe, Asia and Pacific, Americas, Middle East, and all other countries. TIC records holdings by the country where the securities are held in custody, so custody centres such as Belgium, Luxembourg and the Cayman Islands look larger than their own investors' holdings. This caveat about TIC is recalled from memory and wasn't re-read for this chart.
- **Domestic private investors** are split below the OFS-2 categories into the Federal Reserve Z.1 sectors (Table L.210, release of 12 June 2025) and MSPD lines they are built from. See the next section.
- **US government accounts** are grouped by program: Social Security, Medicare, military and veterans, civilian retirement and benefits, insurance and guarantee funds, transport and environment, unemployment insurance, and other accounts. Within each program, funds under $5bn are summed into one cell, "Smaller funds (N)". [government-accounts.csv](government-accounts.csv) lists all 143 funds with their program and value, so every folded total can be checked.

Summing published values adds no estimate. Each folded cell is the exact sum of the funds listed for it.

## Domestic private investors, holder by holder

OFS-2 publishes eight domestic private categories. Six of them equal, to rounding, sums of Z.1 L.210 lines for 2025 Q1 (June 2025 release), or a Z.1 line plus an MSPD line, which shows OFS-2 was built from that release. Each is drawn as its parts.

| OFS-2 category | OFS-2 | Parts drawn (source) | Sum |
|---|---:|---|---:|
| Mutual funds | 4,421.3 | money market funds 2,880.6, mutual funds 1,538.8, closed-end funds 2.0 (Z.1 lines 29, 32, 35) | 4,421.4 |
| Depository institutions | 1,878.1 | U.S.-chartered 1,545.5, holding companies 137.3, foreign banking offices 108.2, credit unions 63.3, banks in U.S.-affiliated areas 23.8 (Z.1 lines 12–15, 40) | 1,878.1 |
| Insurance companies | 622.9 | property-casualty 432.0, life 190.9 (Z.1 lines 16, 19) | 622.9 |
| Private pension funds | 470.8 | defined contribution 250.8, defined benefit 220.1 (Z.1 lines 23, 24) | 470.9 |
| State and local government pension funds | 502.0 | (Z.1 line 28) | 502.0 |
| State and local governments | 1,700.0 | marketable Treasuries excluding SLGS 1,613.5 (Z.1 line 8), State and Local Government Series 86.5 (MSPD Table I) | 1,700.0 |
| U.S. savings bonds | 155.0 | as published | 155.0 |
| Other investors | 5,891.0 | see below | 5,891.0 |

Closed-end funds ($2.0bn) are drawn together with mutual funds, as one cell, because a $2bn cell is too small to see.

OFS-2 "Other investors" is the remainder after every named category, so no table publishes its parts. The Z.1 sectors that aren't in any other OFS-2 category are drawn at their Z.1 values: households and nonprofits 2,859.0, exchange-traded funds 605.3, brokers and dealers 487.6, government-sponsored enterprises 232.3, nonfinancial corporations 123.3, nonfinancial noncorporate businesses 87.2, central clearing counterparties 83.4, asset-backed securities issuers 25.1, and federal retirement funds (mostly the Thrift Savings Plan F Fund) 20.4. Nonmarketable debt held by the public that no other line covers is one cell of 101.1 (MSPD Table I: domestic series 13.7, government account series 82.6, other 4.8). That leaves 1,266.3, drawn as "Residual, holder not identified". It is derived by subtraction and is marked so in the CSV header.

The residual is most likely a valuation gap rather than a missing holder. Z.1 counts marketable Treasuries only (its L.210 footnote 4 puts nonmarketable debt outside the instrument), and most of its holder series are at market value (the "LM" series codes, and line 32 says "market value" outright), while OFS-2 totals are at par. Z.1's own "instrument discrepancy" for the quarter, which it defines as "the accumulated valuation difference between issuance and holdings", is 1,570.1. That reading is an inference: neither source states how OFS-2's residual divides.

Z.1 households don't include savings bonds, because Z.1 excludes nonmarketable debt, so drawing both doesn't count anything twice.

Which parts were read for this change and which are recalled: the Z.1 L.210 values and footnotes, the MSPD Table I lines and the TIC foreign official figure were read on 14 November 2026. That OFS-2 was built from the June 2025 Z.1 release is inferred from the exact matches above. The OFS-2 footnotes that list what "Other investors" includes (individuals, GSEs, brokers and dealers, bank personal trusts, businesses) are recalled from memory; the Bulletin PDF couldn't be read past page 22.

## Foreign official and private holders

TIC reports foreign official holdings of 3,923.4 at March 2025 (bills 419.8, bonds and notes 3,503.6), which leaves 5,128.6 private. TIC doesn't publish the official figure by country, so splitting each country would need an estimate. The chart keeps the regional grouping and records the split here and in the CSV header.

## Areas match values

Output of `python voronoi_treemap.py debt.csv`:

```
101 cells in 4 groups, total $36.2tn
max area error 2.58e-04 (limit 1e-03)
labels: 32 in cell, 45 by key number, 24 key only
```

Every finished cell was measured with the shoelace formula. The worst one is 0.026% off its target area, and the script fails above 0.1%. Rendering takes about 20 seconds, and the same CSV always gives the same picture.

## Sources

- Treasury Bulletin, September 2025, Table OFS-2: [b2025-3.pdf](https://fiscal.treasury.gov/system/files/files/reports-statements/treasury-bulletin/2025/b2025-3.pdf)
- Federal Reserve, Financial Accounts of the United States (Z.1), 12 June 2025, Table L.210: [l210.htm](https://www.federalreserve.gov/releases/z1/20250612/html/l210.htm)
- Monthly Statement of the Public Debt, Tables I and III, 31 March 2025: [Table I](https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/debt/mspd/mspd_table_1?filter=record_date:eq:2025-03-31), [Table III](https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/debt/mspd/mspd_table_3_nonmarket?filter=record_date:eq:2025-03-31)
- Treasury International Capital, major foreign holders of Treasury securities: [mfhhis01.txt](https://ticdata.treasury.gov/resource-center/data-chart-center/tic/Documents/mfhhis01.txt)
