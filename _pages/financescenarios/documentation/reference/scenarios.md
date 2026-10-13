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

Fits every configured factor (interest rates, inflation, equities, currencies, commodities, credit and more) to
live data and simulates correlated scenarios of them.

A `Scenarios` holds one configuration: a settings profile (how the run executes: the number of scenarios, the step
size, the horizon) and a factor set (what is simulated). `simulate()` first fits each factor to its history (the
calibration), then draws thousands of linked future paths and returns them as a `ScenarioSet`. Start with
`from_profiles`, which reads the ready-made profiles; `list_presets()` lists them.

| Method | What it does |
|:-------|:-------------|
| `simulate()` | calibrates, then simulates; `regime=` runs a stress story, `measure="risk_neutral"` the market run |
| `calibrate()` | only the fit, to save and replay later without downloading again |
| `validate(result)` | checks a run in one table |
| `history(...)` | what actually happened, in the same shape, for a backtest |
| `save(result)` | stores a run with its config and calibration; `read_run(path)` reads it back |

The design, a cascade of linked, correlated factors simulated over the full horizon, follows the actuarial models
of Wilkie (1986), Ahlgrim, D'Arcy & Gorvett (2005) and Hibbert, Mowbray & Turnbull (2001). Building one directly
(`Scenarios(toolkit, ...)`) is for code that assembles its own Toolkit and config.

**As an example:**

```python
from financescenarios import Scenarios, list_presets

list_presets()  # every name you can pass, and the argument it goes in
scenarios = Scenarios.from_profiles(settings="default", factor_set="us_only")
result = scenarios.simulate(n_simulations=100)  # calibrates first, then simulates
result.describe()
```

**References:**

- Wilkie, A.D. (1986). "A stochastic investment model for actuarial use." Transactions of the Faculty of Actuaries, 39, 341-403. <https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf>
- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2005). "Modeling Financial Scenarios: A Framework for the Actuarial Profession." Proceedings of the CAS, 92. <https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf>
- Hibbert, J., Mowbray, P., Turnbull, C. (2001). "A Stochastic Asset Model & Calibration for Long-Term Financial Planning Purposes." Barrie & Hibbert. <https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf>

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

Build a `Scenarios` from a loaded configuration. The config is kept on the instance, so `simulate()` needs no
arguments.

Use it when the configuration comes from your own files or code; `from_profiles` is the shortcut for named
profiles. A Finance Toolkit covering every ticker the factors need is built for you (see `build_toolkit`).

**Args:**

- <u>config (ScenariosConfig):</u> a validated configuration, e.g. from `load_config()`.
- <u>toolkit (Toolkit &#124; None):</u> your own Finance Toolkit to use instead. Defaults to None.
- <u>bond_panel (BondPanel &#124; None):</u> your own bond data for the credit-spread curve factor. Defaults to None.
- <u>regime (Regime &#124; None):</u> a stress regime: its belief overrides change `config`, and its targets narrow every `simulate()` result. Defaults to None.
- <u>api_key (str &#124; None):</u> an API key from FinancialModelingPrep, obtain one at https://www.jeroenbouma.com/fmp. Defaults to None, which reads FINANCIAL_MODELING_PREP_API_KEY (or a `.env` file). Unused with `toolkit`.
- <u>fred_api_key (str &#124; None):</u> a free FRED API key (https://fred.stlouisfed.org/docs/api/api_key.html), used by credit and commercial real estate. Defaults to None, which reads FRED_API_KEY.

**Returns:**

<u>Scenarios:</u> an instance holding `config`.

**Raises:**

- <u>ValueError:</u> if the regime targets a factor the config does not simulate.

**As an example:**

```python
from financescenarios import Scenarios, load_config

scenarios = Scenarios.from_config(load_config("settings/default.yaml"))
result = scenarios.simulate()
```

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

The one-call way in: pick a settings profile, a factor set and optionally a stress regime, and get a ready-to-run
`Scenarios`.

A settings profile says how the run executes (scenarios, step size, horizon), a factor set what is simulated
(factors, tickers, beliefs), and a regime is a named stress story. `list_presets()` lists every name. Folders of
your own (from `scaffold_project()`) are read when they exist, the bundled profiles otherwise.

**Args:**

- <u>settings (str):</u> the settings profile, e.g. "default" or "long_horizon". Defaults to "default".
- <u>factor_set (str):</u> the factor set, e.g. "default" or "us_only". Defaults to "default".
- <u>regime (str &#124; Regime &#124; None):</u> a regime's id ("oil_crisis") or name ("Oil Crisis"), a loaded `Regime`, or None for no stress. Defaults to None.
- <u>settings_dir (str &#124; Path):</u> the folder of settings profiles. Defaults to "settings".
- <u>factor_sets_dir (str &#124; Path):</u> the folder of factor sets. Defaults to "factor-sets".
- <u>regimes_dir (str &#124; Path):</u> the folder of regimes, read when a regime is named here or in `simulate()`. Defaults to "regimes".
- <u>toolkit (Toolkit &#124; None):</u> your own Finance Toolkit to use instead. Defaults to None.
- <u>bond_panel (BondPanel &#124; None):</u> your own bond data for the credit-spread curve factor. Defaults to None.
- <u>api_key (str &#124; None):</u> an API key from FinancialModelingPrep, obtain one at https://www.jeroenbouma.com/fmp. Defaults to None, which reads FINANCIAL_MODELING_PREP_API_KEY (or a `.env` file).
- <u>fred_api_key (str &#124; None):</u> an optional, free FRED API key; see `from_config()`. Defaults to None.

**Returns:**

<u>Scenarios:</u> an instance holding the resolved config and regime.

**Raises:**

- <u>FileNotFoundError:</u> if a profile or the named regime does not exist.
- <u>pydantic.ValidationError:</u> if the profiles do not form a valid configuration.
- <u>TypeError:</u> if `regime` is neither a name nor a `Regime`.

**As an example:**

```python
scenarios = Scenarios.from_profiles(
    settings="default", factor_set="us_only", regime="oil_crisis", api_key="FINANCIAL_MODELING_PREP_KEY"
)
result = scenarios.simulate()
```

## Scenarios.from_config_file

```python
Scenarios.from_config_file(
    config_path: str,
    factors_path: str | None = None,
) -> tuple[Scenarios, ScenariosConfig]
```

Build a `Scenarios` from two YAML files: the run settings and the factor definitions.

The two-file counterpart of `load_config()`; `from_profiles()` is the usual way in for named profiles.

**Args:**

- <u>config_path (str):</u> the run-settings YAML file.
- <u>factors_path (str &#124; None):</u> the factor-definitions YAML file. Defaults to None, a `factors.yaml` next to `config_path`.

**Returns:**

<u>tuple[Scenarios, ScenariosConfig]:</u> the instance and the loaded config, which the instance also keeps.

## Scenarios.config

```python
scenarios.config  # property -> ScenariosConfig | None
```

The configuration this instance runs, with its regime's belief overrides already applied: what `calibrate()` and
`simulate()` use when called without one. None when the instance was built directly without a config.

## Scenarios.regime

```python
scenarios.regime  # property -> Regime | None
```

The regime applied to this instance, if any; see `from_profiles()`.

## Scenarios.calibration

```python
scenarios.calibration  # property -> Calibration
```

The object that fits each factor; the per-factor properties (`interest_rates`, `inflation`, ...) reach into it.

## Scenarios.correlation_fallback_pairs

```python
scenarios.correlation_fallback_pairs  # property -> list[str]
```

The "factor_a/factor_b" pairs the latest calibration set to zero correlation (assumed unrelated) because they
shared too little history. Empty when every pair had enough.

## Scenarios.last_calibration

```python
scenarios.last_calibration  # property -> CalibrationResult | None
```

The calibration the latest `simulate()` ran on, or None before the first. Save it (`CalibrationResult.save()`) to
replay this fit later without downloading again, or pass it to `simulate(calibration=...)` for another seed or
number of scenarios.

## Scenarios.calibration_failures

```python
scenarios.calibration_failures  # property -> dict[str, str]
```

The factors the latest calibration could not fit, with the reason (e.g. no mean reversion over a short history).
They are left out of the run rather than stopping it; empty when everything fit.

## Scenarios.interest_rates

```python
scenarios.interest_rates  # property
```

Fits the interest rate factors.

## Scenarios.inflation

```python
scenarios.inflation  # property
```

Fits the inflation factors.

## Scenarios.knw

```python
scenarios.knw  # property
```

Fits the joint interest rate and inflation model of `method: knw` (opt-in).

## Scenarios.knw_sv

```python
scenarios.knw_sv  # property
```

Fits the stochastic-volatility version of that model, `method: knw_sv` (opt-in).

## Scenarios.equities

```python
scenarios.equities  # property
```

Fits the equity factors.

## Scenarios.unemployment

```python
scenarios.unemployment  # property
```

Fits the unemployment factors.

## Scenarios.term_structure

```python
scenarios.term_structure  # property
```

Fits the Nelson-Siegel yield curve's level, slope and curvature (opt-in).

## Scenarios.credit_term_structure

```python
scenarios.credit_term_structure  # property
```

Fits the Nelson-Siegel credit-spread curve's level, slope and curvature to a panel of real bonds (opt-in).

## Scenarios.hjm

```python
scenarios.hjm  # property
```

Fits the two-factor Gaussian HJM forward-rate curve (opt-in).

## Scenarios.real_estate

```python
scenarios.real_estate  # property
```

Fits the real estate factors (opt-in).

## Scenarios.credit

```python
scenarios.credit  # property
```

Fits the credit spread factors (opt-in).

## Scenarios.leading_indicator

```python
scenarios.leading_indicator  # property
```

Fits the leading indicator factors (opt-in).

## Scenarios.credit_migration

```python
scenarios.credit_migration  # property
```

Fits the credit cycle behind rating migrations (opt-in).

## Scenarios.fx

```python
scenarios.fx  # property
```

Fits the exchange rate factors (opt-in).

## Scenarios.commodities

```python
scenarios.commodities  # property
```

Fits the commodity factors (opt-in).

## Scenarios.dividend_yield

```python
scenarios.dividend_yield  # property
```

Fits the dividend yield factors (opt-in).

## Scenarios.dividend_growth

```python
scenarios.dividend_growth  # property
```

Fits the dividend growth factors (opt-in).

## Scenarios.mortality

```python
scenarios.mortality  # property
```

Fits the mortality (longevity) factors (opt-in).

## Scenarios.dependence

```python
scenarios.dependence  # property -> Dependence
```

Builds the correlation matrix that links the factors; see `Dependence`.

## Scenarios.calibrate

```python
calibrate(
    config: ScenariosConfig | None = None,
    mortality_rates: pl.DataFrame | None = None,
    mortality_ages: list[float] | None = None,
    mortality_years: list[int] | None = None,
) -> CalibrationResult
```

Fit every configured factor to its history and build the correlation matrix, without simulating.

`simulate()` calls this for you. Call it yourself to keep the result: save it with `CalibrationResult.save()` and
pass it to `simulate(calibration=...)` later, to run again at another seed or number of scenarios without
downloading data. A factor that cannot be fitted is left out and listed in `calibration_failures` instead of
stopping the run.

**Args:**

- <u>config (ScenariosConfig &#124; None):</u> the configuration to fit. Defaults to None, the one this instance holds.
- <u>mortality_rates (pl.DataFrame &#124; None):</u> a historical mortality table (age x calendar year), needed only when mortality is enabled with `source: supplied`. Defaults to None.
- <u>mortality_ages (list[float] &#124; None):</u> the ages of the table's columns, needed with it. Defaults to None.
- <u>mortality_years (list[int] &#124; None):</u> the calendar years of the table's rows. Defaults to None, which takes the last row as the latest completed year.

**Returns:**

<u>CalibrationResult:</u> the fitted parameters, the correlation matrix and the order the factors are simulated in.

**Raises:**

- <u>RuntimeError:</u> if this instance has no Finance Toolkit.
- <u>ValueError:</u> if there is no config, or mortality is enabled with a supplied source but no rates or ages.

**As an example:**

```python
calibration = scenarios.calibrate()
calibration.save("calibration.json")
result = scenarios.simulate(calibration=calibration, seed=7)
```

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
    regime: str | Regime | None = None,
) -> ScenarioSet
```

Simulate the configured factors: fit them to their history (unless a saved calibration is given), then draw
correlated scenarios of every factor.

A saved `calibration` skips the download and the fit: replay a run offline, or draw it again with another `seed`
to see the Monte Carlo noise.

A `regime` ("oil_crisis"), passed here or set by `from_profiles`, tells a stress story: its beliefs change what
is simulated and its targets keep the scenarios that fit. You still get `n_simulations` scenarios, drawn in
batches until enough fit; each batch ranks its own draws, so "the worst 30%" is the worst 30% of a batch.

**Args:**

- <u>config (ScenariosConfig &#124; None):</u> the configuration to run, engine settings included. Defaults to None, the instance's own.
- <u>calibration (CalibrationResult &#124; None):</u> a saved calibration to simulate from, not with "risk_neutral". Defaults to None (calibrate).
- <u>mortality_rates (pl.DataFrame &#124; None):</u> passed to `calibrate()` for mortality. Defaults to None.
- <u>mortality_ages (list[float] &#124; None):</u> passed to `calibrate()` for mortality. Defaults to None.
- <u>mortality_years (list[int] &#124; None):</u> passed to `calibrate()` for mortality. Defaults to None.
- <u>seed (int &#124; None):</u> another random seed for this call. Defaults to None.
- <u>n_simulations (int &#124; None):</u> the number of scenarios to return; even under antithetic sampling. Defaults to None, the profile's number.
- <u>measure (str):</u> "real_world" (default), or "risk_neutral" for the market-consistent run that values liabilities.
- <u>years (float &#124; None):</u> how many years to simulate, e.g. 30. Defaults to None, the profile's horizon.
- <u>keep (int &#124; None):</u> the old name for `n_simulations`. Defaults to None.
- <u>regime (str &#124; Regime &#124; None):</u> a stress regime for this call: id, name ("Oil Crisis") or `Regime`. Defaults to None.

**Returns:**

<u>ScenarioSet:</u> every factor's simulated paths, with their dates and fitted parameters.

**Raises:**

- <u>ValueError:</u> if there is no config, a count is not positive, `keep` and `n_simulations` differ, the regime does not fit the config or keeps nothing, or the instance carries another regime.
- <u>TypeError:</u> if `calibration` or `regime` has the wrong type.
- <u>FileNotFoundError:</u> if no regime has the id or name given.

**As an example:**

```python
result = scenarios.simulate(n_simulations=2000)
oil_crisis = scenarios.simulate(regime="oil_crisis", n_simulations=500)
risk_neutral = scenarios.simulate(n_simulations=2000, measure="risk_neutral")
```

## Scenarios.history

```python
history(
    portfolio: str | None = None,
    factors: list[str] | None = None,
    period: str = 'monthly',
    portfolios_dir: str | Path = 'portfolios',
) -> ScenarioSet
```

What actually happened, as a one-scenario `ScenarioSet`, so `Portfolio` and every `ScenarioSet` method run on
history the same way they run on simulated scenarios (a backtest).

Each factor's historical series is fetched, and the series are lined up on the dates they all share.

**Args:**

- <u>portfolio (str &#124; None):</u> a portfolio preset's name, e.g. "balanced_60_40", whose holdings are fetched; `list_presets(kind="portfolios")` lists them. Defaults to None.
- <u>factors (list[str] &#124; None):</u> factor names to fetch instead. With neither, every factor with history is fetched; each one narrows the shared dates to its own window, so name only the ones you need. Defaults to None.
- <u>period (str):</u> the calendar to line the series up on: "daily", "weekly", "monthly" (default), "quarterly" or "yearly".
- <u>portfolios_dir (str &#124; Path):</u> where a named portfolio preset is looked up; the bundled presets otherwise. Defaults to "portfolios".

**Returns:**

<u>ScenarioSet:</u> one path per factor, `n_simulations=1`, on the shared dates.

**Raises:**

- <u>ValueError:</u> if this instance has no Finance Toolkit, both `portfolio` and `factors` are given, or the series share too few dates.
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

Check a run in one table, with the same checks the yearly published calibration passes.

Is this run fit to use? It checks that every factor calibrated, the fitted parameters are plausible, the
correlation matrix is valid, the scenarios move together as calibrated, each factor swings about as much as it did
historically, and every path is finite. A "warn" is worth a look but not a reason to discard the run.

**Args:**

- <u>result (ScenarioSet):</u> a run simulated from this instance's latest calibration.

**Returns:**

<u>pl.DataFrame:</u> one row per check: "check", "status" ("pass", "warn" or "fail"), "detail" (what was found, with the numbers) and "meaning" (what the check means).

**Raises:**

- <u>ValueError:</u> if nothing was calibrated yet, or this instance has no Finance Toolkit to fetch history with.
- <u>As an example, on the default profiles:</u> 
- ```python
- result = scenarios.simulate(n_simulations=2000)
- scenarios.validate(result)
- ```
- <u>Which returns (2 of the checks, without "meaning"):</u> 
- | check                   | status | detail                  |
- <u>&#124;:</u> ------------------------|:-------|:------------------------|
- | Every factor calibrated | pass   | every factor calibrated |
- | Every path is finite    | pass   | 27 factors, all finite  |

## Scenarios.save

```python
save(
    result: ScenarioSet,
    output_dir: str | Path = 'results',
    output_format: str = 'parquet',
) -> Path
```

Store a run with everything needed to read it back or replay it: the config, the regime, the calibration and one
file per factor.

**Args:**

- <u>result (ScenarioSet):</u> the run to store.
- <u>output_dir (str &#124; Path):</u> the folder runs are kept in; each run gets its own subfolder. Defaults to "results".
- <u>output_format (str):</u> "parquet" (default, smaller and faster) or "csv".

**Returns:**

<u>Path:</u> the run's own folder.

**As an example:**

```python
from financescenarios import read_run

path = scenarios.save(result, "results/")
result = read_run(path)
```

## CalibrationResult

```python
class CalibrationResult(BaseModel):
    calibrated_params: dict[str, CreditCycleParams | OUParams | RegimeParams | UnemploymentParams | YieldCurveParams | FXParams | CommodityParams | DividendYieldParams | DividendGrowthParams | WilkieConsolsParams | EquityDerivedParams | RandomWalkParams | GARCHParams | OUCovariateParams | DeterministicParams | DeterministicPathParams | HullWhiteForwardParams | AR1Params | MovingTargetOUParams | KnwParams | KnwSvLegParams | KnwSvEquityParams | HjmFactorParams | HestonParams]
    correlation_matrix: np.ndarray
    factor_names: list[str]
    dependencies: dict[str, list[str]]
    raw_long_run_means: dict[str, float] = Field(default_factory=dict, description='factor name -> its fitted long-run mean before any belief override. Only for mean-reverting factors (rates, inflation, unemployment and the like).')
    correlation_fallback_pairs: list[str] = Field(default_factory=list, description="'factor_a/factor_b' pairs set to 0 correlation because their histories overlap too little to estimate one. Only with engine.correlation_method='pairwise' (the default).")
    beliefs: dict[str, Any] | None = Field(default=None, description="the belief overrides this calibration applied, keyed '<category>.<name>'; simulate() refuses to replay it under a config with different beliefs. None for a calibration saved before this existed.")
    correlation_shrinkage: float | None = Field(default=None, description="the shrinkage intensity applied to the sample correlation matrix (the computed one with engine.correlation_shrinkage='auto'); None for a calibration saved before this was recorded.")
    correlation_repair: float | None = Field(default=None, description='how far the shrunk correlation matrix moved to become a valid one (Frobenius norm; 0 if it already was); large values mean the pairwise estimates disagreed. None for an older calibration.')
    long_run_anchors: dict[str, dict[str, float]] = Field(default_factory=dict, description="interest-rate factor name -> {year: long-run level} from that entry's long_run_anchor (EIOPA's forward rates), applied as its long-run belief path when simulating unless the config sets one itself. Empty for a calibration without anchors or saved before they existed.")
    calibration_failures: dict[str, str] = Field(default_factory=dict, description='factor name -> why it could not be fitted (e.g. no mean reversion over a short history), or the factor it depends on that failed. Those factors are left out of the run instead of stopping it; empty when everything calibrated.')
```

A finished calibration: every factor's fitted parameters and the correlation matrix, all that `simulate()` needs
without downloading data again.

`Scenarios.calibrate()` returns it, and `Scenarios.last_calibration` holds the one the latest run used. Save it to
reproduce a run later, or simulate from it again at another seed or number of scenarios without fitting again.

**Attributes:**

- <u>calibrated_params (dict):</u> factor name -> its fitted parameters.
- <u>correlation_matrix (np.ndarray):</u> how the factors' historical changes move together, in `factor_names` order.
- <u>factor_names (list[str]):</u> the calibrated factors, in the order they are simulated.
- <u>dependencies (dict[str, list[str]]):</u> factor name -> the factors it is simulated after.
- <u>raw_long_run_means (dict[str, float]):</u> factor name -> its fitted long-run mean before any belief override.
- <u>correlation_fallback_pairs (list[str]):</u> "factor_a/factor_b" pairs set to zero correlation for lack of shared history.
- <u>beliefs (dict[str, Any] &#124; None):</u> the fixed belief overrides this calibration applied.
- <u>correlation_shrinkage (float &#124; None):</u> how far the correlations were pulled toward their average.
- <u>correlation_repair (float &#124; None):</u> how far the matrix moved to become valid; large means the pairs disagreed.
- <u>long_run_anchors (dict[str, dict[str, float]]):</u> interest rate -> {year: long-run level} from EIOPA's curve.
- <u>calibration_failures (dict[str, str]):</u> factor name -> why it could not be fitted; it is left out of the run.

**As an example:**

```python
calibration = scenarios.calibrate()
calibration.describe()
calibration.save("calibration.json")
```

## CalibrationResult.describe

```python
describe() -> pl.DataFrame
```

One row per calibrated factor: which model was fitted and the parameters most worth a look.

This is the "what did the historical fit say" table, without digging into each factor's own parameters. Rates are
yearly decimals (0.024 is 2.4% a year), comparable down the column even for factors fitted to data of different
frequencies. `half_life_years` is how many years a shock takes to fade halfway back to the long-run mean,
ln(2) / mean_reversion_speed.

**Returns:**

<u>pl.DataFrame:</u> "factor", "process" (the fitted model, e.g. "OUParams"), "initial_value", "long_run_mean", "volatility", "mean_reversion_speed" and "half_life_years"; the last four are empty for a model without them, such as an equity regime fit.

**As an example:**

```python
scenarios.calibrate().describe()
```

## CalibrationResult.correlation_frame

```python
correlation_frame() -> pl.DataFrame
```

The calibrated correlation matrix as a labelled table: a "factor" column plus one column per factor. Set it next
to `ScenarioSet.simulated_correlation()` to check that a run reproduces the correlations it was calibrated with.

## CalibrationResult.plot

```python
plot(annotate: bool | None = None)
```

The quick chart of a calibration: its correlation matrix as a heatmap, the same as `plot_correlation_matrix()`.

**Args:**

- <u>annotate (bool &#124; None):</u> write each cell's value into it. Defaults to None, which does so up to 14 factors.

**Returns:**

<u>matplotlib.figure.Figure:</u> the figure holding the heatmap.

## CalibrationResult.plot_correlation_matrix

```python
plot_correlation_matrix(annotate: bool | None = None)
```

This calibration's correlation matrix as a heatmap, blue for negative and red for positive. The same chart as
`plot_correlation_matrix(calibration.correlation_matrix, calibration.factor_names)`.

**Args:**

- <u>annotate (bool &#124; None):</u> write each cell's value into it. Defaults to None, which does so up to 14 factors.

**Returns:**

<u>matplotlib.figure.Figure:</u> the figure holding the heatmap.

## CalibrationResult.save

```python
save(path: str | Path) -> None
```

Save this calibration to a JSON file, to simulate from it later without downloading data or fitting again.

**Args:**

- <u>path (str &#124; Path):</u> where to write the file.

**As an example:**

```python
scenarios.calibrate().save("calibration.json")
```

## CalibrationResult.load

```python
CalibrationResult.load(path: str | Path) -> CalibrationResult
```

Load a calibration written by `save()`, ready for `Scenarios.simulate(calibration=...)`.

**Args:**

- <u>path (str &#124; Path):</u> the JSON file.

**Returns:**

<u>CalibrationResult:</u> the restored calibration.

**Raises:**

- <u>FileNotFoundError:</u> if `path` does not exist.
- <u>ValueError:</u> if the file is not a calibration written by `save()`.

**As an example:**

```python
calibration = CalibrationResult.load("calibration.json")
result = scenarios.simulate(calibration=calibration, seed=7)
```

## build_toolkit

```python
build_toolkit(
    config: ScenariosConfig,
    api_key: str | None = None,
    fred_api_key: str | None = None,
) -> Toolkit
```

Build the Finance Toolkit a `Scenarios` run fetches its data with, covering every ticker the configured factors
need.

The start and end dates and the benchmark come from the config's `toolkit` section. Nothing is downloaded yet: data
is fetched when a factor is fitted, and served from the Finance Toolkit's local cache whenever it already holds it.
An API key left out is read from the environment, or from a `.env` file in the folder Python runs in.

**Args:**

- <u>config (ScenariosConfig):</u> a validated configuration, e.g. from `load_profiles()` or `load_config()`.
- <u>api_key (str &#124; None):</u> an API key from FinancialModelingPrep, obtain one at https://www.jeroenbouma.com/fmp. Defaults to None, which reads the FINANCIAL_MODELING_PREP_API_KEY environment variable (or `.env`); the examples' placeholder "FINANCIAL_MODELING_PREP_KEY" does the same.
- <u>fred_api_key (str &#124; None):</u> a free FRED API key (https://fred.stlouisfed.org/docs/api/api_key.html), used by credit and commercial real estate. Defaults to None, which reads FRED_API_KEY.

**Returns:**

<u>Toolkit:</u> a Finance Toolkit instance covering every ticker the configured factors need.

**As an example:**

```python
from financescenarios import build_toolkit, load_profiles

toolkit = build_toolkit(load_profiles(settings_id="default", factor_set_id="us_only"))
```
