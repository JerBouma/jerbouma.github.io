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

The Credit Term Structure module simulates a whole credit spread curve: the extra yield corporate bonds pay over
government bonds at every maturity, rather than one spread per bucket. Three numbers (level, slope and curvature)
move the curve through time, so the spread at any maturity can be read off a simulated scenario.

Where `Credit` gives a handful of fixed spread buckets (1-3 years, 7-10 years, BBB), this gives a
continuous curve, so a 4-year or a 12-year spread exists in every scenario. Added to the simulated government
curve (`yield_curve`), it gives the discount curve a risky bond is priced off, which `BondPricer` uses. It is
opt-in (`credit_term_structure.enabled`) and runs next to `credit`, not instead of it.

The model is the dynamic Nelson-Siegel curve ([Nelson & Siegel, 1987](https://doi.org/10.1086/296409);
[Diebold & Li, 2006](https://doi.org/10.1016/j.jeconom.2005.03.005)) that `yield_curve` uses, applied to corporate
spreads as in [Yu & Zivot (2011)](https://doi.org/10.1016/j.ijforecast.2010.04.002): `credit_level` is the
long-maturity spread, `credit_slope` how far the short end sits below or above it and `credit_curvature` a hump at
medium maturities. Each moves as its own mean-reverting process, correlated with the rest of the model. The
`decay` matches `yield_curve.decay` (0.7308) on purpose: two Nelson-Siegel curves with the same decay add up, so
the government curve plus this spread curve is again one.

Two data sources are available through `source`:

- `hqm` (default): the US Treasury's High Quality Market (HQM) corporate bond curve
  ([US Treasury](https://home.treasury.gov/data/treasury-coupon-issues-and-corporate-bond-yield-curves)) as a
  spread over Treasuries at 2, 5, 10 and 30 years, monthly from 1984, with a free FRED key. Built from AAA, AA and
  A rated bonds, it is the investment-grade curve.
- `bond_panel`: the [Open Source Bond Asset Pricing](https://openbondassetpricing.com/) panel of US corporate bond
  trades (TRACE) from July 2002 to March 2025, a 1.8 GB download. It has no ratings, so it is the average spread
  across all bonds, and it starts from its last month, not today.

Like `yield_curve`, it is fitted to history, with no guarantee against arbitrage between maturities.

Configuration (`credit_term_structure` in a factor set):

| Key | Default | Meaning |
|:----|:--------|:--------|
| `enabled` | `false` | Adds `credit_level`, `credit_slope` and `credit_curvature` to the run. |
| `source` | `hqm` | `hqm` (Treasury HQM spread curve) or `bond_panel` (TRACE bond panel). |
| `tenors` | `[1, 2, 3, 5, 7, 10, 15, 20]` | Bond panel maturities in years, at least 3; unused by `hqm`. |
| `period` | `monthly` | Fitting frequency; `hqm` takes `monthly`, `quarterly` or `yearly`. |
| `decay` | `0.7308` | Nelson-Siegel decay (lambda); keep equal to `yield_curve.decay`. |
| `beliefs.level`, `.slope`, `.curvature` | `null` | Override a fitted process, as in `yield_curve`. |

**References:**

- Nelson, C.R., Siegel, A.F. (1987). "Parsimonious Modeling of Yield Curves." The Journal of Business, 60(4), 473-489. <https://doi.org/10.1086/296409>
- Diebold, F.X., Li, C. (2006). "Forecasting the Term Structure of Government Bond Yields." Journal of Econometrics, 130(2), 337-364. <https://doi.org/10.1016/j.jeconom.2005.03.005>
- Yu, W., Zivot, E. (2011). "Forecasting the Term Structures of Treasury and Corporate Yields Using Dynamic Nelson-Siegel Models." International Journal of Forecasting, 27(2), 579-591. <https://doi.org/10.1016/j.ijforecast.2010.04.002>

## calibrate

```python
calibrate(
    tenors: list[float],
    period: str = 'monthly',
    decay: float = 0.7308,
    source: str = 'bond_panel',
) -> YieldCurveParams
```

Calibrate the credit spread curve from history: summarize each period's spread curve by its Nelson-Siegel
level, slope and curvature, then fit each as its own mean-reverting process.

This learns how the corporate spread curve has moved, so the simulated curves shift, tilt and bend the way the
real one has. Each factor gets a speed (`mean_reversion_speed`), a normal level (`long_run_mean`), a swing size
(`volatility`) and a starting value (`initial_value`), in decimals. `level` is the long-maturity spread and
`level + slope` the shortest one. A level speed of 1.24 a year means a shock halves in about seven months
(ln 2 / 1.24).

The method is that of [Diebold and Li (2006)](https://doi.org/10.1016/j.jeconom.2005.03.005), applied to
corporate spreads as in [Yu and Zivot (2011)](https://doi.org/10.1016/j.ijforecast.2010.04.002).

Also known as: dynamic Nelson-Siegel credit curve, corporate spread term structure fit.

**Args:**

- <u>tenors (list[float]):</u> bond panel maturities in years, at least 3; each bond goes to the nearest one. Unused by "hqm".
- <u>period (str):</u> fitting frequency and time step: "daily", "weekly", "monthly", "quarterly" or "yearly" ("hqm": the last three). Defaults to "monthly", as daily bond spreads are too noisy.
- <u>decay (float):</u> the Nelson-Siegel decay (lambda), annualized; fixed, not fitted. Defaults to 0.7308, as for `yield_curve`, so the two curves add up.
- <u>source (str):</u> "bond_panel" (TRACE trades; the first call downloads about 1.8 GB) or "hqm" (the Treasury's HQM curve; FRED key). Defaults to "bond_panel"; a config defaults to "hqm".

**Returns:**

<u>YieldCurveParams:</u> the fitted `level`, `slope` and `curvature` processes and the `decay`.

**Raises:**

- <u>ValueError:</u> if `source`, `period`, `decay` or `tenors` is invalid, or the HQM curve cannot be read (no Toolkit or FRED key).

**As an example:**

```python
from financescenarios.factors.credit_term_structure.credit_term_structure_controller import (
    CreditTermStructure,
)

credit_curve = CreditTermStructure()
credit_curve.calibrate(tenors=[1, 2, 3, 5, 7, 10, 15, 20], period="monthly")
```

Which returns (calibrated on 2026-10-04, 270 monthly curves from July 2002 to December 2024):

| factor | mean_reversion_speed | long_run_mean | volatility | initial_value |
|:-------|---------------------:|--------------:|-----------:|--------------:|
| level | 1.2402 | 0.0236 | 0.0197 | 0.0100 |
| slope | 1.4353 | -0.0128 | 0.0642 | -0.0125 |
| curvature | 3.4101 | 0.0363 | 0.0967 | 0.0261 |

## fetch_hqm_spreads

```python
fetch_hqm_spreads(period: str) -> tuple[pl.Series, dict[float, pl.Series]]
```

Fetch the Treasury's High Quality Market (HQM) corporate spread curve through the Finance Toolkit: the HQM par
yield minus the Treasury par yield at 2, 5, 10 and 30 years, monthly from 1984, averaged to `period`.

**Args:**

- <u>period (str):</u> "monthly", "quarterly" or "yearly".

**Returns:**

<u>tuple[pl.Series, dict[float, pl.Series]]:</u> the dates, and one spread series per maturity in years.

**Raises:**

- <u>ValueError:</u> if no Toolkit was given, or nothing comes back (no FRED key, or a window before 1984).

## params

```python
credittermstructure.params  # property -> YieldCurveParams
```

The parameters from the last `calibrate` call.

**Raises:**

- <u>RuntimeError:</u> if `calibrate` has not been called yet.

## step_function

```python
credittermstructure.step_function  # property
```

The step function that moves each curve factor forward one time step, using the exact mean-reverting transition.

## changes

```python
credittermstructure.changes  # property -> dict[str, pl.DataFrame]
```

The dated period-over-period changes of `credit_level`, `credit_slope` and `credit_curvature` from the last
`calibrate` call, from which the correlation matrix is estimated.

**Returns:**

<u>dict[str, pl.DataFrame]:</u> one table per factor, with a `date` and a `value` column.

**Raises:**

- <u>RuntimeError:</u> if `calibrate` has not been called yet.
