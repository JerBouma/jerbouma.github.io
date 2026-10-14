---
title: "Scenarios"
seo_title: "Scenarios Reference | Finance Scenarios"
seo_title_suffix: false
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

Calibrate every configured factor and simulate correlated scenarios; also the saved calibration and the Toolkit builder.

```python
from financescenarios import Scenarios, CalibrationResult, build_toolkit
```

## Scenarios

An economic scenario generator: thousands of joint, internally consistent futures for interest rates, inflation,
equities, currencies, commodities, credit and more, each fitted to its own history.

Every factor follows a model suited to how it behaves. Rates, inflation and spreads revert to a long-run level at
their own historical speed; equities switch between calm and turbulent regimes, so bad months cluster; currencies
keep their historical volatility. The factors are linked in two ways. A correlation matrix estimated from their
historical changes means a scenario with an equity sell-off also tends to see what history saw alongside one. A
cascade lets one factor's path drive another's where theory says it should: inflation drives rates in the Wilkie
and KNW models, and with `drift_mode: irp` the rate gap drives a currency under uncovered interest rate parity
(the risk-neutral run uses covered parity instead). Your own views (a long-run inflation target, a stress story)
override the fit where you set them.

The real-world run (`simulate()`) is for ALM, strategic asset allocation and risk: how the economy may plausibly
evolve. The risk-neutral run (`measure="risk_neutral"`) is for valuation: it reproduces today's yield curve and
prices, as Solvency II's best estimate requires.

| Method | What it does |
|:-------|:-------------|
| `simulate()` | fits, then simulates; `regime=` runs a stress story, `measure="risk_neutral"` the market run |
| `calibrate()` | only the fit, to save and replay later without downloading again |
| `validate(result)` | checks a run in one table |
| `history(...)` | what actually happened, in the same shape, for a backtest |
| `save(result)` | stores a run with its config and calibration; `read_run(path)` reads it back |

The design, a cascade of linked, correlated factors simulated over the full horizon, follows the actuarial models
of Wilkie (1986), Ahlgrim, D'Arcy & Gorvett (2005) and Hibbert, Mowbray & Turnbull (2001).

**As an example:**

```python
from financescenarios import Scenarios, list_presets

list_presets()  # every name you can pass, and the argument it goes in
scenarios = Scenarios.from_profiles(settings="default", factor_set="us_only")
result = scenarios.simulate(n_simulations=100)
result.describe()
```

**References:**

- Wilkie, A.D. (1986). "A stochastic investment model for actuarial use." Transactions of the Faculty of Actuaries, 39, 341-403. <https://www.soa.org/globalassets/assets/library/monographs/50th-anniversary/investment-section/1999/january/m-as99-2-06.pdf>
- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2005). "Modeling Financial Scenarios: A Framework for the Actuarial Profession." Proceedings of the CAS, 92. <https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf>
- Hibbert, J., Mowbray, P., Turnbull, C. (2001). "A Stochastic Asset Model & Calibration for Long-Term Financial Planning Purposes." Barrie & Hibbert. <https://www.ressources-actuarielles.net/EXT/ISFA/1226.nsf/0/a1d9fb9416c79dfec12576020046e11b/$FILE/hibbert.pdf>

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
Scenarios(
    toolkit: Toolkit | None,
    n_simulations: int = 1000,
    n_steps: int = 52,
    time_step: float = 1 / 52,
    seed: int | None = None,
    antithetic: bool = False,
    shock_distribution: Literal['gaussian', 'student_t'] = 'gaussian',
    degrees_of_freedom: float = 12.0,
    bond_panel: BondPanel | None = None,
    config: ScenariosConfig | None = None,
    regime: Regime | None = None,
)
```

</details>

## Scenarios.from_config

Build a `Scenarios` from a loaded configuration. The config is kept on the instance, so `simulate()` needs no
arguments.

Use it when the configuration comes from your own files or code; `from_profiles` is the shortcut for named
profiles. A Finance Toolkit covering every ticker the factors need is built for you (see `build_toolkit`).

**As an example:**

```python
from financescenarios import Scenarios, load_config

scenarios = Scenarios.from_config(load_config("settings/default.yaml"))
result = scenarios.simulate()
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

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

</details>

## Scenarios.from_profiles

The one-call way in: pick a settings profile, a factor set and optionally a stress regime, and get a ready-to-run
`Scenarios`.

A settings profile says how the run executes (scenarios, step size, horizon), a factor set what is simulated
(factors, tickers, beliefs), and a regime is a named stress story. `list_presets()` lists every name. Folders of
your own (from `scaffold_project()`) are read when they exist, the bundled profiles otherwise.

**As an example:**

```python
scenarios = Scenarios.from_profiles(
    settings="default", factor_set="us_only", regime="oil_crisis", api_key="FINANCIAL_MODELING_PREP_KEY"
)
result = scenarios.simulate()
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

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

</details>

## Scenarios.from_config_file

Build a `Scenarios` from two YAML files: the run settings and the factor definitions.

The two-file counterpart of `load_config()`; `from_profiles()` is the usual way in for named profiles.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
Scenarios.from_config_file(
    config_path: str,
    factors_path: str | None = None,
) -> tuple[Scenarios, ScenariosConfig]
```

**Args:**

- <u>config_path (str):</u> the run-settings YAML file.
- <u>factors_path (str &#124; None):</u> the factor-definitions YAML file. Defaults to None, a `factors.yaml` next to `config_path`.

**Returns:**

<u>tuple[Scenarios, ScenariosConfig]:</u> the instance and the loaded config, which the instance also keeps.

</details>

## Scenarios.config

The configuration this instance runs, with its regime's belief overrides already applied: what `calibrate()` and
`simulate()` use when called without one. None when the instance was built directly without a config.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
scenarios.config  # property -> ScenariosConfig | None
```

</details>

## Scenarios.regime

The regime applied to this instance, if any; see `from_profiles()`.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
scenarios.regime  # property -> Regime | None
```

</details>

## Scenarios.calibration

The object that fits each factor; the per-factor properties (`interest_rates`, `inflation`, ...) reach into it.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
scenarios.calibration  # property -> Calibration
```

</details>

## Scenarios.correlation_fallback_pairs

The "factor_a/factor_b" pairs the latest calibration set to zero correlation (assumed unrelated) because they
shared too little history. Empty when every pair had enough.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
scenarios.correlation_fallback_pairs  # property -> list[str]
```

</details>

## Scenarios.last_calibration

The calibration the latest `simulate()` ran on, or None before the first. Save it (`CalibrationResult.save()`) to
replay this fit later without downloading again, or pass it to `simulate(calibration=...)` for another seed or
number of scenarios.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
scenarios.last_calibration  # property -> CalibrationResult | None
```

</details>

## Scenarios.calibration_failures

The factors the latest calibration could not fit, with the reason (e.g. no mean reversion over a short history).
They are left out of the run rather than stopping it; empty when everything fit.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
scenarios.calibration_failures  # property -> dict[str, str]
```

</details>

## Scenarios.interest_rates

Fits the interest rate factors.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
scenarios.interest_rates  # property
```

</details>

## Scenarios.inflation

Fits the inflation factors.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
scenarios.inflation  # property
```

</details>

## Scenarios.knw

Fits the joint interest rate and inflation model of `method: knw` (opt-in).

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
scenarios.knw  # property
```

</details>

## Scenarios.knw_sv

Fits the stochastic-volatility version of that model, `method: knw_sv` (opt-in).

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
scenarios.knw_sv  # property
```

</details>

## Scenarios.equities

Fits the equity factors.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
scenarios.equities  # property
```

</details>

## Scenarios.unemployment

Fits the unemployment factors.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
scenarios.unemployment  # property
```

</details>

## Scenarios.term_structure

Fits the Nelson-Siegel yield curve's level, slope and curvature (opt-in).

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
scenarios.term_structure  # property
```

</details>

## Scenarios.credit_term_structure

Fits the Nelson-Siegel credit-spread curve's level, slope and curvature to a panel of real bonds (opt-in).

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
scenarios.credit_term_structure  # property
```

</details>

## Scenarios.hjm

Fits the two-factor Gaussian HJM forward-rate curve (opt-in).

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
scenarios.hjm  # property
```

</details>

## Scenarios.real_estate

Fits the real estate factors (opt-in).

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
scenarios.real_estate  # property
```

</details>

## Scenarios.credit

Fits the credit spread factors (opt-in).

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
scenarios.credit  # property
```

</details>

## Scenarios.leading_indicator

Fits the leading indicator factors (opt-in).

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
scenarios.leading_indicator  # property
```

</details>

## Scenarios.credit_migration

Fits the credit cycle behind rating migrations (opt-in).

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
scenarios.credit_migration  # property
```

</details>

## Scenarios.fx

Fits the exchange rate factors (opt-in).

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
scenarios.fx  # property
```

</details>

## Scenarios.commodities

Fits the commodity factors (opt-in).

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
scenarios.commodities  # property
```

</details>

## Scenarios.dividend_yield

Fits the dividend yield factors (opt-in).

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
scenarios.dividend_yield  # property
```

</details>

## Scenarios.dividend_growth

Fits the dividend growth factors (opt-in).

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
scenarios.dividend_growth  # property
```

</details>

## Scenarios.mortality

Fits the mortality (longevity) factors (opt-in).

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
scenarios.mortality  # property
```

</details>

## Scenarios.dependence

Builds the correlation matrix that links the factors; see `Dependence`.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
scenarios.dependence  # property -> Dependence
```

</details>

## Scenarios.calibrate

Fit every configured factor to its history and estimate how the factors move together, without simulating.

The calibration is where the scenarios get their economics: each factor's long-run level, how fast it reverts
to it after a shock, how volatile it is and how its changes correlate with every other factor's. Your beliefs
then override the fitted values where you set them, and the fitted long-run levels are kept beside them so you
can see how far a view departs from history.

Keep a calibration to make a study reproducible: the same fit can be saved, audited, and simulated again with
more scenarios or another seed without new data. A factor whose history cannot support its model (no visible
mean reversion over a short window, say) is left out of the run and listed with the reason in
`calibration_failures`, rather than stopping everything.

**As an example:**

```python
calibration = scenarios.calibrate()
calibration.save("calibration.json")
result = scenarios.simulate(calibration=calibration, seed=7)
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
calibrate(
    config: ScenariosConfig | None = None,
    mortality_rates: pl.DataFrame | None = None,
    mortality_ages: list[float] | None = None,
    mortality_years: list[int] | None = None,
) -> CalibrationResult
```

**Args:**

- <u>config (ScenariosConfig &#124; None):</u> the configuration to fit. Defaults to None, the one this instance holds.
- <u>mortality_rates (pl.DataFrame &#124; None):</u> your own historical mortality rates (calendar year by age), for mortality with `source: supplied`. Defaults to None.
- <u>mortality_ages (list[float] &#124; None):</u> the ages of that table. Defaults to None.
- <u>mortality_years (list[int] &#124; None):</u> the calendar years of that table. Defaults to None, which treats the last row as the latest completed year.

**Returns:**

<u>CalibrationResult:</u> every factor's fitted parameters and the correlation matrix.

**Raises:**

- <u>RuntimeError:</u> if this instance has no Finance Toolkit.
- <u>ValueError:</u> if there is no config, or mortality is enabled with a supplied source but no rates or ages.

</details>

## Scenarios.simulate

Simulate thousands of joint futures of every configured factor, each fitted to its own history and linked to the
others through their historical correlations.

The default real-world run answers "how might the economy evolve?", from history and your beliefs: the run for
ALM, asset allocation and risk budgets. The risk-neutral run (`measure="risk_neutral"`) answers "what is it worth
today?": the short rate is a Hull-White rate that reproduces EIOPA's risk-free curve (the Treasury curve for a
currency EIOPA does not cover), equities earn that rate less their dividend yield, so discounted prices stay
at today's prices, and inflation moves around the bond market's breakeven curve, as Solvency II's best
estimate requires. Rate and inflation volatilities come from history, since no option prices are available.
Factors without a traded price, such as credit or real estate, are left out of it; see `risk_neutral_config`.

A `regime` such as "oil_crisis" tells a stress story. Its beliefs shift what the model expects (inflation pulled
towards 12%); its targets keep the scenarios that play out the story (high rates, weak stocks). Targets are
quantiles of what the model itself produces, so the kept paths stay plausible. You still get `n_simulations`
scenarios back.

A saved `calibration` skips the download and the fit; another `seed` shows how much of a result is Monte Carlo
noise.

**As an example:**

```python
result = scenarios.simulate(n_simulations=2000)
oil_crisis = scenarios.simulate(regime="oil_crisis", n_simulations=500)
risk_neutral = scenarios.simulate(n_simulations=2000, measure="risk_neutral")
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

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

**Args:**

- <u>config (ScenariosConfig &#124; None):</u> the configuration to run, engine settings included. Defaults to None, the instance's own.
- <u>calibration (CalibrationResult &#124; None):</u> a saved calibration to simulate from (real-world runs only). Defaults to None, which fits the factors first.
- <u>mortality_rates (pl.DataFrame &#124; None):</u> your own mortality table; see `calibrate()`. Defaults to None.
- <u>mortality_ages (list[float] &#124; None):</u> the ages of that table; see `calibrate()`. Defaults to None.
- <u>mortality_years (list[int] &#124; None):</u> the calendar years of that table; see `calibrate()`. Defaults to None.
- <u>seed (int &#124; None):</u> a random seed for this call, for a repeatable run. Defaults to None, the profile's.
- <u>n_simulations (int &#124; None):</u> the number of scenarios to return. Defaults to None, the profile's number.
- <u>measure (str):</u> "real_world" (default) for planning and risk, or "risk_neutral" for market-consistent valuation.
- <u>years (float &#124; None):</u> how many years to simulate, e.g. 30. Defaults to None, the profile's horizon.
- <u>keep (int &#124; None):</u> an alias of `n_simulations`. Defaults to None.
- <u>regime (str &#124; Regime &#124; None):</u> a stress regime for this call: id, name ("Oil Crisis") or `Regime`. Defaults to None.

**Returns:**

<u>ScenarioSet:</u> every factor's simulated paths, with their dates and the parameters they were fitted with.

**Raises:**

- <u>ValueError:</u> if there is no config, a count is not positive, `keep` and `n_simulations` differ, the regime does not fit the config or keeps nothing, or the instance carries another regime.
- <u>TypeError:</u> if `calibration` or `regime` has the wrong type.
- <u>FileNotFoundError:</u> if no regime has the id or name given.

</details>

## Scenarios.history

What actually happened, in the same shape as a simulated run, so a portfolio or a risk measure can be backtested
with exactly the code you use on the scenarios.

The realized history is one scenario: every `ScenarioSet` and `Portfolio` method works on it, so you can set the
simulated distribution of, say, a 60/40 portfolio's drawdown next to the one drawdown history delivered. The
series are lined up on the dates they all share, so the window is as long as the shortest history you ask for.

**As an example:**

```python
history = scenarios.history(portfolio="balanced_60_40")
Portfolio.from_preset(history, preset="balanced_60_40").factor_exposure()
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
history(
    portfolio: str | None = None,
    factors: list[str] | None = None,
    period: str = 'monthly',
    portfolios_dir: str | Path = 'portfolios',
) -> ScenarioSet
```

**Args:**

- <u>portfolio (str &#124; None):</u> a portfolio preset's name, e.g. "balanced_60_40", whose holdings are fetched; `list_presets(kind="portfolios")` lists them. Defaults to None.
- <u>factors (list[str] &#124; None):</u> the factors to fetch instead; name only the ones you need, since each shortens the shared window to its own history. Defaults to None, every factor with history.
- <u>period (str):</u> the calendar to line the series up on: "daily", "weekly", "monthly" (default), "quarterly" or "yearly".
- <u>portfolios_dir (str &#124; Path):</u> a folder of your own portfolio presets; the bundled ones otherwise. Defaults to "portfolios".

**Returns:**

<u>ScenarioSet:</u> one scenario holding each factor's realized path on the shared dates.

**Raises:**

- <u>ValueError:</u> if this instance has no Finance Toolkit, both `portfolio` and `factors` are given, or the series share too few dates.
- <u>KeyError:</u> if a named factor has no history.

</details>

## Scenarios.validate

Is this run fit to use? One table of the checks a model validator would ask for, the same ones the yearly
published calibration passes.

It checks that every factor calibrated, the fitted parameters are economically plausible (rates settling
between -5% and 25%, shocks halving in between a week and 50 years), the correlation matrix is a valid one, the
scenarios move together as calibrated, each factor swings about as much as it did historically, and no path
explodes. A "warn" is worth a look but not a reason to discard the run; a "fail" is.

**As an example:**

On the default profiles:

```python
result = scenarios.simulate(n_simulations=2000)
scenarios.validate(result)
```

Which returns (2 of the checks, without "meaning"):

| check                   | status | detail                  |
|:------------------------|:-------|:------------------------|
| Every factor calibrated | pass   | every factor calibrated |
| Every path is finite    | pass   | 27 factors, all finite  |

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
validate(result: ScenarioSet) -> pl.DataFrame
```

**Args:**

- <u>result (ScenarioSet):</u> the run to check, simulated from this instance's latest calibration.

**Returns:**

<u>pl.DataFrame:</u> one row per check: "check", "status" ("pass", "warn" or "fail"), "detail" (what was found, with the numbers) and "meaning" (what the check means).

**Raises:**

- <u>ValueError:</u> if nothing was calibrated yet, or this instance has no Finance Toolkit to fetch history with.

</details>

## Scenarios.save

Store a run with everything needed to read it back, audit it or replay it: the scenarios, the configuration and
regime behind them, and the calibration they were drawn from.

**As an example:**

```python
from financescenarios import read_run

path = scenarios.save(result, "results/")
result = read_run(path)
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
save(
    result: ScenarioSet,
    output_dir: str | Path = 'results',
    output_format: str = 'parquet',
) -> Path
```

**Args:**

- <u>result (ScenarioSet):</u> the run to store.
- <u>output_dir (str &#124; Path):</u> the folder runs are kept in; each run gets its own subfolder. Defaults to "results".
- <u>output_format (str):</u> "parquet" (default, smaller and faster) or "csv".

**Returns:**

<u>Path:</u> the run's own folder.

</details>

## CalibrationResult

A finished calibration: every factor's fitted parameters and the correlation matrix, all that `simulate()` needs
without downloading data again.

`Scenarios.calibrate()` returns it, and `Scenarios.last_calibration` holds the one the latest run used. Save it to
reproduce a run later, or simulate from it again at another seed or number of scenarios without fitting again.

**As an example:**

```python
calibration = scenarios.calibrate()
calibration.describe()
calibration.save("calibration.json")
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
class CalibrationResult(BaseModel):
    calibrated_params: dict[str, CreditCycleParams | OUParams | RegimeParams | UnemploymentParams | YieldCurveParams | FXParams | CommodityParams | DividendYieldParams | DividendGrowthParams | WilkieConsolsParams | EquityDerivedParams | RandomWalkParams | GARCHParams | OUCovariateParams | DeterministicParams | BreakevenInflationParams | DeterministicPathParams | HullWhiteForwardParams | AR1Params | MovingTargetOUParams | KnwParams | KnwSvLegParams | KnwSvEquityParams | HjmFactorParams | HestonParams]
    correlation_matrix: np.ndarray
    factor_names: list[str]
    dependencies: dict[str, list[str]]
    raw_long_run_means: dict[str, float] = Field(default_factory=dict, description='factor name -> its fitted long-run mean before any belief override. Only for mean-reverting factors (rates, inflation, unemployment and the like).')
    correlation_fallback_pairs: list[str] = Field(default_factory=list, description="'factor_a/factor_b' pairs set to 0 correlation because their histories overlap too little to estimate one.")
    beliefs: dict[str, Any] | None = Field(default=None, description="the belief overrides this calibration applied, keyed '<category>.<name>'; simulate() refuses to replay it under a config with different beliefs.")
    correlation_shrinkage: float | None = Field(default=None, description="how far the historical correlations were shrunk to tame estimation noise, toward zero for 'auto' and toward their average for a fixed share (0 is none, 1 is all the way).")
    correlation_repair: float | None = Field(default=None, description='how far the correlation matrix moved to become a valid one (0 if it already was); large values mean the pairwise estimates disagreed.')
    long_run_anchors: dict[str, dict[str, float]] = Field(default_factory=dict, description="interest-rate factor name -> {year: long-run level} from EIOPA's forward rates, the path the rate is pulled towards unless the config sets a long-run belief itself.")
    calibration_failures: dict[str, str] = Field(default_factory=dict, description='factor name -> why it could not be fitted (e.g. no mean reversion over a short history), or the factor it depends on that failed. Those factors are left out of the run instead of stopping it; empty when everything calibrated.')
```

**Attributes:**

- <u>calibrated_params (dict):</u> factor name -> its fitted parameters.
- <u>correlation_matrix (np.ndarray):</u> how the factors' historical changes move together, in `factor_names` order.
- <u>factor_names (list[str]):</u> the calibrated factors, in the order they are simulated.
- <u>dependencies (dict[str, list[str]]):</u> factor name -> the factors it is simulated after.
- <u>raw_long_run_means (dict[str, float]):</u> factor name -> its fitted long-run mean before any belief override.
- <u>correlation_fallback_pairs (list[str]):</u> "factor_a/factor_b" pairs set to zero correlation for lack of shared history.
- <u>beliefs (dict[str, Any] &#124; None):</u> the fixed belief overrides this calibration applied.
- <u>correlation_shrinkage (float &#124; None):</u> how far the correlations were shrunk (toward zero for "auto").
- <u>correlation_repair (float &#124; None):</u> how far the matrix moved to become valid; large means the pairs disagreed.
- <u>long_run_anchors (dict[str, dict[str, float]]):</u> interest rate -> {year: long-run level} from EIOPA's curve.
- <u>calibration_failures (dict[str, str]):</u> factor name -> why it could not be fitted; it is left out of the run.

</details>

## CalibrationResult.describe

One row per calibrated factor: which model was fitted and the parameters most worth a look.

This is the "what did the historical fit say" table, without digging into each factor's own parameters. Rates are
yearly decimals (0.024 is 2.4% a year), comparable down the column even for factors fitted to data of different
frequencies. `half_life_years` is how many years a shock takes to fade halfway back to the long-run mean,
ln(2) / mean_reversion_speed.

**As an example:**

```python
scenarios.calibrate().describe()
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
describe() -> pl.DataFrame
```

**Returns:**

<u>pl.DataFrame:</u> "factor", "process" (the fitted model, e.g. "OUParams"), "initial_value", "long_run_mean", "volatility", "mean_reversion_speed" and "half_life_years"; the last four are empty for a model without them, such as an equity regime fit.

</details>

## CalibrationResult.correlation_frame

The calibrated correlation matrix as a labelled table: a "factor" column plus one column per factor. Set it next
to `ScenarioSet.simulated_correlation()` to check that a run reproduces the correlations it was calibrated with.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
correlation_frame() -> pl.DataFrame
```

</details>

## CalibrationResult.plot

The quick chart of a calibration: its correlation matrix as a heatmap, the same as `plot_correlation_matrix()`.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
plot(annotate: bool | None = None)
```

**Args:**

- <u>annotate (bool &#124; None):</u> write each cell's value into it. Defaults to None, which does so up to 14 factors.

**Returns:**

<u>matplotlib.figure.Figure:</u> the figure holding the heatmap.

</details>

## CalibrationResult.plot_correlation_matrix

This calibration's correlation matrix as a heatmap, blue for negative and red for positive. The same chart as
`plot_correlation_matrix(calibration.correlation_matrix, calibration.factor_names)`.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
plot_correlation_matrix(annotate: bool | None = None)
```

**Args:**

- <u>annotate (bool &#124; None):</u> write each cell's value into it. Defaults to None, which does so up to 14 factors.

**Returns:**

<u>matplotlib.figure.Figure:</u> the figure holding the heatmap.

</details>

## CalibrationResult.save

Save this calibration to a JSON file, to simulate from it later without downloading data or fitting again.

**As an example:**

```python
scenarios.calibrate().save("calibration.json")
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
save(path: str | Path) -> None
```

**Args:**

- <u>path (str &#124; Path):</u> where to write the file.

</details>

## CalibrationResult.load

Load a calibration written by `save()`, ready for `Scenarios.simulate(calibration=...)`.

**As an example:**

```python
calibration = CalibrationResult.load("calibration.json")
result = scenarios.simulate(calibration=calibration, seed=7)
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
CalibrationResult.load(path: str | Path) -> CalibrationResult
```

**Args:**

- <u>path (str &#124; Path):</u> the JSON file.

**Returns:**

<u>CalibrationResult:</u> the restored calibration.

**Raises:**

- <u>FileNotFoundError:</u> if `path` does not exist.
- <u>ValueError:</u> if the file is not a calibration written by `save()`.

</details>

## build_toolkit

Build the Finance Toolkit a `Scenarios` run fetches its data with, covering every ticker the configured factors
need.

The start and end dates and the benchmark come from the config's `toolkit` section. Nothing is downloaded yet: data
is fetched when a factor is fitted, and served from the Finance Toolkit's local cache whenever it already holds it.
An API key left out is read from the environment, or from a `.env` file in the folder Python runs in.

**As an example:**

```python
from financescenarios import build_toolkit, load_profiles

toolkit = build_toolkit(load_profiles(settings_id="default", factor_set_id="us_only"))
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
build_toolkit(
    config: ScenariosConfig,
    api_key: str | None = None,
    fred_api_key: str | None = None,
) -> Toolkit
```

**Args:**

- <u>config (ScenariosConfig):</u> a validated configuration, e.g. from `load_profiles()` or `load_config()`.
- <u>api_key (str &#124; None):</u> an API key from FinancialModelingPrep, obtain one at https://www.jeroenbouma.com/fmp. Defaults to None, which reads the FINANCIAL_MODELING_PREP_API_KEY environment variable (or `.env`); the examples' placeholder "FINANCIAL_MODELING_PREP_KEY" does the same.
- <u>fred_api_key (str &#124; None):</u> a free FRED API key (https://fred.stlouisfed.org/docs/api/api_key.html), used by credit and commercial real estate. Defaults to None, which reads FRED_API_KEY.

**Returns:**

<u>Toolkit:</u> a Finance Toolkit instance covering every ticker the configured factors need.

</details>
