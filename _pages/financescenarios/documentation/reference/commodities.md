---
title: "Commodities"
seo_title: "Commodities Reference – Finance Scenarios"
excerpt: "Commodity futures, one per commodity."
description: "Commodity futures, one per commodity."
author_profile: false
permalink: /projects/financescenarios/docs/reference/commodities
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

Commodity futures, one per commodity. Generated from the docstrings of Finance Scenarios 0.1.0; `help(...)` in Python shows the same text.

```python
from financescenarios.factors.commodities.commodities_controller import Commodities
```

```python
Commodities(toolkit: Toolkit)
```

The Commodities module simulates commodity prices, such as crude oil or gold, as prices that swing widely but are
pulled back toward a normal level over time.

Each entry in `commodities` (an empty list by default) becomes a simulated price path, linked to the other factors
through the correlation matrix and usable as a portfolio holding.

Unlike a stock index, a commodity has a natural price level: storage costs and the convenience yield (the benefit of
holding the physical good, such as keeping a refinery running) pull the spot price back toward what it costs to
produce and store, as [Schwartz (1997)](https://doi.org/10.1111/j.1540-6261.1997.tb02721.x) showed. The default model
(`method="single_factor"`) lets the log price revert to a long-run level:

```text
d(log S) = kappa * (mu - log S) dt + sigma * dW
```

where `kappa` is the speed of the pull, `mu` the long-run log price and `sigma` the volatility. Working in logs keeps
the price positive.

The two-factor model of [Schwartz and Smith (2000)](https://doi.org/10.1287/mnsc.46.7.893.12034)
(`method="schwartz_smith"`) writes the log price as `chi + xi`: a short-term deviation that fades back to zero plus a
long-term level that drifts as a random walk, the convenience-yield economics of
[Gibson and Schwartz (1990)](https://doi.org/10.1111/j.1540-6261.1990.tb05114.x) in another form. It separates a
temporary shock, such as a supply outage, from a lasting change in costs. The parts are simulated as `{name}_chi` and
`{name}_xi`, the price itself under `name`. With `measure="risk_neutral"` the drifts match today's futures prices
instead.

Data: the "Adj Close" of any commodity or futures ticker in the `Toolkit` (Yahoo Finance, no API key needed), such as
`CL=F` (WTI crude oil) or `GC=F` (gold). The two-factor model also reads today's futures curve, available for crude
oil, natural gas, gold, silver, copper, corn, wheat and soybeans.

Configuration (`commodities[i]` in a factor set):

| Key | Default | Meaning |
|:----|:--------|:--------|
| `name` | `commodity` | Name in the output. |
| `ticker` | `CL=F` | Commodity or futures ticker. |
| `currency` | `USD` | Reporting label; prices are in US dollars. |
| `period` | `daily` | `daily`, `weekly`, `monthly`, `quarterly` or `yearly`. |
| `method` | `single_factor` | Or `schwartz_smith`. |
| `measure` | `real_world` | Or `risk_neutral` (`schwartz_smith` only). |
| `contracts` | `12` | `schwartz_smith`: futures contracts to fetch. |
| `long_term_window_years` | `3.0` | `schwartz_smith`: years of prices averaged into `xi`. |
| `volatility_model` | `constant` | `single_factor`: or `garch`, volatility that clusters. |
| `condition_on_business_cycle` | `false` | `single_factor`: follow the leading indicator. |
| `beliefs.<field>` | `null` | `single_factor`: override a fitted value. |

A belief's `long_run_mean` is a log price: for 70 USD, set `log(70)`, about 4.25.

**References:**

- Schwartz, E.S. (1997). "The Stochastic Behavior of Commodity Prices: Implications for Valuation and Hedging." Journal of Finance, 52(3), 923-973. <https://doi.org/10.1111/j.1540-6261.1997.tb02721.x>
- Gibson, R., Schwartz, E.S. (1990). "Stochastic Convenience Yield and the Pricing of Oil Contingent Claims." Journal of Finance, 45(3), 959-976. <https://doi.org/10.1111/j.1540-6261.1990.tb05114.x>
- Schwartz, E., Smith, J.E. (2000). "Short-Term Variations and Long-Term Dynamics in Commodity Prices." Management Science, 46(7), 893-911. <https://doi.org/10.1287/mnsc.46.7.893.12034>

## calibrate

```python
calibrate(
    name: str,
    ticker: str = 'CL=F',
    period: str = 'daily',
    volatility_model: str = 'constant',
    business_cycle_covariate: pl.Series | None = None,
    business_cycle_covariate_dates: pl.Series | None = None,
) -> CommodityParams | GARCHParams | OUCovariateParams
```

Calibrate one commodity's single-factor model from its price history.

It fits how fast the log price returns to its normal level (`mean_reversion_speed`), what that level is
(`long_run_mean`) and how much it swings (`volatility`). A speed of 1.37 a year means half of a price spike fades
in about six months (ln 2 / 1.37). `long_run_mean` is a log price, so `exp(long_run_mean)` is the price the
process is pulled toward, while `initial_value` is today's actual price.

The fit regresses each period's change in log price on the previous log price by ordinary least squares, the exact
discrete form of the [Schwartz (1997)](https://doi.org/10.1111/j.1540-6261.1997.tb02721.x) model. A price that
trends rather than settles back, such as gold monthly since 2016, raises an error.

**Args:**

- <u>name (str):</u> the commodity's name in the output.
- <u>ticker (str):</u> any commodity or futures ticker in the Toolkit. Defaults to "CL=F" (WTI crude).
- <u>period (str):</u> the fit's time step: "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
- <u>volatility_model (str):</u> "constant", or "garch" for volatility that clusters ([Bollerslev, 1986](https://doi.org/10.1016/0304-4076(86)90063-1)). Defaults to "constant".
- <u>business_cycle_covariate (pl.Series &#124; None):</u> a leading indicator's history, such as `LeadingIndicator.series`; when given, the price also moves with its change. Defaults to None.
- <u>business_cycle_covariate_dates (pl.Series &#124; None):</u> the dates of `business_cycle_covariate`, required with it. Defaults to None.

**Returns:**

<u>CommodityParams &#124; GARCHParams &#124; OUCovariateParams:</u> `mean_reversion_speed`, `long_run_mean`, `volatility` and `initial_value`, or their GARCH or business-cycle form.

**Raises:**

- <u>ValueError:</u> if an option is not recognised or the covariate is combined with "garch", the ticker has no data, a price is not strictly positive (daily WTI crude closed at -37.63 USD on 2020-04-20) or the price shows no mean reversion.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.commodities.commodities_controller import Commodities

toolkit = Toolkit(["CL=F", "NG=F"], start_date="2016-01-01")
commodities = Commodities(toolkit)

commodities.calibrate("crude_oil", ticker="CL=F", period="monthly")
commodities.calibrate("natural_gas", ticker="NG=F", period="monthly")
```

Which returns (calibrated on 2026-10-04):

| name | mean_reversion_speed | long_run_mean | volatility | initial_value |
|:-----|---------------------:|--------------:|-----------:|--------------:|
| crude_oil | 1.3659 | 4.2056 | 0.4692 | 91.1100 |
| natural_gas | 1.6133 | 1.1284 | 0.5993 | 3.0350 |

Crude oil starts at 91.11 USD and is pulled toward exp(4.2056) = 67.06 USD.

## calibrate_schwartz_smith

```python
calibrate_schwartz_smith(
    name: str,
    ticker: str = 'CL=F',
    period: str = 'daily',
    contracts: int = 12,
    long_term_window_years: float = 3.0,
) -> SchwartzSmithParams
```

Calibrate one commodity's two-factor Schwartz and Smith model from its price history and today's futures curve.

The log price is split into a short-term deviation `chi` that fades back to zero and a long-term level `xi` that
drifts as a random walk. It separates a temporary dislocation (a refinery outage) from a lasting change in
production costs. The temporary part halves in ln 2 / `chi.mean_reversion_speed` years and today's price is
`exp(chi.initial_value + xi.initial_value)`.

[Schwartz and Smith (2000)](https://doi.org/10.1287/mnsc.46.7.893.12034) estimate the model from years of futures
prices. Only today's curve is available here, so `xi` is a trailing average of the log price and `chi` the rest,
which sets the speed and today's split. The volatilities and their correlation are fitted to the recent swings of
each listed futures contract; failing that, with a warning, the price history alone sets them, which understates
`xi`'s volatility.

**Args:**

- <u>name (str):</u> the commodity's name; its parts are stored as `{name}_chi` and `{name}_xi`.
- <u>ticker (str):</u> the spot ticker. A futures curve exists for "CL=F", "NG=F", "GC=F", "SI=F", "HG=F", "ZC=F", "ZW=F" and "ZS=F". Defaults to "CL=F".
- <u>period (str):</u> time step of the price history, "daily" to "yearly". Defaults to "daily".
- <u>contracts (int):</u> monthly futures contracts to try to fetch, at least 2. Defaults to 12.
- <u>long_term_window_years (float):</u> years of prices averaged into `xi`. Defaults to 3.0.

**Returns:**

<u>SchwartzSmithParams:</u> `chi` (speed, a long-run mean of 0, volatility, today's value) and `xi` (drift, volatility, today's value).

**Raises:**

- <u>ValueError:</u> if an input is invalid, the price history is too short or not strictly positive, `chi` does not mean-revert, or the futures curve comes back empty.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.commodities.commodities_controller import Commodities

toolkit = Toolkit(["CL=F"], start_date="2021-01-01")
commodities = Commodities(toolkit)

commodities.calibrate_schwartz_smith("oil", ticker="CL=F", period="daily")
```

Which returns (calibrated on 2026-10-04):

| factor | mean_reversion_speed | long_run_mean | drift | volatility | initial_value |
|:-------|---------------------:|--------------:|------:|-----------:|--------------:|
| oil_chi | 2.7274 | 0.0000 | | 0.4177 | 0.2145 |
| oil_xi | | | -0.0251 | 0.0058 | 4.2975 |

Today's 91.11 USD price splits into a long-term level of exp(4.2975) = 73.5 USD and a 24% short-term premium.

## calibrate_schwartz_smith_risk_neutral

```python
calibrate_schwartz_smith_risk_neutral(
    name: str,
    ticker: str = 'CL=F',
    period: str = 'daily',
    contracts: int = 12,
    long_term_window_years: float = 3.0,
) -> SchwartzSmithParams
```

Calibrate one commodity's two-factor Schwartz and Smith model so that it reproduces today's futures prices.

Instead of asking how the price has behaved, this asks what path the futures market prices in (the risk-neutral
view). A curve that slopes down (backwardation) gives the long-term level `xi` a negative drift; one that slopes
up (contango), a positive one. Use it for pricing and hedging, not as a forecast.

The speed and volatilities are fitted as in `calibrate_schwartz_smith`, since they are the same under both views.
Only the two drifts are fitted here, by ordinary least squares on the futures pricing formula of
[Schwartz and Smith (2000)](https://doi.org/10.1287/mnsc.46.7.893.12034) (eq. 9). This needs a futures curve and
raises without one.

**Args:**

- <u>name (str):</u> the commodity's name; its parts are stored as `{name}_chi` and `{name}_xi`.
- <u>ticker (str):</u> a spot ticker with a futures curve: "CL=F", "NG=F", "GC=F", "SI=F", "HG=F", "ZC=F", "ZW=F" or "ZS=F". Defaults to "CL=F".
- <u>period (str):</u> time step of the price history, "daily" to "yearly". Defaults to "daily".
- <u>contracts (int):</u> monthly futures contracts to try to fetch, at least 2. Defaults to 12.
- <u>long_term_window_years (float):</u> years of prices averaged into `xi`. Defaults to 3.0.

**Returns:**

<u>SchwartzSmithParams:</u> the real-world fit, with `chi`'s `long_run_mean` and `xi`'s `drift` set by today's futures prices.

**Raises:**

- <u>ValueError:</u> if an input is invalid, the ticker has no futures curve, the price history fails the real-world fit, or fewer than 2 futures contracts have a price today.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.commodities.commodities_controller import Commodities

toolkit = Toolkit(["CL=F"], start_date="2021-01-01")
commodities = Commodities(toolkit)

commodities.calibrate_schwartz_smith_risk_neutral("oil_q", ticker="CL=F", period="daily")
```

Which returns (calibrated on 2026-10-04):

| factor | mean_reversion_speed | long_run_mean | drift | volatility | initial_value |
|:-------|---------------------:|--------------:|------:|-----------:|--------------:|
| oil_q_chi | 2.7274 | 0.1965 | | 0.4177 | 0.2145 |
| oil_q_xi | | | -0.1775 | 0.0058 | 4.2975 |

Only the drifts differ from the real-world fit. The crude curve that day fell from 91.11 USD (November 2026) to
77.90 USD (September 2027), so the market prices the long-term level falling about 17.7% a year, against 2.5% in
the real-world fit.

## names

```python
commodities.names  # property -> list[str]
```

The names of every commodity calibrated so far, in calibration order; a two-factor entry is listed as its `_chi`
and `_xi` parts.

## params

```python
params(name: str) -> CommodityParams | OUParams | RandomWalkParams | GARCHParams | OUCovariateParams
```

The calibrated parameters of one commodity, or of one `_chi` or `_xi` part of a two-factor entry.

**Args:**

- <u>name (str):</u> the name as calibrated, e.g. "crude_oil" or "oil_chi".

**Raises:**

- <u>RuntimeError:</u> if `name` has not been calibrated yet.

## step_function

```python
commodities.step_function  # property
```

The function that moves a single-factor commodity price one time step forward in the simulation, shared by every
entry.

## changes

```python
changes(name: str) -> pl.DataFrame
```

The dated period-to-period changes in one commodity's log price (or `_chi` or `_xi` part), from the data the
calibration already fetched. The correlation matrix is estimated from these.

**Args:**

- <u>name (str):</u> the name as calibrated, e.g. "crude_oil" or "oil_chi".

**Returns:**

<u>pl.DataFrame:</u> two columns, `date` and `value`.

**Raises:**

- <u>RuntimeError:</u> if `name` has not been calibrated yet.

## How It Is Calculated

The model functions behind this page, each with the formula it implements.

### fit_commodity_process

```python
fit_commodity_process(prices: pl.Series, time_step: float) -> CommodityParams
```

Fit a Schwartz (1997) single-factor commodity model to a historical spot-price series: the exact-transition
OU regression of `calibration_model.fit_ou_process`, run on the *log* price.

The formula is as follows:

$$
X_{t+1} - X_{t} = c + b \cdot X_{t} + e_{t},\;\; X_{t} = \ln(S_{t})
$$

$$
\kappa = - \ln(1 + b) / \text{dt},\;\; \mu = - c / b
$$

$$
\sigma = \operatorname{std}(e_{t}) / \sqrt{(1 - \exp(- 2 \cdot \kappa \cdot \text{dt})) / (2 \cdot \kappa)}
$$

**Args:**

- <u>prices (pl.Series):</u> historical spot-price observations, evenly spaced in time, all > 0.
- <u>time_step (float):</u> time increment between observations, in years.

**Returns:**

<u>CommodityParams:</u> the calibrated mean-reversion speed, long-run log-price level, log-price volatility, and the series' last (actual, not log) value as the simulation starting point.

**Raises:**

- <u>ValueError:</u> if fewer than `MINIMUM_OBSERVATIONS_OU` observations are supplied, any observation is not strictly positive, or the fitted mean-reversion speed is non-positive (the series shows no mean reversion at this time step).

**References:**

- Schwartz, E.S. (1997). "The Stochastic Behavior of Commodity Prices: Implications for Valuation and Hedging." Journal of Finance, 52(3), 923-973. <https://doi.org/10.1111/j.1540-6261.1997.tb02721.x>

### step_commodity_process

```python
step_commodity_process(
    current_value: np.ndarray | float,
    shock: np.ndarray | float,
    time_step: float,
    params: CommodityParams,
) -> np.ndarray
```

Advance the commodity spot price by one time step with the OU process's *exact* transition on the log price,
matching `fit_commodity_process`. Prices go in and come out; the log transform is internal.

The formula is as follows:

$$
X_{t+dt} = \mu + (X_{t} - \mu) \cdot \exp(- \kappa \cdot \text{dt}) + \sigma \cdot \sqrt{(1 - \exp(- 2 \cdot \kappa \cdot \text{dt})) / (2 \cdot \kappa)} \cdot z
$$

$$
S_{t+dt} = \exp(X_{t+dt})
$$

**Args:**

- <u>current_value (np.ndarray &#124; float):</u> the spot price at the current time step (> 0).
- <u>shock (np.ndarray &#124; float):</u> a standard normal draw for this step.
- <u>time_step (float):</u> the time increment, in years.
- <u>params (CommodityParams):</u> calibrated mean-reversion speed, long-run log-price level, and log-price volatility.

**Returns:**

<u>np.ndarray:</u> the spot price at the next time step. Always strictly positive.

**References:**

- Schwartz, E.S. (1997). "The Stochastic Behavior of Commodity Prices: Implications for Valuation and Hedging." Journal of Finance, 52(3), 923-973. <https://doi.org/10.1111/j.1540-6261.1997.tb02721.x>

### fit_schwartz_smith_process

```python
fit_schwartz_smith_process(
    prices: pl.Series,
    time_step: float,
    long_term_window_years: float = 3.0,
) -> tuple[SchwartzSmithParams, float, np.ndarray, np.ndarray]
```

Fit Schwartz & Smith's (2000) two-factor model to a historical spot-price series. The paper's Kalman filter
needs a historical panel of futures prices, which isn't available, so this splits the log price with a proxy:
xi is a trailing moving average and chi the deviation from it. chi is then fit as an OU process with its
long-run mean fixed at 0 (a regression through the origin) and xi as a random walk with drift.

The formula is as follows:

$$
\xi_{t} = \operatorname{mean}(\text{ln}\; \text{S\_t-w} + 1,\; ...,\; \text{ln}\; S_{t}),\;\; w = \text{long\_term\_window\_years} / \text{dt}
$$

$$
\chi_{t} = \ln(S_{t}) - \xi_{t}
$$

$$
\chi_{t+1} - \chi_{t} = b \cdot \chi_{t} + e_{t},\;\; \kappa = - \ln(1 + b) / \text{dt}
$$

$$
\sigma_{\chi} = \operatorname{std}(e_{t}) / \sqrt{(1 - \exp(- 2 \cdot \kappa \cdot \text{dt})) / (2 \cdot \kappa)}
$$

$$
\rho = \operatorname{corr}(e_{t},\; \xi_{t+1} - \xi_{t})
$$

kappa and today's chi/xi split are reliable. sigma_chi, sigma_xi, rho and the xi drift are not: averaging a
random walk damps its increments, so xi's volatility comes out roughly ten times too small on synthetic data.
When a forward curve is available, `commodities_controller.Commodities.calibrate_schwartz_smith` replaces the
volatilities and rho with `fit_schwartz_smith_diffusion_from_forward_curve`'s.

**Args:**

- <u>prices (pl.Series):</u> historical spot-price observations, evenly spaced in time, all > 0.
- <u>time_step (float):</u> time increment between observations, in years.
- <u>long_term_window_years (float):</u> the trailing window (in years) of the xi proxy. The 3-year default matches the roughly 3-year half-life of the slow equilibrium factor in Schwartz & Smith's later three-factor note (Table A1, eta = 0.226 per year).

**Returns:**

<u>tuple[SchwartzSmithParams, float, np.ndarray, np.ndarray]:</u> the calibrated chi/xi processes; rho (needed by `fit_schwartz_smith_risk_neutral`, not by the simulation, which takes the chi/xi correlation from `dependence_model`); and chi's and xi's raw period-to-period changes, which the controller stores for the cross-factor correlation estimate.

**Raises:**

- <u>ValueError:</u> if fewer observations are supplied than `long_term_window_years` implies, any observation is not strictly positive, or chi's fitted mean-reversion speed is non-positive (regression slope outside (-1, 0) under the exact transition; see `calibration_model._fit_ou_drift`'s own docstring for why that range, not just "<= 0", is the correct guard).

**References:**

- Schwartz, E., Smith, J.E. (2000). "Short-Term Variations and Long-Term Dynamics in Commodity Prices." Management Science, 46(7), 893-911. <https://doi.org/10.1287/mnsc.46.7.893.12034>

### fit_schwartz_smith_diffusion_from_forward_curve

```python
fit_schwartz_smith_diffusion_from_forward_curve(
    maturities: np.ndarray,
    volatilities: np.ndarray,
    kappa: float,
) -> tuple[float, float, float]
```

Recover Schwartz & Smith's (2000) chi/xi volatilities and their correlation (sigma_chi, sigma_xi, rho) from the
realized volatility of each listed forward contract, a better-identified source than the spot series (see
`fit_schwartz_smith_process`). The model's instantaneous futures volatility is linear in three unknowns once
kappa is fixed, so one least-squares solve fits them.

The formula is as follows:

$$
\sigma ^{2} (F_{T}) = \exp(- 2 \cdot \kappa \cdot T) \cdot \sigma_{\chi} ^{2} + \sigma_{\xi} ^{2} + 2 \cdot \exp(- \kappa \cdot T) \cdot \rho \cdot \sigma_{\chi} \cdot \sigma_{\xi}
$$

kappa comes from the spot fit rather than being searched jointly: with the dozen or so maturities a forward
curve has, a joint four-parameter search recovered a kappa 7x too large on synthetic data, while the linear
three-parameter solve was unbiased (rho the least precise of the three).

**Args:**

- <u>maturities (np.ndarray):</u> time to expiry (years) for each currently- listed forward contract.
- <u>volatilities (np.ndarray):</u> each contract's own recent annualized realized volatility (std of daily log returns * sqrt(252) or equivalent), same length/order as `maturities`. At least 3 required to identify 3 unknowns.
- <u>kappa (float):</u> chi's mean-reversion speed, from `fit_schwartz_smith_process`'s spot-based fit.

**Returns:**

<u>tuple[float, float, float]:</u> (sigma_chi, sigma_xi, rho).

**Raises:**

- <u>ValueError:</u> if fewer than 3 maturities are supplied.

**References:**

- Schwartz, E., Smith, J.E. (2000). "Short-Term Variations and Long-Term Dynamics in Commodity Prices." Management Science, 46(7), 893-911. <https://doi.org/10.1287/mnsc.46.7.893.12034>

### fit_schwartz_smith_risk_neutral

```python
fit_schwartz_smith_risk_neutral(
    maturities: np.ndarray,
    forward_prices: np.ndarray,
    chi_0: float,
    xi_0: float,
    kappa: float,
    sigma_chi: float,
    sigma_xi: float,
    rho: float,
) -> SchwartzSmithParams
```

Calibrate the risk-neutral (Q-measure) leg of a Schwartz & Smith (2000) two-factor model against today's
forward curve. kappa, sigma_chi, sigma_xi and rho do not change with the measure, so they come from the
real-world fit; only the short-term risk premium lambda_chi and the risk-adjusted drift mu*_xi are fit here.
The paper's futures price (eq. 9) is linear in those two, so ordinary least squares over the listed
maturities recovers them.

The formula is as follows:

$$
d\chi_{t} = (- \kappa \cdot \chi_{t} - \lambda_{\chi}) \cdot \text{dt} + \sigma_{\chi} \cdot \text{dW}_{t} ^{\chi} \cdot
$$

$$
d\xi_{t} = \mu \cdot \text{\_xi} \cdot \text{dt} + \sigma_{\xi} \cdot \text{dW}_{t} ^{\xi} \cdot
$$

$$
\text{ln}\; F (0,\; T) = \exp(- \kappa \cdot T) \cdot \chi_{0} + \xi_{0} + A(T)
$$

$$
A(T) = - (1 - \exp(- \kappa \cdot T)) / \kappa \cdot \lambda_{\chi} + \mu \cdot \text{\_xi} \cdot T + (V_{\chi} + V_{\xi} + 2 \cdot \text{V\_cross}) / 2
$$

$$
V_{\chi} = \sigma_{\chi} ^{2} \cdot (1 - \exp(- 2 \cdot \kappa \cdot T)) / (2 \cdot \kappa),\;\; V_{\xi} = \sigma_{\xi} ^{2} \cdot T
$$

$$
\text{V\_cross} = \rho \cdot \sigma_{\chi} \cdot \sigma_{\xi} \cdot (1 - \exp(- \kappa \cdot T)) / \kappa
$$

Where chi under Q is an OU process reverting to -lambda_chi / kappa and * marks risk-neutral quantities.

**Args:**

- <u>maturities (np.ndarray):</u> time to expiry (years) for each traded forward contract, e.g. from `get_commodity_forward_curve`'s column labels.
- <u>forward_prices (np.ndarray):</u> the matching observed forward price for each maturity, same length/order as `maturities`, all > 0.
- <u>chi_0 (float):</u> today's short-term deviation, from decomposing today's spot price the same way `fit_schwartz_smith_process` decomposed history (its returned `chi.initial_value`).
- <u>xi_0 (float):</u> today's long-term equilibrium log-price (`xi.initial_value`).
- <u>kappa (float):</u> chi's mean-reversion speed, from the real-world fit.
- <u>sigma_chi (float):</u> chi's volatility, from the real-world fit.
- <u>sigma_xi (float):</u> xi's volatility, from the real-world fit.
- <u>rho (float):</u> correlation between chi's and xi's shocks, from the real-world fit (`fit_schwartz_smith_process`'s second return value).

**Returns:**

<u>SchwartzSmithParams:</u> chi (OUParams, long_run_mean=-lambda_chi/kappa) and xi (RandomWalkParams, drift=mu*_xi) under the risk-neutral measure; same mean_reversion_speed/volatility as the real-world fit, only the drift/long-run-mean terms differ.

**Raises:**

- <u>ValueError:</u> if fewer than 2 maturities are supplied (the regression needs at least 2 observations to identify 2 unknowns), or any forward price is not strictly positive.

**References:**

- Schwartz, E., Smith, J.E. (2000). "Short-Term Variations and Long-Term Dynamics in Commodity Prices." Management Science, 46(7), 893-911. <https://doi.org/10.1287/mnsc.46.7.893.12034>
