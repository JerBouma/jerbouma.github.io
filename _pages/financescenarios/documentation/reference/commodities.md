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

Commodity futures, one per commodity.

```python
from financescenarios.factors.commodities.commodities_controller import Commodities
```

The Commodities module simulates commodity prices, such as crude oil or gold, as prices that swing widely but are
pulled back toward a normal level over time.

Each entry in `commodities` (an empty list by default) becomes a simulated price path, correlated with the other
factors (oil with inflation and the business cycle, gold often against equities in a sell-off) and usable as a
portfolio holding.

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

The `commodities[i]` keys of a factor set and their defaults are listed on the reference page
[Configuration Classes](https://www.jeroenbouma.com/projects/financescenarios/docs/reference/configuration-classes).

A belief's `long_run_mean` is a log price: for 70 USD, set `log(70)`, about 4.25.

**References:**

- Schwartz, E.S. (1997). "The Stochastic Behavior of Commodity Prices: Implications for Valuation and Hedging." Journal of Finance, 52(3), 923-973. <https://doi.org/10.1111/j.1540-6261.1997.tb02721.x>
- Gibson, R., Schwartz, E.S. (1990). "Stochastic Convenience Yield and the Pricing of Oil Contingent Claims." Journal of Finance, 45(3), 959-976. <https://doi.org/10.1111/j.1540-6261.1990.tb05114.x>
- Schwartz, E., Smith, J.E. (2000). "Short-Term Variations and Long-Term Dynamics in Commodity Prices." Management Science, 46(7), 893-911. <https://doi.org/10.1287/mnsc.46.7.893.12034>

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
Commodities(toolkit: Toolkit)
```

</details>

## calibrate

Calibrate one commodity's single-factor model from its price history.

It fits how fast the log price returns to its normal level (`mean_reversion_speed`), what that level is
(`long_run_mean`) and how much it swings (`volatility`). A speed of 1.37 a year means half of a price spike fades
in about six months (ln 2 / 1.37). `long_run_mean` is a log price, so `exp(long_run_mean)` is the price the
process is pulled toward, while `initial_value` is today's actual price.

The fit regresses each period's change in log price on the previous log price by ordinary least squares, the exact
discrete form of the [Schwartz (1997)](https://doi.org/10.1111/j.1540-6261.1997.tb02721.x) model. A price that
trends rather than settles back, such as gold monthly since 2016, raises an error.

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

Crude oil starts at 91.11 USD and is pulled toward exp(4.2056) = 67.06 USD. A price far above that level falls
on average in the scenarios: in the default factor set on 2026-10-14, Brent (`BZ=F`, daily since July 2007)
started at 106.10 USD against exp(4.3403) = 76.71 USD with a speed of 0.69, so it lost 5.7% a year on average
over five years. The futures market priced a steeper fall that day: WTI for November 2026 at 94.14 USD and for
September 2031 at 61.17 USD.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

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

</details>

## calibrate_schwartz_smith

Calibrate one commodity's two-factor Schwartz and Smith model from its price history and today's futures curve.

The log price is split into a short-term deviation `chi` that fades back to zero and a long-term level `xi` that
drifts as a random walk. It separates a temporary dislocation (a refinery outage) from a lasting change in
production costs. The temporary part halves in ln 2 / `chi.mean_reversion_speed` years and today's price is
`exp(chi.initial_value + xi.initial_value)`.

[Schwartz and Smith (2000)](https://doi.org/10.1287/mnsc.46.7.893.12034) estimate the model from years of futures
prices. Only today's curve is available here, so `xi` is a trailing average of the log price and `chi` the rest,
which sets the speed and today's split. The volatilities and their correlation are fitted to the recent swings of
each listed futures contract. When the curve cannot separate the two parts, `xi`'s volatility comes from the
longest contract, whose volatility tends to it as maturity grows (Schwartz and Smith, section 3.1), and the
rest from the price history, with a warning. Without any futures curve the price history sets all three,
which understates `xi`'s volatility by more than an order of magnitude.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.commodities.commodities_controller import Commodities

toolkit = Toolkit(["CL=F"], start_date="2021-01-01")
commodities = Commodities(toolkit)

commodities.calibrate_schwartz_smith("oil", ticker="CL=F", period="daily")
```

Which returns (calibrated on 2026-10-14):

| factor | mean_reversion_speed | long_run_mean | drift | volatility | initial_value |
|:-------|---------------------:|--------------:|------:|-----------:|--------------:|
| oil_chi | 2.5872 | 0.0000 | | 0.4162 | 0.2508 |
| oil_xi | | | -0.0246 | 0.1984 | 4.2983 |

Today's 94.55 USD price splits into a long-term level of exp(4.2983) = 73.6 USD and a 29% short-term
premium. The long-term volatility of 19.8% a year compares with 14.5% in Schwartz and Smith's own oil fit.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate_schwartz_smith(
    name: str,
    ticker: str = 'CL=F',
    period: str = 'daily',
    contracts: int = 12,
    long_term_window_years: float = 3.0,
) -> SchwartzSmithParams
```

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

</details>

## calibrate_schwartz_smith_risk_neutral

Calibrate one commodity's two-factor Schwartz and Smith model so that it reproduces today's futures prices.

Instead of asking how the price has behaved, this asks what path the futures market prices in (the risk-neutral
view). A curve that slopes down (backwardation) gives the long-term level `xi` a negative drift; one that slopes
up (contango), a positive one. Use it for pricing and hedging, not as a forecast.

The speed and volatilities are fitted as in `calibrate_schwartz_smith`, since they are the same under both views.
Only the two drifts are fitted here, by ordinary least squares on the futures pricing formula of
[Schwartz and Smith (2000)](https://doi.org/10.1287/mnsc.46.7.893.12034) (eq. 9). This needs a futures curve and
raises without one.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.commodities.commodities_controller import Commodities

toolkit = Toolkit(["CL=F"], start_date="2021-01-01")
commodities = Commodities(toolkit)

commodities.calibrate_schwartz_smith_risk_neutral("oil_q", ticker="CL=F", period="daily")
```

Which returns (calibrated on 2026-10-14):

| factor | mean_reversion_speed | long_run_mean | drift | volatility | initial_value |
|:-------|---------------------:|--------------:|------:|-----------:|--------------:|
| oil_q_chi | 2.5872 | 0.2474 | | 0.4162 | 0.2508 |
| oil_q_xi | | | -0.1850 | 0.1984 | 4.2983 |

Only the drifts differ from the real-world fit. The crude curve that day fell from 94.14 USD (November 2026) to
83.02 USD (September 2027), so the market prices the long-term level falling about 18.5% a year, against 2.5% in
the real-world fit.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate_schwartz_smith_risk_neutral(
    name: str,
    ticker: str = 'CL=F',
    period: str = 'daily',
    contracts: int = 12,
    long_term_window_years: float = 3.0,
) -> SchwartzSmithParams
```

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

</details>

## names

The names of every commodity calibrated so far, in calibration order; a two-factor entry is listed as its `_chi`
and `_xi` parts.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
commodities.names  # property -> list[str]
```

</details>

## params

The calibrated parameters of one commodity, or of one `_chi` or `_xi` part of a two-factor entry.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
params(name: str) -> CommodityParams | OUParams | RandomWalkParams | GARCHParams | OUCovariateParams
```

**Args:**

- <u>name (str):</u> the name as calibrated, e.g. "crude_oil" or "oil_chi".

**Raises:**

- <u>RuntimeError:</u> if `name` has not been calibrated yet.

</details>

## step_function

The one-step price update of the single-factor model: the exact mean-reverting step on the log price.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
commodities.step_function  # property
```

</details>

## changes

The dated period-to-period changes in one commodity's log price (or its `_chi` or `_xi` part): the history its
correlations with the other factors are estimated from.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
changes(name: str) -> pl.DataFrame
```

**Args:**

- <u>name (str):</u> the name as calibrated, e.g. "crude_oil" or "oil_chi".

**Returns:**

<u>pl.DataFrame:</u> two columns, `date` and `value`.

**Raises:**

- <u>RuntimeError:</u> if `name` has not been calibrated yet.

</details>

## How It Is Calculated

The model functions behind this page, each with the formula it implements.

### fit_commodity_process

Estimate a commodity's mean-reverting price model from its spot price history, after Schwartz (1997).

A commodity, unlike a stock index, has a natural price level: when the price is high, producers expand supply and
inventories build, and the convenience yield of holding the physical good falls, so the price is pulled back
toward its cost of production and storage. The model lets the log price revert to a long-run level at speed kappa,
which keeps the price positive and makes price spikes temporary. Schwartz (1997), abstract: "The first model is a
simple one-factor model in which the logarithm of the spot price of the commodity is assumed to follow a mean
reverting process", and "The analysis reveals strong mean reversion in the commercial commodity prices." The fit
is a regression of each period's change in log price on the previous level; the slope gives the speed, the
intercept the long-run level and the residuals the volatility, using the exact discrete form of the process so the
time step adds no bias. Schwartz estimates the model from futures prices with "The Kalman filter methodology";
regressing on the spot (front-month) price is a judgement that needs no futures history, and it includes each
month's roll from one contract to the next.

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

A price that trends rather than reverts at the chosen frequency gives no pull to estimate and raises an error.

**References:**

- Schwartz, E.S. (1997). "The Stochastic Behavior of Commodity Prices: Implications for Valuation and Hedging." Journal of Finance, 52(3), 923-973. <https://doi.org/10.1111/j.1540-6261.1997.tb02721.x>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fit_commodity_process(prices: pl.Series, time_step: float) -> CommodityParams
```

**Args:**

- <u>prices (pl.Series):</u> the historical spot price, evenly spaced, all above 0.
- <u>time_step (float):</u> the time between observations, in years.

**Returns:**

<u>CommodityParams:</u> the reversion speed, the long-run log price, the log-price volatility and today's price as the starting point.

**Raises:**

- <u>ValueError:</u> if the history is too short, a price is zero or negative, or the price shows no mean reversion.

</details>

### step_commodity_process

Move a commodity's spot price one step forward under the Schwartz (1997) mean-reverting model.

The log price is pulled toward its long-run level, so a spike above the normal price is expected to fade (a gap
halves in ln(2) / kappa years) while the shock keeps prices volatile. Over long horizons the price settles into a
stable lognormal range around exp(mu), rather than drifting without limit as an equity index does; that makes
commodity scenarios narrower at 30 years than a random walk with the same short-term volatility. The step is exact,
so the result does not depend on the simulation frequency, and the price is always positive.

The formula is as follows:

$$
X_{t+dt} = \mu + (X_{t} - \mu) \cdot \exp(- \kappa \cdot \text{dt}) + \sigma \cdot \sqrt{(1 - \exp(- 2 \cdot \kappa \cdot \text{dt})) / (2 \cdot \kappa)} \cdot z
$$

$$
S_{t+dt} = \exp(X_{t+dt})
$$

**References:**

- Schwartz, E.S. (1997). "The Stochastic Behavior of Commodity Prices: Implications for Valuation and Hedging." Journal of Finance, 52(3), 923-973. <https://doi.org/10.1111/j.1540-6261.1997.tb02721.x>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
step_commodity_process(
    current_value: np.ndarray | float,
    shock: np.ndarray | float,
    time_step: float,
    params: CommodityParams,
) -> np.ndarray
```

**Args:**

- <u>current_value (np.ndarray &#124; float):</u> today's spot price, above 0.
- <u>shock (np.ndarray &#124; float):</u> a standard normal draw.
- <u>time_step (float):</u> the step length, in years.
- <u>params (CommodityParams):</u> the reversion speed, long-run log price and log-price volatility.

**Returns:**

<u>np.ndarray:</u> the spot price one step later, always above zero.

</details>

### fit_schwartz_smith_process

Estimate the Schwartz and Smith (2000) two-factor commodity model from a spot price history.

The model splits the log price into a short-term deviation chi, which fades back to zero, and a long-term level
xi, which drifts as a random walk. That matches how commodity markets behave: a supply outage or a cold winter moves
the front of the futures curve but barely touches the long end, while a change in production technology or demand
shifts the whole curve for good. In the scenarios, short-term shocks fade but long-term uncertainty keeps growing
with the horizon.

The paper estimates both parts from years of futures prices with a Kalman filter. Its section 2 defines them:
"changes in the short-term deviations (χt) represent temporary changes in prices (resulting from, for example,
unusual weather or a supply disruption) that are not expected to persist", while changes in the equilibrium
level "represent fundamental changes that are expected to persist". Without that history, xi is
proxied by a trailing average of the log price and chi by the deviation from it; chi is then fitted as a
mean-reverting process around zero and xi as a random walk with drift.

The formula is as follows:

$$
\xi_{t} = \operatorname{mean}(\text{ln}\; S_{s})
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

The mean runs over the last w observations s up to t, with w = long_term_window_years / dt.

The reversion speed and today's split between the two parts are reliable. The volatilities, their correlation and
the long-term drift are not: averaging smooths the long-term level, so its volatility comes out far too small (0.6%
a year for WTI on 2026-10-14, against 14.5% in Schwartz and Smith's Table 2). When a futures curve is available,
the volatilities and correlation are refitted from the futures contracts instead.

**References:**

- Schwartz, E., Smith, J.E. (2000). "Short-Term Variations and Long-Term Dynamics in Commodity Prices." Management Science, 46(7), 893-911. <https://doi.org/10.1287/mnsc.46.7.893.12034>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fit_schwartz_smith_process(
    prices: pl.Series,
    time_step: float,
    long_term_window_years: float = 3.0,
) -> tuple[SchwartzSmithParams, float, np.ndarray, np.ndarray]
```

**Args:**

- <u>prices (pl.Series):</u> the historical spot price, evenly spaced, all above 0.
- <u>time_step (float):</u> the time between observations, in years.
- <u>long_term_window_years (float):</u> the years of prices averaged into the long-term level. The 3-year default is a judgement: long enough to average out short-term deviations, whose half-life is ln 2 / kappa (about half a year at Schwartz and Smith's kappa of 1.49), short enough to follow the long-term level. Their three-factor note reports a half-life of "approximately 3 years" only for the equilibrium growth rate.

**Returns:**

<u>tuple[SchwartzSmithParams, float, np.ndarray, np.ndarray]:</u> the two fitted parts, the correlation of their shocks, and the history of each part's period changes.

**Raises:**

- <u>ValueError:</u> if the history is shorter than the averaging window, a price is zero or negative, or the short-term part shows no mean reversion.

</details>

### fit_schwartz_smith_diffusion_from_forward_curve

Estimate the volatilities of the short-term and long-term commodity factors, and their correlation, from how much
each futures contract has moved.

In the Schwartz and Smith (2000) model the volatility of a futures contract depends on its maturity: near
contracts carry the full short-term shock, while the short-term part has faded out of distant contracts, leaving
only the long-term volatility. So the term structure of futures volatilities pins down both parts, which the spot
history alone cannot separate. Each contract's own recent volatility is matched to the model, with the reversion
speed taken from the spot fit; the relation is then linear, so one least-squares fit recovers the three values.

The formula is as follows:

$$
\sigma ^{2} (F_{T}) = \exp(- 2 \cdot \kappa \cdot T) \cdot \sigma_{\chi} ^{2} + \sigma_{\xi} ^{2} + 2 \cdot \exp(- \kappa \cdot T) \cdot \rho \cdot \sigma_{\chi} \cdot \sigma_{\xi}
$$

Schwartz and Smith (2000), section 3.1, derive this from their futures price (eq. 9): "The volatility is thus
independent of the state variables. For near maturity futures contracts (i.e., T = 0), the volatility is equal
to the volatility of the sum of the short- and long-term factors." Fixing kappa is a judgement: with the dozen or
so maturities a futures curve has, also fitting kappa overstated it about sevenfold in this package's own
simulation check, while this fit was unbiased. The correlation is the least precise of the three.

**References:**

- Schwartz, E., Smith, J.E. (2000). "Short-Term Variations and Long-Term Dynamics in Commodity Prices." Management Science, 46(7), 893-911. <https://doi.org/10.1287/mnsc.46.7.893.12034>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fit_schwartz_smith_diffusion_from_forward_curve(
    maturities: np.ndarray,
    volatilities: np.ndarray,
    kappa: float,
) -> tuple[float, float, float]
```

**Args:**

- <u>maturities (np.ndarray):</u> each listed futures contract's time to expiry, in years.
- <u>volatilities (np.ndarray):</u> each contract's recent annualized volatility, in the same order; at least 3.
- <u>kappa (float):</u> the short-term part's reversion speed, from the spot fit.

**Returns:**

<u>tuple[float, float, float]:</u> the short-term volatility, the long-term volatility and their correlation.

**Raises:**

- <u>ValueError:</u> if fewer than 3 maturities are supplied.

</details>

### long_term_volatility_from_contract

The long-term factor's volatility implied by one futures contract's volatility, given the short-term factor's
volatility, speed and correlation: the futures volatility formula of Schwartz and Smith (2000) solved for
sigma_xi.

Schwartz and Smith (2000), section 3.1: "as T → ∞, the instantaneous volatility approaches the volatility of the
equilibrium price level (σξ)". The longest listed contract is therefore the one that measures sigma_xi best when
the three-parameter fit to the whole curve cannot separate the two factors. A spot price history alone smooths
the long-term level away: on WTI on 2026-10-14 it gave 0.6% a year against about 20% from the longest contract,
where Schwartz and Smith's own oil estimates are 14.5% (futures data) and 11.5% (Enron data) in Table 2.

The formula is as follows:

$$
\sigma ^{2} (F_{T}) = \exp(- 2 \cdot \kappa \cdot T) \cdot \sigma_{\chi} ^{2} + \sigma_{\xi} ^{2} + 2 \cdot \exp(- \kappa \cdot T) \cdot \rho \cdot \sigma_{\chi} \cdot \sigma_{\xi}
$$

$$
\sigma_{\xi} = - d \cdot \rho \cdot \sigma_{\chi} + \sqrt{\sigma ^{2} (F_{T}) - d ^{2} \cdot \sigma_{\chi} ^{2} \cdot (1 - \rho ^{2})},\;\; d = \exp(- \kappa \cdot T)
$$

Where sigma(F_T) is the contract's volatility; when the root has no positive solution the contract's own
volatility is returned, its value as T grows.

**References:**

- Schwartz, E., Smith, J.E. (2000). "Short-Term Variations and Long-Term Dynamics in Commodity Prices." Management Science, 46(7), 893-911. <https://doi.org/10.1287/mnsc.46.7.893.12034>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
long_term_volatility_from_contract(
    maturity: float,
    contract_volatility: float,
    kappa: float,
    sigma_chi: float,
    rho: float,
) -> float
```

**Args:**

- <u>maturity (float):</u> the contract's time to expiry, in years.
- <u>contract_volatility (float):</u> the contract's recent annualized volatility.
- <u>kappa (float):</u> the short-term factor's reversion speed.
- <u>sigma_chi (float):</u> the short-term factor's volatility.
- <u>rho (float):</u> the correlation of the two factors' shocks.

**Returns:**

<u>float:</u> the long-term factor's annual volatility.

</details>

{% raw %}
### fit_schwartz_smith_risk_neutral

Fit the risk-neutral version of the Schwartz and Smith (2000) model to today's futures curve, for pricing and
hedging.

Under the risk-neutral measure the model must reproduce today's futures prices, so the curve's shape sets the two
drifts. A curve that slopes down (backwardation, typical when inventories are tight and the convenience yield is
high) gives a negative drift; one that slopes up (contango, ample storage) a positive one. The speed, volatilities
and correlation are the same under both measures, so they come from the real-world fit; only the short-term risk
premium lambda_chi and the risk-adjusted long-term drift mu_Q are fitted here. The paper's futures price
(eq. 9) is linear in those two, so ordinary least squares over the listed maturities recovers them.

The formula is as follows:

$$
d\chi_{t} = (- \kappa \cdot \chi_{t} - \lambda_{\chi}) \cdot \text{dt} + \sigma_{\chi} \cdot \text{dW}_{t} ^{\chi}
$$

$$
d\xi_{t} = \mu_{Q} \cdot \text{dt} + \sigma_{\xi} \cdot \text{dW}_{t} ^{\xi}
$$

$$
\text{ln}\; F (0,\; T) = \exp(- \kappa \cdot T) \cdot \chi_{0} + \xi_{0} + A(T)
$$

$$
A(T) = - (1 - \exp(- \kappa \cdot T)) / \kappa \cdot \lambda_{\chi} + \mu_{Q} \cdot T + (V_{\chi} + V_{\xi} + 2 \cdot V_{\text{cross}}) / 2
$$

$$
V_{\chi} = \sigma_{\chi} ^{2} \cdot (1 - \exp(- 2 \cdot \kappa \cdot T)) / (2 \cdot \kappa),\;\; V_{\xi} = \sigma_{\xi} ^{2} \cdot T
$$

$$
V_{\text{cross}} = \rho \cdot \sigma_{\chi} \cdot \sigma_{\xi} \cdot (1 - \exp(- \kappa \cdot T)) / \kappa
$$

Where, under Q, chi is an OU process reverting to -lambda_chi / kappa and xi drifts at mu_Q, and W is the
risk-neutral Brownian motion.

**References:**

- Schwartz, E., Smith, J.E. (2000). "Short-Term Variations and Long-Term Dynamics in Commodity Prices." Management Science, 46(7), 893-911. <https://doi.org/10.1287/mnsc.46.7.893.12034>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

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

**Args:**

- <u>maturities (np.ndarray):</u> each traded futures contract's time to expiry, in years.
- <u>forward_prices (np.ndarray):</u> each contract's price today, in the same order, all above 0.
- <u>chi_0 (float):</u> today's short-term deviation, from the real-world fit.
- <u>xi_0 (float):</u> today's long-term log price, from the real-world fit.
- <u>kappa (float):</u> the short-term part's reversion speed, from the real-world fit.
- <u>sigma_chi (float):</u> the short-term volatility, from the real-world fit.
- <u>sigma_xi (float):</u> the long-term volatility, from the real-world fit.
- <u>rho (float):</u> the correlation of the two parts' shocks, from the real-world fit.

**Returns:**

<u>SchwartzSmithParams:</u> the two parts under the risk-neutral measure, with the real-world speed and volatilities and the drifts implied by today's futures curve.

**Raises:**

- <u>ValueError:</u> if fewer than 2 maturities are supplied or a futures price is zero or negative.

</details>
{% endraw %}
