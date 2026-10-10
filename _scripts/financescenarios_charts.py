"""Builds the data behind the interactive charts on /projects/financescenarios.

The simulation, distribution and portfolio charts read the saved run the
landing page's tables come from (runs/readme/<RUN_ID> in the Finance
Scenarios repository), so chart and table always agree. The stress regimes,
the backtest and the Solvency II chart need a live run, which is calibrated
here with the same profiles as the page's examples.

    FINANCIAL_MODELING_PREP_API_KEY=... FRED_API_KEY=... \
        python _scripts/financescenarios_charts.py /path/to/FinanceScenarios

Writes assets/data/financescenarios-charts.json, drawn by assets/js/ft-charts.js.
"""

import json
import sys
from pathlib import Path

import numpy as np

from financescenarios import Portfolio, Scenarios, Solvency, read_run

REPO = Path(sys.argv[1] if len(sys.argv) > 1 else "/sources/finance-scenarios")
RUN_ID = "20261008T211905Z-53984c77"
OUTPUT = Path(__file__).resolve().parent.parent / "assets" / "data" / "financescenarios-charts.json"
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

    # 1-3: the saved run behind the page's tables
    saved = read_run(REPO / "runs" / "readme" / RUN_ID)
    series, dates = [], None
    tabs = []
    for factor, name in [("united_states_short_rate", "US short rate"), ("united_states_inflation", "US inflation"),
                         ("us_broad", "US equities (annualized return)")]:
        band, dates = fan(saved, factor, name)
        tabs.append({"label": name, "type": "fan", "title": "", "x": dates, "format": "percent", "series": [band]})
    charts["simulation"] = {"type": "tabs", "title": "2,000 simulated scenarios, five years ahead", "tabs": tabs}

    terminal = saved.metric_paths("us_broad")[:, -1]
    charts["distribution"] = histogram(
        terminal, [("5th percentile", np.quantile(terminal, 0.05)), ("Median", np.quantile(terminal, 0.5)),
                   ("95th percentile", np.quantile(terminal, 0.95))],
        "percent", "Where the five-year US equity return lands, across 2,000 scenarios", "Annualized return over five years")

    values = Portfolio.from_preset(saved, preset="balanced_60_40").compute(initial_value=100_000, rebalance_every=12)
    band, dates = fan(values, "portfolio", "60/40 portfolio", levels=True, digits=0)
    charts["portfolio"] = {"type": "fan", "title": "Value of 100,000 in a 60/40 portfolio, rebalanced yearly",
                           "x": dates, "format": "amount", "series": [band]}

    # 4-6: live runs
    scenarios = Scenarios.from_profiles(settings="default", factor_set="default")
    result = scenarios.simulate(n_simulations=2000)
    runs = {"Baseline": result}
    for regime, name in [("oil_shock", "Oil Shock"), ("oil_crisis", "Oil Crisis"), ("climate_collapse", "Climate Collapse")]:
        runs[name] = Scenarios.from_profiles(regime=regime).simulate(keep=2000)
    fans = []
    for name, run in runs.items():
        band, dates = fan(run, "united_states_inflation", name)
        fans.append(band)
    charts["regimes"] = {"type": "fan", "title": "US inflation under three stress regimes against the baseline",
                         "x": dates, "format": "percent", "series": fans}

    history = scenarios.history(portfolio="balanced_60_40")
    hist_values = Portfolio.from_preset(history, preset="balanced_60_40").compute(initial_value=100_000, rebalance_every=12)
    path = hist_values.metric_paths("portfolio", levels=True)[0]
    charts["backtest"] = {"type": "line", "title": "What 100,000 in the 60/40 actually did since 2000",
                          "x": [d.strftime("%Y-%m") for d in hist_values.dates], "format": "amount",
                          "series": [{"name": "60/40 portfolio", "data": r(path, 0)}]}

    risk_neutral = scenarios.simulate(n_simulations=2000, measure="risk_neutral")
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
    OUTPUT.write_text(json.dumps({"charts": charts}, separators=(",", ":")))
    print(f"Wrote {len(charts)} charts to {OUTPUT} ({OUTPUT.stat().st_size // 1024} KB)")
    print("backtest end value:", round(float(path[-1])), "| SCR (today - 1-in-200):", round(today - float(np.quantile(outcome, 0.005))))


if __name__ == "__main__":
    main()
