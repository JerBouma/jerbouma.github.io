"""Builds the data behind the interactive charts on /projects/financetoolkit.

Runs the same Finance Toolkit calls as the examples on that page and writes
the results to assets/data/financetoolkit-charts.json, which the page draws
with ECharts. Rerun it to refresh the charts:

    pip install financetoolkit
    python _scripts/financetoolkit_charts.py

Without a Financial Modeling Prep key the Toolkit falls back to Yahoo Finance,
which covers the last five years of financial statements; set
FINANCIAL_MODELING_PREP_KEY for a longer history. The ICE BofA yields are read
straight from FRED's public CSV download, which needs no key.
"""

import io
import json
import logging
import os
import time
import urllib.request
import warnings
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd
from financetoolkit import Discovery, Economics, Portfolio, Toolkit
from financetoolkit.ratios import profitability_model

warnings.filterwarnings("ignore")
logging.disable(logging.CRITICAL)

START = "2017-12-31"
OUTPUT = Path(__file__).resolve().parent.parent / "assets" / "data" / "financetoolkit-charts.json"
API_KEY = os.environ.get("FINANCIAL_MODELING_PREP_KEY", "")


def label(value) -> str:
    """Dates, periods and numbers as short axis labels."""
    if isinstance(value, pd.Period):
        # weekly periods print as a date range; the week's last day reads better
        if value.freqstr.startswith("W"):
            return value.end_time.strftime("%Y-%m-%d")
        return str(value)
    if isinstance(value, (pd.Timestamp, date)):
        return pd.Timestamp(value).strftime("%Y-%m-%d")
    return str(value)


def values(series: pd.Series, digits: int = 4) -> list:
    """A series as a JSON list, with gaps as null."""
    return [None if pd.isna(v) or np.isinf(v) else round(float(v), digits) for v in series]


def sec_annual_facts(cik: str) -> dict:
    """Fiscal-year values from a company's 10-K filings on SEC EDGAR, per XBRL tag."""
    request = urllib.request.Request(
        f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json",
        headers={"User-Agent": "jeroenbouma.com jer.bouma@gmail.com"},
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        gaap = json.load(response)["facts"]["us-gaap"]
    facts = {}
    for tag, data in gaap.items():
        rows = {}
        for row in data.get("units", {}).get("USD", []):
            if row.get("form") != "10-K":
                continue
            end = pd.Timestamp(row["end"])
            # flows must cover a full year; balances are a single date
            if "start" in row and (end - pd.Timestamp(row["start"])).days < 350:
                continue
            rows[end.year] = row["val"]
        if rows:
            facts[tag] = pd.Series(rows, dtype=float).sort_index()
    return facts


def line(x, series: dict, fmt: str = "num", kind: str = "line", **extra) -> dict:
    """A chart; periods where every series is empty are left out."""
    x = [label(v) for v in x]
    data = {name: values(s) for name, s in series.items()}
    keep = [i for i in range(len(x)) if any(d[i] is not None for d in data.values())]
    return {
        "type": kind,
        "x": [x[i] for i in keep],
        "series": [{"name": name, "data": [d[i] for i in keep]} for name, d in data.items()],
        "format": fmt,
        **extra,
    }


# The regression in the README's Econometrics example. The README doesn't say
# which window it used, so the chart shows its published table rather than a
# fresh run: coefficient, standard error and p-value per ticker.
README_OLS = {
    "TSM": (-0.0054, 0.0523, 0.9182),
    "QCOM": (0.1432, 0.0361, 0.0001),
    "SWKS": (0.2141, 0.0484, 0.0000),
    "MSFT": (0.3036, 0.0864, 0.0005),
    "GOOGL": (0.1448, 0.0689, 0.0369),
    "AMZN": (0.0617, 0.0529, 0.2448),
    "META": (-0.0132, 0.0389, 0.7343),
    "NVDA": (-0.0024, 0.0415, 0.9542),
    "XOM": (-0.0291, 0.0373, 0.4364),
    "PG": (0.2858, 0.0707, 0.0001),
}


def discovery_chart(api_key: str) -> dict:
    """The README's stock screener: US semiconductor companies above $100 billion."""
    discovery = Discovery(api_key=api_key)
    screen = discovery.get_stock_screener(
        industry="Semiconductors", country="US", exchange="NASDAQ", market_cap_higher=100_000_000_000, is_etf=False
    )
    caps = screen["Market Cap"].sort_values(ascending=False)
    return {
        "type": "hbar",
        "title": "US semiconductor companies worth more than $100 billion, by market cap",
        "x": list(caps.index),
        "series": [{"name": "Market cap", "data": [float(v) for v in caps]}],
        "format": "usd",
    }


def econometrics_chart() -> dict:
    """Coefficients with their 95% confidence interval, largest first."""
    rows = sorted(README_OLS.items(), key=lambda item: item[1][0], reverse=True)
    return {
        "type": "coef",
        "title": "Apple's weekly returns regressed on ten stocks: coefficients and 95% confidence intervals",
        "x": [ticker for ticker, _ in rows],
        "coef": [c for _, (c, _, _) in rows],
        "low": [round(c - 1.96 * se, 4) for _, (c, se, _) in rows],
        "high": [round(c + 1.96 * se, 4) for _, (c, se, _) in rows],
        "p": [p for _, (_, _, p) in rows],
    }


def main() -> None:
    companies = Toolkit(["AAPL", "MSFT"], api_key=API_KEY, start_date=START, benchmark_ticker="SPY")
    charts = {}

    # Statements first: the models module relies on them being loaded
    # EBITDA: Apple against Alphabet, whose fiscal years line up with Apple's
    # closely enough that both have the same latest reported year (Microsoft's
    # year ends in June, so it reports a year Apple has not finished yet)
    peers = Toolkit(["AAPL", "GOOGL"], api_key=API_KEY, start_date=START)
    ebitda = peers.get_income_statement().xs("EBITDA", level=1)
    charts["statements"] = line(
        ebitda.columns,
        {"Apple": ebitda.loc["AAPL"] / 1e9, "Alphabet": ebitda.loc["GOOGL"] / 1e9},
        fmt="billions",
        kind="bar",
        title="EBITDA (USD billions)",
    )
    companies.get_income_statement()  # the models module relies on the statements

    historical = companies.get_historical_data(period="weekly")
    cumulative = historical["Cumulative Return"]
    charts["historical"] = line(
        cumulative.index,
        {"Apple": cumulative["AAPL"], "Microsoft": cumulative["MSFT"], "S&P 500": cumulative["Benchmark"]},
        fmt="multiple",
        title="Cumulative return (1 = start)",
    )

    # Profitability ratios for Microsoft, fiscal 2020 to the latest year. The
    # statements come from Microsoft's 10-K filings on SEC EDGAR (free, no key),
    # so the period does not depend on an FMP subscription; the ratios are
    # calculated with the Finance Toolkit's own formulas.
    facts = sec_annual_facts("0000789019")
    revenue = facts["RevenueFromContractWithCustomerExcludingAssessedTax"]
    equity, assets = facts["StockholdersEquity"], facts["Assets"]
    # total debt as the Toolkit defines it: borrowings plus lease liabilities
    debt = sum(facts[tag].reindex(revenue.index).fillna(0) for tag in
               ["LongTermDebt", "CommercialPaper", "OperatingLeaseLiability", "FinanceLeaseLiability"])
    average = lambda s: (s + s.shift(1)) / 2  # noqa: E731
    ratios = pd.DataFrame({
        "Gross Margin": profitability_model.get_gross_margin(revenue, revenue - facts["GrossProfit"]),
        "Operating Margin": profitability_model.get_operating_margin(facts["OperatingIncomeLoss"], revenue),
        "Net Profit Margin": profitability_model.get_net_profit_margin(facts["NetIncomeLoss"], revenue),
        "Return on Equity": profitability_model.get_return_on_equity(facts["NetIncomeLoss"], average(equity)),
        "Return on Assets": profitability_model.get_return_on_assets(facts["NetIncomeLoss"], average(assets)),
        "Return on Invested Capital": profitability_model.get_return_on_invested_capital(
            facts["NetIncomeLoss"], facts["PaymentsOfDividendsCommonStock"], average(equity), average(debt)),
    }).loc[lambda f: f.index >= 2020].dropna().T
    charts["ratios"] = {
        "type": "kpis",
        "title": "Profitability ratios for Microsoft, fiscal years",
        "x": list(ratios.index),
        "series": [{"name": str(year), "data": values(ratios[year])} for year in ratios.columns],
        "format": "percent",
    }

    # Extended DuPont: five components that multiply into Return on Equity
    # the models module needs all three statements loaded first
    companies.get_balance_sheet_statement()
    companies.get_cash_flow_statement()
    dupont = companies.models.get_extended_dupont_analysis()
    parts = [("Interest Burden Ratio", "Interest burden", "percent"),
             ("Tax Burden Ratio", "Tax burden", "percent"),
             ("Operating Profit Margin", "Operating margin", "percent"),
             ("Asset Turnover", "Asset turnover", "multiple"),
             ("Equity Multiplier", "Equity multiplier", "multiple")]
    tabs = []
    for ticker, name in [("AAPL", "Apple"), ("MSFT", "Microsoft")]:
        frame = dupont.loc[ticker].dropna(axis=1, how="any")
        tabs.append({
            "label": name,
            "years": [label(c) for c in frame.columns],
            "components": [{"name": short, "format": fmt, "data": values(frame.loc[row])} for row, short, fmt in parts],
            "result": {"name": "Return on equity", "format": "percent", "data": values(frame.loc["Return on Equity"])},
        })
    charts["models"] = {"type": "dupont", "title": "Extended DuPont Analysis", "tabs": tabs}

    # Greeks for Apple: one line per expiration, against the strike price
    greek_tabs = []
    for name, getter in [("Delta", companies.options.get_delta), ("Gamma", companies.options.get_gamma),
                         ("Theta", companies.options.get_theta), ("Vega", companies.options.get_vega)]:
        frame = getter(expiration_time_range=180).loc["AAPL"]
        columns = list(frame.columns)
        pick = sorted({columns[min(len(columns) - 1, i)] for i in (29, 89, 179)})
        greek_tabs.append({"label": name, **line(frame.index, {f"Expires {label(c)}": frame[c] for c in pick}, fmt="num", xname="Strike price")})
    charts["greeks"] = {"type": "tabs", "title": "Option Greeks for Apple", "tabs": greek_tabs}

    factors = companies.performance.get_factor_asset_correlations(period="quarterly")
    charts["performance"] = {
        "type": "tabs",
        "title": "Correlation with the Fama-French factors",
        "tabs": [
            {"label": ticker, **line(factors.index, {f: factors[ticker][f] for f in factors[ticker].columns}, fmt="num")}
            for ticker in ["AAPL", "MSFT"]
        ],
    }

    var = companies.risk.get_value_at_risk(period="weekly", within_period=True)
    charts["risk"] = line(
        var.index,
        {"Apple": var["AAPL"], "Microsoft": var["MSFT"], "S&P 500": var["Benchmark"]},
        fmt="percent",
        title="Weekly Value at Risk (95%)",
    )

    ichimoku = companies.technicals.get_ichimoku_cloud()
    daily = companies.get_historical_data()["Close"]
    since = ichimoku.index[-260]
    tech_tabs = []
    for ticker, name in [("AAPL", "Apple"), ("MSFT", "Microsoft")]:
        cloud = ichimoku.xs(ticker, axis=1, level=1).loc[since:]
        close = daily[ticker].reindex(cloud.index)
        tech_tabs.append({"label": name, **line(cloud.index, {"Close": close, **{c: cloud[c] for c in cloud.columns}}, fmt="price", cloud=["Leading Span A", "Leading Span B"])})
    charts["technicals"] = {"type": "tabs", "title": "Ichimoku Cloud, last 12 months", "tabs": tech_tabs}

    # ICE BofA effective yields per credit rating, straight from FRED
    ratings = {"AAA": "BAMLC0A1CAAAEY", "AA": "BAMLC0A2CAAEY", "A": "BAMLC0A3CAEY", "BBB": "BAMLC0A4CBBBEY",
               "BB": "BAMLH0A1HYBBEY", "B": "BAMLH0A2HYBEY", "CCC": "BAMLH0A3HYCEY"}
    yields = {}
    for rating, series_id in ratings.items():
        url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}&cosd={START}"
        with urllib.request.urlopen(url, timeout=60) as response:
            frame = pd.read_csv(io.StringIO(response.read().decode()), index_col=0, parse_dates=True)
        yields[rating] = pd.to_numeric(frame.iloc[:, 0], errors="coerce") / 100
    yields = pd.DataFrame(yields).resample("W").last()
    charts["fixedincome"] = line(yields.index, {r: yields[r] for r in yields.columns}, fmt="percent",
                                 title="ICE BofA effective yield by credit rating")

    # the macro dataset is downloaded from GitHub, which now and then answers
    # 503 for a while; then the previous chart is kept
    unemployment = None
    for attempt in range(3):
        try:
            unemployment = Economics(start_date="2010-01-01").get_unemployment_rate()
            break
        except Exception:
            time.sleep(20)
    if unemployment is not None:
        countries = ["Colombia", "United States", "Sweden", "Japan", "Germany"]
        charts["economics"] = line(unemployment.index, {c: unemployment[c] for c in countries if c in unemployment}, fmt="percent",
                                   title="Unemployment rate")
    elif OUTPUT.exists():
        print("Economics data unavailable, keeping the previous chart")
        charts["economics"] = json.loads(OUTPUT.read_text())["charts"]["economics"]

    # the latest weight and return of every position in the example portfolio
    portfolio = Portfolio(example=True, api_key=API_KEY)
    overview = portfolio.get_positions_overview()
    last = overview.iloc[-1]
    weights = last["Current Weight"].sort_values(ascending=False)
    returns = (last["Cumulative Return"] - 1).reindex(weights.index)
    charts["portfolio"] = {
        "type": "tabs",
        "title": f"Example portfolio on {label(overview.index[-1])}",
        "tabs": [
            {"label": "Weights", **line(weights.index, {"Current weight": weights}, fmt="percent", kind="bar")},
            {"label": "Returns", **line(returns.index, {"Cumulative return": returns}, fmt="percent", kind="bar")},
        ],
    }

    if API_KEY:
        charts["discovery"] = discovery_chart(API_KEY)
    else:
        print("No FMP key, keeping the previous Discovery chart")
        charts["discovery"] = json.loads(OUTPUT.read_text())["charts"]["discovery"]
    charts["econometrics"] = econometrics_chart()

    payload = {"generated": date.today().isoformat(), "charts": charts}
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, separators=(",", ":")))
    print(f"Wrote {len(charts)} charts to {OUTPUT} ({OUTPUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
