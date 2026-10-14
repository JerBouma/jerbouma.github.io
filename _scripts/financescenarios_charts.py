"""Builds the charts on /projects/financescenarios from the README's own run.

The page shows the same run as the Finance Scenarios README: the README notebook
saves its calibrations (docs/assets/readme/calibration*.json) and simulates with
seed 42, so replaying them here gives back exactly the same scenarios. The tables
on the page are the README's; this script draws the interactive charts and
writes the calibration date the README states to _data/financescenarios_run.yml.

    FINANCIAL_MODELING_PREP_API_KEY=... FRED_API_KEY=... \
        python _scripts/financescenarios_charts.py /path/to/FinanceScenarios

The backtest reads market history, so run it on the README's calibration date.
Writes assets/data/financescenarios-charts.json, drawn by assets/js/ft-charts.js.
"""

import json
import re
import sys
from pathlib import Path

import numpy as np

import polars as pl

from financescenarios import CalibrationResult, Portfolio, Scenarios, Solvency, compare_runs
from financescenarios.config.config_model import risk_neutral_config

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "assets" / "data" / "financescenarios-charts.json"
RUN_DATE = ROOT / "_data" / "financescenarios_run.yml"
REPO = Path(sys.argv[1] if len(sys.argv) > 1 else "/sources/finance-scenarios")
README_RUN = REPO / "docs" / "assets" / "readme"
SEED = 42
QUANTILES = ["q0.05", "q0.25", "q0.5", "q0.75", "q0.95"]


def r(values, digits=5):
    return [None if v is None or not np.isfinite(v) else round(float(v), digits) for v in values]


def fan(result, factor, name, levels=False, digits=5):
    stats = result.summary_statistics(factor, levels=levels)
    return {"name": name, **{q.replace("q0.", "q"): r(stats[q].to_list(), digits) for q in QUANTILES}}, [
        d.strftime("%Y-%m") for d in stats["date"].to_list()
    ]


def histogram(values, markers, fmt, title, xname, digits=5):
    values = np.asarray(values, dtype=float)
    values = values[np.isfinite(values)]
    counts, edges = np.histogram(values, bins=min(60, max(20, int(2 * np.sqrt(values.size)))))
    centers = (edges[:-1] + edges[1:]) / 2
    return {
        "type": "hist", "title": title, "xname": xname, "format": fmt,
        "bins": r(centers, digits), "counts": [int(c) for c in counts], "width": round(float(edges[1] - edges[0]), digits + 2),
        "markers": [{"label": label, "value": round(float(value), digits)} for label, value in markers],
    }


def main() -> None:
    charts = {}

    scenarios = Scenarios.from_profiles(settings="default", factor_set="default")
    calibration = CalibrationResult.load(README_RUN / "calibration.json")
    run_date = re.search(r"calibrated on (\d{4}-\d{2}-\d{2})", (REPO / "README.md").read_text()).group(1)

    def simulate(**kwargs):
        return scenarios.simulate(calibration=calibration, n_simulations=2000, seed=SEED, **kwargs)

    result = simulate()
    series, dates = [], None
    tabs = []
    for factor, name in [("united_states_short_rate", "US short rate"), ("united_states_inflation", "US inflation")]:
        band, dates = fan(result, factor, name)
        tabs.append({"label": name, "type": "fan", "title": "", "x": dates, "format": "percent", "series": [band]})
    # equities as the value of 100 invested, so the widening range of outcomes shows
    band, dates = fan(result, "us_broad", "US equities", levels=True)
    start = band["q5"][0]
    band = {k: v if k == "name" else [None if x is None else round(100 * x / start, 1) for x in v] for k, v in band.items()}
    tabs.append({"label": "US equities (100 invested)", "type": "fan", "title": "", "x": dates, "format": "amount", "series": [band]})
    charts["simulation"] = {"type": "tabs", "title": "2,000 simulated scenarios, five years ahead", "tabs": tabs}

    terminal = result.metric_paths("us_broad")[:, -1]
    charts["distribution"] = histogram(
        terminal, [("5th percentile", np.quantile(terminal, 0.05)), ("Median", np.quantile(terminal, 0.5)),
                   ("95th percentile", np.quantile(terminal, 0.95))],
        "percent", "Where the five-year US equity return lands, across 2,000 scenarios", "Annualized return over five years")

    values = Portfolio.from_preset(result, preset="balanced_60_40").compute(initial_value=100_000, rebalance_every=12)
    band, dates = fan(values, "portfolio", "60/40 portfolio", levels=True, digits=0)
    charts["portfolio"] = {"type": "fan", "title": "Value of 100,000 in a 60/40 portfolio, rebalanced yearly",
                           "x": dates, "format": "amount", "series": [band]}

    runs = {"Baseline": result}
    for regime, name in [("oil_shock", "Oil Shock"), ("oil_crisis", "Oil Crisis"), ("climate_collapse", "Climate Collapse")]:
        runs[name] = simulate(regime=regime)
    fans = []
    for name, run in runs.items():
        band, dates = fan(run, "united_states_inflation", name)
        fans.append(band)
    charts["regimes"] = {"type": "fan", "title": "US inflation under three stress regimes against the baseline",
                         "x": dates, "format": "percent", "series": fans}

    backtest = Portfolio.backtest(scenarios, ["balanced_60_40", "all_weather", "permanent_portfolio"])
    hist_values = backtest.compute(initial_value=100_000, rebalance_every=12)
    print("backtest series:", hist_values.factor_names)
    paths = {name: hist_values.metric_paths(name, levels=True)[0] for name in hist_values.factor_names}
    start = hist_values.dates[0].strftime("%B %Y")
    charts["backtest"] = {"type": "line", "title": f"What 100,000 in each mix actually did since {start}",
                          "x": [d.strftime("%Y-%m") for d in hist_values.dates], "format": "amount",
                          "series": [{"name": name, "data": r(path, 0)} for name, path in paths.items()]}

    # the risk-neutral run has its own market-consistent calibration, saved next to the real-world one
    market = Scenarios.from_config(risk_neutral_config(scenarios.config), toolkit=scenarios._toolkit)
    risk_neutral = market.simulate(calibration=CalibrationResult.load(README_RUN / "calibration_risk_neutral.json"),
                                   n_simulations=2000, seed=SEED)
    solvency = Solvency(real_world=result, risk_neutral=risk_neutral)
    assets = Portfolio.from_preset(result, preset="balanced_60_40").compute(initial_value=60_000, rebalance_every=12)
    cashflows = [10_000] * 5
    own_funds = solvency._own_funds(cashflows, assets)
    step = result.step_at(1.0)
    deflator = result.discount_factor_paths(solvency.short_rate)[:, step]
    outcome = deflator * own_funds[:, step]
    today = float(own_funds[:, 0].mean())
    charts["solvency"] = histogram(
        outcome, [("Own funds today", today), ("1-in-200 outcome", np.quantile(outcome, 0.005))],
        "amount", "Own funds after one year across 2,000 scenarios, discounted to today", "Own funds", digits=0)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps({"charts": charts, "calibrated": run_date}, separators=(",", ":")))
    RUN_DATE.write_text(f"# Written by _scripts/financescenarios_charts.py: the day the landing page's run was calibrated\ndate: {run_date}\n")
    print(f"Wrote {len(charts)} charts to {OUTPUT} ({OUTPUT.stat().st_size // 1024} KB)")
    for name, run in runs.items():
        print(name, {f: round(float(run.metric_paths(f)[:, -1].mean()), 4) for f in ["united_states_inflation", "united_states_short_rate", "us_broad", "europe"]})
    # the page's tables and the numbers its text quotes, all from this run
    pl.Config.set_tbl_rows(50); pl.Config.set_tbl_cols(20); pl.Config.set_float_precision(4); pl.Config.set_tbl_width_chars(400); pl.Config.set_fmt_str_lengths(200)
    print(result.describe())
    print(result.summary_statistics("us_broad"))
    print(values.summary_statistics("portfolio", levels=True).tail(1))
    print(values.summary_statistics("portfolio").tail(1))
    sixty_forty = Portfolio.from_preset(result, preset="balanced_60_40")
    sixty_forty.compute(initial_value=100_000, rebalance_every=12)
    print(sixty_forty.summary())
    print(compare_runs({"baseline": result, "oil_crisis": runs["Oil Crisis"]}))
    print(backtest.factor_exposure())
    print(solvency.report(cashflows=cashflows, assets=assets))
    for f in ["us_broad"]:
        try:
            print(f, "mean return", round(float(result.metric_paths(f)[:, -1].mean()), 4))
        except Exception:
            pass
    for name, path in paths.items():
        drawdown = path / np.maximum.accumulate(path) - 1
        print(name, "end value", round(float(path[-1])), "deepest fall", round(float(drawdown.min()), 3),
              hist_values.dates[int(drawdown.argmin())])
    print("SCR (today - 1-in-200):", round(today - float(np.quantile(outcome, 0.005))))


if __name__ == "__main__":
    main()
