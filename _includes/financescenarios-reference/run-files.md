## Reference

The reference is generated from the docstrings in the package, so it says what `help(...)` says in Python: what each class and function does, a worked example with real output where the docstring has one, and the arguments and return value folded underneath.

Everything on this page imports as follows:

```python
from financescenarios import write_run, read_run, read_run_calibration, publish_calibration, load_release, simulate_release, Snapshot, ResultCache, ScenarioSummary
from financescenarios.reporting.reporting_controller import Reporting
```

### Run Files

#### write_run

Save a run to disk, so it can be read back later without calibrating or simulating again.

Everything goes into one folder, `<output_dir>/<run_id>/`:

- `config.yaml` (run settings: start date, engine, toolkit, reporting) and `factors.yaml` (every factor
  definition): the configuration that produced the run, split the way `load_config` reads it back.
- One file per factor, `<factor>.parquet` or `<factor>.csv`, with one row per scenario and one column per date.
- `manifest.json`: the run id, creation time, regime, factor names and categories, number of scenarios, seed and any
  warnings, small enough to list many runs without opening a factor file.
- `calibration.json`, only when `calibration` is given, so the run can be simulated again offline (see
  `read_run_calibration`).

`Scenarios.save(result)` calls this for you, into "results/".

**As an example:**

```python
from financescenarios import read_run, write_run

run_id = write_run(result, config, "results", calibration=calibration)
reloaded = read_run(f"results/{run_id}")
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
write_run(
    result: ScenarioSet,
    config: ScenariosConfig,
    output_dir: str | Path,
    regime: str | None = None,
    output_format: str = 'parquet',
    run_id: str | None = None,
    warnings: list[str] | None = None,
    correlation_fallback_pairs: list[str] | None = None,
    calibration_failures: dict[str, str] | None = None,
    calibration: 'CalibrationResult | None' = None,
) -> str
```

**Args:**

- <u>result (ScenarioSet):</u> the run to save.
- <u>config (ScenariosConfig):</u> the configuration that produced it, after any regime beliefs were applied.
- <u>output_dir (str &#124; Path):</u> the runs folder; the run gets its own subfolder.
- <u>regime (str &#124; None):</u> the name of the regime applied, recorded for display; None by default.
- <u>output_format (str):</u> "parquet" (default; smaller and faster to read back) or "csv".
- <u>run_id (str &#124; None):</u> the run's folder name; a UTC timestamp plus a short random suffix by default.
- <u>warnings (list[str] &#124; None):</u> warnings the run produced, kept so they can be read back later; none by default.
- <u>correlation_fallback_pairs (list[str] &#124; None):</u> "factor_a/factor_b" pairs whose correlation was set to 0 for lack of overlapping history; none by default.
- <u>calibration_failures (dict[str, str] &#124; None):</u> factor name -> why its calibration failed and it was left out; none by default.
- <u>calibration (CalibrationResult &#124; None):</u> the calibration the run came from, saved as `calibration.json`; not saved by default.

**Returns:**

<u>str:</u> the run id used.

**Raises:**

- <u>ValueError:</u> if `output_format` is not "parquet" or "csv", or `run_id` is not a plain folder name.

</details>

#### read_run

Read a saved run back into a `ScenarioSet`, without calibrating or simulating anything.

The run comes back with the same paths, dates, time grid, number of scenarios and seed, so `describe()`,
`filter()`, `to_dataframe()` and portfolios work on it exactly as on the original. The fitted parameters are not
stored with the paths, so `diagnose()`, which needs them, does not work on a reloaded run; to simulate again from
the same fit, use `read_run_calibration`.

**As an example:**

```python
from financescenarios import read_run

result = read_run("results/20260819T063851Z-7bfdde41")
result.describe()
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
read_run(run_dir: str | Path) -> ScenarioSet
```

**Args:**

- <u>run_dir (str &#124; Path):</u> the run's own folder, `<output_dir>/<run_id>`.

**Returns:**

<u>ScenarioSet:</u> the reloaded run.

**Raises:**

- <u>FileNotFoundError:</u> if the folder has no `manifest.json`, or misses a factor file the manifest lists.

</details>

#### read_run_calibration

Read back the calibration a run was simulated from, so it can be simulated again offline.

This replays a run without any data download or API key: the same fitted parameters, at a new seed or with more
scenarios. It works for a run saved with its calibration, `write_run(..., calibration=...)`.

**As an example:**

```python
from financescenarios import Scenarios, read_run_calibration

calibration = read_run_calibration("results/20260819T063851Z-7bfdde41")
wider = Scenarios(toolkit=None, n_simulations=20_000).simulate(config, calibration=calibration)
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
read_run_calibration(run_dir: str | Path) -> 'CalibrationResult | None'
```

**Args:**

- <u>run_dir (str &#124; Path):</u> the run's own folder, `<output_dir>/<run_id>`.

**Returns:**

<u>CalibrationResult &#124; None:</u> the stored calibration, or None for a run saved without one.

</details>

### Releases

#### publish_calibration

Calibrate from named profiles and publish the result as a versioned release, checked and with a report.

A calibration is what the model learnt from history. Publishing one fixes it under a version tag, so every later run
can name exactly which one it used and get the same scenarios. Before it is published it is checked: every factor
calibrated, the parameters are plausible, the correlations are valid and reproduced by the simulation, each factor
swings about as much as its history did, and the run is reproducible. Each check passes, warns or fails, and the
worst one sets the release's status.

The release folder `<output_dir>/<release_version>/` holds:

- `calibration.json`: the calibration, for `simulate(calibration=...)` or `simulate_release`.
- `manifest.json`: the version, date, profiles, a fingerprint (SHA-256 hash) of the full configuration, the package
  versions and the data window.
- `checks.json` and `report.md`: every check's status, numbers and explanation, and the fitted parameters.

**As an example:**

```python
from financescenarios import publish_calibration

release = publish_calibration(factor_set="default")
release.manifest.status, release.directory
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
publish_calibration(
    output_dir: str | Path = 'calibrations',
    release_version: str | None = None,
    settings: str = 'default',
    factor_set: str = 'default',
    settings_dir: str | Path = 'settings',
    factor_sets_dir: str | Path = 'factor-sets',
    n_simulations: int = 1000,
    toolkit: Toolkit | None = None,
    subfolder: str | None = None,
) -> ReleaseResult
```

**Args:**

- <u>output_dir (str &#124; Path):</u> where releases are kept; "calibrations" by default.
- <u>release_version (str &#124; None):</u> the version tag; today's date as "YYYY.MM.DD" by default.
- <u>settings (str):</u> the settings profile to calibrate with; "default" by default.
- <u>factor_set (str):</u> the factor set to calibrate; "default" by default.
- <u>settings_dir (str &#124; Path):</u> where the settings profiles live; the bundled presets when "settings" does not exist.
- <u>factor_sets_dir (str &#124; Path):</u> where the factor sets live; the bundled presets when "factor-sets" does not exist.
- <u>n_simulations (int):</u> the size of the two seeded runs the checks simulate; 1000 by default.
- <u>toolkit (Toolkit &#124; None):</u> a ready-made Finance Toolkit `Toolkit`; built from the settings by default.
- <u>subfolder (str &#124; None):</u> write to `<output_dir>/<release_version>/<subfolder>/` instead, so several factor sets can share one version; None by default.

**Returns:**

<u>ReleaseResult:</u> the release `directory`, its `manifest` (with the overall `status`) and every check.

**Raises:**

- <u>FileExistsError:</u> if that version was already published, since a release must never change afterwards.

</details>

#### load_release

Read a published calibration and its manifest from a release folder, ready for `simulate(calibration=...)`.

**As an example:**

```python
from financescenarios import load_release

calibration, manifest = load_release("calibrations/2027.01.01")
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
load_release(directory: str | Path) -> tuple[CalibrationResult, ReleaseManifest]
```

**Args:**

- <u>directory (str &#124; Path):</u> the release folder, e.g. what `publish_calibration` wrote or `download_release` returns.

**Returns:**

<u>tuple[CalibrationResult, ReleaseManifest]:</u> the calibration, and the manifest that identifies it (version, date, profiles and status).

</details>

#### simulate_release

Simulate from a published calibration without fetching any data.

The release's own settings profile and factor set give the run (steps, frequency, number of scenarios, seed), and
its calibration replaces the fit, so the scenarios match anyone else's run from the same release. The profiles must
still be the ones the release was calibrated with: a changed profile would describe different factors than the
calibration holds.

**As an example:**

```python
from financescenarios import simulate_release

result = simulate_release("calibrations/2027.01.01", n_simulations=500)
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
simulate_release(
    directory: str | Path,
    settings_dir: str | Path = 'settings',
    factor_sets_dir: str | Path = 'factor-sets',
    n_simulations: int | None = None,
    seed: int | None = None,
) -> ScenarioSet
```

**Args:**

- <u>directory (str &#124; Path):</u> the release folder, e.g. what `download_release` returns.
- <u>settings_dir (str &#124; Path):</u> where the release's settings profile lives; the bundled presets when "settings" does not exist.
- <u>factor_sets_dir (str &#124; Path):</u> where its factor set lives; the bundled presets when "factor-sets" does not exist.
- <u>n_simulations (int &#124; None):</u> the number of scenarios; the settings profile's by default.
- <u>seed (int &#124; None):</u> the random seed; the settings profile's by default.

**Returns:**

<u>ScenarioSet:</u> the simulated scenarios.

**Raises:**

- <u>ValueError:</u> if the profiles changed since the release was published.

</details>

### Snapshot

A factor set calibrated as of one month and kept on disk, so every later run replays it in seconds, without
downloading data or fitting anything.

Calibrating fetches decades of prices and rates and fits every factor, which takes minutes and an API key.
Doing it once a month and reusing the fit answers every question that month from the same economics: two people
asking about the same regime with the same seed get the same scenarios, and the answer is reproducible later.

A snapshot folder, `<root>/<YYYY-MM>/<settings>__<factor_set>/`, holds the calibration (`calibration.json`, see
`CalibrationResult.save`), the configuration it runs (`config.json`), every factor's realised monthly history
(`history.parquet`, the series `Scenarios.history` reads) and `meta.json` (see `SnapshotMeta`). Every run starts
on the first day of its month. Building writes into a hidden folder renamed into place once complete, under a file
lock, so concurrent builders never build twice or leave half a snapshot.

| Method | What it does |
|:-------|:-------------|
| `Snapshot.build(...)` | calibrates and stores this month's snapshot, or returns it when it exists |
| `Snapshot.load(...)`, `Snapshot.latest(...)` | reads a month's snapshot, or the newest one |
| `simulate(...)` | replays the calibration: any number of scenarios, seed, horizon or regime |
| `summary(...)` | the same run reduced to yearly percentiles, cached when given a `ResultCache` |
| `history`, `changes()`, `history_set()` | the realised history, its monthly moves, or a backtest-ready run |
| `Snapshot.prune(keep_months=2)` | deletes all but the newest snapshots of each profile pair |

**As an example:**

```python
from financescenarios import Snapshot

snapshot = Snapshot.build(api_key="FINANCIAL_MODELING_PREP_KEY")  # once a month; a no-op once built
result = Snapshot.load().simulate(n_simulations=1000, seed=7, years=10, regime="oil_crisis")
result.horizon_summary([1, 5, 10], factors=["us_broad", "united_states_inflation"])
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
Snapshot(
    directory: str | Path,
    meta: SnapshotMeta,
    calibration: CalibrationResult | None = None,
    config: ScenariosConfig | None = None,
    history: pl.DataFrame | None = None,
)
```

</details>

#### Snapshot.id

The snapshot's id, "<YYYY-MM>/<settings>__<factor_set>".

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
snapshot.id  # property -> str
```

</details>

#### Snapshot.as_of

The month it was calibrated for, "YYYY-MM".

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
snapshot.as_of  # property -> str
```

</details>

#### Snapshot.meta

What identifies the snapshot and how it was made; see `SnapshotMeta`.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
snapshot.meta  # property -> SnapshotMeta
```

</details>

#### Snapshot.directory

The snapshot's folder.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
snapshot.directory  # property -> Path
```

</details>

#### Snapshot.calibration

The stored calibration, what every replay simulates from.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
snapshot.calibration  # property -> CalibrationResult
```

</details>

#### Snapshot.config

The configuration every replay runs: the profiles as they were when it was built, starting in its month.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
snapshot.config  # property -> ScenariosConfig
```

</details>

#### Snapshot.history

Every factor's realised history, one row per factor and month: "date" (the month's first day), "factor",
"category" and "value" (the month's last reading, in the factor's own units). Each factor keeps its own window,
and the snapshot's own month holds the readings so far, so drop it when only complete months will do.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
snapshot.history  # property -> pl.DataFrame
```

</details>

#### Snapshot.build

Calibrate a factor set as of a month and store it as a snapshot, or return the snapshot when it already exists.

This is the only step that downloads data. It fits every factor (see `Scenarios.calibrate`), fetches each
factor's history (see `fetch_historical_data`) and writes both, with the configuration and `meta.json`, into
`<root>/<as_of>/<settings>__<factor_set>/`. Every run starts on the first day of `as_of`, and a past month is
built with that month's end as the Toolkit's end date. Two builders of the same snapshot, in threads or
processes, build it once: the second waits for the first and reads its result. A factor whose history cannot be
fetched is left out of the history and listed in `meta.history_failures`, rather than failing the build.

Most regimes replay from the snapshot's own calibration. One that fixes a fitted parameter, such as
`tech_selloff`'s equity regime means, needs a calibration of its own: `regimes="refit"` makes one for every
regime of `regimes_dir` that needs it and fits this factor set, from the data already fetched, and stores it
in `regimes/<regime>/`, so `simulate(regime=...)` replays those offline too. Each costs about one more
calibration: the broad factor set's three took its build from 12 to 46 seconds and added 200 kB each.

Once the Finance Toolkit's cache holds the data, the default factor set builds in about 20 seconds (27
factors, 2026-10-17) into a 110 kB folder.

**As an example:**

```python
from financescenarios import Snapshot

snapshot = Snapshot.build(settings="default", factor_set="default", api_key="FINANCIAL_MODELING_PREP_KEY")
snapshot.meta.build_seconds, snapshot.meta.factor_names[:3]
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
Snapshot.build(
    settings: str = 'default',
    factor_set: str = 'default',
    as_of: str | None = None,
    root: str | Path | None = None,
    api_key: str | None = None,
    fred_api_key: str | None = None,
    toolkit: Toolkit | None = None,
    settings_dir: str | Path = 'settings',
    factor_sets_dir: str | Path = 'factor-sets',
    regimes: str | Sequence[str | Regime] | None = None,
    regimes_dir: str | Path = 'regimes',
    rebuild: bool = False,
    lock_timeout: float = _LOCK_TIMEOUT_SECONDS,
) -> Snapshot
```

**Args:**

- <u>settings (str):</u> the settings profile; "default" by default.
- <u>factor_set (str):</u> the factor set; "default" by default.
- <u>as_of (str &#124; None):</u> the month, "YYYY-MM"; the current month by default.
- <u>root (str &#124; Path &#124; None):</u> where snapshots are kept; `<cache_dir()>/snapshots` by default, set by FINANCESCENARIOS_CACHE_DIR.
- <u>api_key (str &#124; None):</u> a FinancialModelingPrep key (https://www.jeroenbouma.com/fmp); read from FINANCIAL_MODELING_PREP_API_KEY by default.
- <u>fred_api_key (str &#124; None):</u> a FRED key, for credit and commercial real estate; read from FRED_API_KEY by default.
- <u>toolkit (Toolkit &#124; None):</u> a ready-made Finance Toolkit; built from the settings by default.
- <u>settings_dir (str &#124; Path):</u> your settings profiles; the bundled ones when "settings" does not exist.
- <u>factor_sets_dir (str &#124; Path):</u> your factor sets; the bundled ones when "factor-sets" does not exist.
- <u>regimes (str &#124; Sequence[str &#124; Regime] &#124; None):</u> "refit" for every regime that needs its own calibration, or the regimes to calibrate by id, name or as a `Regime`; None (default) calibrates none.
- <u>regimes_dir (str &#124; Path):</u> your regimes folder; the bundled regimes when "regimes" does not exist.
- <u>rebuild (bool):</u> calibrate again and replace an existing snapshot; False by default.
- <u>lock_timeout (float):</u> seconds to wait for another builder before going ahead anyway; an hour by default.

**Returns:**

<u>Snapshot:</u> the snapshot, built or read.

**Raises:**

- <u>ValueError:</u> if `as_of` is not a "YYYY-MM" month or lies in the future, a profile name is not plain, or a regime named in `regimes` does not fit the factor set.

</details>

#### Snapshot.load

Read a stored snapshot: one month's, or the newest when `as_of` is left out.

Loading reads only `meta.json`; the calibration, configuration and history are read when first used, so
listing or choosing a snapshot costs next to nothing.

**As an example:**

```python
from financescenarios import Snapshot

snapshot = Snapshot.load(as_of="2026-10")
snapshot.meta.created_at
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
Snapshot.load(
    settings: str = 'default',
    factor_set: str = 'default',
    as_of: str | None = None,
    root: str | Path | None = None,
) -> Snapshot
```

**Args:**

- <u>settings (str):</u> the settings profile; "default" by default.
- <u>factor_set (str):</u> the factor set; "default" by default.
- <u>as_of (str &#124; None):</u> the month, "YYYY-MM"; the newest built by default.
- <u>root (str &#124; Path &#124; None):</u> where snapshots are kept; `<cache_dir()>/snapshots` by default.

**Returns:**

<u>Snapshot:</u> the snapshot.

**Raises:**

- <u>FileNotFoundError:</u> if no such snapshot was built.

</details>

#### Snapshot.latest

The newest stored snapshot of these profiles, or None when none was built: what to serve while this month's
is still building.

**As an example:**

```python
from financescenarios import Snapshot

snapshot = Snapshot.latest() or Snapshot.build(api_key="FINANCIAL_MODELING_PREP_KEY")
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
Snapshot.latest(
    settings: str = 'default',
    factor_set: str = 'default',
    root: str | Path | None = None,
) -> Snapshot | None
```

**Args:**

- <u>settings (str):</u> the settings profile; "default" by default.
- <u>factor_set (str):</u> the factor set; "default" by default.
- <u>root (str &#124; Path &#124; None):</u> where snapshots are kept; `<cache_dir()>/snapshots` by default.

**Returns:**

<u>Snapshot &#124; None:</u> the newest snapshot, or None.

</details>

#### Snapshot.available

Every stored snapshot's `meta.json`, newest month first.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
Snapshot.available(root: str | Path | None = None) -> list[SnapshotMeta]
```

**Args:**

- <u>root (str &#124; Path &#124; None):</u> where snapshots are kept; `<cache_dir()>/snapshots` by default.

**Returns:**

<u>list[SnapshotMeta]:</u> one per snapshot.

</details>

#### Snapshot.prune

Delete every snapshot but the newest `keep_months` of each settings profile and factor set.

A snapshot is about 110 kB, so this is housekeeping rather than a necessity, but a server building one every
month keeps the month it answers from and the one before. The newest snapshot of each pair is never deleted,
even when it is older than another pair's. Each folder is renamed out of sight before it is deleted, so a
reader never finds half a snapshot, and the leftovers of interrupted builds go too.

**As an example:**

```python
from financescenarios import Snapshot

Snapshot.prune(keep_months=2)
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
Snapshot.prune(keep_months: int = 2, root: str | Path | None = None) -> list[str]
```

**Args:**

- <u>keep_months (int):</u> how many of each pair's newest snapshots to keep, at least 1; 2 by default.
- <u>root (str &#124; Path &#124; None):</u> where snapshots are kept; `<cache_dir()>/snapshots` by default.

**Returns:**

<u>list[str]:</u> the ids of the snapshots deleted, e.g. ["2026-08/default__default"].

**Raises:**

- <u>ValueError:</u> if `keep_months` is below 1.

</details>

#### Snapshot.scenarios

A `Scenarios` set up like the snapshot (its configuration and engine settings) without a Finance Toolkit, so
it simulates from `calibration` only.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
scenarios() -> Scenarios
```

**Returns:**

<u>Scenarios:</u> pass `calibration=snapshot.calibration` to its `simulate()`.

</details>

#### Snapshot.simulate

Simulate from the snapshot's calibration, without downloading or fitting anything.

The same snapshot, number of scenarios, seed, horizon and regime always give the same scenarios, on any
machine running the same package version. A regime runs exactly as it would on a fresh calibration: one that
moves long-run paths (such as `oil_crisis`'s inflation path), adds shocks or keeps the scenarios that tell its
story replays the snapshot's own calibration, and one that fixes a fitted parameter, such as an equity's regime
means, replays the calibration the snapshot stored for it (see `build(regimes=...)`).

**As an example:**

```python
from financescenarios import Snapshot

snapshot = Snapshot.load()
baseline = snapshot.simulate(n_simulations=2000, seed=1)
stressed = snapshot.simulate(n_simulations=2000, seed=1, regime="oil_crisis")
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
simulate(
    n_simulations: int | None = None,
    seed: int | None = None,
    regime: str | Regime | None = None,
    years: float | None = None,
    regimes_dir: str | Path = 'regimes',
) -> ScenarioSet
```

**Args:**

- <u>n_simulations (int &#124; None):</u> the number of scenarios; the settings profile's by default.
- <u>seed (int &#124; None):</u> the random seed; the settings profile's by default.
- <u>regime (str &#124; Regime &#124; None):</u> a stress regime, by id ("oil_crisis"), name or as a `Regime`; None by default.
- <u>years (float &#124; None):</u> the horizon in years, e.g. 30; the settings profile's by default.
- <u>regimes_dir (str &#124; Path):</u> your regimes folder; the bundled regimes when "regimes" does not exist.

**Returns:**

<u>ScenarioSet:</u> the simulated scenarios.

**Raises:**

- <u>ValueError:</u> if the regime targets a factor the snapshot lacks, or fixes a fitted parameter and the snapshot stored no calibration for it.
- <u>FileNotFoundError:</u> if no regime has the id or name given.

</details>

#### Snapshot.summary

Simulate from the snapshot and keep only each factor's percentiles at a few horizons: a whole run in a few
kilobytes, one row per factor and year by default.

A monthly run of forty years has 480 dates per factor; nobody reads them all. The summary keeps the step nearest
each anniversary of the start (or the `horizons` you give), with the mean, spread and percentiles across the
scenarios, read the way `describe()` reads them: a rate as its yearly rate, a price as its yearly return since
the start. With a `cache`, an identical request on the same snapshot is answered from disk.

**As an example:**

```python
from financescenarios import ResultCache, Snapshot

snapshot = Snapshot.load()
summary = snapshot.summary(
    n_simulations=2000, seed=1, factors=["us_broad", "united_states_short_rate"], horizons=[1, 3, 5],
    cache=ResultCache(),
)
summary.to_frame()
```

Which returns (the default snapshot of 2026-10, without "date" and the quartiles), US equities' yearly return
since the start and the US short rate:

| factor                   | horizon |   mean |    std |   q0.05 |   q0.5 |  q0.95 |
|:-------------------------|--------:|-------:|-------:|--------:|-------:|-------:|
| us_broad                 |     1.0 | 0.0990 | 0.1522 | -0.1729 | 0.1043 | 0.3271 |
| us_broad                 |     3.0 | 0.0882 | 0.0964 | -0.0805 | 0.0917 | 0.2405 |
| us_broad                 |     5.0 | 0.0882 | 0.0780 | -0.0449 | 0.0911 | 0.2137 |
| united_states_short_rate |     1.0 | 0.0435 | 0.0111 |  0.0264 | 0.0431 | 0.0621 |
| united_states_short_rate |     3.0 | 0.0448 | 0.0276 |  0.0000 | 0.0427 | 0.0924 |
| united_states_short_rate |     5.0 | 0.0447 | 0.0332 |  0.0000 | 0.0426 | 0.1023 |

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
summary(
    n_simulations: int | None = None,
    seed: int | None = None,
    regime: str | Regime | None = None,
    years: float | None = None,
    factors: Sequence[str] | None = None,
    horizons: Sequence[float] | None = None,
    frequency: SummaryFrequency = 'yearly',
    quantiles: Sequence[float] = SUMMARY_QUANTILES,
    metric: Metric | None = None,
    regimes_dir: str | Path = 'regimes',
    cache: ResultCache | None = None,
) -> ScenarioSummary
```

**Args:**

- <u>n_simulations (int &#124; None):</u> the number of scenarios; the settings profile's by default.
- <u>seed (int &#124; None):</u> the random seed; the settings profile's by default.
- <u>regime (str &#124; Regime &#124; None):</u> a stress regime, see `simulate`; None by default.
- <u>years (float &#124; None):</u> the horizon in years; the settings profile's by default.
- <u>factors (Sequence[str] &#124; None):</u> the factors to report; every factor by default.
- <u>horizons (Sequence[float] &#124; None):</u> years from the start, e.g. [1, 3, 5]; set by `frequency` by default.
- <u>frequency (str):</u> "yearly" (default), "quarterly" or "monthly", the spacing when `horizons` is None.
- <u>quantiles (Sequence[float]):</u> the quantiles to report; 5%, 25%, 50%, 75% and 95% by default.
- <u>metric (str &#124; None):</u> the reading (see `ScenarioSet.metric_paths`); each factor's default by default.
- <u>regimes_dir (str &#124; Path):</u> your regimes folder; the bundled regimes when "regimes" does not exist.
- <u>cache (ResultCache &#124; None):</u> where to look the summary up and keep it; not cached by default.

**Returns:**

<u>ScenarioSummary:</u> the percentiles; `to_frame()` gives them as a table.

</details>

#### Snapshot.cached_summary

The summary `summary()` would return for these arguments when `cache` already holds it, else None: never
simulates, so it tells cheaply whether an answer is ready.

**As an example:**

```python
from financescenarios import ResultCache, Snapshot

snapshot, cache = Snapshot.load(), ResultCache()
snapshot.cached_summary(cache, n_simulations=1000, regime="oil_crisis") is None  # True until computed once
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
cached_summary(
    cache: ResultCache,
    n_simulations: int | None = None,
    seed: int | None = None,
    regime: str | Regime | None = None,
    years: float | None = None,
    factors: Sequence[str] | None = None,
    horizons: Sequence[float] | None = None,
    frequency: SummaryFrequency = 'yearly',
    quantiles: Sequence[float] = SUMMARY_QUANTILES,
    metric: Metric | None = None,
    regimes_dir: str | Path = 'regimes',
) -> ScenarioSummary | None
```

**Args:**

- <u>cache (ResultCache):</u> the cache to look in.
- <u>n_simulations, seed, regime, years, factors, horizons, frequency, quantiles, metric, regimes_dir:</u> as in `summary`.

**Returns:**

<u>ScenarioSummary &#124; None:</u> the cached summary, or None.

</details>

#### Snapshot.changes

Every factor's realised month-on-month moves, side by side: a price's simple return, a rate's change in its own
units. The panel a holding's own returns are regressed on.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
changes(factors: Sequence[str] | None = None) -> pl.DataFrame
```

**Args:**

- <u>factors (Sequence[str] &#124; None):</u> the factors to include; every factor with history by default.

**Returns:**

<u>pl.DataFrame:</u> "date" (the month's first day) and one column per factor.

</details>

#### Snapshot.history_set

The realised history as a one-scenario run on the dates the chosen factors share, as `Scenarios.history`
builds it, so a portfolio is backtested on it with the same calls as on the snapshot's scenarios.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
history_set(factors: Sequence[str] | None = None, period: str = 'monthly') -> ScenarioSet
```

**Args:**

- <u>factors (Sequence[str] &#124; None):</u> the factors to include; every factor with history by default, which limits the window to the shortest history.
- <u>period (str):</u> "monthly" (default), "quarterly" or "yearly".

**Returns:**

<u>ScenarioSet:</u> one path per factor on the shared dates.

</details>

### ResultCache

A small on-disk cache of what runs reduce to, keyed by the request, the snapshot it ran on and the package version.

The same question on the same snapshot always gets the same answer, so it only needs computing once. Each value is
a JSON file named by the SHA-256 of the canonical request (keys sorted, so their order never matters), the snapshot
id and the package version, filed under the snapshot's month so whole months can be dropped once a newer snapshot
replaces them. Values must be small summaries, such as a `ScenarioSummary`; raw paths are refused. Writes replace
a file in one step, so concurrent threads and processes never read half a value.

**As an example:**

```python
from financescenarios import ResultCache, Snapshot

cache = ResultCache()
summary = Snapshot.load().summary(regime="oil_crisis", cache=cache)  # computed once, then read from disk
cache.prune(keep_months=2)
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
ResultCache(root: str | Path | None = None, max_bytes: int = _MAX_RESULT_BYTES)
```

</details>

#### ResultCache.root

The cache's folder.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
resultcache.root  # property -> Path
```

</details>

#### ResultCache.key

The SHA-256 key of a request on a snapshot, for this package version.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
key(request: Any, snapshot_id: str) -> str
```

</details>

#### ResultCache.get

The value stored for a request on a snapshot, or None when there is none.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
get(request: Any, snapshot_id: str) -> Any | None
```

**Args:**

- <u>request (Any):</u> the request, JSON-like: dicts, lists, numbers, strings, dates or Pydantic models.
- <u>snapshot_id (str):</u> the snapshot it ran on, e.g. `snapshot.id`.

**Returns:**

<u>Any &#124; None:</u> the stored value, or None.

</details>

#### ResultCache.put

Store a small JSON value for a request on a snapshot.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
put(request: Any, snapshot_id: str, value: Any) -> str
```

**Args:**

- <u>request (Any):</u> the request, as for `get`.
- <u>snapshot_id (str):</u> the snapshot it ran on, e.g. `snapshot.id`.
- <u>value (Any):</u> the result, JSON-serialisable and no larger than `max_bytes`.

**Returns:**

<u>str:</u> the key it was stored under.

**Raises:**

- <u>ValueError:</u> if the value is larger than `max_bytes`, or holds NaN or infinity.
- <u>TypeError:</u> if the value is not JSON-serialisable, such as a NumPy array of paths.

</details>

#### ResultCache.prune

Delete every month of results but the newest `keep_months`, the months a server still answers from.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
prune(keep_months: int = 2) -> list[str]
```

**Args:**

- <u>keep_months (int):</u> how many of the newest months to keep; 2 by default, this month's and the last.

**Returns:**

<u>list[str]:</u> the months deleted, oldest first.

</details>

#### ResultCache.clear

Delete every cached result.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
clear() -> None
```

</details>

### ScenarioSummary

A run reduced to the percentiles of each factor at a few horizons: small enough to cache, send or read at a glance.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
class ScenarioSummary(BaseModel):
    snapshot_id: str | None = None
    regime: str | None = None
    n_simulations: int
    seed: int | None = None
    start_date: date
    horizons: list[float]
    quantiles: list[float]
    factors: dict[str, dict[str, Any]]
    rows: list[SummaryRow]
```

**Attributes:**

- <u>snapshot_id (str &#124; None):</u> the snapshot the run replayed, if any.
- <u>regime (str &#124; None):</u> the name of the regime the run told, if any.
- <u>n_simulations (int):</u> the number of scenarios behind every percentile.
- <u>seed (int &#124; None):</u> the random seed of the run.
- <u>start_date (date):</u> the run's first date.
- <u>horizons (list[float]):</u> the horizons reported, in years from the start.
- <u>quantiles (list[float]):</u> the quantiles reported, as "q<quantile>" columns.
- <u>factors (dict[str, dict[str, Any]]):</u> factor name -> its "label", "category", "metric" (how its numbers read, e.g. "rate" or "annualized") and "initial" (today's reading, empty for a price).
- <u>rows (list[SummaryRow]):</u> one per factor and horizon: "factor", "horizon", "date", "mean", "std" and the quantiles.

</details>

#### ScenarioSummary.to_frame

The rows as a table: "factor", "horizon", "date", "mean", "std" and one "q<quantile>" column each.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
to_frame() -> pl.DataFrame
```

</details>

### Reporting

Show simulated prices in one reporting currency: take a factor simulated in its own currency, such as a Japanese
equity in yen, and convert every scenario into, say, US dollars with that scenario's own simulated exchange rate.

An investor who reports in dollars wants to see what a Japanese or European holding is worth in dollars in each
scenario, including the currency gain or loss, not just its local price. Because the exchange rate is simulated
together with the price, the converted result carries the currency risk and its correlation with the asset: in
a scenario where the yen weakens as Japanese equities rally, the dollar investor keeps less of the rally. An
unhedged foreign holding is therefore usually riskier in the reporting currency than in its own, unless the
currency tends to move against the asset. `Portfolio` uses it to put every holding in the reporting currency
before weighting; the run itself is left unchanged.

Only price-like factors are converted: `equities`, `commodities` and `real_estate`, whose growth rate is first
compounded into a price index. Rates and ratios (`interest_rates`, `inflation`, `credit`, `unemployment`,
`yield_curve`, `dividend_yield`, `leading_indicator`) have no currency to convert: a German short rate of 3% stays
3%, so asking to convert one raises a `ValueError`.

Exchange rates follow the OECD convention: units of the national currency per US dollar. Going from a currency to
dollars divides by its simulated rate, going from dollars to a currency multiplies by it, and two non-dollar
currencies are bridged through the dollar in two steps, since every `fx` factor is quoted against the dollar. Each
`fx` entry names its currency in `currency`; when that is unset, it is read from an `interest_rates` or `inflation`
entry for the same `country`, or is `EUR` for the OECD's euro area codes.

With the default `fx[i].drift_mode: random_walk` (or `historical`) the exchange rate moves independently of the
simulated interest rates. `drift_mode: irp` ties its expected move to the simulated rate gap between the two
currencies through uncovered interest rate parity, a real-world view, and `drift_mode: ppp` to the simulated
inflation gap through purchasing power parity, with the real rate pulled back over a few years; `measure:
risk_neutral` fixes its drift at
today's rate gap through covered interest rate parity, the forward's no-arbitrage drift a market-consistent
valuation needs, see
[Gorvett (2001)](https://www.casact.org/sites/default/files/database/dpp_dpp01_01dpp19.pdf).

Configuration (`reporting` in a settings profile, beside `engine` and `toolkit`):

| Key | Default | Meaning |
|:----|:--------|:--------|
| `reporting.reporting_currency` | `USD` | The currency `convert()` expresses a level factor in. |

Each level factor's own `currency` field (`equities[i].currency`, `commodities[i].currency`, `real_estate.currency`)
says which currency it is simulated in; a ticker added to the run with `add_holdings()` carries its own. The
reporting currency has no effect on calibration, simulation or the correlation matrix.

**References:**

- Gorvett, R.W. (2001). "Foreign Exchange Rate Risk: Institutional Issues and Stochastic Modeling." CAS Discussion Paper Program. <https://www.casact.org/sites/default/files/database/dpp_dpp01_01dpp19.pdf>

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
Reporting(scenario_set: ScenarioSet, config: ScenariosConfig)
```

</details>

#### Reporting.convert

Convert one price-like factor's simulated paths into the run's reporting currency, using each path's own
simulated exchange rate.

Ask for a factor by name and get its simulated prices in your reporting currency. A yen-priced equity of 430
when the dollar buys 158.79 yen reads as 430 / 158.79 = 2.71 dollars, and every later value is divided by that
path's exchange rate, so currency swings are part of the outcome. A factor already in the reporting currency
comes back unchanged; `real_estate` is first compounded from a growth rate into a price index.

With P_N the price in its own currency and X_N and X_R the simulated units of the native and the reporting
currency per US dollar (1 for the dollar itself), each path converts at its own exchange rates.

The formula is as follows:
- P_R = P_N * X_R / X_N

**As an example:**

```python
from datetime import date

from financescenarios import (
    EngineConfig,
    EquityConfig,
    FXConfig,
    InflationConfig,
    InterestRateConfig,
    Scenarios,
    ScenariosConfig,
    ToolkitConfig,
)
from financescenarios.reporting.reporting_controller import Reporting

config = ScenariosConfig(
    start_date=date(2026, 10, 1),
    engine=EngineConfig(n_simulations=1000, n_steps=5, frequency="yearly", seed=42),
    toolkit=ToolkitConfig(start_date=date(2005, 1, 1)),
    interest_rates=[InterestRateConfig(name="interest_rate", country="United States", currency="USD")],
    inflation=[
        InflationConfig(name="inflation", country="United States", currency="USD"),
        InflationConfig(name="jp_inflation", country="Japan", currency="JPY"),
    ],
    equities=[
        EquityConfig(name="us_equity", ticker="SPY", currency="USD"),
        EquityConfig(name="jp_equity", ticker="1306.T", currency="JPY"),
    ],
    fx=[FXConfig(name="usd_jpy", country="Japan")],
)
result = Scenarios.from_config(config).simulate()

reporting = Reporting(result, config)
jp_equity_in_usd = reporting.convert("jp_equity")
```

Which returns (calibrated on 2026-10-19), as percentiles across the 1,000 paths next to the median yen price
and yen per dollar:

| date | jp_equity (JPY), median | usd_jpy, median | jp_equity (USD), 5% | median | 95% |
|:-----|------------------------:|----------------:|--------------------:|-------:|----:|
| 2026-10-01 | 427.1 | 157.00 | 2.72 | 2.72 | 2.72 |
| 2027-10-01 | 479.2 | 157.14 | 2.17 | 3.07 | 3.77 |
| 2031-10-01 | 660.9 | 156.78 | 2.07 | 4.20 | 7.90 |

The yen price grows 55% in five years and the median exchange rate stays near 157 yen per dollar, so the
median dollar value grows about as much, but the 5% to 95% range in dollars is wide: the dollar investor
carries the currency risk on top of the equity risk.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
convert(factor_name: str) -> pl.DataFrame
```

**Args:**

- <u>factor_name (str):</u> the name of an `equities`, `commodities` or `real_estate` factor in this run.

**Returns:**

<u>pl.DataFrame:</u> a `scenario` column plus one column per date, one row per path, as `ScenarioSet.to_dataframe()`.

**Raises:**

- <u>ValueError:</u> if `factor_name` is not a configured factor with a currency, or is a rate or ratio factor.
- <u>KeyError:</u> if the factor is configured but missing from this `ScenarioSet`.
- <u>RuntimeError:</u> if this run lacks the `fx` entry the conversion needs; the message names its country.

</details>

### How It Is Calculated

The model functions behind this page, each with the formula it implements.

#### monthly_changes

Each factor's month-on-month move, side by side: a price's or an index's simple return, any other factor's change
in its own units (a rate moving from 0.040 to 0.043 changes by 0.003). A month whose previous month is missing, as
in a quarterly series, has no move.

The formula is as follows:
- price or index: r(t) = x(t) / x(t - 1 month) - 1
- any other factor: d(t) = x(t) - x(t - 1 month)

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
monthly_changes(frame: pl.DataFrame, factors: Sequence[str] | None = None) -> pl.DataFrame
```

**Args:**

- <u>frame (pl.DataFrame):</u> the long history table, from `history_frame`.
- <u>factors (Sequence[str] &#124; None):</u> the factors to include. Defaults to None, every factor.

**Returns:**

<u>pl.DataFrame:</u> "date" and one column per factor, sorted by date; empty where a factor has no move that month.

**Raises:**

- <u>KeyError:</u> if a named factor has no history.

</details>

#### convert_to_reporting_currency

Convert a price simulated in its own currency into the reporting currency, scenario by scenario, with each
scenario's own simulated exchange rate. The converted price carries the currency gain or loss, and its correlation
with the asset, that an investor reporting in another currency actually experiences.

Exchange rates are quoted as units of the national currency per US dollar (the OECD convention). Going from a
currency to dollars divides by its rate, going from dollars to a currency multiplies by it, and two non-dollar
currencies are bridged through the dollar in two steps. A price already in the reporting currency comes back
unchanged.

The formula is as follows:

$$
P_{rep}(t) = P_{nat}(t) / X_{nat}(t) \cdot X_{rep}(t)
$$

Where P_nat is the price in its own currency, X_nat and X_rep the units of the native and the reporting currency
per US dollar, and X_USD = 1, so a USD price skips the division and a USD reporting currency the multiplication.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
convert_to_reporting_currency(
    native_paths: np.ndarray,
    fx_rate_paths: dict[str, np.ndarray],
    native_currency: str,
    reporting_currency: str,
) -> np.ndarray
```

**Args:**

- <u>native_paths (np.ndarray):</u> the simulated price per scenario and date, in its own currency.
- <u>fx_rate_paths (dict[str, np.ndarray]):</u> currency code to its simulated exchange rate (units per US dollar) per scenario and date; only the currencies the conversion needs.
- <u>native_currency (str):</u> the currency the price is in.
- <u>reporting_currency (str):</u> the currency to convert into.

**Returns:**

<u>np.ndarray:</u> the price per scenario and date, in the reporting currency.

**Raises:**

- <u>KeyError:</u> if an exchange rate the conversion needs is missing.

</details>
