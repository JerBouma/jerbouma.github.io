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

Consumer price inflation, one per country or region.

```python
from financescenarios.factors.inflation.inflation_controller import Inflation
```

The Inflation module simulates consumer price inflation for one or more countries: the driver of indexed
liabilities, real returns and purchasing power.

The model assumes inflation is pulled back toward a long-run level after a shock, as it was after the 2022 surge
once central banks responded, and that the pull is steady rather than abrupt. That gives scenarios a realistic
spread: a spike decays over a few years instead of persisting forever, while the long-run level anchors 30-year
projections. Inflation can turn negative, so deflation scenarios are possible. Because inflation sits at the root
of the economy in actuarial models such as [Wilkie (1986)][wilkie-1986] and
[Ahlgrim, D'Arcy and Gorvett (2005)](https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf),
it can drive interest rates, dividends and property; `ScenarioSet.cumulative_index` turns a path into a price
index.

The default model is the Ornstein-Uhlenbeck process `dpi = a(theta - pi)dt + sigma*dW`: `a` is how fast a gap to
the long-run level `theta` closes and `sigma` the size of the random swings
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

For `ou`, `volatility_model: garch` lets calm and turbulent periods alternate, which fattens the tails
([Bollerslev, 1986](https://doi.org/10.1016/0304-4076(86)90063-1)); `condition_on_business_cycle` and
`condition_on_interest_rate` tie inflation to the leading indicator or a paired interest rate; and
`measure: risk_neutral` follows the breakeven inflation the bond market prices today (see
`calibrate_risk_neutral`).

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

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
Inflation(toolkit: Toolkit)
```

</details>

## calibrate

Calibrate one country's inflation process from its history: how fast inflation returns to its normal level
(`mean_reversion_speed`), what that level is (`long_run_mean`) and how much it swings (`volatility`).

The parameters come from the country's own Consumer Price Index history, so simulated inflation spikes and
settles the way it has in that economy: a high-inflation country such as Brazil gets a higher anchor and
wider swings than the United States. The `ou` fit regresses each period's change on its level, which measures
how strongly inflation has been pulled back after deviations
([Uhlenbeck and Ornstein, 1930](https://doi.org/10.1103/PhysRev.36.823)); `wilkie_ar1` gives a `persistence`,
the share of last period's gap to the mean carried into this one. Values are annual decimals and every path
starts from `initial_value`, the latest observed rate. The long-run level is only as good as the history
behind it, so use an early `start_date`: five years cover too few inflation cycles.

`hibbert_two_factor` assumes inflation is pulled toward an expected-inflation level that itself drifts, which
keeps regime shifts such as the 1970s or the 2010s low-inflation decade inside the scenario set.

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

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

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

**Args:**

- <u>name (str):</u> the entry's name.
- <u>country (str):</u> the country, default "United States".
- <u>period (str):</u> "monthly" (default), "quarterly" or "yearly"; only "yearly" for "gmdb".
- <u>source (str):</u> "oecd" (default) or "gmdb" (the Global Macro Database).
- <u>method (str):</u> "ou" (default), "wilkie_ar1" or "hibbert_two_factor".
- <u>volatility_model (str):</u> "constant" (default) or "garch".
- <u>business_cycle_covariate (pl.Series &#124; None):</u> the leading indicator or paired interest rate inflation moves with, default None.
- <u>business_cycle_covariate_dates (pl.Series &#124; None):</u> the dates of that series; required with it.
- <u>target_source (str):</u> the "hibbert_two_factor" target: "coarser_period" (default, the same inflation at `target_period`) or "ewma" (a smoothed average of its own history).
- <u>target_period (str):</u> "quarterly" or "yearly" (default) for "coarser_period", coarser than `period`.
- <u>target_smoothing (float):</u> the "ewma" weight on each new observation, between 0 and 1, default 0.05.

**Returns:**

<u>OUParams &#124; GARCHParams &#124; OUCovariateParams &#124; AR1Params &#124; MovingTargetOUParams:</u> the fitted parameters, including `initial_value`.

**Raises:**

- <u>ValueError:</u> if an option is unknown or two options clash, no data come back, or the history is too short or shows no pull toward a normal level.

</details>

## calibrate_risk_neutral

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

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate_risk_neutral(
    name: str,
    decay: float = 0.7308,
    country: str = 'United States',
) -> DeterministicPathParams
```

**Args:**

- <u>name (str):</u> the entry's name, also its factor name in the simulation.
- <u>decay (float):</u> the Nelson-Siegel decay, which sets where the hump sits, default 0.7308; fixed rather than fitted, as in Diebold and Li (2006).
- <u>country (str):</u> "United States" (default, 5 to 30 years), "United Kingdom" (3 to 40 years, against the Retail Prices Index), or "Germany" or "Euro Area" (German bonds paying euro area inflation).

**Returns:**

<u>DeterministicPathParams:</u> the curve's `level`, `slope`, `curvature` and `decay`, plus `initial_value`, today's rate, all annual decimals.

**Raises:**

- <u>ValueError:</u> if `country` or `decay` is not valid, or no date has every maturity quoted (for the United States, an `end_date` before February 2010).

</details>

## names

The names of every inflation entry calibrated so far, in calibration order.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
inflation.names  # property -> list[str]
```

</details>

## params

The calibrated parameters for one inflation entry.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
params(
    name: str,
) -> OUParams | GARCHParams | OUCovariateParams | AR1Params | MovingTargetOUParams | DeterministicPathParams
```

**Args:**

- <u>name (str):</u> the entry's name, as passed to `calibrate`.

**Raises:**

- <u>RuntimeError:</u> if that entry has not been calibrated yet.

</details>

## step_function

The one-period inflation update for a method: Wilkie's AR(1) for "wilkie_ar1" and the exact
Ornstein-Uhlenbeck step otherwise.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
Inflation.step_function(method: str)
```

**Args:**

- <u>method (str):</u> "ou" or "wilkie_ar1".

</details>

## series

The historical inflation rate for one entry. Factors that respond to the level of inflation, such as the
dividend yield's `condition_on_inflation`, are fitted against it.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
series(name: str) -> pl.Series
```

**Args:**

- <u>name (str):</u> the entry's name, as passed to `calibrate`.

**Raises:**

- <u>RuntimeError:</u> if that entry has not been calibrated yet.

</details>

## dates

The dates that go with `series(name)`, in the same order, so another factor can match its own data to this
inflation rate by date rather than by position.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
dates(name: str) -> pl.Series
```

**Args:**

- <u>name (str):</u> the entry's name, as passed to `calibrate`.

**Raises:**

- <u>RuntimeError:</u> if that entry has not been calibrated yet.

</details>

## changes

Dated period-over-period changes in one entry's inflation rate: the history its correlations with the other
factors are estimated from.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
changes(name: str) -> pl.DataFrame
```

**Args:**

- <u>name (str):</u> the entry's name, as passed to `calibrate`.

**Returns:**

<u>pl.DataFrame:</u> two columns, `date` and `value`.

**Raises:**

- <u>RuntimeError:</u> if that entry has not been calibrated yet.

</details>

## How It Is Calculated

The model functions behind this page, each with the formula it implements.

### step_ar1

Move inflation one period forward under Wilkie's (1986) model, the classic UK actuarial inflation model.

Wilkie models the force of inflation (the log change in the price index) as an AR(1): each period keeps a fixed
share of last period's gap to the long-run mean and adds a normal shock. A persistence near one means shocks fade
slowly, so scenarios can show long stretches of high or low inflation; the stationary spread of inflation is
QSD / sqrt(1 - QA^2), wider than one period's shock.

The formula is as follows:

$$
I_{t} = \text{QMU} + \text{QA} \cdot (I_{t-1} - \text{QMU}) + \text{QSD} \cdot z_{t}
$$

Where I_t = ln(Q_t / Q_t-1) is the force of inflation over one period (Q the price index), QMU is `long_run_mean`,
QA is `persistence` and QSD is `volatility`. Wilkie fitted it as a recursion between observation dates rather
than as a continuous-time process, so the simulation frequency must equal the entry's `period`.

**References:**

- Wilkie, A.D. (1986). "A Stochastic Investment Model for Actuarial Use." Transactions of the Faculty of Actuaries, 39, 341-403. Section 3.2. <https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
step_ar1(
    current_value: np.ndarray | float,
    shock: np.ndarray | float,
    time_step: float,
    params: AR1Params,
) -> np.ndarray
```

**Args:**

- <u>current_value (np.ndarray &#124; float):</u> this period's inflation rate.
- <u>shock (np.ndarray &#124; float):</u> a standard normal draw.
- <u>time_step (float):</u> not used; the period is fixed by the calibration.
- <u>params (AR1Params):</u> calibrated long-run mean, persistence, and volatility.

**Returns:**

<u>np.ndarray:</u> inflation one period later.

</details>

### step_ou

Move inflation one step forward under the Ornstein-Uhlenbeck process d(pi_t) = a * (theta - pi_t) * dt + sigma *
dW_t, the default inflation model.

Inflation is pulled toward its long-run level theta at speed a: a gap halves in ln(2) / a years, and the
long-run spread of inflation around theta is sigma / sqrt(2a). This matches how inflation behaves under a
central bank with a target, where shocks fade over a few years, and is the inflation generator of Ahlgrim and
D'Arcy (2012). The step uses the exact transition (as for the Vasicek short rate), so the result is the same
whether you simulate monthly or yearly.

The formula is as follows:

$$
\pi(t + \text{dt}) = \theta + (\pi(t) - \theta) \cdot \exp(- a \cdot \text{dt}) + \sigma \cdot \sqrt{(1 - \exp(- 2 \cdot a \cdot \text{dt})) / (2 \cdot a)} \cdot z
$$

Where a is `mean_reversion_speed`, theta `long_run_mean`, sigma `volatility` and z a standard normal draw.
Nothing stops inflation from going negative, so deflation scenarios occur with the probability the history
implies.

**References:**

- Ahlgrim, K.C., D'Arcy, S.P. (2012). "A User's Guide to the Inflation Generator." Casualty Actuarial Society, Canadian Institute of Actuaries, Society of Actuaries. <https://www.soa.org/globalassets/assets/files/research/projects/research-2012-02-effect-deflation-user-guide.pdf>
- Wilkie, A.D. (1986). "A Stochastic Investment Model for Actuarial Use." Transactions of the Faculty of Actuaries, 39, 341-403. <https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf>
- Vasicek, O. (1977). "An Equilibrium Characterization of the Term Structure." Journal of Financial Economics, 5(2), 177-188. Source of the exact transition used here. <https://doi.org/10.1016/0304-405X(77>)90016-2

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
step_ou(
    current_value: np.ndarray | float,
    shock: np.ndarray | float,
    time_step: float,
    params: OUParams,
) -> np.ndarray
```

**Args:**

- <u>current_value (np.ndarray &#124; float):</u> today's inflation rate.
- <u>shock (np.ndarray &#124; float):</u> a standard normal draw.
- <u>time_step (float):</u> the step length, in years.
- <u>params (OUParams):</u> calibrated mean-reversion speed, long-run mean, and volatility.

**Returns:**

<u>np.ndarray:</u> inflation one step later.

</details>
