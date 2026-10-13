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

Short and long interest rates, one per country or region. Generated from the docstrings of Finance Scenarios 0.1.0; `help(...)` in Python shows the same text.

```python
from financescenarios.factors.interest_rates.interest_rates_controller import InterestRates
```

```python
InterestRates(toolkit: Toolkit)
```

The Interest Rates module simulates the short rate: the interest rate for a very short lending period, such as a
13-week Treasury bill, from which discounting and the rest of a yield curve are derived. Rates drift with the
economy but are pulled back toward a normal level, the pull this module captures.

Every run has at least one interest rate; add one per country or region. Each becomes a variable in the simulated
scenarios, correlated with the other factors, and factors that need a risk-free rate read it. For a whole yield
curve, add the `yield_curve` or `hjm` factor.

The default model is a mean-reverting Ornstein-Uhlenbeck process, `dr = a(theta - r)dt + sigma*dW`: `a` is how fast
the rate returns to its normal level `theta`, and `sigma` the size of the random swings `dW`, as in
[Vasicek (1977)](https://doi.org/10.1016/0304-405x(77)90016-2). `method` picks the process:

| Method | What it is |
|:-------|:-----------|
| `hull_white` (default) | The model above; the rate can go negative ([Hull and White, 1990][hull-white-1990]). |
| `cir` | Swings shrink as the rate nears zero ([Cox, Ingersoll and Ross, 1985][cir-1985]). |
| `wilkie_consols` | A long-term yield driven by a paired inflation entry ([Wilkie, 1986][wilkie-1986]). |
| `hibbert_two_factor` | Pulled toward a moving long-term rate ([Hibbert et al., 2001][hibbert-2001]). |
| `knw` | Linked both ways with a paired inflation entry; fitted by `Knw`. |
| `knw_sv` | `knw` with a shared, randomly changing volatility; fitted by `KnwSv`. |

[hull-white-1990]: https://doi.org/10.1093/rfs/3.4.573
[cir-1985]: https://doi.org/10.2307/1911242
[wilkie-1986]: https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf
[hibbert-2001]: https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf

`volatility_model: garch` lets the size of the swings change over time
([Bollerslev, 1986](https://doi.org/10.1016/0304-4076(86)90063-1)), with `hull_white` only, and
`condition_on_business_cycle` lets the rate move with the leading indicator. `measure: risk_neutral` follows
today's market instead of history: a flat path at today's rate or, with `risk_neutral_forward_curve`, a random rate
whose average path follows today's forward curve.

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

## calibrate

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

Calibrate one country or region's short rate from its history: how fast it returns to its normal level
(`mean_reversion_speed`), what that level is (`long_run_mean`) and how much it swings (`volatility`).

This learns how the rate has behaved, so the simulated scenarios move the way the real one has. A speed of 0.73 a
year halves a shock in about eleven months (ln 2 / 0.73 years). The default fit regresses each period's change in
the rate on its level ([Vasicek, 1977](https://doi.org/10.1016/0304-405x(77)90016-2)); the class lists the other
methods.

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
- <u>inflation (pl.Series &#124; None):</u> the paired inflation series, for "wilkie_consols" only (required there).
- <u>inflation_weight (float):</u> Wilkie's fixed inflation weight, default 1.0.
- <u>inflation_decay (float):</u> Wilkie's fixed inflation decay, default 0.05.
- <u>target_source (str):</u> the "hibbert_two_factor" target: "long_term_rate" (default) or "ewma" (a smoothed average of the rate itself).
- <u>target_term (str):</u> the target's term for "oecd" or "gmdb", default "long"; not equal to `term`.
- <u>target_ticker (str):</u> the target's ticker for "ticker", default "^TNX"; not equal to `ticker`.
- <u>target_smoothing (float):</u> the "ewma" weight on each new observation, between 0 and 1, default 0.05.

**Returns:**

<u>OUParams &#124; GARCHParams &#124; OUCovariateParams &#124; WilkieConsolsParams &#124; MovingTargetOUParams:</u> the fitted parameters, including `initial_value`.

**Raises:**

- <u>ValueError:</u> if an option is unknown or two options clash (such as "garch" with "cir"), no data come back, or the history is too short or shows no pull toward a normal level.

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

## calibrate_risk_neutral

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

Calibrate one country or region's risk-neutral short rate: a flat path at today's observed rate.

Under the real-world measure the module asks how the rate has behaved and projects that forward. Under the
risk-neutral measure it asks what today's market says, so that nothing priced off the rate offers a riskless
profit (no arbitrage). The simplest answer that respects this is to take today's rate as given and hold it,
rather than fit a speed and volatility that no market price confirms. This is what `measure: risk_neutral`
selects.

It fetches the same series as `calibrate` but uses only the last observation. The full history is still kept, so
`changes` feeds the correlation estimate as usual. Other factors read the level too: a risk-neutral equity entry
uses it as its risk-free rate, and a risk-neutral FX entry uses the gap between two countries' levels.

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

## calibrate_risk_neutral_forward

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

Calibrate one country or region's risk-neutral short rate that follows today's forward curve: a random,
mean-reverting rate whose average path matches the curve the market prices today.

The rate still moves randomly, but it is steered along the path today's Treasury curve implies rather than toward
one historical average, so cash flows discounted along these paths agree with today's bond prices. This is what
`risk_neutral_forward_curve: true` selects.

The model is [Hull-White (1990)](https://doi.org/10.1093/rfs/3.4.573) in the form of
[Brigo and Mercurio (2006)](https://doi.org/10.1007/978-3-540-34604-3), Section 3.3: `r(t) = x(t) + alpha(t)`, a
mean-reverting random part plus a fixed shift that matches the forward curve at every maturity. The speed and
volatility come from the fit to history in `calibrate`, as there are no option prices. The curve is a
[Nelson-Siegel (1987)](https://doi.org/10.1086/296409) fit to the latest 13-week, 5, 10 and 30-year Treasury
yields (`^IRX`, `^FVX`, `^TNX`, `^TYX`), which the Toolkit must include.

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

## names

```python
interestrates.names  # property -> list[str]
```

The names of every interest-rate entry calibrated so far, in calibration order.

## params

```python
params(
    name: str,
) -> OUParams | GARCHParams | OUCovariateParams | DeterministicParams | HullWhiteForwardParams | WilkieConsolsParams | MovingTargetOUParams
```

The calibrated parameters for one interest-rate entry.

**Args:**

- <u>name (str):</u> the entry's name, as passed to `calibrate`.

**Raises:**

- <u>RuntimeError:</u> if that entry has not been calibrated yet.

## step_function

```python
InterestRates.step_function(method: str)
```

The function that moves the rate one step for a given method: the exact mean-reverting step for "hull_white" and a
small-step approximation for "cir". It depends only on `method`, so it also works for saved calibration results.

**Args:**

- <u>method (str):</u> "hull_white" or "cir".

## changes

```python
changes(name: str) -> pl.DataFrame
```

Dated period-over-period changes in one entry's rate, from the data `calibrate` already fetched; used to estimate
the correlations between factors.

**Args:**

- <u>name (str):</u> the entry's name, as passed to `calibrate`.

**Returns:**

<u>pl.DataFrame:</u> two columns, `date` and `value`.

**Raises:**

- <u>RuntimeError:</u> if that entry has not been calibrated yet.

## series

```python
series(name: str) -> pl.Series
```

The historical rate level for one entry, from the data `calibrate` already fetched. Other factors use it where
they need the level itself rather than its changes, such as equities' `hibbert_regime_switching` method, which
fits returns in excess of this rate.

**Args:**

- <u>name (str):</u> the entry's name, as passed to `calibrate`.

**Raises:**

- <u>RuntimeError:</u> if that entry has not been calibrated yet.

## dates

```python
dates(name: str) -> pl.Series
```

The dates that go with `series(name)`, in the same order, so another factor can match its own data to this rate by
date rather than by position.

**Args:**

- <u>name (str):</u> the entry's name, as passed to `calibrate`.

**Raises:**

- <u>RuntimeError:</u> if that entry has not been calibrated yet.

## How It Is Calculated

The model functions behind this page, each with the formula it implements.

{% raw %}
### fit_cir_process

```python
fit_cir_process(
    short_rate: pl.Series,
    time_step: float,
    minimum_level: float = _MINIMUM_LEVEL_FOR_CIR_VOLATILITY,
) -> OUParams
```

Fit a Cox-Ingersoll-Ross (CIR) process to a short-rate series. The drift (a, theta) is fit exactly as the
Ornstein-Uhlenbeck one; the volatility is re-estimated from residuals scaled by sqrt(r), since CIR's diffusion
grows with the rate level.

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

Where e_t is the residual of the exact OU drift. Negative observations (real short-rate tickers such as ^IRX
printed some in 2015 and 2020) are floored at 0 with a warning. Levels below `minimum_level` are left out of the
volatility fit only, because dividing by a near-zero sqrt(r) inflates the scaled residuals: on ^IRX 2005-2024,
339 of 5028 days sit under 1bp and would inflate sigma about 28x. A Feller violation only warns: the fit holds,
but simulated paths touch zero more often than the theoretical process.

**Args:**

- <u>short_rate (pl.Series):</u> historical short-rate observations, evenly spaced.
- <u>time_step (float):</u> time increment between observations, in years.
- <u>minimum_level (float):</u> the near-zero cutoff for the volatility fit, in `short_rate`'s own units; the 10bp default suits interest-rate levels. A different-scale series (e.g. `knw_sv_model.fit_knw_sv_triple`'s variance-scale `v_proxy`, ~1e-4) needs a cutoff in its own units.

**Returns:**

<u>OUParams:</u> calibrated CIR parameters (same shape as the generic OU fit).

**Raises:**

- <u>ValueError:</u> if fewer than `MINIMUM_OBSERVATIONS` remain at or above `minimum_level` after flooring negative observations.

**References:**

- Cox, J.C., Ingersoll, J.E., Ross, S.A. (1985). "A Theory of the Term Structure of Interest Rates." Econometrica, 53(2), 385-407. <https://doi.org/10.2307/1911242>
- Vasicek, O. (1977). "An Equilibrium Characterization of the Term Structure." Journal of Financial Economics, 5(2), 177-188. <https://doi.org/10.1016/0304-405x(77>)90016-2
- Chan, K.C., Karolyi, G.A., Longstaff, F.A., Sanders, A.B. (1992). "An Empirical Comparison of Alternative Models of the Short-Term Interest Rate." Journal of Finance, 47(3), 1209-1227. Nests Vasicek and CIR as special cases of one level-scaled diffusion. <https://doi.org/10.1111/j.1540-6261.1992.tb04011.x>
- Ahlgrim, K.C. "Hull-White Term Structure Model." CAS Exam 8 Online Course, Module 4. <https://www.casact.org/sites/default/files/old/oncourses_module4_ahlgrim.pdf>
- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2008). "A Comparison of Actuarial Financial Scenario Generators." Casualty Actuarial Society. <https://www.casact.org/sites/default/files/document/darcy_1.pdf>
{% endraw %}

### step_hull_white

```python
step_hull_white(
    current_value: np.ndarray | float,
    shock: np.ndarray | float,
    time_step: float,
    params: OUParams,
) -> np.ndarray
```

Advance a Hull-White (Gaussian, Vasicek-family) short-rate process by one time step with the exact transition of
dr = a * (theta - r) * dt + sigma * dW (see `calibration_model.step_ou_process`), not an Euler approximation.

The formula is as follows:

$$
r(t + \text{dt}) = \theta + (r(t) - \theta) \cdot \exp(- a \cdot \text{dt}) + \sigma \cdot \sqrt{(1 - \exp(- 2 \cdot a \cdot \text{dt})) / (2 \cdot a)} \cdot z
$$

Where a is the mean-reversion speed, theta the long-run mean, sigma the volatility and z a standard normal draw.

**Args:**

- <u>current_value (np.ndarray &#124; float):</u> the short rate at the current time step.
- <u>shock (np.ndarray &#124; float):</u> a standard normal draw for this step.
- <u>time_step (float):</u> the time increment, in years.
- <u>params (OUParams):</u> calibrated mean-reversion speed, long-run mean, and volatility.

**Returns:**

<u>np.ndarray:</u> the short rate at the next time step. May be negative (Hull-White allows this).

**References:**

- Vasicek, O. (1977). "An Equilibrium Characterization of the Term Structure." Journal of Financial Economics, 5(2), 177-188. Source of the exact transition used here. <https://doi.org/10.1016/0304-405x(77>)90016-2
- Hull, J., White, A. (1990). "Pricing Interest-Rate-Derivative Securities." The Review of Financial Studies, 3(4), 573-592. The Gaussian, mean-reverting short-rate model generalizing Vasicek (1977) to a time-varying long-run mean, universally known as "the Hull-White model". <https://doi.org/10.1093/rfs/3.4.573>
- Ahlgrim, K.C. "Hull-White Term Structure Model." CAS Exam 8 Online Course, Module 4. <https://www.casact.org/sites/default/files/old/oncourses_module4_ahlgrim.pdf>
- Society of Actuaries & Casualty Actuarial Society (2002). "Report on Modeling of Economic Series Coordinated with Interest Rate Scenarios." <https://www.soa.org/globalassets/assets/files/sections/modeling-of-economic-scenarios.pdf>

{% raw %}
### step_cir

```python
step_cir(
    current_value: np.ndarray | float,
    shock: np.ndarray | float,
    time_step: float,
    params: OUParams,
) -> np.ndarray
```

Advance a CIR short-rate process by one time step with the full-truncation Euler scheme of Lord, Koekkoek and
van Dijk (2010), the lowest-bias of their simple schemes.

The formula is as follows:

$$
r(t + \text{dt}) = r(t) + a \cdot (\theta - r +) \cdot \text{dt} + \sigma \cdot \sqrt{r + \cdot \text{dt}} \cdot z
$$

$$
r + = \max(r(t),\; 0)
$$

Only the coefficients use r+; the update applies to the actual, possibly negative, r(t) and the result is not
floored, so zero is not an absorbing barrier. This is not CIR's exact (noncentral chi-square) transition, so
a path can dip slightly below zero, more often than the theoretical process would.

**Args:**

- <u>current_value (np.ndarray &#124; float):</u> the short rate at the current time step (may be negative).
- <u>shock (np.ndarray &#124; float):</u> a standard normal draw for this step.
- <u>time_step (float):</u> the time increment, in years.
- <u>params (OUParams):</u> calibrated mean-reversion speed, long-run mean, and volatility.

**Returns:**

<u>np.ndarray:</u> the short rate at the next time step. May be negative (not floored).

**References:**

- Cox, J.C., Ingersoll, J.E., Ross, S.A. (1985). "A Theory of the Term Structure of Interest Rates." Econometrica, 53(2), 385-407. <https://doi.org/10.2307/1911242>
- Lord, R., Koekkoek, R., van Dijk, D. (2010). "A Comparison of Biased Simulation Schemes for Stochastic Volatility Models." Quantitative Finance, 10(2), 177-194. <https://doi.org/10.1080/14697680802392496>
- Andersen, L. (2008). "Simple and Efficient Simulation of the Heston Stochastic Volatility Model." Journal of Computational Finance, 11(3), 1-42. Its Quadratic-Exponential scheme is a lower-bias alternative for a CIR process, not implemented here. <https://doi.org/10.21314/JCF.2008.189>
- Ahlgrim, K.C. "Hull-White Term Structure Model." CAS Exam 8 Online Course, Module 4. <https://www.casact.org/sites/default/files/old/oncourses_module4_ahlgrim.pdf>
- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2008). "A Comparison of Actuarial Financial Scenario Generators." Casualty Actuarial Society. <https://www.casact.org/sites/default/files/document/darcy_1.pdf>
{% endraw %}

### hull_white_alpha

```python
hull_white_alpha(
    elapsed_time: float | np.ndarray,
    params: HullWhiteForwardParams,
) -> float | np.ndarray
```

The deterministic shift alpha(t) that makes r(t) = x(t) + alpha(t) reproduce today's forward curve f^M(0, t) in
expectation, with x a zero-drift Ornstein-Uhlenbeck process started at 0 (Brigo & Mercurio 2006, Section 3.3).
f^M(0, t) comes from the anchor curve via `term_structure_model.nelson_siegel_forward`, as in `hjm_model`.

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

**Args:**

- <u>elapsed_time (float &#124; np.ndarray):</u> time since the simulation start, in years.
- <u>params (HullWhiteForwardParams):</u> calibrated mean-reversion speed, volatility, and today's Nelson-Siegel forward-curve anchor.

**Returns:**

<u>float &#124; np.ndarray:</u> alpha(t), same shape as `elapsed_time`.

**References:**

- Brigo, D., Mercurio, F. (2006). "Interest Rate Models: Theory and Practice" (2nd ed.), Section 3.3. Springer Finance. <https://doi.org/10.1007/978-3-540-34604-3>

### step_hull_white_forward

```python
step_hull_white_forward(
    current_value: np.ndarray | float,
    shock: np.ndarray | float,
    time_step: float,
    elapsed_time: float,
    params: HullWhiteForwardParams,
) -> np.ndarray
```

Advance the forward-curve-consistent Hull-White short rate by one time step: the exact OU step of
`step_hull_white`, applied to x(t) = r(t) - alpha(t) instead of to r(t) itself.

The formula is as follows:

$$
r(t + \text{dt}) = \alpha(t + \text{dt}) + (r(t) - \alpha(t)) \cdot \exp(- a \cdot \text{dt}) + \sigma \cdot \sqrt{(1 - \exp(- 2 \cdot a \cdot \text{dt})) / (2 \cdot a)} \cdot z
$$

Unlike the other step functions it needs `elapsed_time`, since alpha(t) moves with calendar time along the curve;
see scenarios_controller._make_hull_white_forward_step for how the engine supplies it.

**Args:**

- <u>current_value (float &#124; np.ndarray):</u> the short rate at the current time step.
- <u>shock (float &#124; np.ndarray):</u> a standard normal draw for this step.
- <u>time_step (float):</u> the time increment, in years.
- <u>elapsed_time (float):</u> time since the simulation start, in years, at the *current* time step (before this step advances).
- <u>params (HullWhiteForwardParams):</u> calibrated mean-reversion speed, volatility, and forward-curve anchor.

**Returns:**

<u>float &#124; np.ndarray:</u> the short rate at the next time step.

**References:**

- Brigo, D., Mercurio, F. (2006). "Interest Rate Models: Theory and Practice" (2nd ed.), Section 3.3. Springer Finance. <https://doi.org/10.1007/978-3-540-34604-3>

### inflation_expectation

```python
inflation_expectation(inflation: np.ndarray, decay: float, start: float | None = None) -> np.ndarray
```

Wilkie's (1986) expected inflation: an exponentially weighted moving average of past inflation (eq. 3.12-3.13).

The formula is as follows:

$$
\operatorname{CM}(t) = \text{CD} \cdot I(t) + (1 - \text{CD}) \cdot \operatorname{CM}(t-1)
$$

Where I(t) is the force of inflation and CD the `decay`. It starts from `start`, or the first observation.

**Args:**

- <u>inflation (np.ndarray):</u> inflation per period, oldest first.
- <u>decay (float):</u> CD, the weight of the latest observation, between 0 and 1.
- <u>start (float &#124; None):</u> CM before the first observation. Defaults to None, the first observation itself.

**Returns:**

<u>np.ndarray:</u> CM(t) for every period, the same length as `inflation`.

{% raw %}
### fit_wilkie_consols_process

```python
fit_wilkie_consols_process(
    consols_yield: pl.Series,
    inflation: pl.Series,
    inflation_weight: float = 1.0,
    inflation_decay: float = 0.05,
    time_step: float = 1.0,
) -> WilkieConsolsParams
```

Fit Wilkie's (1986) Reduced Basis Consols yield process: recover the latent real-yield component CN(t) from the
nominal yield and inflation, then fit an AR(1) to ln CN(t) with `calibration_model.fit_ar1_process`.

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

**Args:**

- <u>consols_yield (pl.Series):</u> historical nominal Consols (long-term) yield observations, evenly spaced, decimal (e.g. 0.04 == 4%). Length n.
- <u>inflation (pl.Series):</u> the paired inflation entry's raw historical rate series (Wilkie's dlnQ(t)), same length n and time index.
- <u>inflation_weight (float):</u> CW, fixed (not fit); Wilkie's own published value is the default.
- <u>inflation_decay (float):</u> CD, fixed (not fit), per year as in Wilkie's annual model; his Reduced Basis value 0.05 is the default.
- <u>time_step (float):</u> the data's step in years (1/12 for monthly), to scale CD so the average keeps Wilkie's roughly 20-year memory. Defaults to 1.0, yearly data.

**Returns:**

<u>WilkieConsolsParams:</u> the calibrated process parameters.

**Raises:**

- <u>ValueError:</u> if `consols_yield`/`inflation` aren't the same length, or the derived real-yield component CN(t) is not strictly positive throughout (ln CN needs CN > 0; on US data end the fit window before 2008).

**References:**

- Wilkie, A.D. (1986). "A stochastic investment model for actuarial use." Transactions of the Faculty of Actuaries, 39, 341-403. Section 3.12-3.15, the Consols yield model and its Reduced Basis parameterisation. <https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf>
{% endraw %}

### forward_rate_path

```python
forward_rate_path(
    maturities: np.ndarray,
    spot_rates: np.ndarray,
    tenor: float,
    years: np.ndarray,
) -> np.ndarray
```

The `tenor`-year forward rate starting at each of `years`, read off an annually compounded spot curve: the rate
the curve locks in today for borrowing over [t, t + tenor]. Discount factors are interpolated log-linearly
(piecewise-constant forward rates between published maturities) and held at the last forward rate beyond the
last maturity.

The formula is as follows:

$$
\text{ln}\; P (T) = - T \cdot \ln(1 + s(T))
$$

$$
F(t,\; m) = \exp((\text{ln}\; P (t) - \text{ln}\; P (t + m)) / m) - 1
$$

Where s(T) is the spot rate at maturity T, P(T) the discount factor and m the `tenor`. Used as the long-run level
a rate is pulled toward (`long_run_anchor`), so simulated rates settle where an official curve such as EIOPA's,
which ends at the ultimate forward rate, says they should.

**Args:**

- <u>maturities (np.ndarray):</u> the curve's maturities in years, ascending, all positive.
- <u>spot_rates (np.ndarray):</u> annually compounded spot rates, one per maturity.
- <u>tenor (float):</u> the forward rate's own length in years, e.g. 1 for a short rate, 10 for a long rate.
- <u>years (np.ndarray):</u> the start dates in years from today.

**Returns:**

<u>np.ndarray:</u> the annually compounded forward rates, one per start date.

**Raises:**

- <u>ValueError:</u> if the inputs are empty, unequal in length, not ascending or `tenor` is not positive.
