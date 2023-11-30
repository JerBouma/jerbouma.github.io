---
title: Build your Model
excerpt: All of my talks, both personal and professional, are included here. This include presentations at a variety of universities and webinars.
description: All of my talks, both personal and professional, are included here. This include presentations at a variety of universities and webinars.
author_profile: true
permalink: /modelling/build-your-model
classes: wide-sidebar
author_profile: false
sidebar:
  nav: "modelling"
---

<script src="https://cdn.jsdelivr.net/npm/mermaid@10.6.0/dist/mermaid.min.js"></script>

A financial model can have multiple purposes. It can be as simple as the aggregation of data to a more complex model which includes forecasting and scenario analysis. In any case, the model should be built in such a way that it is easy to understand, maintain and extend. This is where the concept of modular programming comes in which is the approach as found in [Structure your Model](/modelling/structure-your-model). For more examples of this method and inspiration how to build your own model please have a look at the [Finance Toolkit](https://github.com/JerBouma/FinanceToolkit){: target="_blank"}, [Finance Database](https://github.com/JerBouma/FinanceDatabase){:, target="_blank"}, [OpenBB Terminal](https://github.com/OpenBB-finance/OpenBBTerminal){: target="_blank"}, [yfinance](https://github.com/ranaroussi/yfinance){: target="_blank"} and [Riskfolio-Lib](https://github.com/dcajasn/Riskfolio-Lib){: target="_blank"}.

<div class="mermaid">
flowchart LR;
classDef boxfont fill:#3b9cba,stroke-width:0px,color:white,radius:20px,font-weight:bold;
classDef currentfont fill:#d67f05,stroke-width:0px,color:white,radius:20px,font-weight:bold;

Step0[<a href="/modelling/introduction" style="color:white;text-decoration:none">Introduction</a>]:::boxfont --> Step1[<a href="/modelling/getting-started" style="color:white;text-decoration:none">Getting Started</a>]:::boxfont

Step1[<a href="/modelling/getting-started" style="color:white;text-decoration:none">Getting Started</a>] --> Step2[<a href="/modelling/setting-up-your-project" style="color:white;text-decoration:none">Setting up your Project</a>]:::boxfont

Step2[<a href="/modelling/setting-up-your-project" style="color:white;text-decoration:none">Setting up your Project</a>] -->  Step3[<a href="/modelling/structure-your-model" style="color:white;text-decoration:none">Structure your Model</a>]:::boxfont

Step3[<a href="/modelling/structure-your-model" style="color:white;text-decoration:none">Structure your Model</a>] --> Step4[<a href="/modelling/build-your-model" style="color:white;text-decoration:none">Build your Model</a>]:::currentfont

Step4[<a href="/modelling/build-your-model" style="color:white;text-decoration:none">Build your Model</a>] <--> Step5[<a href="/modelling/test-your-model" style="color:white;text-decoration:none">Test your Model</a>]:::boxfont
</div>

Whatever the purpose of your model is, the following styling and coding guidelines should be applied to take out the subjective nature of coding. Applying a style guide will ensure that all code is written in the same way and therefore is easier to read and maintain. This is especially important when working with multiple developers on the same codebase but also when colleagues move teams and need to understand new models. 

The linters, as discussed in [Setting up your Project](/modelling/setting-up-your-project#setting-up-linters), will do much of the initial styling of the code for you. However, the methods you use to code, how you choose to name your variables or what docstring structure you employ is not something linters will be able to help you with. This is where the Style Guide [**PEP8**](https://peps.python.org/pep-0008/){: target="_blank"} comes in.

{: .notice--info}
**Why a Universal Style is Important**<br>
It could be that you are used to a certain method of styling because that was employed within your firm or university. My honest advice is to detach from that and use the universal styling instead as it is adopted by countless of developers. Applying this style will make collaboration with your projects a lot easier since developers will be familiar with the way your code is written in an instant. Any questions whatsoever about the style, you have the full support of the Python Enhancement Proposals (PEP). Other than that, you'd otherwise also be fighting against the styling of the linters which will make your life a lot harder.

## Default Styling

Throughout this page, PEP is frequently referenced. PEP stands for Python Enhancement Proposal. A PEP is a technical design document for the Python community which describes a new feature for the language itself, its processes, or its environment. This is something developers have agreed on and therefore there is no point in reinventing the wheel for this matter.

The styles as described by **PEP8** (see [here](https://peps.python.org/pep-0008/){: target="_blank"}) are used for general code structures. This is the default style that is adopted by countless of developers. By applying this style, the style is the same for both internal and external tooling. It is recommended to browse through the PEP8 documentation to get a better understanding of each component. Within this section, the major components are summarised.

To summarise the code lay-out, this results in the following:

- [**Indentation**](https://peps.python.org/pep-0008/#indentation){: target="_blank"}: use 4 spaces as indentation level. This is the default in basically any code editor.
- [**Maximum line length**](https://peps.python.org/pep-0008/#maximum-line-length){: target="_blank"}: 79 is recommended but there is room to sway from this. PEP8 suggests up to 99 characters but 122 characters is often applied as well. The 79 characters was chosen due to the resolution size of the screens. This has since then greatly improved which loosens up this suggestion.
- [**Line Breaks**](https://peps.python.org/pep-0008/#should-a-line-break-before-or-after-a-binary-operator){: target="_blank"}: should follow the logic of mathematics in which the operator is in front of the variable and not behind it.
- [**Blank Lines**](https://peps.python.org/pep-0008/#blank-lines){: target="_blank"}: space out functionality accordingly, top-level functions with two blank lines and methods inside a class are surrounded by one blank line. Use blank lines within functions to separate logical sections.
- [**Source File Encoding**](https://peps.python.org/pep-0008/#source-file-encoding){: target="_blank"}: code should always use UTF-8. Next to that, code should be written in English except for specific abbreviations.
- [**Import statements**](https://peps.python.org/pep-0008/#imports){: target="_blank"}: are always written down separately and when a module is imported, this is specified explicitly. Thus it should not be `from package import *` but instead `from package import module, module2`.
- [**Model Level Dunder Names**](https://peps.python.org/pep-0008/#module-level-dunder-names){: target="_blank"}: any dunders (e.g. `__version__`) should be placed before the import statements (with the exception to the `__future__` import).

## Naming Conventions

Naming conventions for each type of variable is as follows:

- **Classes:** uses`CapWords` like `Ratios` or `RatiosClass`.
- **Functions:** uses lowercase with a verb like `get_gross_margin`.
- **Variables:** uses lowercase like `margin` or `gross_margin`.
- **Constants:** uses uppercase like `PERIOD`. These variables can <u>never</u> change.
- **Internal Variables:** uses an underscore at the start like `_income_statement`, this is meant for class-based systems to differentiate variables accordingly. Generally you won't use these variables outside of the class.

The goal with the naming convention is to make variables recognizable from the way they are written down. This makes it possible to understand the type of variable without needing to look for the variable declaration. By definition, I will know that `get_gross_margin` will execute a function whereas `gross_margin` and `PERIOD` will return data.

It is also important to make variables as descriptive as possible. For example, a variable should never be called `df` as it has little meaning. It is better to have a variable called `microsoft_trailing_gross_margin` than use `msft_ttm_gm` because *the time spend reading code is 10 times higher than the amount of time code is written.*

If you are working on a model together with other developers, don't forget that they should be able to understand your code as well when you are on a holiday, sick or have left the company.

## Applying Typing

All variables should contain typing on initialization. This means when you create a new variable, it should display exactly what type it could be. This is all defined in PEP 256 (see [here](https://peps.python.org/pep-0526/){: target="_blank"}) and PEP 484 (see [here](https://peps.python.org/pep-0484/){: target="_blank"}). For example:

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
# Single definition which shouldn't change
PERIOD: int = 5

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

This also applies to functions:

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

Not defining typing lowers the quality of the code as the user will need to read the docstring or code first before it is possible to understand what to supply.

## Writing Docstrings

Docstrings should follow PEP 257 (see [here](https://peps.python.org/pep-0257/){: target="_blank"}). This format is widely accepted by developers and used within many code editors as the default as well. An example of how a docstring could look like is as follows:

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

This is the Google format but there are other formats such as [reStructuredText](https://docutils.sourceforge.io/rst.html){: target="_blank"} as well. Which one you choose doesn't matter as long as the docstrings you write explain what the function does, what arguments it takes and what it returns. It needs to provide enough clarity that the user can understand the purpose of the function without having to read the code.

I recommended to be as extensive as possible and thus it is better to overdo it then to have a minimal docstring which still doesn't really explain what is going on. Docstrings give you the room as well to explain the financial theory or the logic of the function. See an example here of what it could look like (from [here](https://github.com/JerBouma/FinanceToolkit/blob/main/financetoolkit/performance/performance_model.py#L129-L174){: target="_blank"}) below. This is on purpose very extensive to show what is possible.

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

Besides styling and docstrings, documentation is actually pretty important if you want to share your code with others. This is where [Sphinx](https://www.sphinx-doc.org/en/master/){: target="_blank"} comes in. Sphinx is a tool that makes it easy to create intelligent and beautiful documentation for Python projects (or other documents consisting of multiple reStructuredText or Markdown files).

This is not the only approach to create documentation. There are other tools such as [MkDocs](https://www.mkdocs.org/){: target="_blank"} and [Read the Docs](https://readthedocs.org/){: target="_blank"} which are also widely used. See below the documentation of the [Finance Toolkit](/projects/financetoolkit/docs/){: target="_blank"} as an example. This uses custom JavaScript but the result is similar to that what you can achieve with Sphinx.

[![Alt text](/assets/images/modelling/build-your-model/image-2.png)](/projects/financetoolkit/docs/){: target="_blank"}

Documentation shouldn't just be about describing each individual function. It should also feature Jupyter Notebooks demonstrating use-cases. This helps in understanding the logic behind the model and for what it could be used. This should be saved in an "examples" folder as also shown in [Structure your Model](/modelling/structure-your-model). E.g. see below a snippet of the Getting Started Notebook from the [Finance Toolkit](/projects/financetoolkit/getting-started){: target="_blank"}.

[![Alt text](/assets/images/modelling/build-your-model/image.png)](/projects/financetoolkit/getting-started){: target="_blank"}

When working in a corporate setting, do not forget about the function of the [Wiki (e.g. from Azure DevOps)](https://learn.microsoft.com/en-us/azure/devops/project/wiki/wiki-create-repo?view=azure-devops&tabs=browser){: target="_blank"}. This is a great way to share information with your team and to document your code on a higher level while still being able to use Markdown and version control.

If you have designed proper docstrings, the documentation can be used to explain the overall structure of the model and how to use it instead of explaining each individual function. Especially when the model serves as the back-end, it can actually help Financial Analysts, Portfolio Managers and similar to understand what the model does without needing to understand any programming language. This is a great way to bridge the gap between the technical and non-technical professionals as well.

Once you have done these steps it's time to start testing your model. Visit [Test your Model](/modelling/test-your-model) to continue!

[Test your Model](/modelling/test-your-model){: .btn .btn--info .btn--large .align-center}