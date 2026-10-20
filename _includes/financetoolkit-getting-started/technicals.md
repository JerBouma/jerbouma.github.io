## Getting Started

The Technicals module calculates technical indicators from the historical prices and volumes the Toolkit collects. It covers four groups: breadth indicators (such as On-Balance Volume and the TRIN), momentum indicators (such as the RSI, the MACD and the Average Directional Index), overlap indicators (moving averages, Bollinger Bands, VWAP and pivot points) and volatility indicators (such as the Average True Range and the volatility cone). Every indicator is calculated for each ticker and for the benchmark, so you can compare a stock's signal with that of the market on the same day.

This section uses Microsoft, ASML, Micron and Amazon over 2023, with the S&P 500 as the benchmark.

### Loading the Data

The Technicals module is part of the `Toolkit` class and works on daily data by default. A start and end date fix the period, which keeps the results the same each time you run them.

To load the data for the four companies over 2023:

```python
import pandas as pd

from financetoolkit import Toolkit

companies = Toolkit(
    ["MSFT", "ASML", "MU", "AMZN"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2023-01-01",
    end_date="2024-01-01",
)
```

### All Indicators at Once

Each group has its own `collect_` function (`collect_breadth_indicators`, `collect_momentum_indicators`, `collect_overlap_indicators` and `collect_volatility_indicators`), and `collect_all_indicators` returns all of them in one DataFrame with a column per indicator and ticker. To calculate every indicator for every ticker:

```python
indicators = companies.technicals.collect_all_indicators()
```

Which gives about 70 indicators for each day. A selection of them on the last trading day of 2023:

| Indicator | Microsoft | ASML | Micron | Amazon | S&P 500 |
|:----------|----------:|-----:|-------:|-------:|--------:|
| Relative Strength Index | 57.95 | 67.20 | 65.66 | 59.01 | 70.56 |
| MACD Line | 2.63 | 23.03 | 3.05 | 2.78 | 7.45 |
| MACD Signal Line | 3.12 | 23.19 | 2.59 | 2.92 | 7.48 |
| Average Directional Index | 24.78 | 39.43 | 38.71 | 20.74 | 47.77 |
| Stochastic %K | 29.90 | 59.54 | 70.37 | 69.22 | 4.31 |
| Williams %R | -70.10 | -40.46 | -29.63 | -30.78 | -95.69 |
| Average True Range | 10.30 | 23.13 | 2.31 | 2.81 | 17.86 |
| Money Flow Index | 76.89 | 77.07 | 72.33 | 62.13 | 69.22 |

### Bollinger Bands

Every indicator also has its own function. Bollinger Bands place a band of two standard deviations around a moving average (14 days by default), so the bands widen when the price moves a lot and narrow when it is calm. A close above the upper band is often read as stretched, a squeeze of the bands as a sign that a larger move is coming.

To calculate the Bollinger Bands and select Microsoft:

```python
bollinger_bands = companies.technicals.get_bollinger_bands()

bollinger_bands.xs("MSFT", level=1, axis=1)
```

Which gives the bands for Microsoft, and in the second tab their width (the distance between the upper and the lower band as a share of the middle band):

{% include ft-chart.html id="technicals-bollinger" src="/assets/data/financetoolkit-guides/technicals.json" label="Bollinger Bands and band width for Microsoft over 2023" %}

Microsoft closed above its upper band on 20 days of 2023 and below the lower band on 4. The width separates the turbulent stretches from the calm ones: it peaked at 16.7% in March and fell to 2.5% in the last week of December, the tightest squeeze of the year.

### Changing the Parameters

Each indicator takes its own parameters, such as the window, and the general `growth` and `lag` parameters that the whole Toolkit supports. The Average Directional Index (ADX) measures the strength of a trend, whatever its direction: a reading above 25 is usually taken as a trending market, below 20 as a market without direction.

To calculate the ADX over 20 days instead of the default 14, and its growth over 1, 3, 5 and 10 days:

```python
companies.technicals.get_average_directional_index(window=20)

companies.technicals.get_average_directional_index(
    window=20, growth=True, lag=[1, 3, 5, 10]
)
```

Which gives, for Microsoft, the ADX with both thresholds, and in the second tab its growth over 1 and 10 days:

{% include ft-chart.html id="technicals-adx-growth" src="/assets/data/financetoolkit-guides/technicals.json" label="Microsoft's Average Directional Index over 20 days and its growth over 1 and 10 days" %}

Microsoft's ADX climbed above 25 in April and peaked at 41.9 in early June, a strong trend, then fell to 9.9 at the end of October, when the price moved sideways. The growth shows the turns sooner, and the longer the lag, the larger the swings: the 10-day change reached 110% in mid-November, as the year-end rally began. Over the last ten trading days of 2023 the ADX fell by about 11%, a trend that was losing strength into the end of the year.

### Relative Strength Index

The Relative Strength Index (RSI) compares the size of recent gains with recent losses on a scale of 0 to 100. Above 70 a stock is usually considered overbought, below 30 oversold.

To calculate the RSI for every ticker:

```python
rsi = companies.technicals.get_relative_strength_index()

(rsi > 70).sum(), (rsi < 30).sum()
```

Which gives the number of days each was overbought or oversold, and the RSI itself in a tab per company and the S&P 500:

{% include ft-chart.html id="technicals-rsi" src="/assets/data/financetoolkit-guides/technicals.json" label="Days overbought and oversold, and the Relative Strength Index of Microsoft, ASML, Micron, Amazon and the S&P 500 over 2023" %}

In the strong market of 2023, the S&P 500 closed above 70 on 41 days, against 13 to 23 days for each of the four companies. ASML spent the most time below 30, on 10 days, and the S&P 500 dipped below it on 2.

### Donchian Channels and the Hull Moving Average

Donchian Channels plot the highest high and the lowest low over a rolling window (20 days by default), with the middle line halfway between them. A close above the upper channel is a breakout to a new high for the window, which is the basis of many trend-following systems. The Hull Moving Average combines weighted moving averages of different lengths to follow the price closely with less lag than a simple moving average.

To calculate both:

```python
donchian_channels = companies.technicals.get_donchian_channels()

hull_moving_average = companies.technicals.get_hull_moving_average()
```

Which gives, for Microsoft with a tab per indicator:

{% include ft-chart.html id="technicals-donchian-hull" src="/assets/data/financetoolkit-guides/technicals.json" label="Donchian Channels and Hull Moving Average for Microsoft over 2023" %}

Microsoft closed at a new 20-day high, on or above the upper channel, on 34 days of 2023, and at a new low on only 4. The flat stretches of the upper channel mark the periods without a breakout, most of all from August to October.

### VWAP, Parabolic SAR and Pivot Points

The Volume Weighted Average Price (VWAP) is the average price weighted by the volume traded, a common benchmark for whether a trade was executed at a good price. The Parabolic SAR (Stop and Reverse) is a trailing level below the price in an uptrend and above it in a downtrend; when the price crosses it, the trend is considered to have reversed. Pivot Points derive support and resistance levels from the previous day's high, low and close.

To calculate all three:

```python
vwap = companies.technicals.get_volume_weighted_average_price()

parabolic_sar = companies.technicals.get_parabolic_sar()

pivot_points = companies.technicals.get_pivot_points()
```

Which gives, for Microsoft with a tab per indicator, the VWAP over the year and the Parabolic SAR and Pivot Points over the last three months (the Pivot Points tab shows the pivot with the first resistance and support levels; the function also returns the second and third):

{% include ft-chart.html id="technicals-overlap" src="/assets/data/financetoolkit-guides/technicals.json" label="VWAP, Parabolic SAR and Pivot Points for Microsoft over 2023" %}

Microsoft closed above its VWAP on 183 of the 237 days with a value, which fits a stock that rose by more than half over the year. The Parabolic SAR flipped 24 times in 2023, 5 of them in the fourth quarter; a jump of the dashed line from below the price to above it, as at the end of November, marks a reversal from an uptrend to a downtrend.

### Volatility Cone

The volatility cone shows the distribution of realized volatility (annualized) for several lookback windows, from 10 to 120 trading days: the minimum, maximum, median and percentiles of every rolling window in the period, next to the current value. It tells you whether volatility today is cheap or expensive compared to its own history, which is a starting point for judging whether options are priced high or low.

To calculate the volatility cone and select Microsoft:

```python
companies.technicals.get_volatility_cone().xs("MSFT", level=1, axis=1)
```

Which gives the cone, with dashed lines for the maximum, the minimum and the 25th and 75th percentiles, a solid line for the median and the current value shaded:

{% include ft-chart.html id="technicals-volatility-cone" src="/assets/data/financetoolkit-guides/technicals.json" label="Volatility cone for Microsoft over 2023" %}

At the end of 2023, Microsoft's volatility was below the 10th percentile for every window, and at the lowest level of the year for the 10, 90 and 120-day windows, with 8.6% for the 10-day window. The cone also narrows as the window grows: short windows swing between calm and turbulent weeks, long windows average them out.

### Breadth Indicators

Breadth indicators are calculated across all tickers in the `Toolkit` at once, rather than per ticker over time, so they describe the basket (or the market, if you load enough tickers) as a whole. The value is therefore the same in every ticker's column. The TRIN (Arms Index) divides the ratio of advancing to declining stocks by the ratio of their volume: below 1, the volume is concentrated in rising stocks, which is a bullish sign, and above 1 in falling stocks. New Highs - New Lows counts the tickers that set a new high for the window minus those that set a new low.

To calculate all breadth indicators, and the TRIN and New Highs - New Lows over 60 days separately:

```python
companies.technicals.collect_breadth_indicators()

trin = companies.technicals.get_trin()

new_highs_new_lows = companies.technicals.get_new_highs_new_lows(window=60)
```

Which gives the TRIN as a 10-day median, since single days spike far above 1, and in the second tab New Highs - New Lows summed per month:

{% include ft-chart.html id="technicals-breadth" src="/assets/data/financetoolkit-guides/technicals.json" label="TRIN and New Highs - New Lows of Microsoft, ASML, Micron, Amazon and the S&P 500 over 2023" %}

With only five instruments the TRIN is erratic: on a day when nearly all the volume is in the one or two falling stocks it spikes far above 1 (to 77 on 1 May), while its median over the year is about 0.76 and the 10-day median stayed below 1 on 69% of the days. New Highs - New Lows was negative only from August to October, the one stretch of 2023 in which the five set more 60-day lows than highs. Breadth indicators become meaningful with a broad set of tickers, for example every company in a sector or industry, which you can find with the [Finance Database](https://github.com/JerBouma/FinanceDatabase){:target="_blank"}.

### Using the Models Directly

The calculations behind the module are plain functions in `financetoolkit.technicals`, grouped by kind (`breadth_model`, `momentum_model`, `overlap_model` and `volatility_model`). They take a pandas Series or DataFrame, so you can run them on your own data or on a scenario without the `Toolkit` class.

To calculate the Ichimoku Cloud on a steadily rising price series, and Bollinger Bands on five closing prices:

```python
from financetoolkit.technicals import momentum_model, volatility_model

ichimoku_cloud = momentum_model.get_ichimoku_cloud(
    prices_low=pd.Series(range(70, 140, 1)),
    prices_high=pd.Series(range(90, 160, 1)),
    conversion_window=9,
    base_window=20,
    lead_span_b_window=40,
)

bollinger_bands = volatility_model.get_bollinger_bands(
    prices=pd.Series([100, 105, 113, 126, 148]),
    window=2,
    num_std_dev=2,
)
```

Which gives the Ichimoku Cloud, with the cloud shaded between the two leading spans:

{% include ft-chart.html id="technicals-ichimoku-direct" src="/assets/data/financetoolkit-guides/technicals.json" label="Ichimoku Cloud on a steadily rising price series" %}

And the Bollinger Bands:

| | Upper Band | Middle Band | Lower Band | Close |
|--:|--:|--:|--:|--:|
| 0 | | | | 100 |
| 1 | 107.50 | 102.50 | 97.50 | 105 |
| 2 | 117.00 | 109.00 | 101.00 | 113 |
| 3 | 132.50 | 119.50 | 106.50 | 126 |
| 4 | 159.00 | 137.00 | 115.00 | 148 |

In a steady uptrend the conversion line stays above the base line and Leading Span A above Leading Span B, which is the textbook bullish configuration of the Ichimoku Cloud.

{% include ft-charts-script.html %}
