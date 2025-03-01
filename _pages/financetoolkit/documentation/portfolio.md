---
title: Portfolio
excerpt: The Portfolio module is meant to calculate important portfolio metrics allows you to compare your own portfolio to a benchmark, seeing performance of individual assets and directly load the portfolio into the Finance Toolkit.
description: The Portfolio module is meant to calculate important portfolio metrics allows you to compare your own portfolio to a benchmark, seeing performance of individual assets and directly load the portfolio into the Finance Toolkit.
author_profile: false
permalink: /projects/financetoolkit/docs/portfolio
classes: wide-sidebar
layout: single
redirect_from:
    - /economics
sidebar:
    nav: "financetoolkit-docs-portfolio"
---

The Portfolio module is meant to calculate important portfolio metrics allows you to compare your own portfolio to a benchmark, seeing performance of individual assets and directly load the portfolio into the Finance Toolkit.

To install the FinanceToolkit it simply requires the following:

{% include code_header.html %}
{% highlight bash %}
pip install financetoolkit -U
{% endhighlight %}

If you are looking for documentation regarding the toolkit, discovery, ratios, models, technicals, fixed income, risk, performance and economics, please have a look below:

<div style="display: flex; justify-content: space-between;" class="show-on-desktop">
    <a href="/projects/financetoolkit/docs" class="btn btn--info" style="flex: 1;font-size:10px;margin-right:5px">Toolkit</a>
    <a href="/projects/financetoolkit/docs/discovery" class="btn btn--info" style="flex: 1;font-size:10px;margin-right:5px">Discovery</a>
    <a href="/projects/financetoolkit/docs/ratios" class="btn btn--info" style="flex: 1;font-size:10px;margin-right:5px">Ratios</a>
    <a href="/projects/financetoolkit/docs/models" class="btn btn--info" style="flex: 1;font-size:10px;margin-right:5px">Models</a>
    <a href="/projects/financetoolkit/docs/options" class="btn btn--info" style="flex: 1;font-size:10px;margin-right:5px">Options</a>
    <a href="/projects/financetoolkit/docs/technicals" class="btn btn--info" style="flex: 1;font-size:10px;margin-right:5px">Technicals</a>
    <a href="/projects/financetoolkit/docs/fixedincome" class="btn btn--info" style="flex: 1;font-size:10px;margin-right:5px">Fixed Income</a>
    <a href="/projects/financetoolkit/docs/risk" class="btn btn--info" style="flex: 1;font-size:10px;margin-right:5px">Risk</a>
    <a href="/projects/financetoolkit/docs/performance" class="btn btn--info" style="flex: 1;font-size:10px;margin-right:5px">Performance</a>
    <a href="/projects/financetoolkit/docs/economics" class="btn btn--info" style="flex: 1;font-size:10px;margin-right:5px">Economics</a>
    <a href="/projects/financetoolkit/docs/portfolio" class="btn btn--warning" style="flex: 1;font-size:10px;">Portfolio</a>
</div>

{% include algolia.html %}

## __init__
Initialize the Portfolio class with the provided configuration file and portfolio dataset.
 This constructor sets up a portfolio management instance, configuring it with a dataset (either as a pandas DataFrame or a file path to an Excel/CSV file), a benchmark ticker for performance comparison, and various settings specified through a configuration file (YAML format). The configuration file defines key columns for cash flow analysis, such as date columns, asset tickers, price, volume, and transaction costs. It also allows for the use of quarterly data and fetching of historical financial data via an API.

**Args:**
 - <u>portfolio_dataset (pd.DataFrame | str | None):</u> A pandas DataFrame containing the portfolio dataset,
 or a file path to an Excel/CSV file containing the portfolio data. If None, the dataset must
 be loaded later using the `read_portfolio_dataset` method.
 - <u>benchmark_ticker (str | None):</u> The ticker symbol for the benchmark asset used for performance comparison.
 If None, the benchmark ticker specified in the configuration file will be used.
 - <u>api_key (str):</u> The API key for accessing financial data and historical metrics. If not provided, only
 basic historical data and indicators are available.
 - <u>quarterly (bool):</u> Flag to specify whether to use quarterly data for performance metrics. Defaults to False
 (yearly data).
 - <u>example (bool):</u> Flag to use example configuration and dataset files for demonstration purposes.
 If True, example files are downloaded and used.
 - <u>configuration_file (str | None):</u> Path to a YAML configuration file defining portfolio settings.
 If None, the default configuration file is used.
 - <u>rounding (int):</u> The number of decimal places to round the outputs. Defaults to 4 decimal places.

 **Raises:**
 ValueError: If the provided configuration file is not in YAML format.
 ValueError: If no portfolio dataset is provided and `example` is set to False.
## toolkit
Converts the Portfolio to a Finance Toolkit object.
 This method converts the Portfolio object to a Finance Toolkit object, enabling the use of the Toolkit's 150+ financial metrics and indicators for the portfolio's assets.
 Next to the historical data, the portfolio weights are also loaded in the Toolkit class. This, together with the "Portfolio" ticker, enables the possibility to calculate any Toolkit metric for all assets in the portfolio in combination with the Portfolio itself which is a weighted average of other results based on the portfolio weights over time.

## read_portfolio_dataset
Read and consolidate cash flow data from Excel or CSV files into a single DataFrame.
 This method consolidates portfolio data from one or more Excel or CSV files. It processes the data by identifying and handling duplicate entries, adjusting for the required date format, and renaming columns based on configuration or user inputs. It ensures consistency across transaction details, including descriptions, amounts, costs, and currencies, before returning the data as a structured DataFrame.
 The function also allows for customization of the column names used in the dataset, including columns for transaction dates, asset tickers, prices, volumes, and costs/incomes. If necessary, adjustments can be made to handle duplicated entries in the dataset based on configuration settings.

**Args:**
 - <u>adjust_duplicates (bool | None):</u> Flag to indicate whether to adjust duplicate rows in the dataset.
 If None, defaults to the configuration setting.
 - <u>date_column (list[str] | None):</u> List of column names for date information.
 Defaults to configuration settings.
 - <u>date_format (str | None):</u> The format for date columns, specified as a string.
 Defaults to configuration.
 - <u>name_columns (list[str] | None):</u> List of column names for transaction descriptions.
 Defaults to configuration.
 - <u>ticker_columns (list[str] | None):</u> List of column names for asset tickers.
 Defaults to configuration.
 - <u>price_columns (list[str] | None):</u> List of column names for asset prices.
 Defaults to configuration.
 - <u>volume_columns (list[str] | None):</u> List of column names for asset volumes.
 Defaults to configuration.
 - <u>currency_columns (list[str] | None):</u> List of column names for transaction currencies.
 Defaults to configuration.
 - <u>costs_columns (list[str] | None):</u> List of column names for costs or income categories.
 Defaults to configuration.
 - <u>column_mapping (dict[str, str] | None):</u> Dictionary mapping dataset columns to the appropriate field names.
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
- Volatility: the volatility of the benchmark over the whole period. 
- Excess Return: the excess return (return minus risk free rate) of the benchmark over time. 
- Excess Volatility: the excess volatility (return minus risk free rate) of the benchmark over time. 
- Cumulative Return: the cumulative return of the benchmark over time.
 This method retrieves historical benchmark data (daily, weekly, monthly, quarterly, and yearly) for the portfolio, based on a specified benchmark ticker or a mapping of portfolio tickers to their corresponding benchmark tickers. The retrieved benchmark data is then aligned with the portfolio's historical data, ensuring that the dates of the benchmark data match the dates of the portfolio's transactions.
 The method can retrieve data for a single benchmark ticker or for multiple benchmarks depending on the portfolio tickers. The resulting benchmark data is returned in a structured DataFrame.

**Args:**
 - <u>benchmark_ticker (str | None):</u> The default benchmark ticker symbol to use if no per-ticker mapping
 is provided. If None, the default benchmark ticker is retrieved from the configuration.

 **Returns:**
 pd.DataFrame: A DataFrame containing the benchmark data for the portfolio, indexed by the portfolio's dates.

 **Notes:**
 - The benchmark data is retrieved in daily, weekly, monthly, quarterly, and yearly periods.
 - If a specific date in the benchmark data does not exist, the method uses the previous available value.
 - The benchmark prices are aligned with the portfolio's data, using a backfill method for missing dates.
 - The method updates several internal attributes:
 - `self._daily_benchmark_data`: Daily benchmark data.
 - `self._weekly_benchmark_data`: Weekly benchmark data.
 - `self._monthly_benchmark_data`: Monthly benchmark data.
 - `self._quarterly_benchmark_data`: Quarterly benchmark data.
 - `self._yearly_benchmark_data`: Yearly benchmark data.
 - `self._benchmark_prices`: Adjusted close prices for the benchmark.
 - `self._benchmark_prices_per_ticker`: Benchmark prices for each ticker.
 - `self._latest_benchmark_price`: The latest available benchmark price.
 - `self._benchmark_specific_prices`: The specific benchmark price for each portfolio transaction.
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
- Volatility: the volatility of each asset over the whole period. 
- Excess Return: the excess return (return minus risk free rate) of each asset over time. 
- Excess Volatility: the excess volatility (return minus risk free rate) of each asset over time. 
- Cumulative Return: the cumulative return of each asset over time.
 This method retrieves historical price data (daily, weekly, monthly, quarterly, and yearly) for the portfolio's tickers and adjusts for any currency mismatches if necessary. It fetches data from a specified data source, applies currency conversion where applicable, and stores the adjusted data in separate DataFrames for different time periods (daily, weekly, monthly, quarterly, yearly).
 The method uses the Toolkit class to fetch historical price data and the Currency Toolkit to handle currency conversions if the portfolio’s transaction currency does not match the historical data's currency.

**Args:**
 - <u>rounding (int | None):</u> An optional integer specifying the number of decimal places to round the
 historical price data. If None, the default rounding value is used.
 - <u>progress_bar (bool):</u> A boolean indicating whether to show a progress bar during data retrieval.

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
 - The latest adjusted price is also captured and available in the `self._latest_price` attribute.
 - If currency conversions are applied, a warning is displayed when mismatches between transaction and
 historical data currencies are found (e.g., for ISIN codes).
## get_positions_overview
Calculate and provide an overview of the portfolio's positions, including key statistics and performance metrics.
 The following columns are included:
 
- Volume: the volume of each asset over time. 
- Costs: the costs of each asset over time. 
- Invested Amount: the invested amount over time. 
- Current Value: the current value of the asset based on the market value on that specific day over time. 
- Cumulative Return: the cumulative return of the asset over time. 
- Invested Weight: the weight of the asset in the portfolio based on the invested amount over time. 
- Current Weight: the weight of the asset in the portfolio based on the current value over time.
 This method computes an overview of the portfolio's positions by calculating important statistics and performance metrics based on the historical data and transactions. If necessary data has not been collected, it will trigger the collection of historical and benchmark data using the `collect_historical_data` and `collect_benchmark_historical_data` methods. Additionally, it will compute an overview of transactions using the `get_transactions_overview` method.
 The resulting overview includes information about the positions, such as the value, performance, and other key metrics. The data is rounded to the specified precision before being returned.

**Args:**
 - <u>rounding (int | None):</u> An optional integer specifying the number of decimal places to round the data.
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
## get_portfolio_overview
Calculate and provide an overview of the portfolio's key statistics, including performance metrics and cost
-related information.
 The following columns are included:
 
- Identifier: The name of the asset, specifically the ticker (e.g. AAPL) 
- Volume: The total volume of the asset representing all transactions. 
- Costs: The total costs associated with the asset transactions. 
- Price: The mean price of the asset based on the transactions. 
- Invested: The total amount invested in the asset, this is the Price times the Volume minus Costs. 
- Latest Price: The latest available price of the asset obtained from historical data. 
- Latest Value: The total value of the asset based on the latest price and the total volume minus costs. 
- Return: The return of the asset based on the latest value and invested amount. 
- Return Value: The absolute return value of the asset based on the latest value and invested amount. 
- Benchmark Return: The return of the asset's benchmark based on the latest value and invested amount. 
- Volatility: The yearly volatility of the asset based on the historical data, this computes the volatility over the entire period and multiplies this number by SQRT(252). 
- Benchmark Volatility: The yearly volatility of the asset's benchmark based on the historical data, this computes the volatility over the entire period and multiplies this number by SQRT(252). 
- Alpha: The alpha is based on the difference between the asset's return and the benchmark return. 
- Beta: The beta is based on the asset's return and the benchmark return. It measures the asset's volatility compared to the benchmark. A beta >1 indicates that the asset is more volatile than the benchmark and a beta <1 indicates that the asset is less volatile than the benchmark. 
- Weight: The weight of the asset in the portfolio based on the latest value and the total value of the portfolio.
 When recalculating these numbers, it is important to note that results are calculated before the rounding parameter is applied which can lead to some discrepancies in the results.
 This method computes a detailed overview of the portfolio, calculating various key statistics such as performance, costs, and returns. If necessary data has not been collected, it will automatically trigger data collection using the `collect_historical_data` and `collect_benchmark_historical_data` methods. The portfolio overview is generated based on the portfolio dataset and benchmark data, and is rounded to the specified precision before being returned.

**Args:**
 - <u>include_portfolio (bool):</u> A boolean flag indicating whether the portfolio itself should be included
 in the overview. Defaults to `True`.
 - <u>exclude_sold_positions (bool):</u> A flag indicating whether to exclude sold positions from the overview.
 - <u>rounding (int | None):</u> An optional integer specifying the number of decimal places to round the data.
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
## get_portfolio_performance
Calculate portfolio performance metrics for a specified period.
 This method calculates key performance metrics, such as returns, for the portfolio over a specified period. The available periods are 'yearly', 'quarterly', 'monthly', 'weekly', and 'daily'. It uses the positions overview dataset for these calculations. If the necessary data has not been collected, it triggers the collection of historical and benchmark data.

**Args:**
 - <u>period (str | None):</u> The time period for which portfolio performance metrics should be calculated.
 It can be one of the following: 'yearly', 'quarterly', 'monthly', 'weekly', or 'daily'.
 If None, the default period is 'quarterly' (if the 'quarterly' attribute is set to True),
 otherwise, it defaults to 'yearly'.
 - <u>exclude_sold_positions (bool):</u> A flag indicating whether to exclude sold positions.
 - <u>rounding (int | None):</u> The number of decimal places to round the output to.
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
## get_transactions_overview
Calculate and collect transaction overview ratios based on the provided data.
 This method calculates various transaction overview ratios, such as returns, costs, and profit & loss (PnL), based on the transaction dataset. The calculated ratios are added as new columns to the portfolio dataset. It also provides the option to use different methods for calculating PnL (FIFO, LIFO, or AVERAGE). The method ensures that necessary historical and benchmark data is available before performing calculations.

**Args:**
 - <u>rounding (int | None):</u> The number of decimal places to round the output to.
 If None, it defaults to the rounding specified in the configuration.
 - <u>exclude_sold_positions (bool):</u> A flag indicating whether to exclude sold positions
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
 - If no rounding is provided, the rounding precision specified in the configuration is used.
## get_transactions_performance
Calculate transaction performance metrics for a specified period.
 This method calculates various transaction performance metrics, such as returns, costs, and benchmarks, for the specified period. The calculation is based on historical price data for the corresponding period, including both the portfolio and benchmark datasets. It provides an overview of how the portfolio's transactions have performed in comparison to the benchmark over the given period.

**Args:**
 - <u>period (str | None):</u> The time period for which transaction performance metrics
 should be calculated. This can be one of the following: 'yearly', 'quarterly',
 'monthly', 'weekly', or 'daily'. If None, the default is 'quarterly' if
 the 'quarterly' attribute is set to True, otherwise 'yearly'.
 - <u>exclude_sold_positions (bool):</u> A flag indicating whether to exclude sold positions
 - <u>rounding (int | None):</u> The number of decimal places to round the output to.
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
 - The method uses historical price data from the specified period and benchmarks
 to calculate the metrics.
 - If no rounding is specified, the rounding precision from the configuration is used.
