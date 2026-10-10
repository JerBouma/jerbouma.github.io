---
title: "CreditTermStructure"
seo_title: "CreditTermStructure Reference – Finance Scenarios"
excerpt: "A Nelson-Siegel credit spread curve."
description: "A Nelson-Siegel credit spread curve."
author_profile: false
permalink: /projects/financescenarios/docs/reference/credit-term-structure
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

A Nelson-Siegel credit spread curve. Generated from the docstrings of Finance Scenarios 0.1.0; `help(...)` in Python shows the same text.

```python
from financescenarios.factors.credit_term_structure.credit_term_structure_controller import CreditTermStructure
```

```python
CreditTermStructure(bond_panel: BondPanel | None = None, toolkit: Toolkit | None = None)
```

The Credit Term Structure module simulates a whole credit spread curve: the extra yield
corporate bonds pay over government bonds, at every maturity from one year out to twenty,
rather than one spread per bucket. The curve moves through time by three numbers (level,
slope and curvature), so the spread at any maturity can be read off a simulated scenario.

In plain terms: where `Credit` gives a handful of fixed spread buckets (1-3 years,
7-10 years, BBB and so on), this gives a continuous curve, so a 4-year or a 12-year
corporate spread exists in every simulated scenario too. Combined with the simulated
government curve (`yield_curve`) it gives the full discount curve a risky bond is priced
off, which is what `BondPricer` uses. It is opt-in (`credit_term_structure.enabled`) and
works next to `credit`, not instead of it: both can be enabled together.

The model is the dynamic Nelson-Siegel curve ([Nelson & Siegel, 1987](https://doi.org/10.1086/296409);
[Diebold & Li, 2006](https://doi.org/10.1016/j.jeconom.2005.03.005)), the same machinery the
government `yield_curve` uses, applied to corporate spreads as in
[Yu & Zivot (2011)](https://doi.org/10.1016/j.ijforecast.2010.04.002). At each date the
observed spreads across maturities are summarized by three factors: `credit_level` (the
long-maturity spread), `credit_slope` (how much lower or higher the short end sits than the
long end) and `credit_curvature` (a hump in the middle maturities). Each factor is then
fitted as its own mean-reverting (Ornstein-Uhlenbeck) process, a process that is pulled back
toward a normal level at a fitted speed, and the three enter the simulation as correlated
factors linked to the rest of the model through the correlation matrix (no cascade
dependency on any other factor). The mathematics is not reimplemented: `term_structure_model`'s
`fit_nelson_siegel_factors`, `fit_ou_process`, `YieldCurveParams` and `step_curve_factor`
are reused directly, the same way `equities_model.fit_risk_neutral_equity` reuses `FXParams`.

The `decay` (lambda) fixes where the curvature hump peaks and is not fitted, following
Diebold and Li. Its default of 0.7308 equals `yield_curve.decay` on purpose:
Nelson-Siegel curves with the same decay add up factor by factor, so the government curve
plus this spread curve is again a Nelson-Siegel curve, the risky-bond discount curve.

Two data sources are available (`source`). The default, `hqm`, is the US Treasury's High
Quality Market (HQM) corporate bond curve through the Finance Toolkit
(`fixedincome.get_hqm_corporate_bond_spread()`): the HQM par yield minus the Treasury par
yield at 2, 5, 10 and 30 years, monthly from 1984 and a few kilobytes, read with a free FRED
key. HQM is the curve US pension plans discount their obligations with
([US Treasury](https://home.treasury.gov/data/treasury-coupon-issues-and-corporate-bond-yield-curves)),
built from high-quality (AAA, AA and A rated) bonds, so it is the investment-grade spread
curve rather than an all-ratings average. It can be averaged to quarters or years but not
split finer than a month.

The alternative, `bond_panel`, is the Open Source Bond Asset Pricing project's public corporate bond panel
([openbondassetpricing.com](https://openbondassetpricing.com/), Dickerson, Robotti and
Rossetti), built from TRACE, the US regulator's record of every corporate bond trade:
29,776,137 (bond, trade date) rows from 2002-07-01 to 2025-03-31, each with a
`credit_spread` measured against [Liu & Wu's (2021)](https://doi.org/10.1016/j.jfineco.2021.05.059)
constant-maturity zero-coupon government curve. It does not come through the Finance
Toolkit: `BondPanel` downloads it once (about 1.8 GB) and caches it under
`.cache/validation/` (see `bond_panel_controller.BondPanel` for the license note). Each bond
is assigned to its nearest requested tenor, spreads are averaged per tenor and trade date,
then averaged again per `period` (`bond_panel_model.spread_by_tenor`). The panel ends in
March 2025, so the curve's starting point is the panel's last usable month, not today.

Two limits follow from that source. The public drop has no credit-rating field, so this is
a curve of the average spread across all bonds, not one per rating, and it is not a
rating-migration model (a bond moving from BBB to BB to default); that remains an open gap,
see the coverage overview. And the three factors are fitted independently, without the cross-factor
restrictions that would make the curve free of arbitrage; the arbitrage-free Nelson-Siegel
variant ([Christensen, Diebold & Rudebusch, 2011](https://doi.org/10.1016/j.jeconom.2011.02.011))
and the four-factor Svensson extension with a second hump
([Svensson, 1994](https://doi.org/10.3386/w4871)), which credit curves sometimes show, are not
implemented. The curve is fitted statistically; the credit-risk theory that explains why
spread curves take this shape (default intensity and rating transitions,
[Jarrow, Lando & Turnbull, 1997](https://doi.org/10.1093/rfs/10.2.481);
[Duffie & Singleton, 1999](https://doi.org/10.1093/rfs/12.4.687)) is not modeled directly.

Configuration (`credit_term_structure` in a factor set):

| Key | Default | Meaning |
|:----|:--------|:--------|
| `enabled` | `false` | Adds `credit_level`, `credit_slope` and `credit_curvature` to the run. |
| `source` | `hqm` | `hqm` (Treasury HQM spread curve, monthly from 1984) or `bond_panel` (TRACE panel, 1.8 GB). |
| `tenors` | `[1, 2, 3, 5, 7, 10, 15, 20]` | Bond panel maturities (years), at least 3; unused by `hqm`. |
| `period` | `monthly` | Fitting frequency; `hqm` monthly, quarterly or yearly; panel `daily` not recommended. |
| `decay` | `0.7308` | Nelson-Siegel decay (lambda); keep equal to `yield_curve.decay`. |
| `beliefs.level` | `null` | Override the level factor's fitted process (same shape as `yield_curve.beliefs`). |
| `beliefs.slope` | `null` | Override the slope factor's fitted process. |
| `beliefs.curvature` | `null` | Override the curvature factor's fitted process. |

`period` defaults to `monthly`, not `daily` as `yield_curve` does, because single-bond daily
spreads carry bid/ask bounce and illiquid-bond noise that reverts within days. Fitted on raw
daily data, that noise produces mean-reversion speeds of tens per year; under the old
Euler-Maruyama discretization one real run diverged to +-1e38 within 60 months. The exact
discrete-time transition `fit_ou_process` now uses (see simulation-engine.md) is stable at
any speed, and its regression-slope guard usually rejects near-random daily noise outright
as having no finite mean-reversion rate, but daily noise is still a poor fitting target.

**References:**

- Nelson, C.R., Siegel, A.F. (1987). "Parsimonious Modeling of Yield Curves." The Journal of Business, 60(4), 473-489. <https://doi.org/10.1086/296409>
- Diebold, F.X., Li, C. (2006). "Forecasting the Term Structure of Government Bond Yields." Journal of Econometrics, 130(2), 337-364. <https://doi.org/10.1016/j.jeconom.2005.03.005>
- Yu, W., Zivot, E. (2011). "Forecasting the Term Structures of Treasury and Corporate Yields Using Dynamic Nelson-Siegel Models." International Journal of Forecasting, 27(2), 579-591. <https://doi.org/10.1016/j.ijforecast.2010.04.002>
- Liu, Y., Wu, J.C. (2021). "Reconstructing the Yield Curve." Journal of Financial Economics, 142(3), 1395-1425. <https://doi.org/10.1016/j.jfineco.2021.05.059>
- Dickerson, A., Robotti, C., Rossetti, G. Open Source Bond Asset Pricing, replication data and code. <https://openbondassetpricing.com/>
- Svensson, L.E.O. (1994). "Estimating and Interpreting Forward Interest Rates: Sweden 1992-1994." NBER Working Paper 4871. <https://doi.org/10.3386/w4871>
- Jarrow, R.A., Lando, D., Turnbull, S.M. (1997). "A Markov Model for the Term Structure of Credit Risk Spreads." Review of Financial Studies, 10(2), 481-523. <https://doi.org/10.1093/rfs/10.2.481>
- Duffie, D., Singleton, K.J. (1999). "Modeling Term Structures of Defaultable Bonds." Review of Financial Studies, 12(4), 687-720. <https://doi.org/10.1093/rfs/12.4.687>
- Christensen, J.H.E., Diebold, F.X., Rudebusch, G.D. (2011). "The Affine Arbitrage-Free Class of Nelson-Siegel Term Structure Models." Journal of Econometrics, 164(1), 4-20. <https://doi.org/10.1016/j.jeconom.2011.02.011>

## calibrate

```python
calibrate(
    tenors: list[float],
    period: str = 'monthly',
    decay: float = 0.7308,
    source: str = 'bond_panel',
) -> YieldCurveParams
```

Calibrate the credit spread curve from the bond panel: bin every bond's spread into the
requested maturities, summarize each period's curve by its Nelson-Siegel level, slope and
curvature, and fit each of the three as a mean-reverting process with its own speed
(`mean_reversion_speed`), normal level (`long_run_mean`) and swing size (`volatility`).

In plain terms: this learns from 22 years of real corporate bond trades how the credit
spread curve has moved, so the simulated curves shift, tilt and bend the way the real one
has. A mean-reversion speed of 1.24 a year, for example, means a shock to the curve's level
has faded by half after about seven months (ln 2 / 1.24 years).

All values are decimals (0.01 is a 1% spread). `level` is the spread at very long
maturities, `level + slope` the spread at the very short end, and `curvature` adds a hump
that peaks at medium maturities. `initial_value` of each factor is the curve in the panel's
last usable month, the starting point of every simulated scenario.

Also known as: dynamic Nelson-Siegel credit curve, corporate spread term structure fit.

**Args:**

- <u>tenors (list[float]):</u> maturity points, in years, to bin the panel into; each bond is assigned to its nearest tenor. At least 3 are needed to identify level, slope and curvature; see `bond_panel_model.spread_by_tenor`.
- <u>period (str):</u> resampling frequency ("daily", "weekly", "monthly", "quarterly", "yearly"). The panel holds raw daily trades, so this both averages the cross-section to `period` and sets the time step of the fitted processes. Defaults to "monthly", not "daily" as `TermStructure.calibrate`'s smooth government-yield data can safely use (see Notes).
- <u>source (str):</u> "bond_panel" (the default of this method, kept for existing callers) or "hqm", the Treasury's HQM spread curve at 2, 5, 10 and 30 years read through the Toolkit; `tenors` is unused for "hqm". A config's `credit_term_structure.source` defaults to "hqm".
- <u>decay (float):</u> the Nelson-Siegel decay parameter (lambda), annualized; fixed rather than fitted, per Diebold & Li (2006). The default 0.7308 equals `yield_curve`'s on purpose: Nelson-Siegel curves with a shared decay add up factor by factor, so the government curve plus this spread curve is exactly the risky-bond curve.

**Returns:**

<u>YieldCurveParams:</u> the calibrated `level`, `slope` and `curvature` processes and the `decay`. The type is named for the government curve it was first built for and is reused as-is here.

**Raises:**

- <u>ValueError:</u> if `period` isn't recognized, `tenors` has fewer than 3 distinct entries or a non-positive one, or `decay` is not positive; all checked before the panel is read.

**Notes:**

- The first call downloads the panel (about 1.8 GB) to `.cache/validation/` (override with
  the `FINANCESCENARIOS_VALIDATION_CACHE_DIR` environment variable); later calls read the
  cache. The panel is scanned lazily, but grouping 29.8 million rows still needs well over
  1 GB of memory; on a small machine, `pl.Config.set_engine_affinity("streaming")` before
  calling keeps it within bounds.
- Only periods in which every requested tenor has at least one bond are kept, so adding a
  thinly traded far tenor can shorten the usable history.
- Bonds maturing before the shortest tenor or after the longest are dropped, and so is
  anything with less than three months (0.25 years) left, where spreads become erratic.
- Why not daily: single-bond daily spreads carry bid/ask and illiquid-bond noise that
  reverts within days. Fitted daily, it gives mean-reversion speeds of tens per year, and
  the regression-slope guard of the exact OU transition often rejects it outright as
  having no finite mean-reversion rate.
- There is no credit rating in the panel, so the curve is the average across all bonds.

**As an example:**

```python
import polars as pl

from financescenarios.factors.credit_term_structure.credit_term_structure_controller import (
    CreditTermStructure,
)

pl.Config.set_engine_affinity("streaming")  # keeps the 29.8M-row scan within a small machine's memory

credit_curve = CreditTermStructure()
credit_curve.calibrate(tenors=[1, 2, 3, 5, 7, 10, 15, 20], period="monthly")
```

Which returns (calibrated on 2026-10-04):

| factor | mean_reversion_speed | long_run_mean | volatility | initial_value |
|:-------|---------------------:|--------------:|-----------:|--------------:|
| level | 1.2402 | 0.0236 | 0.0197 | 0.0100 |
| slope | 1.4353 | -0.0128 | 0.0642 | -0.0125 |
| curvature | 3.4101 | 0.0363 | 0.0967 | 0.0261 |

Fitted on 270 monthly curves from July 2002 to December 2024. Put back together at the
starting values, the spread curve is 0.71% at 1 year, rises to 1.30% at 5 years and eases
to 1.09% at 20 years; the long-run values give a curve about twice as wide (2.28% at 1
year, 2.90% at 5 years, 2.52% at 20 years), since the history includes 2008 and 2020.
Level shocks halve in about seven months and the curvature hump in about two and a half.

**References:**

- Diebold, F.X., Li, C. (2006). "Forecasting the Term Structure of Government Bond Yields." Journal of Econometrics, 130(2), 337-364. <https://doi.org/10.1016/j.jeconom.2005.03.005>
- Yu, W., Zivot, E. (2011). "Forecasting the Term Structures of Treasury and Corporate Yields Using Dynamic Nelson-Siegel Models." International Journal of Forecasting, 27(2), 579-591. <https://doi.org/10.1016/j.ijforecast.2010.04.002>
- Uhlenbeck, G.E., Ornstein, L.S. (1930). "On the Theory of the Brownian Motion." Physical Review, 36(5), 823-841. <https://doi.org/10.1103/PhysRev.36.823>
- Christensen, J.H.E., Diebold, F.X., Rudebusch, G.D. (2011). "The Affine Arbitrage-Free Class of Nelson-Siegel Term Structure Models." Journal of Econometrics, 164(1), 4-20. <https://doi.org/10.1016/j.jeconom.2011.02.011>

## fetch_hqm_spreads

```python
fetch_hqm_spreads(period: str) -> tuple[pl.Series, dict[float, pl.Series]]
```

The Treasury's High Quality Market corporate spread curve (HQM par yield minus the Treasury
par yield at 2, 5, 10 and 30 years, monthly from 1984) through the Finance Toolkit, averaged
to `period`, in the dated per-maturity shape `fit_nelson_siegel_factors` takes.

**Raises:**

- <u>ValueError:</u> if no Toolkit was given, or nothing comes back (no FRED key, or a window before 1984).

## params

```python
credittermstructure.params  # property -> YieldCurveParams
```

The last-calibrated credit curve parameters.

**Raises:**

- <u>RuntimeError:</u> if calibrate() hasn't been called yet.

## step_function

```python
credittermstructure.step_function  # property
```

The exact-transition OU step function shared by all three curve
factors (`term_structure_model.step_curve_factor`, reused unchanged;
not Euler-Maruyama, see that function's own docstring).

## changes

```python
credittermstructure.changes  # property -> dict[str, pl.DataFrame]
```

Dated period-over-period changes in each curve factor ("credit_level",
"credit_slope", "credit_curvature"), from the same data calibrate()
already fetched, reused for cross-factor correlation estimation
(Dependence) instead of a second bond-panel scan.

**Returns:**

<u>dict[str, pl.DataFrame]:</u> one entry per curve factor, each two columns, `date` (pl.Date) and `value` (f64); see helpers.dated_changes().

**Raises:**

- <u>RuntimeError:</u> if calibrate() hasn't been called yet.
