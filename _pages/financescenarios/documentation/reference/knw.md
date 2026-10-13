---
title: "Knw"
seo_title: "Knw Reference – Finance Scenarios"
excerpt: "The KNW model: interest rate and inflation fitted jointly."
description: "The KNW model: interest rate and inflation fitted jointly."
author_profile: false
permalink: /projects/financescenarios/docs/reference/knw
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

The KNW model: interest rate and inflation fitted jointly. Generated from the docstrings of Finance Scenarios 0.1.0; `help(...)` in Python shows the same text.

```python
from financescenarios.models.knw.knw_controller import Knw
```

```python
Knw(toolkit: Toolkit)
```

The Knw module simulates the interest rate and inflation as one coupled pair, in which each one's next value
depends on the current level of both. It is the constant-volatility core of the scenario model De Nederlandsche
Bank (DNB), the Dutch central bank, uses for the scenario sets Dutch pension funds and insurers are regulated
against.

Elsewhere in this project the two are linked only through correlated shocks, or one drives the other in a single
direction (Wilkie's cascade, `condition_on_interest_rate`). With `method: knw` they talk to each other both ways:
high inflation today feeds into next period's interest rate, and today's rate feeds into next period's
inflation. Use it for DNB-style two-way coupling without the extra machinery of stochastic volatility. One
instance holds any number of pairs, one `calibrate_pair()` call each.

DNB's CP2022 model extends the term-structure model of
[Koijen, Nijman & Werker (2010)](https://doi.org/10.1093/rfs/hhp058) and is specified in full in the
[CP2022 Technical Appendix (2022)](
https://www.rijksoverheid.nl/documenten/rapporten/2022/11/29/bijlage-2-technische-appendix). This class keeps its
rate and inflation recursion (eq. 52) at constant volatility, which leaves a bivariate VAR(1): each variable is
regressed on the previous value of both ([Lutkepohl, 2005](https://doi.org/10.1007/978-3-540-27752-1)).

```text
r(t)  = c_r  + phi_rr*r(t-1)   + phi_r_pi*pi(t-1) + sigma_r*z_r(t)
pi(t) = c_pi + phi_pi_r*r(t-1) + phi_pipi*pi(t-1) + sigma_pi*z_pi(t)
```

`KnwSv` adds DNB's stochastic volatility back, and `KnwSvQ` builds a risk-neutral version on top of that.

The data come from the Finance Toolkit without an API key: the rate from a Treasury-yield ticker or an OECD
country's short or long rate, inflation from OECD consumer price index growth. OECD data are not daily or
weekly, so a pair runs monthly, quarterly or yearly.

Configuration (both entries of a pair in a factor set):

| Key | Default | Meaning |
|:----|:--------|:--------|
| `interest_rates[i].method` | `hull_white` | Set to `knw` to make this entry the pair's rate leg. |
| `interest_rates[i].inflation_name` | `inflation` | The `name` of the paired `inflation[j]` entry. |
| `interest_rates[i].source` | `ticker` | `ticker` (set `ticker`, default `^IRX`) or `oecd` (set `country`, `term`). |
| `interest_rates[i].period` | `daily` | Shared by both legs and equal to `engine.frequency`. |
| `inflation[j].method` | `ou` | Set to `knw` to make this entry the pair's inflation leg. |
| `inflation[j].interest_rate_name` | `interest_rate` | The `name` of the paired `interest_rates[i]` entry. |
| `inflation[j].country` | `United States` | The country whose OECD consumer price index is used. |

Both entries set `method: knw` and name each other, and both use one `period` equal to `engine.frequency`. The
config is rejected otherwise: the fitted coefficients hold per period, so another frequency would compound them
too fast or too slow. Belief overrides, `volatility_model: garch`, `condition_on_business_cycle` and
`condition_on_interest_rate` are not supported on a knw pair.

**References:**

- Koijen, R.S.J., Nijman, T.E., Werker, B.J.M. (2010). "When Can Life Cycle Investors Benefit from Time-Varying Bond Risk Premia?" The Review of Financial Studies, 23(2), 741-780. <https://doi.org/10.1093/rfs/hhp058>
- Commissie Parameters (2022). "Technical Appendix: Specification of the CP2022 Model." <https://www.rijksoverheid.nl/documenten/rapporten/2022/11/29/bijlage-2-technische-appendix>
- Lutkepohl, H. (2005). "New Introduction to Multiple Time Series Analysis." Springer. <https://doi.org/10.1007/978-3-540-27752-1>

## calibrate_pair

```python
calibrate_pair(
    interest_rate_name: str,
    inflation_name: str,
    period: str,
    interest_rate_source: str = 'oecd',
    interest_rate_ticker: str = '^IRX',
    interest_rate_country: str = 'United States',
    interest_rate_term: str = 'short',
    inflation_country: str = 'United States',
) -> tuple[KnwParams, KnwParams]
```

Calibrate one interest rate and inflation pair: fetch both histories and fit how each one pulls on the other.

For each leg you get how much of its own last value carries over (`own_persistence`), how much of the other
leg's last value spills into it (`cross_coupling`), a constant (`intercept`) and the size of its random
surprise per period (`volatility`). An `own_persistence` of 0.9 a quarter means half of a deviation is left
after ln(0.5) / ln(0.9) = 6.6 quarters, ignoring cross effects. Rates and inflation are decimals (0.04 = 4%).

Each leg is one least squares regression on the previous rate and inflation, the bivariate VAR(1) of
[Lutkepohl (2005)](https://doi.org/10.1007/978-3-540-27752-1). Only dates both series cover are used, and the
fitted system must settle down over time (be stationary).

**Args:**

- <u>interest_rate_name (str):</u> the rate leg's name, its key in `params()` and the simulation.
- <u>inflation_name (str):</u> the inflation leg's name.
- <u>period (str):</u> the shared sampling frequency, also the simulation's: "monthly", "quarterly" or "yearly".
- <u>interest_rate_source (str):</u> "oecd" (OECD rate) or "ticker" (Yahoo Finance Treasury yield). Defaults to "oecd".
- <u>interest_rate_ticker (str):</u> the Treasury-yield ticker when the source is "ticker". Defaults to "^IRX".
- <u>interest_rate_country (str):</u> the country when the source is "oecd". Defaults to "United States".
- <u>interest_rate_term (str):</u> "short" or "long" OECD rate when the source is "oecd". Defaults to "short".
- <u>inflation_country (str):</u> the country whose OECD consumer price index is used. Defaults to "United States".

**Returns:**

<u>tuple[KnwParams, KnwParams]:</u> (interest_rate_params, inflation_params), with the fields above plus `initial_value`, the last observation.

**Raises:**

- <u>ValueError:</u> if fewer than 5 dates overlap, or the fitted coupling is not stationary.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.models.knw.knw_controller import Knw

toolkit = Toolkit(["^IRX"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="1990-01-01")
knw = Knw(toolkit)

knw.calibrate_pair("interest_rate", "inflation", period="quarterly")
```

Which returns (calibrated on 2026-10-05):

| leg | intercept | own_persistence | cross_coupling | volatility |
|:----|----------:|----------------:|---------------:|-----------:|
| interest_rate | -0.0009 | 0.9397 | 0.0918 | 0.0044 |
| inflation | 0.0036 | 0.8910 | -0.0246 | 0.0073 |

One percentage point more inflation adds 0.092 points to next quarter's rate, and the pair settles at a 2.60%
rate and 2.74% inflation in the long run.

## names

```python
knw.names  # property -> list[str]
```

The names of every knw leg calibrated so far (both legs of every pair), in calibration order.

## params

```python
params(name: str) -> KnwParams
```

The calibrated parameters of one knw leg.

**Args:**

- <u>name (str):</u> the leg's name, as passed to calibrate_pair().

**Raises:**

- <u>RuntimeError:</u> if calibrate_pair(...) naming this leg hasn't been called yet.

## series

```python
series(name: str) -> pl.Series
```

The historical series one knw leg was calibrated on.

**Args:**

- <u>name (str):</u> the leg's name, as passed to calibrate_pair().

**Raises:**

- <u>RuntimeError:</u> if calibrate_pair(...) naming this leg hasn't been called yet.

## dates

```python
dates(name: str) -> pl.Series
```

The dates paired with series(name), same length and order.

**Args:**

- <u>name (str):</u> the leg's name, as passed to calibrate_pair().

**Raises:**

- <u>RuntimeError:</u> if calibrate_pair(...) naming this leg hasn't been called yet.

## changes

```python
changes(name: str) -> pl.DataFrame
```

The dated period-over-period changes of one knw leg, used to estimate its correlation with other factors
without fetching the data again.

**Args:**

- <u>name (str):</u> the leg's name, as passed to calibrate_pair().

**Returns:**

<u>pl.DataFrame:</u> two columns, `date` and `value`.

**Raises:**

- <u>RuntimeError:</u> if calibrate_pair(...) naming this leg hasn't been called yet.

## step_function

```python
Knw.step_function()
```

The function that moves any knw leg forward by one period, given its parameters and the other leg's
current value.
