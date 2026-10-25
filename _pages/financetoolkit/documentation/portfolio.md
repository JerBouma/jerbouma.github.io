---
title: Portfolio
seo_title: "Portfolio Module | Finance Toolkit"
seo_title_suffix: false
excerpt: The Portfolio module is meant to calculate important portfolio metrics allows you to compare your own portfolio to a benchmark, seeing performance of individual assets and directly load the portfolio into the Finance Toolkit.
description: "Reference for every function and parameter in the Finance Toolkit's Portfolio module: load your transactions, track holdings and compare to a benchmark."
author_profile: false
permalink: /projects/financetoolkit/docs/portfolio
classes: wide-sidebar
layout: single
redirect_from:
    - /portfolio
    - /projects/financetoolkit/portfolio-notebook
sidebar:
    nav: "financetoolkit-docs-portfolio"
---

The Portfolio module calculates important portfolio metrics, allowing you to compare your portfolio against a benchmark, analyze individual asset performance and load your portfolio directly into the Finance Toolkit.

To install the FinanceToolkit it simply requires the following:

```python
pip install financetoolkit -U
```

{% include algolia.html %}

{% include financetoolkit-getting-started/portfolio.md %}

## get_presets
List the classic portfolios that ship with the Finance Toolkit, to use with `Portfolio.from_preset`. Each is defined with real funds and the source of its allocation: the 60/40, Ray Dalio's All Weather, Harry Browne's Permanent Portfolio, the Golden Butterfly, the Bogleheads three-fund portfolio, Warren Buffett's 90/10, Nassim Taleb's barbell, a target-date glide path and more.

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
Create a Portfolio from one of the classic portfolios, by its identifier, name or alias (see `Portfolio.get_presets`), e.g. "60/40", "All Weather", "Permanent", "Golden Butterfly" or "Three Fund". It invests `initial_value` on `start_date` and rebalances as the definition says, after which every Portfolio and Toolkit analysis applies.

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
The portfolio as a `PortfolioDefinition`: the definition it was built from (a preset or weights), or, for holdings and transactions, the current weight of every position. It can be stored with `to_yaml` and read by other tools.

**Returns:**

PortfolioDefinition: The definition.

---

## toolkit
Converts the Portfolio to a Finance Toolkit object.

This method converts the Portfolio object to a Finance Toolkit object, enabling the use of the Toolkit's 500+ financial methods for the portfolio's assets. If the historical data of the assets or the benchmark cannot be collected, an empty DataFrame is returned instead.

Next to the historical data, the portfolio weights are also loaded in the Toolkit class. This, together with the "Portfolio" ticker, enables the possibility to calculate any Toolkit metric for all assets in the portfolio in combination with the Portfolio itself which is a weighted average of other results based on the portfolio weights over time.


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
If None, defaults to the configuration setting.
- <u>date_column (list[str] &#124; None):</u> List of column names for date information.
Defaults to configuration settings.
- <u>date_format_options (list[str] &#124; None):</u> List of date format strings to attempt when parsing
date columns (e.g. ['%Y-%m-%d', '%d/%m/%Y']). Defaults to configuration.
- <u>name_columns (list[str] &#124; None):</u> List of column names for transaction descriptions.
Defaults to configuration.
- <u>ticker_columns (list[str] &#124; None):</u> List of column names for asset tickers.
Defaults to configuration.
- <u>price_columns (list[str] &#124; None):</u> List of column names for asset prices.
Defaults to configuration.
- <u>volume_columns (list[str] &#124; None):</u> List of column names for asset volumes.
Defaults to configuration.
- <u>currency_columns (list[str] &#124; None):</u> List of column names for transaction currencies.
Defaults to configuration.
- <u>costs_columns (list[str] &#124; None):</u> List of column names for costs or income categories.
Defaults to configuration.
- <u>column_mapping (dict[str, str] &#124; None):</u> Dictionary mapping dataset columns to the appropriate field names.
Defaults to configuration.

**Returns:**

pd.DataFrame: A DataFrame containing the consolidated and processed portfolio data.

**Raises:**

FileNotFoundError: If any of the files or directories specified in 'excel_location' cannot be found.
ValueError: If essential columns (date, description, amount) are missing in the dataset or configuration.
- Columns can be specified in the configuration or provided explicitly.
- For missing cost or income columns, an exception is raised if no valid configuration is found.

**Notes:**

- Duplicates are handled according to configuration settings ('self._cfg["general"]["adjust_duplicates"]').
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
- Dividends: the dividends of the benchmark over time. -

**Returns:** the returns of the benchmark over time.
- Cumulative Return: the cumulative return of the benchmark over time.

Volatility, Excess Return and Excess Volatility are not included here. These are
available via the Risk module (e.g. toolkit.risk.get_volatility) and the Performance
module (e.g. toolkit.performance.get_excess_return) instead.

This method retrieves historical benchmark data (daily, weekly, monthly, quarterly, and yearly)
for the portfolio, based on a specified benchmark ticker or a mapping of portfolio tickers to
their corresponding benchmark tickers. The retrieved benchmark data is then aligned with the
portfolio's historical data, ensuring that the dates of the benchmark data match the dates of
the portfolio's transactions.

The method can retrieve data for a single benchmark ticker or for multiple benchmarks depending
on the portfolio tickers. The resulting benchmark data is returned in a structured DataFrame.

**Args:**

- <u>benchmark_ticker (str &#124; None):</u> The benchmark ticker symbol. Defaults to None, the benchmark ticker
given to the Portfolio, or the one of the configuration file when none was given.

**Returns:**

pd.DataFrame: A DataFrame containing the benchmark data for the portfolio, indexed by the portfolio's dates,
or an empty DataFrame (with an error logged) when the benchmark has no historical data.

**Notes:**

- The benchmark data is retrieved in daily, weekly, monthly, quarterly, and yearly periods.
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
weekly to yearly data are in the currency most of the portfolio's tickers are traded in.
- The method updates several internal attributes:
- `self._daily_benchmark_data`: Daily benchmark data.
- `self._weekly_benchmark_data`: Weekly benchmark data.
- `self._monthly_benchmark_data`: Monthly benchmark data.
- `self._quarterly_benchmark_data`: Quarterly benchmark data.
- `self._yearly_benchmark_data`: Yearly benchmark data.
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
- Dividends: the dividends of each asset over time. -

**Returns:** the returns of each asset over time.
- Cumulative Return: the cumulative return of each asset over time.

Volatility, Excess Return and Excess Volatility are not included here. These are
available via the Risk module (e.g. toolkit.risk.get_volatility) and the Performance
module (e.g. toolkit.performance.get_excess_return) instead.

This method retrieves historical price data (daily, weekly, monthly, quarterly, and yearly)
for the portfolio's tickers and adjusts for any currency mismatches if necessary. It fetches
data from a specified data source, applies currency conversion where applicable, and stores the
adjusted data in separate DataFrames for different time periods (daily, weekly, monthly, quarterly, yearly).

The method uses the Toolkit class to fetch historical price data and the Currency Toolkit to
handle currency conversions if the portfolio’s transaction currency does not match the historical
data's currency.

**Args:**

- <u>rounding (int &#124; None):</u> An optional integer specifying the number of decimal places to round the
historical price data. If None, the default rounding value is used.

**Returns:**

pd.DataFrame: A DataFrame containing the adjusted daily historical price data for the portfolio.

**Notes:**

- This method utilizes the `Toolkit` class to fetch historical price data for different periods.
- Currency adjustments are made if there's a mismatch between the transaction and historical data currencies.
- The method handles ISIN-to-ticker mapping when ISIN codes are provided in the portfolio data.
- The adjusted historical data is returned in separate DataFrames for daily, weekly, monthly, quarterly,
and yearly price data.
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
- Cumulative Return: the total return on the capital deployed, i.e. (Current Value + Realized Proceeds + Dividends - Invested Amount) / Invested Amount. It is NaN before the first purchase, when no capital has been deployed yet.
- Invested Weight: the weight of the asset in the portfolio based on the invested amount over time.
- Current Weight: the weight of the asset in the portfolio based on the current value over time.

Positions are marked at the traded closing price, the basis of the transaction prices, and the dividends are added as cash when they are paid, so the cumulative return is a total return and "Current Value" is the market value quoted on that date.

A transaction booked on a day without a price, such as a weekend or an exchange holiday, is carried forward to the first following day that does have one.

This method computes an overview of the portfolio's positions by calculating important statistics and performance metrics based on the historical data and transactions. If necessary data has not been collected, it will trigger the collection of historical and benchmark data using the `collect_historical_data` and `collect_benchmark_historical_data` methods. Additionally, it will compute an overview of transactions using the `get_transactions_overview` method.

The resulting overview includes information about the positions, such as the value, performance, and other key metrics. The data is rounded to the specified precision before being returned.

**Args:**

- <u>rounding (int &#124; None):</u> An optional integer specifying the number of decimal places to round the data.
If None, the default rounding precision is used.

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
- Volatility: The annualized volatility of the asset's daily returns over the most recent 252 trading days. For the aggregated "Portfolio" row, this is derived from the full covariance matrix of the underlying asset returns over the same days (Var_p = w^T * Cov * w, Markowitz, 1952) rather than a weighted average of individual volatilities, since the latter ignores diversification from imperfectly correlated assets.
- Benchmark Volatility: The annualized volatility of the benchmark's daily returns over the most recent 252 trading days.
- Alpha: The alpha is based on the difference between the asset's return and the benchmark return.
- Beta: The beta of the asset's daily returns against the benchmark's over the most recent 252 trading days, the window of the Volatility column. A beta >1 indicates that the asset is more volatile than the benchmark and a beta <1 indicates that the asset is less volatile than the benchmark.
- Weight: The weight of the asset in the portfolio based on the latest market value and the total market value of the portfolio.

Positions are valued at the traded closing price, the basis of the transaction prices, and dividends are added as cash, for the asset and the benchmark alike, so Return and Benchmark Return are total returns on the same basis.

No inventory method (FIFO, LIFO or average cost) is applied here: "Return" measures the result of every unit of currency put into the position rather than the basis of the units that happen to remain. The inventory methods drive the realized PnL in get_transactions_overview instead.

The "Portfolio" row sums or averages units of different assets for "Volume", "Price" and "Latest Price", so those three carry no economic meaning at the portfolio level.

When recalculating these numbers, it is important to note that results are calculated before the rounding parameter is applied which can lead to some discrepancies in the results.

This method computes a detailed overview of the portfolio, calculating various key statistics such as performance, costs, and returns. If necessary data has not been collected, it will automatically trigger data collection using the `collect_historical_data` and `collect_benchmark_historical_data` methods. The portfolio overview is generated based on the portfolio dataset and benchmark data, and is rounded to the specified precision before being returned.

**Args:**

- <u>include_portfolio (bool):</u> A boolean flag indicating whether the portfolio itself should be included
in the overview. Defaults to `True`.
- <u>exclude_sold_positions (bool):</u> A flag indicating whether to exclude sold positions from the overview.
- <u>rounding (int &#124; None):</u> An optional integer specifying the number of decimal places to round the data.
If None, the default rounding precision is used.

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
| MPWR         |      116 |     -27 | 250.893  |  30636     |       1140.12  |      132254    |    3301.39  |   3.4394 |      105369    |             0.7644 |       0.5485 |                 0.1274 |  2.675  |  2.5783 |   0.1365 |
| MSFT         |      105 |     -11 |  50.1726 |   5529.99  |        524.51  |       55073.6  |    3367.52  |   9.5947 |       53058.8  |             3.3786 |       0.3292 |                 0.1274 |  6.2161 |  1.0354 |   0.0569 |
| NFLX         |      114 |     -32 |  13.0791 |   1666.89  |         65.85  |        7506.9  |       0     |   3.6304 |        6051.53 |             1.3813 |       0.3572 |                 0.1274 |  2.2491 |  0.2488 |   0.0077 |
| NVDA         |       69 |     -27 |   2.1717 |    202.909 |        210.96  |       14556.2  |      49.646 |  71.138  |       14434.5  |             1.0556 |       0.3761 |                 0.1274 | 70.0824 |  1.9435 |   0.015  |
| OXY          |       27 |     -15 |  52.3833 |   2005.56  |         64.17  |        1732.59 |     876.077 |   0.5181 |        1039    |             2.7097 |       0.3494 |                 0.1274 | -2.1916 | -0.7819 |   0.0018 |
| SKY          |      126 |     -23 |  24.4134 |   3343.23  |         78.92  |        9943.92 |     901.062 |   2.3234 |        7767.74 |             4.8301 |       0.4542 |                 0.1274 | -2.5067 |  1.0893 |   0.0103 |
| VOO          |       77 |     -12 | 256.027  |  20238.2   |        698.58  |       53790.7  |    3863.3   |   1.867  |       37784.6  |             1.6782 |       0.1268 |                 0.1274 |  0.1888 |  0.9928 |   0.0555 |
| VSS          |       98 |     -21 |  94.9125 |  10366.5   |        149.35  |       14636.3  |    3122.51  |   0.8093 |        8390.01 |             2.4396 |       0.1664 |                 0.1274 | -1.6303 |  1.0607 |   0.0151 |
| WMT          |       92 |     -18 |  22.2477 |   2265.02  |        119.89  |       11029.9  |     965.758 |   4.37   |        9898.01 |             3.409  |       0.2626 |                 0.1274 |  0.9609 | -0.0971 |   0.0114 |
| Portfolio    |     2142 |    -532 |  55.8595 | 134818     |        452.235 |      968688    |   35730.9   |   8.8928 |      878276    |             2.5365 |       0.2752 |                 0.1274 |  6.3563 |  1.7913 |   1      |

---

## get_portfolio_performance
Calculate portfolio performance metrics for a specified period.

This method calculates key performance metrics, such as returns, for the portfolio over a specified period. The available periods are 'yearly', 'quarterly', 'monthly', 'weekly', and 'daily'. It uses the positions overview dataset for these calculations. If the necessary data has not been collected, it triggers the collection of historical and benchmark data.

**Args:**

- <u>period (str &#124; None):</u> The time period for which portfolio performance metrics should be calculated.
It can be one of the following: 'yearly', 'quarterly', 'monthly', 'weekly', or 'daily'.
If None, the default period is 'quarterly' (if the 'quarterly' attribute is set to True),
otherwise, it defaults to 'yearly'.
- <u>exclude_sold_positions (bool):</u> A flag indicating whether to exclude sold positions.
- <u>rounding (int &#124; None):</u> The number of decimal places to round the output to.
If None, it defaults to the rounding precision specified in the configuration.

**Returns:**

pd.DataFrame: A DataFrame containing the portfolio performance metrics for the specified period.

**Raises:**

ValueError: If an invalid or unsupported period is provided.
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
| (Period('2026-10-05/2026-10-11', 'W-SUN'), 'META') |       15 |      -1 |          4813.61  |               0     |      81.125 |        10780    |            0.0357 |           0.0099 |   1.2563 |
| (Period('2026-10-05/2026-10-11', 'W-SUN'), 'MPWR') |      116 |     -27 |         30636     |             449.4   |    3301.39  |       160810    |            0.2272 |           0.147  |   4.3715 |
| (Period('2026-10-05/2026-10-11', 'W-SUN'), 'MSFT') |      105 |     -11 |          5529.99  |             147.7   |    3367.52  |        56182.3  |            0.041  |           0.0513 |   9.7952 |
| (Period('2026-10-05/2026-10-11', 'W-SUN'), 'NFLX') |      114 |     -32 |          1666.89  |             211.515 |       0     |         8014.2  |            0.0124 |           0.0073 |   3.9348 |
| (Period('2026-10-05/2026-10-11', 'W-SUN'), 'NVDA') |       69 |     -27 |           202.909 |              31.547 |      49.646 |        15820.3  |            0.0015 |           0.0145 |  77.3678 |
| (Period('2026-10-05/2026-10-11', 'W-SUN'), 'OXY')  |       27 |     -15 |          2005.56  |             435.898 |     876.077 |         1622.97 |            0.0149 |           0.0015 |   0.4634 |
| (Period('2026-10-05/2026-10-11', 'W-SUN'), 'SKY')  |      126 |     -23 |          3343.23  |             265.99  |     901.062 |        10033.4  |            0.0248 |           0.0092 |   2.3502 |
| (Period('2026-10-05/2026-10-11', 'W-SUN'), 'VOO')  |       77 |     -12 |         20238.2   |             368.76  |    3863.3   |        55100.4  |            0.1501 |           0.0504 |   1.9317 |
| (Period('2026-10-05/2026-10-11', 'W-SUN'), 'VSS')  |       98 |     -21 |         10366.5   |             997.66  |    3122.51  |        15201.8  |            0.0769 |           0.0139 |   0.8639 |
| (Period('2026-10-05/2026-10-11', 'W-SUN'), 'WMT')  |       92 |     -18 |          2265.02  |             167.39  |     965.758 |        10244.2  |            0.0168 |           0.0094 |   4.0231 |

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
- <u>pnl_method (str):</u> The method for calculating profit & loss. Options are:
'FIFO' (First In, First Out), 'LIFO' (Last In, First Out), or 'AVERAGE'.
Defaults to 'FIFO'.

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

- <u>period (str &#124; None):</u> The time period for which transaction performance metrics
should be calculated. This can be one of the following: 'yearly', 'quarterly',
'monthly', 'weekly', or 'daily'. If None, the default is 'quarterly' if
the 'quarterly' attribute is set to True, otherwise 'yearly'.
- <u>exclude_sold_positions (bool):</u> A flag indicating whether to exclude sold positions
- <u>rounding (int &#124; None):</u> The number of decimal places to round the output to.
If None, it defaults to the rounding specified in the configuration.

**Returns:**

pd.DataFrame: A DataFrame containing transaction performance metrics, including
returns, costs, and benchmarks, for the specified period.

**Raises:**

ValueError: If an invalid or unsupported period is provided or if there is an issue
with creating the transaction performance metrics.

**Notes:**

- The method supports multiple time periods ('yearly', 'quarterly', 'monthly',
'weekly', 'daily') for calculating transaction performance metrics.
- If no period is provided, it defaults to 'quarterly' or 'yearly' based on the
configuration.
- The end-of-period prices and dividends are taken from the daily data, in the currency of
each ticker's transactions for the asset and the benchmark alike.
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
| (Period('2023Q4', 'Q-DEC'), 'MCHI')  |       15 |   43.29 |      -3 |            652.35 |                   0 |          611.1  |     14.9115 |  -0.0404 |             0.0856 | -0.1259 |
| (Period('2024Q1', 'Q-DEC'), 'BAC')   |        5 |   33.62 |      -3 |            171.1  |                   0 |          189.6  |      1.2    |   0.1151 |             0.028  |  0.0872 |
| (Period('2024Q1', 'Q-DEC'), 'GOOGL') |       14 |  141.16 |       0 |           1976.24 |                   0 |         2113.02 |      0      |   0.0692 |             0.071  | -0.0018 |
| (Period('2024Q1', 'Q-DEC'), 'MCHI')  |        7 |   39.77 |      -1 |            279.39 |                   0 |          278.11 |      0      |  -0.0046 |             0.0292 | -0.0338 |
| (Period('2024Q1', 'Q-DEC'), 'MPWR')  |       11 |  736.55 |       0 |           8102.05 |                   0 |         7451.62 |     13.75   |  -0.0786 |             0.0153 | -0.0939 |
| (Period('2024Q2', 'Q-DEC'), 'CAMT')  |        4 |   94.11 |       0 |            376.44 |                   0 |          500.96 |      0      |   0.3308 |             0.0407 |  0.29   |
| (Period('2024Q2', 'Q-DEC'), 'META')  |        8 |  507.47 |       0 |           4059.76 |                   0 |         4033.76 |      4      |  -0.0054 |             0.0158 | -0.0213 |
| (Period('2024Q2', 'Q-DEC'), 'MPWR')  |       14 |  852.56 |      -1 |          11936.8  |                   0 |        11503.5  |     17.5    |  -0.0348 |            -0.0049 | -0.0299 |
| (Period('2024Q4', 'Q-DEC'), 'MCHI')  |        6 |   49.85 |       0 |            299.1  |                   0 |          281.16 |      5.3466 |  -0.0421 |             0.0127 | -0.0548 |
| (Period('2024Q4', 'Q-DEC'), 'VOO')   |       11 |  549.03 |       0 |           6039.33 |                   0 |         5926.91 |     19.1235 |  -0.0154 |            -0.0173 |  0.0019 |

---

## get_money_weighted_return
Calculate the money-weighted return of every position and of the whole portfolio: the annual rate at which the money put in grew into the money taken out plus the value still held (the internal rate of return, or XIRR, of the transactions).

Unlike the time-weighted return, it depends on when money was added: buying more just before a rally raises it and buying at a peak lowers it. It therefore measures the investor's own result, including the timing of every purchase and sale, rather than the result of the assets alone.

The cash flows are every purchase (money in, including costs), every sale (money out, after costs), every cash dividend received (money out, on its ex-dividend date) and the latest value of the positions still held, on the last date of the historical data.

For more information, see the following book:

- Bacon, C.R. (2008). "Practical Portfolio Performance Measurement and Attribution." Wiley, 2nd edition, chapter 2.

**Also known as:** internal rate of return, IRR, XIRR, dollar-weighted return.

**Args:**

- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Portfolio's rounding.

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
| ASML      |   6348.35  |    736.149 |    8610.47  |      202762    | 2000-01-07          |                  0.2123 |
| SKY       |   3339.23  |    261.99  |     901.062 |        9943.92 | 2000-01-10          |                  0.0652 |
| AMZN      |   5042.91  |    192.851 |       0     |       28768    | 2000-01-28          |                  0.2054 |
| FIX       |   1976.93  |     18.43  |    1294.06  |      141625    | 2000-02-23          |                  0.2513 |
| MSFT      |   5529.99  |    147.7   |    3367.52  |       55073.6  | 2000-02-28          |                  0.1359 |
| AMD       |   2384.36  |   1431.84  |       0     |       40309.6  | 2000-04-27          |                  0.1462 |
| AAPL      |   5750.96  |    266.963 |    1246.48  |       47639    | 2000-05-08          |                  0.2784 |
| FICO      |   4917.94  |    576.42  |     102.122 |       94576    | 2000-06-01          |                  0.1659 |
| BAC       |   2401.58  |    303.8   |     888.08  |        4044.8  | 2000-11-16          |                  0.0672 |
| ALGN      |   9918     |    324.77  |       0     |       12515.3  | 2001-09-18          |                  0.0334 |
| CWST      |   1373.89  |     91.95  |       0     |        6149.43 | 2001-10-15          |                  0.1339 |
| OXY       |   1994.56  |    424.898 |     876.077 |        1732.59 | 2001-11-16          |                  0.0404 |
| WMT       |   2261.02  |    163.39  |     965.758 |       11029.9  | 2001-12-28          |                  0.1285 |
| CAMT      |    546.73  |    104.06  |      67.87  |        5088.72 | 2002-08-07          |                  0.2856 |
| NVDA      |    201.303 |     29.941 |      49.646 |       14556.2  | 2002-09-20          |                  0.3245 |
| NFLX      |   1662.85  |    207.478 |       0     |        7506.9  | 2002-11-18          |                  0.207  |
| GOOGL     |   4668.1   |    359.26  |     304.08  |       46750.7  | 2004-08-24          |                  0.2196 |
| MPWR      |  30633     |    446.4   |    3301.39  |      132254    | 2005-09-16          |                  0.2745 |
| BLDR      |   1682.82  |    121.254 |       0     |        2728.8  | 2006-12-22          |                  0.1004 |
| VSS       |  10364.5   |    995.66  |    3122.51  |       14636.3  | 2009-06-05          |                  0.0765 |
| AVGO      |   1568.81  |    134.64  |    6096.41  |       21230.9  | 2009-11-02          |                  0.5773 |
| MCHI      |   2965.43  |    139.96  |     336.097 |        2646    | 2011-04-26          |                  0.0093 |
| VOO       |  20238.2   |    368.76  |    3863.3   |       53790.7  | 2011-12-20          |                  0.1506 |
| META      |   4813.61  |      0     |      81.125 |        9639.3  | 2012-06-20          |                  0.1931 |
| KHC       |    722.41  |    242.21  |     108.25  |         223.2  | 2017-03-07          |                 -0.0525 |
| EMXC      |   1403.3   |    477.33  |     148.616 |        1467.36 | 2019-05-03          |                  0.0893 |
| Portfolio | 134711     |   8568.1   |   35730.9   |      968688    | 2000-01-07          |                  0.1763 |

---

