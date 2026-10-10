---
title: Validation and Testing
seo_title: Validation and Testing Documentation – Finance Scenarios
excerpt: "What evidence exists that the simulation logic behaves correctly: analytical checks, recorded regressions, external benchmarks, published calibrations and what is not validated."
description: "How Finance Scenarios output is checked: analytical tests, regression checks, NAIC GOES, DNB and bond-panel benchmarks and published calibrations."
author_profile: false
permalink: /projects/financescenarios/docs/validation
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

This page explains what evidence exists that the simulation logic behaves correctly, not just that the code runs without errors. The test suite lives under `tests/`, mirrors the `financescenarios/` package one-to-one, and is run with:

```bash
uv run pytest tests -q
```

## Analytical checks against known formulas

The strongest form of evidence is comparing simulated output against a mathematical result that can be derived independently of the code, rather than against another run of the same code.

For the Ornstein-Uhlenbeck process used by the interest rate and inflation factors, the theoretical stationary (long-run) mean and variance are known in closed form: the mean converges to `theta` (the long-run mean parameter), and the variance converges to `sigma^2 / (2*a)` (volatility squared, divided by twice the mean-reversion speed). `tests/engine/test_engine_model.py` simulates 5000 paths of 500 steps and checks that the simulated terminal mean and variance land within tolerance of these formulas. This confirms the step function and the stepping loop together reproduce the process the mathematics says they should, not just that they run.

Similarly, `tests/engine/test_engine_model.py` checks that `generate_correlated_shocks` (the Cholesky-decomposition step) actually produces correlated randomness: 50,000 simulated shock pairs with a target correlation of 0.6 reproduce that correlation, empirically, within a tolerance of 0.02.

## Boundary and invariant checks

Some properties should hold for every simulated value, not just on average:

- The CIR interest rate model is checked to never go negative across 5000 simulated steps, since the model is only valid for non-negative rates.
- The Hull-White interest rate model is checked to be able to go negative, and to drift toward its long-run mean over many steps, since that is the documented, expected behaviour of a Gaussian mean-reverting process.
- `nearest_correlation_matrix` is checked to always return a matrix with non-negative eigenvalues, a symmetric shape and a unit diagonal, the formal definition of a valid correlation matrix, both when repairing an invalid input and when passed an already-valid one (which it must leave unchanged).

## Regression checks against recorded output

Calibration functions such as `fit_ou_process`, `fit_cir_process`, `fit_regime_switching_lognormal` and `build_correlation_matrix` are deterministic: given the same input series, they always produce the same fitted parameters. `tests/conftest.py` defines a `recorder` fixture that captures a function's output the first time a test runs, saves it to a CSV or JSON file alongside the test module, and compares every later run against that recorded file. If a future code change unintentionally alters the fitted parameters for the same input, the test fails, even though nothing about the test itself changed. `tests/conftest.py` also defines a `stochastic_recorder` fixture, used for the analytical and empirical checks above, which compares a computed value against an expected one within a stated tolerance instead of requiring an exact match, since Monte Carlo output is inherently random.

## Error path checks

Every documented failure condition has a test that asserts the correct error is raised: too few observations to fit an Ornstein-Uhlenbeck or regime-switching model, a fitted process with no mean reversion, a negative CIR observation, mismatched correlation series lengths, a belief override with the wrong number of entries, and a circular factor dependency.

## Documentation and warning checks

- **The README runs against the real API.** `tests/test_readme_snippets.py` parses every Python block in the README and checks that each `from financescenarios import ...` name exists, and that every method and keyword argument it calls on `Scenarios`, `Portfolio`, `Solvency` or a result exists under that name. It needs no network, so a renamed argument fails the suite rather than a newcomer's first run.
- **A numpy division warning fails the test.** `pyproject.toml` turns numpy's "divide by zero" and "invalid value" RuntimeWarnings into errors, since such a warning is usually a NaN on its way into a result. Ratios that are undefined by design, such as a Sharpe ratio on a path that never moves, are computed under `np.errstate` and documented as NaN or infinite.

## Reproducibility checks

Given the same seed, a simulation run must produce byte-identical output. This is checked directly on the correlated-shock generator, on the stepping loop, and end-to-end through `Scenarios.simulate()`.

## Integration tests

`tests/test_scenarios_controller.py` runs a complete `Scenarios.simulate()` call, through calibration, dependence and the engine, against a hand-written fake `Toolkit` that returns realistic pandas data without any network access. This checks the wiring between modules on every test run: that each controller calls the right FinanceToolkit method with the right arguments, and that the data shapes handed between modules line up.

`tests/test_live_smoke.py` runs the same full simulation against the real FinanceToolkit API. It is skipped automatically when no FinancialModelingPrep API key is configured (through a `.env` file, read via `FINANCIAL_MODELING_PREP_API_KEY`), so it never blocks a normal test run or a run without secrets configured. This test exists because the exact shape and parameter names of a real API response can diverge from what a hand-written fake assumes, in ways a fake-data test cannot catch by construction. It also guards the *units* convention ([units](/projects/financescenarios/docs/units)): a synthetic fixture produces whatever scale it was written with, so only real data can catch a source that starts arriving as a per-period growth rate, or in percentage points, where an annualized decimal is expected; the live test asserts inflation, the short rate and unemployment all calibrate into single-digit-percent decimals.

## External validation benchmarks

Everything above checks this codebase against itself (a known formula, a recorded prior run, an internal invariant). `financescenarios/validation/` instead checks a calibrated factor against independent, real-world third-party datasets: "does our simulated distribution land in the same neighborhood as an outside source," not a replacement for the checks above:

- **`dnb_model.py`/`dnb_controller.py`**: compares a run's factor with De Nederlandsche Bank's scenario set at every whole year, quantile by quantile: an interest rate or inflation by its level, an equity by its yearly return. DNB publishes the set every quarter for Dutch pension funds, 20,000 scenarios over 100 years generated with the Commissie Parameters 2022 model, both real world (the P-set) and market consistent (the Q-set, calibrated to market prices including swaptions), so it is an independent, regulator-reviewed reference for a euro run and the only free swaption-consistent one. It comes through the Finance Toolkit (`economics.get_scenario_set`, a 180 MB workbook read once and cached). The same sets can also replace factors in a run, see `external_scenario_source` in [configuration](/projects/financescenarios/docs/configuration).
- **`naic_goes_model.py`/`naic_goes_controller.py`**: compares a calibrated `interest_rates` factor's own simulated percentile bands (`ScenarioSet.summary_statistics`) against NAIC's official percentile grid for the matching US Treasury tenor. That grid comes from the NAIC GOES (Generator of Economic Scenarios) files Conning publishes at `naic.conning.com/scenariofiles`, the actual *prescribed* real-world Treasury/bond/equity scenario set behind VM-20/21/22 statutory reserve calculations under the 2026 Valuation Manual, computed by NAIC/Conning over their own full (multi-thousand-scenario) run.

  `NaicGoes` downloads (with local caching) the much smaller pre-aggregated `additional_statistics` workbook and the small SERT deterministic-scenario CSV, never the full ~3.4GB raw scenario-path dump. See that module's docstring for the redistribution caveat the source page states (personal/local calibration-checking use is fine; shipping the fetcher to *other users* as a built-in feature would need Conning's sign-off first).
- **`bond_panel_model.py`/`bond_panel_controller.py`**: compares `credit_controller.Credit`'s fitted OU spread level/volatility for a maturity bucket against the real cross-sectional spread distribution of individual bonds in that bucket, from the Open Source Bond Asset Pricing project's public TRACE-derived corporate bond panel (`openbondassetpricing.com`, Dickerson, Robotti & Rossetti).

  `credit_model` today fits one process against FinanceToolkit's single ICE BofA *aggregate index* per bucket; this panel (confirmed live: 29.8M bond-date rows, 2002-07-01 to 2025-03-31) checks whether that aggregate's fitted dynamics represent the real dispersion underneath it, or smooth over fatter tail/idiosyncratic widening risk.

  `BondPanel.scan()` lazily scans the parquet (`pl.scan_parquet`), so the 29M+ rows are never eagerly loaded; only an aggregated `group_by` result is. **No credit-rating field exists in this public data** (excluded as proprietary, along with GVKEY); this validates/enriches the existing spread-*level* factor; it cannot build a rating-migration matrix (the `credit_migration` factor takes its matrix from ESMA's CEREP instead, see [COVERAGE](/projects/financescenarios/docs/coverage)).
- **`equity_risk_neutral_model.py`/`equity_risk_neutral_controller.py`**: compares a risk-neutral (Q-measure) equity GBM's simulated terminal-price distribution (`equities_controller.Equities.calibrate_risk_neutral()`, flat ATM-implied or realized volatility) against the market's own risk-neutral density at the same expiration, extracted from real option prices via the [Breeden-Litzenberger (1978)](https://doi.org/10.1086/296025) theorem (`Toolkit.options.get_risk_neutral_density`, SVI-smile-based). Unlike NAIC/the bond panel above, this isn't a third-party dataset: both sides come from the same market (FinanceToolkit's live option chains), so it's a check of the flat-vol GBM *assumption* against the market's actual (generally skewed/fat-tailed) implied shape, not an outside-source cross-check.

  There is no expiration exactly `target_horizon_years` out, so `resolve_target_expiration` picks the nearest live one and recomputes the horizon from *that* date using FinanceToolkit's own calendar-days/365 day count, so the simulated GBM and the market density agree on maturity to the day; `risk_free_rate`/`dividend_yield` must be passed identically to both the GBM calibration and the density call, or a cost-of-carry mismatch would masquerade as a shape mismatch.

  Reports the 1-Wasserstein distance between the two terminal CDFs (primary, in price units: "the model's and market's terminal-price views differ by $X on average") and a one-sample KS statistic/p-value (secondary, catches a sharp local tail mismatch Wasserstein's average could hide). Called directly, like the rest of `financescenarios/validation/`.

Every fetcher above caches downloaded files under `.cache/validation/` by default (override via `FINANCESCENARIOS_VALIDATION_CACHE_DIR`), never committed to this repository. `equity_risk_neutral_*` is the exception: it makes live FinanceToolkit calls only (option chains, implied volatility, risk-neutral density), nothing to cache locally.

## Published calibrations

A calibration is what the model learnt from history. Publishing one fixes it under a version tag, so a run can say exactly which one it used and anyone can reproduce its scenarios, and checks it before release, so a broken fit is caught before anybody simulates with it.

`release_controller.publish_calibration` calibrates from named profiles and writes `<output_dir>/<version>/`:

- `calibration.json`, the calibration itself;
- `manifest.json`, with the version, date, profiles, data window, package versions and a SHA-256 hash of the full configuration;
- `checks.json` and `report.md`, the validation report.

The checks (`release_model`), each pass, warn or fail with its numbers and a plain-language explanation:

| Check | Fails or warns when |
|:------|:--------------------|
| Every factor calibrated | A configured factor's fit failed and it was left out (warn). |
| Parameters in a plausible range | A rate's long-run level is outside -5% to 25%, or a half-life is outside about a week to 50 years (warn). |
| Valid correlation matrix | The matrix is not symmetric, has no unit diagonal or has a negative eigenvalue (fail). |
| Simulation reproduces the correlations | The simulated moves miss the calibrated correlation of a pair the model does not link directly by over 0.1 (warn) or 0.25 (fail); directly linked pairs are reported, not graded. |
| Simulated volatility matches history | A factor's simulated yearly volatility is outside 0.67-1.5 times its history's (warn) or 0.33-3 times (fail). |
| Reproducible under a seed | Two runs with the same seed differ (fail). |
| Every path is finite | Any path holds NaN or infinity (fail). |

`scenarios.validate(result)` runs the same checks on any run of your own, except the seeded-reproducibility one, and returns them as one pass/warn/fail table with a plain-language meaning per check.

A version is never overwritten: publishing an existing one raises. `simulate_release(folder)` replays a release with its own engine settings and no network access, after checking its profiles still hash to the published configuration; `load_release` returns the calibration and manifest for `simulate(calibration=...)`. If the hash differs, the profiles have changed since publication and would describe different factors than the calibration holds, so the replay is refused rather than silently mixing the two.

### Yearly releases

Reference calibrations are not kept in the repository. The yearly pipeline is defined to run every 1 January (and on demand), but its GitHub Actions workflow file still has to be added to `.github/workflows/` by the maintainer: committing a workflow file needs a token with the `workflow` scope. Until then a release is made by hand with the same command the workflow runs:

```bash
python -m financescenarios.release --factor-set default --factor-set broad
```

This publishes both factor sets under that day's version and packages them for a GitHub release (`package_release_assets`); `--output-dir`, `--version`, `--settings` and `--n-simulations` override the defaults, see `--help`. The workflow then attaches the files to a GitHub release tagged `calibration-YYYY.MM.DD`, with each set's status and report as the release notes. It needs the repository secrets `FINANCIAL_MODELING_PREP_API_KEY` and `FRED_API_KEY`.

To use one as reference or example data:

```python
from financescenarios.release.release_controller import download_release, simulate_release

folder = download_release("latest", factor_set="default")  # or a version such as "2027.01.01"
result = simulate_release(folder)
```

`download_release` keeps releases in `~/.cache/financescenarios/calibrations/<version>/<factor_set>/`, so later calls work offline. Preparing the first release caught a real bug: the `spy_yield` dividend yield failed in every default run because the shared Toolkit's pre-history rows carried a 0 dividend without a price.

## Warnings Worth Reading

Some problems do not stop a run but do weaken a result. They are logged as warnings, and the first two below are also recorded in a saved run's manifest, so they are still visible when someone opens it later:

- **A factor failed to calibrate** and was left out, with the reason, in `calibration_failures`.
- **A correlation was set to 0** because the two factors shared fewer than 5 observations, in `correlation_fallback_pairs`.
- **A correlation rests on fewer than 12 shared observations**, or **two factors correlate above 0.98**, which usually means the same ticker or driver is configured twice.
- **A mean-reverting factor did not settle** where its fitted parameters say it should. `simulate()` checks this automatically once the horizon is long enough; see `diagnose()` in [simulation-engine](/projects/financescenarios/docs/simulation-engine#scenarioset).
- **A filter left fewer than 30 scenarios**, too few for percentiles to mean much.

See [How the Correlations Are Estimated](/projects/financescenarios/docs/simulation-engine#how-the-correlations-are-estimated) for the background on the correlation warnings.

## Static checks

Beyond the test suite, these run against the whole `financescenarios/` package:

| Tool | Checks |
|---|---|
| `black` | Code formatting. |
| `ruff` | Style, common bugs, complexity, and a security-focused rule set. |
| `ty` | Static type checking against the type hints on every function. |
| `bandit` | Security-specific static analysis. |
| `codespell` | Spelling mistakes in code and comments. |

```bash
uv run black --target-version py311 --check financescenarios tests
uv run ruff check financescenarios tests
uv run ty check financescenarios
uv run bandit -r financescenarios -q
uv run codespell financescenarios tests
```

## What is not validated

Being clear about the current limits of the model is part of trusting it:

- Cross-factor dependence is one linear correlation matrix, as described in `Dependence`, and it stays the same over the whole horizon. `engine.shock_distribution: "student_t"` adds joint tail risk through one shared t-copula (see [simulation-engine](/projects/financescenarios/docs/simulation-engine#fat-tails-and-tail-dependence)), but tail dependence that differs by pair or is asymmetric is not captured.
- Every factor calibrates real-world (P-measure) by default; `interest_rates`/`inflation`/`equities`/`fx`/`commodities` additionally support an opt-in risk-neutral (Q-measure) calibration (see [configuration](/projects/financescenarios/docs/configuration)'s Real-world and risk-neutral measures section), but that v1 scope stops short of a full arbitrage-free volatility surface; see that page's own limits.
- `interest_rates`/`inflation`/`equities`/`unemployment`/`fx` are all multi-instance and worldwide (several countries'/regions' clouds, correlation-linked), but each region's factors are still calibrated and simulated in their own native units; there's no FX-conversion/re-denomination *at the factor level*. An optional downstream `reporting` layer (see `Reporting`) can convert a level factor's native-currency path into one reporting currency for display/aggregation after simulation, but this never feeds back into calibration or correlation. `credit` covers the US, Germany, Australia and the euro area's borrowing cost (see `Credit`); `yield_curve`/`real_estate`/`leading_indicator`/`mortality` stay single-country in v1.
- `n_regimes` for the equity model, and every belief override, is a user choice. Nothing in the code selects the number of regimes automatically or checks whether a belief override is economically reasonable; it only checks that the override has the right shape.
- There is no scenario reduction or moment-matching step: every simulated path is returned as-is, none are selected or reweighted to reduce the number of scenarios while preserving key statistical properties.
