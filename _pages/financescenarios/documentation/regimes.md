---
title: Regimes
seo_title: Stress Regimes Documentation – Finance Scenarios
excerpt: "A regime is a named story about the future, such as an oil crisis, saved once and reused. It changes an assumption before simulating, keeps only the scenarios that fit the story afterwards, or both."
description: "Named stress regimes in Finance Scenarios: belief overrides, post-simulation filters, official Federal Reserve and ESRB stress tests and climate pathways."
author_profile: false
permalink: /projects/financescenarios/docs/regimes
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

A regime is a named story about the future, such as an oil crisis or a financial crisis, saved once and reused. It can change an assumption before simulating (inflation jumps to 9%), keep only the scenarios that fit the story afterwards (high rates and falling stock markets), or both. `financescenarios.list_presets(kind=...)` lists the regimes that ship with the package.

`Regime` and `RegimeLibrary` (`financescenarios/regimes/`) let a caller name a stress scenario ("Oil Crisis", "Financial Crisis", "Climate Collapse") once, and re-apply it across runs, instead of re-typing raw `filter_narrative()` targets or config belief overrides every time. A regime is a specification, not a controller: no calibration or simulation logic lives here, `RegimeLibrary` only builds a `ScenariosConfig` and/or narrows a `ScenarioSet` using the mechanisms [simulation-engine](/projects/financescenarios/docs/simulation-engine) and [configuration](/projects/financescenarios/docs/configuration) already document. Translating a named regime's scenario subset into portfolio- or instrument-level impact is out of scope for this project: a regime only produces a `ScenarioSet` (or a `ScenariosConfig` ready to simulate) a caller feeds into their own valuation logic.

## One file per regime

Each regime lives in its own YAML file under a `regimes/` directory (see `financescenarios/presets/regimes/` for the shipped set): `regimes/oil_crisis.yaml`, `regimes/financial_crisis.yaml`, and so on. This is deliberate: a caller that wants to run one specific regime loads exactly that one file, never the whole directory; see `load_one()` below. Listing every available regime (`RegimeLibrary.load(<dir>)`) is the only operation that touches every file, since listing inherently requires knowing about all of them.

A regime file's shape:

```yaml
name: Oil Crisis                    # required
description: >                      # optional, free text
  Cost-push inflation spike...
extends: some_other_regime.yaml      # optional, see below
targets: {...}                      # optional, see "Two mechanisms" below
beliefs: {...}                      # optional, see "Two mechanisms" below
step_range: [0, 10]                 # optional
target_mode: sequential             # optional: sequential (default) | joint
```

**`extends`** names another regime file in the same directory to inherit from. Fields are deep-merged: for any key present in both the parent and this file, if both values are dicts they're merged recursively (so a nested override only needs to state what's different, not repeat the rest); anything else (scalars, lists) is replaced by this file's value. `regimes/rate_cut_cycle.yaml` extends `regimes/soft_landing.yaml` this way: it inherits Soft Landing's year-5 inflation anchor and adds only the year-10 anchor and `converge_over_years`, rather than restating both anchors:

```yaml
# soft_landing.yaml
beliefs:
  inflation.united_states_inflation:
    long_run_mean:
      anchors: {5.0: 0.02}

# rate_cut_cycle.yaml
extends: soft_landing.yaml
beliefs:
  inflation.united_states_inflation:
    long_run_mean:
      anchors: {10.0: 0.025}        # merges with the inherited 5.0 anchor
      converge_over_years: 5.0       # added fresh
```

An `extends` chain must be acyclic (`load_one()` raises `ValueError` on a cycle) and every file in it must eventually set `name`.

## Two mechanisms, either or both

A `Regime` can carry:

- **`targets`**: a post-simulation selection spec, the same shape as `ScenarioSet.filter_narrative()`'s `targets` argument (factor name -> `(lower, upper)` quantile range). Narrows an already-simulated baseline run down to the paths consistent with the story. Applied via `RegimeLibrary.apply(scenario_set, name)`.
- **`beliefs`**: a pre-simulation calibration override spec, the same shape as a `ScenariosConfig` factor's own `beliefs` section (see [configuration](/projects/financescenarios/docs/configuration)'s "Belief overrides"/"Belief paths" sections), including a `BeliefPath` term structure for `long_run_mean`. Reshapes what gets simulated in the first place. Applied via `RegimeLibrary.build_config(base_config, name)`.

At least one of the two is required: a regime with neither would do nothing. Use `targets` alone for a pure selection filter on top of a baseline run everyone shares; use `beliefs` alone to make one factor's calibration itself tell the crisis story; use both together (see `regimes/oil_crisis.yaml`) when the belief-shaped run should *also* be narrowed further. This mirrors the distinction Solvency II draws between a "stress test" (a single, prescribed shock; closer to `targets` alone) and "scenario analysis" (a combination of correlated, internally consistent shocks; closer to `beliefs`, or both together): a `Regime` can express either.

**Multi-instance factors** (`equities`/`fx`/`credit` are lists in `ScenariosConfig`, see [configuration](/projects/financescenarios/docs/configuration)'s Multi-instance factors section): `targets` addresses one entry with its plain `name` (e.g. `"tech"`, the factor's actual name in the simulated `ScenarioSet`), while `beliefs` needs a dotted `"<container>.<name>"` key instead (e.g. `"equities.tech"`) to say which list entry's beliefs to shape; `regime.beliefs["equities"]` would otherwise be ambiguous between "the whole `equities` list" and "one entry in it". See `regimes/tech_selloff.yaml` for a worked example.

**Units are one convention: an annualized decimal rate for every rate-type factor (`0.06` means 6% a year), a price level for equities/fx/commodities.** Sources that don't arrive that way are converted at the fetch. See [units](/projects/financescenarios/docs/units) for the full statement, including which conversion each source needs and how belief anchors follow from it. Check a factor's own calibrated level with `scenarios.calibrate().describe()` before choosing anchors.

```python
from financescenarios import Scenarios

scenarios = Scenarios.from_profiles(settings="default", factor_set="default", regime="oil_crisis")
result = scenarios.simulate()   # beliefs already applied to scenarios.config; targets narrow the result

scenarios.regime.description    # what this regime represents
scenarios.config                # the belief-shaped config that actually ran
```

Naming the regime on the `Scenarios` instance is the normal path: its belief overrides shape the config once, at construction, and every `simulate()` call on that instance narrows its result by the regime's `targets` (if it has any). `Scenarios.from_config(config, regime=regime)` does the same for an already-loaded `Regime`/`ScenariosConfig`. Reach for `RegimeLibrary.build_config()`/`.apply()` directly when you want to inspect or reuse the intermediate config, or apply targets to a `ScenarioSet` you already have.

## `RegimeLibrary` and `load_one()`

| Function | Does |
|---|---|
| `load_one(directory, filename)` | Load exactly one regime, resolving its `extends` chain; never touches any other file in `directory`. This is what `Scenarios.from_profiles(..., regime=...)` uses. |
| `RegimeLibrary.load(directory)` | Load every `*.yaml` file in `directory` into a library, keyed by each regime's `name`, for listing. |
| `RegimeLibrary.save(directory)` | Write every regime in the library to `directory`, one file per regime (named after a slugified `name`); round-trips with `load()`. Does not preserve any `extends` relationship; every regime is written fully resolved. |

`RegimeLibrary`'s in-memory API is otherwise the same as before file-per-regime storage:

| Method | Does |
|---|---|
| `add(regime)` | Add or replace a regime, keyed by its own `name`. |
| `get(name)` | Look up a regime by name; raises `KeyError` if unregistered. |
| `names` | The names of every registered regime. |
| `apply(scenario_set, name)` | `scenario_set.filter_narrative(regime.targets, step_range=regime.step_range, mode=regime.target_mode)`. Raises `ValueError` if the regime has no targets (it's beliefs-only). |
| `build_config(base_config, name)` | `base_config` with each factor named in `regime.beliefs` having those belief fields overridden; unchanged fields (and the whole config, if the regime has no beliefs) pass through untouched. |
| `simulate(scenarios, base_config, name)` | `build_config()` -> `scenarios.simulate(config)` -> `apply()`'s `filter_narrative()` step if the regime has targets. Equivalent to `Scenarios.from_config(base_config, regime=regime).simulate()`, kept for callers holding a library rather than building the instance themselves. |

`RegimeLibrary` has no dependency on which factors are enabled in `base_config`: `build_config()` only touches the factor sections a given regime's `beliefs` actually names, so the same library works across configs with different opt-in factors turned on.

A target's quantile range ranks each simulation by one statistic over `step_range` (the whole path by default): a rate by its average level across the window, and a price-level factor (equities, FX, commodities) by its annualized return from the window's first date to its last. `us_broad: [0.0, 0.3]` therefore keeps the 30% of scenarios with the weakest equity *return* over the window. It is deliberately start-to-end rather than an average of the since-start returns at every date, since a return annualized over a single month swings so widely that such an average would really rank the first few months.

## Driving a regime from the library

Every regime under `regimes/` is driven the same way underneath: `load_one()` to load exactly the requested regime, then `Scenarios.from_config(config, regime=regime)`: belief shaping at construction, then the `filter_narrative()` narrowing inside `simulate()` only when the regime has targets. A regime is addressed by its `id` (its filename, without directory or extension), not its display `name`, so exactly one file gets loaded rather than the directory being scanned for a name match; `RegimeLibrary.load("regimes").names` is the listing for a picker.

A regime with targets keeps only part of the run, about 9% for Oil Crisis. `simulate(keep=2000)` draws as many scenarios as that takes, about 22,700 here, and returns exactly 2,000 that fit the story, so a stress result rests on as many scenarios as the baseline. `plot_runs({"baseline": result, "oil_crisis": shocked}, "united_states_inflation")` then draws them side by side on one scale.

## Official stress tests as regimes

`stress_test_regime(toolkit, config, authority, scenario)` builds a regime from a regulator's published stress-test scenario instead of a hand-written one, through the Finance Toolkit (no key):

- `authority="federal_reserve"`: the Federal Reserve's supervisory scenario for the United States, 13 quarters of the 3-month Treasury rate, 10-year Treasury yield, CPI inflation and unemployment.
- `authority="esrb"`: the European Systemic Risk Board's scenario for the EBA's EU-wide bank stress test, three years of the long-term rate, inflation and unemployment for every EU member and the main other economies.

Each interest rate, inflation and unemployment entry follows the scenario for its own `country`. With `follow="path"` (the default) every factor is set to the published value at each period end and its long-run level follows the scenario in between, so even a slow-moving short rate really falls to the Federal Reserve's 0.1%; with `follow="target"` only the long-run level is steered, a gentler stress. Either way the target returns to the factor's own calibrated level over `converge_over_years` (five by default) after the scenario ends. The Federal Reserve's inflation is an annualized quarter-on-quarter rate while this project's is year over year: the same scale, but it reacts sooner.

Real-world equities follow the scenario's stock market too, as one-off price jumps (`shocks`): the Federal Reserve's path is the Dow Jones Total Stock Market Index, used as the adverse level against its own baseline, so the shock is the stress and not the baseline's growth; the ESRB's is the stock-price fall from the starting point, per country. Every equity uses one region, `United States` for the Federal Reserve and `European Union` for the ESRB by default, which `equity_regions={"<equity name>": "<region>"}` changes per equity. The stock path keeps the scenario's own spacing but starts at the run's start, so the fall always lands inside the run even though the ESRB's 2025 scenario was published for 2025 to 2027. Risk-neutral equities are left alone, since their drift is the simulated rate. On the `default` set, the median US broad-market price after a year is 0.50 times the start under the Federal Reserve's 2026 adverse scenario and 0.57 times under the ESRB's, against 1.14 unstressed.

```python
from financescenarios import Scenarios, stress_test_regime

regime = stress_test_regime(toolkit, config, authority="federal_reserve", scenario="adverse")
stressed = Scenarios.from_config(config, toolkit=toolkit, regime=regime).simulate()
```

On the US factors of the `us_only` set, the 2026 severely adverse scenario puts the short rate at 0.1% within a year and unemployment at about 9.8% after two, against 3.7% and 5.5% in the unstressed run.

## Climate scenarios

A climate pathway is not a regime but an overlay on any run: `climate.enabled: true` in a factor set adds an NGFS scenario's deviation from its baseline (Net Zero 2050, Delayed transition, Current Policies and others) to each interest rate, inflation, unemployment and equity factor after simulating, measured from the run's start, and `climate.carbon_price: true` adds the scenario's carbon price as a factor. It combines with a regime: the regime shapes the scenarios, the climate pathway shifts them. See `climate_controller.apply_climate_scenario`.
