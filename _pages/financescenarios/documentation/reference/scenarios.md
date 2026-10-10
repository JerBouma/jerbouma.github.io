---
title: "Scenarios"
seo_title: "Scenarios Reference – Finance Scenarios"
excerpt: "Calibrate every configured factor and simulate correlated scenarios; also the saved calibration and the Toolkit builder."
description: "Calibrate every configured factor and simulate correlated scenarios; also the saved calibration and the Toolkit builder."
author_profile: false
permalink: /projects/financescenarios/docs/reference/scenarios
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

Calibrate every configured factor and simulate correlated scenarios; also the saved calibration and the Toolkit builder. Generated from the docstrings of Finance Scenarios 0.1.0; `help(...)` in Python shows the same text.

```python
from financescenarios import Scenarios, CalibrationResult, build_toolkit
```

## Scenarios

```python
Scenarios(
    toolkit: Toolkit | None,
    n_simulations: int = 1000,
    n_steps: int = 52,
    time_step: float = 1 / 52,
    seed: int | None = None,
    antithetic: bool = False,
    shock_distribution: Literal['gaussian', 'student_t'] = 'gaussian',
    degrees_of_freedom: float = 5.0,
    bond_panel: BondPanel | None = None,
    config: ScenariosConfig | None = None,
    regime: Regime | None = None,
)
```

Calibrates every configured factor (rates, inflation, equities, currencies, commodities, credit and more)
to live data and simulates correlated scenarios of them. Start with `from_profiles`:

```python
from financescenarios import Scenarios, list_presets

list_presets()  # every name you can pass, and the argument it goes in
scenarios = Scenarios.from_profiles(settings="default", factor_set="us_only")
result = scenarios.simulate(n_simulations=100)  # calibrates first, then simulates
result.describe()
```

Then `scenarios.validate(result)` checks the run, `scenarios.history(...)` gives what actually happened,
`scenarios.simulate(measure="risk_neutral")` the market-consistent run, and `scenarios.save(result)` stores it.
Building one directly (`Scenarios(toolkit, ...)`) is for code that assembles its own Toolkit and config.

The overall design (a cascade of dependent, correlated stochastic factors run
over a full multi-decade simulated horizon) descends from the actuarial
multi-asset ESG literature: Wilkie's original cascade structure (Wilkie, 1986),
the CAS's broader multi-factor framework spanning equity, rates, inflation, real
estate and unemployment in one model (Ahlgrim, D'Arcy & Gorvett, 2005), and
Barrie & Hibbert's multi-factor calibration approach for long-term financial
planning (Hibbert, Mowbray & Turnbull, 2001). Simulating the full horizon
directly, rather than only a one-year-ahead risk-factor set, follows Curry's
(2021) argument that a one-year VaR/copula view (the Solvency II standard)
understates risk over the multi-decade horizons a pension-focused ESG like this
one actually needs to project.

**References:**

- Wilkie, A.D. (1986). "A stochastic investment model for actuarial use." Transactions of the Faculty of Actuaries, 39, 341-403.
- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2005). "Modeling Financial Scenarios: A Framework for the Actuarial Profession." Proceedings of the CAS, 92.
- Hibbert, J., Mowbray, P., Turnbull, C. (2001). "A Stochastic Asset Model & Calibration for Long-Term Financial Planning Purposes." Barrie & Hibbert.
- Curry, B. (2021). "Long-term stochastic risk models: the 6th generation of modern actuarial models?" Institute and Faculty of Actuaries sessional paper.

## Scenarios.from_config

```python
Scenarios.from_config(
    config: ScenariosConfig,
    toolkit: Toolkit | None = None,
    bond_panel: BondPanel | None = None,
    regime: Regime | None = None,
    api_key: str | None = None,
    fred_api_key: str | None = None,
) -> Scenarios
```

Build a Scenarios instance from a validated configuration. The config is
kept on the instance, so `simulate()` takes no arguments:

```python
scenarios = Scenarios.from_config(load_config("settings/default.yaml"))
result = scenarios.simulate()
```

**Args:**

- <u>config (ScenariosConfig):</u> a validated configuration, e.g. from load_config().
- <u>toolkit (Toolkit &#124; None):</u> a pre-built Finance Toolkit instance, e.g. to inject a fake/cached Toolkit in tests. If omitted (the normal case), one is built automatically per config.toolkit; see build_toolkit().
- <u>bond_panel (BondPanel &#124; None):</u> a pre-built BondPanel, e.g. a fake/pre- cached instance in tests, for the credit_term_structure factor. If omitted, a default BondPanel() is built on first use.
- <u>regime (Regime &#124; None):</u> a regime whose belief overrides shape `config` before it's stored, and whose targets (if any) narrow every `simulate()` result; see `regimes_controller.RegimeLibrary`. `from_profiles(regime=...)` is the usual way in.
- <u>api_key (str &#124; None):</u> an API key from FinancialModelingPrep, obtain one at https://www.jeroenbouma.com/fmp. Defaults to None, which reads the FINANCIAL_MODELING_PREP_API_KEY environment variable (or a `.env` file). Unused with `toolkit`.
- <u>fred_api_key (str &#124; None):</u> a free FRED API key, https://fred.stlouisfed.org/docs/api/api_key.html, for credit, commercial real estate and breakeven inflation. Defaults to None, which reads FRED_API_KEY.

**Returns:**

<u>Scenarios:</u> an instance configured per config.engine, holding `config`.

## Scenarios.from_profiles

```python
Scenarios.from_profiles(
    settings: str = 'default',
    factor_set: str = 'default',
    regime: str | Regime | None = None,
    settings_dir: str | Path = 'settings',
    factor_sets_dir: str | Path = 'factor-sets',
    regimes_dir: str | Path = 'regimes',
    toolkit: Toolkit | None = None,
    bond_panel: BondPanel | None = None,
    api_key: str | None = None,
    fred_api_key: str | None = None,
) -> Scenarios
```

The one-call entry point: pick a named settings profile, a named factor-set
profile, and optionally a named regime (the three directories of YAML this
project is driven by) and get back a ready-to-run instance.

```python
scenarios = Scenarios.from_profiles(
    settings="default", factor_set="us_only", regime="oil_crisis", api_key="FINANCIAL_MODELING_PREP_KEY"
)
result = scenarios.simulate()
```

**Args:**

- <u>settings (str):</u> settings profile id, e.g. "default" or "long_horizon" (the ".yaml" suffix is optional); run settings only.
- <u>factor_set (str):</u> factor-set profile id, e.g. "default" or "us_only"; every factor/ticker/belief definition.
- <u>regime (str &#124; Regime &#124; None):</u> a regime id to load from `regimes_dir`, an already-loaded `Regime`, or None for an unshaped run. Its belief overrides are applied to the config now; its narrative targets (if any) narrow every `simulate()` result.
- <u>settings_dir (str &#124; Path):</u> the settings profiles directory.
- <u>factor_sets_dir (str &#124; Path):</u> the factor-set profiles directory.
- <u>regimes_dir (str &#124; Path):</u> the regimes directory, only read when `regime` is a string.
- <u>toolkit (Toolkit &#124; None):</u> see `from_config()`.
- <u>bond_panel (BondPanel &#124; None):</u> see `from_config()`.
- <u>api_key (str &#124; None):</u> an API key from FinancialModelingPrep, obtain one at https://www.jeroenbouma.com/fmp. Defaults to None, which reads the FINANCIAL_MODELING_PREP_API_KEY environment variable (or a `.env` file).
- <u>fred_api_key (str &#124; None):</u> an optional, free FRED API key; see `from_config()`.

**Returns:**

<u>Scenarios:</u> an instance holding the resolved config (and regime).

**Raises:**

- <u>FileNotFoundError:</u> if a profile (or a file in its `extends` chain) doesn't exist. `scaffold_project()` scaffolds these three directories if you don't have them yet.
- <u>pydantic.ValidationError:</u> if the merged profiles don't form a valid ScenariosConfig.

## Scenarios.from_config_file

```python
Scenarios.from_config_file(
    config_path: str,
    factors_path: str | None = None,
) -> tuple[Scenarios, ScenariosConfig]
```

Build a Scenarios instance directly from config YAML file paths, including
the Finance Toolkit instance it calibrates against; no separate Toolkit
construction needed. Prefer `from_profiles()` for the named-profile
directories this project actually ships; this is the two-explicit-paths
counterpart, matching `load_config()`.

**Args:**

- <u>config_path (str):</u> path to the run-settings YAML file (see load_config()).
- <u>factors_path (str &#124; None):</u> path to the factor-definitions YAML file. If omitted, defaults to a `factors.yaml` sibling of `config_path` (see load_config()).

**Returns:**

<u>tuple[Scenarios, ScenariosConfig]:</u> the constructed instance, and the loaded config (also kept on the instance, so `.simulate()` needs no argument).

## Scenarios.config

```python
scenarios.config  # property -> ScenariosConfig | None
```

The config this instance runs: what `calibrate()`/`simulate()` use when
called without one, already shaped by `regime`'s belief overrides if it has
one. None when the instance was constructed directly rather than via
`from_config()`/`from_profiles()`.

## Scenarios.regime

```python
scenarios.regime  # property -> Regime | None
```

The regime applied to this instance, if any; see `from_profiles()`.

## Scenarios.calibration

```python
scenarios.calibration  # property -> Calibration
```

The calibration dispatcher (also reachable via .interest_rates/.inflation/.equities/.unemployment).

## Scenarios.correlation_fallback_pairs

```python
scenarios.correlation_fallback_pairs  # property -> list[str]
```

The last calibrate()/simulate() call's correlation_fallback_pairs;
see CalibrationResult's own field docstring. A convenience mirror of
self._dependence.fallback_pairs, reachable without holding onto the
CalibrationResult calibrate()/simulate() may have built internally
(e.g. a caller that only calls simulate(config), never calibrate(config)
directly, still needs a way to read this afterward).

## Scenarios.last_calibration

```python
scenarios.last_calibration  # property -> CalibrationResult | None
```

The calibration the most recent `simulate()` call ran on, whether it
built one itself or was handed one. None before the first call. Save it
(`CalibrationResult.save()`) to replay this exact fit later with no network
access, or pass it straight back to `simulate(calibration=...)` to re-run at
a different seed or path count.

## Scenarios.calibration_failures

```python
scenarios.calibration_failures  # property -> dict[str, str]
```

The last calibrate()/simulate() call's calibration_failures; see
CalibrationResult's own field docstring. A convenience mirror of
self._calibration_failures, the same "live state, readable without
holding onto the CalibrationResult" shape correlation_fallback_pairs'
own property already documents.

## Scenarios.interest_rates

```python
scenarios.interest_rates  # property
```

The interest-rate factor controller.

## Scenarios.inflation

```python
scenarios.inflation  # property
```

The inflation factor controller.

## Scenarios.knw

```python
scenarios.knw  # property
```

The opt-in method='knw' (interest_rate, inflation) VAR(1)-pair controller.

## Scenarios.knw_sv

```python
scenarios.knw_sv  # property
```

The opt-in method='knw_sv' (v, interest_rate, inflation) stochastic-volatility triple controller.

## Scenarios.equities

```python
scenarios.equities  # property
```

The equities factor controller.

## Scenarios.unemployment

```python
scenarios.unemployment  # property
```

The unemployment factor controller.

## Scenarios.term_structure

```python
scenarios.term_structure  # property
```

The opt-in Nelson-Siegel yield curve factor controller (rate_level/rate_slope/rate_curvature).

## Scenarios.credit_term_structure

```python
scenarios.credit_term_structure  # property
```

The opt-in Nelson-Siegel credit-spread curve factor controller
(credit_level/credit_slope/credit_curvature), fit against a real bond
panel; see credit_term_structure_controller.CreditTermStructure.

## Scenarios.hjm

```python
scenarios.hjm  # property
```

The opt-in 2-factor Gaussian HJM forward curve factor controller
(hjm_factor_1/hjm_factor_2); see hjm_controller.Hjm.

## Scenarios.real_estate

```python
scenarios.real_estate  # property
```

The opt-in real estate factor controller.

## Scenarios.credit

```python
scenarios.credit  # property
```

The opt-in credit spread factor controller.

## Scenarios.leading_indicator

```python
scenarios.leading_indicator  # property
```

The opt-in leading indicator factor controller.

## Scenarios.credit_migration

```python
scenarios.credit_migration  # property
```

The opt-in credit cycle (rating migration) controller.

## Scenarios.fx

```python
scenarios.fx  # property
```

The opt-in FX factor controller.

## Scenarios.commodities

```python
scenarios.commodities  # property
```

The opt-in commodity factor controller.

## Scenarios.dividend_yield

```python
scenarios.dividend_yield  # property
```

The opt-in dividend yield factor controller.

## Scenarios.dividend_growth

```python
scenarios.dividend_growth  # property
```

The opt-in dividend growth factor controller.

## Scenarios.mortality

```python
scenarios.mortality  # property
```

The opt-in mortality/longevity factor controller.

## Scenarios.dependence

```python
scenarios.dependence  # property -> Dependence
```

The cross-factor correlation controller.

## Scenarios.calibrate

```python
calibrate(
    config: ScenariosConfig | None = None,
    mortality_rates: pl.DataFrame | None = None,
    mortality_ages: list[float] | None = None,
    mortality_years: list[int] | None = None,
) -> CalibrationResult
```

Calibrate every MVP factor (interest rate, inflation, equity, unemployment),
plus every enabled opt-in factor, and build the cross-factor correlation
matrix, without running the Monte Carlo engine. simulate() calls this
automatically when no `calibration` is supplied; call it directly to save the
result (CalibrationResult.save()) for reproducible or offline re-simulation
later via simulate(calibration=...), or to re-run with a different
seed/n_simulations/belief override on a frozen calibration without
re-fetching data from Finance Toolkit.

**Args:**

- <u>config (ScenariosConfig &#124; None):</u> per-factor calibration settings, belief overrides, and the simulation start date. Defaults to the config this instance was built with (see `from_profiles()`/`from_config()`).
- <u>mortality_rates (pl.DataFrame &#124; None):</u> historical mortality-rate surface (age x calendar year), required only if config.mortality.enabled with `mortality.source: supplied` (the default); `source: eurostat` fetches a European country's life table through the Toolkit instead. See Mortality.calibrate().
- <u>mortality_ages (list[float] &#124; None):</u> ages corresponding to mortality_rates' columns, required alongside mortality_rates.
- <u>mortality_years (list[int] &#124; None):</u> calendar years corresponding to mortality_rates' rows, forwarded to Mortality.calibrate(); see its own docstring for the fallback behavior when omitted.

**Returns:**

<u>CalibrationResult:</u> calibrated parameters, the correlation matrix, and the factor/dependency structure this run's simulate() needs.

**Raises:**

- <u>RuntimeError:</u> if this Scenarios instance was constructed with toolkit=None (only valid for replaying a saved CalibrationResult).
- <u>ValueError:</u> if no config is available at all, or config.mortality.enabled with a supplied source but mortality_rates/mortality_ages are not supplied.

## Scenarios.simulate

```python
simulate(
    config: ScenariosConfig | None = None,
    calibration: CalibrationResult | None = None,
    mortality_rates: pl.DataFrame | None = None,
    mortality_ages: list[float] | None = None,
    mortality_years: list[int] | None = None,
    seed: int | None = None,
    n_simulations: int | None = None,
    measure: Literal['real_world', 'risk_neutral'] = 'real_world',
    years: float | None = None,
    keep: int | None = None,
) -> ScenarioSet
```

Run one Monte Carlo simulation. Calibrates first (see calibrate()) unless a
pre-built CalibrationResult is supplied, in which case Finance Toolkit is
never touched; useful for reproducing a past run byte-for-byte, replaying a
saved calibration without network/API access, or cheaply re-simulating
(different seed, n_simulations, or belief override applied before calling
calibrate()) without recalibrating from live data each time.

If this instance carries a regime with narrative targets (see
`from_profiles(regime=...)`), the result is narrowed to the simulations
satisfying them before it's returned.

**Args:**

- <u>config (ScenariosConfig &#124; None):</u> engine settings and the simulation start date. Defaults to the config this instance was built with; a config whose `engine` differs from that one runs on its own engine settings (steps, frequency, simulations, seed) for this call. If `calibration` is omitted, also drives calibration (per-factor settings, belief overrides) the same way calibrate() does.
- <u>calibration (CalibrationResult &#124; None):</u> a pre-built calibration, e.g. from self.calibrate() or CalibrationResult.load(). If omitted, calibrate() is called automatically.
- <u>mortality_rates (pl.DataFrame &#124; None):</u> forwarded to calibrate() if `calibration` is omitted and config.mortality.enabled; see calibrate().
- <u>mortality_ages (list[float] &#124; None):</u> forwarded to calibrate() if `calibration` is omitted and config.mortality.enabled; see calibrate().
- <u>mortality_years (list[int] &#124; None):</u> forwarded to calibrate() if `calibration` is omitted and config.mortality.enabled; see calibrate().
- <u>seed (int &#124; None):</u> draw this run's shocks from a different seed than the instance was built with, for this call only. Neither the calibration nor the instance is touched, so `simulate(calibration=cal, seed=...)` across a few seeds is the cheap way to see how much of a result is Monte Carlo noise.
- <u>n_simulations (int &#124; None):</u> run a different number of paths, for this call only; the other half of that check (does the answer move when the sample grows?). Must be even when this instance uses antithetic variates.
- <u>measure (str):</u> "real_world" (the default) simulates the config as it is. "risk_neutral" simulates its market-consistent counterpart instead (`config_model.risk_neutral_config`: the risk-free rate on today's forward curve, equities growing at that rate), calibrated afresh, for valuing liabilities and the martingale test. This instance, its calibration and its regime are left untouched.
- <u>years (float &#124; None):</u> how far ahead to simulate, in years, at the profile's own step size, e.g. `years=30` for 360 monthly steps. None (the default) keeps the profile's horizon (`engine.n_steps`).
- <u>keep (int &#124; None):</u> the number of scenarios to return when this instance's regime narrows the run (keeps only the scenarios that fit its story): enough are drawn that exactly this many are kept, e.g. about 22,700 for Oil Crisis to keep 2,000. Without a narrowing regime it is simply the number of scenarios. None (the default) returns whatever the narrowing leaves of `n_simulations`.

**Returns:**

<u>ScenarioSet:</u> the simulated paths, time grid, dates, and calibration metadata.

**Raises:**

- <u>ValueError:</u> if no config is available at all (see `from_profiles()`), `n_simulations` is not a positive whole number or is odd under antithetic variates, this instance's regime targets match no simulation, or `measure="risk_neutral"` is combined with a `calibration`.
- <u>TypeError:</u> if `calibration` is not a `CalibrationResult`.

## Scenarios.history

```python
history(
    portfolio: str | None = None,
    factors: list[str] | None = None,
    period: str = 'monthly',
    portfolios_dir: str | Path = 'portfolios',
) -> ScenarioSet
```

What actually happened, as a one-path ScenarioSet, so `Portfolio` and every ScenarioSet method run on history
the same way they run on simulated scenarios (a backtest). Fetches each factor's historical series and lines
them up on the dates they all share.

**Args:**

- <u>portfolio (str &#124; None):</u> a portfolio preset's name, e.g. "balanced_60_40"; its holdings are fetched (`list_presets(kind="portfolios")` lists them).
- <u>factors (list[str] &#124; None):</u> factor names to fetch instead. With neither, every factor with history is fetched; each one narrows the shared dates to its own window, so name only the ones you need.
- <u>period (str):</u> the calendar to line the series up on: "daily", "weekly", "monthly" (default), "quarterly" or "yearly".
- <u>portfolios_dir (str &#124; Path):</u> where a named portfolio preset is looked up; the bundled presets otherwise.

**Returns:**

<u>ScenarioSet:</u> one path per factor, `n_simulations=1`, on the shared dates.

**Raises:**

- <u>ValueError:</u> if this instance has no Finance Toolkit, or the series share too few dates.
- <u>KeyError:</u> if a named factor has no history.

**As an example:**

```python
history = scenarios.history(portfolio="balanced_60_40")
Portfolio.from_preset(history, preset="balanced_60_40").factor_exposure()
```

## Scenarios.validate

```python
validate(result: ScenarioSet) -> pl.DataFrame
```

Check a run in one table, with the same checks the yearly published calibration passes: every factor
calibrated, the fitted parameters are plausible, the correlation matrix is valid, the scenarios move together
as calibrated, each factor swings about as much as it did historically, and every path is finite.

In plain terms: is this run fit to use? A "warn" is worth a look but not a reason to discard the run.

**Args:**

- <u>result (ScenarioSet):</u> a run simulated from this instance's latest calibration.

**Returns:**

<u>pl.DataFrame:</u> one row per check: 'check', 'status' ("pass", "warn" or "fail"), 'detail' (what was found, with the numbers) and 'meaning' (what the check means).

**Raises:**

- <u>ValueError:</u> if nothing was calibrated yet, or this instance has no Finance Toolkit to fetch history with.

## Scenarios.save

```python
save(
    result: ScenarioSet,
    output_dir: str | Path = 'results',
    output_format: str = 'parquet',
) -> Path
```

Store a run with everything needed to read it back or replay it: the config, the regime, the calibration
and one file per factor (see `run_io_controller.write_run`). `read_run(path)` reads it back.

**Args:**

- <u>result (ScenarioSet):</u> the run to store.
- <u>output_dir (str &#124; Path):</u> the folder runs are kept in; each run gets its own subfolder.
- <u>output_format (str):</u> "parquet" (the default, smaller and faster) or "csv".

**Returns:**

<u>Path:</u> the run's own folder.

## CalibrationResult

```python
class CalibrationResult(BaseModel):
    calibrated_params: dict[str, CreditCycleParams | OUParams | RegimeParams | UnemploymentParams | YieldCurveParams | FXParams | CommodityParams | DividendYieldParams | DividendGrowthParams | WilkieConsolsParams | EquityDerivedParams | RandomWalkParams | GARCHParams | OUCovariateParams | DeterministicParams | DeterministicPathParams | HullWhiteForwardParams | AR1Params | MovingTargetOUParams | KnwParams | KnwSvLegParams | KnwSvEquityParams | HjmFactorParams | HestonParams]
    correlation_matrix: np.ndarray
    factor_names: list[str]
    dependencies: dict[str, list[str]]
    raw_long_run_means: dict[str, float] = Field(default_factory=dict, description="factor name -> that factor's statistically calibrated long_run_mean, captured before any belief override; see Calibration.calibrate_all()'s own docstring. Only populated for OU-family/unemployment factors.")
    correlation_fallback_pairs: list[str] = Field(default_factory=list, description="'factor_a/factor_b' pairs the correlation matrix defaulted to 0.0 (assumed uncorrelated) for lack of a reliable overlap; see dependence_model.build_pairwise_correlation_matrix()'s own docstring. Only ever populated when config.engine.correlation_method='pairwise' (the default); always empty for 'complete_case', which has no such fallback (every pair either has a real estimate from the one shared window, or calibration fails outright).")
    beliefs: dict[str, Any] | None = Field(default=None, description="the fixed belief overrides this calibration applied, keyed '<category>.<name>' (see belief_snapshot()); simulate() refuses to replay it under a config whose overrides differ, since those are baked into calibrated_params. None for a calibration saved before this was recorded.")
    correlation_shrinkage: float | None = Field(default=None, description="the shrinkage intensity applied to the sample correlation matrix (the computed one with engine.correlation_shrinkage='auto'); None for a calibration saved before this was recorded.")
    correlation_repair: float | None = Field(default=None, description='how far the shrunk correlation matrix moved to become a valid one (Frobenius norm; 0 if it already was); large values mean the pairwise estimates disagreed. None for an older calibration.')
    long_run_anchors: dict[str, dict[str, float]] = Field(default_factory=dict, description="interest-rate factor name -> {year: long-run level} from that entry's long_run_anchor (EIOPA's forward rates), applied as its long-run belief path when simulating unless the config sets one itself. Empty for a calibration without anchors or saved before they existed.")
    calibration_failures: dict[str, str] = Field(default_factory=dict, description="factor name -> failure reason, for a configured factor whose own historical fit raised (e.g. no mean reversion over a short calibration window) or which depends on one that did; see calibration_controller.Calibration.calibrate_all()'s own docstring for exactly which factors this covers. That factor is absent from calibrated_params/factor_names rather than aborting every other factor's calibration too. Empty when everything calibrated cleanly (the common case with a full toolkit.start_date history).")
```

Everything Scenarios.simulate() needs to run the Monte Carlo engine, without
touching Finance Toolkit again: the return value of Scenarios.calibrate(config).
Save it to reproduce a run later, or to re-simulate (different seed, n_simulations,
or belief overrides) without recalibrating from live data every time.

## CalibrationResult.describe

```python
describe() -> pl.DataFrame
```

One row per calibrated factor: which process was fitted and the parameters
most worth eyeballing; the "what did the historical fit actually say"
read, without picking a factor out of `calibrated_params` first and knowing
which parameter class it holds.

Every rate-type factor's `long_run_mean`/`volatility` is an annualized
decimal (0.024 meaning 2.4% a year; see the units documentation),
so the numbers are comparable down the column even across factors fitted at
different data frequencies.

**Returns:**

<u>pl.DataFrame:</u> "factor", "process" (the parameter class, e.g. "OUParams"), "initial_value", "long_run_mean", "volatility", "mean_reversion_speed", "half_life_years" (ln 2 / mean_reversion_speed: how many years a shock takes to decay halfway back to the long-run mean); the last four null for a process that has no such parameter (an equity regime fit, an FX GBM, ...).

## CalibrationResult.correlation_frame

```python
correlation_frame() -> pl.DataFrame
```

The calibrated cross-factor correlation matrix as a labelled table: a "factor"
column plus one column per factor, in `factor_names` order. Set it next to
`ScenarioSet.simulated_correlation()` to check a run reproduces the
dependence it was calibrated with.

## CalibrationResult.plot

```python
plot(annotate: bool | None = None)
```

The quick chart of a calibration: its cross-factor correlation matrix as a
heatmap, the same as `plot_correlation_matrix()`.

## CalibrationResult.plot_correlation_matrix

```python
plot_correlation_matrix(annotate: bool | None = None)
```

This calibration's cross-factor correlation matrix as a diverging
heatmap; delegates to `dependence_view.plot_correlation_matrix`
(imported at call time, so matplotlib loads only when a chart is drawn),
see that function's docstring for the full detail.

## CalibrationResult.save

```python
save(path: str | Path) -> None
```

Persist this calibration to a JSON file.

**Args:**

- <u>path (str &#124; Path):</u> where to write the file.

## CalibrationResult.load

```python
CalibrationResult.load(path: str | Path) -> CalibrationResult
```

Load a calibration previously written by save().

**Args:**

- <u>path (str &#124; Path):</u> path to the JSON file.

**Returns:**

<u>CalibrationResult:</u> the restored calibration, ready to pass to Scenarios.simulate(config, calibration=...).

**Raises:**

- <u>FileNotFoundError:</u> if `path` does not exist.
- <u>ValueError:</u> if the file is not a calibration written by save().

## build_toolkit

```python
build_toolkit(
    config: ScenariosConfig,
    api_key: str | None = None,
    fred_api_key: str | None = None,
) -> Toolkit
```

Build the `Toolkit` instance a Scenarios run calibrates against, entirely from
`config.toolkit` plus the tickers each factor section names (`config.tickers`).
The FMP/FRED API keys are the ones passed in; one left out is read from the environment
(`FINANCIAL_MODELING_PREP_API_KEY`, `FRED_API_KEY`), loading a `.env` file first if present. Finance Toolkit
itself never talks to a data provider until a factor's calibrate() actually
requests data, so this is a cheap, side-effect-free construction.

`use_cached_data=True` and `allow_stale_oecd_cache=True` are always passed, not
exposed as config knobs: every external call Finance Toolkit makes (FMP, Yahoo
Finance, FRED, OECD, ...) is served from its shared, incremental, range-aware
SQLite cache whenever the requested tickers/dates are already covered, and a
rate-limited OECD call (60 downloads/hour, easy to hit across a multi-country
run) falls back to the most recently cached response rather than failing the
run outright.

**Args:**

- <u>config (ScenariosConfig):</u> a validated configuration, e.g. from load_config().
- <u>api_key (str &#124; None):</u> an API key from FinancialModelingPrep, obtain one at https://www.jeroenbouma.com/fmp. Defaults to None, which reads the FINANCIAL_MODELING_PREP_API_KEY environment variable (or `.env`).
- <u>fred_api_key (str &#124; None):</u> a free FRED API key (https://fred.stlouisfed.org/docs/api/api_key.html), used by credit, commercial real estate and breakeven inflation. Defaults to None, which reads FRED_API_KEY.

**Returns:**

<u>Toolkit:</u> a Finance Toolkit instance covering every ticker the configured factors need.
