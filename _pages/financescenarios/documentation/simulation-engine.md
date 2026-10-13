---
title: Simulation Engine
seo_title: Simulation Engine Documentation – Finance Scenarios
excerpt: "How the correlated shocks are drawn, how each factor steps forward one time step at a time, and the ScenarioSet result with its methods to summarize, slice, filter and save a run."
description: "How the Finance Scenarios Monte Carlo engine draws correlated shocks, steps every factor forward and returns a ScenarioSet to summarize and filter."
author_profile: false
permalink: /projects/financescenarios/docs/simulation-engine
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

{% include mermaid.html %}

The engine produces the scenarios. It draws random shocks that move together the way history says they should, then steps every variable forward one month (or week, or year) at a time, thousands of times over. Each run of that process is a path; together they form a distribution of outcomes rather than a single forecast. The result is a `ScenarioSet`, with methods to summarize, slice, filter and chart it.

This page covers what every factor shares. How each area is modelled is in the guides on [interest rates](/projects/financescenarios/docs/interest-rates), [the KNW model](/projects/financescenarios/docs/knw), [the economy](/projects/financescenarios/docs/economy) and [markets](/projects/financescenarios/docs/markets); what to do with a finished run is in [portfolios](/projects/financescenarios/docs/portfolio) and [Solvency II](/projects/financescenarios/docs/solvency).

## Engine Settings

The `engine` section of a settings profile (see [configuration](/projects/financescenarios/docs/configuration)):

| Field | Default | What it does |
|---|---|---|
| `n_simulations` | `1000` | Number of scenarios. |
| `n_steps` | `52` | Number of steps after the start. `simulate(years=30)` sets it from a horizon instead. |
| `frequency` | `weekly` | Length of a step: `daily`, `weekly`, `monthly`, `quarterly`, `semi-yearly` or `yearly`. |
| `seed` | `null` | Fix it and the same inputs always give exactly the same output. |
| `antithetic` | `false` | Pair every shock with its mirror image, which reduces Monte Carlo noise; `n_simulations` must be even. On the default factor set it cut the seed-to-seed spread of a 60/40 portfolio's five-year 5th percentile by about a quarter. |
| `shock_distribution` | `gaussian` | `student_t` for fat tails, see below. |
| `degrees_of_freedom` | `5.0` | Tail weight for `student_t`: lower means fatter tails. Must be above 2. |
| `correlation_shrinkage` | `0.1` | How far correlations are pulled in to tame noise; `auto` picks the amount from the data ([Schäfer and Strimmer, 2005](https://doi.org/10.2202/1544-6115.1175)). The shipped settings use `auto`. |
| `correlation_method` | `pairwise` | Which history each correlation is estimated from, see below. |
| `shared_equity_regimes` | `false` | Let all equity markets enter and leave crises together. The shipped settings set it to `true`, which brings simulated equity correlations much closer to the fitted ones. |

## How a Run Is Built

{% raw %}
<div class="mermaid">
flowchart TD
    start[Simulation start] --> timegrid[Build time grid and date grid]
    timegrid --> shocks[Draw correlated shocks]
    shocks --> order[Order the factors by their dependencies]
    order --> loop[Step every factor forward one time step at a time]
    loop --> loop
    loop --> scenarioset[Wrap the result into a ScenarioSet]
</div>
{% endraw %}

1. **Time grid.** The steps from the start date, in years and as calendar dates.
2. **Correlated shocks.** Independent random draws, one per factor, step and scenario, are made to move together with a Cholesky decomposition of the correlation matrix. That is what makes rates, inflation and equities move together realistically.
3. **Equity regimes.** Which market regime (calm or crisis) each equity is in at every step is drawn upfront, from its own random stream.
4. **Stepping.** Factors are ordered so each comes after the factors it depends on (unemployment after inflation, for example), then every factor moves one step at a time for all scenarios at once.

Most factors mean-revert (an Ornstein-Uhlenbeck process) and are stepped with the exact solution of that process, so the step length causes no error and long steps stay stable. The formula is as follows:

$$
x_{t+\Delta t} = \theta + (x_t - \theta)\, e^{-a \Delta t} + \sigma \sqrt{\frac{1 - e^{-2 a \Delta t}}{2a}}\; \varepsilon_t
$$

where $$\theta$$ is the long-run level, $$a$$ the speed of mean reversion, $$\sigma$$ the volatility and $$\varepsilon_t$$ the correlated shock. CIR rates, GARCH factors, equities, FX, commodities and dividend yields use the standard Euler step of their own equation.

## Fat Tails {#fat-tails-and-tail-dependence}

Normally distributed shocks rarely produce extreme moves in several factors at once, while "everything sells off together" is exactly what a stress test is for. `shock_distribution: student_t` uses a Student-t copula instead (Demarta and McNeil, 2005): at each step every factor's shock is divided by the same random scale, so extreme moves cluster across factors. Shocks keep unit variance, so every fitted volatility means the same thing either way; only the tails change.

```yaml
engine:
  shock_distribution: student_t
  degrees_of_freedom: 5.0
```

## How the Correlations Are Estimated

Every factor gets a row and a column in the correlation matrix, estimated from the same historical changes the factor was fitted on (changes in a rate, log returns of a price), so nothing extra is downloaded.

- **Mixed frequencies.** Changes are summed up to the coarser frequency and matched on calendar date, the way twelve monthly log returns add up to a yearly one.
- **Pairwise or one window.** With `pairwise` (the default) each pair uses the dates those two factors share, so a short series only weakens its own pairs. Fewer than 5 shared observations sets the pair to 0 and lists it in `correlation_fallback_pairs`. `complete_case` cuts every factor to one common window instead.
- **Shrinkage.** Correlations are pulled toward a simpler target to trade a little bias for much less noise ([Ledoit and Wolf, 2004](http://www.ledoit.net/Honey_2004.pdf){:target="_blank"}).
- **Repair.** A matrix built from different windows can be inconsistent; it is moved to the nearest valid one ([Higham, 2002](https://doi.org/10.1093/imanum/22.3.329){:target="_blank"}) and the size of the repair is recorded as `correlation_repair`.
- **Warnings.** Pairs with fewer than 12 shared observations, or correlated above 0.98 (usually the same ticker configured twice), are flagged.

The matrix is linear and constant over the horizon.

## The ScenarioSet {#scenarioset}

`simulate()` returns a `ScenarioSet`. By default a rate reads as its annualized rate and a price (equities, FX, commodities, portfolios) as its annualized return since the start; every method takes `metric=` for another reading and `levels=True` for the raw simulated values. See [units](/projects/financescenarios/docs/units).

```python
result = scenarios.simulate()

result.summary_statistics("inflation")          # mean, std, se and quantiles per date
result.horizon_summary([1, 5, 10])              # where each factor is in 1, 5 and 10 years
result.to_dataframe("us_broad")                 # one row per scenario, one column per date
result.discount_factors("united_states_short_rate")
```

| Method | What it gives |
|---|---|
| `summary_statistics(factor)` | Mean, standard deviation, standard error and quantiles at every date. The standard error tells you whether `n_simulations` is enough. |
| `horizon_summary(horizons)` | One row per factor and horizon. |
| `to_dataframe(factor)`, `to_long()` | A scenario-by-date table, or every path in long format for databases. |
| `discount_factors(factor)`, `cumulative_index(factor)` | A rate compounded into discount factors or an index. For a full deflator with a market price of risk, see `KnwSvQ.deflator()`. |
| `result[factor]`, `step_at(years)` | The raw array, and the step nearest a horizon. |
| `select(factors)`, `sample(n)` | A subset of factors, or `n` whole scenarios with their correlations intact. |
| `simulated_correlation()` | The correlation of the simulated moves, to compare with the fitted one (`calibration.correlation_frame()`). |
| `diagnose()` | Checks each mean-reverting factor's simulated end distribution against its theoretical long-run mean and spread. It also runs automatically when the horizon is long enough. |

`compare_runs({"baseline": base, "oil_crisis": shocked})` puts several runs side by side on one end-of-run statistic, as in the [README](/projects/financescenarios#applying-stress-regimes)'s stress-regime table.

## Filtering and Narratives

`filter()` keeps the scenarios in a quantile band of one factor, for example the 30% with the highest average interest rate. Each kept scenario keeps all its other factors too, so the correlations survive:

```python
high_rates = result.filter("interest_rate", quantile_range=(0.7, 1.0))
```

`filter_narrative()` chains several of these into a story such as stagflation:

```python
stagflation = result.filter_narrative(
    {
        "inflation": (0.8, 1.0),   # top 20% by average inflation
        "equity": (0.0, 0.2),      # bottom 20% by equity return
    }
)
```

By default each range applies to what the previous one left; `mode="joint"` ranks every target against the full run instead. A warning appears below 30 remaining scenarios; [regimes](/projects/financescenarios/docs/regimes#driving-a-regime-from-the-library) show how to keep a fixed number.

`rescale_scenario_cloud(factor, mean_shift=0.0, spread_multiplier=1.0)` reshapes one factor's simulated cloud afterwards: shift its mean or widen its spread at every date, without refitting.

```python
wider_equity = result.rescale_scenario_cloud("equity", spread_multiplier=1.3)
```

## Risk Metrics for a Factor

- `compute_factor_metrics(result["united_states_short_rate"])` describes one factor across scenarios: Value-at-Risk, Conditional Value-at-Risk, percentiles, skewness and drawdowns.
- `compute_price_performance_metrics(values, result.time_grid)` describes one value path over time, such as a portfolio or a percentile band: growth, volatility, Sharpe and Sortino ratios, drawdowns.

The first function's Value-at-Risk is the tail across scenarios at the end; the second's is the tail of one path's own returns. Portfolio metrics are in [portfolios](/projects/financescenarios/docs/portfolio).

## Saving and Replaying a Run

`simulate()` fits and simulates in one call. Split the two to reproduce a run exactly, work offline or re-simulate cheaply:

```python
calibration = scenarios.calibrate()
calibration.save("calibration.json")

spread = [scenarios.simulate(calibration=calibration, seed=seed) for seed in range(5)]
wider = scenarios.simulate(calibration=calibration, n_simulations=20_000)
```

A supplied calibration is used as is: nothing is downloaded, so it also works with `Scenarios(toolkit=None)` and no API key. `scenarios.last_calibration` holds the one the latest run used. A calibration refuses a configuration whose fixed beliefs differ from the ones it was fitted with; recalibrate for those.

`scenarios.save(result, "results/")` writes the paths (Parquet), the configuration and the calibration to one folder, so the run reads back and replays without network access:

```python
from financescenarios import read_run, read_run_calibration

same = read_run(path)
calibration = read_run_calibration(path)
```

A factor that fails to fit (for example, no mean reversion in a short window) is left out together with the factors that depend on it, and the reason is recorded in `calibration_failures`, also in a saved run's manifest.
