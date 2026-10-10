"""
Generates the Finance Scenarios API reference pages from the package's own docstrings.

It imports `financescenarios`, walks the public API (the classes and functions in its
`__all__`, plus every factor and model class), and writes one Markdown page per class or
area to `_pages/financescenarios/documentation/reference/`, together with an index page.

Run it with a Python environment that has `financescenarios` installed, from anywhere:

    python assets/python/financescenarios_docs.py

The pages are plain Jekyll Markdown. They are hidden like the rest of the Finance Scenarios
documentation (`sitemap: false`, `noindex: true`, `search: false`).
"""

import ast
import inspect
import re
import sys
import textwrap
from pathlib import Path

import financescenarios as fs
from financescenarios.dependence.dependence_controller import Dependence
from financescenarios.factors.commodities.commodities_controller import Commodities
from financescenarios.factors.credit.credit_controller import Credit
from financescenarios.factors.credit_migration.credit_migration_controller import CreditMigration
from financescenarios.factors.credit_term_structure.credit_term_structure_controller import CreditTermStructure
from financescenarios.factors.dividend_growth.dividend_growth_controller import DividendGrowth
from financescenarios.factors.dividend_yield.dividend_yield_controller import DividendYield
from financescenarios.factors.equities.equities_controller import Equities
from financescenarios.factors.fx.fx_controller import FX
from financescenarios.factors.hjm.hjm_controller import Hjm
from financescenarios.factors.inflation.inflation_controller import Inflation
from financescenarios.factors.interest_rates.interest_rates_controller import InterestRates
from financescenarios.factors.leading_indicator.leading_indicator_controller import LeadingIndicator
from financescenarios.factors.mortality.mortality_controller import Mortality
from financescenarios.factors.real_estate.real_estate_controller import RealEstate
from financescenarios.factors.term_structure.term_structure_controller import TermStructure
from financescenarios.factors.unemployment.unemployment_controller import Unemployment
from financescenarios.models.knw.knw_controller import Knw
from financescenarios.models.knw_sv.knw_sv_controller import KnwSv
from financescenarios.models.knw_sv_q.knw_sv_q_controller import KnwSvQ
from financescenarios.reporting.reporting_controller import Reporting

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "_pages" / "financescenarios" / "documentation" / "reference"
BASE_URL = "/projects/financescenarios/docs/reference"

# ── The pages ──────────────────────────────────────────────────────────────────
# (slug, title, one-line summary, members). The first group is the core API, the
# second the factors and the third the joint models, matching the sidebar.
CORE = [
    ("scenarios", "Scenarios",
     "Calibrate every configured factor and simulate correlated scenarios; also the saved calibration and the Toolkit builder.",
     ["Scenarios", "CalibrationResult", "build_toolkit"]),
    ("scenario-set", "ScenarioSet",
     "The result of a run: describe, filter, plot, diagnose and compare simulated scenarios.",
     ["ScenarioSet", "FactorLabel", "compare_runs"]),
    ("portfolio", "Portfolio",
     "Read a finished run through an investment portfolio: allocations, cashflows, glidepaths, risk metrics and factor exposure.",
     ["Portfolio", "CashflowRule", "GlidepathCheckpoint", "PortfolioSummary", "PortfolioPreset",
      "load_portfolio_library", "load_portfolio_preset", "compute_portfolio_factor_exposure"]),
    ("solvency", "Solvency",
     "Solvency II on a real-world and a risk-neutral run: the martingale test, best estimate, SCR and EIOPA curves.",
     ["Solvency", "best_estimate", "solvency_capital_requirement", "interest_rate_scr", "equity_scr",
      "martingale_test", "market_consistency_check", "eiopa_risk_free_curve", "eiopa_symmetric_adjustment",
      "zero_coupon_curve", "curve_discount_factors", "write_scenario_files"]),
    ("configuration", "Configuration and Presets",
     "Load settings, factor sets and presets, list every named preset and scaffold a project.",
     ["ScenariosConfig", "Profile", "list_presets", "load_profiles", "load_config", "load_profile_library",
      "scaffold_project", "set_log_level"]),
    ("regimes", "Regimes and Stress Tests",
     "Named stress narratives and the official Federal Reserve and ESRB stress scenarios as regimes.",
     ["Regime", "RegimeLibrary", "load_regime", "stress_test_regime"]),
    ("runs-and-releases", "Run Files and Releases",
     "Write and read saved runs, and publish, load and simulate versioned calibration releases.",
     ["write_run", "read_run", "read_run_calibration", "publish_calibration", "load_release",
      "simulate_release"]),
    ("history-and-metrics", "History and Metrics",
     "Fetch the realized history behind a run, turn it into a backtest and compute factor and price metrics.",
     ["fetch_historical_data", "build_synthetic_scenario_set", "compute_factor_metrics",
      "compute_price_performance_metrics"]),
    ("charts", "Charts",
     "The chart functions behind every `.plot()`: fan charts, paths, terminal distributions, runs and portfolios.",
     ["plot_factors", "plot_fan_chart", "plot_paths", "plot_terminal_distribution", "plot_runs",
      "plot_correlation_matrix", "plot_sleeve_values", "plot_weight_drift"]),
    ("dependence", "Dependence",
     "The correlation matrix that links every factor: estimation, shrinkage and repair.",
     [Dependence]),
    ("reporting", "Reporting",
     "Convert simulated prices into one reporting currency after the simulation.",
     [Reporting]),
]

FACTORS = [
    ("interest-rates", "InterestRates", "Short and long interest rates, one per country or region.", [InterestRates]),
    ("inflation", "Inflation", "Consumer price inflation, one per country or region.", [Inflation]),
    ("equities", "Equities", "Equity indices, sectors, regions and styles with regime switching.", [Equities]),
    ("unemployment", "Unemployment", "Unemployment rates, each paired with an inflation entry.", [Unemployment]),
    ("term-structure", "TermStructure", "The yield curve as Nelson-Siegel level, slope and curvature.", [TermStructure]),
    ("hjm", "Hjm", "A two-factor Gaussian HJM forward curve.", [Hjm]),
    ("real-estate", "RealEstate", "House-price and commercial property growth.", [RealEstate]),
    ("credit", "Credit", "Credit spreads by maturity, rating bucket or country.", [Credit]),
    ("credit-migration", "CreditMigration", "A credit cycle driving rating migrations and defaults.",
     [CreditMigration, "rating_migration"]),
    ("credit-term-structure", "CreditTermStructure", "A Nelson-Siegel credit spread curve.", [CreditTermStructure]),
    ("leading-indicator", "LeadingIndicator", "The OECD composite leading indicator.", [LeadingIndicator]),
    ("fx", "FX", "Exchange rates, one per currency against the US dollar.", [FX]),
    ("commodities", "Commodities", "Commodity futures, one per commodity.", [Commodities]),
    ("dividend-yield", "DividendYield", "Dividend yields, one per ticker.", [DividendYield]),
    ("dividend-growth", "DividendGrowth", "Dividend growth, one per ticker.", [DividendGrowth]),
    ("mortality", "Mortality", "Mortality improvement with the Cairns-Blake-Dowd model.", [Mortality]),
]

MODELS = [
    ("knw", "Knw", "The KNW model: interest rate and inflation fitted jointly.", [Knw]),
    ("knw-sv", "KnwSv", "The KNW model with stochastic volatility.", [KnwSv]),
    ("knw-sv-q", "KnwSvQ", "The risk-neutral (Q-measure) side of the KNW models.", [KnwSvQ]),
]

GROUPS = [("Core", CORE), ("Factors", FACTORS), ("Joint models", MODELS)]

# ── Docstring parsing ──────────────────────────────────────────────────────────
SECTION_NAMES = {
    "Args": "Args", "Arguments": "Args", "Parameters": "Args",
    "Attributes": "Attributes",
    "Returns": "Returns", "Return": "Returns", "Yields": "Yields",
    "Raises": "Raises", "Warns": "Warns",
    "Notes": "Notes", "Note": "Notes",
    "References": "References",
    "As an example": "As an example", "Example": "As an example", "Examples": "As an example",
}
ENTRY_SECTIONS = {"Args", "Attributes", "Raises", "Warns"}
RE_SECTION = re.compile(r"^(" + "|".join(map(re.escape, SECTION_NAMES)) + r"):\s*$")
RE_ARG = re.compile(r"^\*{0,2}(\w+(?:,\s*\w+)*)\s*(?:\((.+?)\))?\s*:\s*(.*)$")
RE_BARE_URL = re.compile(r"(?<![(<\[\w/\"'=])(https?://[^\s)>\]]+[^\s)>\].,;:])")
RE_NAMES = re.compile(r"(?<![/\w.`])(FinanceScenarios|FinanceToolkit)(?![/\w`])")
NAME_FIX = {"FinanceScenarios": "Finance Scenarios", "FinanceToolkit": "Finance Toolkit"}

warnings: list[str] = []


def prose(text: str) -> str:
    """Use the two-word project names in prose; code spans, fences and URLs keep the package names."""
    out, in_fence = [], False
    for line in text.split("\n"):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue
        parts = re.split(r"(`[^`]*`)", line)
        out.append("".join(p if p.startswith("`") else RE_NAMES.sub(lambda m: NAME_FIX[m.group(1)], p) for p in parts))
    return "\n".join(out)


def split_sections(doc: str) -> tuple[str, list[tuple[str, str]]]:
    """Split a Google-style docstring into its description and (section, body) pairs."""
    description, sections, current, body, in_fence = [], [], None, [], False
    for line in doc.split("\n"):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        match = None if in_fence else RE_SECTION.match(line)
        if match:
            if current is not None:
                sections.append((current, "\n".join(body)))
            current, body = SECTION_NAMES[match.group(1)], []
            continue
        (description if current is None else body).append(line)
    if current is not None:
        sections.append((current, "\n".join(body)))
    return "\n".join(description).strip(), sections


def entries(body: str) -> list[str]:
    """Each top-level entry of an indented block, continuation lines joined with spaces."""
    items: list[list[str]] = []
    for line in textwrap.dedent(body).split("\n"):
        if not line.strip():
            continue
        if not line.startswith((" ", "\t")):
            items.append([line.strip()])
        elif items:
            items[-1].append(line.strip())
        else:
            items.append([line.strip()])
    return [" ".join(item) for item in items]


def html_type(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("|", "&#124;")


def render_entries(name: str, body: str, where: str) -> str:
    lines = []
    for entry in entries(body):
        entry = entry.removeprefix("- ")
        match = RE_ARG.match(entry)
        if match and name in {"Args", "Attributes"}:
            arg, typ, desc = match.groups()
            label = f"{arg} ({html_type(typ)}):" if typ else f"{arg}:"
            lines.append(f"- <u>{label}</u> {desc}".rstrip())
        elif name in {"Raises", "Warns"} and ":" in entry:
            exc, desc = entry.split(":", 1)
            lines.append(f"- <u>{html_type(exc.strip())}:</u> {desc.strip()}")
        else:
            warnings.append(f"{where}: unparsed {name} entry: {entry[:80]}")
            lines.append(f"- {entry}")
    return "\n".join(lines)


def render_returns(body: str, where: str) -> str:
    items = entries(body)
    if len(items) == 1:
        text = items[0]
        match = re.match(r"^([\w.\[\], |()'\"]+?):\s+(.*)$", text)
        if match and not match.group(1).strip().startswith(("A ", "a ", "The ", "the ")):
            return f"<u>{html_type(match.group(1).strip())}:</u> {match.group(2)}"
        return text
    warnings.append(f"{where}: Returns has {len(items)} entries")
    return "\n".join(f"- {item}" for item in items)


def render_references(body: str) -> str:
    out = []
    for entry in entries(body):
        entry = RE_BARE_URL.sub(r"<\1>", entry.removeprefix("- "))
        out.append(f"- {entry}")
    return "\n".join(out)


def render_free(body: str) -> str:
    """Notes, examples and other free text: dedent and keep it as Markdown."""
    return textwrap.dedent(body).strip()


def fence_indented(text: str) -> str:
    """Indented blocks after a blank line (equations, mostly) become ```text fences, outside lists and fences."""
    lines, out, i, in_fence, prev_list = text.split("\n"), [], 0, False, False
    while i < len(lines):
        line = lines[i]
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        prev_blank = not out or not out[-1].strip()
        if not in_fence and line.startswith("    ") and line.strip() and prev_blank and not prev_list:
            block = []
            while i < len(lines) and (lines[i].startswith("    ") or not lines[i].strip()):
                block.append(lines[i])
                i += 1
            while block and not block[-1].strip():
                block.pop()
            out += ["```text", *textwrap.dedent("\n".join(block)).split("\n"), "```", ""]
            continue
        if line.strip():
            prev_list = bool(re.match(r"^\s*(- |\* |\d+\. )", line)) or (prev_list and line.startswith(" "))
        out.append(line)
        i += 1
    return "\n".join(out).strip()


def render_doc(obj, where: str) -> str:
    doc = inspect.getdoc(obj)
    if not doc:
        warnings.append(f"{where}: no docstring")
        return "*No docstring.*"
    description, sections = split_sections(doc)
    parts = [fence_indented(description)] if description else []
    for name, body in sections:
        if name in ENTRY_SECTIONS:
            rendered = render_entries(name, body, where)
        elif name in {"Returns", "Yields"}:
            rendered = render_returns(body, where)
        elif name == "References":
            rendered = render_references(body)
        else:
            rendered = fence_indented(render_free(body))
        parts.append(f"**{name}:**\n\n{rendered}")
    return prose("\n\n".join(parts))


# ── Signatures ─────────────────────────────────────────────────────────────────
def function_node(func) -> ast.FunctionDef | None:
    try:
        source = textwrap.dedent(inspect.getsource(inspect.unwrap(func)))
    except (OSError, TypeError):
        return None
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            return node
    return None


def format_signature(label: str, func, drop_first: bool) -> str:
    node = function_node(func)
    if node is None:
        warnings.append(f"{label}: signature from inspect")
        return f"{label}{inspect.signature(func)}"
    a = node.args
    params: list[str] = []

    def one(arg: ast.arg, default=None) -> str:
        text = arg.arg + (f": {ast.unparse(arg.annotation)}" if arg.annotation else "")
        if default is not None:
            text += f" = {ast.unparse(default)}" if arg.annotation else f"={ast.unparse(default)}"
        return text

    positional = a.posonlyargs + a.args
    defaults = [None] * (len(positional) - len(a.defaults)) + list(a.defaults)
    for i, (arg, default) in enumerate(zip(positional, defaults)):
        params.append(one(arg, default))
        if a.posonlyargs and i == len(a.posonlyargs) - 1:
            params.append("/")
    if a.vararg:
        params.append("*" + one(a.vararg))
    elif a.kwonlyargs:
        params.append("*")
    for arg, default in zip(a.kwonlyargs, a.kw_defaults):
        params.append(one(arg, default))
    if a.kwarg:
        params.append("**" + one(a.kwarg))
    if drop_first and params and params[0].split(":")[0] in {"self", "cls"}:
        params = params[1:]
    returns = f" -> {ast.unparse(node.returns)}" if node.returns else ""
    flat = f"{label}({', '.join(params)}){returns}"
    if len(flat) <= 100 or not params:
        return flat
    inner = "".join(f"    {p},\n" for p in params)
    return f"{label}(\n{inner}){returns}"


def class_fields(cls) -> str | None:
    """The annotated fields of a pydantic model or dataclass, as written in the source."""
    try:
        source = textwrap.dedent(inspect.getsource(cls))
    except (OSError, TypeError):
        return None
    node = next(n for n in ast.walk(ast.parse(source)) if isinstance(n, ast.ClassDef))
    bases = ", ".join(ast.unparse(b) for b in node.bases)
    fields = [
        f"    {ast.unparse(stmt)}"
        for stmt in node.body
        if isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name)
        and not stmt.target.id.startswith("_") and stmt.target.id != "model_config"
    ]
    if not fields:
        return None
    return f"class {cls.__name__}({bases}):\n" + "\n".join(fields)


def is_model(cls) -> bool:
    return hasattr(cls, "model_fields") or hasattr(cls, "__dataclass_fields__")


def public_members(cls) -> list[tuple[str, object, str]]:
    """(name, object, kind) for every public method and property defined on the class itself."""
    members = []
    for name, value in vars(cls).items():
        if name.startswith("_") or name == "model_config":
            continue
        if isinstance(value, property):
            members.append((name, value.fget, "property"))
        elif isinstance(value, classmethod):
            members.append((name, value.__func__, "classmethod"))
        elif isinstance(value, staticmethod):
            members.append((name, value.__func__, "staticmethod"))
        elif inspect.isfunction(value):
            members.append((name, value, "method"))
        elif type(value).__name__ == "cached_property":
            members.append((name, value.func, "property"))
    return members


# ── Pages ──────────────────────────────────────────────────────────────────────
def code_block(text: str) -> str:
    return f"```python\n{text}\n```"


def raw(text: str) -> str:
    """Keep Liquid away from docstrings that contain its delimiters."""
    if re.search(r"\{\{|\}\}|\{%|%\}", text):
        if "endraw" in text:
            raise ValueError("a docstring contains {% endraw %}")
        return "{% raw %}\n" + text + "\n{% endraw %}"
    return text


def render_class(cls, own_page: bool, qualify: bool) -> tuple[list[str], int]:
    """The class's own section (unless it is the page's subject) and one h2 per public member."""
    blocks, count = [], 0
    where = cls.__name__
    if is_model(cls):
        intro = class_fields(cls)
    elif "__init__" in vars(cls):
        intro = format_signature(cls.__name__, cls.__init__, drop_first=True).removesuffix(" -> None")
    else:
        intro = f"{cls.__name__}()"
    head = (code_block(intro) + "\n\n" if intro else "") + render_doc(cls, where)
    blocks.append(raw(head if own_page else f"## {cls.__name__}\n\n{head}"))
    for name, func, kind in public_members(cls):
        title = f"{cls.__name__}.{name}" if qualify else name
        if kind == "property":
            sig = f"{cls.__name__.lower()}.{name}"
            node = function_node(func)
            if node is not None and node.returns is not None:
                sig += f"  # property -> {ast.unparse(node.returns)}"
            else:
                sig += "  # property"
        elif kind in {"classmethod", "staticmethod"}:
            sig = format_signature(f"{cls.__name__}.{name}", func, drop_first=kind == "classmethod")
        else:
            sig = format_signature(name, func, drop_first=True)
        blocks.append(raw(f"## {title}\n\n{code_block(sig)}\n\n{render_doc(func, f'{where}.{name}')}"))
        count += 1
    return blocks, count


def render_function(func, name: str) -> str:
    sig = format_signature(name, func, drop_first=False)
    return raw(f"## {name}\n\n{code_block(sig)}\n\n{render_doc(func, name)}")


def yaml_quote(text: str) -> str:
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


def front_matter(title: str, permalink: str, excerpt: str, seo_title: str) -> str:
    return f"""---
title: {yaml_quote(title)}
seo_title: {yaml_quote(seo_title)}
excerpt: {yaml_quote(excerpt)}
description: {yaml_quote(excerpt)}
author_profile: false
permalink: {permalink}
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---
"""


def resolve(member) -> tuple[str, object]:
    """A page member is a name exported by `financescenarios` or a class imported above."""
    if isinstance(member, str):
        return member, getattr(fs, member)
    return member.__name__, member


def build_page(slug: str, title: str, summary: str, members: list) -> tuple[str, int]:
    resolved = [resolve(m) for m in members]
    with_methods = [obj for _, obj in resolved if inspect.isclass(obj) and public_members(obj)]
    own_page = len(resolved) == 1 and inspect.isclass(resolved[0][1])
    qualify = len(with_methods) > 1
    blocks, count = [], 0
    top = [name for name, _ in resolved if name in fs.__all__]
    imports = []
    if top:
        imports.append(f"from financescenarios import {', '.join(top)}")
    for name, obj in resolved:
        if name not in fs.__all__:
            imports.append(f"from {obj.__module__} import {name}")
    intro = (
        f"{summary.rstrip('.')}. Generated from the docstrings of Finance Scenarios "
        f"{fs.__version__}; `help(...)` in Python shows the same text.\n\n"
        f"```python\n{chr(10).join(imports)}\n```"
    )
    blocks.append(intro)
    for name, member in resolved:
        if inspect.isclass(member):
            more, n = render_class(member, own_page, qualify)
            blocks.extend(more)
            count += n
        else:
            blocks.append(render_function(member, name))
            count += 1
    seo = f"{title} Reference – Finance Scenarios"
    page = front_matter(title, f"{BASE_URL}/{slug}", summary.replace("`", ""), seo) + "\n" + "\n\n".join(blocks) + "\n"
    return page, count


def build_index(counts: dict[str, int]) -> str:
    lines = [
        "The reference pages are generated from the docstrings in the Finance Scenarios package, so they say exactly "
        "what `help(...)` says in Python. Each page covers one class or area: its constructor, then every public "
        "method and property with its signature, arguments, return value, errors and, where the docstring has one, "
        "a worked example with real output.",
        "",
        "How a run is put together, the configuration keys and the units every result is reported in are on the "
        "[documentation](/projects/financescenarios/docs) pages.",
    ]
    for group, pages in GROUPS:
        lines += ["", f"## {group}", "", "| Page | What it covers |", "|:-----|:---------------|"]
        for slug, title, summary, _ in pages:
            lines.append(f"| [{title}]({BASE_URL}/{slug}) | {summary} |")
    excerpt = "Reference for the Finance Scenarios Python package, generated from its docstrings: every public class, method and function."
    return front_matter("Reference", BASE_URL, excerpt, "Reference – Finance Scenarios") + "\n" + "\n".join(lines) + "\n"


def main() -> None:
    covered = {resolve(m)[0] for _, pages in GROUPS for *_, members in pages for m in members}
    missing = sorted(set(fs.__all__) - covered - {"__version__"})
    if missing:
        sys.exit(f"public names without a reference page: {missing}")
    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob("*.md"):
        old.unlink()
    counts = {}
    for _, pages in GROUPS:
        for slug, title, summary, members in pages:
            page, counts[slug] = build_page(slug, title, summary, members)
            (OUT / f"{slug}.md").write_text(page)
    (OUT / "reference.md").write_text(build_index(counts))
    print(f"{len(counts) + 1} pages, {sum(counts.values())} methods and functions documented")
    for warning in warnings:
        print("warning:", warning)


if __name__ == "__main__":
    main()
