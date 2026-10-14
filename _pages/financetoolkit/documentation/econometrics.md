---
title: Econometrics
seo_title: Econometrics Module – Finance Toolkit Docs
excerpt: The Econometrics module contains statistical tests and estimators for financial time series and panel data, including unit root and cointegration tests, regression estimators, causal inference methods, diagnostics, forecasting and event studies.
description: "Reference for every function and parameter in the Finance Toolkit's Econometrics module: unit root and cointegration tests, regressions and forecasting."
author_profile: false
permalink: /projects/financetoolkit/docs/econometrics
classes: wide-sidebar
layout: single
redirect_from:
    - /econometrics
sidebar:
    nav: "financetoolkit-docs-econometrics"
---

The Econometrics module contains statistical tests and estimators for financial time series and panel data. It covers unit root and cointegration tests, regression estimators (OLS, WLS, GLS, quantile, logit, probit, Fama-MacBeth), causal inference methods (instrumental variables, difference-in-differences, regression discontinuity, propensity score matching, synthetic control), panel data estimators, specification and diagnostic tests, time series forecasting (ARIMA, VAR, VECM) and event studies.

Unlike the other modules, this one depends on `statsmodels` and `linearmodels`. These are bundled in the optional `econometrics` extra, so install the Finance Toolkit with:

```python
pip install "financetoolkit[econometrics]" -U
```

{% include algolia.html %}

## get_arch_lm_test
Calculate Engle's Lagrange Multiplier (LM) test for ARCH effects.

The test regresses squared, mean-demeaned returns on `lags` of themselves and tests whether the resulting R-squared is significantly different from zero. A significant result (low p-value) indicates that the return series exhibits volatility clustering, and a GARCH-family model is an appropriate choice for it. A high p-value suggests fitting GARCH would not be meaningful, since there is no detectable time-varying volatility to model.

For more information about the method, see the following paper:

- Engle, R.F. (1982). "Autoregressive Conditional Heteroscedasticity with Estimates of the Variance of United Kingdom Inflation." Econometrica, 50(4), 987-1008.

**Also known as:** ARCH-LM test, Engle's ARCH test.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>within_period (bool, optional):</u> Whether to calculate the test within the specified period or for
the entire period. Thus whether to look at the test within a specific year (if period = 'yearly')
or look at the entirety of all years. Defaults to False. Note that this requires intraday data
when period = 'daily', since a single day only nests observations when intraday data was fetched.
- <u>lags (int, optional):</u> The number of lags to test for ARCH effects. Defaults to 5.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the
assets tested. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.

**Returns:**

pd.DataFrame: The ARCH-LM statistic and its p-value per asset.

**Notes:**

- The method retrieves historical return data based on the specified `period` and runs the ARCH-LM
test for each asset in the Toolkit instance.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AMZN", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_arch_lm_test(period="quarterly")
```

Which returns:

|                   |   AMZN |   TSLA |
|:------------------|-------:|-------:|
| ARCH-LM Statistic | 9.5073 | 1.6855 |
| P-Value           | 0.0905 | 0.8907 |

---

## get_jarque_bera_test
Calculate the Jarque-Bera test for normality.

The test combines sample skewness and excess kurtosis into a single statistic that is chi-squared distributed with 2 degrees of freedom under the null hypothesis that returns are normally distributed. A significant result (low p-value) indicates that returns are not normally distributed, which is relevant when choosing between e.g. gaussian and Student-T based Value at Risk models.

For more information about the method, see the following paper:

- Jarque, C.M. and Bera, A.K. (1987). "A Test for Normality of Observations and Regression Residuals." International Statistical Review, 55(2), 163-172.

**Also known as:** JB test, normality test.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>within_period (bool, optional):</u> Whether to calculate the test within the specified period or for
the entire period. Thus whether to look at the test within a specific year (if period = 'yearly')
or look at the entirety of all years. Defaults to False. Note that this requires intraday data
when period = 'daily', since a single day only nests observations when intraday data was fetched.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the
assets tested. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.

**Returns:**

pd.DataFrame: The Jarque-Bera statistic and its p-value per asset.

**Notes:**

- The method retrieves historical return data based on the specified `period` and runs the
Jarque-Bera test for each asset in the Toolkit instance.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AMZN", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_jarque_bera_test(period="quarterly")
```

Which returns:

|                       |   AMZN |   TSLA |
|:----------------------|-------:|-------:|
| Jarque-Bera Statistic | 1.852  | 0.3192 |
| P-Value               | 0.3961 | 0.8525 |

---

## get_ljung_box_test
Calculate the Ljung-Box test for autocorrelation.

The test aggregates the squared Autocorrelation Function up to lag `h` into a single statistic that is chi-squared distributed with `h` degrees of freedom under the null hypothesis that the series exhibits no autocorrelation up to that lag. A significant result (low p-value) indicates that the series is autocorrelated, which is relevant both as a standalone diagnostic (e.g. to check whether a return series follows a random walk) and as a residual diagnostic after fitting a model (e.g. checking that GARCH residuals are no longer autocorrelated).

For more information about the method, see the following paper:

- Ljung, G.M., & Box, G.E.P. (1978). "On a Measure of Lack of Fit in Time Series Models." Biometrika, 65(2), 297-303.

**Also known as:** Ljung-Box Q test, portmanteau test.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>within_period (bool, optional):</u> Whether to calculate the test within the specified period or for
the entire period. Thus whether to look at the test within a specific year (if period = 'yearly')
or look at the entirety of all years. Defaults to False. Note that this requires intraday data
when period = 'daily', since a single day only nests observations when intraday data was fetched.
- <u>lags (int, optional):</u> The number of lags to test for autocorrelation up to. Defaults to 10.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the
assets tested. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.

**Returns:**

pd.DataFrame: The Ljung-Box statistic and its p-value per asset.

**Notes:**

- The method retrieves historical return data based on the specified `period` and runs the
Ljung-Box test for each asset in the Toolkit instance.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AMZN", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_ljung_box_test(period="quarterly", within_period=False)
```

Which returns:

|                     |   AMZN |   TSLA |
|:--------------------|-------:|-------:|
| Ljung-Box Statistic | 8.702  | 9.7873 |
| P-Value             | 0.5606 | 0.4594 |

---

## get_variance_ratio_test
Calculate the Lo-MacKinlay Variance Ratio test for the random walk hypothesis.

The test compares the Variance of `q`-period (overlapping) compounded returns to `q` times the Variance of single-period returns. Under the random walk hypothesis these should be equal, giving a Variance Ratio of 1. A Variance Ratio above 1 with a significant (low) p-value indicates positive autocorrelation (momentum/trending behavior), while a Variance Ratio below 1 with a significant p-value indicates negative autocorrelation (mean-reversion).

For more information about the method, see the following paper:

- Lo, A.W., & MacKinlay, A.C. (1988). "Stock Market Prices Do Not Follow Random Walks: Evidence from a Simple Specification Test." Review of Financial Studies, 1(1), 41-66.

**Also known as:** Lo-MacKinlay test, VR test.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>within_period (bool, optional):</u> Whether to calculate the test within the specified period or for
the entire period. Thus whether to look at the test within a specific year (if period = 'yearly')
or look at the entirety of all years. Defaults to False. Note that this requires intraday data
when period = 'daily', since a single day only nests observations when intraday data was fetched.
- <u>q (int, optional):</u> The number of periods to compound returns over. Defaults to 2.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the
assets tested. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.

**Returns:**

pd.DataFrame: The Variance Ratio, the (homoskedastic) test statistic and its p-value
per asset.

**Notes:**

- The method retrieves historical return data based on the specified `period` and runs the
Variance Ratio test for each asset in the Toolkit instance.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AMZN", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_variance_ratio_test(period="quarterly", within_period=False)
```

Which returns:

|                          |    AMZN |    TSLA |
|:-------------------------|--------:|--------:|
| Variance Ratio           |  0.8952 |  0.7879 |
| Variance Ratio Statistic | -0.4568 | -0.9247 |
| P-Value                  |  0.6478 |  0.3551 |

---

## get_cusum_test
Calculate the CUSUM test for the stability of the mean of returns over time.

The test fits a constant-mean model to the returns and cumulates the (scaled) OLS residuals into a path that behaves like a Brownian Bridge under the null hypothesis of a stable mean. A stable mean keeps the path close to zero, while a mean shift partway through the series (a structural break, e.g. a regime change) drags the path away from zero; the test statistic is the maximum absolute value of that path.

For more information about the method, see the following paper:

- Ploberger, W., & Kramer, W. (1992). "The CUSUM Test with OLS Residuals." Econometrica, 60(2), 271-285.

**Also known as:** CUSUM test, CUSUM of OLS residuals test, Ploberger-Kramer test.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>within_period (bool, optional):</u> Whether to calculate the test within the specified period or for
the entire period. Thus whether to look at the test within a specific year (if period = 'yearly')
or look at the entirety of all years. Defaults to False. Note that this requires intraday data
when period = 'daily', since a single day only nests observations when intraday data was fetched.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the
assets tested. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.

**Returns:**

pd.DataFrame: The CUSUM statistic, its p-value, the number of observations used, the
1%/5%/10% critical boundary values, and whether stability is rejected at the 5% level,
per asset.

**Notes:**

- The method retrieves historical return data based on the specified `period` and runs the
CUSUM test for each asset in the Toolkit instance.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2019-01-01",
    end_date="2023-12-31",
)

toolkit.econometrics.get_cusum_test(period="quarterly", within_period=False)
```

---

## get_augmented_dickey_fuller
Calculate the Augmented Dickey-Fuller (ADF) test for a unit root, per asset.

The test regresses the first difference of the series on its own lagged level and `p` lags of its own first difference. The null hypothesis is that the series has a unit root (is a random walk, not mean-reverting); the alternative is that it is stationary. This is a standard first step before modeling a price series or spread with mean-reverting methods, since those methods assume stationarity.

For more information about the method, see the following paper:

- Dickey, D.A. and Fuller, W.A. (1979). "Distribution of the Estimators for Autoregressive Time Series with a Unit Root." Journal of the American Statistical Association, 74(366a), 427-431.

**Also known as:** ADF test, unit root test, stationarity test.

**Args:**

- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to test. Defaults to "Adj Close".
- <u>max_lag (int, optional):</u> The maximum number of lagged differences to consider. Defaults to
the Schwert (1989) rule of thumb.
- <u>regression (str, optional):</u> Which deterministic terms to include, one of "n" (none), "c"
(constant) or "ct" (constant and trend). Defaults to "c".
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the
assets tested. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.

**Returns:**

pd.DataFrame: The ADF statistic, its p-value, lags used, observations used, 1%/5%/10%
critical values, and whether the unit root is rejected at the 5% level, per asset.

**Notes:**

- The method retrieves historical price data based on the specified `period` and runs the ADF
test for each asset in the Toolkit instance.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AMZN", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2019-01-01",
    end_date="2023-12-31",
)

toolkit.econometrics.get_augmented_dickey_fuller(period="quarterly")
```

Which returns:

|                       |         AMZN |      TSLA |
|:----------------------|-------------:|----------:|
| ADF Statistic         | -7.15693     | -2.23772  |
| P-Value               |  3.03759e-10 |  0.192841 |
| Lags Used             |  8           |  8        |
| Observations          | 11           | 11        |
| Critical Value 1%     | -4.22324     | -4.22324  |
| Critical Value 5%     | -3.18937     | -3.18937  |
| Critical Value 10%    | -2.72984     | -2.72984  |
| Reject Unit Root (5%) |  1           |  0        |

---

## get_kpss_test
Calculate the Kwiatkowski-Phillips-Schmidt-Shin (KPSS) test for stationarity, per asset.

KPSS is the natural complement to the Augmented Dickey-Fuller test: where the ADF null hypothesis is that the series HAS a unit root, the KPSS null hypothesis is that the series IS stationary, with a unit root as the alternative. Running both together is standard practice to triangulate a confident conclusion -- ADF rejecting a unit root and KPSS failing to reject stationarity together give a confident stationarity conclusion, while the two tests disagreeing flags an ambiguous case.

For more information about the method, see the following paper:

- Kwiatkowski, D., Phillips, P.C.B., Schmidt, P., & Shin, Y. (1992). "Testing the Null Hypothesis of Stationarity against the Alternative of a Unit Root." Journal of Econometrics, 54(1-3), 159-178.

**Also known as:** KPSS test, stationarity test.

**Args:**

- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to test. Defaults to "Adj Close".
- <u>regression (str, optional):</u> Which deterministic term to remove before testing, one of "c"
(constant, level-stationarity) or "ct" (constant and trend, trend-stationarity).
Defaults to "c".
- <u>lags (int, optional):</u> The truncation lag for the long-run variance estimate. Defaults
to `statsmodels`' automatic (Hobijn, Franses & Ooms, 2004) bandwidth selection.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the
assets tested. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.

**Returns:**

pd.DataFrame: The KPSS statistic, its p-value, truncation lag used, observations used,
1%/2.5%/5%/10% critical values, and whether stationarity is rejected at the 5% level,
per asset.

**Notes:**

- The method retrieves historical price data based on the specified `period` and runs the
KPSS test for each asset in the Toolkit instance.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AMZN", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2019-01-01",
    end_date="2023-12-31",
)

toolkit.econometrics.get_kpss_test(period="quarterly")
```

Which returns:

|                           |    AMZN |    TSLA |
|:--------------------------|--------:|--------:|
| KPSS Statistic            |  0.1739 |  0.5193 |
| P-Value                   |  0.1    |  0.0373 |
| Lags Used                 |  2      |  2      |
| Observations              | 20      | 20      |
| Critical Value 1%         |  0.739  |  0.739  |
| Critical Value 2.5%       |  0.574  |  0.574  |
| Critical Value 5%         |  0.463  |  0.463  |
| Critical Value 10%        |  0.347  |  0.347  |
| Reject Stationarity (5%)  |  0      |  1      |

---

## get_phillips_perron_test
Calculate the Phillips-Perron (PP) test for a unit root, per asset.

Phillips-Perron tests the same null hypothesis as the Augmented Dickey-Fuller test (a unit root), but corrects for heteroskedasticity and serial correlation in the errors nonparametrically via a Newey-West long-run variance estimate, rather than by adding lagged-difference terms to the regression as ADF does. PP and ADF should broadly agree on the same series since they test the same null with different correction methods.

For more information about the method, see the following paper:

- Phillips, P.C.B., & Perron, P. (1988). "Testing for a Unit Root in Time Series Regression." Biometrika, 75(2), 335-346.

**Also known as:** PP test, Z_t test.

**Args:**

- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to test. Defaults to "Adj Close".
- <u>regression (str, optional):</u> Which deterministic term to include, one of "c" (constant) or
"ct" (constant and trend). Defaults to "c". Note "n" (no constant) is not supported, see
`econometrics.unitroot_model.get_phillips_perron_test` for why.
- <u>lags (int, optional):</u> The truncation lag for the Newey-West long-run variance estimate.
Defaults to the Schwert (1989) rule of thumb.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the
assets tested. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.

**Returns:**

pd.DataFrame: The Phillips-Perron Z_t statistic, truncation lag used, observations used,
1%/5%/10% critical values, and whether the unit root is rejected at the 5% level, per asset.

**Notes:**

- The method retrieves historical price data based on the specified `period` and runs the
Phillips-Perron test for each asset in the Toolkit instance.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AMZN", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_phillips_perron_test(period="quarterly")
```

Which returns:

|                           |      AMZN |     TSLA |
|:--------------------------|----------:|---------:|
| Phillips-Perron Statistic | -0.773263 | -1.92247 |
| Lags Used                 |  7        |  7       |
| Observations              | 19        | 19       |
| Critical Value 1%         | -3.43     | -3.43    |
| Critical Value 5%         | -2.86     | -2.86    |
| Critical Value 10%        | -2.57     | -2.57    |
| Reject Unit Root (5%)     |  0        |  0       |

---

## get_zivot_andrews_test
Calculate the Zivot-Andrews test for a unit root, per asset, allowing for a single structural break at an unknown (endogenously estimated) date.

The (A)DF/KPSS/PP tests above all assume the deterministic component of the series (its constant and/or trend) is stable throughout the sample. If a series instead has a single one-time break -- e.g. a permanent level shift or a change in trend slope, such as a stock split, spin-off, or a structural shift in the business -- the ordinary ADF test is biased towards not rejecting the unit root even for a genuinely (trend-)stationary series with a break. The Zivot-Andrews test corrects for this by adding a break dummy to the ADF regression and choosing, for each asset, the break date that is most favorable to the stationary alternative -- which is why it needs its own (more negative) critical values rather than the ordinary ADF ones.

For more information about the method, see the following papers:

- Zivot, E., & Andrews, D.W.K. (1992). "Further Evidence on the Great Crash, the Oil-Price Shock, and the Unit-Root Hypothesis." Journal of Business & Economic Statistics, 10(3), 251-270.
- Perron, P. (1989). "The Great Crash, the Oil Price Shock, and the Unit Root Hypothesis." Econometrica, 57(6), 1361-1401.

**Also known as:** ZA test, structural break unit root test.

**Args:**

- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to test. Defaults to "Adj Close".
- <u>max_lag (int, optional):</u> The maximum number of lagged differences to consider when
selecting the (single, reused) lag length. Defaults to the Schwert (1989) rule of thumb.
- <u>regression (str, optional):</u> Which break to allow for, one of "c" (a break in the
level/intercept), "t" (a break in the trend slope) or "ct" (both). Defaults to "c".
- <u>trim (float, optional):</u> The fraction of observations excluded from the candidate break
date search at the start and end of the sample. Must be in [0, 1/3). Defaults to 0.15.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the
assets tested. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.

**Returns:**

pd.DataFrame: The Zivot-Andrews statistic, its p-value, the (0-indexed) position of the
selected break date within the used sample, the number of lags and observations used,
the 1%/5%/10% critical values, and whether the unit root is rejected at the 5% level, per
asset.

**Notes:**

- The method retrieves historical price data based on the specified `period` and runs the
Zivot-Andrews test for each asset in the Toolkit instance.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2019-01-01",
    end_date="2023-12-31",
)

toolkit.econometrics.get_zivot_andrews_test(period="weekly")
```

Which returns:

|                         |        AAPL |       MSFT |
|:------------------------|------------:|-----------:|
| Zivot-Andrews Statistic |  -4.71085   |  -4.43116  |
| P-Value                 |   0.0685808 |   0.141445 |
| Break Index             | 169         | 169        |
| Observations            | 261         | 261        |
| Lags Used               |   0         |   0        |
| Critical Value 1%       |  -5.27644   |  -5.27644  |
| Critical Value 5%       |  -4.81067   |  -4.81067  |
| Critical Value 10%      |  -4.56618   |  -4.56618  |
| Reject Unit Root (5%)   |   0         |   0        |

---

## get_engle_granger_cointegration
Calculate the Engle-Granger test for cointegration between every ordered pair of tickers in the Toolkit instance.

Two individually non-stationary series (e.g. two stock prices, each following a random walk) are cointegrated if some linear combination of them is stationary, i.e. they share a long-run equilibrium relationship even though each wanders on its own in the short run. This is the classic statistical foundation for pairs-trading: if two assets are cointegrated, deviations of the spread from its equilibrium level tend to revert, making the spread itself tradeable.

For more information about the method, see the following paper:

- Engle, R.F. and Granger, C.W.J. (1987). "Co-integration and Error Correction: Representation, Estimation, and Testing." Econometrica, 55(2), 251-276.

**Also known as:** EG test, residual-based cointegration test, pairs-trading test.

**Args:**

- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to test. Defaults to "Adj Close".
- <u>max_lag (int, optional):</u> The maximum number of lagged differences to consider in the
underlying ADF test on the residuals. Defaults to `statsmodels`' automatic selection.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the
tickers paired up. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.

**Returns:**

pd.DataFrame: One row per ordered `(Dependent, Independent)` ticker pair, with the
Engle-Granger statistic, its p-value, 1%/5%/10% critical values, and whether
cointegration is found at the 5% level -- the test is not symmetric (normalizing on
the dependent ticker matters), so both orderings of every pair are included.

**Notes:**

- The method retrieves historical price data based on the specified `period` for every
ticker in the Toolkit instance and runs the Engle-Granger test on every ordered pair.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_engle_granger_cointegration(period="quarterly")
```

Which returns:

(the 1%/10% critical value columns follow the same pattern as
5%, omitted here for width)

|                  |   Engle-Granger Statistic |   P-Value |   Critical Value 1% |   Critical Value 5% |   Critical Value 10% | Cointegrated (5%)   |
|:-----------------|--------------------------:|----------:|--------------------:|--------------------:|---------------------:|:--------------------|
| ('AAPL', 'MSFT') |                        -0 |    0.9859 |            -4.56573 |            -3.67661 |             -3.27521 | False               |
| ('MSFT', 'AAPL') |                        -0 |    0.9859 |            -4.56573 |            -3.67661 |             -3.27521 | False               |

---

## get_johansen_cointegration
Calculate the Johansen test for cointegration among every ticker in the Toolkit instance.

The Engle-Granger test only handles two assets and imposes an arbitrary normalization (which asset is "dependent"). Johansen's test generalizes this to `N >= 2` assets at once by testing the rank of the long-run coefficient matrix in a Vector Error Correction Model (VECM) fit to all assets jointly. The estimated rank equals the number of independent cointegrating (long-run equilibrium) relationships among the assets: rank 0 means none of them are cointegrated, rank `N` means the whole system is already stationary in levels, and a rank in between means that many independent stationary combinations exist among the `N` individually non-stationary price series.

For more information about the method, see the following papers:

- Johansen, S. (1988). "Statistical Analysis of Cointegration Vectors." Journal of Economic Dynamics and Control, 12(2-3), 231-254.
- Johansen, S. (1991). "Estimation and Hypothesis Testing of Cointegration Vectors in Gaussian Vector Autoregressive Models." Econometrica, 59(6), 1551-1580.

**Also known as:** Johansen test, Johansen procedure, VECM rank test.

**Args:**

- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to test. Defaults to "Adj Close".
- <u>det_order (int, optional):</u> Which deterministic term to include: -1 (none), 0 (a
constant, restricted to lie in the cointegrating relation) or 1 (a linear trend
restricted to the cointegrating relation, alongside an unrestricted constant in
the short-run dynamics). Defaults to 0.
- <u>k_ar_diff (int, optional):</u> The number of lagged first differences to include as
short-run dynamics. Defaults to 1.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the
tickers tested jointly. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.

**Returns:**

pd.DataFrame: One row per candidate cointegration rank `r = 0, ..., N-1`, with the
corresponding eigenvalue, trace statistic, max-eigenvalue statistic, their 90%/95%/99%
critical values, and whether each is rejected at the 5% level. The estimated rank is the
first row (in rank order) that is NOT rejected.

**Notes:**

- The method retrieves historical price data based on the specified `period` for every ticker
in the Toolkit instance and runs the Johansen test jointly across all of them.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_johansen_cointegration(period="quarterly")
```

Which returns:

(showing the trace-statistic columns; the max-eigenvalue-statistic
columns follow the same pattern)

|        |   Eigenvalue |   Trace Statistic |   Trace Critical Value 95% | Reject (Trace, 5%)   |
|:-------|-------------:|------------------:|---------------------------:|:---------------------|
| r <= 0 |       0.528  |           13.6694 |                    15.4943 | False                |
| r <= 1 |       0.0086 |            0.1564 |                     3.8415 | False                |

---

## get_granger_causality
Calculate the Granger causality test, for every ordered pair of tickers in the Toolkit instance, of whether the second helps predict the first.

"Granger causality" is a statement about predictive power, not true causation: one asset is said to Granger-cause another if past values of the first, combined with past values of the second itself, predict the second significantly better than past values of the second alone.

For more information about the method, see the following paper:

- Granger, C.W.J. (1969). "Investigating Causal Relations by Econometric Models and Cross-Spectral Methods." Econometrica, 37(3), 424-438.

**Also known as:** Granger causality test, predictive causality, lead-lag test.

**Args:**

- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to test. Defaults to "Return", since
Granger causality assumes a stationary series (unlike the ADF/Engle-Granger tests, which
operate on price levels on purpose).
- <u>max_lag (int, optional):</u> The number of lags of both assets to include in the regressions.
Defaults to 5.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the
tickers paired up. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.

**Returns:**

pd.DataFrame: One row per ordered `(Dependent, Independent)` ticker pair, with the
F-statistic, its p-value, and whether the independent ticker is found to
Granger-cause the dependent ticker at the 5% level -- Granger causality is inherently
directional, so both orderings of every pair are included.

**Notes:**

- The method retrieves historical return data based on the specified `period` for every
ticker in the Toolkit instance and runs the Granger causality test on every ordered pair.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_granger_causality(period="weekly", max_lag=3)
```

Which returns:

|                  |   F-Statistic |   P-Value | Granger-Causes (5%)   |
|:-----------------|--------------:|----------:|:----------------------|
| ('AAPL', 'MSFT') |       2.47418 | 0.0621177 | False                 |
| ('MSFT', 'AAPL') |       1.44163 | 0.231182  | False                 |

---

## get_diebold_mariano_test
Compare the forecast accuracy of two volatility forecasting methods against realized (squared return) Variance, per asset, via the Diebold-Mariano (1995) test.

Rather than comparing two different assets, this compares two different ways of forecasting the *same* asset's next-day Variance -- e.g. the simpler exponentially weighted (EWMA, see `Risk.get_ewma_volatility`) approach against a plain rolling-window Standard Deviation -- to determine whether one is significantly more accurate than the other for a given asset.

For more information about the method, see the following paper:

- Diebold, F.X., & Mariano, R.S. (1995). "Comparing Predictive Accuracy." Journal of Business & Economic Statistics, 13(3), 253-263.

**Also known as:** DM test, forecast comparison test.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, quarterly, or yearly).
Defaults to "daily", since `window_size` is expressed in return observations of this
frequency.
- <u>method_a (str, optional):</u> The first volatility forecasting method, one of "ewma" or "rolling".
Defaults to "ewma".
- <u>method_b (str, optional):</u> The second (competing) volatility forecasting method, one of "ewma"
or "rolling". Defaults to "rolling".
- <u>window_size (int, optional):</u> The rolling window size used by the "rolling" method. Defaults to
22 (approximately one trading month).
- <u>lambda_ (float, optional):</u> The decay factor used by the "ewma" method. Defaults to 0.94.
- <u>loss (str, optional):</u> The loss function to compare forecast errors with, one of "squared" or
"absolute". Defaults to "squared".
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the
assets tested. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.

**Returns:**

pd.DataFrame: The Diebold-Mariano statistic, its p-value, the mean loss differential (negative
favors `method_a`) and the number of observations used, per asset.

**Notes:**

- Both forecasts are lagged by one period (i.e. use only information available up to, and
including, the prior period) before being compared to the realized squared return, so this is a
genuinely out-of-sample forecast comparison rather than an in-sample fit comparison.
- Like `Risk.get_var_backtest`, this is calculated over the full return history rather than the
`within_period` slices used elsewhere in this module, since the rolling/EWMA forecasts need more
history than a single sub-period provides.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_diebold_mariano_test(method_a="ewma", method_b="rolling")
```

Which returns:

|                           |      AAPL |      MSFT |
|:--------------------------|----------:|----------:|
| Diebold-Mariano Statistic |   -2.1569 |   -1.3434 |
| P-Value                   |    0.0312 |    0.1794 |
| Mean Loss Differential    |   -0      |   -0      |
| Observations              | 1232      | 1232      |

---

## get_ols
Fit an Ordinary Least Squares (OLS) regression of `dependent_ticker` on `independent_tickers`, using the selected `column` (returns by default) of each ticker.

OLS estimates the coefficients that minimise the sum of squared residuals, i.e. the line (or plane) that best explains the dependent ticker from the independent tickers:

- beta_hat = (X'X)^-1 X'y

Each coefficient is the expected change in `dependent_ticker` for a one-unit change in that independent ticker, holding the others fixed, and the intercept is what remains when all of them are zero. With returns this is the familiar way to estimate how strongly one asset moves with others (e.g. a beta against an index).

Under the classical assumptions (linearity, no perfect multicollinearity, homoskedastic and uncorrelated errors) OLS is the Best Linear Unbiased Estimator (Gauss-Markov). The coefficients stay unbiased when the errors are heteroskedastic, but the classical standard errors do not: check with `get_breusch_pagan_test` or `get_white_test` and, if needed, refit with a robust `cov_type` such as "HC1" (or "HC3" for small samples), or "HAC" when the errors are also autocorrelated.

For more information about the HAC covariance, see the following paper:

- Newey, W.K. & West, K.D. (1987). "A Simple, Positive Semi-Definite, Heteroskedasticity and Autocorrelation Consistent Covariance Matrix." Econometrica, 55(3), 703-708.

**Also known as:** linear regression, least squares regression.

**Args:**

- <u>dependent_ticker (str &#124; None, optional):</u> The dependent (predicted) asset.
Defaults to None, meaning the Toolkit instance's first ticker.
- <u>independent_tickers (str &#124; list[str] &#124; None, optional):</u> The independent
(predictor) asset(s). Defaults to None, meaning every other ticker in
the Toolkit instance besides `dependent_ticker`.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" in the
default independent ticker(s) (has no effect when independent_tickers is given
explicitly). Defaults to False.
- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to regress on. Defaults to "Return".
- <u>add_constant (bool, optional):</u> Whether to include an intercept. Defaults to True.
- <u>cov_type (str, optional):</u> Which covariance estimator to use for the standard errors --
one of "nonrobust" (classical, assumes homoskedastic errors), "HC0"/"HC1"/"HC2"/"HC3"
(heteroskedasticity-robust), "cluster" (cluster-robust, requires `clusters`) or "HAC"
(Newey-West, heteroskedasticity-and-autocorrelation-consistent, requires `maxlags`).
Use `get_breusch_pagan_test`/`get_white_test` to check for heteroskedasticity and
`get_ljung_box_test` to check for autocorrelation first. Defaults to "nonrobust".
- <u>clusters (pd.Series &#124; None, optional):</u> The cluster label for each observation
(e.g. a coarser time bucket derived from the return index, to correct for
within-period correlation), required when `cov_type="cluster"`. Aligned to the
regression's own index before use, so it may be indexed by the full period
index even though the regression drops periods with missing data. Defaults
to None.
- <u>maxlags (int &#124; None, optional):</u> The maximum lag to include when estimating the
HAC (Newey-West) covariance matrix, required when `cov_type="HAC"`. A common
rule of thumb is `floor(4 * (n / 100)^(2/9))` (Newey & West, 1994). Defaults to
None.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.

**Returns:**

pd.DataFrame: A coefficient table (Coefficient, Std. Error, t-Statistic, P-Value),
indexed by regressor name.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AMZN", "TSLA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

# AMZN (the first ticker) is dependent; TSLA is independent
toolkit.econometrics.get_ols(period="quarterly")

# Or, override which ticker is dependent/independent, and pull in Benchmark too
toolkit.econometrics.get_ols(
    dependent_ticker="AMZN",
    independent_tickers=["TSLA", "Benchmark"],
    period="quarterly",
    cov_type="HC1",
)
# Or, simply opt every default independent ticker (here, just TSLA) into
# including Benchmark too:
toolkit.econometrics.get_ols(period="quarterly", include_benchmark=True)

# Or, use Newey-West (HAC) standard errors for time-series regressions
# where errors may be both heteroskedastic and autocorrelated:
toolkit.econometrics.get_ols(period="quarterly", cov_type="HAC", maxlags=4)
```

Which returns:

(for the first call, AMZN regressed on TSLA)

|           |   Coefficient |   Std. Error |   t-Statistic |   P-Value |
|:----------|--------------:|-------------:|--------------:|----------:|
| Intercept |        0.0069 |       0.04   |        0.1731 |    0.8626 |
| TSLA      |        0.3094 |       0.1116 |        2.7738 |    0.0055 |

---

## get_wls
Fit a Weighted Least Squares (WLS) regression of `dependent_ticker` on `independent_tickers`.

When the error variance differs across observations (heteroskedasticity) with a known or estimable structure, `Var(e_i) = sigma^2 / w_i`, OLS remains unbiased but is no longer the most efficient estimator. WLS restores efficiency by minimising the weighted sum of squared residuals, so noisier observations (low weight) count less than precise ones (high weight):

- beta_hat = (X'WX)^-1 X'Wy, with W = diag(weights)

With equal weights WLS reduces to OLS. A typical use is down-weighting periods of high volatility, so that a few turbulent periods do not dominate the estimated relationship. Use `get_breusch_pagan_test` or `get_white_test` to establish whether heteroskedasticity is present before choosing WLS over OLS.

**Also known as:** weighted regression.

**Args:**

- <u>weights (pd.Series):</u> The (positive) weight of each observation, aligned to
the same period index as the return data (e.g. `1 / rolling_variance`).
- <u>dependent_ticker (str &#124; None, optional):</u> The dependent (predicted) asset.
Defaults to None, meaning the Toolkit instance's first ticker.
- <u>independent_tickers (str &#124; list[str] &#124; None, optional):</u> The independent
(predictor) asset(s). Defaults to None, meaning every other ticker in
the Toolkit instance besides `dependent_ticker`.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" in the
default independent ticker(s) (has no effect when independent_tickers is given
explicitly). Defaults to False.
- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to regress on. Defaults to "Return".
- <u>add_constant (bool, optional):</u> Whether to include an intercept. Defaults to True.
- <u>cov_type (str, optional):</u> Which covariance estimator to use, applied to the weighted/
transformed problem -- see `get_ols`'s `cov_type` for the full list of options.
Defaults to "nonrobust".
- <u>clusters (pd.Series &#124; None, optional):</u> The cluster label for each observation,
required when `cov_type="cluster"`. Defaults to None.
- <u>maxlags (int &#124; None, optional):</u> The maximum lag to include when estimating the
HAC (Newey-West) covariance matrix, required when `cov_type="HAC"`. See
`get_ols`'s `maxlags` for the rule-of-thumb formula. Defaults to None.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.

**Returns:**

pd.DataFrame: A coefficient table (Coefficient, Std. Error, t-Statistic, P-Value),
indexed by regressor name.

**As an example:**

```python
import pandas as pd
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

returns = toolkit.econometrics._get_price_column("weekly", "Return")
weights = pd.Series(1.0, index=returns.index)

# AAPL (the first ticker) is dependent, MSFT is independent
toolkit.econometrics.get_wls(weights, period="weekly")
```

Which returns:

|           |   Coefficient |   Std. Error |   t-Statistic |   P-Value |
|:----------|--------------:|-------------:|--------------:|----------:|
| Intercept |        0.0012 |       0.0019 |        0.6332 |    0.5272 |
| MSFT      |        0.6281 |       0.058  |       10.8297 |    0      |

---

## get_gls
Fit a Generalized Least Squares (GLS) regression of `dependent_ticker` on `independent_tickers`, given a known error covariance structure `omega`.

GLS generalises WLS to an arbitrary error covariance matrix `Var(e) = sigma^2 * Omega`. Where WLS only corrects for heteroskedasticity (a diagonal `Omega`), GLS also corrects for correlation between the errors of different observations, such as the autocorrelation that is common in financial time series (a non-diagonal `Omega`):

- beta_hat = (X' Omega^-1 X)^-1 X' Omega^-1 y

Under a correctly specified `Omega` this is the most efficient linear unbiased estimator. Note that `omega` must be supplied, for example from a fitted AR(1) error structure: this performs the GLS estimation step itself, not the separate problem of estimating `Omega` (Feasible GLS). `get_durbin_watson_test` helps establish whether the residuals are autocorrelated in the first place.

For more information about the method, see the following paper:

- Aitken, A.C. (1935). "On Least Squares and Linear Combinations of Observations." Proceedings of the Royal Society of Edinburgh, 55, 42-48.

**Also known as:** GLS.

**Args:**

- <u>omega (pd.DataFrame):</u> The (symmetric, positive-definite) error covariance
structure, up to a scalar, shape `(n, n)`.
- <u>dependent_ticker (str &#124; None, optional):</u> The dependent (predicted) asset.
Defaults to None, meaning the Toolkit instance's first ticker.
- <u>independent_tickers (str &#124; list[str] &#124; None, optional):</u> The independent
(predictor) asset(s). Defaults to None, meaning every other ticker in
the Toolkit instance besides `dependent_ticker`.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" in the
default independent ticker(s) (has no effect when independent_tickers is given
explicitly). Defaults to False.
- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to regress on. Defaults to "Return".
- <u>add_constant (bool, optional):</u> Whether to include an intercept. Defaults to True.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.

**Returns:**

pd.DataFrame: A coefficient table (Coefficient, Std. Error, t-Statistic, P-Value),
indexed by regressor name.

**As an example:**

```python
import numpy as np
import pandas as pd
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

returns = toolkit.econometrics._get_price_column("weekly", "Return")
n = len(returns["AAPL"].dropna())
omega = pd.DataFrame(np.eye(n))

# AAPL (the first ticker) is dependent; MSFT is independent
toolkit.econometrics.get_gls(omega, period="weekly")
```

Which returns:

|           |   Coefficient |   Std. Error |   t-Statistic |   P-Value |
|:----------|--------------:|-------------:|--------------:|----------:|
| Intercept |        0.0012 |       0.0019 |        0.6332 |    0.5272 |
| MSFT      |        0.6281 |       0.058  |       10.8297 |    0      |

---

## get_logistic_regression
Fit a Logistic Regression (Logit model) of whether `dependent_ticker`'s return is positive on `independent_tickers`.

The dependent variable is turned into a binary outcome (1 when the return is positive, 0 otherwise) and the model estimates the probability of that outcome through the logistic (sigmoid) function, which maps any value onto the 0 to 1 range:

- P(y = 1 &#124; x) = 1 / (1 + e^(-x'beta))

The model is fitted by Maximum Likelihood. Coefficients are log-odds: a one-unit increase in an independent ticker changes the log-odds of a positive return by that coefficient, holding the others fixed, so a positive coefficient means a higher probability of a positive return. This answers "does this asset tend to be up when the others move this way" rather than "by how much", which is what `get_ols` estimates. `get_probit_regression` is the closely related alternative with a normal instead of a logistic link.

For more information about the method, see the following paper:

- Berkson, J. (1944). "Application of the Logistic Function to Bio-Assay." Journal of the American Statistical Association, 39(227), 357-365.

**Also known as:** logit model, logit regression.

**Args:**

- <u>dependent_ticker (str &#124; None, optional):</u> The dependent asset (whose
up/down direction is predicted). Defaults to None, meaning the Toolkit
instance's first ticker.
- <u>independent_tickers (str &#124; list[str] &#124; None, optional):</u> The independent
(predictor) asset(s). Defaults to None, meaning every other ticker in
the Toolkit instance besides `dependent_ticker`.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" in the
default independent ticker(s) (has no effect when independent_tickers is given
explicitly). Defaults to False.
- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to derive returns from. Defaults to
"Return".
- <u>add_constant (bool, optional):</u> Whether to include an intercept. Defaults to True.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.

**Returns:**

pd.DataFrame: A coefficient table (Coefficient, Std. Error, z-Statistic, P-Value),
indexed by regressor name.

**Notes:**

- The dependent variable is derived as `1` if the dependent ticker's return in the given
period is positive, `0` otherwise -- this method predicts the *direction*, not the
magnitude, of the dependent asset's return.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

# AAPL (the first ticker) is dependent; MSFT and Benchmark are independent
toolkit.econometrics.get_logistic_regression(
    independent_tickers=["MSFT", "Benchmark"], period="weekly"
)
```

Which returns:

|           |   Coefficient |   Std. Error |   z-Statistic |   P-Value |
|:----------|--------------:|-------------:|--------------:|----------:|
| Intercept |       -0.0124 |       0.1626 |       -0.0763 |    0.9392 |
| MSFT      |        6.8387 |       7.6454 |        0.8945 |    0.3711 |
| Benchmark |       89.7491 |      15.0025 |        5.9823 |    0      |

---

## get_probit_regression
Fit a Probit Regression of whether `dependent_ticker`'s return is positive on `independent_tickers`.

As with `get_logistic_regression`, the dependent variable is turned into a binary outcome (1 when the return is positive, 0 otherwise). The probability of that outcome is modelled through the standard normal cumulative distribution function instead of the logistic function:

- P(y = 1 &#124; x) = Phi(x'beta)

Where `Phi` is the standard normal CDF. The model is fitted by Maximum Likelihood. A positive coefficient means a higher probability of a positive return, but the size of a coefficient is not a log-odds ratio as in the Logit model. In practice Probit and Logit give very similar fitted probabilities; Probit is the convention in parts of the econometrics literature and underlies two-step estimators such as the Heckman selection correction.

For more information about the method, see the following paper:

- Bliss, C.I. (1934). "The Method of Probits." Science, 79(2037), 38-39.

**Also known as:** probit model.

**Args:**

- <u>dependent_ticker (str &#124; None, optional):</u> The dependent asset (whose
up/down direction is predicted). Defaults to None, meaning the Toolkit
instance's first ticker.
- <u>independent_tickers (str &#124; list[str] &#124; None, optional):</u> The independent
(predictor) asset(s). Defaults to None, meaning every other ticker in
the Toolkit instance besides `dependent_ticker`.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" in the
default independent ticker(s) (has no effect when independent_tickers is given
explicitly). Defaults to False.
- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to derive returns from. Defaults to
"Return".
- <u>add_constant (bool, optional):</u> Whether to include an intercept. Defaults to True.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.

**Returns:**

pd.DataFrame: A coefficient table (Coefficient, Std. Error, z-Statistic, P-Value),
indexed by regressor name.

**Notes:**

- The dependent variable is derived as `1` if the dependent ticker's return in the given
period is positive, `0` otherwise -- this method predicts the *direction*, not the
magnitude, of the dependent asset's return.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

# AAPL (the first ticker) is dependent; MSFT and Benchmark are independent
toolkit.econometrics.get_probit_regression(
    independent_tickers=["MSFT", "Benchmark"], period="weekly"
)
```

Which returns:

|           |   Coefficient |   Std. Error |   z-Statistic |   P-Value |
|:----------|--------------:|-------------:|--------------:|----------:|
| Intercept |       -0.0156 |       0.0946 |       -0.1652 |    0.8688 |
| MSFT      |        3.1338 |       4.2175 |        0.743  |    0.4575 |
| Benchmark |       52.7578 |       8.2654 |        6.383  |    0      |

---

## get_quantile_regression
Fit a Quantile Regression of `dependent_ticker` on `independent_tickers` at quantile `tau`.

Where OLS estimates how the average (conditional mean) of the dependent ticker depends on the independent tickers, Quantile Regression estimates how a chosen quantile of it does. It minimises an asymmetric ("pinball") loss that is smallest at the conditional `tau`-quantile:

- minimise SUM(tau * max(r_t, 0) + (1 - tau) * max(-r_t, 0)), with r_t = y_t - x_t'beta

With `tau = 0.5` this is the median regression, which is far less sensitive to outliers than OLS. Fitting at several quantiles (e.g. 0.05, 0.5 and 0.95) shows how the whole distribution of returns responds to the independent tickers, for example whether an asset's sensitivity to the market is larger in sell-offs (low quantiles) than in normal periods, which is directly relevant for downside risk.

For more information about the method, see the following paper:

- Koenker, R., & Bassett, G. (1978). "Regression Quantiles." Econometrica, 46(1), 33-50.

**Also known as:** QR.

**Args:**

- <u>dependent_ticker (str &#124; None, optional):</u> The dependent (predicted) asset.
Defaults to None, meaning the Toolkit instance's first ticker.
- <u>independent_tickers (str &#124; list[str] &#124; None, optional):</u> The independent
(predictor) asset(s). Defaults to None, meaning every other ticker in
the Toolkit instance besides `dependent_ticker`.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" in the
default independent ticker(s) (has no effect when independent_tickers is given
explicitly). Defaults to False.
- <u>tau (float, optional):</u> The quantile to fit, in (0, 1). Defaults to 0.5 (the median).
- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to regress on. Defaults to "Return".
- <u>add_constant (bool, optional):</u> Whether to include an intercept. Defaults to True.
- <u>n_bootstrap (int, optional):</u> The number of bootstrap resamples used for coefficient
standard errors, overriding `statsmodels`' default analytic (kernel density-based)
standard errors. Defaults to 0 (use the analytic standard errors).
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.

**Returns:**

pd.DataFrame: A coefficient table (Coefficient, Std. Error), indexed by regressor name.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

# AAPL (the first ticker) is dependent; MSFT and Benchmark are independent
toolkit.econometrics.get_quantile_regression(
    independent_tickers=["MSFT", "Benchmark"], tau=0.5, period="weekly"
)
```

Which returns:

|           |   Coefficient |   Std. Error |
|:----------|--------------:|-------------:|
| Intercept |       -0.0004 |       0.0017 |
| MSFT      |        0.1922 |       0.0732 |
| Benchmark |        0.9121 |       0.1089 |

---

## get_fama_macbeth_regression
Fit a Fama-MacBeth (1973) two-pass cross-sectional regression: `asset_tickers` is treated as the cross-section of test assets, `factor_tickers` as the risk factor(s) whose risk premia are estimated -- the standard procedure for testing whether a proposed risk factor is actually priced.

The method runs in two passes:

1. Time-series pass (per asset): regress each asset's returns on the factor(s) to estimate its factor loadings (betas).
2. Cross-sectional pass (per period): regress that period's returns of all assets on those betas, which gives one estimate of each factor's risk premium per period.
- First pass: R_i,t = alpha_i + beta_i' * F_t + e_i,t, for each asset i
- Second pass: R_i,t = gamma_0,t + gamma_t' * beta_i + u_i,t, for each period t
- Risk premium: gamma_hat = mean_t(gamma_t)
- Standard error: SE(gamma_hat) = std_t(gamma_t) / sqrt(T)

The risk premium is the average of the per-period estimates, and its standard error comes from how much those estimates vary over time. That is the method's key contribution: it accounts for correlation between the assets' residuals without having to model it. A significant positive premium means investors are compensated for exposure to the factor. This uses a single full-sample set of betas (the textbook variant), not the original rolling-window betas.

For more information about the method, see the following papers:

- Fama, E.F. & MacBeth, J.D. (1973). "Risk, Return, and Equilibrium: Empirical Tests." Journal of Political Economy, 81(3), 607-636.
- Cochrane, J.H. (2005). "Asset Pricing." Princeton University Press, Chapter 12.

**Also known as:** two-pass regression, Fama-MacBeth procedure.

**Args:**

- <u>factor_tickers (str &#124; list[str] &#124; None, optional):</u> The ticker(s) whose
returns are used as the risk factor(s) (e.g. "Benchmark" for a
single-factor/CAPM-style test). Defaults to None, meaning `["Benchmark"]`.
- <u>asset_tickers (str &#124; list[str] &#124; None, optional):</u> The ticker(s) forming the
cross-section of test assets. Defaults to None, meaning every Toolkit
ticker (including "Benchmark") not already used as a factor.
- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to regress on. Defaults to "Return".
- <u>add_constant (bool, optional):</u> Whether to include an intercept in the
second-pass cross-sectional regression. Defaults to True.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.

**Returns:**

pd.DataFrame: A coefficient table (Risk Premium, Std. Error, t-Statistic,
P-Value), indexed by factor name (plus "Intercept" if present).

**Notes:**

- The cross-sectional second pass needs strictly more assets than factors
(plus an intercept, if `add_constant=True`) to be identified -- with only a
couple of Toolkit tickers loaded, either pass `add_constant=False` or (better)
construct the Toolkit with many tickers, since Fama-MacBeth is fundamentally a
many-asset cross-sectional technique (dozens of assets is typical in practice),
not a limitation of this method's implementation.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

# Benchmark (the default factor) is the single risk factor; AAPL and MSFT
# are the test assets. add_constant=False since only 2 assets are available.
toolkit.econometrics.get_fama_macbeth_regression(
    period="weekly", add_constant=False
)
```

Which returns:

|           |   Risk Premium |   Std. Error |   t-Statistic |   P-Value |
|:----------|---------------:|-------------:|--------------:|----------:|
| Benchmark |         0.0032 |       0.0017 |        1.8775 |    0.0616 |

---

## get_two_sample_t_test
Calculate a two-sample t-test for a difference in mean `column` between every unordered pair of tickers in the Toolkit instance.

The test checks the null hypothesis that two samples come from distributions with the same mean, against the two-sided alternative that the means differ. Applied to returns it answers whether one asset has had a genuinely different average return than another, or whether the difference could be down to chance. By default this is Welch's t-test, which does not assume the two tickers have the same variance:

- t = (mean_a - mean_b) / sqrt(s_a^2 / n_a + s_b^2 / n_b)

With degrees of freedom from the Welch-Satterthwaite equation. Setting `equal_variance=True` pools the two variances instead (Student's t-test), which is slightly more powerful but only valid when the variances are truly equal. Welch's version is the safer default since assets rarely share the same volatility. A low p-value (e.g. below 0.05) means the difference in means is statistically significant.

For more information about the method, see the following papers:

- Student (1908). "The Probable Error of a Mean." Biometrika, 6(1), 1-25.
- Welch, B.L. (1947). "The Generalization of 'Student's' Problem when Several Different Population Variances are Involved." Biometrika, 34(1/2), 28-35.

**Also known as:** independent samples t-test, Welch's t-test (default), Student's t-test (`equal_variance=True`).

**Args:**

- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to compare. Defaults to "Return".
- <u>equal_variance (bool, optional):</u> Whether to assume the two samples share a common
variance (Student's pooled t-test) instead of Welch's (unequal-variance) t-test.
Defaults to False.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the
tickers paired up. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.

**Returns:**

pd.DataFrame: One row per unordered `(Ticker A, Ticker B)` pair, with the t-statistic,
degrees of freedom, its p-value, and the two sample means.

**Notes:**

- The two return series are compared as independent samples (not paired by date), which is
the standard use of a two-sample t-test -- if a date-by-date, paired comparison is needed
instead, take the difference of the two return series and run a one-sample test on it.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_two_sample_t_test(period="weekly")
```

Which returns:

|                  |   T-Statistic |   Degrees of Freedom |   P-Value |   Mean A |   Mean B |
|:-----------------|--------------:|---------------------:|----------:|---------:|---------:|
| ('AAPL', 'MSFT') |       -0.0515 |               511.12 |    0.9589 |   0.0036 |   0.0037 |

---

## get_f_test
Calculate a nested-model F-test for the joint significance of the regressors in `unrestricted_independent_tickers` that are not already in `restricted_independent_tickers`.

Two OLS regressions of `dependent_ticker` are fitted internally: a "restricted" one on `restricted_independent_tickers` and an "unrestricted" one that adds the extra tickers. The test checks the null hypothesis that the `q` extra tickers are jointly zero, i.e. that adding them does not explain the dependent ticker any better, by comparing how much the Residual Sum of Squares (RSS) drops when they are added:

- F = ((RSS_restricted - RSS_unrestricted) / q) / (RSS_unrestricted / (n - k_unrestricted))

Where `q = k_unrestricted - k_restricted` is the number of added regressors, `n` the number of observations and `k_unrestricted` the number of parameters of the larger model. Under the null, `F` follows an F(q, n - k_unrestricted) distribution. A low p-value means the extra tickers meaningfully improve the fit as a group, even when none of them is significant individually. `get_likelihood_ratio_test` is the asymptotic Maximum Likelihood counterpart.

**Also known as:** nested F-test, restricted vs. unrestricted F-test, partial F-test.

**Args:**

- <u>dependent_ticker (str):</u> The dependent (predicted) asset.
- <u>restricted_independent_tickers (str &#124; list[str]):</u> The independent asset(s) in the
restricted (smaller) model.
- <u>unrestricted_independent_tickers (str &#124; list[str]):</u> The independent asset(s) in the
unrestricted (larger) model -- must be a superset of `restricted_independent_tickers`.
- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>column (str, optional):</u> The historical data column to regress on. Defaults to "Return".
- <u>add_constant (bool, optional):</u> Whether to include an intercept in both models. Defaults
to True.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.

**Returns:**

pd.Series: The F-statistic, its numerator/denominator degrees of freedom, its p-value,
and whether the added regressors are jointly significant at the 5% level.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_f_test(
    "AAPL", "MSFT", ["MSFT", "Benchmark"], period="weekly"
)
```

Which returns:

|                          |       0 |
|:-------------------------|--------:|
| F-Statistic              | 104.748 |
| Df Numerator             |   1     |
| Df Denominator           | 257     |
| P-Value                  |   0     |
| Reject Restrictions (5%) |   1     |

---

## get_likelihood_ratio_test
Calculate a nested-model Likelihood Ratio (LR) test, the Maximum Likelihood analogue of `get_f_test`, for the joint significance of the regressors in `unrestricted_independent_tickers` that are not already in `restricted_independent_tickers`.

As with `get_f_test`, a "restricted" and an "unrestricted" OLS regression of `dependent_ticker` are fitted internally and the null hypothesis is that the `q` extra tickers are jointly zero. Instead of an F-statistic, the two models are compared through the ratio of their likelihoods, which for linear models with normal errors reduces to a function of the two Residual Sums of Squares (RSS):

- LR = n * ln(RSS_restricted / RSS_unrestricted)

Under the null this is asymptotically chi-squared distributed with `q` degrees of freedom. Where the F-test is exact in small samples under the classical assumptions, the LR test relies on a large-sample approximation: both agree for long return histories and can differ somewhat for short ones. A low p-value means the extra tickers meaningfully improve the model.

For more information about the method, see the following paper:

- Wilks, S.S. (1938). "The Large-Sample Distribution of the Likelihood Ratio for Testing Composite Hypotheses." Annals of Mathematical Statistics, 9(1), 60-62.

**Also known as:** LR test, Wilks' likelihood ratio test.

**Args:**

- <u>dependent_ticker (str):</u> The dependent (predicted) asset.
- <u>restricted_independent_tickers (str &#124; list[str]):</u> The independent asset(s) in the
restricted (smaller) model.
- <u>unrestricted_independent_tickers (str &#124; list[str]):</u> The independent asset(s) in the
unrestricted (larger) model -- must be a superset of `restricted_independent_tickers`.
- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>column (str, optional):</u> The historical data column to regress on. Defaults to "Return".
- <u>add_constant (bool, optional):</u> Whether to include an intercept in both models. Defaults
to True.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.

**Returns:**

pd.Series: The LR statistic, its degrees of freedom, its p-value, and whether the added
regressors are jointly significant at the 5% level.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_likelihood_ratio_test(
    "AAPL", "MSFT", ["MSFT", "Benchmark"], period="weekly"
)
```

Which returns:

|                          |       0 |
|:-------------------------|--------:|
| LR Statistic             | 88.8863 |
| Degrees of Freedom       |  1      |
| P-Value                  |  0      |
| Reject Restrictions (5%) |  1      |

---

## get_wald_test
Calculate a Wald test of `q` general linear restriction(s) on the coefficients of an OLS regression of `dependent_ticker` on `independent_tickers`.

A single OLS regression is fitted internally and the test checks the null hypothesis `H0: R @ beta = r`, where `R` (`restriction_matrix`) encodes `q` linear restrictions on the coefficients and `r` (`restriction_values`) holds their hypothesised values (zero by default). This generalises the t-test reported for each coefficient to combinations of coefficients, for example that two coefficients are jointly zero, that a coefficient equals a specific value (such as a beta of exactly 1), or that two tickers have the same coefficient:

- W = (R @ beta_hat - r)' @ (R @ Cov(beta_hat) @ R')^-1 @ (R @ beta_hat - r)

Which is asymptotically chi-squared distributed with `q` degrees of freedom. `W / q` is reported alongside it as an F-statistic for small samples; for a single restriction it equals the squared t-statistic of that coefficient. A low p-value means the data reject the restriction(s).

For more information about the method, see the following paper:

- Wald, A. (1943). "Tests of Statistical Hypotheses Concerning Several Parameters When the Number of Observations is Large." Transactions of the American Mathematical Society, 54(3), 426-482.

**Also known as:** Wald chi-squared test.

**Args:**

- <u>restriction_matrix (pd.DataFrame &#124; np.ndarray):</u> The `(q, k)` restriction matrix `R`, one
row per restriction, one column per coefficient in the same order as `add_constant`
(if True, "Intercept" first) followed by the independent ticker(s).
- <u>dependent_ticker (str &#124; None, optional):</u> The dependent (predicted) asset.
Defaults to None, meaning the Toolkit instance's first ticker.
- <u>independent_tickers (str &#124; list[str] &#124; None, optional):</u> The independent
(predictor) asset(s), in the order the restriction matrix's columns
(after "Intercept", if `add_constant`) refer to them. Defaults to None,
meaning every other ticker in the Toolkit instance besides
`dependent_ticker`.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" in the
default independent ticker(s) (has no effect when independent_tickers is given
explicitly). Defaults to False.
- <u>restriction_values (pd.Series &#124; np.ndarray &#124; None, optional):</u> The length-`q` vector of
hypothesized values. Defaults to None, i.e. all restrictions equal zero.
- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>column (str, optional):</u> The historical data column to regress on. Defaults to "Return".
- <u>add_constant (bool, optional):</u> Whether to include an intercept. Defaults to True.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.

**Returns:**

pd.Series: The Wald (chi-squared) statistic and its p-value, the small-sample F-statistic
and its p-value, the number of restrictions, and whether they are rejected at the 5% level.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

# H0: the coefficients on both MSFT and Benchmark are jointly zero.
toolkit.econometrics.get_wald_test(
    restriction_matrix=[[0, 1, 0], [0, 0, 1]],
    independent_tickers=["MSFT", "Benchmark"],
    period="weekly",
)
```

Which returns:

|                          |       0 |
|:-------------------------|--------:|
| Wald Statistic (Chi2)    | 269.191 |
| Chi2 P-Value             |   0     |
| F-Statistic              | 134.595 |
| F P-Value                |   0     |
| Restrictions (q)         |   2     |
| Reject Restrictions (5%) |   1     |

---

## get_hausman_wu_test
Calculate a regression-based Hausman-Wu test for the endogeneity of `suspect_ticker` in a regression of `dependent_ticker` on `suspect_ticker` (and, optionally, `other_independent_tickers`), using `instrument_tickers` as instruments for `suspect_ticker`.

OLS requires every regressor to be uncorrelated with the error term. When that fails, for example because of an omitted common driver, reverse causality or measurement error, the regressor is "endogenous" and OLS is biased; an instrumental-variables approach such as `get_iv_2sls` is then needed. This test checks whether that is the case before committing to a full IV fit, using two auxiliary OLS regressions:

1. Regress `suspect_ticker` on the instruments (and the other tickers, if given) and keep the residuals: the part of `suspect_ticker` that the instruments do not explain.
2. Regress `dependent_ticker` on `suspect_ticker`, those residuals (and the other tickers) and test whether the coefficient on the residuals is zero.

If `suspect_ticker` is exogenous the residuals add no information, so their coefficient should be statistically zero. A low p-value is evidence that `suspect_ticker` is endogenous and that the OLS estimate is unreliable. The test is only as good as the instruments: they must be correlated with `suspect_ticker` but not with the error term.

For more information about the method, see the following papers:

- Wu, D-M. (1973). "Alternative Tests of Independence Between Stochastic Regressors and Disturbances." Econometrica, 41(4), 733-750.
- Hausman, J.A. (1978). "Specification Tests in Econometrics." Econometrica, 46(6), 1251-1271.

**Also known as:** Hausman test, Durbin-Wu-Hausman test, regression test for endogeneity.

**Args:**

- <u>dependent_ticker (str):</u> The dependent (predicted) asset.
- <u>suspect_ticker (str):</u> The (possibly endogenous) asset being tested.
- <u>instrument_tickers (str &#124; list[str]):</u> One or more instrument asset(s) for
`suspect_ticker` -- assets correlated with `suspect_ticker` but assumed uncorrelated
with `dependent_ticker`'s error term.
- <u>other_independent_tickers (str &#124; list[str] &#124; None, optional):</u> Any other (assumed
exogenous) independent asset(s) to include. Defaults to None.
- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to regress on. Defaults to "Return".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.

**Returns:**

pd.Series: The coefficient on the first-stage residuals, its t-statistic and p-value, and
whether `suspect_ticker` is flagged as endogenous at the 5% level.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_hausman_wu_test(
    "AAPL", "MSFT", "Benchmark", period="weekly"
)
```

Which returns:

|                    |        0 |
|:-------------------|---------:|
| V-Hat Coefficient  |  -1.0052 |
| T-Statistic        | -10.2346 |
| Degrees of Freedom | 257      |
| P-Value            |   0      |
| Endogenous (5%)    |   1      |

---

## get_breusch_pagan_test
Calculate the Breusch-Pagan test for heteroskedasticity of a regression of `dependent_ticker` on `independent_tickers`.

OLS standard errors assume that the residual variance is constant (homoskedasticity). The test regresses the squared residuals of the regression on the original independent tickers and checks whether they explain any of the residual variance, by testing whether the R-squared of that auxiliary regression is significantly different from zero:

- LM = n * R^2_auxiliary

Which is asymptotically chi-squared distributed with `k - 1` degrees of freedom under the null hypothesis of homoskedasticity, where `k` is the number of parameters of the auxiliary regression. A low p-value means the residual variance moves with the independent tickers (for example, errors grow when the market moves more), so the regression's standard errors, t-statistics and p-values are unreliable even though the coefficients themselves remain unbiased. Remedies are a robust `cov_type` in `get_ols` or `get_wls`. `get_white_test` is a more general alternative that also catches non-linear forms of heteroskedasticity.

For more information about the method, see the following paper:

- Breusch, T.S., & Pagan, A.R. (1979). "A Simple Test for Heteroscedasticity and Random Coefficient Variation." Econometrica, 47(5), 1287-1294.

**Also known as:** BP test, Breusch-Pagan-Godfrey test.

**Args:**

- <u>dependent_ticker (str &#124; None, optional):</u> The dependent (predicted) asset.
Defaults to None, meaning the Toolkit instance's first ticker.
- <u>independent_tickers (str &#124; list[str] &#124; None, optional):</u> The independent
(predictor) asset(s). Defaults to None, meaning every other ticker in
the Toolkit instance besides `dependent_ticker`.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" in the
default independent ticker(s) (has no effect when independent_tickers is given
explicitly). Defaults to False.
- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>column (str, optional):</u> The historical data column to regress on. Defaults to "Return".
- <u>add_constant (bool, optional):</u> Whether to include an intercept in the underlying
regression. Defaults to True.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.

**Returns:**

pd.Series: The Breusch-Pagan LM statistic, its p-value, and whether homoskedasticity is
rejected at the 5% level.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

# AAPL (the first ticker) is dependent; MSFT and Benchmark are independent
toolkit.econometrics.get_breusch_pagan_test(
    independent_tickers=["MSFT", "Benchmark"], period="weekly"
)
```

Which returns:

|                              |      0 |
|:-----------------------------|-------:|
| Breusch-Pagan Statistic      | 0.2068 |
| P-Value                      | 0.9018 |
| Reject Homoskedasticity (5%) | 0      |

---

## get_white_test
Calculate White's test for heteroskedasticity of a regression of `dependent_ticker` on `independent_tickers`.

A more general version of `get_breusch_pagan_test`. Instead of regressing the squared residuals on only the original independent tickers, the auxiliary regression uses each ticker, its square and every pairwise cross-product:

- e_t^2 = a_0 + SUM_i(a_i * x_it) + SUM_i(b_i * x_it^2) + SUM_{i<j}(c_ij * x_it * x_jt) + v_t

The test statistic is `LM = n * R^2_auxiliary`, chi-squared distributed with degrees of freedom equal to the number of terms in the auxiliary regression, under the null hypothesis of homoskedasticity (constant residual variance). A low p-value means the regression's standard errors are unreliable and a robust `cov_type` should be used. Because it also detects non-linear patterns in the residual variance, White's test makes fewer assumptions than Breusch-Pagan, at the cost of power when there are many independent tickers, since the number of auxiliary terms grows quadratically.

For more information about the method, see the following paper:

- White, H. (1980). "A Heteroskedasticity-Consistent Covariance Matrix Estimator and a Direct Test for Heteroskedasticity." Econometrica, 48(4), 817-838.

**Also known as:** White's general test.

**Args:**

- <u>dependent_ticker (str &#124; None, optional):</u> The dependent (predicted) asset.
Defaults to None, meaning the Toolkit instance's first ticker.
- <u>independent_tickers (str &#124; list[str] &#124; None, optional):</u> The independent
(predictor) asset(s). Defaults to None, meaning every other ticker in
the Toolkit instance besides `dependent_ticker`.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" in the
default independent ticker(s) (has no effect when independent_tickers is given
explicitly). Defaults to False.
- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>column (str, optional):</u> The historical data column to regress on. Defaults to "Return".
- <u>add_constant (bool, optional):</u> Whether to include an intercept in the underlying
regression. Defaults to True.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.

**Returns:**

pd.Series: White's LM statistic, its p-value, and whether homoskedasticity is rejected at
the 5% level.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

# AAPL (the first ticker) is dependent; MSFT and Benchmark are independent
toolkit.econometrics.get_white_test(
    independent_tickers=["MSFT", "Benchmark"], period="weekly"
)
```

Which returns:

|                              |      0 |
|:-----------------------------|-------:|
| White Statistic              | 1.5118 |
| P-Value                      | 0.9117 |
| Reject Homoskedasticity (5%) | 0      |

---

## get_durbin_watson_test
Calculate the Durbin-Watson statistic for first-order autocorrelation in the residuals of a regression of `dependent_ticker` on `independent_tickers`.

OLS standard errors assume that the residuals of consecutive periods are uncorrelated. The Durbin-Watson statistic compares each residual with the one before it:

- DW = SUM_{t=2}^{n}((e_t - e_(t-1))^2) / SUM_{t=1}^{n}(e_t^2)

The statistic ranges from 0 to 4. A value near 2 means no first-order autocorrelation; values below 2 point to positive autocorrelation (consecutive residuals tend to share the same sign, often a sign of an omitted trend or lagged effect) and values above 2 to negative autocorrelation (residuals tend to alternate in sign). Like heteroskedasticity, autocorrelation leaves the coefficients unbiased but makes the standard errors unreliable; a "HAC" `cov_type` in `get_ols`, or `get_gls` with an AR(1) `omega`, are common remedies. There is no exact p-value: the returned interpretation is a rule of thumb (below 1.5 is likely positive, above 2.5 likely negative autocorrelation).

For more information about the method, see the following paper:

- Durbin, J., & Watson, G.S. (1950). "Testing for Serial Correlation in Least Squares Regression I." Biometrika, 37(3/4), 409-428.

**Also known as:** DW statistic.

**Args:**

- <u>dependent_ticker (str &#124; None, optional):</u> The dependent (predicted) asset.
Defaults to None, meaning the Toolkit instance's first ticker.
- <u>independent_tickers (str &#124; list[str] &#124; None, optional):</u> The independent
(predictor) asset(s). Defaults to None, meaning every other ticker in
the Toolkit instance besides `dependent_ticker`.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" in the
default independent ticker(s) (has no effect when independent_tickers is given
explicitly). Defaults to False.
- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>column (str, optional):</u> The historical data column to regress on. Defaults to "Return".
- <u>add_constant (bool, optional):</u> Whether to include an intercept in the underlying
regression. Defaults to True.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.

**Returns:**

pd.Series: The Durbin-Watson statistic and an approximate interpretation flag.

**Notes:**

- Unlike the other tests in this module, this does not carry a formal p-value/reject flag at a
stated significance level -- see `specification_tests_model.get_durbin_watson_test` for why.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

# AAPL (the first ticker) is dependent; MSFT and Benchmark are independent
toolkit.econometrics.get_durbin_watson_test(
    independent_tickers=["MSFT", "Benchmark"], period="weekly"
)
```

Which returns:

|                         | 0                  |
|:------------------------|:-------------------|
| Durbin-Watson Statistic | 2.1372             |
| Interpretation          | No Strong Evidence |

---

## get_vif
Calculate the Variance Inflation Factor (VIF) of every ticker in the Toolkit instance, treated as regressors against one another.

Multicollinearity, where one regressor can (nearly) be predicted from the others, does not bias regression coefficients but inflates their standard errors. Individual coefficients can then look insignificant, and swing wildly between samples, even when the regressors jointly explain the dependent variable well. VIF measures this for each ticker by regressing it on all the other tickers:

- VIF_i = 1 / (1 - R^2_i)

Where `R^2_i` is the R-squared of regressing ticker `i` on all other tickers. A VIF of 1 means the ticker is uncorrelated with the others; a VIF of `V` means the variance of its coefficient is `V` times larger than it would be without multicollinearity. As a rule of thumb, a VIF above 10 (or above 5 for a stricter cutoff) signals problematic multicollinearity. This is common with assets that move closely together, such as several stocks from the same sector, and is worth checking before using them together as independent tickers in `get_ols` or the other regression methods.

**Also known as:** VIF.

**Args:**

- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to use. Defaults to "Return".
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the
regressors tested. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.

**Returns:**

pd.Series: The VIF of each asset, indexed by ticker.

**Notes:**

- Unlike the other methods in this module, `get_vif` has no `dependent_ticker` -- VIF is a
property of the regressors alone, independent of any particular dependent variable.
- `VIF > 10` is the conventional rule-of-thumb threshold for concerning multicollinearity.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_vif(period="weekly")
```

Which returns:

|      |    VIF |
|:-----|-------:|
| AAPL | 1.4546 |
| MSFT | 1.4546 |

---

## get_ramsey_reset_test
Calculate Ramsey's RESET test for functional form misspecification of a regression of `dependent_ticker` on `independent_tickers`.

If the true relationship is non-linear, or a relevant transformation or variable is missing, the fitted values of a linear regression still carry information about that missing piece. RESET tests for this by adding powers of the fitted values (`fitted^2`, ..., `fitted^power`) to the regression and checking whether they are jointly significant with an F-test that compares the original (restricted) and augmented (unrestricted) model:

- F = ((RSS_r - RSS_u) / q) / (RSS_u / (n - k_u))

Where `RSS_r` and `RSS_u` are the residual sums of squares of both models, `q` is the number of added terms (`power - 1`), `n` the number of observations and `k_u` the number of parameters of the augmented model. Under the null hypothesis that the linear form is correct, `F` follows an F(q, n - k_u) distribution. A low p-value suggests the model is missing something, for example a squared or interaction term or a log transformation, without saying what; it is a signal to reconsider the specification, not a prescription.

For more information about the method, see the following paper:

- Ramsey, J.B. (1969). "Tests for Specification Errors in Classical Linear Least-Squares Regression Analysis." Journal of the Royal Statistical Society, Series B, 31(2), 350-371.

**Also known as:** RESET test, Ramsey RESET.

**Args:**

- <u>dependent_ticker (str &#124; None, optional):</u> The dependent (predicted) asset.
Defaults to None, meaning the Toolkit instance's first ticker.
- <u>independent_tickers (str &#124; list[str] &#124; None, optional):</u> The independent
(predictor) asset(s). Defaults to None, meaning every other ticker in
the Toolkit instance besides `dependent_ticker`.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" in the
default independent ticker(s) (has no effect when independent_tickers is given
explicitly). Defaults to False.
- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>column (str, optional):</u> The historical data column to regress on. Defaults to "Return".
- <u>add_constant (bool, optional):</u> Whether to include an intercept in the underlying
regression. Defaults to True.
- <u>power (int, optional):</u> The highest power of the fitted values to add. Defaults to 3.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.

**Returns:**

pd.Series: The RESET F-statistic, its p-value, and whether correct specification is
rejected at the 5% level.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

# AAPL (the first ticker) is dependent; MSFT and Benchmark are independent
toolkit.econometrics.get_ramsey_reset_test(
    independent_tickers=["MSFT", "Benchmark"], period="weekly"
)
```

Which returns:

|                                   |      0 |
|:----------------------------------|-------:|
| RESET F-Statistic                 | 0.7233 |
| P-Value                           | 0.4861 |
| Reject Correct Specification (5%) | 0      |

---

## get_chow_test
Calculate the Chow test for a structural break at `break_date` in a regression of `dependent_ticker` on `independent_tickers`.

The sample is split at `break_date` into a "before" and "after" period, a regression is fitted on each part separately and on the full sample, and an F-test checks whether allowing the coefficients to differ between the two periods significantly reduces the residual sum of squares:

- F = ((RSS_pooled - (RSS_1 + RSS_2)) / k) / ((RSS_1 + RSS_2) / (n - 2k))

Where `RSS_pooled` is the residual sum of squares of the full-sample regression, `RSS_1` and `RSS_2` those of the two sub-periods, `k` the number of parameters and `n` the total number of observations. Under the null hypothesis of no structural break (the same coefficients apply throughout), `F` follows an F(k, n - 2k) distribution. A low p-value means the relationship changed at `break_date`, for example an asset's beta shifting after a merger, a regulatory change or a market regime change, so a single regression over the full sample is misspecified. The break date must be chosen in advance; testing many candidate dates and keeping the most significant overstates the evidence.

For more information about the method, see the following paper:

- Chow, G.C. (1960). "Tests of Equality Between Sets of Coefficients in Two Linear Regressions." Econometrica, 28(3), 591-605.

**Also known as:** Chow breakpoint test.

**Args:**

- <u>break_date (str):</u> The date (e.g. "2021-06-30") at which to split the sample -- all
periods starting on or after this date form the "after" sub-sample, everything
before it forms the "before" sub-sample.
- <u>dependent_ticker (str &#124; None, optional):</u> The dependent (predicted) asset.
Defaults to None, meaning the Toolkit instance's first ticker.
- <u>independent_tickers (str &#124; list[str] &#124; None, optional):</u> The independent
(predictor) asset(s). Defaults to None, meaning every other ticker in
the Toolkit instance besides `dependent_ticker`.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" in the
default independent ticker(s) (has no effect when independent_tickers is given
explicitly). Defaults to False.
- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to regress on. Defaults to "Return".
- <u>add_constant (bool, optional):</u> Whether to include an intercept in the underlying
regression(s). Defaults to True.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.

**Returns:**

pd.Series: The Chow F-statistic, its p-value, and whether no structural break is rejected
at the 5% level.

**Raises:**

ValueError: If `break_date` does not leave enough observations on either side of the
split to estimate the regression's parameters.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

# AAPL (the first ticker) is dependent; MSFT and Benchmark are independent
toolkit.econometrics.get_chow_test(
    break_date="2021-06-30",
    independent_tickers=["MSFT", "Benchmark"],
    period="weekly",
)
```

Which returns:

|                                 |      0 |
|:--------------------------------|-------:|
| Chow F-Statistic                | 3.6234 |
| P-Value                         | 0.0137 |
| Reject No Structural Break (5%) | 1      |

---

## get_iv_2sls
Fit an Instrumental Variables regression via Two-Stage Least Squares (2SLS) of `dependent_ticker` on `endogenous_ticker`, instrumented by `instrument_tickers`.

**Also known as:** IV, 2SLS, IV-2SLS.

For more information about the method, and why plain OLS on an asset suspected of reverse-causality/omitted-confounder bias against another asset is unreliable, see `causal_inference_model.get_iv_2sls`.

A natural use case in a multi-asset return panel: suppose `endogenous_ticker`'s return is suspected to be simultaneously determined together with `dependent_ticker`'s return (e.g. two closely related assets that react to each other intraday, or one asset's return partly reflects news about the other) -- plain OLS of one on the other is then biased. An `instrument_tickers` asset that moves `endogenous_ticker` for reasons unrelated to `dependent_ticker`'s own error term (e.g. a supplier/peer whose moves affect `endogenous_ticker` but only reach `dependent_ticker`, if at all, THROUGH `endogenous_ticker`) allows recovering a cleaner estimate of the causal pass-through.

**Args:**

- <u>dependent_ticker (str):</u> The dependent (predicted) asset.
- <u>endogenous_ticker (str &#124; list[str]):</u> The endogenous regressor asset(s) --
suspected correlated with the error term.
- <u>instrument_tickers (str &#124; list[str]):</u> The excluded instrument asset(s),
correlated with `endogenous_ticker` but assumed uncorrelated with the error
term. Must supply at least as many instruments as endogenous regressors.
- <u>exogenous_tickers (str &#124; list[str] &#124; None, optional):</u> Other, non-instrumented
control asset(s) included as-is in both stages. Defaults to None.
- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to regress on. Defaults to
"Return".
- <u>add_constant (bool, optional):</u> Whether to include an intercept. Defaults to True.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None.

**Returns:**

pd.DataFrame: A coefficient table (Coefficient, CORRECTED Std. Error, t-Statistic,
P-Value), indexed by regressor name -- see `causal_inference_model.get_iv_2sls` for
why these standard errors differ from (and correct) what a naive two-OLS-calls
approach would report.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_iv_2sls("AAPL", "MSFT", "Benchmark", period="weekly")
```

Which returns:

|           |   Coefficient |   Std. Error |   t-Statistic |   P-Value |
|:----------|--------------:|-------------:|--------------:|----------:|
| Intercept |       -0.0005 |       0.0022 |       -0.2361 |    0.8135 |
| MSFT      |        1.0951 |       0.0887 |       12.3511 |    0      |

---

## get_difference_in_differences
Fit a Difference-in-Differences (DiD) regression estimating the effect of some event on `treatment_date` for `treated_tickers`, relative to `control_tickers`.

**Also known as:** DiD, DD, difference-in-differences estimator.

For more information about the method, and why the `Treated x Post` interaction coefficient IS the DiD treatment-effect estimate, see `causal_inference_model.get_difference_in_differences`.

Builds a stacked (ticker, date) panel from every ticker in `treated_tickers` and `control_tickers`: each observation's outcome is that ticker's return on that date, `Treated` is 1 for every observation belonging to a `treated_tickers` asset (regardless of date) and 0 for `control_tickers` assets, and `Post` is 1 for observations on or after `treatment_date` (regardless of asset). This answers "did `treated_tickers` behave differently after `treatment_date`, beyond both their normal average gap versus `control_tickers` and the common market-wide move over that same before/after window?" -- e.g. isolating the effect of an event (an index-inclusion announcement, a regulatory change affecting only some tickers, an earnings surprise) that hits `treated_tickers` but not `control_tickers`, at a known date.

**Args:**

- <u>treated_tickers (str &#124; list[str]):</u> The asset(s) subject to the event/treatment.
- <u>treatment_date (str):</u> The date the event/treatment occurs, in the same format
accepted by `pd.Timestamp`. Observations on or after this date are `Post = 1`.
- <u>control_tickers (str &#124; list[str] &#124; None, optional):</u> The untreated comparison
asset(s). Defaults to None, which uses every ticker (and "Benchmark", if
present) NOT in `treated_tickers`.
- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to use as the outcome.
Defaults to "Return".
- <u>add_constant (bool, optional):</u> Whether to include an intercept. Defaults to True.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None.

**Returns:**

pd.DataFrame: A coefficient table (Coefficient, Std. Error, t-Statistic, P-Value)
with rows `Intercept`, `Treated`, `Post` and `Treated x Post` -- the last of
which is the DiD treatment-effect estimate.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_difference_in_differences(
    treated_tickers="AAPL", treatment_date="2021-06-30", period="weekly"
)
```

Which returns:

|                |   Coefficient |   Std. Error |   t-Statistic |   P-Value |
|:---------------|--------------:|-------------:|--------------:|----------:|
| Intercept      |        0.0078 |       0.0045 |        1.7302 |    0.084  |
| Treated        |       -0.0047 |       0.0078 |       -0.6015 |    0.5477 |
| Post           |       -0.005  |       0.0047 |       -1.0591 |    0.2899 |
| Treated x Post |        0.0056 |       0.0082 |        0.6779 |    0.498  |

---

## get_regression_discontinuity
Estimate a Sharp Regression Discontinuity (RDD): the jump in `dependent_ticker` exactly where `running_variable_ticker` crosses `cutoff`.

**Also known as:** RDD, sharp RD.

For more information about the method, see `causal_inference_model.get_regression_discontinuity`.

Treats `running_variable_ticker`'s value as the running variable that (hypothetically) triggers some discrete change once it crosses `cutoff` -- e.g. testing whether `dependent_ticker`'s return behaves discontinuously around a round-number/threshold level of another asset or indicator (a psychological price level, an index-inclusion market-cap threshold, a macro indicator's policy-relevant threshold) fed in as `running_variable_ticker`. Fits separate local linear regressions of `dependent_ticker`'s return on the (cutoff-centered) `running_variable_ticker` value, one on each side of `cutoff`, and reports the gap between the two fitted lines exactly at the cutoff.

**Args:**

- <u>dependent_ticker (str):</u> The outcome asset.
- <u>running_variable_ticker (str):</u> The asset (or column) whose value determines
which side of `cutoff` an observation falls on.
- <u>cutoff (float):</u> The threshold value of `running_variable_ticker` at which the
discontinuity is estimated.
- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to use for both series.
Defaults to "Return".
- <u>bandwidth (float &#124; None, optional):</u> The maximum distance from `cutoff` an
observation may be to be included in either local regression. Defaults to
None, which uses half of the running variable's observed range -- see
`causal_inference_model.get_regression_discontinuity` for why this is a
deliberately naive default.
- <u>kernel (str, optional):</u> One of "uniform" or "triangular". Defaults to "uniform".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None.

**Returns:**

pd.DataFrame: A one-column results table with the discontinuity estimate, its
standard error/t-statistic/p-value, and the cutoff/bandwidth/sample sizes used.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_regression_discontinuity(
    "AAPL", "MSFT", cutoff=0.0, period="weekly"
)
```

Which returns:

|               |    Value |
|:--------------|---------:|
| Discontinuity |  -0.0009 |
| Std. Error    |   0.0067 |
| t-Statistic   |  -0.1394 |
| P-Value       |   0.8892 |
| Cutoff        |   0      |
| Bandwidth     |   0.0993 |
| N Left        | 116      |
| N Right       | 141      |

---

## get_propensity_score_matching
Estimate the Average Treatment effect on the Treated (ATT) of `treatment_ticker` exceeding `treatment_threshold` on `dependent_ticker`'s return, via Propensity Score Matching (PSM) on `covariate_tickers`.

**Also known as:** PSM, nearest-neighbor propensity matching.

For more information about the method, see `causal_inference_model.get_propensity_score_matching`.

Derives a binary "treatment" indicator the same way `get_logistic_regression` derives its binary outcome: 1 if `treatment_ticker`'s return in a given period exceeds `treatment_threshold` (0.0, i.e. a positive return, by default), else 0. This lets PSM answer e.g. "on periods where `treatment_ticker` has an outsized/positive move, is `dependent_ticker`'s return different than it would otherwise be -- comparing only periods that LOOK similar on `covariate_tickers` (to control for the possibility that `treatment_ticker` tends to move on the same periods/regimes that also independently affect `dependent_ticker`)?"

**Args:**

- <u>dependent_ticker (str):</u> The outcome asset.
- <u>treatment_ticker (str):</u> The asset whose return, once it exceeds
`treatment_threshold`, defines the treatment indicator.
- <u>covariate_tickers (str &#124; list[str]):</u> The asset(s) used as covariates to
estimate the propensity score -- should include asset(s) believed to drive
selection into "treatment".
- <u>treatment_threshold (float, optional):</u> The return threshold defining
treatment. Defaults to 0.0.
- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to use. Defaults to "Return".
- <u>caliper (float &#124; None, optional):</u> The maximum allowed logit-propensity-score
matching distance. Defaults to None, which uses Austin's (2011) rule of thumb
-- see `causal_inference_model.get_propensity_score_matching`.
- <u>add_constant (bool, optional):</u> Whether to include an intercept in the
propensity score model. Defaults to True.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None.

**Returns:**

pd.Series: The ATT estimate, its standard error/t-statistic/p-value, and the
number of matched pairs/treated/control observations.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_propensity_score_matching(
    "AAPL", "MSFT", "Benchmark", period="weekly"
)
```

Which returns:

|               |        0 |
|:--------------|---------:|
| ATT           |   0.0078 |
| Std. Error    |   0.0054 |
| t-Statistic   |   1.4538 |
| P-Value       |   0.1516 |
| Matched Pairs |  57      |
| N Treated     | 144      |
| N Control     | 116      |

---

## get_synthetic_control
Construct a Synthetic Control for `treated_ticker` from a weighted combination of `donor_tickers` (Abadie, Diamond & Hainmueller, 2010), and estimate the effect of an event/intervention as the post-`treatment_period` gap between `treated_ticker`'s actual and synthetic counterfactual return path.

When a single company or market experiences an event (an acquisition, a regulatory change, an index inclusion) and there is no single obvious comparison, the synthetic control builds one from the data: a weighted average of unaffected "donor" tickers, with weights chosen so it tracks the treated ticker as closely as possible before the event. If that pre-event fit is good, the synthetic control's path after the event estimates what would have happened without it, and the gap is the estimated effect:

- Weights: w* = argmin_w &#124;&#124;treated_pre - donors_pre @ w&#124;&#124;^2, subject to w >= 0 and sum(w) = 1
- Synthetic control: synthetic_t = donors_t @ w*, for every period t
- Treatment effect: gap_t = treated_t - synthetic_t, for every post-event period t

Unlike difference-in-differences, this does not require the treated and comparison units to follow parallel trends, as the synthetic control is built to match the treated ticker's own pre-event path. Because there is only one treated unit, the p-value comes from placebo tests: the procedure is rerun with each donor as if it were treated, and the treated ticker's post/pre fit ratio is compared with theirs. Matching is done on the pre-event outcome path only, a common simplification of the original method.

For more information about the method, see the following papers:

- Abadie, A., Diamond, A., & Hainmueller, J. (2010). "Synthetic Control Methods for Comparative Case Studies: Estimating the Effect of California's Tobacco Control Program." Journal of the American Statistical Association, 105(490), 493-505.
- Abadie, A. (2021). "Using Synthetic Controls: Feasibility, Data Requirements, and Methodological Aspects." Journal of Economic Literature, 59(2), 391-425.

**Also known as:** SCM, synthetic control method.

**Args:**

- <u>treated_ticker (str):</u> The asset believed to be affected by an event/
intervention starting at `treatment_period`.
- <u>treatment_period (str):</u> The first post-treatment period -- periods at or
after this value (within `period`'s index) are treated as post-treatment,
everything before as pre-treatment (used to fit the synthetic control's
weights).
- <u>donor_tickers (str &#124; list[str] &#124; None, optional):</u> The ticker(s) forming
the donor pool the synthetic control is built from. Defaults to None,
meaning every other Toolkit ticker (subject to `include_benchmark`).
- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to use. Defaults to "Return".
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" in the
default donor pool (has no effect when donor_tickers is given explicitly).
Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.

**Returns:**

pd.Series: The average post-treatment effect, pre/post RMSPE and their
ratio, the placebo-based p-value, and the donor pool/period counts.

**Notes:**

- Needs at least 2 donor tickers -- with only 1-2 Toolkit tickers loaded,
pass `donor_tickers` explicitly (e.g. including "Benchmark") or (better)
construct the Toolkit with more tickers, since small donor pools give both a
poorly-identified synthetic control and a very coarse placebo p-value (with
`k` donors, the smallest achievable p-value is `1 / (k + 1)`).

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_synthetic_control(
    "AAPL",
    treatment_period="2021-07-01",
    donor_tickers=["MSFT", "Benchmark"],
    period="weekly",
)
```

Which returns:

|                          |        0 |
|:-------------------------|---------:|
| Average Treatment Effect |   0.0008 |
| Pre-Treatment RMSPE      |   0.0222 |
| Post-Treatment RMSPE     |   0.0308 |
| RMSPE Ratio              |   1.3885 |
| P-Value                  |   0.3333 |
| N Donors                 |   2      |
| N Pre-Periods            |  24      |
| N Post-Periods           | 236      |

---

## get_fixed_effects
Fit a Fixed Effects ("within") estimator explaining a panel of `dependent_tickers` (the entities) by a regressor `x`, controlling for entity-specific (and/or time-specific) fixed effects.

**Also known as:** within estimator, FE, least squares dummy variable (LSDV) estimator.

Unlike this module's other regression methods (`get_ols`, `get_wls`, ...), which each compare a handful of individual ticker return series on equal footing, this treats `dependent_tickers` as a genuine panel of entities -- e.g. every stock in the `Toolkit` instance -- observed over time. The regressor `x` is built in exactly one of two ways (provide exactly one of the two arguments below):

- `independent_tickers`: a COMMON factor (or factors) applied identically to every entity at each date (e.g. a market benchmark, mirroring a Fama-French-style factor regression).
- `independent_column`: a PER-ENTITY regressor -- each entity's own value of a *different* historical data column (e.g. does `"Volume"` explain `"Return"`, across the panel).

Fixed Effects removes any purely entity-specific, time-invariant characteristic (e.g. a stock's typical risk premium) before estimating the regressor's coefficient(s), by demeaning every variable by its entity's mean. See `panel_data_model.get_fixed_effects` for the full formula and references.

**Args:**

- <u>independent_tickers (str &#124; list[str] &#124; None, optional):</u> The factor
ticker(s), whose `column` values are broadcast identically to every
entity at each date. Mutually exclusive with `independent_column`.
- <u>independent_column (str &#124; None, optional):</u> A different historical data
column, taken per-entity from each of `dependent_tickers`' own data, to
use as the regressor. Mutually exclusive with `independent_tickers`.
- <u>dependent_tickers (str &#124; list[str] &#124; None, optional):</u> The panel of
entity tickers to explain. Defaults to None, meaning every ticker in
the `Toolkit` instance (other than `independent_tickers`, if given).
- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly,
quarterly, or yearly). Defaults to "daily".
- <u>column (str, optional):</u> The dependent variable's historical data
column. Defaults to "Return".
- <u>entity_effects (bool, optional):</u> Whether to control for time-invariant
entity-specific characteristics. Defaults to True.
- <u>time_effects (bool, optional):</u> Whether to control for entity-invariant,
time-specific shocks. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the
results to. Defaults to None.

**Returns:**

pd.DataFrame: A coefficient table (Coefficient, Std. Error,
t-Statistic, P-Value) for the regressor(s), indexed by name, with the
recovered entity (and/or time) fixed-effect intercepts appended as
additional rows (only the Coefficient column is populated for those).

**Raises:**

ValueError: If both or neither of `independent_tickers`/
`independent_column` are given, or (see `panel_data_model.
get_fixed_effects`) if there are not enough observations for the
requested fixed effects.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_fixed_effects(
    independent_tickers="Benchmark", period="weekly"
)
```

Which returns:

|                     |   Coefficient |   Std. Error |   t-Statistic |   P-Value |
|:--------------------|--------------:|-------------:|--------------:|----------:|
| Benchmark           |        1.1403 |       0.0482 |       23.6381 |         0 |
| Entity Effect: AAPL |        0.0004 |     nan      |      nan      |       nan |
| Entity Effect: MSFT |        0.0006 |     nan      |      nan      |       nan |

---

## get_random_effects
Fit a Random Effects estimator explaining a panel of `dependent_tickers` (the entities) by a regressor `x`, via Swamy-Arora feasible Generalized Least Squares.

**Also known as:** RE, GLS panel estimator, Swamy-Arora estimator.

See `get_fixed_effects` for how `dependent_tickers`/`independent_tickers`/ `independent_column` are shaped into a panel, and `panel_data_model.get_random_effects` for the full estimator formula, references, and how it compares to Fixed Effects. Unlike Fixed Effects, Random Effects retains and estimates a single, population-average intercept rather than one intercept per entity -- more efficient than Fixed Effects if entity effects are indeed uncorrelated with the regressor(s) (see `get_hausman_test` to check that assumption).

**Args:**

- <u>independent_tickers (str &#124; list[str] &#124; None, optional):</u> The factor
ticker(s), whose `column` values are broadcast identically to every
entity at each date. Mutually exclusive with `independent_column`.
Note: since this `Toolkit` instance's historical data is aligned onto a
common calendar across tickers, a broadcast factor's entity mean is
identical for every entity, leaving no between-entity variation to
identify Random Effects' between-regression step -- prefer
`independent_column` here unless `dependent_tickers` genuinely differ
in their date coverage (e.g. different listing histories).
- <u>independent_column (str &#124; None, optional):</u> A different historical data
column, taken per-entity from each of `dependent_tickers`' own data, to
use as the regressor. Mutually exclusive with `independent_tickers`.
- <u>dependent_tickers (str &#124; list[str] &#124; None, optional):</u> The panel of
entity tickers to explain. Defaults to None, meaning every ticker in
the `Toolkit` instance (other than `independent_tickers`, if given).
- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly,
quarterly, or yearly). Defaults to "daily".
- <u>column (str, optional):</u> The dependent variable's historical data
column. Defaults to "Return".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the
results to. Defaults to None.

**Returns:**

pd.DataFrame: A coefficient table (Coefficient, Std. Error,
t-Statistic, P-Value), indexed by regressor name plus "Intercept".

**Raises:**

ValueError: If both or neither of `independent_tickers`/
`independent_column` are given, or (see `panel_data_model.
get_random_effects`) if there are not enough entities or observations
to estimate the model.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "AMZN"], api_key="FINANCIAL_MODELING_PREP_KEY",
                              start_date="2021-01-01",
                              end_date="2025-12-31",
)

toolkit.econometrics.get_random_effects(
    independent_column="Volume", period="weekly"
)
```

Which returns:

|           |   Coefficient |   Std. Error |   t-Statistic |   P-Value |
|:----------|--------------:|-------------:|--------------:|----------:|
| Intercept |         0.007 |       0.0024 |        2.8772 |    0.0041 |
| Volume    |        -0     |       0      |       -1.7774 |    0.0758 |

---

## get_hausman_test
Calculate the Hausman specification test comparing a Fixed Effects and a Random Effects fit of `dependent_tickers` (the panel of entities) on a regressor `x`.

**Also known as:** Hausman specification test, Hausman-Wu test.

Random Effects is more efficient than Fixed Effects but relies on entity effects being uncorrelated with the regressor(s) -- if that assumption is violated, Random Effects is inconsistent while Fixed Effects remains consistent regardless. See `panel_data_model.get_hausman_test` for the full formula and references, and `get_fixed_effects`/`get_random_effects` for how the two models being compared are estimated (including how `independent_tickers`/`independent_column` shape the panel, and why `independent_column` is generally the more reliable choice here).

**Args:**

- <u>independent_tickers (str &#124; list[str] &#124; None, optional):</u> The factor
ticker(s), whose `column` values are broadcast identically to every
entity at each date. Mutually exclusive with `independent_column`.
- <u>independent_column (str &#124; None, optional):</u> A different historical data
column, taken per-entity from each of `dependent_tickers`' own data, to
use as the regressor. Mutually exclusive with `independent_tickers`.
- <u>dependent_tickers (str &#124; list[str] &#124; None, optional):</u> The panel of
entity tickers to explain. Defaults to None, meaning every ticker in
the `Toolkit` instance (other than `independent_tickers`, if given).
- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly,
quarterly, or yearly). Defaults to "daily".
- <u>column (str, optional):</u> The dependent variable's historical data
column. Defaults to "Return".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the
results to. Defaults to None.

**Returns:**

pd.Series: The Hausman statistic, its degrees of freedom, its p-value,
and whether Fixed Effects is preferred over Random Effects at the 5%
level.

**Raises:**

ValueError: If both or neither of `independent_tickers`/
`independent_column` are given, or (see `panel_data_model.
get_hausman_test`) if there are not enough observations to fit either
model, or the two estimators share no common regressors to compare.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "AMZN"], api_key="FINANCIAL_MODELING_PREP_KEY",
                              start_date="2021-01-01",
                              end_date="2025-12-31",
)

toolkit.econometrics.get_hausman_test(
    independent_column="Volume", period="weekly"
)
```

Which returns:

|                           |      0 |
|:--------------------------|-------:|
| Hausman Statistic         | 1.6066 |
| Degrees of Freedom        | 1      |
| P-Value                   | 0.205  |
| Prefer Fixed Effects (5%) | 0      |

---

## get_arima_forecast
Fit an ARIMA(p, d, q) model to every ticker's price series in the Toolkit instance and forecast `forecast_steps` periods ahead.

**Also known as:** Box-Jenkins model, autoregressive integrated moving average.

An ARIMA(p, d, q) model differences the series `d` times to remove a (stochastic) trend, then fits an autoregressive-moving-average model to the result -- see `time_series_model.get_arima_forecast` for the full formula, estimation method (exact Maximum Likelihood via the Kalman filter) and its practical caveats.

**Args:**

- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to fit. Defaults to
"Adj Close".
- <u>p (int, optional):</u> The autoregressive order. Defaults to 1.
- <u>d (int, optional):</u> The number of times to difference the series. Defaults
to 1 (the typical choice for a non-stationary price level series).
- <u>q (int, optional):</u> The moving-average order. Defaults to 1.
- <u>forecast_steps (int, optional):</u> The number of periods ahead to forecast.
Defaults to 5.
- <u>include_constant (bool, optional):</u> Whether to estimate a free intercept.
Defaults to True -- see `time_series_model.get_arima_forecast` for when
to set this to False.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among
the tickers forecast. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the
results to. Defaults to None.

**Returns:**

pd.DataFrame: The `forecast_steps`-ahead forecast, one column per ticker,
indexed `1, ..., forecast_steps` (periods ahead, not a continuation of the
historical date index). Each ticker's ARIMA model is fit independently.

**Notes:**

- The method retrieves historical price data based on the specified `period`
for every ticker in the Toolkit instance and fits an ARIMA model to each.
- See `time_series_model.get_arima_forecast`'s `Notes` for this estimator's
practical limitations (in particular, keep `p + q` small).

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_arima_forecast(period="quarterly")
```

Which returns:

|   Step |    AAPL |    MSFT |
|-------:|--------:|--------:|
|      1 | 265.182 | 493.438 |
|      2 | 267.177 | 506.734 |
|      3 | 272.247 | 520.271 |
|      4 | 278.508 | 533.944 |
|      5 | 285.232 | 547.694 |

---

## get_var_forecast
Fit a Vector Autoregression (VAR) across every ticker in the Toolkit instance and forecast `forecast_steps` periods ahead.

A VAR models several series jointly: each ticker's value is regressed on `lags` past values of all tickers, including its own. Each asset's future can therefore depend on its own history and on the history of the others, without deciding in advance which one drives which:

- Y_t = c + SUM_{l=1}^{lags}(Phi_l * Y_(t-l)) + e_t

Where `Y_t` holds the values of all tickers at time `t` and each `Phi_l` is a matrix of coefficients. Because every equation has the same regressors, the model is estimated exactly by a separate OLS regression per ticker. Forecasts are produced by running the fitted equations forward one step at a time, feeding each forecast back in as the most recent lag. The coefficients show how shocks spread between assets; `get_impulse_response_function` and `get_variance_decomposition` summarise that, and `get_granger_causality` tests whether one ticker helps predict another. A VAR assumes stationary series, so returns are generally more suitable than prices (see `get_augmented_dickey_fuller`).

For more information about the method, see the following paper:

- Sims, C.A. (1980). "Macroeconomics and Reality." Econometrica, 48(1), 1-48.

**Also known as:** VAR model, vector autoregressive model.

**Args:**

- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to model. Defaults to
"Return".
- <u>lags (int, optional):</u> The VAR order. Defaults to 1.
- <u>forecast_steps (int, optional):</u> The number of periods ahead to forecast.
Defaults to 5.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among
the tickers modeled jointly. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the
results to. Defaults to None.

**Returns:**

pd.DataFrame: The `forecast_steps`-ahead forecast, one column per ticker,
indexed `1, ..., forecast_steps` (periods ahead).

**Notes:**

- The method retrieves historical data based on the specified `period` for every
ticker in the Toolkit instance and fits the VAR model jointly across all of them.
- Unlike `get_vecm_forecast`, this operates on `column` directly (typically
"Return", a stationary series) rather than price levels -- a VAR in levels is
misspecified for non-stationary series (see
`cointegration_model.get_johansen_cointegration`); use `get_vecm_forecast`
instead if the assets' price levels are cointegrated.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_var_forecast(period="quarterly")
```

Which returns:

|   Step |    AAPL |   MSFT |
|-------:|--------:|-------:|
|      1 | -0.0185 | 0.0141 |
|      2 |  0.0547 | 0.0584 |
|      3 |  0.0514 | 0.0432 |
|      4 |  0.0445 | 0.0412 |
|      5 |  0.046  | 0.0431 |

---

## get_impulse_response_function
Fit a Vector Autoregression (VAR) across every ticker in the Toolkit instance and trace out the Impulse Response Function (IRF) -- how a one-standard- deviation shock to each ticker propagates through the whole system over `periods` periods ahead.

**Also known as:** IRF.

A natural companion to `get_var_forecast`: rather than forecasting the levels forward, this traces out each ticker's dynamic response to a shock in every ticker (including itself) -- see `time_series_model.get_impulse_response_function` for the full formula, the Cholesky-orthogonalization used to identify the shocks, and why the ordering of tickers is an identifying assumption.

**Args:**

- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to model. Defaults to
"Return".
- <u>lags (int, optional):</u> The VAR order. Defaults to 1.
- <u>periods (int, optional):</u> The number of periods ahead to trace the response
out to. Defaults to 10.
- <u>orthogonalized (bool, optional):</u> Whether to orthogonalize the shocks via a
Cholesky decomposition of the residual covariance matrix -- see
`time_series_model.get_impulse_response_function`. Defaults to True.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among
the tickers modeled jointly. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the
results to. Defaults to None.

**Returns:**

pd.DataFrame: Each shock ticker's response table, one column per response
ticker, concatenated side by side under a top-level column per shock
ticker, indexed `0, ..., periods` (horizon, `0` = impact response).

**Notes:**

- The ordering of the tickers modeled determines which ticker is treated as
contemporaneously prior to the others. That ordering follows the Toolkit
instance's own ticker order and is not configurable here -- reorder the
Toolkit instance's tickers themselves to change the Cholesky identification
order -- see `time_series_model.get_impulse_response_function`'s `Notes`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_impulse_response_function(period="quarterly", periods=5)
```

Which returns:

|   Horizon |   ('AAPL', 'AAPL') |   ('AAPL', 'MSFT') |   ('MSFT', 'AAPL') |   ('MSFT', 'MSFT') |
|----------:|-------------------:|-------------------:|-------------------:|-------------------:|
|         0 |             0.141  |             0.0571 |             0      |             0.1247 |
|         1 |            -0.0213 |            -0.035  |             0.0658 |             0.0248 |
|         2 |            -0.0107 |             0      |            -0.0109 |            -0.0167 |
|         3 |             0.0039 |             0.0035 |            -0.0048 |             0.0003 |
|         4 |             0.0004 |            -0.0006 |             0.0019 |             0.0016 |
|         5 |            -0.0005 |            -0.0003 |             0.0002 |            -0.0003 |

---

## get_variance_decomposition
Fit a Vector Autoregression (VAR) across every ticker in the Toolkit instance and compute the (orthogonalized) Forecast Error Variance Decomposition (FEVD) -- what fraction of each ticker's `h`-step-ahead forecast error variance is attributable to each ticker's own structural shock, for `h = 1, ..., periods`.

**Also known as:** FEVD, variance decomposition.

The other natural companion to `get_var_forecast` (alongside `get_impulse_response_function`, which the FEVD is built from) -- see `time_series_model.get_variance_decomposition` for the full formula. A large own-shock share at short horizons that decays as the horizon grows is the classic signature of a ticker that is initially self-driven but increasingly explained by the rest of the system over time.

**Args:**

- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to model. Defaults to
"Return".
- <u>lags (int, optional):</u> The VAR order. Defaults to 1.
- <u>periods (int, optional):</u> The forecast horizon to decompose out to.
Defaults to 10.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among
the tickers modeled jointly. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the
results to. Defaults to None.

**Returns:**

pd.DataFrame: Each response ticker's variance-share table (one column per
shock ticker, rows summing to 1), concatenated side by side under a
top-level column per response ticker, indexed `1, ..., periods` (horizon).

**Notes:**

- See `get_impulse_response_function`'s `Notes` on the Cholesky ordering --
the same identifying assumption applies here.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_variance_decomposition(period="quarterly", periods=5)
```

Which returns:

|   Horizon |   ('AAPL', 'AAPL') |   ('AAPL', 'MSFT') |   ('MSFT', 'AAPL') |   ('MSFT', 'MSFT') |
|----------:|-------------------:|-------------------:|-------------------:|-------------------:|
|         1 |             1      |             0      |             0.1735 |             0.8265 |
|         2 |             0.8246 |             0.1754 |             0.2172 |             0.7828 |
|         3 |             0.8215 |             0.1785 |             0.2144 |             0.7856 |
|         4 |             0.8209 |             0.1791 |             0.2148 |             0.7852 |
|         5 |             0.8208 |             0.1792 |             0.2148 |             0.7852 |

---

## get_vecm_forecast
Fit a Vector Error Correction Model (VECM) across every (cointegrated) ticker in the Toolkit instance and forecast `forecast_steps` periods ahead.

**Also known as:** VECM, error correction model (for the multivariate/cointegrated case).

A VECM keeps a VAR's short-run dynamics while ALSO letting each asset's price change react to how far the system currently sits from its long-run equilibrium (the cointegrating relationship(s) among the tickers, taken from `cointegration_model.get_johansen_cointegration`) -- see `time_series_model.get_vecm_forecast` for the full formula, estimation method and verification notes.

**Args:**

- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to model. Defaults to
"Adj Close" -- a VECM needs price LEVELS (non-stationary, cointegrated
series), not returns, the same input `get_johansen_cointegration` expects.
- <u>k_ar_diff (int, optional):</u> The number of lagged first differences to
include as short-run dynamics. Defaults to 1.
- <u>forecast_steps (int, optional):</u> The number of periods ahead to forecast.
Defaults to 5.
- <u>significance (float, optional):</u> The significance level (one of 0.01, 0.05,
0.10) at which the Johansen trace test determines the cointegrating rank.
Defaults to 0.05.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among
the tickers modeled jointly. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the
results to. Defaults to None.

**Returns:**

pd.DataFrame: The `forecast_steps`-ahead forecast, on the price-level
scale, one column per ticker, indexed `1, ..., forecast_steps` (periods
ahead).

**Raises:**

ValueError: If the Johansen test does not reject a cointegrating rank of 0
for the Toolkit instance's tickers at `significance` -- a VECM is not
appropriate for non-cointegrated assets; use `get_var_forecast` on their
returns instead.

**Notes:**

- The method retrieves historical price data based on the specified `period`
for every ticker in the Toolkit instance and fits the VECM jointly across all
of them.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

# AAPL/MSFT alone aren't cointegrated in this sample -- add Benchmark to the
# system to get one that is.
toolkit.econometrics.get_vecm_forecast(period="quarterly", include_benchmark=True)
```

Which returns:

| 0   |
|-----|

---

## get_rmse
Calculate the Root Mean Squared Error (RMSE) between every unordered pair of tickers' series in the Toolkit instance.

**Also known as:** RMSD (Root Mean Squared Deviation).

See `forecast_evaluation_model.get_rmse` for the formula. This controller method compares two ASSETS' series directly, treating one as a naive "forecast" proxy for the other -- a simple, tracking-error style measure of how closely two series move together in absolute deviation terms (e.g. a portfolio versus a benchmark, or one asset as a naive stand-in forecast for a similar one). For evaluating an actual FORECASTING MODEL (ARIMA/VAR) rather than one asset as a naive proxy for another, use `get_out_of_sample_validation` instead.

**Args:**

- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to compare. Defaults to
"Return".
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the
tickers paired up. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the
results to. Defaults to None.

**Returns:**

pd.Series: The RMSE, indexed by unordered `(Ticker A, Ticker B)` pair.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_rmse(period="quarterly")
```

Which returns:

|                  |   RMSE |
|:-----------------|-------:|
| ('AAPL', 'MSFT') | 0.1396 |

---

## get_mae
Calculate the Mean Absolute Error (MAE) between every unordered pair of tickers' series in the Toolkit instance.

MAE is the average absolute difference between two series:

- MAE = mean(&#124;actual_t - forecast_t&#124;)

It is expressed in the units of the series itself (e.g. a return difference) and answers "how far apart are the two series in a typical period". Every difference counts in proportion to its size, so unlike `get_rmse`, which squares the differences and is therefore dominated by a few large gaps, MAE is robust to occasional outliers. A lower value means the two tickers track each other more closely.

This method compares two assets directly, for example how closely a fund tracks its index or how two related stocks move together, rather than an asset against a model's forecast; see `get_rmse` for the reasoning, and `get_out_of_sample_validation` for evaluating actual forecasts.

**Also known as:** MAD (Mean Absolute Deviation).

**Args:**

- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to compare. Defaults to
"Return".
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the
tickers paired up. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the
results to. Defaults to None.

**Returns:**

pd.Series: The MAE, indexed by unordered `(Ticker A, Ticker B)` pair.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_mae(period="quarterly")
```

Which returns:

|                  |    MAE |
|:-----------------|-------:|
| ('AAPL', 'MSFT') | 0.1035 |

---

## get_out_of_sample_validation
Out-of-sample validate an ARIMA or VAR forecast of every ticker in the Toolkit instance -- fit only on a training portion of the history, forecast the held-out remainder, and score the forecast against what actually happened.

**Also known as:** hold-out validation, train/test split validation.

See `forecast_evaluation_model.get_out_of_sample_validation` for the general harness this wraps. Since that function takes a raw Python callable (not serializable for e.g. the MCP-facing tool layer), this controller method instead hardcodes the choice between the two Part-1 forecasting models via the `model` string:

- `model="arima"`: `time_series_model.get_arima_forecast` is fit on each ticker's own training-period series (`p`, `d`, `q`, `include_constant` control the model, same as `get_arima_forecast`).
- `model="var"`: `time_series_model.get_var_forecast` is fit on the training-period series of each ticker together with `other_tickers` (`lags` controls the VAR order, defaulting to every other ticker in the Toolkit instance if not given); only that ticker's own forecast column is scored against its holdout.

**Args:**

- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to validate. Defaults
to "Adj Close".
- <u>model (str, optional):</u> Either "arima" or "var". Defaults to "arima".
- <u>train_fraction (float, optional):</u> The fraction of observations used for
training; the remainder is the holdout. Defaults to 0.8.
- <u>p (int, optional):</u> The ARIMA autoregressive order (`model="arima"` only).
Defaults to 1.
- <u>d (int, optional):</u> The ARIMA differencing order (`model="arima"` only).
Defaults to 1.
- <u>q (int, optional):</u> The ARIMA moving-average order (`model="arima"` only).
Defaults to 1.
- <u>include_constant (bool, optional):</u> Whether the ARIMA model estimates a
free intercept (`model="arima"` only). Defaults to True.
- <u>lags (int, optional):</u> The VAR order (`model="var"` only). Defaults to 1.
- <u>other_tickers (list[str] &#124; None, optional):</u> The other assets to include in
the VAR system alongside the ticker being validated (`model="var"` only).
Defaults to None, meaning every other ticker in the Toolkit instance.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among
the tickers validated (and, for `model="var"`, among the default
`other_tickers`). Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the
results to. Defaults to None.

**Returns:**

pd.DataFrame: `RMSE`, `MAE` and `Holdout Observations`, one column per
ticker.

**Raises:**

ValueError: If `model` is not "arima" or "var", or (for `model="var"`)
fewer than 2 tickers are available to form a VAR system.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_out_of_sample_validation(
    period="weekly", model="arima", p=1, d=1, q=1
)
```

Which returns:

|                      |    AAPL |    MSFT |
|:---------------------|--------:|--------:|
| RMSE                 | 44.5713 | 38.7415 |
| MAE                  | 38.6048 | 32.369  |
| Holdout Observations | 53      | 53      |

---

## get_event_study
Perform a market-model event study around a single event date, following the methodology in MacKinlay, A.C. (1997), "Event Studies in Economics and Finance," Journal of Economic Literature, 35(1), 13-39 -- the canonical reference and still the dominant approach used to measure the stock-price impact of corporate events (earnings announcements, M&A deals, index additions/deletions, dividend changes, regulatory actions, etc.).

A market model (`Return_t = alpha + beta * Benchmark_Return_t + e_t`) is fit via OLS over a clean "estimation window" ending `gap_days` before the event, then the Abnormal Return on each day of the "event window" around the event is the actual return minus the market-model-predicted expected return. These are cumulated into the Cumulative Abnormal Return (CAR) -- the stock-price impact attributable to the event, after stripping out what would have been expected from general market movements alone -- along with a t-test of whether CAR is significantly different from zero.

**Also known as:** CAR analysis, abnormal returns analysis, market model event study.

**Args:**

- <u>event_date (str):</u> The date of the event (e.g. "2023-05-04"). Must fall
within the Toolkit instance's daily historical data.
- <u>dependent_ticker (str &#124; None, optional):</u> The ticker being studied.
Defaults to the first ticker in the Toolkit instance.
- <u>column (str, optional):</u> The historical data column to use. Defaults to
"Return".
- <u>estimation_window (int, optional):</u> Number of trading days used to
estimate the market model. Defaults to 250 (~one trading year).
- <u>gap_days (int, optional):</u> Number of trading days between the end of the
estimation window and the event date. Defaults to 30.
- <u>pre_event_days (int, optional):</u> Number of trading days before the event
date included in the event window. Defaults to 10.
- <u>post_event_days (int, optional):</u> Number of trading days after the event
date included in the event window. Defaults to 10.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the
results to. Defaults to None.

**Returns:**

pd.Series: The Cumulative Abnormal Return (CAR), its t-statistic and
p-value, the market-model alpha and beta, and the number of estimation-
window observations used.

**Notes:**

- Always uses daily data -- event windows are measured in trading days, so
quarterly/yearly granularity would not be meaningful here.
- The market/benchmark return series is the Toolkit instance's `"Benchmark"`
column.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_event_study(event_date="2023-05-04")
```

Which returns:

|                                |        0 |
|:-------------------------------|---------:|
| Cumulative Abnormal Return     |   0.0207 |
| CAR t-statistic                |   0.4243 |
| CAR p-value                    |   0.6717 |
| Alpha                          |   0.0004 |
| Beta                           |   1.3001 |
| Estimation Window Observations | 250      |

---

