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
Calculates all Technical Indicators based on the data provided.

**Args:**

- <u>period (str, optional):</u> The period to use for the calculation. Defaults to "daily".
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
- If `growth` is set to True, the method calculates the growth of the indicator values
using the specified `lag`.

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

| Date       |   McClellan Oscillator |   Advancers - Decliners |   On-Balance Volume |   Accumulation/Distribution Line |   Chaikin Oscillator |     TRIN |   New Highs - New Lows |   Chaikin Money Flow |   Ease of Movement |   Negative Volume Index |   Positive Volume Index |   Money Flow Index |   Williams %R |   Aroon Indicator Up |   Aroon Indicator Down |   Commodity Channel Index |   Relative Vigor Index |   Relative Vigor Index Signal Line |       Force Index |   Ultimate Oscillator |   Percentage Price Oscillator |   Detrended Price Oscillator |   Average Directional Index |   Chande Momentum Oscillator |   Ichimoku Conversion Line |   Ichimoku Base Line |   Ichimoku Leading Span A |   Ichimoku Leading Span B |   Stochastic %K |   Stochastic %D |   MACD Line |   MACD Signal Line |   Relative Strength Index |   Stochastic RSI %K |   Stochastic RSI %D |   True Strength Index |   True Strength Index Signal Line |   Balance of Power |   Awesome Oscillator |   Vortex Indicator VI+ |   Vortex Indicator VI- |   Elder Ray Bull Power |   Elder Ray Bear Power |   Rate of Change |   Choppiness Index |   Know Sure Thing |   Know Sure Thing Signal Line |   Coppock Curve |   Simple Moving Average (SMA) |   Exponential Moving Average (EMA) |   Double Exponential Moving Average (DEMA) |   TRIX |   Triangular Moving Average |   Weighted Moving Average (WMA) |   Hull Moving Average (HMA) |   Kaufman Adaptive Moving Average (KAMA) |   Volume Weighted Average Price (VWAP) |   Parabolic SAR |   Pivot Point |   Pivot Point Resistance 1 |   Pivot Point Support 1 |   Fibonacci Retracement 50.0% |   Fibonacci Retracement 61.8% |   Bollinger Band Upper |   Bollinger Band Middle |   Bollinger Band Lower |   Bollinger %B |   Bollinger BandWidth |   True Range |   Average True Range |   Supertrend |   Supertrend Trend Direction |   Keltner Channel Upper |   Keltner Channel Middle |   Keltner Channel Lower |   Donchian Channel Upper |   Donchian Channel Middle |   Donchian Channel Lower |
|:-----------|-----------------------:|------------------------:|--------------------:|---------------------------------:|---------------------:|---------:|-----------------------:|---------------------:|-------------------:|------------------------:|------------------------:|-------------------:|--------------:|---------------------:|-----------------------:|--------------------------:|-----------------------:|-----------------------------------:|------------------:|----------------------:|------------------------------:|-----------------------------:|----------------------------:|-----------------------------:|---------------------------:|---------------------:|--------------------------:|--------------------------:|----------------:|----------------:|------------:|-------------------:|--------------------------:|--------------------:|--------------------:|----------------------:|----------------------------------:|-------------------:|---------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------:|-------------------:|------------------:|------------------------------:|----------------:|------------------------------:|-----------------------------------:|-------------------------------------------:|-------:|----------------------------:|--------------------------------:|----------------------------:|-----------------------------------------:|---------------------------------------:|----------------:|--------------:|---------------------------:|------------------------:|------------------------------:|------------------------------:|-----------------------:|------------------------:|-----------------------:|---------------:|----------------------:|-------------:|---------------------:|-------------:|-----------------------------:|------------------------:|-------------------------:|------------------------:|-------------------------:|--------------------------:|-------------------------:|
| 2025-12-17 |                -0.0981 |                      -1 |         2.26688e+09 |                      3.99771e+09 |         -1.74849e+07 | nan      |                      0 |              -0.0358 |            -4.7166 |                 2735.53 |                 788.841 |            39.7393 |      -98.8222 |              28.5714 |               100      |                 -139.905  |                -0.2262 |                            -0.0758 |      -3.27416e+07 |               44.5331 |                        0.0063 |                       0.0306 |                     24.6712 |                     -20.621  |                    275.43  |              276.008 |                   265.041 |                   250.519 |          1.1778 |          8.6605 |      1.7262 |             3.1596 |                   45.1866 |              0      |              1.2037 |               12.3226 |                           19.7487 |            -0.7013 |               1.2653 |                 0.9211 |                 1.0533 |                -0.1328 |                -4.6371 |          -0.0206 |            49.8427 |            0.3638 |                        0.5107 |          0.0029 |                       277.781 |                            275.314 |                                    275.767 | 0.0016 |                     277.982 |                         276.128 |                     273.116 |                                  274.218 |                                277.974 |         285.493 |       273.015 |                    275.185 |                 271.488 |                       279.158 |                       277.161 |                285.548 |                 276     |                266.452 |         0.2327 |                0.0692 |       4.5043 |               4.871  |      268.465 |                            1 |                 284.794 |                  275.314 |                 265.833 |                  287.618 |                   279.232 |                  270.846 |
| 2025-12-18 |                -0.0378 |                       1 |         2.31851e+09 |                      4.02708e+09 |         -1.16789e+07 | nan      |                      0 |               0.0024 |            -7.4094 |                 2735.53 |                 789.857 |            34.4002 |      -75.8192 |              21.4286 |               100      |                 -162.428  |                -0.2832 |                            -0.1659 |      -2.59752e+07 |               50.9808 |                        0.0047 |                      -0.3822 |                     24.4323 |                     -24.9065 |                    272.6   |              276.008 |                   265.041 |                   250.519 |         24.1808 |         14.0381 |      1.2731 |             2.7823 |                   45.9182 |              2.4336 |              2.0149 |                9.3441 |                           17.1476 |            -0.2126 |               0.0099 |                 0.865  |                 1.0802 |                -2.0699 |                -8.7267 |          -0.0239 |            42.7375 |            0.311  |                        0.4834 |         -0.014  |                       277.308 |                            274.771 |                                    274.694 | 0.0014 |                     277.238 |                         275.257 |                     271.901 |                                  274.081 |                                277.321 |         284.309 |       272.265 |                    273.833 |                 269.328 |                       276.821 |                       274.272 |                285.211 |                 276.181 |                267.151 |         0.2267 |                0.0654 |       6.6568 |               4.9986 |      268.465 |                            1 |                 284.635 |                  274.771 |                 264.907 |                  287.618 |                   279.158 |                  270.697 |
| 2025-12-19 |                 0.0139 |                       1 |         2.46314e+09 |                      4.11448e+09 |          1.95656e+07 | nan      |                      0 |               0.1361 |            -9.4903 |                 2735.53 |                 794.152 |            43.3299 |      -68.989  |              14.2857 |                92.8571 |                 -103.239  |                -0.2694 |                            -0.2349 |       5.93141e+06 |               51.5414 |                        0.0037 |                      -0.4186 |                     23.9077 |                     -39.3403 |                    272.6   |              276.008 |                   265.041 |                   250.519 |         31.011  |         18.7898 |      1.0212 |             2.4301 |                   49.0174 |             12.7428 |              5.0588 |                7.6467 |                           14.7724 |             0.3234 |              -1.1188 |                 0.903  |                 1.137  |                -0.8132 |                -5.4969 |          -0.0333 |            41.2482 |            0.2645 |                        0.4504 |         -0.0269 |                       276.636 |                            274.498 |                                    274.194 | 0.0012 |                     276.433 |                         274.645 |                     271.147 |                                  273.957 |                                276.002 |         282.481 |       269.983 |                    273.942 |                 267.286 |                       276.821 |                       274.272 |                284.285 |                 276.55  |                268.816 |         0.2524 |                0.0559 |       4.6837 |               4.9761 |      268.465 |                            1 |                 284.312 |                  274.498 |                 264.683 |                  287.618 |                   276.821 |                  266.023 |
| 2025-12-22 |                -0.0419 |                      -1 |         2.42657e+09 |                      4.08789e+09 |          2.21089e+07 | nan      |                      0 |               0.079  |           -12.8266 |                 2708.54 |                 794.152 |            36.4312 |      -81.4489 |               7.1429 |                85.7143 |                 -104.734  |                -0.2367 |                            -0.2614 |      -7.97981e+06 |               45.7604 |                        0.0022 |                       2.2593 |                     23.4206 |                     -64.5457 |                    272.6   |              276.008 |                   264.954 |                   250.519 |         18.5511 |         24.581  |      0.5976 |             2.0636 |                   44.0573 |              0      |              5.0588 |                4.6682 |                           12.2463 |            -0.5608 |              -2.0902 |                 0.8075 |                 1.2147 |                -0.8978 |                -4.2561 |          -0.0532 |            40.4149 |            0.2055 |                        0.4111 |         -0.0418 |                       275.553 |                            273.902 |                                    273.122 | 0.0009 |                     275.578 |                         273.764 |                     270.399 |                                  273.151 |                                275.063 |         280.835 |       271.777 |                    274.59  |                 269.906 |                       276.821 |                       274.272 |                284.343 |                 276.525 |                268.707 |         0.0846 |                0.0565 |       3.3583 |               4.8605 |      268.465 |                            1 |                 283.406 |                  273.902 |                 264.397 |                  287.618 |                   276.821 |                  266.023 |
| 2025-12-23 |                 0.0106 |                       1 |         2.45621e+09 |                      4.11471e+09 |          2.96727e+07 | nan      |                      0 |               0.0651 |           -14.4653 |                 2722.43 |                 794.152 |            37.2984 |      -69.5725 |               0      |                78.5714 |                  -97.9342 |                -0.205  |                            -0.2501 |      -1.44131e+06 |               49.1967 |                        0.0014 |                       2.3511 |                     23.1943 |                     -51.4169 |                    272.6   |              276.008 |                   265.083 |                   250.519 |         30.4275 |         26.6632 |      0.3694 |             1.7248 |                   47.029  |             15.5285 |              9.4238 |                3.0048 |                            9.9359 |             0.517  |              -2.6623 |                 0.7732 |                 1.2661 |                -1.9284 |                -4.8582 |          -0.0415 |            46.4518 |            0.1522 |                        0.3663 |         -0.0501 |                       274.714 |                            273.57  |                                    272.607 | 0.0007 |                     274.764 |                         273.212 |                     269.985 |                                  272.908 |                                274.256 |         279.354 |       270.843 |                    272.115 |                 268.757 |                       274.882 |                       272.792 |                284.455 |                 276.347 |                268.24  |         0.1958 |                0.0587 |       2.9298 |               4.7226 |      268.465 |                            1 |                 282.71  |                  273.57  |                 264.43  |                  287.618 |                   276.821 |                  266.023 |
| 2025-12-24 |                 0.0554 |                       1 |         2.47412e+09 |                      4.11466e+09 |          3.00518e+07 | nan      |                      0 |               0.0846 |            -6.6454 |                 2736.93 |                 794.152 |            41.6581 |      -51.6561 |               0      |                71.4286 |                  -34.6704 |                -0.1841 |                            -0.2228 |       2.20159e+06 |               54.4448 |                        0.0011 |                       3.0907 |                     22.0179 |                     -32.919  |                    272.6   |              276.008 |                   265.063 |                   250.519 |         48.3439 |         32.4408 |      0.3017 |             1.4402 |                   50.0121 |             38.5457 |             18.0248 |                2.4525 |                            8.0651 |             0.4551 |              -2.8188 |                 0.8892 |                 1.1613 |                 1.0804 |                -2.1383 |          -0.0245 |            53.1324 |            0.1033 |                        0.3168 |         -0.0518 |                       274.223 |                            273.476 |                                    272.559 | 0.0006 |                     274.049 |                         272.965 |                     270.161 |                                  272.904 |                                273.798 |         278.021 |       270.531 |                    272.438 |                 269.508 |                       273.094 |                       271.425 |                284.438 |                 276.19  |                267.941 |         0.2981 |                0.0597 |       3.2188 |               4.6152 |      268.465 |                            1 |                 282.345 |                  273.476 |                 264.606 |                  283.741 |                   274.882 |                  266.023 |
| 2025-12-26 |                -0.0066 |                      -1 |         2.4526e+09  |                      4.10239e+09 |          2.35736e+07 | nan      |                      0 |               0.0857 |            -5.4396 |                 2736.93 |                 792.962 |            46.9441 |      -51.1363 |               0      |                64.2857 |                  -25.6932 |                -0.1697 |                            -0.1974 |  735536           |               51.2159 |                        0.0008 |                      -0.6819 |                     20.9256 |                     -27.7033 |                    272.6   |              276.098 |                   264.961 |                   250.519 |         48.8637 |         42.545  |      0.2126 |             1.1946 |                   49.1689 |             34.622  |             29.5654 |                1.7619 |                            6.4893 |            -0.3028 |              -2.1658 |                 0.9091 |                 1.1011 |                 1.1553 |                -1.346  |          -0.0193 |            55.49   |            0.0564 |                        0.2631 |         -0.0522 |                       273.84  |                            273.339 |                                    272.426 | 0.0004 |                     273.429 |                         272.729 |                     270.664 |                                  272.88  |                                273.418 |         276.821 |       272.863 |                    274.471 |                 271.252 |                       272.6   |                       271.048 |                284.387 |                 275.983 |                267.579 |         0.2899 |                0.0609 |       2.5013 |               4.4642 |      268.465 |                            1 |                 281.822 |                  273.339 |                 264.856 |                  280.164 |                   273.094 |                  266.023 |
| 2025-12-29 |                 0.0405 |                       1 |         2.47632e+09 |                      4.11195e+09 |          2.18213e+07 |   0.4593 |                      0 |               0.0756 |            -4.7955 |                 2736.93 |                 794.007 |            48.1203 |      -48.4089 |              35.7143 |                57.1429 |                  -30.567  |                -0.1563 |                            -0.1782 |       1.77189e+06 |               57.3149 |                        0.0006 |                       0.1103 |                     20.0592 |                     -21.8633 |                    270.612 |              276.183 |                   265.068 |                   250.519 |         51.5911 |         49.5995 |      0.169  |             0.9895 |                   49.9666 |             40.0248 |             37.7308 |                1.4002 |                            5.217  |             0.5323 |              -2.0654 |                 0.9316 |                 1.0955 |                 0.2129 |                -1.7901 |          -0.0149 |            54.4742 |            0.0118 |                        0.2104 |         -0.0496 |                       273.546 |                            273.268 |                                    272.416 | 0.0003 |                     272.918 |                         272.591 |                     271.326 |                                  272.877 |                                273.16  |         275.741 |       272.926 |                    273.939 |                 271.438 |                       272.6   |                       271.048 |                284.195 |                 275.729 |                267.264 |         0.3276 |                0.0614 |       2.003  |               4.2884 |      268.465 |                            1 |                 281.304 |                  273.268 |                 265.233 |                  279.177 |                   272.6   |                  266.023 |
| 2025-12-30 |                -0.0195 |                      -1 |         2.45418e+09 |                      4.10949e+09 |          1.83379e+07 |   1.5877 |                      0 |               0.0249 |            -5.2836 |                 2730.13 |                 794.007 |            43.4593 |      -53.5607 |              28.5714 |                50      |                  -35.5283 |                -0.1288 |                            -0.1608 | -464819           |               54.1042 |                        0.0003 |                      -2.3582 |                     19.276  |                     -21.7389 |                    270.612 |              276.183 |                   265.068 |                   250.519 |         46.4393 |         48.9647 |      0.0788 |             0.8074 |                   48.4209 |             29.5554 |             34.7341 |                0.6843 |                            4.0838 |             0.15   |              -1.9448 |                 0.9145 |                 1.1096 |                 0.0857 |                -1.708  |          -0.0148 |            53.5704 |           -0.0182 |                        0.1612 |         -0.0465 |                       273.254 |                            273.117 |                                    272.247 | 0.0002 |                     272.531 |                         272.403 |                     271.798 |                                  272.849 |                                272.911 |         274.769 |       272.541 |                    273.676 |                 271.673 |                       272.6   |                       271.048 |                283.299 |                 275.23  |                267.162 |         0.308  |                0.0586 |       1.7937 |               4.1102 |      268.465 |                            1 |                 280.707 |                  273.117 |                 265.526 |                  279.177 |                   272.6   |                  266.023 |
| 2025-12-31 |                -0.0707 |                      -1 |         2.42688e+09 |                      4.08531e+09 |          7.5513e+06  | nan      |                      0 |              -0.0357 |            -5.2468 |                 2730.13 |                 790.459 |            38.2003 |      -62.8029 |              21.4286 |                42.8571 |                  -56.9135 |                -0.0887 |                            -0.1381 |      -4.82706e+06 |               46.4079 |                       -0.0003 |                      -1.5169 |                     18.7175 |                     -37.4456 |                    270.248 |              276.821 |                   265.6   |                   250.867 |         37.1971 |         45.0758 |     -0.0897 |             0.628  |                   45.6902 |             12.0098 |             27.1967 |               -0.6702 |                            2.8953 |            -0.6218 |              -1.6049 |                 0.9113 |                 1.1148 |                -0.0091 |                -1.9324 |          -0.0248 |            52.5944 |           -0.0452 |                        0.1157 |         -0.0431 |                       272.762 |                            272.823 |                                    271.815 | 0.0001 |                     272.2   |                         272.091 |                     271.883 |                                  272.686 |                                272.594 |         273.895 |       272.198 |                    273.062 |                 271.268 |                       272.6   |                       271.048 |                281.366 |                 274.516 |                267.666 |         0.2372 |                0.0499 |       1.9233 |               3.954  |      268.465 |                            1 |                 280.039 |                  272.823 |                 265.607 |                  279.177 |                   272.6   |                  266.023 |

---

## collect_breadth_indicators
Calculates and collects various breadth indicators based on the provided data.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
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
- If `growth` is set to True, the method calculates the growth of the indicator values
using the specified `lag`.

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

| Date       |   McClellan Oscillator |   Advancers - Decliners |   On-Balance Volume |   Accumulation/Distribution Line |   Chaikin Oscillator |     TRIN |   New Highs - New Lows |   Chaikin Money Flow |   Ease of Movement |   Negative Volume Index |   Positive Volume Index |
|:-----------|-----------------------:|------------------------:|--------------------:|---------------------------------:|---------------------:|---------:|-----------------------:|---------------------:|-------------------:|------------------------:|------------------------:|
| 2025-12-17 |                -0.0981 |                      -1 |         2.26688e+09 |                      3.99772e+09 |         -1.74845e+07 | nan      |                      0 |              -0.0358 |            -4.7239 |                 2735.56 |                 788.833 |
| 2025-12-18 |                -0.0378 |                       1 |         2.31851e+09 |                      4.02709e+09 |         -1.16785e+07 | nan      |                      0 |               0.0024 |            -7.4207 |                 2735.56 |                 789.848 |
| 2025-12-19 |                 0.0139 |                       1 |         2.46314e+09 |                      4.11449e+09 |          1.95658e+07 | nan      |                      0 |               0.1361 |            -9.5049 |                 2735.56 |                 794.143 |
| 2025-12-22 |                -0.0419 |                      -1 |         2.42657e+09 |                      4.0879e+09  |          2.21091e+07 | nan      |                      0 |               0.079  |           -12.8462 |                 2708.57 |                 794.143 |
| 2025-12-23 |                 0.0106 |                       1 |         2.45621e+09 |                      4.11472e+09 |          2.96729e+07 | nan      |                      0 |               0.0651 |           -14.4874 |                 2722.46 |                 794.143 |
| 2025-12-24 |                 0.0554 |                       1 |         2.47412e+09 |                      4.11466e+09 |          3.0052e+07  | nan      |                      0 |               0.0846 |            -6.6556 |                 2736.96 |                 794.143 |
| 2025-12-26 |                -0.0066 |                      -1 |         2.4526e+09  |                      4.1024e+09  |          2.35738e+07 | nan      |                      0 |               0.0857 |            -5.448  |                 2736.96 |                 792.954 |
| 2025-12-29 |                 0.0405 |                       1 |         2.47632e+09 |                      4.11196e+09 |          2.18213e+07 |   0.4593 |                      0 |               0.0756 |            -4.8029 |                 2736.96 |                 793.999 |
| 2025-12-30 |                -0.0195 |                      -1 |         2.45418e+09 |                      4.1095e+09  |          1.83379e+07 |   1.5877 |                      0 |               0.0249 |            -5.2917 |                 2730.16 |                 793.999 |
| 2025-12-31 |                -0.0707 |                      -1 |         2.42688e+09 |                      4.08532e+09 |          7.55142e+06 | nan      |                      0 |              -0.0357 |            -5.2549 |                 2730.16 |                 790.451 |

---

## get_mcclellan_oscillator
Calculate the McClellan Oscillator for a given price series.

The McClellan Oscillator is the difference between a short-term and a long-term exponential moving average of the daily advance/decline signal. Traditionally it is calculated from the number of advancing minus declining stocks across a market; here it is applied to each ticker's own signal (+1 on a day it closed higher, -1 on a day it closed lower, 0 otherwise), so it measures how persistently that ticker has been rising or falling.

The formula is as follows:

$$
\text{McClellan Oscillator} = \operatorname{EMA}(\text{Advance/Decline} \;\text{Signal},\; \text{short\_ema\_window}) - \operatorname{EMA}(\text{Advance/Decline} \;\text{Signal},\; \text{long\_ema\_window})
$$

**Also known as:** McClellan oscillator, market breadth.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
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
- If `growth` is set to True, the method calculates the growth of the indicator values
using the specified `lag`.

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
Calculate the daily advance/decline signal for a given price series.

Traditionally advancers versus decliners is a market-wide count of rising against falling stocks; applied to a single ticker it becomes a directional signal: +1 on a day the ticker closed higher than the day before, -1 on a day it closed lower and 0 on an unchanged day. It feeds the McClellan Oscillator; get_trin and get_new_highs_new_lows measure breadth across all tickers.

The formula is as follows:

$$
\text{Signal} = + 1 \;\text{if Close}(t) > \operatorname{Close}(t-1),\;\; - 1 \;\text{if Close}(t) < \operatorname{Close}(t-1),\;\; \text{else 0}
$$

**Also known as:** advance decline ratio, market breadth.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
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
- If `growth` is set to True, the method calculates the growth of the indicator values
using the specified `lag`.

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
Calculate the On-Balance Volume (OBV) for a given price series.

The On-Balance Volume (OBV) is a technical indicator that uses volume flow to predict changes in stock price. It accumulates the volume on up days and subtracts the volume on down days. The resulting OBV line provides insights into the buying and selling pressure behind price movements.

The formula is as follows:

$$
\text{OBV} = \text{Previous OBV} + \text{Volume if Close} > \text{Previous Close, Previous OBV} - \text{Volume if Close} < \text{Previous Close},\;\; \text{and Previous OBV otherwise}
$$

The level of OBV has no meaning by itself, since it depends on the first date of the data; only its direction and its divergences from price matter. A rising OBV while price moves sideways is read as accumulation ahead of a breakout, a falling OBV as distribution. A single day of very high volume, such as an index rebalance or an earnings day, can move the line for a long time.

For more information, see the following sources:

- TA-Lib: OBV, the reference implementation ([https://ta-lib.org/functions/obv.html](https://ta-lib.org/functions/obv.html){:target="_blank"}).

**Also known as:** OBV, volume momentum.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
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
- If `growth` is set to True, the method calculates the growth of the OBV using the specified `lag`.

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
Calculate the Price Volume Trend (PVT) for a given price series.

The Price Volume Trend is a running total of volume weighted by the period's percentage change in price. On-Balance Volume adds or subtracts the whole volume depending on the direction of the close; the PVT adds only the share of the volume that matches the size of the move, so a small change in price moves the line only a little.

The formula is as follows:

$$
\text{PVT} = \text{Previous PVT} + \frac{\text{Volume} \cdot (\text{Close} - \text{Previous Close})}{\text{Previous Close}}
$$

$$
\text{PVT} = 0 \;\text{on the first date},\;\; \text{which has no previous close}
$$

The level of the PVT has no meaning by itself, since it starts at 0 on the start date; only its direction and its divergences from price matter. A rising PVT confirms an uptrend carried by volume, and a PVT that fails to follow price to a new high warns that the move lacks participation. The line is in shares, so it cannot be compared across stocks.

For more information, see the following sources:

- TA-Lib: PVT, the reference implementation ([https://ta-lib.org/functions/pvt.html](https://ta-lib.org/functions/pvt.html){:target="_blank"}).

**Also known as:** PVT, Price and Volume Trend, Volume Price Trend.

See `breadth_model.get_price_volume_trend` for the references.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
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
- If `growth` is set to True, the method calculates the growth of the PVT using the specified `lag`.

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
Calculate the Accumulation/Distribution Line for a given price series.

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

For more information, see the following sources:

- TA-Lib: AD, the reference implementation ([https://ta-lib.org/functions/ad.html](https://ta-lib.org/functions/ad.html){:target="_blank"}).

**Also known as:** ADL, Chaikin ADL, volume-price trend.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
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
- The Accumulation/Distribution Line equals TA-Lib's AD.
- If `growth` is set to True, the method calculates the growth of the Accumulation/Distribution Line
using the specified `lag`.

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
Calculate the Chaikin Oscillator for a given price series.

The Chaikin Oscillator is a momentum-based indicator that combines price and volume to help identify potential trends and reversals in the market. It is calculated as the difference between the 3-day and 10-day Accumulation/Distribution Line.

The formula is as follows:

$$
\text{Chaikin Oscillator} = \operatorname{EMA}(\text{short-window ADL}) - \operatorname{EMA}(\text{long-window ADL})
$$

For more information, see the following sources:

- TA-Lib: ADOSC, the reference implementation ([https://ta-lib.org/functions/adosc.html](https://ta-lib.org/functions/adosc.html){:target="_blank"}).

**Also known as:** Chaikin oscillator, volume accumulation.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
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
- If `growth` is set to True, the method calculates the growth of the Chaikin Oscillator
using the specified `lag`.

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
Calculate the Chaikin Money Flow (CMF) for a given price series.

The Chaikin Money Flow sums the same Money Flow Volume used by the Accumulation/ Distribution Line over a rolling window and normalizes it by the window's total volume, turning the running (unbounded) Accumulation/Distribution Line into a bounded oscillator. Sustained readings above zero indicate buying pressure (accumulation) is dominating over the window, while sustained readings below zero indicate selling pressure (distribution).

The formula is as follows:

$$
\text{Money Flow Multiplier} = \frac{(\text{Close} - \text{Low}) - (\text{High} - \text{Close})}{\text{High} - \text{Low}}
$$

$$
\text{Money Flow Volume} = \text{Money Flow Multiplier} \cdot \text{Volume}
$$

$$
\text{CMF} = \frac{\operatorname{Sum}(\text{Money Flow Volume},\; \text{window})}{\operatorname{Sum}(\text{Volume},\; \text{window})}
$$

For more information, see the following sources:

- TA-Lib: CMF, the reference implementation ([https://ta-lib.org/functions/cmf.html](https://ta-lib.org/functions/cmf.html){:target="_blank"}).

**Also known as:** CMF, Chaikin Money Flow.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the open, high and low prices are adjusted
for dividends in the same way.
- <u>window (int, optional):</u> Number of periods to sum the Money Flow Volume and
volume over. Defaults to 20.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Chaikin Money Flow.
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

pd.Series or pd.DataFrame: Chaikin Money Flow values, bounded between -1 and 1.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the Chaikin Money Flow for each asset in the Toolkit instance.
- There is no formal journal citation for the Chaikin Money Flow; the standard
textbook treatment is Murphy, J.J. (1999). "Technical Analysis of the Financial
Markets." New York Institute of Finance.
- The Chaikin Money Flow equals TA-Lib's CMF.
- If `growth` is set to True, the method calculates the growth of the Chaikin Money
Flow using the specified `lag`.

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
Calculate the Ease of Movement (EMV) for a given price series.

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

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
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
Volume Analysis of Stock and Bond Markets." Business One Irwin.
- TA-Lib: EMV, the reference implementation ([https://ta-lib.org/functions/emv.html](https://ta-lib.org/functions/emv.html){:target="_blank"}).
- The Ease of Movement equals TA-Lib's EMV with its `volumedivisor` set to `volume_divisor`
(TA-Lib's default is 10,000).
- If `growth` is set to True, the method calculates the growth of the Ease of
Movement using the specified `lag`.

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

## get_negative_volume_index
Calculate the Negative Volume Index (NVI) for a given price series.

The Negative Volume Index is a cumulative index that only updates on days where volume decreases from the prior period, compounding that day's percentage price change onto the running index; on days where volume increases (or stays flat), the index is carried forward unchanged. The premise, per Fosback, is that "smart money" tends to be active on low-volume (quiet) days, so tracking price behaviour specifically on those days isolates informed trading from the noise of high-volume, crowd-driven days.

The formula is as follows:

$$
\operatorname{Index}(t) = \operatorname{Index}(t-1) \cdot \left(1 + \left(\frac{\operatorname{Close}(t)}{\operatorname{Close}(t-1)} - 1\right)\right) \;\text{if Volume}(t) < \operatorname{Volume}(t-1)
$$

$$
\operatorname{Index}(t) = \operatorname{Index}(t-1) \;\text{otherwise}
$$

**Also known as:** NVI, Negative Volume Index.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>start_value (float, optional):</u> The index value to start the series at.
Defaults to 1000.0.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Negative Volume Index.
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

pd.Series or pd.DataFrame: Negative Volume Index values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the Negative Volume Index for each asset in the Toolkit instance.
- Reference: Fosback, N.G. (1976). "Stock Market Logic: A Sophisticated Approach to
Profits on Wall Street." The Institute for Econometric Research.
- TA-Lib: NVI, the reference implementation ([https://ta-lib.org/functions/nvi.html](https://ta-lib.org/functions/nvi.html){:target="_blank"}).
- With the default `start_value` of 1,000, the Negative Volume Index equals TA-Lib's NVI.
- If `growth` is set to True, the method calculates the growth of the Negative Volume
Index using the specified `lag`.

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

toolkit.technicals.get_negative_volume_index().tail(5)
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

## get_positive_volume_index
Calculate the Positive Volume Index (PVI) for a given price series.

The Positive Volume Index mirrors the Negative Volume Index: it is a cumulative index that only updates on days where volume increases from the prior period, compounding that day's percentage price change onto the running index; on days where volume decreases (or stays flat), the index is carried forward unchanged. Per Fosback, the Positive Volume Index isolates price behaviour on high-volume (crowd-driven) days, which is traditionally read as tracking less-informed, sentiment-driven trading.

The formula is as follows:

$$
\operatorname{Index}(t) = \operatorname{Index}(t-1) \cdot \left(1 + \left(\frac{\operatorname{Close}(t)}{\operatorname{Close}(t-1)} - 1\right)\right) \;\text{if Volume}(t) > \operatorname{Volume}(t-1)
$$

$$
\operatorname{Index}(t) = \operatorname{Index}(t-1) \;\text{otherwise}
$$

**Also known as:** PVI, Positive Volume Index.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>start_value (float, optional):</u> The index value to start the series at.
Defaults to 1000.0.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Positive Volume Index.
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

pd.Series or pd.DataFrame: Positive Volume Index values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the Positive Volume Index for each asset in the Toolkit instance.
- Reference: Fosback, N.G. (1976). "Stock Market Logic: A Sophisticated Approach to
Profits on Wall Street." The Institute for Econometric Research.
- TA-Lib: PVI, the reference implementation ([https://ta-lib.org/functions/pvi.html](https://ta-lib.org/functions/pvi.html){:target="_blank"}).
- With the default `start_value` of 1,000, the Positive Volume Index equals TA-Lib's PVI.
- If `growth` is set to True, the method calculates the growth of the Positive Volume
Index using the specified `lag`.

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

toolkit.technicals.get_positive_volume_index().tail(5)
```

Which returns:

| Date       |     SPY |     IWM |
|:-----------|--------:|--------:|
| 2025-12-24 | 368.611 | 308.515 |
| 2025-12-26 | 368.574 | 306.942 |
| 2025-12-29 | 367.26  | 305.061 |
| 2025-12-30 | 367.26  | 305.061 |
| 2025-12-31 | 364.539 | 302.758 |

---

## collect_momentum_indicators
Calculates and collects various momentum indicators based on the provided data.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
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
- If `growth` is set to True, the method calculates the growth of the indicator values
using the specified `lag`.

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

| Date       |   Money Flow Index |   Williams %R |   Aroon Indicator Up |   Aroon Indicator Down |   Commodity Channel Index |   Relative Vigor Index |   Relative Vigor Index Signal Line |       Force Index |   Ultimate Oscillator |   Percentage Price Oscillator |   Detrended Price Oscillator |   Average Directional Index |   Chande Momentum Oscillator |   Ichimoku Conversion Line |   Ichimoku Base Line |   Ichimoku Leading Span A |   Ichimoku Leading Span B |   Stochastic %K |   Stochastic %D |   MACD Line |   MACD Signal Line |   Relative Strength Index |   Stochastic RSI %K |   Stochastic RSI %D |   True Strength Index |   True Strength Index Signal Line |   Balance of Power |   Awesome Oscillator |   Vortex Indicator VI+ |   Vortex Indicator VI- |   Elder Ray Bull Power |   Elder Ray Bear Power |   Rate of Change |   Choppiness Index |   Know Sure Thing |   Know Sure Thing Signal Line |   Coppock Curve |
|:-----------|-------------------:|--------------:|---------------------:|-----------------------:|--------------------------:|-----------------------:|-----------------------------------:|------------------:|----------------------:|------------------------------:|-----------------------------:|----------------------------:|-----------------------------:|---------------------------:|---------------------:|--------------------------:|--------------------------:|----------------:|----------------:|------------:|-------------------:|--------------------------:|--------------------:|--------------------:|----------------------:|----------------------------------:|-------------------:|---------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------:|-------------------:|------------------:|------------------------------:|----------------:|
| 2025-12-17 |            39.7393 |      -98.8222 |              28.5714 |               100      |                 -139.905  |                -0.2262 |                            -0.0758 |      -3.27416e+07 |               44.5331 |                        0.0063 |                       0.0306 |                     24.6712 |                     -20.621  |                    275.43  |              276.008 |                   265.041 |                   250.519 |          1.1778 |          8.6605 |      1.7262 |             3.1596 |                   45.1866 |              0      |              1.2037 |               12.3226 |                           19.7487 |            -0.7013 |               1.2653 |                 0.9211 |                 1.0533 |                -0.1328 |                -4.6371 |          -0.0206 |            49.8427 |            0.3638 |                        0.5107 |          0.0029 |
| 2025-12-18 |            34.4002 |      -75.8192 |              21.4286 |               100      |                 -162.428  |                -0.2832 |                            -0.1659 |      -2.59752e+07 |               50.9808 |                        0.0047 |                      -0.3822 |                     24.4323 |                     -24.9065 |                    272.6   |              276.008 |                   265.041 |                   250.519 |         24.1808 |         14.0381 |      1.2731 |             2.7823 |                   45.9182 |              2.4336 |              2.0149 |                9.3441 |                           17.1476 |            -0.2126 |               0.0099 |                 0.865  |                 1.0802 |                -2.0699 |                -8.7267 |          -0.0239 |            42.7375 |            0.311  |                        0.4834 |         -0.014  |
| 2025-12-19 |            43.3299 |      -68.989  |              14.2857 |                92.8571 |                 -103.239  |                -0.2694 |                            -0.2349 |       5.93141e+06 |               51.5414 |                        0.0037 |                      -0.4186 |                     23.9077 |                     -39.3403 |                    272.6   |              276.008 |                   265.041 |                   250.519 |         31.011  |         18.7898 |      1.0212 |             2.4301 |                   49.0174 |             12.7428 |              5.0588 |                7.6467 |                           14.7724 |             0.3234 |              -1.1188 |                 0.903  |                 1.137  |                -0.8132 |                -5.4969 |          -0.0333 |            41.2482 |            0.2645 |                        0.4504 |         -0.0269 |
| 2025-12-22 |            36.4312 |      -81.4489 |               7.1429 |                85.7143 |                 -104.734  |                -0.2367 |                            -0.2614 |      -7.97981e+06 |               45.7604 |                        0.0022 |                       2.2593 |                     23.4206 |                     -64.5457 |                    272.6   |              276.008 |                   264.954 |                   250.519 |         18.5511 |         24.581  |      0.5976 |             2.0636 |                   44.0573 |              0      |              5.0588 |                4.6682 |                           12.2463 |            -0.5608 |              -2.0902 |                 0.8075 |                 1.2147 |                -0.8978 |                -4.2561 |          -0.0532 |            40.4149 |            0.2055 |                        0.4111 |         -0.0418 |
| 2025-12-23 |            37.2984 |      -69.5725 |               0      |                78.5714 |                  -97.9342 |                -0.205  |                            -0.2501 |      -1.44131e+06 |               49.1967 |                        0.0014 |                       2.3511 |                     23.1943 |                     -51.4169 |                    272.6   |              276.008 |                   265.083 |                   250.519 |         30.4275 |         26.6632 |      0.3694 |             1.7248 |                   47.029  |             15.5285 |              9.4238 |                3.0048 |                            9.9359 |             0.517  |              -2.6623 |                 0.7732 |                 1.2661 |                -1.9284 |                -4.8582 |          -0.0415 |            46.4518 |            0.1522 |                        0.3663 |         -0.0501 |
| 2025-12-24 |            41.6581 |      -51.6561 |               0      |                71.4286 |                  -34.6704 |                -0.1841 |                            -0.2228 |       2.20159e+06 |               54.4448 |                        0.0011 |                       3.0907 |                     22.0179 |                     -32.919  |                    272.6   |              276.008 |                   265.063 |                   250.519 |         48.3439 |         32.4408 |      0.3017 |             1.4402 |                   50.0121 |             38.5457 |             18.0248 |                2.4525 |                            8.0651 |             0.4551 |              -2.8188 |                 0.8892 |                 1.1613 |                 1.0804 |                -2.1383 |          -0.0245 |            53.1324 |            0.1033 |                        0.3168 |         -0.0518 |
| 2025-12-26 |            46.9441 |      -51.1363 |               0      |                64.2857 |                  -25.6932 |                -0.1697 |                            -0.1974 |  735536           |               51.2159 |                        0.0008 |                      -0.6819 |                     20.9256 |                     -27.7033 |                    272.6   |              276.098 |                   264.961 |                   250.519 |         48.8637 |         42.545  |      0.2126 |             1.1946 |                   49.1689 |             34.622  |             29.5654 |                1.7619 |                            6.4893 |            -0.3028 |              -2.1658 |                 0.9091 |                 1.1011 |                 1.1553 |                -1.346  |          -0.0193 |            55.49   |            0.0564 |                        0.2631 |         -0.0522 |
| 2025-12-29 |            48.1203 |      -48.4089 |              35.7143 |                57.1429 |                  -30.567  |                -0.1563 |                            -0.1782 |       1.77189e+06 |               57.3149 |                        0.0006 |                       0.1103 |                     20.0592 |                     -21.8633 |                    270.612 |              276.183 |                   265.068 |                   250.519 |         51.5911 |         49.5995 |      0.169  |             0.9895 |                   49.9666 |             40.0248 |             37.7308 |                1.4002 |                            5.217  |             0.5323 |              -2.0654 |                 0.9316 |                 1.0955 |                 0.2129 |                -1.7901 |          -0.0149 |            54.4742 |            0.0118 |                        0.2104 |         -0.0496 |
| 2025-12-30 |            43.4593 |      -53.5607 |              28.5714 |                50      |                  -35.5283 |                -0.1288 |                            -0.1608 | -464819           |               54.1042 |                        0.0003 |                      -2.3582 |                     19.276  |                     -21.7389 |                    270.612 |              276.183 |                   265.068 |                   250.519 |         46.4393 |         48.9647 |      0.0788 |             0.8074 |                   48.4209 |             29.5554 |             34.7341 |                0.6843 |                            4.0838 |             0.15   |              -1.9448 |                 0.9145 |                 1.1096 |                 0.0857 |                -1.708  |          -0.0148 |            53.5704 |           -0.0182 |                        0.1612 |         -0.0465 |
| 2025-12-31 |            38.2003 |      -62.8029 |              21.4286 |                42.8571 |                  -56.9135 |                -0.0887 |                            -0.1381 |      -4.82706e+06 |               46.4079 |                       -0.0003 |                      -1.5169 |                     18.7175 |                     -37.4456 |                    270.248 |              276.821 |                   265.6   |                   250.867 |         37.1971 |         45.0758 |     -0.0897 |             0.628  |                   45.6902 |             12.0098 |             27.1967 |               -0.6702 |                            2.8953 |            -0.6218 |              -1.6049 |                 0.9113 |                 1.1148 |                -0.0091 |                -1.9324 |          -0.0248 |            52.5944 |           -0.0452 |                        0.1157 |         -0.0431 |

---

## get_money_flow_index
Calculate the Money Flow Index (MFI) for a given price series.

The Money Flow Index is a momentum indicator that measures the strength and direction of money flowing in and out of a security by considering both price and volume.

The formula is as follows:

$$
\text{MFI} = 100 - \frac{100}{1 + \frac{\text{positive\_money\_flow}}{\text{negative\_money\_flow}}}
$$

For more information, see the following sources:

- TA-Lib: MFI, the reference implementation ([https://ta-lib.org/functions/mfi.html](https://ta-lib.org/functions/mfi.html){:target="_blank"}).

**Also known as:** MFI, volume-weighted RSI.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
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
- The MFI equals TA-Lib's MFI.
- If `growth` is set to True, the method calculates the growth of the indicator values
using the specified `lag`.

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
Calculate the Williams Percent R (Williams %R) for a given price series.

The Williams %R is a momentum indicator that measures the level of the close price relative to the high-low range over a certain number of periods.

The formula is as follows:

$$
\text{Williams}\; \%R = \frac{\text{Highest High} - \text{Close}}{\text{Highest High} - \text{Lowest Low}} \cdot - 100
$$

For more information, see the following sources:

- TA-Lib: WILLR, the reference implementation ([https://ta-lib.org/functions/willr.html](https://ta-lib.org/functions/willr.html){:target="_blank"}).

**Also known as:** Williams percent R, overbought oversold oscillator.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
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
- Williams %R equals TA-Lib's WILLR.
- If `growth` is set to True, the method calculates the growth of the indicator values
using the specified `lag`.

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
Calculate the Aroon Indicator for a given price series.

The Aroon Indicator is an oscillator that measures the strength of a trend and the likelihood of its continuation or reversal.

The formula is as follows:

$$
\text{Aroon Up} = \frac{(\text{Number of periods}) - (\text{Number of periods since highest high})}{\text{Number of periods}} \cdot 100
$$

For more information, see the following sources:

- TA-Lib: AROON, the reference implementation ([https://ta-lib.org/functions/aroon.html](https://ta-lib.org/functions/aroon.html){:target="_blank"}).

**Also known as:** Aroon Up, Aroon Down, trend strength.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
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
Aroon Indicator values for the upward and downward trends.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the Aroon Indicator values for each asset in the Toolkit instance.
- Aroon Up and Aroon Down equal TA-Lib's AROON.
- If `growth` is set to True, the method calculates the growth of the indicator values
using the specified `lag`.

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

| Date       |   Aroon Down |   Aroon Up |
|:-----------|-------------:|-----------:|
| 2025-12-26 |       0      |   100      |
| 2025-12-28 |       0      |    92.8571 |
| 2025-12-29 |       0      |    85.7143 |
| 2025-12-30 |      14.2857 |    78.5714 |
| 2025-12-31 |     100      |    71.4286 |

---

## get_commodity_channel_index
Calculate the Commodity Channel Index (CCI) for a given price series.

The Commodity Channel Index is an oscillator that measures the current price level relative to an average price level over a specified period.

The formula is as follows:

$$
\text{CCI} = \frac{\text{Typical Price} - \operatorname{SMA}(\text{Typical Price})}{\text{constant} \cdot \text{Mean Deviation}}
$$

For more information, see the following sources:

- TA-Lib: CCI, the reference implementation ([https://ta-lib.org/functions/cci.html](https://ta-lib.org/functions/cci.html){:target="_blank"}).

**Also known as:** CCI, cyclical trend indicator.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
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
- With the default `constant` of 0.015, the CCI equals TA-Lib's CCI.
- If `growth` is set to True, the method calculates the growth of the indicator values
using the specified `lag`.

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
Calculate the Relative Vigor Index (RVI) for a given price series.

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

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
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
- If `growth` is set to True, the method calculates the growth of the indicator values
using the specified `lag`.

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
Calculate the Force Index for a given price series.

The Force Index is an indicator that measures the strength behind price movements.

The formula is as follows:

$$
\text{Raw Force Index} = (\text{Close} - \operatorname{Close}(1)) \cdot \text{Volume}
$$

$$
\text{Force Index} = \operatorname{EMA}(\text{Raw Force Index},\; \text{window})
$$

For more information, see the following sources:

- TA-Lib: EFI, the reference implementation ([https://ta-lib.org/functions/efi.html](https://ta-lib.org/functions/efi.html){:target="_blank"}).

**Also known as:** FI, Elder's Force Index.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column in the historical data that represents
the closing prices. Defaults to "Adj Close".
- <u>window (int, optional):</u> The number of periods of the EMA that smooths the raw
Force Index. Defaults to 13, Elder's setting for the trend (2 is his setting
for timing entries).
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

pd.Series or pd.DataFrame: Force Index values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the Force Index values for each asset in the Toolkit instance.
- The Force Index equals TA-Lib's EFI.
- If `growth` is set to True, the method calculates the growth of the indicator values
using the specified `lag`.

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
Calculate the Ultimate Oscillator for a given price series.

The Ultimate Oscillator is a momentum oscillator that combines short-term, mid-term, and long-term price momentum into a single value.

The formula is as follows:

$$
\operatorname{Average}(i) = \frac{\operatorname{Sum}(\text{Buying Pressure},\; \text{window}_{i})}{\operatorname{Sum}(\text{True Range},\; \text{window}_{i})}
$$

$$
\text{Ultimate Oscillator} = \frac{100 \cdot \left[(4 \cdot \text{Average}_{1}) + (2 \cdot \text{Average}_{2}) + \text{Average}_{3}\right]}{7}
$$

For more information, see the following sources:

- TA-Lib: ULTOSC, the reference implementation ([https://ta-lib.org/functions/ultosc.html](https://ta-lib.org/functions/ultosc.html){:target="_blank"}).

**Also known as:** UO, ultimate momentum oscillator. See `momentum_model.get_ultimate_oscillator` for the Buying Pressure and True Range definitions.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
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
- The Ultimate Oscillator equals TA-Lib's ULTOSC. The first period counts with its High —
Low range and its close minus its low, so the oscillator starts on period `window_3`, one
period before TA-Lib's.
- If `growth` is set to True, the method calculates the growth of the indicator values
using the specified `lag`.

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

## get_percentage_price_oscillator
Calculate the Percentage Price Oscillator (PPO) for a given price series.

The Percentage Price Oscillator (PPO) is a momentum oscillator that measures the difference between two moving averages as a percentage of the longer moving average.

The formula is as follows:

$$
\text{PPO} = \frac{\text{Short-term EMA} - \text{Long-term EMA}}{\text{Long-term EMA}}
$$

The PPO is the MACD line as a percentage of the long EMA, so unlike the MACD its level can be compared across stocks and over long periods. The usual signal line is the 9-period EMA of the PPO; it is not returned here and can be calculated from the result, for example with `get_exponential_moving_average` of the `overlap_model`.

For more information, see the following sources:

- TA-Lib: PPO, the reference implementation ([https://ta-lib.org/functions/ppo.html](https://ta-lib.org/functions/ppo.html){:target="_blank"}).

**Also known as:** PPO, price oscillator.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column in the historical data that represents
the closing prices. Defaults to "Adj Close".
- <u>short_window (int, optional):</u> The number of periods for the short-term moving average.
Defaults to 12, as for MACD.
- <u>long_window (int, optional):</u> The number of periods for the long-term moving average.
Defaults to 26, as for MACD.
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

pd.Series or pd.DataFrame: Percentage Price Oscillator (PPO) values as a decimal
(0.02 is 2%).

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the PPO values for each asset in the Toolkit instance.
- The PPO is a decimal and equals TA-Lib's PPO with the EMA (`matype=1`) divided by 100,
since TA-Lib's PPO is in percent.
- If `growth` is set to True, the method calculates the growth of the indicator values
using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["^STOXX50E", "^GSPC"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_percentage_price_oscillator().tail(5)
```

Which returns:

| Date       |   ^STOXX50E |   ^GSPC |   Benchmark |
|:-----------|------------:|--------:|------------:|
| 2025-12-24 |    nan      |  0.0045 |      0.0048 |
| 2025-12-26 |    nan      |  0.0051 |      0.0054 |
| 2025-12-29 |      0.0048 |  0.0052 |      0.0055 |
| 2025-12-30 |      0.0054 |  0.0051 |      0.0055 |
| 2025-12-31 |    nan      |  0.0044 |      0.0048 |

---

## get_percentage_volume_oscillator
Calculate the Percentage Volume Oscillator (PVO) for a given volume series.

The Percentage Volume Oscillator is the Percentage Price Oscillator applied to volume: the difference between a short-term and a long-term EMA of volume as a share of the long-term EMA, with a signal line and a histogram as for the MACD.

The formula is as follows:

$$
\text{PVO} = \frac{\operatorname{EMA}(\text{Volume},\; \text{short\_window}) - \operatorname{EMA}(\text{Volume},\; \text{long\_window})}{\operatorname{EMA}(\text{Volume},\; \text{long\_window})}
$$

$$
\text{Signal Line} = \operatorname{EMA}(\text{PVO},\; \text{signal\_window})
$$

$$
\text{Histogram} = \text{PVO} - \text{Signal Line}
$$

A positive PVO means recent volume runs above its longer-term average, which gives weight to a breakout or a trend in price; a PVO below zero in a rising market says the move happens on thinning volume. Because it is a share of the average volume, the PVO can be compared across stocks whatever the number of shares they trade. It says nothing about the direction of price.

For more information, see the following sources:

- TA-Lib: PVO, the reference implementation ([https://ta-lib.org/functions/pvo.html](https://ta-lib.org/functions/pvo.html){:target="_blank"}).

**Also known as:** PVO, volume oscillator. See `momentum_model.get_percentage_volume_oscillator` for the references.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
- <u>short_window (int, optional):</u> The number of periods for the short-term moving average.
Defaults to 12, as for the PPO and MACD.
- <u>long_window (int, optional):</u> The number of periods for the long-term moving average.
Defaults to 26, as for the PPO and MACD.
- <u>signal_window (int, optional):</u> The number of periods for the signal line.
Defaults to 9.
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
volume. It equals TA-Lib's PVO (with its default EMA) divided by 100: TA-Lib's PVO is in
percent, returns 0 without volume and has no signal line or histogram.
- If `growth` is set to True, the method calculates the growth of the indicator values
using the specified `lag`.

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
Calculate the Detrended Price Oscillator (DPO) for a given price series.

The Detrended Price Oscillator (DPO) is an indicator that helps identify short-term cycles by removing longer-term trends from prices.

The formula is as follows:

$$
\text{Displacement} = \left\lfloor \frac{\text{Number of Periods}}{2} \right\rfloor + 1
$$

$$
\text{DPO} = \operatorname{Close}(t - \text{Displacement}) - \operatorname{SMA}(\text{Close},\; \text{Number of Periods}) (t)
$$

For more information, see the following sources:

- TA-Lib: DPO, the reference implementation ([https://ta-lib.org/functions/dpo.html](https://ta-lib.org/functions/dpo.html){:target="_blank"}).

**Also known as:** DPO, detrended price oscillator. Note the moving average itself is not shifted - only the close price used for the comparison is looked up further back in time; see `momentum_model.get_detrended_price_oscillator` for the full explanation.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
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
- The DPO equals TA-Lib's DPO.
- If `growth` is set to True, the method calculates the growth of the indicator values
using the specified `lag`.

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
Calculate the Average Directional Index (ADX) for a given price series.

The Average Directional Index (ADX) is an indicator that measures the strength of a trend, whether it's an uptrend or a downtrend.

The formula is as follows:

$$
\text{ADX} = \text{Wilder's Smoothed Moving Average of DX},\;\; \text{where}\;\; \text{DX} = \frac{100 \cdot \left|\text{+DI} - \text{-DI}\right|}{\text{+DI} + \text{-DI}}
$$

The ADX measures trend strength, not direction: a reading above about 25 is usually taken as a trending market and below 20 as a range, whether prices are rising or falling. Traders combine it with the +DI and -DI lines it is built from, which this method does not return, or with the price itself, to know the direction. With Wilder's smoothing it reacts slowly and needs a few times the window of history before its values settle.

For more information, see the following sources:

- TA-Lib: ADX, the reference implementation ([https://ta-lib.org/functions/adx.html](https://ta-lib.org/functions/adx.html){:target="_blank"}).

**Also known as:** ADX, trend strength indicator. See `momentum_model.get_average_directional_index` for the full formula, which uses Wilder's smoothing (not a plain SMA) throughout.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column in the historical data that represents
Defaults to "Adj Close", in which case the open, high and low prices are adjusted
for dividends in the same way.
- <u>window (int, optional):</u> The number of periods to consider for the ADX calculation.
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

pd.DataFrame or pd.Series: Average Directional Index (ADX) values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the ADX values for each asset in the Toolkit instance.
- Wilder's smoothing is seeded with the average of the first `window` values, while TA-Lib's
ADX seeds its running sums with `window` - 1 values, so the first values differ from
TA-Lib's until the two converge (within 0.01% after about 120 periods with the default
window).
- If `growth` is set to True, the method calculates the growth of the indicator values
using the specified `lag`.

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

## get_chande_momentum_oscillator
Calculate the Chande Momentum Oscillator (CMO) for a given price series.

The Chande Momentum Oscillator is an indicator that measures the momentum of a price series and identifies overbought and oversold conditions.

The formula is as follows:

$$
\text{CMO} = \frac{100 \cdot ((\text{Sum of Upward Change}) - (\text{Sum of Downward Change}))}{(\text{Sum of Upward Change}) + (\text{Sum of Downward Change})},\;\; \text{bounded between -100 and 100}
$$

For more information, see the following sources:

- TA-Lib: CMO, the reference implementation ([https://ta-lib.org/functions/cmo.html](https://ta-lib.org/functions/cmo.html){:target="_blank"}).

**Also known as:** CMO, Chande momentum.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column in the historical data that represents
the closing prices. Defaults to "Adj Close".
- <u>window (int, optional):</u> The number of periods to consider for the CMO calculation.
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

pd.Series or pd.DataFrame: Chande Momentum Oscillator values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the Chande Momentum Oscillator values for each asset in the Toolkit instance.
- The gains and losses are summed over the window, as Chande defines the CMO and as on
StockCharts. TA-Lib's CMO smooths them with Wilder's method instead, as in its RSI, so the
two differ throughout (by up to about 55 points on daily data).
- If `growth` is set to True, the method calculates the growth of the indicator values
using the specified `lag`.

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
Calculate the Ichimoku Cloud indicator for a given price series.

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

For more information, see the following sources:

- TA-Lib: ICHIMOKU, the reference implementation ([https://ta-lib.org/functions/ichimoku.html](https://ta-lib.org/functions/ichimoku.html){:target="_blank"}).

**Also known as:** Ichimoku Kinko Hyo, cloud indicator. The default windows (9, 26, 52) are Goichi Hosoda's original values, both leading spans are conventionally displaced forward by the base (Kijun-sen) period.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
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
- The Conversion Line and Base Line equal TA-Lib's ICHIMOKU, and so do the leading spans
`base_window` periods earlier: TA-Lib places them on the period they are calculated on
instead of displacing them forward, and starts every line on the `lead_span_b_window`-th
period.
- If `growth` is set to True, the method calculates the growth of the indicator values
using the specified `lag`.
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
Calculate the Stochastic Oscillator indicator for a given price series.

The Stochastic Oscillator is a momentum indicator that shows the location of the close relative to the high-low range over a set number of periods. It consists of the %K line (fast) and the %D line (slow).

The formula is as follows:

$$
\%K = 100 \cdot \frac{\text{Close} - \text{Lowest Low}}{\text{Highest High} - \text{Lowest Low}}
$$

$$
\%D = \operatorname{SMA}(\%K,\; \text{smooth\_window})
$$

For more information, see the following sources:

- TA-Lib: STOCHF, the reference implementation ([https://ta-lib.org/functions/stochf.html](https://ta-lib.org/functions/stochf.html){:target="_blank"}).

**Also known as:** stochastic oscillator, percent K, percent D.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the open, high and low prices are adjusted
for dividends in the same way.
- <u>window (int, optional):</u> The number of periods to consider for the %K line calculation.
Defaults to 14.
- <u>smooth_window (int, optional):</u> The number of periods used to smooth the %K line
into the %D signal line. Defaults to 3.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the %K and %D values.
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

pd.Series or pd.DataFrame: Stochastic Oscillator (%K and %D) values.

**Raises:**

ValueError: If the specified `period` is not one of the valid options.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the Stochastic Oscillator values for each asset in the Toolkit instance.
- %K and %D equal TA-Lib's STOCHF (the fast stochastic) with `fastd_period` set to
`smooth_window` and a simple moving average (`fastd_matype=0`), which TA-Lib's STOCH gives
with a `slowk_period` of 1. TA-Lib starts %K on the first %D.
- If `growth` is set to True, the method calculates the growth of the %K and %D values
using the specified `lag`.

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
Calculate the Moving Average Convergence Divergence (MACD) indicator for a given price series.

The Moving Average Convergence Divergence (MACD) is a trend-following momentum indicator that shows the relationship between two moving averages of a security's price. It consists of the MACD line and its signal line; their difference is the MACD histogram.

The formula is as follows:

$$
\text{MACD Line} = \operatorname{EMA}(\text{Close},\; \text{short\_window}) - \operatorname{EMA}(\text{Close},\; \text{long\_window})
$$

$$
\text{Signal Line} = \operatorname{EMA}(\text{MACD Line},\; \text{signal\_window})
$$

The MACD line crossing its signal line is the usual trigger, and the MACD crossing zero means the short average has crossed the long one. Because the MACD is a price difference, its level scales with the share price and cannot be compared across stocks; the Percentage Price Oscillator divides by the long average for that. Both lines lag price, so crossovers come late in fast reversals.

For more information, see the following sources:

- TA-Lib: MACD, the reference implementation ([https://ta-lib.org/functions/macd.html](https://ta-lib.org/functions/macd.html){:target="_blank"}).

**Also known as:** MACD, momentum indicator.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>short_window (int, optional):</u> The number of periods for the shorter moving average.
Defaults to 12.
- <u>long_window (int, optional):</u> The number of periods for the longer moving average.
Defaults to 26.
- <u>signal_window (int, optional):</u> The number of periods for the signal line.
Defaults to 9.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the MACD and signal values.
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
MACD line and signal line values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the MACD and signal line values for each asset in the Toolkit instance.
- TA-Lib's MACD starts the short EMA on the same period as the long EMA and shows the MACD
line from the first signal value, so the first values differ from TA-Lib's until the two
converge (within 0.01% after about 85 periods with the default windows).
- If `growth` is set to True, the method calculates the growth of the MACD and signal values
using the specified `lag`.

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

| Date       |   MACD Line |   Signal Line |
|:-----------|------------:|--------------:|
| 2025-12-24 |     -3.02   |       -4.8167 |
| 2025-12-26 |     -2.5054 |       -4.3544 |
| 2025-12-29 |     -2.122  |       -3.908  |
| 2025-12-30 |     -1.7673 |       -3.4798 |
| 2025-12-31 |     -1.7752 |       -3.1389 |

---

## get_relative_strength_index
Calculate the Relative Strength Index (RSI) indicator for a given price series.

The Relative Strength Index (RSI) is a momentum oscillator that measures the speed and change of price movements. It ranges from 0 to 100 and is used to identify overbought or oversold conditions in an asset's price.

The formula is as follows:

$$
\text{RSI} = 100 - \frac{100}{1 + \text{RS}}
$$

Readings above 70 are conventionally read as overbought and below 30 as oversold, but in a strong trend the RSI can stay above 70 or below 30 for weeks, so a crossing is not a signal on its own. Practitioners look more at divergences, a new price high with a lower RSI high, and at the 50 line as a trend filter. The value depends on the window: a shorter window swings more and reaches the extremes more often.

For more information, see the following sources:

- TA-Lib: RSI, the reference implementation ([https://ta-lib.org/functions/rsi.html](https://ta-lib.org/functions/rsi.html){:target="_blank"}).

**Also known as:** RSI, momentum oscillator, overbought, oversold.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int, optional):</u> The number of periods for RSI calculation. Defaults to 14.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the RSI.
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
Relative Strength Index (RSI) values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates the
RSI for each asset in the Toolkit instance.
- The RSI equals TA-Lib's RSI.
- If `growth` is set to True, the method calculates the growth of the RSI
using the specified `lag`.

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

## get_stochastic_relative_strength_index
Calculate the Stochastic RSI for a given price series.

The Stochastic RSI applies the Stochastic Oscillator to the Relative Strength Index instead of to price: it shows where the current RSI sits within its own high-low range over the last `stochastic_window` periods. Chande and Kroll (1994, "The New Technical Trader") designed it because the RSI can spend long stretches between 30 and 70 without reaching either extreme; the Stochastic RSI reaches 0 and 100 far more often.

The formula is as follows:

$$
\text{RSI} = \text{Relative Strength Index}(\text{Close},\; \text{window}),\;\; \text{with Wilder's smoothing}
$$

$$
\%K = \frac{100 \cdot (\text{RSI} - \text{Lowest RSI})}{\text{Highest RSI} - \text{Lowest RSI}},\;\; \text{over the last stochastic\_window RSI values}
$$

$$
\%D = \operatorname{SMA}(\%K,\; \text{smooth\_window})
$$

The defaults follow Chande and Kroll's definition, a 14-period stochastic of a 14-period RSI, which StockCharts and TradingView use as well. StockCharts shows this %K on a scale of 0 to 1; TradingView smooths it over 3 periods, so its %K is the %D here. TA-Lib's STOCHRSI defaults to a 5-period stochastic instead (timeperiod 14, fastk_period 5 and fastd_period 3 with a simple average): pass stochastic_window=5 for its %K and %D. A %K of 100 means the RSI is at its highest of the window, not that the price is overbought, so the readings above 80 and below 20 come and go quickly and are mostly read together with the trend.

For more information, see the following sources:

- TA-Lib: STOCHRSI, the reference implementation ([https://ta-lib.org/functions/stochrsi.html](https://ta-lib.org/functions/stochrsi.html){:target="_blank"}).

**Also known as:** StochRSI, Stoch RSI.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int, optional):</u> The number of periods of the RSI. Defaults to 14.
- <u>stochastic_window (int, optional):</u> The number of periods of RSI values whose high-low
range gives %K. Defaults to 14.
- <u>smooth_window (int, optional):</u> The number of periods used to smooth %K into the %D
signal line. Defaults to 3.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the %K and %D values.
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

pd.Series or pd.DataFrame: Stochastic RSI %K and %D values, between 0 and 100.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the Stochastic RSI for each asset in the Toolkit instance.
- The RSI is seeded with a simple average of its first `window` changes, as Wilder and
TA-Lib do, so %K starts `window` + `stochastic_window` - 1 periods after the first
price and %D `smooth_window` - 1 periods later. TA-Lib starts both on the first %D,
with the same values from there.
- An RSI that did not move over the stochastic window has no range, which leaves %K
missing (TA-Lib sets it to 0).
- With `fastk_period` set to `stochastic_window`, `fastd_period` to `smooth_window` and a
simple moving average (`fastd_matype=0`), %K and %D equal TA-Lib's STOCHRSI.
- If `growth` is set to True, the method calculates the growth of the %K and %D values
using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["NVDA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2024-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_stochastic_relative_strength_index().xs("NVDA", level=1, axis="columns").tail(5)
```

Which returns:

| Date       |   Stochastic RSI %D |   Stochastic RSI %K |
|:-----------|--------------------:|--------------------:|
| 2025-12-24 |             98.8179 |             96.4537 |
| 2025-12-26 |             98.8179 |            100      |
| 2025-12-29 |             94.1715 |             86.0606 |
| 2025-12-30 |             89.3317 |             81.9345 |
| 2025-12-31 |             81.1377 |             75.418  |

---

## get_true_strength_index
Calculate the True Strength Index (TSI) for a given price series.

The True Strength Index of Blau (1995, "Momentum, Direction, and Divergence") smooths the one-period price change twice with Exponential Moving Averages and divides it by the same double smoothing of the absolute change. The double smoothing filters out noise while lagging less than a single long average, and the division bounds the result between -100 (every change down) and +100 (every change up).

The formula is as follows:

$$
\text{Momentum} = \operatorname{Close}(t) - \operatorname{Close}(t - 1)
$$

$$
\text{TSI} = \frac{100 \cdot \operatorname{EMA}(\operatorname{EMA}(\text{Momentum},\; \text{long\_window}),\; \text{short\_window})}{\operatorname{EMA}(\operatorname{EMA}(\left|\text{Momentum}\right|,\; \text{long\_window}),\; \text{short\_window})}
$$

$$
\text{Signal Line} = \operatorname{EMA}(\text{TSI},\; \text{signal\_window})
$$

Blau smooths over 25 and then 13 periods; the 7-period signal line is the one StockCharts uses. The TSI crossing zero means the smoothed momentum has turned, crossing its signal line is the faster trigger, and readings beyond about +25 or -25 are read as overbought or oversold. Like the RSI it is on a scale of -100 to 100 rather than a decimal.

For more information, see the following sources:

- TA-Lib: TSI, the reference implementation ([https://ta-lib.org/functions/tsi.html](https://ta-lib.org/functions/tsi.html){:target="_blank"}).

**Also known as:** TSI, double smoothed momentum.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>long_window (int, optional):</u> The number of periods of the first EMA of the price
change. Defaults to 25.
- <u>short_window (int, optional):</u> The number of periods of the second EMA. Defaults to 13.
- <u>signal_window (int, optional):</u> The number of periods of the EMA of the TSI that gives
the signal line. Defaults to 7.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the TSI and signal line.
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

pd.Series or pd.DataFrame: True Strength Index and Signal Line values, between -100
and 100.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the True Strength Index for each asset in the Toolkit instance.
- Every EMA is seeded with the simple average of its first values and is missing
before it, as in TA-Lib and StockCharts, so the TSI starts `long_window` +
`short_window` - 1 periods after the first price and the signal line
`signal_window` - 1 periods later.
- A stretch without any price change leaves the TSI missing.
- The TSI equals TA-Lib's TSI, which has no signal line.
- If `growth` is set to True, the method calculates the growth of the TSI and signal
line using the specified `lag`.

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
Calculate the Balance of Power (BOP) indicator for a given price series.

The Balance of Power (BOP) indicator measures the strength of buyers versus sellers in the market. It relates the price change to the change in the asset's trading range.

The formula is as follows:

$$
\text{BOP} = \frac{\text{Close} - \text{Open}}{\text{High} - \text{Low}}
$$

For more information, see the following sources:

- TA-Lib: BOP, the reference implementation ([https://ta-lib.org/functions/bop.html](https://ta-lib.org/functions/bop.html){:target="_blank"}).

**Also known as:** BOP, bull bear power.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
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
- The BOP equals TA-Lib's BOP.
- If `growth` is set to True, the method calculates the growth of the BOP
using the specified `lag`.

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

## get_awesome_oscillator
Calculate the Awesome Oscillator (AO) for a given price series.

The Awesome Oscillator measures market momentum by comparing a short-term and a long-term Simple Moving Average of the median price (the midpoint of each period's high and low, rather than the closing price). It was developed by Bill Williams as part of his broader "Trading Chaos" collection of momentum indicators.

The formula is as follows:

$$
\text{Median Price} = \frac{\text{High} + \text{Low}}{2}
$$

$$
\text{AO} = \operatorname{SMA}(\text{Median Price},\; \text{short\_window}) - \operatorname{SMA}(\text{Median Price},\; \text{long\_window})
$$

For more information, see the following sources:

- TA-Lib: AO, the reference implementation ([https://ta-lib.org/functions/ao.html](https://ta-lib.org/functions/ao.html){:target="_blank"}).

**Also known as:** AO, Bill Williams Awesome Oscillator.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>short_window (int, optional):</u> The number of periods for the short-term SMA of the
median price. Defaults to 5.
- <u>long_window (int, optional):</u> The number of periods for the long-term SMA of the
median price. Defaults to 34.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the AO.
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

pd.Series or pd.DataFrame: Awesome Oscillator (AO) values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the AO for each asset in the Toolkit instance.
- There is no academic journal citation for the Awesome Oscillator. Like most of Bill
Williams' indicators, it is a practitioner-developed tool rather than one derived from
a published financial paper. The standard textbook source is Williams, B. (1995).
"Trading Chaos: Applying Expert Techniques to Maximize Your Profit." Wiley.
- A cross of the AO above zero occurs exactly when the short-window SMA of the median
price crosses above the long-window SMA, and vice versa for a cross below zero.
- The AO equals TA-Lib's AO.
- If `growth` is set to True, the method calculates the growth of the AO
using the specified `lag`.

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
Calculate the Vortex Indicator for a given price series.

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

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
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
of Stocks & Commodities, 28(1), 20-25.
- TA-Lib: VORTEX, the reference implementation ([https://ta-lib.org/functions/vortex.html](https://ta-lib.org/functions/vortex.html){:target="_blank"}).
- VI+ and VI- equal TA-Lib's VORTEX.
- If `growth` is set to True, the method calculates the growth of the VI+ and VI-
using the specified `lag`.

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
Calculate the Elder Ray Index (Bull Power and Bear Power) for a given price series.

The Elder Ray Index measures buying and selling pressure in the market relative to a trend baseline (an Exponential Moving Average of the closing price). Bull Power captures how far the high extends above the EMA (buying pressure), while Bear Power captures how far the low extends below the EMA (selling pressure).

The formula is as follows:

$$
\text{Bull Power} = \text{High} - \operatorname{EMA}(\text{Close},\; \text{window})
$$

$$
\text{Bear Power} = \text{Low} - \operatorname{EMA}(\text{Close},\; \text{window})
$$

**Also known as:** Elder Ray, Bull Power, Bear Power.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
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
- TA-Lib: ERI, the reference implementation ([https://ta-lib.org/functions/eri.html](https://ta-lib.org/functions/eri.html){:target="_blank"}).
- Bull Power and Bear Power equal TA-Lib's ERI.
- If `growth` is set to True, the method calculates the growth of the Bull and Bear Power
using the specified `lag`.

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
Calculate the Rate of Change (ROC) for a given price series.

The Rate of Change is a pure momentum oscillator that measures the percentage change in price between the current period and the price a fixed number of periods ago. It oscillates around zero: positive values indicate price is higher than `window` periods ago (upward momentum), while negative values indicate price is lower (downward momentum).

The formula is as follows:

$$
\text{ROC} = \frac{\operatorname{Close}(t)}{\operatorname{Close}(t - \text{window})} - 1
$$

**Also known as:** ROC, Price Rate of Change, momentum.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int, optional):</u> Number of periods to look back for the rate of change
calculation. Defaults to 12.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Rate of Change.
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

pd.Series or pd.DataFrame: Rate of Change values as a decimal (0.05 is 5%).

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the Rate of Change for each asset in the Toolkit instance.
- Reference: Murphy, J.J. (1999). "Technical Analysis of the Financial Markets." New
York Institute of Finance.
- TA-Lib: ROCP, the reference implementation ([https://ta-lib.org/functions/rocp.html](https://ta-lib.org/functions/rocp.html){:target="_blank"}).
- The Rate of Change is a decimal and equals TA-Lib's ROCP; TA-Lib's ROC is the same in
percent.
- If `growth` is set to True, the method calculates the growth of the Rate of Change
using the specified `lag`.

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
Calculate the Choppiness Index (CHOP) for a given price series.

The Choppiness Index quantifies whether the market is trending or moving sideways ("choppy") by comparing the sum of True Range over the window (a measure of the total price path travelled) to the net range the price actually covered over that same window (the distance between the highest high and the lowest low). When price travels a long, winding path but ends up covering little net ground, the index is high (near 100), signalling a choppy, range-bound market. When price travels efficiently in one direction, the index is low (near 0), signalling a trending market.

The formula is as follows:

$$
\text{CHOP} = \frac{100 \cdot \log_{10}\left(\frac{\operatorname{Sum}(\text{True Range},\; \text{window})}{\max(\text{High},\; \text{window}) - \min(\text{Low},\; \text{window})}\right)}{\log_{10}(\text{window})}
$$

For more information, see the following sources:

- TA-Lib: CHOP, the reference implementation ([https://ta-lib.org/functions/chop.html](https://ta-lib.org/functions/chop.html){:target="_blank"}).

**Also known as:** CHOP, Choppiness Index.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the open, high and low prices are adjusted
for dividends in the same way.
- <u>window (int, optional):</u> Number of periods to consider for the Choppiness Index
calculation. Defaults to 14.
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
- The Choppiness Index equals TA-Lib's CHOP. The first period counts with its High — Low
range, so the index starts on period `window`, one period before TA-Lib's.
- If `growth` is set to True, the method calculates the growth of the Choppiness
Index using the specified `lag`.

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

## get_know_sure_thing
Calculate the Know Sure Thing (KST) for a given price series.

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

**Also known as:** KST, Pring's Know Sure Thing, Summed Rate of Change.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
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
- Reference: Pring, M.J. (1992). "The Know Sure Thing (KST)." Technical Analysis of
Stocks & Commodities, 10(6).
- TA-Lib: KST, the reference implementation ([https://ta-lib.org/functions/kst.html](https://ta-lib.org/functions/kst.html){:target="_blank"}).
- The KST and Signal Line are decimals and equal TA-Lib's KST divided by 100, since TA-Lib's
KST is in percent. TA-Lib starts the KST on the first signal value.
- If `growth` is set to True, the method calculates the growth of the KST and Signal
Line using the specified `lag`.

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
Calculate the Coppock Curve for a given price series.

The Coppock Curve is a long-term momentum indicator that Edwin Coppock designed for monthly closes of a stock index, to time buying after a bear market (Coppock, 1962, "Practical Relative Strength Charting", Trendex Research Group, first presented in Barron's). He took the 11 and 14 months from the time an Episcopal bishop told him mourning takes, as the time investors need to get over a loss.

The formula is as follows:

$$
\text{Coppock Curve} = \operatorname{WMA}(\operatorname{ROC}(\text{Close},\; \text{long\_roc\_window}) + \operatorname{ROC}(\text{Close},\; \text{short\_roc\_window}),\; \text{wma\_window})
$$

$$
\operatorname{ROC}(\text{Close},\; n) = \frac{\operatorname{Close}(t)}{\operatorname{Close}(t - n)} - 1
$$

with WMA the linearly Weighted Moving Average, so the defaults give WMA10(ROC14 + ROC11). The windows count periods of the chosen `period`: the curve as Coppock defined it is period="monthly", the default "daily" applies the same windows to days, as the other technical indicators do. The classic signal is the curve turning up while below zero; Coppock did not use it for sell signals. The Rates of Change are decimals, so the curve is a weighted sum of decimal returns (0.30 where charting platforms show 30).

For more information, see the following sources:

- TA-Lib: COPPOCK, the reference implementation ([https://ta-lib.org/functions/coppock.html](https://ta-lib.org/functions/coppock.html){:target="_blank"}).

**Also known as:** Coppock Indicator, Coppock Guide.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
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
- The Coppock Curve is a decimal and equals TA-Lib's COPPOCK divided by 100, since TA-Lib's
is in percent.
- If `growth` is set to True, the method calculates the growth of the Coppock Curve
using the specified `lag`.

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

## collect_overlap_indicators
Calculates and collects various overlap-based indicators based on the provided data.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
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
- If `growth` is set to True, the method calculates the growth of the indicator values
using the specified `lag`.

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

| Date       |   Simple Moving Average (SMA) |   Exponential Moving Average (EMA) |   Double Exponential Moving Average (DEMA) |   TRIX |   Triangular Moving Average |   Weighted Moving Average (WMA) |   Hull Moving Average (HMA) |   Kaufman Adaptive Moving Average (KAMA) |   Volume Weighted Average Price (VWAP) |   Parabolic SAR |   Pivot Point |   Pivot Point Resistance 1 |   Pivot Point Support 1 |   Fibonacci Retracement 50.0% |   Fibonacci Retracement 61.8% |
|:-----------|------------------------------:|-----------------------------------:|-------------------------------------------:|-------:|----------------------------:|--------------------------------:|----------------------------:|-----------------------------------------:|---------------------------------------:|----------------:|--------------:|---------------------------:|------------------------:|------------------------------:|------------------------------:|
| 2025-12-17 |                       277.993 |                            275.523 |                                    275.977 | 0.0016 |                     278.193 |                         276.338 |                     273.323 |                                  274.426 |                                278.186 |         285.71  |       273.223 |                    275.394 |                 271.694 |                       279.37  |                       277.371 |
| 2025-12-18 |                       277.518 |                            274.98  |                                    274.903 | 0.0014 |                     277.449 |                         275.466 |                     272.107 |                                  274.289 |                                277.532 |         284.525 |       272.472 |                    274.041 |                 269.533 |                       277.031 |                       274.481 |
| 2025-12-19 |                       276.846 |                            274.706 |                                    274.402 | 0.0012 |                     276.642 |                         274.854 |                     271.353 |                                  274.166 |                                276.211 |         282.695 |       270.188 |                    274.15  |                 267.489 |                       277.031 |                       274.481 |
| 2025-12-22 |                       275.762 |                            274.11  |                                    273.33  | 0.0009 |                     275.788 |                         273.972 |                     270.604 |                                  273.358 |                                275.272 |         281.048 |       271.983 |                    274.799 |                 270.111 |                       277.031 |                       274.481 |
| 2025-12-23 |                       274.922 |                            273.778 |                                    272.814 | 0.0007 |                     274.973 |                         273.42  |                     270.19  |                                  273.115 |                                274.464 |         279.566 |       271.049 |                    272.322 |                 268.961 |                       275.091 |                       272.999 |
| 2025-12-24 |                       274.432 |                            273.683 |                                    272.766 | 0.0006 |                     274.257 |                         273.173 |                     270.366 |                                  273.112 |                                274.006 |         278.232 |       270.736 |                    272.645 |                 269.713 |                       273.301 |                       271.631 |
| 2025-12-26 |                       274.048 |                            273.547 |                                    272.633 | 0.0004 |                     273.637 |                         272.936 |                     270.87  |                                  273.087 |                                273.626 |         277.031 |       273.07  |                    274.679 |                 271.458 |                       272.807 |                       271.254 |
| 2025-12-29 |                       273.754 |                            273.476 |                                    272.623 | 0.0003 |                     273.126 |                         272.798 |                     271.532 |                                  273.085 |                                273.368 |         275.951 |       273.133 |                    274.147 |                 271.644 |                       272.807 |                       271.254 |
| 2025-12-30 |                       273.462 |                            273.324 |                                    272.454 | 0.0002 |                     272.738 |                         272.61  |                     272.005 |                                  273.056 |                                273.119 |         274.978 |       272.748 |                    273.885 |                 271.88  |                       272.807 |                       271.254 |
| 2025-12-31 |                       272.969 |                            273.031 |                                    272.022 | 0.0001 |                     272.407 |                         272.298 |                     272.09  |                                  272.894 |                                272.801 |         274.103 |       272.405 |                    273.269 |                 271.474 |                       272.807 |                       271.254 |

---

## get_moving_average
Calculate a Moving Average (MA) of a given price series: the simple, exponential, double exponential, triangular, weighted or Hull moving average.

A Moving Average smooths out price data by averaging the price over a specified number of periods. The variants differ in how they weight the prices within the window: equally (simple), with exponentially decaying weights (exponential and double exponential), with weights that peak in the middle of the window (triangular), with linearly increasing weights (weighted) or with a combination of weighted averages that reduces the lag (Hull).

The formula is as follows, per method:

$$
\text{"simple":}\;\; \text{SMA} = \frac{\text{Sum of Prices}}{\text{Number of Prices}}
$$

$$
\text{"exponential":}\;\; \text{the first EMA is SMA(Close, Window), on the Window-th period},\;\; \text{and}\;\; \text{EMA} = (\text{Close} - \text{Previous EMA}) \cdot \frac{2}{1 + \text{Window}} + \text{Previous EMA}
$$

$$
\text{"double\_exponential":}\;\; \text{DEMA} = 2 \cdot \operatorname{EMA}(\text{Close},\; \text{Window}) - \operatorname{EMA}(\operatorname{EMA}(\text{Close},\; \text{Window}),\; \text{Window})
$$

$$
\text{"triangular":}\;\; \text{TMA} = \operatorname{SMA}(\operatorname{SMA}(\text{Close},\; \text{Sub-window Length}\; 1),\; \text{Sub-window Length}\; 2),\;\; \text{with both sub-windows} \;\frac{\text{Window} + 1}{2} \;\text{for an odd window and} \;\frac{\text{Window}}{2} \;\text{and} \;\frac{\text{Window}}{2} + 1 \;\text{for an even window} \;(\text{TA-Lib's TRIMA convention})
$$

$$
\text{"weighted":}\;\; \text{WMA} = \frac{\text{Sum of} \;(\text{Price} \cdot \text{Weight})}{\text{Sum of Weights}},\;\; \text{with weights 1 to Window from the oldest to the latest price}
$$

$$
\text{"hull":}\;\; \text{HMA} = \operatorname{WMA}\left(2 \cdot \operatorname{WMA}\left(\text{Close},\; \frac{\text{Window}}{2}\right) - \operatorname{WMA}(\text{Close},\; \text{Window}),\; \sqrt{\text{Window}}\right)
$$

Seeding the EMA with a simple average, as TA-Lib and StockCharts do, leaves the first Window - 1 periods of the price history empty. The DEMA, TRIX, MACD, Percentage Price Oscillator, Force Index, Elder Ray Index, Keltner Channels and Chaikin and McClellan Oscillators use the same EMA and start once their own EMAs are seeded. The Kaufman Adaptive Moving Average, which adapts its smoothing to the efficiency of the price move, is `get_kaufman_adaptive_moving_average`.

For more information, see the following sources:

- TA-Lib: SMA, EMA, DEMA, TRIMA, WMA and HMA, the reference implementations ([https://ta-lib.org/functions/](https://ta-lib.org/functions/){:target="_blank"}).

**Also known as:** MA, SMA, simple moving average, EMA, exponential moving average, DEMA, double exponential moving average, TMA, TRIMA, triangular moving average, WMA, linearly weighted moving average, HMA, Hull moving average.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int, optional):</u> Number of periods to consider for the moving average.
The number of periods (time intervals) over which to calculate the MA. Defaults to 14.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the MA.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>method (str, optional):</u> The moving average: "simple", "exponential",
"double_exponential", "triangular", "weighted" or "hull". Defaults to "simple".
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame or pd.Series:
Moving Average (MA) values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates the
MA for each asset in the Toolkit instance.
- The simple, exponential, double exponential, triangular, weighted and Hull moving averages
equal TA-Lib's SMA, EMA, DEMA, TRIMA, WMA and HMA.
- If `growth` is set to True, the method calculates the growth of the MA
using the specified `lag`.

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
Calculate the Trix (Triple Exponential Moving Average) for a given price series.

Trix is a momentum oscillator that calculates the percentage rate of change of a triple exponentially smoothed moving average. It helps identify overbought and oversold conditions in a market.

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

**Also known as:** triple smoothed EMA, rate of change oscillator.

Reference: Hutson, J. (1983). "TRIX - Triple Exponential Smoothing Oscillator." Technical Analysis of Stocks & Commodities, 1(5).

TA-Lib: TRIX, the reference implementation ([https://ta-lib.org/functions/trix.html](https://ta-lib.org/functions/trix.html){:target="_blank"}).

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int, optional):</u> The number of periods of each of the three exponential moving
averages. Defaults to 15, the window of Hutson (1983) and StockCharts.
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
Trix values as a decimal (0.001 is 0.1%).

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates the
Trix for each asset in the Toolkit instance.
- TRIX is a decimal and equals TA-Lib's TRIX divided by 100, since TA-Lib's TRIX is in
percent.
- If `growth` is set to True, the method calculates the growth of the Trix
using the specified `lag`.
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

## get_bollinger_bands
Calculate the Bollinger Bands for a given price series.

Bollinger Bands are a volatility indicator that consists of three lines: an upper band, a middle band (simple moving average), and a lower band. The upper and lower bands are calculated as the moving average plus and minus a specified number of standard deviations, respectively.

The formula is as follows:

$$
\text{Middle Band} = \operatorname{SMA}(\text{Close},\; \text{Window})
$$

$$
\text{Upper Band} = \text{Middle Band} + (\text{Num Std Dev} \cdot \text{Std Dev})
$$

$$
\text{Lower Band} = \text{Middle Band} - (\text{Num Std Dev} \cdot \text{Std Dev})
$$

The standard deviation is the *population* standard deviation (dividing by n), as Bollinger himself specifies and as TA-Lib and StockCharts both implement, not pandas' default sample standard deviation.

The band width tracks volatility: bands that narrow sharply (a squeeze) often precede a larger move, without saying in which direction. A close at or beyond a band is not a sell or buy signal by itself, since prices can walk along a band in a trend. The defaults are Bollinger's own setting, a 20-period average with 2 standard deviations, as on most charting platforms.

For more information, see the following sources:

- TA-Lib: BBANDS, the reference implementation ([https://ta-lib.org/functions/bbands.html](https://ta-lib.org/functions/bbands.html){:target="_blank"}).

**Also known as:** Bollinger Bands, BB, volatility bands, price channels.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int, optional):</u> Number of periods for moving average calculation.
The number of periods (time intervals) over which to calculate the moving average. Defaults to 20.
- <u>num_std_dev (float, optional):</u> Number of standard deviations for the bands.
Defaults to 2.
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
Bollinger Bands (upper, middle, lower).

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates the
Bollinger Bands for each asset in the Toolkit instance.
- The bands equal TA-Lib's BBANDS with a simple moving average (`matype=0`).
- If `growth` is set to True, the method calculates the growth of the Bollinger Bands
using the specified `lag`.

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
Calculate the Bollinger %B and BandWidth for a given price series.

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

For more information, see the following sources:

- TA-Lib: PERCENTB and BBW, the reference implementations ([https://ta-lib.org/functions/percentb.html](https://ta-lib.org/functions/percentb.html){:target="_blank"}, [https://ta-lib.org/functions/bbw.html](https://ta-lib.org/functions/bbw.html){:target="_blank"}).

**Also known as:** Percent B, %b, Bollinger Band Width, BBW, Bollinger Squeeze.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
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
- With a simple moving average (`matype=0`), %B equals TA-Lib's PERCENTB and BandWidth
equals TA-Lib's BBW divided by 100, since TA-Lib's BBW is in percent.
- If `growth` is set to True, the method calculates the growth of %B and BandWidth
using the specified `lag`.

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

## get_kaufman_adaptive_moving_average
Calculate the Kaufman Adaptive Moving Average (KAMA) for a given price series.

The Kaufman Adaptive Moving Average adjusts its own responsiveness to price changes based on how "efficiently" price is moving. It compares the net directional move over the window to the total (sum of absolute) movement over that same window - the Efficiency Ratio. When price trends strongly in one direction (an efficient move), the Efficiency Ratio is close to 1 and KAMA tracks price closely, behaving like a fast EMA. When price whipsaws sideways (an inefficient move), the Efficiency Ratio is close to 0 and KAMA flattens out, behaving like a slow EMA - reducing whipsaw signals in choppy markets while still reacting quickly during strong trends.

The formula is as follows:

$$
\text{Change} = \left|\operatorname{Close}(t) - \operatorname{Close}(t - \text{window})\right|
$$

$$
\text{Volatility} = \operatorname{Sum}(\left|\operatorname{Close}(i) - \operatorname{Close}(i - 1)\right|,\; \text{window})
$$

$$
\text{Efficiency Ratio} \;(\text{ER}) = \frac{\text{Change}}{\text{Volatility}}
$$

$$
\text{Fastest SC} = \frac{2}{\text{fast\_window} + 1},\;\; \text{Slowest SC} = \frac{2}{\text{slow\_window} + 1}
$$

$$
\text{Smoothing Constant} \;(\text{SC}) = \left[\text{ER} \cdot (\text{Fastest SC} - \text{Slowest SC}) + \text{Slowest SC}\right]^{2}
$$

$$
\operatorname{KAMA}(t) = \operatorname{KAMA}(t-1) + \text{SC} \cdot (\operatorname{Close}(t) - \operatorname{KAMA}(t-1))
$$

**Also known as:** KAMA, Kaufman's Adaptive Moving Average.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int, optional):</u> Number of periods over which the Efficiency Ratio is
calculated. Defaults to 10.
- <u>fast_window (int, optional):</u> The number of periods that corresponds to the
fastest EMA constant used when the Efficiency Ratio is at its maximum (1.0).
Defaults to 2.
- <u>slow_window (int, optional):</u> The number of periods that corresponds to the
slowest EMA constant used when the Efficiency Ratio is at its minimum (0.0).
Defaults to 30.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the KAMA.
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

pd.Series or pd.DataFrame: KAMA values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the KAMA for each asset in the Toolkit instance.
- Reference: Kaufman, P.J. (1998). "Trading Systems and Methods." 3rd ed. Wiley.
- TA-Lib: KAMA, the reference implementation ([https://ta-lib.org/functions/kama.html](https://ta-lib.org/functions/kama.html){:target="_blank"}).
- With the default `fast_window` of 2 and `slow_window` of 30, which TA-Lib fixes, the KAMA
equals TA-Lib's KAMA.
- If `growth` is set to True, the method calculates the growth of the KAMA using the
specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["^STOXX50E"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.technicals.get_kaufman_adaptive_moving_average().tail(5)
```

Which returns:

| Date       |   ^STOXX50E |   Benchmark |
|:-----------|------------:|------------:|
| 2025-12-24 |      nan    |     674.145 |
| 2025-12-26 |      nan    |     674.285 |
| 2025-12-29 |     5725.07 |     674.644 |
| 2025-12-30 |     5726.77 |     674.963 |
| 2025-12-31 |      nan    |     674.999 |

---

## get_volume_weighted_average_price
Calculate the Volume Weighted Average Price (VWAP) for a given price series.

The Volume Weighted Average Price (VWAP) weighs the typical price of each period by its traded volume over a rolling window, giving a more volume-informed view of the average price than a plain moving average.

The formula is as follows:

$$
\text{Typical Price} = \frac{\text{High} + \text{Low} + \text{Close}}{3}
$$

$$
\text{VWAP} = \frac{\operatorname{Sum}(\text{Typical Price} \cdot \text{Volume},\; \text{Window})}{\operatorname{Sum}(\text{Volume},\; \text{Window})}
$$

The VWAP that trading desks use as an execution benchmark is calculated from the trades of a single session and resets every day. This method computes a rolling VWAP over several periods from the high, low, close and volume of each period, which works as a volume-weighted moving average, not as the intraday benchmark against which fills are measured.

For more information, see the following sources:

- TA-Lib: VWAP, the reference implementation ([https://ta-lib.org/functions/vwap.html](https://ta-lib.org/functions/vwap.html){:target="_blank"}).

**Also known as:** VWAP.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the open, high and low prices are adjusted
for dividends in the same way.
- <u>window (int, optional):</u> Number of periods to consider for the VWAP.
The number of periods (time intervals) over which to calculate the VWAP. Defaults to 14.
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
- The VWAP is taken over a rolling `window`. TA-Lib's VWAP accumulates the typical price
times volume from the first period on, which is the VWAP over a window that grows with the
data.
- If `growth` is set to True, the method calculates the growth of the VWAP
using the specified `lag`.

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
Calculate the Parabolic Stop and Reverse (SAR) for a given price series.

The Parabolic SAR is a trend-following indicator that trails price action, flipping from below to above price (and vice versa) whenever the trend reverses. The acceleration factor increases as the trend extends, causing the SAR to converge towards price over time.

The formula is as follows:

$$
\text{Uptrend SAR} = \text{Prior SAR} + \text{AF} \cdot (\text{Extreme Point} - \text{Prior SAR})
$$

$$
\text{Downtrend SAR} = \text{Prior SAR} - \text{AF} \cdot (\text{Prior SAR} - \text{Extreme Point})
$$

For more information, see the following sources:

- TA-Lib: SAR, the reference implementation ([https://ta-lib.org/functions/sar.html](https://ta-lib.org/functions/sar.html){:target="_blank"}).

**Also known as:** Parabolic SAR, stop and reverse, PSAR.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>af_start (float, optional):</u> Initial acceleration factor. Defaults to 0.02.
- <u>af_increment (float, optional):</u> Amount by which the acceleration factor
increases every time a new extreme point is reached. Defaults to 0.02.
- <u>af_max (float, optional):</u> Maximum value the acceleration factor can reach.
Defaults to 0.2.
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
- The Parabolic SAR equals TA-Lib's SAR, which takes `af_increment` equal to `af_start`, and
its SAREXT for any `af_increment`.
- If `growth` is set to True, the method calculates the growth of the Parabolic SAR
using the specified `lag`.

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
Calculate the Pivot Points for a given price series.

Pivot Points are calculated from the previous period's high, low and close prices and are used to identify potential support and resistance levels for the current period.

The formula is as follows:

$$
\text{Pivot Point} = \frac{\text{Previous High} + \text{Previous Low} + \text{Previous Close}}{3}
$$

$$
\text{Resistance}\; 1 = (2 \cdot \text{Pivot Point}) - \text{Previous Low}
$$

$$
\text{Support}\; 1 = (2 \cdot \text{Pivot Point}) - \text{Previous High}
$$

$$
\text{Resistance}\; 2 = \text{Pivot Point} + (\text{Previous High} - \text{Previous Low})
$$

$$
\text{Support}\; 2 = \text{Pivot Point} - (\text{Previous High} - \text{Previous Low})
$$

$$
\text{Resistance}\; 3 = \text{Previous High} + 2 \cdot (\text{Pivot Point} - \text{Previous Low})
$$

$$
\text{Support}\; 3 = \text{Previous Low} - 2 \cdot (\text{Previous High} - \text{Pivot Point})
$$

**Also known as:** pivot points, floor trader pivots.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the open, high and low prices are adjusted
for dividends in the same way.
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
Pivot Points (pivot, resistance 1-3, support 1-3).

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates the
Pivot Points for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the Pivot Points
using the specified `lag`.

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
Retrieves the support and resistance levels for the specified period and assets.

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

**Args:**

- <u>sensitivity (float, optional):</u> The sensitivity parameter to determine the significance of the peaks
and valleys. A higher sensitivity value will result in fewer support and resistance levels
being identified. Defaults to 0.05.
- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
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
Calculate the Fibonacci Retracement Levels for a given price series.

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

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int, optional):</u> The number of periods over which the rolling swing high
(maximum) and swing low (minimum) are determined. Defaults to 14.
- <u>levels (list[float] &#124; None, optional):</u> The Fibonacci ratios to calculate levels for.
Defaults to the standard [0.0, 0.236, 0.382, 0.5, 0.618, 0.786, 1.0].
- <u>trend (str, optional):</u> Whether to compute retracement levels for an "uptrend"
(levels measured down from the high — the conventional direction, used when a
prior move was up and price is now pulling back) or a "downtrend" (levels
measured up from the low, used when a prior move was down and price is now
bouncing). Defaults to "uptrend".
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
- If `growth` is set to True, the method calculates the growth of the retracement levels
using the specified `lag`.

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

## collect_volatility_indicators
Calculates and collects various volatility indicators based on the provided data.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
- <u>window (int, optional):</u> The window size for calculating indicators.
Defaults to 14. The Bollinger Bands and their %B and BandWidth keep their own
window of 20 periods (with 2 standard deviations), as defined by Bollinger, and
the Supertrend its own defaults.
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
- If `growth` is set to True, the method calculates the growth of the indicator values
using the specified `lag`.

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

| Date       |   Bollinger Band Upper |   Bollinger Band Middle |   Bollinger Band Lower |   Bollinger %B |   Bollinger BandWidth |   True Range |   Average True Range |   Supertrend |   Supertrend Trend Direction |   Keltner Channel Upper |   Keltner Channel Middle |   Keltner Channel Lower |   Donchian Channel Upper |   Donchian Channel Middle |   Donchian Channel Lower |
|:-----------|-----------------------:|------------------------:|-----------------------:|---------------:|----------------------:|-------------:|---------------------:|-------------:|-----------------------------:|------------------------:|-------------------------:|------------------------:|-------------------------:|--------------------------:|-------------------------:|
| 2025-12-17 |                285.548 |                 276     |                266.452 |         0.2327 |                0.0692 |       4.5043 |               4.871  |      268.465 |                            1 |                 284.794 |                  275.314 |                 265.833 |                  287.618 |                   279.232 |                  270.846 |
| 2025-12-18 |                285.211 |                 276.181 |                267.151 |         0.2267 |                0.0654 |       6.6568 |               4.9986 |      268.465 |                            1 |                 284.635 |                  274.771 |                 264.907 |                  287.618 |                   279.158 |                  270.697 |
| 2025-12-19 |                284.285 |                 276.55  |                268.816 |         0.2524 |                0.0559 |       4.6837 |               4.9761 |      268.465 |                            1 |                 284.312 |                  274.498 |                 264.683 |                  287.618 |                   276.821 |                  266.023 |
| 2025-12-22 |                284.343 |                 276.525 |                268.707 |         0.0846 |                0.0565 |       3.3583 |               4.8605 |      268.465 |                            1 |                 283.406 |                  273.902 |                 264.397 |                  287.618 |                   276.821 |                  266.023 |
| 2025-12-23 |                284.455 |                 276.347 |                268.24  |         0.1958 |                0.0587 |       2.9298 |               4.7226 |      268.465 |                            1 |                 282.71  |                  273.57  |                 264.43  |                  287.618 |                   276.821 |                  266.023 |
| 2025-12-24 |                284.438 |                 276.19  |                267.941 |         0.2981 |                0.0597 |       3.2188 |               4.6152 |      268.465 |                            1 |                 282.345 |                  273.476 |                 264.606 |                  283.741 |                   274.882 |                  266.023 |
| 2025-12-26 |                284.387 |                 275.983 |                267.579 |         0.2899 |                0.0609 |       2.5013 |               4.4642 |      268.465 |                            1 |                 281.822 |                  273.339 |                 264.856 |                  280.164 |                   273.094 |                  266.023 |
| 2025-12-29 |                284.195 |                 275.729 |                267.264 |         0.3276 |                0.0614 |       2.003  |               4.2884 |      268.465 |                            1 |                 281.304 |                  273.268 |                 265.233 |                  279.177 |                   272.6   |                  266.023 |
| 2025-12-30 |                283.299 |                 275.23  |                267.162 |         0.308  |                0.0586 |       1.7937 |               4.1102 |      268.465 |                            1 |                 280.707 |                  273.117 |                 265.526 |                  279.177 |                   272.6   |                  266.023 |
| 2025-12-31 |                281.366 |                 274.516 |                267.666 |         0.2372 |                0.0499 |       1.9233 |               3.954  |      268.465 |                            1 |                 280.039 |                  272.823 |                 265.607 |                  279.177 |                   272.6   |                  266.023 |

---

## get_true_range
Calculate the True Range (TR) for a given price series.

The True Range (TR) is a measure of market volatility that considers the differences between the high and low prices and the previous closing price. It provides insights into the price movement of an asset.

The formula is as follows:

$$
\text{TR} = \max(\text{high} - \text{low},\; \operatorname{abs}(\text{high} - \text{previous\_close}),\; \operatorname{abs}(\text{low} - \text{previous\_close}))
$$

For more information, see the following sources:

- TA-Lib: TRANGE, the reference implementation ([https://ta-lib.org/functions/trange.html](https://ta-lib.org/functions/trange.html){:target="_blank"}).

**Also known as:** TR, true range.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
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
- The True Range equals TA-Lib's TRANGE from the second period on. The first period, which
has no previous close, is High — Low here and empty in TA-Lib.
- If `growth` is set to True, the method calculates the growth of the True Range
using the specified `lag`.

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
Calculate the Average True Range (ATR) of a given price series.

The Average True Range (ATR) is a technical indicator that measures the volatility of an asset's price movements over a specified number of periods. It provides insights into the potential price range of an asset, which can help traders and investors make more informed decisions.

The formula is as follows:

$$
\text{TR} = \max(\text{high} - \text{low},\; \operatorname{abs}(\text{high} - \text{previous\_close}),\; \operatorname{abs}(\text{low} - \text{previous\_close}))
$$

$$
\text{ATR} = \text{Wilder's Smoothed Moving Average of TR over} \;\text{window} \;\text{periods}
$$

The ATR is in price units, which makes it the common basis for stop distances (for example two ATRs below the entry) and for sizing positions to equal risk. For the same reason it cannot be compared across stocks or over long periods in which the price changed a lot; divide it by the price for a percentage volatility. It measures how far price moves, not in which direction.

For more information, see the following sources:

- TA-Lib: ATR, the reference implementation ([https://ta-lib.org/functions/atr.html](https://ta-lib.org/functions/atr.html){:target="_blank"}).

**Also known as:** ATR, volatility indicator. See `volatility_model.get_average_true_range` for the full formula; Wilder's smoothing constant (1/window) is slower than a standard EMA's (2/(window+1)) of the same window.

The first period has no previous close, so its True Range is High - Low and the first ATR is the average of the first `window` True Ranges (the StockCharts convention; TA-Lib starts one period later).

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the open, high and low prices are adjusted
for dividends in the same way.
- <u>window (int, optional):</u> The number of periods over which to calculate the Average
True Range. Defaults to 14.
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
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: ATR values per ticker or ATR growth rate (if growth is True).
A pandas Series containing the calculated Average True Range values or growth rate for each period.

**Notes:**

- ATR values are typically used to assess the volatility and potential price movement of an asset.
- A higher ATR value indicates higher volatility, while a lower ATR value suggests lower volatility.
- Because the True Range starts on the first period, the ATR starts one period before
TA-Lib's ATR and differs from it until the two converge (within 0.01% after about 80
periods with the default window).

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
Calculate the Mass Index for a given price series.

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

For more information, see the following sources:

- TA-Lib: MASSI, the reference implementation ([https://ta-lib.org/functions/massi.html](https://ta-lib.org/functions/massi.html){:target="_blank"}).

**Also known as:** Mass Index, MI. See `volatility_model.get_mass_index` for the references.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
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
the 41st with the default windows. The Mass Index equals TA-Lib's MASSI.
- If `growth` is set to True, the method calculates the growth of the indicator values
using the specified `lag`.

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
Calculate the Supertrend indicator for a given price series.

The Supertrend indicator plots a single trailing line that flips between sitting below price (in an uptrend) and above price (in a downtrend). The line is built from two bands offset from the median price ((High + Low) / 2) by a multiple of the Average True Range, which are then "ratcheted" period over period - each band can only move in the direction that tightens around price - so that the active band only flips to the other side once the closing price actually crosses it. This makes Supertrend both a trend filter (the flip direction signals a trend change) and a trailing stop-loss level.

The formula is as follows:

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

For more information, see the following sources:

- TA-Lib: SUPERTREND, the reference implementation ([https://ta-lib.org/functions/supertrend.html](https://ta-lib.org/functions/supertrend.html){:target="_blank"}).

**Also known as:** Supertrend, SuperTrend.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the open, high and low prices are adjusted
for dividends in the same way.
- <u>window (int, optional):</u> Number of periods for the underlying Average True Range
calculation. Defaults to 10.
- <u>multiplier (float, optional):</u> Multiplier applied to the Average True Range to
determine how far the bands sit from the median price. Defaults to 3.0.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Supertrend and
Trend Direction values. Defaults to False.
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
Supertrend (the trailing indicator line) and Trend Direction (1 for an uptrend
and -1 for a downtrend) values.

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
equals TA-Lib's `trend` from TA-Lib's first value.
- If `growth` is set to True, the method calculates the growth of the Supertrend and
Trend Direction values using the specified `lag`.

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
Calculate the Chandelier Exit for a given price series.

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

See `volatility_model.get_chandelier_exit` for the references.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
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
- If `growth` is set to True, the method calculates the growth of the Long Exit and Short Exit
using the specified `lag`.

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
Calculate the Keltner Channels for a given price series.

The Keltner Channels consist of three lines: a middle line, the Exponential Moving Average (EMA) of the closing prices, and an upper and a lower line a multiple of the Average True Range (ATR) above and below it.

The formula is as follows:

$$
\text{Middle Line} = \operatorname{EMA}(\text{Close},\; \text{window})
$$

$$
\text{Upper Line} = \text{Middle Line} + \text{atr\_multiplier} \cdot \operatorname{ATR}(\text{atr\_window})
$$

$$
\text{Lower Line} = \text{Middle Line} - \text{atr\_multiplier} \cdot \operatorname{ATR}(\text{atr\_window}),\;\; \text{where the ATR uses Wilder's smoothing}
$$

For more information, see the following sources:

- TA-Lib: KC, the reference implementation ([https://ta-lib.org/functions/kc.html](https://ta-lib.org/functions/kc.html){:target="_blank"}).

**Also known as:** ATR-based bands, volatility channels.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the open, high and low prices are adjusted
for dividends in the same way.
- <u>window (int, optional):</u> Number of periods for the Exponential Moving Average (the
middle line). Defaults to 20, as on StockCharts.
- <u>atr_window (int, optional):</u> Number of periods for ATR calculation.
Defaults to 10, as on StockCharts.
- <u>atr_multiplier (float, optional):</u> Multiplier for ATR to determine channel width.
Defaults to 2.
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

pd.Series or pd.DataFrame: Keltner Channels (upper, middle, lower).

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates Keltner Channels
for each asset in the Toolkit instance.
- The middle line is the EMA of the close, as on StockCharts. TA-Lib's KC takes the EMA of
the typical price ((High + Low + Close) / 3) and starts its ATR one period later, so the
channels differ throughout (by about 0.3% on daily data).
- If `growth` is set to True, the method calculates the growth of the channels using the specified `lag`.

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
Calculate the Donchian Channels for a given price series.

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

For more information, see the following sources:

- TA-Lib: DONCHIAN, the reference implementation ([https://ta-lib.org/functions/donchian.html](https://ta-lib.org/functions/donchian.html){:target="_blank"}).

**Also known as:** Donchian Channels, price channel breakout.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int, optional):</u> Number of periods for the Donchian Channels.
Defaults to 20.
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
- TA-Lib's DONCHIAN includes the current period, so each channel here equals TA-Lib's of the
previous period.
- If `growth` is set to True, the method calculates the growth of the channels using the specified `lag`.

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
Retrieves the Volatility Cone for the specified period and assets.

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

**Args:**

- <u>windows (list[int] &#124; None, optional):</u> The rolling windows (in periods) to
calculate realized volatility for. Defaults to [10, 20, 30, 60, 90, 120].
- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
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

## get_trin
Calculate the TRIN (Arms Index) for a given price series.

TRIN compares the ratio of advancing to declining issues against the ratio of volume in advancing issues to volume in declining issues. It is a market-wide breadth reading computed across all tickers in the Toolkit instance (excluding the synthetic "Portfolio" and "Benchmark" columns), and the resulting single reading is broadcast to every ticker column so it lines up with the other breadth indicators.

The formula is as follows:

$$
\text{TRIN} = \frac{\frac{\text{Advancing Issues}}{\text{Declining Issues}}}{\frac{\text{Advancing Volume}}{\text{Declining Volume}}}
$$

A TRIN below 1 means the volume in rising stocks outweighs their number, which is read as buying pressure, and above 1 as selling pressure; readings far above 2 tend to come with capitulation days. It is meant for a broad universe, such as all stocks of an exchange. Calculated across a handful of tickers it jumps between extremes and is undefined on days when none of them fell.

A ticker counts on the dates it traded, with its change since its own previous close: on a date only a cryptocurrency in the Toolkit traded, such as a weekend, only the cryptocurrency counts, and a stock is never counted as unchanged on it.

**Also known as:** Arms Index, TRIN.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
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
- If `growth` is set to True, the method calculates the growth of the indicator values
using the specified `lag`.

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
Calculate the New Highs - New Lows for a given price series.

New Highs - New Lows measures the number of tickers reaching a new high over the specified window minus the number of tickers reaching a new low over the same window. It is a market-wide breadth reading computed across all tickers in the Toolkit instance (excluding the synthetic "Portfolio" and "Benchmark" columns), and the resulting single reading is broadcast to every ticker column so it lines up with the other breadth indicators.

The formula is as follows:

$$
\text{New Highs} - \text{New Lows} = (\text{Number of tickers at a window-period high}) - (\text{Number of tickers at a window-period low})
$$

The reading counts tickers at a high or low of the lookback window, so it needs a broad universe and a history of at least one window before the start of the period of interest: in the first periods every ticker is compared with only a few prices, so it is often counted at a high or a low, and on the first date at both. Persistently more new lows than new highs while an index still rises is a classic sign of narrowing breadth.

Each ticker's window counts its own closes and the ticker counts on the dates it traded, so the weekends of a cryptocurrency in the Toolkit do not shorten a stock's window.

**Also known as:** new highs minus new lows, record high percent.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The name of the column containing the close prices.
Defaults to "Adj Close".
- <u>window (int, optional):</u> Number of periods for the new high / new low lookback.
Defaults to 252.
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
- If `growth` is set to True, the method calculates the growth of the indicator values
using the specified `lag`.

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

## get_market_breadth
Calculate the breadth of the market the Toolkit's tickers make up: how many of them take part in a move. An index can rise on the strength of a few large companies while most of its members fall; breadth shows that divergence, which often comes before the index itself turns. Breadth is most meaningful across many tickers, such as the constituents of an index, which `Discovery.get_index_constituents` lists (e.g. the 500 tickers of the S&P 500). Today's members leave out the companies that were removed from the index since (often after falling behind), so breadth of past dates computed from them is biased towards the survivors, the further back the more; its `date=` gives the members on the first date of the window instead.

Per date it returns:

- Advancers, Decliners and Unchanged: the number of tickers whose close rose, fell or stayed the same, and the Net Advances.
- Advance-Decline Line: the running total of the net advances. A rising index with a falling line is the classic negative divergence.
- Advance-Decline Ratio: the advancers divided by the decliners.
- McClellan Oscillator: the ratio-adjusted version, the 19-period minus the 39-period exponential moving average (smoothing constants of 0.10 and 0.05) of the net advances divided by advancers plus decliners (times 1,000); unchanged issues are left out. Each average starts from the simple average of its first 19 or 39 values, so the oscillator starts once the 39-period average exists (NaN before), as does its running total, the McClellan Summation Index.
- Percentage Above the short and long moving average: the share of tickers trading above their 50 and 200-period average, a gauge of how broad a trend is.
- New Highs and New Lows: the tickers whose close is above the highest (below the lowest) close of the previous `high_low_window` - 1 periods, so the highest or lowest of the last `high_low_window` periods; a close that only equals the previous high is no new high. NaN until at least one ticker has a full window.

The Benchmark (and a Portfolio) are left out. A constituent counts on the dates it traded, and its changes, moving averages and highs and lows run over its own closes: on a date only a cryptocurrency in the Toolkit traded, such as a weekend, only the cryptocurrency counts, and the McClellan averages then skip that date (see `breadth_model.get_market_breadth`).

For more information, see the following book:

- McClellan, S. and McClellan, M. (1970). "Patterns for Profit: The McClellan Oscillator and Summation Index." Trade Levels Inc.

**Also known as:** market breadth, advance-decline line, McClellan oscillator, percentage above 200-day moving average, new highs new lows.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
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

## get_seasonality
Calculate the seasonality of every ticker's returns: the average return per calendar month (from monthly returns) or per day of the week (from daily returns), with the median, the hit rate (the share of positive returns), the t-statistic of the average and the number of observations. Well-known examples are the January effect and the "sell in May" pattern. A pattern needs many years and a t-statistic well above 2 before it says much, and even then it can fade once it is widely traded on.

A monthly return runs from one month's last close to the next, so a final month that is not complete yet (an end date before that month's last business day, as with the default end date of today) is left out rather than averaged as a full month. The Benchmark is included as a ticker, so its seasonality is there to compare with; a Portfolio is left out.

For more information, see the following paper:

- Heston, S.L. and Sadka, R. (2008). "Seasonality in the Cross-Section of Stock Returns." Journal of Financial Economics, 87(2), 418-445.

**Also known as:** seasonality, monthly seasonality, day of the week effect, January effect, calendar anomalies.

**Args:**

- <u>frequency (str, optional):</u> "month" (per calendar month) or "weekday" (per day of
the week). Defaults to "month".
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
Calculate the relative strength of every ticker against the Benchmark and against the other tickers. Relative strength investing buys what has been outperforming, the momentum effect that has held across markets and decades.

- Relative Strength: the price divided by the Benchmark's, set to 1 on the first date. It rises while the ticker outperforms the Benchmark.
- Mansfield Relative Strength: the relative strength against its own moving average (of `window` periods, a year by default) minus 1. Above zero the ticker is gaining on the Benchmark.
- Relative Strength Rating: the ticker's performance over the last year, the last quarter weighing most (the 3, 6, 9 and 12-month returns weighted 0.4, 0.2, 0.2 and 0.2), ranked against the other tickers from 1 (weakest) to 99 (strongest), from daily prices. Investor's Business Daily publishes the original rating with a proprietary formula; this weighting is its common public approximation. Tickers with the same score share the highest rank among them, so the rating reads as the share of the other tickers outperformed or matched and tied leaders both rate 99. It needs many tickers to be meaningful, such as the constituents of an index (see `Discovery.get_index_constituents`, whose `date=` gives the members on a past date; today's members leave out the companies removed from the index since).

For more information, see the following papers and books:

- Jegadeesh, N. and Titman, S. (1993). "Returns to Buying Winners and Selling Losers: Implications for Stock Market Efficiency." The Journal of Finance, 48(1), 65-91.
- Weinstein, S. (1988). "Stan Weinstein's Secrets for Profiting in Bull and Bear Markets." McGraw-Hill.
- O'Neil, W.J. (1988). "How to Make Money in Stocks." McGraw-Hill.

**Also known as:** relative strength, price relative, Mansfield relative strength, RS rating, relative performance.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
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

## get_factor_analysis
Factor analysis (predictive power) of the technical indicators: whether the tickers that score high on an indicator go on to return more than those that score low. Per period, the information coefficient (IC) is the Spearman rank correlation between the indicator of the tickers at the end of the period and their return over the following horizon: 1 means the indicator ranks the later returns perfectly, -1 in reverse and 0 that it says nothing about them. The IC measures skill in Grinold and Kahn's fundamental law of active management, $$\text{IR} \approx \text{IC} \times \sqrt{\text{breadth}}$$: a small but consistent IC across many tickers and periods gives a high information ratio.

The summary has a row per indicator and horizon with the mean IC, its standard deviation, the IC information ratio (mean divided by standard deviation), the t-statistic of the mean with its p-value, the share of periods with a positive IC, the number of periods, the top minus bottom spread (the mean forward return of the highest quantile minus that of the lowest), the mean turnover of the top and bottom quantiles and the mean rank autocorrelation of the indicator from one period to the next. With detail, it returns one of those parts per period (or per quantile) for a single indicator.

The indicators are calculated daily and the value on the last trading day of each period is compared with the returns from that day's close onwards, using the dividend and split adjusted close. An indicator in price units does not compare across tickers with different share prices, so a price line (a moving average, band, channel, stop or cloud line) is used as the distance of the close from it, close / line - 1, and a price difference (the true range, ATR, MACD, awesome oscillator, elder ray and detrended price oscillator) as a share of the close. Each ticker keeps its own history: a ticker without a value or a return in a period is left out of that period only.

**Args:**

- <u>metrics (str &#124; list[str], optional):</u> An indicator method name, e.g.
"get_relative_strength_index", a list of them, or a collection: "momentum",
"overlap", "volatility", "breadth" or "all". Defaults to "momentum", the
oscillators and momentum indicators. The collections leave out the market-wide
breadth measures, the volume-scaled indicators and the pivot points and
Fibonacci levels.
- <u>period (str, optional):</u> The frequency at which the indicators are evaluated:
daily, weekly, monthly, quarterly or yearly. Defaults to "monthly".
- <u>horizons (list[int] &#124; int &#124; None, optional):</u> The number of periods the forward
returns cover. Defaults to None, which uses about a period, a quarter and a
year ahead (1, 3 and 12 months for monthly).
- <u>quantiles (int, optional):</u> The number of quantiles the tickers are sorted into per
period. Defaults to 5.
- <u>periods_apart (int, optional):</u> The number of periods between the dates the
quantile turnover and the rank autocorrelation compare. Defaults to 1.
- <u>detail (str &#124; None, optional):</u> Returns one part of the analysis of a single
indicator instead of the summary: "information_coefficient" (per period and
horizon), "quantile_returns" (the mean forward return per quantile and
horizon), "quantile_turnover" (per period and quantile) or
"rank_autocorrelation" (per period). Defaults to None.
- <u>column (str &#124; None, optional):</u> The output to use of an indicator with several,
e.g. "Signal Line" of the MACD or "Upper Band" of the Bollinger Bands.
Defaults to None, which uses the first output in alphabetical order other
than a price, e.g. "MACD Line" or "Lower Band".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
**kwargs: Parameters passed to the indicators that take them, e.g. window=14 or
close_column="Close".
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
- Based on alphalens (Quantopian) and on Grinold and Kahn (2000), Active Portfolio
Management.

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

|                                     |   Mean IC |   IC Standard Deviation |   IC Information Ratio |   t-Statistic |   p-Value |   Positive Share |   Observations |   Top Minus Bottom |   Quantile Turnover |   Rank Autocorrelation |
|:------------------------------------|----------:|------------------------:|-----------------------:|--------------:|----------:|-----------------:|---------------:|-------------------:|--------------------:|-----------------------:|
| ('get_rate_of_change', '1 Month')   |    0.0477 |                  0.3456 |                 0.1381 |        1.5063 |    0.1347 |           0.5798 |            119 |             0.0092 |              0.2626 |                 0.8582 |
| ('get_rate_of_change', '12 Months') |    0.1181 |                  0.3986 |                 0.2964 |        3.0802 |    0.0026 |           0.6389 |            108 |             0.08   |              0.2626 |                 0.8582 |
| ('get_moving_average', '1 Month')   |    0.0383 |                  0.3458 |                 0.1107 |        1.2071 |    0.2298 |           0.563  |            119 |             0.0125 |              0.3074 |                 0.8031 |
| ('get_moving_average', '12 Months') |    0.1018 |                  0.3848 |                 0.2646 |        2.7503 |    0.007  |           0.5833 |            108 |             0.0853 |              0.3074 |                 0.8031 |

---

## get_candlestick_patterns
Recognise 15 classic candlestick patterns in every ticker's candles, with the definitions of TA-Lib's CDL functions. Candlestick charting reads the open, high, low and close of a period as one candle: the real body between the open and the close and the shadows up to the high and down to the low. Certain shapes and sequences are read as a sign that a move is ending or continuing.

Each pattern is 1 on the candle that completes it as a bullish pattern, -1 as a bearish pattern and 0 otherwise (TA-Lib's +100 and -100 divided by 100). The weaker engulfing and harami, where one end of the two real bodies is equal, are 0.8 and -0.8 (TA-Lib's 80). The doji is indecision rather than a direction and is 1 when present; a marubozu and a spinning top take the colour of the candle (1 white, -1 black).

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

Sizes are relative to the ticker's own recent candles, as in TA-Lib: a real body is long (short) when it is longer (shorter) than the average real body of the 10 previous candles, a doji's body is at most 10% and a very short shadow less than 10% of their average high-low range, a long shadow is longer than the candle's own real body, and "near" is within 20% and "far" at least 60% of the average high-low range of the 5 previous candles.

For more information, see the following sources:

- Nison, S. (1991). "Japanese Candlestick Charting Techniques." New York Institute of Finance.
- Bulkowski, T.N. (2008). "Encyclopedia of Candlestick Charts." Wiley.
- TA-Lib: the CDL functions, the reference implementation ([https://ta-lib.org/functions/](https://ta-lib.org/functions/){:target="_blank"}).

**Also known as:** candlestick patterns, candle patterns, CDL, Japanese candlesticks.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close", in which case the open, high and low prices are adjusted
for dividends in the same way, so an ex-dividend day doesn't read as a gap. "Close"
uses the candles as traded (split-adjusted).
- <u>patterns (str &#124; list[str] &#124; None, optional):</u> The patterns to return, e.g. ["Hammer",
"Engulfing"]. Defaults to None, which returns all 15.
- <u>signals_only (bool, optional):</u> Whether to return only the periods in which at least one
of the returned patterns occurs for at least one ticker. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The patterns per date, with a column per pattern and ticker: 1 (bullish),
-1 (bearish), 0.8 / -0.8 (the weaker engulfing and harami) or 0.

**Notes:**

- The patterns match TA-Lib (github.com/TA-Lib/ta-lib, src/ta_func/ta_CDL*.c) candle for
candle, including its default candle settings and penetrations (30% for the stars, 50%
for the dark cloud cover).
- A pattern is empty until TA-Lib's lookback has passed: the 10 to 13 candles its
averages and the pattern itself need, counted from the ticker's own first candle.
- A pattern only describes the candles. The trend before it, which candlestick analysis
requires for a reversal (a hammer after a decline, a hanging man after a rise), is not
checked, as in TA-Lib; combine a pattern with a trend measure such as
`get_moving_average` or `get_signals`.

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

## get_signals
Turn the moving averages, the MACD, the RSI, the Bollinger Bands and new highs and lows into the events traders act on: the period a line is crossed. The indicators themselves are available as `get_moving_average`, `get_moving_average_convergence_divergence`, `get_relative_strength_index` and `get_bollinger_bands`, and give the same values.

Every signal is 1 on the period a line is crossed upwards, -1 on the period it is crossed downwards and 0 otherwise:

- Moving Average Crossover: the short Simple Moving Average crossing the long one; with the default 50 and 200 periods a golden cross (1) or a death cross (-1).
- MACD Crossover: the MACD line crossing its signal line, the classic trigger of the MACD.
- RSI Overbought: the RSI entering (1) or leaving (-1) the overbought zone above `rsi_overbought`. Leaving it is the classic sell signal.
- RSI Oversold: the RSI leaving (1) or entering (-1) the oversold zone below `rsi_oversold`. Leaving it is the classic buy signal.
- Upper Bollinger Band: the price breaking out above (1) or falling back below (-1) the upper band.
- Lower Bollinger Band: the price recovering above (1) or breaking down below (-1) the lower band.
- New High/Low: a close above every close of the previous `high_low_window` periods (1), a 52-week high with daily prices by default, or below every one of them (-1).

For more information, see the following books and papers:

- Murphy, J.J. (1999). "Technical Analysis of the Financial Markets." New York Institute of Finance.
- Appel, G. (1979). "The Moving Average Convergence-Divergence Trading Method." Signalert Corp.
- Wilder, J.W. Jr. (1978). "New Concepts in Technical Trading Systems." Trend Research.
- Bollinger, J. (2001). "Bollinger on Bollinger Bands." McGraw-Hill.
- Brock, W., Lakonishok, J., and LeBaron, B. (1992). "Simple Technical Trading Rules and the Stochastic Properties of Stock Returns." The Journal of Finance, 47(5), 1731-1764.

**Also known as:** trading signals, golden cross, death cross, crossovers, breakouts, MACD crossover, RSI signal, 52-week high, new high.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "intraday", "daily", "weekly", "monthly", "quarterly" or "yearly". Defaults to "daily".
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
Summarise the history of a technical indicator per ticker in a single row instead of the series itself: where the latest value ranks in its own history, the lowest and highest value with their dates, how many periods the indicator spent below or above a threshold, when it last crossed into that zone and how the price did afterwards. This answers questions such as "how oversold is the RSI compared with the last five years, and what happened after the previous times it fell below 30?" without the thousands of daily values behind it.

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

For more information, see the following books:

- Wilder, J.W. Jr. (1978). "New Concepts in Technical Trading Systems." Trend Research.
- Murphy, J.J. (1999). "Technical Analysis of the Financial Markets." New York Institute of Finance.

**Also known as:** indicator statistics, indicator percentile, oversold history, event study, forward returns after a signal, RSI below 30.

**Args:**

- <u>metric (str, optional):</u> The indicator method name, e.g. "get_stochastic_oscillator"
or "get_rate_of_change". Defaults to "get_relative_strength_index".
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
other than a price, e.g. "MACD Line".
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
default, weeks with period="weekly".

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

