"""Builds the charts of articles whose numbers come from a script.

Writes its charts into assets/data/article-charts.json and leaves every other
chart in that file as it is. Rerun it to refresh them:

    pip install financetoolkit -U
    FINANCIAL_MODELING_PREP_KEY=... python _scripts/article_charts.py

Articles covered:

- /articles/screening-undervalued-stocks-finance-toolkit: the screen of 15
  large caps on fiscal 2025 ratios, recalculated on every run. The text of the
  article quotes these numbers, so check it after a refresh.
- /articles/equity-research-family-offices-fmp-mcp: the FMP MCP answers are a
  record of what the server returned on July 17, 2026 (estimates, price
  targets and 13F counts change over time, so they can't be fetched again);
  the Finance Toolkit dashboard is recalculated with prices up to that date.
- The history series (/articles/black-death-economic-effects, ...): one
  event from economic history per article, from the Finance Toolkit's
  historical datasets. These need no key and end at a fixed date, so a rerun
  gives the same charts. Run only these with `python _scripts/article_charts.py history`.
"""

import json
import logging
import os
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from financetoolkit import Economics, Toolkit

warnings.filterwarnings("ignore")
logging.disable(logging.CRITICAL)

OUTPUT = Path(__file__).resolve().parent.parent / "assets" / "data" / "article-charts.json"
API_KEY = os.environ.get("FINANCIAL_MODELING_PREP_KEY", "")


def values(series, digits: int = 4) -> list:
    """A series as a JSON list, with gaps as null."""
    return [None if pd.isna(v) or np.isinf(v) else round(float(v), digits) for v in series]


def years(frame: pd.DataFrame) -> list:
    return [str(c) for c in frame.columns]


# --- Screening for undervalued stocks -------------------------------------

SCREEN = ["AAPL", "MSFT", "INTC", "IBM", "JNJ", "PFE", "MRK", "KO", "WMT", "JPM", "BAC", "XOM", "CVX", "META", "GOOGL"]
YEAR = "2025"
# label positions for points that sit on top of each other
POS_VALUATION = {"PFE": "bottom"}
POS_FINAL = {"XOM": "top", "CVX": "bottom"}


def point(name, x, y, positions):
    p = {"name": name, "x": x, "y": y}
    if name in positions:
        p["pos"] = positions[name]
    return p


def screen_charts() -> dict:
    screener = Toolkit(tickers=SCREEN, api_key=API_KEY, start_date="2022-01-01", progress_bar=False)
    pe = screener.ratios.get_price_to_earnings_ratio()
    ev_ebitda = screener.ratios.get_ev_to_ebitda_ratio()
    roe = screener.ratios.get_return_on_equity()
    # NOPAT over average debt plus equity
    roic = screener.ratios.get_return_on_invested_capital()
    gross = screener.ratios.get_gross_margin()

    snapshot = pd.DataFrame({"pe": pe[YEAR], "ev": ev_ebitda[YEAR], "roic": roic[YEAR]})
    # negative multiples mean nothing, so both have to be positive
    passing = snapshot[(snapshot["pe"] > 0) & (snapshot["pe"] < 20) & (snapshot["ev"] > 0) & (snapshot["ev"] < 18)].index
    candidates = list(snapshot.loc[passing].sort_values("roic", ascending=False).index)
    final = [t for t in candidates if snapshot.loc[t, "roic"] > 0.10]

    priced = snapshot[snapshot["pe"] > 0].sort_values("pe")
    source = "Company filings and share prices via FinancialModelingPrep"
    to_year = [c for c in roic.columns if str(c) <= YEAR]
    charts = {
        "screen-valuation": {
            "type": "scatter",
            "title": "P/E against EV/EBITDA",
            "subtitle": "14 large caps, fiscal 2025, in times; Intel left out (negative earnings); dashed lines at 20x and 18x",
            "source": source,
            "legend": "Orange: below 20x earnings and 18x EBITDA",
            "xname": "P/E",
            "yname": "EV/EBITDA",
            "xformat": "multiple",
            "yformat": "multiple",
            "highlight": [i for i, t in enumerate(priced.index) if t in passing],
            "lines": [{"axis": "x", "value": 20, "label": "P/E 20x"}, {"axis": "y", "value": 18, "label": "EV/EBITDA 18x"}],
            "points": [point(t, round(float(r.pe), 2), round(float(r.ev), 2), POS_VALUATION) for t, r in priced.iterrows()],
        },
        "screen-quality": {
            "type": "tabs",
            "title": "Return on equity, ROIC and gross margin of the five value candidates",
            "subtitle": "Percent; fiscal 2025, and ROIC for each fiscal year from 2022 to 2025",
            "source": source,
            "tabs": [
                {
                    "label": "Fiscal 2025",
                    "type": "bar",
                    "title": "",
                    "x": candidates,
                    "series": [
                        {"name": "ROE", "data": values(roe.loc[candidates, YEAR])},
                        {"name": "ROIC", "data": values(roic.loc[candidates, YEAR])},
                        {"name": "Gross margin", "data": values(gross.loc[candidates, YEAR])},
                    ],
                    "format": "percent",
                },
                {
                    "label": "ROIC 2022 to 2025",
                    "type": "line",
                    "title": "",
                    "x": [str(c) for c in to_year],
                    "series": [{"name": t, "data": values(roic.loc[t, to_year])} for t in candidates],
                    "format": "percent",
                },
            ],
        },
        "screen-final": {
            "type": "scatter",
            "title": "ROIC against EV/EBITDA",
            "subtitle": "All 15 stocks, fiscal 2025; ROIC in percent, EV/EBITDA in times; dashed line at 10% ROIC",
            "source": source,
            "legend": "Orange: passes the valuation filter and earns more than 10% on invested capital",
            "xname": "ROIC",
            "yname": "EV/EBITDA",
            "xformat": "percent",
            "yformat": "multiple",
            "highlight": [i for i, t in enumerate(snapshot.index) if t in final],
            "lines": [{"axis": "x", "value": 0.10, "label": "ROIC 10%"}],
            "points": [point(t, round(float(r.roic), 4), round(float(r.ev), 2), POS_FINAL) for t, r in snapshot.iterrows()],
        },
    }
    return charts


# --- Equity research for family offices: Axon on July 17, 2026 ------------

AS_OF = "2026-07-17"

# What the FMP MCP server returned on July 17, 2026, when AXON closed at $510.28.
FMP_KEY_METRICS = {  # fiscal year: ROE, ROIC, EV/EBITDA, revenue ($M), EBITDA ($M)
    "2021": (-0.057, -0.056, -85.9, 863.4, -117.1),
    "2022": (0.116, 0.031, 53.4, 1189.9, 227.6),
    "2023": (0.109, 0.060, 105.1, 1560.7, 183.4),
    "2024": (0.162, 0.017, 105.2, 2082.5, 437.0),
    "2025": (0.039, -0.011, 236.1, 2779.5, 196.4),
}
FMP_TARGETS = {"High target": 820.0, "Median target": 724.0, "Average target": 658.56, "Share price, July 17": 510.28, "Low target": 440.0}
FMP_DCF = {"Share price, July 17": 510.28, "Levered DCF value": 94.30}
FMP_13F = {  # quarter: holders, new positions, closed positions, share of float held
    "Q2 2025": (1250, 230, 88, 0.827),
    "Q3 2025": (1232, 134, 151, 0.815),
    "Q4 2025": (1195, 160, 193, 0.836),
    "Q1 2026": (1101, 132, 227, 0.833),
}


def axon_charts() -> dict:
    fy = list(FMP_KEY_METRICS)
    km = list(FMP_KEY_METRICS.values())
    quarters = list(FMP_13F)
    q = list(FMP_13F.values())
    charts = {
        "axon-fmp-metrics": {
            "type": "tabs",
            "title": "Axon: FMP key metrics, fiscal 2021 to 2025",
            "tabs": [
                {"label": "ROE and ROIC", "type": "line", "title": "Return on equity and ROIC", "x": fy,
                 "series": [{"name": "ROE", "data": [r[0] for r in km]}, {"name": "ROIC", "data": [r[1] for r in km]}], "format": "percent"},
                {"label": "EV/EBITDA", "type": "bar", "title": "EV/EBITDA (negative in 2021: EBITDA was a loss)", "x": fy,
                 "series": [{"name": "EV/EBITDA", "data": [r[2] for r in km]}], "format": "multiple"},
                {"label": "Revenue and EBITDA", "type": "bar", "title": "Revenue and EBITDA", "x": fy,
                 "series": [{"name": "Revenue", "data": [r[3] * 1e6 for r in km]}, {"name": "EBITDA", "data": [r[4] * 1e6 for r in km]}], "format": "usd"},
            ],
        },
        "axon-fmp-targets": {
            "type": "hbar",
            "title": "Axon: analyst price targets against the share price, July 17, 2026",
            "x": list(FMP_TARGETS),
            "series": [{"name": "Price", "data": list(FMP_TARGETS.values())}],
            "format": "price",
            "highlight": list(FMP_TARGETS).index("Share price, July 17"),
        },
        "axon-fmp-dcf": {
            "type": "hbar",
            "title": "Axon: levered DCF value against the share price, July 17, 2026",
            "x": list(FMP_DCF),
            "series": [{"name": "Per share", "data": list(FMP_DCF.values())}],
            "format": "price",
            "highlight": 0,
        },
        "axon-fmp-13f": {
            "type": "tabs",
            "title": "Axon: institutional ownership from 13F filings",
            "tabs": [
                {"label": "Opened and closed", "type": "bar", "title": "Positions opened and closed per quarter", "x": quarters,
                 "series": [{"name": "Opened", "data": [r[1] for r in q]}, {"name": "Closed", "data": [r[2] for r in q]}], "format": "amount"},
                {"label": "Holders", "type": "line", "title": "Number of institutional holders", "x": quarters,
                 "series": [{"name": "Holders", "data": [r[0] for r in q]}], "format": "amount"},
                {"label": "Share of float", "type": "line", "title": "Share of the float held by institutions", "x": quarters,
                 "series": [{"name": "Held", "data": [r[3] for r in q]}], "format": "percent"},
            ],
        },
    }

    # The Finance Toolkit MCP dashboard: the same calculations as its tools
    # (profitability, liquidity, solvency, valuation, performance), prices up to July 17
    axon = Toolkit(["AXON"], api_key=API_KEY, start_date="2021-01-04", end_date=AS_OF, progress_bar=False)
    ratios = axon.ratios

    def row(frame):
        return values(frame.loc["AXON"] if isinstance(frame, pd.DataFrame) else frame)

    gross = ratios.get_gross_margin()
    fy = years(gross)
    returns = axon.performance.get_returns(period="yearly")
    charts.update({
        "axon-ft-profit": {
            "type": "line",
            "title": "Gross and operating margin, ROE and ROIC, 2021 to 2025",
            "x": fy,
            "series": [
                {"name": "Gross", "data": row(gross)},
                {"name": "Operating", "data": row(ratios.get_operating_margin())},
                {"name": "ROE", "data": row(ratios.get_return_on_equity())},
                {"name": "ROIC", "data": row(ratios.get_return_on_invested_capital())},
            ],
            "format": "percent",
        },
        "axon-ft-balance": {
            "type": "line",
            "title": "Liquidity and leverage, fiscal 2021 to 2025",
            "x": fy,
            "series": [
                {"name": "Current ratio", "data": row(ratios.get_current_ratio())},
                {"name": "Quick ratio", "data": row(ratios.get_quick_ratio())},
                {"name": "Debt to equity", "data": row(ratios.get_debt_to_equity_ratio())},
            ],
            "format": "ratio",
        },
        "axon-ft-valuation": {
            "type": "line",
            "title": "Valuation multiples, fiscal 2021 to 2025",
            "x": fy,
            "series": [
                {"name": "EV/sales", "data": row(ratios.get_ev_to_sales_ratio())},
                {"name": "Price-to-book", "data": row(ratios.get_price_to_book_ratio())},
            ],
            "format": "multiple",
        },
        "axon-ft-returns": {
            "type": "bar",
            "title": "Total return per year against the S&P 500 (SPY), 2026 up to July 17",
            "x": [str(y) for y in returns.index],
            "series": [{"name": "Axon", "data": values(returns["AXON"])}, {"name": "S&P 500", "data": values(returns["Benchmark"])}],
            "format": "percent",
        },
    })
    return charts


# --- History series: the Black Death and English wages ---------------------

BOE = {
    "population": "Population (England)",
    "wages": "Real consumption wages",
    "earnings": "Earnings per head",
    "prices": "Consumer price index",
    "gdp": "Real GDP of England at market prices",
}


def millennium() -> pd.DataFrame:
    """The Bank of England's millennium dataset, by year, with short column names."""
    economics = Economics(start_date="1086-01-01")
    data = economics.get_millennium_of_macroeconomic_data(series=list(BOE.values()))
    data = data[list(BOE.values())].rename(columns={v: k for k, v in BOE.items()})
    data.index = [int(str(year)) for year in data.index]
    return data


def index_to(series: pd.Series, start: int, end: int) -> pd.Series:
    """A series as an index, with its average over start..end set to 100."""
    return series / series.loc[start:end].mean() * 100


def black_death_charts() -> dict:
    data = millennium()
    data["gdp_per_head"] = data["gdp"] / data["population"]

    def line(title, frame, names, fmt, digits=2):
        return {
            "type": "line",
            "title": title,
            "x": [str(year) for year in frame.index],
            "series": [{"name": name, "data": values(frame[column], digits)} for column, name in names.items()],
            "format": fmt,
        }

    span = data.loc[1300:1500]
    charts = {
        "bd-population": line(
            "Population of England (millions)", span.assign(population=span["population"] / 1000),
            {"population": "Population"}, "ratio"),
        "bd-wages": line(
            "Real consumption wages in England", data.loc[1300:1550], {"wages": "Real consumption wage"}, "number"),
    }

    pay = data.loc[1330:1450]
    # an area from zero, so the fall of almost half in three years shows as the drop it was
    charts["bd-population"]["series"][0]["area"] = True

    charts["bd-pay-prices"] = line(
        "Earnings and consumer prices in England (1340-1347 = 100)",
        pd.DataFrame({"earnings": index_to(pay["earnings"], 1340, 1347), "prices": index_to(pay["prices"], 1340, 1347)}),
        {"earnings": "Earnings per head", "prices": "Consumer prices"}, "number", 1)

    output = pd.DataFrame({
        "gdp": index_to(pay["gdp"], 1340, 1347),
        "gdp_per_head": index_to(pay["gdp_per_head"], 1340, 1347),
    })
    charts["bd-output"] = {
        "type": "tabs",
        "title": "Real GDP of England (1340-1347 = 100)",
        "tabs": [
            {**line("Real GDP of England (1340-1347 = 100)", output, {"gdp": "Real GDP"}, "number", 1), "label": "Real GDP"},
            {**line("Real GDP per head in England (1340-1347 = 100)", output, {"gdp_per_head": "Real GDP per head"}, "number", 1),
             "label": "Real GDP per head"},
        ],
    }

    long_run = data.loc[1250:1700]
    charts["bd-long-run"] = line(
        "Population and real wages in England (1340-1347 = 100)",
        pd.DataFrame({
            "population": index_to(long_run["population"], 1340, 1347),
            "wages": index_to(long_run["wages"], 1340, 1347),
        }),
        {"population": "Population", "wages": "Real consumption wage"}, "number", 1)
    return charts


HISTORY = [black_death_charts]


def main() -> None:
    payload = json.loads(OUTPUT.read_text())
    for build in HISTORY:
        payload["charts"].update(build())
    if sys.argv[1:] != ["history"]:
        if not API_KEY:
            raise SystemExit("Set FINANCIAL_MODELING_PREP_KEY first, or run only the history series with 'history'.")
        payload["charts"].update(screen_charts())
        payload["charts"].update(axon_charts())
    OUTPUT.write_text(json.dumps(payload, indent=1) + "\n")


if __name__ == "__main__":
    main()
