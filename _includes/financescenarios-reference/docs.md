## Reference

The reference is generated from the docstrings in the package, so it says what `help(...)` says in Python: what each class and function does, a worked example with real output where the docstring has one, and the arguments and return value folded underneath.

Everything on this page imports as follows:

```python
from financescenarios import Scenarios, ScenarioSet, CalibrationResult, FactorLabel, compare_runs, build_toolkit, set_display, set_log_level
```

### Scenarios

An economic scenario generator: thousands of joint, internally consistent futures for interest rates, inflation,
equities, currencies, commodities, credit and more, each fitted to its own history.

Every factor follows a model suited to how it behaves. In the default factor set a short rate follows a central
bank's policy rule from the market's expected path, a long rate is its short rate's expected path plus a term
premium, inflation and unemployment switch between calm and high regimes, and equities between calm and turbulent
ones, so bad months cluster; credit spreads, when added, revert to a long-run level at their own speed. The
factors are linked in two ways. A correlation matrix estimated from their historical changes means a scenario with
an equity sell-off also tends to see what history saw alongside one. A cascade lets one factor's path drive
another's where theory says it should: simulated inflation and unemployment set the short rate through the policy
rule and the short rate sets the long rate, inflation drives rates in the Wilkie and KNW models, and with
`drift_mode: irp` the rate gap drives a currency under uncovered interest rate parity (the risk-neutral run uses
covered parity instead). Your own views (a long-run inflation target, a stress story)
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
| `out_of_sample(as_of)` | fits and simulates from a past date, scored against what happened next |
| `save(result)` | stores a run with its config and calibration; `read_run(path)` reads it back |

The design, a cascade of linked, correlated factors simulated over the full horizon, follows the actuarial models
of Wilkie (1986), Ahlgrim, D'Arcy and Gorvett (2005) and Hibbert, Mowbray and Turnbull (2001).

**As an example:**

```python
from financescenarios import Scenarios, list_presets

list_presets()  # every name you can pass, and the argument it goes in
scenarios = Scenarios.from_profiles(settings="default", factor_set="default")
result = scenarios.simulate(n_simulations=100)
result.describe()
```

**References:**

- Wilkie, A.D. (1986). "A stochastic investment model for actuarial use." Transactions of the Faculty of Actuaries, 39, 341-403. <https://doi.org/10.1017/S0071368600009009>
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

#### Scenarios.from_config

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

#### Scenarios.from_profiles

The one-call way in: pick a settings profile, a factor set and optionally a stress regime, and get a ready-to-run
`Scenarios`.

A settings profile says how the run executes (scenarios, step size, horizon), a factor set what is simulated
(factors, tickers, beliefs), and a regime is a named stress story. `list_presets()` lists every name. Folders of
your own (from `scaffold_project()`) are read when they exist, the bundled profiles otherwise.

**As an example:**

```python
scenarios = Scenarios.from_profiles(
    settings="default", factor_set="default", regime="oil_crisis", api_key="FINANCIAL_MODELING_PREP_KEY"
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
- <u>factor_set (str):</u> the factor set, e.g. "default" or "broad". Defaults to "default".
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

#### Scenarios.from_config_file

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

#### Scenarios.config

The configuration this instance runs, with its regime's belief overrides already applied: what `calibrate()` and
`simulate()` use when called without one. None when the instance was built directly without a config.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
scenarios.config  # property -> ScenariosConfig | None
```

</details>

#### Scenarios.regime

The regime applied to this instance, if any; see `from_profiles()`.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
scenarios.regime  # property -> Regime | None
```

</details>

#### Scenarios.calibration

The object that fits each factor; the per-factor properties (`interest_rates`, `inflation`, ...) reach into it.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
scenarios.calibration  # property -> Calibration
```

</details>

#### Scenarios.correlation_fallback_pairs

The "factor_a/factor_b" pairs the latest calibration set to zero correlation (assumed unrelated) because they
shared too little history. Empty when every pair had enough.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
scenarios.correlation_fallback_pairs  # property -> list[str]
```

</details>

#### Scenarios.last_calibration

The calibration the latest `simulate()` ran on, or None before the first. Save it (`CalibrationResult.save()`) to
replay this fit later without downloading again, or pass it to `simulate(calibration=...)` for another seed or
number of scenarios.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
scenarios.last_calibration  # property -> CalibrationResult | None
```

</details>

#### Scenarios.calibration_failures

The factors the latest calibration could not fit, with the reason (e.g. no mean reversion over a short history).
They are left out of the run rather than stopping it; empty when everything fit.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
scenarios.calibration_failures  # property -> dict[str, str]
```

</details>

#### Scenarios.interest_rates

Fits the interest rate factors.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
scenarios.interest_rates  # property
```

</details>

#### Scenarios.inflation

Fits the inflation factors.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
scenarios.inflation  # property
```

</details>

#### Scenarios.knw

Fits the joint interest rate and inflation model of `method: knw` (opt-in).

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
scenarios.knw  # property
```

</details>

#### Scenarios.knw_sv

Fits the stochastic-volatility version of that model, `method: knw_sv` (opt-in).

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
scenarios.knw_sv  # property
```

</details>

#### Scenarios.cp2022

Reads DNB's CP2022 model and its quarterly parameters, `method: cp2022` (opt-in).

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
scenarios.cp2022  # property
```

</details>

#### Scenarios.equities

Fits the equity factors.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
scenarios.equities  # property
```

</details>

#### Scenarios.unemployment

Fits the unemployment factors.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
scenarios.unemployment  # property
```

</details>

#### Scenarios.term_structure

Fits the Nelson-Siegel yield curve's level, slope and curvature (opt-in).

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
scenarios.term_structure  # property
```

</details>

#### Scenarios.credit_term_structure

Fits the Nelson-Siegel credit-spread curve's level, slope and curvature to a panel of real bonds (opt-in).

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
scenarios.credit_term_structure  # property
```

</details>

#### Scenarios.hjm

Fits the two-factor Gaussian HJM forward-rate curve (opt-in).

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
scenarios.hjm  # property
```

</details>

#### Scenarios.real_estate

Fits the real estate factors (opt-in).

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
scenarios.real_estate  # property
```

</details>

#### Scenarios.credit

Fits the credit spread factors (opt-in).

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
scenarios.credit  # property
```

</details>

#### Scenarios.leading_indicator

Fits the leading indicator factors (opt-in).

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
scenarios.leading_indicator  # property
```

</details>

#### Scenarios.credit_migration

Fits the credit cycle behind rating migrations (opt-in).

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
scenarios.credit_migration  # property
```

</details>

#### Scenarios.fx

Fits the exchange rate factors (opt-in).

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
scenarios.fx  # property
```

</details>

#### Scenarios.commodities

Fits the commodity factors (opt-in).

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
scenarios.commodities  # property
```

</details>

#### Scenarios.dividend_yield

Fits the dividend yield factors (opt-in).

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
scenarios.dividend_yield  # property
```

</details>

#### Scenarios.dividend_growth

Fits the dividend growth factors (opt-in).

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
scenarios.dividend_growth  # property
```

</details>

#### Scenarios.mortality

Fits the mortality (longevity) factors (opt-in).

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
scenarios.mortality  # property
```

</details>

#### Scenarios.dependence

Builds the correlation matrix that links the factors; see `Dependence`.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
scenarios.dependence  # property -> Dependence
```

</details>

#### Scenarios.calibrate

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

#### Scenarios.simulate

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

#### Scenarios.history

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

#### Scenarios.out_of_sample

Go back to a past date, fit and simulate from there with only the data known then, and set the scenarios
against what actually happened.

It is the honest test of a scenario generator: would a model fitted before 2008, COVID or the 2022 inflation
have held them in its cloud? Every series the fit reads ends on `as_of` (a month counts once it has ended;
consumer prices once published, a month later, and unemployment one month later in the US and two elsewhere,
as the statistics offices' release calendars have it), today's snapshots such as option chains raise rather
than leak in, and the run starts from the values known on that date. The sourced values the fit reads besides
the data are taken as of `as_of` from a dated table: a 2007 fit reads the New York Fed's 2007 estimate of the
neutral real rate, the inflation expectations and the equity premium on data to 2007. Where a source has no
vintage that old, its earliest stands in and the note says so: the natural rate of unemployment and its gap
before 2011 come from the 2011 vintages of the Congressional Budget Office and the European Commission, which
estimated those earlier years with later data. `notes` lists each with its source, what was switched off to
keep the fit honest, such as an EIOPA anchor before EIOPA's first curve, and every belief override, a view held
today. Three reads stay today's and are noted: OECD and FRED series as revised today, not as first published,
and the New York Fed's ACM term premium a dollar market path takes out, re-estimated on the whole sample (the
euro and the pound fit their own on the Bundesbank's and the Bank of England's curves up to that date).

Each factor is scored per year ahead: where the realized value fell among the scenarios (its PIT, uniform for
a correct forecast, Diebold, Gunther and Tay (1998, section 3)), whether the 50% and 90% bands held it, and
its CRPS (Gneiting and Raftery (2007, section 4.2)). `Portfolio.backtest` is another thing: it replays one
history through a portfolio, while this forecasts every factor.

**As an example:**

```python
test = scenarios.out_of_sample(
    as_of="2007-12-31", years=5, n_simulations=1000, seed=42, factors=["united_states_unemployment"]
)
test.table.select("date", "realized", "p5", "p50", "p95", "pit")
```

Which returns (on the default profiles, 2026-10-19; three of the five rows):

| date       | realized |    p5 |   p50 |   p95 |   pit |
|:-----------|---------:|------:|------:|------:|------:|
| 2008-12-31 |    0.073 | 0.041 | 0.049 | 0.064 | 0.989 |
| 2009-12-31 |    0.099 | 0.041 | 0.051 | 0.074 | 0.999 |
| 2012-12-31 |    0.079 | 0.043 | 0.058 | 0.090 | 0.872 |

Fitted on data up to 2007, with the Congressional Budget Office's 5.0% natural rate of the time, 1 in 20
scenarios took US unemployment above 7.4% by the end of 2009; it reached 9.9%. `test.plot()` draws it.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
out_of_sample(
    as_of: date | str,
    years: int = 5,
    n_simulations: int | None = None,
    seed: int | None = None,
    factors: list[str] | None = None,
    history_years: float | None = None,
    min_history_years: float = 5.0,
    beliefs: Literal['keep', 'drop'] = 'keep',
) -> OutOfSample
```

**Args:**

- <u>as_of (date &#124; str):</u> the date to go back to, e.g. "2007-12-31"; a month end reads cleanly.
- <u>years (int):</u> the years to simulate and score. Defaults to 5.
- <u>n_simulations (int &#124; None):</u> the number of scenarios. Defaults to None, the profile's.
- <u>seed (int &#124; None):</u> a random seed for a repeatable run. Defaults to None, the profile's.
- <u>factors (list[str] &#124; None):</u> the factors to score. Defaults to None, every one with a realized series.
- <u>history_years (float &#124; None):</u> the fitting window, ending on `as_of`. Defaults to None, as long as the configured one (26 years on the default settings).
- <u>min_history_years (float):</u> the history a factor needs by `as_of`; one with less is left out and noted. Defaults to 5.0.
- <u>beliefs (str):</u> "keep" (default) or "drop" the belief overrides.

**Returns:**

<u>OutOfSample:</u> the scenarios, the realized paths, `table`, `tails`, `scores`, `notes`, and `plot()`.

**Raises:**

- <u>ValueError:</u> without a Toolkit, with a regime, or for a date that is not in the past.

</details>

#### Scenarios.out_of_sample_many

Run `out_of_sample()` from several past dates and score every factor over all of them: are its bands as wide
as they should be, too narrow or too wide, and do its scenarios reach history's worst years as often as
history did?

One origin shows whether a single crisis fit; many show whether the model is calibrated. Per factor:

- coverage of the 50% and 90% bands against 0.5 and 0.9, with exact binomial tests of the coverage
  (Christoffersen (1998, section 3.1)), which reject both too many misses and too few;
- the PITs' mean and spread, and their uniformity tested with Kolmogorov-Smirnov;
- the CRPS (Gneiting and Raftery (2007, section 4.2)) against a no-change forecast;
- the share of scenarios reaching history's lowest and highest year against history's own frequency, flagging
  tails too thin as clearly as too fat.

The rows of one origin share a path, and origins less than a horizon apart share years, so the rows are not
independent. Both tests therefore split each horizon's rows into groups of origins at least that horizon
apart, which are independent under a correct model, and bound the result with Bonferroni over horizons, groups
and bands, as Diebold, Gunther and Tay (1998, p. 880) propose for multi-step forecasts: a model that is right
is flagged in at most 5% of evaluations. Few origins give few rows per group, so the tests flag only a clear
miss; the coverage and PIT spread themselves are the measure. A run starts from its origin's state, so a level
near its record (house prices at the end of 2008) reaches it easily; the tail verdict takes the median over
origins. An origin that cannot run is skipped and listed in `skipped`.

**As an example:**

```python
evaluation = scenarios.out_of_sample_many(
    origins=["2003-12-31", "2007-12-31", "2011-12-31", "2015-12-31", "2019-12-31"],
    years=4,
    n_simulations=1000,
    seed=42,
)
evaluation.scores.select("factor", "coverage_90", "bands", "crps_skill", "tails")
```

Which returns (on the default profiles, 2026-10-19; three of the 27 rows):

| factor                   | coverage_90 | bands      | crps_skill | tails         |
|:-------------------------|------------:|:-----------|-----------:|:--------------|
| united_states_inflation  |       0.850 | ok         |      0.376 | low too fat   |
| united_kingdom_inflation |       0.600 | ok         |      0.405 | high too thin |
| us_broad                 |       0.850 | ok         |      0.542 | ok            |

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
out_of_sample_many(
    origins: list[date | str],
    years: int = 5,
    n_simulations: int | None = None,
    seed: int | None = None,
    factors: list[str] | None = None,
    history_years: float | None = None,
    min_history_years: float = 5.0,
    beliefs: Literal['keep', 'drop'] = 'keep',
) -> OutOfSampleEvaluation
```

**Args:**

- <u>origins (list[date &#124; str]):</u> the dates to go back to, e.g. ["2000-12-31", "2007-12-31", "2019-12-31"].
- <u>years (int):</u> the years each run simulates and is scored over. Defaults to 5.
- <u>n_simulations (int &#124; None):</u> the number of scenarios per origin. Defaults to None, the profile's.
- <u>seed (int &#124; None):</u> the random seed of every origin. Defaults to None, the profile's.
- <u>factors (list[str] &#124; None):</u> the factors to score. Defaults to None, every one.
- <u>history_years (float &#124; None):</u> the fitting window, see `out_of_sample()`. Defaults to None.
- <u>min_history_years (float):</u> see `out_of_sample()`. Defaults to 5.0.
- <u>beliefs (str):</u> "keep" (default) or "drop" the belief overrides.

**Returns:**

<u>OutOfSampleEvaluation:</u> `scores` (one row per factor), `runs` (each origin's `OutOfSample`), `table`, `tails`, `skipped`, and `plot(factor)`.

**Raises:**

- <u>ValueError:</u> without a Toolkit, with a regime, or without origins.

</details>

#### Scenarios.validate

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

#### Scenarios.check_relationships

Does the run behave like an economy? One table of the macro-financial relationships a validator expects, each
measured the same way on decades of history and on every scenario.

The calibration fits each factor on its own history and links them through correlated shocks and a few built-in
drifts, so patterns across factors are not fitted directly: central banks raising rates as inflation rises and
cutting them as unemployment rises (the Taylor (1993) rule and the Federal Reserve's policy-rule benchmarks),
rates near neutral with inflation at the 2% target, the Phillips curve, bear markets with rising unemployment,
the long rate following the short rate, an inverted curve before a downturn, low real equity returns in
high-inflation years, rates slowing house prices, oil passing into inflation and the rate gap moving the
currency. Each is read on year-end values with the same statistic on history (OECD series from the 1950s,
Shiller's US data from 1871) and on each scenario. "fail" means the median scenario has the opposite direction
to history, "warn" the right direction but more than a factor of two off in size. See `Relationships`.

`validate()` asks whether the calibration carried each factor's own history into the run; this asks whether
the factors move together the way the economy does, and needs history beyond the calibration window, so it is
a separate call. A five-year run gives each scenario five yearly observations; simulate 30 years for a sharper
reading.

**As an example:**

On the default profiles (calibrated on 2026-10-19), over 30 years:

```python
result = scenarios.simulate(n_simulations=1000, years=30, seed=42)
scenarios.check_relationships(result)
```

Which returns (3 of the 26 rows, without the other columns):

| relationship                               | region        | status | history | simulated_median |
|:-------------------------------------------|:--------------|:-------|--------:|-----------------:|
| Policy rate reacts to inflation            | United States | warn   |    0.45 |             0.21 |
| Phillips curve                             | United States | pass   |   -0.59 |            -0.32 |
| Bear markets come with rising unemployment | United States | warn   |   -0.41 |            -0.12 |

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
check_relationships(
    result: ScenarioSet,
    regions: list[RelationshipRegion] | None = None,
) -> pl.DataFrame
```

**Args:**

- <u>result (ScenarioSet):</u> the run to check; its step must divide a year.
- <u>regions (list[RelationshipRegion] &#124; None):</u> the economies to check; None takes one per currency of the configured short rates.

**Returns:**

<u>pl.DataFrame:</u> one row per relationship and economy: "relationship", "region", "status" ("pass", "warn" or "fail"), "history", "simulated_median", "simulated_p5", "simulated_p95", "simulated_pooled", "scenarios", "unit", "expected", "measure", "history_source", "history_error" and "detail".

**Raises:**

- <u>ValueError:</u> if the run's step does not divide a year.

</details>

#### Scenarios.check_realism

Does each factor behave as its history did? One table of every factor's range, largest one-year moves,
drawdowns and regime-like stretches, measured the same way on the longest record and on every scenario.

A calibration fits each factor's moves on a few decades of data, and nothing in the fit stops a rate from
wandering below anything a central bank has set, or keeps a calm window's fit from ruling out a 1970s. This
reads every factor at year ends, as `check_relationships` does, against its longest record: OECD series from
the 1950s for rates, inflation and unemployment, Shiller's US home prices since 1890, each equity market's long
index (Shiller's US total return since 1871, Ken French's small caps, European and emerging markets, the
Nikkei 225), the World Bank's Pink Sheet since 1971 for commodities, and exchange rates in real terms. The
statistics cover the lowest and highest level, the largest one-year rise and fall, the worst drawdown from the
previous ten years' high and the longest stretch below one, the longest stretches at the zero lower bound, in a
curve inversion and with inflation above 5%, and states no economy can be in.

The grade compares frequencies on both sides. History is cut into every window as long as the run, and at the
most extreme level it reached in two separate episodes the share of scenarios reaching it is set against the
share of windows that did, within a band for the handful of independent windows behind it: too rarely is a
tail too thin, too often one too fat. Beyond history's worst, where it gives no frequency, at most once in 200
years is allowed, the 99.5% one-year level of Solvency II, European Parliament and Council (2009, Article
101(3)). Any scenario in an impossible state fails. See `Realism`.

**As an example:**

On the default profiles (calibrated on 2026-10-19), over 30 years:

```python
result = scenarios.simulate(n_simulations=1000, years=30, seed=42)
scenarios.check_realism(result)
```

Which returns (3 of the 120 rows, without the other columns):

| factor                  | metric                  | status | history | recurring_level | history_share |
|:------------------------|:------------------------|:-------|--------:|----------------:|--------------:|
| us_broad                | largest one-year fall   | fail   | -0.4178 |         -0.3923 |        0.3840 |
| real_estate             | lowest level            | pass   | -0.1610 |         -0.1337 |        0.1048 |
| united_states_long_rate | longest curve inversion | pass   |       3 |               3 |        0.5312 |

The scenarios reach those levels in 7.3%, 2.1% and 50.5% of cases ("simulated_share").

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
check_realism(
    result: ScenarioSet,
    factors: list[RealismFactor] | None = None,
    summary: bool = False,
) -> pl.DataFrame
```

**Args:**

- <u>result (ScenarioSet):</u> the run to check; its step must divide a year.
- <u>factors (list[RealismFactor] &#124; None):</u> the factors to check; None takes every configured rate, inflation, unemployment, equity, exchange rate, commodity, house-price and credit factor.
- <u>summary (bool):</u> one row per factor, its worst status and the metrics that warn or fail. Defaults to False.

**Returns:**

<u>pl.DataFrame:</u> one row per factor and metric: "factor", "kind", "metric", "status", "envelope_status", "frequency_status", "tail", "history", "secondary_history", "simulated_median", "simulated_extreme", "tolerance", "margin", "beyond_history", "beyond_tolerance", "beyond_margin", "allowed", "recurring_level", "recurring_episodes", "history_share", "share_low", "share_high", "independent_windows", "simulated_share", "nominal_history", "nominal_extreme", "scenarios", "unit", "history_source", "secondary_history_source" and "detail"; with `summary`, "factor", "kind", "status" and "flagged".

**Raises:**

- <u>ValueError:</u> if the run's step does not divide a year.

</details>

#### Scenarios.check_parameters

Are the fitted parameters ones the real world could produce? One table of guardrails on every calibrated
factor, each naming the fit behind it.

A fit can be numerically fine and still describe an economy that never existed: a speed at the bound of its
search, a shock that takes a century to fade, a long-run level outside anything history shows, or an equity
that spends half its time in a crisis regime. This flags, per factor, parameters at a bound of their fit (a
regime at the volatility floor or visited under 2% of the time, a staying probability of 0 or 1, a GARCH or
AR(1) at a unit root, a Hull-White speed at its search bound), half-lives ln(2) / a outside 0.1 to 50 years,
long-run levels outside history's range (a rate read at its EIOPA anchor when it has one), simulated volatility
outside 2/3 to 1.5 times the realised volatility of the history it was fitted on (the release checks' bands),
and an equity's crisis share and expected stays, dt / (1 - p_ii), more than a factor of two from the same
two-regime model, the regime-switching lognormal model of Hardy (2001), fitted on the US market's month-end
total return since 1926 (Ken French). `validate()` grades the run as a whole; this says which factor and which
fit.

**As an example:**

On the default profiles (calibrated on 2026-10-19), over 30 years:

```python
result = scenarios.simulate(n_simulations=1000, years=30, seed=42)
scenarios.check_parameters(result, flagged_only=True)
```

Which returns (3 of the 6 rows, without the other columns):

| factor                | check          | parameter                  | status |  value |
|:----------------------|:---------------|:---------------------------|:-------|-------:|
| eurozone_unemployment | long-run level | long_run_mean              | warn   | 0.0716 |
| eurozone_short_rate   | volatility     | volatility                 | warn   | 1.6674 |
| japan                 | regime share   | stationary_distribution[0] | warn   | 0.4489 |

**References:**

- Hardy, M.R. (2001). "A Regime-Switching Model of Long-Term Stock Returns." North American Actuarial Journal, 5(2), 41-53. <https://doi.org/10.1080/10920277.2001.10595984>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
check_parameters(result: ScenarioSet, flagged_only: bool = False) -> pl.DataFrame
```

**Args:**

- <u>result (ScenarioSet):</u> the run simulated from this instance's latest calibration.
- <u>flagged_only (bool):</u> keep only the guardrails that warn or fail. Defaults to False.

**Returns:**

<u>pl.DataFrame:</u> one row per factor and guardrail: "factor", "check" ("fit bound", "half-life", "long-run level", "volatility", "regime share" or "regime duration"), "parameter", "status", "value", "yardstick", "fit" and "detail".

**Raises:**

- <u>ValueError:</u> if nothing was calibrated yet.

</details>

#### Scenarios.save

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

### ScenarioSet

The result of a simulation: every factor's simulated paths, one row per scenario and one column per date.

Each scenario is one complete, internally consistent future: its inflation, rates, equity returns and currencies
were drawn together, so a scenario with a sell-off carries the rates and spreads that tend to come with one. Read
across scenarios at a date and you get a distribution: its percentiles are the ranges a risk report quotes, and a
portfolio or a liability valued on every scenario inherits the same joint behaviour. `Portfolio` and the Solvency II
functions read it.

Every report reads a factor the same way: a rate as its yearly rate, and anything with a price (equities, FX,
commodities, a portfolio) as its yearly return since the start, both as decimals (0.0441 is 4.41%). `metric_paths`
lists the other readings, such as inflation as a price index or a year-over-year change, and `levels=True` gives the
raw simulated values.

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

result = Scenarios.from_profiles(settings="default", factor_set="default").simulate(n_simulations=100)
result.describe()                                      # one row per factor
result.summary_statistics("united_states_short_rate")  # percentile bands date by date
result.plot("us_broad")                                # a fan chart
result.factors("equities")                             # the factor names in one category
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

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

**Attributes:**

- <u>paths (dict[str, np.ndarray]):</u> factor name -> simulated values, one row per scenario, one column per date.
- <u>time_grid (np.ndarray):</u> each date's distance from the start, in years.
- <u>dates (list[date]):</u> the calendar dates of the run.
- <u>factor_names (list[str]):</u> the simulated factors, in simulation order.
- <u>n_simulations (int):</u> the number of scenarios.
- <u>seed (int &#124; None):</u> the random seed the run was drawn with.
- <u>calibration_metadata (dict[str, Any]):</u> factor name -> the fitted parameters it was simulated with.
- <u>antithetic (bool):</u> whether every scenario has a mirror image with the opposite shocks, which pins down averages more precisely for the same number of scenarios.
- <u>factor_categories (dict[str, str]):</u> factor name -> its category, e.g. "equities" or "inflation".
- <u>factor_labels (dict[str, FactorLabel]):</u> factor name -> its display name for charts and tables.
- <u>return_paths (dict[str, np.ndarray]):</u> a portfolio holding's own growth, before rebalancing flows, which its returns are read from.

</details>

#### ScenarioSet.n_steps

The number of time steps in the run, one fewer than its dates: 60 for five years of monthly steps.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
scenarioset.n_steps  # property -> int
```

</details>

#### ScenarioSet.label

A factor's display name (see `FactorLabel`), or a tidied version of its name when the run carries none.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
label(factor: str) -> FactorLabel
```

</details>

#### ScenarioSet.is_level_factor

Whether a factor is simulated as a level (a price, a portfolio value or the leading indicator) rather than as a
rate. See `factor_kind`.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
is_level_factor(factor: str) -> bool
```

</details>

#### ScenarioSet.factor_kind

What a factor's simulated values are, which decides how each `metric` reads it.

- "price": a price or value (equities, FX, commodities, a dividend index, a portfolio). Changes are percentages.
- "growth": the growth rate of a price index (inflation, real estate). Its level is the index it compounds into.
- "rate": a rate or spread (interest rates, the yield-curve factors, credit spreads, unemployment, dividend yield,
  mortality). Changes are differences in the rate's own units.
- "index": an index with no rate reading (the OECD composite leading indicator). Changes are percentages.

A factor without a category, as in a hand-built run, counts as a "rate".

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
factor_kind(factor: str) -> FactorKind
```

**Args:**

- <u>factor (str):</u> the factor name.

**Returns:**

<u>str:</u> "price", "growth", "rate" or "index".

</details>

#### ScenarioSet.resolve_metric

The reading `metric_paths` gives for these arguments: "native" for `levels=True`, the factor's default when
`metric` is None, otherwise `metric` itself once checked.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
resolve_metric(factor: str, levels: bool = False, metric: Metric | None = None) -> str
```

**Args:**

- <u>factor (str):</u> the factor name.
- <u>levels (bool):</u> ask for the raw simulated values. Defaults to False.
- <u>metric (str &#124; None):</u> the reading asked for (see `metric_paths`). Defaults to None.

**Returns:**

<u>str:</u> the reading, e.g. "rate", "annualized" or "native".

**Raises:**

- <u>ValueError:</u> if `levels=True` is combined with a `metric`, the metric is unknown, or it has no meaning for the factor (a "rate" of a price, an "annualized" return of a rate).

</details>

#### ScenarioSet.metric_paths

One factor's paths the way every summary, table and chart reads them.

`metric` picks how a number is expressed: the same simulated inflation can be its yearly rate (3.4%), a price
index that starts at 100, or that index's change over one step, one year or since today. By default a rate reads
as itself and a price as its yearly return since the start: a 769 -> 1,209 equity path over five years reads as
9.5% a year. That is A(t) below, with S the price and t the years since the start. A growth rate r's `level`
compounds it into the index I(t), summing over the steps before t.

The formula is as follows:
- A(t) = (S(t) / S(0))^(1 / t) - 1
- I(t) = 100 * exp(sum(ln(1 + r(s)) * dt)), so a constant r gives 100 * (1 + r)^t

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

**As an example:**

```python
result.metric_paths("united_states_inflation", metric="level")
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
metric_paths(factor: str, levels: bool = False, metric: Metric | None = None) -> np.ndarray
```

**Args:**

- <u>factor (str):</u> the factor name.
- <u>levels (bool):</u> the raw simulated values instead; not combined with `metric`. Defaults to False.
- <u>metric (str &#124; None):</u> a reading from the table; None keeps the factor's default.

**Returns:**

<u>np.ndarray:</u> one row per scenario, one column per date; NaN where there is no value yet.

**Raises:**

- <u>KeyError:</u> if the run has no such factor.
- <u>ValueError:</u> if the metric does not apply to the factor, or for `yoy` on a step that does not divide a year.

</details>

#### ScenarioSet.metric_applies

Whether `metric` has a reading for `factor` (None always does); multi-factor reports fall back to the
factor's default where it has none, e.g. `describe(metric="annualized")` keeps rates as rates.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
metric_applies(factor: str, metric: Metric | None) -> bool
```

</details>

#### ScenarioSet.metric_description

A few words naming the reading for a chart subtitle, or None when the value is the factor itself.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
metric_description(factor: str, levels: bool = False, metric: Metric | None = None) -> str | None
```

</details>

#### ScenarioSet.to_dataframe

One factor's paths as a Polars table, one row per scenario and one column per date.

Values are read the way every report reads them (see `metric_paths`): a rate as itself, a price as its yearly
return since the start, which is empty on the first date.

**As an example:**

```python
result.to_dataframe("united_states_short_rate")
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
to_dataframe(factor: str, levels: bool = False, metric: Metric | None = None) -> pl.DataFrame
```

**Args:**

- <u>factor (str):</u> the factor name.
- <u>levels (bool):</u> give the raw simulated values (prices) instead. Defaults to False.
- <u>metric (str &#124; None):</u> the reading, "rate", "level", "change", "yoy", "cumulative" or "annualized" (see `metric_paths`). Defaults to None, the factor's default.

**Returns:**

<u>pl.DataFrame:</u> a "scenario" column plus one column per date ("YYYY-MM-DD").

**Raises:**

- <u>KeyError:</u> if the run has no such factor.

</details>

#### ScenarioSet.discount_factor_paths

`discount_factors()` as a plain array, one row per scenario and 1 at the start: the discount factors the Solvency
II functions use.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
discount_factor_paths(factor: str) -> np.ndarray
```

</details>

#### ScenarioSet.discount_factors

What 1 paid at each date is worth today, scenario by scenario, treating one factor as the short rate.

This turns a simulated short rate into a discount curve per scenario, the way money in a bank account grows at
that rate. It is usually applied to an interest rate factor, but works on any rate. The discount factor is
DF(t) = exp(-sum of rate x time step up to t), so it is 1 at the start.

It discounts a known cash flow correctly. Pricing an uncertain payoff under these real-world scenarios needs an
extra adjustment for the market price of risk, which this package does not compute (see the reference).

**As an example:**

```python
result.discount_factors("united_states_short_rate")
```

**References:**

- Cheng, P.-K., Planchet, F. (2019). "Stochastic Deflator for an Economic Scenario Generator with Five Factors." Bankers, Markets & Investors, 157. <https://www.journaleska.com/index.php/bmi/article/view/9378>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
discount_factors(factor: str) -> pl.DataFrame
```

**Args:**

- <u>factor (str):</u> the rate factor to discount with, e.g. "united_states_short_rate".

**Returns:**

<u>pl.DataFrame:</u> a "scenario" column plus one discount-factor column per date.

**Raises:**

- <u>KeyError:</u> if the run has no such factor.
- <u>ValueError:</u> if the factor is a price or index rather than a rate.

</details>

#### ScenarioSet.cumulative_index

Compound a rate factor into an index, such as inflation into a price index that starts at 100.

Use it for factors simulated as a growth rate, such as inflation or real estate. Prices such as equities or FX
already are an index and don't need it. A growth rate is a year-over-year rate, the growth of the index over a
year, so the index is initial_index x exp(sum of ln(1 + rate) x time step up to t): inflation held at 3% gives
1.03^T, as the log change of the price index Ahlgrim, D'Arcy and Gorvett (2005, section 3, eq. 3.7) model
does. Any other rate compounds continuously, initial_index x exp(sum of rate x time step up to t).

**As an example:**

```python
result.cumulative_index("united_states_inflation")
```

**References:**

- Ahlgrim, K.C., D'Arcy, S.P., Gorvett, R.W. (2005). "Modeling Financial Scenarios: A Framework for the Actuarial Profession." Proceedings of the Casualty Actuarial Society, 92. Section 3, eq. 3.7. <https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
cumulative_index(factor: str, initial_index: float = 100.0) -> pl.DataFrame
```

**Args:**

- <u>factor (str):</u> the rate factor to compound, e.g. "united_states_inflation".
- <u>initial_index (float):</u> the index level at the start. Defaults to 100.0.

**Returns:**

<u>pl.DataFrame:</u> a "scenario" column plus one index-level column per date.

**Raises:**

- <u>KeyError:</u> if the run has no such factor.
- <u>ValueError:</u> if the factor is a price or index rather than a rate, or `initial_index` is not a positive number.

</details>

#### ScenarioSet.diagnose

Check that a factor's scenarios end up where its fitted model says they should settle in the long run.

On a long horizon the long-run level is what drives the answer: a liability discounted at rates that settle at
3% is worth something very different from one discounted at 4%. Interest rates, inflation, unemployment, real
estate, credit spreads, the leading indicator and the yield-curve factors are usually fitted as mean-reverting
(an Ornstein-Uhlenbeck process): pulled back toward a long-run level, with a known long-run mean and spread.
This compares the last date's simulated mean and standard deviation with them. Equities and FX have no such
long-run level and are skipped. Below are the long-run mean, the spread (the third line for a CIR process) and
the noise floor e, with kappa the mean-reversion speed, theta the long-run mean, sigma the volatility and n the
number of scenarios.

The formula is as follows:
- mu_x = theta
- sigma_x = sigma / sqrt(2 * kappa)
- sigma_x = sigma * sqrt(theta / (2 * kappa))
- e = 3 * sigma_x / sqrt(n)

A `within_tolerance=False` is not always a fault, and `reason` says which case it is: the mean is off by more than
the tolerance and `mean_noise_floor` e (3 standard errors of the simulated mean, the gap sampling noise alone
explains), the spread is off, or both. It adds "slow to settle" when the horizon spans fewer than three time
constants (1 / kappa, about four half-lives): such a factor has not reached its long-run level
yet, so a gap is expected. `unit` is "log" for a factor fitted on the logarithm of its value (credit spreads,
commodities, dividend yield), whose numbers are then in log space, and "level" otherwise.

**As an example:**

```python
result.diagnose("united_states_short_rate")
result.diagnose().filter(~pl.col("within_tolerance"))  # every factor off, with its reason
```

**References:**

- Vasicek, O. (1977). "An Equilibrium Characterization of the Term Structure." Journal of Financial Economics, 5(2), 177-188. <https://doi.org/10.1016/0304-405X(77>)90016-2
- Cox, J.C., Ingersoll, J.E., Ross, S.A. (1985). "A Theory of the Term Structure of Interest Rates." Econometrica, 53(2), 385-407. <https://doi.org/10.2307/1911242>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
diagnose(factor: str | None = None, tolerance: float = 0.2) -> 'FactorDiagnostics | pl.DataFrame'
```

**Args:**

- <u>factor (str &#124; None):</u> the factor to check. Defaults to None, every factor this applies to.
- <u>tolerance (float):</u> how far the simulated mean and standard deviation may be from the long-run values, as a share of them. Defaults to 0.2.

**Returns:**

<u>FactorDiagnostics &#124; pl.DataFrame:</u> for one factor, a `FactorDiagnostics` with the means, spreads, mean gap, noise floor, `within_tolerance`, `unit` and `reason`; without one, a table with "factor", "simulated_mean", "theoretical_mean", "simulated_std", "theoretical_std", "within_tolerance", "unit" and "reason", one row per factor.

**Raises:**

- <u>KeyError:</u> if the run has no such factor, or no fitted parameters for it.
- <u>NotOUCalibratedError:</u> if the factor is not mean-reverting, such as equities or FX (a ValueError).

</details>

#### ScenarioSet.plot

One quick chart of this run: a fan chart, the individual paths, or where a factor lands at the end.

Rates and returns share one percentage axis (see `metric_paths`); `levels=True` draws prices and portfolio values
in money instead. Without a factor it draws a computed portfolio's value when the run holds one, and otherwise a
grid with one fan chart per factor. The `plot_*` methods give finer control over bands, bins and path counts.

**As an example:**

```python
result.plot("us_broad")                                 # one factor's percentile fan
result.plot("us_broad", kind="distribution")            # where it lands at the horizon
result.plot("united_states_inflation", metric="level")  # inflation as a price index
values.plot(kind="sleeves")                             # a Portfolio.compute() result's holdings
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
plot(
    factors: str | Sequence[str] | None = None,
    kind: Literal['fan', 'paths', 'distribution', 'sleeves'] = 'fan',
    levels: bool = False,
    ax: 'Axes | None' = None,
    metric: Metric | None = None,
) -> 'Figure'
```

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

</details>

#### ScenarioSet.plot_fan_chart

One factor's fan chart: the median path with shaded bands, by default for the middle 50% and 90% of scenarios.
The same chart as `plot_fan_chart(result, factor)`.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
plot_fan_chart(
    factor: str,
    quantile_bands: Sequence[tuple[float, float]] = ((0.05, 0.95), (0.25, 0.75)),
    ax: 'Axes | None' = None,
    levels: bool = False,
    metric: Metric | None = None,
) -> 'Figure'
```

**Args:**

- <u>factor (str):</u> the factor to draw.
- <u>quantile_bands (Sequence[tuple[float, float]]):</u> (lower, upper) quantile pairs, outermost first. Defaults to ((0.05, 0.95), (0.25, 0.75)).
- <u>ax (Axes &#124; None):</u> an existing matplotlib Axes to draw into. Defaults to None, a new figure.
- <u>levels (bool):</u> draw a price's level instead of its yearly return since the start. Defaults to False.
- <u>metric (str &#124; None):</u> the reading (see `metric_paths`). Defaults to None, the factor's default.

**Returns:**

<u>matplotlib.figure.Figure:</u> the figure holding the chart.

</details>

#### ScenarioSet.plot_paths

Every simulated path of one factor (or a random sample of them), with the median on top. The same chart as
`plot_paths(result, factor)`.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

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

**Args:**

- <u>factor (str):</u> the factor to draw.
- <u>n_paths (int &#124; None):</u> how many paths to draw, picked at random. Defaults to None, every path.
- <u>seed (int &#124; None):</u> the random seed for that pick. Defaults to None.
- <u>ax (Axes &#124; None):</u> an existing matplotlib Axes to draw into. Defaults to None, a new figure.
- <u>levels (bool):</u> draw a price's level instead of its yearly return since the start. Defaults to False.
- <u>metric (str &#124; None):</u> the reading (see `metric_paths`). Defaults to None, the factor's default.

**Returns:**

<u>matplotlib.figure.Figure:</u> the figure holding the chart.

</details>

#### ScenarioSet.plot_terminal_distribution

A histogram of where one factor ends up at the horizon, with percentiles marked. The same chart as
`plot_terminal_distribution(result, factor)`.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

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

**Args:**

- <u>factor (str):</u> the factor to draw.
- <u>bins (int &#124; None):</u> the number of bars. Defaults to None, scaled to the number of scenarios.
- <u>quantiles (Sequence[float]):</u> the quantiles to mark. Defaults to (0.05, 0.5, 0.95).
- <u>ax (Axes &#124; None):</u> an existing matplotlib Axes to draw into. Defaults to None, a new figure.
- <u>levels (bool):</u> show a price's final level instead of its yearly return. Defaults to False.
- <u>metric (str &#124; None):</u> the reading (see `metric_paths`). Defaults to None, the factor's default.

**Returns:**

<u>matplotlib.figure.Figure:</u> the figure holding the chart.

</details>

#### ScenarioSet.plot_factors

A grid with one fan chart per factor, each on its own scale. The same chart as `plot_factors(result)`.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
plot_factors(
    factors: Sequence[str] | None = None,
    n_columns: int = 3,
    quantile_bands: Sequence[tuple[float, float]] = ((0.05, 0.95), (0.25, 0.75)),
    levels: bool = False,
    metric: Metric | None = None,
) -> 'Figure'
```

**Args:**

- <u>factors (Sequence[str] &#124; None):</u> the factors to draw. Defaults to None, every factor.
- <u>n_columns (int):</u> panels per row. Defaults to 3.
- <u>quantile_bands (Sequence[tuple[float, float]]):</u> the bands each panel shades. Defaults to ((0.05, 0.95), (0.25, 0.75)).
- <u>levels (bool):</u> draw prices as levels instead of yearly returns since the start. Defaults to False.
- <u>metric (str &#124; None):</u> the reading (see `metric_paths`). Defaults to None, each factor's default.

**Returns:**

<u>matplotlib.figure.Figure:</u> the figure holding the grid.

</details>

#### ScenarioSet.filter

Keep only the scenarios where one factor sits within a chosen range, such as the 30% with the highest interest
rates.

Each scenario i is ranked by a statistic s(i) over the chosen steps a to b: a rate x's average (first line), or
a price S's yearly log return (second line). The scenarios whose s(i) lies between the lower and upper quantile
Q of s across scenarios are kept.

The formula is as follows:
- s(i) = (x(i, a) + ... + x(i, b)) / (b - a + 1)
- s(i) = ln(S(i, b) / S(i, a)) / (t(b) - t(a))
- Q(lower) <= s(i) <= Q(upper)

A kept scenario keeps every other factor's path too, so a high-rate scenario brings its own correlated inflation
and equity paths along: a stress scenario built from the simulation instead of by hand. Fewer than 30 kept
scenarios log a warning, since percentiles mean little on so few.

**As an example:**

```python
high_rates = result.filter("united_states_short_rate", (0.7, 1.0))
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
filter(
    factor: str,
    quantile_range: tuple[float, float],
    step_range: tuple[int, int] | None = None,
) -> 'ScenarioSet'
```

**Args:**

- <u>factor (str):</u> the factor to rank scenarios by.
- <u>quantile_range (tuple[float, float]):</u> the (lower, upper) quantiles to keep, in [0, 1]; (0.7, 1.0) keeps the top 30%.
- <u>step_range (tuple[int, int] &#124; None):</u> the (start, stop) steps to rank over, like a Python slice. Defaults to None, the whole path.

**Returns:**

<u>ScenarioSet:</u> the same run with only the kept scenarios.

**Raises:**

- <u>KeyError:</u> if the run has no such factor.
- <u>ValueError:</u> if the quantile or step range is invalid, or no scenario falls within it.

</details>

#### ScenarioSet.filter_narrative

Keep only the scenarios that fit a story told through several factors at once, such as stagflation: high
inflation and weak equities.

Each target is a (lower, upper) quantile range for one factor, as in `filter`. The result is a stress scenario
drawn from the simulation itself rather than one hand-picked path, with every factor's path kept.

**As an example:**

```python
stagflation = result.filter_narrative({"united_states_inflation": (0.8, 1.0), "us_broad": (0.0, 0.2)})
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
filter_narrative(
    targets: dict[str, tuple[float, float]],
    step_range: tuple[int, int] | None = None,
    mode: Literal['sequential', 'joint'] = 'sequential',
) -> 'ScenarioSet'
```

**Args:**

- <u>targets (dict[str, tuple[float, float]]):</u> factor name -> the (lower, upper) quantile range to keep.
- <u>step_range (tuple[int, int] &#124; None):</u> the (start, stop) steps every target ranks over. Defaults to None, the whole path.
- <u>mode (str):</u> "sequential" (default) applies each target to what the previous ones left, so (0.7, 1.0) on rates then (0.0, 0.3) on equities keeps about 9%; "joint" ranks every target against the full run and keeps the overlap, which can be much smaller.

**Returns:**

<u>ScenarioSet:</u> the scenarios that meet every target.

**Raises:**

- <u>KeyError:</u> if a target factor is not in the run.
- <u>ValueError:</u> if a quantile range or `mode` is invalid, or no scenario meets every target.

</details>

#### ScenarioSet.rescale_scenario_cloud

Shift and widen (or narrow) one factor's simulated scenarios without simulating again.

Use it when a view is easiest to state about the whole distribution, such as "inflation half a point higher and
more uncertain", rather than as a change to one fitted parameter before simulating (a belief override). At
every date, each scenario becomes (mean + mean_shift) + spread_multiplier x (value - mean), with mean that date's
average across scenarios. The shape of the distribution and every other factor stay as they are.

**As an example:**

```python
result.rescale_scenario_cloud("united_states_inflation", mean_shift=0.005, spread_multiplier=1.5)
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
rescale_scenario_cloud(
    factor: str,
    mean_shift: float = 0.0,
    spread_multiplier: float = 1.0,
) -> 'ScenarioSet'
```

**Args:**

- <u>factor (str):</u> the factor to rescale.
- <u>mean_shift (float):</u> the amount added to the factor's average at every date, in its simulated units. Defaults to 0.0.
- <u>spread_multiplier (float):</u> widens (above 1) or narrows (below 1) the spread around that average; must be above 0. Defaults to 1.0.

**Returns:**

<u>ScenarioSet:</u> the same run with this factor's paths replaced.

**Raises:**

- <u>KeyError:</u> if the run has no such factor.
- <u>ValueError:</u> if `mean_shift` is not finite or `spread_multiplier` is not above 0.

</details>

#### ScenarioSet.summary_statistics

Percentile bands for one factor, date by date: its mean, spread and chosen percentiles across every scenario.

This is the table behind a fan chart: the 5% and 95% columns are the band 9 in 10 scenarios stay within at each
date. `se` is the standard error of the mean, how precisely this many scenarios pin down `mean`; when it is too
large for the use at hand, simulate more scenarios. With antithetic sampling it is measured on the n / 2 pair
averages m(i) = (x(i) + x(i + n / 2)) / 2, which are independent where the mirrored paths are not, so it reflects
the precision they buy. With sigma(t) the spread across the n scenarios on date t and sigma_m(t) that of the
pair averages, the first line is a plain run and the second an antithetic one.

The formula is as follows:
- se(t) = sigma(t) / sqrt(n)
- se(t) = sigma_m(t) / sqrt(n / 2)

**As an example:**

```python
result = Scenarios.from_profiles(api_key="FINANCIAL_MODELING_PREP_KEY").simulate(n_simulations=2000)
result.summary_statistics("united_states_short_rate")
```

Which returns (the last three months of the five-year run, `se` left out):

| date       |   mean |    std |  q0.05 |  q0.25 |   q0.5 |  q0.75 |  q0.95 |
|:-----------|-------:|-------:|-------:|-------:|-------:|-------:|-------:|
| 2030-11-01 | 0.0459 | 0.0341 | 0.0000 | 0.0204 | 0.0437 | 0.0650 | 0.1095 |
| 2030-12-02 | 0.0458 | 0.0343 | 0.0000 | 0.0198 | 0.0435 | 0.0651 | 0.1089 |
| 2031-01-01 | 0.0459 | 0.0345 | 0.0000 | 0.0196 | 0.0439 | 0.0659 | 0.1099 |

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
summary_statistics(
    factor: str,
    quantiles: list[float] | None = None,
    levels: bool = False,
    metric: Metric | None = None,
) -> pl.DataFrame
```

**Args:**

- <u>factor (str):</u> the factor name.
- <u>quantiles (list[float] &#124; None):</u> the quantiles to report. Defaults to None, which gives 0.05, 0.25, 0.5, 0.75 and 0.95.
- <u>levels (bool):</u> summarize the raw simulated values (prices) instead. Defaults to False.
- <u>metric (str &#124; None):</u> the reading (see `metric_paths`). Defaults to None, the factor's default.

**Returns:**

<u>pl.DataFrame:</u> "date", "mean", "std", "se" and one "q<quantile>" column per quantile; a price's first row is empty, since a return starts after the first date.

**Raises:**

- <u>KeyError:</u> if the run has no such factor.

</details>

#### ScenarioSet.factors

The factor names in this run, optionally only those of one category.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
factors(category: str | None = None) -> list[str]
```

**Args:**

- <u>category (str &#124; None):</u> a category such as "equities" or "interest_rates". Defaults to None, every factor.

**Returns:**

<u>list[str]:</u> the matching factor names, in simulation order.

**Raises:**

- <u>ValueError:</u> if the category is not in the run but close to one that is ("equity" for "equities").

</details>

#### ScenarioSet.describe

One row per factor: where it starts and where its scenarios end up. The first table to read after a simulation.

Every value is a decimal in one unit (see `metric_paths`): a rate as its yearly rate, a price as its yearly return
since the start. So "initial" is empty for a price, and its terminal columns are the yearly return over the whole
horizon. `terminal_mean` is the central expectation, and `terminal_q05` and `terminal_q95` are what 1 in 20
scenarios end below and above: the 90% range a risk report would quote. In the table below, US equities return
9.8% a year on average over five years, but 1 in 20 scenarios lose 4.7% a year; inflation starts at 3.4% and
averages 2.8% by the horizon, with about 1 in 20 scenarios in deflation.

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
| united_states_inflation  | inflation      |  0.0374 |        0.0234 |      -0.0064 |       0.0770 |
| united_states_short_rate | interest_rates |  0.0408 |        0.0459 |       0.0000 |       0.1099 |
| us_broad                 | equities       |         |        0.0849 |      -0.0569 |       0.2082 |

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
describe(levels: bool = False, metric: Metric | None = None) -> pl.DataFrame
```

**Args:**

- <u>levels (bool):</u> report the raw simulated values (prices) instead. Defaults to False.
- <u>metric (str &#124; None):</u> the reading (see `metric_paths`). Defaults to None, each factor's default, which a factor the metric has no reading for also keeps.

**Returns:**

<u>pl.DataFrame:</u> "factor", "label", "category", "metric", "initial", "terminal_mean", "terminal_q05" and "terminal_q95".

</details>

#### ScenarioSet.step_at

The step closest to a number of years from the start, e.g. `step_at(10)` is step 120 of a monthly run.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
step_at(years: float) -> int
```

**Args:**

- <u>years (float):</u> years from the start.

**Returns:**

<u>int:</u> the step index.

**Raises:**

- <u>ValueError:</u> if `years` lies outside the simulated horizon.

</details>

#### ScenarioSet.select

The same run with only some factors, in the run's own order; categories, labels and fitted parameters follow.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
select(factors: Sequence[str]) -> 'ScenarioSet'
```

**Args:**

- <u>factors (Sequence[str]):</u> the factors to keep.

**Returns:**

<u>ScenarioSet:</u> the narrowed run.

**Raises:**

- <u>KeyError:</u> if a factor is not in this run.

</details>

#### ScenarioSet.sample

A random subset of `n` scenarios, each kept whole across every factor so their correlation survives. Handy for a
quick look, a lighter export, or checking how stable a statistic is.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
sample(n: int, seed: int | None = None) -> 'ScenarioSet'
```

**Args:**

- <u>n (int):</u> how many scenarios to keep, between 1 and `n_simulations`.
- <u>seed (int &#124; None):</u> the random seed, for a repeatable draw. Defaults to None.

**Returns:**

<u>ScenarioSet:</u> the sampled run.

**Raises:**

- <u>ValueError:</u> if `n` is not between 1 and `n_simulations`.

</details>

#### ScenarioSet.horizon_summary

Percentiles of every factor at chosen horizons, one row per factor and horizon: where each factor is in 1, 5 and
10 years.

This is the term structure of risk. For a mean-reverting factor such as a rate the band widens at first and then
levels off as the pull back to the long-run level takes hold; for an equity's yearly return it narrows with the
horizon, since good and bad years average out.

**As an example:**

```python
result.horizon_summary([1, 3, 5])
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
horizon_summary(
    horizons: Sequence[float],
    factors: Sequence[str] | None = None,
    quantiles: Sequence[float] = (0.05, 0.25, 0.5, 0.75, 0.95),
    levels: bool = False,
    metric: Metric | None = None,
) -> pl.DataFrame
```

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

</details>

#### ScenarioSet.to_long

Every path in one long table, one row per factor, scenario and date: the shape databases, plotting libraries and
group-by pipelines expect.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
to_long(
    factors: Sequence[str] | None = None,
    levels: bool = False,
    metric: Metric | None = None,
) -> pl.DataFrame
```

**Args:**

- <u>factors (Sequence[str] &#124; None):</u> the factors to include. Defaults to None, every factor.
- <u>levels (bool):</u> give the raw simulated values (prices) instead. Defaults to False.
- <u>metric (str &#124; None):</u> the reading (see `metric_paths`). Defaults to None, each factor's default.

**Returns:**

<u>pl.DataFrame:</u> "factor", "scenario", "date", "time" (years from the start) and "value".

</details>

#### ScenarioSet.simulated_correlation

How the simulated factors move together, step by step, pooled over every scenario.

Use it to check that a run reproduces the correlations it was calibrated with, next to
`CalibrationResult.correlation_frame()`. Prices are measured by their log returns and every other factor by its
change, the same way calibration measures them.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
simulated_correlation(
    factors: Sequence[str] | None = None,
    step_range: tuple[int, int] | None = None,
) -> pl.DataFrame
```

**Args:**

- <u>factors (Sequence[str] &#124; None):</u> the factors to include. Defaults to None, every factor.
- <u>step_range (tuple[int, int] &#124; None):</u> the (start, stop) dates to measure over. Defaults to None, the whole path.

**Returns:**

<u>pl.DataFrame:</u> a "factor" column plus one column per factor; a factor that never moves correlates as empty.

**Raises:**

- <u>KeyError:</u> if a factor is not in this run.
- <u>ValueError:</u> if `step_range` leaves fewer than two dates.

</details>

#### ScenarioSet.validate

Not available on a run: check one with `scenarios.validate(result)`, which also needs its calibration.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
ScenarioSet.validate(*args: Any, **kwargs: Any) -> Any
```

</details>

### CalibrationResult

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
    calibrated_params: dict[str, CreditCycleParams | OUParams | RegimeParams | UnemploymentParams | YieldCurveParams | FXPPPParams | FXParams | CommodityParams | CommodityRandomWalkParams | DividendYieldParams | DividendGrowthParams | WilkieConsolsParams | EquityDerivedParams | RandomWalkParams | GARCHParams | OUCovariateParams | DeterministicParams | BreakevenInflationParams | InflationRegimeParams | DeterministicPathParams | HullWhiteForwardParams | AR1Params | MovingTargetOUParams | KnwParams | KnwSvLegParams | KnwSvEquityParams | Cp2022EntryParams | HjmFactorParams | HestonParams | PolicyRuleParams | TermPremiumParams | RateLinkedOUParams | RegimeOUParams]
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
    calibration_notes: dict[str, str] = Field(default_factory=dict, description="factor name -> how its fit departs from its config while it still runs, e.g. an equity with expected_return 'risk_free_plus_premium' that kept its own average return because its short rate failed, or an expectations long rate whose expected path reverts at its policy-rule short rate's own speed on history.")
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
- <u>calibration_notes (dict[str, str]):</u> factor name -> how its fit departs from its config, e.g. an equity that kept its own average return because its short rate failed to calibrate, or a long rate whose expected path reverts at its policy-rule short rate's own speed on history rather than the rule's.

</details>

#### CalibrationResult.describe

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

#### CalibrationResult.correlation_frame

The calibrated correlation matrix as a labelled table: a "factor" column plus one column per factor. Set it next
to `ScenarioSet.simulated_correlation()` to check that a run reproduces the correlations it was calibrated with.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
correlation_frame() -> pl.DataFrame
```

</details>

#### CalibrationResult.plot

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

#### CalibrationResult.plot_correlation_matrix

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

#### CalibrationResult.save

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

#### CalibrationResult.load

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

### FactorLabel

A factor's display name in two parts: a headline and the line under it.

Charts and `describe()` tables show "Inflation — United States" or "US Broad — Equity" instead of the raw factor
name ("united_states_inflation", "us_broad"). Every simulated run carries one label per factor, taken from the
factor set.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
class FactorLabel(BaseModel):
    title: str
    qualifier: str | None = None
```

**Attributes:**

- <u>title (str):</u> the headline, e.g. "Inflation" or "US Broad".
- <u>qualifier (str &#124; None):</u> the second layer, e.g. "United States" or "Equity"; None for no second layer.

</details>

### compare_runs

Put several runs side by side on one statistic of where each factor ends up, such as a baseline against a stress
regime.

The average tells only half of a stress test: a regime can leave the mean of a factor almost where it was while
making its bad outcomes much worse. `quantiles` adds that tail next to each run's column, such as `quantiles=(0.05,)`
for the level 1 in 20 scenarios end below. Each quantile column reads exactly like `describe()`'s `terminal_q05`:
the same metric and units as the run's own column, on the last date.

**As an example:**

With `result` a baseline of 2,000 scenarios on the default profiles:

```python
from financescenarios import Scenarios, compare_runs

oil_crisis = Scenarios.from_profiles(regime="oil_crisis", api_key="FINANCIAL_MODELING_PREP_KEY")
shocked = oil_crisis.simulate(n_simulations=2000)

compare_runs({"baseline": result, "oil_crisis": shocked})
compare_runs({"baseline": result, "oil_crisis": shocked}, quantiles=(0.05,))  # adds baseline_q05, oil_crisis_q05
```

Which returns, for the first call (4 of the factors):

| factor                   | baseline | oil_crisis |
|:-------------------------|---------:|-----------:|
| united_states_inflation  |   0.0234 |     0.0592 |
| united_states_short_rate |   0.0459 |     0.1153 |
| united_states_long_rate  |   0.0579 |     0.1275 |
| us_broad                 |   0.0849 |    -0.0126 |

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

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

</details>

### build_toolkit

Build the Finance Toolkit a `Scenarios` run fetches its data with, covering every ticker the configured factors
need.

The start and end dates and the benchmark come from the config's `toolkit` section. Nothing is downloaded yet: data
is fetched when a factor is fitted, and served from the Finance Toolkit's local cache whenever it already holds it.
An API key left out is read from the environment, or from a `.env` file in the folder Python runs in.

**As an example:**

```python
from financescenarios import build_toolkit, load_profiles

toolkit = build_toolkit(load_profiles(settings_id="default", factor_set_id="default"))
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

### set_display

Make Polars print this package's tables in full, in a notebook or a terminal, with one call.

Polars, the table library every result here comes as, shortens what it prints: about 30 characters of text per
cell, 10 rows and 8 columns. That cuts off the "detail" and "meaning" of `scenarios.validate(result)`, the factors
of a long `describe()` and the quantile columns of `compare_runs`. This sets the table width, the text length per
cell, and the rows and columns shown, so those tables print whole; long text wraps within its cell instead. It only
changes how tables are shown, never their values, and lasts for the session. `decimals=4` also rounds how floats
print, so 0.051953 reads 0.0520. `reset=True` hands these options back to Polars' own defaults.

**As an example:**

```python
from financescenarios import set_display

set_display()                    # validate(), describe() and compare_runs() print in full
set_display(width=120, rows=30)  # narrower, fewer rows
set_display(decimals=4)          # floats as 0.0520 instead of 0.051953
set_display(reset=True)          # back to Polars' defaults
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
set_display(
    width: int = 200,
    text: int = 1000,
    rows: int = 100,
    columns: int = 20,
    reset: bool = False,
    decimals: int | None = None,
) -> None
```

**Args:**

- <u>width (int):</u> the widest a printed table may be, in characters; -1 for no limit. Defaults to 200.
- <u>text (int):</u> the most characters of text shown per cell. Defaults to 1000.
- <u>rows (int):</u> the most rows shown before the middle is cut; -1 for every row. Defaults to 100.
- <u>columns (int):</u> the most columns shown before the middle is cut; -1 for every column. Defaults to 20.
- <u>reset (bool):</u> restore Polars' defaults instead, ignoring the other arguments. Defaults to False.
- <u>decimals (int &#124; None):</u> the decimals shown per float; None leaves Polars' setting as it is. Defaults to None.

**Raises:**

- <u>ValueError:</u> if an argument is not a whole number, `text` or `decimals` is below its minimum, or `width` is 0.

</details>

### set_log_level

Set how much Finance Scenarios, and the Finance Toolkit underneath, prints while it works.

"INFO" (the default) shows every calibration, data fetch and simulation step with how long it took, "WARNING" only
what needs a look, and "ERROR" next to nothing.

**As an example:**

```python
from financescenarios import set_log_level

set_log_level("WARNING")
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
set_log_level(level: int | str) -> None
```

**Args:**

- <u>level (int &#124; str):</u> a Python `logging` level, e.g. "INFO" or `logging.INFO`.

</details>
