---
title: "Inflation"
seo_title: "Inflation Reference – Finance Scenarios"
excerpt: "Consumer price inflation, one per country or region."
description: "Consumer price inflation, one per country or region."
author_profile: false
permalink: /projects/financescenarios/docs/reference/inflation
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

Consumer price inflation, one per country or region. Generated from the docstrings of Finance Scenarios 0.1.0; `help(...)` in Python shows the same text.

```python
from financescenarios.factors.inflation.inflation_controller import Inflation
```

```python
Inflation(toolkit: Toolkit)
```

The Inflation module simulates the inflation rate: how fast consumer prices rise each year, for one or more
countries. Inflation drifts back toward a normal level after a shock (the 2022 surge had largely faded by 2024) and
can briefly turn negative (deflation).

Add one entry per country, such as the United States or Brazil; at least one is required. Each becomes a variable
in the simulated scenarios, correlated with the other factors, and shows how purchasing power might evolve
(`ScenarioSet.cumulative_index` turns a path into a price index). Inflation is simulated first, so it can drive
other factors, as in [Wilkie (1986)][wilkie-1986] and
[Ahlgrim, D'Arcy and Gorvett (2005)](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf).

The default model is the same mean-reverting process as the short rate, `dpi = a(theta - pi)dt + sigma*dW`: `a` is
how fast a gap to the normal level `theta` closes, and `sigma` the size of the random swings `dW`
([Uhlenbeck and Ornstein, 1930](https://doi.org/10.1103/PhysRev.36.823)). `method` picks the process:

| Method | What it is |
|:-------|:-----------|
| `ou` (default) | The model above; inflation can go negative. |
| `wilkie_ar1` | Each period keeps a fixed share of last period's gap to the mean ([Wilkie, 1986][wilkie-1986]). |
| `hibbert_two_factor` | Pulled toward a moving "expected inflation" level ([Hibbert et al., 2001][hibbert-2001]). |
| `knw` | Linked both ways with a paired interest rate; fitted by `Knw`. |
| `knw_sv` | `knw` with a shared, randomly changing volatility; fitted by `KnwSv`. |

[wilkie-1986]: https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf
[hibbert-2001]: https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf

For `ou`, `volatility_model: garch` lets the size of the swings change over time
([Bollerslev, 1986](https://doi.org/10.1016/0304-4076(86)90063-1)); `condition_on_business_cycle` and
`condition_on_interest_rate` let inflation move with the leading indicator or a paired interest rate; and
`measure: risk_neutral` follows the inflation the bond market prices today (see `calibrate_risk_neutral`).

The data are the Finance Toolkit's Consumer Price Index, year over year, with no API key needed: 0.034 means
prices are 3.4% higher than a year ago. `source: oecd` covers the roughly 38 OECD members; `source: gmdb`
(the Global Macro Database) adds countries such as Brazil and India, yearly only. Only headline inflation is
modeled.

Configuration (`inflation[i]` in a factor set):

| Key | Default | Meaning |
|:----|:--------|:--------|
| `name` | `inflation` | The factor's name; unique across all factors. |
| `country` | `United States` | The country whose prices are used. |
| `source` | `oecd` | `oecd` or `gmdb`. |
| `method` | `ou` | One of the methods above. |
| `period` | `monthly` | `monthly`, `quarterly` or `yearly` (`yearly` only for `gmdb`). |
| `measure` | `real_world` | `real_world`, or `risk_neutral` with `ou` or `knw_sv`. |
| `volatility_model` | `constant` | `constant` or `garch`. |
| `interest_rate_name` | `interest_rate` | The paired rate for `condition_on_interest_rate`, `knw` and `knw_sv`. |
| `beliefs` | `null` | Your own `mean_reversion_speed`, `long_run_mean` or `volatility`. |

Other keys are in the configuration documentation. Beliefs are annual decimals (`long_run_mean: 0.09` is 9% a
year) and apply only to the constant-volatility `ou` fit, not with `risk_neutral`; a regime file addresses one
entry as `"inflation.<name>"`.

## calibrate

```python
calibrate(
    name: str,
    country: str = 'United States',
    period: str = 'monthly',
    source: str = 'oecd',
    method: str = 'ou',
    volatility_model: str = 'constant',
    business_cycle_covariate: pl.Series | None = None,
    business_cycle_covariate_dates: pl.Series | None = None,
    target_source: str = 'coarser_period',
    target_period: str = 'yearly',
    target_smoothing: float = 0.05,
) -> OUParams | GARCHParams | OUCovariateParams | AR1Params | MovingTargetOUParams
```

Calibrate one country's inflation process from its history: how fast inflation returns to its normal level
(`mean_reversion_speed`), what that level is (`long_run_mean`) and how much it swings (`volatility`).

This learns how inflation has behaved, so simulated scenarios spike and settle the way the real rate has.
Values are annual decimals and every path starts from `initial_value`, the latest observed rate. The `ou` fit
regresses each period's change on its level
([Uhlenbeck and Ornstein, 1930](https://doi.org/10.1103/PhysRev.36.823)); `wilkie_ar1` gives a `persistence`,
the share of last period's gap carried into this one. Use an early Toolkit `start_date`; five default years
are too few.

**Args:**

- <u>name (str):</u> the entry's name.
- <u>country (str):</u> the country, default "United States".
- <u>period (str):</u> "monthly" (default), "quarterly" or "yearly"; only "yearly" for "gmdb".
- <u>source (str):</u> "oecd" (default) or "gmdb" (the Global Macro Database).
- <u>method (str):</u> "ou" (default), "wilkie_ar1" or "hibbert_two_factor".
- <u>volatility_model (str):</u> "constant" (default) or "garch".
- <u>business_cycle_covariate (pl.Series &#124; None):</u> a level series to move with (the leading indicator or a paired rate), default None.
- <u>business_cycle_covariate_dates (pl.Series &#124; None):</u> its dates; required with it.
- <u>target_source (str):</u> the "hibbert_two_factor" target: "coarser_period" (default, the same inflation at `target_period`) or "ewma" (a smoothed average of its own history).
- <u>target_period (str):</u> "quarterly" or "yearly" (default) for "coarser_period", coarser than `period`.
- <u>target_smoothing (float):</u> the "ewma" weight on each new observation, between 0 and 1, default 0.05.

**Returns:**

<u>OUParams &#124; GARCHParams &#124; OUCovariateParams &#124; AR1Params &#124; MovingTargetOUParams:</u> the fitted parameters, including `initial_value`.

**Raises:**

- <u>ValueError:</u> if an option is unknown or two options clash, no data come back, or the history is too short or shows no pull toward a normal level.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.inflation.inflation_controller import Inflation

toolkit = Toolkit(["SPY"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2000-01-01")
inflation = Inflation(toolkit)

inflation.calibrate("united_states_inflation", country="United States")
inflation.calibrate("brazil_inflation", country="Brazil", source="gmdb", period="yearly")
```

Which returns (calibrated on 2026-10-05):

| name | mean_reversion_speed | long_run_mean | volatility | initial_value |
|:-----|---------------------:|--------------:|-----------:|--------------:|
| united_states_inflation | 0.4150 | 0.0266 | 0.0158 | 0.0340 |
| brazil_inflation | 0.9484 | 0.0592 | 0.0371 | 0.0313 |

US inflation starts at 3.40% and is pulled toward 2.66%, halving a gap in about 1.7 years.

## calibrate_risk_neutral

```python
calibrate_risk_neutral(
    name: str,
    decay: float = 0.7308,
    country: str = 'United States',
) -> DeterministicPathParams
```

Calibrate one risk-neutral inflation path: a curve fitted to the inflation the bond market prices today, which
every simulated path then follows.

The gap between a nominal government bond yield and an inflation-protected one of the same maturity, the
"breakeven", is the inflation the bond market prices in. Use it to value inflation-linked cash flows in line
with market prices. It is a curve, not one number, because expected inflation differs by horizon. This is what
`measure: risk_neutral` selects with `method: ou`.

The curve is a [Nelson-Siegel (1987)](https://doi.org/10.1086/296409) fit (a long-run level, a slope and a hump)
on the latest date every maturity is quoted, with no randomness. The data come from the US Treasury, the Bank of
England and the Bundesbank, with no API key needed. The shortest breakeven is three or five years out, so the
first years of the path are extrapolated.

**Args:**

- <u>name (str):</u> the entry's name, also its factor name in the simulation.
- <u>decay (float):</u> the Nelson-Siegel decay, which sets where the hump sits, default 0.7308; fixed rather than fitted, as in Diebold and Li (2006).
- <u>country (str):</u> "United States" (default, 5 to 30 years), "United Kingdom" (3 to 40 years, against the Retail Prices Index), or "Germany" or "Euro Area" (German bonds paying euro area inflation).

**Returns:**

<u>DeterministicPathParams:</u> the curve's `level`, `slope`, `curvature` and `decay`, plus `initial_value`, today's rate, all annual decimals.

**Raises:**

- <u>ValueError:</u> if `country` or `decay` is not valid, or no date has every maturity quoted (for the United States, an `end_date` before February 2010).

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.inflation.inflation_controller import Inflation

toolkit = Toolkit(["SPY"], api_key="FINANCIAL_MODELING_PREP_KEY", fred_api_key="FRED_KEY")
inflation = Inflation(toolkit)

inflation.calibrate_risk_neutral("us_breakeven")
```

Which returns (calibrated on 2026-10-04):

| name | level | slope | curvature | decay | initial_value |
|:-----|------:|------:|----------:|------:|--------------:|
| us_breakeven | 0.0238 | -0.0057 | 0.0053 | 0.7308 | 0.0181 |

The curve starts at 1.81% today (extrapolated), rises to about 2.42% at five years and settles at 2.38% for the
long run.

**References:**

- Diebold, F.X., Li, C. (2006). "Forecasting the Term Structure of Government Bond Yields." Journal of Econometrics, 130(2), 337-364. <https://doi.org/10.1016/j.jeconom.2005.03.005>

## names

```python
inflation.names  # property -> list[str]
```

The names of every inflation entry calibrated so far, in calibration order.

## params

```python
params(
    name: str,
) -> OUParams | GARCHParams | OUCovariateParams | AR1Params | MovingTargetOUParams | DeterministicPathParams
```

The calibrated parameters for one inflation entry.

**Args:**

- <u>name (str):</u> the entry's name, as passed to `calibrate`.

**Raises:**

- <u>RuntimeError:</u> if that entry has not been calibrated yet.

## step_function

```python
Inflation.step_function(method: str)
```

The function that moves inflation one step for a given method: Wilkie's AR(1) step for "wilkie_ar1" and the exact
mean-reverting step otherwise. GARCH, conditioned, moving-target and risk-neutral entries use their own steps.

**Args:**

- <u>method (str):</u> "ou" or "wilkie_ar1".

## series

```python
series(name: str) -> pl.Series
```

The historical inflation rate for one entry, from the data `calibrate` already fetched. Other factors use it where
they need the level itself rather than its changes, such as the dividend yield's `condition_on_inflation`.

**Args:**

- <u>name (str):</u> the entry's name, as passed to `calibrate`.

**Raises:**

- <u>RuntimeError:</u> if that entry has not been calibrated yet.

## changes

```python
changes(name: str) -> pl.DataFrame
```

Dated period-over-period changes in one entry's inflation rate, from the data `calibrate` already fetched; used to
estimate the correlations between factors.

**Args:**

- <u>name (str):</u> the entry's name, as passed to `calibrate`.

**Returns:**

<u>pl.DataFrame:</u> two columns, `date` and `value`.

**Raises:**

- <u>RuntimeError:</u> if that entry has not been calibrated yet.
