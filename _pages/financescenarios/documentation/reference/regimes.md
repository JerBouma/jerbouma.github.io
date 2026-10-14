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

Named stress narratives and the official Federal Reserve and ESRB stress scenarios as regimes.

```python
from financescenarios import Regime, RegimeLibrary, load_regime, stress_test_regime
```

## Regime

A named stress regime, such as "Oil Crisis": a story about the economy you can save, share and apply to any run.

A regime works in one or both of two ways:

- `beliefs` change what is simulated, before the run. Each key names a factor and the belief fields to override,
  in the same shape as that factor's `beliefs` section of the configuration. A factor that is one entry of a list
  (interest rates, inflation, equities, FX, credit, ...) is named "<list>.<name>", e.g.
  "inflation.united_states_inflation", or by its own name alone when that name is not also a section.
- `targets` pick, after the run, the scenarios that match the story. Each key names a factor and a (lower, upper)
  quantile range: `us_broad: [0.0, 0.3]` keeps the 30% of scenarios where US stocks earned least, and
  `united_states_short_rate: [0.7, 1.0]` the 30% with the highest average short rate. The dotted form
  ("equities.us_broad") works here too.

A regime needs at least one of the two. The bundled regimes are YAML files in the `regimes/` folder; see
`list_presets(kind="regimes")`, `load_regime` and `RegimeLibrary`, or pass one by name with
`Scenarios.from_profiles(regime=...)`.

**As an example:**

The bundled `oil_crisis.yaml`, description left out:

```yaml
name: Oil Crisis
beliefs:
  inflation.united_states_inflation:
    long_run_mean:
      anchors:
        1.0: 0.12
        3.0: 0.055
        8.0: 0.025
targets:
  united_states_short_rate: [0.7, 1.0]
  us_broad: [0.0, 0.3]
```

It pulls US inflation towards 12% in year one and back to 2.5% by year eight, then keeps the scenarios with high rates
and weak stocks.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
class Regime(BaseModel):
    name: str = Field(min_length=1, description="A short, human-readable label, e.g. 'Oil Crisis'.")
    description: str = Field(default='', description='What this regime represents and why these targets/beliefs were chosen.')
    targets: dict[str, tuple[float, float]] | None = Field(default=None, description="factor name -> (lower, upper) quantile range, same shape as filter_narrative()'s targets.")
    beliefs: dict[str, dict[str, Any]] | None = Field(default=None, description="factor name -> that factor's belief-field overrides, same shape as ScenariosConfig's own beliefs sections.")
    step_range: tuple[int, int] | None = Field(default=None, description="Shared step range for every target, same semantics as filter_narrative()'s step_range.")
    target_mode: Literal['sequential', 'joint'] = Field(default='sequential', description="How targets combine: 'sequential' narrows target by target (each range is a quantile within what the previous targets left), 'joint' ranks every target against the full run and intersects; see ScenarioSet.filter_narrative().")
```

**Attributes:**

- <u>name (str):</u> a short, readable label, e.g. "Oil Crisis".
- <u>description (str):</u> what the regime represents; free text, "" by default.
- <u>targets (dict[str, tuple[float, float]] &#124; None):</u> factor name -> (lower, upper) quantile range, applied after the run; None by default.
- <u>beliefs (dict[str, dict[str, Any]] &#124; None):</u> factor name -> belief overrides, applied before the run; None by default.
- <u>step_range (tuple[int, int] &#124; None):</u> the (start, stop) steps every target is measured over; the whole run by default.
- <u>target_mode (str):</u> "sequential" (default) narrows target by target, each range a quantile of what the previous targets left; "joint" ranks every target against the full run and keeps the scenarios inside all of them.

</details>

## Regime.factor_targets

The targets keyed by each factor's own name, the form a finished run is filtered with.

A target may name one entry of a list of factors either way: "tech" or "equities.tech" (the form beliefs use).
This returns the plain names, so `{"equities.tech": (0.0, 0.25)}` becomes `{"tech": (0.0, 0.25)}`.

**As an example:**

```python
from financescenarios import Regime

Regime(name="Tech Selloff", targets={"equities.tech": (0.0, 0.25)}).factor_targets()
```

Which returns:

```
{'tech': (0.0, 0.25)}
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
factor_targets() -> dict[str, tuple[float, float]]
```

**Returns:**

<u>dict[str, tuple[float, float]]:</u> factor name -> (lower, upper) quantile range; empty without targets.

</details>

## RegimeLibrary

A named collection of regimes: load them from a folder, add your own, and run or apply one by name.

A regime is a stress story such as "Oil Crisis" that works in one or both of two ways. Its `beliefs` change what is
simulated, before the run (inflation heading to 9% within a year, say); its `targets` keep, after the run, only the
scenarios that match the story (the ones with high rates and weak stocks). `build_config` and `simulate` use the
beliefs, `apply` uses the targets. See `Regime` for how each is written.

The two answer different questions. Beliefs ask "what if the economy were different?": they move the factors they
name, and any factor the model ties to them, before a single scenario is drawn. Targets ask "what does the bad part
of the distribution look like?": nothing is changed, only selected, so every kept scenario is one the model
considers plausible. Combined, a regime moves the economy first and then keeps the paths where the story actually
plays out.

| Method | What it does |
|:-------|:-------------|
| `load(directory)` | Read every regime YAML file in a folder (the bundled ones by default). |
| `names`, `get(name)`, `add(regime)` | List, look up, or add or replace a regime. |
| `build_config(base_config, name)` | The configuration with the regime's beliefs applied. |
| `simulate(scenarios, base_config, name)` | Apply the beliefs, simulate and keep the targets, in one call. |
| `apply(scenario_set, name)` | Keep only the scenarios of a finished run that match the targets. |
| `save(directory)` | Write every regime to its own YAML file. |

Every method that takes a `name` accepts the regime's name ("Oil Crisis") or its id ("oil_crisis", the file name
without ".yaml").

**As an example:**

```python
from financescenarios import RegimeLibrary

library = RegimeLibrary.load("regimes")
library.names[:4]
```

Which returns:

```
['Climate Collapse', 'Commodity Supercycle', 'Credit Crunch', 'Currency Crisis']
```

Then `library.apply(result, "Oil Crisis")` narrows a finished run to its high-rate, weak-stock scenarios.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
RegimeLibrary(regimes: dict[str, Regime] | None = None)
```

</details>

## RegimeLibrary.names

The names of every regime currently in this library.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
regimelibrary.names  # property -> list[str]
```

</details>

## RegimeLibrary.add

Add (or replace) a regime in the library, keyed by its own name.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
add(regime: Regime) -> None
```

**Args:**

- <u>regime (Regime):</u> the regime to add.

</details>

## RegimeLibrary.get

Look up one regime by its name or its id.

The name is the label inside the regime ("Oil Crisis"); the id is the file it was loaded from without ".yaml"
("oil_crisis"), or for a regime added by hand, its name in lower case with underscores, the file `save` writes.

**As an example:**

```python
library = RegimeLibrary.load()
library.get("oil_crisis") == library.get("Oil Crisis")
```

Which returns:

```
True
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
get(name: str) -> Regime
```

**Args:**

- <u>name (str):</u> the regime's name, e.g. "Oil Crisis", or its id, e.g. "oil_crisis".

**Returns:**

<u>Regime:</u> the regime with that name or id.

**Raises:**

- <u>KeyError:</u> if no regime has that name or id; the message lists the names available.

</details>

## RegimeLibrary.apply

Keep only the scenarios of a finished run that match a regime's targets.

Each target ranks the scenarios by one factor (a rate by its average, a price by its return) and keeps a quantile
range of them, e.g. (0.0, 0.3) for the worst 30%. Every factor of a kept scenario comes along, so its other
variables show what tends to happen alongside the story: the inflation and credit spreads of the weakest equity
scenarios, say. The result holds only what fits, so fewer scenarios than the run had; `simulate` (or
`Scenarios.simulate(regime=...)`) returns a full set instead.

**As an example:**

```python
library = RegimeLibrary.load("regimes")
oil_crisis = library.apply(result, "Oil Crisis")
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
apply(scenario_set: ScenarioSet, name: str) -> ScenarioSet
```

**Args:**

- <u>scenario_set (ScenarioSet):</u> the run to narrow.
- <u>name (str):</u> the regime's name or id; it must have `targets`.

**Returns:**

<u>ScenarioSet:</u> the scenarios that meet every target.

**Raises:**

- <u>KeyError:</u> if no regime has that name, or a target factor is not in the run.
- <u>ValueError:</u> if the regime has no targets (use `simulate` for a beliefs-only regime), a quantile range is invalid, or no scenario meets every target at once.

</details>

## RegimeLibrary.build_config

Return the configuration with a regime's beliefs applied: the settings that change what gets simulated.

A belief replaces what the calibration would otherwise decide, such as inflation's long-run level heading to 9% in
a year and easing to 2.5% by year eight in "Oil Crisis". Each belief key names a factor: a single factor by its
own name (`real_estate`, `yield_curve`, `mortality`, ...), or one entry of a list of factors as "<list>.<name>",
e.g. "equities.us_broad", or by its own name alone, e.g. "us_broad". A name that is also a section, such as
"inflation", needs the dotted form. Only the belief fields the regime sets change; every other setting stays as
in `base_config`.

**As an example:**

```python
library = RegimeLibrary.load("regimes")
config = library.build_config(base_config, "Oil Crisis")
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
build_config(base_config: ScenariosConfig, name: str) -> ScenariosConfig
```

**Args:**

- <u>base_config (ScenariosConfig):</u> the configuration to start from.
- <u>name (str):</u> the regime's name or id.

**Returns:**

<u>ScenariosConfig:</u> `base_config` with the regime's beliefs applied; unchanged when the regime has none.

**Raises:**

- <u>KeyError:</u> if no regime has that name.
- <u>RegimeMismatchError:</u> (a ValueError) if a belief names a factor or list entry `base_config` does not have, names a list of factors without picking one entry, or uses a name two lists share; the message names the dotted keys to use instead.
- <u>pydantic.ValidationError:</u> if a belief does not fit that factor's beliefs, e.g. an unknown field.

</details>

## RegimeLibrary.simulate

Run a regime from start to finish: apply its beliefs, calibrate and simulate, then keep the scenarios that match
its targets.

The same as `Scenarios.simulate(base_config, regime=name)`: the beliefs change what is simulated, and for a regime
with targets more scenarios are drawn until the configured number fit the story, so a stress run is as large,
and its percentiles as reliable, as a baseline. A regime with only beliefs returns the whole belief-shaped run.

**As an example:**

```python
library = RegimeLibrary.load("regimes")
oil_crisis = library.simulate(scenarios, config, "Oil Crisis")
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

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

**Args:**

- <u>scenarios (Scenarios):</u> the `Scenarios` instance to calibrate and simulate with; one without a regime of its own (or with this same one).
- <u>base_config (ScenariosConfig):</u> the configuration to start from.
- <u>name (str):</u> the regime's name or id.
- <u>mortality_rates (pl.DataFrame &#124; None):</u> your own mortality table; see `Scenarios.calibrate`. Defaults to None.
- <u>mortality_ages (list[float] &#124; None):</u> the ages of that table. Defaults to None.
- <u>mortality_years (list[int] &#124; None):</u> the calendar years of that table. Defaults to None.

**Returns:**

<u>ScenarioSet:</u> the simulated run, narrowed to the regime's targets when it has any.

**Raises:**

- <u>KeyError:</u> if no regime has that name.
- <u>RegimeMismatchError:</u> if a belief or target does not match `base_config` (see `build_config`).
- <u>ValueError:</u> if `scenarios` already carries another regime, or the targets keep no scenario.

</details>

## RegimeLibrary.load

Read every regime in a folder, one YAML file per regime.

A file may start with `extends: <filename>` to build on another regime (see `load_regime`). Use this to list or
pick from everything a folder holds; to load a single regime, `load_regime` reads only the files it needs.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
RegimeLibrary.load(directory: str | Path = 'regimes') -> 'RegimeLibrary'
```

**Args:**

- <u>directory (str &#124; Path):</u> the regimes folder; "regimes" by default, the bundled presets when no such folder exists.

**Returns:**

<u>RegimeLibrary:</u> the regimes, keyed by each regime's `name` and also found by their file id.

**Raises:**

- <u>FileNotFoundError:</u> if the folder does not exist and is not one of the bundled preset folders.

</details>

## RegimeLibrary.save

Write every regime in the library to `directory`, one YAML file each, named after the regime (e.g.
"oil_crisis.yaml" for "Oil Crisis").

The files read back with `load`. Each regime is written in full, so an `extends` link it was loaded with is not
kept.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
save(directory: str | Path) -> None
```

**Args:**

- <u>directory (str &#124; Path):</u> the folder to write into, created if missing.

</details>

## load_regime

Load one regime by its id or its name, from your own `regimes/` folder or the bundled ones.

A regime is named two ways: its id is the file name ("oil_crisis") and its name is the label inside it ("Oil
Crisis"). Either works. Called with one argument, the regime is looked up the way `Scenarios.from_profiles` does
it: in a `regimes/` folder when you have one (from `scaffold_project()`), in the bundled regimes otherwise. Called
with two, the first is the folder to read.

A regime file may start with `extends: <filename>` to build on another regime: that chain is followed and merged,
with the file's own fields winning. Use `RegimeLibrary.load` instead to read every regime in a folder at once.

**As an example:**

```python
from financescenarios import load_regime

regime = load_regime("oil_crisis")  # the same as load_regime("regimes", "Oil Crisis")
regime.name, regime.targets
```

Which returns:

```
('Oil Crisis', {'united_states_short_rate': (0.7, 1.0), 'us_broad': (0.0, 0.3)})
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
load_regime(directory: str | Path, filename: str | None = None) -> Regime
```

**Args:**

- <u>directory (str &#124; Path):</u> the regimes folder, e.g. "regimes"; or, when `filename` is left out, the regime's id or name.
- <u>filename (str &#124; None):</u> the regime's id, e.g. "oil_crisis" (".yaml" optional), or its name, e.g. "Oil Crisis". Defaults to None, which reads the regime named by `directory` from the "regimes" folder.

**Returns:**

<u>Regime:</u> the regime, with its `extends` chain merged in.

**Raises:**

- <u>FileNotFoundError:</u> if no regime has that id or name, or a file it extends does not exist.
- <u>ValueError:</u> if the `extends` chain loops back on itself or never sets `name`.
- <u>pydantic.ValidationError:</u> if the merged fields do not form a valid regime.

</details>

## stress_test_regime

Turn a regulator's published stress-test scenario into a regime that steers your scenarios through it.

Instead of writing a recession by hand, this takes the one the Federal Reserve or the European Systemic Risk Board
prescribes for banks' stress tests and lets the simulated scenarios follow it, each with its own randomness. Its
paths for interest rates, inflation and unemployment steer the matching factors of `config` through the stress
and back to their calibrated levels; stocks follow as falls and recoveries, measured against each regulator's
own baseline so the equity model's normal growth is not counted twice. The Federal Reserve's 2026 severely adverse
scenario, for example, takes US stocks 59% below its baseline after three quarters and 56% below after a year
("Equity prices fall about 58 percent in the first three quarters of the scenario", 2026 Final Scenarios, p. 4).
The ESRB's stocks are published as a "Deviation from the starting point (%)", with "stock prices ... assumed to
remain unchanged" in its baseline (2025 scenario, section 4.1.7), so that deviation is already the gap to its
baseline: -50% for the EU in 2025 and -42% by 2027.

The value is in running your own portfolio or balance sheet through the same story supervisors use: the published
scenario is one narrative path, and laying it over simulated scenarios turns it into a distribution around that
narrative, so you see both the stressed outcome and how much worse it could get within the stress. Each
regulator publishes two scenarios, a stress and its own central view ("baseline"), a useful reference to measure
the stress against. Both come through the Finance Toolkit, with no API key:

- "federal_reserve": "baseline" and "severely_adverse", the two scenarios the Federal Reserve's scenario
  documents have contained since 2020 (their section "Baseline and Severely Adverse Scenarios", in the 2020
  Supervisory Scenarios and on p. 8 of the final 2026 scenarios), for the United States, quarterly over 13 quarters:
  the 3-month and 10-year Treasury rates, inflation, unemployment and stocks. "adverse" is accepted as the same
  severely adverse scenario.
- "esrb": "baseline" and "adverse", the scenarios the ESRB designs for the EBA's EU-wide stress test ("This
  document presents the baseline and adverse macro-financial scenarios that banks are required to use", ESRB
  2025 scenario, p. 1), yearly over three years for every EU member and the main other economies: the long-term
  interest rate, inflation, unemployment and stocks. The ESRB publishes no "severely_adverse" scenario.

**As an example:**

```python
from financescenarios import Scenarios, stress_test_regime

regime = stress_test_regime(toolkit, config, authority="federal_reserve", scenario="severely_adverse")
scenarios = Scenarios.from_config(config, regime=regime)
```

**References:**

- Board of Governors of the Federal Reserve System. "Stress test scenarios." <https://www.federalreserve.gov/supervisionreg/dfast-archive.htm>
- Board of Governors of the Federal Reserve System (2020). "2020 Supervisory Scenarios for Annual Stress Tests." <https://www.federalreserve.gov/newsevents/pressreleases/files/bcreg20200206a1.pdf>
- Board of Governors of the Federal Reserve System (2026). "2026 Final Supervisory Stress Test Scenarios." <https://www.federalreserve.gov/publications/files/2026-final-supervisory-stress-test-scenarios-20260204.pdf>
- European Systemic Risk Board (2025). "Macro-financial scenario for the 2025 EU-wide banking sector stress test." <https://www.eba.europa.eu/sites/default/files/2025-02/f23c8470-a2e1-410f-b752-55aff8f8e8f4/2025-02-26%20-%20ESRB%20-%20Macrofinancial%20scenario%20for%20the%202025%20EU-wide%20banking%20sector%20stress%20test%20%28updated%2026%20February%202025%29.pdf>
- European Systemic Risk Board. "EBA EU-wide stress test, macro-financial scenario." <https://www.esrb.europa.eu/mppa/stress/html/index.en.html>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
stress_test_regime(
    toolkit: Toolkit,
    config: ScenariosConfig,
    authority: Literal['federal_reserve', 'esrb'] = 'federal_reserve',
    scenario: Literal['baseline', 'adverse', 'severely_adverse'] = 'adverse',
    year: int | None = None,
    converge_over_years: float = 5.0,
    follow: Literal['path', 'target'] = 'path',
    equity_regions: Mapping[str, str] | None = None,
) -> Regime
```

**Args:**

- <u>toolkit (Toolkit):</u> the Finance Toolkit `Toolkit`.
- <u>config (ScenariosConfig):</u> the configuration; each entry follows its own `country`.
- <u>authority (str):</u> "federal_reserve" (default) or "esrb".
- <u>scenario (str):</u> "severely_adverse" (Federal Reserve), "adverse" (ESRB; the severely adverse one for the Federal Reserve) or "baseline". Defaults to "adverse", the stress of either authority.
- <u>year (int &#124; None):</u> the Federal Reserve's stress-test year; the latest by default.
- <u>converge_over_years (float):</u> the years after the scenario over which each factor returns to its calibrated level; 5.0 by default. Neither regulator publishes a path past its horizon (13 quarters, three years), so this is a judgement: about the length of a full recovery, during which the stress fades linearly.
- <u>follow (str):</u> "path" (default) also sets each factor to the published value at every period end, as the regulators prescribe the path itself; "target" only steers its long-run level, a gentler stress.
- <u>equity_regions (Mapping[str, str] &#124; None):</u> equity name -> the published region whose stocks it follows; the United States (Federal Reserve) or European Union (ESRB) by default.

**Returns:**

<u>Regime:</u> the stress as belief paths, for `Scenarios.from_config(config, regime=...)`.

**Raises:**

- <u>ValueError:</u> if the authority does not publish the scenario, it comes back empty or none of `config`'s factors has a matching country.

</details>
