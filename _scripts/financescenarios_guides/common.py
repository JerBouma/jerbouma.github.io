"""Shared helpers for the charts of the Finance Scenarios documentation pages.

Every page uses one run: the default settings and factor set, calibrated on 2026-10-25 (the README's saved calibration,
docs/assets/readme/calibration.json in the finance-scenarios repository), simulated with seed 42 and 2,000 scenarios.
Passing that calibration to simulate() reproduces the run exactly; leaving it out calibrates on the day you run it.

Each page has its own builder, run with a Python environment that has `financescenarios` installed:

    FINANCESCENARIOS_REPO=/path/to/FinanceScenarios python _scripts/financescenarios_guides/interest_rates.py

It writes assets/data/financescenarios-guides/<page>.json, drawn by assets/js/ft-charts.js.
"""

import json
import os
import warnings
from pathlib import Path

import numpy as np

from financescenarios import CalibrationResult, Scenarios, set_display, set_log_level

warnings.simplefilter("ignore")
set_log_level("WARNING")
set_display(decimals=4, text=60)

REPO = Path(os.environ.get("FINANCESCENARIOS_REPO", "/sources/finance-scenarios"))
CALIBRATION = REPO / "docs" / "assets" / "readme" / "calibration.json"
CALIBRATION_RISK_NEUTRAL = REPO / "docs" / "assets" / "readme" / "calibration_risk_neutral.json"
OUTPUT = Path(__file__).resolve().parents[2] / "assets" / "data" / "financescenarios-guides"
NUMBERS: dict = {}


def default_run(n_simulations: int = 2000, seed: int = 42, **kwargs):
    """The page's `scenarios` and `result`, from the saved calibration of 2026-10-25."""
    calibration = CalibrationResult.load(CALIBRATION)
    scenarios = Scenarios.from_profiles(settings="default", factor_set="default")
    result = scenarios.simulate(n_simulations=n_simulations, seed=seed, calibration=calibration, **kwargs)
    return scenarios, calibration, result


def labels(dates) -> list[str]:
    return [str(d)[:10] for d in dates]


def values(array, digits: int = 5) -> list:
    return [None if v is None or not np.isfinite(v) else round(float(v), digits) for v in np.asarray(array, float)]


def quantiles(paths: np.ndarray, inner: bool = False) -> dict:
    """q05, q5 (the median: ft-charts names the centre line q5) and q95 per date, plus q25 and q75 if inner."""
    q = np.nanquantile(paths, [0.05, 0.25, 0.5, 0.75, 0.95], axis=0)
    out = {"q05": values(q[0]), "q5": values(q[2]), "q95": values(q[4])}
    if inner:
        out.update(q25=values(q[1]), q75=values(q[3]))
    return out


def growth_of_100(run, factor: str) -> np.ndarray:
    """What 100 put in the factor at the start is worth at each date, per scenario."""
    prices = run.metric_paths(factor, levels=True)
    return 100 * prices / prices[:, :1]


def fan(result, factors: dict, fmt: str = "percent", levels: bool = False, inner: bool = False, index100: bool = False,
        **extra) -> dict:
    """A fan chart: one band per factor, {display name: factor}, from the run's metric paths (as growth of 100 with
    index100)."""
    series = []
    for name, factor in factors.items():
        if isinstance(factor, np.ndarray):
            paths = factor
        else:
            paths = growth_of_100(result, factor) if index100 else result.metric_paths(factor, levels=levels)
        series.append({"name": name, **quantiles(paths, inner=inner and len(factors) == 1)})
    return {"type": "fan", "x": labels(result.dates), "series": series, "format": fmt, **extra}


def runs_fan(runs: dict, factor: str, fmt: str = "percent", levels: bool = False, index100: bool = False,
             **extra) -> dict:
    """One band per run of the same factor, {display name: ScenarioSet} (as growth of 100 with index100)."""
    first = next(iter(runs.values()))
    series = [
        {"name": name, **quantiles(growth_of_100(run, factor) if index100 else run.metric_paths(factor, levels=levels))}
        for name, run in runs.items()
    ]
    return {"type": "fan", "x": labels(first.dates), "series": series, "format": fmt, **extra}


def hist(sample, width: float, xname: str, markers: dict, fmt: str = "percent") -> dict:
    sample = np.asarray(sample, float)
    sample = sample[np.isfinite(sample)]
    edges = np.arange(np.floor(sample.min() / width) * width, sample.max() + width, width)
    counts, edges = np.histogram(sample, bins=edges)
    return {
        "type": "hist", "bins": [round(float(e + width / 2), 6) for e in edges[:-1]], "counts": [int(c) for c in counts],
        "width": width, "format": fmt, "xname": xname,
        "markers": [{"label": k, "value": round(float(v), 6)} for k, v in markers.items()],
    }


def bar(x, series: dict, fmt: str = "percent", kind: str = "bar", **extra) -> dict:
    return {"type": kind, "x": [str(v) for v in x], "series": [{"name": k, "data": values(v)} for k, v in series.items()],
            "format": fmt, **extra}


def tabs(specs: dict) -> dict:
    return {"type": "tabs", "tabs": [{"label": k, **v} for k, v in specs.items()]}


def write(page: str, charts: dict, titles: dict) -> None:
    for chart_id, chart in charts.items():
        chart["title"] = titles[chart_id]
        chart["period"] = False
    (OUTPUT / f"{page}.json").write_text(json.dumps({"charts": charts}, separators=(",", ":")))
    print(page, len(charts), "charts")
