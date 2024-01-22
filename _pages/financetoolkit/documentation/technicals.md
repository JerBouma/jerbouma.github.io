---
title: Technicals
excerpt: The Technicals Module contains 30+ Technical Indicators that can be used to analyse companies. These ratios are divided into 4 categories which are breadth, momentum, overlap and volatility. Each indicator is calculated using the data from the Toolkit module.
description: The Technicals Module contains 30+ Technical Indicators that can be used to analyse companies. These ratios are divided into 4 categories which are breadth, momentum, overlap and volatility. Each indicator is calculated using the data from the Toolkit module.
author_profile: false
permalink: /projects/financetoolkit/docs/technicals
classes: wide-sidebar
layout: single
redirect_from:
    - /technicals
sidebar:
    nav: "financetoolkit-docs-technicals"
---

The Technicals Module contains 30+ Technical Indicators that can be used to analyse companies. These ratios are divided into 4 categories which are breadth, momentum, overlap and volatility. Each indicator is calculated using the data from the Toolkit module.

To install the FinanceToolkit it simply requires the following:

{% include code_header.html %}
{% highlight bash %}
pip install financetoolkit -U
{% endhighlight %}

If you are looking for documentation regarding the toolkit, discovery, ratios, models, risk, performance and economics, please have a look below:

<div style="display: flex; justify-content: space-between;" class="show-on-desktop">
    <a href="/projects/financetoolkit/docs" class="btn btn--info" style="flex: 1;margin-right:5px">Toolkit</a>
    <a href="/projects/financetoolkit/docs/discovery" class="btn btn--info" style="flex: 1;margin-right:5px">Discovery</a>
    <a href="/projects/financetoolkit/docs/ratios" class="btn btn--info" style="flex: 1;margin-right:5px">Ratios</a>
    <a href="/projects/financetoolkit/docs/models" class="btn btn--info" style="flex: 1;margin-right:5px">Models</a>
    <a href="/projects/financetoolkit/docs/options" class="btn btn--info" style="flex: 1;margin-right:5px">Options</a>
    <a href="/projects/financetoolkit/docs/technicals" class="btn btn--warning" style="flex: 1;margin-right:5px">Technicals</a>
    <a href="/projects/financetoolkit/docs/risk" class="btn btn--info" style="flex: 1;margin-right:5px">Risk</a>
    <a href="/projects/financetoolkit/docs/performance" class="btn btn--info" style="flex: 1;margin-right:5px">Performance</a>
    <a href="/projects/financetoolkit/docs/economics" class="btn btn--info" style="flex: 1; ">Economics</a>
</div>

{% include algolia.html %}

## __init__
Initializes the Technicals Controller Class.

**Args:**
 - <u>tickers (str | list[str]):</u> The tickers to use for the calculation.
 - <u>intraday_historical (pd.DataFrame, optional):</u> The intraday historical data to use for the calculation.
 Defaults to pd.DataFrame().
 - <u>daily_historical (pd.DataFrame, optional):</u> The daily historical data to use for the calculation.
 Defaults to pd.DataFrame().
 - <u>weekly_historical (pd.DataFrame, optional):</u> The weekly historical data to use for the calculation.
 Defaults to pd.DataFrame().
 - <u>monthly_historical (pd.DataFrame, optional):</u> The monthly historical data to use for the calculation.
 Defaults to pd.DataFrame().
 - <u>quarterly_historical (pd.DataFrame, optional):</u> The quarterly historical data to use for the calculation.
 Defaults to pd.DataFrame().
 - <u>yearly_historical (pd.DataFrame, optional):</u> The yearly historical data to use for the calculation.
 Defaults to pd.DataFrame().
 - <u>rounding (int | None, optional):</u> The number of decimals to round the results to.
 Defaults to 4.
 - <u>start_date (str | None, optional):</u> The start date to use for the calculation.
 Defaults to None.
 - <u>end_date (str | None, optional):</u> The end date to use for the calculation.
 Defaults to None.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

average_directional_index = toolkit.technicals.get_average_directional_index()
{% endhighlight %}


Which returns:

| Date | AAPL | MSFT |
 |:-----------|--------:|--------:|
 | 2023-08-21 | 62.8842 | 36.7468 |
 | 2023-08-22 | 65.7063 | 36.5525 |
 | 2023-08-23 | 67.3596 | 35.5149 |
 | 2023-08-24 | 66.4527 | 35.4399 |
 | 2023-08-25 | 63.4837 | 32.3323 |

## collect_all_indicators
Calculates all Technical Indicators based on the data provided.

**Args:**
 - <u>period (str, optional):</u> The period to use for the calculation. Defaults to "daily".
 - <u>window (int, optional):</u> The number of days to use for the calculation. Defaults to 14.
 - <u>close_column (str, optional):</u> The column to use for the calculation. Defaults to "Adj Close".
 - <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
 - <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.

 **Returns:**
 pd.Series or pd.DataFrame: Technical indicators calculated based on the specified parameters.

 **Notes:**
 - The method calculates various types of technical indicators for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the indicator values
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.collect_all_indicators()
{% endhighlight %}

## collect_breadth_indicators
Calculates and collects various breadth indicators based on the provided data.

**Args:**
 - <u>period (str, optional):</u> The time period to consider for historical data.
 Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
 - <u>close_column (str, optional):</u> The name of the column containing the close prices.
 Defaults to "Adj Close".
 - <u>rounding (int | None, optional):</u> The number of decimals to round the results to.
 Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
 Defaults to False.
 - <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation.
 Defaults to 1.

 **Returns:**
 pd.Series or pd.DataFrame: Breadth indicators calculated based on the specified parameters.

 **Notes:**
 - The method calculates various breadth indicators for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the indicator values
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.collect_breadth_indicators()
{% endhighlight %}

## get_mcclellan_oscillator
Calculate the McClellan Oscillator for a given price series.

The McClellan Oscillator is a breadth indicator that measures the difference between the exponential moving average of advancing stocks and the exponential moving average of declining stocks.

The formula is a follows:


- McClellan Oscillator = EMA(Advancers) - EMA(Decliners)

**Args:**
 - <u>period (str, optional):</u> The time period to consider for historical data.
 Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
 - <u>close_column (str, optional):</u> The name of the column containing the close prices.
 Defaults to "Adj Close".
 - <u>short_ema_window (int, optional):</u> The window size for the short-term EMA.
 Defaults to 19.
 - <u>long_ema_window (int, optional):</u> The window size for the long-term EMA.
 Defaults to 39.
 - <u>rounding (int | None, optional):</u> The number of decimals to round the results to.
 Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
 Defaults to False.
 - <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation.
 Defaults to 1.

 **Returns:**
 pd.Series or pd.DataFrame: McClellan Oscillator values.

 **Notes:**
 - The method retrieves historical data based on the specified `period` and calculates
 the McClellan Oscillator for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the indicator values
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_mcclellan_oscillator()
{% endhighlight %}

## get_advancers_decliners
Calculate the Advancers/Decliners ratio for a given price series.

The Advancers/Decliners ratio is a breadth indicator that measures the number of advancing stocks (stocks with positive price changes) versus the number of declining stocks (stocks with negative price changes).

The formula is a follows:


- Advancers/Decliners = Advancers / Decliners

**Args:**
 - <u>period (str, optional):</u> The time period to consider for historical data.
 Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
 - <u>close_column (str, optional):</u> The name of the column containing the close prices.
 Defaults to "Adj Close".
 - <u>rounding (int | None, optional):</u> The number of decimals to round the results to.
 Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
 Defaults to False.
 - <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation.
 Defaults to 1.

 **Returns:**
 pd.Series or pd.DataFrame: Advancers/Decliners ratio values.

 **Notes:**
 - The method retrieves historical data based on the specified `period` and calculates
 the Advancers/Decliners ratio for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the indicator values
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_advancers_decliners()
{% endhighlight %}

## get_on_balance_volume
Calculate the On
-Balance Volume (OBV) for a given price series.

The On
-Balance Volume (OBV) is a technical indicator that uses volume flow to predict changes in stock price. It accumulates the volume on up days and subtracts the volume on down days. The resulting OBV line provides insights into the buying and selling pressure behind price movements.

The formula is a follows:


- OBV = Previous OBV + Current Volume if Close > Previous Close

**Args:**
 - <u>period (str, optional):</u> The time period to consider for historical data.
 Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
 - <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
 Defaults to "Adj Close".
 - <u>rounding (int | None, optional):</u> The number of decimals to round the results to.
 Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the OBV.
 Defaults to False.
 - <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation.
 Defaults to 1.

 **Returns:**
 pd.Series or pd.DataFrame: On-Balance Volume values.

 **Notes:**
 - The method retrieves historical data based on the specified `period` and calculates On-Balance Volume
 for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the OBV using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_on_balance_volume()
{% endhighlight %}

## get_accumulation_distribution_line
Calculate the Accumulation/Distribution Line for a given price series.

The Accumulation/Distribution Line is a technical indicator that evaluates the flow of money into or out of an asset. It takes into account both price and volume information to identify whether an asset is being accumulated (bought) or distributed (sold) by investors.

The formula is a follows:


- ADL = Previous ADL + Current ADL

**Args:**
 - <u>period (str, optional):</u> The time period to consider for historical data.
 Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
 - <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
 Defaults to "Adj Close".
 - <u>rounding (int | None, optional):</u> The number of decimals to round the results to.
 Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the Accumulation/Distribution Line.
 Defaults to False.
 - <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation.
 Defaults to 1.

 **Returns:**
 pd.Series or pd.DataFrame: Accumulation/Distribution Line values.

 **Notes:**
 - The method retrieves historical data based on the specified `period` and calculates the
 Accumulation/Distribution Line for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the Accumulation/Distribution Line
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_accumulation_distribution_line()
{% endhighlight %}

## get_chaikin_oscillator
Calculate the Chaikin Oscillator for a given price series.

The Chaikin Oscillator is a momentum
-based indicator that combines price and volume to help identify potential trends and reversals in the market. It is calculated as the difference between the 3
-day and 10
-day Accumulation/Distribution Line.

The formula is a follows:


- Chaikin Oscillator = EMA(short
-window ADL) - EMA(long
-window ADL)

**Args:**
 - <u>period (str, optional):</u> The time period to consider for historical data.
 Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
 - <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
 Defaults to "Adj Close".
 - <u>short_window (int, optional):</u> Number of periods for the short-term moving average.
 Defaults to 3.
 - <u>long_window (int, optional):</u> Number of periods for the long-term moving average.
 Defaults to 10.
 - <u>rounding (int | None, optional):</u> The number of decimals to round the results to.
 Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the Chaikin Oscillator.
 Defaults to False.
 - <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation.
 Defaults to 1.

 **Returns:**
 pd.Series or pd.DataFrame: Chaikin Oscillator values.

 **Notes:**
 - The method retrieves historical data based on the specified `period` and calculates the
 Chaikin Oscillator for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the Chaikin Oscillator
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_chaikin_oscillator()
{% endhighlight %}

## collect_momentum_indicators
Calculates and collects various momentum indicators based on the provided data.

**Args:**
 - <u>period (str, optional):</u> The time period to consider for historical data.
 Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
 - <u>window (int, optional):</u> The window size for calculating indicators.
 Defaults to 14.
 - <u>close_column (str, optional):</u> The name of the column containing the close prices.
 Defaults to "Adj Close".
 - <u>rounding (int | None, optional):</u> The number of decimals to round the results to.
 Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
 Defaults to False.
 - <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation.
 Defaults to 1.

 **Returns:**
 pd.Series or pd.DataFrame: Momentum indicators calculated based on the specified parameters.

 **Notes:**
 - The method calculates various momentum indicators for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the indicator values
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.collect_momentum_indicators()
{% endhighlight %}

## get_money_flow_index
Calculate the Money Flow Index (MFI) for a given price series.

The Money Flow Index is a momentum indicator that measures the strength and direction of money flowing in and out of a security by considering both price and volume.

The formula is a follows:


- MFI = 100 
- (100 / (1 + (positive_money_flow / negative_money_flow)))

**Args:**
 - <u>period (str, optional):</u> The time period to consider for historical data.
 Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
 - <u>close_column (str, optional):</u> The name of the column containing the close prices.
 Defaults to "Adj Close".
 - <u>window (int, optional):</u> The number of periods for calculating the MFI.
 Defaults to 14.
 - <u>rounding (int | None, optional):</u> The number of decimals to round the results to.
 Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
 Defaults to False.
 - <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation.
 Defaults to 1.

 **Returns:**
 pd.Series or pd.DataFrame: Money Flow Index (MFI) values.

 **Notes:**
 - The method retrieves historical data based on the specified `period` and calculates
 the MFI values for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the indicator values
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_money_flow_index()
{% endhighlight %}

## get_williams_percent_r
Calculate the Williams Percent R (Williams %R) for a given price series.

The Williams %R is a momentum indicator that measures the level of the close price relative to the high
-low range over a certain number of periods.

The formula is a follows:


- Williams %R = (Highest High - Close) / (Highest High - Lowest Low) * -100

**Args:**
 - <u>period (str, optional):</u> The time period to consider for historical data.
 Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
 - <u>close_column (str, optional):</u> The name of the column containing the close prices.
 Defaults to "Adj Close".
 - <u>window (int, optional):</u> The number of periods for calculating the Williams %R.
 Defaults to 14.
 - <u>rounding (int | None, optional):</u> The number of decimals to round the results to.
 Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
 Defaults to False.
 - <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation.
 Defaults to 1.

 **Returns:**
 pd.Series or pd.DataFrame: Williams %R values.

 **Notes:**
 - The method retrieves historical data based on the specified `period` and calculates
 the Williams %R values for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the indicator values
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_williams_percent_r()
{% endhighlight %}

## get_aroon_indicator
Calculate the Aroon Indicator for a given price series.

The Aroon Indicator is an oscillator that measures the strength of a trend and the likelihood of its continuation or reversal.

The formula is a follows:


- Aroon Up = ((Number of periods) - (Number of periods since highest high)) / (Number of periods) * 100

**Args:**
 - <u>period (str, optional):</u> The time period to consider for historical data.
 Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
 - <u>window (int, optional):</u> The number of periods for calculating the Aroon Indicator.
 Defaults to 14.
 - <u>rounding (int | None, optional):</u> The number of decimals to round the results to.
 Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
 Defaults to False.
 - <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation.
 Defaults to 1.

 **Returns:**
 Tuple[pd.Series, pd.Series] or Tuple[pd.DataFrame, pd.DataFrame]:
 Aroon Indicator values for the upward and downward trends.

 **Notes:**
 - The method retrieves historical data based on the specified `period` and calculates
 the Aroon Indicator values for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the indicator values
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_aroon_indicator()
{% endhighlight %}

## get_commodity_channel_index
Calculate the Commodity Channel Index (CCI) for a given price series.

The Commodity Channel Index is an oscillator that measures the current price level relative to an average price level over a specified period.

The formula is a follows:


- CCI = (Typical Price - SMA(Typical Price)) / (constant * Mean Deviation)

**Args:**
 - <u>period (str, optional):</u> The time period to consider for historical data.
 Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
 - <u>close_column (str, optional):</u> The column in the historical data that represents
 the closing prices. Defaults to "Adj Close".
 - <u>window (int, optional):</u> The number of periods for calculating the CCI.
 Defaults to 14.
 - <u>constant (float, optional):</u> Constant multiplier used in the CCI calculation.
 Defaults to 0.015.
 - <u>rounding (int | None, optional):</u> The number of decimals to round the results to.
 Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
 Defaults to False.
 - <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation.
 Defaults to 1.

 **Returns:**
 pd.Series or pd.DataFrame: Commodity Channel Index (CCI) values.

 **Notes:**
 - The method retrieves historical data based on the specified `period` and calculates
 the CCI values for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the indicator values
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_commodity_channel_index()
{% endhighlight %}

## get_relative_vigor_index
Calculate the Relative Vigor Index (RVI) for a given price series.

The Relative Vigor Index is an oscillator that measures the conviction of a current price trend using the relationship between closing and opening prices.

The formula is a follows:


- RVI = SMA(Upward Change) / (SMA(Upward Change) + SMA(Downward Change))

**Args:**
 - <u>period (str, optional):</u> The time period to consider for historical data.
 Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
 - <u>close_column (str, optional):</u> The column in the historical data that represents
 the closing prices. Defaults to "Adj Close".
 - <u>window (int, optional):</u> The number of periods for calculating the RVI.
 Defaults to 14.
 - <u>rounding (int | None, optional):</u> The number of decimals to round the results to.
 Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
 Defaults to False.
 - <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation.
 Defaults to 1.

 **Returns:**
 pd.Series or pd.DataFrame: Relative Vigor Index (RVI) values.

 **Notes:**
 - The method retrieves historical data based on the specified `period` and calculates
 the RVI values for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the indicator values
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_relative_vigor_index()
{% endhighlight %}

## get_force_index
Calculate the Force Index for a given price series.

The Force Index is an indicator that measures the strength behind price movements.

The formula is a follows:


- Force Index = SMA(Periods) * (Close - Close(1))

**Args:**
 - <u>period (str, optional):</u> The time period to consider for historical data.
 Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
 - <u>close_column (str, optional):</u> The column in the historical data that represents
 the closing prices. Defaults to "Adj Close".
 - <u>window (int, optional):</u> The number of periods for calculating the Force Index.
 Defaults to 14.
 - <u>rounding (int | None, optional):</u> The number of decimals to round the results to.
 Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
 Defaults to False.
 - <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation.
 Defaults to 1.

 **Returns:**
 pd.Series or pd.DataFrame: Force Index values.

 **Notes:**
 - The method retrieves historical data based on the specified `period` and calculates
 the Force Index values for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the indicator values
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_force_index()
{% endhighlight %}

## get_ultimate_oscillator
Calculate the Ultimate Oscillator for a given price series.

The Ultimate Oscillator is a momentum oscillator that combines short
-term, mid
-term, and long
-term price momentum into a single value.

The formula is a follows:


- Ultimate Oscillator = 100 * ((4 * SMA(Periods)) / (SMA(Periods) + SMA(Periods) + SMA(Periods)))

**Args:**
 - <u>period (str, optional):</u> The time period to consider for historical data.
 Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
 - <u>close_column (str, optional):</u> The column in the historical data that represents
 the closing prices. Defaults to "Adj Close".
 - <u>window_1 (int, optional):</u> The number of periods for the first short-term window.
 Defaults to 7.
 - <u>window_2 (int, optional):</u> The number of periods for the second mid-term window.
 Defaults to 14.
 - <u>window_3 (int, optional):</u> The number of periods for the third long-term window.
 Defaults to 28.
 - <u>rounding (int | None, optional):</u> The number of decimals to round the results to.
 Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
 Defaults to False.
 - <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation.
 Defaults to 1.

 **Returns:**
 pd.Series or pd.DataFrame: Ultimate Oscillator values.

 **Notes:**
 - The method retrieves historical data based on the specified `period` and calculates
 the Ultimate Oscillator values for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the indicator values
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_ultimate_oscillator()
{% endhighlight %}

## get_percentage_price_oscillator
Calculate the Percentage Price Oscillator (PPO) for a given price series.

The Percentage Price Oscillator (PPO) is a momentum oscillator that measures the difference between two moving averages as a percentage of the longer moving average.

The formula is a follows:


- PPO = ((Long
-term EMA - Short
-term EMA) / Short-term EMA) * 100

**Args:**
 - <u>period (str, optional):</u> The time period to consider for historical data.
 Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
 - <u>close_column (str, optional):</u> The column in the historical data that represents
 the closing prices. Defaults to "Adj Close".
 - <u>short_window (int, optional):</u> The number of periods for the short-term moving average.
 Defaults to 7.
 - <u>long_window (int, optional):</u> The number of periods for the long-term moving average.
 Defaults to 28.
 - <u>rounding (int | None, optional):</u> The number of decimals to round the results to.
 Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
 Defaults to False.
 - <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation.
 Defaults to 1.

 **Returns:**
 pd.Series or pd.DataFrame: Percentage Price Oscillator (PPO) values.

 **Notes:**
 - The method retrieves historical data based on the specified `period` and calculates
 the PPO values for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the indicator values
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_percentage_price_oscillator()
{% endhighlight %}

## get_detrended_price_oscillator
Calculate the Detrended Price Oscillator (DPO) for a given price series.

The Detrended Price Oscillator (DPO) is an indicator that helps identify short
-term cycles by removing longer
-term trends from prices.

The formula is a follows:


- DPO = Close 
- SMA(Close, (Number of Periods / 2) + 1)

**Args:**
 - <u>period (str, optional):</u> The time period to consider for historical data.
 Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
 - <u>close_column (str, optional):</u> The column in the historical data that represents
 the closing prices. Defaults to "Adj Close".
 - <u>window (int, optional):</u> The number of periods to consider for the DPO calculation.
 Defaults to 14.
 - <u>rounding (int | None, optional):</u> The number of decimals to round the results to.
 Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
 Defaults to False.
 - <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation.
 Defaults to 1.

 **Returns:**
 pd.Series or pd.DataFrame: Detrended Price Oscillator (DPO) values.

 **Notes:**
 - The method retrieves historical data based on the specified `period` and calculates
 the DPO values for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the indicator values
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_detrended_price_oscillator()
{% endhighlight %}

## get_average_directional_index
Calculate the Average Directional Index (ADX) for a given price series.

The Average Directional Index (ADX) is an indicator that measures the strength of a trend, whether it's an uptrend or a downtrend.

The formula is a follows:


- ADX = SMA(DMI) / (SMA(DMI) + SMA(DMI))

**Args:**
 - <u>period (str, optional):</u> The time period to consider for historical data.
 Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
 - <u>close_column (str, optional):</u> The column in the historical data that represents
 the closing prices. Defaults to "Adj Close".
 - <u>window (int, optional):</u> The number of periods to consider for the ADX calculation.
 Defaults to 14.
 - <u>rounding (int | None, optional):</u> The number of decimals to round the results to.
 Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
 Defaults to False.
 - <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation.
 Defaults to 1.

 **Returns:**
 pd.DataFrame or pd.Series: Average Directional Index (ADX) values.

 **Notes:**
 - The method retrieves historical data based on the specified `period` and calculates
 the ADX values for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the indicator values
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_average_directional_index()
{% endhighlight %}

## get_chande_momentum_oscillator
Calculate the Chande Momentum Oscillator (CMO) for a given price series.

The Chande Momentum Oscillator is an indicator that measures the momentum of a price series and identifies overbought and oversold conditions.

The formula is a follows:


- CMO = ((Sum of Upward Change) - (Sum of Downward Change)) / ((Sum of Upward Change) + (Sum of Downward Change))

**Args:**
 - <u>period (str, optional):</u> The time period to consider for historical data.
 Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
 - <u>close_column (str, optional):</u> The column in the historical data that represents
 the closing prices. Defaults to "Adj Close".
 - <u>window (int, optional):</u> The number of periods to consider for the CMO calculation.
 Defaults to 14.
 - <u>rounding (int | None, optional):</u> The number of decimals to round the results to.
 Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
 Defaults to False.
 - <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation.
 Defaults to 1.

 **Returns:**
 pd.Series or pd.DataFrame: Chande Momentum Oscillator values.

 **Notes:**
 - The method retrieves historical data based on the specified `period` and calculates
 the Chande Momentum Oscillator values for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the indicator values
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_chande_momentum_oscillator()
{% endhighlight %}

## get_ichimoku_cloud
Calculate the Ichimoku Cloud indicator for a given price series.

The Ichimoku Cloud, also known as the Ichimoku Kinko Hyo, is a versatile indicator that defines support and resistance, identifies trend direction, gauges momentum, and provides trading signals.

The formula is a follows:


- Conversion Line = (Highest High + Lowest Low) / 2

**Args:**
 - <u>period (str, optional):</u> The time period to consider for historical data.
 Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
 - <u>conversion_window (int, optional):</u> The number of periods to consider for the
 Conversion Line (Tenkan-sen) calculation. Defaults to 9.
 - <u>base_window (int, optional):</u> The number of periods to consider for the Base Line
 (Kijun-sen) calculation. Defaults to 20.
 - <u>lead_span_b_window (int, optional):</u> The number of periods to shift forward for the
 Lead Span B calculation. Defaults to 40.
 - <u>rounding (int | None, optional):</u> The number of decimals to round the results to.
 Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
 Defaults to False.
 - <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation.
 Defaults to 1.

 **Returns:**
 Tuple[pd.Series, pd.Series, pd.Series, pd.Series] or
 Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
 Conversion Line, Base Line, Lead Span A, and Lead Span B values.

 **Notes:**
 - The method retrieves historical data based on the specified `period` and calculates
 the Ichimoku Cloud values for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the indicator values
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_ichimoku_cloud()
{% endhighlight %}

## get_stochastic_oscillator
Calculate the Stochastic Oscillator indicator for a given price series.

The Stochastic Oscillator is a momentum indicator that shows the location of the close relative to the high
-low range over a set number of periods. It consists of the %K line (fast) and the %D line (slow).

The formula is a follows:


- %K = 100 * ((Close - Lowest Low) / (Highest High - Lowest Low)) 
- %D = SMA(%K)

**Args:**
 - <u>period (str, optional):</u> The time period to consider for historical data.
 Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
 - <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
 Defaults to "Adj Close".
 - <u>window (int, optional):</u> The number of periods to consider for the %K line calculation.
 Defaults to 14.
 - <u>smooth_widow (int, optional):</u> The number of periods to consider for the %D line
 (slow stochastic) calculation. Defaults to 3.
 - <u>rounding (int | None, optional):</u> The number of decimals to round the results to.
 Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the %K and %D values.
 Defaults to False.
 - <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation.
 Defaults to 1.

 **Returns:**
 Tuple[pd.Series, pd.Series] or Tuple[pd.DataFrame, pd.DataFrame]:
 %K line and %D line values.

 **Notes:**
 - The method retrieves historical data based on the specified `period` and calculates
 the Stochastic Oscillator values for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the %K and %D values
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_stochastic_oscillator()
{% endhighlight %}

## get_moving_average_convergence_divergence
Calculate the Moving Average Convergence Divergence (MACD) indicator for a given price series.

The Moving Average Convergence Divergence (MACD) is a trend
-following momentum indicator that shows the relationship between two moving averages of a security's price. It consists of the MACD line, signal line, and MACD histogram.

The formula is a follows:


- MACD Line = Short
-term EMA - Long
-term EMA 
- Signal Line = SMA(MACD Line)

**Args:**
 - <u>period (str, optional):</u> The time period to consider for historical data.
 Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
 - <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
 Defaults to "Adj Close".
 - <u>short_window (int, optional):</u> The number of periods for the shorter moving average.
 Defaults to 12.
 - <u>long_window (int, optional):</u> The number of periods for the longer moving average.
 Defaults to 26.
 - <u>signal_window (int, optional):</u> The number of periods for the signal line.
 Defaults to 9.
 - <u>rounding (int | None, optional):</u> The number of decimals to round the results to.
 Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the MACD and signal values.
 Defaults to False.
 - <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation.
 Defaults to 1.

 **Returns:**
 Tuple[pd.DataFrame, pd.DataFrame] or Tuple[pd.Series, pd.Series]:
 MACD line and signal line values.

 **Notes:**
 - The method retrieves historical data based on the specified `period` and calculates
 the MACD and signal line values for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the MACD and signal values
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_moving_average_convergence_divergence()
{% endhighlight %}

## get_relative_strength_index
Calculate the Relative Strength Index (RSI) indicator for a given price series.

The Relative Strength Index (RSI) is a momentum oscillator that measures the speed and change of price movements. It ranges from 0 to 100 and is used to identify overbought or oversold conditions in an asset's price.

The formula is a follows:


- RSI = 100 - (100 / (1 + RS))

**Args:**
 - <u>period (str, optional):</u> The time period to consider for historical data.
 Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
 - <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
 Defaults to "Adj Close".
 - <u>window (int, optional):</u> The number of periods for RSI calculation. Defaults to 14.
 - <u>rounding (int | None, optional):</u> The number of decimals to round the results to.
 Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the RSI.
 Defaults to False.
 - <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation.
 Defaults to 1.

 **Returns:**
 pd.DataFrame or pd.Series:
 Relative Strength Index (RSI) values.

 **Notes:**
 - The method retrieves historical data based on the specified `period` and calculates the
 RSI for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the RSI
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_relative_strength_index()
{% endhighlight %}

## get_balance_of_power
Calculate the Balance of Power (BOP) indicator for a given price series.

The Balance of Power (BOP) indicator measures the strength of buyers versus sellers in the market. It relates the price change to the change in the asset's trading range.

The formula is a follows:


- BOP = (Close - Open) / (High - Low)

**Args:**
 - <u>period (str, optional):</u> The time period to consider for historical data.
 Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
 - <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
 Defaults to "Adj Close".
 - <u>rounding (int | None, optional):</u> The number of decimals to round the results to.
 Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the BOP.
 Defaults to False.
 - <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation.
 Defaults to 1.

 **Returns:**
 pd.DataFrame or pd.Series:
 Balance of Power (BOP) values.

 **Notes:**
 - The method retrieves historical data based on the specified `period` and calculates the
 BOP for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the BOP
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_balance_of_power()
{% endhighlight %}

## collect_overlap_indicators
Calculates and collects various overlap
-based indicators based on the provided data.

**Args:**
 - <u>period (str, optional):</u> The time period to consider for historical data.
 Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
 - <u>window (int, optional):</u> The window size for calculating indicators.
 Defaults to 14.
 - <u>close_column (str, optional):</u> The name of the column containing the close prices.
 Defaults to "Adj Close".
 - <u>rounding (int | None, optional):</u> The number of decimals to round the results to.
 Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
 Defaults to False.
 - <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation.
 Defaults to 1.

 **Returns:**
 pd.Series or pd.DataFrame: Overlap-based indicators calculated based on the specified parameters.

 **Notes:**
 - The method calculates several overlap-based indicators for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the indicator values
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.collect_overlap_indicators()
{% endhighlight %}

## get_moving_average
Calculate the Moving Average (MA) for a given price series.

The Moving Average (MA) is a commonly used technical indicator that smooths out price data by calculating the average price over a specified number of periods.

The formula is a follows:


- MA = (Sum of Prices) / (Number of Prices)

**Args:**
 - <u>period (str, optional):</u> The time period to consider for historical data.
 Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
 - <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
 Defaults to "Adj Close".
 - <u>window (int, optional):</u> Number of periods to consider for the moving average.
 The number of periods (time intervals) over which to calculate the MA.
 - <u>rounding (int | None, optional):</u> The number of decimals to round the results to.
 Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the MA.
 Defaults to False.
 - <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation.
 Defaults to 1.

 **Returns:**
 pd.DataFrame or pd.Series:
 Moving Average (MA) values.

 **Notes:**
 - The method retrieves historical data based on the specified `period` and calculates the
 MA for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the MA
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_moving_average()
{% endhighlight %}

## get_exponential_moving_average
Calculate the Exponential Moving Average (EMA) for a given price series.

EMA is a technical indicator that gives more weight to recent price data, providing a smoothed moving average that reacts faster to price changes.

The formula is a follows:


- EMA = (Close - Previous EMA) * (2 / (1 + Window)) + Previous EMA

**Args:**
 - <u>period (str, optional):</u> The time period to consider for historical data.
 Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
 - <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
 Defaults to "Adj Close".
 - <u>window (int, optional):</u> Number of periods for EMA calculation.
 The number of periods (time intervals) over which to calculate the EMA.
 - <u>rounding (int | None, optional):</u> The number of decimals to round the results to.
 Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the EMA.
 Defaults to False.
 - <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation.
 Defaults to 1.

 **Returns:**
 pd.DataFrame or pd.Series:
 Exponential Moving Average (EMA) values.

 **Notes:**
 - The method retrieves historical data based on the specified `period` and calculates the
 EMA for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the EMA
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_exponential_moving_average()
{% endhighlight %}

## get_double_exponential_moving_average
Calculate the Double Exponential Moving Average (DEMA) for a given price series.

DEMA is a technical indicator that attempts to reduce the lag from traditional moving averages by using a combination of two exponential moving averages.

The formula is a follows:


- EMA = (Close - Previous EMA) * (2 / (1 + Window)) + Previous EMA

**Args:**
 - <u>period (str, optional):</u> The time period to consider for historical data.
 Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
 - <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
 Defaults to "Adj Close".
 - <u>window (int, optional):</u> Number of periods for moving average calculation.
 The number of periods (time intervals) over which to calculate the moving average.
 - <u>rounding (int | None, optional):</u> The number of decimals to round the results to.
 Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the DEMA.
 Defaults to False.
 - <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation.
 Defaults to 1.

 **Returns:**
 pd.DataFrame or pd.Series:
 Double Exponential Moving Average (DEMA) values.

 **Notes:**
 - The method retrieves historical data based on the specified `period` and calculates the
 DEMA for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the DEMA
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_double_exponential_moving_average()
{% endhighlight %}

## get_trix
Calculate the Trix (Triple Exponential Moving Average) for a given price series.

Trix is a momentum oscillator that calculates the percentage rate of change of a triple exponentially smoothed moving average. It helps identify overbought and oversold conditions in a market.

The formula is a follows:


- EMA1 = EMA(Close, Window) 
- EMA2 = EMA(EMA1, Window) 
- EMA3 = EMA(EMA2, Window) 
- TRIX = 100 * ((EMA3 - EMA3[-1]) / EMA3[-1])

**Args:**
 - <u>period (str, optional):</u> The time period to consider for historical data.
 Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
 - <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
 Defaults to "Adj Close".
 - <u>window (int, optional):</u> Number of periods for moving average calculation.
 The number of periods (time intervals) over which to calculate the moving average.
 - <u>rounding (int | None, optional):</u> The number of decimals to round the results to.
 Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the Trix.
 Defaults to False.
 - <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation.
 Defaults to 1.

 **Returns:**
 pd.DataFrame or pd.Series:
 Trix values.

 **Notes:**
 - The method retrieves historical data based on the specified `period` and calculates the
 Trix for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the Trix
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_trix()
{% endhighlight %}

## get_bollinger_bands
Calculate the Bollinger Bands for a given price series.

Bollinger Bands are a volatility indicator that consists of three lines: an upper band, a middle band (simple moving average), and a lower band. The upper and lower bands are calculated as the moving average plus and minus a specified number of standard deviations, respectively.

The formula is a follows:


- Middle Band = SMA(Close, Window) 
- Upper Band = Middle Band + (Num Std Dev * Std Dev) 
- Lower Band = Middle Band - (Num Std Dev * Std Dev)

**Args:**
 - <u>period (str, optional):</u> The time period to consider for historical data.
 Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
 - <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
 Defaults to "Adj Close".
 - <u>window (int, optional):</u> Number of periods for moving average calculation.
 The number of periods (time intervals) over which to calculate the moving average.
 - <u>num_std_dev (int, optional):</u> Number of standard deviations for the bands.
 Defaults to 2.
 - <u>rounding (int | None, optional):</u> The number of decimals to round the results to.
 Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the bands.
 Defaults to False.
 - <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation.
 Defaults to 1.

 **Returns:**
 Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame] or Tuple[pd.Series, pd.Series, pd.Series]:
 Bollinger Bands (upper, middle, lower).

 **Notes:**
 - The method retrieves historical data based on the specified `period` and calculates the
 Bollinger Bands for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the Bollinger Bands
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_bollinger_bands()
{% endhighlight %}

## get_triangular_moving_average
Calculate the Triangular Moving Average (TMA) for a given price series.

The Triangular Moving Average (TMA) is a smoothed version of the Simple Moving Average (SMA) that uses multiple SMAs to reduce noise and provide a smoother trendline.

The formula is a follows:


- TMA = SMA(SMA(Close, Window), Window)

**Args:**
 - <u>period (str, optional):</u> The time period to consider for historical data.
 Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
 - <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
 Defaults to "Adj Close".
 - <u>window (int, optional):</u> Number of periods for TMA calculation.
 The number of periods (time intervals) over which to calculate the TMA.
 - <u>rounding (int | None, optional):</u> The number of decimals to round the results to.
 Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the TMA.
 Defaults to False.
 - <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation.
 Defaults to 1.

 **Returns:**
 pd.Series or pd.DataFrame: Triangular Moving Average values.

 **Notes:**
 - The method retrieves historical data based on the specified `period` and calculates the
 Triangular Moving Average for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the Triangular Moving Average
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_triangular_moving_average()
{% endhighlight %}

## collect_volatility_indicators
Calculates and collects various volatility indicators based on the provided data.

**Args:**
 - <u>period (str, optional):</u> The time period to consider for historical data.
 Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
 - <u>window (int, optional):</u> The window size for calculating indicators.
 Defaults to 14.
 - <u>close_column (str, optional):</u> The name of the column containing the close prices.
 Defaults to "Adj Close".
 - <u>rounding (int | None, optional):</u> The number of decimals to round the results to.
 Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
 Defaults to False.
 - <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation.
 Defaults to 1.

 **Returns:**
 pd.Series or pd.DataFrame: Volatility indicators calculated based on the specified parameters.

 **Notes:**
 - The method calculates several volatility-based indicators for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the indicator values
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.collect_volatility_indicators()
{% endhighlight %}

## get_true_range
Calculate the True Range (TR) for a given price series.

The True Range (TR) is a measure of market volatility that considers the differences between the high and low prices and the previous closing price. It provides insights into the price movement of an asset.

The formula is a follows:


- TR = max(high - low, abs(high - previous_close), abs(low - previous_close))

**Args:**
 - <u>period (str, optional):</u> The time period to consider for historical data.
 Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
 - <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
 Defaults to "Adj Close".
 - <u>rounding (int | None, optional):</u> The number of decimals to round the results to.
 Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the True Range.
 Defaults to False.
 - <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation.
 Defaults to 1.

 **Returns:**
 pd.Series or pd.DataFrame: True Range values.

 **Notes:**
 - The method retrieves historical data based on the specified `period` and calculates the
 True Range for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the True Range
 using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_true_range()
{% endhighlight %}

## get_average_true_range
Calculate the Average True Range (ATR) of a given price series.

The Average True Range (ATR) is a technical indicator that measures the volatility of an asset's price movements over a specified number of periods. It provides insights into the potential price range of an asset, which can help traders and investors make more informed decisions.

The formula is a follows:


- TR = max(high - low, abs(high - previous_close), abs(low - previous_close)) 
- ATR = EMA(TR, Window)

**Args:**
 - <u>period (str):</u> Period for which to calculate the ATR.
 - <u>window (int):</u> Number of periods for ATR calculation.
 The number of periods (time intervals) over which to calculate the Average True Range.
 - <u>rounding (int | None):</u> Number of decimal places to round the resulting ATR values to.
 If None, no rounding is performed.
 - <u>growth (bool):</u> Flag indicating whether to return the ATR growth rate.
 If True, the ATR growth rate is calculated.
 - <u>lag (int | list[int]):</u> Number of periods to lag the ATR values by.
 If an integer is provided, all ATR values are lagged by the same number of periods.
 If a list of integers is provided, each ATR value is lagged by the corresponding number of periods.

 **Returns:**
 pd.Series: ATR values or ATR growth rate (if growth is True).
 A pandas Series containing the calculated Average True Range values or growth rate for each period.

 Formula:
 The Average True Range (ATR) is calculated using the following steps:
 1. Calculate the True Range (TR) for each period:
 - True Range (TR) = max(high - low, abs(high - previous_close), abs(low - previous_close))
 2. Calculate the Average True Range (ATR) over the specified window:
 - ATR = EMA(TR, window), where EMA is the Exponential Moving Average.

 **Notes:**
 - ATR values are typically used to assess the volatility and potential price movement of an asset.
 - A higher ATR value indicates higher volatility, while a lower ATR value suggests lower volatility.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_average_true_range()
{% endhighlight %}

## get_keltner_channels
Calculate the Keltner Channels for a given price series.

The Keltner Channels consist of three lines: 
- Upper Channel Line = Exponential Moving Average (EMA) of High Prices + ATR * ATR Multiplier 
- Middle Channel Line = Exponential Moving Average (EMA) of Closing Prices 
- Lower Channel Line = Exponential Moving Average (EMA) of Low Prices 
- ATR * ATR Multiplier

The formula is a follows:


- EMA = (Close - Previous EMA) * (2 / (1 + Window)) + Previous EMA 
- ATR = EMA(TR, ATR Window) 
- Upper Channel Line = EMA(High, Window) + ATR * ATR Multiplier 
- Middle Channel Line = EMA(Close, Window) 
- Lower Channel Line = EMA(Low, Window) - ATR * ATR Multiplier

**Args:**
 - <u>period (str, optional):</u> The time period to consider for historical data.
 Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
 - <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
 Defaults to "Adj Close".
 - <u>window (int, optional):</u> Number of periods for the moving average.
 Defaults to 14.
 - <u>atr_window (int, optional):</u> Number of periods for ATR calculation.
 Defaults to 14.
 - <u>atr_multiplier (int, optional):</u> Multiplier for ATR to determine channel width.
 Defaults to 2.
 - <u>rounding (int | None, optional):</u> The number of decimals to round the results to.
 Defaults to 4.
 - <u>growth (bool, optional):</u> Whether to calculate the growth of the channels.
 Defaults to False.
 - <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation.
 Defaults to 1.

 **Returns:**
 pd.DataFrame or Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]: Keltner Channels (upper, middle, lower).

 **Notes:**
 - The method retrieves historical data based on the specified `period` and calculates Keltner Channels
 for each asset in the Toolkit instance.
 - If `growth` is set to True, the method calculates the growth of the channels using the specified `lag`.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_keltner_channels()
{% endhighlight %}

