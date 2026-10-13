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

The Mortality module simulates how death rates at older ages change over the coming years: the longevity risk a
pension fund or annuity provider carries when people live longer than expected. Mortality has fallen steadily for
decades, but not at a fixed pace, and that uncertain trend is what this module captures.

Give it a table of historical death rates by age and year, and every scenario gets a path for the overall
mortality level and for how steeply mortality rises with age, correlated with rates, equities and the rest. From
those two paths the death rate at any age in any simulated year can be read back, which is what a pension or
annuity liability needs. It is opt-in (`mortality.enabled`) and off in the shipped factor sets.

The model is the two-factor [Cairns-Blake-Dowd (2006)](https://doi.org/10.1111/j.1539-6975.2006.00195.x) model:

`logit(q(x, t)) = kappa1(t) + kappa2(t) * (x - mean_age)`

where `q(x, t)` is the one-year probability of death at age `x` in year `t`, the logit is `log(q / (1 - q))` and
`mean_age` the average fitted age. `kappa1` is the level, moving mortality at every age alike; `kappa2` is the age
slope. Both are simulated as a random walk with drift (`mortality_level`, `mortality_slope`), with no pull back to
a normal level: mortality improvement is a trend over decades. `cbd_mortality_rate(kappa1, kappa2, age, mean_age)`
turns the paths back into a death rate, with `mean_age` from `scenarios.mortality.params.mean_age`.

The data come one of two ways (`source`):

- `supplied` (default): you pass a historical table, for example from the
  [Human Mortality Database](https://www.mortality.org/), a Society of Actuaries table or a national statistics
  agency, for any country. Without one, calibration raises a `ValueError` rather than skipping the factor.
- `eurostat`: a European country's life table is fetched through the Finance Toolkit (yearly from 1960 for most
  countries, no API key), for ages 60 to 84 by default.

```python
result = scenarios.simulate(
    config,
    mortality_rates=mortality_rates,  # pl.DataFrame: one row per year, one column per age
    mortality_ages=[60.0, 65.0, 70.0, 75.0, 80.0, 85.0],
)
```

Configuration (`mortality` in a factor set):

| Key | Default | Meaning |
|:----|:--------|:--------|
| `enabled` | `false` | Adds `mortality_level` and `mortality_slope`. |
| `source` | `supplied` | `supplied` (pass `mortality_rates`/`mortality_ages`) or `eurostat` (fetched). |
| `country` / `sex` | `Germany` / `total` | Eurostat country, and `total`, `male` or `female`. |
| `min_age` / `max_age` | `60` / `84` | Ages fitted with `source: eurostat`; at most 94. |
| `period` | `yearly` | Only `yearly` is supported; mortality tables are annual. |
| `beliefs.kappa1`, `.kappa2` | `null` | Override a fitted `drift` or `volatility` (logit units per year). |

**References:**

- Cairns, A.J.G., Blake, D., Dowd, K. (2006). "A Two-Factor Model for Stochastic Mortality with Parameter Uncertainty: Theory and Calibration." Journal of Risk and Insurance, 73(4), 687-718. <https://doi.org/10.1111/j.1539-6975.2006.00195.x>
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

Fetch one country's historical one-year death probabilities (Eurostat's `qx`) by single year of age through the
Finance Toolkit, in the shape `calibrate` takes: a row per calendar year (oldest first), a column per age.

This downloads how likely a person of each age was to die within the year, for every year Eurostat has recorded
(from 1960 for most countries), so the mortality trend is learned from official national statistics rather than
from a table you provide.

**Args:**

- <u>country (str):</u> a European Economic Area country as Eurostat names it, e.g. "Germany".
- <u>sex (str):</u> "total", "male" or "female". Defaults to "total".
- <u>min_age (int):</u> the youngest age to fit. Defaults to 60, where the Cairns-Blake-Dowd model's straight-line logit is designed to hold.
- <u>max_age (int):</u> the oldest age, at most 94. Defaults to 84, since many countries published single ages only up to an "85 and over" group until the 2010s, so a higher age keeps only recent years.

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

Calibrate the Cairns-Blake-Dowd mortality model: split every year's death rates into a level (`kappa1`) and an
age slope (`kappa2`), then fit each as a random walk with a yearly trend (`drift`) and swing size (`volatility`).

This learns how fast death rates have been falling and how uncertain that pace is. A `kappa1` drift of -0.015
means death rates fall by roughly 1.5% a year at every age; `1 / (1 + exp(-kappa1))` is the one-year death
probability at the mean age and `exp(kappa2)` its growth per extra year of age.

Each year's logit mortality is regressed on age, as in
[Cairns, Blake and Dowd (2006)](https://doi.org/10.1111/j.1539-6975.2006.00195.x).

Also known as: CBD model, stochastic mortality calibration, longevity trend fit.

**Args:**

- <u>mortality_rates (pl.DataFrame):</u> one row per year (oldest first), one column per age, of one-year death probabilities (the Human Mortality Database's `qx`, not `Mx`).
- <u>ages (list[float]):</u> the age of each column, strictly increasing.
- <u>period (str):</u> the data frequency; only "yearly" is supported. Defaults to "yearly".
- <u>mortality_years (list[int] &#124; None):</u> the calendar year of each row, to date the changes. Defaults to None: the last row is taken as last year, with a warning.

**Returns:**

<u>CBDParams:</u> the fitted `kappa1` and `kappa2` processes, `mean_age`, `min_age` and `max_age`.

**Raises:**

- <u>ValueError:</u> if `period` is unknown, `ages` has fewer than 2 entries or does not match the columns, a rate is outside 0 to 1, or `mortality_years` has the wrong length.

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

Which returns (calibrated on 2026-10-04, `mean_age` 72.0):

| factor | drift | volatility | initial_value |
|:-------|------:|-----------:|--------------:|
| kappa1 | -0.0153 | 0.0272 | -3.9380 |
| kappa2 | 0.0003 | 0.0019 | 0.1105 |

A 72-year-old in 2024 had a 1.9% chance of dying within the year.

## params

```python
mortality.params  # property -> CBDParams
```

The parameters from the last `calibrate` call.

**Raises:**

- <u>RuntimeError:</u> if `calibrate` has not been called yet.

## step_function

```python
mortality.step_function  # property
```

The step function that moves `kappa1` and `kappa2` forward one time step as a random walk with drift.

## changes

```python
mortality.changes  # property -> dict[str, pl.DataFrame]
```

The dated period-over-period changes of `mortality_level` and `mortality_slope` from the last `calibrate` call,
from which the correlation matrix is estimated.

**Returns:**

<u>dict[str, pl.DataFrame]:</u> one table per factor, with a `date` and a `value` column.

**Raises:**

- <u>RuntimeError:</u> if `calibrate` has not been called yet.

## How It Is Calculated

The model functions behind this page, each with the formula it implements.

### cbd_mortality_rate

```python
cbd_mortality_rate(
    kappa1: float | np.ndarray,
    kappa2: float | np.ndarray,
    age: float,
    mean_age: float,
    min_age: float | None = None,
    max_age: float | None = None,
) -> float | np.ndarray
```

Reconstruct the one-year mortality rate q(x, t) at a given age from CBD kappa1/kappa2 factor values. Works on
scalars and on simulated path arrays shaped `(n_simulations, n_steps + 1)` alike, by broadcasting.

The formula is as follows:

$$
\text{logit}\; q (x,\; t) = \operatorname{kappa1}(t) + \operatorname{kappa2}(t) \cdot (x - \text{xbar})
$$

$$
q(x,\; t) = 1 / (1 + \exp(- (\operatorname{kappa1}(t) + \operatorname{kappa2}(t) \cdot (x - \text{xbar}))))
$$

**Args:**

- <u>kappa1 (float &#124; np.ndarray):</u> the level factor value(s).
- <u>kappa2 (float &#124; np.ndarray):</u> the age-slope factor value(s).
- <u>age (float):</u> the age to reconstruct the mortality rate for.
- <u>mean_age (float):</u> the mean age the model was fit against (CBDParams.mean_age).
- <u>min_age (float &#124; None):</u> the youngest age the model was fit against (CBDParams.min_age). When given (along with max_age), warns if `age` falls outside the fitted range; the logit-linear form is a local approximation, not validated to extrapolate reliably beyond it.
- <u>max_age (float &#124; None):</u> the oldest age the model was fit against (CBDParams.max_age), paired with min_age above.

**Returns:**

<u>float &#124; np.ndarray:</u> the reconstructed mortality rate q(x, t) at `age`, in (0, 1), same shape as the factor inputs.

**References:**

- Cairns, A.J.G., Blake, D., Dowd, K. (2006). "A Two-Factor Model for Stochastic Mortality with Parameter Uncertainty: Theory and Calibration." Journal of Risk and Insurance, 73(4), 687-718. <https://doi.org/10.1111/j.1539-6975.2006.00195.x>

### fit_cbd_factors

```python
fit_cbd_factors(mortality_rates: pl.DataFrame, ages: list[float]) -> tuple[pl.DataFrame, float]
```

Cross-sectionally fit CBD kappa1 (level) and kappa2 (age-slope) factors at every
calendar year, via OLS regression of that year's logit-transformed mortality
rates (across ages) on age centered at the mean age. Since the design matrix
depends only on the (fixed) age set, not on the year, this is one linear system
solved for every year at once, the CBD analogue of
term_structure_model.fit_nelson_siegel_factors's per-date cross-sectional fit.

The formula is as follows:

$$
\ln(q(x_{j},\; t) / (1 - q(x_{j},\; t))) = \operatorname{kappa1}(t) + \operatorname{kappa2}(t) \cdot (x_{j} - \text{xbar}) + e_{t},\;\; \text{j}
$$

**Args:**

- <u>mortality_rates (pl.DataFrame):</u> one row per calendar year, one column per age in `ages` (same order), one-year mortality rates q(x, t) in (0, 1), not the *central* mortality rate m(x, t) (q = 1 - e^(-m)); see `mortality_controller.Mortality.calibrate`'s own docstring for the practical caveat.
- <u>ages (list[float]):</u> the ages each column corresponds to, same order as mortality_rates' columns.

**Returns:**

<u>tuple[pl.DataFrame, float]:</u> a DataFrame with "kappa1"/"kappa2" columns (one row per calendar year, in the same year order as the input rows), and the mean age used to center the age axis (needed later to reconstruct mortality rates from simulated factors via cbd_mortality_rate).

**Raises:**

- <u>ValueError:</u> if fewer than 2 ages are supplied, `ages` isn't strictly increasing, `ages` doesn't match mortality_rates' column count, or any rate is not strictly between 0 and 1.

**References:**

- Cairns, A.J.G., Blake, D., Dowd, K. (2006). "A Two-Factor Model for Stochastic Mortality with Parameter Uncertainty: Theory and Calibration." Journal of Risk and Insurance, 73(4), 687-718. <https://doi.org/10.1111/j.1539-6975.2006.00195.x>
