---
title: Plotting
seo_title: Plotting Documentation – Finance Scenarios
excerpt: "What each chart tells you and how to read it: fan charts, individual paths, the distribution at the horizon, the correlation matrix and stress runs side by side."
description: "How to read Finance Scenarios charts: fan charts, individual paths, the distribution at the horizon, the correlation matrix and stress runs side by side."
author_profile: false
permalink: /projects/financescenarios/docs/plotting
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

Which chart answers which question about a run: where the distribution sits over time, what a single future looks like, where it lands and what moves with what. The charts are for a quick read, not a reporting tool. Options such as bands and bin counts are in the [reference](/projects/financescenarios/docs/reference/charts).

```python
from financescenarios import Scenarios

scenarios = Scenarios.from_profiles(settings="default", factor_set="us_only")
result = scenarios.simulate()

result.plot()   # one fan chart per factor, the whole run at a glance
```

Every chart uses the readings described under [units](/projects/financescenarios/docs/units): a rate as its rate, a price as its annualized return since the start, both as percentages. Other readings, or the price itself, are available too.

## Fan Chart: Where the Distribution Sits Over Time

The dark line is the median scenario, the darker band holds the middle 50% of scenarios and the lighter band 90% (the 5th to 95th percentile). Read it for three things: where the median drifts (mean reversion toward a long-run level, or a trend), how fast the bands widen (volatility), and whether they widen evenly (skew: a band that stretches more on one side means the risk sits there).

A fan for a rate that mean-reverts stops widening after a few years, because shocks fade. A fan for a cumulative return keeps widening. On an annualized return the fan narrows with the horizon instead, as good and bad years average out; its first months are cut off the scale because a few weeks' move scaled up to a year swamps the rest.

```python
result.plot("us_broad")                             # annualized return since start
result.plot("us_broad", levels=True)                # the price itself
result.plot("united_states_inflation", metric="level")  # inflation as a price index from 100
```

## Paths: What a Single Future Looks Like

A fan chart smooths away how jagged any one scenario is. The paths view draws every scenario faintly with the median on top, so you see the texture: regime switches, crashes and recoveries, rates lingering at zero, a few extreme paths that drive the tail. Check it whenever a model produces something the fan can't show, such as jumps or a floor.

```python
result.plot("us_broad", kind="paths")
result.plot_paths("us_broad", n_paths=50)   # a sample, to follow individual paths
```

## Distribution: Where It Lands

A histogram of the value at the horizon across all scenarios, with the 5th, 50th and 95th percentiles marked. This is where tail questions start: how far the 5th percentile sits from the median, whether the distribution is skewed, how fat the tails are. For a price it shows the annualized return over the whole horizon.

```python
result.plot("us_broad", kind="distribution")
```

## Correlation Matrix: What Moves with What

A heatmap of the fitted correlations. Read it for the diversification the scenarios assume: whether equities and bonds hedge each other, whether currencies offset equity losses, which factors are near duplicates. The correlations are constant over the horizon; dependence that rises in a crisis comes from shared regimes and fat tails instead (see the [simulation engine](/projects/financescenarios/docs/simulation-engine)).

```python
scenarios.last_calibration.plot()
```

## Comparing Runs

The same factor in a baseline and its stress runs, one fan chart each on a shared scale, so a shift in the median or a wider band stands out.

```python
from financescenarios import plot_runs

stressed = scenarios.simulate(regime="oil_crisis")
plot_runs({"baseline": result, "oil crisis": stressed}, "us_broad")
```

## Portfolios and Solvency

A computed portfolio is drawn the same way: its value as a fan chart, and its holdings over time to see how the allocation drifts between rebalancing dates. The [Solvency II](/projects/financescenarios/docs/solvency) guide draws own funds after one year with today's level and the 1-in-200 outcome (the SCR) marked.

```python
from financescenarios import Portfolio

portfolio = Portfolio.from_preset(result, preset="balanced_60_40", config=scenarios.config)
values = portfolio.compute()

values.plot()                 # the portfolio value's fan chart
values.plot(kind="sleeves")   # what each holding is worth over time
```

Several presets computed together share one chart instead, a line per portfolio on one axis, so the gap between two lines is the difference an investor would have seen. On simulated scenarios each line is the median, with the middle half of the scenarios shaded in its color; on a backtest it is the realized value.

```python
presets = Portfolio.from_preset(result, preset=["balanced_60_40", "all_weather"], config=scenarios.config)
presets.compute().plot(levels=True)   # one line per preset, in money
```
