"""
This file generates the Finance Toolkit documentation pages by fetching docstrings
from the controller modules on GitHub and converting them to Jekyll Markdown.
"""

import base64
import os
import re
import sys

import requests

# ── Compiled regexes (module-level, compiled once) ────────────────────────────
_RE_FUNC = re.compile(r"def\s+(\w+)\([\s\S]*?\"\"\"([\s\S]*?)\"\"\"")
_RE_URL = re.compile(r"https?://\S+")
_RE_ARG_LABEL = re.compile(r"\w+ \([^)]+\):")
_RE_MULTI_SPACE = re.compile(r" +")
_RE_BLANK_LINE = re.compile(r"\n[ \t]*\n")
_RE_DESCRIPTION = re.compile(r"([\s\S]*?)(?:Args:|As an example:|$)", re.DOTALL)
_RE_ARGUMENTS = re.compile(r"(Args:[\s\S]*?)(```python|$)", re.DOTALL)
_RE_CODE = re.compile(r"```python([\s\S]*?)```", re.DOTALL)
_RE_RESULT = re.compile(r"Which returns:[\s\S]*$", re.DOTALL)

# Section headers that get bolded wherever they appear as their own paragraph.
_BOLD_HEADERS = ("Also known as:", "See definition:", "See Definition:")

_GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
_REQUEST_TIMEOUT = 30

# ── Local mode ──────────────────────────────────────────────────────────────
# Set DOCS_LOCAL_PATH (or pass --local) to read controller modules straight
# off disk instead of hitting the GitHub API. Points at the financetoolkit
# package directory, e.g. /Users/jeroenbouma/Documents/FinanceToolkit/financetoolkit
_DEFAULT_LOCAL_PATH = "/Users/jeroenbouma/Documents/FinanceToolkit/financetoolkit"
_LOCAL_PATH = os.environ.get("DOCS_LOCAL_PATH", "")
if "--local" in sys.argv and not _LOCAL_PATH:
    _LOCAL_PATH = _DEFAULT_LOCAL_PATH

_INSTALL_SNIPPET = """\
To install the FinanceToolkit it simply requires the following:

```python
pip install financetoolkit -U
```

{% include algolia.html %}

"""


def _trim_url(url: str) -> tuple[str, str]:
    """Split a raw regex match into (url, trailing_punctuation).

    Sentence punctuation directly after a URL (e.g. "See https://x.com.")
    is not part of the link, but a closing paren that balances one inside
    the URL itself (e.g. Wikipedia's ".../wiki/Beta_(finance)") is.
    """
    trailing = ""
    while url and url[-1] in ".,;:!?":
        trailing = url[-1] + trailing
        url = url[:-1]
    if url.endswith(")") and url.count("(") < url.count(")"):
        trailing = ")" + trailing
        url = url[:-1]
    return url, trailing


def _linkify(text: str) -> str:
    def _replace(match: re.Match) -> str:
        url, trailing = _trim_url(match.group(0))
        return f'[{url}]({url}){{:target="_blank"}}{trailing}'

    return _RE_URL.sub(_replace, text)


def _underline_arg(match: re.Match) -> str:
    return f"- <u>{match.group(0)}</u>"


def _dedent_block(text: str) -> str:
    """Strip the docstring's fixed source indentation while preserving any
    relative indentation the author used (e.g. nested multi-line calls or
    aligned table columns).

    The section regexes (Args:, Which returns:, ...) match starting mid-line,
    right after the header text, so the first captured line often has zero
    leading whitespace even though every other line shares the docstring's
    real indent. That lone unindented line would otherwise fool
    `textwrap.dedent` into stripping nothing at all, so it is excluded when
    the common indent is computed.
    """
    lines = text.strip("\n").split("\n")
    if not lines:
        return ""

    indents = [len(l) - len(l.lstrip(" ")) for l in lines[1:] if l.strip()]
    if not indents:
        return "\n".join(l.strip() for l in lines).strip()

    base = min(indents)
    dedented = [lines[0].strip()] + [
        l[base:] if l.strip() else "" for l in lines[1:]
    ]
    return "\n".join(dedented).strip("\n")


def _clean_description(text: str) -> str:
    """Turn a raw docstring description into clean Markdown.

    Paragraphs are detected via blank lines (the only reliable signal in the
    source). A paragraph is treated as a bullet list only if *every* one of
    its lines already starts with "- " once dedented - anything else
    (formula minus signs, hyphenated words, negative numbers) is left alone.

    Source docstrings often put a blank line between each bullet (for their
    own readability). If that blank line survived into the Markdown, Kramdown
    would render the list as "loose" - wrapping each item's text in its own
    <p> - which double-applies the site's `.page__content li { font-size:
    0.8em }` rule (once for the <li>, again for the nested <p>) and renders
    the bullets visibly smaller than surrounding text. Consecutive
    bullet-list paragraphs are therefore joined with a single newline so
    Kramdown treats them as one tight list instead.
    """
    text = text.replace("—", "-")  # em dash -> hyphen, used for formula minus signs

    paragraphs = []
    for raw_paragraph in _RE_BLANK_LINE.split(_dedent_block(text)):
        lines = [_RE_MULTI_SPACE.sub(" ", line.strip()) for line in raw_paragraph.split("\n")]
        lines = [line for line in lines if line]
        if not lines:
            continue

        for header in _BOLD_HEADERS:
            if lines[0].startswith(header):
                lines[0] = f"**{header}**{lines[0][len(header):]}"
                break

        is_bullet_list = all(line.startswith("- ") for line in lines)
        # A paragraph "is" a bullet (for joining purposes) whenever it starts
        # with "- ", even if it's really one bullet whose continuation lines
        # got wrapped without a "- " prefix (is_bullet_list is False for
        # those, but they still need to join tightly with neighbouring
        # bullets rather than getting a blank line before them).
        starts_as_bullet = lines[0].startswith("- ")
        paragraph = "\n".join(lines) if is_bullet_list else " ".join(lines)
        paragraphs.append((paragraph, starts_as_bullet))

    parts = []
    for i, (paragraph, starts_as_bullet) in enumerate(paragraphs):
        if i > 0:
            parts.append("\n" if starts_as_bullet and paragraphs[i - 1][1] else "\n\n")
        parts.append(paragraph)

    return "".join(parts)


def _local_file_path(file_url: str) -> str:
    """Map a GitHub contents-API URL to its local file path under _LOCAL_PATH."""
    relative_path = file_url.split(f"{_BASE}/", 1)[1]
    return os.path.join(_LOCAL_PATH, relative_path)


def _fetch_file(url: str) -> str:
    if _LOCAL_PATH:
        local_path = _local_file_path(url)
        with open(local_path, encoding="utf-8") as f:
            return f.read()

    headers = {"Authorization": f"token {_GITHUB_TOKEN}"} if _GITHUB_TOKEN else {}
    try:
        response = requests.get(url, headers=headers, timeout=_REQUEST_TIMEOUT)
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        if response.status_code == 403:
            raise RuntimeError(
                f"GitHub API rate limit likely exceeded fetching {url}. "
                "Set a GITHUB_TOKEN environment variable to raise the limit."
            ) from error
        raise RuntimeError(f"Failed to fetch {url}: {error}") from error
    except requests.exceptions.RequestException as error:
        raise RuntimeError(f"Network error fetching {url}: {error}") from error

    data = response.json()
    if "content" not in data:
        raise ValueError(f"No 'content' key in GitHub API response for {url}")
    return base64.b64decode(data["content"]).decode("utf-8")


def create_markdown_file(file_url: str, header: str, location: str) -> None:
    file_content = _fetch_file(file_url)

    functions_with_docstrings = []
    for function_name, docstring in _RE_FUNC.findall(file_content):
        # Skip private and dunder methods
        if function_name.startswith("_"):
            continue

        # Description
        desc_m = _RE_DESCRIPTION.match(docstring)
        description = _clean_description(desc_m.group(1)) if desc_m else ""
        description = _linkify(description)

        # Arguments (also covers Returns / Raises / Notes, which follow Args:)
        args_m = _RE_ARGUMENTS.search(docstring)
        arguments = _linkify(args_m.group(1)) if args_m else ""
        arguments = _dedent_block(arguments)
        arguments = _RE_ARG_LABEL.sub(_underline_arg, arguments)
        arguments = "\n".join(
            _RE_MULTI_SPACE.sub(" ", line).strip() for line in arguments.split("\n")
        )

        # Example code block
        code_m = _RE_CODE.search(docstring)
        example_code = _dedent_block(code_m.group(1)) if code_m else ""

        # Example result
        result_m = _RE_RESULT.search(docstring)
        example_result = _dedent_block(result_m.group(0)) if result_m else ""

        functions_with_docstrings.append({
            "function_name": function_name,
            "description": description,
            "arguments": arguments,
            "example_code": example_code,
            "example_result": example_result,
        })

    markdown_content = header
    for fn in functions_with_docstrings:
        markdown_content += f'## {fn["function_name"]}\n'
        markdown_content += f'{fn["description"]}\n\n'

        if fn["arguments"]:
            arguments = (
                fn["arguments"]
                .replace("Args:", "**Args:**")
                .replace("Raises:", "**Raises:**")
                .replace("Returns:", "**Returns:**")
                .replace("Notes:", "**Notes:**")
                .replace("As an example:", "**As an example:**")
            )
            # Ensure a blank line follows each bolded header so a directly
            # adjacent bullet list (e.g. "**Notes:**\n- ...") renders as a list.
            arguments = re.sub(r"(\*\*[^*]+:\*\*)\n(?!\n)", r"\1\n\n", arguments)
            markdown_content += arguments
            markdown_content += "\n"

        if fn["example_code"]:
            markdown_content += f"\n```python\n{fn['example_code']}\n```\n"

        if fn["example_result"]:
            result_body = fn["example_result"].replace("Which returns:", "").strip()
            markdown_content += f"\nWhich returns:\n\n{result_body}\n\n"

        markdown_content += "\n---\n\n"

    with open(location, "w", encoding="utf-8") as f:
        f.write(markdown_content)

    print(f"✓  {location}  ({len(functions_with_docstrings)} functions)")


# ── Page definitions ──────────────────────────────────────────────────────────
_BASE = "https://api.github.com/repos/JerBouma/FinanceToolkit/contents/financetoolkit"

PAGES = [
    {
        "url": f"{_BASE}/toolkit_controller.py",
        "location": "_pages/financetoolkit/documentation/docs.md",
        "header": f"""---
title: Documentation
excerpt: This the documentation of the FinanceToolkit. This is an open-source toolkit in which 200+ financial ratios, indicators and performance measurements are written down in the most simplistic way allowing for complete transparency of the calculation method.
description: This the documentation of the FinanceToolkit. This is an open-source toolkit in which 200+ financial ratios, indicators and performance measurements are written down in the most simplistic way allowing for complete transparency of the calculation method.
author_profile: false
permalink: /projects/financetoolkit/docs
classes: wide-sidebar
layout: single
redirect_from:
    - /docs
sidebar:
    nav: "financetoolkit-docs"
---

This page includes all the documentation for the Finance Toolkit, an open-source toolkit in which all relevant financial ratios (200+), indicators and performance measurements are written down in the most simplistic way allowing for complete transparency of the calculation method. Each functionality includes an example of how to use it and is therefore an excellent way to better understand how to use each functionality. These examples are also directly embedded in the code. For simplicity sake, only the controller modules are included here given that the models themselves should be relatively straightforward. Make sure to also have a look at the example notebooks as found [here](/projects/financetoolkit#how-to-guides-for-the-financetoolkit).

{_INSTALL_SNIPPET}The Toolkit Module is a collection of functions that collect and parse data, including historical data, fundamental data (balance, income and cash flow statements) and metrics from Financial Modeling Prep such as enterprise values, company profiles and more. From this module you can access all related sub-modules.

""",
    },
    {
        "url": f"{_BASE}/discovery/discovery_controller.py",
        "location": "_pages/financetoolkit/documentation/discovery.md",
        "header": f"""---
title: Discovery
excerpt: The Discovery Module contains lists of companies, cryptocurrencies, forex, commodities, etfs and indices including screeners, quotes, performance metrics and more to find and select tickers to use in the Finance Toolkit.
description: The Discovery Module contains lists of companies, cryptocurrencies, forex, commodities, etfs and indices including screeners, quotes, performance metrics and more to find and select tickers to use in the Finance Toolkit.
author_profile: false
permalink: /projects/financetoolkit/docs/discovery
classes: wide-sidebar
layout: single
redirect_from:
    - /discovery
sidebar:
    nav: "financetoolkit-docs-discovery"
---

The Discovery Module contains lists of companies, cryptocurrencies, forex, commodities, ETFs and indices including screeners, quotes, performance metrics and more to find and select tickers to use in the Finance Toolkit.

{_INSTALL_SNIPPET}""",
    },
    {
        "url": f"{_BASE}/ratios/ratios_controller.py",
        "location": "_pages/financetoolkit/documentation/ratios.md",
        "header": f"""---
title: Ratios
excerpt: The Ratios Module contains over 50+ ratios that can be used to analyse companies. These ratios are divided into 5 categories which are efficiency, liquidity, profitability, solvency and valuation. Each ratio is calculated using the data from the Toolkit module.
description: The Ratios Module contains over 50+ ratios that can be used to analyse companies. These ratios are divided into 5 categories which are efficiency, liquidity, profitability, solvency and valuation. Each ratio is calculated using the data from the Toolkit module.
author_profile: false
permalink: /projects/financetoolkit/docs/ratios
classes: wide-sidebar
layout: single
redirect_from:
    - /ratios
sidebar:
    nav: "financetoolkit-docs-ratios"
---

The Ratios Module contains 50+ ratios divided into 5 categories: efficiency, liquidity, profitability, solvency and valuation. Each ratio is calculated using the data from the Toolkit module.

{_INSTALL_SNIPPET}""",
    },
    {
        "url": f"{_BASE}/models/models_controller.py",
        "location": "_pages/financetoolkit/documentation/models.md",
        "header": f"""---
title: Models
excerpt: The Models module is meant to execute well-known models such as DUPONT and the Discounted Cash Flow (DCF) model. These models are also directly related to the data retrieved from the Toolkit module.
description: The Models module is meant to execute well-known models such as DUPONT and the Discounted Cash Flow (DCF) model. These models are also directly related to the data retrieved from the Toolkit module.
author_profile: false
permalink: /projects/financetoolkit/docs/models
classes: wide-sidebar
layout: single
redirect_from:
    - /models
sidebar:
    nav: "financetoolkit-docs-models"
---

The Models module executes well-known models such as DuPont analysis and the Discounted Cash Flow (DCF) model, using data retrieved from the Toolkit module.

{_INSTALL_SNIPPET}""",
    },
    {
        "url": f"{_BASE}/options/options_controller.py",
        "location": "_pages/financetoolkit/documentation/options.md",
        "header": f"""---
title: Options
excerpt: The Options module is meant to calculate important options metrics such as the First, Second and Third Order Greeks, the Black Scholes Model and the Option Chains as well as Implied Volatilities, Breeden Litzenberger and more.
description: The Options module is meant to calculate important options metrics such as the First, Second and Third Order Greeks, the Black Scholes Model and the Option Chains as well as Implied Volatilities, Breeden Litzenberger and more.
author_profile: false
permalink: /projects/financetoolkit/docs/options
classes: wide-sidebar
layout: single
redirect_from:
    - /options
sidebar:
    nav: "financetoolkit-docs-options"
---

The Options module calculates important options metrics including First, Second and Third Order Greeks, the Black-Scholes Model, Option Chains, Implied Volatilities, Breeden–Litzenberger and more.

{_INSTALL_SNIPPET}""",
    },
    {
        "url": f"{_BASE}/technicals/technicals_controller.py",
        "location": "_pages/financetoolkit/documentation/technicals.md",
        "header": f"""---
title: Technicals
excerpt: The Technicals Module contains 30+ Technical Indicators that can be used to analyse companies. These ratios are divided into 4 categories which are breadth, momentum, overlap and volatility. Each indicator is calculated using the data from the Toolkit module.
description: The Technicals Module contains 30+ Technical Indicators that can be used to analyse companies. These ratios are divided into 4 categories which are breadth, momentum, overlap and volatility. Each indicator is calculated using the data from the Toolkit module.
author_profile: false
permalink: /projects/financetoolkit/docs/technicals
classes: wide-sidebar
layout: single
redirect_from:
    - /technicals
sidebar:
    nav: "financetoolkit-docs-technicals"
---

The Technicals Module contains 30+ technical indicators divided into 4 categories: breadth, momentum, overlap and volatility.

{_INSTALL_SNIPPET}""",
    },
    {
        "url": f"{_BASE}/fixedincome/fixedincome_controller.py",
        "location": "_pages/financetoolkit/documentation/fixedincome.md",
        "header": f"""---
title: Fixed Income
excerpt: The Fixed Income module contains a wide variety of fixed income related calculations such as the Effective Yield, the Macaulay Duration, the Modified Duration Convexity, the Yield to Maturity and models such as Black and Bachelier to valuate derivative instruments such as Swaptions.
description: The Fixed Income module contains a wide variety of fixed income related calculations such as the Effective Yield, the Macaulay Duration, the Modified Duration Convexity, the Yield to Maturity and models such as Black and Bachelier to valuate derivative instruments such as Swaptions.
author_profile: false
permalink: /projects/financetoolkit/docs/fixedincome
classes: wide-sidebar
layout: single
redirect_from:
    - /fixedincome
sidebar:
    nav: "financetoolkit-docs-fixedincome"
---

The Fixed Income module covers a wide variety of calculations including the Effective Yield, Macaulay Duration, Modified Duration, Convexity, Yield to Maturity and derivative pricing models such as Black and Bachelier (used for Swaptions and other instruments).

{_INSTALL_SNIPPET}""",
    },
    {
        "url": f"{_BASE}/risk/risk_controller.py",
        "location": "_pages/financetoolkit/documentation/risk.md",
        "header": f"""---
title: Risk
excerpt: The Risk module is meant to calculate important risk metrics such as Value at Risk (VaR), Conditional Value at Risk (cVaR), Maximum Drawdown, Correlations, GARCH, EWMA and more.
description: The Risk module is meant to calculate important risk metrics such as Value at Risk (VaR), Conditional Value at Risk (cVaR), Maximum Drawdown, Correlations, GARCH, EWMA and more.
author_profile: false
permalink: /projects/financetoolkit/docs/risk
classes: wide-sidebar
layout: single
redirect_from:
    - /risk
sidebar:
    nav: "financetoolkit-docs-risk"
---

The Risk module calculates important risk metrics such as Value at Risk (VaR), Conditional Value at Risk (CVaR), Maximum Drawdown, Correlations, GARCH, EWMA and more.

{_INSTALL_SNIPPET}""",
    },
    {
        "url": f"{_BASE}/performance/performance_controller.py",
        "location": "_pages/financetoolkit/documentation/performance.md",
        "header": f"""---
title: Performance
excerpt: The Performance module is meant to calculate important performance metrics such as Sharpe Ratio, Sortino Ratio, Treynor Ratio, Information Ratio, Jensen's Alpha, Beta, Capital Asset Pricing Model, R-Squared and more.
description: The Performance module is meant to calculate important performance metrics such as Sharpe Ratio, Sortino Ratio, Treynor Ratio, Information Ratio, Jensen's Alpha, Beta, Capital Asset Pricing Model, R-Squared and more.
author_profile: false
permalink: /projects/financetoolkit/docs/performance
classes: wide-sidebar
layout: single
redirect_from:
    - /performance
sidebar:
    nav: "financetoolkit-docs-performance"
---

The Performance module calculates important performance metrics such as the Sharpe Ratio, Sortino Ratio, Treynor Ratio, Information Ratio, Jensen's Alpha, Beta, Capital Asset Pricing Model (CAPM), R-Squared and more.

{_INSTALL_SNIPPET}""",
    },
    {
        "url": f"{_BASE}/economics/economics_controller.py",
        "location": "_pages/financetoolkit/documentation/economics.md",
        "header": f"""---
title: Economics
excerpt: The Economics module gives insights for 60+ countries into key economic indicators such as the Consumer Price Index (CPI), Gross Domestic Product (GDP), Unemployment Rates and 3-month and 10-year Government Interest Rates. This is done through the economics module and can be used as a standalone module as well.
description: The Economics module gives insights for 60+ countries into key economic indicators such as the Consumer Price Index (CPI), Gross Domestic Product (GDP), Unemployment Rates and 3-month and 10-year Government Interest Rates. This is done through the economics module and can be used as a standalone module as well.
author_profile: false
permalink: /projects/financetoolkit/docs/economics
classes: wide-sidebar
layout: single
redirect_from:
    - /economics
sidebar:
    nav: "financetoolkit-docs-economics"
---

The Economics module provides insights for 60+ countries into key economic indicators such as the Consumer Price Index (CPI), Gross Domestic Product (GDP), Unemployment Rates and government interest rates. It can also be used as a standalone module.

{_INSTALL_SNIPPET}""",
    },
    {
        "url": f"{_BASE}/portfolio/portfolio_controller.py",
        "location": "_pages/financetoolkit/documentation/portfolio.md",
        "header": f"""---
title: Portfolio
excerpt: The Portfolio module is meant to calculate important portfolio metrics allows you to compare your own portfolio to a benchmark, seeing performance of individual assets and directly load the portfolio into the Finance Toolkit.
description: The Portfolio module is meant to calculate important portfolio metrics allows you to compare your own portfolio to a benchmark, seeing performance of individual assets and directly load the portfolio into the Finance Toolkit.
author_profile: false
permalink: /projects/financetoolkit/docs/portfolio
classes: wide-sidebar
layout: single
redirect_from:
    - /portfolio
sidebar:
    nav: "financetoolkit-docs-portfolio"
---

The Portfolio module calculates important portfolio metrics, allowing you to compare your portfolio against a benchmark, analyse individual asset performance and load your portfolio directly into the Finance Toolkit.

{_INSTALL_SNIPPET}""",
    },
]

# ── Generate all pages ────────────────────────────────────────────────────────
if __name__ == "__main__":
    if _LOCAL_PATH:
        print(f"Local mode: reading controllers from {_LOCAL_PATH}\n")
    for page in PAGES:
        create_markdown_file(page["url"], page["header"], page["location"])
