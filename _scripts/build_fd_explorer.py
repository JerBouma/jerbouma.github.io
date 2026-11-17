"""Write the data of the Finance Database explorer (/projects/financedatabase/explorer).

One JSON file per asset class with the columns the explorer filters and shows.
Columns with few distinct values (sector, country, exchange, ...) are stored as
an index into a sorted list of values, which keeps the equities file under 2 MB
gzipped. The rows come from the financedatabase package itself, so delisted
entries and primary listings are exactly what select() and
only_primary_listing=True give in Python.

Runs in the deploy (.github/workflows/build-github-pages.yml) after the Jekyll
build, so the explorer is as current as the database on every daily rebuild:

    python _scripts/build_fd_explorer.py _site/assets/data/financedatabase
"""

import json
import sys
from datetime import date
from pathlib import Path

import financedatabase as fd

# asset class -> (class, columns); the first two are always symbol and name
CLASSES = {
    "equities": (fd.Equities, ["symbol", "name", "isin", "country", "sector", "industry_group",
                               "industry", "market_cap", "market", "exchange", "currency"]),
    "etfs": (fd.ETFs, ["symbol", "name", "isin", "category_group", "category", "family",
                       "exchange", "currency"]),
    "indices": (fd.Indices, ["symbol", "name", "category_group", "category", "exchange", "currency"]),
    "currencies": (fd.Currencies, ["symbol", "name", "base_currency", "quote_currency", "exchange"]),
    "cryptos": (fd.Cryptos, ["symbol", "name", "cryptocurrency", "currency", "exchange"]),
}
FREE_TEXT = {"symbol", "name", "isin"}
CAP_ORDER = ["Mega Cap", "Large Cap", "Mid Cap", "Small Cap", "Micro Cap", "Nano Cap"]


def build(name: str, cls, columns: list[str]) -> dict:
    database = cls()
    frame = database.select(as_pandas=False).select(columns)
    primary = database.get_primary_symbols()
    primary = set(primary.to_list()) if primary is not None else None

    rows = frame.to_dicts()
    if name == "equities":  # the order of the MCP server: primary listings, then by size
        rank = {cap: i for i, cap in enumerate(CAP_ORDER)}
        rows.sort(key=lambda r: (r["symbol"] not in primary, rank.get(r["market_cap"], 9), r["symbol"]))
    elif primary is not None:
        rows.sort(key=lambda r: (r["symbol"] not in primary, r["symbol"]))
    else:
        rows.sort(key=lambda r: r["symbol"])

    values = {c: sorted({r[c] for r in rows if r[c] is not None}) for c in columns if c not in FREE_TEXT}
    if "market_cap" in values:
        values["market_cap"] = [c for c in CAP_ORDER if c in values["market_cap"]]
    index = {c: {v: i for i, v in enumerate(vals)} for c, vals in values.items()}

    data = []
    for r in rows:
        row = [(index[c][r[c]] if r[c] is not None else -1) if c in index else (r[c] or "") for c in columns]
        if primary is not None:
            row.append(1 if r["symbol"] in primary else 0)
        data.append(row)
    return {"columns": columns, "values": values, "primary": primary is not None, "rows": data}


def main(out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    counts, values = {}, {}
    for name, (cls, columns) in CLASSES.items():
        payload = build(name, cls, columns)
        (out / f"{name}.json").write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
        counts[name] = len(payload["rows"])
        values[name] = payload["values"]
        print(f"{name}: {counts[name]:,} rows")
    # the headline numbers above the explorer
    exchanges = {e for v in values.values() for e in v.get("exchange", [])}
    stats = {
        "countries": len(values["equities"]["country"]),
        "exchanges": len(exchanges),
        "industries": len(values["equities"]["industry"]),
        "etf_families": len(values["etfs"]["family"]),
        "index_categories": len(values["indices"]["category"]),
    }
    (out / "index.json").write_text(json.dumps({"updated": date.today().isoformat(), "counts": counts, "stats": stats}))


if __name__ == "__main__":
    main(Path(sys.argv[1] if len(sys.argv) > 1 else "_site/assets/data/financedatabase"))
