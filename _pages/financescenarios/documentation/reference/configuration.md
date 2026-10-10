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
from financescenarios import ScenariosConfig, Profile, list_presets, load_profiles, load_config, load_profile_library, scaffold_project, set_log_level
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

Top-level configuration for a Scenarios run, loaded via load_config().

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

One resolved named profile: a settings/factor-set preset (or, indirectly,
a Regime, see regimes_controller.load_one()), fully merged down its `extends`
chain.

**Attributes:**

- <u>id (str):</u> the profile's filename stem, e.g. "long_horizon" for settings/long_horizon.yaml. What a caller names it by (the `settings`/`factor_set` request fields), same convention as a Regime's `id` in RegimeSummary.
- <u>name (str):</u> a short, human-readable label. Defaults to `id` when the YAML (or its extends chain) never sets a `name:` key.
- <u>description (str):</u> free-text documentation. Defaults to "" when unset.
- <u>data (dict[str, Any]):</u> the resolved dict, with `extends`/`name`/ `description` popped, ready to merge straight into whatever schema the caller validates it against.

## list_presets

```python
list_presets(kind: str | None = None) -> pl.DataFrame
```

Every ready-made preset you can name: settings profiles and factor sets (for `Scenarios.from_profiles`),
regimes (its `regime=`) and portfolios (for `Portfolio.from_preset`). A local folder of the same name, such
as one `scaffold_project()` wrote, is read instead of the bundled copy, exactly as those calls do.

**Args:**

- <u>kind (str &#124; None):</u> "settings", "factor-sets", "regimes" or "portfolios"; None lists all four.

**Returns:**

<u>pl.DataFrame:</u> one row per preset: 'kind', 'id' (the name to pass), 'use_with' (the call and argument that takes it), 'name' and 'description'.

**Raises:**

- <u>ValueError:</u> if `kind` is not one of the four.

**As an example:**

```python
from financescenarios import list_presets

list_presets(kind="portfolios")
```

## load_profiles

```python
load_profiles(
    settings_dir: str | Path = 'settings',
    settings_id: str = 'default',
    factor_sets_dir: str | Path = 'factor-sets',
    factor_set_id: str = 'default',
) -> ScenariosConfig
```

Load and validate a Scenarios configuration from a named settings profile and a
named factor-set profile: the `settings/`/`factor-sets/` counterpart to
`load_config()`'s two explicit file paths, mirroring how `regimes/` lets a run
pick a named, swappable preset instead of hand-editing a file in place. Each
profile is resolved independently via `profiles_controller.load_one()` (its own `extends`
chain, if any, merged in), then the two resolved dicts are shallow-merged the
same way `load_config()` merges `config.yaml`/`factors.yaml`, so swapping only
the settings profile or only the factor-set profile between two runs leaves the
other one byte-identical.

**Args:**

- <u>settings_dir (str &#124; Path):</u> the settings profiles directory (e.g. `settings/`).
- <u>settings_id (str):</u> the settings profile's filename, e.g. "default" or "long_horizon" (the ".yaml" suffix is optional).
- <u>factor_sets_dir (str &#124; Path):</u> the factor-set profiles directory (e.g. `factor-sets/`).
- <u>factor_set_id (str):</u> the factor-set profile's filename, e.g. "default" or "us_only" (the ".yaml" suffix is optional).

**Returns:**

<u>ScenariosConfig:</u> the validated configuration, merged from both profiles.

**Raises:**

- <u>FileNotFoundError:</u> if either profile (or a file in its `extends` chain) doesn't exist.
- <u>ValueError:</u> if either profile's `extends` chain is circular.
- <u>pydantic.ValidationError:</u> if the merged fields don't form a valid ScenariosConfig.

## load_config

```python
load_config(config_path: str | Path, factors_path: str | Path | None = None) -> ScenariosConfig
```

Load and validate a Scenarios configuration from two YAML files: `config_path`
for run settings (`start_date`, `engine`, `toolkit`) and `factors_path` for every
factor definition (`interest_rates`, `inflation`, `equities`, `unemployment`,
`yield_curve`, `real_estate`, `credit`, `leading_indicator`, `fx`, `commodities`,
`dividend_yield`, `mortality`; anything that names a belief override or picks
an index/ETF/ticker/country). Kept
as two separate files so changing what gets simulated (factors.yaml) never
touches run mechanics (config.yaml), and vice versa.

**Args:**

- <u>config_path (str &#124; Path):</u> path to the run-settings YAML file.
- <u>factors_path (str &#124; Path &#124; None):</u> path to the factor-definitions YAML file. Defaults to a `factors.yaml` sibling of `config_path` (same directory). If that file doesn't exist, factor sections fall back to `ScenariosConfig`'s own single-region defaults, same as any other omitted section; factors.yaml isn't required to exist.

**Returns:**

<u>ScenariosConfig:</u> the validated configuration, merged from both files.

## load_profile_library

```python
load_profile_library(directory: str | Path) -> dict[str, Profile]
```

Load every profile in a directory: one `*.yaml` file per profile, each
optionally starting with `extends: <filename>` to inherit another profile's
fields (see `load_one()`). Use this for "list everything" (a picker UI); to
run one specific profile, prefer `load_one()`, which never touches the other
files in the directory.

**Args:**

- <u>directory (str &#124; Path):</u> path to a directory of profile YAML files.

**Returns:**

<u>dict[str, Profile]:</u> every profile, keyed by its `id` (filename stem).

## scaffold_project

```python
scaffold_project(target_dir: str | Path, force: bool = False) -> list[Path]
```

Materialize the bundled default settings/, factor-sets/, regimes/ and
portfolios/ profiles, plus a `.env` key template, into `target_dir` --
everything `load_profiles()`/`Scenarios.from_profiles()` read, under their
default directory names. Only needed to get an *editable* copy: the
packaged profiles are readable in place without scaffolding anything (see
`profiles_controller.resolve_directory()`).

**Args:**

- <u>target_dir (str &#124; Path):</u> directory to scaffold into; created if missing.
- <u>force (bool):</u> overwrite files that already exist in `target_dir`. Defaults to False, which skips (not errors on) any file already present, so re-running in an already-scaffolded directory only fills in what's missing.

**Returns:**

<u>list[Path]:</u> every file actually written, relative-to-`target_dir` order matching `_SUBDIRS`, then `.env`, `.gitignore` (which keeps `.env` out of git) and a `README.md` explaining the folders.

## set_log_level

```python
set_log_level(level: int | str) -> None
```

How much Finance Scenarios (and the Finance Toolkit underneath) prints while it works: "WARNING" (the default)
shows only what needs a look, "INFO" every calibration, data fetch and simulation step, "ERROR" next to nothing.

**Args:**

- <u>level (int &#124; str):</u> a `logging` level, e.g. "INFO" or logging.INFO.
