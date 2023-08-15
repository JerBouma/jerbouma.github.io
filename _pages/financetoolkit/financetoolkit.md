---
permalink: /projects/financetoolkit
title: Finance Toolkit
excerpt: This is an open-source toolkit in which all relevant financial ratios (50+), indicators and performance measurements are written down in the most simplistic way allowing for complete transparency of the calculation method. This allows you to not have to rely on metrics from other providers and, given a financial statement, allow for efficient manual calculations. This leads to one uniform method of calculation being applied that is available and understood by everyone.
description: This is an open-source toolkit in which all relevant financial ratios (50+), indicators and performance measurements are written down in the most simplistic way allowing for complete transparency of the calculation method. This allows you to not have to rely on metrics from other providers and, given a financial statement, allow for efficient manual calculations. This leads to one uniform method of calculation being applied that is available and understood by everyone.
classes: wide-sidebar
author_profile: false
redirect_from:
  - /financetoolkit
sidebar:
  nav: "financetoolkit"
---

While browsing a variety of websites, I kept finding that the same financial metric can greatly vary per source and so do the financial statements reported while little information is given how the metric was calculated.

For example, Microsoft's Price-to-Earnings (PE) ratio on the 6th of May, 2023 is reported to be 28.93 (Stockopedia), 32.05 (Morningstar), 32.66 (Macrotrends), 33.09 (Finance Charts), 33.66 (Y Charts), 33.67 (Wall Street Journal), 33.80 (Yahoo Finance) and 34.4 (Companies Market Cap). All of these calculations are correct, however the method applied varies leading to different results. Therefore, collecting data from multiple sources can lead to wrong interpretation of the results given that one source could be applying a different calculation method than another. And that is, if it is even freely available. Often the calculation is hidden behind a paid subscription.

**This is why I designed the FinanceToolkit**, this is an open-source toolkit in which all relevant financial ratios (50+), indicators and performance measurements are written down in the most simplistic way allowing for complete transparency of the calculation method. This allows you to not have to rely on metrics from other providers and, given a financial statement, allow for efficient manual calculations. This leads to one uniform method of calculation being applied that is available and understood by everyone.

The Finance Toolkit is complimented very well with the [Finance Database 🌎](/projects/financedatabase), a database that features 300.000+ symbols containing Equities, ETFs, Funds, Indices, Currencies, Cryptocurrencies and Money Markets. By utilising both, it is possible to do a fully-fledged competitive analysis with the tickers found from the FinanceDatabase inputted into the FinanceToolkit.

<p align="center">
    <img src="https://github.com/JerBouma/FinanceToolkit/blob/main/examples/Finance%20Toolkit%20-%206.%20Video%20Demo.gif?raw=true" alt="Finance Toolkit Illustration" width="100%" onerror="this.style.display = 'none'"/>
</p>

## Installation

To install the FinanceToolkit it simply requires the following:

```
pip install financetoolkit
````

Then within Python use:

```python
from financetoolkit import Toolkit
```
To be able to get started, you need to obtain an API Key from FinancialModelingPrep. This is used to gain access to 30+ years of financial statement both annually and quarterly. Note that the Free plan is limited to 250 requests each day, 5 years of data and only features companies listed on US exchanges.

___

<p><b><div align="center">Obtain an API Key from FinancialModelingPrep <a href="https://site.financialmodelingprep.com/developer/docs/pricing/jeroen/">here</a>.</div></b></p>
___

Through the link you are able to subscribe for the free plan and also premium plans at a **15% discount**. This is an affiliate link and thus supports the project at the same time I have chosen FinancialModelingPrep as a source as I find it to be the most transparent, reliable and at an affordable price. I have yet to find a platform offering such low prices for the amount of data offered. When you notice that the data is inaccurate or have any other issue related to the data, note that I simply provide the means to access this data and I am not responsible for the accuracy of the data itself. For this, use [their contact form](https://site.financialmodelingprep.com/contact) or provide the data yourself. 

## How-To Guides for the FinanceToolkit

This section contains a list of How-To guides for the Finance Toolkit. These guides are meant to show you how to use the Finance Toolkit and how to perform a financial analysis. The guides are written in the form of Jupyter Notebooks. You can view the notebooks by clicking on the button below the description.

<div class="row">
<div markdown="1" class="fifty-column-left mobile-max-column-width">

### Getting Started with the Finance Toolkit

The Finance Toolkit offers a comprehensive set of tools designed to empower users with in-depth insights into the world of finance. By demonstrating each functionality and its practical application. This notebook will show you how to get started with the Finance Toolkit.

[Open the Notebook](/projects/financetoolkit/getting-started){: .btn .btn--info}

</div>
<div markdown="1" class="fifty-column-right mobile-max-column-width">

### Visit the Code Documentation

Besides the practical examples, there exists a fully fledged documentation of the code. This documentation contains a description of each function, its parameters and an example. This allows you to quickly find the function you are looking for and understand how to use it.

[Visit the Code Documentation](/projects/financetoolkit/docs){: .btn .btn--warning}

</div>
</div>
<div markdown="1" class="fifty-column-left mobile-max-column-width">

### The Finance Database and the Finance Toolkit

This Notebooks demonstrates how to use the Finance Toolkit with the Finance Database to perform a complete financial analysis. Through the Finance Database you are able to find companies that are in the same country, sector and industry as the company you are analysing. This allows you to perform a complete competitive analysis with the help of the Finance Toolkit.

[Open the Notebook](/projects/financetoolkit/finance-database){: .btn .btn--info}

</div>

<div class="row">
<div markdown="1" class="fifty-column-right mobile-max-column-width">

### Defining Custom Ratios

The Finance Toolkit has an abundance of financial ratios, however it could be that you are looking for a specific ratio that is currently not provided. First and foremost, I encourage you to [create a Pull Request](https://github.com/JerBouma/FinanceToolkit/pulls) to add these ratios in but there is also an option to add custom ratios as follows. This feature was designed by [sword134](https://github.com/sword134).

[Open the Notebook](/projects/financetoolkit/custom-ratios){: .btn .btn--info}


</div>
</div>
<div markdown="1" class="fifty-column-left mobile-max-column-width">

### Calling Functions Directly

If you possess your own dataset or a particular use-case in mind, there might arise a need to directly call a specific function. This Notebook illustrates the process of accomplishing this.

[Open the Notebook](/projects/financetoolkit/functional-toolkit){: .btn .btn--info}

</div>

<div class="row">
<div markdown="1" class="fifty-column-right mobile-max-column-width">

### Using External Datasets

The Finance Toolkit has the ability to leverage custom datasets from any data provider as well. This makes it possible to work with your preferred data and not be limited to the data source the Finance Toolkit currently provides.

[Open the Notebook](/projects/financetoolkit/external-datasets){: .btn .btn--info}

</div>
</div>

## Using the Finance Toolkit

A basic example of how to initialise the Finance Toolkit is shown below, also see [this notebook](projects/financetoolkit/getting-started) for a detailed Getting Started guide as well as [this notebook](/projects/financetoolkit/finance-database) that includes the [Finance Database 🌎](/projects/financedatabase) and a proper financial analysis.

````python
from financetoolkit import Toolkit

companies = Toolkit(['AAPL', 'MSFT'], api_key="FMP_KEY", start_date='2017-12-31')

# an Enterprise example
enterprise = companies.get_enterprise()

# a Historical example
historical_data = companies.get_historical_data()

# a Financial Statement example
balance_sheet_statement = companies.get_balance_sheet_statement()

# a Ratios example
profitability_ratios = companies.ratios.collect_profitability_ratios()

# Show the profitability ratios for Apple
profitability_ratios.loc['AAPL']
````

This returns the following output for `profitability_ratios.loc['AAPL]`. Omitting `.loc['AAPL']` will return the result for both AAPL and MSFT.


|                                             |     2018 |     2019 |     2020 |     2021 |     2022 |
|:--------------------------------------------|---------:|---------:|---------:|---------:|---------:|
| Gross Margin                                | 0.383437 | 0.378178 | 0.382332 | 0.417794 | 0.433096 |
| Operating Margin                            | 0.26694  | 0.24572  | 0.241473 | 0.297824 | 0.302887 |
| Net Profit Margin                           | 0.224142 | 0.212381 | 0.209136 | 0.258818 | 0.253096 |
| Interest Burden Ratio                       | 1.02828  | 1.02827  | 1.01211  | 1.00237  | 0.997204 |
| Income Before Tax Profit Margin             | 0.274489 | 0.252666 | 0.244398 | 0.298529 | 0.30204  |
| Effective Tax Rate                          | 0.183422 | 0.159438 | 0.144282 | 0.133023 | 0.162045 |
| Return on Assets (ROA)                      | 0.162775 | 0.16323  | 0.177256 | 0.269742 | 0.282924 |
| Return on Equity (ROE)                      | 0.555601 | 0.610645 | 0.878664 | 1.50071  | 1.96959  |
| Return on Invested Capital (ROIC)           | 0.269858 | 0.293721 | 0.344126 | 0.503852 | 0.562645 |
| Return on Capital Employed (ROCE)           | 0.305968 | 0.297739 | 0.320207 | 0.495972 | 0.613937 |
| Return on Tangible Assets                   | 0.555601 | 0.610645 | 0.878664 | 1.50071  | 1.96959  |
| Income Quality Ratio                        | 1.30073  | 1.25581  | 1.4052   | 1.09884  | 1.22392  |
| Net Income per EBT                          | 0.816578 | 0.840562 | 0.855718 | 0.866977 | 0.837955 |
| Free Cash Flow to Operating Cash Flow Ratio | 0.828073 | 0.848756 | 0.909401 | 0.893452 | 0.912338 |
| EBT to EBIT Ratio                           | 0.957448 | 0.948408 | 0.958936 | 0.976353 | 0.975982 |
| EBIT to Revenue                             | 0.286688 | 0.26641  | 0.254864 | 0.305759 | 0.309473 |

## Working with Custom Ratios

The Finance Toolkit has an abundance of financial ratios, however it could be that you are looking for a specific ratio that is currently not provided. First and foremost, I encourage to [create a Pull Request](https://github.com/JerBouma/FinanceToolkit/pulls) to add these ratios in but there is also an option to add custom ratios as follows. This feature was designed by [sword134](https://github.com/sword134). Find a Notebook example [here](/projects/financetoolkit/custom-ratios).

Define how each custom ratio needs to be calculated. This follows the structure `Name of Ratio`: `Financial Statement Item * Financial Statement Item`. Note that you adhere to the normalization files naming. This can be viewed relatively easy by initializing the Toolkit and running for example `get_balance_sheet_statement`.

```python
custom_ratios = {
    'WC / Net Income': 'Working Capital / Net Income',
    'Net Income / Total Assets': 'Net Income / Total Assets',
    'Current Assets Inventory': 'Total Current Assets - Inventory',
    'Quick Ratio Current': 'Current Assets Inventory / Total Current Liabilities',
    'Quick Ratio Total': 'Current Assets Inventory / Total Liabilities'
}
```

Initializing the Finance Toolkit. Make sure to set the parameter `custom_ratios` with the above dictionary. Note that `quarterly=True` doesn't work without a Premium plan.

```python
from financetoolkit import Toolkit

# Initialize the Finance Toolkit
companies = Toolkit(
    ["AAPL", "MSFT", "GOOGL", "AMZN"], api_key=API_KEY, start_date="2022-08-10",
    custom_ratios=custom_ratios, quarterly=True
)
```

By then running `ratios.collect_custom_ratios` it automatically calculates the given ratios. Note the ratios 'Quick Ratio Current' and 'Quick Ratio Total' which rely on an earlier defined ratio ('Current Assets Inventory'). This is an example of how you can create a custom ratio based on another custom ratio.

Below you can find the custom ratios from GOOGL which has been selected with `.loc['GOOGL]`. The Notebook as found [here](/projects/financetoolkit/getting-started) shows the full output.

|                           |      2022Q3 |      2022Q4 |     2023Q1 |      2023Q2 |
|:--------------------------|------------:|------------:|-----------:|------------:|
| Current Assets Inventory  | 1.62953e+11 | 1.62125e+11 | 1.5967e+11 | 1.66557e+11 |
| Net Income / Total Assets | 0.0388271   | 0.037299    | 0.0407344  | 0.0479527   |
| Quick Ratio Current       | 2.46977     | 2.33947     | 2.31896    | 2.14334     |
| Quick Ratio Total         | 1.55744     | 1.48575     | 1.4703     | 1.43704     |
| WC / Net Income           | 7.19842     | 7.00932     | 6.1877     | 4.95857     |

## Accessing Functions Directly

It also possible to call any ratio or model directly as shown below. This allows access to 50+ ratios with custom data. Also see [this notebook](/projects/financetoolkit/functional-toolkit).

```python
import pandas as pd
import numpy as np

from financetoolkit.models import dupont

years = [2018, 2019, 2020, 2021, 2022]

dupont.get_dupont_analysis(
    net_income=pd.Series(
        [59531000000, 55256000000, 57411000000, 94680000000, 99803000000], index=years
    ),
    total_revenue=pd.Series(
        [265595000000, 260174000000, 274515000000, 365817000000, 394328000000],
        index=years,
    ),
    total_assets_begin=pd.Series(
        [np.nan, 365725000000, 338516000000, 323888000000, 351002000000],
        index=years,
    ),
    total_assets_end=pd.Series(
        [365725000000, 338516000000, 323888000000, 351002000000, 352755000000],
        index=years,
    ),
    total_equity_begin=pd.Series(
        [np.nan, 107147000000, 90488000000, 65339000000, 63090000000], index=years
    ),
    total_equity_end=pd.Series(
        [107147000000, 90488000000, 65339000000, 63090000000, 50672000000], index=years
    ),
)
```

This returns the following table which closely resembles a proper Dupont analysis for Apple at their given reporting dates in October:

|                   |       2018 |     2019 |     2020 |     2021 |     2022 |
|:------------------|-----------:|---------:|---------:|---------:|---------:|
| Net Profit Margin |   0.224142 | 0.212381 | 0.209136 | 0.258818 | 0.253096 |
| Asset Turnover    | nan        | 0.738878 | 0.828845 | 1.08408  | 1.12064  |
| Equity Multiplier | nan        | 3.56334  | 4.25089  | 5.25497  | 6.18622  |
| Return on Equity  | nan        | 0.559172 | 0.736856 | 1.47443  | 1.75459  |

## Working with other Datasets

The Finance Toolkit has the ability to leverage custom datasets from any data provider as well. This makes it possible to work with your preferred data and not be limited to the data source the Finance Toolkit currently provides. A detailed example can be found [here](/projects/financetoolkit/external-datasets) but to get started see the code below.

```python
from financetoolkit import Toolkit

# Initialize the Finance Toolkit
companies = Toolkit(['AAPL', 'MSFT'])

# Copy the normalization files
companies.get_normalization_files()
```
This copies over three files, `balance.csv`, `income.csv` and `cash.csv` which will contain a structure like the following:

![Normalization Format](https://github.com/JerBouma/FinanceToolkit/assets/46355364/ea4ebf87-1a27-4c40-a1fb-40d0eb0634bc)

By replacing the first column with the names from your dataset (e.g. replace `cashAndCashEquivalents` with `Cash` if this is how it is called in your dataset), it will automatically normalize the dataset when you initialize the Finance Toolkit. Note that the DataFrame needs to be a multi-index in case you use multiple tickers structured as `Ticker x Financial Statement Item x Periods`.

As an example:

![Dataset Example](https://github.com/JerBouma/FinanceToolkit/assets/46355364/fe0e3db0-3e88-41d2-a355-5f68110fdcf3)

If you have individual DataFrames for each company, you can do the following which will return the DataFrame structure that is required:

```python
from financetoolkit.base import helpers

balance_grouped = helpers.combine_dataframes({'AAPL': balance_apple, 'MSFT': balance_msft})
```

Once all of this is set-up you can feed this information to the Toolkit and use the Toolkit as normally.

```python

# Initialize the Toolkit
companies = Toolkit(
    tickers=['AAPL', 'MSFT'],
    balance=balance_grouped,
    income=income_grouped,
    cash=cash_grouped,
    format_location="FOLDER_PATH",
    reverse_dates=False) # Put this to True in case dates are descending

# Return all Ratios
companies.ratios.collect_all_ratios()
```

This will return all financial ratios that can be collected based on the provided data and the format.

![Output of Result](https://github.com/JerBouma/FinanceToolkit/assets/46355364/2a995430-b8d8-4236-892c-edb47042d6af)