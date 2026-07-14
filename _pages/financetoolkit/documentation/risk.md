---
title: Risk
excerpt: The Risk module is meant to calculate important risk metrics such as Value at Risk (VaR), Conditional Value at Risk (cVaR), Maximum Drawdown, Correlations, GARCH, EWMA and more.
description: The Risk module is meant to calculate important risk metrics such as Value at Risk (VaR), Conditional Value at Risk (cVaR), Maximum Drawdown, Correlations, GARCH, EWMA and more.
author_profile: false
permalink: /projects/financetoolkit/docs/risk
classes: wide-sidebar
layout: single
redirect_from:
    - /risk
sidebar:
    nav: "financetoolkit-docs-risk"
---

The Risk module calculates important risk metrics such as Value at Risk (VaR), Conditional Value at Risk (CVaR), Maximum Drawdown, Correlations, GARCH, EWMA and more.

To install the FinanceToolkit it simply requires the following:

```python
pip install financetoolkit -U
```

{% include algolia.html %}

## collect_all_metrics
Calculates and collects all risk metrics.

**Args:**

- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
- <u>lag (int | str, optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>trailing (int):</u> Defines whether to select a trailing period.
E.g. when selecting 4 with quarterly data, the TTM is calculated.

**Returns:**

pd.Series or pd.DataFrame: Risk metrics calculated based on the specified parameters.

**Notes:**

- The method calculates various risk metrics for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the ratio values
using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(["AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

toolkit.risk.collect_all_metrics().xs("AAPL", level=1, axis=1)
```

Which returns:

|      |   Ulcer Index |   GARCH |   Skewness |   Kurtosis |   Downside Deviation |   Variance |   Volatility |
|:-----|--------------:|--------:|-----------:|-----------:|---------------------:|-----------:|-------------:|
| 2021 |        0.0376 |  0.0616 |    -0.0677 |     3.3347 |               0.0102 |     0.063  |       0.2511 |
| 2022 |        0.0672 |  0.1223 |     0.3199 |     4.012  |               0.0135 |     0.1274 |       0.357  |
| 2023 |        0.0332 |  0.1667 |    -0.0672 |     4.4211 |               0.0082 |     0.0412 |       0.203  |
| 2024 |        0.0341 |  0.2181 |     0.4479 |     6.516  |               0.0091 |     0.0515 |       0.2268 |
| 2025 |        0.0492 |  0.2452 |     1.1284 |    16.8074 |               0.0149 |     0.1056 |       0.3249 |
| 2026 |        0.0391 |  0.2585 |    -0.2958 |     4.5239 |               0.0119 |     0.0717 |       0.2677 |


---

## get_value_at_risk
Calculate the Value at Risk (VaR) of an investment portfolio or asset's returns.

Value at Risk (VaR) is a risk management metric that quantifies the maximum potential loss an investment portfolio or asset may experience over a specified time horizon and confidence level. It provides insights into the downside risk associated with an investment and helps investors make informed decisions about risk tolerance.

The VaR is calculated as the quantile of the return distribution, representing the loss threshold that is not expected to be exceeded with a given confidence level (e.g., 5% for alpha=0.05).

**Also known as:** VaR, maximum expected loss, portfolio loss risk.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, quarterly, or yearly).
Defaults to "yearly".
- <u>alpha (float, optional):</u> The confidence level for VaR calculation (e.g., 0.05 for 95% confidence).
Defaults to 0.05.
- <u>within_period (bool, optional):</u> Whether to calculate VaR within the specified period or for the entire
period. Thus whether to look at the VaR within a specific year (if period = 'yearly') or look at the entirety
of all years. Defaults to True.
- <u>rolling (int, optional):</u> The rolling window size to use for the calculation. If set, VaR is
calculated over a rolling window of this many periods across the full return history instead
of per `period` (e.g. a rolling 60-day VaR). Defaults to None.
- <u>rounding (int | None, optional):</u> The number of decimals to round the results to. Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the VaR values over time. Defaults to False.
- <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>distribution (str):</u> The distribution to use for the VaR calculations (historic, gaussian, cf,
studentt or evt). Defaults to "historic".
- <u>threshold_percentile (float, optional):</u> Only used when `distribution` is "evt". The percentile
of losses above which the Generalized Pareto Distribution is fitted. Defaults to 0.95.

**Returns:**

pd.Series: VaR values with time as the index.

**Notes:**

- The method retrieves historical return data based on the specified `period` and calculates VaR for each
asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of VaR values using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(["AMZN", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

toolkit.risk.get_value_at_risk()
```

Which returns:

|      |    AMZN |    TSLA |
|:-----|--------:|--------:|
| 2012 | -0.0244 | -0.0343 |
| 2013 | -0.0204 | -0.0537 |
| 2014 | -0.0312 | -0.0423 |
| 2015 | -0.0208 | -0.0422 |
| 2016 | -0.0288 | -0.0394 |
| 2017 | -0.0154 | -0.0345 |
| 2018 | -0.0416 | -0.0503 |
| 2019 | -0.0232 | -0.0492 |
| 2020 | -0.0369 | -0.0741 |
| 2021 | -0.0252 | -0.0499 |
| 2022 | -0.0518 | -0.0713 |
| 2023 | -0.0271 | -0.054  |


---

## get_conditional_value_at_risk
Calculate the Conditional Value at Risk (CVaR) of an investment portfolio or asset's returns.

Conditional Value at Risk (CVaR) is a risk management metric that quantifies the loss in the worst % of cases of an investment portfolio or asset may experience over a specified time horizon and confidence level. It provides insights into the downside risk associated with an investment and helps investors make informed decisions about risk tolerance.

The CVaR is calculated as the expected loss given that the loss threshold (VaR) with a given confidence level (e.g., 5% for alpha=0.05) is excceeded.

**Also known as:** CVaR, expected shortfall, ES, tail risk.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, quarterly, or yearly).
Defaults to "yearly".
- <u>alpha (float, optional):</u> The confidence level for CVaR calculation (e.g., 0.05 for 95% confidence).
Defaults to 0.05.
- <u>within_period (bool, optional):</u> Whether to calculate CVaR within the specified period or for the entire
period. Thus whether to look at the CVaR within a specific year (if period = 'yearly') or look at the entirety
of all years. Defaults to True.
- <u>rolling (int, optional):</u> The rolling window size to use for the calculation. If set, CVaR is
calculated over a rolling window of this many periods across the full return history instead
of per `period` (e.g. a rolling 60-day CVaR). Defaults to None.
- <u>rounding (int | None, optional):</u> The number of decimals to round the results to. Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the CVaR values over time. Defaults to False.
- <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>distribution (str):</u> The distribution to use for the CVaR calculations (historic, gaussian, studentt, laplace
or logistic). Defaults to "historic".

**Returns:**

pd.Series: CVaR values with time as the index.

**Notes:**

- The method retrieves historical return data based on the specified `period` and calculates CVaR for each
asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of CVaR values using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(["AMZN", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

toolkit.risk.get_conditional_value_at_risk()
```

Which returns:

|      |    AMZN |    TSLA |
|:-----|--------:|--------:|
| 2012 | -0.0302 | -0.0622 |
| 2013 | -0.0323 | -0.0807 |
| 2014 | -0.0552 | -0.0607 |
| 2015 | -0.0318 | -0.053  |
| 2016 | -0.0456 | -0.0604 |
| 2017 | -0.0236 | -0.0483 |
| 2018 | -0.0540 | -0.0746 |
| 2019 | -0.0327 | -0.0758 |
| 2020 | -0.0510 | -0.1262 |
| 2021 | -0.0327 | -0.0683 |
| 2022 | -0.0685 | -0.0914 |
| 2023 | -0.0397 | -0.0747 |


---

## get_entropic_value_at_risk
Calculate the Entropic Value at Risk (EVaR) of an investment portfolio or asset's returns.

Entropic Value at Risk (EVaR) is a risk management metric that quantifies upper bound for the value at risk (VaR) and the conditional value at risk (CVaR) over a specified time horizon and confidence level. EVaR is obtained from the Chernoff inequality. It provides insights into the downside risk associated with an investment and helps investors make informed decisions about risk tolerance.

The EVaR is calculated as the upper bound of VaR and CVaR with a given confidence level (e.g., 5% for alpha=0.05).

**Also known as:** EVaR.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, quarterly, or yearly).
Defaults to "yearly".
- <u>alpha (float, optional):</u> The confidence level for EVaR calculation (e.g., 0.05 for 95% confidence).
Defaults to 0.05.
- <u>within_period (bool, optional):</u> Whether to calculate EVaR within the specified period or for the entire
period. Thus whether to look at the CVaR within a specific year (if period = 'yearly') or look at the entirety
of all years. Defaults to True.
- <u>rounding (int | None, optional):</u> The number of decimals to round the results to. Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the CVaR values over time. Defaults to False.
- <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.Series: EVaR values with time as the index.

**Notes:**

- The method retrieves historical return data based on the specified `period` and calculates EVaR for each
asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of EVaR values using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(["AMZN", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

toolkit.risk.get_entropic_value_at_risk()
```

Which returns:

|      |    AMZN |    TSLA |   SPY |
|:-----|--------:|--------:|--------:|
| 2012 | -0.0392 | -0.0604 | -0.0177 |
| 2013 | -0.0377 | -0.0928 | -0.0152 |
| 2014 | -0.0481 | -0.0689 | -0.0162 |
| 2015 | -0.046  | -0.0564 | -0.0227 |
| 2016 | -0.043  | -0.0571 | -0.0188 |
| 2017 | -0.0289 | -0.0501 | -0.0091 |
| 2018 | -0.0518 | -0.085  | -0.0252 |
| 2019 | -0.0327 | -0.071  | -0.0173 |
| 2020 | -0.054  | -0.1211 | -0.0497 |
| 2021 | -0.0352 | -0.0782 | -0.0183 |
| 2022 | -0.0758 | -0.1012 | -0.0362 |
| 2023 | -0.0471 | -0.0793 | -0.0188 |


---

## get_conditional_drawdown_at_risk
Calculate the Conditional Drawdown at Risk (CDaR) of an investment portfolio or asset's returns.

Conditional Drawdown at Risk (CDaR) extends the concept of Value at Risk and Conditional Value at Risk to the drawdown series instead of the return series. It is calculated as the average of the worst drawdowns that exceed the Drawdown at Risk (DaR), i.e. the alpha-quantile of the drawdown distribution, giving insight into the depth of the most severe drawdowns an investment portfolio or asset could experience.

**Also known as:** CDaR.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, quarterly, or yearly).
Defaults to "yearly".
- <u>alpha (float, optional):</u> The confidence level for CDaR calculation (e.g., 0.05 for 95% confidence).
Defaults to 0.05.
- <u>within_period (bool, optional):</u> Whether to calculate CDaR within the specified period or for the entire
period. Thus whether to look at the CDaR within a specific year (if period = 'yearly') or look at the entirety
of all years. Defaults to True.
- <u>rolling (int, optional):</u> The rolling window size to use for the calculation. If set, CDaR is
calculated over a rolling window of this many periods across the full return history instead
of per `period`. Defaults to None.
- <u>rounding (int | None, optional):</u> The number of decimals to round the results to. Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the CDaR values over time. Defaults to False.
- <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.Series: CDaR values with time as the index.

**Notes:**

- The method retrieves historical return data based on the specified `period` and calculates CDaR for each
asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of CDaR values using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(["AMZN", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

toolkit.risk.get_conditional_drawdown_at_risk()
```

Which returns:

|      |    AMZN |    TSLA |   Benchmark |
|:-----|--------:|--------:|------------:|
| 2021 | -0.1325 | -0.3407 |     -0.0437 |
| 2022 | -0.499  | -0.6603 |     -0.2424 |
| 2023 | -0.1756 | -0.2867 |     -0.0832 |
| 2024 | -0.1612 | -0.3662 |     -0.0576 |
| 2025 | -0.2721 | -0.4558 |     -0.1459 |
| 2026 | -0.1869 | -0.2267 |     -0.072  |


---

## get_tail_ratio
Calculate the Tail Ratio of an investment portfolio or asset's returns.

The Tail Ratio compares the size of the right (gain) tail to the left (loss) tail of the return distribution, calculated as the absolute value of the (1 - alpha)-th percentile of returns divided by the absolute value of the alpha-th percentile of returns. A Tail Ratio above 1 indicates that best-case gains outsize worst-case losses.

**Also known as:** gain-to-pain tail ratio.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, quarterly, or yearly).
Defaults to "yearly".
- <u>alpha (float, optional):</u> The percentile used to define each tail (e.g., 0.05 uses the 5th and
95th percentile). Defaults to 0.05.
- <u>within_period (bool, optional):</u> Whether to calculate the Tail Ratio within the specified period or
for the entire period. Thus whether to look at the Tail Ratio within a specific year (if period =
'yearly') or look at the entirety of all years. Defaults to True.
- <u>rolling (int, optional):</u> The rolling window size to use for the calculation. If set, the Tail
Ratio is calculated over a rolling window of this many periods across the full return history
instead of per `period`. Defaults to None.
- <u>rounding (int | None, optional):</u> The number of decimals to round the results to. Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Tail Ratio values over time.
Defaults to False.
- <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.Series: Tail Ratio values with time as the index.

**Notes:**

- The method retrieves historical return data based on the specified `period` and calculates the Tail
Ratio for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of Tail Ratio values using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(["AMZN", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

toolkit.risk.get_tail_ratio()
```

Which returns:

|      |   AMZN |   TSLA |   Benchmark |
|:-----|-------:|-------:|------------:|
| 2021 | 0.8591 | 1.0173 |      1.0688 |
| 2022 | 0.8406 | 1.0049 |      0.9524 |
| 2023 | 1.2609 | 1.1958 |      1.0432 |
| 2024 | 1.1246 | 1.1942 |      0.9049 |
| 2025 | 0.9359 | 1.0702 |      0.93   |
| 2026 | 1.0012 | 0.9592 |      0.8828 |


---

## get_maximum_drawdown
Calculate the Maximum Drawdown (MDD) of an investment portfolio or asset's returns.

Maximum Drawdown (MDD) is a risk management metric that quantifies the largest historical loss of n investment portfolio or asset experienced over a specified time horizon. It provides insights into the downside risk associated with an investment and helps investors make informed decisions about risk tolerance.

**Also known as:** max drawdown, peak-to-trough decline.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, quarterly, or yearly).
Defaults to "yearly".
- <u>alpha (float, optional):</u> The confidence level for CVaR calculation (e.g., 0.05 for 95% confidence).
Defaults to 0.05.
- <u>within_period (bool, optional):</u> Whether to calculate CVaR within the specified period or for the entire
period. Thus whether to look at the CVaR within a specific year (if period = 'yearly') or look at the entirety
of all years. Defaults to True.
- <u>rounding (int | None, optional):</u> The number of decimals to round the results to. Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the CVaR values over time. Defaults to False.
- <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.Series: Maximum Drawdown values with time as the index.

**Notes:**

- The method retrieves historical return data based on the specified `period` and calculates MMD for each
asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of MMD values using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(["AMZN", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

toolkit.risk.get_maximum_drawdown()
```

Which returns:

|      |    AMZN |    TSLA |
|:-----|--------:|--------:|
| 2012 | -0.1570 | -0.1601 |
| 2013 | -0.1259 | -0.3768 |
| 2014 | -0.2948 | -0.3085 |
| 2015 | -0.1371 | -0.2669 |
| 2016 | -0.2432 | -0.357  |
| 2017 | -0.1085 | -0.2227 |
| 2018 | -0.3410 | -0.3399 |
| 2019 | -0.1561 | -0.4847 |
| 2020 | -0.2274 | -0.6063 |
| 2021 | -0.1457 | -0.3625 |
| 2022 | -0.5198 | -0.7272 |
| 2023 | -0.1964 | -0.2823 |


---

## get_maximum_drawdown_duration
Calculate the Maximum Drawdown Duration of an investment portfolio or asset's returns.

The Maximum Drawdown Duration is the number of periods between the peak and the lowest point of the largest drawdown, giving insight into how long the worst loss of value took to unfold.

**Also known as:** drawdown length.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, quarterly, or yearly).
Defaults to "yearly".
- <u>within_period (bool, optional):</u> Whether to calculate the duration within the specified period or
for the entire period. Thus whether to look at the duration within a specific year (if period =
'yearly') or look at the entirety of all years. Defaults to True.
- <u>rounding (int | None, optional):</u> The number of decimals to round the results to. Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the duration values over time. Defaults to False.
- <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.Series: Maximum Drawdown Duration values, in number of periods, with time as the index.

**Notes:**

- The method retrieves historical return data based on the specified `period` and calculates the Maximum
Drawdown Duration for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the duration values using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(["AMZN", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

toolkit.risk.get_maximum_drawdown_duration()
```

Which returns:

|      |   AMZN |   TSLA |   Benchmark |
|:-----|-------:|-------:|------------:|
| 2021 |     30 |     28 |          21 |
| 2022 |    248 |    247 |         195 |
| 2023 |     25 |     73 |          63 |
| 2024 |     23 |     76 |          14 |
| 2025 |     52 |     57 |          34 |
| 2026 |     24 |     64 |          43 |


---

## get_maximum_drawdown_recovery_time
Calculate the Maximum Drawdown Recovery Time of an investment portfolio or asset's returns.

The Maximum Drawdown Recovery Time is the number of periods it takes for the cumulative return to reach a new high after the lowest point of the largest drawdown. If the drawdown has not yet been recovered from within the selected period, this returns NaN.

**Also known as:** time to recovery, drawdown recovery.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, quarterly, or yearly).
Defaults to "yearly".
- <u>within_period (bool, optional):</u> Whether to calculate the recovery time within the specified period
or for the entire period. Thus whether to look at the recovery time within a specific year (if
period = 'yearly') or look at the entirety of all years. Defaults to True.
- <u>rounding (int | None, optional):</u> The number of decimals to round the results to. Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the recovery time values over time.
Defaults to False.
- <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.Series: Maximum Drawdown Recovery Time values, in number of periods, with time as the index.

**Notes:**

- The method retrieves historical return data based on the specified `period` and calculates the Maximum
Drawdown Recovery Time for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the recovery time values using the
specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(["AMZN", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

toolkit.risk.get_maximum_drawdown_recovery_time()
```

Which returns:

|      |   AMZN |   TSLA |   Benchmark |
|:-----|-------:|-------:|------------:|
| 2021 |    nan |    159 |          13 |
| 2022 |    nan |    nan |         nan |
| 2023 |     46 |    nan |          24 |
| 2024 |     66 |     51 |          32 |
| 2025 |    135 |    114 |          55 |
| 2026 |     40 |    nan |          11 |


---

## get_ulcer_index
The Ulcer Index is a financial metric used to assess the risk and volatility of an investment portfolio or asset. Developed by Peter Martin in the 1980s, the Ulcer Index is particularly useful for evaluating the downside risk and drawdowns associated with investments.

The Ulcer Index differs from traditional volatility measures like standard deviation or variance because it focuses on the depth and duration of drawdowns rather than the dispersion of returns.

The formula is a follows:

Ulcer Index = SQRT(SUM[(Pn / Highest High)^2] / n)

**Also known as:** UI, drawdown risk.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, quarterly, or yearly).
Defaults to "yearly".
- <u>rolling (int, optional):</u> The rolling period to use for the calculation. Defaults to 14.
- <u>rounding (int | None, optional):</u> The number of decimals to round the results to. Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the UI values over time. Defaults to False.
- <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.Series: UI values with time as the index.

**Notes:**

- The method retrieves historical return data based on the specified `period` and calculates UI for each
asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of VaR values using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(["AMZN", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

toolkit.risk.get_ulcer_index()
```

Which returns:

|      |   AMZN |   TSLA |   Benchmark |
|:-----|-------:|-------:|------------:|
| 2012 | 0.0497 | 0.0454 |      0.0234 |
| 2013 | 0.035  | 0.0829 |      0.0142 |
| 2014 | 0.0659 | 0.0746 |      0.0174 |
| 2015 | 0.0273 | 0.0624 |      0.0238 |
| 2016 | 0.0519 | 0.0799 |      0.0151 |
| 2017 | 0.0241 | 0.0616 |      0.0067 |
| 2018 | 0.0619 | 0.0892 |      0.0356 |
| 2019 | 0.0373 | 0.0839 |      0.016  |
| 2020 | 0.0536 | 0.1205 |      0.0594 |
| 2021 | 0.0427 | 0.085  |      0.0136 |
| 2022 | 0.1081 | 0.1373 |      0.0492 |
| 2023 | 0.0475 | 0.0815 |      0.0186 |


---

## get_garch
Calculates volatility forecasts based on the GARCH model.

GARCH (Generalized autoregressive conditional heteroskedasticity) is stochastic model for time series, which is for instance used to model volatility clusters, stock return and inflation. It is a generalisation of the ARCH models.

**Also known as:** GARCH, volatility clustering, conditional heteroscedasticity.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, quarterly, or yearly).
Defaults to "weekly".
- <u>t (int, optional):</u> Time steps to calculate GARCH for.
- <u>optimization_t (int, optional):</u> Time steps to optimize GRACH for. It is only used if no weights are given.
- <u>within_period (bool, optional):</u> Whether to calculate GARCH within the specified period or for the entire
period. Thus whether to look at the GARCH within a specific year (if period = 'yearly') or look at the
entirety of all years. Defaults to False.
- <u>rounding (int | None, optional):</u> The number of decimals to round the results to. Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the GARCH values over time. Defaults to False.
- <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.DataFrame | pd.Series: GARCH values

**Notes:**

- The method retrieves historical return data based on the specified `period` and calculates GARCH for each
asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of GARCH values using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(["AMZN", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

toolkit.risk.get_garch()
```

Which returns:

| Date   |   AMZN |   TSLA |   Benchmark |
|:-------|-------:|-------:|------------:|
| 2012Q4 | 0      |  0     |      0      |
| 2013Q1 | 0.0147 |  0.214 |      0.0008 |
| 2013Q2 | 0.0223 |  0.214 |      0.0024 |
| 2013Q3 | 0.0262 |  0.214 |      0.0029 |
| 2013Q4 | 0.0282 |  0.214 |      0.0034 |
| 2014Q1 | 0.0293 |  0.214 |      0.0045 |
| 2014Q2 | 0.0298 |  0.214 |      0.0045 |
| 2014Q3 | 0.03   |  0.214 |      0.0047 |
| 2014Q4 | 0.0302 |  0.214 |      0.0047 |
| 2015Q1 | 0.0303 |  0.214 |      0.0048 |


---

## get_garch_forecast
Calculates sigma_2 forecasts.

GARCH (Generalized autoregressive conditional heteroskedasticity) is stochastic model for time series, which is for instance used to model volatility clusters, stock return and inflation. It is a generalisation of the ARCH models.

The forecasting with GARCH is done with the following formula:

- sigma_l ** 2 + (sigma_t ** 2 - sigma_l ** 2) * (alpha + beta) ** (t - 1)

For more information about the method, see the following book:

- Finance Compact Plus Band 1, by Yvonne Seler Zimmerman and Heinz Zimmerman; ISBN: 978-3-907291-31-1

**Also known as:** volatility forecast, predicted volatility.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, quarterly, or yearly).
Defaults to "quarterly".
- <u>t (int, optional):</u> Time steps to calculate GARCH and to forecast sigma_2 values for.
- <u>within_period (bool, optional):</u> Whether to calculate GARCH within each specified period or all
at once. Thus whether to look at the GARCH within each specific year (if period = 'yearly') or
look at the entirety of all years. Defaults to False.
- <u>rounding (int | None, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the GARCH values over time. Defaults to
False.
- <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.DataFrame | pd.Series: sigma_2 forecast values

**Notes:**

- The method retrieves historical return data based on the specified `period` and calculates the sigma_2
forecast for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the forecasted simga_2 values using
the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(["AMZN", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

toolkit.risk.get_garch_forecast()
```

Which returns:

|      |   AMZN |     TSLA |   Benchmark |
|:-----|-------:|---------:|------------:|
| 2024 | 0      |    0     |      0      |
| 2025 | 0      |    0     |      0      |
| 2026 | 0.4156 |  252.921 |      0.0058 |
| 2027 | 0.7897 |  480.55  |      0.011  |
| 2028 | 1.1263 |  685.417 |      0.0156 |
| 2029 | 1.4293 |  869.796 |      0.0198 |
| 2030 | 1.702  | 1035.74  |      0.0236 |
| 2031 | 1.9474 | 1185.09  |      0.027  |
| 2032 | 2.1683 | 1319.5   |      0.0301 |
| 2033 | 2.3671 | 1440.47  |      0.0329 |


---

## get_skewness
Calculate the Skewness of an investment portfolio or asset's returns.

Skewness is a statistical measure used in finance to assess the asymmetry in the distribution of returns for an investment portfolio or asset over a defined period. It offers valuable insights into the shape of the return distribution, indicating whether returns are skewed towards the positive or negative side of the mean. Skewness is a crucial tool for investors and analysts seeking to understand the potential risk and return characteristics of an investment, aiding in the assessment of the distribution's tails and potential outliers. It provides a means to gauge the level of skew in returns, enabling more informed investment decisions and risk management strategies.

**Also known as:** return distribution asymmetry, tail skew.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, quarterly, or yearly).
Defaults to "yearly".
- <u>alpha (float, optional):</u> The confidence level for CVaR calculation (e.g., 0.05 for 95% confidence).
Defaults to 0.05.
- <u>within_period (bool, optional):</u> Whether to calculate CVaR within the specified period or for the entire
period. Thus whether to look at the CVaR within a specific year (if period = 'yearly') or look at the entirety
of all years. Defaults to True.
- <u>rolling (int, optional):</u> The rolling window size to use for the calculation. If set, Skewness is
calculated over a rolling window of this many periods across the full return history instead of
per `period`. Defaults to None.
- <u>rounding (int | None, optional):</u> The number of decimals to round the results to. Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the CVaR values over time. Defaults to False.
- <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.Series: CVaR values with time as the index.

**Notes:**

- The method retrieves historical return data based on the specified `period` and calculates Skew for each
asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of VaR values using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(["MSFT", "AAPL", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

toolkit.risk.get_skewness()
```

Which returns:

|      |    MSFT |    AAPL |    TSLA |
|:-----|--------:|--------:|--------:|
| 2019 | -0.194  | -0.9216 | -0.0646 |
| 2020 | -0.0747 | -0.0586 | -0.1824 |
| 2021 | -0.0194 | -0.0716 |  0.6572 |
| 2022 |  0.1478 |  0.3164 | -0.0263 |
| 2023 |  0.5252 |  0.0318 | -0.0972 |


---

## get_kurtosis
Calculate the Kurtosis of an investment portfolio or asset's returns.

Kurtosis is a statistical measure used in finance to evaluate the shape of the probability distribution of returns for an investment portfolio or asset over a defined time period. It assesses the "tailedness" of the return distribution, indicating whether returns have fatter or thinner tails compared to a normal distribution. Kurtosis plays a critical role in risk assessment by revealing the potential presence of extreme outliers or the likelihood of heavy tails in the return data. This information aids investors and analysts in understanding the degree of risk associated with an investment and assists in making more informed decisions regarding risk tolerance. In essence, kurtosis serves as a valuable tool for comprehending the distribution characteristics of returns, offering insights into the potential for rare but significant events in the financial markets.

**Also known as:** tail heaviness, fat tails, leptokurtosis.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, quarterly, or yearly).
Defaults to "yearly".
- <u>within_period (bool, optional):</u> Whether to calculate CVaR within the specified period or for the entire
period. Thus whether to look at the CVaR within a specific year (if period = 'yearly') or look at
the entirety of all years. Defaults to True.
- <u>fisher (bool, optional):</u> Whether to use Fisher's definition of kurtosis (kurtosis = 0.0
for a normal distribution).
- <u>rolling (int, optional):</u> The rolling window size to use for the calculation. If set, Kurtosis is
calculated over a rolling window of this many periods across the full return history instead of
per `period`. Defaults to None.
- <u>rounding (int | None, optional):</u> The number of decimals to round the results to. Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the CVaR values over time.
efaults to False.
- <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.Series: CVaR values with time as the index.

**Notes:**

- The method retrieves historical return data based on the specified `period` and calculates VaR for each
asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of VaR values using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(["MSFT", "AAPL", "TSLA"]], api_key="FINANCIAL_MODELING_PREP_KEY")

toolkit.risk.get_kurtosis()
```

Which returns:

|      |   MSFT |    AAPL |   TSLA |
|:-----|-------:|--------:|-------:|
| 2019 | 4.0972 | 10.0741 | 9.128  |
| 2020 | 9.2914 |  6.6307 | 5.2189 |
| 2021 | 3.3152 |  3.3352 | 7.3197 |
| 2022 | 3.852  |  4.0085 | 3.3553 |
| 2023 | 4.2908 |  4.4568 | 4.07   |


---

## get_variance
Calculate the Variance of an investment portfolio or asset's returns for a given period based on the daily historical returns.

Variance measures the spread or dispersion of returns around the mean. A higher Variance indicates more variability in the returns, while a lower Variance suggests that the returns are closer to the mean.

The daily Variance is scaled to the given period by multiplying it with the number of trading days within that period (e.g. 252 / 52 for weekly).

**Also known as:** dispersion, spread.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (weekly, monthly,
quarterly, or yearly). Defaults to "yearly".
- <u>rolling (int, optional):</u> The rolling window size to use for the calculation. If set,
Variance is calculated over a rolling window of this many periods (e.g. period='monthly'
and rolling=6 gives the rolling 6-month Variance) instead of one value per `period`.
Defaults to None.
- <u>rounding (int | None, optional):</u> The number of decimals to round the results to. Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Variance values over time. Defaults to False.
- <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.Series: Variance values with time as the index.

**Notes:**

- The method retrieves the daily historical return data and calculates the Variance for
the specified `period` for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of Variance values using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(["AMZN", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

toolkit.risk.get_variance(period="yearly")
```

Which returns:

| Date   |   AMZN |   TSLA |   Benchmark |
|:-------|-------:|-------:|------------:|
| 2021   | 0.058  | 0.2999 |      0.0172 |
| 2022   | 0.2508 | 0.4446 |      0.0589 |
| 2023   | 0.109  | 0.2922 |      0.0174 |
| 2024   | 0.0789 | 0.4032 |      0.0158 |
| 2025   | 0.1184 | 0.4031 |      0.0379 |
| 2026   | 0.0999 | 0.1859 |      0.02   |


---

## get_volatility
Calculate the Volatility of an investment portfolio or asset's returns for a given period based on the daily historical returns.

Volatility measures the amount of dispersion or variability in returns. It is the square root of the Variance. A higher Volatility indicates greater variability, while a lower Volatility suggests that returns are closer to the mean.

The daily Volatility is scaled to the given period by multiplying it with the square root of the number of trading days within that period (e.g. SQRT(252 / 52) for weekly).

**Also known as:** standard deviation of returns.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (weekly, monthly,
quarterly, or yearly). Defaults to "yearly".
- <u>rolling (int, optional):</u> The rolling window size to use for the calculation. If set,
Volatility is calculated over a rolling window of this many periods (e.g. period='monthly'
and rolling=6 gives the rolling 6-month Volatility) instead of one value per `period`.
Defaults to None.
- <u>rounding (int | None, optional):</u> The number of decimals to round the results to. Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Volatility values over time.
Defaults to False.
- <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.Series: Volatility values with time as the index.

**Notes:**

- The method retrieves the daily historical return data and calculates the Volatility for
the specified `period` for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of Volatility values using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(["AMZN", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

toolkit.risk.get_volatility(period="yearly")
```

Which returns:

| Date   |   AMZN |   TSLA |   Benchmark |
|:-------|-------:|-------:|------------:|
| 2021   | 0.2409 | 0.5476 |      0.131  |
| 2022   | 0.5008 | 0.6668 |      0.2427 |
| 2023   | 0.3302 | 0.5406 |      0.1318 |
| 2024   | 0.2809 | 0.635  |      0.1258 |
| 2025   | 0.3442 | 0.6349 |      0.1948 |
| 2026   | 0.3161 | 0.4312 |      0.1414 |


---

## get_excess_volatility
Calculate the Excess Volatility of an investment portfolio or asset's returns for a given period based on the daily historical returns.

Excess Volatility is the Volatility of the Excess Return, i.e. the daily return minus the risk free rate, scaled to the given period in the same way as the Volatility.

**Also known as:** standard deviation of excess returns.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (weekly, monthly,
quarterly, or yearly). Defaults to "yearly".
- <u>rolling (int, optional):</u> The rolling window size to use for the calculation. If set,
Excess Volatility is calculated over a rolling window of this many periods (e.g.
period='monthly' and rolling=6 gives the rolling 6-month Excess Volatility) instead of
one value per `period`. Defaults to None.
- <u>rounding (int | None, optional):</u> The number of decimals to round the results to. Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Excess Volatility values
over time. Defaults to False.
- <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.Series: Excess Volatility values with time as the index.

**Notes:**

- The method retrieves the daily historical return data and calculates the Excess Volatility for
the specified `period` for each asset in the Toolkit instance.
- The risk-free rate is often represented by the return of a risk-free investment, such as a Treasury bond.
- If `growth` is set to True, the method calculates the growth of Excess Volatility values using
the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(["AMZN", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

toolkit.risk.get_excess_volatility(period="yearly")
```

Which returns:

| Date   |   AMZN |   TSLA |   Benchmark |
|:-------|-------:|-------:|------------:|
| 2021   | 0.2414 | 0.5483 |      0.1333 |
| 2022   | 0.5207 | 0.686  |      0.2663 |
| 2023   | 0.3421 | 0.5535 |      0.1527 |
| 2024   | 0.2841 | 0.6346 |      0.1336 |
| 2025   | 0.3435 | 0.635  |      0.1946 |
| 2026   | 0.3196 | 0.4331 |      0.1446 |


---

## get_downside_deviation
Calculate the Downside Deviation of an investment portfolio or asset's returns.

The Downside Deviation, also known as semi-deviation, is the standard deviation of only the returns that fall below a minimum acceptable return (MAR), isolating the volatility of negative outcomes from the volatility of the overall return distribution. It underlies risk-adjusted return measures such as the Sortino Ratio and the Omega Ratio.

**Also known as:** semi-deviation, downside risk, downside volatility.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, quarterly, or yearly).
Defaults to "yearly".
- <u>minimum_acceptable_return (float, optional):</u> The minimum acceptable return (MAR) used as the
threshold below which returns are considered downside. Defaults to 0.0.
- <u>within_period (bool, optional):</u> Whether to calculate the Downside Deviation within the specified
period or for the entire period. Thus whether to look at the Downside Deviation within a specific
year (if period = 'yearly') or look at the entirety of all years. Defaults to True.
- <u>rolling (int, optional):</u> The rolling window size to use for the calculation. If set, the Downside
Deviation is calculated over a rolling window of this many periods across the full return history
instead of per `period`. Defaults to None.
- <u>rounding (int | None, optional):</u> The number of decimals to round the results to. Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Downside Deviation values over
time. Defaults to False.
- <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.Series: Downside Deviation values with time as the index.

**Notes:**

- The method retrieves historical return data based on the specified `period` and calculates the
Downside Deviation for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the Downside Deviation values using
the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(["AMZN", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

toolkit.risk.get_downside_deviation()
```

Which returns:

|      |   AMZN |   TSLA |   Benchmark |
|:-----|-------:|-------:|------------:|
| 2021 | 0.0106 | 0.0215 |      0.0058 |
| 2022 | 0.0202 | 0.0283 |      0.0095 |
| 2023 | 0.0129 | 0.0217 |      0.005  |
| 2024 | 0.0118 | 0.0227 |      0.006  |
| 2025 | 0.0146 | 0.0257 |      0.0096 |
| 2026 | 0.0123 | 0.0165 |      0.0061 |


---

## get_mean_absolute_deviation
Calculate the Mean Absolute Deviation (MAD) of an investment portfolio or asset's returns for a given period based on the daily historical returns.

MAD measures the average absolute distance of each return from the mean return. Unlike Variance and Volatility, it does not square the deviations, making it less sensitive to outliers.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (weekly, monthly,
quarterly, or yearly). Defaults to "yearly".
- <u>rounding (int | None, optional):</u> The number of decimals to round the results to. Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the MAD values over time. Defaults to False.
- <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.Series: Mean Absolute Deviation values with time as the index.

**Notes:**

- The method retrieves the daily historical return data and calculates the MAD for
the specified `period` for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of MAD values using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(["AMZN", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

toolkit.risk.get_mean_absolute_deviation(period="yearly")
```

Which returns:

| Date   |   AMZN |   TSLA |   Benchmark |
|:-------|-------:|-------:|------------:|
| 2021   | 0.0114 | 0.0246 |      0.0062 |
| 2022   | 0.0235 | 0.032  |      0.0119 |
| 2023   | 0.0156 | 0.0255 |      0.0065 |
| 2024   | 0.0132 | 0.0286 |      0.0058 |
| 2025   | 0.015  | 0.0292 |      0.0074 |
| 2026   | 0.0157 | 0.0216 |      0.0067 |


---

## get_coefficient_of_variation
Calculate the Coefficient of Variation (CV) of an investment portfolio or asset's returns for a given period based on the daily historical returns.

The Coefficient of Variation is the ratio of the standard deviation to the mean of returns, which normalizes dispersion relative to the average return. This makes it useful for comparing the relative volatility of assets with different average returns, which a raw standard deviation cannot do.

**Also known as:** relative standard deviation.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (weekly, monthly,
quarterly, or yearly). Defaults to "yearly".
- <u>rounding (int | None, optional):</u> The number of decimals to round the results to. Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the CV values over time. Defaults to False.
- <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.Series: Coefficient of Variation values with time as the index.

**Notes:**

- The method retrieves the daily historical return data and calculates the CV for
the specified `period` for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of CV values using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(["AMZN", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

toolkit.risk.get_coefficient_of_variation(period="yearly")
```

Which returns:

| Date   |     AMZN |      TSLA |   Benchmark |
|:-------|---------:|----------:|------------:|
| 2021   |  73.121  |   15.7477 |      8.3938 |
| 2022   | -14.1417 |  -12.7544 |    -20.4791 |
| 2023   |   8.0356 |   10.0506 |      9.1833 |
| 2024   |  10.9398 |   14.7623 |      9.1557 |
| 2025   |  49.9543 |   32.8037 |     18.0122 |
| 2026   |  31.132  | -163.952  |     11.047  |


---

## get_ewma_volatility
Calculate the exponentially weighted moving average (EWMA) Volatility of an investment portfolio or asset's daily returns, following the RiskMetrics methodology.

Unlike a fixed-window rolling Volatility, EWMA Volatility weights recent observations more heavily than older ones, so it reacts faster to changes in the underlying volatility regime. It is a simpler, more interpretable alternative to a full GARCH fit.

The formula is as follows:

- EWMA Variance(t) = lambda * EWMA Variance(t-1) + (1 - lambda) * Return(t-1) ** 2

**Also known as:** RiskMetrics volatility, exponentially weighted volatility.

**Args:**

- <u>lambda_ (float, optional):</u> The decay factor. Higher values weight the past
more heavily (slower to react), lower values weight recent returns more
heavily (faster to react). RiskMetrics uses 0.94 for daily data. Defaults to 0.94.
- <u>rounding (int | None, optional):</u> The number of decimals to round the results to. Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the EWMA Volatility values over
time. Defaults to False.
- <u>lag (int | list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.Series: Daily EWMA Volatility values with time as the index.

**Notes:**

- The method retrieves the daily historical return data and calculates the EWMA Volatility for
each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the EWMA Volatility values using
the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(["AMZN", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

toolkit.risk.get_ewma_volatility()
```

Which returns:

| Date       |   AMZN |   TSLA |   Benchmark |
|:-----------|-------:|-------:|------------:|
| 2026-06-22 | 0.0229 | 0.0279 |      0.0099 |
| 2026-06-23 | 0.0223 | 0.0304 |      0.0103 |
| 2026-06-24 | 0.0216 | 0.0296 |      0.01   |
| 2026-06-25 | 0.022  | 0.0287 |      0.0097 |
| 2026-06-26 | 0.0225 | 0.0281 |      0.0096 |
| 2026-06-29 | 0.0234 | 0.0345 |      0.0101 |
| 2026-06-30 | 0.0228 | 0.0338 |      0.01   |
| 2026-07-01 | 0.0224 | 0.0328 |      0.0097 |
| 2026-07-02 | 0.0218 | 0.037  |      0.0094 |
| 2026-07-06 | 0.0211 | 0.0395 |      0.0093 |


---

## get_autocorrelation
Calculate the Autocorrelation Function (ACF) of each asset's daily returns for a range of lags.

The ACF measures the correlation between a return series and a lagged version of itself. A significant ACF at a given lag indicates that returns are not fully independent over time, which is relevant for assessing return predictability and volatility clustering (as opposed to a trading-signal use case, which is why this lives in the Risk module rather than Technicals).

**Args:**

- <u>lags (int, optional):</u> The number of lags to calculate the ACF for. Defaults to 10.
- <u>rounding (int | None, optional):</u> The number of decimals to round the results to.
Defaults to 4.

**Returns:**

pd.DataFrame: The ACF value for each lag (rows) and each asset (columns).

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(["AMZN", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

toolkit.risk.get_autocorrelation()
```

Which returns:

|    |    AMZN |    TSLA |   Benchmark |
|---:|--------:|--------:|------------:|
|  1 | -0.0109 | -0.0306 |     -0.0366 |
|  2 | -0.0013 |  0.0121 |      0.0066 |
|  3 | -0.0216 |  0.0006 |     -0.0571 |
|  4 |  0.01   |  0.0117 |     -0.0344 |
|  5 | -0.0063 | -0.0302 |      0.0002 |
|  6 |  0.0018 |  0.0298 |     -0.022  |
|  7 | -0.0451 |  0.0209 |     -0.0076 |
|  8 | -0.0281 |  0.0092 |     -0.013  |
|  9 |  0.0017 |  0.0675 |      0.0529 |
| 10 | -0.0162 | -0.0293 |     -0.0133 |


---

## get_hurst_exponent
Calculate the Hurst Exponent of each asset's daily returns, a measure of long-term memory that indicates whether a series is mean-reverting, trending, or a random walk.

The Hurst Exponent (H) is interpreted as follows:

- H < 0.5: the series is mean-reverting (anti-persistent).
- H = 0.5: the series is a random walk (no memory).
- H > 0.5: the series is trending (persistent).

**Args:**

- <u>max_lag (int, optional):</u> The maximum lag to use when estimating the exponent.
Defaults to 20.
- <u>rounding (int | None, optional):</u> The number of decimals to round the results to.
Defaults to 4.

**Returns:**

pd.Series: The estimated Hurst Exponent for each asset.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(["AMZN", "TSLA"], api_key="FINANCIAL_MODELING_PREP_KEY")

toolkit.risk.get_hurst_exponent()
```

Which returns:

|           |       0 |
|:----------|--------:|
| AMZN      | -0.0082 |
| TSLA      |  0.0099 |
| Benchmark | -0.0077 |


---

