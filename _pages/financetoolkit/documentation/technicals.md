---
title: Technicals
seo_title: Technicals Module Documentation – Finance Toolkit
excerpt: The Technicals Module contains 30+ Technical Indicators that can be used to analyse companies. These ratios are divided into 4 categories which are breadth, momentum, overlap and volatility. Each indicator is calculated using the data from the Toolkit module.
description: "Reference for every function and parameter in the Finance Toolkit's Technicals module: 30+ breadth, momentum, overlap and volatility indicators in Python."
author_profile: false
permalink: /projects/financetoolkit/docs/technicals
classes: wide-sidebar
layout: single
redirect_from:
    - /technicals
sidebar:
    nav: "financetoolkit-docs-technicals"
---

The Technicals Module contains 30+ technical indicators divided into 4 categories: breadth, momentum, overlap and volatility.

To install the FinanceToolkit it simply requires the following:

```python
pip install financetoolkit -U
```

{% include algolia.html %}

## collect_all_indicators
Calculates all Technical Indicators based on the data provided.

**Args:**

- <u>period (str, optional):</u> The period to use for the calculation. Defaults to "daily".
- <u>window (int, optional):</u> The number of days to use for the calculation. Defaults to 14.
- <u>close_column (str, optional):</u> The column to use for the calculation. Defaults to "Adj Close".
- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
- <u>lag (int \| list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.Series or pd.DataFrame: Technical indicators calculated based on the specified parameters.

**Notes:**

- The method calculates various types of technical indicators for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the indicator values
using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.collect_all_indicators().xs("AAPL", level=1, axis="columns")
```

Which returns:

| Date       |   Bollinger Band Upper |   Bollinger Band Middle |   Bollinger Band Lower |   True Range |
|:-----------|-----------------------:|------------------------:|-----------------------:|-------------:|
| 2026-06-18 |                316.843 |                 300.742 |                284.642 |         4.95 |
| 2026-06-22 |                315.955 |                 300.078 |                284.201 |         5.66 |
| 2026-06-23 |                312.09  |                 298.585 |                285.08  |         7.46 |
| 2026-06-24 |                309.328 |                 297.358 |                285.388 |         6.76 |
| 2026-06-25 |                309.176 |                 294.781 |                280.386 |        19.33 |
| 2026-06-26 |                306.652 |                 293.098 |                279.544 |        11.74 |
| 2026-06-29 |                305.571 |                 291.684 |                277.796 |         8.52 |
| 2026-06-30 |                305.53  |                 291.599 |                277.667 |         9.24 |
| 2026-07-01 |                305.81  |                 291.799 |                277.788 |         7.39 |
| 2026-07-02 |                309.318 |                 292.727 |                276.137 |        15.74 |

---

## collect_breadth_indicators
Calculates and collects various breadth indicators based on the provided data.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The name of the column containing the close prices.
Defaults to "Adj Close".
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to.
Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int \| list[int], optional):</u> The lag to use for the growth calculation.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
Defaults to 1.

**Returns:**

pd.Series or pd.DataFrame: Breadth indicators calculated based on the specified parameters.

**Notes:**

- The method calculates various breadth indicators for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the indicator values
using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.collect_breadth_indicators().xs("AAPL", level=1, axis="columns")
```

Which returns:

| Date       |   McClellan Oscillator |   Advancers - Decliners |   On-Balance Volume |
|:-----------|-----------------------:|------------------------:|--------------------:|
| 2026-06-18 |                 5.1473 |                  298.01 |         4.50241e+09 |
| 2026-06-22 |                 4.8047 |                  297.01 |         4.45753e+09 |
| 2026-06-23 |                 4.3522 |                  294.3  |         4.40552e+09 |
| 2026-06-24 |                 3.8826 |                  293.08 |         4.35243e+09 |
| 2026-06-25 |                 2.5652 |                  275.15 |         4.24518e+09 |
| 2026-06-26 |                 1.8575 |                  283.78 |         4.50696e+09 |
| 2026-06-29 |                 1.1411 |                  281.74 |         4.44053e+09 |
| 2026-06-30 |                 0.9039 |                  289.36 |         4.50563e+09 |
| 2026-07-01 |                 0.9476 |                  294.38 |         4.55579e+09 |
| 2026-07-02 |                 1.6926 |                  308.63 |         4.63119e+09 |

---

## get_mcclellan_oscillator
Calculate the McClellan Oscillator for a given price series.

The McClellan Oscillator is a breadth indicator that measures the difference between the exponential moving average of advancing stocks and the exponential moving average of declining stocks.

The formula is as follows:

$$
\text{McClellan Oscillator} = \operatorname{EMA}(\text{Advancers}) - \operatorname{EMA}(\text{Decliners})
$$

**Also known as:** McClellan oscillator, market breadth.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The name of the column containing the close prices.
Defaults to "Adj Close".
- <u>short_ema_window (int, optional):</u> The window size for the short-term EMA.
Defaults to 19.
- <u>long_ema_window (int, optional):</u> The window size for the long-term EMA.
Defaults to 39.
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to.
Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int \| list[int], optional):</u> The lag to use for the growth calculation.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
Defaults to 1.

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

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_mcclellan_oscillator()
```

Which returns:

| Date       |   AAPL |     MSFT |   Benchmark |
|:-----------|-------:|---------:|------------:|
| 2026-06-18 | 5.1473 |  -4.4405 |      9.1566 |
| 2026-06-22 | 4.8047 |  -6.079  |      8.7467 |
| 2026-06-23 | 4.3522 |  -7.1196 |      7.8119 |
| 2026-06-24 | 3.8826 |  -8.3976 |      6.9567 |
| 2026-06-25 | 2.5652 | -10.0799 |      6.2436 |
| 2026-06-26 | 1.8575 | -10.4608 |      5.3373 |
| 2026-06-29 | 1.1411 | -10.9542 |      5.1361 |
| 2026-06-30 | 0.9039 | -11.0988 |      5.227  |
| 2026-07-01 | 0.9476 | -10.6039 |      5.228  |
| 2026-07-02 | 1.6926 |  -9.8173 |      5.1538 |

---

## get_advancers_decliners
Calculate the Advancers/Decliners ratio for a given price series.

The Advancers/Decliners ratio is a breadth indicator that measures the number of advancing stocks (stocks with positive price changes) versus the number of declining stocks (stocks with negative price changes).

The formula is as follows:

$$
\text{Advancers} / \text{Decliners} = \text{Advancers} / \text{Decliners}
$$

**Also known as:** advance decline ratio, market breadth.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The name of the column containing the close prices.
Defaults to "Adj Close".
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to.
Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int \| list[int], optional):</u> The lag to use for the growth calculation.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
Defaults to 1.

**Returns:**

pd.Series or pd.DataFrame: Advancers/Decliners ratio values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the Advancers/Decliners ratio for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the indicator values
using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_advancers_decliners()
```

Which returns:

| Date       |   AAPL |   MSFT |   Benchmark |
|:-----------|-------:|-------:|------------:|
| 2026-06-18 | 298.01 | 379.4  |      746.74 |
| 2026-06-22 | 297.01 | 367.34 |      744.39 |
| 2026-06-23 | 294.3  | 373.94 |      733.58 |
| 2026-06-24 | 293.08 | 365.46 |      733.24 |
| 2026-06-25 | 275.15 | 352.83 |      734.3  |
| 2026-06-26 | 283.78 | 372.97 |      728.99 |
| 2026-06-29 | 281.74 | 368.57 |      741    |
| 2026-06-30 | 289.36 | 373.02 |      746.77 |
| 2026-07-01 | 294.38 | 384.28 |      745.76 |
| 2026-07-02 | 308.63 | 390.49 |      744.78 |

---

## get_on_balance_volume
Calculate the On-Balance Volume (OBV) for a given price series.

The On-Balance Volume (OBV) is a technical indicator that uses volume flow to predict changes in stock price. It accumulates the volume on up days and subtracts the volume on down days. The resulting OBV line provides insights into the buying and selling pressure behind price movements.

The formula is as follows:

$$
\text{OBV} = \text{Previous OBV} + \text{Current Volume if Close} > \text{Previous Close}
$$

**Also known as:** OBV, volume momentum.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to.
Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the OBV.
Defaults to False.
- <u>lag (int \| list[int], optional):</u> The lag to use for the growth calculation.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
Defaults to 1.

**Returns:**

pd.Series or pd.DataFrame: On-Balance Volume values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates On-Balance Volume
for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the OBV using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_on_balance_volume()
```

Which returns:

| Date       |        AAPL |        MSFT |   Benchmark |
|:-----------|------------:|------------:|------------:|
| 2026-06-18 | 4.50241e+09 | 3.51706e+08 | 1.39684e+09 |
| 2026-06-22 | 4.45753e+09 | 3.06535e+08 | 1.35021e+09 |
| 2026-06-23 | 4.40552e+09 | 3.47183e+08 | 1.28336e+09 |
| 2026-06-24 | 4.35243e+09 | 3.02673e+08 | 1.22592e+09 |
| 2026-06-25 | 4.24518e+09 | 2.36312e+08 | 1.28005e+09 |
| 2026-06-26 | 4.50696e+09 | 4.22514e+08 | 1.20902e+09 |
| 2026-06-29 | 4.44053e+09 | 3.71284e+08 | 1.26705e+09 |
| 2026-06-30 | 4.50563e+09 | 4.1623e+08  | 1.32268e+09 |
| 2026-07-01 | 4.55579e+09 | 4.64295e+08 | 1.27558e+09 |
| 2026-07-02 | 4.63119e+09 | 5.0649e+08  | 1.21807e+09 |

---

## get_accumulation_distribution_line
Calculate the Accumulation/Distribution Line for a given price series.

The Accumulation/Distribution Line is a technical indicator that evaluates the flow of money into or out of an asset. It takes into account both price and volume information to identify whether an asset is being accumulated (bought) or distributed (sold) by investors.

The formula is as follows:

$$
\text{ADL} = \text{Previous ADL} + \text{Current ADL}
$$

**Also known as:** ADL, Chaikin ADL, volume-price trend.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to.
Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Accumulation/Distribution Line.
Defaults to False.
- <u>lag (int \| list[int], optional):</u> The lag to use for the growth calculation.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
Defaults to 1.

**Returns:**

pd.Series or pd.DataFrame: Accumulation/Distribution Line values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates the
Accumulation/Distribution Line for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the Accumulation/Distribution Line
using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_accumulation_distribution_line()
```

Which returns:

| Date       |        AAPL |        MSFT |   Benchmark |
|:-----------|------------:|------------:|------------:|
| 2026-06-18 | 4.92368e+09 | 1.8149e+09  | 9.17282e+09 |
| 2026-06-22 | 4.88276e+09 | 1.77141e+09 | 9.14286e+09 |
| 2026-06-23 | 4.83242e+09 | 1.77134e+09 | 9.09936e+09 |
| 2026-06-24 | 4.78154e+09 | 1.73113e+09 | 9.07218e+09 |
| 2026-06-25 | 4.69424e+09 | 1.69682e+09 | 9.07013e+09 |
| 2026-06-26 | 4.85924e+09 | 1.81902e+09 | 9.08747e+09 |
| 2026-06-29 | 4.82229e+09 | 1.81091e+09 | 9.13864e+09 |
| 2026-06-30 | 4.87922e+09 | 1.8407e+09  | 9.17476e+09 |
| 2026-07-01 | 4.89938e+09 | 1.85739e+09 | 9.17276e+09 |
| 2026-07-02 | 4.96721e+09 | 1.8826e+09  | 9.16369e+09 |

---

## get_chaikin_oscillator
Calculate the Chaikin Oscillator for a given price series.

The Chaikin Oscillator is a momentum-based indicator that combines price and volume to help identify potential trends and reversals in the market. It is calculated as the difference between the 3-day and 10-day Accumulation/Distribution Line.

The formula is as follows:

$$
\text{Chaikin Oscillator} = \operatorname{EMA}(\text{short-window ADL}) - \operatorname{EMA}(\text{long-window ADL})
$$

**Also known as:** Chaikin oscillator, volume accumulation.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>short_window (int, optional):</u> Number of periods for the short-term moving average.
Defaults to 3.
- <u>long_window (int, optional):</u> Number of periods for the long-term moving average.
Defaults to 10.
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to.
Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Chaikin Oscillator.
Defaults to False.
- <u>lag (int \| list[int], optional):</u> The lag to use for the growth calculation.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
Defaults to 1.

**Returns:**

pd.Series or pd.DataFrame: Chaikin Oscillator values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates the
Chaikin Oscillator for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the Chaikin Oscillator
using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_chaikin_oscillator()
```

Which returns:

| Date       |         AAPL |         MSFT |    Benchmark |
|:-----------|-------------:|-------------:|-------------:|
| 2026-06-18 | -1.81858e+07 | -3.96544e+06 | -3.10439e+07 |
| 2026-06-22 | -2.9078e+07  | -1.41917e+07 | -3.73954e+07 |
| 2026-06-23 | -4.6907e+07  | -1.71047e+07 | -5.04353e+07 |
| 2026-06-24 | -6.61266e+07 | -2.95377e+07 | -5.98313e+07 |
| 2026-06-25 | -9.57547e+07 | -4.28543e+07 | -5.88882e+07 |
| 2026-06-26 | -4.66693e+07 | -5.52418e+06 | -4.76316e+07 |
| 2026-06-29 | -3.41049e+07 |  7.66983e+06 | -2.24146e+07 |
| 2026-06-30 | -7.75122e+06 |  2.18471e+07 |  1.4324e+06  |
| 2026-07-01 |  1.01493e+07 |  3.09708e+07 |  1.0421e+07  |
| 2026-07-02 |  3.81324e+07 |  3.99114e+07 |  1.02634e+07 |

---

## get_chaikin_money_flow
Calculate the Chaikin Money Flow (CMF) for a given price series.

The Chaikin Money Flow sums the same Money Flow Volume used by the Accumulation/ Distribution Line over a rolling window and normalizes it by the window's total volume, turning the running (unbounded) Accumulation/Distribution Line into a bounded oscillator. Sustained readings above zero indicate buying pressure (accumulation) is dominating over the window, while sustained readings below zero indicate selling pressure (distribution).

The formula is as follows:

$$
\text{Money Flow Multiplier} = ((\text{Close} - \text{Low}) - (\text{High} - \text{Close})) / (\text{High} - \text{Low})
$$

$$
\text{Money Flow Volume} = \text{Money Flow Multiplier} \cdot \text{Volume}
$$

$$
\text{CMF} = \operatorname{Sum}(\text{Money Flow Volume},\; \text{window}) / \operatorname{Sum}(\text{Volume},\; \text{window})
$$

**Also known as:** CMF, Chaikin Money Flow.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int, optional):</u> Number of periods to sum the Money Flow Volume and
volume over. Defaults to 20.
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to.
Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Chaikin Money Flow.
Defaults to False.
- <u>lag (int \| list[int], optional):</u> The lag to use for the growth calculation.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
Defaults to 1.

**Returns:**

pd.Series or pd.DataFrame: Chaikin Money Flow values, bounded between -1 and 1.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the Chaikin Money Flow for each asset in the Toolkit instance.
- There is no formal journal citation for the Chaikin Money Flow; the standard
textbook treatment is Murphy, J.J. (1999). "Technical Analysis of the Financial
Markets." New York Institute of Finance.
- If `growth` is set to True, the method calculates the growth of the Chaikin Money
Flow using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_chaikin_money_flow()
```

---

## get_ease_of_movement
Calculate the Ease of Movement (EMV) for a given price series.

The Ease of Movement indicator relates how far price moved (the change in the midpoint of the high-low range from one period to the next) to the volume required to move it (via the "Box Ratio", volume scaled down and divided by the period's high-low range). High positive readings mean price is moving up easily on relatively little volume; high negative readings mean price is moving down easily on relatively little volume. The raw daily reading is smoothed with a Simple Moving Average to reduce noise.

The formula is as follows:

$$
\text{Distance Moved} = (\operatorname{High}(t) + \operatorname{Low}(t)) / 2 - (\operatorname{High}(t-1) + \operatorname{Low}(t-1)) / 2
$$

$$
\text{Box Ratio} = (\text{Volume} / \text{volume\_divisor}) / (\text{High} - \text{Low})
$$

$$
\text{Raw EMV} = \text{Distance Moved} / \text{Box Ratio}
$$

$$
\text{EMV} = \operatorname{SMA}(\text{Raw EMV},\; \text{window})
$$

**Also known as:** EMV, Ease of Movement.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int, optional):</u> Number of periods used to smooth the raw Ease of
Movement values with a Simple Moving Average. Defaults to 14.
- <u>volume_divisor (float, optional):</u> Scaling constant applied to volume so that the
Box Ratio (and therefore EMV) stays in a readable range regardless of an
asset's typical share volume. Defaults to 100,000,000.
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to.
Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Ease of Movement.
Defaults to False.
- <u>lag (int \| list[int], optional):</u> The lag to use for the growth calculation.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
Defaults to 1.

**Returns:**

pd.Series or pd.DataFrame: Ease of Movement values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the Ease of Movement for each asset in the Toolkit instance.
- Reference: Arms, R.W. (1989). "The Arms - <u>Index (TRIN):</u> An Introduction to the
Volume Analysis of Stock and Bond Markets." Business One Irwin.
- If `growth` is set to True, the method calculates the growth of the Ease of
Movement using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_ease_of_movement()
```

---

## get_negative_volume_index
Calculate the Negative Volume Index (NVI) for a given price series.

The Negative Volume Index is a cumulative index that only updates on days where volume decreases from the prior period, compounding that day's percentage price change onto the running index; on days where volume increases (or stays flat), the index is carried forward unchanged. The premise, per Fosback, is that "smart money" tends to be active on low-volume (quiet) days, so tracking price behaviour specifically on those days isolates informed trading from the noise of high-volume, crowd-driven days.

The formula is as follows:

$$
\operatorname{Index}(t) = \operatorname{Index}(t-1) \cdot (1 + (\operatorname{Close}(t) / \operatorname{Close}(t-1) - 1)) \text{if Volume} (t) < \operatorname{Volume}(t-1)
$$

$$
\operatorname{Index}(t) = \operatorname{Index}(t-1) \text{otherwise}
$$

**Also known as:** NVI, Negative Volume Index.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>start_value (float, optional):</u> The index value to start the series at.
Defaults to 1000.0.
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to.
Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Negative Volume Index.
Defaults to False.
- <u>lag (int \| list[int], optional):</u> The lag to use for the growth calculation.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
Defaults to 1.

**Returns:**

pd.Series or pd.DataFrame: Negative Volume Index values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the Negative Volume Index for each asset in the Toolkit instance.
- Reference: Fosback, N.G. (1976). "Stock Market Logic: A Sophisticated Approach to
Profits on Wall Street." The Institute for Econometric Research.
- If `growth` is set to True, the method calculates the growth of the Negative Volume
Index using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_negative_volume_index()
```

---

## get_positive_volume_index
Calculate the Positive Volume Index (PVI) for a given price series.

The Positive Volume Index mirrors the Negative Volume Index: it is a cumulative index that only updates on days where volume increases from the prior period, compounding that day's percentage price change onto the running index; on days where volume decreases (or stays flat), the index is carried forward unchanged. Per Fosback, the Positive Volume Index isolates price behaviour on high-volume (crowd-driven) days, which is traditionally read as tracking less-informed, sentiment-driven trading.

The formula is as follows:

$$
\operatorname{Index}(t) = \operatorname{Index}(t-1) \cdot (1 + (\operatorname{Close}(t) / \operatorname{Close}(t-1) - 1)) \text{if Volume} (t) > \operatorname{Volume}(t-1)
$$

$$
\operatorname{Index}(t) = \operatorname{Index}(t-1) \text{otherwise}
$$

**Also known as:** PVI, Positive Volume Index.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>start_value (float, optional):</u> The index value to start the series at.
Defaults to 1000.0.
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to.
Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Positive Volume Index.
Defaults to False.
- <u>lag (int \| list[int], optional):</u> The lag to use for the growth calculation.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
Defaults to 1.

**Returns:**

pd.Series or pd.DataFrame: Positive Volume Index values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the Positive Volume Index for each asset in the Toolkit instance.
- Reference: Fosback, N.G. (1976). "Stock Market Logic: A Sophisticated Approach to
Profits on Wall Street." The Institute for Econometric Research.
- If `growth` is set to True, the method calculates the growth of the Positive Volume
Index using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_positive_volume_index()
```

---

## collect_momentum_indicators
Calculates and collects various momentum indicators based on the provided data.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
- <u>window (int, optional):</u> The window size for calculating indicators.
Defaults to 14.
- <u>close_column (str, optional):</u> The name of the column containing the close prices.
Defaults to "Adj Close".
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to.
Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int \| list[int], optional):</u> The lag to use for the growth calculation.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
Defaults to 1.

**Returns:**

pd.Series or pd.DataFrame: Momentum indicators calculated based on the specified parameters.

**Notes:**

- The method calculates various momentum indicators for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the indicator values
using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.collect_momentum_indicators().xs("AAPL", level=1, axis="columns")
```

Which returns:

| Date       |   Ichimoku Leading Span A |   Ichimoku Leading Span B |   Stochastic %K |   Stochastic %D |
|:-----------|--------------------------:|--------------------------:|----------------:|----------------:|
| 2026-06-18 |                   307.225 |                   286.8   |         35.4097 |         34.4881 |
| 2026-06-22 |                   306.55  |                   287.03  |         32.0786 |         32.012  |
| 2026-06-23 |                   302.59  |                   287.295 |         23.0513 |         30.1799 |
| 2026-06-24 |                   302.39  |                   287.605 |         18.9873 |         24.7058 |
| 2026-06-25 |                   302.39  |                   289.335 |          3.2073 |         15.082  |
| 2026-06-26 |                   302.39  |                   291.235 |         22.9782 |         15.0576 |
| 2026-06-29 |                   302.39  |                   291.235 |         27.8689 |         18.0181 |
| 2026-06-30 |                   302.39  |                   291.235 |         54.4472 |         35.0981 |
| 2026-07-01 |                   302.39  |                   291.235 |         71.9567 |         51.4243 |
| 2026-07-02 |                   302.39  |                   291.235 |         97.7853 |         74.7297 |

---

## get_money_flow_index
Calculate the Money Flow Index (MFI) for a given price series.

The Money Flow Index is a momentum indicator that measures the strength and direction of money flowing in and out of a security by considering both price and volume.

The formula is as follows:

$$
\text{MFI} = 100 - (100 / (1 + (\text{positive\_money\_flow} / \text{negative\_money\_flow})))
$$

**Also known as:** MFI, volume-weighted RSI.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The name of the column containing the close prices.
Defaults to "Adj Close".
- <u>window (int, optional):</u> The number of periods for calculating the MFI.
Defaults to 14.
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to.
Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int \| list[int], optional):</u> The lag to use for the growth calculation.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
Defaults to 1.

**Returns:**

pd.Series or pd.DataFrame: Money Flow Index (MFI) values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the MFI values for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the indicator values
using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_money_flow_index()
```

Which returns:

| Date       |    AAPL |    MSFT |   Benchmark |
|:-----------|--------:|--------:|------------:|
| 2026-06-18 | 34.2012 | 17.0425 |     45.4099 |
| 2026-06-22 | 40.4098 |  6.0393 |     40.4024 |
| 2026-06-23 | 33.9909 | 13.2653 |     35.5328 |
| 2026-06-24 | 34.0195 | 13.2877 |     35.3632 |
| 2026-06-25 | 31.7751 | 12.5721 |     29.9219 |
| 2026-06-26 | 50.9525 | 34.8784 |     30.7073 |
| 2026-06-29 | 58.3251 | 40.8726 |     36.5958 |
| 2026-06-30 | 65.173  | 46.3834 |     44.023  |
| 2026-07-01 | 70.4341 | 51.8574 |     49.9149 |
| 2026-07-02 | 71.4645 | 57.9088 |     41.6417 |

---

## get_williams_percent_r
Calculate the Williams Percent R (Williams %R) for a given price series.

The Williams %R is a momentum indicator that measures the level of the close price relative to the high-low range over a certain number of periods.

The formula is as follows:

$$
\text{Williams} \%R = (\text{Highest High} - \text{Close}) / (\text{Highest High} - \text{Lowest Low}) \cdot - 100
$$

**Also known as:** Williams percent R, overbought oversold oscillator.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The name of the column containing the close prices.
Defaults to "Adj Close".
- <u>window (int, optional):</u> The number of periods for calculating the Williams %R.
Defaults to 14.
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to.
Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int \| list[int], optional):</u> The lag to use for the growth calculation.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
Defaults to 1.

**Returns:**

pd.Series or pd.DataFrame: Williams %R values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the Williams %R values for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the indicator values
using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_williams_percent_r()
```

Which returns:

| Date       |     AAPL |     MSFT |   Benchmark |
|:-----------|---------:|---------:|------------:|
| 2026-06-18 | -64.5903 | -93.4222 |    -36.128  |
| 2026-06-22 | -67.9214 | -99.6876 |    -42.3433 |
| 2026-06-23 | -76.9487 | -90.6301 |    -69.6493 |
| 2026-06-24 | -81.0127 | -99.0472 |    -70.1848 |
| 2026-06-25 | -96.7927 | -95.4778 |    -65.6498 |
| 2026-06-26 | -77.0218 | -65.0235 |    -69.0524 |
| 2026-06-29 | -72.1311 | -69.1462 |    -39.1022 |
| 2026-06-30 | -45.5528 | -57.3424 |    -24.7132 |
| 2026-07-01 | -28.0433 | -33.2445 |    -27.2319 |
| 2026-07-02 |  -2.2147 | -21.4272 |    -29.6758 |

---

## get_aroon_indicator
Calculate the Aroon Indicator for a given price series.

The Aroon Indicator is an oscillator that measures the strength of a trend and the likelihood of its continuation or reversal.

The formula is as follows:

$$
\text{Aroon Up} = ((\text{Number of periods}) - (\text{Number of periods since highest high})) / (\text{Number of periods}) \cdot 100
$$

**Also known as:** Aroon Up, Aroon Down, trend strength.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
- <u>window (int, optional):</u> The number of periods for calculating the Aroon Indicator.
Defaults to 14.
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to.
Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int \| list[int], optional):</u> The lag to use for the growth calculation.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
Defaults to 1.

**Returns:**

pd.Series or pd.DataFrame:
Aroon Indicator values for the upward and downward trends.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the Aroon Indicator values for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the indicator values
using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_aroon_indicator().xs("AAPL", level=1, axis="columns")
```

Which returns:

| Date       |   Aroon Down |   Aroon Up |
|:-----------|-------------:|-----------:|
| 2026-06-18 |      50      |    64.2857 |
| 2026-06-22 |      57.1429 |    71.4286 |
| 2026-06-23 |      64.2857 |    78.5714 |
| 2026-06-24 |      71.4286 |    85.7143 |
| 2026-06-25 |       7.1429 |    92.8571 |
| 2026-06-26 |      14.2857 |   100      |
| 2026-06-29 |      21.4286 |    42.8571 |
| 2026-06-30 |      28.5714 |    50      |
| 2026-07-01 |      35.7143 |    57.1429 |
| 2026-07-02 |      42.8571 |     7.1429 |

---

## get_commodity_channel_index
Calculate the Commodity Channel Index (CCI) for a given price series.

The Commodity Channel Index is an oscillator that measures the current price level relative to an average price level over a specified period.

The formula is as follows:

$$
\text{CCI} = (\text{Typical Price} - \operatorname{SMA}(\text{Typical Price})) / (\text{constant} \cdot \text{Mean Deviation})
$$

**Also known as:** CCI, cyclical trend indicator.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column in the historical data that represents
the closing prices. Defaults to "Adj Close".
- <u>window (int, optional):</u> The number of periods for calculating the CCI.
Defaults to 14.
- <u>constant (float, optional):</u> Constant multiplier used in the CCI calculation.
Defaults to 0.015.
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to.
Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int \| list[int], optional):</u> The lag to use for the growth calculation.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
Defaults to 1.

**Returns:**

pd.Series or pd.DataFrame: Commodity Channel Index (CCI) values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the CCI values for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the indicator values
using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_commodity_channel_index()
```

Which returns:

| Date       |      AAPL |     MSFT |   Benchmark |
|:-----------|----------:|---------:|------------:|
| 2026-06-18 |  -29.8087 | -96.1785 |      0.3891 |
| 2026-06-22 |  -18.6411 | -97.7637 |      4.5369 |
| 2026-06-23 |  -28.0495 | -75.0122 |    -75.9764 |
| 2026-06-24 |  -31.5076 | -70.1223 |    -67.2592 |
| 2026-06-25 | -146.597  | -87.7738 |    -56.5227 |
| 2026-06-26 | -101.005  | -42.5782 |   -105.047  |
| 2026-06-29 |  -67.6738 | -31.457  |    -11.134  |
| 2026-06-30 |  -42.7183 | -21.1814 |     50.4596 |
| 2026-07-01 |   11.4352 |  12.9724 |     53.1052 |
| 2026-07-02 |  102.962  |  33.0344 |     43.6351 |

---

## get_relative_vigor_index
Calculate the Relative Vigor Index (RVI) for a given price series.

The Relative Vigor Index is an oscillator that measures the conviction of a current price trend using the relationship between closing and opening prices.

The formula is as follows:

$$
\text{RVI} = \operatorname{Sum}(\text{Upward Close-Open Movement},\; \text{window}) / (\operatorname{Sum}(\text{Upward Close-Open Movement},\; \text{window}) + \operatorname{Sum}(\text{Downward Close-Open Movement},\; \text{window}))
$$

**Also known as:** vigor index. Note this is a bounded [0, 1] measure of the proportion of upward close-open movement, related in spirit to (but not numerically the same as) John Ehlers' published Relative Vigor Index. See `momentum_model.get_relative_vigor_index` for the full formula and caveats.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column in the historical data that represents
the closing prices. Defaults to "Adj Close".
- <u>window (int, optional):</u> The number of periods for calculating the RVI.
Defaults to 14.
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to.
Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int \| list[int], optional):</u> The lag to use for the growth calculation.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
Defaults to 1.

**Returns:**

pd.Series or pd.DataFrame: Relative Vigor Index (RVI) values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the RVI values for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the indicator values
using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_relative_vigor_index()
```

Which returns:

| Date       |   AAPL |   MSFT |   Benchmark |
|:-----------|-------:|-------:|------------:|
| 2026-06-18 | 0.4036 | 0.0663 |      0.4484 |
| 2026-06-22 | 0.4352 | 0.0626 |      0.3655 |
| 2026-06-23 | 0.2163 | 0.091  |      0.319  |
| 2026-06-24 | 0.2251 | 0.0984 |      0.3306 |
| 2026-06-25 | 0.1793 | 0.095  |      0.2203 |
| 2026-06-26 | 0.397  | 0.4174 |      0.2946 |
| 2026-06-29 | 0.4175 | 0.3712 |      0.4362 |
| 2026-06-30 | 0.7891 | 0.4475 |      0.6846 |
| 2026-07-01 | 0.7922 | 0.5237 |      0.9267 |
| 2026-07-02 | 1.1745 | 0.7045 |      0.5225 |

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

**Also known as:** FI, Elder's Force Index.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column in the historical data that represents
the closing prices. Defaults to "Adj Close".
- <u>window (int, optional):</u> The number of periods for calculating the Force Index.
Defaults to 14.
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to.
Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int \| list[int], optional):</u> The lag to use for the growth calculation.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
Defaults to 1.

**Returns:**

pd.Series or pd.DataFrame: Force Index values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the Force Index values for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the indicator values
using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_force_index()
```

Which returns:

| Date       |         AAPL |         MSFT |    Benchmark |
|:-----------|-------------:|-------------:|-------------:|
| 2026-06-18 |  1.5469e+09  |  2.64103e+08 |  5.23308e+09 |
| 2026-06-22 | -7.46954e+08 | -6.39817e+09 | -2.13467e+09 |
| 2026-06-23 | -2.04451e+09 |  3.52532e+09 | -1.02007e+10 |
| 2026-06-24 | -9.23144e+08 | -4.57591e+09 | -3.22888e+08 |
| 2026-06-25 | -1.46857e+10 | -7.31369e+09 |  1.01111e+09 |
| 2026-06-26 |  8.76398e+09 |  1.47121e+10 | -4.94319e+09 |
| 2026-06-29 | -2.04817e+09 | -3.2984e+09  |  1.1285e+10  |
| 2026-06-30 |  7.61233e+09 |  3.37872e+09 |  5.23673e+09 |
| 2026-07-01 |  5.00175e+09 |  8.72373e+09 | -9.03283e+08 |
| 2026-07-02 |  1.4666e+10  |  4.77999e+09 | -8.48204e+08 |

---

## get_ultimate_oscillator
Calculate the Ultimate Oscillator for a given price series.

The Ultimate Oscillator is a momentum oscillator that combines short-term, mid-term, and long-term price momentum into a single value.

The formula is as follows:

$$
\operatorname{Average}(i) = \operatorname{Sum}(\text{Buying Pressure},\; \text{window}_{i}) / \operatorname{Sum}(\text{True Range},\; \text{window}_{i})
$$

$$
\text{Ultimate Oscillator} = 100 \cdot \left[(4 \cdot \text{Average}_{1}) + (2 \cdot \text{Average}_{2}) + \text{Average}_{3}\right] / 7
$$

**Also known as:** UO, ultimate momentum oscillator. See `momentum_model.get_ultimate_oscillator` for the Buying Pressure and True Range definitions.

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
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to.
Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int \| list[int], optional):</u> The lag to use for the growth calculation.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
Defaults to 1.

**Returns:**

pd.Series or pd.DataFrame: Ultimate Oscillator values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the Ultimate Oscillator values for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the indicator values
using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_ultimate_oscillator()
```

Which returns:

| Date       |   AAPL |    MSFT |   Benchmark |
|:-----------|-------:|--------:|------------:|
| 2026-06-18 | 5.7264 |  1.4313 |      5.7432 |
| 2026-06-22 | 5.7478 |  0.3073 |      5.6389 |
| 2026-06-23 | 4.1905 |  1.5815 |      3.88   |
| 2026-06-24 | 3.6773 |  1.0805 |      2.8505 |
| 2026-06-25 | 0.392  | -0.874  |      1.6945 |
| 2026-06-26 | 1.0483 |  0.9805 |      2.1519 |
| 2026-06-29 | 1.9469 |  2.2386 |      4.6356 |
| 2026-06-30 | 3.0712 |  3.2361 |      5.7923 |
| 2026-07-01 | 4.2231 |  4.5312 |      6.0908 |
| 2026-07-02 | 5.615  |  5.5004 |      6.4095 |

---

## get_percentage_price_oscillator
Calculate the Percentage Price Oscillator (PPO) for a given price series.

The Percentage Price Oscillator (PPO) is a momentum oscillator that measures the difference between two moving averages as a percentage of the longer moving average.

The formula is as follows:

$$
\text{PPO} = ((\text{Long-term EMA} - \text{Short-term EMA}) / \text{Short-term EMA}) \cdot 100
$$

**Also known as:** PPO, price oscillator.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column in the historical data that represents
the closing prices. Defaults to "Adj Close".
- <u>short_window (int, optional):</u> The number of periods for the short-term moving average.
Defaults to 7.
- <u>long_window (int, optional):</u> The number of periods for the long-term moving average.
Defaults to 28.
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to.
Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int \| list[int], optional):</u> The lag to use for the growth calculation.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
Defaults to 1.

**Returns:**

pd.Series or pd.DataFrame: Percentage Price Oscillator (PPO) values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the PPO values for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the indicator values
using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_percentage_price_oscillator()
```

Which returns:

| Date       |    AAPL |    MSFT |   Benchmark |
|:-----------|--------:|--------:|------------:|
| 2026-06-18 |  0.1732 | -4.0561 |      0.6878 |
| 2026-06-22 |  0.14   | -4.8668 |      0.6275 |
| 2026-06-23 | -0.0508 | -5.0611 |      0.3105 |
| 2026-06-24 | -0.2579 | -5.5078 |      0.0753 |
| 2026-06-25 | -1.5005 | -6.3251 |     -0.0644 |
| 2026-06-26 | -1.8165 | -5.8609 |     -0.2913 |
| 2026-06-29 | -2.1348 | -5.645  |     -0.15   |
| 2026-06-30 | -1.848  | -5.1917 |      0.0925 |
| 2026-07-01 | -1.304  | -4.2572 |      0.2353 |
| 2026-07-02 | -0.022  | -3.2398 |      0.3068 |

---

## get_detrended_price_oscillator
Calculate the Detrended Price Oscillator (DPO) for a given price series.

The Detrended Price Oscillator (DPO) is an indicator that helps identify short-term cycles by removing longer-term trends from prices.

The formula is as follows:

$$
\text{Displacement} = \operatorname{floor}(\text{Number of Periods} / 2) + 1
$$

$$
\text{DPO} = \operatorname{Close}(t - \text{Displacement}) - \operatorname{SMA}(\text{Close},\; \text{Number of Periods}) (t)
$$

**Also known as:** DPO, detrended price oscillator. Note the moving average itself is not shifted - only the close price used for the comparison is looked up further back in time; see `momentum_model.get_detrended_price_oscillator` for the full explanation.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column in the historical data that represents
the closing prices. Defaults to "Adj Close".
- <u>window (int, optional):</u> The number of periods to consider for the DPO calculation.
Defaults to 14.
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to.
Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int \| list[int], optional):</u> The lag to use for the growth calculation.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
Defaults to 1.

**Returns:**

pd.Series or pd.DataFrame: Detrended Price Oscillator (DPO) values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the DPO values for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the indicator values
using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_detrended_price_oscillator()
```

Which returns:

| Date       |     AAPL |     MSFT |   Benchmark |
|:-----------|---------:|---------:|------------:|
| 2026-06-18 | -16.7529 | -21.8536 |    -11.8786 |
| 2026-06-22 | -14.9607 | -26.2107 |    -22.3686 |
| 2026-06-23 | -10.2421 | -31.1771 |     -9.6843 |
| 2026-06-24 | -13.4786 | -28.7893 |     -5.4164 |
| 2026-06-25 |  -7.3379 | -18.6071 |      7.3607 |
| 2026-06-26 |  -3.6886 | -23.1914 |      2.87   |
| 2026-06-29 |  -5.7957 | -34.6771 |     -5.5257 |
| 2026-06-30 |  -2.7321 | -29.1271 |      0.95   |
| 2026-07-01 |  -3.0679 | -34.5314 |     -0.3893 |
| 2026-07-02 |  -4.285  | -23.1193 |     -9.3429 |

---

## get_average_directional_index
Calculate the Average Directional Index (ADX) for a given price series.

The Average Directional Index (ADX) is an indicator that measures the strength of a trend, whether it's an uptrend or a downtrend.

The formula is as follows:

$$
\text{ADX} = \text{Wilder's Smoothed Moving Average of DX},\;\; \text{where} \;\; \text{DX} = 100 \cdot | \text{+DI} - \text{-DI} | / (\text{+DI} + \text{-DI})
$$

**Also known as:** ADX, trend strength indicator. See `momentum_model.get_average_directional_index` for the full formula, which uses Wilder's smoothing (not a plain SMA) throughout.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column in the historical data that represents
the closing prices. Defaults to "Adj Close".
- <u>window (int, optional):</u> The number of periods to consider for the ADX calculation.
Defaults to 14.
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to.
Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int \| list[int], optional):</u> The lag to use for the growth calculation.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
Defaults to 1.

**Returns:**

pd.DataFrame or pd.Series: Average Directional Index (ADX) values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the ADX values for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the indicator values
using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_average_directional_index()
```

Which returns:

| Date       |    AAPL |    MSFT |   Benchmark |
|:-----------|--------:|--------:|------------:|
| 2026-06-18 | 31.7885 | 26.0482 |     24.8516 |
| 2026-06-22 | 28.0539 | 27.1817 |     25.2744 |
| 2026-06-23 | 25.3719 | 29.9043 |     25.3022 |
| 2026-06-24 | 23.5607 | 33.0223 |     26.3917 |
| 2026-06-25 | 23.3155 | 36.6469 |     28.5969 |
| 2026-06-26 | 24.2698 | 40.1891 |     31.1122 |
| 2026-06-29 | 25.7674 | 43.281  |     33.5671 |
| 2026-06-30 | 27.545  | 44.9576 |     33.0473 |
| 2026-07-01 | 27.4563 | 45.3851 |     31.753  |
| 2026-07-02 | 27.743  | 43.8357 |     30.2519 |

---

## get_chande_momentum_oscillator
Calculate the Chande Momentum Oscillator (CMO) for a given price series.

The Chande Momentum Oscillator is an indicator that measures the momentum of a price series and identifies overbought and oversold conditions.

The formula is as follows:

$$
\text{CMO} = ((\text{Sum of Upward Change}) - (\text{Sum of Downward Change})) / ((\text{Sum of Upward Change}) + (\text{Sum of Downward Change}))
$$

**Also known as:** CMO, Chande momentum.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column in the historical data that represents
the closing prices. Defaults to "Adj Close".
- <u>window (int, optional):</u> The number of periods to consider for the CMO calculation.
Defaults to 14.
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to.
Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int \| list[int], optional):</u> The lag to use for the growth calculation.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
Defaults to 1.

**Returns:**

pd.Series or pd.DataFrame: Chande Momentum Oscillator values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the Chande Momentum Oscillator values for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the indicator values
using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_chande_momentum_oscillator()
```

Which returns:

| Date       |     AAPL |     MSFT |   Benchmark |
|:-----------|---------:|---------:|------------:|
| 2026-06-18 | -21.8609 | -62.8906 |    -10.2182 |
| 2026-06-22 | -15.625  | -81.4368 |    -14.7997 |
| 2026-06-23 | -39.1826 | -66.1723 |    -24.6608 |
| 2026-06-24 | -34.6231 | -64.2442 |    -20.9163 |
| 2026-06-25 | -54.1904 | -69.4937 |    -23.1112 |
| 2026-06-26 | -33.0342 | -37.3504 |    -10.1446 |
| 2026-06-29 | -29.3073 | -37.0653 |      1.8792 |
| 2026-06-30 |  -1.8539 | -26.9917 |      9.8861 |
| 2026-07-01 |   4.1068 | -11.1036 |     23.1787 |
| 2026-07-02 |  16.5859 |   0.1282 |      9.1933 |

---

## get_ichimoku_cloud
Calculate the Ichimoku Cloud indicator for a given price series.

The Ichimoku Cloud, also known as the Ichimoku Kinko Hyo, is a versatile indicator that defines support and resistance, identifies trend direction, gauges momentum, and provides trading signals.

The formula is as follows:

$$
\text{Conversion Line} = (\text{Highest High} + \text{Lowest Low}) / 2,\;\; \text{over conversion\_window periods}
$$

$$
\text{Base Line} = (\text{Highest High} + \text{Lowest Low}) / 2,\;\; \text{over base\_window periods}
$$

$$
\text{Leading Span} A = ((\text{Conversion Line} + \text{Base Line}) / 2),\;\; \text{shifted forward base\_window periods}
$$

$$
\text{Leading Span} B = (\text{Highest High} + \text{Lowest Low}) / 2 \text{over} \text{lead\_span\_b\_window} \text{periods},\;\; \text{shifted forward base\_window periods}
$$

**Also known as:** Ichimoku Kinko Hyo, cloud indicator. The default windows (9, 26, 52) are Goichi Hosoda's original values, both leading spans are conventionally displaced forward by the base (Kijun-sen) period.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
- <u>conversion_window (int, optional):</u> The number of periods to consider for the
Conversion Line (Tenkan-sen) calculation. Defaults to 9.
- <u>base_window (int, optional):</u> The number of periods to consider for the Base Line
(Kijun-sen) calculation, also used as the forward displacement for both
Leading Spans. Defaults to 26.
- <u>lead_span_b_window (int, optional):</u> The number of periods to consider for the
Lead Span B (Senkou Span B) calculation. Defaults to 52.
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to.
Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int \| list[int], optional):</u> The lag to use for the growth calculation.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
Defaults to 1.

**Returns:**

pd.Series or pd.DataFrame:
Conversion Line, Base Line, Lead Span A, and Lead Span B values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the Ichimoku Cloud values for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the indicator values
using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_ichimoku_cloud().xs("AAPL", level=1, axis="columns")
```

Which returns:

| Date       |   Base Line |   Conversion Line |   Leading Span A |   Leading Span B |
|:-----------|------------:|------------------:|-----------------:|-----------------:|
| 2026-06-18 |     302.39  |           302.39  |          307.225 |          286.8   |
| 2026-06-22 |     302.39  |           294.9   |          306.55  |          287.03  |
| 2026-06-23 |     302.39  |           294.9   |          302.59  |          287.295 |
| 2026-06-24 |     302.39  |           296.005 |          302.39  |          287.605 |
| 2026-06-25 |     295.575 |           288.085 |          302.39  |          289.335 |
| 2026-06-26 |     295.575 |           288.085 |          302.39  |          291.235 |
| 2026-06-29 |     295.575 |           288.085 |          302.39  |          291.235 |
| 2026-06-30 |     295.575 |           288.085 |          302.39  |          291.235 |
| 2026-07-01 |     295.575 |           288.085 |          302.39  |          291.235 |
| 2026-07-02 |     295.575 |           291.585 |          302.39  |          291.235 |

---

## get_stochastic_oscillator
Calculate the Stochastic Oscillator indicator for a given price series.

The Stochastic Oscillator is a momentum indicator that shows the location of the close relative to the high-low range over a set number of periods. It consists of the %K line (fast) and the %D line (slow).

The formula is as follows:

$$
\%K = 100 \cdot ((\text{Close} - \text{Lowest Low}) / (\text{Highest High} - \text{Lowest Low}))
$$

$$
\%D = \operatorname{SMA}(\%K,\; \text{smooth\_window})
$$

**Also known as:** stochastic oscillator, percent K, percent D.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int, optional):</u> The number of periods to consider for the %K line calculation.
Defaults to 14.
- <u>smooth_window (int, optional):</u> The number of periods used to smooth the %K line
into the %D signal line. Defaults to 3.
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to.
Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the %K and %D values.
Defaults to False.
- <u>lag (int \| list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>smooth_widow (int \| None, optional):</u> Deprecated misspelling of `smooth_window`,
accepted so that existing callers keep working. Passing it emits a
DeprecationWarning and forwards the value to `smooth_window`. Defaults to None.

**Returns:**

pd.Series or pd.DataFrame: Stochastic Oscillator (%K and %D) values.

**Raises:**

ValueError: If the specified `period` is not one of the valid options, or if both
`smooth_window` and the deprecated `smooth_widow` are given conflicting values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the Stochastic Oscillator values for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the %K and %D values
using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_stochastic_oscillator().xs("AAPL", level=1, axis="columns")
```

Which returns:

| Date       |   Stochastic %D |   Stochastic %K |
|:-----------|----------------:|----------------:|
| 2026-06-18 |         34.4881 |         35.4097 |
| 2026-06-22 |         32.012  |         32.0786 |
| 2026-06-23 |         30.1799 |         23.0513 |
| 2026-06-24 |         24.7058 |         18.9873 |
| 2026-06-25 |         15.082  |          3.2073 |
| 2026-06-26 |         15.0576 |         22.9782 |
| 2026-06-29 |         18.0181 |         27.8689 |
| 2026-06-30 |         35.0981 |         54.4472 |
| 2026-07-01 |         51.4243 |         71.9567 |
| 2026-07-02 |         74.7297 |         97.7853 |

---

## get_moving_average_convergence_divergence
Calculate the Moving Average Convergence Divergence (MACD) indicator for a given price series.

The Moving Average Convergence Divergence (MACD) is a trend-following momentum indicator that shows the relationship between two moving averages of a security's price. It consists of the MACD line, signal line, and MACD histogram.

The formula is as follows:

$$
\text{MACD Line} = \text{Short-term EMA} - \text{Long-term EMA}
$$

$$
\text{Signal Line} = \operatorname{SMA}(\text{MACD Line})
$$

**Also known as:** MACD, momentum indicator.

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
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to.
Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the MACD and signal values.
Defaults to False.
- <u>lag (int \| list[int], optional):</u> The lag to use for the growth calculation.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
Defaults to 1.

**Returns:**

pd.Series or pd.DataFrame:
MACD line and signal line values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the MACD and signal line values for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the MACD and signal values
using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_moving_average_convergence_divergence().xs("AAPL", level=1, axis="columns")
```

Which returns:

| Date       |   MACD Line |   Signal Line |
|:-----------|------------:|--------------:|
| 2026-06-18 |      1.1803 |        3.2153 |
| 2026-06-22 |      0.9697 |        2.7662 |
| 2026-06-23 |      0.5776 |        2.3285 |
| 2026-06-24 |      0.1664 |        1.8961 |
| 2026-06-25 |     -1.588  |        1.1993 |
| 2026-06-26 |     -2.2559 |        0.5082 |
| 2026-06-29 |     -2.9163 |       -0.1767 |
| 2026-06-30 |     -2.7926 |       -0.6999 |
| 2026-07-01 |     -2.2633 |       -1.0125 |
| 2026-07-02 |     -0.6862 |       -0.9473 |

---

## get_relative_strength_index
Calculate the Relative Strength Index (RSI) indicator for a given price series.

The Relative Strength Index (RSI) is a momentum oscillator that measures the speed and change of price movements. It ranges from 0 to 100 and is used to identify overbought or oversold conditions in an asset's price.

The formula is as follows:

$$
\text{RSI} = 100 - (100 / (1 + \text{RS}))
$$

**Also known as:** RSI, momentum oscillator, overbought, oversold.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int, optional):</u> The number of periods for RSI calculation. Defaults to 14.
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to.
Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the RSI.
Defaults to False.
- <u>lag (int \| list[int], optional):</u> The lag to use for the growth calculation.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
Defaults to 1.

**Returns:**

pd.DataFrame or pd.Series:
Relative Strength Index (RSI) values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates the
RSI for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the RSI
using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_relative_strength_index()
```

Which returns:

| Date       |    AAPL |    MSFT |   Benchmark |
|:-----------|--------:|--------:|------------:|
| 2026-06-18 | 39.0696 | 18.5547 |     44.8909 |
| 2026-06-22 | 42.1875 |  9.2816 |     42.6001 |
| 2026-06-23 | 30.4087 | 16.9139 |     37.6696 |
| 2026-06-24 | 32.6884 | 17.8779 |     39.5418 |
| 2026-06-25 | 22.9048 | 15.2531 |     38.4444 |
| 2026-06-26 | 33.4829 | 31.3248 |     44.9277 |
| 2026-06-29 | 35.3464 | 31.4673 |     50.9396 |
| 2026-06-30 | 49.0731 | 36.5041 |     54.943  |
| 2026-07-01 | 52.0534 | 44.4482 |     61.5893 |
| 2026-07-02 | 58.2929 | 50.0641 |     54.5966 |

---

## get_balance_of_power
Calculate the Balance of Power (BOP) indicator for a given price series.

The Balance of Power (BOP) indicator measures the strength of buyers versus sellers in the market. It relates the price change to the change in the asset's trading range.

The formula is as follows:

$$
\text{BOP} = (\text{Close} - \text{Open}) / (\text{High} - \text{Low})
$$

**Also known as:** BOP, bull bear power.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to.
Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the BOP.
Defaults to False.
- <u>lag (int \| list[int], optional):</u> The lag to use for the growth calculation.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
Defaults to 1.

**Returns:**

pd.DataFrame or pd.Series:
Balance of Power (BOP) values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates the
BOP for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the BOP
using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_balance_of_power()
```

Which returns:

| Date       |    AAPL |    MSFT |   Benchmark |
|:-----------|--------:|--------:|------------:|
| 2026-06-18 | -0.0202 |  0.1953 |     -0.2334 |
| 2026-06-22 | -0.053  | -0.5769 |     -0.4695 |
| 2026-06-23 | -0.4343 |  0.2382 |     -0.0314 |
| 2026-06-24 | -0.3373 | -0.4333 |     -0.2119 |
| 2026-06-25 | -0.814  | -0.6613 |     -0.4719 |
| 2026-06-26 |  0.7479 |  0.7469 |      0.002  |
| 2026-06-29 | -0.5857 | -0.4335 |      0.472  |
| 2026-06-30 |  0.8864 |  0.297  |      0.7686 |
| 2026-07-01 |  0.1272 |  0.2475 |      0.1076 |
| 2026-07-02 |  0.9219 |  0.7071 |     -0.2323 |

---

## get_awesome_oscillator
Calculate the Awesome Oscillator (AO) for a given price series.

The Awesome Oscillator measures market momentum by comparing a short-term and a long-term Simple Moving Average of the median price (the midpoint of each period's high and low, rather than the closing price). It was developed by Bill Williams as part of his broader "Trading Chaos" collection of momentum indicators.

The formula is as follows:

$$
\text{Median Price} = (\text{High} + \text{Low}) / 2
$$

$$
\text{AO} = \operatorname{SMA}(\text{Median Price},\; \text{short\_window}) - \operatorname{SMA}(\text{Median Price},\; \text{long\_window})
$$

**Also known as:** AO, Bill Williams Awesome Oscillator.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>short_window (int, optional):</u> The number of periods for the short-term SMA of the
median price. Defaults to 5.
- <u>long_window (int, optional):</u> The number of periods for the long-term SMA of the
median price. Defaults to 34.
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to.
Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the AO.
Defaults to False.
- <u>lag (int \| list[int], optional):</u> The lag to use for the growth calculation.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
Defaults to 1.

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
- If `growth` is set to True, the method calculates the growth of the AO
using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_awesome_oscillator()
```

Which returns:

| Date       |     AAPL |    MSFT |   Benchmark |
|:-----------|---------:|--------:|------------:|
| 2022-12-16 |  -3.5418 | 11.2131 |      2.3418 |
| 2022-12-19 |  -4.8628 |  9.3716 |     -0.5142 |
| 2022-12-20 |  -7.3604 |  5.5371 |     -5.2622 |
| 2022-12-21 |  -8.7804 |  1.9144 |     -8.5319 |
| 2022-12-22 |  -9.8319 | -1.2635 |    -11.0124 |
| 2022-12-23 | -10.5435 | -3.8732 |    -11.8451 |
| 2022-12-27 | -10.9665 | -5.1579 |    -11.8737 |
| 2022-12-28 | -11.2666 | -6.1431 |    -11.8561 |
| 2022-12-29 | -12.1821 | -7.321  |    -12.6508 |
| 2022-12-30 | -12.5038 | -7.2199 |    -12.3585 |

---

## get_vortex_indicator
Calculate the Vortex Indicator for a given price series.

The Vortex Indicator quantifies the presence and strength of a directional trend by comparing each period's price movement away from the prior period's range to the period's overall volatility (True Range). It consists of two lines, VI+ and VI-, whose crossovers signal potential trend changes: VI+ above VI- suggests an uptrend is in control, VI- above VI+ suggests a downtrend is in control.

The formula is as follows:

$$
\text{VM} + = | \operatorname{High}(t) - \operatorname{Low}(t-1) |
$$

$$
\text{VM} - = | \operatorname{Low}(t) - \operatorname{High}(t-1) |
$$

$$
\text{VI} + = \operatorname{Sum}(\text{VM} +,\; \text{window}) / \operatorname{Sum}(\text{True Range},\; \text{window})
$$

$$
\text{VI} - = \operatorname{Sum}(\text{VM} -,\; \text{window}) / \operatorname{Sum}(\text{True Range},\; \text{window})
$$

**Also known as:** VI, Vortex Indicator +/-, trend direction indicator.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int, optional):</u> The number of periods to sum the directional movement and
true range over. Defaults to 14.
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to.
Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the VI+ and VI- values.
Defaults to False.
- <u>lag (int \| list[int], optional):</u> The lag to use for the growth calculation.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
Defaults to 1.

**Returns:**

pd.Series or pd.DataFrame:
VI+ and VI- values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the Vortex Indicator values for each asset in the Toolkit instance.
- Reference: Botes, E., & Siepman, D. (2010). "The Vortex Indicator." Technical Analysis
of Stocks & Commodities, 28(1), 20-25.
- If `growth` is set to True, the method calculates the growth of the VI+ and VI-
using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_vortex_indicator().xs("AAPL", level=1, axis="columns")
```

Which returns:

| Date       |    VI+ |    VI- |
|:-----------|-------:|-------:|
| 2022-12-16 | 0.7841 | 1.0588 |
| 2022-12-19 | 0.7914 | 1.0685 |
| 2022-12-20 | 0.7615 | 1.1866 |
| 2022-12-21 | 0.6978 | 1.1025 |
| 2022-12-22 | 0.6841 | 1.1164 |
| 2022-12-23 | 0.6603 | 1.1994 |
| 2022-12-27 | 0.693  | 1.1657 |
| 2022-12-28 | 0.687  | 1.105  |
| 2022-12-29 | 0.6859 | 1.0921 |
| 2022-12-30 | 0.6736 | 1.1363 |

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
Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int, optional):</u> The number of periods for the EMA used as the trend baseline.
Defaults to 13, as originally proposed by Elder.
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to.
Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Bull and Bear Power.
Defaults to False.
- <u>lag (int \| list[int], optional):</u> The lag to use for the growth calculation.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
Defaults to 1.

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
- If `growth` is set to True, the method calculates the growth of the Bull and Bear Power
using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_elder_ray_index().xs("AAPL", level=1, axis="columns")
```

Which returns:

| Date       |   Bear Power |   Bull Power |
|:-----------|-------------:|-------------:|
| 2022-12-16 |      -6.837  |      -2.917  |
| 2022-12-19 |      -7.8589 |      -3.9789 |
| 2022-12-20 |      -8.089  |      -4.729  |
| 2022-12-21 |      -4.6449 |      -0.5849 |
| 2022-12-22 |      -6.1399 |      -1.8799 |
| 2022-12-23 |      -5.9285 |      -3.1485 |
| 2022-12-27 |      -5.8444 |      -3.1544 |
| 2022-12-28 |      -7.2695 |      -2.1095 |
| 2022-12-29 |      -4.6924 |      -1.9424 |
| 2022-12-30 |      -4.4235 |      -1.9035 |

---

## get_rate_of_change
Calculate the Rate of Change (ROC) for a given price series.

The Rate of Change is a pure momentum oscillator that measures the percentage change in price between the current period and the price a fixed number of periods ago. It oscillates around zero: positive values indicate price is higher than `window` periods ago (upward momentum), while negative values indicate price is lower (downward momentum).

The formula is as follows:

$$
\text{ROC} = (\operatorname{Close}(t) / \operatorname{Close}(t - \text{window}) - 1) \cdot 100
$$

**Also known as:** ROC, Price Rate of Change, momentum.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int, optional):</u> Number of periods to look back for the rate of change
calculation. Defaults to 12.
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to.
Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Rate of Change.
Defaults to False.
- <u>lag (int \| list[int], optional):</u> The lag to use for the growth calculation.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
Defaults to 1.

**Returns:**

pd.Series or pd.DataFrame: Rate of Change values, expressed as a percentage.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the Rate of Change for each asset in the Toolkit instance.
- Reference: Murphy, J.J. (1999). "Technical Analysis of the Financial Markets." New
York Institute of Finance.
- If `growth` is set to True, the method calculates the growth of the Rate of Change
using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_rate_of_change()
```

---

## get_choppiness_index
Calculate the Choppiness Index (CHOP) for a given price series.

The Choppiness Index quantifies whether the market is trending or moving sideways ("choppy") by comparing the sum of True Range over the window (a measure of the total price path travelled) to the net range the price actually covered over that same window (the distance between the highest high and the lowest low). When price travels a long, winding path but ends up covering little net ground, the index is high (near 100), signalling a choppy, range-bound market. When price travels efficiently in one direction, the index is low (near 0), signalling a trending market.

The formula is as follows:

$$
\text{CHOP} = 100 \cdot \log_{10}(\operatorname{Sum}(\text{True Range},\; \text{window}) / (\max(\text{High},\; \text{window}) - \min(\text{Low},\; \text{window}))) / \log_{10}(\text{window})
$$

**Also known as:** CHOP, Choppiness Index.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int, optional):</u> Number of periods to consider for the Choppiness Index
calculation. Defaults to 14.
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to.
Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Choppiness Index.
Defaults to False.
- <u>lag (int \| list[int], optional):</u> The lag to use for the growth calculation.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
Defaults to 1.

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
- If `growth` is set to True, the method calculates the growth of the Choppiness
Index using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_choppiness_index()
```

---

## get_know_sure_thing
Calculate the Know Sure Thing (KST) for a given price series.

The Know Sure Thing is a momentum oscillator developed by Martin Pring that combines four smoothed Rate of Change series, each calculated over a progressively longer lookback period, into a single weighted sum. Smoothing each Rate of Change with a Simple Moving Average before combining them reduces noise, while the increasing weights on the longer lookback periods give more influence to the more significant, longer-term price cycles. A signal line (a Simple Moving Average of the KST itself) is used to spot crossovers, in the same way the MACD line is compared to its signal line.

The formula is as follows:

$$
\operatorname{RCMA}(i) = \operatorname{SMA}(\operatorname{ROC}(\text{Close},\; \text{roc\_windows} \left[i\right]),\; \text{sma\_windows} \left[i\right])
$$

$$
\text{KST} = \operatorname{Sum}(\operatorname{RCMA}(i) \cdot \text{weights} \left[i\right]) \text{for} i = 1..4
$$

$$
\text{Signal Line} = \operatorname{SMA}(\text{KST},\; \text{signal\_window})
$$

**Also known as:** KST, Pring's Know Sure Thing, Summed Rate of Change.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>roc_windows (list[int] \| None, optional):</u> The four lookback periods used for the
underlying Rate of Change calculations. Defaults to the standard
[10, 15, 20, 30].
- <u>sma_windows (list[int] \| None, optional):</u> The four Simple Moving Average
smoothing periods applied to each Rate of Change series. Defaults to the
standard [10, 10, 10, 15].
- <u>weights (list[int] \| None, optional):</u> The four weights applied to each smoothed
Rate of Change series before summing. Defaults to the standard [1, 2, 3, 4].
- <u>signal_window (int, optional):</u> Number of periods for the Simple Moving Average of
the KST used as the signal line. Defaults to 9.
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to.
Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the KST and Signal Line.
Defaults to False.
- <u>lag (int \| list[int], optional):</u> The lag to use for the growth calculation.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
Defaults to 1.

**Returns:**

pd.Series or pd.DataFrame:
KST and Signal Line values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the Know Sure Thing values for each asset in the Toolkit instance.
- Reference: Pring, M.J. (1992). "The Know Sure Thing (KST)." Technical Analysis of
Stocks & Commodities, 10(6).
- If `growth` is set to True, the method calculates the growth of the KST and Signal
Line using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_know_sure_thing().xs("AAPL", level=1, axis="columns")
```

---

## collect_overlap_indicators
Calculates and collects various overlap-based indicators based on the provided data.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
- <u>window (int, optional):</u> The window size for calculating indicators.
Defaults to 14.
- <u>close_column (str, optional):</u> The name of the column containing the close prices.
Defaults to "Adj Close".
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to.
Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int \| list[int], optional):</u> The lag to use for the growth calculation.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
Defaults to 1.

**Returns:**

pd.Series or pd.DataFrame: Overlap-based indicators calculated based on the specified parameters.

**Notes:**

- The method calculates several overlap-based indicators for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the indicator values
using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.collect_overlap_indicators().xs("AAPL", level=1, axis="columns")
```

Which returns:

| Date       |   Simple Moving Average (SMA) |   Exponential Moving Average (EMA) |
|:-----------|------------------------------:|-----------------------------------:|
| 2026-06-18 |                       300.742 |                            298.807 |
| 2026-06-22 |                       300.078 |                            298.567 |
| 2026-06-23 |                       298.585 |                            297.998 |
| 2026-06-24 |                       297.358 |                            297.342 |
| 2026-06-25 |                       294.781 |                            294.383 |
| 2026-06-26 |                       293.098 |                            292.969 |
| 2026-06-29 |                       291.684 |                            291.472 |
| 2026-06-30 |                       291.599 |                            291.191 |
| 2026-07-01 |                       291.799 |                            291.616 |
| 2026-07-02 |                       292.727 |                            293.884 |

---

## get_moving_average
Calculate the Moving Average (MA) for a given price series.

The Moving Average (MA) is a commonly used technical indicator that smooths out price data by calculating the average price over a specified number of periods.

The formula is as follows:

$$
\text{MA} = (\text{Sum of Prices}) / (\text{Number of Prices})
$$

**Also known as:** SMA, simple moving average, MA.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int, optional):</u> Number of periods to consider for the moving average.
The number of periods (time intervals) over which to calculate the MA.
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to.
Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the MA.
Defaults to False.
- <u>lag (int \| list[int], optional):</u> The lag to use for the growth calculation.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
Defaults to 1.

**Returns:**

pd.DataFrame or pd.Series:
Moving Average (MA) values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates the
MA for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the MA
using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_moving_average()
```

Which returns:

| Date       |    AAPL |    MSFT |   Benchmark |
|:-----------|--------:|--------:|------------:|
| 2026-06-18 | 300.742 | 408.527 |     745.79  |
| 2026-06-22 | 300.078 | 401.871 |     744.779 |
| 2026-06-23 | 298.585 | 397.059 |     742.923 |
| 2026-06-24 | 297.358 | 392.639 |     741.423 |
| 2026-06-25 | 294.781 | 387.266 |     739.795 |
| 2026-06-26 | 293.098 | 384.145 |     739.184 |
| 2026-06-29 | 291.684 | 381.061 |     739.311 |
| 2026-06-30 | 291.599 | 378.891 |     740.005 |
| 2026-07-01 | 291.799 | 377.956 |     741.457 |
| 2026-07-02 | 292.727 | 377.967 |     741.959 |

---

## get_exponential_moving_average
Calculate the Exponential Moving Average (EMA) for a given price series.

EMA is a technical indicator that gives more weight to recent price data, providing a smoothed moving average that reacts faster to price changes.

The formula is as follows:

$$
\text{EMA} = (\text{Close} - \text{Previous EMA}) \cdot (2 / (1 + \text{Window})) + \text{Previous EMA}
$$

**Also known as:** EMA.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int, optional):</u> Number of periods for EMA calculation.
The number of periods (time intervals) over which to calculate the EMA.
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to.
Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the EMA.
Defaults to False.
- <u>lag (int \| list[int], optional):</u> The lag to use for the growth calculation.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
Defaults to 1.

**Returns:**

pd.DataFrame or pd.Series:
Exponential Moving Average (EMA) values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates the
EMA for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the EMA
using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_exponential_moving_average()
```

Which returns:

| Date       |    AAPL |    MSFT |   Benchmark |
|:-----------|--------:|--------:|------------:|
| 2026-06-18 | 298.807 | 400.817 |     744.491 |
| 2026-06-22 | 298.567 | 396.353 |     744.477 |
| 2026-06-23 | 297.998 | 393.365 |     743.024 |
| 2026-06-24 | 297.342 | 389.644 |     741.72  |
| 2026-06-25 | 294.383 | 384.736 |     740.73  |
| 2026-06-26 | 292.969 | 383.167 |     739.165 |
| 2026-06-29 | 291.472 | 381.221 |     739.41  |
| 2026-06-30 | 291.191 | 380.127 |     740.391 |
| 2026-07-01 | 291.616 | 380.681 |     741.107 |
| 2026-07-02 | 293.884 | 381.989 |     741.597 |

---

## get_double_exponential_moving_average
Calculate the Double Exponential Moving Average (DEMA) for a given price series.

DEMA is a technical indicator that attempts to reduce the lag from traditional moving averages by using a combination of two exponential moving averages.

The formula is as follows:

$$
\text{EMA} = (\text{Close} - \text{Previous EMA}) \cdot (2 / (1 + \text{Window})) + \text{Previous EMA}
$$

**Also known as:** DEMA, double EMA.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int, optional):</u> Number of periods for moving average calculation.
The number of periods (time intervals) over which to calculate the moving average.
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to.
Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the DEMA.
Defaults to False.
- <u>lag (int \| list[int], optional):</u> The lag to use for the growth calculation.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
Defaults to 1.

**Returns:**

pd.DataFrame or pd.Series:
Double Exponential Moving Average (DEMA) values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates the
DEMA for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the DEMA
using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_double_exponential_moving_average()
```

Which returns:

| Date       |    AAPL |    MSFT |   Benchmark |
|:-----------|--------:|--------:|------------:|
| 2026-06-18 | 297.732 | 388.259 |     746.117 |
| 2026-06-22 | 297.428 | 381.601 |     745.875 |
| 2026-06-23 | 296.518 | 377.99  |     742.977 |
| 2026-06-24 | 295.491 | 373.095 |     740.548 |
| 2026-06-25 | 290.215 | 366.139 |     738.857 |
| 2026-06-26 | 288.132 | 365.69  |     736.185 |
| 2026-06-29 | 285.982 | 364.387 |     737.039 |
| 2026-06-30 | 286.188 | 364.591 |     739.187 |
| 2026-07-01 | 287.649 | 367.696 |     740.684 |
| 2026-07-02 | 292.412 | 371.868 |     741.654 |

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
\text{TRIX} = 100 \cdot ((\text{EMA3} - \text{EMA3} \left[- 1\right]) / \text{EMA3} \left[- 1\right])
$$

**Also known as:** triple smoothed EMA, rate of change oscillator.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int, optional):</u> Number of periods for moving average calculation.
The number of periods (time intervals) over which to calculate the moving average.
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to.
Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Trix.
Defaults to False.
- <u>lag (int \| list[int], optional):</u> The lag to use for the growth calculation.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
Defaults to 1.

**Returns:**

pd.DataFrame or pd.Series:
Trix values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates the
Trix for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the Trix
using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_trix()
```

Which returns:

| Date       |    AAPL |    MSFT |   Benchmark |
|:-----------|--------:|--------:|------------:|
| 2026-06-18 |  0.1364 | -0.1466 |      0.0936 |
| 2026-06-22 |  0.1102 | -0.1998 |      0.0849 |
| 2026-06-23 |  0.0852 | -0.2492 |      0.0734 |
| 2026-06-24 |  0.061  | -0.2982 |      0.0603 |
| 2026-06-25 |  0.0242 | -0.3513 |      0.0471 |
| 2026-06-26 | -0.0123 | -0.3924 |      0.0325 |
| 2026-06-29 | -0.0485 | -0.4254 |      0.0216 |
| 2026-06-30 | -0.0765 | -0.4481 |      0.0154 |
| 2026-07-01 | -0.0937 | -0.4554 |      0.0122 |
| 2026-07-02 | -0.0914 | -0.4477 |      0.0107 |

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

**Also known as:** Bollinger Bands, BB, volatility bands, price channels.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int, optional):</u> Number of periods for moving average calculation.
The number of periods (time intervals) over which to calculate the moving average.
- <u>num_std_dev (int, optional):</u> Number of standard deviations for the bands.
Defaults to 2.
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to.
Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the bands.
Defaults to False.
- <u>lag (int \| list[int], optional):</u> The lag to use for the growth calculation.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
Defaults to 1.

**Returns:**

pd.Series or pd.DataFrame:
Bollinger Bands (upper, middle, lower).

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates the
Bollinger Bands for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the Bollinger Bands
using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_bollinger_bands().xs("AAPL", level=1, axis="columns")
```

Which returns:

| Date       |   Close |   Lower Band |   Middle Band |   Upper Band |
|:-----------|--------:|-------------:|--------------:|-------------:|
| 2026-06-18 |  298.01 |      284.642 |       300.742 |      316.843 |
| 2026-06-22 |  297.01 |      284.201 |       300.078 |      315.955 |
| 2026-06-23 |  294.3  |      285.08  |       298.585 |      312.09  |
| 2026-06-24 |  293.08 |      285.388 |       297.358 |      309.328 |
| 2026-06-25 |  275.15 |      280.386 |       294.781 |      309.176 |
| 2026-06-26 |  283.78 |      279.544 |       293.098 |      306.652 |
| 2026-06-29 |  281.74 |      277.796 |       291.684 |      305.571 |
| 2026-06-30 |  289.36 |      277.667 |       291.599 |      305.53  |
| 2026-07-01 |  294.38 |      277.788 |       291.799 |      305.81  |
| 2026-07-02 |  308.63 |      276.137 |       292.727 |      309.318 |

---

## get_triangular_moving_average
Calculate the Triangular Moving Average (TMA) for a given price series.

The Triangular Moving Average (TMA) is a smoothed version of the Simple Moving Average (SMA) that uses multiple SMAs to reduce noise and provide a smoother trendline.

The formula is as follows:

$$
\text{For an odd window:}\;\; \text{Sub-window Length} = (\text{Window} + 1) / 2,\;\; \text{applied for both passes}
$$

$$
\text{For an even window:}\;\; \text{the two passes use different sub-window lengths},\;\; \text{Window} / 2 \text{and Window} / 2 + 1 (\text{matching TA-Lib's TRIMA convention})
$$

$$
\text{TMA} = \operatorname{SMA}(\operatorname{SMA}(\text{Close},\; \text{Sub-window Length} 1),\; \text{Sub-window Length} 2)
$$

**Also known as:** TMA, triangular MA.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int, optional):</u> Number of periods for TMA calculation.
The number of periods (time intervals) over which to calculate the TMA.
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to.
Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the TMA.
Defaults to False.
- <u>lag (int \| list[int], optional):</u> The lag to use for the growth calculation.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
Defaults to 1.

**Returns:**

pd.Series or pd.DataFrame: Triangular Moving Average values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates the
Triangular Moving Average for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the Triangular Moving Average
using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_triangular_moving_average()
```

Which returns:

| Date       |    AAPL |    MSFT |   Benchmark |
|:-----------|--------:|--------:|------------:|
| 2026-06-18 | 561.385 | 762.584 |     1392.14 |
| 2026-06-22 | 560.145 | 750.16  |     1390.25 |
| 2026-06-23 | 557.359 | 741.177 |     1386.79 |
| 2026-06-24 | 555.068 | 732.927 |     1383.99 |
| 2026-06-25 | 550.257 | 722.897 |     1380.95 |
| 2026-06-26 | 547.116 | 717.071 |     1379.81 |
| 2026-06-29 | 544.476 | 711.315 |     1380.05 |
| 2026-06-30 | 544.317 | 707.263 |     1381.34 |
| 2026-07-01 | 544.691 | 705.519 |     1384.05 |
| 2026-07-02 | 546.424 | 705.539 |     1384.99 |

---

## get_weighted_moving_average
Calculate the Weighted Moving Average (WMA) for a given price series.

The Weighted Moving Average (WMA) is a moving average that assigns a linearly increasing weight to more recent prices, making it more responsive to recent price changes than a Simple Moving Average.

The formula is as follows:

$$
\text{WMA} = (\text{Sum of} (\text{Price} \cdot \text{Weight})) / (\text{Sum of Weights})
$$

**Also known as:** WMA, linearly weighted moving average.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int, optional):</u> Number of periods to consider for the WMA.
The number of periods (time intervals) over which to calculate the WMA.
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to.
Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the WMA.
Defaults to False.
- <u>lag (int \| list[int], optional):</u> The lag to use for the growth calculation.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
Defaults to 1.

**Returns:**

pd.DataFrame or pd.Series:
Weighted Moving Average (WMA) values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates the
WMA for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the WMA
using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_weighted_moving_average()
```

Which returns:

| Date       |    AAPL |    MSFT |   Benchmark |
|:-----------|--------:|--------:|------------:|
| 2026-06-18 | 300.742 | 408.527 |     745.79  |
| 2026-06-22 | 300.078 | 401.871 |     744.779 |
| 2026-06-23 | 298.585 | 397.059 |     742.923 |
| 2026-06-24 | 297.358 | 392.639 |     741.423 |
| 2026-06-25 | 294.781 | 387.266 |     739.795 |
| 2026-06-26 | 293.098 | 384.145 |     739.184 |
| 2026-06-29 | 291.684 | 381.061 |     739.311 |
| 2026-06-30 | 291.599 | 378.891 |     740.005 |
| 2026-07-01 | 291.799 | 377.956 |     741.457 |
| 2026-07-02 | 292.727 | 377.967 |     741.959 |

---

## get_hull_moving_average
Calculate the Hull Moving Average (HMA) for a given price series.

The Hull Moving Average (HMA) reduces the lag typically associated with moving averages while improving smoothing, by combining a Weighted Moving Average (WMA) of half the window length, a WMA of the full window length, and a further WMA over the square root of the window length.

The formula is as follows:

$$
\text{Raw HMA} = (2 \cdot \operatorname{WMA}(\text{Close},\; \text{Window} / 2)) - \operatorname{WMA}(\text{Close},\; \text{Window})
$$

$$
\text{HMA} = \operatorname{WMA}(\text{Raw HMA},\; \sqrt{\text{Window}})
$$

**Also known as:** HMA, Hull MA.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int, optional):</u> Number of periods to consider for the HMA.
The number of periods (time intervals) over which to calculate the HMA.
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to.
Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the HMA.
Defaults to False.
- <u>lag (int \| list[int], optional):</u> The lag to use for the growth calculation.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
Defaults to 1.

**Returns:**

pd.DataFrame or pd.Series:
Hull Moving Average (HMA) values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates the
HMA for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the HMA
using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_hull_moving_average()
```

Which returns:

| Date       |    AAPL |    MSFT |   Benchmark |
|:-----------|--------:|--------:|------------:|
| 2026-06-18 | 300.742 | 408.527 |     745.79  |
| 2026-06-22 | 300.078 | 401.871 |     744.779 |
| 2026-06-23 | 298.585 | 397.059 |     742.923 |
| 2026-06-24 | 297.358 | 392.639 |     741.423 |
| 2026-06-25 | 294.781 | 387.266 |     739.795 |
| 2026-06-26 | 293.098 | 384.145 |     739.184 |
| 2026-06-29 | 291.684 | 381.061 |     739.311 |
| 2026-06-30 | 291.599 | 378.891 |     740.005 |
| 2026-07-01 | 291.799 | 377.956 |     741.457 |
| 2026-07-02 | 292.727 | 377.967 |     741.959 |

---

## get_kaufman_adaptive_moving_average
Calculate the Kaufman Adaptive Moving Average (KAMA) for a given price series.

The Kaufman Adaptive Moving Average adjusts its own responsiveness to price changes based on how "efficiently" price is moving. It compares the net directional move over the window to the total (sum of absolute) movement over that same window - the Efficiency Ratio. When price trends strongly in one direction (an efficient move), the Efficiency Ratio is close to 1 and KAMA tracks price closely, behaving like a fast EMA. When price whipsaws sideways (an inefficient move), the Efficiency Ratio is close to 0 and KAMA flattens out, behaving like a slow EMA - reducing whipsaw signals in choppy markets while still reacting quickly during strong trends.

The formula is as follows:

$$
\text{Change} = | \operatorname{Close}(t) - \operatorname{Close}(t - \text{window}) |
$$

$$
\text{Volatility} = \operatorname{Sum}(| \operatorname{Close}(i) - \operatorname{Close}(i - 1) |,\; \text{window})
$$

$$
\text{Efficiency Ratio} (\text{ER}) = \text{Change} / \text{Volatility}
$$

$$
\text{Fastest SC} = 2 / (\text{fast\_window} + 1),\;\; \text{Slowest SC} = 2 / (\text{slow\_window} + 1)
$$

$$
\text{Smoothing Constant} (\text{SC}) = \left[\text{ER} \cdot (\text{Fastest SC} - \text{Slowest SC}) + \text{Slowest SC}\right] ^{2}
$$

$$
\operatorname{KAMA}(t) = \operatorname{KAMA}(t-1) + \text{SC} \cdot (\operatorname{Close}(t) - \operatorname{KAMA}(t-1))
$$

**Also known as:** KAMA, Kaufman's Adaptive Moving Average.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
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
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to.
Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the KAMA.
Defaults to False.
- <u>lag (int \| list[int], optional):</u> The lag to use for the growth calculation.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
Defaults to 1.

**Returns:**

pd.Series or pd.DataFrame: KAMA values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the KAMA for each asset in the Toolkit instance.
- Reference: Kaufman, P.J. (1998). "Trading Systems and Methods." 3rd ed. Wiley.
- If `growth` is set to True, the method calculates the growth of the KAMA using the
specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_kaufman_adaptive_moving_average()
```

---

## get_volume_weighted_average_price
Calculate the Volume Weighted Average Price (VWAP) for a given price series.

The Volume Weighted Average Price (VWAP) weighs the typical price of each period by its traded volume over a rolling window, giving a more volume-informed view of the average price than a plain moving average.

The formula is as follows:

$$
\text{Typical Price} = (\text{High} + \text{Low} + \text{Close}) / 3
$$

$$
\text{VWAP} = \operatorname{Sum}(\text{Typical Price} \cdot \text{Volume},\; \text{Window}) / \operatorname{Sum}(\text{Volume},\; \text{Window})
$$

**Also known as:** VWAP.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int, optional):</u> Number of periods to consider for the VWAP.
The number of periods (time intervals) over which to calculate the VWAP.
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to.
Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the VWAP.
Defaults to False.
- <u>lag (int \| list[int], optional):</u> The lag to use for the growth calculation.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
Defaults to 1.

**Returns:**

pd.DataFrame or pd.Series:
Volume Weighted Average Price (VWAP) values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates the
VWAP for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the VWAP
using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_volume_weighted_average_price()
```

Which returns:

| Date       |    AAPL |    MSFT |   Benchmark |
|:-----------|--------:|--------:|------------:|
| 2026-06-18 | 300.742 | 408.527 |     745.79  |
| 2026-06-22 | 300.078 | 401.871 |     744.779 |
| 2026-06-23 | 298.585 | 397.059 |     742.923 |
| 2026-06-24 | 297.358 | 392.639 |     741.423 |
| 2026-06-25 | 294.781 | 387.266 |     739.795 |
| 2026-06-26 | 293.098 | 384.145 |     739.184 |
| 2026-06-29 | 291.684 | 381.061 |     739.311 |
| 2026-06-30 | 291.599 | 378.891 |     740.005 |
| 2026-07-01 | 291.799 | 377.956 |     741.457 |
| 2026-07-02 | 292.727 | 377.967 |     741.959 |

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

**Also known as:** Parabolic SAR, stop and reverse, PSAR.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>af_start (float, optional):</u> Initial acceleration factor. Defaults to 0.02.
- <u>af_increment (float, optional):</u> Amount by which the acceleration factor
increases every time a new extreme point is reached. Defaults to 0.02.
- <u>af_max (float, optional):</u> Maximum value the acceleration factor can reach.
Defaults to 0.2.
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to.
Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Parabolic SAR.
Defaults to False.
- <u>lag (int \| list[int], optional):</u> The lag to use for the growth calculation.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
Defaults to 1.

**Returns:**

pd.DataFrame or pd.Series:
Parabolic SAR values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates the
Parabolic SAR for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the Parabolic SAR
using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_parabolic_sar()
```

Which returns:

| Date       |    AAPL |    MSFT |   Benchmark |
|:-----------|--------:|--------:|------------:|
| 2026-06-18 | 300.742 | 408.527 |     745.79  |
| 2026-06-22 | 300.078 | 401.871 |     744.779 |
| 2026-06-23 | 298.585 | 397.059 |     742.923 |
| 2026-06-24 | 297.358 | 392.639 |     741.423 |
| 2026-06-25 | 294.781 | 387.266 |     739.795 |
| 2026-06-26 | 293.098 | 384.145 |     739.184 |
| 2026-06-29 | 291.684 | 381.061 |     739.311 |
| 2026-06-30 | 291.599 | 378.891 |     740.005 |
| 2026-07-01 | 291.799 | 377.956 |     741.457 |
| 2026-07-02 | 292.727 | 377.967 |     741.959 |

---

## get_pivot_points
Calculate the Pivot Points for a given price series.

Pivot Points are calculated from the previous period's high, low and close prices and are used to identify potential support and resistance levels for the current period.

The formula is as follows:

$$
\text{Pivot Point} = (\text{Previous High} + \text{Previous Low} + \text{Previous Close}) / 3
$$

$$
\text{Resistance} 1 = (2 \cdot \text{Pivot Point}) - \text{Previous Low}
$$

$$
\text{Support} 1 = (2 \cdot \text{Pivot Point}) - \text{Previous High}
$$

$$
\text{Resistance} 2 = \text{Pivot Point} + (\text{Previous High} - \text{Previous Low})
$$

$$
\text{Support} 2 = \text{Pivot Point} - (\text{Previous High} - \text{Previous Low})
$$

$$
\text{Resistance} 3 = \text{Previous High} + 2 \cdot (\text{Pivot Point} - \text{Previous Low})
$$

$$
\text{Support} 3 = \text{Previous Low} - 2 \cdot (\text{Previous High} - \text{Pivot Point})
$$

**Also known as:** pivot points, floor trader pivots.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to.
Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Pivot Points.
Defaults to False.
- <u>lag (int \| list[int], optional):</u> The lag to use for the growth calculation.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
Defaults to 1.

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

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_pivot_points().xs("AAPL", level=1, axis="columns")
```

Which returns:

| Date       |   Pivot Point |   Resistance 1 |   Support 1 |
|:-----------|--------------:|----------------:|-------------:|
| 2026-06-18 |       300.742 |          305.53  |      295.954 |
| 2026-06-22 |       300.078 |          304.201 |      295.955 |
| 2026-06-23 |       298.585 |          303.09  |      294.08  |
| 2026-06-24 |       297.358 |          301.328 |      293.388 |
| 2026-06-25 |       294.781 |          299.176 |      290.386 |
| 2026-06-26 |       293.098 |          296.652 |      289.544 |
| 2026-06-29 |       291.684 |          295.571 |      287.796 |
| 2026-06-30 |       291.599 |          295.53  |      287.667 |
| 2026-07-01 |       291.799 |          295.81  |      287.788 |
| 2026-07-02 |       292.727 |          299.318 |      286.137 |

---

## get_support_resistance_levels
Retrieves the support and resistance levels for the specified period and assets.

The Support and Resistance Levels are price levels where the price tends to stop and reverse.

- Support Levels: These are the valleys where the price tends to stop going down and may start to go up. Think of support levels as "floors" that the price has trouble falling below.
- Resistance Levels: These are the peaks where the price tends to stop going up and may start to go down. Think of resistance levels as "ceilings" that the price has trouble breaking through.

It does so by:

- Looking for Peaks and Valleys: The function looks at the stock prices and finds the high points (peaks) and low points (valleys) over time.
- Grouping Similar Peaks and Valleys: Sometimes, prices will stop at similar points multiple times. The function groups these similar peaks and valleys together to identify key resistance and support levels.

**Also known as:** support levels, resistance levels, pivot points.

**Args:**

- <u>sensitivity (float, optional):</u> The sensitivity parameter to determine the significance of the peaks
and valleys. A higher sensitivity value will result in fewer support and resistance levels
being identified. Defaults to 0.05.
- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int, optional):</u> Number of periods for calculating support and resistance levels.
The number of periods (time intervals) over which to calculate the support and resistance levels.
Defaults to 14.
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to.
If None, the rounding value specified during the initialization of the Toolkit instance will be used.
Defaults to None.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the levels.
Defaults to False.
- <u>lag (int \| list[int], optional):</u> The lag to use for the growth calculation.
Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

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

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

support_resistance_levels = toolkit.technicals.get_support_resistance_levels()

support_resistance_levels.xs("AAPL", level=1, axis="columns")
```

Which returns:

| Date       |   Resistance |   Support |
|:-----------|-------------:|----------:|
| 2026-06-24 |      174.201 |   128.17  |
| 2026-06-25 |      174.201 |   128.17  |
| 2026-06-26 |      174.201 |   128.17  |
| 2026-06-29 |      174.201 |   128.17  |
| 2026-06-30 |      174.201 |   128.17  |
| 2026-07-01 |      174.201 |   128.17  |
| 2026-07-02 |      174.201 |   128.17  |

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
Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int, optional):</u> The number of periods over which the rolling swing high
(maximum) and swing low (minimum) are determined. Defaults to 14.
- <u>levels (list[float] \| None, optional):</u> The Fibonacci ratios to calculate levels for.
Defaults to the standard [0.0, 0.236, 0.382, 0.5, 0.618, 0.786, 1.0].
- <u>trend (str, optional):</u> Whether to compute retracement levels for an "uptrend"
(levels measured down from the high — the conventional direction, used when a
prior move was up and price is now pulling back) or a "downtrend" (levels
measured up from the low, used when a prior move was down and price is now
bouncing). Defaults to "uptrend".
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to.
Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the retracement levels.
Defaults to False.
- <u>lag (int \| list[int], optional):</u> The lag to use for the growth calculation.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
Defaults to 1.

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
- There is no single canonical academic paper behind Fibonacci Retracement Levels — the
indicator is a practitioner tool derived from the Fibonacci sequence's ratios rather
than a published financial model. The standard textbook treatment is Murphy, J.J.
(1999). "Technical Analysis of the Financial Markets." New York Institute of Finance.
- If `growth` is set to True, the method calculates the growth of the retracement levels
using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_fibonacci_retracement_levels().xs("AAPL", level=1, axis="columns")
```

Which returns:

Note that the columns sort lexicographically by their label (so "100.0%" sorts right
after "0.0%", ahead of "23.6%"), matching the sorting convention used by every other
multi-column indicator in this module (e.g. Pivot Points' Resistance/Support levels).

| Date       |   0.0% |   100.0% |   23.6% |   38.2% |   50.0% |   61.8% |   78.6% |
|:-----------|-------:|---------:|--------:|--------:|--------:|--------:|--------:|
| 2022-12-16 | 150.92 |   133.73 | 146.863 | 144.353 | 142.325 | 140.297 | 137.409 |
| 2022-12-19 | 150.92 |   131.32 | 146.294 | 143.433 | 141.12  | 138.807 | 135.514 |
| 2022-12-20 | 150.92 |   129.89 | 145.957 | 142.887 | 140.405 | 137.923 | 134.39  |
| 2022-12-21 | 150.92 |   129.89 | 145.957 | 142.887 | 140.405 | 137.923 | 134.39  |
| 2022-12-22 | 150.92 |   129.89 | 145.957 | 142.887 | 140.405 | 137.923 | 134.39  |
| 2022-12-23 | 149.97 |   129.64 | 145.172 | 142.204 | 139.805 | 137.406 | 133.991 |
| 2022-12-27 | 149.97 |   128.72 | 144.955 | 141.852 | 139.345 | 136.838 | 133.268 |
| 2022-12-28 | 149.97 |   125.87 | 144.282 | 140.764 | 137.92  | 135.076 | 131.027 |
| 2022-12-29 | 149.97 |   125.87 | 144.282 | 140.764 | 137.92  | 135.076 | 131.027 |
| 2022-12-30 | 149.97 |   125.87 | 144.282 | 140.764 | 137.92  | 135.076 | 131.027 |

---

## collect_volatility_indicators
Calculates and collects various volatility indicators based on the provided data.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
- <u>window (int, optional):</u> The window size for calculating indicators.
Defaults to 14.
- <u>close_column (str, optional):</u> The name of the column containing the close prices.
Defaults to "Adj Close".
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to.
Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int \| list[int], optional):</u> The lag to use for the growth calculation.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
Defaults to 1.

**Returns:**

pd.Series or pd.DataFrame: Volatility indicators calculated based on the specified parameters.

**Notes:**

- The method calculates several volatility-based indicators for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the indicator values
using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.collect_volatility_indicators().xs("AAPL", level=1, axis="columns")
```

Which returns:

| Date       |   Bollinger Band Upper |   Bollinger Band Middle |   Bollinger Band Lower |   True Range |
|:-----------|-----------------------:|------------------------:|-----------------------:|-------------:|
| 2026-06-18 |                316.843 |                 300.742 |                284.642 |         4.95 |
| 2026-06-22 |                315.955 |                 300.078 |                284.201 |         5.66 |
| 2026-06-23 |                312.09  |                 298.585 |                285.08  |         7.46 |
| 2026-06-24 |                309.328 |                 297.358 |                285.388 |         6.76 |
| 2026-06-25 |                309.176 |                 294.781 |                280.386 |        19.33 |
| 2026-06-26 |                306.652 |                 293.098 |                279.544 |        11.74 |
| 2026-06-29 |                305.571 |                 291.684 |                277.796 |         8.52 |
| 2026-06-30 |                305.53  |                 291.599 |                277.667 |         9.24 |
| 2026-07-01 |                305.81  |                 291.799 |                277.788 |         7.39 |
| 2026-07-02 |                309.318 |                 292.727 |                276.137 |        15.74 |

---

## get_true_range
Calculate the True Range (TR) for a given price series.

The True Range (TR) is a measure of market volatility that considers the differences between the high and low prices and the previous closing price. It provides insights into the price movement of an asset.

The formula is as follows:

$$
\text{TR} = \max(\text{high} - \text{low},\; \operatorname{abs}(\text{high} - \text{previous\_close}),\; \operatorname{abs}(\text{low} - \text{previous\_close}))
$$

**Also known as:** TR, true range.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to.
Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the True Range.
Defaults to False.
- <u>lag (int \| list[int], optional):</u> The lag to use for the growth calculation.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
Defaults to 1.

**Returns:**

pd.Series or pd.DataFrame: True Range values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates the
True Range for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the True Range
using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_true_range()
```

Which returns:

| Date       |   AAPL |   MSFT |   Benchmark |
|:-----------|-------:|-------:|------------:|
| 2026-06-18 |   4.95 |   8.09 |        7.27 |
| 2026-06-22 |   5.66 |  14.56 |        7.05 |
| 2026-06-23 |   7.46 |   9.88 |       12.09 |
| 2026-06-24 |   6.76 |  14.1  |        9.11 |
| 2026-06-25 |  19.33 |  16.26 |        9.77 |
| 2026-06-26 |  11.74 |  23.78 |       19.95 |
| 2026-06-29 |   8.52 |  20.6  |       12.57 |
| 2026-06-30 |   9.24 |   6.7  |        7.13 |
| 2026-07-01 |   7.39 |  15.81 |        7.06 |
| 2026-07-02 |  15.74 |   8.5  |       11.28 |

---

## get_average_true_range
Calculate the Average True Range (ATR) of a given price series.

The Average True Range (ATR) is a technical indicator that measures the volatility of an asset's price movements over a specified number of periods. It provides insights into the potential price range of an asset, which can help traders and investors make more informed decisions.

The formula is as follows:

$$
\text{TR} = \max(\text{high} - \text{low},\; \operatorname{abs}(\text{high} - \text{previous\_close}),\; \operatorname{abs}(\text{low} - \text{previous\_close}))
$$

$$
\text{ATR} = \text{Wilder's Smoothed Moving Average of TR over} \text{window} \text{periods}
$$

**Also known as:** ATR, volatility indicator. See `volatility_model.get_average_true_range` for the full formula; Wilder's smoothing constant (1/window) is slower than a standard EMA's (2/(window+1)) of the same window.

**Args:**

- <u>period (str):</u> Period for which to calculate the ATR.
- <u>window (int):</u> Number of periods for ATR calculation.
The number of periods (time intervals) over which to calculate the Average True Range.
- <u>rounding (int \| None):</u> Number of decimal places to round the resulting ATR values to.
If None, no rounding is performed.
- <u>growth (bool):</u> Flag indicating whether to return the ATR growth rate.
If True, the ATR growth rate is calculated.
- <u>lag (int \| list[int]):</u> Number of periods to lag the ATR values by.
If an integer is provided, all ATR values are lagged by the same number of periods.
If a list of integers is provided, each ATR value is lagged by the corresponding number of periods.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.Series: ATR values or ATR growth rate (if growth is True).
A pandas Series containing the calculated Average True Range values or growth rate for each period.

Formula:
The Average True Range (ATR) is calculated using the following steps:
1. Calculate the True Range (TR) for each period:
- True Range (TR) = max(high — low, abs(high — previous_close), abs(low — previous_close))
2. Calculate the Average True Range (ATR) over the specified window:
- ATR = EMA(TR, window), where EMA is the Exponential Moving Average.

**Notes:**

- ATR values are typically used to assess the volatility and potential price movement of an asset.
- A higher ATR value indicates higher volatility, while a lower ATR value suggests lower volatility.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_average_true_range()
```

Which returns:

| Date       |   AAPL |    MSFT |   Benchmark |
|:-----------|-------:|--------:|------------:|
| 2026-06-18 | 8.1636 | 12.5379 |     11.0343 |
| 2026-06-22 | 8.065  | 12.4293 |     11.1386 |
| 2026-06-23 | 7.945  | 11.7    |     11.7414 |
| 2026-06-24 | 7.85   | 11.4886 |     11.9636 |
| 2026-06-25 | 8.9529 | 11.9543 |     12.1729 |
| 2026-06-26 | 9.2186 | 12.5764 |     12.0579 |
| 2026-06-29 | 8.6679 | 13.4336 |     12.3993 |
| 2026-06-30 | 8.345  | 12.9479 |     11.1721 |
| 2026-07-01 | 8.3464 | 13.5143 |     10.7443 |
| 2026-07-02 | 8.9414 | 13.1671 |     10.4364 |

---

## get_supertrend
Calculate the Supertrend indicator for a given price series.

The Supertrend indicator plots a single trailing line that flips between sitting below price (in an uptrend) and above price (in a downtrend). The line is built from two bands offset from the median price ((High + Low) / 2) by a multiple of the Average True Range, which are then "ratcheted" period over period - each band can only move in the direction that tightens around price - so that the active band only flips to the other side once the closing price actually crosses it. This makes Supertrend both a trend filter (the flip direction signals a trend change) and a trailing stop-loss level.

The formula is as follows:

$$
\text{Basic Upper Band} = (\text{High} + \text{Low}) / 2 + \text{multiplier} \cdot \operatorname{ATR}(\text{window})
$$

$$
\text{Basic Lower Band} = (\text{High} + \text{Low}) / 2 - \text{multiplier} \cdot \operatorname{ATR}(\text{window})
$$

$$
\text{Final Upper Band} (t) = \text{Basic Upper Band} (t) \text{if Basic Upper Band} (t) < \text{Final Upper Band} (t-1) \text{or Close} (t-1) > \text{Final Upper Band} (t-1),\;\; \text{else Final Upper Band(t-1)}
$$

$$
\text{Final Lower Band} (t) = \text{Basic Lower Band} (t) \text{if Basic Lower Band} (t) > \text{Final Lower Band} (t-1) \text{or Close} (t-1) < \text{Final Lower Band} (t-1),\;\; \text{else Final Lower Band(t-1)}
$$

$$
\text{While in an uptrend},\;\; \text{Supertrend} = \text{Final Lower Band},\;\; \text{until Close crosses below it},\;\; \text{at which point the trend flips to} a \text{downtrend and Supertrend} = \text{Final Upper Band} (\text{and vice versa})
$$

**Also known as:** Supertrend, SuperTrend.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int, optional):</u> Number of periods for the underlying Average True Range
calculation. Defaults to 10.
- <u>multiplier (float, optional):</u> Multiplier applied to the Average True Range to
determine how far the bands sit from the median price. Defaults to 3.0.
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to.
Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Supertrend and
Trend Direction values. Defaults to False.
- <u>lag (int \| list[int], optional):</u> The lag to use for the growth calculation.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
Defaults to 1.

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
- If `growth` is set to True, the method calculates the growth of the Supertrend and
Trend Direction values using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_supertrend().xs("AAPL", level=1, axis="columns")
```

---

## get_keltner_channels
Calculate the Keltner Channels for a given price series.

The Keltner Channels consist of three lines: - Upper Channel Line = Exponential Moving Average (EMA) of High Prices + ATR * ATR Multiplier - Middle Channel Line = Exponential Moving Average (EMA) of Closing Prices - Lower Channel Line = Exponential Moving Average (EMA) of Low Prices - ATR * ATR Multiplier

The formula is as follows:

$$
\text{EMA} = (\text{Close} - \text{Previous EMA}) \cdot (2 / (1 + \text{Window})) + \text{Previous EMA}
$$

$$
\text{ATR} = \operatorname{EMA}(\text{TR},\; \text{ATR Window})
$$

$$
\text{Upper Channel Line} = \operatorname{EMA}(\text{High},\; \text{Window}) + \text{ATR} \cdot \text{ATR Multiplier}
$$

$$
\text{Middle Channel Line} = \operatorname{EMA}(\text{Close},\; \text{Window})
$$

$$
\text{Lower Channel Line} = \operatorname{EMA}(\text{Low},\; \text{Window}) - \text{ATR} \cdot \text{ATR Multiplier}
$$

**Also known as:** ATR-based bands, volatility channels.

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
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to.
Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the channels.
Defaults to False.
- <u>lag (int \| list[int], optional):</u> The lag to use for the growth calculation.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
Defaults to 1.

**Returns:**

pd.Series or pd.DataFrame: Keltner Channels (upper, middle, lower).

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates Keltner Channels
for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the channels using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_keltner_channels().xs("AAPL", level=1, axis="columns")
```

Which returns:

| Date       |   Lower Line |   Middle Line |   Upper Line |
|:-----------|-------------:|--------------:|-------------:|
| 2026-06-18 |      282.479 |       298.807 |      315.134 |
| 2026-06-22 |      282.437 |       298.567 |      314.697 |
| 2026-06-23 |      282.108 |       297.998 |      313.888 |
| 2026-06-24 |      281.642 |       297.342 |      313.042 |
| 2026-06-25 |      276.478 |       294.383 |      312.289 |
| 2026-06-26 |      274.532 |       292.969 |      311.407 |
| 2026-06-29 |      274.137 |       291.472 |      308.808 |
| 2026-06-30 |      274.501 |       291.191 |      307.881 |
| 2026-07-01 |      274.923 |       291.616 |      308.309 |
| 2026-07-02 |      276.002 |       293.884 |      311.767 |

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
\text{Middle Channel} = (\text{Upper Channel} + \text{Lower Channel}) / 2
$$

The current period is deliberately excluded from the lookback, per Donchian's original breakout rule and StockCharts' Price Channels definition - including it would make a channel break impossible by construction.

**Also known as:** Donchian Channels, price channel breakout.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>window (int, optional):</u> Number of periods for the Donchian Channels.
Defaults to 20.
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to.
Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the channels.
Defaults to False.
- <u>lag (int \| list[int], optional):</u> The lag to use for the growth calculation.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
Defaults to 1.

**Returns:**

pd.Series or pd.DataFrame: Donchian Channels (upper, middle, lower).

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates Donchian Channels
for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the channels using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_donchian_channels().xs("AAPL", level=1, axis="columns")
```

Which returns:

| Date       |   Lower Channel |   Middle Channel |   Upper Channel |
|:-----------|-----------------:|------------------:|-----------------:|
| 2026-06-18 |           279.4  |            300.13 |           320.86 |
| 2026-06-22 |           279.4  |            299.4  |           319.4  |
| 2026-06-23 |           279.4  |            298.7  |           318    |
| 2026-06-24 |           275.15 |            296.87 |           318.6  |
| 2026-06-25 |           275.15 |            296.87 |           318.6  |
| 2026-06-26 |           275.15 |            296.87 |           318.6  |
| 2026-06-29 |           275.15 |            296.87 |           318.6  |
| 2026-06-30 |           275.15 |            296.87 |           318.6  |
| 2026-07-01 |           275.15 |            296.87 |           318.6  |
| 2026-07-02 |           275.15 |            296.87 |           318.6  |

---

## get_volatility_cone
Retrieves the Volatility Cone for the specified period and assets.

The Volatility Cone summarizes the distribution of historical annualized realized volatility over a range of rolling windows, showing how the current realized volatility for each window compares to its own historical range. It is commonly used to judge whether current (or implied) volatility is cheap or expensive relative to history.

**Also known as:** volatility cone, realized volatility term structure.

**Args:**

- <u>windows (list[int] \| None, optional):</u> The rolling windows (in periods) to
calculate realized volatility for. Defaults to [10, 20, 30, 60, 90, 120].
- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The column name for closing prices in the historical data.
Defaults to "Adj Close".
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to.
If None, the rounding value specified during the initialization of the Toolkit instance will be used.
Defaults to None.

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

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

volatility_cone = toolkit.technicals.get_volatility_cone()

volatility_cone.xs("AAPL", level=1, axis="columns")
```

Which returns:

| Window   |   Min |   Median |   Max |   Current |
|:---------|------:|---------:|------:|----------:|
| 10       |  0.12 |     0.24 |  0.58 |      0.27 |
| 20       |  0.14 |     0.23 |  0.52 |      0.25 |
| 30       |  0.15 |     0.22 |  0.47 |      0.24 |

---

## get_trin
Calculate the TRIN (Arms Index) for a given price series.

TRIN compares the ratio of advancing to declining issues against the ratio of volume in advancing issues to volume in declining issues. It is a market-wide breadth reading computed across all tickers in the Toolkit instance (excluding the synthetic "Portfolio" and "Benchmark" columns), and the resulting single reading is broadcast to every ticker column so it lines up with the other breadth indicators.

The formula is as follows:

$$
\text{TRIN} = (\text{Advancing Issues} / \text{Declining Issues}) / (\text{Advancing Volume} / \text{Declining Volume})
$$

**Also known as:** Arms Index, TRIN.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The name of the column containing the close prices.
Defaults to "Adj Close".
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to.
Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int \| list[int], optional):</u> The lag to use for the growth calculation.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
Defaults to 1.

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

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_trin()
```

Which returns:

| Date       |   AAPL |   MSFT |   Benchmark |
|:-----------|-------:|-------:|------------:|
| 2026-06-18 |   0.85 |   0.85 |        0.85 |
| 2026-06-22 |   1.12 |   1.12 |        1.12 |
| 2026-06-23 |   0.97 |   0.97 |        0.97 |
| 2026-06-24 |   1.05 |   1.05 |        1.05 |
| 2026-06-25 |   1.31 |   1.31 |        1.31 |
| 2026-06-26 |   0.79 |   0.79 |        0.79 |
| 2026-06-29 |   0.91 |   0.91 |        0.91 |
| 2026-06-30 |   0.88 |   0.88 |        0.88 |
| 2026-07-01 |   0.94 |   0.94 |        0.94 |
| 2026-07-02 |   1.02 |   1.02 |        1.02 |

---

## get_new_highs_new_lows
Calculate the New Highs - New Lows for a given price series.

New Highs - New Lows measures the number of tickers reaching a new high over the specified window minus the number of tickers reaching a new low over the same window. It is a market-wide breadth reading computed across all tickers in the Toolkit instance (excluding the synthetic "Portfolio" and "Benchmark" columns), and the resulting single reading is broadcast to every ticker column so it lines up with the other breadth indicators.

The formula is as follows:

$$
\text{New Highs} - \text{New Lows} = (\text{Number of tickers at} a \text{window-period high}) - (\text{Number of tickers at} a \text{window-period low})
$$

**Also known as:** new highs minus new lows, record high percent.

**Args:**

- <u>period (str, optional):</u> The time period to consider for historical data.
Can be "daily", "weekly", "quarterly", or "yearly". Defaults to "daily".
- <u>close_column (str, optional):</u> The name of the column containing the close prices.
Defaults to "Adj Close".
- <u>window (int, optional):</u> Number of periods for the new high / new low lookback.
Defaults to 252.
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to.
Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the indicator values.
Defaults to False.
- <u>lag (int \| list[int], optional):</u> The lag to use for the growth calculation.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
Defaults to 1.

**Returns:**

pd.Series or pd.DataFrame: New Highs — New Lows values.

**Notes:**

- The method retrieves historical data based on the specified `period` and calculates
the New Highs — New Lows across all tickers in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the indicator values
using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT"])

toolkit.technicals.get_new_highs_new_lows()
```

Which returns:

| Date       |   AAPL |   MSFT |   Benchmark |
|:-----------|-------:|-------:|------------:|
| 2026-06-18 |      0 |      0 |           0 |
| 2026-06-22 |      0 |      0 |           0 |
| 2026-06-23 |     -1 |     -1 |          -1 |
| 2026-06-24 |      0 |      0 |           0 |
| 2026-06-25 |     -1 |     -1 |          -1 |
| 2026-06-26 |      0 |      0 |           0 |
| 2026-06-29 |      0 |      0 |           0 |
| 2026-06-30 |      1 |      1 |           1 |
| 2026-07-01 |      1 |      1 |           1 |
| 2026-07-02 |      1 |      1 |           1 |

---

