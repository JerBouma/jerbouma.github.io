"""Charts for the Models guide: the same calls as the code on that page."""

import pandas as pd
from financetoolkit import Toolkit

from .common import API_KEY, frame_chart, label, line, values

TICKERS = ["AAPL", "TSLA", "META", "AMZN"]
NAMES = {"AAPL": "Apple", "TSLA": "Tesla", "META": "Meta", "AMZN": "Amazon"}
# the early years of Amazon (equity close to zero) and Tesla (losses) produce
# ratios in the hundreds that flatten every other bar; the charts that show
# ratios therefore start ten years before the latest year
RECENT_YEARS = 10


def per_company(frame: pd.DataFrame, row: str | None = None) -> dict:
    """One series per company, from a frame indexed by ticker (and row)."""
    return {NAMES[t]: (frame.loc[t] if row is None else frame.loc[t].loc[row]) for t in TICKERS}


def recent(frame: pd.DataFrame) -> pd.DataFrame:
    return frame.iloc[:, -RECENT_YEARS:]


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
    for ticker in TICKERS:
        frame = recent(dupont.loc[ticker]).dropna(axis=1, how="any")
        tabs.append({
            "label": NAMES[ticker],
            "years": [label(c) for c in frame.columns],
            "components": [{"name": short, "format": fmt, "data": values(frame.loc[row])} for row, short, fmt in parts],
            "result": {"name": "Return on equity", "format": "percent", "data": values(frame.loc["Return on Equity"])},
        })
    charts["models-dupont-extended"] = {"type": "dupont", "title": "Extended DuPont analysis", "tabs": tabs}

    # WACC: the level for every company, and Amazon's components standardized
    wacc = companies.models.get_weighted_average_cost_of_capital()
    wacc_level = recent(wacc.xs("Weighted Average Cost of Capital", level=1))
    amazon = companies.models.get_weighted_average_cost_of_capital(standardize=True, show_full_results=True).loc["AMZN"]
    charts["models-wacc"] = {
        "type": "tabs",
        "title": "Weighted Average Cost of Capital",
        "tabs": [
            {"label": "WACC", **line(wacc_level.columns, per_company(wacc_level), fmt="percent")},
            {"label": "Amazon, standardized", **frame_chart(amazon.T, fmt="ratio")},
        ],
    }

    # Altman Z-Score with the classic zones (distress below 1.81, safe above 2.99)
    altman = companies.models.get_altman_z_score()
    z = altman.xs("Altman Z-Score", level=1)
    zones = {"Safe zone (2.99)": pd.Series(2.99, index=z.columns), "Distress zone (1.81)": pd.Series(1.81, index=z.columns)}
    z_chart = line(z.columns, {**per_company(z), **zones}, fmt="ratio")
    for s in z_chart["series"]:
        if "zone" in s["name"]:
            s["reference"] = True
    amazon_altman = altman.loc["AMZN"].drop("Altman Z-Score")
    charts["models-altman"] = {
        "type": "tabs",
        "title": "Altman Z-Score",
        "tabs": [
            {"label": "Z-Score", **z_chart},
            {"label": "Amazon's components", **frame_chart(amazon_altman.T, fmt="ratio")},
        ],
    }

    # Piotroski F-Score: 0 to 9 per year and company
    piotroski = companies.models.get_piotroski_score()
    score = piotroski.xs("Piotroski Score", level=1)
    charts["models-piotroski"] = line(score.columns, per_company(score), kind="bar", fmt="number",
                                      title="Piotroski F-Score (0 to 9)")

    # DuPont (three-step), standardized, for Apple
    standardized = companies.models.get_dupont_analysis(standardize=True).loc["AAPL"]
    charts["models-dupont-standardized"] = frame_chart(
        standardized.T, fmt="ratio", title="DuPont analysis for Apple, standardized (standard deviations from its mean)")

    # PVGO per share
    pvgo = companies.models.get_present_value_of_growth_opportunities()
    charts["models-pvgo"] = line(pvgo.index, {NAMES[t]: pvgo[t] for t in TICKERS}, fmt="price",
                                 title="Present Value of Growth Opportunities per share")

    # Beneish M-Score with the -1.78 threshold
    beneish = companies.models.get_beneish_m_score()
    # the last ten years: a single early Tesla reading near 170 would flatten the rest
    m = recent(beneish.xs("Beneish M-Score", level=1))
    m_chart = line(m.columns, {**per_company(m), "Threshold (-1.78)": pd.Series(-1.78, index=m.columns)}, fmt="ratio")
    m_chart["series"][-1]["reference"] = True
    meta = beneish.loc["META"].drop("Beneish M-Score")
    charts["models-beneish"] = {
        "type": "tabs",
        "title": "Beneish M-Score",
        "tabs": [
            {"label": "M-Score", **m_chart},
            {"label": "Meta's components", **frame_chart(meta.T, fmt="ratio")},
        ],
    }

    # Sustainable and internal growth rates, last ten years
    sgr = recent(companies.models.get_sustainable_growth_rate())
    igr = recent(companies.models.get_internal_growth_rate())
    charts["models-growth-rates"] = {
        "type": "tabs",
        "title": "Sustainable and internal growth rate",
        "tabs": [
            {"label": "Sustainable growth rate", **line(sgr.columns, per_company(sgr), fmt="percent")},
            {"label": "Internal growth rate", **line(igr.columns, per_company(igr), fmt="percent")},
        ],
    }

    # Graham Number (latest year) against the latest share price
    graham_number = companies.models.get_graham_number().iloc[:, -1]
    current_price = companies.get_historical_data()["Adj Close"].iloc[-1].drop("Benchmark")
    charts["models-graham"] = {
        "type": "bar",
        "title": "Graham Number against the current share price",
        "x": [NAMES[t] for t in TICKERS],
        "series": [
            {"name": "Graham Number", "data": values(graham_number.reindex(TICKERS))},
            {"name": "Current price", "data": values(current_price.reindex(TICKERS))},
        ],
        "format": "price",
    }

    # numbers for the tables on the page
    print("WACC growth AAPL:\n", companies.models.get_weighted_average_cost_of_capital(growth=True, lag=[1, 2, 3])
          .loc[("AAPL", "Weighted Average Cost of Capital")].iloc[:, -4:].round(2).to_string())
    print("Piotroski AAPL:\n", piotroski.loc["AAPL"].iloc[:, -5:].to_string())
    print("EV breakdown AAPL:\n", (companies.models.get_enterprise_value_breakdown().loc["AAPL"].iloc[:, -3:]).to_string())
    print("Intrinsic:\n", companies.models.get_intrinsic_valuation(0.05, 0.025, 0.094).to_string())
    print("Price:\n", current_price.to_string())
    print("Graham:\n", graham_number.to_string())
    print("WACC level:\n", wacc_level.iloc[:, -4:].to_string())
    print("Altman z:\n", z.iloc[:, -4:].to_string())
    print("Beneish:\n", m.iloc[:, -4:].to_string())
    print("SGR/IGR:\n", sgr.iloc[:, -3:].to_string(), "\n", igr.iloc[:, -3:].to_string())
    print("PVGO:\n", pvgo.tail(3).to_string())
    print("Piotroski:\n", score.iloc[:, -4:].to_string())
    return charts
