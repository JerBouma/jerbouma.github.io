---
title: "History and Metrics"
seo_title: "History and Metrics Reference | Finance Scenarios"
seo_title_suffix: false
excerpt: "Fetch the realized history behind a run, turn it into a backtest and compute factor and price metrics."
description: "Fetch the realized history behind a run, turn it into a backtest and compute factor and price metrics."
author_profile: false
permalink: /projects/financescenarios/docs/reference/history-and-metrics
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

Fetch the realized history behind a run, turn it into a backtest and compute factor and price metrics.

```python
from financescenarios import fetch_historical_data, build_synthetic_scenario_set, compute_factor_metrics, compute_price_performance_metrics
```

## fetch_historical_data

Fetch every configured factor's raw history, without fitting anything: the same data each factor's calibration
reads.

Use it to look at the data behind a run, or to build a backtest with `build_synthetic_scenario_set()`;
`Scenarios.history()` does both in one call. Pass a toolkit made with `build_toolkit(config)`, so the downloads are
cached and a later simulation of the same config reuses them.

**As an example:**

```python
from financescenarios import build_toolkit, fetch_historical_data

# config: a ScenariosConfig, such as the one in build_synthetic_scenario_set()'s example
history = fetch_historical_data(config, build_toolkit(config))
[series.name for series in history]
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fetch_historical_data(
    config: ScenariosConfig,
    toolkit: Toolkit,
    bond_panel: BondPanel | None = None,
) -> list[HistoricalSeries]
```

**Args:**

- <u>config (ScenariosConfig):</u> the configuration naming every factor to fetch.
- <u>toolkit (Toolkit):</u> a Finance Toolkit covering the config's tickers, from `build_toolkit(config)`.
- <u>bond_panel (BondPanel &#124; None):</u> the bond data for the credit term structure factor. Defaults to None, built when that factor is enabled.

**Returns:**

<u>list[HistoricalSeries]:</u> one series per configured factor, with `name`, `category`, `dates` and `values`; the yield curve and credit term structure give one per maturity, and mortality is skipped, since it has no downloadable history.

</details>

## build_synthetic_scenario_set

Turn historical series into a one-path `ScenarioSet`, so a portfolio can be backtested with exactly the same calls
as a simulated run.

Every chosen factor is put on one calendar (`period`), taking the last value in each period, and only the dates
all factors share are kept: nothing is filled in or invented. A factor published only quarterly therefore limits a
monthly backtest to one date a quarter, so match `period` to the least frequent factor. With one path, statistics
across scenarios (percentiles, success rates) collapse to a single number, while returns, volatility and drawdowns
keep their usual meaning. `Scenarios.history()` does the fetching and this step in one call.

**As an example:**

```python
from datetime import date

from financescenarios import ScenariosConfig, build_synthetic_scenario_set, build_toolkit, fetch_historical_data
from financescenarios.config.config_model import EquityConfig, InterestRateConfig, ToolkitConfig

config = ScenariosConfig(
    start_date=date(2000, 1, 1),
    toolkit=ToolkitConfig(start_date=date(2000, 1, 1)),
    interest_rates=[InterestRateConfig(name="united_states_short_rate", country="United States", currency="USD")],
    equities=[EquityConfig(name="us_broad", ticker="SPY", currency="USD")],
)
history = fetch_historical_data(config, build_toolkit(config))
backtest = build_synthetic_scenario_set(history, ["us_broad", "united_states_short_rate"], period="monthly")
```

Which gives (on 2026-10-04) 274 monthly dates, from 2004-01-01 to 2026-10-01, the window both series cover.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
build_synthetic_scenario_set(
    series: list[HistoricalSeries],
    factor_names: list[str],
    period: str = 'monthly',
) -> ScenarioSet
```

**Args:**

- <u>series (list[HistoricalSeries]):</u> the fetched history, from `fetch_historical_data()`.
- <u>factor_names (list[str]):</u> the factors to include, such as a portfolio's holdings and its inflation factor.
- <u>period (str):</u> "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "monthly".

**Returns:**

<u>ScenarioSet:</u> one path per factor (`n_simulations=1`) on the shared dates, each labelled with the start of its period. It records each factor's category, so `Portfolio` takes it directly.

**Raises:**

- <u>KeyError:</u> if a name in `factor_names` was not fetched.
- <u>ValueError:</u> if `period` is unknown, or the factors share fewer than two dates.

</details>

## compute_factor_metrics

Compute the risk and distribution statistics of one simulated factor: Value-at-Risk, drawdowns, percentiles and
more, in one object.

Most measures look at how much the factor changed from the first to the last date, across scenarios. That works for
any factor, including ones that can turn negative such as interest rates, where a percentage return would make no
sense. The drawdown measures look at each scenario's whole path instead, since a fall from a peak needs the path's
history, not just where it ended. The calculations come from the Finance Toolkit's risk and performance functions.

Use it to check a calibration against what you expect of the asset before relying on the run: a 95% VaR of the
short rate that implies a 3-point move in a year, or an equity kurtosis near 0, says the tails are off.

**As an example:**

```python
from financescenarios import compute_factor_metrics

metrics = compute_factor_metrics(result["united_states_short_rate"])
metrics.risk.value_at_risk_historic, metrics.distribution.percentiles["95"]
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
compute_factor_metrics(paths: np.ndarray, alpha: float = DEFAULT_ALPHA) -> FactorMetrics
```

**Args:**

- <u>paths (np.ndarray):</u> one factor's simulated paths, shaped (n_simulations, n_steps + 1), e.g. `result["us_broad"]`.
- <u>alpha (float):</u> the tail level for Value-at-Risk, Conditional Value-at-Risk, the tail ratio and drawdown at risk; 0.05 (the worst 5%) by default.

**Returns:**

<u>FactorMetrics:</u> `risk` (Value-at-Risk, Conditional Value-at-Risk, drawdowns and the ratios built on them) and `distribution` (mean, standard deviation, skewness, kurtosis, percentiles and more).

**Raises:**

- <u>ValueError:</u> if `alpha` is not between 0 and 1, or `paths` is not a finite (n_simulations, n_steps + 1) array with at least two dates.

</details>

## compute_price_performance_metrics

Compute return-based performance measures for one value path, such as a portfolio's value over time: growth,
volatility, Sharpe and Sortino ratios, drawdowns and Value-at-Risk.

These measures need percentage returns, so they only make sense for a value that stays above zero, such as a
portfolio, one of its holdings or one of its percentile bands, not for a factor like an interest rate that can cross
zero (use `compute_factor_metrics` for that). Ratios are annualized from the spacing of `time_grid`. The
Value-at-Risk measures here are the tail of one path's own period returns, not the spread across scenarios: they
describe how rough a single scenario's ride is, while the spread across scenarios says how uncertain the outcome
is. The calculations come from the Finance Toolkit's performance and risk functions. With V the value, T the years,
r the return per step, r_f the annual risk-free rate and m the steps per year:

The formula is as follows:
- CAGR = (V_T / V_0)^(1 / T) - 1
- Sharpe = mean(r - r_f / m) / std(r - r_f / m) * sqrt(m)

**As an example:**

```python
from financescenarios import compute_price_performance_metrics

metrics = compute_price_performance_metrics(result["us_broad"][0], result.time_grid, risk_free_rate=0.04)
metrics.cagr, metrics.sharpe_ratio, metrics.max_drawdown_pct
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
compute_price_performance_metrics(
    values: np.ndarray,
    time_grid: np.ndarray,
    risk_free_rate: float = 0.0,
    alpha: float = DEFAULT_ALPHA,
) -> PricePerformanceMetrics
```

**Args:**

- <u>values (np.ndarray):</u> one value path over time, shaped (n_steps + 1,), e.g. one scenario or a percentile band.
- <u>time_grid (np.ndarray):</u> the matching times in years from the start, evenly spaced, e.g. `result.time_grid`.
- <u>risk_free_rate (float):</u> the annual risk-free rate taken off the return in the Sharpe, Sortino, Kappa and STARR ratios; 0.0 by default.
- <u>alpha (float):</u> the tail level for Value-at-Risk, Conditional Value-at-Risk, the tail ratio, drawdown at risk and the Rachev ratio; 0.05 (the worst 5%) by default.

**Returns:**

<u>PricePerformanceMetrics:</u> `cagr`, `annualized_volatility`, `sharpe_ratio`, `sortino_ratio`, `max_drawdown_pct`, `calmar_ratio` and the other ratio, drawdown and Value-at-Risk measures. Every field is NaN when the path starts at or below zero or has a single date; a single ratio is NaN when it would divide by zero, e.g. `calmar_ratio` on a path that never falls.

**Raises:**

- <u>ValueError:</u> if `alpha` is not between 0 and 1, `values` is not one path as long as `time_grid`, or `risk_free_rate` is not finite.

</details>
