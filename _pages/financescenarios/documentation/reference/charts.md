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

The chart functions behind every `.plot()`: fan charts, paths, terminal distributions, runs and portfolios. Generated from the docstrings of Finance Scenarios 0.1.0; `help(...)` in Python shows the same text.

```python
from financescenarios import plot_factors, plot_fan_chart, plot_paths, plot_terminal_distribution, plot_runs, plot_correlation_matrix, plot_sleeve_values, plot_weight_drift
```

## plot_factors

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

A small-multiples grid: one fan chart per factor, shared style, each on its
own y-scale (never a dual axis; a rate and a price level don't share one).
The default reads every simulated factor in the run.

**Args:**

- <u>scenario_set (ScenarioSet):</u> the simulation to read.
- <u>factors (Sequence[str] &#124; None):</u> which factors to draw, defaulting to every factor in the run in its own order.
- <u>n_columns (int):</u> grid width; rows follow from the factor count.
- <u>quantile_bands:</u> passed through to each panel's `plot_fan_chart`.
- <u>levels (bool):</u> draw level factors as price levels instead of annualized returns since start.
- <u>metric (str &#124; None):</u> the reading, "rate", "level", "change", "yoy", "cumulative" or "annualized" (see `ScenarioSet.metric_paths`); None keeps the factor's default.

**Returns:**

<u>matplotlib.figure.Figure:</u> the figure holding the grid.

**Raises:**

- <u>KeyError:</u> if a named factor is not a key in `paths`.

## plot_fan_chart

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

The headline read of one simulated factor: nested cross-simulation quantile
bands (outermost first) around the median path. Magnitude nested in
magnitude, so the bands are one blue ramp light-to-dark rather than
different hues, and the median is a single dark line on top.

**Args:**

- <u>scenario_set (ScenarioSet):</u> the simulation to read.
- <u>factor (str):</u> the factor name, must be a key in `paths`; a `Portfolio.compute()` result's `"portfolio"` works the same way.
- <u>quantile_bands (Sequence[tuple[float, float]]):</u> (lower, upper) quantile pairs, outermost first; each is drawn as one filled band.
- <u>ax:</u> an existing matplotlib Axes to draw into; a new figure otherwise.
- <u>subtitle (str &#124; None):</u> replaces the default subtitle (qualifier, bands and simulation count); `plot_factors` passes the short qualifier alone.
- <u>levels (bool):</u> draw a level factor's native price level instead of its annualized return since start (see `ScenarioSet.metric_paths`).
- <u>metric (str &#124; None):</u> the reading, "rate", "level", "change", "yoy", "cumulative" or "annualized" (see `ScenarioSet.metric_paths`); None keeps the factor's default.

**Returns:**

<u>matplotlib.figure.Figure:</u> the figure holding the chart.

**Raises:**

- <u>KeyError:</u> if `factor` is not a key in `paths`.
- <u>ValueError:</u> if a band's lower quantile is not strictly below its upper.

## plot_paths

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

A spaghetti view of individual simulated paths: the texture the fan chart's
percentile bands smooth away (a fan says nothing about how jagged any one
future is). A random sample of `n_paths` paths in a translucent blue, the
cross-simulation median on top in the same dark line the fan chart uses.

**Args:**

- <u>scenario_set (ScenarioSet):</u> the simulation to read.
- <u>factor (str):</u> the factor name, must be a key in `paths`.
- <u>n_paths (int &#124; None):</u> how many individual paths to sample; None (the default) draws every simulated path.
- <u>seed (int &#124; None):</u> sampling seed, for a reproducible selection.
- <u>ax:</u> an existing matplotlib Axes to draw into; a new figure otherwise.
- <u>levels (bool):</u> draw a level factor's native price level instead of its annualized return since start.
- <u>metric (str &#124; None):</u> the reading, "rate", "level", "change", "yoy", "cumulative" or "annualized" (see `ScenarioSet.metric_paths`); None keeps the factor's default.

**Returns:**

<u>matplotlib.figure.Figure:</u> the figure holding the chart.

**Raises:**

- <u>KeyError:</u> if `factor` is not a key in `paths`.

## plot_terminal_distribution

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

The cross-simulation distribution of one factor's final-step value: the
"where does this land" histogram every tail-risk question starts from, with
the requested quantiles marked as labeled vertical lines.

**Args:**

- <u>scenario_set (ScenarioSet):</u> the simulation to read.
- <u>factor (str):</u> the factor name, must be a key in `paths`.
- <u>bins (int &#124; None):</u> histogram bin count; None scales it to the run (about 2 * sqrt(n_simulations), between 10 and 40), so 100 simulations don't scatter across mostly empty bins.
- <u>quantiles (Sequence[float]):</u> quantiles to mark with vertical lines.
- <u>ax:</u> an existing matplotlib Axes to draw into; a new figure otherwise.
- <u>levels (bool):</u> a level factor's final price level instead of its annualized return over the whole horizon.
- <u>metric (str &#124; None):</u> the reading, "rate", "level", "change", "yoy", "cumulative" or "annualized" (see `ScenarioSet.metric_paths`); None keeps the factor's default.

**Returns:**

<u>matplotlib.figure.Figure:</u> the figure holding the chart.

**Raises:**

- <u>KeyError:</u> if `factor` is not a key in `paths`.

## plot_runs

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

The same factor across several runs, one fan chart per run on a shared scale, so a baseline and its stress
regimes read side by side: the chart companion to `compare_runs`.

**Args:**

- <u>runs (Mapping[str, ScenarioSet]):</u> run name -> run, drawn in that order, e.g. {"baseline": result, ...}.
- <u>factor (str):</u> the factor to compare; every run must simulate it.
- <u>n_columns (int):</u> grid width; rows follow from the number of runs.
- <u>quantile_bands:</u> passed through to each panel's `plot_fan_chart`.
- <u>levels (bool):</u> draw a level factor's native price level instead of its annualized return since start.
- <u>metric (str &#124; None):</u> the reading (see `ScenarioSet.metric_paths`); None keeps the factor's default.

**Returns:**

<u>matplotlib.figure.Figure:</u> the figure holding the grid.

**Raises:**

- <u>ValueError:</u> if `runs` is empty or `n_columns` is below 1.
- <u>KeyError:</u> if a run does not simulate `factor`.

**As an example:**

```python
from financescenarios import plot_runs

plot_runs({"baseline": result, "oil_crisis": oil_crisis}, "united_states_inflation")
```

## plot_correlation_matrix

```python
plot_correlation_matrix(
    correlation_matrix: np.ndarray,
    factor_names: list[str],
    annotate: bool | None = None,
    labels: list[str] | None = None,
    ax: 'Axes | None' = None,
) -> 'Figure'
```

The calibrated cross-factor correlation matrix as a diverging heatmap:
blue for negative, neutral gray at zero, red for positive, fixed to the
[-1, 1] domain so two runs' matrices are directly comparable. Cells are
annotated with their values up to a readability cap (colors alone can't
carry a two-decimal read).

```python
calibration = scenarios.calibrate(config)
plot_correlation_matrix(calibration.correlation_matrix, calibration.factor_names)
```

**Args:**

- <u>correlation_matrix (np.ndarray):</u> shape (n_factors, n_factors), e.g. `CalibrationResult.correlation_matrix`.
- <u>factor_names (list[str]):</u> axis labels, same order as the matrix rows, e.g. `CalibrationResult.factor_names`.
- <u>annotate (bool &#124; None):</u> write each cell's value into it. Defaults to True up to 14 factors, False beyond.
- <u>labels (list[str] &#124; None):</u> display names for the axes, same order as `factor_names`; defaults to each name humanized ("us_broad" -> "US Broad").
- <u>ax:</u> an existing matplotlib Axes to draw into; a new figure otherwise.

**Returns:**

<u>matplotlib.figure.Figure:</u> the figure holding the heatmap.

**Raises:**

- <u>ValueError:</u> if the matrix isn't square or doesn't match `factor_names`.

## plot_sleeve_values

```python
plot_sleeve_values(portfolio_result: ScenarioSet, ax: 'Axes | None' = None) -> 'Figure'
```

The median dollar value of every sleeve over time as a stacked area: how
the portfolio's composition actually evolves (a drifting buy-and-hold
equity sleeve visibly outgrows its band; a rebalanced one doesn't).
Medians are taken per sleeve, so the stack is a typical composition, not
any single simulation's.

**Args:**

- <u>portfolio_result (ScenarioSet):</u> a `Portfolio.compute()`/`compute_glidepath()` result; the `"<factor>_value"` sleeve paths are read, `"portfolio"` ignored.
- <u>ax:</u> an existing matplotlib Axes to draw into; a new figure otherwise.

**Returns:**

<u>matplotlib.figure.Figure:</u> the figure holding the chart.

**Raises:**

- <u>ValueError:</u> if the scenario set holds no sleeve paths.

## plot_weight_drift

```python
plot_weight_drift(
    portfolio_result: ScenarioSet,
    weight_drift: dict[str, np.ndarray],
    ax: 'Axes | None' = None,
) -> 'Figure'
```

Each sleeve's median actual-minus-target weight over time: how far the
allocation has wandered from its target between rebalances, per sleeve,
around a zero line. Sleeves keep the same fixed categorical slots
`plot_sleeve_values` assigns.

```python
portfolio = Portfolio.from_preset(result, preset="balanced_60_40")
computed = portfolio.compute()
plot_weight_drift(computed, portfolio.weight_drift(computed))
```

**Args:**

- <u>portfolio_result (ScenarioSet):</u> the computed portfolio the drift was measured on (supplies the date axis and sleeve ordering).
- <u>weight_drift (dict[str, np.ndarray]):</u> factor name -> per-step drift, as `Portfolio.weight_drift()` returns: either shape (n_steps + 1,) or (n_simulations, n_steps + 1), reduced to the median here.
- <u>ax:</u> an existing matplotlib Axes to draw into; a new figure otherwise.

**Returns:**

<u>matplotlib.figure.Figure:</u> the figure holding the chart.

**Raises:**

- <u>ValueError:</u> if `weight_drift` is empty.
