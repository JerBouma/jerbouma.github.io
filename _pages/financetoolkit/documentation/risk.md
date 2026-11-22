---
title: Risk
seo_title: "Value at Risk and Risk Metrics in Python | Finance Toolkit"
seo_title_suffix: false
excerpt: The Risk module is meant to calculate important risk metrics such as Value at Risk (VaR), Conditional Value at Risk (cVaR), Maximum Drawdown, Correlations, GARCH, EWMA and more.
description: "Calculate Value at Risk (VaR), Conditional VaR, maximum drawdown, GARCH and EWMA volatility and other risk metrics in Python with the Finance Toolkit."
author_profile: false
permalink: /projects/financetoolkit/docs/risk
classes: wide-sidebar
layout: single
redirect_from:
    - /risk
    - /projects/financetoolkit/risk-notebook
    - /projects/financetoolkit/risk-module
sidebar:
    nav: "financetoolkit-docs-risk"
---

The Risk module calculates important risk metrics such as Value at Risk (VaR), Conditional Value at Risk (CVaR), Maximum Drawdown, Correlations, GARCH, EWMA and more.

Use it in Claude, ChatGPT or another AI assistant through the [Finance Toolkit MCP](/projects/financetoolkit/mcp), or install the Python package:

```python
pip install financetoolkit -U
```

{% include docs-search.html %}

{% include financetoolkit-getting-started/risk.md %}

## collect_all_metrics
Calculates and collects all risk metrics.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly, or yearly).
Defaults to "quarterly" if the Toolkit is initialised with quarterly=True, otherwise "yearly".
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

## get_factor_analysis
Factor analysis (predictive power) of the risk metrics: whether the tickers that score high on a metric go on to return more than those that score low. Per period, the information coefficient (IC) is the Spearman rank correlation between the metric of the tickers in the period and their return over the following horizon: 1 means the metric ranks the later returns perfectly, -1 in reverse and 0 that it says nothing about them. The IC measures skill in Grinold and Kahn's fundamental law of active management, $$\text{IR} \approx \text{IC} \times \sqrt{\text{breadth}}$$: a small but consistent IC across many tickers and periods gives a high information ratio.

The summary has a row per metric and horizon with the mean IC, its standard deviation, the IC information ratio (mean divided by standard deviation), the t-statistic of the mean with its p-value, the share of periods with a positive IC, the number of periods, the top minus bottom spread (the mean forward return of the highest quantile minus that of the lowest), the mean turnover of the top and bottom quantiles and the mean rank autocorrelation of the metric from one period to the next. With detail, it returns one of those parts per period (or per quantile) for a single metric.

Each metric is measured within each period (e.g. the volatility of a month's daily returns) and compared with the returns from the close of the period's last trading day onwards, using the dividend and split adjusted close, so a metric never overlaps the returns it is compared with. Each ticker keeps its own history: a ticker without a value or a return in a period is left out of that period only.

**Args:**

- <u>metrics (str &#124; list[str], optional):</u> A risk method name with a value per ticker and period,
e.g. "get_volatility", a list of them, or a collection: "anomalies" or "all".
Defaults to "anomalies", the volatility, maximum drawdown, skewness and Amihud
illiquidity. "all" adds the downside deviation, kurtosis, value at risk,
conditional value at risk, tail ratio and Roll spread.
- <u>period (str, optional):</u> The frequency at which the metrics are measured and evaluated
(weekly, monthly, quarterly or yearly). Each metric is calculated
within each period from that period's daily returns, so use monthly or longer
for enough returns per period. Defaults to "monthly".
- <u>horizons (list[int] &#124; int &#124; None, optional):</u> The number of periods the forward
returns cover. Defaults to None, which uses about a period, a quarter and a
year ahead (1, 3 and 12 months for monthly).
- <u>quantiles (int, optional):</u> The number of quantiles the tickers are sorted into per
period. Defaults to 5.
- <u>periods_apart (int, optional):</u> The number of periods between the dates the
quantile turnover and the rank autocorrelation compare. Defaults to 1.
- <u>detail (str &#124; None, optional):</u> Returns one part of the analysis of a single metric
instead of the summary: "information_coefficient" (per period and horizon),
"quantile_returns" (the mean forward return per quantile and horizon),
"quantile_turnover" (per period and quantile) or "rank_autocorrelation" (per
period). Defaults to None.
- <u>column (str &#124; None, optional):</u> The output to use of a metric with several.
Defaults to None, which uses the first.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
**kwargs: Parameters passed to the metrics that take them, e.g. alpha=0.05.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The summary per metric and horizon, or with detail that part of the
analysis of the metric.

**Notes:**

- The IC is reported as measured: the low-volatility anomaly, where the least
volatile stocks go on to return more, shows as a negative IC for the volatility.
Read the sign as the direction of the relationship.
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

toolkit.risk.get_factor_analysis(horizons=[1, 12])
```

Which returns:

|                                         |   Mean IC |   IC Standard Deviation |   IC Information Ratio |   t-Statistic |   p-Value |   Positive Share |   Observations |   Top Minus Bottom |   Quantile Turnover |   Rank Autocorrelation |
|:----------------------------------------|----------:|------------------------:|-----------------------:|--------------:|----------:|-----------------:|---------------:|-------------------:|--------------------:|-----------------------:|
| ('get_volatility', '1 Month')           |    0.0963 |                  0.3676 |                 0.262  |        2.8586 |    0.005  |           0.6218 |            119 |             0.0185 |              0.4688 |                 0.5848 |
| ('get_volatility', '12 Months')         |    0.2759 |                  0.3703 |                 0.7451 |        7.7428 |    0      |           0.7685 |            108 |             0.3154 |              0.4688 |                 0.5848 |
| ('get_maximum_drawdown', '1 Month')     |   -0.0257 |                  0.3315 |                -0.0774 |       -0.8443 |    0.4002 |           0.4622 |            119 |            -0.0041 |              0.6275 |                 0.2719 |
| ('get_maximum_drawdown', '12 Months')   |   -0.1759 |                  0.3542 |                -0.4965 |       -5.1603 |    0      |           0.3241 |            108 |            -0.2094 |              0.6275 |                 0.2719 |
| ('get_skewness', '1 Month')             |    0.0136 |                  0.2943 |                 0.0464 |        0.5056 |    0.6141 |           0.5462 |            119 |            -0.0007 |              0.7521 |                 0.0593 |
| ('get_skewness', '12 Months')           |    0.0081 |                  0.2996 |                 0.0271 |        0.2815 |    0.7789 |           0.5093 |            108 |             0.0142 |              0.7521 |                 0.0593 |
| ('get_amihud_illiquidity', '1 Month')   |   -0.0285 |                  0.3896 |                -0.0731 |       -0.7971 |    0.427  |           0.479  |            119 |            -0.0059 |              0.1905 |                 0.8996 |
| ('get_amihud_illiquidity', '12 Months') |   -0.1164 |                  0.3789 |                -0.3072 |       -3.1927 |    0.0019 |           0.3611 |            108 |            -0.0796 |              0.1905 |                 0.8996 |

---

## get_tail_dependence_coefficient
Calculate the Upper and Lower Tail Dependence Coefficients between `ticker_a` and `ticker_b`. Without a pair, every ticker is paired with the benchmark, which tells how likely each company is to be in distress when the market is.

Correlation only captures the *average* co-movement between two assets -- it says nothing about whether they are more likely to crash together than an equivalent gaussian relationship would imply. The Tail Dependence Coefficient answers that specific question directly: the probability that one asset is in extreme distress, given that the other one already is.

The empirical estimate at $$q = 0.95$$ rests on the few days on which both assets are in their worst (or best) 5% at the same time, so it needs several years of daily data to be stable. A gaussian dependence of any correlation below 1 implies zero tail dependence, so a Lower Tail Dependence Coefficient well above zero means that diversification between the two assets is weakest exactly when it is needed.

For more information about the method, see the following papers:

- Embrechts, P., McNeil, A., & Straumann, D. (1999). "Correlation: Pitfalls and Alternatives." RISK Magazine, 12, 69-71.
- Poon, S.H., Rockinger, M., & Tawn, J. (2004). "Extreme Value Dependence in Financial Markets: Diagnostics, Models, and Financial Implications." Review of Financial Studies, 17(2), 581-610.

The formula is as follows (with the default method="empirical" and q=0.95):

$$
\text{Upper Tail Dependence} = \frac{\#(A > Q_{A}(q) \;\text{and}\; B > Q_{B}(q))}{\#(A > Q_{A}(q))}
$$

$$
\text{Lower Tail Dependence} = \frac{\#(A \leq Q_{A}(1 - q) \;\text{and}\; B \leq Q_{B}(1 - q))}{\#(A \leq Q_{A}(1 - q))}
$$

Where A and B are the values of `ticker_a` and `ticker_b` on their common dates and $$Q_{A}$$ and $$Q_{B}$$ their empirical quantiles. With method="gaussian" both coefficients are 0 (1 only for a correlation of exactly 1), and with method="student-t" both are $$2 \cdot t_{v + 1} (- \sqrt{(v + 1) \cdot (1 - \rho) / (1 + \rho)})$$, with v = `dof`, rho the Pearson correlation and $$t_{v + 1}$$ the Student-T distribution function.

**Also known as:** tail dependence, extremal dependence coefficient.

**Args:**

- <u>ticker_a (str &#124; None, optional):</u> The first asset. Defaults to None, which pairs every other ticker
in the Toolkit instance (the benchmark included when `ticker_b` is given) with `ticker_b`.
- <u>ticker_b (str &#124; None, optional):</u> The second asset. Defaults to None, which uses the benchmark.
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
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Raises:**

ValueError: If one of the two tickers is missing while the Toolkit has no benchmark.

**Returns:**

pd.Series &#124; pd.DataFrame: The Lower and Upper Tail Dependence Coefficients, the linear (Pearson)
correlation between the two assets, and the number of observations used -- a Series for a given
pair, or a DataFrame with a row per ticker paired with `ticker_b` (or the benchmark) otherwise.

**Notes:**

- The method retrieves historical data based on the specified `period` for each pair of
assets and estimates the tail dependence coefficient between them.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "JPM", "XOM", "^STOXX50E"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_tail_dependence_coefficient()
```

Which returns:

|           |   Lower Tail Dependence |   Upper Tail Dependence |   Correlation |   Observations |
|:----------|------------------------:|------------------------:|--------------:|---------------:|
| AAPL      |                  0.4603 |                  0.4921 |        0.7582 |           1254 |
| JPM       |                  0.3968 |                  0.4127 |        0.6233 |           1254 |
| XOM       |                  0.2063 |                  0.2222 |        0.3425 |           1254 |
| ^STOXX50E |                  0.3387 |                  0.3226 |        0.4509 |           1240 |

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
u_{i} = \frac{\operatorname{Rank}(A_{i})}{n + 1},\;\; v_{i} = \frac{\operatorname{Rank}(B_{i})}{n + 1}
$$

$$
\text{Gaussian Rho} = \operatorname{Correlation}(\Phi^{-1} (u),\; \Phi^{-1} (v))
$$

$$
\text{Student-T Rho} = \sin\left(\frac{\pi \cdot \text{Kendall's Tau}}{2}\right)
$$

$$
\Theta \;(\text{and the Student-T Degrees of Freedom}) = \operatorname*{arg\,max} \sum \ln c(u_{i},\; v_{i})
$$

$$
\text{AIC} = 2 \cdot k - 2 \cdot \text{Log-Likelihood}
$$

Where A and B are the values of the two assets on their n common dates, c is the copula density and k the number of fitted parameters (2 for the Student-T, 1 otherwise). The search bounds are [2.05, 60] for the Degrees of Freedom and, for Theta, [0.0001, 100] (Clayton), [1, 50] (Gumbel) and [-50, 50] (Frank). The implied tail dependence is $$2^{- 1 / \text{Theta}}$$ in the lower tail for Clayton, $$2 - 2^{1 / \text{Theta}}$$ in the upper tail for Gumbel, $$2 \cdot t_{v + 1} (- \sqrt{(v + 1) \cdot (1 - \text{Rho}) / (1 + \text{Rho})})$$ in both tails for the Student-T and 0 otherwise.

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
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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
(Z_{1},\; Z_{2}) \sim N\left(0,\; \begin{pmatrix} 1 & \text{Rho} \\ \text{Rho} & 1 \end{pmatrix}\right)
$$

$$
U = \Phi(Z_{1}),\;\; V = \Phi(Z_{2})
$$

$$
\text{Simulated Return}\; A = \operatorname{Quantile}(A,\; U),\;\; \text{Simulated Return}\; B = \operatorname{Quantile}(B,\; V)
$$

Where Rho is fitted as in `get_copula_parameters` and Quantile is the empirical quantile (linear interpolation) of each asset's own history. The Student-T copula scales (Z1, Z2) by $$\sqrt{v / W}$$, with $$W \sim \chi^{2} (v)$$, and maps them with the Student-T distribution function; the Clayton, Gumbel and Frank copulas draw U and T uniformly and solve $$C (V \vert U) = T$$ for V.

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
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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
Calculate the (Delta-)CoVaR of `ticker` conditional on `conditioning_ticker` being in its own distress state. Without a pair, it measures how much each ticker's distress adds to the tail risk of the benchmark (the market as the "system"), as in Adrian & Brunnermeier (2016).

Ordinary Value at Risk treats each asset in isolation, which misses systemic risk -- the fact that one asset's distress can spill over and worsen another's risk. CoVaR directly measures that spillover: it is the VaR of `ticker`, conditional on `conditioning_ticker` itself being at its own `alpha`-VaR, estimated via a linear Quantile Regression of `ticker`'s returns on `conditioning_ticker`'s returns at quantile `alpha`. The Delta-CoVaR isolates the marginal, distress-specific contribution by subtracting the same construction evaluated in the "normal" (median) state instead.

CoVaR was introduced to measure systemic risk: in its original application `ticker` is a financial-system index (or a bank's peers) and `conditioning_ticker` a single institution, so the Delta-CoVaR reads as that institution's contribution to system-wide tail risk. Because the quantile regression is fitted at the `alpha` quantile, it needs several years of daily data, and the result is a statement about co-movement in the tails, not about causality.

The formula is as follows (with the default alpha=0.05):

$$
\operatorname{Quantile}_{\alpha}(A \mid B) = \text{Intercept} + \text{Slope} \cdot B
$$

$$
\text{CoVaR} = \text{Intercept} + \text{Slope} \cdot \text{VaR}_{B}
$$

$$
\text{Delta-CoVaR} = \text{Slope} \cdot (\text{VaR}_{B} - \operatorname{Median}(B))
$$

Where A are the values of `ticker` and B those of `conditioning_ticker` on their common dates, the Intercept and Slope come from a linear quantile regression at quantile alpha (minimizing the check loss) and $$\text{VaR}_{B}$$ is the empirical alpha-quantile of B.

For more information about the method, see the following paper:

- Adrian, T., & Brunnermeier, M.K. (2016). "CoVaR." American Economic Review, 106(7), 1705-1741.

**Also known as:** Conditional Value at Risk (systemic risk sense), Delta-CoVaR.

**Args:**

- <u>ticker (str &#124; None, optional):</u> The asset whose conditional VaR is being measured (the system).
Defaults to None, which uses the benchmark.
- <u>conditioning_ticker (str &#124; None, optional):</u> The asset whose distress `ticker` is conditioned on.
Defaults to None, which conditions `ticker` on every other ticker in the Toolkit instance in turn
(the benchmark included when `ticker` is given), a row each.
- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily", since a dependence estimate needs far more observations than a
lower frequency provides -- at "yearly" a decade of history is only ten
observations.
- <u>column (str, optional):</u> The historical data column to use. Defaults to "Return".
- <u>alpha (float, optional):</u> The tail probability for both the tail quantile regression and
the VaR of `conditioning_ticker` (e.g., 0.05 for the 95% confidence level). Defaults to 0.05.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Raises:**

ValueError: If one of the two tickers is missing while the Toolkit has no benchmark.

**Returns:**

pd.Series &#124; pd.DataFrame: The CoVaR, the Delta-CoVaR, the tail (alpha-quantile) Quantile Regression
slope and intercept, and the number of observations used -- a Series for a given pair, or a
DataFrame with a row per conditioning ticker otherwise.

**Notes:**

- The method retrieves historical data based on the specified `period` for each pair of
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

toolkit.risk.get_covar()[["CoVaR", "Delta-CoVaR"]]
```

Which returns:

|     |   CoVaR |   Delta-CoVaR |
|:----|--------:|--------------:|
| GS  | -0.0232 |       -0.0104 |
| JPM | -0.0247 |       -0.012  |

---

## get_marginal_expected_shortfall
Calculate the Marginal Expected Shortfall (MES) of each ticker per period: its average return on the days the market (the benchmark) is in its worst `alpha` tail.

Acharya, Pedersen, Philippon and Richardson (2017) show that a financial institution's contribution to the Expected Shortfall of the system is its MES, the return it is expected to make when the system as a whole is in its tail. Measured over a year of daily returns on the 5% worst days of the market, the MES of the financial firms before 2007 predicted which of them lost the most in the crisis. Where the CoVaR asks how much the system suffers when a firm is in distress, the MES asks how much a firm suffers when the system is; it is the market component of SRISK (see `get_srisk`).

The formula is as follows (with the default alpha=0.05):

$$
\text{VaR}_{\text{alpha}}(\text{Market}) = \operatorname{Quantile}(\text{Market Returns within the period},\; \alpha)
$$

$$
\text{MES} = \operatorname{MEAN}(\text{Returns}_{t} \mid \text{Market Return}_{t} \leq \text{VaR}_{\text{alpha}}(\text{Market}))
$$

Where the returns are the daily returns of the Adjusted Close within the period on the days the ticker and the market both have a return, and the quantile interpolates linearly between the two nearest returns. The MES is reported as a return, negative for a loss, like the Value at Risk and the Conditional Value at Risk (the paper reports the loss, -MES). With `rolling`, the days of the last `rolling` periods are used together.

For more information about the method, see the following paper:

- Acharya, V.V., Pedersen, L.H., Philippon, T., & Richardson, M. (2017). "Measuring Systemic Risk." The Review of Financial Studies, 30(1), 2-47.

**Also known as:** MES, marginal expected shortfall, systemic expected shortfall, tail beta.

**Args:**

- <u>ticker (str &#124; None, optional):</u> The ticker whose MES to calculate. Defaults to None, which
uses every ticker except the market.
- <u>market_ticker (str &#124; None, optional):</u> The ticker that represents the market (the system).
Defaults to None, which uses the benchmark.
- <u>period (str, optional):</u> The period of each estimate (monthly, quarterly or yearly). Defaults
to "yearly", as in the paper.
- <u>alpha (float, optional):</u> The tail probability of the market returns. Defaults to 0.05, the
5% worst days of the market.
- <u>rolling (int, optional):</u> Use the daily returns of the last `rolling` periods instead of one
period (e.g. period='monthly' and rolling=12 for a one-year window at every month end).
Defaults to None.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the MES over time. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Raises:**

ValueError: If the period is not monthly, quarterly or yearly, or if the Toolkit has no
benchmark and no market_ticker is given.

**Returns:**

pd.DataFrame: The MES as a return, with the periods as the index and the tickers as columns.

**Notes:**

- Each ticker is paired with the market on the days both have a return: a market return on a day the
ticker did not trade is compounded into the next shared date, so the other tickers of the Toolkit (e.g.
a cryptocurrency that trades every day) do not change a ticker's MES.
- A period with fewer than 1 / alpha shared returns (20 at alpha=0.05) is NaN, as its tail would hold
less than one day on average.
- The market itself is left out: its MES is the average of its own worst days, its Conditional Value at
Risk.
- Closes on different exchanges are not synchronous (BNP.PA closes hours before SPY), so a market fall
after the ticker's close shows up in its next day and the MES understates the tail dependence; use a
local market index as market_ticker for such tickers.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["JPM", "BAC", "C", "GS"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_marginal_expected_shortfall()
```

Which returns:

| Date   |     JPM |     BAC |       C |      GS |
|:-------|--------:|--------:|--------:|--------:|
| 2021   | -0.0126 | -0.0134 | -0.0152 | -0.0173 |
| 2022   | -0.0282 | -0.0315 | -0.029  | -0.0284 |
| 2023   | -0.0155 | -0.0205 | -0.0187 | -0.017  |
| 2024   | -0.02   | -0.0196 | -0.0232 | -0.0233 |
| 2025   | -0.029  | -0.0339 | -0.0393 | -0.0394 |

---

## get_srisk
Calculate SRISK, the capital each firm is expected to need in a crisis, per period, with the Long-Run Marginal Expected Shortfall (LRMES) it is based on and each firm's share of the total.

Brownlees and Engle (2017) define SRISK as the capital shortfall of a firm conditional on a severe market decline: in a crisis the market falls by 40% over six months, the firm's equity falls by its LRMES, and the firm has to hold a prudential share k of its assets (8% for U.S. firms) as equity. The firms with the largest SRISK contribute most to the undercapitalization of the financial system in a crisis, which NYU Stern's V-Lab publishes as its systemic risk ranking (SRISK%). It is meant for financial firms, whose liabilities are mostly debt; for other firms the liabilities include operating items.

The formula is as follows (with the defaults decline=0.4 and capital_ratio=0.08):

$$
\text{Beta} = \frac{\operatorname{Covariance}(\text{Returns},\; \text{Market Returns})}{\operatorname{Variance}(\text{Market Returns})}
$$

$$
\text{LRMES} = (1 - \text{decline})^{\text{Beta}} - 1
$$

$$
\text{SRISK} = k \cdot \text{Total Liabilities} - (1 - k) \cdot (1 + \text{LRMES}) \cdot \text{Market Cap}
$$

$$
\text{SRISK Share} = \frac{\max(\text{SRISK},\; 0)}{\sum(\max(\text{SRISK},\; 0) \;\text{of every ticker})}
$$

Where Beta is the market beta from the daily returns of the Adjusted Close within the period on the days the ticker and the market (the benchmark) both have a return, k the capital ratio, Total Liabilities those of the balance sheet and Market Cap the Close on the ticker's last trading day of the period times the Weighted Average Shares Diluted. The LRMES is the approximation V-Lab publishes (1 - exp(log(1 - d) * Beta)), reported as a return, negative for a loss, like the Marginal Expected Shortfall; 1 + LRMES is the share of the equity left after the crisis. With `rolling`, the beta uses the days of the last `rolling` periods.

For more information about the method, see the following papers:

- Brownlees, C., & Engle, R.F. (2017). "SRISK: A Conditional Capital Shortfall Measure of Systemic Risk." The Review of Financial Studies, 30(1), 48-79.
- Acharya, V.V., Engle, R.F., & Richardson, M. (2012). "Capital Shortfall: A New Approach to Ranking and Regulating Systemic Risks." American Economic Review, 102(3), 59-64.

**Also known as:** systemic risk, capital shortfall, SRISK%, long-run marginal expected shortfall, LRMES.

**Args:**

- <u>ticker (str &#124; None, optional):</u> The ticker whose SRISK to calculate. Defaults to None, which
uses every ticker except the market.
- <u>market_ticker (str &#124; None, optional):</u> The ticker that represents the market. Defaults to None,
which uses the benchmark.
- <u>period (str, optional):</u> The period of each estimate (monthly, quarterly or yearly). Defaults
to "yearly".
- <u>decline (float, optional):</u> The fall of the market over six months that defines the crisis, as a
decimal. Defaults to 0.4, as in V-Lab.
- <u>capital_ratio (float, optional):</u> The prudential capital ratio k, the share of the assets a firm
has to hold as equity. Defaults to 0.08, V-Lab's ratio for U.S. firms (5.5% for European
firms, whose IFRS balance sheets report more liabilities).
- <u>rolling (int, optional):</u> Estimate the beta from the daily returns of the last `rolling` periods
instead of one period (e.g. period='monthly' and rolling=12 for a one-year beta at every
month end). Defaults to None.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the results over time. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Raises:**

ValueError: If the period is not monthly, quarterly or yearly, or if the Toolkit has no
benchmark and no market_ticker is given.

**Returns:**

pd.DataFrame: The Beta, LRMES, Total Liabilities, Market Cap, SRISK and SRISK Share, with the
periods as the index and (item, ticker) as columns. SRISK, the liabilities and the market cap are
in currency units, the others decimals.

**Notes:**

- SRISK is positive for a capital shortfall and negative for a surplus. Each firm keeps its signed
SRISK; the SRISK Share (V-Lab's SRISK%) only adds the shortfalls, as a surplus does not offset another
firm's shortfall in a crisis, so a firm with a surplus has a share of 0.
- The liabilities and the share count are those of the last fiscal period that ended on or before the
last calendar day of the period (filed on or before it with point_in_time), so a fiscal year that ends
on a weekend still belongs to its own year and a period never uses figures that were not yet reported.
A Toolkit with quarterly=True uses the latest quarter, as V-Lab does. The market cap is the traded
(split-adjusted) Close times the diluted share count, which for periods that coincide with the fiscal
periods equals `toolkit.ratios.get_market_cap`.
- The Close is in the currency the ticker trades in, while the statements are in the currency they
are reported in unless the Toolkit converts them to the currency of the prices (convert_currency=True);
when the two differ without a conversion, a warning is logged.
- V-Lab estimates the beta with a GJR-GARCH volatility and a Dynamic Conditional Correlation (DCC)
model, a beta for every day, while this beta is the ordinary least squares beta over the period's daily
returns, so the figures are of the same order but do not match V-Lab's.
- The beta needs at least 15 shared returns in the window; the market and tickers without financial
statements (such as an index or a cryptocurrency) are left out or NaN.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["JPM", "BAC", "C"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
    quarterly=True,
)

toolkit.risk.get_srisk().xs("C", level=1, axis=1)
```

Which returns:

| Date   |   Beta |   LRMES |   Total Liabilities |   Market Cap |       SRISK |   SRISK Share |
|:-------|-------:|--------:|--------------------:|-------------:|------------:|--------------:|
| 2021   | 0.9001 | -0.3686 |         2.08874e+12 |  1.20877e+11 | 9.68806e+10 |        0.832  |
| 2022   | 0.9657 | -0.3894 |         2.21484e+12 |  8.84654e+10 | 1.27491e+11 |        0.544  |
| 2023   | 1.1149 | -0.4342 |         2.20558e+12 |  9.8235e+10  | 1.25313e+11 |        0.5676 |
| 2024   | 1.0891 | -0.4267 |         2.14358e+12 |  1.35923e+11 | 9.97953e+10 |        0.7761 |
| 2025   | 1.2277 | -0.4659 |         2.44338e+12 |  2.17347e+11 | 8.86712e+10 |        0.8611 |

---

## get_tail_ratio
Calculate the Tail Ratio of an investment portfolio or asset's returns.

The Tail Ratio compares the size of the right (gain) tail to the left (loss) tail of the return distribution. A Tail Ratio above 1 indicates that best-case gains outsize worst-case losses.

The formula is as follows (with the default alpha=0.05):

$$
\text{Tail Ratio} = \frac{\left|\operatorname{Quantile}(\text{Returns},\; 1 - \alpha)\right|}{\left|\operatorname{Quantile}(\text{Returns},\; \alpha)\right|}
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
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Tail Ratio values over time.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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

## get_skewness
Calculate the Skewness of an investment portfolio or asset's returns.

Skewness is a statistical measure used in finance to assess the asymmetry in the distribution of returns for an investment portfolio or asset over a defined period. It offers valuable insights into the shape of the return distribution, indicating whether returns are skewed towards the positive or negative side of the mean. Skewness is a crucial tool for investors and analysts seeking to understand the potential risk and return characteristics of an investment, aiding in the assessment of the distribution's tails and potential outliers. It provides a means to gauge the level of skew in returns, enabling more informed investment decisions and risk management strategies.

The formula is as follows:

$$
\text{Skewness} = \frac{n}{(n - 1) \cdot (n - 2)} \cdot \sum\left(\frac{\text{Return} - \text{Mean}}{\text{Std}}\right)^{3}
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
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Skewness values over time.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series: Skewness values with time as the index.

**Notes:**

- The method retrieves historical return data based on the specified `period` and calculates Skew for each
asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of Skewness values using the specified `lag`.
- Returns that do not vary (a constant price, such as a suspended stock) have no Skewness and give NaN.

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
\text{Excess Kurtosis} = \frac{n(n + 1)}{(n - 1) (n - 2) (n - 3)} \cdot \sum z^{4} - \frac{3(n - 1)^{2}}{(n - 2) (n - 3)}
$$

$$
z = \frac{\text{Return} - \text{Mean}}{\text{Std}}
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
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Kurtosis values over time.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series: Kurtosis values with time as the index.

**Notes:**

- The method retrieves historical return data based on the specified `period` and calculates Kurtosis for each
asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of Kurtosis values using the specified `lag`.
- Returns that do not vary (a constant price, such as a suspended stock) have no Kurtosis and give NaN.

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
\text{Hill Shape} \;(\xi) = \frac{1}{k} \cdot \sum(\ln X_{(i)} - \ln X_{(k+1)}) \;\text{for}\; i = 1,\; \ldots,\; k
$$

$$
\text{Hill Tail Index} = \frac{1}{\xi}
$$

$$
\text{Standard Error} = \frac{\text{Hill Tail Index}}{\sqrt{k}}
$$

Where $$X_{1} \geq X_{2} \geq \ldots$$ are the strictly positive losses (the negated returns, or the returns themselves for tail="right") sorted from large to small, and k is the number of order statistics used: int(0.1 * the number of positive losses) by default, or `k` itself when it is an integer.

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
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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

Where Var is the sample variance (ddof=1) and the trading days per period are 252 / 52 (weekly), 252 / 12 (monthly), 252 / 4 (quarterly) or 252 (yearly). A ticker with returns on weekends, such as a cryptocurrency, has a return on every calendar day and uses 365 days a year instead (365 / 52 weekly). With `rolling`, the result is the sample variance of the last `rolling` returns of the chosen period itself, without scaling.

**Also known as:** dispersion, spread.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (weekly, monthly, quarterly, or yearly). Defaults
to "quarterly" if the Toolkit is initialised with quarterly=True, otherwise "yearly".
- <u>rolling (int, optional):</u> The rolling window size to use for the calculation. If set,
Variance is calculated over a rolling window of this many periods (e.g. period='monthly'
and rolling=6 gives the rolling 6-month Variance) instead of one value per `period`.
Defaults to None.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Variance values over time. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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

## get_mean_absolute_deviation
Calculate the Mean Absolute Deviation (MAD) of an investment portfolio or asset's returns for a given period based on the daily historical returns.

MAD measures the average absolute distance of each return from the mean return. Unlike Variance and Volatility, it does not square the deviations, making it less sensitive to outliers.

The formula is as follows:

$$
\text{Mean Absolute Deviation} = \frac{\sum\left|\text{Return}_{t} - \text{Mean}\right|}{n}
$$

Where the returns are the n daily returns within each period, without scaling to the period length.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (weekly, monthly, quarterly, or yearly). Defaults
to "quarterly" if the Toolkit is initialised with quarterly=True, otherwise "yearly".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the MAD values over time. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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
\text{Coefficient of Variation} = \frac{\operatorname{Std}(\text{Daily Returns})}{\operatorname{Mean}(\text{Daily Returns})}
$$

Where both are taken over the daily returns within each period, with Std the sample standard deviation (ddof=1), without scaling to the period length.

**Also known as:** relative standard deviation.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (weekly, monthly, quarterly, or yearly). Defaults
to "quarterly" if the Toolkit is initialised with quarterly=True, otherwise "yearly".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the CV values over time. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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

## get_move_significance
Calculate how unusual each move of an investment portfolio or asset is: the return in units of its trailing volatility and of its trailing Value at Risk, its percentile among the earlier moves and the date of the last move at least as large in the same direction.

A return only says how far a price moved, not whether that is a lot for the asset: a 3% day is ordinary for a volatile growth stock and exceptional for a utility or an index. Dividing the return by the volatility of the returns before it (the "sigma" of a move) makes moves comparable across assets and calm or turbulent markets, the percentile says how many earlier moves were smaller, and "largest since" gives the familiar headline ("the biggest one-day fall since March 2020"). The VaR Multiple measures the move against the historic Value at Risk of the same earlier returns instead of their standard deviation, so it does not assume normal returns: a fall with a VaR Multiple below -1 is a VaR exceedance, worse than the loss the trailing VaR expected on all but a share alpha of days. When the trailing quantile is not a loss (every earlier return was a gain or nearly so), the VaR Multiple is NaN. Ties count half, as in `get_level_significance`.

The formula is as follows:

$$
\text{Volatility Multiple}(t) = \frac{\operatorname{Return}(t)}{\sigma(\operatorname{Return}(t - \text{window}),\; \ldots,\; \operatorname{Return}(t - 1))}
$$

$$
\text{VaR Multiple}(t) = \frac{\operatorname{Return}(t)}{\left|\operatorname{Quantile}(\operatorname{Return}(t - \text{window}),\; \ldots,\; \operatorname{Return}(t - 1) ; \alpha)\right|}
$$

$$
\operatorname{Percentile}(t) = \frac{\operatorname{Count}(\left|\operatorname{Return}(s)\right| < \left|\operatorname{Return}(t)\right|,\; s < t) + 0.5 \cdot \operatorname{Count}(\left|\operatorname{Return}(s)\right| = \left|\operatorname{Return}(t)\right|,\; s < t)}{\operatorname{Count}(s < t)}
$$

$$
\text{Largest Since}(t) = \max(s < t \text{:} \;\text{Return}(s) \leq \operatorname{Return}(t)) \;\text{if Return}(t) < 0
$$

$$
\text{Largest Since}(t) = \max(s < t \text{:} \;\text{Return}(s) \geq \operatorname{Return}(t)) \;\text{if Return}(t) > 0
$$

The volatility $$\sigma$$ uses ddof=1 and the quantile is the historic Value at Risk, interpolated linearly as in `get_value_at_risk`.

Each measure only uses the returns before the period itself, so a move is never part of the volatility or the history it is measured against (no look-ahead). Largest Since compares falls with falls and rises with rises, as a headline does: a 6% fall is the largest fall since the last fall of 6% or more, whatever the rises in between.

**Also known as:** sigma move, standardized return, biggest move since, return z-score, worst day since, VaR exceedance, VaR breach ratio.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly,
quarterly, or yearly). Defaults to "daily".
- <u>window (int &#124; None, optional):</u> The number of earlier returns the volatility is
measured over, which the percentile also needs at least. Defaults to None, which
uses a year of observations with a minimum of 20 (252 daily, 52 weekly and 20
monthly, quarterly or yearly returns).
- <u>alpha (float, optional):</u> The tail probability of the trailing historic Value at Risk
the VaR Multiple divides by (0.05 for the 95% VaR). Defaults to 0.05.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the rounding of the Toolkit (4 unless set otherwise).
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Return, Volatility Multiple, VaR Multiple, Percentile and Largest Since
(the date as text) per asset, with time as the index and the measures and tickers as the column
levels.

**Notes:**

- The returns are total returns (Adj Close), compounded within each period for a period
other than daily.
- `get_value_at_risk` reports the VaR as a return (negative for a loss); the VaR Multiple
divides by its size, so its sign is the move's, like the Volatility Multiple.
- The history a move is compared with starts at the Toolkit's start_date: the volatility,
the VaR and the percentile are NaN until `window` returns are available, and Largest Since is
NaN when no earlier move in the data was as large, which makes the move the largest
since the start_date. Choose an early start_date for a long history.
- Each ticker uses its own history, so a ticker that listed later starts later.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["NVDA", "KO"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2015-01-01",
    end_date="2025-12-31",
)

significance = toolkit.risk.get_move_significance()

significance.loc["2025-01-27"].unstack(level=0)
```

Which returns:

|           |   Return |   Volatility Multiple |   VaR Multiple |   Percentile | Largest Since   |
|:----------|---------:|----------------------:|---------------:|-------------:|:----------------|
| NVDA      |  -0.1697 |               -5.0682 |        -3.4613 |       0.9976 | 2020-03-16      |
| KO        |   0.0318 |                3.891  |         2.3363 |       0.9818 | 2022-11-10      |
| Benchmark |  -0.0141 |               -1.76   |        -1.026  |       0.8632 | 2025-01-10      |

---

## get_autocorrelation
Calculate the Autocorrelation Function (ACF) of each asset's daily returns for a range of lags.

The ACF measures the correlation between a return series and a lagged version of itself. A significant ACF at a given lag indicates that returns are not fully independent over time, which is relevant for assessing return predictability and volatility clustering (as opposed to a trading-signal use case, which is why this lives in the Risk module rather than Technicals).

The formula is as follows:

$$
\operatorname{ACF}(k) = \frac{\sum(r_{t} - \text{Mean}) \cdot (r_{t+k} - \text{Mean})}{\sum(r_{t} - \text{Mean})^{2}}
$$

Where $$r_{t}$$ are the n daily returns (missing values dropped), the numerator runs over $$t = 1$$, ..., n - k, the denominator over all n returns, and $$k = 1$$, ..., `lags` (10 by default).

**Args:**

- <u>lags (int, optional):</u> The number of lags to calculate the ACF for. Defaults to 10.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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

- $$H < 0.5$$: the series is mean-reverting (anti-persistent).
- $$H = 0.5$$: the series is a random walk (no memory).
- $$H > 0.5$$: the series is trending (persistent).

For liquid stocks the estimate is usually close to 0.5, and with lags of at most `max_lag` days it describes short-term behaviour only; a value of 0.45 or 0.55 over a few years is within estimation noise rather than evidence of a tradable pattern.

The formula is as follows (with the default max_lag=20):

$$
\sigma(\tau) = \operatorname{Std}(\ln P_{t+\tau} - \ln P_{t})
$$

$$
\ln \sigma(\tau) = c + H \cdot \ln \tau,\;\; \text{fitted by least squares over}\; \tau = 2,\; \ldots,\; 20
$$

Where P is the daily adjusted close, Std the population standard deviation (ddof=0) of the lagged log price differences and H, the slope, the Hurst Exponent.

**Args:**

- <u>max_lag (int, optional):</u> The maximum lag, included, to use when estimating the exponent:
the regression runs over the lags 2 up to and including `max_lag`. Defaults to 20.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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

## get_conditional_drawdown_at_risk
Calculate the Conditional Drawdown at Risk (CDaR) of an investment portfolio or asset's returns.

Conditional Drawdown at Risk (CDaR) extends the concept of Value at Risk and Conditional Value at Risk to the drawdown series instead of the return series. It is calculated as the average of the worst drawdowns that exceed the Drawdown at Risk (DaR), i.e. the alpha-quantile of the drawdown distribution, giving insight into the depth of the most severe drawdowns an investment portfolio or asset could experience.

The formula is as follows (with the default alpha=0.05):

$$
\operatorname{Wealth}(t) = \prod(1 + \operatorname{Return}(s)) \;\text{for}\; s \leq t
$$

$$
\operatorname{Drawdown}(t) = \frac{\operatorname{Wealth}(t)}{\max(1,\; \max(\operatorname{Wealth}(s) \;\text{for}\; s \leq t))} - 1
$$

$$
\text{DaR} = \operatorname{Quantile}(\text{Drawdown},\; \alpha)
$$

$$
\text{CDaR} = \operatorname{Mean}(\text{Drawdown} \mid \text{Drawdown} \leq \text{DaR})
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
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the CDaR values over time. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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
| 2021 |     -0.0629 | -0.1002 | -0.0421 |     -0.0414 |
| 2022 |     -0.2395 | -0.131  | -0.2429 |     -0.2341 |
| 2023 |     -0.091  | -0.0816 | -0.0833 |     -0.0805 |
| 2024 |     -0.0826 | -0.1616 | -0.0585 |     -0.0576 |
| 2025 |     -0.1185 | -0.1602 | -0.1445 |     -0.1432 |

---

## get_maximum_drawdown
Calculate the Maximum Drawdown (MDD) of an investment portfolio or asset's returns.

Maximum Drawdown (MDD) is a risk management metric that quantifies the largest historical loss of an investment portfolio or asset experienced over a specified time horizon. It provides insights into the downside risk associated with an investment and helps investors make informed decisions about risk tolerance.

The Maximum Drawdown is a single-path statistic: it depends entirely on the window chosen, so a figure over a window that includes a market crash and one over a window that starts after it are not comparable. It says how deep the worst fall was, not how long it lasted, which is why it is usually read together with the drawdown duration and recovery time (see `get_maximum_drawdown_duration` and `get_maximum_drawdown_recovery_time`), and it underlies return-to-risk ratios such as the Calmar ratio.

The formula is as follows:

$$
\operatorname{Wealth}(t) = \prod(1 + \operatorname{Return}(s)) \;\text{for}\; s \leq t
$$

$$
\operatorname{Drawdown}(t) = \frac{\operatorname{Wealth}(t)}{\max(1,\; \max(\operatorname{Wealth}(s) \;\text{for}\; s \leq t))} - 1
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
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Maximum Drawdown values over time.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the duration values over time. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the recovery time values over time.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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

## get_drawdown_series
Calculate the drawdown in every period: how far an asset stands below its highest value so far, or the gain it needs to get back there.

The drawdown series, also known as the underwater curve, shows the whole history of losses from a previous high instead of only the worst one. It is 0 at every new high and negative while the value is below one, so its lowest point is the Maximum Drawdown (see `get_maximum_drawdown`) and the stretches below 0 are the drawdowns that `get_drawdown_table` lists.

Losses and gains are not symmetric: after a fall of 20% the asset needs a gain of 25% to be back at its high, after a fall of 50% a gain of 100%. With recovery=True the series shows that gain, the return needed from each period's value to get back to the running peak.

With deepest_since=True every period below the peak also gets the last earlier date with a drawdown at least as deep, the familiar headline ("the deepest drawdown since April"), as `get_move_significance` gives the "largest since" date of a single move.

The formula is as follows:

$$
\operatorname{Wealth}(t) = \prod(1 + \operatorname{Return}(s)) \;\text{for}\; s \leq t
$$

$$
\operatorname{Peak}(t) = \max(1,\; \max(\operatorname{Wealth}(s) \;\text{for}\; s \leq t))
$$

$$
\operatorname{Drawdown}(t) = \frac{\operatorname{Wealth}(t)}{\operatorname{Peak}(t)} - 1
$$

$$
\text{Recovery Needed}(t) = \frac{\operatorname{Peak}(t)}{\operatorname{Wealth}(t)} - 1 = - \frac{\operatorname{Drawdown}(t)}{1 + \operatorname{Drawdown}(t)}
$$

$$
\text{Deepest Since}(t) = \text{the last date}\; s < t \;\text{with Drawdown}(s) \leq \operatorname{Drawdown}(t),\;\; \text{for Drawdown}(t) < 0
$$

Returns are total returns (Adj Close). Wealth starts at 1 at the first close of the window, so a decline from the start of the window counts as well.

**Also known as:** underwater curve, underwater plot, drawdown curve, distance from the high, gain needed to recover, breakeven return, recovery return.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>recovery (bool, optional):</u> Whether to return the gain needed to get back to the running peak
(Recovery Needed) instead of the drawdown. Defaults to False.
- <u>deepest_since (bool, optional):</u> Whether to add the Deepest Since date of every period below the
peak. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The drawdown per period as a negative decimal or, with recovery=True, the gain needed
as a positive decimal (0 at a new high), with time as the index. With deepest_since=True, the
columns hold the measures (Drawdown or Recovery Needed, and Deepest Since, the date as text)
and the tickers.

**Notes:**

- Each ticker keeps its own history: a ticker that listed during the window starts at its first close
and is NaN before it.
- A longer period only compares the closes of each period, so period="monthly" shows shallower
drawdowns than period="daily".
- Deepest Since is NaN at a high and when no earlier period in the data was as deep, which makes
the drawdown the deepest since the start_date. Choose an early start_date for a long history.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["META", "NFLX", "AMZN"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_drawdown_series(period="quarterly")
```

Which returns:

| Date   |    META |    NFLX |    AMZN |   Benchmark |
|:-------|--------:|--------:|--------:|------------:|
| 2021Q1 |  0      |  0      |  0      |      0      |
| 2021Q2 |  0      |  0      |  0      |      0      |
| 2021Q3 | -0.0239 |  0      | -0.0451 |      0      |
| 2021Q4 | -0.0327 | -0.0129 | -0.0308 |      0      |
| 2022Q1 | -0.3605 | -0.3862 | -0.0524 |     -0.0461 |
| 2022Q2 | -0.5362 | -0.7134 | -0.3825 |     -0.1998 |
| 2022Q3 | -0.6098 | -0.6143 | -0.3431 |     -0.2392 |
| 2022Q4 | -0.6539 | -0.5168 | -0.5116 |     -0.1817 |
| 2023Q1 | -0.3904 | -0.4339 | -0.3995 |     -0.1207 |
| 2023Q2 | -0.1746 | -0.2782 | -0.2421 |     -0.0443 |
| 2023Q3 | -0.1365 | -0.3813 | -0.261  |     -0.0751 |
| 2023Q4 |  0      | -0.2021 | -0.1168 |      0      |
| 2024Q1 |  0      | -0.0048 |  0      |      0      |
| 2024Q2 |  0      |  0      |  0      |      0      |
| 2024Q3 |  0      |  0      | -0.0358 |      0      |
| 2024Q4 |  0      |  0      |  0      |      0      |
| 2025Q1 | -0.0148 |  0      | -0.1328 |     -0.0427 |
| 2025Q2 |  0      |  0      |  0      |      0      |
| 2025Q3 | -0.0043 | -0.1047 |  0      |      0      |
| 2025Q4 | -0.1043 | -0.2998 |  0      |      0      |

---

## get_drawdown_table
List the largest drawdowns of each asset with their peak, trough and recovery dates, depth and length.

Where the Maximum Drawdown gives only the single worst decline, the drawdown table shows the largest declines side by side: when each started (the last high before it), when it bottomed out, when the asset was back at its high and how many periods each phase took. It shows whether an asset has one bad episode or recurring ones, and how long recoveries usually take, which a single figure hides. Recovery Needed is the gain needed from the trough to be back at the peak, which is larger than the drawdown itself: a 50% fall needs a 100% gain.

The formula is as follows:

$$
\operatorname{Drawdown}(t) = \frac{\operatorname{Wealth}(t)}{\max(1,\; \max(\operatorname{Wealth}(s) \;\text{for}\; s \leq t))} - 1
$$

$$
\text{To Trough} = t(\text{trough}) - t(\text{peak})
$$

$$
\text{To Recovery} = t(\text{recovery}) - t(\text{trough})
$$

$$
\text{Length} = t(\text{recovery}) - t(\text{peak})
$$

$$
\text{Recovery Needed} = - \frac{\text{Drawdown}}{1 + \text{Drawdown}}
$$

$$
\text{To Trough} \;(\text{Days}) = \operatorname{date}(\text{trough}) - \operatorname{date}(\text{peak}),\;\; \text{likewise To Recovery (Days) and Length (Days)}
$$

$$
\text{Length} \;(\text{Years}) = \frac{\text{Length} \;(\text{Days})}{365.25}
$$

The Drawdown is the drawdown series of `get_drawdown_series`. A drawdown runs from the Peak (the last period at a high) to the Recovery (the first period back at that high), with its Trough at the lowest Drawdown in between. To Trough, To Recovery and Length count periods (trading days for daily data), the columns marked (Days) count calendar days between the same dates (the last day of each period for weekly or longer periods), and Length (Years) is Length (Days) in years of 365.25 days. Calendar time compares assets on exchanges with other holidays, and reads as the time an investor waited.

Each drawdown is dated by its peak, valley and recovery, so it starts on the peak rather than on the first period below it. The deepest drawdown matches `get_maximum_drawdown`, `get_maximum_drawdown_duration` (To Trough) and `get_maximum_drawdown_recovery_time` (To Recovery).

**Also known as:** worst drawdowns, drawdown details, drawdown periods, gain needed to recover.

**Args:**

- <u>top (int, optional):</u> The number of drawdowns per asset, deepest first. Defaults to 5.
- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: One row per drawdown, indexed by ticker and rank, with the dates of the Peak, Trough
and Recovery, the Drawdown as a negative decimal, the gain needed from the trough back to the peak
(Recovery Needed) as a positive decimal, in periods the time from peak to trough
(To Trough), from trough to recovery (To Recovery) and from peak to recovery (Length), the
same in calendar days (To Trough (Days), To Recovery (Days), Length (Days)) and Length
(Years).

**Notes:**

- A drawdown that has not recovered by the end of the window has no Recovery, To Recovery or
Length, in periods or calendar time (NaN). Its Recovery Needed is the gain from its trough; the gain
still needed from the latest value is the last row of `get_drawdown_series(recovery=True)`.
- Each ticker keeps its own history: a ticker that listed during the window starts at its first close.
- The table depends on the window: a drawdown that started before the start date is measured from
the first close of the window.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["META", "NFLX"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_drawdown_table(top=3)
```

Which returns:

|                  | Peak       | Trough     | Recovery   |   Drawdown |   Recovery Needed |   To Trough |   To Recovery |   Length |   To Trough (Days) |   To Recovery (Days) |   Length (Days) |   Length (Years) |
|:-----------------|:-----------|:-----------|:-----------|-----------:|------------------:|------------:|--------------:|---------:|-------------------:|---------------------:|----------------:|-----------------:|
| ('META', 1)      | 2021-09-07 | 2022-11-03 | 2024-01-19 |    -0.7672 |            3.2955 |         293 |           302 |      595 |                422 |                  442 |             864 |           2.3655 |
| ('META', 2)      | 2025-02-14 | 2025-04-21 | 2025-06-30 |    -0.3416 |            0.5189 |          44 |            48 |       92 |                 66 |                   70 |             136 |           0.3723 |
| ('META', 3)      | 2025-08-12 | 2025-11-20 | NaT        |    -0.2537 |            0.34   |          71 |           nan |      nan |                100 |                  nan |             nan |         nan      |
| ('NFLX', 1)      | 2021-11-17 | 2022-05-11 | 2024-08-20 |    -0.7593 |            3.1548 |         120 |           571 |      691 |                175 |                  832 |            1007 |           2.757  |
| ('NFLX', 2)      | 2025-06-30 | 2025-12-10 | NaT        |    -0.3076 |            0.4443 |         114 |           nan |      nan |                163 |                  nan |             nan |         nan      |
| ('NFLX', 3)      | 2025-02-14 | 2025-04-04 | 2025-04-24 |    -0.1916 |            0.237  |          34 |            13 |       47 |                 49 |                   20 |              69 |           0.1889 |
| ('Benchmark', 1) | 2022-01-03 | 2022-10-12 | 2023-12-13 |    -0.245  |            0.3245 |         195 |           294 |      489 |                282 |                  427 |             709 |           1.9411 |
| ('Benchmark', 2) | 2025-02-19 | 2025-04-08 | 2025-06-26 |    -0.1877 |            0.2311 |          34 |            54 |       88 |                 48 |                   79 |             127 |           0.3477 |
| ('Benchmark', 3) | 2024-07-16 | 2024-08-05 | 2024-09-19 |    -0.0841 |            0.0918 |          14 |            32 |       46 |                 20 |                   45 |              65 |           0.178  |

---

## get_ulcer_index
The Ulcer Index is a financial metric used to assess the risk and volatility of an investment portfolio or asset. Developed by Peter Martin in the 1980s, the Ulcer Index is particularly useful for evaluating the downside risk and drawdowns associated with investments.

The Ulcer Index differs from traditional volatility measures like standard deviation or variance because it focuses on the depth and duration of drawdowns rather than the dispersion of returns.

The formula is as follows (with the default rolling=14):

$$
\text{Ulcer Index} = \sqrt{\frac{\sum\left(\frac{\operatorname{Wealth}(t) - \text{Highest High}(t)}{\text{Highest High}(t)}\right)^{2}}{n}}
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
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the UI values over time. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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
| 2021 | 0.0564 |   0.041  |      0.0131 |
| 2022 | 0.0917 |   0.0606 |      0.0481 |
| 2023 | 0.0442 |   0.0289 |      0.0198 |
| 2024 | 0.0696 |   0.0426 |      0.0164 |
| 2025 | 0.0642 |   0.0503 |      0.027  |

---

## get_pain_index
The Pain Index, developed by Zephyr Associates and described by Bacon (2013), measures the downside risk of an investment portfolio or asset as the average depth of its drawdowns over every day of a period, the days at a new high counting as a drawdown of 0.

Like the Ulcer Index it grows with both the depth and the duration of the drawdowns, so an asset that falls 10% and stays there for months scores worse than one that drops 10% and recovers within a week. Where the Ulcer Index takes the root mean square of the drawdowns, which makes the deepest ones dominate, the Pain Index takes their plain average: the area under water divided by the number of days. It is the risk measure behind the Pain Ratio (excess return divided by the Pain Index, see `toolkit.performance.get_pain_ratio`).

The formula is as follows:

$$
\operatorname{Wealth}(t) = \prod(1 + \operatorname{Return}(s)) \;\text{for}\; s \leq t
$$

$$
\operatorname{Drawdown}(t) = \frac{\operatorname{Wealth}(t)}{\max(1,\; \max(\operatorname{Wealth}(s) \;\text{for}\; s \leq t))} - 1
$$

$$
\text{Pain Index} = \frac{\sum\left|\operatorname{Drawdown}(t)\right|}{n}
$$

Where Wealth(t) compounds the daily returns within each period from a starting value of 1, so a loss on the first day of the period is a drawdown as well, the drawdowns are measured from the highest wealth since the start of the period and n is the number of daily returns in the period. The result is a positive decimal (0.05 is an average drawdown of 5%). Each ticker is measured over its own trading days, and the days before its first or after its last return (a later listing, a delisting) are no observations of it.

For more information, see the following sources:

- Bacon, C.R. (2013). "Practical Risk-Adjusted Performance Measurement." John Wiley & Sons, chapter 5 (the Pain Index of Zephyr Associates).
- PerformanceAnalytics (R), `PainIndex`.

**Also known as:** average drawdown, mean drawdown.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly, or yearly).
Defaults to "quarterly" if the Toolkit is initialised with quarterly=True, otherwise "yearly".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Pain Index values over time. Defaults
to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Pain Index values with the periods as index and the tickers as columns.

**Notes:**

- The method retrieves the daily returns within each `period` and calculates the Pain Index for each
asset in the Toolkit instance.
- If `growth` is set to True, the method calculates the growth of the Pain Index values using the
specified `lag`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["BA", "AIR.PA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_pain_index()
```

Which returns:

|      |     BA |   AIR.PA |   Benchmark |
|:-----|-------:|---------:|------------:|
| 2021 | 0.1321 |   0.0404 |      0.009  |
| 2022 | 0.2629 |   0.1135 |      0.139  |
| 2023 | 0.0702 |   0.031  |      0.0223 |
| 2024 | 0.3182 |   0.1191 |      0.0113 |
| 2025 | 0.0715 |   0.0447 |      0.0278 |

---

## get_amihud_illiquidity
Calculate the Amihud (2002) Illiquidity ratio, per asset.

The Amihud ratio measures the average price impact of trading -- how much the price moves per dollar of trading volume. A high value means that even a small amount of trading moves the price a lot (the asset is illiquid), while a low value means the asset can absorb a large amount of trading with little price impact (the asset is liquid).

The Amihud ratio is mainly a cross-sectional measure: it ranks stocks by how much a given dollar volume moves the price and is used as a liquidity factor in asset pricing. Its level depends on the scale, the frequency and the price level of the market, so compare stocks within the same market and period, and expect the ratio of large caps to be several orders of magnitude below that of small caps.

For more information about the method, see the following paper:

- Amihud, Y. (2002). "Illiquidity and Stock Returns: Cross-Section and Time-Series Effects." Journal of Financial Markets, 5(1), 31-56.

The formula is as follows (with the default scale of 1,000,000):

$$
\text{Amihud Illiquidity} = \operatorname{Mean}\left(\frac{\left|\text{Return}_{t}\right|}{\text{Close}_{t} \cdot \text{Volume}_{t}}\right) \cdot \text{1,000,000}
$$

Where the mean runs over the periods of the chosen frequency (within each period with `within_period`), and periods without dollar volume are skipped.

**Also known as:** Amihud illiquidity ratio, ILLIQ, price impact ratio.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>within_period (bool, optional):</u> Whether to calculate the ratio within the specified period or
for the entire period. Defaults to False. Note that this requires intraday data when period = 'daily', since a
single day only nests observations when intraday data was fetched.
- <u>scale (float, optional):</u> A multiplier applied to the resulting ratio purely for readability.
Defaults to 1,000,000.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Amihud Illiquidity values over
time. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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
\text{Roll Spread} = 2 \cdot \sqrt{- \operatorname{Cov}(\Delta P_{t},\; \Delta P_{t-1})}
$$

$$
\text{Relative Roll Spread} = \frac{\text{Roll Spread}}{\operatorname{Mean}(P)}
$$

Where P is the Close price, $$\Delta P_{t} = P_{t} - P_{t - 1}$$ and Cov the sample autocovariance (ddof=1) of consecutive price changes; a covariance of zero or above gives NaN.

**Also known as:** Roll's implied spread, Roll measure.

**Args:**

- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>within_period (bool, optional):</u> Whether to calculate the spread within the specified period or
for the entire period. Defaults to False. Note that this requires intraday data when period = 'daily', since a
single day only nests observations when intraday data was fetched.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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

## get_corwin_schultz_spread
Calculate the Corwin and Schultz (2012) high-low bid-ask spread, per asset and period.

The daily High is almost always a trade at the ask and the daily Low a trade at the bid, so the range of a day holds both the volatility and the bid-ask spread. The volatility part of the range grows with the length of the window while the spread part does not, so comparing the ranges of two single days with the range over both days together backs out the spread from daily High and Low prices alone, without quote data. Each pair of consecutive trading days gives an estimate and the spread of a period is the average of the estimates within it.

The estimator is mostly used where no quotes are available (historical studies, smaller markets) and ranks stocks well by their spread. For liquid large caps the spread is a few basis points and the estimate is dominated by the volatility within the day, so read it as a relative measure.

For more information about the method, see the following paper:

- Corwin, S. A., & Schultz, P. (2012). "A Simple Way to Estimate Bid-Ask Spreads from Daily High and Low Prices." The Journal of Finance, 67(2), 719-760.

The formula is as follows:

$$
\beta = \left[\ln\left(\frac{H_{t}}{L_{t}}\right)\right]^{2} + \left[\ln\left(\frac{H_{t+1}}{L_{t+1}}\right)\right]^{2}
$$

$$
\gamma = \left[\ln\left(\frac{\max(H_{t},\; H_{t+1})}{\min(L_{t},\; L_{t+1})}\right)\right]^{2}
$$

$$
\alpha = \frac{\sqrt{2 \beta} - \sqrt{\beta}}{3 - 2 \sqrt{2}} - \sqrt{\frac{\gamma}{3 - 2 \sqrt{2}}}
$$

$$
\text{Two-Day Spread} = \max\left(\frac{2 \cdot (e^{\alpha} - 1)}{1 + e^{\alpha}},\; 0\right)
$$

$$
\text{Corwin-Schultz Spread} = \operatorname{Mean}(\text{Two-Day Spreads within the period})
$$

Where H and L are the daily High and Low of two consecutive trading days t and t+1 of the asset. Before $$\beta$$ and $$\gamma$$ are calculated, day t+1 is adjusted for the overnight return as in the paper: when its Low is above the Close of day t, its High and Low are lowered by the difference, and when its High is below that Close, they are raised by the difference. A negative two-day spread is set to 0, the paper's main convention, before the average is taken.

**Also known as:** high-low spread estimator, HL spread, CS spread.

**Args:**

- <u>period (str, optional):</u> The period to average the two-day spreads over (weekly, monthly, quarterly
or yearly). Defaults to "monthly", as in the paper.
- <u>rolling (int, optional):</u> Average the two-day spreads of the last `rolling` periods instead of one
period (e.g. period='monthly' and rolling=3 for a three-month spread at every month end).
Defaults to None.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the spread over time. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The spread as a decimal of the price (0.005 is 0.5%), with the periods as the index
and the assets as columns.

**Notes:**

- The method uses the daily High, Low and Close (split-adjusted) of each asset on its own trading
days: a day on which only another ticker or the benchmark traded is not part of a pair, so the pair
is always two consecutive trading days of the asset.
- Both days of a pair fall within the period; a pair across two periods is left out.
- A day with a price of 0 or below (a bad bar) is left out.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["SNAP", "ETSY", "LYFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-06-30",
)

toolkit.risk.get_corwin_schultz_spread()
```

Which returns:

| Date    |   SNAP |   ETSY |   LYFT |   Benchmark |
|:--------|-------:|-------:|-------:|------------:|
| 2025-01 | 0.0106 | 0.0086 | 0.0095 |      0.0017 |
| 2025-02 | 0.011  | 0.0117 | 0.0115 |      0.002  |
| 2025-03 | 0.0119 | 0.0096 | 0.0151 |      0.0046 |
| 2025-04 | 0.0173 | 0.0174 | 0.0183 |      0.0099 |
| 2025-05 | 0.0098 | 0.0086 | 0.0096 |      0.0031 |
| 2025-06 | 0.0111 | 0.0067 | 0.0155 |      0.0024 |

---

## get_abdi_ranaldo_spread
Calculate the Abdi and Ranaldo (2017) close-high-low bid-ask spread, per asset and period.

The average of the daily High and Low (the mid-range) is a proxy for the efficient price without the spread, while the Close is a trade at either the bid or the ask. The distance of the Close to the mid-range of its own day and to that of the next day both hold half the spread, and their product removes the volatility of the efficient price, which backs out the spread from daily Close, High and Low prices alone, without quote data. Each pair of consecutive trading days gives an estimate and the spread of a period is the average of the estimates within it.

Unlike the Corwin-Schultz spread, the estimator uses the Close as well and needs no adjustment for the overnight return (a weekend or a gap at the open). Like it, the estimate is mostly used where no quotes are available and ranks assets by their spread; for liquid large caps the spread is a few basis points and the estimate is dominated by the volatility, so read it as a relative measure.

For more information about the method, see the following paper:

- Abdi, F., & Ranaldo, A. (2017). "A Simple Estimation of Bid-Ask Spreads from Daily Close, High, and Low Prices." The Review of Financial Studies, 30(12), 4437-4480.

The formula is as follows:

$$
\eta_{t} = \frac{\ln H_{t} + \ln L_{t}}{2}
$$

$$
\text{Two-Day Spread} = \sqrt{\max(4 \cdot (\ln C_{t} - \eta_{t}) \cdot (\ln C_{t} - \eta_{t+1}),\; 0)}
$$

$$
\text{Abdi-Ranaldo Spread} = \operatorname{Mean}(\text{Two-Day Spreads within the period})
$$

Where H, L and C are the daily High, Low and Close of two consecutive trading days t and t+1 of the asset. This is the "two-day corrected" version that the paper uses in its empirical analysis (equation 11): a negative two-day estimate of the squared spread is set to 0 before the square root and the average are taken.

**Also known as:** close-high-low spread estimator, CHL spread, AR spread.

**Args:**

- <u>period (str, optional):</u> The period to average the two-day spreads over (weekly, monthly, quarterly
or yearly). Defaults to "monthly", as in the paper.
- <u>rolling (int, optional):</u> Average the two-day spreads of the last `rolling` periods instead of one
period (e.g. period='monthly' and rolling=3 for a three-month spread at every month end).
Defaults to None.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the spread over time. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The spread as a decimal of the price (0.005 is 0.5%), with the periods as the index
and the assets as columns.

**Notes:**

- The method uses the daily High, Low and Close (split-adjusted) of each asset on its own trading
days: a day on which only another ticker or the benchmark traded is not part of a pair, so the pair
is always two consecutive trading days of the asset.
- Both days of a pair fall within the period; a pair across two periods is left out.
- A day with a price of 0 or below (a bad bar) is left out.
- Averaging the square roots of the two-day estimates lowers the level when the daily volatility
is large relative to the spread (in simulations with a 1% spread and a 1% daily volatility the
estimate is about 0.8%). The paper accepts this for the closer correlation with the effective
spread from trade and quote data; `get_edge_spread` has no such bias.
- The paper discards months with fewer than 12 applicable days; no such minimum is applied here,
as for `get_corwin_schultz_spread`, so a period with a single pair has an estimate.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["SNAP", "ETSY", "LYFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-06-30",
)

toolkit.risk.get_abdi_ranaldo_spread()
```

Which returns:

| Date    |   SNAP |   ETSY |   LYFT |   Benchmark |
|:--------|-------:|-------:|-------:|------------:|
| 2025-01 | 0.0115 | 0.0107 | 0.0084 |      0.0024 |
| 2025-02 | 0.014  | 0.0087 | 0.0176 |      0.0035 |
| 2025-03 | 0.0117 | 0.0065 | 0.0113 |      0.0053 |
| 2025-04 | 0.0287 | 0.0116 | 0.0284 |      0.013  |
| 2025-05 | 0.0168 | 0.0112 | 0.0137 |      0.0047 |
| 2025-06 | 0.0109 | 0.007  | 0.0101 |      0.0029 |

---

## get_edge_spread
Calculate the EDGE bid-ask spread of Ardia, Guidotti and Kroencke (2024), per asset and period.

EDGE (the Efficient Discrete Generalized Estimator) estimates the spread from the daily Open, High, Low and Close. The mid-range (the average of the High and Low) is a proxy for the efficient price, while the Open and the Close are trades at the bid or the ask, so the returns between them around the open and around the close bounce with the spread. Four such estimators, two at the open and two at the close (one of them a generalization of the Abdi-Ranaldo spread), are combined with the weights of the Generalized Method of Moments that minimize the variance of the estimate. The probabilities in the formula correct for days without trades, which repeat the previous Close. The estimate is asymptotically unbiased and, in the paper's simulations and empirical tests, more precise than the Roll, Corwin-Schultz and Abdi-Ranaldo estimators.

Unlike the Corwin-Schultz and Abdi-Ranaldo spreads, which average two-day estimates, EDGE is estimated from all pairs of consecutive trading days of the period at once. For liquid large caps the spread is a few basis points, close to the estimation error, so read it as a relative measure there.

For more information about the method, see the following paper:

- Ardia, D., Guidotti, E., & Kroencke, T. A. (2024). "Efficient Estimation of Bid-Ask Spreads from Open, High, Low, and Close Prices." Journal of Financial Economics, 161, 103916.

The formula is as follows:

$$
\eta_{t} = \frac{h_{t} + l_{t}}{2}\;\;\text{and}\;\; \tau_{t} = 1 \;\text{if}\; h_{t} \text{≠} l_{t} \;\text{or}\; l_{t} \text{≠} c_{t-1},\;\; \text{else 0}
$$

$$
\pi_{o} = - \frac{8}{P\left[o_{t} \text{≠} h_{t},\; \tau_{t} = 1\right] + P\left[o_{t} \text{≠} l_{t},\; \tau_{t} = 1\right]}
$$

$$
\pi_{c} = - \frac{8}{P\left[c_{t-1} \text{≠} h_{t-1},\; \tau_{t} = 1\right] + P\left[c_{t-1} \text{≠} l_{t-1},\; \tau_{t} = 1\right]}
$$

$$
x_{1} = \frac{\pi_{o}}{2} \cdot (\eta_{t} - o_{t}) \cdot (o_{t} - \eta_{t-1}) + \frac{\pi_{c}}{2} \cdot (\eta_{t} - c_{t-1}) \cdot (c_{t-1} - \eta_{t-1})
$$

$$
x_{2} = \frac{\pi_{o}}{2} \cdot (\eta_{t} - o_{t}) \cdot (o_{t} - c_{t-1}) + \frac{\pi_{c}}{2} \cdot (o_{t} - c_{t-1}) \cdot (c_{t-1} - \eta_{t-1})
$$

$$
S^{2} = \frac{\text{Var}\left[x_{2}\right] \cdot E\left[x_{1}\right] + \text{Var}\left[x_{1}\right] \cdot E\left[x_{2}\right]}{\text{Var}\left[x_{1}\right] + \text{Var}\left[x_{2}\right]}
$$

$$
\text{EDGE Spread} = \sqrt{\max(S^{2},\; 0)}
$$

Where o, h, l and c are the log Open, High, Low and Close of two consecutive trading days t-1 and t of the asset, and the probabilities, expectations and variances are taken over the pairs within the period. The returns $$\eta_{t} - o_{t}$$, $$\eta_{t} - c_{t - 1}$$ and $$o_{t} - c_{t - 1}$$ in the first factor of each product are de-meaned over the pairs with $$\tau_{t} = 1$$, as in the authors' implementation. A negative squared spread of the period is set to 0, as in the paper (equation 26); setting the period's estimate rather than each two-day estimate to 0 keeps the estimate consistent.

**Also known as:** Efficient Discrete Generalized Estimator, EDGE estimator, OHLC spread estimator.

**Args:**

- <u>period (str, optional):</u> The period to estimate the spread over (weekly, monthly, quarterly or
yearly). Defaults to "monthly", as in the paper.
- <u>rolling (int, optional):</u> Estimate the spread from the pairs of the last `rolling` periods together
instead of one period (e.g. period='monthly' and rolling=3 for a three-month spread at every
month end). Defaults to None.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the spread over time. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The spread as a decimal of the price (0.005 is 0.5%), with the periods as the index
and the assets as columns.

**Notes:**

- The method uses the daily Open, High, Low and Close (split-adjusted) of each asset on its own
trading days: a day on which only another ticker or the benchmark traded is not part of a pair, so
the pair is always two consecutive trading days of the asset.
- Both days of a pair fall within the period; a pair across two periods is left out, also in a
rolling window.
- A day with a price of 0 or below (a bad bar) is left out.
- A period with fewer than two pairs with a price change, or in which the Open (or the previous
Close) equals both the High and the Low on every pair with a price change (only single-price days),
is NaN.
- The estimates equal those of the authors' `bidask` package (`edge` on the days of the period,
with negative squared spreads set to 0).

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["SNAP", "ETSY", "LYFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-06-30",
)

toolkit.risk.get_edge_spread()
```

Which returns:

| Date    |   SNAP |   ETSY |   LYFT |   Benchmark |
|:--------|-------:|-------:|-------:|------------:|
| 2025-01 | 0      | 0.0032 | 0      |      0.0019 |
| 2025-02 | 0.0121 | 0      | 0.0296 |      0.0045 |
| 2025-03 | 0      | 0      | 0      |      0.003  |
| 2025-04 | 0.0245 | 0.0176 | 0.0219 |      0.0135 |
| 2025-05 | 0.0173 | 0.0134 | 0      |      0.007  |
| 2025-06 | 0      | 0      | 0.0061 |      0.0017 |

---

## get_share_turnover
Calculate the Share Turnover, the number of shares traded relative to the number of shares outstanding, per asset and period.

Datar, Naik and Radcliffe (1998) use the turnover as a liquidity proxy: a share that changes hands often can be traded at a lower cost. They find that stocks with a lower turnover earn higher returns, also after controlling for size, the book-to-market ratio and the market beta. The turnover of a period is the share of the outstanding shares that was traded in it, the sum of the daily turnover within the period.

The paper measures the turnover per month and averages it over the three months before the month of the returns, which `rolling=3` gives with the default monthly period. A turnover of 0.1 means that 10% of the shares outstanding changed hands; a value above 1 means more shares were traded than there are outstanding.

For more information about the method, see the following paper:

- Datar, V. T., Naik, N. Y., & Radcliffe, R. (1998). "Liquidity and Stock Returns: An Alternative Test." Journal of Financial Markets, 1(2), 203-219.

The formula is as follows:

$$
\text{Daily Turnover} = \frac{\text{Volume}_{t}}{\text{Weighted Average Shares}_{t}}
$$

$$
\text{Share Turnover} = \sum(\text{Daily Turnover within the period})
$$

Where Volume is the number of shares traded on day t and Weighted Average Shares the number of shares of the last fiscal period that ended on or before day t. With `rolling`, the result is the mean of the Share Turnover of the last `rolling` periods.

**Also known as:** turnover ratio, share turnover rate, trading turnover.

**Args:**

- <u>period (str, optional):</u> The period to sum the daily turnover over (weekly, monthly, quarterly or
yearly). Defaults to "monthly", as in the paper.
- <u>rolling (int, optional):</u> The mean of the turnover of the last `rolling` periods instead of the
turnover per period (e.g. rolling=3 for the paper's three-month average). Defaults to None.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the turnover over time. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The Share Turnover as a decimal, with the periods as the index and the assets as
columns.

**Notes:**

- The number of shares is the Weighted Average Shares of the income statement, the share count the
Toolkit's market capitalization uses as well. Each period's figure applies from the end of its fiscal
period (from the filing day with point_in_time), so a day never uses a share count that was not yet
reported. The days before the first fiscal period end in the statements have no share count, so a
period with such a day is NaN rather than a partial sum, as is a period with a trading day without a
positive share count.
- The Volume is that of the asset's own trading days. The benchmark and other assets without
financial statements are NaN.
- The share count is not adjusted within a fiscal period, so a stock split during a period changes the
turnover until the statements of the period after the split apply.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["SNAP", "ETSY", "LYFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-06-30",
)

toolkit.risk.get_share_turnover()
```

Which returns:

| Date    |   SNAP |   ETSY |   LYFT |   Benchmark |
|:--------|-------:|-------:|-------:|------------:|
| 2025-01 | 0.3433 | 0.4878 | 0.7121 |         nan |
| 2025-02 | 0.3536 | 0.6891 | 1.2397 |         nan |
| 2025-03 | 0.3493 | 0.7956 | 0.905  |         nan |
| 2025-04 | 0.5942 | 0.9174 | 0.7491 |         nan |
| 2025-05 | 0.4435 | 0.8986 | 1.1707 |         nan |
| 2025-06 | 0.4057 | 1.2026 | 0.6827 |         nan |

---

## get_idiosyncratic_volatility
Calculate the Idiosyncratic Volatility, the volatility of the part of the returns the factors do not explain, per asset and period.

Ang, Hodrick, Xing and Zhang (2006) regress the daily excess returns of every stock on the Fama and French three factors within each month and take the standard deviation of the residuals. Stocks with a high idiosyncratic volatility earn strikingly low returns in the following month, the idiosyncratic volatility puzzle: a diversified investor is not exposed to this risk, so it should not be priced at all, let alone negatively. With model="capm" the regression is the market model on the excess return of the benchmark instead.

For more information about the method, see the following paper:

- Ang, A., Hodrick, R. J., Xing, Y., & Zhang, X. (2006). "The Cross-Section of Volatility and Expected Returns." The Journal of Finance, 61(1), 259-299.

The formula is as follows (with the default model="fama_french"):

$$
\text{Excess Return}_{t} = \alpha + \beta_{1} \cdot (\text{Mkt-RF}) \;\text{}_{t} + \beta_{2} \cdot \text{SMB}_{t} + \beta_{3} \cdot \text{HML}_{t} + \epsilon_{t}
$$

$$
\text{Idiosyncratic Volatility} = \operatorname{Std}(\epsilon_{t}) \cdot \sqrt{\text{Trading Days per Period}}
$$

And with model="capm":

$$
\text{Excess Return}_{t} = \alpha + \beta \cdot \text{Benchmark Excess Return}_{t} + \epsilon_{t}
$$

Where the regression runs on the daily returns within the period, Std is the sample standard deviation (ddof=1) of the residuals and the trading days per period are 252 / 12 (monthly), 252 / 4 (quarterly) or 252 (yearly), the scaling of the Volatility of the Risk module; with annualize=True it is √252 for every period. A period with fewer than 15 daily returns (the paper's minimum) is NaN.

**Also known as:** IVOL, idiosyncratic risk, residual volatility, specific risk.

**Args:**

- <u>period (str, optional):</u> The period each regression runs within (monthly, quarterly or yearly).
Defaults to "monthly", as in the paper.
- <u>model (str, optional):</u> The factors to regress on: "fama_french" for the Fama and French three
factors (Mkt-RF, SMB, HML) or "capm" for the excess return of the benchmark. Defaults to
"fama_french".
- <u>rolling (int, optional):</u> Regress on the daily returns of the last `rolling` periods instead of one
period (e.g. period='monthly' and rolling=12 for a one-year window at every month end).
Defaults to None.
- <u>annualize (bool, optional):</u> Whether to scale the daily standard deviation of the residuals to a
year (√252) instead of to the period. Defaults to False.
- <u>region (str, optional):</u> The region whose Fama and French factors to use with model="fama_french":
"United States", "Developed", "Developed ex US", "Europe", "Japan", "Asia Pacific ex Japan"
or "North America". Every region's factors are U.S. dollar returns. Defaults to
"United States".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Idiosyncratic Volatility over time.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The Idiosyncratic Volatility, with the periods as the index and the assets as
columns.

**Notes:**

- The returns are the daily returns of the Adjusted Close on the asset's own trading days.
- With model="fama_french", the excess return is the return minus the risk-free rate (RF) of the
Fama and French dataset, the one-month Treasury bill the factors are built with, as in the paper.
The dataset is published with a delay of a month or more, so the most recent periods are NaN.
- With model="capm", the excess returns are taken over the risk-free rate of the Toolkit, an annually
compounded yield converted to a daily rate with (1 + rate)^(1 / 252) - 1, and the benchmark itself is
left out, as its residuals are 0.
- The regression runs on the days with a return for both the asset and every factor.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "TSLA", "KO"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-06-30",
)

toolkit.risk.get_idiosyncratic_volatility()
```

Which returns:

| Date    |   AAPL |   TSLA |     KO |   Benchmark |
|:--------|-------:|-------:|-------:|------------:|
| 2025-01 | 0.077  | 0.1089 | 0.0393 |      0.0015 |
| 2025-02 | 0.0598 | 0.1275 | 0.0602 |      0.0028 |
| 2025-03 | 0.0576 | 0.168  | 0.0413 |      0.0037 |
| 2025-04 | 0.0545 | 0.1187 | 0.053  |      0.011  |
| 2025-05 | 0.0659 | 0.0962 | 0.0457 |      0.0035 |
| 2025-06 | 0.043  | 0.188  | 0.0286 |      0.0023 |

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
z_{cf} = z + \frac{(z^{2} - 1) \cdot S}{6} + \frac{(z^{3} - 3 \cdot z) \cdot K}{24} - \frac{(2 \cdot z^{3} - 5 \cdot z) \cdot S^{2}}{36}
$$

$$
\text{Student-T VaR} = \text{Location} + \text{Scale} \cdot t_{v}^{-1} (\alpha)
$$

$$
\text{EVT VaR} = - \left(u + \frac{\text{Scale}_{\text{GPD}}}{\xi} \cdot \left(\left(\frac{\alpha}{p}\right)^{- \xi} - 1\right)\right)
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
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
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
The fit needs at least 10 losses above the threshold (about 200 returns at 0.95); a period
with fewer is NaN, with a logged warning. Defaults to 0.95.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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
| 2021 |  -0.0626 |  -0.0838 | -0.013  |     -0.0126 |
| 2022 |  -0.0574 |  -0.0742 | -0.0264 |     -0.0263 |
| 2023 |  -0.0312 |  -0.0374 | -0.0138 |     -0.0138 |
| 2024 |  -0.0407 |  -0.0533 | -0.0134 |     -0.0132 |
| 2025 |  -0.0358 |  -0.0569 | -0.0161 |     -0.0165 |

---

## get_conditional_value_at_risk
Calculate the Conditional Value at Risk (CVaR) of an investment portfolio or asset's returns.

Conditional Value at Risk (CVaR) is a risk management metric that quantifies the loss in the worst % of cases of an investment portfolio or asset may experience over a specified time horizon and confidence level. It provides insights into the downside risk associated with an investment and helps investors make informed decisions about risk tolerance.

The CVaR is calculated as the expected loss given that the loss threshold (VaR) with a given confidence level (e.g., 5% for alpha=0.05) is exceeded.

The Conditional Value at Risk (expected shortfall) is the measure banks report for market risk under the Basel framework, at 97.5% rather than 95% confidence, because unlike VaR it accounts for the size of the losses in the tail and never penalises diversification (it is subadditive). With daily data the estimate rests on few observations (one year at 95% leaves about 12 days in the tail), so a single extreme day can move it a lot; a longer window or a parametric distribution gives a steadier figure.

The formula is as follows (with the default distribution="historic" and alpha=0.05):

$$
\text{CVaR} = \operatorname{Mean}(\text{Returns} \mid \text{Returns} \leq \text{VaR})
$$

$$
\text{VaR} = \operatorname{Quantile}(\text{Returns},\; \alpha)
$$

The quantile interpolates linearly and the CVaR is reported as a return (negative for a loss). The other distributions use closed forms, with Std the sample standard deviation (ddof=1) and $$z_{\alpha}$$ the standard normal quantile at alpha:

$$
\text{Gaussian CVaR} = \text{Mean} - \frac{\text{Std} \cdot \operatorname{pdf}(z_{\alpha})}{\alpha}
$$

$$
\text{Student-T CVaR} = \text{Location} - \frac{\frac{\text{Scale} \cdot (v + t^{2})}{v - 1} \cdot \text{pdf}_{v}(t)}{\alpha},\;\; \text{with}\;\; t = t_{v}^{-1} (1 - \alpha)
$$

$$
\text{Laplace CVaR} = \text{Mean} - b \cdot (1 - \ln(2 \cdot \alpha)),\;\; \text{with}\;\; b = \frac{\text{Std}}{\sqrt{2}}
$$

$$
\text{Logistic CVaR} = \text{Mean} - s \cdot \ln\left(\frac{(1 - \alpha)^{1 - \frac{1}{\alpha}}}{\alpha}\right),\;\; \text{with}\;\; s = \frac{\text{Std} \cdot \sqrt{3}}{\pi}
$$

$$
\text{Cornish-Fisher CVaR} = \text{Mean of} \;(\text{Mean} + z_{cf}(p) \cdot \text{Std}) \;\text{over}\; \text{1,000} \;\text{evenly spaced}\; p \;\text{in} \;(0,\; \alpha)
$$

$$
\text{EVT CVaR} = - \frac{\text{VaR}_{\text{loss}} + \text{Scale}_{\text{GPD}} - \xi \cdot u}{1 - \xi}
$$

Where the Student-T v, Location and Scale are fitted by maximum likelihood (NaN for v <= 1), $$z_{\text{cf}}$$ is the Cornish-Fisher quantile of `get_value_at_risk`, and u, xi, Scale_GPD and $$\text{VaR}_{\text{loss}}$$ are the loss threshold, the fitted Generalized Pareto shape and scale and the EVT VaR as a positive loss (NaN for xi >= 1).

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
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
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
The fit needs at least 10 losses above the threshold (about 200 returns at 0.95); a period
with fewer is NaN, with a logged warning. Defaults to 0.95.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the CVaR values over time. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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

## get_marginal_value_at_risk
Calculate the Marginal Value at Risk (Marginal VaR) of each asset in a portfolio.

Ordinary VaR (see `get_value_at_risk`) treats each asset in isolation. Marginal VaR instead measures how much the *portfolio's* VaR would change for an infinitesimal increase in a given asset's portfolio weight - i.e. the sensitivity of portfolio risk to each holding, not the risk of the holding on its own.

The formula is as follows (with the default distribution="historic"):

$$
\text{Portfolio Return} = \sum(\text{weight}_{i} \cdot \text{Return}_{i})
$$

$$
\text{Beta}_{i} = \frac{\operatorname{Cov}(\text{Return}_{i},\; \text{Portfolio Return})}{\operatorname{Var}(\text{Portfolio Return})}
$$

$$
\text{Marginal VaR}_{i} = \text{Beta}_{i} \cdot \text{Portfolio VaR}
$$

Where the weights are normalized to sum to 1, the covariance and variance are sample estimates (ddof=1) on the dates all assets have a return (the returns of a date only some of them traded on are compounded into the next date all of them traded on), and Portfolio VaR is the VaR of the portfolio return under `distribution` (see `get_value_at_risk`). The beta-based sensitivity is exact for a zero-mean elliptical distribution and an approximation otherwise; distribution="gaussian" uses the exact derivative instead, with $$z_{\alpha}$$ the standard normal quantile at alpha:

$$
\text{Gaussian Marginal VaR}_{i} = \text{Mean}_{i} + \frac{z_{\alpha} \cdot \operatorname{Cov}(\text{Return}_{i},\; \text{Portfolio Return})}{\operatorname{Std}(\text{Portfolio Return})}
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
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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
\sum(\text{Component VaR}_{i}) = \text{Portfolio VaR}
$$

Where the weights are normalized to sum to 1 and Marginal $$\text{VaR}_{i}$$ is that of `get_marginal_value_at_risk`: Beta_i * Portfolio VaR by default, or the exact derivative with distribution="gaussian".

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
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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

The formula is as follows (with the default distribution="historic", alpha=0.05 and daily returns, for which the window is 252):

$$
\text{VaR}_{t} = \operatorname{Quantile}(\text{Return}_{t-252},\; \ldots,\; \text{Return}_{t-1} ; \alpha)
$$

$$
\text{Breach}_{t} = 1 \;\text{if Return}_{t} < \text{VaR}_{t},\;\; \text{else 0}
$$

$$
\text{Kupiec Statistic} = - 2 \cdot \ln\left[\frac{(1 - \alpha)^{n - x} \cdot \alpha^{x}}{\left(1 - \frac{x}{n}\right)^{n - x} \cdot \left(\frac{x}{n}\right)^{x}}\right]
$$

$$
\text{Christoffersen Statistic} = - 2 \cdot \ln\left[\frac{L(\pi)}{L(\pi_{01},\; \pi_{11})}\right]
$$

Where n is the number of out-of-sample VaR estimates and x the number of breaches. L(pi) is the likelihood of the breach sequence with a single breach probability pi, and $$L (\pi_{01} , \pi_{11})$$ that of a first-order Markov chain in which the breach probability depends on whether the previous period was a breach. Both statistics are compared with a $$\chi^{2}$$ distribution with one degree of freedom for the p-value.

For more information about the methods, see the following papers:

- Kupiec, P.H. (1995). "Techniques for Verifying the Accuracy of Risk Measurement Models." The Journal of Derivatives, 3(2), 73-84.
- Christoffersen, P.F. (1998). "Evaluating Interval Forecasts." International Economic Review, 39(4), 841-862.

**Also known as:** VaR validation, VaR backtest, POF test.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly or yearly).
Defaults to "daily".
- <u>distribution (str, optional):</u> The distribution to use for the rolling VaR estimates, one of
"historic", "gaussian", "studentt" or "evt". Defaults to "historic".
"studentt" and "evt" fit their distribution to every window, which takes minutes for
years of daily data, where "historic" and "gaussian" take well under a second.
- <u>alpha (float, optional):</u> The tail probability for the VaR estimates (e.g., 0.05 for the 95%
confidence level). Defaults to 0.05. With "evt" it can be at most 0.05, since the Generalized
Pareto Distribution is fitted above the 95th percentile of losses; a larger `alpha` gives an
empty result (with a logged error).
- <u>window_size (int &#124; None, optional):</u> The rolling window size (in number of return observations of
`period`) used to estimate each VaR value. Defaults to None, which uses a year of observations
with a minimum of 20 (252 daily, 52 weekly and 20 monthly, quarterly or yearly returns).
- <u>test (str, optional):</u> Which test(s) to run, one of "kupiec", "christoffersen" or "both". Defaults
to "both".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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

The formula is as follows (with the default distribution="historic", alpha=0.05 and daily returns, for which the window is 252):

$$
Z_{2} = \frac{\sum\left(\frac{\text{Return}_{t} \cdot \text{Breach}_{t}}{\text{CVaR}_{t}}\right)}{n \cdot \alpha} - 1
$$

$$
\text{P-Value} = 1 - \Phi\left(\frac{Z_{2}}{\text{Standard Error}}\right)
$$

Where $$\text{VaR}_{t}$$ and CVaR_t are estimated from the window_size returns before t (see `get_var_backtest`), Breach_t is 1 if Return_t < $$\text{VaR}_{t}$$ and 0 otherwise, n is the number of estimates and the Standard Error is the sample standard deviation (ddof=1) of Z2 over `n_bootstrap` paired bootstrap resamples. Returns and CVaR are both negative, so Z2 is about 0 for a well-calibrated model and positive when the realized tail losses exceed the CVaR (the opposite sign of the paper, which counts losses as positive).

For more information about the method, see the following paper:

- Acerbi, C., & Szekely, B. (2014). "Back-Testing Expected Shortfall." RISK Magazine, 27(11), 76-81.

**Also known as:** Acerbi-Szekely test, ES backtest, Z2 test.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly or yearly).
Defaults to "daily".
- <u>distribution (str, optional):</u> The distribution to use for the rolling VaR/CVaR estimates,
one of "historic", "gaussian", "studentt" or "evt". Defaults to "historic".
"studentt" and "evt" fit their distribution to every window, which takes minutes for
years of daily data, where "historic" and "gaussian" take well under a second.
- <u>alpha (float, optional):</u> The tail probability for the VaR/CVaR estimates (e.g., 0.05 for the 95%
confidence level). Defaults to 0.05. With "evt" it can be at most 0.05, since the Generalized
Pareto Distribution is fitted above the 95th percentile of losses; a larger `alpha` gives an
empty result (with a logged error).
- <u>window_size (int &#124; None, optional):</u> The rolling window size (in number of return observations
of `period`) used to estimate each VaR/CVaR value. Defaults to None, which uses a year of
observations with a minimum of 20 (252 daily, 52 weekly and 20 monthly, quarterly or yearly
returns).
- <u>n_bootstrap (int, optional):</u> The number of bootstrap resamples used to estimate the Standard
Error of Z2. Defaults to 1000.
- <u>random_state (int, optional):</u> The seed for the bootstrap random number generator. Defaults to
42.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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

## get_garch
Calculates the conditional variance ($$\sigma_{t}^{2}$$) of the returns with a GARCH(1, 1) model fitted to them. Take the square root for the conditional volatility, and see `get_garch_forecast` for the variance forecast beyond the last observation.

GARCH (Generalized autoregressive conditional heteroskedasticity) is stochastic model for time series, which is for instance used to model volatility clusters, stock return and inflation. It is a generalisation of the ARCH models.

The formula is as follows:

$$
\sigma_{t}^{2} = \Omega + \text{Alpha} \cdot r_{t-1}^{2} + \text{Beta} \cdot \sigma_{t-1}^{2}
$$

$$
\sigma_{1}^{2} = \Omega + (\text{Alpha} + \text{Beta}) \cdot \text{Backcast}
$$

Where $$r_{t}$$ are the returns (not demeaned) and the Backcast is an exponentially weighted average (decay 0.94) of the first 75 squared returns. Omega, Alpha and Beta maximize the Gaussian log-likelihood, i.e. minimize $$\sum (\ln \sigma_{t}^{2} + r_{t}^{2} / \sigma_{t}^{2})$$, under Omega, Alpha, Beta > 0 and Alpha + Beta < 1 (see `get_garch_parameters`).

**Also known as:** GARCH, volatility clustering, conditional heteroscedasticity.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>time_steps (int, optional):</u> Time steps to calculate GARCH for. Defaults to None, which uses the length of the
returns.
- <u>optimization_t (int, optional):</u> Time steps to optimize GARCH for. It is only used if no weights are given.
Defaults to None, which uses the length of the returns.
- <u>within_period (bool, optional):</u> Whether to calculate GARCH within the specified period or for the entire
period. Thus whether to look at the GARCH within a specific year (if period = 'yearly') or look at the
entirety of all years. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the GARCH values over time. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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
\sigma_{n+h}^{2} = \sigma_{L}^{2} + (\sigma_{n+1}^{2} - \sigma_{L}^{2}) \cdot (\text{Alpha} + \text{Beta})^{h - 1}
$$

$$
\sigma_{L}^{2} = \frac{\Omega}{1 - \text{Alpha} - \text{Beta}}
$$

Where n is the last observation, $$h = 1$$, ..., `time_steps` (10 by default) the forecast step, $$\sigma_{n + 1}^{2}$$ the one-step-ahead variance of the fitted GARCH(1, 1) recursion (see `get_garch`) and $$\sigma_{L}^{2}$$ the long-run variance.

For more information about the method, see the following book:

- Finance Compact Plus Band 1, by Yvonne Seler Zimmerman and Heinz Zimmerman; ISBN: 978-3-907291-31-1

**Also known as:** volatility forecast, predicted volatility.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>time_steps (int, optional):</u> Time steps to calculate GARCH and to forecast sigma_2 values for. Defaults to 10.
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
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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
\sigma_{t}^{2} = \Omega + \text{Alpha} \cdot r_{t-1}^{2} + \text{Beta} \cdot \sigma_{t-1}^{2}
$$

$$
\text{Log-Likelihood} = - \sum\left(\ln \sigma_{t}^{2} + \frac{r_{t}^{2}}{\sigma_{t}^{2}}\right)(\text{up to constants})
$$

Where $$r_{t}$$ are the returns (not demeaned), with the constraints Omega, Alpha, Beta > 0 and Alpha + Beta < 1. The parameters are estimated by maximizing the Gaussian log-likelihood with L-BFGS-B, started from a domain-informed initial guess and from 32 points of a Sobol sequence, and the best fit is finished with Nelder-Mead. The search runs on the parameters scaled to their bounds, as Omega (of the order of a daily variance) and Alpha and Beta differ by orders of magnitude.

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
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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
Calculates the conditional variance ($$\sigma_{t}^{2}$$) of the returns with a GJR-GARCH(1, 1, 1) model fitted to them. Take the square root for the conditional volatility, and see `get_gjr_garch_forecast` for the variance forecast.

GJR-GARCH extends GARCH with a leverage term that lets negative shocks (bad news) raise volatility by more than positive shocks of the same size, a well documented asymmetry in equity returns that symmetric GARCH cannot capture.

For more information about the method, see the following paper:

- Glosten, L.R., Jagannathan, R., and Runkle, D.E. (1993). "On the Relation between the Expected Value and the Volatility of the Nominal Excess Return on Stocks." The Journal of Finance, 48(5), 1779-1801.

The formula is as follows:

$$
\sigma_{t}^{2} = \Omega + (\text{Alpha} + \Gamma \cdot I_{t-1}) \cdot r_{t-1}^{2} + \text{Beta} \cdot \sigma_{t-1}^{2}
$$

$$
\sigma_{1}^{2} = \Omega + \left(\text{Alpha} + \frac{\Gamma}{2} + \text{Beta}\right) \cdot \text{Backcast}
$$

Where $$r_{t}$$ are the returns (not demeaned), $$I_{t - 1}$$ is 1 when $$r_{t - 1} < 0$$ and 0 otherwise, and the Backcast is the same as in `get_garch`. The parameters maximize the Gaussian log-likelihood under Alpha + Gamma / 2 + Beta < 1 and Alpha + Gamma >= 0 (see `get_gjr_garch_parameters`).

**Also known as:** GJR-GARCH, threshold GARCH, TGARCH.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>time_steps (int, optional):</u> Time steps to calculate GJR-GARCH for. Defaults to None, which uses the length of
the returns.
- <u>optimization_t (int, optional):</u> Time steps to optimize GJR-GARCH for. It is only used if no
weights are given. Defaults to None, which uses the length of the returns.
- <u>within_period (bool, optional):</u> Whether to calculate GJR-GARCH within the specified period or
for the entire period. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the GJR-GARCH values over time.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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
\sigma_{n+h}^{2} = \sigma_{L}^{2} + (\sigma_{n+1}^{2} - \sigma_{L}^{2}) \cdot \left(\text{Alpha} + \frac{\Gamma}{2} + \text{Beta}\right)^{h - 1}
$$

$$
\sigma_{L}^{2} = \frac{\Omega}{1 - \text{Alpha} - \frac{\Gamma}{2} - \text{Beta}}
$$

Where n is the last observation, $$h = 1$$, ..., `time_steps` (10 by default) the forecast step and $$\sigma_{n + 1}^{2}$$ the one-step-ahead variance of the fitted GJR-GARCH(1, 1, 1) recursion (see `get_gjr_garch`). The leverage term enters at its expectation, Gamma / 2, as a negative shock is as likely as a positive one.

For more information about the method, see the following paper:

- Glosten, L.R., Jagannathan, R., and Runkle, D.E. (1993). "On the Relation between the Expected Value and the Volatility of the Nominal Excess Return on Stocks." The Journal of Finance, 48(5), 1779-1801.

**Also known as:** volatility forecast, predicted volatility.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>time_steps (int, optional):</u> Time steps to calculate GJR-GARCH and to forecast sigma_2 values for. Defaults to
10.
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
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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
\sigma_{t}^{2} = \Omega + (\text{Alpha} + \Gamma \cdot I_{t-1}) \cdot r_{t-1}^{2} + \text{Beta} \cdot \sigma_{t-1}^{2}
$$

$$
\text{Log-Likelihood} = - \sum\left(\ln \sigma_{t}^{2} + \frac{r_{t}^{2}}{\sigma_{t}^{2}}\right)(\text{up to constants})
$$

Where $$r_{t}$$ are the returns (not demeaned) and $$I_{t - 1}$$ is 1 when $$r_{t - 1} < 0$$ and 0 otherwise. The log-likelihood is maximized under Alpha + Gamma / 2 + Beta < 1 and Alpha + Gamma >= 0.

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
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Omega, Alpha, Gamma and Beta values per asset.

**Notes:**

- The method retrieves historical return data based on the specified `period` and fits a
GJR-GARCH(1, 1, 1) model for each asset in the Toolkit instance.
- Every asset is fitted on its own available returns, so an asset with a shorter history (or a gap)
does not shorten the sample of the others.
- GJR-GARCH nests GARCH ($$\gamma = 0$$), so the fit never ends at a lower log-likelihood than the
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
Calculates the conditional variance ($$\sigma_{t}^{2}$$) of the returns with an EGARCH(1, 1) model fitted to them. Take the square root for the conditional volatility, and see `get_egarch_forecast` for the variance forecast.

EGARCH models the log of the conditional variance, which avoids having to constrain the parameters to keep the variance positive and, like GJR-GARCH, lets negative and positive shocks of the same size have a different impact on volatility (the leverage effect).

For more information about the method, see the following paper:

- Nelson, D.B. (1991). "Conditional Heteroskedasticity in Asset Returns: A New Approach." Econometrica, 59(2), 347-370.

The formula is as follows:

$$
\ln \sigma_{t}^{2} = \Omega + \text{Alpha} \cdot \left(\left|z_{t-1}\right| - \sqrt{\frac{2}{\pi}}\right) + \Gamma \cdot z_{t-1} + \text{Beta} \cdot \ln \sigma_{t-1}^{2}
$$

$$
z_{t} = \frac{r_{t}}{\sigma_{t}}
$$

$$
\ln \sigma_{1}^{2} = \Omega + \text{Beta} \cdot \ln(\text{Backcast})
$$

Where $$r_{t}$$ are the returns (not demeaned), $$\sqrt{2 / \pi}$$ is the expected &#124;z&#124; of a standard normal shock, the log variance is kept within [-20, 20] and the Backcast is the same as in `get_garch`. The parameters maximize the Gaussian log-likelihood with &#124;Beta&#124; < 1 (see `get_egarch_parameters`).

**Also known as:** exponential GARCH, log-GARCH.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>time_steps (int, optional):</u> Time steps to calculate EGARCH for. Defaults to None, which uses the length of the
returns.
- <u>optimization_t (int, optional):</u> Time steps to optimize EGARCH for. It is only used if no
weights are given. Defaults to None, which uses the length of the returns.
- <u>within_period (bool, optional):</u> Whether to calculate EGARCH within the specified period or
for the entire period. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the EGARCH values over time.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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
\ln \sigma_{n+h}^{2} = L + \text{Beta}^{h - 1} \cdot (\ln \sigma_{n+1}^{2} - L)
$$

$$
L = \frac{\Omega}{1 - \text{Beta}}
$$

$$
\sigma_{n+h}^{2} = \exp(\ln \sigma_{n+h}^{2})
$$

Where n is the last observation, $$h = 1$$, ..., `time_steps` (10 by default) the forecast step and $$\sigma_{n + 1}^{2}$$ the one-step-ahead variance of the fitted EGARCH(1, 1) recursion (see `get_egarch`). The shock terms drop out at their expectation of zero, so the forecast is the exponential of the expected log variance.

For more information about the method, see the following paper:

- Nelson, D.B. (1991). "Conditional Heteroskedasticity in Asset Returns: A New Approach." Econometrica, 59(2), 347-370.

**Also known as:** volatility forecast, predicted volatility.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>time_steps (int, optional):</u> Time steps to calculate EGARCH and to forecast sigma_2 values for. Defaults to 10.
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
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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
\ln \sigma_{t}^{2} = \Omega + \text{Alpha} \cdot \left(\left|z_{t-1}\right| - \sqrt{\frac{2}{\pi}}\right) + \Gamma \cdot z_{t-1} + \text{Beta} \cdot \ln \sigma_{t-1}^{2}
$$

$$
\text{Log-Likelihood} = - \sum\left(\ln \sigma_{t}^{2} + \frac{r_{t}^{2}}{\sigma_{t}^{2}}\right)(\text{up to constants})
$$

Where $$r_{t}$$ are the returns (not demeaned) and $$z_{t} = r_{t} / \sigma_{t}$$. The log-likelihood is maximized with Omega in [-15, 5], Alpha and Gamma in [-1, 1] and &#124;Beta&#124; < 1, starting the recursion from $$\ln \sigma_{1}^{2} = \text{Omega} + \text{Beta} \cdot \ln (\text{Backcast})$$, with the Backcast of `get_garch_parameters`.

For more information about the method, see the following paper:

- Nelson, D.B. (1991). "Conditional Heteroskedasticity in Asset Returns: A New Approach." Econometrica, 59(2), 347-370.

**Also known as:** EGARCH weights, EGARCH coefficients, leverage parameters.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>optimization_t (int, optional):</u> Time steps of the returns series to use for the optimization.
Defaults to the full length of the returns series.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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

Where Std is the sample standard deviation (ddof=1) and the trading days per period are 252 / 52 (weekly), 252 / 12 (monthly), 252 / 4 (quarterly) or 252 (yearly). A ticker with returns on weekends, such as a cryptocurrency, has a return on every calendar day and uses 365 days a year instead (365 / 52 weekly), so its Volatility is not understated against the stocks. The range-based estimators take the square root of a daily variance and scale it the same way, with H, L, O and C the daily High, Low, Open and Close, $$C_{- 1}$$ the previous Close, Mean the average and Var the sample variance (ddof=1) over the days in the period:

$$
\text{Parkinson Variance} = \frac{\operatorname{Mean}\left(\ln\left(\frac{H}{L}\right)^{2}\right)}{4 \cdot \ln 2}
$$

$$
\text{Garman-Klass Variance} = \operatorname{Mean}\left(0.5 \cdot \ln\left(\frac{H}{L}\right)^{2} - (2 \cdot \ln 2 - 1) \cdot \ln\left(\frac{C}{O}\right)^{2}\right)
$$

$$
\text{Rogers-Satchell Variance} = \operatorname{Mean}\left(\ln\left(\frac{H}{C}\right) \cdot \ln\left(\frac{H}{O}\right) + \ln\left(\frac{L}{C}\right) \cdot \ln\left(\frac{L}{O}\right)\right)
$$

$$
\text{Yang-Zhang Variance} = \operatorname{Var}\left(\ln\left(\frac{O}{C_{-1}}\right)\right) + k \cdot \operatorname{Var}\left(\ln\left(\frac{C}{O}\right)\right) + (1 - k) \cdot \text{Rogers-Satchell Variance}
$$

$$
k = \frac{0.34}{1.34 + \frac{n + 1}{n - 1}},\;\; \text{with } n \text{ the number of days in the period}
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
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Volatility values over time.
Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series: Volatility values with time as the index.

**Notes:**

- The method retrieves the daily historical price data and calculates the Volatility for
the specified `period` for each asset in the Toolkit instance. The close-to-close estimator
only needs the daily returns, Parkinson needs the High and Low, and the remaining
estimators need the Open, High, Low and Close.
- A range-based estimator leaves out each day on which a price it uses is 0 or below (a bad bar, as some
feeds report for illiquid days), since its logarithm is undefined; the period is measured over the
remaining days. The Yang-Zhang overnight return also needs the previous Close.
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
| 2021   |   0.0679 |   0.8133 |  0.1303 |  0.1752 |      0.1293 |
| 2022   |   0.1199 |   0.639  |  0.2417 |  0.1881 |      0.2424 |
| 2023   |   0.0895 |   0.4408 |  0.1309 |  0.1652 |      0.1308 |
| 2024   |   0.0708 |   0.5345 |  0.1265 |  0.185  |      0.1257 |
| 2025   |   0.089  |   0.4194 |  0.1875 |  0.2421 |      0.1949 |

---

## get_har_rv_forecast
Calculate the Corsi (2009) Heterogeneous Autoregressive Realized Volatility (HAR-RV) forecast of future daily Realized Variance, per asset.

Volatility clustering happens across multiple, overlapping time horizons at once. HAR-RV captures this cheaply -- without the numerical optimization a GARCH-family fit requires (see `get_garch`) -- by regressing future daily Realized Variance on trailing daily, weekly and monthly average Realized Variance components. The daily Realized Variance itself can be constructed in several ways via `estimator`: the simplest is the squared daily return, while the OHLC range-based estimators (see `get_volatility`, which exposes the same estimators via its own `method` parameter) use the daily (pre-period-aggregation) term behind each of those estimators instead, which is more statistically efficient since it uses the daily trading range rather than only the close-to-close move.

The formula is as follows (with the default estimator="squared_return", weekly_window=5, monthly_window=22 and horizon=1):

$$
\text{RV}_{t} = \text{Return}_{t}^{2}
$$

$$
\text{RV}^{w}_{t} = \operatorname{Mean}(\text{RV}_{t-4},\; \ldots,\; \text{RV}_{t})\;\;\text{and}\;\; \text{RV}^{m}_{t} = \operatorname{Mean}(\text{RV}_{t-21},\; \ldots,\; \text{RV}_{t})
$$

$$
\text{Forecast of}\; \text{RV}_{t+1} = b_{0} + b_{d} \cdot \text{RV}_{t} + b_{w} \cdot \text{RV}^{w}_{t} + b_{m} \cdot \text{RV}^{m}_{t}
$$

Where $$b_{0}$$, $$b_{d}$$, $$b_{w}$$ and $$b_{m}$$ are estimated once by ordinary least squares over each asset's full history, and the forecast of $$\text{RV}_{t + 1}$$ is shown at date t. The range-based estimators replace $$\text{RV}_{t}$$ with the daily Parkinson, Garman-Klass or Rogers-Satchell variance term (see `get_volatility`).

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
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the HAR-RV forecast values over
time. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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

## get_excess_volatility
Calculate the Excess Volatility of an investment portfolio or asset's returns for a given period based on the daily historical returns.

Excess Volatility is the Volatility of the Excess Return, i.e. the daily return minus the risk free rate, scaled to the given period in the same way as the Volatility.

The formula is as follows:

$$
\text{Excess Volatility} = \operatorname{Std}(\text{Daily Return} - \text{Daily Risk Free Rate}) \cdot \sqrt{\text{Trading Days per Period}}
$$

Where Std is the sample standard deviation (ddof=1) over the days within the period, the annualized risk free rate is converted to the rate earned with each return (a trading day of it, 1 / 252 of a year, or for a ticker that trades on weekends the calendar days since its previous return, on 365 days a year), and the trading days per period are 252 / 52 (weekly), 252 / 12 (monthly), 252 / 4 (quarterly) or 252 (yearly), or 365 days a year for a ticker with returns on weekends. With `rolling`, the result is the sample standard deviation of the last `rolling` excess returns of the chosen period itself, without scaling, with the risk free rate compounded over the dates in each period on which the ticker has a return.

**Also known as:** standard deviation of excess returns.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (weekly, monthly, quarterly, or yearly). Defaults
to "quarterly" if the Toolkit is initialised with quarterly=True, otherwise "yearly".
- <u>rolling (int, optional):</u> The rolling window size to use for the calculation. If set,
Excess Volatility is calculated over a rolling window of this many periods (e.g.
period='monthly' and rolling=6 gives the rolling 6-month Excess Volatility) instead of
one value per `period`. Defaults to None.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Excess Volatility values
over time. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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
\text{Downside Deviation} = \sqrt{\frac{\sum \min(\text{Return}_{t} - \text{MAR},\; 0)^{2}}{n}}
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
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Downside Deviation values over
time. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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

## get_ewma_volatility
Calculate the exponentially weighted moving average (EWMA) Volatility of an investment portfolio or asset's daily returns, following the RiskMetrics methodology.

Unlike a fixed-window rolling Volatility, EWMA Volatility weights recent observations more heavily than older ones, so it reacts faster to changes in the underlying volatility regime. It is a simpler, more interpretable alternative to a full GARCH fit.

The formula is as follows:

$$
\text{EWMA Variance}(t) = \lambda \cdot \text{EWMA Variance}(t-1) + (1 - \lambda) \cdot \operatorname{Return}(t-1)^{2}
$$

$$
\text{EWMA Volatility}(t) = \sqrt{\text{EWMA Variance}(t)}
$$

Where lambda is 0.94 by default and Return(t-1) the previous daily return, so the value on a day only uses the returns before it. The recursion starts from the first squared return.

With the RiskMetrics decay factor of 0.94, about 70% of the weight sits on the last 20 trading days, so EWMA Volatility reacts within days to a market shock and falls back almost as quickly. The values are daily; multiply them by the square root of 252 (365 for a ticker that trades on weekends) for an annualized figure comparable with `get_volatility(period="yearly")`.

**Also known as:** RiskMetrics volatility, exponentially weighted volatility.

**Args:**

- <u>lambda_ (float, optional):</u> The decay factor. Higher values weight the past
more heavily (slower to react), lower values weight recent returns more
heavily (faster to react). RiskMetrics uses 0.94 for daily data. Defaults to 0.94.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the EWMA Volatility values over
time. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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

