---
title: "Configuration and Presets"
seo_title: "Configuration and Presets Reference | Finance Scenarios"
seo_title_suffix: false
excerpt: "Load settings, factor sets and presets, list every named preset and scaffold a project."
description: "Load settings, factor sets and presets, list every named preset and scaffold a project."
author_profile: false
permalink: /projects/financescenarios/docs/reference/configuration
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

Load settings, factor sets and presets, list every named preset and scaffold a project.

```python
from financescenarios import ScenariosConfig, Profile, list_presets, load_profiles, load_config, load_profile_library, scaffold_project, set_log_level, set_display
```

## ScenariosConfig

The full configuration of a run: when it starts, how it executes, which factors it simulates and which views
override their history.

Every run is built from one `ScenariosConfig`, so it is also the record of a study's assumptions: the history each
factor is fitted on, the models chosen, and every belief (a long-run inflation target, a lower equity premium) laid
over the fit. You rarely write one by hand: `load_profiles` builds it from a named settings profile and factor
set, and `load_config` from two YAML files. It can also be built straight from a dictionary with
`ScenariosConfig.model_validate`. Each top-level key is one section:

| Key | What it sets |
|:----|:-------------|
| `start_date` | The first date of the simulation; the only required key. |
| `engine` | The number of scenarios, steps and their frequency, the seed and how shocks are drawn (see below). |
| `toolkit` | The history the factors are fitted on (start and end date) and any extra tickers. |
| `reporting` | The currency results can be converted into. |
| `interest_rates`, `inflation`, `unemployment` | One entry per country, at least one each. |
| `equities` | One entry per index or ETF, at least one. |
| `fx`, `commodities`, `credit`, `dividend_yield`, `dividend_growth` | Optional lists, empty by default. |
| `yield_curve`, `credit_term_structure`, `hjm`, `real_estate` | Optional factors, switched on with `enabled: true`. |
| `leading_indicator`, `credit_migration`, `climate`, `mortality` | The same. |
| `external_scenario_source` | A published scenario set (GOES or DNB) used for some factors instead. |

How shocks are drawn matters for the tails. With `shock_distribution: student_t` the joint shocks have fat tails and
tail dependence: extreme moves are more frequent and tend to arrive in several factors at once, as in 2008 or 2020,
where under the default Gaussian shocks a joint crash is far rarer. `antithetic: true` pairs every scenario with its
mirror image (the same shocks with the opposite sign), which cancels much of the sampling noise in averages and
valuations for the same number of scenarios; it does not change the model, only how precisely a given number of
scenarios measures it.

Interest rates, inflation and unemployment are written per country, as `{defaults: {...}, countries: [{name: ...},
...]}`, so shared settings are given once. The configuration is checked as it is built: a misspelt key, a duplicate
factor name or settings that do not fit together raise an error before any data is fetched. `describe()` lists the
factors it would simulate, `tickers` the tickers it would download, and `factor_categories` and `factor_labels` give
each factor's category and display name.

**As an example:**

```python
from datetime import date

from financescenarios.config.config_model import ScenariosConfig

config = ScenariosConfig.model_validate(
    {
        "start_date": date(2026, 10, 1),
        "engine": {"n_simulations": 2000, "n_steps": 12, "frequency": "monthly", "seed": 42},
        "interest_rates": {"countries": [{"name": "United States"}]},
        "inflation": {"countries": [{"name": "United States"}]},
        "unemployment": {"countries": [{"name": "United States"}]},
        "equities": [{"name": "us_broad", "ticker": "SPY", "period": "monthly"}],
    }
)
config.describe()
```

Which returns:

| category | n_factors | factors |
|:---------|----------:|:--------|
| equities | 1 | us_broad |
| inflation | 1 | united_states_inflation |
| interest_rates | 1 | united_states_short_rate |
| unemployment | 1 | united_states_unemployment |

and `config.tickers` is `['^IRX', 'SPY']`: the 13-week Treasury yield for the short rate, and SPY.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
class ScenariosConfig(_StrictModel):
    start_date: date
    engine: EngineConfig = Field(default_factory=EngineConfig)
    reporting: ReportingConfig = Field(default_factory=ReportingConfig)
    interest_rates: list[InterestRateConfig] = Field(default_factory=lambda: [InterestRateConfig()], description='One interest rate per country or region, each its own correlated factor; at least one. Written in YAML as {defaults: {...}, countries: [{name: ..., <overrides>}, ...]}, or as a list of entries.')
    inflation: list[InflationConfig] = Field(default_factory=lambda: [InflationConfig()], description='One inflation rate per country, each its own correlated factor; at least one. Written as {defaults, countries}, like interest_rates.')
    equities: list[EquityConfig] = Field(default_factory=lambda: [EquityConfig()], description='One entry per equity index, sector, region or style, each its own correlated regime-switching factor; at least one.')
    unemployment: list[UnemploymentConfig] = Field(default_factory=lambda: [UnemploymentConfig()], description="One unemployment rate per region, each paired with that region's inflation through a Phillips curve; at least one. Written as {defaults, countries}, like interest_rates.")
    yield_curve: YieldCurveConfig = Field(default_factory=YieldCurveConfig)
    credit_term_structure: CreditTermStructureConfig = Field(default_factory=CreditTermStructureConfig)
    hjm: HjmConfig = Field(default_factory=HjmConfig)
    real_estate: RealEstateConfig = Field(default_factory=RealEstateConfig)
    credit: list[CreditConfig] = Field(default_factory=list, description='Credit spreads by maturity, rating bucket or country; none by default.')
    leading_indicator: LeadingIndicatorConfig = Field(default_factory=LeadingIndicatorConfig)
    credit_migration: CreditMigrationConfig = Field(default_factory=CreditMigrationConfig)
    climate: ClimateConfig = Field(default_factory=ClimateConfig)
    fx: list[FXConfig] = Field(default_factory=list, description='Exchange rates against the US dollar, one per currency; none by default.')
    commodities: list[CommodityConfig] = Field(default_factory=list, description='Commodities, each mean-reverting in its log price (Schwartz, 1997); none by default.')
    dividend_yield: list[DividendYieldConfig] = Field(default_factory=list, description="Dividend yields, each mean-reverting in its log (Ahlgrim, D'Arcy & Gorvett, 2005); none by default.")
    dividend_growth: list[DividendGrowthConfig] = Field(default_factory=list, description='Dividend growth as in Wilkie (1986), each tied to an inflation and a dividend_yield entry; none by default.')
    mortality: MortalityConfig = Field(default_factory=MortalityConfig)
    toolkit: ToolkitConfig = Field(default_factory=ToolkitConfig)
    external_scenario_source: ExternalScenarioSourceConfig = Field(default_factory=ExternalScenarioSourceConfig)
```

</details>

## factor_categories

Every factor this configuration simulates, mapped to its category ("equities", "inflation", ...).

It covers every name a simulated run holds, including the helper series some models add next to the factor you
configured: a two-factor commodity's short- and long-term components ("commodities_state") and the moving
long-run target of a two-factor rate or inflation ("interest_rates_target", "inflation_target").

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
scenariosconfig.factor_categories  # property -> dict[str, str]
```

**Returns:**

<u>dict[str, str]:</u> factor name -> category.

</details>

## factor_labels

Every factor's display name for charts and tables, such as "Inflation — United States" or "US Broad — Equity".

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
scenariosconfig.factor_labels  # property -> dict[str, 'FactorLabel']
```

**Returns:**

<u>dict[str, FactorLabel]:</u> factor name -> display label, for the same names as `factor_categories`.

</details>

## describe

What this configuration would simulate, one row per category, before any data is fetched or fitted.

It sits next to `CalibrationResult.describe()` (what the fit said) and `ScenarioSet.describe()` (where the run
landed).

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
describe() -> pl.DataFrame
```

**Returns:**

<u>pl.DataFrame:</u> "category", "n_factors", "factors" (comma-separated names, in configuration order), sorted by category.

</details>

## with_equity

Return a copy of this configuration with one more equity added, such as a sector or regional ETF.

Each equity is its own correlated factor in the run, fitted to its ticker's history and named by `name`, the
name you use for it in portfolios, regimes and results. The configuration you call this on is left as it was,
so several variants can be built from one base. Any other equity setting (`period`, `currency`, `method`,
`beliefs`, ...) can be passed by keyword, as in an `equities` entry of a factor set.

The new configuration is checked like any other: a name already used by another factor raises, as it would
when written in a factor set.

**As an example:**

```python
import polars as pl

from financescenarios import load_profiles

config = load_profiles(factor_set_id="us_only").with_equity("tech", "XLK")
config.describe().filter(pl.col("category") == "equities")
```

Which returns:

| category | n_factors | factors |
|:---------|----------:|:--------|
| equities | 2 | us_broad, tech |

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
with_equity(name: str, ticker: str, **fields: Any) -> 'ScenariosConfig'
```

**Args:**

- <u>name (str):</u> the factor's name, e.g. "tech"; unique across all factors.
- <u>ticker (str):</u> the ticker to fit it to, e.g. "XLK".
- <u>fields (Any):</u> any other `EquityConfig` setting, e.g. `period="weekly"`.

**Returns:**

<u>ScenariosConfig:</u> a new configuration with the equity appended to `equities`.

**Raises:**

- <u>pydantic.ValidationError:</u> if the name is already used, or a setting is unknown or does not fit.

</details>

## tickers

Every market ticker this configuration downloads history for: the rates, equities, commodities and dividend
series, the Treasury yields behind a yield curve or a risk-neutral forward curve, and any extra tickers.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
scenariosconfig.tickers  # property -> list[str]
```

**Returns:**

<u>list[str]:</u> the unique tickers, in the order they first appear.

</details>

## Profile

One named settings profile or factor set, read from its YAML file with any `extends` chain merged in.

`load_profile_library` returns these, keyed by id; `load_profiles` merges a settings profile and a factor set into
one configuration; `list_presets` shows them as a table.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
class Profile(BaseModel):
    id: str
    name: str
    description: str = ''
    data: dict[str, Any] = Field(default_factory=dict)
```

**Attributes:**

- <u>id (str):</u> the file name without ".yaml", e.g. "long_horizon"; the name you pass to `Scenarios.from_profiles`.
- <u>name (str):</u> a short, readable label, e.g. "Long Horizon"; the `id` when the file sets none.
- <u>description (str):</u> what the profile is for; "" when the file sets none.
- <u>data (dict[str, Any]):</u> the profile's settings, ready to merge into a configuration.

</details>

## list_presets

List every ready-made preset you can name, with the call that takes it.

There are four kinds: settings profiles and factor sets (for `Scenarios.from_profiles`), regimes (its `regime=`)
and portfolios (for `Portfolio.from_preset`). A local folder of the same name, such as one `scaffold_project` wrote,
is read instead of the bundled copy, exactly as those calls do.

**As an example:**

```python
from financescenarios import list_presets

list_presets(kind="settings")
```

Which returns (without the 'description' column):

| kind | id | use_with | name |
|:-----|:---|:---------|:-----|
| settings | default | Scenarios.from_profiles(settings="default") | Default |
| settings | goes | Scenarios.from_profiles(settings="goes") | NAIC GOES |
| settings | long_horizon | Scenarios.from_profiles(settings="long_horizon") | Long Horizon |
| settings | wilkie | Scenarios.from_profiles(settings="wilkie") | Wilkie 1986 |

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
list_presets(kind: str | None = None) -> pl.DataFrame
```

**Args:**

- <u>kind (str &#124; None):</u> "settings", "factor-sets", "regimes" or "portfolios"; None (the default) lists all four.

**Returns:**

<u>pl.DataFrame:</u> one row per preset: 'kind', 'id' (the name to pass), 'use_with' (the call and argument that takes it), 'name' and 'description'.

**Raises:**

- <u>ValueError:</u> if `kind` is not one of the four.

</details>

## load_profiles

Load a configuration from a named settings profile and a named factor set, such as "default" and "us_only".

A settings profile says how a run executes (start date, steps, number of scenarios, seed); a factor set says what it
simulates: which factors, fitted on which history, and the beliefs laid over that fit. Each is one YAML file picked
by name, and may start with `extends: <name>` to build on another profile. Swapping one never changes the other.
This is what `Scenarios.from_profiles` uses, and `list_presets` shows every name you can pass.

**As an example:**

```python
from financescenarios import load_profiles

config = load_profiles(settings_id="long_horizon", factor_set_id="us_only")
config.describe()
```

Which returns (cut to four of the ten categories):

| category | n_factors | factors |
|:---------|----------:|:--------|
| equities | 1 | us_broad |
| fx | 9 | eur, gbp, jpy, chf, cad, aud, cny, inr, brl |
| inflation | 1 | united_states_inflation |
| interest_rates | 2 | united_states_short_rate, united_states_long_rate |

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
load_profiles(
    settings_dir: str | Path = 'settings',
    settings_id: str = 'default',
    factor_sets_dir: str | Path = 'factor-sets',
    factor_set_id: str = 'default',
) -> ScenariosConfig
```

**Args:**

- <u>settings_dir (str &#124; Path):</u> the settings folder; "settings" by default, the bundled presets when it does not exist.
- <u>settings_id (str):</u> the settings profile's name, e.g. "long_horizon"; "default" by default.
- <u>factor_sets_dir (str &#124; Path):</u> the factor-set folder; "factor-sets" by default, the bundled presets when it does not exist.
- <u>factor_set_id (str):</u> the factor set's name, e.g. "us_only"; "default" by default.

**Returns:**

<u>ScenariosConfig:</u> the validated configuration, merged from both profiles.

**Raises:**

- <u>FileNotFoundError:</u> if either profile, or one it extends, does not exist; the message lists the names available.
- <u>ValueError:</u> if an `extends` chain loops back on itself.
- <u>pydantic.ValidationError:</u> if the merged fields do not form a valid configuration.

</details>

## load_config

Load a configuration from two YAML files: one for how the run executes, one for what it simulates.

`config_path` holds the run settings (`start_date`, `engine`, `toolkit`, `reporting`) and `factors_path` the factor
definitions (`interest_rates`, `inflation`, `equities`, `fx`, ...). Keeping them apart means changing what is
simulated never touches how the run executes, and the other way around. A section left out of both files takes its
default. To pick named, ready-made profiles instead of file paths, use `load_profiles`.

**As an example:**

```python
from financescenarios import Scenarios, load_config

config = load_config("my-project/config.yaml")  # reads my-project/factors.yaml too
scenarios = Scenarios.from_config(config)
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
load_config(config_path: str | Path, factors_path: str | Path | None = None) -> ScenariosConfig
```

**Args:**

- <u>config_path (str &#124; Path):</u> the run-settings YAML file.
- <u>factors_path (str &#124; Path &#124; None):</u> the factor-definitions YAML file; a `factors.yaml` next to `config_path` by default. Without that default file every factor takes its default; a path you pass must exist.

**Returns:**

<u>ScenariosConfig:</u> the validated configuration, merged from both files.

**Raises:**

- <u>FileNotFoundError:</u> if `config_path`, or a `factors_path` you pass, does not exist.
- <u>ValueError:</u> if a file is not valid YAML or does not hold a mapping of keys to values.
- <u>pydantic.ValidationError:</u> if the merged fields do not form a valid configuration, e.g. a misspelt key.

</details>

## load_profile_library

Load every profile in a folder, one YAML file per profile, each with its `extends` chain merged in.

Use it to see what a folder holds; to run with one profile, `load_profiles` (or `Scenarios.from_profiles`) reads
only the files it needs. `list_presets` gives the same overview as a table.

**As an example:**

```python
from financescenarios import load_profile_library

profiles = load_profile_library("settings")
{profile_id: profile.name for profile_id, profile in profiles.items()}
```

Which returns:

```
{'default': 'Default', 'goes': 'NAIC GOES', 'long_horizon': 'Long Horizon', 'wilkie': 'Wilkie 1986'}
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
load_profile_library(directory: str | Path) -> dict[str, Profile]
```

**Args:**

- <u>directory (str &#124; Path):</u> the profiles folder, e.g. "settings" or "factor-sets"; the bundled presets when no such folder exists.

**Returns:**

<u>dict[str, Profile]:</u> every profile, keyed by its id (the file name without ".yaml").

**Raises:**

- <u>FileNotFoundError:</u> if the folder does not exist and is not one of the bundled preset folders.
- <u>ValueError:</u> if a file is not valid YAML or its `extends` chain loops back on itself.

</details>

## scaffold_project

Copy the bundled presets into a folder you can edit: settings profiles, factor sets, regimes and portfolios, plus a
`.env` template for API keys.

The bundled presets work without this: `Scenarios.from_profiles` and `list_presets` read them straight from the
package. Scaffold only when you want to change them. Once a `settings/`, `factor-sets/`, `regimes/` or `portfolios/`
folder exists where Python runs, it is read instead of the bundled copy. A `.gitignore` that keeps `.env` out of git
and a `README.md` explaining the folders are written too.

**As an example:**

```python
from financescenarios import Scenarios, scaffold_project

scaffold_project("my-project")
scenarios = Scenarios.from_profiles(settings_dir="my-project/settings", factor_sets_dir="my-project/factor-sets")
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
scaffold_project(target_dir: str | Path, force: bool = False) -> list[Path]
```

**Args:**

- <u>target_dir (str &#124; Path):</u> the folder to write into, created if missing.
- <u>force (bool):</u> overwrite files that already exist; False by default, which skips them, so running it again only fills in what is missing.

**Returns:**

<u>list[Path]:</u> every file written: the presets folder by folder, then `.env`, `.gitignore` and `README.md`.

</details>

## set_log_level

Set how much Finance Scenarios, and the Finance Toolkit underneath, prints while it works.

"WARNING" (the default) shows only what needs a look, "INFO" every calibration, data fetch and simulation step, and
"ERROR" next to nothing.

**As an example:**

```python
from financescenarios import set_log_level

set_log_level("INFO")
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
set_log_level(level: int | str) -> None
```

**Args:**

- <u>level (int &#124; str):</u> a Python `logging` level, e.g. "INFO" or `logging.INFO`.

</details>

## set_display

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
