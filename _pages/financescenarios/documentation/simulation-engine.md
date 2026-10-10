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

The engine is the part that actually produces the scenarios. It draws random shocks that move together the way history says they should, then steps every variable forward one month (or week, or year) at a time, thousands of times over. What comes out is a `ScenarioSet`: every simulated scenario, with methods to summarize, slice, filter and chart it.

The simulation engine is asset-class-agnostic: it knows nothing about interest rates, inflation, equities or unemployment specifically. It only knows how to advance a set of named factors, one time step at a time, using a step function supplied by the caller for each factor. `scenarios_controller.py` is what supplies the actual interest-rate, inflation, equity and unemployment step functions.

A Monte Carlo simulation, the technique used here, runs the same random process many times with different random draws, in order to build up a distribution of possible outcomes rather than a single prediction. Each individual run is called a path or a simulation.

## Engine settings

These come from the `engine` section of a settings profile (see [configuration](/projects/financescenarios/docs/configuration)) and are validated by `EngineConfig`:

| Field | Type | Default | Meaning |
|---|---|---|---|
| `n_simulations` | integer, greater than 0 | `1000` | Number of independent Monte Carlo paths to simulate. |
| `n_steps` | integer, greater than 0 | `52` | Number of time steps per path, after the starting point. `simulate(years=30)` sets it for one call from a horizon in years, at the profile's own `frequency`. |
| `frequency` | one of `daily`, `weekly`, `monthly`, `quarterly`, `semi-yearly`, `yearly` | `weekly` | How much time each step represents. Converted internally to a year fraction (`time_step`), for example `weekly` becomes `1/52`. |
| `seed` | integer or `null` | `null` | Random seed. Fixing it makes a run fully reproducible: the same seed and the same inputs always produce byte-identical output. |
| `antithetic` | boolean | `false` | Use antithetic variates: draw half the independent shock sets and pair each with its exact negation, before correlating. Standard Monte Carlo variance reduction: lower variance in the simulated distribution for the same `n_simulations`, at the cost of half the draws being deterministic given the other half rather than fully independent. `n_simulations` must be even when enabled. On the `default` factor set with 2,000 scenarios it cut the seed-to-seed spread of a 60/40's five-year 5th percentile and mean by about a quarter (1.48 to 1.15 and 0.78 to 0.56, over 8 seeds); it stays off in the shipped settings so published numbers do not move. Under `shock_distribution: "student_t"`, only the correlated Gaussian component is exactly negated; the chi-square tail-scale variable is paired via antithetic uniforms instead (negatively, not identically, correlated), so every simulation still contributes independent tail-scale information; see `generate_correlated_shocks`'s own docstring for why a literal shared draw there would have silently defeated variance reduction for tail statistics specifically. |
| `shock_distribution` | one of `gaussian`, `student_t` | `gaussian` | The joint distribution correlated shocks are drawn from; see "Fat tails and tail dependence" below. |
| `degrees_of_freedom` | float, greater than 2 | `5.0` | Student-t degrees of freedom, only used when `shock_distribution: student_t`. Lower means fatter tails and stronger tail dependence. |
| `correlation_shrinkage` | number in [0, 1], or `auto` | `0.1` | How far the estimated correlations are pulled in before use, to tame noise. A number blends them that far toward their average. `auto` pulls them toward no correlation by the data-driven amount of [Schäfer and Strimmer (2005)](https://doi.org/10.2202/1544-6115.1175): more when correlations rest on few observations. Trained on history before 2012 or 2016 and scored on the years after, `auto` cut the default factor set's correlation error by 7.5% and 1.6%. The shipped `settings/default.yaml` (and every settings profile extending it) uses `auto`; a configuration without the key keeps 0.1. The intensity used and how far the matrix had to be repaired to be valid are recorded on the calibration (`correlation_shrinkage`, `correlation_repair`). |
| `shared_equity_regimes` | boolean | `false` | Draw every regime-switching equity's calm/crisis switches from one shared stream of random numbers, so markets tend to enter and leave crises together. Each equity keeps its own fitted switching probabilities, so paths still differ where those differ. With separate streams (the default), one market can sit in crisis while another is calm, which dilutes the simulated correlation between equities: on the `core` factor set the mean gap to the calibrated correlations fell from 0.094 to 0.044 and the largest from 0.135 to 0.081. The shipped `settings/default.yaml` sets it to `true`. |

## Building one simulation run

1. **Time grid.** `build_time_grid(n_steps, time_step)` produces the numeric time points, in years from the start date: `[0, time_step, 2*time_step, ...]`. `build_date_grid` (in `helpers.py`) produces the matching calendar dates.
2. **Correlated shocks.** `generate_correlated_shocks` draws independent random numbers, one per factor, per time step, per simulation, and then correlates them using a Cholesky decomposition of the factor correlation matrix (see `Dependence` for how that matrix is built). A Cholesky decomposition factorises a valid correlation matrix into a lower-triangular matrix; multiplying independent random draws by that matrix produces draws with the target correlation. This is the mechanism that makes interest rates, inflation and equity returns move together realistically instead of independently. By default the independent draws are standard normal (`shock_distribution: gaussian`); see "Fat tails and tail dependence" below for the `student_t` alternative.
3. **Regime pre-simulation.** For equities, which regime (for example "bull" or "bear") is active at each time step is resolved once upfront by `simulate_regime_path`, as its own discrete Markov chain draw, using a separate random generator offset from the main seed by a large constant. This keeps the discrete regime draws statistically independent from the continuous correlated shocks, even when both are derived from the same user-supplied seed.
4. **Stepping loop.** `simulate_paths` resolves the factor dependency graph into a valid order using a topological sort (an ordering where every factor appears only after everything it depends on), then advances every factor, for every simulation, one time step at a time, by calling that factor's step function.

{% raw %}
<div class="mermaid">
flowchart TD
    start[Simulation start] --> timegrid[Build time grid and date grid]
    timegrid --> shocks[Generate correlated shocks via Cholesky decomposition]
    shocks --> order[Resolve factor order via topological sort]
    order --> loop[Step every factor forward one time step at a time]
    loop --> loop
    loop --> scenarioset[Wrap result into a ScenarioSet]
</div>
{% endraw %}

## Fat tails and tail dependence

A Gaussian correlation structure (the default) is a real limitation for a *shock*/stress-testing model specifically: it structurally cannot produce simultaneous extreme moves across factors more often than a Gaussian implies, understating exactly the kind of joint tail event ("everything sells off together") stress testing exists to capture. This is the standard, long-documented critique of Gaussian-copula Monte Carlo models in the risk literature.

`engine.shock_distribution: "student_t"` replaces the Gaussian draw in step 2 above with a multivariate Student-t distribution (a t-copula, Demarta & McNeil 2005), without changing anything else about the engine: `generate_correlated_shocks` draws correlated Gaussian shocks exactly as before, then divides every factor's shock at a given (simulation, step) by the *same* `sqrt(chi-square(degrees_of_freedom) / degrees_of_freedom)` draw. Sharing that divisor across every factor at that instant is what creates *tail dependence* (an extreme move in one factor becomes more likely to coincide with an extreme move in another), not just fatter marginal tails computed independently per factor.

The result is rescaled by `sqrt((degrees_of_freedom - 2) / degrees_of_freedom)` so every shock keeps unit variance regardless of `shock_distribution`; every calibrated `volatility` parameter elsewhere in this project means the same thing either way, and only the shape of the tail changes. Lower `degrees_of_freedom` means fatter tails and stronger tail dependence; the value must be greater than 2, since a Student-t distribution's variance is only finite above that.

This closes the fat-tailed dependence gap `Dependence` previously documented as future work, using the standard tractable construction (a single shared degrees-of-freedom parameter across every factor) rather than the more flexible but substantially more complex per-pair copula constructions surveyed there (Pfeifer & Ragulina's patchwork copula, Josaphat & Syuhada's dependent CVaR extension); those remain a natural next step if a use case needs asymmetric or pairwise-varying tail behavior a single shared t-copula can't express.

## Step functions

Every step function has the same signature: `(current_values, shocks, time_step, step_index, paths) -> next_values`, where `current_values`/`shocks`/`next_values` are each `(n_simulations,)` arrays: one call per `(factor, step_index)` advances every simulation at once, not one call per `(factor, step_index, simulation_index)`.

`simulate_paths` used to loop over both step and simulation, ~4.2M individual Python-level calls for a realistic 1000-simulation x 520-step x 8-factor run; since every step function's own math is already elementwise (a NumPy ufunc formula broadcasts identically over a scalar or an array), collapsing the inner simulation loop into one vectorized call per `(factor, step_index)` needed no formula changes, only rewriting the handful of step functions that carried per-simulation state or did per-simulation lookups (`GARCHStepper`'s variance array, the equity regime lookup, and the business-cycle/Phillips-curve/FX-IRP covariate reads in `scenarios_controller.py`) to operate on the whole array instead of indexing a single simulation out of it.

`step_index` and `paths` let a factor look up any externally pre-resolved state it needs beyond the continuous shock, such as equities looking up its pre-simulated regime for that step across every simulation at once. `paths` is the in-progress `paths` dict `simulate_paths` is filling in for the current run: since factors are stepped in topologically sorted dependency order within each time step, a factor simulated later (e.g. unemployment) can read another factor's value already written for that same step (e.g. inflation's move, used as the Phillips-curve input in `Unemployment`). Interest rates and inflation ignore the trailing arguments.

Every plain OU-family step function (`step_ou_process` and its near-duplicates: interest rates, inflation, unemployment, the yield-curve/credit-curve factors, real estate, credit, leading indicator) implements the process's *exact* discrete-time transition, not an Euler-Maruyama approximation of it: `x_{t+dt} = theta + (x_t - theta)*e^{-a*dt} + sigma*sqrt((1 - e^{-2*a*dt})/(2*a))*eps_t`, the closed-form solution of `dx = a(theta - x)dt + sigma*dW` (Vasicek, 1977). Zero discretization error, and unconditionally stable for any `mean_reversion_speed * time_step`, unlike Euler-Maruyama, which oscillates/diverges once that product reaches 2.

GARCH-volatility factors (`GARCHStepper`) and CIR (`step_cir`) are the exceptions: both still step via Euler-Maruyama, since neither has a closed-form exact transition (GARCH's variance is itself stochastic and time-varying; CIR's noncentral-chi-square exact transition is a materially different, harder scheme; see `InterestRates`). Every other step function (equity, FX, commodities, dividend yield) implements an Euler-Maruyama discretization of its own SDE, the standard first-order scheme that Ito's lemma justifies for approximating an SDE's solution over a small time step (Kohn, 2003).

## `ScenarioSet`

`ScenarioEngine.simulate()` returns a `ScenarioSet`, defined in `engine/engine_model.py`. It stores the raw simulated paths as NumPy arrays rather than a table, since a table for 1000 or more simulations across a multi-decade weekly grid is a real memory and performance cost that would otherwise be paid on every run. Two methods convert to a table on demand:

Every one of these reads a factor the way [units](/projects/financescenarios/docs/units) describes: by default a rate as its annualized rate, a price (equities, FX, commodities, a dividend index, portfolio values) as its annualized return since start, `(S_t / S_0) ** (1 / t) - 1`, null at `t0`, and the leading indicator as its index level. Every method below takes `metric=` for another reading (`"rate"`, `"level"`, `"change"`, `"yoy"`, `"cumulative"`, `"annualized"`) and `levels=True` for the native simulated values. `metric_paths(factor, metric=...)` is that transform on its own, `factor_kind(factor)` says which of the four kinds (price, growth rate, rate, index) a factor is, and `paths[factor]` always holds the native values.

- `to_dataframe(factor)` returns a scenario-by-time table for a single named factor: one row per simulation, a `scenario` index column plus one column per date, the same orientation as `paths[factor]` itself. `discount_factors()`/`cumulative_index()` share the shape.
- `summary_statistics(factor, quantiles=None)` returns `date`, `mean`, `std`, `se` and one column per requested quantile (the default quantiles are `0.05`, `0.25`, `0.5`, `0.75` and `0.95`), computed across all simulations at each time step. `se` (`std / sqrt(n_simulations)`) is the standard error of the simulated mean: how precisely that mean is pinned down by this many simulations, a convergence diagnostic for judging whether `engine.n_simulations` is actually enough for a given use case.
- `discount_factors(factor)` and `cumulative_index(factor, initial_index=100.0)` treat a rate-like factor (e.g. `interest_rate`, `inflation`, `real_estate`) as an instantaneous rate and compound it into a usable money-market discount factor (`exp(-cumsum(rate * time_step))`, `DF(0) = 1`) or index level (`exp(cumsum(rate * time_step))`, scaled by `initial_index`), the transform every downstream reserving/reporting use needs on top of a raw rate.

  This is the plain bank-account numeraire's discount factor under whichever measure `factor` was simulated under, not a full stochastic deflator/pricing kernel; that would additionally need a market-price-of-risk adjustment. For a `method="knw_sv"` pair, `KnwSvQ.deflator()` (see `KnwSvQ`'s Stochastic deflator section) builds exactly that adjustment, [Cheng & Planchet (2018)](https://arxiv.org/abs/1806.02991)'s own construction, from an already P-measure-simulated run's paths; this generic `discount_factors` stays the simpler bank-account-only building block for every other factor. Factors that already simulate a price level directly (`equity`, `fx`) don't need this; they already are the index.
- `diagnose()` with no factor returns the same check for every factor it applies to as one table (factor, simulated and theoretical mean and spread, `within_tolerance`). Commodity prices and dividend yields are fitted on their logarithm, so they are compared in log space, like a log-OU credit spread. A factor that follows a belief path (an anchored rate) is compared against its own fitted level, so it can read `false` by design.
- `diagnose(factor, tolerance=0.2)` sanity-checks one OU-calibrated factor's simulated terminal-step distribution against the closed-form stationary mean/std implied by its calibrated parameters (`long_run_mean`, `sqrt(volatility^2 / (2*mean_reversion_speed))`), the same analytical check `test_simulate_paths_ou_long_run_statistics` uses to validate the engine, promoted into a reusable diagnostic.

  Only applies to OU-family factors (not `equity` or `fx`); a `within_tolerance=False` result can just mean the horizon is short relative to the factor's mean-reversion speed, not that anything is wrong.

  `ScenarioEngine.simulate()` (`engine_controller.py`'s `_check_ou_stationary_convergence`) already runs this automatically for every plain-`OUParams` factor (not `OUCovariateParams`/`GARCHParams`/`MovingTargetOUParams`; their own stationary distributions aren't this simple closed form) once its horizon spans at least 3 mean-reversion time constants, logging a warning on divergence rather than requiring a caller to remember to call `diagnose()` themselves; calling it directly is still useful for a specific factor's full numeric detail, or one that the automatic pass skipped as too short a horizon to trust.

### Slicing, reshaping and comparing

- `result["us_broad"]` returns one factor's raw `(n_simulations, n_steps + 1)` array, and `step_at(years)` the time-grid index nearest a horizon (`step_at(10)` is step 120 on a monthly grid).
- `select(factors)` narrows a run to a subset of factors (categories, labels and calibration metadata follow), and `sample(n, seed=None)` draws `n` whole simulations without replacement, every factor kept jointly so the cross-factor correlation survives.
- `horizon_summary(horizons, factors=None, quantiles=...)` is the "where is each factor in 1, 5 and 10 years" table: one row per factor and horizon with `mean`, `std` and the requested quantiles.
- `to_long(factors=None)` returns every path in tidy long format (`factor`, `scenario`, `date`, `time`, `value`), the shape databases and group-by pipelines expect. It materializes `n_factors * n_simulations * (n_steps + 1)` rows, so narrow it with `factors` (or `sample()` first) on a large run.
- `simulated_correlation(factors=None, step_range=None)` measures the correlation of the simulated per-step moves, pooled over every simulation: log returns for price-level categories (equities, commodities, FX), first differences for everything else. Set it next to `CalibrationResult.correlation_matrix` to check the run reproduces the dependence it was calibrated with; a deterministic path correlates as null.
- `compare_runs({"baseline": base, "oil_crisis": shocked}, statistic="terminal_mean")` (exported at the package root) puts several runs side by side on one terminal-step statistic (`terminal_mean`, `terminal_median`, `terminal_std`, `terminal_q05`, `terminal_q95`), with null where a run lacks a factor. The [README](/projects/financescenarios#applying-stress-regimes)'s baseline-versus-regime table is exactly this call.

On the calibration side, `CalibrationResult.describe()` lists every fitted process with its `half_life_years` (`ln 2 / mean_reversion_speed`, how long a shock takes to decay halfway back), and `CalibrationResult.correlation_frame()` returns the calibrated correlation matrix as a labelled table to set beside `simulated_correlation()`.

`ScenarioSet` also carries `calibration_metadata`: the calibrated parameters that were actually used for the run, keyed by factor name, for audit and reproducibility.

## Scenario filtering

`filter(factor, quantile_range, step_range=None)` selects the subset of simulations whose value for one factor over a given step range (a rate's average across the window, a price level's annualized return from the window's first date to its last) falls within a given quantile range of that statistic's distribution across all simulations. For example, `result.filter("interest_rate", quantile_range=(0.7, 1.0))` keeps the 30% of simulated paths with the highest average interest rate, isolating a "structurally high rates" scenario subset, useful for stress testing, sensitivity analysis, and narrative-driven scenario construction.

Selection is by simulation index, applied identically across every factor in the returned `ScenarioSet`: a simulation selected for having high interest rates keeps its own correlated inflation/equity/unemployment path too, not an independently filtered one. This preserves the cross-factor correlation structure within the filtered subset.

`filter()` operates purely on already-simulated output; it doesn't recalibrate or re-run the Monte Carlo simulation, so it's cheap to call repeatedly with different factors/ranges on the same `ScenarioSet`.

## Narrative stress scenarios

`filter_narrative(targets, step_range=None, mode="sequential")` builds a deterministic/narrative stress scenario by chaining `filter()` across several factors' quantile ranges at once. For example:

```python
stagflation = result.filter_narrative(
    {
        "inflation": (0.8, 1.0),  # top 20% by average inflation
        "equity": (0.0, 0.2),  # bottom 20% by average equity return
    }
)
```

narrows to the simulations satisfying every target simultaneously, the workflow layer on top of `filter()`: translate a narrative ("stagflation", "credit crunch") into a target-variable specification (which factors, which quantile band), then derive the scenario by filtering rather than hand-picking a single path. Targets are applied in dict order, each narrowing the surviving simulation set further; an unsatisfiable combination raises the same `ValueError` an individual `filter()` call raises when nothing matches.

That sequential reading means every range after the first is a quantile *within* what the earlier targets left: `(0.7, 1.0)` on rates followed by `(0.0, 0.3)` on equities keeps roughly 9% of paths, the weakest equity paths among the high-rate ones. `mode="joint"` instead ranks every target against the full, unfiltered run and keeps the intersection, so each range means exactly what it says unconditionally and the result doesn't depend on dict order. A joint selection can be much smaller, or empty, when the targets pull against the correlation structure. `filter()` also rejects an empty or out-of-bounds `step_range` rather than averaging over nothing.

## Scenario-cloud belief rescaling

`rescale_scenario_cloud(factor, mean_shift=0.0, spread_multiplier=1.0)` is an alternative to the config-driven, per-parameter belief overrides (`apply_*_beliefs` in `config_model.py`, see [configuration](/projects/financescenarios/docs/configuration)): instead of substituting a calibrated parameter *before* simulation, it reshapes the already-simulated cloud *after* the fact, shifting one factor's cross-sectional mean at every time step by `mean_shift` and/or widening or narrowing its cross-sectional spread around that mean by `spread_multiplier`. Useful when a belief is naturally expressed as "shift/widen the whole distribution" rather than as a specific model parameter; for example, a user who trusts the calibrated dynamics but wants a wider or narrower cone of simulated outcomes overall:

```python
wider_equity = result.rescale_scenario_cloud("equity", spread_multiplier=1.3)
```

Every time step is rescaled around its own cross-sectional mean independently, preserving that step's cross-sectional shape (skew, quantile spacing) up to the affine transform, and every other factor's path is left untouched. Like `filter()`, this operates purely on already-simulated output: no recalibration or resimulation.

## Calibration persistence

`Scenarios.simulate()` calibrates and simulates in one call. For reproducibility or offline use, the two steps split apart:

```python
calibration = scenarios.calibrate(config)  # talks to FinanceToolkit
calibration.save("calibration.json")

# later, possibly without network/API access:
loaded = CalibrationResult.load("calibration.json")
offline_scenarios = Scenarios(toolkit=None, n_simulations=5000, seed=123)
result = offline_scenarios.simulate(config, calibration=loaded)
```

`scenarios.save(result)` writes the run to its own folder with the config that produced it (`config.yaml` and `factors.yaml`) and the calibration (`calibration.json`), so a run on disk reads back, and replays, with no network access at all:

```python
from financescenarios import Scenarios, load_config, read_run, read_run_calibration

path = scenarios.save(result, "results/")  # e.g. results/20260819T082519Z-419a81fd
same = read_run(path)  # the stored paths, as a ScenarioSet

calibration = read_run_calibration(path)
config = load_config(path / "config.yaml", path / "factors.yaml")
offline = Scenarios(toolkit=None, n_simulations=20_000, n_steps=config.engine.n_steps)
wider = offline.simulate(config, calibration=calibration)
```

`write_run(result, config, output_dir, calibration=...)` is the lower-level function `save()` calls, for a result and config you hold yourself.

In a script, `scenarios.last_calibration` holds whatever the most recent `simulate()` ran on, whether it built one itself or was handed one; no need to call `calibrate()` separately just to keep a copy.

Re-running the same calibration under a different seed or path count needs no new instance; `simulate()` takes both as per-call overrides, which is the cheap way to separate a real result from Monte Carlo noise:

```python
calibration = scenarios.calibrate()
spread = [scenarios.simulate(calibration=calibration, seed=seed) for seed in range(5)]
wider = scenarios.simulate(calibration=calibration, n_simulations=20_000)
```

`Scenarios.calibrate(config)` runs every enabled factor's calibration and the cross-factor correlation matrix, returning a `CalibrationResult` (calibrated parameters, correlation matrix, factor names, dependencies) without running the Monte Carlo engine. `Scenarios.simulate(config, calibration=...)` skips calibration entirely when a `CalibrationResult` is supplied; FinanceToolkit is never touched. This is useful for: reproducing a past run byte-for-byte without depending on FinanceToolkit still returning the same historical window; replaying a calibration with no network/API key at all (`Scenarios(toolkit=None, ...)`); and cheaply re-simulating with a different `seed`, `n_simulations`, engine setting, shock or time-varying `long_run_mean` path without re-fetching data each time.

A config passed to `simulate()` runs on its own `engine` block (steps, frequency, simulations, seed) when that differs from the instance's. Fixed belief overrides (a constant `mean_reversion_speed`, `long_run_mean` or `volatility`, an equity's regime means) are different: they are applied while calibrating, so a `CalibrationResult` records the ones it was made with, and `simulate()` refuses to replay it under a config whose fixed overrides differ, naming the factors, rather than silently keeping the old ones. Recalibrate with `calibrate(config)` for those; a calibration saved before this record existed only logs a warning.

Which factors get simulated is read from the `CalibrationResult` itself (which keys are present in `calibrated_params`), not from `config.*.enabled`: a loaded or reused calibration is the source of truth, even if the `config` passed to `simulate()` differs from the one originally passed to `calibrate()`.
