---
permalink: /projects/financetoolkit
software:
  name: "Finance Toolkit"
  repository: "https://github.com/JerBouma/FinanceToolkit"
  download: "https://pypi.org/project/financetoolkit/"
title: Finance Toolkit
excerpt: This is a free open-source toolkit written in Python in which 500+ financial methods are written down in the most simplistic way allowing for complete transparency of the calculation method. This allows you to not have to rely on metrics from other providers and, given a financial statement, allow for efficient manual calculations. This leads to one uniform method of calculation being applied that is available and understood by everyone.
description: "The Finance Toolkit is a free open-source Python package with 500+ transparent financial ratios, metrics and models computed from financial statements."
classes: wide-sidebar ft-overview
author_profile: false
redirect_from:
  - /financetoolkit
  - /projects/financetoolkit/interactive-dashboard
sidebar:
  nav: "financetoolkit"
image: assets/images/projects/FinanceToolkit.jpg
---

<div class="page-header-action notebook-viewer-actions"><a href="https://github.com/JerBouma/FinanceToolkit" target="_blank" rel="noopener"><i class="fab fa-github"></i> View on GitHub</a></div>

{%- assign ft = site.data.projects.maintained | where: "name", "Finance Toolkit" | first %}
{%- assign ft_stars = ft.stats | where: "icon", "fa-star" | first %}
{%- assign ft_dl = ft.stats | where: "icon", "fa-download" | first %}
<div class="ft-hero">
  <div class="mcp-video-wrapper ft-hero__video">
    <video class="mcp-demo-video" autoplay muted playsinline controls preload="auto" width="1920" height="1080"
           poster="/assets/images/projects/financetoolkit-launch.jpg"
           aria-label="Same metric, same day, different answers across financial websites; the Finance Toolkit gives one consistent, verifiable formula for 500+ metrics.">
      <source src="/assets/video/financetoolkit-launch.mp4" type="video/mp4">
    </video>
  </div>
  <div class="mcp-facts ft-hero__facts">
    <div class="mcp-fact"><strong>500+</strong><span>metrics</span></div>
    <div class="mcp-fact"><strong>{{ ft_stars.value }}</strong><span>GitHub stars</span></div>
    <div class="mcp-fact"><strong>{{ ft_dl.value }}</strong><span>downloads</span></div>
  </div>
</div>

While browsing a variety of websites, I kept finding that the same financial metric can vary a lot per source, and so do the reported financial statements, while little information is given on how the metric was calculated.

For example, Microsoft's Price-to-Earnings (PE) ratio on the 6th of May, 2023 is reported to be 28.93 (Stockopedia), 32.05 (Morningstar), 32.66 (Macrotrends), 33.09 (Finance Charts), 33.66 (Y Charts), 33.67 (Wall Street Journal), 33.80 (Yahoo Finance) and 34.4 (Companies Market Cap). All of these calculations are correct, but each source applies a different method, which leads to different results. Collecting data from multiple sources can therefore lead to a wrong interpretation of the results, since one source could be using a different calculation method than another. That is, if the method is freely available at all; often it is hidden behind a paid subscription.

**This is why I designed the FinanceToolkit**, an open-source toolkit in which all relevant financial methods ([500+](/projects/financetoolkit/docs)) are written down in the simplest way possible so that the calculation method is completely transparent ([proof](https://github.com/JerBouma/FinanceToolkit/blob/main/financetoolkit/ratios/valuation_model.py){:target="_blank"}). This way you don't have to depend on metrics from providers that don't share their methods. Given a set of financial statements, you can do the calculations yourself with one consistent set of formulas that anyone can read and understand.

Beyond Equities, it supports Options, Currencies, Cryptocurrencies, ETFs, Mutual Funds, Indices, Money Markets, Commodities, Key Economic Indicators and more, allowing you to obtain historical data as well as important performance and risk measurements such as the Sharpe Ratio and Value at Risk.

The Finance Toolkit works well together with the [Finance Database 🌎](https://github.com/JerBouma/FinanceDatabase){:target="_blank"}, a database of 300,000+ symbols covering Equities, ETFs, Indices, Currencies and Cryptocurrencies. By using both, you can do a full competitive analysis: find the tickers in the FinanceDatabase and feed them into the FinanceToolkit.

## Installation

Before installation, consider starring the project on GitHub which helps others find the project as well. 

<a href="https://github.com/JerBouma/FinanceToolkit" target="_blank"><img width="1415" alt="image" src="https://github.com/JerBouma/FinanceToolkit/assets/46355364/014109fe-0c68-47d4-99bd-217c69dcea8d" target="_blank"></a>

Installing the FinanceToolkit only requires the following:

```bash
pip install financetoolkit -U
```

Then within Python use:

```python
from financetoolkit import Toolkit

companies = Toolkit(
    tickers=['GOOGL', 'MSFT', 'AMZN'],
    api_key="FINANCIAL_MODELING_PREP_KEY",
)
```

To be able to get started, you need to obtain an API Key from FinancialModelingPrep. This gives access to 30+ years of financial statements, both annual and quarterly. Note that the Free plan is limited to 250 requests each day, 5 years of data and only features companies listed on US exchanges.

[Obtain an API Key from FinancialModelingPrep](/fmp){: .btn .btn--warning .btn--large .align-center target="_blank"}

Through the link you are able to subscribe for the free plan and also premium plans at a **15% discount**. This is an affiliate link and thus supports the project at the same time. I chose FinancialModelingPrep as a source because I find it the most transparent and reliable option at an affordable price. I have yet to find a platform offering such low prices for the amount of data offered. If you notice that the data is inaccurate or have any other issue with the data, note that I only provide the means to access it and am not responsible for its accuracy. For that, use [their contact form](https://site.financialmodelingprep.com/contact){:target="_blank"} or provide the data yourself.

**By default, the Finance Toolkit prioritizes Financial Modeling Prep for data retrieval. If data acquisition from Financial Modeling Prep is unsuccessful (e.g., due to plan restrictions or API key issues), the toolkit automatically switches to Yahoo Finance as a secondary source.** To disable this fallback behavior and exclusively use Financial Modeling Prep, set `enforce_source="FinancialModelingPrep"` during Toolkit initialization.

## Functionality
{: .heading-as-h1}
This section is an introduction to the Finance Toolkit. The documentation contains many more examples: every module page opens with a Getting Started section, from the basics to creating custom ratios and working with your own datasets.

[Find the Documentation](/projects/financetoolkit/docs){: .btn .btn--warning .btn--large .align-center}

The sections below follow one analysis from start to finish: finding companies, loading their prices and financial statements, analysing their fundamentals, weighing their risk and return, and finally looking at the economies they depend on. That covers only part of the Finance Toolkit; [options and the Greeks](/projects/financetoolkit/docs/options), [technical indicators](/projects/financetoolkit/docs/technicals), [bonds and derivatives](/projects/financetoolkit/docs/fixedincome), [econometrics](/projects/financetoolkit/docs/econometrics) and [your own portfolio](/projects/financetoolkit/docs/portfolio) each have their own documentation page.

### Finding Companies

An analysis starts with a set of companies. The Discovery module finds them without needing any tickers yet, through stock screeners, sector performance, news and lists of companies, ETFs, indices, currencies, cryptocurrencies and commodities.

The screener below looks for semiconductor companies on NASDAQ that are worth more than $100 billion:

```python
from financetoolkit import Discovery

# Initialize the standalone Discovery module
discovery = Discovery(api_key="FINANCIAL_MODELING_PREP_KEY")

# Find US semiconductor companies worth more than $100 billion
semiconductors = discovery.get_stock_screener(
    industry="Semiconductors",
    country="US",
    exchange="NASDAQ",
    market_cap_higher=100_000_000_000,
    is_etf=False,
)
```

The screener returns twelve companies, of which the five largest are shown below:

| Symbol   | Name                         |     Market Cap |   Beta |   Price |   Dividend |
|:---------|:-----------------------------|---------------:|-------:|--------:|-----------:|
| NVDA     | NVIDIA Corporation           | 5330680000000  |  2.216 |  221.19 |       0.28 |
| AVGO     | Broadcom Inc.                | 1612050000000  |  1.476 |  337.70 |       2.60 |
| MU       | Micron Technology, Inc.      | 1039300000000  |  2.226 |  918.58 |       0.57 |
| AMD      | Advanced Micro Devices, Inc. |  907583000000  |  2.454 |  555.96 |       0.00 |
| INTC     | Intel Corp.                  |  490921000000  |  2.231 |   92.87 |       0.00 |

And below all twelve are ranked by market cap.

{% include ft-chart.html id="discovery" label="Market capitalization of US semiconductor companies worth more than $100 billion" %}

### Loading Prices and Financial Statements

The rest of this walkthrough follows three of them: Nvidia, AMD and Intel. They are loaded into the Toolkit in one line, and the S&P 500 comes along as the benchmark:

```python
from financetoolkit import Toolkit

# Initialize the Toolkit for Nvidia, AMD and Intel
companies = Toolkit(["NVDA", "AMD", "INTC"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2017-12-31")
```

[Historical data](/projects/financetoolkit/docs#get_historical_data) comes on a daily, weekly, monthly, quarterly or yearly basis, with the return and cumulative return of each period:

```python
# Obtain weekly market data for all tickers
historical_data = companies.get_historical_data(period="weekly")

# Select the results for Nvidia
historical_data.xs("NVDA", axis=1, level=1)
```

For example, the first weeks for Nvidia are shown below.

| Date                  |   Open |   High |    Low |  Close |      Volume |   Return |   Cumulative Return |
|:----------------------|-------:|-------:|-------:|-------:|------------:|---------:|--------------------:|
| 2018-01-01/2018-01-07 | 4.8945 | 5.4513 | 4.8625 | 5.3850 | 2.43371e+09 |          |              1.0000 |
| 2018-01-08/2018-01-14 | 5.5100 | 5.6568 | 5.4000 | 5.5745 | 2.72683e+09 |   0.0352 |              1.0352 |
| 2018-01-15/2018-01-21 | 5.6013 | 5.7772 | 5.4173 | 5.7527 | 2.25877e+09 |   0.0320 |              1.0683 |
| 2018-01-22/2018-01-28 | 5.7607 | 6.0835 | 5.7025 | 6.0833 | 2.53238e+09 |   0.0575 |              1.1297 |
| 2018-01-29/2018-02-04 | 6.0685 | 6.2318 | 5.7793 | 5.8380 | 2.74221e+09 |  -0.0403 |              1.0841 |

And below the cumulative returns of all three are plotted against the S&P 500:

{% include ft-chart.html id="historical" label="Cumulative returns of Nvidia, AMD, Intel and the S&P 500" %}

The [income statement](/projects/financetoolkit/docs#get_income_statement), [balance sheet](/projects/financetoolkit/docs#get_balance_sheet_statement) and [cash flow statement](/projects/financetoolkit/docs#get_cash_flow_statement) come annually or quarterly in the same way:

```python
# Obtain the Income Statement for all tickers
income_statement = companies.get_income_statement()

# Select the results for Nvidia
income_statement.loc["NVDA"]
```

For example, the first rows of Nvidia's income statement are shown below.

|                                              |        2021 |        2022 |        2023 |        2024 |        2025 |
|:---------------------------------------------|------------:|------------:|------------:|------------:|------------:|
| Revenue                                      | 2.6914e+10  | 2.6974e+10  | 6.0922e+10  | 1.30497e+11 | 2.15938e+11 |
| Cost of Goods Sold                           | 9.439e+09   | 1.1618e+10  | 1.6621e+10  | 3.2639e+10  | 6.2475e+10  |
| Gross Profit                                 | 1.7475e+10  | 1.5356e+10  | 4.4301e+10  | 9.7858e+10  | 1.53463e+11 |
| Research and Development Expenses            | 5.268e+09   | 7.339e+09   | 8.675e+09   | 1.2914e+10  | 1.8497e+10  |
| Selling, General and Administrative Expenses | 2.166e+09   | 2.44e+09    | 2.654e+09   | 3.491e+09   | 4.579e+09   |

And below the revenue of all three is plotted for each fiscal year:

{% include ft-chart.html id="statements" label="Revenue of Nvidia, AMD and Intel" %}

### Analysing the Fundamentals

From these statements the Toolkit calculates 80+ [ratios](/projects/financetoolkit/docs/ratios) in five categories: efficiency, liquidity, profitability, solvency and valuation. Each ratio has its own function, and a `collect_` function returns a whole category at once:

```python
# Collect all Profitability Ratios for all tickers
profitability_ratios = companies.ratios.collect_profitability_ratios()

# Select the results for Nvidia
profitability_ratios.loc["NVDA"]
```

For example, some of Nvidia's profitability ratios are shown below.

|                            |   2021 |   2022 |   2023 |   2024 |   2025 |
|:---------------------------|-------:|-------:|-------:|-------:|-------:|
| Gross Margin               | 0.6493 | 0.5693 | 0.7272 | 0.7499 | 0.7107 |
| Operating Margin           | 0.3731 | 0.1566 | 0.5412 | 0.6242 | 0.6038 |
| Net Profit Margin          | 0.3623 | 0.1619 | 0.4885 | 0.5585 | 0.5560 |
| Return on Assets           | 0.2673 | 0.1023 | 0.5567 | 0.8220 | 0.7542 |
| Return on Equity           | 0.4483 | 0.1793 | 0.9146 | 1.1918 | 1.0149 |
| Return on Invested Capital | 0.2967 | 0.1094 | 0.6661 | 1.0032 | 0.9221 |

And below each of them is shown with its latest value and its course over the years.

{% include ft-chart.html id="ratios" label="Profitability ratios of Nvidia" %}

[Models](/projects/financetoolkit/docs/models) combine these ratios. The [Extended DuPont Analysis](/projects/financetoolkit/docs/models#get_extended_dupont_analysis) splits the return on equity into five components that multiply into it: interest burden, tax burden, operating margin, asset turnover and equity multiplier.

```python
# Get the Extended DuPont Analysis for all tickers
extended_dupont_analysis = companies.models.get_extended_dupont_analysis()

# Select the results for Nvidia
extended_dupont_analysis.loc["NVDA"]
```

For example, the components for Nvidia are shown below.

|                         |   2021 |   2022 |   2023 |   2024 |   2025 |
|:------------------------|-------:|-------:|-------:|-------:|-------:|
| Interest Burden Ratio   | 0.9900 | 0.9898 | 1.0257 | 1.0316 | 1.0848 |
| Tax Burden Ratio        | 0.9810 | 1.0447 | 0.8800 | 0.8674 | 0.8488 |
| Operating Profit Margin | 0.3731 | 0.1566 | 0.5412 | 0.6242 | 0.6038 |
| Asset Turnover          | 0.7376 | 0.6319 | 1.1397 | 1.4718 | 1.3564 |
| Equity Multiplier       | 1.6775 | 1.7525 | 1.6428 | 1.4499 | 1.3456 |
| Return on Equity        | 0.4483 | 0.1793 | 0.9146 | 1.1918 | 1.0149 |

And below the components and the resulting return on equity are plotted for each of the three companies.

{% include ft-chart.html id="models" label="Extended DuPont Analysis" %}

Other models include the [Weighted Average Cost of Capital](/projects/financetoolkit/docs/models#get_weighted_average_cost_of_capital), [Altman Z-Score](/projects/financetoolkit/docs/models#get_altman_z_score), [Piotroski F-Score](/projects/financetoolkit/docs/models#get_piotroski_score) and [Intrinsic Valuation](/projects/financetoolkit/docs/models#get_intrinsic_valuation). Almost every function also accepts `growth=True` for the growth from one period to the next, `trailing=4` for trailing twelve-month figures and `standardize=True` for Z-Scores.

### Weighing Risk and Return

The market data feeds the [performance](/projects/financetoolkit/docs/performance) and [risk](/projects/financetoolkit/docs/risk) modules, which calculate their metrics for any period, from intraday to yearly:

```python
# The annualized Sharpe Ratio for each year
sharpe_ratio = companies.performance.get_sharpe_ratio(period="yearly", annualize=True)

# The deepest fall within each year
maximum_drawdown = companies.risk.get_maximum_drawdown(period="yearly", within_period=True)
```

For example, the yearly Sharpe Ratios are shown below.

|      |    NVDA |     AMD |    INTC |
|:-----|--------:|--------:|--------:|
| 2020 |  1.6530 |  1.4190 | -0.0445 |
| 2021 |  2.0012 |  1.2366 |  0.2976 |
| 2022 | -0.8417 | -1.0530 | -1.5306 |
| 2023 |  2.6959 |  1.9195 |  1.8358 |
| 2024 |  2.0848 | -0.2615 | -1.5749 |
| 2025 |  0.8321 |  1.1753 |  1.2061 |

And below both are plotted for each year, the maximum drawdown together with the S&P 500.

{% include ft-chart.html id="risk" label="Sharpe Ratio and Maximum Drawdown" %}

Together the two modules cover 50+ metrics, such as [Value at Risk](/projects/financetoolkit/docs/risk#get_value_at_risk), [GARCH](/projects/financetoolkit/docs/risk#get_garch), [Jensen's Alpha](/projects/financetoolkit/docs/performance#get_jensens_alpha), the [Capital Asset Pricing Model](/projects/financetoolkit/docs/performance#get_capital_asset_pricing_model) and the [Fama-French factors](/projects/financetoolkit/docs/performance#get_fama_and_french_model). Most of them also accept `rolling=<n>` for a value that moves through time.

### Understanding the Economic Environment

Chip makers depend on the economies they sell into. The [revenue by region](/projects/financetoolkit/docs#get_revenue_geographic_segmentation) shows which economies those are:

```python
# Obtain the revenue per region for all tickers
geographic_segmentation = companies.get_revenue_geographic_segmentation()

# Select the results for Nvidia
geographic_segmentation.loc["NVDA"]
```

For example, the largest regions of Nvidia are shown below.

|                |       2022 |       2023 |       2024 |       2025 |
|:---------------|-----------:|-----------:|-----------:|-----------:|
| United States  | 4.349e+09  | 8.292e+09  | 2.6966e+10 | 6.1257e+10 |
| Taiwan         | 8.544e+09  | 6.986e+09  | 1.3405e+10 | 2.0573e+10 |
| Singapore      | 0          | 0          | 0          | 2.3684e+10 |
| China          | 7.111e+09  | 5.785e+09  | 1.0306e+10 | 1.7108e+10 |
| Other Americas | 6.91e+09   | 5.911e+09  | 1.0245e+10 | 7.875e+09  |

The [economics](/projects/financetoolkit/docs/economics) module covers 60+ countries with 50+ indicators, from GDP and inflation to unemployment, money supply and interest rates. It is reached through the same Toolkit instance, or on its own with `from financetoolkit import Economics`. The growth of the economy drives the demand for chips, and long-term interest rates weigh on how much investors pay for future earnings:

```python
countries = ["United States", "China", "Japan", "South Korea", "Germany"]

# Real GDP growth on the same quarter a year earlier
gdp_growth = companies.economics.get_gross_domestic_product_growth(countries, year_over_year=True)

# The yield on 10-year government bonds
long_term_interest_rate = companies.economics.get_long_term_interest_rate(countries)
```

For example, the long-term interest rates are shown below.

|      |   United States |   China |   Japan |   South Korea |   Germany |
|:-----|----------------:|--------:|--------:|--------------:|----------:|
| 2021 |          0.0144 |  0.0301 |  0.0006 |        0.0206 |   -0.0037 |
| 2022 |          0.0294 |  0.0276 |  0.0023 |        0.0336 |    0.0114 |
| 2023 |          0.0396 |  0.0271 |  0.0056 |        0.0364 |    0.0243 |
| 2024 |          0.0421 |  0.0218 |  0.0090 |        0.0322 |    0.0232 |
| 2025 |          0.0432 |  0.0175 |  0.0153 |        0.0289 |    0.0259 |

And below both are plotted over time, the GDP growth per quarter.

{% include ft-chart.html id="economics" label="GDP growth and long-term interest rates" %}

Interest rates, bond yields and central bank rates are also covered by the [fixed income](/projects/financetoolkit/docs/fixedincome) module, including [Euribor](/projects/financetoolkit/docs/fixedincome#get_euribor_rates), [ECB](/projects/financetoolkit/docs/fixedincome#get_european_central_bank_rates) and [Federal Reserve](/projects/financetoolkit/docs/fixedincome#get_federal_reserve_rates) rates.

## Questions & Answers
{: .heading-as-h1}

This section includes frequently asked questions and is meant to clear up confusion about certain results and/or deviations from other sources. If you have any questions that are not answered here, feel free to reach out to me via the contact details below.

> **How do you deal with companies that have different fiscal years?**

For any financial statement, I make sure to line it up with the corresponding *calendar* period. For example, Apple's Q4 2023 relates to July to September of 2023. This corresponds to the calendar period Q3 which is why I normalize Apple's numbers to Q3 2023 instead. This is done to allow for comparison between companies that have different fiscal years.

> **Why do the numbers in the financial statements sometimes deviate from the data from FinancialModelingPrep?**

When looking at a company such as Hyundai Motor Company (ticker: 005380.KS), you will notice that the financial statements are reported in KRW (South Korean won). As this specific ticker is listed on the Korean Exchange, the historical market data will also be reported in KRW. However, if you use the ticker HYMTF, which is listed on the American OTC market, the historical market data will be reported in USD. To deal with this discrepancy, the end of year or end of quarter exchange rate is retrieved which is used to convert the financial statements to USD. This is done to prevent ratio calculations such as the Free Cash Flow Yield (which is based on the market capitalization) or Price Earnings Ratio (which is based on the stock price) from being incorrect. This can be disabled by setting `convert_currency=False` in the Toolkit initialization. I recommend always using the ticker that is listed on the exchange where the company is based.

> **How can I get TTM (Trailing Twelve Months) and Growth metrics?**

Most functions will have the option to define the `trailing` parameter. This lets you define the number of periods that you want to use to calculate the trailing metrics. For example, if you want to calculate the trailing 12-month (TTM) Price-to-Earnings Ratio, you can set `trailing=4` when you have set `quarterly=True` in the Toolkit initialization. The same goes for growth metrics which can be calculated by setting `growth=True`. This will calculate the growth for each period based on the previous period. This also includes a `lag` parameter in which you can define lagged growth. Furthermore, you can also combine the trailing and growth parameters to get trailing growth. For example, set `trailing=4` and `growth=True`  for the Price-to-Earnings Ratio which will then calculate the TTM growth.

> **How can I save the data periodically so that I don't have to retrieve it every single time again?**

The Toolkit has the option to work with cached data through `use_cached_data=True` when initializing the Toolkit class. Any data that comes from an external source (financial statements, historical prices, economic indicators, and so on) is then stored in a local SQLite database and reused on the next run. Anything the Toolkit calculates itself is never cached; it is always derived from that data on demand.

The cache keeps track of what it already holds per ticker and per date range, which means changing a parameter does not throw the rest away:

- Repeating the same request retrieves nothing at all.
- Widening the period only retrieves the years that were missing.
- Adding a new ticker to an existing Toolkit only retrieves that ticker.

By default the database lives in your user configuration directory, which is the same one the MCP server uses, so both share a single cache. You can also select a specific location by providing a string to the `use_cached_data` parameter, which will store the database in the provided folder.

To see what is currently stored, use `toolkit.get_cache_contents()`. It reports the entries grouped by source and dataset:

```python
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "MSFT"], api_key="FINANCIAL_MODELING_PREP_KEY", use_cached_data=True)

toolkit.get_balance_sheet_statement()

toolkit.get_cache_contents()
```

The Finance Toolkit never clears the cache on its own, not even when its own internal structure changes. Removing data is always something you ask for explicitly with `toolkit.clear_cache()`, and it can be narrowed instead of wholesale:

```python
# Remove only the price history of a single ticker
toolkit.clear_cache(source="FinancialModelingPrep", ticker="AAPL")

# Remove everything retrieved from the OECD
toolkit.clear_cache(source="OECD")

# Remove the entire cache, which has to be confirmed
toolkit.clear_cache(confirm=True)
```

The `source` names match the ones used by the `enforce_source` parameter, so "FinancialModelingPrep" and "YahooFinance" mean the same thing in both places.

> **What is the "Benchmark" that is automatically obtained when acquiring historical data?**

This is related to the `benchmark_ticker` parameter which is set to "SPY" (S&P 500) by default. This is important when calculating performance metrics such as the Sharpe Ratio or Treynor Ratio that require a market return. This can be disabled by setting `benchmark_ticker=None` in the Toolkit initialization.

> **Data collection seems to be slow, what could be the issue?**

Generally, it should take less than 15 seconds to retrieve the historical data of 100 tickers. If it takes much longer, this could be due to reaching the API limit (the Starter plan has 250 requests per minute), due to a slow internet connection or due to unoptimized code. As the Finance Toolkit makes use of threading, initializing the Toolkit with a single ticker will result in a slow process. This is because the Toolkit will have to wait for the previous request to finish before it can start the next one. I therefore recommend initializing the Toolkit with all the tickers you want to analyze. If it is taking 10+ minutes consider having a look at [this issue](https://github.com/JerBouma/FinanceToolkit/issues/99#issuecomment-1889726000){:target="_blank"} that managed to resolve the problem.

> **Are you part of FinancialModelingPrep?**

*No, I am not*. I've merely picked them as the primary data provider given that they have a generous free tier and fair pricing compared to other providers. Therefore, any questions related to the data should go through [their contact form](https://site.financialmodelingprep.com/contact){:target="_blank"}. When it comes to any type of ratios, performance metrics, risk metrics, technical indicators or economic indicators, feel free to reach out to me as this is my own work.

{% include ft-charts-script.html %}
