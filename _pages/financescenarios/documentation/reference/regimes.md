---
title: "Regimes and Stress Tests"
seo_title: "Regimes and Stress Tests Reference – Finance Scenarios"
excerpt: "Named stress narratives and the official Federal Reserve and ESRB stress scenarios as regimes."
description: "Named stress narratives and the official Federal Reserve and ESRB stress scenarios as regimes."
author_profile: false
permalink: /projects/financescenarios/docs/reference/regimes
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

Named stress narratives and the official Federal Reserve and ESRB stress scenarios as regimes. Generated from the docstrings of Finance Scenarios 0.1.0; `help(...)` in Python shows the same text.

```python
from financescenarios import Regime, RegimeLibrary, load_regime, stress_test_regime
```

{% raw %}
## Regime

```python
class Regime(BaseModel):
    name: str = Field(min_length=1, description="A short, human-readable label, e.g. 'Oil Crisis'.")
    description: str = Field(default='', description='What this regime represents and why these targets/beliefs were chosen.')
    targets: dict[str, tuple[float, float]] | None = Field(default=None, description="factor name -> (lower, upper) quantile range, same shape as filter_narrative()'s targets.")
    beliefs: dict[str, dict[str, Any]] | None = Field(default=None, description="factor name -> that factor's belief-field overrides, same shape as ScenariosConfig's own beliefs sections.")
    step_range: tuple[int, int] | None = Field(default=None, description="Shared step range for every target, same semantics as filter_narrative()'s step_range.")
    target_mode: Literal['sequential', 'joint'] = Field(default='sequential', description="How targets combine: 'sequential' narrows target by target (each range is a quantile within what the previous targets left), 'joint' ranks every target against the full run and intersects; see ScenarioSet.filter_narrative().")
```

A named stress regime; see module docstring for how targets and beliefs differ.

**Attributes:**

- <u>name (str):</u> a short, human-readable label, e.g. "Oil Crisis".
- <u>description (str):</u> what this regime represents and why these targets/beliefs were chosen. Free text, purely documentation.
- <u>targets (dict[str, tuple[float, float]] &#124; None):</u> factor name -> (lower, upper) quantile range, the same shape as ScenarioSet.filter_narrative()'s targets argument. Applied post-simulation, via RegimeLibrary.apply().
- <u>beliefs (dict[str, dict[str, Any]] &#124; None):</u> factor name -> that factor's belief-field overrides, the same shape as ScenariosConfig's own `<factor>.beliefs` section (e.g. {"inflation": {"long_run_mean": {...}}} for a BeliefPath, or {"equity": {"regime_means": [...]}}). For a multi-instance factor (equities/fx/credit are lists in ScenariosConfig), use a dotted "<container>.<name>" key instead, e.g. {"equities.tech": {"regime_means": [...]}}, to target one list entry -- see RegimeLibrary.build_config(). Applied pre-simulation, via RegimeLibrary.build_config().
- <u>step_range (tuple[int, int] &#124; None):</u> shared step range for every target, same semantics as filter_narrative()'s step_range. Defaults to the full path. Only meaningful together with targets.
{% endraw %}

## RegimeLibrary

```python
RegimeLibrary(regimes: dict[str, Regime] | None = None)
```

A named collection of Regime presets, loadable from / savable to a
directory (one YAML file per regime), applicable to a ScenarioSet (targets)
and/or usable to build a belief-shaped ScenariosConfig (beliefs); see
Regime's docstring for the distinction.

## names

```python
regimelibrary.names  # property -> list[str]
```

The names of every regime currently in this library.

## add

```python
add(regime: Regime) -> None
```

Add (or replace) a regime in the library, keyed by its own name.

**Args:**

- <u>regime (Regime):</u> the regime to add.

## get

```python
get(name: str) -> Regime
```

**Args:**

- <u>name (str):</u> the regime's name.

**Returns:**

<u>Regime:</u> the regime registered under that name.

**Raises:**

- <u>KeyError:</u> if no regime is registered under that name.

## apply

```python
apply(scenario_set: ScenarioSet, name: str) -> ScenarioSet
```

Apply a named regime's targets to an already-simulated ScenarioSet, narrowing
it to the subset of simulations consistent with that regime's narrative.

**Args:**

- <u>scenario_set (ScenarioSet):</u> the simulation to narrow.
- <u>name (str):</u> the regime's name, must be registered in this library and have targets set.

**Returns:**

<u>ScenarioSet:</u> the simulations satisfying every target in the named regime, via ScenarioSet.filter_narrative().

**Raises:**

- <u>KeyError:</u> if no regime is registered under that name, or a regime's target factor is not in scenario_set.
- <u>ValueError:</u> if the regime has no targets (it's beliefs-only; use build_config()/simulate() instead), a quantile range is invalid, or no simulation satisfies every target at once.

{% raw %}
## build_config

```python
build_config(base_config: ScenariosConfig, name: str) -> ScenariosConfig
```

Build a ScenariosConfig with a named regime's belief overrides substituted in
on top of base_config, e.g. "Oil Crisis" believing inflation targets 8% in
1 year, easing to 3% by year 5, rather than whatever the calibrated OU fit's
long_run_mean would otherwise be.

A regime.beliefs key is either a plain factor name (real_estate,
leading_indicator, yield_curve, credit_term_structure, mortality: every
single-instance factor) or a dotted "<container>.<name>" key addressing
one entry of a multi-instance factor list (interest_rates, inflation,
unemployment, equities, fx, credit, commodities, dividend_yield), e.g.
"equities.us_broad" or "credit.ig_7_10y", matched against that entry's own
`name` field.

A factor override is deep-merged onto the existing belief block, not
replaced wholesale, e.g. {"yield_curve": {"level": {"long_run_mean":
0.05}}} only touches level.long_run_mean, leaving any other field already
set on level (or slope/curvature) untouched, the same nested-belief shape
yield_curve/credit_term_structure/mortality all have.

**Args:**

- <u>base_config (ScenariosConfig):</u> the config to start from; unaffected fields (everything not named in regime.beliefs) are unchanged.
- <u>name (str):</u> the regime's name, must be registered in this library.

**Returns:**

<u>ScenariosConfig:</u> base_config with each factor named in regime.beliefs having those belief fields overridden. Identical to base_config if the regime has no beliefs set.

**Raises:**

- <u>KeyError:</u> if no regime is registered under that name.
- <u>RegimeMismatchError:</u> (a ValueError, and a KeyError) if a dotted key names a container entry that doesn't exist in base_config, or a plain key names a multi-instance (list) factor; use a dotted "<container>.<name>" key for those instead, even when the list has only one entry.
- <u>pydantic.ValidationError:</u> if a belief override doesn't validate against that factor's beliefs schema (e.g. an unknown field name).
{% endraw %}

## simulate

```python
simulate(
    scenarios: 'Scenarios',
    base_config: ScenariosConfig,
    name: str,
    mortality_rates: pl.DataFrame | None = None,
    mortality_ages: list[float] | None = None,
    mortality_years: list[int] | None = None,
) -> ScenarioSet
```

Run a named regime end-to-end: build a belief-shaped config (build_config()),
calibrate and simulate it, then narrow to the regime's targets if it has any
(apply()'s filter_narrative() step): the single-call version of doing both
by hand.

**Args:**

- <u>scenarios (Scenarios):</u> the calibration/simulation entry point to run with.
- <u>base_config (ScenariosConfig):</u> the config to start from.
- <u>name (str):</u> the regime's name, must be registered in this library.
- <u>mortality_rates (pl.DataFrame &#124; None):</u> forwarded to Scenarios.simulate() if base_config.mortality.enabled; see that method's own docstring.
- <u>mortality_ages (list[float] &#124; None):</u> forwarded to Scenarios.simulate() if base_config.mortality.enabled.
- <u>mortality_years (list[int] &#124; None):</u> forwarded to Scenarios.simulate() if base_config.mortality.enabled.

**Returns:**

<u>ScenarioSet:</u> the belief-shaped simulation, further narrowed by targets if the regime has any.

**Raises:**

- <u>KeyError:</u> if no regime is registered under that name.

## load

```python
RegimeLibrary.load(directory: str | Path = 'regimes') -> 'RegimeLibrary'
```

Load every regime in a directory: one `*.yaml` file per regime, each
optionally starting with `extends: <filename>` to inherit another
regime's fields (see `load_one()`). Use this for "list everything"
(any listing/picker surface); to run one specific regime,
prefer `load_one()`, which never touches the other files in the directory.

**Args:**

- <u>directory (str &#124; Path):</u> path to a directory of regime YAML files.

**Returns:**

<u>RegimeLibrary:</u> the loaded library, keyed by each regime's `name`.

## save

```python
save(directory: str | Path) -> None
```

Save every regime in this library to `directory`, one file per regime
(named after a slugified version of its `name`); round-trips with
`load()`. Does not preserve any `extends` relationship a regime was
originally loaded with; every regime is written fully resolved.

**Args:**

- <u>directory (str &#124; Path):</u> destination directory, created if missing.

## load_regime

```python
load_regime(directory: str | Path, filename: str) -> Regime
```

Load exactly one regime, resolving its `extends` chain if it has one, but
never scanning the rest of `directory`. This is the path a single simulate
run should use to pick one regime, instead of building a full RegimeLibrary
(which parses every file in the directory) just to pick one back out of it;
see RegimeLibrary.load() for that "list everything" case.

**Args:**

- <u>directory (str &#124; Path):</u> the regimes directory.
- <u>filename (str):</u> the regime's own YAML filename, e.g. "oil_crisis.yaml" (the ".yaml" suffix is optional).

**Returns:**

<u>Regime:</u> the fully resolved regime (extends chain merged in, `name` required at the end of that chain).

**Raises:**

- <u>FileNotFoundError:</u> if `filename`, or a file named in its `extends` chain, doesn't exist in `directory`.
- <u>ValueError:</u> if the `extends` chain is circular, or no file in the chain sets `name`.
- <u>pydantic.ValidationError:</u> if the resolved fields don't form a valid Regime.

## stress_test_regime

```python
stress_test_regime(
    toolkit: Toolkit,
    config: ScenariosConfig,
    authority: Literal['federal_reserve', 'esrb'] = 'federal_reserve',
    scenario: Literal['baseline', 'adverse'] = 'adverse',
    year: int | None = None,
    converge_over_years: float = 5.0,
    follow: Literal['path', 'target'] = 'path',
    equity_regions: Mapping[str, str] | None = None,
) -> Regime
```

A regulator's published stress-test scenario as a regime: the scenario's paths for interest rates, inflation and
unemployment become belief paths for the matching factors of `config`, which steer each factor's long-run level
through the stress and then back to its own calibrated level over `converge_over_years`. With `follow="path"`
(the default) each factor is also set to the published value at every period end, so a slowly mean-reverting
factor such as a short rate really falls to the scenario's 0.1% rather than drifting toward it; the scenarios
then spread out again between those dates and after the scenario ends.

In plain terms: instead of writing a recession by hand, this takes the one the Federal Reserve or the European
Systemic Risk Board prescribes for banks' stress tests (unemployment climbing to 10%, say, and rates cut), and
lets the simulated scenarios follow it, with their own randomness around it.

Stock prices follow the scenario too, as one-off falls and recoveries at each period end
(`EquityBeliefs.shocks`): the Federal Reserve's stock index relative to its own baseline (so the falls are the
stress, not the baseline's growth), or the ESRB's stock-price deviation from the starting point. The stock path
keeps the scenario's own spacing but starts at the run's start, so the fall always happens within the run even
when the published scenario began earlier (the ESRB's 2025 scenario runs 2025 to 2027). On the default factor
set the Federal Reserve's 2026 adverse scenario takes US stocks about 50% below where they would otherwise be
after a year.

The two authorities (both through the Finance Toolkit's `economics.get_stress_test_scenario`, no key):

- "federal_reserve": the Federal Reserve's supervisory scenario for the United States, quarterly over 13
  quarters: the 3-month Treasury rate (short rates), the 10-year Treasury yield (long rates), CPI inflation and
  unemployment. Its inflation is the annualized quarter-on-quarter rate, while this project's inflation is
  year over year, so the inflation path is on the same scale but reacts sooner than a year-over-year series.
- "esrb": the European Systemic Risk Board's scenario for the EBA's EU-wide stress test, yearly over three years
  for every EU member and the main other economies: the long-term interest rate, inflation and unemployment
  (no short rate).

Each entry follows its own `country` (for the Federal Reserve, only the United States). Interest rates with a
method other than hull_white or cir, and risk-neutral entries, have no long-run level to steer and are left as
calibrated.

**Args:**

- <u>toolkit (Toolkit):</u> the Finance Toolkit `Toolkit`.
- <u>config (ScenariosConfig):</u> the configuration the regime will be applied to.
- <u>authority (str):</u> "federal_reserve" or "esrb".
- <u>scenario (str):</u> "adverse" (the Federal Reserve's severely adverse scenario) or "baseline".
- <u>year (int &#124; None):</u> the Federal Reserve's stress-test year; the latest by default (the ESRB's is always the latest).
- <u>converge_over_years (float):</u> years after the scenario ends over which targets return to calibrated levels.
- <u>follow (str):</u> "path" sets each factor to the published value at every period end within the run, as well as steering its long-run level; "target" only steers the long-run level, a gentler stress.
- <u>equity_regions (Mapping[str, str] &#124; None):</u> equity name -> the published region whose stock-market path it follows; by default every real-world equity follows the United States (Federal Reserve) or the European Union (ESRB). The ESRB also publishes the United States, the United Kingdom, Japan, Canada, Switzerland, Norway, Australia & New Zealand and the rest of the world.

**Returns:**

<u>Regime:</u> a regime with belief paths, for `Scenarios.from_config(config, regime=...)` or `Scenarios.from_profiles(..., regime=...)`.

**Raises:**

- <u>ValueError:</u> if the scenario comes back empty or none of `config`'s factors has a matching country.

**References:**

- Board of Governors of the Federal Reserve System. "Stress test scenarios." <https://www.federalreserve.gov/supervisionreg/dfast-archive.htm>
- European Systemic Risk Board. "EBA EU-wide stress test, macro-financial scenario." <https://www.esrb.europa.eu/mppa/stress/html/index.en.html>
