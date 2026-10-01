---
title: Build your Model
seo_title: Build a Financial Model in Python
excerpt: "Build financial models that last, with modular code, clear styling, the PEP 8 conventions and a careful review of AI-written code."
description: "Build financial models that last, with modular code, clear styling, the PEP 8 conventions and a careful review of AI-written code."
author_profile: true
permalink: /modelling/build-your-model
classes: wide-sidebar
author_profile: false
sidebar:
    nav: "modelling"
---

A financial model can serve multiple purposes, ranging from simple data aggregation to complex forecasting and scenario analysis. However complex it is, the model should be clear, maintainable, and easy to extend. That is why the modular programming discussed in [Structure your Model](/modelling/structure-your-model) matters so much. For examples of this method and inspiration for building your own model, have a look at projects like the [Finance Toolkit](https://github.com/JerBouma/FinanceToolkit){: target="_blank"}, [Finance Database](https://github.com/JerBouma/FinanceDatabase){: target="_blank"}, [OpenBB Terminal](https://github.com/OpenBB-finance/OpenBB){: target="_blank"}, [yfinance](https://github.com/ranaroussi/yfinance){: target="_blank"}, and [Riskfolio-Lib](https://github.com/dcajasn/Riskfolio-Lib){: target="_blank"}.

Regardless of the model's purpose, applying consistent styling and coding guidelines helps remove the subjective nature of coding. A style guide ensures code consistency, making it easier to read and maintain. This matters most when multiple developers work on the same codebase or when colleagues move between teams and need to understand models they haven't seen before.

Linters, as discussed in [Setting up your Project](/modelling/setting-up-your-project#setting-up-linters), automate much of the initial code styling. However, linters cannot enforce choices regarding coding methods, variable naming conventions, or docstring structures. For those choices you need a style guide such as [**PEP 8**](https://peps.python.org/pep-0008/){: target="_blank"}.

With an assistant writing the code, you will rarely apply these conventions by hand. Instead, they serve two purposes. First, they are instructions: put them in your [instruction file](/modelling/working-with-ai#instruction-files) and let the linters enforce what can be automated, so every generated function follows the same style. Second, they are what makes code reviewable: consistent names, type hints and docstrings let you read a generated function in seconds and see what it is supposed to do. The sections below explain each convention so you know what to ask for and what to look for.

{: .notice--info}
**Why a Universal Style is Important**<br>
You might be accustomed to specific styling methods from your firm or university. However, I recommend adopting a universally accepted style like PEP 8, as countless developers use it. This standardization makes collaboration much easier, because other developers can quickly understand your code. Adhering to PEP standards also gives you clear guidelines and avoids conflicts with automated linters.

## Default Styling

Throughout this page, PEP (Python Enhancement Proposal) is frequently referenced. A PEP is a technical design document for the Python community, outlining new features, processes, or environmental standards for the language. These proposals represent community consensus and therefore describe established best practices.

The styles described by **PEP 8** (see [here](https://peps.python.org/pep-0008/){: target="_blank"}) define conventions for general code structure. As the default style adopted by numerous developers, it ensures consistency across both internal and external tooling. I recommend reading the PEP 8 documentation itself for a thorough understanding; this section summarizes the main components.

Key aspects of code layout include:

-   [**Indentation**](https://peps.python.org/pep-0008/#indentation){: target="_blank"}: Use 4 spaces per indentation level. This is the standard in most code editors.
-   [**Maximum line length**](https://peps.python.org/pep-0008/#maximum-line-length){: target="_blank"}: While 79 characters is the traditional recommendation (originally based on screen resolution limitations), PEP 8 allows flexibility. Limits up to 99 or even 122 characters are common practice today due to improved screen resolutions.
-   [**Line Breaks**](https://peps.python.org/pep-0008/#should-a-line-break-before-or-after-a-binary-operator){: target="_blank"}: Should generally occur *before* binary operators, aligning with mathematical conventions where the operator precedes the operand on the new line.
-   [**Blank Lines**](https://peps.python.org/pep-0008/#blank-lines){: target="_blank"}: Use blank lines appropriately to separate functionality. Surround top-level functions and classes with two blank lines, and methods within a class with one blank line. Use blank lines sparingly within functions to indicate logical sections.
-   [**Source File Encoding**](https://peps.python.org/pep-0008/#source-file-encoding){: target="_blank"}: Always use UTF-8 encoding for source files. Code identifiers (variables, functions, classes, comments) should be in English, except for widely understood abbreviations.
-   [**Import statements**](https://peps.python.org/pep-0008/#imports){: target="_blank"}: Each import should generally be on a separate line. Imports should be explicit, specifying the modules being imported (e.g., `from package import module1, module2`) rather than using wildcard imports (`from package import *`). Imports should be grouped in the standard order: standard library, related third-party, local application/library specific.
-   [**Module Level Dunder Names**](https://peps.python.org/pep-0008/#module-level-dunder-names){: target="_blank"}: Module-level "dunders" (names with double leading and trailing underscores), such as `__version__` or `__author__`, should be placed after the module docstring but before any import statements, except for `from __future__` imports.

## Naming Conventions

Recommended naming conventions include:

-   **Classes:** Use `CapWords` (also known as PascalCase), like `Ratios` or `FinancialModel`.
-   **Functions:** Use `lowercase_with_underscores` (snake_case), often starting with a verb, like `calculate_gross_margin` or `get_data`.
-   **Variables:** Use `lowercase_with_underscores` (snake_case), like `margin` or `gross_margin`.
-   **Constants:** Use `UPPERCASE_WITH_UNDERSCORES` (SCREAMING_SNAKE_CASE), like `INTEREST_RATE` or `PERIOD`. Constants represent values that are not intended to change.
-   **Internal Use (Protected):** Use a single leading underscore, like `_income_statement`. This convention indicates that a variable or method is intended for internal use within a class or module, although it's not strictly enforced by Python.

The goal of these conventions is to make code more readable by indicating the intended use of a name (e.g., class, function, variable, constant) simply by its format. For instance, `calculate_gross_margin` clearly suggests a function, while `gross_margin` suggests a variable and `PERIOD` suggests a constant.

Choose descriptive names over overly abbreviated ones. For example, `microsoft_trailing_gross_margin` is preferable to `msft_ttm_gm`. Brevity has its place, but clarity matters more, especially considering that *code is read far more often than it is written.* Avoid generic names like `df` unless the scope is very limited and the meaning is obvious from context.

When collaborating, remember that your code needs to be understandable by others, even in your absence (e.g., during holidays, sick leave, or after you've left the team).

## Applying Typing

Use type hints for variables and function signatures as defined in PEP 484 (Type Hints) and PEP 526 (Syntax for Variable Annotations). Type hints improve code clarity and allow static analysis tools to catch potential errors. Examples:

<div class="row">
<div markdown="1" class="fifty-column-left mobile-max-column-width">

```python
# General definition
revenue: pd.Series = pd.Series([1, 2, 3])

# Multiple possible types based on any
cost_of_goods_sold: pd.Series | float = 5

# Definitions within a dictionary
reported_values: dict[str, float] = {
    "revenue": 500,
    "cost_of_goods_sold": 200,
    "gross_margin": 0.6,
}
```

</div>
<div markdown="1" class="fifty-column-left mobile-max-column-width">

```python
# Constant definition (use Final for linters)
from typing import Final

# Multiple possible types based on Pandas
transactions: pd.DataFrame | pd.Series = (
    pd.Series([10, 15, 5])
)

# Defining dtypes at the same time
margin: pd.DataFrame = pd.DataFrame(
    data=[0.8, 0.3, 0.2],
    dtype=np.float64)
```
</div>
</div>

Type hints should also be applied to function parameters and return values:

<div class="row">
<div markdown="1" class="fifty-column-left mobile-max-column-width">

```python
def get_gross_margin(
    revenue: pd.Series | int,
    cost_of_goods_sold: int) -> pd.Series:
    """Docstring here"""
    # Code here
    return
```
</div>
<div markdown="1" class="fifty-column-left mobile-max-column-width">

```python
def get_cost_of_goods_sold(
    transactions: pd.DataFrame | pd.Series,
    margin: pd.DataFrame)  -> pd.DataFrame:
    """Docstring here"""
    # Code here
    return
```
</div>
</div>

Omitting type hints reduces code clarity, forcing users to rely solely on docstrings or reading the implementation to understand function inputs and outputs. When reviewing generated code, the signature is the first thing to read: if a model function takes a full DataFrame instead of a Series, it probably depends on specific column names and doesn't belong in the Model layer.

## Writing Docstrings

Write clear and informative docstrings following PEP 257 (Docstring Conventions). Consistent docstring formatting is widely accepted and supported by many development tools. Here's an example using the Google style format:

```python
def function_name(param1: type, param2: type) -> return_type:
    """
    Description of the function and its arguments.

    Args:
        param1 (type): Description of the first parameter.
        param2 (type): Description of the second parameter.

    Returns:
        return_type: Description of the return value.

    Raises:
        KeyError: Description of the exception raised.
    """
```

While this example uses the Google format, other formats like [reStructuredText (reST)](https://docutils.sourceforge.io/rst.html){: target="_blank"} or NumPy style are also common. The chosen format is less important than ensuring the docstring clearly explains the function's purpose, arguments (including types), return value(s), and any exceptions raised. The goal is to allow users to understand the function without needing to inspect its source code.

Aim for complete docstrings; it's generally better to provide too much detail than too little. Docstrings are a good place to explain underlying financial theory or complex logic within the function. Assistants write them well; it's still worth a quick check that the formula and assumptions described match the definition you want to use. Below is an extensive example (from the [Finance Toolkit](https://github.com/JerBouma/FinanceToolkit/blob/main/financetoolkit/performance/performance_model.py#L129-L174){: target="_blank"}) demonstrating the level of detail possible:

```python
def get_capital_asset_pricing_model(
    risk_free_rate: pd.Series | float,
    beta: pd.Series | pd.DataFrame | float,
    benchmark_returns: pd.Series | float,
) -> pd.Series | pd.DataFrame | float:
    """
    CAPM, or the Capital Asset Pricing Model, is a financial model used to estimate
    the expected return on an investment, such as a stock or portfolio of stocks. It
    provides a framework for evaluating the risk and return trade-off of an asset or
    portfolio in relation to the overall market. CAPM is based on the following
    key components:

    1. Risk-Free Rate (Rf): This is the theoretical return an investor could earn from
    an investment with no risk of financial loss. It is typically based on the yield
    of a government bond.
    
    2. Market Risk Premium (Rm - Rf): This represents the additional return that
    investors expect to earn for taking on the risk of investing in the overall market
    as opposed to a risk-free asset. It is calculated as the difference between the
    expected return of the market (Rm) and the risk-free rate (Rf).
    
    3. Beta (β): Beta is a measure of an asset's or portfolio's sensitivity to market 
    movements. It quantifies how much an asset's returns are expected to move in relation
    to changes in the overall market. A beta of 1 indicates that the asset moves in
    line with the market, while a beta greater than 1 suggests higher volatility, and
    a beta less than 1 indicates lower volatility.

    The formula is as follows:

    Expected Return (ER) = Risk-Free Rate (Rf) + Beta (β) * Market Risk Premium (Rm - Rf)

    Args:
        risk_free_rate (pd.Series | float): the risk free rate.
        beta (pd.Series | pd.DataFrame | float): the beta.
        benchmark_returns (pd.Series | float): the benchmark returns.

    Returns:
        pd.Series | pd.DataFrame | float: the capital asset pricing model.

    Raises:
        TypeError: if beta is not a pd.Series, pd.DataFrame or float.
    """
    if isinstance(beta, pd.DataFrame):
        capital_asset_pricing_model = pd.DataFrame(
            columns=beta.columns, dtype=np.float64
        )
        for column in capital_asset_pricing_model.columns:
            capital_asset_pricing_model.loc[:, column] = risk_free_rate + beta[
                column
            ] * (benchmark_returns - risk_free_rate)
    elif isinstance(beta, (pd.Series | float)):
        capital_asset_pricing_model = risk_free_rate + beta * (
            benchmark_returns - risk_free_rate
        )
    else:
        raise TypeError(
            "beta should be a pd.Series, pd.DataFrame or float, "
            f"not {type(beta)}"
        )

    return capital_asset_pricing_model
```

## Creating Documentation

Besides styling and docstrings, documentation is important if you want to share your code with others. Assistants are good at drafting and updating it from your docstrings and examples, which removes the main reason documentation used to fall behind. Your job is to check that it describes what the model actually does. This is where [Sphinx](https://www.sphinx-doc.org/en/master/){: target="_blank"} comes in. Sphinx makes it easy to create well-structured, good-looking documentation for Python projects (or other documents consisting of multiple reStructuredText or Markdown files).

Other popular documentation generators include [MkDocs](https://www.mkdocs.org/){: target="_blank"}. Additionally, platforms like [Read the Docs](https://readthedocs.org/){: target="_blank"} can host documentation generated by these tools. The [Finance Toolkit documentation](/projects/financetoolkit/docs){: target="_blank"} is an example of what you can achieve with such tools (though it uses custom elements alongside standard tooling).

[![Alt text](/assets/images/modelling/build-your-model/image-2.png)](/projects/financetoolkit/docs){: target="_blank"}

Good documentation contains more than API references (descriptions of individual functions). It should also include tutorials, conceptual explanations, and practical examples, often using Jupyter Notebooks to demonstrate use cases. These examples help users understand the model's logic and applications. Store such examples in a dedicated `examples` directory, as suggested in [Structure your Model](/modelling/structure-your-model). See a snippet from the [Finance Toolkit's Getting Started Notebook](/projects/financetoolkit/getting-started){: target="_blank"} below:

[![Alt text](/assets/images/modelling/build-your-model/image.png)](/projects/financetoolkit/getting-started){: target="_blank"}

In corporate environments, internal wikis (like those in [Azure DevOps](https://learn.microsoft.com/en-us/azure/devops/project/wiki/wiki-create-repo?view=azure-devops&tabs=browser){: target="_blank"} or Confluence) are useful for sharing higher-level project information, architectural decisions, and team processes, often using Markdown and benefiting from version control.

Well-written docstrings allow the main documentation to focus on the model's overall structure, usage patterns, and concepts, rather than repeating low-level function details. This helps in particular when the model serves as a back-end, because it lets non-programmers (like Financial Analysts or Portfolio Managers) understand what the model can do and what it assumes.

## Reviewing AI-Written Code

Today's assistants write code that is usually correct and well structured. What deserves your attention are the choices behind it: in financial models, the decisions that change a result are rarely in the syntax and almost always in the finance or the data. Whether a function was written by you, a colleague or an assistant, these are the things I look at before accepting a change:

- **The formula.** Does it match the definition you intend to use? Many metrics have several accepted definitions (think of the many ways to calculate a P/E ratio), and an assistant will pick one without telling you.
- **Units and conventions.** Are percentages stored as fractions or as whole numbers? Are returns simple or logarithmic? Is a cost negative or positive in the data?
- **Periods and alignment.** Does the calculation mix annual and quarterly data, shift a series by the wrong lag, or annualise with the wrong factor (252 trading days versus 365 calendar days)?
- **Missing data.** What happens with a missing quarter, a division by zero or a company without a specific line item? Silent `NaN` values or forward-filled gaps can change the outcome without any error.
- **Hidden assumptions.** Look for hardcoded numbers, such as a risk-free rate or a tax rate, that should be inputs or named constants.
- **Fit with the model.** Is the code in the right layer, does it reuse existing helpers, and does it follow the conventions on this page?

Reviewing a change with these questions in mind takes a few minutes, and most of the time you will simply agree with the choices made. But you can only do that if you understand each of these topics, which is why the earlier pages focus on understanding rather than on rules.

After establishing these coding and documentation practices, the next step is testing. Proceed to [Test your Model](/modelling/test-your-model) to learn more.

[Test your Model](/modelling/test-your-model){: .btn .btn--info .btn--large .align-center}