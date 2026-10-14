---
title: "CreditTermStructure"
seo_title: "CreditTermStructure Reference | Finance Scenarios"
seo_title_suffix: false
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

A Nelson-Siegel credit spread curve.

```python
from financescenarios.factors.credit_term_structure.credit_term_structure_controller import CreditTermStructure
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
medium maturities. Each moves as its own mean-reverting process, correlated with the rest of the model, so the
curve can widen in parallel, steepen or invert (short spreads above long ones, as in 2008) but returns toward its
usual shape. Three factors are enough because spread curves, like yield curves, move mostly in these three ways,
and they keep every maturity consistent with every other. The factors are normally distributed, so a spread can
turn slightly negative in a benign tail scenario. The
`decay` matches `yield_curve.decay` (0.7308) on purpose: two Nelson-Siegel curves with the same decay add up, so
the government curve plus this spread curve is again one. The value is Diebold and Li's: "Two- or three-year
maturities are commonly used in that regard, so we simply picked the average, 30 months. The λ value that
maximizes the loading on the medium-term factor at exactly 30 months is λ=0.0609" (working-paper version,
section 3, [NBER w10048](https://www.nber.org/papers/w10048)), monthly, so 0.0609 × 12 = 0.7308 a year.

Two data sources are available through `source`:

- `hqm` (default): the US Treasury's High Quality Market (HQM) corporate bond curve
  ([US Treasury](https://home.treasury.gov/data/treasury-coupon-issues-and-corporate-bond-yield-curves)) as a
  spread over Treasuries at 2, 5, 10 and 30 years, monthly from 1984, with a free FRED key. It is the
  investment-grade curve: "The HQM yield curve pertains to the high quality corporate bond market, i.e., corporate
  bonds rated AAA, AA, or A" (Girola, 2011, "The HQM Yield Curve: Basic Concepts", slide 2,
  [US Treasury](https://home.treasury.gov/system/files/226/ycp_oct2011.pdf)).
- `bond_panel`: the [Open Source Bond Asset Pricing](https://openbondassetpricing.com/) panel of US corporate bond
  trades (TRACE) from July 2002 to March 2025, a 1.8 GB download. It has no ratings, so it is the average spread
  across all bonds, and it starts from its last month, not today.

Like `yield_curve`, it is fitted to history, with no guarantee against arbitrage between maturities.

The `credit_term_structure` keys of a factor set and their defaults are listed on the reference page
[Configuration Classes](https://www.jeroenbouma.com/projects/financescenarios/docs/reference/configuration-classes).

**References:**

- Nelson, C.R., Siegel, A.F. (1987). "Parsimonious Modeling of Yield Curves." The Journal of Business, 60(4), 473-489. <https://doi.org/10.1086/296409>
- Diebold, F.X., Li, C. (2006). "Forecasting the Term Structure of Government Bond Yields." Journal of Econometrics, 130(2), 337-364. <https://doi.org/10.1016/j.jeconom.2005.03.005>
- Yu, W., Zivot, E. (2011). "Forecasting the Term Structures of Treasury and Corporate Yields Using Dynamic Nelson-Siegel Models." International Journal of Forecasting, 27(2), 579-591. <https://doi.org/10.1016/j.ijforecast.2010.04.002>

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
CreditTermStructure(bond_panel: BondPanel | None = None, toolkit: Toolkit | None = None)
```

</details>

## calibrate

Calibrate the credit spread curve from history: summarize each period's spread curve by its Nelson-Siegel
level, slope and curvature, then fit each as its own mean-reverting process.

Fitting to history means the simulated curves shift, tilt and bend the way the real one has, with the same
speed of recovery after a credit shock. Each factor gets a speed (`mean_reversion_speed`), a normal level
(`long_run_mean`), a swing size (`volatility`) and a starting value (`initial_value`), in decimals.
`level` is the long-maturity spread and `level + slope` the shortest one. A level speed of 1.24 a year means a
shock halves in about seven months (ln 2 / 1.24).

The method is that of [Diebold and Li (2006)](https://doi.org/10.1016/j.jeconom.2005.03.005), applied to
corporate spreads as in [Yu and Zivot (2011)](https://doi.org/10.1016/j.ijforecast.2010.04.002).

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

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate(
    tenors: list[float],
    period: str = 'monthly',
    decay: float = 0.7308,
    source: str = 'bond_panel',
) -> YieldCurveParams
```

**Args:**

- <u>tenors (list[float]):</u> bond panel maturities in years, at least 3; each bond goes to the nearest one. Unused by "hqm".
- <u>period (str):</u> fitting frequency and time step: "daily", "weekly", "monthly", "quarterly" or "yearly" ("hqm": the last three). Defaults to "monthly", as daily bond spreads are too noisy.
- <u>decay (float):</u> the Nelson-Siegel decay (lambda), annualized; fixed, not fitted. Defaults to 0.7308, as for `yield_curve`, so the two curves add up.
- <u>source (str):</u> "bond_panel" (TRACE trades; the first call downloads about 1.8 GB) or "hqm" (the Treasury's HQM curve; FRED key). Defaults to "bond_panel"; a config defaults to "hqm".

**Returns:**

<u>YieldCurveParams:</u> the fitted `level`, `slope` and `curvature` processes and the `decay`.

**Raises:**

- <u>ValueError:</u> if `source`, `period`, `decay` or `tenors` is invalid, or the HQM curve cannot be read (no Toolkit or FRED key).

</details>

## fetch_hqm_spreads

The Treasury's High Quality Market (HQM) corporate spread curve: the yield of high-grade (AAA to A) US corporate
bonds over Treasuries at 2, 5, 10 and 30 years, monthly from 1984, averaged to `period`. This is the history
the default `hqm` source calibrates on.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fetch_hqm_spreads(period: str) -> tuple[pl.Series, dict[float, pl.Series]]
```

**Args:**

- <u>period (str):</u> "monthly", "quarterly" or "yearly".

**Returns:**

<u>tuple[pl.Series, dict[float, pl.Series]]:</u> the dates, and one spread series per maturity in years.

**Raises:**

- <u>ValueError:</u> if no Toolkit was given, or nothing comes back (no FRED key, or a window before 1984).

</details>

## params

The calibrated spread curve: the level, slope and curvature processes and the decay.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
credittermstructure.params  # property -> YieldCurveParams
```

**Raises:**

- <u>RuntimeError:</u> if the curve has not been calibrated yet.

</details>

## step_function

The one-step move of each curve factor: the exact mean-reverting step, so the speed of recovery does not depend
on the time step.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
credittermstructure.step_function  # property
```

</details>

## changes

The historical period-over-period changes of `credit_level`, `credit_slope` and `credit_curvature`, the input
for their correlation with each other and with the other factors.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
credittermstructure.changes  # property -> dict[str, pl.DataFrame]
```

**Returns:**

<u>dict[str, pl.DataFrame]:</u> one table per factor, with a `date` and a `value` column.

**Raises:**

- <u>RuntimeError:</u> if the curve has not been calibrated yet.

</details>
