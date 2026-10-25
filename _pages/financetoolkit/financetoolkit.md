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

The sections below follow one analysis of the semiconductor sector from start to finish, where each step answers the question the previous one raises: which companies make up the sector, how their shares did, what drives their profits, how much risk came with the returns, what the option market expects next, how the economy shaped all of it, whether a fund is the better way in and how the sector fits into a diversified portfolio. Every module of the Finance Toolkit appears once, but each holds far more than shown here: 500+ methods in total, all described with examples in the [documentation](/projects/financetoolkit/docs).

### Discovering the Sector

An analysis starts with a set of companies. The [Discovery](/projects/financetoolkit/docs/discovery) module finds them without needing any tickers yet, through stock screeners, sector performance, news and lists of companies, ETFs, indices, currencies, cryptocurrencies and commodities.

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

# Show the five largest
semiconductors[["Name", "Market Cap", "Beta", "Price", "Dividend"]].head()
```

For example, the five largest companies the screener returns are shown below.

| Symbol   | Name                         |    Market Cap |   Beta |   Price |   Dividend |
|:---------|:-----------------------------|--------------:|-------:|--------:|-----------:|
| NVDA     | NVIDIA Corporation           | 5084136000000 |  2.216 |  210.96 |      0.28  |
| AVGO     | Broadcom Inc.                | 1535581254973 |  1.476 |  321.68 |      2.6   |
| MU       | Micron Technology, Inc.      |  992877621000 |  2.226 |  877.55 |      0.565 |
| AMD      | Advanced Micro Devices, Inc. |  843646776955 |  2.454 |  516.79 |      0     |
| INTC     | Intel Corp.                  |  459679713584 |  2.23  |   86.96 |      0     |

And below all of them are ranked by market cap.

{% include ft-chart.html id="discovery" label="Market capitalization of US semiconductor companies worth more than $100 billion" %}

### Following the Market

The rest of this walkthrough follows three of them: Nvidia, AMD and Intel. They are loaded into the Toolkit in one line, and the S&P 500 comes along as the benchmark:

```python
from financetoolkit import Toolkit

# Initialize the Toolkit for Nvidia, AMD and Intel from 2018 to 2025
companies = Toolkit(
    ["NVDA", "AMD", "INTC"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2017-12-31",
    end_date="2025-12-31",
)
```

[Historical data](/projects/financetoolkit/docs#get_historical_data) comes on a daily, weekly, monthly, quarterly or yearly basis, with the return and cumulative return of each period, and so do the [income statement](/projects/financetoolkit/docs#get_income_statement), [balance sheet](/projects/financetoolkit/docs#get_balance_sheet_statement) and [cash flow statement](/projects/financetoolkit/docs#get_cash_flow_statement) on an annual or quarterly basis. How far a share has travelled is one thing; whether the rally was stretched is another. The [technicals](/projects/financetoolkit/docs/technicals) module answers that with 50+ indicators, such as the Relative Strength Index (RSI), which moves between 0 and 100 and is commonly read as overbought above 70:

```python
# Obtain weekly market data for all tickers and the benchmark
historical_data = companies.get_historical_data(period="weekly")

# The 14-week Relative Strength Index
relative_strength_index = companies.technicals.get_relative_strength_index(period="weekly", window=14)

# Show the highest RSI of each year
relative_strength_index.groupby(relative_strength_index.index.start_time.year).max()
```

For example, the highest weekly RSI of each year is shown below.

|   Date |    NVDA |     AMD |    INTC |   Benchmark |
|-------:|--------:|--------:|--------:|------------:|
|   2018 | 66.1087 | 90.9719 | 66.7363 |     66.0498 |
|   2019 | 73.8156 | 81.2446 | 69.8225 |     75.9305 |
|   2020 | 85.2337 | 82.1215 | 78.4827 |     80.2378 |
|   2021 | 85.1593 | 82.0983 | 71.5862 |     74.4751 |
|   2022 | 58.4343 | 58.9426 | 61.2806 |     59.9225 |
|   2023 | 87.5129 | 77.5060 | 76.2332 |     71.4291 |
|   2024 | 91.0702 | 82.1403 | 67.6949 |     80.0566 |
|   2025 | 73.3514 | 82.5281 | 79.7429 |     71.6939 |

And below the cumulative returns of all three are plotted against the S&P 500, with the RSI in the second tab.

{% include ft-chart.html id="historical" label="Cumulative returns and 14-week RSI of Nvidia, AMD, Intel and the S&P 500" %}

### Zooming in on Competitors

Nvidia's shares outran the other two by far, which raises the question whether its business did as well. From the financial statements the Toolkit calculates 80+ [ratios](/projects/financetoolkit/docs/ratios) in five categories: efficiency, liquidity, profitability, solvency and valuation. Each ratio has its own function, and a `collect_` function returns a whole category at once:

```python
# Collect all Profitability Ratios for all tickers
profitability_ratios = companies.ratios.collect_profitability_ratios()

# Show the first ratios for Nvidia
profitability_ratios.loc["NVDA"].head()
```

For example, some of Nvidia's profitability ratios are shown below.

|                       |   2017 |   2018 |   2019 |   2020 |   2021 |   2022 |   2023 |   2024 |   2025 |
|:----------------------|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|
| Gross Margin          | 0.5993 | 0.6121 | 0.6199 | 0.6234 | 0.6493 | 0.5693 | 0.7272 | 0.7499 | 0.7107 |
| Operating Margin      | 0.3305 | 0.3247 | 0.2607 | 0.2718 | 0.3731 | 0.1566 | 0.5412 | 0.6242 | 0.6038 |
| Net Profit Margin     | 0.3137 | 0.3534 | 0.2561 | 0.2598 | 0.3623 | 0.1619 | 0.4885 | 0.5585 | 0.5560 |
| EBITDA Margin         | 0.3509 | 0.3470 | 0.2956 | 0.3376 | 0.4167 | 0.2138 | 0.5660 | 0.6385 | 0.6170 |
| Free Cash Flow Margin | 0.2995 | 0.2683 | 0.3913 | 0.2815 | 0.3021 | 0.1412 | 0.4435 | 0.4663 | 0.4477 |

And below a few of them are shown with their latest value and their course over the years.

{% include ft-chart.html id="ratios" label="Profitability ratios of Nvidia" %}

A high return on equity can come from margins, from turnover or from debt. [Models](/projects/financetoolkit/docs/models) combine the ratios to tell these apart: the [Extended DuPont Analysis](/projects/financetoolkit/docs/models#get_extended_dupont_analysis) splits the return on equity into five components that multiply into it: interest burden, tax burden, operating margin, asset turnover and equity multiplier.

```python
# Get the Extended DuPont Analysis for all tickers
extended_dupont_analysis = companies.models.get_extended_dupont_analysis()

# Show the results for Nvidia
extended_dupont_analysis.loc["NVDA"]
```

For example, the components for Nvidia are shown below.

|                         |   2017 |   2018 |   2019 |   2020 |   2021 |   2022 |   2023 |   2024 |   2025 |
|:------------------------|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|
| Interest Burden Ratio   | 0.9956 | 1.0242 | 1.0436 | 0.9729 | 0.9900 | 0.9898 | 1.0257 | 1.0316 | 1.0848 |
| Tax Burden Ratio        | 0.9534 | 1.0629 | 0.9414 | 0.9825 | 0.9810 | 1.0447 | 0.8800 | 0.8674 | 0.8488 |
| Operating Profit Margin | 0.3305 | 0.3247 | 0.2607 | 0.2718 | 0.3731 | 0.1566 | 0.5412 | 0.6242 | 0.6038 |
| Asset Turnover          | 0.9215 | 0.9551 | 0.7134 | 0.7233 | 0.7376 | 0.6319 | 1.1397 | 1.4718 | 1.3564 |
| Equity Multiplier       | 1.5931 | 1.4592 | 1.4205 | 1.5846 | 1.6775 | 1.7525 | 1.6428 | 1.4499 | 1.3456 |
| Return on Equity        | 0.4605 | 0.4926 | 0.2595 | 0.2978 | 0.4483 | 0.1793 | 0.9146 | 1.1918 | 1.0149 |

And below each component is shown for every fiscal year, multiplying into the return on equity.

{% include ft-chart.html id="models" label="Extended DuPont Analysis for Nvidia" %}

Other models include the [Weighted Average Cost of Capital](/projects/financetoolkit/docs/models#get_weighted_average_cost_of_capital), [Altman Z-Score](/projects/financetoolkit/docs/models#get_altman_z_score), [Piotroski F-Score](/projects/financetoolkit/docs/models#get_piotroski_score) and [Intrinsic Valuation](/projects/financetoolkit/docs/models#get_intrinsic_valuation). Almost every function also accepts `growth=True` for the growth from one period to the next, `trailing=4` for trailing twelve-month figures and `standardize=True` for Z-Scores.

### Weighing Risk and Return

Strong businesses do not make for smooth shares. The market data feeds the [performance](/projects/financetoolkit/docs/performance) and [risk](/projects/financetoolkit/docs/risk) modules, which calculate their metrics for any period, from intraday to yearly:

```python
# The annualized Sharpe Ratio for each year
sharpe_ratio = companies.performance.get_sharpe_ratio(period="yearly", annualize=True)

# The deepest fall within each year
maximum_drawdown = companies.risk.get_maximum_drawdown(period="yearly", within_period=True)

# Show the Sharpe Ratios
sharpe_ratio
```

For example, the yearly Sharpe Ratios are shown below.

| Date   |    NVDA |     AMD |    INTC |
|:-------|--------:|--------:|--------:|
| 2018   | -0.6130 |  1.1009 |  0.1610 |
| 2019   |  1.5458 |  1.9143 |  1.0480 |
| 2020   |  1.6560 |  1.4190 | -0.0445 |
| 2021   |  2.0003 |  1.2366 |  0.2976 |
| 2022   | -0.8393 | -1.0532 | -1.5306 |
| 2023   |  2.6986 |  1.9195 |  1.8358 |
| 2024   |  2.0851 | -0.2615 | -1.5749 |
| 2025   |  0.8325 |  1.1753 |  1.2061 |

And below both are plotted for each year, the maximum drawdown together with the S&P 500.

{% include ft-chart.html id="risk" label="Sharpe Ratio and Maximum Drawdown" %}

Together the two modules cover 70+ metrics, such as [Value at Risk](/projects/financetoolkit/docs/risk#get_value_at_risk), [GARCH](/projects/financetoolkit/docs/risk#get_garch), [Jensen's Alpha](/projects/financetoolkit/docs/performance#get_jensens_alpha), the [Capital Asset Pricing Model](/projects/financetoolkit/docs/performance#get_capital_asset_pricing_model) and the [Fama-French factors](/projects/financetoolkit/docs/performance#get_fama_and_french_model). Most of them also accept `rolling=<n>` for a value that moves through time.

### What the Option Market Expects

The past shows how much risk came with the returns; the option market puts a price on the risk ahead. The [options](/projects/financetoolkit/docs/options) module prices options with Black-Scholes, the Binomial Model and others, calculates the Greeks up to the third order and reads the live option chains: the put-call ratio, max pain, dealer gamma exposure, the volatility skew and term structure and the implied move. As the chains are those of today, the Toolkit below runs up to today:

```python
# Initialize the Toolkit up to today, as the option chains are live
companies_today = Toolkit(["NVDA", "AMD", "INTC"], api_key="FINANCIAL_MODELING_PREP_KEY")

# The volatility the options imply for the next 30 days against that of the past 30 days
companies_today.options.get_volatility_risk_premium(days=30)
```

The implied volatility is model-free, read with the method behind the VIX from all out-of-the-money options around the horizon, and the realized volatility is that of the daily returns over the same number of days. For example, both are shown below for each company.

|      |   Implied Volatility |   Realized Volatility |   Volatility Risk Premium |   Variance Risk Premium |   Implied to Realized Ratio |
|:-----|---------------------:|----------------------:|--------------------------:|------------------------:|----------------------------:|
| NVDA |               0.4845 |                0.2795 |                    0.2049 |                  0.1566 |                      1.7331 |
| AMD  |               0.6570 |                0.4980 |                    0.1590 |                  0.1836 |                      1.3192 |
| INTC |               0.6991 |                0.5196 |                    0.1795 |                  0.2188 |                      1.3456 |

Options usually price more risk than follows, as their sellers want to be paid for taking it on, and here they priced far more turbulence for the coming month than the past month delivered: Nvidia's options implied 1.7 times the volatility its shares showed. And below the implied and realized volatility of each company are plotted next to each other.

{% include ft-chart.html id="options" label="Implied and realized volatility of Nvidia, AMD and Intel" %}

### The Economic Environment

All three are listed in the United States and valued on earnings that lie years ahead, which makes US inflation and interest rates the backdrop to their share prices. In 2022, the year the maximum drawdown above shows each of them falling by more than half, inflation reached 9% and the Federal Reserve raised its policy rate from 0.12% to 4.38%.

The [economics](/projects/financetoolkit/docs/economics) module covers 60+ countries with 50+ indicators, from GDP and unemployment to money supply and interest rates, and the [fixed income](/projects/financetoolkit/docs/fixedincome) module adds bond yields, yield curves, central bank rates and bond and derivative valuations. Both are reached through the same Toolkit instance, or on their own with `from financetoolkit import Economics, FixedIncome`:

```python
# Inflation on the same month a year earlier and the Federal Reserve's policy rate
inflation_rate = companies.economics.get_inflation_rate("United States", period="monthly")
policy_rate = companies.economics.get_central_bank_policy_rate("United States", period="monthly")

# The daily U.S. Treasury par yield curve
treasury_rates = companies.fixedincome.get_treasury_rates()

# Show the curve on the last trading day of each year
treasury_rates.groupby(treasury_rates.index.year).last()
```

For example, the yield curve at the end of each year is shown below.

|   Date |   1 Month |   2 Month |   3 Month |   6 Month |   1 Year |   2 Year |   3 Year |   5 Year |   7 Year |   10 Year |   20 Year |   30 Year |
|-------:|----------:|----------:|----------:|----------:|---------:|---------:|---------:|---------:|---------:|----------:|----------:|----------:|
|   2018 |    0.0244 |    0.0245 |    0.0245 |    0.0256 |   0.0263 |   0.0248 |   0.0246 |   0.0251 |   0.0259 |    0.0269 |    0.0287 |    0.0302 |
|   2019 |    0.0148 |    0.0151 |    0.0155 |    0.0160 |   0.0159 |   0.0158 |   0.0162 |   0.0169 |   0.0183 |    0.0192 |    0.0225 |    0.0239 |
|   2020 |    0.0008 |    0.0008 |    0.0009 |    0.0009 |   0.0010 |   0.0013 |   0.0017 |   0.0036 |   0.0065 |    0.0093 |    0.0145 |    0.0165 |
|   2021 |    0.0006 |    0.0005 |    0.0006 |    0.0019 |   0.0039 |   0.0073 |   0.0097 |   0.0126 |   0.0144 |    0.0152 |    0.0194 |    0.0190 |
|   2022 |    0.0412 |    0.0441 |    0.0442 |    0.0476 |   0.0473 |   0.0441 |   0.0422 |   0.0399 |   0.0396 |    0.0388 |    0.0414 |    0.0397 |
|   2023 |    0.0560 |    0.0559 |    0.0540 |    0.0526 |   0.0479 |   0.0423 |   0.0401 |   0.0384 |   0.0388 |    0.0388 |    0.0420 |    0.0403 |
|   2024 |    0.0440 |    0.0439 |    0.0437 |    0.0424 |   0.0416 |   0.0425 |   0.0427 |   0.0438 |   0.0448 |    0.0458 |    0.0486 |    0.0478 |
|   2025 |    0.0374 |    0.0367 |    0.0367 |    0.0359 |   0.0348 |   0.0347 |   0.0355 |   0.0373 |   0.0394 |    0.0418 |    0.0479 |    0.0484 |

The curve went from almost zero at the short end in 2021 to above 4% across all maturities a year later, and when short-term yields lie above long-term ones, as at the end of 2022 and 2023, the curve is inverted. And below the yield curve at the end of each year is plotted.

{% include ft-chart.html id="economics" label="U.S. Treasury yield curve at each year end" %}

### Economic Relations

Rates rose and the shares fell, but a 10-year Treasury yield is made of two parts: the real yield, the return investors demand on top of inflation, and the inflation they expect over those ten years. The [econometrics](/projects/financetoolkit/docs/econometrics) module tells such drivers apart with regressions, tests and forecasts built on `statsmodels` and `linearmodels` (`pip install "financetoolkit[econometrics]"`). Through the Toolkit it analyzes the returns of its tickers, and on its own, through `Econometrics(data=...)`, any data at all, here the monthly returns of the three next to the monthly change in the US 10-year real yield and in 10-year inflation expectations:

```python
import pandas as pd

from financetoolkit import Econometrics

# The US 10-year real yield and inflation expectations at the end of each month
real_yield = companies.economics.get_real_yield_curve("United States", period="monthly")
inflation_expectations = companies.economics.get_breakeven_inflation_expectations(
    "United States", period="monthly"
)

# The monthly change in both next to the monthly returns
monthly_returns = companies.get_historical_data(period="monthly")["Return"][["NVDA", "AMD", "INTC"]]
monthly_returns["Real Yield"] = real_yield[("United States", "10Y")].diff()
monthly_returns["Inflation Expectations"] = inflation_expectations[("United States", "10Y")].diff()

# The data are changes already
econometrics = Econometrics(data=monthly_returns, changes=None)

# Regress the return of each company on the change in the real yield and inflation expectations
regressions = pd.concat(
    {
        ticker: econometrics.get_ols(
            dependent_ticker=ticker, independent_tickers=["Real Yield", "Inflation Expectations"]
        )
        for ticker in ["NVDA", "AMD", "INTC"]
    }
)

# Show the results for Nvidia
regressions.loc["NVDA"]
```

For example, the coefficients for Nvidia are shown below.

|                        |   Coefficient |   Std. Error |   t-Statistic |   P-Value |
|:-----------------------|--------------:|-------------:|--------------:|----------:|
| Intercept              |        0.0490 |       0.0129 |        3.7980 |    0.0003 |
| Real Yield             |      -22.7555 |       5.6650 |       -4.0169 |    0.0001 |
| Inflation Expectations |       18.0352 |       9.1127 |        1.9791 |    0.0508 |

A rise of 0.1 percentage point in the real yield went with a monthly return about 2.3% lower for Nvidia, 3.4% for AMD and 1.8% for Intel, as a higher real yield discounts their distant earnings more heavily. Inflation expectations matter far less: only for Nvidia does their coefficient come close to significance. And below each coefficient is shown with its 95% confidence interval.

{% include ft-chart.html id="econometrics" label="Coefficients of the real yield and inflation expectations with 95% confidence intervals" %}

The module also covers unit root and cointegration tests, Granger causality, panel data, causal inference, ARIMA, VAR and VECM forecasts, regime switching, a time-varying beta and pairs trading.

### Comparing the Sector's ETFs

Rather than picking three companies, a fund holds the whole industry. The [ETF](/projects/financetoolkit/docs/etf) module analyzes the holdings, sector and country weightings, tracking, concentration, overlap, valuation and liquidity of any fund. Below it compares six semiconductor funds: three focused on the United States (SOXX, XSD and PSI), one global fund (SMH) and two that hold a single country, China (SMHC) and South Korea (KCHP):

```python
# Initialize the Toolkit for six semiconductor funds
funds = Toolkit(
    ["SOXX", "XSD", "PSI", "SMH", "SMHC", "KCHP"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2017-12-31",
    end_date="2025-12-31",
)

# Where each fund invests, how concentrated it is and how much the funds hold of the same
country_weightings = funds.etf.get_country_weightings()
concentration = funds.etf.get_concentration()
overlap = funds.etf.get_overlap()

# Show the overlap between every pair of funds
overlap.round(2)
```

For example, the overlap between every pair of funds is shown below: the share of the two portfolios that is the same. Holdings are those of today, as funds publish their current holdings only.

|      |   SOXX |   XSD |   PSI |   SMH |   SMHC |   KCHP |
|:-----|-------:|------:|------:|------:|-------:|-------:|
| SOXX |   1.00 |  0.38 |  0.46 |  0.70 |   0.00 |   0.00 |
| XSD  |   0.38 |  1.00 |  0.34 |  0.28 |   0.00 |   0.00 |
| PSI  |   0.46 |  0.34 |  1.00 |  0.38 |   0.00 |   0.00 |
| SMH  |   0.70 |  0.28 |  0.38 |  1.00 |   0.00 |   0.00 |
| SMHC |   0.00 |  0.00 |  0.00 |  0.00 |   1.08 |   0.00 |
| KCHP |   0.00 |  0.00 |  0.00 |  0.00 |   0.00 |   1.00 |

The three US funds and SMH largely hold the same companies, with SOXX and SMH sharing 70% of their portfolios. SMH holds the most outside the United States, 9% in Taiwan and 6% in the Netherlands. The China and Korea funds share nothing with any other fund, which is what diversification within one sector looks like. And below the country weights of each fund are plotted.

{% include ft-chart.html id="etf-countries" label="Country weights of six semiconductor funds" %}

The overlap of every pair of funds is plotted as well.

{% include ft-chart.html id="etf-overlap" label="Overlap between six semiconductor funds" %}

### Building a Diversified Portfolio

A fund spreads the risk over the sector, but the sector still moves as one. The [portfolio](/projects/financetoolkit/docs/portfolio-optimization) module builds portfolios from the tickers of any Toolkit: minimum variance, maximum Sharpe ratio, mean-variance, risk parity, Hierarchical Risk Parity, minimum CVaR and Black-Litterman weights, the efficient frontier, risk contributions, stress tests and attribution. Below the semiconductor fund is combined with health care (XLV), energy (XLE), long-term Treasuries (TLT) and gold (GLD):

```python
# Initialize the Toolkit for funds across sectors and asset classes from 2021 to 2025
assets = Toolkit(
    ["SMH", "XLV", "XLE", "TLT", "GLD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

# The efficient frontier and the maximum Sharpe ratio portfolio, with at most 40% per asset
efficient_frontier = assets.portfolio.get_efficient_frontier(points=25, maximum_weight=0.4)
maximum_sharpe = assets.portfolio.get_maximum_sharpe_weights(maximum_weight=0.4)

# The portfolio in which every asset contributes the same share of the risk
risk_parity = assets.portfolio.get_risk_parity_weights()

# Show the risk parity portfolio
risk_parity
```

For example, the risk parity portfolio is shown below. Returns and volatilities are annualized and the risk contribution is each asset's share of the portfolio's volatility.

|           |   Weight |   Expected Return |   Volatility |   Sharpe Ratio |   Risk Contribution |
|:----------|---------:|------------------:|-------------:|---------------:|--------------------:|
| SMH       |   0.1008 |            0.3067 |       0.3508 |         0.7782 |              0.2000 |
| XLV       |   0.2358 |            0.0901 |       0.1449 |         0.3889 |              0.2000 |
| XLE       |   0.1481 |            0.2463 |       0.2672 |         0.7954 |              0.2000 |
| TLT       |   0.2750 |           -0.0748 |       0.1606 |        -0.6756 |              0.2000 |
| GLD       |   0.2403 |            0.1681 |       0.1562 |         0.8603 |              0.2000 |
| Portfolio |   1.0000 |            0.1084 |       0.1085 |         0.6888 |              1.0000 |

And below the efficient frontier is plotted with both portfolios and each asset on its own.

{% include ft-chart.html id="optimization-frontier" label="Efficient frontier with the maximum Sharpe ratio and risk parity portfolios" %}

The weights of both portfolios are plotted next to each other.

{% include ft-chart.html id="optimization-weights" label="Weights of the maximum Sharpe ratio and risk parity portfolios" %}

### Following the Portfolio

Optimal weights on paper still have to be held. The [Portfolio](/projects/financetoolkit/docs/portfolio) class follows a portfolio over time, given as weights, as the shares held, as your own transactions or as one of thirteen classic portfolios such as the 60/40 and the All Weather portfolio. Below the risk parity weights are invested at the start of 2021, brought back to their weights every year and followed up to today:

```python
from financetoolkit import Portfolio

# Invest the risk parity weights and rebalance every year
portfolio = Portfolio(
    weights=risk_parity,
    start_date="2021-01-01",
    rebalancing="yearly",
    api_key="FINANCIAL_MODELING_PREP_KEY",
)

# Get an overview of the positions against the benchmark
overview = portfolio.get_portfolio_overview()

# Show the main figures
overview[["Weight", "Return", "Benchmark Return", "Volatility", "Alpha", "Beta"]]
```

For example, the main figures of each position are shown below.

| Identifier   |   Weight |   Return |   Benchmark Return |   Volatility |   Alpha |    Beta |
|:-------------|---------:|---------:|-------------------:|-------------:|--------:|--------:|
| GLD          |   0.1969 |   0.9564 |             0.8569 |       0.2845 |  0.0995 |  0.8392 |
| SMH          |   0.1307 |   2.0911 |             0.5285 |       0.4001 |  1.5626 |  2.4046 |
| TLT          |   0.2273 |  -0.2012 |             0.7411 |       0.0960 | -0.9423 |  0.2198 |
| XLE          |   0.2034 |   1.6774 |             0.2317 |       0.2212 |  1.4457 | -0.4119 |
| XLV          |   0.2418 |   0.5476 |             0.7982 |       0.1632 | -0.2505 |  0.2560 |
| Portfolio    |   1.0000 |   1.0219 |             1.1356 |       0.1047 | -0.1137 |  0.5075 |

And below the return of each position is plotted against the return of the benchmark over the same period.

{% include ft-chart.html id="portfolio" label="Return of each position against the benchmark" %}

With `portfolio.toolkit` the portfolio, the time-weighted sum of all positions, is loaded into the Toolkit, so every metric above can be calculated for it as well.

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
