---
title: "Credit"
seo_title: "Credit Reference – Finance Scenarios"
excerpt: "Credit spreads by maturity, rating bucket or country."
description: "Credit spreads by maturity, rating bucket or country."
author_profile: false
permalink: /projects/financescenarios/docs/reference/credit
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

Credit spreads by maturity, rating bucket or country. Generated from the docstrings of Finance Scenarios 0.1.0; `help(...)` in Python shows the same text.

```python
from financescenarios.factors.credit.credit_controller import Credit
```

```python
Credit(toolkit: Toolkit)
```

The Credit module simulates credit spreads: the extra interest companies pay on their bonds compared with the
government, as compensation for the risk that they fail to pay. A spread widens when markets worry about defaults (it
roughly tripled in 2008) and tends to fall back toward a normal level once the worry fades. Each `credit[i]` entry
becomes a simulated variable, linked to the other factors through the correlation matrix; `credit` is empty by
default.

By default each spread follows a mean-reverting (Ornstein-Uhlenbeck) process on its logarithm, so a simulated
spread can widen sharply but never turns negative. `volatility_model: garch` lets the size of the swings vary over
time ([Bollerslev, 1986](https://doi.org/10.1016/0304-4076(86)90063-1)), and `condition_on_business_cycle` adds a
pull from the leading indicator, so spreads tend to widen as the economy slows.

The data come through the Finance Toolkit, chosen with `dimension`:

- `maturity` or `rating`: ICE BofA spreads of US corporate bonds by maturity or rating, from FRED (API key
  needed), which keeps only three years of them, so the shipped factor sets leave credit off.
- `moodys`: Moody's Aaa and Baa yields over the 10-year Treasury, monthly from 1953 (FRED key).
- `corporate`: corporate bond spreads over government bonds, monthly, no key: Germany from 1957
  ([Bundesbank](https://www.bundesbank.de/en/statistics/money-and-capital-markets)) or Australia's A and BBB by
  maturity from 2005 ([RBA table F3](https://www.rba.gov.au/statistics/tables/)).
- `borrowing_cost`: the ECB's cost of new bank loans to euro area companies, monthly from 2003
  ([ECB MIR](https://data.ecb.europa.eu/data/datasets/MIR)), no key; a rate level rather than a spread.

Set `toolkit.start_date` back for the longer histories. For ratings that move and default see `CreditMigration`,
for a whole spread curve `CreditTermStructure`.

Configuration (`credit[i]` in a factor set):

| Key | Default | Meaning |
|:----|:--------|:--------|
| `name` | `credit` | The factor's name, unique in the list. |
| `dimension` | `maturity` | `maturity`, `rating`, `moodys`, `corporate` or `borrowing_cost`. |
| `country` | `null` | `Germany` or `Australia` (`corporate`); `Euro Area` or a member (`borrowing_cost`). |
| `maturity_bucket` | `7-10 Years` | `1-3 Years` up to `15+ Years`. |
| `rating_bucket` | `BBB` | `AAA` to `CCC`; `Aaa`, `Baa` or `Baa - Aaa` (`moodys`); e.g. `BBB 10Y` (Australia). |
| `period` | `daily` | Calibration frequency; `monthly` for `corporate` and `borrowing_cost`. |
| `currency` | `USD` | `EUR` for Germany and the euro area, `AUD` for Australia. |
| `volatility_model` | `constant` | `constant` or `garch`. |
| `condition_on_business_cycle` | `false` | Requires `leading_indicator.enabled: true`. |
| `beliefs` | none | Override the fitted speed, level or volatility (constant volatility only). |

A belief about the normal level of a log-fitted spread is a log too: a 2% target is `log(0.02)`, about `-3.9`.

Fitted on 2026-10-07 on data from 2000, Germany's spread reverts to 1.57% with a one-year half-life and the euro
area's borrowing cost to 2.54%.

**References:**

- Uhlenbeck, G.E., Ornstein, L.S. (1930). "On the Theory of the Brownian Motion." Physical Review, 36(5), 823-841. <https://doi.org/10.1103/PhysRev.36.823>
- Arvanitis, A., Gregory, J., Laurent, J-P. (1999). "Building Models for Credit Spreads." The Journal of Derivatives, 6(3), 27-43. <https://doi.org/10.3905/jod.1999.319117>

## calibrate

```python
calibrate(
    name: str,
    dimension: str = 'maturity',
    maturity_bucket: str = '7-10 Years',
    rating_bucket: str = 'BBB',
    period: str = 'daily',
    volatility_model: str = 'constant',
    business_cycle_covariate: pl.Series | None = None,
    business_cycle_covariate_dates: pl.Series | None = None,
    country: str | None = None,
) -> OUParams | GARCHParams | OUCovariateParams
```

Calibrate one credit spread from its history: fetch the spread, then fit how fast it returns to its normal level
(`mean_reversion_speed`), what that level is (`long_run_mean`) and how much it swings (`volatility`).

This learns how a spread has behaved, so the scenarios widen and tighten the way the real spread has. A speed of
3 a year means a widening fades by half in about three months (ln 2 / 3 years). The default fit works on the log
of the spread: `exp(long_run_mean)` is the level it is pulled toward, and `initial_value` is today's spread as a
decimal.

**Args:**

- <u>name (str):</u> the spread's name in the simulation and in `params()` and `changes()`.
- <u>dimension (str):</u> "maturity" or "rating" (ICE BofA), "moodys", "corporate" or "borrowing_cost". Defaults to "maturity".
- <u>maturity_bucket (str):</u> "1-3 Years" up to "15+ Years", for "maturity". Defaults to "7-10 Years".
- <u>rating_bucket (str):</u> "AAA" to "CCC", Moody's "Aaa", "Baa" or "Baa - Aaa", or e.g. "BBB 10Y" for "corporate". Defaults to "BBB".
- <u>period (str):</u> "daily" up to "yearly"; a coarser period averages the data. Defaults to "daily".
- <u>volatility_model (str):</u> "constant" or "garch". Defaults to "constant".
- <u>business_cycle_covariate (pl.Series &#124; None):</u> leading indicator history to condition on. Defaults to None.
- <u>business_cycle_covariate_dates (pl.Series &#124; None):</u> its dates, needed with it. Defaults to None.
- <u>country (str &#124; None):</u> "Germany" or "Australia" ("corporate"), "Euro Area" or a member ("borrowing_cost"). Defaults to None.

**Returns:**

<u>OUParams &#124; GARCHParams &#124; OUCovariateParams:</u> the fitted process; GARCHParams with "garch", OUCovariateParams with a covariate.

**Raises:**

- <u>ValueError:</u> if an option, bucket or country is not recognized, "garch" is combined with a covariate, or no data come back.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.credit.credit_controller import Credit

toolkit = Toolkit(["SPY"], api_key="FINANCIAL_MODELING_PREP_KEY", fred_api_key="FRED_KEY")
credit = Credit(toolkit)

credit.calibrate("ig_7_10y", maturity_bucket="7-10 Years", period="monthly")
credit.calibrate("high_yield_bb", dimension="rating", rating_bucket="BB", period="monthly")
```

Which returns (calibrated on 2026-10-04):

| name | mean_reversion_speed | long_run_mean | volatility | initial_value |
|:-----|---------------------:|--------------:|-----------:|--------------:|
| ig_7_10y | 2.9710 | -4.5984 | 0.2297 | 0.0105 |
| high_yield_bb | 6.7129 | -3.9995 | 0.3835 | 0.0204 |

The investment-grade spread starts at 1.05% and is pulled toward exp(-4.5984) = 1.01%, the BB spread toward 1.83%.

## names

```python
credit.names  # property -> list[str]
```

The names of every credit bucket calibrated so far, in calibration order.

## params

```python
params(name: str) -> OUParams | GARCHParams | OUCovariateParams
```

The calibrated process parameters of one credit spread.

**Args:**

- <u>name (str):</u> the spread's name, as passed to `calibrate()`.

**Raises:**

- <u>RuntimeError:</u> if `calibrate(name, ...)` has not been called yet.

## step_function

```python
credit.step_function  # property
```

The function that moves a constant-volatility spread one time step, on the scale it was fitted on (log, or plain
for a spread that touched zero). A GARCH or business-cycle-conditioned spread uses its own step instead.

## changes

```python
changes(name: str) -> pl.DataFrame
```

Dated period-over-period changes of one spread, from the data `calibrate()` already fetched, used to estimate its
correlation with the other factors without fetching the data again.

**Args:**

- <u>name (str):</u> the spread's name, as passed to `calibrate()`.

**Returns:**

<u>pl.DataFrame:</u> two columns, `date` and `value`.

**Raises:**

- <u>RuntimeError:</u> if `calibrate(name, ...)` has not been called yet.
