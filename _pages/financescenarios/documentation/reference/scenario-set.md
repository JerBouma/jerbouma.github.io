---
title: "ScenarioSet"
seo_title: "ScenarioSet Reference – Finance Scenarios"
excerpt: "The result of a run: describe, filter, plot, diagnose and compare simulated scenarios."
description: "The result of a run: describe, filter, plot, diagnose and compare simulated scenarios."
author_profile: false
permalink: /projects/financescenarios/docs/reference/scenario-set
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

The result of a run: describe, filter, plot, diagnose and compare simulated scenarios. Generated from the docstrings of Finance Scenarios 0.1.0; `help(...)` in Python shows the same text.

```python
from financescenarios import ScenarioSet, FactorLabel, compare_runs
```

## ScenarioSet

```python
class ScenarioSet(BaseModel):
    paths: dict[str, np.ndarray]
    time_grid: np.ndarray
    dates: list[date]
    factor_names: list[str]
    n_simulations: int
    seed: int | None
    calibration_metadata: dict[str, Any]
    antithetic: bool = False
    factor_categories: dict[str, str] = {}
    factor_labels: dict[str, FactorLabel] = {}
    return_paths: dict[str, np.ndarray] = {}
```

The result of a simulation: every factor's simulated paths, one row per scenario and one column per date.

`Scenarios.simulate()` returns it, and `Portfolio` and the Solvency II functions read it. Every report reads a factor
the same way: a rate as its yearly rate, and anything with a price (equities, FX, commodities, a portfolio) as its
yearly return since the start, both as decimals (0.0441 is 4.41%). `metric_paths` lists the other readings, such as
inflation as a price index or a year-over-year change, and `levels=True` gives the raw simulated values.

| Method | What it gives |
|:-------|:--------------|
| `describe()` | one row per factor: where it starts and where it ends up |
| `summary_statistics(factor)` | percentile bands, date by date |
| `horizon_summary([1, 5, 10])` | percentiles at chosen horizons |
| `plot(factor)` | a fan chart, the individual paths or the final distribution |
| `filter(...)`, `filter_narrative(...)` | only the scenarios that fit a story |
| `to_dataframe(factor)`, `to_long()` | the paths as Polars tables |
| `result["us_broad"]` | one factor's raw paths as a NumPy array |

**As an example:**

```python
from financescenarios import Scenarios

result = Scenarios.from_profiles(settings="default", factor_set="us_only").simulate(n_simulations=100)
result.describe()                                      # one row per factor
result.summary_statistics("united_states_short_rate")  # percentile bands date by date
result.plot("us_broad")                                # a fan chart
result.factors("equities")                             # the factor names in one category
```

**Attributes:**

- <u>paths (dict[str, np.ndarray]):</u> factor name -> simulated values, one row per scenario, one column per date.
- <u>time_grid (np.ndarray):</u> each date's distance from the start, in years.
- <u>dates (list[date]):</u> the calendar dates of the run.
- <u>factor_names (list[str]):</u> the simulated factors, in simulation order.
- <u>n_simulations (int):</u> the number of scenarios.
- <u>seed (int &#124; None):</u> the random seed the run was drawn with.
- <u>calibration_metadata (dict[str, Any]):</u> factor name -> the fitted parameters it was simulated with.
- <u>antithetic (bool):</u> whether scenarios were drawn in mirrored pairs (antithetic variates) to reduce noise.
- <u>factor_categories (dict[str, str]):</u> factor name -> its category, e.g. "equities" or "inflation".
- <u>factor_labels (dict[str, FactorLabel]):</u> factor name -> its display name for charts and tables.
- <u>return_paths (dict[str, np.ndarray]):</u> a portfolio holding's own growth, which its returns are read from.

## n_steps

```python
scenarioset.n_steps  # property -> int
```

The number of time steps in the run, one fewer than its dates: 60 for five years of monthly steps.

## label

```python
label(factor: str) -> FactorLabel
```

A factor's display name (see `FactorLabel`), or a tidied version of its name when the run carries none.

## is_level_factor

```python
is_level_factor(factor: str) -> bool
```

Whether a factor is simulated as a level (a price, a portfolio value or the leading indicator) rather than as a
rate. See `factor_kind`.

## factor_kind

```python
factor_kind(factor: str) -> FactorKind
```

What a factor's simulated values are, which decides how each `metric` reads it.

- "price": a price or value (equities, FX, commodities, a dividend index, a portfolio). Changes are percentages.
- "growth": the growth rate of a price index (inflation, real estate). Its level is the index it compounds into.
- "rate": a rate or spread (interest rates, the yield-curve factors, credit spreads, unemployment, dividend yield,
  mortality). Changes are differences in the rate's own units.
- "index": an index with no rate reading (the OECD composite leading indicator). Changes are percentages.

A factor without a category, as in a hand-built run, counts as a "rate".

**Args:**

- <u>factor (str):</u> the factor name.

**Returns:**

<u>str:</u> "price", "growth", "rate" or "index".

## resolve_metric

```python
resolve_metric(factor: str, levels: bool = False, metric: Metric | None = None) -> str
```

The reading `metric_paths` gives for these arguments: "native" for `levels=True`, the factor's default when
`metric` is None, otherwise `metric` itself once checked.

**Args:**

- <u>factor (str):</u> the factor name.
- <u>levels (bool):</u> ask for the raw simulated values. Defaults to False.
- <u>metric (str &#124; None):</u> the reading asked for (see `metric_paths`). Defaults to None.

**Returns:**

<u>str:</u> the reading, e.g. "rate", "annualized" or "native".

**Raises:**

- <u>ValueError:</u> if `levels=True` is combined with a `metric`, the metric is unknown, or it has no meaning for the factor (a "rate" of a price, an "annualized" return of a rate).

## metric_paths

```python
metric_paths(factor: str, levels: bool = False, metric: Metric | None = None) -> np.ndarray
```

One factor's paths the way every summary, table and chart reads them.

`metric` picks how a number is expressed: the same simulated inflation can be its yearly rate (3.4%), a price
index that starts at 100, or that index's change over one step, one year or since today. By default a rate reads
as itself and a price as its yearly return since the start, (S_t / S_0) ** (1 / t) - 1: a 769 -> 1,209 equity
path over five years reads as 9.5% a year.

| metric | price (equity, FX, ...) | growth rate (inflation, real estate) | rate level (rates, spreads, ...) |
|:-------|:-------------------------|:-------------------------------------|:---------------------------------|
| `rate` | not available | the simulated rate (default) | the simulated rate (default) |
| `level` | the price | the compounded index, 100 at start | the rate |
| `change` | % change over one step | % change of the index over one step | change over one step |
| `yoy` | % change over one year | % change of the index over one year | change over one year |
| `cumulative` | % change since start | % change of the index since start | change since start |
| `annualized` | yearly return since start (default) | average yearly growth since start | not available |

The leading indicator reads like a price but defaults to `level`. A change of a rate is a difference in its own
units (0.005 is half a percentage point). See [percentage change](https://en.wikipedia.org/wiki/Relative_change)
and [year over year](https://en.wikipedia.org/wiki/Year_over_year).

**Args:**

- <u>factor (str):</u> the factor name.
- <u>levels (bool):</u> the raw simulated values instead; not combined with `metric`. Defaults to False.
- <u>metric (str &#124; None):</u> a reading from the table; None keeps the factor's default.

**Returns:**

<u>np.ndarray:</u> one row per scenario, one column per date; NaN where there is no value yet.

**Raises:**

- <u>KeyError:</u> if the run has no such factor.
- <u>ValueError:</u> if the metric does not apply to the factor, or for `yoy` on a step that does not divide a year.

**As an example:**

```python
result.metric_paths("united_states_inflation", metric="level")
```

## metric_applies

```python
metric_applies(factor: str, metric: Metric | None) -> bool
```

Whether `metric` has a reading for `factor` (None always does); multi-factor reports fall back to the
factor's default where it has none, e.g. `describe(metric="annualized")` keeps rates as rates.

## metric_description

```python
metric_description(factor: str, levels: bool = False, metric: Metric | None = None) -> str | None
```

A few words naming the reading for a chart subtitle, or None when the value is the factor itself.

## to_dataframe

```python
to_dataframe(factor: str, levels: bool = False, metric: Metric | None = None) -> pl.DataFrame
```

One factor's paths as a Polars table, one row per scenario and one column per date.

Values are read the way every report reads them (see `metric_paths`): a rate as itself, a price as its yearly
return since the start, which is empty on the first date.

**Args:**

- <u>factor (str):</u> the factor name.
- <u>levels (bool):</u> give the raw simulated values (prices) instead. Defaults to False.
- <u>metric (str &#124; None):</u> the reading, "rate", "level", "change", "yoy", "cumulative" or "annualized" (see `metric_paths`). Defaults to None, the factor's default.

**Returns:**

<u>pl.DataFrame:</u> a "scenario" column plus one column per date ("YYYY-MM-DD").

**Raises:**

- <u>KeyError:</u> if the run has no such factor.

**As an example:**

```python
result.to_dataframe("united_states_short_rate")
```

## discount_factor_paths

```python
discount_factor_paths(factor: str) -> np.ndarray
```

`discount_factors()` as a plain array, one row per scenario and 1 at the start: the discount factors the Solvency
II functions use.

## discount_factors

```python
discount_factors(factor: str) -> pl.DataFrame
```

What 1 paid at each date is worth today, scenario by scenario, treating one factor as the short rate.

This turns a simulated short rate into a discount curve per scenario, the way money in a bank account grows at
that rate. It is usually applied to an interest rate factor, but works on any rate. The discount factor is
DF(t) = exp(-sum of rate x time step up to t), so it is 1 at the start.

It discounts a known cash flow correctly. Pricing an uncertain payoff under these real-world scenarios needs an
extra adjustment for the market price of risk, which this package does not compute (see the reference).

**Args:**

- <u>factor (str):</u> the rate factor to discount with, e.g. "united_states_short_rate".

**Returns:**

<u>pl.DataFrame:</u> a "scenario" column plus one discount-factor column per date.

**Raises:**

- <u>KeyError:</u> if the run has no such factor.
- <u>ValueError:</u> if the factor is a price or index rather than a rate.

**As an example:**

```python
result.discount_factors("united_states_short_rate")
```

**References:**

- Cheng, P.K., Planchet, F. (2018). "Stochastic Deflator for an Economic Scenario Generator with Five Factors." Laboratoire SAF, Universite Claude Bernard Lyon 1. <https://arxiv.org/abs/1806.02991>

## cumulative_index

```python
cumulative_index(factor: str, initial_index: float = 100.0) -> pl.DataFrame
```

Compound a rate factor into an index, such as inflation into a price index that starts at 100.

Use it for factors simulated as a growth rate, such as inflation or real estate. Prices such as equities or FX
already are an index and don't need it. The index is initial_index x exp(sum of rate x time step up to t).

**Args:**

- <u>factor (str):</u> the rate factor to compound, e.g. "united_states_inflation".
- <u>initial_index (float):</u> the index level at the start. Defaults to 100.0.

**Returns:**

<u>pl.DataFrame:</u> a "scenario" column plus one index-level column per date.

**Raises:**

- <u>KeyError:</u> if the run has no such factor.
- <u>ValueError:</u> if the factor is a price or index rather than a rate, or `initial_index` is not a positive number.

**As an example:**

```python
result.cumulative_index("united_states_inflation")
```

## diagnose

```python
diagnose(factor: str | None = None, tolerance: float = 0.2) -> 'FactorDiagnostics | pl.DataFrame'
```

Check that a factor's scenarios end up where its fitted model says they should settle in the long run.

Interest rates, inflation, unemployment, real estate, credit spreads, the leading indicator and the yield-curve
factors are usually fitted as mean-reverting (an Ornstein-Uhlenbeck process): pulled back toward a long-run level.
Such a process has a known long-run mean and spread, so this compares the last date's simulated mean and standard
deviation with them. Equities and FX have no such long-run level and are skipped.

A `within_tolerance=False` is not always a fault, and `reason` says which case it is: the mean is off by more than
the tolerance and `mean_noise_floor` (3 standard errors of the simulated mean, the gap sampling noise alone
explains), the spread is off, or both. It adds "slow to settle" when the horizon spans fewer than three time
constants (1 / mean_reversion_speed, about four half-lives): such a factor has not reached its long-run level
yet, so a gap is expected. `unit` is "log" for a factor fitted on the logarithm of its value (credit spreads,
commodities, dividend yield), whose numbers are then in log space, and "level" otherwise.

**Args:**

- <u>factor (str &#124; None):</u> the factor to check. Defaults to None, every factor this applies to.
- <u>tolerance (float):</u> how far the simulated mean and standard deviation may be from the long-run values, as a share of them. Defaults to 0.2.

**Returns:**

<u>FactorDiagnostics &#124; pl.DataFrame:</u> for one factor, a `FactorDiagnostics` with the means, spreads, mean gap, noise floor, `within_tolerance`, `unit` and `reason`; without one, a table with "factor", "simulated_mean", "theoretical_mean", "simulated_std", "theoretical_std", "within_tolerance", "unit" and "reason", one row per factor.

**Raises:**

- <u>KeyError:</u> if the run has no such factor, or no fitted parameters for it.
- <u>NotOUCalibratedError:</u> if the factor is not mean-reverting, such as equities or FX (a ValueError).

**As an example:**

```python
result.diagnose("united_states_short_rate")
result.diagnose().filter(~pl.col("within_tolerance"))  # every factor off, with its reason
```

## plot

```python
plot(
    factors: str | Sequence[str] | None = None,
    kind: Literal['fan', 'paths', 'distribution', 'sleeves'] = 'fan',
    levels: bool = False,
    ax: 'Axes | None' = None,
    metric: Metric | None = None,
) -> 'Figure'
```

One quick chart of this run: a fan chart, the individual paths, or where a factor lands at the end.

Rates and returns share one percentage axis (see `metric_paths`); `levels=True` draws prices and portfolio values
in money instead. Without a factor it draws a computed portfolio's value when the run holds one, and otherwise a
grid with one fan chart per factor. The `plot_*` methods give finer control over bands, bins and path counts.

**Args:**

- <u>factors (str &#124; Sequence[str] &#124; None):</u> one factor, several (a grid of fan charts), or None. Defaults to None.
- <u>kind (str):</u> "fan" (default), "paths", "distribution", or "sleeves" for a portfolio's holdings over time.
- <u>levels (bool):</u> draw prices and money values instead of returns. Defaults to False.
- <u>ax (Axes &#124; None):</u> an existing matplotlib Axes for a single chart. Defaults to None, a new figure.
- <u>metric (str &#124; None):</u> the reading (see `metric_paths`). Defaults to None, each factor's default.

**Returns:**

<u>matplotlib.figure.Figure:</u> the figure holding the chart.

**Raises:**

- <u>KeyError:</u> if a named factor is not in this run.
- <u>ValueError:</u> if `kind` is unknown, or several factors are combined with a single-chart `kind`.

**As an example:**

```python
result.plot("us_broad")                                 # one factor's percentile fan
result.plot("us_broad", kind="distribution")            # where it lands at the horizon
result.plot("united_states_inflation", metric="level")  # inflation as a price index
values.plot(kind="sleeves")                             # a Portfolio.compute() result's holdings
```

## plot_fan_chart

```python
plot_fan_chart(
    factor: str,
    quantile_bands: Sequence[tuple[float, float]] = ((0.05, 0.95), (0.25, 0.75)),
    ax: 'Axes | None' = None,
    levels: bool = False,
    metric: Metric | None = None,
) -> 'Figure'
```

One factor's fan chart: the median path with shaded bands, by default for the middle 50% and 90% of scenarios.
The same chart as `plot_fan_chart(result, factor)`.

**Args:**

- <u>factor (str):</u> the factor to draw.
- <u>quantile_bands (Sequence[tuple[float, float]]):</u> (lower, upper) quantile pairs, outermost first. Defaults to ((0.05, 0.95), (0.25, 0.75)).
- <u>ax (Axes &#124; None):</u> an existing matplotlib Axes to draw into. Defaults to None, a new figure.
- <u>levels (bool):</u> draw a price's level instead of its yearly return since the start. Defaults to False.
- <u>metric (str &#124; None):</u> the reading (see `metric_paths`). Defaults to None, the factor's default.

**Returns:**

<u>matplotlib.figure.Figure:</u> the figure holding the chart.

## plot_paths

```python
plot_paths(
    factor: str,
    n_paths: int | None = None,
    seed: int | None = None,
    ax: 'Axes | None' = None,
    levels: bool = False,
    metric: Metric | None = None,
) -> 'Figure'
```

Every simulated path of one factor (or a random sample of them), with the median on top. The same chart as
`plot_paths(result, factor)`.

**Args:**

- <u>factor (str):</u> the factor to draw.
- <u>n_paths (int &#124; None):</u> how many paths to draw, picked at random. Defaults to None, every path.
- <u>seed (int &#124; None):</u> the random seed for that pick. Defaults to None.
- <u>ax (Axes &#124; None):</u> an existing matplotlib Axes to draw into. Defaults to None, a new figure.
- <u>levels (bool):</u> draw a price's level instead of its yearly return since the start. Defaults to False.
- <u>metric (str &#124; None):</u> the reading (see `metric_paths`). Defaults to None, the factor's default.

**Returns:**

<u>matplotlib.figure.Figure:</u> the figure holding the chart.

## plot_terminal_distribution

```python
plot_terminal_distribution(
    factor: str,
    bins: int | None = None,
    quantiles: Sequence[float] = (0.05, 0.5, 0.95),
    ax: 'Axes | None' = None,
    levels: bool = False,
    metric: Metric | None = None,
) -> 'Figure'
```

A histogram of where one factor ends up at the horizon, with percentiles marked. The same chart as
`plot_terminal_distribution(result, factor)`.

**Args:**

- <u>factor (str):</u> the factor to draw.
- <u>bins (int &#124; None):</u> the number of bars. Defaults to None, scaled to the number of scenarios.
- <u>quantiles (Sequence[float]):</u> the quantiles to mark. Defaults to (0.05, 0.5, 0.95).
- <u>ax (Axes &#124; None):</u> an existing matplotlib Axes to draw into. Defaults to None, a new figure.
- <u>levels (bool):</u> show a price's final level instead of its yearly return. Defaults to False.
- <u>metric (str &#124; None):</u> the reading (see `metric_paths`). Defaults to None, the factor's default.

**Returns:**

<u>matplotlib.figure.Figure:</u> the figure holding the chart.

## plot_factors

```python
plot_factors(
    factors: Sequence[str] | None = None,
    n_columns: int = 3,
    quantile_bands: Sequence[tuple[float, float]] = ((0.05, 0.95), (0.25, 0.75)),
    levels: bool = False,
    metric: Metric | None = None,
) -> 'Figure'
```

A grid with one fan chart per factor, each on its own scale. The same chart as `plot_factors(result)`.

**Args:**

- <u>factors (Sequence[str] &#124; None):</u> the factors to draw. Defaults to None, every factor.
- <u>n_columns (int):</u> panels per row. Defaults to 3.
- <u>quantile_bands (Sequence[tuple[float, float]]):</u> the bands each panel shades. Defaults to ((0.05, 0.95), (0.25, 0.75)).
- <u>levels (bool):</u> draw prices as levels instead of yearly returns since the start. Defaults to False.
- <u>metric (str &#124; None):</u> the reading (see `metric_paths`). Defaults to None, each factor's default.

**Returns:**

<u>matplotlib.figure.Figure:</u> the figure holding the grid.

## filter

```python
filter(
    factor: str,
    quantile_range: tuple[float, float],
    step_range: tuple[int, int] | None = None,
) -> 'ScenarioSet'
```

Keep only the scenarios where one factor sits within a chosen range, such as the 30% with the highest interest
rates.

Each scenario is ranked by the factor's average over the chosen steps (a price by its yearly return across them),
and the scenarios between the two quantiles are kept. A kept scenario keeps every other factor's path too, so a
high-rate scenario brings its own correlated inflation and equity paths along. Useful for stress tests and for
building a story-driven scenario out of the simulation instead of by hand. Fewer than 30 kept scenarios log a
warning, since percentiles mean little on so few.

**Args:**

- <u>factor (str):</u> the factor to rank scenarios by.
- <u>quantile_range (tuple[float, float]):</u> the (lower, upper) quantiles to keep, in [0, 1]; (0.7, 1.0) keeps the top 30%.
- <u>step_range (tuple[int, int] &#124; None):</u> the (start, stop) steps to rank over, like a Python slice. Defaults to None, the whole path.

**Returns:**

<u>ScenarioSet:</u> the same run with only the kept scenarios.

**Raises:**

- <u>KeyError:</u> if the run has no such factor.
- <u>ValueError:</u> if the quantile or step range is invalid, or no scenario falls within it.

**As an example:**

```python
high_rates = result.filter("united_states_short_rate", (0.7, 1.0))
```

## filter_narrative

```python
filter_narrative(
    targets: dict[str, tuple[float, float]],
    step_range: tuple[int, int] | None = None,
    mode: Literal['sequential', 'joint'] = 'sequential',
) -> 'ScenarioSet'
```

Keep only the scenarios that fit a story told through several factors at once, such as stagflation: high
inflation and weak equities.

Each target is a (lower, upper) quantile range for one factor, as in `filter`. The result is a stress scenario
drawn from the simulation itself rather than one hand-picked path, with every factor's path kept.

**Args:**

- <u>targets (dict[str, tuple[float, float]]):</u> factor name -> the (lower, upper) quantile range to keep.
- <u>step_range (tuple[int, int] &#124; None):</u> the (start, stop) steps every target ranks over. Defaults to None, the whole path.
- <u>mode (str):</u> "sequential" (default) applies each target to what the previous ones left, so (0.7, 1.0) on rates then (0.0, 0.3) on equities keeps about 9%; "joint" ranks every target against the full run and keeps the overlap, which can be much smaller.

**Returns:**

<u>ScenarioSet:</u> the scenarios that meet every target.

**Raises:**

- <u>KeyError:</u> if a target factor is not in the run.
- <u>ValueError:</u> if a quantile range or `mode` is invalid, or no scenario meets every target.

**As an example:**

```python
stagflation = result.filter_narrative({"united_states_inflation": (0.8, 1.0), "us_broad": (0.0, 0.2)})
```

## rescale_scenario_cloud

```python
rescale_scenario_cloud(
    factor: str,
    mean_shift: float = 0.0,
    spread_multiplier: float = 1.0,
) -> 'ScenarioSet'
```

Shift and widen (or narrow) one factor's simulated scenarios without simulating again.

Use it when a view is easiest to state about the whole distribution, such as "inflation half a point higher and
more uncertain", rather than as a change to one fitted parameter before simulating (a belief override). At
every date, each scenario becomes (mean + mean_shift) + spread_multiplier x (value - mean), with mean that date's
average across scenarios. The shape of the distribution and every other factor stay as they are.

**Args:**

- <u>factor (str):</u> the factor to rescale.
- <u>mean_shift (float):</u> the amount added to the factor's average at every date, in its simulated units. Defaults to 0.0.
- <u>spread_multiplier (float):</u> widens (above 1) or narrows (below 1) the spread around that average; must be above 0. Defaults to 1.0.

**Returns:**

<u>ScenarioSet:</u> the same run with this factor's paths replaced.

**Raises:**

- <u>KeyError:</u> if the run has no such factor.
- <u>ValueError:</u> if `mean_shift` is not finite or `spread_multiplier` is not above 0.

**As an example:**

```python
result.rescale_scenario_cloud("united_states_inflation", mean_shift=0.005, spread_multiplier=1.5)
```

## summary_statistics

```python
summary_statistics(
    factor: str,
    quantiles: list[float] | None = None,
    levels: bool = False,
    metric: Metric | None = None,
) -> pl.DataFrame
```

Percentile bands for one factor, date by date: its mean, spread and chosen percentiles across every scenario.

This is the table behind a fan chart. `se` is the standard error of the mean: how precisely this many scenarios
pin down `mean`. When it is too large for the use at hand, simulate more scenarios.

**Args:**

- <u>factor (str):</u> the factor name.
- <u>quantiles (list[float] &#124; None):</u> the quantiles to report. Defaults to None, which gives 0.05, 0.25, 0.5, 0.75 and 0.95.
- <u>levels (bool):</u> summarize the raw simulated values (prices) instead. Defaults to False.
- <u>metric (str &#124; None):</u> the reading (see `metric_paths`). Defaults to None, the factor's default.

**Returns:**

<u>pl.DataFrame:</u> "date", "mean", "std", "se" and one "q<quantile>" column per quantile; a price's first row is empty, since a return starts after the first date.

**Raises:**

- <u>KeyError:</u> if the run has no such factor.

**As an example:**

```python
result = Scenarios.from_profiles(api_key="FINANCIAL_MODELING_PREP_KEY").simulate(n_simulations=2000)
result.summary_statistics("united_states_short_rate")
```

Which returns (the last three months of the five-year run, `se` left out):

| date       |   mean |    std |  q0.05 |  q0.25 |   q0.5 |  q0.75 |  q0.95 |
|:-----------|-------:|-------:|-------:|-------:|-------:|-------:|-------:|
| 2030-11-01 | 0.0441 | 0.0244 | 0.0047 | 0.0276 | 0.0445 | 0.0600 | 0.0856 |
| 2030-12-02 | 0.0440 | 0.0245 | 0.0042 | 0.0275 | 0.0437 | 0.0606 | 0.0854 |
| 2031-01-01 | 0.0441 | 0.0245 | 0.0049 | 0.0275 | 0.0442 | 0.0602 | 0.0858 |

## factors

```python
factors(category: str | None = None) -> list[str]
```

The factor names in this run, optionally only those of one category.

**Args:**

- <u>category (str &#124; None):</u> a category such as "equities" or "interest_rates". Defaults to None, every factor.

**Returns:**

<u>list[str]:</u> the matching factor names, in simulation order.

**Raises:**

- <u>ValueError:</u> if the category is not in the run but close to one that is ("equity" for "equities").

## describe

```python
describe(levels: bool = False, metric: Metric | None = None) -> pl.DataFrame
```

One row per factor: where it starts and where its scenarios end up. The first table to read after a simulation.

Every value is a decimal in one unit (see `metric_paths`): a rate as its yearly rate, a price as its yearly return
since the start. So "initial" is empty for a price, and its terminal columns are the yearly return over the whole
horizon. `terminal_q05` and `terminal_q95` are what 1 in 20 scenarios end below and above.

**Args:**

- <u>levels (bool):</u> report the raw simulated values (prices) instead. Defaults to False.
- <u>metric (str &#124; None):</u> the reading (see `metric_paths`). Defaults to None, each factor's default, which a factor the metric has no reading for also keeps.

**Returns:**

<u>pl.DataFrame:</u> "factor", "label", "category", "metric", "initial", "terminal_mean", "terminal_q05" and "terminal_q95".

**As an example:**

```python
from financescenarios import Scenarios

scenarios = Scenarios.from_profiles(api_key="FINANCIAL_MODELING_PREP_KEY")
result = scenarios.simulate(n_simulations=2000)
result.describe()
```

Which returns (3 of the 27 factors, without "label" and "metric"):

| factor                   | category       | initial | terminal_mean | terminal_q05 | terminal_q95 |
|:-------------------------|:---------------|--------:|--------------:|-------------:|-------------:|
| united_states_inflation  | inflation      |  0.0340 |        0.0283 |      -0.0005 |       0.0570 |
| united_states_short_rate | interest_rates |  0.0404 |        0.0441 |       0.0049 |       0.0858 |
| us_broad                 | equities       |         |        0.0983 |      -0.0465 |       0.2321 |

## step_at

```python
step_at(years: float) -> int
```

The step closest to a number of years from the start, e.g. `step_at(10)` is step 120 of a monthly run.

**Args:**

- <u>years (float):</u> years from the start.

**Returns:**

<u>int:</u> the step index.

**Raises:**

- <u>ValueError:</u> if `years` lies outside the simulated horizon.

## select

```python
select(factors: Sequence[str]) -> 'ScenarioSet'
```

The same run with only some factors, in the run's own order; categories, labels and fitted parameters follow.

**Args:**

- <u>factors (Sequence[str]):</u> the factors to keep.

**Returns:**

<u>ScenarioSet:</u> the narrowed run.

**Raises:**

- <u>KeyError:</u> if a factor is not in this run.

## sample

```python
sample(n: int, seed: int | None = None) -> 'ScenarioSet'
```

A random subset of `n` scenarios, each kept whole across every factor so their correlation survives. Handy for a
quick look, a lighter export, or checking how stable a statistic is.

**Args:**

- <u>n (int):</u> how many scenarios to keep, between 1 and `n_simulations`.
- <u>seed (int &#124; None):</u> the random seed, for a repeatable draw. Defaults to None.

**Returns:**

<u>ScenarioSet:</u> the sampled run.

**Raises:**

- <u>ValueError:</u> if `n` is not between 1 and `n_simulations`.

## horizon_summary

```python
horizon_summary(
    horizons: Sequence[float],
    factors: Sequence[str] | None = None,
    quantiles: Sequence[float] = (0.05, 0.25, 0.5, 0.75, 0.95),
    levels: bool = False,
    metric: Metric | None = None,
) -> pl.DataFrame
```

Percentiles of every factor at chosen horizons, one row per factor and horizon: where each factor is in 1, 5 and
10 years.

**Args:**

- <u>horizons (Sequence[float]):</u> years from the start; each maps to the nearest date of the run.
- <u>factors (Sequence[str] &#124; None):</u> the factors to include. Defaults to None, every factor.
- <u>quantiles (Sequence[float]):</u> the quantiles to report. Defaults to (0.05, 0.25, 0.5, 0.75, 0.95).
- <u>levels (bool):</u> report the raw simulated values (prices) instead. Defaults to False.
- <u>metric (str &#124; None):</u> the reading (see `metric_paths`). Defaults to None, each factor's default.

**Returns:**

<u>pl.DataFrame:</u> "factor", "horizon" (years), "date", "mean", "std" and one "q<quantile>" column per quantile.

**Raises:**

- <u>ValueError:</u> if a horizon lies outside the simulated horizon.

**As an example:**

```python
result.horizon_summary([1, 3, 5])
```

## to_long

```python
to_long(
    factors: Sequence[str] | None = None,
    levels: bool = False,
    metric: Metric | None = None,
) -> pl.DataFrame
```

Every path in one long table, one row per factor, scenario and date: the shape databases, plotting libraries and
group-by pipelines expect.

**Args:**

- <u>factors (Sequence[str] &#124; None):</u> the factors to include. Defaults to None, every factor.
- <u>levels (bool):</u> give the raw simulated values (prices) instead. Defaults to False.
- <u>metric (str &#124; None):</u> the reading (see `metric_paths`). Defaults to None, each factor's default.

**Returns:**

<u>pl.DataFrame:</u> "factor", "scenario", "date", "time" (years from the start) and "value".

## simulated_correlation

```python
simulated_correlation(
    factors: Sequence[str] | None = None,
    step_range: tuple[int, int] | None = None,
) -> pl.DataFrame
```

How the simulated factors move together, step by step, pooled over every scenario.

Use it to check that a run reproduces the correlations it was calibrated with, next to
`CalibrationResult.correlation_frame()`. Prices are measured by their log returns and every other factor by its
change, the same way calibration measures them.

**Args:**

- <u>factors (Sequence[str] &#124; None):</u> the factors to include. Defaults to None, every factor.
- <u>step_range (tuple[int, int] &#124; None):</u> the (start, stop) dates to measure over. Defaults to None, the whole path.

**Returns:**

<u>pl.DataFrame:</u> a "factor" column plus one column per factor; a factor that never moves correlates as empty.

**Raises:**

- <u>KeyError:</u> if a factor is not in this run.
- <u>ValueError:</u> if `step_range` leaves fewer than two dates.

## validate

```python
ScenarioSet.validate(*args: Any, **kwargs: Any) -> Any
```

Not available on a run: check one with `scenarios.validate(result)`, which also needs its calibration.

## FactorLabel

```python
class FactorLabel(BaseModel):
    title: str
    qualifier: str | None = None
```

A factor's display name in two parts: a headline and the line under it.

Charts and `describe()` tables show "Inflation — United States" or "US Broad — Equity" instead of the raw factor
name ("united_states_inflation", "us_broad"). Every simulated run carries one label per factor, taken from the
factor set.

**Attributes:**

- <u>title (str):</u> the headline, e.g. "Inflation" or "US Broad".
- <u>qualifier (str &#124; None):</u> the second layer, e.g. "United States" or "Equity"; None for no second layer.

## compare_runs

```python
compare_runs(
    runs: 'dict[str, ScenarioSet]',
    statistic: Literal['terminal_mean', 'terminal_median', 'terminal_std', 'terminal_q05', 'terminal_q95'] = 'terminal_mean',
    factors: Sequence[str] | None = None,
    levels: bool = False,
    metric: Metric | None = None,
    quantiles: Sequence[float] = (),
) -> pl.DataFrame
```

Put several runs side by side on one statistic of where each factor ends up, such as a baseline against a stress
regime.

The average tells only half of a stress test: a regime can leave the mean of a factor almost where it was while
making its bad outcomes much worse. `quantiles` adds that tail next to each run's column, such as `quantiles=(0.05,)`
for the level 1 in 20 scenarios end below. Each quantile column reads exactly like `describe()`'s `terminal_q05`:
the same metric and units as the run's own column, on the last date.

**Args:**

- <u>runs (dict[str, ScenarioSet]):</u> column name -> run, in the column order wanted.
- <u>statistic (str):</u> "terminal_mean" (default), "terminal_median", "terminal_std", "terminal_q05" or "terminal_q95".
- <u>factors (Sequence[str] &#124; None):</u> the factors to compare. Defaults to None, every factor of every run; a factor a run lacks is empty.
- <u>levels (bool):</u> compare the raw simulated values (prices) instead. Defaults to False.
- <u>metric (str &#124; None):</u> the reading (see `ScenarioSet.metric_paths`). Defaults to None, each factor's default.
- <u>quantiles (Sequence[float]):</u> quantiles between 0 and 1 to add per run, each as a "<run>_q<percent>" column right after that run's column, e.g. 0.05 gives "baseline_q05". Defaults to (), none.

**Returns:**

<u>pl.DataFrame:</u> a "factor" column plus one column per run, each followed by its quantile columns.

**Raises:**

- <u>ValueError:</u> if `runs` is empty, `statistic` is unknown, a quantile is outside 0 to 1, or a quantile column would take the name of a run.
- <u>As an example, with `result` a baseline of 2,000 scenarios on the default profiles:</u> 
- ```python
- from financescenarios import Scenarios, compare_runs
- oil_crisis = Scenarios.from_profiles(regime="oil_crisis", api_key="FINANCIAL_MODELING_PREP_KEY")
- shocked = oil_crisis.simulate(keep=2000)
- <u>compare_runs({"baseline":</u> result, "oil_crisis": shocked})
- <u>compare_runs({"baseline":</u> result, "oil_crisis": shocked}, quantiles=(0.05,))  # adds baseline_q05, oil_crisis_q05
- ```
- <u>Which returns, for the first call (4 of the factors):</u> 
- | factor                   | baseline | oil_crisis |
- <u>&#124;:</u> -------------------------|---------:|-----------:|
- | united_states_inflation  |   0.0283 |     0.0516 |
- | united_states_short_rate |   0.0441 |     0.0647 |
- | us_broad                 |   0.0983 |     0.0178 |
- | europe                   |   0.0768 |     0.0201 |
