---
title: "Mortality"
seo_title: "Mortality Reference | Finance Scenarios"
seo_title_suffix: false
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

Mortality improvement with the Cairns-Blake-Dowd model.

```python
from financescenarios.factors.mortality.mortality_controller import Mortality
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
a normal level: mortality improvement is a trend over decades, and its uncertainty grows with the horizon,so the
range of death rates in year 30 is far wider than in year 5. That is the longevity risk a long-dated
liability carries. The logit form keeps every death probability between 0 and 1, and the straight line in age
describes mortality well from about 60 upward, the ages that drive pension and annuity values.
`cbd_mortality_rate(kappa1, kappa2, age, mean_age)` turns the paths back into a death rate, with `mean_age` from
the calibrated parameters.

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

The `mortality` keys of a factor set and their defaults are listed on the reference page
[Configuration Classes](https://www.jeroenbouma.com/projects/financescenarios/docs/reference/configuration-classes).

**References:**

- Cairns, A.J.G., Blake, D., Dowd, K. (2006). "A Two-Factor Model for Stochastic Mortality with Parameter Uncertainty: Theory and Calibration." Journal of Risk and Insurance, 73(4), 687-718. <https://doi.org/10.1111/j.1539-6975.2006.00195.x>
- Eurostat. "Life table by age and sex" (dataset demo_mlifetable). <https://ec.europa.eu/eurostat/databrowser/view/demo_mlifetable/default/table>

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
Mortality(toolkit: Toolkit | None = None)
```

</details>

## fetch_life_table

One European country's historical one-year death probabilities by single year of age, from Eurostat's life
tables: a row per calendar year (oldest first), a column per age, ready for `calibrate`.

This gives how likely a person of each age was to die within the year, for every year Eurostat has recorded
(from 1960 for most countries), so the mortality trend is learned from official national statistics rather than
from a table you provide.

**References:**

- Eurostat. "Life table" (demo_mlifetable). <https://ec.europa.eu/eurostat/databrowser/view/demo_mlifetable/default/table>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fetch_life_table(
    country: str,
    sex: str = 'total',
    min_age: int = 60,
    max_age: int = 84,
) -> tuple[pl.DataFrame, list[float], list[int]]
```

**Args:**

- <u>country (str):</u> a European Economic Area country as Eurostat names it, e.g. "Germany".
- <u>sex (str):</u> "total", "male" or "female". Defaults to "total".
- <u>min_age (int):</u> the youngest age to fit. Defaults to 60: Cairns, Blake and Dowd (2006) fit "mortality rates above the age of 60".
- <u>max_age (int):</u> the oldest age, at most 94. Defaults to 84: Eurostat "extended the calculation of the life table and life expectancy from up to age 85+ to up to age 95+ by single ages" only from reference year 2014 ([metadata](https://ec.europa.eu/eurostat/cache/metadata/en/demo_mor_esms.htm)), so a higher age keeps only recent years.

**Returns:**

<u>tuple[pl.DataFrame, list[float], list[int]]:</u> the death probabilities, the ages of its columns, and the calendar year of each row. Years with a missing age are dropped.

**Raises:**

- <u>ValueError:</u> if no Toolkit was given, the age range is invalid, or Eurostat has no table for the country.

</details>

## calibrate

Calibrate the Cairns-Blake-Dowd mortality model: split every year's death rates into a level (`kappa1`) and an
age slope (`kappa2`), then fit each as a random walk with a yearly trend (`drift`) and swing size (`volatility`).

This measures how fast death rates have been falling and how uncertain that pace is; the scenarios carry that
trend forward, so an annuity's value reflects both the expected improvement and the risk that it runs faster. A
`kappa1` drift of -0.015 means death rates fall by roughly 1.5% a year at every age; `1 / (1 + exp(-kappa1))` is
the one-year death probability at the mean age and `exp(kappa2)` its growth per extra year of age.

Each year's logit mortality is regressed on age, as in
[Cairns, Blake and Dowd (2006)](https://doi.org/10.1111/j.1539-6975.2006.00195.x).

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

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate(
    mortality_rates: pl.DataFrame,
    ages: list[float],
    period: str = 'yearly',
    mortality_years: list[int] | None = None,
) -> CBDParams
```

**Args:**

- <u>mortality_rates (pl.DataFrame):</u> one row per year (oldest first), one column per age, of one-year death probabilities (the Human Mortality Database's `qx`, not `Mx`).
- <u>ages (list[float]):</u> the age of each column, strictly increasing.
- <u>period (str):</u> the data frequency; only "yearly" is supported. Defaults to "yearly".
- <u>mortality_years (list[int] &#124; None):</u> the calendar year of each row, to date the changes. Defaults to None: the last row is taken as last year, with a warning.

**Returns:**

<u>CBDParams:</u> the fitted `kappa1` and `kappa2` processes, `mean_age`, `min_age` and `max_age`.

**Raises:**

- <u>ValueError:</u> if `period` is unknown, `ages` has fewer than 2 entries or does not match the columns, a rate is outside 0 to 1, or `mortality_years` has the wrong length.

</details>

## params

The calibrated mortality model: the `kappa1` and `kappa2` trends and the fitted age range.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
mortality.params  # property -> CBDParams
```

**Raises:**

- <u>RuntimeError:</u> if the model has not been calibrated yet.

</details>

## step_function

The one-step move of `kappa1` and `kappa2`: a random walk with drift, so improvement continues at the fitted
pace with no pull back to a past level.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
mortality.step_function  # property
```

</details>

## changes

The historical yearly changes of `mortality_level` and `mortality_slope`, the input for their correlation with
the other factors.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
mortality.changes  # property -> dict[str, pl.DataFrame]
```

**Returns:**

<u>dict[str, pl.DataFrame]:</u> one table per factor, with a `date` and a `value` column.

**Raises:**

- <u>RuntimeError:</u> if the model has not been calibrated yet.

</details>

## How It Is Calculated

The model functions behind this page, each with the formula it implements.

### cbd_mortality_rate

The one-year probability of death at a given age in a simulated year, read back from the two Cairns-Blake-Dowd
factors: the level `kappa1` and the age slope `kappa2`.

The model assumes that, at pension ages, the log-odds of dying rise in a straight line with age, so two numbers
per year describe the whole table: how high mortality is at the mean age and how fast it climbs with every extra
year of age. Feeding in simulated factor paths gives a death probability per scenario and year, the input for an
annuity or pension liability, and an improving `kappa1` lowers mortality at every age at once. Working on the
logit keeps every probability between 0 and 1, however far a scenario runs
([Cairns, Blake and Dowd, 2006](https://doi.org/10.1111/j.1539-6975.2006.00195.x)).

The formula is as follows:

$$
\text{logit}\; q (x,\; t) = \operatorname{kappa1}(t) + \operatorname{kappa2}(t) \cdot (x - \text{xbar})
$$

$$
q(x,\; t) = 1 / (1 + \exp(- (\operatorname{kappa1}(t) + \operatorname{kappa2}(t) \cdot (x - \text{xbar}))))
$$

Where xbar is the mean age of the fit.

**References:**

- Cairns, A.J.G., Blake, D., Dowd, K. (2006). "A Two-Factor Model for Stochastic Mortality with Parameter Uncertainty: Theory and Calibration." Journal of Risk and Insurance, 73(4), 687-718. <https://doi.org/10.1111/j.1539-6975.2006.00195.x>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

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

**Args:**

- <u>kappa1 (float &#124; np.ndarray):</u> the simulated mortality level.
- <u>kappa2 (float &#124; np.ndarray):</u> the simulated age slope.
- <u>age (float):</u> the age to read the death probability for.
- <u>mean_age (float):</u> the mean age of the fitted ages, `mean_age` in the calibrated parameters.
- <u>min_age (float &#124; None):</u> the youngest fitted age; with `max_age`, warns when `age` lies outside the fitted range, where the straight-line logit is not validated. Defaults to None.
- <u>max_age (float &#124; None):</u> the oldest fitted age, paired with `min_age`. Defaults to None.

**Returns:**

<u>float &#124; np.ndarray:</u> the one-year death probability at `age`, per scenario and year when paths are passed.

</details>

### fit_cbd_factors

Split each year's mortality table into the two Cairns-Blake-Dowd factors: the level `kappa1` and the age slope
`kappa2`, by regressing that year's log-odds of death on age.

This turns a table with dozens of ages per year into two time series, whose trend and volatility are what the
longevity scenarios project: a falling `kappa1` is mortality improvement at every age, a changing `kappa2` means
older ages improve faster or slower than younger ones. A straight line in age fits mortality well from about 60
upward, the range that matters for pensions and annuities
([Cairns, Blake and Dowd, 2006](https://doi.org/10.1111/j.1539-6975.2006.00195.x)), fitted the paper's way: "For
each t, A1 and A2 were estimated using least squares by transforming the ungraduated mortality rates from qy to
log qy/py = A1 + A2 y + error" (footnote 8; working-paper version, Pensions Institute PI-0611).

The formula is as follows:

$$
\ln(q(x_{j},\; t) / (1 - q(x_{j},\; t))) = \operatorname{kappa1}(t) + \operatorname{kappa2}(t) \cdot (x_{j} - \text{xbar}) + e_{t},\;\; \text{j}
$$

Where q(x_j, t) is the one-year probability of death at age x_j in year t and xbar the mean age.

**References:**

- Cairns, A.J.G., Blake, D., Dowd, K. (2006). "A Two-Factor Model for Stochastic Mortality with Parameter Uncertainty: Theory and Calibration." Journal of Risk and Insurance, 73(4), 687-718. <https://doi.org/10.1111/j.1539-6975.2006.00195.x>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fit_cbd_factors(mortality_rates: pl.DataFrame, ages: list[float]) -> tuple[pl.DataFrame, float]
```

**Args:**

- <u>mortality_rates (pl.DataFrame):</u> one row per calendar year, one column per age, of one-year death probabilities q(x, t), not central death rates m(x, t) (q = 1 - e^(-m)).
- <u>ages (list[float]):</u> the age of each column, strictly increasing.

**Returns:**

<u>tuple[pl.DataFrame, float]:</u> `kappa1` and `kappa2` per year, and the mean age the ages are centred on.

**Raises:**

- <u>ValueError:</u> if fewer than 2 ages are given, `ages` is not strictly increasing or does not match the columns, or a rate is not strictly between 0 and 1.

</details>
