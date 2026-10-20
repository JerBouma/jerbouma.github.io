---
title: "External Datasets"
seo_title: "External Datasets Guide | Finance Toolkit"
seo_title_suffix: false
excerpt: "How to run the Finance Toolkit's ratios, models, performance and risk metrics on financial statements from your own data source."
description: "Load financial statements from Yahoo Finance or any other source into the Finance Toolkit and calculate ratios, DuPont, beta and drawdowns in Python."
author_profile: false
permalink: /projects/financetoolkit/docs/getting-started/external-datasets
classes: wide-sidebar
layout: single
redirect_from:
  - /projects/financetoolkit/external-datasets
sidebar:
  nav: "financetoolkit-guides"
---

The Finance Toolkit doesn't have to fetch its own financial statements. You can hand it statements from any source, whether that is a data vendor's API, a CSV export from a terminal, your own database or a library such as `yfinance`, and every ratio, model, performance and risk metric works on them exactly as it does on the default data. That makes it possible to keep your existing data provider, to work with companies or periods your provider doesn't cover, or to check a calculation on statements you have adjusted yourself.

The only step in between is telling the Toolkit what each line item in your data is called. This guide walks through that with the income statements, balance sheets and cash flow statements of Tesla and Alphabet as reported on Yahoo Finance for the fiscal years 2021 to 2024.

## Reading the Statements

All files used in this guide, the statements of both companies and the filled-in normalisation files, are in the [external_datasets folder](https://github.com/JerBouma/FinanceToolkit/tree/main/examples/external_datasets){:target="_blank"} of the Finance Toolkit repository. Download that folder, or clone the repository, and run the code from the directory that contains it. The statements were collected with `yfinance`, which is a separate library and not part of the Finance Toolkit. Each file has the line items as rows and the fiscal years as columns. To read the six statements:

```python
import pandas as pd

from financetoolkit import Toolkit

# Balance Sheet Statements
tsla_balance = pd.read_csv("external_datasets/TSLA_balance.csv", index_col=0)
googl_balance = pd.read_csv("external_datasets/GOOGL_balance.csv", index_col=0)

# Income Statements
tsla_income = pd.read_csv("external_datasets/TSLA_income.csv", index_col=0)
googl_income = pd.read_csv("external_datasets/GOOGL_income.csv", index_col=0)

# Cash Flow Statements
tsla_cash = pd.read_csv("external_datasets/TSLA_cash.csv", index_col=0)
googl_cash = pd.read_csv("external_datasets/GOOGL_cash.csv", index_col=0)
```

The line items carry Yahoo Finance's own names, such as `TotalRevenue`, `CostOfRevenue` and `NetIncomeFromContinuingOperationNetMinorityInterest`, and the most recent year comes first.

## Filling the Normalisation Files

The Finance Toolkit maps every source onto one set of names through four normalisation files: `balance.csv`, `income.csv`, `cash.csv` and `statistics.csv`. To copy the default files to your Downloads folder (pass `path` to save them elsewhere):

```python
Toolkit("TSLA").get_normalization_files()
```

Each file has two columns. Column B holds the generic names the Finance Toolkit depends on, so never change those. Column A holds the names as they appear in your source: for every row, put the name of the matching line item from your data in column A. The `TotalRevenue` row of Yahoo Finance, for instance, goes next to `Revenue`. For the income statement, the first rows of the filled-in `income.csv` look like this:

| Income                          | Generic                                      |
|:--------------------------------|:---------------------------------------------|
| TotalRevenue                    | Revenue                                      |
| OperatingRevenue                | Operating Revenue                            |
| CostOfRevenue                   | Cost of Goods Sold                           |
| GrossProfit                     | Gross Profit                                 |
| OperatingExpense                | Operating Expenses                           |
| SellingGeneralAndAdministration | Selling, General and Administrative Expenses |
| ResearchAndDevelopment          | Research and Development Expenses            |
| OperatingIncome                 | Operating Income                             |
| PretaxIncome                    | Income Before Tax                            |
| TaxProvision                    | Income Tax Expense                           |
| NetIncome                       | Net Income                                   |
| EBITDA                          | EBITDA                                       |

The complete files for Yahoo Finance are in the same folder on GitHub, so for this data source you can use them as they are. A line item that has no counterpart in your data can stay empty; only the ratios that need it are skipped.

## Combining the Statements

The Toolkit expects one DataFrame per statement type for all companies together, with the ticker as the first level of the index. `combine_dataframes` builds that from a dictionary of ticker and statement. To combine the statements of both companies:

```python
from financetoolkit.utilities import dataframe_model

balance_sheets = dataframe_model.combine_dataframes(
    {"TSLA": tsla_balance, "GOOGL": googl_balance},
)
income_statements = dataframe_model.combine_dataframes(
    {"TSLA": tsla_income, "GOOGL": googl_income},
)
cash_flow_statements = dataframe_model.combine_dataframes(
    {"TSLA": tsla_cash, "GOOGL": googl_cash},
)
```

The result is three DataFrames with a row for every combination of ticker and line item and a column per fiscal year.

## Initialising the Toolkit with Your Own Data

The statements go into the `balance`, `income` and `cash` parameters, and `format_location` points to the folder with the filled-in normalisation files. The dates must run from left to right, oldest first, because growth rates and any ratio that uses an average of two years (such as asset turnover) shift the columns to find the previous year. Yahoo Finance puts the latest year first, which `reverse_dates=True` corrects. To initialise the Toolkit and show the normalised balance sheet:

```python
companies = Toolkit(
    tickers=["TSLA", "GOOGL"],
    balance=balance_sheets,
    income=income_statements,
    cash=cash_flow_statements,
    format_location="external_datasets",
    reverse_dates=True,  # Important when the dates are descending
)

companies.get_balance_sheet_statement()
```

Which returns the balance sheets with the generic names from the normalisation files, such as `Total Assets`, `Total Debt` and `Cash and Cash Equivalents`, and the years in order from 2021 to 2024.

## Ratios and Models

From here on, everything works as with the default data. The Extended DuPont Analysis splits the return on equity into five drivers: the interest burden, the tax burden, the operating margin, the asset turnover and the equity multiplier, which multiply into the ROE. To run it on the custom statements:

```python
companies.models.get_extended_dupont_analysis()
```

Which shows why the two companies moved in opposite directions: Tesla's return on equity fell from about 32% in 2022 to about 10% in 2024 as its operating margin dropped from 17% to 8% and its assets turned over more slowly, while Alphabet's rose from about 24% to 33% on a wider operating margin:

{% include ft-chart.html id="external-datasets-dupont" src="/assets/data/financetoolkit-guides/external-datasets.json" label="Extended DuPont Analysis of Tesla and Alphabet from Yahoo Finance statements" %}

The tax burden of Tesla above 1 in 2023 is not an error: that year its net income exceeded its pre-tax income because of a large one-off deferred tax benefit. The interest burden above 1 for both means net interest income added to earnings rather than costing them.

The ratio functions work the same way. To collect all efficiency ratios:

```python
companies.ratios.collect_efficiency_ratios()
```

Which gives the cost structure of a manufacturer next to that of a software and advertising business: Alphabet spends 12% of revenue on SG&A and 14% on R&D against about 5% for each at Tesla, while Tesla's operating costs absorb more than 90% of its revenue:

{% include ft-chart.html id="external-datasets-efficiency" src="/assets/data/financetoolkit-guides/external-datasets.json" label="Efficiency ratios of Tesla and Alphabet" %}

The working capital ratios from the same call show the other side of the business models. In days, for the latest year, they compare as follows:

{% include ft-chart.html id="external-datasets-days" src="/assets/data/financetoolkit-guides/external-datasets.json" label="Days of inventory, receivables and payables and the cash conversion cycle for Tesla and Alphabet" %}

Tesla collects from customers in about 15 days and pays its suppliers in about 61, which keeps its cash conversion cycle at around 12 days despite holding about two months of inventory. Alphabet carries hardly any inventory and reports none for 2023 and 2024, so its inventory days and cash conversion cycle are left empty for those years.

<div class="fs-callout" markdown="1"><p class="fs-callout__title">Missing line items</p>

When a ratio needs a line item that your data doesn't have, the Toolkit logs which one is missing and leaves that ratio out instead of failing. Yahoo Finance reports selling, general and administrative expenses as one figure, so the selling and marketing ratio and the general and administrative ratio are skipped here, with a message naming `Selling and Marketing Expenses` and `General and Administrative Expenses`.
</div>

The optional parameters work on custom data too. With `growth=True` any statement or ratio returns the change from the previous period instead of the level. To get the growth of every balance sheet item:

```python
companies.get_balance_sheet_statement(growth=True)
```

Which gives, for a selection of the items:

|                            |   2022 |   2023 |   2024 |
|:---------------------------|-------:|-------:|-------:|
| Tesla: Total Assets        |  32.5% |  29.5% |  14.5% |
| Tesla: Total Equity        |  45.3% |  38.6% |  15.8% |
| Tesla: Total Debt          | -35.2% |  66.5% |  42.3% |
| Alphabet: Total Assets     |   1.7% |  10.2% |  11.9% |
| Alphabet: Total Equity     |   1.8% |  10.6% |  14.7% |
| Alphabet: Total Debt       |   4.5% |  -8.6% |  -6.1% |

## Performance and Risk

Performance and risk metrics need prices rather than statements. Without an API key, the Toolkit collects the historical prices from Yahoo Finance, which covers about five years, and uses the S&P 500 (SPY) as the benchmark. To calculate the beta of both companies on monthly returns:

```python
companies.performance.get_beta(period="monthly")
```

Which shows Tesla's beta at around 2 for most of the period, twice the market's sensitivity, against about 1.3 for Alphabet:

{% include ft-chart.html id="external-datasets-beta" src="/assets/data/financetoolkit-guides/external-datasets.json" label="Monthly beta of Tesla and Alphabet against the S&P 500" %}

The maximum drawdown is the largest fall from a peak to a trough. With `within_period=True` it is calculated within each quarter from the daily prices. To calculate it for each quarter:

```python
companies.risk.get_maximum_drawdown(period="quarterly", within_period=True)
```

Which shows how much deeper Tesla's falls went, down 59% within the last quarter of 2022 and 48% in the first quarter of 2025, where the S&P 500 never lost more than 20% within a quarter:

{% include ft-chart.html id="external-datasets-drawdown" src="/assets/data/financetoolkit-guides/external-datasets.json" label="Maximum drawdown within each quarter for Tesla, Alphabet and the S&P 500" %}

The historical data itself, with open, high, low and close prices, volume, dividends and (cumulative) returns, is available as well. To get it and select the cumulative returns:

```python
historical_data = companies.get_historical_data()

historical_data["Cumulative Return"]
```

Which shows that Alphabet more than doubled over the five years, ahead of the S&P 500, while Tesla ended about 25% higher after a volatile ride:

{% include ft-chart.html id="external-datasets-returns" src="/assets/data/financetoolkit-guides/external-datasets.json" label="Cumulative return of Tesla, Alphabet and the S&P 500" %}

## Combining Your Data with an API Key

Custom statements and an API key can be used together: the Toolkit then uses your statements for every calculation based on them, and the API for everything else, such as analyst estimates, company profiles and longer price histories. To add the key and collect the analyst estimates:

```python
companies = Toolkit(
    tickers=["TSLA", "GOOGL"],
    balance=balance_sheets,
    income=income_statements,
    cash=cash_flow_statements,
    api_key="FINANCIAL_MODELING_PREP_KEY",
    format_location="external_datasets",
    reverse_dates=True,  # Important when the dates are descending
)

companies.get_analyst_estimates()
```

Which returns the low, high and average estimates for revenue, EBITDA, EBIT, net income, SG&A and EPS, together with the number of analysts, for past years and the years ahead. The average revenue and EPS estimates for both companies:

{% include ft-chart.html id="external-datasets-estimates" src="/assets/data/financetoolkit-guides/external-datasets.json" label="Average analyst estimates for revenue and EPS of Tesla and Alphabet" %}

<div class="fs-ref"><a href="/projects/financetoolkit/docs"><i class="fas fa-book" aria-hidden="true"></i>Full reference: Finance Toolkit</a></div>

{% include ft-charts-script.html %}
