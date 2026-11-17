"""Generate the Finance Database documentation pages (/projects/financedatabase/docs).

One page per asset class with its select, search and show_options, and an
overview page with the functions every class shares (fd.show_options and
to_toolkit). Each function shows its docstring from the installed
financedatabase package (description, a parameters table and its example),
followed by more examples from EXAMPLES below. Every example is run and its
output written under it, so the pages show what the released package returns.

The pages' front matter and introduction are edited on the pages themselves:
everything above the first "## " heading of an existing page is kept.

    set -a; . /etc/personal-brand/finance-toolkit.env; set +a   # for to_toolkit
    python _scripts/financedatabase_docs.py

Run it with the released package (pip install -U financedatabase) and
financetoolkit installed, from the repository root.
"""

import ast
import html
import inspect
import os
import re
import sys
from pathlib import Path

import financedatabase as fd
import numpy as np
import pandas as pd
from financedatabase.frame_model import FinanceFrame

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets" / "python"))
from docs import _clean_description, _linkify  # noqa: E402  (the Finance Toolkit generator)

OUT = Path("_pages/financedatabase/docs")
KEY = os.environ.get("FINANCIAL_MODELING_PREP_API_KEY", "")
ROWS = 10
# columns left out of an output table: long text and identifiers that make it too wide to read
WIDE = ["summary", "cusip", "figi", "composite_figi", "shareclass_figi", "zipcode", "website",
        "state", "city", "isin", "mic", "delisted"]

# Examples shown after a function's own, per page and function: (lead-in, code).
EXAMPLES = {
    "equities": {
        "select": [
            ("To find the primary listings of Dutch technology companies:",
             'equities.select(country="Netherlands", sector="Information Technology", only_primary_listing=True)[\n'
             '    ["name", "currency", "industry", "market", "market_cap"]\n].head()'),
            ("Every filter also accepts a list, which matches any of its values. To find the primary "
             "listings of Dutch and German chipmakers:",
             'equities.select(\n    country=["Netherlands", "Germany"],\n    industry="Semiconductors & Chip Equipment",\n'
             '    only_primary_listing=True,\n)[["name", "country", "market", "market_cap"]]'),
        ],
        "search": [
            ("The queries are regular expressions and can be combined with any column. To find "
             "primary listings in capital goods whose summary mentions robotics:",
             'equities.search(summary="robotics", industry_group="Capital Goods", only_primary_listing=True)[\n'
             '    ["name", "country", "industry", "market"]\n].head(10)'),
        ],
        "show_options": [
            ("To see which industries exist among Dutch financial companies:",
             'equities.show_options(selection="industry", sector="Financials", country="Netherlands")'),
        ],
    },
    "etfs": {
        "select": [
            ("To find bond ETFs from Vanguard:",
             'etfs.select(category_group="Fixed Income", family="Vanguard Asset Management", only_primary_listing=True)[\n'
             '    ["name", "category", "currency", "exchange"]\n].head(10)'),
        ],
        "search": [
            ("To find ETFs whose summary mentions robotics:",
             'etfs.search(summary="robotics", only_primary_listing=True)[["name", "category", "family", "exchange"]].head(10)'),
        ],
    },
    "indices": {
        "search": [
            ("To find the Euro Stoxx 50 indices:",
             'indices.search(name="Euro Stoxx 50")[["name", "currency", "category", "exchange"]].head(10)'),
        ],
    },
    "currencies": {
        "search": [
            ("To find the currency pairs that quote the Japanese yen:",
             'currencies.search(quote_currency="JPY")[["name", "base_currency", "quote_currency"]].head(10)'),
        ],
    },
    "cryptos": {
        "search": [
            ("To find Solana in every currency it is quoted in:",
             'cryptos.search(name="Solana")[["name", "cryptocurrency", "currency", "exchange"]].head(10)'),
        ],
    },
    "docs": {
        "to_toolkit": [
            ("To calculate the return on invested capital of the chipmakers listed in Amsterdam:",
             'equities = fd.Equities()\n\nchipmakers = equities.select(\n    country="Netherlands",\n'
             '    industry="Semiconductors & Chip Equipment",\n    market="Euronext Amsterdam",\n)\n\n'
             'toolkit = chipmakers.to_toolkit(\n    api_key="FINANCIAL_MODELING_PREP_KEY",\n'
             '    start_date="2021-01-01",\n    end_date="2025-12-31",\n    progress_bar=False,\n)\n\n'
             'toolkit.ratios.get_return_on_invested_capital()'),
        ],
    },
}

REPLACE = {("equities", "select")}

# page -> (class or None for the overview, variable name, functions)
PAGES = {
    "equities": (fd.Equities, "equities", ["select", "search", "show_options"]),
    "etfs": (fd.ETFs, "etfs", ["select", "search", "show_options"]),
    "indices": (fd.Indices, "indices", ["select", "search", "show_options"]),
    "currencies": (fd.Currencies, "currencies", ["select", "search", "show_options"]),
    "cryptos": (fd.Cryptos, "cryptos", ["select", "search", "show_options"]),
    "docs": (None, None, ["show_options", "to_toolkit"]),
}

SPLIT = re.compile(r"\n\s*(Args:|Returns:|Raises:|As an example:)\s*\n")
ARG = re.compile(r"^(\*{0,2}\w+) \(([^)]*)\):\s*(.*)$")


def sections(doc: str) -> dict:
    """The parts of a Google-style docstring."""
    parts = SPLIT.split("\n" + doc)
    out = {"description": parts[0].strip()}
    for name, body in zip(parts[1::2], parts[2::2]):
        out[name.rstrip(":")] = body
    return out


def arguments(block: str) -> list:
    """(name, type, description, default) per argument."""
    rows, current = [], None
    for line in inspect.cleandoc(block).splitlines():
        m = ARG.match(line.strip()) if not line.startswith(" ") else None
        if m:
            current = [m.group(1), m.group(2).replace(", optional", ""), m.group(3)]
            rows.append(current)
        elif line.strip().startswith("**kwargs:"):
            current = ["**kwargs", "str | list", line.strip()[len("**kwargs:"):].strip()]
            rows.append(current)
        elif current:
            current[2] += " " + line.strip()
    out = []
    for name, kind, text in rows:
        default = re.search(r"Defaults to ([^.]+(?:\.\d+)?)\.?\s*$", text)
        out.append((name, kind, text, default.group(1).strip() if default else ""))
    return out


def table(rows: list) -> str:
    body = "\n".join(
        f"<tr><td><code>{html.escape(n)}</code></td><td><code>{html.escape(k)}</code></td>"
        f"<td>{html.escape(t)}</td><td>{f'<code>{html.escape(d)}</code>' if d else ''}</td></tr>"
        for n, k, t, d in rows)
    return ('<div class="docs-params"><div class="docs-params__table"><table>\n'
            "<thead><tr><th>Parameter</th><th>Type</th><th>Description</th><th>Default</th></tr></thead>\n"
            f"<tbody>\n{body}\n</tbody>\n</table></div></div>")


def run(code: str, scope: dict):
    """Run an example, returning the value of its last line."""
    code = code.replace('"FINANCIAL_MODELING_PREP_KEY"', repr(KEY))
    tree = ast.parse(code)
    last = tree.body.pop()
    exec(compile(tree, "<example>", "exec"), scope)
    if isinstance(last, ast.Expr):
        return eval(compile(ast.Expression(last.value), "<example>", "eval"), scope)
    exec(compile(ast.Module([last], []), "<example>", "exec"), scope)
    return None


def values(items) -> str:
    items = [str(v) for v in items]
    shown = ", ".join(items[:12]) + (f", … ({len(items)} in total)" if len(items) > 12 else "")
    return shown


def render(result) -> str:
    """The output of an example, as the page shows it."""
    if isinstance(result, pd.DataFrame):
        frame = result.drop(columns=[c for c in WIDE if c in result.columns])
        note = ""
        if len(frame) > ROWS:
            note = f"\n\nThe first {ROWS} of {len(frame):,} rows."
            frame = frame.head(ROWS)
        return frame.round(4).to_markdown() + note
    if isinstance(result, dict):
        return "\n".join(f"- **{k}**: {values(v)}" for k, v in result.items())
    if isinstance(result, (np.ndarray, pd.Index, pd.Series, list, pd.api.extensions.ExtensionArray)):
        return f"```\n{values(list(result))}\n```"
    return f"```\n{result}\n```"


def function(page: str, cls, variable: str, name: str) -> str:
    if name == "to_toolkit":
        obj, call = FinanceFrame.to_toolkit, "to_toolkit"
    elif cls is None:
        obj, call = fd.show_options, "fd.show_options"
    else:
        obj, call = getattr(cls, name), f"{variable}.{name}"
    doc = sections(inspect.getdoc(obj))
    out = [f"## {name}\n", _linkify(_clean_description(doc["description"])), ""]
    if "Args" in doc:
        out += [f"`{call}` accepts the following parameters:", "", table(arguments(doc["Args"])), ""]
    if "Returns" in doc:
        out += [f"**Returns:** {' '.join(inspect.cleandoc(doc['Returns']).split())}", ""]

    examples = []
    own = re.search(r"```python\n(.*?)```", doc.get("As an example", ""), re.S)
    # search() is shared by every class and its example uses equities, so it is
    # only shown on the equities page; the other pages have their own examples
    # REPLACE: functions whose own example the page doesn't show (the content
    # rules keep Dutch insurers out of examples, and equities.select's lists them)
    if own and not (name == "search" and page != "equities") and (page, name) not in REPLACE:
        examples.append(("As an example:", own.group(1).strip()))
    examples += EXAMPLES.get(page, {}).get(name, [])

    scope = {"fd": fd}
    if cls is not None:
        run(f"{variable} = fd.{cls.__name__}()", scope)
    for i, (lead, code) in enumerate(examples):
        # a function's first example starts from the import, later ones build on it
        shown = code
        if i == 0 and not code.startswith("import"):
            shown = "import financedatabase as fd\n\n" + (f"{variable} = fd.{cls.__name__}()\n\n" if cls else "") + code
        result = run(code, scope)
        out += [lead, "", f"```python\n{shown}\n```", "", "Which returns:", "", render(result), ""]
        print(f"  {page}.{name} example {i + 1}: {type(result).__name__}")
    return "\n".join(out) + "\n---\n"


def main() -> None:
    for page, (cls, variable, names) in PAGES.items():
        path = OUT / f"{page}.md"
        text = path.read_text() if path.exists() else f"---\ntitle: {page}\n---\n\n"
        end = text.find("\n## ")
        header = text[: end + 1] if end >= 0 else text.rstrip() + "\n\n"
        body = "\n".join(function(page, cls, variable, n) for n in names)
        path.write_text(header + body)
        print(f"✓ {path}")


if __name__ == "__main__":
    main()
