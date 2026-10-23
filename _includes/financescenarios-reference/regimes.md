## Reference

The reference is generated from the docstrings in the package, so it says what `help(...)` says in Python: what each class and function does, a worked example with real output where the docstring has one, and the arguments and return value folded underneath.

Everything on this page imports as follows:

```python
from financescenarios import Regime, RegimeLibrary, Shock, load_regime, search_regimes, shock_regime, stress_test_regime
```

### Regime

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
`Scenarios.from_profiles(regime=...)`. `category` and `keywords` make a regime easy to find with `search_regimes`
("stagflation" finds the 1970s regimes); they change nothing in a run.

**As an example:**

The bundled `oil_crisis.yaml`, description left out:

```yaml
# my-project/regimes/oil_crisis.yaml (a stress regime)
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
    category: str | None = Field(default=None, description="The kind of story, e.g. 'inflation', 'recession' or 'currency', for search.")
    keywords: list[str] = Field(default_factory=list, description="Words a search should find this regime by, e.g. ['stagflation', '1970s'].")
    targets: dict[str, tuple[float, float]] | None = Field(default=None, description="factor name -> (lower, upper) quantile range, same shape as filter_narrative()'s targets.")
    beliefs: dict[str, dict[str, Any]] | None = Field(default=None, description="factor name -> that factor's belief-field overrides, same shape as ScenariosConfig's own beliefs sections.")
    step_range: tuple[int, int] | None = Field(default=None, description="Shared step range for every target, same semantics as filter_narrative()'s step_range.")
    target_mode: Literal['sequential', 'joint'] = Field(default='sequential', description="How targets combine: 'sequential' narrows target by target (each range is a quantile within what the previous targets left), 'joint' ranks every target against the full run and intersects; see ScenarioSet.filter_narrative().")
```

**Attributes:**

- <u>name (str):</u> a short, readable label, e.g. "Oil Crisis".
- <u>description (str):</u> what the regime represents; free text, "" by default.
- <u>category (str &#124; None):</u> the kind of story, e.g. "inflation", "recession", "crash", "currency" or "housing"; None by default.
- <u>keywords (list[str]):</u> words a search should find the regime by, e.g. ["stagflation", "1970s"]; empty by default.
- <u>targets (dict[str, tuple[float, float]] &#124; None):</u> factor name -> (lower, upper) quantile range, applied after the run; None by default.
- <u>beliefs (dict[str, dict[str, Any]] &#124; None):</u> factor name -> belief overrides, applied before the run; None by default.
- <u>step_range (tuple[int, int] &#124; None):</u> the (start, stop) steps every target is measured over; the whole run by default.
- <u>target_mode (str):</u> "sequential" (default) narrows target by target, each range a quantile of what the previous targets left; "joint" ranks every target against the full run and keeps the scenarios inside all of them.

</details>

#### Regime.factor_targets

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

### RegimeLibrary

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
| `search(query)` | The regimes that match a few words, such as "high inflation", best first. |
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

#### RegimeLibrary.names

The names of every regime currently in this library.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
regimelibrary.names  # property -> list[str]
```

</details>

#### RegimeLibrary.add

Add (or replace) a regime in the library, keyed by its own name.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
add(regime: Regime) -> None
```

**Args:**

- <u>regime (Regime):</u> the regime to add.

</details>

#### RegimeLibrary.get

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

#### RegimeLibrary.ids

Each regime's id -> its name: the file it was loaded from without ".yaml", or for a regime added by hand,
its name in lower case with underscores (the file `save` writes).

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
regimelibrary.ids  # property -> dict[str, str]
```

</details>

#### RegimeLibrary.search

Find the regimes that match a few words, best match first, the way you would ask for one: "high inflation",
"1970s stagflation", "euro crisis" or "housing crash".

Each word of the query is looked up in a regime's name and keywords (which count most), its id and category,
and its description. Case and accents do not matter, common words such as "what", "if" and "the" are skipped,
and a word of four letters or more also matches the start of a longer one, so "inflationary" finds the
inflation regimes. A regime that matches more of the words ranks higher, a whole word above a partial one;
one whose name or a keyword holds the whole query in order ranks higher still.

**As an example:**

```python
from financescenarios import RegimeLibrary

RegimeLibrary.load().search("oil", limit=3)
```

Which returns (without the 'keywords' and 'description' columns):

| id                | name                       | category    | score |
|:------------------|:---------------------------|:------------|------:|
| oil_collapse_2014 | Oil Price Collapse 2014-16 | commodities |   5.5 |
| oil_crisis        | Oil Crisis                 | inflation   |   5.0 |
| oil_shock         | Oil Shock                  | inflation   |   5.0 |

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
search(query: str, category: str | None = None, limit: int | None = None) -> pl.DataFrame
```

**Args:**

- <u>query (str):</u> the words to search for; "" lists every regime.
- <u>category (str &#124; None):</u> keep only this kind of regime, e.g. "inflation", "recession", "crash", "currency", "commodities", "housing" or "rates". Defaults to None, every category.
- <u>limit (int &#124; None):</u> the most rows to return. Defaults to None, every match.

**Returns:**

<u>pl.DataFrame:</u> one row per matching regime, best first: 'id' (to pass to `simulate(regime=...)`), 'name', 'category', 'keywords' (comma-separated), 'description' and 'score' (higher is a better match).

</details>

#### RegimeLibrary.apply

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

#### RegimeLibrary.build_config

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

#### RegimeLibrary.simulate

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

#### RegimeLibrary.load

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

#### RegimeLibrary.save

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

### Shock

A one-off jump in a factor's level at a given year, such as "+2% on the short rate in year 3".

Unlike a `BeliefPath`, which moves where the factor is heading, a shock moves where it is: the factor jumps once,
then its own dynamics take over, so a mean-reverting factor drifts back from the shocked level at its fitted speed.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
class Shock(BaseModel):
    year: float = Field(ge=0, description='Simulated year the shock lands on.')
    magnitude: float = Field(allow_inf_nan=False, description='Shock size: added (additive) or set (absolute).')
    mode: Literal['additive', 'absolute'] = Field(default='additive', description="'additive' adds magnitude to the step's value; 'absolute' replaces it.")
```

**Attributes:**

- <u>year (float):</u> the year the shock lands, at the nearest simulated date.
- <u>magnitude (float):</u> the size of the jump, or the level to jump to with mode "absolute".
- <u>mode (str):</u> "additive" (default) adds `magnitude` to the simulated value; "absolute" sets the value to it.

</details>

### load_regime

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

### search_regimes

Find the stress regimes that match a few words, best match first: "high inflation", "1970s stagflation", "euro
crisis", "housing crash".

A regime is a ready-made story about the economy, such as the 1970s stagflation or the 2008 financial crisis, that
`simulate(regime=...)` runs your scenarios through. With dozens bundled, searching is quicker than reading the whole
list: each query word is looked up in a regime's name and keywords (which count most), its id and category, and its
description, ignoring case, accents and common words, and the regimes that match the most words come first. This is
`RegimeLibrary.load(directory).search(...)` in one call.

**As an example:**

```python
from financescenarios import search_regimes

search_regimes("stagflation", limit=2)
```

Which returns (without the 'keywords' and 'description' columns):

| id                | name              | category  | score |
|:------------------|:------------------|:----------|------:|
| stagflation_1970s | 1970s Stagflation | inflation |   5.0 |
| oil_crisis        | Oil Crisis        | inflation |   3.0 |

Then pass the best match's id on: `scenarios.simulate(regime="stagflation_1970s")`.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
search_regimes(
    query: str,
    directory: str | Path = 'regimes',
    category: str | None = None,
    limit: int | None = None,
) -> pl.DataFrame
```

**Args:**

- <u>query (str):</u> the words to search for; "" lists every regime.
- <u>directory (str &#124; Path):</u> the regimes folder; "regimes" by default, the bundled regimes when you have no such folder of your own.
- <u>category (str &#124; None):</u> keep only this kind of regime, e.g. "inflation", "recession", "crash", "currency", "commodities", "housing" or "rates". Defaults to None, every category.
- <u>limit (int &#124; None):</u> the most rows to return. Defaults to None, every match.

**Returns:**

<u>pl.DataFrame:</u> one row per matching regime, best first: 'id' (to pass to `simulate(regime=...)`), 'name', 'category', 'keywords', 'description' and 'score'.

**Raises:**

- <u>FileNotFoundError:</u> if `directory` does not exist and is not the bundled regimes folder.
- <u>ValueError:</u> if `limit` is not a positive whole number.

</details>

### shock_regime

Build a one-factor what-if as a regime: "what if inflation hit 8% within a year?", "what if stocks fell 30%?",
"what if the euro lost 20% against the dollar?".

A named regime tells a whole story; this answers the quicker question of one factor moving. The factor's expected
path heads in a straight line to `level` by `peak_year` and back onto its usual path by `normal_by_year`, while
every scenario keeps its own randomness. Name it in plain words ("inflation", "short rate", "long rate",
"unemployment", "stocks", "oil", "gold", "house prices", "credit spreads", "euro", "yen", "dollar") or by its
factor name, such as "eurozone_long_rate". `level` is an annual decimal for rates, inflation, unemployment,
house-price growth and credit spreads (0.08 for 8%), the change against the usual path for stocks, oil and gold
(-0.3 for 30% lower), and the change in a currency's dollar value (-0.2 for a euro 20% weaker).

Mean-reverting factors get a moving long-run level (a `BeliefPath`) that the factor's own reversion speed turns
into exactly that expected path, given the `calibration` the regime runs on; without one, every scenario is set to
`level` at `peak_year` and eases back at its own pace. Prices move by one log-return jump per step, as
`stress_test_regime` lays a regulator's stock-market path over a run. Both replay on a saved calibration. Factors
tied to the shocked one follow it, such as unemployment through its Phillips curve; the correlations act on the
random draws instead, so `tail` keeps the scenarios where the factor ran furthest to show what tends to come with
the move.

**As an example:**

```python
from financescenarios import Scenarios, shock_regime

scenarios = Scenarios.from_profiles(api_key="FINANCIAL_MODELING_PREP_KEY")
baseline = scenarios.simulate(n_simulations=2000, seed=42)
calibration = scenarios.last_calibration
regime = shock_regime("inflation", 0.08, calibration=calibration)
shocked = scenarios.simulate(regime=regime, calibration=calibration, n_simulations=2000, seed=42)
```

On the calibration of 2026-10-19 of the default set, the median US inflation is 7.6% one year in (the mean 7.9%)
against 2.7% in the baseline, 4.7% after three years against 2.0%, and back on the baseline's 1.8% after five. The
US short rate follows through its policy rule, to a median of 6.2% after one year and 8.6% after two against the
baseline's 4.3% and 4.4%, while US unemployment barely moves in the first year (4.2% against 4.3%) and ends higher
(5.7% against 5.2% after five years).

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
shock_regime(
    factor: str,
    level: float,
    peak_year: float = 1.0,
    normal_by_year: float | None = 5.0,
    country: str = 'United States',
    factor_set: str | ScenariosConfig = 'default',
    calibration: CalibrationResult | None = None,
    tail: tuple[float, float] | None = None,
    targets: Mapping[str, tuple[float, float]] | None = None,
    years: float | None = None,
    name: str | None = None,
) -> Regime
```

**Args:**

- <u>factor (str):</u> what to shock, in plain words or by its factor name, e.g. "inflation", "stocks" or "euro".
- <u>level (float):</u> where it goes, in the units above, e.g. 0.08 or -0.3.
- <u>peak_year (float):</u> when it gets there, in years. Defaults to 1.0.
- <u>normal_by_year (float &#124; None):</u> when it is back to normal, in years; None keeps the shock. Defaults to 5.0.
- <u>country (str):</u> the country for inflation, rates, unemployment and stocks; "US" or "UK" work too. Defaults to "United States".
- <u>factor_set (str &#124; ScenariosConfig):</u> the factor set it runs on, by id or as a configuration. Defaults to "default".
- <u>calibration (CalibrationResult &#124; None):</u> the calibration it runs on. Defaults to None.
- <u>tail (tuple[float, float] &#124; None):</u> a quantile range of the shocked factor to keep, e.g. (0.7, 1.0). Defaults to None, every scenario.
- <u>targets (Mapping[str, tuple[float, float]] &#124; None):</u> quantile ranges of other factors to keep. Defaults to None.
- <u>years (float &#124; None):</u> the horizon it runs over; jumps past it are left out. Defaults to None, the factor set's.
- <u>name (str &#124; None):</u> the regime's name. Defaults to None, one made from the shock.

**Returns:**

<u>Regime:</u> the what-if, for `scenarios.simulate(regime=...)`.

**Raises:**

- <u>ValueError:</u> if the factor means nothing in the factor set (the closest names are suggested), its model takes no shock, or a number is out of range.

</details>

### stress_test_regime

Turn a regulator's published stress-test scenario into a regime that steers your scenarios through it.

Instead of writing a recession by hand, this takes the one the Federal Reserve or the European Systemic Risk Board
prescribes for banks' stress tests and lets the simulated scenarios follow it, each with its own randomness. Its
paths for interest rates, inflation and unemployment steer the matching factors of `config` through the stress and
back to their calibrated levels; stocks follow as falls and recoveries, measured against each regulator's own
baseline so the equity model's normal growth is not counted twice. In the Federal Reserve's 2026 severely adverse
scenario, for example, equity prices fall about 58% in the first three quarters (Federal Reserve (2026, p. 4)), a fall
from their starting level; against the Fed's own baseline, which keeps rising, that is 59% below it after three
quarters and 56% below after a year, the falls the regime uses. The ESRB's stocks are published as a percentage
deviation from the starting point, with stock prices unchanged in its baseline (ESRB (2025, section 4.1.7)), so
that deviation is already the gap to its baseline: -50% for the EU in 2025 and -42% by 2027.

The value is in running your own portfolio or balance sheet through the same story supervisors use: the published
scenario is one narrative path, and laying it over simulated scenarios turns it into a distribution around that
narrative, so you see both the stressed outcome and how much worse it could get within the stress. Each
regulator publishes two scenarios, a stress and its own central view ("baseline"), a useful reference to measure
the stress against. Both come through the Finance Toolkit, with no API key:

- "federal_reserve": "baseline" and "severely_adverse", the two scenarios the Federal Reserve's scenario documents
  have contained since 2020 (their section Baseline and Severely Adverse Scenarios, in the 2020 Supervisory
  Scenarios and on p. 8 of the final 2026 scenarios), for the United States, quarterly over 13 quarters: the 3-month
  and 10-year Treasury rates, inflation, unemployment and stocks. "adverse" is accepted as the same severely adverse
  scenario.
- "esrb": "baseline" and "adverse", the scenarios the ESRB designs for the EBA's EU-wide stress test, the two
  macro-financial scenarios banks are required to use (ESRB 2025 scenario, p. 1), yearly over three years for every
  EU member and the main other economies: the long-term interest rate, inflation, unemployment and stocks. The ESRB
  publishes no "severely_adverse" scenario.

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
