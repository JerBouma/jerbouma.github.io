"""Builds the data behind the interactive charts on /projects/financedatabase.

Runs the same Finance Database calls as the examples on that page, then loads
the three large Dutch insurers from those examples into the Finance Toolkit,
and writes the results to assets/data/financedatabase-charts.json, which the
page draws with ECharts. Rerun it to refresh the charts:

    pip install financedatabase financetoolkit
    FINANCIAL_MODELING_PREP_KEY=... python _scripts/financedatabase_charts.py

The Finance Database needs no key. The Finance Toolkit charts (cumulative
returns and profitability ratios) read the Financial Modeling Prep key from
the environment (FINANCIAL_MODELING_PREP_KEY, or FINANCIAL_MODELING_PREP_API_KEY);
without one the Toolkit falls back to Yahoo Finance, which covers the last
five years of financial statements. Set FINANCEDATABASE_CACHE_DIR to choose
where the database files are cached. The asset classes are loaded one at a
time to keep memory use low.
"""

import gc
import json
import logging
import os
import re
import warnings
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

import financedatabase as fd

warnings.filterwarnings("ignore")
logging.disable(logging.CRITICAL)

START = "2017-12-31"
OUTPUT = Path(__file__).resolve().parent.parent / "assets" / "data" / "financedatabase-charts.json"
API_KEY = os.environ.get("FINANCIAL_MODELING_PREP_KEY") or os.environ.get("FINANCIAL_MODELING_PREP_API_KEY", "")
TICKERS = {"AGN.AS": "Aegon", "ASRNL.AS": "ASR Nederland", "NN.AS": "NN Group"}
RATIOS = [
    "Net Profit Margin",
    "Income Before Tax Profit Margin",
    "Effective Tax Rate",
    "Return on Assets",
    "Return on Equity",
    "Return on Invested Capital",
]


def values(series: pd.Series, digits: int = 4) -> list:
    """A series as a JSON list, with gaps as null."""
    return [None if pd.isna(v) or np.isinf(v) else round(float(v), digits) for v in series]


def day(value) -> pd.Timestamp:
    """A daily index value (a Period or a date) as a timestamp."""
    return pd.Timestamp(value.start_time if isinstance(value, pd.Period) else value)


def counts(series: pd.Series, title: str, name: str) -> dict:
    """A ranking of category counts as a horizontal bar chart, largest on top."""
    ranked = series.dropna().value_counts()
    return {
        "type": "hbar",
        "title": title,
        "x": [str(v) for v in ranked.index],
        "series": [{"name": name, "data": [int(v) for v in ranked]}],
        "format": "amount",
    }


def website(url) -> str | None:
    """A website without scheme, www. or trailing slash, so variants match."""
    if not isinstance(url, str):
        return None
    url = re.sub(r"^https?://", "", url.strip().lower())
    return re.sub(r"^www\.", "", url).strip("/") or None


def companies(frame: pd.DataFrame) -> pd.DataFrame:
    """One row per company: listings that share an ISIN, share class FIGI,
    website or the first word of their name are combined."""
    parent = list(range(len(frame)))

    def find(i: int) -> int:
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    seen = {}
    for i, row in enumerate(frame.itertuples(index=False)):
        first_word = row.name.split()[0].lower().strip(",.") if isinstance(row.name, str) and row.name else None
        for key in [("isin", row.isin), ("figi", row.shareclass_figi), ("web", website(row.website)), ("name", first_word)]:
            if not isinstance(key[1], str) or not key[1]:
                continue
            if key in seen:
                parent[find(i)] = find(seen[key])
            else:
                seen[key] = i
    grouped = frame.assign(company=[find(i) for i in range(len(frame))]).groupby("company")
    return grouped.agg(name=("name", "first"), industry=("industry", lambda s: s.mode().iloc[0]))


def database_charts() -> dict:
    charts = {}

    equities = fd.Equities()
    charts["sectors"] = counts(equities.select()["sector"], "Actively listed equities per sector", "Equities")

    dutch = equities.select(sector="Financials", country="Netherlands")
    dutch = dutch[dutch["industry"].notna()]
    charts["options"] = counts(
        companies(dutch)["industry"], "Financial companies in the Netherlands per industry", "Companies"
    )

    found = equities.search(summary=["Robotics", "Education"], industry="Equipment", market="Frankfurt", index=".F")
    charts["search"] = counts(
        found["industry"], "Frankfurt listings with robotics or education in their summary, per industry", "Listings"
    )
    del equities, dutch, found
    gc.collect()

    etfs = fd.ETFs()
    charts["etfs"] = counts(etfs.select()["category_group"], "Actively listed ETFs per category group", "ETFs")
    del etfs
    gc.collect()
    return charts


def toolkit_charts() -> tuple[dict, str]:
    """The Dutch insurers from the page's example, loaded into the Finance Toolkit."""
    equities = fd.Equities()
    insurers = equities.select(
        country="Netherlands", industry="Insurance", market="Euronext Amsterdam", market_cap="Large Cap"
    )
    del equities
    gc.collect()
    toolkit = insurers.to_toolkit(api_key=API_KEY, start_date=START, progress_bar=False)

    # daily cumulative returns, as in the page's table, up to the last full
    # trading day (today's session may still be running) with a benchmark close
    daily = toolkit.get_historical_data()["Cumulative Return"].dropna(subset=["Benchmark"])
    daily = daily[[day(d).date() < date.today() for d in daily.index]]
    names = {**TICKERS, "Benchmark": "S&P 500"}
    charts = {
        "toolkit": {
            "type": "line",
            "title": "Cumulative return (1 = start)",
            "x": [day(d).strftime("%Y-%m-%d") for d in daily.index],
            "series": [{"name": names[column], "data": values(daily[column])} for column in names if column in daily],
            "format": "multiple",
        }
    }

    ratios = toolkit.ratios.collect_profitability_ratios().loc["ASRNL.AS"]
    ratios = ratios.loc[RATIOS, [c for c in ratios.columns if int(str(c)) >= 2018]]
    charts["ratios"] = {
        "type": "kpis",
        "title": "Profitability ratios for ASR Nederland, fiscal years",
        "x": RATIOS,
        "series": [{"name": str(year), "data": values(ratios[year])} for year in ratios.columns],
        "format": "percent",
    }
    return charts, charts["toolkit"]["x"][-1]


def main() -> None:
    charts = database_charts()
    toolkit, last_day = toolkit_charts()
    charts.update(toolkit)

    payload = {"generated": date.today().isoformat(), "market_data_until": last_day, "charts": charts}
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, separators=(",", ":")))
    print(f"Wrote {len(charts)} charts to {OUTPUT} ({OUTPUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
