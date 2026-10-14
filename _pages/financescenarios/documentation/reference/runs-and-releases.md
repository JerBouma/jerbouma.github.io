---
title: "Run Files and Releases"
seo_title: "Run Files and Releases Reference | Finance Scenarios"
seo_title_suffix: false
excerpt: "Write and read saved runs, and publish, load and simulate versioned calibration releases."
description: "Write and read saved runs, and publish, load and simulate versioned calibration releases."
author_profile: false
permalink: /projects/financescenarios/docs/reference/runs-and-releases
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

Write and read saved runs, and publish, load and simulate versioned calibration releases.

```python
from financescenarios import write_run, read_run, read_run_calibration, publish_calibration, load_release, simulate_release
```

## write_run

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

## read_run

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

## read_run_calibration

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

## publish_calibration

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

release = publish_calibration(factor_set="us_only")
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

## load_release

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

## simulate_release

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
