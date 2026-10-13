---
title: "InterestRates"
seo_title: "InterestRates Reference – Finance Scenarios"
excerpt: "Short and long interest rates, one per country or region."
description: "Short and long interest rates, one per country or region."
author_profile: false
permalink: /projects/financescenarios/docs/reference/interest-rates
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

Short and long interest rates, one per country or region.

```python
from financescenarios.factors.interest_rates.interest_rates_controller import InterestRates
```

The Interest Rates module simulates the short rate: the yield on very short lending, such as a 13-week Treasury
bill, which sets the risk-free return and the discount rate in every scenario. Each entry is one country or
region, correlated with the other factors, which read it where they need a risk-free rate. For a whole yield
curve, add the `yield_curve` or `hjm` factor.

The core assumption is mean reversion: central banks raise rates when the economy runs hot and cut them when it
slows, so a short rate is pulled back toward a long-run level. That keeps 30-year projections realistic while
still allowing rate cycles. The default model is the Ornstein-Uhlenbeck process of [Vasicek (1977)](https://doi.org/10.1016/0304-405x(77)90016-2),
`dr = a(theta - r)dt + sigma*dW`: `theta` is the long-run level, `a` the speed of the pull (a gap halves in
ln 2 / `a` years) and `sigma` the size of the random swings `dW`. Shocks are normal, so the rate can go
negative, as euro and yen rates did after 2014, and swing sizes do not depend on the level. `method` picks the
process:

| Method | What it is |
|:-------|:-----------|
| `hull_white` (default) | The model above; the rate can go negative ([Hull and White, 1990][hull-white-1990]). |
| `cir` | Swings shrink with the level, so rates stay near zero or above ([Cox, Ingersoll, Ross, 1985][cir-1985]). |
| `wilkie_consols` | A long yield = expected inflation + a real yield ([Wilkie, 1986][wilkie-1986]). |
| `hibbert_two_factor` | Pulled toward a long-term rate that itself moves ([Hibbert et al., 2001][hibbert-2001]). |
| `knw` | Linked both ways with a paired inflation entry; fitted by `Knw`. |
| `knw_sv` | `knw` with a shared, randomly changing volatility; fitted by `KnwSv`. |

[hull-white-1990]: https://doi.org/10.1093/rfs/3.4.573
[cir-1985]: https://doi.org/10.2307/1911242
[wilkie-1986]: https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf
[hibbert-2001]: https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf

Inflation feeds yields in `wilkie_consols`, `knw` and `knw_sv`: a yield carries expected inflation plus a real
return.

Real rate volatility comes in bursts (2008, 2022), so `volatility_model: garch` lets the size of the swings change
over time ([Bollerslev, 1986](https://doi.org/10.1016/0304-4076(86)90063-1)), with `hull_white` only, giving
calm and turbulent stretches and fatter tails. `condition_on_business_cycle` tilts the rate with the leading
indicator. `measure: risk_neutral` follows today's market instead of history, for valuing cash flows at market
prices: a flat path at today's rate or, with `risk_neutral_forward_curve`, a random rate whose average path
follows today's forward curve.

The data come through the Finance Toolkit, with no API key needed: a Yahoo Finance Treasury yield such as `^IRX`
(`source: ticker`, US only in practice), an OECD member's short- or long-term rate (`oecd`, monthly or slower) or
the Global Macro Database, which adds countries such as Brazil and India (`gmdb`, yearly only).

Configuration (`interest_rates[i]` in a factor set):

| Key | Default | Meaning |
|:----|:--------|:--------|
| `name` | `interest_rate` | The factor's name; unique across all factors. |
| `source` | `ticker` | `ticker`, `oecd` or `gmdb`. |
| `method` | `hull_white` | One of the methods above. |
| `ticker` | `^IRX` | With `source: ticker`. |
| `country`, `term` | `United States`, `short` | With `oecd` or `gmdb`; `term` is `short` or `long`. |
| `period` | `daily` | Data frequency, `daily` to `yearly`. |
| `volatility_model` | `constant` | `constant` or `garch`. |
| `measure` | `real_world` | `real_world` or `risk_neutral`. |
| `beliefs` | `null` | Your own `mean_reversion_speed`, `long_run_mean` or `volatility`. |

Other keys are in the configuration documentation. Beliefs apply to `hull_white` and `cir` with constant
volatility, not with `risk_neutral`; a regime file addresses one entry as `"interest_rates.<name>"`.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
InterestRates(toolkit: Toolkit)
```

</details>

## calibrate

Calibrate one country or region's short rate from its history: how fast it returns to its normal level
(`mean_reversion_speed`), what that level is (`long_run_mean`) and how much it swings (`volatility`).

These are the real-world parameters: how the rate has actually behaved, so simulated rate cycles are as deep
and as long as history suggests. The speed sets how persistent a shock is: 0.73 a year halves a gap to the
long-run level in about eleven months (ln 2 / 0.73 years), while a slow speed lets low or high rates linger for
years. The long-run level is where rates settle over a long horizon, the number that matters most for
long-dated liabilities, so check it against your own view and override it with `beliefs` where needed. The
default fit regresses each period's change in the rate on its level
([Vasicek, 1977](https://doi.org/10.1016/0304-405x(77)90016-2)); the class lists the other methods. The fit
reflects the window you give it: a window dominated by zero rates gives a low long-run level.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.interest_rates.interest_rates_controller import InterestRates

toolkit = Toolkit(["SPY", "^IRX", "^TNX"], api_key="FINANCIAL_MODELING_PREP_KEY")
rates = InterestRates(toolkit)

rates.calibrate("united_states", ticker="^IRX", period="monthly")
rates.calibrate("germany", source="oecd", country="Germany", period="monthly")
```

Which returns (calibrated on 2026-10-04):

| name | mean_reversion_speed | long_run_mean | volatility | initial_value |
|:-----|---------------------:|--------------:|-----------:|--------------:|
| united_states | 0.7344 | 0.0488 | 0.0071 | 0.0399 |
| germany | 0.4667 | 0.0359 | 0.0057 | 0.0251 |

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate(
    name: str,
    source: str = 'ticker',
    method: str = 'hull_white',
    ticker: str = '^IRX',
    country: str = 'United States',
    term: str = 'short',
    period: str = 'daily',
    volatility_model: str = 'constant',
    business_cycle_covariate: pl.Series | None = None,
    business_cycle_covariate_dates: pl.Series | None = None,
    inflation: pl.Series | None = None,
    inflation_weight: float = 1.0,
    inflation_decay: float = 0.05,
    target_source: str = 'long_term_rate',
    target_term: str = 'long',
    target_ticker: str = '^TNX',
    target_smoothing: float = 0.05,
) -> OUParams | GARCHParams | OUCovariateParams | WilkieConsolsParams | MovingTargetOUParams
```

**Args:**

- <u>name (str):</u> the entry's name (e.g. "united_states").
- <u>source (str):</u> "ticker" (default), "oecd" or "gmdb".
- <u>method (str):</u> "hull_white" (default), "cir", "wilkie_consols" or "hibbert_two_factor".
- <u>ticker (str):</u> the yield ticker for "ticker", default "^IRX"; must be in the Toolkit.
- <u>country (str):</u> the country for "oecd" or "gmdb", default "United States".
- <u>term (str):</u> "short" (default) or "long", for "oecd" or "gmdb".
- <u>period (str):</u> data frequency, default "daily"; "monthly" or slower for "oecd", "yearly" for "gmdb".
- <u>volatility_model (str):</u> "constant" (default) or "garch" ("hull_white" only).
- <u>business_cycle_covariate (pl.Series &#124; None):</u> the leading indicator's level to move with, default None.
- <u>business_cycle_covariate_dates (pl.Series &#124; None):</u> its dates; required with it.
- <u>inflation (pl.Series &#124; None):</u> the paired inflation history, for "wilkie_consols" only (required there).
- <u>inflation_weight (float):</u> how much of expected inflation passes into the long yield (Wilkie's CW), default 1.0, one for one.
- <u>inflation_decay (float):</u> how fast expected inflation adapts to new inflation (Wilkie's CD), default 0.05 a year, a memory of about 20 years.
- <u>target_source (str):</u> the "hibbert_two_factor" target: "long_term_rate" (default) or "ewma" (a smoothed average of the rate itself).
- <u>target_term (str):</u> the target's term for "oecd" or "gmdb", default "long"; not equal to `term`.
- <u>target_ticker (str):</u> the target's ticker for "ticker", default "^TNX"; not equal to `ticker`.
- <u>target_smoothing (float):</u> the "ewma" weight on each new observation, between 0 and 1, default 0.05.

**Returns:**

<u>OUParams &#124; GARCHParams &#124; OUCovariateParams &#124; WilkieConsolsParams &#124; MovingTargetOUParams:</u> the fitted parameters, including `initial_value`.

**Raises:**

- <u>ValueError:</u> if an option is unknown or two options clash (such as "garch" with "cir"), no data come back, or the history is too short or shows no pull toward a normal level.

</details>

## calibrate_risk_neutral

Calibrate one country or region's risk-neutral short rate: a flat path at today's observed rate.

A real-world calibration asks how the rate has behaved and projects that forward. A risk-neutral one asks what
today's market says, so that nothing priced off the rate offers a riskless profit (no arbitrage). The simplest
answer that respects this is to take today's rate as given and hold it, rather than fit a speed and volatility
that no market price confirms. Every scenario then discounts at the same rate, so all spread in a valuation
comes from the other factors: a risk-neutral equity entry grows at this rate, and a risk-neutral exchange rate
drifts by the gap between two countries' rates (covered interest parity). This is what
`measure: risk_neutral` selects. Use `calibrate_risk_neutral_forward` when the shape of today's curve, or
interest-rate risk itself, matters for the valuation.

The rate's history still sets its correlation with the other factors.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.interest_rates.interest_rates_controller import InterestRates

toolkit = Toolkit(["SPY", "^IRX"], api_key="FINANCIAL_MODELING_PREP_KEY")
rates = InterestRates(toolkit)

rates.calibrate_risk_neutral("united_states", ticker="^IRX")
```

Which returns (calibrated on 2026-10-04):

| Field | Value |
|:------|------:|
| level | 0.0399 |
| initial_value | 0.0399 |

Every simulated path holds the 13-week Treasury bill rate at today's 3.99%.

**References:**

- Hull, J., White, A. (1990). "Pricing Interest-Rate-Derivative Securities." The Review of Financial Studies, 3(4), 573-592. <https://doi.org/10.1093/rfs/3.4.573>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate_risk_neutral(
    name: str,
    source: str = 'ticker',
    ticker: str = '^IRX',
    country: str = 'United States',
    term: str = 'short',
    period: str = 'daily',
) -> DeterministicParams
```

**Args:**

- <u>name (str):</u> the entry's name, also its factor name in the simulation.
- <u>source (str):</u> "ticker" (default), "oecd" or "gmdb", as in `calibrate`.
- <u>ticker (str):</u> the yield ticker for source="ticker", default "^IRX".
- <u>country (str):</u> the country for source="oecd" or "gmdb", default "United States".
- <u>term (str):</u> the "short" (default) or "long" rate, for source="oecd" or "gmdb".
- <u>period (str):</u> data frequency, default "daily"; the same choices as in `calibrate`.

**Returns:**

<u>DeterministicParams:</u> `level` and `initial_value`, both today's observed rate.

**Raises:**

- <u>ValueError:</u> if `source` or `period` is not recognized, or no data come back.

</details>

## calibrate_risk_neutral_forward

Calibrate one country or region's risk-neutral short rate that follows today's forward curve: a random,
mean-reverting rate whose average path matches the curve the market prices today.

The rate still moves randomly, but it reverts toward the path today's Treasury curve implies rather than toward
one historical average, so the average discount factor across scenarios reproduces today's zero-coupon bond
prices at every maturity. That is the property a market-consistent valuation of interest-rate-sensitive
liabilities and options needs: the curve is matched exactly, and the spread around it prices the optionality.
This is what `risk_neutral_forward_curve: true` selects.

The model is [Hull-White (1990)](https://doi.org/10.1093/rfs/3.4.573) in the form of
[Brigo and Mercurio (2006)](https://doi.org/10.1007/978-3-540-34604-3), Section 3.3: `r(t) = x(t) + alpha(t)`, a
mean-reverting random part plus a fixed shift that matches the forward curve at every maturity. Rates are
normally distributed, so they can go negative. The speed and volatility are the historical ones from
`calibrate`, not implied from swaption prices, so treat option values as indicative. The curve is a
[Nelson-Siegel (1987)](https://doi.org/10.1086/296409) fit to the latest 13-week, 5, 10 and 30-year Treasury
yields (`^IRX`, `^FVX`, `^TNX`, `^TYX`), which the Toolkit must include.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.interest_rates.interest_rates_controller import InterestRates

toolkit = Toolkit(["SPY", "^IRX", "^FVX", "^TNX", "^TYX"], api_key="FINANCIAL_MODELING_PREP_KEY")
rates = InterestRates(toolkit)

rates.calibrate_risk_neutral_forward("united_states", ticker="^IRX", period="monthly")
```

Which returns (calibrated on 2026-10-04):

| Field | Value |
|:------|------:|
| mean_reversion_speed | 0.7344 |
| volatility | 0.0071 |
| anchor_level | 0.0572 |
| anchor_slope | -0.0181 |
| initial_value | 0.0391 |

Today's curve starts at 3.91% (5.72% - 1.81%) and rises toward 5.72%, steering the simulated rate upward.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate_risk_neutral_forward(
    name: str,
    source: str = 'ticker',
    ticker: str = '^IRX',
    country: str = 'United States',
    term: str = 'short',
    period: str = 'daily',
    decay: float = 0.7308,
) -> HullWhiteForwardParams
```

**Args:**

- <u>name (str):</u> the entry's name, also its factor name in the simulation.
- <u>source (str):</u> "ticker" (default), "oecd" or "gmdb", for the speed and volatility fit, as in `calibrate`.
- <u>ticker (str):</u> the yield ticker for "ticker", default "^IRX".
- <u>country (str):</u> the country for "oecd" or "gmdb", default "United States".
- <u>term (str):</u> "short" (default) or "long", for "oecd" or "gmdb".
- <u>period (str):</u> data frequency for both fits, default "daily".
- <u>decay (float):</u> the Nelson-Siegel decay, which sets where the curve's hump sits, default 0.7308.

**Returns:**

<u>HullWhiteForwardParams:</u> `mean_reversion_speed`, `volatility`, the curve's `anchor_level`, `anchor_slope`, `anchor_curvature` and `anchor_decay`, and `initial_value`, today's short rate.

**Raises:**

- <u>ValueError:</u> if `source`, `period` or `decay` is not valid, no data come back, or the rate shows no pull toward a normal level.

</details>

## names

The names of every interest-rate entry calibrated so far, in calibration order.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
interestrates.names  # property -> list[str]
```

</details>

## params

The calibrated parameters for one interest-rate entry.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
params(
    name: str,
) -> OUParams | GARCHParams | OUCovariateParams | DeterministicParams | HullWhiteForwardParams | WilkieConsolsParams | MovingTargetOUParams
```

**Args:**

- <u>name (str):</u> the entry's name, as passed to `calibrate`.

**Raises:**

- <u>RuntimeError:</u> if that entry has not been calibrated yet.

</details>

## step_function

The one-step rule that moves the rate forward for a given method: `step_hull_white` for "hull_white" and
`step_cir` for "cir", both described below.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
InterestRates.step_function(method: str)
```

**Args:**

- <u>method (str):</u> "hull_white" or "cir".

</details>

## changes

The historical period-over-period changes in one entry's rate, which set its correlation with the other
factors.

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

## series

The historical rate level for one entry. Other factors use it where they need the level itself rather than its
changes, such as equities' `hibbert_regime_switching` method, which fits returns in excess of this rate.

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

The observation dates that go with `series(name)`, so other data can be lined up with this rate by date.

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

## How It Is Calculated

The model functions behind this page, each with the formula it implements.

{% raw %}
### fit_cir_process

Fit the Cox-Ingersoll-Ross (CIR) short-rate model to a rate history: the same pull toward a long-run level as
Hull-White, but with swings that scale with the square root of the rate itself.

That scaling is the point of CIR: when rates are high they move a lot, and as they approach zero the moves
shrink, so simulated rates stay near or above zero. It suits a view that deeply negative rates are not a
plausible scenario for the liabilities in question; the price is a weaker fit in a zero-rate era, when CIR sees
almost no volatility. The speed and long-run level are fitted as in Hull-White, and the volatility from the
period-by-period surprises divided by the square root of the rate.

The formula is as follows:

$$
\text{dr} = a \cdot (\theta - r) \cdot \text{dt} + \sigma \cdot \sqrt{r} \cdot \text{dW}
$$

$$
\sigma = \operatorname{std}(e_{t} / \sqrt{r_{t-1}}) / \sqrt{\text{dt}},\;\; \text{over} \;\; r_{t-1} \geq \text{minimum\_level}
$$

$$
2 \cdot a \cdot \theta \geq \sigma ^{2} (\text{Feller condition})
$$

Where e_t is the unexpected part of each change, given the pull toward theta. Negative observations (the US
bill rate printed some in 2015 and 2020) are set to zero, since CIR has no room for them. Days with almost zero
rates are left out of the volatility estimate, because dividing by a near-zero sqrt(r) would inflate it many
times over. When the Feller condition fails, the fit still holds but simulated rates touch zero more often than
the theoretical model would.

**References:**

- Cox, J.C., Ingersoll, J.E., Ross, S.A. (1985). "A Theory of the Term Structure of Interest Rates." Econometrica, 53(2), 385-407. <https://doi.org/10.2307/1911242>
- Vasicek, O. (1977). "An Equilibrium Characterization of the Term Structure." Journal of Financial Economics, 5(2), 177-188. <https://doi.org/10.1016/0304-405x(77>)90016-2
- Chan, K.C., Karolyi, G.A., Longstaff, F.A., Sanders, A.B. (1992). "An Empirical Comparison of Alternative Models of the Short-Term Interest Rate." Journal of Finance, 47(3), 1209-1227. Nests Vasicek and CIR as special cases of one level-scaled diffusion. <https://doi.org/10.1111/j.1540-6261.1992.tb04011.x>
- Ahlgrim, K.C. "Hull-White Term Structure Model." CAS Exam 8 Online Course, Module 4. <https://www.casact.org/sites/default/files/old/oncourses_module4_ahlgrim.pdf>
- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2008). "A Comparison of Actuarial Financial Scenario Generators." Casualty Actuarial Society. <https://www.casact.org/sites/default/files/document/darcy_1.pdf>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fit_cir_process(
    short_rate: pl.Series,
    time_step: float,
    minimum_level: float = _MINIMUM_LEVEL_FOR_CIR_VOLATILITY,
) -> OUParams
```

**Args:**

- <u>short_rate (pl.Series):</u> the short-rate history as decimals, evenly spaced.
- <u>time_step (float):</u> the time between observations, in years (1/12 for monthly).
- <u>minimum_level (float):</u> rates below this are left out of the volatility estimate, default 10bp; a series on another scale, such as a variance, needs a cutoff on its own scale.

**Returns:**

<u>OUParams:</u> the mean-reversion speed, long-run level, volatility and today's rate.

**Raises:**

- <u>ValueError:</u> if too few observations remain above `minimum_level`.

</details>
{% endraw %}

### step_hull_white

Move a Hull-White short rate forward one step: part of the gap to the long-run level closes, and a normally
distributed shock is added.

Each step the rate keeps a share exp(-a * dt) of its gap to theta, so after a shock the rate drifts back at a
steady pace, while the shock's size grows with the step but levels off for long steps, because mean reversion
caps how far the rate can wander. The long-run spread of rates around theta is sigma / sqrt(2 * a): a fast pull
keeps rates in a narrow band. The step is the exact one for this model, so a yearly simulation gives the same
distribution as a daily one.

The formula is as follows:

$$
r(t + \text{dt}) = \theta + (r(t) - \theta) \cdot \exp(- a \cdot \text{dt}) + \sigma \cdot \sqrt{(1 - \exp(- 2 \cdot a \cdot \text{dt})) / (2 \cdot a)} \cdot z
$$

Where a is the mean-reversion speed, theta the long-run level, sigma the volatility and z a standard normal draw.
Nothing stops the rate from going below zero, which is how Hull-White allows for negative rates.

**References:**

- Vasicek, O. (1977). "An Equilibrium Characterization of the Term Structure." Journal of Financial Economics, 5(2), 177-188. Source of the exact transition used here. <https://doi.org/10.1016/0304-405x(77>)90016-2
- Hull, J., White, A. (1990). "Pricing Interest-Rate-Derivative Securities." The Review of Financial Studies, 3(4), 573-592. The Gaussian, mean-reverting short-rate model generalizing Vasicek (1977) to a time-varying long-run mean, universally known as "the Hull-White model". <https://doi.org/10.1093/rfs/3.4.573>
- Ahlgrim, K.C. "Hull-White Term Structure Model." CAS Exam 8 Online Course, Module 4. <https://www.casact.org/sites/default/files/old/oncourses_module4_ahlgrim.pdf>
- Society of Actuaries & Casualty Actuarial Society (2002). "Report on Modeling of Economic Series Coordinated with Interest Rate Scenarios." <https://www.soa.org/globalassets/assets/files/sections/modeling-of-economic-scenarios.pdf>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
step_hull_white(
    current_value: np.ndarray | float,
    shock: np.ndarray | float,
    time_step: float,
    params: OUParams,
) -> np.ndarray
```

**Args:**

- <u>current_value (np.ndarray &#124; float):</u> today's short rate in each scenario.
- <u>shock (np.ndarray &#124; float):</u> the random draw for this step, standard normal.
- <u>time_step (float):</u> the step length, in years.
- <u>params (OUParams):</u> the calibrated speed, long-run level and volatility.

**Returns:**

<u>np.ndarray:</u> the short rate one step later; it may be negative.

</details>

{% raw %}
### step_cir

Move a CIR short rate forward one step: the same pull toward the long-run level as Hull-White, with a shock
that shrinks as the rate approaches zero.

Because the shock scales with sqrt(r), a rate of 1% moves about a third as much as one of 9%, so low-rate
scenarios are calm and high-rate scenarios volatile, as in the 1970s and 1980s. The step is the full-truncation
scheme of Lord, Koekkoek and van Dijk (2010), the most accurate of their simple schemes.

The formula is as follows:

$$
r(t + \text{dt}) = r(t) + a \cdot (\theta - r +) \cdot \text{dt} + \sigma \cdot \sqrt{r + \cdot \text{dt}} \cdot z
$$

$$
r + = \max(r(t),\; 0)
$$

Only the pull and the shock size use r+; the rate itself is not floored, so it is not stuck at zero once it gets
there. As an approximation to the exact CIR distribution, a path can dip slightly below zero with coarse steps;
monthly or finer steps keep this rare.

**References:**

- Cox, J.C., Ingersoll, J.E., Ross, S.A. (1985). "A Theory of the Term Structure of Interest Rates." Econometrica, 53(2), 385-407. <https://doi.org/10.2307/1911242>
- Lord, R., Koekkoek, R., van Dijk, D. (2010). "A Comparison of Biased Simulation Schemes for Stochastic Volatility Models." Quantitative Finance, 10(2), 177-194. <https://doi.org/10.1080/14697680802392496>
- Andersen, L. (2008). "Simple and Efficient Simulation of the Heston Stochastic Volatility Model." Journal of Computational Finance, 11(3), 1-42. Its Quadratic-Exponential scheme is a lower-bias alternative for a CIR process, not implemented here. <https://doi.org/10.21314/JCF.2008.189>
- Ahlgrim, K.C. "Hull-White Term Structure Model." CAS Exam 8 Online Course, Module 4. <https://www.casact.org/sites/default/files/old/oncourses_module4_ahlgrim.pdf>
- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2008). "A Comparison of Actuarial Financial Scenario Generators." Casualty Actuarial Society. <https://www.casact.org/sites/default/files/document/darcy_1.pdf>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
step_cir(
    current_value: np.ndarray | float,
    shock: np.ndarray | float,
    time_step: float,
    params: OUParams,
) -> np.ndarray
```

**Args:**

- <u>current_value (np.ndarray &#124; float):</u> today's short rate in each scenario (may be slightly negative).
- <u>shock (np.ndarray &#124; float):</u> the random draw for this step, standard normal.
- <u>time_step (float):</u> the step length, in years.
- <u>params (OUParams):</u> the calibrated speed, long-run level and volatility.

**Returns:**

<u>np.ndarray:</u> the short rate one step later; it can dip slightly below zero.

</details>
{% endraw %}

### hull_white_alpha

The path a risk-neutral Hull-White short rate is centred on, chosen so the scenarios reprice today's yield curve
exactly.

The short rate is split into a random, mean-reverting part x(t) that starts at zero and a fixed path alpha(t)
(Brigo and Mercurio, 2006, Section 3.3). alpha(t) is today's instantaneous forward rate f^M(0, t), read off the
Nelson-Siegel fit to today's curve, plus a small convexity term. That term is needed because discounting is
convex in rates: random rates raise the average discount factor, so the centre is lifted slightly to keep zero-
coupon bond prices where the market has them. The adjustment grows with volatility and maturity and is small
for typical parameters (a few basis points).

The formula is as follows:

$$
r(t) = x(t) + \alpha(t),\;\; \text{with dx} = - a \cdot x \cdot \text{dt} + \sigma \cdot \text{dW and}\; x (0) = 0
$$

$$
\alpha(t) = f ^{M} (0,\; t) + \sigma ^{2} / (2 \cdot a ^{2}) \cdot (1 - \exp(- a \cdot t)) ^{2}
$$

$$
\theta(t) = \text{df} ^{M} (0,\; t) / \text{dt} + a \cdot f ^{M} (0,\; t) + \sigma ^{2} / (2 \cdot a) \cdot (1 - \exp(- 2 \cdot a \cdot t))
$$

The last line is the same model in Hull and White's (1990) form, dr = (theta(t) - a * r) * dt + sigma * dW.

**References:**

- Brigo, D., Mercurio, F. (2006). "Interest Rate Models: Theory and Practice" (2nd ed.), Section 3.3. Springer Finance. <https://doi.org/10.1007/978-3-540-34604-3>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
hull_white_alpha(
    elapsed_time: float | np.ndarray,
    params: HullWhiteForwardParams,
) -> float | np.ndarray
```

**Args:**

- <u>elapsed_time (float &#124; np.ndarray):</u> years since the valuation date.
- <u>params (HullWhiteForwardParams):</u> the calibrated speed, volatility and today's Nelson-Siegel curve.

**Returns:**

<u>float &#124; np.ndarray:</u> alpha(t), one value per time given.

</details>

### step_hull_white_forward

Move a risk-neutral Hull-White short rate forward one step, reverting toward today's forward curve rather than to
a fixed long-run level.

The rate's distance from the curve-implied path alpha(t) (see `hull_white_alpha`) decays at the calibrated speed
and receives a normal shock, exactly as in `step_hull_white`. Because the centre moves along today's curve, an
upward-sloping curve lifts the simulated rates over time and an inverted one lowers them, and the average
discount factor across scenarios matches today's bond prices. Rates can go negative.

The formula is as follows:

$$
r(t + \text{dt}) = \alpha(t + \text{dt}) + (r(t) - \alpha(t)) \cdot \exp(- a \cdot \text{dt}) + \sigma \cdot \sqrt{(1 - \exp(- 2 \cdot a \cdot \text{dt})) / (2 \cdot a)} \cdot z
$$

**References:**

- Brigo, D., Mercurio, F. (2006). "Interest Rate Models: Theory and Practice" (2nd ed.), Section 3.3. Springer Finance. <https://doi.org/10.1007/978-3-540-34604-3>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
step_hull_white_forward(
    current_value: np.ndarray | float,
    shock: np.ndarray | float,
    time_step: float,
    elapsed_time: float,
    params: HullWhiteForwardParams,
) -> np.ndarray
```

**Args:**

- <u>current_value (float &#124; np.ndarray):</u> today's short rate in each scenario.
- <u>shock (float &#124; np.ndarray):</u> the random draw for this step, standard normal.
- <u>time_step (float):</u> the step length, in years.
- <u>elapsed_time (float):</u> years since the valuation date at the start of this step.
- <u>params (HullWhiteForwardParams):</u> the calibrated speed, volatility and today's Nelson-Siegel curve.

**Returns:**

<u>float &#124; np.ndarray:</u> the short rate one step later.

</details>

### inflation_expectation

Wilkie's (1986) expected inflation: an exponentially weighted average of past inflation (eq. 3.12-3.13), the
inflation the bond market is assumed to build into long yields.

Investors are taken to form expectations adaptively, giving recent inflation more weight but remembering the
past: with Wilkie's CD of 0.05 a year, a burst of inflation raises expected inflation, and with it long yields,
only gradually, and the effect fades over roughly 20 years. That slow adjustment is why a Wilkie long yield
lags an inflation shock rather than jumping with it.

The formula is as follows:

$$
\operatorname{CM}(t) = \text{CD} \cdot I(t) + (1 - \text{CD}) \cdot \operatorname{CM}(t-1)
$$

Where I(t) is the force of inflation and CD the `decay`.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
inflation_expectation(inflation: np.ndarray, decay: float, start: float | None = None) -> np.ndarray
```

**Args:**

- <u>inflation (np.ndarray):</u> inflation per period, oldest first.
- <u>decay (float):</u> CD, the weight of the latest observation, between 0 and 1.
- <u>start (float &#124; None):</u> expected inflation before the first observation, default None (the first observation).

**Returns:**

<u>np.ndarray:</u> expected inflation CM(t) for every period.

</details>

{% raw %}
### fit_wilkie_consols_process

Fit Wilkie's (1986) long-term (Consols) yield model, in which a long yield is expected inflation plus a real
yield, to a history of long yields and inflation.

This is how inflation feeds yields in the classic actuarial model: the nominal long yield C(t) is CW times
expected inflation CM(t), a slow moving average of past inflation, plus a real yield CN(t). The real part is
lognormal and mean-reverting, so it stays positive and its swings are proportional to its level. In the
scenarios, a sustained rise in inflation lifts long yields gradually and permanently, while a brief spike barely
moves them. The fit backs CN(t) out of the data and fits its persistence CA1, long-run level CMU and volatility
CSD; CW and CD stay at Wilkie's published values (his Reduced Basis).

The formula is as follows:

$$
\operatorname{CM}(t) = \text{CD\_dt} \cdot \operatorname{dlnQ}(t) + (1 - \text{CD\_dt}) \cdot \operatorname{CM}(t-1),\;\; \text{started at CM} (0) = \operatorname{dlnQ}(0)
$$

$$
\text{CD\_dt} = 1 - (1 - \text{CD}) ^{\text{dt}}
$$

$$
\operatorname{CN}(t) = C(t) - \text{CW} \cdot \operatorname{CM}(t)
$$

$$
\text{ln CN} (t) = \text{ln CMU} + \text{CA1} \cdot (\text{ln CN} (t-1) - \text{ln CMU}) + \text{CSD} \cdot \operatorname{CZ}(t)
$$

**References:**

- Wilkie, A.D. (1986). "A stochastic investment model for actuarial use." Transactions of the Faculty of Actuaries, 39, 341-403. Section 3.12-3.15, the Consols yield model and its Reduced Basis parameterisation. <https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fit_wilkie_consols_process(
    consols_yield: pl.Series,
    inflation: pl.Series,
    inflation_weight: float = 1.0,
    inflation_decay: float = 0.05,
    time_step: float = 1.0,
) -> WilkieConsolsParams
```

**Args:**

- <u>consols_yield (pl.Series):</u> the long-term government yield history as decimals (0.04 is 4%), evenly spaced.
- <u>inflation (pl.Series):</u> the inflation history over the same dates (Wilkie's dlnQ(t)).
- <u>inflation_weight (float):</u> CW, how much of expected inflation passes into the yield, default 1.0 (Wilkie).
- <u>inflation_decay (float):</u> CD, the yearly weight of new inflation in expected inflation, default 0.05 (Wilkie).
- <u>time_step (float):</u> the time between observations in years, default 1.0; 1/12 for monthly data keeps Wilkie's roughly 20-year memory.

**Returns:**

<u>WilkieConsolsParams:</u> CW, CD, the real yield's CMU, CA1 and CSD, and today's long yield.

**Raises:**

- <u>ValueError:</u> if the two histories differ in length, or the long yield falls to or below expected inflation anywhere in the window (a negative real yield, which the model cannot hold; on US data, end the window before 2008).

</details>
{% endraw %}

### forward_rate_path

The forward rates a spot curve implies: the rate it locks in today for borrowing over `tenor` years starting at
each future date.

This turns an official curve such as EIOPA's into a path for the long-run level a simulated rate is pulled toward
(`long_run_anchor`), so scenarios settle where the curve says rates will be, ending at its ultimate forward rate,
rather than at a historical average. Between published maturities the forward rate is held flat (log-linear
discount factors), and beyond the last maturity it stays at the last forward rate.

The formula is as follows:

$$
\text{ln}\; P (T) = - T \cdot \ln(1 + s(T))
$$

$$
F(t,\; m) = \exp((\text{ln}\; P (t) - \text{ln}\; P (t + m)) / m) - 1
$$

Where s(T) is the spot rate at maturity T, P(T) the discount factor and m the `tenor`.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
forward_rate_path(
    maturities: np.ndarray,
    spot_rates: np.ndarray,
    tenor: float,
    years: np.ndarray,
) -> np.ndarray
```

**Args:**

- <u>maturities (np.ndarray):</u> the curve's maturities in years, ascending, all positive.
- <u>spot_rates (np.ndarray):</u> annually compounded spot rates, one per maturity.
- <u>tenor (float):</u> the forward rate's own length in years, e.g. 1 for a short rate, 10 for a long rate.
- <u>years (np.ndarray):</u> the start dates in years from today.

**Returns:**

<u>np.ndarray:</u> the annually compounded forward rates, one per start date.

**Raises:**

- <u>ValueError:</u> if the inputs are empty, unequal in length, not ascending or `tenor` is not positive.

</details>
