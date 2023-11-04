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

<div align="center"><b>Obtain an API Key from FinancialModelingPrep <a href="https://www.jeroenbouma.com/fmp">here</a>.</b></div>
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

companies = Toolkit(["AAPL", "MSFT"], api_key=API_KEY, start_date="2017-12-31")

# a Historical example
historical_data = companies.get_historical_data()

# a Financial Statement example
income_statement = companies.get_income_statement()

# a Ratios example
profitability_ratios = companies.ratios.collect_profitability_ratios()

# a Models example
extended_dupont_analysis = companies.models.get_extended_dupont_analysis()

# a Performance example
factor_asset_correlations = companies.performance.get_factor_asset_correlations(period='quarterly')

# a Risk example
value_at_risk = companies.risk.get_value_at_risk(period="weekly")

# a Technical example
ichimoku_cloud = companies.technicals.get_ichimoku_cloud()
````

Generally, the functions return a DataFrame with a multi-index in which all tickers, in this case Apple and Microsoft, are presented. To keep things manageable for this README, I've selected just Apple but in essence it can be any list of tickers (no limit). The filtering is done through using `.loc['AAPL']` and `.xs('AAPL', level=1, axis=1)` based on whether it's fundamental data or historical data respectively.

### Obtaining Historical Data

Obtain historical data on a daily, weekly, monthly or yearly basis. This includes OHLC, volumes, dividends, returns, cumulative returns and volatility calculations for each corresponding period. For example, the historical data for Apple is shown below.

| date       |    Open |    High |     Low |   Close |   Adj Close |      Volume |   Dividends |   Return |   Volatility |   Excess Return |   Excess Volatility |   Cumulative Return |
|:-----------|--------:|--------:|--------:|--------:|------------:|------------:|------------:|---------:|-------------:|----------------:|--------------------:|--------------------:|
| 2018-01-02 | 42.54   | 43.075  | 42.315  | 43.065  |       40.78 | 1.02224e+08 |           0 |   0      |       0.0202 |         -0.0067 |              0.0233 |              1      |
| 2018-01-03 | 43.1325 | 43.6375 | 42.99   | 43.0575 |       40.77 | 1.17982e+08 |           0 |  -0.0002 |       0.0202 |         -0.0247 |              0.0233 |              0.9998 |
| 2018-01-04 | 43.135  | 43.3675 | 43.02   | 43.2575 |       40.96 | 8.97384e+07 |           0 |   0.0047 |       0.0202 |         -0.0198 |              0.0233 |              1.0044 |
| 2018-01-05 | 43.36   | 43.8425 | 43.2625 | 43.75   |       41.43 | 9.46401e+07 |           0 |   0.0115 |       0.0202 |         -0.0133 |              0.0233 |              1.0159 |
| 2018-01-08 | 43.5875 | 43.9025 | 43.4825 | 43.5875 |       41.27 | 8.22711e+07 |           0 |  -0.0039 |       0.0202 |         -0.0287 |              0.0233 |              1.012  |

And below the cumulative returns are plotted which include the S&P 500 as benchmark:

![HistoricalData](https://github.com/JerBouma/FinanceToolkit/assets/46355364/cd7b5029-0e66-4592-9822-42b652e7deed)


### Obtaining Financial Statements

Obtain an Income Statement on an annual or quarterly basis. This can also be an income statement (`companies.get_income_statement()`) or cash flow statement (`companies.get_cash_flow_statement()`). For example, the first 5 rows of the Income Statement for Apple are shown below.

|                                   |        2017 |        2018 |        2019 |        2020 |        2021 |        2022 |        2023 |
|:----------------------------------|------------:|------------:|------------:|------------:|------------:|------------:|------------:|
| Revenue                           | 2.29234e+11 | 2.65595e+11 | 2.60174e+11 | 2.74515e+11 | 3.65817e+11 | 3.94328e+11 | 3.83285e+11 |
| Cost of Goods Sold                | 1.41048e+11 | 1.63756e+11 | 1.61782e+11 | 1.69559e+11 | 2.12981e+11 | 2.23546e+11 | 2.14137e+11 |
| Gross Profit                      | 8.8186e+10  | 1.01839e+11 | 9.8392e+10  | 1.04956e+11 | 1.52836e+11 | 1.70782e+11 | 1.69148e+11 |
| Gross Profit Ratio                | 0.3847      | 0.3834      | 0.3782      | 0.3823      | 0.4178      | 0.4331      | 0.4413      |
| Research and Development Expenses | 1.1581e+10  | 1.4236e+10  | 1.6217e+10  | 1.8752e+10  | 2.1914e+10  | 2.6251e+10  | 2.9915e+10  |

And below the Earnings Before Interest, Taxes, Depreciation and Amortization (EBITDA) are plotted for both Apple and Microsoft.

![FinancialStatements](https://github.com/JerBouma/FinanceToolkit/assets/46355364/a4ba0629-0832-4dc0-a5c1-9cf2c9bd13ce)

### Obtaining Financial Ratios

Get Profitability Ratios based on the inputted balance sheet, income and cash flow statements. This can be any of the 50+ ratios within the `ratios` module. The `get_` functions show a single ratio whereas the `collect_` functions show an aggregation of multiple ratios. For example, see some of the profitability ratios of Microsoft below.

|                                 |    2017 |    2018 |    2019 |    2020 |    2021 |    2022 |    2023 |
|:--------------------------------|--------:|--------:|--------:|--------:|--------:|--------:|--------:|
| Gross Margin                    |  0.6191 |  0.6525 |  0.659  |  0.6778 |  0.6893 |  0.684  |  0.6892 |
| Operating Margin                |  0.2482 |  0.3177 |  0.3414 |  0.3703 |  0.4159 |  0.4206 |  0.4177 |
| Net Profit Margin               |  0.2357 |  0.1502 |  0.3118 |  0.3096 |  0.3645 |  0.3669 |  0.3415 |
| Interest Coverage Ratio         | 13.9982 | 16.5821 | 20.3429 | 25.3782 | 34.7835 | 47.4275 | 52.0244 |
| Income Before Tax Profit Margin |  0.2574 |  0.3305 |  0.3472 |  0.3708 |  0.423  |  0.4222 |  0.4214 |

And below a few of the profitability ratios are plotted for Microsoft.

![FinancialRatios](https://github.com/JerBouma/FinanceToolkit/assets/46355364/93221f7a-face-4035-87c7-e43815e89eb4)

### Obtaining Financial Models

Get an Extended DuPont Analysis based on the inputted balance sheet, income and cash flow statements. This can also be an Enterprise Value Breakdown, Weighted Average Cost of Capital (WACC), Altman Z-Score and many more models. For example, this shows the Extended DuPont Analysis for Apple:

|                         |     2017 |   2018 |   2019 |   2020 |   2021 |   2022 |   2023 |
|:------------------------|---------:|-------:|-------:|-------:|-------:|-------:|-------:|
| Interest Burden Ratio   |   0.9572 | 0.9725 | 0.9725 | 0.988  | 0.9976 | 1.0028 | 1.005  |
| Tax Burden Ratio        |   0.7882 | 0.8397 | 0.8643 | 0.8661 | 0.869  | 0.8356 | 0.8486 |
| Operating Profit Margin |   0.2796 | 0.2745 | 0.2527 | 0.2444 | 0.2985 | 0.302  | 0.2967 |
| Asset Turnover          | nan      | 0.7168 | 0.7389 | 0.8288 | 1.0841 | 1.1206 | 1.0868 |
| Equity Multiplier       | nan      | 3.0724 | 3.5633 | 4.2509 | 5.255  | 6.1862 | 6.252  |
| Return on Equity        | nan      | 0.4936 | 0.5592 | 0.7369 | 1.4744 | 1.7546 | 1.7195 |

And below each component of the Extended Dupont Analysis is plotted including the resulting Return on Equity (ROE).

![Models](https://github.com/JerBouma/FinanceToolkit/assets/46355364/f5e1cab3-d1bd-455d-a4ba-92e1348163be)

### Obtaining Performance Metrics

Get the correlations with the factors as defined by Fama-and-French. These include market, size, value, operating profitability and investment. The beauty of all functionality here is that it can be based on any period as the function accepts the period 'weekly', 'monthly', 'quarterly' and 'yearly'. For example, this shows the quarterly correlations for Apple:

|        |   Mkt-RF |     SMB |     HML |     RMW |     CMA |
|:-------|---------:|--------:|--------:|--------:|--------:|
| 2022Q2 |   0.9177 | -0.1248 | -0.5077 | -0.3202 | -0.2624 |
| 2022Q3 |   0.8092 |  0.1528 | -0.5046 | -0.1997 | -0.5231 |
| 2022Q4 |   0.8998 |  0.2309 | -0.5968 | -0.1868 | -0.5946 |
| 2023Q1 |   0.7737 |  0.1606 | -0.3775 | -0.228  | -0.5707 |
| 2023Q2 |   0.7416 | -0.1166 | -0.2722 |  0.0093 | -0.4745 |

And below the correlations with each factor are plotted over time for both Apple and Microsoft.

![Performance](https://github.com/JerBouma/FinanceToolkit/assets/46355364/9c1eff76-b5c8-4bd2-9f47-8ce70bf002db)

### Obtaining Risk Metrics

Get the Value at Risk for each quarter. Here, the days within each quarter are considered for the Value at Risk. This makes it so that you can understand within each period what is the expected Value at Risk (VaR) which can again be any period but also based on distributions such as Historical, Gaussian, Student-t, Cornish-Fisher.

|                       |    AAPL |    MSFT |   Benchmark |
|:----------------------|--------:|--------:|------------:|
| 2023-09-25/2023-10-01 | -0.0205 | -0.0133 |     -0.0122 |
| 2023-10-02/2023-10-08 | -0.0048 | -0.0206 |     -0.0108 |
| 2023-10-09/2023-10-15 | -0.0089 | -0.0092 |     -0.0059 |
| 2023-10-16/2023-10-22 | -0.0135 | -0.0124 |     -0.0131 |
| 2023-10-23/2023-10-29 | -0.0224 | -0.0293 |     -0.0139 |

And below the Value at Risk (VaR) for Apple, Microsoft and the benchmark (S&P 500) are plotted also demonstrating the impact of COVID-19.

![Risk](https://github.com/JerBouma/FinanceToolkit/assets/46355364/a95e5b51-f7fc-4a70-bbb4-bf88b346523e)

### Obtaining Technical Indicators

Get the Ichimoku Cloud parameters based on the historical market data. This can be any of the 30+ technical indicators within the `technicals` module. The `get_` functions show a single indicator whereas the `collect_` functions show an aggregation of multiple indicators. For example, see some of the parameters for Apple below:

| Date       |   Base Line |   Conversion Line |   Leading Span A |   Leading Span B |
|:-----------|------------:|------------------:|-----------------:|-----------------:|
| 2023-10-30 |     174.005 |           171.755 |          176.245 |            178.8 |
| 2023-10-31 |     174.005 |           171.755 |          176.37  |            178.8 |
| 2023-11-01 |     174.005 |           170.545 |          176.775 |            178.8 |
| 2023-11-02 |     174.005 |           171.725 |          176.235 |            178.8 |
| 2023-11-03 |     174.005 |           171.725 |          175.558 |            178.8 |

And below the Ichimoku Cloud parameters are plotted for Apple and Microsoft side-by-side.

![Technicals](https://github.com/JerBouma/FinanceToolkit/assets/46355364/1ced5b34-2410-4206-8ddf-bb053bcb21b2)