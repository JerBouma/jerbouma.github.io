"""Chart data of "How the Published Models Held Up" (validation-how-it-works.md): each reference factor set's fan
from its paper's start against what happened since, on keyless OECD data."""

import json

import polars as pl

from common import OUTPUT, bar, tabs
from financescenarios.validation.published_frameworks.published_frameworks_controller import held_up

pl.Config.set_tbl_rows(40)
pl.Config.set_tbl_cols(20)
TITLES = {
    "validation-held-up-ahlgrim": "Ahlgrim, D'Arcy and Gorvett (2005) from June 2004 against What Happened in the US",
    "validation-held-up-hibbert": "Hibbert, Mowbray and Turnbull (2001) from March 2001 against What Happened in the UK",
    "validation-held-up-wilkie": "Wilkie (1986) from His Neutral Start against What Happened in the UK",
}
NAMES = {"nominal_short_rate": "Short rate", "inflation": "Inflation", "unemployment": "Unemployment",
         "stock_prices": "Share prices", "real_estate": "Real estate", "consols_rate": "Long yield"}
charts = {}
for framework in ("ahlgrim", "hibbert", "wilkie"):
    rows, scores = held_up(framework)
    print(framework)
    print(scores)
    out = {}
    for factor in rows["factor"].unique(maintain_order=True):
        part = rows.filter(pl.col("factor") == factor).sort("year")
        spec = bar([str(y) for y in part["year"]], {"5th percentile": part["p5"], "Median": part["p50"],
                                                     "95th percentile": part["p95"], "What happened": part["realized"]},
                   kind="line", fmt="percent")
        spec["series"][0]["dashed"] = spec["series"][2]["dashed"] = True
        out[NAMES.get(factor, factor)] = spec
    chart = tabs(out)
    chart["title"], chart["period"] = TITLES[f"validation-held-up-{framework}"], False
    charts[f"validation-held-up-{framework}"] = chart
(OUTPUT / "validation-held-up.json").write_text(json.dumps({"charts": charts}, separators=(",", ":")))
print("validation-held-up", len(charts), "charts")
