---
title: "Run Files and Releases"
seo_title: "Run Files and Releases Reference – Finance Scenarios"
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

Write and read saved runs, and publish, load and simulate versioned calibration releases. Generated from the docstrings of Finance Scenarios 0.1.0; `help(...)` in Python shows the same text.

```python
from financescenarios import write_run, read_run, read_run_calibration, publish_calibration, load_release, simulate_release
```

## write_run

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

Write one run's full output to `output_dir/<run_id>/`: `config.yaml` and
`factors.yaml` (the resolved config that produced this run, split the same
way `load_config()` reads them: `config.yaml` for `start_date`/`engine`/
`toolkit`/`reporting` (run settings, not factor definitions, since swapping
factor-sets shouldn't drag `reporting_currency` along with it),
`factors.yaml` for every factor definition), one `<factor>.<format>`
file per simulated factor (via `ScenarioSet.to_dataframe()`), and a
`manifest.json` (run_id, creation time, regime, factor names and their
categories, n_simulations, seed, warnings) cheap enough to read for listing
runs without opening any factor file.

**Args:**

- <u>result (ScenarioSet):</u> the simulation to persist.
- <u>config (ScenariosConfig):</u> the resolved config that produced `result` (post regime belief-shaping, if a regime was applied).
- <u>output_dir (str &#124; Path):</u> the runs directory; a subdirectory named `run_id` is created under it.
- <u>regime (str &#124; None):</u> the regime name applied, if any, recorded in the manifest for display, purely informational.
- <u>output_format (str):</u> "csv" or "parquet" (the default), the per-factor file format. Parquet is both smaller on disk (columnar, zstd-compressed by `write_parquet()`'s own default) and faster to read back (`read_run()`), so it's the default for every caller that doesn't explicitly ask for CSV.
- <u>run_id (str &#124; None):</u> the run's identifier (its subdirectory name). Defaults to a UTC timestamp plus a short random suffix.
- <u>warnings (list[str] &#124; None):</u> calibration/simulation warnings this run produced (e.g. from `financescenarios.helpers.collect_warnings()` wrapped around the calibrate+simulate call), persisted so a caller reading the run back later (a fresh process, a notebook) still sees them, not just whoever was watching the console when the run happened. Defaults to an empty list, not None, so every run's manifest has a consistent "warnings" key regardless of caller.
- <u>correlation_fallback_pairs (list[str] &#124; None):</u> 'factor_a/factor_b' pairs the correlation matrix defaulted to 0.0 (assumed uncorrelated) for lack of a reliable overlap; see `Scenarios.correlation_fallback_pairs`/ `CalibrationResult.correlation_fallback_pairs`'s own docstring. Only ever populated for `engine.correlation_method="pairwise"` (the default). Same "always a list, not None, in the manifest" reasoning as `warnings`.
- <u>calibration_failures (dict[str, str] &#124; None):</u> factor name -> failure reason, for a configured factor whose own calibration raised (or which depended on one that did) and was skipped rather than aborting the whole run; see `Scenarios.calibration_failures`/ `CalibrationResult.calibration_failures`'s own docstring. Same "always a dict, not None, in the manifest" reasoning as `warnings`.
- <u>calibration (CalibrationResult &#124; None):</u> the calibration this run was simulated from. When given, it's written alongside as `calibration.json`, which makes the run replayable with no network or API key at all: `read_run_calibration()` reads it back for `Scenarios.simulate(calibration=...)`, e.g. to re-run the same fit at a different seed or path count. Omitted by default, since a caller that never intends to replay shouldn't pay for the extra file.

**Returns:**

<u>str:</u> the run_id used (generated if not given).

**Raises:**

- <u>ValueError:</u> if `output_format` is not "parquet" or "csv", or `run_id` is not a plain folder name (a path such as "../x" would write outside `output_dir`).

## read_run

```python
read_run(run_dir: str | Path) -> ScenarioSet
```

Reconstruct a ScenarioSet from a directory `write_run()` wrote: reads the
per-factor files back with polars and rebuilds the same paths/dates/
n_simulations/seed shape, so every ScenarioSet method (`to_dataframe()`,
`summary_statistics()`, `filter()`, `diagnose()`, ...) works on it exactly
as it would on the original in-memory result. No calibration or simulation
happens here, only reading and reshaping already-computed numbers.

`calibration_metadata` is empty on the returned ScenarioSet (it isn't
persisted), so `diagnose()`, which needs it, isn't usable on a reloaded run.
`time_grid` round-trips exactly via the manifest, so dt-sensitive readers
(`cumulative_index()`, `discount_factors()`, a portfolio's rate sleeves)
compound at the true `time_step`. A run written before the manifest carried
"time_grid" falls back to a date-derived grid (years elapsed since the
first date), whose first monthly interval is ~30/365.25 rather than 1/12.

**Args:**

- <u>run_dir (str &#124; Path):</u> the run's own directory (`output_dir/<run_id>`).

**Returns:**

<u>ScenarioSet:</u> the reloaded simulation.

**Raises:**

- <u>FileNotFoundError:</u> if `run_dir` has no `manifest.json` or is missing a factor file the manifest lists.

## read_run_calibration

```python
read_run_calibration(run_dir: str | Path) -> 'CalibrationResult | None'
```

Read back the calibration a run was simulated from, if `write_run()` was given
one. The offline replay path: no Finance Toolkit call, no API key, no refetch.

```python
calibration = read_run_calibration("output/20260819T063851Z-7bfdde41")
wider = Scenarios(toolkit=None, n_simulations=20_000).simulate(config, calibration=calibration)
```

**Args:**

- <u>run_dir (str &#124; Path):</u> the run's own directory (`output_dir/<run_id>`).

**Returns:**

<u>CalibrationResult &#124; None:</u> the stored calibration, or None for a run written without one (including every run written before this was recorded).

## publish_calibration

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

Calibrate from named profiles and publish the result as a versioned release with a validation report.

In plain terms: a calibration is what the model learnt from history. Publishing one fixes it under a version
tag, so every later run can name exactly which one it used and get the same scenarios, and checks it first:
every factor calibrated, the parameters are plausible, the correlations are valid and reproduced by the
simulation, each factor swings about as much as its history did, and the run is reproducible.

The release folder `<output_dir>/<release_version>/` holds:

- `calibration.json`: the calibration, for `CalibrationResult.load` and `simulate(calibration=...)`.
- `manifest.json`: the version, date, profiles, a SHA-256 hash of the full configuration, the package versions
  and the data window.
- `checks.json` and `report.md`: every check's status, numbers and plain-language explanation, and the
  fitted parameters.

**Args:**

- <u>output_dir (str &#124; Path):</u> where releases are kept.
- <u>release_version (str &#124; None):</u> the tag; today's date as "YYYY.MM.DD" by default.
- <u>settings, factor_set (str):</u> the profiles to calibrate from (see `load_profiles`).
- <u>settings_dir, factor_sets_dir (str &#124; Path):</u> where those profiles live; the bundled presets otherwise.
- <u>n_simulations (int):</u> the size of the two seeded runs the checks simulate.
- <u>toolkit (Toolkit &#124; None):</u> a pre-built Toolkit, e.g. a fake in tests; built from the settings otherwise.
- <u>subfolder (str &#124; None):</u> write to `<output_dir>/<release_version>/<subfolder>/` instead, so several factor sets share one version (the yearly pipeline uses the factor set's name).

**Returns:**

<u>ReleaseResult:</u> the folder, the manifest and the checks.

**Raises:**

- <u>FileExistsError:</u> if that version was already published, since a release must never change after the fact.

**As an example:**

```python
from financescenarios.release.release_controller import publish_calibration

release = publish_calibration(factor_set="us_only")
release.manifest.status, release.directory
```

## load_release

```python
load_release(directory: str | Path) -> tuple[CalibrationResult, ReleaseManifest]
```

A published calibration and its manifest, ready for `simulate(calibration=...)`.

**Args:**

- <u>directory (str &#124; Path):</u> the release folder, e.g. what `download_release` returns.

**Returns:**

<u>tuple[CalibrationResult, ReleaseManifest]:</u> the calibration and what identifies it.

## simulate_release

```python
simulate_release(
    directory: str | Path,
    settings_dir: str | Path = 'settings',
    factor_sets_dir: str | Path = 'factor-sets',
    n_simulations: int | None = None,
    seed: int | None = None,
) -> ScenarioSet
```

Simulate from a published calibration without fetching any data: the release's own settings and factor set
give the engine (steps, frequency, simulations, seed), and its calibration replaces the fit.

**Args:**

- <u>directory (str &#124; Path):</u> the release folder, e.g. what `download_release` returns.
- <u>settings_dir, factor_sets_dir (str &#124; Path):</u> where the release's profiles live; the bundled presets otherwise.
- <u>n_simulations, seed (int &#124; None):</u> override the settings' own values for this run.

**Returns:**

<u>ScenarioSet:</u> the simulated scenarios.

**Raises:**

- <u>ValueError:</u> if the profiles no longer hash to the release's configuration (they changed since it was published), since the calibration would not match the factors they now define.
