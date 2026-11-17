"""Fill in the output of every variant page in _data/docs_variants.yml.

A variant page (the Adjusted Sharpe Ratio is get_sharpe_ratio with
method="adjusted") shows the function's example with the argument added, so
the function's own output doesn't apply. This runs each variant's example as it
appears on the built page and stores what it returns, the same way the
docstrings show it: rounded to 4 decimals, the last 10 rows of a long table.

    set -a; . /etc/personal-brand/finance-toolkit.env; set +a
    python _scripts/docs_variant_outputs.py _site
"""

import ast
import os
import re
import sys
from pathlib import Path

import yaml
from bs4 import BeautifulSoup

DATA = Path("_data/docs_variants.yml")
NAV = Path("_data/navigation.yml")


def page_for(site: Path, module: str, anchor: str) -> Path:
    """The built page of a sidebar anchor, found through its sidebar title."""
    nav = NAV.read_text()
    title = re.search(r'- title: "?([^"\n]+)"?\n\s+url:\s+/projects/financetoolkit/docs/' + module + "#" + re.escape(anchor) + r"\n", nav).group(1)
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return site / "projects/financetoolkit/docs" / module / f"{slug}.html"


def run(code: str):
    code = code.replace('"FINANCIAL_MODELING_PREP_KEY"', repr(os.environ["FINANCIAL_MODELING_PREP_API_KEY"]))
    tree = ast.parse(code)
    last = tree.body.pop()
    scope: dict = {}
    exec(compile(tree, "<example>", "exec"), scope)
    return eval(compile(ast.Expression(last.value), "<example>", "eval"), scope)


def main(site: Path) -> None:
    text = DATA.read_text()
    variants = yaml.safe_load(text)
    for module, entries in variants.items():
        for anchor, variant in entries.items():
            if "argument" not in variant:
                continue
            html = BeautifulSoup(page_for(site, module, anchor).read_text(), "html.parser")
            code = [c.get_text() for c in html.select(".page__content pre code") if "import" in c.get_text()][0]
            result = run(code).round(4)
            if len(result) > 10:
                result = result.tail(10)
            table = result.to_markdown()
            print(f"{module} {anchor}: {result.shape}")
            block = "    output: |\n" + "".join("      " + line + "\n" for line in table.splitlines())
            # replace an earlier output, else add one under the anchor's argument line
            pattern = re.compile(r"(\n  " + re.escape(anchor) + r":\n(?:    .*\n|      .*\n)*?)    output: \|\n(?:      .*\n)+")
            if pattern.search(text):
                text = pattern.sub(lambda m: m.group(1) + block, text, count=1)
            else:
                text = re.sub(r"(\n  " + re.escape(anchor) + r":\n    argument: .*\n)", lambda m: m.group(1) + block, text, count=1)
    DATA.write_text(text)


if __name__ == "__main__":
    main(Path(sys.argv[1] if len(sys.argv) > 1 else "_site"))
