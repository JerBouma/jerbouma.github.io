---
title: "Getting Started"
seo_title: "Getting Started Guide | Finance Toolkit"
seo_title_suffix: false
excerpt: "Load the Finance Toolkit, pull historical prices and financial statements, apply growth, trailing, rolling and Z-Score options, and take a tour of every module."
description: "Get started with the Finance Toolkit: load companies, historical data and financial statements, then tour each module from ratios to portfolios."
author_profile: false
permalink: /projects/financetoolkit/docs/getting-started
classes: wide-sidebar
layout: single
redirect_from:
  - /projects/financetoolkit/getting-started
sidebar:
  nav: "financetoolkit-guides"
---

The Finance Toolkit computes 500+ financial ratios, indicators and models from the underlying data with one transparent formula each, so a margin or a Sharpe ratio means the same thing for every company and every period. This guide covers the basics: loading a set of companies, retrieving their prices and financial statements, the options that work across nearly every function, and a short tour of each module. Each module has its own guide with the full depth, linked at the end of its section.

## Installation

The Finance Toolkit is on PyPI. To install or upgrade it:

```bash
pip install financetoolkit -U
```

Most data comes from Financial Modeling Prep, which needs an API key. The free plan allows 250 requests a day, five years of history and companies listed on US exchanges; the paid plans give 30+ years of annual and quarterly statements. You can get a key [through this link](/fmp){:target="_blank"}, which also gives 15% off the paid plans and supports the project. Without a key, or when a request is outside your plan, the Toolkit falls back to Yahoo Finance; set `enforce_source="FinancialModelingPrep"` to switch that off.

## Loading the Toolkit

Everything starts with a `Toolkit` instance for one or more tickers. The data is retrieved once and kept, so every ratio, model and indicator afterwards is computed from the same statements and prices without asking the data provider again. Annual statements are the default; add `quarterly=True` for quarterly statements (a paid Financial Modeling Prep plan).

To load Apple, Microsoft, Alphabet and Amazon from 2005 onwards:

```python
from financetoolkit import Toolkit

API_KEY = "FINANCIAL_MODELING_PREP_KEY"

companies = Toolkit(
    ["AAPL", "MSFT", "GOOGL", "AMZN"], api_key=API_KEY, start_date="2005-01-01"
)
```

Every example below uses this `companies` instance.

## Historical Data

`get_historical_data` returns open, high, low, close, adjusted close, volume, dividends, returns and cumulative returns for every ticker, plus the benchmark (the S&P 500 through SPY by default; change it with `benchmark_ticker`). The period can be `daily` (the default), `weekly`, `monthly`, `quarterly` or `yearly`.

To retrieve daily, yearly and quarterly prices:

```python
# Daily prices for every company and the benchmark
daily = companies.get_historical_data()

# One row per year
yearly = companies.get_historical_data(period="yearly")

# The cumulative return per quarter
cumulative_returns = companies.get_historical_data(period="quarterly")["Cumulative Return"]
```

The columns hold two levels, the field and the ticker, so `daily["Close"]` gives the closing prices of all companies and `daily.xs("AAPL", axis=1, level=1)` everything for Apple. The cumulative returns start at 1, so a value of 10 means the investment grew tenfold:

{% include ft-chart.html id="getting-started-cumulative" src="/assets/data/financetoolkit-guides/getting-started.json" label="Cumulative quarterly returns of Apple, Microsoft, Alphabet, Amazon and the S&P 500 since 2005" %}

Over this period Apple multiplied its starting value more than 250 times and Amazon about 150 times, against roughly ten times for the S&P 500.

When tickers trade on different exchanges or in different currencies, it helps to check what each one is. To see the currency, exchange and listing details of every ticker:

```python
companies.get_historical_statistics()
```

Which shows, among other fields:

|                  | AAPL       | MSFT       | GOOGL      | AMZN       |
|:-----------------|:-----------|:-----------|:-----------|:-----------|
| Currency         | USD        | USD        | USD        | USD        |
| Exchange Name    | NMS        | NMS        | NMS        | NMS        |
| Instrument Type  | EQUITY     | EQUITY     | EQUITY     | EQUITY     |
| First Trade Date | 1980-12-12 | 1986-03-13 | 2004-08-19 | 1997-05-15 |

## Financial Statements

The balance sheet, income statement and cash flow statement come back in one standardized layout for every company: the rows are the ticker and the line item, the columns the fiscal years (or quarters with `quarterly=True`). Because the line items have the same names for every company, comparing Apple's equity with Amazon's is a matter of selecting a row.

To retrieve the three statements:

```python
balance_sheet = companies.get_balance_sheet_statement()
income_statement = companies.get_income_statement()
cash_flow_statement = companies.get_cash_flow_statement()

# The balance sheet of Amazon only
balance_sheet.loc["AMZN"]

# One line item for every company
equity = balance_sheet.xs("Total Shareholder Equity", level=1)
```

The last line selects total shareholder equity for all four companies, which plotted per fiscal year gives:

{% include ft-chart.html id="getting-started-equity" src="/assets/data/financetoolkit-guides/getting-started.json" label="Total shareholder equity of Apple, Microsoft, Alphabet and Amazon per fiscal year" %}

Apple stands out: its equity peaked in 2017 and has since fallen by almost half, because its buybacks and dividends return more than it earns, while Microsoft, Alphabet and Amazon each built up several hundred billion dollars.

## Growth, Trailing, Rolling and Z-Scores

A handful of parameters work across nearly every function in the Toolkit, from the statements to the ratios, risk and performance metrics.

`growth=True` returns the period-over-period change instead of the value itself. To get the revenue growth of each company:

```python
income_statement_growth = companies.get_income_statement(growth=True)

income_statement_growth.loc[:, "Revenue", :]
```

Which gives the year-over-year revenue growth:

{% include ft-chart.html id="getting-started-revenue-growth" src="/assets/data/financetoolkit-guides/getting-started.json" label="Year-over-year revenue growth of Apple, Microsoft, Alphabet and Amazon" %}

By default growth is measured against the previous period. `lag` changes that, and a list of lags returns each of them side by side, e.g. the growth over one, two and three years. To get the growth of every income statement item over three lags:

```python
companies.get_income_statement(growth=True, lag=[1, 2, 3])
```

Three more parameters turn a single number per period into something more useful:

- **`trailing`** sums or averages a metric over the last N periods. On quarterly data `trailing=4` gives the trailing twelve months (TTM); on annual data, as here, it covers four years.
- **`standardize=True`** converts the values into a Z-Score: the number of standard deviations a value is from that company's own historical mean. It makes metrics on very different scales comparable and shows when a reading is unusual for that company.
- **`rolling`** calculates a metric over a sliding window, which turns a metric into a time series of itself. It is available in the Risk, Performance and Economics modules.

To calculate a trailing net profit margin, a standardized return on equity and a rolling 12-month beta:

```python
# Trailing: the net profit margin over the last four periods
companies.ratios.get_net_profit_margin(trailing=4)

# Standardize: the return on equity as a Z-Score
companies.ratios.get_return_on_equity(standardize=True)

# Rolling: the beta against the S&P 500 over the last 12 months
companies.performance.get_beta(period="monthly", rolling=12)
```

Which gives the three series, one per tab:

{% include ft-chart.html id="getting-started-parameters" src="/assets/data/financetoolkit-guides/getting-started.json" label="Trailing net profit margin, standardized return on equity and rolling 12-month beta" %}

The trailing margins show how far apart these businesses are: Microsoft keeps about 36 cents of every dollar of revenue, Amazon less than 7.

## Analyst Estimates and ESG Scores

Beyond the reported figures, the Toolkit also retrieves the analyst consensus for the coming years: the low, high and average estimates of revenue, EBITDA, EBIT, net income, SG&A and EPS, and the number of analysts behind each. The ESG scores give the environmental, social and governance scores per year.

To retrieve both:

```python
companies.get_analyst_estimates()

companies.get_esg_scores()
```

The earnings calendar, dividend calendar, company profiles, quotes, news and more are available in the same way; the [Toolkit reference](/projects/financetoolkit/docs) lists every function.

## Explore the Modules

The metrics are organized in modules. Most hang off the `Toolkit` (`companies.ratios`, `companies.risk` and so on) and reuse the data it already holds; `Discovery`, `Economics`, `FixedIncome` and `Portfolio` are classes of their own. Each section below gives a taste of one module and links to its guide.

### Discovery

The Discovery module finds instruments when you don't know the ticker yet: lists of stocks, ETFs, indices, cryptocurrencies, forex and commodities, a stock screener, sector performance, news, IPOs and more.

To search for a company by name and run a screen:

```python
from financetoolkit import Discovery

discovery = Discovery(api_key=API_KEY)

# Every instrument whose name matches "Apple"
discovery.search_instruments("Apple")

# US semiconductor companies worth more than $100 billion
discovery.get_stock_screener(
    industry="Semiconductors", country="US", market_cap_higher=100_000_000_000, is_etf=False
)
```

Read the [Discovery guide](/projects/financetoolkit/docs/getting-started/discovery).

### Ratios

The Ratios module covers 80+ efficiency, liquidity, profitability, solvency and valuation ratios, calculated from the statements loaded above, plus custom ratios you define yourself.

To collect every ratio at once, or a single one:

```python
# All ratios, grouped by category
companies.ratios.collect_all_ratios()

# One ratio
companies.ratios.get_effective_tax_rate()
```

Read the [Ratios guide](/projects/financetoolkit/docs/getting-started/ratios).

### Models

The Models module combines ratios and statements into complete models: the (Extended) DuPont analysis, the Weighted Average Cost of Capital, the Altman Z-Score, the Piotroski F-Score, intrinsic valuation and more.

To run the Extended DuPont analysis and the WACC:

```python
# Return on equity split into five components
companies.models.get_extended_dupont_analysis()

# The Weighted Average Cost of Capital
companies.models.get_weighted_average_cost_of_capital()
```

For Apple, the Extended DuPont analysis shows that an equity multiplier above 5 drives most of its return on equity of well over 100%.

Read the [Models guide](/projects/financetoolkit/docs/getting-started/models).

### Options

The Options module prices options with the Black-Scholes and Binomial models and calculates the Greeks for every strike price and expiration.

To price European options with Black-Scholes and American options with a binomial tree:

```python
# European options with Black-Scholes
companies.options.get_black_scholes_model()

# American options with the Binomial model
companies.options.get_binomial_model(american_option=True)
```

Read the [Options guide](/projects/financetoolkit/docs/getting-started/options).

### Technicals

The Technicals module offers 40+ technical indicators in four groups: breadth, overlap, momentum and volatility.

To collect every indicator at once, or the Bollinger Bands only:

```python
# All technical indicators
companies.technicals.collect_all_indicators()

# One indicator
companies.technicals.get_bollinger_bands()
```

Read the [Technicals guide](/projects/financetoolkit/docs/getting-started/technicals).

### Risk

The Risk module measures downside risk: Value at Risk and Conditional Value at Risk, drawdowns, the Ulcer Index, volatility, skewness, kurtosis and more.

To get the monthly Conditional Value at Risk and the yearly growth of the Ulcer Index:

```python
# Conditional Value at Risk per month
companies.risk.get_conditional_value_at_risk(period="monthly")

# The Ulcer Index per year, as growth
companies.risk.get_ulcer_index(period="yearly", growth=True)
```

Read the [Risk guide](/projects/financetoolkit/docs/getting-started/risk).

### Performance

The Performance module covers risk-adjusted returns: alpha, beta, the Sharpe, Sortino and Treynor ratios, the Capital Asset Pricing Model, the Fama-French factors and more.

To get Jensen's Alpha per quarter and the CAPM per year:

```python
# Jensen's Alpha per quarter
companies.performance.get_jensens_alpha(period="quarterly")

# The expected return under the Capital Asset Pricing Model
companies.performance.get_capital_asset_pricing_model(period="yearly")
```

Read the [Performance guide](/projects/financetoolkit/docs/getting-started/performance).

### Econometrics

The Econometrics module brings regressions, hypothesis tests, unit root and cointegration tests, panel data estimators, causal inference and forecasting to the same data. It relies on `statsmodels` and `linearmodels`, so it is installed as an extra with `pip install "financetoolkit[econometrics]" -U`.

To regress Apple's weekly returns on the other three companies and test the returns for normality:

```python
# The first ticker is the dependent variable, the others the regressors
companies.econometrics.get_ols(period="weekly")

# Are the weekly returns normally distributed?
companies.econometrics.get_jarque_bera_test(period="weekly")
```

Read the [Econometrics guide](/projects/financetoolkit/docs/getting-started/econometrics).

### Fixed Income

The Fixed Income module prices bonds and calculates their analytics, such as yields, duration and convexity, prices swaptions with the Black-76 and Bachelier models, and retrieves government bond and corporate bond yields.

To calculate the statistics of a five-year bond with a 5% coupon at a yield of 8%:

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome(start_date="2012-01-01")

fixedincome.collect_bond_statistics(
    par_value=1000,
    coupon_rate=0.05,
    years_to_maturity=5,
    yield_to_maturity=0.08,
    frequency=2,
)
```

Which gives, among others:

| Statistic           | Value  |
|:--------------------|-------:|
| Present Value       | 878.34 |
| Current Yield       | 5.69%  |
| Macaulay's Duration | 4.44   |
| Modified Duration   | 4.27   |
| DV01                | 0.38   |
| Convexity           | 21.70  |

Read the [Fixed Income guide](/projects/financetoolkit/docs/getting-started/fixed-income).

### Economics

The Economics module gives 50+ macroeconomic indicators for 60+ countries, from GDP and inflation to unemployment, interest rates and confidence indicators, independent of any ticker.

To get the consumer confidence index and the long-term interest rate of the United States, China and Germany:

```python
from financetoolkit import Economics

economics = Economics(start_date="2015-01-01")

countries = ["United States", "China", "Germany"]

economics.get_consumer_confidence_index()[countries]

economics.get_long_term_interest_rate(period="quarterly")[countries]
```

Read the [Economics guide](/projects/financetoolkit/docs/getting-started/economics).

### Portfolio

The Portfolio module analyzes your own transactions: the positions and their weights, profit and loss per transaction, performance against a benchmark and the portfolio-wide risk and performance metrics. Without a dataset it loads an example portfolio and writes the templates for your own to the working directory.

To load the example portfolio and look at its overview and transactions:

```python
from financetoolkit import Portfolio

portfolio = Portfolio(example=True, api_key=API_KEY)

# Every position, plus a weighted row for the portfolio as a whole
portfolio.get_portfolio_overview(include_portfolio=True)

# Profit and loss per transaction, first in first out
portfolio.get_transactions_overview(pnl_method="FIFO")
```

Read the [Portfolio guide](/projects/financetoolkit/docs/getting-started/portfolio).

### External Datasets

The Toolkit doesn't need Financial Modeling Prep: you can pass your own statements and prices from any source, map their line items to the Toolkit's names once with the normalization files, and every module works on them as usual.

To load your own statements:

```python
# balance_sheets, income_statements and cash_flow_statements are your own
# DataFrames, with the tickers and line items as rows and the periods as columns
companies = Toolkit(
    tickers=["TSLA", "GOOGL"],
    balance=balance_sheets,
    income=income_statements,
    cash=cash_flow_statements,
    format_location="external_datasets",
)
```

Read the [External Datasets guide](/projects/financetoolkit/docs/getting-started/external-datasets).

<div class="fs-ref"><a href="/projects/financetoolkit/docs"><i class="fas fa-book" aria-hidden="true"></i>Full reference: Finance Toolkit</a></div>

{% include ft-charts-script.html %}
