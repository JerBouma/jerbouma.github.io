---
permalink: /projects/financetoolkit
title: Finance Toolkit
excerpt: This is an open-source toolkit in which 100+ financial ratios, indicators and performance measurements are written down in the most simplistic way allowing for complete transparency of the calculation method. This allows you to not have to rely on metrics from other providers and, given a financial statement, allow for efficient manual calculations. This leads to one uniform method of calculation being applied that is available and understood by everyone.
description: This is an open-source toolkit in which 100+ financial ratios, indicators and performance measurements are written down in the most simplistic way allowing for complete transparency of the calculation method. This allows you to not have to rely on metrics from other providers and, given a financial statement, allow for efficient manual calculations. This leads to one uniform method of calculation being applied that is available and understood by everyone.
classes: wide-sidebar
author_profile: false
redirect_from:
  - /financetoolkit
sidebar:
  nav: "financetoolkit"
---

While browsing a variety of websites, I kept finding that the same financial metric can greatly vary per source and so do the financial statements reported while little information is given how the metric was calculated.

For example, Microsoft's Price-to-Earnings (PE) ratio on the 6th of May, 2023 is reported to be 28.93 (Stockopedia), 32.05 (Morningstar), 32.66 (Macrotrends), 33.09 (Finance Charts), 33.66 (Y Charts), 33.67 (Wall Street Journal), 33.80 (Yahoo Finance) and 34.4 (Companies Market Cap). All of these calculations are correct, however the method applied varies leading to different results. Therefore, collecting data from multiple sources can lead to wrong interpretation of the results given that one source could be applying a different calculation method than another. And that is, if it is even freely available. Often the calculation is hidden behind a paid subscription.

**This is why I designed the FinanceToolkit**, this is an open-source toolkit in which all relevant financial ratios ([130+](#available-metrics)), indicators and performance measurements are written down in the most simplistic way allowing for complete transparency of the calculation method ([proof](https://github.com/JerBouma/FinanceToolkit/blob/main/financetoolkit/ratios/valuation.py)). This allows you to not have to rely on metrics from other providers and, given a financial statement, allow for efficient manual calculations. This leads to one uniform method of calculation being applied that is available and understood by everyone.

The Finance Toolkit not only supports Equities. Even for Currencies, Cryptocurrencies, ETFs, Mutual Funds, Indices, Money Markets, Commodities and more, the Finance Toolkit can be used to obtain historical data as well as important performance and risk measurements such as the Sharpe Ratio and Value at Risk.

The Finance Toolkit is complimented very well with the [Finance Database 🌎](https://github.com/JerBouma/FinanceDatabase), a database that features 300.000+ symbols containing Equities, ETFs, Funds, Indices, Currencies, Cryptocurrencies and Money Markets. By utilising both, it is possible to do a fully-fledged competitive analysis with the tickers found from the FinanceDatabase inputted into the FinanceToolkit.

<p align="center">
    <img src="https://github.com/JerBouma/FinanceToolkit/blob/main/examples/Finance%20Toolkit%20-%206.%20Video%20Demo.gif?raw=true" alt="Finance Toolkit Illustration" width="100%" onerror="this.style.display = 'none'"/>
</p>

# Installation

Before installation, consider starring the project on GitHub which helps others find the project as well. 

<a href="https://github.com/JerBouma/FinanceToolkit" target="_blank"><img width="1415" alt="image" src="https://github.com/JerBouma/FinanceToolkit/assets/46355364/014109fe-0c68-47d4-99bd-217c69dcea8d"></a>

To install the FinanceToolkit it simply requires the following:

```
pip install financetoolkit -U
````

Then within Python use:

```python
from financetoolkit import Toolkit

companies = Toolkit(
    tickers=['GOOGL', 'MSFT', 'AMZN'],
    api_key="FINANCIAL_MODELING_PREP_KEY",
)
```
To be able to get started, you need to obtain an API Key from FinancialModelingPrep. This is used to gain access to 30+ years of financial statement both annually and quarterly. Note that the Free plan is limited to 250 requests each day, 5 years of data and only features companies listed on US exchanges.

___ 

<div align="center"><b>Obtain an API Key from FinancialModelingPrep <a href="https://intelligence.financialmodelingprep.com/pricing-plans?couponCode=jeroen">here</a>.</b></div>
___

Through the link you are able to subscribe for the free plan and also premium plans at a **15% discount**. This is an affiliate link and thus supports the project at the same time. I have chosen FinancialModelingPrep as a source as I find it to be the most transparent, reliable and at an affordable price. I have yet to find a platform offering such low prices for the amount of data offered. When you notice that the data is inaccurate or have any other issue related to the data, note that I simply provide the means to access this data and I am not responsible for the accuracy of the data itself. For this, use [their contact form](https://site.financialmodelingprep.com/contact) or provide the data yourself. 

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

### Creating Custom Ratios

The Finance Toolkit has an abundance of financial ratios, however it could be that you are looking for a specific ratio that is currently not provided. First and foremost, I encourage you to [create a Pull Request](https://github.com/JerBouma/FinanceToolkit/pulls) to add these ratios in but there is also an option to add custom ratios as follows. This feature was designed by [sword134](https://github.com/sword134).

[Open the Notebook](/projects/financetoolkit/custom-ratios){: .btn .btn--info}


</div>
</div>
<div markdown="1" class="fifty-column-left mobile-max-column-width">

### Calling Functions Directly

If you possess your own financial statements data or have a different particular use-case in mind, it could be that you wish to directly use the functions in the FinanceToolkit. This Notebook illustrates the process of accomplishing this.

[Open the Notebook](/projects/financetoolkit/functional-toolkit){: .btn .btn--info}

</div>

<div class="row">
<div markdown="1" class="fifty-column-right mobile-max-column-width">

### Using External Datasets

The Finance Toolkit has the ability to leverage custom datasets from any data provider as well. This makes it possible to work with your preferred data and not be limited to the data source the Finance Toolkit currently provides. With this, it is possible to work with datasets from Yahoo Finance, OpenBB, Quandl, EODH, Bloomberg and much more.

[Open the Notebook](/projects/financetoolkit/external-datasets){: .btn .btn--info}

</div>
</div>

## Functionality

The Finance Toolkit features the following functionality, also see [Basic Usage](#basic-usage) to see some of these functions in action:

- **Company profiles** (`get_profile`), including country, sector, ISIN and general characteristics (from FinancialModelingPrep)
- **Company quotes** (`get_quote`), inclufding 52 week highs and lows, volume metrics and current shares outstanding (from FinancialModelingPrep)
- **Company ratings** (`get_rating`), based on key indicators like PE and DE ratios (from FinancialModelingPrep)
- **Historical market data** (`get_historical_data`), which can be retrieved on a daily, weekly, monthly, quarterly and yearly basis. This includes OHLC, dividends, returns, cumulative returns and volatility calculations for each corresponding period. (from FinancialModelingPrep or Yahoo Finance)
- **Treasury Rates** (`get_treasury_data`) for several months and several years over the last 3 months which allows yield curves to be constructed (from FinancialModelingPrep or Yahoo Finance)
- **Dividends Calendar** (`get_dividend_calendar`) which shows the (adjusted) dividend and the the related record, payment and declaration dates (from FinancialModelingPrep)
- **Analyst Estimates** (`get_analyst_estimates`) that show the expected EPS and Revenue from the past and future from a range of analysts (from FinancialModelingPrep)
- **Earnings Calendar**(`get_earnings_calendar`) which shows the exact dates earnings are released in the past and in the future including expectations (from FinancialModelingPrep)
- **Revenue Geographic Segmentation** (`get_revenue_geographic_segmentation`) which shows the revenue per company from each country and **Revenue Product Segmentation** (`get_revenue_product_segmenttion`) which shows the revenue per company from each product (from FinancialModelingPrep)
- **Balance Sheet Statements** (`get_balance_sheet_statement`), **Income Statements** (`get_income_statement`), **Cash Flow Statements** (`get_cash_flow_statement`) and **Statistics Statements** (`get_statistics_statement`), obtainable from FinancialModelingPrep or the source of your choosing through custom input. These functions are accompanied with a normalization function so that for any source, the same ratio analysis can be performed. Next to that, you can obtain growth and trailing (TTM) results as well. Please see [this Jupyter Notebook](https://www.jeroenbouma.com/projects/financetoolkit/external-datasets) that explains how to use a custom source.
- **Efficiency ratios** (`ratios.collect_efficiency_ratios`), **liquidity ratios** (`ratios.collect_liquidity_ratios`), **profitability ratios** (`ratios._collect_profitability_ratios`), **solvency ratios** (`ratios.collect_solvency_ratios`) and **valuation ratios** (`ratios.collect_valuation_ratios`) functionality that automatically calculates the most important ratios (50+) based on the inputted balance sheet, income and cash flow statements. Any of the underlying ratios can also be called individually such as `ratios.get_return_on_equity` and it is possible to calculate their growth with lags as well as calculate trailing metrics (TTM). Next to that, it is also possible to input your own **custom ratios** (`ratios.collect_custom_ratios`). See also [this Notebook](https://www.jeroenbouma.com/projects/financetoolkit/custom-ratios) for more information.
- **Models** like DUPONT analysis (`models.get_extended_dupont_analysis`) or Enterprise Breakdown (`models.get_enterprise_value_breakdown`) that can be used to perform in-depth financial analysis through a single function. These functions combine much of the functionality throughout the Toolkit to provide advanced calculations. 
- **Performance metrics** like Jensens Alpha (`performance.get_jensens_alpha`),  Capital Asset Pricing Model (CAPM) (`performance.get_capital_asset_pricing_model`) and (Rolling) Sharpe Ratio (`performance.get_sharpe_ratio`) that can be used to understand how each company is performing versus the benchmark and compared to each other.
- **Risk metrics** like Value at Risk (`risk.get_value_at_risk`) and Conditional Value at Risk (`risk.get_conditional_value_at_risk`) that can be used to understand the risk profile of each company and how it compares to the benchmark.
- **Technical indicators** like Relative Strength Index (`technicals.get_relative_strength_index`),  Exponential Moving Average (`technicals.get_exponential_moving_average`) and Bollinger Bands (`technicals.get_bollinger_bands`) that can be used to perform in-depth momentum and trend analysis. These functions allow for the calculation of technical indicators based on the historical market data.

The dependencies of the package are on purpose *very slim* so that it will work well with any combination of packages and not result in conflicts.

## Basic Usage

This section is an introduction to the Finance Toolkit. Also see [this notebook](https://www.jeroenbouma.com/projects/financetoolkit/getting-started) for a detailed Getting Started guide as well as [this notebook](https://www.jeroenbouma.com/projects/financetoolkit/finance-database) that includes the [Finance Database 🌎](https://www.jeroenbouma.com/projects/financedatabase) and a proper financial analysis. Next to that, find below a fully-fledged code documentation as well as Jupyter Notebooks in which you can see many examples ranging from basic examples to creating custom ratios to working with your own datasets.

A basic example of how to use the Finance Toolkit is shown below.

````python
from financetoolkit import Toolkit

companies = Toolkit(['AAPL', 'MSFT'], api_key="FINANCIAL_MODELING_PREP_KEY", start_date='2017-12-31')

# a Historical example
historical_data = companies.get_historical_data()

# a Financial Statement example
balance_sheet_statement = companies.get_balance_sheet_statement()

# a Ratios example
profitability_ratios = companies.ratios.collect_profitability_ratios()

# a Models example
extended_dupont_analysis = companies.models.get_extended_dupont_analysis()

# a Performance example
capital_asset_pricing_model = companies.performance.get_capital_asset_pricing_model(show_full_results=True)

# a Risk example
value_at_risk = companies.risk.get_value_at_risk(period='quarterly')

# a Technical example
bollinger_bands = companies.technicals.get_bollinger_bands()
````

Generally, the functions return a DataFrame with a multi-index in which all tickers, in this case Apple and Microsoft, are presented. To keep things manageable for this README, I've selected just Apple but in essence it can be any list of tickers (no limit). The filtering is done through using `.loc['AAPL']` and `.xs('AAPL', level=1, axis=1)` based on whether it's fundamental data or historical data respectively.

### Obtaining Historical Data

Obtain historical data on a daily, weekly, monthly or yearly basis. This includes OHLC, volumes, dividends, returns, cumulative returns and volatility calculations for each corresponding period.

| Date       |    Open |    High |     Low |   Close |   Adj Close |      Volume |   Dividends |       Return |   Volatility |   Excess Return |   Excess Volatility |   Cumulative Return |
|:-----------|--------:|--------:|--------:|--------:|------------:|------------:|------------:|-------------:|-------------:|----------------:|--------------------:|--------------------:|
| 2018-01-02 | 42.54   | 43.075  | 42.315  | 43.065  |     40.7765 | 1.02224e+08 |           0 |  0           |    0.0203524 |     -0.00674528 |           0.0231223 |            1        |
| 2018-01-03 | 43.1325 | 43.6375 | 42.99   | 43.0575 |     40.7694 | 1.18072e+08 |           0 | -0.000173997 |    0.0203524 |     -0.024644   |           0.0231223 |            0.999826 |
| 2018-01-04 | 43.135  | 43.3675 | 43.02   | 43.2575 |     40.9588 | 8.97384e+07 |           0 |  0.00464441  |    0.0203524 |     -0.0198856  |           0.0231223 |            1.00447  |
| 2018-01-05 | 43.36   | 43.8425 | 43.2625 | 43.75   |     41.4251 | 9.464e+07   |           0 |  0.0113856   |    0.0203524 |     -0.0133744  |           0.0231223 |            1.01591  |
| 2018-01-08 | 43.5875 | 43.9025 | 43.4825 | 43.5875 |     41.2713 | 8.22712e+07 |           0 | -0.00371412  |    0.0203524 |     -0.0285141  |           0.0231223 |            1.01213  |

### Obtaining Financial Statements

Obtain a Balance Sheet Statement on an annual or quarterly basis. This can also be an income statement (`companies.get_income_statement()`) or cash flow statement (`companies.get_cash_flow_statement()`).

|                                          |         2018 |         2019 |         2020 |        2021 |         2022 |
|:-----------------------------------------|-------------:|-------------:|-------------:|------------:|-------------:|
| Cash and Cash Equivalents                |  2.5913e+10  |  4.8844e+10  |  3.8016e+10  | 3.494e+10   |  2.3646e+10  |
| Short Term Investments                   |  4.0388e+10  |  5.1713e+10  |  5.2927e+10  | 2.7699e+10  |  2.4658e+10  |
| Cash and Short Term Investments          |  6.6301e+10  |  1.00557e+11 |  9.0943e+10  | 6.2639e+10  |  4.8304e+10  |
| Accounts Receivable                      |  4.8995e+10  |  4.5804e+10  |  3.7445e+10  | 5.1506e+10  |  6.0932e+10  |
| Inventory                                |  3.956e+09   |  4.106e+09   |  4.061e+09   | 6.58e+09    |  4.946e+09   |
| Other Current Assets                     |  1.2087e+10  |  1.2352e+10  |  1.1264e+10  | 1.4111e+10  |  2.1223e+10  |
| Total Current Assets                     |  1.31339e+11 |  1.62819e+11 |  1.43713e+11 | 1.34836e+11 |  1.35405e+11 |
| Property, Plant and Equipment            |  4.1304e+10  |  3.7378e+10  |  3.6766e+10  | 3.944e+10   |  4.2117e+10  |
| Goodwill                                 |  0           |  0           |  0           | 0           |  0           |
| Intangible Assets                        |  0           |  0           |  0           | 0           |  0           |
| Long Term Investments                    |  1.70799e+11 |  1.05341e+11 |  1.00887e+11 | 1.27877e+11 |  1.20805e+11 |
| Tax Assets                               |  0           |  0           |  0           | 0           |  0           |
| Other Fixed Assets                       |  2.2283e+10  |  3.2978e+10  |  4.2522e+10  | 4.8849e+10  |  5.4428e+10  |
| Fixed Assets                             |  2.34386e+11 |  1.75697e+11 |  1.80175e+11 | 2.16166e+11 |  2.1735e+11  |
| Other Assets                             |  0           |  0           |  0           | 0           |  0           |
| Total Assets                             |  3.65725e+11 |  3.38516e+11 |  3.23888e+11 | 3.51002e+11 |  3.52755e+11 |
| Accounts Payable                         |  5.5888e+10  |  4.6236e+10  |  4.2296e+10  | 5.4763e+10  |  6.4115e+10  |
| Short Term Debt                          |  2.0748e+10  |  1.624e+10   |  1.3769e+10  | 1.5613e+10  |  2.111e+10   |
| Tax Payables                             |  0           |  0           |  0           | 0           |  0           |
| Deferred Revenue                         |  7.543e+09   |  5.522e+09   |  6.643e+09   | 7.612e+09   |  7.912e+09   |
| Other Current Liabilities                |  3.2687e+10  |  3.772e+10   |  4.2684e+10  | 4.7493e+10  |  6.0845e+10  |
| Total Current Liabilities                |  1.16866e+11 |  1.05718e+11 |  1.05392e+11 | 1.25481e+11 |  1.53982e+11 |
| Long Term Debt                           |  9.3735e+10  |  9.1807e+10  |  9.8667e+10  | 1.09106e+11 |  9.8959e+10  |
| Deferred Revenue Non Current             |  2.797e+09   |  0           |  0           | 0           |  0           |
| Deferred Tax Liabilities                 |  4.26e+08    |  0           |  0           | 0           |  0           |
| Other Non Current Liabilities            |  4.4754e+10  |  5.0503e+10  |  5.449e+10   | 5.3325e+10  |  4.9142e+10  |
| Total Non Current Liabilities            |  1.41712e+11 |  1.4231e+11  |  1.53157e+11 | 1.62431e+11 |  1.48101e+11 |
| Other Liabilities                        |  0           |  0           |  0           | 0           |  0           |
| Capital Lease Obligations                |  0           |  0           |  0           | 0           |  0           |
| Total Liabilities                        |  2.58578e+11 |  2.48028e+11 |  2.58549e+11 | 2.87912e+11 |  3.02083e+11 |
| Preferred Stock                          |  0           |  0           |  0           | 0           |  0           |
| Common Stock                             |  4.0201e+10  |  4.5174e+10  |  5.0779e+10  | 5.7365e+10  |  6.4849e+10  |
| Retained Earnings                        |  7.04e+10    |  4.5898e+10  |  1.4966e+10  | 5.562e+09   | -3.068e+09   |
| Accumulated Other Comprehensive Income   | -3.454e+09   | -5.84e+08    | -4.06e+08    | 1.63e+08    | -1.1109e+10  |
| Other Total Shareholder Equity           |  0           |  0           |  0           | 0           |  0           |
| Total Shareholder Equity                 |  1.07147e+11 |  9.0488e+10  |  6.5339e+10  | 6.309e+10   |  5.0672e+10  |
| Total Equity                             |  1.07147e+11 |  9.0488e+10  |  6.5339e+10  | 6.309e+10   |  5.0672e+10  |
| Total Liabilities and Shareholder Equity |  3.65725e+11 |  3.38516e+11 |  3.23888e+11 | 3.51002e+11 |  3.52755e+11 |
| Minority Interest                        |  0           |  0           |  0           | 0           |  0           |
| Total Liabilities and Equity             |  3.65725e+11 |  3.38516e+11 |  3.23888e+11 | 3.51002e+11 |  3.52755e+11 |
| Total Investments                        |  2.11187e+11 |  1.57054e+11 |  1.53814e+11 | 1.55576e+11 |  1.45463e+11 |
| Total Debt                               |  1.14483e+11 |  1.08047e+11 |  1.12436e+11 | 1.24719e+11 |  1.20069e+11 |
| Net Debt                                 |  8.857e+10   |  5.9203e+10  |  7.442e+10   | 8.9779e+10  |  9.6423e+10  |

### Obtaining Financial Ratios

Get Profitability Ratios based on the inputted balance sheet, income and cash flow statements. This can be any of the 50+ ratios within the `ratios` module. The `get_` functions show a single ratio whereas the `collect_` functions show an aggregation of multiple ratios.

|                                             |     2018 |    2019 |    2020 |    2021 |    2022 |
|:--------------------------------------------|---------:|--------:|--------:|--------:|--------:|
| Gross Margin                                |   0.3834 |  0.3782 |  0.3823 |  0.4178 |  0.4331 |
| Operating Margin                            |   0.2669 |  0.2457 |  0.2415 |  0.2978 |  0.3029 |
| Net Profit Margin                           |   0.2241 |  0.2124 |  0.2091 |  0.2588 |  0.2531 |
| Interest Coverage Ratio                     |  25.2472 | 21.3862 | 26.921  | 45.4567 | 44.538  |
| Income Before Tax Profit Margin             |   0.2745 |  0.2527 |  0.2444 |  0.2985 |  0.302  |
| Effective Tax Rate                          |   0.1834 |  0.1594 |  0.1443 |  0.133  |  0.162  |
| Return on Assets (ROA)                      |   0.1628 |  0.1632 |  0.1773 |  0.2697 |  0.2829 |
| Return on Equity (ROE)                      | nan      |  0.5592 |  0.7369 |  1.4744 |  1.7546 |
| Return on Invested Capital (ROIC)           |   0.2699 |  0.2937 |  0.3441 |  0.5039 |  0.5627 |
| Return on Capital Employed (ROCE)           |   0.306  |  0.2977 |  0.3202 |  0.496  |  0.6139 |
| Return on Tangible Assets                   |   0.5556 |  0.6106 |  0.8787 |  1.5007 |  1.9696 |
| Income Quality Ratio                        |   1.3007 |  1.2558 |  1.4052 |  1.0988 |  1.2239 |
| Net Income per EBT                          |   0.8166 |  0.8406 |  0.8557 |  0.867  |  0.838  |
| Free Cash Flow to Operating Cash Flow Ratio |   0.8281 |  0.8488 |  0.9094 |  0.8935 |  0.9123 |
| EBT to EBIT Ratio                           |   0.9574 |  0.9484 |  0.9589 |  0.9764 |  0.976  |
| EBIT to Revenue                             |   0.2867 |  0.2664 |  0.2549 |  0.3058 |  0.3095 |

### Obtaining Financial Models

Get an Extended DuPont Analysis based on the inputted balance sheet, income and cash flow statements. This can also be for example an Enterprise Value Breakdown (`companies.models.get_enterprise_value_breakdown()`).

|                         |     2017 |   2018 |   2019 |   2020 |   2021 |   2022 |
|:------------------------|---------:|-------:|-------:|-------:|-------:|-------:|
| Interest Burden Ratio   |   0.9572 | 0.9725 | 0.9725 | 0.988  | 0.9976 | 1.0028 |
| Tax Burden Ratio        |   0.7882 | 0.8397 | 0.8643 | 0.8661 | 0.869  | 0.8356 |
| Operating Profit Margin |   0.2796 | 0.2745 | 0.2527 | 0.2444 | 0.2985 | 0.302  |
| Asset Turnover          | nan      | 0.7168 | 0.7389 | 0.8288 | 1.0841 | 1.1206 |
| Equity Multiplier       | nan      | 3.0724 | 3.5633 | 4.2509 | 5.255  | 6.1862 |
| Return on Equity        | nan      | 0.4936 | 0.5592 | 0.7369 | 1.4744 | 1.7546 |

### Obtaining Performance Metrics

Get the Expected Return as defined by the Capital Asset Pricing Model. Here with the `show_full_results=True` parameter not only the expected return is found but also the Betas. The beauty of this is that it can be based on any period as the function also accepts the period 'weekly', 'monthly', 'quarterly' and 'yearly' (as shown below).


| Date   |   Risk Free Rate |   Beta AAPL |   Beta MSFT |   Benchmark Returns |   CAPM AAPL |   CAPM MSFT |
|:-------|-----------------:|------------:|------------:|--------------------:|------------:|------------:|
| 2017   |           0.024  |     1.36406 |     1.29979 |           0.1942    |      0.2562 |    0.245223 |
| 2018   |           0.0269 |     1.25651 |     1.44686 |          -0.0623726 |     -0.0853 |   -0.102265 |
| 2019   |           0.0192 |     1.5572  |     1.2942  |           0.288781  |      0.439  |    0.36809  |
| 2020   |           0.0092 |     1.12329 |     1.1204  |           0.162589  |      0.1815 |    0.181058 |
| 2021   |           0.0151 |     1.3144  |     1.1523  |           0.268927  |      0.3487 |    0.307586 |
| 2022   |           0.0388 |     1.30786 |     1.2829  |          -0.194428  |     -0.2662 |   -0.260409 |
| 2023   |           0.0427 |     1.20463 |     1.2727  |           0.157231  |      0.1807 |    0.188465 |

### Obtaining Risk Metrics

Get the Value at Risk for each quarter. Here, the days within each quarter are considered for the Value at Risk. This makes it so that you can understand within each period what is the expected Value at Risk (VaR) which can again be any period but also based on distributions such as Historical, Gaussian, Student-t, Cornish-Fisher.

|        |    AAPL |    MSFT |   Benchmark |
|:-------|--------:|--------:|------------:|
| 2017Q1 | -0.0042 | -0.0098 |     -0.0036 |
| 2017Q2 | -0.0147 | -0.0182 |     -0.0068 |
| 2017Q3 | -0.0171 | -0.0119 |     -0.0071 |
| 2017Q4 | -0.0149 | -0.0084 |     -0.0041 |
| 2018Q1 | -0.025  | -0.0291 |     -0.0212 |
| 2018Q2 | -0.016  | -0.0228 |     -0.0131 |
| 2018Q3 | -0.0163 | -0.0135 |     -0.0065 |
| 2018Q4 | -0.0461 | -0.0394 |     -0.0267 |
| 2019Q1 | -0.0189 | -0.0195 |     -0.0094 |
| 2019Q2 | -0.0204 | -0.0208 |     -0.0117 |
| 2019Q3 | -0.0216 | -0.0268 |     -0.0121 |
| 2019Q4 | -0.0137 | -0.0138 |     -0.0083 |
| 2020Q1 | -0.0653 | -0.0668 |     -0.0517 |
| 2020Q2 | -0.0297 | -0.0257 |     -0.0278 |
| 2020Q3 | -0.0406 | -0.0326 |     -0.0168 |
| 2020Q4 | -0.0296 | -0.0279 |     -0.0137 |
| 2021Q1 | -0.0348 | -0.0267 |     -0.0148 |
| 2021Q2 | -0.0176 | -0.0159 |     -0.0092 |
| 2021Q3 | -0.0234 | -0.0167 |     -0.0117 |
| 2021Q4 | -0.0204 | -0.0206 |     -0.0118 |
| 2022Q1 | -0.0258 | -0.0374 |     -0.0194 |
| 2022Q2 | -0.0396 | -0.0424 |     -0.0355 |
| 2022Q3 | -0.029  | -0.029  |     -0.0205 |
| 2022Q4 | -0.0364 | -0.0314 |     -0.0234 |
| 2023Q1 | -0.018  | -0.0257 |     -0.0156 |
| 2023Q2 | -0.01   | -0.0191 |     -0.0076 |
| 2023Q3 | -0.0314 | -0.0226 |     -0.0105 |

### Obtaining Technical Indicators

Get Bollinger Bands based on the historical market data. This can be any of the 30+ technical indicators within the `technicals` module. The `get_` functions show a single indicator whereas the `collect_` functions show an aggregation of multiple indicators.

| Date       |   Lower Band |   Middle Band |   Upper Band |
|:-----------|-------------:|--------------:|-------------:|
| 2023-08-22 |      170.336 |       178.524 |      186.712 |
| 2023-08-23 |      173.376 |       177.824 |      182.272 |
| 2023-08-24 |      173.56  |       177.441 |      181.322 |
| 2023-08-25 |      173.56  |       177.441 |      181.323 |
| 2023-08-28 |      173.486 |       177.486 |      181.487 |