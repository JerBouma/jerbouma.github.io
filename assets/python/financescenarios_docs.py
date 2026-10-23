"""
Generates the reference at the bottom of every Finance Scenarios docs page from the package's
own docstrings, and the sidebar of those pages.

It imports `financescenarios`, walks the public API (every name in its `__all__`, plus the
factor and model classes reached through `Scenarios`) and writes one include per page to
`_includes/financescenarios-reference/<page>.md`. Each docs page in
`_pages/financescenarios/documentation/` includes its reference at the end. It then rebuilds
the `financescenarios-docs*` entries of `_data/navigation.yml` from the headings each page
ends up with: the module list, the Under the Hood list and the page's own sections.

Run it with a Python environment that has `financescenarios` installed, from anywhere:

    python assets/python/financescenarios_docs.py

It stops when a public name has no page or sits on two.
"""

import ast
import importlib
import inspect
import re
import sys
import textwrap
from collections import Counter
from pathlib import Path

# The formula → LaTeX conversion of the Finance Toolkit docs generator, next to this file.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from docs import _RE_FORMULA_INTRO, _formula_to_latex, _looks_like_formula  # noqa: E402

import financescenarios as fs
from financescenarios.config.config_model import (
    CorrelationsConfig,
    CreditMigrationConfig,
    CreditTermStructureConfig,
    FixedCorrelation,
    HjmConfig,
    LeadingIndicatorConfig,
    MortalityConfig,
)
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
from financescenarios.models.cp2022.cp2022_controller import Cp2022
from financescenarios.models.cp2022.cp2022_model import Cp2022Params, Cp2022Vintage
from financescenarios.models.knw.knw_controller import Knw
from financescenarios.models.knw_sv.knw_sv_controller import KnwSv
from financescenarios.models.knw_sv_q.knw_sv_q_controller import KnwSvQ
from financescenarios.reporting.reporting_controller import Reporting
from financescenarios.validation.dnb.dnb_controller import Dnb
from financescenarios.validation.naic_goes.naic_goes_controller import NaicGoes
from financescenarios.validation.published_frameworks.published_frameworks_controller import compare_published, held_up

ROOT = Path(__file__).resolve().parents[2]
PAGES_DIR = ROOT / "_pages" / "financescenarios" / "documentation"
INCLUDES = ROOT / "_includes"
OUT = INCLUDES / "financescenarios-reference"
NAVIGATION = ROOT / "_data" / "navigation.yml"
DOCS = "/projects/financescenarios/docs"

# ── The pages ──────────────────────────────────────────────────────────────────
# (page, sidebar title, url path, members). A member is a name or class, or a
# (heading, [members]) group that puts several under one heading. The first list
# is the sidebar's Modules, the second its Under the Hood; a page without members
# has no reference.
MODULES = [
    ("docs", "Scenarios", "", [
        "Scenarios", "ScenarioSet", "CalibrationResult", "FactorLabel", "compare_runs", "build_toolkit",
        "set_display", "set_log_level"]),
    ("configuration", "Configuration", "/configuration", [
        "ScenariosConfig",
        ("Configuration Classes", [
            "EngineConfig", "ToolkitConfig", "InterestRateConfig", "InflationConfig", "UnemploymentConfig",
            "EquityConfig", "FXConfig", "CreditConfig", "CommodityConfig", "DividendYieldConfig",
            "DividendGrowthConfig", "RealEstateConfig", "YieldCurveConfig", CreditTermStructureConfig, HjmConfig,
            CreditMigrationConfig, LeadingIndicatorConfig, MortalityConfig, CorrelationsConfig, FixedCorrelation]),
        ("Beliefs", ["OUBeliefs", "InterestRateBeliefs", "EquityBeliefs", "BeliefPath"]),
        ("Presets and Profiles", [
            "Profile", "list_presets", "load_profiles", "load_config", "load_profile_library", "scaffold_project"]),
    ]),
    ("interest-rates", "Interest Rates", "/interest-rates", [
        InterestRates, TermStructure, Hjm, Knw, KnwSv, KnwSvQ, Cp2022, Cp2022Vintage, Cp2022Params]),
    ("economy", "Economy", "/economy", [Inflation, Unemployment, Mortality, LeadingIndicator]),
    ("markets", "Markets", "/markets", [
        Equities, FX, Commodities, RealEstate, DividendYield, DividendGrowth, Credit, CreditTermStructure,
        CreditMigration, "rating_migration"]),
    ("regimes", "Regimes", "/regimes", [
        "Regime", "RegimeLibrary", "Shock", "load_regime", "search_regimes", "shock_regime", "stress_test_regime"]),
    ("portfolio", "Portfolio", "/portfolio", [
        "Portfolio", "PortfolioSummary",
        ("Cashflows and Glidepaths", ["CashflowRule", "GlidepathCheckpoint"]),
        ("Portfolio Presets", ["PortfolioPreset", "load_portfolio_preset", "load_portfolio_library"]),
        ("Ticker Mapping", [
            "TickerMapping", "StyleFactor", "TickerNotFoundError", "map_ticker", "add_holdings", "add_ticker_history",
            "compute_portfolio_factor_exposure"]),
        ("History and Metrics", [
            "fetch_historical_data", "build_synthetic_scenario_set", "compute_factor_metrics",
            "compute_price_performance_metrics"]),
    ]),
    ("solvency", "Solvency", "/solvency", [
        "Solvency",
        ("Solvency II Functions", [
            "best_estimate", "solvency_capital_requirement", "interest_rate_scr", "equity_scr",
            "symmetric_adjustment_cap", "eiopa_extrapolation", "eiopa_risk_free_curve", "eiopa_symmetric_adjustment",
            "zero_coupon_curve", "curve_discount_factors", "martingale_test", "market_consistency_check",
            "write_scenario_files"]),
    ]),
    ("validation", "Validation", "/validation", [
        "Relationships", "RelationshipRegion", "Realism", "RealismFactor", "OutOfSample", "OutOfSampleEvaluation",
        NaicGoes, Dnb, compare_published, held_up]),
]
UNDER_THE_HOOD = [
    ("architecture", "How a Run Is Built", "/architecture", []),
    ("simulation-engine", "Simulation Engine", "/simulation-engine", []),
    ("units", "Units", "/units", []),
    ("dependence", "Dependence", "/dependence", [Dependence]),
    ("plotting", "Charts and Plotting", "/plotting", [
        "plot_factors", "plot_fan_chart", "plot_paths", "plot_terminal_distribution", "plot_runs", "plot_portfolios",
        "plot_correlation_matrix", "plot_sleeve_values", "plot_weight_drift"]),
    ("run-files", "Run Files and Releases", "/run-files", [
        ("Run Files", ["write_run", "read_run", "read_run_calibration"]),
        ("Releases", ["publish_calibration", "load_release", "simulate_release"]),
        "Snapshot", "ResultCache", "ScenarioSummary", Reporting]),
    ("coverage", "Coverage", "/coverage", []),
]
PAGES = MODULES + UNDER_THE_HOOD

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


def formulas(text: str) -> str:
    """Bullets after a formula introduction ("The formula is as follows:") become $$ math blocks,
    the same way as on the Finance Toolkit pages."""
    paragraphs = re.split(r"\n[ \t]*\n", text)
    for i in range(1, len(paragraphs)):
        lines = paragraphs[i].split("\n")
        if not all(line.startswith("- ") for line in lines):
            continue
        if not _RE_FORMULA_INTRO.search(paragraphs[i - 1].rstrip().split("\n")[-1].rstrip()):
            continue
        paragraphs[i] = "\n\n".join(_formula_to_latex(line) if _looks_like_formula(line) else line for line in lines)
    return "\n\n".join(paragraphs)


API_SECTIONS = {"Args", "Attributes", "Returns", "Yields", "Raises", "Warns"}


def render_doc(obj, where: str, signature: str | None = None) -> str:
    """The explanation, example and references in the open; the signature, arguments, return value
    and errors folded into one expander at the end, since the page is read for what the method does."""
    doc = inspect.getdoc(obj)
    if not doc:
        warnings.append(f"{where}: no docstring")
        return "*No docstring.*"
    description, sections = split_sections(doc)
    parts = [formulas(fence_indented(description))] if description else []
    api = [code_block(signature)] if signature else []
    for name, body in sections:
        if name in ENTRY_SECTIONS:
            rendered = render_entries(name, body, where)
        elif name in {"Returns", "Yields"}:
            rendered = render_returns(body, where)
        elif name == "References":
            rendered = render_references(body)
        else:
            rendered = formulas(fence_indented(render_free(body)))
        (api if name in API_SECTIONS else parts).append(f"**{name}:**\n\n{rendered}")
    if api:
        label = "Arguments and returns" if len(api) > 1 or not signature else "Signature"
        parts.append(
            f'<details class="ft-details fs-api" markdown="1">\n<summary><b>{label}</b></summary>\n\n'
            + "\n\n".join(api)
            + "\n\n</details>",
        )
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


# ── Reference ──────────────────────────────────────────────────────────────────
def code_block(text: str) -> str:
    return f"```python\n{text}\n```"


def raw(text: str) -> str:
    """Keep Liquid away from docstrings that contain its delimiters."""
    if re.search(r"\{\{|\}\}|\{%|%\}", text):
        if "endraw" in text:
            raise ValueError("a docstring contains {% endraw %}")
        return "{% raw %}\n" + text + "\n{% endraw %}"
    return text


def render_class(cls, level: int, qualify: bool) -> tuple[list[str], int]:
    """The class's own section and one heading a level below it per public member."""
    blocks, count = [], 0
    where = cls.__name__
    if is_model(cls):
        intro = class_fields(cls)
    elif "__init__" in vars(cls):
        intro = format_signature(cls.__name__, cls.__init__, drop_first=True).removesuffix(" -> None")
    else:
        intro = f"{cls.__name__}()"
    blocks.append(raw(f"{'#' * level} {cls.__name__}\n\n{render_doc(cls, where, intro)}"))
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
        blocks.append(raw(f"{'#' * (level + 1)} {title}\n\n{render_doc(func, f'{where}.{name}', sig)}"))
        count += 1
    return blocks, count


def render_function(func, name: str, level: int) -> str:
    sig = format_signature(name, func, drop_first=False)
    return raw(f"{'#' * level} {name}\n\n{render_doc(func, name, sig)}")


def model_functions(cls) -> list[tuple[str, object]]:
    """The public functions in a controller's sibling model module whose docstring states
    a formula: how the class's numbers are calculated, in source order."""
    module = getattr(cls, "__module__", "")
    if not module.endswith("_controller"):
        return []
    try:
        models = importlib.import_module(module[: -len("_controller")] + "_model")
    except ImportError:
        return []
    found = []
    for name, func in inspect.getmembers(models, inspect.isfunction):
        if name.startswith("_") or func.__module__ != models.__name__:
            continue
        if "formula is as follows" in (inspect.getdoc(func) or "").lower():
            found.append((inspect.getsourcelines(func)[1], name, func))
    return [(name, func) for _, name, func in sorted(found)]


def yaml_quote(text: str) -> str:
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


def resolve(member) -> tuple[str, object]:
    """A page member is a name exported by `financescenarios` or a class imported above."""
    if isinstance(member, str):
        return member, getattr(fs, member)
    return member.__name__, member


def flatten(members: list) -> list[tuple[str, object]]:
    out = []
    for member in members:
        out += [resolve(m) for m in member[1]] if isinstance(member, tuple) else [resolve(member)]
    return out


def scenarios_attribute(name: str) -> str | None:
    """The `Scenarios` property that holds a factor or model class (`InterestRates` is `scenarios.interest_rates`)."""
    attribute = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", name).lower()
    return attribute if isinstance(getattr(fs.Scenarios, attribute, None), property) else None


def imports(resolved: list[tuple[str, object]]) -> list[str]:
    """How to reach the page's names: imported from the package, or through a `Scenarios` object."""
    top = [name for name, _ in resolved if name in fs.__all__]
    reached = [(scenarios_attribute(name), name) for name, _ in resolved if name not in fs.__all__]
    reached = [(attribute, name) for attribute, name in reached if attribute]
    other = [(obj.__module__, name) for name, obj in resolved
             if name not in fs.__all__ and scenarios_attribute(name) is None]
    blocks = []
    if top or other:
        lines = ([f"from financescenarios import {', '.join(top)}"] if top else [])
        lines += [f"from {module} import {name}" for module, name in other]
        rest = top + [name for _, name in other]
        which = (f"{', '.join(f'`{name}`' for name in rest)} import{'s' if len(rest) == 1 else ''}" if reached
                 else "Everything on this page imports")
        blocks += [f"{which} as follows:", code_block("\n".join(lines))]
    if reached:
        width = max(len(attribute) for attribute, _ in reached) + len("scenarios.")
        lines = [f"{('scenarios.' + attribute).ljust(width)}  # {name}" for attribute, name in reached]
        many = len(reached) > 1
        lead = (f"The {'factor and model classes are' if many else f'`{reached[0][1]}` class is'} reached through "
                "a `Scenarios` object, after `scenarios = Scenarios.from_profiles(...)`:")
        blocks = [lead, code_block("\n".join(lines))] + blocks
    return blocks


def build_reference(members: list) -> tuple[str, int]:
    resolved = flatten(members)
    with_methods = [obj for _, obj in resolved if inspect.isclass(obj) and public_members(obj)]
    qualify = len(with_methods) > 1
    blocks = [
        "## Reference",
        "The reference is generated from the docstrings in the package, so it says what `help(...)` says in Python: "
        "what each class and function does, a worked example with real output where the docstring has one, and the "
        "arguments and return value folded underneath.",
        *imports(resolved),
    ]
    count = 0

    def add(member, level):
        nonlocal count
        name, obj = resolve(member)
        if inspect.isclass(obj):
            more, n = render_class(obj, level, qualify)
            blocks.extend(more)
            count += n
        else:
            blocks.append(render_function(obj, name, level))
            count += 1

    for member in members:
        if isinstance(member, tuple):
            blocks.append(f"### {member[0]}")
            for inner in member[1]:
                add(inner, 4)
        else:
            add(member, 3)
    formulas, seen = [], set()
    for _, obj in resolved:
        if inspect.isclass(obj):
            for name, func in model_functions(obj):
                if name not in seen:
                    seen.add(name)
                    formulas.append(render_function(func, name, 4))
    if formulas:
        blocks.append("### How It Is Calculated\n\nThe model functions behind this page, each with the formula it implements.")
        blocks.extend(formulas)
        count += len(formulas)
    return "\n\n".join(blocks) + "\n", count


# ── Navigation ─────────────────────────────────────────────────────────────────
RE_INCLUDE = re.compile(r"\{%-?\s*include\s+(financescenarios-[\w-]+/[\w.-]+)\s*-?%\}")
RE_HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
RE_EXPLICIT_ID = re.compile(r"\s*\{#([^}]+)\}\s*$")


def page_body(page: str) -> str:
    """The page's Markdown with its Finance Scenarios includes filled in, as Jekyll renders it."""
    text = (PAGES_DIR / f"{page}.md").read_text().split("\n---\n", 1)[1]
    for _ in range(3):
        text = RE_INCLUDE.sub(lambda m: (INCLUDES / m.group(1)).read_text(), text)
    return text


def headings(text: str) -> list[tuple[int, str, str]]:
    """(level, title, id) of every heading outside code, with the ids kramdown's GFM parser gives them."""
    out, fence, seen = [], False, Counter()
    for line in text.split("\n"):
        if line.lstrip().startswith(("```", "~~~")):
            fence = not fence
            continue
        match = None if fence else RE_HEADING.match(line)
        if not match:
            continue
        title = match.group(2)
        explicit = RE_EXPLICIT_ID.search(title)
        title = RE_EXPLICIT_ID.sub("", title)
        plain = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", title).replace("`", "").replace("**", "")
        if explicit:
            anchor = explicit.group(1)
        else:
            anchor = re.sub(r"[^\w\- ]", "", plain.lower()).replace(" ", "-")
            seen[anchor] += 1
            if seen[anchor] > 1:
                anchor += f"-{seen[anchor] - 1}"
        out.append((len(match.group(1)), plain, anchor))
    return out


def sections(page: str, title: str) -> list[tuple[str, list[tuple[str, str]]]]:
    """The sidebar groups of a page: a module page lists the h3s under each h2 (Getting Started, How It Works,
    Reference); another page lists its h2s under its title, then the h3s of its Reference."""
    found = headings(page_body(page))
    groups: list[tuple[str, list[tuple[str, str]]]] = []
    if any(level == 2 and text == "Getting Started" for level, text, _ in found):
        for level, text, anchor in found:
            if level == 2:
                groups.append((text, []))
            elif level == 3 and groups:
                groups[-1][1].append((text, anchor))
        return [group for group in groups if group[1]]
    own = [(text, anchor) for level, text, anchor in found if level == 2 and text != "Reference"]
    groups = [(title, own)] if own else []
    in_reference, reference = False, []
    for level, text, anchor in found:
        if level == 2:
            in_reference = text == "Reference"
        elif level == 3 and in_reference:
            reference.append((text, anchor))
    return groups + ([("Reference", reference)] if reference else [])


def navigation_entry(page: str, title: str, path: str) -> list[str]:
    key = "financescenarios-docs" if page == "docs" else f"financescenarios-docs-{page}"
    lines = [f"{key}:"]
    for group, pages in (("Modules", MODULES), ("Under the Hood", UNDER_THE_HOOD)):
        lines += [f"  - title: {group}", "    children:"]
        for _, other, other_path, _ in pages:
            lines += [f"    - title: {yaml_quote(other)}", f"      url: {DOCS}{other_path}"]
    for group, children in sections(page, title):
        lines += [f"  - title: {yaml_quote(group)}", "    children:"]
        for text, anchor in children:
            lines += [f"      - title: {yaml_quote(text)}", f"        url: {DOCS}{path}#{anchor}"]
    return lines


def write_navigation() -> None:
    """Replace the financescenarios-docs* entries of _data/navigation.yml, keeping their place in the file."""
    lines = NAVIGATION.read_text().split("\n")
    keys = [i for i, line in enumerate(lines) if re.match(r"^[A-Za-z][\w-]*:\s*$", line)]
    ours = [i for i in keys if lines[i].startswith("financescenarios-docs")]
    if not ours:
        sys.exit("_data/navigation.yml has no financescenarios-docs entry")
    start = ours[0]
    end = next((i for i in keys if i > start and not lines[i].startswith("financescenarios-docs")), len(lines))
    entries = []
    for page, title, path, _ in PAGES:
        entries += navigation_entry(page, title, path) + [""]
    NAVIGATION.write_text("\n".join(lines[:start] + entries + lines[end:]))


def main() -> None:
    placed = Counter(name for *_, members in PAGES for name, _ in flatten(members))
    public = set(fs.__all__) - {"__version__"}
    missing = sorted(public - set(placed))
    twice = sorted(name for name, n in placed.items() if n > 1)
    if missing or twice:
        sys.exit(f"public names without a page: {missing}; on two pages: {twice}")
    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob("*.md"):
        old.unlink()
    counts = {}
    for page, _, _, members in PAGES:
        if members:
            text, counts[page] = build_reference(members)
            (OUT / f"{page}.md").write_text(text)
    write_navigation()
    print(f"{len(counts)} references, {sum(counts.values())} methods and functions documented; navigation written")
    for warning in warnings:
        print("warning:", warning)


if __name__ == "__main__":
    main()
