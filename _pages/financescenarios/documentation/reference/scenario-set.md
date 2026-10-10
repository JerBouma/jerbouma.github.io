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
```

The result of a Monte Carlo scenario simulation run: every factor's simulated paths, one row per scenario.

```python
result = Scenarios.from_profiles(settings="default", factor_set="us_only").simulate(n_simulations=100)
result.describe()                                    # one row per factor
result.summary_statistics("united_states_short_rate")  # percentile bands date by date
result.plot("us_broad")                              # a fan chart
result.factors("equities")                           # the factor names in one category
```

Stores simulated paths as raw NumPy arrays (a per-simulation DataFrame at
N=1000+ simulations x multi-decade weekly grids is a real memory/perf cost
recomputed on every simulate() call). `to_dataframe()` and `summary_statistics()`
are the explicit conversion boundaries to Polars for downstream analysis.

**Attributes:**

- <u>paths (dict[str, np.ndarray]):</u> factor name -> array of shape (n_simulations, n_steps + 1).
- <u>time_grid (np.ndarray):</u> time points in years from t0, shape (n_steps + 1,).
- <u>dates (list[date]):</u> calendar dates matching time_grid.
- <u>factor_names (list[str]):</u> names of the simulated factors.
- <u>n_simulations (int):</u> number of simulated paths per factor.
- <u>seed (int &#124; None):</u> the random seed used to generate this scenario set.
- <u>calibration_metadata (dict[str, Any]):</u> calibrated parameters used per factor, for audit.
- <u>antithetic (bool):</u> whether these paths were drawn with antithetic variates (see generate_correlated_shocks): simulation i and i + n_simulations//2 are then exact shock negations of each other, not independent draws, so `summary_statistics()`'s `se` needs a different estimator (see there).
- <u>factor_categories (dict[str, str]):</u> factor name -> the category it was configured under (see `ScenariosConfig.factor_categories`), stamped on by `Scenarios.simulate()`. Lets a downstream reader (`financescenarios.portfolio.Portfolio`, a chart labeller) know what kind of series each path is without also holding the config that produced it. Empty on a hand-built ScenarioSet.

## label

```python
label(factor: str) -> FactorLabel
```

The factor's two-layer display identity: the stamped label when the
run carries one, a humanized slug otherwise (hand-built sets, runs
written before labels were recorded).

## is_level_factor

```python
is_level_factor(factor: str) -> bool
```

Whether a factor is simulated as a level (an equity, commodity or FX price, a
dividend index, the leading indicator, a portfolio or sleeve value) rather than as
an annualized decimal rate. See `factor_kind` for how each is reported.

## factor_kind

```python
factor_kind(factor: str) -> FactorKind
```

What a factor's simulated values are, which decides how each `metric` reads it:

- "price": a price or value (equities, FX, commodities, a dividend index, a
  portfolio or sleeve value). Changes are percentage changes.
- "growth": the growth rate of a price index (inflation, real estate). The rate
  is the value itself; its level is the index it compounds into, and changes
  are percentage changes of that index.
- "rate": a rate or spread read as a level (interest rates, the yield-curve
  components, credit spreads, unemployment, dividend yield, mortality). Changes
  are differences, in the rate's own units.
- "index": a stationary index with no rate reading (the OECD composite leading
  indicator). Changes are percentage changes.

A factor without a category (a hand-built set) is a "rate", read as itself.

## resolve_metric

```python
resolve_metric(factor: str, levels: bool = False, metric: Metric | None = None) -> str
```

The reading `metric_paths` returns for these arguments: "native" for `levels=True`,
the factor's default (`factor_kind`) when `metric` is None, otherwise `metric`
itself once checked to make sense for that factor.

**Raises:**

- <u>ValueError:</u> if `levels=True` is combined with a `metric`, the metric is unknown, or it has no meaning for the factor ("rate" of a price, "annualized" of a rate level).

## metric_paths

```python
metric_paths(factor: str, levels: bool = False, metric: Metric | None = None) -> np.ndarray
```

One factor's paths the way every summary, table and chart reads them. By default a
rate factor reads as its annualized decimal rate and a price as its annualized
return since start, (S_t / S_0) ** (1 / t) - 1, so a 769 -> 1,209 equity path over
five years reads as 9.5% a year, directly comparable with a 2.8% short rate; the
leading indicator reads as its index level.

In plain terms: `metric` picks how a number is expressed. The same simulated
inflation can be shown as the yearly rate (3.4%), as a price index that starts at
100, as the index's change over the last month or the last year, or as its total
or average yearly change since today.

| metric | price (equity, FX, ...) | growth rate (inflation, real estate) | rate level (rates, spreads, ...) |
|:-------|:-------------------------|:-------------------------------------|:---------------------------------|
| `rate` | not available | the simulated rate (default) | the simulated rate (default) |
| `level` | the price | the compounded index, 100 at start | the rate |
| `change` | % change over one step | % change of the index over one step | change over one step |
| `yoy` | % change over one year | % change of the index over one year | change over one year |
| `cumulative` | % change since start | % change of the index since start | change since start |
| `annualized` | yearly return since start (default) | average yearly growth since start | not available |

The leading indicator reads like a price, except that its default is `level`.
A change of a rate is a difference in its own units (0.005 is half a percentage
point), the convention for rates and spreads, not a percentage of a percentage.
A growth rate's index compounds the rate continuously, `100 * exp(cumsum(rate * dt))`
(`cumulative_index`). See [percentage change](https://en.wikipedia.org/wiki/Relative_change)
and [year over year](https://en.wikipedia.org/wiki/Year_over_year).

**Args:**

- <u>factor (str):</u> the factor name, must be a key in `paths`.
- <u>levels (bool):</u> return the native simulated values instead, exactly as `paths[factor]` holds them; cannot be combined with `metric`.
- <u>metric ("rate" &#124; "level" &#124; "change" &#124; "yoy" &#124; "cumulative" &#124; "annualized" &#124; None):</u> the reading in the table above; None keeps each factor's default.

**Returns:**

<u>np.ndarray:</u> shape (n_simulations, n_steps + 1). Points with no value (the start for a since-start return, the first step or year for a change) are NaN; a price path that reaches zero or below reads as -100%.

**Raises:**

- <u>KeyError:</u> if `factor` is not a key in `paths`.
- <u>ValueError:</u> see `resolve_metric`; and for `yoy` when the time step does not divide a year evenly.

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

Convert one factor's simulated paths into a Polars DataFrame, read the way
every report reads them (see `metric_paths`): a rate as itself, a level
factor as its annualized return since start (null at t0).

**Args:**

- <u>factor (str):</u> the factor name, must be a key in `paths`.
- <u>levels (bool):</u> the native simulated values (price levels) instead.
- <u>metric (str &#124; None):</u> the reading, "rate", "level", "change", "yoy", "cumulative" or "annualized" (see `metric_paths`); None keeps each factor's default.

**Returns:**

<u>pl.DataFrame:</u> one row per simulation, a "scenario" index column plus one column per date (ISO "YYYY-MM-DD"), the same scenario-by-time orientation as `paths[factor]` itself.

## discount_factor_paths

```python
discount_factor_paths(factor: str) -> np.ndarray
```

`discount_factors()` as the raw (n_simulations, n_steps + 1) array, DF(0) = 1: the
pathwise bank-account deflator the `solvency` functions discount with.

## discount_factors

```python
discount_factors(factor: str) -> pl.DataFrame
```

Compute the money-market (bank-account) discount factor path implied by
treating one factor as an instantaneous short rate: DF(t) = exp(-integral
of rate ds from 0 to t), discretized as exp(-cumsum(rate * time_step)).
DF(0) = 1 for every simulation.

This is the standard actuarial/financial transform from a simulated short
rate to a usable discounting curve, typically applied to the
`interest_rate` factor (or the yield curve's `rate_level`), but works on
any rate-like factor.

Not a stochastic deflator/pricing kernel: this is the plain money-market
numeraire's discount factor under whatever measure `factor` was simulated
under (P-measure, here, since every real_world-calibrated factor in this
project is real-world). It correctly discounts a *known* cash flow, but is
not by itself sufficient to correctly *price* a risky asset's uncertain
payoff under the real-world measure, which additionally needs a
market-price-of-risk adjustment (the Radon-Nikodym derivative between the
real-world and pricing measures) this project doesn't compute. See Cheng
& Planchet (2018) for the fuller stochastic-deflator construction this
function is a (deliberately simpler) building block of, not an
implementation of.

**Args:**

- <u>factor (str):</u> the factor to treat as a short rate, must be a key in `paths`.

**Returns:**

<u>pl.DataFrame:</u> one row per simulation, a "scenario" index column plus one discount-factor column per date, DF(0) = 1.0.

**Raises:**

- <u>KeyError:</u> if factor is not a key in `paths`.
- <u>ValueError:</u> if factor is a price or index level rather than a rate.

**References:**

- Cheng, P.K., Planchet, F. (2018). "Stochastic Deflator for an Economic Scenario Generator with Five Factors." Laboratoire SAF, Universite Claude Bernard Lyon 1. <https://arxiv.org/abs/1806.02991>

## cumulative_index

```python
cumulative_index(factor: str, initial_index: float = 100.0) -> pl.DataFrame
```

Compound one factor into an index level, treating it as an instantaneous
growth rate: index(t) = initial_index * exp(integral of rate ds from 0 to t),
discretized as initial_index * exp(cumsum(rate * time_step)).

This is the transform from a simulated *rate* factor (e.g. `inflation`,
`real_estate`) to a usable *index* (a CPI-style price level, a real estate
price index). Factors that already simulate a price level directly (e.g.
`equity`, `fx`) don't need this; they already are the index.

**Args:**

- <u>factor (str):</u> the factor to compound, must be a key in `paths`.
- <u>initial_index (float):</u> the index level at t=0.

**Returns:**

<u>pl.DataFrame:</u> one row per simulation, a "scenario" index column plus one index-level column per date, index(0) = initial_index.

**Raises:**

- <u>KeyError:</u> if factor is not a key in `paths`.
- <u>ValueError:</u> if factor is a price or index level rather than a rate, or initial_index is not a positive finite number.

## diagnose

```python
diagnose(factor: str | None = None, tolerance: float = 0.2) -> 'FactorDiagnostics | pl.DataFrame'
```

Without a factor, every factor this check applies to in one table: 'factor', 'simulated_mean',
'theoretical_mean', 'simulated_std', 'theoretical_std' and 'within_tolerance', one row each. Equities, FX
and other factors without a closed-form long-run distribution are left out.

Sanity-check one factor's simulated terminal-step distribution against the
closed-form stationary distribution implied by its calibrated Ornstein-
Uhlenbeck parameters: the same analytical check
test_simulate_paths_ou_long_run_statistics uses to validate the engine
(see validation-and-testing.md), promoted into a reusable diagnostic. Only
applicable to OU-calibrated factors (interest_rate under hull_white,
inflation, unemployment, real_estate, credit, leading_indicator, and the
yield curve's rate_level/rate_slope/rate_curvature), not equity
(regime-switching) or fx (GBM), which have no such closed form. `credit`
under its default constant-volatility fit is log-space (`family="log_ou"`,
see `fit_log_ou_process`); in that case this method compares log(simulated
values) against the theoretical log-space distribution, transparently.

A `within_tolerance=False` result doesn't necessarily mean something is
wrong: the terminal-step distribution only approaches the theoretical
stationary one given enough simulated time relative to the factor's
mean-reversion speed. A short horizon on a slowly-reverting factor will
legitimately look "unconverged" here without being miscalibrated.

The mean check's tolerance band is also floored at 3 Monte Carlo standard
errors of the simulated mean (`theoretical_std / sqrt(n_simulations)`), not
just the relative `tolerance` fraction: a factor whose calibrated
`long_run_mean` sits near zero (e.g. Japan's near-deflationary historical
inflation, ~7e-5) can otherwise fail the *relative* check on a difference
that's actually smaller than ordinary sampling noise for that
`n_simulations` count. `mean_difference` and `mean_noise_floor` in the
return value make that comparison explicit rather than leaving a caller to
eyeball simulated_mean vs theoretical_mean themselves.

**Args:**

- <u>factor (str &#124; None):</u> the factor name, must be a key in `paths` and `calibration_metadata`; None for the every-factor table.
- <u>tolerance (float):</u> relative tolerance: how far the simulated mean/std may differ from the theoretical value, as a fraction of the theoretical value, before `within_tolerance` is False.

**Returns:**

<u>FactorDiagnostics:</u> `simulated_mean`, `theoretical_mean`, `simulated_std`, `theoretical_std`, `mean_difference` (absolute, signed), `mean_noise_floor` (3 standard errors of the simulated mean; differences smaller than this are expected sampling noise, not a real divergence), and `within_tolerance`.

**Raises:**

- <u>KeyError:</u> if factor is not a key in `paths`.
- <u>NotOUCalibratedError:</u> (a ValueError, and an AttributeError) if factor's calibrated parameters aren't OU-shaped (no mean_reversion_speed/ long_run_mean/volatility), e.g. equity or fx.

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

One quick chart of this run, for a simple read rather than a report:

```python
result.plot()                                   # every factor, one fan chart each
result.plot("us_broad")                         # one factor's percentile fan
result.plot("us_broad", kind="paths")           # its individual simulated paths
result.plot("us_broad", kind="distribution")    # where it lands at the horizon
result.plot("united_states_inflation", metric="level")  # inflation as a price index
values.plot()                                   # a computed portfolio's value
values.plot(kind="sleeves")                     # and its composition over time
```

Every factor reads in the package's one reporting unit (see `metric_paths`),
so rates and returns share a percentage axis; `levels=True` draws prices and
portfolio values in money instead. The `plot_*` methods remain for finer
control (bands, bins, path counts, seeds).

**Args:**

- <u>factors (str &#124; Sequence[str] &#124; None):</u> one factor, several (drawn as a grid of fan charts), or None: a computed portfolio's `"portfolio"` path when this run holds one, otherwise every factor as a grid.
- <u>kind ("fan" &#124; "paths" &#124; "distribution" &#124; "sleeves"):</u> the chart for a single factor; "sleeves" draws a computed portfolio's composition.
- <u>levels (bool):</u> draw native prices and money values instead of returns.
- <u>ax:</u> an existing matplotlib Axes for a single-factor chart.
- <u>metric (str &#124; None):</u> the reading, "rate", "level", "change", "yoy", "cumulative" or "annualized" (see `metric_paths`); None keeps each factor's default.

**Returns:**

<u>matplotlib.figure.Figure:</u> the figure holding the chart.

**Raises:**

- <u>KeyError:</u> if a named factor is not in this run.
- <u>ValueError:</u> if `kind` is unknown, or a grid is asked for with a single-chart `kind`.

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

One factor's nested cross-simulation quantile bands around its median
path; delegates to `engine_view.plot_fan_chart` (imported at call time:
matplotlib loads only when a chart is drawn, and this model module stays
free of it), see that function's docstring for the full detail.

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

Every simulated path (or an `n_paths` sample) with the median on top;
delegates to `engine_view.plot_paths` (imported at call time, see
`plot_fan_chart`), see that function's docstring for the full detail.

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

One factor's final-step distribution across simulations; delegates
to `engine_view.plot_terminal_distribution` (imported at call time, see
`plot_fan_chart`), see that function's docstring for the full detail.

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

A small-multiples grid, one fan chart per factor; delegates to
`engine_view.plot_factors` (imported at call time, see `plot_fan_chart`),
see that function's docstring for the full detail.

## filter

```python
filter(
    factor: str,
    quantile_range: tuple[float, float],
    step_range: tuple[int, int] | None = None,
) -> 'ScenarioSet'
```

Select the subset of simulations whose value for one factor over a given step
range (a rate's average over the window, a price level's annualized return
across it, see `units`) falls within a given quantile range of that statistic's
distribution across all simulations, e.g. the 30% of paths with the highest
average interest rate, to isolate a "structurally high rates" scenario subset.
Useful for stress testing, sensitivity analysis, and narrative-driven scenario
construction.

Selection is by simulation index, applied identically across every factor: a
simulation selected for having high interest rates keeps its own correlated
inflation/equity/unemployment path too, not an independently filtered one.

**Args:**

- <u>factor (str):</u> the factor to filter on, must be a key in `paths`.
- <u>quantile_range (tuple[float, float]):</u> (lower, upper) quantiles, each in [0, 1] with lower < upper, of the per-simulation average to keep. For example (0.7, 1.0) keeps the top 30% of simulations by average value.
- <u>step_range (tuple[int, int] &#124; None):</u> (start, stop) step indices (like a Python slice) the average is computed over. Defaults to the full path.

**Returns:**

<u>ScenarioSet:</u> a new ScenarioSet with the same factors, time grid and dates, containing only the selected simulations.

**Raises:**

- <u>KeyError:</u> if factor is not a key in `paths`.
- <u>ValueError:</u> if quantile_range is not a valid (lower, upper) pair in [0, 1], step_range is empty or out of bounds, or no simulation falls within the requested range.

## filter_narrative

```python
filter_narrative(
    targets: dict[str, tuple[float, float]],
    step_range: tuple[int, int] | None = None,
    mode: Literal['sequential', 'joint'] = 'sequential',
) -> 'ScenarioSet'
```

Build a deterministic/narrative stress scenario by filtering on several
factors' quantile ranges at once, e.g. targets={"inflation": (0.8, 1.0),
"equity": (0.0, 0.2)} for a "stagflation" narrative (high inflation, weak
equity returns), or targets={"credit": (0.8, 1.0), "equity": (0.0, 0.2)} for
a "credit crunch" narrative. Each target is applied as a sequential filter()
call, narrowing the simulation set further with every additional factor: a
workflow layer on top of scenario filtering, translating a narrative into a
target-variable specification and deriving the deterministic scenario by
filtering rather than hand-picking one path.

**Args:**

- <u>targets (dict[str, tuple[float, float]]):</u> factor name -> (lower, upper) quantile range to filter on, applied in dict iteration order.
- <u>step_range (tuple[int, int] &#124; None):</u> shared step range for every target's filter() call. Defaults to the full path.
- <u>mode ("sequential" &#124; "joint"):</u> "sequential" (the default) applies each target to what the previous targets left, so every range after the first is a quantile *within* the already-narrowed subset: (0.7, 1.0) on rates then (0.0, 0.3) on equities keeps ~9% of paths. "joint" ranks every target against the full, unfiltered run and keeps the intersection, so each range means exactly what it says unconditionally; the result is order-independent but can be much smaller (or empty) when the targets pull against the correlation structure.

**Returns:**

<u>ScenarioSet:</u> the simulations satisfying every target simultaneously.

**Raises:**

- <u>KeyError:</u> if a target factor is not a key in `paths`.
- <u>ValueError:</u> if a quantile_range is invalid, or no simulation satisfies every target at once (raised by the filter() call that narrows to zero).

## rescale_scenario_cloud

```python
rescale_scenario_cloud(
    factor: str,
    mean_shift: float = 0.0,
    spread_multiplier: float = 1.0,
) -> 'ScenarioSet'
```

Rescale one factor's entire simulated cloud, shifting its cross-sectional
mean at every time step by `mean_shift` and/or widening or narrowing its
cross-sectional spread around that (shifted) mean by `spread_multiplier`,
without recalibrating or resimulating. An alternative belief-application mode
to this project's per-parameter belief overrides (config_model.py's
apply_*_beliefs functions), which substitute one calibrated parameter
*before* simulation: this reshapes the already-simulated cloud *after* the
fact instead, useful when a belief is naturally expressed as "shift/widen the
whole distribution" rather than as a specific parameter override.

At every time step t: new_value(sim, t) = (mean(t) + mean_shift) +
spread_multiplier * (old_value(sim, t) - mean(t)), where mean(t) is that
step's original cross-sectional mean across all simulations.
spread_multiplier == 1.0 and mean_shift == 0.0 is a no-op; spread_multiplier
> 1 widens dispersion (more extreme scenarios), < 1 narrows it. This preserves
each time step's cross-sectional shape (skew, quantile spacing) exactly, up to
the affine rescale, and does not alter the correlation structure between
factors (every other factor's path is untouched) or within a path over time
(each time step is rescaled around its own mean independently).

**Args:**

- <u>factor (str):</u> the factor to rescale, must be a key in `paths`.
- <u>mean_shift (float):</u> shift applied to every time step's cross-sectional mean.
- <u>spread_multiplier (float):</u> multiplier applied to every simulation's deviation from its time step's cross-sectional mean. Must be > 0.

**Returns:**

<u>ScenarioSet:</u> a new ScenarioSet with `factor`'s path replaced by the rescaled cloud; every other factor is unchanged.

**Raises:**

- <u>KeyError:</u> if factor is not a key in `paths`.
- <u>ValueError:</u> if mean_shift is not finite or spread_multiplier is not strictly positive and finite.

## summary_statistics

```python
summary_statistics(
    factor: str,
    quantiles: list[float] | None = None,
    levels: bool = False,
    metric: Metric | None = None,
) -> pl.DataFrame
```

Compute mean/std/standard-error/percentile paths per time step for one factor.

`se` (the standard error of the simulated mean, `std / sqrt(n_simulations)`)
is a convergence diagnostic: it says how precisely `mean` at a given step is
pinned down by this many simulations, independent of how spread out the
underlying distribution (`std`) is; useful for judging whether
`engine.n_simulations` is actually enough for the precision a given use case
needs, rather than picking a number and hoping. `std/sqrt(n)` assumes n i.i.d.
draws; under antithetic variates (`self.antithetic`), simulation i and
i + n_simulations//2 are exact shock negations of each other, not independent,
so `se` is instead computed from the n_simulations//2 pair-averages (the
actual i.i.d. unit under antithetic sampling), the standard antithetic-
variate standard-error estimator.

**Args:**

- <u>factor (str):</u> the factor name, must be a key in `paths`.
- <u>quantiles (list[float] &#124; None):</u> quantiles to compute. Defaults to [0.05, 0.25, 0.5, 0.75, 0.95].
- <u>levels (bool):</u> summarize the native simulated values (price levels) instead of the annualized return a level factor reports as.
- <u>metric (str &#124; None):</u> the reading, "rate", "level", "change", "yoy", "cumulative" or "annualized" (see `metric_paths`); None keeps each factor's default.

**Returns:**

<u>pl.DataFrame:</u> "date", "mean", "std", "se", and one column per requested quantile; a level factor's t0 row is null (a return starts after t0).

## factors

```python
factors(category: str | None = None) -> list[str]
```

The factor names in this run, optionally narrowed to one category.

**Args:**

- <u>category (str &#124; None):</u> a category from `factor_categories`, e.g. "equities" or "interest_rates". None (the default) returns every factor.

**Returns:**

<u>list[str]:</u> matching factor names, in simulation order.

**Raises:**

- <u>ValueError:</u> if `category` is absent but close to one this run has ("equity" for "equities").

## describe

```python
describe(levels: bool = False, metric: Metric | None = None) -> pl.DataFrame
```

One row per factor: its category, where it started, and where the
distribution ended up; the "what did I just simulate" read, without
picking a factor first.

**Args:**

- <u>levels (bool):</u> report the native simulated values (price levels) instead.
- <u>metric (str &#124; None):</u> the reading, "rate", "level", "change", "yoy", "cumulative" or "annualized" (see `metric_paths`); None keeps each factor's default, as does a factor the metric has no reading for.

**Returns:**

<u>pl.DataFrame:</u> "factor", "label" (the two-layer display identity, see `label()`), "category", "metric" (the reading each row is in, see `resolve_metric`), "initial", "terminal_mean", "terminal_q05", "terminal_q95", one row per factor in `paths`. Every value shares one unit (see `metric_paths`): a rate as an annualized decimal, a level factor as its annualized return since start, so "initial" is null for a level factor and its terminal columns read as the return a year over the whole horizon.

## step_at

```python
step_at(years: float) -> int
```

The time-grid index closest to `years` from t0, e.g. `step_at(10)` for the
10-year point of a monthly run (step 120).

**Raises:**

- <u>ValueError:</u> if `years` lies outside the simulated horizon.

## select

```python
select(factors: Sequence[str]) -> 'ScenarioSet'
```

The same run narrowed to a subset of factors, in this run's own simulation
order; categories, labels and calibration metadata follow the selection.

**Raises:**

- <u>KeyError:</u> if a requested factor is not in this run.

## sample

```python
sample(n: int, seed: int | None = None) -> 'ScenarioSet'
```

A random subset of `n` simulations (without replacement), every factor kept
jointly so each path's cross-factor correlation survives; handy for a quick
look, a lighter export, or a bootstrap of a statistic's stability.

**Raises:**

- <u>ValueError:</u> if `n` is not in [1, n_simulations].

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

Cross-simulation percentiles at chosen horizons, one row per factor and
horizon: the "where is each factor in 1, 5 and 10 years" table.

**Args:**

- <u>horizons (Sequence[float]):</u> horizons in years from t0; each maps to the nearest time-grid step (see `step_at`).
- <u>factors (Sequence[str] &#124; None):</u> factors to include; every factor by default.
- <u>quantiles (Sequence[float]):</u> quantiles to report, each in [0, 1].
- <u>levels (bool):</u> the native simulated values (price levels) instead of the annualized return a level factor reports as.
- <u>metric (str &#124; None):</u> the reading, "rate", "level", "change", "yoy", "cumulative" or "annualized" (see `metric_paths`); None keeps each factor's default, as does a factor the metric has no reading for.

**Returns:**

<u>pl.DataFrame:</u> "factor", "horizon" (years, as requested), "date", "mean", "std", and one "q<quantile>" column per quantile.

## to_long

```python
to_long(
    factors: Sequence[str] | None = None,
    levels: bool = False,
    metric: Metric | None = None,
) -> pl.DataFrame
```

Every path in tidy long format, one row per (factor, scenario, date): the
shape databases, plotting libraries and group-by pipelines expect.

**Args:**

- <u>factors (Sequence[str] &#124; None):</u> factors to include; every factor by default.
- <u>levels (bool):</u> the native simulated values (price levels) instead of the annualized return a level factor reports as (see `metric_paths`).
- <u>metric (str &#124; None):</u> the reading, "rate", "level", "change", "yoy", "cumulative" or "annualized" (see `metric_paths`); None keeps each factor's default, as does a factor the metric has no reading for.

**Returns:**

<u>pl.DataFrame:</u> "factor", "scenario", "date", "time" (years from t0), "value".

## simulated_correlation

```python
simulated_correlation(
    factors: Sequence[str] | None = None,
    step_range: tuple[int, int] | None = None,
) -> pl.DataFrame
```

Correlation of the simulated per-step moves across factors, pooled over every
simulation: the check that the run reproduces the dependence structure it was
calibrated with (compare against `CalibrationResult.correlation_matrix`).
Price-level categories (equities, commodities, fx) use log returns, every
other factor its first difference, matching how calibration measures moves.

**Args:**

- <u>factors (Sequence[str] &#124; None):</u> factors to include; every factor by default.
- <u>step_range (tuple[int, int] &#124; None):</u> (start, stop) time-point slice the moves are taken over. Defaults to the full path.

**Returns:**

<u>pl.DataFrame:</u> a "factor" column plus one column per factor; a factor with no variation (a deterministic path) correlates as null.

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

One factor's two-layer display identity: what it measures (`title`, e.g.
"Inflation") and which instance of that (`qualifier`, e.g. "United States").
Derived from the config (`ScenariosConfig.factor_labels`), stamped onto every
simulated run, and read wherever a factor is shown to a person (chart
titles, describe() tables), so the raw slug ("united_states_inflation")
stays an internal key, not a display string.

## compare_runs

```python
compare_runs(
    runs: 'dict[str, ScenarioSet]',
    statistic: Literal['terminal_mean', 'terminal_median', 'terminal_std', 'terminal_q05', 'terminal_q95'] = 'terminal_mean',
    factors: Sequence[str] | None = None,
    levels: bool = False,
    metric: Metric | None = None,
) -> pl.DataFrame
```

Put several runs side by side on one terminal-step statistic, e.g. a baseline
against the same factor set under a regime:
`compare_runs({"baseline": base, "oil_crisis": shocked})`.

**Args:**

- <u>runs (dict[str, ScenarioSet]):</u> column name -> run, in the column order wanted.
- <u>statistic (str):</u> the terminal-step statistic to report per factor.
- <u>factors (Sequence[str] &#124; None):</u> factors to compare; defaults to every factor of every run, in first-seen order. A factor a run lacks reads as null.
- <u>levels (bool):</u> compare native simulated values (price levels) instead of the annualized return since start a level factor reports as.
- <u>metric (str &#124; None):</u> the reading, "rate", "level", "change", "yoy", "cumulative" or "annualized" (see `ScenarioSet.metric_paths`); None keeps each factor's default, as does a factor the metric has no reading for.

**Returns:**

<u>pl.DataFrame:</u> a "factor" column plus one column per run.

**Raises:**

- <u>ValueError:</u> if `runs` is empty or `statistic` is unknown.
