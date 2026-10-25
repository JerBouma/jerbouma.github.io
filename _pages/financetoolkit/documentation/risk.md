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
    - /projects/financetoolkit/risk-notebook
sidebar:
    nav: "financetoolkit-docs-risk"
---

The Risk module calculates important risk metrics such as Value at Risk (VaR), Conditional Value at Risk (CVaR), Maximum Drawdown, Correlations, GARCH, EWMA and more.

Use it in Claude, ChatGPT or another AI assistant through the [Finance Toolkit MCP](/projects/financetoolkit/mcp), or install the Python package:

```python
pip install financetoolkit -U
```

{% include algolia.html %}

{% include financetoolkit-getting-started/risk.md %}

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

metrics = toolkit.risk.collect_all_metrics().xs("AAPL", level=1, axis=1)

metrics[["Value at Risk", "Maximum Drawdown", "Ulcer Index", "Skewness", "Kurtosis"]]
```

Which returns:

|      |   Value at Risk |   Maximum Drawdown |   Ulcer Index |   Skewness |   Kurtosis |
|:-----|----------------:|-------------------:|--------------:|-----------:|-----------:|
| 2021 |         -0.0256 |            -0.1861 |        0.0366 |    -0.0748 |     3.4006 |
| 2022 |         -0.0373 |            -0.3032 |        0.0664 |     0.3168 |     4.0553 |
| 2023 |         -0.0175 |            -0.1498 |        0.0324 |    -0.0686 |     4.4756 |
| 2024 |         -0.0217 |            -0.1539 |        0.0343 |     0.4447 |     6.6112 |
| 2025 |         -0.0321 |            -0.3107 |        0.0502 |     1.1306 |    17.0892 |

---

## get_value_at_risk
Calculate the Value at Risk (VaR) of an investment portfolio or asset's returns.

Value at Risk (VaR) is a risk management metric that quantifies the maximum potential loss an investment portfolio or asset may experience over a specified time horizon and confidence level. It provides insights into the downside risk associated with an investment and helps investors make informed decisions about risk tolerance.

The VaR is calculated as the quantile of the return distribution, representing the loss threshold that is only exceeded with tail probability alpha (e.g., in 5% of the periods for alpha=0.05, the 95% confidence level).

Value at Risk is a quantile: it says how bad a period gets at the chosen confidence level, not how bad the periods beyond it are, so two assets with the same VaR can have very different tails (see the Conditional Value at Risk for that). Historical VaR depends heavily on the window: one calm year gives a much smaller figure than a window that includes a crisis, so compare assets over the same period and confidence level. Scaling a daily VaR to a longer horizon with the square root of time assumes independent returns, which tends to understate risk when volatility clusters.

The formula is as follows (with the default distribution="historic" and alpha=0.05):

$$
\text{VaR} = \operatorname{Quantile}(\text{Returns},\; \alpha)
$$

The quantile interpolates linearly between the two nearest returns and the VaR is reported as a return (negative for a loss). With `rolling`, the same quantile is taken over each trailing window of `rolling` returns. The other distributions replace the empirical quantile with:

$$
\text{Gaussian VaR} = \text{Mean} + z \cdot \text{Std}
$$

$$
\text{Cornish-Fisher VaR} = \text{Mean} + z_{cf} \cdot \text{Std}
$$

$$
z_{cf} = z + (z ^{2} - 1) \cdot S / 6 + (z ^{3} - 3 \cdot z) \cdot K / 24 - (2 \cdot z ^{3} - 5 \cdot z) \cdot S ^{2} / 36
$$

$$
\text{Student-T VaR} = \text{Location} + \text{Scale} \cdot t_{v} ^{-1} (\alpha)
$$

$$
\text{EVT VaR} = - (u + (\text{Scale\_GPD} / \xi) \cdot ((\alpha / p) ^{- \xi} - 1))
$$

Where z is the standard normal quantile at alpha, Std the sample standard deviation (ddof=1), S the sample skewness and K the sample excess kurtosis. The Student-T degrees of freedom v, Location and Scale are fitted by maximum likelihood. For "evt", u is the loss at `threshold_percentile`, xi and Scale_GPD the shape and scale of the Generalized Pareto Distribution fitted to the losses above it and p the fraction of losses above it.

**Also known as:** VaR, maximum expected loss, portfolio loss risk.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>alpha (float, optional):</u> The tail probability for the VaR calculation (e.g., 0.05 for the 95%
confidence level). Defaults to 0.05.
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
- <u>distribution (str):</u> The distribution to use for the VaR calculations (historic, gaussian,
cornish-fisher, studentt or evt). Defaults to "historic". The parametric distributions use the
sample standard deviation; "cornish-fisher" adjusts the gaussian quantile for the skewness and
excess kurtosis of the returns (see `var_model.get_var_cornish_fisher`) and "studentt" uses the
quantile of a Student-T distribution fitted by maximum likelihood.
- <u>threshold_percentile (float, optional):</u> Only used when `distribution` is "evt". The percentile
of losses above which the Generalized Pareto Distribution is fitted; `alpha` can be at most
1 - `threshold_percentile`, and a larger `alpha` gives an empty result (with a logged error).
Defaults to 0.95.

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
    ["BTCUSD", "ETHUSD", "^GSPC"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_value_at_risk(period="yearly", within_period=True)
```

Which returns:

|      |   BTCUSD |   ETHUSD |   ^GSPC |   Benchmark |
|:-----|---------:|---------:|--------:|------------:|
| 2021 |  -0.0626 |  -0.0838 | -0.0087 |     -0.0089 |
| 2022 |  -0.0574 |  -0.0742 | -0.02   |     -0.0203 |
| 2023 |  -0.0313 |  -0.0374 | -0.0116 |     -0.0117 |
| 2024 |  -0.0407 |  -0.0533 | -0.0094 |     -0.0096 |
| 2025 |  -0.0358 |  -0.0569 | -0.0113 |     -0.0113 |

---

## get_conditional_value_at_risk
Calculate the Conditional Value at Risk (CVaR) of an investment portfolio or asset's returns.

Conditional Value at Risk (CVaR) is a risk management metric that quantifies the loss in the worst % of cases of an investment portfolio or asset may experience over a specified time horizon and confidence level. It provides insights into the downside risk associated with an investment and helps investors make informed decisions about risk tolerance.

The CVaR is calculated as the expected loss given that the loss threshold (VaR) with a given confidence level (e.g., 5% for alpha=0.05) is exceeded.

The Conditional Value at Risk (expected shortfall) is the measure banks report for market risk under the Basel framework, at 97.5% rather than 95% confidence, because unlike VaR it accounts for the size of the losses in the tail and never penalises diversification (it is subadditive). With daily data the estimate rests on few observations (one year at 95% leaves about 12 days in the tail), so a single extreme day can move it a lot; a longer window or a parametric distribution gives a steadier figure.

The formula is as follows (with the default distribution="historic" and alpha=0.05):

$$
\text{CVaR} = \operatorname{Mean}(\text{Returns} | \text{Returns} \leq \text{VaR})
$$

$$
\text{VaR} = \operatorname{Quantile}(\text{Returns},\; \alpha)
$$

The quantile interpolates linearly and the CVaR is reported as a return (negative for a loss). The other distributions use closed forms, with Std the sample standard deviation (ddof=1) and z_alpha the standard normal quantile at alpha:

$$
\text{Gaussian CVaR} = \text{Mean} - \text{Std} \cdot \operatorname{pdf}(z_{\alpha}) / \alpha
$$

$$
\text{Student-T CVaR} = \text{Location} - \text{Scale} \cdot (v + t ^{2}) / (v - 1) \cdot \text{pdf}_{v}(t) / \alpha,\;\; \text{with}\; t = t_{v} ^{-1} (1 - \alpha)
$$

$$
\text{Laplace CVaR} = \text{Mean} - b \cdot (1 - \ln(2 \cdot \alpha)),\;\; \text{with}\; b = \text{Std} / \sqrt{2}
$$

$$
\text{Logistic CVaR} = \text{Mean} - s \cdot \ln((1 - \alpha) ^{1 - 1 / \alpha} / \alpha),\;\; \text{with}\; s = \text{Std} \cdot \sqrt{3} / \pi
$$

$$
\text{Cornish-Fisher CVaR} = \text{Mean of} (\text{Mean} + z_{cf}(p) \cdot \text{Std}) \text{over}\; 1,\;\; \text{000 evenly spaced p in (0, alpha)}
$$

$$
\text{EVT CVaR} = - (\text{VaR\_loss} + \text{Scale\_GPD} - \xi \cdot u) / (1 - \xi)
$$

Where the Student-T v, Location and Scale are fitted by maximum likelihood (NaN for v <= 1), z_cf is the Cornish-Fisher quantile of `get_value_at_risk`, and u, xi, Scale_GPD and VaR_loss are the loss threshold, the fitted Generalized Pareto shape and scale and the EVT VaR as a positive loss (NaN for xi >= 1).

**Also known as:** CVaR, expected shortfall, ES, tail risk.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>alpha (float, optional):</u> The tail probability for the CVaR calculation (e.g., 0.05 for the 95%
confidence level). Defaults to 0.05.
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
of losses above which the Generalized Pareto Distribution is fitted; `alpha` can be at most
1 - `threshold_percentile`, and a larger `alpha` gives an empty result (with a logged error).
Defaults to 0.95.

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
    ["XOM", "CVX", "COP"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_conditional_value_at_risk()
```

Which returns:

|           |   Value |
|:----------|--------:|
| XOM       | -0.0359 |
| CVX       | -0.0383 |
| COP       | -0.0532 |
| Benchmark | -0.0275 |

---

## get_entropic_value_at_risk
Calculate the Entropic Value at Risk (EVaR) of an investment portfolio or asset's returns.

Entropic Value at Risk (EVaR) is a risk management metric that quantifies upper bound for the value at risk (VaR) and the conditional value at risk (CVaR) over a specified time horizon and confidence level. EVaR is obtained from the Chernoff inequality. It provides insights into the downside risk associated with an investment and helps investors make informed decisions about risk tolerance.

The EVaR is calculated under the assumption that returns are normally distributed, for which the Chernoff bound has a closed form.

The formula is as follows (with the default alpha=0.05):

$$
\text{EVaR} = \text{Mean} - \text{Std} \cdot \sqrt{- 2 \cdot \ln(\alpha)}
$$

Where alpha is the tail probability (0.05 for the 95% confidence level) and Std the sample standard deviation (ddof=1). It is an upper bound of the gaussian VaR and CVaR at the same confidence level. Since it only uses the mean and the standard deviation of the returns, it does not reflect their skewness or fat tails, and at high confidence levels it can be less severe than the historical CVaR of an asset with heavy tails.

For more information about the method, see the following paper:

- Ahmadi-Javid, A. (2012). "Entropic Value-at-Risk: A New Coherent Risk Measure." Journal of Optimization Theory and Applications, 155(3), 1105-1123.

**Also known as:** EVaR.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>alpha (float, optional):</u> The tail probability for the EVaR calculation (e.g., 0.05 for the 95%
confidence level). Defaults to 0.05.
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
    ["CLUSD", "NGUSD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_entropic_value_at_risk(period="yearly", within_period=True)
```

Which returns:

|      |   CLUSD |   NGUSD |   Benchmark |
|:-----|--------:|--------:|------------:|
| 2021 | -0.0496 | -0.0837 |     -0.0185 |
| 2022 | -0.0718 | -0.1505 |     -0.0373 |
| 2023 | -0.0509 | -0.1079 |     -0.0187 |
| 2024 | -0.0436 | -0.1183 |     -0.018  |
| 2025 | -0.0474 | -0.1001 |     -0.0279 |

---

## get_conditional_drawdown_at_risk
Calculate the Conditional Drawdown at Risk (CDaR) of an investment portfolio or asset's returns.

Conditional Drawdown at Risk (CDaR) extends the concept of Value at Risk and Conditional Value at Risk to the drawdown series instead of the return series. It is calculated as the average of the worst drawdowns that exceed the Drawdown at Risk (DaR), i.e. the alpha-quantile of the drawdown distribution, giving insight into the depth of the most severe drawdowns an investment portfolio or asset could experience.

The formula is as follows (with the default alpha=0.05):

$$
\operatorname{Wealth}(t) = \text{Π} (1 + \operatorname{Return}(s)) \text{for}\; s \leq t
$$

$$
\operatorname{Drawdown}(t) = \operatorname{Wealth}(t) / \max(1,\; \max(\operatorname{Wealth}(s) \text{for}\; s \leq t)) - 1
$$

$$
\text{DaR} = \operatorname{Quantile}(\text{Drawdown},\; \alpha)
$$

$$
\text{CDaR} = \operatorname{Mean}(\text{Drawdown} | \text{Drawdown} \leq \text{DaR})
$$

Every period counts towards the drawdown distribution, including those at a high (a drawdown of 0), the quantile interpolates linearly, and Wealth starts at 1, so a decline from the start of the window counts.

**Also known as:** CDaR.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>alpha (float, optional):</u> The tail probability for the CDaR calculation (e.g., 0.05 for the 95%
confidence level). Defaults to 0.05.
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
    ["^STOXX50E", "^N225", "^GSPC"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_conditional_drawdown_at_risk(period="yearly", within_period=True)
```

Which returns:

|      |   ^STOXX50E |   ^N225 |   ^GSPC |   Benchmark |
|:-----|------------:|--------:|--------:|------------:|
| 2021 |     -0.0628 | -0.1001 | -0.042  |     -0.0413 |
| 2022 |     -0.24   | -0.1312 | -0.2422 |     -0.2344 |
| 2023 |     -0.0912 | -0.0813 | -0.0834 |     -0.0807 |
| 2024 |     -0.0818 | -0.1612 | -0.0574 |     -0.0565 |
| 2025 |     -0.123  | -0.1603 | -0.1469 |     -0.1457 |

---

## get_tail_ratio
Calculate the Tail Ratio of an investment portfolio or asset's returns.

The Tail Ratio compares the size of the right (gain) tail to the left (loss) tail of the return distribution. A Tail Ratio above 1 indicates that best-case gains outsize worst-case losses.

The formula is as follows (with the default alpha=0.05):

$$
\text{Tail Ratio} = | \operatorname{Quantile}(\text{Returns},\; 1 - \alpha) | / | \operatorname{Quantile}(\text{Returns},\; \alpha) |
$$

The quantiles interpolate linearly, and a left-tail quantile of 0 gives NaN.

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
    ["QQQ", "TLT", "GLD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_tail_ratio(period="yearly", within_period=True)
```

Which returns:

|      |    QQQ |    TLT |    GLD |   Benchmark |
|:-----|-------:|-------:|-------:|------------:|
| 2021 | 0.9646 | 1.0836 | 0.7734 |      1.1304 |
| 2022 | 0.9109 | 0.8904 | 1.0385 |      0.9524 |
| 2023 | 1.2227 | 1.1695 | 1.1281 |      1.0466 |
| 2024 | 0.9029 | 0.8128 | 1.072  |      0.9091 |
| 2025 | 0.8622 | 1.104  | 1.2495 |      0.93   |

---

## get_maximum_drawdown
Calculate the Maximum Drawdown (MDD) of an investment portfolio or asset's returns.

Maximum Drawdown (MDD) is a risk management metric that quantifies the largest historical loss of an investment portfolio or asset experienced over a specified time horizon. It provides insights into the downside risk associated with an investment and helps investors make informed decisions about risk tolerance.

The Maximum Drawdown is a single-path statistic: it depends entirely on the window chosen, so a figure over a window that includes a market crash and one over a window that starts after it are not comparable. It says how deep the worst fall was, not how long it lasted, which is why it is usually read together with the drawdown duration and recovery time (see `get_maximum_drawdown_duration` and `get_maximum_drawdown_recovery_time`), and it underlies return-to-risk ratios such as the Calmar ratio.

The formula is as follows:

$$
\operatorname{Wealth}(t) = \text{Π} (1 + \operatorname{Return}(s)) \text{for}\; s \leq t
$$

$$
\operatorname{Drawdown}(t) = \operatorname{Wealth}(t) / \max(1,\; \max(\operatorname{Wealth}(s) \text{for}\; s \leq t)) - 1
$$

$$
\text{Maximum Drawdown} = \min(\operatorname{Drawdown}(t))
$$

Wealth starts at 1, so a decline from the start of the window counts as well, and the result is a negative decimal (0 when the value never fell below a previous high).

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
    ["META", "NFLX", "AMZN"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_maximum_drawdown(period="yearly", within_period=True)
```

Which returns:

|      |    META |    NFLX |    AMZN |   Benchmark |
|:-----|--------:|--------:|--------:|------------:|
| 2021 | -0.1972 | -0.173  | -0.1456 |     -0.051  |
| 2022 | -0.7372 | -0.7237 | -0.5197 |     -0.245  |
| 2023 | -0.1298 | -0.2752 | -0.1965 |     -0.0999 |
| 2024 | -0.1842 | -0.1345 | -0.1949 |     -0.0841 |
| 2025 | -0.3416 | -0.3073 | -0.3088 |     -0.1877 |

---

## get_maximum_drawdown_duration
Calculate the Maximum Drawdown Duration of an investment portfolio or asset's returns.

The Maximum Drawdown Duration is the number of periods between the peak and the lowest point of the largest drawdown, giving insight into how long the worst loss of value took to unfold.

The formula is as follows:

$$
\text{Maximum Drawdown Duration} = t(\text{trough}) - t(\text{peak})
$$

Where t(trough) is the period of the lowest Drawdown (see `get_maximum_drawdown`) and t(peak) the last period at or before it in which Wealth stood at the high that drawdown is measured from. When that high is the starting value of 1, t(peak) is the period before the first return.

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
    ["^GSPC", "^HSI", "^FTSE"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_maximum_drawdown_duration(period="yearly", within_period=True)
```

Which returns:

|      |   ^GSPC |   ^HSI |   ^FTSE |   Benchmark |
|:-----|--------:|-------:|--------:|------------:|
| 2021 |      22 |    217 |      15 |          22 |
| 2022 |     201 |    200 |     173 |         201 |
| 2023 |      64 |    225 |      98 |          64 |
| 2024 |      14 |     35 |      58 |          14 |
| 2025 |      34 |     13 |      27 |          34 |

---

## get_maximum_drawdown_recovery_time
Calculate the Maximum Drawdown Recovery Time of an investment portfolio or asset's returns.

The Maximum Drawdown Recovery Time is the number of periods it takes for the cumulative return to climb back to its previous peak after the lowest point of the largest drawdown. If the drawdown has not yet been recovered from within the selected period, this returns NaN.

The formula is as follows:

$$
\text{Maximum Drawdown Recovery Time} = t(\text{recovery}) - t(\text{trough})
$$

Where t(trough) is the period of the lowest Drawdown (see `get_maximum_drawdown`) and t(recovery) the first period at or after it in which Wealth is back at or above the high that drawdown is measured from.

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
    ["TLT", "IEF", "HYG"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_maximum_drawdown_recovery_time(period="yearly", within_period=True)
```

Which returns:

|      |   TLT |   IEF |   HYG |   Benchmark |
|:-----|------:|------:|------:|------------:|
| 2021 |   nan |   nan |    19 |          12 |
| 2022 |   nan |   nan |   nan |         nan |
| 2023 |   nan |   nan |    98 |          23 |
| 2024 |   nan |   nan |    14 |          32 |
| 2025 |   100 |    49 |    23 |          54 |

---

## get_ulcer_index
The Ulcer Index is a financial metric used to assess the risk and volatility of an investment portfolio or asset. Developed by Peter Martin in the 1980s, the Ulcer Index is particularly useful for evaluating the downside risk and drawdowns associated with investments.

The Ulcer Index differs from traditional volatility measures like standard deviation or variance because it focuses on the depth and duration of drawdowns rather than the dispersion of returns.

The formula is as follows (with the default rolling=14):

$$
\text{Ulcer Index} = \sqrt{\text{Σ} ((\operatorname{Wealth}(t) - \text{Highest High} (t)) / \text{Highest High} (t)) ^{2} / n}
$$

Where Wealth(t) compounds the daily returns within each period from a starting value of 1, Highest High(t) is the highest Wealth over the trailing 14 observations (the starting value of 1 included while fewer are available) and n is the number of daily returns in the period.

Martin measures every drawdown from the highest value so far (`rolling=None`); the default trailing 14-period high is the variant StockCharts popularised. While fewer than `rolling` observations are available, the high is taken over the observations so far, so periods shorter than the window still have a value. The result is a decimal (0.05 is a root mean squared drawdown of 5%), where Martin quotes percentages.

The Ulcer Index punishes both the depth and the length of drawdowns, so an asset that falls 10% and stays there for months scores worse than one that drops 10% and recovers within a week, which a volatility figure would not show. It is the risk measure behind the Martin ratio (excess return divided by the Ulcer Index) and is read best relative to peers over the same window, since the default 14-period lookback gives lower values than a since-inception high-water mark.

**Also known as:** UI, drawdown risk.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly, or yearly).
Defaults to "quarterly" if the Toolkit is initialised with quarterly=True, otherwise "yearly".
- <u>rolling (int &#124; None, optional):</u> The trailing lookback window used as the high-water
mark reference for each day's drawdown. Pass None for an expanding
(since-inception) high-water mark instead -- Martin's "Highest High"; a fixed
int window is the common trailing-high variant (e.g. a 14-day trailing high).
Defaults to 14.
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
- If `growth` is set to True, the method calculates the growth of UI values using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["BA", "AIR.PA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_ulcer_index()
```

Which returns:

|      |     BA |   AIR.PA |   Benchmark |
|:-----|-------:|---------:|------------:|
| 2021 | 0.0555 |   0.0408 |      0.0129 |
| 2022 | 0.0901 |   0.0606 |      0.0477 |
| 2023 | 0.0433 |   0.0288 |      0.0194 |
| 2024 | 0.0686 |   0.0423 |      0.0162 |
| 2025 | 0.0635 |   0.0499 |      0.0267 |

---

## get_garch
Calculates the conditional variance (sigma_t^2) of the returns with a GARCH(1, 1) model fitted to them. Take the square root for the conditional volatility, and see `get_garch_forecast` for the variance forecast beyond the last observation.

GARCH (Generalized autoregressive conditional heteroskedasticity) is stochastic model for time series, which is for instance used to model volatility clusters, stock return and inflation. It is a generalisation of the ARCH models.

The formula is as follows:

$$
\sigma_{t} ^{2} = \text{Omega} + \text{Alpha} \cdot r_{t-1} ^{2} + \text{Beta} \cdot \sigma_{t-1} ^{2}
$$

$$
\sigma_{1} ^{2} = \text{Omega} + (\text{Alpha} + \text{Beta}) \cdot \text{Backcast}
$$

Where r_t are the returns (not demeaned) and the Backcast is an exponentially weighted average (decay 0.94) of the first 75 squared returns. Omega, Alpha and Beta maximize the Gaussian log-likelihood, i.e. minimize Σ (ln sigma_t^2 + r_t^2 / sigma_t^2), under Omega, Alpha, Beta > 0 and Alpha + Beta < 1 (see `get_garch_parameters`).

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
- Every asset is fitted on its own available returns, so an asset with a shorter history (or a gap)
does not shorten the sample of the others; dates without a return for an asset are NaN.
- If `growth` is set to True, the method calculates the growth of GARCH values using the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["BTCUSD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_garch().tail(5)
```

Which returns:

| Date       |   BTCUSD |   Benchmark |
|:-----------|---------:|------------:|
| 2025-12-27 |   0.0004 |           0 |
| 2025-12-28 |   0.0004 |           0 |
| 2025-12-29 |   0.0004 |           0 |
| 2025-12-30 |   0.0004 |           0 |
| 2025-12-31 |   0.0004 |           0 |

---

## get_garch_forecast
Calculates sigma_2 forecasts.

GARCH (Generalized autoregressive conditional heteroskedasticity) is stochastic model for time series, which is for instance used to model volatility clusters, stock return and inflation. It is a generalisation of the ARCH models.

The formula is as follows:

$$
\sigma_{n + h} ^{2} = \sigma_{L} ^{2} + (\sigma_{n + 1} ^{2} - \sigma_{L} ^{2}) \cdot (\text{Alpha} + \text{Beta}) ^{h - 1}
$$

$$
\sigma_{L} ^{2} = \text{Omega} / (1 - \text{Alpha} - \text{Beta})
$$

Where n is the last observation, h = 1, ..., `time_steps` (10 by default) the forecast step, sigma_(n+1)^2 the one-step-ahead variance of the fitted GARCH(1, 1) recursion (see `get_garch`) and sigma_L^2 the long-run variance.

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
- Every asset is fitted on its own available returns, so an asset with a shorter history (or a gap)
does not shorten the sample of the others.
- If `growth` is set to True, the method calculates the growth of the forecasted sigma_2 values using
the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["^GSPC"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_garch_forecast()
```

Which returns:

|            |   ^GSPC |   Benchmark |
|:-----------|--------:|------------:|
| 2026-01-01 |  0.0001 |      0      |
| 2026-01-02 |  0.0001 |      0.0001 |
| 2026-01-05 |  0.0001 |      0.0001 |
| 2026-01-06 |  0.0001 |      0.0001 |
| 2026-01-07 |  0.0001 |      0.0001 |
| 2026-01-08 |  0.0001 |      0.0001 |
| 2026-01-09 |  0.0001 |      0.0001 |
| 2026-01-12 |  0.0001 |      0.0001 |
| 2026-01-13 |  0.0001 |      0.0001 |
| 2026-01-14 |  0.0001 |      0.0001 |

---

## get_garch_parameters
Fits a GARCH(1, 1) model to the historical returns and returns the estimated Omega, Alpha and Beta parameters for each asset.

GARCH (Generalized autoregressive conditional heteroskedasticity) is a stochastic model for time series, used to model volatility clustering.

The formula is as follows:

$$
\sigma_{t} ^{2} = \text{Omega} + \text{Alpha} \cdot r_{t-1} ^{2} + \text{Beta} \cdot \sigma_{t-1} ^{2}
$$

$$
\text{Log-Likelihood} = - \text{Σ} (\text{ln}\; \sigma_{t} ^{2} + r_{t} ^{2} / \sigma_{t} ^{2}) (\text{up to constants})
$$

Where r_t are the returns (not demeaned), with the constraints Omega, Alpha, Beta > 0 and Alpha + Beta < 1. The parameters are estimated by maximizing the Gaussian log-likelihood with L-BFGS-B, started from a domain-informed initial guess and from 32 points of a Sobol sequence, and the best fit is finished with Nelder-Mead. The search runs on the parameters scaled to their bounds, as Omega (of the order of a daily variance) and Alpha and Beta differ by orders of magnitude.

The variance recursion starts from a backcast, an exponentially weighted average (decay 0.94) of the first 75 squared returns, which stands in for both the squared return and the variance before the first observation, and every observation enters the likelihood. This is the start the arch package uses, so the estimates agree with it.

Unlike `get_garch` and `get_garch_forecast`, which return a (forecasted) conditional variance path, this method returns the fitted parameters themselves. This is useful when the parameters are needed directly, for example to seed a separate volatility simulation.

For daily equity returns, Alpha is typically between 0.05 and 0.15 and Alpha + Beta (the persistence) between 0.95 and 0.99, meaning a volatility shock fades over weeks rather than days. The long-run variance the model reverts to is Omega / (1 - Alpha - Beta). A fit far outside these ranges is a reason to check the data and the window before using the parameters.

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
- Every asset is fitted on its own available returns, so an asset with a shorter history (or a gap)
does not shorten the sample of the others.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["LOW", "SBUX", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_garch_parameters(rounding=6)
```

Which returns:

|       |      LOW |     SBUX |     TSLA |   Benchmark |
|:------|---------:|---------:|---------:|------------:|
| Omega | 2.1e-05  | 0.000102 | 1.6e-05  |    5e-06    |
| Alpha | 0.035763 | 0.057692 | 0.048602 |    0.154079 |
| Beta  | 0.875036 | 0.715864 | 0.940197 |    0.811018 |

---

## get_gjr_garch
Calculates the conditional variance (sigma_t^2) of the returns with a GJR-GARCH(1, 1, 1) model fitted to them. Take the square root for the conditional volatility, and see `get_gjr_garch_forecast` for the variance forecast.

GJR-GARCH extends GARCH with a leverage term that lets negative shocks (bad news) raise volatility by more than positive shocks of the same size, a well documented asymmetry in equity returns that symmetric GARCH cannot capture.

For more information about the method, see the following paper:

- Glosten, L.R., Jagannathan, R., and Runkle, D.E. (1993). "On the Relation between the Expected Value and the Volatility of the Nominal Excess Return on Stocks." The Journal of Finance, 48(5), 1779-1801.

The formula is as follows:

$$
\sigma_{t} ^{2} = \text{Omega} + (\text{Alpha} + \text{Gamma} \cdot I_{t-1}) \cdot r_{t-1} ^{2} + \text{Beta} \cdot \sigma_{t-1} ^{2}
$$

$$
\sigma_{1} ^{2} = \text{Omega} + (\text{Alpha} + \text{Gamma} / 2 + \text{Beta}) \cdot \text{Backcast}
$$

Where r_t are the returns (not demeaned), I_(t-1) is 1 when r_(t-1) < 0 and 0 otherwise, and the Backcast is the same as in `get_garch`. The parameters maximize the Gaussian log-likelihood under Alpha + Gamma / 2 + Beta < 1 and Alpha + Gamma >= 0 (see `get_gjr_garch_parameters`).

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
- Every asset is fitted on its own available returns, so an asset with a shorter history (or a gap)
does not shorten the sample of the others; dates without a return for an asset are NaN.
- If `growth` is set to True, the method calculates the growth of GJR-GARCH values using the
specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["NVDA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_gjr_garch().tail(5)
```

Which returns:

| Date       |   NVDA |   Benchmark |
|:-----------|-------:|------------:|
| 2025-12-24 | 0.0005 |      0.0001 |
| 2025-12-26 | 0.0005 |      0.0001 |
| 2025-12-29 | 0.0005 |      0      |
| 2025-12-30 | 0.0005 |      0      |
| 2025-12-31 | 0.0005 |      0      |

---

## get_gjr_garch_forecast
Calculates sigma_2 forecasts based on the GJR-GARCH model.

The formula is as follows:

$$
\sigma_{n + h} ^{2} = \sigma_{L} ^{2} + (\sigma_{n + 1} ^{2} - \sigma_{L} ^{2}) \cdot (\text{Alpha} + \text{Gamma} / 2 + \text{Beta}) ^{h - 1}
$$

$$
\sigma_{L} ^{2} = \text{Omega} / (1 - \text{Alpha} - \text{Gamma} / 2 - \text{Beta})
$$

Where n is the last observation, h = 1, ..., `time_steps` (10 by default) the forecast step and sigma_(n+1)^2 the one-step-ahead variance of the fitted GJR-GARCH(1, 1, 1) recursion (see `get_gjr_garch`). The leverage term enters at its expectation, Gamma / 2, as a negative shock is as likely as a positive one.

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
- Every asset is fitted on its own available returns, so an asset with a shorter history (or a gap)
does not shorten the sample of the others.
- If `growth` is set to True, the method calculates the growth of the forecasted sigma_2 values using
the specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["CLUSD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_gjr_garch_forecast()
```

Which returns:

|            |   CLUSD |   Benchmark |
|:-----------|--------:|------------:|
| 2026-01-01 |  0.0003 |      0      |
| 2026-01-02 |  0.0003 |      0      |
| 2026-01-05 |  0.0003 |      0.0001 |
| 2026-01-06 |  0.0003 |      0.0001 |
| 2026-01-07 |  0.0003 |      0.0001 |
| 2026-01-08 |  0.0003 |      0.0001 |
| 2026-01-09 |  0.0003 |      0.0001 |
| 2026-01-12 |  0.0003 |      0.0001 |
| 2026-01-13 |  0.0003 |      0.0001 |
| 2026-01-14 |  0.0004 |      0.0001 |

---

## get_gjr_garch_parameters
Fits a GJR-GARCH(1, 1, 1) model to the historical returns and returns the estimated Omega, Alpha, Gamma and Beta parameters for each asset.

A positive Gamma indicates the presence of a leverage effect (negative shocks raise volatility by more than positive ones of the same size), which symmetric GARCH cannot represent.

The formula is as follows:

$$
\sigma_{t} ^{2} = \text{Omega} + (\text{Alpha} + \text{Gamma} \cdot I_{t-1}) \cdot r_{t-1} ^{2} + \text{Beta} \cdot \sigma_{t-1} ^{2}
$$

$$
\text{Log-Likelihood} = - \text{Σ} (\text{ln}\; \sigma_{t} ^{2} + r_{t} ^{2} / \sigma_{t} ^{2}) (\text{up to constants})
$$

Where r_t are the returns (not demeaned) and I_(t-1) is 1 when r_(t-1) < 0 and 0 otherwise. The log-likelihood is maximized under Alpha + Gamma / 2 + Beta < 1 and Alpha + Gamma >= 0.

The variance recursion starts from a backcast, an exponentially weighted average (decay 0.94) of the first 75 squared returns, with the leverage term at its expectation (Gamma / 2) for the period before the first observation, and every observation enters the likelihood. This is the start the arch package uses, so the estimates agree with it.

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
- Every asset is fitted on its own available returns, so an asset with a shorter history (or a gap)
does not shorten the sample of the others.
- GJR-GARCH nests GARCH (gamma = 0), so the fit never ends at a lower log-likelihood than the
GARCH(1, 1) fit of `get_garch_parameters`: if the search does, the GARCH weights with a Gamma of 0
are returned.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["^GSPC", "^STOXX50E"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_gjr_garch_parameters(rounding=6)
```

Which returns:

|       |    ^GSPC |   ^STOXX50E |   Benchmark |
|:------|---------:|------------:|------------:|
| Omega | 3e-06    |    1e-05    |    3e-06    |
| Alpha | 0        |    0        |    0        |
| Gamma | 0.210531 |    0.308907 |    0.221968 |
| Beta  | 0.870765 |    0.764269 |    0.865708 |

---

## get_egarch
Calculates the conditional variance (sigma_t^2) of the returns with an EGARCH(1, 1) model fitted to them. Take the square root for the conditional volatility, and see `get_egarch_forecast` for the variance forecast.

EGARCH models the log of the conditional variance, which avoids having to constrain the parameters to keep the variance positive and, like GJR-GARCH, lets negative and positive shocks of the same size have a different impact on volatility (the leverage effect).

For more information about the method, see the following paper:

- Nelson, D.B. (1991). "Conditional Heteroskedasticity in Asset

**Returns:** A New
Approach." Econometrica, 59(2), 347-370.

The formula is as follows:

- ln sigma_t^2 = Omega + Alpha * (&#124;z_(t-1)&#124; - √(2 / π)) + Gamma * z_(t-1) + Beta * ln sigma_(t-1)^2
- z_t = r_t / sigma_t
- ln sigma_1^2 = Omega + Beta * ln(Backcast)

Where r_t are the returns (not demeaned), √(2 / π) is the expected &#124;z&#124; of a standard normal shock, the
log variance is kept within [-20, 20] and the Backcast is the same as in `get_garch`. The parameters
maximize the Gaussian log-likelihood with &#124;Beta&#124; < 1 (see `get_egarch_parameters`).

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
- Every asset is fitted on its own available returns, so an asset with a shorter history (or a gap)
does not shorten the sample of the others; dates without a return for an asset are NaN.
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
| 2021Q2 | 0.0229 | 0.0923 |      0.0077 |
| 2021Q3 | 0.0158 | 0.1671 |      0.0049 |
| 2021Q4 | 0.0244 | 0.1704 |      0.0131 |
| 2022Q1 | 0.0411 | 0.0597 |      0.0062 |
| 2022Q2 | 0.0737 | 0.1035 |      0.0116 |
| 2022Q3 | 0.0642 | 0.2104 |      0.009  |
| 2022Q4 | 0.0868 | 0.1936 |      0.0145 |
| 2023Q1 | 0.0975 | 0.3935 |      0.0105 |
| 2023Q2 | 0.0675 | 0.0902 |      0.0078 |
| 2023Q3 | 0.0321 | 0.0321 |      0.0048 |
| 2023Q4 | 0.0565 | 0.0654 |      0.0108 |
| 2024Q1 | 0.0348 | 0.133  |      0.0046 |
| 2024Q2 | 0.0167 | 0.2705 |      0.0017 |
| 2024Q3 | 0.0149 | 0.3389 |      0.002  |
| 2024Q4 | 0.0239 | 0.2276 |      0.0015 |
| 2025Q1 | 0.0094 | 0.0473 |      0.0033 |
| 2025Q2 | 0.0077 | 0.0964 |      0.0076 |
| 2025Q3 | 0.0013 | 0.0458 |      0.0033 |
| 2025Q4 | 0.0025 | 0.0022 |      0.0017 |

---

## get_egarch_forecast
Calculates sigma_2 forecasts based on the EGARCH model.

The formula is as follows:

$$
\text{ln}\; \sigma_{} (n + h) ^{2} = L + \text{Beta} ^{h - 1} \cdot (\text{ln}\; \sigma_{} (n + 1) ^{2} - L)
$$

$$
L = \text{Omega} / (1 - \text{Beta})
$$

$$
\sigma_{n + h} ^{2} = \exp(\text{ln}\; \sigma_{} (n + h) ^{2})
$$

Where n is the last observation, h = 1, ..., `time_steps` (10 by default) the forecast step and sigma_(n+1)^2 the one-step-ahead variance of the fitted EGARCH(1, 1) recursion (see `get_egarch`). The shock terms drop out at their expectation of zero, so the forecast is the exponential of the expected log variance.

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
- Every asset is fitted on its own available returns, so an asset with a shorter history (or a gap)
does not shorten the sample of the others.
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
| 2026Q1 | 0.0012 | 0.0028 |      0.0034 |
| 2026Q2 | 0.001  | 0.0026 |      0.0055 |
| 2026Q3 | 0.0009 | 0.0024 |      0.007  |
| 2026Q4 | 0.0008 | 0.0022 |      0.0079 |
| 2027Q1 | 0.0007 | 0.002  |      0.0084 |
| 2027Q2 | 0.0006 | 0.0018 |      0.0086 |
| 2027Q3 | 0.0005 | 0.0017 |      0.0087 |
| 2027Q4 | 0.0004 | 0.0016 |      0.0088 |
| 2028Q1 | 0.0004 | 0.0014 |      0.0089 |
| 2028Q2 | 0.0003 | 0.0013 |      0.0089 |

---

## get_egarch_parameters
Fits an EGARCH(1, 1) model to the historical returns and returns the estimated Omega, Alpha, Gamma and Beta parameters for each asset.

A negative Gamma indicates the presence of a leverage effect (negative shocks raise volatility by more than positive ones of the same size).

The formula is as follows:

$$
\text{ln}\; \sigma_{t} ^{2} = \text{Omega} + \text{Alpha} \cdot (| z_{t-1} | - \sqrt{2 / \pi}) + \text{Gamma} \cdot z_{t-1} + \text{Beta} \cdot \text{ln}\; \sigma_{} (t-1) ^{2}
$$

$$
\text{Log-Likelihood} = - \text{Σ} (\text{ln}\; \sigma_{t} ^{2} + r_{t} ^{2} / \sigma_{t} ^{2}) (\text{up to constants})
$$

Where r_t are the returns (not demeaned) and z_t = r_t / sigma_t. The log-likelihood is maximized with Omega in [-15, 5], Alpha and Gamma in [-1, 1] and &#124;Beta&#124; < 1, starting the recursion from ln sigma_1^2 = Omega + Beta * ln(Backcast), with the Backcast of `get_garch_parameters`.

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
- Every asset is fitted on its own available returns, so an asset with a shorter history (or a gap)
does not shorten the sample of the others.
- EGARCH's log-variance parameterization is less constrained than plain GARCH, which makes it
prone to unstable, boundary-hugging fits on short return histories, which include quarterly
data over a few years. Prefer daily or weekly returns.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AMZN", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_egarch_parameters(period="daily", rounding=6)
```

Which returns:

|       |      AMZN |      TSLA |   Benchmark |
|:------|----------:|----------:|------------:|
| Omega | -0.382664 | -0.225452 |   -0.309737 |
| Alpha |  0.193573 |  0.081906 |    0.059855 |
| Gamma | -0.080739 | -0.03535  |   -0.181222 |
| Beta  |  0.949074 |  0.964858 |    0.96578  |

---

## get_tail_dependence_coefficient
Calculate the Upper and Lower Tail Dependence Coefficients between `ticker_a` and `ticker_b`.

Correlation only captures the *average* co-movement between two assets -- it says nothing about whether they are more likely to crash together than an equivalent gaussian relationship would imply. The Tail Dependence Coefficient answers that specific question directly: the probability that one asset is in extreme distress, given that the other one already is.

The empirical estimate at q = 0.95 rests on the few days on which both assets are in their worst (or best) 5% at the same time, so it needs several years of daily data to be stable. A gaussian dependence of any correlation below 1 implies zero tail dependence, so a Lower Tail Dependence Coefficient well above zero means that diversification between the two assets is weakest exactly when it is needed.

For more information about the method, see the following papers:

- Embrechts, P., McNeil, A., & Straumann, D. (1999). "Correlation: Pitfalls and Alternatives." RISK Magazine, 12, 69-71.
- Poon, S.H., Rockinger, M., & Tawn, J. (2004). "Extreme Value Dependence in Financial Markets: Diagnostics, Models, and Financial Implications." Review of Financial Studies, 17(2), 581-610.

The formula is as follows (with the default method="empirical" and q=0.95):

$$
\text{Upper Tail Dependence} = \operatorname{\#}(A > Q_{A}(q) \text{and}\; B > Q_{B}(q)) / \operatorname{\#}(A > Q_{A}(q))
$$

$$
\text{Lower Tail Dependence} = \operatorname{\#}(A \leq Q_{A}(1 - q) \text{and}\; B \leq Q_{B}(1 - q)) / \operatorname{\#}(A \leq Q_{A}(1 - q))
$$

Where A and B are the values of `ticker_a` and `ticker_b` on their common dates and Q_A and Q_B their empirical quantiles. With method="gaussian" both coefficients are 0 (1 only for a correlation of exactly 1), and with method="student-t" both are 2 * t_(v+1)(-√((v + 1) * (1 - rho) / (1 + rho))), with v = `dof`, rho the Pearson correlation and t_(v+1) the Student-T distribution function.

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
    ["^GSPC", "^STOXX50E"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_tail_dependence_coefficient("^GSPC", "^STOXX50E")
```

Which returns:

|                       |     Value |
|:----------------------|----------:|
| Lower Tail Dependence |    0.3231 |
| Upper Tail Dependence |    0.3387 |
| Correlation           |    0.4545 |
| Observations          | 1289      |

---

## get_copula_parameters
Calibrate a bivariate copula between `ticker_a` and `ticker_b` on the pseudo-observations (ranks) of their returns: the Clayton, Gumbel and Frank parameters by maximum likelihood, the gaussian correlation from the normal scores, and the Student-T correlation from Kendall's tau with the degrees of freedom by maximum likelihood (Demarta & McNeil, 2005).

When `ticker_a`/`ticker_b` are not given, every unique pair among the Toolkit's tickers is calibrated instead.

A copula separates the dependence structure between two assets from their individual (marginal) return distributions (Sklar's theorem), letting the two be modeled independently. Five families are supported, each capturing a different shape of dependence:

- "gaussian": zero tail dependence -- crashes and rallies are no more likely to happen together than the correlation alone implies. Included mainly as a baseline, since real asset returns typically show more joint tail risk than this.
- "student-t": symmetric, nonzero tail dependence in both tails.
- "clayton": nonzero *lower* tail dependence only -- assets crash together more than they rally together. The most common choice for equity return pairs.
- "gumbel": nonzero *upper* tail dependence only -- assets rally together more than they crash together.
- "frank": zero tail dependence in both tails, but (unlike gaussian) can represent negative dependence and is symmetric around independence.

See `get_best_fitting_copula` to compare all five by AIC on the same pair of assets, and see `get_copula_simulation` to draw joint scenarios from the fitted copula.

The formula is as follows:

$$
u_{i} = \operatorname{Rank}(A_{i}) / (n + 1),\;\; v_{i} = \operatorname{Rank}(B_{i}) / (n + 1)
$$

$$
\text{Gaussian Rho} = \operatorname{Correlation}(\Phi ^{-1} (u),\; \Phi ^{-1} (v))
$$

$$
\text{Student-T Rho} = \operatorname{sin}(\pi \cdot \text{Kendall's Tau} / 2)
$$

$$
\Theta (\text{and the Student-T Degrees of Freedom}) = \text{argmax}\; \text{Σ} \;\text{ln}\; c (u_{i},\; v_{i})
$$

$$
\text{AIC} = 2 \cdot k - 2 \cdot \text{Log-Likelihood}
$$

Where A and B are the values of the two assets on their n common dates, c is the copula density and k the number of fitted parameters (2 for the Student-T, 1 otherwise). The search bounds are [2.05, 60] for the Degrees of Freedom and, for Theta, [0.0001, 100] (Clayton), [1, 50] (Gumbel) and [-50, 50] (Frank). The implied tail dependence is 2^(-1 / Theta) in the lower tail for Clayton, 2 - 2^(1 / Theta) in the upper tail for Gumbel, 2 * t_(v+1)(-√((v + 1) * (1 - Rho) / (1 + Rho))) in both tails for the Student-T and 0 otherwise.

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
    ["GCUSD", "SIUSD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_copula_parameters("GCUSD", "SIUSD", copula="student-t")
```

Which returns:

|                       |      Value |
|:----------------------|-----------:|
| Rho                   |     0.7498 |
| Degrees of Freedom    |     8.1362 |
| Lower Tail Dependence |     0.2821 |
| Upper Tail Dependence |     0.2821 |
| Log-Likelihood        |   532.413  |
| AIC                   | -1060.83   |
| Observations          |  1300      |

---

## get_copula_simulation
Calibrate a bivariate copula (see `get_copula_parameters`) between `ticker_a` and `ticker_b`, and simulate joint scenarios from it.

When `ticker_a`/`ticker_b` are not given, every unique pair among the Toolkit's tickers is calibrated and simulated instead, as columns grouped under a top-level (Ticker A, Ticker B) column per pair.

This is what a copula-based portfolio Monte Carlo simulation needs: draws that preserve the calibrated dependence structure -- including tail dependence, for the "student-t", "clayton" and "gumbel" families -- rather than the (typically understated) joint crash risk a plain multivariate gaussian simulation would produce.

The formula is as follows (with the default copula="gaussian" and empirical_margins=True):

$$
(Z_{1},\; Z_{2}) \sim N(0,\; \left[\left[1,\; \text{Rho}\right],\; \left[\text{Rho},\; 1\right]\right])
$$

$$
U = \Phi(Z_{1}),\;\; V = \Phi(Z_{2})
$$

$$
\text{Simulated Return}\; A = \operatorname{Quantile}(A,\; U),\;\; \text{Simulated Return}\; B = \operatorname{Quantile}(B,\; V)
$$

Where Rho is fitted as in `get_copula_parameters` and Quantile is the empirical quantile (linear interpolation) of each asset's own history. The Student-T copula scales (Z1, Z2) by √(v / W), with W ~ χ²(v), and maps them with the Student-T distribution function; the Clayton, Gumbel and Frank copulas draw U and T uniformly and solve C(V &#124; U) = T for V.

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
    ["HD", "LOW"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_copula_simulation("HD", "LOW", n_simulations=30).head(5)
```

Which returns:

|    |      HD |     LOW |
|---:|--------:|--------:|
|  0 |  0.0001 | -0.0073 |
|  1 | -0.012  | -0.0059 |
|  2 |  0.0332 |  0.0247 |
|  3 |  0.0001 | -0.0019 |
|  4 |  0.0038 | -0.0019 |

---

## get_best_fitting_copula
Calibrate all five supported copula families (see `get_copula_parameters`) between `ticker_a` and `ticker_b`, and compare them by AIC (Akaike Information Criterion) -- the lower the AIC, the better the fit relative to its number of parameters, so the top row is the best-fitting family.

When `ticker_a`/`ticker_b` are not given, every unique pair among the Toolkit's tickers is compared instead.

The formula is as follows:

$$
\text{AIC} = 2 \cdot k - 2 \cdot \text{Log-Likelihood}
$$

Where the Log-Likelihood is that of each family fitted as in `get_copula_parameters` and k the number of fitted parameters (2 for the Student-T copula, 1 for the others).

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
    ["V", "MA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

copulas = toolkit.risk.get_best_fitting_copula("V", "MA")

copulas[["Lower Tail Dependence", "Upper Tail Dependence", "Log-Likelihood", "AIC"]]
```

Which returns:

| Copula    |   Lower Tail Dependence |   Upper Tail Dependence |   Log-Likelihood |      AIC |
|:----------|------------------------:|------------------------:|-----------------:|---------:|
| Student-T |                  0.5596 |                  0.5596 |          946.907 | -1889.81 |
| Gaussian  |                  0      |                  0      |          912.208 | -1822.42 |
| Gumbel    |                  0      |                  0.7388 |          892.134 | -1782.27 |
| Frank     |                  0      |                  0      |          826.803 | -1651.61 |
| Clayton   |                  0.7852 |                  0      |          757.472 | -1512.94 |

---

## get_covar
Calculate the (Delta-)CoVaR of `ticker` conditional on `conditioning_ticker` being in its own distress state.

Ordinary Value at Risk treats each asset in isolation, which misses systemic risk -- the fact that one asset's distress can spill over and worsen another's risk. CoVaR directly measures that spillover: it is the VaR of `ticker`, conditional on `conditioning_ticker` itself being at its own `alpha`-VaR, estimated via a linear Quantile Regression of `ticker`'s returns on `conditioning_ticker`'s returns at quantile `alpha`. The Delta-CoVaR isolates the marginal, distress-specific contribution by subtracting the same construction evaluated in the "normal" (median) state instead.

CoVaR was introduced to measure systemic risk: in its original application `ticker` is a financial-system index (or a bank's peers) and `conditioning_ticker` a single institution, so the Delta-CoVaR reads as that institution's contribution to system-wide tail risk. Because the quantile regression is fitted at the `alpha` quantile, it needs several years of daily data, and the result is a statement about co-movement in the tails, not about causality.

The formula is as follows (with the default alpha=0.05):

$$
\operatorname{Quantile\_alpha}(A | B) = \text{Intercept} + \text{Slope} \cdot B
$$

$$
\text{CoVaR} = \text{Intercept} + \text{Slope} \cdot \text{VaR}_{B}
$$

$$
\text{Delta-CoVaR} = \text{Slope} \cdot (\text{VaR}_{B} - \operatorname{Median}(B))
$$

Where A are the values of `ticker` and B those of `conditioning_ticker` on their common dates, the Intercept and Slope come from a linear quantile regression at quantile alpha (minimizing the check loss) and VaR_B is the empirical alpha-quantile of B.

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
- <u>alpha (float, optional):</u> The tail probability for both the tail quantile regression and
the VaR of `conditioning_ticker` (e.g., 0.05 for the 95% confidence level). Defaults to 0.05.
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
    ["GS", "JPM"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_covar("GS", "JPM").loc[["CoVaR", "Delta-CoVaR"]]
```

Which returns:

|             |   Value |
|:------------|--------:|
| CoVaR       | -0.0353 |
| Delta-CoVaR | -0.0206 |

---

## get_marginal_value_at_risk
Calculate the Marginal Value at Risk (Marginal VaR) of each asset in a portfolio.

Ordinary VaR (see `get_value_at_risk`) treats each asset in isolation. Marginal VaR instead measures how much the *portfolio's* VaR would change for an infinitesimal increase in a given asset's portfolio weight - i.e. the sensitivity of portfolio risk to each holding, not the risk of the holding on its own.

The formula is as follows (with the default distribution="historic"):

$$
\text{Portfolio Return} = \operatorname{SUM}(\text{weight}_{i} \cdot \text{Return}_{i})
$$

$$
\text{Beta}_{i} = \operatorname{Cov}(\text{Return}_{i},\; \text{Portfolio Return}) / \operatorname{Var}(\text{Portfolio Return})
$$

$$
\text{Marginal VaR}_{i} = \text{Beta}_{i} \cdot \text{Portfolio VaR}
$$

Where the weights are normalized to sum to 1, the covariance and variance are sample estimates (ddof=1) on the dates all assets have a return, and Portfolio VaR is the VaR of the portfolio return under `distribution` (see `get_value_at_risk`). The beta-based sensitivity is exact for a zero-mean elliptical distribution and an approximation otherwise; distribution="gaussian" uses the exact derivative instead, with z_alpha the standard normal quantile at alpha:

$$
\text{Gaussian Marginal VaR}_{i} = \text{Mean}_{i} + z_{\alpha} \cdot \operatorname{Cov}(\text{Return}_{i},\; \text{Portfolio Return}) / \operatorname{Std}(\text{Portfolio Return})
$$

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
- <u>alpha (float, optional):</u> The tail probability (e.g., 0.05 for the 95% confidence level).
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
    ["VTI", "TLT", "GLD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_marginal_value_at_risk(weights={"VTI": 0.6, "TLT": 0.3, "GLD": 0.1})
```

Which returns:

|     |   Marginal VaR |
|:----|---------------:|
| VTI |        -0.0159 |
| TLT |        -0.0078 |
| GLD |        -0.0053 |

---

## get_component_value_at_risk
Calculate the Component Value at Risk (Component VaR) of each asset in a portfolio.

Component VaR allocates total portfolio VaR across its constituent assets, such that the allocations sum exactly back to the portfolio VaR - an "Euler" (or "fully consistent") risk decomposition.

The formula is as follows (with the default distribution="historic"):

$$
\text{Component VaR}_{i} = \text{weight}_{i} \cdot \text{Marginal VaR}_{i}
$$

$$
\operatorname{SUM}(\text{Component VaR}_{i}) = \text{Portfolio VaR}
$$

Where the weights are normalized to sum to 1 and Marginal VaR_i is that of `get_marginal_value_at_risk`: Beta_i * Portfolio VaR by default, or the exact derivative with distribution="gaussian".

Where Marginal VaR measures each asset's risk *sensitivity*, Component VaR measures its actual *contribution* in the same units as portfolio VaR, making it directly usable to identify which holdings account for the largest share of portfolio risk.

Component VaR is the basis of risk budgeting: a holding with a 20% weight that accounts for 45% of the portfolio VaR stands out immediately, and a component with the opposite sign of the portfolio VaR marks a holding that hedges the rest. The components always add up to the portfolio VaR, but the beta-based allocation is exact only for normally (elliptically) distributed returns and an approximation for the historical distribution used by default.

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
- <u>alpha (float, optional):</u> The tail probability (e.g., 0.05 for the 95% confidence level).
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
    ["VTI", "AGG", "GLD", "VNQ"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_component_value_at_risk(
    weights={"VTI": 0.5, "AGG": 0.3, "GLD": 0.1, "VNQ": 0.1}
)
```

Which returns:

|           |   Component VaR |
|:----------|----------------:|
| VTI       |         -0.0081 |
| AGG       |         -0.0008 |
| GLD       |         -0.0005 |
| VNQ       |         -0.0015 |
| Portfolio |         -0.0109 |

---

## get_var_backtest
Backtest a Value at Risk model against realized returns.

A Value at Risk estimate is only useful if it is actually well-calibrated against reality. This method builds a rolling, out-of-sample VaR path (each VaR estimate uses only the `window_size` returns preceding it, never the return it is compared against) and tests it with Kupiec's Proportion of Failures test (is the overall breach rate consistent with `alpha`?) and/or Christoffersen's independence test (are breaches spread out over time, or do they cluster together?).

Regulators backtest VaR on the number of exceptions over the last 250 trading days (the Basel traffic-light approach at 99% confidence), and Kupiec's test formalises the same question. With few exceptions the test has little power, so a model that passes is not necessarily well calibrated. Clustered exceptions, which Christoffersen's test detects, are the usual failure of historical VaR when volatility rises.

The formula is as follows (with the default distribution="historic", alpha=0.05 and window_size=252):

$$
\text{VaR}_{t} = \operatorname{Quantile}(\text{Return}_{t-252},\; ...,\; \text{Return}_{t-1} \text{;} \alpha)
$$

$$
\text{Breach}_{t} = 1 \;\text{if Return}_{t} < \text{VaR}_{t},\;\; \text{else 0}
$$

$$
\text{Kupiec Statistic} = - 2 \cdot \text{ln} \left[(1 - \alpha) ^{n - x} \cdot \alpha ^{x} / ((1 - x / n) ^{n - x} \cdot (x / n) ^{x})\right]
$$

$$
\text{Christoffersen Statistic} = - 2 \cdot \text{ln} \left[L(\pi) / L(\pi_{01},\; \pi_{11})\right]
$$

Where n is the number of out-of-sample VaR estimates and x the number of breaches. L(pi) is the likelihood of the breach sequence with a single breach probability pi, and L(pi_01, pi_11) that of a first-order Markov chain in which the breach probability depends on whether the previous period was a breach. Both statistics are compared with a χ² distribution with one degree of freedom for the p-value.

For more information about the methods, see the following papers:

- Kupiec, P.H. (1995). "Techniques for Verifying the Accuracy of Risk Measurement Models." The Journal of Derivatives, 3(2), 73-84.
- Christoffersen, P.F. (1998). "Evaluating Interval Forecasts." International Economic Review, 39(4), 841-862.

**Also known as:** VaR validation, VaR backtest, POF test.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly or yearly).
Defaults to "daily", since `window_size` is expressed in return observations of this frequency
(252 only means "about one year" when `period` is daily).
- <u>distribution (str, optional):</u> The distribution to use for the rolling VaR estimates, one of
"historic", "gaussian", "studentt" or "evt". Defaults to "historic".
- <u>alpha (float, optional):</u> The tail probability for the VaR estimates (e.g., 0.05 for the 95%
confidence level). Defaults to 0.05. With "evt" it can be at most 0.05, since the Generalized
Pareto Distribution is fitted above the 95th percentile of losses; a larger `alpha` gives an
empty result (with a logged error).
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
a single sub-period provides. Each asset is rolled over its own available returns, so a shorter
history of one asset does not shorten the others.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["EURUSD", "USDJPY", "GBPUSD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_var_backtest(test="kupiec")
```

Which returns:

|                  |   EURUSD |   USDJPY |   GBPUSD |   Benchmark |
|:-----------------|---------:|---------:|---------:|------------:|
| Kupiec Statistic |   8.3686 |   1.8323 |   2.2039 |      0.0836 |
| P-Value          |   0.0038 |   0.1759 |   0.1377 |      0.7725 |

---

## get_acerbi_szekely_test
Backtest a Conditional Value at Risk (Expected Shortfall) model against realized returns, via the Acerbi-Szekely (2014) Z2 statistic.

`get_var_backtest` above only backtests the VaR estimate itself -- it checks how often (and how independently) the VaR threshold is breached, but says nothing about the *severity* of the losses on those breach days, which is exactly the extra information a CVaR (Expected Shortfall) estimate is supposed to add over VaR. This method builds a rolling, out-of-sample CVaR (and VaR) path and compares the actual loss on each breach day to the CVaR that was supposed to describe the average loss on such days.

The formula is as follows (with the default distribution="historic", alpha=0.05 and window_size=252):

$$
Z_{2} = \text{Σ} (\text{Return}_{t} \cdot \text{Breach}_{t} / \text{CVaR}_{t}) / (n \cdot \alpha) - 1
$$

$$
\text{P-Value} = 1 - \Phi(Z_{2} / \text{Standard Error})
$$

Where VaR_t and CVaR_t are estimated from the 252 returns before t (see `get_var_backtest`), Breach_t is 1 if Return_t < VaR_t and 0 otherwise, n is the number of estimates and the Standard Error is the sample standard deviation (ddof=1) of Z2 over `n_bootstrap` paired bootstrap resamples. Returns and CVaR are both negative, so Z2 is about 0 for a well-calibrated model and positive when the realized tail losses exceed the CVaR (the opposite sign of the paper, which counts losses as positive).

For more information about the method, see the following paper:

- Acerbi, C., & Szekely, B. (2014). "Back-Testing Expected Shortfall." RISK Magazine, 27(11), 76-81.

**Also known as:** Acerbi-Szekely test, ES backtest, Z2 test.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly or yearly).
Defaults to "daily", since `window_size` is expressed in return observations of this frequency.
- <u>distribution (str, optional):</u> The distribution to use for the rolling VaR/CVaR estimates,
one of "historic", "gaussian", "studentt" or "evt". Defaults to "historic".
- <u>alpha (float, optional):</u> The tail probability for the VaR/CVaR estimates (e.g., 0.05 for the 95%
confidence level). Defaults to 0.05. With "evt" it can be at most 0.05, since the Generalized
Pareto Distribution is fitted above the 95th percentile of losses; a larger `alpha` gives an
empty result (with a logged error).
- <u>window_size (int, optional):</u> The rolling window size (in number of return observations) used
to estimate each VaR/CVaR value. Defaults to 252 (approximately one trading year of daily
returns).
- <u>n_bootstrap (int, optional):</u> The number of bootstrap resamples used to estimate the Standard
Error of Z2. Defaults to 1000.
- <u>random_state (int, optional):</u> The seed for the bootstrap random number generator. Defaults to
42.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.

**Returns:**

pd.DataFrame: The Z2 statistic, its bootstrap Standard Error, its one-sided p-value (a low
value means the model underestimates the tail losses), and the number of breaches observed
(returns strictly below the VaR), per asset.

**Notes:**

- The rolling VaR/CVaR path is calculated over the full return history, not the `within_period`
slices used elsewhere in this module, since a meaningful rolling window generally needs more
history than a single sub-period provides. Each asset is rolled over its own available returns.
- The paper simulates the null distribution of Z2 from the model's predictive distributions; a
rolling path does not carry those, so the p-value is approximated with a paired bootstrap of the
observed (return, VaR, CVaR) triples and a normal approximation (see
`backtesting_model.get_acerbi_szekely_test`).

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["BA", "DAL", "CCL"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_acerbi_szekely_test().loc[["Acerbi-Szekely Statistic", "P-Value"]]
```

Which returns:

|                          |     BA |    DAL |    CCL |   Benchmark |
|:-------------------------|-------:|-------:|-------:|------------:|
| Acerbi-Szekely Statistic | 0.1548 | 0.2473 | 0.1402 |      0.2394 |
| P-Value                  | 0.176  | 0.0762 | 0.1963 |      0.0785 |

---

## get_skewness
Calculate the Skewness of an investment portfolio or asset's returns.

Skewness is a statistical measure used in finance to assess the asymmetry in the distribution of returns for an investment portfolio or asset over a defined period. It offers valuable insights into the shape of the return distribution, indicating whether returns are skewed towards the positive or negative side of the mean. Skewness is a crucial tool for investors and analysts seeking to understand the potential risk and return characteristics of an investment, aiding in the assessment of the distribution's tails and potential outliers. It provides a means to gauge the level of skew in returns, enabling more informed investment decisions and risk management strategies.

The formula is as follows:

$$
\text{Skewness} = n / ((n - 1) \cdot (n - 2)) \cdot \text{Σ} ((\text{Return} - \text{Mean}) / \text{Std}) ^{3}
$$

Where n is the number of returns and Std the sample standard deviation (ddof=1), which is the bias-adjusted sample skewness (G1) of pandas and Excel's SKEW.

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
    ["NFLX", "DIS", "WBD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_skewness(period="yearly", within_period=True)
```

Which returns:

|      |    NFLX |     DIS |     WBD |   Benchmark |
|:-----|--------:|--------:|--------:|------------:|
| 2021 |  1.8966 |  0.2848 | -2.1536 |     -0.3334 |
| 2022 | -2.1029 | -0.5086 | -0.0126 |      0.0454 |
| 2023 |  1.5636 | -0.2155 | -0.42   |     -0.0206 |
| 2024 |  0.872  |  0.7012 |  0.6324 |     -0.5242 |
| 2025 | -0.2855 |  0.6672 |  1.9711 |      1.5069 |

---

## get_kurtosis
Calculate the Kurtosis of an investment portfolio or asset's returns.

Kurtosis is a statistical measure used in finance to evaluate the shape of the probability distribution of returns for an investment portfolio or asset over a defined time period. It assesses the "tailedness" of the return distribution, indicating whether returns have fatter or thinner tails compared to a normal distribution. Kurtosis plays a critical role in risk assessment by revealing the potential presence of extreme outliers or the likelihood of heavy tails in the return data. This information aids investors and analysts in understanding the degree of risk associated with an investment and assists in making more informed decisions regarding risk tolerance. In essence, kurtosis serves as a valuable tool for comprehending the distribution characteristics of returns, offering insights into the potential for rare but significant events in the financial markets.

By default this is Pearson's kurtosis, which is 3 for a normal distribution; with `fisher=True` it is the excess kurtosis, which is 0. Daily stock returns typically show an excess kurtosis of several points, and within a single year one exceptional day (an earnings shock, a market-wide gap) can push it above 10, so a high value often reflects one event rather than a persistently fat-tailed distribution.

The formula is as follows (with the default fisher=False):

$$
\text{Kurtosis} = \text{Excess Kurtosis} + 3
$$

$$
\text{Excess Kurtosis} = n(n + 1) / ((n - 1) (n - 2) (n - 3)) \cdot \text{Σ} z ^{4} - \operatorname{3}(n - 1) ^{2} / ((n - 2) (n - 3))
$$

$$
z = (\text{Return} - \text{Mean}) / \text{Std}
$$

Where n is the number of returns and Std the sample standard deviation (ddof=1), which is the bias-adjusted sample excess kurtosis (G2) of pandas and Excel's KURT. With fisher=True the Excess Kurtosis is returned.

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
    ["BTCUSD", "ETHUSD", "SOLUSD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_kurtosis(period="yearly", within_period=True, fisher=True)
```

Which returns:

|      |   BTCUSD |   ETHUSD |   SOLUSD |   Benchmark |
|:-----|---------:|---------:|---------:|------------:|
| 2021 |   1.6215 |   3.5555 |   2.46   |      2.5374 |
| 2022 |   4.0666 |   2.545  |   6.8965 |      2.359  |
| 2023 |   3.2756 |   2.4865 |   5.3817 |      1.416  |
| 2024 |   1.9522 |   4.0366 |   0.2918 |      3.8134 |
| 2025 |   2.3709 |   4.0428 |   4.1957 |     45.0722 |

---

## get_hill_estimator
Calculate the Hill Estimator of the tail index of returns, per asset.

Unlike the (finite-sample) Skewness and Kurtosis above, the Hill Estimator is a semi-parametric estimate of how heavy the tail of the return distribution actually is, under the assumption that the tail follows a Pareto-type power law. Smaller values of the tail index indicate a heavier tail (more extreme outliers are likely) -- as a rule of thumb, a tail index below 4 implies the Kurtosis is theoretically infinite, and below 2 implies the Variance itself is theoretically infinite.

For daily stock returns the tail index typically lies between about 2 and 5, while a normal distribution has an infinite tail index. The estimate depends on `k`: practitioners plot it against a range of `k` (a Hill plot) and read it where it is stable, since a small `k` is noisy and a large `k` pulls in the center of the distribution.

The formula is as follows (with the default tail="left" and k=0.1):

$$
\text{Hill Shape} (\xi) = (1 / k) \cdot \text{Σ} (\text{ln}\; X_{} (i) - \text{ln}\; X_{} (k + 1)) \text{for}\; i = 1,\;\; \text{...},\;\; \text{k}
$$

$$
\text{Hill Tail Index} = 1 / \xi
$$

$$
\text{Standard Error} = \text{Hill Tail Index} / \sqrt{k}
$$

Where X_(1) >= X_(2) >= ... are the strictly positive losses (the negated returns, or the returns themselves for tail="right") sorted from large to small, and k is the number of order statistics used: int(0.1 * the number of positive losses) by default, or `k` itself when it is an integer.

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
it is interpreted as the fraction of the strictly positive observations to use. A period
without such observations reports NaN with 0 observations used. Defaults to 0.1 (the top 10%).
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
    ["BTCUSD", "^GSPC", "GCUSD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_hill_estimator(k=60)
```

Which returns:

|                       |   BTCUSD |   ^GSPC |   GCUSD |   Benchmark |
|:----------------------|---------:|--------:|--------:|------------:|
| Hill Tail Index       |   3.4392 |  2.9068 |  3.0565 |      2.7613 |
| Hill Shape (xi)       |   0.2908 |  0.344  |  0.3272 |      0.3621 |
| Standard Error        |   0.444  |  0.3753 |  0.3946 |      0.3565 |
| Observations Used (k) |  60      | 60      | 60      |     60      |

---

## get_variance
Calculate the Variance of an investment portfolio or asset's returns for a given period based on the daily historical returns.

Variance measures the spread or dispersion of returns around the mean. A higher Variance indicates more variability in the returns, while a lower Variance suggests that the returns are closer to the mean.

The formula is as follows:

$$
\text{Variance} = \operatorname{Var}(\text{Daily Returns within the period}) \cdot \text{Trading Days per Period}
$$

Where Var is the sample variance (ddof=1) and the trading days per period are 252 / 52 (weekly), 252 / 12 (monthly), 252 / 4 (quarterly) or 252 (yearly). With `rolling`, the result is the sample variance of the last `rolling` returns of the chosen period itself, without scaling.

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
    ["WMT", "TGT", "COST"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_variance(period="yearly")
```

Which returns:

| Date   |    WMT |    TGT |   COST |   Benchmark |
|:-------|-------:|-------:|-------:|------------:|
| 2021   | 0.0278 | 0.0559 | 0.0359 |      0.0167 |
| 2022   | 0.0714 | 0.2131 | 0.0984 |      0.0588 |
| 2023   | 0.0245 | 0.0965 | 0.0365 |      0.0171 |
| 2024   | 0.0313 | 0.1377 | 0.0355 |      0.0158 |
| 2025   | 0.063  | 0.1166 | 0.0467 |      0.038  |

---

## get_volatility
Calculate the Volatility of an investment portfolio or asset's returns for a given period based on the daily historical prices.

Volatility measures the amount of dispersion or variability in returns. It is the square root of the Variance. A higher Volatility indicates greater variability, while a lower Volatility suggests that returns are closer to the mean.

By default this is the close-to-close Volatility, i.e. the standard deviation of the daily returns. The `method` parameter selects one of four range-based estimators instead, each of which uses more of the day's price action than just the close and is therefore more statistically efficient (i.e. needs fewer observations to reach the same precision), at the cost of additional assumptions about how prices move:

- `"parkinson"` - uses the daily trading range (High vs Low) rather than the close-to-close return, assuming prices follow a continuous geometric Brownian motion with no drift and no overnight jumps.
- `"garman_klass"` - extends Parkinson by also incorporating the Open and Close, which allows it to account for the opening jump and makes it more efficient still (assuming, as Parkinson does, no drift and no overnight jumps beyond the modeled open).
- `"rogers_satchell"` - drift-independent, meaning it remains unbiased even when the underlying asset has a non-zero expected return over the period, at the cost of still assuming no overnight jumps.
- `"yang_zhang"` - a weighted combination of the overnight (close-to-open) Variance, the open-to-close Variance and the Rogers-Satchell Variance. It is both drift-independent and accounts for overnight jumps, which makes it the most statistically efficient of the range-based estimators implemented here.

The formula is as follows (with the default method="close_to_close"):

$$
\text{Volatility} = \operatorname{Std}(\text{Daily Returns within the period}) \cdot \sqrt{\text{Trading Days per Period}}
$$

Where Std is the sample standard deviation (ddof=1) and the trading days per period are 252 / 52 (weekly), 252 / 12 (monthly), 252 / 4 (quarterly) or 252 (yearly). The range-based estimators take the square root of a daily variance and scale it the same way, with H, L, O and C the daily High, Low, Open and Close, C_(-1) the previous Close, Mean the average and Var the sample variance (ddof=1) over the days in the period:

$$
\text{Parkinson Variance} = \operatorname{Mean}(\ln(H / L) ^{2}) / (4 \cdot \text{ln}\; 2)
$$

$$
\text{Garman-Klass Variance} = \operatorname{Mean}(0.5 \cdot \ln(H / L) ^{2} - (2 \cdot \text{ln}\; 2 - 1) \cdot \ln(C / O) ^{2})
$$

$$
\text{Rogers-Satchell Variance} = \operatorname{Mean}(\ln(H / C) \cdot \ln(H / O) + \ln(L / C) \cdot \ln(L / O))
$$

$$
\text{Yang-Zhang Variance} = \operatorname{Var}(\ln(O / C_{- 1})) + k \cdot \operatorname{Var}(\ln(C / O)) + (1 - k) \cdot \text{Rogers-Satchell Variance}
$$

$$
k = 0.34 / (1.34 + (n + 1) / (n - 1)),\;\; \text{with n the number of days in the period}
$$

With `rolling`, the result is the sample standard deviation of the last `rolling` returns of the chosen period itself, without scaling.

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

Passing `method="parkinson"` (or another range-based estimator) uses the daily trading range instead of
only the closes.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["EURUSD", "BTCUSD", "^GSPC", "GCUSD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_volatility(period="yearly")
```

Which returns:

| Date   |   EURUSD |   BTCUSD |   ^GSPC |   GCUSD |   Benchmark |
|:-------|---------:|---------:|--------:|--------:|------------:|
| 2021   |   0.0574 |   0.6758 |  0.1    |  0.1156 |      0.0993 |
| 2022   |   0.091  |   0.531  |  0.189  |  0.1216 |      0.1897 |
| 2023   |   0.0764 |   0.3662 |  0.1042 |  0.1088 |      0.104  |
| 2024   |   0.0665 |   0.4441 |  0.098  |  0.1201 |      0.0975 |
| 2025   |   0.0831 |   0.3485 |  0.1457 |  0.1554 |      0.152  |

---

## get_har_rv_forecast
Calculate the Corsi (2009) Heterogeneous Autoregressive Realized Volatility (HAR-RV) forecast of future daily Realized Variance, per asset.

Volatility clustering happens across multiple, overlapping time horizons at once. HAR-RV captures this cheaply -- without the numerical optimization a GARCH-family fit requires (see `get_garch`) -- by regressing future daily Realized Variance on trailing daily, weekly and monthly average Realized Variance components. The daily Realized Variance itself can be constructed in several ways via `estimator`: the simplest is the squared daily return, while the OHLC range-based estimators (see `get_volatility`, which exposes the same estimators via its own `method` parameter) use the daily (pre-period-aggregation) term behind each of those estimators instead, which is more statistically efficient since it uses the daily trading range rather than only the close-to-close move.

The formula is as follows (with the default estimator="squared_return", weekly_window=5, monthly_window=22 and horizon=1):

$$
\text{RV}_{t} = \text{Return}_{t} ^{2}
$$

$$
\text{RV} ^{w_{t}} = \operatorname{Mean}(\text{RV}_{t-4},\; ...,\; \text{RV}_{t}) \text{and RV} ^{m_{t}} = \operatorname{Mean}(\text{RV}_{t-21},\; ...,\; \text{RV}_{t})
$$

$$
\text{Forecast of RV}_{} (t + 1) = b_{0} + b_{d} \cdot \text{RV}_{t} + b_{w} \cdot \text{RV} ^{w_{t}} + b_{m} \cdot \text{RV} ^{m_{t}}
$$

Where b_0, b_d, b_w and b_m are estimated once by ordinary least squares over each asset's full history, and the forecast of RV_(t+1) is shown at date t. The range-based estimators replace RV_t with the daily Parkinson, Garman-Klass or Rogers-Satchell variance term (see `get_volatility`).

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

In the example below, the last row is the forecast for the first trading day after the end date,
which has not been observed yet.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["SPY", "QQQ"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
    benchmark_ticker=None,
)

toolkit.risk.get_har_rv_forecast(estimator="squared_return").tail(5)
```

Which returns:

| Date       |    SPY |    QQQ |
|:-----------|-------:|-------:|
| 2025-12-24 | 0.0001 | 0.0001 |
| 2025-12-26 | 0.0001 | 0.0001 |
| 2025-12-29 | 0.0001 | 0.0001 |
| 2025-12-30 | 0.0001 | 0.0001 |
| 2025-12-31 | 0.0001 | 0.0001 |

---

## get_amihud_illiquidity
Calculate the Amihud (2002) Illiquidity ratio, per asset.

The Amihud ratio measures the average price impact of trading -- how much the price moves per dollar of trading volume. A high value means that even a small amount of trading moves the price a lot (the asset is illiquid), while a low value means the asset can absorb a large amount of trading with little price impact (the asset is liquid).

The Amihud ratio is mainly a cross-sectional measure: it ranks stocks by how much a given dollar volume moves the price and is used as a liquidity factor in asset pricing. Its level depends on the scale, the frequency and the price level of the market, so compare stocks within the same market and period, and expect the ratio of large caps to be several orders of magnitude below that of small caps.

For more information about the method, see the following paper:

- Amihud, Y. (2002). "Illiquidity and Stock

**Returns:** Cross-Section and
Time-Series Effects." Journal of Financial Markets, 5(1), 31-56.

The formula is as - <u>follows (with the default scale of 1,000,000):</u>

- Amihud Illiquidity = Mean(&#124;Return_t&#124; / (Close_t * Volume_t)) * 1,000,000

Where the mean runs over the periods of the chosen frequency (within each period with `within_period`),
and periods without dollar volume are skipped.

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

A `scale` of one billion is used in the example below: liquid stocks trade so much dollar volume
relative to their typical daily price move that the default `scale` of 1,000,000 (as in Amihud's
original paper) can round their values to 0.0 at the default precision.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["SNAP", "ETSY", "LYFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_amihud_illiquidity(scale=1e9)
```

Which returns:

|           |   Value |
|:----------|--------:|
| SNAP      |  0.0634 |
| ETSY      |  0.0768 |
| LYFT      |  0.1277 |
| Benchmark |  0.0002 |

---

## get_roll_spread
Calculate the Roll (1984) implied bid-ask spread, per asset.

Roll's model shows that, under a stylized microstructure model in which the true (efficient) price follows a random walk and observed trade prices randomly bounce between the bid and the ask, the effective spread can be backed out purely from the serial covariance of consecutive price changes, without needing any actual quote data. If the estimated covariance is zero or positive, no valid estimate can be backed out and NaN is returned instead.

The Roll measure is used when no quote data is available, typically for less liquid stocks or historical studies. On daily closes of liquid large caps it mostly picks up price noise rather than the bid-ask bounce, and in trending periods the autocovariance is positive and no estimate exists, so treat it as a rough, relative measure.

For more information about the method, see the following paper:

- Roll, R. (1984). "A Simple Implicit Measure of the Effective Bid-Ask Spread in an Efficient Market." The Journal of Finance, 39(4), 1127-1139.

The formula is as follows:

$$
\text{Roll Spread} = 2 \cdot \sqrt{- \operatorname{Cov}(\Delta P_{t},\; \Delta P_{} (t-1))}
$$

$$
\text{Relative Roll Spread} = \text{Roll Spread} / \operatorname{Mean}(P)
$$

Where P is the Close price, ΔP_t = P_t - P_(t-1) and Cov the sample autocovariance (ddof=1) of consecutive price changes; a covariance of zero or above gives NaN.

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

pd.DataFrame: The Roll Spread (in price units), the Relative Roll Spread (the Roll Spread divided
by the mean price, as a decimal), the underlying lag-1 autocovariance, and whether that
autocovariance was negative (i.e. whether a valid estimate could be backed out), per asset.

**Notes:**

- The method retrieves historical Close price data based on the specified `period` and calculates
the Roll Spread for each asset in the Toolkit instance.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["KO", "PEP", "PG"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_roll_spread()
```

Which returns:

|                      |          KO |         PEP |         PG |   Benchmark |
|:---------------------|------------:|------------:|-----------:|------------:|
| Roll Spread          |  0.173128   |  0.72957    |  0.751753  |  1.97906    |
| Relative Roll Spread |  0.0028038  |  0.00449337 |  0.0049553 |  0.00408282 |
| Autocovariance       | -0.00749332 | -0.133068   | -0.141283  | -0.979167   |
| Valid Estimate       |  1          |  1          |  1         |  1          |

---

## get_excess_volatility
Calculate the Excess Volatility of an investment portfolio or asset's returns for a given period based on the daily historical returns.

Excess Volatility is the Volatility of the Excess Return, i.e. the daily return minus the risk free rate, scaled to the given period in the same way as the Volatility.

The formula is as follows:

$$
\text{Excess Volatility} = \operatorname{Std}(\text{Daily Return} - \text{Daily Risk Free Rate}) \cdot \sqrt{\text{Trading Days per Period}}
$$

Where Std is the sample standard deviation (ddof=1) over the days within the period, the annualized risk free rate is converted to a daily rate, and the trading days per period are 252 / 52 (weekly), 252 / 12 (monthly), 252 / 4 (quarterly) or 252 (yearly). With `rolling`, the result is the sample standard deviation of the last `rolling` excess returns of the chosen period itself, without scaling.

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
    ["ADBE", "CRM", "ORCL"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_excess_volatility(period="yearly")
```

Which returns:

| Date   |   ADBE |    CRM |   ORCL |   Benchmark |
|:-------|-------:|-------:|-------:|------------:|
| 2021   | 0.2924 | 0.282  | 0.2927 |      0.1293 |
| 2022   | 0.4506 | 0.4722 | 0.3053 |      0.2425 |
| 2023   | 0.3178 | 0.2958 | 0.302  |      0.1307 |
| 2024   | 0.3663 | 0.3594 | 0.3226 |      0.1257 |
| 2025   | 0.3062 | 0.319  | 0.6169 |      0.1948 |

---

## get_downside_deviation
Calculate the Downside Deviation of an investment portfolio or asset's returns.

The Downside Deviation, also known as semi-deviation, measures the dispersion of the returns below a minimum acceptable return (MAR), isolating the volatility of negative outcomes from the volatility of the overall return distribution. It underlies risk-adjusted return measures such as the Sortino Ratio and the Omega Ratio.

The formula is as follows (with the default minimum_acceptable_return of 0):

$$
\text{Downside Deviation} = \sqrt{\text{Σ} \;\text{min} (\text{Return}_{t} - \text{MAR},\; 0) ^{2} / n}
$$

Where n is the number of all returns, so returns above the MAR count as a shortfall of zero rather than being left out.

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
    ["NEE", "DUK", "SO"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_downside_deviation()
```

Which returns:

|           |   Value |
|:----------|--------:|
| NEE       |  0.0124 |
| DUK       |  0.0074 |
| SO        |  0.0079 |
| Benchmark |  0.0081 |

---

## get_mean_absolute_deviation
Calculate the Mean Absolute Deviation (MAD) of an investment portfolio or asset's returns for a given period based on the daily historical returns.

MAD measures the average absolute distance of each return from the mean return. Unlike Variance and Volatility, it does not square the deviations, making it less sensitive to outliers.

The formula is as follows:

$$
\text{Mean Absolute Deviation} = \text{Σ} | \text{Return}_{t} - \text{Mean} | / n
$$

Where the returns are the n daily returns within each period, without scaling to the period length.

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
    ["KO", "PEP", "MDLZ"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_mean_absolute_deviation(period="yearly")
```

Which returns:

| Date   |     KO |    PEP |   MDLZ |   Benchmark |
|:-------|-------:|-------:|-------:|------------:|
| 2021   | 0.007  | 0.0069 | 0.0073 |      0.0061 |
| 2022   | 0.0091 | 0.009  | 0.0098 |      0.0119 |
| 2023   | 0.0063 | 0.007  | 0.008  |      0.0064 |
| 2024   | 0.0061 | 0.0076 | 0.0082 |      0.0058 |
| 2025   | 0.0083 | 0.0104 | 0.0104 |      0.0074 |

---

## get_coefficient_of_variation
Calculate the Coefficient of Variation (CV) of an investment portfolio or asset's returns for a given period based on the daily historical returns.

The Coefficient of Variation is the ratio of the standard deviation to the mean of returns, which normalizes dispersion relative to the average return. This makes it useful for comparing the relative volatility of assets with different average returns, which a raw standard deviation cannot do.

The Coefficient of Variation is only meaningful when the mean return is clearly positive. In a period with an average daily return close to zero it explodes, and in a down period it turns negative, so for returns it is best read over periods with a positive mean, or replaced by a Sharpe ratio, which is its inverse with the risk-free rate subtracted.

The formula is as follows:

$$
\text{Coefficient of Variation} = \operatorname{Std}(\text{Daily Returns}) / \operatorname{Mean}(\text{Daily Returns})
$$

Where both are taken over the daily returns within each period, with Std the sample standard deviation (ddof=1), without scaling to the period length.

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
    ["MSFT", "ORCL", "IBM"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2023-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_coefficient_of_variation(period="yearly")
```

Which returns:

| Date   |    MSFT |    ORCL |     IBM |   Benchmark |
|:-------|--------:|--------:|--------:|------------:|
| 2023   |  8.0237 | 16.2298 | 12.0942 |      8.3745 |
| 2024   | 22.4294 |  9.8256 | 10.3503 |      8.6564 |
| 2025   | 21.9925 | 28.2432 | 12.934  |     16.8499 |

---

## get_ewma_volatility
Calculate the exponentially weighted moving average (EWMA) Volatility of an investment portfolio or asset's daily returns, following the RiskMetrics methodology.

Unlike a fixed-window rolling Volatility, EWMA Volatility weights recent observations more heavily than older ones, so it reacts faster to changes in the underlying volatility regime. It is a simpler, more interpretable alternative to a full GARCH fit.

The formula is as follows:

$$
\text{EWMA Variance} (t) = \lambda \cdot \text{EWMA Variance} (t-1) + (1 - \lambda) \cdot \operatorname{Return}(t-1) ^{2}
$$

$$
\text{EWMA Volatility} (t) = \sqrt{\text{EWMA Variance} (t)}
$$

Where lambda is 0.94 by default and Return(t-1) the previous daily return, so the value on a day only uses the returns before it. The recursion starts from the first squared return.

With the RiskMetrics decay factor of 0.94, about 70% of the weight sits on the last 20 trading days, so EWMA Volatility reacts within days to a market shock and falls back almost as quickly. The values are daily; multiply them by the square root of 252 for an annualized figure comparable with `get_volatility(period="yearly")`.

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
    ["USDJPY", "EURUSD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_ewma_volatility().tail(5)
```

Which returns:

| Date       |   USDJPY |   EURUSD |   Benchmark |
|:-----------|---------:|---------:|------------:|
| 2025-12-26 |   0.0046 |   0.0046 |      0.0057 |
| 2025-12-28 |   0.0045 |   0.0044 |      0.0055 |
| 2025-12-29 |   0.0043 |   0.0043 |      0.0054 |
| 2025-12-30 |   0.0042 |   0.0042 |      0.0052 |
| 2025-12-31 |   0.0041 |   0.0045 |      0.0051 |

---

## get_autocorrelation
Calculate the Autocorrelation Function (ACF) of each asset's daily returns for a range of lags.

The ACF measures the correlation between a return series and a lagged version of itself. A significant ACF at a given lag indicates that returns are not fully independent over time, which is relevant for assessing return predictability and volatility clustering (as opposed to a trading-signal use case, which is why this lives in the Risk module rather than Technicals).

The formula is as follows:

$$
\operatorname{ACF}(k) = \text{Σ} (r_{t} - \text{Mean}) \cdot (r_{t + k} - \text{Mean}) / \text{Σ} (r_{t} - \text{Mean}) ^{2}
$$

Where r_t are the n daily returns (missing values dropped), the numerator runs over t = 1, ..., n - k, the denominator over all n returns, and k = 1, ..., `lags` (10 by default).

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
    ["SPY", "QQQ", "IWM"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
    benchmark_ticker=None,
)

toolkit.risk.get_autocorrelation()
```

Which returns:

|   Lag |     SPY |     QQQ |     IWM |
|------:|--------:|--------:|--------:|
|     1 | -0.031  | -0.0387 | -0.0092 |
|     2 | -0.0069 | -0.001  | -0.0254 |
|     3 | -0.0626 | -0.0629 | -0.0055 |
|     4 | -0.0344 | -0.0216 | -0.0437 |
|     5 | -0.0075 | -0.0071 | -0.016  |
|     6 | -0.0104 |  0      | -0.0112 |
|     7 | -0.0109 |  0.0031 | -0.013  |
|     8 | -0.0063 | -0.0118 | -0.0168 |
|     9 |  0.0399 |  0.0505 |  0.0285 |
|    10 | -0.0111 | -0.0214 | -0.0059 |

---

## get_hurst_exponent
Calculate the Hurst Exponent of each asset's daily (adjusted close) log price series, a measure of long-term memory that indicates whether the price is mean-reverting, trending, or a random walk.

The Hurst Exponent (H) is interpreted as follows:

- H < 0.5: the series is mean-reverting (anti-persistent).
- H = 0.5: the series is a random walk (no memory).
- H > 0.5: the series is trending (persistent).

For liquid stocks the estimate is usually close to 0.5, and with lags of at most `max_lag` days it describes short-term behaviour only; a value of 0.45 or 0.55 over a few years is within estimation noise rather than evidence of a tradable pattern.

The formula is as follows (with the default max_lag=20):

$$
\sigma(\tau) = \operatorname{Std}(\text{ln}\; P_{} (t + \tau) - \text{ln}\; P_{t})
$$

$$
\text{ln}\; \sigma (\tau) = c + H \cdot \text{ln}\; \tau,\;\; \text{fitted by least squares over}\; \tau = 2,\;\; \text{...},\;\; \text{20}
$$

Where P is the daily adjusted close, Std the population standard deviation (ddof=0) of the lagged log price differences and H, the slope, the Hurst Exponent.

**Args:**

- <u>max_lag (int, optional):</u> The maximum lag, included, to use when estimating the exponent:
the regression runs over the lags 2 up to and including `max_lag`. Defaults to 20.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to 4.

**Returns:**

pd.Series: The estimated Hurst Exponent for each asset.

**Notes:**

- The exponent is estimated with the generalized Hurst (structure function) method of
Di Matteo, Aste & Dacorogna (2005) on the logarithm of the adjusted close, as in that paper,
see `risk_model.get_hurst_exponent`. The lagged differences of log prices are log returns,
so the estimate does not depend on the price level.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["EURUSD", "GCUSD", "BTCUSD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_hurst_exponent()
```

Which returns:

|           |   Value |
|:----------|--------:|
| EURUSD    |  0.4229 |
| GCUSD     |  0.4886 |
| BTCUSD    |  0.5057 |
| Benchmark |  0.4621 |

---

