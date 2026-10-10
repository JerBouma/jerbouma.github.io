---
title: Architecture
seo_title: Architecture Documentation – Finance Scenarios
excerpt: "The code is split into three kinds of file so each can be read and tested on its own. This page shows which folder does what and the order a run goes through, from settings to simulated scenarios."
description: "The Finance Scenarios module layout (model, controller and view files) and the data flow from configuration to simulated scenarios."
author_profile: false
permalink: /projects/financescenarios/docs/architecture
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

{% include mermaid.html %}

The code is split into three kinds of file so each can be read and tested on its own: one kind does the maths, one fetches data and wires the steps together, and one draws the charts. This page shows which folder does what and the order a run goes through, from settings to simulated scenarios.

Finance Scenarios separates pure calculation from orchestration from presentation. Every module follows one of four file types:

- **`_model.py`**: pure functions and data schemas. No I/O, no dependency on FinanceToolkit, with no exceptions: reading a config off disk lives in `config_controller.py`, and the metric/regression functions that delegate their maths to FinanceToolkit live in `metrics_controller.py`/`factor_exposure_controller.py`, leaving their `_model.py` files holding the result schemas. Given the same inputs, a model function always produces the same output. This is where the mathematics lives.
- **`_controller.py`**: orchestration. Pulls data from a FinanceToolkit `Toolkit` instance, calls the matching model functions, and exposes the result. This is where FinanceToolkit is called. Controllers import `Toolkit` for type hints only (under `TYPE_CHECKING`) and import FinanceToolkit at call time where they build one, so `import financescenarios` and an offline replay of a saved calibration never load it (2.8 s and 205 MB instead of 3.7 s and 254 MB).
- **`_view.py`**: presentation. Pure matplotlib rendering of what a model object already holds: no calculation beyond percentiles, no I/O, no FinanceToolkit. No `_model.py`/`_controller.py` imports a `_view.py` at module level; the `plot_*` convenience methods on `ScenarioSet`/`CalibrationResult` delegate via a call-time import, so matplotlib loads only when a plot is actually asked for. `engine/engine_view.py` hosts the shared chart style; see [plotting](/projects/financescenarios/docs/plotting).
- **`helpers.py`**: small utilities shared across modules (random number generation, calendar date construction, logging setup).

Each folder holds exactly one `_controller.py`, named after the folder itself, the same layout FinanceToolkit uses. A second controller means a second concern and gets its own folder (`portfolio/factor_exposure/`, `validation/naic_goes/`); the package root's own entry point (`scenarios_controller.py`) is the only controller not named after its folder, mirroring FinanceToolkit's root `toolkit_controller.py`. Every module in `financescenarios/` carries one of the three suffixes; `helpers.py` and `__init__.py` are the only exceptions, and there are no others: a module that orchestrates, reads or writes anything is a `_controller.py` even when it isn't tied to one factor (`run_io_controller.py`, `profiles_controller.py`, `validation/cache_controller.py`).

## Module map

Factor packages live under `financescenarios/factors/`, jointly-fit model families (`knw`, `knw_sv`, `knw_sv_q`) under `financescenarios/models/`; the bare folder names below are used for brevity.

| Module | Responsibility |
|---|---|
| `scenarios_controller.py` | `Scenarios`, the root controller. Wires calibration, dependence and the engine together into one `.simulate()` call, and `build_toolkit()`, which constructs the embedded FinanceToolkit `Toolkit` instance from `config.toolkit`. |
| `config_controller.py` | `load_config()`/`load_profiles()`, the only place a config is read off disk. |
| `config_model.py` | `ScenariosConfig` and its nested settings, loaded from a named settings profile (run settings, `settings/<id>.yaml`) merged with a named factor-set profile (factor definitions, `factor-sets/<id>.yaml`) via `load_profiles()` (or two explicit file paths via `load_config()`). |
| `profiles_controller.py` | Generic `extends`-chain-walking and deep-merge machinery shared by every named-preset directory (`settings/`, `factor-sets/`, `regimes/`, `portfolios/`; see below), plus `resolve_directory()`, which falls back to the copy of those presets bundled in the package when no such directory exists where the caller is running. |
| `calibration/calibration_controller.py` | `Calibration`, dispatches calibration across all four factors and applies belief overrides. |
| `calibration/calibration_model.py` | `fit_ou_process`, the Ornstein-Uhlenbeck fitter shared by interest rates and inflation. |
| `interest_rates/` | `InterestRates` controller and the Hull-White / CIR short-rate model. |
| `inflation/` | `Inflation` controller and the inflation step function. |
| `equities/` | `Equities` controller and the regime-switching lognormal equity model. |
| `unemployment/` | `Unemployment` controller and the Phillips-curve-augmented mean-reverting unemployment model. |
| `term_structure/` | `TermStructure` controller and the opt-in Nelson-Siegel dynamic yield curve model (`rate_level`/`rate_slope`/`rate_curvature`). |
| `real_estate/` | `RealEstate` controller (opt-in). No dedicated model file; calibrates via `calibration_model.fit_ou_process`/`step_ou_process` directly. |
| `credit/` | `Credit` controller (opt-in). Same as `real_estate/`: no dedicated model file, reuses `calibration_model` directly. |
| `leading_indicator/` | `LeadingIndicator` controller (opt-in). Same as `real_estate/`. |
| `fx/` | `FX` controller and the opt-in geometric Brownian motion FX model (`fx_model.py`). |
| `commodities/` | `Commodities` controller and the opt-in Schwartz (1997) mean-reverting log-price commodity model (`commodities_model.py`). |
| `dividend_yield/` | `DividendYield` controller and the opt-in Ahlgrim/D'Arcy/Gorvett (2005) mean-reverting log-yield model (`dividend_yield_model.py`), derived from `Close`/`Dividends` data no other factor already fetches for this purpose. |
| `mortality/` | `Mortality` controller and the opt-in Cairns-Blake-Dowd two-factor stochastic mortality model (`mortality_level`/`mortality_slope`, `mortality_model.py`). Its mortality-rate surface is either supplied by the caller or, with `source: eurostat`, a European life table fetched through the Finance Toolkit. |
| `dependence/` | `Dependence` controller, builds and repairs the cross-factor correlation matrix. |
| `portfolio/` | `Portfolio` controller and the allocation math (`portfolio_model.py`), plus named presets (`portfolio_preset_*.py`, `portfolios/<id>.yaml`) and the relative-performance read (`benchmark_model.py`). A second, independent entry point next to `Scenarios`: it reads an already-simulated `ScenarioSet` (from `simulate()`, from `run_io_controller.read_run()`, or hand-built) and never calibrates or simulates anything. |
| `regimes/` | `Regime` schema and `RegimeLibrary`: named belief overrides and/or post-simulation narrative filters, applied through `Scenarios(regime=...)`. |
| `solvency/` | Solvency II and actuarial reads over a `ScenarioSet` (`solvency_model.py`: `martingale_test`, `zero_coupon_curve`, `best_estimate`, `solvency_capital_requirement`) and the actuarial scenario-file export plus the one-table `Solvency` report over a real-world and a risk-neutral run (`solvency_controller.py`: `write_scenario_files`, `Solvency`). Downstream and non-mutating, like `portfolio/`; see `financescenarios.solvency`. |
| `reporting/` | `Reporting` controller (opt-in read layer). Converts one already-simulated level-type factor's native-currency path into `config.reporting.reporting_currency`; a downstream, non-mutating view on a `ScenarioSet`, not part of the calibrate/simulate pipeline itself. |
| `engine/` | `ScenarioEngine` controller and the Monte Carlo core: time grid, correlated shocks, the stepping loop, and `ScenarioSet`. |
| `helpers.py` | `seed_random_generator`, `build_date_grid`, `setup_logger`, `get_logger`. |

## Data flow

A simulation run moves through four stages: calibration, dependence, regime pre-simulation, and the stepping loop.

{% raw %}
<div class="mermaid">
flowchart TD
    config["settings profile + factor-set profile"] --> toolkit["build_toolkit: embedded FinanceToolkit Toolkit instance"]
    toolkit --> calibration[Calibration dispatcher]
    calibration --> interestrates[InterestRates controller]
    calibration --> inflation[Inflation controller]
    calibration --> equities[Equities controller]
    calibration --> unemployment[Unemployment controller]
    calibration -.->|if yield_curve.enabled| termstructure[TermStructure controller]
    calibration -.->|if enabled| optional[RealEstate / Credit / LeadingIndicator / FX controllers]
    calibration -.->|if mortality.enabled, supplied or Eurostat data| mortality[Mortality controller]
    interestrates --> dependence[Dependence controller]
    inflation --> dependence
    equities --> dependence
    unemployment --> dependence
    termstructure -.-> dependence
    optional -.-> dependence
    mortality -.-> dependence
    dependence --> engine[ScenarioEngine]
    equities --> regimepath[Pre-simulated equity regime path]
    regimepath --> engine
    engine --> scenarioset[ScenarioSet]
</div>
{% endraw %}

`Scenarios.simulate()` in `scenarios_controller.py` runs this sequence:

1. `Calibration.calibrate_all(config)` calibrates every entry of the four always-on multi-instance MVP factors (`interest_rates`, `inflation`, `equities`, `unemployment`; each a list, one calibration per configured entry), plus every opt-in factor that's configured (`yield_curve.enabled`, `real_estate.enabled`, every `credit`/`fx`/`commodities`/`dividend_yield` list entry, `leading_indicator.enabled`, `mortality.enabled` with caller-supplied `mortality_rates`/`mortality_ages` or `source: eurostat`), and applies any belief overrides from `config`.
2. Each factor controller caches the historical series it fetched during calibration (its `.changes`/`.changes(name)` accessor), and `Dependence.calibrate()` reuses those series directly, instead of triggering a second FinanceToolkit fetch. Since the factors are calibrated at different sampling frequencies, the series are resampled to the coarsest configured period and inner-joined on calendar date (`align_factor_series_by_date`, not a positional "truncate to the shortest series" match) before the correlation matrix is built (then shrunk toward a constant-correlation target, Ledoit & Wolf 2004, before PSD repair; see `Dependence`).
3. Each equity entry's own regime path (which of the two, or more, regimes is active at each time step, for each simulation) is pre-simulated once per entry, each with its own RNG stream, independently of the correlated shocks used for the continuous part of the model.
4. `ScenarioEngine.simulate()` generates the correlated shocks, builds the time grid, and runs the stepping loop that advances every factor one time step at a time, in dependency order. Each factor's step function also receives the in-progress `paths` dict for that step, letting a factor simulated later in the order (e.g. an unemployment entry) read another factor's already-computed value for that same step (e.g. its paired inflation entry's move, the Phillips-curve input); see [simulation-engine](/projects/financescenarios/docs/simulation-engine). Most step functions ignore this and every trailing argument beyond `params`; `scenarios_controller.py`'s `_make_simple_step` helper wraps that common case once.

The always-on factors form a directed acyclic graph (a set of dependencies with no cycles), built fully dynamically in `Scenarios.calibrate()` (no fixed factor-name constant, since every entry's name is user-configured):

- Each inflation entry has no dependencies.
- Each interest-rate entry depends on every configured inflation entry, and each equity entry depends on every configured interest-rate and inflation entry. Both are cosmetic ordering edges only, since neither step function actually reads another factor's simulated value (the cascade is expressed through the correlation matrix, not sequential value-passing).
- Each unemployment entry has exactly one *real* dependency, on its own paired inflation entry (`UnemploymentConfig.inflation_name`), whose step-to-step change its Phillips-curve term actually reads.

This is resolved into a valid simulation order by a topological sort, described in [simulation-engine](/projects/financescenarios/docs/simulation-engine).

Every opt-in factor (the three yield curve factors, `real_estate`, each `credit`/`fx`/`commodities`/`dividend_yield` entry, `leading_indicator`, `mortality_level`/`mortality_slope`) has no cascade dependency of its own: only the correlation matrix links each to the rest, matching how Diebold-Li's three-factor yield curve system is specified (see `TermStructure`), how Ahlgrim/D'Arcy/Gorvett found real estate's inflation-dependence not significant (see `RealEstate`), and how Cairns-Blake-Dowd specify mortality improvement as a standalone bivariate random walk with no dependence on any financial-market factor (see `Mortality`).

## A library, driven directly

Finance Scenarios is a library: one entry point drives the `ScenariosConfig` in, `ScenarioSet` out contract: `financescenarios/` imported directly (`Scenarios.from_profiles(...)`, `Scenarios.from_config(...)`, `Portfolio`). Scripting and CI use go through the same imports. The one command line, `python -m financescenarios.release`, is a thin wrapper over `publish_calibration()` for the yearly release pipeline, not a second way to configure a run.

A full result can be written to disk via `financescenarios/run_io/run_io_controller.py` (`write_run()`, or `Scenarios.save()`, which supplies the config, regime and calibration itself and returns the run's folder) rather than held in memory, so a written run can be re-read later (`read_run()` + `Portfolio.from_preset()`) without resimulating.

`helpers.track_progress`/`count_calibration_stages` expose stage-by-stage calibration progress to any caller that wants to render it (`helpers.get_progress(token)`), which is what turns an indefinite wait into a countable one. Calibration is live network round-trips to FinanceToolkit per configured factor, so a worldwide default config takes low minutes, not milliseconds.
