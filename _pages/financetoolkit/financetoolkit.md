---
permalink: projects/financetoolkit
title: Finance Toolkit
excerpt: This is a free open-source toolkit written in Python in which 150+ financial ratios, indicators and performance measurements are written down in the most simplistic way allowing for complete transparency of the calculation method. This allows you to not have to rely on metrics from other providers and, given a financial statement, allow for efficient manual calculations. This leads to one uniform method of calculation being applied that is available and understood by everyone.
description: This is a free open-source toolkit written in Python in which 150+ financial ratios, indicators and performance measurements are written down in the most simplistic way allowing for complete transparency of the calculation method. This allows you to not have to rely on metrics from other providers and, given a financial statement, allow for efficient manual calculations. This leads to one uniform method of calculation being applied that is available and understood by everyone.
classes: wide-sidebar
author_profile: false
redirect_from:
  - /financetoolkit
sidebar:
  nav: "financetoolkit"
---

While browsing a variety of websites, I kept finding that the same financial metric can greatly vary per source and so do the financial statements reported while little information is given how the metric was calculated.

For example, Microsoft's Price-to-Earnings (PE) ratio on the 6th of May, 2023 is reported to be 28.93 (Stockopedia), 32.05 (Morningstar), 32.66 (Macrotrends), 33.09 (Finance Charts), 33.66 (Y Charts), 33.67 (Wall Street Journal), 33.80 (Yahoo Finance) and 34.4 (Companies Market Cap). All of these calculations are correct, however the method applied varies leading to different results. Therefore, collecting data from multiple sources can lead to wrong interpretation of the results given that one source could be applying a different calculation method than another. And that is, if it is even freely available. Often the calculation is hidden behind a paid subscription.

**This is why I designed the FinanceToolkit**, this is an open-source toolkit in which all relevant financial ratios ([180+](#available-metrics)), indicators and performance measurements are written down in the most simplistic way allowing for complete transparency of the calculation method ([proof](https://github.com/JerBouma/FinanceToolkit/blob/main/financetoolkit/ratios/valuation_model.py)). This allows you to not have to rely on metrics from other providers and, given a financial statement, allow for efficient manual calculations. This leads to one uniform method of calculation being applied that is available and understood by everyone.

The Finance Toolkit not only supports Equities. Even for Options, Currencies, Cryptocurrencies, ETFs, Mutual Funds, Indices, Money Markets, Commodities, Key Economic Indicators and more, the Finance Toolkit can be used to obtain historical data as well as important performance and risk measurements such as the Sharpe Ratio and Value at Risk.

The Finance Toolkit is complimented very well with the [Finance Database 🌎](https://github.com/JerBouma/FinanceDatabase), a database that features 300.000+ symbols containing Equities, ETFs, Funds, Indices, Currencies, Cryptocurrencies and Money Markets. By utilising both, it is possible to do a fully-fledged competitive analysis with the tickers found from the FinanceDatabase inputted into the FinanceToolkit.

---

**Interested in seeing the Finance Toolkit in action?** Find below a dashboard that can plot most of the metrics found inside the Finance Toolkit. <a href="/projects/financetoolkit/interactive-dashboard" target="_blank">**Find the dashboard here.**</a>

<p align="center">
    <a href="/projects/financetoolkit/interactive-dashboard" target="_blank">
        <img src="https://github.com/JerBouma/FinanceToolkit/blob/main/app/assets/financetoolkit-dashboard.gif?raw=true" alt="Finance Toolkit Illustration" width="100%" onerror="this.style.display = 'none'"/>
    </a>
</p>

## Installation

Before installation, consider starring the project on GitHub which helps others find the project as well. 

<a href="https://github.com/JerBouma/FinanceToolkit" target="_blank"><img width="1415" alt="image" src="https://github.com/JerBouma/FinanceToolkit/assets/46355364/014109fe-0c68-47d4-99bd-217c69dcea8d" target="_blank"></a>

To install the FinanceToolkit it simply requires the following:

{% include code_header.html %}
{% highlight bash %}
pip install financetoolkit -U
{% endhighlight %}

Then within Python use:

{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

companies = Toolkit(
    tickers=['GOOGL', 'MSFT', 'AMZN'],
    api_key="FINANCIAL_MODELING_PREP_KEY",
)
{% endhighlight %}

To be able to get started, you need to obtain an API Key from FinancialModelingPrep. This is used to gain access to 30+ years of financial statement both annually and quarterly. Note that the Free plan is limited to 250 requests each day, 5 years of data and only features companies listed on US exchanges.

___ 

<p align="center"><b>Obtain an API Key from FinancialModelingPrep <a href="https://www.jeroenbouma.com/fmp" target="_blank">here</a>.</b></p>
___

Through the link you are able to subscribe for the free plan and also premium plans at a **15% discount**. This is an affiliate link and thus supports the project at the same time. I have chosen FinancialModelingPrep as a source as I find it to be the most transparent, reliable and at an affordable price. I have yet to find a platform offering such low prices for the amount of data offered. When you notice that the data is inaccurate or have any other issue related to the data, note that I simply provide the means to access this data and I am not responsible for the accuracy of the data itself. For this, use [their contact form](https://site.financialmodelingprep.com/contact) or provide the data yourself. 

## How-To Guides for the FinanceToolkit

This section contains a list of How-To guides for the Finance Toolkit. These guides are meant to show you how to use the Finance Toolkit and how to perform a financial analysis. The guides are written in the form of Jupyter Notebooks. You can view the notebooks by clicking on the button below the description.

<div class="row">
<div markdown="1" class="fifty-column-left mobile-max-column-width">

### Getting Started

The Finance Toolkit offers a comprehensive set of tools designed to empower users with in-depth insights into the world of finance. By demonstrating each functionality and its practical application. This notebook will show you how to get started with the Finance Toolkit.

[Open the Notebook](/projects/financetoolkit/getting-started){: .btn .btn--warning}

</div>
<div markdown="1" class="fifty-column-right mobile-max-column-width">

### Discovery Module

The Discovery Module contains lists of companies, cryptocurrencies, forex, commodities, etfs and indices including screeners, quotes, performance metrics and more to find and select tickers to use in the Finance Toolkit. 

[Open the Notebook](/projects/financetoolkit/discovery-module){: .btn .btn--info}

</div>
</div>
<div markdown="1" class="fifty-column-left mobile-max-column-width">

### Ratios Module

The Ratios Module contains over 50+ ratios that can be used to analyse companies. These ratios are divided into 5 categories which are efficiency, liquidity, profitability, solvency and valuation. Each ratio is calculated using the data from the Toolkit module. 

[Open the Notebook](/projects/financetoolkit/ratios-module){: .btn .btn--info}

</div>

<div class="row">
<div markdown="1" class="fifty-column-right mobile-max-column-width">

### Models Module

The Models module is meant to execute well-known models such as DUPONT and the Discounted Cash Flow (DCF) model. These models are also directly related to the data retrieved from the Toolkit module.

[Open the Notebook](/projects/financetoolkit/models-module){: .btn .btn--info}

</div>
</div>

<div markdown="1" class="fifty-column-left mobile-max-column-width">

### Options Module

The Options module is meant to calculate important options metrics such as the First, Second and Third Order Greeks, the Black Scholes Model and the Option Chains as well as Implied Volatilities, Breeden—Litzenberger and more.

[Open the Notebook](/projects/financetoolkit/options-module){: .btn .btn--info}

</div>

<div class="row">
<div markdown="1" class="fifty-column-right mobile-max-column-width">

### Technicals Module

The Technicals Module contains 30+ Technical Indicators that can be used to analyse companies. These ratios are divided into 4 categories which are breadth, momentum, overlap and volatility. Each indicator is calculated using the data from the Toolkit module.

[Open the Notebook](/projects/financetoolkit/technicals-module){: .btn .btn--info}

</div>
</div>

<div markdown="1" class="fifty-column-left mobile-max-column-width">

### Risk Module

The Risk module is meant to calculate important risk metrics such as Value at Risk (VaR), Conditional Value at Risk (cVaR), Maximum Drawdown, Correlations, GARCH, EWMA and more.

[Open the Notebook](/projects/financetoolkit/risk-module){: .btn .btn--info}

</div>

<div class="row">
<div markdown="1" class="fifty-column-right mobile-max-column-width">

### Performance Module

The Performance module is meant to calculate important performance metrics such as Sharpe Ratio, Sortino Ratio, Treynor Ratio, Information Ratio, Jensen's Alpha, Beta, Capital Asset Pricing Model, R-Squared and more.

[Open the Notebook](/projects/financetoolkit/performance-module){: .btn .btn--info}

</div>
</div>

<div class="row">
<div markdown="1" class="fifty-column-left mobile-max-column-width">

### Fixed Income Module

The Fixed Income module contains a wide variety of fixed income related calculations such as the Effective Yield, the Macaulay Duration, the Modified Duration Convexity, the Yield to Maturity and models such as Black and Bachelier to valuate derivative instruments such as Swaptions.

[Open the Notebook](/projects/financetoolkit/fixed-income-module){: .btn .btn--info}

</div>

<div markdown="1" class="fifty-column-right mobile-max-column-width">

### Economics Module

The Economics module gives insights for 60+ countries into key economic indicators such as the Consumer Price Index (CPI), Gross Domestic Product (GDP), Unemployment Rates and 3-month and 10-year Government Interest Rates. This is done through the economics module and can be used as a standalone module as well.

[Open the Notebook](/projects/financetoolkit/economics-module){: .btn .btn--info}

</div>
</div>

<div class="row">
<div markdown="1" class="fifty-column-left mobile-max-column-width">

### Portfolio Module

The Portfolio Module allows you to use your own transactions data from your portfolio to see performance over time and understand key drivers of your portfolio (compared to a benchmark). It also directly integrates with the Toolkit module to provide you with the most up-to-date data.

[Open the Notebook](/projects/financetoolkit/portfolio-module){: .btn .btn--info}

</div>

<div markdown="1" class="fifty-column-left mobile-max-column-width">

### External Datasets

The Finance Toolkit has the ability to leverage custom datasets from any data provider as well. This makes it possible to work with your preferred data and not be limited to the data source the Finance Toolkit currently provides. With this, it is possible to work with datasets from Yahoo Finance, OpenBB, Quandl, EODH, Bloomberg and much more.

[Open the Notebook](/projects/financetoolkit/external-datasets){: .btn .btn--info}

</div>

## Basic Usage

This section is an introduction to the Finance Toolkit. Also see [this notebook](https://www.jeroenbouma.com/projects/financetoolkit/getting-started) for a detailed Getting Started guide as well as [this notebook](https://www.jeroenbouma.com/projects/financetoolkit/finance-database) that includes the [Finance Database 🌎](https://www.jeroenbouma.com/projects/financedatabase) and a proper financial analysis. Next to that, find below a fully-fledged code documentation as well as Jupyter Notebooks in which you can see many examples ranging from basic examples to creating custom ratios to working with your own datasets.

<p align="center">
    <img src="https://github.com/JerBouma/FinanceToolkit/blob/main/examples/Finance%20Toolkit%20-%20Video%20Demo.gif?raw=true" alt="Finance Toolkit Illustration" width="100%" onerror="this.style.display = 'none'"/>
</p>

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

# an Options example
all_greeks = companies.options.collect_all_greeks(expiration_time_range=180)

# a Performance example
factor_asset_correlations = companies.performance.get_factor_asset_correlations(
    period="quarterly"
)

# a Risk example
value_at_risk = companies.risk.get_value_at_risk(period="weekly")

# a Technical example
ichimoku_cloud = companies.technicals.get_ichimoku_cloud()

# a Fixed Income example
corporate_bond_yields = companies.fixed_income.get_ice_bofa_effective_yield()

# an Economics example
unemployment_rates = companies.economics.get_unemployment_rate()
````

Generally, the functions return a DataFrame with a multi-index in which all tickers, in this case Apple and Microsoft, are presented. To keep things manageable for this README, I select just Apple but in essence the list of tickers can be endless as I've seen DataFrames with thousands of tickers. The filtering is done through `.loc['AAPL']` and `.xs('AAPL', level=1, axis=1)` based on whether it's fundamental data or historical data respectively.

### Obtaining Historical Data

Obtain historical data on a daily, weekly, monthly or yearly basis. This includes OHLC, volumes, dividends, returns, cumulative returns and volatility calculations for each corresponding period. For example, the a portion of the historical data for Apple is shown below.

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

Obtain an Income Statement on an annual or quarterly basis. This can also be a balance statement (`companies.get_balance_sheet_statement()`) or cash flow statement (`companies.get_cash_flow_statement()`). For example, the first 5 rows of the Income Statement for Apple are shown below.

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

### Obtaining Options and Greeks

Get the Black Scholes Model for both call and put options including the relevant Greeks, in this case Delta, Gamma, Theta and Vega. This can be any of the First, Second or Third Order Greeks as found in the the `options` module. The `get_` functions show a single Greek whereas the `collect_` functions show an aggregation of Greeks. For example, see the delta of the Call options for Apple for multiple expiration times and strike prices below (Stock Price: 185.92, Volatility: 31.59%, Dividend Yield: 0.49% and Risk Free Rate: 3.95%):

|     |   1 Month |   2 Months |   3 Months |   4 Months |   5 Months |   6 Months |
|----:|----------:|-----------:|-----------:|-----------:|-----------:|-----------:|
| 175 |    0.7686 |     0.7178 |     0.6967 |     0.6857 |     0.6794 |     0.6759 |
| 180 |    0.6659 |     0.64   |     0.6318 |     0.629  |     0.6285 |     0.6291 |
| 185 |    0.5522 |     0.5583 |     0.5648 |     0.571  |     0.5767 |     0.5816 |
| 190 |    0.4371 |     0.4762 |     0.4977 |     0.513  |     0.5249 |     0.5342 |
| 195 |    0.3298 |     0.3971 |     0.4324 |     0.4562 |     0.474  |     0.4875 |

Which can also be plotted together with Gamma, Theta and Vega as follows:

![Greeks](https://github.com/JerBouma/FinanceToolkit/assets/46355364/3aebe116-c4ac-4845-9801-54d2b4bde0f5)

### Obtaining Performance Metrics

Get the correlations with the factors as defined by Fama-and-French. These include market, size, value, operating profitability and investment. The beauty of all functionality here is that it can be based on any period as the function accepts the period `intraday`, `weekly`, `monthly`, `quarterly` and `yearly`. For example, this shows the quarterly correlations for Apple:

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

Get the Value at Risk for each week. Here, the days within each week are considered for the Value at Risk. This makes it so that you can understand within each period what is the expected Value at Risk (VaR) which can again be any period but also based on distributions such as Historical, Gaussian, Student-t, Cornish-Fisher.

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

### Obtaining Fixed Income Metrics

Get access to the ICE BofA Corporate Bond benchmark indices and a variety of other bond and derivative related valuations within the `fixedincome` module. For example, see the Effective Yield for the ICE BofA Corporate Bond Index below for each Credit Rating:

| Date       |    AAA |     AA |      A |    BBB |     BB |      B |    CCC |
|:-----------|-------:|-------:|-------:|-------:|-------:|-------:|-------:|
| 2024-04-19 | 0.0518 | 0.0532 | 0.0561 | 0.0594 | 0.0678 | 0.0804 | 0.1385 |
| 2024-04-22 | 0.0517 | 0.0532 | 0.056  | 0.0593 | 0.0671 | 0.0793 | 0.1377 |
| 2024-04-23 | 0.0514 | 0.0528 | 0.0556 | 0.0589 | 0.066  | 0.0777 | 0.1364 |
| 2024-04-24 | 0.0518 | 0.0531 | 0.0559 | 0.0592 | 0.0664 | 0.0778 | 0.1361 |
| 2024-04-25 | 0.0524 | 0.0537 | 0.0564 | 0.0598 | 0.0673 | 0.079  | 0.1368 |

And below a variety of Fixed Income metrics are shown all acquired from the Fixed Income module.

![Fixed Income](https://github.com/JerBouma/FinanceToolkit/assets/46355364/dfe2a819-87d8-46be-892c-f90663bc177d)

### Understanding Key Economic Indicators

Get insights for 60+ countries into key economic indicators such as the Consumer Price Index (CPI), Gross Domestic Product (GDP), Unemployment Rates and 3-month and 10-year Government Interest Rates. This is done through the `economics` module and can be used as a standalone module as well by using `from financetoolkit import Economics`. For example see a selection of the countries below:

|      |   Colombia |   United States |   Sweden |   Japan |   Germany |
|:-----|-----------:|----------------:|---------:|--------:|----------:|
| 2017 |     0.093  |          0.0435 |   0.0686 |  0.0281 |    0.0357 |
| 2018 |     0.0953 |          0.039  |   0.0648 |  0.0244 |    0.0321 |
| 2019 |     0.1037 |          0.0367 |   0.0691 |  0.0235 |    0.0298 |
| 2020 |     0.1586 |          0.0809 |   0.0848 |  0.0278 |    0.0362 |
| 2021 |     0.1381 |          0.0537 |   0.0889 |  0.0282 |    0.0358 |
| 2022 |     0.1122 |          0.0365 |   0.0748 |  0.026  |    0.0307 |

And below these Unemployment Rates are plotted over time:

![Economics](https://github.com/JerBouma/FinanceToolkit/assets/46355364/0bba2ce2-9846-42de-a89d-737cdcd07b31)

### Explore your own Portfolio

Through a custom XLSX, XLS or CSV file you are able to load in your own portfolio directly into the Finance Toolkit. This allows you to view your positions and performance (over time) versus a benchmark and other positions as well as your PnL development over time. Furthermore, the portfolio can be directly loaded in the core functionality of the Finance Toolkit as well making it possible to calculate all metrics and ratios for your portfolio (which is a time-weighted sum of all positions). The portfolio module is a standalone module and can be used as such by using `from financetoolkit import Portfolio`.

___
<b><div align="center">It is important to note that it requires a specific Excel template to work, see for further instructions the following notebook <a href="https://www.jeroenbouma.com/projects/financetoolkit/portfolio" target="_blank">here</a>.</div></b>
___

The table below shows one of the functionalities of the Portfolio module but is purposely shrunken down given the >30 assets.

| Identifier   |   Volume |   Costs |    Price |   Invested |   Latest Price |   Latest Value |   Return |   Return Value |   Benchmark Return |   Volatility |   Benchmark Volatility |   Alpha |   Beta |   Weight |
|:-------------|---------:|--------:|---------:|-----------:|---------------:|---------------:|---------:|---------------:|-------------------:|-------------:|-----------------------:|--------:|-------:|---------:|
| AAPL         |      137 |     -28 |  38.9692 |   5310.78  |        241.84  |       33132.1  |   5.2386 |     27821.3    |             2.2258 |       0.3858 |                 0.1937 |  3.0128 | 1.2027 |   0.0405 |
| ALGN         |       81 |     -34 | 117.365  |   9472.53  |        187.03  |       15149.4  |   0.5993 |      5676.9    |             2.1413 |       0.5985 |                 0.1937 | -1.542  | 1.5501 |   0.0185 |
| AMD          |       78 |     -30 |  11.9075 |    898.784 |         99.86  |        7789.08 |   7.6662 |      6890.3    |             3.7945 |       0.6159 |                 0.1937 |  3.8718 | 1.6551 |   0.0095 |
| AMZN         |      116 |     -28 |  41.5471 |   4791.46  |        212.28  |       24624.5  |   4.1392 |     19833      |             1.8274 |       0.4921 |                 0.1937 |  2.3118 | 1.1594 |   0.0301 |
| ASML         |      129 |     -25 |  33.3184 |   4273.07  |        709.08  |       91471.3  |  20.4065 |     87198.3    |             3.8005 |       0.4524 |                 0.1937 | 16.606  | 1.4407 |   0.1119 |
| VOO          |       77 |     -12 | 238.499  |  18352.5   |        546.33  |       42067.4  |   1.2922 |     23715      |             1.1179 |       0.1699 |                 0.1937 |  0.1743 | 0.9973 |   0.0515 |
| WMT          |       92 |     -18 |  17.8645 |   1625.53  |         98.61  |        9072.12 |   4.581  |      7446.59   |             2.4787 |       0.2334 |                 0.1937 |  2.1024 | 0.4948 |   0.0111 |
| Portfolio    |     2142 |    -532 |  59.8406 | 128710     |        381.689 |      817577    |   5.3521 |    688867      |             2.0773 |       0.4193 |                 0.1937 |  3.2747 | 1.2909 |   1      |

In which the weights and returns can be depicted as follows:

![Portfolio](https://github.com/user-attachments/assets/a5e05df5-a76a-42fa-bb30-f640cd48da62)
# Questions & Answers

This section includes frequently asked questions and is meant to clear up confusion about certain results and/or deviations from other sources. If you have any questions that are not answered here, feel free to reach out to me via the contact details below.

> **How do you deal with companies that have different fiscal years?**

For any financial statement, I make sure to line it up with the corresponding *calendar* period. For example, Apple's Q4 2023 relates to July to September of 2023. This corresponds to the calendar period Q3 which is why I normalize Apple's numbers to Q3 2023 instead. This is done to allow for comparison between companies that have different fiscal years.

> **Why do the numbers in the financial statements sometimes deviate from the data from FinancialModelingPrep?**

When looking at a company such as Hyundai Motor Company (ticker: 005380.KS), you will notice that the financial statements are reported in KRW (South Korean won). As this specific ticker is listed on the Korean Exchange, the historical market data will also be reported in KRW. However, if you use the ticker HYMTF, which is listed on the American OTC market, the historical market data will be reported in USD. To deal with this discrepancy, the end of year or end of quarter exchange rate is retrieved which is used to convert the financial statements to USD. This is done to prevent ratio calculations such as the Free Cash Flow Yield (which is based on the market capitalization) or Price Earnings Ratio (which is based on the stock price) from being incorrect. This can be disabled by setting `convert_currency=False` in the Toolkit initialization. It is recommended to always use the ticker that is listed on the exchange where the company is based.

> **How can I get TTM (Trailing Twelve Months) and Growth metrics?**

Most functions will have the option to define the `trailing` parameter. This lets you define the number of periods that you want to use to calculate the trailing metrics. For example, if you want to calculate the trailing 12-month (TTM) Price-to-Earnings Ratio, you can set `trailing=4` when you have set `quarterly=True` in the Toolkit initialization. The same goes for growth metrics which can be calculated by setting `growth=True`. This will calculate the growth for each period based on the previous period. This also includes a `lag` parameter in which you can define lagged growth. Furthermore, you can also combine the trailing and growth parameters to get trailing growth. For example, set `trailing=4` and `growth=True`  for the Price-to-Earnings Ratio which will then calculate the TTM growth.

> **How can I save the data periodically so that I don't have to retrieve it every single time again?**

The Toolkit has the option to work with cached data through `use_cached_data=True` when initializing the Toolkit class. If you then use any of the functionalities of the Toolkit itself (e.g. `get_balance_sheet_statement`) it will store the data in a pickle file. When initializing the Toolkit class again with `use_cached_data=True`, it will load the data from the pickle file including all other previously set parameters (e.g. start_date and quarterly). You are also able to select a specific location to store the cached data by providing a string to the `use_cached_data` parameter. This will store the data in the provided location (with the assumption the folder exists).

> **What is the "Benchmark" that is automatically obtained when acquiring historical data?**

This is related to the `benchmark_ticker` parameter which is set to "SPY" (S&P 500) by default. This is important when calculating performance metrics such as the Sharpe Ratio or Treynor Ratio that require a market return. This can be disabled by setting `benchmark_ticker=None` in the Toolkit initialization.

> **Data collection seems to be slow, what could be the issue?**

Generally, it should take less than 15 seconds to retrieve the historical data of 100 tickers. If it takes much longer, this could be due to reaching the API limit (the Starter plan has 250 requests per minute), due to a slow internet connection or due to unoptimized code. As the Finance Toolkit makes use of threading, initializing the Toolkit with a single ticker will result in a slow process. This is because the Toolkit will have to wait for the previous request to finish before it can start the next one. Therefore, it is recommended to initialize the Toolkit with all tickers you want to analyze. If it is taking 10+ minutes consider having a look at [this issue](https://github.com/JerBouma/FinanceToolkit/issues/99#issuecomment-1889726000) that managed to resolve the problem.

> **Are you part of FinancialModelingPrep?**

*No, I am not*. I've merely picked them as the primary data provider given that they have a generous free tier and fair pricing compared to other providers. Therefore, any questions related to the data should go through [their contact form](https://site.financialmodelingprep.com/contact). When it comes to any type of ratios, performance metrics, risk metrics, technical indicators or economic indicators, feel free to reach out to me as this is my own work.

# Contributing
First off all, thank you for taking the time to contribute (or at least read the Contributing Guidelines)! 🚀

___ 

<b><div align="center">Find the Contributing Guidelines <a href="/CONTRIBUTING.md">here</a>.</div></b>
___

The goal of the Finance Toolkit is to make any type of financial calculation as transparent and efficient as possible. I want to make these type of calculations as accessible to anyone as possible and seeing how many websites exists that do the same thing (but instead you have to pay) gave me plenty of reasons to work on this.

# Contact
If you have any questions about the FinanceToolkit or would like to share with me what you have been working on, feel free to reach out to me via:

- **Website**: https://jeroenbouma.com/
- **LinkedIn:** https://www.linkedin.com/in/boumajeroen/
- **Email:** jer.bouma@gmail.com

If you'd like to support my efforts, either help me out by contributing to the package or [Sponsor Me](https://github.com/sponsors/JerBouma).

[![Star History Chart](https://api.star-history.com/svg?repos=JerBouma/FinanceToolkit&type=Date)](https://star-history.com/#JerBouma/FinanceToolkit&Date)