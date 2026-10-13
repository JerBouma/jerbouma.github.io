---
title: "Configuration and Presets"
seo_title: "Configuration and Presets Reference – Finance Scenarios"
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

Load settings, factor sets and presets, list every named preset and scaffold a project. Generated from the docstrings of Finance Scenarios 0.1.0; `help(...)` in Python shows the same text.

```python
from financescenarios import ScenariosConfig, Profile, list_presets, load_profiles, load_config, load_profile_library, scaffold_project, set_log_level, set_display
```

## ScenariosConfig

```python
class ScenariosConfig(_StrictModel):
    start_date: date
    engine: EngineConfig = Field(default_factory=EngineConfig)
    reporting: ReportingConfig = Field(default_factory=ReportingConfig)
    interest_rates: list[InterestRateConfig] = Field(default_factory=lambda: [InterestRateConfig()], description="One or more interest-rate 'clouds' (one per country/region), each its own correlated short-rate factor. Must have at least one entry: interest rate is an always-on MVP factor. Authored in YAML as {defaults: {...}, countries: [{name: ..., <overrides>}, ...]}; see _resolve_countries().")
    inflation: list[InflationConfig] = Field(default_factory=lambda: [InflationConfig()], description="One or more inflation 'clouds' (one per country), each its own correlated factor. Must have at least one entry. Same {defaults, countries} authored shape as interest_rates.")
    equities: list[EquityConfig] = Field(default_factory=lambda: [EquityConfig()], description="One or more equity 'clouds' (broad index, sector, region, style, ...), each its own correlated regime-switching factor. Must have at least one entry: equity is an always-on MVP factor.")
    unemployment: list[UnemploymentConfig] = Field(default_factory=lambda: [UnemploymentConfig()], description="One or more unemployment 'clouds' (one per region), each paired with a named inflation entry for its Phillips-curve term. Must have at least one entry. Same {defaults, countries} authored shape as interest_rates, plus inflation_name auto-pairing; see _resolve_countries().")
    yield_curve: YieldCurveConfig = Field(default_factory=YieldCurveConfig)
    credit_term_structure: CreditTermStructureConfig = Field(default_factory=CreditTermStructureConfig)
    hjm: HjmConfig = Field(default_factory=HjmConfig)
    real_estate: RealEstateConfig = Field(default_factory=RealEstateConfig)
    credit: list[CreditConfig] = Field(default_factory=list, description='Zero or more credit-spread bucket factors (opt-in, empty = disabled).')
    leading_indicator: LeadingIndicatorConfig = Field(default_factory=LeadingIndicatorConfig)
    credit_migration: CreditMigrationConfig = Field(default_factory=CreditMigrationConfig)
    climate: ClimateConfig = Field(default_factory=ClimateConfig)
    fx: list[FXConfig] = Field(default_factory=list, description='Zero or more FX currency-pair factors (opt-in, empty = disabled).')
    commodities: list[CommodityConfig] = Field(default_factory=list, description="Zero or more commodity factors (opt-in, empty = disabled), each a Schwartz (1997) mean-reverting process on one commodity/futures ticker's log spot price.")
    dividend_yield: list[DividendYieldConfig] = Field(default_factory=list, description="Zero or more dividend yield factors (opt-in, empty = disabled), each an Ahlgrim/D'Arcy/Gorvett (2005) mean-reverting process on one ticker's log trailing dividend yield.")
    dividend_growth: list[DividendGrowthConfig] = Field(default_factory=list, description="Zero or more dividend growth factors (opt-in, empty = disabled), each a Wilkie (1986) Reduced Basis process on one ticker's dividend index. Each entry requires a paired inflation[] entry and a paired dividend_yield[] entry.")
    mortality: MortalityConfig = Field(default_factory=MortalityConfig)
    toolkit: ToolkitConfig = Field(default_factory=ToolkitConfig)
    external_scenario_source: ExternalScenarioSourceConfig = Field(default_factory=ExternalScenarioSourceConfig)
```

The full configuration of a run: when it starts, how it executes and which factors it simulates.

Every run is built from one `ScenariosConfig`. You rarely write one by hand: `load_profiles` builds it from a named
settings profile and factor set, and `load_config` from two YAML files. It can also be built straight from a
dictionary with `ScenariosConfig.model_validate`. Each top-level key is one section:

| Key | What it sets |
|:----|:-------------|
| `start_date` | The first date of the simulation; the only required key. |
| `engine` | The number of scenarios, steps and their frequency, the seed and how shocks are drawn. |
| `toolkit` | The history the factors are fitted on (start and end date) and any extra tickers. |
| `reporting` | The currency results can be converted into. |
| `interest_rates`, `inflation`, `unemployment` | One entry per country, at least one each. |
| `equities` | One entry per index or ETF, at least one. |
| `fx`, `commodities`, `credit`, `dividend_yield`, `dividend_growth` | Optional lists, empty by default. |
| `yield_curve`, `credit_term_structure`, `hjm`, `real_estate` | Optional factors, switched on with `enabled: true`. |
| `leading_indicator`, `credit_migration`, `climate`, `mortality` | The same. |
| `external_scenario_source` | A published scenario set (GOES or DNB) used for some factors instead. |

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

## factor_categories

```python
scenariosconfig.factor_categories  # property -> dict[str, str]
```

Every factor name this config simulates, mapped to the category it came
from: the resolved config already knows this unambiguously (it's just
which field each entry was authored under), so this reads it off directly
rather than inferring it from the name string, which is free-form for
several categories (equities/credit/fx/commodities/dividend_*) and would
silently misclassify a user-chosen name.

Every name `Scenarios.simulate()` puts in `ScenarioSet.paths` appears here,
including the derived ones a single config entry expands into: a
`method="schwartz_smith"` commodity's `<name>_chi`/`<name>_xi` latent
components (category `"commodities_state"`, not `"commodities"`; they're
log-space state variables, not a priced series; the reconstructed
`<name>` price is the `"commodities"` one) and a
`method="hibbert_two_factor"` entry's `<name>_target` moving target
(category `"<parent category>_target"`, same reasoning).

**Returns:**

<u>dict[str, str]:</u> factor name -> category. Investable categories (the ones a `Portfolio` sleeve may name) are `portfolio_model.INVESTABLE_FACTOR_TYPES`.

## factor_labels

```python
scenariosconfig.factor_labels  # property -> dict[str, 'FactorLabel']
```

Every simulated factor name mapped to its two-layer display identity,
read off each entry's own authored fields (country/term/name), never
parsed back out of the slug. Country-scoped macro factors lead with what
they measure ("Inflation" — "United States"); instance-named factors
lead with the instance so a grid of ten equities never repeats one
title ("US Broad" — "Equity", "Gold" — "Commodity", "Euro" — "Exchange
Rate"). Stamped onto every `Scenarios.simulate()` result
(`ScenarioSet.factor_labels`) and persisted with a written run;
"united_states_inflation" stays the internal key.

**Returns:**

<u>dict[str, FactorLabel]:</u> factor name -> display label, covering the same names `factor_categories` does.

## describe

```python
describe() -> pl.DataFrame
```

One row per configured category: how many factors it contributes and what
they're called: the "what would this actually simulate" read, before
paying for a calibration. The config-side counterpart to
`CalibrationResult.describe()` (what the fit said) and
`ScenarioSet.describe()` (where the run landed).

**Returns:**

<u>pl.DataFrame:</u> "category", "n_factors", "factors" (comma-separated names, in configuration order), sorted by category.

## with_equity

```python
with_equity(name: str, ticker: str, **fields: Any) -> 'ScenariosConfig'
```

Return a copy of this configuration with one more equity added, such as a sector or regional ETF.

Each equity is its own correlated factor in the run, fitted to its ticker's history and named by `name`, the
name you use for it in portfolios, regimes and results. The configuration you call this on is left as it was,
so several variants can be built from one base. Any other equity setting (`period`, `currency`, `method`,
`beliefs`, ...) can be passed by keyword, as in an `equities` entry of a factor set.

The new configuration is checked like any other: a name already used by another factor raises, as it would
when written in a factor set.

**Args:**

- <u>name (str):</u> the factor's name, e.g. "tech"; unique across all factors.
- <u>ticker (str):</u> the ticker to fit it to, e.g. "XLK".
- <u>fields (Any):</u> any other `EquityConfig` setting, e.g. `period="weekly"`.

**Returns:**

<u>ScenariosConfig:</u> a new configuration with the equity appended to `equities`.

**Raises:**

- <u>pydantic.ValidationError:</u> if the name is already used, or a setting is unknown or does not fit.

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

## tickers

```python
scenariosconfig.tickers  # property -> list[str]
```

All tickers the embedded `Toolkit` instance must be constructed with:
every ticker-sourced interest-rate entry's ticker (plus its `target_ticker`
when `method="hibbert_two_factor"` and `target_source="long_term_rate"`;
a second, independently-fetched series, not derivable from `ticker` alone),
every configured equity's ticker, every configured commodity's ticker, every
configured dividend yield/dividend growth entry's ticker, the four
yield-curve tenor tickers if `yield_curve.enabled`, `hjm.enabled`, any
`method="knw_sv"` interest_rates entry has `measure="risk_neutral"` (KnwSvQ fits its market
price of risk against that same panel), or any interest_rates entry has
`risk_neutral_forward_curve=true` (`calibrate_risk_neutral_forward` fits today's
forward curve against that same panel), plus `toolkit.extra_tickers`,
deduplicated in order of first appearance.

**Returns:**

<u>list[str]:</u> the unique tickers to pass to `Toolkit()`.

## Profile

```python
class Profile(BaseModel):
    id: str
    name: str
    description: str = ''
    data: dict[str, Any] = Field(default_factory=dict)
```

One named settings profile or factor set, read from its YAML file with any `extends` chain merged in.

`load_profile_library` returns these, keyed by id; `load_profiles` merges a settings profile and a factor set into
one configuration; `list_presets` shows them as a table.

**Attributes:**

- <u>id (str):</u> the file name without ".yaml", e.g. "long_horizon"; the name you pass to `Scenarios.from_profiles`.
- <u>name (str):</u> a short, readable label, e.g. "Long Horizon"; the `id` when the file sets none.
- <u>description (str):</u> what the profile is for; "" when the file sets none.
- <u>data (dict[str, Any]):</u> the profile's settings, ready to merge into a configuration.

## list_presets

```python
list_presets(kind: str | None = None) -> pl.DataFrame
```

List every ready-made preset you can name, with the call that takes it.

There are four kinds: settings profiles and factor sets (for `Scenarios.from_profiles`), regimes (its `regime=`)
and portfolios (for `Portfolio.from_preset`). A local folder of the same name, such as one `scaffold_project` wrote,
is read instead of the bundled copy, exactly as those calls do.

**Args:**

- <u>kind (str &#124; None):</u> "settings", "factor-sets", "regimes" or "portfolios"; None (the default) lists all four.

**Returns:**

<u>pl.DataFrame:</u> one row per preset: 'kind', 'id' (the name to pass), 'use_with' (the call and argument that takes it), 'name' and 'description'.

**Raises:**

- <u>ValueError:</u> if `kind` is not one of the four.

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

## load_profiles

```python
load_profiles(
    settings_dir: str | Path = 'settings',
    settings_id: str = 'default',
    factor_sets_dir: str | Path = 'factor-sets',
    factor_set_id: str = 'default',
) -> ScenariosConfig
```

Load a configuration from a named settings profile and a named factor set, such as "default" and "us_only".

A settings profile says how a run executes (start date, steps, number of scenarios, seed); a factor set says what it
simulates. Each is one YAML file picked by name, and may start with `extends: <name>` to build on another profile.
Swapping one never changes the other. This is what `Scenarios.from_profiles` uses, and `list_presets` shows every
name you can pass.

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

## load_config

```python
load_config(config_path: str | Path, factors_path: str | Path | None = None) -> ScenariosConfig
```

Load a configuration from two YAML files: one for how the run executes, one for what it simulates.

`config_path` holds the run settings (`start_date`, `engine`, `toolkit`, `reporting`) and `factors_path` the factor
definitions (`interest_rates`, `inflation`, `equities`, `fx`, ...). Keeping them apart means changing what is
simulated never touches how the run executes, and the other way around. A section left out of both files takes its
default. To pick named, ready-made profiles instead of file paths, use `load_profiles`.

**Args:**

- <u>config_path (str &#124; Path):</u> the run-settings YAML file.
- <u>factors_path (str &#124; Path &#124; None):</u> the factor-definitions YAML file; a `factors.yaml` next to `config_path` by default. Without that default file every factor takes its default; a path you pass must exist.

**Returns:**

<u>ScenariosConfig:</u> the validated configuration, merged from both files.

**Raises:**

- <u>FileNotFoundError:</u> if `config_path`, or a `factors_path` you pass, does not exist.
- <u>ValueError:</u> if a file is not valid YAML or does not hold a mapping of keys to values.
- <u>pydantic.ValidationError:</u> if the merged fields do not form a valid configuration, e.g. a misspelt key.

**As an example:**

```python
from financescenarios import Scenarios, load_config

config = load_config("my-project/config.yaml")  # reads my-project/factors.yaml too
scenarios = Scenarios.from_config(config)
```

## load_profile_library

```python
load_profile_library(directory: str | Path) -> dict[str, Profile]
```

Load every profile in a folder, one YAML file per profile, each with its `extends` chain merged in.

Use it to see what a folder holds; to run with one profile, `load_profiles` (or `Scenarios.from_profiles`) reads
only the files it needs. `list_presets` gives the same overview as a table.

**Args:**

- <u>directory (str &#124; Path):</u> the profiles folder, e.g. "settings" or "factor-sets"; the bundled presets when no such folder exists.

**Returns:**

<u>dict[str, Profile]:</u> every profile, keyed by its id (the file name without ".yaml").

**Raises:**

- <u>FileNotFoundError:</u> if the folder does not exist and is not one of the bundled preset folders.
- <u>ValueError:</u> if a file is not valid YAML or its `extends` chain loops back on itself.

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

## scaffold_project

```python
scaffold_project(target_dir: str | Path, force: bool = False) -> list[Path]
```

Copy the bundled presets into a folder you can edit: settings profiles, factor sets, regimes and portfolios, plus a
`.env` template for API keys.

The bundled presets work without this: `Scenarios.from_profiles` and `list_presets` read them straight from the
package. Scaffold only when you want to change them. Once a `settings/`, `factor-sets/`, `regimes/` or `portfolios/`
folder exists where Python runs, it is read instead of the bundled copy. A `.gitignore` that keeps `.env` out of git
and a `README.md` explaining the folders are written too.

**Args:**

- <u>target_dir (str &#124; Path):</u> the folder to write into, created if missing.
- <u>force (bool):</u> overwrite files that already exist; False by default, which skips them, so running it again only fills in what is missing.

**Returns:**

<u>list[Path]:</u> every file written: the presets folder by folder, then `.env`, `.gitignore` and `README.md`.

**As an example:**

```python
from financescenarios import Scenarios, scaffold_project

scaffold_project("my-project")
scenarios = Scenarios.from_profiles(settings_dir="my-project/settings", factor_sets_dir="my-project/factor-sets")
```

## set_log_level

```python
set_log_level(level: int | str) -> None
```

Set how much Finance Scenarios, and the Finance Toolkit underneath, prints while it works.

"WARNING" (the default) shows only what needs a look, "INFO" every calibration, data fetch and simulation step, and
"ERROR" next to nothing.

**Args:**

- <u>level (int &#124; str):</u> a Python `logging` level, e.g. "INFO" or `logging.INFO`.

**As an example:**

```python
from financescenarios import set_log_level

set_log_level("INFO")
```

## set_display

```python
set_display(
    width: int = 200,
    text: int = 1000,
    rows: int = 100,
    columns: int = 20,
    reset: bool = False,
) -> None
```

Make Polars print this package's tables in full, in a notebook or a terminal, with one call.

Polars, the table library every result here comes as, shortens what it prints: about 30 characters of text per
cell, 10 rows and 8 columns. That cuts off the "detail" and "meaning" of `scenarios.validate(result)`, the factors
of a long `describe()` and the quantile columns of `compare_runs`. This sets the table width, the text length per
cell, and the rows and columns shown, so those tables print whole; long text wraps within its cell instead. It only
changes how tables are shown, never their values, and lasts for the session. `reset=True` hands these four
options back to Polars' own defaults.

**Args:**

- <u>width (int):</u> the widest a printed table may be, in characters; -1 for no limit. Defaults to 200.
- <u>text (int):</u> the most characters of text shown per cell. Defaults to 1000.
- <u>rows (int):</u> the most rows shown before the middle is cut; -1 for every row. Defaults to 100.
- <u>columns (int):</u> the most columns shown before the middle is cut; -1 for every column. Defaults to 20.
- <u>reset (bool):</u> restore Polars' defaults instead, ignoring the other arguments. Defaults to False.

**Raises:**

- <u>ValueError:</u> if an argument is not a whole number, `text` is below 1, or `width` is 0.

**As an example:**

```python
from financescenarios import set_display

set_display()                    # validate(), describe() and compare_runs() print in full
set_display(width=120, rows=30)  # narrower, fewer rows
set_display(reset=True)          # back to Polars' defaults
```
