---
title: "FX"
seo_title: "FX Reference – Finance Scenarios"
excerpt: "Exchange rates, one per currency against the US dollar."
description: "Exchange rates, one per currency against the US dollar."
author_profile: false
permalink: /projects/financescenarios/docs/reference/fx
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

Exchange rates, one per currency against the US dollar.

```python
from financescenarios.factors.fx.fx_controller import FX
```

Simulate exchange rates: how many units of a foreign currency one US dollar buys, such as euros, yen or pounds per
dollar, for valuing foreign assets and liabilities or reporting in another currency.

Each currency pair is correlated with the other factors, so a scenario where US equities fall can also be one
where the dollar strengthens, as it tends to in a flight to safety. FX is opt-in: `fx` is empty by default.

The model is a geometric Brownian motion (GBM): a random walk in the logarithm of the rate, so the rate can rise or
fall without limit but never turns negative,

```text
d(log S) = (mu - 0.5 * sigma^2) dt + sigma * dW
```

with `mu` the annual drift and `sigma` the annual volatility. An exchange rate has no natural long-run level to return
to, so shocks are permanent and the range of outcomes keeps widening with the horizon; this random walk is the
standard treatment, surveyed in
[Gorvett (2001)](https://www.casact.org/sites/default/files/database/dpp_dpp01_01dpp19.pdf). The trend is the
assumption that matters most over long horizons, so it has three options:

- `drift_mode: irp`: the drift at every step is the gap between two simulated short rates, foreign minus US (uncovered
  interest rate parity: the higher-rate currency is expected to weaken by about the rate gap).
- `drift_mode: random_walk`: no trend, so the median rate stays at today's level
  ([Meese and Rogoff, 1983](https://doi.org/10.1016/0022-1996(83)90017-X)).
- `measure: risk_neutral`: a fixed drift from today's two interest rates, for pricing; see `calibrate_risk_neutral`.
- `source: gmdb`: the Global Macro Database instead of the OECD, for countries such as Brazil, India or China, yearly
  only.

The data are OECD (or Global Macro Database) exchange rates in national currency per US dollar, with no API key
needed. The OECD series is keyed by currency area: use `EA20` for the euro area, as `Germany` has no exchange
rate of its own there. Volatility is always historical, as there is no FX options data.

Configuration (`fx[i]` in a factor set):

| Key | Default | Meaning |
|:----|:--------|:--------|
| `name` | `fx` | The name in the simulated output; unique across the list. |
| `country` | `EA20` | The country or currency area paired against the US dollar. |
| `currency` | `null` | The quoted currency (e.g. `EUR`) for reporting; else from a same-country rate or `EA20`. |
| `source` | `oecd` | `oecd` or `gmdb` (`period: yearly` only). |
| `period` | `monthly` | `monthly`, `quarterly` or `yearly`. |
| `measure` | `real_world` | `real_world` or `risk_neutral`. |
| `drift_mode` | `historical` | `historical`, `irp` or `random_walk`. |
| `domestic_rate_name` | `null` | With `drift_mode: irp`, required: the `interest_rates[i].name` of the US rate. |
| `foreign_rate_name` | `null` | With `drift_mode: irp`: the foreign rate; defaults to `<country>_short_rate`. |
| `beliefs.drift`, `beliefs.volatility` | `null` | Your own annual drift or volatility (volatility above 0). |

`beliefs.drift` cannot be combined with `drift_mode: irp`, and no belief with `measure: risk_neutral`. In a regime
YAML, address one entry with a dotted `"fx.<name>"` key.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
FX(toolkit: Toolkit)
```

</details>

## calibrate

Calibrate one currency pair from its history: fetch the US dollar exchange rate against `country`'s currency and
fit its annual drift and volatility.

A volatility of 0.06 means a typical year moves the rate by about 6% either way; a drift near 0 means no built-in
tendency for the dollar to strengthen or weaken. Both are annualized from the historical log-returns, so the
fitted drift carries the sample's own dollar cycle forward; over decades that can dominate a foreign
portfolio's result, which is why the trend is a choice.

`drift_mode` sets the trend: `"historical"` fits it, `"random_walk"` drops it (the median rate stays at today's
level), and `"irp"` replaces it each step with the gap between two simulated short rates, foreign minus US
(uncovered interest rate parity: the higher-rate currency is expected to weaken by the rate gap), named in a
factor set by `domestic_rate_name` and `foreign_rate_name`. As the rate is in foreign currency per dollar, a
higher US rate pulls it down.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.fx.fx_controller import FX

toolkit = Toolkit(["AAPL"])
fx = FX(toolkit)

fx.calibrate("eur", country="EA20", period="monthly")
fx.calibrate("jpy", country="Japan", period="monthly")
fx.calibrate("brl", country="Brazil", period="yearly", source="gmdb")
```

Which returns (calibrated on 2026-10-04):

| name | drift | volatility | initial_value |
|:-----|------:|-----------:|--------------:|
| eur | 0.0019 | 0.0593 | 0.8625 |
| jpy | 0.0740 | 0.0867 | 158.7871 |
| brl | -0.0145 | 0.0624 | 5.0517 |

A dollar buys 0.86 euros, 158.79 yen and 5.05 reais today; the yen's 7.4% drift reflects the dollar's strong run
against it over the Toolkit's default five-year window.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate(
    name: str,
    country: str = 'EA20',
    period: str = 'monthly',
    source: str = 'oecd',
    drift_mode: str = 'historical',
) -> FXParams
```

**Args:**

- <u>name (str):</u> the pair's name in the simulation and in `params()`/`changes()`, e.g. "eur".
- <u>country (str):</u> the country or currency area paired against the dollar. Defaults to "EA20", the euro area.
- <u>period (str):</u> the data frequency: "monthly", "quarterly" or "yearly" ("yearly" only with `source="gmdb"`). Defaults to "monthly".
- <u>source (str):</u> "oecd" or "gmdb" (Global Macro Database, for non-OECD countries). Defaults to "oecd".
- <u>drift_mode (str):</u> "historical", "random_walk" or "irp", as above. Defaults to "historical".

**Returns:**

<u>FXParams:</u> `drift`, `volatility` and `initial_value` (the last rate, in foreign currency per US dollar).

**Raises:**

- <u>ValueError:</u> if an argument is not recognized, no exchange rate comes back for `country` (such as "Germany" instead of "EA20", or a rate-limited OECD request), or the history has fewer than 3 rates or one at or below zero.

</details>

## calibrate_risk_neutral

Calibrate one currency pair for pricing: the drift comes from today's two interest rates (covered interest rate
parity) and the volatility from history.

A risk-neutral run asks which drift is consistent with today's market prices, so anything priced off the simulated
rate allows no riskless profit (an arbitrage). For a currency pair the two interest rates fix that drift: holding
the higher-rate currency earns more interest, so its forward price must be lower. The drift is
`foreign_rate - domestic_rate`: with a 4.25% US rate and a 2% euro rate, the euros-per-dollar quote drifts down
about 2.25% a year.

The drift is fixed at today's rate gap, unlike `drift_mode="irp"`, which follows the simulated rates. In a
factor set this is `measure: risk_neutral`, which takes today's levels of the configured United States interest
rate and the interest rate for `country`; both must be configured.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.fx.fx_controller import FX

toolkit = Toolkit(["AAPL"])
fx = FX(toolkit)

fx.calibrate_risk_neutral("eur_q", domestic_rate=0.0425, foreign_rate=0.0200, country="EA20")
```

Which returns (calibrated on 2026-10-04):

| name | drift | volatility | initial_value |
|:-----|------:|-----------:|--------------:|
| eur_q | -0.0225 | 0.0593 | 0.8625 |

The drift is 2.00% - 4.25% = -2.25% a year; volatility and today's rate match `calibrate("eur", ...)`.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate_risk_neutral(
    name: str,
    domestic_rate: float,
    foreign_rate: float,
    volatility_source: str = 'historical',
    country: str = 'EA20',
    period: str = 'monthly',
    source: str = 'oecd',
) -> FXParams
```

**Args:**

- <u>name (str):</u> the pair's name in the simulation and in `params()`/`changes()`.
- <u>domestic_rate (float):</u> today's US short rate, annual, as a decimal (0.0425 is 4.25%).
- <u>foreign_rate (float):</u> today's short rate for `country`, annual, as a decimal.
- <u>volatility_source (str):</u> only "historical", as there is no FX options data. Defaults to "historical".
- <u>country (str):</u> the country or currency area, as in `calibrate()`. Defaults to "EA20".
- <u>period (str):</u> the data frequency, as in `calibrate()`. Defaults to "monthly".
- <u>source (str):</u> "oecd" or "gmdb", as in `calibrate()`. Defaults to "oecd".

**Returns:**

<u>FXParams:</u> `drift` (foreign_rate - domestic_rate), with `volatility` and `initial_value` as in `calibrate()`.

**Raises:**

- <u>ValueError:</u> if `volatility_source`, `period` or `source` is not recognized, a rate is not a finite number, or no exchange rate comes back for `country`.

</details>

## names

The names of every currency pair calibrated so far, in calibration order.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
fx.names  # property -> list[str]
```

</details>

## params

The calibrated drift, volatility and starting rate for one currency pair.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
params(name: str) -> FXParams
```

**Args:**

- <u>name (str):</u> the pair's name, as passed to `calibrate()` or `calibrate_risk_neutral()`.

**Raises:**

- <u>RuntimeError:</u> if neither has been called for `name` yet.

</details>

## step_function

The one-step exchange rate update for a fixed-drift currency pair: geometric Brownian motion.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
fx.step_function  # property
```

</details>

## changes

The dated period log-changes of one currency pair's exchange rate: the history its correlations with the other
factors are estimated from.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
changes(name: str) -> pl.DataFrame
```

**Args:**

- <u>name (str):</u> the pair's name, as passed to `calibrate()` or `calibrate_risk_neutral()`.

**Returns:**

<u>pl.DataFrame:</u> two columns, `date` and `value`.

**Raises:**

- <u>RuntimeError:</u> if neither has been called for `name` yet.

</details>

## How It Is Calculated

The model functions behind this page, each with the formula it implements.

{% raw %}
### fit_fx_process

Estimate an exchange rate's annual drift and volatility from its history, for a geometric Brownian motion.

The model assumes the log exchange rate is a random walk with a constant trend: currencies have no natural
level to return to, so shocks are permanent, the spread of outcomes widens with the square root of the horizon
and the rate can never turn negative
([Gorvett, 2001](https://www.casact.org/sites/default/files/database/dpp_dpp01_01dpp19.pdf)).
The estimates are the mean and standard deviation of the log-returns, annualized. The average log-return is the
median growth of the rate, so half the variance is added back to get the expected growth mu. A drift fitted
on a short window extrapolates that window's trend for decades, which is why `random_walk` and `irp` exist.

The formula is as follows:

$$
r_{t} = \ln(S_{t} / S_{t-1})
$$

$$
\sigma = \operatorname{std}(r_{t}) / \sqrt{\text{dt}}
$$

$$
\mu = \operatorname{mean}(r_{t}) / \text{dt} + \sigma ^{2} / 2
$$

**References:**

- Gorvett, R.W. (2001). "Foreign Exchange Rate Risk: Institutional Issues and Stochastic Modeling." CAS Discussion Paper Program. <https://www.casact.org/sites/default/files/database/dpp_dpp01_01dpp19.pdf>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fit_fx_process(exchange_rate: pl.Series, time_step: float) -> FXParams
```

**Args:**

- <u>exchange_rate (pl.Series):</u> the historical rate in foreign currency per US dollar, evenly spaced, all above 0.
- <u>time_step (float):</u> the time between observations, in years.

**Returns:**

<u>FXParams:</u> the annual drift and volatility, and the latest rate as the starting point.

**Raises:**

- <u>ValueError:</u> if there are fewer than 3 observations or any rate is zero or negative.

</details>
{% endraw %}

{% raw %}
### step_fx_process

Move the exchange rate one step forward under geometric Brownian motion.

Each step multiplies the rate by a lognormal shock, so the rate stays positive, moves are proportional to its
level and the distribution of future rates is skewed: a currency can appreciate further than it can fall.
The step is exact, so the result does not depend on the simulation frequency.

The formula is as follows:

$$
S_{t+dt} = S_{t} \cdot \exp((\mu - \sigma ^{2} / 2) \cdot \text{dt} + \sigma \cdot \sqrt{\text{dt}} \cdot z)
$$

**References:**

- Gorvett, R.W. (2001). "Foreign Exchange Rate Risk: Institutional Issues and Stochastic Modeling." CAS Discussion Paper Program. <https://www.casact.org/sites/default/files/database/dpp_dpp01_01dpp19.pdf>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
step_fx_process(
    current_value: np.ndarray | float,
    shock: np.ndarray | float,
    time_step: float,
    params: FXParams,
) -> np.ndarray
```

**Args:**

- <u>current_value (np.ndarray &#124; float):</u> today's exchange rate.
- <u>shock (np.ndarray &#124; float):</u> a standard normal draw.
- <u>time_step (float):</u> the step length, in years.
- <u>params (FXParams):</u> the calibrated drift and volatility.

**Returns:**

<u>np.ndarray:</u> the exchange rate one step later, always above zero.

</details>
{% endraw %}

### fit_fx_process_random_walk

Estimate an exchange rate process with historical volatility but no trend, so the median rate stays at
today's level.

A drift fitted on five or ten years of data mostly reflects that window's dollar cycle; projecting it for
decades would build a strong currency view into every scenario. Meese and Rogoff
[(1983)](https://doi.org/10.1016/0022-1996(83)90017-X) found a random walk forecasts exchange rates out of
sample at least as well as the structural models of the time, so a trend-free rate is the neutral choice for
long horizons. The scenarios still spread out with the historical volatility.

The formula is as follows:

$$
\mu = \sigma ^{2} / 2,\;\; \text{so}\; d (\text{log}\; S_{t}) = \sigma \cdot \text{dW}_{t}
$$

**References:**

- Meese, R.A. and Rogoff, K. (1983). "Empirical exchange rate models of the seventies: Do they fit out of sample?" Journal of International Economics, 14(1-2), 3-24. <https://doi.org/10.1016/0022-1996(83>)90017-X

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fit_fx_process_random_walk(exchange_rate: pl.Series, time_step: float) -> FXParams
```

**Args:**

- <u>exchange_rate (pl.Series):</u> the historical rate in foreign currency per US dollar, evenly spaced, all above 0.
- <u>time_step (float):</u> the time between observations, in years.

**Returns:**

<u>FXParams:</u> the historical volatility, the latest rate and a drift that leaves the median rate flat.

**Raises:**

- <u>ValueError:</u> if there are fewer than 3 observations or any rate is zero or negative.

</details>

{% raw %}
### step_fx_process_irp

Move the exchange rate one step forward with its trend set by the simulated interest rate gap (uncovered
interest rate parity).

Uncovered interest rate parity says the higher-rate currency is expected to weaken by about the rate gap, so an
investor earns the same expected return in either currency. Tying the trend to the two simulated short rates
makes currencies respond to the rate scenarios: when US rates rise relative to the foreign rate, the dollar
is expected to weaken over the following period, and FX and rates stay consistent in every path. Parity is a
long-run tendency rather than a short-run law (the carry trade profits from its failure), so treat this as a
structural, not a forecasting, choice.

The formula is as follows:

$$
S_{t+dt} = S_{t} \cdot \exp((r_{f},\; t - r_{d},\; t - \sigma ^{2} / 2) \cdot \text{dt} + \sigma \cdot \sqrt{\text{dt}} \cdot z)
$$

Where S is units of foreign currency per US dollar, r_f the foreign and r_d the US short rate: a higher US rate
makes the quote fall, the same direction as the risk-neutral drift.

**References:**

- Gorvett, R.W. (2001). "Foreign Exchange Rate Risk: Institutional Issues and Stochastic Modeling." CAS Discussion Paper Program. <https://www.casact.org/sites/default/files/database/dpp_dpp01_01dpp19.pdf>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
step_fx_process_irp(
    current_value: np.ndarray | float,
    shock: np.ndarray | float,
    time_step: float,
    params: FXParams,
    rate_differential: np.ndarray | float,
) -> np.ndarray
```

**Args:**

- <u>current_value (np.ndarray &#124; float):</u> today's exchange rate.
- <u>shock (np.ndarray &#124; float):</u> a standard normal draw.
- <u>time_step (float):</u> the step length, in years.
- <u>params (FXParams):</u> the calibrated volatility; the fitted drift is not used.
- <u>rate_differential (np.ndarray &#124; float):</u> the simulated foreign short rate minus the US short rate, annual.

**Returns:**

<u>np.ndarray:</u> the exchange rate one step later, always above zero.

</details>
{% endraw %}
