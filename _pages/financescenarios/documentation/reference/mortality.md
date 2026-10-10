---
title: "Mortality"
seo_title: "Mortality Reference – Finance Scenarios"
excerpt: "Mortality improvement with the Cairns-Blake-Dowd model."
description: "Mortality improvement with the Cairns-Blake-Dowd model."
author_profile: false
permalink: /projects/financescenarios/docs/reference/mortality
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

Mortality improvement with the Cairns-Blake-Dowd model. Generated from the docstrings of Finance Scenarios 0.1.0; `help(...)` in Python shows the same text.

```python
from financescenarios.factors.mortality.mortality_controller import Mortality
```

```python
Mortality(toolkit: Toolkit | None = None)
```

The Mortality module simulates how death rates at older ages change over the coming years:
the longevity risk a pension fund or annuity provider carries when people live longer than
expected. Mortality has fallen steadily for decades, but not at a fixed pace, and that
uncertain trend is what this module captures.

In plain terms: hand it a table of historical death rates by age and year, and every
simulated scenario gets a path for the overall mortality level and for how steeply mortality
rises with age, linked to interest rates, equities and the rest through the correlation
matrix. From those two paths the death rate at any age in any simulated year can be read
back, which is what a pension or annuity liability needs. It is opt-in
(`mortality.enabled`) and stays off even in the shipped `default.yaml` and `broad.yaml`, since there is no
default data to turn it on with.

The model is the two-factor [Cairns-Blake-Dowd (2006)](https://doi.org/10.1111/j.1539-6975.2006.00195.x)
model. In each calendar year `t`, the one-year probability of death `q(x, t)` at age `x`
follows `logit(q(x, t)) = kappa1(t) + kappa2(t) * (x - mean_age)`, where the logit is
`log(q / (1 - q))` and `mean_age` is the average of the fitted ages. `kappa1` is the level:
raising it moves mortality up or down at every age alike. `kappa2` is the age slope: raising
it steepens the rise of mortality with age, so older ages move more than younger ones. Both
factors are found per year by a cross-sectional regression (`mortality_model.fit_cbd_factors`),
the same per-date pattern `term_structure_model.fit_nelson_siegel_factors` uses to split a
yield curve into level, slope and curvature, only regressing logit mortality on centered age.

Unlike every mean-reverting factor elsewhere in this project, `kappa1` and `kappa2` are each
calibrated and simulated as a random walk with drift, `dx = mu*dt + sigma*dW`, with no pull
back to a normal level (`calibration_model.fit_random_walk_process` and
`step_random_walk_process`). This follows CBD's own specification: mortality improvement is
a sustained trend over decades, not a level that returns to a historical average.
`RandomWalkParams` is the generic counterpart to `OUParams` for any factor of that shape. The
two factors enter the simulation as `mortality_level` and `mortality_slope`, correlated with
the rest of the model through the correlation matrix, with no cascade dependency on or from
any other factor.

To turn simulated paths back into a death rate at a given age, use
`mortality_model.cbd_mortality_rate(kappa1, kappa2, age, mean_age)`, with `mean_age` from
`scenarios.mortality.params.mean_age`; it works on whole path arrays at once, the way
`term_structure_model.nelson_siegel_yield` rebuilds a yield at a tenor.

The data come one of two ways (`source`). With `source: eurostat`, the life table of a
European Economic Area `country` is fetched through the Finance Toolkit
(`economics.get_life_table`, Eurostat dataset `demo_mlifetable`, yearly from 1960 for most
countries, no API key): the one-year death probabilities of `sex` for every age from
`min_age` to `max_age` (60 to 84 by default: the model's straight-line logit is built for
old ages, and many countries published single ages only up to an "85 and over" group
until the 2010s, so a higher `max_age` keeps only recent years; at most 94, since the
95-and-over group dies with probability 1). With
`source: supplied`, the default, the caller loads a historical mortality table (from the
[Human Mortality Database](https://www.mortality.org/), a Society of Actuaries period life
table or a national statistics agency, for any country) and passes it in:

```python
result = scenarios.simulate(
    config,
    mortality_rates=mortality_rates,  # pl.DataFrame: one row per year, one column per age
    mortality_ages=[60.0, 65.0, 70.0, 75.0, 80.0, 85.0],
)
```

`Scenarios.calibrate()` accepts the same `mortality_rates`/`mortality_ages` (and
`mortality_years`), and `simulate()` forwards them when no pre-built `CalibrationResult` is
given. If `mortality.enabled` is true with `source: supplied` and neither is given, calibration raises a
`ValueError` rather than silently skipping the factor. Cohort effects (generations whose
mortality improves differently from their neighbors, the extensions to CBD) are deliberately
not modeled; see the coverage overview.

Configuration (`mortality` in a factor set):

| Key | Default | Meaning |
|:----|:--------|:--------|
| `enabled` | `false` | Adds `mortality_level` and `mortality_slope`. |
| `source` | `supplied` | `supplied` (pass `mortality_rates`/`mortality_ages`) or `eurostat` (fetched). |
| `country` | `Germany` | Eurostat country for `source: eurostat`. |
| `sex` | `total` | `total`, `male` or `female`, for `source: eurostat`. |
| `min_age` / `max_age` | `60` / `84` | Ages fitted with `source: eurostat`; above 84 keeps fewer years, at most 94. |
| `period` | `yearly` | Only `yearly` is supported; mortality tables are annual. |
| `beliefs.kappa1.drift` | `null` | Override the level factor's fitted drift. |
| `beliefs.kappa1.volatility` | `null` | Override the level factor's fitted volatility; must be above 0. |
| `beliefs.kappa2.drift` | `null` | Override the age-slope factor's fitted drift. |
| `beliefs.kappa2.volatility` | `null` | Override the age-slope factor's fitted volatility; must be above 0. |

A belief left as `null` keeps the fitted value, through `config_model.apply_mortality_beliefs`
and `apply_random_walk_beliefs`. Beliefs are in logit units per year: a `kappa1.drift` of
-0.02 means death rates fall by roughly 2% a year at every age.

**References:**

- Cairns, A.J.G., Blake, D., Dowd, K. (2006). "A Two-Factor Model for Stochastic Mortality with Parameter Uncertainty: Theory and Calibration." Journal of Risk and Insurance, 73(4), 687-718. <https://doi.org/10.1111/j.1539-6975.2006.00195.x>
- Human Mortality Database. University of California, Berkeley (USA), and Max Planck Institute for Demographic Research (Germany). <https://www.mortality.org/>
- Eurostat. "Life table by age and sex" (dataset demo_mlifetable). <https://ec.europa.eu/eurostat/databrowser/view/demo_mlifetable/default/table>

## fetch_life_table

```python
fetch_life_table(
    country: str,
    sex: str = 'total',
    min_age: int = 60,
    max_age: int = 84,
) -> tuple[pl.DataFrame, list[float], list[int]]
```

Fetch one country's historical one-year death probabilities (q, Eurostat's `qx`) by single
year of age through the Finance Toolkit (`economics.get_life_table`), in the shape `calibrate`
takes: a row per calendar year (oldest first), a column per age.

In plain terms: this downloads how likely a person of each age was to die within the year,
for every year Eurostat has recorded (from 1960 for most countries), so the mortality trend
is learned from official national statistics rather than from a table you provide.

**Args:**

- <u>country (str):</u> a European Economic Area country as Eurostat names it, e.g. "Germany".
- <u>sex (str):</u> "total", "male" or "female".
- <u>min_age (int):</u> the youngest age to fit; 60 by default, where the Cairns-Blake-Dowd model's straight-line logit is designed to hold.
- <u>max_age (int):</u> the oldest age; 84 by default, since many countries published single ages only up to an "85 and over" group until the 2010s (Germany until 2013), so a higher age keeps only the recent years. At most 94: the 95-and-over group dies with probability 1 and has no logit.

**Returns:**

<u>tuple[pl.DataFrame, list[float], list[int]]:</u> the death probabilities, the ages of its columns, and the calendar year of each row. Years with a missing age are dropped.

**Raises:**

- <u>ValueError:</u> if no Toolkit was given, the age range is invalid, or Eurostat has no table for the country.

**References:**

- Eurostat. "Life table" (demo_mlifetable). <https://ec.europa.eu/eurostat/databrowser/view/demo_mlifetable/default/table>

## calibrate

```python
calibrate(
    mortality_rates: pl.DataFrame,
    ages: list[float],
    period: str = 'yearly',
    mortality_years: list[int] | None = None,
) -> CBDParams
```

Calibrate the Cairns-Blake-Dowd mortality model from a historical mortality table: split
every year's death rates into a level (`kappa1`) and an age slope (`kappa2`), then fit
each as a random walk with drift, with its own yearly trend (`drift`) and swing size
(`volatility`).

In plain terms: this learns from the past how fast death rates have been falling and
how uncertain that pace is, so the simulated scenarios carry on the trend with realistic
surprises around it. A `kappa1` drift of -0.015, for example, means death rates fall by
roughly 1.5% a year at every age, halving in about 45 years (ln 2 / 0.015).

Both factors are in logit units (`log(q / (1 - q))`). `kappa1` is the logit death rate at
the mean age, so `1 / (1 + exp(-kappa1))` is that age's one-year probability of death;
`kappa2` is how much the logit rises per year of age, so `exp(kappa2)` is the factor by
which mortality grows with each extra year of age. `initial_value` is the last year in
the table, and `mean_age`, `min_age` and `max_age` record the fitted age range.

Also known as: CBD model, stochastic mortality calibration, longevity trend fit.

**Args:**

- <u>mortality_rates (pl.DataFrame):</u> one row per calendar year (oldest first), one column per age in `ages` (same order), one-year mortality rates q(x, t) in (0, 1). CBD models q, the probability of death within one year, not the *central* mortality rate m(x, t) (related by q = 1 - e^(-m)). This matters for the Human Mortality Database, which exports both `Mx` (central rate) and `qx` (one-year rate); feeding `Mx` here validates cleanly (both are typically < 1 at working ages) but silently biases the fit (~2% relative discrepancy at age 90, non-negligible for pension liability); use `qx`. Eurostat's equivalent is `indic_de=PROBDEATH`.
- <u>ages (list[float]):</u> the ages each column of mortality_rates corresponds to, same order as its columns, strictly increasing.
- <u>period (str):</u> sampling frequency of the underlying data; only "yearly" is supported, since mortality-rate tables are conventionally annual.
- <u>mortality_years (list[int] &#124; None):</u> the calendar year each row of mortality_rates corresponds to (oldest first, same order/length as its rows), used only to date changes() for cross-factor correlation alignment (dependence_model.align_factor_series_by_date), not the CBD fit itself. Defaults to None, which assumes the table's last row is the most recently completed calendar year (consistent with every other factor's own history ending "as of today") and counts backward, with a warning; pass this explicitly if that assumption doesn't hold for your table (e.g. a projection table whose last row is a future year, or historical rates as of a specific past cutoff).

**Returns:**

<u>CBDParams:</u> the calibrated kappa1 and kappa2 processes, the mean age used to center the age axis, and the youngest and oldest fitted ages.

**Raises:**

- <u>ValueError:</u> if period is not recognized, fewer than 2 ages are supplied, `ages` doesn't match mortality_rates' column count or isn't strictly increasing, any rate is not strictly between 0 and 1, or `mortality_years` is supplied but its length doesn't match mortality_rates' row count.

**Notes:**

- With exactly 2 ages the regression fits perfectly by construction, so a warning is
  logged: there is no goodness-of-fit signal. CBD's own paper fits ages 60 to 89.
- The logit-linear shape is a local approximation: reading a death rate back far outside
  the fitted ages (say age 30 from a 60-89 fit) is not supported by the calibration, and
  `cbd_mortality_rate` warns when given `min_age`/`max_age`.
- Both factors' changes feed the correlation matrix as `mortality_level` and
  `mortality_slope`; with yearly data and a short table that correlation is estimated
  from few points.

**As an example:**

```python
import pandas as pd
import polars as pl

from financescenarios.factors.mortality.mortality_controller import Mortality

ages = [60, 64, 68, 72, 76, 80, 84]
url = (
    "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/demo_mlifetable/"
    "A.PROBDEATH.T." + "+".join(f"Y{age}" for age in ages) + ".NL?format=SDMX-CSV"
)
table = pd.read_csv(url).pivot(index="TIME_PERIOD", columns="age", values="OBS_VALUE").dropna()
table = table[[f"Y{age}" for age in ages]]  # Dutch one-year death probabilities, 1985-2024

mortality = Mortality()
mortality.calibrate(
    pl.from_pandas(table.reset_index(drop=True)),
    ages=[float(age) for age in ages],
    mortality_years=table.index.to_list(),
)
```

Which returns (calibrated on 2026-10-04):

| factor | drift | volatility | initial_value |
|:-------|------:|-----------:|--------------:|
| kappa1 | -0.0153 | 0.0272 | -3.9380 |
| kappa2 | 0.0003 | 0.0019 | 0.1105 |

With `mean_age` 72.0, `min_age` 60.0 and `max_age` 84.0, fitted on 40 years of Dutch
data. A 72-year-old in 2024 had a 1.9% chance of dying within the year
(1 / (1 + exp(3.938))), and each extra year of age raised that by about 12% (exp(0.1105)).
The level falls by about 1.5% a year, so a 65-year-old's 0.89% today drifts to about
0.75% in ten years; the age slope barely moves.

**References:**

- Cairns, A.J.G., Blake, D., Dowd, K. (2006). "A Two-Factor Model for Stochastic Mortality with Parameter Uncertainty: Theory and Calibration." Journal of Risk and Insurance, 73(4), 687-718. <https://doi.org/10.1111/j.1539-6975.2006.00195.x>

## params

```python
mortality.params  # property -> CBDParams
```

The last-calibrated CBD parameters.

**Raises:**

- <u>RuntimeError:</u> if calibrate() hasn't been called yet.

## step_function

```python
mortality.step_function  # property
```

The Euler-Maruyama step function shared by both kappa1 and kappa2.

## changes

```python
mortality.changes  # property -> dict[str, pl.DataFrame]
```

Dated period-over-period changes in each kappa factor ("mortality_level",
"mortality_slope"), from the same data calibrate() already fit, reused for
cross-factor correlation estimation (Dependence).

**Returns:**

<u>dict[str, pl.DataFrame]:</u> one entry per kappa factor, each two columns, `date` (pl.Date) and `value` (f64); see helpers.dated_changes().

**Raises:**

- <u>RuntimeError:</u> if calibrate() hasn't been called yet.
