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

Exchange rates, one per currency against the US dollar. Generated from the docstrings of Finance Scenarios 0.1.0; `help(...)` in Python shows the same text.

```python
from financescenarios.factors.fx.fx_controller import FX
```

```python
FX(toolkit: Toolkit)
```

Simulate exchange rates: how many units of a foreign currency one US dollar buys, such as euros, yen or pounds per
dollar, and how that rate could move over the years ahead.

Each currency pair you add becomes a variable in the scenarios, linked to the rest through the correlation matrix, as
a portfolio with foreign assets or a report in another currency needs. FX is opt-in: `fx` is empty by default.

The model is a geometric Brownian motion (GBM): a random walk in the logarithm of the rate, so the rate can rise or
fall without limit but never turns negative,

```text
d(log S) = (mu - 0.5 * sigma^2) dt + sigma * dW
```

with `mu` the annual drift and `sigma` the annual volatility. An exchange rate has no natural long-run level to return
to, so this random walk is the standard treatment, surveyed in
[Gorvett (2001)](https://www.casact.org/sites/default/files/database/dpp_dpp01_01dpp19.pdf).

Options that change the model:

- `drift_mode: irp`: the drift at every step is the gap between two simulated short rates, foreign minus US (uncovered
  interest rate parity: the higher-rate currency is expected to weaken by about the rate gap).
- `drift_mode: random_walk`: no trend, so the median rate stays at today's level
  ([Meese and Rogoff, 1983](https://doi.org/10.1016/0022-1996(83)90017-X)).
- `measure: risk_neutral`: a fixed drift from today's two interest rates, for pricing; see `calibrate_risk_neutral`.
- `source: gmdb`: the Global Macro Database instead of the OECD, for countries such as Brazil, India or China, yearly
  only.

The data come from the Finance Toolkit's `economics.get_exchange_rates`, in national currency per US dollar, with no
API key needed. The OECD series is keyed by currency area: use `EA20` for the euro area, as `Germany` has no exchange
rate of its own there. The OECD limits bursts of requests; if a fetch comes back empty, wait a minute and retry.
Volatility is always historical, as there is no FX options data.

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

## calibrate

```python
calibrate(
    name: str,
    country: str = 'EA20',
    period: str = 'monthly',
    source: str = 'oecd',
    drift_mode: str = 'historical',
) -> FXParams
```

Calibrate one currency pair from its history: fetch the US dollar exchange rate against `country`'s currency and
fit its annual drift and volatility.

A volatility of 0.06 means a typical year moves the rate by about 6% either way; a drift near 0 means no built-in
tendency for the dollar to strengthen or weaken. Both are annualized from the historical log-returns.

`drift_mode` sets the trend: `"historical"` fits it, `"random_walk"` drops it (the median rate stays at today's
level), and `"irp"` replaces it each step with the gap between two simulated short rates, foreign minus US
(uncovered interest rate parity), named in a factor set by `domestic_rate_name` and `foreign_rate_name`. As the
rate is in foreign currency per dollar, a higher US rate pulls it down.

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

## calibrate_risk_neutral

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

Calibrate one currency pair for pricing: the drift comes from today's two interest rates (covered interest rate
parity) and the volatility from history.

A risk-neutral run asks which drift is consistent with today's market prices, so anything priced off the simulated
rate allows no riskless profit (an arbitrage). For a currency pair the two interest rates fix that drift: holding
the higher-rate currency earns more interest, so its forward price must be lower. The drift is
`foreign_rate - domestic_rate`: with a 4.25% US rate and a 2% euro rate, the euros-per-dollar quote drifts down
about 2.25% a year.

The drift is set once, unlike `drift_mode="irp"`, which follows the simulated rates step by step. In a factor set
this is `measure: risk_neutral`: the run passes today's levels of its United States interest rate and the interest
rate for `country`, and raises when either is not configured.

Also known as: covered interest parity (CIP) drift, risk-neutral FX, Q-measure exchange rate.

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

## names

```python
fx.names  # property -> list[str]
```

The names of every currency pair calibrated so far, in calibration order.

## params

```python
params(name: str) -> FXParams
```

The calibrated drift, volatility and starting rate for one currency pair.

**Args:**

- <u>name (str):</u> the pair's name, as passed to `calibrate()` or `calibrate_risk_neutral()`.

**Raises:**

- <u>RuntimeError:</u> if neither has been called for `name` yet.

## step_function

```python
fx.step_function  # property
```

The geometric Brownian motion step function, stateless and shared by every fixed-drift currency pair.

## changes

```python
changes(name: str) -> pl.DataFrame
```

The dated period log-changes of one currency pair's exchange rate, from the data already fetched during
calibration. The correlation estimate reuses them instead of fetching the data again.

**Args:**

- <u>name (str):</u> the pair's name, as passed to `calibrate()` or `calibrate_risk_neutral()`.

**Returns:**

<u>pl.DataFrame:</u> two columns, `date` and `value`.

**Raises:**

- <u>RuntimeError:</u> if neither has been called for `name` yet.

## How It Is Calculated

The model functions behind this page, each with the formula it implements.

{% raw %}
### fit_fx_process

```python
fit_fx_process(exchange_rate: pl.Series, time_step: float) -> FXParams
```

Fit a GBM process to a historical exchange-rate series with the closed-form estimates of its log-returns. The
mean log-return estimates nu = mu - sigma^2 / 2, so half the variance is added back: step_fx_process subtracts
it again, and storing nu as the drift would subtract it twice.

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

**Args:**

- <u>exchange_rate (pl.Series):</u> historical exchange-rate observations, evenly spaced in time, all > 0.
- <u>time_step (float):</u> time increment between observations, in years.

**Returns:**

<u>FXParams:</u> the calibrated drift, volatility, and the series' last value as the simulation starting point.

**Raises:**

- <u>ValueError:</u> if fewer than 3 observations are supplied, or any observation is not strictly positive.

**References:**

- Gorvett, R.W. (2001). "Foreign Exchange Rate Risk: Institutional Issues and Stochastic Modeling." CAS Discussion Paper Program. <https://www.casact.org/sites/default/files/database/dpp_dpp01_01dpp19.pdf>
{% endraw %}

{% raw %}
### step_fx_process

```python
step_fx_process(
    current_value: np.ndarray | float,
    shock: np.ndarray | float,
    time_step: float,
    params: FXParams,
) -> np.ndarray
```

Advance the exchange rate by one time step with GBM's exact solution, so no discretization error is introduced.

The formula is as follows:

$$
S_{t+dt} = S_{t} \cdot \exp((\mu - \sigma ^{2} / 2) \cdot \text{dt} + \sigma \cdot \sqrt{\text{dt}} \cdot z)
$$

**Args:**

- <u>current_value (np.ndarray &#124; float):</u> the exchange rate at the current time step.
- <u>shock (np.ndarray &#124; float):</u> a standard normal draw for this step.
- <u>time_step (float):</u> the time increment, in years.
- <u>params (FXParams):</u> calibrated drift and volatility.

**Returns:**

<u>np.ndarray:</u> the exchange rate at the next time step. Always strictly positive.

**References:**

- Gorvett, R.W. (2001). "Foreign Exchange Rate Risk: Institutional Issues and Stochastic Modeling." CAS Discussion Paper Program. <https://www.casact.org/sites/default/files/database/dpp_dpp01_01dpp19.pdf>
{% endraw %}

### fit_fx_process_random_walk

```python
fit_fx_process_random_walk(exchange_rate: pl.Series, time_step: float) -> FXParams
```

Fit an FX process for drift_mode="random_walk": the historical volatility, but no trend, so the median
exchange rate stays where it is today instead of extrapolating the sample's own appreciation or
depreciation for decades. Meese and Rogoff [(1983)](https://doi.org/10.1016/0022-1996(83)90017-X) found a
random walk forecasts exchange rates out of sample at least as well as the structural models of the time.

The formula is as follows:

$$
\mu = \sigma ^{2} / 2,\;\; \text{so}\; d (\text{log}\; S_{t}) = \sigma \cdot \text{dW}_{t}
$$

**Args:**

- <u>exchange_rate (pl.Series):</u> historical exchange-rate observations, evenly spaced in time, all > 0.
- <u>time_step (float):</u> time increment between observations, in years.

**Returns:**

<u>FXParams:</u> volatility and initial_value as fit_fx_process() computes them, with a trend-free drift.

**Raises:**

- <u>ValueError:</u> if fewer than 3 observations are supplied, or any observation is not strictly positive.

**References:**

- Meese, R.A. and Rogoff, K. (1983). "Empirical exchange rate models of the seventies: Do they fit out of sample?" Journal of International Economics, 14(1-2), 3-24. <https://doi.org/10.1016/0022-1996(83>)90017-X

{% raw %}
### step_fx_process_irp

```python
step_fx_process_irp(
    current_value: np.ndarray | float,
    shock: np.ndarray | float,
    time_step: float,
    params: FXParams,
    rate_differential: np.ndarray | float,
) -> np.ndarray
```

Advance the exchange rate by one time step under drift_mode="irp": step_fx_process's exact GBM step with the
drift replaced by this step's simulated foreign-minus-domestic short-rate differential (uncovered interest
rate parity: the higher-rate currency is expected to depreciate by the rate differential).

The formula is as follows:

$$
S_{t+dt} = S_{t} \cdot \exp((r_{f},\; t - r_{d},\; t - \sigma ^{2} / 2) \cdot \text{dt} + \sigma \cdot \sqrt{\text{dt}} \cdot z)
$$

Where S is units of foreign currency per USD (the OECD quote, so domestic = USD), r_f the foreign and r_d the
USD short rate: a higher USD rate makes the quote fall, the same sign as calibrate_risk_neutral's static drift.

**Args:**

- <u>current_value (np.ndarray &#124; float):</u> the exchange rate at the current time step.
- <u>shock (np.ndarray &#124; float):</u> a standard normal draw for this step.
- <u>time_step (float):</u> the time increment, in years.
- <u>params (FXParams):</u> calibrated volatility (params.drift is ignored; replacing it every step is this step function's entire purpose).
- <u>rate_differential (np.ndarray &#124; float):</u> foreign short rate minus domestic short rate, this step's already-simulated values (not their annualized fit) for the two rate factors driving this FX pair.

**Returns:**

<u>np.ndarray:</u> the exchange rate at the next time step. Always strictly positive.

**References:**

- Gorvett, R.W. (2001). "Foreign Exchange Rate Risk: Institutional Issues and Stochastic Modeling." CAS Discussion Paper Program. <https://www.casact.org/sites/default/files/database/dpp_dpp01_01dpp19.pdf>
{% endraw %}
