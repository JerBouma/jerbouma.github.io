---
title: Portfolio
seo_title: "Portfolio Tracking in Python | Finance Toolkit"
seo_title_suffix: false
excerpt: The Portfolio module is meant to calculate important portfolio metrics allows you to compare your own portfolio to a benchmark, seeing performance of individual assets and directly load the portfolio into the Finance Toolkit.
description: "Load your transactions, track positions and returns, including the money-weighted return, and compare a portfolio with its benchmark in Python."
author_profile: false
permalink: /projects/financetoolkit/docs/portfolio
classes: wide-sidebar
layout: single
redirect_from:
    - /portfolio
    - /projects/financetoolkit/portfolio-notebook
    - /projects/financetoolkit/portfolio-module
sidebar:
    nav: "financetoolkit-docs-portfolio"
---

The Portfolio module calculates important portfolio metrics, allowing you to compare your portfolio against a benchmark, analyze individual asset performance and load your portfolio directly into the Finance Toolkit.

To install the FinanceToolkit it simply requires the following:

```python
pip install financetoolkit -U
```

{% include docs-search.html %}

{% include financetoolkit-getting-started/portfolio.md %}

## get_presets
List the classic portfolios that ship with the Finance Toolkit, to use with `Portfolio.from_preset`.

Each is defined with real funds and the source of its allocation: the 60/40, Ray Dalio's All Weather, Harry Browne's Permanent Portfolio, the Golden Butterfly, the Bogleheads three-fund portfolio, Warren Buffett's 90/10, Nassim Taleb's barbell, a target-date glide path and more.

**Returns:**

pd.DataFrame: Per preset (by identifier) its Name, Description, Holdings,
Rebalancing and Aliases.

**As an example:**

```python
from financetoolkit import Portfolio

Portfolio.get_presets()[["Name", "Holdings", "Rebalancing"]]
```

Which returns:

|                       | Name                             | Holdings                                                                                          | Rebalancing   |
|:----------------------|:---------------------------------|:--------------------------------------------------------------------------------------------------|:--------------|
| all_weather           | All Weather                      | VTI 30.0%, TLT 40.0%, GOVT 15.0%, GLD 7.5%, DBC 7.5%                                              | quarterly     |
| balanced_60_40        | 60/40 Balanced                   | VTI 60.0%, BND 40.0%                                                                              | quarterly     |
| barbell               | Barbell                          | BIL 85.0%, VB 7.5%, VUG 7.5%                                                                      | yearly        |
| bogleheads_three_fund | Bogleheads Three-Fund            | VTI 42.0%, VXUS 18.0%, BND 40.0%                                                                  | yearly        |
| buffett_90_10         | Buffett's 90/10                  | VOO 90.0%, BIL 10.0%                                                                              | yearly        |
| conservative_income   | Conservative Multi-Country Bonds | VTI 10.0%, GOVT 40.0%, IEGA.AS 30.0%, IGLT.L 20.0%                                                | quarterly     |
| global_60_40          | Global 60/40                     | VTI 30.0%, VGK 15.0%, VWO 15.0%, GOVT 20.0%, IEGA.AS 10.0%, IGLT.L 10.0%                          | quarterly     |
| global_equity_growth  | Global Equity Growth             | VTI 30.0%, VGK 15.0%, EWJ 10.0%, VWO 15.0%, MCHI 10.0%, VUG 20.0%                                 | yearly        |
| golden_butterfly      | Golden Butterfly                 | VTI 20.0%, VBR 20.0%, TLT 20.0%, SHY 20.0%, GLD 20.0%                                             | yearly        |
| permanent_portfolio   | Permanent Portfolio              | VTI 25.0%, TLT 25.0%, BIL 25.0%, GLD 25.0%                                                        | yearly        |
| small_cap_value_tilt  | Small-Cap Value Tilt             | VB 40.0%, VTV 40.0%, GOVT 20.0%                                                                   | yearly        |
| target_date_glidepath | Target-Date Glidepath            | VTI 90.0%, BND 10.0%                                                                              | quarterly     |
| us_equity_sectors     | US Equity Sectors                | XLK 11.1%, XLF 11.1%, XLE 11.1%, XLV 11.1%, XLI 11.1%, XLY 11.1%, XLP 11.1%, XLU 11.1%, XLB 11.1% | quarterly     |

---

## from_preset
Create a Portfolio from one of the classic portfolios.

A portfolio is chosen by its identifier, name or alias (see `Portfolio.get_presets`), such as "60/40", "All Weather", "Permanent", "Golden Butterfly" or "Three Fund". It invests `initial_value` on `start_date` and rebalances as the definition says, after which every Portfolio and Toolkit analysis applies.

**Args:**

- <u>name (str):</u> The identifier, name or alias of the preset.
**kwargs: The other arguments of Portfolio, such as api_key, start_date,
initial_value, rebalancing and benchmark_ticker.

**Returns:**

Portfolio: The portfolio.

**As an example:**

```python
from financetoolkit import Portfolio

portfolio = Portfolio.from_preset(
    "Permanent Portfolio",
    start_date="2016-01-01",
    api_key="FINANCIAL_MODELING_PREP_KEY",
)

portfolio.get_portfolio_overview()
```

---

## definition
The portfolio as a `PortfolioDefinition`: the definition it was built from (a preset or weights), or, for holdings and transactions, the current weight of every position.

It can be stored with `to_yaml` and read by other tools.

**Returns:**

PortfolioDefinition: The definition.

---

## toolkit
Converts the Portfolio to a Finance Toolkit object.

This method converts the Portfolio object to a Finance Toolkit object, enabling the use of the Toolkit's 1100+ financial methods for the portfolio's assets. If the historical data of the assets or the benchmark cannot be collected, an empty DataFrame is returned instead.

The Toolkit holds the historical data of every asset, the benchmark as "Benchmark", and the Portfolio itself as the "Portfolio" ticker: its daily time-weighted total return, every day each position's total return with its weight at the previous close (purchases and sales change the weights and are no return themselves), with Close, Adj Close and Cumulative Return as an index that starts at 1 on the first day something is held. The risk metrics (volatility, Value at Risk, drawdowns and the other measures of the return distribution), the performance metrics (the Sharpe, Sortino and Treynor ratios, Beta, Jensen's Alpha, the Information Ratio, the capture ratios and the others, with the excess returns over the risk free rate and the benchmark of the Portfolio), the statistical tests of the econometrics and the technical indicators of the close are calculated on that series, so they include how the holdings move together: a stock next to its inverse fund has a low volatility and a Sharpe ratio of its own, not the average of two. The ratios of the financial statements are the weighted average of the assets' results with the portfolio weights of each period.


```python
from financetoolkit import Portfolio

portfolio = Portfolio(example=True, api_key="FINANCIAL_MODELING_PREP_KEY")

toolkit = portfolio.toolkit

toolkit.ratios.get_net_profit_margin()
```

Which returns:

|           |    2020 |   2021 |    2022 |   2023 |   2024 |
|:----------|--------:|-------:|--------:|-------:|-------:|
| AAPL      |  0.2091 | 0.2588 |  0.2531 | 0.2531 | 0.2397 |
| ALGN      |  0.7184 | 0.1953 |  0.0968 | 0.1152 | 0.1054 |
| AMD       |  0.2551 | 0.1924 |  0.0559 | 0.0377 | 0.0636 |
| AMZN      |  0.0553 | 0.071  | -0.0053 | 0.0529 | 0.0929 |
| ASML      |  0.2542 | 0.3161 |  0.2656 | 0.2844 | 0.2679 |
| AVGO      |  0.1115 | 0.2345 |  0.338  | 0.3931 | 0.1143 |
| BAC       |  0.1757 | 0.3256 |  0.2261 | 0.1446 | 0.1325 |
| BLDR      |  0.0366 | 0.0867 |  0.121  | 0.0901 | 0.0657 |
| CAMT      |  0.1397 | 0.2239 |  0.2525 | 0.2528 | 0.2787 |
| CWST      |  0.1176 | 0.0462 |  0.0489 | 0.0201 | 0.0087 |
| FICO      |  0.1826 | 0.2978 |  0.2712 | 0.2837 | 0.2986 |
| FIX       |  0.0526 | 0.0466 |  0.0594 | 0.0621 | 0.0743 |
| GOOGL     |  0.2206 | 0.2951 |  0.212  | 0.2401 | 0.286  |
| KHC       |  0.0136 | 0.0389 |  0.0892 | 0.1072 | 0.1062 |
| META      |  0.339  | 0.3338 |  0.199  | 0.2898 | 0.3791 |
| MPWR      |  0.1947 | 0.2004 |  0.2439 | 0.2347 | 0.8095 |
| MSFT      |  0.3096 | 0.3645 |  0.3669 | 0.3415 | 0.3596 |
| NFLX      |  0.1105 | 0.1723 |  0.1421 | 0.1604 | 0.2234 |
| NVDA      |  0.2598 | 0.3623 |  0.1619 | 0.4885 | 0.5585 |
| OXY       | -0.9146 | 0.0582 |  0.3428 | 0.1324 | 0.0872 |
| SKY       |  0.0597 | 0.1124 |  0.1542 | 0.0724 | 0.0799 |
| WMT       |  0.0242 | 0.0239 |  0.0191 | 0.0239 | 0.0285 |
| Portfolio |  0.2509 | 0.2266 |  0.2051 | 0.2171 | 0.2769 |

---

## read_portfolio_dataset
Read and consolidate cash flow data from Excel or CSV files into a single DataFrame.

This method consolidates portfolio data from one or more Excel or CSV files. It processes the data by identifying and handling duplicate entries, adjusting for the required date format, and renaming columns based on configuration or user inputs. It ensures consistency across transaction details, including descriptions, amounts, costs, and currencies, before returning the data as a structured DataFrame.

The function also allows for customization of the column names used in the dataset, including columns for transaction dates, asset tickers, prices, volumes, and costs/incomes. If necessary, adjustments can be made to handle duplicated entries in the dataset based on configuration settings.

**Args:**

- <u>adjust_duplicates (bool &#124; None):</u> Flag to indicate whether to adjust duplicate rows in the dataset.
Defaults to None, which uses the configuration setting.
- <u>date_column (list[str] &#124; None):</u> List of column names for date information.
Defaults to None, which uses the configuration.
- <u>date_format_options (list[str] &#124; None):</u> List of date format strings to attempt when parsing
date columns (e.g. ['%Y-%m-%d', '%d/%m/%Y']). Defaults to None, which uses the configuration.
- <u>name_columns (list[str] &#124; None):</u> List of column names for transaction descriptions.
Defaults to None, which uses the configuration.
- <u>ticker_columns (list[str] &#124; None):</u> List of column names for asset tickers.
Defaults to None, which uses the configuration.
- <u>price_columns (list[str] &#124; None):</u> List of column names for asset prices.
Defaults to None, which uses the configuration.
- <u>volume_columns (list[str] &#124; None):</u> List of column names for asset volumes.
Defaults to None, which uses the configuration.
- <u>currency_columns (list[str] &#124; None):</u> List of column names for transaction currencies.
Defaults to None, which uses the configuration.
- <u>costs_columns (list[str] &#124; None):</u> List of column names for costs or income categories.
Defaults to None, which uses the configuration.
- <u>column_mapping (dict[str, str] &#124; None):</u> Dictionary mapping dataset columns to the appropriate field names.
Defaults to None, which uses the configuration.

**Returns:**

pd.DataFrame: A DataFrame containing the consolidated and processed portfolio data.

**Raises:**

FileNotFoundError: If any of the files or directories in the portfolio dataset path cannot be found.
ValueError: If essential columns (date, description, amount) are missing in the dataset or configuration.
- Columns can be specified in the configuration or provided explicitly.
- For missing cost or income columns, an exception is raised if no valid configuration is found.

**Notes:**

- Reading the transactions again, after data was collected, starts over: the prices, the benchmark
and every overview are collected and calculated again for the transactions that are read.
- Duplicates are handled according to the adjust duplicates setting of the
configuration.
- If duplicate data is found in the combination of datasets, it will be removed to prevent double-counting.
- The date columns are converted to datetime objects, and transaction descriptions are treated as
categorical data.
- Transaction amount columns are converted to float, with support for different decimal separators.
- Cost or income columns are processed as categorical data, with optional customization.
- The dataset is sorted by the date column in ascending order, and the index is set to both
the date and ticker columns.

**As an example:**

```python
from financetoolkit import Portfolio

portfolio = Portfolio(example=True, api_key="FINANCIAL_MODELING_PREP_KEY")

portfolio.read_portfolio_dataset()
```

Which returns:

|                                      | Name   |    Price |   Volume |   Costs | Currency   |
|:-------------------------------------|:-------|---------:|---------:|--------:|:-----------|
| (Period('2024-05-14', 'D'), 'CAMT')  | CAMT   |  94.4243 |        4 |       0 | USD        |
| (Period('2024-06-11', 'D'), 'META')  | META   | 505.574  |        8 |       0 | USD        |
| (Period('2024-06-18', 'D'), 'MPWR')  | MPWR   | 847.6    |       14 |      -1 | USD        |
| (Period('2024-06-21', 'D'), 'GOOGL') | GOOGL  | 179.908  |       -2 |       0 | USD        |
| (Period('2024-07-30', 'D'), 'AMD')   | AMD    | 139.57   |        3 |       0 | USD        |
| (Period('2024-08-29', 'D'), 'AMD')   | AMD    | 146.358  |       -5 |      -2 | USD        |
| (Period('2024-10-25', 'D'), 'MCHI')  | MCHI   |  48.8436 |        6 |       0 | USD        |
| (Period('2024-11-05', 'D'), 'EMXC')  | EMXC   |  58.2921 |       -5 |      -1 | USD        |
| (Period('2024-11-13', 'D'), 'VOO')   | VOO    | 552.136  |       11 |       0 | USD        |
| (Period('2024-12-05', 'D'), 'OXY')   | OXY    |  48.2517 |       -2 |       0 | USD        |

---

## collect_benchmark_historical_data
Collect and align historical benchmark data with the portfolio's data.

The following columns are included:

- Open: the opening price for the benchmark over time.
- High: the highest price for the benchmark over time.
- Low: the lowest price for the benchmark over time.
- Close: the closing price for the benchmark over time.
- Adj Close: the adjusted closing price for the benchmark over time.
- Volume: the volume of the benchmark over time.
- Dividends: the dividends of the benchmark over time.
- Returns: the returns of the benchmark over time.
- Cumulative Return: the growth of 1 invested in the benchmark at the start, the product of (1 + Return): 1.0 on the first date and 1.25 after a 25% gain.

Volatility, Excess Return and Excess Volatility are not included here. These are available via the Risk module (e.g. toolkit.risk.get_volatility) and the Performance module (e.g. toolkit.performance.get_excess_return) instead.

This method retrieves historical benchmark data (daily and weekly) for the portfolio, based on a specified benchmark ticker or a mapping of portfolio tickers to their corresponding benchmark tickers. The retrieved benchmark data is then aligned with the portfolio's historical data, ensuring that the dates of the benchmark data match the dates of the portfolio's transactions.

The method can retrieve data for a single benchmark ticker or for multiple benchmarks depending on the portfolio tickers. The resulting benchmark data is returned in a structured DataFrame.

**Args:**

- <u>benchmark_ticker (str &#124; None):</u> The benchmark ticker symbol. Another ticker than the current
benchmark replaces it for every later method of the Portfolio, such as the Benchmark Return,
Alpha and Beta of the overviews. Defaults to None, the current benchmark: the one given to
the Portfolio, or the one of the configuration file when none was given.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: A DataFrame containing the benchmark data for the portfolio, indexed by the portfolio's dates,
or an empty DataFrame (with an error logged) when the benchmark has no historical data.

**Notes:**

- The benchmark data is retrieved in daily and weekly periods.
- The daily data is aligned to the dates of the portfolio's historical data. A date without a
benchmark quote, such as a holiday of the benchmark's exchange, carries the previous quote
forward with a return of zero, and the Return and Cumulative Return are calculated again from
the aligned Adj Close. Volume and dividends on a date missing from the portfolio's dates are
added to the next date.
- A transaction on a date without a price, such as a weekend, is matched with the benchmark's
closing price of the first following trading day, the same day its position starts on.
- When the transactions are in another currency than the benchmark, the benchmark's prices and
dividends are converted to the currency of the transactions with the daily exchange rate, so
the benchmark buys the same amount of money as the transaction. The returned data and the
weekly data are in the currency most of the portfolio's tickers are traded in.
- The method updates several internal attributes:
- `self._daily_benchmark_data`: Daily benchmark data.
- `self._weekly_benchmark_data`: Weekly benchmark data.
- `self._benchmark_prices_per_ticker`: The daily benchmark closing price in the currency of
each ticker.
- `self._benchmark_dividends_per_ticker`: The cumulative benchmark dividends per unit in the
currency of each ticker.
- `self._latest_benchmark_price`: The latest available benchmark closing price per ticker.
- `self._benchmark_specific_prices`: The benchmark closing price for each portfolio transaction.
- `self._benchmark_transaction_dividends`: The cumulative benchmark dividends per unit up to
each portfolio transaction.

**As an example:**

```python
from financetoolkit import Portfolio

portfolio = Portfolio(example=True, api_key="FINANCIAL_MODELING_PREP_KEY")

portfolio.collect_benchmark_historical_data()
```

Which returns:

| Date       |    Open |    High |     Low |   Close |   Adj Close |      Volume |   Dividends |       Return |   Cumulative Return |
|:-----------|--------:|--------:|--------:|--------:|------------:|------------:|------------:|-------------:|--------------------:|
| 2026-09-24 | 7666.99 | 7719.01 | 7662.57 | 7704.13 |     7704.13 | 5.31639e+09 |           0 | -0.000246547 |             5.34463 |
| 2026-09-25 | 7709.86 | 7752.07 | 7693.08 | 7743.41 |     7743.41 | 4.49918e+09 |           0 |  0.0050986   |             5.37188 |
| 2026-09-28 | 7721.7  | 7724.15 | 7666.6  | 7683.69 |     7683.69 | 5.12971e+09 |           0 | -0.0077124   |             5.33045 |
| 2026-09-29 | 7699.6  | 7699.6  | 7653.55 | 7670.84 |     7670.84 | 5.02359e+09 |           0 | -0.00167239  |             5.32154 |
| 2026-09-30 | 7688.99 | 7722.88 | 7651.54 | 7651.54 |     7651.54 | 4.27655e+09 |           0 | -0.002516    |             5.30815 |
| 2026-10-01 | 7666.47 | 7684.75 | 7616.78 | 7666.45 |     7666.45 | 5.7838e+09  |           0 |  0.00194865  |             5.31849 |
| 2026-10-02 | 7726.24 | 7754.67 | 7700.51 | 7722.72 |     7722.72 | 5.27743e+09 |           0 |  0.00733977  |             5.35753 |
| 2026-10-05 | 7730.86 | 7794.35 | 7727.59 | 7773.95 |     7773.95 | 5.8409e+09  |           0 |  0.00663367  |             5.39307 |
| 2026-10-06 | 7805.96 | 7844.52 | 7805.96 | 7818.93 |     7818.93 | 5.01965e+09 |           0 |  0.00578599  |             5.42428 |
| 2026-10-07 | 7792.98 | 7807.02 | 7763.34 | 7801.77 |     7801.77 | 5.11115e+09 |           0 | -0.0021947   |             5.41237 |

---

## collect_historical_data
Collect and adjust historical price data for the portfolio's tickers.

The following columns are included:

- Open: the opening price of each asset over time.
- High: the highest price of each asset over time.
- Low: the lowest price of each asset over time.
- Close: the closing price of each asset over time.
- Adj Close: the adjusted closing price of each asset over time.
- Volume: the volume of each asset over time.
- Dividends: the dividends of each asset over time.
- Returns: the returns of each asset over time.
- Cumulative Return: the growth of 1 invested in each asset at the start, the product of (1 + Return): 1.0 on the first date and 1.25 after a 25% gain.

Volatility, Excess Return and Excess Volatility are not included here. These are available via the Risk module (e.g. toolkit.risk.get_volatility) and the Performance module (e.g. toolkit.performance.get_excess_return) instead.

This method retrieves historical price data (daily and weekly) for the portfolio's tickers and adjusts for any currency mismatches if necessary. It fetches data from a specified data source, applies currency conversion where applicable, and stores the adjusted data in separate DataFrames for the daily and weekly periods.

The method uses the Toolkit class to fetch historical price data and the Currency Toolkit to handle currency conversions if the portfolio’s transaction currency does not match the historical data's currency.

**Args:**

- <u>rounding (int &#124; None, optional):</u> An optional integer specifying the number of decimal places to round the
historical price data. If None, the default rounding value is used. Defaults to None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: A DataFrame containing the adjusted daily historical price data for the portfolio.

**Notes:**

- This method utilizes the `Toolkit` class to fetch historical price data for different periods.
- Currency adjustments are made if there's a mismatch between the transaction and historical data currencies.
- The method handles ISIN-to-ticker mapping when ISIN codes are provided in the portfolio data.
- The adjusted historical data is stored in separate DataFrames for daily and weekly price data.
- If any currency mismatch is found between the portfolio's transaction and historical data,
a warning message is displayed.
- The method rounds the data according to the specified or default rounding precision.
- The latest closing price of every ticker, carried forward over a holiday of its exchange, is
also captured and available in the `self._latest_price` attribute.
- If currency conversions are applied, a warning is displayed when mismatches between transaction and
historical data currencies are found (e.g., for ISIN codes).

**As an example:**

```python
from financetoolkit import Portfolio

portfolio = Portfolio(example=True, api_key="FINANCIAL_MODELING_PREP_KEY")

portfolio.collect_historical_data()
```

Which returns:

|            |   ('Open', 'ASML') |   ('Open', 'SKY') |   ('Open', 'AMZN') |   ('Open', 'FIX') |   ('Open', 'MSFT') |   ('Open', 'AMD') |   ('Open', 'AAPL') |
|:-----------|-------------------:|------------------:|-------------------:|------------------:|-------------------:|------------------:|-------------------:|
| 2026-09-24 |            1708.85 |             85.38 |             246.02 |           1584    |             495.07 |            600.27 |             336.72 |
| 2026-09-25 |            1741.25 |             85.91 |             248.56 |           1656.27 |             499.04 |            634.54 |             336.04 |
| 2026-09-28 |            1748.82 |             86.83 |             246.63 |           1655.82 |             505.47 |            624.9  |             340.37 |
| 2026-09-29 |            1811.51 |             87.41 |             246.71 |           1681.64 |             508.31 |            616.74 |             336.97 |
| 2026-09-30 |            1828.6  |             85.85 |             246.79 |           1677.78 |             511.61 |            609.89 |             330.8  |
| 2026-10-01 |            1799.1  |             84.62 |             251.61 |           1658    |             519.88 |            612.7  |             330    |
| 2026-10-02 |            1849.74 |             89.57 |             251.51 |           1714.05 |             519.39 |            635.95 |             333.26 |
| 2026-10-05 |            1852.53 |             87.53 |             250.19 |           1723.93 |             521.62 |            630.61 |             332.82 |
| 2026-10-06 |            1870    |             85.9  |             253.4  |           1725    |             531.68 |            648.04 |             332.28 |
| 2026-10-07 |            1788.92 |             84.2  |             254.23 |           1770.01 |             530.73 |            634.77 |             336.96 |

---

## get_positions_overview
Calculate and provide an overview of the portfolio's positions, including key statistics and performance metrics.

The following columns are included:

- Volume: the net volume of each asset over time, i.e. every buy minus every sell.
- Costs: the cumulative transaction costs of each asset over time.
- Invested Amount: the cumulative capital deployed over time, i.e. the value of every buy plus the absolute transaction costs. Sale proceeds are not netted off.
- Realized Proceeds: the cumulative cash received from selling units of the asset over time.
- Dividends: the cumulative cash dividends received over time, i.e. on every ex-dividend date the units held at the previous close times the dividend per unit.
- Current Value: the market value of the position still held, marked at the closing price of that day.
- Cumulative Return: the total return on the capital deployed, i.e. (Current Value + Realized Proceeds + Dividends - Invested Amount) / Invested Amount: a return, 0.25 after a 25% gain (unlike the Cumulative Return of the historical data, the growth of 1). It is NaN before the first purchase, when no capital has been deployed yet.
- Invested Weight: the weight of the asset in the portfolio based on the invested amount over time.
- Current Weight: the weight of the asset in the portfolio based on the current value over time.

Positions are marked at the traded closing price, the basis of the transaction prices, and the dividends are added as cash when they are paid, so the cumulative return is a total return and "Current Value" is the market value quoted on that date.

A transaction booked on a day without a price, such as a weekend or an exchange holiday, is carried forward to the first following day that does have one.

This method computes an overview of the portfolio's positions by calculating important statistics and performance metrics based on the historical data and transactions. If necessary data has not been collected, it will trigger the collection of historical and benchmark data using the `collect_historical_data` and `collect_benchmark_historical_data` methods. Additionally, it will compute an overview of transactions using the `get_transactions_overview` method.

The resulting overview includes information about the positions, such as the value, performance, and other key metrics. The data is rounded to the specified precision before being returned.

**Args:**

- <u>rounding (int &#124; None, optional):</u> An optional integer specifying the number of decimal places to round the data.
If None, the default rounding precision is used. Defaults to None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: A DataFrame containing an overview of the portfolio's positions, with key statistics and
performance metrics.

**Raises:**

Exception: If data collection for historical or benchmark data fails, or if the positions overview cannot
be created. Specific error messages will be raised for each failure.

**Notes:**

- This method ensures that all necessary data is available before calculating the positions overview.
- The method handles the collection of missing data (historical, benchmark, and transactions) automatically.
- The positions overview is calculated based on portfolio tickers, transaction data,
and historical price data.
- The resulting overview DataFrame is rounded to the specified or default precision.

**As an example:**

```python
from financetoolkit import Portfolio

portfolio = Portfolio(example=True, api_key="FINANCIAL_MODELING_PREP_KEY")

portfolio.get_positions_overview()
```

Which returns:

|            |   ('Volume', 'ASML') |   ('Volume', 'SKY') |   ('Volume', 'AMZN') |   ('Volume', 'FIX') |   ('Volume', 'MSFT') |   ('Volume', 'AMD') |
|:-----------|---------------------:|--------------------:|---------------------:|--------------------:|---------------------:|--------------------:|
| 2026-09-24 |                  129 |                 126 |                  116 |                 122 |                  105 |                  78 |
| 2026-09-25 |                  129 |                 126 |                  116 |                 122 |                  105 |                  78 |
| 2026-09-28 |                  129 |                 126 |                  116 |                 122 |                  105 |                  78 |
| 2026-09-29 |                  129 |                 126 |                  116 |                 122 |                  105 |                  78 |
| 2026-09-30 |                  129 |                 126 |                  116 |                 122 |                  105 |                  78 |
| 2026-10-01 |                  129 |                 126 |                  116 |                 122 |                  105 |                  78 |
| 2026-10-02 |                  129 |                 126 |                  116 |                 122 |                  105 |                  78 |
| 2026-10-05 |                  129 |                 126 |                  116 |                 122 |                  105 |                  78 |
| 2026-10-06 |                  129 |                 126 |                  116 |                 122 |                  105 |                  78 |
| 2026-10-07 |                  129 |                 126 |                  116 |                 122 |                  105 |                  78 |

---

## get_portfolio_overview
Calculate and provide an overview of the portfolio's key statistics, including performance metrics and cost-related information.

The following columns are included:

- Identifier: The name of the asset, specifically the ticker (e.g. AAPL)
- Volume: The net volume of the asset, i.e. every buy minus every sell.
- Costs: The total costs associated with the asset transactions.
- Price: The volume-weighted average price paid for the units that were bought. Sells do not enter this figure, so it stays a purchase price rather than a net cash figure.
- Invested: The total capital deployed in the asset, i.e. the value of every buy plus the absolute transaction costs. Sale proceeds are deliberately not netted off, because a denominator that shrinks with every profitable sale inflates the reported return and flips its sign once more cash has come out than went in.
- Latest Price: The latest closing price of the asset obtained from historical data.
- Latest Value: The market value of the position still held, i.e. Volume times Latest Price.
- Dividends: The cash dividends received on the units held on every ex-dividend date.
- Return: The total return on the capital deployed, i.e. Return Value divided by Invested. This covers realized and unrealized results and the dividends together and is NaN when nothing was invested. The "Portfolio" row divides by the capital contributed to the portfolio instead: the peak of the cumulative net contribution, i.e. every buy plus the costs minus the sale proceeds and the dividends received up to that date, summed over the assets per date. The buys of a rebalancing are paid for by the sells and dividends of the portfolio itself, so a portfolio that invests 10,000 once has 10,000 of capital however often it is rebalanced, while its "Invested" adds up every rebalancing buy. A portfolio of buys has its "Invested" as its capital, less the part of a later buy that a dividend received before it paid for.
- Return Value: The absolute profit or loss, i.e. Latest Value plus all sale proceeds plus Dividends minus Invested. This equals realized PnL plus unrealized PnL plus dividends minus the transaction costs, where the realized PnL is the figure reported by get_transactions_overview.
- Benchmark Return: The return the identical cash flows would have produced in the benchmark. Every transaction buys or sells benchmark units at the benchmark's closing price for the exact cash amount of that transaction on that date, so the comparison is matched in money rather than in share count, and the benchmark's dividends are received as cash as well. The "Portfolio" row divides by the same capital as its Return, so its Alpha compares like with like.
- Volatility: The annualized volatility of the asset's daily returns over the most recent 252 trading days. For the aggregated "Portfolio" row, this is derived from the full covariance matrix of the underlying asset returns over the same days ($$\operatorname{Var}_{p} = w^{T} \cdot \operatorname{Cov} \cdot w$$, Markowitz, 1952) rather than a weighted average of individual volatilities, since the latter ignores diversification from imperfectly correlated assets.
- Benchmark Volatility: The annualized volatility of the benchmark's daily returns over the most recent 252 trading days.
- Alpha: The alpha is based on the difference between the asset's return and the benchmark return.
- Beta: The beta of the asset's daily returns against the benchmark's over the most recent 252 trading days, the window of the Volatility column. A beta >1 indicates that the asset is more volatile than the benchmark and a beta <1 indicates that the asset is less volatile than the benchmark.
- Weight: The weight of the asset in the portfolio based on the latest market value and the total market value of the portfolio. With short positions the total is the net value, so a weight can be negative or above 1.

Positions are valued at the traded closing price, the basis of the transaction prices, and dividends are added as cash, for the asset and the benchmark alike, so Return and Benchmark Return are total returns on the same basis.

No inventory method (FIFO, LIFO or average cost) is applied here: "Return" measures the result of every unit of currency put into the position rather than the basis of the units that happen to remain. The inventory methods drive the realized PnL in get_transactions_overview instead.

The "Portfolio" row sums or averages units of different assets for "Volume", "Price" and "Latest Price", so those three carry no economic meaning at the portfolio level.

Units held of an asset without a price, such as a ticker without data, are worth an unknown amount rather than nothing. The value of the portfolio is then unknown, so every "Weight" and the "Portfolio" row's value, return, alpha, volatility and beta are NaN; its "Invested", "Costs" and "Dividends" remain.

When recalculating these numbers, it is important to note that results are calculated before the rounding parameter is applied which can lead to some discrepancies in the results.

This method computes a detailed overview of the portfolio, calculating various key statistics such as performance, costs, and returns. If necessary data has not been collected, it will automatically trigger data collection using the `collect_historical_data` and `collect_benchmark_historical_data` methods. The portfolio overview is generated based on the portfolio dataset and benchmark data, and is rounded to the specified precision before being returned.

**Args:**

- <u>include_portfolio (bool):</u> A boolean flag indicating whether the portfolio itself should be included
in the overview. Defaults to `True`.
- <u>exclude_sold_positions (bool):</u> A flag indicating whether to exclude sold positions from the overview,
those whose sales add up to their purchases. Open positions stay, long or short, and so does the
Portfolio row while any position is open. Defaults to True.
- <u>rounding (int &#124; None, optional):</u> An optional integer specifying the number of decimal places to round the data.
If None, the default rounding precision is used. Defaults to None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: A DataFrame containing key statistics and an overview of the portfolio, including
performance metrics, costs, and returns.

**Raises:**

ValueError: If data collection for historical or benchmark data fails.
ValueError: If the creation of the portfolio overview fails.

**Notes:**

- This method ensures that all necessary data is available before calculating the portfolio overview.
- The method handles the collection of missing data (historical, benchmark) automatically.
- The portfolio overview includes important metrics such as returns, costs, and volume, and
is based on both the portfolio's dataset and benchmark data.
- The resulting DataFrame is rounded to the specified or default precision.

**As an example:**

```python
from financetoolkit import Portfolio

portfolio = Portfolio(example=True, api_key="FINANCIAL_MODELING_PREP_KEY")

portfolio.get_portfolio_overview()
```

Which returns:

| Identifier   |   Volume |   Costs |    Price |   Invested |   Latest Price |   Latest Value |   Dividends |   Return |   Return Value |   Benchmark Return |   Volatility |   Benchmark Volatility |   Alpha |    Beta |   Weight |
|:-------------|---------:|--------:|---------:|-----------:|---------------:|---------------:|------------:|---------:|---------------:|-------------------:|-------------:|-----------------------:|--------:|--------:|---------:|
| MPWR         |      116 |     -27 | 250.893  |  30636     |       1314     |      152424    |   3301.39   |   4.0978 |     125539     |             0.7169 |       0.5874 |                 0.1374 |  3.3809 |  2.6395 |   0.163  |
| MSFT         |      105 |     -11 |  50.1726 |   5529.99  |        517.99  |       54388.9  |   3367.52   |   9.4709 |      52374.2   |             3.2604 |       0.3393 |                 0.1374 |  6.2105 |  1.0243 |   0.0582 |
| NFLX         |      114 |     -32 |  13.0791 |   1666.89  |         60.75  |        6925.5  |      0      |   3.2816 |       5470.13  |             1.3201 |       0.3632 |                 0.1374 |  1.9616 |  0.292  |   0.0074 |
| NVDA         |       69 |     -27 |   2.1717 |    202.909 |        156.14  |       10773.7  |     49.6373 |  52.4962 |      10651.9   |             1.004  |       0.388  |                 0.1374 | 51.4922 |  1.7966 |   0.0115 |
| OXY          |       27 |     -15 |  52.3833 |   2005.56  |         57.36  |        1548.72 |    876.061  |   0.4264 |        855.115 |             2.6148 |       0.3558 |                 0.1374 | -2.1884 | -0.6839 |   0.0017 |
| SKY          |      126 |     -23 |  24.4134 |   3343.23  |         92.02  |       11594.5  |    901.062  |   2.8171 |       9418.34  |             4.6739 |       0.4394 |                 0.1374 | -1.8567 |  1.1355 |   0.0124 |
| VOO          |       77 |     -12 | 256.027  |  20238.2   |        680.26  |       52380    |   3925.88   |   1.8004 |      36436.5   |             1.606  |       0.1368 |                 0.1374 |  0.1944 |  0.994  |   0.056  |
| VSS          |       98 |     -21 |  94.9125 |  10366.5   |        144.89  |       14199.2  |   3069.98   |   0.7621 |       7900.4   |             2.3488 |       0.175  |                 0.1374 | -1.5867 |  1.0539 |   0.0152 |
| WMT          |       92 |     -18 |  22.2477 |   2265.02  |        128.41  |       11813.7  |    965.737  |   4.716  |      10681.8   |             3.2913 |       0.2686 |                 0.1374 |  1.4248 | -0.06   |   0.0126 |
| Portfolio    |     2142 |    -532 |  55.8595 | 134818     |        436.564 |      935121    |  31003.8    |   8.0831 |     839982     |             2.3122 |       0.2971 |                 0.1374 |  5.7709 |  1.7916 |   1      |

---

## get_portfolio_performance
Calculate portfolio performance metrics for a specified period: each position and the Portfolio at the end of every period.

The Return is the total return on the capital deployed since the purchase, as of the end of the period, not the return within the period (`get_return_contributions` gives that per period).

This method calculates key performance metrics, such as returns, for the portfolio over a specified period, from daily to yearly. It uses the positions overview dataset for these calculations. If the necessary data has not been collected, it triggers the collection of historical and benchmark data.

**Args:**

- <u>period (str &#124; None):</u> The time period for which portfolio performance metrics should be calculated.
Options are: "daily", "weekly", "monthly", "quarterly", "yearly". Defaults to None, which is
"quarterly" when the Portfolio is quarterly and "yearly" otherwise.
- <u>exclude_sold_positions (bool):</u> A flag indicating whether to exclude the periods in which a position was
sold, its sales adding up to its purchases. Open positions stay, long or short. Defaults to True.
- <u>rounding (int &#124; None):</u> The number of decimal places to round the output to.
If None, it defaults to the rounding precision specified in the configuration.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: A DataFrame containing the portfolio performance metrics for the specified period.

**Raises:**

InvalidArgumentError: If the period is not one of the options.
ValueError: If there is an issue with collecting historical data or creating the portfolio performance.

**Notes:**

- This method ensures that the required historical and benchmark data is available before calculating
performance.
- The method uses the `overview_model.create_portfolio_performance` function to compute performance metrics.
- The resulting DataFrame will be rounded to the specified number of decimal places
(or the default configuration).

**As an example:**

```python
from financetoolkit import Portfolio

portfolio = Portfolio(example=True, api_key="FINANCIAL_MODELING_PREP_KEY")

portfolio.get_portfolio_performance(period='weekly')
```

Which returns:

|                                                    |   Volume |   Costs |   Invested Amount |   Realized Proceeds |   Dividends |   Current Value |   Invested Weight |   Current Weight |   Return |
|:---------------------------------------------------|---------:|--------:|------------------:|--------------------:|------------:|----------------:|------------------:|-----------------:|---------:|
| (Period('2026-10-05/2026-10-11', 'W-SUN'), 'META') |       15 |      -1 |          4813.61  |               0     |     81.125  |        10780    |            0.0357 |           0.0099 |   1.2563 |
| (Period('2026-10-05/2026-10-11', 'W-SUN'), 'MPWR') |      116 |     -27 |         30636     |             449.4   |   3301.39   |       160810    |            0.2272 |           0.147  |   4.3715 |
| (Period('2026-10-05/2026-10-11', 'W-SUN'), 'MSFT') |      105 |     -11 |          5529.99  |             147.7   |   3367.52   |        56182.4  |            0.041  |           0.0513 |   9.7952 |
| (Period('2026-10-05/2026-10-11', 'W-SUN'), 'NFLX') |      114 |     -32 |          1666.89  |             211.515 |      0      |         8014.2  |            0.0124 |           0.0073 |   3.9348 |
| (Period('2026-10-05/2026-10-11', 'W-SUN'), 'NVDA') |       69 |     -27 |           202.909 |              31.547 |     49.6373 |        15820.3  |            0.0015 |           0.0145 |  77.3678 |
| (Period('2026-10-05/2026-10-11', 'W-SUN'), 'OXY')  |       27 |     -15 |          2005.56  |             435.898 |    876.061  |         1622.97 |            0.0149 |           0.0015 |   0.4634 |
| (Period('2026-10-05/2026-10-11', 'W-SUN'), 'SKY')  |      126 |     -23 |          3343.23  |             265.99  |    901.062  |        10033.4  |            0.0248 |           0.0092 |   2.3502 |
| (Period('2026-10-05/2026-10-11', 'W-SUN'), 'VOO')  |       77 |     -12 |         20238.2   |             368.76  |   3925.88   |        55100.4  |            0.1501 |           0.0504 |   1.9348 |
| (Period('2026-10-05/2026-10-11', 'W-SUN'), 'VSS')  |       98 |     -21 |         10366.5   |             997.66  |   3069.98   |        15201.8  |            0.0769 |           0.0139 |   0.8588 |
| (Period('2026-10-05/2026-10-11', 'W-SUN'), 'WMT')  |       92 |     -18 |          2265.02  |             167.39  |    965.737  |        10244.2  |            0.0168 |           0.0094 |   4.0231 |

---

## get_transactions_overview
Calculate and collect transaction overview ratios based on the provided data.

This method calculates various transaction overview ratios, such as returns, costs, and profit & loss (PnL), based on the transaction dataset. The calculated ratios are added as new columns to the portfolio dataset. It also provides the option to use different methods for calculating PnL (FIFO, LIFO, or AVERAGE). The method ensures that necessary historical and benchmark data is available before performing calculations.

**Args:**

- <u>rounding (int &#124; None):</u> The number of decimal places to round the output to.
If None, it defaults to the rounding specified in the configuration.
- <u>exclude_sold_positions (bool):</u> Whether to leave out the sell transactions. Profit & loss
is realized when shares are sold, so it is booked on the sell transactions: with
True, every remaining (buy) transaction shows a PnL of 0 and the realized total is
in the Cumulative PnL column. Pass False to see the PnL of each sale. Defaults to True.
- <u>pnl_method (str):</u> The method for calculating profit & loss. Options are: "FIFO" (first in, first out:
the oldest lots close first), "LIFO" (last in, first out: the newest lots close first), "AVERAGE"
(every sale at the average cost of the units held). Defaults to "FIFO". The purchases of a day come
before its sales, unless the dates of the transactions include a time of day ("%Y-%m-%d %H:%M:%S"),
which orders them within the day.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The portfolio dataset with added transaction overview ratios and PnL columns.

**Raises:**

ValueError: If there is an issue with collecting historical data, creating the transaction overview,
or if an invalid PnL method is provided.

**Notes:**

- The method first checks and collects necessary historical data if not already available.
- It uses the `overview_model.create_transactions_overview` and
`overview_model.create_profit_and_loss_overview` functions to calculate the transaction ratios
and profit & loss.
- The transaction ratios and PnL are added to the original portfolio dataset as new columns.
- "PnL" is the realized result of a sell transaction under the chosen inventory method and
is zero on every buy. "Cumulative PnL" is the running realized total per ticker and
restarts at zero for the next ticker rather than carrying across the portfolio.
- Transaction costs are deliberately excluded from the PnL. They are carried by the
invested amount instead, so a cost is never counted in two places. The identity
Return Value = realized PnL + unrealized PnL + dividends - transaction costs therefore ties
this output back to get_portfolio_overview exactly.
- "Invested Amount" is per transaction and is negative on a sell, since it is the cash
movement of that one transaction rather than the capital deployed in the position.
- "Current Value" values the units of a buy at the latest closing price and "Dividends" holds
the cash dividends paid on them since the transaction, so "% Return" and "Return" are total
returns of the units bought. A sell has no current value, dividends or return; its result
is the PnL.
- If no rounding is provided, the rounding precision specified in the configuration is used.

**As an example:**

```python
from financetoolkit import Portfolio

portfolio = Portfolio(example=True, api_key="FINANCIAL_MODELING_PREP_KEY")

portfolio.get_transactions_overview()
```

Which returns:

|                                      | Name   |   Price |   Volume |   Costs | Currency   |   Invested Amount |   Current Value |   Dividends |   % Return |    Return |   PnL |   Cumulative PnL |
|:-------------------------------------|:-------|--------:|---------:|--------:|:-----------|------------------:|----------------:|------------:|-----------:|----------:|------:|-----------------:|
| (Period('2024-02-01', 'D'), 'GOOGL') | GOOGL  |  141.16 |       14 |       0 | USD        |           1976.24 |         4482.94 |     29.12   |     1.2832 | 2535.82   |     0 |           0      |
| (Period('2024-02-12', 'D'), 'BAC')   | BAC    |   33.62 |        5 |      -3 | USD        |            171.1  |          252.8  |     14.8    |     0.564  |   96.5    |     0 |          22.7994 |
| (Period('2024-02-22', 'D'), 'MCHI')  | MCHI   |   39.77 |        7 |      -1 | USD        |            279.39 |          343    |     18.9952 |     0.2957 |   82.6052 |     0 |         -19.26   |
| (Period('2024-03-12', 'D'), 'MPWR')  | MPWR   |  736.55 |       11 |       0 | USD        |           8102.05 |        12541.3  |    189.64   |     0.5713 | 4628.91   |     0 |         399.48   |
| (Period('2024-05-14', 'D'), 'CAMT')  | CAMT   |   94.11 |        4 |       0 | USD        |            376.44 |          484.64 |      0      |     0.2874 |  108.2    |     0 |         102.7    |
| (Period('2024-06-11', 'D'), 'META')  | META   |  507.47 |        8 |       0 | USD        |           4059.76 |         5140.96 |     41.4    |     0.2765 | 1122.6    |     0 |           0      |
| (Period('2024-06-18', 'D'), 'MPWR')  | MPWR   |  852.56 |       14 |      -1 | USD        |          11936.8  |        15961.7  |    223.86   |     0.3559 | 4248.7    |     0 |         399.48   |
| (Period('2024-07-30', 'D'), 'AMD')   | AMD    |  138.44 |        3 |       0 | USD        |            415.32 |         1550.37 |      0      |     2.733  | 1135.05   |     0 |          13.3825 |
| (Period('2024-10-25', 'D'), 'MCHI')  | MCHI   |   49.85 |        6 |       0 | USD        |            299.1  |          294    |     15.138  |     0.0336 |   10.038  |     0 |         -19.26   |
| (Period('2024-11-13', 'D'), 'VOO')   | VOO    |  549.03 |       11 |       0 | USD        |           6039.33 |         7684.38 |    159.099  |     0.2987 | 1804.15   |     0 |         140.84   |

---

## get_transactions_performance
Calculate transaction performance metrics for a specified period.

This method calculates per asset and period how the units bought in that period performed up to the end of the period, next to the return the identical purchases would have made in the benchmark. The following columns are included:

- Volume: the net volume traded in the period, i.e. buys minus sells.
- Price: the volume-weighted average price paid for the units bought in the period.
- Costs: the transaction costs of the period, of buys and sells.
- Invested Amount: the value of the units bought plus the costs of those buys.
- Realized Proceeds: the cash received from sales in the period.
- Current Value: the units bought in the period at the closing price at the end of the period.
- Dividends: the cash dividends those units received up to the end of the period.
- Return: (Current Value + Dividends - Invested Amount) / Invested Amount, NaN in a period without purchases.
- Benchmark Return: the same return for benchmark units bought with the same money on the same dates, dividends included.
- Alpha: Return minus Benchmark Return.

Sales are reported but left out of the return: the units sold in a period were usually bought in an earlier one, and their proceeds would credit this period's purchases with the gains of earlier ones. Units are valued at the traded closing price and receive their dividends as cash.

**Args:**

- <u>period (str &#124; None, optional):</u> The time period for which transaction performance metrics should be
calculated. Options are: "daily", "weekly", "monthly", "quarterly", "yearly". Defaults to None,
which is "quarterly" when the Portfolio is quarterly and "yearly" otherwise.
- <u>exclude_sold_positions (bool):</u> Whether to leave out the periods without an
invested amount, those in which only units bought earlier were sold, and those whose only
purchases cost nothing (a price of 0), which have no return to measure. Defaults
to True.
- <u>rounding (int &#124; None):</u> The number of decimal places to round the output to.
If None, it defaults to the rounding specified in the configuration.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: A DataFrame containing transaction performance metrics, including
returns, costs, and benchmarks, for the specified period.

**Raises:**

InvalidArgumentError: If the period is not one of the options.
ValueError: If there is an issue with creating the transaction performance metrics.

**Notes:**

- The method supports every period from daily to yearly for calculating transaction
performance metrics.
- If no period is provided, it defaults to quarterly or yearly based on the
configuration.
- The end-of-period prices and dividends are taken from the daily data, in the currency of
each ticker's transactions for the asset and the benchmark alike.
- A transaction on a day without a price, such as a weekend, belongs to the period of the
next trading day, the day it is priced on and receives dividends from; a transaction after
the last date belongs to the period of the last date.
- If no rounding is specified, the rounding precision from the configuration is used.

**As an example:**

```python
from financetoolkit import Portfolio

portfolio = Portfolio(example=True, api_key="FINANCIAL_MODELING_PREP_KEY")

portfolio.get_transactions_performance(period='quarterly')
```

Which returns:

|                                      |   Volume |   Price |   Costs |   Invested Amount |   Realized Proceeds |   Current Value |   Dividends |   Return |   Benchmark Return |   Alpha |
|:-------------------------------------|---------:|--------:|--------:|------------------:|--------------------:|----------------:|------------:|---------:|-------------------:|--------:|
| (Period('2023Q4', 'Q-DEC'), 'MCHI')  |       15 |   43.29 |      -3 |            652.35 |                   0 |          611.1  |     14.912  |  -0.0404 |             0.0856 | -0.1259 |
| (Period('2024Q1', 'Q-DEC'), 'BAC')   |        5 |   33.62 |      -3 |            171.1  |                   0 |          189.6  |      1.2    |   0.1151 |             0.028  |  0.0872 |
| (Period('2024Q1', 'Q-DEC'), 'GOOGL') |       14 |  141.16 |       0 |           1976.24 |                   0 |         2113.02 |      0      |   0.0692 |             0.071  | -0.0018 |
| (Period('2024Q1', 'Q-DEC'), 'MCHI')  |        7 |   39.77 |      -1 |            279.39 |                   0 |          278.11 |      0      |  -0.0046 |             0.0292 | -0.0338 |
| (Period('2024Q1', 'Q-DEC'), 'MPWR')  |       11 |  736.55 |       0 |           8102.05 |                   0 |         7451.62 |     13.75   |  -0.0786 |             0.0153 | -0.0939 |
| (Period('2024Q2', 'Q-DEC'), 'CAMT')  |        4 |   94.11 |       0 |            376.44 |                   0 |          500.96 |      0      |   0.3308 |             0.0407 |  0.29   |
| (Period('2024Q2', 'Q-DEC'), 'META')  |        8 |  507.47 |       0 |           4059.76 |                   0 |         4033.76 |      4      |  -0.0054 |             0.0158 | -0.0213 |
| (Period('2024Q2', 'Q-DEC'), 'MPWR')  |       14 |  852.56 |      -1 |          11936.8  |                   0 |        11503.5  |     17.5    |  -0.0348 |            -0.0049 | -0.0299 |
| (Period('2024Q4', 'Q-DEC'), 'MCHI')  |        6 |   49.85 |       0 |            299.1  |                   0 |          281.16 |      5.3464 |  -0.0421 |             0.0127 | -0.0548 |
| (Period('2024Q4', 'Q-DEC'), 'VOO')   |       11 |  549.03 |       0 |           6039.33 |                   0 |         5926.91 |     19.1235 |  -0.0154 |            -0.0173 |  0.0019 |

---

## get_money_weighted_return
Calculate the money-weighted return of every position and of the whole portfolio.

It is the annual rate at which the money put in grew into the money taken out plus the value still held (the internal rate of return, or XIRR, of the transactions). Unlike the time-weighted return, it depends on when money was added: buying more just before a rally raises it and buying at a peak lowers it. It therefore measures the investor's own result, including the timing of every purchase and sale, rather than the result of the assets alone.

The cash flows are every purchase (money in, including costs), every sale (money out, after costs), every cash dividend received (money out, on its ex-dividend date) and the latest value of the positions still held, on the last date of the historical data.

**Also known as:** internal rate of return, IRR, XIRR, dollar-weighted return.

**References:**

- paper | Bacon, C.R. (2008). "Practical Portfolio Performance Measurement and Attribution." Wiley, 2nd edition, chapter 2.

**Args:**

- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Portfolio's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per position and for the Portfolio, the money Invested, the money
Received from sales, the Dividends received, the Latest Value, the First
Transaction date and the annualized Money-Weighted Return.

**As an example:**

```python
from financetoolkit import Portfolio

portfolio = Portfolio(example=True, api_key="FINANCIAL_MODELING_PREP_KEY")

portfolio.get_money_weighted_return()
```

Which returns:

|           |   Invested |   Received |   Dividends |   Latest Value | First Transaction   |   Money-Weighted Return |
|:----------|-----------:|-----------:|------------:|---------------:|:--------------------|------------------------:|
| ASML      |   6348.35  |    736.149 |   8880.87   |      181476    | 2000-01-07          |                  0.2066 |
| SKY       |   3339.23  |    261.99  |    901.062  |       11594.5  | 2000-01-10          |                  0.0718 |
| AMZN      |   5042.91  |    192.851 |      0      |       29899    | 2000-01-28          |                  0.2079 |
| FIX       |   1976.93  |     18.43  |   1416.06   |      129037    | 2000-02-23          |                  0.2456 |
| MSFT      |   5529.99  |    147.7   |   3367.52   |       54388.9  | 2000-02-28          |                  0.1349 |
| AMD       |   2384.36  |   1431.84  |      0      |       39333.8  | 2000-04-27          |                  0.1447 |
| AAPL      |   5750.96  |    266.963 |   1283.5    |       48330.9  | 2000-05-08          |                  0.2783 |
| FICO      |   4917.94  |    576.42  |    102.132  |       83204.5  | 2000-06-01          |                  0.1585 |
| BAC       |   2401.58  |    303.8   |    888.08   |        4006.4  | 2000-11-16          |                  0.0665 |
| ALGN      |   9918     |    324.77  |      0      |       13444.4  | 2001-09-18          |                  0.0419 |
| CWST      |   1373.89  |     91.95  |      0      |        6465.06 | 2001-10-15          |                  0.1368 |
| OXY       |   1994.56  |    424.898 |    876.061  |        1548.72 | 2001-11-16          |                  0.0352 |
| WMT       |   2261.02  |    163.39  |    965.737  |       11813.7  | 2001-12-28          |                  0.132  |
| CAMT      |    546.73  |    104.06  |     67.87   |        3916.5  | 2002-08-07          |                  0.2678 |
| NVDA      |    201.303 |     29.941 |     49.6373 |       10773.7  | 2002-09-20          |                  0.3045 |
| NFLX      |   1662.85  |    207.478 |      0      |        6925.5  | 2002-11-18          |                  0.1972 |
| GOOGL     |   4668.1   |    359.26  |    304.08   |       41423.1  | 2004-08-24          |                  0.2094 |
| MPWR      |  30633     |    446.4   |   3301.39   |      152424    | 2005-09-16          |                  0.2877 |
| BLDR      |   1682.82  |    121.254 |      0      |        2887.2  | 2006-12-22          |                  0.1084 |
| VSS       |  10364.5   |    995.66  |   3069.98   |       14199.2  | 2009-06-05          |                  0.0725 |
| AVGO      |   1568.81  |    134.64  |    935.747  |       22004.4  | 2009-11-02          |                  0.375  |
| MCHI      |   2965.43  |    139.96  |    327.316  |        2648.7  | 2011-04-26          |                  0.0088 |
| VOO       |  20238.2   |    368.76  |   3925.88   |       52380    | 2011-12-20          |                  0.1475 |
| META      |   4813.61  |      0     |     81.125  |        9396.15 | 2012-06-20          |                  0.1842 |
| KHC       |    722.41  |    242.21  |    108.25   |         225.63 | 2017-03-07          |                 -0.0511 |
| EMXC      |   1403.3   |    477.33  |    151.542  |        1373.76 | 2019-05-03          |                  0.079  |
| Portfolio | 134711     |   8568.1   |  31003.8    |      935121    | 2000-01-07          |                  0.1728 |

---

## get_turnover
Calculate the turnover of the portfolio, the value traded as a share of the value held: how much of the portfolio the transactions replace.

A turnover of 0.1 on a day means that a tenth of the portfolio's value was bought or sold.

- Traded Value = Σ &#124;volume × price&#124; of the day's transactions
- Gross Value = Σ &#124;value of every position&#124;
- Turnover = Traded Value / ((Gross Value_t + Gross Value_t-1) / 2)

The traded value can also be divided by the net value of the positions that day instead. Over weeks, months, quarters or years the traded values and the daily turnovers are added up and the value is that at the end of the period.

**Also known as:** portfolio turnover, turnover rate, trading activity.

**References:**

- paper | Bacon, C. R. (2008). "Practical Portfolio Performance Measurement and Attribution." 2nd edition, Wiley.
- library | Shares similar logic as pyfolio's [get_turnover](https://github.com/stefan-jansen/pyfolio-reloaded/blob/0.9.9/src/pyfolio/txn.py#L148){:target="_blank"}

**Args:**

- <u>denominator (str, optional):</u> Options are: "gross_value" (pyfolio's "AGB", the average of the gross value
of the day and the day before), "net_value" (pyfolio's "portfolio_value"). Defaults to
"gross_value".
- <u>period (str, optional):</u> The period over which the traded values and turnovers are added up. Options are:
"daily", "weekly", "monthly", "quarterly", "yearly". Defaults to "daily".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Portfolio's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per period the Traded Value, the Gross Value (or Net Value) and
the Turnover.

**Notes:**

- The positions hold no cash, so the net value is that of the positions, where
pyfolio adds the cash.
- The first purchase of the portfolio is a turnover of 2: the average gross value
of that day and the empty day before is half the value bought.
- A transaction on a day without prices counts on the next day that has one.

**As an example:**

```python
from financetoolkit import Portfolio

portfolio = Portfolio(example=True, api_key="FINANCIAL_MODELING_PREP_KEY")

portfolio.get_turnover(period="yearly")
```

Which returns:

| Date   |   Traded Value |   Gross Value |   Turnover |
|:-------|---------------:|--------------:|-----------:|
| 2000   |       3657.08  |       2392.28 |     4.1243 |
| 2001   |       1569.55  |       4798.28 |     0.4154 |
| 2002   |       1693.63  |       5422.3  |     0.3135 |
| 2003   |       1456.49  |       8204.56 |     0.2284 |
| 2004   |       1518.38  |      10365.3  |     0.1683 |
| 2005   |       1918.15  |      13539.3  |     0.1678 |
| 2006   |       2377.66  |      16209    |     0.1559 |
| 2007   |       3585.34  |      19071.4  |     0.2099 |
| 2008   |       1123.91  |      12108.2  |     0.0745 |
| 2009   |       3013.99  |      20985.5  |     0.1933 |
| 2010   |       2621.67  |      25801.1  |     0.1206 |
| 2011   |       3174.61  |      26933.1  |     0.1253 |
| 2012   |       5141.61  |      34851.3  |     0.1546 |
| 2013   |        522.848 |      49217.5  |     0.0121 |
| 2014   |       3364.75  |      54772.7  |     0.0674 |
| 2015   |       2003.66  |      61747.1  |     0.0349 |
| 2016   |       2364.38  |      78378.2  |     0.0384 |
| 2017   |       7271.19  |     117708    |     0.0743 |
| 2018   |       6702.23  |     125233    |     0.0507 |
| 2019   |       7866.05  |     206431    |     0.0445 |
| 2020   |      15353.6   |     328089    |     0.0631 |
| 2021   |       5121.04  |     435818    |     0.0137 |
| 2022   |      18121.5   |     337393    |     0.0569 |
| 2023   |       6215.22  |     547989    |     0.0142 |
| 2024   |      35203.6   |     739785    |     0.051  |
| 2025   |          0     |     908218    |     0      |
| 2026   |          0     |     865290    |     0      |

---

## get_gross_leverage
Calculate the gross leverage of the portfolio, the value of its long and short positions together as a multiple of its net value:

$$
\text{Gross Leverage} = \frac{\sum\left|\text{value of every position}\right|}{\sum \;\text{value of every position}}
$$

A portfolio of long positions has a gross leverage of 1; short positions raise it, e.g. to 1.6 for a 130/30 portfolio. Over weeks, months, quarters or years the values at the end of the period are shown. The measure is defined in pyfolio (Quantopian).

**Also known as:** gross exposure, leverage ratio.

**References:**

- library | Shares similar logic as pyfolio's [gross_lev](https://github.com/stefan-jansen/pyfolio-reloaded/blob/0.9.9/src/pyfolio/timeseries.py#L605){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The period whose last values are shown. Options are: "daily", "weekly",
"monthly", "quarterly", "yearly". Defaults to "daily".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Portfolio's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per period the Gross Value, Net Value and Gross Leverage, NaN when
the net value is not positive.

**Notes:**

- Unlike pyfolio, the positions hold no cash, so the net value is that of the
positions.

**As an example:**

```python
from financetoolkit import Portfolio

portfolio = Portfolio(example=True, api_key="FINANCIAL_MODELING_PREP_KEY")

portfolio.get_gross_leverage(period="yearly")
```

Which returns:

| Date   |   Gross Value |   Net Value |   Gross Leverage |
|:-------|--------------:|------------:|-----------------:|
| 2000   |       2392.28 |     2392.28 |                1 |
| 2001   |       4798.28 |     4798.28 |                1 |
| 2002   |       5422.3  |     5422.3  |                1 |
| 2003   |       8204.56 |     8204.56 |                1 |
| 2004   |      10365.3  |    10365.3  |                1 |
| 2005   |      13539.3  |    13539.3  |                1 |
| 2006   |      16209    |    16209    |                1 |
| 2007   |      19071.4  |    19071.4  |                1 |
| 2008   |      12108.2  |    12108.2  |                1 |
| 2009   |      20985.5  |    20985.5  |                1 |
| 2010   |      25801.1  |    25801.1  |                1 |
| 2011   |      26933.1  |    26933.1  |                1 |
| 2012   |      34851.3  |    34851.3  |                1 |
| 2013   |      49217.5  |    49217.5  |                1 |
| 2014   |      54772.7  |    54772.7  |                1 |
| 2015   |      61747.1  |    61747.1  |                1 |
| 2016   |      78378.2  |    78378.2  |                1 |
| 2017   |     117708    |   117708    |                1 |
| 2018   |     125233    |   125233    |                1 |
| 2019   |     206431    |   206431    |                1 |
| 2020   |     328089    |   328089    |                1 |
| 2021   |     435818    |   435818    |                1 |
| 2022   |     337393    |   337393    |                1 |
| 2023   |     547989    |   547989    |                1 |
| 2024   |     739785    |   739785    |                1 |
| 2025   |     908218    |   908218    |                1 |
| 2026   |     865290    |   865290    |                1 |

---

## get_trades
Calculate the trade list of the portfolio.

Its round trips, every lot a transaction opened paired with the transaction that closed it, with its profit and loss, return and duration, and the lots still held marked to the latest closing price. The trades follow from the same lot matching as the realized profit and loss of `get_transactions_overview`: a sale closes the oldest lots first (FIFO) or the newest (LIFO). A sale that closes part of a lot splits it, so a purchase sold in two parts is two trades, and a sale of more units than are held opens a short trade that later purchases close. The costs of a transaction are spread over its units, so a trade carries the share of the costs of its entry and exit that belongs to its units.

- Gross PnL = Size × (Exit Price − Entry Price) × Direction, with Direction 1 for a long and −1 for a short trade
- Costs = &#124;Entry Costs&#124; × Size / &#124;Entry Volume&#124; + &#124;Exit Costs&#124; × Size / &#124;Exit Volume&#124;
- PnL = Gross PnL − Costs
- Return = PnL / (Size × Entry Price)
- Duration (Days) = Exit Date − Entry Date in calendar days, Duration (Periods) the number of trading days from the entry to the exit

**Also known as:** round trips, closed trades, trade log, trade blotter.

**References:**

- library | Shares similar logic as vectorbt's [Trades](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades){:target="_blank"}
- library | Shares similar logic as backtesting.py's [Trade](https://kernc.github.io/backtesting.py/doc/backtesting/backtesting.html#backtesting.backtesting.Trade){:target="_blank"}
- library | Shares similar logic as backtrader's [TradeAnalyzer](https://www.backtrader.com/docu/analyzers-reference/#tradeanalyzer){:target="_blank"}

**Args:**

- <u>method (str, optional):</u> Which lots a sale closes first. Options are: "FIFO" (first in, first out: the
oldest lots close first), "LIFO" (last in, first out: the newest lots close first). Defaults to
"FIFO". The purchases of a day come before its sales, unless the dates of the transactions include a
time of day.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Portfolio's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: One row per trade, numbered in the order of their entry, with the
Ticker, Direction ("Long" or "Short"), Status ("Closed" or "Open"), Entry Date, Entry
Price, Exit Date, Exit Price, Size, Costs, Gross PnL, PnL, Return, Duration (Days)
and Duration (Periods).

**Notes:**

- An open trade exits at the latest date and closing price, without exit costs, so its
PnL is the unrealized profit and loss of the lot.
- The Gross PnL of the closed long trades of a ticker adds up to its realized PnL in
`get_transactions_overview` with the same method, which leaves the costs out.
- Dividends are not part of a trade's PnL; `get_portfolio_overview` adds them.
- The average cost method of `get_transactions_overview` has no trade list, as it does
not pair a sale with the purchases it closes.

**As an example:**

```python
from financetoolkit import Portfolio

portfolio = Portfolio(example=True, api_key="FINANCIAL_MODELING_PREP_KEY")

portfolio.get_trades(
    show_columns=["Ticker", "Status", "Entry Date", "Entry Price", "Exit Date", "Size", "PnL", "Return"]
)
```

Which returns:

|   Trade | Ticker   | Status   | Entry Date   |   Entry Price | Exit Date   |   Size |        PnL |    Return |
|--------:|:---------|:---------|:-------------|--------------:|:------------|-------:|-----------:|----------:|
|       1 | ASML     | Closed   | 2000-01-07   |       49.3709 | 2010-04-28  |      3 |   -21.4634 |   -0.1449 |
|       2 | ASML     | Closed   | 2000-01-07   |       49.3709 | 2014-02-03  |      3 |   103.567  |    0.6992 |
|       3 | ASML     | Closed   | 2000-01-07   |       49.3709 | 2017-11-15  |      2 |   256.411  |    2.5968 |
|       4 | ASML     | Open     | 2000-01-07   |       49.3709 | 2026-11-20  |      1 |  1216.52   |   24.6403 |
|       5 | SKY      | Closed   | 2000-01-10   |       23.4375 | 2000-06-07  |      1 |    -3.1042 |   -0.1324 |
|       6 | SKY      | Closed   | 2000-01-10   |       23.4375 | 2001-03-20  |      4 |    -3.0167 |   -0.0322 |
|       7 | SKY      | Closed   | 2000-01-10   |       23.4375 | 2002-10-17  |      1 |     3.1958 |    0.1364 |
|       8 | SKY      | Closed   | 2000-01-10   |       23.4375 | 2003-02-20  |      1 |     1.5358 |    0.0655 |
|       9 | SKY      | Closed   | 2000-01-10   |       23.4375 | 2007-05-01  |      3 |    27.3375 |    0.3888 |
|      10 | SKY      | Open     | 2000-01-10   |       23.4375 | 2026-11-20  |      2 |   135.412  |    2.8888 |
|      11 | AMZN     | Closed   | 2000-01-28   |        3.0844 | 2001-06-04  |      2 |    -6.2278 |   -1.0096 |
|      12 | AMZN     | Closed   | 2000-01-28   |        3.0844 | 2003-10-21  |      5 |    -3.4595 |   -0.2243 |
|      13 | AMZN     | Closed   | 2000-01-28   |        3.0844 | 2009-10-06  |      1 |     0.0861 |    0.0279 |
|      14 | FIX      | Closed   | 2000-02-23   |        8.75   | 2003-05-20  |      4 |   -28.32   |   -0.8091 |
|      15 | FIX      | Closed   | 2000-02-23   |        8.75   | 2003-06-23  |      4 |   -25.6    |   -0.7314 |
|      16 | MSFT     | Closed   | 2000-02-28   |       45.7812 | 2006-12-11  |      5 |   -81.206  |   -0.3548 |
|      17 | MSFT     | Open     | 2000-02-28   |       45.7812 | 2026-11-20  |      8 |  3509.91   |    9.5834 |
|      18 | FIX      | Closed   | 2000-03-31   |        6.375  | 2003-06-23  |      1 |    -4.1361 |   -0.6488 |
|      19 | FIX      | Open     | 2000-03-31   |        6.375  | 2026-11-20  |      8 |  8287.87   |  162.507  |
|      20 | SKY      | Open     | 2000-04-06   |       20.8125 | 2026-11-20  |     11 |   773.472  |    3.3785 |
|      21 | AMD      | Closed   | 2000-04-27   |       42.625  | 2004-08-06  |      4 |  -127.66   |   -0.7487 |
|      22 | AMD      | Closed   | 2000-04-27   |       42.625  | 2011-10-14  |      4 |  -154.02   |   -0.9033 |
|      23 | AMD      | Closed   | 2000-04-27   |       42.625  | 2013-04-23  |      2 |   -81.29   |   -0.9535 |
|      24 | AAPL     | Closed   | 2000-05-08   |        0.9833 | 2007-02-21  |      1 |     0.8024 |    0.816  |
|      25 | AAPL     | Closed   | 2000-05-08   |        0.9833 | 2009-06-03  |      4 |    14.6024 |    3.7126 |
|      26 | FICO     | Closed   | 2000-06-01   |       12.5556 | 2006-04-06  |      3 |    81.4632 |    2.1627 |
|      27 | FICO     | Closed   | 2000-06-01   |       12.5556 | 2009-01-08  |      4 |    11.0976 |    0.221  |
|      28 | FICO     | Closed   | 2000-06-01   |       12.5556 | 2011-02-17  |      3 |    45.0932 |    1.1972 |
|      29 | FICO     | Closed   | 2000-06-01   |       12.5556 | 2012-03-20  |      1 |    30.0544 |    2.3937 |
|      30 | FICO     | Closed   | 2000-06-01   |       12.5556 | 2014-03-11  |      4 |   163.698  |    3.2595 |
|      31 | MSFT     | Open     | 2000-07-07   |       41      | 2026-11-20  |     15 |  6650.8    |   10.8143 |
|      32 | FIX      | Open     | 2000-08-29   |        5.375  | 2026-11-20  |      7 |  7257.66   |  192.895  |
|      33 | SKY      | Open     | 2000-11-13   |       20.5    | 2026-11-20  |     10 |   707.1    |    3.4493 |
|      34 | AMD      | Closed   | 2000-11-15   |       21.9375 | 2013-04-23  |      2 |   -39.715  |   -0.9052 |
|      35 | AMD      | Closed   | 2000-11-15   |       21.9375 | 2014-05-05  |      2 |   -39.095  |   -0.8911 |
|      36 | AMD      | Closed   | 2000-11-15   |       21.9375 | 2020-07-22  |      1 |    38.9858 |    1.7771 |
|      37 | BAC      | Closed   | 2000-11-16   |       20.9375 | 2003-09-03  |      2 |    31.925  |    0.7624 |
|      38 | BAC      | Closed   | 2000-11-29   |       20.3438 | 2003-09-03  |      3 |    54.1686 |    0.8876 |
|      39 | BAC      | Closed   | 2000-11-29   |       20.3438 | 2012-05-03  |      4 |   -50.3752 |   -0.619  |
|      40 | BAC      | Closed   | 2000-11-29   |       20.3438 | 2015-08-28  |      5 |   -20.919  |   -0.2057 |
|      41 | BAC      | Open     | 2000-11-29   |       20.3438 | 2026-11-20  |      3 |    80.0886 |    1.3123 |
|      42 | FIX      | Open     | 2001-01-22   |        2.1875 | 2026-11-20  |      8 |  8320.26   |  475.443  |
|      43 | AMD      | Closed   | 2001-02-13   |       24.01   | 2020-07-22  |      2 |    74.0933 |    1.543  |
|      44 | AMD      | Closed   | 2001-02-13   |       24.01   | 2021-02-10  |      2 |   136.547  |    2.8435 |
|      45 | AMD      | Closed   | 2001-02-13   |       24.01   | 2022-07-22  |      3 |   190.07   |    2.6388 |
|      46 | AMD      | Closed   | 2001-02-13   |       24.01   | 2024-08-29  |      5 |   605.067  |    5.0401 |
|      47 | AMD      | Open     | 2001-02-13   |       24.01   | 2026-11-20  |      3 |  1200.94   |   16.6728 |
|      48 | FICO     | Closed   | 2001-03-28   |       17.7926 | 2014-03-11  |      1 |    35.8874 |    2.017  |
|      49 | FICO     | Open     | 2001-03-28   |       17.7926 | 2026-11-20  |      3 |  2029.55   |   38.0224 |
|      50 | AAPL     | Closed   | 2001-04-20   |        0.4471 | 2009-07-02  |      3 |    13.6608 |   10.1847 |
|      51 | AAPL     | Closed   | 2001-04-20   |        0.4471 | 2020-11-09  |      2 |   228.746  |  255.811  |
|      52 | AAPL     | Open     | 2001-04-20   |        0.4471 | 2026-11-20  |      7 |  2394.79   |  765.182  |
|      53 | AAPL     | Open     | 2001-05-03   |        0.4457 | 2026-11-20  |     12 |  4105.37   |  767.589  |
|      54 | AAPL     | Open     | 2001-05-23   |        0.4148 | 2026-11-20  |     15 |  5132.18   |  824.844  |
|      55 | SKY      | Open     | 2001-05-29   |       24.3    | 2026-11-20  |      8 |   536.08   |    2.7576 |
|      56 | ASML     | Open     | 2001-08-13   |       29.2062 | 2026-11-20  |     10 | 12370.1    |   42.3545 |
|      57 | ALGN     | Closed   | 2001-09-18   |        5.05   | 2001-09-26  |      1 |    -4.1    |   -0.8119 |
|      58 | ALGN     | Closed   | 2001-09-18   |        5.05   | 2002-08-22  |      2 |    -7.7    |   -0.7624 |
|      59 | ALGN     | Closed   | 2001-09-18   |        5.05   | 2002-09-25  |      1 |    -4.4    |   -0.8713 |
|      60 | CWST     | Closed   | 2001-10-15   |       11.5    | 2002-06-06  |      1 |    -0.05   |   -0.0043 |
|      61 | CWST     | Closed   | 2001-10-15   |       11.5    | 2022-09-01  |      1 |    69      |    6      |
|      62 | CWST     | Open     | 2001-10-15   |       11.5    | 2026-11-20  |      2 |   175.58   |    7.6339 |
|      63 | OXY      | Closed   | 2001-11-16   |       11.4967 | 2003-04-08  |      1 |     2.0898 |    0.1818 |
|      64 | OXY      | Closed   | 2001-11-16   |       11.4967 | 2009-07-24  |      1 |    54.8957 |    4.7749 |
|      65 | OXY      | Closed   | 2001-11-16   |       11.4967 | 2011-04-07  |      1 |    83.392  |    7.2536 |
|      66 | SKY      | Open     | 2001-12-12   |       29.25   | 2026-11-20  |      9 |   558.54   |    2.1217 |
|      67 | WMT      | Closed   | 2001-12-28   |       19.45   | 2003-04-15  |      4 |    -7.58   |   -0.0974 |
|      68 | WMT      | Closed   | 2001-12-28   |       19.45   | 2010-12-16  |      2 |    -5.23   |   -0.1344 |
|      69 | WMT      | Closed   | 2001-12-28   |       19.45   | 2011-11-28  |      2 |    -1.4834 |   -0.0381 |
|      70 | MSFT     | Open     | 2002-04-01   |       30.19   | 2026-11-20  |     15 |  6814.95   |   15.049  |
|      71 | FICO     | Open     | 2002-04-02   |       27.7822 | 2026-11-20  |     14 |  9331.39   |   23.9912 |
|      72 | FIX      | Open     | 2002-04-03   |        4.72   | 2026-11-20  |      7 |  7264.25   |  219.862  |
|      73 | ALGN     | Closed   | 2002-04-08   |        4.5    | 2002-09-25  |      1 |    -3.1    |   -0.6889 |
|      74 | ALGN     | Closed   | 2002-04-08   |        4.5    | 2002-11-06  |      1 |    -2.78   |   -0.6178 |
|      75 | ALGN     | Closed   | 2002-04-08   |        4.5    | 2003-09-05  |      4 |    32.96   |    1.8311 |
|      76 | ALGN     | Closed   | 2002-04-08   |        4.5    | 2007-02-20  |      5 |    66.9    |    2.9733 |
|      77 | ALGN     | Closed   | 2002-04-08   |        4.5    | 2011-02-25  |      1 |    14.79   |    3.2867 |
|      78 | ALGN     | Closed   | 2002-04-08   |        4.5    | 2012-05-30  |      2 |    53      |    5.8889 |
|      79 | BAC      | Open     | 2002-04-12   |       35.025  | 2026-11-20  |      4 |    47.06   |    0.3359 |
|      80 | SKY      | Open     | 2002-05-03   |       37      | 2026-11-20  |      6 |   323.86   |    1.4588 |
|      81 | FICO     | Open     | 2002-07-05   |       22.2067 | 2026-11-20  |      1 |   672.103  |   30.2658 |
|      82 | SKY      | Open     | 2002-07-25   |       28.81   | 2026-11-20  |      3 |   184.5    |    2.1347 |
|      83 | CAMT     | Closed   | 2002-08-07   |        0.9    | 2003-11-25  |      2 |     1.4533 |    0.8074 |
|      84 | FICO     | Open     | 2002-08-16   |       25.3333 | 2026-11-20  |      4 |  2675.91   |   26.407  |
|      85 | NVDA     | Closed   | 2002-09-20   |        0.0768 | 2004-03-15  |      5 |    -3.6728 |   -9.5647 |
|      86 | NVDA     | Closed   | 2002-09-20   |        0.0768 | 2011-11-04  |      2 |    -0.8741 |   -5.691  |
|      87 | NVDA     | Closed   | 2002-09-20   |        0.0768 | 2018-10-18  |      5 |    28.4032 |   73.9665 |
|      88 | NVDA     | Open     | 2002-09-20   |        0.0768 | 2026-11-20  |      1 |   125.222  | 1630.5    |
|      89 | MSFT     | Open     | 2002-11-15   |       28.345  | 2026-11-20  |      1 |   455.175  |   16.0584 |
|      90 | NFLX     | Closed   | 2002-11-18   |        0.0779 | 2011-11-21  |      1 |     0.7638 |    9.8046 |
|      91 | NFLX     | Closed   | 2002-11-18   |        0.0779 | 2011-12-23  |      1 |    -1.2627 |  -16.2095 |
|      92 | NFLX     | Closed   | 2002-11-18   |        0.0779 | 2013-11-15  |      5 |    23.4824 |   60.2885 |
|      93 | NFLX     | Closed   | 2002-11-18   |        0.0779 | 2021-04-27  |      2 |    99.1764 |  636.562  |
|      94 | CWST     | Open     | 2002-12-20   |        9.2    | 2026-11-20  |     11 |   988.99   |    9.7726 |
|      95 | AMD      | Open     | 2003-01-09   |        6.91   | 2026-11-20  |     14 |  5842.72   |   60.3961 |
|      96 | MSFT     | Open     | 2003-01-27   |       24.585  | 2026-11-20  |      7 |  3219.54   |   18.708  |
|      97 | CAMT     | Closed   | 2003-01-29   |        0.4    | 2003-11-25  |      1 |     2.441  |    6.1024 |
|      98 | CAMT     | Closed   | 2003-01-29   |        0.4    | 2009-11-04  |      1 |     0.7043 |    1.7607 |
|      99 | CAMT     | Closed   | 2003-01-29   |        0.4    | 2010-06-11  |      2 |     1.2886 |    1.6107 |
|     100 | CAMT     | Closed   | 2003-01-29   |        0.4    | 2017-01-23  |      3 |     7.9929 |    6.6607 |
|     101 | SKY      | Open     | 2003-02-07   |       25.4    | 2026-11-20  |     11 |   725.01   |    2.5949 |
|     102 | FIX      | Open     | 2003-02-11   |        2.85   | 2026-11-20  |      4 |  4156.48   |  364.603  |
|     103 | AAPL     | Open     | 2003-02-13   |        0.2596 | 2026-11-20  |      1 |   339.3    | 1307.01   |
|     104 | ASML     | Open     | 2003-03-06   |        9.6721 | 2026-11-20  |     11 | 13820      |  129.896  |
|     105 | CAMT     | Closed   | 2003-04-03   |        0.47   | 2017-01-23  |      1 |     2.7262 |    5.8003 |
|     106 | CAMT     | Closed   | 2003-04-03   |        0.47   | 2019-05-07  |      3 |    25.7985 |   18.2968 |
|     107 | CAMT     | Closed   | 2003-04-03   |        0.47   | 2020-05-29  |      4 |    47.0646 |   25.0344 |
|     108 | CAMT     | Open     | 2003-04-03   |        0.47   | 2026-11-20  |      5 |   442.881  |  188.46   |
|     109 | AAPL     | Open     | 2003-07-14   |        0.3554 | 2026-11-20  |     12 |  4105.46   |  962.637  |
|     110 | ASML     | Open     | 2003-07-15   |       18.1607 | 2026-11-20  |     10 | 12477.6    |   68.7066 |
|     111 | NVDA     | Open     | 2003-07-31   |        0.1591 | 2026-11-20  |      1 |   122.371  |  769.145  |
|     112 | SKY      | Open     | 2003-08-05   |       27.8    | 2026-11-20  |      1 |    61.51   |    2.2126 |
|     113 | NVDA     | Open     | 2003-08-13   |        0.1398 | 2026-11-20  |      1 |   125.39   |  896.926  |
|     114 | NFLX     | Closed   | 2003-10-07   |        0.3146 | 2021-04-27  |      1 |    49.4199 |  157.088  |
|     115 | NFLX     | Closed   | 2003-10-07   |        0.3146 | 2023-03-27  |      1 |    31.2976 |   99.4836 |
|     116 | NFLX     | Open     | 2003-10-07   |        0.3146 | 2026-11-20  |     11 |   618.877  |  178.835  |
|     117 | ALGN     | Closed   | 2003-11-04   |       17.02   | 2012-05-30  |      3 |    41.2733 |    0.8083 |
|     118 | ALGN     | Open     | 2003-11-04   |       17.02   | 2026-11-20  |      6 |   827.567  |    8.1039 |
|     119 | NFLX     | Open     | 2004-01-29   |        0.5054 | 2026-11-20  |     10 |   559.246  |  110.654  |
|     120 | ALGN     | Open     | 2004-03-08   |       19.11   | 2026-11-20  |      3 |   406.18   |    7.0849 |
|     121 | AMD      | Open     | 2004-03-10   |       14.43   | 2026-11-20  |      2 |   819.92   |   28.4103 |
|     122 | ASML     | Open     | 2004-03-25   |       26.3718 | 2026-11-20  |     15 | 18597.7    |   47.0142 |
|     123 | FICO     | Open     | 2004-05-03   |       34.07   | 2026-11-20  |     13 |  8582.12   |   19.3767 |
|     124 | SKY      | Open     | 2004-05-07   |       40.06   | 2026-11-20  |      3 |   153.75   |    1.2793 |
|     125 | FICO     | Open     | 2004-07-12   |       31.36   | 2026-11-20  |      2 |  1322.9    |   21.0922 |
|     126 | BAC      | Open     | 2004-08-11   |       42.765  | 2026-11-20  |      2 |     5.55   |    0.0649 |
|     127 | GOOGL    | Closed   | 2004-08-24   |        2.6244 | 2024-06-21  |      2 |   353.611  |   67.3699 |
|     128 | GOOGL    | Open     | 2004-08-24   |        2.6244 | 2026-11-20  |      8 |  2099.72   |  100.01   |
|     129 | NFLX     | Open     | 2004-10-12   |        0.2469 | 2026-11-20  |     11 |   620.314  |  228.401  |
|     130 | AMZN     | Closed   | 2004-10-19   |        1.9165 | 2009-10-06  |      1 |     1.379  |    0.7195 |
|     131 | AMZN     | Closed   | 2004-10-19   |        1.9165 | 2010-01-21  |      3 |    12.4935 |    2.173  |
|     132 | AMZN     | Closed   | 2004-10-19   |        1.9165 | 2014-02-11  |      4 |    63.692  |    8.3084 |
|     133 | AMZN     | Closed   | 2004-10-19   |        1.9165 | 2015-10-02  |      3 |    73.3815 |   12.7631 |
|     134 | AMZN     | Open     | 2004-10-19   |        1.9165 | 2026-11-20  |      1 |   244.654  |  127.656  |
|     135 | ASML     | Open     | 2004-11-11   |       22.4562 | 2026-11-20  |      8 |  9948.11   |   55.3751 |
|     136 | GOOGL    | Open     | 2004-12-01   |        4.5035 | 2026-11-20  |      6 |  1561.72   |   57.7965 |
|     137 | AMZN     | Open     | 2004-12-29   |        2.241  | 2026-11-20  |      7 |  1712.05   |  109.138  |
|     138 | ASML     | Open     | 2005-01-06   |       21.5503 | 2026-11-20  |     11 | 13689.4    |   57.7481 |
|     139 | GOOGL    | Open     | 2005-02-17   |        4.9525 | 2026-11-20  |     12 |  3123.05   |   52.5501 |
|     140 | NVDA     | Open     | 2005-03-04   |        0.2298 | 2026-11-20  |      7 |   875.101  |  544.014  |
|     141 | FIX      | Open     | 2005-03-09   |        7.87   | 2026-11-20  |     10 | 10344      |  131.436  |
|     142 | GOOGL    | Open     | 2005-05-18   |        5.985  | 2026-11-20  |      8 |  2074.44   |   43.3258 |
|     143 | SKY      | Open     | 2005-08-03   |       41.85   | 2026-11-20  |     11 |   541.06   |    1.1753 |
|     144 | SKY      | Open     | 2005-08-22   |       38.44   | 2026-11-20  |      1 |    52.87   |    1.3754 |
|     145 | AMD      | Open     | 2005-08-30   |       20.37   | 2026-11-20  |      7 |  2827.14   |   19.8271 |
|     146 | MPWR     | Closed   | 2005-09-16   |        8.32   | 2010-03-22  |      2 |    28      |    1.6827 |
|     147 | MPWR     | Closed   | 2005-09-16   |        8.32   | 2017-04-05  |      2 |   164.92   |    9.9111 |
|     148 | MPWR     | Closed   | 2005-09-16   |        8.32   | 2017-12-04  |      2 |   202.36   |   12.1611 |
|     149 | MPWR     | Open     | 2005-09-16   |        8.32   | 2026-11-20  |      9 | 10201.8    |  136.242  |
|     150 | MSFT     | Open     | 2005-09-19   |       26      | 2026-11-20  |     13 |  5958.76   |   17.6295 |
|     151 | MSFT     | Open     | 2005-09-22   |       25.34   | 2026-11-20  |     12 |  5507.16   |   18.1109 |
|     152 | NFLX     | Open     | 2005-10-04   |        0.3856 | 2026-11-20  |     10 |   563.444  |  146.121  |
|     153 | GOOGL    | Open     | 2005-11-14   |        9.9342 | 2026-11-20  |      5 |  1276.78   |   25.7047 |
|     154 | AAPL     | Open     | 2005-12-07   |        2.6411 | 2026-11-20  |     12 |  4077.03   |  128.64   |
|     155 | FICO     | Open     | 2006-01-09   |       46.9    | 2026-11-20  |     12 |  7765.92   |   13.7987 |
|     156 | AMD      | Open     | 2006-02-01   |       42.1    | 2026-11-20  |      4 |  1526.16   |    9.0627 |
|     157 | AMZN     | Open     | 2006-03-16   |        1.8385 | 2026-11-20  |      7 |  1713.87   |  133.173  |
|     158 | MSFT     | Open     | 2006-03-17   |       27.5    | 2026-11-20  |      1 |   454.02   |   16.5098 |
|     159 | ASML     | Open     | 2006-04-05   |       30.1997 | 2026-11-20  |     13 | 16067.3    |   40.9257 |
|     160 | AMZN     | Open     | 2006-08-11   |        1.3035 | 2026-11-20  |      4 |   982.066  |  188.352  |
|     161 | NVDA     | Open     | 2006-08-14   |        0.388  | 2026-11-20  |      6 |   747.852  |  321.242  |
|     162 | NFLX     | Open     | 2006-08-23   |        0.2669 | 2026-11-20  |      5 |   281.315  |  210.802  |
|     163 | NVDA     | Open     | 2006-09-08   |        0.4617 | 2026-11-20  |      9 |  1125.61   |  270.887  |
|     164 | FICO     | Open     | 2006-11-01   |       36.46   | 2026-11-20  |     15 |  9867.75   |   18.0431 |
|     165 | NVDA     | Open     | 2006-11-08   |        0.5767 | 2026-11-20  |      2 |   246.907  |  214.069  |
|     166 | ASML     | Open     | 2006-11-09   |       33.9545 | 2026-11-20  |      5 |  6158.33   |   36.274  |
|     167 | FIX      | Open     | 2006-12-07   |       13.24   | 2026-11-20  |     15 | 15435.4    |   77.7213 |
|     168 | NFLX     | Open     | 2006-12-21   |        0.3827 | 2026-11-20  |      6 |   336.084  |  146.365  |
|     169 | BLDR     | Closed   | 2006-12-22   |       14.3061 | 2008-05-02  |      1 |   -11.4524 |   -0.8005 |
|     170 | AMZN     | Open     | 2007-01-23   |        1.8215 | 2026-11-20  |     15 |  3671.98   |  134.394  |
|     171 | FIX      | Open     | 2007-02-28   |       13.61   | 2026-11-20  |     15 | 15432.9    |   75.5959 |
|     172 | SKY      | Open     | 2007-03-06   |       31.12   | 2026-11-20  |     13 |   782.47   |    1.9341 |
|     173 | WMT      | Closed   | 2007-04-16   |       16.0233 | 2011-11-28  |      1 |     2.9933 |    0.1868 |
|     174 | WMT      | Open     | 2007-04-16   |       16.0233 | 2026-11-20  |     14 |  1566.04   |    6.9811 |
|     175 | SKY      | Open     | 2007-04-18   |       33.39   | 2026-11-20  |      5 |   289.6    |    1.7347 |
|     176 | OXY      | Closed   | 2007-05-21   |       52.4922 | 2017-02-27  |      1 |     9.9064 |    0.1887 |
|     177 | OXY      | Closed   | 2007-05-21   |       52.4922 | 2020-12-18  |      5 |  -172.218  |   -0.6562 |
|     178 | OXY      | Closed   | 2007-05-21   |       52.4922 | 2024-12-05  |      2 |    -8.1673 |   -0.0778 |
|     179 | OXY      | Open     | 2007-05-21   |       52.4922 | 2026-11-20  |      6 |     8.0182 |    0.0255 |
|     180 | OXY      | Open     | 2007-05-29   |       51.8024 | 2026-11-20  |     10 |    19.976  |    0.0386 |
|     181 | FIX      | Open     | 2007-07-12   |       14.51   | 2026-11-20  |     12 | 12335.5    |   70.8449 |
|     182 | FICO     | Open     | 2007-09-04   |       37.75   | 2026-11-20  |     15 |  9847.4    |   17.3906 |
|     183 | FICO     | Open     | 2007-10-22   |       34.21   | 2026-11-20  |      2 |  1319.2    |   19.2809 |
|     184 | AMD      | Open     | 2007-11-21   |       10.83   | 2026-11-20  |      3 |  1240.68   |   38.1865 |
|     185 | MPWR     | Open     | 2007-12-10   |       21.34   | 2026-11-20  |     12 | 13448.5    |   52.5169 |
|     186 | BAC      | Open     | 2008-01-04   |       39.85   | 2026-11-20  |      3 |    19.57   |    0.1637 |
|     187 | MPWR     | Open     | 2008-01-17   |       16.04   | 2026-11-20  |      2 |  2251.02   |   70.169  |
|     188 | GOOGL    | Open     | 2008-02-25   |       12.1732 | 2026-11-20  |     15 |  3794.75   |   20.782  |
|     189 | BAC      | Open     | 2008-03-25   |       40.97   | 2026-11-20  |      8 |    48.56   |    0.1482 |
|     190 | WMT      | Open     | 2008-07-08   |       19.7033 | 2026-11-20  |      9 |   974.22   |    5.4938 |
|     191 | AAPL     | Open     | 2008-07-11   |        6.1636 | 2026-11-20  |     11 |  3699.36   |   54.5632 |
|     192 | NVDA     | Open     | 2008-07-16   |        0.283  | 2026-11-20  |      8 |   999.976  |  441.685  |
|     193 | NVDA     | Open     | 2008-08-05   |        0.2797 | 2026-11-20  |      3 |   374.751  |  446.611  |
|     194 | GOOGL    | Open     | 2008-12-01   |        6.6564 | 2026-11-20  |     14 |  3619.87   |   38.8441 |
|     195 | ALGN     | Open     | 2008-12-02   |        6.83   | 2026-11-20  |      6 |   887.04   |   21.6457 |
|     196 | WMT      | Open     | 2008-12-10   |       18.4167 | 2026-11-20  |      4 |   437.133  |    5.9339 |
|     197 | FIX      | Open     | 2009-02-17   |       10.34   | 2026-11-20  |      9 |  9287.17   |   99.7977 |
|     198 | VSS      | Closed   | 2009-06-05   |       66.66   | 2012-08-21  |      4 |    72.2286 |    0.2709 |
|     199 | VSS      | Closed   | 2009-06-05   |       66.66   | 2018-12-24  |      4 |    96.2686 |    0.361  |
|     200 | VSS      | Closed   | 2009-06-05   |       66.66   | 2020-06-22  |      3 |    92.3314 |    0.4617 |
|     201 | VSS      | Open     | 2009-06-05   |       66.66   | 2026-11-20  |      3 |   205.011  |    1.0252 |
|     202 | SKY      | Open     | 2009-06-12   |       19.69   | 2026-11-20  |      9 |   644.58   |    3.6374 |
|     203 | ASML     | Open     | 2009-06-18   |       26.4026 | 2026-11-20  |     13 | 16116.6    |   46.9552 |
|     204 | WMT      | Open     | 2009-06-29   |       16.2533 | 2026-11-20  |      6 |   667.18   |    6.8415 |
|     205 | MPWR     | Open     | 2009-07-15   |       23.73   | 2026-11-20  |      6 |  6706.92   |   47.1058 |
|     206 | AAPL     | Open     | 2009-08-03   |        5.9439 | 2026-11-20  |      9 |  3026.54   |   56.5761 |
|     207 | BLDR     | Closed   | 2009-08-06   |        5.635  | 2010-09-13  |      2 |    -6.69   |   -0.5936 |
|     208 | VSS      | Open     | 2009-08-11   |       72.15   | 2026-11-20  |      2 |   123.98   |    0.8592 |
|     209 | NFLX     | Open     | 2009-08-28   |        0.6317 | 2026-11-20  |      5 |   278.491  |   88.1721 |
|     210 | FICO     | Open     | 2009-10-22   |       22.62   | 2026-11-20  |     13 |  8728.97   |   29.6843 |
|     211 | AVGO     | Closed   | 2009-11-02   |        1.49   | 2014-01-30  |      4 |    12.5086 |    2.0988 |
|     212 | AVGO     | Closed   | 2009-11-02   |        1.49   | 2016-08-09  |      1 |    12.4871 |    8.3806 |
|     213 | AVGO     | Closed   | 2009-11-02   |        1.49   | 2018-06-20  |      2 |    47.4743 |   15.931  |
|     214 | FIX      | Open     | 2009-11-17   |       11.48   | 2026-11-20  |     13 | 13401.9    |   89.8008 |
|     215 | ALGN     | Open     | 2009-11-20   |       15.54   | 2026-11-20  |     11 |  1534.93   |    8.9793 |
|     216 | BAC      | Open     | 2009-12-23   |       15.19   | 2026-11-20  |     12 |   381.2    |    2.0913 |
|     217 | AMD      | Open     | 2009-12-31   |        9.68   | 2026-11-20  |      3 |  1244.13   |   42.8419 |
|     218 | WMT      | Open     | 2010-01-05   |       17.8967 | 2026-11-20  |     14 |  1537.75   |    6.1374 |
|     219 | CWST     | Open     | 2010-01-28   |        4.51   | 2026-11-20  |      6 |   567.68   |   20.9786 |
|     220 | OXY      | Open     | 2010-01-29   |       75.0545 | 2026-11-20  |      2 |   -42.309  |   -0.2819 |
|     221 | VSS      | Open     | 2010-03-17   |       85.58   | 2026-11-20  |      8 |   394.48   |    0.5762 |
|     222 | BLDR     | Closed   | 2010-04-08   |        3.5    | 2010-09-13  |      1 |    -1.3211 |   -0.3775 |
|     223 | BLDR     | Closed   | 2010-04-08   |        3.5    | 2011-04-12  |      2 |    -2.8222 |   -0.4032 |
|     224 | BLDR     | Closed   | 2010-04-08   |        3.5    | 2015-12-08  |      2 |    18.6578 |    2.6654 |
|     225 | BLDR     | Closed   | 2010-04-08   |        3.5    | 2016-07-29  |      3 |    26.8367 |    2.5559 |
|     226 | BLDR     | Closed   | 2010-04-08   |        3.5    | 2017-12-27  |      1 |    18.1789 |    5.194  |
|     227 | FICO     | Open     | 2010-06-08   |       21.15   | 2026-11-20  |      8 |  5383.28   |   31.8161 |
|     228 | AAPL     | Open     | 2010-07-08   |        9.2175 | 2026-11-20  |     11 |  3665.77   |   36.1542 |
|     229 | WMT      | Open     | 2010-07-15   |       16.8033 | 2026-11-20  |     15 |  1667.2    |    6.6146 |
|     230 | AAPL     | Open     | 2010-07-20   |        8.9961 | 2026-11-20  |     13 |  4333.33   |   37.0531 |
|     231 | WMT      | Open     | 2010-09-15   |       17.62   | 2026-11-20  |      2 |   219.66   |    6.2333 |
|     232 | GOOGL    | Open     | 2010-09-24   |       13.1954 | 2026-11-20  |     10 |  2517.95   |   19.082  |
|     233 | ALGN     | Open     | 2010-09-28   |       19.73   | 2026-11-20  |      5 |   675.2    |    6.8444 |
|     234 | ASML     | Open     | 2010-10-21   |       41.4675 | 2026-11-20  |      8 |  9798.02   |   29.5352 |
|     235 | BAC      | Open     | 2011-02-02   |       14.24   | 2026-11-20  |      3 |    96.4    |    2.2566 |
|     236 | MPWR     | Open     | 2011-02-03   |       14.81   | 2026-11-20  |     11 | 12396.6    |   76.095  |
|     237 | BLDR     | Closed   | 2011-03-16   |        2.44   | 2017-12-27  |      1 |    19.2071 |    7.8718 |
|     238 | BLDR     | Open     | 2011-03-16   |        2.44   | 2026-11-20  |      6 |   314.683  |   21.4947 |
|     239 | MCHI     | Closed   | 2011-04-26   |       53.74   | 2014-10-27  |      3 |   -21.76   |   -0.135  |
|     240 | MCHI     | Open     | 2011-04-26   |       53.74   | 2026-11-20  |      3 |   -23.66   |   -0.1468 |
|     241 | AVGO     | Closed   | 2011-06-30   |        3.8    | 2018-06-20  |      2 |    42.7114 |    5.6199 |
|     242 | AVGO     | Open     | 2011-06-30   |        3.8    | 2026-11-20  |     12 |  3604.75   |   79.0515 |
|     243 | CWST     | Open     | 2011-08-17   |        5.3    | 2026-11-20  |     13 |  1218.87   |   17.6904 |
|     244 | NVDA     | Open     | 2011-09-02   |        0.323  | 2026-11-20  |      3 |   373.621  |  385.574  |
|     245 | SKY      | Open     | 2011-09-12   |        9.07   | 2026-11-20  |      1 |    81.24   |    8.957  |
|     246 | NFLX     | Open     | 2011-09-19   |        2.0536 | 2026-11-20  |      6 |   326.058  |   26.4623 |
|     247 | MSFT     | Open     | 2011-10-25   |       26.81   | 2026-11-20  |     10 |  4577.1    |   17.0724 |
|     248 | ASML     | Open     | 2011-11-18   |       49.4416 | 2026-11-20  |     13 | 15815.1    |   24.6057 |
|     249 | AVGO     | Open     | 2011-11-30   |        2.99   | 2026-11-20  |     11 |  3312.62   |  100.718  |
|     250 | VOO      | Closed   | 2011-12-20   |      113.96   | 2014-11-04  |      2 |   140.84   |    0.6179 |
|     251 | VOO      | Open     | 2011-12-20   |      113.96   | 2026-11-20  |      9 |  4694.22   |    4.5769 |
|     252 | MPWR     | Open     | 2012-01-04   |       14.86   | 2026-11-20  |      2 |  2254.38   |   75.854  |
|     253 | AMD      | Open     | 2012-02-09   |        7.24   | 2026-11-20  |      5 |  2085.75   |   57.6174 |
|     254 | GOOGL    | Open     | 2012-03-09   |       15.0213 | 2026-11-20  |     10 |  2499.69   |   16.641  |
|     255 | NVDA     | Open     | 2012-03-29   |        0.3808 | 2026-11-20  |      4 |   499.597  |  327.992  |
|     256 | VOO      | Open     | 2012-04-26   |      128.22   | 2026-11-20  |     14 |  7099.48   |    3.955  |
|     257 | VSS      | Open     | 2012-06-18   |       79.46   | 2026-11-20  |     15 |   835.2    |    0.7007 |
|     258 | META     | Open     | 2012-06-20   |       31.6    | 2026-11-20  |      2 |  1058.48   |   16.7481 |
|     259 | ALGN     | Open     | 2012-06-28   |       31.9    | 2026-11-20  |      1 |   122.27   |    3.8329 |
|     260 | ALGN     | Open     | 2012-06-29   |       33.46   | 2026-11-20  |     10 |  1216.1    |    3.6345 |
|     261 | VSS      | Open     | 2012-07-09   |       81.09   | 2026-11-20  |      7 |   375.35   |    0.6613 |
|     262 | VSS      | Open     | 2012-10-17   |       89.47   | 2026-11-20  |      1 |    44.67   |    0.4993 |
|     263 | SKY      | Open     | 2012-10-25   |        4.42   | 2026-11-20  |      9 |   781.01   |   19.6332 |
|     264 | AMD      | Open     | 2012-11-13   |        2.09   | 2026-11-20  |     12 |  5065.6    |  201.978  |
|     265 | GOOGL    | Open     | 2012-12-24   |       17.7553 | 2026-11-20  |     12 |  2967.42   |   13.9274 |
|     266 | BLDR     | Open     | 2013-03-01   |        6.04   | 2026-11-20  |     12 |   585.88   |    8.0833 |
|     267 | BLDR     | Open     | 2013-05-21   |        6.92   | 2026-11-20  |      3 |   144.33   |    6.9523 |
|     268 | MPWR     | Open     | 2013-05-24   |       24.11   | 2026-11-20  |      4 |  4469.76   |   46.3476 |
|     269 | AMZN     | Open     | 2013-06-06   |       13.3915 | 2026-11-20  |      2 |   464.857  |   17.3564 |
|     270 | BLDR     | Open     | 2013-06-21   |        6.28   | 2026-11-20  |      1 |    46.75   |    7.4443 |
|     271 | AMD      | Open     | 2013-07-01   |        4.1    | 2026-11-20  |      7 |  2939.03   |  102.405  |
|     272 | NVDA     | Open     | 2013-09-09   |        0.3783 | 2026-11-20  |      8 |   999.214  |  330.166  |
|     273 | AAPL     | Open     | 2013-10-17   |       18.0179 | 2026-11-20  |      2 |   646.084  |   17.929  |
|     274 | SKY      | Open     | 2013-10-29   |        4.4    | 2026-11-20  |     10 |   867.1    |   19.7068 |
|     275 | MSFT     | Open     | 2013-12-03   |       38.31   | 2026-11-20  |      4 |  1784.84   |   11.6474 |
|     276 | AMZN     | Open     | 2014-02-24   |       17.589  | 2026-11-20  |      8 |  1831.85   |   13.0184 |
|     277 | BAC      | Open     | 2014-03-26   |       17.18   | 2026-11-20  |      9 |   265.74   |    1.7187 |
|     278 | WMT      | Open     | 2014-07-16   |       25.62   | 2026-11-20  |     15 |  1533.95   |    3.9915 |
|     279 | FICO     | Open     | 2014-08-19   |       56.06   | 2026-11-20  |      8 |  5106      |   11.3851 |
|     280 | FIX      | Open     | 2014-09-22   |       14.38   | 2026-11-20  |      6 |  6167.54   |   71.4828 |
|     281 | AMZN     | Open     | 2014-10-23   |       15.659  | 2026-11-20  |     14 |  3234.25   |   14.7531 |
|     282 | GOOGL    | Open     | 2014-11-25   |       27.4615 | 2026-11-20  |      2 |   474.657  |    8.6422 |
|     283 | ASML     | Open     | 2014-12-17   |      105.69   | 2026-11-20  |      7 |  8123.71   |   10.9805 |
|     284 | MPWR     | Open     | 2015-01-13   |       46.94   | 2026-11-20  |      2 |  2187.22   |   23.298  |
|     285 | MCHI     | Open     | 2015-01-29   |       51.51   | 2026-11-20  |      1 |    -5.49   |   -0.1066 |
|     286 | MPWR     | Open     | 2015-02-05   |       47.53   | 2026-11-20  |     11 | 12039.7    |   23.028  |
|     287 | ALGN     | Open     | 2015-02-20   |       56.81   | 2026-11-20  |     12 |  1178.32   |    1.7285 |
|     288 | NVDA     | Open     | 2015-03-02   |        0.565  | 2026-11-20  |      4 |   499.86   |  221.177  |
|     289 | CWST     | Open     | 2015-04-06   |        6.17   | 2026-11-20  |      4 |   372.48   |   15.0924 |
|     290 | AVGO     | Open     | 2015-05-19   |       12.95   | 2026-11-20  |     10 |  2914.6    |   22.5066 |
|     291 | AMZN     | Open     | 2015-10-12   |       27.5095 | 2026-11-20  |      4 |   875.242  |    7.954  |
|     292 | AMZN     | Open     | 2015-11-12   |       33.28   | 2026-11-20  |      6 |  1279.24   |    6.4065 |
|     293 | VOO      | Open     | 2016-01-19   |      172.34   | 2026-11-20  |      8 |  3703.6    |    2.6863 |
|     294 | GOOGL    | Open     | 2016-03-22   |       38.0025 | 2026-11-20  |      3 |   681.862  |    5.9809 |
|     295 | CAMT     | Open     | 2016-04-13   |        2.09   | 2026-11-20  |      7 |   608.77   |   41.6111 |
|     296 | MSFT     | Open     | 2016-05-03   |       49.78   | 2026-11-20  |      7 |  3043.18   |    8.7332 |
|     297 | BAC      | Open     | 2016-05-10   |       14.3    | 2026-11-20  |      7 |   227.18   |    2.2695 |
|     298 | CAMT     | Open     | 2016-05-13   |        1.88   | 2026-11-20  |     12 |  1045.84   |   46.3582 |
|     299 | NFLX     | Open     | 2016-07-18   |        9.881  | 2026-11-20  |     15 |   700.735  |    4.7278 |
|     300 | AVGO     | Open     | 2016-12-23   |       18.19   | 2026-11-20  |     10 |  2859.2    |   15.7185 |
|     301 | NFLX     | Open     | 2017-01-18   |       13.326  | 2026-11-20  |      2 |    85.808  |    3.2196 |
|     302 | KHC      | Closed   | 2017-03-07   |       90.8    | 2020-08-10  |      3 |  -170.03   |   -0.6242 |
|     303 | AMZN     | Open     | 2017-03-23   |       42.369  | 2026-11-20  |     11 |  2246.96   |    4.8212 |
|     304 | VSS      | Open     | 2017-04-12   |      102.99   | 2026-11-20  |      7 |   222.05   |    0.308  |
|     305 | MCHI     | Open     | 2017-06-21   |       54.65   | 2026-11-20  |      5 |   -43.15   |   -0.1579 |
|     306 | VOO      | Open     | 2017-06-29   |      221.69   | 2026-11-20  |     11 |  4551.35   |    1.8664 |
|     307 | MCHI     | Open     | 2017-07-06   |       54.24   | 2026-11-20  |      4 |   -32.88   |   -0.1515 |
|     308 | ALGN     | Open     | 2017-10-02   |      187.22   | 2026-11-20  |      5 |  -162.25   |   -0.1733 |
|     309 | CAMT     | Open     | 2017-11-24   |        6.44   | 2026-11-20  |     12 |   993.12   |   12.8509 |
|     310 | GOOGL    | Open     | 2017-11-30   |       51.8085 | 2026-11-20  |      6 |  1277.89   |    4.1109 |
|     311 | MCHI     | Open     | 2017-12-05   |       64.75   | 2026-11-20  |      1 |   -19.73   |   -0.3047 |
|     312 | AMZN     | Open     | 2017-12-29   |       58.4735 | 2026-11-20  |     10 |  1883.47   |    3.2211 |
|     313 | FICO     | Open     | 2018-01-18   |      161.2    | 2026-11-20  |      6 |  3198.66   |    3.3071 |
|     314 | VOO      | Open     | 2018-01-22   |      259.75   | 2026-11-20  |      8 |  3003.32   |    1.4453 |
|     315 | CWST     | Open     | 2018-03-20   |       23.91   | 2026-11-20  |     14 |  1055.32   |    3.1527 |
|     316 | MPWR     | Open     | 2018-04-05   |      114.11   | 2026-11-20  |     11 | 11304.3    |    9.0059 |
|     317 | BAC      | Open     | 2018-04-27   |       30.15   | 2026-11-20  |     11 |   182.79   |    0.5512 |
|     318 | MCHI     | Open     | 2018-10-26   |       52.51   | 2026-11-20  |      6 |   -40.94   |   -0.1299 |
|     319 | SKY      | Open     | 2018-11-05   |       24.61   | 2026-11-20  |      2 |   133.4    |    2.7103 |
|     320 | SKY      | Open     | 2018-11-28   |       22      | 2026-11-20  |      1 |    69.31   |    3.1505 |
|     321 | META     | Open     | 2018-12-04   |      137.93   | 2026-11-20  |      5 |  2113.55   |    3.0647 |
|     322 | NFLX     | Open     | 2018-12-31   |       26.766  | 2026-11-20  |      6 |   178.784  |    1.1133 |
|     323 | VSS      | Open     | 2019-02-21   |      103.29   | 2026-11-20  |      5 |   157.25   |    0.3045 |
|     324 | GOOGL    | Open     | 2019-03-21   |       61.8065 | 2026-11-20  |      2 |   403.967  |    3.268  |
|     325 | CAMT     | Open     | 2019-04-12   |       10.63   | 2026-11-20  |      1 |    76.57   |    7.2032 |
|     326 | EMXC     | Closed   | 2019-05-03   |       50      | 2021-05-24  |      3 |    27.48   |    0.1832 |
|     327 | EMXC     | Closed   | 2019-05-03   |       50      | 2024-11-05  |      2 |    18.02   |    0.1802 |
|     328 | AMD      | Open     | 2019-07-03   |       31.19   | 2026-11-20  |     15 |  5897      |   12.6045 |
|     329 | GOOGL    | Open     | 2019-07-24   |       56.9865 | 2026-11-20  |     15 |  3121.55   |    3.6518 |
|     330 | AVGO     | Open     | 2019-07-29   |       30.17   | 2026-11-20  |      1 |   274.24   |    9.0898 |
|     331 | AMZN     | Open     | 2019-08-26   |       88.4435 | 2026-11-20  |     12 |  1900.52   |    1.7907 |
|     332 | NFLX     | Open     | 2019-08-28   |       29.177  | 2026-11-20  |      3 |    81.659  |    0.9329 |
|     333 | BAC      | Open     | 2019-09-24   |       28.94   | 2026-11-20  |     12 |   216.2    |    0.6226 |
|     334 | AMZN     | Open     | 2019-11-01   |       89.572  | 2026-11-20  |      5 |   786.24   |    1.7555 |
|     335 | ALGN     | Open     | 2019-11-08   |      259.92   | 2026-11-20  |     14 | -1468.5    |   -0.4036 |
|     336 | VSS      | Open     | 2020-02-24   |      104.43   | 2026-11-20  |     10 |   307.1    |    0.2941 |
|     337 | VOO      | Open     | 2020-03-09   |      252.11   | 2026-11-20  |      5 |  1914.15   |    1.5185 |
|     338 | GOOGL    | Open     | 2020-04-02   |       55.8515 | 2026-11-20  |      4 |   836.754  |    3.7454 |
|     339 | MSFT     | Open     | 2020-05-08   |      184.68   | 2026-11-20  |     12 |  3598.08   |    1.6236 |
|     340 | KHC      | Closed   | 2020-06-05   |       32.62   | 2020-08-10  |      2 |     3.94   |    0.0604 |
|     341 | KHC      | Closed   | 2020-06-05   |       32.62   | 2024-03-05  |      2 |     2.62   |    0.0402 |
|     342 | KHC      | Open     | 2020-06-05   |       32.62   | 2026-11-20  |      6 |   -44.58   |   -0.2278 |
|     343 | NFLX     | Open     | 2020-07-31   |       48.888  | 2026-11-20  |     10 |    76.42   |    0.1563 |
|     344 | AMZN     | Open     | 2020-08-24   |      165.373  | 2026-11-20  |     10 |   812.47   |    0.4913 |
|     345 | AAPL     | Open     | 2020-09-16   |      112.13   | 2026-11-20  |      5 |  1150.15   |    2.0515 |
|     346 | NVDA     | Open     | 2020-09-25   |       12.8737 | 2026-11-20  |     12 |  1350.88   |    8.7444 |
|     347 | NFLX     | Open     | 2020-10-01   |       52.751  | 2026-11-20  |     11 |    41.769  |    0.072  |
|     348 | ALGN     | Open     | 2020-11-02   |      458.44   | 2026-11-20  |      8 | -2428.16   |   -0.6621 |
|     349 | BLDR     | Open     | 2020-11-03   |       32.68   | 2026-11-20  |      8 |   177.8    |    0.6801 |
|     350 | CWST     | Open     | 2020-11-10   |       59.7    | 2026-11-20  |      4 |   157.36   |    0.659  |
|     351 | VSS      | Open     | 2020-11-24   |      116.41   | 2026-11-20  |     12 |   223.76   |    0.1602 |
|     352 | BLDR     | Open     | 2020-12-29   |       41.91   | 2026-11-20  |      6 |    75.72   |    0.3011 |
|     353 | CWST     | Open     | 2021-02-04   |       58.39   | 2026-11-20  |      9 |   368.1    |    0.7005 |
|     354 | EMXC     | Closed   | 2021-03-15   |       59.81   | 2024-11-05  |      3 |    -0.975  |   -0.0054 |
|     355 | EMXC     | Open     | 2021-03-15   |       59.81   | 2026-11-20  |      5 |    89.175  |    0.2982 |
|     356 | WMT      | Open     | 2021-03-23   |       44.6467 | 2026-11-20  |     13 |  1081.94   |    1.8641 |
|     357 | MCHI     | Open     | 2021-03-29   |       80.77   | 2026-11-20  |      6 |  -210.5    |   -0.4344 |
|     358 | EMXC     | Open     | 2021-05-21   |       60.24   | 2026-11-20  |      4 |    68.12   |    0.2827 |
|     359 | AVGO     | Open     | 2021-08-04   |       48.78   | 2026-11-20  |      7 |  1786.41   |    5.2317 |
|     360 | EMXC     | Open     | 2021-10-13   |       60.98   | 2026-11-20  |      7 |   116.53   |    0.273  |
|     361 | AVGO     | Open     | 2021-10-19   |       51.04   | 2026-11-20  |     13 |  3291.81   |    4.9611 |
|     362 | AVGO     | Open     | 2021-11-30   |       55.37   | 2026-11-20  |      2 |   498.08   |    4.4977 |
|     363 | FIX      | Open     | 2021-12-01   |       93.73   | 2026-11-20  |      8 |  7589.92   |   10.1221 |
|     364 | VSS      | Open     | 2022-05-24   |      112.32   | 2026-11-20  |     10 |   227.2    |    0.2023 |
|     365 | MPWR     | Open     | 2022-06-15   |      416.19   | 2026-11-20  |      7 |  5078.02   |    1.743  |
|     366 | AAPL     | Open     | 2022-08-23   |      167.23   | 2026-11-20  |     14 |  2452.62   |    1.0476 |
|     367 | ASML     | Open     | 2022-09-02   |      467.19   | 2026-11-20  |      4 |  3193.12   |    1.7087 |
|     368 | OXY      | Open     | 2022-09-30   |       61.45   | 2026-11-20  |      9 |   -69.95   |   -0.1265 |
|     369 | BAC      | Open     | 2022-10-12   |       29.86   | 2026-11-20  |      1 |    16.18   |    0.5419 |
|     370 | MPWR     | Open     | 2022-11-07   |      352.96   | 2026-11-20  |     14 | 11045.3    |    2.2352 |
|     371 | CAMT     | Open     | 2022-11-09   |       22.48   | 2026-11-20  |      1 |    66.72   |    2.968  |
|     372 | VOO      | Open     | 2022-12-06   |      362.03   | 2026-11-20  |     11 |  3008.61   |    0.7555 |
|     373 | NFLX     | Open     | 2023-01-23   |       35.742  | 2026-11-20  |      3 |    59.964  |    0.5592 |
|     374 | VSS      | Open     | 2023-02-14   |      111.02   | 2026-11-20  |      6 |   143.72   |    0.2158 |
|     375 | BLDR     | Open     | 2023-03-20   |       82.02   | 2026-11-20  |     12 |  -325.88   |   -0.3311 |
|     376 | KHC      | Open     | 2023-04-28   |       39.27   | 2026-11-20  |      3 |   -43.64   |   -0.3704 |
|     377 | AAPL     | Open     | 2023-06-14   |      183.95   | 2026-11-20  |     13 |  2060.93   |    0.8618 |
|     378 | VSS      | Open     | 2023-09-26   |      105.53   | 2026-11-20  |     12 |   354.32   |    0.2798 |
|     379 | MCHI     | Open     | 2023-10-16   |       43.29   | 2026-11-20  |     15 |    37.95   |    0.0584 |
|     380 | GOOGL    | Open     | 2024-02-01   |      141.16   | 2026-11-20  |     14 |  1737.82   |    0.8794 |
|     381 | BAC      | Open     | 2024-02-12   |       33.62   | 2026-11-20  |      5 |    64.1    |    0.3813 |
|     382 | MCHI     | Open     | 2024-02-22   |       39.77   | 2026-11-20  |      7 |    42.75   |    0.1536 |
|     383 | MPWR     | Open     | 2024-03-12   |      736.55   | 2026-11-20  |     11 |  4460.5    |    0.5505 |
|     384 | CAMT     | Open     | 2024-05-14   |       94.11   | 2026-11-20  |      4 |   -19.64   |   -0.0522 |
|     385 | META     | Open     | 2024-06-11   |      507.47   | 2026-11-20  |      8 |   426.96   |    0.1052 |
|     386 | MPWR     | Open     | 2024-06-18   |      852.56   | 2026-11-20  |     14 |  4051.86   |    0.3395 |
|     387 | AMD      | Open     | 2024-07-30   |      138.44   | 2026-11-20  |      3 |   857.85   |    2.0655 |
|     388 | MCHI     | Open     | 2024-10-25   |       49.85   | 2026-11-20  |      6 |   -22.98   |   -0.0768 |
|     389 | VOO      | Open     | 2024-11-13   |      549.03   | 2026-11-20  |     11 |   951.61   |    0.1576 |

---

## get_trade_statistics
Calculate the statistics of the trades of the portfolio (`get_trades`).

How many trades there were, how many made money, how much they made and lost, the profit factor, expectancy, System Quality Number and Kelly fraction, how long they lasted, the longest winning and losing streaks and how much of the time a trade was held. Every statistic but the counts, the Open PnL and the coverage is calculated on the closed trades, in the order they closed.

- Win Rate = W = number of trades with $$\text{PnL} > 0$$ / number of closed trades
- Payoff Ratio = R = mean(PnL⁺) / $$\vert \text{mean} (\text{PnL}^{-}) \vert$$
- Profit Factor = $$\sum \text{PnL}^{+} / \vert \sum \text{PnL}^{-} \vert$$
- Expectancy = W × mean(PnL⁺) − $$L \times \vert \text{mean} (\text{PnL}^{-}) \vert$$, with L the share of losing trades, the mean PnL per trade
- Expectancy Ratio = $$\text{Expectancy} / \vert \text{mean} (\text{PnL}^{-}) \vert$$, the expectancy in multiples of the average loss
- SQN = $$\sqrt{n}$$ × mean(PnL) / std(PnL), with n closed trades and ddof=1
- Kelly Criterion = W − (1 − W) / R
- Coverage = share of trading days since the first transaction with at least one trade held, Overlap Coverage = share of those days with more than one

Tharp defines the expectancy and the System Quality Number on R-multiples, the PnL of every trade divided by the risk taken on it. A trade list has no stops, so the PnL in currency takes its place: the SQN is the same for any constant risk per trade, and with the average loss as the risk the Expectancy Ratio is the expectancy in R. Tharp's later scoring caps n at $$100 (\sqrt{\min (n , 100)})$$; here n is the number of trades, as in vectorbt and backtesting.py, while backtrader divides the standard deviation by n rather than n − 1. The Expectancy is vectorbt's, in currency; backtesting.py's "Expectancy [%]" is the mean trade return, the Average Trade here, and its profit factor uses the trade returns rather than the PnL.

**Also known as:** trade analysis, trade statistics, win rate, hit ratio, profit factor, System Quality Number.

**References:**

- paper | Tharp, V.K. (2008). "Van Tharp's Definitive Guide to Position Sizing." International Institute of Trading Mastery.
- paper | Tharp, V.K. (2006). "Trade Your Way to Financial Freedom." 2nd edition, McGraw-Hill.
- paper | Kelly, J.L. (1956). "A New Interpretation of Information Rate." Bell System Technical Journal, 35(4), 917-926.
- library | Shares similar logic as vectorbt's [Trades.stats](https://vectorbt.dev/api/portfolio/trades/#vectorbt.portfolio.trades.Trades){:target="_blank"}
- library | Shares similar logic as vectorbt's [Ranges.coverage](https://vectorbt.dev/api/generic/ranges/#vectorbt.generic.ranges.Ranges.coverage){:target="_blank"} (coverage)
- library | Shares similar logic as backtesting.py's [Backtest.run](https://kernc.github.io/backtesting.py/doc/backtesting/backtesting.html#backtesting.backtesting.Backtest.run){:target="_blank"} (statistics)
- library | Shares similar logic as backtrader's [TradeAnalyzer](https://www.backtrader.com/docu/analyzers-reference/#tradeanalyzer){:target="_blank"}
- library | Shares similar logic as backtrader's [SQN](https://www.backtrader.com/docu/analyzers-reference/#sqn){:target="_blank"}

**Args:**

- <u>method (str, optional):</u> Which lots a sale closes first (see get_trades). Options are: "FIFO" (first in,
first out: the oldest lots close first), "LIFO" (last in, first out: the newest lots close first).
Defaults to "FIFO".
- <u>by (str &#124; None, optional):</u> How the trades are split. Options are: "direction" (the long and short trades
next to all of them), "ticker" (every ticker next to all of them). Defaults to None, all trades
together.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Portfolio's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The statistics as rows, with a column "All" and one per direction or
ticker: the number of Trades, Closed, Open, Long, Short, Winning and Losing Trades,
the Win Rate, Gross PnL, Costs, Net PnL and Open PnL, the Best, Worst, Average,
Average Winning and Average Losing Trade (returns), the Average, Average Winning and
Average Losing PnL, the Payoff Ratio, Profit Factor, Expectancy, Expectancy Ratio,
SQN and Kelly Criterion, the Average, Average Winning, Average Losing, Maximum and
Minimum Duration in calendar days, the Longest Winning and Losing Streak, the
Current Streak (positive for wins, negative for losses) and the Coverage and
Overlap Coverage.

**Notes:**

- A trade without a profit or loss counts as neither a win nor a loss and ends a streak.
- A ratio without losing (or winning) trades to divide by is NaN.

**As an example:**

```python
from financetoolkit import Portfolio

portfolio = Portfolio(example=True, api_key="FINANCIAL_MODELING_PREP_KEY")

portfolio.get_trade_statistics(by="direction")
```

Which returns:

|                          |         All |        Long |   Short |
|:-------------------------|------------:|------------:|--------:|
| Trades                   |    389      |    389      |       0 |
| Closed Trades            |    109      |    109      |       0 |
| Open Trades              |    280      |    280      |       0 |
| Long Trades              |    389      |    389      |       0 |
| Short Trades             |      0      |      0      |       0 |
| Winning Trades           |     72      |     72      |       0 |
| Losing Trades            |     37      |     37      |       0 |
| Win Rate                 |      0.6606 |      0.6606 |     nan |
| Gross PnL                |   3490.68   |   3490.68   |       0 |
| Costs                    |    165.025  |    165.025  |       0 |
| Net PnL                  |   3325.66   |   3325.66   |       0 |
| Open PnL                 | 735822      | 735822      |       0 |
| Best Trade               |    636.562  |    636.562  |     nan |
| Worst Trade              |    -16.2095 |    -16.2095 |     nan |
| Average Trade            |     14.2837 |     14.2837 |     nan |
| Average Winning Trade    |     22.2973 |     22.2973 |     nan |
| Average Losing Trade     |     -1.3103 |     -1.3103 |     nan |
| Average PnL              |     30.5106 |     30.5106 |     nan |
| Average Winning PnL      |     61.8463 |     61.8463 |     nan |
| Average Losing PnL       |    -30.4669 |    -30.4669 |     nan |
| Payoff Ratio             |      2.0299 |      2.0299 |     nan |
| Profit Factor            |      3.9502 |      3.9502 |     nan |
| Expectancy               |     30.5106 |     30.5106 |     nan |
| Expectancy Ratio         |      1.0014 |      1.0014 |     nan |
| SQN                      |      3.4601 |      3.4601 |     nan |
| Kelly Criterion          |      0.4933 |      0.4933 |     nan |
| Average Duration         |   3021.09   |   3021.09   |     nan |
| Average Winning Duration |   3541.26   |   3541.26   |     nan |
| Average Losing Duration  |   2008.86   |   2008.86   |     nan |
| Maximum Duration         |   8598      |   8598      |     nan |
| Minimum Duration         |      8      |      8      |     nan |
| Longest Winning Streak   |     21      |     21      |       0 |
| Longest Losing Streak    |      8      |      8      |       0 |
| Current Streak           |     -2      |     -2      |       0 |
| Coverage                 |      1      |      1      |       0 |
| Overlap Coverage         |      1      |      1      |     nan |

---

## get_position_timing
Calculate the timing of the positions of the portfolio as López de Prado describes it.

How often each position was flattened (sold to zero) or flipped (from long to short or back), the number of bets these end, and the average holding period of its units. A bet is a position held from the moment it opens until it is flattened or flipped, so the number of bets counts the independent positions taken in a ticker; a position still held ends a bet on the latest date. The average holding period weighs the time every unit was held by the units: each purchase moves the average entry time of the position towards its date, and each sale closes units held since that average entry time.

- Average Entry Time_t = (Average Entry Time_t-1 × $$\vert p_{t} - 1 \vert + t \times \vert \Delta p_{t} \vert$$) / &#124;p_t&#124; when the position grows
- Average Holding Period = $$\Sigma$$ (t − Average Entry Time) × &#124;units closed at $$t \vert / \sum$$ &#124;units closed&#124;

**Also known as:** bet frequency, holding period, flattening and flips.

**References:**

- paper | López de Prado, M. (2018). "Advances in Financial Machine Learning." Wiley, section 14.3 (Snippets 14.1 and 14.2).

**Args:**

- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Portfolio's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per ticker the number of Flattenings, Flips and Bets and the Average
Holding Period in calendar days.

**Notes:**

- The positions are the daily volumes of `get_positions_overview`. Units still held
have no holding period yet, so a ticker that was never sold has none (NaN).
- Over a position that ends flat, the average holding period equals the average
duration of its FIFO trades (`get_trades`) weighted by their size.
- There is no total for the portfolio, as units of different tickers do not add up.

**As an example:**

```python
from financetoolkit import Portfolio

portfolio = Portfolio(example=True, api_key="FINANCIAL_MODELING_PREP_KEY")

portfolio.get_position_timing()
```

Which returns:

|       |   Flattenings |   Flips |   Bets |   Average Holding Period |
|:------|--------------:|--------:|-------:|-------------------------:|
| ASML  |             0 |       0 |      1 |                 2982.51  |
| SKY   |             0 |       0 |      1 |                  714.509 |
| AMZN  |             0 |       0 |      1 |                 1791.41  |
| FIX   |             0 |       0 |      1 |                  874.215 |
| MSFT  |             0 |       0 |      1 |                 1506.19  |
| AMD   |             0 |       0 |      1 |                 3744.21  |
| AAPL  |             0 |       0 |      1 |                 2799.96  |
| FICO  |             0 |       0 |      1 |                 2173.02  |
| BAC   |             0 |       0 |      1 |                 2017.6   |
| ALGN  |             0 |       0 |      1 |                 1021.06  |
| CWST  |             0 |       0 |      1 |                 1862.59  |
| OXY   |             0 |       0 |      1 |                 3740.11  |
| WMT   |             0 |       0 |      1 |                  766.283 |
| CAMT  |             0 |       0 |      1 |                 2197.39  |
| NVDA  |             0 |       0 |      1 |                 2138.97  |
| NFLX  |             0 |       0 |      1 |                 3214.34  |
| GOOGL |             0 |       0 |      1 |                 4550.35  |
| MPWR  |             0 |       0 |      1 |                 2187.85  |
| BLDR  |             1 |       0 |      2 |                 1051.15  |
| VSS   |             0 |       0 |      1 |                 1805.36  |
| AVGO  |             0 |       0 |      1 |                 1460.42  |
| MCHI  |             0 |       0 |      1 |                 1280     |
| VOO   |             0 |       0 |      1 |                  978.32  |
| META  |             0 |       0 |      1 |                  nan     |
| KHC   |             0 |       0 |      1 |                  608.288 |
| EMXC  |             0 |       0 |      1 |                  960.277 |

---

## get_return_contributions
Calculate how much each position added to the portfolio's return in every period.

The periods are weeks, months, quarters or years, and the contributions add up to the portfolio's return of that period. Every day a position contributes its weight in the portfolio at the previous close times its return, $$c_{i,t} = w_{i,t} - 1 r_{i,t}$$, and over a longer period the daily contributions are carried by the growth of the portfolio since the period began, $$C_{i} = \sum_{t} c_{i,t} \Pi_{s < t} (1 + R_{s})$$, so they add up to the compounded return of the portfolio (Bacon, 2008). It is `toolkit.portfolio.get_return_contributions` with the weights of the positions as they moved from day to day.

The returns are the total returns of the assets (dividends reinvested) and the weights the Current Weight of the positions overview, so a purchase or a sale changes the weights from the next day on and is no return itself.

**Also known as:** contribution to return, return attribution by position.

**References:**

- paper | Bacon, C. R. (2008). "Practical Portfolio Performance Measurement and Attribution." 2nd edition, Wiley, chapter 5.
- library | Shares similar logic as PerformanceAnalytics (R)'s [to.period.contributions](https://github.com/cran/PerformanceAnalytics/blob/2.1.0/R/to.period.contributions.R#L45){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The period to add the contributions up over. Options are: "daily", "weekly",
"monthly", "quarterly", "yearly". Defaults to "monthly".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Portfolio's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per period the contribution of every position and the Portfolio
return.

**As an example:**

```python
from financetoolkit import Portfolio

portfolio = Portfolio(example=True, api_key="FINANCIAL_MODELING_PREP_KEY")

portfolio.get_return_contributions(period="yearly")[
    ["ASML", "MSFT", "NVDA", "AMZN", "Portfolio"]
]
```

Which returns:

| Date   |    ASML |    MSFT |    NVDA |    AMZN |   Portfolio |
|:-------|--------:|--------:|--------:|--------:|------------:|
| 2000   |  0.0919 | -0.2261 |  0      | -0.0067 |     -0.3338 |
| 2001   | -0.0367 |  0.1306 |  0      | -0.0005 |      0.4238 |
| 2002   | -0.0307 | -0.0517 |  0      |  0.0004 |     -0.1471 |
| 2003   |  0.1081 |  0.0148 |  0.0002 |  0.002  |      0.3673 |
| 2004   | -0.0334 |  0.0131 |  0      |  0.0003 |      0.1162 |
| 2005   |  0.0401 |  0      |  0.0001 |  0.0002 |      0.1153 |
| 2006   |  0.0407 |  0.0222 |  0.0006 | -0.0003 |      0.0813 |
| 2007   |  0.042  |  0.0235 |  0.0004 |  0.007  |      0.0047 |
| 2008   | -0.0793 | -0.0579 | -0.0012 | -0.0049 |     -0.4002 |
| 2009   |  0.1632 |  0.0634 |  0.0009 |  0.0144 |      0.488  |
| 2010   |  0.028  | -0.0073 | -0.0002 |  0.004  |      0.1289 |
| 2011   |  0.0237 | -0.0038 | -0.0001 | -0.0004 |     -0.0446 |
| 2012   |  0.097  |  0.0059 | -0.0001 |  0.0056 |      0.2123 |
| 2013   |  0.1062 |  0.0274 |  0.0002 |  0.0091 |      0.416  |
| 2014   |  0.0363 |  0.018  |  0.0001 | -0.004  |      0.1043 |
| 2015   | -0.0417 |  0.0158 |  0.0004 |  0.0202 |      0.1086 |
| 2016   |  0.0488 |  0.0123 |  0.0018 |  0.0038 |      0.238  |
| 2017   |  0.0992 |  0.0287 |  0.0017 |  0.02   |      0.4316 |
| 2018   | -0.0159 |  0.0138 | -0.0006 |  0.0124 |      0.0287 |
| 2019   |  0.1419 |  0.0426 |  0.0011 |  0.0127 |      0.592  |
| 2020   |  0.1134 |  0.0316 |  0.002  |  0.0353 |      0.5131 |
| 2021   |  0.1187 |  0.037  |  0.0034 |  0.0014 |      0.3203 |
| 2022   | -0.0695 | -0.0226 | -0.0023 | -0.0218 |     -0.2619 |
| 2023   |  0.0827 |  0.0431 |  0.0071 |  0.0233 |      0.6117 |
| 2024   | -0.0108 |  0.0094 |  0.0106 |  0.014  |      0.295  |
| 2025   |  0.0672 |  0.0093 |  0.0049 |  0.0018 |      0.234  |
| 2026   |  0.029  |  0.0006 | -0.0046 |  0.002  |     -0.0437 |

---

