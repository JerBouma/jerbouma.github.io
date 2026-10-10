---
title: Plotting
seo_title: Plotting Documentation – Finance Scenarios
excerpt: "Every result has a .plot() that draws it in one line: a fan chart of where each variable is likely to go, its individual scenarios, or where it ends up."
description: "Charts in Finance Scenarios: the one-line .plot() on every result, fan charts, paths, terminal distributions, portfolio views and the shared style."
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

Every result has a `.plot()` that draws it in one line: a fan chart of where each variable is likely to go, its individual scenarios, or where it ends up. The charts are meant for a quick look, not as a reporting tool, and come with every install.

The `_view` modules are this project's third MVC leg: a `_model.py` computes, a `_controller.py` orchestrates, and a `_view.py` only draws what a model object already holds: pure matplotlib rendering, no calculation beyond percentiles, no I/O, no FinanceToolkit. matplotlib is loaded only when a chart is drawn, so `import financescenarios` stays fast. Every function returns the `matplotlib.figure.Figure`, and the single-panel ones take an `ax=` to draw into an existing grid.

Plotting is meant for a quick, simple read rather than as a reporting tool, so the everyday entry point is one method with a few arguments, on every result:

```python
result.plot()                                   # every factor, one fan chart each
result.plot("us_broad")                         # one factor's percentile fan
result.plot(["us_broad", "gold"])               # a chosen few, as a grid
result.plot("us_broad", kind="paths")           # its individual simulated paths
result.plot("us_broad", kind="distribution")    # where it lands at the horizon
result.plot("us_broad", levels=True)            # in prices rather than returns
result.plot("united_states_inflation", metric="level")  # inflation as a price index from 100

values.plot()                                   # a computed portfolio's value
values.plot(kind="sleeves")                     # and its composition over time
calibration.plot()                              # the calibrated correlation matrix
```

`kind="paths"` and `kind="distribution"` draw one factor; a list of factors is always a grid of fan charts. The `plot_*` methods and functions below remain for finer control (band choice, bin count, path sampling, a seed), and every one returns the `Figure`.

```python
from financescenarios import Scenarios

scenarios = Scenarios.from_profiles(settings="default", factor_set="us_only")
result = scenarios.simulate()

result.plot_fan_chart("us_broad")             # quantile bands around the median path
result.plot_paths("us_broad")                 # every simulated path, or n_paths= for a sample
result.plot_terminal_distribution("us_broad") # where the final step lands, across simulations
result.plot_factors()                         # one fan chart per factor, small-multiples grid

scenarios.last_calibration.plot_correlation_matrix()
```

The same views are importable as plain functions (`from financescenarios import plot_fan_chart, ...`) for composing into your own figure grids via their `ax=` argument; the methods above are thin delegations to them, importing matplotlib only at call time so `import financescenarios` stays fast.

A computed portfolio is itself a `ScenarioSet`, so the same fan chart reads it, plus two portfolio-specific views:

```python
from financescenarios import Portfolio

portfolio = Portfolio.from_preset(result, preset="balanced_60_40", config=scenarios.config)
computed = portfolio.compute()

computed.plot_fan_chart("portfolio")                         # the portfolio value's own fan

from financescenarios import plot_sleeve_values, plot_weight_drift
plot_sleeve_values(computed)                                 # median dollar value per sleeve, stacked
plot_weight_drift(computed, portfolio.weight_drift(computed))  # actual minus target weight per sleeve
```

## What each view is for

| Function | Reads | The question it answers |
|---|---|---|
| `result.plot_fan_chart(factor)` | any simulated factor (or `"portfolio"`) | Where does the distribution sit over time? |
| `result.plot_paths(factor)` | every path, or an `n_paths` sample | How jagged is any one scenario? (the texture the fan smooths away) |
| `result.plot_terminal_distribution(factor)` | the final step, across simulations | Where does this land, and how fat are the tails? |
| `result.plot_factors()` | every factor | The whole run at a glance, one panel per factor |
| `calibration.plot_correlation_matrix()` | `CalibrationResult` | What co-moves with what, and in which direction? |
| `plot_runs({name: run}, factor)` | several runs | The same factor in a baseline and its stress regimes, side by side on one scale |
| `solvency.plot(cashflows, assets)` | a `Solvency` | Where own funds could be after one year, with today's level and the 1-in-200 outcome (the SCR) marked |
| `plot_sleeve_values(computed)` | a `Portfolio.compute()` result | How does the composition actually evolve? |
| `plot_weight_drift(computed, drift)` | `Portfolio.weight_drift()` | How far has the allocation wandered from target? |

## The shared style

`engine/engine_view.py` hosts the one chart style every view uses (`apply_chart_style` plus the palette constants); restyling it restyles every figure the package produces. The palette is a validated colorblind-safe set with three fixed roles:

- **Categorical** (`CATEGORICAL_COLORS`): eight hues in a fixed slot order for identity (portfolio sleeves). The ordering is the colorblind-safety mechanism, so slots are assigned in order and never cycled; past eight sleeves, the rest fold into one gray "Other" band rather than inventing a ninth hue.
- **Sequential**: one blue ramp light-to-dark for nested magnitude (a fan chart's outer band, inner band, median line).
- **Diverging**: blue and red poles around a neutral gray midpoint for polarity (the correlation heatmap, fixed to the [-1, 1] domain so two runs' matrices are directly comparable).

Every chart keeps one y-axis (a rate and a price level never share one; `plot_factors` gives each panel its own scale instead), grids stay recessive behind the data, and identity is never carried by color alone (legends plus per-cell annotations where numbers matter).

## Reading the axes

Every factor is drawn in the reading the rest of the package reports (see [units](/projects/financescenarios/docs/units)): by default a rate-type factor as its rate, a price (an equity, commodity or FX price, a dividend index, a portfolio value) as its annualized return since start, and the leading indicator as its index level. Rates, changes and returns read as percentages (`3.5%`, `9.5%`). Every chart takes `metric=` for another reading (`"level"`, `"change"`, `"yoy"`, `"cumulative"`, `"annualized"`, `"rate"`), named in the subtitle (`year-over-year return`, `index, 100 at start`), and `levels=True` for the native value; prices and index levels read with thousands separators (`4,544`).

An annualized return is extremely wide over the first months, so on a return chart the y-scale is fitted from the first year on and those early swings run off the top rather than flattening the rest of the fan. A hand-built `ScenarioSet` without categories keeps plain numbers rather than risk mislabelling a level as a percentage.

The terminal distribution scales its bin count to the run (about `2 * sqrt(n_simulations)`, between 10 and 40) unless `bins=` is given, and marks its percentiles with the same formatting (`5th pct: -1.9%`), labels are the run's display names rather than slugs (`US Broad`, not `us_broad`), and a fan chart's subtitle says in words what its shading is (`median, shaded 50% and 90% ranges`), once per grid in `plot_factors`.

`plot_paths` draws every simulation as one `LineCollection` with an opacity scaled to the path count, so 2,000 paths render in about two seconds and still read as a cloud with visible tails rather than a solid block; the median sits on top with a light halo. The correlation heatmap writes each value into its cell, since color alone cannot carry a two-decimal reading. Above 14 factors the numbers stop being readable, so only the colors are drawn unless you pass `annotate=True`; in deeply colored cells the text turns white. `plot_correlation_matrix` takes `labels=` for custom axis names and `ax=` to draw into your own grid, like every other view.
