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

Credit spreads by maturity, rating bucket or country.

```python
from financescenarios.factors.credit.credit_controller import Credit
```

The Credit module simulates credit spreads: the extra yield corporate bonds pay over government bonds as
compensation for default and liquidity risk. Each `credit[i]` entry is one spread series, correlated with the other
factors (typically widening when equities fall); `credit` is empty by default.

The model assumes a spread has a normal level it returns to: it widens sharply in a sell-off such as 2008 and
tightens again once the stress fades, rather than wandering off: an Ornstein-Uhlenbeck process
([Uhlenbeck and Ornstein, 1930](https://doi.org/10.1103/PhysRev.36.823)). Fitting the logarithm of the spread, the
default, is a judgement: it keeps every simulated spread positive and makes the swings proportional to the level,
so a wide spread moves more in basis points than a tight one and the distribution of future spreads is skewed
toward sharp widenings, as in credit history. A series that has touched zero or below is
fitted on its level instead.

`volatility_model: garch` lets the size of the swings cluster in time, so a volatile month tends to be followed by
another ([Bollerslev, 1986](https://doi.org/10.1016/0304-4076(86)90063-1)), and `condition_on_business_cycle` adds a
pull from the leading indicator, so spreads tend to widen as the economy slows.

The data come through the Finance Toolkit, chosen with `dimension`:

- `maturity` or `rating`: ICE BofA spreads of US corporate bonds by maturity or rating, from FRED (API key
  needed), which keeps only three years of them ("Starting in April 2026, this series will only include 3 years
  of observations", [FRED](https://fred.stlouisfed.org/series/BAMLC0A4CBBB)), so the shipped factor sets leave
  credit off.
- `moodys`: Moody's Aaa and Baa yields over the 10-year Treasury, monthly from 1953 (FRED key).
- `corporate`: corporate bond spreads over government bonds, monthly, no key: Germany from 1957
  ([Bundesbank](https://www.bundesbank.de/en/statistics/money-and-capital-markets)) or Australia's A and BBB by
  maturity from 2005 ([RBA table F3](https://www.rba.gov.au/statistics/tables/)).
- `borrowing_cost`: the ECB's cost of new bank loans to euro area companies, monthly from 2003
  ([ECB MIR](https://data.ecb.europa.eu/data/datasets/MIR)), no key; a rate level rather than a spread.

Set `toolkit.start_date` back for the longer histories. For ratings that move and default see `CreditMigration`,
for a whole spread curve `CreditTermStructure`.

The `credit[i]` keys of a factor set and their defaults are listed on the reference page
[Configuration Classes](https://www.jeroenbouma.com/projects/financescenarios/docs/reference/configuration-classes).

A belief about the normal level of a log-fitted spread is a log too: a 2% target is `log(0.02)`, about `-3.9`.

Fitted on 2026-10-07 on data from 2000, Germany's spread reverts to 1.57% with a one-year half-life and the euro
area's borrowing cost to 2.54%.

**References:**

- Uhlenbeck, G.E., Ornstein, L.S. (1930). "On the Theory of the Brownian Motion." Physical Review, 36(5), 823-841. <https://doi.org/10.1103/PhysRev.36.823>

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
Credit(toolkit: Toolkit)
```

</details>

## calibrate

Calibrate one credit spread from its history: how fast it returns to its normal level
(`mean_reversion_speed`), what that level is (`long_run_mean`) and how much it swings (`volatility`).

Fitting these to the observed spread means the scenarios widen and tighten at the speed and with the size the
real market has shown. The speed sets how long a credit shock lasts: a speed of
3 a year means a widening fades by half in about three months (ln 2 / 3 years), so short-horizon stresses are
severe while long-horizon spreads cluster around the normal level. The default fit works on the log of the
spread, a judgement that keeps every spread positive: `exp(long_run_mean)` is the level it is pulled toward,
and every path starts from `initial_value`, today's spread as a decimal.

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

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

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

**Args:**

- <u>name (str):</u> the spread's name in the scenarios.
- <u>dimension (str):</u> "maturity" or "rating" (ICE BofA), "moodys", "corporate" or "borrowing_cost". Defaults to "maturity".
- <u>maturity_bucket (str):</u> "1-3 Years" up to "15+ Years", for "maturity". Defaults to "7-10 Years", a judgement: a medium-to-long investment-grade maturity.
- <u>rating_bucket (str):</u> "AAA" to "CCC", Moody's "Aaa", "Baa" or "Baa - Aaa", or e.g. "BBB 10Y" for "corporate". Defaults to "BBB".
- <u>period (str):</u> "daily" up to "yearly"; a coarser period averages the data. Defaults to "daily".
- <u>volatility_model (str):</u> "constant" or "garch". Defaults to "constant".
- <u>business_cycle_covariate (pl.Series &#124; None):</u> the leading indicator history the spread moves with, so it widens as the economy slows. Defaults to None.
- <u>business_cycle_covariate_dates (pl.Series &#124; None):</u> the dates of that history, needed with it. Defaults to None.
- <u>country (str &#124; None):</u> "Germany" or "Australia" ("corporate"), "Euro Area" or a member ("borrowing_cost"). Defaults to None.

**Returns:**

<u>OUParams &#124; GARCHParams &#124; OUCovariateParams:</u> the fitted speed, level and volatility, plus the GARCH terms or the business-cycle sensitivity when those are used.

**Raises:**

- <u>ValueError:</u> if an option, bucket or country is not recognized, "garch" is combined with a covariate, or no data come back.

</details>

## names

The names of every credit bucket calibrated so far, in calibration order.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
credit.names  # property -> list[str]
```

</details>

## params

The calibrated parameters of one credit spread: its speed of mean reversion, normal level and volatility.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
params(name: str) -> OUParams | GARCHParams | OUCovariateParams
```

**Args:**

- <u>name (str):</u> the spread's name, as passed to `calibrate`.

**Raises:**

- <u>RuntimeError:</u> if that spread has not been calibrated yet.

</details>

## step_function

The one-step move of a constant-volatility spread: the exact mean-reverting step on the log of the spread (or on
its plain level for a spread that has touched zero), so simulated spreads keep the fitted speed and stay
positive. GARCH and business-cycle-conditioned spreads move with their own step.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
credit.step_function  # property
```

</details>

## changes

The historical period-over-period changes of one spread, the input for its correlation with the other factors
(how far spreads widen when equities fall, for example).

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
changes(name: str) -> pl.DataFrame
```

**Args:**

- <u>name (str):</u> the spread's name, as passed to `calibrate`.

**Returns:**

<u>pl.DataFrame:</u> two columns, `date` and `value`.

**Raises:**

- <u>RuntimeError:</u> if that spread has not been calibrated yet.

</details>
