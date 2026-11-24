---
title: Technicals
seo_title: "Technical Indicators in Python | Finance Toolkit"
seo_title_suffix: false
excerpt: The Technicals Module contains 50+ Technical Indicators that can be used to analyze companies. These ratios are divided into 4 categories which are breadth, momentum, overlap and volatility. Each indicator is calculated using the data from the Toolkit module.
description: "Calculate 50+ technical indicators in Python, from RSI, MACD and Bollinger Bands to breadth, momentum, overlap and volatility, with the Finance Toolkit."
author_profile: false
permalink: /projects/financetoolkit/docs/technicals
classes: wide-sidebar
layout: single
redirect_from:
    - /technicals
    - /projects/financetoolkit/technicals-notebook
    - /projects/financetoolkit/technicals-module
sidebar:
    nav: "financetoolkit-docs-technicals"
---

The Technicals Module contains 50+ technical indicators divided into 4 categories: breadth, momentum, overlap and volatility.

Use it in Claude, ChatGPT or another AI assistant through the [Finance Toolkit MCP](/projects/financetoolkit/mcp), or install the Python package:

```python
pip install financetoolkit -U
```

{% include docs-search.html %}

{% include financetoolkit-getting-started/technicals.md %}

## collect_all_indicators
Collect all the technical indicators of every ticker in one table: the breadth, momentum, overlap, volatility and cycle indicators.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>window (int, optional):</u> The number of periods to use for the calculation. Defaults to 14.
The Bollinger Bands and their %B and BandWidth keep their own window of 20
periods (with 2 standard deviations), as defined by Bollinger, and the indicators
without a single window, such as the MACD, the True Strength Index, the Coppock
Curve or the Supertrend, their own defaults.
- <u>close_column (str, optional):</u> The column to use for the calculation. Defaults to "Adj Close".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: Technical indicators calculated based on the specified parameters.

**Notes:**

- The method calculates various types of technical indicators for each asset in the Toolkit instance.
- When growth is requested, the method calculates the growth of the indicator values
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.collect_all_indicators().xs("AAPL", level=1, axis="columns")
```

Which returns:

| Date       |   McClellan Oscillator |   Advancers - Decliners |   On-Balance Volume |   Price Volume Trend |   Accumulation/Distribution Line |   Chaikin Oscillator |     TRIN |   New Highs - New Lows |   Chaikin Money Flow |   Ease of Movement |   Negative Volume Index |   Positive Volume Index |   Klinger Volume Oscillator |   Klinger Volume Oscillator Signal Line |   Market Facilitation Index |   Williams Accumulation/Distribution |   Relative Volume |   Volume Flow Indicator |   Finite Volume Elements |   Twiggs Money Flow |   Volume Zone Oscillator |   Cumulative Force Index |   Price Volume |   Price Volume Rank |   Buying Pressure |   Selling Pressure |   Archer On-Balance Volume Fast Average |   Archer On-Balance Volume Slow Average |   Archer On-Balance Volume Minimum |   Archer On-Balance Volume Maximum |   Archer On-Balance Volume Long Run |   Archer On-Balance Volume Short Run |   Money Flow Index |   Williams %R |   Aroon Indicator Up |   Aroon Indicator Down |   Aroon Oscillator |   Commodity Channel Index |   Relative Vigor Index |   Relative Vigor Index Signal Line |       Force Index |   Ultimate Oscillator |   Percentage Price Oscillator |   Percentage Price Oscillator Signal Line |   Percentage Price Oscillator Histogram |   Absolute Price Oscillator |   Percentage Volume Oscillator |   Percentage Volume Oscillator Signal Line |   Percentage Volume Oscillator Histogram |   Detrended Price Oscillator |   Average Directional Index |   Plus Directional Movement |   Minus Directional Movement |   Plus Directional Indicator |   Minus Directional Indicator |   Directional Movement Index |   Average Directional Index Rating |   Chande Momentum Oscillator |   Intraday Momentum Index |   Ichimoku Conversion Line |   Ichimoku Base Line |   Ichimoku Leading Span A |   Ichimoku Leading Span B |   Stochastic %K |   Stochastic %D |   MACD Line |   MACD Signal Line |   MACD Histogram |   Relative Strength Index |   Stochastic RSI %K |   Stochastic RSI %D |   True Strength Index |   True Strength Index Signal Line |   Balance of Power |   Internal Bar Strength |   Qstick |   Awesome Oscillator |   Accelerator Oscillator |   Vortex Indicator VI+ |   Vortex Indicator VI- |   Elder Ray Bull Power |   Elder Ray Bear Power |   Rate of Change |   Momentum |   Choppiness Index |   Efficiency Ratio |   Vertical Horizontal Filter |   Know Sure Thing |   Know Sure Thing Signal Line |   Coppock Curve |   Fisher Transform |   Fisher Transform Trigger |   Inverse Fisher Transform RSI |   KDJ K |   KDJ D |   KDJ J |   Premier Stochastic Oscillator |   Stochastic Momentum Index |   Stochastic Momentum Index Signal Line |   SMI Ergodic Indicator |   SMI Ergodic Signal Line |   SMI Ergodic Oscillator |   Schaff Trend Cycle |   WaveTrend |   WaveTrend Signal Line |   Derivative Oscillator |   Swing Index |   Accumulative Swing Index |     QQE |   QQE RSI Moving Average |   Dynamic Momentum Index |   Price Zone Oscillator |   Connors RSI |   Inertia |    Bias |   BRAR AR |   BRAR BR |   Pretty Good Oscillator |   Psychological Line |   Volatility-Based Momentum |   AMAT Long Run |   AMAT Short Run |   TTM Trend |   Correlation Trend Indicator |   Forecast Oscillator |   Projection Oscillator |   Simple Moving Average (SMA) |   Exponential Moving Average (EMA) |   Double Exponential Moving Average (DEMA) |   TRIX |   Triangular Moving Average |   Weighted Moving Average (WMA) |   Hull Moving Average (HMA) |   Triple Exponential Moving Average (TEMA) |   Zero Lag Exponential Moving Average (ZLEMA) |   Wilder's Smoothed Moving Average (RMA) |   Sine Weighted Moving Average (SINWMA) |   Fibonacci Weighted Moving Average (FWMA) |   Pascal's Weighted Moving Average (PWMA) |   Kaufman Adaptive Moving Average (KAMA) |   Tillson T3 Moving Average (T3) |   Arnaud Legoux Moving Average (ALMA) |   Volume Weighted Moving Average (VWMA) |   McGinley Dynamic |   Variable Index Dynamic Average (VIDYA) |   Fractal Adaptive Moving Average (FRAMA) |   Holt-Winters Moving Average (HWMA) |   Holt-Winters Channel Upper Band |   Holt-Winters Channel Lower Band |   Elastic Volume Weighted Moving Average (EVWMA) |   Volume Adjusted Moving Average (VAMA) |   Midpoint |   Midpoint Price |   Average Price |   Median Price |   Typical Price |   Weighted Close Price |   Volume Weighted Average Price (VWAP) |   Parabolic SAR |   Gann HiLo Activator |   Zig Zag |   Pivot Point |   Pivot Point Resistance 1 |   Pivot Point Support 1 |   Fibonacci Retracement 50.0% |   Fibonacci Retracement 61.8% |   Bollinger Band Upper |   Bollinger Band Middle |   Bollinger Band Lower |   Bollinger %B |   Bollinger BandWidth |   True Range |   Average True Range |   Mass Index |   Supertrend |   Supertrend Trend Direction |   Chandelier Exit Long |   Chandelier Exit Short |   Keltner Channel Upper |   Keltner Channel Middle |   Keltner Channel Lower |   Donchian Channel Upper |   Donchian Channel Middle |   Donchian Channel Lower |   Normalized Average True Range |   Average Day Range |   Chaikin Volatility |   Relative Volatility Index |   Acceleration Band Upper |   Acceleration Band Middle |   Acceleration Band Lower |   Chande Kroll High Stop |   Chande Kroll Low Stop |   Adaptive Price Zone Upper |   Adaptive Price Zone Middle |   Adaptive Price Zone Lower |   Aberration Upper |   Aberration Middle |   Aberration Lower |    PMax |   PMax Trend Direction |   Price Distance |   Market Thermometer |   Market Thermometer Average |   Squeeze Momentum |   Squeeze |   Hilbert Dominant Cycle Period |   Hilbert Dominant Cycle Phase |   Hilbert In Phase |   Hilbert Quadrature |   Hilbert Sine |   Hilbert Lead Sine |   Hilbert Trend Mode |   Hilbert Instantaneous Trendline |   MESA Adaptive Moving Average (MAMA) |   Following Adaptive Moving Average (FAMA) |   Swiss Army Knife Filter |   SuperSmoother Filter |   Even Better Sinewave |   Detrended Synthetic Price |   MESA Sine Wave Sine |   MESA Sine Wave Lead Sine |   Center of Gravity Oscillator |   Center of Gravity Trigger |   Laguerre RSI |
|:-----------|-----------------------:|------------------------:|--------------------:|---------------------:|---------------------------------:|---------------------:|---------:|-----------------------:|---------------------:|-------------------:|------------------------:|------------------------:|----------------------------:|----------------------------------------:|----------------------------:|-------------------------------------:|------------------:|------------------------:|-------------------------:|--------------------:|-------------------------:|-------------------------:|---------------:|--------------------:|------------------:|-------------------:|----------------------------------------:|----------------------------------------:|-----------------------------------:|-----------------------------------:|------------------------------------:|-------------------------------------:|-------------------:|--------------:|---------------------:|-----------------------:|-------------------:|--------------------------:|-----------------------:|-----------------------------------:|------------------:|----------------------:|------------------------------:|------------------------------------------:|----------------------------------------:|----------------------------:|-------------------------------:|-------------------------------------------:|-----------------------------------------:|-----------------------------:|----------------------------:|----------------------------:|-----------------------------:|-----------------------------:|------------------------------:|-----------------------------:|-----------------------------------:|-----------------------------:|--------------------------:|---------------------------:|---------------------:|--------------------------:|--------------------------:|----------------:|----------------:|------------:|-------------------:|-----------------:|--------------------------:|--------------------:|--------------------:|----------------------:|----------------------------------:|-------------------:|------------------------:|---------:|---------------------:|-------------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------:|-----------:|-------------------:|-------------------:|-----------------------------:|------------------:|------------------------------:|----------------:|-------------------:|---------------------------:|-------------------------------:|--------:|--------:|--------:|--------------------------------:|----------------------------:|----------------------------------------:|------------------------:|--------------------------:|-------------------------:|---------------------:|------------:|------------------------:|------------------------:|--------------:|---------------------------:|--------:|-------------------------:|-------------------------:|------------------------:|--------------:|----------:|--------:|----------:|----------:|-------------------------:|---------------------:|----------------------------:|----------------:|-----------------:|------------:|------------------------------:|----------------------:|------------------------:|------------------------------:|-----------------------------------:|-------------------------------------------:|-------:|----------------------------:|--------------------------------:|----------------------------:|-------------------------------------------:|----------------------------------------------:|-----------------------------------------:|----------------------------------------:|-------------------------------------------:|------------------------------------------:|-----------------------------------------:|---------------------------------:|--------------------------------------:|----------------------------------------:|-------------------:|-----------------------------------------:|------------------------------------------:|-------------------------------------:|----------------------------------:|----------------------------------:|-------------------------------------------------:|----------------------------------------:|-----------:|-----------------:|----------------:|---------------:|----------------:|-----------------------:|---------------------------------------:|----------------:|----------------------:|----------:|--------------:|---------------------------:|------------------------:|------------------------------:|------------------------------:|-----------------------:|------------------------:|-----------------------:|---------------:|----------------------:|-------------:|---------------------:|-------------:|-------------:|-----------------------------:|-----------------------:|------------------------:|------------------------:|-------------------------:|------------------------:|-------------------------:|--------------------------:|-------------------------:|--------------------------------:|--------------------:|---------------------:|----------------------------:|--------------------------:|---------------------------:|--------------------------:|-------------------------:|------------------------:|----------------------------:|-----------------------------:|----------------------------:|-------------------:|--------------------:|-------------------:|--------:|-----------------------:|-----------------:|---------------------:|-----------------------------:|-------------------:|----------:|--------------------------------:|-------------------------------:|-------------------:|---------------------:|---------------:|--------------------:|---------------------:|----------------------------------:|--------------------------------------:|-------------------------------------------:|--------------------------:|-----------------------:|-----------------------:|----------------------------:|----------------------:|---------------------------:|-------------------------------:|----------------------------:|---------------:|
| 2025-12-17 |                -0.0981 |                      -1 |         2.26688e+09 |          6.59406e+07 |                      3.99771e+09 |         -1.74849e+07 | nan      |                      0 |              -0.0358 |            -4.7166 |                 2735.53 |                 788.839 |                -2.03391e+08 |                            -4.28732e+07 |                      8.9837 |                              165.336 |            1.171  |                 25.8886 |                  -0.0337 |             -0.0429 |                  -0.194  |              1.01185e+10 |    1.36297e+10 |                   3 |            0.7602 |             0.9939 |                             2.29242e+09 |                             2.31813e+09 |                        2.26688e+09 |                        2.31702e+09 |                                   0 |                                    1 |            39.7393 |      -98.8222 |              28.5714 |               100      |           -71.4286 |                 -139.905  |                -0.2262 |                            -0.0758 |      -3.27416e+07 |               44.5331 |                        0.0063 |                                    0.0116 |                                 -0.0053 |                      1.7262 |                        -0.0329 |                                    -0.0509 |                                   0.018  |                       0.0306 |                     24.6713 |                     12.185  |                      13.7577 |                      17.868  |                       20.1742 |                       6.0622 |                            27.6362 |                     -20.6209 |                   41.1264 |                    275.43  |              276.008 |                   265.041 |                   250.519 |          1.1778 |          8.6605 |      1.7262 |             3.1596 |          -1.4334 |                   45.1866 |              0      |              1.2037 |               12.3225 |                           19.7487 |            -0.7013 |                  0.0442 |  -0.4015 |               1.2653 |                  -1.836  |                 0.9211 |                 1.0533 |                -0.1328 |                -4.6371 |          -0.0206 |    -5.6902 |            49.8427 |             0.2062 |                       0.5182 |            0.3638 |                        0.5107 |          0.0029 |            -2.2385 |                    -1.8906 |                        -0.8927 | 15.8397 | 25.2454 | -2.9718 |                         -0.84   |                      9.1395 |                                 26.1148 |                 -6.2668 |                    4.4051 |                 -10.6719 |               1.3165 |     -2.5415 |                 12.0151 |                 -6.9465 |      -38.8013 |                    5877.92 | 57.4732 |                  50.8734 |                  13.8158 |                -14.5643 |       20.1105 |   51.7715 | -0.014  |  131.997  |  121.214  |                  -1.3452 |              33.3333 |                     -2.243  |               0 |                1 |          -1 |                       -0.8216 |               -0.013  |                  0.2466 |                       277.781 |                            275.314 |                                    275.767 | 0.0016 |                     277.982 |                         276.128 |                     273.116 |                                    273.419 |                                       274.067 |                                  273.378 |                                 278.063 |                                    273.419 |                                   277.589 |                                  274.218 |                          279.323 |                               274.905 |                                 277.896 |            271.978 |                                  270.616 |                                   275.481 |                              276.12  |                           280.057 |                           272.184 |                                          273.073 |                                 277.765 |    278.046 |          279.158 |         272.712 |        272.949 |         272.265 |                271.923 |                                277.974 |         285.493 |               280.207 |   270.697 |       273.015 |                    275.185 |                 271.488 |                       279.158 |                       277.161 |                285.548 |                 276     |                266.452 |         0.2327 |                0.0692 |       4.5043 |               4.871  |      24.5798 |      268.465 |                            1 |                272.67  |                 279.347 |                 284.794 |                  275.314 |                 265.833 |                  287.618 |                   279.232 |                  270.846 |                          0.018  |              4.5036 |              -0.1546 |                     49.6227 |                   288.841 |                    276     |                   263.609 |                  282.999 |                 270.062 |                     284.262 |                      275.342 |                     266.422 |            279.563 |             274.669 |            269.775 | 263.457 |                      1 |           6.2482 |               0.6577 |                       1.7931 |             0.179  |         1 |                         18.3902 |                       282.339  |            -2.1962 |               4.3124 |        -0.9769 |             -0.5397 |                    0 |                           276.437 |                               276.673 |                                    273.841 |                   -2.8349 |                274.241 |                -0.9054 |                     -1.3767 |               -0.7739 |                    -0.0994 |                        -5.5219 |                     -5.5285 |         0      |
| 2025-12-18 |                -0.0378 |                       1 |         2.31851e+09 |          6.6007e+07  |                      4.02708e+09 |         -1.16789e+07 | nan      |                      0 |               0.0024 |            -7.4094 |                 2735.53 |                 789.855 |                -2.50907e+08 |                            -7.25923e+07 |                     12.8931 |                              170.558 |            1.1996 |                 25.9203 |                   0.0135 |             -0.0099 |                  -0.0055 |              1.0083e+10  |    1.40534e+10 |                   1 |            0.9191 |             0.961  |                             2.30286e+09 |                             2.31819e+09 |                        2.26688e+09 |                        2.31851e+09 |                                   0 |                                    1 |            34.4002 |      -75.8192 |              21.4286 |               100      |           -78.5714 |                 -162.428  |                -0.2832 |                            -0.1659 |      -2.59752e+07 |               50.9808 |                        0.0047 |                                    0.0102 |                                 -0.0055 |                      1.2731 |                        -0.0132 |                                    -0.0434 |                                   0.0302 |                      -0.3822 |                     24.4324 |                     11.3147 |                      17.4488 |                      16.1683 |                       24.9338 |                      21.3261 |                            28.0928 |                     -24.9064 |                   36.3175 |                    272.6   |              276.008 |                   265.041 |                   250.519 |         24.1808 |         14.0381 |      1.2731 |             2.7823 |          -1.5092 |                   45.9182 |              2.4336 |              2.0149 |                9.3441 |                           17.1476 |            -0.2126 |                  0.7844 |  -0.6157 |               0.0099 |                  -2.1487 |                 0.865  |                 1.0802 |                -2.0699 |                -8.7267 |          -0.0239 |    -6.6369 |            42.7375 |             0.2491 |                       0.5366 |            0.311  |                        0.4834 |         -0.014  |            -2.6249 |                    -2.2385 |                        -0.9368 | 23.7921 | 24.761  | 21.8543 |                         -0.8426 |                      3.2693 |                                 21.5457 |                -10.1477 |                   -0.4458 |                  -9.7019 |               0.6582 |    -12.4226 |                  2.2173 |                 -7.2145 |      -12.5266 |                    5865.39 | 55.8771 |                  49.2217 |                  15.5532 |                  0.5149 |       46.5574 |   50.526  | -0.0123 |  108.702  |  105.088  |                  -1.1882 |              33.3333 |                     -2.7539 |               0 |                1 |          -1 |                       -0.9297 |               -0.003  |                  0.5333 |                       277.308 |                            274.771 |                                    274.694 | 0.0014 |                     277.238 |                         275.257 |                     271.901 |                                    272.199 |                                       272.815 |                                  273.226 |                                 277.267 |                                    272.587 |                                   277.094 |                                  274.081 |                          279.146 |                               273.813 |                                 277.325 |            271.925 |                                  270.663 |                                   273.495 |                              274.766 |                           278.713 |                           270.819 |                                          272.916 |                                 277.208 |    278.046 |          276.821 |         270.652 |        269.352 |         269.983 |                270.298 |                                277.321 |         284.309 |               279.456 |   266.023 |       272.265 |                    273.833 |                 269.328 |                       276.821 |                       274.272 |                285.211 |                 276.181 |                267.151 |         0.2267 |                0.0654 |       6.6568 |               4.9986 |      24.6224 |      268.465 |                            1 |                272.441 |                 279.575 |                 284.635 |                  274.771 |                 264.907 |                  287.618 |                   279.158 |                  270.697 |                          0.0184 |              4.7648 |              -0.1054 |                     52.2511 |                   288.909 |                    276.181 |                   263.684 |                  282.999 |                 270.955 |                     283.909 |                      274.378 |                     264.847 |            278.441 |             273.429 |            268.418 | 263.457 |                      1 |          13.6624 |               4.6738 |                       2.0436 |            -1.5338 |         1 |                         18.2309 |                       303.757  |            -0.8123 |               1.9646 |        -0.8314 |             -0.195  |                    1 |                           276.799 |                               276.073 |                                    273.964 |                   -2.5273 |                272.939 |                -0.9568 |                     -1.5143 |               -0.6032 |                     0.1375 |                        -5.5252 |                     -5.5219 |         0      |
| 2025-12-19 |                 0.0139 |                       1 |         2.46314e+09 |          6.67935e+07 |                      4.11448e+09 |          1.95656e+07 | nan      |                      0 |               0.1361 |            -9.4904 |                 2735.53 |                 794.15  |                -1.89072e+08 |                            -8.92323e+07 |                      3.2384 |                              174.315 |            3.3172 |                 27.1858 |                   0.149  |              0.0742 |                   0.3343 |              1.00928e+10 |    3.95814e+10 |                   1 |            1.2421 |             0.9738 |                             2.36697e+09 |                             2.34049e+09 |                        2.31851e+09 |                        2.46314e+09 |                                   1 |                                    0 |            43.3299 |      -68.989  |              14.2857 |                92.8571 |           -78.5714 |                 -103.239  |                -0.2694 |                            -0.2349 |       5.93143e+06 |               51.5414 |                        0.0037 |                                    0.0089 |                                 -0.0052 |                      1.0212 |                         0.1453 |                                    -0.0056 |                                   0.1509 |                      -0.4186 |                     23.9078 |                     11.4732 |                      16.2024 |                      16.469  |                       23.2575 |                      17.0882 |                            28.6043 |                     -39.3401 |                   28.2097 |                    272.6   |              276.008 |                   265.041 |                   250.519 |         31.011  |         18.7898 |      1.0212 |             2.4301 |          -1.4089 |                   49.0174 |             12.7427 |              5.0588 |                7.6467 |                           14.7723 |             0.3234 |                  0.8021 |  -0.8698 |              -1.1188 |                  -2.2692 |                 0.903  |                 1.137  |                -0.8132 |                -5.4969 |          -0.0333 |    -9.3972 |            41.2482 |             0.3934 |                       0.5987 |            0.2645 |                        0.4504 |         -0.0269 |            -2.3555 |                    -2.6249 |                        -0.9292 | 32.8313 | 27.4511 | 43.5917 |                         -0.7977 |                     -0.9462 |                                 17.0473 |                 -9.7979 |                   -3.5632 |                  -6.2347 |               0.3291 |    -16.4302 |                 -6.2154 |                 -6.63   |       14.9273 |                    5880.32 | 55.8245 |                  49.1536 |                  57.0396 |                 13.6936 |       64.4303 |   49.4718 | -0.007  |  113.263  |  110.127  |                  -0.7701 |              41.6667 |                     -2.0674 |               0 |                1 |          -1 |                       -0.9192 |                0.0092 |                  0.7123 |                       276.636 |                            274.498 |                                    274.194 | 0.0012 |                     276.433 |                         274.645 |                     271.147 |                                    271.835 |                                       272.223 |                                  273.19  |                                 276.385 |                                    272.635 |                                   276.649 |                                  273.957 |                          278.852 |                               273.059 |                                 276.053 |            271.981 |                                  270.755 |                                   272.783 |                              273.865 |                           277.958 |                           269.773 |                                          272.876 |                                 276.066 |    278.046 |          276.821 |         271.634 |        271.305 |         271.777 |                272.012 |                                276.002 |         282.481 |               278.475 |   266.023 |       269.983 |                    273.942 |                 267.286 |                       276.821 |                       274.272 |                284.285 |                 276.55  |                268.816 |         0.2524 |                0.0559 |       4.6837 |               4.9761 |      24.6659 |      268.465 |                            1 |                272.493 |                 279.704 |                 284.312 |                  274.498 |                 264.683 |                  287.618 |                   276.821 |                  266.023 |                          0.0182 |              4.5812 |              -0.036  |                     54.7332 |                   288.375 |                    276.55  |                   264.349 |                  282.999 |                 270.93  |                     283.524 |                      273.768 |                     264.013 |            277.346 |             272.356 |            267.367 | 263.457 |                      1 |           7.8924 |               0.9667 |                       1.95   |            -3.209  |         1 |                         18.064  |                       -35.1903 |            -0.6121 |              -1.6203 |        -0.5763 |              0.1704 |                    1 |                           276.956 |                               274.397 |                                    274.072 |                   -2.0487 |                272.161 |                -0.9881 |                     -1.274  |               -0.2922 |                     0.4696 |                        -5.5254 |                     -5.5252 |         0      |
| 2025-12-22 |                -0.0419 |                      -1 |         2.42657e+09 |          6.64327e+07 |                      4.08789e+09 |          2.21089e+07 | nan      |                      0 |               0.079  |           -12.8267 |                 2708.55 |                 794.15  |                -1.99306e+08 |                            -1.04957e+08 |                      9.1827 |                              171.415 |            0.7534 |                 27.6286 |                   0.1149 |              0.0461 |                   0.2145 |              1.00828e+10 |    9.90986e+09 |                   4 |            1.1372 |             0.9639 |                             2.39081e+09 |                             2.35373e+09 |                        2.42657e+09 |                        2.46314e+09 |                                   1 |                                    0 |            36.4312 |      -81.4487 |               7.1429 |                85.7143 |           -78.5714 |                 -104.733  |                -0.2367 |                            -0.2614 |      -7.97965e+06 |               45.7604 |                        0.0022 |                                    0.0076 |                                 -0.0054 |                      0.5976 |                         0.1018 |                                     0.0158 |                                   0.0859 |                       2.2593 |                     23.4207 |                     10.6537 |                      15.0451 |                      15.6562 |                       22.1097 |                      17.0882 |                            29.1456 |                     -64.5455 |                   17.6515 |                    272.6   |              276.008 |                   264.954 |                   250.519 |         18.5513 |         24.581  |      0.5976 |             2.0636 |          -1.466  |                   44.0574 |              0      |              5.0588 |                4.6682 |                           12.2463 |            -0.5608 |                  0.1365 |  -1.2314 |              -2.0902 |                  -2.1525 |                 0.8075 |                 1.2147 |                -0.8978 |                -4.2561 |          -0.0532 |   -15.1671 |            40.4149 |             0.6455 |                       0.5589 |            0.2055 |                        0.4111 |         -0.0418 |            -2.0419 |                    -2.3555 |                        -0.9498 | 32.0392 | 28.9805 | 38.1567 |                         -0.7692 |                     -4.8407 |                                 12.6697 |                -13.7773 |                   -6.9679 |                  -6.8094 |               0.1646 |    -20.9318 |                -13.0815 |                 -6.456  |      -45.6961 |                    5834.63 | 54.1419 |                  47.4549 |                  37.2576 |                 -1.2512 |       20.8244 |   48.1033 | -0.0165 |  110.181  |  102.622  |                  -1.0926 |              41.6667 |                     -1.9446 |               0 |                1 |          -1 |                       -0.9246 |                0.0011 |                  0.5069 |                       275.553 |                            273.902 |                                    273.122 | 0.0009 |                     275.578 |                         273.764 |                     270.399 |                                    270.666 |                                       270.96  |                                  272.964 |                                 275.489 |                                    271.634 |                                   275.978 |                                  273.151 |                          278.443 |                               272.238 |                                 275.011 |            271.838 |                                  270.713 |                                   272.504 |                              272.454 |                           276.493 |                           268.414 |                                          272.723 |                                 275.059 |    276.596 |          276.821 |         271.111 |        271.25  |         270.843 |                270.64  |                                275.063 |         280.835 |               277.345 |   266.023 |       271.777 |                    274.59  |                 269.906 |                       276.821 |                       274.272 |                284.343 |                 276.525 |                268.707 |         0.0846 |                0.0565 |       3.3583 |               4.8605 |      24.609  |      268.465 |                            1 |                272.722 |                 279.644 |                 283.406 |                  273.902 |                 264.397 |                  287.618 |                   276.821 |                  266.023 |                          0.018  |              4.4815 |              -0.0369 |                     51.5807 |                   287.967 |                    276.525 |                   265.009 |                  282.999 |                 270.776 |                     282.464 |                      273.023 |                     263.583 |            276.457 |             271.577 |            266.696 | 263.457 |                      1 |           5.6404 |               0      |                       1.7804 |            -5.0602 |         1 |                         17.9853 |                       -17.9254 |            -2.3868 |              -3.8682 |        -0.3078 |              0.4552 |                    1 |                           276.873 |                               274.178 |                                    274.075 |                   -1.347  |                271.642 |                -0.9995 |                     -1.4735 |                0.1789 |                     0.8222 |                        -5.5263 |                     -5.5254 |         0      |
| 2025-12-23 |                 0.0106 |                       1 |         2.45621e+09 |          6.65847e+07 |                      4.11471e+09 |          2.96727e+07 | nan      |                      0 |               0.0651 |           -14.4654 |                 2722.44 |                 794.15  |                -2.24884e+08 |                            -1.22089e+08 |                      9.8839 |                              174.205 |            0.6251 |                 27.8548 |                   0.1894 |              0.071  |                   0.2753 |              1.00822e+10 |    8.07329e+09 |                   2 |            1.0956 |             0.8755 |                             2.41697e+09 |                             2.3695e+09  |                        2.42657e+09 |                        2.45621e+09 |                                   1 |                                    0 |            37.2984 |      -69.5725 |               0      |                78.5714 |           -78.5714 |                  -97.9344 |                -0.205  |                            -0.2501 |      -1.44128e+06 |               49.1967 |                        0.0014 |                                    0.0063 |                                 -0.005  |                      0.3694 |                         0.0548 |                                     0.0236 |                                   0.0311 |                       2.351  |                     23.1944 |                      9.8927 |                      14.9172 |                      14.9624 |                       22.5619 |                      20.2521 |                            28.9735 |                     -51.4169 |                   23.8077 |                    272.6   |              276.008 |                   265.083 |                   250.519 |         30.4275 |         26.6632 |      0.3694 |             1.7248 |          -1.3553 |                   47.029  |             15.5282 |              9.4236 |                3.0048 |                            9.9359 |             0.517  |                  0.9524 |  -0.9773 |              -2.6623 |                  -1.7431 |                 0.7732 |                 1.2661 |                -1.9284 |                -4.8582 |          -0.0415 |   -11.7491 |            46.4518 |             0.5142 |                       0.4243 |            0.1522 |                        0.3663 |         -0.0501 |            -1.9612 |                    -2.0419 |                        -0.9406 | 35.0211 | 30.994  | 43.0753 |                         -0.727  |                     -6.7949 |                                  8.7768 |                -13.4496 |                   -9.1285 |                  -4.3211 |               0.0823 |    -24.6243 |                -18.6022 |                 -5.7342 |       12.4911 |                    5847.12 | 53.9827 |                  47.3129 |                  56.8024 |                 12.1426 |       57.2709 |   47.6333 | -0.0114 |  105.311  |  103.415  |                  -0.6584 |              50      |                     -1.3037 |               0 |                1 |          -1 |                       -0.9141 |                0.0076 |                  0.7178 |                       274.714 |                            273.57  |                                    272.607 | 0.0007 |                     274.764 |                         273.212 |                     269.985 |                                    270.319 |                                       270.788 |                                  272.853 |                                 274.716 |                                    271.545 |                                   275.004 |                                  272.908 |                          277.949 |                               271.772 |                                 274.32  |            271.808 |                                  270.755 |                                   272.185 |                              271.5   |                           275.349 |                           267.651 |                                          272.665 |                                 274.38  |    274.877 |          274.882 |         270.373 |        270.089 |         270.531 |                270.752 |                                274.256 |         279.354 |               276.408 |   266.023 |       270.843 |                    272.115 |                 268.757 |                       274.882 |                       272.792 |                284.455 |                 276.347 |                268.24  |         0.1958 |                0.0587 |       2.9298 |               4.7226 |      24.5236 |      268.465 |                            1 |                273     |                 279.366 |                 282.71  |                  273.57  |                 264.43  |                  287.618 |                   276.821 |                  266.023 |                          0.0174 |              4.3121 |              -0.0391 |                     54.401  |                   287.422 |                    276.347 |                   265.252 |                  282.999 |                 270.593 |                     281.343 |                      272.509 |                     263.674 |            275.83  |             271.08  |            266.329 | 263.457 |                      1 |           4.4745 |               0.9467 |                       1.7079 |            -6.1264 |         1 |                         18.0561 |                        -3.6741 |            -3.886  |              -1.9042 |        -0.0641 |              0.6603 |                    1 |                           276.637 |                               274.04  |                                    274.074 |                   -0.5972 |                271.196 |                -0.9999 |                     -1.2831 |                0.8774 |                     0.9597 |                        -5.5259 |                     -5.5263 |         0      |
| 2025-12-24 |                 0.0554 |                       1 |         2.47412e+09 |          6.66801e+07 |                      4.11466e+09 |          3.00518e+07 | nan      |                      0 |               0.0846 |            -6.6454 |                 2736.93 |                 794.15  |                -2.1628e+08  |                            -1.35545e+08 |                     17.9713 |                              175.81  |            0.3926 |                 27.2474 |                   0.156  |              0.0697 |                   0.3125 |              1.00864e+10 |    4.9041e+09  |                   2 |            1.0156 |             0.8174 |                             2.43983e+09 |                             2.38559e+09 |                        2.45621e+09 |                        2.47412e+09 |                                   1 |                                    0 |            41.6581 |      -51.6561 |               0      |                71.4286 |           -71.4286 |                  -34.6705 |                -0.1841 |                            -0.2228 |       2.20161e+06 |               54.4448 |                        0.0011 |                                    0.0053 |                                 -0.0042 |                      0.3017 |                        -0.0045 |                                     0.018  |                                  -0.0225 |                       3.0907 |                     22.018  |                     12.1059 |                      13.8517 |                      18.736  |                       21.4379 |                       6.7256 |                            28.2487 |                     -32.919  |                   31.7545 |                    272.6   |              276.008 |                   265.063 |                   250.519 |         48.3439 |         32.4409 |      0.3017 |             1.4402 |          -1.1385 |                   50.0121 |             38.5455 |             18.0246 |                2.4525 |                            8.0651 |             0.4551 |                  0.4985 |  -0.6307 |              -2.8188 |                  -1.0827 |                 0.8892 |                 1.1613 |                 1.0804 |                -2.1383 |          -0.0245 |    -6.8661 |            53.1324 |             0.3292 |                       0.3731 |            0.1033 |                        0.3168 |         -0.0518 |            -1.5593 |                    -1.9612 |                        -0.8894 | 40.6707 | 34.2196 | 53.573  |                         -0.6448 |                     -7.0164 |                                  5.6181 |                -10.3613 |                   -9.5394 |                  -0.8219 |               0.0411 |    -22.4462 |                -21.1081 |                 -4.3189 |       36.2295 |                    5883.35 | 53.9827 |                  48.2126 |                  42.5356 |                 23.8305 |       67.2632 |   47.9699 | -0.0071 |  112.863  |  120.363  |                  -0.2751 |              58.3333 |                     -0.8397 |               0 |                1 |           1 |                       -0.852  |                0.0123 |                  0.8331 |                       274.223 |                            273.476 |                                    272.559 | 0.0006 |                     274.049 |                         272.965 |                     270.161 |                                    270.616 |                                       270.958 |                                  272.854 |                                 274.088 |                                    272.044 |                                   273.884 |                                  272.904 |                          277.412 |                               271.704 |                                 273.909 |            271.882 |                                  270.834 |                                   272.353 |                              270.973 |                           274.704 |                           267.242 |                                          272.67  |                                 273.974 |    273.921 |          273.094 |         272.496 |        272.864 |         272.863 |                272.862 |                                273.798 |         278.021 |               275.97  |   266.023 |       270.531 |                    272.438 |                 269.508 |                       273.094 |                       271.425 |                284.438 |                 276.19  |                267.941 |         0.2981 |                0.0597 |       3.2188 |               4.6152 |      24.4118 |      268.465 |                            1 |                273.225 |                 280.416 |                 282.345 |                  273.476 |                 264.606 |                  283.741 |                   274.882 |                  266.023 |                          0.0169 |              4.105  |              -0.037  |                     56.7182 |                   286.983 |                    276.19  |                   265.287 |                  282.999 |                 270.458 |                     280.619 |                      272.348 |                     264.077 |            275.848 |             271.199 |            266.551 | 263.457 |                      1 |           4.9926 |               2.9198 |                       1.8133 |            -6.7609 |         1 |                         18.3028 |                         9.1699 |            -4.0014 |              -0.3151 |         0.1594 |              0.8108 |                    1 |                           276.361 |                               273.981 |                                    274.072 |                    0.2127 |                271.251 |                -0.9962 |                     -0.8825 |                0.6824 |                    -0.0344 |                        -5.519  |                     -5.5259 |         0.1145 |
| 2025-12-26 |                -0.0066 |                      -1 |         2.4526e+09  |          6.66479e+07 |                      4.10239e+09 |          2.35736e+07 | nan      |                      0 |               0.0857 |            -5.4396 |                 2736.93 |                 792.961 |                -1.90374e+08 |                            -1.43378e+08 |                     11.6221 |                              173.846 |            0.4872 |                 26.5611 |                   0.0943 |              0.0554 |                   0.2254 |              1.00882e+10 |    5.88406e+09 |                   3 |            0.9294 |             0.7778 |                             2.44494e+09 |                             2.3959e+09  |                        2.4526e+09  |                        2.47412e+09 |                                   1 |                                    0 |            46.9441 |      -51.1363 |               0      |                64.2857 |           -64.2857 |                  -25.6932 |                -0.1697 |                            -0.1974 |  735552           |               51.2159 |                        0.0008 |                                    0.0044 |                                 -0.0036 |                      0.2126 |                        -0.0488 |                                     0.0046 |                                  -0.0534 |                      -0.6819 |                     20.9257 |                     11.2412 |                      12.8623 |                      17.9861 |                       20.58   |                       6.7256 |                            27.2889 |                     -27.7033 |                   33.1185 |                    272.6   |              276.098 |                   264.961 |                   250.519 |         48.8637 |         42.545  |      0.2126 |             1.1946 |          -0.982  |                   49.1689 |             34.6217 |             29.5651 |                1.7619 |                            6.4893 |            -0.3028 |                  0.2151 |  -0.5595 |              -2.1658 |                   0.0054 |                 0.9091 |                 1.1011 |                 1.1553 |                -1.346  |          -0.0193 |    -5.3614 |            55.49   |             0.277  |                       0.4022 |            0.0564 |                        0.2631 |         -0.0522 |            -1.1484 |                    -1.5593 |                        -0.8224 | 43.4017 | 37.2803 | 55.6445 |                         -0.4625 |                     -6.9074 |                                  3.113  |                 -9.0825 |                   -9.3871 |                   0.3046 |               0.0206 |    -20.284  |                -22.0716 |                 -2.8918 |       -3.8045 |                    5879.54 | 53.9827 |                  48.5314 |                  33.7903 |                  7.3734 |       39.8837 |   48.2486 | -0.0094 |  120.453  |  119.909  |                  -0.284  |              58.3333 |                     -0.7927 |               1 |                0 |           1 |                       -0.7986 |                0.0095 |                  0.7973 |                       273.84  |                            273.339 |                                    272.426 | 0.0004 |                     273.429 |                         272.729 |                     270.664 |                                    270.745 |                                       271.364 |                                  272.825 |                                 273.546 |                                    272.197 |                                   272.872 |                                  272.88  |                          276.858 |                               271.784 |                                 273.559 |            271.922 |                                  270.903 |                                   272.475 |                              270.423 |                           273.963 |                           266.884 |                                          272.663 |                                 273.628 |    273.921 |          272.6   |         272.996 |        273.163 |         272.926 |                272.807 |                                273.418 |         276.821 |               275.64  |   266.023 |       272.863 |                    274.471 |                 271.252 |                       272.6   |                       271.048 |                284.387 |                 275.983 |                267.579 |         0.2899 |                0.0609 |       2.5013 |               4.4642 |      24.2185 |      268.465 |                            1 |                273.538 |                 280.103 |                 281.822 |                  273.339 |                 264.856 |                  280.164 |                   273.094 |                  266.023 |                          0.0164 |              4.0637 |              -0.1593 |                     54.2874 |                   286.737 |                    275.983 |                   265.137 |                  282.851 |                 270.265 |                     279.904 |                      272.297 |                     264.69  |            276.293 |             271.788 |            267.282 | 263.457 |                      1 |           4.594  |               0      |                       1.6556 |            -7.2886 |         1 |                         18.6492 |                        13.3467 |            -4.0726 |               2.8793 |         0.2308 |              0.8512 |                    0 |                           276.11  |                               273.904 |                                    274.067 |                    1.0468 |                271.629 |                -0.9816 |                     -0.6725 |                0.9729 |                     0.5244 |                        -5.5128 |                     -5.519  |         0.1222 |
| 2025-12-29 |                 0.0405 |                       1 |         2.47632e+09 |          6.66791e+07 |                      4.11195e+09 |          2.18213e+07 |   0.4593 |                      0 |               0.0756 |            -4.7955 |                 2736.93 |                 794.005 |                -1.915e+08   |                            -1.50253e+08 |                      8.4461 |                              175.251 |            0.5442 |                 26.2841 |                   0.0461 |              0.0642 |                   0.2857 |              1.00912e+10 |    6.49227e+09 |                   1 |            0.8723 |             0.7174 |                             2.45749e+09 |                             2.40827e+09 |                        2.4526e+09  |                        2.47632e+09 |                                   1 |                                    0 |            48.1203 |      -48.4089 |              35.7143 |                57.1429 |           -21.4286 |                  -30.5671 |                -0.1563 |                            -0.1782 |       1.7719e+06  |               57.3149 |                        0.0006 |                                    0.0036 |                                 -0.003  |                      0.169  |                        -0.0817 |                                    -0.0126 |                                  -0.0691 |                       0.1103 |                     20.0593 |                     10.4382 |                      12.4518 |                      17.3861 |                       20.7398 |                       8.7965 |                            26.5057 |                     -21.8633 |                   36.4164 |                    270.612 |              276.183 |                   265.068 |                   250.519 |         51.5911 |         49.5995 |      0.169  |             0.9895 |          -0.8205 |                   49.9666 |             40.0245 |             37.7306 |                1.4003 |                            5.217  |             0.5323 |                  0.7015 |  -0.4662 |              -2.0654 |                   0.2951 |                 0.9316 |                 1.0955 |                 0.2129 |                -1.7901 |          -0.0149 |    -4.1157 |            54.4742 |             0.2186 |                       0.4134 |            0.0118 |                        0.2104 |         -0.0496 |            -0.8195 |                    -1.1484 |                        -0.6882 | 53.5816 | 42.714  | 75.3166 |                         -0.1913 |                     -6.4822 |                                  1.194  |                 -7.5042 |                   -8.7594 |                   1.2553 |               0.0103 |    -19.6328 |                -21.7468 |                 -1.5792 |        5.5886 |                    5885.13 | 53.9827 |                  49.0098 |                  34.5775 |                 19.7029 |       57.1631 |   49.2247 | -0.0088 |  110.988  |  114.995  |                  -0.1531 |              58.3333 |                     -1.0766 |               1 |                0 |           1 |                       -0.7244 |                0.0103 |                  0.854  |                       273.546 |                            273.268 |                                    272.416 | 0.0003 |                     272.918 |                         272.591 |                     271.326 |                                    271.012 |                                       271.765 |                                  272.824 |                                 273.082 |                                    272.429 |                                   272.145 |                                  272.877 |                          276.31  |                               272.011 |                                 273.315 |            271.984 |                                  270.911 |                                   272.462 |                              270.03  |                           273.441 |                           266.62  |                                          272.668 |                                 273.386 |    273.921 |          272.6   |         272.341 |        272.406 |         272.541 |                272.608 |                                273.16  |         275.741 |               275.206 |   266.023 |       272.926 |                    273.939 |                 271.438 |                       272.6   |                       271.048 |                284.195 |                 275.729 |                267.264 |         0.3276 |                0.0614 |       2.003  |               4.2884 |      23.8779 |      268.465 |                            1 |                273.905 |                 279.736 |                 281.304 |                  273.268 |                 265.233 |                  279.177 |                   272.6   |                  266.023 |                          0.0157 |              3.9562 |              -0.1596 |                     55.4689 |                   286.405 |                    275.729 |                   265.055 |                  282.851 |                 270.041 |                     279.204 |                      272.345 |                     265.486 |            276.279 |             271.941 |            267.602 | 263.457 |                      1 |           3.6472 |               0.5082 |                       1.5559 |            -7.4802 |         1 |                         18.9903 |                        23.5748 |            -1.6754 |               4.2075 |         0.3999 |              0.9309 |                    0 |                           275.772 |                               273.85  |                                    274.062 |                    1.7167 |                272.038 |                -0.9626 |                     -0.4628 |                0.3714 |                    -0.3939 |                        -5.5043 |                     -5.5128 |         0.203  |
| 2025-12-30 |                -0.0195 |                      -1 |         2.45418e+09 |          6.66241e+07 |                      4.10949e+09 |          1.83379e+07 |   1.5877 |                      0 |               0.0249 |            -5.2836 |                 2730.14 |                 794.005 |                -2.06929e+08 |                            -1.58349e+08 |                      8.1019 |                              174.255 |            0.506  |                 25.8195 |                   0.0467 |              0.06   |                   0.1863 |              1.0091e+10  |    6.04588e+09 |                   4 |            0.8069 |             0.6714 |                             2.45616e+09 |                             2.41534e+09 |                        2.45418e+09 |                        2.47632e+09 |                                   1 |                                    0 |            43.4593 |      -53.5607 |              28.5714 |                50      |           -21.4286 |                  -35.5284 |                -0.1288 |                            -0.1608 | -464807           |               54.1042 |                        0.0003 |                                    0.003  |                                 -0.0027 |                      0.0788 |                        -0.1122 |                                    -0.0325 |                                  -0.0797 |                      -2.3582 |                     19.2762 |                      9.6926 |                      11.6321 |                      16.8441 |                       20.2146 |                       9.095  |                            25.712  |                     -21.7389 |                   38.6752 |                    270.612 |              276.183 |                   265.068 |                   250.519 |         46.4393 |         48.9647 |      0.0788 |             0.8074 |          -0.7285 |                   48.4209 |             29.5551 |             34.7338 |                0.6843 |                            4.0838 |             0.15   |                  0.4444 |  -0.3773 |              -1.9448 |                   0.3866 |                 0.9145 |                 1.1096 |                 0.0857 |                -1.708  |          -0.0148 |    -4.0858 |            53.5704 |             0.2174 |                       0.4141 |           -0.0182 |                        0.1612 |         -0.0465 |            -0.4022 |                    -0.8195 |                        -0.6065 | 57.9069 | 47.7783 | 78.1641 |                          0.0877 |                     -6.3714 |                                 -0.3191 |                 -7.7102 |                   -8.4097 |                   0.6995 |               0.0051 |    -20.2725 |                -20.6589 |                 -0.7486 |       -3.2998 |                    5881.83 | 53.9827 |                  48.8135 |                  50.5959 |                  3.8001 |       36.7617 |   50.4639 | -0.0122 |  113.905  |  105.452  |                  -0.2379 |              58.3333 |                     -1.0873 |               0 |                1 |           1 |                       -0.6718 |                0.0069 |                  0.7814 |                       273.254 |                            273.117 |                                    272.247 | 0.0002 |                     272.531 |                         272.403 |                     271.798 |                                    271.015 |                                       271.736 |                                  272.774 |                                 272.681 |                                    272.315 |                                   271.738 |                                  272.849 |                          275.78  |                               272.173 |                                 273.113 |            271.995 |                                  270.932 |                                   272.442 |                              269.554 |                           272.853 |                           266.256 |                                          272.648 |                                 273.181 |    273.921 |          272.6   |         272.115 |        272.232 |         272.198 |                272.182 |                                272.911 |         274.769 |               274.771 |   266.023 |       272.541 |                    273.676 |                 271.673 |                       272.6   |                       271.048 |                283.299 |                 275.23  |                267.162 |         0.308  |                0.0586 |       1.7937 |               4.1102 |      23.5003 |      268.465 |                            1 |                274.284 |                 279.357 |                 280.707 |                  273.117 |                 265.526 |                  279.177 |                   272.6   |                  266.023 |                          0.0151 |              3.863  |              -0.3267 |                     54.0398 |                   285.385 |                    275.23  |                   265.399 |                  279.001 |                 269.818 |                     278.457 |                      272.336 |                     266.215 |            276.381 |             272.212 |            268.043 | 263.457 |                      1 |           4.2652 |               0.0698 |                       1.4266 |            -7.2914 |         0 |                         19.3292 |                        29.9642 |            -1.2127 |               1.7906 |         0.4995 |              0.9658 |                    1 |                           275.284 |                               272.991 |                                    273.794 |                    2.1545 |                272.316 |                -0.9522 |                     -0.423  |               -0.6187 |                    -0.993  |                        -5.4973 |                     -5.5043 |         0.2628 |
| 2025-12-31 |                -0.0707 |                      -1 |         2.42688e+09 |          6.65022e+07 |                      4.08531e+09 |          7.5513e+06  | nan      |                      0 |              -0.0357 |            -5.2468 |                 2730.14 |                 790.458 |                -2.31239e+08 |                            -1.68762e+08 |                      7.0467 |                              172.441 |            0.6417 |                 25.8501 |                  -0.005  |              0.0314 |                   0.0688 |              1.00847e+10 |    7.42004e+09 |                   3 |            0.7332 |             0.659  |                             2.44445e+09 |                             2.41711e+09 |                        2.42688e+09 |                        2.45418e+09 |                                   0 |                                    1 |            38.2003 |      -62.8029 |              21.4286 |                42.8571 |           -21.4286 |                  -56.9136 |                -0.0887 |                            -0.1381 |      -4.82705e+06 |               46.4079 |                       -0.0003 |                                    0.0023 |                                 -0.0026 |                     -0.0897 |                        -0.1258 |                                    -0.0512 |                                  -0.0746 |                      -1.5169 |                     18.7176 |                      9.0003 |                      11.3294 |                      16.2589 |                       20.4663 |                      11.4565 |                            24.6539 |                     -37.4456 |                   34.0262 |                    270.248 |              276.821 |                   265.6   |                   250.867 |         37.1971 |         45.0758 |     -0.0897 |             0.628  |          -0.7176 |                   45.6902 |             12.0094 |             27.1964 |               -0.6702 |                            2.8953 |            -0.6218 |                  0.057  |  -0.536  |              -1.6049 |                   0.515  |                 0.9113 |                 1.1148 |                -0.0091 |                -1.9324 |          -0.0248 |    -6.896  |            52.5944 |             0.3745 |                       0.3956 |           -0.0452 |                        0.1157 |         -0.0431 |            -0.1073 |                    -0.4022 |                        -0.6548 | 57.905  | 51.1539 | 71.4071 |                          0.1423 |                     -7.1079 |                                 -1.6769 |                -10.1732 |                   -8.9975 |                  -1.1757 |               0.0026 |    -23.361  |                -20.8876 |                 -0.6816 |      -19.3794 |                    5862.45 | 53.9827 |                  47.7724 |                  43.3308 |                 -9.9432 |       24.882  |   52.0466 | -0.0166 |   99.0847 |   92.3301 |                  -0.3998 |              50      |                     -1.4421 |               0 |                1 |          -1 |                       -0.6071 |                0.0023 |                  0.6255 |                       272.762 |                            272.823 |                                    271.815 | 0.0001 |                     272.2   |                         272.091 |                     271.883 |                                    270.627 |                                       271.745 |                                  272.642 |                                 272.319 |                                    271.777 |                                   271.608 |                                  272.686 |                          275.262 |                               272.102 |                                 272.746 |            271.917 |                                  270.932 |                                   272.383 |                              268.893 |                           272.144 |                           265.643 |                                          272.568 |                                 272.8   |    273.672 |          272.6   |         271.641 |        271.768 |         271.484 |                271.342 |                                272.594 |         273.895 |               274.318 |   266.023 |       272.198 |                    273.062 |                 271.268 |                       272.6   |                       271.048 |                281.366 |                 274.516 |                267.666 |         0.2372 |                0.0499 |       1.9233 |               3.954  |      23.1557 |      268.465 |                            1 |                274.628 |                 279.013 |                 280.039 |                  272.823 |                 265.607 |                  279.177 |                   272.6   |                  266.023 |                          0.0146 |              3.7647 |              -0.3494 |                     52.7331 |                   284.415 |                    274.516 |                   265.137 |                  275.232 |                 269.631 |                     277.662 |                      272.143 |                     266.623 |            276.421 |             272.402 |            268.383 | 263.457 |                      1 |           2.6706 |               0.5281 |                       1.3485 |            -6.9011 |         1 |                         19.6066 |                        33.1912 |            -0.9892 |               3.5114 |         0.5474 |              0.9788 |                    1 |                           274.885 |                               272.887 |                                    273.772 |                    2.3417 |                272.229 |                -0.9772 |                     -0.5599 |               -0.7431 |                    -0.0523 |                        -5.4957 |                     -5.4973 |         0.3273 |

---

## get_factor_analysis
Factor analysis (predictive power) of the technical indicators: whether the tickers that score high on an indicator go on to return more than those that score low.

Per period, the information coefficient (IC) is the Spearman rank correlation between the indicator of the tickers at the end of the period and their return over the following horizon: 1 means the indicator ranks the later returns perfectly, -1 in reverse and 0 that it says nothing about them. The IC measures skill in Grinold and Kahn's fundamental law of active management, $$\text{IR} \approx \text{IC} \times \sqrt{\text{breadth}}$$: a small but consistent IC across many tickers and periods gives a high information ratio.

The summary has a row per indicator and horizon with the mean IC, its standard deviation, the IC information ratio (mean divided by standard deviation), the t-statistic of the mean with its p-value, the skewness and excess kurtosis of the IC, the share of periods with a positive IC, the number of periods, the top minus bottom spread (the mean forward return of the highest quantile minus that of the lowest), the annualized alpha and the beta of the factor-weighted long-short portfolio against the equally weighted tickers, the mean turnover of the top and bottom quantiles and the mean rank autocorrelation of the indicator from one period to the next. With detail, it returns one part of the analysis per period, quantile or group for a single indicator.

The formula is as follows:

$$
\operatorname{IC}(t) = \text{Spearman rank correlation of} \;f(i,\; t) \;\text{and} \;R(i,\; t,\; t + h) \;\text{over the tickers}\; i,\;\; \text{with } f \text{ the factor and } R \text{ the forward return over the horizon } h
$$

- Demeaned return: R(i, t) − mean R(j, t) over the tickers j (of the group of i)

$$
\text{Portfolio weight:}\;\; w(i,\; t) = \frac{f(i,\; t) - \text{mean} \;f(t)}{\Sigma_{j} \left|f(j,\; t) - \text{mean} \;f(t)\right|}
$$

$$
\text{Portfolio return:}\;\; R_{F}(t) = \Sigma_{i} w(i,\; t) \cdot R(i,\; t,\; t + h)
$$

$$
\text{Alpha and beta:}\;\; R_{F}(t) = \alpha + \beta \cdot R_{U}(t) + \epsilon(t),\;\; \text{with}\;\; R_{U}(t) = \text{mean} \;R(i,\; t,\; t + h)
$$

$$
\text{Annualized Alpha} = (1 + \alpha)^{\frac{\text{periods per year}}{h}} - 1
$$

$$
\text{Per period:}\;\; (1 + \text{mean return})^{\frac{1}{h}} - \frac{1 \;\text{and standard error}}{\sqrt{h}}
$$

$$
\text{Standard error of a quantile} = \text{standard deviation over the periods} \;/ \sqrt{\text{periods}}
$$

The indicators are calculated daily and the value on the last trading day of each period is compared with the returns from that day's close onwards, using the dividend and split adjusted close. An indicator in price units does not compare across tickers with different share prices, so a price line (a moving average, band, channel, stop or cloud line, and the Butterworth and Gaussian filters of the Swiss Army Knife) is used as the distance of the close from it, close / line - 1, and a price difference as a share of the close: the true range, the ATR and average day range, the price distance, the market thermometer, the squeeze momentum, the MACD, the momentum (absolute rate of change), the Qstick, the awesome and accelerator oscillators, the elder ray, the detrended price oscillator, the force index, the Hilbert phasor components, the high-pass and band-pass filters of the Swiss Army Knife and the detrended synthetic price. The collections evaluate every variant of an indicator with variants, such as each method of `get_moving_average`, labelled with the method name and its parameters. Each ticker keeps its own history: a ticker without a value or a return in a period is left out of that period only.

**References:**

- library | Referenced against alphalens' [factor_information_coefficient](https://github.com/stefan-jansen/alphalens-reloaded/blob/v0.4.4/src/alphalens/performance.py#L28){:target="_blank"}
- library | Referenced against alphalens' [mean_information_coefficient](https://github.com/stefan-jansen/alphalens-reloaded/blob/v0.4.4/src/alphalens/performance.py#L80){:target="_blank"}
- library | Referenced against alphalens' [mean_return_by_quantile](https://github.com/stefan-jansen/alphalens-reloaded/blob/v0.4.4/src/alphalens/performance.py#L461){:target="_blank"}
- library | Referenced against alphalens' [factor_weights](https://github.com/stefan-jansen/alphalens-reloaded/blob/v0.4.4/src/alphalens/performance.py#L131){:target="_blank"}
- library | Referenced against alphalens' [factor_returns](https://github.com/stefan-jansen/alphalens-reloaded/blob/v0.4.4/src/alphalens/performance.py#L210){:target="_blank"}
- library | Referenced against alphalens' [factor_alpha_beta](https://github.com/stefan-jansen/alphalens-reloaded/blob/v0.4.4/src/alphalens/performance.py#L265){:target="_blank"}
- library | Referenced against alphalens' [quantile_turnover](https://github.com/stefan-jansen/alphalens-reloaded/blob/v0.4.4/src/alphalens/performance.py#L575){:target="_blank"}
- library | Referenced against alphalens' [factor_rank_autocorrelation](https://github.com/stefan-jansen/alphalens-reloaded/blob/v0.4.4/src/alphalens/performance.py#L620){:target="_blank"}
- library | Shares similar logic as alphalens' [average_cumulative_return_by_quantile](https://github.com/stefan-jansen/alphalens-reloaded/blob/v0.4.4/src/alphalens/performance.py#L758){:target="_blank"}

**Args:**

- <u>metrics (str &#124; list[str], optional):</u> An indicator method name, e.g.
"get_relative_strength_index", a variant of one by its label, the method with
its parameters as keyword arguments, e.g. "get_relative_strength_index(method='connors')"
or "get_moving_average(method='hull', window=10)", a list of them, or a collection: "momentum",
"overlap", "volatility", "breadth", "cycle" or "all". Defaults to "momentum",
the oscillators and momentum indicators. The collections leave out the market-wide
breadth measures, the volume-scaled indicators, the pivot points and
Fibonacci levels and the Hilbert dominant cycle phase and trend mode.
- <u>period (str, optional):</u> The frequency at which the indicators are evaluated. Options are:
"daily" (daily prices), "weekly" (weekly prices), "monthly" (monthly prices),
"quarterly" (quarterly prices), "yearly" (yearly prices). Defaults to "monthly".
- <u>horizons (list[int] &#124; int &#124; None, optional):</u> The number of periods the forward
returns cover. Defaults to None, which uses about a period, a quarter and a
year ahead (1, 3 and 12 months for monthly).
- <u>quantiles (int, optional):</u> The number of quantiles the tickers are sorted into per
period. Defaults to 5.
- <u>periods_apart (int, optional):</u> The number of periods between the dates the
quantile turnover and the rank autocorrelation compare. Defaults to 1.
- <u>detail (str &#124; None, optional):</u> Returns one part of the analysis of a single indicator instead of the
summary. Options are: "information_coefficient" (the IC per period and horizon),
"information_coefficient_by_month" (the mean IC per calendar month),
"information_coefficient_by_year" (the mean IC per calendar year),
"group_information_coefficient" (the IC statistics within each group, needs group),
"quantile_returns" (the mean forward return per quantile and horizon),
"quantile_returns_by_date" (the mean forward return per quantile and horizon, per period),
"quantile_return_statistics" (the mean forward return, its standard error and both per single
period), "quantile_statistics" (the range, mean and count of the factor values in each
quantile), "quantile_turnover" (the turnover per period and quantile),
"rank_autocorrelation" (the rank autocorrelation per period), "factor_weights" (the weights of
the factor-weighted long-short portfolio per period and ticker), "factor_returns" (its return
per period and horizon), "cumulative_returns" (the growth of 1 in it and in each quantile),
"event_returns" (the mean price path of each quantile from the longest horizon before to the
longest horizon after the periods it is formed). Defaults to None.
- <u>column (str &#124; None, optional):</u> The output to use of an indicator with several,
e.g. "Signal Line" of the MACD or "Upper Band" of the Bollinger Bands.
Defaults to None, which uses the first output in alphabetical order other
than a price, a histogram or a signal line, e.g. "MACD Line" or "Lower Band".
- <u>group (str &#124; dict &#124; None, optional):</u> The group of each ticker for the group options:
"sector" or "industry" (or another company profile item) from the company profiles
of Financial Modeling Prep, or a dictionary of tickers and their groups. Defaults to
None.
- <u>demeaned (bool, optional):</u> Whether to compare the forward returns with the mean of
the tickers in each period, or with group with the mean of the ticker's group:
a group-neutral analysis, in which the IC is group-adjusted and the
factor-weighted portfolio neutral within each group. Without group the IC
stays the same, as subtracting one mean from every ticker keeps their ranks.
Defaults to False.
- <u>binning (str, optional):</u> How the tickers are sorted into quantiles per period. Options are:
"quantile" (equally sized), "equal_width" (bins of equal width between the lowest and highest
value), "zero_aware" (half of the quantiles for the negative and half for the zero and positive
values, for a signal centred on zero; needs an even number of quantiles), "group" (equally sized
within each group, needs group). Defaults to "quantile".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
**kwargs: Parameters passed to the indicators that take them, e.g. window=14,
close_column="Close" or method="connors" for a single indicator. A variant in a
collection keeps its own method.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The summary per indicator and horizon, or with detail that part of
the analysis of the indicator.

**Notes:**

- The IC is reported as measured: an overbought RSI that goes on to underperform
gives a negative IC. Read the sign as the direction of the relationship.
- The cross-section is the tickers of the Toolkit, so use at least ten and
preferably twenty or more for a meaningful rank correlation and quantiles.
- A horizon longer than one period makes consecutive returns overlap, which
inflates the t-statistic; judge those horizons by their mean IC and IC
information ratio.
- The groups from the company profiles are today's sector or industry, applied
to every period.
- The factor-weighted portfolio is long-short: its weights sum to zero and their
absolute values to one. A horizon longer than one period makes its returns
overlap too, so its alpha and beta are averages rather than tests.
- The cumulative returns split the capital over as many portfolios as the horizon
has periods, started on consecutive periods and each rebalanced once per
horizon; a value shows when its holding period ends, so the series starts at 1.
- The IC is that of Grinold, R.C. and Kahn, R.N. (2000). "Active Portfolio
Management." 2nd ed. McGraw-Hill; the factor-weighted portfolio, the demeaned
and group-neutral returns that of Qian, E., Hua, R. and Sorensen, E. (2007).
"Quantitative Equity Portfolio Management." Chapman & Hall/CRC; the alpha that
of Jensen, M.C. (1968). "The Performance of Mutual Funds in the Period
1945-1964." Journal of Finance 23(2); the event returns follow MacKinlay, A.C.
(1997). "Event Studies in Economics and Finance." Journal of Economic Literature
35(1).
- Unlike alphalens, the top minus bottom spread is twice alphalens' (a gross
exposure of two rather than one), each horizon uses its own returns where alphalens
drops a period and ticker without every horizon's return, and the event returns are
the price paths rebased to the period itself where alphalens averages the
single-period returns at each offset.

Also known as: predictive power, information coefficient, factor testing, alpha signal

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "JPM", "JNJ",
     "XOM", "PG", "KO", "WMT", "V", "UNH", "HD", "CVX"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2016-01-01",
    end_date="2025-12-31",
)

# The 200-day rate of change and the distance of the close from its 200-day average.
toolkit.technicals.get_factor_analysis(
    ["get_rate_of_change", "get_moving_average"], horizons=[1, 12], window=200
)
```

Which returns:

|                                     |   Mean IC |   IC Standard Deviation |   IC Information Ratio |   t-Statistic |   P-Value |   IC Skewness |   IC Kurtosis |   Positive Share |   Observations |   Top Minus Bottom |   Annualized Alpha |    Beta |   Quantile Turnover |   Rank Autocorrelation |
|:------------------------------------|----------:|------------------------:|-----------------------:|--------------:|----------:|--------------:|--------------:|-----------------:|---------------:|-------------------:|-------------------:|--------:|--------------------:|-----------------------:|
| ('get_rate_of_change', '1 Month')   |    0.0468 |                  0.3467 |                 0.1349 |        1.4713 |    0.1439 |       -0.3812 |       -0.3944 |           0.5798 |            119 |             0.0091 |             0.1115 |  0.0444 |              0.2637 |                 0.8582 |
| ('get_rate_of_change', '12 Months') |    0.1184 |                  0.3988 |                 0.2968 |        3.0848 |    0.0026 |       -0.4661 |       -0.3225 |           0.6389 |            108 |             0.079  |            -0.0334 |  0.6091 |              0.2637 |                 0.8582 |
| ('get_moving_average', '1 Month')   |    0.0382 |                  0.346  |                 0.1104 |        1.204  |    0.231  |       -0.2546 |       -0.7156 |           0.563  |            119 |             0.0125 |             0.1154 | -0.0278 |              0.3074 |                 0.8036 |
| ('get_moving_average', '12 Months') |    0.102  |                  0.3847 |                 0.2651 |        2.7545 |    0.0069 |       -0.3393 |       -0.5643 |           0.5833 |            108 |             0.0853 |            -0.0393 |  0.5512 |              0.3074 |                 0.8036 |

---

## collect_breadth_indicators
Collect the breadth and volume indicators of every ticker in one table: how much volume and how many tickers take part in the moves of the prices.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The name of the column containing the close prices.
Defaults to "Adj Close".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: Breadth indicators calculated based on the specified parameters.

**Notes:**

- The method calculates various breadth indicators for each asset in the Toolkit instance.
- When growth is requested, the method calculates the growth of the indicator values
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.collect_breadth_indicators().xs("AAPL", level=1, axis="columns")
```

Which returns:

| Date       |   McClellan Oscillator |   Advancers - Decliners |   On-Balance Volume |   Price Volume Trend |   Accumulation/Distribution Line |   Chaikin Oscillator |     TRIN |   New Highs - New Lows |   Chaikin Money Flow |   Ease of Movement |   Negative Volume Index |   Positive Volume Index |   Klinger Volume Oscillator |   Klinger Volume Oscillator Signal Line |   Market Facilitation Index |   Williams Accumulation/Distribution |   Relative Volume |   Volume Flow Indicator |   Finite Volume Elements |   Twiggs Money Flow |   Volume Zone Oscillator |   Cumulative Force Index |   Price Volume |   Price Volume Rank |   Buying Pressure |   Selling Pressure |   Archer On-Balance Volume Fast Average |   Archer On-Balance Volume Slow Average |   Archer On-Balance Volume Minimum |   Archer On-Balance Volume Maximum |   Archer On-Balance Volume Long Run |   Archer On-Balance Volume Short Run |
|:-----------|-----------------------:|------------------------:|--------------------:|---------------------:|---------------------------------:|---------------------:|---------:|-----------------------:|---------------------:|-------------------:|------------------------:|------------------------:|----------------------------:|----------------------------------------:|----------------------------:|-------------------------------------:|------------------:|------------------------:|-------------------------:|--------------------:|-------------------------:|-------------------------:|---------------:|--------------------:|------------------:|-------------------:|----------------------------------------:|----------------------------------------:|-----------------------------------:|-----------------------------------:|------------------------------------:|-------------------------------------:|
| 2025-12-17 |                -0.0981 |                      -1 |         2.26688e+09 |          6.59406e+07 |                      3.99771e+09 |         -1.74849e+07 | nan      |                      0 |              -0.0358 |            -4.7166 |                 2735.54 |                 788.839 |                -2.03391e+08 |                            -4.28732e+07 |                      8.9837 |                              165.337 |            1.171  |                 25.8886 |                  -0.0337 |             -0.0429 |                  -0.194  |              1.01185e+10 |    1.36297e+10 |                   3 |            0.7602 |             0.9939 |                             2.29242e+09 |                             2.31813e+09 |                        2.26688e+09 |                        2.31702e+09 |                                   0 |                                    1 |
| 2025-12-18 |                -0.0378 |                       1 |         2.31851e+09 |          6.60071e+07 |                      4.02708e+09 |         -1.16789e+07 | nan      |                      0 |               0.0024 |            -7.4093 |                 2735.54 |                 789.854 |                -2.50907e+08 |                            -7.25923e+07 |                     12.8931 |                              170.559 |            1.1996 |                 25.9203 |                   0.0135 |             -0.0099 |                  -0.0055 |              1.0083e+10  |    1.40534e+10 |                   1 |            0.9191 |             0.961  |                             2.30286e+09 |                             2.31819e+09 |                        2.26688e+09 |                        2.31851e+09 |                                   0 |                                    1 |
| 2025-12-19 |                 0.0139 |                       1 |         2.46314e+09 |          6.67935e+07 |                      4.11448e+09 |          1.95656e+07 | nan      |                      0 |               0.1361 |            -9.4903 |                 2735.54 |                 794.149 |                -1.89072e+08 |                            -8.92323e+07 |                      3.2384 |                              174.316 |            3.3172 |                 27.1858 |                   0.149  |              0.0742 |                   0.3343 |              1.00928e+10 |    3.95814e+10 |                   1 |            1.2421 |             0.9738 |                             2.36697e+09 |                             2.34049e+09 |                        2.31851e+09 |                        2.46314e+09 |                                   1 |                                    0 |
| 2025-12-22 |                -0.0419 |                      -1 |         2.42657e+09 |          6.64327e+07 |                      4.08789e+09 |          2.21089e+07 | nan      |                      0 |               0.079  |           -12.8266 |                 2708.55 |                 794.149 |                -1.99306e+08 |                            -1.04957e+08 |                      9.1827 |                              171.416 |            0.7534 |                 27.6286 |                   0.1149 |              0.0461 |                   0.2145 |              1.00829e+10 |    9.90986e+09 |                   4 |            1.1372 |             0.9639 |                             2.39081e+09 |                             2.35373e+09 |                        2.42657e+09 |                        2.46314e+09 |                                   1 |                                    0 |
| 2025-12-23 |                 0.0106 |                       1 |         2.45621e+09 |          6.65848e+07 |                      4.11471e+09 |          2.96727e+07 | nan      |                      0 |               0.0651 |           -14.4653 |                 2722.44 |                 794.149 |                -2.24884e+08 |                            -1.22089e+08 |                      9.8839 |                              174.206 |            0.6251 |                 27.8548 |                   0.1894 |              0.071  |                   0.2753 |              1.00822e+10 |    8.07329e+09 |                   2 |            1.0956 |             0.8755 |                             2.41697e+09 |                             2.3695e+09  |                        2.42657e+09 |                        2.45621e+09 |                                   1 |                                    0 |
| 2025-12-24 |                 0.0554 |                       1 |         2.47412e+09 |          6.66801e+07 |                      4.11466e+09 |          3.00518e+07 | nan      |                      0 |               0.0846 |            -6.6454 |                 2736.94 |                 794.149 |                -2.1628e+08  |                            -1.35545e+08 |                     17.9713 |                              175.81  |            0.3926 |                 27.2474 |                   0.156  |              0.0697 |                   0.3125 |              1.00864e+10 |    4.9041e+09  |                   2 |            1.0156 |             0.8174 |                             2.43983e+09 |                             2.38559e+09 |                        2.45621e+09 |                        2.47412e+09 |                                   1 |                                    0 |
| 2025-12-26 |                -0.0066 |                      -1 |         2.4526e+09  |          6.66479e+07 |                      4.10239e+09 |          2.35736e+07 | nan      |                      0 |               0.0857 |            -5.4395 |                 2736.94 |                 792.96  |                -1.90374e+08 |                            -1.43378e+08 |                     11.6221 |                              173.847 |            0.4872 |                 26.5611 |                   0.0943 |              0.0554 |                   0.2254 |              1.00882e+10 |    5.88406e+09 |                   3 |            0.9294 |             0.7778 |                             2.44494e+09 |                             2.3959e+09  |                        2.4526e+09  |                        2.47412e+09 |                                   1 |                                    0 |
| 2025-12-29 |                 0.0405 |                       1 |         2.47632e+09 |          6.66791e+07 |                      4.11195e+09 |          2.18213e+07 |   0.4593 |                      0 |               0.0756 |            -4.7954 |                 2736.94 |                 794.004 |                -1.915e+08   |                            -1.50253e+08 |                      8.4461 |                              175.252 |            0.5442 |                 26.2841 |                   0.0461 |              0.0642 |                   0.2857 |              1.00912e+10 |    6.49227e+09 |                   1 |            0.8723 |             0.7174 |                             2.45749e+09 |                             2.40827e+09 |                        2.4526e+09  |                        2.47632e+09 |                                   1 |                                    0 |
| 2025-12-30 |                -0.0195 |                      -1 |         2.45418e+09 |          6.66241e+07 |                      4.10949e+09 |          1.83379e+07 |   1.5877 |                      0 |               0.0249 |            -5.2835 |                 2730.14 |                 794.004 |                -2.06929e+08 |                            -1.58349e+08 |                      8.1019 |                              174.256 |            0.506  |                 25.8195 |                   0.0467 |              0.06   |                   0.1863 |              1.0091e+10  |    6.04588e+09 |                   4 |            0.8069 |             0.6714 |                             2.45616e+09 |                             2.41534e+09 |                        2.45418e+09 |                        2.47632e+09 |                                   1 |                                    0 |
| 2025-12-31 |                -0.0707 |                      -1 |         2.42688e+09 |          6.65022e+07 |                      4.08531e+09 |          7.5513e+06  | nan      |                      0 |              -0.0357 |            -5.2467 |                 2730.14 |                 790.457 |                -2.31239e+08 |                            -1.68762e+08 |                      7.0467 |                              172.442 |            0.6417 |                 25.8501 |                  -0.005  |              0.0314 |                   0.0688 |              1.00847e+10 |    7.42004e+09 |                   3 |            0.7332 |             0.659  |                             2.44445e+09 |                             2.41711e+09 |                        2.42688e+09 |                        2.45418e+09 |                                   0 |                                    1 |

---

## get_mcclellan_oscillator
Calculate the McClellan Oscillator: the momentum of the market's breadth, as the difference between a fast and a slow average of the advancing minus declining tickers.

The McClellan Oscillator is the difference between a short-term and a long-term exponential moving average of the daily advance/decline signal. Traditionally it is calculated from the number of advancing minus declining stocks across a market; here it is applied to each ticker's own signal (+1 on a day it closed higher, -1 on a day it closed lower, 0 otherwise), so it measures how persistently that ticker has been rising or falling.

The formula is as follows:

$$
\text{McClellan Oscillator} = \operatorname{EMA}(\text{Advance/Decline} \;\text{Signal},\; \text{short\_ema\_window}) - \operatorname{EMA}(\text{Advance/Decline} \;\text{Signal},\; \text{long\_ema\_window})
$$

**Also known as:** McClellan oscillator, market breadth.

**References:**

- paper | McClellan, S. and McClellan, M. (1970). "Patterns for Profit: The McClellan Oscillator and Summation Index." Trade Levels Inc.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The name of the column containing the close prices.
Defaults to "Adj Close".
- <u>short_ema_window (int, optional):</u> The window size for the short-term EMA.
Defaults to 19.
- <u>long_ema_window (int, optional):</u> The window size for the long-term EMA.
Defaults to 39.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: McClellan Oscillator values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the McClellan Oscillator for each asset in the Toolkit instance.
- When growth is requested, the method calculates the growth of the indicator values
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["EWJ", "EWG", "EWU", "EWQ", "EWZ", "INDA", "FXI", "EWC", "EWA", "EWY"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_mcclellan_oscillator().loc[:, ["EWJ", "EWG", "EWZ", "INDA", "FXI", "Benchmark"]].tail(5)
```

Which returns:

| Date       |     EWJ |    EWG |     EWZ |    INDA |    FXI |   Benchmark |
|:-----------|--------:|-------:|--------:|--------:|-------:|------------:|
| 2025-12-24 | -0.0357 | 0.1365 | -0.0693 |  0.0631 | 0.0419 |      0.0718 |
| 2025-12-26 | -0.0875 | 0.1604 | -0.0203 | -0.002  | 0.0863 |      0.0008 |
| 2025-12-29 | -0.0314 | 0.0801 | -0.0783 | -0.0576 | 0.0239 |     -0.06   |
| 2025-12-30 | -0.0832 | 0.1111 | -0.0275 | -0.0049 | 0.0703 |     -0.1116 |
| 2025-12-31 | -0.1272 | 0.037  | -0.0839 |  0.0402 | 0.0097 |     -0.1552 |

---

## get_advancers_decliners
Calculate the advance/decline signal: whether each ticker closed higher (1) or lower (-1) than the period before, the building block of the market breadth measures.

Traditionally advancers versus decliners is a market-wide count of rising against falling stocks; applied to a single ticker it becomes a directional signal: +1 on a day the ticker closed higher than the day before, -1 on a day it closed lower and 0 on an unchanged day. It feeds the McClellan Oscillator; get_trin and get_new_highs_new_lows measure breadth across all tickers.

The formula is as follows:

$$
\text{Signal} = + 1 \;\text{if Close}(t) > \operatorname{Close}(t-1),\;\; - 1 \;\text{if Close}(t) < \operatorname{Close}(t-1),\;\; \text{else 0}
$$

**Also known as:** advance decline ratio, market breadth.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The name of the column containing the close prices.
Defaults to "Adj Close".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: Advance/decline signal values (+1, 0 or -1).

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the advance/decline signal for each asset in the Toolkit instance.
- When growth is requested, the method calculates the growth of the indicator values
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["EWJ", "EWG", "EWU", "EWQ", "EWZ", "INDA", "FXI", "EWC", "EWA", "EWY"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_advancers_decliners().loc[:, ["EWJ", "EWG", "EWZ", "INDA", "FXI", "Benchmark"]].tail(5)
```

Which returns:

| Date       |   EWJ |   EWG |   EWZ |   INDA |   FXI |   Benchmark |
|:-----------|------:|------:|------:|-------:|------:|------------:|
| 2025-12-24 |    -1 |     1 |    -1 |     -1 |     1 |           1 |
| 2025-12-26 |    -1 |     1 |     1 |     -1 |     1 |          -1 |
| 2025-12-29 |     1 |    -1 |    -1 |     -1 |    -1 |          -1 |
| 2025-12-30 |    -1 |     1 |     1 |      1 |     1 |          -1 |
| 2025-12-31 |    -1 |    -1 |    -1 |      1 |    -1 |          -1 |

---

## get_on_balance_volume
Calculate the On-Balance Volume (OBV): a running total of volume that adds the volume of up periods and subtracts that of down periods, to show whether volume flows into or out of a security.

The On-Balance Volume (OBV) is a technical indicator that uses volume flow to predict changes in stock price. It accumulates the volume on up days and subtracts the volume on down days. The resulting OBV line provides insights into the buying and selling pressure behind price movements.

The formula is as follows:

$$
\text{OBV} = \text{Previous OBV} + \text{Volume if Close} > \text{Previous Close, Previous OBV} - \text{Volume if Close} < \text{Previous Close},\;\; \text{and Previous OBV otherwise}
$$

The level of OBV has no meaning by itself, since it depends on the first date of the data; only its direction and its divergences from price matter. A rising OBV while price moves sideways is read as accumulation ahead of a breakout, a falling OBV as distribution. A single day of very high volume, such as an index rebalance or an earnings day, can move the line for a long time.

**Also known as:** OBV, volume momentum.

**References:**

- paper | Granville, J.E. (1963). "Granville's New Key to Stock Market Profits." Prentice-Hall.
- library | Referenced against TA-Lib's [OBV](https://ta-lib.org/functions/obv.html){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the OBV.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: On-Balance Volume values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates On-Balance Volume
for each asset in the Toolkit instance.
- TA-Lib's OBV starts its running total at the first period's volume instead of 0, so it is
the On-Balance Volume here plus that volume; every change is equal.
- When growth is requested, the method calculates the growth of the OBV over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["BTCUSD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_on_balance_volume().tail(5)
```

Which returns:

| Date       |       BTCUSD |     Benchmark |
|:-----------|-------------:|--------------:|
| 2025-12-27 | -1.15162e+12 | nan           |
| 2025-12-28 | -1.13646e+12 | nan           |
| 2025-12-29 | -1.18487e+12 |   1.32079e+09 |
| 2025-12-30 | -1.14929e+12 |   1.27363e+09 |
| 2025-12-31 | -1.18312e+12 |   1.19948e+09 |

---

## get_price_volume_trend
Calculate the Price Volume Trend (PVT): a running total of volume weighted by the percentage change of the close, which shows how strongly buying or selling pressure backs a trend.

The Price Volume Trend is a running total of volume weighted by the period's percentage change in price. On-Balance Volume adds or subtracts the whole volume depending on the direction of the close; the PVT adds only the share of the volume that matches the size of the move, so a small change in price moves the line only a little.

The formula is as follows:

$$
\text{PVT} = \text{Previous PVT} + \frac{\text{Volume} \cdot (\text{Close} - \text{Previous Close})}{\text{Previous Close}}
$$

$$
\text{PVT} = 0 \;\text{on the first date},\;\; \text{which has no previous close}
$$

The level of the PVT has no meaning by itself, since it starts at 0 on the start date; only its direction and its divergences from price matter. A rising PVT confirms an uptrend carried by volume, and a PVT that fails to follow price to a new high warns that the move lacks participation. The line is in shares, so it cannot be compared across stocks.

**Also known as:** PVT, Price and Volume Trend, Volume Price Trend.

See `breadth_model.get_price_volume_trend` for the references.

**References:**

- paper | Granville, J.E. (1963). "Granville's New Key to Stock Market Profits." Prentice-Hall, the On-Balance Volume the PVT refines.
- library | Referenced against TA-Lib's [PVT](https://ta-lib.org/functions/pvt.html){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", so that the change in price is the return including dividends.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the PVT.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: Price Volume Trend values, in shares.

**Notes:**

- The running total starts at 0 on each ticker's first date with a close and a volume on or
after the start date of the Toolkit, as in TA-Lib's PVT, which it equals.
- When growth is requested, the method calculates the growth of the PVT over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_price_volume_trend().tail(5)
```

Which returns:

| Date       |        AAPL |        MSFT |    Benchmark |
|:-----------|------------:|------------:|-------------:|
| 2025-12-24 | 6.67008e+07 | 2.02096e+07 | -9.46523e+06 |
| 2025-12-26 | 6.66686e+07 | 2.02039e+07 | -9.46945e+06 |
| 2025-12-29 | 6.66998e+07 | 2.01903e+07 | -9.69239e+06 |
| 2025-12-30 | 6.66449e+07 | 2.02012e+07 | -9.74998e+06 |
| 2025-12-31 | 6.65229e+07 | 2.00776e+07 | -1.02993e+07 |

---

## get_accumulation_distribution_line
Calculate the Accumulation/Distribution Line: a running total of volume weighted by where each close lies within its high-low range, to show whether a security is being accumulated or distributed.

The Accumulation/Distribution Line is a technical indicator that evaluates the flow of money into or out of an asset. It takes into account both price and volume information to identify whether an asset is being accumulated (bought) or distributed (sold) by investors.

The formula is as follows:

$$
\text{Money Flow Multiplier} = \frac{(\text{Close} - \text{Low}) - (\text{High} - \text{Close})}{\text{High} - \text{Low}}
$$

$$
\text{Money Flow Volume} = \text{Money Flow Multiplier} \cdot \text{Volume}
$$

$$
\text{ADL} = \text{Previous ADL} + \text{Money Flow Volume}
$$

**Also known as:** ADL, Chaikin ADL, volume-price trend.

**References:**

- paper | Chaikin, M., who published no formal paper on it; the standard textbook treatment is Murphy, J.J. (1999). "Technical Analysis of the Financial Markets." New York Institute of Finance.
- library | Referenced against TA-Lib's [AD](https://ta-lib.org/functions/ad.html){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the open, high and low prices are adjusted
for dividends in the same way.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Accumulation/Distribution Line.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: Accumulation/Distribution Line values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates the
Accumulation/Distribution Line for each asset in the Toolkit instance.
- The Accumulation/Distribution Line agrees with TA-Lib's AD.
- When growth is requested, the method calculates the growth of the Accumulation/Distribution Line
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["GLD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_accumulation_distribution_line().tail(5)
```

Which returns:

| Date       |         GLD |   Benchmark |
|:-----------|------------:|------------:|
| 2025-12-24 | 7.95203e+08 | 8.01111e+09 |
| 2025-12-26 | 7.95996e+08 | 8.00572e+09 |
| 2025-12-29 | 7.9136e+08  | 8.01431e+09 |
| 2025-12-30 | 7.82463e+08 | 7.98763e+09 |
| 2025-12-31 | 7.75502e+08 | 7.919e+09   |

---

## get_chaikin_oscillator
Calculate the Chaikin Oscillator: the momentum of the Accumulation/Distribution Line, as the difference between its fast and slow exponential moving averages.

The Chaikin Oscillator is a momentum-based indicator that combines price and volume to help identify potential trends and reversals in the market. It is calculated as the difference between the 3-day and 10-day Accumulation/Distribution Line.

The formula is as follows:

$$
\text{Chaikin Oscillator} = \operatorname{EMA}(\text{short-window ADL}) - \operatorname{EMA}(\text{long-window ADL})
$$

**Also known as:** Chaikin oscillator, volume accumulation.

**References:**

- paper | Chaikin, M., who published no formal paper on it; the standard textbook treatment is Murphy, J.J. (1999). "Technical Analysis of the Financial Markets." New York Institute of Finance.
- library | Referenced against TA-Lib's [ADOSC](https://ta-lib.org/functions/adosc.html){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the open, high and low prices are adjusted
for dividends in the same way.
- <u>short_window (int, optional):</u> Number of periods for the short-term moving average.
Defaults to 3.
- <u>long_window (int, optional):</u> Number of periods for the long-term moving average.
Defaults to 10.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Chaikin Oscillator.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: Chaikin Oscillator values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates the
Chaikin Oscillator for each asset in the Toolkit instance.
- Both EMAs are seeded with the simple average of their first values, as on StockCharts,
while TA-Lib's ADOSC starts them from the first Accumulation/Distribution value, so the
first values differ from TA-Lib's until the two converge (within 0.01% after about 65
periods with the default windows).
- When growth is requested, the method calculates the growth of the Chaikin Oscillator
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["QQQ"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_chaikin_oscillator().tail(5)
```

Which returns:

| Date       |          QQQ |   Benchmark |
|:-----------|-------------:|------------:|
| 2025-12-24 |  1.33735e+07 | 4.48979e+07 |
| 2025-12-26 |  1.24876e+07 | 4.67752e+07 |
| 2025-12-29 |  1.15765e+07 | 4.60255e+07 |
| 2025-12-30 |  1.62538e+06 | 3.30466e+07 |
| 2025-12-31 | -1.44174e+07 | 2.89497e+06 |

---

## get_chaikin_money_flow
Calculate the Chaikin Money Flow (CMF) or Colin Twiggs' Money Flow (TMF): the share of volume over a window that came with closes near the highs rather than the lows, a measure of buying versus selling pressure.

The Chaikin Money Flow sums the same Money Flow Volume used by the Accumulation/ Distribution Line over a rolling window and normalizes it by the window's total volume, turning the running (unbounded) Accumulation/Distribution Line into a bounded oscillator. Sustained readings above zero indicate buying pressure (accumulation) is dominating over the window, while sustained readings below zero indicate selling pressure (distribution).

Twiggs Money Flow refines the Chaikin Money Flow. It places the close within the true range (which includes a gap from the previous close) instead of the high-low range, so a gap does not show up as a close at the top or bottom of a narrow range, and it smooths the money flow volume and the volume with Wilder's moving average instead of summing them over a window, so a large volume does not distort the result when it leaves the window. Twiggs used crossings of zero and divergences from price as signals.

The formula is as follows, per method:

$$
\text{Chaikin Money Flow:}\;\; \text{Money Flow Multiplier} = \frac{(\text{Close} - \text{Low}) - (\text{High} - \text{Close})}{\text{High} - \text{Low}},\;\; \text{Money Flow Volume} = \text{Money Flow Multiplier} \cdot \text{Volume}\;\;\text{and}\;\; \text{CMF} = \frac{\operatorname{Sum}(\text{Money Flow Volume},\; \text{window})}{\operatorname{Sum}(\text{Volume},\; \text{window})}
$$

$$
\text{Twiggs Money Flow:}\;\; \text{True High} = \max(\text{High},\; \operatorname{Close}(t-1)),\;\; \text{True Low} = \min(\text{Low},\; \operatorname{Close}(t-1)),\;\; \text{Money Flow Volume} = \frac{\text{Volume} \cdot ((\text{Close} - \text{True Low}) - (\text{True High} - \text{Close}))}{\text{True High} - \text{True Low}}\;\;\text{and}\;\; \text{TMF} = \frac{\text{Wilder MA}(\text{Money Flow Volume},\; \text{window})}{\text{Wilder MA}(\text{Volume},\; \text{window})}
$$

**Also known as:** CMF, Chaikin Money Flow, TMF, Twiggs Money Flow.

**References:**

- paper | Twiggs, C. (2003). "Twiggs Money Flow." Incredible Charts ([https://www.incrediblecharts.com/indicators/twiggs_money_flow.php](https://www.incrediblecharts.com/indicators/twiggs_money_flow.php){:target="_blank"}).
- library | Referenced against TA-Lib's [CMF](https://ta-lib.org/functions/cmf.html){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the open, high and low prices are adjusted
for dividends in the same way.
- <u>window (int &#124; None, optional):</u> Number of periods to sum the Money Flow Volume and
volume over, or of Wilder's moving average with method="twiggs". Defaults to None,
which uses 20 for "standard" and 21 for "twiggs".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Chaikin Money Flow.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>method (str, optional):</u> The variant. Options are: "standard" (the Chaikin Money Flow),
"twiggs" (Twiggs Money Flow). Defaults to "standard".
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: Chaikin Money Flow (or Twiggs Money Flow) values, bounded
between -1 and 1.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the Chaikin Money Flow for each asset in the Toolkit instance.
- There is no formal journal citation for the Chaikin Money Flow; the standard
textbook treatment is Murphy, J.J. (1999). "Technical Analysis of the Financial
Markets." New York Institute of Finance.
- The Chaikin Money Flow agrees with TA-Lib's CMF.
- Twiggs Money Flow: TA-Lib, pandas-ta-classic, ta and Tulip Indicators do not have it, and finta's
TMF is an unfinished stub, so it follows Twiggs' definition. Wilder's moving average starts
from the simple average of its first `window` values, and the first period, without a
previous close, uses its own high-low range.
- When growth is requested, the method calculates the growth of the Chaikin Money
Flow over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["ETHUSD", "SOLUSD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_chaikin_money_flow().tail(5)
```

Which returns:

| Date       |   ETHUSD |   SOLUSD |   Benchmark |
|:-----------|---------:|---------:|------------:|
| 2025-12-27 |  -0.0938 |  -0.143  |    nan      |
| 2025-12-28 |  -0.1006 |  -0.0945 |    nan      |
| 2025-12-29 |  -0.1815 |  -0.1419 |      0.0671 |
| 2025-12-30 |  -0.1279 |  -0.0749 |      0.0614 |
| 2025-12-31 |  -0.1646 |  -0.1521 |      0.017  |

---

## get_ease_of_movement
Calculate the Ease of Movement (EMV): how far the price moves per unit of volume, so a large value shows a price rising or falling on little volume.

The Ease of Movement indicator relates how far price moved (the change in the midpoint of the high-low range from one period to the next) to the volume required to move it (via the "Box Ratio", volume scaled down and divided by the period's high-low range). High positive readings mean price is moving up easily on relatively little volume; high negative readings mean price is moving down easily on relatively little volume. The raw daily reading is smoothed with a Simple Moving Average to reduce noise.

The formula is as follows:

$$
\text{Distance Moved} = \frac{\operatorname{High}(t) + \operatorname{Low}(t)}{2} - \frac{\operatorname{High}(t-1) + \operatorname{Low}(t-1)}{2}
$$

$$
\text{Box Ratio} = \frac{\frac{\text{Volume}}{\text{volume\_divisor}}}{\text{High} - \text{Low}}
$$

$$
\text{Raw EMV} = \frac{\text{Distance Moved}}{\text{Box Ratio}}
$$

$$
\text{EMV} = \operatorname{SMA}(\text{Raw EMV},\; \text{window})
$$

**Also known as:** EMV, Ease of Movement.

**References:**

- library | Referenced against TA-Lib's [EMV](https://ta-lib.org/functions/emv.html){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int, optional):</u> Number of periods used to smooth the raw Ease of
Movement values with a Simple Moving Average. Defaults to 14.
- <u>volume_divisor (float, optional):</u> Scaling constant applied to volume so that the
Box Ratio (and therefore EMV) stays in a readable range regardless of an
asset's typical share volume. Defaults to 100,000,000.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Ease of Movement.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: Ease of Movement values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the Ease of Movement for each asset in the Toolkit instance.
- Reference: Arms, R.W. (1989). "The Arms - <u>Index (TRIN):</u> An Introduction to the
Volume Analysis of Stock and Bond Markets." Dow Jones-Irwin.
- The Ease of Movement agrees with TA-Lib's EMV with its `volumedivisor` set to `volume_divisor`
(TA-Lib's default is 10,000).
- When growth is requested, the method calculates the growth of the Ease of
Movement over the given lag.


**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["^GSPC"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_ease_of_movement().tail(5)
```

Which returns:

| Date       |   ^GSPC |   Benchmark |
|:-----------|--------:|------------:|
| 2025-12-24 |  1.404  |      2.8161 |
| 2025-12-26 |  0.6053 |      2.227  |
| 2025-12-29 |  0.6173 |      2.7602 |
| 2025-12-30 |  0.6371 |      2.7794 |
| 2025-12-31 | -4.2755 |      0.4354 |

---

## get_volume_index
Calculate the Negative or the Positive Volume Index (NVI or PVI), which separates the trades of informed investors from those of the crowd.

It is a running total of the price changes on the periods volume falls (NVI) or rises (PVI).

The Negative Volume Index is a cumulative index that only updates on days where volume decreases from the prior period, compounding that day's percentage price change onto the running index; on days where volume increases (or stays flat), the index is carried forward unchanged. The premise, per Fosback, is that "smart money" tends to be active on low-volume (quiet) days, so tracking price behaviour specifically on those days isolates informed trading from the noise of high-volume, crowd-driven days. The Positive Volume Index mirrors it: it only updates on days where volume increases from the prior period, and is carried forward unchanged on days where volume decreases (or stays flat). Per Fosback, it isolates price behaviour on high-volume (crowd-driven) days, which is traditionally read as tracking less-informed, sentiment-driven trading.

The formula is as follows, per method:

$$
\text{Negative Volume Index:}\;\; \operatorname{Index}(t) = \operatorname{Index}(t-1) \cdot \left(1 + \left(\frac{\operatorname{Close}(t)}{\operatorname{Close}(t-1)} - 1\right)\right) \;\text{if Volume}(t) < \operatorname{Volume}(t-1),\;\; \text{and}\;\; \operatorname{Index}(t) = \operatorname{Index}(t-1) \;\text{otherwise}
$$

$$
\text{Positive Volume Index:}\;\; \operatorname{Index}(t) = \operatorname{Index}(t-1) \cdot \left(1 + \left(\frac{\operatorname{Close}(t)}{\operatorname{Close}(t-1)} - 1\right)\right) \;\text{if Volume}(t) > \operatorname{Volume}(t-1),\;\; \text{and}\;\; \operatorname{Index}(t) = \operatorname{Index}(t-1) \;\text{otherwise}
$$

**Also known as:** NVI, Negative Volume Index, PVI, Positive Volume Index, volume index.

**References:**

- paper | Fosback, N.G. (1976). "Stock Market Logic: A Sophisticated Approach to Profits on Wall Street." The Institute for Econometric Research.
- library | Referenced against TA-Lib's [NVI](https://ta-lib.org/functions/nvi.html){:target="_blank"}
- library | Referenced against TA-Lib's [PVI](https://ta-lib.org/functions/pvi.html){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>start_value (float, optional):</u> The index value to start the series at.
Defaults to 1000.0.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the volume index.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>method (str, optional):</u> The index. Options are: "negative" (the Negative Volume Index),
"positive" (the Positive Volume Index). Defaults to "negative".
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: Negative (or Positive) Volume Index values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the volume index for each asset in the Toolkit instance.
- With the default `start_value` of 1,000, the Negative Volume Index agrees with TA-Lib's NVI
and the Positive Volume Index with TA-Lib's PVI.
- When growth is requested, the method calculates the growth of the volume index over
the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["SPY", "IWM"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
    benchmark_ticker=None,
)

toolkit.technicals.get_volume_index().tail(5)
```

Which returns:

| Date       |     SPY |     IWM |
|:-----------|--------:|--------:|
| 2025-12-24 | 5440.48 | 4501.78 |
| 2025-12-26 | 5440.48 | 4501.78 |
| 2025-12-29 | 5440.48 | 4501.78 |
| 2025-12-30 | 5433.84 | 4468.59 |
| 2025-12-31 | 5433.84 | 4468.59 |

---

## get_trin
Calculate the TRIN (Arms Index): the ratio of advancing to declining tickers divided by the ratio of their volumes, which shows whether volume favours the rising or the falling tickers.

TRIN compares the ratio of advancing to declining issues against the ratio of volume in advancing issues to volume in declining issues. It is a market-wide breadth reading computed across all tickers in the Toolkit instance (excluding the synthetic "Portfolio" and "Benchmark" columns), and the resulting single reading is broadcast to every ticker column so it lines up with the other breadth indicators.

The formula is as follows:

$$
\text{TRIN} = \frac{\frac{\text{Advancing Issues}}{\text{Declining Issues}}}{\frac{\text{Advancing Volume}}{\text{Declining Volume}}}
$$

A TRIN below 1 means the volume in rising stocks outweighs their number, which is read as buying pressure, and above 1 as selling pressure; readings far above 2 tend to come with capitulation days. It is meant for a broad universe, such as all stocks of an exchange. Calculated across a handful of tickers it jumps between extremes and is undefined on days when none of them fell.

A ticker counts on the dates it traded, with its change since its own previous close: on a date only a cryptocurrency in the Toolkit traded, such as a weekend, only the cryptocurrency counts, and a stock is never counted as unchanged on it.

**Also known as:** Arms Index, TRIN.

**References:**

- paper | Arms, R.W. (1967), who introduced the index in Barron's as the Short-Term Trading Index.
- paper | Arms, R.W. (1989). "The Arms Index (TRIN): An Introduction to the Volume Analysis of Stock and Bond Markets." Dow Jones-Irwin.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The name of the column containing the close prices.
Defaults to "Adj Close".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: TRIN values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the TRIN across all tickers in the Toolkit instance.
- When growth is requested, the method calculates the growth of the indicator values
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["XLK", "XLF", "XLE", "XLV", "XLY", "XLP", "XLI", "XLB", "XLU", "XLRE", "XLC"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

# TRIN is one market-wide reading, repeated in every ticker column
toolkit.technicals.get_trin().loc[:, ["XLK"]].tail(5)
```

Which returns:

| Date       |      XLK |
|:-----------|---------:|
| 2025-12-24 |   2.485  |
| 2025-12-26 |   1.6498 |
| 2025-12-29 |   0.6578 |
| 2025-12-30 |   0.6376 |
| 2025-12-31 | nan      |

---

## get_new_highs_new_lows
Calculate the New Highs - New Lows: the number of tickers at a new high over a window minus the number at a new low, which shows how broad a rise or a fall is.

New Highs - New Lows measures the number of tickers reaching a new high over the specified window minus the number of tickers reaching a new low over the same window. It is a market-wide breadth reading computed across all tickers in the Toolkit instance (excluding the synthetic "Portfolio" and "Benchmark" columns), and the resulting single reading is broadcast to every ticker column so it lines up with the other breadth indicators.

The formula is as follows:

$$
\text{New Highs} - \text{New Lows} = (\text{Number of tickers at a window-period high}) - (\text{Number of tickers at a window-period low})
$$

The reading counts tickers at a high or low of the lookback window, so it needs a broad universe and a history of at least one window before the start of the period of interest: the reading is NaN until a ticker has a full window of closes. The default window of 252 periods is a year of daily closes; weekly data needs a shorter window, such as 52 periods for a year. Persistently more new lows than new highs while an index still rises is a classic sign of narrowing breadth.

Each ticker's window counts its own closes and the ticker counts on the dates it traded, so the weekends of a cryptocurrency in the Toolkit do not shorten a stock's window.

**Also known as:** new highs minus new lows, record high percent.

**References:**

- paper | Colby, R.W. (2003). "The Encyclopedia of Technical Market Indicators." 2nd ed. McGraw-Hill.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The name of the column containing the close prices.
Defaults to "Adj Close".
- <u>window (int, optional):</u> Number of periods for the new high / new low lookback.
Defaults to 252, a year of daily closes (52 is a year of weekly closes).
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: New Highs - New Lows values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the New Highs - New Lows across all tickers in the Toolkit instance.
- When growth is requested, the method calculates the growth of the indicator values
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["XLK", "XLF", "XLE", "XLV", "XLY", "XLP", "XLI", "XLB", "XLU", "XLRE", "XLC"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2024-10-01",
    end_date="2025-12-31",
)

# New Highs - New Lows is one market-wide reading, repeated in every ticker column
toolkit.technicals.get_new_highs_new_lows(window=20).loc[:, ["XLK"]].tail(5)
```

Which returns:

| Date       |   XLK |
|:-----------|------:|
| 2025-12-24 |     5 |
| 2025-12-26 |     1 |
| 2025-12-29 |     0 |
| 2025-12-30 |     2 |
| 2025-12-31 |     0 |

---

## get_klinger_volume_oscillator
Calculate the Klinger Volume Oscillator (KVO): the difference between a fast and a slow average of the volume force, which compares the volume of up and down trends to show long-term money flow.

The Klinger Volume Oscillator turns each period's volume into a signed "volume force": positive when the sum of the high, low and close rose from the period before (an up trend), negative when it fell, and weighted by how the period's range compares with the range accumulated since the trend last turned. The oscillator is the difference between a short and a long exponential moving average of that force, with a signal line to show when it turns.

The formula is as follows:

$$
\text{Trend} = + 1 \;\text{if High} + \text{Low} + \text{Close} > \text{the previous High} + \text{Low} + \text{Close},\;\; \text{-1 if lower, else the previous Trend}
$$

$$
\,\mathrm{d}m = \text{High} - \text{Low}
$$

$$
\text{cm} = \operatorname{cm}(t-1) + \,\mathrm{d}m \;\text{if the Trend is unchanged},\;\; \text{else}\;\; \operatorname{dm}(t-1) + \,\mathrm{d}m
$$

$$
\text{Volume Force} = \text{Volume} \cdot \left|\frac{2 \cdot \,\mathrm{d}m}{\text{cm}} - 1\right| \cdot \text{Trend} \cdot 100
$$

$$
\text{KVO} = \operatorname{EMA}(\text{Volume Force},\; \text{short\_window}) - \operatorname{EMA}(\text{Volume Force},\; \text{long\_window})
$$

$$
\text{Signal Line} = \operatorname{EMA}(\text{KVO},\; \text{signal\_window})
$$

Klinger designed it to follow the long-term flow of money while staying sensitive to short-term reversals: the KVO crossing its signal line, or diverging from price at a new high or low, is the usual signal. Its level is in units of volume and depends on how many shares trade, so it is not comparable across tickers.

**Also known as:** KVO, Klinger Oscillator, Klinger Volume Force.

**References:**

- paper | Klinger, S.J. (1997). "Identifying Trends With Volume Analysis." Technical Analysis of Stocks & Commodities, 15(12).
- library | Referenced against TA-Lib's [KVO](https://ta-lib.org/functions/kvo.html){:target="_blank"}
- library | Referenced against Tulip Indicators' [kvo](https://tulipindicators.org/kvo){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the open, high and low prices are adjusted
for dividends in the same way.
- <u>short_window (int, optional):</u> The number of periods for the short-term EMA of the volume force.
Defaults to 34.
- <u>long_window (int, optional):</u> The number of periods for the long-term EMA of the volume force.
Defaults to 55.
- <u>signal_window (int, optional):</u> The number of periods for the signal line. Defaults to 13.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: The Klinger Volume Oscillator and its Signal Line, in units of volume.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates the KVO for
each asset in the Toolkit instance.
- The volume force agrees with that of TA-Lib (and Tulip Indicators). Every EMA is seeded with the simple average
of its first values, so the KVO starts on the 56th period, as TA-Lib's, and the signal line 12
periods later. TA-Lib seeds the averages with the first volume force instead; on daily data of
AAPL and MSFT the two agree to 1% of the typical KVO after about 210 periods and to 0.0001% after
about 470. pandas-ta-classic's `kvo` uses a simplified force (the volume signed by the change in
the typical price) and differs.
- When growth is requested, the method calculates the growth of the indicator values
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_klinger_volume_oscillator().xs("AAPL", level=1, axis="columns").tail(5)
```

Which returns:

| Date       |   Klinger Volume Oscillator |   Signal Line |
|:-----------|----------------------------:|--------------:|
| 2025-12-24 |                -2.16282e+08 |  -1.35548e+08 |
| 2025-12-26 |                -1.90376e+08 |  -1.43381e+08 |
| 2025-12-29 |                -1.91502e+08 |  -1.50255e+08 |
| 2025-12-30 |                -2.06931e+08 |  -1.58352e+08 |
| 2025-12-31 |                -2.31241e+08 |  -1.68765e+08 |

---

## get_market_facilitation_index
Calculate Bill Williams' Market Facilitation Index (BW MFI): the range of a period per unit of volume, which shows how efficiently volume moves the price.

The Market Facilitation Index measures how far price moved per unit of volume: the period's range divided by its volume. Williams read it together with the change in volume: a rising index on rising volume ("green") shows a market that moves easily with new participants, a falling index on falling volume ("fade") a market that loses interest, a falling index on rising volume ("squat") a struggle between buyers and sellers that often comes before a breakout, and a rising index on falling volume ("fake") a move without participation.

The formula is as follows:

$$
\text{Market Facilitation Index} = \frac{\text{High} - \text{Low}}{\frac{\text{Volume}}{\text{volume\_divisor}}}
$$

The index depends on the price and the number of shares traded, so it is read against its own history rather than compared across tickers.

**Also known as:** BW MFI, Market Facilitation Index, MARKETFI.

**References:**

- paper | Williams, B.M. (1995). "Trading Chaos: Applying Expert Techniques to Maximize Your Profits." John Wiley & Sons.
- library | Referenced against TA-Lib's [MARKETFI](https://ta-lib.org/functions/marketfi.html){:target="_blank"}
- library | Referenced against pandas-ta-classic's [marketfi](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/volume/marketfi.py#L16){:target="_blank"}
- library | Referenced against Tulip Indicators' [marketfi](https://tulipindicators.org/marketfi){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the open, high and low prices are adjusted
for dividends in the same way.
- <u>volume_divisor (float, optional):</u> Scaling constant the volume is divided by, so the index stays in
a readable range at the Toolkit's rounding. Defaults to 100,000,000, as for the Ease of Movement.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: Market Facilitation Index values, the range per 100 million shares
traded by default.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates the Market
Facilitation Index for each asset in the Toolkit instance.
- With a volume divisor of 1 it agrees with TA-Lib's MARKETFI, pandas-ta-classic's `marketfi` and Tulip
Indicators' `marketfi`, whose index for a stock trading millions of shares is a fraction of a
millionth. A period without volume has no index (NaN) rather than an infinite one.
- When growth is requested, the method calculates the growth of the indicator values
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_market_facilitation_index().tail(5)
```

Which returns:

| Date       |    AAPL |    MSFT |   Benchmark |
|:-----------|--------:|--------:|------------:|
| 2025-12-24 | 17.9714 | 73.3347 |      7.6219 |
| 2025-12-26 | 11.6221 | 24.2275 |      5.6988 |
| 2025-12-29 |  8.4461 | 37.9654 |      4.9645 |
| 2025-12-30 |  8.102  | 29.7295 |      4.1659 |
| 2025-12-31 |  7.0467 | 30.7675 |      7.5612 |

---

## get_williams_accumulation_distribution
Calculate Larry Williams' Accumulation/Distribution (WAD): a running total of how far each close moved from the opposite end of its true range, which shows accumulation and distribution from prices alone.

Williams' Accumulation/Distribution is a running total of how far each close moved away from the opposite end of the period's true range: on an up close the distance from the true low (accumulation), on a down close the distance from the true high (distribution). Unlike Chaikin's Accumulation/Distribution Line it uses no volume.

The formula is as follows:

$$
\text{True High} = \max(\text{High},\; \operatorname{Close}(t-1)),\;\; \text{True Low} = \min(\text{Low},\; \operatorname{Close}(t-1))
$$

$$
\operatorname{⟦A/D⟧}(t) = \text{Close} - \text{True Low if Close} > \operatorname{Close}(t-1),\;\; \text{Close} - \text{True High if Close} < \operatorname{Close}(t-1),\;\; \text{else 0}
$$

$$
\operatorname{WAD}(t) = \operatorname{WAD}(t-1) + \frac{A}{D(t)},\;\; \text{starting at 0 on the start date}
$$

Williams traded the divergences: price making a new high while the line does not points to distribution, price making a new low while the line holds up to accumulation. The level of the line depends on the start date; only its direction and divergences carry meaning.

**Also known as:** WAD, Williams A/D, Williams Accumulation Distribution.

**References:**

- paper | Williams, L.R. (1973). "How I Made One Million Dollars Last Year Trading Commodities." Windsor Books.
- library | Referenced against TA-Lib's [WAD](https://ta-lib.org/functions/wad.html){:target="_blank"}
- library | Referenced against pandas-ta-classic's [wad](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/volume/wad.py#L13){:target="_blank"}
- library | Referenced against Tulip Indicators' [wad](https://tulipindicators.org/wad){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the open, high and low prices are adjusted
for dividends in the same way.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: Williams' Accumulation/Distribution values, in price units.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates Williams'
Accumulation/Distribution for each asset in the Toolkit instance, as a running total from the
start date.
- It agrees with TA-Lib's WAD (which also starts at 0), Tulip Indicators' `wad` (which starts on the
second period) and pandas-ta-classic's `wad` (NaN on the first period).
- When growth is requested, the method calculates the growth of the indicator values
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_williams_accumulation_distribution().tail(5)
```

Which returns:

| Date       |    AAPL |    MSFT |   Benchmark |
|:-----------|--------:|--------:|------------:|
| 2025-12-24 | 175.81  | 316.48  |     368.326 |
| 2025-12-26 | 173.847 | 316.073 |     366.986 |
| 2025-12-29 | 175.252 | 314.834 |     364.546 |
| 2025-12-30 | 174.256 | 316.797 |     363.007 |
| 2025-12-31 | 172.442 | 312.315 |     357.61  |

---

## get_relative_volume
Calculate the Relative Volume (RVOL): the volume of a period divided by its average over a window, which shows how unusually busy the period is.

Relative Volume compares a period's volume with the average volume of the periods before it. A value of 2 means twice the usual volume: a breakout or a gap on high relative volume carries more conviction than one on thin trading, and traders use it to screen for stocks "in play".

The formula is as follows:

$$
\text{RVOL} = \frac{\operatorname{Volume}(t)}{\operatorname{SMA}(\text{Volume},\; \text{window}) (t-1)}
$$

The average covers the `window` periods before the current one, so a spike does not raise its own benchmark. As a ratio it can be compared across tickers whatever the number of shares they trade.

**Also known as:** RVOL, Relative Volume, volume ratio.

**References:**

- paper | Bulkowski, T.N. (2005). "Encyclopedia of Chart Patterns." 2nd ed. John Wiley & Sons.
- library | Referenced against TA-Lib's [RVOL](https://ta-lib.org/functions/rvol.html){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>window (int, optional):</u> The number of earlier periods to average the volume over. Defaults to 20.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: Relative Volume values, as a ratio (1 is the average volume).

**Notes:**

- The method retrieves the volumes of the specified `period` and calculates the Relative Volume for
each asset in the Toolkit instance.
- It agrees with TA-Lib's RVOL. A ticker without volume, such as an index or a currency pair, has no
Relative Volume (NaN).
- When growth is requested, the method calculates the growth of the indicator values
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["NVDA", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_relative_volume().tail(5)
```

Which returns:

| Date       |   NVDA |   TSLA |   Benchmark |
|:-----------|-------:|-------:|------------:|
| 2025-12-24 | 0.353  | 0.5386 |      0.4951 |
| 2025-12-26 | 0.8084 | 0.7825 |      0.5363 |
| 2025-12-29 | 0.7032 | 0.8849 |      0.8223 |
| 2025-12-30 | 0.5726 | 0.7756 |      0.6145 |
| 2025-12-31 | 0.7232 | 0.6418 |      0.975  |

---

## get_volume_flow_indicator
Calculate Markos Katsanos' Volume Flow Indicator (VFI): the volume of the periods with a meaningful move of the typical price, signed by the direction of the move, which shows whether money flows in or out.

The Volume Flow Indicator refines On-Balance Volume in three ways: it uses the typical price instead of the close, it ignores moves too small to matter (below a cutoff that scales with the recent volatility of the typical price) and it caps the volume of a single period at a multiple of the average volume, so one spike cannot dominate. The sum of that signed volume over the window, divided by the average volume, is smoothed with a short EMA.

The formula is as follows:

$$
\text{Typical Price} = \frac{\text{High} + \text{Low} + \text{Close}}{3}
$$

$$
\text{Volatility} = \text{Population Standard Deviation of} \;\ln\left(\frac{\text{Typical Price}}{\text{Typical Price}(t-1)}\right) \;\text{over 30 periods}
$$

$$
\text{Cutoff} = \text{coefficient} \cdot \text{Volatility} \cdot \text{Close}
$$

$$
\text{Average Volume} = \operatorname{SMA}(\text{Volume},\; \text{window}) (t-1)
$$

$$
\text{Capped Volume} = \min(\text{Volume},\; \text{volume\_coefficient} \cdot \text{Average Volume})
$$

$$
\text{Signed Volume} = + \text{Capped Volume if Typical Price} \;\mathord{-} \;\text{Typical Price}(t-1) > \text{Cutoff},\;\; \text{-Capped Volume if it is below -Cutoff, else 0}
$$

$$
\text{VFI} = \operatorname{EMA}\left(\frac{\operatorname{Sum}(\text{Signed Volume},\; \text{window})}{\text{Average Volume}},\; \text{smooth\_window}\right)
$$

Katsanos read a VFI above zero as a bullish flow of money and below zero as a bearish one, a crossing of zero as a change in trend and a divergence from price as an early warning. The VFI is in units of the average volume (a sum of up to `window` periods), so it is comparable across tickers.

**Also known as:** VFI, Volume Flow Indicator.

**References:**

- paper | Katsanos, M. (2004). "Using Money Flow to Stay with the Trend." Technical Analysis of Stocks & Commodities, 22(6).
- paper | Katsanos, M. (2004). "Volume Flow Indicator Performance." Technical Analysis of Stocks & Commodities, 22(7).
- library | Referenced against pandas-ta-classic's [vfi](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/volume/vfi.py#L17){:target="_blank"}
- library | Shares similar logic as finta's [VFI](https://github.com/peerchemist/finta/blob/1.3/finta/finta.py#L2026){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the open, high and low prices are adjusted
for dividends in the same way.
- <u>window (int, optional):</u> The number of periods for the average volume and the sum of signed volume.
Defaults to 130, about six months of trading days.
- <u>coefficient (float, optional):</u> The multiple of the volatility times the close that a move of the
typical price needs to count. Defaults to 0.2.
- <u>volume_coefficient (float, optional):</u> The multiple of the average volume that a single period's
volume is capped at. Defaults to 2.5.
- <u>smooth_window (int, optional):</u> The number of periods for the EMA that smooths the result.
Defaults to 3.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: Volume Flow Indicator values, in units of the average volume.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates the VFI for
each asset in the Toolkit instance. With the default window it needs 261 periods before its first
value, so start a year earlier than the dates of interest.
- The volatility is the population standard deviation (ddof=0), as in Katsanos' MetaStock formula:
it only sets the cutoff of the indicator's definition, so it follows the primary source, as the
Bollinger Bands do. The VFI agrees with pandas-ta-classic's `vfi` exactly. finta uses the sample
deviation (ddof=1), a 1.7% larger cutoff, and differs wherever a move falls between the two
cutoffs.
- When growth is requested, the method calculates the growth of the indicator values
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2020-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_volume_flow_indicator().tail(5)
```

Which returns:

| Date       |    AAPL |    MSFT |   Benchmark |
|:-----------|--------:|--------:|------------:|
| 2025-12-24 | 27.2483 | -5.4611 |     18.9447 |
| 2025-12-26 | 26.5619 | -6.4634 |     19.1226 |
| 2025-12-29 | 26.285  | -7.5029 |     18.3944 |
| 2025-12-30 | 25.8204 | -8.4473 |     17.6238 |
| 2025-12-31 | 25.851  | -9.7919 |     16.2389 |

---

## get_finite_volume_elements
Calculate Markos Katsanos' Finite Volume Elements (FVE): the share of volume over a window classified as buying rather than selling, leaving out moves too small to matter, a measure of money flow.

Finite Volume Elements is a money flow indicator that classifies each period's whole volume as buying, selling or neutral. It looks at both the intraday move (the close against the middle of the range) and the interday move (the change in the typical price), and leaves out periods whose combined move is smaller than a cutoff, so noise does not count as flow. The result is the net signed volume as a share of all volume over the window.

The formula is as follows:

$$
\text{Typical Price} = \frac{\text{High} + \text{Low} + \text{Close}}{3}
$$

$$
\text{Money Flow} = \text{Close} - \frac{\text{High} + \text{Low}}{2} + \text{Typical Price} - \text{Typical Price}(t-1)
$$

$$
\text{Signed Volume} = + \text{Volume if Money Flow} > \text{cutoff} \cdot \text{Close},\;\; - \text{Volume if Money Flow} < - \text{cutoff} \cdot \text{Close},\;\; \text{else 0}
$$

$$
\text{FVE} = \frac{\operatorname{Sum}(\text{Signed Volume},\; \text{window})}{\operatorname{Sum}(\text{Volume},\; \text{window})}
$$

A rising FVE while price moves sideways points to accumulation ahead of a breakout, a falling one to distribution. As a share of volume it lies between -1 and 1 and is comparable across tickers.

**Also known as:** FVE, Finite Volume Elements.

**References:**

- paper | Katsanos, M. (2003). "Detecting Breakouts." Technical Analysis of Stocks & Commodities, 21(4).
- paper | Katsanos, M. (2003). "Detecting Breakouts In Intraday Charts." Technical Analysis of Stocks & Commodities, 21(9).
- library | Referenced against finta's [FVE](https://github.com/peerchemist/finta/blob/1.3/finta/finta.py#L1998){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the open, high and low prices are adjusted
for dividends in the same way.
- <u>window (int, optional):</u> The number of periods to sum the signed and total volume over. Defaults to
22, a month of trading days.
- <u>cutoff (float, optional):</u> The share of the close the money flow needs to exceed to count, as a
decimal. Defaults to 0.003 (0.3%).
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: Finite Volume Elements values, as decimals between -1 and 1.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates the FVE for
each asset in the Toolkit instance.
- It agrees with finta's FVE divided by 100 (Katsanos and finta express it in percent, with the cutoff
in percent as well), from the second value on: finta counts the first period, which has no
change in the typical price, as neutral volume and starts one period earlier.
- When growth is requested, the method calculates the growth of the indicator values
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_finite_volume_elements().tail(5)
```

Which returns:

| Date       |    AAPL |   MSFT |   Benchmark |
|:-----------|--------:|-------:|------------:|
| 2025-12-24 |  0.156  | 0.3175 |      0.1378 |
| 2025-12-26 |  0.0943 | 0.333  |      0.0929 |
| 2025-12-29 |  0.0461 | 0.289  |      0.0072 |
| 2025-12-30 |  0.0467 | 0.244  |     -0.0367 |
| 2025-12-31 | -0.005  | 0.183  |     -0.1106 |

---

## get_volume_zone_oscillator
Calculate the Volume Zone Oscillator (VZO): the volume of up closes minus that of down closes as a share of the total volume, smoothed, which shows whether buying or selling volume dominates.

The Volume Zone Oscillator divides the volume into the volume of up closes and that of down closes and expresses their difference, smoothed with an exponential moving average, as a share of the smoothed total volume.

The formula is as follows:

$$
\text{Signed Volume} = \operatorname{sign}(\text{Close} - \operatorname{Close}(t-1)) \cdot \text{Volume}
$$

$$
\text{VZO} = \frac{\operatorname{EMA}(\text{Signed Volume},\; \text{window})}{\operatorname{EMA}(\text{Volume},\; \text{window})}
$$

Khalil and Steckler read it in zones: above 0.05 the trend is bullish and above 0.40 overbought (0.60 extremely), below -0.05 bearish and below -0.40 oversold (-0.60 extremely), with crossings of zero and of the 0.40 lines as signals. As a share of volume it is comparable across tickers.

**Also known as:** VZO, Volume Zone Oscillator.

**References:**

- paper | Khalil, W. and Steckler, D. (2011). "In The Volume Zone." Technical Analysis of Stocks & Commodities, 29(5).
- library | Referenced against finta's [VZO](https://github.com/peerchemist/finta/blob/1.3/finta/finta.py#L1521){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int, optional):</u> The number of periods for both EMAs. Defaults to 14.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: Volume Zone Oscillator values, as decimals between -1 and 1.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates the VZO for
each asset in the Toolkit instance.
- The VZO is a decimal; Khalil and Steckler and finta multiply it by 100, so their zones are at 5,
40 and 60. Both EMAs start from the simple average of their first values on the second period
(the first has no change), so the VZO starts on period `window` + 1. finta averages from the
first value and agrees after about 90 periods.
- When growth is requested, the method calculates the growth of the indicator values
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_volume_zone_oscillator().tail(5)
```

Which returns:

| Date       |   AAPL |   MSFT |   Benchmark |
|:-----------|-------:|-------:|------------:|
| 2025-12-24 | 0.3125 | 0.3228 |      0.2742 |
| 2025-12-26 | 0.2254 | 0.2524 |      0.1808 |
| 2025-12-29 | 0.2857 | 0.1642 |      0.0476 |
| 2025-12-30 | 0.1863 | 0.2429 |     -0.046  |
| 2025-12-31 | 0.0688 | 0.1082 |     -0.1791 |

---

## get_price_volume
Calculate the Price-Volume (dollar volume): the close times the volume, the amount of money that traded in each period.

The Price-Volume is the value traded in a period: the close times the volume. Unlike the number of shares, it can be compared across stocks with very different prices and is the usual measure of liquidity for position sizing. Signed, it carries the direction of the close, as a money flow per period.

The formula is as follows:

$$
\text{Price-Volume} = \text{Close} \cdot \text{Volume}
$$

$$
\text{Signed Price-Volume} = \operatorname{sign}(\text{Close} - \operatorname{Close}(t-1)) \cdot \text{Close} \cdot \text{Volume}
$$

**Also known as:** PVOL, dollar volume, traded value.

**References:**

- paper | Amihud, Y. (2002). "Illiquidity and Stock Returns: Cross-Section and Time-Series Effects." Journal of Financial Markets, 5(1), 31-56.
- library | Referenced against pandas-ta-classic's [pvol](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/volume/pvol.py#L17){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Close".
- <u>signed (bool, optional):</u> Whether to sign the value with the direction of the close. Defaults to
False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: Price-Volume values, in the currency of the prices.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates the
Price-Volume for each asset in the Toolkit instance.
- The traded close is the default, as the value traded is a market value; the dividend-adjusted
close would understate the value of older periods.
- It agrees with pandas-ta-classic's `pvol`, also in its signed form.
- When growth is requested, the method calculates the growth of the indicator values
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_price_volume().tail(5)
```

Which returns:

| Date       |        AAPL |        MSFT |   Benchmark |
|:-----------|------------:|------------:|------------:|
| 2025-12-24 | 4.9041e+09  | 2.8578e+09  | 2.72325e+10 |
| 2025-12-26 | 5.88406e+09 | 4.31243e+09 | 2.87261e+10 |
| 2025-12-29 | 6.49228e+09 | 5.30618e+09 | 4.30316e+10 |
| 2025-12-30 | 6.04589e+09 | 6.79767e+09 | 3.23999e+10 |
| 2025-12-31 | 7.42005e+09 | 7.54525e+09 | 5.05608e+10 |

---

## get_price_volume_rank
Calculate the Price Volume Rank (PVR): a code from 1 (a rising price on rising volume) to 4 (a falling price on falling volume), which shows whether volume confirms a move.

The Price Volume Rank classifies each period by the direction of the close and of the volume, from the most bullish to the most bearish combination: a rising price on rising volume (1), a rising price on falling volume (2), a falling price on rising volume (3) and a falling price on falling volume (4). An unchanged close or volume counts as rising.

The formula is as follows:

$$
\text{PVR} = 1 \;\text{if Close} \geq \operatorname{Close}(t-1) \;\text{and Volume} \geq \operatorname{Volume}(t-1)
$$

$$
\text{PVR} = 2 \;\text{if Close} \geq \operatorname{Close}(t-1) \;\text{and Volume} < \operatorname{Volume}(t-1)
$$

$$
\text{PVR} = 3 \;\text{if Close} < \operatorname{Close}(t-1) \;\text{and Volume} \geq \operatorname{Volume}(t-1)
$$

$$
\text{PVR} = 4 \;\text{if Close} < \operatorname{Close}(t-1) \;\text{and Volume} < \operatorname{Volume}(t-1)
$$

A moving average of the rank below 2.5 is read as bullish and above it as bearish.

**Also known as:** PVR, Price Volume Rank.

**References:**

- paper | Fulks Maxwell Laboratories (fmlabs), "Price Volume Rank," Technical Indicators Reference.
- library | Referenced against pandas-ta-classic's [pvr](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/volume/pvr.py#L12){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: Price Volume Rank values (1, 2, 3 or 4).

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates the Price
Volume Rank for each asset in the Toolkit instance.
- It agrees with pandas-ta-classic's `pvr`.
- When growth is requested, the method calculates the growth of the indicator values
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_price_volume_rank().tail(5)
```

Which returns:

| Date       |   AAPL |   MSFT |   Benchmark |
|:-----------|-------:|-------:|------------:|
| 2025-12-24 |      2 |      2 |           2 |
| 2025-12-26 |      3 |      3 |           3 |
| 2025-12-29 |      1 |      3 |           3 |
| 2025-12-30 |      4 |      1 |           4 |
| 2025-12-31 |      3 |      3 |           3 |

---

## get_buying_selling_pressure
Calculate the Buying and Selling Pressure (BASP), which shows whether buyers or sellers control the market.

It compares the distance of the close above the low (buying) and of the high above the close (selling) with their averages, weighted by volume.

The Buying Pressure is the distance of the close above the low, the Selling Pressure the distance of the high above the close. Each is divided by its own exponential moving average, so it shows whether the pressure is larger than usual, and multiplied by the volume relative to its average, so a session with heavy volume weighs more. A short EMA smooths both lines.

The formula is as follows:

$$
\text{Relative Volume} = \frac{\text{Volume}}{\operatorname{EMA}(\text{Volume},\; \text{window})}
$$

$$
\text{Buying Pressure} = \operatorname{EMA}\left(\frac{\text{Close} - \text{Low}}{\operatorname{EMA}(\text{Close} - \text{Low},\; \text{window})} \cdot \text{Relative Volume},\; \text{smooth\_window}\right)
$$

$$
\text{Selling Pressure} = \operatorname{EMA}\left(\frac{\text{High} - \text{Close}}{\operatorname{EMA}(\text{High} - \text{Close},\; \text{window})} \cdot \text{Relative Volume},\; \text{smooth\_window}\right)
$$

Both lines are ratios around 1 (the usual pressure on the usual volume). Buying pressure above selling pressure points to accumulation, and a crossing of the two to a change in who is in control.

**Also known as:** BASP, BASPN, normalized buying and selling pressure.

**References:**

- paper | Williams, L.R. (1985). "The Ultimate Oscillator." Technical Analysis of Stocks & Commodities, 3(4), for a similar buying pressure measured from the lower of the low and the previous close.
- library | Referenced against finta's [BASP](https://github.com/peerchemist/finta/blob/1.3/finta/finta.py#L1671){:target="_blank"}
- library | Referenced against finta's [BASPN](https://github.com/peerchemist/finta/blob/1.3/finta/finta.py#L1691){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the open, high and low prices are adjusted
for dividends in the same way.
- <u>window (int, optional):</u> The number of periods for the averages of the pressure and the volume.
Defaults to 40.
- <u>smooth_window (int, optional):</u> The number of periods for the EMA that smooths both lines.
Defaults to 20; 1 gives the unsmoothed lines.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: The Buying Pressure and Selling Pressure.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates the buying
and selling pressure for each asset in the Toolkit instance.
- finta's BASPN is the default and its BASP a `smooth_window` of 1; finta cites no primary source.
Every EMA starts from the simple average of its first values, while finta's average from the
first value, so the two agree after about 300 periods.
- When growth is requested, the method calculates the growth of the indicator values
over the given lag.
- finta defines the Buying and Selling Pressure without citing a primary source.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_buying_selling_pressure().xs("AAPL", level=1, axis="columns").tail(5)
```

Which returns:

| Date       |   Buying Pressure |   Selling Pressure |
|:-----------|------------------:|-------------------:|
| 2025-12-24 |            1.0156 |             0.8174 |
| 2025-12-26 |            0.9294 |             0.7778 |
| 2025-12-29 |            0.8723 |             0.7174 |
| 2025-12-30 |            0.8069 |             0.6714 |
| 2025-12-31 |            0.7332 |             0.659  |

---

## get_archer_on_balance_volume
Calculate the Archer On-Balance Volume (AOBV): a fast and a slow average of the On-Balance Volume and whether the volume trend is up or down.

The Archer On-Balance Volume adds a fast and a slow exponential moving average of On-Balance Volume and two flags for their trend, so OBV can be read like a moving average crossover system. A "long run" is a period in which the fast average rose over the last `run_window` periods while the slow one moved (a rising OBV trend or a potential bottom); a "short run" one in which the fast average fell (a falling trend or a potential top). The rolling minimum and maximum of OBV mark its recent range.

The formula is as follows:

$$
\text{OBV} = \text{Cumulative Sum}(\operatorname{sign}(\text{Close} - \operatorname{Close}(t-1)) \cdot \text{Volume}),\;\; \text{starting at 0 on the start date}
$$

$$
\text{Fast Average} = \operatorname{EMA}(\text{OBV},\; \text{short\_window}),\;\; \text{Slow Average} = \operatorname{EMA}(\text{OBV},\; \text{long\_window})
$$

$$
\text{Minimum} = \min(\text{OBV},\; \text{extreme\_window}),\;\; \text{Maximum} = \max(\text{OBV},\; \text{extreme\_window})
$$

$$
\text{Long Run} = 1 \;\text{if Fast Average rose over} \;\text{run\_window} \;\text{periods and the Slow Average changed},\;\; \text{else 0}
$$

$$
\text{Short Run} = 1 \;\text{if Fast Average fell over} \;\text{run\_window} \;\text{periods and the Slow Average changed},\;\; \text{else 0}
$$

**Also known as:** AOBV, Archer OBV.

**References:**

- paper | Granville, J.E. (1963). "Granville's New Key to Stock Market Profits." Prentice-Hall.
- library | Referenced against pandas-ta-classic's [aobv](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/volume/aobv.py#L17){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>short_window (int, optional):</u> The number of periods for the fast EMA of OBV. Defaults to 4.
- <u>long_window (int, optional):</u> The number of periods for the slow EMA of OBV. Defaults to 12.
- <u>extreme_window (int, optional):</u> The number of periods for the rolling minimum and maximum of OBV.
Defaults to 2.
- <u>run_window (int, optional):</u> The number of periods over which the averages must rise or fall.
Defaults to 2.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: The On-Balance Volume, its Minimum and Maximum, the Fast and Slow
Average and the Long Run and Short Run flags (1 or 0).

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates the Archer
On-Balance Volume for each asset in the Toolkit instance, as a running total from the start date.
- The indicator comes from a TradingView script by Archer without a published paper. It equals
pandas-ta-classic's `aobv`, except that its On-Balance Volume (as TA-Lib's) starts at the first
period's volume instead of 0: the OBV, its minimum, maximum and averages are that volume higher
there, and the flags are equal.
- When growth is requested, the method calculates the growth of the indicator values
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

archer_obv = toolkit.technicals.get_archer_on_balance_volume(
    show_columns=["On-Balance Volume", "Fast Average", "Slow Average", "Long Run", "Short Run"]
)

archer_obv.xs("AAPL", level=1, axis="columns").tail(5)
```

Which returns:

| Date       |   Fast Average |   Long Run |   On-Balance Volume |   Short Run |   Slow Average |
|:-----------|---------------:|-----------:|--------------------:|------------:|---------------:|
| 2025-12-24 |    2.43811e+09 |          1 |         2.47241e+09 |           0 |    2.38388e+09 |
| 2025-12-26 |    2.44322e+09 |          1 |         2.45088e+09 |           0 |    2.39418e+09 |
| 2025-12-29 |    2.45577e+09 |          1 |         2.4746e+09  |           0 |    2.40656e+09 |
| 2025-12-30 |    2.45445e+09 |          1 |         2.45246e+09 |           0 |    2.41362e+09 |
| 2025-12-31 |    2.44273e+09 |          0 |         2.42517e+09 |           1 |    2.41539e+09 |

---

## get_volume_profile
Calculate the Volume Profile (Volume by Price) between the start and end date: how much volume traded at each price level, which shows the prices the market accepted most.

The Volume Profile is not a series over time but a histogram: it divides the range of the closes between the start and end date into price bins of equal width and adds up the volume traded at a close in each bin, split into the volume of up closes and that of down closes.

The formula is as follows:

$$
\text{Bin edges} = \min(\text{Close}) + \frac{k \cdot (\max(\text{Close}) - \min(\text{Close}))}{\text{bins}},\;\; \text{for}\;\; k = 0 \;\text{to bins}
$$

$$
\text{Up Volume} = \operatorname{Sum}(\text{Volume of the periods with Close} > \operatorname{Close}(t-1) \;\text{and the Close in the bin})
$$

$$
\text{Down Volume} = \operatorname{Sum}(\text{Volume of the periods with Close} < \operatorname{Close}(t-1) \;\text{and the Close in the bin})
$$

$$
\text{Total Volume} = \operatorname{Sum}(\text{Volume of all periods with the Close in the bin})
$$

Bins with a lot of volume are prices at which many positions were opened, which tend to act as support or resistance when price returns to them; the bin with the most volume is the point of control. More up than down volume in a bin suggests the positions opened there were mostly purchases.

**Also known as:** VP, Volume by Price, Volume at Price, Market Profile.

**References:**

- paper | Steidlmayer, J.P. and Koy, K. (1986). "Markets and Market Logic." Porcupine Press.
- paper | StockCharts ChartSchool, "Volume by Price" ([https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-overlays/volume-by-price](https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-overlays/volume-by-price){:target="_blank"}).
- library | Referenced against pandas-ta-classic's [vp](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/volume/vp.py#L13){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>bins (int, optional):</u> The number of price bins of equal width. Defaults to 10.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: A row per price bin (1 for the lowest prices) with the Low Price, High Price,
Up Volume, Down Volume and Total Volume of each ticker.

**Notes:**

- The profile covers the periods between the start and end date of the Toolkit and looks at every
close in them, so it describes that window as a whole and is not meant for a backtest. Each
ticker has its own bins, over the range of its own closes.
- The bins are those of pandas-ta-classic's `vp` sorted by close, whose up and down volume
it equals, with the exact range of the closes as edges and every bin kept, also those without
volume (pandas-ta-classic widens the range by 0.1% and drops empty bins; its default
splits the period into stretches of time instead). Its total is the up plus
the down volume; here the Total Volume also includes the volume of unchanged closes and of the
first period, which has no change.
- A close on an inner edge belongs to the lower bin. A ticker whose close does not change has all
its volume in the first bin, with every edge at that close.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_volume_profile().xs("AAPL", level=1, axis="columns")
```

Which returns:

|   Price Bin |   Down Volume |   High Price |   Low Price |   Total Volume |   Up Volume |
|------------:|--------------:|-------------:|------------:|---------------:|------------:|
|           1 |   2.81326e+08 |      182.632 |     171.236 |    2.81326e+08 | 0           |
|           2 |   3.54266e+08 |      194.028 |     182.632 |    3.54266e+08 | 0           |
|           3 |   1.25692e+09 |      205.424 |     194.028 |    2.79533e+09 | 1.53841e+09 |
|           4 |   9.40298e+08 |      216.82  |     205.424 |    2.32431e+09 | 1.38402e+09 |
|           5 |   8.29389e+08 |      228.216 |     216.82  |    1.59005e+09 | 7.60656e+08 |
|           6 |   1.1089e+09  |      239.612 |     228.216 |    2.11226e+09 | 1.00335e+09 |
|           7 |   3.32909e+08 |      251.008 |     239.612 |    1.00977e+09 | 6.21122e+08 |
|           8 |   3.4874e+08  |      262.404 |     251.008 |    9.81495e+08 | 6.32755e+08 |
|           9 |   7.25819e+08 |      273.8   |     262.404 |    1.47212e+09 | 7.46301e+08 |
|          10 |   2.38447e+08 |      285.196 |     273.8   |    6.23551e+08 | 3.85104e+08 |

---

## get_market_breadth
Calculate the breadth of the market the Toolkit's tickers make up: how many of them take part in a move.

An index can rise on the strength of a few large companies while most of its members fall; breadth shows that divergence, which often comes before the index itself turns. Breadth is most meaningful across many tickers, such as the constituents of an index, which `Discovery.get_index_constituents` lists (e.g. the 500 tickers of the S&P 500). Today's members leave out the companies that were removed from the index since (often after falling behind), so breadth of past dates computed from them is biased towards the survivors, the further back the more; its `date=` gives the members on the first date of the window instead.

Per date it returns:

- Advancers, Decliners and Unchanged: the number of tickers whose close rose, fell or stayed the same, and the Net Advances.
- Advance-Decline Line: the running total of the net advances. A rising index with a falling line is the classic negative divergence.
- Advance-Decline Ratio: the advancers divided by the decliners.
- McClellan Oscillator: the ratio-adjusted version, the 19-period minus the 39-period exponential moving average (smoothing constants of 0.10 and 0.05) of the net advances divided by advancers plus decliners (times 1,000); unchanged issues are left out. Each average starts from the simple average of its first 19 or 39 values, so the oscillator starts once the 39-period average exists (NaN before), as does its running total, the McClellan Summation Index.
- Percentage Above the short and long moving average: the share of tickers trading above their 50 and 200-period average, a gauge of how broad a trend is.
- New Highs and New Lows: the tickers whose close is above the highest (below the lowest) close of the previous `high_low_window` - 1 periods, so the highest or lowest of the last `high_low_window` periods; a close that only equals the previous high is no new high. NaN until at least one ticker has a full window.

The Benchmark (and a Portfolio) are left out. A constituent counts on the dates it traded, and its changes, moving averages and highs and lows run over its own closes: on a date only a cryptocurrency in the Toolkit traded, such as a weekend, only the cryptocurrency counts, and the McClellan averages then skip that date (see `breadth_model.get_market_breadth`).

**Also known as:** market breadth, advance-decline line, McClellan oscillator, percentage above 200-day moving average, new highs new lows.

**References:**

- paper | McClellan, S. and McClellan, M. (1970). "Patterns for Profit: The McClellan Oscillator and Summation Index." Trade Levels Inc.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The name of the column containing the close prices.
Defaults to "Adj Close".
- <u>short_window (int, optional):</u> The short moving average window. Defaults to 50.
- <u>long_window (int, optional):</u> The long moving average window. Defaults to 200.
- <u>high_low_window (int &#124; None, optional):</u> The number of periods, including the current
one, of the new highs and lows. Defaults to None, which uses a year of periods:
252 daily, 52 weekly, 12 monthly, 4 quarterly and 1 yearly (too short for a new
high or low, so those stay NaN), and 252 for intraday data.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the rounding of the Toolkit.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The breadth measures per date.

**As an example:**

```python
from financetoolkit import Discovery, Toolkit

discovery = Discovery(api_key="FINANCIAL_MODELING_PREP_KEY")

constituents = discovery.get_index_constituents("Dow Jones")

toolkit = Toolkit(
    constituents.index.tolist(),
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2024-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_market_breadth().tail()
```

Which returns:

| Date       |   Advancers |   Decliners |   Unchanged |   Net Advances |   Advance-Decline Line |   Advance-Decline Ratio |   McClellan Oscillator |   McClellan Summation Index |   Percentage Above 50-Period Average |   Percentage Above 200-Period Average |   New Highs |   New Lows |
|:-----------|------------:|------------:|------------:|---------------:|-----------------------:|------------------------:|-----------------------:|----------------------------:|-------------------------------------:|--------------------------------------:|------------:|-----------:|
| 2025-12-24 |          26 |           3 |           1 |             23 |                    978 |                  8.6667 |                65.5048 |                    -814.088 |                               0.7333 |                                   0.8 |           3 |          0 |
| 2025-12-26 |          14 |          16 |           0 |             -2 |                    976 |                  0.875  |                49.8424 |                    -764.246 |                               0.7    |                                   0.8 |           1 |          0 |
| 2025-12-29 |          10 |          20 |           0 |            -10 |                    966 |                  0.5    |                22.8684 |                    -741.377 |                               0.7333 |                                   0.8 |           0 |          0 |
| 2025-12-30 |           9 |          21 |           0 |            -12 |                    954 |                  0.4286 |                -3.642  |                    -745.019 |                               0.7    |                                   0.8 |           0 |          0 |
| 2025-12-31 |           3 |          27 |           0 |            -24 |                    930 |                  0.1111 |               -46.2902 |                    -791.309 |                               0.5667 |                                   0.8 |           0 |          0 |

---

## collect_cycle_indicators
Collect the cycle indicators of every ticker in one table: the length, phase and turning points of the cycles in the prices.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>window (int, optional):</u> The window size for calculating indicators.
Defaults to 14.
- <u>close_column (str, optional):</u> The name of the column containing the close prices.
Defaults to "Adj Close".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: Cycle indicators calculated based on the specified parameters.

**Notes:**

- The method calculates the cycle indicators for each asset in the Toolkit instance.
- The Hilbert transform indicators adapt to the dominant cycle of the price and the filters and
oscillators use their own default windows, so `window` is left unused.
- When growth is requested, the method calculates the growth of the indicator values
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.collect_cycle_indicators().xs("AAPL", level=1, axis="columns")
```

Which returns:

| Date       |   Hilbert Dominant Cycle Period |   Hilbert Dominant Cycle Phase |   Hilbert In Phase |   Hilbert Quadrature |   Hilbert Sine |   Hilbert Lead Sine |   Hilbert Trend Mode |   Hilbert Instantaneous Trendline |   MESA Adaptive Moving Average (MAMA) |   Following Adaptive Moving Average (FAMA) |   Swiss Army Knife Filter |   SuperSmoother Filter |   Even Better Sinewave |   Detrended Synthetic Price |   MESA Sine Wave Sine |   MESA Sine Wave Lead Sine |   Center of Gravity Oscillator |   Center of Gravity Trigger |   Laguerre RSI |
|:-----------|--------------------------------:|-------------------------------:|-------------------:|---------------------:|---------------:|--------------------:|---------------------:|----------------------------------:|--------------------------------------:|-------------------------------------------:|--------------------------:|-----------------------:|-----------------------:|----------------------------:|----------------------:|---------------------------:|-------------------------------:|----------------------------:|---------------:|
| 2025-12-17 |                         18.3901 |                       282.339  |            -2.1962 |               4.3125 |        -0.9769 |             -0.5397 |                    0 |                           276.437 |                               276.673 |                                    273.841 |                   -2.8349 |                274.241 |                -0.9054 |                     -1.3767 |               -0.7739 |                    -0.0994 |                        -5.5219 |                     -5.5285 |         0      |
| 2025-12-18 |                         18.2309 |                       303.757  |            -0.8122 |               1.9647 |        -0.8314 |             -0.195  |                    1 |                           276.799 |                               276.073 |                                    273.964 |                   -2.5273 |                272.939 |                -0.9568 |                     -1.5143 |               -0.6032 |                     0.1375 |                        -5.5252 |                     -5.5219 |         0      |
| 2025-12-19 |                         18.064  |                       -35.1903 |            -0.6121 |              -1.6204 |        -0.5763 |              0.1704 |                    1 |                           276.957 |                               274.397 |                                    274.072 |                   -2.0487 |                272.161 |                -0.9881 |                     -1.2741 |               -0.2922 |                     0.4696 |                        -5.5254 |                     -5.5252 |         0      |
| 2025-12-22 |                         17.9853 |                       -17.9254 |            -2.3867 |              -3.8683 |        -0.3078 |              0.4551 |                    1 |                           276.873 |                               274.178 |                                    274.075 |                   -1.347  |                271.642 |                -0.9995 |                     -1.4735 |                0.1788 |                     0.8222 |                        -5.5263 |                     -5.5254 |         0      |
| 2025-12-23 |                         18.0561 |                        -3.6741 |            -3.886  |              -1.9043 |        -0.0641 |              0.6603 |                    1 |                           276.637 |                               274.04  |                                    274.074 |                   -0.5972 |                271.196 |                -0.9999 |                     -1.2831 |                0.8774 |                     0.9597 |                        -5.5259 |                     -5.5263 |         0      |
| 2025-12-24 |                         18.3028 |                         9.1698 |            -4.0015 |              -0.3152 |         0.1594 |              0.8108 |                    1 |                           276.361 |                               273.981 |                                    274.072 |                    0.2127 |                271.251 |                -0.9962 |                     -0.8825 |                0.6824 |                    -0.0344 |                        -5.519  |                     -5.5259 |         0.1145 |
| 2025-12-26 |                         18.6492 |                        13.3466 |            -4.0726 |               2.8793 |         0.2308 |              0.8512 |                    0 |                           276.11  |                               273.904 |                                    274.067 |                    1.0468 |                271.629 |                -0.9816 |                     -0.6725 |                0.9729 |                     0.5244 |                        -5.5128 |                     -5.519  |         0.1222 |
| 2025-12-29 |                         18.9902 |                        23.5747 |            -1.6754 |               4.2075 |         0.3999 |              0.9309 |                    0 |                           275.772 |                               273.85  |                                    274.062 |                    1.7167 |                272.038 |                -0.9626 |                     -0.4628 |                0.3714 |                    -0.3939 |                        -5.5043 |                     -5.5128 |         0.203  |
| 2025-12-30 |                         19.3292 |                        29.9641 |            -1.2128 |               1.7906 |         0.4995 |              0.9658 |                    1 |                           275.284 |                               272.991 |                                    273.794 |                    2.1545 |                272.316 |                -0.9522 |                     -0.423  |               -0.6187 |                    -0.993  |                        -5.4973 |                     -5.5043 |         0.2628 |
| 2025-12-31 |                         19.6066 |                        33.1911 |            -0.9892 |               3.5115 |         0.5474 |              0.9788 |                    1 |                           274.885 |                               272.887 |                                    273.772 |                    2.3417 |                272.229 |                -0.9772 |                     -0.5599 |               -0.7431 |                    -0.0523 |                        -5.4957 |                     -5.4973 |         0.3273 |

---

## get_hilbert_dominant_cycle_period
Calculate the Hilbert Transform Dominant Cycle Period (HT_DCPERIOD): the length, in periods, of the main cycle in the prices.

The dominant cycle period is the length, in periods, of the cycle that dominates the price, measured with Ehlers' homodyne discriminator. The smoothed and detrended price is split by the Hilbert transform into an in-phase and a quadrature component, the two sides of an analytic signal whose angle advances 360 degrees per cycle. Multiplying the signal with that of the period before gives the change of the angle per period, and 360 degrees divided by that change is the period of the cycle. A short period means the price swings quickly, a long one that it moves in slow waves or trends.

The formula is as follows:

$$
\text{Smooth} = \frac{4 \cdot \text{Price} + 3 \cdot \operatorname{Price}(t-1) + 2 \cdot \operatorname{Price}(t-2) + \operatorname{Price}(t-3)}{10}
$$

$$
H(x) = (0.0962 \cdot x + 0.5769 \cdot x(t-2) - 0.5769 \cdot x(t-4) - 0.0962 \cdot x(t-6)) \cdot (0.075 \cdot \operatorname{Period}(t-1) + 0.54)
$$

$$
\text{Detrender} = H(\text{Smooth}),\;\; Q_{1} = H(\text{Detrender}),\;\; I_{1} = \operatorname{Detrender}(t-3)
$$

$$
I_{2} = 0.2 \cdot (I_{1} - H(Q_{1})) + 0.8 \cdot \operatorname{I2}(t-1)\;\;\text{and}\;\; Q_{2} = 0.2 \cdot (Q_{1} + H(I_{1})) + 0.8 \cdot \operatorname{Q2}(t-1)
$$

$$
\text{Re} = 0.2 \cdot (I_{2} \cdot \operatorname{I2}(t-1) + Q_{2} \cdot \operatorname{Q2}(t-1)) + 0.8 \cdot \operatorname{Re}(t-1)
$$

$$
\text{Im} = 0.2 \cdot (I_{2} \cdot \operatorname{Q2}(t-1) - Q_{2} \cdot \operatorname{I2}(t-1)) + 0.8 \cdot \operatorname{Im}(t-1)
$$

$$
\text{Period} = \frac{360}{\operatorname{arctan}\left(\frac{\text{Im}}{\text{Re}}\right) \;\text{in degrees}},\;\; \text{limited to between 0.67 and 1.5 times Period(t-1) and to between 6 and 50 periods},\;\; \text{then smoothed as}\; 0.2 \cdot \text{Period} + 0.8 \cdot \operatorname{Period}(t-1)
$$

$$
\text{Dominant Cycle Period} = 0.33 \cdot \text{Period} + 0.67 \cdot \text{Dominant Cycle Period}(t-1)
$$

**References:**

- paper | Ehlers, J.F. (2001). "Rocket Science for Traders: Digital Signal Processing Applications." John Wiley & Sons.
- library | Referenced against TA-Lib's [HT_DCPERIOD](https://ta-lib.org/functions/ht_dcperiod.html){:target="_blank"}
- library | Shares similar logic as pandas-ta-classic's [ht_dcperiod](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/cycles/ht_dcperiod.py#L14){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the dominant cycle period.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame or pd.Series: The dominant cycle period in periods.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the dominant cycle period for each asset in the Toolkit instance.
- Equals TA-Lib's HT_DCPERIOD and pandas-ta-classic's ht_dcperiod.
- The recursion starts from zero on the 12th period of each ticker's own history, as in TA-Lib,
and the first 32 periods (TA-Lib's lookback) are NaN.
- The Hilbert transform and the homodyne discriminator are shared with the other Hilbert Transform
indicators and MAMA.
- When growth is requested, the method calculates the growth of the dominant cycle period over the
given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_hilbert_dominant_cycle_period().tail(5)
```

Which returns:

| Date       |    AAPL |    MSFT |   Benchmark |
|:-----------|--------:|--------:|------------:|
| 2025-12-24 | 18.3028 | 16.1896 |     18.5522 |
| 2025-12-26 | 18.6492 | 15.902  |     19.001  |
| 2025-12-29 | 18.9902 | 15.6336 |     19.0715 |
| 2025-12-30 | 19.3292 | 15.4975 |     18.9697 |
| 2025-12-31 | 19.6066 | 15.3876 |     18.9366 |

---

## get_hilbert_dominant_cycle_phase
Calculate the Hilbert Transform Dominant Cycle Phase (HT_DCPHASE): where the prices are within their main cycle, in degrees.

The dominant cycle phase is the position of the price within its dominant cycle, in degrees. It is the angle of the discrete Fourier transform of the smoothed price over exactly one dominant cycle period, corrected for the lag of the smoothing. The phase advances by about 360 degrees divided by the period each period while the price cycles, and barely moves (or moves backwards) while it trends. It runs from -45 to 315 degrees and wraps around once per cycle.

The formula is as follows:

$$
\text{Smooth} = \frac{4 \cdot \text{Price} + 3 \cdot \operatorname{Price}(t-1) + 2 \cdot \operatorname{Price}(t-2) + \operatorname{Price}(t-3)}{10}
$$

$$
H(x) = (0.0962 \cdot x + 0.5769 \cdot x(t-2) - 0.5769 \cdot x(t-4) - 0.0962 \cdot x(t-6)) \cdot (0.075 \cdot \operatorname{Period}(t-1) + 0.54)
$$

$$
\text{Detrender} = H(\text{Smooth}),\;\; Q_{1} = H(\text{Detrender}),\;\; I_{1} = \operatorname{Detrender}(t-3)
$$

$$
I_{2} = 0.2 \cdot (I_{1} - H(Q_{1})) + 0.8 \cdot \operatorname{I2}(t-1)\;\;\text{and}\;\; Q_{2} = 0.2 \cdot (Q_{1} + H(I_{1})) + 0.8 \cdot \operatorname{Q2}(t-1)
$$

$$
\text{Re} = 0.2 \cdot (I_{2} \cdot \operatorname{I2}(t-1) + Q_{2} \cdot \operatorname{Q2}(t-1)) + 0.8 \cdot \operatorname{Re}(t-1)
$$

$$
\text{Im} = 0.2 \cdot (I_{2} \cdot \operatorname{Q2}(t-1) - Q_{2} \cdot \operatorname{I2}(t-1)) + 0.8 \cdot \operatorname{Im}(t-1)
$$

$$
\text{Period} = \frac{360}{\operatorname{arctan}\left(\frac{\text{Im}}{\text{Re}}\right) \;\text{in degrees}},\;\; \text{limited to between 0.67 and 1.5 times Period(t-1) and to between 6 and 50 periods},\;\; \text{then smoothed as}\; 0.2 \cdot \text{Period} + 0.8 \cdot \operatorname{Period}(t-1)
$$

$$
\text{Dominant Cycle Period} = 0.33 \cdot \text{Period} + 0.67 \cdot \text{Dominant Cycle Period}(t-1)
$$

$$
N = \text{the Dominant Cycle Period rounded to the nearest whole period}
$$

$$
\text{Real} = \sum \sin\left(\frac{360 \cdot i}{N}\right) \cdot \operatorname{Smooth}(\text{t-i})\;\;\text{and}\;\; \text{Imag} = \sum \cos\left(\frac{360 \cdot i}{N}\right) \cdot \operatorname{Smooth}(\text{t-i}) \;\text{for}\; i = 0 \;\text{to}\; N - 1
$$

$$
\text{Dominant Cycle Phase} = \operatorname{arctan}\left(\frac{\text{Real}}{\text{Imag}}\right) + 90 + \frac{360}{\text{Dominant Cycle Period in degrees}},\;\; \text{plus 180 when Imag is negative and minus 360 when above 315}
$$

**References:**

- paper | Ehlers, J.F. (2001). "Rocket Science for Traders: Digital Signal Processing Applications." John Wiley & Sons.
- library | Referenced against TA-Lib's [HT_DCPHASE](https://ta-lib.org/functions/ht_dcphase.html){:target="_blank"}
- library | Shares similar logic as pandas-ta-classic's [ht_dcphase](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/cycles/ht_dcphase.py#L14){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the dominant cycle phase.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame or pd.Series: The dominant cycle phase in degrees.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the dominant cycle phase for each asset in the Toolkit instance.
- Equals TA-Lib's HT_DCPHASE and pandas-ta-classic's ht_dcphase, in degrees as in TA-Lib and Ehlers
(multiply by $$\pi / 180$$ for radians).
- The recursion starts from zero on the 37th period of each ticker's own history, as in TA-Lib,
and the first 63 periods (TA-Lib's lookback) are NaN.
- The phase is an angle that wraps from 315 to -45 degrees, so its growth and its standardized
values jump at every new cycle.
- When growth is requested, the method calculates the growth of the dominant cycle phase over the
given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_hilbert_dominant_cycle_phase().tail(5)
```

Which returns:

| Date       |    AAPL |     MSFT |   Benchmark |
|:-----------|--------:|---------:|------------:|
| 2025-12-24 |  9.1698 |  54.627  |    -17.3216 |
| 2025-12-26 | 13.3466 |  80.4208 |     37.7222 |
| 2025-12-29 | 23.5747 | 104.685  |     74.4394 |
| 2025-12-30 | 29.9641 | 136.968  |     97.2947 |
| 2025-12-31 | 33.1911 | 164.331  |    115.377  |

---

## get_hilbert_phasor_components
Calculate the Hilbert Transform Phasor Components (HT_PHASOR): the in-phase and quadrature parts of the prices' cycle, from which its phase and period follow.

The phasor components are the in-phase component, the smoothed and detrended price lagged three periods, and the quadrature component, its Hilbert transform: the same cycle shifted by 90 degrees. Together they form the analytic signal (the phasor) of the price cycle, whose angle is the phase of the cycle and whose length is its amplitude, in price units.

The formula is as follows:

$$
\text{Smooth} = \frac{4 \cdot \text{Price} + 3 \cdot \operatorname{Price}(t-1) + 2 \cdot \operatorname{Price}(t-2) + \operatorname{Price}(t-3)}{10}
$$

$$
H(x) = (0.0962 \cdot x + 0.5769 \cdot x(t-2) - 0.5769 \cdot x(t-4) - 0.0962 \cdot x(t-6)) \cdot (0.075 \cdot \operatorname{Period}(t-1) + 0.54)
$$

$$
\text{In Phase} = H(\text{Smooth}) (t-3)
$$

$$
\text{Quadrature} = H(H(\text{Smooth}))
$$

$$
\text{Period} = \text{the period of the homodyne discriminator before smoothing} \;(\text{see the Dominant Cycle Period})
$$

**References:**

- paper | Ehlers, J.F. (2001). "Rocket Science for Traders: Digital Signal Processing Applications." John Wiley & Sons.
- library | Referenced against TA-Lib's [HT_PHASOR](https://ta-lib.org/functions/ht_phasor.html){:target="_blank"}
- library | Shares similar logic as pandas-ta-classic's [ht_phasor](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/cycles/ht_phasor.py#L14){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the phasor components.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The In Phase and Quadrature components in price units.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the phasor components for each asset in the Toolkit instance.
- Equals TA-Lib's HT_PHASOR and pandas-ta-classic's ht_phasor.
- The recursion starts from zero on the 12th period of each ticker's own history, as in TA-Lib,
and the first 32 periods (TA-Lib's lookback) are NaN.
- When growth is requested, the method calculates the growth of the phasor components over the
given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_hilbert_phasor_components().xs("AAPL", level=1, axis="columns").tail(5)
```

Which returns:

| Date       |   In Phase |   Quadrature |
|:-----------|-----------:|-------------:|
| 2025-12-24 |    -4.0015 |      -0.3152 |
| 2025-12-26 |    -4.0726 |       2.8793 |
| 2025-12-29 |    -1.6754 |       4.2075 |
| 2025-12-30 |    -1.2128 |       1.7906 |
| 2025-12-31 |    -0.9892 |       3.5115 |

---

## get_hilbert_sine_wave
Calculate the Hilbert Transform SineWave (HT_SINE), or the MESA Sine Wave over a fixed window: the sine of the phase of the prices' main cycle and its lead, whose crossings mark the turning points of the cycle.

The sine wave is the sine of the dominant cycle phase and the lead sine the sine of the phase advanced by 45 degrees. While the price cycles, the two lines cross shortly before the turning points of the cycle: the sine crossing above the lead sine marks a low, crossing below a high. While the price trends, the phase barely moves and the two lines run apart without crossing. The MESA Sine Wave is Ehlers' sinewave indicator over a fixed window: the phase of the price within a cycle of that window, measured with a discrete Fourier transform, where the Hilbert Transform SineWave measures the window as the dominant cycle.

The formula is as follows, per method:

"standard":

$$
\text{Smooth} = \frac{4 \cdot \text{Price} + 3 \cdot \operatorname{Price}(t-1) + 2 \cdot \operatorname{Price}(t-2) + \operatorname{Price}(t-3)}{10}
$$

$$
H(x) = (0.0962 \cdot x + 0.5769 \cdot x(t-2) - 0.5769 \cdot x(t-4) - 0.0962 \cdot x(t-6)) \cdot (0.075 \cdot \operatorname{Period}(t-1) + 0.54)
$$

$$
\text{Detrender} = H(\text{Smooth}),\;\; Q_{1} = H(\text{Detrender}),\;\; I_{1} = \operatorname{Detrender}(t-3)
$$

$$
I_{2} = 0.2 \cdot (I_{1} - H(Q_{1})) + 0.8 \cdot \operatorname{I2}(t-1)\;\;\text{and}\;\; Q_{2} = 0.2 \cdot (Q_{1} + H(I_{1})) + 0.8 \cdot \operatorname{Q2}(t-1)
$$

$$
\text{Re} = 0.2 \cdot (I_{2} \cdot \operatorname{I2}(t-1) + Q_{2} \cdot \operatorname{Q2}(t-1)) + 0.8 \cdot \operatorname{Re}(t-1)
$$

$$
\text{Im} = 0.2 \cdot (I_{2} \cdot \operatorname{Q2}(t-1) - Q_{2} \cdot \operatorname{I2}(t-1)) + 0.8 \cdot \operatorname{Im}(t-1)
$$

$$
\text{Period} = \frac{360}{\operatorname{arctan}\left(\frac{\text{Im}}{\text{Re}}\right) \;\text{in degrees}},\;\; \text{limited to between 0.67 and 1.5 times Period(t-1) and to between 6 and 50 periods},\;\; \text{then smoothed as}\; 0.2 \cdot \text{Period} + 0.8 \cdot \operatorname{Period}(t-1)
$$

$$
\text{Dominant Cycle Period} = 0.33 \cdot \text{Period} + 0.67 \cdot \text{Dominant Cycle Period}(t-1)
$$

$$
N = \text{the Dominant Cycle Period rounded to the nearest whole period}
$$

$$
\text{Real} = \sum \sin\left(\frac{360 \cdot i}{N}\right) \cdot \operatorname{Smooth}(\text{t-i})\;\;\text{and}\;\; \text{Imag} = \sum \cos\left(\frac{360 \cdot i}{N}\right) \cdot \operatorname{Smooth}(\text{t-i}) \;\text{for}\; i = 0 \;\text{to}\; N - 1
$$

$$
\text{Dominant Cycle Phase} = \operatorname{arctan}\left(\frac{\text{Real}}{\text{Imag}}\right) + 90 + \frac{360}{\text{Dominant Cycle Period in degrees}},\;\; \text{plus 180 when Imag is negative and minus 360 when above 315}
$$

$$
\text{Sine} = \sin(\text{Dominant Cycle Phase})
$$

$$
\text{Lead Sine} = \sin(\text{Dominant Cycle Phase} + 45 \;\text{degrees})
$$

"mesa":

$$
\text{Real} = \sum \sin\left(\frac{360 \cdot i}{\text{Window}}\right) \cdot \operatorname{Price}(\text{t-i})\;\;\text{and}\;\; \text{Imaginary} = \sum \cos\left(\frac{360 \cdot i}{\text{Window}}\right) \cdot \operatorname{Price}(\text{t-i}) \;\text{for}\; i = 0 \;\text{to Window} - 1
$$

$$
\text{Phase} = \operatorname{arctan}\left(\frac{\text{Real}}{\text{Imaginary}}\right) + 90 \;\text{degrees},\;\; \text{plus 180 when Imaginary is negative},\;\; \text{or}\;\; 90 \cdot \operatorname{sign}(\text{Real}) + 90 \;\text{when} \;\left|\text{Imaginary}\right| \;\text{is at most}\; 0.001
$$

$$
\text{Sine} = \sin(\text{Phase})
$$

$$
\text{Lead Sine} = \sin(\text{Phase} + 45 \;\text{degrees})
$$

**Also known as:** HT_SINE, Hilbert Transform SineWave, sine wave, lead sine, MSW, MESA Sine Wave, MESA sinewave.

**References:**

- paper | Ehlers, J.F. (2001). "Rocket Science for Traders: Digital Signal Processing Applications." John Wiley & Sons.
- paper | Ehlers, J.F. (1992). "MESA and Trading Market Cycles." John Wiley & Sons.
- library | Referenced against TA-Lib's [HT_SINE](https://ta-lib.org/functions/ht_sine.html){:target="_blank"}
- library | Referenced against Tulip Indicators' [msw](https://tulipindicators.org/msw){:target="_blank"} (MESA Sine Wave)
- library | Referenced against pandas-ta-classic's [msw](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/cycles/msw.py#L14){:target="_blank"} (MESA Sine Wave)
- library | Shares similar logic as pandas-ta-classic's [ht_sine](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/cycles/ht_sine.py#L14){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the high and low of the median price are
adjusted for dividends in the same way.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the sine wave.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>method (str, optional):</u> The sine wave. Options are: "standard" (the Hilbert Transform SineWave),
"mesa" (the MESA Sine Wave over a fixed window). Defaults to "standard".
- <u>median_price (bool, optional):</u> Whether to filter the median price (High + Low) / 2, as
Ehlers does, or the close of `close_column`, as Tulip Indicators and
pandas-ta-classic do. Only used when method="mesa". Defaults to True.
- <u>window (int, optional):</u> The number of periods of the cycle. Only used when
method="mesa". Defaults to 5.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The Sine and Lead Sine, between -1 and 1.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the sine wave for each asset in the Toolkit instance.
- Equals TA-Lib's HT_SINE and pandas-ta-classic's ht_sine.
- The recursion starts from zero on the 37th period of each ticker's own history, as in TA-Lib,
and the first 63 periods (TA-Lib's lookback) are NaN.
- MESA Sine Wave: equals pandas-ta-classic's msw on the close (not the median price), and Tulip
Indicators' msw to 1e-4, as Tulip takes 3.1415926 for $$\pi$$. Both start one period later, on the
period after the first full window. Without an imaginary part the phase is 90 degrees times
the sign of the real part, as in Ehlers' sinewave indicator, where Tulip Indicators and
pandas-ta-classic take 180 degrees.
- When growth is requested, the method calculates the growth of the sine wave over the
given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_hilbert_sine_wave().xs("AAPL", level=1, axis="columns").tail(5)
```

Which returns:

| Date       |   Lead Sine |   Sine |
|:-----------|------------:|-------:|
| 2025-12-24 |      0.8108 | 0.1594 |
| 2025-12-26 |      0.8512 | 0.2308 |
| 2025-12-29 |      0.9309 | 0.3999 |
| 2025-12-30 |      0.9658 | 0.4995 |
| 2025-12-31 |      0.9788 | 0.5474 |

---

## get_hilbert_trend_mode
Calculate the Hilbert Transform Trend vs Cycle Mode (HT_TRENDMODE): whether the prices are trending (1) or moving in a cycle (0).

The trend mode tells whether the price trends (1) or moves in a cycle (0). Ehlers' rules: a crossing of the sine and the lead sine starts a cycle, which lasts at least half a dominant cycle period; a phase that advances at the rate of the dominant cycle is a cycle; and a smoothed price 1.5% or more away from the instantaneous trendline is always a trend. Cycle indicators (oscillators) fit the cycle mode, trend-following indicators the trend mode.

The formula is as follows:

$$
\text{Trend} = 1,\;\; \text{or 0 with the periods in trend restarting from zero when the Sine and the Lead Sine cross (see the Hilbert Transform SineWave)}
$$

$$
\text{Trend} = 0 \;\text{while the periods in trend are fewer than half the Dominant Cycle Period}
$$

$$
\text{Trend} = 0 \;\text{when the change of the Dominant Cycle Phase is between}\; 0.67 \;\text{and}\; 1.5 \;\text{times} \;\frac{360}{\text{Dominant Cycle Period}}
$$

$$
\text{Trend} = 1 \;\text{when} \;\frac{\left|\text{Smooth} - \text{Trendline}\right|}{\text{Trendline}} \geq 0.015 \;(\text{see the Instantaneous Trendline})
$$

**References:**

- paper | Ehlers, J.F. (2001). "Rocket Science for Traders: Digital Signal Processing Applications." John Wiley & Sons.
- library | Referenced against TA-Lib's [HT_TRENDMODE](https://ta-lib.org/functions/ht_trendmode.html){:target="_blank"}
- library | Shares similar logic as pandas-ta-classic's [ht_trendmode](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/cycles/ht_trendmode.py#L14){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the trend mode.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame or pd.Series: 1 when the price trends and 0 when it cycles.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the trend mode for each asset in the Toolkit instance.
- Equals TA-Lib's HT_TRENDMODE and pandas-ta-classic's ht_trendmode after the lookback.
- The recursion starts from zero on the 37th period of each ticker's own history, as in TA-Lib,
and the first 63 periods (TA-Lib's lookback) are NaN, where TA-Lib returns 0.
- When growth is requested, the method calculates the growth of the trend mode over the
given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_hilbert_trend_mode().tail(5)
```

Which returns:

| Date       |   AAPL |   MSFT |   Benchmark |
|:-----------|-------:|-------:|------------:|
| 2025-12-24 |      1 |      0 |           0 |
| 2025-12-26 |      0 |      0 |           0 |
| 2025-12-29 |      0 |      0 |           0 |
| 2025-12-30 |      1 |      0 |           0 |
| 2025-12-31 |      1 |      0 |           0 |

---

## get_mesa_adaptive_moving_average
Calculate the MESA Adaptive Moving Average (MAMA) and the Following Adaptive Moving Average (FAMA): averages that adapt to the speed of the prices' cycle, so they follow fast moves and stay flat in a range.

MAMA is an exponential moving average whose smoothing factor follows the rate at which the phase of the price cycle changes, measured with the Hilbert transform. When the phase jumps, as at the start of a move, the smoothing factor is the fast limit and MAMA follows the price closely; when the phase advances slowly, the factor falls towards the slow limit and MAMA flattens. FAMA applies half the smoothing factor to MAMA, so that it follows MAMA, and Ehlers reads the crossings of the two lines as changes of direction.

The formula is as follows:

$$
\text{Smooth} = \frac{4 \cdot \text{Price} + 3 \cdot \operatorname{Price}(t-1) + 2 \cdot \operatorname{Price}(t-2) + \operatorname{Price}(t-3)}{10}
$$

$$
I_{1} \;\text{and}\; Q_{1} = \text{the In Phase and Quadrature components} \;(\text{see the Hilbert Transform Phasor Components})
$$

$$
\text{Phase} = \operatorname{arctan}\left(\frac{Q_{1}}{I_{1}}\right) \;\text{in degrees}
$$

$$
\text{Delta Phase} = \operatorname{Phase}(t-1) - \text{Phase},\;\; \text{at least 1}
$$

$$
\text{Alpha} = \frac{\text{Fast Limit}}{\text{Delta Phase}},\;\; \text{at least the Slow Limit}
$$

$$
\text{MAMA} = \text{Alpha} \cdot \text{Price} + (1 - \text{Alpha}) \cdot \operatorname{MAMA}(t-1)
$$

$$
\text{FAMA} = 0.5 \cdot \text{Alpha} \cdot \text{MAMA} + (1 - 0.5 \cdot \text{Alpha}) \cdot \operatorname{FAMA}(t-1)
$$

**Also known as:** MAMA, FAMA, MESA adaptive moving average.

**References:**

- paper | Ehlers, J.F. (2001). "MESA Adaptive Moving Averages." Technical Analysis of Stocks & Commodities, September 2001.
- paper | Ehlers, J.F. (2001). "Rocket Science for Traders: Digital Signal Processing Applications." John Wiley & Sons.
- library | Referenced against TA-Lib's [MAMA](https://ta-lib.org/functions/mama.html){:target="_blank"}
- library | Shares similar logic as pandas-ta-classic's [mama](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/overlap/mama.py#L248){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>fast_limit (float, optional):</u> The largest smoothing factor, used when the phase jumps.
Defaults to 0.5, Ehlers' value.
- <u>slow_limit (float, optional):</u> The smallest smoothing factor, used when the phase advances
slowly. Defaults to 0.05, Ehlers' value.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the MESA adaptive moving average.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The MAMA and FAMA in price units.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the MESA adaptive moving average for each asset in the Toolkit instance.
- Equals TA-Lib's MAMA and pandas-ta-classic's mama on the close. Ehlers applies it to the median
price (High + Low) / 2 in his article.
- The recursion starts from zero on the 12th period of each ticker's own history, as in TA-Lib,
and the first 32 periods (TA-Lib's lookback) are NaN. MAMA and FAMA also start from zero there, as in
TA-Lib and Ehlers' article. MAMA has caught up with the price by the end of the lookback, but FAMA, at half
the smoothing factor, is then still several percent below it and settles to within 0.1% after about
80 periods. The Toolkit calculates the technical indicators from a year before `start_date`, so with
daily data this warm-up falls before the dates shown.
- With the default `close_column` of "Adj Close" the prices are adjusted for dividends.
- When growth is requested, the method calculates the growth of the MESA adaptive moving average over
the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_mesa_adaptive_moving_average().xs("AAPL", level=1, axis="columns").tail(5)
```

Which returns:

| Date       |    FAMA |    MAMA |
|:-----------|--------:|--------:|
| 2025-12-24 | 274.072 | 273.981 |
| 2025-12-26 | 274.067 | 273.904 |
| 2025-12-29 | 274.062 | 273.85  |
| 2025-12-30 | 273.794 | 272.991 |
| 2025-12-31 | 273.772 | 272.887 |

---

## get_swiss_army_knife_filter
Calculate Ehlers' Swiss Army Knife filter: a family of filters that remove the trend (high-pass), the noise (low-pass) or both (band-pass) from the prices.

The Swiss Army Knife indicator of Ehlers (2006) is one second-order recursive filter whose coefficients select its response. The high-pass filters remove the trend and keep the cycles shorter than the window, the two-pole one with a steeper cut than the one-pole one. The band-pass filter keeps only the cycles around the window, which shows how strongly that cycle is present and where it turns. The Butterworth and Gaussian filters are low-pass filters that smooth away the cycles shorter than the window with little lag.

The formula is as follows:

$$
\text{Filter} = c_{0} \cdot (b_{0} \cdot \text{Price} + b_{1} \cdot \operatorname{Price}(t-1) + b_{2} \cdot \operatorname{Price}(t-2)) + a_{1} \cdot \operatorname{Filter}(t-1) + a_{2} \cdot \operatorname{Filter}(t-2),\;\; \text{with}\;\; b_{0} = 1 \;\text{and every other coefficient 0 unless set below}
$$

$$
\text{One-pole}\; \alpha = \frac{\cos\left(\frac{360}{\text{Window}}\right) + \sin\left(\frac{360}{\text{Window}}\right) - 1}{\cos\left(\frac{360}{\text{Window}}\right)}
$$

$$
\text{Two-pole}\; \alpha = - \text{Beta} + \sqrt{\text{Beta}^{2} + 2 \cdot \text{Beta}},\;\; \text{with}\;\; \text{Beta} = 2.415 \cdot \left(1 - \cos\left(\frac{360}{\text{Window}}\right)\right)
$$

$$
\text{High-pass:}\;\; c_{0} = 1 - \frac{\alpha}{2},\;\; b_{1} = - 1\;\;\text{and}\;\; a_{1} = 1 - \alpha,\;\; \text{with the one-pole alpha}
$$

$$
\text{Two-pole high-pass:}\;\; c_{0} = \left(1 - \frac{\alpha}{2}\right)^{2},\;\; b_{1} = - 2,\;\; b_{2} = 1,\;\; a_{1} = 2 \cdot (1 - \alpha)\;\;\text{and}\;\; a_{2} = - (1 - \alpha)^{2}
$$

$$
\text{Butterworth:}\;\; c_{0} = \frac{\alpha^{2}}{4},\;\; b_{1} = 2,\;\; b_{2} = 1,\;\; a_{1} = 2 \cdot (1 - \alpha)\;\;\text{and}\;\; a_{2} = - (1 - \alpha)^{2}
$$

$$
\text{Gaussian:}\;\; c_{0} = \alpha^{2},\;\; a_{1} = 2 \cdot (1 - \alpha)\;\;\text{and}\;\; a_{2} = - (1 - \alpha)^{2}
$$

$$
\text{Band-pass:}\;\; \text{Beta} = \cos\left(\frac{360}{\text{Window}}\right),\;\; \Gamma = \frac{1}{\cos\left(\frac{720 \cdot \Delta}{\text{Window}}\right)},\;\; \alpha = \Gamma - \sqrt{\Gamma^{2} - 1},\;\; c_{0} = \frac{1 - \alpha}{2},\;\; b_{2} = - 1,\;\; a_{1} = \text{Beta} \cdot (1 + \alpha)\;\;\text{and}\;\; a_{2} = - \alpha
$$

**References:**

- paper | Ehlers, J.F. (2006). "Swiss Army Knife Indicator." Technical Analysis of Stocks & Commodities, 24(1), 28-31, 50-53.
- library | Referenced against TA-Lib's [SWAK_HP](https://ta-lib.org/functions/swak_hp.html){:target="_blank"}
- library | Referenced against TA-Lib's [SWAK_2PHP](https://ta-lib.org/functions/swak_2php.html){:target="_blank"}
- library | Referenced against TA-Lib's [SWAK_BP](https://ta-lib.org/functions/swak_bp.html){:target="_blank"}
- library | Referenced against TA-Lib's [SWAK_BUTTER](https://ta-lib.org/functions/swak_butter.html){:target="_blank"}
- library | Referenced against TA-Lib's [SWAK_GAUSS](https://ta-lib.org/functions/swak_gauss.html){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the high and low prices are adjusted
for dividends in the same way.
- <u>median_price (bool, optional):</u> Whether to filter the median price (High + Low) / 2, as Ehlers does,
or the close of `close_column`, as TA-Lib's SWAK functions do. Defaults to True.
- <u>window (int, optional):</u> The cutoff period of the high-pass and low-pass filters and the centre period of
the band-pass filter, at least 5. Defaults to 20.
- <u>method (str, optional):</u> The filter. Options are: "high_pass" (one-pole high-pass filter),
"two_pole_high_pass" (two-pole high-pass filter), "band_pass" (band-pass filter),
"butterworth" (two-pole Butterworth low-pass filter), "gaussian" (Gaussian low-pass filter).
Defaults to "band_pass", the default of Ehlers' listing.
- <u>delta (float, optional):</u> The half bandwidth of the band-pass filter as a fraction of its centre
frequency, above 0 and at most 0.5. Defaults to 0.1.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Swiss Army Knife filter.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame or pd.Series: The filtered prices, in price units for the Butterworth and Gaussian filters
and centred on zero for the high-pass and band-pass filters.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the Swiss Army Knife filter for each asset in the Toolkit instance.
- Equals TA-Lib's SWAK functions on the close (not the median price), from the first period on.
- The filter starts in the steady state of a constant price equal to the first price of each ticker's own
history: the low-pass filters on that price, the high-pass and band-pass filters on zero, as in TA-Lib.
Ehlers' listing starts every filter from zero, which keeps the low-pass filters far below the price for
many periods.
- When growth is requested, the method calculates the growth of the Swiss Army Knife filter over the
given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_swiss_army_knife_filter().tail(5)
```

Which returns:

| Date       |   AAPL |   MSFT |   Benchmark |
|:-----------|-------:|-------:|------------:|
| 2025-12-24 | 0.2127 | 1.3624 |     -0.207  |
| 2025-12-26 | 1.0468 | 2.0027 |      1.5323 |
| 2025-12-29 | 1.7167 | 2.3917 |      2.9695 |
| 2025-12-30 | 2.1545 | 2.5467 |      3.9497 |
| 2025-12-31 | 2.3417 | 2.4341 |      4.4016 |

---

## get_even_better_sinewave
Calculate Ehlers' Even Better Sinewave: an oscillator between -1 and 1 that shows whether the prices move in a cycle or a trend and where they are in the cycle.

The Even Better Sinewave of Ehlers (2013) removes the trend with a one-pole high-pass filter, smooths the remaining cycles with a SuperSmoother and divides their average over three periods by the square root of their power over the same periods. The result swings between -1 and 1 like a sine wave while the price cycles and stays near 1 (or -1) while it trends up (or down), so it tells a cycle from a trend and marks the turns of the cycle.

The formula is as follows:

$$
\alpha = \frac{1 - \sin\left(\frac{360}{\text{Window}}\right)}{\cos\left(\frac{360}{\text{Window}}\right)}
$$

$$
\text{HP} = 0.5 \cdot (1 + \alpha) \cdot (\text{Price} - \operatorname{Price}(t-1)) + \alpha \cdot \operatorname{HP}(t-1)
$$

$$
a = \exp\left(- \frac{\sqrt{2} \cdot \pi}{\text{Smoothing Window}}\right),\;\; b = 2 \cdot a \cdot \cos\left(\frac{\sqrt{2} \cdot 180}{\text{Smoothing Window}}\right),\;\; c_{2} = b,\;\; c_{3} = - a^{2}\;\;\text{and}\;\; c_{1} = 1 - c_{2} - c_{3}
$$

$$
\text{Filter} = \frac{c_{1} \cdot (\text{HP} + \operatorname{HP}(t-1))}{2} + c_{2} \cdot \operatorname{Filter}(t-1) + c_{3} \cdot \operatorname{Filter}(t-2)
$$

$$
\text{Wave} = \frac{\text{Filter} + \operatorname{Filter}(t-1) + \operatorname{Filter}(t-2)}{3}
$$

$$
\text{Power} = \frac{\text{Filter}^{2} + \operatorname{Filter}(t-1)^{2} + \operatorname{Filter}(t-2)^{2}}{3}
$$

$$
\text{Even Better Sinewave} = \frac{\text{Wave}}{\sqrt{\text{Power}}}
$$

**References:**

- paper | Ehlers, J.F. (2013). "Cycle Analytics for Traders: Advanced Technical Trading Concepts." John Wiley & Sons.
- library | Referenced against pandas-ta-classic's [ebsw](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/cycles/ebsw.py#L63){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int, optional):</u> The cutoff period of the high-pass filter, the longest cycle kept. Defaults to 40.
- <u>smooth_window (int, optional):</u> The critical period of the SuperSmoother. Defaults to 10.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Even Better Sinewave.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame or pd.Series: The Even Better Sinewave, between -1 and 1.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the Even Better Sinewave for each asset in the Toolkit instance.
- The filters start from zero on the first period of each ticker's own history, as in Ehlers' listing, and
the first `window` periods are NaN while they settle. pandas-ta-classic starts them on the 12th period;
the two converge as the start fades and are equal on prices that do not move before it.
- A period without power (three filter values of zero) is NaN, where pandas-ta-classic gives 0.
- When growth is requested, the method calculates the growth of the Even Better Sinewave over the
given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_even_better_sinewave().tail(5)
```

Which returns:

| Date       |    AAPL |   MSFT |   Benchmark |
|:-----------|--------:|-------:|------------:|
| 2025-12-24 | -0.9962 | 0.6793 |      0.5028 |
| 2025-12-26 | -0.9816 | 0.9452 |      0.8897 |
| 2025-12-29 | -0.9626 | 0.9932 |      0.9801 |
| 2025-12-30 | -0.9522 | 0.9992 |      0.9989 |
| 2025-12-31 | -0.9772 | 0.9868 |      0.9863 |

---

## get_detrended_synthetic_price
Calculate Ehlers' Detrended Synthetic Price: the difference between a fast and a slow average tuned to the prices' cycle, which shows the cycle without the trend.

The Detrended Synthetic Price of Ehlers (1992) is the difference between an exponential moving average over a quarter of the dominant cycle and one over half of it. The difference removes the trend and leaves a wave in phase with the dominant cycle of the price: above zero in the rising half of the cycle and below zero in the falling half.

The formula is as follows:

$$
\text{Detrended Synthetic Price} = \operatorname{EMA}\left(\text{Price},\; \frac{\text{Window}}{4}\right) - \operatorname{EMA}\left(\text{Price},\; \frac{\text{Window}}{2}\right)
$$

**References:**

- paper | Ehlers, J.F. (1992). "MESA and Trading Market Cycles." John Wiley & Sons.
- library | Referenced against pandas-ta-classic's [dsp](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/cycles/dsp.py#L12){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int, optional):</u> The period of the dominant cycle, at least 4. Defaults to 20.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Detrended Synthetic Price.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame or pd.Series: The Detrended Synthetic Price in price units.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the Detrended Synthetic Price for each asset in the Toolkit instance.
- The averages span a quarter and a half of the window, rounded down, and are seeded with their simple
average as every exponential moving average of the Toolkit; they agree with pandas-ta-classic's ema.
- pandas-ta-classic's dsp subtracts one exponential moving average from the price, Price - EMA(Price, 14),
a simpler detrender that also keeps the shorter cycles.
- When growth is requested, the method calculates the growth of the Detrended Synthetic Price over the
given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_detrended_synthetic_price().tail(5)
```

Which returns:

| Date       |    AAPL |   MSFT |   Benchmark |
|:-----------|--------:|-------:|------------:|
| 2025-12-24 | -0.8825 | 1.3797 |      2.6009 |
| 2025-12-26 | -0.6725 | 1.4629 |      2.902  |
| 2025-12-29 | -0.4628 | 1.328  |      2.5204 |
| 2025-12-30 | -0.423  | 1.231  |      2.0333 |
| 2025-12-31 | -0.5599 | 0.5235 |      0.8791 |

---

## get_center_of_gravity_oscillator
Calculate Ehlers' Center of Gravity (CG) Oscillator: the weighted position of the prices within a window, which marks the turning points of the cycle with little lag.

The Center of Gravity Oscillator of Ehlers (2002) is the balance point of the prices in the window, with the latest price at position 1, turned negative. When prices rise, the weight shifts to the latest prices and the balance point moves towards them, so the oscillator rises with the price, smoothed and with almost no lag. The trigger is the previous value, and a crossing of the two marks a turn. Ehlers sets the window to half the dominant cycle.

The formula is as follows:

$$
\text{Center of Gravity} = - \frac{\sum(i + 1) \cdot \operatorname{Price}(\text{t-i})}{\sum \;\operatorname{Price}(\text{t-i})} \;\text{for}\; i = 0 \;\text{to Window} - 1
$$

$$
\text{Trigger} = \text{Center of Gravity}(t-1)
$$

**References:**

- paper | Ehlers, J.F. (2002). "The Center Of Gravity Oscillator." Technical Analysis of Stocks & Commodities, 20(5), 20-24.
- library | Referenced against TA-Lib's [CG](https://ta-lib.org/functions/cg.html){:target="_blank"}
- library | Referenced against pandas-ta-classic's [cg](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/momentum/cg.py#L12){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the high and low prices are adjusted
for dividends in the same way.
- <u>median_price (bool, optional):</u> Whether to filter the median price (High + Low) / 2, as Ehlers does,
or the close of `close_column`, as TA-Lib and pandas-ta-classic do. Defaults to True.
- <u>window (int, optional):</u> The number of periods, ideally half the dominant cycle. Defaults to 10.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Center of Gravity Oscillator.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The Center of Gravity and its Trigger.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the Center of Gravity Oscillator for each asset in the Toolkit instance.
- Equals TA-Lib's CG and pandas-ta-classic's cg on the close (not the median price).
- The oscillator is not centred on zero: for flat prices it is -(Window + 1) / 2.
- A window whose prices sum to zero is NaN, where Ehlers' listing keeps the value before.
- When growth is requested, the method calculates the growth of the Center of Gravity Oscillator over the
given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_center_of_gravity_oscillator().xs("AAPL", level=1, axis="columns").tail(5)
```

Which returns:

| Date       |   Center of Gravity |   Trigger |
|:-----------|--------------------:|----------:|
| 2025-12-24 |             -5.519  |   -5.5259 |
| 2025-12-26 |             -5.5128 |   -5.519  |
| 2025-12-29 |             -5.5043 |   -5.5128 |
| 2025-12-30 |             -5.4973 |   -5.5043 |
| 2025-12-31 |             -5.4957 |   -5.4973 |

---

## get_event_filter
Calculate the events of an event filter: the dates something happens that is worth labeling, such as a run of returns in one direction.

Sampling on events rather than on every date keeps the labels of a quiet market from outnumbering those of the moves that matter, and the events are the dates `get_triple_barrier_labels(events=...)` labels.

- CUSUM filter: the symmetric CUSUM filter of López de Prado, after the quality control charts of Page (1954) and the trading rule of Lam and Yam (1997). It sums the log returns since the last event of each direction and reports an event when a sum moves beyond `threshold` daily volatilities, after which that sum starts again from zero. A price hovering around a level triggers no events, unlike a band crossing, as it takes a full run of the threshold to set one off.
- Z-score filter: the z-score filter: an event when the price lies at least `threshold` standard deviations from its average over `window` periods, a filter after the z-score peak detection of van Brakel (2014).

The formula is as follows, per method:

$$
\text{CUSUM filter:}\;\; y_{t} = \ln\left(\frac{p_{t}}{p_{t-1}}\right),\;\; S + \text{}_{t} = \max(0,\; S + \text{}_{t-1} + y_{t}),\;\; S - \text{}_{t} = \min(0,\; S - \text{}_{t-1} + y_{t}),\;\; h_{t} = \text{threshold}\; x \sigma_{t} \;(\text{the AFML daily volatility},\; \text{an EWM standard deviation of the returns with} \;\text{span});\;\; \text{an event of} - 1 \;\text{when}\; S - \text{}_{t} < - h_{t} (S - \text{}_{t} \;\text{resets}) \;\text{or else of 1 when}\; S + \text{}_{t} > h_{t} (S + \text{}_{t} \;\text{resets})
$$

$$
\text{Z-score filter:}\;\; z_{t} = \frac{p_{t} - \operatorname{mean}(p,\; \text{window})}{\operatorname{std}(p,\; \text{window})};\;\; \text{an event of 1 when}\; z_{t} \geq \text{threshold and of} - 1 \;\text{when}\; z_{t} \leq - \text{threshold}
$$

Each value uses the prices up to its date only.

**Also known as:** CUSUM filter, symmetric CUSUM filter, event-based sampling, z-score filter, event filter.

**References:**

- paper | López de Prado, M. (2018). "Advances in Financial Machine Learning." Wiley, section 2.5.2.1 (Snippet 2.4).
- paper | Lam, K. and Yam, H.C. (1997). "CUSUM Techniques for Technical Trading in Financial Markets." Financial Engineering and the Japanese Markets, 4(3), 257-274.
- paper | Page, E.S. (1954). "Continuous Inspection Schemes." Biometrika, 41(1/2), 100-115.
- paper | van Brakel, J.P.G. (2014). "Robust peak detection algorithm using z-scores." Stack Overflow ([https://stackoverflow.com/questions/22583391](https://stackoverflow.com/questions/22583391){:target="_blank"}).
- library | Referenced against RiskLabAI's [symmetric_cusum_filter](https://github.com/RiskLabAI/RiskLabAI.py/blob/v3.2.0/src/RiskLabAI/data/labeling/labeling.py#L78){:target="_blank"}

**Args:**

- <u>method (str, optional):</u> The filter. Options are: "cusum" (the symmetric CUSUM filter),
"z_score" (the z-score filter). Defaults to "cusum".
- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>threshold (float &#124; None, optional):</u> The threshold in volatilities: the multiple of
the daily volatility the CUSUM sums need to pass, or the number of standard
deviations of the z-score. Defaults to None, which uses 1 for "cusum" (the daily
volatility itself) and 3 for "z_score".
- <u>span (int, optional):</u> The span of the daily volatility of the CUSUM filter. Defaults
to 100.
- <u>window (int, optional):</u> The window of the average and standard deviation of the
z-score filter. Defaults to 20.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The events per date and ticker: 1 for an upward event, -1 for a
downward event and 0 otherwise.

**Notes:**

- The CUSUM sums start on each ticker's first return and the threshold needs two returns
for its volatility, so the first event comes after the third price.
- The z-score filter reports prices both above and below the band and takes one window
for the average and the standard deviation.
- The CUSUM test of `toolkit.econometrics.get_cusum_test` is a different tool: a test of
a stable mean over the whole sample rather than a filter that marks dates.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2024-01-01",
    end_date="2025-12-31",
)

events = toolkit.technicals.get_event_filter(threshold=2)

events[events.ne(0).any(axis=1)].tail()
```

Which returns:

| Date       |   AAPL |   MSFT |   Benchmark |
|:-----------|-------:|-------:|------------:|
| 2025-12-08 |     -1 |      1 |           0 |
| 2025-12-10 |      0 |     -1 |           0 |
| 2025-12-17 |      0 |      0 |          -1 |
| 2025-12-22 |     -1 |      0 |           1 |
| 2025-12-23 |      0 |      1 |           0 |

---

## get_triple_barrier_labels
Calculate the triple-barrier labels of López de Prado: for every date (or event) the first of three barriers the price reaches.

A profit-taking barrier lies `profit_taking` daily volatilities above the price, a stop-loss barrier `stop_loss` daily volatilities below it and a vertical barrier `horizon` periods later. The label is 1 when the upper barrier is reached first, -1 for the lower barrier and the sign of the return at the vertical barrier. Unlike a label on the return over a fixed horizon, it follows the path of the price the way a trade with a profit target, a stop-loss and a time limit does, and its barriers widen and narrow with the volatility.

With a `side`, such as the crossovers of `get_signals`, the labels are meta-labels: the returns are those of the bet (multiplied by the side) and the label is 1 when the bet made money and 0 when it did not. A second model trained on them learns when to act on the first model's signals and how much to bet, rather than which side to take.

The formula is as follows:

$$
\sigma_{t} = \text{the EWM standard deviation of the period returns with} \;\text{span},\;\; \text{up to } t
$$

$$
R_{t,k} = \left(\frac{p_{t+k}}{p_{t}} - 1\right) x \;\text{side}_{t},\;\; \text{for}\;\; k = 1 \ldots \;\text{horizon} \;(\text{side 1 without a side})
$$

$$
\text{upper}_{t} = \text{profit\_taking} x \sigma_{t}\;\;\text{and}\;\; \text{lower}_{t} = - \text{stop\_loss} x \sigma_{t}
$$

$$
k^{*} = \text{the first}\; k \;\text{with}\; R_{t,k} > \text{upper}_{t} \;\text{or}\; R_{t,k} < \text{lower}_{t},\;\; \text{else horizon}
$$

$$
\text{Label} = 1 \;(\text{upper}),\;\; \text{-1 (lower) or } \operatorname{sign} (R_{t,k}^{*}) \text{ (vertical)};\;\; \text{with a side 1 when}\; R_{t,k} \cdot > 0,\;\; \text{else 0}
$$

Labels look forward by construction: the label of a date describes the prices after it, up to `horizon` periods later, and is only known once a barrier is reached. The volatility of the barriers uses the returns up to the date only. Train a model on the labels with the features of the date itself and leave the labels' spans out of the test set (purging, see `get_label_uniqueness`).

**Also known as:** triple barrier method, triple-barrier labeling, meta-labeling, meta labels, profit-taking and stop-loss labels.

**References:**

- paper | López de Prado, M. (2018). "Advances in Financial Machine Learning." Wiley, chapter 3 (Snippets 3.1 to 3.7).
- library | Referenced against RiskLabAI's [triple_barrier](https://github.com/RiskLabAI/RiskLabAI.py/blob/v3.2.0/src/RiskLabAI/data/labeling/labeling.py#L193){:target="_blank"}
- library | Referenced against RiskLabAI's [meta_labeling](https://github.com/RiskLabAI/RiskLabAI.py/blob/v3.2.0/src/RiskLabAI/data/labeling/labeling.py#L402){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>horizon (int, optional):</u> The number of periods to the vertical barrier. Defaults to 10.
- <u>profit_taking (float, optional):</u> The multiple of the volatility of the upper barrier,
0 for no upper barrier. Defaults to 1.0.
- <u>stop_loss (float, optional):</u> The multiple of the volatility of the lower barrier, 0 for
no lower barrier. Defaults to 1.0.
- <u>span (int, optional):</u> The span of the exponentially weighted volatility. Defaults to
100, as López de Prado.
- <u>minimum_target (float, optional):</u> The volatility a date needs to exceed to be labeled.
Defaults to 0.0.
- <u>events (str &#124; pd.DataFrame &#124; None, optional):</u> The dates to label. Options are: "cusum" (the events
of the CUSUM filter of `get_event_filter` with its defaults), "z_score" (the events of its
z-score filter with its defaults), or a DataFrame per date and ticker that is non-zero on the
dates to label, such as the result of `get_event_filter` with other settings. Defaults to None,
which labels every date.
- <u>side (str &#124; pd.DataFrame &#124; None, optional):</u> The side of the bets for meta-labels: the
name of a signal of `get_signals`, such as "Moving Average Crossover" or "MACD
Crossover", whose crossovers are the bets, or a DataFrame per date and ticker of
1 (long), -1 (short) and 0 (no bet). Only the dates with a bet are labeled.
Defaults to None, which gives the triple-barrier labels themselves.
- <u>vertical_barrier_zero (bool, optional):</u> Whether a date whose vertical barrier is
reached first is labeled 0 rather than with the sign of its return. Defaults
to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The Label, Return (of the bet for meta-labels), Barrier (1 upper, -1
lower, 0 vertical), Holding Period (the periods to the barrier) and Target (the
volatility) per date, with the Side for meta-labels, a column per measure and ticker.

**Notes:**

- The holding period counts each ticker's own trading days. A date whose barriers are not
reached before the end of the data and whose vertical barrier lies beyond it has no
label yet (NaN), so the last `horizon` dates are mostly empty.
- The volatility is that of each period's return. López de Prado's Snippet 3.1 measures
the return over the bar a calendar day earlier, written for intraday bars.
- The vertical barrier lies `horizon` periods ahead, where López de Prado's Snippet 3.4
places it a number of calendar days ahead. Without a side the two multiples apply as
given, where Snippet 3.3 takes the profit-taking multiple for both barriers. The label
is that of the barrier reached first. The return of a short bet is minus the price
return, as in López de Prado's Snippet 3.7.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2024-01-01",
    end_date="2025-12-31",
)

labels = toolkit.technicals.get_triple_barrier_labels()

labels.xs("AAPL", level=1, axis="columns").dropna().tail()
```

Which returns:

| Date       |   Label |   Return |   Barrier |   Holding Period |   Target |
|:-----------|--------:|---------:|----------:|-----------------:|---------:|
| 2025-12-10 |      -1 |  -0.0168 |        -1 |                3 |   0.0143 |
| 2025-12-11 |      -1 |  -0.0223 |        -1 |                4 |   0.0142 |
| 2025-12-12 |      -1 |  -0.015  |        -1 |                1 |   0.014  |
| 2025-12-15 |      -1 |  -0.0038 |         0 |               10 |   0.0141 |
| 2025-12-16 |      -1 |  -0.01   |         0 |               10 |   0.014  |

---

## get_fixed_horizon_labels
Calculate the fixed-horizon labels: the sign of the return over the next `horizon` periods, 0 when it stays within the threshold, the most common labels of financial machine learning.

The return can be the ticker's own or relative: its excess over the mean or median return of the tickers (a cross-sectional label, for which only the ranking matters) or over the Benchmark.

The formula is as follows:

$$
r_{t} = p_{t} + \frac{\text{horizon}}{p_{t}} - 1
$$

$$
x_{t} = r_{t},\;\; \text{or } r_{t} \text{ minus the mean or median } r_{t} \text{ of the tickers, or minus the Benchmark's } r_{t}
$$

$$
\tau_{t} = \text{threshold},\;\; \text{or threshold } x \text{ } \sigma_{t} \text{ } x \text{ sqrt(horizon) when volatility scaled}
$$

$$
\text{Label} = 1 \;\text{when}\; x_{t} > \tau_{t},\;\; - 1 \;\text{when}\; x_{t} < - \tau_{t},\;\; \text{else 0}
$$

Labels look forward by construction: the label of a date is the return of the `horizon` periods after it. The volatility of a scaled threshold uses the returns up to the date only. López de Prado points out that a fixed threshold ignores the volatility, so that quiet periods are labeled 0 and volatile ones rarely, which the scaled threshold and the triple-barrier labels (`get_triple_barrier_labels`) address.

**Also known as:** fixed-time horizon labels, fixed horizon method, return labels, excess return labels, relative labels.

**References:**

- paper | López de Prado, M. (2018). "Advances in Financial Machine Learning." Wiley, section 3.2.
- paper | López de Prado, M. (2020). "Machine Learning for Asset Managers." Cambridge University Press, section 5.2.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>horizon (int, optional):</u> The number of periods ahead. Defaults to 1.
- <u>threshold (float, optional):</u> The threshold of the 0 label, a return, or a number of
volatilities when volatility scaled. Defaults to 0.0.
- <u>volatility_scaled (bool, optional):</u> Whether the threshold is a multiple of the
volatility over the horizon, $$\sigma_{t}$$ x sqrt(horizon). Defaults to False.
- <u>span (int, optional):</u> The span of the exponentially weighted volatility of a scaled
threshold. Defaults to 100.
- <u>relative_to (str &#124; None, optional):</u> What the return is measured against. Options are: "mean" (the
excess over the mean return of the tickers), "median" (the excess over the median return of the
tickers), "benchmark" (the excess over the Benchmark). Defaults to None, which labels the return
itself.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The Return (the excess return when relative), Label and Holding Period
(the horizon) per date, a column per measure and ticker.

**Notes:**

- The horizon counts each ticker's own trading days, and the last `horizon` dates have no
label.
- A relative label leaves out the Benchmark (and a Portfolio) as tickers; the mean or
median is that of the tickers with a return on the date.
- The volatility of a scaled threshold is the one known at the date, not that of the
forward returns.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "NVDA", "AMZN"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2024-01-01",
    end_date="2025-12-31",
)

labels = toolkit.technicals.get_fixed_horizon_labels(horizon=5, relative_to="mean")

labels.dropna()["Label"].tail()
```

Which returns:

| Date       |   AAPL |   MSFT |   NVDA |   AMZN |
|:-----------|-------:|-------:|-------:|-------:|
| 2025-12-17 |     -1 |     -1 |      1 |      1 |
| 2025-12-18 |     -1 |     -1 |      1 |     -1 |
| 2025-12-19 |     -1 |     -1 |      1 |      1 |
| 2025-12-22 |     -1 |     -1 |      1 |      1 |
| 2025-12-23 |      1 |      1 |     -1 |      1 |

---

## get_trend_scanning_labels
Calculate López de Prado's trend-scanning labels: the sign of the most significant linear trend in the prices after every date.

For every date it fits a linear trend to the prices of each forward window from `minimum_window` to `maximum_window` periods and takes the window whose slope is the most significant. The label is the sign of that slope and its t-value the strength of the trend. Unlike a fixed horizon, the method lets the data decide how long the trend after a date lasts, and labels the dates without a clear trend with a small t-value rather than a forced sign.

The formula is as follows:

$$
\text{for}\;\; L = \text{minimum\_window} \;\ldots \;\text{maximum\_window:} \;\text{OLS of}\; p_{t+l} = b_{0} + b_{1} x l + e,\;\; l = 0 \ldots L-1
$$

$$
t(b_{1}) = \frac{b_{1}}{\sqrt{\frac{\frac{\text{SSR}}{L - 2}}{\sum((l - \operatorname{mean}(l))^{2})}}}
$$

$$
L^{*} = \text{the}\; L \;\text{with the largest} \;\left|t(b_{1})\right|
$$

$$
\text{Label} = \operatorname{sign}(t(b_{1}) \;\text{at} \;L^{*}),\;\; \text{t-Value} = t(b_{1}) \;\text{at} \;L^{*},\;\; \text{Holding Period} = L^{*} - 1\;\;\text{and}\;\; \text{Return} = p_{t} + L \cdot - \frac{1}{p_{t}} - 1
$$

Labels look forward by construction: the label of a date describes the prices of up to `maximum_window` periods after it.

**Also known as:** trend scanning, trend-scanning method, t-value labels.

**References:**

- paper | López de Prado, M. (2020). "Machine Learning for Asset Managers." Cambridge University Press, section 5.4 (Snippets 5.1 and 5.2).
- library | Referenced against RiskLabAI's [find_trend_using_trend_scanning](https://github.com/RiskLabAI/RiskLabAI.py/blob/v3.2.0/src/RiskLabAI/data/labeling/financial_labels.py#L51){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>minimum_window (int, optional):</u> The shortest forward window in prices, at least 3.
Defaults to 5.
- <u>maximum_window (int, optional):</u> The longest forward window in prices. Defaults to 20.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The Label, t-Value, Return and Holding Period per date, a column per
measure and ticker.

**Notes:**

- The windows count each ticker's own trading days. A date gets a label once all its
windows are complete, so the last `maximum_window - 1` dates have none.
- The trend is fitted on the prices, as in López de Prado's Snippet 5.1; a tie between
windows goes to the shortest.
- The windows run up to and including `maximum_window`; the span of López de Prado's
Snippet 5.2 is a Python range, which leaves its end out.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2024-01-01",
    end_date="2025-12-31",
)

labels = toolkit.technicals.get_trend_scanning_labels()

labels.xs("MSFT", level=1, axis="columns").dropna().tail()
```

Which returns:

| Date       |   Label |   t-Value |   Return |   Holding Period |
|:-----------|--------:|----------:|---------:|-----------------:|
| 2025-11-26 |      -1 |   -2.9557 |  -0.0193 |               14 |
| 2025-11-28 |      -1 |   -3.0081 |  -0.0323 |               13 |
| 2025-12-01 |      -1 |   -2.352  |  -0.0218 |               12 |
| 2025-12-02 |      -1 |   -2.0796 |  -0.0283 |               11 |
| 2025-12-03 |       1 |    7.1482 |   0.0299 |                4 |

---

## get_tail_set_labels
Calculate the tail-set labels: per date, rank the tickers on their volatility-adjusted return over the next `horizon` periods and label the top `quantile` 1, the bottom `quantile` -1 and the rest 0.

A model trained on them learns to tell the best from the worst performers of a universe, the question a long-short portfolio asks, without being distracted by the noisy middle. The labels need a universe of tickers, such as the constituents of an index.

The formula is as follows:

$$
\text{Score}_{t} = \frac{p_{t} + \frac{\text{horizon}}{p_{t}} - 1}{\sigma_{t}},\;\; \sigma_{t} \text{ the EWM volatility up to } t \text{ (or the return itself without volatility adjustment)}
$$

$$
q = \frac{\text{rank} - 1}{N - 1},\;\; \text{the percentile rank among the } N \text{ tickers with a score}
$$

$$
\text{Label} = 1 \;\text{when}\; q \geq 1 - \text{quantile},\;\; - 1 \;\text{when}\; q \leq \text{quantile},\;\; \text{else 0}
$$

Labels look forward by construction: the score of a date is the return of the `horizon` periods after it, divided by the volatility known at the date.

The tail sets follow Huerta, Corbacho and Elkan (2013), who label the stocks with the highest and lowest volatility-adjusted returns and leave the middle out.

**Also known as:** tail sets, tail set labels, cross-sectional quantile labels.

**References:**

- paper | Huerta, R., Corbacho, F. and Elkan, C. (2013). "Nonlinear Support Vector Machines Can Systematically Identify Stocks with High and Low Future Returns." Algorithmic Finance, 2(1), 45-58.
- paper | López de Prado, M. (2020). "Machine Learning for Asset Managers." Cambridge University Press, chapter 5.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>horizon (int, optional):</u> The number of periods of the forward return. Defaults to 1.
- <u>quantile (float, optional):</u> The share of the tickers in each tail, up to 0.5. Defaults
to 0.1.
- <u>volatility_adjusted (bool, optional):</u> Whether the returns are divided by the
volatility. Defaults to True.
- <u>span (int, optional):</u> The span of the exponentially weighted volatility. Defaults to 100.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The Score and Label per date, a column per measure and ticker.

**Notes:**

- The Benchmark (and a Portfolio) are left out of the ranking; it needs at least two
tickers, and with fewer than 1 / quantile tickers each tail holds a single ticker.
- Tickers with an equal score share their average rank. A ticker exactly on the
boundary of a tail belongs to the tail on both sides.
- The forward return is labeled, adjusted by the volatility known at the date.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "META", "TSLA", "AVGO", "ORCL", "AMD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2024-01-01",
    end_date="2025-12-31",
)

labels = toolkit.technicals.get_tail_set_labels()

labels["Label"].dropna().tail()
```

Which returns:

| Date       |   AAPL |   MSFT |   NVDA |   AMZN |   GOOGL |   META |   TSLA |   AVGO |   ORCL |   AMD |
|:-----------|-------:|-------:|-------:|-------:|--------:|-------:|-------:|-------:|-------:|------:|
| 2025-12-23 |      1 |      0 |     -1 |      0 |       0 |      0 |      0 |      0 |      0 |     0 |
| 2025-12-24 |      0 |      0 |      1 |      0 |       0 |      0 |     -1 |      0 |      0 |     0 |
| 2025-12-26 |      1 |      0 |      0 |      0 |       0 |      0 |     -1 |      0 |      0 |     0 |
| 2025-12-29 |      0 |      0 |      0 |      0 |       0 |      1 |     -1 |      0 |      0 |     0 |
| 2025-12-30 |      0 |     -1 |      0 |      0 |       0 |      0 |      0 |      0 |      0 |     1 |

---

## get_matrix_flag_labels
Calculate the matrix flag labels: how closely the prices of the last `window` periods fit a bull (or bear) flag, a sharp move followed by a consolidation that chartists read as the pause before the move continues.

The window's prices are laid out as a 10 x 10 grid of their price deciles (rows) over ten consecutive parts of the window (columns), and a template of weights rewards the cells the flag passes through and penalises the others. The score is the sum of the weighted grid; with a threshold the label is 1 from that score.

The templates are those of Leigh, Modani, Purvis and Roberts (2002), "leigh_bull", and of Cervelló-Royo, Guijarro and Michniuk (2015), "cervello_royo_bull", who proposed a flag whose weights are concentrated in the consolidation. The bear templates are the bull templates upside down, the highest decile becoming the lowest.

The formula is as follows:

$$
D\left[d,\; j\right] = \text{the share of the prices of part}\; j \;\text{of the window in price decile}\; d \;\text{of the whole window},\;\; \text{the highest decile in the top row}
$$

$$
\text{Score} = \sum(W \cdot D),\;\; W \text{ the template}
$$

$$
\text{Label} = 1 \;\text{when Score} \geq \text{threshold},\;\; \text{else 0}
$$

Unlike the other labels, the score looks back: it uses the prices of the window up to and including the date, so a flag is known at the close of the date.

**Also known as:** matrix flags, bull flag, bear flag, flag pattern, template matching.

**References:**

- paper | Leigh, W., Modani, N., Purvis, R. and Roberts, T. (2002). "Stock Market Trading Rule Discovery Using Technical Charting Heuristics." Expert Systems with Applications, 23(2), 155-159.
- paper | Cervelló-Royo, R., Guijarro, F. and Michniuk, K. (2015). "Stock Market Trading Rule Based on Pattern Recognition and Technical Analysis: Forecasting the DJIA Index with Intraday Data." Expert Systems with Applications, 42(14), 5963-5975.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int, optional):</u> The number of prices of the window, at least 10. Defaults to 40.
- <u>template (str, optional):</u> The template of weights. Options are: "leigh_bull" (the bull flag of
Leigh, Modani, Purvis and Roberts, 2002), "leigh_bear" (the Leigh bull flag upside down),
"cervello_royo_bull" (the bull flag of Cervelló-Royo, Guijarro and Michniuk, 2015),
"cervello_royo_bear" (the Cervelló-Royo bull flag upside down). Defaults to "leigh_bull".
- <u>threshold (float &#124; None, optional):</u> The score from which the label is 1. Defaults to
None, which returns the score only.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The Score, and the Label with a threshold, per date, a column per
measure and ticker.

**Notes:**

- The window counts each ticker's own trading days; a window that is not a multiple of
ten gives its first parts one price more.
- A price on the boundary of two deciles belongs to the lower one.
- The window ends at the date, and the scores below the threshold are labeled 0, since
a missing flag is no sign of the opposite move.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2024-01-01",
    end_date="2025-12-31",
)

flags = toolkit.technicals.get_matrix_flag_labels(threshold=2.5)

flags.xs("MSFT", level=1, axis="columns").tail()
```

Which returns:

| Date       |   Score |   Label |
|:-----------|--------:|--------:|
| 2025-12-24 |   3.25  |       1 |
| 2025-12-26 |   3.75  |       1 |
| 2025-12-29 |   4.125 |       1 |
| 2025-12-30 |   4.75  |       1 |
| 2025-12-31 |   4.125 |       1 |

---

## get_label_uniqueness
Calculate the concurrency and the average uniqueness of labels: how many labels span each date and how much of its span each label shares with others.

Labels that span several periods overlap: the triple-barrier labels of two consecutive days share most of their prices, so they are not independent observations. The concurrency of a date is the number of labels whose span includes it, and the average uniqueness of a label is the mean of one over the concurrency across its span: 1 for a label that overlaps no other and 1/10 for a label sharing its whole span with nine others. López de Prado uses it to weigh the labels, to bootstrap them in proportion to their uniqueness (sequential bootstrap) and to set the number of samples a bagging classifier draws.

The formula is as follows:

$$
c_{t} = \sum_{i} 1\left[t_{0}_{i} \leq t \leq t_{1}_{i}\right],\;\; t_{1,i} \text{ the date Holding Period periods after } t_{0,i}
$$

$$
u_{i} = \frac{\text{mean of} \;1}{c_{t}} \;\text{over}\; t_{0}_{i} \leq t \leq t_{1}_{i}
$$

Both look forward by construction, as the spans of the labels do: the uniqueness of a label depends on the labels after it.

**Also known as:** label concurrency, number of concurrent events, average uniqueness, sample uniqueness, overlapping labels.

**References:**

- paper | López de Prado, M. (2018). "Advances in Financial Machine Learning." Wiley, sections 4.3 and 4.4 (Snippets 4.1 and 4.2).
- library | Referenced against RiskLabAI's [calculate_average_uniqueness](https://github.com/RiskLabAI/RiskLabAI.py/blob/v3.2.0/src/RiskLabAI/data/weights/sample_weights.py#L71){:target="_blank"}

**Args:**

- <u>labels (pd.DataFrame &#124; None, optional):</u> Labels with a Holding Period per date and
ticker, such as the result of `get_triple_barrier_labels`,
`get_fixed_horizon_labels` or `get_trend_scanning_labels`. Defaults to None, which
uses the triple-barrier labels with their defaults.
- <u>period (str, optional):</u> The time period of the labels. Options are: "intraday" (intraday prices),
"daily" (daily prices), "weekly" (weekly prices), "monthly" (monthly prices),
"quarterly" (quarterly prices), "yearly" (yearly prices). Defaults to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The Concurrency per date and the Average Uniqueness per label date, a
column per measure and ticker.

**Notes:**

- The spans count each ticker's own trading days and include both the label's date and
the date of its barrier, as in López de Prado's Snippet 4.1.
- Dates without a label (such as the last ones, whose outcome is not known yet) count
for no span.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2024-01-01",
    end_date="2025-12-31",
)

uniqueness = toolkit.technicals.get_label_uniqueness()

uniqueness.xs("AAPL", level=1, axis="columns").dropna().tail()
```

Which returns:

| Date       |   Concurrency |   Average Uniqueness |
|:-----------|--------------:|---------------------:|
| 2025-12-10 |             5 |               0.1586 |
| 2025-12-11 |             6 |               0.1669 |
| 2025-12-12 |             7 |               0.1339 |
| 2025-12-15 |             8 |               0.4114 |
| 2025-12-16 |             5 |               0.4909 |

---

## get_sample_weights
Calculate the sample weights of labels for training a model: how much each label should count, by its uniqueness, its return or its age, as López de Prado proposes for labels that overlap.

- Return attribution: the weight by return attribution. Each period's log return is shared among the labels whose span includes it, and a label's weight is the absolute sum of its shares. Labels whose spans saw large moves, and that share them with few other labels, count most, while a label over a flat stretch counts little. The weights add up to the number of labels.
- Time decay: the weight by time decay. The weights fall linearly with the cumulative average uniqueness from 1 for the newest label to `decay` for the oldest, so that older observations count less, measured in unique information rather than in dates.

The formula is as follows, per method:

$$
\text{Return attribution:}\;\; r_{t} = \ln\left(\frac{p_{t}}{p_{t-1}}\right),\;\; w \sim \text{}_{i} = \left|\sum_{t0_i<t \leq t1_i} \frac{r_{t}}{c_{t}}\right|\;\;\text{and}\;\; w_{i} = w \sim \frac{\text{}_{i} \cdot N}{\sum_{j} w} \sim \text{}_{j},\;\; \text{with } c_{t} \text{ the concurrency}
$$

$$
\text{Time decay:}\;\; x_{i} \text{ the cumulative average uniqueness up to label } i \text{ and } X \text{ the total},\;\; \text{slope} = \frac{1 - \text{decay}}{X} \;\text{when decay} \geq 0,\;\; \text{else}\;\; \frac{1}{(\text{decay} + 1) \cdot X},\;\; \text{and}\;\; w_{i} = \max(0,\; 1 - \text{slope} \cdot X + \text{slope}\; x x_{i})
$$

The weights look forward by construction, as the spans of the labels do.

**Also known as:** sample weights, return attribution, time decay, time-decay weights.

**References:**

- paper | López de Prado, M. (2018). "Advances in Financial Machine Learning." Wiley, sections 4.6 and 4.7 (Snippets 4.10 and 4.11).
- library | Referenced against RiskLabAI's [sample_weight_absolute_return_meta_labeling](https://github.com/RiskLabAI/RiskLabAI.py/blob/v3.2.0/src/RiskLabAI/data/weights/sample_weights.py#L200){:target="_blank"}
- library | Referenced against RiskLabAI's [calculate_time_decay](https://github.com/RiskLabAI/RiskLabAI.py/blob/v3.2.0/src/RiskLabAI/data/weights/sample_weights.py#L279){:target="_blank"}

**Args:**

- <u>method (str, optional):</u> The weighting. Options are: "return" (return attribution),
"time_decay" (time decay). Defaults to "return".
- <u>labels (pd.DataFrame &#124; None, optional):</u> Labels with a Holding Period per date and
ticker, such as the result of `get_triple_barrier_labels`,
`get_fixed_horizon_labels` or `get_trend_scanning_labels`. Defaults to None, which
uses the triple-barrier labels with their defaults.
- <u>decay (float, optional):</u> The weight of the oldest label of "time_decay", in (-1, 1]: 1
for no decay, 0 for a decay to zero and a negative value to give the oldest share
(-decay) of the labels no weight. Defaults to 1.0.
- <u>period (str, optional):</u> The time period of the labels. Options are: "intraday" (intraday prices),
"daily" (daily prices), "weekly" (weekly prices), "monthly" (monthly prices),
"quarterly" (quarterly prices), "yearly" (yearly prices). Defaults to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The weight of the label at each date, a column per ticker.

**Notes:**

- The weights are calculated per ticker, over the labels from the start date of the
Toolkit, so each ticker's weights add up to its number of labels ("return").
- López de Prado's Snippet 4.10 also adds the return into the label's date,
the period before the label starts; the sum here starts after it, with the returns the
label earns.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2024-01-01",
    end_date="2025-12-31",
)

weights = toolkit.technicals.get_sample_weights()

weights.dropna().tail()
```

Which returns:

| Date       |   AAPL |   MSFT |   Benchmark |
|:-----------|-------:|-------:|------------:|
| 2025-12-10 | 0.3814 | 1.1291 |      0.3261 |
| 2025-12-11 | 0.5911 | 1.0596 |      0.4031 |
| 2025-12-12 | 0.326  | 0.7975 |      0.6633 |
| 2025-12-15 | 0.1058 | 0.7868 |      0.5882 |
| 2025-12-16 | 0.7306 | 0.6239 |      0.4716 |

---

## get_bet_sizes
Calculate López de Prado's bet size for meta-labelled bets: how much of the budget to put on each date, from -1 (fully short) to 1 (fully long).

It follows from the sides of the bets a primary model takes and, for the probability bet size, how often its bets have paid off. A model that only says which side to take does not say how much to bet; sizing the bets keeps a strategy from betting the same on a weak signal as on a strong one.

- Budget bet size: the open long bets as a share of the most long bets ever open, minus the same share of the short bets, a size that spreads the budget over the bets the strategy usually has open.
- Reserve bet size: the net number of open bets (long minus short) against how many the strategy usually has open, through a mixture of two normal distributions fitted to it with the EF3M algorithm (López de Prado and Foreman, 2014). An unusually large net count gives a bet close to 1 and a usual one a small bet, keeping a reserve for stronger signals.
- Probability bet size: every bet sized by the probability that it pays off, taken as the hit rate of the bets closed before it was placed (the share whose meta-label is 1), and the sizes averaged over the bets still open. A hit rate of 50% or less gives no bet.

The formula is as follows, per method:

- Long Bets_t and Short Bets_t, the bets open on t: placed on or before t and closing after t, `Holding Period` periods after they were placed

$$
\text{Budget bet size:}\;\; m_{t} = \frac{\text{Long Bets}_{t}}{\max(\text{Long Bets})} - \frac{\text{Short Bets}_{t}}{\max(\text{Short Bets})}
$$

$$
\text{Reserve bet size:}\;\; c_{t} = \text{Long Bets}_{t} - \text{Short Bets}_{t},\;\; F \text{ the mixture of two normal distributions that matches the first five moments of } c_{t} \text{ on the dates bets are placed},\;\; \text{and}\;\; m_{t} = \frac{F(c_{t}) - F(0)}{1 - F(0)} \;\text{when}\; c_{t} \geq 0,\;\; \frac{F(c_{t}) - F(0)}{F(0)} \;\text{otherwise}
$$

$$
\text{Probability bet size:}\;\; p = \text{the hit rate known when bet}\; i \;\text{is placed},\;\; z_{i} = \frac{p - 0.5}{\sqrt{p \cdot (1 - p)}}\;\;\text{and}\;\; m_{i} = \text{side}_{i} \cdot (2 \cdot N(z_{i}) - 1) \;\text{when}\; p > 0.5,\;\; \text{else 0};\;\; m_{t} = \text{the average of}\; m_{i} \;\text{over the bets open on}\; t \;(0 \;\text{without an open bet})
$$

$$
\text{with a step\_size:}\;\; m^{*}_{t} = \operatorname{round}\left(\frac{m_{t}}{\text{step\_size}}\right) x \text{step\_size},\;\; \text{capped at -1 and 1}
$$

Where N is the standard normal distribution function. The bets come from the meta-labels: the Side is the side of a bet, the Holding Period the periods until it closes at a barrier and the Label (1 or 0) whether it made money.

**Also known as:** bet sizing, position sizing from meta-labels, budget bet size, reserve bet size, EF3M, bet size from predicted probabilities.

**References:**

- paper | López de Prado, M. (2018). "Advances in Financial Machine Learning." Wiley, chapter 10 (Snippets 10.1 to 10.3).
- paper | López de Prado, M. and Foreman, M. (2014). "A mixture of two Gaussians approach to mathematical portfolio oversight: the EF3M algorithm." Quantitative Finance, 14(5), 913-930.
- library | Referenced against RiskLabAI's [probability_bet_size](https://github.com/RiskLabAI/RiskLabAI.py/blob/v3.2.0/src/RiskLabAI/backtest/bet_sizing.py#L33){:target="_blank"}
- library | Referenced against RiskLabAI's [avg_active_signals](https://github.com/RiskLabAI/RiskLabAI.py/blob/v3.2.0/src/RiskLabAI/backtest/bet_sizing.py#L166){:target="_blank"}

**Args:**

- <u>method (str, optional):</u> The bet size. Options are: "budget" (the budget bet size), "reserve" (the
reserve bet size), "probability" (the probability bet size). Defaults to "budget".
- <u>labels (pd.DataFrame &#124; None, optional):</u> Meta-labels with a Side, Holding Period and
Label per date and ticker, such as the result of `get_triple_barrier_labels` with a
side. Defaults to None, which uses the triple-barrier meta-labels of the CUSUM
filter's events with the direction of each event as the side (a trend-following
primary model) and the other defaults.
- <u>step_size (float &#124; None, optional):</u> The step the bet sizes are rounded to, between 0
and 1, so small changes of the size do not trade. Defaults to None, which keeps
them unrounded.
- <u>minimum_labels (int, optional):</u> The number of closed bets the hit rate of
"probability" needs before it sizes a bet; earlier bets are left out. Defaults
to 20.
- <u>runs (int, optional):</u> The number of random starting points of the EF3M fit of
"reserve". Defaults to 100.
- <u>seed (int, optional):</u> The seed of the starting points of the EF3M fit. Defaults to 0.
- <u>period (str, optional):</u> The time period of the labels. Options are: "intraday" (intraday prices),
"daily" (daily prices), "weekly" (weekly prices), "monthly" (monthly prices),
"quarterly" (quarterly prices), "yearly" (yearly prices). Defaults to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The Long Bets, Short Bets and Bet Size per date, with the Hit Rate for
"probability", a column per measure and ticker.

**Notes:**

- The bets are those whose barrier was reached; a bet still open at the end of the data
has no Holding Period yet and is left out.
- A bet counts from the date it is placed up to, but not including, the date it closes.
The "budget" maximum and the "reserve" fit cover each ticker's whole sample, as in
López de Prado, so like the labels themselves they describe the bets of the sample
rather than a size known on the date. The hit rate of "probability" uses only the bets
closed by the date.
- The "reserve" fit solves the five moment equations of EF3M with Powell's hybrid method
from EF3M's random starting points rather than with EF3M's fixed-point iteration, whose
solution is often a repelling point it cannot reach, so where it stops differs per
seed. Here every seed reaches the same exact solution, so `seed` only matters when
the moments allow several.
- "probability" sizes the bets with the hit rate of the past bets as the predicted
probability, a simple secondary model; `bet_sizing_model.get_probability_bet_size`
takes the probabilities of a classifier of your own.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2024-01-01",
    end_date="2025-12-31",
)

bet_sizes = toolkit.technicals.get_bet_sizes(method="reserve")

bet_sizes.xs("AAPL", level=1, axis="columns").tail()
```

Which returns:

| Date       |   Long Bets |   Short Bets |   Bet Size |
|:-----------|------------:|-------------:|-----------:|
| 2025-12-24 |           0 |            1 |     -0.534 |
| 2025-12-26 |           0 |            1 |     -0.534 |
| 2025-12-29 |           0 |            1 |     -0.534 |
| 2025-12-30 |           0 |            0 |      0     |
| 2025-12-31 |           0 |            0 |      0     |

---

## collect_momentum_indicators
Collect the momentum indicators of every ticker in one table: how fast and how strongly the prices move, and whether they are overbought or oversold.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>window (int, optional):</u> The window size for calculating indicators.
Defaults to 14.
- <u>close_column (str, optional):</u> The name of the column containing the close prices.
Defaults to "Adj Close".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: Momentum indicators calculated based on the specified parameters.

**Notes:**

- The method calculates various momentum indicators for each asset in the Toolkit instance.
- When growth is requested, the method calculates the growth of the indicator values
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.collect_momentum_indicators().xs("AAPL", level=1, axis="columns")
```

Which returns:

| Date       |   Money Flow Index |   Williams %R |   Aroon Indicator Up |   Aroon Indicator Down |   Aroon Oscillator |   Commodity Channel Index |   Relative Vigor Index |   Relative Vigor Index Signal Line |       Force Index |   Ultimate Oscillator |   Percentage Price Oscillator |   Percentage Price Oscillator Signal Line |   Percentage Price Oscillator Histogram |   Absolute Price Oscillator |   Percentage Volume Oscillator |   Percentage Volume Oscillator Signal Line |   Percentage Volume Oscillator Histogram |   Detrended Price Oscillator |   Average Directional Index |   Plus Directional Movement |   Minus Directional Movement |   Plus Directional Indicator |   Minus Directional Indicator |   Directional Movement Index |   Average Directional Index Rating |   Chande Momentum Oscillator |   Intraday Momentum Index |   Ichimoku Conversion Line |   Ichimoku Base Line |   Ichimoku Leading Span A |   Ichimoku Leading Span B |   Stochastic %K |   Stochastic %D |   MACD Line |   MACD Signal Line |   MACD Histogram |   Relative Strength Index |   Stochastic RSI %K |   Stochastic RSI %D |   True Strength Index |   True Strength Index Signal Line |   Balance of Power |   Internal Bar Strength |   Qstick |   Awesome Oscillator |   Accelerator Oscillator |   Vortex Indicator VI+ |   Vortex Indicator VI- |   Elder Ray Bull Power |   Elder Ray Bear Power |   Rate of Change |   Momentum |   Choppiness Index |   Efficiency Ratio |   Vertical Horizontal Filter |   Know Sure Thing |   Know Sure Thing Signal Line |   Coppock Curve |   Fisher Transform |   Fisher Transform Trigger |   Inverse Fisher Transform RSI |   KDJ K |   KDJ D |   KDJ J |   Premier Stochastic Oscillator |   Stochastic Momentum Index |   Stochastic Momentum Index Signal Line |   SMI Ergodic Indicator |   SMI Ergodic Signal Line |   SMI Ergodic Oscillator |   Schaff Trend Cycle |   WaveTrend |   WaveTrend Signal Line |   Derivative Oscillator |   Swing Index |   Accumulative Swing Index |     QQE |   QQE RSI Moving Average |   Dynamic Momentum Index |   Price Zone Oscillator |   Connors RSI |   Inertia |    Bias |   BRAR AR |   BRAR BR |   Pretty Good Oscillator |   Psychological Line |   Volatility-Based Momentum |   AMAT Long Run |   AMAT Short Run |   TTM Trend |   Correlation Trend Indicator |   Forecast Oscillator |   Projection Oscillator |
|:-----------|-------------------:|--------------:|---------------------:|-----------------------:|-------------------:|--------------------------:|-----------------------:|-----------------------------------:|------------------:|----------------------:|------------------------------:|------------------------------------------:|----------------------------------------:|----------------------------:|-------------------------------:|-------------------------------------------:|-----------------------------------------:|-----------------------------:|----------------------------:|----------------------------:|-----------------------------:|-----------------------------:|------------------------------:|-----------------------------:|-----------------------------------:|-----------------------------:|--------------------------:|---------------------------:|---------------------:|--------------------------:|--------------------------:|----------------:|----------------:|------------:|-------------------:|-----------------:|--------------------------:|--------------------:|--------------------:|----------------------:|----------------------------------:|-------------------:|------------------------:|---------:|---------------------:|-------------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------:|-----------:|-------------------:|-------------------:|-----------------------------:|------------------:|------------------------------:|----------------:|-------------------:|---------------------------:|-------------------------------:|--------:|--------:|--------:|--------------------------------:|----------------------------:|----------------------------------------:|------------------------:|--------------------------:|-------------------------:|---------------------:|------------:|------------------------:|------------------------:|--------------:|---------------------------:|--------:|-------------------------:|-------------------------:|------------------------:|--------------:|----------:|--------:|----------:|----------:|-------------------------:|---------------------:|----------------------------:|----------------:|-----------------:|------------:|------------------------------:|----------------------:|------------------------:|
| 2025-12-17 |            39.7393 |      -98.8222 |              28.5714 |               100      |           -71.4286 |                 -139.905  |                -0.2262 |                            -0.0758 |      -3.27416e+07 |               44.5331 |                        0.0063 |                                    0.0116 |                                 -0.0053 |                      1.7262 |                        -0.0329 |                                    -0.0509 |                                   0.018  |                       0.0306 |                     24.6713 |                     12.185  |                      13.7577 |                      17.868  |                       20.1742 |                       6.0622 |                            27.6362 |                     -20.6209 |                   41.1264 |                    275.43  |              276.008 |                   265.041 |                   250.519 |          1.1778 |          8.6605 |      1.7262 |             3.1596 |          -1.4334 |                   45.1866 |              0      |              1.2037 |               12.3225 |                           19.7487 |            -0.7013 |                  0.0442 |  -0.4015 |               1.2653 |                  -1.836  |                 0.9211 |                 1.0533 |                -0.1328 |                -4.6371 |          -0.0206 |    -5.6902 |            49.8427 |             0.2062 |                       0.5182 |            0.3638 |                        0.5107 |          0.0029 |            -2.2385 |                    -1.8906 |                        -0.8927 | 15.8397 | 25.2454 | -2.9718 |                         -0.84   |                      9.1395 |                                 26.1148 |                 -6.2668 |                    4.4051 |                 -10.6719 |               1.3165 |     -2.5415 |                 12.0151 |                 -6.9465 |      -38.8013 |                    5877.92 | 57.4732 |                  50.8734 |                  13.8158 |                -14.5643 |       20.1105 |   51.7715 | -0.014  |  131.997  |  121.214  |                  -1.3452 |              33.3333 |                     -2.243  |               0 |                1 |          -1 |                       -0.8216 |               -0.013  |                  0.2466 |
| 2025-12-18 |            34.4002 |      -75.8192 |              21.4286 |               100      |           -78.5714 |                 -162.428  |                -0.2832 |                            -0.1659 |      -2.59752e+07 |               50.9808 |                        0.0047 |                                    0.0102 |                                 -0.0055 |                      1.2731 |                        -0.0132 |                                    -0.0434 |                                   0.0302 |                      -0.3822 |                     24.4324 |                     11.3147 |                      17.4488 |                      16.1683 |                       24.9338 |                      21.3261 |                            28.0928 |                     -24.9064 |                   36.3175 |                    272.6   |              276.008 |                   265.041 |                   250.519 |         24.1808 |         14.0381 |      1.2731 |             2.7823 |          -1.5092 |                   45.9182 |              2.4336 |              2.0149 |                9.3441 |                           17.1476 |            -0.2126 |                  0.7844 |  -0.6157 |               0.0099 |                  -2.1487 |                 0.865  |                 1.0802 |                -2.0699 |                -8.7267 |          -0.0239 |    -6.6369 |            42.7375 |             0.2491 |                       0.5366 |            0.311  |                        0.4834 |         -0.014  |            -2.6249 |                    -2.2385 |                        -0.9368 | 23.7921 | 24.761  | 21.8543 |                         -0.8426 |                      3.2693 |                                 21.5457 |                -10.1477 |                   -0.4458 |                  -9.7019 |               0.6582 |    -12.4226 |                  2.2173 |                 -7.2145 |      -12.5266 |                    5865.39 | 55.8771 |                  49.2217 |                  15.5532 |                  0.5149 |       46.5574 |   50.526  | -0.0123 |  108.702  |  105.088  |                  -1.1882 |              33.3333 |                     -2.7539 |               0 |                1 |          -1 |                       -0.9297 |               -0.003  |                  0.5333 |
| 2025-12-19 |            43.3299 |      -68.989  |              14.2857 |                92.8571 |           -78.5714 |                 -103.239  |                -0.2694 |                            -0.2349 |       5.93143e+06 |               51.5414 |                        0.0037 |                                    0.0089 |                                 -0.0052 |                      1.0212 |                         0.1453 |                                    -0.0056 |                                   0.1509 |                      -0.4186 |                     23.9078 |                     11.4732 |                      16.2024 |                      16.469  |                       23.2575 |                      17.0882 |                            28.6043 |                     -39.3401 |                   28.2097 |                    272.6   |              276.008 |                   265.041 |                   250.519 |         31.011  |         18.7898 |      1.0212 |             2.4301 |          -1.4089 |                   49.0174 |             12.7427 |              5.0588 |                7.6467 |                           14.7723 |             0.3234 |                  0.8021 |  -0.8698 |              -1.1188 |                  -2.2692 |                 0.903  |                 1.137  |                -0.8132 |                -5.4969 |          -0.0333 |    -9.3972 |            41.2482 |             0.3934 |                       0.5987 |            0.2645 |                        0.4504 |         -0.0269 |            -2.3555 |                    -2.6249 |                        -0.9292 | 32.8313 | 27.4511 | 43.5917 |                         -0.7977 |                     -0.9462 |                                 17.0473 |                 -9.7979 |                   -3.5632 |                  -6.2347 |               0.3291 |    -16.4302 |                 -6.2154 |                 -6.63   |       14.9273 |                    5880.32 | 55.8245 |                  49.1536 |                  57.0396 |                 13.6936 |       64.4303 |   49.4718 | -0.007  |  113.263  |  110.127  |                  -0.7701 |              41.6667 |                     -2.0674 |               0 |                1 |          -1 |                       -0.9192 |                0.0092 |                  0.7123 |
| 2025-12-22 |            36.4312 |      -81.4487 |               7.1429 |                85.7143 |           -78.5714 |                 -104.733  |                -0.2367 |                            -0.2614 |      -7.97965e+06 |               45.7604 |                        0.0022 |                                    0.0076 |                                 -0.0054 |                      0.5976 |                         0.1018 |                                     0.0158 |                                   0.0859 |                       2.2593 |                     23.4207 |                     10.6537 |                      15.0451 |                      15.6562 |                       22.1097 |                      17.0882 |                            29.1456 |                     -64.5455 |                   17.6515 |                    272.6   |              276.008 |                   264.954 |                   250.519 |         18.5513 |         24.581  |      0.5976 |             2.0636 |          -1.466  |                   44.0574 |              0      |              5.0588 |                4.6682 |                           12.2463 |            -0.5608 |                  0.1365 |  -1.2314 |              -2.0902 |                  -2.1525 |                 0.8075 |                 1.2147 |                -0.8978 |                -4.2561 |          -0.0532 |   -15.1671 |            40.4149 |             0.6455 |                       0.5589 |            0.2055 |                        0.4111 |         -0.0418 |            -2.0419 |                    -2.3555 |                        -0.9498 | 32.0392 | 28.9805 | 38.1567 |                         -0.7692 |                     -4.8407 |                                 12.6697 |                -13.7773 |                   -6.9679 |                  -6.8094 |               0.1646 |    -20.9318 |                -13.0815 |                 -6.456  |      -45.6961 |                    5834.63 | 54.1419 |                  47.4549 |                  37.2576 |                 -1.2512 |       20.8244 |   48.1033 | -0.0165 |  110.181  |  102.622  |                  -1.0926 |              41.6667 |                     -1.9446 |               0 |                1 |          -1 |                       -0.9246 |                0.0011 |                  0.5069 |
| 2025-12-23 |            37.2984 |      -69.5725 |               0      |                78.5714 |           -78.5714 |                  -97.9344 |                -0.205  |                            -0.2501 |      -1.44128e+06 |               49.1967 |                        0.0014 |                                    0.0063 |                                 -0.005  |                      0.3694 |                         0.0548 |                                     0.0236 |                                   0.0311 |                       2.351  |                     23.1944 |                      9.8927 |                      14.9172 |                      14.9624 |                       22.5619 |                      20.2521 |                            28.9735 |                     -51.4169 |                   23.8077 |                    272.6   |              276.008 |                   265.083 |                   250.519 |         30.4275 |         26.6632 |      0.3694 |             1.7248 |          -1.3553 |                   47.029  |             15.5282 |              9.4236 |                3.0048 |                            9.9359 |             0.517  |                  0.9524 |  -0.9773 |              -2.6623 |                  -1.7431 |                 0.7732 |                 1.2661 |                -1.9284 |                -4.8582 |          -0.0415 |   -11.7491 |            46.4518 |             0.5142 |                       0.4243 |            0.1522 |                        0.3663 |         -0.0501 |            -1.9612 |                    -2.0419 |                        -0.9406 | 35.0211 | 30.994  | 43.0753 |                         -0.727  |                     -6.7949 |                                  8.7768 |                -13.4496 |                   -9.1285 |                  -4.3211 |               0.0823 |    -24.6243 |                -18.6022 |                 -5.7342 |       12.4911 |                    5847.12 | 53.9827 |                  47.3129 |                  56.8024 |                 12.1426 |       57.2709 |   47.6333 | -0.0114 |  105.311  |  103.415  |                  -0.6584 |              50      |                     -1.3037 |               0 |                1 |          -1 |                       -0.9141 |                0.0076 |                  0.7178 |
| 2025-12-24 |            41.6581 |      -51.6561 |               0      |                71.4286 |           -71.4286 |                  -34.6705 |                -0.1841 |                            -0.2228 |       2.20161e+06 |               54.4448 |                        0.0011 |                                    0.0053 |                                 -0.0042 |                      0.3017 |                        -0.0045 |                                     0.018  |                                  -0.0225 |                       3.0907 |                     22.018  |                     12.1059 |                      13.8517 |                      18.736  |                       21.4379 |                       6.7256 |                            28.2487 |                     -32.919  |                   31.7545 |                    272.6   |              276.008 |                   265.063 |                   250.519 |         48.3439 |         32.4409 |      0.3017 |             1.4402 |          -1.1385 |                   50.0121 |             38.5455 |             18.0246 |                2.4525 |                            8.0651 |             0.4551 |                  0.4985 |  -0.6307 |              -2.8188 |                  -1.0827 |                 0.8892 |                 1.1613 |                 1.0804 |                -2.1383 |          -0.0245 |    -6.8661 |            53.1324 |             0.3292 |                       0.3731 |            0.1033 |                        0.3168 |         -0.0518 |            -1.5593 |                    -1.9612 |                        -0.8894 | 40.6707 | 34.2196 | 53.573  |                         -0.6448 |                     -7.0164 |                                  5.6181 |                -10.3613 |                   -9.5394 |                  -0.8219 |               0.0411 |    -22.4462 |                -21.1081 |                 -4.3189 |       36.2295 |                    5883.35 | 53.9827 |                  48.2126 |                  42.5356 |                 23.8305 |       67.2632 |   47.9699 | -0.0071 |  112.863  |  120.363  |                  -0.2751 |              58.3333 |                     -0.8397 |               0 |                1 |           1 |                       -0.852  |                0.0123 |                  0.8331 |
| 2025-12-26 |            46.9441 |      -51.1363 |               0      |                64.2857 |           -64.2857 |                  -25.6932 |                -0.1697 |                            -0.1974 |  735552           |               51.2159 |                        0.0008 |                                    0.0044 |                                 -0.0036 |                      0.2126 |                        -0.0488 |                                     0.0046 |                                  -0.0534 |                      -0.6819 |                     20.9257 |                     11.2412 |                      12.8623 |                      17.9861 |                       20.58   |                       6.7256 |                            27.2889 |                     -27.7033 |                   33.1185 |                    272.6   |              276.098 |                   264.961 |                   250.519 |         48.8637 |         42.545  |      0.2126 |             1.1946 |          -0.982  |                   49.1689 |             34.6217 |             29.5651 |                1.7619 |                            6.4893 |            -0.3028 |                  0.2151 |  -0.5595 |              -2.1658 |                   0.0054 |                 0.9091 |                 1.1011 |                 1.1553 |                -1.346  |          -0.0193 |    -5.3614 |            55.49   |             0.277  |                       0.4022 |            0.0564 |                        0.2631 |         -0.0522 |            -1.1484 |                    -1.5593 |                        -0.8224 | 43.4017 | 37.2803 | 55.6445 |                         -0.4625 |                     -6.9074 |                                  3.113  |                 -9.0825 |                   -9.3871 |                   0.3046 |               0.0206 |    -20.284  |                -22.0716 |                 -2.8918 |       -3.8045 |                    5879.54 | 53.9827 |                  48.5314 |                  33.7903 |                  7.3734 |       39.8837 |   48.2486 | -0.0094 |  120.453  |  119.909  |                  -0.284  |              58.3333 |                     -0.7927 |               1 |                0 |           1 |                       -0.7986 |                0.0095 |                  0.7973 |
| 2025-12-29 |            48.1203 |      -48.4089 |              35.7143 |                57.1429 |           -21.4286 |                  -30.5671 |                -0.1563 |                            -0.1782 |       1.7719e+06  |               57.3149 |                        0.0006 |                                    0.0036 |                                 -0.003  |                      0.169  |                        -0.0817 |                                    -0.0126 |                                  -0.0691 |                       0.1103 |                     20.0593 |                     10.4382 |                      12.4518 |                      17.3861 |                       20.7398 |                       8.7965 |                            26.5057 |                     -21.8633 |                   36.4164 |                    270.612 |              276.183 |                   265.068 |                   250.519 |         51.5911 |         49.5995 |      0.169  |             0.9895 |          -0.8205 |                   49.9666 |             40.0245 |             37.7306 |                1.4003 |                            5.217  |             0.5323 |                  0.7015 |  -0.4662 |              -2.0654 |                   0.2951 |                 0.9316 |                 1.0955 |                 0.2129 |                -1.7901 |          -0.0149 |    -4.1157 |            54.4742 |             0.2186 |                       0.4134 |            0.0118 |                        0.2104 |         -0.0496 |            -0.8195 |                    -1.1484 |                        -0.6882 | 53.5816 | 42.714  | 75.3166 |                         -0.1913 |                     -6.4822 |                                  1.194  |                 -7.5042 |                   -8.7594 |                   1.2553 |               0.0103 |    -19.6328 |                -21.7468 |                 -1.5792 |        5.5886 |                    5885.13 | 53.9827 |                  49.0098 |                  34.5775 |                 19.7029 |       57.1631 |   49.2247 | -0.0088 |  110.988  |  114.995  |                  -0.1531 |              58.3333 |                     -1.0766 |               1 |                0 |           1 |                       -0.7244 |                0.0103 |                  0.854  |
| 2025-12-30 |            43.4593 |      -53.5607 |              28.5714 |                50      |           -21.4286 |                  -35.5284 |                -0.1288 |                            -0.1608 | -464807           |               54.1042 |                        0.0003 |                                    0.003  |                                 -0.0027 |                      0.0788 |                        -0.1122 |                                    -0.0325 |                                  -0.0797 |                      -2.3582 |                     19.2762 |                      9.6926 |                      11.6321 |                      16.8441 |                       20.2146 |                       9.095  |                            25.712  |                     -21.7389 |                   38.6752 |                    270.612 |              276.183 |                   265.068 |                   250.519 |         46.4393 |         48.9647 |      0.0788 |             0.8074 |          -0.7285 |                   48.4209 |             29.5551 |             34.7338 |                0.6843 |                            4.0838 |             0.15   |                  0.4444 |  -0.3773 |              -1.9448 |                   0.3866 |                 0.9145 |                 1.1096 |                 0.0857 |                -1.708  |          -0.0148 |    -4.0858 |            53.5704 |             0.2174 |                       0.4141 |           -0.0182 |                        0.1612 |         -0.0465 |            -0.4022 |                    -0.8195 |                        -0.6065 | 57.9069 | 47.7783 | 78.1641 |                          0.0877 |                     -6.3714 |                                 -0.3191 |                 -7.7102 |                   -8.4097 |                   0.6995 |               0.0051 |    -20.2725 |                -20.6589 |                 -0.7486 |       -3.2998 |                    5881.83 | 53.9827 |                  48.8135 |                  50.5959 |                  3.8001 |       36.7617 |   50.4639 | -0.0122 |  113.905  |  105.452  |                  -0.2379 |              58.3333 |                     -1.0873 |               0 |                1 |           1 |                       -0.6718 |                0.0069 |                  0.7814 |
| 2025-12-31 |            38.2003 |      -62.8029 |              21.4286 |                42.8571 |           -21.4286 |                  -56.9136 |                -0.0887 |                            -0.1381 |      -4.82705e+06 |               46.4079 |                       -0.0003 |                                    0.0023 |                                 -0.0026 |                     -0.0897 |                        -0.1258 |                                    -0.0512 |                                  -0.0746 |                      -1.5169 |                     18.7176 |                      9.0003 |                      11.3294 |                      16.2589 |                       20.4663 |                      11.4565 |                            24.6539 |                     -37.4456 |                   34.0262 |                    270.248 |              276.821 |                   265.6   |                   250.867 |         37.1971 |         45.0758 |     -0.0897 |             0.628  |          -0.7176 |                   45.6902 |             12.0094 |             27.1964 |               -0.6702 |                            2.8953 |            -0.6218 |                  0.057  |  -0.536  |              -1.6049 |                   0.515  |                 0.9113 |                 1.1148 |                -0.0091 |                -1.9324 |          -0.0248 |    -6.896  |            52.5944 |             0.3745 |                       0.3956 |           -0.0452 |                        0.1157 |         -0.0431 |            -0.1073 |                    -0.4022 |                        -0.6548 | 57.905  | 51.1539 | 71.4071 |                          0.1423 |                     -7.1079 |                                 -1.6769 |                -10.1732 |                   -8.9975 |                  -1.1757 |               0.0026 |    -23.361  |                -20.8876 |                 -0.6816 |      -19.3794 |                    5862.45 | 53.9827 |                  47.7724 |                  43.3308 |                 -9.9432 |       24.882  |   52.0466 | -0.0166 |   99.0847 |   92.3301 |                  -0.3998 |              50      |                     -1.4421 |               0 |                1 |          -1 |                       -0.6071 |                0.0023 |                  0.6255 |

---

## get_money_flow_index
Calculate the Money Flow Index (MFI): how strongly money flows into or out of a security, using price and volume.

The Money Flow Index is a momentum indicator that measures the strength and direction of money flowing in and out of a security by considering both price and volume.

The formula is as follows:

$$
\text{MFI} = 100 - \frac{100}{1 + \frac{\text{positive\_money\_flow}}{\text{negative\_money\_flow}}}
$$

**Also known as:** MFI, volume-weighted RSI.

**References:**

- paper | Quong, G. & Soudack, A. (1989). "Volume-Weighted RSI: Money Flow." Technical Analysis of Stocks & Commodities, 7(3), 76-77.
- library | Referenced against TA-Lib's [MFI](https://ta-lib.org/functions/mfi.html){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The name of the column containing the close prices.
Defaults to "Adj Close", in which case the open, high and low prices are adjusted
for dividends in the same way.
- <u>window (int, optional):</u> The number of periods for calculating the MFI.
Defaults to 14.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: Money Flow Index (MFI) values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the MFI values for each asset in the Toolkit instance.
- The MFI agrees with TA-Lib's MFI.
- When growth is requested, the method calculates the growth of the indicator values
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["^IXIC"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_money_flow_index().tail(5)
```

Which returns:

| Date       |   ^IXIC |   Benchmark |
|:-----------|--------:|------------:|
| 2025-12-24 | 49.2154 |     53.8187 |
| 2025-12-26 | 47.7867 |     52.3146 |
| 2025-12-29 | 48.6922 |     51.9588 |
| 2025-12-30 | 48.8975 |     52.4467 |
| 2025-12-31 | 42.2704 |     45.3999 |

---

## get_williams_percent_r
Calculate the Williams Percent R (Williams %R): where the close lies within the high-low range of a window, from 0 (at the high) to -100 (at the low), to show overbought and oversold levels.

The Williams %R is a momentum indicator that measures the level of the close price relative to the high-low range over a certain number of periods.

The formula is as follows:

$$
\text{Williams}\; \%R = \frac{\text{Highest High} - \text{Close}}{\text{Highest High} - \text{Lowest Low}} \cdot - 100
$$

**Also known as:** Williams percent R, overbought oversold oscillator.

**References:**

- paper | Williams, L.R. (1973). "How I Made One Million Dollars Last Year Trading Commodities." Windsor Books.
- library | Referenced against TA-Lib's [WILLR](https://ta-lib.org/functions/willr.html){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The name of the column containing the close prices.
Defaults to "Adj Close", in which case the open, high and low prices are adjusted
for dividends in the same way.
- <u>window (int, optional):</u> The number of periods for calculating the Williams %R.
Defaults to 14.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: Williams %R values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the Williams %R values for each asset in the Toolkit instance.
- Williams %R agrees with TA-Lib's WILLR.
- When growth is requested, the method calculates the growth of the indicator values
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["EURUSD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_williams_percent_r().tail(5)
```

Which returns:

| Date       |   EURUSD |   Benchmark |
|:-----------|---------:|------------:|
| 2025-12-26 | -29.4352 |     -6.0166 |
| 2025-12-28 | -39.9621 |    nan      |
| 2025-12-29 | -33.5227 |    -16.9802 |
| 2025-12-30 | -56.8182 |    -20.7239 |
| 2025-12-31 | -58.8068 |    -43.4088 |

---

## get_aroon_indicator
Calculate the Aroon Indicator: how many periods ago the highest high and the lowest low of a window were, which shows whether a trend is starting and how strong it is.

The Aroon Indicator is an oscillator that measures the strength of a trend and the likelihood of its continuation or reversal.

The formula is as follows:

$$
\text{Aroon Up} = \frac{(\text{Number of periods}) - (\text{Number of periods since highest high})}{\text{Number of periods}} \cdot 100
$$

$$
\text{Aroon Down} = \frac{(\text{Number of periods}) - (\text{Number of periods since lowest low})}{\text{Number of periods}} \cdot 100
$$

$$
\text{Aroon Oscillator} = \text{Aroon Up} - \text{Aroon Down}
$$

The Aroon Oscillator runs from -100 to 100: above zero the latest high is more recent than the latest low, which reads as an uptrend, and a reading near 100 or -100 as a strong trend.

**Also known as:** Aroon Up, Aroon Down, Aroon Oscillator, AROONOSC, trend strength.

**References:**

- paper | Chande, T.S. (1995). "The Time Price Oscillator." Technical Analysis of Stocks & Commodities, 13(9), 369-374.
- library | Referenced against TA-Lib's [AROON](https://ta-lib.org/functions/aroon.html){:target="_blank"}
- library | Referenced against TA-Lib's [AROONOSC](https://ta-lib.org/functions/aroonosc.html){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int, optional):</u> The number of periods for calculating the Aroon Indicator.
Defaults to 14.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame:
Aroon Indicator values for the upward and downward trends and the Aroon Oscillator.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the Aroon Indicator values for each asset in the Toolkit instance.
- Aroon Up and Aroon Down agree with TA-Lib's AROON, and the Aroon Oscillator TA-Lib's AROONOSC.
- When growth is requested, the method calculates the growth of the indicator values
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["GCUSD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_aroon_indicator().xs("GCUSD", level=1, axis="columns").tail(5)
```

Which returns:

| Date       |   Aroon Down |   Aroon Oscillator |   Aroon Up |
|:-----------|-------------:|-------------------:|-----------:|
| 2025-12-26 |       0      |           100      |   100      |
| 2025-12-28 |       0      |            92.8571 |    92.8571 |
| 2025-12-29 |       0      |            85.7143 |    85.7143 |
| 2025-12-30 |      14.2857 |            64.2857 |    78.5714 |
| 2025-12-31 |     100      |           -28.5714 |    71.4286 |

---

## get_commodity_channel_index
Calculate the Commodity Channel Index (CCI): how far the typical price lies from its average, in units of its mean deviation, to show cyclical turns and overbought and oversold levels.

The Commodity Channel Index is an oscillator that measures the current price level relative to an average price level over a specified period.

The formula is as follows:

$$
\text{CCI} = \frac{\text{Typical Price} - \operatorname{SMA}(\text{Typical Price})}{\text{constant} \cdot \text{Mean Deviation}}
$$

**Also known as:** CCI, cyclical trend indicator.

**References:**

- paper | Lambert, D.R. (1980). "Commodity Channel Index: Tool for Trading Cyclic Trends." Commodities, October 1980; reprinted in Technical Analysis of Stocks & Commodities, 1(5), 120-122.
- library | Referenced against TA-Lib's [CCI](https://ta-lib.org/functions/cci.html){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column in the historical data that represents
Defaults to "Adj Close", in which case the open, high and low prices are adjusted
for dividends in the same way.
- <u>window (int, optional):</u> The number of periods for calculating the CCI.
Defaults to 14.
- <u>constant (float, optional):</u> Constant multiplier used in the CCI calculation.
Defaults to 0.015.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: Commodity Channel Index (CCI) values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the CCI values for each asset in the Toolkit instance.
- With the default `constant` of 0.015, the CCI agrees with TA-Lib's CCI.
- When growth is requested, the method calculates the growth of the indicator values
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["CLUSD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_commodity_channel_index().tail(5)
```

Which returns:

| Date       |   CLUSD |   Benchmark |
|:-----------|--------:|------------:|
| 2025-12-26 | 15.2689 |    144.032  |
| 2025-12-28 | -1.512  |    nan      |
| 2025-12-29 | 51.2665 |     82.3342 |
| 2025-12-30 | 69.184  |     67.1731 |
| 2025-12-31 | 38.1997 |     13.3141 |

---

## get_relative_vigor_index
Calculate the Relative Vigor Index (RVI): how strongly the close ends above the open relative to the range, which shows the conviction behind a move.

The Relative Vigor Index measures the conviction behind a move by comparing where each period closes relative to its open with the period's full high-low range: in an uptrend prices tend to close above their open, in a downtrend below it.

The formula is as follows:

$$
\text{Numerator} = (\text{Close} - \text{Open}) \;\text{smoothed with the symmetric weights}\; 1,\; 2,\; 2,\; 1 \;\text{over the current and three prior periods},\;\; \text{divided by 6}
$$

$$
\text{Denominator} = (\text{High} - \text{Low}) \;\text{smoothed with the same weights}
$$

$$
\text{RVI} = \frac{\operatorname{SMA}(\text{Numerator},\; \text{window})}{\operatorname{SMA}(\text{Denominator},\; \text{window})}
$$

$$
\text{Signal Line} = \text{RVI smoothed with the same symmetric weights}
$$

The RVI usually lies between -1 and 1 and is positive when closes sit above opens. Crossovers of the RVI and its signal line are the usual trigger, and a divergence from price warns that a move lacks conviction. See `momentum_model.get_relative_vigor_index` for the full formula.

**Also known as:** RVI, RVGI, vigor index.

**References:**

- paper | Ehlers, J.F. (2002). "Relative Vigor Index." Technical Analysis of Stocks & Commodities, 20(1), 16-20.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column in the historical data that represents
the closing prices. Defaults to "Adj Close", in which case the open, high and
low prices are adjusted for dividends in the same way.
- <u>window (int, optional):</u> The number of periods for the averages of the numerator
and denominator. Defaults to 10, Ehlers' setting.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: Relative Vigor Index and Signal Line values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the RVI values for each asset in the Toolkit instance.
- When growth is requested, the method calculates the growth of the indicator values
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["^HSI"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_relative_vigor_index().xs("^HSI", level=1, axis="columns").tail(5)
```

Which returns:

| Date       |   Relative Vigor Index |   Signal Line |
|:-----------|-----------------------:|--------------:|
| 2025-12-24 |                -0.0322 |       -0.0822 |
| 2025-12-26 |               nan      |      nan      |
| 2025-12-29 |                -0.0004 |       -0.0522 |
| 2025-12-30 |                -0.0074 |       -0.0247 |
| 2025-12-31 |                -0.03   |       -0.013  |

---

## get_force_index
Calculate the Force Index or the Cumulative Force Index (CFI): the price change times the volume, smoothed (and added up over time for the CFI), which shows the force of the buyers or sellers behind a move.

The Force Index of Elder measures the strength behind price movements: each period's change in price times its volume, smoothed with an exponential moving average. The Cumulative Force Index is its running total. Where On-Balance Volume adds the whole volume of an up close however small the move, the force weights the volume with the size of the move, so a heavy session that barely moves price adds little. With a window of 1 there is no smoothing and the Cumulative Force Index is the Weighted On-Balance Volume.

The formula for the Force Index is as follows:

$$
\text{Raw Force Index} = (\text{Close} - \operatorname{Close}(1)) \cdot \text{Volume}
$$

$$
\text{Force Index} = \operatorname{EMA}(\text{Raw Force Index},\; \text{window})
$$

The formula for the Cumulative Force Index is as follows:

$$
\operatorname{Force}(t) = (\operatorname{Close}(t) - \operatorname{Close}(t-1)) \cdot \operatorname{Volume}(t)
$$

$$
\operatorname{CFI}(t) = \operatorname{CFI}(t-1) + \operatorname{EMA}(\text{Force},\; \text{window}) (t),\;\; \text{starting on the start date}
$$

As with On-Balance Volume, the level of the Cumulative Force Index depends on the start date and the number of shares traded; only the direction and the divergences from price carry meaning.

**Also known as:** FI, Elder's Force Index, EFI, CFI, Cumulative Force Index, Weighted On-Balance Volume, WOBV (the Cumulative Force Index with a window of 1).

**References:**

- paper | Elder, A. (1993). "Trading for a Living: Psychology, Trading Tactics, Money Management." John Wiley & Sons.
- library | Referenced against TA-Lib's [EFI](https://ta-lib.org/functions/efi.html){:target="_blank"}
- library | Referenced against finta's [CFI](https://github.com/peerchemist/finta/blob/1.3/finta/finta.py#L1585){:target="_blank"} (cumulative Force Index)
- library | Referenced against finta's [WOBV](https://github.com/peerchemist/finta/blob/1.3/finta/finta.py#L1506){:target="_blank"} (cumulative Force Index)

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column in the historical data that represents
the closing prices. Defaults to "Adj Close".
- <u>window (int &#124; None, optional):</u> The number of periods of the EMA that smooths the raw
Force Index. Defaults to None, which is 13 with method="standard", Elder's setting
for the trend (2 is his setting for timing entries), and 10 with
method="cumulative"; 1 gives the Weighted On-Balance Volume.
- <u>method (str, optional):</u> The index. Options are: "standard" (the Force Index), "cumulative" (its
running total from the start date, the Cumulative Force Index). Defaults to "standard".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: Force Index or Cumulative Force Index values, in price times
volume.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the Force Index values for each asset in the Toolkit instance; the Cumulative Force Index
as a running total from the start date.
- The Force Index agrees with TA-Lib's EFI.
- The Cumulative Force Index with a window of 1 agrees with finta's WOBV. With a larger window
every change agrees with that of finta's CFI once the EMAs have converged (after about
200 periods), but the EMA starts from the simple average of its first `window` values
while finta's averages from the first value, and the running total keeps the difference
of the warm-up as a constant offset.
- When growth is requested, the method calculates the growth of the indicator values
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["TLT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_force_index().tail(5)
```

Which returns:

| Date       |               TLT |    Benchmark |
|:-----------|------------------:|-------------:|
| 2025-12-24 |  946514           |  8.27837e+07 |
| 2025-12-26 | -287501           |  7.05413e+07 |
| 2025-12-29 |       1.09756e+06 |  3.86575e+07 |
| 2025-12-30 |  223430           |  2.75431e+07 |
| 2025-12-31 |      -3.35421e+06 | -2.98818e+07 |

---

## get_ultimate_oscillator
Calculate the Ultimate Oscillator: the buying pressure over three windows combined into one value from 0 to 100, to show overbought and oversold levels with fewer false signals.

The Ultimate Oscillator is a momentum oscillator that combines short-term, mid-term, and long-term price momentum into a single value.

The formula is as follows:

$$
\operatorname{Average}(i) = \frac{\operatorname{Sum}(\text{Buying Pressure},\; \text{window}_{i})}{\operatorname{Sum}(\text{True Range},\; \text{window}_{i})}
$$

$$
\text{Ultimate Oscillator} = \frac{100 \cdot \left[(4 \cdot \text{Average}_{1}) + (2 \cdot \text{Average}_{2}) + \text{Average}_{3}\right]}{7}
$$

**Also known as:** UO, ultimate momentum oscillator. See `momentum_model.get_ultimate_oscillator` for the Buying Pressure and True Range definitions.

**References:**

- paper | Williams, L.R. (1985). "The Ultimate Oscillator." Technical Analysis of Stocks & Commodities, 3(4), 140-141.
- library | Referenced against TA-Lib's [ULTOSC](https://ta-lib.org/functions/ultosc.html){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column in the historical data that represents
Defaults to "Adj Close", in which case the open, high and low prices are adjusted
for dividends in the same way.
- <u>window_1 (int, optional):</u> The number of periods for the first short-term window.
Defaults to 7.
- <u>window_2 (int, optional):</u> The number of periods for the second mid-term window.
Defaults to 14.
- <u>window_3 (int, optional):</u> The number of periods for the third long-term window.
Defaults to 28.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: Ultimate Oscillator values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the Ultimate Oscillator values for each asset in the Toolkit instance.
- The Ultimate Oscillator agrees with TA-Lib's ULTOSC. The first period counts with its High —
Low range and its close minus its low, so the oscillator starts on period `window_3`, one
period before TA-Lib's.
- When growth is requested, the method calculates the growth of the indicator values
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["^GDAXI"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_ultimate_oscillator().tail(5)
```

Which returns:

| Date       |   ^GDAXI |   Benchmark |
|:-----------|---------:|------------:|
| 2025-12-24 | nan      |     57.7084 |
| 2025-12-26 | nan      |     56.8787 |
| 2025-12-29 |  56.2772 |     64.508  |
| 2025-12-30 |  61.9948 |     66.0178 |
| 2025-12-31 | nan      |     52.8916 |

---

## get_percentage_volume_oscillator
Calculate the Percentage Volume Oscillator (PVO): the difference between a fast and a slow average of the volume as a share of the slow one, which shows whether volume is rising or falling.

The Percentage Volume Oscillator is the Percentage Price Oscillator applied to volume: the difference between a short-term and a long-term EMA of volume as a share of the long-term EMA, with a signal line and a histogram as for the MACD.

The formula is as follows:

$$
\text{PVO} = \frac{\operatorname{MA}(\text{Volume},\; \text{short\_window}) - \operatorname{MA}(\text{Volume},\; \text{long\_window})}{\operatorname{MA}(\text{Volume},\; \text{long\_window})}
$$

$$
\text{Signal Line} = \operatorname{EMA}(\text{PVO},\; \text{signal\_window})
$$

$$
\text{Histogram} = \text{PVO} - \text{Signal Line}
$$

with MA the Exponential Moving Average by default. With the Simple Moving Average it is the Volume Oscillator (VOSC) of StockCharts, pandas-ta-classic and Tulip Indicators, often used with 14 and 28 periods.

A positive PVO means recent volume runs above its longer-term average, which gives weight to a breakout or a trend in price; a PVO below zero in a rising market says the move happens on thinning volume. Because it is a share of the average volume, the PVO can be compared across stocks whatever the number of shares they trade. It says nothing about the direction of price.

**Also known as:** PVO, volume oscillator, VOSC. See `momentum_model.get_percentage_volume_oscillator` for the references.

**References:**

- paper | Appel, G. (1979). "The Moving Average Convergence-Divergence Trading Method." Signalert Corp., the MACD of which the PVO is the volume counterpart in percent.
- library | Referenced against TA-Lib's [PVO](https://ta-lib.org/functions/pvo.html){:target="_blank"}
- library | Referenced against pandas-ta-classic's [vosc](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/volume/vosc.py#L12){:target="_blank"}
- library | Referenced against Tulip Indicators' [vosc](https://tulipindicators.org/vosc){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>short_window (int, optional):</u> The number of periods for the short-term moving average.
Defaults to 12, as for the PPO and MACD.
- <u>long_window (int, optional):</u> The number of periods for the long-term moving average.
Defaults to 26, as for the PPO and MACD.
- <u>signal_window (int, optional):</u> The number of periods for the signal line.
Defaults to 9.
- <u>moving_average (str, optional):</u> The moving average of the volume. Options are:
"exponential" (Exponential Moving Average), "simple" (Simple Moving Average, which gives the
Volume Oscillator). The signal line is always an EMA. Defaults to "exponential".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: The Percentage Volume Oscillator, Signal Line and Histogram
as decimals (0.02 is 2%), as the Percentage Price Oscillator.

**Notes:**

- The method retrieves the volumes of the specified `period` and calculates the PVO for each
asset in the Toolkit instance. Every EMA is seeded with the simple average of its first
values, so the PVO starts on the `long_window`-th period and the signal line and histogram
`signal_window` - 1 periods later.
- A ticker without volume, such as an index or a currency pair, has no PVO.
- The PVO is a decimal, like the Percentage Price Oscillator, and NaN for a ticker without
volume. It agrees with TA-Lib's PVO (with its default EMA) divided by 100: TA-Lib's PVO is in
percent, returns 0 without volume and has no signal line or histogram. With the
Simple Moving Average it agrees with TA-Lib's PVO with that moving average and the `vosc` of
pandas-ta-classic and Tulip Indicators, divided by 100.
- When growth is requested, the method calculates the growth of the indicator values
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["NVDA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_percentage_volume_oscillator().xs("NVDA", level=1, axis="columns").tail(5)
```

Which returns:

| Date       |   Histogram |   Percentage Volume Oscillator |   Signal Line |
|:-----------|------------:|-------------------------------:|--------------:|
| 2025-12-24 |     -0.0392 |                        -0.0687 |       -0.0295 |
| 2025-12-26 |     -0.0393 |                        -0.0786 |       -0.0393 |
| 2025-12-29 |     -0.0451 |                        -0.0957 |       -0.0506 |
| 2025-12-30 |     -0.0559 |                        -0.1205 |       -0.0646 |
| 2025-12-31 |     -0.0509 |                        -0.1282 |       -0.0773 |

---

## get_detrended_price_oscillator
Calculate the Detrended Price Oscillator (DPO): the price minus a moving average shifted back in time, which removes the trend to show the cycles.

The Detrended Price Oscillator (DPO) is an indicator that helps identify short-term cycles by removing longer-term trends from prices.

The formula is as follows:

$$
\text{Displacement} = \left\lfloor \frac{\text{Number of Periods}}{2} \right\rfloor + 1
$$

$$
\text{DPO} = \operatorname{Close}(t - \text{Displacement}) - \operatorname{SMA}(\text{Close},\; \text{Number of Periods}) (t)
$$

**Also known as:** DPO, detrended price oscillator. Note the moving average itself is not shifted - only the close price used for the comparison is looked up further back in time; see `momentum_model.get_detrended_price_oscillator` for the full explanation.

**References:**

- paper | Murphy, J.J. (1999). "Technical Analysis of the Financial Markets." New York Institute of Finance.
- library | Referenced against TA-Lib's [DPO](https://ta-lib.org/functions/dpo.html){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column in the historical data that represents
the closing prices. Defaults to "Adj Close".
- <u>window (int, optional):</u> The number of periods to consider for the DPO calculation.
Defaults to 14.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: Detrended Price Oscillator (DPO) values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the DPO values for each asset in the Toolkit instance.
- The DPO agrees with TA-Lib's DPO.
- When growth is requested, the method calculates the growth of the indicator values
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["NGUSD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_detrended_price_oscillator().tail(5)
```

Which returns:

| Date       |   NGUSD |   Benchmark |
|:-----------|--------:|------------:|
| 2025-12-26 | -0.0656 |     -3.2958 |
| 2025-12-28 | -0.1575 |    nan      |
| 2025-12-29 | -0.0724 |     -5.5778 |
| 2025-12-30 | -0.001  |    -13.3921 |
| 2025-12-31 | -0.0537 |     -8.1194 |

---

## get_average_directional_index
Calculate the Average Directional Index (ADX) or its rating (ADXR): how strong a trend is, whatever its direction, from the smoothed difference between upward and downward movement.

The Average Directional Index (ADX) is an indicator that measures the strength of a trend, whether it's an uptrend or a downtrend. The Average Directional Movement Index Rating (ADXR) is Wilder's smoothed ADX: the average of today's ADX and the ADX of window - 1 periods ago. Wilder rated markets with it on how strongly they trend, to choose the ones to trade with his trend-following systems; it moves more slowly than the ADX and lags it.

The formula is as follows, per method:

$$
\text{ADX:}\;\; \text{ADX} = \text{Wilder's Smoothed Moving Average of DX},\;\; \text{where}\;\; \text{DX} = \frac{100 \cdot \left|\text{+DI} - \text{-DI}\right|}{\text{+DI} + \text{-DI}}
$$

$$
\text{ADXR:}\;\; \text{ADXR} = \frac{\operatorname{ADX}(t) + \operatorname{ADX}(t - (\text{window} - 1))}{2}
$$

The ADX measures trend strength, not direction: a reading above about 25 is usually taken as a trending market and below 20 as a range, whether prices are rising or falling. Traders combine it with the +DI and -DI lines it is built from (`get_directional_movement_index`), or with the price itself, to know the direction. With Wilder's smoothing it reacts slowly and needs a few times the window of history before its values settle. The same readings apply to the ADXR.

**Also known as:** ADX, trend strength indicator, ADXR, Average Directional Movement Rating, Average Directional Movement Index Rating.

See `momentum_model.get_average_directional_index` for the full formula, which uses Wilder's smoothing (not a plain SMA) throughout.

**References:**

- paper | Wilder, J.W. Jr. (1978). "New Concepts in Technical Trading Systems." Trend Research.
- library | Referenced against TA-Lib's [ADX](https://ta-lib.org/functions/adx.html){:target="_blank"}
- library | Referenced against TA-Lib's [ADXR](https://ta-lib.org/functions/adxr.html){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column in the historical data that represents
Defaults to "Adj Close", in which case the open, high and low prices are adjusted
for dividends in the same way.
- <u>window (int, optional):</u> The number of periods to consider for the ADX calculation.
Defaults to 14. With method="rating" also the lag of the rating.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>method (str, optional):</u> Options are: "standard" (the ADX), "rating" (the ADXR). Defaults to
"standard".
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame or pd.Series: Average Directional Index (ADX) or Average Directional
Movement Index Rating (ADXR) values, between 0 and 100.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the ADX values for each asset in the Toolkit instance.
- Wilder's smoothing is seeded with the average of the first `window` values, while TA-Lib's
ADX seeds its running sums with `window` - 1 values, so the first values differ from
TA-Lib's until the two converge (within 0.01% after about 120 periods with the default
window).
- ADXR: the ADXR starts 3 * `window` — 2 periods after the first price, as in TA-Lib,
and its first values differ from TA-Lib's ADXR in the same way until the two converge
(within 0.01% after about 100 to 125 periods with the default window).
- When growth is requested, the method calculates the growth of the indicator values
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["USDJPY"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_average_directional_index().tail(5)
```

Which returns:

| Date       |   USDJPY |   Benchmark |
|:-----------|---------:|------------:|
| 2025-12-26 |  12.9436 |     14.8316 |
| 2025-12-28 |  12.0867 |    nan      |
| 2025-12-29 |  11.4583 |     14.7623 |
| 2025-12-30 |  11.0975 |     14.698  |
| 2025-12-31 |  10.4608 |     13.7116 |

---

## get_directional_movement_index
Calculate Wilder's Directional Movement System: the smoothed Plus and Minus Directional Movement (+DM, -DM), the Directional Indicators (+DI, -DI) and the Directional Movement Index (DX).

The Directional Movement is the part of a period's range outside the previous period's range: upward when the high rises above the previous high by more than the low falls below the previous low, downward the other way around. Wilder sums each over the window with his smoothing and divides it by the smoothed True Range, which gives the Directional Indicators: the share of the recent range that moved up (+DI) and down (-DI). The DX is their difference as a share of their sum, high in a trend in either direction and low in a range; its Wilder average is the ADX.

The formula is as follows:

$$
+ \operatorname{DM}(1) = \text{High} - \text{Previous High},\;\; \text{where positive and larger than Previous Low} \;\mathord{-} \;\text{Low},\;\; \text{else 0}
$$

$$
\operatorname{DM}(1) = \text{Previous Low} - \text{Low},\;\; \text{where positive and larger than High} \;\mathord{-} \;\text{Previous High},\;\; \text{else 0}
$$

$$
+ \text{DM} = \text{Wilder's sum of} + \operatorname{DM}(1) \;\text{over window},\;\; \operatorname{Sum}(t) = \operatorname{Sum}(t-1) - \frac{\operatorname{Sum}(t-1)}{\text{window}} + + \operatorname{DM}(1) (t),\;\; \text{and -DM analogously}
$$

$$
\text{+DI} = 100 \cdot + \frac{\text{DM}}{\text{Wilder's sum of the True Range}},\;\; \text{-DI} = 100 \cdot - \frac{\text{DM}}{\text{Wilder's sum of the True Range}}
$$

$$
\text{DX} = \frac{100 \cdot \left|\text{+DI} - \text{-DI}\right|}{\text{+DI} + \text{-DI}}
$$

+DI crossing above -DI is Wilder's buy signal and crossing below it his sell signal, which he only took when the ADX showed a trend. The DX itself is jumpy; the ADX (`get_average_directional_index`) and the ADXR (the rating of `get_average_directional_index`) smooth it.

**Also known as:** DMI, Directional Movement System, +DM, -DM, +DI, -DI, DX, PLUS_DM, MINUS_DM, PLUS_DI, MINUS_DI, directional indicators.

**References:**

- paper | Wilder, J.W. Jr. (1978). "New Concepts in Technical Trading Systems." Trend Research.
- library | Referenced against TA-Lib's [PLUS_DM](https://ta-lib.org/functions/plus_dm.html){:target="_blank"}
- library | Referenced against TA-Lib's [MINUS_DM](https://ta-lib.org/functions/minus_dm.html){:target="_blank"}
- library | Referenced against TA-Lib's [PLUS_DI](https://ta-lib.org/functions/plus_di.html){:target="_blank"}
- library | Referenced against TA-Lib's [MINUS_DI](https://ta-lib.org/functions/minus_di.html){:target="_blank"}
- library | Referenced against TA-Lib's [DX](https://ta-lib.org/functions/dx.html){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the open, high and low prices are adjusted
for dividends in the same way.
- <u>window (int, optional):</u> The number of periods of Wilder's smoothing. Defaults to 14.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: +DM and -DM (Wilder's smoothed sums, in price units), +DI and -DI and the DX
(between 0 and 100).

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the Directional Movement Index for each asset in the Toolkit instance.
- The columns are the inputs of `get_average_directional_index`, whose ADX is Wilder's
average of this DX, so the two are consistent. Wilder's smoothing is seeded with the sum of
the first `window` values (from the second period, the first with a previous one), so every
column starts `window` periods after the first price and the ADX 2 * `window` — 1 periods
after it.
- TA-Lib seeds its running sums with `window` - 1 values and starts PLUS_DM and MINUS_DM one
period earlier, so the first values differ from TA-Lib's PLUS_DM, MINUS_DM, PLUS_DI, MINUS_DI
and DX and converge as the seed decays by a factor 1 — 1 / `window` per period: with the default
window within 0.01% after about 100 periods for the +DM, -DM, +DI and -DI and 150 for the DX,
and to 1e-8 after about 260.
- A window without any directional movement (+DI and -DI both 0) has no DX.
- When growth is requested, the method calculates the growth of the Directional Movement Index
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_directional_movement_index().xs("AAPL", level=1, axis="columns").tail(5)
```

Which returns:

| Date       |     +DI |     +DM |     -DI |     -DM |      DX |
|:-----------|--------:|--------:|--------:|--------:|--------:|
| 2025-12-24 | 18.7359 | 12.1058 | 21.4378 | 13.8516 |  6.7255 |
| 2025-12-26 | 17.9861 | 11.2411 | 20.5798 | 12.8622 |  6.7255 |
| 2025-12-29 | 17.386  | 10.4382 | 20.7397 | 12.4517 |  8.7965 |
| 2025-12-30 | 16.844  |  9.6926 | 20.2144 | 11.6321 |  9.0948 |
| 2025-12-31 | 16.2588 |  9.0003 | 20.4662 | 11.3294 | 11.4565 |

---

## get_chande_momentum_oscillator
Calculate the Chande Momentum Oscillator (CMO): the gains minus the losses over a window as a share of their sum, from -100 to 100, to show momentum and overbought and oversold levels.

The Chande Momentum Oscillator is an indicator that measures the momentum of a price series and identifies overbought and oversold conditions.

The formula is as follows:

$$
\text{CMO} = \frac{100 \cdot ((\text{Sum of Upward Change}) - (\text{Sum of Downward Change}))}{(\text{Sum of Upward Change}) + (\text{Sum of Downward Change})},\;\; \text{bounded between -100 and 100}
$$

$$
\text{Smoothed CMO} = \frac{100 \cdot (\text{Wilder's MA}(\text{Upward Change}) - \text{Wilder's MA}(\text{Downward Change}))}{\text{Wilder's MA}(\text{Upward Change}) + \text{Wilder's MA}(\text{Downward Change})}
$$

Chande sums the changes over the window, so every change in the window counts equally and the CMO jumps when a large change leaves the window. The smoothed CMO averages the changes with Wilder's smoothing, as in the RSI, which gives TA-Lib's CMO: a smoother line that equals 2 * RSI - 100.

**Also known as:** CMO, CMOU, Chande momentum.

**References:**

- paper | Chande, T.S. & Kroll, S. (1994). "The New Technical Trader." Wiley.
- library | Referenced against TA-Lib's [CMOU](https://ta-lib.org/functions/cmou.html){:target="_blank"}
- library | Referenced against TA-Lib's [CMO](https://ta-lib.org/functions/cmo.html){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column in the historical data that represents
the closing prices. Defaults to "Adj Close".
- <u>window (int, optional):</u> The number of periods to consider for the CMO calculation.
Defaults to 14.
- <u>smoothed (bool, optional):</u> Whether to smooth the gains and losses with Wilder's method
(TA-Lib's CMO) instead of summing them (Chande's CMO, TA-Lib's CMOU). Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: Chande Momentum Oscillator values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the Chande Momentum Oscillator values for each asset in the Toolkit instance.
- By default the gains and losses are summed over the window, as Chande defines the CMO and as
on StockCharts, which agrees with TA-Lib's CMOU. TA-Lib's CMO smooths them with Wilder's method
instead, as in its RSI, so the two differ throughout (by up to about 55 points on daily data);
the smoothed CMO gives TA-Lib's CMO, from the same period on.
- When growth is requested, the method calculates the growth of the indicator values
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["SIUSD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_chande_momentum_oscillator().tail(5)
```

Which returns:

| Date       |   SIUSD |   Benchmark |
|:-----------|--------:|------------:|
| 2025-12-26 | 59.7384 |     13.98   |
| 2025-12-28 | 57.585  |    nan      |
| 2025-12-29 | 26.3917 |     13.0139 |
| 2025-12-30 | 38.9776 |     12.4231 |
| 2025-12-31 | 15.5101 |     -7.4365 |

---

## get_ichimoku_cloud
Calculate the Ichimoku Cloud: the midpoints of the highs and lows over three windows, which show the trend, the momentum and the support and resistance of the prices at a glance.

The Ichimoku Cloud, also known as the Ichimoku Kinko Hyo, is a versatile indicator that defines support and resistance, identifies trend direction, gauges momentum, and provides trading signals.

The formula is as follows:

$$
\text{Conversion Line} = \frac{\text{Highest High} + \text{Lowest Low}}{2},\;\; \text{over conversion\_window periods}
$$

$$
\text{Base Line} = \frac{\text{Highest High} + \text{Lowest Low}}{2},\;\; \text{over base\_window periods}
$$

$$
\text{Leading Span}\; A = \frac{\text{Conversion Line} + \text{Base Line}}{2},\;\; \text{shifted forward base\_window periods}
$$

$$
\text{Leading Span}\; B = \frac{\text{Highest High} + \text{Lowest Low}}{2} \;\text{over}\; \text{lead\_span\_b\_window} \;\text{periods},\;\; \text{shifted forward base\_window periods}
$$

Price above the cloud is read as an uptrend and below it as a downtrend, with the cloud itself as support or resistance; a thick cloud is stronger support than a thin one. The leading spans are shifted forward by the base window, so the cloud value shown on a date was calculated base_window periods (26 by default) earlier from the data then available. The method returns the Conversion and Base Lines and the two Leading Spans but not the Lagging Span (the close shifted back), which would report a future close on each date.

**Also known as:** Ichimoku Kinko Hyo, cloud indicator. The default windows (9, 26, 52) are Goichi Hosoda's original values, both leading spans are conventionally displaced forward by the base (Kijun-sen) period.

**References:**

- paper | Hosoda, G. (1969). "Ichimoku Kinko Hyo." Published under the pen name Ichimoku Sanjin.
- paper | Elliott, N. (2007). "Ichimoku Charts." Harriman House.
- library | Referenced against TA-Lib's [ICHIMOKU](https://ta-lib.org/functions/ichimoku.html){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>conversion_window (int, optional):</u> The number of periods to consider for the
Conversion Line (Tenkan-sen) calculation. Defaults to 9.
- <u>base_window (int, optional):</u> The number of periods to consider for the Base Line
(Kijun-sen) calculation, also used as the forward displacement for both
Leading Spans. Defaults to 26.
- <u>lead_span_b_window (int, optional):</u> The number of periods to consider for the
Lead Span B (Senkou Span B) calculation. Defaults to 52.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame:
Conversion Line, Base Line, Lead Span A, and Lead Span B values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the Ichimoku Cloud values for each asset in the Toolkit instance.
- The Conversion Line and Base Line agree with TA-Lib's ICHIMOKU, and so do the leading spans
`base_window` periods earlier: TA-Lib places them on the period they are calculated on
instead of displacing them forward, and starts every line on the `lead_span_b_window`-th
period.
- When growth is requested, the method calculates the growth of the indicator values
over the given lag.
- The leading spans are shifted forward by exactly `base_window` periods, as StockCharts
defines the cloud. Platforms that count the current period as the first of the 26
shift by `base_window` - 1 and show the same values one period earlier.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["^N225"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_ichimoku_cloud().xs("^N225", level=1, axis="columns").tail(5)
```

Which returns:

| Date       |   Base Line |   Conversion Line |   Leading Span A |   Leading Span B |
|:-----------|------------:|------------------:|-----------------:|-----------------:|
| 2025-12-25 |     49681.5 |           49640.4 |          49838.9 |          47250   |
| 2025-12-26 |     49808.9 |           49792.8 |          49732.3 |          47250   |
| 2025-12-29 |     49808.9 |           49792.8 |          49824   |          47351.7 |
| 2025-12-30 |     49819.8 |           49792.8 |          49969.9 |          47710.2 |
| 2025-12-31 |       nan   |             nan   |          49926.3 |          47990.2 |

---

## get_stochastic_oscillator
Calculate the Stochastic Oscillator or the Stochastic RSI, from 0 to 100, which show momentum and overbought and oversold levels.

It is where the close, or for the Stochastic RSI the Relative Strength Index, lies within its range over a window.

The Stochastic Oscillator is a momentum indicator that shows the location of the close relative to the high-low range over a set number of periods. It consists of the %K line (fast) and the %D line (slow). The Stochastic RSI applies the Stochastic Oscillator to the Relative Strength Index instead of to price: it shows where the current RSI sits within its own high-low range over the last `stochastic_window` periods. Chande and Kroll (1994, "The New Technical Trader") designed it because the RSI can spend long stretches between 30 and 70 without reaching either extreme; the Stochastic RSI reaches 0 and 100 far more often.

The formula is as follows, per method:

$$
\text{Stochastic Oscillator:}\;\; \%K = 100 \cdot \frac{\text{Close} - \text{Lowest Low}}{\text{Highest High} - \text{Lowest Low}},\;\; \%D = \operatorname{SMA}(\%K,\; \text{smooth\_window}),\;\; \text{and}\;\; \text{with} \;\text{slow} \;\text{Slow}\; \%K = \operatorname{SMA}(\%K,\; \text{smooth\_window}) \;\text{and Slow}\; \%D = \operatorname{SMA}(\text{Slow}\; \%K,\; \text{smooth\_window})
$$

$$
\text{Stochastic RSI:}\;\; \text{RSI} = \text{Relative Strength Index}(\text{Close},\; \text{window}),\;\; \text{with Wilder's smoothing},\;\; \%K = \frac{100 \cdot (\text{RSI} - \text{Lowest RSI})}{\text{Highest RSI} - \text{Lowest RSI}} \;\text{over the last}\; \text{stochastic\_window} \;\text{RSI values},\;\; \text{and}\;\; \%D = \operatorname{SMA}(\%K,\; \text{smooth\_window})
$$

The fast stochastic (the default) reacts to every close and gives many crossovers. The slow stochastic smooths %K once more, so its %K is the fast %D; it is the stochastic George Lane charted and the one most platforms show by default (14, 3, 3).

The defaults of the Stochastic RSI follow Chande and Kroll's definition, a 14-period stochastic of a 14-period RSI, which StockCharts and TradingView use as well. StockCharts shows this %K on a scale of 0 to 1; TradingView smooths it over 3 periods, so its %K is the %D here. TA-Lib's STOCHRSI defaults to a 5-period stochastic instead (timeperiod 14, fastk_period 5 and fastd_period 3 with a simple average): a stochastic window of 5 gives its %K and %D. A %K of 100 means the RSI is at its highest of the window, not that the price is overbought, so the readings above 80 and below 20 come and go quickly and are mostly read together with the trend.

**Also known as:** stochastic oscillator, percent K, percent D, fast stochastic, slow stochastic, Stochastic RSI, StochRSI, Stoch RSI.

**References:**

- paper | Lane, G.C. (1984). "Lane's Stochastics." Technical Analysis of Stocks & Commodities, 2(3).
- paper | Chande, T.S. & Kroll, S. (1994). "The New Technical Trader." Wiley.
- library | Referenced against TA-Lib's [STOCHF](https://ta-lib.org/functions/stochf.html){:target="_blank"}
- library | Referenced against TA-Lib's [STOCH](https://ta-lib.org/functions/stoch.html){:target="_blank"}
- library | Referenced against TA-Lib's [STOCHRSI](https://ta-lib.org/functions/stochrsi.html){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the open, high and low prices are adjusted
for dividends in the same way.
- <u>window (int, optional):</u> The number of periods to consider for the %K line calculation,
and with method="rsi" the number of periods of the RSI. Defaults to 14.
- <u>smooth_window (int, optional):</u> The number of periods used to smooth the %K line
into the %D signal line, and with `slow` the raw %K into the slow %K. Defaults to 3.
- <u>slow (bool, optional):</u> Whether to return the slow stochastic instead of the fast one.
Only used when method="standard". Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the %K and %D values.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>method (str, optional):</u> The stochastic. Options are: "standard" (of the price), "rsi" (the
Stochastic RSI). Defaults to "standard".
- <u>stochastic_window (int, optional):</u> The number of periods of RSI values whose high-low
range gives %K. Only used when method="rsi". Defaults to 14.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: Stochastic Oscillator (%K and %D) values, between 0 and
100, as "Stochastic %K" and "Stochastic %D", or "Stochastic RSI %K" and
"Stochastic RSI %D" for the Stochastic RSI.

**Raises:**

ValueError: If the specified `period` or `method` is not one of the valid options.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the Stochastic Oscillator values for each asset in the Toolkit instance.
- %K and %D agree with TA-Lib's STOCHF (the fast stochastic) with `fastd_period` set to
`smooth_window` and a simple moving average, which TA-Lib's STOCH gives
with a `slowk_period` of 1. TA-Lib starts %K on the first %D.
- The slow stochastic's %K and %D agree with TA-Lib's STOCH with `slowk_period` and `slowd_period` set to
`smooth_window` and simple moving averages, and
pandas-ta-classic's stoch. TA-Lib starts %K on the first %D.
- Stochastic RSI: the RSI is seeded with a simple average of its first `window` changes, as Wilder
and TA-Lib do, so %K starts `window` + `stochastic_window` - 1 periods after the first
price and %D `smooth_window` - 1 periods later. TA-Lib starts both on the first %D,
with the same values from there. An RSI that did not move over the stochastic window
has no range, which leaves %K missing (TA-Lib sets it to 0). With `fastk_period` set to
`stochastic_window`, `fastd_period` to `smooth_window` and a simple moving average,
%K and %D agree with TA-Lib's STOCHRSI.
- When growth is requested, the method calculates the growth of the %K and %D values
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["GBPUSD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_stochastic_oscillator().xs("GBPUSD", level=1, axis="columns").tail(5)
```

Which returns:

| Date       |   Stochastic %D |   Stochastic %K |
|:-----------|----------------:|----------------:|
| 2025-12-26 |         86.4285 |         82.9586 |
| 2025-12-28 |         85.136  |         82.9137 |
| 2025-12-29 |         84.997  |         89.1187 |
| 2025-12-30 |         80.5606 |         69.6493 |
| 2025-12-31 |         74.4904 |         64.7032 |

---

## get_moving_average_convergence_divergence
Calculate the Moving Average Convergence Divergence (MACD) or the Percentage Price Oscillator, which show the direction and momentum of a trend.

It is the difference between a fast and a slow moving average, in price units or, for the Percentage Price Oscillator, as a percentage of the slow average, with its signal line.

The Moving Average Convergence Divergence (MACD) is a trend-following momentum indicator that shows the relationship between two moving averages of a security's price. It consists of the MACD line and its signal line; their difference is the MACD histogram. The MACD line is the Absolute Price Oscillator (APO), the difference between a short-term and a long-term moving average of the price, in price units: with exponential moving averages it is Appel's MACD line, and `moving_average` lets the average be chosen, such as simple moving averages for a slower oscillator. The Percentage Price Oscillator measures the difference between the two moving averages as a percentage of the longer one.

The formula is as follows, per method:

$$
\text{MACD:}\;\; \text{MACD Line} \;(\text{APO}) = \operatorname{MA}(\text{Close},\; \text{short\_window}) - \operatorname{MA}(\text{Close},\; \text{long\_window}),\;\; \text{with the EMA by default},\;\; \text{Signal Line} = \operatorname{EMA}(\text{MACD Line},\; \text{signal\_window})\;\;\text{and}\;\; \text{Histogram} = \text{MACD Line} - \text{Signal Line}
$$

$$
\text{Percentage Price Oscillator:}\;\; \text{PPO} = \frac{\operatorname{MA}(\text{Close},\; \text{short\_window}) - \operatorname{MA}(\text{Close},\; \text{long\_window})}{\operatorname{MA}(\text{Close},\; \text{long\_window})},\;\; \text{with the EMA by default},\;\; \text{Signal Line} = \operatorname{EMA}(\text{PPO},\; \text{signal\_window})\;\;\text{and}\;\; \text{Histogram} = \text{PPO} - \text{Signal Line}
$$

The MACD line crossing its signal line is the usual trigger, and the MACD crossing zero means the short average has crossed the long one. The histogram is the distance between the two lines: it crosses zero with every crossover and shrinks before one, which is why it is read as an early warning. Because the MACD is a price difference, its level scales with the share price and cannot be compared across stocks; the Percentage Price Oscillator divides by the long average for that. Both lines lag price, so crossovers come late in fast reversals. The PPO is the MACD line as a percentage of the long average, so unlike the MACD its level can be compared across stocks and over long periods; its signal line is always an EMA.

`moving_average` and `signal_moving_average` replace the EMAs of the MACD line and of the signal line with another moving average (TA-Lib's MACDEXT), and the fixed MACD smooths the 12- and 26-period EMAs with the fixed constants 0.15 and 0.075 instead of 2 / (window + 1) (TA-Lib's MACDFIX). With the Volume Weighted Moving Average it is Dormeier's Volume Weighted MACD: the Volume Weighted Moving Averages, Sum(Close × Volume) / Sum(Volume), let the periods with heavy volume count more, so a move on heavy volume moves the MACD more than one on light volume. The Elastic Volume Weighted MACD uses Fries' Elastic Volume Weighted Moving Average, which moves towards the price by the share of the window's volume traded in a period (the 20 and 40 periods in finta).

**Also known as:** MACD, MACD histogram, MACDEXT, MACDFIX, VWMACD, volume weighted MACD, EVMACD, elastic volume weighted MACD, momentum indicator, APO, absolute price oscillator, price oscillator, PPO, percentage price oscillator, PPO signal line, PPO histogram.

**References:**

- paper | Appel, G. (1979). "The Moving Average Convergence-Divergence Trading Method." Signalert Corp.
- paper | Aspray, T. (1988). "MACD Momentum." Technical Analysis of Stocks & Commodities, 6(8), 294-297, for the MACD histogram.
- paper | Achelis, S.B. (2000). "Technical Analysis from A to Z." 2nd ed. McGraw-Hill.
- paper | Appel, G. (2005). "Technical Analysis: Power Tools for Active Investors." FT Press.
- paper | Dormeier, B.P. (2011). "Investing with Volume Analysis." FT Press.
- paper | Fries, C.P. (2001). "Elastic Moving Averages." Technical Analysis of Stocks & Commodities, 19(6), 52-56 ([https://www.christian-fries.de/evwma/](https://www.christian-fries.de/evwma/){:target="_blank"}).
- library | Referenced against TA-Lib's [MACD](https://ta-lib.org/functions/macd.html){:target="_blank"}
- library | Referenced against TA-Lib's [MACDEXT](https://ta-lib.org/functions/macdext.html){:target="_blank"}
- library | Referenced against TA-Lib's [MACDFIX](https://ta-lib.org/functions/macdfix.html){:target="_blank"}
- library | Referenced against pandas-ta-classic's [vwmacd](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/momentum/vwmacd.py#L12){:target="_blank"}
- library | Referenced against TA-Lib's [APO](https://ta-lib.org/functions/apo.html){:target="_blank"}
- library | Referenced against TA-Lib's [PPO](https://ta-lib.org/functions/ppo.html){:target="_blank"}
- library | Shares similar logic as finta's [VW_MACD](https://github.com/peerchemist/finta/blob/1.3/finta/finta.py#L575){:target="_blank"}
- library | Shares similar logic as finta's [EV_MACD](https://github.com/peerchemist/finta/blob/1.3/finta/finta.py#L617){:target="_blank"}
- library | Shares similar logic as pandas-ta-classic's [ppo](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/momentum/ppo.py#L48){:target="_blank"}
- library | Shares similar logic as ta's [PercentagePriceOscillator](https://github.com/bukosabino/ta/blob/0.11.0/ta/momentum.py#L622){:target="_blank"}
- library | Shares similar logic as finta's [PPO](https://github.com/peerchemist/finta/blob/1.3/finta/finta.py#L541){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>short_window (int, optional):</u> The number of periods for the shorter moving average.
Defaults to 12.
- <u>long_window (int, optional):</u> The number of periods for the longer moving average.
Defaults to 26.
- <u>signal_window (int, optional):</u> The number of periods for the signal line.
Defaults to 9.
- <u>moving_average (str, optional):</u> The moving average of the short and long term. Options are:
"simple" (Simple Moving Average), "exponential" (Exponential Moving Average),
"double_exponential" (Double Exponential Moving Average), "triangular" (Triangular Moving
Average), "weighted" (Weighted Moving Average), "hull" (Hull Moving Average),
"kaufman_adaptive" (Kaufman Adaptive Moving Average), "volume_weighted" (Volume Weighted Moving
Average, the Volume Weighted MACD), "elastic_volume_weighted" (Elastic Volume Weighted Moving
Average, the Elastic Volume Weighted MACD). Defaults to "exponential".
- <u>signal_moving_average (str, optional):</u> The moving average of the signal line. Options are:
"simple" (Simple Moving Average), "exponential" (Exponential Moving Average),
"double_exponential" (Double Exponential Moving Average), "triangular" (Triangular Moving
Average), "weighted" (Weighted Moving Average), "hull" (Hull Moving Average),
"kaufman_adaptive" (Kaufman Adaptive Moving Average), "volume_weighted" (Volume Weighted Moving
Average, the Volume Weighted MACD), "elastic_volume_weighted" (Elastic Volume Weighted Moving
Average, the Elastic Volume Weighted MACD). Only used when method="absolute"; the signal line of
the PPO is an EMA. Defaults to "exponential".
- <u>fixed (bool, optional):</u> Whether to smooth the 12- and 26-period EMAs with the fixed
constants 0.15 and 0.075 (TA-Lib's MACDFIX). Needs the exponential moving average and
the default windows. Only used when method="absolute". Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the MACD and signal values.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>method (str, optional):</u> Options are: "absolute" (the MACD in price units), "percentage" (the
Percentage Price Oscillator, a decimal of the long average). The volume weighted moving averages
and `fixed` apply to the MACD only. Defaults to "absolute".
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame:
MACD line, signal line and histogram values in price units ("MACD Line", "Signal Line"
and "Histogram"), or for the Percentage Price Oscillator the "Percentage Price Oscillator",
"Signal Line" and "Histogram" as decimals (0.02 is 2%).

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the MACD and signal line values for each asset in the Toolkit instance.
- TA-Lib's MACD starts the short EMA on the same period as the long EMA and shows the MACD
line from the first signal value, so the first values differ from TA-Lib's until the two
converge (within 0.01% after about 85 periods with the default windows). The histogram
agrees with TA-Lib's `macdhist` and ta's `macd_diff` from then on.
- TA-Lib's MACDEXT and MACDFIX start their averages in the same way. With simple, weighted or
triangular moving averages, which have no recursion, the lines equal MACDEXT from the
first value; with exponential ones (also MACDFIX) they converge within 0.01% after about 90
periods, with double exponential ones after about 130 and with Kaufman adaptive ones, whose
smoothing can be very slow, after about 210.
- With the Volume Weighted Moving Average for both the MACD line and the signal line the
lines agree with pandas-ta-classic's vwmacd. finta's VW_MACD divides exponential averages of
Close × Volume and of the volume instead. finta's EV_MACD starts every eVWMA from 0 where the
Toolkit seeds it with a simple average, so the two converge as the start decays (after
several hundred periods for a 40-period eVWMA).
- The MACD line agrees with TA-Lib's APO with the same moving average (its moving average type:
SMA 0, EMA 1, WMA 2, DEMA 3, TRIMA 5, KAMA 6) from the first value.
- Percentage Price Oscillator: the PPO is a decimal and agrees with TA-Lib's PPO with the same moving average
divided by 100, since TA-Lib's PPO is in percent. TA-Lib has no signal line or
histogram; with the default EMAs all three agree with pandas-ta-classic's ppo with
its exponential moving average, divided by 100. ta and finta seed their EMAs with the first price instead of
a simple average, so their first values differ until the two converge. Every EMA is seeded
with the simple average of its first values, so the PPO starts on the `long_window`-th
period and the signal line and histogram `signal_window` - 1 periods later.
- When growth is requested, the method calculates the growth of the MACD and signal values
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2024-10-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_moving_average_convergence_divergence().xs("MSFT", level=1, axis="columns").tail(5)
```

Which returns:

| Date       |   Histogram |   MACD Line |   Signal Line |
|:-----------|------------:|------------:|--------------:|
| 2025-12-24 |      1.7933 |     -3.0142 |       -4.8074 |
| 2025-12-26 |      1.8455 |     -2.5005 |       -4.3461 |
| 2025-12-29 |      1.7825 |     -2.1179 |       -3.9004 |
| 2025-12-30 |      1.7092 |     -1.7639 |       -3.4731 |
| 2025-12-31 |      1.361  |     -1.7718 |       -3.1329 |

---

## get_relative_strength_index
Calculate the Relative Strength Index (RSI): the size of the gains against the losses over a window, from 0 to 100, to show momentum and overbought and oversold levels.

The Relative Strength Index (RSI) is a momentum oscillator that measures the speed and change of price movements. It ranges from 0 to 100 and is used to identify overbought or oversold conditions in an asset's price. The variants share that scale:

- RSI: Wilder's RSI of the close.
- ConnorsRSI: the ConnorsRSI of Connors, Alvarez and Radtke averages three short-term measures of how overbought or oversold a price is, each on a scale of 0 to 100: a 3-period RSI of the close, a 2-period RSI of the streak (the number of periods in a row the close rose, positive, or fell, negative) and the percent rank of the latest one-period return among the returns of the previous 100 periods. It was designed for short-term mean reversion: below 10 (or 5) is oversold and a pullback in an uptrend to buy, above 90 (or 95) overbought.
- Laguerre RSI: the Laguerre RSI of Ehlers (2004) is an RSI over the four elements of a Laguerre filter instead of four prices. The first element is an exponential moving average and each next one an all-pass element that delays the low frequencies more than the high ones. That warps time: four elements look as far back as a much longer window, so the RSI is smooth yet reacts quickly. Ehlers buys when it crosses back above 20 and sells when it crosses back below 80.
- Dynamic Momentum Index: the Dynamic Momentum Index of Chande and Kroll (1994) is an RSI whose period changes with the volatility: it shortens when the recent volatility is above its average and lengthens when it is below, between 5 and 30 periods. The index thereby reacts quickly in volatile markets and stays calm in quiet ones.
- Intraday Momentum Index: the Intraday Momentum Index is an RSI of the moves within each period: it compares the bodies of the periods that closed above their open with all bodies over the window. Tushar Chande designed it for traders who care about the move from open to close rather than from close to close.

The formula is as follows, per method:

$$
\text{RSI:}\;\; \text{RSI} = 100 - \frac{100}{1 + \text{RS}},\;\; \text{with RS the ratio of Wilder's averages of the gains and losses over the window}
$$

$$
\text{ConnorsRSI:}\;\; \text{Streak} = \text{the number of consecutive periods the close rose} \;(\text{positive}) \;\text{or fell} \;(\text{negative}),\;\; \text{0 when it was unchanged},\;\; \text{Return} = \frac{\operatorname{Close}(t)}{\operatorname{Close}(t - 1)} - 1,\;\; \text{and}\;\; \text{ConnorsRSI} = \frac{\operatorname{RSI}(\text{Close},\; \text{window}) + \operatorname{RSI}(\text{Streak},\; \text{streak\_window}) + 100 \cdot \text{Percent Rank}(\text{Return},\; \text{rank\_window})}{3},\;\; \text{with Wilder's RSI and the Percent Rank the share of the previous rank\_window returns below the latest one (get\_percent\_rank)}
$$

$$
\text{Laguerre RSI:}\;\; L_{0} = (1 - \Gamma) \cdot \text{Price} + \Gamma \cdot \operatorname{L0}(t-1),\;\; L_{1} = - \Gamma \cdot L_{0} + \operatorname{L0}(t-1) + \Gamma \cdot \operatorname{L1}(t-1),\;\; L_{2} = - \Gamma \cdot L_{1} + \operatorname{L1}(t-1) + \Gamma \cdot \operatorname{L2}(t-1),\;\; L_{3} = - \Gamma \cdot L_{2} + \operatorname{L2}(t-1) + \Gamma \cdot \operatorname{L3}(t-1),\;\; \text{CU} = \text{the sum of}\; L_{0} - L_{1},\;\; L_{1} - L_{2} \;\text{and}\; L_{2} - L_{3} \;\text{where positive},\;\; \text{CD} = \text{the sum of}\; L_{1} - L_{0},\;\; L_{2} - L_{1} \;\text{and}\; L_{3} - L_{2} \;\text{where positive},\;\; \text{and}\;\; \text{Laguerre RSI} = \frac{100 \cdot \text{CU}}{\text{CU} + \text{CD}}
$$

$$
\text{Dynamic Momentum Index:}\;\; \text{Volatility Index} = \frac{\operatorname{StdDev}(\text{Close},\; \text{volatility\_window})}{\operatorname{SMA}(\operatorname{StdDev}(\text{Close},\; \text{volatility\_window}),\; \text{average\_window})},\;\; \text{Period} = \operatorname{Int}\left(\frac{\text{window}}{\text{Volatility Index}}\right) \;\text{bounded to}\; \text{minimum\_window} \;\text{and}\; \text{maximum\_window},\;\; \text{and}\;\; \text{DMI} = \frac{100 \cdot \operatorname{Sum}(\text{Up Changes},\; \text{Period})}{\operatorname{Sum}(\text{Up Changes},\; \text{Period}) + \operatorname{Sum}(\text{Down Changes},\; \text{Period})}
$$

$$
\text{Intraday Momentum Index:}\;\; \text{Gain} = \text{Close} - \text{Open where Close} > \text{Open},\;\; \text{else 0},\;\; \text{Loss} = \text{Open} - \text{Close where Close} < \text{Open},\;\; \text{else 0},\;\; \text{and}\;\; \text{IMI} = \frac{100 \cdot \operatorname{Sum}(\text{Gain},\; \text{window})}{\operatorname{Sum}(\text{Gain},\; \text{window}) + \operatorname{Sum}(\text{Loss},\; \text{window})}
$$

Readings above 70 are conventionally read as overbought and below 30 as oversold, but in a strong trend the RSI can stay above 70 or below 30 for weeks, so a crossing is not a signal on its own. Practitioners look more at divergences, a new price high with a lower RSI high, and at the 50 line as a trend filter. The value depends on the window: a shorter window swings more and reaches the extremes more often. Chande's Dynamic Momentum Index uses a 14-period base, a 5-period standard deviation and its 10-period average.

**Also known as:** RSI, momentum oscillator, overbought, oversold, CRSI, ConnorsRSI, Connors RSI, Laguerre RSI, LRSI, Ehlers' Laguerre RSI, DYMI, Dynamic Momentum Index, Chande's Dynamic Momentum Index, variable-term RSI, IMI, Intraday Momentum Index, intraday momentum.

**References:**

- paper | Wilder, J.W. Jr. (1978). "New Concepts in Technical Trading Systems." Trend Research.
- paper | Connors, L., Alvarez, C. & Radtke, M. (2012). "An Introduction to ConnorsRSI." Connors Research Trading Strategy Series.
- paper | Connors, L. & Alvarez, C. (2009). "Short Term Trading Strategies That Work." TradingMarkets Publishing.
- paper | Ehlers, J.F. (2004). "Cybernetic Analysis for Stocks and Futures." John Wiley & Sons, chapter 14, "Time Warp - Without Space Travel."
- paper | Chande, T.S. & Kroll, S. (1994). "The New Technical Trader." Wiley.
- library | Referenced against TA-Lib's [RSI](https://ta-lib.org/functions/rsi.html){:target="_blank"}
- library | Referenced against TA-Lib's [CRSI](https://ta-lib.org/functions/crsi.html){:target="_blank"} (ConnorsRSI)
- library | Referenced against pandas-ta-classic's [lrsi](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/momentum/lrsi.py#L29){:target="_blank"} (Laguerre RSI)
- library | Referenced against TA-Lib's [IMI](https://ta-lib.org/functions/imi.html){:target="_blank"} (Intraday Momentum Index)
- library | Shares similar logic as finta's [DYMI](https://github.com/peerchemist/finta/blob/1.3/finta/finta.py#L752){:target="_blank"} (Dynamic Momentum Index)

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the open of method="intraday" is adjusted
for dividends in the same way.
- <u>window (int &#124; None, optional):</u> The number of periods for RSI calculation: of the RSI
of the close ("connors"), the base period that the volatility index divides
("dynamic") and the number of periods to sum the gains and losses over
("intraday"). Not used by "laguerre". Defaults to None, which uses 3 for
"connors" and 14 for the others.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the RSI.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>method (str, optional):</u> The RSI. Options are: "standard" (Wilder's RSI), "connors" (ConnorsRSI),
"laguerre" (Ehlers' Laguerre RSI), "dynamic" (Chande's Dynamic Momentum Index),
"intraday" (Chande's Intraday Momentum Index). Defaults to "standard".
- <u>streak_window (int, optional):</u> The number of periods of the RSI of the streak. Only
used when method="connors". Defaults to 2.
- <u>rank_window (int, optional):</u> The number of previous returns of the percent rank. Only
used when method="connors". Defaults to 100.
- <u>gamma (float, optional):</u> The damping factor of the Laguerre filter, at least 0 and
below 1: a higher value smooths more and lags more. Only used when
method="laguerre". Defaults to 0.5.
- <u>volatility_window (int, optional):</u> The number of periods of the standard deviation.
Only used when method="dynamic". Defaults to 5.
- <u>average_window (int, optional):</u> The number of periods of the average of the standard
deviation. Only used when method="dynamic". Defaults to 10.
- <u>minimum_window (int, optional):</u> The shortest period of the RSI. Only used when
method="dynamic". Defaults to 5.
- <u>maximum_window (int, optional):</u> The longest period of the RSI. Only used when
method="dynamic". Defaults to 30.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame or pd.Series:
Relative Strength Index (RSI) values, between 0 and 100.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates the
RSI for each asset in the Toolkit instance.
- RSI: the RSI agrees with TA-Lib's RSI.
- ConnorsRSI: equals TA-Lib's CRSI. It starts `rank_window` + 1 periods after the first
price, the first percent rank of a return.
- Laguerre RSI: on the same scale of 0 to 100 as the other variants, as pandas-ta-classic's
lrsi, where Ehlers' listing and the model function
`cycle_model.get_laguerre_relative_strength_index` give a decimal between 0 and 1;
otherwise they are equal. The filter elements start on the first price of each
ticker's own history, as pandas-ta-classic starts them, so the first period is NaN;
Ehlers' listing starts them from zero. When the four elements are equal (CU + CD is
zero) the value before is kept, as in Ehlers' listing, where pandas-ta-classic gives 0.
- Dynamic Momentum Index: the period changes every period, which leaves no single period for Wilder's
recursive average, so each period's RSI sums the gains and losses of its own last
`Period` changes (Cutler's RSI), the summed form Chande also uses for his Momentum
Oscillator (`get_chande_momentum_oscillator`). The standard deviation is the sample
standard deviation (ddof=1). finta's DYMI rounds the Volatility Index before the
division and takes an exponentially smoothed RSI over the periods before the current
one, so it differs from this by up to 50 points.
- Intraday Momentum Index: the IMI agrees with TA-Lib's IMI, except on a window in which every period
closed at its open, which has no IMI (NaN) where TA-Lib returns 50.
- When growth is requested, the method calculates the growth of the RSI
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["BTCUSD", "ETHUSD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_relative_strength_index().tail(5)
```

Which returns:

| Date       |   BTCUSD |   ETHUSD |   Benchmark |
|:-----------|---------:|---------:|------------:|
| 2025-12-27 |  44.6846 |  45.0659 |    nan      |
| 2025-12-28 |  44.9649 |  45.241  |    nan      |
| 2025-12-29 |  42.4043 |  44.276  |     58.6691 |
| 2025-12-30 |  47.7803 |  47.2561 |     57.6091 |
| 2025-12-31 |  44.643  |  46.9887 |     51.5337 |

---

## get_true_strength_index
Calculate the True Strength Index (TSI) or the SMI Ergodic Indicator and Oscillator, which show the direction and strength of momentum.

Both are the double-smoothed price change as a share of the double-smoothed absolute price change.

The True Strength Index of Blau (1995, "Momentum, Direction, and Divergence") smooths the one-period price change twice with Exponential Moving Averages and divides it by the same double smoothing of the absolute change. The double smoothing filters out noise while lagging less than a single long average, and the division bounds the result between -100 (every change down) and +100 (every change up).

The SMI Ergodic Indicator, also of Blau (1995), is the True Strength Index with short smoothing periods, and its signal line an EMA of the indicator. The SMI Ergodic Oscillator, the histogram, is the difference between the two, in the way the MACD histogram is the MACD line minus its signal line.

The formula for the True Strength Index is as follows:

$$
\text{Momentum} = \operatorname{Close}(t) - \operatorname{Close}(t - 1)
$$

$$
\text{TSI} = \frac{100 \cdot \operatorname{EMA}(\operatorname{EMA}(\text{Momentum},\; \text{long\_window}),\; \text{short\_window})}{\operatorname{EMA}(\operatorname{EMA}(\left|\text{Momentum}\right|,\; \text{long\_window}),\; \text{short\_window})}
$$

$$
\text{Signal Line} = \operatorname{EMA}(\text{TSI},\; \text{signal\_window})
$$

The formula for the SMI Ergodic Indicator is as follows:

$$
\text{Momentum} = \operatorname{Close}(t) - \operatorname{Close}(t - 1)
$$

$$
\text{Smoothed Momentum} = \operatorname{EMA}(\operatorname{EMA}(\text{Momentum},\; \text{long\_window}),\; \text{short\_window})
$$

$$
\text{Smoothed Absolute Momentum} = \operatorname{EMA}(\operatorname{EMA}(\left|\text{Momentum}\right|,\; \text{long\_window}),\; \text{short\_window})
$$

$$
\text{SMI Ergodic Indicator} = \frac{100 \cdot \text{Smoothed Momentum}}{\text{Smoothed Absolute Momentum}}
$$

$$
\text{Signal Line} = \operatorname{EMA}(\text{SMI Ergodic Indicator},\; \text{signal\_window})
$$

$$
\text{Histogram} \;(\text{SMI Ergodic Oscillator}) = \text{SMI Ergodic Indicator} - \text{Signal Line}
$$

Blau smooths the TSI over 25 and then 13 periods; the 7-period signal line is the one StockCharts uses. The common parameters of the SMI Ergodic Indicator are 20, 5 and 5. The TSI crossing zero means the smoothed momentum has turned, crossing its signal line is the faster trigger, and readings beyond about +25 or -25 are read as overbought or oversold. Blau trades the direction of the SMI Ergodic Oscillator: a turn up from below zero is a buy signal, a turn down from above zero a sell signal. Like the RSI both are on a scale of -100 to 100 rather than a decimal.

**Also known as:** TSI, double smoothed momentum, SMI Ergodic, SMIIO, SMI Ergodic Oscillator, ergodic oscillator.

**References:**

- paper | Blau, W. (1995). "Momentum, Direction, and Divergence." Wiley.
- library | Referenced against TA-Lib's [TSI](https://ta-lib.org/functions/tsi.html){:target="_blank"}
- library | Referenced against pandas-ta-classic's [smi](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/momentum/smi.py#L13){:target="_blank"} (SMI Ergodic Indicator)

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>long_window (int &#124; None, optional):</u> The number of periods of the first EMA of the price
change. Defaults to None, which is 25 with method="standard" and 20 with
method="ergodic".
- <u>short_window (int &#124; None, optional):</u> The number of periods of the second EMA. Defaults
to None, which is 13 with method="standard" and 5 with method="ergodic".
- <u>signal_window (int &#124; None, optional):</u> The number of periods of the EMA of the indicator
that gives the signal line. Defaults to None, which is 7 with method="standard" and 5
with method="ergodic".
- <u>method (str, optional):</u> Options are: "standard" (the True Strength Index and its signal line),
"ergodic" (the SMI Ergodic Indicator, its signal line and the histogram, the SMI Ergodic
Oscillator). Defaults to "standard".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator lines.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: True Strength Index and Signal Line values, or for the
ergodic form the SMI Ergodic Indicator, Signal Line and Histogram (the SMI Ergodic
Oscillator) values, between -100 and 100.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the True Strength Index or the SMI Ergodic lines for each asset in the Toolkit instance.
- Every EMA is seeded with the simple average of its first values and is missing
before it, as in TA-Lib and StockCharts, so the indicator starts `long_window` +
`short_window` - 1 periods after the first price and the signal line (and histogram)
`signal_window` - 1 periods later.
- A stretch without any price change leaves the indicator missing.
- The TSI agrees with TA-Lib's TSI, which has no signal line, with either set of windows.
The three SMI Ergodic columns agree with pandas-ta-classic's smi times 100, as
pandas-ta-classic uses a scale of -1 to 1.
- When growth is requested, the method calculates the growth of the indicator lines
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2024-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_true_strength_index().xs("MSFT", level=1, axis="columns").tail(5)
```

Which returns:

| Date       |   Signal Line |   True Strength Index |
|:-----------|--------------:|----------------------:|
| 2025-12-24 |      -12.4871 |               -8.9924 |
| 2025-12-26 |      -11.3039 |               -7.7544 |
| 2025-12-29 |      -10.1871 |               -6.8369 |
| 2025-12-30 |       -9.1285 |               -5.9526 |
| 2025-12-31 |       -8.3772 |               -6.1233 |

---

## get_balance_of_power
Calculate the Balance of Power (BOP): how far the close lies from the open as a share of the range, which shows whether buyers or sellers control the period.

The Balance of Power (BOP) indicator measures the strength of buyers versus sellers in the market. It relates the price change to the change in the asset's trading range.

The formula is as follows:

$$
\text{BOP} = \frac{\text{Close} - \text{Open}}{\text{High} - \text{Low}}
$$

**Also known as:** BOP, bull bear power.

**References:**

- paper | Igor Livshin, who created the indicator; described in Kaufman, P.J. (2005). "New Trading Systems and Methods." 4th ed. Wiley.
- library | Referenced against TA-Lib's [BOP](https://ta-lib.org/functions/bop.html){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the open, high and low prices are adjusted
for dividends in the same way.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the BOP.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame or pd.Series:
Balance of Power (BOP) values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates the
BOP for each asset in the Toolkit instance.
- The BOP agrees with TA-Lib's BOP.
- When growth is requested, the method calculates the growth of the BOP
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["^FTSE"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_balance_of_power().tail(5)
```

Which returns:

| Date       |    ^FTSE |   Benchmark |
|:-----------|---------:|------------:|
| 2025-12-24 |  -0.5953 |      0.802  |
| 2025-12-26 | nan      |     -0.1381 |
| 2025-12-29 |  -0.1212 |      0.099  |
| 2025-12-30 |   0.7846 |     -0.2222 |
| 2025-12-31 |  -0.279  |     -0.9239 |

---

## get_internal_bar_strength
Calculate the Internal Bar Strength (IBS): where the close lies within the range of its period, from 0 (at the low) to 1 (at the high).

The Internal Bar Strength is where the close sits within the period's own range: 0 for a close on the low, 1 for a close on the high. It is a mean-reversion measure: in equity indices and ETFs a close near the low of the day (an IBS below about 0.2) has tended to be followed by higher returns the next day, and a close near the high (above about 0.8) by lower returns.

The formula is as follows:

$$
\text{IBS} = \frac{\text{Close} - \text{Low}}{\text{High} - \text{Low}}
$$

**Also known as:** IBS, internal bar strength.

**References:**

- paper | Pagonidis, A.S. (2014). "The IBS Effect: Mean Reversion in Equity ETFs." NAAIM Founders Award paper.
- library | Referenced against TA-Lib's [IBS](https://ta-lib.org/functions/ibs.html){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the open, high and low prices are adjusted
for dividends in the same way.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: Internal Bar Strength (IBS) values as a decimal between 0 and 1.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the IBS for each asset in the Toolkit instance.
- The IBS agrees with TA-Lib's IBS, except on a period without a range (High equal to Low), which
has no IBS (NaN) where TA-Lib returns 0.5.
- When growth is requested, the method calculates the growth of the IBS
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["SPY", "QQQ"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_internal_bar_strength().tail(5)
```

Which returns:

| Date       |    QQQ |   Benchmark |
|:-----------|-------:|------------:|
| 2025-12-24 | 0.8633 |      0.8515 |
| 2025-12-26 | 0.3151 |      0.4351 |
| 2025-12-29 | 0.5284 |      0.5687 |
| 2025-12-30 | 0.0709 |      0.2172 |
| 2025-12-31 | 0.044  |      0.0372 |

---

## get_qstick
Calculate the Qstick: the average of the close minus the open over a window, which shows whether candles have been mostly rising or falling.

Qstick is the moving average of the candlestick bodies, Close - Open, over the window. It turns the colour of the recent candles into a number: above zero the periods closed above their open on average (white candles, buying pressure), below zero below their open (black candles, selling pressure). A cross of zero is read as a change of the pressure.

The formula is as follows:

$$
\text{Qstick} = \operatorname{SMA}(\text{Close} - \text{Open},\; \text{window})
$$

**Also known as:** Qstick, QSTICK, Q-stick.

**References:**

- paper | Chande, T.S. & Kroll, S. (1994). "The New Technical Trader." Wiley.
- library | Referenced against TA-Lib's [QSTICK](https://ta-lib.org/functions/qstick.html){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the open, high and low prices are adjusted
for dividends in the same way.
- <u>window (int, optional):</u> The number of periods of the moving average. Defaults to 10.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: Qstick values, in price units.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the Qstick for each asset in the Toolkit instance.
- Qstick agrees with TA-Lib's QSTICK and pandas-ta-classic's qstick.
- When growth is requested, the method calculates the growth of the Qstick
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_qstick().tail(5)
```

Which returns:

| Date       |    AAPL |   MSFT |   Benchmark |
|:-----------|--------:|-------:|------------:|
| 2025-12-24 | -0.6886 | 1.1227 |     -0.5913 |
| 2025-12-26 | -0.6577 | 0.5435 |     -1.0227 |
| 2025-12-29 | -0.5889 | 0.8936 |     -0.3578 |
| 2025-12-30 |  0.0399 | 1.571  |      0.0942 |
| 2025-12-31 | -0.2581 | 0.7081 |     -0.3881 |

---

## get_awesome_oscillator
Calculate the Awesome Oscillator (AO) or the Accelerator/Decelerator Oscillator (AC), which show the momentum of the market (AO) and whether it speeds up or slows down (AC).

The AO is the difference between a fast and a slow average of the median price.

The Awesome Oscillator measures market momentum by comparing a short-term and a long-term Simple Moving Average of the median price (the midpoint of each period's high and low, rather than the closing price). The Accelerator Oscillator is the Awesome Oscillator minus its own 5-period Simple Moving Average: where the Awesome Oscillator measures the momentum of the median price, the Accelerator Oscillator measures how that momentum changes, on Bill Williams' premise that momentum changes direction before price does. Both were developed by Bill Williams as part of his "Trading Chaos" collection of momentum indicators.

The formula for the Awesome Oscillator is as follows:

$$
\text{Median Price} = \frac{\text{High} + \text{Low}}{2}
$$

$$
\text{AO} = \operatorname{SMA}(\text{Median Price},\; \text{short\_window}) - \operatorname{SMA}(\text{Median Price},\; \text{long\_window})
$$

The formula for the Accelerator/Decelerator Oscillator is as follows:

$$
\text{Median Price} = \frac{\text{High} + \text{Low}}{2}
$$

$$
\text{AO} = \operatorname{SMA}(\text{Median Price},\; \text{short\_window}) - \operatorname{SMA}(\text{Median Price},\; \text{long\_window})
$$

$$
\text{AC} = \text{AO} - \operatorname{SMA}(\text{AO},\; \text{signal\_window})
$$

A cross of the AO above zero occurs exactly when the short-window SMA of the median price crosses above the long-window SMA, and vice versa for a cross below zero. Williams reads the AC by the colour of its bars: two rising bars in a row above zero (three below zero) are a buy signal, two falling bars below zero (three above zero) a sell signal.

**Also known as:** AO, Bill Williams Awesome Oscillator, AC, Accelerator Oscillator, Acceleration/Deceleration Oscillator, AC oscillator.

**References:**

- paper | Williams, B. (1995). "Trading Chaos: Applying Expert Techniques to Maximize Your Profits." Wiley.
- paper | Williams, B. (1998). "New Trading Dimensions: How to Profit from Chaos in Stocks, Bonds, and Commodities." Wiley.
- library | Referenced against TA-Lib's [AO](https://ta-lib.org/functions/ao.html){:target="_blank"}
- library | Referenced against TA-Lib's [AC](https://ta-lib.org/functions/ac.html){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the open, high and low prices are adjusted
for dividends in the same way.
- <u>short_window (int, optional):</u> The number of periods for the short-term SMA of the
median price. Defaults to 5.
- <u>long_window (int, optional):</u> The number of periods for the long-term SMA of the
median price. Defaults to 34.
- <u>signal_window (int, optional):</u> The number of periods for the SMA of the Awesome
Oscillator, with method="accelerator" only. Defaults to 5.
- <u>method (str, optional):</u> Options are: "standard" (the Awesome Oscillator), "accelerator" (the
Accelerator Oscillator). Defaults to "standard".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the oscillator.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: Awesome Oscillator (AO) or Accelerator Oscillator (AC)
values, in price units.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the AO or AC for each asset in the Toolkit instance.
- There is no academic journal citation for the Awesome and Accelerator Oscillators.
Like most of Bill Williams' indicators, they are practitioner-developed tools rather
than ones derived from a published financial paper; the standard textbook sources are
Williams' books above.
- The AO agrees with TA-Lib's AO, and the AC with TA-Lib's AC; the AC starts
`long_window` + `signal_window` — 2 periods after the first price.
- When growth is requested, the method calculates the growth of the oscillator
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["SOLUSD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_awesome_oscillator().tail(5)
```

Which returns:

| Date       |   SOLUSD |   Benchmark |
|:-----------|---------:|------------:|
| 2025-12-27 |  -8.9048 |    nan      |
| 2025-12-28 |  -8.6621 |    nan      |
| 2025-12-29 |  -7.5992 |     10.4586 |
| 2025-12-30 |  -6.6618 |     11.0505 |
| 2025-12-31 |  -5.546  |     10.5955 |

---

## get_vortex_indicator
Calculate the Vortex Indicator: the upward and downward movement of the prices relative to their true range, whose crossings mark the start of a new trend.

The Vortex Indicator quantifies the presence and strength of a directional trend by comparing each period's price movement away from the prior period's range to the period's overall volatility (True Range). It consists of two lines, VI+ and VI-, whose crossovers signal potential trend changes: VI+ above VI- suggests an uptrend is in control, VI- above VI+ suggests a downtrend is in control.

The formula is as follows:

$$
\text{VM}^{+} = \left|\operatorname{High}(t) - \operatorname{Low}(t-1)\right|
$$

$$
\text{VM}^{-} = \left|\operatorname{Low}(t) - \operatorname{High}(t-1)\right|
$$

$$
\text{VI}^{+} = \frac{\operatorname{Sum}(\text{VM}^{+},\; \text{window})}{\operatorname{Sum}(\text{True Range},\; \text{window})}
$$

$$
\text{VI}^{-} = \frac{\operatorname{Sum}(\text{VM}^{-},\; \text{window})}{\operatorname{Sum}(\text{True Range},\; \text{window})}
$$

**Also known as:** VI, Vortex Indicator +/-, trend direction indicator.

**References:**

- library | Referenced against TA-Lib's [VORTEX](https://ta-lib.org/functions/vortex.html){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the open, high and low prices are adjusted
for dividends in the same way.
- <u>window (int, optional):</u> The number of periods to sum the directional movement and
true range over. Defaults to 14.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the VI+ and VI- values.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame:
VI+ and VI- values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the Vortex Indicator values for each asset in the Toolkit instance.
- Reference: Botes, E., & Siepman, D. (2010). "The Vortex Indicator." Technical Analysis
of Stocks & Commodities, 28(1), 20-30.
- VI+ and VI- agree with TA-Lib's VORTEX.
- When growth is requested, the method calculates the growth of the VI+ and VI-
over the given lag.


**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AUDUSD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_vortex_indicator().xs("AUDUSD", level=1, axis="columns").tail(5)
```

Which returns:

| Date       |    VI+ |    VI- |
|:-----------|-------:|-------:|
| 2025-12-26 | 1.1422 | 0.9189 |
| 2025-12-28 | 1.1661 | 0.8887 |
| 2025-12-29 | 1.1108 | 0.8889 |
| 2025-12-30 | 1.1099 | 0.8697 |
| 2025-12-31 | 1.0576 | 0.9069 |

---

## get_elder_ray_index
Calculate the Elder Ray Index: how far the high (Bull Power) and the low (Bear Power) lie from an exponential moving average, which shows the strength of the buyers and the sellers.

The Elder Ray Index measures buying and selling pressure in the market relative to a trend baseline (an Exponential Moving Average of the closing price). Bull Power captures how far the high extends above the EMA (buying pressure), while Bear Power captures how far the low extends below the EMA (selling pressure).

The formula is as follows:

$$
\text{Bull Power} = \text{High} - \operatorname{EMA}(\text{Close},\; \text{window})
$$

$$
\text{Bear Power} = \text{Low} - \operatorname{EMA}(\text{Close},\; \text{window})
$$

**Also known as:** Elder Ray, Bull Power, Bear Power.

**References:**

- library | Referenced against TA-Lib's [ERI](https://ta-lib.org/functions/eri.html){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the open, high and low prices are adjusted
for dividends in the same way.
- <u>window (int, optional):</u> The number of periods for the EMA used as the trend baseline.
Defaults to 13, as originally proposed by Elder.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Bull and Bear Power.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame:
Bull Power and Bear Power values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the Elder Ray Index values for each asset in the Toolkit instance.
- When the close is above the EMA (uptrend), Bull Power tends to stay positive and Bear
Power moves toward zero from below; when the close is below the EMA (downtrend), both
tend to be negative.
- Reference: Elder, A. (1993). "Trading for a Living." Wiley.
- Bull Power and Bear Power agree with TA-Lib's ERI.
- When growth is requested, the method calculates the growth of the Bull and Bear Power
over the given lag.


**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["HGUSD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_elder_ray_index().xs("HGUSD", level=1, axis="columns").tail(5)
```

Which returns:

| Date       |   Bear Power |   Bull Power |
|:-----------|-------------:|-------------:|
| 2025-12-26 |       0.1171 |       0.3356 |
| 2025-12-28 |       0.1638 |       0.3223 |
| 2025-12-29 |      -0.0388 |       0.3272 |
| 2025-12-30 |      -0.0877 |       0.1728 |
| 2025-12-31 |       0.0063 |       0.1473 |

---

## get_rate_of_change
Calculate the Rate of Change (ROC), as a percentage or in price units (the Momentum): the change of the price over a window, the speed at which the price moves.

The Rate of Change is a pure momentum oscillator that measures the percentage change in price between the current period and the price a fixed number of periods ago. It oscillates around zero: positive values indicate price is higher than `window` periods ago (upward momentum), while negative values indicate price is lower (downward momentum). The Momentum is the same change in price units: the simplest measure of the speed of a move. Momentum that falls while the price still rises says the move slows down. The Rate of Change is the change as a share of the earlier price, which can be compared across stocks; the Momentum is in the currency of the price.

The formula is as follows, per method:

$$
\text{Rate of Change:}\;\; \text{ROC} = \frac{\operatorname{Close}(t)}{\operatorname{Close}(t - \text{window})} - 1
$$

$$
\text{Momentum:}\;\; \text{Momentum} = \operatorname{Close}(t) - \operatorname{Close}(t - \text{window})
$$

**Also known as:** ROC, Price Rate of Change, momentum, MOM, price momentum, momentum oscillator.

**References:**

- paper | Murphy, J.J. (1999). "Technical Analysis of the Financial Markets." New York Institute of Finance.
- paper | Pring, M.J. (1991). "Technical Analysis Explained." 3rd ed. McGraw-Hill.
- library | Referenced against TA-Lib's [ROCP](https://ta-lib.org/functions/rocp.html){:target="_blank"}
- library | Referenced against TA-Lib's [MOM](https://ta-lib.org/functions/mom.html){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int, optional):</u> Number of periods to look back for the rate of change
calculation. Defaults to None, which uses 12 for "percentage" and 10 for "absolute".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Rate of Change.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>method (str, optional):</u> Options are: "percentage" (the Rate of Change as a decimal), "absolute" (the
Momentum in price units). Defaults to "percentage".
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: Rate of Change values as a decimal (0.05 is 5%), or for the
Momentum, the change in price in price units.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the Rate of Change for each asset in the Toolkit instance.
- The Rate of Change is a decimal and agrees with TA-Lib's ROCP; TA-Lib's ROC is the same in
percent.
- Momentum: the Momentum agrees with TA-Lib's MOM, pandas-ta-classic's mom and finta's MOM.
- When growth is requested, the method calculates the growth of the Rate of Change
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["GCUSD", "SIUSD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_rate_of_change().tail(5)
```

Which returns:

| Date       |   GCUSD |   SIUSD |   Benchmark |
|:-----------|--------:|--------:|------------:|
| 2025-12-26 |  0.0518 |  0.245  |      0.0136 |
| 2025-12-28 |  0.0411 |  0.2629 |    nan      |
| 2025-12-29 |  0.0019 |  0.1081 |      0.0034 |
| 2025-12-30 |  0.0125 |  0.2305 |     -0.0002 |
| 2025-12-31 | -0.0075 |  0.0553 |      0.0032 |

---

## get_choppiness_index
Calculate the Choppiness Index (CHOP): how much of the range of a window the price travelled, from trending (near 0) to choppy and sideways (near 100).

The Choppiness Index quantifies whether the market is trending or moving sideways ("choppy") by comparing the sum of True Range over the window (a measure of the total price path travelled) to the net range the price actually covered over that same window (the distance between the highest high and the lowest low). When price travels a long, winding path but ends up covering little net ground, the index is high (near 100), signalling a choppy, range-bound market. When price travels efficiently in one direction, the index is low (near 0), signalling a trending market.

The formula is as follows:

$$
\text{CHOP} = \frac{100 \cdot \log_{10}\left(\frac{\operatorname{Sum}(\text{True Range},\; \text{window})}{\max(\text{High},\; \text{window}) - \min(\text{Low},\; \text{window})}\right)}{\log_{10}(\text{window})}
$$

With the true range as the box, the net range is that of the true highs and lows, Max(High, Previous Close) and Min(Low, Previous Close), the range the summed True Ranges span, so a gap between periods counts in both the path and the net range (TA-Lib's CHOPTR).

**Also known as:** CHOP, CHOPTR, Choppiness Index.

**References:**

- paper | Kaufman, P.J. (2013). "Trading Systems and Methods." 5th ed. Wiley.
- library | Referenced against TA-Lib's [CHOP](https://ta-lib.org/functions/chop.html){:target="_blank"}
- library | Referenced against TA-Lib's [CHOPTR](https://ta-lib.org/functions/choptr.html){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the open, high and low prices are adjusted
for dividends in the same way.
- <u>window (int, optional):</u> Number of periods to consider for the Choppiness Index
calculation. Defaults to 14.
- <u>range_method (str, optional):</u> The net range the summed True Range is divided by. Options are:
"high_low" (the highest high minus the lowest low), "true_range" (the highest true high minus
the lowest true low, TA-Lib's CHOPTR). Defaults to "high_low".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Choppiness Index.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: Choppiness Index values, bounded between 0 and 100.
Values above 61.8 are commonly read as signalling a choppy (range-bound) market,
while values below 38.2 are commonly read as signalling a trending market.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the Choppiness Index for each asset in the Toolkit instance.
- Developed by Australian commodities trader Bill Dreiss; there is no formal journal
citation. The standard textbook treatment is Kaufman, P.J. (2013). "Trading Systems
and Methods." 5th ed. Wiley.
- The Choppiness Index agrees with TA-Lib's CHOP, and with the true range as the box TA-Lib's
CHOPTR. The first period counts with its High — Low range, so the index starts on period
`window`, one period before TA-Lib's.
- When growth is requested, the method calculates the growth of the Choppiness
Index over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["EURUSD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_choppiness_index().tail(5)
```

Which returns:

| Date       |   EURUSD |   Benchmark |
|:-----------|---------:|------------:|
| 2025-12-26 |  58.6157 |     50.3552 |
| 2025-12-28 |  61.2072 |    nan      |
| 2025-12-29 |  61.879  |     49.989  |
| 2025-12-30 |  63.269  |     49.6207 |
| 2025-12-31 |  63.0658 |     48.7037 |

---

## get_efficiency_ratio
Calculate Kaufman's Efficiency Ratio (ER): the net change over a window as a share of the path travelled, from 0 (noise) to 1 (a straight trend).

The Efficiency Ratio compares the net change in price over the window with the path the price travelled to get there, the sum of the absolute changes of each period. A price that moves in a straight line has a ratio of 1; a price that ends where it started, however much it moved in between, has a ratio of 0. Perry Kaufman uses it to adapt the speed of his Adaptive Moving Average (the Kaufman adaptive method of `get_moving_average`) to the noise in the market.

The formula is as follows:

$$
\text{Change} = \left|\operatorname{Close}(t) - \operatorname{Close}(t - \text{window})\right|
$$

$$
\text{Volatility} = \operatorname{Sum}(\left|\operatorname{Close}(i) - \operatorname{Close}(i - 1)\right|,\; \text{window})
$$

$$
\text{Efficiency Ratio} = \frac{\text{Change}}{\text{Volatility}}
$$

**Also known as:** ER, Kaufman Efficiency Ratio, fractal efficiency.

**References:**

- paper | Kaufman, P.J. (1995). "Smarter Trading: Improving Performance in Changing Markets." McGraw-Hill.
- library | Referenced against TA-Lib's [ER](https://ta-lib.org/functions/er.html){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int, optional):</u> The number of periods of the change and the path. Defaults to 10.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: Efficiency Ratio values as a decimal between 0 and 1.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the Efficiency Ratio for each asset in the Toolkit instance.
- The Efficiency Ratio agrees with TA-Lib's ER, pandas-ta-classic's er and finta's ER, except on a
window without any change (flat prices), which has no ratio (NaN) where TA-Lib returns 1.
- When growth is requested, the method calculates the growth of the Efficiency Ratio
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_efficiency_ratio().tail(5)
```

Which returns:

| Date       |   AAPL |   MSFT |   Benchmark |
|:-----------|-------:|-------:|------------:|
| 2025-12-24 | 0.3144 | 0.3229 |      0.1201 |
| 2025-12-26 | 0.2993 | 0.1717 |      0.0818 |
| 2025-12-29 | 0.2901 | 0.4207 |      0.2395 |
| 2025-12-30 | 0.0852 | 0.743  |      0.2464 |
| 2025-12-31 | 0.2147 | 0.374  |      0.137  |

---

## get_vertical_horizontal_filter
Calculate the Vertical Horizontal Filter (VHF): the range of a window as a share of the path travelled, which shows whether prices trend or move sideways.

The Vertical Horizontal Filter tells a trending market from a congested one by dividing the range of the closes over the window (the vertical move) by the sum of the absolute changes from period to period (the path, horizontal in a range). A high or rising VHF says the price moves in one direction, which suits trend-following indicators; a low or falling VHF says it moves back and forth, which suits oscillators.

The formula is as follows:

$$
\text{VHF} = \frac{\max(\text{Close},\; \text{window}) - \min(\text{Close},\; \text{window})}{\operatorname{Sum}(\left|\operatorname{Close}(i) - \operatorname{Close}(i - 1)\right|,\; \text{window})}
$$

**Also known as:** VHF, vertical horizontal filter.

**References:**

- paper | White, A. (1991). "Trending or Trading? The Vertical Horizontal Filter." Futures Magazine.
- library | Referenced against TA-Lib's [VHF](https://ta-lib.org/functions/vhf.html){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int, optional):</u> The number of periods of the range and the path. Defaults to 28.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: Vertical Horizontal Filter (VHF) values, a ratio between 0 and 1.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the VHF for each asset in the Toolkit instance.
- The VHF agrees with TA-Lib's VHF and pandas-ta-classic's vhf and starts `window` periods after the
first price, except on a window without any change (flat prices), which has no VHF (NaN) where TA-Lib
returns 0.
- When growth is requested, the method calculates the growth of the VHF
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_vertical_horizontal_filter().tail(5)
```

Which returns:

| Date       |   AAPL |   MSFT |   Benchmark |
|:-----------|-------:|-------:|------------:|
| 2025-12-24 | 0.3606 | 0.2618 |      0.3575 |
| 2025-12-26 | 0.3614 | 0.2547 |      0.3576 |
| 2025-12-29 | 0.3942 | 0.1559 |      0.3702 |
| 2025-12-30 | 0.3891 | 0.1661 |      0.3873 |
| 2025-12-31 | 0.3884 | 0.1701 |      0.3779 |

---

## get_know_sure_thing
Calculate the Know Sure Thing (KST): a weighted sum of four smoothed rates of change over increasing windows, which shows the momentum of the major price cycles.

The Know Sure Thing is a momentum oscillator developed by Martin Pring that combines four smoothed Rate of Change series, each calculated over a progressively longer lookback period, into a single weighted sum. Smoothing each Rate of Change with a Simple Moving Average before combining them reduces noise, while the increasing weights on the longer lookback periods give more influence to the more significant, longer-term price cycles. A signal line (a Simple Moving Average of the KST itself) is used to spot crossovers, in the same way the MACD line is compared to its signal line.

The formula is as follows:

$$
\operatorname{RCMA}(i) = \operatorname{SMA}(\operatorname{ROC}(\text{Close},\; \text{roc\_windows}\left[i\right]),\; \text{sma\_windows}\left[i\right])
$$

$$
\text{KST} = \operatorname{Sum}(\operatorname{RCMA}(i) \cdot \text{weights}\left[i\right]) \;\text{for}\; i = 1 \ldots 4
$$

$$
\text{Signal Line} = \operatorname{SMA}(\text{KST},\; \text{signal\_window})
$$

Pring smooths with Simple Moving Averages; `moving_average` and `signal_moving_average` smooth the Rates of Change and the signal line with another moving average instead, as TA-Lib's KSTEXT does.

**Also known as:** KST, KSTEXT, Pring's Know Sure Thing, Summed Rate of Change.

**References:**

- paper | Pring, M.J. (1992). "Summed Rate of Change (KST)." Technical Analysis of Stocks & Commodities, 10(9), 365-369.
- library | Referenced against TA-Lib's [KST](https://ta-lib.org/functions/kst.html){:target="_blank"}
- library | Referenced against TA-Lib's [KSTEXT](https://ta-lib.org/functions/kstext.html){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>roc_windows (list[int] &#124; None, optional):</u> The four lookback periods used for the
underlying Rate of Change calculations. Defaults to the standard
[10, 15, 20, 30].
- <u>sma_windows (list[int] &#124; None, optional):</u> The four Simple Moving Average
smoothing periods applied to each Rate of Change series. Defaults to the
standard [10, 10, 10, 15].
- <u>weights (list[int] &#124; None, optional):</u> The four weights applied to each smoothed
Rate of Change series before summing. Defaults to the standard [1, 2, 3, 4].
- <u>signal_window (int, optional):</u> Number of periods for the Simple Moving Average of
the KST used as the signal line. Defaults to 9.
- <u>moving_average (str, optional):</u> The moving average that smooths each Rate of Change. Options are:
"simple" (Simple Moving Average), "exponential" (Exponential Moving Average),
"double_exponential" (Double Exponential Moving Average), "triangular" (Triangular Moving
Average), "weighted" (Weighted Moving Average), "hull" (Hull Moving Average),
"kaufman_adaptive" (Kaufman Adaptive Moving Average). Defaults to "simple".
- <u>signal_moving_average (str, optional):</u> The moving average of the signal line. Options are:
"simple" (Simple Moving Average), "exponential" (Exponential Moving Average),
"double_exponential" (Double Exponential Moving Average), "triangular" (Triangular Moving
Average), "weighted" (Weighted Moving Average), "hull" (Hull Moving Average),
"kaufman_adaptive" (Kaufman Adaptive Moving Average). Defaults to "simple".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the KST and Signal Line.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame:
KST and Signal Line values, weighted sums of Rates of Change as decimals.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the Know Sure Thing values for each asset in the Toolkit instance.
- The KST and Signal Line are decimals and agree with TA-Lib's KST divided by 100, since TA-Lib's
KST is in percent. TA-Lib starts the KST on the first signal value.
- With other moving averages they agree with TA-Lib's KSTEXT with the same `rocmatype` and
`signalmatype` divided by 100: from the first value for the simple, weighted and triangular
averages, and after the warm-up for the recursive ones, since TA-Lib starts their recursion
later (within 0.01% after about 85 periods for exponential averages).
- When growth is requested, the method calculates the growth of the KST and Signal
Line over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["^GSPC"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_know_sure_thing().xs("^GSPC", level=1, axis="columns").tail(5)
```

Which returns:

| Date       |    KST |   Signal Line |
|:-----------|-------:|--------------:|
| 2025-12-24 | 0.1217 |        0.1297 |
| 2025-12-26 | 0.1149 |        0.1271 |
| 2025-12-29 | 0.1085 |        0.1233 |
| 2025-12-30 | 0.1088 |        0.1192 |
| 2025-12-31 | 0.1105 |        0.1166 |

---

## get_coppock_curve
Calculate the Coppock Curve: a weighted moving average of the sum of a long and a short rate of change, which shows long-term buying opportunities after a decline.

The Coppock Curve is a long-term momentum indicator that Edwin Coppock designed for monthly closes of a stock index, to time buying after a bear market (Coppock, 1962, "Practical Relative Strength Charting", Trendex Research Group, first presented in Barron's). He took the 11 and 14 months from the time an Episcopal bishop told him mourning takes, as the time investors need to get over a loss.

The formula is as follows:

$$
\text{Coppock Curve} = \operatorname{WMA}(\operatorname{ROC}(\text{Close},\; \text{long\_roc\_window}) + \operatorname{ROC}(\text{Close},\; \text{short\_roc\_window}),\; \text{wma\_window})
$$

$$
\operatorname{ROC}(\text{Close},\; n) = \frac{\operatorname{Close}(t)}{\operatorname{Close}(t - n)} - 1
$$

with WMA the linearly Weighted Moving Average, so the defaults give WMA10(ROC14 + ROC11). The windows count periods of the chosen `period`: the curve as Coppock defined it is monthly, the default of daily periods applies the same windows to days, as the other technical indicators do. The classic signal is the curve turning up while below zero; Coppock did not use it for sell signals. The Rates of Change are decimals, so the curve is a weighted sum of decimal returns (0.30 where charting platforms show 30).

**Also known as:** Coppock Indicator, Coppock Guide.

**References:**

- library | Referenced against TA-Lib's [COPPOCK](https://ta-lib.org/functions/coppock.html){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>long_roc_window (int, optional):</u> Number of periods of the longer Rate of Change.
Defaults to 14.
- <u>short_roc_window (int, optional):</u> Number of periods of the shorter Rate of Change.
Defaults to 11.
- <u>wma_window (int, optional):</u> Number of periods of the Weighted Moving Average of the
summed Rates of Change. Defaults to 10.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Coppock Curve.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: Coppock Curve values, weighted sums of Rates of Change as
decimals.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the Coppock Curve for each asset in the Toolkit instance.
- The curve starts max(`long_roc_window`, `short_roc_window`) + `wma_window` - 1
periods after the first price: 23 months with the defaults on monthly data, so start
about two years before the first value you need.
- The Coppock Curve is a decimal and agrees with TA-Lib's COPPOCK divided by 100, since TA-Lib's
is in percent.
- When growth is requested, the method calculates the growth of the Coppock Curve
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["^GSPC"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2016-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_coppock_curve(period="monthly").tail(5)
```

Which returns:

| Date    |   ^GSPC |   Benchmark |
|:--------|--------:|------------:|
| 2025-08 |  0.3174 |      0.3475 |
| 2025-09 |  0.3183 |      0.3481 |
| 2025-10 |  0.3173 |      0.3469 |
| 2025-11 |  0.3228 |      0.3521 |
| 2025-12 |  0.3274 |      0.357  |

---

## get_fisher_transform
Calculate the Fisher Transform: the prices' position within their range turned into a near-normal distribution, which makes the turning points sharper and easier to see.

The Fisher Transform of Ehlers (2002) turns the position of the median price within its recent range into a series that is close to normally distributed. An oscillator of the position spends most of its time in the middle and gives vague turning points; the transform stretches the values near the edges of the range, so the extremes, and the turns after them, become sharp and rare. The trigger is the previous value of the transform, and the transform crossing its trigger marks a turn.

The formula is as follows:

$$
\text{Median Price} = \frac{\text{High} + \text{Low}}{2}
$$

$$
\text{Lowest} = \min(\text{Median Price},\; \text{window})\;\;\text{and}\;\; \text{Highest} = \max(\text{Median Price},\; \text{window})
$$

$$
\text{Position} = \frac{\text{Median Price} - \text{Lowest}}{\text{Highest} - \text{Lowest}}
$$

$$
\operatorname{Value}(t) = 0.66 \cdot (\text{Position} - 0.5) + 0.67 \cdot \operatorname{Value}(t - 1),\;\; \text{set to 0.999 above 0.99 and to -0.999 below -0.99}
$$

$$
\text{Fisher Transform}(t) = 0.5 \cdot \ln\left(\frac{1 + \operatorname{Value}(t)}{1 - \operatorname{Value}(t)}\right) + 0.5 \cdot \text{Fisher Transform}(t - 1)
$$

$$
\operatorname{Trigger}(t) = \text{Fisher Transform}(t - 1)
$$

Value and Fisher Transform start from 0, as in Ehlers' published formula. The transform is centred on zero and bounded by ln(1999), about -7.6 and 7.6.

**Also known as:** Fisher, Ehlers Fisher Transform, FISHT.

**References:**

- paper | Ehlers, J.F. (2002). "Using the Fisher Transform." Technical Analysis of Stocks & Commodities, 20(11).
- paper | Ehlers, J.F. (2004). "Cybernetic Analysis for Stocks and Futures." Wiley.
- library | Referenced against TA-Lib's [FISHER](https://ta-lib.org/functions/fisher.html){:target="_blank"}
- library | Shares similar logic as pandas-ta-classic's [fisher](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/momentum/fisher.py#L36){:target="_blank"}
- library | Shares similar logic as finta's [FISH](https://github.com/peerchemist/finta/blob/1.3/finta/finta.py#L1827){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the high and low prices are adjusted
for dividends in the same way.
- <u>window (int, optional):</u> The number of periods of the range of the median price.
Defaults to 10.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Fisher Transform and trigger.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: Fisher Transform and Trigger values, centred on zero.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the Fisher Transform and trigger for each asset in the Toolkit instance.
- The Fisher Transform agrees with TA-Lib's FISHER and starts `window` - 1 periods after the first price,
the trigger one period later (TA-Lib gives the first trigger the value 0).
- A window in which the median price did not move gives the neutral position 0.5, as in TA-Lib, so the
transform decays towards zero.
- pandas-ta-classic's fisher (9 periods by default) starts one period later and equals it after the
first values; finta's FISH smooths with exponential averages of 5 and 3 periods instead of
Ehlers' constants, a different series.
- When growth is requested, the method calculates the growth of the Fisher Transform and trigger
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2024-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_fisher_transform().xs("AAPL", level=1, axis="columns").tail(5)
```

Which returns:

| Date       |   Fisher Transform |   Trigger |
|:-----------|-------------------:|----------:|
| 2025-12-24 |            -1.5593 |   -1.9612 |
| 2025-12-26 |            -1.1485 |   -1.5593 |
| 2025-12-29 |            -0.8195 |   -1.1485 |
| 2025-12-30 |            -0.4022 |   -0.8195 |
| 2025-12-31 |            -0.1073 |   -0.4022 |

---

## get_inverse_fisher_transform_rsi
Calculate the Inverse Fisher Transform of the RSI: the smoothed Relative Strength Index squeezed between -1 and 1, which makes its overbought and oversold signals clearer.

The inverse Fisher transform (the hyperbolic tangent) of Ehlers (2004) squeezes a series into the range from -1 to 1 with most values close to the edges. Applied to a rescaled and smoothed short Relative Strength Index, it turns the RSI into a nearly binary signal that switches quickly between overbought and oversold. Ehlers buys when it crosses above -0.5 and sells when it crosses below 0.5.

The formula is as follows:

$$
\text{Value}\; 1 = 0.1 \cdot (\operatorname{RSI}(\text{Close},\; \text{rsi\_window}) - 50)
$$

$$
\text{Value}\; 2 = \operatorname{WMA}(\text{Value}\; 1,\; \text{wma\_window})
$$

$$
\text{IFT RSI} = \frac{\exp(2 \cdot \text{Value}\; 2) - 1}{\exp(2 \cdot \text{Value}\; 2) + 1} = \operatorname{tanh}(\text{Value}\; 2)
$$

Ehlers uses a 5-period RSI and a 9-period weighted moving average.

**Also known as:** IFT RSI, IFTRSI, Inverse Fisher RSI.

**References:**

- paper | Ehlers, J.F. (2004). "The Inverse Fisher Transform." Technical Analysis of Stocks & Commodities, 22(5).
- library | Shares similar logic as finta's [IFT_RSI](https://github.com/peerchemist/finta/blob/1.3/finta/finta.py#L714){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>rsi_window (int, optional):</u> The number of periods of the RSI. Defaults to 5.
- <u>wma_window (int, optional):</u> The number of periods of the weighted moving average of
the rescaled RSI. Defaults to 9.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the IFT RSI.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: IFT RSI values, between -1 and 1.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the IFT RSI for each asset in the Toolkit instance.
- The RSI is that of `get_relative_strength_index` (Wilder's smoothing, seeded with a simple average,
as TA-Lib's RSI), so the IFT RSI starts `rsi_window` + `wma_window` - 1 periods after the
first price.
- finta's IFT_RSI returns (Value $$2^{2} - 1$$) / (Value $$2^{2} + 1$$) instead of the hyperbolic tangent, with an
RSI from an unseeded exponential average; this follows Ehlers' formula.
- When growth is requested, the method calculates the growth of the IFT RSI
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2024-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_inverse_fisher_transform_rsi().tail(5)
```

Which returns:

| Date       |    AAPL |   MSFT |   Benchmark |
|:-----------|--------:|-------:|------------:|
| 2025-12-24 | -0.8895 | 0.6215 |      0.6121 |
| 2025-12-26 | -0.8224 | 0.765  |      0.8322 |
| 2025-12-29 | -0.6882 | 0.8175 |      0.8765 |
| 2025-12-30 | -0.6065 | 0.8526 |      0.8845 |
| 2025-12-31 | -0.6548 | 0.6957 |      0.759  |

---

## get_kdj_indicator
Calculate the KDJ indicator: the Stochastic Oscillator's %K and %D with the J line that leads them, to show overbought and oversold levels and turning points.

The KDJ indicator is a stochastic oscillator, widely used in Chinese and other Asian markets, that smooths the raw stochastic with Wilder's average instead of a simple one and adds a third line, J, which extrapolates K away from D. J leaves the 0 to 100 range when the momentum is strong, so J above 100 (or below 0) is read as overbought (or oversold) before K and D get there, and K crossing D is the trade signal, as with the stochastic.

The formula is as follows:

$$
\text{RSV} = \frac{100 \cdot (\text{Close} - \text{Lowest Low}(\text{window}))}{\text{Highest High}(\text{window}) - \text{Lowest Low}(\text{window})}
$$

$$
K = \text{Wilder's MA}(\text{RSV},\; k_{\text{window}})
$$

$$
D = \text{Wilder's MA}(K,\; d_{\text{window}})
$$

$$
J = 3 \cdot K - 2 \cdot D
$$

Wilder's moving average is the recursion $$K (t) = K (t - 1)$$ + (RSV(t) - K(t - 1)) / k_window, written SMA(RSV, 3, 1) in the formula language of Asian charting platforms. The KDJ has no single primary source; it extends Lane's stochastic (see `get_stochastic_oscillator`).

**Also known as:** KDJ, KDJ stochastic, random index.

**References:**

- paper | Lane, G.C. (1984). "Lane's Stochastics." Technical Analysis of Stocks & Commodities, 2(3).
- library | Referenced against TA-Lib's [KDJ](https://ta-lib.org/functions/kdj.html){:target="_blank"}
- library | Shares similar logic as pandas-ta-classic's [kdj](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/momentum/kdj.py#L17){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the high and low prices are adjusted
for dividends in the same way.
- <u>window (int, optional):</u> The number of periods of the high-low range of the RSV.
Defaults to 9.
- <u>k_window (int, optional):</u> The number of periods of Wilder's average of the RSV that
gives K. Defaults to 3.
- <u>d_window (int, optional):</u> The number of periods of Wilder's average of K that gives
D. Defaults to 3.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the K, D and J.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: K, D and J values; K and D between 0 and 100, J unbounded.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the K, D and J for each asset in the Toolkit instance.
- K, D and J agree with TA-Lib's KDJ (with its default RMA averages) and pandas-ta-classic's kdj. Every
Wilder average is seeded with the simple average of its first values, so K starts `window`
+ `k_window` - 2 periods after the first price and D and J `d_window` - 1 periods later;
TA-Lib starts K on the first D. Platforms that start K and D at 50 differ in the first few
dozen periods.
- A window without a range has no RSV (NaN), where TA-Lib and pandas-ta-classic use 0; the averages
carry on over it.
- When growth is requested, the method calculates the growth of the K, D and J
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2024-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_kdj_indicator().xs("AAPL", level=1, axis="columns").tail(5)
```

Which returns:

| Date       |       D |       J |       K |
|:-----------|--------:|--------:|--------:|
| 2025-12-24 | 34.2194 | 53.5727 | 40.6705 |
| 2025-12-26 | 37.2801 | 55.6444 | 43.4016 |
| 2025-12-29 | 42.7139 | 75.3166 | 53.5815 |
| 2025-12-30 | 47.7783 | 78.1645 | 57.907  |
| 2025-12-31 | 51.1539 | 71.4073 | 57.905  |

---

## get_premier_stochastic_oscillator
Calculate the Premier Stochastic Oscillator (PSO): the smoothed and normalised Stochastic %K squeezed between -1 and 1, which gives clearer overbought and oversold signals.

The Premier Stochastic Oscillator of Leibfarth (2008) rescales a short stochastic around zero, smooths it twice with an exponential average and squeezes the result between -1 and 1 with the inverse Fisher transform. The smoothing removes the noise of the stochastic and the transform keeps the oscillator near its extremes most of the time, so a reading that crosses back through 0.9 or -0.9 (or 0.2 and -0.2) stands out.

The formula is as follows:

$$
\%K = \frac{100 \cdot (\text{Close} - \text{Lowest Low}(\text{window}))}{\text{Highest High}(\text{window}) - \text{Lowest Low}(\text{window})}
$$

$$
\text{Normalized Stochastic} = 0.1 \cdot (\%K - 50)
$$

$$
\text{Smoothed Stochastic} = \operatorname{EMA}(\operatorname{EMA}(\text{Normalized Stochastic},\; \text{smooth\_window}),\; \text{smooth\_window})
$$

$$
\text{PSO} = \frac{\exp(\text{Smoothed Stochastic}) - 1}{\exp(\text{Smoothed Stochastic}) + 1}
$$

Leibfarth uses an 8-period stochastic and a smoothing of 5 periods (the square root of 25).

**Also known as:** PSO, Premier Stochastic.

**References:**

- paper | Leibfarth, L. (2008). "Premier Stochastic Oscillator." Technical Analysis of Stocks & Commodities, 26(8).
- library | Referenced against TA-Lib's [PSO](https://ta-lib.org/functions/pso.html){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the high and low prices are adjusted
for dividends in the same way.
- <u>window (int, optional):</u> The number of periods of the high-low range of %K.
Defaults to 8.
- <u>smooth_window (int, optional):</u> The number of periods of each of the two EMAs.
Defaults to 5.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the PSO.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: PSO values, between -1 and 1.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the PSO for each asset in the Toolkit instance.
- The PSO agrees with TA-Lib's PSO. Every EMA is seeded with the simple average of its first values and is
missing before it, so the PSO starts `window` + 2 * `smooth_window` - 3 periods after the
first price.
- A window without a range has no %K (NaN), where TA-Lib uses 50; the averages carry on over it.
- When growth is requested, the method calculates the growth of the PSO
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2024-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_premier_stochastic_oscillator().tail(5)
```

Which returns:

| Date       |    AAPL |   MSFT |   Benchmark |
|:-----------|--------:|-------:|------------:|
| 2025-12-24 | -0.6448 | 0.5466 |      0.5421 |
| 2025-12-26 | -0.4625 | 0.7272 |      0.7504 |
| 2025-12-29 | -0.1913 | 0.8145 |      0.8373 |
| 2025-12-30 |  0.0877 | 0.8577 |      0.8676 |
| 2025-12-31 |  0.1423 | 0.7679 |      0.8168 |

---

## get_stochastic_momentum_index
Calculate the Stochastic Momentum Index (SMI): where the close lies relative to the middle of the high-low range of a window, smoothed, from -100 to 100.

The Stochastic Momentum Index of Blau (1993) measures where the close sits relative to the midpoint of the high-low range, rather than to its low as the stochastic does, and smooths both the distance and the range twice with an exponential average before dividing. It runs from -100 (a close on the low) to +100 (a close on the high) around zero, is less erratic than the stochastic, and is read with its signal line and the levels -40 and 40.

The formula is as follows:

$$
\text{Distance} = \text{Close} - \frac{\text{Highest High}(\text{window}) + \text{Lowest Low}(\text{window})}{2}
$$

$$
\text{Range} = \text{Highest High}(\text{window}) - \text{Lowest Low}(\text{window})
$$

$$
\text{SMI} = \frac{100 \cdot \operatorname{EMA}(\operatorname{EMA}(\text{Distance},\; \text{long\_window}),\; \text{short\_window})}{0.5 \cdot \operatorname{EMA}(\operatorname{EMA}(\text{Range},\; \text{long\_window}),\; \text{short\_window})}
$$

$$
\text{Signal Line} = \operatorname{EMA}(\text{SMI},\; \text{signal\_window})
$$

Blau uses a 13-period range, smoothed over 25 and then 2 periods.

**Also known as:** SMI, Blau's stochastic momentum.

**References:**

- paper | Blau, W. (1993). "Stochastic Momentum." Technical Analysis of Stocks & Commodities, 11(1).
- paper | Blau, W. (1995). "Momentum, Direction, and Divergence." Wiley.
- library | Referenced against TA-Lib's [SMI](https://ta-lib.org/functions/smi.html){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the high and low prices are adjusted
for dividends in the same way.
- <u>window (int, optional):</u> The number of periods of the high-low range. Defaults to 13.
- <u>long_window (int, optional):</u> The number of periods of the first EMA of the distance
and the range. Defaults to 25.
- <u>short_window (int, optional):</u> The number of periods of the second EMA. Defaults to 2.
- <u>signal_window (int, optional):</u> The number of periods of the EMA of the SMI that gives
the signal line. Defaults to 9.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the SMI and signal line.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: Stochastic Momentum Index and Signal Line values, between -100 and 100.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the SMI and signal line for each asset in the Toolkit instance.
- The SMI and signal line agree with TA-Lib's SMI. Every EMA is seeded with the simple average of its first
values and is missing before it, so the SMI starts `window` + `long_window` +
`short_window` - 3 periods after the first price and the signal line `signal_window` - 1
periods later; TA-Lib starts both on the first signal value.
- A stretch in which the smoothed range is zero has no SMI (NaN), where TA-Lib returns 0.
- When growth is requested, the method calculates the growth of the SMI and signal line
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2024-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_stochastic_momentum_index().xs("AAPL", level=1, axis="columns").tail(5)
```

Which returns:

| Date       |   Signal Line |   Stochastic Momentum Index |
|:-----------|--------------:|----------------------------:|
| 2025-12-24 |        5.6181 |                     -7.0164 |
| 2025-12-26 |        3.113  |                     -6.9074 |
| 2025-12-29 |        1.194  |                     -6.4823 |
| 2025-12-30 |       -0.3191 |                     -6.3715 |
| 2025-12-31 |       -1.6769 |                     -7.108  |

---

## get_schaff_trend_cycle
Calculate the Schaff Trend Cycle (STC): a stochastic of the MACD, applied twice, from 0 to 100, which shows the turns of a trend faster than the MACD.

The Schaff Trend Cycle of Schaff (2002, 2008) applies a smoothed stochastic twice to the MACD line: it measures where the MACD sits within its range over the last cycle, smooths that, and does the same again. The result moves between 0 and 100 and turns earlier than the MACD, as it follows the MACD's cycle rather than its level. A turn up from below 25 is read as bullish and a turn down from above 75 as bearish.

The formula is as follows:

$$
\text{MACD} = \operatorname{EMA}(\text{Close},\; \text{short\_window}) - \operatorname{EMA}(\text{Close},\; \text{long\_window})
$$

$$
\text{Fraction}\; 1 = \frac{100 \cdot (\text{MACD} - \min(\text{MACD},\; \text{cycle\_window}))}{\max(\text{MACD},\; \text{cycle\_window}) - \min(\text{MACD},\; \text{cycle\_window})}
$$

$$
\operatorname{PF}(t) = \operatorname{PF}(t - 1) + \text{factor} \cdot (\text{Fraction} \;1(t) - \operatorname{PF}(t - 1))
$$

$$
\text{Fraction}\; 2 = \frac{100 \cdot (\text{PF} - \min(\text{PF},\; \text{cycle\_window}))}{\max(\text{PF},\; \text{cycle\_window}) - \min(\text{PF},\; \text{cycle\_window})}
$$

$$
\operatorname{STC}(t) = \operatorname{STC}(t - 1) + \text{factor} \cdot (\text{Fraction} \;2(t) - \operatorname{STC}(t - 1))
$$

A fraction over a window without a range keeps its previous value and each smoothing starts on its first input, as in Schaff (2008). Schaff uses 23, 50 and 10 with a factor of 0.5.

**Also known as:** STC, Schaff Trend Cycle indicator.

**References:**

- paper | Schaff, D. (2008). "Releasing the Code to the Schaff Trend Cycle." FX-Strategy.com.
- paper | Schaff, D. (2002). "Catching Currency Moves with the Schaff Trend Cycle Indicator." Chartpoint, July/August 2002.
- library | Referenced against TA-Lib's [STC](https://ta-lib.org/functions/stc.html){:target="_blank"}
- library | Shares similar logic as pandas-ta-classic's [stc](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/momentum/stc.py#L100){:target="_blank"}
- library | Shares similar logic as ta's [STCIndicator](https://github.com/bukosabino/ta/blob/0.11.0/ta/trend.py#L1093){:target="_blank"}
- library | Shares similar logic as finta's [STC](https://github.com/peerchemist/finta/blob/1.3/finta/finta.py#L2121){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>short_window (int, optional):</u> The number of periods of the short EMA of the MACD.
Defaults to 23.
- <u>long_window (int, optional):</u> The number of periods of the long EMA of the MACD.
Defaults to 50.
- <u>cycle_window (int, optional):</u> The number of periods of the range of each stochastic.
Defaults to 10.
- <u>factor (float, optional):</u> The smoothing factor of each stochastic. Defaults to 0.5.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the STC.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: STC values, between 0 and 100.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the STC for each asset in the Toolkit instance.
- The EMAs of the MACD are seeded with the simple average of their first values with an empty warm-up,
as in `get_moving_average_convergence_divergence`. TA-Lib's STC starts the short EMA on
the same period as the long one, so the two differ in the first values (up to 50 points)
and agree within 0.01 after about 200 periods and within 1e-5 after about 250 at the
default windows; on the same MACD line the two stochastic stages agree with TA-Lib's.
- pandas-ta-classic's stc (12 and 26 periods by default) equals it with the same windows after the
first values, and ta's STCIndicator, which smooths with a 3-period EMA (a factor of 0.5)
without a seed, within 1e-6 after about 500 periods. finta's STC smooths with 3-period
simple averages, a different series.
- When growth is requested, the method calculates the growth of the STC
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2024-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_schaff_trend_cycle().tail(5)
```

Which returns:

| Date       |   AAPL |    MSFT |   Benchmark |
|:-----------|-------:|--------:|------------:|
| 2025-12-24 | 0.0411 | 95.6845 |     18.5194 |
| 2025-12-26 | 0.0206 | 97.8422 |     35.7456 |
| 2025-12-29 | 0.0103 | 98.9211 |     60.1545 |
| 2025-12-30 | 0.0051 | 99.4606 |     80.0773 |
| 2025-12-31 | 0.0026 | 99.7303 |     87.8871 |

---

## get_wavetrend_oscillator
Calculate the WaveTrend Oscillator: how far the typical price lies from its average in units of its average distance, smoothed, to show overbought and oversold levels and turning points.

The WaveTrend Oscillator of LazyBear (2014) is a Commodity Channel Index built from exponential averages: the distance of the typical price from its EMA, divided by 0.015 times the EMA of that absolute distance, and smoothed with a longer EMA. Its signal line is a short simple average. Readings beyond 53 or 60 (or -53 and -60) are read as overbought (or oversold), and the oscillator crossing its signal line there as a turn.

The formula is as follows:

$$
\text{Typical Price} = \frac{\text{High} + \text{Low} + \text{Close}}{3}
$$

$$
\text{ESA} = \operatorname{EMA}(\text{Typical Price},\; \text{channel\_window})
$$

$$
D = \operatorname{EMA}(\left|\text{Typical Price} - \text{ESA}\right|,\; \text{channel\_window})
$$

$$
\text{CI} = \frac{\text{Typical Price} - \text{ESA}}{0.015 \cdot D}
$$

$$
\text{WaveTrend} = \operatorname{EMA}(\text{CI},\; \text{average\_window})
$$

$$
\text{Signal Line} = \operatorname{SMA}(\text{WaveTrend},\; \text{signal\_window})
$$

LazyBear's parameters are 10, 21 and 4.

**Also known as:** WaveTrend, WT, WTO, WT1 and WT2.

**References:**

- paper | LazyBear (2014). "WaveTrend Oscillator [WT]." TradingView published script.
- library | Referenced against TA-Lib's [WAVETREND](https://ta-lib.org/functions/wavetrend.html){:target="_blank"}
- library | Shares similar logic as finta's [WTO](https://github.com/peerchemist/finta/blob/1.3/finta/finta.py#L1802){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the high and low prices are adjusted
for dividends in the same way.
- <u>channel_window (int, optional):</u> The number of periods of the EMA of the typical
price and of its distance. Defaults to 10.
- <u>average_window (int, optional):</u> The number of periods of the EMA of the CI.
Defaults to 21.
- <u>signal_window (int, optional):</u> The number of periods of the SMA that gives the
signal line. Defaults to 4.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the WaveTrend and signal line.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: WaveTrend and Signal Line values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the WaveTrend and signal line for each asset in the Toolkit instance.
- The WaveTrend and signal line agree with TA-Lib's WAVETREND. Every EMA is seeded with the simple average
of its first values and is missing before it, so the WaveTrend starts 2 * `channel_window`
+ `average_window` - 3 periods after the first price and the signal line `signal_window` -
1 periods later. finta's WTO uses averages without a seed and equals it after the first
values.
- A stretch without any distance from the average has no CI (NaN), where TA-Lib returns 0.
- When growth is requested, the method calculates the growth of the WaveTrend and signal line
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2024-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_wavetrend_oscillator().xs("AAPL", level=1, axis="columns").tail(5)
```

Which returns:

| Date       |   Signal Line |   WaveTrend |
|:-----------|--------------:|------------:|
| 2025-12-24 |      -21.1082 |    -22.4463 |
| 2025-12-26 |      -22.0717 |    -20.284  |
| 2025-12-29 |      -21.7469 |    -19.6328 |
| 2025-12-30 |      -20.6589 |    -20.2723 |
| 2025-12-31 |      -20.8875 |    -23.3609 |

---

## get_derivative_oscillator
Calculate the Derivative Oscillator: a double-smoothed Relative Strength Index minus its average, which shows the momentum of the RSI itself.

The Derivative Oscillator of Constance Brown (1994) smooths the Relative Strength Index twice with an exponential average and subtracts a simple average of the result, the way the MACD histogram subtracts the signal line from the MACD. It shows the momentum of the smoothed RSI: a crossing of zero marks a turn of the RSI, and the distance from zero how far the smoothed RSI has moved from its mean.

The formula is as follows:

$$
\text{Double Smoothed RSI} = \operatorname{EMA}(\operatorname{EMA}(\operatorname{RSI}(\text{Close},\; \text{window}),\; \text{first\_window}),\; \text{second\_window})
$$

$$
\text{Derivative Oscillator} = \text{Double Smoothed RSI} - \operatorname{SMA}(\text{Double Smoothed RSI},\; \text{signal\_window})
$$

Brown uses a 14-period RSI, smoothed over 5 and then 3 periods, and a 9-period signal.

**Also known as:** DOSC, Brown's Derivative Oscillator.

**References:**

- paper | Brown, C.M. (1994). "The Derivative Oscillator: A New Approach for an Old Problem." MTA Journal, 42.
- paper | Brown, C.M. (1999). "Technical Analysis for the Trading Professional." McGraw-Hill.
- library | Referenced against TA-Lib's [DOSC](https://ta-lib.org/functions/dosc.html){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int, optional):</u> The number of periods of the RSI. Defaults to 14.
- <u>first_window (int, optional):</u> The number of periods of the first EMA of the RSI.
Defaults to 5.
- <u>second_window (int, optional):</u> The number of periods of the second EMA. Defaults to 3.
- <u>signal_window (int, optional):</u> The number of periods of the SMA subtracted from the
smoothed RSI. Defaults to 9.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Derivative Oscillator.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: Derivative Oscillator values, in RSI points around zero.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the Derivative Oscillator for each asset in the Toolkit instance.
- The Derivative Oscillator agrees with TA-Lib's DOSC and starts `window` + `first_window` +
`second_window` + `signal_window` - 3 periods after the first price.
- When growth is requested, the method calculates the growth of the Derivative Oscillator
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2024-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_derivative_oscillator().tail(5)
```

Which returns:

| Date       |    AAPL |   MSFT |   Benchmark |
|:-----------|--------:|-------:|------------:|
| 2025-12-24 | -4.319  | 3.3478 |      1.4327 |
| 2025-12-26 | -2.8918 | 3.7216 |      3.1297 |
| 2025-12-29 | -1.5792 | 3.6241 |      3.7512 |
| 2025-12-30 | -0.7486 | 3.2821 |      3.6025 |
| 2025-12-31 | -0.6816 | 2.1574 |      2.0585 |

---

## get_swing_index
Calculate Wilder's Swing Index and Accumulative Swing Index: the strength of each period's move compared with the previous period, and its running total, which shows the real direction of the prices.

The Swing Index of Wilder (1978) weighs the change of the close against the previous period's open and close and against the range of the current period, to measure the real direction of a period's move. Wilder accumulates it into the Accumulative Swing Index, a line that follows the price but filters out the moves that the open, high and low do not confirm: a breakout of the ASI through a previous high or low swing point confirms a breakout of the price.

The formula is as follows:

$$
A = \left|\text{High} - \operatorname{Close}(t - 1)\right|,\;\; B = \left|\text{Low} - \operatorname{Close}(t - 1)\right|,\;\; C = \left|\text{High} - \text{Low}\right|,\;\; D = \left|\operatorname{Close}(t - 1) - \operatorname{Open}(t - 1)\right|
$$

$$
R = A - 0.5 \cdot B + 0.25 \cdot D \;\text{when}\; A \;\text{is the largest of}\; A,\;\; B \text{ and } C
$$

$$
R = B - 0.5 \cdot A + 0.25 \cdot D \;\text{when}\; B \;\text{is the largest},\;\; \text{else}\;\; R = C + 0.25 \cdot D
$$

$$
K = \max(A,\; B)
$$

$$
N = (\text{Close} - \operatorname{Close}(t - 1)) + 0.5 \cdot (\text{Close} - \text{Open}) + 0.25 \cdot (\operatorname{Close}(t - 1) - \operatorname{Open}(t - 1))
$$

$$
\text{Swing Index} = 50 \cdot \frac{N}{R} \cdot \frac{K}{\text{limit\_move}}
$$

$$
\text{Accumulative Swing Index} = \text{Sum of the Swing Index since the first period}
$$

The limit move is the largest move a futures contract may make in one period. A stock has none, so `limit_move` is a scale in price units: the Swing Index stays within -100 and 100 only for moves within it, and only the shape of the ASI, not its level, carries meaning.

**Also known as:** SI, ASI, Wilder Swing Index, Accumulation Swing Index.

**References:**

- paper | Wilder, J.W. Jr. (1978). "New Concepts in Technical Trading Systems." Trend Research, section VIII "The Swing Index."
- library | Referenced against TA-Lib's [SI](https://ta-lib.org/functions/si.html){:target="_blank"}
- library | Referenced against TA-Lib's [ASI](https://ta-lib.org/functions/asi.html){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the open, high and low prices are adjusted
for dividends in the same way.
- <u>limit_move (float, optional):</u> The limit move that scales the index, in price units.
Defaults to 3.0, TA-Lib's default.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Swing Index and Accumulative Swing Index.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: Swing Index and Accumulative Swing Index values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the Swing Index and Accumulative Swing Index for each asset in the Toolkit instance.
- The Swing Index agrees with TA-Lib's SI. The first period has no previous period and no Swing Index, so
the Accumulative Swing Index starts on the second period, where it agrees with TA-Lib's ASI,
which gives the first period 0. The ASI accumulates from the first date of the Toolkit's
data.
- A period without any move (R equal to 0) has no Swing Index (NaN), where TA-Lib uses 0; the ASI
carries on over it. Neither is rounded, where Wilder rounded to whole numbers by hand.
- When growth is requested, the method calculates the growth of the Swing Index and Accumulative Swing Index
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2024-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_swing_index().xs("AAPL", level=1, axis="columns").tail(5)
```

Which returns:

| Date       |   Accumulative Swing Index |   Swing Index |
|:-----------|---------------------------:|--------------:|
| 2025-12-24 |                    3959.09 |       36.229  |
| 2025-12-26 |                    3955.29 |       -3.8043 |
| 2025-12-29 |                    3960.88 |        5.5885 |
| 2025-12-30 |                    3957.58 |       -3.2993 |
| 2025-12-31 |                    3938.2  |      -19.3803 |

---

## get_quantitative_qualitative_estimation
Calculate the Quantitative Qualitative Estimation (QQE): a smoothed Relative Strength Index with a trailing stop line a multiple of its own average move away, whose crossings show the turns of a trend.

The Quantitative Qualitative Estimation smooths the Relative Strength Index with an exponential average (the fast line) and trails it with a stop line (the QQE, the slow line), placed a multiple of the RSI's own average move away, in the way an Average True Range stop trails the price. The stop only moves towards the RSI while the RSI moves away from it and jumps to the other side when the RSI crosses it, so the RSI crossing the QQE line marks a change of trend. The QQE is a community indicator of the MetaTrader platform without a published primary source.

The formula is as follows:

$$
\text{RSI Moving Average} = \operatorname{EMA}(\operatorname{RSI}(\text{Close},\; \text{window}),\; \text{smooth\_window})
$$

$$
\text{Average Move} = \operatorname{EMA}(\operatorname{EMA}(\left|\text{RSI Moving Average}(t) - \text{RSI Moving Average}(t - 1)\right|,\; 2 \cdot \text{window} - 1),\; 2 \cdot \text{window} - 1)
$$

$$
\text{Distance} = \text{multiplier} \cdot \text{Average Move}
$$

$$
\operatorname{QQE}(t) = \max(\operatorname{QQE}(t - 1),\; \text{RSI Moving Average}(t) - \operatorname{Distance}(t)) \;\text{while the RSI Moving Average stays above QQE}
$$

$$
\operatorname{QQE}(t) = \min(\operatorname{QQE}(t - 1),\; \text{RSI Moving Average}(t) + \operatorname{Distance}(t)) \;\text{while it stays below QQE}
$$

$$
\operatorname{QQE}(t) = \text{RSI Moving Average}(t) - / + \operatorname{Distance}(t) \;\text{on the period it crosses QQE}
$$

The EMA over 2 * window - 1 periods has the smoothing constant 1 / window of Wilder's average. The common parameters are 14, 5 and 4.236.

**Also known as:** QQE, QQE fast and slow line.

**References:**

- library | Referenced against pandas-ta-classic's [qqe](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/momentum/qqe.py#L71){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int, optional):</u> The number of periods of the RSI. Defaults to 14.
- <u>smooth_window (int, optional):</u> The number of periods of the EMA of the RSI. Defaults
to 5.
- <u>multiplier (float, optional):</u> The multiple of the average move of the RSI Moving Average
that sets the distance of the QQE line. Defaults to 4.236.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the QQE and RSI Moving Average.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: QQE and RSI Moving Average values, in RSI points.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the QQE and RSI Moving Average for each asset in the Toolkit instance.
- The RSI is that of `get_relative_strength_index` and every EMA is seeded with the simple average of
its first values with an empty warm-up, so the RSI Moving Average starts `window` +
`smooth_window` - 1 periods after the first price and the QQE 2 * (2 * `window` - 1) - 1
periods later, at the RSI Moving Average minus the distance.
- The RSI Moving Average and QQE agree with pandas-ta-classic's qqe, except that its line switches sides
when the RSI Moving Average crosses the band on the other side, which can keep it on the
old side for a few more periods (3 of 757 days on the test data); this follows the
original MetaTrader indicator, which switches on the period of the crossing.
- When growth is requested, the method calculates the growth of the QQE and RSI Moving Average
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2024-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_quantitative_qualitative_estimation().xs("AAPL", level=1, axis="columns").tail(5)
```

Which returns:

| Date       |     QQE |   RSI Moving Average |
|:-----------|--------:|---------------------:|
| 2025-12-24 | 53.9827 |              48.2126 |
| 2025-12-26 | 53.9827 |              48.5314 |
| 2025-12-29 | 53.9827 |              49.0098 |
| 2025-12-30 | 53.9827 |              48.8135 |
| 2025-12-31 | 53.9827 |              47.7724 |

---

## get_price_zone_oscillator
Calculate the Price Zone Oscillator (PZO): the share of the recent closes that moved up, from -100 to 100, which shows overbought and oversold levels and the direction of a trend.

The Price Zone Oscillator of Khalil and Steckler (2011) counts each close as positive when it closed above the previous close and as negative when it closed below, and divides the EMA of these signed closes by the EMA of the closes. It is thereby the share of the recent price action that went up, on a scale of -100 to 100: above 40 is overbought and below -40 oversold in a trendless market, while in a trend Khalil and Steckler use the crossings of zero, 15 and -5.

The formula is as follows:

$$
\text{Signed Close} = \operatorname{sign}(\operatorname{Close}(t) - \operatorname{Close}(t - 1)) \cdot \operatorname{Close}(t)
$$

$$
\text{PZO} = \frac{100 \cdot \operatorname{EMA}(\text{Signed Close},\; \text{window})}{\operatorname{EMA}(\text{Close},\; \text{window})}
$$

Both EMAs run over the periods with a change, so they start on the same period.

**Also known as:** PZO.

**References:**

- paper | Khalil, W. & Steckler, D. (2011). "Entering The Price Zone." Technical Analysis of Stocks & Commodities, 29(6), 28-35.
- library | Shares similar logic as finta's [PZO](https://github.com/peerchemist/finta/blob/1.3/finta/finta.py#L1542){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int, optional):</u> The number of periods of the EMAs. Defaults to 14.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the PZO.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: PZO values, between -100 and 100.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the PZO for each asset in the Toolkit instance.
- Every EMA is seeded with the simple average of its first values and is missing before it, so the PZO
starts `window` periods after the first price. finta's PZO uses averages without a seed
and equals it after the first values.
- When growth is requested, the method calculates the growth of the PZO
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2024-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_price_zone_oscillator().tail(5)
```

Which returns:

| Date       |    AAPL |    MSFT |   Benchmark |
|:-----------|--------:|--------:|------------:|
| 2025-12-24 | 23.8305 | 30.886  |     41.0541 |
| 2025-12-26 |  7.3734 | 13.3243 |     22.033  |
| 2025-12-29 | 19.7029 | -1.8518 |      5.6525 |
| 2025-12-30 |  3.8001 | 11.7892 |     -8.5015 |
| 2025-12-31 | -9.9432 | -3.071  |    -20.6729 |

---

## get_inertia
Calculate Dorsey's Inertia: the Relative Volatility Index smoothed with a linear regression, which shows the direction of a trend, up above 50 and down below it.

Inertia is Dorsey's Relative Volatility Index (RVI) smoothed with a linear regression: the end point of the least-squares line through the last 20 RVI values. Dorsey regarded a trend as momentum that persists, inertia, with its direction given by the direction of volatility, so Inertia above 50 marks an up trend and below 50 a down trend. The regression smooths the RVI with less lag than a moving average.

The formula is as follows:

$$
\text{RVI} = \text{Relative Volatility Index}(\text{Close},\; \text{rvi\_window},\; \text{std\_window}),\;\; \text{or}\;\; \text{for the refined RVI} \;\frac{\operatorname{RVI}(\text{High}) + \operatorname{RVI}(\text{Low})}{2}
$$

$$
\text{Inertia} = \text{Linear Regression}(\text{RVI},\; \text{window}),\;\; \text{the end point of the least-squares line}
$$

with the RVI of `get_relative_volatility_index` (Wilder's smoothing of the standard deviation on up and down periods) and the linear regression of `get_linear_regression`.

**Also known as:** INERTIA, Dorsey Inertia.

**References:**

- paper | Dorsey, D. (1995). "Refining the Relative Volatility Index." Technical Analysis of Stocks & Commodities, 13(9).
- paper | Dorsey, D. (1993). "The Relative Volatility Index." Technical Analysis of Stocks & Commodities, 11(6).
- library | Referenced against pandas-ta-classic's [inertia](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/momentum/inertia.py#L61){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int, optional):</u> The number of periods of the linear regression. Defaults to 20.
- <u>rvi_window (int, optional):</u> The number of periods of Wilder's smoothing in the RVI.
Defaults to 14.
- <u>std_window (int, optional):</u> The number of periods of the standard deviation in the RVI.
Defaults to 10.
- <u>method (str, optional):</u> The Relative Volatility Index it uses. Options are: "original" (the RVI of
the close), "refined" (the average of the RVI of the highs and of the lows; Dorsey, 1995).
Defaults to "original".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Inertia.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: Inertia values, around 0 to 100.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the Inertia for each asset in the Toolkit instance.
- Equals the linear regression of `get_relative_volatility_index` with the same parameters,
and pandas-ta-classic's inertia with Wilder's smoothing and `std_window` equal to `rvi_window`. By
default pandas-ta-classic smooths its RVI with an EMA and takes the standard deviation over
the RVI window. The linear regression can overshoot the 0 to 100 range of the RVI.
- When growth is requested, the method calculates the growth of the Inertia
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2024-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_inertia().tail(5)
```

Which returns:

| Date       |    AAPL |    MSFT |   Benchmark |
|:-----------|--------:|--------:|------------:|
| 2025-12-24 | 47.9699 | 57.9156 |     67.4073 |
| 2025-12-26 | 48.2486 | 57.5311 |     66.9018 |
| 2025-12-29 | 49.2247 | 56.9374 |     65.6764 |
| 2025-12-30 | 50.4639 | 56.4007 |     62.9555 |
| 2025-12-31 | 52.0466 | 55.6652 |     59.8904 |

---

## get_bias
Calculate the Bias: the distance of the price from its moving average, as a share of that average.

The Bias, or deviation rate, is a standard indicator on Asian trading platforms. It measures how far the close has run from its moving average as a share of that average: a price far above its average is read as overbought and likely to return to it, and far below as oversold. What counts as far depends on the security and the window, so it is usually compared with the Bias's own history.

The formula is as follows:

$$
\text{Bias} = \frac{\text{Close}}{\operatorname{MA}(\text{Close},\; \text{window})} - 1
$$

with MA the Simple Moving Average by default.

**Also known as:** BIAS, deviation rate, BIAS ratio, distance to the moving average.

**References:**

- library | Referenced against pandas-ta-classic's [bias](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/momentum/bias.py#L12){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int, optional):</u> The number of periods of the moving average. Defaults to 26.
- <u>moving_average (str, optional):</u> The moving average. Options are: "simple" (Simple Moving Average),
"exponential" (Exponential Moving Average), "double_exponential" (Double Exponential Moving
Average), "triangular" (Triangular Moving Average), "weighted" (Weighted Moving Average),
"hull" (Hull Moving Average), "kaufman_adaptive" (Kaufman Adaptive Moving Average). Defaults to
"simple".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Bias.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: Bias values as decimals (0.05 is 5% above the average).

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the Bias for each asset in the Toolkit instance.
- Equals pandas-ta-classic's bias, also a decimal; some platforms multiply it by 100.
- When growth is requested, the method calculates the growth of the Bias
over the given lag.
- The indicator has no single primary source; it is a standard indicator on Asian trading platforms, defined
here as in pandas-ta-classic.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2024-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_bias().tail(5)
```

Which returns:

| Date       |    AAPL |   MSFT |   Benchmark |
|:-----------|--------:|-------:|------------:|
| 2025-12-24 | -0.0071 | 0.0105 |      0.0205 |
| 2025-12-26 | -0.0094 | 0.0102 |      0.0185 |
| 2025-12-29 | -0.0088 | 0.0089 |      0.0133 |
| 2025-12-30 | -0.0122 | 0.009  |      0.01   |
| 2025-12-31 | -0.0166 | 0      |      0.0011 |

---

## get_brar
Calculate the AR and BR sentiment indicators (BRAR), which show how popular a security is and how willing the market is to buy it.

They set how far the prices rose against how far they fell, measured from the open (AR) and from the previous close (BR).

AR (popularity) compares how far the price rose above the open with how far it fell below it over the window, and BR (willingness) does the same against the previous close, which also counts the gaps between periods. Both are 100 when the upward and downward moves balance. AR from 150 and BR from 300 are read as overheated and AR below 50 and BR below 40 as depressed; BR crossing AR from below is a buy signal.

The formula is as follows:

$$
\text{AR} = \frac{100 \cdot \operatorname{Sum}(\text{High} - \text{Open},\; \text{window})}{\operatorname{Sum}(\text{Open} - \text{Low},\; \text{window})}
$$

$$
\text{BR} = \frac{100 \cdot \operatorname{Sum}(\max(\text{High} - \operatorname{Close}(t - 1),\; 0),\; \text{window})}{\operatorname{Sum}(\max(\operatorname{Close}(t - 1) - \text{Low},\; 0),\; \text{window})}
$$

**Also known as:** BRAR, AR and BR, popularity and willingness indicators, sentiment indicator.

**References:**

- library | Referenced against pandas-ta-classic's [brar](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/momentum/brar.py#L18){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int, optional):</u> The number of periods of the sums. Defaults to 26.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the AR and BR.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: AR and BR, 100 for a balance.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the AR and BR for each asset in the Toolkit instance.
- Equals pandas-ta-classic's brar, on its scale of 100 for a balance. A window without any
downward move has no AR or BR (missing) where pandas-ta-classic gives an infinite value.
- When growth is requested, the method calculates the growth of the AR and BR
over the given lag.
- The indicator has no single primary source; it is a standard indicator on Asian trading platforms, defined
here as in pandas-ta-classic.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2024-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_brar().xs("AAPL", level=1, axis="columns").tail(5)
```

Which returns:

| Date       |       AR |       BR |
|:-----------|---------:|---------:|
| 2025-12-24 | 112.898  | 120.363  |
| 2025-12-26 | 120.492  | 119.908  |
| 2025-12-29 | 110.988  | 114.995  |
| 2025-12-30 | 113.905  | 105.452  |
| 2025-12-31 |  99.0846 |  92.3299 |

---

## get_pretty_good_oscillator
Calculate Johnson's Pretty Good Oscillator (PGO): how far the close lies from its moving average, in units of the Average True Range, which shows breakouts from a range.

The Pretty Good Oscillator of Mark Johnson measures the distance of the close from its Simple Moving Average in units of the average true range, so the distance compares across securities and periods of different volatility. Johnson used it for breakouts: a close more than 3 average ranges above its average is a long entry, more than 3 below a short entry, and the trade is closed when the oscillator returns to zero.

The formula is as follows:

$$
\text{PGO} = \frac{\text{Close} - \operatorname{SMA}(\text{Close},\; \text{window})}{\operatorname{EMA}(\operatorname{ATR}(\text{window}),\; \text{window})}
$$

with ATR Wilder's Average True Range and the EMA seeded with a simple average.

**Also known as:** PGO, Pretty Good Oscillator.

**References:**

- paper | Johnson, M. "Pretty Good Oscillator." FM Labs technical analysis library ([https://www.fmlabs.com/reference/default.htm?url=PGO.htm](https://www.fmlabs.com/reference/default.htm?url=PGO.htm){:target="_blank"}).
- library | Referenced against pandas-ta-classic's [pgo](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/momentum/pgo.py#L14){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int, optional):</u> The number of periods of the SMA, the ATR and its EMA. Defaults to 14.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the PGO.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: PGO values, in average true ranges.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the PGO for each asset in the Toolkit instance.
- Equals pandas-ta-classic's pgo once Wilder's smoothing of the ATR has forgotten its - <u>seed (within
1e-7 after 200 periods):</u> the Toolkit's ATR includes the High — Low of the first period, as
StockCharts does. A period without any range has no PGO (missing) where pandas-ta-classic
gives 0.
- When growth is requested, the method calculates the growth of the PGO
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2024-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_pretty_good_oscillator().tail(5)
```

Which returns:

| Date       |    AAPL |   MSFT |   Benchmark |
|:-----------|--------:|-------:|------------:|
| 2025-12-24 | -0.2751 | 0.5238 |      1.1828 |
| 2025-12-26 | -0.284  | 0.466  |      1.1293 |
| 2025-12-29 | -0.1531 | 0.4401 |      0.7459 |
| 2025-12-30 | -0.2379 | 0.5319 |      0.5822 |
| 2025-12-31 | -0.3998 | 0.0483 |     -0.1073 |

---

## get_psychological_line
Calculate the Psychological Line (PSL): the share of periods in a window that closed higher, which shows whether buyers or sellers have the upper hand.

The Psychological Line is the percentage of the last `window` periods that closed higher, a measure of the mood of the market: after many periods up in a row buyers may be exhausted (overbought above 75) and after many down sellers (oversold below 25). The open-based form counts the periods that closed above their own open instead.

The formula is as follows:

$$
\text{PSL} = \frac{100 \cdot \operatorname{Count}(\operatorname{Close}(t) > \operatorname{Close}(t - 1),\; \text{window})}{\text{window}}
$$

or in the open-based form, 100 × Count(Close > Open, window) / window.

**Also known as:** PSL, PSY, psychological line, psychological index.

**References:**

- library | Referenced against pandas-ta-classic's [psl](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/momentum/psl.py#L19){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int, optional):</u> The number of periods counted. Defaults to 12.
- <u>method (str, optional):</u> What counts as an up period. Options are: "close" (a close above the
previous close), "open" (a close above the period's open). Defaults to "close".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the PSL.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: PSL values, between 0 and 100.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the PSL for each asset in the Toolkit instance.
- Equals pandas-ta-classic's psl, also on the scale of 0 to 100.
- When growth is requested, the method calculates the growth of the PSL
over the given lag.
- The indicator has no single primary source; it is a standard indicator on Asian trading platforms, defined
here as in pandas-ta-classic.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2024-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_psychological_line().tail(5)
```

Which returns:

| Date       |    AAPL |    MSFT |   Benchmark |
|:-----------|--------:|--------:|------------:|
| 2025-12-24 | 58.3333 | 58.3333 |     58.3333 |
| 2025-12-26 | 58.3333 | 50      |     58.3333 |
| 2025-12-29 | 58.3333 | 50      |     50      |
| 2025-12-30 | 58.3333 | 50      |     41.6667 |
| 2025-12-31 | 50      | 50      |     41.6667 |

---

## get_volatility_based_momentum
Calculate the Volatility-Based Momentum (VBM): the change of the price over a window in units of the Average True Range, which compares momentum across tickers of different volatility.

Volatility-Based Momentum is the change in the close over `window` periods in units of the Average True Range, instead of as a share of the earlier close as in the Rate of Change. A move of 3 average ranges is then large for any security, whatever its price or volatility, which makes the momentum comparable across securities and over time.

The formula is as follows:

$$
\text{VBM} = \frac{\operatorname{Close}(t) - \operatorname{Close}(t - \text{window})}{\operatorname{ATR}(\text{atr\_window})}
$$

with ATR Wilder's Average True Range.

**Also known as:** VBM, volatility-based momentum, volatility adjusted momentum.

**References:**

- paper | Pring, M.J. (1991). "Technical Analysis Explained." 3rd ed. McGraw-Hill (momentum).
- paper | Wilder, J.W. Jr. (1978). "New Concepts in Technical Trading Systems." Trend Research (Average True Range).
- library | Shares similar logic as finta's [VBM](https://github.com/peerchemist/finta/blob/1.3/finta/finta.py#L664){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int, optional):</u> The number of periods of the price change. Defaults to 12.
- <u>atr_window (int, optional):</u> The number of periods of the Average True Range. Defaults to 26.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the VBM.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: VBM values, in average true ranges.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the VBM for each asset in the Toolkit instance.
- finta documents this formula, but its VBM subtracts the earlier close twice
(Close.diff(n) — Close.shift(n)) and averages the true range with a simple moving average,
so its values differ.
- When growth is requested, the method calculates the growth of the VBM
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2024-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_volatility_based_momentum().tail(5)
```

Which returns:

| Date       |    AAPL |    MSFT |   Benchmark |
|:-----------|--------:|--------:|------------:|
| 2025-12-24 | -0.8397 | -0.3403 |      1.236  |
| 2025-12-26 | -0.7927 | -0.5035 |      1.3433 |
| 2025-12-29 | -1.0766 |  1.0178 |      0.3387 |
| 2025-12-30 | -1.0873 |  0.4873 |     -0.0195 |
| 2025-12-31 | -1.4421 |  0.6285 |      0.3294 |

---

## get_archer_moving_average_trends
Calculate Archer's Moving Averages Trends (AMAT): whether a fast and a slow moving average both rise (a long run) or both fall (a short run), which shows the direction of a trend.

AMAT flags a long run when the short moving average rose over the last `lookback` periods while the long one moved (a rising long average confirms the up trend, a falling one marks a potential bottom), and a short run when the short average fell while the long one moved (a potential top when the long one still rose). Both flags are 0 when the short average is flat or the long one did not move.

The formula is as follows:

$$
\text{Long Run} = 1 \;\text{if MA}(\text{Close},\; \text{short\_window}) \;\text{rose over} \;\text{lookback} \;\text{periods and MA}(\text{Close},\; \text{long\_window}) \;\text{changed},\;\; \text{else 0}
$$

$$
\text{Short Run} = 1 \;\text{if MA}(\text{Close},\; \text{short\_window}) \;\text{fell over} \;\text{lookback} \;\text{periods and MA}(\text{Close},\; \text{long\_window}) \;\text{changed},\;\; \text{else 0}
$$

with MA the exponential moving average by default.

**Also known as:** AMAT, Archer Moving Averages Trends.

**References:**

- paper | Archer's TradingView script "Archer Moving Averages Trends", which defines the indicator; there is no published primary source.
- library | Referenced against pandas-ta-classic's [amat](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/trend/amat.py#L15){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>short_window (int, optional):</u> The number of periods of the short moving average. Defaults to 8.
- <u>long_window (int, optional):</u> The number of periods of the long moving average. Defaults to 21.
- <u>lookback (int, optional):</u> The number of periods over which the averages rise or fall.
Defaults to 2.
- <u>moving_average (str, optional):</u> The moving average. Options are: "simple" (Simple Moving Average),
"exponential" (Exponential Moving Average), "double_exponential" (Double Exponential Moving
Average), "triangular" (Triangular Moving Average), "weighted" (Weighted Moving Average),
"hull" (Hull Moving Average), "kaufman_adaptive" (Kaufman Adaptive Moving Average). Defaults to
"exponential".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the AMAT.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: Long Run and Short Run, 1 when the run holds and 0 otherwise.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the AMAT for each asset in the Toolkit instance.
- Equals pandas-ta-classic's amat (its long_run and short_run columns).
- When growth is requested, the method calculates the growth of the AMAT
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2024-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_archer_moving_average_trends().xs("AAPL", level=1, axis="columns").tail(5)
```

Which returns:

| Date       |   Long Run |   Short Run |
|:-----------|-----------:|------------:|
| 2025-12-24 |          0 |           1 |
| 2025-12-26 |          1 |           0 |
| 2025-12-29 |          1 |           0 |
| 2025-12-30 |          0 |           1 |
| 2025-12-31 |          0 |           1 |

---

## get_ttm_trend
Calculate Carter's TTM Trend: whether the close lies above the average midpoint of the previous bars (1) or not (-1), which shows the direction of the trend.

The TTM Trend of John Carter colours each bar by the short-term trend: up (1) when the close is above the average midpoint, (High + Low) / 2, of the previous six bars, and down (-1) when it is not. Carter uses it to stay in a trade while the bars keep their colour and to avoid trading against it; two bars of the opposite colour in a row signal that the trend has turned.

The formula is as follows:

$$
\text{Average Midpoint} = \operatorname{SMA}\left(\frac{\text{High} + \text{Low}}{2},\; \text{window}\right) \;\text{over the} \;\text{window} \;\text{bars before the current one}
$$

$$
\text{TTM Trend} = 1 \;\text{if Close} > \text{Average Midpoint},\;\; \text{else -1}
$$

**Also known as:** TTM Trend, TTM_TRND.

**References:**

- paper | Carter, J.F. (2005). "Mastering the Trade: Proven Techniques for Profiting from Intraday and Swing Trading Setups." McGraw-Hill.
- library | Referenced against pandas-ta-classic's [ttm_trend](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/trend/ttm_trend.py#L12){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int, optional):</u> The number of earlier bars of the average midpoint. Defaults to 6.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the TTM Trend.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: 1 for an up trend and -1 for a down trend.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the TTM Trend for each asset in the Toolkit instance.
- Equals pandas-ta-classic's ttm_trend. It starts `window` periods after the first price.
- When growth is requested, the method calculates the growth of the TTM Trend
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2024-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_ttm_trend().tail(5)
```

Which returns:

| Date       |   AAPL |   MSFT |   Benchmark |
|:-----------|-------:|-------:|------------:|
| 2025-12-24 |      1 |      1 |           1 |
| 2025-12-26 |      1 |      1 |           1 |
| 2025-12-29 |      1 |      1 |           1 |
| 2025-12-30 |      1 |      1 |           1 |
| 2025-12-31 |     -1 |     -1 |          -1 |

---

## get_correlation_trend_indicator
Calculate the Correlation Trend Indicator (CTI) of a price series: the Pearson correlation of the prices over the window with a straight line rising over time.

Ehlers (2020) measures the trend by how closely the prices follow an upward-sloping line: +1 when they rise in a straight line, -1 when they fall in one, and around 0 when they move sideways or in a cycle. Ehlers reads values above 0 as an uptrend and below 0 as a downtrend, with the indicator crossing zero as the switch between them. Unlike the slope it is bounded and does not depend on the price level, so it compares across securities.

The formula is as follows:

$$
\text{CTI} = \operatorname{Correlation}(\text{Close},\; x,\; \text{window}),\;\; \text{with}\;\; \text{time}\; x = 0,\; \ldots,\; \text{window} - 1 \;\text{from the oldest price of the window to the latest}
$$

**Also known as:** CTI, correlation trend, Ehlers correlation trend indicator.

**References:**

- paper | Ehlers, J.F. (2020). "Correlation As A Trend Indicator." Technical Analysis of Stocks & Commodities, 38(5), 24-27.
- library | Referenced against TA-Lib's [CTI](https://ta-lib.org/functions/cti.html){:target="_blank"}
- library | Referenced against pandas-ta-classic's [cti](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/momentum/cti.py#L12){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int, optional):</u> The number of periods, at least 2. Defaults to 20.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the CTI.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame:
Correlation Trend Indicator values between -1 and 1.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates the
CTI for each asset in the Toolkit instance.
- The CTI agrees with TA-Lib's CTI and pandas-ta-classic's cti (whose default window is 12).
- A window of flat prices has no correlation and is missing, where TA-Lib gives 0.
- When growth is requested, the method calculates the growth of the CTI
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_correlation_trend_indicator().tail(5)
```

Which returns:

| Date       |    AAPL |    MSFT |   Benchmark |
|:-----------|--------:|--------:|------------:|
| 2025-12-24 | -0.8202 | -0.2102 |      0.1879 |
| 2025-12-26 | -0.8697 | -0.1202 |      0.2628 |
| 2025-12-29 | -0.8843 |  0.0683 |      0.3433 |
| 2025-12-30 | -0.8571 |  0.1828 |      0.3518 |
| 2025-12-31 | -0.8485 |  0.3044 |      0.2916 |

---

## get_forecast_oscillator
Calculate the Forecast Oscillator of a price series: how far the price lies from the Time Series Forecast made for it one period earlier, as a share of the price.

Chande's Forecast Oscillator measures the error of the linear regression forecast: it is positive when the price comes in above the forecast of the previous period and negative when below it. A forecast that keeps being too low points to a trend that accelerates, and the oscillator crossing zero to a change in the direction of the error.

The formula is as follows:

$$
\text{Time Series Forecast}(t - 1) = \text{the least-squares line over the} \;\text{window} \;\text{periods up to}\; t - 1,\;\; \text{extended to } t
$$

$$
\text{Forecast Oscillator} = \frac{\text{Close} - \text{Time Series Forecast}(t - 1)}{\text{Close}}
$$

**Also known as:** FOSC, Chande Forecast Oscillator, CFO, forecast error.

**References:**

- paper | Chande, T.S. & Kroll, S. (1994). "The New Technical Trader." Wiley.
- library | Referenced against TA-Lib's [FOSC](https://ta-lib.org/functions/fosc.html){:target="_blank"}
- library | Referenced against Tulip Indicators' [fosc](https://tulipindicators.org/fosc){:target="_blank"}
- library | Shares similar logic as pandas-ta-classic's [fosc](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/momentum/fosc.py#L12){:target="_blank"}
- library | Shares similar logic as pandas-ta-classic's [cfo](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/momentum/cfo.py#L17){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int, optional):</u> The number of periods the forecast line is fitted over, at
least 2. Defaults to 5.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Forecast Oscillator.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame:
Forecast Oscillator values as decimals.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates the
Forecast Oscillator for each asset in the Toolkit instance.
- The oscillator agrees with TA-Lib's FOSC and Tulip Indicators' fosc divided by 100: a decimal (0.01 is 1%)
where they give a percentage.
- pandas-ta-classic's fosc and cfo compare the price with the forecast of the same period, a line fitted
through that price, rather than with the forecast made the period before.
- When growth is requested, the method calculates the growth of the Forecast Oscillator
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_forecast_oscillator().tail(5)
```

Which returns:

| Date       |    AAPL |    MSFT |   Benchmark |
|:-----------|--------:|--------:|------------:|
| 2025-12-24 |  0.0061 | -0.0046 |     -0.0048 |
| 2025-12-26 |  0.0008 | -0.0019 |     -0.0074 |
| 2025-12-29 |  0.0008 | -0.0033 |     -0.0094 |
| 2025-12-30 | -0.0065 | -0.0021 |     -0.0055 |
| 2025-12-31 | -0.0068 | -0.0081 |     -0.008  |

---

## get_projection_oscillator
Calculate the Projection Oscillator of a price series: where the close lies within Widner's Projection Bands, 0 on the lower band and 1 on the upper band.

Widner (1995) projects every high and low of the window forward to the latest period along the least-squares slope of the highs and of the lows over the window. The upper Projection Band is the highest of the projected highs and the lower band the lowest of the projected lows, so the bands follow the trend of the window rather than lying flat like the highest high and lowest low of the Stochastic Oscillator. The Projection Oscillator is the stochastic within those bands: high readings mean the close is near the top of its trend channel, and Widner reads turns from extreme readings as signals.

The formula is as follows:

$$
\text{Slope High, Slope Low} = \text{the least-squares slopes of the highs and of the lows over the window}
$$

$$
\text{Upper Band} = \max(\operatorname{High}(t - i) + i \cdot \text{Slope High}),\;\; i = 0,\; \ldots,\; \text{window} - 1
$$

$$
\text{Lower Band} = \min(\operatorname{Low}(t - i) + i \cdot \text{Slope Low}),\;\; i = 0,\; \ldots,\; \text{window} - 1
$$

$$
\text{Projection Oscillator} = \frac{\text{Close} - \text{Lower Band}}{\text{Upper Band} - \text{Lower Band}}
$$

**Also known as:** PO, Projection Oscillator, Projection Bands, Widner.

**References:**

- paper | Widner, M. (1995). "Signaling Change with Projection Bands." Technical Analysis of Stocks & Commodities, 13(7), 275-281.
- library | Shares similar logic as pandas-ta-classic's [po](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/momentum/po.py#L12){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int, optional):</u> The number of periods, at least 2. Defaults to 14.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Projection Oscillator.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame:
Projection Oscillator values as decimals.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates the
Projection Oscillator for each asset in the Toolkit instance.
- Widner gives the oscillator from 0 to 100; the Toolkit gives a decimal from 0 to 1.
- pandas-ta-classic's po is a simpler measure under the same name, the distance of the close from the
end point of its linear regression in percent, 100 * (Close - Linear Regression) / Linear Regression,
which follows from `get_linear_regression`.
- With the dividend-adjusted close (the default), the high and low are adjusted by the same factor, so
the close stays within the high and low of its period.
- When growth is requested, the method calculates the growth of the Projection Oscillator
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_projection_oscillator().tail(5)
```

Which returns:

| Date       |   AAPL |   MSFT |   Benchmark |
|:-----------|-------:|-------:|------------:|
| 2025-12-24 | 0.8331 | 0.7613 |      0.9788 |
| 2025-12-26 | 0.7973 | 0.7345 |      0.9305 |
| 2025-12-29 | 0.854  | 0.5524 |      0.7633 |
| 2025-12-30 | 0.7814 | 0.5129 |      0.6374 |
| 2025-12-31 | 0.6255 | 0.1683 |      0.2356 |

---

## get_trend_detection_index
Calculate M.H. Pee's Trend Detection Index (TDI) and its Direction Indicator: how strongly the momentum keeps one sign over a window, which shows whether the prices trend and in which direction.

The Trend Detection Index tells a trending market from a consolidating one. It compares the net momentum over the window with how much the momentum moved over a longer window: when the momentum keeps one sign, its sum outweighs the absolute momentum of the earlier periods and the TDI is positive (a trend); when it changes sign, the sum cancels out and the TDI is negative (a consolidation). The Direction Indicator, the sum of the momentum, says which way the trend goes.

The formula is as follows:

$$
\text{Momentum} = \operatorname{Close}(t) - \operatorname{Close}(t - \text{window})
$$

$$
\text{Direction Indicator} = \operatorname{Sum}(\text{Momentum},\; \text{window})
$$

$$
\text{TDI} = \left|\text{Direction Indicator}\right| - (\operatorname{Sum}(\left|\text{Momentum}\right|,\; \text{multiple} \cdot \text{window}) - \operatorname{Sum}(\left|\text{Momentum}\right|,\; \text{window}))
$$

Pee buys when both the TDI and the Direction Indicator are positive, and sells when the TDI is positive and the Direction Indicator negative. A negative TDI says to stay out, or to trade the range. Both are in price units, so they compare over time but not across stocks with different prices.

**Also known as:** TDI, trend detection index, Pee's trend detection index.

**References:**

- paper | Pee, M.H. (2001). "Trend Detection Index." Technical Analysis of Stocks & Commodities, 19(10).
- library | Referenced against TTR (R)'s [TDI](https://github.com/joshuaulrich/TTR/blob/v0.24.4/R/TDI.R#L63){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int, optional):</u> The number of periods of the momentum and of the Direction
Indicator. Defaults to 20, as in TTR's TDI.
- <u>multiple (int, optional):</u> The longer window of the absolute momentum, as a multiple of
`window`. Defaults to 2, Pee's own.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: The TDI and the Direction Indicator, in price units.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates the
Trend Detection Index for each asset in the Toolkit instance.
- Every sum covers momentum values only, so the TDI starts on period
(`multiple` + 1) * `window` — 1 and the Direction Indicator on period 2 * `window` — 1.
TTR's TDI sets the first `window` momentum values, which have no earlier price, to 0, so
both start `window` periods earlier there, with sums that include those zeros; from
then on the two agree.
- When growth is requested, the method calculates the growth of the Trend Detection
Index over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_trend_detection_index().xs("AAPL", level=1, axis="columns").tail(5)
```

Which returns:

| Date       |   Direction Indicator |      TDI |
|:-----------|----------------------:|---------:|
| 2025-12-24 |              128.144  | -160.945 |
| 2025-12-26 |              115.926  | -167.06  |
| 2025-12-29 |              103.167  | -173.298 |
| 2025-12-30 |               80.2354 | -196.881 |
| 2025-12-31 |               48.615  | -233.537 |

---

## get_dv_intermediate_oscillator
Calculate David Varadi's DV Intermediate Oscillator (DVI), from 0 to 1, which shows how stretched the price is.

It blends rankings of how far the price stands from its short average and of the balance of up and down days.

The DVI is a smooth oscillator between 0 and 1 that combines two rankings over the last `window` periods. The magnitude ranks how far the price stands above or below its 3-period average, smoothed over a short and a long window; the stretch ranks the number of up days against down days over a short and a long window. Varadi weights the magnitude 0.8 and the stretch 0.2.

The formula is as follows:

$$
\text{Return} = \frac{\operatorname{Close}(t)}{\operatorname{SMA}(\text{Close},\; 3)} - 1
$$

$$
\text{Magnitude} = \operatorname{SMA}\left(\frac{\operatorname{SMA}(\text{Return},\; 5) + \frac{\operatorname{SMA}(\text{Return},\; 100)}{10}}{2},\; 5\right)
$$

$$
\text{Direction} = + 1 \;\text{if Close}(t) > \operatorname{Close}(t - 1),\;\; \text{else -1}
$$

$$
\text{Stretch} = \operatorname{SMA}\left(\frac{\operatorname{Sum}(\text{Direction},\; 10) + \frac{\operatorname{Sum}(\text{Direction},\; 100)}{10}}{2},\; 2\right)
$$

$$
\text{DVI Magnitude} = \text{Percent Rank}(\text{Magnitude},\; \text{window})
$$

$$
\text{DVI Stretch} = \text{Percent Rank}(\text{Stretch},\; \text{window})
$$

$$
\text{DVI} = \text{magnitude\_weight} \cdot \text{DVI Magnitude} + (1 - \text{magnitude\_weight}) \cdot \text{DVI Stretch}
$$

The Percent Rank is the share of the previous `window` values that are lower than the latest one, as in `get_percent_rank`. A DVI above 0.5 marks a price stretched upwards relative to the past year and one below 0.5 a price stretched downwards. Varadi uses it for short-term mean reversion: buy below 0.5 and sell above it, preferably in the direction of the longer trend.

**Also known as:** DVI, DV Intermediate, DV indicator.

**References:**

- paper | Varadi, D. (2009). "What is the DVI?" CSS Analytics, December 13, 2009 ([https://cssanalytics.wordpress.com/2009/12/13/what-is-the-dvi/](https://cssanalytics.wordpress.com/2009/12/13/what-is-the-dvi/){:target="_blank"}).
- library | Referenced against TTR (R)'s [DVI](https://github.com/joshuaulrich/TTR/blob/v0.24.4/R/DVI.R#L50){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int, optional):</u> The number of previous periods of the Percent Ranks. Defaults to
252, a year of trading days.
- <u>magnitude_weight (float, optional):</u> The weight of the magnitude in the DVI, between 0 and
1; the stretch gets the rest. Defaults to 0.8, Varadi's own.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: The DVI Magnitude, the DVI Stretch and the DVI, as decimals
between 0 and 1.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates the
DVI for each asset in the Toolkit instance. The first DVI needs `window` + 106 periods,
so with the default window a Toolkit needs about a year and a half of daily data before
its start date for a DVI on every date.
- The Percent Rank lies between 0 (a new low of the window) and 1 (a new high). TTR's DVI
ranks within a window of `n` values that includes the latest one and counts it, and
equal values, as lower, so its rank lies between 1/n and 1. Without equal values, TTR's
magnitude rank with n = `window` + 1 equals (`window` * DVI Magnitude + 1) / (`window` + 1);
the stretch takes few distinct values, which TTR counts as lower when equal.
- An unchanged close counts as a down day, as in TTR's DVI.
- When growth is requested, the method calculates the growth of the DVI over the
given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_dv_intermediate_oscillator().xs("AAPL", level=1, axis="columns").tail(5)
```

Which returns:

| Date       |    DVI |   DVI Magnitude |   DVI Stretch |
|:-----------|-------:|----------------:|--------------:|
| 2025-12-24 | 0.3921 |          0.3175 |        0.6905 |
| 2025-12-26 | 0.4524 |          0.3929 |        0.6905 |
| 2025-12-29 | 0.4778 |          0.4246 |        0.6905 |
| 2025-12-30 | 0.5198 |          0.4802 |        0.6786 |
| 2025-12-31 | 0.5111 |          0.5079 |        0.5238 |

---

## collect_overlap_indicators
Collect the overlap indicators of every ticker in one table: the moving averages, bands and levels drawn on the same scale as the prices.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>window (int, optional):</u> The window size for calculating indicators.
Defaults to 14.
- <u>close_column (str, optional):</u> The name of the column containing the close prices.
Defaults to "Adj Close".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: Overlap-based indicators calculated based on the specified parameters.

**Notes:**

- The method calculates several overlap-based indicators for each asset in the Toolkit instance.
- When growth is requested, the method calculates the growth of the indicator values
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.collect_overlap_indicators().xs("AAPL", level=1, axis="columns")
```

Which returns:

| Date       |   Simple Moving Average (SMA) |   Exponential Moving Average (EMA) |   Double Exponential Moving Average (DEMA) |   TRIX |   Triangular Moving Average |   Weighted Moving Average (WMA) |   Hull Moving Average (HMA) |   Triple Exponential Moving Average (TEMA) |   Zero Lag Exponential Moving Average (ZLEMA) |   Wilder's Smoothed Moving Average (RMA) |   Sine Weighted Moving Average (SINWMA) |   Fibonacci Weighted Moving Average (FWMA) |   Pascal's Weighted Moving Average (PWMA) |   Kaufman Adaptive Moving Average (KAMA) |   Tillson T3 Moving Average (T3) |   Arnaud Legoux Moving Average (ALMA) |   Volume Weighted Moving Average (VWMA) |   McGinley Dynamic |   Variable Index Dynamic Average (VIDYA) |   Fractal Adaptive Moving Average (FRAMA) |   Holt-Winters Moving Average (HWMA) |   Holt-Winters Channel Upper Band |   Holt-Winters Channel Lower Band |   Elastic Volume Weighted Moving Average (EVWMA) |   Volume Adjusted Moving Average (VAMA) |   Midpoint |   Midpoint Price |   Average Price |   Median Price |   Typical Price |   Weighted Close Price |   Volume Weighted Average Price (VWAP) |   Parabolic SAR |   Gann HiLo Activator |   Zig Zag |   Pivot Point |   Pivot Point Resistance 1 |   Pivot Point Support 1 |   Fibonacci Retracement 50.0% |   Fibonacci Retracement 61.8% |
|:-----------|------------------------------:|-----------------------------------:|-------------------------------------------:|-------:|----------------------------:|--------------------------------:|----------------------------:|-------------------------------------------:|----------------------------------------------:|-----------------------------------------:|----------------------------------------:|-------------------------------------------:|------------------------------------------:|-----------------------------------------:|---------------------------------:|--------------------------------------:|----------------------------------------:|-------------------:|-----------------------------------------:|------------------------------------------:|-------------------------------------:|----------------------------------:|----------------------------------:|-------------------------------------------------:|----------------------------------------:|-----------:|-----------------:|----------------:|---------------:|----------------:|-----------------------:|---------------------------------------:|----------------:|----------------------:|----------:|--------------:|---------------------------:|------------------------:|------------------------------:|------------------------------:|
| 2025-12-17 |                       277.781 |                            275.314 |                                    275.767 | 0.0016 |                     277.982 |                         276.128 |                     273.116 |                                    273.419 |                                       274.067 |                                  273.378 |                                 278.063 |                                    273.419 |                                   277.589 |                                  274.218 |                          279.323 |                               274.905 |                                 277.896 |            271.978 |                                  270.616 |                                   275.481 |                              276.12  |                           280.057 |                           272.184 |                                          273.073 |                                 277.765 |    278.046 |          279.158 |         272.712 |        272.949 |         272.265 |                271.923 |                                277.974 |         285.493 |               280.207 |   270.697 |       273.015 |                    275.185 |                 271.488 |                       279.158 |                       277.161 |
| 2025-12-18 |                       277.308 |                            274.771 |                                    274.694 | 0.0014 |                     277.238 |                         275.257 |                     271.901 |                                    272.199 |                                       272.815 |                                  273.226 |                                 277.267 |                                    272.587 |                                   277.094 |                                  274.081 |                          279.146 |                               273.813 |                                 277.325 |            271.925 |                                  270.663 |                                   273.495 |                              274.766 |                           278.713 |                           270.819 |                                          272.916 |                                 277.208 |    278.046 |          276.821 |         270.652 |        269.352 |         269.983 |                270.298 |                                277.321 |         284.309 |               279.456 |   266.023 |       272.265 |                    273.833 |                 269.328 |                       276.821 |                       274.272 |
| 2025-12-19 |                       276.636 |                            274.498 |                                    274.194 | 0.0012 |                     276.433 |                         274.645 |                     271.147 |                                    271.835 |                                       272.223 |                                  273.19  |                                 276.385 |                                    272.635 |                                   276.649 |                                  273.957 |                          278.852 |                               273.059 |                                 276.053 |            271.981 |                                  270.755 |                                   272.783 |                              273.865 |                           277.958 |                           269.773 |                                          272.876 |                                 276.066 |    278.046 |          276.821 |         271.634 |        271.305 |         271.776 |                272.012 |                                276.002 |         282.481 |               278.475 |   266.023 |       269.983 |                    273.942 |                 267.286 |                       276.821 |                       274.272 |
| 2025-12-22 |                       275.553 |                            273.902 |                                    273.122 | 0.0009 |                     275.578 |                         273.764 |                     270.399 |                                    270.666 |                                       270.96  |                                  272.964 |                                 275.489 |                                    271.634 |                                   275.978 |                                  273.151 |                          278.443 |                               272.238 |                                 275.011 |            271.838 |                                  270.713 |                                   272.504 |                              272.454 |                           276.493 |                           268.414 |                                          272.723 |                                 275.059 |    276.596 |          276.821 |         271.111 |        271.25  |         270.843 |                270.64  |                                275.063 |         280.835 |               277.345 |   266.023 |       271.776 |                    274.59  |                 269.906 |                       276.821 |                       274.272 |
| 2025-12-23 |                       274.714 |                            273.57  |                                    272.607 | 0.0007 |                     274.764 |                         273.212 |                     269.985 |                                    270.319 |                                       270.788 |                                  272.853 |                                 274.716 |                                    271.545 |                                   275.004 |                                  272.908 |                          277.949 |                               271.772 |                                 274.32  |            271.808 |                                  270.755 |                                   272.185 |                              271.5   |                           275.349 |                           267.651 |                                          272.665 |                                 274.38  |    274.877 |          274.882 |         270.373 |        270.089 |         270.531 |                270.752 |                                274.256 |         279.354 |               276.408 |   266.023 |       270.843 |                    272.115 |                 268.757 |                       274.882 |                       272.792 |
| 2025-12-24 |                       274.223 |                            273.476 |                                    272.559 | 0.0006 |                     274.049 |                         272.965 |                     270.161 |                                    270.616 |                                       270.958 |                                  272.854 |                                 274.088 |                                    272.044 |                                   273.884 |                                  272.904 |                          277.412 |                               271.704 |                                 273.909 |            271.882 |                                  270.834 |                                   272.353 |                              270.973 |                           274.704 |                           267.242 |                                          272.67  |                                 273.974 |    273.921 |          273.094 |         272.496 |        272.864 |         272.863 |                272.862 |                                273.798 |         278.021 |               275.97  |   266.023 |       270.531 |                    272.438 |                 269.508 |                       273.094 |                       271.425 |
| 2025-12-26 |                       273.84  |                            273.339 |                                    272.426 | 0.0004 |                     273.429 |                         272.729 |                     270.664 |                                    270.745 |                                       271.364 |                                  272.825 |                                 273.546 |                                    272.197 |                                   272.872 |                                  272.88  |                          276.858 |                               271.784 |                                 273.559 |            271.922 |                                  270.903 |                                   272.475 |                              270.423 |                           273.963 |                           266.884 |                                          272.663 |                                 273.628 |    273.921 |          272.6   |         272.996 |        273.163 |         272.926 |                272.807 |                                273.418 |         276.821 |               275.64  |   266.023 |       272.863 |                    274.47  |                 271.252 |                       272.6   |                       271.048 |
| 2025-12-29 |                       273.546 |                            273.268 |                                    272.416 | 0.0003 |                     272.918 |                         272.591 |                     271.326 |                                    271.012 |                                       271.765 |                                  272.824 |                                 273.082 |                                    272.429 |                                   272.145 |                                  272.877 |                          276.31  |                               272.011 |                                 273.315 |            271.984 |                                  270.911 |                                   272.462 |                              270.03  |                           273.441 |                           266.62  |                                          272.668 |                                 273.386 |    273.921 |          272.6   |         272.341 |        272.406 |         272.541 |                272.608 |                                273.16  |         275.741 |               275.206 |   266.023 |       272.926 |                    273.939 |                 271.438 |                       272.6   |                       271.048 |
| 2025-12-30 |                       273.255 |                            273.117 |                                    272.247 | 0.0002 |                     272.531 |                         272.403 |                     271.798 |                                    271.015 |                                       271.736 |                                  272.774 |                                 272.681 |                                    272.315 |                                   271.738 |                                  272.849 |                          275.78  |                               272.173 |                                 273.113 |            271.995 |                                  270.932 |                                   272.442 |                              269.554 |                           272.853 |                           266.256 |                                          272.648 |                                 273.181 |    273.921 |          272.6   |         272.115 |        272.232 |         272.198 |                272.182 |                                272.911 |         274.769 |               274.771 |   266.023 |       272.541 |                    273.677 |                 271.674 |                       272.6   |                       271.048 |
| 2025-12-31 |                       272.762 |                            272.823 |                                    271.815 | 0.0001 |                     272.2   |                         272.091 |                     271.883 |                                    270.627 |                                       271.745 |                                  272.642 |                                 272.319 |                                    271.777 |                                   271.608 |                                  272.686 |                          275.262 |                               272.102 |                                 272.746 |            271.917 |                                  270.932 |                                   272.383 |                              268.893 |                           272.144 |                           265.643 |                                          272.568 |                                 272.8   |    273.672 |          272.6   |         271.641 |        271.768 |         271.484 |                271.342 |                                272.594 |         273.895 |               274.318 |   266.023 |       272.198 |                    273.062 |                 271.268 |                       272.6   |                       271.048 |

---

## get_moving_average
Calculate the Simple Moving Average (SMA): the average price over a window, which smooths the prices to show their trend.

A Moving Average smooths out price data by averaging the price over a specified number of periods. The variants differ in how they weight the prices within the window: equally (simple), with exponentially decaying weights (exponential, double and triple exponential, zero lag exponential and Wilder), with weights that peak in the middle of the window (triangular, sine and Pascal's weighted), with linearly increasing weights (weighted), with weights that grow with the Fibonacci numbers (Fibonacci weighted), with a Gaussian curve (Arnaud Legoux), with a combination of weighted averages that reduces the lag (Hull) or with the volume traded (volume weighted, elastic volume weighted and volume adjusted). The adaptive averages change their speed with the market: with the efficiency of the price move (Kaufman), the strength of the trend (variable index dynamic), the fractal dimension of the prices (fractal adaptive), the distance of the price from the average (McGinley Dynamic) or the velocity and acceleration of the price (Holt-Winters). Tillson's T3 applies a generalized DEMA three times for a smooth average with little lag, Ehlers' SuperSmoother is a low-pass filter that removes the cycles shorter than the window, and his instantaneous trendline averages the price over its dominant cycle, measured with the Hilbert transform.

The formula is as follows, per method:

$$
\text{Simple Moving Average:}\;\; \text{SMA} = \frac{\text{Sum of Prices}}{\text{Number of Prices}}
$$

$$
\text{Exponential Moving Average:}\;\; \text{the first EMA is SMA(Close, Window), on the Window-th period},\;\; \text{and}\;\; \text{EMA} = (\text{Close} - \text{Previous EMA}) \cdot \frac{2}{1 + \text{Window}} + \text{Previous EMA}
$$

$$
\text{Double Exponential Moving Average:}\;\; \text{DEMA} = 2 \cdot \operatorname{EMA}(\text{Close},\; \text{Window}) - \operatorname{EMA}(\operatorname{EMA}(\text{Close},\; \text{Window}),\; \text{Window})
$$

$$
\text{Triple Exponential Moving Average:}\;\; \text{TEMA} = 3 \cdot \text{EMA1} - 3 \cdot \text{EMA2} + \text{EMA3},\;\; \text{with}\;\; \text{EMA1} = \operatorname{EMA}(\text{Close},\; \text{Window}),\;\; \text{EMA2} = \operatorname{EMA}(\text{EMA1},\; \text{Window})\;\;\text{and}\;\; \text{EMA3} = \operatorname{EMA}(\text{EMA2},\; \text{Window})
$$

$$
\text{Zero Lag Exponential Moving Average:}\;\; \text{ZLEMA} = \operatorname{EMA}(2 \cdot \text{Close} - \operatorname{Close}(t - \text{Lag}),\; \text{Window}),\;\; \text{with}\;\; \text{Lag} = \frac{\text{Window} - 1}{2 \;\text{rounded down}}
$$

$$
\text{Wilder's Smoothed Moving Average:}\;\; \text{the first value is SMA(Close, Window), on the Window-th period},\;\; \text{and}\;\; \text{RMA} = \text{Previous RMA} + \frac{\text{Close} - \text{Previous RMA}}{\text{Window}}
$$

$$
\text{Triangular Moving Average:}\;\; \text{TMA} = \operatorname{SMA}(\operatorname{SMA}(\text{Close},\; \text{Sub-window Length}\; 1),\; \text{Sub-window Length}\; 2),\;\; \text{with both sub-windows} \;\frac{\text{Window} + 1}{2} \;\text{for an odd window and} \;\frac{\text{Window}}{2} \;\text{and} \;\frac{\text{Window}}{2} + 1 \;\text{for an even window} \;(\text{TA-Lib's TRIMA convention})
$$

$$
\text{Weighted Moving Average:}\;\; \text{WMA} = \frac{\text{Sum of} \;(\text{Price} \cdot \text{Weight})}{\text{Sum of Weights}},\;\; \text{with weights 1 to Window from the oldest to the latest price}
$$

$$
\text{Hull Moving Average:}\;\; \text{HMA} = \operatorname{WMA}\left(2 \cdot \operatorname{WMA}\left(\text{Close},\; \frac{\text{Window}}{2}\right) - \operatorname{WMA}(\text{Close},\; \text{Window}),\; \sqrt{\text{Window}}\right)
$$

$$
\text{Sine Weighted Moving Average:}\;\; \text{SINWMA} = \frac{\text{Sum of} \;(\text{Price} \cdot \text{Weight})}{\text{Sum of Weights}},\;\; \text{with}\;\; \text{weights} \;\sin\left(\frac{i \cdot \pi}{\text{Window} + 1}\right) \;\text{for}\; i = 1 \;\text{to Window}
$$

$$
\text{Fibonacci Weighted Moving Average:}\;\; \text{FWMA} = \frac{\text{Sum of} \;(\text{Price} \cdot \text{Weight})}{\text{Sum of Weights}},\;\; \text{with the Fibonacci numbers 1, 1, 2, 3, 5, ... from the oldest to the latest price}
$$

$$
\text{Pascal's Weighted Moving Average:}\;\; \text{PWMA} = \frac{\text{Sum of} \;(\text{Price} \cdot \text{Weight})}{\text{Sum of Weights}},\;\; \text{with the binomial coefficients of row Window} \;\mathord{-} 1 \;\text{of Pascal's triangle}
$$

$$
\text{Kaufman Adaptive Moving Average:}\;\; \text{Change} = \left|\operatorname{Close}(t) - \operatorname{Close}(t - \text{Window})\right|,\;\; \text{Volatility} = \operatorname{Sum}(\left|\operatorname{Close}(i) - \operatorname{Close}(i - 1)\right|,\; \text{Window}),\;\; \text{Efficiency Ratio} \;(\text{ER}) = \frac{\text{Change}}{\text{Volatility, Fastest SC}} = \frac{2}{\text{Fast Window} + 1},\;\; \text{Slowest SC} = \frac{2}{\text{Slow Window} + 1},\;\; \text{Smoothing Constant} \;(\text{SC}) = \left[\text{ER} \cdot (\text{Fastest SC} - \text{Slowest SC}) + \text{Slowest SC}\right]^{2}\;\;\text{and}\;\; \operatorname{KAMA}(t) = \operatorname{KAMA}(t-1) + \text{SC} \cdot (\operatorname{Close}(t) - \operatorname{KAMA}(t-1))
$$

$$
\text{T3 Moving Average:}\;\; E_{1} = \operatorname{EMA}(\text{Close},\; \text{Window}),\;\; E_{2} = \operatorname{EMA}(E_{1},\; \text{Window}),\; \ldots,\; E_{6} = \operatorname{EMA}(E_{5},\; \text{Window}),\;\; c_{1} = - a^{3},\;\; c_{2} = 3a^{2} + 3a^{3},\;\; c_{3} = - 6a^{2} - 3a - 3a^{3},\;\; c_{4} = 1 + 3a + a^{3} + 3a^{2} \;\text{with a the Volume Factor},\;\; \text{and}\;\; T_{3} = c_{1} \cdot E_{6} + c_{2} \cdot E_{5} + c_{3} \cdot E_{4} + c_{4} \cdot E_{3}
$$

$$
\text{Arnaud Legoux Moving Average:}\;\; m = \left\lfloor \text{Offset} \cdot (\text{Window} - 1) \right\rfloor,\;\; s = \frac{\text{Window}}{\text{Sigma, Weight}(i)} = \exp\left(- \frac{(i - m)^{2}}{2 \cdot s^{2}}\right) \;\text{for}\; i = 0 \;(\text{the oldest price}) \;\text{to Window} - 1,\;\; \text{and}\;\; \text{ALMA} = \frac{\operatorname{Sum}(\operatorname{Weight}(i) \cdot \operatorname{Price}(i))}{\operatorname{Sum}(\operatorname{Weight}(i))}
$$

$$
\text{Volume Weighted Moving Average:}\;\; \text{VWMA} = \frac{\operatorname{Sum}(\text{Close} \cdot \text{Volume},\; \text{Window})}{\operatorname{Sum}(\text{Volume},\; \text{Window})}
$$

$$
\text{McGinley Dynamic:}\;\; \text{the first MD is SMA(Close, Window), on the Window-th period},\;\; \text{and}\;\; \operatorname{MD}(t) = \operatorname{MD}(t-1) + \frac{\operatorname{Close}(t) - \operatorname{MD}(t-1)}{\text{Constant} \cdot \text{Window} \cdot \left(\frac{\operatorname{Close}(t)}{\operatorname{MD}(t-1)}\right)^{4}}
$$

$$
\text{Variable Index Dynamic Average:}\;\; \text{Gains} = \operatorname{Sum}(\max(\operatorname{Close}(t) - \operatorname{Close}(t-1),\; 0),\; \text{CMO Window}),\;\; \text{Losses} = \operatorname{Sum}(\max(\operatorname{Close}(t-1) - \operatorname{Close}(t),\; 0),\; \text{CMO Window}),\;\; \left|\text{CMO}\right| = \frac{\left|\text{Gains} - \text{Losses}\right|}{\text{Gains} + \text{Losses}} \;\text{and 0 when prices did not move},\;\; \text{Alpha} = \frac{2}{\text{Window} + 1},\;\; \text{and}\;\; \operatorname{VIDYA}(t) = \text{Alpha} \cdot \left|\operatorname{CMO}(t)\right| \cdot \operatorname{Close}(t) + (1 - \text{Alpha} \cdot \left|\operatorname{CMO}(t)\right|) \cdot \operatorname{VIDYA}(t-1)
$$

$$
\text{Fractal Adaptive Moving Average:}\;\; \text{Price} = \frac{\text{High} + \text{Low}}{2},\;\; N_{1} = \frac{\text{Highest High} - \text{Lowest Low}}{\frac{\text{Window}}{2}} \;\text{over the latest} \;\frac{\text{Window}}{2 \;\text{periods}},\;\; N_{2} \;\text{the same over the} \;\frac{\text{Window}}{2 \;\text{periods before}},\;\; N_{3} = \frac{\text{Highest High} - \text{Lowest Low}}{\text{Window}} \;\text{over the whole window},\;\; D = \frac{\log(N_{1} + N_{2}) - \log(N_{3})}{\log(2)},\;\; \text{Alpha} = \exp(- 4.6 \cdot (D - 1)) \;\text{limited to between}\; 0.01 \;\text{and}\; 1,\;\; \text{and}\;\; \operatorname{FRAMA}(t) = \operatorname{Alpha}(t) \cdot \operatorname{Price}(t) + (1 - \operatorname{Alpha}(t)) \cdot \operatorname{FRAMA}(t-1)
$$

$$
\text{Holt-Winters Moving Average:}\;\; F(t) = (1 - \text{Level Smoothing}) \cdot (F(t-1) + V(t-1) + 0.5 \cdot A(t-1)) + \text{Level Smoothing} \cdot \operatorname{Close}(t),\;\; V(t) = (1 - \text{Velocity Smoothing}) \cdot (V(t-1) + A(t-1)) + \text{Velocity Smoothing} \cdot (F(t) - F(t-1)),\;\; A(t) = (1 - \text{Acceleration Smoothing}) \cdot A(t-1) + \text{Acceleration Smoothing} \cdot (V(t) - V(t-1))\;\;\text{and}\;\; \operatorname{HWMA}(t) = F(t) + V(t) + 0.5 \cdot A(t),\;\; \text{with } F \text{ starting at the first close and } V \text{ and A at 0}
$$

$$
\text{Elastic Volume Weighted Moving Average:}\;\; \text{Volume Sum} = \operatorname{Sum}(\text{Volume},\; \text{Window})\;\;\text{and}\;\; \operatorname{eVWMA}(t) = \frac{(\text{Volume Sum} - \operatorname{Volume}(t)) \cdot \operatorname{eVWMA}(t-1) + \operatorname{Volume}(t) \cdot \operatorname{Close}(t)}{\text{Volume Sum}}
$$

$$
\text{Volume Adjusted Moving Average:}\;\; \operatorname{Weight}(t) = \frac{\operatorname{Close}(t) \cdot \operatorname{Volume}(t)}{\operatorname{SMA}(\text{Volume},\; \text{Window}) (t)}\;\;\text{and}\;\; \text{VAMA} = \frac{\operatorname{Sum}(\text{Weight} \cdot \text{Close},\; \text{Window})}{\operatorname{Sum}(\text{Weight},\; \text{Window})}
$$

$$
\text{"super\_smoother" with two poles:}\;\; a = \exp\left(- \frac{\sqrt{2} \cdot \pi}{\text{Window}}\right),\;\; b = 2 \cdot a \cdot \cos\left(\frac{\sqrt{2} \cdot 180}{\text{Window}}\right),\;\; c_{2} = b,\;\; c_{3} = - a^{2},\;\; c_{1} = 1 - c_{2} - c_{3}\;\;\text{and}\;\; \text{Filter} = \frac{c_{1} \cdot (\text{Price} + \operatorname{Price}(t-1))}{2} + c_{2} \cdot \operatorname{Filter}(t-1) + c_{3} \cdot \operatorname{Filter}(t-2);\;\; \text{with}\;\; \text{three poles:}\;\; a = \exp\left(- \frac{\pi}{\text{Window}}\right),\;\; b = 2 \cdot a \cdot \cos\left(\frac{\sqrt{3} \cdot 180}{\text{Window}}\right),\;\; c = a^{2},\;\; c_{2} = b + c,\;\; c_{3} = - (c + b \cdot c),\;\; c_{4} = c^{2},\;\; c_{1} = 1 - c_{2} - c_{3} - c_{4}\;\;\text{and}\;\; \text{Filter} = c_{1} \cdot \text{Price} + c_{2} \cdot \operatorname{Filter}(t-1) + c_{3} \cdot \operatorname{Filter}(t-2) + c_{4} \cdot \operatorname{Filter}(t-3)
$$

$$
\text{Hilbert Transform Instantaneous Trendline:}\;\; \text{Smooth} = \frac{4 \cdot \text{Price} + 3 \cdot \operatorname{Price}(t-1) + 2 \cdot \operatorname{Price}(t-2) + \operatorname{Price}(t-3)}{10},\;\; H(x) = (0.0962 \cdot x + 0.5769 \cdot x(t-2) - 0.5769 \cdot x(t-4) - 0.0962 \cdot x(t-6)) \cdot (0.075 \cdot \operatorname{Period}(t-1) + 0.54),\;\; \text{Detrender} = H(\text{Smooth}),\;\; Q_{1} = H(\text{Detrender}),\;\; I_{1} = \operatorname{Detrender}(t-3),\;\; I_{2} = 0.2 \cdot (I_{1} - H(Q_{1})) + 0.8 \cdot \operatorname{I2}(t-1),\;\; Q_{2} = 0.2 \cdot (Q_{1} + H(I_{1})) + 0.8 \cdot \operatorname{Q2}(t-1),\;\; \text{Re} = 0.2 \cdot (I_{2} \cdot \operatorname{I2}(t-1) + Q_{2} \cdot \operatorname{Q2}(t-1)) + 0.8 \cdot \operatorname{Re}(t-1),\;\; \text{Im} = 0.2 \cdot (I_{2} \cdot \operatorname{Q2}(t-1) - Q_{2} \cdot \operatorname{I2}(t-1)) + 0.8 \cdot \operatorname{Im}(t-1),\;\; \text{Period} = \frac{360}{\operatorname{arctan}\left(\frac{\text{Im}}{\text{Re}}\right) \;\text{in degrees}},\;\; \text{limited to between 0.67 and 1.5 times Period(t-1) and to between 6 and 50 periods},\;\; \text{then smoothed as}\; 0.2 \cdot \text{Period} + 0.8 \cdot \operatorname{Period}(t-1),\;\; \text{Dominant Cycle Period} = 0.33 \cdot \text{Period} + 0.67 \cdot \text{Dominant Cycle Period}(t-1),\;\; N = \text{the Dominant Cycle Period rounded to the nearest whole period},\;\; \text{Average} = \text{the simple average of the latest}\; N \;\text{prices},\;\; \text{and}\;\; \text{Trendline} = \frac{4 \cdot \text{Average} + 3 \cdot \operatorname{Average}(t-1) + 2 \cdot \operatorname{Average}(t-2) + \operatorname{Average}(t-3)}{10}
$$

Seeding the EMA with a simple average, as TA-Lib and StockCharts do, leaves the first Window - 1 periods of the price history empty. The DEMA, TRIX, MACD, Percentage Price Oscillator, Force Index, Elder Ray Index, Keltner Channels and Chaikin and McClellan Oscillators use the same EMA and start once their own EMAs are seeded; TEMA starts at period 3 * (Window - 1) and ZLEMA at period Lag + Window - 1. Wilder's average is the smoothing of the RSI, ATR and ADX, an EMA with a smoothing factor of 1 / Window instead of 2 / (Window + 1). The triangular moving average is also the symmetric weighted moving average, with weights 1, 2, ..., 2, 1. The MESA Adaptive Moving Average, which returns MAMA and FAMA, is `get_mesa_adaptive_moving_average`.

**Also known as:** MA, SMA, simple moving average, EMA, exponential moving average, DEMA, double exponential moving average, TEMA, triple exponential moving average, ZLEMA, ZLMA, zero lag moving average, RMA, SMMA, Wilder's smoothing, smoothed moving average, TRIMA, TMA, triangular moving average, SWMA, symmetric weighted moving average, WMA, weighted moving average, linear weighted moving average, HMA, Hull moving average, SINWMA, sine weighted moving average, FWMA, Fibonacci weighted moving average, PWMA, Pascal's weighted moving average, KAMA, Kaufman Adaptive Moving Average, Kaufman's Adaptive Moving Average, T3, Tillson T3, T3 moving average, ALMA, Arnaud Legoux moving average, VWMA, volume weighted moving average, MCGD, McGinley Dynamic, McGinley Dynamic Indicator, VIDYA, variable index dynamic average, Chande's dynamic average, FRAMA, fractal adaptive moving average, HWMA, Holt-Winters moving average, Holt-Winter moving average, eVWMA, EVWMA, elastic volume weighted moving average, VAMA, volume adjusted moving average, SSF, SuperSmoother, super smoother filter, Ehlers' SuperSmoother, HT_TRENDLINE, Hilbert transform instantaneous trendline, instantaneous trendline.

**References:**

- paper | Mulloy, P.G. (1994). "Smoothing Data with Faster Moving Averages." Technical Analysis of Stocks & Commodities, 12(1).
- paper | Mulloy, P.G. (1994). "Smoothing Data with Less Lag." Technical Analysis of Stocks & Commodities, 12(2).
- paper | Ehlers, J.F. & Way, R. (2010). "Zero Lag (Well, Almost)." Technical Analysis of Stocks & Commodities, November 2010.
- paper | Wilder, J.W. Jr. (1978). "New Concepts in Technical Trading Systems." Trend Research.
- paper | Hull, A. (2005). "Hull Moving Average."
- paper | Everget (2018). "Sine Weighted Moving Average." TradingView script.
- paper | Kaufman, P.J. (1998). "Trading Systems and Methods." 3rd ed. Wiley.
- paper | Tillson, T. (1998). "Smoothing Techniques for More Accurate Signals." Technical Analysis of Stocks & Commodities, 16(1).
- paper | Legoux, A. & Kouzis-Loukas, D. (2009). "ALMA: Arnaud Legoux Moving Average." arnaudlegoux.com.
- paper | Dormeier, B.P. (2011). "Investing with Volume Analysis." FT Press.
- paper | McGinley, J.R. (1997). "The McGinley Dynamic." Journal of Technical Analysis (Market Technicians Association).
- paper | Chande, T.S. (1992). "Adapting Moving Averages to Market Volatility." Technical Analysis of Stocks & Commodities, 10(3).
- paper | Chande, T.S. & Kroll, S. (1994). "The New Technical Trader." Wiley.
- paper | Ehlers, J.F. (2005). "Fractal Adaptive Moving Averages." Technical Analysis of Stocks & Commodities, 23(10), 81-82.
- paper | Holt, C.C. (1957). "Forecasting Seasonals and Trends by Exponentially Weighted Moving Averages." ONR Memorandum 52, Carnegie Institute of Technology (reprinted in the International Journal of Forecasting, 20(1), 2004).
- paper | Winters, P.R. (1960). "Forecasting Sales by Exponentially Weighted Moving Averages." Management Science, 6(3), 324-342.
- paper | MQL5 Code Base: HWMA ([https://www.mql5.com/en/code/20856](https://www.mql5.com/en/code/20856){:target="_blank"}).
- paper | Fries, C.P. (2001). "Elastic Moving Averages." Technical Analysis of Stocks & Commodities, 19(6), 52-56 ([https://www.christian-fries.de/evwma/](https://www.christian-fries.de/evwma/){:target="_blank"}).
- paper | Arms, R.W. Jr. (1983). "Volume Cycles in the Stock Market: Market Timing Through Equivolume Charting." Dow Jones-Irwin, on adjusting prices for the volume traded.
- paper | Ehlers, J.F. (2001). "Rocket Science for Traders: Digital Signal Processing Applications." John Wiley & Sons.
- paper | Ehlers, J.F. (2004). "Cybernetic Analysis for Stocks and Futures." John Wiley & Sons.
- paper | Ehlers, J.F. (2013). "Cycle Analytics for Traders: Advanced Technical Trading Concepts." John Wiley & Sons.
- paper | Ehlers, J.F. (2014). "Predictive And Successful Indicators." Technical Analysis of Stocks & Commodities, 32(1), 16-25.
- library | Referenced against TA-Lib's [SMA](https://ta-lib.org/functions/sma.html){:target="_blank"}
- library | Referenced against TA-Lib's [EMA](https://ta-lib.org/functions/ema.html){:target="_blank"}
- library | Referenced against TA-Lib's [DEMA](https://ta-lib.org/functions/dema.html){:target="_blank"}
- library | Referenced against TA-Lib's [TEMA](https://ta-lib.org/functions/tema.html){:target="_blank"}
- library | Referenced against TA-Lib's [ZLEMA](https://ta-lib.org/functions/zlema.html){:target="_blank"}
- library | Referenced against TA-Lib's [TRIMA](https://ta-lib.org/functions/trima.html){:target="_blank"}
- library | Referenced against pandas-ta-classic's [swma](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/overlap/swma.py#L18){:target="_blank"}
- library | Referenced against TA-Lib's [WMA](https://ta-lib.org/functions/wma.html){:target="_blank"}
- library | Referenced against TA-Lib's [HMA](https://ta-lib.org/functions/hma.html){:target="_blank"}
- library | Referenced against TA-Lib's [KAMA](https://ta-lib.org/functions/kama.html){:target="_blank"}
- library | Referenced against TA-Lib's [T3](https://ta-lib.org/functions/t3.html){:target="_blank"}
- library | Referenced against pandas-ta-classic's [t3](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/overlap/t3.py#L14){:target="_blank"}
- library | Referenced against TA-Lib's [ALMA](https://ta-lib.org/functions/alma.html){:target="_blank"}
- library | Referenced against pandas-ta-classic's [alma](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/overlap/alma.py#L12){:target="_blank"}
- library | Referenced against TA-Lib's [VWMA](https://ta-lib.org/functions/vwma.html){:target="_blank"}
- library | Referenced against pandas-ta-classic's [vwma](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/overlap/vwma.py#L13){:target="_blank"}
- library | Referenced against TA-Lib's [MCGD](https://ta-lib.org/functions/mcgd.html){:target="_blank"}
- library | Referenced against pandas-ta-classic's [mcgd](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/overlap/mcgd.py#L28){:target="_blank"}
- library | Referenced against TA-Lib's [VIDYA](https://ta-lib.org/functions/vidya.html){:target="_blank"}
- library | Referenced against pandas-ta-classic's [vidya](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/overlap/vidya.py#L27){:target="_blank"}
- library | Referenced against TA-Lib's [FRAMA](https://ta-lib.org/functions/frama.html){:target="_blank"}
- library | Referenced against finta's [FRAMA](https://github.com/peerchemist/finta/blob/1.3/finta/finta.py#L463){:target="_blank"}
- library | Referenced against pandas-ta-classic's [sinwma](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/overlap/sinwma.py#L12){:target="_blank"}
- library | Referenced against pandas-ta-classic's [fwma](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/overlap/fwma.py#L17){:target="_blank"}
- library | Referenced against pandas-ta-classic's [pwma](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/overlap/pwma.py#L17){:target="_blank"}
- library | Referenced against pandas-ta-classic's [hwma](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/overlap/hwma.py#L31){:target="_blank"}
- library | Referenced against finta's [EVWMA](https://github.com/peerchemist/finta/blob/1.3/finta/finta.py#L381){:target="_blank"}
- library | Referenced against finta's [VAMA](https://github.com/peerchemist/finta/blob/1.3/finta/finta.py#L226){:target="_blank"}
- library | Referenced against pandas-ta-classic's [ssf](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/overlap/ssf.py#L28){:target="_blank"} (SuperSmoother)
- library | Referenced against TA-Lib's [HT_TRENDLINE](https://ta-lib.org/functions/ht_trendline.html){:target="_blank"} (Hilbert Transform Instantaneous Trendline)
- library | Referenced against pandas-ta-classic's [ht_trendline](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/overlap/ht_trendline.py#L14){:target="_blank"} (Hilbert Transform Instantaneous Trendline)
- library | Shares similar logic as TA-Lib's [RMA](https://ta-lib.org/functions/rma.html){:target="_blank"}
- library | Shares similar logic as Tulip Indicators' [vwma](https://tulipindicators.org/vwma){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int &#124; None, optional):</u> Number of periods to consider for the moving average:
the number of periods of the Efficiency Ratio ("kaufman_adaptive"), of each of the six
EMAs ("t3"), of the volume sum ("elastic_volume_weighted"), over which the fractal
dimension is measured, an even number ("fractal_adaptive"), and the critical period
below which cycles are removed ("super_smoother"). Not used by "holt_winters" and
"hilbert_trendline". Defaults to None, which uses the window of each method: 10 for
"kaufman_adaptive" and "super_smoother", 5 for "t3", 9 for "arnaud_legoux", 12 for
"variable_index_dynamic", 16 for "fractal_adaptive", 20 for "elastic_volume_weighted",
8 for "volume_adjusted" and 14 for the others.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the MA.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>method (str, optional):</u> The moving average. Options are: "simple" (Simple Moving Average),
"exponential" (Exponential Moving Average), "double_exponential" (Double Exponential Moving
Average), "triple_exponential" (Triple Exponential Moving Average), "zero_lag" (Zero Lag
Exponential Moving Average), "wilder" (Wilder's Moving Average), "triangular" (Triangular Moving
Average), "weighted" (Weighted Moving Average), "hull" (Hull Moving Average), "sine" (Sine
Weighted Moving Average), "fibonacci" (Fibonacci Weighted Moving Average), "pascal" (Pascal
Weighted Moving Average), "kaufman_adaptive" (Kaufman Adaptive Moving Average), "t3" (Tillson T3
Moving Average), "arnaud_legoux" (Arnaud Legoux Moving Average), "volume_weighted" (Volume
Weighted Moving Average), "mcginley" (McGinley Dynamic), "variable_index_dynamic" (Variable
Index Dynamic Average), "fractal_adaptive" (Fractal Adaptive Moving Average),
"holt_winters" (Holt-Winters Moving Average), "elastic_volume_weighted" (Elastic Volume Weighted
Moving Average), "volume_adjusted" (Volume Adjusted Moving Average), "super_smoother" (Ehlers'
SuperSmoother filter), "hilbert_trendline" (Hilbert Transform Instantaneous Trendline). Defaults
to "simple".
- <u>short_window (int, optional):</u> The number of periods that corresponds to the fastest EMA
constant, used when the Efficiency Ratio is at its maximum (1.0). Only used when
method="kaufman_adaptive". Defaults to 2.
- <u>long_window (int, optional):</u> The number of periods that corresponds to the slowest EMA
constant, used when the Efficiency Ratio is at its minimum (0.0). Only used when
method="kaufman_adaptive". Defaults to 30.
- <u>volume_factor (float, optional):</u> The volume factor a of the T3, between 0 and 1. Only
used when method="t3". Defaults to 0.7, Tillson's value.
- <u>sigma (float, optional):</u> The width of the Gaussian curve of the ALMA, as the number of
standard deviations that fit in the window. Only used when method="arnaud_legoux".
Defaults to 6.0.
- <u>offset (float, optional):</u> The position of the peak of the ALMA's curve in the window,
from 0 (the oldest price) to 1 (the latest price). Only used when
method="arnaud_legoux". Defaults to 0.85.
- <u>constant (float, optional):</u> The constant k of the McGinley Dynamic that multiplies the
window. Only used when method="mcginley". Defaults to 1.0, as in TA-Lib and
pandas-ta-classic; McGinley suggested 0.6 to follow the price more closely.
- <u>cmo_window (int, optional):</u> The number of periods of the Chande Momentum Oscillator of
the VIDYA. Only used when method="variable_index_dynamic". Defaults to 9, TA-Lib's
default.
- <u>level_smoothing (float, optional):</u> The smoothing factor of the level of the HWMA,
between 0 and 1. Only used when method="holt_winters". Defaults to 0.2.
- <u>velocity_smoothing (float, optional):</u> The smoothing factor of the velocity of the HWMA,
between 0 and 1. Only used when method="holt_winters". Defaults to 0.1.
- <u>acceleration_smoothing (float, optional):</u> The smoothing factor of the acceleration of
the HWMA, between 0 and 1. Only used when method="holt_winters". Defaults to 0.1.
- <u>poles (int, optional):</u> The number of poles of the SuperSmoother filter. Options are: 2 (the two-pole
SuperSmoother), 3 (the three-pole SuperSmoother). Only used when method="super_smoother".
Defaults to 2.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame or pd.Series:
Moving Average (MA) values in price units.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates the
MA for each asset in the Toolkit instance.
- The simple, exponential, double exponential, triple exponential, zero lag exponential,
Wilder, triangular, weighted and Hull moving averages agree with TA-Lib's SMA, EMA, DEMA, TEMA,
ZLEMA, RMA, TRIMA, WMA and HMA, and the triangular, sine, Fibonacci and Pascal's weighted
averages agree with pandas-ta-classic's swma, sinwma, fwma and pwma.
- finta's TEMA, SMMA and SSMA start their exponential averages on the first price (with
pandas' ewm) instead of seeding them with a simple average over the window, so they
differ during the warm-up and converge afterwards.
- Kaufman Adaptive Moving Average: with the default `short_window` of 2 and `long_window` of 30, which
TA-Lib fixes, the KAMA agrees with TA-Lib's KAMA.
- T3 Moving Average: each of the six EMAs is seeded with the simple average of its first `window`
values, so the T3 starts at period 6 * (window - 1). It agrees with TA-Lib's T3 and
pandas-ta-classic's t3.
- Arnaud Legoux Moving Average: the peak m is rounded down to a whole period, and the ALMA agrees with
TA-Lib's ALMA. pandas-ta-classic's alma measures the offset from the latest price and
keeps m unrounded: its alma with an offset of 0.85 equals this ALMA with an offset of 0.15 and an
unrounded peak, so it puts the weight on the older prices.
- Volume Weighted Moving Average: the VWMA differs from the rolling VWAP
(`get_volume_weighted_average_price`) only in the price it averages: the close instead
of the typical price (High + Low + Close) / 3. It agrees with TA-Lib's VWMA and
pandas-ta-classic's vwma. A window without any volume has no average (NaN).
- McGinley Dynamic: the recursion is seeded with the simple average of the first `window`
prices, as the Toolkit seeds its exponential moving averages. TA-Lib's MCGD and
pandas-ta-classic's mcgd start the recursion from the first price instead. The
difference fades by about a factor 1 - 1 / window per period: with the default window
of 14 the two agree to 0.01% within about 70 periods.
- Variable Index Dynamic Average: the volatility index is the absolute Chande Momentum
Oscillator over unsmoothed sums (Chande & Kroll, 1994), as in TA-Lib and
pandas-ta-classic. Chande's 1992 article and Tulip Indicators' vidya use the ratio of a
short to a long standard deviation instead. The recursion is seeded with the simple
average of `window` prices on the period before the first oscillator value that follows
a full window, as the Toolkit seeds its exponential moving averages. With equal windows
it agrees with pandas-ta-classic's vidya. TA-Lib starts the recursion from the first
price, with the oscillator over the changes available so far, and shows it from period
`cmo_window` on. The difference fades by a factor 1 - Alpha * &#124;CMO&#124; per period: with the
defaults the two agree to 0.01% within about 100 periods.
- Fractal Adaptive Moving Average: FRAMA averages the median price of the high and low, which with the
default `close_column` of "Adj Close" are adjusted for dividends in the same way as the
close. The recursion is seeded with the simple average of the first `window` median
prices, on the window-th period, as the Toolkit seeds its exponential moving averages.
Ehlers and TA-Lib start from the median price of that period, which TA-Lib does not
show, so TA-Lib's FRAMA starts one period later. The difference fades by a factor
1 - Alpha per period: with the default window of 16 the two agree to 0.01% within about
45 periods. A half without a range still gives a dimension, as in TA-Lib: a flat latest
half next to a moving earlier one is a dimension of 1, so FRAMA moves to the price.
Without any range in the window, or in both halves, the last dimension is kept.
- Holt-Winters Moving Average: the HWMA agrees with pandas-ta-classic's hwma. The recursion starts on
each ticker's first close, as in the MQL5 indicator, so there is no warm-up: the weight
of the start fades by a factor 1 - Level Smoothing per period, and the first values of
the price history lean on that close. The channel around it is
`get_holt_winters_channel`.
- Elastic Volume Weighted Moving Average: Fries divides by the number of shares outstanding (the
float); the volume over the window stands in for it, as in finta. The recursion is
seeded with the simple average of the first `window` closes, as the Toolkit seeds its
exponential moving averages. finta starts it from 0, so its eVWMA climbs from 0 to the
price; after that start has faded, about 300 periods with the default window, the two
are equal. A window without any volume keeps the last average.
- Volume Adjusted Moving Average: the VAMA agrees with finta's VAMA; its weight multiplies the volume
ratio by the close as well, so it is the traded value relative to the average volume.
A window without any volume has no average (NaN).
- SuperSmoother: the two-pole filter (Ehlers, 2013) also averages the last two prices,
which removes the two-period cycle completely; the three-pole filter (Ehlers, 2004) is
smoother at the cost of more lag. The filter equals the price on the first two (three)
periods of each ticker's own history and runs from there, as pandas-ta-classic starts
it; Ehlers' listing starts it from zero. The three-pole filter agrees with
pandas-ta-classic's ssf. Its two-pole ssf filters the price itself rather than the
average of the last two prices, which differs by up to 2% on daily prices; applied to
that average the two are equal. √2, √3 and $$\pi$$ are exact, where Ehlers' listings write
1.414 and 3.14159.
- Hilbert Transform Instantaneous Trendline: equals TA-Lib's HT_TRENDLINE and pandas-ta-classic's ht_trendline.
The recursion starts from zero on the 37th period of each ticker's own history, as in
TA-Lib, and the first 63 periods (TA-Lib's lookback) are NaN. Ehlers compares the
trendline with the smoothed price (or MAMA) to tell a trend from a cycle.
- When growth is requested, the method calculates the growth of the MA
over the given lag.
- The Volume Adjusted Moving Average follows finta's definition, which has no published source, and the
Fibonacci and Pascal's weighted averages follow pandas-ta-classic's.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["^GSPC"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_moving_average(window=50).tail(5)
```

Which returns:

| Date       |   ^GSPC |   Benchmark |
|:-----------|--------:|------------:|
| 2025-12-24 | 6784.99 |     669.712 |
| 2025-12-26 | 6790.16 |     670.25  |
| 2025-12-29 | 6795.7  |     670.828 |
| 2025-12-30 | 6800.34 |     671.316 |
| 2025-12-31 | 6802.55 |     671.566 |

---

## get_trix
Calculate the TRIX (Triple Exponential Moving Average oscillator): the rate of change of a triple exponential moving average, which shows momentum without the noise of the shortest moves.

Trix is a momentum oscillator that calculates the percentage rate of change of a triple exponentially smoothed moving average. It helps identify overbought and oversold conditions in a market. With a `signal_window` it adds the signal line, an EMA of the TRIX whose crossings Hutson read as signals, and the histogram, the TRIX minus its signal line.

The formula is as follows:

$$
\text{EMA1} = \operatorname{EMA}(\text{Close},\; \text{Window})
$$

$$
\text{EMA2} = \operatorname{EMA}(\text{EMA1},\; \text{Window})
$$

$$
\text{EMA3} = \operatorname{EMA}(\text{EMA2},\; \text{Window})
$$

$$
\text{TRIX} = \frac{\text{EMA3} - \text{EMA3}\left[- 1\right]}{\text{EMA3}\left[- 1\right]}
$$

$$
\text{Signal Line} = \operatorname{EMA}(\text{TRIX},\; \text{Signal Window})
$$

$$
\text{Histogram} = \text{TRIX} - \text{Signal Line}
$$

**Also known as:** triple smoothed EMA, rate of change oscillator, TRIX signal, TRIXH, TRIX histogram.

**References:**

- paper | Hutson, J.K. (1983). "Good TRIX." Technical Analysis of Stocks & Commodities, 1(5), 105-108.
- library | Referenced against TA-Lib's [TRIX](https://ta-lib.org/functions/trix.html){:target="_blank"}
- library | Shares similar logic as pandas-ta-classic's [trix](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/momentum/trix.py#L18){:target="_blank"}
- library | Shares similar logic as pandas-ta-classic's [trixh](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/momentum/trixh.py#L12){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int, optional):</u> The number of periods of each of the three exponential moving
averages. Defaults to 15, the window of Hutson (1983) and StockCharts.
- <u>signal_window (int &#124; None, optional):</u> The number of periods of the signal line, e.g. 9.
Defaults to None, which returns only the TRIX.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Trix.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame or pd.Series:
Trix values as a decimal (0.001 is 0.1%), or with a `signal_window` the TRIX, Signal Line
and Histogram.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates the
Trix for each asset in the Toolkit instance.
- TRIX is a decimal and agrees with TA-Lib's TRIX divided by 100, since TA-Lib's TRIX is in
percent.
- The signal line is an EMA seeded with the simple average of its first values, as every
EMA of the Toolkit, and agrees with TA-Lib's EMA of the TRIX. pandas-ta-classic's trixh takes
a simple moving average of the TRIX as its signal line instead.
- When growth is requested, the method calculates the growth of the Trix
over the given lag.
- Daily TRIX values are small (a few hundredths of a percent), so four decimals keep
about one significant digit. Pass a higher `rounding` (or None) for more precision.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["^IXIC"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_trix(rounding=6).tail(5)
```

Which returns:

| Date       |    ^IXIC |   Benchmark |
|:-----------|---------:|------------:|
| 2025-12-24 | 0.000367 |    0.000541 |
| 2025-12-26 | 0.000402 |    0.000582 |
| 2025-12-29 | 0.000432 |    0.00062  |
| 2025-12-30 | 0.000454 |    0.000651 |
| 2025-12-31 | 0.000452 |    0.00066  |

---

## get_price_transform
Calculate a Price Transform: the average, median, typical or weighted close price of each period.

A price transform condenses the open, high, low and close of a period into one price. Indicators that should reflect the whole bar rather than only the close are built on them: the Commodity Channel Index, Money Flow Index and VWAP on the typical price, the Awesome Oscillator and FRAMA on the median price. The weighted close counts the close twice, as the price the period settled at.

The formula is as follows, per method:

$$
\text{Average price:}\;\; \text{Average Price} = \frac{\text{Open} + \text{High} + \text{Low} + \text{Close}}{4}
$$

$$
\text{Median price:}\;\; \text{Median Price} = \frac{\text{High} + \text{Low}}{2}
$$

$$
\text{Typical price:}\;\; \text{Typical Price} = \frac{\text{High} + \text{Low} + \text{Close}}{3}
$$

$$
\text{Weighted close price:}\;\; \text{Weighted Close Price} = \frac{\text{High} + \text{Low} + 2 \cdot \text{Close}}{4}
$$

**Also known as:** AVGPRICE, average price, OHLC4, MEDPRICE, median price, HL2, TYPPRICE, typical price, HLC3, pivot price, WCLPRICE, weighted close price, HLCC4.

**References:**

- paper | Lambert, D.R. (1980). "Commodity Channel Index: Tool for Trading Cyclic Trends." Commodities, October 1980, the typical price of the CCI.
- library | Referenced against TA-Lib's [AVGPRICE](https://ta-lib.org/functions/avgprice.html){:target="_blank"}
- library | Referenced against TA-Lib's [MEDPRICE](https://ta-lib.org/functions/medprice.html){:target="_blank"}
- library | Referenced against TA-Lib's [TYPPRICE](https://ta-lib.org/functions/typprice.html){:target="_blank"}
- library | Referenced against TA-Lib's [WCLPRICE](https://ta-lib.org/functions/wclprice.html){:target="_blank"}
- library | Shares similar logic as pandas-ta-classic's [ohlc4](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/overlap/ohlc4.py#L12){:target="_blank"}
- library | Shares similar logic as pandas-ta-classic's [hl2](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/overlap/hl2.py#L12){:target="_blank"}
- library | Shares similar logic as pandas-ta-classic's [hlc3](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/overlap/hlc3.py#L12){:target="_blank"}
- library | Shares similar logic as pandas-ta-classic's [wcp](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/overlap/wcp.py#L12){:target="_blank"}
- library | Shares similar logic as finta's [TP](https://github.com/peerchemist/finta/blob/1.3/finta/finta.py#L1405){:target="_blank"}
- library | Shares similar logic as Tulip Indicators' [avgprice](https://tulipindicators.org/avgprice){:target="_blank"}
- library | Shares similar logic as Tulip Indicators' [medprice](https://tulipindicators.org/medprice){:target="_blank"}
- library | Shares similar logic as Tulip Indicators' [typprice](https://tulipindicators.org/typprice){:target="_blank"}
- library | Shares similar logic as Tulip Indicators' [wcprice](https://tulipindicators.org/wcprice){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the open, high and low prices are adjusted
for dividends in the same way.
- <u>method (str, optional):</u> The price. Options are: "average" (the average of the open, high, low and
close), "median" (the average of the high and low), "typical" (the average of the high, low and
close), "weighted_close" (the weighted close, (high + low + 2 × close) / 4). Defaults to
"typical".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the price.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame or pd.Series: The price of each period.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the price for each asset in the Toolkit instance.
- The four prices agree with TA-Lib's AVGPRICE, MEDPRICE, TYPPRICE and WCLPRICE.
- When growth is requested, the method calculates the growth of the price over the
given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["NVDA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_price_transform(method="weighted_close").tail(5)
```

Which returns:

| Date       |    NVDA |   Benchmark |
|:-----------|--------:|------------:|
| 2025-12-24 | 187.741 |     684.502 |
| 2025-12-26 | 189.993 |     685.038 |
| 2025-12-29 | 187.339 |     682.413 |
| 2025-12-30 | 187.312 |     681.964 |
| 2025-12-31 | 187.075 |     677.933 |

---

## get_midpoint
Calculate the Midpoint: the middle of the highest and lowest price over a window.

The midpoint is the centre of the range the price covered over the window, a moving average that only looks at the extremes. With the closes it is the midpoint of the highest and lowest close; with the highs and lows it is the midpoint price, the middle line of a Donchian Channel that includes the current period.

The formula is as follows, per method:

$$
\text{Midpoint of the closes:}\;\; \text{Midpoint} = \frac{\text{Highest Close}(\text{Window}) + \text{Lowest Close}(\text{Window})}{2}
$$

$$
\text{Midpoint price:}\;\; \text{Midpoint Price} = \frac{\text{Highest High}(\text{Window}) + \text{Lowest Low}(\text{Window})}{2}
$$

**Also known as:** MIDPOINT, midpoint over period, MIDPRICE, midpoint price, Donchian middle line.

**References:**

- paper | Donchian, R.D. (1960). "Commodities: High Finance in Copper." Financial Analysts Journal, 16(6), 133-142.
- library | Referenced against TA-Lib's [MIDPOINT](https://ta-lib.org/functions/midpoint.html){:target="_blank"}
- library | Referenced against TA-Lib's [MIDPRICE](https://ta-lib.org/functions/midprice.html){:target="_blank"}
- library | Shares similar logic as pandas-ta-classic's [midpoint](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/overlap/midpoint.py#L12){:target="_blank"}
- library | Shares similar logic as pandas-ta-classic's [midprice](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/overlap/midprice.py#L12){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the high and low prices are adjusted for
dividends in the same way.
- <u>window (int, optional):</u> The number of periods, including the current one. Defaults to 14.
- <u>method (str, optional):</u> Options are: "close" (the midpoint of the closes, MIDPOINT), "high_low" (the
midpoint of the highs and lows, MIDPRICE). Defaults to "close".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the midpoint.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame or pd.Series: Midpoint values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the midpoint for each asset in the Toolkit instance.
- The midpoint agrees with TA-Lib's MIDPOINT and the midpoint price its MIDPRICE. The middle
line of `get_donchian_channels` ends one period earlier, so it differs whenever the
current period sets a new high or low.
- When growth is requested, the method calculates the growth of the midpoint over
the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AMZN"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_midpoint(method="high_low").tail(5)
```

Which returns:

| Date       |   AMZN |   Benchmark |
|:-----------|-------:|------------:|
| 2025-12-24 | 226.97 |     674.756 |
| 2025-12-26 | 226.99 |     675.168 |
| 2025-12-29 | 226.99 |     675.168 |
| 2025-12-30 | 226.99 |     675.168 |
| 2025-12-31 | 226.99 |     675.168 |

---

## get_holt_winters_channel
Calculate the Holt-Winters Channel: bands a multiple of the smoothed standard deviation around the Holt-Winters Moving Average, which widen when the price strays from its trend.

The channel draws bands around the Holt-Winters Moving Average at a multiple of an exponentially smoothed standard deviation of the close from the average. It widens when the price strays from its trend and narrows when it follows it, so a close outside the channel marks a move the trend does not explain.

The formula is as follows:

$$
\text{Middle Band} = \text{HWMA} \;(\text{the Holt-Winters Moving Average of} \;\text{get\_moving\_average})
$$

$$
\operatorname{Var}(t) = (1 - \text{Deviation Smoothing}) \cdot \operatorname{Var}(t-1) + \text{Deviation Smoothing} \cdot (\operatorname{Close}(t-1) - \operatorname{HWMA}(t-1))^{2},\;\; \text{starting at 0}
$$

$$
\text{Upper Band} = \operatorname{HWMA}(t) + \text{Multiplier} \cdot \sqrt{\operatorname{Var}(t-1)}
$$

$$
\text{Lower Band} = \operatorname{HWMA}(t) - \text{Multiplier} \cdot \sqrt{\operatorname{Var}(t-1)}
$$

**Also known as:** HWC, Holt-Winters channel, Holt-Winter channel.

**References:**

- paper | Holt, C.C. (1957). "Forecasting Seasonals and Trends by Exponentially Weighted Moving Averages." ONR Memorandum 52, Carnegie Institute of Technology.
- paper | Winters, P.R. (1960). "Forecasting Sales by Exponentially Weighted Moving Averages." Management Science, 6(3), 324-342.
- paper | MQL5 Code Base: HWC ([https://www.mql5.com/en/code/20857](https://www.mql5.com/en/code/20857){:target="_blank"}).
- library | Referenced against pandas-ta-classic's [hwc](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/volatility/hwc.py#L75){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>level_smoothing (float, optional):</u> The smoothing factor of the level. Defaults to 0.2.
- <u>velocity_smoothing (float, optional):</u> The smoothing factor of the velocity. Defaults to 0.1.
- <u>acceleration_smoothing (float, optional):</u> The smoothing factor of the acceleration.
Defaults to 0.1.
- <u>deviation_smoothing (float, optional):</u> The smoothing factor of the variance. Defaults to 0.1.
- <u>multiplier (float, optional):</u> The number of standard deviations of the bands. Defaults to 1.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the bands.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame or pd.Series: The Upper Band, Middle Band and Lower Band.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the channel for each asset in the Toolkit instance.
- The channel agrees with pandas-ta-classic's hwc. The band of a period uses the variance up
to the period before, which holds the deviations up to two periods before, as in the
MQL5 indicator. Since the average starts on the first close, the bands open from the
fourth close on.
- When growth is requested, the method calculates the growth of the bands over the
given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["GOOGL"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_holt_winters_channel().xs("GOOGL", level=1, axis="columns").tail(5)
```

Which returns:

| Date       |   Lower Band |   Middle Band |   Upper Band |
|:-----------|-------------:|--------------:|-------------:|
| 2025-12-24 |      295.027 |       307.333 |      319.639 |
| 2025-12-26 |      294.832 |       306.652 |      318.472 |
| 2025-12-29 |      294.639 |       306.02  |      317.401 |
| 2025-12-30 |      294.532 |       305.508 |      316.484 |
| 2025-12-31 |      294.23  |       304.872 |      315.512 |

---

## get_gann_hilo_activator
Calculate the Gann HiLo Activator: a trailing stop drawn from a moving average of the lows in an uptrend and of the highs in a downtrend, which flips when the close crosses the other average.

The HiLo Activator is a trailing stop drawn from a moving average of the highs and one of the lows. A close above the previous average of the highs turns the trend up, after which the line follows the average of the lows beneath the price; a close below the previous average of the lows turns it down, after which the line follows the average of the highs above the price. A close between the two averages keeps the trend, so the line only flips side on a clear break.

The formula is as follows:

$$
\text{High Average} = \operatorname{SMA}(\text{High},\; \text{High Window}),\;\; \text{Low Average} = \operatorname{SMA}(\text{Low},\; \text{Low Window})
$$

$$
\operatorname{Trend}(t) = 1 \;\text{if Close}(t) > \text{High Average}(t-1),\;\; - 1 \;\text{if Close}(t) < \text{Low Average}(t-1),\;\; \text{otherwise Trend(t-1)}
$$

$$
\text{HiLo Activator}(t) = \text{Low Average}(t) \;\text{when the trend is}\; 1,\;\; \text{High Average(} t \text{) when it is -1}
$$

**Also known as:** HiLo, Gann HiLo, Gann HiLo Activator, HiLo Activator.

**References:**

- paper | Krausz, R. (1998). "The New Gann Swing Chartist." Technical Analysis of Stocks & Commodities, 16(2).
- library | Shares similar logic as pandas-ta-classic's [hilo](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/overlap/hilo.py#L40){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the high and low prices are adjusted for
dividends in the same way.
- <u>high_window (int, optional):</u> The number of periods of the average of the highs.
Defaults to 13.
- <u>low_window (int, optional):</u> The number of periods of the average of the lows.
Defaults to 21.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the activator.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame or pd.Series: The Gann HiLo Activator and the Trend Direction (1 up, -1 down).

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the activator for each asset in the Toolkit instance.
- The line follows the average of the side of the trend every period, as in Krausz's
formula. pandas-ta-classic's hilo keeps the previous value of the line on a close
between the two averages instead, so the two are equal on every period with a close
beyond an average and differ on the others.
- The defaults are those of pandas-ta-classic and TradingView (13 and 21 periods);
Krausz used three-period averages of both.
- When growth is requested, the method calculates the growth of the activator over
the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AMD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_gann_hilo_activator().xs("AMD", level=1, axis="columns").tail(5)
```

Which returns:

| Date       |   Gann HiLo Activator |   Trend Direction |
|:-----------|----------------------:|------------------:|
| 2025-12-24 |               217.501 |                -1 |
| 2025-12-26 |               216.971 |                -1 |
| 2025-12-29 |               216.295 |                -1 |
| 2025-12-30 |               215.85  |                -1 |
| 2025-12-31 |               215.553 |                -1 |

---

## get_zigzag
Calculate the Zig Zag: the swing highs and lows of the prices, ignoring moves smaller than a threshold, which shows the trend's turning points.

The Zig Zag filters out moves smaller than the sensitivity. It follows the highest high of a rising leg until the low falls the sensitivity below it, which confirms that high as a swing high and starts a falling leg from that low, and the lowest low of a falling leg until the high rises the sensitivity above it. Drawn on a chart, the lines between the confirmed swing highs and lows are the zig zag, which shows the waves of the market without the noise in between.

The formula is as follows:

$$
\text{In a rising leg:}\;\; \text{the trend turns down when Low}(t) \leq \text{Extreme} \cdot (1 - \text{Sensitivity}),\;\; \text{otherwise}\;\; \text{Extreme} = \operatorname{High}(t) \;\text{when High}(t) \geq \text{Extreme}
$$

$$
\text{In a falling leg:}\;\; \text{the trend turns up when High}(t) \geq \text{Extreme} \cdot (1 + \text{Sensitivity}),\;\; \text{otherwise}\;\; \text{Extreme} = \operatorname{Low}(t) \;\text{when Low}(t) \leq \text{Extreme}
$$

- A leg only turns once at least Minimum Trend Length periods have passed since its extreme

**Also known as:** ZIGZAG, Zig Zag, swing filter, filtered waves.

**References:**

- paper | Merrill, A.A. (1977). "Filtered Waves: Basic Theory." Analysis Press.
- library | Referenced against TA-Lib's [ZIGZAG](https://ta-lib.org/functions/zigzag.html){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the high and low prices are adjusted for
dividends in the same way.
- <u>sensitivity (float, optional):</u> The reversal from the extreme that turns a leg, as a
decimal (0.05 is 5%). Defaults to 0.05.
- <u>minimum_trend_length (int, optional):</u> The number of periods since the extreme of a
leg before it can turn. Defaults to 1.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the values.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame or pd.Series: The Zig Zag (the extreme of the current leg), the Trend
Direction (1 rising, -1 falling) and the Periods Since Pivot (since that extreme).

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the Zig Zag for each asset in the Toolkit instance.
- Every period shows what is known at its close: the extreme of the current leg, its
direction and how many periods ago it was set. This agrees with TA-Lib's ZIGZAG (with the
sensitivity in percent there and the pivot as a position instead of the periods since
it) and a value never changes once its period has passed. The line drawn on a chart
instead connects the swings, and its last leg is redrawn as long as the leg runs: a
swing high or low is only confirmed by the reversal that follows it, which here is the
period the Trend Direction turns.
- The first leg starts falling from the first low, as in TA-Lib, and the first
`minimum_trend_length` periods are empty. A price equal to the extreme moves the pivot
to the later period.
- When growth is requested, the method calculates the growth of the values over the
given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["SIUSD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_zigzag(sensitivity=0.1).xs("SIUSD", level=1, axis="columns").tail(5)
```

Which returns:

| Date       |   Periods Since Pivot |   Trend Direction |   Zig Zag |
|:-----------|----------------------:|------------------:|----------:|
| 2025-12-26 |                     0 |                 1 |    79.7   |
| 2025-12-28 |                     0 |                 1 |    82.67  |
| 2025-12-29 |                     0 |                -1 |    70.215 |
| 2025-12-30 |                     0 |                 1 |    78.065 |
| 2025-12-31 |                     0 |                -1 |    69.255 |

---

## get_volume_weighted_average_price
Calculate the Volume Weighted Average Price (VWAP): the average price weighted by volume since an anchor date, the price at which most volume traded.

The Volume Weighted Average Price (VWAP) weighs the typical price of each period by its traded volume over a rolling window, giving a more volume-informed view of the average price than a plain moving average.

The formula is as follows:

$$
\text{Typical Price} = \frac{\text{High} + \text{Low} + \text{Close}}{3}
$$

$$
\text{VWAP} = \frac{\operatorname{Sum}(\text{Typical Price} \cdot \text{Volume},\; \text{Window})}{\operatorname{Sum}(\text{Volume},\; \text{Window})}
$$

$$
\text{Anchored VWAP} = \frac{\text{Cumulative Sum}(\text{Typical Price} \cdot \text{Volume})}{\text{Cumulative Sum}(\text{Volume})},\;\; \text{both summed from the anchor on}
$$

The VWAP that trading desks use as an execution benchmark is calculated from the trades of a single session and resets every day. By default this method computes a rolling VWAP over several periods from the high, low, close and volume of each period, which works as a volume-weighted moving average. With an `anchor` the sums start at a fixed point instead: the first period ("all"), the start of every day, week, month, quarter or year (with intraday data and "daily" the session VWAP), or a date such as an earnings release or a market low, the anchored VWAP that shows the average price paid since that event.

**Also known as:** VWAP, anchored VWAP, AVWAP, session VWAP, cumulative VWAP.

**References:**

- paper | Berkowitz, S.A., Logue, D.E., & Noser, E.A. Jr. (1988). "The Total Cost of Transactions on the NYSE." Journal of Finance, 43(1), 97-112.
- paper | Shannon, B. (2023). "Maximum Trading Gains With Anchored VWAP." Alphatrends Publishing.
- library | Referenced against TA-Lib's [VWAP](https://ta-lib.org/functions/vwap.html){:target="_blank"}
- library | Shares similar logic as pandas-ta-classic's [vwap](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/overlap/vwap.py#L18){:target="_blank"}
- library | Shares similar logic as finta's [VWAP](https://github.com/peerchemist/finta/blob/1.3/finta/finta.py#L411){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the open, high and low prices are adjusted
for dividends in the same way.
- <u>window (int, optional):</u> Number of periods to consider for the VWAP.
The number of periods (time intervals) over which to calculate the VWAP, when there is
no anchor. Defaults to 14.
- <u>anchor (str &#124; None, optional):</u> Where the sums start. Options are: "all" (the first period),
"daily" (the start of every day), "weekly" (the start of every week), "monthly" (the start of
every month), "quarterly" (the start of every quarter), "yearly" (the start of every year), or a
date such as "2024-08-05" for the VWAP from that date on (empty before it). Defaults to None,
which takes the rolling `window`.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the VWAP.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame or pd.Series:
Volume Weighted Average Price (VWAP) values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates the
VWAP for each asset in the Toolkit instance.
- The VWAP is taken over a rolling `window` by default. TA-Lib's VWAP accumulates the
typical price times volume from the first period on, which is the anchor of all periods here
(equal to TA-Lib's VWAP), and pandas-ta-classic's vwap starts the sums at every calendar period
of its anchor, which is the daily, weekly, monthly, quarterly or yearly anchor here.
- The anchor of all periods starts on the first period of the price history the Toolkit loaded,
which can be before `start_date`.
- When growth is requested, the method calculates the growth of the VWAP
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["SPY"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
    benchmark_ticker=None,
)

toolkit.technicals.get_volume_weighted_average_price().tail(5)
```

Which returns:

| Date       |     SPY |
|:-----------|--------:|
| 2025-12-24 | 675.242 |
| 2025-12-26 | 675.346 |
| 2025-12-29 | 675.664 |
| 2025-12-30 | 675.891 |
| 2025-12-31 | 675.847 |

---

## get_parabolic_sar
Calculate the Parabolic Stop and Reverse (SAR): a trailing stop that speeds up as the trend extends and flips side when the price crosses it.

The Parabolic SAR is a trend-following indicator that trails price action, flipping from below to above price (and vice versa) whenever the trend reverses. The acceleration factor increases as the trend extends, causing the SAR to converge towards price over time.

The formula is as follows:

$$
\text{Uptrend SAR} = \text{Prior SAR} + \text{AF} \cdot (\text{Extreme Point} - \text{Prior SAR})
$$

$$
\text{Downtrend SAR} = \text{Prior SAR} - \text{AF} \cdot (\text{Prior SAR} - \text{Extreme Point})
$$

- AF starts at the initial acceleration factor and rises by the increment with every new extreme point, up to the maximum, each with its own value for long and short trades

- On a reversal the SAR is the extreme point of the trade that ends, moved away from the price by the offset on reverse

The extended parameters (separate acceleration factors for short trades, a start value and an offset on reverse) are those of TA-Lib's SAREXT; the defaults give Wilder's SAR.

**Also known as:** Parabolic SAR, stop and reverse, PSAR, SAREXT, extended parabolic SAR.

**References:**

- paper | Wilder, J.W. Jr. (1978). "New Concepts in Technical Trading Systems." Trend Research.
- library | Referenced against TA-Lib's [SAR](https://ta-lib.org/functions/sar.html){:target="_blank"}
- library | Referenced against TA-Lib's [SAREXT](https://ta-lib.org/functions/sarext.html){:target="_blank"}
- library | Shares similar logic as pandas-ta-classic's [psar](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/trend/psar.py#L73){:target="_blank"}
- library | Shares similar logic as pandas-ta-classic's [sarext](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/trend/sarext.py#L156){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>af_start (float, optional):</u> Initial acceleration factor. Defaults to 0.02.
- <u>af_increment (float, optional):</u> Amount by which the acceleration factor
increases every time a new extreme point is reached. Defaults to 0.02.
- <u>af_max (float, optional):</u> Maximum value the acceleration factor can reach.
Defaults to 0.2.
- <u>af_start_short (float &#124; None, optional):</u> Initial acceleration factor of a short trade.
Defaults to None, which takes `af_start` (so the same factor for both directions).
- <u>af_increment_short (float &#124; None, optional):</u> Increment of the acceleration factor of a
short trade. Defaults to None, which takes `af_increment`.
- <u>af_max_short (float &#124; None, optional):</u> Maximum acceleration factor of a short trade.
Defaults to None, which takes `af_max`.
- <u>start_value (float, optional):</u> The SAR of the first trade: a positive value starts a long
trade at that SAR and a negative value a short trade at its absolute value. Defaults
to 0, which derives the start from the first two periods.
- <u>offset_on_reverse (float, optional):</u> The share by which the SAR moves away from the price
on a reversal, as a decimal (0.01 is 1%). Defaults to 0.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Parabolic SAR.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame or pd.Series:
Parabolic SAR values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates the
Parabolic SAR for each asset in the Toolkit instance.
- The Parabolic SAR agrees with TA-Lib's SAR, which takes `af_increment` equal to `af_start`, and
its SAREXT for any acceleration factors, start value and offset on reverse. TA-Lib's
SAREXT returns the SAR negated during a short trade to mark the direction; here it is
always the price level.
- When growth is requested, the method calculates the growth of the Parabolic SAR
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["CLUSD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_parabolic_sar().tail(5)
```

Which returns:

| Date       |   CLUSD |   Benchmark |
|:-----------|--------:|------------:|
| 2025-12-26 | 55.5988 |     666.32  |
| 2025-12-28 | 55.8613 |     nan     |
| 2025-12-29 | 56.1028 |     667.918 |
| 2025-12-30 | 56.325  |     669.389 |
| 2025-12-31 | 56.5294 |     670.742 |

---

## get_pivot_points
Calculate the Pivot Points: the levels of support and resistance derived from the previous period's high, low and close.

Pivot Points are calculated from the previous period's high, low and close prices and are used to identify potential support and resistance levels for the current period. The classic (floor trader) pivots are the default; the Fibonacci, Camarilla, Woodie and DeMark pivots place the levels differently, and the central pivot range adds a zone around the pivot point whose width reflects the previous period's range.

The formula is as follows, with H, L, C and O the previous period's high, low, close and open:

$$
\text{Classic:}\;\; \text{Pivot Point} \;(P) = \frac{H + L + C}{3},\;\; \text{Resistance}\; 1 = 2 \cdot P - L,\;\; \text{Support}\; 1 = 2 \cdot P - H,\;\; \text{Resistance}\; 2 = P + (H - L),\;\; \text{Support}\; 2 = P - (H - L),\;\; \text{Resistance}\; 3 = H + 2 \cdot (P - L),\;\; \text{Support}\; 3 = L - 2 \cdot (H - P)
$$

$$
\text{Fibonacci:}\;\; P = \frac{H + L + C}{3},\;\; \text{Resistance}\; n = P + \text{Ratio} \cdot (H - L)\;\;\text{and}\;\; \text{Support}\; n = P - \text{Ratio} \cdot (H - L),\;\; \text{with the ratios 0.382, 0.618 and 1.0}
$$

$$
\text{Camarilla:}\;\; P = \frac{H + L + C}{3},\;\; \text{Resistance}\; n = C + \frac{(H - L) \cdot 1.1}{\text{Divisor}}\;\;\text{and}\;\; \text{Support}\; n = C - \frac{(H - L) \cdot 1.1}{\text{Divisor}},\;\; \text{with the divisors 12, 6, 4 and 2}
$$

$$
\text{Woodie:}\;\; P = \frac{H + L + 2 \cdot C}{4},\;\; \text{Resistance}\; 1 = 2 \cdot P - L,\;\; \text{Support}\; 1 = 2 \cdot P - H,\;\; \text{Resistance}\; 2 = P + (H - L),\;\; \text{Support}\; 2 = P - (H - L)
$$

$$
\text{DeMark:}\;\; X = H + 2 \cdot L + C \;\text{when}\; C < O,\;\; 2 \cdot H + L + C \;\text{when}\; C > O \;\text{and}\; H + L + 2 \cdot C \;\text{otherwise};\;\; P = \frac{X}{4},\;\; \text{Resistance}\; 1 = \frac{X}{2} - L,\;\; \text{Support}\; 1 = \frac{X}{2} - H
$$

$$
\text{Central pivot range:}\;\; \text{Bottom Central Pivot} = \frac{H + L}{2},\;\; \text{Top Central Pivot} = 2 \cdot P - \text{Bottom Central Pivot}
$$

**Also known as:** pivot points, floor trader pivots, Fibonacci pivots, Camarilla pivots, Woodie pivots, DeMark pivots, central pivot range, CPR.

**References:**

- paper | Person, J.L. (2004). "A Complete Guide to Technical Trading Tactics." Wiley.
- paper | DeMark, T.R. (1994). "The New Science of Technical Analysis." Wiley.
- paper | Ochoa, F. (2010). "Secrets of a Pivot Boss: Revealing Proven Methods for Profiting in the Market." 311 Publishing.
- library | Referenced against pandas-ta-classic's [cpr](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/trend/cpr.py#L76){:target="_blank"}
- library | Shares similar logic as finta's [PIVOT](https://github.com/peerchemist/finta/blob/1.3/finta/finta.py#L1123){:target="_blank"}
- library | Shares similar logic as finta's [PIVOT_FIB](https://github.com/peerchemist/finta/blob/1.3/finta/finta.py#L1162){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the open, high and low prices are adjusted
for dividends in the same way.
- <u>method (str, optional):</u> The pivots. Options are: "classic" (classic floor pivots),
"fibonacci" (Fibonacci pivots), "camarilla" (Camarilla pivots), "woodie" (Woodie's pivots),
"demark" (DeMark's pivots). Defaults to "classic".
- <u>central_pivot_range (bool, optional):</u> Whether to add the Top and Bottom Central Pivot.
Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Pivot Points.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame:
Pivot Points: the pivot with resistance and support 1-3 (classic and Fibonacci), 1-4
(Camarilla), 1-2 (Woodie) or 1 (DeMark), and the central pivots when asked for.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates the
Pivot Points for each asset in the Toolkit instance.
- Every level comes from the previous period, so it is known at the open of the period.
- The classic, Fibonacci, Camarilla and Woodie pivots and the central pivot range equal
pandas-ta-classic's cpr; the classic and Fibonacci pivots also agree with finta's PIVOT and
PIVOT_FIB, which add a fourth level. The Woodie pivot weights the previous close twice,
as in pandas-ta-classic; some charting packages take the current open instead.
- When growth is requested, the method calculates the growth of the Pivot Points
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["EURUSD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

pivot_points = toolkit.technicals.get_pivot_points().xs("EURUSD", level=1, axis="columns")

pivot_points.loc[:, ["Pivot Point", "Resistance 1", "Resistance 2", "Support 1", "Support 2"]].tail(5)
```

Which returns:

| Date       |   Pivot Point |   Resistance 1 |   Resistance 2 |   Support 1 |   Support 2 |
|:-----------|--------------:|---------------:|---------------:|------------:|------------:|
| 2025-12-26 |        1.1785 |         1.1793 |         1.1802 |      1.1777 |      1.1768 |
| 2025-12-28 |        1.1776 |         1.1791 |         1.1812 |      1.1756 |      1.1741 |
| 2025-12-29 |        1.1772 |         1.178  |         1.1794 |      1.1759 |      1.1751 |
| 2025-12-30 |        1.177  |         1.1791 |         1.181  |      1.1752 |      1.1731 |
| 2025-12-31 |        1.1757 |         1.1771 |         1.1793 |      1.1734 |      1.1721 |

---

## get_support_resistance_levels
Calculate the support and resistance levels: the prices at which the prices repeatedly stopped falling (support) or rising (resistance).

The Support and Resistance Levels are price levels where the price tends to stop and reverse.

- Support Levels: These are the valleys where the price tends to stop going down and may start to go up. Think of support levels as "floors" that the price has trouble falling below.
- Resistance Levels: These are the peaks where the price tends to stop going up and may start to go down. Think of resistance levels as "ceilings" that the price has trouble breaking through.

It does so by:

- Looking for Peaks and Valleys: The function looks at the stock prices and finds the high points (peaks) and low points (valleys) over time.
- Grouping Similar Peaks and Valleys: Sometimes, prices will stop at similar points multiple times. The function groups these similar peaks and valleys together to identify key resistance and support levels.

The formula is as follows:

$$
\text{Peak} \;(t) = \text{Close} \;(t) \;\text{if Close} \;(t) > \text{every Close within} \;\text{window} \;\text{periods before and after}\; t \;(14 \;\text{by default})
$$

$$
\text{Valley} \;(t) = \text{Close} \;(t) \;\text{if Close} \;(t) < \text{every Close within} \;\text{window} \;\text{periods before and after}\; t
$$

$$
\text{Level} = \frac{\text{Existing Level} + \text{Peak or Valley}}{2} \;\text{if} \;\frac{\left|\text{Peak or Valley} - \text{Existing Level}\right|}{\left|\text{Existing Level}\right|} < \text{Sensitivity} \;(0.05 \;\text{by default}),\;\; \text{otherwise a new level at the Peak or Valley}
$$

$$
\text{Resistance} \;(t) = \text{the most recent level from the peaks published up to}\; t,\;\; \text{and Support (} t \text{) the same for the valleys, with each level published window periods after its peak or valley (when it is confirmed)}
$$

Where Close is the `close_column`, the Adj Close by default (the Close for intraday data).

**Also known as:** support levels, resistance levels, pivot points.

**References:**

- paper | Murphy, J.J. (1999). "Technical Analysis of the Financial Markets." New York Institute of Finance.

**Args:**

- <u>sensitivity (float, optional):</u> The sensitivity parameter to determine the significance of the peaks
and valleys. A higher sensitivity value will result in fewer support and resistance levels
being identified. Defaults to 0.05.
- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int, optional):</u> Number of periods for calculating support and resistance levels.
The number of periods (time intervals) over which to calculate the support and resistance levels.
Defaults to 14.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
If None, the rounding value specified during the initialization of the Toolkit instance will be used.
Defaults to None.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the levels.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: The support and resistance levels for each asset.

**Raises:**

ValueError: If the specified `period` is not one of the valid options.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates the
support and resistance levels for each asset in the Toolkit instance.
- A level is only identified on the handful of dates where a new local maximum or minimum
is confirmed. The result is forward-filled so every date shows the most recently
confirmed level (NaN before the first level is confirmed for that asset).
- Levels are identified with a centred pivot window, which cannot confirm an extreme
until `window` further periods have printed without exceeding it. Every level is
therefore published with a confirmation lag of exactly `window` periods, and the
series is append-only: a value read at any date is exactly the value that was
available at that date, so the output is safe to use in a backtest.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["GCUSD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_support_resistance_levels().xs("GCUSD", level=1, axis="columns").tail(5)
```

Which returns:

| Date       |   Resistance |   Support |
|:-----------|-------------:|----------:|
| 2025-12-26 |       4359.4 |    3960.5 |
| 2025-12-28 |       4359.4 |    3960.5 |
| 2025-12-29 |       4359.4 |    3960.5 |
| 2025-12-30 |       4359.4 |    3960.5 |
| 2025-12-31 |       4359.4 |    3960.5 |

---

## get_fibonacci_retracement_levels
Calculate the Fibonacci Retracement Levels: the prices at the Fibonacci ratios of the range between the high and the low, where a pullback may find support or resistance.

Fibonacci Retracement Levels are horizontal price levels, derived from ratios found in the Fibonacci sequence, that traders watch as potential support (during a pullback within an uptrend) or resistance (during a bounce within a downtrend) zones. For every date, the swing high and swing low are taken as the rolling maximum high and rolling minimum low over the specified `window`, and the retracement levels are derived from that high/low pair.

The formula is as follows:

$$
\text{Uptrend (retracing down from the high):}\;\; \text{Level} = \text{High} - \text{Ratio} \cdot (\text{High} - \text{Low})
$$

$$
\text{Downtrend (retracing up from the low):}\;\; \text{Level} = \text{Low} + \text{Ratio} \cdot (\text{High} - \text{Low})
$$

**Also known as:** Fibonacci retracement, Fib levels, retracement levels.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int, optional):</u> The number of periods over which the rolling swing high
(maximum) and swing low (minimum) are determined. Defaults to 14.
- <u>levels (list[float] &#124; None, optional):</u> The Fibonacci ratios to calculate levels for.
Defaults to the standard [0.0, 0.236, 0.382, 0.5, 0.618, 0.786, 1.0].
- <u>trend (str, optional):</u> The direction of the prior move. Options are: "uptrend" (levels measured down
from the high — the conventional direction, used when a prior move was up and price is now
pulling back), "downtrend" (levels measured up from the low, used when a prior move was down and
price is now bouncing). Defaults to "uptrend".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the retracement levels.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: Fibonacci Retracement Levels, one column per ratio in
`levels`, labelled by the ratio expressed as a percentage (e.g. "23.6%").

**Raises:**

ValueError: If the specified `period` is not one of the valid options, or if `trend`
is not "uptrend" or "downtrend".

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the Fibonacci Retracement Levels for each asset in the Toolkit instance.
- The 50% level is not actually a Fibonacci ratio. It is included purely by long-standing
market convention, based on the Dow Theory observation that markets often retrace
about half of a prior move.
- The 78.6% level is the square root of 0.618, not a ratio drawn directly from the
Fibonacci sequence itself (unlike 23.6%, 38.2% and 61.8%, which are).
- The columns sort lexicographically by their label (so "100.0%" sorts right after
"0.0%", ahead of "23.6%"), matching the sorting convention used by every other
multi-column indicator in this module (e.g. Pivot Points' Resistance/Support levels).
- There is no single canonical academic paper behind Fibonacci Retracement Levels — the
indicator is a practitioner tool derived from the Fibonacci sequence's ratios rather
than a published financial model. The standard textbook treatment is Murphy, J.J.
(1999). "Technical Analysis of the Financial Markets." New York Institute of Finance.
- When growth is requested, the method calculates the growth of the retracement levels
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["BTCUSD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_fibonacci_retracement_levels().xs("BTCUSD", level=1, axis="columns").tail(5)
```

Which returns:

| Date       |    0.0% |   100.0% |   23.6% |   38.2% |   50.0% |   61.8% |   78.6% |
|:-----------|--------:|---------:|--------:|--------:|--------:|--------:|--------:|
| 2025-12-27 | 90541.8 |    84400 | 89092.3 | 88195.6 | 87470.9 | 86746.2 | 85714.3 |
| 2025-12-28 | 90541.8 |    84400 | 89092.3 | 88195.6 | 87470.9 | 86746.2 | 85714.3 |
| 2025-12-29 | 90541.8 |    84400 | 89092.3 | 88195.6 | 87470.9 | 86746.2 | 85714.3 |
| 2025-12-30 | 90541.8 |    84400 | 89092.3 | 88195.6 | 87470.9 | 86746.2 | 85714.3 |
| 2025-12-31 | 90541.8 |    84400 | 89092.3 | 88195.6 | 87470.9 | 86746.2 | 85714.3 |

---

## get_guppy_multiple_moving_averages
Calculate Daryl Guppy's Multiple Moving Averages (GMMA), whose spread and order show the strength of the traders' and the investors' trend.

They are a group of short and a group of long exponential moving averages, returned with the spreads of the two groups.

The Guppy Multiple Moving Averages are two groups of Exponential Moving Averages: a short group of 3 to 15 periods that follows the traders, and a long group of 30 to 60 periods that follows the investors. A trend is up when the short group lies above the long group and down when it lies below, and a change of trend shows where the groups cross.

The formula is as follows:

$$
\text{Short EMA}(n) = \operatorname{EMA}(\text{Close},\; n),\;\; \text{for } n \text{ in 3, 5, 8, 10, 12 and 15}
$$

$$
\text{Long EMA}(n) = \operatorname{EMA}(\text{Close},\; n),\;\; \text{for } n \text{ in 30, 35, 40, 45, 50 and 60}
$$

$$
\text{Short Group Spread} = \max(\text{Short EMAs}) - \min(\text{Short EMAs})
$$

$$
\text{Long Group Spread} = \max(\text{Long EMAs}) - \min(\text{Long EMAs})
$$

$$
\text{Group Spread} = \operatorname{Mean}(\text{Short EMAs}) - \operatorname{Mean}(\text{Long EMAs})
$$

Guppy reads the spread within each group as the conviction of that group: a long group that widens confirms the trend, one that compresses warns that the investors are changing their minds, and a short group that compresses near the long group marks a pause in which the traders test the trend. The Group Spread is positive when the short group lies above the long group, and its sign changes where the groups cross.

**Also known as:** GMMA, Guppy multiple moving average, Guppy ribbons.

**References:**

- paper | Guppy, D. (2004). "Trend Trading: A Seven-Step Approach to Success." Wiley.
- library | Referenced against TTR (R)'s [GMMA](https://github.com/joshuaulrich/TTR/blob/v0.24.4/R/GMMA.R#L55){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>short_windows (list[int] &#124; None, optional):</u> The windows of the short group. Defaults to
None, which uses Guppy's 3, 5, 8, 10, 12 and 15.
- <u>long_windows (list[int] &#124; None, optional):</u> The windows of the long group. Defaults to
None, which uses Guppy's 30, 35, 40, 45, 50 and 60.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: The short EMAs ("Short EMA 3" and on), the long EMAs ("Long
EMA 30" and on), the Short Group Spread, the Long Group Spread and the Group Spread, in
price units.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates the
averages for each asset in the Toolkit instance.
- The averages are the exponential moving averages of `get_moving_average`, seeded with the
simple average of their first `n` prices, and equal TTR's GMMA. The spreads start once
every average of their groups has started; TTR's GMMA returns the averages only.
- When growth is requested, the method calculates the growth of the averages over the
given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

guppy = toolkit.technicals.get_guppy_multiple_moving_averages()

guppy.xs("AAPL", level=1, axis="columns").iloc[:, [0, 11, 12, 13, 14]].tail(5)
```

Which returns:

| Date       |   Short EMA 3 |   Long EMA 60 |   Short Group Spread |   Long Group Spread |   Group Spread |
|:-----------|--------------:|--------------:|---------------------:|--------------------:|---------------:|
| 2025-12-24 |       272.079 |       265.43  |               1.4554 |              6.9689 |         3.2856 |
| 2025-12-26 |       272.265 |       265.66  |               1.1666 |              6.742  |         3.1498 |
| 2025-12-29 |       272.537 |       265.894 |               0.9006 |              6.5339 |         3.0817 |
| 2025-12-30 |       272.335 |       266.099 |               0.8491 |              6.3103 |         2.8482 |
| 2025-12-31 |       271.625 |       266.257 |               1.2684 |              6.056  |         2.4064 |

---

## get_candlestick_patterns
Recognise 62 classic candlestick patterns in every ticker's candles: the shapes of one to five candles that traders read as a reversal or a continuation of the trend.

Candlestick charting reads the open, high, low and close of a period as one candle: the real body between the open and the close and the shadows up to the high and down to the low. Certain shapes and sequences are read as a sign that a move is ending or continuing.

Each pattern is 1 on the candle that completes it as a bullish pattern, -1 as a bearish pattern and 0 otherwise (TA-Lib's +100 and -100 divided by 100). The weaker engulfing, harami and harami cross, where one end of the two real bodies is equal, are 0.8 and -0.8 (TA-Lib's 80). The dojis (doji, dragonfly, gravestone and long-legged doji, rickshaw man and takuri) are indecision rather than a direction and are 1 when present; a marubozu, a spinning top, a belt-hold, a closing marubozu, a high-wave, long line and short line candle and an inside bar take the colour of the candle (1 white, -1 black). A hikkake and a modified hikkake are 1 or -1 on the candle that completes them and 2 or -2 on the later candle that confirms them (TA-Lib's +200 and -200 divided by 100, like every other value).

The patterns:

- Doji: an open and close nearly equal.
- Hammer (bullish) and Hanging Man (bearish): a short real body at the top of a long lower shadow, near the previous low or the previous high respectively.
- Inverted Hammer (bullish) and Shooting Star (bearish): a short real body at the bottom of a long upper shadow that gaps down or up from the previous real body.
- Engulfing: a real body that engulfs the previous real body of the opposite colour.
- Harami: a short real body inside the previous long real body, opposite to its colour.
- Piercing Line (bullish) and Dark Cloud Cover (bearish): a long candle followed by one of the opposite colour that opens beyond the previous low (high) and closes past the middle of the previous real body.
- Morning Star (bullish) and Evening Star (bearish): a long real body, a short real body that gaps away from it and a real body of the opposite colour that closes at least 30% into the first.
- Three White Soldiers (bullish) and Three Black Crows (bearish): three long-enough candles of one colour with ever higher (lower) closes, each opening within the previous real body.
- Marubozu: a long real body with (almost) no shadows.
- Spinning Top: a short real body with both shadows longer than the body.
- Belt-hold: a long real body without (or with a very short) shadow on the side of the open: a white candle opening on its low (bullish) or a black candle opening on its high (bearish).
- Closing Marubozu: a long real body without (or with a very short) shadow on the side of the close.
- Dragonfly Doji and Takuri: a doji at the top of the range, with a lower shadow (a very long one, more than twice the body, for the takuri).
- Gravestone Doji: a doji at the bottom of the range, with an upper shadow.
- Long-Legged Doji: a doji with at least one long shadow, and Rickshaw Man: a doji with two long shadows and the body near the middle of the range.
- High-Wave Candle: a short real body with very long upper and lower shadows.
- Long Line Candle and Short Line Candle: a long (short) real body with short shadows.
- Inside Bar: a candle whose high is below and low is above the previous candle's, a price-action pattern (pandas-ta-classic's cdl_inside) and the start of a hikkake.
- Counterattack: two long real bodies of opposite colour that close at the same price, in the direction of the second.
- Doji Star: a long real body followed by a doji that gaps away from it, opposite to the colour of the first candle; Harami Cross: a doji inside the previous long real body, opposite to its colour.
- Homing Pigeon (bullish): a short black real body inside the previous long black one.
- In-Neck, On-Neck and Thrusting (bearish): a long black candle followed by a white candle that opens below its low and closes at its close (in-neck), at its low (on-neck) or above its close but not above the middle of its real body (thrusting).
- Kicking: a marubozu followed by a marubozu of the opposite colour that gaps away from it, in the direction of the second; Kicking by Length: in the direction of the longer one.
- Matching Low (bullish): two black candles that close at the same price.
- Separating Lines: two candles of opposite colour that open at the same price, the second a long real body without (or with a very short) shadow on the side of the open, in its direction.
- Three Inside and Three Outside (Up or Down): a harami or an engulfing pattern confirmed by a third candle that closes beyond the first candle's open (inside) or the second candle's close (outside).
- Morning Doji Star (bullish) and Evening Doji Star (bearish): the morning and evening star with a doji as the middle candle.
- Two Crows (bearish): a long white candle, a black candle that gaps above it and a black candle that opens within the second real body and closes within the first; Upside Gap Two Crows (bearish): a long white candle, a short black candle that gaps above it and a black candle that engulfs the second and still closes above the first close.
- Three Stars in the South (bullish): three black candles that shrink: a long one with a long lower shadow, a smaller one with a low within the first's range and a lower shadow, and a short one with (almost) no shadows inside the second candle's range.
- Abandoned Baby: a long real body, a doji whose shadows gap away from it and a candle of the opposite colour that gaps away from the doji the other way and closes at least 30% into the first body, in the direction of the third candle.
- Advance Block (bearish) and Stalled Pattern (bearish): three white candles with higher closes whose advance weakens: ever shorter bodies or long upper shadows (advance block), or two long white candles followed by a short one riding on the second (stalled).
- Side-by-Side White Lines: two white candles of the same size and open beyond a gap, bullish after a gap up and bearish after a gap down.
- Identical Three Crows (bearish): three declining black candles, each opening at the previous close.
- Stick Sandwich (bullish): two black candles that close at the same price around a white candle trading above the first close.
- Tasuki Gap: a gap followed by a candle in its direction and a candle of the opposite colour of about the same size that closes inside the gap, in the direction of the gap.
- Tri-Star: three dojis, the middle one gapping away; bullish after a gap down, bearish after a gap up.
- Unique Three River (bullish): a long black candle, a black harami with a lower low and a short white candle opening above that low.
- Gap Three Methods (Upside or Downside): two candles of one colour with a gap between them and a candle of the opposite colour that closes the gap, in the direction of the gap.
- Three-Line Strike: three candles of one colour with ever higher (white) or lower (black) closes, struck back by a candle of the other colour that closes beyond the first open, in the direction of the three.
- Concealing Baby Swallow (bullish): two black candles without shadows, a black candle that gaps down with an upper shadow reaching into the second body, and a black candle that engulfs it including its shadows.
- Breakaway: a long candle, a candle of its colour that gaps away from it, two candles that move further away and a candle of the other colour that closes inside the gap, in the direction of the last candle.
- Ladder Bottom (bullish): three black candles with lower opens and closes, a black candle with an upper shadow and a white candle that opens above its open and closes above its high.
- Mat Hold (bullish): a long white candle, a short black candle that gaps above it and two more short falling candles that hold in the upper half of its body, followed by a white candle that closes above all three.
- Rising/Falling Three Methods: a long candle, three short falling (rising) candles of the other colour within its range and a long candle of the first colour that closes beyond the first close, in the direction of the first candle.
- Hikkake: an inside bar followed by a candle that breaks out of it with a lower high and low (1, a false breakdown) or a higher high and low (-1, a false breakout), confirmed (2 or -2) by the first close beyond the other side of the inside bar within 3 candles; Modified Hikkake: the same after two inside bars in a row, the first closing near its low (bullish) or high (bearish).

Sizes are relative to the ticker's own recent candles, as in TA-Lib: a real body is long (short) when it is longer (shorter) than the average real body of the 10 previous candles, a doji's body is at most 10% and a very short shadow less than 10% of their average high-low range, a short shadow is shorter than their average shadow (half the average sum of both shadows), a long shadow is longer than the candle's own real body and a very long shadow longer than twice that body, "near" is within 20% and "far" at least 60% of the average high-low range of the 5 previous candles, and two prices are the same ("equal") when they are within 5% of that range.

**Also known as:** candlestick patterns, candle patterns, CDL, Japanese candlesticks, belt hold, dragonfly doji, gravestone doji, long-legged doji, rickshaw man, takuri, high wave, inside bar, counterattack lines, meeting lines, doji star, harami cross, homing pigeon, in neck, on neck, thrusting line, kicker, matching low, separating lines, three inside up, three inside down, three outside up, three outside down, morning doji star, evening doji star, two crows, three stars in the south, abandoned baby, advance block, deliberation, stalled pattern, upside gap side-by-side white lines, downside gap side-by-side white lines, identical three crows, stick sandwich, upside tasuki gap, downside tasuki gap, tri star, unique three river bottom, upside gap two crows, upside gap three methods, downside gap three methods, three line strike, concealing baby swallow, breakaway, ladder bottom, mat hold, rising three methods, falling three methods, hikkake, modified hikkake.

**References:**

- paper | Nison, S. (1991). "Japanese Candlestick Charting Techniques." New York Institute of Finance.
- paper | Bulkowski, T.N. (2008). "Encyclopedia of Candlestick Charts." Wiley.
- paper | Chesler, D. (2004). "Trading False Moves with the Hikkake Pattern." Active Trader, April 2004.
- library | Referenced against TA-Lib's [CDL2CROWS](https://ta-lib.org/functions/cdl2crows.html){:target="_blank"}
- library | Referenced against TA-Lib's [CDL3BLACKCROWS](https://ta-lib.org/functions/cdl3blackcrows.html){:target="_blank"}
- library | Referenced against TA-Lib's [CDL3INSIDE](https://ta-lib.org/functions/cdl3inside.html){:target="_blank"}
- library | Referenced against TA-Lib's [CDL3LINESTRIKE](https://ta-lib.org/functions/cdl3linestrike.html){:target="_blank"}
- library | Referenced against TA-Lib's [CDL3OUTSIDE](https://ta-lib.org/functions/cdl3outside.html){:target="_blank"}
- library | Referenced against TA-Lib's [CDL3STARSINSOUTH](https://ta-lib.org/functions/cdl3starsinsouth.html){:target="_blank"}
- library | Referenced against TA-Lib's [CDL3WHITESOLDIERS](https://ta-lib.org/functions/cdl3whitesoldiers.html){:target="_blank"}
- library | Referenced against TA-Lib's [CDLABANDONEDBABY](https://ta-lib.org/functions/cdlabandonedbaby.html){:target="_blank"}
- library | Referenced against TA-Lib's [CDLADVANCEBLOCK](https://ta-lib.org/functions/cdladvanceblock.html){:target="_blank"}
- library | Referenced against TA-Lib's [CDLBELTHOLD](https://ta-lib.org/functions/cdlbelthold.html){:target="_blank"}
- library | Referenced against TA-Lib's [CDLBREAKAWAY](https://ta-lib.org/functions/cdlbreakaway.html){:target="_blank"}
- library | Referenced against TA-Lib's [CDLCLOSINGMARUBOZU](https://ta-lib.org/functions/cdlclosingmarubozu.html){:target="_blank"}
- library | Referenced against TA-Lib's [CDLCONCEALBABYSWALL](https://ta-lib.org/functions/cdlconcealbabyswall.html){:target="_blank"}
- library | Referenced against TA-Lib's [CDLCOUNTERATTACK](https://ta-lib.org/functions/cdlcounterattack.html){:target="_blank"}
- library | Referenced against TA-Lib's [CDLDARKCLOUDCOVER](https://ta-lib.org/functions/cdldarkcloudcover.html){:target="_blank"}
- library | Referenced against TA-Lib's [CDLDOJI](https://ta-lib.org/functions/cdldoji.html){:target="_blank"}
- library | Referenced against TA-Lib's [CDLDOJISTAR](https://ta-lib.org/functions/cdldojistar.html){:target="_blank"}
- library | Referenced against TA-Lib's [CDLDRAGONFLYDOJI](https://ta-lib.org/functions/cdldragonflydoji.html){:target="_blank"}
- library | Referenced against TA-Lib's [CDLENGULFING](https://ta-lib.org/functions/cdlengulfing.html){:target="_blank"}
- library | Referenced against TA-Lib's [CDLEVENINGDOJISTAR](https://ta-lib.org/functions/cdleveningdojistar.html){:target="_blank"}
- library | Referenced against TA-Lib's [CDLEVENINGSTAR](https://ta-lib.org/functions/cdleveningstar.html){:target="_blank"}
- library | Referenced against TA-Lib's [CDLGAPSIDESIDEWHITE](https://ta-lib.org/functions/cdlgapsidesidewhite.html){:target="_blank"}
- library | Referenced against TA-Lib's [CDLGRAVESTONEDOJI](https://ta-lib.org/functions/cdlgravestonedoji.html){:target="_blank"}
- library | Referenced against TA-Lib's [CDLHAMMER](https://ta-lib.org/functions/cdlhammer.html){:target="_blank"}
- library | Referenced against TA-Lib's [CDLHANGINGMAN](https://ta-lib.org/functions/cdlhangingman.html){:target="_blank"}
- library | Referenced against TA-Lib's [CDLHARAMI](https://ta-lib.org/functions/cdlharami.html){:target="_blank"}
- library | Referenced against TA-Lib's [CDLHARAMICROSS](https://ta-lib.org/functions/cdlharamicross.html){:target="_blank"}
- library | Referenced against TA-Lib's [CDLHIGHWAVE](https://ta-lib.org/functions/cdlhighwave.html){:target="_blank"}
- library | Referenced against TA-Lib's [CDLHIKKAKE](https://ta-lib.org/functions/cdlhikkake.html){:target="_blank"}
- library | Referenced against TA-Lib's [CDLHIKKAKEMOD](https://ta-lib.org/functions/cdlhikkakemod.html){:target="_blank"}
- library | Referenced against TA-Lib's [CDLHOMINGPIGEON](https://ta-lib.org/functions/cdlhomingpigeon.html){:target="_blank"}
- library | Referenced against TA-Lib's [CDLIDENTICAL3CROWS](https://ta-lib.org/functions/cdlidentical3crows.html){:target="_blank"}
- library | Referenced against TA-Lib's [CDLINNECK](https://ta-lib.org/functions/cdlinneck.html){:target="_blank"}
- library | Referenced against TA-Lib's [CDLINVERTEDHAMMER](https://ta-lib.org/functions/cdlinvertedhammer.html){:target="_blank"}
- library | Referenced against TA-Lib's [CDLKICKING](https://ta-lib.org/functions/cdlkicking.html){:target="_blank"}
- library | Referenced against TA-Lib's [CDLKICKINGBYLENGTH](https://ta-lib.org/functions/cdlkickingbylength.html){:target="_blank"}
- library | Referenced against TA-Lib's [CDLLADDERBOTTOM](https://ta-lib.org/functions/cdlladderbottom.html){:target="_blank"}
- library | Referenced against TA-Lib's [CDLLONGLEGGEDDOJI](https://ta-lib.org/functions/cdllongleggeddoji.html){:target="_blank"}
- library | Referenced against TA-Lib's [CDLLONGLINE](https://ta-lib.org/functions/cdllongline.html){:target="_blank"}
- library | Referenced against TA-Lib's [CDLMARUBOZU](https://ta-lib.org/functions/cdlmarubozu.html){:target="_blank"}
- library | Referenced against TA-Lib's [CDLMATCHINGLOW](https://ta-lib.org/functions/cdlmatchinglow.html){:target="_blank"}
- library | Referenced against TA-Lib's [CDLMATHOLD](https://ta-lib.org/functions/cdlmathold.html){:target="_blank"}
- library | Referenced against TA-Lib's [CDLMORNINGDOJISTAR](https://ta-lib.org/functions/cdlmorningdojistar.html){:target="_blank"}
- library | Referenced against TA-Lib's [CDLMORNINGSTAR](https://ta-lib.org/functions/cdlmorningstar.html){:target="_blank"}
- library | Referenced against TA-Lib's [CDLONNECK](https://ta-lib.org/functions/cdlonneck.html){:target="_blank"}
- library | Referenced against TA-Lib's [CDLPIERCING](https://ta-lib.org/functions/cdlpiercing.html){:target="_blank"}
- library | Referenced against TA-Lib's [CDLRICKSHAWMAN](https://ta-lib.org/functions/cdlrickshawman.html){:target="_blank"}
- library | Referenced against TA-Lib's [CDLRISEFALL3METHODS](https://ta-lib.org/functions/cdlrisefall3methods.html){:target="_blank"}
- library | Referenced against TA-Lib's [CDLSEPARATINGLINES](https://ta-lib.org/functions/cdlseparatinglines.html){:target="_blank"}
- library | Referenced against TA-Lib's [CDLSHOOTINGSTAR](https://ta-lib.org/functions/cdlshootingstar.html){:target="_blank"}
- library | Referenced against TA-Lib's [CDLSHORTLINE](https://ta-lib.org/functions/cdlshortline.html){:target="_blank"}
- library | Referenced against TA-Lib's [CDLSPINNINGTOP](https://ta-lib.org/functions/cdlspinningtop.html){:target="_blank"}
- library | Referenced against TA-Lib's [CDLSTALLEDPATTERN](https://ta-lib.org/functions/cdlstalledpattern.html){:target="_blank"}
- library | Referenced against TA-Lib's [CDLSTICKSANDWICH](https://ta-lib.org/functions/cdlsticksandwich.html){:target="_blank"}
- library | Referenced against TA-Lib's [CDLTAKURI](https://ta-lib.org/functions/cdltakuri.html){:target="_blank"}
- library | Referenced against TA-Lib's [CDLTASUKIGAP](https://ta-lib.org/functions/cdltasukigap.html){:target="_blank"}
- library | Referenced against TA-Lib's [CDLTHRUSTING](https://ta-lib.org/functions/cdlthrusting.html){:target="_blank"}
- library | Referenced against TA-Lib's [CDLTRISTAR](https://ta-lib.org/functions/cdltristar.html){:target="_blank"}
- library | Referenced against TA-Lib's [CDLUNIQUE3RIVER](https://ta-lib.org/functions/cdlunique3river.html){:target="_blank"}
- library | Referenced against TA-Lib's [CDLUPSIDEGAP2CROWS](https://ta-lib.org/functions/cdlupsidegap2crows.html){:target="_blank"}
- library | Referenced against TA-Lib's [CDLXSIDEGAP3METHODS](https://ta-lib.org/functions/cdlxsidegap3methods.html){:target="_blank"}
- library | Shares similar logic as pandas-ta-classic's [cdl_inside](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/candles/cdl_inside.py#L11){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the open, high and low prices are adjusted
for dividends in the same way, so an ex-dividend day doesn't read as a gap. "Close"
uses the candles as traded (split-adjusted).
- <u>patterns (str &#124; list[str] &#124; None, optional):</u> The patterns to return, e.g. ["Hammer",
"Engulfing"] or "hammer, engulfing" (in any casing). Defaults to None, which returns
all 62.
- <u>signals_only (bool, optional):</u> Whether to return only the periods in which at least one
of the returned patterns occurs for at least one ticker. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The patterns per date, with a column per pattern and ticker: 1 (bullish),
-1 (bearish), 0.8 / -0.8 (the weaker engulfing, harami and harami cross), 2 / -2 (a
confirmed hikkake) or 0.

**Notes:**

- The patterns are TA-Lib's definitions (Mario Fortier, [https://ta-lib.org/functions/](https://ta-lib.org/functions/){:target="_blank"}) of the
patterns described by Nison and Bulkowski, and match TA-Lib candle for candle, including its
default candle settings and penetrations (30% for the stars, doji stars and abandoned baby,
50% for the dark cloud cover and the mat hold); the inside bar agrees with pandas-ta-classic's cdl_inside.
- A pattern is empty until TA-Lib's lookback has passed: the 2 to 14 candles its
averages and the pattern itself need (1 for the inside bar, which pandas-ta-classic
sets to 0 on the first candle), counted from the ticker's own first candle.
- TA-Lib marks the gravestone doji, which candlestick analysis reads as bearish after a
rise, as 1 like every doji; so does this method.
- A pattern only describes the candles. The trend before it, which candlestick analysis
requires for a reversal (a hammer after a decline, a hanging man after a rise), is not
checked, as in TA-Lib; combine a pattern with a trend measure such as
`get_moving_average` or `get_signals`. The direction follows TA-Lib: separating lines, a
continuation pattern in candlestick analysis, follow the second candle, the in-neck,
on-neck and thrusting, bearish continuation patterns after a decline, are -1 whatever
the trend, and the tasuki gap, side-by-side white lines and gap three methods follow
the direction of their gap. The breakaway follows its last candle, and the three-line
strike, mat hold and rising/falling three methods their first candles.
- A hikkake is confirmed by a close beyond the inside bar (TA-Lib's measurable form of
Chesler's breakout) within 3 candles. Its confirmation keeps its sign at twice the size,
so 1 / -1 marks the setups and 2 / -2 the confirmations.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

patterns = toolkit.technicals.get_candlestick_patterns(
    patterns="Engulfing", signals_only=True
)

patterns["Engulfing"].tail()
```

Which returns:

| Date       |   AAPL |   MSFT |   Benchmark |
|:-----------|-------:|-------:|------------:|
| 2025-12-10 |      0 |      0 |           1 |
| 2025-12-15 |     -1 |      0 |           0 |
| 2025-12-17 |     -1 |      0 |           0 |
| 2025-12-19 |      1 |      0 |           0 |
| 2025-12-31 |      0 |     -1 |           0 |

---

## get_heikin_ashi
Calculate the Heikin-Ashi ("average bar") candles of every ticker: candles built from two-period averages, which smooth the noise so the trend stands out.

Each candle averages the prices of its period, and its open is the midpoint of the previous Heikin-Ashi candle's body, so the candles smooth out the noise of single periods: a trend shows as a run of candles of one colour, often without a shadow on the side of the open, and a small body with long shadows on both sides hints at a turn.

The formula is as follows:

$$
\text{HA Close} = \frac{\text{Open} + \text{High} + \text{Low} + \text{Close}}{4}
$$

$$
\text{HA Open} = \frac{\text{previous HA Open} + \text{previous HA Close}}{2},\;\; \frac{\text{starting from} \;(\text{Open} + \text{Close})}{2 \;\text{on the first candle}}
$$

$$
\text{HA High} = \max(\text{High},\; \text{HA Open},\; \text{HA Close})
$$

$$
\text{HA Low} = \min(\text{Low},\; \text{HA Open},\; \text{HA Close})
$$

The HA Open is an exponential average of the previous HA Closes with a smoothing factor of 1/2.

**Also known as:** Heikin-Ashi, Heikin Ashi, Heiken Ashi, HA candles, average bar.

**References:**

- paper | Valcu, D. (2004). "Using the Heikin-Ashi Technique." Technical Analysis of Stocks & Commodities, 22(2).
- library | Referenced against TA-Lib's [HA](https://ta-lib.org/functions/ha.html){:target="_blank"}
- library | Shares similar logic as pandas-ta-classic's [ha](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/candles/ha.py#L25){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the open, high and low prices are adjusted
for dividends in the same way. "Close" uses the candles as traded (split-adjusted).
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The Heikin-Ashi Open, High, Low and Close per date and ticker.

**Notes:**

- The values agree with TA-Lib's HA and pandas-ta-classic's ha on every candle, from the
ticker's own first candle on.
- The first candle's open is the seed (Open + Close) / 2, whose weight halves every
period, so the candles of the first few periods after the Toolkit's start date depend
on where the history starts.
- The Heikin-Ashi prices are averages, not traded prices: an order is filled at the
prices of the actual candles.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

heikin_ashi = toolkit.technicals.get_heikin_ashi()

heikin_ashi.xs("AAPL", level=1, axis="columns").tail()
```

Which returns:

| Date       |    Open |    High |     Low |   Close |
|:-----------|--------:|--------:|--------:|--------:|
| 2025-12-24 | 270.938 | 274.474 | 270.938 | 272.496 |
| 2025-12-26 | 271.717 | 274.414 | 271.717 | 272.996 |
| 2025-12-29 | 272.357 | 273.408 | 271.404 | 272.341 |
| 2025-12-30 | 272.349 | 273.128 | 271.335 | 272.115 |
| 2025-12-31 | 272.232 | 272.73  | 270.807 | 271.641 |

---

## get_williams_fractal
Mark Bill Williams' fractals in every ticker's prices: an up fractal is a high above the highs of the two bars before and the two bars after it, a down fractal a low below their lows.

They mark the swing highs and lows of a market; Williams buys a break above the last up fractal and sells a break below the last down fractal.

A fractal needs the bars after it, so it is only known `right_bars` periods later. It is therefore marked on the bar that confirms it, two periods after the high or low with the defaults, and never on the bar of the high or low itself: the value on a date only uses the prices up to that date, so it can be used in a backtest as it is. The fractal's price is the High (Low) `right_bars` periods before the marked date.

The formula is as follows:

$$
\text{Up Fractal} \;(t) = 1 \;\text{if High} \;(t - \text{right\_bars}) > \text{every other High from}\; t - \text{left\_bars} - \text{right\_bars} \;\text{to}\; t,\;\; \text{else 0}
$$

$$
\text{Down Fractal} \;(t) = 1 \;\text{if Low} \;(t - \text{right\_bars}) < \text{every other Low from}\; t - \text{left\_bars} - \text{right\_bars} \;\text{to}\; t,\;\; \text{else 0}
$$

**Also known as:** Williams Fractal, fractals, swing high, swing low, FRACTAL.

**References:**

- paper | Williams, B.M. (1995). "Trading Chaos: Applying Expert Techniques to Maximize Your Profits." Wiley.
- library | Referenced against TA-Lib's [FRACTAL](https://ta-lib.org/functions/fractal.html){:target="_blank"}
- library | Shares similar logic as finta's [WILLIAMS_FRACTAL](https://github.com/peerchemist/finta/blob/1.3/finta/finta.py#L2205){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the high and low prices are adjusted for
dividends in the same way. "Close" uses the prices as traded (split-adjusted).
- <u>left_bars (int, optional):</u> The bars before the high or low it must exceed. Defaults to 2.
- <u>right_bars (int, optional):</u> The bars after the high or low it must exceed, which is
also the delay before a fractal is confirmed. Defaults to 2.
- <u>signals_only (bool, optional):</u> Whether to return only the periods in which at least one
ticker has a fractal. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The Up Fractal and Down Fractal per date and ticker, 1 on the period that
confirms a fractal and 0 otherwise.

**Notes:**

- The fractals agree with TA-Lib's FRACTAL (swinghigh and swinglow, 100 there), which also marks
the confirming bar. finta's WILLIAMS_FRACTAL marks the bar of the high or low itself,
which uses the prices of the following bars (look-ahead).
- The comparison is strict, as in TA-Lib: a high equal to one of the other highs is no
fractal.
- The first left_bars + right_bars periods of a ticker are empty.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

fractals = toolkit.technicals.get_williams_fractal(signals_only=True)

fractals["Up Fractal"].tail()
```

Which returns:

| Date       |   AAPL |   MSFT |   Benchmark |
|:-----------|-------:|-------:|------------:|
| 2025-12-19 |      0 |      0 |           0 |
| 2025-12-22 |      0 |      1 |           0 |
| 2025-12-26 |      0 |      0 |           0 |
| 2025-12-29 |      1 |      1 |           0 |
| 2025-12-30 |      0 |      0 |           1 |

---

## get_td_sequential
Count Tom DeMark's TD Sequential for every ticker: the TD Setup of nine closes in a row beyond the close four bars earlier, and the TD Countdown to 13 that follows it.

DeMark designed it to find where a trend exhausts itself: a completed buy setup (nine lower closes) and above all a completed buy countdown (13) point to a low, a completed sell setup and countdown to a high.

The rules are DeMark's:

- Price Flip: a buy setup starts on a close below the close four bars earlier right after a close above the close four bars before that one, a sell setup on the reverse.
- TD Buy Setup: from the flip on, every close below the close four bars earlier counts 1 to 9, and a close that is not below breaks it. The setup is complete on its ninth bar; the count then stops until the next flip. The TD Sell Setup counts closes above the close four bars earlier.
- TD Buy Countdown: starts on the bar that completes a buy setup and counts every bar, not necessarily in a row, that closes at or below the low two bars earlier, up to 13. The 13th bar also needs a low at or below the close of the eighth countdown bar, else the countdown waits at 12. The TD Sell Countdown counts closes at or above the high two bars earlier, its 13th bar a high at or above the close of the eighth.
- Cancellation: a buy countdown ends when a sell setup completes (which starts the sell countdown) or when a close rises above the TDST level of its setup, the highest true high (the high, or the previous close when higher) of its nine bars; a sell countdown ends on a completed buy setup or a close below the lowest true low of its setup.

TD Sequential, TD Setup, TD Countdown and TDST are Tom DeMark's names for his indicator and its parts.

**Also known as:** TD Sequential, DeMark Sequential, Tom DeMark, TD Setup, TD Countdown, TDST, TD9, TD13, DeMark 9 13, td_seq.

**References:**

- paper | DeMark, T.R. (1994). "The New Science of Technical Analysis." Wiley.
- paper | Perl, J. (2008). "DeMark Indicators." Bloomberg Press.
- library | Referenced against pandas-ta-classic's [td_seq](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/momentum/td_seq.py#L31){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the high and low prices are adjusted for
dividends in the same way. "Close" uses the prices as traded (split-adjusted).
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The Buy Setup and Sell Setup (1 to 9 on the bars of a setup) and the Buy
Countdown and Sell Countdown (1 to 13 on the bars that count) per date and ticker, 0
otherwise.

**Notes:**

- A new setup in the same direction during a countdown does not restart it: DeMark's
recycling, which compares the size of the two setups, is left out, as are the
"perfection" of a setup and the "intersection" filter of the countdown.
- pandas-ta-classic's td_seq counts every run of closes beyond the close four bars
earlier, also one without a price flip before it, and continues past 9 up to 13; on the
bars of a setup that starts on a flip, its counts 1 to 9 are the same as here.
- The counts carry over from the ticker's own first bar, so the first setups after the
Toolkit's start date depend on where the history starts; the first four bars are empty.
- pandas-ta-classic's td_seq counts the TD Setup only.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

td_sequential = toolkit.technicals.get_td_sequential()

td_sequential.xs("AAPL", level=1, axis="columns").tail()
```

Which returns:

| Date       |   Buy Setup |   Sell Setup |   Buy Countdown |   Sell Countdown |
|:-----------|------------:|-------------:|----------------:|-----------------:|
| 2025-12-24 |           0 |            2 |               0 |                0 |
| 2025-12-26 |           1 |            0 |               0 |                1 |
| 2025-12-29 |           0 |            1 |               0 |                0 |
| 2025-12-30 |           0 |            2 |               0 |                0 |
| 2025-12-31 |           1 |            0 |               0 |                0 |

---

## get_liquidity_sweep
Mark the liquidity sweeps in every ticker's candles: a candle that trades through the lowest low (or highest high) of the previous 15 bars, where stop orders tend to rest, and closes back inside with a long wick.

Traders read it as a stop hunt that has run its course, so a sweep below the lows (bullish) hints at a move up and a sweep above the highs (bearish) at a move down.

The formula is as follows:

$$
\text{Swing Low} = \text{lowest Low of the} \;\text{window} \;\text{bars before the candle},\;\; \text{Swing High} = \text{their highest High}
$$

- Bullish Sweep (1): Low < Swing Low, Close > Swing Low, Close > Open and lower shadow > wick_multiple x real body

- Bearish Sweep (-1): High > Swing High, Close < Swing High, Close < Open and upper shadow > wick_multiple x real body

The real body is &#124;Close - Open&#124;, the lower shadow runs from the bottom of the body to the Low and the upper shadow from the top of the body to the High.

The liquidity sweep (or stop hunt) is a pattern defined by the ICT (Inner Circle Trader) and Smart Money Concepts community, without a primary publication. The measurable form with a swing over the previous 15 bars and a wick longer than 1.5 times the body is pandas-ta-classic's.

**Also known as:** liquidity sweep, liquidity grab, stop hunt, stop run, smart money concepts, SMC, ICT, swing failure, smc_sweep.

**References:**

- library | Referenced against pandas-ta-classic's [smc_sweep](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/momentum/smc_sweep.py#L12){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the open, high and low prices are adjusted
for dividends in the same way. "Close" uses the candles as traded (split-adjusted).
- <u>window (int, optional):</u> The number of previous bars the swing low and high are taken
over. Defaults to 15.
- <u>wick_multiple (float, optional):</u> How many times the real body the wick through the
swing must exceed. Defaults to 1.5.
- <u>signals_only (bool, optional):</u> Whether to return only the periods in which at least one
ticker has a sweep. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The sweeps per date and ticker: 1 (bullish), -1 (bearish) or 0.

**Notes:**

- The values agree with pandas-ta-classic's smc_sweep, also in its first `window` bars, which
are empty.
- Smart Money Concepts traders often take the swing low and high from swing points (see
`get_williams_fractal`) rather than from the extremes of a fixed window.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

sweeps = toolkit.technicals.get_liquidity_sweep(signals_only=True)

sweeps.tail()
```

Which returns:

| Date       |   AAPL |   MSFT |   Benchmark |
|:-----------|-------:|-------:|------------:|
| 2025-10-02 |      0 |     -1 |           0 |
| 2025-10-03 |      0 |      0 |          -1 |
| 2025-10-30 |     -1 |      0 |           0 |
| 2025-11-25 |      0 |      1 |           0 |
| 2025-12-26 |      0 |      0 |          -1 |

---

## get_signals
Turn moving averages, the MACD, the RSI, the Bollinger Bands and new highs and lows into the events traders act on: the period a line is crossed.

The indicators themselves are available as `get_moving_average`, `get_moving_average_convergence_divergence`, `get_relative_strength_index` and `get_bollinger_bands`, and give the same values.

Every signal is 1 on the period a line is crossed upwards, -1 on the period it is crossed downwards and 0 otherwise:

- Moving Average Crossover: the short Simple Moving Average crossing the long one; with the default 50 and 200 periods a golden cross (1) or a death cross (-1).
- MACD Crossover: the MACD line crossing its signal line, the classic trigger of the MACD.
- RSI Overbought: the RSI entering (1) or leaving (-1) the overbought zone above `rsi_overbought`. Leaving it is the classic sell signal.
- RSI Oversold: the RSI leaving (1) or entering (-1) the oversold zone below `rsi_oversold`. Leaving it is the classic buy signal.
- Upper Bollinger Band: the price breaking out above (1) or falling back below (-1) the upper band.
- Lower Bollinger Band: the price recovering above (1) or breaking down below (-1) the lower band.
- New High/Low: a close above every close of the previous `high_low_window` periods (1), a 52-week high with daily prices by default, or below every one of them (-1).

**Also known as:** trading signals, golden cross, death cross, crossovers, breakouts, MACD crossover, RSI signal, 52-week high, new high.

**References:**

- paper | Murphy, J.J. (1999). "Technical Analysis of the Financial Markets." New York Institute of Finance.
- paper | Appel, G. (1979). "The Moving Average Convergence-Divergence Trading Method." Signalert Corp.
- paper | Wilder, J.W. Jr. (1978). "New Concepts in Technical Trading Systems." Trend Research.
- paper | Bollinger, J. (2001). "Bollinger on Bollinger Bands." McGraw-Hill.
- paper | Brock, W., Lakonishok, J., and LeBaron, B. (1992). "Simple Technical Trading Rules and the Stochastic Properties of Stock Returns." The Journal of Finance, 47(5), 1731-1764.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>short_window (int, optional):</u> The window of the short moving average. Defaults to 50.
- <u>long_window (int, optional):</u> The window of the long moving average. Defaults to 200.
- <u>macd_short_window (int, optional):</u> The short window of the MACD. Defaults to 12.
- <u>macd_long_window (int, optional):</u> The long window of the MACD. Defaults to 26.
- <u>macd_signal_window (int, optional):</u> The window of the MACD's signal line. Defaults to 9.
- <u>rsi_window (int, optional):</u> The window of the RSI. Defaults to 14.
- <u>rsi_overbought (float, optional):</u> The RSI above which a price is overbought. Defaults to 70.
- <u>rsi_oversold (float, optional):</u> The RSI below which a price is oversold. Defaults to 30.
- <u>bollinger_window (int, optional):</u> The window of the Bollinger Bands. Defaults to 20.
- <u>bollinger_std_dev (float, optional):</u> The number of standard deviations of the Bollinger
Bands. Defaults to 2.
- <u>high_low_window (int &#124; None, optional):</u> The number of previous periods a new high or
low is measured against. Defaults to None, which uses a year of periods: 252 daily
(and intraday), or 365 for a ticker that also trades on weekends such as a
cryptocurrency, 52 weekly, 12 monthly, 4 quarterly and 1 yearly.
- <u>signals_only (bool, optional):</u> Whether to return only the periods in which at least one
signal occurs for at least one ticker. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The signals per date, with a column per signal and ticker: 1 (crossed
upwards), -1 (crossed downwards) or 0.

**Notes:**

- A signal is empty until its indicator has two values to compare, e.g. 200 periods
for the default long moving average, counted from the ticker's own first price; start
the Toolkit early enough for the signals of interest.
- A crossover is the period the line reaches the other side than the side it was on
last: touching a line and turning back is no signal, while moving through it over two
periods counts on the period the other side is reached.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2020-01-01",
    end_date="2025-12-31",
)

signals = toolkit.technicals.get_signals()

crossovers = signals["Moving Average Crossover"]
crossovers[crossovers.ne(0).any(axis=1)].tail()
```

Which returns:

| Date       |   AAPL |   MSFT |   Benchmark |
|:-----------|-------:|-------:|------------:|
| 2025-04-07 |     -1 |      0 |           0 |
| 2025-04-16 |      0 |      0 |          -1 |
| 2025-06-09 |      0 |      1 |           0 |
| 2025-06-27 |      0 |      0 |           1 |
| 2025-09-15 |      1 |      0 |           0 |

---

## get_indicator_summary
Summarise the history of a technical indicator per ticker in a single row instead of the series itself.

The row holds where the latest value ranks in its own history, the lowest and highest value with their dates, how many periods the indicator spent below or above a threshold, when it last crossed into that zone and how the price did afterwards. This answers questions such as "how oversold is the RSI compared with the last five years, and what happened after the previous times it fell below 30?" without the thousands of daily values behind it.

Each value is ranked against its own history up to that date, so the percentile of a crossing in the past only uses the values known at that time:

$$
\text{Percentile} = \text{share of the values up to and including the date that are at most the value on that date}
$$

$$
\text{Rank} = \text{number of values up to and including the date that are at most the value on that}\; \text{date:} 1 \;\text{is the lowest value so far},\;\; \text{the number of observations the highest}
$$

$$
\text{Forward Return} \;(n \;\text{periods}) = \frac{\operatorname{Price}(t + n)}{\operatorname{Price}(t)} - 1,\;\; \text{from the close of the crossing to the close } n \text{ trading periods later, on the dividend and split adjusted close}
$$

A crossing below `below` is the period the indicator falls below the line, entering the zone, and a crossing above `above` the period it rises above the line (the same crossings as `get_signals`). The average forward return after the crossings is shown next to the average forward return over every period, so the effect of the signal can be read against the drift of the share itself.

**Also known as:** indicator statistics, indicator percentile, oversold history, event study, forward returns after a signal, RSI below 30.

**References:**

- paper | Wilder, J.W. Jr. (1978). "New Concepts in Technical Trading Systems." Trend Research.
- paper | Murphy, J.J. (1999). "Technical Analysis of the Financial Markets." New York Institute of Finance.

**Args:**

- <u>metric (str, optional):</u> The indicator method name, e.g. "get_stochastic_oscillator"
or "get_rate_of_change", with method= among the other parameters for a variant
(e.g. method="connors"). Defaults to "get_relative_strength_index".
- <u>below (float &#124; None, optional):</u> The line the indicator falls below, e.g. 30 for an
oversold RSI. Defaults to None.
- <u>above (float &#124; None, optional):</u> The line the indicator rises above, e.g. 70 for an
overbought RSI. Defaults to None.
- <u>forward_periods (list[int] &#124; int &#124; None, optional):</u> The numbers of trading periods
after each date to measure the return over, e.g. [5, 21, 63] for about a week,
a month and a quarter of daily data. Defaults to None, which measures no
returns.
- <u>show_crossings (bool, optional):</u> Whether to return a row per crossing (ticker and
date) with its zone, the indicator value, its percentile at the time and the
forward returns instead of the summary. Defaults to False.
- <u>column (str &#124; None, optional):</u> The output to use of an indicator with several,
e.g. "Signal Line" of the MACD. Defaults to None, which uses the first output
other than a price, a histogram or a signal line, e.g. "MACD Line".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
**kwargs: Parameters passed to the indicator, e.g. window=14 or period="weekly".
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The summary per ticker: Latest, Latest Date, Percentile, Rank,
Observations, Mean, Minimum, Minimum Date, Maximum and Maximum Date; with
forward_periods the Average n-Period Return; with below (or above) the Periods
Below, Crossings Below, Last Crossing Below and the Average n-Period Return After
Crossing Below. With show_crossings a row per ticker and crossing date.

**Notes:**

- The history is the Toolkit's date range, after the warm-up the indicator needs
(e.g. 14 periods for the RSI), so start early enough for the comparison you are
after.
- The forward returns of the last n periods are not known yet: those crossings are
listed without a return and left out of the averages.
- Crossings close together overlap in their forward returns, so a handful of
crossings says little about the signal in general.
- The returns are measured over the periods of the indicator: trading days by
default, weeks for weekly periods.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["NVDA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-11-01",
    end_date="2026-11-05",
)

toolkit.technicals.get_indicator_summary(
    "get_relative_strength_index", below=30, forward_periods=[5, 21, 63]
).T
```

Which returns:

|                                               | NVDA       |
|:----------------------------------------------|:-----------|
| Latest                                        | 25.3948    |
| Latest Date                                   | 2026-11-05 |
| Percentile                                    | 0.0008     |
| Rank                                          | 1          |
| Observations                                  | 1259       |
| Mean                                          | 54.7452    |
| Minimum                                       | 25.3948    |
| Minimum Date                                  | 2026-11-05 |
| Maximum                                       | 89.1421    |
| Maximum Date                                  | 2021-11-08 |
| Average 5-Period Return                       | 0.0103     |
| Average 21-Period Return                      | 0.044      |
| Average 63-Period Return                      | 0.1495     |
| Periods Below                                 | 12         |
| Crossings Below                               | 6          |
| Last Crossing Below                           | 2026-11-05 |
| Average 5-Period Return After Crossing Below  | 0.0625     |
| Average 21-Period Return After Crossing Below | 0.0313     |
| Average 63-Period Return After Crossing Below | 0.1968     |

---

## get_seasonality
Calculate the seasonality of every ticker's returns: the average return per calendar month or per day of the week.

Monthly returns give the months and daily returns the days of the week, each with the median, the hit rate (the share of positive returns), the t-statistic of the average and the number of observations. Well-known examples are the January effect and the "sell in May" pattern. A pattern needs many years and a t-statistic well above 2 before it says much, and even then it can fade once it is widely traded on.

A monthly return runs from one month's last close to the next, so a final month that is not complete yet (an end date before that month's last business day, as with the default end date of today) is left out rather than averaged as a full month. The Benchmark is included as a ticker, so its seasonality is there to compare with; a Portfolio is left out.

**Also known as:** seasonality, monthly seasonality, day of the week effect, January effect, calendar anomalies.

**References:**

- paper | Heston, S.L. and Sadka, R. (2008). "Seasonality in the Cross-Section of Stock Returns." Journal of Financial Economics, 87(2), 418-445.

**Args:**

- <u>frequency (str, optional):</u> Options are: "month" (per calendar month), "weekday" (per day of the
week). Defaults to "month".
- <u>close_column (str, optional):</u> The name of the column containing the close prices.
Defaults to "Adj Close".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the rounding of the Toolkit.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The Average Return, Median Return, Hit Rate, t-Statistic and
Observations per month or weekday, with a column per statistic and ticker.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2000-01-01",
    end_date="2025-12-31",
)

seasonality = toolkit.technicals.get_seasonality()

seasonality.xs("AAPL", level=1, axis="columns")
```

Which returns:

| Month     |   Average Return |   Median Return |   Hit Rate |   t-Statistic |   Observations |
|:----------|-----------------:|----------------:|-----------:|--------------:|---------------:|
| January   |           0.0239 |          0.0477 |     0.6    |        0.8733 |             25 |
| February  |           0.0139 |          0.0245 |     0.5385 |        0.7962 |             26 |
| March     |           0.0486 |          0.0529 |     0.6538 |        2.6472 |             26 |
| April     |           0.028  |          0.0057 |     0.5769 |        1.5009 |             26 |
| May       |           0.018  |          0.0457 |     0.5769 |        0.7223 |             26 |
| June      |           0.0171 |          0.0096 |     0.5385 |        0.8119 |             26 |
| July      |           0.0523 |          0.0501 |     0.7692 |        2.7965 |             26 |
| August    |           0.0501 |          0.0466 |     0.6538 |        3.2948 |             26 |
| September |          -0.0252 |         -0.0128 |     0.4231 |       -0.8129 |             26 |
| October   |           0.0529 |          0.0616 |     0.7308 |        2.4423 |             26 |
| November  |           0.0306 |          0.0334 |     0.5769 |        1.4177 |             26 |
| December  |          -0.0061 |          0.0112 |     0.5385 |       -0.4179 |             26 |

---

## get_relative_strength
Calculate the relative strength of every ticker against the Benchmark and against the other tickers: which tickers outperform and by how much.

Relative strength investing buys what has been outperforming, the momentum effect that has held across markets and decades.

- Relative Strength: the price divided by the Benchmark's, set to 1 on the first date. It rises while the ticker outperforms the Benchmark.
- Mansfield Relative Strength: the relative strength against its own moving average (of `window` periods, a year by default) minus 1. Above zero the ticker is gaining on the Benchmark.
- Relative Strength Rating: the ticker's performance over the last year, the last quarter weighing most (the 3, 6, 9 and 12-month returns weighted 0.4, 0.2, 0.2 and 0.2), ranked against the other tickers from 1 (weakest) to 99 (strongest), from daily prices. Investor's Business Daily publishes the original rating with a proprietary formula; this weighting is its common public approximation. Tickers with the same score share the highest rank among them, so the rating reads as the share of the other tickers outperformed or matched and tied leaders both rate 99. It needs many tickers to be meaningful, such as the constituents of an index (see `Discovery.get_index_constituents`, whose date argument gives the members on a past date; today's members leave out the companies removed from the index since).

**Also known as:** relative strength, price relative, Mansfield relative strength, RS rating, relative performance.

**References:**

- paper | Jegadeesh, N. and Titman, S. (1993). "Returns to Buying Winners and Selling Losers: Implications for Stock Market Efficiency." The Journal of Finance, 48(1), 65-91.
- paper | Weinstein, S. (1988). "Stan Weinstein's Secrets for Profiting in Bull and Bear Markets." Dow Jones-Irwin.
- paper | O'Neil, W.J. (1988). "How to Make Money in Stocks." McGraw-Hill.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are: "daily" (daily
prices), "weekly" (weekly prices), "monthly" (monthly prices), "quarterly" (quarterly prices),
"yearly" (yearly prices). Defaults to "daily".
- <u>close_column (str, optional):</u> The name of the column containing the close prices.
Defaults to "Adj Close".
- <u>window (int &#124; None, optional):</u> The moving average window of the Mansfield relative
strength, in periods. Defaults to None, which uses a year of periods: 252 daily
(365 for a ticker that also trades on weekends, such as a cryptocurrency), 52 weekly, 12 monthly, 4 quarterly and 1 yearly (a single period, which makes the
measure zero, so pass a longer window for yearly data).
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the rounding of the Toolkit.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The Relative Strength, Mansfield Relative Strength and Relative Strength
Rating per date, with a column per measure and ticker.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "NVDA", "AMZN", "GOOGL"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2022-01-01",
    end_date="2025-12-31",
)

relative_strength = toolkit.technicals.get_relative_strength()

relative_strength["Relative Strength Rating"].tail()
```

Which returns:

| Date       |   AAPL |   MSFT |   NVDA |   AMZN |   GOOGL |
|:-----------|-------:|-------:|-------:|-------:|--------:|
| 2025-12-24 |     50 |      1 |     74 |     26 |      99 |
| 2025-12-26 |     50 |      1 |     74 |     26 |      99 |
| 2025-12-29 |     50 |      1 |     74 |     26 |      99 |
| 2025-12-30 |     50 |      1 |     74 |     26 |      99 |
| 2025-12-31 |     50 |      1 |     74 |     26 |      99 |

---

## collect_volatility_indicators
Collect the volatility indicators of every ticker in one table: how widely the prices move and the bands and channels around them.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>window (int, optional):</u> The window size for calculating indicators.
Defaults to 14. The Bollinger Bands and their %B and BandWidth keep their own
window of 20 periods (with 2 standard deviations), as defined by Bollinger, and
the Supertrend, Chaikin Volatility, acceleration bands, Chande Kroll Stop,
adaptive price zone, aberration bands, Profit Maximizer, market thermometer,
squeeze momentum and Price Bands their own defaults.
- <u>close_column (str, optional):</u> The name of the column containing the close prices.
Defaults to "Adj Close".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: Volatility indicators calculated based on the specified parameters.

**Notes:**

- The method calculates several volatility-based indicators for each asset in the Toolkit instance.
- The Standard Deviation Channel is left out: it is fitted over the whole date range at
once, so its values depend on later prices.
- When growth is requested, the method calculates the growth of the indicator values
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.collect_volatility_indicators().xs("AAPL", level=1, axis="columns")
```

Which returns:

| Date       |   Bollinger Band Upper |   Bollinger Band Middle |   Bollinger Band Lower |   Bollinger %B |   Bollinger BandWidth |   True Range |   Average True Range |   Mass Index |   Supertrend |   Supertrend Trend Direction |   Chandelier Exit Long |   Chandelier Exit Short |   Keltner Channel Upper |   Keltner Channel Middle |   Keltner Channel Lower |   Donchian Channel Upper |   Donchian Channel Middle |   Donchian Channel Lower |   Normalized Average True Range |   Average Day Range |   Chaikin Volatility |   Relative Volatility Index |   Acceleration Band Upper |   Acceleration Band Middle |   Acceleration Band Lower |   Chande Kroll High Stop |   Chande Kroll Low Stop |   Adaptive Price Zone Upper |   Adaptive Price Zone Middle |   Adaptive Price Zone Lower |   Aberration Upper |   Aberration Middle |   Aberration Lower |    PMax |   PMax Trend Direction |   Price Distance |   Market Thermometer |   Market Thermometer Average |   Squeeze Momentum |   Squeeze |
|:-----------|-----------------------:|------------------------:|-----------------------:|---------------:|----------------------:|-------------:|---------------------:|-------------:|-------------:|-----------------------------:|-----------------------:|------------------------:|------------------------:|-------------------------:|------------------------:|-------------------------:|--------------------------:|-------------------------:|--------------------------------:|--------------------:|---------------------:|----------------------------:|--------------------------:|---------------------------:|--------------------------:|-------------------------:|------------------------:|----------------------------:|-----------------------------:|----------------------------:|-------------------:|--------------------:|-------------------:|--------:|-----------------------:|-----------------:|---------------------:|-----------------------------:|-------------------:|----------:|
| 2025-12-17 |                285.548 |                 276     |                266.452 |         0.2327 |                0.0692 |       4.5043 |               4.871  |      24.5798 |      268.465 |                            1 |                272.67  |                 279.347 |                 284.794 |                  275.314 |                 265.833 |                  287.618 |                   279.232 |                  270.846 |                          0.018  |              4.5036 |              -0.1546 |                     49.6227 |                   288.841 |                    276     |                   263.609 |                  282.999 |                 270.062 |                     284.262 |                      275.342 |                     266.422 |            279.563 |             274.669 |            269.775 | 263.457 |                      1 |           6.2482 |               0.6577 |                       1.7931 |             0.179  |         1 |
| 2025-12-18 |                285.211 |                 276.181 |                267.151 |         0.2267 |                0.0654 |       6.6568 |               4.9986 |      24.6224 |      268.465 |                            1 |                272.442 |                 279.575 |                 284.635 |                  274.771 |                 264.907 |                  287.618 |                   279.158 |                  270.697 |                          0.0184 |              4.7648 |              -0.1054 |                     52.2511 |                   288.909 |                    276.181 |                   263.684 |                  282.999 |                 270.955 |                     283.909 |                      274.378 |                     264.847 |            278.441 |             273.429 |            268.418 | 263.457 |                      1 |          13.6624 |               4.6738 |                       2.0436 |            -1.5338 |         1 |
| 2025-12-19 |                284.285 |                 276.55  |                268.816 |         0.2524 |                0.0559 |       4.6837 |               4.9761 |      24.6659 |      268.465 |                            1 |                272.493 |                 279.704 |                 284.312 |                  274.498 |                 264.683 |                  287.618 |                   276.821 |                  266.023 |                          0.0182 |              4.5812 |              -0.036  |                     54.7332 |                   288.375 |                    276.55  |                   264.349 |                  282.999 |                 270.93  |                     283.524 |                      273.768 |                     264.013 |            277.346 |             272.356 |            267.367 | 263.457 |                      1 |           7.8924 |               0.9667 |                       1.95   |            -3.209  |         1 |
| 2025-12-22 |                284.343 |                 276.525 |                268.707 |         0.0846 |                0.0565 |       3.3583 |               4.8605 |      24.609  |      268.465 |                            1 |                272.722 |                 279.644 |                 283.406 |                  273.902 |                 264.397 |                  287.618 |                   276.821 |                  266.023 |                          0.018  |              4.4815 |              -0.0369 |                     51.5807 |                   287.967 |                    276.525 |                   265.009 |                  282.999 |                 270.776 |                     282.464 |                      273.024 |                     263.583 |            276.457 |             271.577 |            266.696 | 263.457 |                      1 |           5.6404 |               0      |                       1.7804 |            -5.0602 |         1 |
| 2025-12-23 |                284.455 |                 276.347 |                268.24  |         0.1958 |                0.0587 |       2.9298 |               4.7226 |      24.5236 |      268.465 |                            1 |                273     |                 279.366 |                 282.71  |                  273.57  |                 264.43  |                  287.618 |                   276.821 |                  266.023 |                          0.0174 |              4.3121 |              -0.0391 |                     54.401  |                   287.422 |                    276.347 |                   265.252 |                  282.999 |                 270.593 |                     281.343 |                      272.509 |                     263.674 |            275.83  |             271.08  |            266.329 | 263.457 |                      1 |           4.4745 |               0.9467 |                       1.7079 |            -6.1264 |         1 |
| 2025-12-24 |                284.438 |                 276.19  |                267.941 |         0.2981 |                0.0597 |       3.2188 |               4.6152 |      24.4118 |      268.465 |                            1 |                273.225 |                 280.416 |                 282.345 |                  273.476 |                 264.606 |                  283.741 |                   274.882 |                  266.023 |                          0.0169 |              4.105  |              -0.037  |                     56.7182 |                   286.983 |                    276.19  |                   265.287 |                  282.999 |                 270.458 |                     280.619 |                      272.348 |                     264.077 |            275.848 |             271.199 |            266.551 | 263.457 |                      1 |           4.9926 |               2.9198 |                       1.8133 |            -6.7609 |         1 |
| 2025-12-26 |                284.387 |                 275.983 |                267.579 |         0.2899 |                0.0609 |       2.5013 |               4.4642 |      24.2185 |      268.465 |                            1 |                273.538 |                 280.103 |                 281.822 |                  273.339 |                 264.856 |                  280.164 |                   273.094 |                  266.023 |                          0.0164 |              4.0637 |              -0.1593 |                     54.2874 |                   286.737 |                    275.983 |                   265.137 |                  282.851 |                 270.265 |                     279.904 |                      272.297 |                     264.69  |            276.293 |             271.788 |            267.282 | 263.457 |                      1 |           4.594  |               0      |                       1.6556 |            -7.2886 |         1 |
| 2025-12-29 |                284.195 |                 275.729 |                267.264 |         0.3276 |                0.0614 |       2.003  |               4.2884 |      23.8779 |      268.465 |                            1 |                273.905 |                 279.736 |                 281.304 |                  273.268 |                 265.233 |                  279.177 |                   272.6   |                  266.023 |                          0.0157 |              3.9562 |              -0.1596 |                     55.4689 |                   286.405 |                    275.729 |                   265.055 |                  282.851 |                 270.041 |                     279.204 |                      272.345 |                     265.486 |            276.279 |             271.941 |            267.602 | 263.457 |                      1 |           3.6472 |               0.5082 |                       1.5559 |            -7.4802 |         1 |
| 2025-12-30 |                283.299 |                 275.23  |                267.162 |         0.308  |                0.0586 |       1.7937 |               4.1102 |      23.5003 |      268.465 |                            1 |                274.284 |                 279.357 |                 280.707 |                  273.117 |                 265.526 |                  279.177 |                   272.6   |                  266.023 |                          0.0151 |              3.863  |              -0.3267 |                     54.0398 |                   285.385 |                    275.23  |                   265.399 |                  279.001 |                 269.818 |                     278.457 |                      272.336 |                     266.215 |            276.381 |             272.212 |            268.043 | 263.457 |                      1 |           4.2652 |               0.0698 |                       1.4266 |            -7.2914 |         0 |
| 2025-12-31 |                281.366 |                 274.516 |                267.666 |         0.2372 |                0.0499 |       1.9233 |               3.954  |      23.1557 |      268.465 |                            1 |                274.628 |                 279.013 |                 280.039 |                  272.823 |                 265.607 |                  279.177 |                   272.6   |                  266.023 |                          0.0146 |              3.7647 |              -0.3494 |                     52.7332 |                   284.415 |                    274.516 |                   265.137 |                  275.232 |                 269.631 |                     277.662 |                      272.143 |                     266.623 |            276.421 |             272.402 |            268.383 | 263.457 |                      1 |           2.6707 |               0.5282 |                       1.3485 |            -6.9011 |         1 |

---

## get_bollinger_bands
Calculate the Bollinger Bands or the Price Bands: bands around a moving average, a number of standard deviations wide, which show how high or low the price is relative to its recent volatility.

Bollinger Bands are a volatility indicator that consists of three lines: an upper band, a middle band (simple moving average), and a lower band. The upper and lower bands are calculated as the moving average plus and minus a specified number of standard deviations, respectively.

Price Bands are a variant of the Bollinger Bands whose width comes from the distance between the moving average and a fast moving average of the price, rather than from the distance between the price and the moving average. The fast average filters out the noise of single periods, so a spike widens the bands less than it widens the Bollinger Bands, and the bands react to sustained moves away from the average instead.

The formula for the Bollinger Bands is as follows:

$$
\text{Middle Band} = \operatorname{SMA}(\text{Close},\; \text{Window}),\;\; \text{or another moving average with moving\_average}
$$

$$
\text{Upper Band} = \text{Middle Band} + (\text{Num Std Dev} \cdot \text{Std Dev})
$$

$$
\text{Lower Band} = \text{Middle Band} - (\text{Num Std Dev} \cdot \text{Std Dev})
$$

The formula for the Price Bands is as follows:

$$
\text{Middle Band} = \operatorname{SMA}(\text{Close},\; \text{window}),\;\; \text{or another moving average with moving\_average}
$$

$$
\text{Deviation} = \text{Middle Band} - \operatorname{SMA}(\text{Close},\; \text{short\_window})
$$

$$
\text{Width} = \text{Population Standard Deviation}(\text{Deviation},\; \text{window})
$$

$$
\text{Upper Band} = \text{Middle Band} + \text{num\_std\_dev} \cdot \text{Width}
$$

$$
\text{Lower Band} = \text{Middle Band} - \text{num\_std\_dev} \cdot \text{Width}
$$

The standard deviation is the *population* standard deviation (dividing by n), as Bollinger himself specifies and as TA-Lib and StockCharts both define it, not pandas' default sample standard deviation.

The band width tracks volatility: bands that narrow sharply (a squeeze) often precede a larger move, without saying in which direction. A close at or beyond a band is not a sell or buy signal by itself, since prices can walk along a band in a trend. The defaults are Bollinger's own setting, a 20-period average with 2 standard deviations, as on most charting platforms. The Price Bands are read the same way, but since their width follows the smoothed price, they are narrower than the Bollinger Bands of the same window and a close outside them is more common.

**Also known as:** Bollinger Bands, BB, volatility bands, price channels, PBands, price bands, smoothed Bollinger Bands.

**References:**

- paper | Bollinger, J. (2001). "Bollinger on Bollinger Bands." McGraw-Hill.
- paper | The Price Bands are defined by Brian G. Peterson in TTR's PBands, after the bands of Bollinger (2001), and referenced against TTR's PBands ([https://cran.r-project.org/package=TTR](https://cran.r-project.org/package=TTR){:target="_blank"}).
- library | Referenced against TA-Lib's [BBANDS](https://ta-lib.org/functions/bbands.html){:target="_blank"}
- library | Referenced against TTR (R)'s [PBands](https://github.com/joshuaulrich/TTR/blob/v0.24.4/R/priceBands.R#L68){:target="_blank"} (Price Bands)
- library | Shares similar logic as pandas-ta-classic's [bbands](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/volatility/bbands.py#L48){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int, optional):</u> Number of periods for moving average calculation.
The number of periods (time intervals) over which to calculate the moving average
and the standard deviation. Defaults to 20, as in TTR's PBands.
- <u>num_std_dev (float, optional):</u> Number of standard deviations for the bands.
Defaults to 2.
- <u>moving_average (str, optional):</u> The moving average of the middle band (and, with
method="price_bands", of the fast average), one of the window-only methods of
`get_moving_average`. Options are: "simple" (Simple Moving Average), "exponential" (Exponential
Moving Average), "double_exponential" (Double Exponential Moving Average),
"triple_exponential" (Triple Exponential Moving Average), "zero_lag" (Zero Lag Exponential
Moving Average), "wilder" (Wilder's Moving Average), "triangular" (Triangular Moving Average),
"weighted" (Weighted Moving Average), "hull" (Hull Moving Average), "sine" (Sine Weighted Moving
Average), "fibonacci" (Fibonacci Weighted Moving Average), "pascal" (Pascal Weighted Moving
Average). Defaults to "simple", Bollinger's own.
- <u>short_window (int, optional):</u> The number of periods of the fast moving average, with
method="price_bands" only. Defaults to 2.
- <u>method (str, optional):</u> The variant of the bands. Options are: "standard" (the Bollinger Bands),
"price_bands" (the Price Bands, whose width comes from the fast moving average). Defaults to
"standard".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the bands.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame:
The Close and the Bollinger Bands or Price Bands (upper, middle, lower), in price units.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates the
Bollinger Bands or Price Bands for each asset in the Toolkit instance.
- The bands agree with TA-Lib's BBANDS with a simple moving average, and with the exponential,
weighted, double exponential, triple exponential and triangular averages its moving average
types 1 to 5. The standard deviation stays the one around the simple average of the
window, as in TA-Lib, whatever the middle band.
- The standard deviation of the Price Bands is the population one (dividing by `window`), as
in TTR's PBands. The Price Bands start on period 2 * `window` — 2.
- TTR's PBands can also centre the bands (`centered=TRUE`), which adds the moving average
of the deviation divided by the width to the middle band. That adds a number of standard
deviations to a price, so the shift does not scale with the price, and the Toolkit
leaves it out.
- When growth is requested, the method calculates the growth of the bands
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["USDJPY"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_bollinger_bands().xs("USDJPY", level=1, axis="columns").tail(5)
```

Which returns:

| Date       |   Close |   Lower Band |   Middle Band |   Upper Band |
|:-----------|--------:|-------------:|--------------:|-------------:|
| 2025-12-26 | 156.5   |      154.463 |       155.975 |      157.486 |
| 2025-12-28 | 156.324 |      154.582 |       156.038 |      157.495 |
| 2025-12-29 | 156.031 |      154.652 |       156.073 |      157.494 |
| 2025-12-30 | 156.329 |      154.744 |       156.124 |      157.504 |
| 2025-12-31 | 156.852 |      154.759 |       156.171 |      157.582 |

---

## get_bollinger_percent_b_and_bandwidth
Calculate the Bollinger %B and BandWidth: where the close lies within the Bollinger Bands and how wide the bands are, which show overbought and oversold levels and squeezes of volatility.

Bollinger (2001, "Bollinger on Bollinger Bands") derived two indicators from his bands. %B places the close within the bands: 0 is on the lower band, 0.5 on the middle band and 1 on the upper band, with values below 0 or above 1 for a close outside the bands. BandWidth is the distance between the bands relative to the middle band, a measure of volatility that can be compared across securities and over time.

The formula is as follows:

$$
\text{Middle Band} = \operatorname{SMA}(\text{Close},\; \text{window})
$$

$$
\text{Upper Band} = \text{Middle Band} + (\text{num\_std\_dev} \cdot \text{Std Dev}),\;\; \text{Lower Band} = \text{Middle Band} - (\text{num\_std\_dev} \cdot \text{Std Dev})
$$

$$
\%B = \frac{\text{Close} - \text{Lower Band}}{\text{Upper Band} - \text{Lower Band}}
$$

$$
\text{BandWidth} = \frac{\text{Upper Band} - \text{Lower Band}}{\text{Middle Band}}
$$

The bands are those of get_bollinger_bands, with the *population* standard deviation (dividing by n) that Bollinger specifies and TA-Lib and StockCharts implement, and the defaults are Bollinger's own 20 periods and 2 standard deviations. Both results are decimals: a BandWidth of 0.10 means bands 10% of the middle band apart (StockCharts multiplies it by 100). A BandWidth at a six-month low marks what Bollinger calls the Squeeze, which often precedes a larger move without saying in which direction; %B above 1 or below 0 shows a close outside the bands, which in a trend can last for weeks.

**Also known as:** Percent B, %b, Bollinger Band Width, BBW, Bollinger Squeeze.

**References:**

- library | Referenced against TA-Lib's [PERCENTB](https://ta-lib.org/functions/percentb.html){:target="_blank"}
- library | Referenced against TA-Lib's [BBW](https://ta-lib.org/functions/bbw.html){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int, optional):</u> Number of periods of the moving average and standard deviation.
Defaults to 20.
- <u>num_std_dev (float, optional):</u> Number of standard deviations for the bands.
Defaults to 2.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of %B and BandWidth.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: %B and BandWidth values, both decimals.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
%B and BandWidth for each asset in the Toolkit instance.
- A window of identical prices gives bands without width, which leaves %B missing and
BandWidth at 0.
- With a simple moving average, %B agrees with TA-Lib's PERCENTB and BandWidth
agrees with TA-Lib's BBW divided by 100, since TA-Lib's BBW is in percent.
- When growth is requested, the method calculates the growth of %B and BandWidth
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2024-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_bollinger_percent_b_and_bandwidth().xs("AAPL", level=1, axis="columns").tail(5)
```

Which returns:

| Date       |     %B |   BandWidth |
|:-----------|-------:|------------:|
| 2025-12-24 | 0.2981 |      0.0597 |
| 2025-12-26 | 0.2899 |      0.0609 |
| 2025-12-29 | 0.3276 |      0.0614 |
| 2025-12-30 | 0.308  |      0.0586 |
| 2025-12-31 | 0.2372 |      0.0499 |

---

## get_true_range
Calculate the True Range (TR): the range of a period including any gap from the previous close, the basic measure of how far the price moved.

The True Range (TR) is a measure of market volatility that considers the differences between the high and low prices and the previous closing price. It provides insights into the price movement of an asset.

The formula is as follows:

$$
\text{TR} = \max(\text{high} - \text{low},\; \operatorname{abs}(\text{high} - \text{previous\_close}),\; \operatorname{abs}(\text{low} - \text{previous\_close}))
$$

**Also known as:** TR, true range.

**References:**

- paper | Wilder, J.W. Jr. (1978). "New Concepts in Technical Trading Systems." Trend Research.
- library | Referenced against TA-Lib's [TRANGE](https://ta-lib.org/functions/trange.html){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the open, high and low prices are adjusted
for dividends in the same way.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the True Range.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: True Range values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates the
True Range for each asset in the Toolkit instance.
- The True Range agrees with TA-Lib's TRANGE from the second period on. The first period, which
has no previous close, is High — Low here and empty in TA-Lib.
- When growth is requested, the method calculates the growth of the True Range
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["NGUSD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_true_range().tail(5)
```

Which returns:

| Date       |   NGUSD |   Benchmark |
|:-----------|--------:|------------:|
| 2025-12-26 |   0.52  |      2.3715 |
| 2025-12-28 |   0.475 |    nan      |
| 2025-12-29 |   0.242 |      4.2071 |
| 2025-12-30 |   0.26  |      1.9647 |
| 2025-12-31 |   0.304 |      5.6062 |

---

## get_average_true_range
Calculate the Average True Range (ATR), normalised by the close (NATR) or as the Average Day Range (ADR): the average range of the periods, a measure of how much the price moves.

The Average True Range (ATR) is a technical indicator that measures the volatility of an asset's price movements over a specified number of periods. It provides insights into the potential price range of an asset, which can help traders and investors make more informed decisions. The Normalized Average True Range is the Average True Range divided by the close, so the average range is a share of the price: unlike the ATR, which is in price units, it compares across stocks with different prices and over periods in which the price changed a lot. The Average Day Range is the simple average of the High - Low range: unlike the Average True Range it leaves out the gaps between periods, so it measures how far the price moves within a period, a basis for intraday targets and stops (for example a stop half an ADR away).

The formula is as follows, per method:

$$
\text{Average True Range:}\;\; \text{TR} = \max(\text{high} - \text{low},\; \operatorname{abs}(\text{high} - \text{previous\_close}),\; \operatorname{abs}(\text{low} - \text{previous\_close}))\;\;\text{and}\;\; \text{ATR} = \text{Wilder's Smoothed Moving Average of TR over} \;\text{window} \;\text{periods}
$$

$$
\text{Normalized Average True Range:}\;\; \text{NATR} = \frac{\operatorname{ATR}(\text{window})}{\text{Close}},\;\; \text{where the ATR uses Wilder's smoothing};\;\; \text{0.02 is an average range of 2\% of the close}
$$

$$
\text{Average Day Range:}\;\; \text{ADR} = \operatorname{SMA}(\text{High} - \text{Low},\; \text{window})
$$

The ATR is in price units, which makes it the common basis for stop distances (for example two ATRs below the entry) and for sizing positions to equal risk. For the same reason it cannot be compared across stocks or over long periods in which the price changed a lot; divide it by the price for a percentage volatility. It measures how far price moves, not in which direction.

**Also known as:** ATR, volatility indicator, NATR, normalized average true range, ATR percent, ATRP, ADR, average day range, average daily range, average high-low range.

See `volatility_model.get_average_true_range` for the full formula; Wilder's smoothing constant (1/window) is slower than a standard EMA's (2/(window+1)) of the same window.

The first period has no previous close, so its True Range is High - Low and the first ATR is the average of the first `window` True Ranges (the StockCharts convention; TA-Lib starts one period later).

**References:**

- paper | Wilder, J.W. Jr. (1978). "New Concepts in Technical Trading Systems." Trend Research.
- paper | Forman, J. (2006). "Cross-Market Evaluations With Normalized Average True Range." Technical Analysis of Stocks & Commodities, 24(5).
- paper | Keltner, C.W. (1960). "How to Make Money in Commodities." The Keltner Statistical Service, whose channel is the average day range around the typical price.
- library | Referenced against TA-Lib's [ATR](https://ta-lib.org/functions/atr.html){:target="_blank"}
- library | Referenced against TA-Lib's [NATR](https://ta-lib.org/functions/natr.html){:target="_blank"}
- library | Referenced against TA-Lib's [ADR](https://ta-lib.org/functions/adr.html){:target="_blank"}
- library | Shares similar logic as pandas-ta-classic's [natr](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/volatility/natr.py#L20){:target="_blank"}
- library | Shares similar logic as Tulip Indicators' [natr](https://tulipindicators.org/natr){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the open, high and low prices are adjusted
for dividends in the same way.
- <u>window (int, optional):</u> The number of periods over which to calculate the Average
True Range, or of the average of the range with method="day_range". Defaults to 14,
as in TA-Lib.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the rounding set on the Toolkit (4 unless set
otherwise).
- <u>growth (bool, optional):</u> Whether to return the growth of the ATR instead of its
level. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>method (str, optional):</u> Options are: "standard" (the ATR), "normalized" (the NATR, a decimal of the
close), "day_range" (the Average Day Range). Defaults to "standard".
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: ATR values per ticker in price units, or their growth when growth is requested.
For the NATR the values are decimals and for the ADR price units.

**Notes:**

- ATR values are typically used to assess the volatility and potential price movement of an asset.
- A higher ATR value indicates higher volatility, while a lower ATR value suggests lower volatility.
- Because the True Range starts on the first period, the ATR starts one period before
TA-Lib's ATR and differs from it until the two converge (within 0.01% after about 80
periods with the default window).
- Normalized Average True Range: the ATR is the one above (the StockCharts seeding), so the NATR starts one
period before TA-Lib's NATR and equals it, divided by 100, once the seeds have converged
(within 1e-8 after about 150 periods with the default window).
- Average Day Range: equals TA-Lib's ADR.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["CLUSD", "NGUSD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_average_true_range().tail(5)
```

Which returns:

| Date       |   CLUSD |   NGUSD |   Benchmark |
|:-----------|--------:|--------:|------------:|
| 2025-12-26 |  1.2031 |  0.304  |      6.4283 |
| 2025-12-28 |  1.1614 |  0.3162 |    nan      |
| 2025-12-29 |  1.1778 |  0.3109 |      6.2696 |
| 2025-12-30 |  1.1558 |  0.3073 |      5.9621 |
| 2025-12-31 |  1.1697 |  0.3071 |      5.9367 |

---

## get_mass_index
Calculate the Mass Index: the sum of the ratios of an exponential moving average of the high-low range to its own average, which signals a reversal when the range widens and then narrows.

The Mass Index, developed by Donald Dorsey, looks for reversals in the width of the trading range rather than in price. It divides an EMA of the High - Low range by an EMA of that EMA, a ratio above 1 while the range widens and below 1 while it narrows, and sums the ratio over `sum_window` periods.

The formula is as follows:

$$
\text{Single EMA} = \operatorname{EMA}(\text{High} - \text{Low},\; \text{ema\_window})
$$

$$
\text{Double EMA} = \operatorname{EMA}(\text{Single EMA},\; \text{ema\_window})
$$

$$
\text{Mass Index} = \operatorname{Sum}\left(\frac{\text{Single EMA}}{\text{Double EMA}},\; \sum_{window}\right)
$$

With the default windows a range that neither widens nor narrows gives a Mass Index of 25. Dorsey's "reversal bulge" is the index rising above 27 and then falling back below 26.5, after which the current trend is expected to reverse. The index does not say in which direction, so it is read together with a trend indicator such as a moving average. The ratio has no unit, so the level can be compared across stocks.

**Also known as:** Mass Index, MI. See `volatility_model.get_mass_index` for the references.

**References:**

- paper | Dorsey, D. (1992). "The Mass Index." Technical Analysis of Stocks & Commodities, 10(6), 265-267.
- library | Referenced against TA-Lib's [MASSI](https://ta-lib.org/functions/massi.html){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The close the high and low are taken on the basis of.
Defaults to "Adj Close", in which case the high and low prices are adjusted
for dividends in the same way.
- <u>ema_window (int, optional):</u> The number of periods of the single and double EMA.
Defaults to 9, as defined by Dorsey.
- <u>sum_window (int, optional):</u> The number of periods over which the EMA ratio is summed.
Defaults to 25, as defined by Dorsey.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: Mass Index values.

**Notes:**

- Both EMAs are seeded with the simple average of their first values, as in TA-Lib and on
StockCharts, so the first Mass Index is on period 2 × (`ema_window` — 1) + `sum_window`,
the 41st with the default windows. The Mass Index agrees with TA-Lib's MASSI.
- When growth is requested, the method calculates the growth of the indicator values
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AMZN", "GOOGL"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_mass_index().tail(5)
```

Which returns:

| Date       |    AMZN |   GOOGL |   Benchmark |
|:-----------|--------:|--------:|------------:|
| 2025-12-24 | 23.5078 | 24.9252 |     24.0591 |
| 2025-12-26 | 23.285  | 24.4336 |     23.7267 |
| 2025-12-29 | 22.9215 | 23.8576 |     23.1418 |
| 2025-12-30 | 22.6104 | 23.4152 |     22.5802 |
| 2025-12-31 | 22.4079 | 23.0341 |     22.2524 |

---

## get_supertrend
Calculate the Supertrend or the Profit Maximizer: a trailing stop that shows the direction of the trend and flips when it is crossed.

The stop is a multiple of the Average True Range away from the price, or for the Profit Maximizer from its moving average.

The Supertrend indicator plots a single trailing line that flips between sitting below price (in an uptrend) and above price (in a downtrend). The line is built from two bands offset from the median price ((High + Low) / 2) by a multiple of the Average True Range, which are then "ratcheted" period over period - each band can only move in the direction that tightens around price - so that the active band only flips to the other side once the closing price actually crosses it. This makes Supertrend both a trend filter (the flip direction signals a trend change) and a trailing stop-loss level.

The Profit Maximizer applies the Supertrend's trailing logic to a moving average instead of the price: two stops a multiple of the Average True Range below and above an Exponential Moving Average of the median price, each of which only tightens while the average stays on its side. The trend turns down when the average falls below the long stop and up when it rises above the short stop, and PMax is the active stop. Because the average is smoother than the price, PMax flips less often than the Supertrend.

The formula is as follows, per method:

"standard":

$$
\text{Basic Upper Band} = \frac{\text{High} + \text{Low}}{2} + \text{multiplier} \cdot \operatorname{ATR}(\text{window})
$$

$$
\text{Basic Lower Band} = \frac{\text{High} + \text{Low}}{2} - \text{multiplier} \cdot \operatorname{ATR}(\text{window})
$$

$$
\text{Final Upper Band}(t) = \text{Basic Upper Band}(t) \;\text{if Basic Upper Band}(t) < \text{Final Upper Band}(t-1) \;\text{or Close}(t-1) > \text{Final Upper Band}(t-1),\;\; \text{else Final Upper Band(t-1)}
$$

$$
\text{Final Lower Band}(t) = \text{Basic Lower Band}(t) \;\text{if Basic Lower Band}(t) > \text{Final Lower Band}(t-1) \;\text{or Close}(t-1) < \text{Final Lower Band}(t-1),\;\; \text{else Final Lower Band(t-1)}
$$

$$
\text{While in an uptrend},\;\; \text{Supertrend} = \text{Final Lower Band},\;\; \text{until Close crosses below it},\;\; \text{at which point the trend flips to a downtrend and Supertrend} = \text{Final Upper Band} \;(\text{and vice versa})
$$

"profit_maximizer":

$$
\text{Average} = \operatorname{EMA}\left(\frac{\text{High} + \text{Low}}{2},\; \text{window}\right)
$$

$$
\text{Long Stop} = \text{Average} - \text{multiplier} \cdot \operatorname{ATR}(\text{atr\_window}),\;\; \text{never lowered while the Average stays above the previous Long Stop}
$$

$$
\text{Short Stop} = \text{Average} + \text{multiplier} \cdot \operatorname{ATR}(\text{atr\_window}),\;\; \text{never raised while the Average stays below the previous Short Stop}
$$

$$
\text{PMax} = \text{Long Stop in an uptrend and Short Stop in a downtrend}
$$

**Also known as:** Supertrend, SuperTrend, PMax, Profit Maximizer.

**References:**

- paper | Ozbilgic, K. (2020). "Profit Maximizer - PMax." TradingView script.
- library | Referenced against TA-Lib's [SUPERTREND](https://ta-lib.org/functions/supertrend.html){:target="_blank"}
- library | Shares similar logic as pandas-ta-classic's [pmax](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/trend/pmax.py#L51){:target="_blank"} (Profit Maximizer)

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the open, high and low prices are adjusted
for dividends in the same way.
- <u>window (int, optional):</u> Number of periods for the underlying Average True Range
calculation, and with method="profit_maximizer" of the EMA of the median price.
Defaults to 10, as defined by Ozbilgic for the Profit Maximizer.
- <u>multiplier (float, optional):</u> Multiplier applied to the Average True Range to
determine how far the bands (or the stops of the Profit Maximizer) sit from the median
price (or its average). Defaults to 3.0.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Supertrend and
Trend Direction values. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>method (str, optional):</u> Options are: "standard" (the Supertrend), "profit_maximizer" (the Profit
Maximizer, PMax). Defaults to "standard".
- <u>atr_window (int, optional):</u> The number of periods of the Average True Range of the
Profit Maximizer. Only used when method="profit_maximizer". Defaults to 10, as
defined by Ozbilgic.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame:
Supertrend (the trailing indicator line) and Trend Direction (1 for an uptrend
and -1 for a downtrend) values, or for the Profit Maximizer PMax (the active
stop, in price units) and Trend Direction.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the Supertrend for each asset in the Toolkit instance.
- There is no academic journal citation for Supertrend. Like the Parabolic SAR, it is
a practitioner-developed trailing-stop/trend indicator rather than one derived from
a published financial paper.
- The trend is initialized as an uptrend on the first available period, since there
is no prior period to determine the starting direction from.
- The ATR starts one period before TA-Lib's (see `get_average_true_range`), so the
Supertrend starts one period before TA-Lib's SUPERTREND and differs from it until the two
converge (within 0.01% after about 40 periods with the defaults). The Trend Direction
agrees with TA-Lib's `trend` from TA-Lib's first value.
- Profit Maximizer: this follows Ozbilgic's script (EMA of the median price, Wilder's ATR,
starting in an uptrend). pandas-ta-classic's pmax averages the close and turns the trend on
the close instead of the average, so it differs by design.
- When growth is requested, the method calculates the growth of the Supertrend and
Trend Direction values over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["SHOP"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_supertrend().xs("SHOP", level=1, axis="columns").tail(5)
```

Which returns:

| Date       |   Supertrend |   Trend Direction |
|:-----------|-------------:|------------------:|
| 2025-12-24 |      150.646 |                 1 |
| 2025-12-26 |      151.942 |                 1 |
| 2025-12-29 |      152.113 |                 1 |
| 2025-12-30 |      152.113 |                 1 |
| 2025-12-31 |      152.113 |                 1 |

---

## get_chandelier_exit
Calculate the Chandelier Exit: a trailing stop a multiple of the Average True Range below the highest high (or above the lowest low), which keeps a trade open while the trend lasts.

The Chandelier Exit, developed by Chuck Le Beau, is a trailing stop set a multiple of the Average True Range away from the most extreme price of the last `window` periods: the long exit "hangs" below the highest high like a chandelier from a ceiling, and the short exit sits above the lowest low.

The formula is as follows:

$$
\text{Long Exit} = \text{Highest High}(\text{window}) - \text{multiplier} \cdot \operatorname{ATR}(\text{window})
$$

$$
\text{Short Exit} = \text{Lowest Low}(\text{window}) + \text{multiplier} \cdot \operatorname{ATR}(\text{window})
$$

A long position is closed when the price closes below the long exit, and a short position when it closes above the short exit. Because the distance is in ATRs, the stop is wider in volatile markets and tighter in quiet ones. The stop moves with both the highest high and the ATR, so it can fall while the high holds when volatility rises. The exits are in price units, so they are compared with the stock's own price rather than across stocks.

**Also known as:** Chandelier Exit, Chandelier Stop, CE.

**References:**

- paper | Le Beau, C. & Lucas, D.W. (1992). "Technical Traders Guide to Computer Analysis of the Futures Market." Business One Irwin.
- paper | Elder, A. (2002). "Come Into My Trading Room." John Wiley & Sons, which popularised the exit.
- library | Shares similar logic as TA-Lib's [CE](https://ta-lib.org/functions/ce.html){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the open, high and low prices are adjusted
for dividends in the same way.
- <u>window (int, optional):</u> The number of periods of the highest high, the lowest low and the
Average True Range. Defaults to 22, about a month of trading days, as defined by Le Beau.
- <u>multiplier (float, optional):</u> The number of Average True Ranges the exits sit from the
highest high and the lowest low. Defaults to 3.0, as defined by Le Beau.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Long Exit and Short Exit.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: The Long Exit and Short Exit, in price units.

**Notes:**

- The Average True Range is that of `get_average_true_range`: Wilder's smoothing of the True
Range, with the first True Range High — Low and the first ATR the average of the first
`window` True Ranges (the StockCharts convention), so the exits start on the `window`-th
period. The highest high and the lowest low include the current period.
- Because the ATR is seeded as on StockCharts, the first exits differ from those built on
TA-Lib's ATR, which starts the True Range on the second period, until the two converge
(within 0.01% after about 80 periods with the defaults).
- When growth is requested, the method calculates the growth of the Long Exit and Short Exit
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_chandelier_exit().xs("TSLA", level=1, axis="columns").tail(5)
```

Which returns:

| Date       |   Long Exit |   Short Exit |
|:-----------|------------:|-------------:|
| 2025-12-24 |     444.423 |      455.497 |
| 2025-12-26 |     444.814 |      459.966 |
| 2025-12-29 |     445.062 |      470.658 |
| 2025-12-30 |     446.239 |      474.711 |
| 2025-12-31 |     447.641 |      473.309 |

---

## get_keltner_channels
Calculate the Keltner Channels or the Aberration bands: bands a multiple of the Average True Range above and below an average of the price, which show breakouts and overbought and oversold levels.

The Keltner Channels consist of three lines: a middle line, the Exponential Moving Average (EMA) of the closing prices, and an upper and a lower line a multiple of the Average True Range (ATR) above and below it.

The formula is as follows:

$$
\text{Middle Line} = \operatorname{EMA}(\text{Close},\; \text{window})
$$

$$
\text{Upper Line} = \text{Middle Line} + \text{multiplier} \cdot \operatorname{ATR}(\text{atr\_window})
$$

$$
\text{Lower Line} = \text{Middle Line} - \text{multiplier} \cdot \operatorname{ATR}(\text{atr\_window}),\;\; \text{where the ATR uses Wilder's smoothing}
$$

Keltner's original channel is a simple average of the typical price with the average High - Low range on either side.

- Middle Line = SMA((High + Low + Close) / 3, window)
- Upper Line = Middle Line + multiplier * SMA(High - Low, window)
- Lower Line = Middle Line - multiplier * SMA(High - Low, window)

The Aberration bands place one Average True Range above and below a short simple average of the typical price. They come from Keith Fitschen's Aberration breakout system, which buys a close above the upper band and sells a close below the lower band.

- Middle Band = SMA((High + Low + Close) / 3, window)
- Upper Band = Middle Band + ATR(atr_window)
- Lower Band = Middle Band - ATR(atr_window)

**Also known as:** Keltner Channels, KC, ATR-based bands, volatility channels, ABER, Aberration, Aberration bands.

**References:**

- paper | Keltner, C.W. (1960). "How to Make Money in Commodities." The Keltner Statistical Service.
- paper | Fitschen, K. (2013). "Building Reliable Trading Systems." John Wiley & Sons, on the Aberration system (1993), to which the Aberration bands are attributed; no definitive source of the formula exists.
- library | Referenced against TA-Lib's [KC](https://ta-lib.org/functions/kc.html){:target="_blank"}
- library | Referenced against ta's [KeltnerChannel](https://github.com/bukosabino/ta/blob/0.11.0/ta/volatility.py#L183){:target="_blank"}
- library | Referenced against pandas-ta-classic's [aberration](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/volatility/aberration.py#L14){:target="_blank"} (Aberration)

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the open, high and low prices are adjusted
for dividends in the same way.
- <u>window (int &#124; None, optional):</u> Number of periods for the Exponential Moving Average (the
middle line), or of the simple average of the typical price ("original" and
"aberration"). Defaults to None, which uses 20, as on StockCharts, and 5 for
"aberration", as in pandas-ta-classic.
- <u>atr_window (int &#124; None, optional):</u> Number of periods for ATR calculation. Not used by
"original". Defaults to None, which uses 10, as on StockCharts, and 15 for
"aberration", as in pandas-ta-classic.
- <u>multiplier (float, optional):</u> Multiplier for ATR (or, for the original channel, the
average range) to determine channel width. Defaults to 2; Keltner's original channel
uses 1. Not used by "aberration", whose bands sit one ATR away.
- <u>method (str, optional):</u> The channels. Options are: "exponential" (the EMA of the close with ATR
bands, as StockCharts), "original" (Keltner's simple average of the typical price with average
range bands), "aberration" (the Aberration bands). Defaults to "exponential".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the channels.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: Keltner Channels ("Upper Line", "Middle Line" and "Lower
Line"), or for the Aberration bands the "Upper Band", "Middle Band" and "Lower Band", in
price units.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates Keltner Channels
for each asset in the Toolkit instance.
- The middle line is the EMA of the close, as on StockCharts. TA-Lib's KC takes the EMA of
the typical price ((High + Low + Close) / 3) and starts its ATR one period later, so the
channels differ throughout (by about 0.3% on daily data).
- The original channel uses `window` for both averages (Keltner used 10 days with one
average range, a multiplier of 1) and no ATR, so `atr_window` does not apply. With
a multiplier of 1 it agrees with ta's KeltnerChannel in its original version.
- Aberration bands: the ATR is that of `get_average_true_range`; pandas-ta-classic seeds its ATR
one period later and its bands equal these once the seeds have converged.
- When growth is requested, the method calculates the growth of the channels over the given lag.
- ta's KeltnerChannel defaults to Keltner's original channel.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["^GDAXI"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_keltner_channels().xs("^GDAXI", level=1, axis="columns").tail(5)
```

Which returns:

| Date       |   Lower Line |   Middle Line |   Upper Line |
|:-----------|-------------:|--------------:|-------------:|
| 2025-12-24 |        nan   |         nan   |        nan   |
| 2025-12-26 |        nan   |         nan   |        nan   |
| 2025-12-29 |      23670.6 |       24089.3 |      24508   |
| 2025-12-30 |      23710.7 |       24127.5 |      24544.2 |
| 2025-12-31 |        nan   |         nan   |        nan   |

---

## get_donchian_channels
Calculate the Donchian Channels: the highest high and the lowest low of the previous periods, whose breakouts signal the start of a trend.

Donchian Channels plot the highest high and lowest low over the `window` periods *preceding* the current one, with the middle line being the average of the two. They are used to identify breakouts and the overall volatility of the price range.

The formula is as follows:

$$
\text{Upper Channel} = \text{Highest High over Window},\;\; \text{ending one period ago}
$$

$$
\text{Lower Channel} = \text{Lowest Low over Window},\;\; \text{ending one period ago}
$$

$$
\text{Middle Channel} = \frac{\text{Upper Channel} + \text{Lower Channel}}{2}
$$

The current period is deliberately excluded from the lookback, per Donchian's original breakout rule and StockCharts' Price Channels definition - including it would make a channel break impossible by construction.

**Also known as:** Donchian Channels, price channel breakout.

**References:**

- paper | Donchian, R.D. (1960). "Commodities: High Finance in Copper." Financial Analysts Journal, 16(6), 133-142.
- paper | Kaufman, P.J. (2013). "Trading Systems and Methods." 5th ed. Wiley.
- library | Referenced against TA-Lib's [DONCHIAN](https://ta-lib.org/functions/donchian.html){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int, optional):</u> Number of periods for the Donchian Channels.
Defaults to 20.
- <u>include_current (bool, optional):</u> Whether the window ends on the current period instead
of the period before it, as in TA-Lib's DONCHIAN, pandas-ta-classic's donchian and
ta's DonchianChannel. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the channels.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: Donchian Channels (upper, middle, lower).

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates Donchian Channels
for each asset in the Toolkit instance.
- TA-Lib's DONCHIAN includes the current period, so each channel here agrees with TA-Lib's of the
previous period; including the current period, it agrees with TA-Lib's DONCHIAN.
- When growth is requested, the method calculates the growth of the channels over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["HGUSD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_donchian_channels().xs("HGUSD", level=1, axis="columns").tail(5)
```

Which returns:

| Date       |   Lower Channel |   Middle Channel |   Upper Channel |
|:-----------|----------------:|-----------------:|----------------:|
| 2025-12-26 |          5.2415 |           5.499  |          5.7565 |
| 2025-12-28 |          5.28   |           5.584  |          5.888  |
| 2025-12-29 |          5.28   |           5.6018 |          5.9235 |
| 2025-12-30 |          5.28   |           5.6018 |          5.9235 |
| 2025-12-31 |          5.28   |           5.6018 |          5.9235 |

---

## get_volatility_cone
Calculate the Volatility Cone for the specified period: the range of the historical annualised realised volatility over several windows, which shows whether the current volatility is high or low for each window.

The Volatility Cone summarizes the distribution of historical annualized realized volatility over a range of rolling windows, showing how the current realized volatility for each window compares to its own historical range. It is commonly used to judge whether current (or implied) volatility is cheap or expensive relative to history.

Realized volatility is the standard deviation of the log returns over each rolling window, annualized with the square root of the observations per year of the period (252 for daily data, or 365 for a ticker that also trades on weekends such as a cryptocurrency, 52 for weekly and 12 for monthly data). Each ticker is measured over the days it traded, so a stock in a Toolkit with a cryptocurrency keeps its own returns rather than flat weekend days. For each window, the cone reports the minimum, the 10th, 25th, 50th, 75th and 90th percentiles, the maximum and the most recent value of that realized volatility series.

The formula is as follows:

$$
\text{Log Return} \;(t) = \ln\left(\frac{\text{Close} \;(t)}{\text{Close} \;(t-1)}\right)
$$

$$
\text{Realized Volatility} \;(t,\; \text{Window}) = \text{Sample Standard Deviation} \;(\text{ddof} = 1) \;\text{of the Log Returns over the last Window periods} \cdot \sqrt{\text{Periods per Year}}
$$

$$
\text{Cone} \;(\text{Window}) = \text{Min},\;\; \text{10th, 25th, 50th (Median), 75th and 90th Percentile, Max and Current (latest) value of Realized Volatility (} t \text{, Window) over the full history, for each window (10, 20, 30, 60, 90 and 120 by default)}
$$

Where Close is the `close_column`, the Adj Close by default (the Close for intraday data).

Options traders compare implied volatility with the cone at the matching horizon: implied volatility near the top of the historical range for that window suggests options are expensive relative to history, near the bottom cheap. The percentiles depend on the sample, so a period that includes a crash widens the cone for as long as it stays in the data; five years of daily data or more gives a more stable picture than one.

**Also known as:** volatility cone, realized volatility term structure.

**References:**

- paper | Burghardt, G. & Lane, M. (1990). "How to Tell if Options are Cheap." Journal of Portfolio Management, 16(2), 72-78.
- paper | Natenberg, S. (1994). "Option Volatility and Pricing." McGraw-Hill.

**Args:**

- <u>windows (list[int] &#124; None, optional):</u> The rolling windows (in periods) to
calculate realized volatility for. Defaults to [10, 20, 30, 60, 90, 120].
- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
If None, the rounding value specified during the initialization of the Toolkit instance will be used.
Defaults to None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The Volatility Cone for each asset, indexed by rolling window.

**Raises:**

ValueError: If the specified `period` is not one of the valid options.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates the
Volatility Cone for each asset in the Toolkit instance.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["BTCUSD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

volatility_cone = toolkit.technicals.get_volatility_cone().xs("BTCUSD", level=1, axis="columns")

volatility_cone.loc[:, ["Min", "10th Percentile", "Median", "90th Percentile", "Max", "Current"]]
```

Which returns:

|   Window |    Min |   10th Percentile |   Median |   90th Percentile |    Max |   Current |
|---------:|-------:|------------------:|---------:|------------------:|-------:|----------:|
|       10 | 0.0875 |            0.2495 |   0.4784 |            0.8814 | 1.5987 |    0.1574 |
|       20 | 0.1146 |            0.2978 |   0.4996 |            0.8581 | 1.3232 |    0.2658 |
|       30 | 0.1704 |            0.317  |   0.5149 |            0.8225 | 1.215  |    0.3448 |
|       60 | 0.2618 |            0.3441 |   0.5461 |            0.7757 | 1.0868 |    0.4155 |
|       90 | 0.2776 |            0.3564 |   0.5356 |            0.7652 | 0.9631 |    0.4132 |
|      120 | 0.2903 |            0.3656 |   0.5216 |            0.7495 | 0.9164 |    0.3861 |

---

## get_chaikin_volatility
Calculate Chaikin's Volatility: the percentage change of the average high-low range over a window, which shows whether the range is widening or narrowing.

Chaikin's Volatility is the rate of change of an Exponential Moving Average of the High - Low range: how much wider or narrower the average range is than `roc_window` periods ago. Chaikin read a sharp rise over a short time as a sign of an approaching bottom (panic selling) and a long decline as typical of a maturing top.

The formula is as follows:

$$
\text{Range Average} = \operatorname{EMA}(\text{High} - \text{Low},\; \text{window})
$$

$$
\text{Chaikin Volatility} = \frac{\text{Range Average}}{\text{Range Average} \;\text{roc\_window} \;\text{periods ago}} - 1
$$

The result is a decimal: 0.25 is an average range 25% wider than `roc_window` periods ago.

**Also known as:** CV, CVI, Chaikin Volatility Indicator.

**References:**

- paper | Achelis, S.B. (2000). "Technical Analysis from A to Z." 2nd ed. McGraw-Hill, "Chaikin's Volatility".
- library | Referenced against TA-Lib's [CVI](https://ta-lib.org/functions/cvi.html){:target="_blank"}
- library | Shares similar logic as pandas-ta-classic's [cvi](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/volatility/cvi.py#L12){:target="_blank"}
- library | Shares similar logic as Tulip Indicators' [cvi](https://tulipindicators.org/cvi){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the open, high and low prices are adjusted
for dividends in the same way.
- <u>window (int, optional):</u> The number of periods of the EMA of the range. Defaults to 10,
as defined by Chaikin.
- <u>roc_window (int, optional):</u> The number of periods the rate of change looks back.
Defaults to 10, as defined by Chaikin.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Chaikin Volatility.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Chaikin Volatility per ticker as decimals, or its growth (if growth is
True).

**Notes:**

- The EMA is seeded with the simple average of its first `window` ranges, so this equals
TA-Lib's CVI and pandas-ta-classic's cvi divided by 100.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["NVDA", "AMD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_chaikin_volatility().tail(5)
```

Which returns:

| Date       |    NVDA |     AMD |   Benchmark |
|:-----------|--------:|--------:|------------:|
| 2025-12-24 | -0.0771 | -0.0443 |     -0.0722 |
| 2025-12-26 | -0.0633 | -0.2027 |     -0.1996 |
| 2025-12-29 | -0.2297 | -0.2813 |     -0.3266 |
| 2025-12-30 | -0.2501 | -0.3586 |     -0.3925 |
| 2025-12-31 | -0.1966 | -0.3463 |     -0.3378 |

---

## get_relative_volatility_index
Calculate Dorsey's Relative Volatility Index (RVI): the standard deviation of the up periods against that of the down periods, from 0 to 100, which shows the direction of volatility.

The Relative Volatility Index is built like the Relative Strength Index, but measures the direction of volatility instead of the size of price changes: on a period that closes higher, the standard deviation of the last `std_window` closes counts as upward volatility, and on one that closes lower as downward volatility. Dorsey designed it to confirm other signals: buy signals when the RVI is above 50 and sell signals when it is below 50. The refined RVI averages the RVI of the highs and of the lows.

The formula is as follows:

$$
\text{Up} = \operatorname{StdDev}(\text{Close},\; \text{std\_window}) \;\text{if the close rose},\;\; \text{else 0}
$$

$$
\text{Down} = \operatorname{StdDev}(\text{Close},\; \text{std\_window}) \;\text{if the close fell},\;\; \text{else 0}
$$

$$
\text{RVI} = \frac{100 \cdot \operatorname{Wilder}(\text{Up},\; \text{window})}{\operatorname{Wilder}(\text{Up},\; \text{window}) + \operatorname{Wilder}(\text{Down},\; \text{window})}
$$

$$
\text{Refined RVI} = \frac{\text{RVI of the highs} + \text{RVI of the lows}}{2}
$$

Wilder is Wilder's smoothing, seeded with a simple average. The RVI runs from 0 to 100.

**Also known as:** RVI, RVIR, Relative Volatility Index. Not to be confused with the Relative Vigor Index (`get_relative_vigor_index`).

**References:**

- paper | Dorsey, D. (1993). "The Relative Volatility Index." Technical Analysis of Stocks & Commodities, 11(6).
- paper | Dorsey, D. (1995). "Refining the Relative Volatility Index." Technical Analysis of Stocks & Commodities, 13(9).
- library | Referenced against TA-Lib's [RVI](https://ta-lib.org/functions/rvi.html){:target="_blank"}
- library | Referenced against TA-Lib's [RVIR](https://ta-lib.org/functions/rvir.html){:target="_blank"}
- library | Shares similar logic as pandas-ta-classic's [rvi](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/volatility/rvi.py#L61){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the open, high and low prices are adjusted
for dividends in the same way.
- <u>window (int, optional):</u> The number of periods of Wilder's smoothing. Defaults to 14,
as defined by Dorsey.
- <u>std_window (int, optional):</u> The number of periods of the standard deviation. Defaults
to 10, as defined by Dorsey.
- <u>method (str, optional):</u> Options are: "original" (the RVI of the close; Dorsey, 1993), "refined" (the
average of the RVI of the highs and the lows; Dorsey, 1995). Defaults to "original".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the RVI.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: RVI values per ticker between 0 and 100, or their growth (if growth is
True).

**Notes:**

- Equals TA-Lib's RVI (method "original") and RVIR (method "refined").
pandas-ta-classic's rvi smooths with an EMA instead of Wilder's smoothing by default,
which gives different values.
- A window in which the price did not move has no RVI (missing) instead of 0.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["JPM", "GS"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_relative_volatility_index().tail(5)
```

Which returns:

| Date       |     JPM |      GS |   Benchmark |
|:-----------|--------:|--------:|------------:|
| 2025-12-24 | 61.2674 | 73.4633 |     72.3434 |
| 2025-12-26 | 56.7194 | 69.8239 |     66.3989 |
| 2025-12-29 | 52.4974 | 66.3047 |     60.8153 |
| 2025-12-30 | 48.5788 | 62.8379 |     55.7399 |
| 2025-12-31 | 45.1855 | 59.4845 |     51.3189 |

---

## get_acceleration_bands
Calculate Headley's Acceleration Bands: bands around a moving average that widen with the range of the candles, whose breakouts show an accelerating trend.

Acceleration Bands place an envelope around a simple average of the close whose width follows the High - Low range of each period relative to its price. Headley used a close outside the bands as the start of an accelerating move (a breakout) and a close back inside them as the end of it.

The formula is as follows:

$$
\text{Range Ratio} = \frac{\text{multiplier} \cdot (\text{High} - \text{Low})}{\text{High} + \text{Low}}
$$

$$
\text{Upper Band} = \operatorname{SMA}(\text{High} \cdot (1 + \text{Range Ratio}),\; \text{window})
$$

$$
\text{Middle Band} = \operatorname{SMA}(\text{Close},\; \text{window})
$$

$$
\text{Lower Band} = \operatorname{SMA}(\text{Low} \cdot (1 - \text{Range Ratio}),\; \text{window})
$$

**Also known as:** ACCBANDS, Price Headley's Acceleration Bands.

**References:**

- paper | Headley, P. (2002). "Big Trends in Trading: Strategies to Master Major Market Moves." John Wiley & Sons.
- library | Referenced against TA-Lib's [ACCBANDS](https://ta-lib.org/functions/accbands.html){:target="_blank"}
- library | Referenced against pandas-ta-classic's [accbands](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/volatility/accbands.py#L17){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the open, high and low prices are adjusted
for dividends in the same way.
- <u>window (int, optional):</u> The number of periods of the simple averages. Defaults to 20,
as defined by Headley.
- <u>multiplier (float, optional):</u> The multiplier of the relative range. Defaults to 4.0, as
defined by Headley.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the bands.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: Upper Band, Middle Band and Lower Band in price units.

**Notes:**

- Equals TA-Lib's ACCBANDS and pandas-ta-classic's accbands.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_acceleration_bands().xs("TSLA", level=1, axis="columns").tail(5)
```

Which returns:

| Date       |   Lower Band |   Middle Band |   Upper Band |
|:-----------|-------------:|--------------:|-------------:|
| 2025-12-24 |      422.209 |       458.558 |      493.941 |
| 2025-12-26 |      424.545 |       460.988 |      497.583 |
| 2025-12-29 |      425.825 |       462.462 |      499.78  |
| 2025-12-30 |      427.161 |       463.676 |      501.346 |
| 2025-12-31 |      429.244 |       464.7   |      501.571 |

---

## get_chande_kroll_stop
Calculate the Chande Kroll Stop: a long and a short stop a multiple of the Average True Range from the recent extremes, which shows where a trend would be broken.

The Chande Kroll Stop is a pair of trailing stops a multiple of the Average True Range from the extreme price of the last `window` periods, smoothed a second time by taking the extreme of those first stops over `stop_window` periods. The high stop trails below the highs and the low stop above the lows: a close below the high stop exits a long position, a close above the low stop exits a short one, and a close above both lines marks an uptrend.

The formula is as follows:

$$
\text{First High Stop} = \text{Highest High}(\text{window}) - \text{multiplier} \cdot \operatorname{ATR}(\text{window})
$$

$$
\text{First Low Stop} = \text{Lowest Low}(\text{window}) + \text{multiplier} \cdot \operatorname{ATR}(\text{window})
$$

$$
\text{High Stop} = \operatorname{Highest}(\text{First High Stop},\; \text{stop\_window})
$$

$$
\text{Low Stop} = \operatorname{Lowest}(\text{First Low Stop},\; \text{stop\_window})
$$

**Also known as:** CKSP, Chande Kroll stop loss. Chande and Kroll call the high stop the "stop short" and the low stop the "stop long".

**References:**

- paper | Chande, T.S. & Kroll, S. (1994). "The New Technical Trader." John Wiley & Sons.
- library | Referenced against TA-Lib's [CKSP](https://ta-lib.org/functions/cksp.html){:target="_blank"}
- library | Shares similar logic as pandas-ta-classic's [cksp](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/trend/cksp.py#L12){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the open, high and low prices are adjusted
for dividends in the same way.
- <u>window (int, optional):</u> The number of periods of the highest high, the lowest low and
the Average True Range. Defaults to 10, as in TA-Lib.
- <u>multiplier (float, optional):</u> The number of Average True Ranges the first stops sit
from the extremes. Defaults to 1.0, as in TA-Lib.
- <u>stop_window (int, optional):</u> The number of periods over which the first stops are
smoothed. Defaults to 9, as in TA-Lib.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the stops.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: High Stop and Low Stop in price units.

**Notes:**

- The ATR is that of `get_average_true_range` (the StockCharts seeding), so the stops start
one period before TA-Lib's CKSP and equal it, and pandas-ta-classic's cksp, once the
seeds have converged (within 1e-8 after about 120 periods with the defaults).

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["META"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_chande_kroll_stop().xs("META", level=1, axis="columns").tail(5)
```

Which returns:

| Date       |   High Stop |   Low Stop |
|:-----------|------------:|-----------:|
| 2025-12-24 |     691.835 |    653.213 |
| 2025-12-26 |     692.75  |    652.298 |
| 2025-12-29 |     692.75  |    652.209 |
| 2025-12-30 |     692.75  |    652.209 |
| 2025-12-31 |     692.75  |    652.209 |

---

## get_adaptive_price_zone
Calculate Leibfarth's Adaptive Price Zone (APZ): bands around a double-smoothed exponential moving average that adapt to the range, which show turning points in a sideways market.

The Adaptive Price Zone is a band around a fast, double-smoothed Exponential Moving Average of the close, with a width that is the same double-smoothed average of the High - Low range. Both averages use the square root of `window` as their period, so the zone follows the price closely. Leibfarth designed it for markets without a trend (an ADX below 30): a close above the zone is a chance to sell, and a close below it a chance to buy, in anticipation of a reversal.

The formula is as follows:

$$
\text{Smoothing Period} = \sqrt{\text{window}}
$$

$$
\text{Middle Band} = \operatorname{EMA}(\operatorname{EMA}(\text{Close},\; \text{Smoothing Period}),\; \text{Smoothing Period})
$$

$$
\text{Range} = \operatorname{EMA}(\operatorname{EMA}(\text{High} - \text{Low},\; \text{Smoothing Period}),\; \text{Smoothing Period})
$$

$$
\text{Upper Band} = \text{Middle Band} + \text{multiplier} \cdot \text{Range}
$$

$$
\text{Lower Band} = \text{Middle Band} - \text{multiplier} \cdot \text{Range}
$$

**Also known as:** APZ, Adaptive Price Zone.

**References:**

- paper | Leibfarth, L. (2006). "Trading With An Adaptive Price Zone." Technical Analysis of Stocks & Commodities, 24(9).
- library | Shares similar logic as finta's [APZ](https://github.com/peerchemist/finta/blob/1.3/finta/finta.py#L1907){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the open, high and low prices are adjusted
for dividends in the same way.
- <u>window (int, optional):</u> The number of periods whose square root is the smoothing
period. Defaults to 20, as in Leibfarth's article.
- <u>multiplier (float, optional):</u> The number of smoothed ranges between the middle band and
the outer bands. Defaults to 2.0.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the bands.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: Upper Band, Middle Band and Lower Band in price units.

**Notes:**

- Each EMA has the smoothing constant $$2 / (\sqrt{\text{window}} + 1)$$ and is seeded with the simple
average of its first $$\text{⌈} \sqrt{\text{window}} \text{⌉}$$ values; after about 35 periods the zone equals
Leibfarth's TradeStation formula, which starts from the first price.
- finta's APZ smooths over the full `window` instead of its square root and centres the
zone on a Double Exponential Moving Average, so it differs by design.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["QQQ"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_adaptive_price_zone().xs("QQQ", level=1, axis="columns").tail(5)
```

Which returns:

| Date       |   Lower Band |   Middle Band |   Upper Band |
|:-----------|-------------:|--------------:|-------------:|
| 2025-12-24 |      602.35  |       614.275 |      626.2   |
| 2025-12-26 |      605.75  |       616.032 |      626.315 |
| 2025-12-29 |      607.778 |       617.105 |      626.431 |
| 2025-12-30 |      609.082 |       617.566 |      626.05  |
| 2025-12-31 |      608.453 |       617.038 |      625.623 |

---

## get_price_distance
Calculate the Price Distance: the distance the price travelled within each period, including the gap from the previous close, a measure of how much the price moves.

The Price Distance estimates how far the price travelled within a period: twice the High - Low range (down to the low and up to the high, or the reverse), less the open-to-close body that the range already covers once, plus the gap from the previous close to the open.

The formula is as follows:

$$
\text{Price Distance} = 2 \cdot (\text{High} - \text{Low}) - \left|\text{Close} - \text{Open}\right| + \left|\text{Open} - \text{Previous Close}\right|
$$

**Also known as:** PDIST, price distance volatility.

**References:**

- paper | ProRealCode, "Price Distance" indicator.
- library | Referenced against pandas-ta-classic's [pdist](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/volatility/pdist.py#L17){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the open, high and low prices are adjusted
for dividends in the same way.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Price Distance.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Price Distance per ticker in price units, or its growth (if growth is
True).

**Notes:**

- Equals pandas-ta-classic's pdist.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["KO", "PEP"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_price_distance().tail(5)
```

Which returns:

| Date       |     KO |    PEP |   Benchmark |
|:-----------|-------:|-------:|------------:|
| 2025-12-24 | 0.6278 | 2.0768 |      3.6118 |
| 2025-12-26 | 0.9417 | 1.611  |      4.6735 |
| 2025-12-29 | 1.0889 | 2.3679 |      8.6524 |
| 2025-12-30 | 0.9515 | 2.6979 |      3.8896 |
| 2025-12-31 | 0.3924 | 1.7274 |      6.1619 |

---

## get_market_thermometer
Calculate Elder's Market Thermometer: how far each period's range pushes outside that of the previous period, which shows how hot or quiet the market is.

The Market Thermometer measures how far each period's range pushes outside the previous one: the larger of the rise of the high above the previous high and the fall of the low below the previous low, or 0 for an inside period. Elder compares it with its Exponential Moving Average: a temperature far above the average (Elder uses three times) marks a burst of volatility in which to take profits, and several periods below the average a quiet market that often precedes an explosive move.

The formula is as follows:

$$
\text{Thermometer} = \max(\text{High} - \text{Previous High},\; \text{Previous Low} - \text{Low},\; 0)
$$

$$
\text{Thermometer Average} = \operatorname{EMA}(\text{Thermometer},\; \text{window})
$$

**Also known as:** THERMO, Elder's thermometer, market temperature.

**References:**

- paper | Elder, A. (2002). "Come Into My Trading Room." John Wiley & Sons.
- library | Shares similar logic as pandas-ta-classic's [thermo](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/volatility/thermo.py#L18){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the open, high and low prices are adjusted
for dividends in the same way.
- <u>window (int, optional):</u> The number of periods of the EMA. Defaults to 22, as defined by
Elder.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Thermometer and its average.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: Thermometer and Thermometer Average in price units.

**Notes:**

- An inside period has a temperature of 0, as Elder defines it. pandas-ta-classic's thermo
takes the absolute changes of both the high and the low, so a falling high or a rising
low also counts there; the two agree on periods with a higher high and a lower low.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["GLD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_market_thermometer().xs("GLD", level=1, axis="columns").tail(5)
```

Which returns:

| Date       |   Thermometer |   Thermometer Average |
|:-----------|--------------:|----------------------:|
| 2025-12-24 |          0    |                2.6893 |
| 2025-12-26 |          5.82 |                2.9615 |
| 2025-12-29 |         19.42 |                4.3927 |
| 2025-12-30 |          0.04 |                4.0142 |
| 2025-12-31 |          2.97 |                3.9234 |

---

## get_squeeze_momentum
Calculate the Squeeze Momentum (TTM Squeeze): whether the Bollinger Bands lie inside the Keltner Channels (a squeeze of volatility) and the momentum that shows the direction of the breakout.

The squeeze compares two volatility bands around the same simple average of the close: Bollinger Bands, which follow the standard deviation, and a Keltner Channel, which follows the average True Range. When the Bollinger Bands contract inside the Keltner Channel, volatility is unusually low and the market is "in a squeeze". Carter trades the release of the squeeze (the first period the bands leave the channel) in the direction of the momentum, LazyBear's linear regression of the close relative to the middle of its recent range and its average.

The formula is as follows:

$$
\text{Middle} = \operatorname{SMA}(\text{Close},\; \text{window})
$$

$$
\text{Bollinger Bands} = \text{Middle} \;\pm \;\text{num\_std\_dev} \cdot \operatorname{StdDev}(\text{Close},\; \text{window})
$$

$$
\text{Keltner Channel}(m) = \text{Middle} \;\pm m \cdot \operatorname{SMA}(\text{True Range},\; \text{window})
$$

$$
\text{Squeeze} = \text{the number of} \;\text{keltner\_multipliers} \;m \;\text{with the Bollinger Bands inside Keltner Channel}(m)
$$

$$
\text{Momentum} = \text{Linear Regression}\left(\text{Close} - \frac{\frac{\text{Highest High} + \text{Lowest Low}}{2} + \text{Middle}}{2},\; \text{window}\right)
$$

With the default multipliers 2, 1.5 and 1 (the wide, normal and narrow channels of the TTM Squeeze Pro), the Squeeze is 0 without a squeeze and 1, 2 or 3 for a low, normal or high compression. Carter's original squeeze (a Keltner Channel of 1.5) is on from 2; a single Keltner multiplier of 1.5 returns it as 1 (on) or 0 (off).

**Also known as:** TTM Squeeze, Squeeze Pro, SQZ, SQZMOM, squeeze momentum indicator.

**References:**

- paper | Carter, J.F. (2005). "Mastering the Trade." McGraw-Hill, chapter 11.
- paper | LazyBear (2014). "Squeeze Momentum Indicator." TradingView script.
- library | Referenced against TA-Lib's [SQZMOM](https://ta-lib.org/functions/sqzmom.html){:target="_blank"}
- library | Referenced against pandas-ta-classic's [squeeze](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/momentum/squeeze.py#L94){:target="_blank"}
- library | Shares similar logic as pandas-ta-classic's [squeeze_pro](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/momentum/squeeze_pro.py#L17){:target="_blank"}
- library | Shares similar logic as finta's [SQZMI](https://github.com/peerchemist/finta/blob/1.3/finta/finta.py#L1941){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the open, high and low prices are adjusted
for dividends in the same way.
- <u>window (int, optional):</u> The number of periods of the bands, the channels, the range
and the regression. Defaults to 20, as defined by Carter.
- <u>num_std_dev (float, optional):</u> The number of standard deviations of the Bollinger
Bands. Defaults to 2.0, as defined by Carter.
- <u>keltner_multipliers (list[float] &#124; None, optional):</u> The widths, in average True Ranges,
of the Keltner Channels the Bollinger Bands are compared with. Defaults to None,
which uses [2.0, 1.5, 1.0], as in TA-Lib's SQZMOM.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Momentum and Squeeze.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: Momentum (in price units) and Squeeze (the number of Keltner
Channels the Bollinger Bands lie inside).

**Notes:**

- The Momentum agrees with TA-Lib's SQZMOM and pandas-ta-classic's `squeeze` in LazyBear's form.
The Squeeze agrees with TA-Lib's squeeze output, with 0 instead of -1 for no squeeze. It starts
on the `window`-th period, while TA-Lib reports it from the first Momentum on.
- The Keltner Channel here is LazyBear's (a simple average of the close and of the True
Range), not that of `get_keltner_channels`, and the Bollinger standard deviation is the
population one, as in `get_bollinger_bands`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["QQQ"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_squeeze_momentum().xs("QQQ", level=1, axis="columns").tail(5)
```

Which returns:

| Date       |   Momentum |   Squeeze |
|:-----------|-----------:|----------:|
| 2025-12-24 |     3.8112 |         1 |
| 2025-12-26 |     3.072  |         1 |
| 2025-12-29 |     2.2261 |         1 |
| 2025-12-30 |     0.9902 |         1 |
| 2025-12-31 |    -0.3707 |         1 |

---

## get_standard_deviation_channel
Calculate the Standard Deviation Channel: a least-squares line through the prices with bands a number of standard deviations above and below it.

The line runs through all prices of the Toolkit's date range, or the last `window` of them.

The channel shows the trend of the whole period and how far the prices stray from it: a price near an outer band lies far from the trend of the period. It is the thinkorswim study StDevAll, which draws the regression line of all bars (InertiaAll) with bands at 1, 2 and 3 standard deviations.

The formula is as follows, with time $$x = 0$$, ..., n - 1 over the n prices of the period:

$$
\text{Linear Regression} = b_{0} + b_{1} \cdot x,\;\; \text{the least-squares line through the prices}
$$

$$
\text{Upper Band}\; k = \text{Linear Regression} + k \cdot \operatorname{StdDev}(\text{Close})
$$

$$
\text{Lower Band}\; k = \text{Linear Regression} - k \cdot \operatorname{StdDev}(\text{Close})
$$

with the sample standard deviation (ddof=1) of the prices of the period.

**Also known as:** standard deviation channel, StDevAll, linear regression channel, regression bands.

**References:**

- paper | thinkorswim (TD Ameritrade). thinkScript studies StDevAll and InertiaAll.
- library | Referenced against pandas-ta-classic's [tos_stdevall](https://github.com/xgboosted/pandas-ta-classic/blob/0.9.0/pandas_ta_classic/statistics/tos_stdevall.py#L15){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int &#124; None, optional):</u> The number of latest periods the line is fitted over,
at least 2. Defaults to None, which uses every period of the Toolkit's date range.
- <u>num_std_dev (float &#124; list[float] &#124; None, optional):</u> The number or numbers of standard
deviations of the bands. Defaults to None, which uses 1, 2 and 3.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Standard Deviation Channel.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame:
Linear Regression with a Lower Band k and Upper Band k per number of standard deviations k.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates the
Standard Deviation Channel for each asset in the Toolkit instance.
- The channel agrees with pandas-ta-classic's tos_stdevall.
- The line is fitted over the whole period at once, so every value depends on the later prices of the
period and the channel is redrawn when the date range changes. It describes a period and is not a
signal that was known at the time, which is why `collect_volatility_indicators` leaves it out.
- When growth is requested, the method calculates the growth of the Standard Deviation Channel
over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_standard_deviation_channel(num_std_dev=[1, 2]).xs("AAPL", level=1, axis="columns").tail(5)
```

Which returns:

| Date       |   Linear Regression |   Lower Band 1 |   Lower Band 2 |   Upper Band 1 |   Upper Band 2 |
|:-----------|--------------------:|---------------:|---------------:|---------------:|---------------:|
| 2025-12-24 |             240.281 |        200.328 |        160.375 |        280.234 |        320.188 |
| 2025-12-26 |             240.38  |        200.426 |        160.473 |        280.333 |        320.286 |
| 2025-12-29 |             240.478 |        200.525 |        160.572 |        280.431 |        320.385 |
| 2025-12-30 |             240.577 |        200.623 |        160.67  |        280.53  |        320.483 |
| 2025-12-31 |             240.675 |        200.722 |        160.769 |        280.628 |        320.582 |

---

## get_signal_to_noise_ratio
Calculate the Signal-to-Noise Ratio (SNR): the net move of the close over a window divided by the Average True Range, which shows how cleanly the price trends.

The Signal-to-Noise Ratio divides the net move of the close over the window (the signal) by the Average True Range over the same window (the noise). A ratio of 5 means the price moved five times its average range in `window` periods, a market that trends cleanly, while a ratio near 0 means the price moved a lot but went nowhere. Skeggs and Hill use it to measure how much trend a market offers a trend follower.

The formula is as follows:

$$
\text{Signal} = \left|\operatorname{Close}(t) - \operatorname{Close}(t - \text{window})\right|
$$

$$
\text{Noise} = \operatorname{ATR}(\text{window}),\;\; \text{Wilder's Smoothed Moving Average of the True Range}
$$

$$
\text{SNR} = \frac{\text{Signal}}{\text{Noise}}
$$

Because the ATR includes the gaps between periods, the noise covers the overnight moves a close-to-close measure would miss. The ratio says how far the price trended, not in which direction.

**Also known as:** SNR, signal to noise ratio, trend strength ratio.

**References:**

- paper | Skeggs, J. and Hill, A. (2015). "Back in Black Part 2: The Opportunity Set for Trend Following." Man AHL.
- library | Referenced against TTR (R)'s [SNR](https://github.com/joshuaulrich/TTR/blob/v0.24.4/R/SNR.R#L47){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data. Options are:
"intraday" (intraday prices), "daily" (daily prices), "weekly" (weekly prices),
"monthly" (monthly prices), "quarterly" (quarterly prices), "yearly" (yearly prices). Defaults
to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the high and low prices are adjusted for
dividends in the same way.
- <u>window (int, optional):</u> The number of periods of the move and of the Average True
Range. Defaults to 14, the default window of the Average True Range.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series or pd.DataFrame: Signal-to-Noise Ratio values, in multiples of the Average
True Range.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the Signal-to-Noise Ratio for each asset in the Toolkit instance.
- The ATR is that of `get_average_true_range`, whose first True Range is High — Low (the
StockCharts convention). TTR's ATR starts one period later, so the ratio equals TTR's
SNR once the seeds of the averages have converged (within 0.01% after about 100
periods with the default window).
- A window without any range (an ATR of 0) has no ratio.
- When growth is requested, the method calculates the growth of the Signal-to-Noise
Ratio over the given lag.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_signal_to_noise_ratio().tail(5)
```

Which returns:

| Date       |   AAPL |   MSFT |   Benchmark |
|:-----------|-------:|-------:|------------:|
| 2025-12-24 | 1.4877 | 0.8712 |      1.1787 |
| 2025-12-26 | 1.201  | 0.5828 |      1.025  |
| 2025-12-29 | 0.9597 | 0.5194 |      0.9867 |
| 2025-12-30 | 0.994  | 0.6213 |      0.9957 |
| 2025-12-31 | 1.744  | 0.7096 |      0.6057 |

---

