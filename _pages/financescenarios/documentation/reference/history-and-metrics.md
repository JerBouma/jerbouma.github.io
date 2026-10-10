---
title: "History and Metrics"
seo_title: "History and Metrics Reference – Finance Scenarios"
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

Fetch the realized history behind a run, turn it into a backtest and compute factor and price metrics. Generated from the docstrings of Finance Scenarios 0.1.0; `help(...)` in Python shows the same text.

```python
from financescenarios import fetch_historical_data, build_synthetic_scenario_set, compute_factor_metrics, compute_price_performance_metrics
```

## fetch_historical_data

```python
fetch_historical_data(
    config: ScenariosConfig,
    toolkit: Toolkit,
    bond_panel: BondPanel | None = None,
) -> list[HistoricalSeries]
```

Fetch every configured factor's raw historical series, unfitted: the same
Finance Toolkit (or, for credit_term_structure, BondPanel) call each factor's
own `calibrate()` makes, without the calibration itself. Pass a `toolkit`
built via `scenarios_controller.build_toolkit(config)` so this shares (and
warms) the exact cache a subsequent `Scenarios.simulate(config)` call hits.

**Args:**

- <u>config (ScenariosConfig):</u> the configuration naming every factor to fetch.
- <u>toolkit (Toolkit):</u> a Finance Toolkit instance covering config's tickers; see `scenarios_controller.build_toolkit()`.
- <u>bond_panel (BondPanel &#124; None):</u> the credit_term_structure factor's data source, injectable the same way `Scenarios.from_config()`'s own `bond_panel` is (e.g. a fake/pre-cached instance in tests). Built fresh on first use if omitted and `config.credit_term_structure.enabled`.

**Returns:**

<u>list[HistoricalSeries]:</u> one entry per configured factor entry, except yield_curve/credit_term_structure (one per tenor) and mortality (skipped entirely: no Finance Toolkit-backed fetch, caller-supplied data).

## build_synthetic_scenario_set

```python
build_synthetic_scenario_set(
    series: list[HistoricalSeries],
    factor_names: list[str],
    period: str = 'monthly',
) -> ScenarioSet
```

Build a single-path (n_simulations=1) ScenarioSet from raw historical series, so
financescenarios.portfolio can run its rebalance/cashflow/fee engine against
realized history the same way it runs against a simulated run.

**Args:**

- <u>series (list[HistoricalSeries]):</u> every fetched factor (see historical_data_controller.fetch_historical_data); only the entries named in factor_names are used.
- <u>factor_names (list[str]):</u> the factors to include (a portfolio's sleeves, plus inflation_factor if used); every name must have a matching entry in series.
- <u>period (str):</u> the common calendar every factor is resampled onto: "daily", "weekly", "monthly" (default), "quarterly", or "yearly". Each factor is downsampled to this cadence by taking each bucket's last observation; a factor whose own native frequency is coarser than `period` has no value in the buckets between its prints, which drops those buckets out of the final intersection rather than forward-filling a stale value into them.

**Returns:**

<u>ScenarioSet:</u> paths shaped (1, n_steps + 1), dates the intersection of every requested factor's own resampled observations. Each date is a bucket-start label (e.g. the 1st of the month at period="monthly"), not the actual date its own last observation came from; see this module's own docstring for why. `factor_categories` is filled in from each series' own category, so `Portfolio` takes the result directly; calibration_metadata empty, seed None.

**Raises:**

- <u>KeyError:</u> if factor_names names a factor missing from series.
- <u>ValueError:</u> if period isn't recognized, or the requested factors' resampled observations don't overlap enough to build at least two aligned points.

## compute_factor_metrics

```python
compute_factor_metrics(paths: np.ndarray, alpha: float = DEFAULT_ALPHA) -> FactorMetrics
```

**Args:**

- <u>paths (np.ndarray):</u> one factor's simulated paths, shape (n_simulations, n_steps + 1), i.e. ScenarioSet.paths[factor_name].
- <u>alpha (float):</u> VaR/CVaR/tail-ratio/CDaR confidence level (0.05 = 95%).

**Returns:**

<u>FactorMetrics:</u> this factor's risk metrics and distribution statistics; see FactorMetrics' docstring for which axis each field uses.

## compute_price_performance_metrics

```python
compute_price_performance_metrics(
    values: np.ndarray,
    time_grid: np.ndarray,
    risk_free_rate: float = 0.0,
    alpha: float = DEFAULT_ALPHA,
) -> PricePerformanceMetrics
```

The return-based axis, distinct from the level-change metrics above: a strictly positive
price path has well-defined percentage returns, which unlocks the Sharpe/Sortino/Calmar
family that a signed level change cannot support.

**Args:**

- <u>values (np.ndarray):</u> shape (n_steps + 1,), one price-level track over time; must be strictly positive (a portfolio/sleeve dollar value, e.g. one of `FactorResult`'s own mean/q05/q25/q75/q95 bands), never a generic factor's level or level change.
- <u>time_grid (np.ndarray):</u> shape (n_steps + 1,), years from t0, same as `ScenarioSet.time_grid`; assumed uniformly spaced (as `build_time_grid` always produces), used to annualize.
- <u>risk_free_rate (float):</u> annual risk-free rate subtracted from the annualized return before Sharpe/Sortino/Kappa/STARR.
- <u>alpha (float):</u> VaR/CVaR/tail-ratio/CDaR/Rachev confidence level (0.05 = 95%), applied to the band's own period-return series.

**Returns:**

<u>PricePerformanceMetrics:</u> all-NaN if `values[0] <= 0` (the path never had a meaningful positive starting value to compound from, e.g. a glidepath sleeve with 0 weight at t=0) or if there are fewer than 2 time points to derive a period return from. Individual fields (not the whole result) can independently come back NaN on a valid path too, e.g. `calmar_ratio` when `max_drawdown_pct` is exactly 0 (a monotonically non-decreasing path), the same "well-defined but undefined here" NaN-on-a-zero-denominator pattern the cross-sectional `RiskMetrics` already uses.
