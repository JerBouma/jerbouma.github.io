---
title: "Equities"
seo_title: "Equities Reference – Finance Scenarios"
excerpt: "Equity indices, sectors, regions and styles with regime switching."
description: "Equity indices, sectors, regions and styles with regime switching."
author_profile: false
permalink: /projects/financescenarios/docs/reference/equities
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

Equity indices, sectors, regions and styles with regime switching. Generated from the docstrings of Finance Scenarios 0.1.0; `help(...)` in Python shows the same text.

```python
from financescenarios.factors.equities.equities_controller import Equities
```

```python
Equities(toolkit: Toolkit)
```

Simulate equity prices: a broad stock index, a sector, a region or an investment style, each tracked through one
ticker such as SPY or an ETF.

Stock markets alternate between calm stretches of steady gains and turbulent stretches of losses and large swings, and
this module captures that switching. Every run has at least one equity (by default `SPY`, named `equity`); add as many
as you like, such as technology or Europe. Each becomes its own variable in the scenarios, linked to the rest through
the correlation matrix.

The model is the regime-switching lognormal model of [Hardy (2001)](https://doi.org/10.1080/10920277.2001.10595984):
the market is always in one of a few regimes, by default a calm and a turbulent one, each with its own mean and
volatility of log-returns (the logarithm of each period's price change). It switches regime at random with fitted
probabilities (a Markov chain), each equity on its own regime path.

The options:

- `method`: `regime_switching` (the default); `hibbert_regime_switching`, the same model on the return above a short
  interest rate (Hibbert, Mowbray and Turnbull
  [(2001)](https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf));
  `wilkie_derived`, the price as dividends divided by the dividend yield (Wilkie
  [(1986)](https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf));
  or `knw_sv`, the equity leg of the Koijen, Nijman and Werker model, fitted together with its interest rate.
- `condition_on_business_cycle`: turbulence becomes more likely when the leading indicator signals a downturn
  ([Filardo, 1994](https://doi.org/10.1080/07350015.1994.10524545)).
- `measure: risk_neutral`: one volatility and a drift of the risk-free rate minus the dividend yield, for pricing
  rather than forecasting ([Black and Scholes, 1973](https://doi.org/10.1086/260062)), or a volatility that moves with
  `volatility_source: heston` ([Heston, 1993](https://doi.org/10.1093/rfs/6.2.327)).
- `beliefs`: your own regime means and volatilities instead of the fitted ones.

Prices are each ticker's adjusted closes from the Finance Toolkit (Yahoo Finance, or Financial Modeling Prep with a
`FINANCIAL_MODELING_PREP_API_KEY`); any ticker worldwide works, given at least `n_regimes * 5` of them. Pass
`benchmark_ticker=None` when you build a `Toolkit` yourself.

Configuration (`equities[i]` in a factor set):

| Key | Default | Meaning |
|:----|:--------|:--------|
| `name` | `equity` | The name in the output; unique across the list. |
| `ticker` | `SPY` | Any ticker: an index, sector, regional or style ETF. |
| `asset_class` | `null` | A private-market class (e.g. `Private Equity`); sets `ticker` to its listed proxy. |
| `n_regimes` | `2` | Number of regimes, at least 2. |
| `period` | `monthly` | Price frequency, `daily` to `yearly`. |
| `nominal_rate_name` | `null` | The paired `interest_rates[i].name`; `hibbert_regime_switching` and `knw_sv`. |
| `dividend_growth_name`, `dividend_yield_name` | `null` | The paired dividend entries; `wilkie_derived` only. |
| `condition_on_business_cycle` | `false` | Needs `leading_indicator.enabled: true`; `regime_switching` only. |
| `measure` | `real_world` | `real_world` or `risk_neutral` (with `regime_switching` only). |
| `volatility_source` | `implied` | `implied`, `svi`, `heston` or `realized`; `risk_neutral` only. |
| `history_source` | `null` | `shiller` or `jst`: fit the regimes on history since the 1870s. |
| `beliefs.regime_means`, `beliefs.regime_volatilities` | `null` | Annual values, one per regime. |

Beliefs cannot be combined with `measure: risk_neutral` or `wilkie_derived`; in a regime YAML, address one entry as
`"equities.<name>"`.

## calibrate

```python
calibrate(name: str, ticker: str, n_regimes: int = 2, period: str = 'monthly') -> RegimeParams
```

Calibrate one equity from its price history: the mean and volatility of its log-return in each regime, and the
chance of moving between regimes each period.

This learns from the past how a market alternates between calm and turbulent stretches, so the scenarios switch
the same way. The diagonal of the transition matrix is the chance of staying in a regime one more period, so the
expected stay is 1 / (1 - that chance): a 0.90 monthly chance of staying calm means calm stretches last about ten
months. Regime 0 is always the one with the lowest mean return.

The regimes are never observed, only the returns, so the fit is the Baum-Welch expectation-maximization algorithm
for hidden Markov models ([Baum et al., 1970](https://doi.org/10.1214/aoms/1177697196)). Means and volatilities
are annual; the transition matrix is per period of the data.

Also known as: regime-switching lognormal (RSLN), hidden Markov model of equity returns.

**Args:**

- <u>name (str):</u> the equity's name in the simulation and in `params()`/`changes()`, e.g. "us_broad".
- <u>ticker (str):</u> the ticker to fit, such as "SPY" or a sector, regional or style ETF.
- <u>n_regimes (int):</u> the number of regimes, at least 2. Defaults to 2 (calm and turbulent, as in Hardy 2001).
- <u>period (str):</u> the price frequency: "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "monthly".

**Returns:**

<u>RegimeParams:</u> `regime_means`, `regime_volatilities`, `transition_matrix`, `stationary_distribution` (long-run share of time per regime), `initial_regime` and `initial_value` (the last price).

**Raises:**

- <u>ValueError:</u> if `period`, `n_regimes` or `ticker` is invalid, there are fewer than `n_regimes * 5` prices, or a regime ends up with almost no observations.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.equities.equities_controller import Equities

toolkit = Toolkit(["SPY"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2005-01-01", benchmark_ticker=None)
equities = Equities(toolkit)

equities.calibrate("us_broad", "SPY", period="monthly")
```

Which returns (calibrated on 2026-10-04):

| regime | regime_mean | regime_volatility | chance of staying | long-run share |
|-------:|------------:|------------------:|------------------:|---------------:|
| 0 | -0.0009 | 0.2020 | 0.8715 | 0.4377 |
| 1 | 0.1853 | 0.0793 | 0.9000 | 0.5623 |

The S&P 500's turbulent regime has a flat average return at 20% volatility, its calm one 18.5% a year at 8%.

## calibrate_tvtp

```python
calibrate_tvtp(
    name: str,
    ticker: str,
    business_cycle_covariate: pl.Series,
    business_cycle_covariate_dates: pl.Series,
    n_regimes: int = 2,
    period: str = 'monthly',
) -> RegimeParams
```

Calibrate one equity whose regime switching follows the business cycle: `calibrate()`'s fit plus a regression that
ties the chance of switching regime to the leading indicator.

With `calibrate()` the chance of a calm market turning turbulent is the same every month. Here it rises when the
leading indicator (the OECD Composite Leading Indicator, around 100 in a normal economy) signals a downturn, so
turbulent stretches cluster around weak economies. This is the time-varying transition probability (TVTP) model of
[Filardo (1994)](https://doi.org/10.1080/07350015.1994.10524545), estimated in the simpler two-step way of
[Diebold, Lee and Weinbach (1994)](https://doi.org/10.1093/oso/9780198773917.003.0010): first the regimes, then a
logit regression of which regime came next on the indicator's level.

In a factor set this is `condition_on_business_cycle: true`, which needs `leading_indicator.enabled: true`.

**Args:**

- <u>name (str):</u> the equity's name in the simulation and in `params()`/`changes()`.
- <u>ticker (str):</u> the ticker to fit, as in `calibrate()`.
- <u>business_cycle_covariate (pl.Series):</u> the leading indicator's historical levels, e.g. `LeadingIndicator.series`.
- <u>business_cycle_covariate_dates (pl.Series):</u> the dates of those levels, e.g. `LeadingIndicator.dates`.
- <u>n_regimes (int):</u> the number of regimes, at least 2. Defaults to 2.
- <u>period (str):</u> the price frequency, as in `calibrate()`. Defaults to "monthly".

**Returns:**

<u>RegimeParams:</u> the regime fit, with `tvtp` holding `baseline_log_odds` and `covariate_sensitivity`, one row per starting regime.

**Raises:**

- <u>ValueError:</u> if `period`, `n_regimes` or `ticker` is invalid, too few prices line up with the indicator by date, or a regime has too few observed transitions to fit.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.equities.equities_controller import Equities
from financescenarios.factors.leading_indicator.leading_indicator_controller import LeadingIndicator

toolkit = Toolkit(["SPY"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2005-01-01", benchmark_ticker=None)
leading_indicator = LeadingIndicator(toolkit)
leading_indicator.calibrate(country="United States", period="monthly")

equities = Equities(toolkit)
params = equities.calibrate_tvtp(
    "us_broad", "SPY", leading_indicator.series, leading_indicator.dates, period="monthly"
)
```

Which returns (calibrated on 2026-10-04):

| regime | regime_mean | regime_volatility | baseline_log_odds | covariate_sensitivity |
|-------:|------------:|------------------:|:------------------|:----------------------|
| 0 | -0.0016 | 0.2020 | [0.0, -1.0835] | [0.0, -0.0106] |
| 1 | 0.1876 | 0.0798 | [0.0, -1.9354] | [0.0, 0.0449] |

In the calm regime (row 1) the chance of turning turbulent is 5.8% a month at a leading indicator of 105 and 8.9%
at 95, so a weakening economy shortens calm stretches from about 17 to 11 months.

## calibrate_hibbert_regime_switching

```python
calibrate_hibbert_regime_switching(
    name: str,
    ticker: str,
    risk_free_rate: pl.Series,
    n_regimes: int = 2,
    period: str = 'monthly',
) -> RegimeParams
```

Calibrate one equity on its return above a short interest rate, as in the Barrie & Hibbert model of Hibbert,
Mowbray and Turnbull
[(2001)](https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf).

The fit is the same as in `calibrate()`, but on the extra return stocks earn over cash (the equity risk premium):
each period's log-return minus the short rate times the period length. When simulating, the paired interest rate's
simulated level is added back each step, so higher rates mean higher expected equity returns, while the premium on
top keeps its own calm and turbulent regimes.

In a factor set this is `method: hibbert_regime_switching`, with `nominal_rate_name` naming the interest rate; it
has no risk-neutral version.

**Args:**

- <u>name (str):</u> the equity's name in the simulation and in `params()`/`changes()`.
- <u>ticker (str):</u> the ticker to fit, as in `calibrate()`.
- <u>risk_free_rate (pl.Series):</u> the paired interest rate's historical levels (annual, as decimals), e.g. `InterestRates.series(name)`, sampled at the same `period` as the prices.
- <u>n_regimes (int):</u> the number of regimes, at least 2. Defaults to 2.
- <u>period (str):</u> the price frequency, as in `calibrate()`. Defaults to "monthly".

**Returns:**

<u>RegimeParams:</u> the regime fit, with `regime_means` as annual returns above the short rate.

**Raises:**

- <u>ValueError:</u> if `period`, `n_regimes` or `ticker` is invalid, there are fewer than `n_regimes * 5` prices, or a regime ends up with almost no observations.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.equities.equities_controller import Equities
from financescenarios.factors.interest_rates.interest_rates_controller import InterestRates

toolkit = Toolkit(
    ["SPY", "^IRX"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2005-01-01", benchmark_ticker=None
)
rates = InterestRates(toolkit)
rates.calibrate("us_short_rate", ticker="^IRX", period="monthly")

equities = Equities(toolkit)
equities.calibrate_hibbert_regime_switching(
    "us_premium", "SPY", rates.series("us_short_rate"), period="monthly"
)
```

Which returns (calibrated on 2026-10-04):

| regime | regime_mean | regime_volatility | chance of staying | long-run share |
|-------:|------------:|------------------:|------------------:|---------------:|
| 0 | -0.0149 | 0.2016 | 0.8735 | 0.4389 |
| 1 | 0.1651 | 0.0799 | 0.9010 | 0.5611 |

Against the 13-week Treasury bill, the S&P 500's calm regime earns 16.5% a year above cash and its turbulent
regime 1.5% below it.

## calibrate_risk_neutral

```python
calibrate_risk_neutral(
    name: str,
    ticker: str,
    risk_free_rate: float,
    dividend_yield: float,
    volatility_source: str = 'implied',
    expiration_date: str | None = None,
    period: str = 'monthly',
) -> FXParams
```

Calibrate one equity for pricing rather than forecasting: a constant volatility and a drift of the risk-free rate
minus the dividend yield, as in Black and Scholes [(1973)](https://doi.org/10.1086/260062) and Merton
[(1973)](https://doi.org/10.2307/3003143).

`calibrate()` forecasts how the market will behave; this matches today's market prices instead, so an option
valued on the simulated paths allows no riskless profit (an arbitrage). The price follows
`d(log S) = (r - q - 0.5 * sigma^2) dt + sigma dW`, with `r` the risk-free rate, `q` the dividend yield and
`sigma` the volatility; the result is an `FXParams`, as for FX.

`volatility_source` picks `sigma`:

- `"implied"`: the options market's volatility at the strike nearest today's price, at one expiration.
- `"svi"`: the at-the-money point of the Finance Toolkit's smoothed volatility surface
  ([Gatheral and Jacquier, 2014](https://doi.org/10.1080/14697688.2013.819986)), longest expiration.
- `"realized"`: the ticker's own historical volatility, for tickers without liquid options.

The first two fall back to `"realized"`, with a warning, without options data; `calibrate_heston` lets the
volatility itself move.

**Args:**

- <u>name (str):</u> the equity's name in the simulation and in `params()`/`changes()`.
- <u>ticker (str):</u> the ticker, such as "SPY".
- <u>risk_free_rate (float):</u> today's annual risk-free rate, as a decimal (0.04 is 4%).
- <u>dividend_yield (float):</u> today's annual dividend yield, as a decimal.
- <u>volatility_source (str):</u> "implied", "svi" or "realized". Defaults to "implied".
- <u>expiration_date (str &#124; None):</u> the option expiration for "implied". Defaults to None, the first one at least a week away.
- <u>period (str):</u> the price frequency, as in `calibrate()`. Defaults to "monthly".

**Returns:**

<u>FXParams:</u> `drift` (risk-free rate minus dividend yield), `volatility` and `initial_value` (today's price).

**Raises:**

- <u>ValueError:</u> if `volatility_source` or `period` is not recognized, or a rate is not a finite number.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.equities.equities_controller import Equities

toolkit = Toolkit(["SPY"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2005-01-01", benchmark_ticker=None)
equities = Equities(toolkit)

runs = [("implied", "2026-12-18"), ("svi", None), ("realized", None)]
for source, expiration in runs:
    equities.calibrate_risk_neutral(
        f"spy_{source}_{expiration}", "SPY", risk_free_rate=0.0399, dividend_yield=0.0115,
        volatility_source=source, expiration_date=expiration,
    )
```

Which returns (calibrated on 2026-10-04):

| volatility_source | drift | volatility |
|:------------------|------:|-----------:|
| implied | 0.0284 | 0.1426 |
| svi | 0.0284 | 0.1349 |
| realized | 0.0284 | 0.1486 |

## calibrate_derived

```python
calibrate_derived(
    name: str,
    dividend_growth_changes: pl.DataFrame,
    dividend_growth_initial_value: float,
    dividend_yield_changes: pl.DataFrame,
    dividend_yield_initial_value: float,
) -> EquityDerivedParams
```

Set up an equity price derived from dividends, as in Wilkie
[(1986)](https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf):
the price is the dividend index divided by the dividend yield, both already calibrated as their own factors.

A dividend yield is the yearly dividend divided by the price, so the price is the dividend divided by the yield.
Wilkie's model simulates dividends and yields, and the price follows from them: when dividends grow or yields
fall, the price rises. There is no data fetch, no fit and no separate equity shock; the starting price is
`P(0) = D(0) / Y(0)`. It is the last link of Wilkie's cascade, where inflation drives the dividend yield and
dividend growth, which in turn give the price.

In a factor set this is `method: wilkie_derived` with `dividend_growth_name` and `dividend_yield_name`; `ticker`,
`n_regimes` and `period` are ignored, and beliefs and `measure: risk_neutral` are not allowed.

**Args:**

- <u>name (str):</u> the equity's name in the simulation and in `params()`/`changes()`.
- <u>dividend_growth_changes (pl.DataFrame):</u> the dividend growth entry's `changes()` output (`date` and `value`).
- <u>dividend_growth_initial_value (float):</u> that entry's calibrated `initial_value`, the dividend index D(0).
- <u>dividend_yield_changes (pl.DataFrame):</u> the dividend yield entry's `changes()` output (`date` and `value`).
- <u>dividend_yield_initial_value (float):</u> that entry's calibrated `initial_value`, the yield Y(0).

**Returns:**

<u>EquityDerivedParams:</u> `initial_value`, the starting price D(0) / Y(0).

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.dividend_growth.dividend_growth_controller import DividendGrowth
from financescenarios.factors.dividend_yield.dividend_yield_controller import DividendYield
from financescenarios.factors.dividend_yield.dividend_yield_model import reconstruct_dividend_yield_residuals
from financescenarios.factors.equities.equities_controller import Equities
from financescenarios.factors.inflation.inflation_controller import Inflation

toolkit = Toolkit(
    ["JNJ"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="1995-01-01", end_date="2019-12-31",
    benchmark_ticker=None,
)
inflation = Inflation(toolkit)
inflation.calibrate("inflation", country="United States", period="monthly", method="wilkie_ar1")
dividend_yield = DividendYield(toolkit)
yield_params = dividend_yield.calibrate("dividend_yield", ticker="JNJ", period="monthly")
yield_residual = reconstruct_dividend_yield_residuals(
    dividend_yield.series("dividend_yield"), yield_params, dividend_yield.time_step("dividend_yield")
)
dividend_growth = DividendGrowth(toolkit)
growth_params = dividend_growth.calibrate(
    "dividend_growth", inflation.series("inflation"), yield_residual, ticker="JNJ", period="monthly"
)

equities = Equities(toolkit)
equities.calibrate_derived(
    "equity",
    dividend_growth_changes=dividend_growth.changes("dividend_growth"),
    dividend_growth_initial_value=growth_params.initial_value,
    dividend_yield_changes=dividend_yield.changes("dividend_yield"),
    dividend_yield_initial_value=yield_params.initial_value,
)
```

Which returns (calibrated on 2026-10-04):

| dividend index D(0) | dividend yield Y(0) | initial_value P(0) |
|--------------------:|--------------------:|-------------------:|
| 3.75 | 0.0263 | 142.47 |

Johnson & Johnson's $3.75 dividend at a 2.63% yield gives a starting price of $142.47 at the end of 2019, close to
its actual closing price of $145.87.

## calibrate_heston

```python
calibrate_heston(
    name: str,
    ticker: str,
    risk_free_rate: float,
    dividend_yield: float,
    period: str = 'monthly',
) -> HestonParams | FXParams
```

Calibrate one equity for pricing with the Heston [(1993)](https://doi.org/10.1093/rfs/6.2.327) model, in which the
volatility itself moves, fitted to today's option prices.

A flat volatility treats a 20% fall and a 20% rise as equally likely and every horizon as equally uncertain.
Option prices disagree: crash protection costs more than a bet on a rally (the skew), and a year's volatility
differs from a month's (the term structure). Heston's variance moves, returns to a long-run level and rises when
prices fall, which reproduces both, so an option valued on these paths prices close to the market's own quote.

The fit uses the Finance Toolkit's smoothed volatility surface at the expirations nearest 1, 2, 3, 6, 9 and 12
months, on strikes within 20% of today's price; the drift is as in `calibrate_risk_neutral`. Paths use the
full-truncation scheme of [Lord, Koekkoek and van Dijk (2010)](https://doi.org/10.1080/14697680802392496). Without
usable options data this falls back to `calibrate_risk_neutral` with `volatility_source="realized"` and logs a
warning.

**Args:**

- <u>name (str):</u> the equity's name in the simulation and in `params()`/`changes()`.
- <u>ticker (str):</u> the ticker whose options to fit; it needs a liquid options market, such as SPY.
- <u>risk_free_rate (float):</u> today's risk-free rate, annual, as a decimal.
- <u>dividend_yield (float):</u> today's dividend yield, annual, as a decimal.
- <u>period (str):</u> the frequency of the price history behind `changes()` and the fallback. Defaults to "monthly".

**Returns:**

<u>HestonParams &#124; FXParams:</u> the Heston fit, or the flat-volatility fallback.

**Raises:**

- <u>ValueError:</u> if `period` is not recognized or a rate is not a finite number.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.factors.equities.equities_controller import Equities

toolkit = Toolkit(["SPY"], api_key="FINANCIAL_MODELING_PREP_KEY", benchmark_ticker=None)
params = Equities(toolkit).calibrate_heston("spy", "SPY", risk_free_rate=0.0399, dividend_yield=0.0115)
```

Which returns (calibrated on 2026-10-07 on 545 quotes):

| Field | Value |
|:------|------:|
| drift | 0.0284 |
| initial_variance | 0.0201 |
| mean_reversion_speed | 14.62 |
| long_run_variance | 0.0219 |
| volatility_of_variance | 1.18 |
| correlation | -0.51 |
| initial_value | 779.09 |
| fit_error | 0.0050 |

Today's volatility is 14.2% (the square root of 0.0201), the long-run level 14.8%, and the -0.51 correlation is
the skew.

## names

```python
equities.names  # property -> list[str]
```

The names of every equity calibrated so far, in calibration order.

## params

```python
params(name: str) -> RegimeParams | FXParams | HestonParams | EquityDerivedParams
```

The calibrated parameters for one equity: `RegimeParams` for a regime fit, `FXParams` for a risk-neutral one,
`HestonParams` for a Heston fit and `EquityDerivedParams` for a Wilkie-derived one.

**Args:**

- <u>name (str):</u> the equity's name, as passed to a `calibrate` method.

**Raises:**

- <u>RuntimeError:</u> if no `calibrate` method has been called for `name` yet.

## step_function

```python
equities.step_function  # property
```

The regime-switching lognormal step function; it holds no state, so every regime-switching equity shares it.

## changes

```python
changes(name: str) -> pl.DataFrame
```

The dated period log-returns of one equity, from the prices already fetched during calibration. The correlation
estimate reuses them instead of fetching the data again.

**Args:**

- <u>name (str):</u> the equity's name, as passed to a `calibrate` method.

**Returns:**

<u>pl.DataFrame:</u> two columns, `date` and `value`.

**Raises:**

- <u>RuntimeError:</u> if no `calibrate` method has been called for `name` yet.

## How It Is Calculated

The model functions behind this page, each with the formula it implements.

{% raw %}
### rescale_transition_matrix

```python
rescale_transition_matrix(
    transition_matrix: list[list[float]],
    from_dt: float,
    to_dt: float,
) -> list[list[float]]
```

Rescale a Markov transition matrix fit at one step size to another via its continuous-time generator, since
`simulate_regime_path` steps it once per *simulation* step (a monthly-fit chain stepped weekly would otherwise
switch regimes ~4.3x too fast).

The formula is as follows:

$$
Q = \operatorname{logm}(P) / \text{from\_dt}
$$

$$
\text{P\_rescaled} = \operatorname{expm}(Q \cdot \text{to\_dt})
$$

$$
\text{P\_rescaled} = \text{Pi} + \lambda ^{\text{to\_dt} / \text{from\_dt}} \cdot (I - \text{Pi}),\;\; \lambda = p_{00} + p_{11} - 1 (\text{two regimes})
$$

Where Pi has both rows equal to the stationary distribution, pi_0 = (1 - p_11) / (2 - p_00 - p_11). The
two-regime closed form applies when 0 < lambda < 1 and matches logm/expm to float noise.

**Args:**

- <u>transition_matrix (list[list[float]]):</u> row-stochastic transition probabilities, fit at `from_dt`'s granularity.
- <u>from_dt (float):</u> the time step (in years) `transition_matrix` was fit at.
- <u>to_dt (float):</u> the time step (in years) to rescale to.

**Returns:**

<u>list[list[float]]:</u> the rescaled row-stochastic transition matrix. Identical to the input (as a plain list round-trip) when `from_dt == to_dt`.

**References:**

- Israel, R.B., Rosenthal, J.S., Wei, J.Z. (2001). "Finding Generators for Markov Chains via Empirical Transition Matrices, with Applications to Credit Ratings." Mathematical Finance, 11(2), 245-265. <https://doi.org/10.1111/1467-9965.00114>
{% endraw %}

### fit_regime_switching_lognormal

```python
fit_regime_switching_lognormal(
    prices: pl.Series,
    time_step: float,
    n_regimes: int = 2,
    max_iterations: int = _MAX_EM_ITERATIONS,
    tolerance: float = 1e-06,
) -> RegimeParams
```

Fit Hardy's (2001) regime-switching lognormal model to a price series: each log-return is normal with the mean
and volatility of a hidden regime that follows a Markov chain. Baum-Welch EM alternates an E-step (Hamilton's
1989 filter forward, a smoother backward, giving each step's regime probabilities) and an M-step (the parameters
as probability-weighted averages) until the log-likelihood gains less than `tolerance`.

The formula is as follows:

$$
r_{t} | s_{t} = k \sim \operatorname{Normal}(\mu_{k},\; \sigma_{k} ^{2}),\;\; P(s_{t+1} = j | s_{t} = i) = p_{ij}
$$

$$
\alpha_{t}(j) = e_{t}(j) \cdot \sum_{i} \alpha_{t-1} (i) \cdot p_{ij} / c_{t}
$$

$$
\beta_{t}(i) = \sum_{j} p_{ij} \cdot e_{t+1}(j) \cdot \beta_{t+1}(j) / c_{t+1}
$$

$$
\gamma_{t}(k) = \alpha_{t}(k) \cdot \beta_{t}(k) / \sum_{j} \alpha_{t} (j) \cdot \beta_{t}(j)
$$

$$
p_{ij} < - \sum_{t} \alpha_{t} (i) \cdot p_{ij} \cdot e_{t+1}(j) \cdot \beta_{t+1}(j) / c_{t+1},\;\; \text{each row rescaled to sum to 1}
$$

$$
\mu_{k} = \sum_{t} \gamma_{t} (k) \cdot r_{t} / \sum_{t} \gamma_{t} (k)
$$

$$
\sigma_{k} ^{2} = \sum_{t} \gamma_{t} (k) \cdot (r_{t} - \mu_{k}) ^{2} / \sum_{t} \gamma_{t} (k)
$$

$$
\text{log}\; L = \sum_{t} \;\text{log} (c_{t})
$$

Where r_t is the log-return, e_t(k) the normal density of r_t in regime k, c_t the scale that makes alpha_t sum
to 1 and gamma_t(k) the smoothed probability of regime k at t. Only the returned means and volatilities are
annualized (divided by `time_step` and `sqrt(time_step)`), so a simulation can use its own step size.

**Args:**

- <u>prices (pl.Series):</u> historical price levels, evenly spaced in time (not returns).
- <u>time_step (float):</u> time increment between price observations, in years; used only to annualize the returned regime_means/regime_volatilities, not part of the EM fit itself.
- <u>n_regimes (int):</u> number of regimes to fit (2 = the standard Hardy bull/bear model).
- <u>max_iterations (int):</u> maximum EM iterations before stopping.
- <u>tolerance (float):</u> stop when the log-likelihood improves by less than this.

**Returns:**

<u>RegimeParams:</u> calibrated regime means/volatilities (annualized) /transition matrix (in this fit's own per-observation units, see RegimeParams.transition_matrix), the most likely current regime, and the last observed price as x0.

**Raises:**

- <u>ValueError:</u> if prices has fewer than n_regimes * 5 observations, or the EM fit collapses a regime to ~zero posterior mass (a degenerate fit with no observations assigned to it).

**Warns:**

- <u>UserWarning:</u> if the log-likelihood decreases between iterations (should be monotonically non-decreasing; signals a real bug/numerical instability, not just slow convergence), or if max_iterations is reached without the tolerance being satisfied.

**References:**

- Hardy, M.R. (2001). "A Regime-Switching Model of Long-Term Stock Returns." North American Actuarial Journal, 5(2), 41-53. <https://doi.org/10.1080/10920277.2001.10595984>
- Hamilton, J.D. (1989). "A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle." Econometrica, 57(2), 357-384. <https://doi.org/10.2307/1912559>
- Alswaidan, A., Jin, C., Varner, J.D. "Continuous Hidden Markov Models for Equity Returns: Heavy-Tail Emission Families and Regime-Conditional Value-at-Risk." arXiv:2606.23492. <https://arxiv.org/abs/2606.23492>. Only its shared Gaussian EM/forward-backward machinery is used here, not its heavy-tail emission families.
- Baum, L.E., Petrie, T., Soules, G., Weiss, N. (1970). "A Maximization Technique Occurring in the Statistical Analysis of Probabilistic Functions of Markov Chains." The Annals of Mathematical Statistics, 41(1), 164-171. <https://doi.org/10.1214/aoms/1177697196>

### fit_hibbert_regime_switching

```python
fit_hibbert_regime_switching(
    prices: pl.Series,
    risk_free_rate: pl.Series,
    time_step: float,
    n_regimes: int = 2,
    max_iterations: int = _MAX_EM_ITERATIONS,
    tolerance: float = 1e-06,
) -> RegimeParams
```

Fit Hibbert, Mowbray and Turnbull's (2001) regime-switching equity: the same Baum-Welch EM as
`fit_regime_switching_lognormal`, but on log-returns in excess of the nominal short rate, so the regimes
describe the equity risk premium and the simulated short rate is added back at each step (see
scenarios_controller._make_hibbert_equity_step). `prices` and `risk_free_rate` are paired by their trailing
observations, not joined on date.

The formula is as follows:

$$
x_{t} = \ln(S_{t} / S_{t-1}) - r_{t} \cdot \text{dt}
$$

$$
x_{t} | s_{t} = k \sim \operatorname{Normal}(\mu_{k} \cdot \text{dt},\; \sigma_{k} ^{2} \cdot \text{dt})
$$

Where r_t is the annualized short rate and s_t the hidden regime.

**Args:**

- <u>prices (pl.Series):</u> historical price levels, evenly spaced in time.
- <u>risk_free_rate (pl.Series):</u> the paired nominal short-rate factor's raw historical level series (annualized, decimal fraction), the same period as `prices`, trailing-truncated to `prices`' length if longer.
- <u>time_step (float):</u> time increment between observations, in years.
- <u>n_regimes (int):</u> number of regimes to fit (2 = bull/bear, per Hardy 2001).
- <u>max_iterations (int):</u> maximum EM iterations before stopping.
- <u>tolerance (float):</u> stop when the log-likelihood improves by less than this.

**Returns:**

<u>RegimeParams:</u> calibrated regime means/volatilities of the *excess* log-return (annualized), transition matrix, most likely current regime, and the last observed price as x0.

**Raises:**

- <u>ValueError:</u> if prices has fewer than n_regimes * 5 observations, or the EM fit collapses a regime to ~zero posterior mass.

**References:**

- Hibbert, J., Mowbray, P., Turnbull, C. (2001). "A Stochastic Asset Model & Calibration for Long-Term Financial Planning Purposes." Barrie & Hibbert Limited. <https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf>
- Hardy, M.R. (2001). "A Regime-Switching Model of Long-Term Stock Returns." North American Actuarial Journal, 5(2), 41-53. <https://doi.org/10.1080/10920277.2001.10595984>

### fit_regime_switching_tvtp

```python
fit_regime_switching_tvtp(
    prices: pl.Series,
    price_dates: pl.Series,
    business_cycle_covariate: pl.Series,
    business_cycle_covariate_dates: pl.Series,
    time_step: float,
    n_regimes: int = 2,
    max_iterations: int = _MAX_EM_ITERATIONS,
    tolerance: float = 1e-06,
) -> RegimeParams
```

Fit a regime-switching lognormal model whose transition probabilities vary with a business-cycle covariate
(Filardo's 1994 time-varying transition probabilities, see RegimeTVTPParams). Two steps rather than a joint
maximum-likelihood fit (Filardo; Diebold, Lee and Weinbach's 1994 EM): fit the plain model with Baum-Welch EM, then
take each return's most likely regime as the state path and fit, per origin regime, a multinomial logit of the
next regime on the covariate. Prices and covariate are inner-joined on date.

The formula is as follows:

$$
s_{t} = \text{argmax}_{k} P (s_{t} = k | r_{1},\; ...,\; r_{T})
$$

$$
\text{max over (theta\_i, gamma\_i) of sum\_t:s\_t=i ln p\_i},\;\; s_{t+1}(z_{t}) - 0.01 \cdot (| \theta_{i} | ^{2} + | \gamma_{i} | ^{2})
$$

$$
p_{ij}(z_{t}) = \exp(\theta_{ij} + \gamma_{ij} \cdot z_{t}) / \sum_{k} \;\text{exp} (\theta_{ik} + \gamma_{ik} \cdot z_{t})
$$

Where P(s_t = k | r_1, ..., r_T) is the smoothed regime probability and z_t the covariate at the end of return
t; the small ridge penalty keeps the fit finite when a row's transitions separate perfectly by covariate level.

**Args:**

- <u>prices (pl.Series):</u> historical price levels, evenly spaced in time.
- <u>price_dates (pl.Series):</u> one date per `prices` observation.
- <u>business_cycle_covariate (pl.Series):</u> the business-cycle indicator's raw historical level series (e.g. LeadingIndicator.series).
- <u>business_cycle_covariate_dates (pl.Series):</u> the dates paired with `business_cycle_covariate` (e.g. LeadingIndicator.dates).
- <u>time_step (float):</u> time increment between price observations, in years.
- <u>n_regimes (int):</u> number of regimes to fit (2 = the standard Hardy bull/bear model).
- <u>max_iterations (int):</u> maximum EM iterations before stopping (baseline fit only).
- <u>tolerance (float):</u> stop when the log-likelihood improves by less than this (baseline fit only).

**Returns:**

<u>RegimeParams:</u> the baseline calibration (regime_means/regime_volatilities/ transition_matrix, exactly as fit_regime_switching_lognormal would produce against the date-joined price series), plus `tvtp`: the fitted RegimeTVTPParams.

**Raises:**

- <u>ValueError:</u> if fewer than `n_regimes * 5` price observations remain after the date join, the baseline EM fit collapses a regime, or a row of the transition matrix has too few observed transitions to fit its own multinomial logit (fewer than `2*(n_regimes-1)*_MINIMUM_TVTP_ROW_OBSERVATIONS_MULTIPLE`).

**References:**

- Filardo, A.J. (1994). "Business-Cycle Phases and Their Transitional Dynamics." Journal of Business & Economic Statistics, 12(3), 299-308. <https://doi.org/10.1080/07350015.1994.10524545>
- Diebold, F.X., Lee, J.H., Weinbach, G.C. (1994). "Regime Switching with Time-Varying Transition Probabilities." In Hargreaves, C. (ed.), Nonstationary Time Series Analysis and Cointegration, Oxford University Press, 283-302. The joint EM estimator this two-step fit approximates. <https://doi.org/10.1093/oso/9780198773917.003.0010>
- Hardy, M.R. (2001). "A Regime-Switching Model of Long-Term Stock Returns." North American Actuarial Journal, 5(2), 41-53. <https://doi.org/10.1080/10920277.2001.10595984>

{% raw %}
### simulate_regime_path

```python
simulate_regime_path(
    params: RegimeParams,
    n_simulations: int,
    n_steps: int,
    rng: np.random.Generator,
    simulation_time_step: float | None = None,
) -> np.ndarray
```

Pre-simulate every path's regime sequence as a Markov chain, independent of the correlated return shocks, so it
is drawn once upfront rather than inside the engine loop. Each step inverts the current row's cumulative
transition probabilities at a uniform draw.

The formula is as follows:

$$
s_{t+1} = \text{number of}\; j \;\text{with}\; u_{t} > p_{s_{t}},\;\; \text{0 + ... + p\_s\_t},\;\; \text{j},\;\; u_{t} \sim \operatorname{Uniform}(0,\; 1)
$$

**Args:**

- <u>params (RegimeParams):</u> calibrated regime transition matrix and initial regime.
- <u>n_simulations (int):</u> number of Monte Carlo paths.
- <u>n_steps (int):</u> number of time steps per path.
- <u>rng (np.random.Generator):</u> the random generator to draw regime transitions from.
- <u>simulation_time_step (float &#124; None):</u> the *simulation*'s own time step (in years), which need not match `params.time_step` (the historical fit's observation spacing). When given and different from `params.time_step`, `params.transition_matrix` is rescaled to this step size first (see rescale_transition_matrix); otherwise regime dwell times would be off by the frequency ratio. None (the default) steps `transition_matrix` as-is, at its own fit granularity.

**Returns:**

<u>np.ndarray:</u> shape (n_simulations, n_steps + 1), int regime index per simulation/time-step, column 0 is params.initial_regime for every simulation.

**References:**

- Hardy, M.R. (2001). "A Regime-Switching Model of Long-Term Stock Returns." North American Actuarial Journal, 5(2), 41-53. <https://doi.org/10.1080/10920277.2001.10595984>
- Alswaidan, A., Jin, C., Varner, J.D. "Continuous Hidden Markov Models for Equity Returns: Heavy-Tail Emission Families and Regime-Conditional Value-at-Risk." arXiv:2606.23492. <https://arxiv.org/abs/2606.23492>
- Israel, R.B., Rosenthal, J.S., Wei, J.Z. (2001). "Finding Generators for Markov Chains via Empirical Transition Matrices, with Applications to Credit Ratings." Mathematical Finance, 11(2), 245-265. <https://doi.org/10.1111/1467-9965.00114>
{% endraw %}

### fit_risk_neutral_equity

```python
fit_risk_neutral_equity(
    risk_free_rate: float,
    dividend_yield: float,
    volatility: float,
    initial_value: float,
) -> FXParams
```

Build risk-neutral (Q-measure) equity parameters: geometric Brownian motion with the Black-Scholes-Merton
drift, the cost of carry r - q, instead of a fitted real-world drift. Reuses `FXParams`/`step_fx_process`,
the same GBM; see equities_controller.Equities.calibrate_risk_neutral().

The formula is as follows:

$$
\text{dS}_{t} = (r - q) \cdot S_{t} \cdot \text{dt} + \sigma \cdot S_{t} \cdot \text{dW}_{t}
$$

**Args:**

- <u>risk_free_rate (float):</u> today's continuously-compounded risk-free rate (annualized, decimal fraction), typically the already-calibrated interest_rates factor's current level.
- <u>dividend_yield (float):</u> today's dividend yield (annualized, decimal fraction), typically the already-calibrated dividend_yield factor's current level.
- <u>volatility (float):</u> annualized volatility to simulate with, either options-implied (ATM) or realized, see Equities.calibrate_risk_neutral().
- <u>initial_value (float):</u> the last observed price level, the simulation's S0.

**Returns:**

<u>FXParams:</u> drift = risk_free_rate - dividend_yield, the given volatility and initial_value.

**References:**

- Black, F., Scholes, M. (1973). "The Pricing of Options and Corporate Liabilities." Journal of Political Economy, 81(3), 637-654. <https://doi.org/10.1086/260062>
- Merton, R.C. (1973). "Theory of Rational Option Pricing." Bell Journal of Economics and Management Science, 4(1), 141-183. <https://doi.org/10.2307/3003143>

{% raw %}
### step_regime_switching

```python
step_regime_switching(
    current_value: np.ndarray | float,
    shock: np.ndarray | float,
    mean: np.ndarray | float,
    volatility: np.ndarray | float,
) -> np.ndarray
```

Advance a lognormal price by one step in an already-drawn regime (see simulate_regime_path). The caller passes
mean and volatility already scaled to the step, so there is no time_step argument.

The formula is as follows:

$$
S_{t+dt} = S_{t} \cdot \exp(m + v \cdot z),\;\; m = \mu_{k} \cdot \text{dt},\;\; v = \sigma_{k} \cdot \sqrt{\text{dt}}
$$

Where k is the regime over the step and z the standard normal shock.

**Args:**

- <u>current_value (np.ndarray &#124; float):</u> the price level at the current time step.
- <u>shock (np.ndarray &#124; float):</u> a standard normal draw for the return innovation this step.
- <u>mean (np.ndarray &#124; float):</u> the active regime's mean log-return, already scaled by time_step.
- <u>volatility (np.ndarray &#124; float):</u> the active regime's log-return volatility, already scaled by sqrt(time_step).

**Returns:**

<u>np.ndarray:</u> the price at the next time step.

**References:**

- Hardy, M.R. (2001). "A Regime-Switching Model of Long-Term Stock Returns." North American Actuarial Journal, 5(2), 41-53. <https://doi.org/10.1080/10920277.2001.10595984>
- Alswaidan, A., Jin, C., Varner, J.D. "Continuous Hidden Markov Models for Equity Returns: Heavy-Tail Emission Families and Regime-Conditional Value-at-Risk." arXiv:2606.23492. <https://arxiv.org/abs/2606.23492>
{% endraw %}
