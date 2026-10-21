"""Charts for the Models guide: the same calls as the code on that page."""

import pandas as pd
from financetoolkit import Toolkit

from .common import API_KEY, label, line, values

TICKERS = ["AAPL", "TSLA", "META", "AMZN"]
NAMES = {"AAPL": "Apple", "TSLA": "Tesla", "META": "Meta", "AMZN": "Amazon"}
# the early years of Amazon (equity close to zero) and Tesla (losses) produce
# ratios in the hundreds that flatten every other bar; the charts that show
# ratios therefore start ten years before the latest year
RECENT_YEARS = 10

# the weights of the Altman Z-Score and the Beneish M-Score, as in financetoolkit.models
ALTMAN_WEIGHTS = {
    "Working Capital to Total Assets": ("Working capital", 1.2),
    "Retained Earnings to Total Assets": ("Retained earnings", 1.4),
    "EBIT to Total Assets": ("EBIT", 3.3),
    "Market Value to Total Liabilities": ("Market value", 0.6),
    "Sales to Total Assets": ("Sales", 1.0),
}
BENEISH_WEIGHTS = {
    "Asset Quality Index": ("Asset quality", 0.404),
    "Gross Margin Index": ("Gross margin", 0.528),
    "Sales Growth Index": ("Sales growth", 0.892),
    "Total Accruals to Total Assets": ("Accruals", 4.679),
    "Leverage Index": ("Leverage", -0.327),
    "Days Sales in Receivables Index": ("Receivables", 0.92),
    "Depreciation Index": ("Depreciation", 0.115),
    "SGA Expenses Index": ("SG&A", -0.172),
}
PIOTROSKI_GROUPS = {
    "Profitability": ["Return on Assets Criteria", "Operating Cashflow Criteria",
                      "Change in Return on Assets Criteria", "Accruals Criteria"],
    "Leverage and liquidity": ["Change in Leverage Criteria", "Change in Current Ratio Criteria",
                               "Number of Shares Criteria"],
    "Operating efficiency": ["Gross Margin Criteria", "Asset Turnover Criteria"],
}


def per_company(frame: pd.DataFrame, row: str | None = None) -> dict:
    """One series per company, from a frame indexed by ticker (and row)."""
    return {NAMES[t]: (frame.loc[t] if row is None else frame.loc[t].loc[row]) for t in TICKERS}


def recent(frame: pd.DataFrame, years: int = RECENT_YEARS) -> pd.DataFrame:
    return frame.iloc[:, -years:]


def reference(spec: dict, name: str, level: float) -> dict:
    spec["series"].append({"name": name, "data": [level] * len(spec["x"]), "reference": True})
    return spec


def build() -> dict:
    companies = Toolkit(TICKERS, api_key=API_KEY, start_date="2005-01-01")
    charts = {}

    # Extended DuPont: five components multiplying into ROE, one tab per company
    dupont = companies.models.get_extended_dupont_analysis()
    parts = [("Interest Burden Ratio", "Interest burden", "percent"),
             ("Tax Burden Ratio", "Tax burden", "percent"),
             ("Operating Profit Margin", "Operating margin", "percent"),
             ("Asset Turnover", "Asset turnover", "multiple"),
             ("Equity Multiplier", "Equity multiplier", "multiple")]
    tabs = []
    for ticker in ["AAPL", "META", "AMZN", "TSLA"]:
        frame = recent(dupont.loc[ticker]).dropna(axis=1, how="any")
        tabs.append({
            "label": NAMES[ticker],
            "years": [label(c) for c in frame.columns],
            "components": [{"name": short, "format": fmt, "data": values(frame.loc[row])} for row, short, fmt in parts],
            "result": {"name": "Return on equity", "format": "percent", "data": values(frame.loc["Return on Equity"])},
        })
    charts["models-dupont-extended"] = {
        "type": "dupont",
        "tabs": tabs,
    }

    # WACC: the level for every company, with the 2022 sell-off marked, and
    # Amazon's WACC next to its cost of equity and debt, standardized
    wacc = companies.models.get_weighted_average_cost_of_capital()
    wacc_level = recent(wacc.xs("Weighted Average Cost of Capital", level=1))
    amazon = companies.models.get_weighted_average_cost_of_capital(standardize=True, show_full_results=True).loc["AMZN"]
    amazon = recent(amazon.loc[["Weighted Average Cost of Capital", "Cost of Equity", "Cost of Debt"]])
    level_chart = line(wacc_level.columns, per_company(wacc_level), fmt="percent",
                       markers=[{"x": "2018", "label": "S&P 500 -6%"}, {"x": "2022", "label": "S&P 500 -18%"}])
    level_chart = reference(level_chart, "Zero", 0)
    amazon_chart = line(amazon.columns, {"WACC": amazon.loc["Weighted Average Cost of Capital"],
                                         "Cost of equity": amazon.loc["Cost of Equity"],
                                         "Cost of debt": amazon.loc["Cost of Debt"]}, fmt="ratio")
    amazon_chart["series"][0]["color"] = "#f97316"
    amazon_chart["series"][1]["color"] = "#38bdf8"
    amazon_chart["series"][1]["dashed"] = True
    amazon_chart["series"][2]["color"] = "#34d399"
    charts["models-wacc"] = {
        "type": "tabs",
        "tabs": [
            {"label": "WACC", **level_chart},
            {"label": "Amazon, standardized", **amazon_chart},
        ],
    }

    # Altman Z-Score with the classic zones, and Amazon's score split into its
    # five weighted parts
    altman = companies.models.get_altman_z_score()
    z = recent(altman.xs("Altman Z-Score", level=1))
    z_chart = line(z.columns, per_company(z), fmt="ratio", markers=[{"x": "2022", "label": "Amazon 2.94"}])
    z_chart = reference(z_chart, "Safe (2.99)", 2.99)
    z_chart = reference(z_chart, "Distress (1.81)", 1.81)
    amazon_altman = recent(altman.loc["AMZN"])
    parts_chart = line(amazon_altman.columns,
                       {short: amazon_altman.loc[row] * weight for row, (short, weight) in ALTMAN_WEIGHTS.items()},
                       fmt="ratio", kind="bar", stack=True)
    parts_chart = reference(parts_chart, "Safe (2.99)", 2.99)
    charts["models-altman"] = {
        "type": "tabs",
        "tabs": [
            {"label": "Z-Score", **z_chart},
            {"label": "Amazon, the five parts", **parts_chart},
        ],
    }

    # Piotroski F-Score: 0 to 9 per year and company, and where the points of
    # the latest year come from
    piotroski = companies.models.get_piotroski_score()
    score = recent(piotroski.xs("Piotroski Score", level=1), 6)
    latest = piotroski.columns[-1]
    groups = {group: [piotroski.loc[t].loc[rows, latest].sum() for t in TICKERS] for group, rows in PIOTROSKI_GROUPS.items()}
    charts["models-piotroski"] = {
        "type": "tabs",
        "tabs": [
            {"label": "Score per year", **line(score.columns, per_company(score), kind="bar", fmt="number")},
            {"label": f"Where the points come from, {label(latest)}",
             **line([NAMES[t] for t in TICKERS], {g: pd.Series(v) for g, v in groups.items()}, kind="bar",
                    fmt="number", stack=True)},
        ],
    }

    # DuPont (three-step), standardized, for Apple
    standardized = companies.models.get_dupont_analysis(standardize=True).loc["AAPL"]
    dupont_chart = line(standardized.columns, {
        "Net profit margin": standardized.loc["Net Profit Margin"],
        "Asset turnover": standardized.loc["Asset Turnover"],
        "Equity multiplier": standardized.loc["Equity Multiplier"],
        "Return on equity": standardized.loc["Return on Equity"],
    }, fmt="ratio", bands=[{"from": "2021", "to": "2025", "label": "All above average"}])
    dupont_chart["series"][3].update({"color": "#c084fc", "dashed": True})
    dupont_chart = reference(dupont_chart, "Average", 0)
    charts["models-dupont-standardized"] = dupont_chart

    # PVGO: the year-end share price split into current earnings and growth
    pvgo = companies.models.get_present_value_of_growth_opportunities()
    share_price = companies.models.get_enterprise_value_breakdown().xs("Share Price", level=1)
    year = pvgo.index[-1]
    growth_part = pvgo.loc[year].reindex(TICKERS)
    price_end = share_price[year].reindex(TICKERS)
    pvgo_recent = pvgo.iloc[-RECENT_YEARS:]
    charts["models-pvgo"] = {
        "type": "tabs",
        "tabs": [
            {"label": f"Share price, {label(year)}",
             **line([NAMES[t] for t in TICKERS], {"Value of current earnings": price_end - growth_part,
                                                   "Growth (PVGO)": growth_part}, kind="bar", fmt="price", stack=True)},
            {"label": "PVGO per share", **line(pvgo_recent.index, {NAMES[t]: pvgo_recent[t] for t in TICKERS}, fmt="price")},
        ],
    }
    print("PVGO share of price:\n", (growth_part / price_end).round(3).to_string(), "\n", price_end.to_string())

    # Beneish M-Score with the -1.78 threshold, and what pushed Tesla over it
    beneish = companies.models.get_beneish_m_score()
    # the last ten years: a single early Tesla reading near 170 would flatten the rest
    m = recent(beneish.xs("Beneish M-Score", level=1))
    m_chart = line(m.columns, per_company(m), fmt="ratio", markers=[{"x": "2023", "label": "Tesla -1.62"}])
    m_chart = reference(m_chart, "Threshold (-1.78)", -1.78)
    tesla = beneish.loc["TSLA"][[c for c in beneish.columns if label(c) == "2023"][0]]
    # each index against a neutral year (an index of 1, accruals of 0), times its weight
    contribution = {short: weight * (tesla[row] - (0 if "Accruals" in row else 1))
                    for row, (short, weight) in BENEISH_WEIGHTS.items()}
    contribution = dict(sorted(contribution.items(), key=lambda kv: -kv[1]))
    charts["models-beneish"] = {
        "type": "tabs",
        "tabs": [
            {"label": "M-Score", **m_chart},
            {"label": "Tesla 2023, what moved the score",
             **line(list(contribution), {"Points added to the M-Score": pd.Series(list(contribution.values()))},
                    kind="bar", fmt="ratio", highlight=0)},
        ],
    }
    print("Beneish TSLA 2023 contributions:", {k: round(v, 3) for k, v in contribution.items()}, sum(contribution.values()))

    # Sustainable and internal growth rates, Apple against Meta
    sgr = recent(companies.models.get_sustainable_growth_rate())
    igr = recent(companies.models.get_internal_growth_rate())
    pair = ["AAPL", "META"]
    charts["models-growth-rates"] = {
        "type": "compare",
        "x": [label(c) for c in sgr.columns],
        "format": "percent",
        "names": {t: NAMES[t] for t in pair},
        "metrics": [
            {"name": "Sustainable growth rate", "series": [{"name": t, "data": values(sgr.loc[t])} for t in pair]},
            {"name": "Internal growth rate", "series": [{"name": t, "data": values(igr.loc[t])} for t in pair]},
        ],
    }

    # Graham Number (latest year) against the latest share price
    graham_number = companies.models.get_graham_number().iloc[:, -1]
    current_price = companies.get_historical_data()["Adj Close"].iloc[-1].drop("Benchmark")
    multiple = (current_price / graham_number).reindex(TICKERS).sort_values(ascending=False)
    charts["models-graham"] = {
        "type": "bar",
        "x": [NAMES[t] for t in multiple.index],
        "series": [{"name": "Price / Graham Number", "data": values(multiple)}],
        "format": "multiple",
    }

    # numbers for the tables and text on the page
    print("WACC growth AAPL:\n", companies.models.get_weighted_average_cost_of_capital(growth=True, lag=[1, 2, 3])
          .loc[("AAPL", "Weighted Average Cost of Capital")].iloc[:, -4:].round(2).to_string())
    print("Piotroski AAPL:\n", piotroski.loc["AAPL"].iloc[:, -5:].to_string())
    print("Piotroski groups", latest, groups)
    print("EV breakdown AAPL:\n", (companies.models.get_enterprise_value_breakdown().loc["AAPL"].iloc[:, -3:]).to_string())
    print("Intrinsic:\n", companies.models.get_intrinsic_valuation(0.05, 0.025, 0.094).to_string())
    print("Price:\n", current_price.to_string())
    print("Graham:\n", graham_number.to_string(), "\n", multiple.round(2).to_string())
    print("WACC level:\n", wacc_level.round(3).to_string())
    print("Altman z:\n", z.round(2).to_string())
    print("Amazon Altman parts:\n", pd.DataFrame({s: amazon_altman.loc[r] * w for r, (s, w) in ALTMAN_WEIGHTS.items()}).round(2).to_string())
    print("Beneish:\n", m.round(2).to_string())
    print("SGR/IGR:\n", sgr.round(3).to_string(), "\n", igr.round(3).to_string())
    print("Standardized DuPont AAPL:\n", standardized.iloc[:, -6:].round(2).to_string())
    print("Amazon standardized:\n", amazon.round(2).to_string())
    print("PVGO:\n", pvgo_recent.round(1).to_string())
    print("Piotroski:\n", score.to_string())
    return charts
