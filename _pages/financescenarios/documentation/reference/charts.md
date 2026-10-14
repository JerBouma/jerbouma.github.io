---
title: "Charts"
seo_title: "Charts Reference – Finance Scenarios"
excerpt: "The chart functions behind every .plot(): fan charts, paths, terminal distributions, runs and portfolios."
description: "The chart functions behind every .plot(): fan charts, paths, terminal distributions, runs and portfolios."
author_profile: false
permalink: /projects/financescenarios/docs/reference/charts
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

The chart functions behind every `.plot()`: fan charts, paths, terminal distributions, runs and portfolios.

```python
from financescenarios import plot_factors, plot_fan_chart, plot_paths, plot_terminal_distribution, plot_runs, plot_portfolios, plot_correlation_matrix, plot_sleeve_values, plot_weight_drift
```

## plot_factors

Draw a grid with one fan chart per factor, each on its own scale.

The quickest look at a whole run: by default every factor, in the run's own order. A rate and a price never share
an axis, so each panel scales to its own factor. Several portfolios of one `Portfolio.compute()` are the exception:
they share one chart, one line each, so they compare on the same scale.

**As an example:**

```python
from financescenarios import plot_factors

plot_factors(result, ["united_states_short_rate", "united_states_inflation", "us_broad"])
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
plot_factors(
    scenario_set: ScenarioSet,
    factors: Sequence[str] | None = None,
    n_columns: int = 3,
    quantile_bands: Sequence[tuple[float, float]] = ((0.05, 0.95), (0.25, 0.75)),
    levels: bool = False,
    metric: Metric | None = None,
) -> 'Figure'
```

**Args:**

- <u>scenario_set (ScenarioSet):</u> the run to draw from.
- <u>factors (Sequence[str] &#124; None):</u> the factors to draw. Defaults to None, every factor.
- <u>n_columns (int):</u> panels per row. Defaults to 3.
- <u>quantile_bands (Sequence[tuple[float, float]]):</u> the bands each panel shades, as in `plot_fan_chart`. Defaults to ((0.05, 0.95), (0.25, 0.75)).
- <u>levels (bool):</u> draw prices as levels instead of yearly returns since the start. Defaults to False.
- <u>metric (str &#124; None):</u> the reading (see `ScenarioSet.metric_paths`). Defaults to None, each factor's default.

**Returns:**

<u>matplotlib.figure.Figure:</u> the figure holding the grid.

**Raises:**

- <u>KeyError:</u> if a named factor is not in the run.
- <u>ValueError:</u> if `n_columns` is below 1.

</details>

## plot_fan_chart

Draw one factor's fan chart: the median path with shaded bands around it.

This is the headline picture of a simulated factor. With the default bands, the darker inner band holds the middle
half of the scenarios, the lighter outer band nine in ten, and the dark line is the median. Rates and returns are
drawn as percentages, prices and values in their own units.

**As an example:**

```python
from financescenarios import plot_fan_chart

plot_fan_chart(result, "us_broad")
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
plot_fan_chart(
    scenario_set: ScenarioSet,
    factor: str,
    quantile_bands: Sequence[tuple[float, float]] = ((0.05, 0.95), (0.25, 0.75)),
    ax: 'Axes | None' = None,
    subtitle: str | None = None,
    levels: bool = False,
    metric: Metric | None = None,
) -> 'Figure'
```

**Args:**

- <u>scenario_set (ScenarioSet):</u> the run to draw from.
- <u>factor (str):</u> the factor to draw, including a computed portfolio's "portfolio".
- <u>quantile_bands (Sequence[tuple[float, float]]):</u> (lower, upper) quantile pairs, outermost first. Defaults to ((0.05, 0.95), (0.25, 0.75)).
- <u>ax (Axes &#124; None):</u> an existing matplotlib Axes to draw into. Defaults to None, a new figure.
- <u>subtitle (str &#124; None):</u> replaces the default subtitle (the qualifier, bands and scenario count). Defaults to None.
- <u>levels (bool):</u> draw a price's level instead of its yearly return since the start. Defaults to False.
- <u>metric (str &#124; None):</u> the reading (see `ScenarioSet.metric_paths`). Defaults to None, the factor's default.

**Returns:**

<u>matplotlib.figure.Figure:</u> the figure holding the chart.

**Raises:**

- <u>KeyError:</u> if the run has no such factor.
- <u>ValueError:</u> if a band's lower quantile is not below its upper one.

</details>

## plot_paths

Draw a factor's individual simulated paths, with the median on top.

A fan chart shows the spread but smooths away how jagged any single future is; this shows the paths themselves.
Lines grow fainter as more are drawn, so thousands of paths stay readable.

**As an example:**

```python
from financescenarios import plot_paths

plot_paths(result, "us_broad", n_paths=200, seed=1)
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
plot_paths(
    scenario_set: ScenarioSet,
    factor: str,
    n_paths: int | None = None,
    seed: int | None = None,
    ax: 'Axes | None' = None,
    levels: bool = False,
    metric: Metric | None = None,
) -> 'Figure'
```

**Args:**

- <u>scenario_set (ScenarioSet):</u> the run to draw from.
- <u>factor (str):</u> the factor to draw.
- <u>n_paths (int &#124; None):</u> how many paths to draw, picked at random. Defaults to None, every path.
- <u>seed (int &#124; None):</u> the random seed for that pick, for a repeatable chart. Defaults to None.
- <u>ax (Axes &#124; None):</u> an existing matplotlib Axes to draw into. Defaults to None, a new figure.
- <u>levels (bool):</u> draw a price's level instead of its yearly return since the start. Defaults to False.
- <u>metric (str &#124; None):</u> the reading (see `ScenarioSet.metric_paths`). Defaults to None, the factor's default.

**Returns:**

<u>matplotlib.figure.Figure:</u> the figure holding the chart.

**Raises:**

- <u>KeyError:</u> if the run has no such factor.
- <u>ValueError:</u> if `n_paths` is below 1.

</details>

## plot_terminal_distribution

Draw a histogram of where one factor ends up at the horizon, with chosen percentiles marked.

This is the "where does it land" chart every tail-risk question starts from. A price is shown as its yearly return
over the whole horizon, and each marked percentile carries its value as a label.

**As an example:**

```python
from financescenarios import plot_terminal_distribution

plot_terminal_distribution(result, "us_broad")
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
plot_terminal_distribution(
    scenario_set: ScenarioSet,
    factor: str,
    bins: int | None = None,
    quantiles: Sequence[float] = (0.05, 0.5, 0.95),
    ax: 'Axes | None' = None,
    levels: bool = False,
    metric: Metric | None = None,
) -> 'Figure'
```

**Args:**

- <u>scenario_set (ScenarioSet):</u> the run to draw from.
- <u>factor (str):</u> the factor to draw.
- <u>bins (int &#124; None):</u> the number of bars. Defaults to None, about 2 x the square root of the number of scenarios, between 10 and 40.
- <u>quantiles (Sequence[float]):</u> the quantiles to mark with a line. Defaults to (0.05, 0.5, 0.95).
- <u>ax (Axes &#124; None):</u> an existing matplotlib Axes to draw into. Defaults to None, a new figure.
- <u>levels (bool):</u> show a price's final level instead of its yearly return. Defaults to False.
- <u>metric (str &#124; None):</u> the reading (see `ScenarioSet.metric_paths`). Defaults to None, the factor's default.

**Returns:**

<u>matplotlib.figure.Figure:</u> the figure holding the chart.

**Raises:**

- <u>KeyError:</u> if the run has no such factor.

</details>

## plot_runs

Draw the same factor across several runs, one fan chart per run on a shared scale.

This puts a baseline and its stress regimes side by side, the chart that goes with `compare_runs`.

**As an example:**

```python
from financescenarios import plot_runs

plot_runs({"baseline": result, "oil_crisis": oil_crisis}, "united_states_inflation")
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
plot_runs(
    runs: Mapping[str, ScenarioSet],
    factor: str,
    n_columns: int = 2,
    quantile_bands: Sequence[tuple[float, float]] = ((0.05, 0.95), (0.25, 0.75)),
    levels: bool = False,
    metric: Metric | None = None,
) -> 'Figure'
```

**Args:**

- <u>runs (Mapping[str, ScenarioSet]):</u> run name -> run, drawn in that order, e.g. {"baseline": result, ...}.
- <u>factor (str):</u> the factor to compare; every run must simulate it.
- <u>n_columns (int):</u> panels per row. Defaults to 2.
- <u>quantile_bands (Sequence[tuple[float, float]]):</u> the bands each panel shades, as in `plot_fan_chart`. Defaults to ((0.05, 0.95), (0.25, 0.75)).
- <u>levels (bool):</u> draw a price's level instead of its yearly return since the start. Defaults to False.
- <u>metric (str &#124; None):</u> the reading (see `ScenarioSet.metric_paths`). Defaults to None, the factor's default.

**Returns:**

<u>matplotlib.figure.Figure:</u> the figure holding the grid.

**Raises:**

- <u>ValueError:</u> if `runs` is empty or `n_columns` is below 1.
- <u>KeyError:</u> if a run does not simulate `factor`.

</details>

## plot_portfolios

Plot several portfolios on one chart, one line each, to see which mix grew most and when they parted ways.

On history each line is what the portfolio was worth; on simulated scenarios it is the median, with the middle half
of the scenarios shaded in the same color. Every portfolio shares one axis, so the gap between two lines is the
difference an investor would have seen. `result.plot()` draws this chart for a `compute()` of several presets.

**As an example:**

```python
from financescenarios import Portfolio, Scenarios

portfolio = Portfolio.backtest(Scenarios.from_profiles(), ["balanced_60_40", "all_weather"])
portfolio.compute(initial_value=100_000, rebalance_every=12).plot(levels=True)
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
plot_portfolios(
    portfolio_result: ScenarioSet,
    portfolios: Sequence[str] | None = None,
    ax: 'Axes | None' = None,
    levels: bool = False,
    metric: Metric | None = None,
    quantile_band: tuple[float, float] = (0.25, 0.75),
) -> 'Figure'
```

**Args:**

- <u>portfolio_result (ScenarioSet):</u> a `Portfolio.compute()` result of several presets, one path per preset.
- <u>portfolios (Sequence[str] &#124; None):</u> the portfolios to draw. Defaults to None, every one in the result.
- <u>ax (matplotlib Axes &#124; None):</u> an existing Axes to draw into. Defaults to None, a new figure.
- <u>levels (bool):</u> draw values in money instead of the yearly return since the start. Defaults to False.
- <u>metric (str &#124; None):</u> the reading (see `ScenarioSet.metric_paths`). Defaults to None, the yearly return.
- <u>quantile_band (tuple[float, float]):</u> the range shaded around each median on scenarios. Defaults to (0.25, 0.75).

**Returns:**

<u>matplotlib.figure.Figure:</u> the figure holding the chart.

**Raises:**

- <u>ValueError:</u> if the result holds no portfolios.
- <u>KeyError:</u> if a named portfolio is not in the result.

</details>

## plot_correlation_matrix

Draw a correlation matrix as a heatmap: blue for negative, gray at zero, red for positive.

The colors always span -1 to 1, so the matrices of two runs can be compared directly. Each cell shows its value
while the grid stays readable, up to 14 factors by default.

**As an example:**

```python
from financescenarios import plot_correlation_matrix

calibration = scenarios.calibrate()
plot_correlation_matrix(calibration.correlation_matrix, calibration.factor_names)
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
plot_correlation_matrix(
    correlation_matrix: np.ndarray,
    factor_names: list[str],
    annotate: bool | None = None,
    labels: list[str] | None = None,
    ax: 'Axes | None' = None,
) -> 'Figure'
```

**Args:**

- <u>correlation_matrix (np.ndarray):</u> a square matrix, e.g. `CalibrationResult.correlation_matrix`.
- <u>factor_names (list[str]):</u> the factor of each row, in order, e.g. `CalibrationResult.factor_names`.
- <u>annotate (bool &#124; None):</u> write each cell's value into it. Defaults to None, which does so up to 14 factors.
- <u>labels (list[str] &#124; None):</u> display names for the axes, in the same order. Defaults to None, each factor name tidied up ("us_broad" -> "US Broad").
- <u>ax (Axes &#124; None):</u> an existing matplotlib Axes to draw into. Defaults to None, a new figure.

**Returns:**

<u>matplotlib.figure.Figure:</u> the figure holding the heatmap.

**Raises:**

- <u>ValueError:</u> if the matrix is not square, or does not match `factor_names` or `labels`.

</details>

## plot_sleeve_values

Plot the median value of every holding over time as a stacked area, showing how the portfolio's make-up changes.

A buy-and-hold equity holding visibly grows its share; a rebalanced one keeps it. The median is taken per holding,
so the stack shows a typical make-up rather than any single scenario. Past eight holdings, the rest are grouped as
"Other". `result.plot(kind="sleeves")` draws the same chart.

**As an example:**

```python
from financescenarios import Portfolio, plot_sleeve_values

values = Portfolio.from_preset(result, preset="balanced_60_40").compute(rebalance_every=12)
plot_sleeve_values(values)
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
plot_sleeve_values(portfolio_result: ScenarioSet, ax: 'Axes | None' = None) -> 'Figure'
```

**Args:**

- <u>portfolio_result (ScenarioSet):</u> a `Portfolio.compute()` or `compute_glidepath()` result.
- <u>ax (matplotlib Axes &#124; None):</u> an existing Axes to draw into. Defaults to None, a new figure.

**Returns:**

<u>matplotlib.figure.Figure:</u> the figure holding the chart.

**Raises:**

- <u>ValueError:</u> if the result holds no holdings, such as a plain simulated run.

</details>

## plot_weight_drift

Plot each holding's median weight drift over time: how far the mix has wandered from its target, around a zero
line.

Between rebalances the weights wander as one asset outgrows another; this shows by how much, per holding. Each
holding keeps the same color as in `plot_sleeve_values()`.

**As an example:**

```python
from financescenarios import Portfolio, plot_weight_drift

portfolio = Portfolio.from_preset(result, preset="balanced_60_40")
computed = portfolio.compute()
plot_weight_drift(computed, portfolio.weight_drift(computed))
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
plot_weight_drift(
    portfolio_result: ScenarioSet,
    weight_drift: dict[str, np.ndarray],
    ax: 'Axes | None' = None,
) -> 'Figure'
```

**Args:**

- <u>portfolio_result (ScenarioSet):</u> the computed portfolio the drift was measured on, for its dates and holdings.
- <u>weight_drift (dict[str, np.ndarray]):</u> factor name to drift per step, as `Portfolio.weight_drift()` returns; a drift per scenario is reduced to its median.
- <u>ax (matplotlib Axes &#124; None):</u> an existing Axes to draw into. Defaults to None, a new figure.

**Returns:**

<u>matplotlib.figure.Figure:</u> the figure holding the chart.

**Raises:**

- <u>ValueError:</u> if `weight_drift` is empty.

</details>
