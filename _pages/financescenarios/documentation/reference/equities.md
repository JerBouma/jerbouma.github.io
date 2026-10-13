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

Equity indices, sectors, regions and styles with regime switching.

```python
from financescenarios.factors.equities.equities_controller import Equities
```

Simulate equity prices: a broad stock index, a sector, a region or an investment style, each tracked through one
ticker such as SPY or an ETF.

The model is the regime-switching lognormal model of [Hardy (2001)](https://doi.org/10.1080/10920277.2001.10595984).
Markets alternate between calm stretches of steady gains and turbulent stretches of losses and large swings, and
once turbulent they tend to stay so for months. Each regime has its own mean and volatility of log-returns, and the
market switches between them with fitted chances. A single lognormal understates crashes; the mixture of regimes
gives the fatter left tail and the clustered, multi-period drawdowns that matter for guarantees, capital and
tail metrics, while prices stay positive. Each equity, such as SPY or a sector, region or style ETF, follows its own
regime path and is linked to the other factors through the correlation matrix.

The options:

- `method`: `regime_switching` (the default); `hibbert_regime_switching`, the same model on the return above a short
  interest rate (Hibbert, Mowbray and Turnbull
  [(2001)](https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf));
  `wilkie_derived`, the price as dividends divided by the dividend yield (Wilkie
  [(1986)](https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf));
  or `knw_sv`, the equity leg of the Koijen, Nijman and Werker model, fitted together with its interest rate.
- `condition_on_business_cycle`: turbulence becomes more likely when the leading indicator signals a downturn
  ([Filardo, 1994](https://doi.org/10.1080/07350015.1994.10524545)).
- `measure: risk_neutral`: one volatility and a drift of the risk-free rate minus the dividend yield, for
  market-consistent valuation ([Black and Scholes, 1973](https://doi.org/10.1086/260062)), or a volatility that moves
  with `volatility_source: heston` ([Heston, 1993](https://doi.org/10.1093/rfs/6.2.327)).
- `beliefs`: your own regime means and volatilities instead of the fitted ones.

Prices are each ticker's adjusted closes (dividends reinvested) from the Finance Toolkit; any ticker worldwide works.

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

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
Equities(toolkit: Toolkit)
```

</details>

## calibrate

Calibrate one equity from its price history: the mean and volatility of its log-return in each regime, and the
chance of moving between regimes each period.

The scenarios inherit the market's own history of calm and turbulent stretches: how deep and how long its
drawdowns were, and how often they came. The diagonal of the transition matrix is the chance of staying in a
regime one more period, so the expected stay is 1 / (1 - that chance): a 0.90 monthly chance of staying calm means
calm stretches last about ten months. Regime 0 is always the one with the lowest mean return.

The regimes are never observed, only the returns, so the fit is the Baum-Welch expectation-maximization algorithm
for hidden Markov models ([Baum et al., 1970](https://doi.org/10.1214/aoms/1177697196)). Means and volatilities
are annual; the transition matrix is per period of the data.

Also known as: regime-switching lognormal (RSLN), hidden Markov model of equity returns.

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

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate(name: str, ticker: str, n_regimes: int = 2, period: str = 'monthly') -> RegimeParams
```

**Args:**

- <u>name (str):</u> the equity's name in the scenarios, e.g. "us_broad".
- <u>ticker (str):</u> the ticker to fit, such as "SPY" or a sector, regional or style ETF.
- <u>n_regimes (int):</u> the number of regimes, at least 2. Defaults to 2 (calm and turbulent, as in Hardy 2001).
- <u>period (str):</u> the price frequency: "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "monthly".

**Returns:**

<u>RegimeParams:</u> `regime_means`, `regime_volatilities`, `transition_matrix`, `stationary_distribution` (long-run share of time per regime), `initial_regime` and `initial_value` (the last price).

**Raises:**

- <u>ValueError:</u> if `period`, `n_regimes` or `ticker` is invalid, there are fewer than `n_regimes * 5` prices, or a regime ends up with almost no observations.

</details>

## calibrate_tvtp

Calibrate one equity whose regime switching follows the business cycle: `calibrate()`'s fit plus a regression that
ties the chance of switching regime to the leading indicator.

With `calibrate()` the chance of a calm market turning turbulent is the same every month. Here it rises when the
leading indicator (the OECD Composite Leading Indicator, around 100 in a normal economy) signals a downturn, so
turbulent stretches cluster around weak economies. This is the time-varying transition probability (TVTP) model of
[Filardo (1994)](https://doi.org/10.1080/07350015.1994.10524545), estimated in the simpler two-step way of
[Diebold, Lee and Weinbach (1994)](https://doi.org/10.1093/oso/9780198773917.003.0010): first the regimes, then a
logit regression of which regime came next on the indicator's level.

In a factor set this is `condition_on_business_cycle: true`, which needs `leading_indicator.enabled: true`.

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

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

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

**Args:**

- <u>name (str):</u> the equity's name in the scenarios.
- <u>ticker (str):</u> the ticker to fit, as in `calibrate()`.
- <u>business_cycle_covariate (pl.Series):</u> the leading indicator's historical levels, e.g. `LeadingIndicator.series`.
- <u>business_cycle_covariate_dates (pl.Series):</u> the dates of those levels, e.g. `LeadingIndicator.dates`.
- <u>n_regimes (int):</u> the number of regimes, at least 2. Defaults to 2.
- <u>period (str):</u> the price frequency, as in `calibrate()`. Defaults to "monthly".

**Returns:**

<u>RegimeParams:</u> the regime fit, with `tvtp` holding `baseline_log_odds` and `covariate_sensitivity`, one row per starting regime.

**Raises:**

- <u>ValueError:</u> if `period`, `n_regimes` or `ticker` is invalid, too few prices line up with the indicator by date, or a regime has too few observed transitions to fit.

</details>

## calibrate_hibbert_regime_switching

Calibrate one equity on its return above a short interest rate, as in the Barrie & Hibbert model of Hibbert,
Mowbray and Turnbull
[(2001)](https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf).

The fit is the same as in `calibrate()`, but on the extra return stocks earn over cash (the equity risk premium):
each period's log-return minus the short rate times the period length. When simulating, the paired interest rate's
simulated level is added back each step, so higher rates mean higher expected equity returns, while the premium on
top keeps its own calm and turbulent regimes.

In a factor set this is `method: hibbert_regime_switching`, with `nominal_rate_name` naming the interest rate; it
has no risk-neutral version.

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

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate_hibbert_regime_switching(
    name: str,
    ticker: str,
    risk_free_rate: pl.Series,
    n_regimes: int = 2,
    period: str = 'monthly',
) -> RegimeParams
```

**Args:**

- <u>name (str):</u> the equity's name in the scenarios.
- <u>ticker (str):</u> the ticker to fit, as in `calibrate()`.
- <u>risk_free_rate (pl.Series):</u> the paired interest rate's historical levels (annual, as decimals), e.g. `InterestRates.series(name)`, sampled at the same `period` as the prices.
- <u>n_regimes (int):</u> the number of regimes, at least 2. Defaults to 2.
- <u>period (str):</u> the price frequency, as in `calibrate()`. Defaults to "monthly".

**Returns:**

<u>RegimeParams:</u> the regime fit, with `regime_means` as annual returns above the short rate.

**Raises:**

- <u>ValueError:</u> if `period`, `n_regimes` or `ticker` is invalid, there are fewer than `n_regimes * 5` prices, or a regime ends up with almost no observations.

</details>

## calibrate_risk_neutral

Calibrate one equity for pricing rather than forecasting: a constant volatility and a drift of the risk-free rate
minus the dividend yield, as in Black and Scholes [(1973)](https://doi.org/10.1086/260062) and Merton
[(1973)](https://doi.org/10.2307/3003143).

`calibrate()` forecasts how the market will behave, with an equity risk premium and regimes; this matches today's
market prices instead. Every path is expected to earn the risk-free rate, so discounted scenario values
reproduce today's prices and an option or guarantee valued on them has its market-consistent value, as a
Solvency II best estimate or an IFRS 17 fulfillment value requires. The price follows
`d(log S) = (r - q - 0.5 * sigma^2) dt + sigma dW`, with `r` the risk-free rate, `q` the dividend yield and
`sigma` the volatility.

`volatility_source` picks `sigma`:

- `"implied"`: the options market's volatility at the strike nearest today's price, at one expiration.
- `"svi"`: the at-the-money point of the Finance Toolkit's smoothed volatility surface
  ([Gatheral and Jacquier, 2014](https://doi.org/10.1080/14697688.2013.819986)), longest expiration.
- `"realized"`: the ticker's own historical volatility, for tickers without liquid options.

The first two fall back to `"realized"`, with a warning, without options data; `calibrate_heston` lets the
volatility itself move.

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

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

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

**Args:**

- <u>name (str):</u> the equity's name in the scenarios.
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

</details>

## calibrate_derived

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

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate_derived(
    name: str,
    dividend_growth_changes: pl.DataFrame,
    dividend_growth_initial_value: float,
    dividend_yield_changes: pl.DataFrame,
    dividend_yield_initial_value: float,
) -> EquityDerivedParams
```

**Args:**

- <u>name (str):</u> the equity's name in the scenarios.
- <u>dividend_growth_changes (pl.DataFrame):</u> the dividend growth entry's `changes()` output (`date` and `value`).
- <u>dividend_growth_initial_value (float):</u> that entry's calibrated `initial_value`, the dividend index D(0).
- <u>dividend_yield_changes (pl.DataFrame):</u> the dividend yield entry's `changes()` output (`date` and `value`).
- <u>dividend_yield_initial_value (float):</u> that entry's calibrated `initial_value`, the yield Y(0).

**Returns:**

<u>EquityDerivedParams:</u> `initial_value`, the starting price D(0) / Y(0).

</details>

## calibrate_heston

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

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate_heston(
    name: str,
    ticker: str,
    risk_free_rate: float,
    dividend_yield: float,
    period: str = 'monthly',
) -> HestonParams | FXParams
```

**Args:**

- <u>name (str):</u> the equity's name in the scenarios.
- <u>ticker (str):</u> the ticker whose options to fit; it needs a liquid options market, such as SPY.
- <u>risk_free_rate (float):</u> today's risk-free rate, annual, as a decimal.
- <u>dividend_yield (float):</u> today's dividend yield, annual, as a decimal.
- <u>period (str):</u> the frequency of the price history behind `changes()` and the fallback. Defaults to "monthly".

**Returns:**

<u>HestonParams &#124; FXParams:</u> the Heston fit, or the flat-volatility fallback.

**Raises:**

- <u>ValueError:</u> if `period` is not recognized or a rate is not a finite number.

</details>

## names

The names of every equity calibrated so far, in calibration order.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
equities.names  # property -> list[str]
```

</details>

## params

The calibrated parameters for one equity: `RegimeParams` for a regime fit, `FXParams` for a risk-neutral one,
`HestonParams` for a Heston fit and `EquityDerivedParams` for a Wilkie-derived one.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
params(name: str) -> RegimeParams | FXParams | HestonParams | EquityDerivedParams
```

**Args:**

- <u>name (str):</u> the equity's name, as passed to a `calibrate` method.

**Raises:**

- <u>RuntimeError:</u> if no `calibrate` method has been called for `name` yet.

</details>

## step_function

The price step of the regime-switching lognormal model: a lognormal move with the current regime's mean and
volatility.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
equities.step_function  # property
```

</details>

## changes

The historical log-returns of one equity, by date, from which its correlations with the other factors are
estimated.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
changes(name: str) -> pl.DataFrame
```

**Args:**

- <u>name (str):</u> the equity's name, as passed to a `calibrate` method.

**Returns:**

<u>pl.DataFrame:</u> two columns, `date` and `value`.

**Raises:**

- <u>RuntimeError:</u> if no `calibrate` method has been called for `name` yet.

</details>

## How It Is Calculated

The model functions behind this page, each with the formula it implements.

{% raw %}
### rescale_transition_matrix

Convert regime-switching probabilities fitted on one data frequency to another, so calm and turbulent
stretches last just as long in calendar time whatever step the scenarios use.

A transition matrix fitted on monthly returns gives the chance of switching regime per month. Applied
unchanged to weekly steps, the market would switch about 4.3 times too often and turbulent spells would be
far too short. The matrix is turned into a continuous-time rate of switching (its generator) and back into
probabilities at the new step, as is standard for rating migration matrices (Israel, Rosenthal and Wei,
2001). The long-run share of time in each regime is unchanged.

The formula is as follows:

$$
Q = \operatorname{logm}(P) / \text{from\_dt}
$$

$$
P_{\text{rescaled}} = \operatorname{expm}(Q \cdot \text{to\_dt})
$$

$$
P_{\text{rescaled}} = \text{Pi} + \lambda ^{\text{to\_dt} / \text{from\_dt}} \cdot (I - \text{Pi}),\;\; \lambda = p_{00} + p_{11} - 1 (\text{two regimes})
$$

Where Pi has both rows equal to the stationary distribution, pi_0 = (1 - p_11) / (2 - p_00 - p_11). The
two-regime closed form applies when 0 < lambda < 1 and gives the same answer as the general one.

**References:**

- Israel, R.B., Rosenthal, J.S., Wei, J.Z. (2001). "Finding Generators for Markov Chains via Empirical Transition Matrices, with Applications to Credit Ratings." Mathematical Finance, 11(2), 245-265. <https://doi.org/10.1111/1467-9965.00114>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
rescale_transition_matrix(
    transition_matrix: list[list[float]],
    from_dt: float,
    to_dt: float,
) -> list[list[float]]
```

**Args:**

- <u>transition_matrix (list[list[float]]):</u> the chances of moving between regimes per period of the fit.
- <u>from_dt (float):</u> the length of that period, in years (1/12 for monthly).
- <u>to_dt (float):</u> the length of the scenario step, in years.

**Returns:**

<u>list[list[float]]:</u> the chances of moving between regimes per scenario step; unchanged when the two periods match.

</details>
{% endraw %}

### fit_regime_switching_lognormal

Fit Hardy's (2001) regime-switching lognormal model to an equity's price history: a calm and a turbulent
market, each with its own mean return and volatility, and the chance of moving between them.

A single lognormal return distribution understates crashes: real equity returns have fatter tails and
volatility comes in clusters. Hardy's model keeps returns normal within each regime but lets the market sit
in a high-volatility regime for months at a time, so a mixture of the two produces the fat left tail and the
clustered losses that guarantees and capital requirements are most sensitive to. It is widely used for
equity-linked guarantees such as segregated funds and variable annuities.

The regimes are never observed, so the fit is Baum-Welch expectation-maximization: Hamilton's (1989) filter
gives the chance of each regime at every date, the parameters are re-estimated as weighted averages, and the
two steps repeat until the likelihood stops improving.

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
to 1 and gamma_t(k) the smoothed probability of regime k at t. Means and volatilities are reported per year;
the switching chances stay per period of the data.

**References:**

- Hardy, M.R. (2001). "A Regime-Switching Model of Long-Term Stock Returns." North American Actuarial Journal, 5(2), 41-53. <https://doi.org/10.1080/10920277.2001.10595984>
- Hamilton, J.D. (1989). "A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle." Econometrica, 57(2), 357-384. <https://doi.org/10.2307/1912559>
- Alswaidan, A., Jin, C., Varner, J.D. "Continuous Hidden Markov Models for Equity Returns: Heavy-Tail Emission Families and Regime-Conditional Value-at-Risk." arXiv:2606.23492. <https://arxiv.org/abs/2606.23492>. Its Gaussian fitting algorithm only.
- Baum, L.E., Petrie, T., Soules, G., Weiss, N. (1970). "A Maximization Technique Occurring in the Statistical Analysis of Probabilistic Functions of Markov Chains." The Annals of Mathematical Statistics, 41(1), 164-171. <https://doi.org/10.1214/aoms/1177697196>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fit_regime_switching_lognormal(
    prices: pl.Series,
    time_step: float,
    n_regimes: int = 2,
    max_iterations: int = _MAX_EM_ITERATIONS,
    tolerance: float = 1e-06,
) -> RegimeParams
```

**Args:**

- <u>prices (pl.Series):</u> the equity's price history, evenly spaced in time.
- <u>time_step (float):</u> the time between prices, in years (1/12 for monthly).
- <u>n_regimes (int):</u> the number of regimes, default 2 (calm and turbulent, as in Hardy 2001).
- <u>max_iterations (int):</u> the most fitting rounds before stopping.
- <u>tolerance (float):</u> stop once the likelihood improves by less than this.

**Returns:**

<u>RegimeParams:</u> each regime's annual mean and volatility, the chances of switching, the long-run share of time per regime, today's most likely regime and the last price.

**Raises:**

- <u>ValueError:</u> if there are fewer than `n_regimes * 5` prices, or a regime ends up with almost no observations.

**Warns:**

- <u>UserWarning:</u> if the fit does not settle within `max_iterations`, or the likelihood falls between rounds.

</details>

### fit_hibbert_regime_switching

Fit the regime-switching equity of Hibbert, Mowbray and Turnbull (2001): Hardy's calm and turbulent regimes,
fitted on the return stocks earn above cash rather than on the total return.

Equity returns are cash plus a risk premium. Modeling the premium, not the total return, ties equities to the
rate environment: in a scenario where short rates climb to 6%, expected equity returns climb with them, and in
a zero-rate world they fall. That consistency between asset classes is what the Barrie & Hibbert model was
built for, and it matters for long-horizon ALM, where a fixed equity return next to a moving yield curve would
make equities look too cheap or too dear against bonds. The premium itself keeps its regimes, so the fat
left tail and clustered losses of the plain model remain. In the scenarios the simulated short rate is added
back each step.

The formula is as follows:

$$
x_{t} = \ln(S_{t} / S_{t-1}) - r_{t} \cdot \text{dt}
$$

$$
x_{t} | s_{t} = k \sim \operatorname{Normal}(\mu_{k} \cdot \text{dt},\; \sigma_{k} ^{2} \cdot \text{dt})
$$

Where r_t is the annualized short rate and s_t the hidden regime.

**References:**

- Hibbert, J., Mowbray, P., Turnbull, C. (2001). "A Stochastic Asset Model & Calibration for Long-Term Financial Planning Purposes." Barrie & Hibbert Limited. <https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf>
- Hardy, M.R. (2001). "A Regime-Switching Model of Long-Term Stock Returns." North American Actuarial Journal, 5(2), 41-53. <https://doi.org/10.1080/10920277.2001.10595984>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

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

**Args:**

- <u>prices (pl.Series):</u> the equity's price history, evenly spaced in time.
- <u>risk_free_rate (pl.Series):</u> the short rate's history at the same frequency, annual, as decimals; the two are lined up on their latest observations.
- <u>time_step (float):</u> the time between prices, in years.
- <u>n_regimes (int):</u> the number of regimes, default 2 (calm and turbulent).
- <u>max_iterations (int):</u> the most fitting rounds before stopping.
- <u>tolerance (float):</u> stop once the likelihood improves by less than this.

**Returns:**

<u>RegimeParams:</u> each regime's annual mean and volatility of the return above cash, the chances of switching, today's most likely regime and the last price.

**Raises:**

- <u>ValueError:</u> if there are fewer than `n_regimes * 5` prices, or a regime ends up with almost no observations.

</details>

### fit_regime_switching_tvtp

Fit a regime-switching equity whose chance of turning turbulent depends on the business cycle, the
time-varying transition probabilities of Filardo (1994).

In the plain regime model a calm market is as likely to turn turbulent in a boom as in a slowdown. In practice
bear markets cluster around recessions. Here the chance of switching moves with a business-cycle indicator
such as the OECD leading indicator, so scenarios that start or pass through a weak economy carry a higher
chance of an equity drawdown, and equity losses line up with weak growth across the other factors.

The fit takes two steps rather than the joint estimation of Filardo and of Diebold, Lee and Weinbach (1994):
first the plain regime model, then, for each starting regime, a logit regression of which regime came next on
the indicator. A small penalty keeps the regression finite when the data separate perfectly.

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

Where P(s_t = k | r_1, ..., r_T) is the smoothed regime probability and z_t the indicator's level at the end of
return t.

**References:**

- Filardo, A.J. (1994). "Business-Cycle Phases and Their Transitional Dynamics." Journal of Business & Economic Statistics, 12(3), 299-308. <https://doi.org/10.1080/07350015.1994.10524545>
- Diebold, F.X., Lee, J.H., Weinbach, G.C. (1994). "Regime Switching with Time-Varying Transition Probabilities." In Hargreaves, C. (ed.), Nonstationary Time Series Analysis and Cointegration, Oxford University Press, 283-302. The joint EM estimator this two-step fit approximates. <https://doi.org/10.1093/oso/9780198773917.003.0010>
- Hardy, M.R. (2001). "A Regime-Switching Model of Long-Term Stock Returns." North American Actuarial Journal, 5(2), 41-53. <https://doi.org/10.1080/10920277.2001.10595984>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

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

**Args:**

- <u>prices (pl.Series):</u> the equity's price history, evenly spaced in time.
- <u>price_dates (pl.Series):</u> the date of each price.
- <u>business_cycle_covariate (pl.Series):</u> the business-cycle indicator's history, such as `LeadingIndicator.series`.
- <u>business_cycle_covariate_dates (pl.Series):</u> the date of each indicator value; only dates both share are used.
- <u>time_step (float):</u> the time between prices, in years.
- <u>n_regimes (int):</u> the number of regimes, default 2 (calm and turbulent).
- <u>max_iterations (int):</u> the most fitting rounds for the regime fit.
- <u>tolerance (float):</u> stop the regime fit once the likelihood improves by less than this.

**Returns:**

<u>RegimeParams:</u> the plain regime fit on the shared dates, plus `tvtp`, the logit coefficients that tie each regime's switching chances to the indicator.

**Raises:**

- <u>ValueError:</u> if fewer than `n_regimes * 5` prices share a date with the indicator, a regime ends up with almost no observations, or a regime has too few observed switches to fit (ten per regime with two regimes).

</details>

{% raw %}
### simulate_regime_path

Draw the sequence of calm and turbulent regimes each scenario passes through, starting from today's most
likely regime.

Each step the market stays in its regime or switches, with the fitted chances. Because regimes persist, a
scenario that enters the turbulent regime tends to stay there for several periods, which produces the
multi-period drawdowns that a single lognormal distribution cannot. The regime path is drawn separately from
the return shocks, so the regime decides each period's mean and volatility while the shock, correlated with
the other factors, decides where in that distribution the return lands. Each equity follows its own regime
path.

The formula is as follows:

$$
s_{t+1} = \text{number of}\; j \;\text{with}\; u_{t} > p_{s_{t}},\;\; \text{0 + ... + p\_s\_t},\;\; \text{j},\;\; u_{t} \sim \operatorname{Uniform}(0,\; 1)
$$

**References:**

- Hardy, M.R. (2001). "A Regime-Switching Model of Long-Term Stock Returns." North American Actuarial Journal, 5(2), 41-53. <https://doi.org/10.1080/10920277.2001.10595984>
- Alswaidan, A., Jin, C., Varner, J.D. "Continuous Hidden Markov Models for Equity Returns: Heavy-Tail Emission Families and Regime-Conditional Value-at-Risk." arXiv:2606.23492. <https://arxiv.org/abs/2606.23492>
- Israel, R.B., Rosenthal, J.S., Wei, J.Z. (2001). "Finding Generators for Markov Chains via Empirical Transition Matrices, with Applications to Credit Ratings." Mathematical Finance, 11(2), 245-265. <https://doi.org/10.1111/1467-9965.00114>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
simulate_regime_path(
    params: RegimeParams,
    n_simulations: int,
    n_steps: int,
    rng: np.random.Generator,
    simulation_time_step: float | None = None,
) -> np.ndarray
```

**Args:**

- <u>params (RegimeParams):</u> the calibrated switching chances and today's regime.
- <u>n_simulations (int):</u> the number of scenarios.
- <u>n_steps (int):</u> the number of steps per scenario.
- <u>rng (np.random.Generator):</u> the random number generator.
- <u>simulation_time_step (float &#124; None):</u> the scenario step in years; when it differs from the data frequency the switching chances are converted first (see `rescale_transition_matrix`). Default None, no conversion.

**Returns:**

<u>np.ndarray:</u> the regime of every scenario at every step, starting from today's regime.

</details>
{% endraw %}

### fit_risk_neutral_equity

Set up a risk-neutral equity for market-consistent valuation: a lognormal price that grows at the risk-free
rate minus the dividend yield, with one volatility, as in Black and Scholes (1973) and Merton (1973).

Under the risk-neutral measure every asset is expected to earn the risk-free rate, so the equity risk premium
drops out and the only parameter to choose is the volatility. Discounted at the risk-free rate, the expected
simulated price then equals today's price, which is what a market-consistent valuation of guarantees or
options (for example a Solvency II best estimate) requires. The dividend yield is subtracted because the
holder of the index receives it in cash, not in price. Returns are normal in log terms with no regimes, so
tail risk is set by the volatility alone.

The formula is as follows:

$$
\text{dS}_{t} = (r - q) \cdot S_{t} \cdot \text{dt} + \sigma \cdot S_{t} \cdot \text{dW}_{t}
$$

**References:**

- Black, F., Scholes, M. (1973). "The Pricing of Options and Corporate Liabilities." Journal of Political Economy, 81(3), 637-654. <https://doi.org/10.1086/260062>
- Merton, R.C. (1973). "Theory of Rational Option Pricing." Bell Journal of Economics and Management Science, 4(1), 141-183. <https://doi.org/10.2307/3003143>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fit_risk_neutral_equity(
    risk_free_rate: float,
    dividend_yield: float,
    volatility: float,
    initial_value: float,
) -> FXParams
```

**Args:**

- <u>risk_free_rate (float):</u> today's continuously compounded risk-free rate, annual, as a decimal.
- <u>dividend_yield (float):</u> today's dividend yield, annual, as a decimal.
- <u>volatility (float):</u> the annual volatility, implied by options or realized.
- <u>initial_value (float):</u> today's price.

**Returns:**

<u>FXParams:</u> `drift` (the risk-free rate minus the dividend yield), `volatility` and `initial_value`.

</details>

{% raw %}
### step_regime_switching

Move an equity price one step forward in the regime the scenario is in, the price step of Hardy's (2001)
regime-switching lognormal model.

Within a regime the log-return is normal, so the price stays positive and returns compound. Between regimes
the mean and volatility jump: a turbulent step can have a volatility two to three times that of a calm one
and a mean near zero or below. Over a horizon the result is a mixture of normals, with a fatter left tail and
more clustered losses than any single lognormal with the same average volatility. The shock is the
equity's correlated draw, so equities still move with rates, credit and the other factors within a step.

The formula is as follows:

$$
S_{t+dt} = S_{t} \cdot \exp(m + v \cdot z),\;\; m = \mu_{k} \cdot \text{dt},\;\; v = \sigma_{k} \cdot \sqrt{\text{dt}}
$$

Where k is the regime over the step and z the standard normal shock.

**References:**

- Hardy, M.R. (2001). "A Regime-Switching Model of Long-Term Stock Returns." North American Actuarial Journal, 5(2), 41-53. <https://doi.org/10.1080/10920277.2001.10595984>
- Alswaidan, A., Jin, C., Varner, J.D. "Continuous Hidden Markov Models for Equity Returns: Heavy-Tail Emission Families and Regime-Conditional Value-at-Risk." arXiv:2606.23492. <https://arxiv.org/abs/2606.23492>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
step_regime_switching(
    current_value: np.ndarray | float,
    shock: np.ndarray | float,
    mean: np.ndarray | float,
    volatility: np.ndarray | float,
) -> np.ndarray
```

**Args:**

- <u>current_value (np.ndarray &#124; float):</u> today's price in each scenario.
- <u>shock (np.ndarray &#124; float):</u> the equity's correlated standard normal shock for this step.
- <u>mean (np.ndarray &#124; float):</u> the regime's mean log-return over the step (annual mean times the step).
- <u>volatility (np.ndarray &#124; float):</u> the regime's volatility over the step (annual volatility times the square root of the step).

**Returns:**

<u>np.ndarray:</u> the price at the end of the step.

</details>
{% endraw %}
