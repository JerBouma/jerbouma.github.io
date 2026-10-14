---
title: Risk
seo_title: "Risk Module | Finance Toolkit"
seo_title_suffix: false
excerpt: The Risk module is meant to calculate important risk metrics such as Value at Risk (VaR), Conditional Value at Risk (cVaR), Maximum Drawdown, Correlations, GARCH, EWMA and more.
description: "Reference for every function and parameter in the Finance Toolkit's Risk module: Value at Risk, Conditional VaR, maximum drawdown, GARCH and EWMA."
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

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly, or yearly).
Defaults to "quarterly" if the Toolkit is initialised with quarterly=True, otherwise "yearly".
- <u>rounding (int, optional):</u> The number of decimals to round the results to. Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the ratios. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.Series or pd.DataFrame: Risk metrics calculated based on the specified parameters.

**Notes:**

- The method calculates various risk metrics for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the ratio values
using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.collect_all_metrics().xs("AAPL", level=1, axis=1)
```

Which returns:

|      |   Ulcer Index |    GARCH |   Skewness |   Kurtosis |   Downside Deviation |   Variance |   Volatility |
|:-----|--------------:|---------:|-----------:|-----------:|---------------------:|-----------:|-------------:|
| 2021 |        0.0373 | nan      |    -0.0735 |     3.4146 |               0.0105 |     0.0626 |       0.2502 |
| 2022 |        0.067  |   0.0697 |     0.3167 |     4.054  |               0.016  |     0.1274 |       0.357  |
| 2023 |        0.033  |   0.1142 |    -0.0662 |     4.4804 |               0.0082 |     0.0412 |       0.2031 |
| 2024 |        0.034  |   0.1142 |     0.4447 |     6.6121 |               0.0093 |     0.0514 |       0.2268 |
| 2025 |        0.0492 |   0.1142 |     1.1299 |    17.0667 |               0.0136 |     0.1056 |       0.325  |

---

## get_value_at_risk
Calculate the Value at Risk (VaR) of an investment portfolio or asset's returns.

Value at Risk (VaR) is a risk management metric that quantifies the maximum potential loss an investment portfolio or asset may experience over a specified time horizon and confidence level. It provides insights into the downside risk associated with an investment and helps investors make informed decisions about risk tolerance.

The VaR is calculated as the quantile of the return distribution, representing the loss threshold that is not expected to be exceeded with a given confidence level (e.g., 5% for alpha=0.05).

**Also known as:** VaR, maximum expected loss, portfolio loss risk.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>alpha (float, optional):</u> The confidence level for VaR calculation (e.g., 0.05 for 95% confidence).
Defaults to 0.05.
- <u>within_period (bool, optional):</u> Whether to calculate VaR within the specified period or for the entire
period. Thus whether to look at the VaR within a specific year (if period = 'yearly') or look at the entirety
of all years. Defaults to False. Note that this requires intraday data when period = 'daily', since a
single day only nests observations when intraday data was fetched.
- <u>rolling (int, optional):</u> The rolling window size to use for the calculation. If set, VaR is
calculated over a rolling window of this many periods across the full return history instead
of per `period` (e.g. a rolling 60-day VaR). Only available for
`distribution="historic"`; see `get_var_backtest` for a rolling, out-of-sample VaR path
under the parametric distributions. Defaults to None.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the VaR values over time. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>distribution (str):</u> The distribution to use for the VaR calculations (historic, gaussian, cf,
cornish-fisher, studentt or evt). Defaults to "historic". Note that "cf" and "cornish-fisher"
both adjust the gaussian quantile for skewness and kurtosis, but "cornish-fisher" uses the
more standard Cornish-Fisher expansion (see `var_model.get_var_cornish_fisher`), while "cf"
is kept for backwards compatibility.
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

toolkit = Toolkit(
    ["AMZN", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_value_at_risk(period="yearly", within_period=True)
```

Which returns:

|      |    AMZN |    TSLA |   Benchmark |
|:-----|--------:|--------:|------------:|
| 2021 | -0.0253 | -0.05   |     -0.0126 |
| 2022 | -0.0518 | -0.0714 |     -0.0262 |
| 2023 | -0.0273 | -0.0505 |     -0.0139 |
| 2024 | -0.0248 | -0.0522 |     -0.0132 |
| 2025 | -0.0305 | -0.0553 |     -0.0165 |

---

## get_conditional_value_at_risk
Calculate the Conditional Value at Risk (CVaR) of an investment portfolio or asset's returns.

Conditional Value at Risk (CVaR) is a risk management metric that quantifies the loss in the worst % of cases of an investment portfolio or asset may experience over a specified time horizon and confidence level. It provides insights into the downside risk associated with an investment and helps investors make informed decisions about risk tolerance.

The CVaR is calculated as the expected loss given that the loss threshold (VaR) with a given confidence level (e.g., 5% for alpha=0.05) is exceeded.

**Also known as:** CVaR, expected shortfall, ES, tail risk.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>alpha (float, optional):</u> The confidence level for CVaR calculation (e.g., 0.05 for 95% confidence).
Defaults to 0.05.
- <u>within_period (bool, optional):</u> Whether to calculate CVaR within the specified period or for the entire
period. Thus whether to look at the CVaR within a specific year (if period = 'yearly') or look at the entirety
of all years. Defaults to False. Note that this requires intraday data when period = 'daily', since a
single day only nests observations when intraday data was fetched.
- <u>rolling (int, optional):</u> The rolling window size to use for the calculation. If set, CVaR is
calculated over a rolling window of this many periods across the full return history instead
of per `period` (e.g. a rolling 60-day CVaR). Only available for
`distribution="historic"`; see `get_acerbi_szekely_test` for a rolling, out-of-sample CVaR
path under the parametric distributions. Defaults to None.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the CVaR values over time. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>distribution (str):</u> The distribution to use for the CVaR calculations (historic, gaussian, studentt, laplace,
logistic, cornish-fisher or evt). Defaults to "historic".
- <u>threshold_percentile (float, optional):</u> Only used when `distribution` is "evt". The percentile
of losses above which the Generalized Pareto Distribution is fitted. Defaults to 0.95.

**Returns:**

pd.Series: CVaR values with time as the index.

**Notes:**

- The method retrieves historical return data based on the specified `period` and calculates CVaR for each
asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of CVaR values using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AMZN", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_conditional_value_at_risk(period="yearly", within_period=True)
```

Which returns:

|      |    AMZN |    TSLA |   Benchmark |
|:-----|--------:|--------:|------------:|
| 2021 | -0.0327 | -0.0683 |     -0.0183 |
| 2022 | -0.0685 | -0.0914 |     -0.0335 |
| 2023 | -0.0413 | -0.071  |     -0.0157 |
| 2024 | -0.0372 | -0.0776 |     -0.0189 |
| 2025 | -0.047  | -0.0821 |     -0.0275 |

---

## get_entropic_value_at_risk
Calculate the Entropic Value at Risk (EVaR) of an investment portfolio or asset's returns.

Entropic Value at Risk (EVaR) is a risk management metric that quantifies upper bound for the value at risk (VaR) and the conditional value at risk (CVaR) over a specified time horizon and confidence level. EVaR is obtained from the Chernoff inequality. It provides insights into the downside risk associated with an investment and helps investors make informed decisions about risk tolerance.

The EVaR is calculated as the upper bound of VaR and CVaR with a given confidence level (e.g., 5% for alpha=0.05).

**Also known as:** EVaR.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>alpha (float, optional):</u> The confidence level for EVaR calculation (e.g., 0.05 for 95% confidence).
Defaults to 0.05.
- <u>within_period (bool, optional):</u> Whether to calculate EVaR within the specified period or for the entire
period. Thus whether to look at the CVaR within a specific year (if period = 'yearly') or look at the entirety
of all years. Defaults to False. Note that this requires intraday data when period = 'daily', since a
single day only nests observations when intraday data was fetched.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the CVaR values over time. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
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

toolkit = Toolkit(
    ["AMZN", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_entropic_value_at_risk(period="yearly", within_period=True)
```

Which returns:

|      |    AMZN |    TSLA |   Benchmark |
|:-----|--------:|--------:|------------:|
| 2021 | -0.0366 | -0.0821 |     -0.0188 |
| 2022 | -0.0793 | -0.1059 |     -0.038  |
| 2023 | -0.0482 | -0.0798 |     -0.0191 |
| 2024 | -0.0416 | -0.095  |     -0.0184 |
| 2025 | -0.0525 | -0.0965 |     -0.0293 |

---

## get_conditional_drawdown_at_risk
Calculate the Conditional Drawdown at Risk (CDaR) of an investment portfolio or asset's returns.

Conditional Drawdown at Risk (CDaR) extends the concept of Value at Risk and Conditional Value at Risk to the drawdown series instead of the return series. It is calculated as the average of the worst drawdowns that exceed the Drawdown at Risk (DaR), i.e. the alpha-quantile of the drawdown distribution, giving insight into the depth of the most severe drawdowns an investment portfolio or asset could experience.

**Also known as:** CDaR.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>alpha (float, optional):</u> The confidence level for CDaR calculation (e.g., 0.05 for 95% confidence).
Defaults to 0.05.
- <u>within_period (bool, optional):</u> Whether to calculate CDaR within the specified period or for the entire
period. Thus whether to look at the CDaR within a specific year (if period = 'yearly') or look at the entirety
of all years. Defaults to False. Note that this requires intraday data when period = 'daily', since a
single day only nests observations when intraday data was fetched.
- <u>rolling (int, optional):</u> The rolling window size to use for the calculation. If set, CDaR is
calculated over a rolling window of this many periods across the full return history instead
of per `period`. Defaults to None.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the CDaR values over time. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
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

toolkit = Toolkit(
    ["AMZN", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_conditional_drawdown_at_risk(period="yearly", within_period=True)
```

Which returns:

|      |    AMZN |    TSLA |   Benchmark |
|:-----|--------:|--------:|------------:|
| 2021 | -0.1325 | -0.3407 |     -0.0413 |
| 2022 | -0.499  | -0.6603 |     -0.2343 |
| 2023 | -0.1756 | -0.2867 |     -0.0806 |
| 2024 | -0.1612 | -0.3662 |     -0.0576 |
| 2025 | -0.2721 | -0.4558 |     -0.1434 |

---

## get_tail_ratio
Calculate the Tail Ratio of an investment portfolio or asset's returns.

The Tail Ratio compares the size of the right (gain) tail to the left (loss) tail of the return distribution, calculated as the absolute value of the (1 - alpha)-th percentile of returns divided by the absolute value of the alpha-th percentile of returns. A Tail Ratio above 1 indicates that best-case gains outsize worst-case losses.

**Also known as:** gain-to-pain tail ratio.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>alpha (float, optional):</u> The percentile used to define each tail (e.g., 0.05 uses the 5th and
95th percentile). Defaults to 0.05.
- <u>within_period (bool, optional):</u> Whether to calculate the Tail Ratio within the specified period or
for the entire period. Thus whether to look at the Tail Ratio within a specific year (if period =
'yearly') or look at the entirety of all years. Defaults to False.
Note that this requires intraday data when period = 'daily', since a
single day only nests observations when intraday data was fetched.
- <u>rolling (int, optional):</u> The rolling window size to use for the calculation. If set, the Tail
Ratio is calculated over a rolling window of this many periods across the full return history
instead of per `period`. Defaults to None.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Tail Ratio values over time.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
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

toolkit = Toolkit(
    ["AMZN", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_tail_ratio(period="yearly", within_period=True)
```

Which returns:

|      |   AMZN |   TSLA |   Benchmark |
|:-----|-------:|-------:|------------:|
| 2021 | 0.8591 | 1.0173 |      1.1327 |
| 2022 | 0.8406 | 1.0049 |      0.9524 |
| 2023 | 1.2609 | 1.1958 |      1.0466 |
| 2024 | 1.1246 | 1.1942 |      0.9091 |
| 2025 | 0.9359 | 1.0702 |      0.93   |

---

## get_maximum_drawdown
Calculate the Maximum Drawdown (MDD) of an investment portfolio or asset's returns.

Maximum Drawdown (MDD) is a risk management metric that quantifies the largest historical loss of an investment portfolio or asset experienced over a specified time horizon. It provides insights into the downside risk associated with an investment and helps investors make informed decisions about risk tolerance.

**Also known as:** max drawdown, peak-to-trough decline.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>within_period (bool, optional):</u> Whether to calculate the Maximum Drawdown within the specified period
or for the entire period. Thus whether to look at the Maximum Drawdown within a specific year
(if period = 'yearly') or look at the entirety of all years. Defaults to False.
Note that this requires intraday data when period = 'daily', since a
single day only nests observations when intraday data was fetched.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Maximum Drawdown values over time.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.Series: Maximum Drawdown values with time as the index.

**Notes:**

- The method retrieves historical return data based on the specified `period` and calculates MMD for each
asset in the Toolkit instance.
- Without `within_period`, the drawdown is measured on the returns of the chosen period, so
period="yearly" only compares year-end values: it is 0 when every year in the range closed at a
new high, even if prices fell within a year. Use period="daily" for the deepest decline, or
within_period=True for the deepest decline within each year.
- If `growth` is set to True, the method calculates the growth of MMD values using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AMZN", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_maximum_drawdown(period="yearly", within_period=True)
```

Which returns:

|      |    AMZN |    TSLA |   Benchmark |
|:-----|--------:|--------:|------------:|
| 2021 | -0.146  | -0.3625 |     -0.051  |
| 2022 | -0.5197 | -0.7272 |     -0.245  |
| 2023 | -0.1965 | -0.3273 |     -0.0999 |
| 2024 | -0.1949 | -0.4279 |     -0.0841 |
| 2025 | -0.3088 | -0.4821 |     -0.1877 |

---

## get_maximum_drawdown_duration
Calculate the Maximum Drawdown Duration of an investment portfolio or asset's returns.

The Maximum Drawdown Duration is the number of periods between the peak and the lowest point of the largest drawdown, giving insight into how long the worst loss of value took to unfold.

**Also known as:** drawdown length.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>within_period (bool, optional):</u> Whether to calculate the duration within the specified period or
for the entire period. Thus whether to look at the duration within a specific year (if period =
'yearly') or look at the entirety of all years. Defaults to False.
Note that this requires intraday data when period = 'daily', since a
single day only nests observations when intraday data was fetched.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the duration values over time. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
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

toolkit = Toolkit(
    ["AMZN", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_maximum_drawdown_duration(period="yearly", within_period=True)
```

Which returns:

|      |   AMZN |   TSLA |   Benchmark |
|:-----|-------:|-------:|------------:|
| 2021 |     30 |     28 |          21 |
| 2022 |    248 |    247 |         195 |
| 2023 |     25 |     73 |          63 |
| 2024 |     23 |     76 |          14 |
| 2025 |     52 |     57 |          34 |

---

## get_maximum_drawdown_recovery_time
Calculate the Maximum Drawdown Recovery Time of an investment portfolio or asset's returns.

The Maximum Drawdown Recovery Time is the number of periods it takes for the cumulative return to reach a new high after the lowest point of the largest drawdown. If the drawdown has not yet been recovered from within the selected period, this returns NaN.

**Also known as:** time to recovery, drawdown recovery.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>within_period (bool, optional):</u> Whether to calculate the recovery time within the specified period
or for the entire period. Thus whether to look at the recovery time within a specific year (if
period = 'yearly') or look at the entirety of all years. Defaults to False.
Note that this requires intraday data when period = 'daily', since a
single day only nests observations when intraday data was fetched.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the recovery time values over time.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
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

toolkit = Toolkit(
    ["AMZN", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_maximum_drawdown_recovery_time(period="yearly", within_period=True)
```

Which returns:

|      |   AMZN |   TSLA |   Benchmark |
|:-----|-------:|-------:|------------:|
| 2021 |    nan |    159 |          12 |
| 2022 |    nan |    nan |         nan |
| 2023 |     46 |    nan |          23 |
| 2024 |     66 |     51 |          32 |
| 2025 |    135 |    114 |          54 |

---

## get_ulcer_index
The Ulcer Index is a financial metric used to assess the risk and volatility of an investment portfolio or asset. Developed by Peter Martin in the 1980s, the Ulcer Index is particularly useful for evaluating the downside risk and drawdowns associated with investments.

The Ulcer Index differs from traditional volatility measures like standard deviation or variance because it focuses on the depth and duration of drawdowns rather than the dispersion of returns.

The formula is as follows:

Ulcer Index = SQRT(SUM[((Pn - Highest High) / Highest High)^2] / n)

**Also known as:** UI, drawdown risk.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly, or yearly).
Defaults to "quarterly" if the Toolkit is initialised with quarterly=True, otherwise "yearly".
- <u>rolling (int &#124; None, optional):</u> The trailing lookback window used as the high-water
mark reference for each day's drawdown. Pass None for an expanding
(since-inception) high-water mark instead -- this is what the "Highest High"
in the formula above literally refers to; a fixed int window is a common,
distinct variant (e.g. a 14-day trailing high) rather than a substitute for
"the entire period". Note that passing `rolling=` the full length of your
return series does NOT give you the since-inception result -- pandas only
starts producing a rolling value once the full window is filled, so it would
silently degenerate to just the final period's drawdown; use `rolling=None`
instead. Defaults to 14.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the UI values over time. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
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

toolkit = Toolkit(
    ["AMZN", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_ulcer_index()
```

Which returns:

|      |   AMZN |   TSLA |   Benchmark |
|:-----|-------:|-------:|------------:|
| 2021 | 0.0427 | 0.0851 |      0.0133 |
| 2022 | 0.1081 | 0.1373 |      0.0488 |
| 2023 | 0.0483 | 0.0839 |      0.0202 |
| 2024 | 0.0395 | 0.0908 |      0.0167 |
| 2025 | 0.0567 | 0.1006 |      0.0276 |

---

## get_garch
Calculates volatility forecasts based on the GARCH model.

GARCH (Generalized autoregressive conditional heteroskedasticity) is stochastic model for time series, which is for instance used to model volatility clusters, stock return and inflation. It is a generalisation of the ARCH models.

**Also known as:** GARCH, volatility clustering, conditional heteroscedasticity.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>time_steps (int, optional):</u> Time steps to calculate GARCH for.
- <u>optimization_t (int, optional):</u> Time steps to optimize GARCH for. It is only used if no weights are given.
- <u>within_period (bool, optional):</u> Whether to calculate GARCH within the specified period or for the entire
period. Thus whether to look at the GARCH within a specific year (if period = 'yearly') or look at the
entirety of all years. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the GARCH values over time. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.DataFrame &#124; pd.Series: GARCH values

**Notes:**

- The method retrieves historical return data based on the specified `period` and calculates GARCH for each
asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of GARCH values using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AMZN", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_garch(period="quarterly")
```

Which returns:

| Date   |   AMZN |   TSLA |   Benchmark |
|:-------|-------:|-------:|------------:|
| 2021Q2 | 0.0125 | 0.0003 |      0.007  |
| 2021Q3 | 0.0186 | 0.0462 |      0.0068 |
| 2021Q4 | 0.0222 | 0.0745 |      0.0065 |
| 2022Q1 | 0.0244 | 0.092  |      0.0063 |
| 2022Q2 | 0.0257 | 0.1029 |      0.0061 |
| 2022Q3 | 0.0264 | 0.1096 |      0.006  |
| 2022Q4 | 0.0269 | 0.1137 |      0.0058 |
| 2023Q1 | 0.0271 | 0.1163 |      0.0056 |
| 2023Q2 | 0.0273 | 0.1179 |      0.0055 |
| 2023Q3 | 0.0274 | 0.1189 |      0.0054 |
| 2023Q4 | 0.0274 | 0.1195 |      0.0053 |
| 2024Q1 | 0.0275 | 0.1199 |      0.0051 |
| 2024Q2 | 0.0275 | 0.1201 |      0.005  |
| 2024Q3 | 0.0275 | 0.1202 |      0.0049 |
| 2024Q4 | 0.0275 | 0.1203 |      0.0049 |
| 2025Q1 | 0.0275 | 0.1204 |      0.0048 |
| 2025Q2 | 0.0275 | 0.1204 |      0.0047 |
| 2025Q3 | 0.0275 | 0.1204 |      0.0046 |
| 2025Q4 | 0.0275 | 0.1204 |      0.0046 |

---

## get_garch_forecast
Calculates sigma_2 forecasts.

GARCH (Generalized autoregressive conditional heteroskedasticity) is stochastic model for time series, which is for instance used to model volatility clusters, stock return and inflation. It is a generalisation of the ARCH models.

The forecasting with GARCH is done with the following formula:

$$
\sigma_{l} ^{2} + (\sigma_{t} ^{2} - \sigma_{l} ^{2}) \cdot (\alpha + \beta) ^{t - 1}
$$

For more information about the method, see the following book:

- Finance Compact Plus Band 1, by Yvonne Seler Zimmerman and Heinz Zimmerman; ISBN: 978-3-907291-31-1

**Also known as:** volatility forecast, predicted volatility.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>time_steps (int, optional):</u> Time steps to calculate GARCH and to forecast sigma_2 values for.
- <u>within_period (bool, optional):</u> Whether to calculate GARCH within each specified period or all
at once. Thus whether to look at the GARCH within each specific year (if period = 'yearly') or
look at the entirety of all years. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the GARCH values over time. Defaults to
False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.DataFrame &#124; pd.Series: sigma_2 forecast values

**Notes:**

- The method retrieves historical return data based on the specified `period` and calculates the sigma_2
forecast for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the forecasted sigma_2 values using
the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AMZN", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_garch_forecast(period="quarterly")
```

Which returns:

|        |   AMZN |   TSLA |   Benchmark |
|:-------|-------:|-------:|------------:|
| 2026Q1 | 0.0275 | 0.1205 |      0.0045 |
| 2026Q2 | 0.0275 | 0.1205 |      0.0044 |
| 2026Q3 | 0.0275 | 0.1205 |      0.0044 |
| 2026Q4 | 0.0275 | 0.1205 |      0.0043 |
| 2027Q1 | 0.0275 | 0.1205 |      0.0043 |
| 2027Q2 | 0.0275 | 0.1205 |      0.0042 |
| 2027Q3 | 0.0275 | 0.1205 |      0.0042 |
| 2027Q4 | 0.0275 | 0.1205 |      0.0042 |
| 2028Q1 | 0.0275 | 0.1205 |      0.0041 |
| 2028Q2 | 0.0275 | 0.1205 |      0.0041 |

---

## get_garch_parameters
Fits a GARCH(1, 1) model to the historical returns and returns the estimated Omega, Alpha and Beta parameters for each asset.

GARCH (Generalized autoregressive conditional heteroskedasticity) is a stochastic model for time series, used to model volatility clustering. A GARCH(1, 1) model expresses the conditional variance sigma_t^2 as:

$$
\sigma_{t} ^{2} = \text{Omega} + \text{Alpha} \cdot u_{t-1} ^{2} + \text{Beta} \cdot \sigma_{t-1} ^{2}
$$

With the constraints Omega, Alpha, Beta > 0 and Alpha + Beta < 1. The parameters are estimated via simulated annealing, maximizing the GARCH log-likelihood function.

Unlike `get_garch` and `get_garch_forecast`, which return a (forecasted) volatility path, this method returns the fitted parameters themselves. This is useful when the parameters are needed directly, for example to seed a separate volatility simulation.

For more information about the method, see the following book:

- Finance Compact Plus Band 1, by Yvonne Seler Zimmerman and Heinz Zimmerman; ISBN: 978-3-907291-31-1

**Also known as:** GARCH weights, GARCH coefficients, conditional variance parameters.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>optimization_t (int, optional):</u> Time steps of the returns series to use for the optimization.
Defaults to the full length of the returns series.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.

**Returns:**

pd.DataFrame: Omega, Alpha and Beta values per asset.

**Notes:**

- The method retrieves historical return data based on the specified `period` and fits a
GARCH(1, 1) model for each asset in the Toolkit instance.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AMZN", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_garch_parameters(period="quarterly")
```

Which returns:

|       |   AMZN |   TSLA |   Benchmark |
|:------|-------:|-------:|------------:|
| Omega | 0.0112 | 0.046  |      0.0003 |
| Alpha | 0      | 0      |      0      |
| Beta  | 0.5947 | 0.6184 |      0.9274 |

---

## get_gjr_garch
Calculates volatility forecasts based on the GJR-GARCH model.

GJR-GARCH extends GARCH with a leverage term that lets negative shocks (bad news) raise volatility by more than positive shocks of the same size, a well documented asymmetry in equity returns that symmetric GARCH cannot capture.

For more information about the method, see the following paper:

- Glosten, L.R., Jagannathan, R., and Runkle, D.E. (1993). "On the Relation between the Expected Value and the Volatility of the Nominal Excess Return on Stocks." The Journal of Finance, 48(5), 1779-1801.

**Also known as:** GJR-GARCH, threshold GARCH, TGARCH.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>time_steps (int, optional):</u> Time steps to calculate GJR-GARCH for.
- <u>optimization_t (int, optional):</u> Time steps to optimize GJR-GARCH for. It is only used if no
weights are given.
- <u>within_period (bool, optional):</u> Whether to calculate GJR-GARCH within the specified period or
for the entire period. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the GJR-GARCH values over time.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.DataFrame &#124; pd.Series: GJR-GARCH values

**Notes:**

- The method retrieves historical return data based on the specified `period` and calculates
GJR-GARCH for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of GJR-GARCH values using the
specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AMZN", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_gjr_garch(period="quarterly")
```

Which returns:

| Date   |   AMZN |   TSLA |   Benchmark |
|:-------|-------:|-------:|------------:|
| 2021Q2 | 0.0125 | 0.0003 |      0.007  |
| 2021Q3 | 0.0208 | 0.0523 |      0.0065 |
| 2021Q4 | 0.0219 | 0.0735 |      0.0057 |
| 2022Q1 | 0.0219 | 0.0821 |      0.0057 |
| 2022Q2 | 0.0219 | 0.0856 |      0.0054 |
| 2022Q3 | 0.0319 | 0.1403 |      0.0088 |
| 2022Q4 | 0.0233 | 0.1093 |      0.0079 |
| 2023Q1 | 0.0275 | 0.2052 |      0.0072 |
| 2023Q2 | 0.0235 | 0.1357 |      0.0066 |
| 2023Q3 | 0.0232 | 0.1074 |      0.0062 |
| 2023Q4 | 0.0221 | 0.0966 |      0.0056 |
| 2024Q1 | 0.0225 | 0.0915 |      0.0057 |
| 2024Q2 | 0.0225 | 0.1218 |      0.0056 |
| 2024Q3 | 0.022  | 0.1018 |      0.0052 |
| 2024Q4 | 0.022  | 0.0936 |      0.0048 |
| 2025Q1 | 0.0224 | 0.0903 |      0.0044 |
| 2025Q2 | 0.0234 | 0.1375 |      0.0044 |
| 2025Q3 | 0.0225 | 0.1081 |      0.0046 |
| 2025Q4 | 0.0219 | 0.0962 |      0.0046 |

---

## get_gjr_garch_forecast
Calculates sigma_2 forecasts based on the GJR-GARCH model.

For more information about the method, see the following paper:

- Glosten, L.R., Jagannathan, R., and Runkle, D.E. (1993). "On the Relation between the Expected Value and the Volatility of the Nominal Excess Return on Stocks." The Journal of Finance, 48(5), 1779-1801.

**Also known as:** volatility forecast, predicted volatility.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>time_steps (int, optional):</u> Time steps to calculate GJR-GARCH and to forecast sigma_2 values for.
- <u>within_period (bool, optional):</u> Whether to calculate GJR-GARCH within each specified period or
all at once. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the GJR-GARCH values over time.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.DataFrame &#124; pd.Series: sigma_2 forecast values

**Notes:**

- The method retrieves historical return data based on the specified `period` and calculates the
sigma_2 forecast for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the forecasted sigma_2 values using
the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AMZN", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_gjr_garch_forecast(period="quarterly")
```

Which returns:

|        |   AMZN |   TSLA |   Benchmark |
|:-------|-------:|-------:|------------:|
| 2026Q1 | 0.0219 | 0.0913 |      0.0042 |
| 2026Q2 | 0.023  | 0.1066 |      0.0043 |
| 2026Q3 | 0.0232 | 0.1158 |      0.0044 |
| 2026Q4 | 0.0232 | 0.1212 |      0.0045 |
| 2027Q1 | 0.0232 | 0.1244 |      0.0046 |
| 2027Q2 | 0.0232 | 0.1264 |      0.0047 |
| 2027Q3 | 0.0232 | 0.1275 |      0.0048 |
| 2027Q4 | 0.0232 | 0.1282 |      0.0048 |
| 2028Q1 | 0.0232 | 0.1286 |      0.0049 |
| 2028Q2 | 0.0232 | 0.1288 |      0.0049 |

---

## get_gjr_garch_parameters
Fits a GJR-GARCH(1, 1, 1) model to the historical returns and returns the estimated Omega, Alpha, Gamma and Beta parameters for each asset.

A positive Gamma indicates the presence of a leverage effect (negative shocks raise volatility by more than positive ones of the same size), which symmetric GARCH cannot represent.

For more information about the method, see the following paper:

- Glosten, L.R., Jagannathan, R., and Runkle, D.E. (1993). "On the Relation between the Expected Value and the Volatility of the Nominal Excess Return on Stocks." The Journal of Finance, 48(5), 1779-1801.

**Also known as:** GJR-GARCH weights, GJR-GARCH coefficients, leverage parameters.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>optimization_t (int, optional):</u> Time steps of the returns series to use for the optimization.
Defaults to the full length of the returns series.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.

**Returns:**

pd.DataFrame: Omega, Alpha, Gamma and Beta values per asset.

**Notes:**

- The method retrieves historical return data based on the specified `period` and fits a
GJR-GARCH(1, 1, 1) model for each asset in the Toolkit instance.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AMZN", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_gjr_garch_parameters(period="quarterly")
```

Which returns:

|       |   AMZN |   TSLA |   Benchmark |
|:------|-------:|-------:|------------:|
| Omega | 0.0189 | 0.0522 |      0.0005 |
| Alpha | 0.0169 | 0      |      0.05   |
| Gamma | 0.0656 | 0.3783 |      0.1    |
| Beta  | 0.1363 | 0.4067 |      0.8    |

---

## get_egarch
Calculates volatility forecasts based on the EGARCH model.

EGARCH models the log of the conditional variance, which avoids having to constrain the parameters to keep the variance positive and, like GJR-GARCH, lets negative and positive shocks of the same size have a different impact on volatility (the leverage effect).

For more information about the method, see the following paper:

- Nelson, D.B. (1991). "Conditional Heteroskedasticity in Asset

**Returns:** A New
Approach." Econometrica, 59(2), 347-370.

Also known as: exponential GARCH, log-GARCH.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>time_steps (int, optional):</u> Time steps to calculate EGARCH for.
- <u>optimization_t (int, optional):</u> Time steps to optimize EGARCH for. It is only used if no
weights are given.
- <u>within_period (bool, optional):</u> Whether to calculate EGARCH within the specified period or
for the entire period. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the EGARCH values over time.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.DataFrame &#124; pd.Series: EGARCH values

**Notes:**

- The method retrieves historical return data based on the specified `period` and calculates
EGARCH for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of EGARCH values using the
specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AMZN", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_egarch(period="quarterly")
```

Which returns:

| Date   |   AMZN |   TSLA |   Benchmark |
|:-------|-------:|-------:|------------:|
| 2021Q2 | 0.0125 | 0.0003 |      0.007  |
| 2021Q3 | 0.0064 | 0.016  |      0.0041 |
| 2021Q4 | 0.011  | 0.0375 |      0.0125 |
| 2022Q1 | 0.0204 | 0.016  |      0.0054 |
| 2022Q2 | 0.043  | 0.1453 |      0.0118 |
| 2022Q3 | 0.0416 | 0.1801 |      0.0109 |
| 2022Q4 | 0.0595 | 0.1849 |      0.0175 |
| 2023Q1 | 0.0793 | 0.1644 |      0.0118 |
| 2023Q2 | 0.0536 | 0.0304 |      0.0082 |
| 2023Q3 | 0.0226 | 0.0257 |      0.0047 |
| 2023Q4 | 0.0474 | 0.1743 |      0.012  |
| 2024Q1 | 0.0284 | 0.3327 |      0.0047 |
| 2024Q2 | 0.0123 | 0.2949 |      0.0016 |
| 2024Q3 | 0.0108 | 0.2774 |      0.0018 |
| 2024Q4 | 0.0207 | 0.1595 |      0.0013 |
| 2025Q1 | 0.0075 | 0.0479 |      0.003  |
| 2025Q2 | 0.0079 | 0.0922 |      0.0084 |
| 2025Q3 | 0.0014 | 0.0997 |      0.0034 |
| 2025Q4 | 0.0031 | 0.0485 |      0.0016 |

---

## get_egarch_forecast
Calculates sigma_2 forecasts based on the EGARCH model.

For more information about the method, see the following paper:

- Nelson, D.B. (1991). "Conditional Heteroskedasticity in Asset

**Returns:** A New
Approach." Econometrica, 59(2), 347-370.

Also known as: volatility forecast, predicted volatility.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>time_steps (int, optional):</u> Time steps to calculate EGARCH and to forecast sigma_2 values for.
- <u>within_period (bool, optional):</u> Whether to calculate EGARCH within each specified period or
all at once. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the EGARCH values over time.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.DataFrame &#124; pd.Series: sigma_2 forecast values

**Notes:**

- The method retrieves historical return data based on the specified `period` and calculates the
sigma_2 forecast for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the forecasted sigma_2 values using
the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AMZN", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_egarch_forecast(period="quarterly")
```

Which returns:

|        |   AMZN |   TSLA |   Benchmark |
|:-------|-------:|-------:|------------:|
| 2026Q1 | 0.0018 | 0.2247 |      0.0035 |
| 2026Q2 | 0.0018 | 0.1615 |      0.006  |
| 2026Q3 | 0.0019 | 0.1483 |      0.0076 |
| 2026Q4 | 0.0019 | 0.1451 |      0.0085 |
| 2027Q1 | 0.002  | 0.1443 |      0.009  |
| 2027Q2 | 0.0021 | 0.1441 |      0.0092 |
| 2027Q3 | 0.0021 | 0.144  |      0.0093 |
| 2027Q4 | 0.0022 | 0.144  |      0.0093 |
| 2028Q1 | 0.0022 | 0.144  |      0.0093 |
| 2028Q2 | 0.0023 | 0.144  |      0.0093 |

---

## get_egarch_parameters
Fits an EGARCH(1, 1) model to the historical returns and returns the estimated Omega, Alpha, Gamma and Beta parameters for each asset.

A negative Gamma indicates the presence of a leverage effect (negative shocks raise volatility by more than positive ones of the same size).

For more information about the method, see the following paper:

- Nelson, D.B. (1991). "Conditional Heteroskedasticity in Asset

**Returns:** A New
Approach." Econometrica, 59(2), 347-370.

Also known as: EGARCH weights, EGARCH coefficients, leverage parameters.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>optimization_t (int, optional):</u> Time steps of the returns series to use for the optimization.
Defaults to the full length of the returns series.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.

**Returns:**

pd.DataFrame: Omega, Alpha, Gamma and Beta values per asset.

**Notes:**

- The method retrieves historical return data based on the specified `period` and fits an
EGARCH(1, 1) model for each asset in the Toolkit instance.
- EGARCH's log-variance parameterization is less constrained than plain GARCH, which makes it
more prone to unstable, boundary-hugging fits on very short return histories (e.g. yearly data).
Prefer `period="quarterly"` or a higher frequency where possible.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AMZN", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_egarch_parameters(period="quarterly")
```

Which returns:

|       |    AMZN |    TSLA |   Benchmark |
|:------|--------:|--------:|------------:|
| Omega |  0.0232 | -1.4376 |     -2.5535 |
| Alpha | -1      | -1      |     -1      |
| Gamma | -0.4903 | -0.414  |     -0.4958 |
| Beta  |  0.999  |  0.2582 |      0.4535 |

---

## get_tail_dependence_coefficient
Calculate the Upper and Lower Tail Dependence Coefficients between `ticker_a` and `ticker_b`.

Correlation only captures the *average* co-movement between two assets -- it says nothing about whether they are more likely to crash together than an equivalent gaussian relationship would imply. The Tail Dependence Coefficient answers that specific question directly: the probability that one asset is in extreme distress, given that the other one already is.

For more information about the method, see the following papers:

- Embrechts, P., McNeil, A., & Straumann, D. (1999). "Correlation: Pitfalls and Alternatives." RISK Magazine, 12, 69-71.
- Poon, S.H., Rockinger, M., & Tawn, J. (2004). "Extreme Value Dependence in Financial Markets: Diagnostics, Models, and Financial Implications." Review of Financial Studies, 17(2), 581-610.

**Also known as:** tail dependence, extremal dependence coefficient.

**Args:**

- <u>ticker_a (str):</u> The first asset.
- <u>ticker_b (str):</u> The second asset.
- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily", since a dependence estimate needs far more observations than a
lower frequency provides -- at "yearly" a decade of history is only ten
observations.
- <u>column (str, optional):</u> The historical data column to use. Defaults to "Return", since
tail dependence between return series is the standard risk management application.
- <u>q (float, optional):</u> The threshold quantile used for the "empirical" method, in (0.5, 1).
Defaults to 0.95.
- <u>method (str, optional):</u> The estimation method, one of "empirical", "gaussian" or
"student-t". Defaults to "empirical".
- <u>dof (float, optional):</u> The degrees of freedom of the Student-T copula, only used when
`method="student-t"`. Defaults to 4.0.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.

**Returns:**

pd.Series: The Lower and Upper Tail Dependence Coefficients, the linear (Pearson)
correlation between the two assets, and the number of observations used.

**Notes:**

- The method retrieves historical data based on the specified `period` for the two given
assets and estimates the tail dependence coefficient between them.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AMZN", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_tail_dependence_coefficient("AAPL", "MSFT", period="weekly")
```

Which returns:

| 0   |
|-----|

---

## get_copula_parameters
Calibrate a bivariate copula between `ticker_a` and `ticker_b`, via maximum likelihood.

When `ticker_a`/`ticker_b` are not given, every unique pair among the Toolkit's tickers is calibrated instead.

A copula separates the dependence structure between two assets from their individual (marginal) return distributions (Sklar's theorem), letting the two be modeled independently. Five families are supported, each capturing a different shape of dependence:

- "gaussian": zero tail dependence -- crashes and rallies are no more likely to happen together than the correlation alone implies. Included mainly as a baseline, since real asset returns typically show more joint tail risk than this.
- "student-t": symmetric, nonzero tail dependence in both tails.
- "clayton": nonzero *lower* tail dependence only -- assets crash together more than they rally together. The most common choice for equity return pairs.
- "gumbel": nonzero *upper* tail dependence only -- assets rally together more than they crash together.
- "frank": zero tail dependence in both tails, but (unlike gaussian) can represent negative dependence and is symmetric around independence.

See `get_best_fitting_copula` to compare all five by AIC on the same pair of assets, and see `get_copula_simulation` to draw joint scenarios from the fitted copula.

For more information about the method, see:

- Sklar, A. (1959). Publications de l'Institut de Statistique de l'Universite de Paris, 8, 229-231.
- McNeil, A.J., Frey, R., & Embrechts, P. (2015). "Quantitative Risk Management: Concepts, Techniques and Tools." Princeton University Press.
- Demarta, S., & McNeil, A.J. (2005). "The T Copula and Related Copulas." International Statistical Review, 73(1), 111-129.

**Also known as:** copula calibration, copula fit, dependence modeling.

**Args:**

- <u>ticker_a (str, optional):</u> The first asset. Defaults to None, meaning every unique pair of
tickers in the Toolkit instance is calibrated (requires `ticker_b` to also be None).
- <u>ticker_b (str, optional):</u> The second asset. Defaults to None, see `ticker_a`.
- <u>copula (str, optional):</u> The copula family to fit, one of "gaussian",
"student-t", "clayton", "gumbel" or "frank". Defaults to "gaussian".
- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily", since a dependence estimate needs far more observations than a
lower frequency provides -- at "yearly" a decade of history is only ten
observations.
- <u>column (str, optional):</u> The historical data column to use. Defaults to "Return".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.

**Raises:**

ValueError: If `copula` is not one of "gaussian", "student-t", "clayton", "gumbel" or "frank",
if only one of `ticker_a`/`ticker_b` is given, if fewer than 2 tickers are available to pair
up when neither is given, or if fewer than 10 paired, non-missing observations are available.

**Returns:**

pd.Series &#124; pd.DataFrame: The fitted copula parameter(s), the Lower and Upper Tail
Dependence implied by them, the Log-Likelihood, the AIC and the number of observations used
-- a Series for a single given pair, or a DataFrame indexed by every (Ticker A, Ticker B)
pair when neither ticker is given.

**Notes:**

- The method retrieves historical data based on the specified `period` and calibrates the
requested copula between the given pair, or every pair, of tickers.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AMZN", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_copula_parameters("AAPL", "MSFT", copula="clayton", period="weekly")
```

Which returns:

| 0   |
|-----|

---

## get_copula_simulation
Calibrate a bivariate copula (see `get_copula_parameters`) between `ticker_a` and `ticker_b`, and simulate joint scenarios from it.

When `ticker_a`/`ticker_b` are not given, every unique pair among the Toolkit's tickers is calibrated and simulated instead, as columns grouped under a top-level (Ticker A, Ticker B) column per pair.

This is what a copula-based portfolio Monte Carlo simulation needs: draws that preserve the calibrated dependence structure -- including tail dependence, for the "student-t", "clayton" and "gumbel" families -- rather than the (typically understated) joint crash risk a plain multivariate gaussian simulation would produce.

**Also known as:** copula Monte Carlo, dependence simulation, scenario generation.

**Args:**

- <u>ticker_a (str, optional):</u> The first asset. Defaults to None, meaning every unique pair of
tickers in the Toolkit instance is used (requires `ticker_b` to also be None).
- <u>ticker_b (str, optional):</u> The second asset. Defaults to None, see `ticker_a`.
- <u>copula (str, optional):</u> The copula family to fit and simulate from, one of "gaussian",
"student-t", "clayton", "gumbel" or "frank". Defaults to "gaussian".
- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily", since a dependence estimate needs far more observations than a
lower frequency provides -- at "yearly" a decade of history is only ten
observations.
- <u>column (str, optional):</u> The historical data column to use. Defaults to "Return".
- <u>n_simulations (int, optional):</u> The number of joint draws to simulate. Defaults to 10,000.
- <u>random_state (int, optional):</u> The seed for the random number generator. Defaults to 42.
- <u>empirical_margins (bool, optional):</u> Whether to map the simulated pseudo-observations back
to realistic returns via each asset's own empirical (historical) quantile function.
Defaults to True. When False, the raw pseudo-observations (each in (0, 1)) are returned
instead.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.

**Raises:**

ValueError: If `copula` is not one of "gaussian", "student-t", "clayton", "gumbel" or "frank",
if only one of `ticker_a`/`ticker_b` is given, if fewer than 2 tickers are available to pair
up when neither is given, or if fewer than 10 paired, non-missing observations are available.

**Returns:**

pd.DataFrame: `n_simulations` simulated joint draws, one column per asset (or "U"/"V" when
`empirical_margins=False`) for a single given pair, or with columns grouped by
(Ticker A, Ticker B) pair when neither ticker is given.

**Notes:**

- The method retrieves historical data based on the specified `period`, calibrates the
requested copula, and simulates from it, for the given pair or every pair of tickers.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AMZN", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_copula_simulation(
    "AAPL", "MSFT", copula="clayton", period="weekly", n_simulations=5000
).describe()
```

Which returns:

|        |   0 |
|:-------|----:|
| count  |   0 |
| unique |   0 |
| top    | nan |
| freq   | nan |

---

## get_best_fitting_copula
Calibrate all five supported copula families (see `get_copula_parameters`) between `ticker_a` and `ticker_b`, and compare them by AIC (Akaike Information Criterion) -- the lower the AIC, the better the fit relative to its number of parameters, so the top row is the best-fitting family.

When `ticker_a`/`ticker_b` are not given, every unique pair among the Toolkit's tickers is compared instead.

**Also known as:** copula selection, copula comparison.

**Args:**

- <u>ticker_a (str, optional):</u> The first asset. Defaults to None, meaning every unique pair of
tickers in the Toolkit instance is compared (requires `ticker_b` to also be None).
- <u>ticker_b (str, optional):</u> The second asset. Defaults to None, see `ticker_a`.
- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily", since a dependence estimate needs far more observations than a
lower frequency provides -- at "yearly" a decade of history is only ten
observations.
- <u>column (str, optional):</u> The historical data column to use. Defaults to "Return".
- <u>show_full_results (bool, optional):</u> Only relevant when neither ticker is given. When False
(the default), returns a square ticker-by-ticker grid of just the winning copula family
per pair. When True, returns one row per pair instead, with the winning family's fitted
parameter(s), Lower and Upper Tail Dependence, Log-Likelihood, AIC and the number of
observations used. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.

**Raises:**

ValueError: If only one of `ticker_a`/`ticker_b` is given, or if fewer than 2 tickers are
available to pair up when neither is given.

**Returns:**

pd.DataFrame: For a single given pair, one row per copula family, sorted by AIC (best fit
first), with each family's fitted parameter(s), Lower and Upper Tail Dependence,
Log-Likelihood, AIC and the number of observations used, indexed by "Copula". When neither
ticker is given, a square ticker-by-ticker grid of the winning copula family per pair (or,
with `show_full_results=True`, one row per pair instead, indexed by (Ticker A, Ticker B),
with a "Best Copula" column and that family's fitted stats).

**Notes:**

- The method retrieves historical data based on the specified `period` and calibrates every
supported copula family for the given pair, or every pair, of tickers.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AMZN", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_best_fitting_copula("AAPL", "MSFT", period="weekly")
```

Which returns:

| 0   |
|-----|

---

## get_covar
Calculate the (Delta-)CoVaR of `ticker` conditional on `conditioning_ticker` being in its own distress state.

Ordinary Value at Risk treats each asset in isolation, which misses systemic risk -- the fact that one asset's distress can spill over and worsen another's risk. CoVaR directly measures that spillover: it is the VaR of `ticker`, conditional on `conditioning_ticker` itself being at its own `alpha`-VaR, estimated via a linear Quantile Regression of `ticker`'s returns on `conditioning_ticker`'s returns at quantile `alpha`. The Delta-CoVaR isolates the marginal, distress-specific contribution by subtracting the same construction evaluated in the "normal" (median) state instead.

For more information about the method, see the following paper:

- Adrian, T., & Brunnermeier, M.K. (2016). "CoVaR." American Economic Review, 106(7), 1705-1741.

**Also known as:** Conditional Value at Risk (systemic risk sense), Delta-CoVaR.

**Args:**

- <u>ticker (str):</u> The asset whose conditional VaR is being measured.
- <u>conditioning_ticker (str):</u> The asset (or e.g. a benchmark/index) whose distress
`ticker` is conditioned on.
- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily", since a dependence estimate needs far more observations than a
lower frequency provides -- at "yearly" a decade of history is only ten
observations.
- <u>column (str, optional):</u> The historical data column to use. Defaults to "Return".
- <u>alpha (float, optional):</u> The confidence level for both the tail quantile regression and
the VaR of `conditioning_ticker` (e.g., 0.05 for 95% confidence). Defaults to 0.05.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.

**Returns:**

pd.Series: The CoVaR, the Delta-CoVaR, the tail (alpha-quantile) Quantile Regression
slope and intercept, and the number of observations used.

**Notes:**

- The method retrieves historical data based on the specified `period` for the two given
assets and estimates the CoVaR of `ticker` conditional on `conditioning_ticker`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AMZN", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_covar("AAPL", "MSFT", period="weekly")
```

Which returns:

| 0   |
|-----|

---

## get_marginal_value_at_risk
Calculate the Marginal Value at Risk (Marginal VaR) of each asset in a portfolio.

Ordinary VaR (see `get_value_at_risk`) treats each asset in isolation. Marginal VaR instead measures how much the *portfolio's* VaR would change for an infinitesimal increase in a given asset's portfolio weight - i.e. the sensitivity of portfolio risk to each holding, not the risk of the holding on its own:

- Portfolio Return = SUM(weight_i * Return_i)
- Beta_i = Cov(Return_i, Portfolio Return) / Var(Portfolio Return)
- Marginal VaR_i = Beta_i * Portfolio VaR

An asset with Beta_i > 1 contributes disproportionately to portfolio risk, while Beta_i < 1 (and especially Beta_i < 0) indicates a diversifying holding.

For more information about the method, see the following sources:

- Garman, M.B. (1997). "Taking VaR to Pieces." Risk, 10(10), 70-71.
- Litterman, R. (1996). "Hot Spots and Hedges." Goldman Sachs Risk Management Series.
- Jorion, P. (2006). "Value at Risk: The New Benchmark for Managing Financial Risk." 3rd ed., McGraw-Hill, Chapter 7.

**Also known as:** Marginal VaR, MVaR.

**Args:**

- <u>weights (dict[str, float] &#124; None, optional):</u> Portfolio weights
keyed by ticker. Normalized internally to sum to 1. Defaults to None, which
uses equal weights across every ticker in the Toolkit instance (excluding
the "Portfolio" and "Benchmark" pseudo-tickers, if present).
- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily", since a whole-series estimate needs far more observations than a single
quarter or year holds.
- <u>column (str, optional):</u> The historical data column to use. Defaults to "Return".
- <u>alpha (float, optional):</u> The confidence level (e.g., 0.05 for 95% confidence).
Defaults to 0.05.
- <u>distribution (str, optional):</u> The distribution to use for the underlying portfolio
VaR calculation (historic, gaussian, cornish-fisher or studentt). Defaults to
"historic".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None.

**Returns:**

pd.Series: The Marginal VaR of each asset.

**Notes:**

- The method retrieves historical return data based on the specified `period` for
every ticker in the Toolkit instance and computes each asset's Marginal VaR against
the weighted portfolio built from `weights`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AMZN", "TSLA", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_marginal_value_at_risk(weights={"AMZN": 0.5, "TSLA": 0.3, "MSFT": 0.2})
```

Which returns:

|      |   Marginal VaR |
|:-----|---------------:|
| AMZN |        -0.0298 |
| TSLA |        -0.05   |
| MSFT |        -0.0182 |

---

## get_component_value_at_risk
Calculate the Component Value at Risk (Component VaR) of each asset in a portfolio.

Component VaR allocates total portfolio VaR across its constituent assets, such that the allocations sum exactly back to the portfolio VaR - an "Euler" (or "fully consistent") risk decomposition:

$$
\text{Component VaR}_{i} = \text{weight}_{i} \cdot \text{Marginal VaR}_{i} (\text{see}\; \text{get\_marginal\_value\_at\_risk})
$$

$$
\operatorname{SUM}(\text{Component VaR}_{i}) = \text{Portfolio VaR}
$$

Where Marginal VaR measures each asset's risk *sensitivity*, Component VaR measures its actual *contribution* in the same units as portfolio VaR, making it directly usable to identify which holdings account for the largest share of portfolio risk.

For more information about the method, see the following sources:

- Garman, M.B. (1997). "Taking VaR to Pieces." Risk, 10(10), 70-71.
- Litterman, R. (1996). "Hot Spots and Hedges." Goldman Sachs Risk Management Series.
- Jorion, P. (2006). "Value at Risk: The New Benchmark for Managing Financial Risk." 3rd ed., McGraw-Hill, Chapter 7.

**Also known as:** Component VaR, risk contribution.

**Args:**

- <u>weights (dict[str, float] &#124; None, optional):</u> Portfolio weights
keyed by ticker. Normalized internally to sum to 1. Defaults to None, which
uses equal weights across every ticker in the Toolkit instance (excluding
the "Portfolio" and "Benchmark" pseudo-tickers, if present).
- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily", since a whole-series estimate needs far more observations than a single
quarter or year holds.
- <u>column (str, optional):</u> The historical data column to use. Defaults to "Return".
- <u>alpha (float, optional):</u> The confidence level (e.g., 0.05 for 95% confidence).
Defaults to 0.05.
- <u>distribution (str, optional):</u> The distribution to use for the underlying portfolio
VaR calculation (historic, gaussian, cornish-fisher or studentt). Defaults to
"historic".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None.

**Returns:**

pd.Series: The Component VaR of each asset, plus a "Portfolio" entry equal to
their sum (the total portfolio VaR), for validation.

**Notes:**

- The method retrieves historical return data based on the specified `period` for
every ticker in the Toolkit instance and computes each asset's Component VaR against
the weighted portfolio built from `weights`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AMZN", "TSLA", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_component_value_at_risk(weights={"AMZN": 0.5, "TSLA": 0.3, "MSFT": 0.2})
```

Which returns:

|           |   Component VaR |
|:----------|----------------:|
| AMZN      |         -0.0149 |
| TSLA      |         -0.015  |
| MSFT      |         -0.0036 |
| Portfolio |         -0.0335 |

---

## get_var_backtest
Backtest a Value at Risk model against realized returns.

A Value at Risk estimate is only useful if it is actually well-calibrated against reality. This method builds a rolling, out-of-sample VaR path (each VaR estimate uses only the `window_size` returns preceding it, never the return it is compared against) and tests it with Kupiec's Proportion of Failures test (is the overall breach rate consistent with `alpha`?) and/or Christoffersen's independence test (are breaches spread out over time, or do they cluster together?).

For more information about the methods, see the following papers:

- Kupiec, P.H. (1995). "Techniques for Verifying the Accuracy of Risk Measurement Models." The Journal of Derivatives, 3(2), 73-84.
- Christoffersen, P.F. (1998). "Evaluating Interval Forecasts." International Economic Review, 39(4), 841-862.

**Also known as:** VaR validation, VaR backtest, POF test.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, quarterly, or yearly).
Defaults to "daily", since `window_size` is expressed in return observations of this frequency
(252 only means "about one year" when `period` is daily).
- <u>distribution (str, optional):</u> The distribution to use for the rolling VaR estimates, one of
"historic", "gaussian", "studentt" or "evt". Defaults to "historic".
- <u>alpha (float, optional):</u> The confidence level for the VaR estimates (e.g., 0.05 for 95%
confidence). Defaults to 0.05.
- <u>window_size (int, optional):</u> The rolling window size (in number of return observations) used to
estimate each VaR value. Defaults to 252 (approximately one trading year of daily returns).
- <u>test (str, optional):</u> Which test(s) to run, one of "kupiec", "christoffersen" or "both". Defaults
to "both".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.

**Returns:**

pd.DataFrame: The requested test statistic(s) and their p-value(s) per asset.

**Notes:**

- The rolling VaR path is calculated over the full return history, not the `within_period` slices
used elsewhere in this module, since a meaningful rolling window generally needs more history than
a single sub-period provides.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AMZN", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_var_backtest(window_size=252)
```

Which returns:

|                          |   AMZN |   TSLA |   Benchmark |
|:-------------------------|-------:|-------:|------------:|
| Kupiec Statistic         | 2.3413 | 0.1736 |      0.312  |
| P-Value                  | 0.126  | 0.677  |      0.5765 |
| Christoffersen Statistic | 0.4588 | 5.9293 |      4.7906 |
| P-Value                  | 0.4982 | 0.0149 |      0.0286 |

---

## get_acerbi_szekely_test
Backtest a Conditional Value at Risk (Expected Shortfall) model against realized returns, via the Acerbi-Szekely (2014) Z2 statistic.

`get_var_backtest` above only backtests the VaR estimate itself -- it checks how often (and how independently) the VaR threshold is breached, but says nothing about the *severity* of the losses on those breach days, which is exactly the extra information a CVaR (Expected Shortfall) estimate is supposed to add over VaR. This method builds a rolling, out-of-sample CVaR (and VaR) path and compares the actual loss on each breach day to the CVaR that was supposed to describe the average loss on such days.

For more information about the method, see the following paper:

- Acerbi, C., & Szekely, B. (2014). "Back-Testing Expected Shortfall." RISK Magazine, 27(11), 76-81.

**Also known as:** Acerbi-Szekely test, ES backtest, Z2 test.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, quarterly, or yearly).
Defaults to "daily", since `window_size` is expressed in return observations of this frequency.
- <u>distribution (str, optional):</u> The distribution to use for the rolling VaR/CVaR estimates,
one of "historic", "gaussian", "studentt" or "evt". Defaults to "historic".
- <u>alpha (float, optional):</u> The confidence level for the VaR/CVaR estimates (e.g., 0.05 for 95%
confidence). Defaults to 0.05.
- <u>window_size (int, optional):</u> The rolling window size (in number of return observations) used
to estimate each VaR/CVaR value. Defaults to 252 (approximately one trading year of daily
returns).
- <u>n_bootstrap (int, optional):</u> The number of bootstrap resamples used to estimate the Standard
Error of Z2. Defaults to 1000.
- <u>random_state (int, optional):</u> The seed for the bootstrap random number generator. Defaults to
42.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.

**Returns:**

pd.DataFrame: The Z2 statistic, its bootstrap Standard Error, its p-value, and the number of
breaches observed, per asset.

**Notes:**

- The rolling VaR/CVaR path is calculated over the full return history, not the `within_period`
slices used elsewhere in this module, since a meaningful rolling window generally needs more
history than a single sub-period provides.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AMZN", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_acerbi_szekely_test(window_size=100)
```

Which returns:

|                          |    AMZN |    TSLA |   Benchmark |
|:-------------------------|--------:|--------:|------------:|
| Acerbi-Szekely Statistic |  0.2146 |  0.2444 |      0.3931 |
| Standard Error           |  0.1615 |  0.1543 |      0.1554 |
| P-Value                  |  0.1838 |  0.1133 |      0.0114 |
| Breaches                 | 65      | 70      |     78      |

---

## get_skewness
Calculate the Skewness of an investment portfolio or asset's returns.

Skewness is a statistical measure used in finance to assess the asymmetry in the distribution of returns for an investment portfolio or asset over a defined period. It offers valuable insights into the shape of the return distribution, indicating whether returns are skewed towards the positive or negative side of the mean. Skewness is a crucial tool for investors and analysts seeking to understand the potential risk and return characteristics of an investment, aiding in the assessment of the distribution's tails and potential outliers. It provides a means to gauge the level of skew in returns, enabling more informed investment decisions and risk management strategies.

**Also known as:** return distribution asymmetry, tail skew.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>within_period (bool, optional):</u> Whether to calculate the Skewness within the specified period or for the
entire period. Thus whether to look at the Skewness within a specific year (if period = 'yearly') or look
at the entirety of all years. Defaults to False.
Note that this requires intraday data when period = 'daily', since a
single day only nests observations when intraday data was fetched.
- <u>rolling (int, optional):</u> The rolling window size to use for the calculation. If set, Skewness is
calculated over a rolling window of this many periods across the full return history instead of
per `period`. Defaults to None.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Skewness values over time.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.Series: Skewness values with time as the index.

**Notes:**

- The method retrieves historical return data based on the specified `period` and calculates Skew for each
asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of Skewness values using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["MSFT", "AAPL", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_skewness(period="yearly", within_period=True)
```

Which returns:

|      |    MSFT |    AAPL |    TSLA |   Benchmark |
|:-----|--------:|--------:|--------:|------------:|
| 2021 | -0.0175 | -0.0735 |  0.669  |     -0.3324 |
| 2022 |  0.1474 |  0.3167 | -0.026  |      0.0454 |
| 2023 |  0.3774 | -0.0662 |  0.0021 |     -0.0206 |
| 2024 | -0.8882 |  0.4447 |  0.8937 |     -0.5242 |
| 2025 |  1.3142 |  1.1299 |  0.4045 |      1.5069 |

---

## get_kurtosis
Calculate the Kurtosis of an investment portfolio or asset's returns.

Kurtosis is a statistical measure used in finance to evaluate the shape of the probability distribution of returns for an investment portfolio or asset over a defined time period. It assesses the "tailedness" of the return distribution, indicating whether returns have fatter or thinner tails compared to a normal distribution. Kurtosis plays a critical role in risk assessment by revealing the potential presence of extreme outliers or the likelihood of heavy tails in the return data. This information aids investors and analysts in understanding the degree of risk associated with an investment and assists in making more informed decisions regarding risk tolerance. In essence, kurtosis serves as a valuable tool for comprehending the distribution characteristics of returns, offering insights into the potential for rare but significant events in the financial markets.

**Also known as:** tail heaviness, fat tails, leptokurtosis.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>within_period (bool, optional):</u> Whether to calculate the Kurtosis within the specified period or for the
entire period. Thus whether to look at the Kurtosis within a specific year (if period = 'yearly') or look
at the entirety of all years. Defaults to False.
Note that this requires intraday data when period = 'daily', since a
single day only nests observations when intraday data was fetched.
- <u>fisher (bool, optional):</u> Whether to use Fisher's definition of kurtosis (kurtosis = 0.0
for a normal distribution). Defaults to False.
- <u>rolling (int, optional):</u> The rolling window size to use for the calculation. If set, Kurtosis is
calculated over a rolling window of this many periods across the full return history instead of
per `period`. Defaults to None.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Kurtosis values over time.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.Series: Kurtosis values with time as the index.

**Notes:**

- The method retrieves historical return data based on the specified `period` and calculates Kurtosis for each
asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of Kurtosis values using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["MSFT", "AAPL", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_kurtosis(period="yearly", within_period=True)
```

Which returns:

|      |    MSFT |    AAPL |   TSLA |   Benchmark |
|:-----|--------:|--------:|-------:|------------:|
| 2021 |  3.3906 |  3.4146 | 7.488  |      3.7279 |
| 2022 |  3.8936 |  4.054  | 3.386  |      3.3635 |
| 2023 |  4.4619 |  4.4804 | 4.3336 |      2.843  |
| 2024 |  5.1741 |  6.6121 | 7.5225 |      4.7961 |
| 2025 | 13.1336 | 17.0667 | 7.7019 |     26.576  |

---

## get_hill_estimator
Calculate the Hill Estimator of the tail index of returns, per asset.

Unlike the (finite-sample) Skewness and Kurtosis above, the Hill Estimator is a semi-parametric estimate of how heavy the tail of the return distribution actually is, under the assumption that the tail follows a Pareto-type power law. Smaller values of the tail index indicate a heavier tail (more extreme outliers are likely) -- as a rule of thumb, a tail index below 4 implies the Kurtosis is theoretically infinite, and below 2 implies the Variance itself is theoretically infinite.

For more information about the method, see the following paper:

- Hill, B.M. (1975). "A Simple General Approach to Inference About the Tail of a Distribution." The Annals of Statistics, 3(5), 1163-1174.

**Also known as:** Hill tail index estimator, Hill's estimator.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>within_period (bool, optional):</u> Whether to calculate the estimator within the specified period
or for the entire period. Defaults to False.
Note that this requires intraday data when period = 'daily', since a
single day only nests observations when intraday data was fetched.
- <u>k (int &#124; float, optional):</u> The number of upper order statistics to use. If a float in (0, 1)
it is interpreted as the fraction of the strictly positive observations to use. Defaults to
0.1 (the top 10%).
- <u>tail (str, optional):</u> Which tail to estimate, one of "left" (the loss tail) or "right" (the
gain tail). Defaults to "left".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.

**Returns:**

pd.DataFrame: The Hill tail index, the Hill shape parameter, its Standard Error and the
number of order statistics used, per asset.

**Notes:**

- The method retrieves historical return data based on the specified `period` and calculates the
Hill Estimator for each asset in the Toolkit instance.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AMZN", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_hill_estimator(period="weekly", within_period=False)
```

Which returns:

|                       |    AMZN |    TSLA |   Benchmark |
|:----------------------|--------:|--------:|------------:|
| Hill Tail Index       |  3.2418 |  9.5123 |      2.7487 |
| Hill Shape (xi)       |  0.3085 |  0.1051 |      0.3638 |
| Standard Error        |  0.9358 |  2.746  |      0.8288 |
| Observations Used (k) | 12      | 12      |     11      |

---

## get_variance
Calculate the Variance of an investment portfolio or asset's returns for a given period based on the daily historical returns.

Variance measures the spread or dispersion of returns around the mean. A higher Variance indicates more variability in the returns, while a lower Variance suggests that the returns are closer to the mean.

The daily Variance is scaled to the given period by multiplying it with the number of trading days within that period (e.g. 252 / 52 for weekly).

**Also known as:** dispersion, spread.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (weekly, monthly, quarterly, or yearly). Defaults
to "quarterly" if the Toolkit is initialised with quarterly=True, otherwise "yearly".
- <u>rolling (int, optional):</u> The rolling window size to use for the calculation. If set,
Variance is calculated over a rolling window of this many periods (e.g. period='monthly'
and rolling=6 gives the rolling 6-month Variance) instead of one value per `period`.
Defaults to None.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Variance values over time. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
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

toolkit = Toolkit(
    ["AMZN", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_variance(period="yearly")
```

Which returns:

| Date   |   AMZN |   TSLA |   Benchmark |
|:-------|-------:|-------:|------------:|
| 2021   | 0.0578 | 0.3    |      0.0167 |
| 2022   | 0.2508 | 0.4446 |      0.0588 |
| 2023   | 0.109  | 0.2922 |      0.0171 |
| 2024   | 0.0789 | 0.4032 |      0.0158 |
| 2025   | 0.1184 | 0.4031 |      0.038  |

---

## get_volatility
Calculate the Volatility of an investment portfolio or asset's returns for a given period based on the daily historical prices.

Volatility measures the amount of dispersion or variability in returns. It is the square root of the Variance. A higher Volatility indicates greater variability, while a lower Volatility suggests that returns are closer to the mean.

By default this is the close-to-close Volatility, i.e. the standard deviation of the daily returns. The `method` parameter selects one of four range-based estimators instead, each of which uses more of the day's price action than just the close and is therefore more statistically efficient (i.e. needs fewer observations to reach the same precision), at the cost of additional assumptions about how prices move:

- `"parkinson"` - uses the daily trading range (High vs Low) rather than the close-to-close return, assuming prices follow a continuous geometric Brownian motion with no drift and no overnight jumps.
- `"garman_klass"` - extends Parkinson by also incorporating the Open and Close, which allows it to account for the opening jump and makes it more efficient still (assuming, as Parkinson does, no drift and no overnight jumps beyond the modeled open).
- `"rogers_satchell"` - drift-independent, meaning it remains unbiased even when the underlying asset has a non-zero expected return over the period, at the cost of still assuming no overnight jumps.
- `"yang_zhang"` - a weighted combination of the overnight (close-to-open) Variance, the open-to-close Variance and the Rogers-Satchell Variance. It is both drift-independent and accounts for overnight jumps, which makes it the most statistically efficient of the range-based estimators implemented here.

In every case the daily Volatility is scaled to the given period by multiplying the underlying Variance with the number of trading days within that period (e.g. 252 / 52 for weekly).

**Also known as:** standard deviation of returns. The range-based estimators are also known as Parkinson's range-based or high-low Volatility, Garman-Klass range-based Volatility, Rogers-Satchell drift-independent Volatility and Yang-Zhang drift-independent overnight-aware Volatility.

For more information about the range-based estimators, see the following papers:

- Parkinson, M. (1980). "The Extreme Value Method for Estimating the Variance of the Rate of Return." Journal of Business, 53(1), 61-65.
- Garman, M.B., & Klass, M.J. (1980). "On the Estimation of Security Price Volatilities from Historical Data." Journal of Business, 53(1), 67-78.
- Rogers, L.C.G., & Satchell, S.E. (1991). "Estimating Variance from High, Low and Close Prices." Annals of Applied Probability, 1(4), 504-512.
- Yang, D., & Zhang, Q. (2000). "Drift-Independent Volatility Estimation Based on High, Low, Open, and Close Prices." Journal of Business, 73(3), 477-491.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (weekly, monthly, quarterly, or yearly). Defaults
to "quarterly" if the Toolkit is initialised with quarterly=True, otherwise "yearly".
- <u>rolling (int, optional):</u> The rolling window size to use for the calculation. If set,
Volatility is calculated over a rolling window of this many periods (e.g. period='monthly'
and rolling=6 gives the rolling 6-month Volatility) instead of one value per `period`.
Only available for method="close_to_close". Defaults to None.
- <u>method (str, optional):</u> Which Volatility estimator to use, one of "close_to_close",
"parkinson", "garman_klass", "rogers_satchell" or "yang_zhang", as described above.
Defaults to "close_to_close".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Volatility values over time.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.Series: Volatility values with time as the index.

**Notes:**

- The method retrieves the daily historical price data and calculates the Volatility for
the specified `period` for each asset in the Toolkit instance. The close-to-close estimator
only needs the daily returns, Parkinson needs the High and Low, and the remaining
estimators need the Open, High, Low and Close.
- If `growth` is set to True, the method calculates the growth of Volatility values using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AMZN", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_volatility(period="yearly")
```

Which returns:

| Date   |   AMZN |   TSLA |   Benchmark |
|:-------|-------:|-------:|------------:|
| 2021   | 0.2404 | 0.5477 |      0.1293 |
| 2022   | 0.5008 | 0.6668 |      0.2425 |
| 2023   | 0.3302 | 0.5406 |      0.1307 |
| 2024   | 0.2809 | 0.635  |      0.1257 |
| 2025   | 0.3442 | 0.6349 |      0.1948 |

And, using the daily trading range instead of only the closes:

```python
toolkit.risk.get_volatility(period="yearly", method="parkinson")
```



| Date   |   AMZN |   TSLA |   Benchmark |
|:-------|-------:|-------:|------------:|
| 2021   | 0.2089 | 0.4563 |      0.1073 |
| 2022   | 0.3717 | 0.5547 |      0.1916 |
| 2023   | 0.2617 | 0.438  |      0.1101 |
| 2024   | 0.219  | 0.4357 |      0.0989 |
| 2025   | 0.267  | 0.5062 |      0.152  |

---

## get_har_rv_forecast
Calculate the Corsi (2009) Heterogeneous Autoregressive Realized Volatility (HAR-RV) forecast of future daily Realized Variance, per asset.

Volatility clustering happens across multiple, overlapping time horizons at once. HAR-RV captures this cheaply -- without the numerical optimization a GARCH-family fit requires (see `get_garch`) -- by regressing future daily Realized Variance on trailing daily, weekly and monthly average Realized Variance components. The daily Realized Variance itself can be constructed in several ways via `estimator`: the simplest is the squared daily return, while the OHLC range-based estimators (see `get_volatility`, which exposes the same estimators via its own `method` parameter) use the daily (pre-period-aggregation) term behind each of those estimators instead, which is more statistically efficient since it uses the daily trading range rather than only the close-to-close move.

For more information about the method, see the following paper:

- Corsi, F. (2009). "A Simple Approximate Long-Memory Model of Realized Volatility." Journal of Financial Econometrics, 7(2), 174-196.

**Also known as:** HAR-RV model, Corsi's HAR model, Heterogeneous Autoregressive model.

**Args:**

- <u>estimator (str, optional):</u> How to construct the daily Realized Variance input, one of
"squared_return", "parkinson", "garman_klass" or "rogers_satchell". Defaults to
"squared_return".
- <u>weekly_window (int, optional):</u> The trailing window (in trading days) for the weekly RV
component. Defaults to 5.
- <u>monthly_window (int, optional):</u> The trailing window (in trading days) for the monthly RV
component. Defaults to 22.
- <u>horizon (int, optional):</u> The number of days ahead to forecast. Defaults to 1.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the HAR-RV forecast values over
time. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.Series: The HAR-RV forecast of Realized Variance with time as the index.

**Notes:**

- The method retrieves daily historical price data and calculates the HAR-RV forecast for each
asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the HAR-RV forecast values
using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AMZN", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_har_rv_forecast(estimator="squared_return").tail()
```

Which returns:

| Date       |     AMZN |     TSLA |   Benchmark |
|:-----------|---------:|---------:|------------:|
| 2025-12-24 |   0.0003 |   0.0011 |      0.0001 |
| 2025-12-26 |   0.0003 |   0.0011 |      0.0001 |
| 2025-12-29 |   0.0003 |   0.0011 |      0.0001 |
| 2025-12-30 |   0.0003 |   0.0011 |      0.0001 |
| 2025-12-31 | nan      | nan      |    nan      |

The last row is NaN since there is no `2022-12-31` return yet to forecast against.

---

## get_amihud_illiquidity
Calculate the Amihud (2002) Illiquidity ratio, per asset.

The Amihud ratio measures the average price impact of trading -- how much the price moves per dollar of trading volume. A high value means that even a small amount of trading moves the price a lot (the asset is illiquid), while a low value means the asset can absorb a large amount of trading with little price impact (the asset is liquid).

For more information about the method, see the following paper:

- Amihud, Y. (2002). "Illiquidity and Stock

**Returns:** Cross-Section and
Time-Series Effects." Journal of Financial Markets, 5(1), 31-56.

Also known as: Amihud illiquidity ratio, ILLIQ, price impact ratio.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>within_period (bool, optional):</u> Whether to calculate the ratio within the specified period or
for the entire period. Defaults to False. Note that this requires intraday data when period = 'daily', since a
single day only nests observations when intraday data was fetched.
- <u>scale (float, optional):</u> A multiplier applied to the resulting ratio purely for readability.
Defaults to 1,000,000.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Amihud Illiquidity values over
time. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.Series: Amihud Illiquidity values with time as the index.

**Notes:**

- The method retrieves historical return, Close price and Volume data based on the specified
`period` and calculates the Amihud Illiquidity ratio for each asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the Amihud Illiquidity values
using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AMZN", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_amihud_illiquidity(period="quarterly", scale=1e12)
```

Which returns:

|           |      0 |
|:----------|-------:|
| AMZN      | 0.2447 |
| TSLA      | 0.1704 |
| Benchmark | 0.0306 |

Note that a large `scale` is used here since these are liquid, large-cap
stocks with very high dollar trading volume relative to their typical daily
price move -- the default `scale` of 1,000,000 (as used in Amihud's original
1980s/1990s-era paper) would round these to 0.0 at the default precision.

---

## get_roll_spread
Calculate the Roll (1984) implied bid-ask spread, per asset.

Roll's model shows that, under a stylized microstructure model in which the true (efficient) price follows a random walk and observed trade prices randomly bounce between the bid and the ask, the effective spread can be backed out purely from the serial covariance of consecutive price changes, without needing any actual quote data. If the estimated covariance is zero or positive, no valid estimate can be backed out and NaN is returned instead.

For more information about the method, see the following paper:

- Roll, R. (1984). "A Simple Implicit Measure of the Effective Bid-Ask Spread in an Efficient Market." The Journal of Finance, 39(4), 1127-1139.

**Also known as:** Roll's implied spread, Roll measure.

**Args:**

- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>within_period (bool, optional):</u> Whether to calculate the spread within the specified period or
for the entire period. Defaults to False. Note that this requires intraday data when period = 'daily', since a
single day only nests observations when intraday data was fetched.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.

**Returns:**

pd.DataFrame: The Roll Spread (in price units), the Roll Spread as a percentage of the mean
price, the underlying lag-1 autocovariance, and whether that autocovariance was negative (i.e.
whether a valid estimate could be backed out), per asset.

**Notes:**

- The method retrieves historical Close price data based on the specified `period` and calculates
the Roll Spread for each asset in the Toolkit instance.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AMZN", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_roll_spread()
```

Which returns:

|                 |      AMZN |     TSLA |   Benchmark |
|:----------------|----------:|---------:|------------:|
| Roll Spread     |  0.917232 |  3.64757 |    1.97906  |
| Roll Spread (%) |  0.561329 |  1.37352 |    0.408282 |
| Autocovariance  | -0.210329 | -3.32619 |   -0.979167 |
| Valid Estimate  |  1        |  1       |    1        |

---

## get_excess_volatility
Calculate the Excess Volatility of an investment portfolio or asset's returns for a given period based on the daily historical returns.

Excess Volatility is the Volatility of the Excess Return, i.e. the daily return minus the risk free rate, scaled to the given period in the same way as the Volatility.

**Also known as:** standard deviation of excess returns.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (weekly, monthly, quarterly, or yearly). Defaults
to "quarterly" if the Toolkit is initialised with quarterly=True, otherwise "yearly".
- <u>rolling (int, optional):</u> The rolling window size to use for the calculation. If set,
Excess Volatility is calculated over a rolling window of this many periods (e.g.
period='monthly' and rolling=6 gives the rolling 6-month Excess Volatility) instead of
one value per `period`. Defaults to None.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Excess Volatility values
over time. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
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

toolkit = Toolkit(
    ["AMZN", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_excess_volatility(period="yearly")
```

Which returns:

| Date   |   AMZN |   TSLA |   Benchmark |
|:-------|-------:|-------:|------------:|
| 2021   | 0.2404 | 0.5477 |      0.1293 |
| 2022   | 0.5008 | 0.6668 |      0.2425 |
| 2023   | 0.3302 | 0.5406 |      0.1307 |
| 2024   | 0.2809 | 0.635  |      0.1257 |
| 2025   | 0.3442 | 0.6349 |      0.1948 |

---

## get_downside_deviation
Calculate the Downside Deviation of an investment portfolio or asset's returns.

The Downside Deviation, also known as semi-deviation, is the standard deviation of only the returns that fall below a minimum acceptable return (MAR), isolating the volatility of negative outcomes from the volatility of the overall return distribution. It underlies risk-adjusted return measures such as the Sortino Ratio and the Omega Ratio.

**Also known as:** semi-deviation, downside risk, downside volatility.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>minimum_acceptable_return (float, optional):</u> The minimum acceptable return (MAR) used as the
threshold below which returns are considered downside. Defaults to 0.0.
- <u>within_period (bool, optional):</u> Whether to calculate the Downside Deviation within the specified
period or for the entire period. Thus whether to look at the Downside Deviation within a specific
year (if period = 'yearly') or look at the entirety of all years. Defaults to False.
Note that this requires intraday data when period = 'daily', since a
single day only nests observations when intraday data was fetched.
- <u>rolling (int, optional):</u> The rolling window size to use for the calculation. If set, the Downside
Deviation is calculated over a rolling window of this many periods across the full return history
instead of per `period`. Defaults to None.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Downside Deviation values over
time. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
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

toolkit = Toolkit(
    ["AMZN", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_downside_deviation(period="yearly", within_period=True)
```

Which returns:

|      |   AMZN |   TSLA |   Benchmark |
|:-----|-------:|-------:|------------:|
| 2021 | 0.0108 | 0.0221 |      0.0054 |
| 2022 | 0.0229 | 0.0318 |      0.011  |
| 2023 | 0.013  | 0.022  |      0.0053 |
| 2024 | 0.0117 | 0.0243 |      0.0055 |
| 2025 | 0.0146 | 0.0268 |      0.0081 |

---

## get_mean_absolute_deviation
Calculate the Mean Absolute Deviation (MAD) of an investment portfolio or asset's returns for a given period based on the daily historical returns.

MAD measures the average absolute distance of each return from the mean return. Unlike Variance and Volatility, it does not square the deviations, making it less sensitive to outliers.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (weekly, monthly, quarterly, or yearly). Defaults
to "quarterly" if the Toolkit is initialised with quarterly=True, otherwise "yearly".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the MAD values over time. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
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

toolkit = Toolkit(
    ["AMZN", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_mean_absolute_deviation(period="yearly")
```

Which returns:

| Date   |   AMZN |   TSLA |   Benchmark |
|:-------|-------:|-------:|------------:|
| 2021   | 0.0114 | 0.0246 |      0.0061 |
| 2022   | 0.0235 | 0.032  |      0.0119 |
| 2023   | 0.0156 | 0.0255 |      0.0064 |
| 2024   | 0.0132 | 0.0286 |      0.0058 |
| 2025   | 0.015  | 0.0292 |      0.0074 |

---

## get_coefficient_of_variation
Calculate the Coefficient of Variation (CV) of an investment portfolio or asset's returns for a given period based on the daily historical returns.

The Coefficient of Variation is the ratio of the standard deviation to the mean of returns, which normalizes dispersion relative to the average return. This makes it useful for comparing the relative volatility of assets with different average returns, which a raw standard deviation cannot do.

**Also known as:** relative standard deviation.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (weekly, monthly, quarterly, or yearly). Defaults
to "quarterly" if the Toolkit is initialised with quarterly=True, otherwise "yearly".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the CV values over time. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
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

toolkit = Toolkit(
    ["AMZN", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_coefficient_of_variation(period="yearly")
```

Which returns:

| Date   |     AMZN |     TSLA |   Benchmark |
|:-------|---------:|---------:|------------:|
| 2021   |  51.4326 |  16.7257 |      7.4324 |
| 2022   | -14.1417 | -12.7544 |    -22.3928 |
| 2023   |   8.0356 |  10.0506 |      8.5443 |
| 2024   |  10.9398 |  14.7623 |      8.6564 |
| 2025   |  49.9543 |  32.8037 |     16.8499 |

---

## get_ewma_volatility
Calculate the exponentially weighted moving average (EWMA) Volatility of an investment portfolio or asset's daily returns, following the RiskMetrics methodology.

Unlike a fixed-window rolling Volatility, EWMA Volatility weights recent observations more heavily than older ones, so it reacts faster to changes in the underlying volatility regime. It is a simpler, more interpretable alternative to a full GARCH fit.

The formula is as follows:

$$
\text{EWMA Variance} (t) = \lambda \cdot \text{EWMA Variance} (t-1) + (1 - \lambda) \cdot \operatorname{Return}(t-1) ^{2}
$$

**Also known as:** RiskMetrics volatility, exponentially weighted volatility.

**Args:**

- <u>lambda_ (float, optional):</u> The decay factor. Higher values weight the past
more heavily (slower to react), lower values weight recent returns more
heavily (faster to react). RiskMetrics uses 0.94 for daily data. Defaults to 0.94.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to 4.
- <u>growth (bool, optional):</u> Whether to calculate the growth of the EWMA Volatility values over
time. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
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

toolkit = Toolkit(
    ["AMZN", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_ewma_volatility()
```

Which returns:

| Date       |   AMZN |   TSLA |   Benchmark |
|:-----------|-------:|-------:|------------:|
| 2025-12-17 | 0.018  | 0.0276 |      0.007  |
| 2025-12-18 | 0.0175 | 0.029  |      0.0073 |
| 2025-12-19 | 0.018  | 0.0294 |      0.0073 |
| 2025-12-22 | 0.0175 | 0.0285 |      0.0075 |
| 2025-12-23 | 0.017  | 0.0279 |      0.0074 |
| 2025-12-24 | 0.017  | 0.0271 |      0.0073 |
| 2025-12-26 | 0.0164 | 0.0263 |      0.0071 |
| 2025-12-29 | 0.0159 | 0.026  |      0.0069 |
| 2025-12-30 | 0.0155 | 0.0264 |      0.0067 |
| 2025-12-31 | 0.015  | 0.0258 |      0.0065 |

---

## get_autocorrelation
Calculate the Autocorrelation Function (ACF) of each asset's daily returns for a range of lags.

The ACF measures the correlation between a return series and a lagged version of itself. A significant ACF at a given lag indicates that returns are not fully independent over time, which is relevant for assessing return predictability and volatility clustering (as opposed to a trading-signal use case, which is why this lives in the Risk module rather than Technicals).

**Args:**

- <u>lags (int, optional):</u> The number of lags to calculate the ACF for. Defaults to 10.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to 4.

**Returns:**

pd.DataFrame: The ACF value for each lag (rows) and each asset (columns).

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AMZN", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_autocorrelation()
```

Which returns:

|    |    AMZN |    TSLA |   Benchmark |
|---:|--------:|--------:|------------:|
|  1 | -0.0125 | -0.026  |     -0.031  |
|  2 | -0.0064 |  0.0128 |     -0.0069 |
|  3 | -0.0114 | -0.0109 |     -0.0626 |
|  4 |  0.0112 |  0.0189 |     -0.0344 |
|  5 | -0.0143 | -0.0213 |     -0.0075 |
|  6 |  0.0047 |  0.045  |     -0.0104 |
|  7 | -0.0523 |  0.0309 |     -0.0109 |
|  8 | -0.0307 |  0.0198 |     -0.0063 |
|  9 | -0.0102 |  0.063  |      0.0399 |
| 10 | -0.0084 | -0.0499 |     -0.0111 |

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
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to 4.

**Returns:**

pd.Series: The estimated Hurst Exponent for each asset.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AMZN", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_hurst_exponent()
```

Which returns:

|           |      0 |
|:----------|-------:|
| AMZN      | 0.4596 |
| TSLA      | 0.52   |
| Benchmark | 0.4362 |

---

