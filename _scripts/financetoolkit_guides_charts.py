"""Builds the data behind the interactive charts in the Finance Toolkit Getting Started guides.

Each guide page under /projects/financetoolkit/docs#getting-started has a builder module in
_scripts/financetoolkit_guides/ that runs the same Finance Toolkit calls as the code on that
page and returns its charts. This script runs one, several or all of them and writes each to
assets/data/financetoolkit-guides/<guide>.json, which the page draws with ECharts:

    FINANCIAL_MODELING_PREP_KEY=... python _scripts/financetoolkit_guides_charts.py [guide ...]

Without arguments every guide is rebuilt.
"""

import importlib
import json
import logging
import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")
logging.disable(logging.CRITICAL)

HERE = Path(__file__).resolve().parent
OUTPUT = HERE.parent / "assets" / "data" / "financetoolkit-guides"
sys.path.insert(0, str(HERE))

from financetoolkit_guides.titles import TITLES  # noqa: E402

GUIDES = [
    "getting-started", "discovery", "ratios", "models", "options", "technicals", "risk",
    "performance", "econometrics", "fixed-income", "economics", "portfolio", "external-datasets",
]


def main(names):
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for name in names or GUIDES:
        module = importlib.import_module("financetoolkit_guides." + name.replace("-", "_"))
        charts = module.build()
        # every chart takes its title from titles.py: what is plotted
        for chart_id, chart in charts.items():
            chart["title"] = TITLES[chart_id]
            chart["period"] = False  # card charts would add their years to the title otherwise
            for tab in chart.get("tabs", []):
                tab.pop("title", None)
        (OUTPUT / f"{name}.json").write_text(json.dumps({"charts": charts}, separators=(",", ":")))
        print(name, len(charts), "charts")


if __name__ == "__main__":
    main(sys.argv[1:])
