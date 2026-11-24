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
Collect all risk metrics of every asset in one table: its volatility, tail risk, drawdowns and distribution side by side.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns. Options are: "daily", "weekly", "monthly",
"quarterly", "yearly". Defaults to "quarterly" if the Toolkit is initialised with quarterly=True, otherwise "yearly".
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
- With growth, the method calculates the growth of the ratio values
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
Calculate the factor analysis (predictive power) of the risk metrics: whether the tickers that score high on a metric go on to return more than those that score low.

Per period, the information coefficient (IC) is the Spearman rank correlation between the metric of the tickers in the period and their return over the following horizon: 1 means the metric ranks the later returns perfectly, -1 in reverse and 0 that it says nothing about them. The IC measures skill in Grinold and Kahn's fundamental law of active management, $$\text{IR} \approx \text{IC} \times \sqrt{\text{breadth}}$$: a small but consistent IC across many tickers and periods gives a high information ratio.

The summary has a row per metric and horizon with the mean IC, its standard deviation, the IC information ratio (mean divided by standard deviation), the t-statistic of the mean with its p-value, the skewness and excess kurtosis of the IC, the share of periods with a positive IC, the number of periods, the top minus bottom spread (the mean forward return of the highest quantile minus that of the lowest), the annualized alpha and the beta of the factor-weighted long-short portfolio against the equally weighted tickers, the mean turnover of the top and bottom quantiles and the mean rank autocorrelation of the metric from one period to the next. With detail, it returns one part of the analysis per period, quantile or group for a single metric.

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

Each metric is measured within each period (e.g. the volatility of a month's daily returns) and compared with the returns from the close of the period's last trading day onwards, using the dividend and split adjusted close, so a metric never overlaps the returns it is compared with. Each ticker keeps its own history: a ticker without a value or a return in a period is left out of that period only.

**References:**

- library | Shares similar logic as alphalens' [factor_information_coefficient](https://github.com/stefan-jansen/alphalens-reloaded/blob/v0.4.4/src/alphalens/performance.py#L28){:target="_blank"}
- library | Shares similar logic as alphalens' [factor_returns](https://github.com/stefan-jansen/alphalens-reloaded/blob/v0.4.4/src/alphalens/performance.py#L210){:target="_blank"}
- library | Shares similar logic as alphalens' [mean_return_by_quantile](https://github.com/stefan-jansen/alphalens-reloaded/blob/v0.4.4/src/alphalens/performance.py#L461){:target="_blank"}

**Args:**

- <u>metrics (str &#124; list[str], optional):</u> A risk method name with a value per ticker and period,
e.g. "get_volatility", a list of them, or a collection. Options for a collection are:
"anomalies" (the volatility, maximum drawdown, skewness and Amihud illiquidity), "all"
(every risk metric with a value per ticker and period). Defaults to "anomalies". "all" adds the downside deviation, kurtosis, value at risk,
conditional value at risk, tail ratio and Roll spread.
- <u>period (str, optional):</u> The frequency at which the metrics are measured and evaluated.
Options are: "daily", "weekly", "monthly", "quarterly", "yearly". Each metric is calculated
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
instead of the summary. Options are: "information_coefficient" (per period and horizon),
"information_coefficient_by_month" (the mean IC per calendar month),
"information_coefficient_by_year" (the mean IC per calendar year),
"group_information_coefficient" (the IC statistics within each group, needs group),
"quantile_returns" (the mean forward return per quantile and horizon),
"quantile_returns_by_date" (per period), "quantile_return_statistics" (the mean, its
standard error and both per single period), "quantile_statistics" (the range, mean and
count of the factor values in each quantile), "quantile_turnover" (per period and
quantile), "rank_autocorrelation" (per period), "factor_weights" (the weights of the
factor-weighted long-short portfolio per period and ticker), "factor_returns" (its
return per period and horizon), "cumulative_returns" (the growth of 1 in it and in
each quantile), "event_returns" (the mean price path of each quantile from the
longest horizon before to the longest horizon after the periods it is formed).
Defaults to None.
- <u>column (str &#124; None, optional):</u> The output to use of a metric with several.
Defaults to None, which uses the first.
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
"quantile" (equally sized), "equal_width" (bins of equal width between the lowest
and highest value), "zero_aware" (half of the quantiles for the negative and half
for the zero and positive values, for a signal centred on zero; needs an even number
of quantiles), "group" (equally sized within each group, needs group). Defaults to
"quantile".
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
- The top minus bottom spread of alphalens (Stefan Jansen's alphalens-reloaded)
is half of the one here (a gross exposure of one rather than two), it
drops a period and ticker without every horizon's return where each horizon
here uses its own, and its event returns average the single-period returns at
each offset where these are the price paths rebased to the period itself.

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

|                                         |   Mean IC |   IC Standard Deviation |   IC Information Ratio |   t-Statistic |   P-Value |   IC Skewness |   IC Kurtosis |   Positive Share |   Observations |   Top Minus Bottom |   Annualized Alpha |    Beta |   Quantile Turnover |   Rank Autocorrelation |
|:----------------------------------------|----------:|------------------------:|-----------------------:|--------------:|----------:|--------------:|--------------:|-----------------:|---------------:|-------------------:|-------------------:|--------:|--------------------:|-----------------------:|
| ('get_volatility', '1 Month')           |    0.0963 |                  0.3676 |                 0.262  |        2.8586 |    0.005  |       -0.2056 |       -0.405  |           0.6218 |            119 |             0.0185 |             0.0337 |  0.407  |              0.4688 |                 0.5848 |
| ('get_volatility', '12 Months')         |    0.2759 |                  0.3703 |                 0.7451 |        7.7428 |    0      |       -0.7586 |       -0.2658 |           0.7685 |            108 |             0.3154 |            -0.0757 |  1.0993 |              0.4688 |                 0.5848 |
| ('get_maximum_drawdown', '1 Month')     |   -0.0257 |                  0.3315 |                -0.0774 |       -0.8443 |    0.4002 |       -0.0332 |       -0.4476 |           0.4622 |            119 |            -0.0041 |             0.0118 | -0.3113 |              0.6275 |                 0.2719 |
| ('get_maximum_drawdown', '12 Months')   |   -0.1759 |                  0.3542 |                -0.4965 |       -5.1603 |    0      |        0.496  |       -0.4167 |           0.3241 |            108 |            -0.2094 |             0.0475 | -0.6263 |              0.6275 |                 0.2719 |
| ('get_skewness', '1 Month')             |    0.0136 |                  0.2943 |                 0.0464 |        0.5056 |    0.6141 |       -0.0773 |        0.1094 |           0.5462 |            119 |            -0.0007 |            -0.0055 |  0.0598 |              0.7521 |                 0.0593 |
| ('get_skewness', '12 Months')           |    0.0081 |                  0.2996 |                 0.0271 |        0.2815 |    0.7789 |        0.1058 |       -0.547  |           0.5093 |            108 |             0.0142 |            -0.0111 |  0.0936 |              0.7521 |                 0.0593 |
| ('get_amihud_illiquidity', '1 Month')   |   -0.0285 |                  0.3896 |                -0.0731 |       -0.7971 |    0.427  |       -0.0875 |       -0.9255 |           0.479  |            119 |            -0.0059 |             0.0216 | -0.1902 |              0.1905 |                 0.8996 |
| ('get_amihud_illiquidity', '12 Months') |   -0.1164 |                  0.3789 |                -0.3072 |       -3.1927 |    0.0019 |        0.68   |       -0.2884 |           0.3611 |            108 |            -0.0796 |             0.1036 | -0.457  |              0.1905 |                 0.8996 |

---

## get_tail_dependence_coefficient
Calculate the Upper and Lower Tail Dependence Coefficients between `ticker_a` and `ticker_b`: how likely one asset is in extreme distress given that the other one already is.

Without a pair, every ticker is paired with the benchmark, which tells how likely each company is to be in distress when the market is.

Correlation only captures the *average* co-movement between two assets -- it says nothing about whether they are more likely to crash together than an equivalent gaussian relationship would imply. The Tail Dependence Coefficient answers that specific question directly: the probability that one asset is in extreme distress, given that the other one already is.

The empirical estimate at $$q = 0.95$$ rests on the few days on which both assets are in their worst (or best) 5% at the same time, so it needs several years of daily data to be stable. A gaussian dependence of any correlation below 1 implies zero tail dependence, so a Lower Tail Dependence Coefficient well above zero means that diversification between the two assets is weakest exactly when it is needed.

The formula is as follows (with the default empirical estimate and a q of 0.95):

$$
\text{Upper Tail Dependence} = \frac{\#(A > Q_{A}(q) \;\text{and}\; B > Q_{B}(q))}{\#(A > Q_{A}(q))}
$$

$$
\text{Lower Tail Dependence} = \frac{\#(A \leq Q_{A}(1 - q) \;\text{and}\; B \leq Q_{B}(1 - q))}{\#(A \leq Q_{A}(1 - q))}
$$

Where A and B are the values of `ticker_a` and `ticker_b` on their common dates and $$Q_{A}$$ and $$Q_{B}$$ their empirical quantiles. With the gaussian copula both coefficients are 0 (1 only for a correlation of exactly 1), and with the Student-T copula both are $$2 \cdot t_{v + 1} (- \sqrt{(v + 1) \cdot (1 - \rho) / (1 + \rho)})$$, with v = `dof`, rho the Pearson correlation and $$t_{v + 1}$$ the Student-T distribution function.

**Also known as:** tail dependence, extremal dependence coefficient.

**References:**

- paper | Embrechts, P., McNeil, A., & Straumann, D. (1999). "Correlation: Pitfalls and Alternatives." RISK Magazine, 12, 69-71.
- paper | Poon, S.H., Rockinger, M., & Tawn, J. (2004). "Extreme Value Dependence in Financial Markets: Diagnostics, Models, and Financial Implications." Review of Financial Studies, 17(2), 581-610.
- library | Shares similar logic as skfolio's [StudentTCopula](https://skfolio.org/generated/skfolio.distribution.StudentTCopula.html){:target="_blank"} (Student-T)

**Args:**

- <u>ticker_a (str &#124; None, optional):</u> The first asset. Defaults to None, which pairs every other ticker
in the Toolkit instance (the benchmark included when `ticker_b` is given) with `ticker_b`.
- <u>ticker_b (str &#124; None, optional):</u> The second asset, the benchmark by its own ticker (SPY) or as
"Benchmark", or a ticker outside the Toolkit, whose returns are retrieved for the same dates
(with column="Return"). Defaults to None, which uses the benchmark.
- <u>period (str, optional):</u> The data frequency. Options are: "daily", "weekly", "monthly", "quarterly",
"yearly". Defaults to "daily", since a dependence estimate needs far more observations than a
lower frequency provides -- at "yearly" a decade of history is only ten
observations.
- <u>column (str, optional):</u> The historical data column to use. Defaults to "Return", since
tail dependence between return series is the standard risk management application.
- <u>q (float, optional):</u> The threshold quantile used for the "empirical" method, in (0.5, 1).
Defaults to 0.95.
- <u>method (str, optional):</u> The estimation method. Options are: "empirical" (nonparametric plug-in
estimate), "gaussian" (gaussian copula), "student-t" (Student-T copula). Defaults to "empirical".
- <u>dof (float, optional):</u> The degrees of freedom of the Student-T copula, only used when
method is "student-t". Defaults to 4.0.
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
Calibrate a bivariate copula between `ticker_a` and `ticker_b`: how their returns move together apart from their own distributions, including how often their crashes or rallies coincide.

It is fitted on the pseudo-observations (ranks) of their returns: the Clayton, Gumbel and Frank parameters by maximum likelihood, the gaussian correlation from the normal scores, and the Student-T correlation from Kendall's tau with the degrees of freedom by maximum likelihood (Demarta & McNeil, 2005).

When `ticker_a`/`ticker_b` are not given, every unique pair among the Toolkit's tickers is calibrated instead.

A copula separates the dependence structure between two assets from their individual (marginal) return distributions (Sklar's theorem), letting the two be modeled independently. Five families are supported, each capturing a different shape of dependence:

- Gaussian: zero tail dependence -- crashes and rallies are no more likely to happen together than the correlation alone implies. Included mainly as a baseline, since real asset returns typically show more joint tail risk than this.
- Student-T: symmetric, nonzero tail dependence in both tails.
- Clayton: nonzero *lower* tail dependence only -- assets crash together more than they rally together. The most common choice for equity return pairs.
- Gumbel: nonzero *upper* tail dependence only -- assets rally together more than they crash together.
- Frank: zero tail dependence in both tails, but (unlike gaussian) can represent negative dependence and is symmetric around independence.

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

**Also known as:** copula calibration, copula fit, dependence modeling.

**References:**

- paper | Sklar, A. (1959). Publications de l'Institut de Statistique de l'Universite de Paris, 8, 229-231.
- paper | McNeil, A.J., Frey, R., & Embrechts, P. (2015). "Quantitative Risk Management: Concepts, Techniques and Tools." Princeton University Press.
- paper | Demarta, S., & McNeil, A.J. (2005). "The T Copula and Related Copulas." International Statistical Review, 73(1), 111-129.
- library | Shares similar logic as skfolio's [GaussianCopula](https://skfolio.org/generated/skfolio.distribution.GaussianCopula.html){:target="_blank"}
- library | Shares similar logic as skfolio's [StudentTCopula](https://skfolio.org/generated/skfolio.distribution.StudentTCopula.html){:target="_blank"}
- library | Shares similar logic as skfolio's [ClaytonCopula](https://skfolio.org/generated/skfolio.distribution.ClaytonCopula.html){:target="_blank"}
- library | Shares similar logic as skfolio's [GumbelCopula](https://skfolio.org/generated/skfolio.distribution.GumbelCopula.html){:target="_blank"}
- library | Shares similar logic as statsmodels' [FrankCopula](https://www.statsmodels.org/stable/generated/statsmodels.distributions.copula.api.FrankCopula.html){:target="_blank"}

**Args:**

- <u>ticker_a (str, optional):</u> The first asset. Defaults to None, meaning every unique pair of
tickers in the Toolkit instance is calibrated (requires `ticker_b` to also be None).
- <u>ticker_b (str, optional):</u> The second asset. Defaults to None, see `ticker_a`.
- <u>copula (str, optional):</u> The copula family to fit. Options are: "gaussian" (Gaussian copula),
"student-t" (Student-T copula), "clayton" (Clayton copula), "gumbel" (Gumbel copula), "frank" (Frank
copula). Defaults to "gaussian".
- <u>period (str, optional):</u> The data frequency. Options are: "daily", "weekly", "monthly", "quarterly",
"yearly". Defaults to "daily", since a dependence estimate needs far more observations than a
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
Simulate joint return scenarios of `ticker_a` and `ticker_b` from a bivariate copula: draws that keep how the two move together, including in their tails.

The copula is calibrated as in `get_copula_parameters`.

When `ticker_a`/`ticker_b` are not given, every unique pair among the Toolkit's tickers is calibrated and simulated instead, as columns grouped under a top-level (Ticker A, Ticker B) column per pair.

This is what a copula-based portfolio Monte Carlo simulation needs: draws that preserve the calibrated dependence structure -- including tail dependence, for the Student-T, Clayton and Gumbel families -- rather than the (typically understated) joint crash risk a plain multivariate gaussian simulation would produce.

The formula is as follows (with the default gaussian copula and empirical margins):

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

**References:**

- library | Shares similar logic as skfolio's [GaussianCopula](https://skfolio.org/generated/skfolio.distribution.GaussianCopula.html){:target="_blank"}
- library | Shares similar logic as skfolio's [StudentTCopula](https://skfolio.org/generated/skfolio.distribution.StudentTCopula.html){:target="_blank"}
- library | Shares similar logic as skfolio's [ClaytonCopula](https://skfolio.org/generated/skfolio.distribution.ClaytonCopula.html){:target="_blank"}
- library | Shares similar logic as skfolio's [GumbelCopula](https://skfolio.org/generated/skfolio.distribution.GumbelCopula.html){:target="_blank"}
- library | Shares similar logic as statsmodels' [FrankCopula](https://www.statsmodels.org/stable/generated/statsmodels.distributions.copula.api.FrankCopula.html){:target="_blank"}

**Args:**

- <u>ticker_a (str, optional):</u> The first asset. Defaults to None, meaning every unique pair of
tickers in the Toolkit instance is used (requires `ticker_b` to also be None).
- <u>ticker_b (str, optional):</u> The second asset. Defaults to None, see `ticker_a`.
- <u>copula (str, optional):</u> The copula family to fit and simulate from. Options are: "gaussian" (Gaussian copula),
"student-t" (Student-T copula), "clayton" (Clayton copula), "gumbel" (Gumbel copula), "frank" (Frank
copula). Defaults to "gaussian".
- <u>period (str, optional):</u> The data frequency. Options are: "daily", "weekly", "monthly", "quarterly",
"yearly". Defaults to "daily", since a dependence estimate needs far more observations than a
lower frequency provides -- at "yearly" a decade of history is only ten
observations.
- <u>column (str, optional):</u> The historical data column to use. Defaults to "Return".
- <u>simulations (int, optional):</u> The number of joint draws to simulate. Defaults to 10,000.
- <u>seed (int, optional):</u> The seed for the random number generator. Defaults to 0.
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

pd.DataFrame: `simulations` simulated joint draws, one column per asset (or "U"/"V" without
empirical margins) for a single given pair, or with columns grouped by
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

toolkit.risk.get_copula_simulation("HD", "LOW", simulations=30).head(5)
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
Calculate which copula family best describes how `ticker_a` and `ticker_b` move together, by comparing all five supported families on their AIC (Akaike Information Criterion).

Each family is calibrated as in `get_copula_parameters`. The lower the AIC, the better the fit relative to its number of parameters, so the top row is the best-fitting family.

When `ticker_a`/`ticker_b` are not given, every unique pair among the Toolkit's tickers is compared instead.

The formula is as follows:

$$
\text{AIC} = 2 \cdot k - 2 \cdot \text{Log-Likelihood}
$$

Where the Log-Likelihood is that of each family fitted as in `get_copula_parameters` and k the number of fitted parameters (2 for the Student-T copula, 1 for the others).

**Also known as:** copula selection, copula comparison.

**References:**

- library | Shares similar logic as skfolio's [GaussianCopula](https://skfolio.org/generated/skfolio.distribution.GaussianCopula.html){:target="_blank"}
- library | Shares similar logic as skfolio's [StudentTCopula](https://skfolio.org/generated/skfolio.distribution.StudentTCopula.html){:target="_blank"}
- library | Shares similar logic as skfolio's [ClaytonCopula](https://skfolio.org/generated/skfolio.distribution.ClaytonCopula.html){:target="_blank"}
- library | Shares similar logic as skfolio's [GumbelCopula](https://skfolio.org/generated/skfolio.distribution.GumbelCopula.html){:target="_blank"}
- library | Shares similar logic as statsmodels' [FrankCopula](https://www.statsmodels.org/stable/generated/statsmodels.distributions.copula.api.FrankCopula.html){:target="_blank"}

**Args:**

- <u>ticker_a (str, optional):</u> The first asset. Defaults to None, meaning every unique pair of
tickers in the Toolkit instance is compared (requires `ticker_b` to also be None).
- <u>ticker_b (str, optional):</u> The second asset. Defaults to None, see `ticker_a`.
- <u>period (str, optional):</u> The data frequency. Options are: "daily", "weekly", "monthly", "quarterly",
"yearly". Defaults to "daily", since a dependence estimate needs far more observations than a
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
with full results, one row per pair instead, indexed by (Ticker A, Ticker B),
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
Calculate the (Delta-)CoVaR of `ticker`: how much worse its Value at Risk gets when `conditioning_ticker` is in its own distress state, the spillover of tail risk.

Without a pair, it measures how much each ticker's distress adds to the tail risk of the benchmark (the market as the "system"), as in Adrian & Brunnermeier (2016).

Ordinary Value at Risk treats each asset in isolation, which misses systemic risk -- the fact that one asset's distress can spill over and worsen another's risk. CoVaR directly measures that spillover: it is the VaR of `ticker`, conditional on `conditioning_ticker` itself being at its own `alpha`-VaR, estimated via a linear Quantile Regression of `ticker`'s returns on `conditioning_ticker`'s returns at quantile `alpha`. The Delta-CoVaR isolates the marginal, distress-specific contribution by subtracting the same construction evaluated in the "normal" (median) state instead.

CoVaR was introduced to measure systemic risk: in its original application `ticker` is a financial-system index (or a bank's peers) and `conditioning_ticker` a single institution, so the Delta-CoVaR reads as that institution's contribution to system-wide tail risk. Because the quantile regression is fitted at the `alpha` quantile, it needs several years of daily data, and the result is a statement about co-movement in the tails, not about causality.

The formula is as follows (with the default alpha of 0.05):

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

**Also known as:** Conditional Value at Risk (systemic risk sense), Delta-CoVaR.

**References:**

- paper | Adrian, T., & Brunnermeier, M.K. (2016). "CoVaR." American Economic Review, 106(7), 1705-1741.

**Args:**

- <u>ticker (str &#124; None, optional):</u> The asset whose conditional VaR is being measured (the system),
the benchmark by its own ticker (SPY) or as "Benchmark", or a ticker outside the Toolkit, whose
returns are retrieved for the same dates (with column="Return"). Defaults to None, which uses the
benchmark.
- <u>conditioning_ticker (str &#124; None, optional):</u> The asset whose distress `ticker` is conditioned on.
Defaults to None, which conditions `ticker` on every other ticker in the Toolkit instance in turn
(the benchmark included when `ticker` is given), a row each.
- <u>period (str, optional):</u> The data frequency. Options are: "daily", "weekly", "monthly", "quarterly",
"yearly". Defaults to "daily", since a dependence estimate needs far more observations than a
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

The formula is as follows (with the default alpha of 0.05):

$$
\text{VaR}_{\text{alpha}}(\text{Market}) = \operatorname{Quantile}(\text{Market Returns within the period},\; \alpha)
$$

$$
\text{MES} = \operatorname{MEAN}(\text{Returns}_{t} \mid \text{Market Return}_{t} \leq \text{VaR}_{\text{alpha}}(\text{Market}))
$$

Where the returns are the daily returns of the Adjusted Close within the period on the days the ticker and the market both have a return, and the quantile interpolates linearly between the two nearest returns. The MES is reported as a return, negative for a loss, like the Value at Risk and the Conditional Value at Risk (the paper reports the loss, -MES). With `rolling`, the days of the last `rolling` periods are used together.

**Also known as:** MES, marginal expected shortfall, systemic expected shortfall, tail beta.

**References:**

- paper | Acharya, V.V., Pedersen, L.H., Philippon, T., & Richardson, M. (2017). "Measuring Systemic Risk." The Review of Financial Studies, 30(1), 2-47.

**Args:**

- <u>ticker (str &#124; None, optional):</u> The ticker whose MES to calculate. Defaults to None, which
uses every ticker except the market and the benchmark.
- <u>market_ticker (str &#124; None, optional):</u> The ticker that represents the - <u>market (the system):</u> the
benchmark by its own ticker (SPY) or as "Benchmark", one of the tickers, or a ticker outside
the Toolkit (such as ^GSPC), whose returns are retrieved for the same dates. Defaults to None,
which uses the benchmark.
- <u>period (str, optional):</u> The period of each estimate. Options are: "monthly", "quarterly",
"yearly". Defaults to "yearly", as in the paper.
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
- A period with fewer than 1 / alpha shared returns (20 at an alpha of 0.05) is NaN, as its tail would hold
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

The formula is as follows (with the default decline of 0.4 and capital ratio of 0.08):

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

**Also known as:** systemic risk, capital shortfall, SRISK%, long-run marginal expected shortfall, LRMES.

**References:**

- paper | Brownlees, C., & Engle, R.F. (2017). "SRISK: A Conditional Capital Shortfall Measure of Systemic Risk." The Review of Financial Studies, 30(1), 48-79.
- paper | Acharya, V.V., Engle, R.F., & Richardson, M. (2012). "Capital Shortfall: A New Approach to Ranking and Regulating Systemic Risks." American Economic Review, 102(3), 59-64.
- library | Shares similar logic as empyrical's [beta](https://github.com/quantopian/empyrical/blob/0.5.5/empyrical/stats.py#L1314){:target="_blank"} (Beta)

**Args:**

- <u>ticker (str &#124; None, optional):</u> The ticker whose SRISK to calculate. Defaults to None, which
uses every ticker except the market and the benchmark.
- <u>market_ticker (str &#124; None, optional):</u> The ticker that represents the market: the benchmark by
its own ticker (SPY) or as "Benchmark", one of the tickers, or a ticker outside the Toolkit
(such as ^GSPC), whose returns are retrieved for the same dates. Defaults to None, which uses
the benchmark.
- <u>period (str, optional):</u> The period of each estimate. Options are: "monthly", "quarterly",
"yearly". Defaults to "yearly".
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
A quarterly Toolkit uses the latest quarter, as V-Lab does. The market cap is the traded
(split-adjusted) Close times the diluted share count, which for periods that coincide with the fiscal
periods equals `toolkit.ratios.get_market_cap`.
- The Close is in the currency the ticker trades in, while the statements are in the currency they
are reported in unless the Toolkit converts them to the currency of the prices (currency conversion);
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
Calculate the Tail Ratio: how large the best returns of an investment portfolio or asset are compared with its worst returns.

The Tail Ratio compares the size of the right (gain) tail to the left (loss) tail of the return distribution. A Tail Ratio above 1 indicates that best-case gains outsize worst-case losses.

The formula is as follows:

$$
\text{Tail Ratio} = \frac{\left|\operatorname{Quantile}(\text{Returns},\; 1 - \alpha)\right|}{\left|\operatorname{Quantile}(\text{Returns},\; \alpha)\right|}
$$

The quantiles interpolate linearly, and a left-tail quantile of 0 gives NaN.

**Also known as:** gain-to-pain tail ratio.

**References:**

- library | Shares similar logic as empyrical's [tail_ratio](https://github.com/quantopian/empyrical/blob/0.5.5/empyrical/stats.py#L1501){:target="_blank"}
- library | Shares similar logic as quantstats' [tail_ratio](https://github.com/ranaroussi/quantstats/blob/v0.0.86/quantstats/stats.py#L2192){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The data frequency for returns. Options are: "daily", "weekly", "monthly",
"quarterly", "yearly". Defaults to "daily".
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
- With growth, the method calculates the growth of Tail Ratio values using the specified `lag`.

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
Calculate the Skewness: how asymmetric the returns of an investment portfolio or asset are, negative when the large deviations from the mean are losses.

Skewness is a statistical measure used in finance to assess the asymmetry in the distribution of returns for an investment portfolio or asset over a defined period. It offers valuable insights into the shape of the return distribution, indicating whether returns are skewed towards the positive or negative side of the mean. Skewness is a crucial tool for investors and analysts seeking to understand the potential risk and return characteristics of an investment, aiding in the assessment of the distribution's tails and potential outliers. It provides a means to gauge the level of skew in returns, enabling more informed investment decisions and risk management strategies.

The formula is as follows:

$$
\text{Skewness} = \frac{n}{(n - 1) \cdot (n - 2)} \cdot \sum\left(\frac{\text{Return} - \text{Mean}}{\text{Std}}\right)^{3}
$$

Where n is the number of returns and Std the sample standard deviation (with n - 1 in the denominator), which is the bias-adjusted sample skewness (G1) of pandas and Excel's SKEW.

**Also known as:** return distribution asymmetry, tail skew.

**References:**

- library | Shares similar logic as scipy's [skew](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.skew.html){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The data frequency for returns. Options are: "daily", "weekly", "monthly",
"quarterly", "yearly". Defaults to "daily".
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
- With growth, the method calculates the growth of Skewness values using the specified `lag`.
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
Calculate the Kurtosis: how heavy the tails of the returns of an investment portfolio or asset are, how likely extreme returns are compared with a normal distribution.

Kurtosis is a statistical measure used in finance to evaluate the shape of the probability distribution of returns for an investment portfolio or asset over a defined time period. It assesses the "tailedness" of the return distribution, indicating whether returns have fatter or thinner tails compared to a normal distribution. Kurtosis plays a critical role in risk assessment by revealing the potential presence of extreme outliers or the likelihood of heavy tails in the return data. This information aids investors and analysts in understanding the degree of risk associated with an investment and assists in making more informed decisions regarding risk tolerance. In essence, kurtosis serves as a valuable tool for comprehending the distribution characteristics of returns, offering insights into the potential for rare but significant events in the financial markets.

By default this is Pearson's kurtosis, which is 3 for a normal distribution; Fisher's definition gives the excess kurtosis, which is 0. Daily stock returns typically show an excess kurtosis of several points, and within a single year one exceptional day (an earnings shock, a market-wide gap) can push it above 10, so a high value often reflects one event rather than a persistently fat-tailed distribution.

The formula is as follows:

$$
\text{Kurtosis} = \text{Excess Kurtosis} + 3
$$

$$
\text{Excess Kurtosis} = \frac{n(n + 1)}{(n - 1) (n - 2) (n - 3)} \cdot \sum z^{4} - \frac{3(n - 1)^{2}}{(n - 2) (n - 3)}
$$

$$
z = \frac{\text{Return} - \text{Mean}}{\text{Std}}
$$

Where n is the number of returns and Std the sample standard deviation (with n - 1 in the denominator), which is the bias-adjusted sample excess kurtosis (G2) of pandas and Excel's KURT. Fisher's definition returns the Excess Kurtosis.

**Also known as:** tail heaviness, fat tails, leptokurtosis.

**References:**

- library | Shares similar logic as scipy's [kurtosis](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.kurtosis.html){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The data frequency for returns. Options are: "daily", "weekly", "monthly",
"quarterly", "yearly". Defaults to "daily".
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
- With growth, the method calculates the growth of Kurtosis values using the specified `lag`.
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
Calculate the Hill Estimator of the tail index of returns: how heavy the tail of each asset's return distribution is, smaller for a heavier tail.

Unlike the (finite-sample) Skewness and Kurtosis above, the Hill Estimator is a semi-parametric estimate of how heavy the tail of the return distribution actually is, under the assumption that the tail follows a Pareto-type power law. Smaller values of the tail index indicate a heavier tail (more extreme outliers are likely) -- as a rule of thumb, a tail index below 4 implies the Kurtosis is theoretically infinite, and below 2 implies the Variance itself is theoretically infinite.

For daily stock returns the tail index typically lies between about 2 and 5, while a normal distribution has an infinite tail index. The estimate depends on `k`: practitioners plot it against a range of `k` (a Hill plot) and read it where it is stable, since a small `k` is noisy and a large `k` pulls in the center of the distribution.

The formula is as follows:

$$
\text{Hill Shape} \;(\xi) = \frac{1}{k} \cdot \sum(\ln X_{(i)} - \ln X_{(k+1)}) \;\text{for}\; i = 1,\; \ldots,\; k
$$

$$
\text{Hill Tail Index} = \frac{1}{\xi}
$$

$$
\text{Standard Error} = \frac{\text{Hill Tail Index}}{\sqrt{k}}
$$

Where $$X_{1} \geq X_{2} \geq \ldots$$ are the strictly positive losses (the negated returns, or the returns themselves for the right tail) sorted from large to small, and k is the number of order statistics used: int(0.1 * the number of positive losses) by default, or `k` itself when it is an integer.

**Also known as:** Hill tail index estimator, Hill's estimator.

**References:**

- paper | Hill, B.M. (1975). "A Simple General Approach to Inference About the Tail of a Distribution." The Annals of Statistics, 3(5), 1163-1174.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns. Options are: "daily", "weekly", "monthly",
"quarterly", "yearly". Defaults to "daily".
- <u>within_period (bool, optional):</u> Whether to calculate the estimator within the specified period
or for the entire period. Defaults to False.
Note that this requires intraday data when period = 'daily', since a
single day only nests observations when intraday data was fetched.
- <u>k (int &#124; float, optional):</u> The number of upper order statistics to use. If a float in (0, 1)
it is interpreted as the fraction of the strictly positive observations to use. A period
without such observations reports NaN with 0 observations used. Defaults to 0.1 (the top 10%).
- <u>tail (str, optional):</u> Which tail to estimate. Options are: "left" (the loss tail), "right" (the
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
Calculate the Variance: how widely the daily returns of an investment portfolio or asset spread around their mean in each period.

Variance measures the spread or dispersion of returns around the mean. A higher Variance indicates more variability in the returns, while a lower Variance suggests that the returns are closer to the mean.

The formula is as follows:

$$
\text{Variance} = \operatorname{Var}(\text{Daily Returns within the period}) \cdot \text{Trading Days per Period}
$$

Where Var is the sample variance (with n - 1 in the denominator) and the trading days per period are 252 / 52 (weekly), 252 / 12 (monthly), 252 / 4 (quarterly) or 252 (yearly). A ticker with returns on weekends, such as a cryptocurrency, has a return on every calendar day and uses 365 days a year instead (365 / 52 weekly). With `rolling`, the result is the sample variance of the last `rolling` returns of the chosen period itself, without scaling.

**Also known as:** dispersion, spread.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns. Options are: "weekly", "monthly", "quarterly",
"yearly". Defaults to "quarterly" if the Toolkit is initialised with quarterly=True, otherwise
"yearly".
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
- With growth, the method calculates the growth of Variance values using the specified `lag`.

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
Calculate the Mean Absolute Deviation (MAD): how far the daily returns of an investment portfolio or asset lie from their mean on average in each period.

MAD measures the average absolute distance of each return from the mean return. Unlike Variance and Volatility, it does not square the deviations, making it less sensitive to outliers.

The formula is as follows:

$$
\text{Mean Absolute Deviation} = \frac{\sum\left|\text{Return}_{t} - \text{Mean}\right|}{n}
$$

Where the returns are the n daily returns within each period, without scaling to the period length.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns. Options are: "weekly", "monthly", "quarterly",
"yearly". Defaults to "quarterly" if the Toolkit is initialised with quarterly=True, otherwise
"yearly".
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
- With growth, the method calculates the growth of MAD values using the specified `lag`.

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
Calculate the Coefficient of Variation (CV): how large the spread of the daily returns of an investment portfolio or asset is relative to their mean in each period.

The Coefficient of Variation is the ratio of the standard deviation to the mean of returns, which normalizes dispersion relative to the average return. This makes it useful for comparing the relative volatility of assets with different average returns, which a raw standard deviation cannot do.

The Coefficient of Variation is only meaningful when the mean return is clearly positive. In a period with an average daily return close to zero it explodes, and in a down period it turns negative, so for returns it is best read over periods with a positive mean, or replaced by a Sharpe ratio, which is its inverse with the risk-free rate subtracted.

The formula is as follows:

$$
\text{Coefficient of Variation} = \frac{\operatorname{Std}(\text{Daily Returns})}{\operatorname{Mean}(\text{Daily Returns})}
$$

Where both are taken over the daily returns within each period, with Std the sample standard deviation (with n - 1 in the denominator), without scaling to the period length.

**Also known as:** relative standard deviation.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns. Options are: "weekly", "monthly", "quarterly",
"yearly". Defaults to "quarterly" if the Toolkit is initialised with quarterly=True, otherwise
"yearly".
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
- With growth, the method calculates the growth of CV values using the specified `lag`.

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

## get_autocorrelation
Calculate the Autocorrelation Function (ACF) of each asset's daily returns: how strongly a return is related to the returns before it, for a range of lags.

The ACF measures the correlation between a return series and a lagged version of itself. A significant ACF at a given lag indicates that returns are not fully independent over time, which is relevant for assessing return predictability and volatility clustering (as opposed to a trading-signal use case, which is why this lives in the Risk module rather than Technicals).

The formula is as follows:

$$
\operatorname{ACF}(k) = \frac{\sum(r_{t} - \text{Mean}) \cdot (r_{t+k} - \text{Mean})}{\sum(r_{t} - \text{Mean})^{2}}
$$

Where $$r_{t}$$ are the n daily returns (missing values dropped), the numerator runs over $$t = 1$$, ..., n - k, the denominator over all n returns, and $$k = 1$$, ..., `lags` (10 by default). A lag of n or more has no pairs of returns and is NaN.

**References:**

- library | Referenced against statsmodels' [acf](https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.acf.html){:target="_blank"}

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
Calculate the Hurst Exponent of each asset: its long-term memory, which shows whether the price is mean-reverting, trending, or a random walk.

The Hurst Exponent (H) is interpreted as follows:

- $$H < 0.5$$: the series is mean-reverting (anti-persistent).
- $$H = 0.5$$: the series is a random walk (no memory).
- $$H > 0.5$$: the series is trending (persistent).

For liquid stocks the estimate is usually close to 0.5, and with lags of at most `max_lag` days it describes short-term behaviour only; a value of 0.45 or 0.55 over a few years is within estimation noise rather than evidence of a tradable pattern, so the exponent is mostly of use to compare assets or periods (with `rolling`) with each other.

The methods are as follows:

$$
\text{Generalized (Di Matteo, Aste and Dacorogna, 2005)},\;\; \text{on the}\; \log \;\text{prices}\; X = \ln \text{P:} \;K_{q}(\tau) = \operatorname{Mean}(\operatorname{abs}(d - \operatorname{Mean}(d))^{q}) \;\text{of the differences}\; d = X_{(t+\tau)} - X_{t},\;\; \text{and}\;\; \ln K_{q}(\tau) = c + q \cdot H(q) \cdot \ln \tau,\;\; \text{fitted by least squares over}\; \tau = 2,\; \ldots,\; 20.\;\; \text{With}\; q = 2 \;\text{this is the slope of the}\; \log \;\text{standard deviation} \;(\text{with}\; n \;\text{in the denominator}) \;\text{of the lagged differences on the}\; \log \;\text{lag}.\;\; \text{A list of } q \text{ gives } H \text{(} q \text{) per } q \text{: for fat-tailed returns } H \text{(1) above } H \text{(2) points to multifractality}
$$

$$
\text{Rescaled range (Hurst, 1951; Anis and Lloyd, 1976; Peters, 1994), on the log returns } x \text{:}\;\; \text{within windows of } n \text{ returns},\;\; \text{R/S} = \frac{\max(Y) - \min(Y)}{\operatorname{Std}(x)} \;\text{with}\; Y \;\text{the cumulative deviations from the window mean and Std the population standard deviation};\;\; \left(\frac{R}{S}\right) (n) \;\text{its average over the} \;\left\lfloor \frac{N}{n} \right\rfloor \;\text{windows},\;\; \text{and}\;\; H = 0.5 + \text{slope of}\; \ln \left(\frac{R}{S}\right) (n) - \ln E\left[\frac{R}{S}\right] (n) \;\text{on}\; \ln n,\;\; \text{with}\;\; E\left[\frac{R}{S}\right] (n) = \frac{\frac{n - 0.5}{n} \cdot \Gamma\left(\frac{n - 1}{2}\right)}{\operatorname{Sqrt}(\pi) \cdot \Gamma\left(\frac{n}{2}\right)} \cdot \operatorname{Sum}\left(\operatorname{Sqrt}\left(\frac{n - i}{i}\right),\; i = 1,\; \ldots,\; n - 1\right) \;\text{the expected rescaled range of independent returns}.\;\; \text{Without the correction, } H \text{ is the slope of ln (} R \text{/} S \text{)(} n \text{) on ln } n
$$

$$
\text{Detrended fluctuation (Peng et al., 1994), on the log returns } x \text{:}\;\; \text{the profile}\; Y_{k} = \operatorname{Sum}(x_{i} - \operatorname{Mean}(x)) \;\text{is cut into windows of}\; n,\;\; \text{a straight line (a polynomial of degree order) is fitted and removed in every window},\;\; F(n) = \operatorname{Sqrt}(\operatorname{Mean}(\text{residual}^{2}))\;\;\text{and}\;\; H (\alpha) = \text{slope of}\; \ln F(n) \;\text{on}\; \ln n
$$

The window sizes n of the rescaled range and the detrended fluctuation grow by 20% from 10 up to a tenth of the observations, so every size has at least ten windows.

**Also known as:** generalized Hurst exponent, GHE, R/S analysis, rescaled range, DFA, detrended fluctuation analysis, multifractal Hurst exponent.

**References:**

- paper | Di Matteo, T., Aste, T., & Dacorogna, M.M. (2005). "Long-Term Memories of Developed and Emerging Markets: Using the Scaling Analysis to Characterize Their Stage of Development." Journal of Banking & Finance, 29(4), 827-851.
- paper | Di Matteo, T. (2007). "Multi-scaling in finance." Quantitative Finance, 7(1), 21-36.
- paper | Hurst, H.E. (1951). "Long-term storage capacity of reservoirs." Transactions of the American Society of Civil Engineers, 116, 770-799.
- paper | Anis, A.A. & Lloyd, E.H. (1976). "The expected value of the adjusted rescaled Hurst range of independent normal summands." Biometrika, 63(1), 111-116.
- paper | Peters, E.E. (1994). "Fractal Market Analysis." Wiley.
- paper | Peng, C.-K., Buldyrev, S.V., Havlin, S., Simons, M., Stanley, H.E. & Goldberger, A.L. (1994). "Mosaic organization of DNA nucleotides." Physical Review E, 49(2), 1685-1689.
- library | Referenced against nolds' [hurst_rs](https://github.com/CSchoel/nolds/blob/0.6.3/nolds/measures.py#L1203){:target="_blank"} (rescaled range)
- library | Referenced against nolds' [dfa](https://github.com/CSchoel/nolds/blob/0.6.3/nolds/measures.py#L1997){:target="_blank"} (detrended fluctuation)
- library | Shares similar logic as nolds' [mfhurst_dm](https://github.com/CSchoel/nolds/blob/0.6.3/nolds/measures.py#L1695){:target="_blank"} (generalized)
- library | Shares similar logic as antropy's [detrended_fluctuation](https://github.com/raphaelvallat/antropy/blob/v0.2.3/src/antropy/fractal.py#L369){:target="_blank"} (detrended fluctuation)

**Args:**

- <u>max_lag (int, optional):</u> The maximum lag of the generalized method, included: the
regression runs over the lags 2 up to and including `max_lag`. Defaults to 20.
- <u>method (str, optional):</u> The estimation method. Options are: "generalized" (generalized Hurst
exponent), "rescaled_range" (rescaled range), "detrended_fluctuation" (detrended fluctuation
analysis). Defaults to "generalized".
- <u>period (str &#124; None, optional):</u> The data frequency. Options are: "daily", "weekly", "monthly", "quarterly",
"yearly". Defaults to None, which uses "daily".
- <u>rolling (int &#124; None, optional):</u> The number of periods of a rolling window. Defaults to
None, which calculates one value over the full history of every asset.
- <u>q (float &#124; list[float], optional):</u> The order of the moment of the generalized method,
or a list of orders for a column per order. Defaults to 2.0.
- <u>window_sizes (list[int] &#124; None, optional):</u> The window sizes of the rescaled range and
the detrended fluctuation. Defaults to None, which uses 10 up to a tenth of the
observations, growing by 20%.
- <u>corrected (bool, optional):</u> Whether to apply the Anis-Lloyd-Peters correction to the
rescaled range. Defaults to True.
- <u>order (int, optional):</u> The degree of the polynomial removed from every window of the
detrended fluctuation. Defaults to 1.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series &#124; pd.DataFrame: The Hurst Exponent per asset, with `rolling` per date (a
column per asset), and with a list of q a column "H(q)" per order.

**Notes:**

- The generalized method works on the log prices: their lagged differences are log returns
over the lag, whose dispersion does not depend on the price level. The rescaled range
and the detrended fluctuation work on the log returns, the differences of the log prices.
- The rescaled range equals nolds' hurst_rs without its unbiased standard deviation and with a polynomial fit,
and the detrended fluctuation nolds' dfa without overlapping windows and with a polynomial fit, for the same
window sizes. nolds' mfhurst_dm samples the differences without overlap, detrends the series and averages
over the largest lags 5 to 19, so it differs by about 0.01 to 0.03.

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
| EURUSD    |  0.4718 |
| GCUSD     |  0.4617 |
| BTCUSD    |  0.5057 |
| Benchmark |  0.4396 |

---

## get_fractal_dimension
Calculate the Fractal Dimension of each asset's log price path: how rough the path is, between 1 for a straight line and 2 for a path that fills the plane.

A random walk has a Higuchi dimension of 1.5, which is 2 - H for a self-affine path with Hurst exponent H: a trending path has a lower and a mean-reverting path a higher dimension. The Katz and Petrosian dimensions are quick measures of the same roughness on their own scales: Katz from how far the path gets for the distance it travels and Petrosian from how often it turns. Price paths are close to random walks, so the dimensions are mostly of use to compare assets or periods (with `rolling`).

The methods are as follows (on the log prices x of N periods):

$$
\text{Higuchi (1988):}\;\; L_{m}(k) = \frac{\frac{\operatorname{Sum}(\operatorname{abs}(x_{m+i*k} - x_{}(m + (i - 1) \cdot k))) \cdot (N - 1)}{\left\lfloor \frac{N - m}{k} \right\rfloor \cdot k}}{k},\;\; L(k) = \operatorname{Mean}(L_{m}(k)) \;\text{over}\; m = 1,\; \ldots,\; k,\;\; \text{and}\;\; \text{FD} = - \text{slope of}\; \ln L(k) \;\text{on}\; \ln k \;\text{over}\; k = 1,\; \ldots,\; \text{kmax}
$$

$$
\text{Katz (1988):}\;\; \text{FD} = \frac{\log_{10}(n)}{\log_{10}(n) + \log_{10}\left(\frac{d}{L}\right)},\;\; \text{with}\;\; L = \operatorname{Sum}(\operatorname{abs}(x_{i+1} - x_{i})) \;\text{the length of the path},\;\; d = \max(\operatorname{abs}(x_{i} - x_{1})) \;\text{its largest distance from the start}\;\;\text{and}\;\; n = N - 1 \;\text{the number of steps}
$$

$$
\text{Petrosian (1995):}\;\; \text{FD} = \frac{\log_{10}(N)}{\log_{10}(N) + \log_{10}\left(\frac{N}{N + 0.4 \cdot N_{\delta}}\right)},\;\; \text{with } N_{\delta} \text{ the number of sign changes of the returns (a return of 0 interrupts one)}
$$

**Also known as:** HFD, KFD, PFD, Higuchi fractal dimension, fractal roughness.

**References:**

- paper | Higuchi, T. (1988). "Approach to an irregular time series on the basis of the fractal theory." Physica D, 31(2), 277-283.
- paper | Katz, M.J. (1988). "Fractals and the analysis of waveforms." Computers in Biology and Medicine, 18(3), 145-156.
- paper | Petrosian, A. (1995). "Kolmogorov complexity of finite sequences and recognition of different preictal EEG patterns." Proceedings of the Eighth IEEE Symposium on Computer-Based Medical Systems, 212-217.
- library | Referenced against antropy's [higuchi_fd](https://github.com/raphaelvallat/antropy/blob/v0.2.3/src/antropy/fractal.py#L232){:target="_blank"}
- library | Referenced against antropy's [katz_fd](https://github.com/raphaelvallat/antropy/blob/v0.2.3/src/antropy/fractal.py#L104){:target="_blank"}
- library | Referenced against antropy's [petrosian_fd](https://github.com/raphaelvallat/antropy/blob/v0.2.3/src/antropy/fractal.py#L14){:target="_blank"}

**Args:**

- <u>method (str, optional):</u> The fractal dimension. Options are: "higuchi" (Higuchi), "katz" (Katz),
"petrosian" (Petrosian). Defaults to "higuchi".
- <u>period (str &#124; None, optional):</u> The data frequency. Options are: "daily", "weekly", "monthly", "quarterly",
"yearly". Defaults to None, which uses "daily".
- <u>rolling (int &#124; None, optional):</u> The number of periods of a rolling window. Defaults to
None, which calculates one value over the full history of every asset.
- <u>kmax (int, optional):</u> The largest step k of the Higuchi dimension. Defaults to 10.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series &#124; pd.DataFrame: The fractal dimension per asset, or with `rolling` per date
(a column per asset).

**Notes:**

- The dimensions equal antropy's higuchi_fd, katz_fd and petrosian_fd of the log prices.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["EURUSD", "GCUSD", "BTCUSD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_fractal_dimension()
```

Which returns:

|           |   Value |
|:----------|--------:|
| EURUSD    |  1.515  |
| GCUSD     |  1.4903 |
| BTCUSD    |  1.4827 |
| Benchmark |  1.5085 |

---

## get_correlation_dimension
Calculate the Correlation Dimension of each asset's log returns by the Grassberger-Procaccia algorithm: the dimension of the set that stretches of consecutive returns fill, low for a deterministic process.

A deterministic, chaotic process fills a set of a low dimension however many returns a stretch holds; for noise the dimension grows with the embedding dimension (close to it for independent returns). Daily returns behave mostly like noise, so a value well below the embedding dimension is the exception, and comparing several embedding dimensions shows whether the dimension levels off.

The formula is as follows:

$$
X_{i} = \left[x_{i},\; x_{i+\tau},\; \ldots,\; x_{}(i + (m - 1) \cdot \tau)\right],\;\; \text{the delay embedding of the log returns}
$$

$$
C(r) = \frac{2}{M \cdot (M - 1)} \cdot \operatorname{Sum}(1\left[\left\|X_{i} - X_{j}\right\| < r\right],\; i < j),\;\; \frac{\text{the share of the}\; M \cdot (M - 1)}{2 \;\text{pairs of vectors closer than}\; r}
$$

$$
D_{2} = \text{slope of}\; \ln C(r) \;\text{on}\; \ln r
$$

with &#124;&#124;.&#124;&#124; the Euclidean norm and, by default, the radii (3% apart) at which C(r) lies between 0.0001 and 0.01.

**Also known as:** D2, Grassberger-Procaccia dimension, correlation integral.

**References:**

- paper | Grassberger, P. & Procaccia, I. (1983). "Characterization of strange attractors." Physical Review Letters, 50(5), 346-349.
- library | Shares similar logic as nolds' [corr_dim](https://github.com/CSchoel/nolds/blob/0.6.3/nolds/measures.py#L1848){:target="_blank"}

**Args:**

- <u>period (str &#124; None, optional):</u> The data frequency. Options are: "daily", "weekly", "monthly", "quarterly",
"yearly". Defaults to None, which uses "daily".
- <u>embedding (int, optional):</u> The embedding dimension m. Defaults to 10.
- <u>delay (int, optional):</u> The number of periods between the returns of a vector.
Defaults to 1.
- <u>radii (list[float] &#124; None, optional):</u> The radii as multiples of the standard deviation
(with n - 1 in the denominator) of the returns. Defaults to None, which uses the radii at which C(r) lies
between 0.0001 and 0.01.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series: The correlation dimension per asset.

**Notes:**

- Every pair of vectors is compared, so the time grows with the square of the number of
returns: about 0.6 seconds for ten years of daily returns.
- With the radii given, it equals a direct count of the pairs closer than every radius. nolds'
corr_dim also counts every vector as a pair with itself, which pulls its slope towards
0 where few pairs are close (0 for ten daily returns at its default radii of 0.1 to 0.5
standard deviations, at which there are hardly any pairs).

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["EURUSD", "GCUSD", "BTCUSD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_correlation_dimension(embedding=4)
```

Which returns:

|           |   Value |
|:----------|--------:|
| EURUSD    |  4.0576 |
| GCUSD     |  3.6576 |
| BTCUSD    |  3.8436 |
| Benchmark |  3.8736 |

---

## get_lyapunov_exponent
Calculate the Lyapunov Exponent of each asset's log returns: the rate, per period, at which nearby paths of the reconstructed dynamics move apart, positive for a chaotic process.

A positive largest exponent points to chaos, a sensitive dependence on the starting point that makes the series unpredictable beyond a few periods even if it were deterministic; a value around 0 or below to a regular process. For noise, such as daily returns, the estimate is not 0 but depends on the embedding, so the exponent is mostly of use to compare assets or periods with each other.

The methods are as follows ($$X_{i}$$ the delay embedding of the log returns x):

$$
\text{Rosenstein, Collins and De Luca (1993):}\;\; \text{every vector } X_{i} \text{ is paired with its nearest neighbour } X_{j} \text{ (Euclidean) at least min\_separation periods away},\;\; y(k) = \operatorname{Mean}(\ln \left\|X_{(i+k)} - X_{(j+k)}\right\|) \;\text{for}\; k = 0,\; \ldots,\; \text{trajectory\_length} - 1,\;\; \text{and}\;\; \lambda_{1} = \text{slope of} \;y(k) \;\text{on}\; k,\;\; \text{the largest exponent}
$$

$$
\text{Eckmann, Kamphorst, Ruelle and Ciliberto (1986):}\;\; \text{with}\;\; m = \frac{\text{embedding} - 1}{\text{matrix\_dimension} - 1},\;\; \text{a linear map}\; T_{i} \;\text{from}\; X_{i} = \left[x_{i},\; x_{i+m},\; \ldots\right] \;\text{to}\; X_{(i+m)} \;\text{is fitted by least squares on the}\; \text{min\_neighbors} \;\text{nearest neighbours} \;(\text{Chebyshev});\;\; \text{the maps are multiplied along the path with a QR decomposition}\; T_{i} Q_{i-m} = Q_{i} R_{i}\;\;\text{and}\;\; \lambda_{k} = \frac{\operatorname{Mean}(\ln \;\text{abs}(R_{i,\text{kk}}))}{m},\;\; \text{the matrix\_dimension largest exponents}
$$

**Also known as:** largest Lyapunov exponent, LLE, Lyapunov spectrum, chaos exponent.

**References:**

- paper | Rosenstein, M.T., Collins, J.J. & De Luca, C.J. (1993). "A practical method for calculating largest Lyapunov exponents from small data sets." Physica D, 65(1-2), 117-134.
- paper | Eckmann, J.-P., Kamphorst, S.O., Ruelle, D. & Ciliberto, S. (1986). "Liapunov exponents from time series." Physical Review A, 34(6), 4971-4979.
- library | Referenced against nolds' [lyap_r](https://github.com/CSchoel/nolds/blob/0.6.3/nolds/measures.py#L117){:target="_blank"} (Rosenstein)
- library | Referenced against nolds' [lyap_e](https://github.com/CSchoel/nolds/blob/0.6.3/nolds/measures.py#L400){:target="_blank"} (Eckmann)

**Args:**

- <u>method (str, optional):</u> The algorithm. Options are: "rosenstein" (Rosenstein, Collins and De
Luca, the largest exponent), "eckmann" (Eckmann, Kamphorst, Ruelle and Ciliberto, the
spectrum). Defaults to "rosenstein".
- <u>period (str &#124; None, optional):</u> The data frequency. Options are: "daily", "weekly", "monthly", "quarterly",
"yearly". Defaults to None, which uses "daily".
- <u>embedding (int, optional):</u> The embedding dimension; for "eckmann", embedding - 1 must be
a multiple of matrix_dimension - 1. Defaults to 10.
- <u>delay (int, optional):</u> The number of periods between the returns of a vector of the
Rosenstein method. Defaults to 1.
- <u>min_separation (int &#124; None, optional):</u> The smallest number of periods between a vector
and its neighbour. Defaults to None, which uses the mean period of the returns
(one over the power-weighted mean frequency of the periodogram, rounded up) for
"rosenstein" and 0 for "eckmann".
- <u>trajectory_length (int, optional):</u> The number of periods the pairs of the Rosenstein
method are followed. Defaults to 20.
- <u>matrix_dimension (int, optional):</u> The number of exponents of the Eckmann method.
Defaults to 4.
- <u>min_neighbors (int &#124; None, optional):</u> The number of neighbours of every vector of the
Eckmann method. Defaults to None, which uses min(2 * matrix_dimension,
matrix_dimension + 4).
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series &#124; pd.DataFrame: The largest exponent per asset, or for "eckmann" the
exponents "Exponent 1" to "Exponent d" per asset (a row per asset), per period.

**Notes:**

- Every vector is compared with every other one, so the time grows with the square of the
number of returns: about 1 second for the Rosenstein and 2 seconds for the Eckmann
method on ten years of daily returns.
- The Rosenstein method equals nolds' lyap_r with the same delay and minimum separation and a
polynomial fit.
The Eckmann method multiplies the maps along each path i, i + m, i + 2m, ..., where
nolds' lyap_e multiplies the maps of consecutive vectors; with $$m = 1$$ both are equal, and
on the Hénon map (largest exponent 0.42) the paths here give 0.42 for $$m = 2$$ and 3, where
nolds gives 0.45 and 0.47.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["EURUSD", "GCUSD", "BTCUSD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_lyapunov_exponent()
```

Which returns:

|           |   Value |
|:----------|--------:|
| EURUSD    |  0.0388 |
| GCUSD     |  0.0398 |
| BTCUSD    |  0.0395 |
| Benchmark |  0.0409 |

---

## get_partial_moment
Calculate the Lower (or Upper) Partial Moment: how often and how far the returns of an investment portfolio or asset fall below (or rise above) a minimum acceptable return.

A partial moment measures only one side of the return distribution: the lower partial moment averages the shortfalls below a minimum acceptable return (MAR) raised to a power, the order, and the upper partial moment does the same for the returns above it. The order sets what is measured: order 0 is how often the returns fall below the MAR (the downside frequency), order 1 how far they fall below it on average (the downside potential, the expected shortfall below the target), order 2 the downside variance behind the Sortino Ratio and higher orders the weight of the extreme losses. Investors who care about losses rather than about deviations in either direction use them in place of the variance, and the ratio of an upper to a lower partial moment is the Omega Ratio (order 1) and the Upside Potential Ratio's building block.

The formula is as follows:

$$
\text{Lower Partial Moment} = \frac{\sum \max(\text{MAR} - \text{Return}_{t},\; 0)^{\text{order}}}{n}
$$

$$
\text{Upper Partial Moment} = \frac{\sum \max(\text{Return}_{t} - \text{MAR},\; 0)^{\text{order}}}{n}
$$

Where n is the number of all returns, so the returns on the other side of the MAR count as zero rather than being left out. Of order 0 the moment counts the returns strictly below (or above) the MAR, as a share of all returns. Raised to the power 1 / order (its root), order 2 becomes the Downside Deviation (the lower side) or the Upside Deviation (the upper side). With the mean of each sample as the MAR it gives the semi-moments around the mean (order 2: the semi-variance with n in the denominator).

**Also known as:** LPM, UPM, downside potential, downside frequency, upside frequency, upside potential, shortfall probability, semi-moment.

**References:**

- paper | Bawa, V.S. (1975). "Optimal Rules for Ordering Uncertain Prospects." Journal of Financial Economics, 2(1), 95-121.
- paper | Fishburn, P.C. (1977). "Mean-Risk Analysis with Risk Associated with Below-Target Returns." The American Economic Review, 67(2), 116-126.
- paper | Bacon, C.R. (2008). "Practical Portfolio Performance Measurement and Attribution." John Wiley & Sons, chapter 4 (Downside Potential, Downside and Upside Frequency, Upside Potential).
- library | Referenced against Riskfolio-Lib's [LPM](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/risk.html#RiskFunctions.LPM){:target="_blank"}
- library | Referenced against Riskfolio-Lib's [SemiKurtosis](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/risk.html#RiskFunctions.SemiKurtosis){:target="_blank"}
- library | Referenced against skfolio's [first_lower_partial_moment](https://skfolio.org/generated/skfolio.measures.first_lower_partial_moment.html){:target="_blank"}
- library | Referenced against skfolio's [fourth_lower_partial_moment](https://skfolio.org/generated/skfolio.measures.fourth_lower_partial_moment.html){:target="_blank"}
- library | Shares similar logic as PerformanceAnalytics (R)'s [DownsideFrequency](https://github.com/braverock/PerformanceAnalytics/blob/v2.0.4/R/DownsideFrequency.R#L35){:target="_blank"}
- library | Shares similar logic as PerformanceAnalytics (R)'s [UpsideFrequency](https://github.com/braverock/PerformanceAnalytics/blob/v2.0.4/R/UpsideFrequency.R#L35){:target="_blank"}
- library | Shares similar logic as PerformanceAnalytics (R)'s [UpsideRisk](https://github.com/braverock/PerformanceAnalytics/blob/v2.0.4/R/UpsideRisk.R#L54){:target="_blank"}
- library | Shares similar logic as PerformanceAnalytics (R)'s [DownsidePotential](https://github.com/braverock/PerformanceAnalytics/blob/v2.0.4/R/DownsideDeviation.R#L166){:target="_blank"}
- library | Shares similar logic as PerformanceAnalytics (R)'s [lpm](https://github.com/braverock/PerformanceAnalytics/blob/v2.0.4/R/lpm.R#L23){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The data frequency for returns. Options are: "daily", "weekly", "monthly",
"quarterly", "yearly". Defaults to "daily".
- <u>order (float, optional):</u> The order of the moment, 0 or higher: 0 for the frequency, 1 for the
potential, 2 for the variance and higher orders for the extremes. Defaults to 1.
- <u>minimum_acceptable_return (float &#124; str, optional):</u> The minimum acceptable return (MAR) per
observation of the chosen `period` (e.g. per day), or "mean" for the mean of each sample.
Defaults to 0.0.
- <u>side (str, optional):</u> The side of the MAR. Options are: "lower" (the returns below the MAR),
"upper" (the returns above it). Defaults to "lower".
- <u>root (bool, optional):</u> Whether to raise the moment to the power 1 / order, which needs an
order above 0. Defaults to False.
- <u>within_period (bool, optional):</u> Whether to calculate the Partial Moment within the specified period or
for the entire period. Thus whether to look at the Partial Moment within a specific year (if period =
'yearly') or look at the entirety of all years. Defaults to False.
Note that this requires intraday data when period = 'daily', since a
single day only nests observations when intraday data was fetched.
- <u>rolling (int, optional):</u> The rolling window size to use for the calculation. If set, the Partial Moment
is calculated over a rolling window of this many periods across the full return history
instead of per `period`. Defaults to None.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Partial Moment values over time.
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

pd.Series &#124; pd.DataFrame: Partial Moment values, per ticker, or per period (or date) and ticker.

**Notes:**

- The method retrieves historical return data based on the specified `period` and calculates the
Partial Moment for each asset in the Toolkit instance, each on its own returns (a ticker that listed later
or misses a date another ticker traded is measured on the returns it has).
- With growth, the method calculates the growth of the Partial Moment values using the
specified `lag`.
- The lower partial moment of order 1 agrees with PerformanceAnalytics' DownsidePotential and
Riskfolio-Lib's LPM of order 1, order 0 equals DownsideFrequency (UpsideFrequency on the upper side)
and the upper side of order 1 and 2 equals the potential and the variance of UpsideRisk.
- With the mean as the MAR, order 1 and 4 agree with skfolio's first_lower_partial_moment and
fourth_lower_partial_moment. Riskfolio-Lib's LPM of order 2 divides by n - 1 instead of n and
takes the root, and PerformanceAnalytics' lpm divides by the number of returns below the
threshold. Riskfolio-Lib's SemiKurtosis is the square of the root of order 4 around the mean, and
its EvenSemiMoment of p the (order 2p) moment to the power 1 / p.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["JPM", "GS", "MS"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_partial_moment(period="yearly", within_period=True)
```

Which returns:

|      |    JPM |     GS |     MS |   Benchmark |
|:-----|-------:|-------:|-------:|------------:|
| 2021 | 0.0048 | 0.0055 | 0.0057 |      0.0026 |
| 2022 | 0.0074 | 0.0072 | 0.0081 |      0.0063 |
| 2023 | 0.0041 | 0.0053 | 0.0056 |      0.0028 |
| 2024 | 0.0041 | 0.0046 | 0.0048 |      0.0025 |
| 2025 | 0.0048 | 0.0059 | 0.0057 |      0.0034 |

---

## get_central_moment
Calculate a Central Moment: the average deviation of the returns of an investment portfolio or asset from their mean raised to a power, the spread, asymmetry or tails in the returns' own units.

A central moment is the average deviation from the mean return raised to a power, the order. The second central moment is the (population) variance, the third measures the asymmetry of the return distribution in squared-and-cubed return units (negative when the large deviations are losses) and the fourth the weight of the tails. Unlike the Skewness and Kurtosis, which divide by a power of the standard deviation, they keep the scale of the returns, so a volatile asset has larger moments, and they are the building blocks of the moment-based risk measures of portfolio optimization, such as the square-root kurtosis.

The formula is as follows:

$$
\text{Central Moment} = \frac{\sum(\text{Return}_{t} - \text{Mean})^{\text{order}}}{n}
$$

Where Mean is the average return and n the number of returns of the sample (the population moment, without a bias adjustment).

**Also known as:** moment about the mean, third central moment, fourth central moment, square-root kurtosis (its square root for order 4).

**References:**

- library | Referenced against skfolio's [third_central_moment](https://skfolio.org/generated/skfolio.measures.third_central_moment.html){:target="_blank"}
- library | Referenced against skfolio's [fourth_central_moment](https://skfolio.org/generated/skfolio.measures.fourth_central_moment.html){:target="_blank"}
- library | Referenced against Riskfolio-Lib's [Kurtosis](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/risk.html#RiskFunctions.Kurtosis){:target="_blank"}
- library | Shares similar logic as Riskfolio-Lib's [EvenMoment](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/risk.html#RiskFunctions.EvenMoment){:target="_blank"}
- library | Shares similar logic as PerformanceAnalytics (R)'s [centeredmoment](https://github.com/braverock/PerformanceAnalytics/blob/v2.0.4/R/CoMoments.R#L127){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The data frequency for returns. Options are: "daily", "weekly", "monthly",
"quarterly", "yearly". Defaults to "daily".
- <u>order (int, optional):</u> The order of the moment, an integer of 2 or higher. Defaults to 3.
- <u>within_period (bool, optional):</u> Whether to calculate the Central Moment within the specified period or
for the entire period. Thus whether to look at the Central Moment within a specific year (if period =
'yearly') or look at the entirety of all years. Defaults to False.
Note that this requires intraday data when period = 'daily', since a
single day only nests observations when intraday data was fetched.
- <u>rolling (int, optional):</u> The rolling window size to use for the calculation. If set, the Central Moment
is calculated over a rolling window of this many periods across the full return history
instead of per `period`. Defaults to None.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Central Moment values over time.
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

pd.Series &#124; pd.DataFrame: Central Moment values, per ticker, or per period (or date) and ticker.

**Notes:**

- The method retrieves historical return data based on the specified `period` and calculates the
Central Moment for each asset in the Toolkit instance, each on its own returns (a ticker that listed later
or misses a date another ticker traded is measured on the returns it has).
- With growth, the method calculates the growth of the Central Moment values using the
specified `lag`.
- Order 3 and 4 agree with skfolio's third_central_moment and fourth_central_moment and
PerformanceAnalytics' centeredmoment. Riskfolio-Lib's Kurtosis is the square root of order 4 and
its EvenMoment of p the (order 2p) moment to the power 1 / p.
- The moments of daily returns are small numbers (order 4 of a stock is about 1e-7), so use the
rounding parameter to show them.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["XOM", "CVX", "COP"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_central_moment(period="yearly", within_period=True, order=4, rounding=10)
```

Which returns:

|      |       XOM |       CVX |        COP |   Benchmark |
|:-----|----------:|----------:|-----------:|------------:|
| 2021 | 3.194e-07 | 1.706e-07 | 7.526e-07  |   1.61e-08  |
| 2022 | 8.624e-07 | 8.274e-07 | 2.0632e-06 |   1.797e-07 |
| 2023 | 2.417e-07 | 2.375e-07 | 6.268e-07  |   1.29e-08  |
| 2024 | 6.71e-08  | 8.64e-08  | 2.004e-07  |   1.85e-08  |
| 2025 | 2.85e-07  | 5.392e-07 | 1.8409e-06 |   5.877e-07 |

---

## get_worst_realization
Calculate the Worst Realization: the lowest return of an investment portfolio or asset, the loss on the worst day (or week, month) of the sample.

The Worst Realization is the most conservative measure of the risk in the left tail: the loss on the worst day (or week, month) of the sample. It is the limit of the Value at Risk and Conditional Value at Risk as their tail probability goes to 0, and the risk measure of Young's (1998) minimax portfolio, which minimizes the worst loss rather than the variance. As it rests on a single observation it moves in jumps and depends on the length of the sample: a longer history can only add worse days.

The formula is as follows:

$$
\text{Worst Realization} = \min(\text{Return}_{t})
$$

The result is a return, negative for a loss, as the Value at Risk and Conditional Value at Risk of the Toolkit are.

**Also known as:** worst return, minimax risk, maximum loss.

**References:**

- paper | Young, M.R. (1998). "A Minimax Portfolio Selection Rule with Linear Programming Solution." Management Science, 44(5), 673-683.
- library | Referenced against Riskfolio-Lib's [WR](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/risk.html#RiskFunctions.WR){:target="_blank"}
- library | Referenced against skfolio's [worst_realization](https://skfolio.org/generated/skfolio.measures.worst_realization.html){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The data frequency for returns. Options are: "daily", "weekly", "monthly",
"quarterly", "yearly". Defaults to "daily".
- <u>within_period (bool, optional):</u> Whether to calculate the Worst Realization within the specified period or
for the entire period. Thus whether to look at the Worst Realization within a specific year (if period =
'yearly') or look at the entirety of all years. Defaults to False.
Note that this requires intraday data when period = 'daily', since a
single day only nests observations when intraday data was fetched.
- <u>rolling (int, optional):</u> The rolling window size to use for the calculation. If set, the Worst Realization
is calculated over a rolling window of this many periods across the full return history
instead of per `period`. Defaults to None.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Worst Realization values over time.
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

pd.Series &#124; pd.DataFrame: Worst Realization values, per ticker, or per period (or date) and ticker.

**Notes:**

- The method retrieves historical return data based on the specified `period` and calculates the
Worst Realization for each asset in the Toolkit instance, each on its own returns (a ticker that listed later
or misses a date another ticker traded is measured on the returns it has).
- With growth, the method calculates the growth of the Worst Realization values using the
specified `lag`.
- Riskfolio-Lib's WR and skfolio's worst_realization report the loss as a positive number
(-min(Return)); the Toolkit keeps the sign of the return.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["NVDA", "AMD", "INTC"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_worst_realization(period="yearly", within_period=True)
```

Which returns:

|      |    NVDA |     AMD |    INTC |   Benchmark |
|:-----|--------:|--------:|--------:|------------:|
| 2021 | -0.0821 | -0.062  | -0.1168 |     -0.0244 |
| 2022 | -0.0951 | -0.1387 | -0.0856 |     -0.0435 |
| 2023 | -0.0589 | -0.0922 | -0.0641 |     -0.0201 |
| 2024 | -0.1    | -0.1062 | -0.2606 |     -0.0298 |
| 2025 | -0.1697 | -0.089  | -0.115  |     -0.0585 |

---

## get_gini_mean_difference
Calculate the Gini Mean Difference (GMD): how far apart two returns of an investment portfolio or asset lie on average, a measure of dispersion that does not square the deviations.

The Gini Mean Difference is the average absolute difference between two returns drawn from the sample, a measure of dispersion that, unlike the standard deviation, does not square the deviations and needs no mean to measure them from. Yitzhaki (1982) showed that, unlike the variance, it is consistent with second-degree stochastic dominance, which makes it a sound risk measure for returns that are not normally distributed. For a normal distribution it equals $$2 \sigma / \sqrt{\pi}$$, about 1.13 times the standard deviation.

The formula is as follows:

$$
\text{Gini Mean Difference} = \frac{\Sigma_{i} \Sigma_{j} \left|\text{Return}_{i} - \text{Return}_{j}\right|}{n \cdot (n - 1)}
$$

Where the double sum runs over every pair of the n returns. It is calculated as an ordered weighted average (OWA) of the returns sorted from low to high, with weight 2 * (2i - 1 - n) / (n * (n - 1)) on the i-th lowest (Cajas 2021), and equals twice the second L-moment (`get_l_moment`).

**Also known as:** GMD, Gini's mean difference, mean absolute difference.

**References:**

- paper | Yitzhaki, S. (1982). "Stochastic Dominance, Mean Variance, and Gini's Mean Difference." The American Economic Review, 72(1), 178-185.
- paper | Cajas, D. (2021). "OWA Portfolio Optimization: A Disciplined Convex Programming Framework." SSRN Electronic Journal.
- library | Referenced against Riskfolio-Lib's [GMD](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/risk.html#RiskFunctions.GMD){:target="_blank"}
- library | Referenced against skfolio's [gini_mean_difference](https://skfolio.org/generated/skfolio.measures.gini_mean_difference.html){:target="_blank"}
- library | Shares similar logic as Riskfolio-Lib's [owa_gmd](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/auxiliary.html#OwaWeights.owa_gmd){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The data frequency for returns. Options are: "daily", "weekly", "monthly",
"quarterly", "yearly". Defaults to "daily".
- <u>within_period (bool, optional):</u> Whether to calculate the Gini Mean Difference within the specified period or
for the entire period. Thus whether to look at the Gini Mean Difference within a specific year (if period =
'yearly') or look at the entirety of all years. Defaults to False.
Note that this requires intraday data when period = 'daily', since a
single day only nests observations when intraday data was fetched.
- <u>rolling (int, optional):</u> The rolling window size to use for the calculation. If set, the Gini Mean Difference
is calculated over a rolling window of this many periods across the full return history
instead of per `period`. Defaults to None.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Gini Mean Difference values over time.
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

pd.Series &#124; pd.DataFrame: Gini Mean Difference values, per ticker, or per period (or date) and ticker.

**Notes:**

- The method retrieves historical return data based on the specified `period` and calculates the
Gini Mean Difference for each asset in the Toolkit instance, each on its own returns (a ticker that listed later
or misses a date another ticker traded is measured on the returns it has).
- With growth, the method calculates the growth of the Gini Mean Difference values using the
specified `lag`.
- The result agrees with Riskfolio-Lib's GMD and skfolio's gini_mean_difference.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["MCD", "SBUX", "CMG"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_gini_mean_difference(period="yearly", within_period=True)
```

Which returns:

|      |    MCD |   SBUX |    CMG |   Benchmark |
|:-----|-------:|-------:|-------:|------------:|
| 2021 | 0.0104 | 0.0149 | 0.0174 |      0.009  |
| 2022 | 0.0136 | 0.0244 | 0.0274 |      0.0171 |
| 2023 | 0.0098 | 0.0142 | 0.0158 |      0.0093 |
| 2024 | 0.012  | 0.0189 | 0.0194 |      0.0086 |
| 2025 | 0.0126 | 0.022  | 0.0237 |      0.0112 |

---

## get_tail_gini
Calculate the Tail Gini: the loss in the worst tail of the returns of an investment portfolio or asset, weighing the worst returns within that tail most.

The Tail Gini of Furman, Wang and Zitikis (2017) measures the variability within the loss tail, the alpha share of the worst returns. Cajas (2021) writes it as a weighted average of the Conditional Value at Risk at tail probabilities from 0.0001 up to alpha, which puts more weight on the worst returns within the tail than the Conditional Value at Risk at alpha, which weighs every return in the tail equally. It is therefore always at or below the Conditional Value at Risk and above the Worst Realization.

The formula is as follows (with the default alpha of 0.05 and 100 points):

$$
\text{Tail Gini} = \Sigma_{j} c_{j} \cdot \operatorname{CVaR}(\alpha_{j})
$$

$$
c_{1} = \frac{\alpha_{2} \cdot \alpha_{1}}{\alpha^{2}},\;\; c_{j} = \frac{(\alpha_{j+1} - \alpha_{j-1}) \cdot \alpha_{j}}{\alpha^{2}}\;\;\text{and}\;\; c_{m} = \frac{\alpha_{m} - \alpha_{m-1}}{\alpha}
$$

Where $$\alpha_{1} < \ldots < \alpha_{m} = \alpha$$ are m = `points` evenly spaced tail probabilities from 0.0001 to alpha and $$\text{CVaR} (\alpha_{j})$$ is the average of the $$\alpha_{j}$$ share of the lowest returns, the return at the boundary counting with its fraction (the ordered weighted average of Cajas 2021). The result is a return, negative for a loss, as the Conditional Value at Risk of the Toolkit is.

**Also known as:** TG, Gini shortfall, tail Gini risk.

**References:**

- paper | Furman, E., Wang, R. and Zitikis, R. (2017). "Gini-type Measures of Risk and Variability: Gini Shortfall, Capital Allocations, and Heavy-tailed Risks." Journal of Banking & Finance, 83, 70-84.
- paper | Cajas, D. (2021). "OWA Portfolio Optimization: A Disciplined Convex Programming Framework." SSRN Electronic Journal.
- library | Referenced against Riskfolio-Lib's [TG](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/risk.html#RiskFunctions.TG){:target="_blank"}
- library | Shares similar logic as Riskfolio-Lib's [owa_tg](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/auxiliary.html#OwaWeights.owa_tg){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The data frequency for returns. Options are: "daily", "weekly", "monthly",
"quarterly", "yearly". Defaults to "daily".
- <u>alpha (float, optional):</u> The tail probability, between 0.0001 and 1. Defaults to 0.05.
- <u>points (int, optional):</u> The number of tail probabilities the Conditional Value at Risk
is averaged over. Defaults to 100.
- <u>within_period (bool, optional):</u> Whether to calculate the Tail Gini within the specified period or
for the entire period. Thus whether to look at the Tail Gini within a specific year (if period =
'yearly') or look at the entirety of all years. Defaults to False.
Note that this requires intraday data when period = 'daily', since a
single day only nests observations when intraday data was fetched.
- <u>rolling (int, optional):</u> The rolling window size to use for the calculation. If set, the Tail Gini
is calculated over a rolling window of this many periods across the full return history
instead of per `period`. Defaults to None.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Tail Gini values over time.
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

pd.Series &#124; pd.DataFrame: Tail Gini values, per ticker, or per period (or date) and ticker.

**Notes:**

- The method retrieves historical return data based on the specified `period` and calculates the
Tail Gini for each asset in the Toolkit instance, each on its own returns (a ticker that listed later
or misses a date another ticker traded is measured on the returns it has).
- With growth, the method calculates the growth of the Tail Gini values using the
specified `lag`.
- The result agrees with Riskfolio-Lib's TG with the opposite sign: Riskfolio-Lib reports the loss as
a positive number. Its Conditional Value at Risk is the exact one of Rockafellar and Uryasev
(2002), which can differ slightly from the average of the returns below the interpolated quantile
that `get_conditional_value_at_risk` takes.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["TSLA", "F", "GM"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_tail_gini(period="yearly", within_period=True)
```

Which returns:

|      |    TSLA |       F |      GM |   Benchmark |
|:-----|--------:|--------:|--------:|------------:|
| 2021 | -0.0785 | -0.0558 | -0.056  |     -0.0207 |
| 2022 | -0.1    | -0.0823 | -0.0642 |     -0.0365 |
| 2023 | -0.0832 | -0.0642 | -0.0462 |     -0.0168 |
| 2024 | -0.0902 | -0.0719 | -0.0542 |     -0.0218 |
| 2025 | -0.099  | -0.0526 | -0.0582 |     -0.0348 |

---

## get_risk_range
Calculate a Range measure: how far the gain tail of the returns of an investment portfolio or asset lies from its loss tail.

The Range is the distance between the best and the worst return. Cajas (2021) generalizes it to the tails: the VaR Range is the distance between the 1 - beta and the alpha quantile, the CVaR Range between the average return in the best beta share and in the worst alpha share of the returns and the Tail Gini Range between the Tail Gini of the gains and of the losses. They measure the width of the distribution where it matters most, without the assumption of symmetry behind the standard deviation, and with beta different from alpha they weigh the gains and the losses differently. The VaR Range at $$\alpha = \beta = 0.25$$ is the interquartile range. The EVaR Range does the same with the historic Entropic Value at Risk, the most severe of these tail measures.

The formula is as follows:

$$
\text{Range} = \max(\text{Return}) - \min(\text{Return})
$$

$$
\text{VaR Range} = \operatorname{Quantile}(\text{Return},\; 1 - \beta) - \operatorname{Quantile}(\text{Return},\; \alpha)
$$

$$
\text{CVaR Range} = \operatorname{mean}(\text{Return} \geq \operatorname{Quantile}(\text{Return},\; 1 - \beta)) - \operatorname{mean}(\text{Return} \leq \operatorname{Quantile}(\text{Return},\; \alpha))
$$

$$
\text{Tail Gini Range} = \text{Tail Gini of the gains} \;(\beta) - \text{Tail Gini of the losses} \;(\alpha)
$$

$$
\text{EVaR Range} = \text{EVaR of the gains} \;(\beta) - \text{EVaR of the losses} \;(\alpha)
$$

Where the quantiles are interpolated linearly and the CVaR is the average of the returns beyond the quantile, as in the historic `get_value_at_risk` and `get_conditional_value_at_risk`, the Tail Gini is that of `get_tail_gini` and the EVaR the historic one of `get_entropic_value_at_risk`, each measured on the negated returns for the gains. The result is a positive decimal.

**Also known as:** return range, VaR range, CVaR range, Tail Gini range, EVaR range, tail spread.

**References:**

- paper | Cajas, D. (2021). "OWA Portfolio Optimization: A Disciplined Convex Programming Framework." SSRN Electronic Journal.
- library | Referenced against Riskfolio-Lib's [RG](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/risk.html#RiskFunctions.RG){:target="_blank"} (Range)
- library | Referenced against Riskfolio-Lib's [TGRG](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/risk.html#RiskFunctions.TGRG){:target="_blank"} (Tail Gini Range)
- library | Referenced against Riskfolio-Lib's [EVRG](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/risk.html#RiskFunctions.EVRG){:target="_blank"} (EVaR Range)
- library | Shares similar logic as Riskfolio-Lib's [VRG](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/risk.html#RiskFunctions.VRG){:target="_blank"} (VaR Range)
- library | Shares similar logic as Riskfolio-Lib's [CVRG](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/risk.html#RiskFunctions.CVRG){:target="_blank"} (CVaR Range)

**Args:**

- <u>period (str, optional):</u> The data frequency for returns. Options are: "daily", "weekly", "monthly",
"quarterly", "yearly". Defaults to "daily".
- <u>measure (str, optional):</u> The range to calculate. Options are: "range" (Range), "var" (VaR
Range), "cvar" (CVaR Range), "tail_gini" (Tail Gini Range), "evar" (EVaR Range). Defaults to
"range".
- <u>alpha (float, optional):</u> The tail probability of the losses, between 0 and 1 (between 0.0001
and 1 for the Tail Gini). Defaults to 0.05.
- <u>beta (float &#124; None, optional):</u> The tail probability of the gains. Defaults to None, which uses
alpha.
- <u>points (int, optional):</u> The number of tail probabilities of the Tail Gini Range.
Defaults to 100.
- <u>within_period (bool, optional):</u> Whether to calculate the Risk Range within the specified period or
for the entire period. Thus whether to look at the Risk Range within a specific year (if period =
'yearly') or look at the entirety of all years. Defaults to False.
Note that this requires intraday data when period = 'daily', since a
single day only nests observations when intraday data was fetched.
- <u>rolling (int, optional):</u> The rolling window size to use for the calculation. If set, the Risk Range
is calculated over a rolling window of this many periods across the full return history
instead of per `period`. Defaults to None.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Risk Range values over time.
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

pd.Series &#124; pd.DataFrame: Range values, per ticker, or per period (or date) and ticker.

**Notes:**

- The method retrieves historical return data based on the specified `period` and calculates the
Risk Range for each asset in the Toolkit instance, each on its own returns (a ticker that listed later
or misses a date another ticker traded is measured on the returns it has).
- With growth, the method calculates the growth of the Risk Range values using the
specified `lag`.
- The Range, the Tail Gini Range and the EVaR Range agree with Riskfolio-Lib's RG, TGRG and EVRG.
Riskfolio-Lib's VRG and CVRG take the order statistic at ceil(alpha * n) instead of the interpolated quantile and the exact
Conditional Value at Risk of Rockafellar and Uryasev (2002), so the VaR Range and CVaR Range differ
slightly from them and equal the difference of the Toolkit's own historic Value at Risk and
Conditional Value at Risk of the gains and the losses instead.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AMZN", "WMT", "COST"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_risk_range(period="yearly", within_period=True, measure="cvar")
```

Which returns:

|      |   AMZN |    WMT |   COST |   Benchmark |
|:-----|-------:|-------:|-------:|------------:|
| 2021 | 0.065  | 0.0457 | 0.05   |      0.0352 |
| 2022 | 0.1352 | 0.0736 | 0.0879 |      0.0634 |
| 2023 | 0.0913 | 0.0393 | 0.0523 |      0.0332 |
| 2024 | 0.0772 | 0.0485 | 0.0499 |      0.0352 |
| 2025 | 0.0975 | 0.0728 | 0.0631 |      0.0538 |

---

## get_l_moment
Calculate an L-moment, or an L-moment ratio: the location, spread, asymmetry or tails of the returns of an investment portfolio or asset, robust to a few extreme returns.

L-moments (Hosking 1990) describe the location, scale and shape of a distribution as the ordinary moments do, but as linear combinations of the sorted returns rather than powers of the deviations. This makes them far less sensitive to a few extreme returns and well defined whenever the mean is: the L-skewness and L-kurtosis of a sample are bounded and nearly unbiased, where the sample skewness and kurtosis of fat-tailed returns are dominated by the largest move. The first L-moment is the mean, the second a measure of scale (half the Gini Mean Difference), and the ratios of the third and fourth to the second, the L-skewness and L-kurtosis, measure the asymmetry and the tails. For a normal distribution the L-skewness is 0 and the L-kurtosis 0.1226.

The formula is as follows:

$$
\text{L-moment}\; \lambda_{k} = \Sigma_{i} w_{i} \cdot \text{Return}_{i}
$$

$$
w_{i} = \frac{\Sigma_{j} (- 1)^{j} \cdot C(k - 1,\; j) \cdot C(i - 1,\; k - 1 - j) \cdot C(n - i,\; j)}{k \cdot C(n,\; k)}
$$

$$
\text{L-moment ratio}\; \tau_{k} = \frac{\lambda_{k}}{\lambda_{2}} \;\text{for}\; k \geq 3\;\;\text{and}\;\; \tau_{2} = \frac{\lambda_{2}}{\lambda_{1}} \;(\text{the L-CV})
$$

Where Return_(i) is the i-th lowest of the n returns, k the order, C the binomial coefficient and j runs from 0 to k - 1. These are Hosking's unbiased sample L-moments, written as an ordered weighted average as in Cajas (2021).

**Also known as:** L-moments, L-scale, L-skewness, L-kurtosis, L-CV, linear moments.

**References:**

- paper | Hosking, J.R.M. (1990). "L-moments: Analysis and Estimation of Distributions using Linear Combinations of Order Statistics." Journal of the Royal Statistical Society: Series B, 52(1), 105-124.
- paper | Cajas, D. (2021). "OWA Portfolio Optimization: A Disciplined Convex Programming Framework." SSRN Electronic Journal.
- library | Referenced against Riskfolio-Lib's [L_Moment](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/risk.html#RiskFunctions.L_Moment){:target="_blank"}
- library | Referenced against scipy's [lmoment](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.lmoment.html){:target="_blank"}
- library | Shares similar logic as Riskfolio-Lib's [owa_l_moment](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/auxiliary.html#OwaWeights.owa_l_moment){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The data frequency for returns. Options are: "daily", "weekly", "monthly",
"quarterly", "yearly". Defaults to "daily".
- <u>order (int, optional):</u> The order k, an integer of 1 or higher (1 is the mean, 2 the L-scale,
3 with ratio=True the L-skewness and 4 the L-kurtosis). Defaults to 2.
- <u>ratio (bool, optional):</u> Whether to return the L-moment ratio, which needs an order of 2 or
higher. Defaults to False.
- <u>within_period (bool, optional):</u> Whether to calculate the L-moment within the specified period or
for the entire period. Thus whether to look at the L-moment within a specific year (if period =
'yearly') or look at the entirety of all years. Defaults to False.
Note that this requires intraday data when period = 'daily', since a
single day only nests observations when intraday data was fetched.
- <u>rolling (int, optional):</u> The rolling window size to use for the calculation. If set, the L-moment
is calculated over a rolling window of this many periods across the full return history
instead of per `period`. Defaults to None.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the L-moment values over time.
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

pd.Series &#124; pd.DataFrame: L-moment values, per ticker, or per period (or date) and ticker.

**Notes:**

- The method retrieves historical return data based on the specified `period` and calculates the
L-moment for each asset in the Toolkit instance, each on its own returns (a ticker that listed later
or misses a date another ticker traded is measured on the returns it has).
- With growth, the method calculates the growth of the L-moment values using the
specified `lag`.
- The L-moments agree with Riskfolio-Lib's L_Moment and scipy's lmoment, and the ratios with the
standardized L-moments of scipy's lmoment.
- A sample needs at least `order` returns, fewer give NaN.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["PFE", "MRK", "JNJ"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_l_moment(period="yearly", within_period=True, order=3, ratio=True)
```

Which returns:

|      |     PFE |     MRK |     JNJ |   Benchmark |
|:-----|--------:|--------:|--------:|------------:|
| 2021 |  0.1252 | -0.0172 | -0.0248 |     -0.0386 |
| 2022 |  0.0344 |  0.0321 |  0.0518 |      0.0138 |
| 2023 | -0.0124 | -0.0261 | -0.0389 |     -0.0039 |
| 2024 |  0.0588 | -0.0149 |  0.0183 |     -0.0586 |
| 2025 | -0.0016 | -0.0154 | -0.0189 |     -0.0597 |

---

## get_l_moment_risk_measure
Calculate the L-moment Convex Risk Measure: one risk figure for the spread, skew and tails of the returns of an investment portfolio or asset, robust to outliers.

Cajas (2023) combines the L-moments of order 2 up to `order` into one convex risk measure: a weighted sum of the L-scale, minus the L-moment of order 3 (so a negative skew adds risk), plus that of order 4 and so on, with weights that are non-negative, sum to 1 and decrease with the order. The weights are chosen so that the ordered weighted average they imply puts at least as much weight on every worse return, which keeps the measure convex and therefore usable in portfolio optimization. It captures the dispersion, the skew and the tails of the returns in one figure that is as robust to outliers as the L-moments themselves.

The formula is as follows:

$$
\text{L-moment Convex Risk Measure} = \Sigma_{k} \phi_{k} \cdot (- 1)^{k} \cdot \lambda_{k} \;\text{for}\; k = 2,\; \ldots,\; \text{order}
$$

$$
\sum \phi_{k} = 1,\; 0 \leq \phi_{k} \leq \text{max\_weight} \;\text{and}\; \phi_{k} \geq \phi_{k+1}
$$

Where $$\lambda_{k}$$ is the L-moment of order k (`get_l_moment`) and the $$\phi_{k}$$ follow from the method: the minimum squared differences method minimizes the squared differences between the neighbouring weights of the ordered weighted average, the minimum sum of squares method the sum of its squared weights and the constant relative risk aversion method sets $$\phi_{k}$$ in proportion to $$\Pi_{i = 1 \ldots k - 1}$$ (risk_aversion + i - 1) / k!, after which the ordered weights are made non-decreasing. The result is a positive decimal.

**Also known as:** L-moment CRM, L-moment based convex risk measure.

**References:**

- paper | Cajas, D. (2023). "Higher Order Moment Portfolio Optimization with L-Moments." SSRN 4393155.
- paper | Hosking, J.R.M. (1990). "L-moments: Analysis and Estimation of Distributions using Linear Combinations of Order Statistics." Journal of the Royal Statistical Society: Series B, 52(1), 105-124.
- library | Referenced against Riskfolio-Lib's [L_Moment_CRM](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/risk.html#RiskFunctions.L_Moment_CRM){:target="_blank"} (constant relative risk aversion)
- library | Shares similar logic as Riskfolio-Lib's [owa_l_moment_crm](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/auxiliary.html#OwaWeights.owa_l_moment_crm){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The data frequency for returns. Options are: "daily", "weekly", "monthly",
"quarterly", "yearly". Defaults to "daily".
- <u>order (int, optional):</u> The highest L-moment order, an integer of 2 or higher. Defaults to 4.
- <u>method (str, optional):</u> How the L-moments are weighted. Options are: "msd" (minimum squared
differences), "mss" (minimum sum of squares), "crra" (constant relative risk aversion).
Defaults to "msd".
- <u>risk_aversion (float, optional):</u> The risk aversion of the constant relative risk aversion
method, between 0 and 1. Defaults to 0.5.
- <u>max_weight (float, optional):</u> The largest weight of one L-moment for "msd" and "mss", between
0 and 1. Defaults to 0.5.
- <u>within_period (bool, optional):</u> Whether to calculate the L-moment Convex Risk Measure within the specified
period or for the entire period. Thus whether to look at the L-moment Convex Risk Measure within a specific
year (if period = 'yearly') or look at the entirety of all years. Defaults to False.
Note that this requires intraday data when period = 'daily', since a
single day only nests observations when intraday data was fetched.
- <u>rolling (int, optional):</u> The rolling window size to use for the calculation. If set, the
L-moment Convex Risk Measure is calculated over a rolling window of this many periods across the full return
history instead of per `period`. Defaults to None.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the L-moment Convex Risk Measure values over time.
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

pd.Series &#124; pd.DataFrame: L-moment Convex Risk Measure values, per ticker, or per period (or date) and ticker.

**Notes:**

- The method retrieves historical return data based on the specified `period` and calculates the
L-moment Convex Risk Measure for each asset in the Toolkit instance, each on its own returns (a ticker that
listed later or misses a date another ticker traded is measured on the returns it has).
- With growth, the method calculates the growth of the L-moment Convex Risk Measure values using
the specified `lag`.
- With constant relative risk aversion the result agrees with Riskfolio-Lib's L_Moment_CRM. For the
minimum squared differences and minimum sum of squares methods the weights
solve a small convex program over the order - 1 weights with scipy (SLSQP) where Riskfolio-Lib uses
cvxpy with the Clarabel solver; the Toolkit's weights meet the constraints exactly and match a
tightly solved cvxpy program, while Clarabel's default tolerances leave Riskfolio-Lib's weights
slightly off, so the results differ in the fourth significant digit for the minimum squared
differences and the second for the minimum sum of squares. Riskfolio-Lib's maximum entropy method is
left out: the entropy it maximizes is
that of a bound which is the same for every set of weights, so its result depends on the solver.
- With an order of 3 and a maximum weight of 0.5 no weights meet the constraints, which gives an error.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["V", "MA", "PYPL"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_l_moment_risk_measure(period="yearly", within_period=True)
```

Which returns:

|      |      V |     MA |   PYPL |   Benchmark |
|:-----|-------:|-------:|-------:|------------:|
| 2021 | 0.0044 | 0.0052 | 0.0068 |      0.0024 |
| 2022 | 0.0054 | 0.0058 | 0.0098 |      0.0044 |
| 2023 | 0.0028 | 0.0031 | 0.0067 |      0.0024 |
| 2024 | 0.0031 | 0.0029 | 0.0061 |      0.0024 |
| 2025 | 0.0039 | 0.004  | 0.0069 |      0.0032 |

---

## get_skewness_kurtosis_ratio
Calculate the Skewness-Kurtosis Ratio: how lopsided the returns of an investment portfolio or asset are relative to how heavy their tails are, higher being better.

The Skewness-Kurtosis Ratio (Bacon 2008) divides the skewness by the kurtosis, combining the two shape statistics an investor in fat-tailed assets cares about into one number: a positive skew is attractive and fat tails are not, so a higher ratio is better. It is used to rank funds whose returns are far from normal, where the Sharpe Ratio's reliance on the standard deviation misleads.

The formula is as follows:

$$
\text{Skewness-Kurtosis Ratio} = \frac{\text{Skewness}}{\text{Kurtosis}}
$$

Where the Skewness is that of `get_skewness` and the Kurtosis that of `get_kurtosis`, Pearson's kurtosis (3 for a normal distribution), both the bias-adjusted sample estimates.

**Also known as:** skewness to kurtosis ratio.

**References:**

- paper | Bacon, C.R. (2008). "Practical Portfolio Performance Measurement and Attribution." John Wiley & Sons, chapter 4.
- library | Shares similar logic as PerformanceAnalytics (R)'s [SkewnessKurtosisRatio](https://github.com/braverock/PerformanceAnalytics/blob/v2.0.4/R/SkewnessKurtosisRatio.R#L31){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The data frequency for returns. Options are: "daily", "weekly", "monthly",
"quarterly", "yearly". Defaults to "daily".
- <u>within_period (bool, optional):</u> Whether to calculate the Skewness-Kurtosis Ratio within the specified
period or for the entire period. Thus whether to look at the Skewness-Kurtosis Ratio within a specific
year (if period = 'yearly') or look at the entirety of all years. Defaults to False.
Note that this requires intraday data when period = 'daily', since a
single day only nests observations when intraday data was fetched.
- <u>rolling (int, optional):</u> The rolling window size to use for the calculation. If set, the
Skewness-Kurtosis Ratio is calculated over a rolling window of this many periods across the full return
history instead of per `period`. Defaults to None.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Skewness-Kurtosis Ratio values over time.
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

pd.Series &#124; pd.DataFrame: Skewness-Kurtosis Ratio values, per ticker, or per period (or date) and ticker.

**Notes:**

- The method retrieves historical return data based on the specified `period` and calculates the
Skewness-Kurtosis Ratio for each asset in the Toolkit instance, each on its own returns (a ticker that
listed later or misses a date another ticker traded is measured on the returns it has).
- With growth, the method calculates the growth of the Skewness-Kurtosis Ratio values using
the specified `lag`.
- PerformanceAnalytics' SkewnessKurtosisRatio divides the population (moment) skewness by the
population kurtosis; the Toolkit uses its bias-adjusted sample estimates of both, as in
`get_skewness` and `get_kurtosis`, which differ by about 0.4% of the ratio for three years of daily
returns and more for short samples.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["META", "GOOGL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_skewness_kurtosis_ratio(period="yearly", within_period=True)
```

Which returns:

|      |    META |   GOOGL |    MSFT |   Benchmark |
|:-----|--------:|--------:|--------:|------------:|
| 2021 |  0.0058 |  0.0708 | -0.0057 |     -0.0897 |
| 2022 | -0.0997 |  0.0468 |  0.038  |      0.0132 |
| 2023 |  0.1119 | -0.0405 |  0.0846 |     -0.007  |
| 2024 |  0.0804 |  0.0277 | -0.1715 |     -0.1095 |
| 2025 |  0.0563 |  0.0465 |  0.1    |      0.0567 |

---

## get_conditional_drawdown_at_risk
Calculate the Conditional Drawdown at Risk (CDaR) of an investment portfolio or asset's returns: the average of the deepest drawdowns, those beyond the Drawdown at Risk.

Conditional Drawdown at Risk (CDaR) extends the concept of Value at Risk and Conditional Value at Risk to the drawdown series instead of the return series. It is calculated as the average of the worst drawdowns that exceed the Drawdown at Risk (DaR), i.e. the alpha-quantile of the drawdown distribution, giving insight into the depth of the most severe drawdowns an investment portfolio or asset could experience.

The formula is as follows (with the default alpha of 0.05):

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

Every period counts towards the drawdown distribution, including those at a high (a drawdown of 0), the quantile interpolates linearly, and Wealth starts at 1, so a decline from the start of the window counts. Without compounding the drawdowns are measured on the summed returns instead, as an absolute decline from their peak (Drawdown(t) = Sum(t) - max(0, max(Sum(s) for s <= t)), with Sum(t) = Σ Return(s)), the uncompounded drawdown of Chekhlov, Uryasev and Zabarankin (2005).

**Also known as:** CDaR, uncompounded CDaR, absolute CDaR.

**References:**

- paper | Chekhlov, A., Uryasev, S. and Zabarankin, M. (2005). "Drawdown Measure in Portfolio Optimization." International Journal of Theoretical and Applied Finance, 8(1), 13-58.
- library | Shares similar logic as Riskfolio-Lib's [CDaR_Rel](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/risk.html#RiskFunctions.CDaR_Rel){:target="_blank"} (compounded)
- library | Shares similar logic as Riskfolio-Lib's [CDaR_Abs](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/risk.html#RiskFunctions.CDaR_Abs){:target="_blank"} (uncompounded)
- library | Shares similar logic as skfolio's [cdar](https://skfolio.org/generated/skfolio.measures.cdar.html){:target="_blank"}
- library | Shares similar logic as PerformanceAnalytics (R)'s [CDD](https://github.com/braverock/PerformanceAnalytics/blob/v2.0.4/R/maxDrawdown.R#L106){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The data frequency for returns. Options are: "daily", "weekly", "monthly",
"quarterly", "yearly". Defaults to "daily".
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
- <u>compound_returns (bool, optional):</u> Whether to compound the returns into the wealth path the drawdowns are
measured on, or to sum them (absolute drawdowns). Defaults to True.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series: CDaR values with time as the index.

**Notes:**

- The method retrieves historical return data based on the specified `period` and calculates CDaR for each
asset in the Toolkit instance.
- With growth, the method calculates the growth of CDaR values using the specified `lag`.
- Riskfolio-Lib's CDaR_Rel and CDaR_Abs and skfolio's cdar take the exact tail average of Rockafellar and
Uryasev (2002), which counts the drawdown at the boundary with a fraction, and report the loss as a
positive number; the Toolkit averages the drawdowns up to the interpolated quantile, as its historic
CVaR does, which differs from them by up to 2e-4 on three years of daily returns.

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

## get_conditional_expected_drawdown
Calculate the Conditional Expected Drawdown (CED) of an investment portfolio or asset's returns: the average of the worst Maximum Drawdowns over paths of a fixed length.

The Maximum Drawdown of the whole history is a single number that depends on how long the history is. Goldberg and Mahmoud (2017) fix the length instead: the Maximum Drawdown of every path of `window` returns forms a distribution, and the CED is the tail average of it, as the CVaR is of the returns. With a window of 21 daily returns it reads as how deep the decline within a bad month gets, on average over the worst 5% of months. Where the Conditional Drawdown at Risk averages the drawdown of single days, the CED averages the worst decline of whole paths, and unlike the Maximum Drawdown it is a tail average, so a single crash moves it less and it does not grow with the length of the data.

The formula is as follows (with the default window of 21 and alpha of 0.05):

$$
\operatorname{Wealth}(t) = \prod(1 + \operatorname{Return}(s)) \;\text{for}\; s \leq t,\;\; \text{starting at 1 before the first return of each path}
$$

$$
\text{Maximum Drawdown}(s) = \min \;\text{over}\; t \;\text{in} \;\left[s,\; s + \frac{\text{window)} \;\text{of Wealth}(t)}{\max(1,\; \max(\operatorname{Wealth}(u) \;\text{for}\; u \leq t))} - 1\right]
$$

$$
\text{CED} = \frac{\sum_{i <= k} \;\operatorname{MDD}(i) + (m \cdot \alpha - k) \cdot \operatorname{MDD}(k + 1)}{m \cdot \alpha}
$$

Where MDD(1) <= MDD(2) <= ... are the m Maximum Drawdowns in ascending order and k = floor(m · alpha). The paths overlap, one starting at every return, so n returns give $$m = n$$ - window + 1 paths. The tail average is the exact one of Rockafellar and Uryasev (2002), the average of the deepest m · alpha paths with the one at the boundary counted with its fraction. Overlapping paths often share their Maximum Drawdown, so a cut at an interpolated quantile, as the Toolkit's CDaR and historic CVaR make, would take or leave such ties on the last digit of the rounding. Without compounding the drawdowns are measured on the summed returns instead, as an absolute decline from their peak.

**Also known as:** CED, conditional expected drawdown, expected maximum drawdown in the tail.

**References:**

- paper | Goldberg, L.R. and Mahmoud, O. (2017). "Drawdown: From Practice to Theory and Back Again." Mathematics and Financial Economics, 11(3), 275-297.
- library | Shares similar logic as RiskLabAI's [conditional_expected_drawdown](https://github.com/RiskLabAI/RiskLabAI.py/blob/v3.2.0/RiskLabAI/backtest/robust_statistics.py#L88){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The data frequency for returns. Options are: "daily", "weekly", "monthly",
"quarterly", "yearly". Defaults to "daily".
- <u>window (int, optional):</u> The length of each path in returns of `period`. Defaults to 21, a month of
trading days.
- <u>alpha (float, optional):</u> The tail probability for the CED calculation (e.g., 0.05 for the worst 5% of
paths). Defaults to 0.05.
- <u>within_period (bool, optional):</u> Whether to calculate the CED within the specified period or for the
entire period. Thus whether to look at the CED within a specific year (if period = 'yearly') or look at
the entirety of all years. Defaults to False. Note that this requires intraday data when period =
'daily', since a single day only nests observations when intraday data was fetched.
- <u>rolling (int, optional):</u> The rolling window size to use for the calculation. If set, the CED is
calculated over a rolling window of this many periods across the full return history instead
of per `period`; it needs to be at least `window`. Defaults to None.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the CED values over time. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>compound_returns (bool, optional):</u> Whether to compound the returns into the wealth path the drawdowns are
measured on, or to sum them (absolute drawdowns). Defaults to True.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series &#124; pd.DataFrame: CED values, negative (0 without a decline), per ticker, or per period (or
date) and ticker.

**Notes:**

- The method retrieves historical return data based on the specified `period` and calculates the CED
for each asset in the Toolkit instance, each on its own returns. A period with fewer than `window`
returns has no path and gives NaN.
- RiskLabAI's conditional_expected_drawdown takes alpha as the confidence level (0.90 for the worst 10%)
and reports the drawdown as a positive number; the Toolkit takes the tail probability, as for the
CDaR, and keeps the sign of a return.
- With fewer than 1 / alpha paths the tail holds less than one path and the CED is the deepest
Maximum Drawdown of any path.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["^STOXX50E", "^N225", "^GSPC"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_conditional_expected_drawdown(period="yearly", within_period=True)
```

Which returns:

|      |   ^STOXX50E |   ^N225 |   ^GSPC |   Benchmark |
|:-----|------------:|--------:|--------:|------------:|
| 2021 |     -0.0769 | -0.1009 | -0.0464 |     -0.0454 |
| 2022 |     -0.1575 | -0.1059 | -0.1269 |     -0.1263 |
| 2023 |     -0.0646 | -0.0886 | -0.066  |     -0.0651 |
| 2024 |     -0.0844 | -0.242  | -0.0799 |     -0.0792 |
| 2025 |     -0.1587 | -0.1812 | -0.1374 |     -0.1372 |

---

## get_drawdown_at_risk
Calculate the Drawdown at Risk (DaR) of an investment portfolio or asset's returns: how deep below its high the asset is in all but the worst alpha share of the periods.

The Drawdown at Risk is the Value at Risk of the drawdown series: the depth below the running peak that the asset was at or beyond in only an alpha share of the periods (5% for the default alpha). Where the Maximum Drawdown rests on the single worst moment of the sample, the DaR describes how deep the drawdowns usually get in bad times, and the Conditional Drawdown at Risk (`get_conditional_drawdown_at_risk`) averages the drawdowns beyond it. Chekhlov, Uryasev and Zabarankin (2005) introduced it as a constraint for portfolio optimization: a fund manager whose clients leave after a deep drawdown cares about how often the portfolio is far below its high, not only about its volatility.

The formula is as follows (with the default alpha of 0.05):

$$
\operatorname{Wealth}(t) = \prod(1 + \operatorname{Return}(s)) \;\text{for}\; s \leq t
$$

$$
\operatorname{Drawdown}(t) = \frac{\operatorname{Wealth}(t)}{\max(1,\; \max(\operatorname{Wealth}(s) \;\text{for}\; s \leq t))} - 1
$$

$$
\text{DaR} = \operatorname{Quantile}(\text{Drawdown},\; \alpha)
$$

Every period counts towards the drawdown distribution, including those at a high (a drawdown of 0), the quantile interpolates linearly, and Wealth starts at 1, so a decline from the start of the window counts. Without compounding the drawdowns are measured on the summed returns instead, as an absolute decline from their peak (Drawdown(t) = Sum(t) - max(0, max(Sum(s) for s <= t)), with Sum(t) = Σ Return(s)). The result is a negative decimal (0 when the asset was at a high in more than 1 - alpha of the periods).

**Also known as:** DaR, drawdown quantile, uncompounded DaR, absolute DaR.

**References:**

- paper | Chekhlov, A., Uryasev, S. and Zabarankin, M. (2005). "Drawdown Measure in Portfolio Optimization." International Journal of Theoretical and Applied Finance, 8(1), 13-58.
- library | Shares similar logic as Riskfolio-Lib's [DaR_Rel](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/risk.html#RiskFunctions.DaR_Rel){:target="_blank"} (compounded)
- library | Shares similar logic as Riskfolio-Lib's [DaR_Abs](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/risk.html#RiskFunctions.DaR_Abs){:target="_blank"} (uncompounded)
- library | Shares similar logic as skfolio's [drawdown_at_risk](https://skfolio.org/generated/skfolio.measures.drawdown_at_risk.html){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The data frequency for returns. Options are: "daily", "weekly", "monthly",
"quarterly", "yearly". Defaults to "daily".
- <u>alpha (float, optional):</u> The tail probability for the DaR calculation (e.g., 0.05 for the 95%
confidence level). Defaults to 0.05.
- <u>compound_returns (bool, optional):</u> Whether to compound the returns into the wealth path the drawdowns are
measured on, or to sum them (absolute drawdowns). Defaults to True.
- <u>within_period (bool, optional):</u> Whether to calculate the DaR within the specified period or for the
entire period. Thus whether to look at the DaR within a specific year (if period = 'yearly') or look at
the entirety of all years. Defaults to False. Note that this requires intraday data when period =
'daily', since a single day only nests observations when intraday data was fetched.
- <u>rolling (int, optional):</u> The rolling window size to use for the calculation. If set, the DaR is
calculated over a rolling window of this many periods across the full return history instead
of per `period`, every window starting from a wealth of 1. Defaults to None.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the DaR values over time. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series &#124; pd.DataFrame: DaR values, per ticker, or per period (or date) and ticker.

**Notes:**

- The method retrieves historical return data based on the specified `period` and calculates the DaR
for each asset in the Toolkit instance, each on its own returns.
- With growth, the method calculates the growth of DaR values using the specified `lag`.
- Riskfolio-Lib's $$\text{DaR}_{\text{Rel}}$$ and $$\text{DaR}_{\text{Abs}}$$ and skfolio's drawdown_at_risk take the order statistic at
ceil(alpha * n) of the sorted drawdowns instead of the interpolated quantile and report the drawdown
as a positive number; on three years of daily returns they differ by up to 1e-3.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["^STOXX50E", "^N225", "^GSPC"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_drawdown_at_risk(period="yearly", within_period=True)
```

Which returns:

|      |   ^STOXX50E |   ^N225 |   ^GSPC |   Benchmark |
|:-----|------------:|--------:|--------:|------------:|
| 2021 |     -0.0527 | -0.0947 | -0.0385 |     -0.0375 |
| 2022 |     -0.2303 | -0.1148 | -0.2335 |     -0.2244 |
| 2023 |     -0.0821 | -0.0687 | -0.0715 |     -0.0693 |
| 2024 |     -0.07   | -0.1379 | -0.0445 |     -0.0433 |
| 2025 |     -0.077  | -0.1335 | -0.1164 |     -0.1122 |

---

## get_entropic_drawdown_at_risk
Calculate the Entropic Drawdown at Risk (EDaR) of an investment portfolio or asset's returns: the tightest entropic bound on the deep drawdowns, between the CDaR and the Maximum Drawdown.

The Entropic Drawdown at Risk is the historic Entropic Value at Risk (the historic method of `get_entropic_value_at_risk`) of the drawdown series: the tightest bound on the drawdowns that follows from the Chernoff inequality. It is at least as severe as the Drawdown at Risk and the Conditional Drawdown at Risk at the same alpha and at most as severe as the Maximum Drawdown, and as a coherent risk measure it is the drawdown counterpart of the EVaR in Cajas' (2021) entropic portfolio optimization. It weighs the deepest drawdowns more than the CDaR does, without resting on the single worst moment as the Maximum Drawdown does.

The formula is as follows (with the default alpha of 0.05):

$$
\operatorname{Wealth}(t) = \prod(1 + \operatorname{Return}(s)) \;\text{for}\; s \leq t
$$

$$
\operatorname{Drawdown}(t) = \frac{\operatorname{Wealth}(t)}{\max(1,\; \max(\operatorname{Wealth}(s) \;\text{for}\; s \leq t))} - 1
$$

$$
\text{EDaR} = - \text{inf over}\; z > 0 \;\text{of}\; z \cdot \ln\left(\frac{\operatorname{mean}\left(\exp\left(- \frac{\operatorname{Drawdown}(t)}{z}\right)\right)}{\alpha}\right)
$$

Every period counts towards the drawdown distribution, including those at a high (a drawdown of 0), and Wealth starts at 1, so a decline from the start of the window counts. The bound is minimized over the risk aversion z numerically (on the logarithm of 1 / z, with scipy's brentq). Without compounding the drawdowns are measured on the summed returns instead, as an absolute decline from their peak (Drawdown(t) = Sum(t) - max(0, max(Sum(s) for s <= t)), with Sum(t) = Σ Return(s)). The result is a negative decimal.

**Also known as:** EDaR, entropic drawdown, uncompounded EDaR, absolute EDaR.

**References:**

- paper | Cajas, D. (2021). "Entropic Portfolio Optimization: a Disciplined Convex Programming Framework." SSRN Electronic Journal.
- paper | Ahmadi-Javid, A. (2012). "Entropic Value-at-Risk: A New Coherent Risk Measure." Journal of Optimization Theory and Applications, 155(3), 1105-1123.
- library | Referenced against skfolio's [edar](https://skfolio.org/generated/skfolio.measures.edar.html){:target="_blank"}
- library | Referenced against Riskfolio-Lib's [EDaR_Rel](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/risk.html#RiskFunctions.EDaR_Rel){:target="_blank"} (compounded)
- library | Referenced against Riskfolio-Lib's [EDaR_Abs](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/risk.html#RiskFunctions.EDaR_Abs){:target="_blank"} (uncompounded)

**Args:**

- <u>period (str, optional):</u> The data frequency for returns. Options are: "daily", "weekly", "monthly",
"quarterly", "yearly". Defaults to "daily".
- <u>alpha (float, optional):</u> The tail probability for the EDaR calculation (e.g., 0.05 for the 95%
confidence level). Defaults to 0.05.
- <u>compound_returns (bool, optional):</u> Whether to compound the returns into the wealth path the drawdowns are
measured on, or to sum them (absolute drawdowns). Defaults to True.
- <u>within_period (bool, optional):</u> Whether to calculate the EDaR within the specified period or for the
entire period. Thus whether to look at the EDaR within a specific year (if period = 'yearly') or look
at the entirety of all years. Defaults to False. Note that this requires intraday data when period =
'daily', since a single day only nests observations when intraday data was fetched.
- <u>rolling (int, optional):</u> The rolling window size to use for the calculation. If set, the EDaR is
calculated over a rolling window of this many periods across the full return history instead
of per `period`, every window starting from a wealth of 1. Defaults to None.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the EDaR values over time. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series &#124; pd.DataFrame: EDaR values, per ticker, or per period (or date) and ticker.

**Notes:**

- The method retrieves historical return data based on the specified `period` and calculates the EDaR
for each asset in the Toolkit instance, each on its own returns.
- With growth, the method calculates the growth of EDaR values using the specified `lag`.
- Equals Riskfolio-Lib's EDaR_Rel and EDaR_Abs and skfolio's edar, which report the drawdown as a
positive number.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["^STOXX50E", "^N225", "^GSPC"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_entropic_drawdown_at_risk(period="yearly", within_period=True)
```

Which returns:

|      |   ^STOXX50E |   ^N225 |   ^GSPC |   Benchmark |
|:-----|------------:|--------:|--------:|------------:|
| 2021 |     -0.0676 | -0.1046 | -0.0453 |     -0.0446 |
| 2022 |     -0.2426 | -0.1427 | -0.2474 |     -0.2382 |
| 2023 |     -0.0947 | -0.0864 | -0.0902 |     -0.0874 |
| 2024 |     -0.0911 | -0.2002 | -0.0702 |     -0.0695 |
| 2025 |     -0.1374 | -0.184  | -0.1606 |     -0.1592 |

---

## get_maximum_drawdown
Calculate the Maximum Drawdown (MDD) of an investment portfolio or asset's returns: the largest decline from a high to a low, the worst loss an investor who bought at the top would have seen.

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

Wealth starts at 1, so a decline from the start of the window counts as well, and the result is a negative decimal (0 when the value never fell below a previous high). Without compounding the drawdowns are measured on the summed returns, as an absolute decline from their peak (Drawdown(t) = Sum(t) - max(0, max(Sum(s) for s <= t)), with Sum(t) = Σ Return(s)), which is the Maximum Drawdown of Chekhlov, Uryasev and Zabarankin (2005) and Riskfolio-Lib's $$\text{MDD}_{\text{Abs}}$$. With `rolling`, every window starts from a wealth of 1 at its first return, so it is the deepest decline within the trailing window.

**Also known as:** max drawdown, peak-to-trough decline, rolling maximum drawdown, uncompounded drawdown, absolute drawdown.

**References:**

- paper | Magdon-Ismail, M. and Atiya, A.F. (2004). "Maximum Drawdown." Risk Magazine, 17(10), 99-102.
- paper | Chekhlov, A., Uryasev, S. and Zabarankin, M. (2005). "Drawdown Measure in Portfolio Optimization." International Journal of Theoretical and Applied Finance, 8(1), 13-58.
- library | Referenced against skfolio's [max_drawdown](https://skfolio.org/generated/skfolio.measures.max_drawdown.html){:target="_blank"}
- library | Referenced against Riskfolio-Lib's [MDD_Rel](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/risk.html#RiskFunctions.MDD_Rel){:target="_blank"} (compounded)
- library | Referenced against Riskfolio-Lib's [MDD_Abs](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/risk.html#RiskFunctions.MDD_Abs){:target="_blank"} (uncompounded)
- library | Shares similar logic as empyrical's [max_drawdown](https://github.com/quantopian/empyrical/blob/0.5.5/empyrical/stats.py#L352){:target="_blank"}
- library | Shares similar logic as empyrical's [roll_max_drawdown](https://github.com/quantopian/empyrical/blob/0.5.5/empyrical/stats.py#L405){:target="_blank"} (rolling)
- library | Shares similar logic as PerformanceAnalytics (R)'s [maxDrawdown](https://github.com/braverock/PerformanceAnalytics/blob/v2.0.4/R/maxDrawdown.R#L44){:target="_blank"}
- library | Shares similar logic as quantstats' [max_drawdown](https://github.com/ranaroussi/quantstats/blob/v0.0.86/quantstats/stats.py#L2677){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The data frequency for returns. Options are: "daily", "weekly", "monthly",
"quarterly", "yearly". Defaults to "daily".
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
- <u>compound_returns (bool, optional):</u> Whether to compound the returns into the wealth path the drawdowns are
measured on, or to sum them (absolute drawdowns). Defaults to True.
- <u>rolling (int, optional):</u> The rolling window size to use for the calculation. If set, the Maximum
Drawdown is calculated over a rolling window of this many periods across the full return history
instead of per `period` (e.g. the deepest decline of the last 252 days). Defaults to None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series: Maximum Drawdown values with time as the index.

**Notes:**

- The method retrieves historical return data based on the specified `period` and calculates MMD for each
asset in the Toolkit instance.
- Without `within_period`, the drawdown is measured on the returns of the chosen period, so the
yearly period only compares year-end values: it is 0 when every year in the range closed at a
new high, even if prices fell within a year. Use the daily period for the deepest decline, or
the within-period version for the deepest decline within each year.
- With growth, the method calculates the growth of MMD values using the specified `lag`.
- Equals empyrical's max_drawdown and roll_max_drawdown, Riskfolio-Lib's $$\text{MDD}_{\text{Rel}}$$ and $$\text{MDD}_{\text{Abs}}$$ and skfolio's
max_drawdown, which report the decline as a positive number.

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
Calculate the Maximum Drawdown Duration of an investment portfolio or asset's returns: how many periods the largest drawdown took from its peak to its lowest point.

The Maximum Drawdown Duration is the number of periods between the peak and the lowest point of the largest drawdown, giving insight into how long the worst loss of value took to unfold.

The formula is as follows:

$$
\text{Maximum Drawdown Duration} = t(\text{trough}) - t(\text{peak})
$$

Where t(trough) is the period of the lowest Drawdown (see `get_maximum_drawdown`) and t(peak) the last period at or before it in which Wealth stood at the high that drawdown is measured from. When that high is the starting value of 1, t(peak) is the period before the first return.

**Also known as:** drawdown length.

**References:**

- library | Shares similar logic as PerformanceAnalytics (R)'s [table.Drawdowns](https://github.com/braverock/PerformanceAnalytics/blob/v2.0.4/R/table.Drawdowns.R#L54){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The data frequency for returns. Options are: "daily", "weekly", "monthly",
"quarterly", "yearly". Defaults to "daily".
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
- With growth, the method calculates the growth of the duration values using the specified `lag`.

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
Calculate the Maximum Drawdown Recovery Time of an investment portfolio or asset's returns: how many periods the asset took to climb back to its high after the bottom of its largest drawdown.

The Maximum Drawdown Recovery Time is the number of periods it takes for the cumulative return to climb back to its previous peak after the lowest point of the largest drawdown. If the drawdown has not yet been recovered from within the selected period, this returns NaN.

The formula is as follows:

$$
\text{Maximum Drawdown Recovery Time} = t(\text{recovery}) - t(\text{trough})
$$

Where t(trough) is the period of the lowest Drawdown (see `get_maximum_drawdown`) and t(recovery) the first period at or after it in which Wealth is back at or above the high that drawdown is measured from.

**Also known as:** time to recovery, drawdown recovery.

**References:**

- library | Shares similar logic as PerformanceAnalytics (R)'s [table.Drawdowns](https://github.com/braverock/PerformanceAnalytics/blob/v2.0.4/R/table.Drawdowns.R#L54){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The data frequency for returns. Options are: "daily", "weekly", "monthly",
"quarterly", "yearly". Defaults to "daily".
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
- With growth, the method calculates the growth of the recovery time values using the
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

Losses and gains are not symmetric: after a fall of 20% the asset needs a gain of 25% to be back at its high, after a fall of 50% a gain of 100%. The recovery version of the series shows that gain, the return needed from each period's value to get back to the running peak.

With the Deepest Since dates, every period below the peak also gets the last earlier date with a drawdown at least as deep, the familiar headline ("the deepest drawdown since April"), as `get_move_significance` (Econometrics) gives the "largest since" date of a single move.

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

**References:**

- library | Shares similar logic as PerformanceAnalytics (R)'s [Drawdowns](https://github.com/braverock/PerformanceAnalytics/blob/v2.0.4/R/Drawdowns.R#L3){:target="_blank"}
- library | Shares similar logic as quantstats' [to_drawdown_series](https://github.com/ranaroussi/quantstats/blob/v0.0.86/quantstats/stats.py#L2729){:target="_blank"}
- library | Shares similar logic as skfolio's [get_drawdowns](https://skfolio.org/generated/skfolio.measures.get_drawdowns.html){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The data frequency for returns. Options are: "daily", "weekly", "monthly",
"quarterly", "yearly". Defaults to "daily".
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

pd.DataFrame: The drawdown per period as a negative decimal or, with recovery, the gain needed
as a positive decimal (0 at a new high), with time as the index. With deepest since, the
columns hold the measures (Drawdown or Recovery Needed, and Deepest Since, the date as text)
and the tickers.

**Notes:**

- Each ticker keeps its own history: a ticker that listed during the window starts at its first close
and is NaN before it.
- A longer period only compares the closes of each period, so a monthly period shows shallower
drawdowns than a daily one.
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
List the largest drawdowns of each asset with their peak, trough and recovery dates, depth and length: whether an asset has one bad episode or recurring ones, and how long they took to recover.

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
\text{Recovery Ratio} = \frac{\text{To Recovery}}{\text{To Trough}}
$$

$$
\text{Recovery Return} = \frac{\operatorname{Wealth}(\text{recovery})}{\operatorname{Wealth}(\text{trough})} - 1
$$

$$
\text{To Trough} \;(\text{Days}) = \operatorname{date}(\text{trough}) - \operatorname{date}(\text{peak}),\;\; \text{likewise To Recovery (Days) and Length (Days)}
$$

$$
\text{Length} \;(\text{Years}) = \frac{\text{Length} \;(\text{Days})}{365.25}
$$

The Drawdown is the drawdown series of `get_drawdown_series`. A drawdown runs from the Peak (the last period at a high) to the Recovery (the first period back at that high), with its Trough at the lowest Drawdown in between. To Trough, To Recovery and Length count periods (trading days for daily data), the columns marked (Days) count calendar days between the same dates (the last day of each period for weekly or longer periods), and Length (Years) is Length (Days) in years of 365.25 days. Calendar time compares assets on exchanges with other holidays, and reads as the time an investor waited. The Recovery Ratio compares the way back with the way down: above 1 the recovery took longer than the decline. The Recovery Return is the gain from the trough to the close of the recovery, which can be more than the Recovery Needed when that close lies above the old peak.

Each drawdown is dated by its peak, valley and recovery, so it starts on the peak rather than on the first period below it. The deepest drawdown matches `get_maximum_drawdown`, `get_maximum_drawdown_duration` (To Trough) and `get_maximum_drawdown_recovery_time` (To Recovery).

**Also known as:** worst drawdowns, drawdown details, drawdown periods, gain needed to recover, recovery duration ratio, recovery return.

**References:**

- library | Shares similar logic as PerformanceAnalytics (R)'s [table.Drawdowns](https://github.com/braverock/PerformanceAnalytics/blob/v2.0.4/R/table.Drawdowns.R#L54){:target="_blank"}
- library | Shares similar logic as quantstats' [drawdown_details](https://github.com/ranaroussi/quantstats/blob/v0.0.86/quantstats/stats.py#L3301){:target="_blank"}

**Args:**

- <u>top (int, optional):</u> The number of drawdowns per asset, deepest first. Defaults to 5.
- <u>period (str, optional):</u> The data frequency for returns. Options are: "daily", "weekly", "monthly",
"quarterly", "yearly". Defaults to "daily".
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
Recovery Ratio and the Recovery Return, the same in calendar days (To Trough (Days), To Recovery
(Days), Length (Days)) and Length (Years).

**Notes:**

- A drawdown that has not recovered by the end of the window has no Recovery, To Recovery, Length,
Recovery Ratio or Recovery Return, in periods or calendar time (NaN); `get_drawdown_statistics` gives
the state of that open drawdown. Its Recovery Needed is the gain from its trough; the gain
still needed from the latest value is the last Recovery Needed of `get_drawdown_series`.
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

|                  | Peak       | Trough     | Recovery   |   Drawdown |   Recovery Needed |   To Trough |   To Recovery |   Length |   Recovery Ratio |   Recovery Return |   To Trough (Days) |   To Recovery (Days) |   Length (Days) |   Length (Years) |
|:-----------------|:-----------|:-----------|:-----------|-----------:|------------------:|------------:|--------------:|---------:|-----------------:|------------------:|-------------------:|---------------------:|----------------:|-----------------:|
| ('META', 1)      | 2021-09-07 | 2022-11-03 | 2024-01-19 |    -0.7674 |            3.2985 |         293 |           302 |      595 |           1.0307 |            3.3128 |                422 |                  442 |             864 |           2.3655 |
| ('META', 2)      | 2025-02-14 | 2025-04-21 | 2025-06-30 |    -0.3415 |            0.5186 |          44 |            48 |       92 |           1.0909 |            0.5241 |                 66 |                   70 |             136 |           0.3723 |
| ('META', 3)      | 2025-08-12 | 2025-11-20 | NaT        |    -0.2537 |            0.34   |          71 |           nan |      nan |         nan      |          nan      |                100 |                  nan |             nan |         nan      |
| ('NFLX', 1)      | 2021-11-17 | 2022-05-11 | 2024-08-20 |    -0.7594 |            3.1569 |         120 |           571 |      691 |           4.7583 |            3.1977 |                175 |                  832 |            1007 |           2.757  |
| ('NFLX', 2)      | 2025-06-30 | 2025-12-10 | NaT        |    -0.3077 |            0.4444 |         114 |           nan |      nan |         nan      |          nan      |                163 |                  nan |             nan |         nan      |
| ('NFLX', 3)      | 2025-02-14 | 2025-04-04 | 2025-04-24 |    -0.1915 |            0.2368 |          34 |            13 |       47 |           0.3824 |            0.2816 |                 49 |                   20 |              69 |           0.1889 |
| ('Benchmark', 1) | 2022-01-03 | 2022-10-12 | 2023-12-13 |    -0.245  |            0.3244 |         195 |           294 |      489 |           1.5077 |            0.3403 |                282 |                  427 |             709 |           1.9411 |
| ('Benchmark', 2) | 2025-02-19 | 2025-04-08 | 2025-06-26 |    -0.1876 |            0.2308 |          34 |            54 |       88 |           1.5882 |            0.2361 |                 48 |                   79 |             127 |           0.3477 |
| ('Benchmark', 3) | 2024-07-16 | 2024-08-05 | 2024-09-19 |    -0.0841 |            0.0918 |          14 |            32 |       46 |           2.2857 |            0.1036 |                 20 |                   45 |              65 |           0.178  |

---

## get_drawdown_statistics
Summarize the drawdowns of each asset: how many there were, how deep they were on average, how much their depth varied, how long they took to reach the bottom and to recover, how much of the time the asset spent below its high and where the drawdown that is still open stands.

Where the drawdown table (`get_drawdown_table`) lists the largest drawdowns one by one, the statistics average over all of them, which is what Bacon (2008) uses to describe the drawdown risk of a fund: a manager with many shallow drawdowns that recover quickly and one with a few deep, long ones can have the same Maximum Drawdown. The Coverage is the share of the periods spent below the running high, and the Active measures describe the drawdown the asset is in at the end of the window: how deep it is, how long ago the high was and the bottom was, and how much of the decline has been made good.

The formula is as follows:

$$
\operatorname{Drawdown}(t) = \frac{\operatorname{Wealth}(t)}{\max(1,\; \max(\operatorname{Wealth}(s) \;\text{for}\; s \leq t))} - 1
$$

$$
\text{Average Drawdown} = \frac{\sum \;\operatorname{Drawdown}(j)}{d}
$$

$$
\text{Drawdown Deviation} = \sqrt{\frac{\sum \;\operatorname{Drawdown}(j)^{2}}{n}}
$$

$$
\text{Average To Trough} = \frac{\sum(t(\text{trough},\; j) - t(\text{peak},\; j))}{d}
$$

$$
\text{Average To Recovery} = \frac{\sum(t(\text{recovery},\; j) - t(\text{trough},\; j))}{d_{\text{recovered}}}
$$

$$
\text{Average Length} = \frac{\sum(t(\text{recovery},\; j) - t(\text{peak},\; j))}{d_{\text{recovered}}}
$$

$$
\text{Average Recovery Ratio} = \frac{\frac{\sum(t(\text{recovery},\; j) - t(\text{trough},\; j))}{t(\text{trough},\; j) - t(\text{peak},\; j)}}{d_{\text{recovered}}}
$$

$$
\text{Average Recovery Return} = \frac{\sum\left(\frac{\operatorname{Wealth}(\text{recovery},\; j)}{\operatorname{Wealth}(\text{trough},\; j)} - 1\right)}{d_{\text{recovered}}}
$$

$$
\text{Coverage} = \text{the number of periods with Drawdown}(t) < \frac{0}{n}
$$

$$
\text{Active Drawdown} = \operatorname{Drawdown}(T)
$$

$$
\text{Active Duration} = T - t(\text{peak}),\;\; \text{Active Recovery Duration} = T - t(\text{trough})
$$

$$
\text{Active Recovery Return} = \frac{1 + \operatorname{Drawdown}(T)}{1 + \operatorname{Drawdown}(\text{trough})} - 1
$$

$$
\text{Active Recovery} = 1 - \frac{\operatorname{Drawdown}(T)}{\operatorname{Drawdown}(\text{trough})}
$$

Where Drawdown(j) is the depth (the lowest Drawdown) of the j-th of the d drawdowns of `get_drawdown_table`, n the number of returns, d_recovered the number of drawdowns that recovered before the end of the window, T the last period and, for the Active measures, peak the last period at the high and trough the lowest Drawdown since. The lengths count periods (trading days for daily data) and Average Length (Days) the calendar days from peak to recovery. Average Drawdown is negative, Drawdown Deviation positive. The Active Recovery is the share of the decline from the peak to the trough that has been made good (0 at the trough, 1 back at the peak).

**Also known as:** drawdown summary, average drawdown, drawdown deviation, average drawdown length, average recovery time, average drawdown days, time under water, current drawdown, open drawdown, recovery duration ratio.

**References:**

- paper | Bacon, C.R. (2008). "Practical Portfolio Performance Measurement and Attribution." John Wiley & Sons, 2nd edition.
- library | Shares similar logic as PerformanceAnalytics (R)'s [AverageDrawdown](https://github.com/braverock/PerformanceAnalytics/blob/v2.0.4/R/maxDrawdown.R#L178){:target="_blank"}
- library | Shares similar logic as PerformanceAnalytics (R)'s [DrawdownDeviation](https://github.com/braverock/PerformanceAnalytics/blob/v2.0.4/R/maxDrawdown.R#L147){:target="_blank"}
- library | Shares similar logic as PerformanceAnalytics (R)'s [AverageRecovery](https://github.com/braverock/PerformanceAnalytics/blob/v2.0.4/R/maxDrawdown.R#L212){:target="_blank"}
- library | Shares similar logic as PerformanceAnalytics (R)'s [AverageLength](https://github.com/braverock/PerformanceAnalytics/blob/v2.0.4/R/maxDrawdown.R#L240){:target="_blank"}
- library | Shares similar logic as ffn's [PerformanceStats.avg_drawdown](https://github.com/pmorissette/ffn/blob/v1.4.1/ffn/core.py#L377){:target="_blank"}
- library | Shares similar logic as vectorbt's [Drawdowns.active_drawdown](https://github.com/polakowo/vectorbt/blob/v1.2.1/vectorbt/generic/drawdowns.py#L407){:target="_blank"}
- library | Shares similar logic as vectorbt's [Drawdowns.recovery_duration_ratio](https://github.com/polakowo/vectorbt/blob/v1.2.1/vectorbt/generic/drawdowns.py#L392){:target="_blank"}
- library | Shares similar logic as vectorbt's [Drawdowns.recovery_return](https://github.com/polakowo/vectorbt/blob/v1.2.1/vectorbt/generic/drawdowns.py#L328){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The data frequency for returns. Options are: "daily", "weekly", "monthly",
"quarterly", "yearly". Defaults to "daily".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: One row per ticker with the number of Drawdowns, the Average Drawdown, the Drawdown
Deviation, the Average To Trough, Average To Recovery and Average Length in periods, the
Average Length (Days) in calendar days, the Average Recovery Ratio and Average Recovery Return,
the Coverage and the Active Drawdown, Active Duration, Active Recovery Duration (in periods),
Active Recovery Return and Active Recovery.

**Notes:**

- Each ticker keeps its own history: a ticker that listed during the window starts at its first close.
- The Average Drawdown and Drawdown Deviation agree with PerformanceAnalytics' AverageDrawdown and
DrawdownDeviation (which report the average as a positive number), and the Average Drawdown equals
ffn's avg_drawdown. A drawdown that has not recovered by the end of the window has no recovery, so it
is left out of the Average To Recovery, Average Length and the recovery averages; PerformanceAnalytics'
AverageRecovery and AverageLength count it as recovered one period after the end. ffn's avg_drawdown_days
counts calendar days from the first day below the peak, Average Length (Days) from the peak itself.
- The Coverage, the Active measures and the recovery averages equal vectorbt's Drawdowns measures of the
same names on the wealth path (the recovery averages over its recovered drawdowns).
- At a high there is no open drawdown: the Active Drawdown and Active Duration are 0 and the other
Active measures NaN.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["META", "NFLX"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_drawdown_statistics().T
```

Which returns:

|                          |    META |     NFLX |   Benchmark |
|:-------------------------|--------:|---------:|------------:|
| Drawdowns                | 39      |  30      |     87      |
| Average Drawdown         | -0.072  |  -0.0735 |     -0.0174 |
| Drawdown Deviation       |  0.0267 |   0.0249 |      0.0101 |
| Average To Trough        | 15.5641 |  15      |      5.977  |
| Average To Recovery      | 15.3684 |  25.931  |      7.3372 |
| Average Length           | 29.4737 |  37.5172 |     13.3372 |
| Average Length (Days)    | 42.7895 |  54.7241 |     19.3605 |
| Average Recovery Ratio   |  1.4327 |   1.3625 |      1.1949 |
| Average Recovery Return  |  0.1628 |   0.1717 |      0.0225 |
| Coverage                 |  0.941  |   0.9466 |      0.8493 |
| Active Drawdown          | -0.1632 |  -0.2998 |     -0.0123 |
| Active Duration          | 98      | 128      |      4      |
| Active Recovery Duration | 27      |  14      |      0      |
| Active Recovery Return   |  0.1213 |   0.0113 |      0      |
| Active Recovery          |  0.3568 |   0.0255 |      0      |

---

## get_ulcer_index
Calculate the Ulcer Index of an investment portfolio or asset's returns: how deep and how long its drawdowns are, the root mean square of the declines from a recent high.

The Ulcer Index is a financial metric used to assess the risk and volatility of an investment portfolio or asset. Developed by Peter Martin in the 1980s, the Ulcer Index is particularly useful for evaluating the downside risk and drawdowns associated with investments.

The Ulcer Index differs from traditional volatility measures like standard deviation or variance because it focuses on the depth and duration of drawdowns rather than the dispersion of returns.

The formula is as follows (with the default window of 14):

$$
\text{Ulcer Index} = \sqrt{\frac{\sum\left(\frac{\operatorname{Wealth}(t) - \text{Highest High}(t)}{\text{Highest High}(t)}\right)^{2}}{n}}
$$

Where Wealth(t) compounds the daily returns within each period from a starting value of 1, Highest High(t) is the highest Wealth over the trailing 14 observations (the starting value of 1 included while fewer are available) and n is the number of daily returns in the period.

Martin measures every drawdown from the highest value so far (no window); the default trailing 14-period high is the variant StockCharts popularised. While fewer than `window` observations are available, the high is taken over the observations so far, so periods shorter than the window still have a value. The result is a decimal (0.05 is a root mean squared drawdown of 5%), where Martin quotes percentages.

The Ulcer Index punishes both the depth and the length of drawdowns, so an asset that falls 10% and stays there for months scores worse than one that drops 10% and recovers within a week, which a volatility figure would not show. It is the risk measure behind the Martin ratio (excess return divided by the Ulcer Index) and is read best relative to peers over the same window, since the default 14-period lookback gives lower values than a since-inception high-water mark.

Without compounding the drawdowns are the absolute declines of 1 plus the summed returns from their high, (Wealth(t) - Highest High(t)) with Wealth(t) = $$1 + \Sigma$$ Return(s), instead of the relative ones.

**Also known as:** UI, drawdown risk, uncompounded ulcer index.

**References:**

- paper | Martin, P.G. and McCann, B.B. (1989). "The Investor's Guide to Fidelity Funds." John Wiley & Sons.
- library | Referenced against Riskfolio-Lib's [UCI_Rel](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/risk.html#RiskFunctions.UCI_Rel){:target="_blank"} (compounded, no window)
- library | Referenced against Riskfolio-Lib's [UCI_Abs](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/risk.html#RiskFunctions.UCI_Abs){:target="_blank"} (uncompounded, no window)
- library | Shares similar logic as PerformanceAnalytics (R)'s [UlcerIndex](https://github.com/braverock/PerformanceAnalytics/blob/v2.0.4/R/UlcerIndex.R#L31){:target="_blank"}
- library | Shares similar logic as quantstats' [ulcer_index](https://github.com/ranaroussi/quantstats/blob/v0.0.86/quantstats/stats.py#L1829){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The data frequency for returns. Options are: "daily", "weekly", "monthly",
"quarterly", "yearly". Defaults to "quarterly" for a quarterly Toolkit, otherwise "yearly".
- <u>window (int &#124; None, optional):</u> The trailing lookback window used as the high-water
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
- <u>compound_returns (bool, optional):</u> Whether to compound the returns into the wealth path the drawdowns
are measured on, or to sum them (absolute drawdowns). Defaults to True.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series: UI values with time as the index.

**Notes:**

- The method retrieves historical return data based on the specified `period` and calculates UI for each
asset in the Toolkit instance.
- With growth, the method calculates the growth of UI values using the specified `lag`.

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
Calculate the Pain Index of an investment portfolio or asset's returns: the average depth below its high over every day of a period, the area under water per day.

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

**Also known as:** average drawdown, mean drawdown.

**References:**

- paper | Bacon, C.R. (2013). "Practical Risk-Adjusted Performance Measurement." John Wiley & Sons, chapter 5 (the Pain Index of Zephyr Associates).
- library | Shares similar logic as PerformanceAnalytics (R)'s [PainIndex](https://github.com/braverock/PerformanceAnalytics/blob/v2.0.4/R/PainIndex.R#L38){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The data frequency for returns. Options are: "daily", "weekly", "monthly",
"quarterly", "yearly". Defaults to "quarterly" for a quarterly Toolkit, otherwise "yearly".
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
- With growth, the method calculates the growth of the Pain Index values using the
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
| 2024 | 0.3182 |   0.1124 |      0.0113 |
| 2025 | 0.0715 |   0.0422 |      0.0278 |

---

## get_average_drawdown
Calculate the Average Drawdown of an investment portfolio or asset's returns: how deep a typical setback is, or how far below its high the asset typically was.

The Average Drawdown has two definitions. Bacon (2008), PerformanceAnalytics and ffn average the depth of the drawdown episodes: every decline from a high until the asset is back at it counts once, with its deepest point. Chekhlov, Uryasev and Zabarankin (2005), Riskfolio-Lib and skfolio average the drawdown of every period instead, the periods at a high counting as 0, which weighs a drawdown by how long it lasted (the Pain Index, `get_pain_index`, is that average per year as a positive number). The episode average says how deep a typical setback is, the period average how far below its high the asset typically was. Both are less dominated by a single crash than the Maximum Drawdown.

The formula for the episode average, the default, is as follows:

$$
\operatorname{Wealth}(t) = \prod(1 + \operatorname{Return}(s)) \;\text{for}\; s \leq t
$$

$$
\operatorname{Drawdown}(t) = \frac{\operatorname{Wealth}(t)}{\max(1,\; \max(\operatorname{Wealth}(s) \;\text{for}\; s \leq t))} - 1
$$

$$
\text{Average Drawdown} = \frac{\sum \;\operatorname{Trough}(j)}{d}
$$

Where Trough(j) is the lowest Drawdown of the j-th of the d episodes below a high (one that has not recovered by the end of the window included). The formula for the observation average is as follows:

$$
\text{Average Drawdown} = \frac{\sum \;\operatorname{Drawdown}(t)}{n}
$$

Where n is the number of returns. Wealth starts at 1, so a decline from the start of the window counts. Without compounding the drawdowns are measured on the summed returns instead, as an absolute decline from their peak (Drawdown(t) = Sum(t) - max(0, max(Sum(s) for s <= t)), with Sum(t) = Σ Return(s)). The result is a negative decimal (0 when the value never fell below a previous high).

**Also known as:** ADD, average drawdown depth, mean drawdown, uncompounded average drawdown.

**References:**

- paper | Bacon, C.R. (2008). "Practical Portfolio Performance Measurement and Attribution." John Wiley & Sons, 2nd edition.
- paper | Chekhlov, A., Uryasev, S. and Zabarankin, M. (2005). "Drawdown Measure in Portfolio Optimization." International Journal of Theoretical and Applied Finance, 8(1), 13-58.
- library | Referenced against skfolio's [average_drawdown](https://skfolio.org/generated/skfolio.measures.average_drawdown.html){:target="_blank"} (observation)
- library | Referenced against Riskfolio-Lib's [ADD_Rel](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/risk.html#RiskFunctions.ADD_Rel){:target="_blank"} (observation, compounded)
- library | Referenced against Riskfolio-Lib's [ADD_Abs](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/risk.html#RiskFunctions.ADD_Abs){:target="_blank"} (observation, uncompounded)
- library | Shares similar logic as PerformanceAnalytics (R)'s [AverageDrawdown](https://github.com/braverock/PerformanceAnalytics/blob/v2.0.4/R/maxDrawdown.R#L178){:target="_blank"} (episode)
- library | Shares similar logic as ffn's [PerformanceStats.avg_drawdown](https://github.com/pmorissette/ffn/blob/v1.4.1/ffn/core.py#L377){:target="_blank"} (episode)

**Args:**

- <u>period (str, optional):</u> The data frequency for returns. Options are: "daily", "weekly", "monthly",
"quarterly", "yearly". Defaults to "daily".
- <u>method (str, optional):</u> The average. Options are: "episode" (the average depth of the drawdown
episodes), "observation" (the average drawdown of every period). Defaults to "episode".
- <u>compound_returns (bool, optional):</u> Whether to compound the returns into the wealth path the drawdowns are
measured on, or to sum them (absolute drawdowns). Defaults to True.
- <u>within_period (bool, optional):</u> Whether to calculate the Average Drawdown within the specified period
or for the entire period. Thus whether to look at the Average Drawdown within a specific year (if
period = 'yearly') or look at the entirety of all years. Defaults to False. Note that this requires
intraday data when period = 'daily', since a single day only nests observations when intraday data
was fetched.
- <u>rolling (int, optional):</u> The rolling window size to use for the calculation. If set, the Average
Drawdown is calculated over a rolling window of this many periods across the full return history
instead of per `period`, every window starting from a wealth of 1. Defaults to None.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Average Drawdown values over time.
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

pd.Series &#124; pd.DataFrame: Average Drawdown values, per ticker, or per period (or date) and ticker.

**Notes:**

- The method retrieves historical return data based on the specified `period` and calculates the Average
Drawdown for each asset in the Toolkit instance, each on its own returns.
- With growth, the method calculates the growth of the Average Drawdown values using the
specified `lag`.
- The episode average agrees with PerformanceAnalytics' AverageDrawdown and ffn's avg_drawdown, the
observation average with Riskfolio-Lib's $$\text{ADD}_{\text{Rel}}$$ and $$\text{ADD}_{\text{Abs}}$$ and skfolio's average_drawdown;
PerformanceAnalytics and the Python libraries other than ffn report the drawdown as a positive number.
PerformanceAnalytics' arithmetic version divides the decline of 1 + the summed returns by its peak, where the uncompounded drawdown here
(and in Riskfolio-Lib and skfolio) takes the absolute decline.
- The Sterling Ratio of `toolkit.performance` averages the depths of the 3 deepest episodes only (Bacon's
Average Largest Drawdown); with at least as many as there are episodes it is the episode average.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["TSLA", "GM", "F"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_average_drawdown(period="yearly", within_period=True)
```

Which returns:

|      |    TSLA |      GM |       F |   Benchmark |
|:-----|--------:|--------:|--------:|------------:|
| 2021 | -0.1491 | -0.0916 | -0.0589 |     -0.0128 |
| 2022 | -0.7272 | -0.5304 | -0.2025 |     -0.245  |
| 2023 | -0.1077 | -0.0943 | -0.13   |     -0.0164 |
| 2024 | -0.1443 | -0.0581 | -0.0914 |     -0.0129 |
| 2025 | -0.1155 | -0.0296 | -0.0561 |     -0.0195 |

---

## get_amihud_illiquidity
Calculate the Amihud (2002) Illiquidity ratio per asset: how much the price moves per dollar traded, high for an illiquid asset.

The Amihud ratio measures the average price impact of trading -- how much the price moves per dollar of trading volume. A high value means that even a small amount of trading moves the price a lot (the asset is illiquid), while a low value means the asset can absorb a large amount of trading with little price impact (the asset is liquid).

The Amihud ratio is mainly a cross-sectional measure: it ranks stocks by how much a given dollar volume moves the price and is used as a liquidity factor in asset pricing. Its level depends on the scale, the frequency and the price level of the market, so compare stocks within the same market and period, and expect the ratio of large caps to be several orders of magnitude below that of small caps.

The formula is as follows (with the default scale of 1,000,000):

$$
\text{Amihud Illiquidity} = \operatorname{Mean}\left(\frac{\left|\text{Return}_{t}\right|}{\text{Close}_{t} \cdot \text{Volume}_{t}}\right) \cdot \text{1,000,000}
$$

Where the mean runs over the periods of the chosen frequency (within each period with `within_period`), and periods without dollar volume are skipped.

**Also known as:** Amihud illiquidity ratio, ILLIQ, price impact ratio.

**References:**

- paper | Amihud, Y. (2002). "Illiquidity and Stock Returns: Cross-Section and Time-Series Effects." Journal of Financial Markets, 5(1), 31-56.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns. Options are: "daily", "weekly", "monthly",
"quarterly", "yearly". Defaults to "daily".
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
- With growth, the method calculates the growth of the Amihud Illiquidity values
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

## get_price_impact
Calculate the price impact of trading per asset and period: how much the price moves per unit traded, with Kyle's, Amihud's or Hasbrouck's lambda as the regression slopes of López de Prado (2018, chapter 19.4) or with the Roll Impact (section 19.3.2).

Each lambda is the slope of a regression, without an intercept, of the daily price changes on a measure of the trading of the day, over the days within the period. A high value is an illiquid asset, in which trading moves the price a lot:

- Kyle's lambda: Kyle (1985) models market makers who cannot tell informed from uninformed orders and move the price by $$\lambda$$ per share of net order flow. The price change of a day is regressed on its Volume, signed with the tick rule (a rise is buying, a fall selling).
- Amihud's lambda: the absolute log return of a day is regressed on its dollar volume. This is the regression form of the Amihud (2002) illiquidity ratio (`get_amihud_illiquidity`, the mean of the ratios), which weighs the days by their dollar volume, so a quiet day with a large move does not dominate it.
- Hasbrouck's lambda: Hasbrouck (2009) uses the square root of the signed dollar volume, as the impact of an order grows less than proportionally with its size. The log return of a day is regressed on the square root of its dollar volume, signed with the tick rule.
- Roll Impact: the Roll (1984) spread of the period (see `get_roll_spread`) divided by the mean dollar volume of its days, the spread paid per dollar traded.

The measures are mostly used to compare assets and periods: a rising lambda is a market that has become thinner. Their level depends on the size of the asset (a large cap trades billions of dollars a day), so compare assets of a similar size or look at the changes over time.

The formula is as follows:

For Kyle's lambda:

$$
b_{t} = \operatorname{sign}(\Delta P_{t}),\;\; \text{or}\;\; b_{t-1} \;\text{when}\; \Delta P_{t} = 0
$$

$$
\Delta P_{t} = \lambda \cdot (b_{t} \cdot V_{t}) + \epsilon_{t}
$$

$$
\text{Kyle's Lambda} = \frac{\sum(\Delta P_{t} \cdot b_{t} \cdot V_{t})}{\sum((b_{t} \cdot V_{t})^{2})} \cdot \text{1,000,000}
$$

For Amihud's lambda:

$$
\left|r_{t}\right| = \lambda \cdot \text{DV}_{t} + \epsilon_{t}
$$

$$
\text{Amihud's Lambda} = \frac{\sum(\left|r_{t}\right| \cdot \text{DV}_{t})}{\sum(\text{DV}_{t}^{2})} \cdot \text{1,000,000,000}
$$

For Hasbrouck's lambda:

$$
b_{t} = \operatorname{sign}(r_{t}),\;\; \text{or}\;\; b_{t-1} \;\text{when}\; r_{t} = 0
$$

$$
r_{t} = \lambda \cdot (b_{t} \cdot \sqrt{\text{DV}} \;\text{}_{t}) + \epsilon_{t}
$$

$$
\text{Hasbrouck's Lambda} = \frac{\sum(r_{t} \cdot b_{t} \cdot \sqrt{\text{DV}} \;\text{}_{t})}{\sum(\text{DV}_{t})} \cdot \text{1,000,000}
$$

For the Roll Impact:

$$
\text{Roll Spread} = 2 \cdot \sqrt{- \operatorname{Cov}(\Delta P_{t},\; \Delta P_{t-1})}
$$

$$
\text{Roll Impact} = \frac{\text{Roll Spread}}{\operatorname{Mean}(\text{DV}_{t})} \cdot \text{1,000,000,000}
$$

Where $$\Delta P_{t}$$ is the change of the Close, $$V_{t}$$ the Volume, $$\text{DV}_{t}$$ = Close_t * $$V_{t}$$ the dollar volume and $$r_{t}$$ the log return of the Adjusted Close (continuously compounded) on day t; the sums, the covariance (with n - 1 in the denominator) and the mean run over the days within the period. The default `scale` makes the measures of stocks readable: Kyle's lambda is the change of the price per million shares of net buying, Amihud's lambda the absolute log return per billion dollars traded (as `get_amihud_illiquidity` is shown), Hasbrouck's lambda the log return per square root of a dollar times 1,000,000 and the Roll Impact the spread in price units per billion dollars traded a day.

**Also known as:** price impact coefficient, Kyle's lambda, market depth, Amihud's lambda, Hasbrouck's lambda, Roll impact.

**References:**

- paper | Kyle, A. S. (1985). "Continuous Auctions and Insider Trading." Econometrica, 53(6), 1315-1335.
- paper | Amihud, Y. (2002). "Illiquidity and Stock Returns: Cross-Section and Time-Series Effects." Journal of Financial Markets, 5(1), 31-56.
- paper | Hasbrouck, J. (2009). "Trading Costs and Returns for U.S. Equities: Estimating Effective Costs from Daily Data." The Journal of Finance, 64(3), 1445-1477.
- paper | Roll, R. (1984). "A Simple Implicit Measure of the Effective Bid-Ask Spread in an Efficient Market." The Journal of Finance, 39(4), 1127-1139.
- paper | López de Prado, M. (2018). "Advances in Financial Machine Learning." Wiley, sections 19.3.2 and 19.4.

**Args:**

- <u>period (str, optional):</u> The period each regression runs within. Options are: "weekly", "monthly",
"quarterly", "yearly". Defaults to "monthly".
- <u>rolling (int, optional):</u> Regress on the days of the last `rolling` periods together instead of one
period (e.g. period='monthly' and rolling=3 for a three-month lambda at every month end).
Defaults to None.
- <u>method (str, optional):</u> The measure. Options are: "kyle" (Kyle's lambda), "amihud" (Amihud's lambda),
"hasbrouck" (Hasbrouck's lambda), "roll" (Roll Impact). Defaults to "kyle".
- <u>scale (float &#124; None, optional):</u> A multiplier applied to the measure for readability. Defaults to
None, which uses 1,000,000 for method="kyle" and "hasbrouck" and 1,000,000,000 for "amihud" and
"roll".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the measure over time. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The price impact with the periods as the index and the assets as columns.

**Notes:**

- The method uses the daily prices of each asset on its own trading days; the price change and log
return of a day are those since the asset's previous trading day.
- A day without a price change keeps the sign of the last change (the tick rule), as in the book.
- A period with fewer than two days, or for the Roll Impact with fewer than three pairs of consecutive
price changes within the period or an autocovariance of zero or above (no Roll spread), is NaN.
- The lambdas are the regression slopes of the book, not the means of the ratios ($$\Delta P_{t} / (b_{t} \cdot V_{t})$$
and the like), which would weigh every day equally however little traded on it. For the Roll impact a
positive autocovariance is NaN, as in `get_roll_spread`, and the spread is divided by the mean dollar
volume of the period.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["SNAP", "ETSY", "LYFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-06-30",
)

toolkit.risk.get_price_impact()
```

Which returns:

| Date    |   SNAP |   ETSY |   LYFT |   Benchmark |
|:--------|-------:|-------:|-------:|------------:|
| 2025-01 | 0.0121 | 0.3753 | 0.018  |      0.091  |
| 2025-02 | 0.008  | 0.2696 | 0.0139 |      0.089  |
| 2025-03 | 0.008  | 0.2065 | 0.0151 |      0.0879 |
| 2025-04 | 0.0079 | 0.2512 | 0.0307 |      0.1089 |
| 2025-05 | 0.006  | 0.2008 | 0.0263 |      0.0672 |
| 2025-06 | 0.0061 | 0.1986 | 0.0166 |      0.0462 |

---

## get_roll_spread
Calculate the Roll (1984) implied bid-ask spread per asset: the cost of a round trip implied by the bounce of the price between the bid and the ask.

Roll's model shows that, under a stylized microstructure model in which the true (efficient) price follows a random walk and observed trade prices randomly bounce between the bid and the ask, the effective spread can be backed out purely from the serial covariance of consecutive price changes, without needing any actual quote data. If the estimated covariance is zero or positive, no valid estimate can be backed out and NaN is returned instead.

The Roll measure is used when no quote data is available, typically for less liquid stocks or historical studies. On daily closes of liquid large caps it mostly picks up price noise rather than the bid-ask bounce, and in trending periods the autocovariance is positive and no estimate exists, so treat it as a rough, relative measure.

The formula is as follows:

$$
\text{Roll Spread} = 2 \cdot \sqrt{- \operatorname{Cov}(\Delta P_{t},\; \Delta P_{t-1})}
$$

$$
\text{Relative Roll Spread} = \frac{\text{Roll Spread}}{\operatorname{Mean}(P)}
$$

Where P is the Close price, $$\Delta P_{t} = P_{t} - P_{t - 1}$$ and Cov the sample autocovariance (with n - 1 in the denominator) of consecutive price changes; a covariance of zero or above gives NaN.

**Also known as:** Roll's implied spread, Roll measure.

**References:**

- paper | Roll, R. (1984). "A Simple Implicit Measure of the Effective Bid-Ask Spread in an Efficient Market." The Journal of Finance, 39(4), 1127-1139.

**Args:**

- <u>period (str, optional):</u> The data frequency. Options are: "daily", "weekly", "monthly", "quarterly",
"yearly". Defaults to "daily".
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

## get_bid_ask_spread
Calculate the bid-ask spread per asset and period: the cost of a round trip, estimated from daily prices alone, without quote data.

It uses the EDGE estimator of Ardia, Guidotti and Kroencke (2024), the high-low estimator of Corwin and Schultz (2012) or the close-high-low estimator of Abdi and Ranaldo (2017).

The daily High is almost always a trade at the ask and the daily Low a trade at the bid, while the Open and the Close are trades at either. The range of a day and the distance of the Open and Close to it therefore hold both the volatility and the bid-ask spread, and each estimator separates the two in its own way:

- EDGE (the Efficient Discrete Generalized Estimator) takes the mid-range (the average of the High and Low) as a proxy for the efficient price; the returns between it and the Open and the Close bounce with the spread. Four such estimators, two at the open and two at the close (one of them a generalization of the Abdi-Ranaldo spread), are combined with the weights of the Generalized Method of Moments that minimize the variance of the estimate. The probabilities in the formula correct for days without trades, which repeat the previous Close. The estimate is asymptotically unbiased and, in the paper's simulations and empirical tests, more precise than the Roll, Corwin-Schultz and Abdi-Ranaldo estimators. It is estimated from all pairs of consecutive trading days of the period at once.
- Corwin-Schultz: the volatility part of the range grows with the length of the window while the spread part does not, so comparing the ranges of two single days with the range over both days together backs out the spread from the daily High and Low. Each pair of consecutive trading days gives an estimate and the spread of a period is the average of the estimates within it.
- Abdi-Ranaldo: the distance of the Close to the mid-range of its own day and to that of the next day both hold half the spread, and their product removes the volatility of the efficient price. Unlike the Corwin-Schultz spread, the estimator uses the Close as well and needs no adjustment for the overnight return (a weekend or a gap at the open). Each pair of consecutive trading days gives an estimate and the spread of a period is the average of the estimates within it.

The estimators are mostly used where no quotes are available (historical studies, smaller markets) and rank assets well by their spread. For liquid large caps the spread is a few basis points, close to the estimation error and dominated by the volatility within the day, so read it as a relative measure there. The Roll spread, which uses the covariance of the close-to-close price changes, is `get_roll_spread`.

The formula is as follows:

For the EDGE spread:

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

For the Corwin-Schultz spread:

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

For the Abdi-Ranaldo spread:

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

**Also known as:** bid-ask spread estimator, effective spread, Efficient Discrete Generalized Estimator, EDGE spread, EDGE estimator, OHLC spread estimator, Corwin-Schultz spread, high-low spread estimator, HL spread, CS spread, Abdi-Ranaldo spread, close-high-low spread estimator, CHL spread, AR spread.

**References:**

- paper | Ardia, D., Guidotti, E., & Kroencke, T. A. (2024). "Efficient Estimation of Bid-Ask Spreads from Open, High, Low, and Close Prices." Journal of Financial Economics, 161, 103916.
- paper | Corwin, S. A., & Schultz, P. (2012). "A Simple Way to Estimate Bid-Ask Spreads from Daily High and Low Prices." The Journal of Finance, 67(2), 719-760.
- paper | Abdi, F., & Ranaldo, A. (2017). "A Simple Estimation of Bid-Ask Spreads from Daily Close, High, and Low Prices." The Review of Financial Studies, 30(12), 4437-4480.
- library | Shares similar logic as RiskLabAI's [edge_estimator](https://github.com/RiskLabAI/RiskLabAI.py/blob/v3.2.0/src/RiskLabAI/features/microstructural_features/edge.py#L42){:target="_blank"} (EDGE)
- library | Shares similar logic as RiskLabAI's [corwin_schultz_estimator](https://github.com/RiskLabAI/RiskLabAI.py/blob/v3.2.0/src/RiskLabAI/features/microstructural_features/corwin_schultz.py#L106){:target="_blank"} (Corwin-Schultz)

**Args:**

- <u>period (str, optional):</u> The period to estimate the spread over. Options are: "weekly", "monthly",
"quarterly", "yearly". Defaults to "monthly", as in the papers.
- <u>rolling (int, optional):</u> Estimate the spread from the pairs of the last `rolling` periods together
(method="edge"), or average the two-day spreads of the last `rolling` periods
(method="corwin_schultz" and "abdi_ranaldo"), instead of one period (e.g. period='monthly' and
rolling=3 for a three-month spread at every month end). Defaults to None.
- <u>method (str, optional):</u> The estimator. Options are: "edge" (Ardia, Guidotti and Kroencke, from the
Open, High, Low and Close), "corwin_schultz" (from the High and Low), "abdi_ranaldo" (from the
Close, High and Low). Defaults to "edge".
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

- The method uses the daily prices (split-adjusted) of each asset on its own trading days: a day on
which only another ticker or the benchmark traded is not part of a pair, so the pair is always two
consecutive trading days of the asset.
- Both days of a pair fall within the period; a pair across two periods is left out, also in a
rolling window.
- A day with a price of 0 or below (a bad bar) is left out.
- For the EDGE spread, a period with fewer than two pairs with a price change, or in which the Open
(or the previous Close) equals both the High and the Low on every pair with a price change (only
single-price days), is NaN. The estimate follows the equations of the authors' `bidask` package
(`edge` on the days of the period, with negative squared spreads set to 0).
- For the Abdi-Ranaldo spread, averaging the square roots of the two-day estimates lowers the level
when the daily volatility is large relative to the spread (in simulations with a 1% spread and a 1%
daily volatility the estimate is about 0.8%). The paper accepts this for the closer correlation
with the effective spread from trade and quote data; the EDGE spread has no such bias.
- Abdi and Ranaldo discard months with fewer than 12 applicable days; no such minimum is applied
here, as for the Corwin-Schultz spread, so a period with a single pair has an estimate.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["SNAP", "ETSY", "LYFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-06-30",
)

toolkit.risk.get_bid_ask_spread()
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

## get_bekker_parkinson_volatility
Calculate the Bekker-Parkinson Volatility per asset and period: the volatility in the daily High/Low range once the bid-ask spread of Corwin and Schultz (2012) is taken out.

The daily High is almost always a trade at the ask and the daily Low one at the bid, so the range of a day holds both the volatility and the spread, and a range-based volatility such as Parkinson's overstates the volatility of an asset with a wide spread. Corwin and Schultz write the expected squared range of one day and of two days in terms of the spread and the volatility; the spread part does not grow with the length of the window while the volatility part does. Solving the two equations for the spread gives the Corwin-Schultz spread (`get_bid_ask_spread`), and solving them for the volatility gives this estimate, as López de Prado (2018, section 19.3.4 and snippet 19.2) does; RiskLabAI names it the Bekker-Parkinson volatility.

The formula is as follows:

$$
\beta = \left[\ln\left(\frac{H_{t}}{L_{t}}\right)\right]^{2} + \left[\ln\left(\frac{H_{t+1}}{L_{t+1}}\right)\right]^{2}
$$

$$
\gamma = \left[\ln\left(\frac{\max(H_{t},\; H_{t+1})}{\min(L_{t},\; L_{t+1})}\right)\right]^{2}
$$

$$
k_{2} = \sqrt{\frac{8}{\pi}}
$$

$$
\sigma_{t} = \max\left(\frac{\sqrt{\frac{\beta}{2}} - \sqrt{\beta}}{k_{2} \cdot (3 - 2 \sqrt{2})} + \sqrt{\frac{\gamma}{k_{2}^{2} \cdot (3 - 2 \sqrt{2})}},\; 0\right)
$$

$$
\text{Bekker-Parkinson Volatility} = \operatorname{Mean}(\sigma_{t} \;\text{within the period}) \cdot \sqrt{\text{Trading Days per Period}}
$$

Where H and L are the daily High and Low of two consecutive trading days t and t+1 of the asset, with the overnight adjustment of day t+1 of the Corwin-Schultz spread. $$\sigma_{t}$$ is the volatility of the log price (continuously compounded) over one day; the mean is scaled to the period as the Parkinson Volatility of `get_volatility` is, by the square root of the trading days per period (252 / 12 for monthly, or 365 / 12 for a ticker that trades on weekends).

**Also known as:** Corwin-Schultz volatility, spread-adjusted high-low volatility.

**References:**

- paper | Corwin, S. A., & Schultz, P. (2012). "A Simple Way to Estimate Bid-Ask Spreads from Daily High and Low Prices." The Journal of Finance, 67(2), 719-760.
- paper | López de Prado, M. (2018). "Advances in Financial Machine Learning." Wiley, section 19.3.4.
- paper | Parkinson, M. (1980). "The Extreme Value Method for Estimating the Variance of the Rate of Return." Journal of Business, 53(1), 61-65.
- library | Shares similar logic as RiskLabAI's [bekker_parkinson_volatility_estimates](https://github.com/RiskLabAI/RiskLabAI.py/blob/v3.2.0/src/RiskLabAI/features/microstructural_features/bekker_parkinson_volatility_estimator.py#L51){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The period to estimate the volatility over and scale to. Options are:
"weekly", "monthly", "quarterly", "yearly". Defaults to "monthly", as for the Corwin-Schultz spread.
- <u>rolling (int, optional):</u> Average the two-day volatilities of the last `rolling` periods instead of
one period (e.g. period='monthly' and rolling=3 for a three-month estimate at every month end).
Defaults to None.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the volatility over time. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The volatility as a decimal, with the periods as the index and the assets as columns.

**Notes:**

- The pairs are those of the Corwin-Schultz spread: consecutive trading days of the asset of which both
fall within the period, without days with a price of 0 or below.
- A two-day volatility below zero (the range over both days is narrow relative to the single days) is
set to 0 before the average is taken, as in López de Prado's snippet 19.2.
- RiskLabAI's `bekker_parkinson_volatility_estimates` averages $$\beta$$ over a rolling window of days but takes
$$\gamma$$ of the last pair only, and does not adjust for the overnight return. Here $$\sigma$$ is taken per pair and
averaged per period, as the Corwin-Schultz spread is; per pair the two use the same formula.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["SNAP", "ETSY", "LYFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-06-30",
)

toolkit.risk.get_bekker_parkinson_volatility()
```

Which returns:

| Date    |   SNAP |   ETSY |   LYFT |   Benchmark |
|:--------|-------:|-------:|-------:|------------:|
| 2025-01 | 0.1554 | 0.1103 | 0.1333 |      0.03   |
| 2025-02 | 0.1062 | 0.1188 | 0.1899 |      0.0311 |
| 2025-03 | 0.1375 | 0.1276 | 0.1383 |      0.0458 |
| 2025-04 | 0.1692 | 0.1336 | 0.1422 |      0.0851 |
| 2025-05 | 0.1086 | 0.1143 | 0.1353 |      0.0319 |
| 2025-06 | 0.1184 | 0.1271 | 0.0643 |      0.0236 |

---

## get_share_turnover
Calculate the Share Turnover per asset and period: the number of shares traded relative to the number of shares outstanding, high for a liquid asset.

Datar, Naik and Radcliffe (1998) use the turnover as a liquidity proxy: a share that changes hands often can be traded at a lower cost. They find that stocks with a lower turnover earn higher returns, also after controlling for size, the book-to-market ratio and the market beta. The turnover of a period is the share of the outstanding shares that was traded in it, the sum of the daily turnover within the period.

The paper measures the turnover per month and averages it over the three months before the month of the returns, which a rolling window of 3 gives with the default monthly period. A turnover of 0.1 means that 10% of the shares outstanding changed hands; a value above 1 means more shares were traded than there are outstanding.

The formula is as follows:

$$
\text{Daily Turnover} = \frac{\text{Volume}_{t}}{\text{Weighted Average Shares}_{t}}
$$

$$
\text{Share Turnover} = \sum(\text{Daily Turnover within the period})
$$

Where Volume is the number of shares traded on day t and Weighted Average Shares the number of shares of the last fiscal period that ended on or before day t. With `rolling`, the result is the mean of the Share Turnover of the last `rolling` periods.

**Also known as:** turnover ratio, share turnover rate, trading turnover.

**References:**

- paper | Datar, V. T., Naik, N. Y., & Radcliffe, R. (1998). "Liquidity and Stock Returns: An Alternative Test." Journal of Financial Markets, 1(2), 203-219.

**Args:**

- <u>period (str, optional):</u> The period to sum the daily turnover over. Options are: "weekly", "monthly",
"quarterly", "yearly". Defaults to "monthly", as in the paper.
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
period (from the filing day with a point-in-time Toolkit), so a day never uses a share count that was not yet
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
Calculate the Idiosyncratic Volatility per asset and period: the volatility of the part of the returns the factors do not explain.

Ang, Hodrick, Xing and Zhang (2006) regress the daily excess returns of every stock on the Fama and French three factors within each month and take the standard deviation of the residuals. Stocks with a high idiosyncratic volatility earn strikingly low returns in the following month, the idiosyncratic volatility puzzle: a diversified investor is not exposed to this risk, so it should not be priced at all, let alone negatively. With the CAPM the regression is the market model on the excess return of the benchmark instead.

The formula is as follows (with the default Fama and French three factors):

$$
\text{Excess Return}_{t} = \alpha + \beta_{1} \cdot (\text{Mkt-RF}) \;\text{}_{t} + \beta_{2} \cdot \text{SMB}_{t} + \beta_{3} \cdot \text{HML}_{t} + \epsilon_{t}
$$

$$
\text{Idiosyncratic Volatility} = \operatorname{Std}(\epsilon_{t}) \cdot \sqrt{\text{Trading Days per Period}}
$$

And with the CAPM:

$$
\text{Excess Return}_{t} = \alpha + \beta \cdot \text{Benchmark Excess Return}_{t} + \epsilon_{t}
$$

Where the regression runs on the daily returns within the period, Std is the sample standard deviation (with n - 1 in the denominator) of the residuals and the trading days per period are 252 / 12 (monthly), 252 / 4 (quarterly) or 252 (yearly), the scaling of the Volatility of the Risk module; annualized it is √252 for every period. A period with fewer than 15 daily returns (the paper's minimum) is NaN.

**Also known as:** IVOL, idiosyncratic risk, residual volatility, specific risk.

**References:**

- paper | Ang, A., Hodrick, R. J., Xing, Y., & Zhang, X. (2006). "The Cross-Section of Volatility and Expected Returns." The Journal of Finance, 61(1), 259-299.

**Args:**

- <u>period (str, optional):</u> The period each regression runs within. Options are: "monthly", "quarterly",
"yearly". Defaults to "monthly", as in the paper.
- <u>model (str, optional):</u> The factors to regress on. Options are: "fama_french" (the Fama and French
three factors Mkt-RF, SMB and HML), "capm" (the excess return of the benchmark). Defaults to
"fama_french".
- <u>rolling (int, optional):</u> Regress on the daily returns of the last `rolling` periods instead of one
period (e.g. period='monthly' and rolling=12 for a one-year window at every month end).
Defaults to None.
- <u>annualize (bool, optional):</u> Whether to scale the daily standard deviation of the residuals to a
year (√252) instead of to the period. Defaults to False.
- <u>region (str, optional):</u> The region whose Fama and French factors to use with model="fama_french".
Options are: "United States", "Developed", "Developed ex US", "Europe", "Japan", "Asia Pacific
ex Japan", "North America". Every region's factors are U.S. dollar returns. Defaults to
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
- With the Fama and French factors, the excess return is the return minus the risk-free rate (RF) of the
Fama and French dataset, the one-month Treasury bill the factors are built with, as in the paper.
The dataset is published with a delay of a month or more, so the most recent periods are NaN.
- With the CAPM, the excess returns are taken over the risk-free rate of the Toolkit, an annually
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

## get_vpin
Calculate the Volume-Synchronized Probability of Informed Trading (VPIN) of Easley, López de Prado and O'Hara (2012) per asset and day, from daily bars: how one-sided, and thus toxic, the order flow is.

VPIN measures the toxicity of the order flow, the share of the volume that is one-sided: informed traders buy (or sell) persistently, while uninformed trading roughly balances. The volume is cut into buckets of the same size (a volume clock rather than a time clock), the volume of each bucket is split into buys and sells with the Bulk Volume Classification (a large rise is mostly buying, a day without a change half buying and half selling) and VPIN is the mean order imbalance over the last 50 buckets. A high VPIN means a one-sided market in which market makers lose to informed traders and may withdraw; the paper finds that VPIN was at its highest in the hours before the flash crash of 6 May 2010.

This is a coarse approximation of a measure designed for intraday data. The paper fills 50 buckets a day from one-minute bars, so its VPIN measures the toxicity within a day. On daily bars the finest classification is a whole day, which nets the buying and selling within it, and a bucket holds about a day of volume, so VPIN here is a slow-moving estimate of the one-sidedness of the volume over about 50 trading days. Use it to compare assets and periods, not as the published intraday VPIN or as a warning of an intraday liquidity crash.

The formula is as follows:

$$
\Delta P_{t} = P_{t} - P_{t-1}
$$

$$
V^{B_{t}} = V_{t} \cdot Z\left(\frac{\Delta P_{t}}{\sigma_{\Delta} P}\right)
$$

$$
V^{B_{\tau}} = \text{the buy volume of the volume in bucket}\; \tau,\;\; V^{S_{\tau}} = V - V^{B_{\tau}}
$$

$$
\text{VPIN} = \frac{\sum\left|V^{S_{\tau}} - V^{B_{\tau}}\right|}{n \cdot V} \;\text{over the last}\; n \;\text{buckets}
$$

Where P is the Adjusted Close and $$V_{t}$$ the Volume of day t, Z the cumulative distribution function of the standard normal distribution (or of the Student-t distribution with `degrees_of_freedom`), $$\sigma_{\Delta} P$$ the sample standard deviation (with n - 1 in the denominator) of the price changes of the last `window` days, V the volume of a bucket and n the number of `buckets`.

**Also known as:** volume-synchronized probability of informed trading, flow toxicity, order flow toxicity, bulk volume classification, BVC.

**References:**

- paper | Easley, D., López de Prado, M., & O'Hara, M. (2012). "Flow Toxicity and Liquidity in a High-Frequency World." The Review of Financial Studies, 25(5), 1457-1493.
- paper | Easley, D., López de Prado, M., & O'Hara, M. (2016). "Discerning Information from Trade Data." Journal of Financial Economics, 120(2), 269-285.
- paper | López de Prado, M. (2018). "Advances in Financial Machine Learning." Wiley, section 19.5.2.
- library | Shares similar logic as RiskLabAI's [volume_synchronized_pin](https://github.com/RiskLabAI/RiskLabAI.py/blob/v3.2.0/src/RiskLabAI/features/microstructural_features/order_flow.py#L157){:target="_blank"}

**Args:**

- <u>buckets (int, optional):</u> The number of buckets n VPIN is the mean over. Defaults to 50, as in the
paper.
- <u>window (int, optional):</u> The number of days the standard deviation of the price changes of the
classification is taken over. Defaults to 50.
- <u>degrees_of_freedom (float &#124; None, optional):</u> The degrees of freedom of a Student-t distribution for
the classification, as in Easley, López de Prado and O'Hara (2016), instead of the standard normal
distribution. Defaults to None.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: VPIN between 0 and 1, with the dates as the index and the assets as columns.

**Notes:**

- The volume of a bucket is the mean daily Volume of the asset over its first `window` days, the days
before the first one classified, so a bucket holds about a day of trading at the start of the data and the
volume clock is fixed in advance, as in the paper. Every VPIN thus uses the data up to its day only; when
the volume grows over the years, the buckets fill faster and VPIN spans fewer days.
- A day that fills more than the rest of a bucket carries its excess volume into the next bucket with its
own buy share, as in the paper, so every bucket holds the same volume.
- VPIN is updated on the day a bucket completes and kept on the days in between; it is NaN until the
first `window` days are classified and `buckets` buckets are complete, so start the Toolkit about half
a year before the first date of interest.
- The days are those the asset traded on; the Adjusted Close keeps a dividend from counting as selling.
- Every bucket holds the same volume V, so the mean imbalance of the buckets is divided by that volume.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["SNAP", "ETSY", "LYFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2024-07-01",
    end_date="2025-06-30",
)

toolkit.risk.get_vpin().tail()
```

Which returns:

| Date       |   SNAP |   ETSY |   LYFT |   Benchmark |
|:-----------|-------:|-------:|-------:|------------:|
| 2025-06-24 | 0.2988 | 0.5868 | 0.4158 |      0.2241 |
| 2025-06-25 | 0.3125 | 0.5908 | 0.4132 |      0.2323 |
| 2025-06-26 | 0.3138 | 0.6208 | 0.4149 |      0.2339 |
| 2025-06-27 | 0.3097 | 0.6293 | 0.4178 |      0.2457 |
| 2025-06-30 | 0.3153 | 0.6162 | 0.4109 |      0.2541 |

---

## get_value_at_risk
Calculate the Value at Risk (VaR) of an investment portfolio or asset's returns: the return that a period only falls below with a small probability alpha, a bad-case loss.

Value at Risk (VaR) is a risk management metric that quantifies the maximum potential loss an investment portfolio or asset may experience over a specified time horizon and confidence level. It provides insights into the downside risk associated with an investment and helps investors make informed decisions about risk tolerance.

The VaR is calculated as the quantile of the return distribution, representing the loss threshold that is only exceeded with tail probability alpha (e.g., in 5% of the periods for an alpha of 0.05, the 95% confidence level).

Value at Risk is a quantile: it says how bad a period gets at the chosen confidence level, not how bad the periods beyond it are, so two assets with the same VaR can have very different tails (see the Conditional Value at Risk for that). Historical VaR depends heavily on the window: one calm year gives a much smaller figure than a window that includes a crisis, so compare assets over the same period and confidence level. Scaling a daily VaR to a longer horizon with the square root of time assumes independent returns, which tends to understate risk when volatility clusters.

The formula is as follows (with the default historic method and an alpha of 0.05):

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

$$
\text{Kernel VaR solves mean}\left(\Phi\left(\frac{\text{VaR} - \text{Return}_{i}}{h}\right)\right) = \alpha,\;\; \text{with}\;\; h = \text{Std} \cdot \left(\frac{4}{3 \cdot n}\right)^{\frac{1}{5}}
$$

$$
\text{GARCH VaR} = \text{Mu} + \text{Volatility}_{t+1} \cdot F^{-1} (\alpha)
$$

Where z is the standard normal quantile at alpha, Std the sample standard deviation (with n - 1 in the denominator), S the sample skewness and K the sample excess kurtosis. The Student-T degrees of freedom v, Location and Scale are fitted by maximum likelihood. For the EVT VaR, u is the loss at `threshold_percentile`, xi and Scale_GPD the shape and scale of the Generalized Pareto Distribution fitted to the losses above it and p the fraction of losses above it. The kernel VaR is the alpha quantile of a Gaussian kernel density of the n returns with Silverman's bandwidth h, a smoothed historical quantile (Gourieroux, Laurent and Scaillet 2000), and $$\Phi$$ the standard normal distribution function.

The GARCH VaR is the conditional VaR of the next period: Mu is the constant mean and Volatility_(t+1) the one-step volatility forecast of the GARCH-family model `garch_method` with innovations `garch_distribution`, fitted by maximum likelihood (see `get_garch`), and $$F^{-1}$$ the quantile of the standardized innovations with their fitted Shape and Skew. It responds to the latest volatility, where the other distributions weigh every return of the period equally. With `rolling`, the model is refitted every `refit_every` returns on the `rolling` returns before it, and the value at each date is the VaR of the next period given the returns up to that date (McNeil and Frey 2000).

**Also known as:** VaR, maximum expected loss, portfolio loss risk.

**References:**

- paper | Gourieroux, C., Laurent, J.P. and Scaillet, O. (2000). "Sensitivity Analysis of Values at Risk." Journal of Empirical Finance, 7(3-4), 225-245.
- paper | Silverman, B.W. (1986). "Density Estimation for Statistics and Data Analysis." Chapman and Hall.
- paper | McNeil, A.J. and Frey, R. (2000). "Estimation of Tail-Related Risk Measures for Heteroscedastic Financial Time Series: An Extreme Value Approach." Journal of Empirical Finance, 7(3-4), 271-300.
- library | Referenced against scipy's [gaussian_kde](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.gaussian_kde.html){:target="_blank"} (kernel)
- library | Referenced against arch's [GARCH](https://bashtage.github.io/arch/univariate/generated/arch.univariate.GARCH.html){:target="_blank"} (GARCH)
- library | Shares similar logic as PerformanceAnalytics (R)'s [VaR](https://github.com/braverock/PerformanceAnalytics/blob/v2.0.4/R/VaR.R#L329){:target="_blank"} (historic, gaussian, Cornish-Fisher)
- library | Shares similar logic as empyrical's [value_at_risk](https://github.com/quantopian/empyrical/blob/0.5.5/empyrical/stats.py#L2095){:target="_blank"} (historic)
- library | Shares similar logic as quantstats' [value_at_risk](https://github.com/ranaroussi/quantstats/blob/v0.0.86/quantstats/stats.py#L2014){:target="_blank"} (gaussian)
- library | Shares similar logic as Riskfolio-Lib's [VaR_Hist](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/risk.html#RiskFunctions.VaR_Hist){:target="_blank"} (historic)
- library | Shares similar logic as skfolio's [value_at_risk](https://skfolio.org/generated/skfolio.measures.value_at_risk.html){:target="_blank"} (historic)
- library | Shares similar logic as empyrical's [gpd_risk_estimates](https://github.com/quantopian/empyrical/blob/0.5.5/empyrical/stats.py#L1675){:target="_blank"} (EVT)
- library | Shares similar logic as rugarch (R)'s [ugarchroll](https://github.com/cran/rugarch/blob/1.5-6/R/rugarch-methods.R#L1141){:target="_blank"} (rolling GARCH)

**Args:**

- <u>period (str, optional):</u> The data frequency for returns. Options are: "daily", "weekly", "monthly",
"quarterly", "yearly". Defaults to "daily".
- <u>alpha (float, optional):</u> The tail probability for the VaR calculation (e.g., 0.05 for the 95%
confidence level). Defaults to 0.05.
- <u>within_period (bool, optional):</u> Whether to calculate VaR within the specified period or for the entire
period. Thus whether to look at the VaR within a specific year (if period = 'yearly') or look at the entirety
of all years. Defaults to False. Note that this requires intraday data when period = 'daily', since a
single day only nests observations when intraday data was fetched.
- <u>rolling (int, optional):</u> The rolling window size to use for the calculation. If set, VaR is
calculated over a rolling window of this many periods across the full return history instead
of per `period` (e.g. a rolling 60-day VaR). Only available for the historic and GARCH
methods (the number of returns of every fit, at least 100); see `get_var_backtest` for a rolling, out-of-sample VaR path under the other
parametric distributions. Defaults to None.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the VaR values over time. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>method (str, optional):</u> The estimator of the VaR, a distribution or a model. Options are: "historic"
(the empirical quantile), "gaussian" (normal distribution), "cornish-fisher" (Cornish-Fisher
expansion), "studentt" (Student-T distribution), "evt" (Extreme Value Theory), "kernel" (Gaussian
kernel density), "garch" (GARCH-family model). Defaults to "historic". The parametric distributions use
the sample standard deviation; "cornish-fisher" adjusts the gaussian quantile for the skewness and
excess kurtosis of the returns (see `var_model.get_var_cornish_fisher`), "studentt" uses the
quantile of a Student-T distribution fitted by maximum likelihood and "kernel" the quantile of a
Gaussian kernel density of the returns. "garch" fits a GARCH-family model per ticker (and per period with
`within_period`), which takes one to five seconds per fit and needs at least 100 returns; a ticker
or period with fewer is NaN.
- <u>threshold_percentile (float, optional):</u> Only used with the "evt" method. The percentile
of losses above which the Generalized Pareto Distribution is fitted; `alpha` can be at most
1 - `threshold_percentile`, and a larger `alpha` gives an empty result (with a logged error).
The fit needs at least 10 losses above the threshold (about 200 returns at 0.95); a period
with fewer is NaN, with a logged warning. Defaults to 0.95.
- <u>refit_every (int, optional):</u> Only used with the "garch" method and `rolling`. The number of
returns between two fits; the fitted model filters the returns in between. Every refit after the
first starts from the previous fit and takes a fraction of a second. Defaults to 21.
- <u>garch_method (str, optional):</u> Only used with the GARCH method. The variance model of `get_garch`.
Options are: "garch" (GARCH), "gjr" (GJR-GARCH), "egarch"
(EGARCH), "igarch" (IGARCH), "aparch" (APARCH), "tgarch" (threshold GARCH), "ngarch" (nonlinear GARCH),
"avgarch" (absolute value GARCH), "nagarch" (nonlinear asymmetric GARCH), "component" (component GARCH),
"figarch" (FIGARCH). Defaults to "garch".
- <u>garch_distribution (str, optional):</u> Only used with the GARCH method. The innovation distribution.
Options are: "normal" (normal), "t" (Student-t), "skewt" (Hansen's skewed
Student-t), "skewt_fernandez_steel" (Fernández and Steel's skewed Student-t), "ged" (generalized error
distribution), "johnson_su" (Johnson's SU). Defaults to "normal".
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series: VaR values with time as the index.

**Notes:**

- The method retrieves historical return data based on the specified `period` and calculates VaR for each
asset in the Toolkit instance.
- With growth, the method calculates the growth of VaR values using the specified `lag`.
- The kernel VaR equals the quantile of scipy's gaussian_kde with Silverman's bandwidth. It differs
from PerformanceAnalytics' kernel VaR, which is the kernel estimator of the component VaR of
Epperlein and Smillie (2006) and is not defined for a single asset.

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
Calculate the Conditional Value at Risk (CVaR) of an investment portfolio or asset's returns: the average return in the worst alpha share of the periods, how bad the bad cases are.

Conditional Value at Risk (CVaR) is a risk management metric that quantifies the loss in the worst % of cases of an investment portfolio or asset may experience over a specified time horizon and confidence level. It provides insights into the downside risk associated with an investment and helps investors make informed decisions about risk tolerance.

The CVaR is calculated as the expected loss given that the loss threshold (VaR) with a given confidence level (e.g., 5% for an alpha of 0.05) is exceeded.

The Conditional Value at Risk (expected shortfall) is the measure banks report for market risk under the Basel framework, at 97.5% rather than 95% confidence, because unlike VaR it accounts for the size of the losses in the tail and never penalises diversification (it is subadditive). With daily data the estimate rests on few observations (one year at 95% leaves about 12 days in the tail), so a single extreme day can move it a lot; a longer window or a parametric distribution gives a steadier figure.

The formula is as follows (with the default historic method and an alpha of 0.05):

$$
\text{CVaR} = \operatorname{Mean}(\text{Returns} \mid \text{Returns} \leq \text{VaR})
$$

$$
\text{VaR} = \operatorname{Quantile}(\text{Returns},\; \alpha)
$$

The quantile interpolates linearly and the CVaR is reported as a return (negative for a loss). The other distributions use closed forms, with Std the sample standard deviation (with n - 1 in the denominator) and $$z_{\alpha}$$ the standard normal quantile at alpha:

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

$$
\text{Kernel CVaR} = \frac{\operatorname{mean}(\text{Return}_{i} \cdot \Phi(u_{i}) - h \cdot \phi(u_{i}))}{\alpha},\;\; \text{with}\;\; u_{i} = \frac{\text{VaR}_{\text{kernel}} - \text{Return}_{i}}{h}
$$

$$
\text{GARCH CVaR} = \text{Mu} + \text{Volatility}_{t+1} \cdot E\left[z \mid z \leq F^{-1} (\alpha)\right]
$$

Where the Student-T v, Location and Scale are fitted by maximum likelihood (NaN for v <= 1), $$z_{\text{cf}}$$ is the Cornish-Fisher quantile of `get_value_at_risk`, and u, xi, Scale_GPD and $$\text{VaR}_{\text{loss}}$$ are the loss threshold, the fitted Generalized Pareto shape and scale and the EVT VaR as a positive loss (NaN for xi >= 1). The kernel CVaR is the mean return below the kernel VaR of `get_value_at_risk` under a Gaussian kernel density of the returns with Silverman's bandwidth $$h = \operatorname{Std}$$ * (4 / (3 * n))^(1/5) (Scaillet 2004), with $$\Phi$$ and $$\phi$$ the standard normal distribution and density. The GARCH CVaR is the conditional CVaR of the next period, with Mu, Volatility_(t+1) and the standardized innovations z with distribution function F of the GARCH VaR of `get_value_at_risk` (McNeil and Frey 2000).

With a list of tail probabilities in `alpha`, the result is the Weighted Conditional Value at Risk, the weighted sum of the CVaR at each of them:

$$
\text{Weighted CVaR} = \Sigma_{k} \;\text{Weight}_{k} \cdot \operatorname{CVaR}(\alpha_{k})
$$

With non-negative weights that sum to 1 this is a spectral risk measure (Acerbi 2002): it weighs the worst returns more than the CVaR at the largest alpha does, and any weighting of the tail can be built from enough tail probabilities. Each CVaR uses the chosen method.

**Also known as:** CVaR, expected shortfall, ES, tail risk, weighted CVaR, WCVaR, spectral risk measure.

**References:**

- paper | Acerbi, C. (2002). "Spectral Measures of Risk: A Coherent Representation of Subjective Risk Aversion." Journal of Banking & Finance, 26(7), 1505-1518.
- paper | Cajas, D. (2021). "OWA Portfolio Optimization: A Disciplined Convex Programming Framework." SSRN Electronic Journal.
- paper | McNeil, A.J. and Frey, R. (2000). "Estimation of Tail-Related Risk Measures for Heteroscedastic Financial Time Series: An Extreme Value Approach." Journal of Empirical Finance, 7(3-4), 271-300.
- paper | Scaillet, O. (2004). "Nonparametric Estimation and Sensitivity Analysis of Expected Shortfall." Mathematical Finance, 14(1), 115-129.
- library | Referenced against scipy's [gaussian_kde](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.gaussian_kde.html){:target="_blank"} (kernel)
- library | Shares similar logic as PerformanceAnalytics (R)'s [ES](https://github.com/braverock/PerformanceAnalytics/blob/v2.0.4/R/ES.R#L245){:target="_blank"} (historic, gaussian, Cornish-Fisher)
- library | Shares similar logic as empyrical's [conditional_value_at_risk](https://github.com/quantopian/empyrical/blob/0.5.5/empyrical/stats.py#L2115){:target="_blank"} (historic)
- library | Shares similar logic as quantstats' [conditional_value_at_risk](https://github.com/ranaroussi/quantstats/blob/v0.0.86/quantstats/stats.py#L2086){:target="_blank"} (historic)
- library | Shares similar logic as Riskfolio-Lib's [CVaR_Hist](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/risk.html#RiskFunctions.CVaR_Hist){:target="_blank"} (historic)
- library | Shares similar logic as skfolio's [cvar](https://skfolio.org/generated/skfolio.measures.cvar.html){:target="_blank"} (historic)
- library | Shares similar logic as empyrical's [gpd_risk_estimates](https://github.com/quantopian/empyrical/blob/0.5.5/empyrical/stats.py#L1675){:target="_blank"} (EVT)
- library | Shares similar logic as Riskfolio-Lib's [owa_wcvar](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/auxiliary.html#OwaWeights.owa_wcvar){:target="_blank"} (Weighted CVaR)

**Args:**

- <u>period (str, optional):</u> The data frequency for returns. Options are: "daily", "weekly", "monthly",
"quarterly", "yearly". Defaults to "daily".
- <u>alpha (float &#124; list[float], optional):</u> The tail probability for the CVaR calculation (e.g., 0.05 for
the 95% confidence level), or a list of them for the Weighted CVaR. Defaults to 0.05.
- <u>within_period (bool, optional):</u> Whether to calculate CVaR within the specified period or for the entire
period. Thus whether to look at the CVaR within a specific year (if period = 'yearly') or look at the entirety
of all years. Defaults to False. Note that this requires intraday data when period = 'daily', since a
single day only nests observations when intraday data was fetched.
- <u>rolling (int, optional):</u> The rolling window size to use for the calculation. If set, CVaR is
calculated over a rolling window of this many periods across the full return history instead
of per `period` (e.g. a rolling 60-day CVaR). Only available for the historic and GARCH
methods (the number of returns of every fit, at least 100); see `get_acerbi_szekely_test` for a rolling, out-of-sample CVaR path under the
other parametric distributions. Defaults to None.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the CVaR values over time. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>method (str, optional):</u> The estimator of the CVaR, a distribution or a model. Options are: "historic"
(the empirical tail average), "gaussian" (normal distribution), "studentt" (Student-T distribution),
"laplace" (Laplace distribution), "logistic" (logistic distribution), "cornish-fisher" (Cornish-Fisher
expansion), "evt" (Extreme Value Theory), "kernel" (Gaussian kernel density), "garch" (GARCH-family
model). Defaults to "historic". "garch" fits a GARCH-family
model per ticker (and per period with `within_period`), see `get_value_at_risk`.
- <u>threshold_percentile (float, optional):</u> Only used with the "evt" method. The percentile
of losses above which the Generalized Pareto Distribution is fitted; `alpha` can be at most
1 - `threshold_percentile`, and a larger `alpha` gives an empty result (with a logged error).
The fit needs at least 10 losses above the threshold (about 200 returns at 0.95); a period
with fewer is NaN, with a logged warning. Defaults to 0.95.
- <u>alpha_weights (list[float] &#124; None, optional):</u> The weight of the CVaR at each tail probability in `alpha`,
non-negative and summing to 1. Defaults to None, which weighs every tail probability equally.
- <u>refit_every (int, optional):</u> Only used with the "garch" method and `rolling`. The number of
returns between two fits. Defaults to 21.
- <u>garch_method (str, optional):</u> Only used with the GARCH method. The variance model of `get_garch`.
Options are: "garch" (GARCH), "gjr" (GJR-GARCH), "egarch"
(EGARCH), "igarch" (IGARCH), "aparch" (APARCH), "tgarch" (threshold GARCH), "ngarch" (nonlinear GARCH),
"avgarch" (absolute value GARCH), "nagarch" (nonlinear asymmetric GARCH), "component" (component GARCH),
"figarch" (FIGARCH). Defaults to "garch".
- <u>garch_distribution (str, optional):</u> Only used with the GARCH method. The innovation distribution.
Options are: "normal" (normal), "t" (Student-t), "skewt" (Hansen's skewed
Student-t), "skewt_fernandez_steel" (Fernández and Steel's skewed Student-t), "ged" (generalized error
distribution), "johnson_su" (Johnson's SU). Defaults to "normal".
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series: CVaR values with time as the index.

**Notes:**

- The method retrieves historical return data based on the specified `period` and calculates CVaR for each
asset in the Toolkit instance.
- With growth, the method calculates the growth of CVaR values using the specified `lag`.
- Riskfolio-Lib's Weighted CVaR applies the ordered weighted average weights of its CVaR, the exact
tail average of Rockafellar and Uryasev (2002) that counts the return at the boundary with a fraction,
where the historic CVaR here averages the returns up to the interpolated quantile; the weighted sum is
the same, so the two differ by the difference of the CVaR estimators. Riskfolio-Lib reports the loss
as a positive number, the Toolkit as a return.
- The kernel CVaR equals the mean below the quantile of scipy's gaussian_kde with Silverman's
bandwidth. PerformanceAnalytics' kernel ES is defined for the component
Expected Shortfall of a portfolio only.

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
Calculate the Entropic Value at Risk (EVaR) of an investment portfolio or asset's returns: an upper bound on the VaR and CVaR from the Chernoff inequality, the most conservative of the three.

Entropic Value at Risk (EVaR) is a risk management metric that quantifies upper bound for the value at risk (VaR) and the conditional value at risk (CVaR) over a specified time horizon and confidence level. EVaR is obtained from the Chernoff inequality. It provides insights into the downside risk associated with an investment and helps investors make informed decisions about risk tolerance.

By default the EVaR is calculated under the assumption that returns are normally distributed, for which the Chernoff bound has a closed form. The historic method uses the empirical moment generating function of the returns instead, so it reflects their skewness and fat tails and always lies between the historical CVaR and the worst return.

The formula is as follows (with the default gaussian method and an alpha of 0.05):

$$
\text{EVaR} = \text{Mean} - \text{Std} \cdot \sqrt{- 2 \cdot \ln(\alpha)}
$$

Where alpha is the tail probability (0.05 for the 95% confidence level) and Std the sample standard deviation (with n - 1 in the denominator). It is an upper bound of the gaussian VaR and CVaR at the same confidence level. Since it only uses the mean and the standard deviation of the returns, it does not reflect their skewness or fat tails, and at high confidence levels it can be less severe than the historical CVaR of an asset with heavy tails. With the historic method:

$$
\text{EVaR} = - \text{inf over}\; z > 0 \;\text{of}\; z \cdot \ln\left(\frac{\operatorname{mean}\left(\exp\left(- \frac{\text{Return}_{i}}{z}\right)\right)}{\alpha}\right)
$$

Where z is the risk aversion of the entropic risk measure (see `get_entropic_risk_measure`), the bound is minimized over it numerically (on the logarithm of 1 / z, with scipy's brentq) and the mean runs over the n returns. When the worst return holds a share of the returns of at least alpha (for instance fewer than 20 returns at an alpha of 0.05), the EVaR is that worst return.

**Also known as:** EVaR, historical EVaR, entropic VaR, Chernoff bound.

**References:**

- paper | Ahmadi-Javid, A. (2012). "Entropic Value-at-Risk: A New Coherent Risk Measure." Journal of Optimization Theory and Applications, 155(3), 1105-1123.
- library | Referenced against skfolio's [evar](https://skfolio.org/generated/skfolio.measures.evar.html){:target="_blank"} (historic)
- library | Referenced against Riskfolio-Lib's [EVaR_Hist](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/risk.html#RiskFunctions.EVaR_Hist){:target="_blank"} (historic)

**Args:**

- <u>period (str, optional):</u> The data frequency for returns. Options are: "daily", "weekly", "monthly",
"quarterly", "yearly". Defaults to "daily".
- <u>alpha (float, optional):</u> The tail probability for the EVaR calculation (e.g., 0.05 for the 95%
confidence level). Defaults to 0.05.
- <u>within_period (bool, optional):</u> Whether to calculate EVaR within the specified period or for the entire
period. Thus whether to look at the EVaR within a specific year (if period = 'yearly') or look at the entirety
of all years. Defaults to False. Note that this requires intraday data when period = 'daily', since a
single day only nests observations when intraday data was fetched.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the CVaR values over time. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>method (str, optional):</u> The estimator of the EVaR. Options are: "gaussian" (the closed form of normally
distributed returns) or "historic" (the empirical moment generating function of the returns). Defaults
to "gaussian".
- <u>rolling (int, optional):</u> The rolling window size to use for the calculation. If set, EVaR is
calculated over a rolling window of this many periods across the full return history instead
of per `period`. Defaults to None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series: EVaR values with time as the index.

**Notes:**

- The method retrieves historical return data based on the specified `period` and calculates EVaR for each
asset in the Toolkit instance.
- With growth, the method calculates the growth of EVaR values using the specified `lag`.
- The historic EVaR agrees with Riskfolio-Lib's EVaR_Hist and skfolio's evar, which report the loss as a
positive number; the Toolkit keeps the sign of a return, as for the VaR and CVaR.

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

## get_entropic_risk_measure
Calculate the Entropic Risk Measure (ERM) of an investment portfolio or asset's returns at a given risk aversion: the entropic bound on the tail loss of an investor with that risk aversion.

The Entropic Risk Measure is the certainty equivalent loss of an investor with exponential utility, shifted by the confidence level: by the Chernoff inequality the loss exceeds it with a probability of at most alpha, whatever the risk aversion z. The Entropic Value at Risk is its smallest value over z (the historic method of `get_entropic_value_at_risk`), so the ERM at any risk aversion is at least as severe as the historic EVaR, and equal to it at the z that minimizes it. A z close to the size of the returns (about 0.01 for daily returns) gives a value near the EVaR; a large z gives a value dominated by z * ln(1 / alpha).

The formula is as follows (with the default risk aversion of 1 and an alpha of 0.05):

$$
\text{ERM} = - z \cdot \ln\left(\frac{\operatorname{mean}\left(\exp\left(- \frac{\text{Return}_{i}}{z}\right)\right)}{\alpha}\right)
$$

Where z is the risk aversion and the mean runs over the returns. The result is a return, negative for a loss, as the VaR, CVaR and EVaR of the Toolkit are.

**Also known as:** ERM, entropic risk, exponential utility risk measure.

**References:**

- paper | Föllmer, H. and Schied, A. (2002). "Convex Measures of Risk and Trading Constraints." Finance and Stochastics, 6(4), 429-447.
- paper | Ahmadi-Javid, A. (2012). "Entropic Value-at-Risk: A New Coherent Risk Measure." Journal of Optimization Theory and Applications, 155(3), 1105-1123.
- library | Referenced against skfolio's [entropic_risk_measure](https://skfolio.org/generated/skfolio.measures.entropic_risk_measure.html){:target="_blank"}
- library | Referenced against Riskfolio-Lib's [Entropic_RM](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/risk.html#RiskFunctions.Entropic_RM){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The data frequency for returns. Options are: "daily", "weekly", "monthly",
"quarterly", "yearly". Defaults to "daily".
- <u>risk_aversion (float, optional):</u> The risk aversion z, larger than 0, in the units of the returns.
Defaults to 1, the default of Riskfolio-Lib and skfolio.
- <u>alpha (float, optional):</u> The tail probability (e.g., 0.05 for the 95% confidence level).
Defaults to 0.05.
- <u>within_period (bool, optional):</u> Whether to calculate the ERM within the specified period or for the
entire period. Thus whether to look at the ERM within a specific year (if period = 'yearly') or look at
the entirety of all years. Defaults to False. Note that this requires intraday data when period =
'daily', since a single day only nests observations when intraday data was fetched.
- <u>rolling (int, optional):</u> The rolling window size to use for the calculation. If set, the ERM is
calculated over a rolling window of this many periods across the full return history instead
of per `period`. Defaults to None.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the ERM values over time. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series &#124; pd.DataFrame: ERM values, per ticker, or per period (or date) and ticker.

**Notes:**

- The method retrieves historical return data based on the specified `period` and calculates the ERM
for each asset in the Toolkit instance, each on its own returns.
- With growth, the method calculates the growth of ERM values using the specified `lag`.
- Equals Riskfolio-Lib's Entropic_RM and skfolio's entropic_risk_measure, which report the loss as a
positive number; the Toolkit keeps the sign of a return. The exponential average is taken in log
space (logsumexp), so a small risk aversion does not overflow.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["GLD", "SLV", "USO"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_entropic_risk_measure(period="yearly", within_period=True, risk_aversion=0.01)
```

Which returns:

|      |     GLD |     SLV |     USO |   Benchmark |
|:-----|--------:|--------:|--------:|------------:|
| 2021 | -0.0349 | -0.0614 | -0.0871 |     -0.0326 |
| 2022 | -0.0345 | -0.0434 | -0.0922 |     -0.0423 |
| 2023 | -0.0329 | -0.0438 | -0.0502 |     -0.0323 |
| 2024 | -0.0346 | -0.0496 | -0.0448 |     -0.0329 |
| 2025 | -0.0444 | -0.0638 | -0.0612 |     -0.0429 |

---

## get_higher_moment_coherent_risk
Calculate the Higher Moment Coherent Risk (HMCR) of an investment portfolio or asset's returns: a tail loss like the CVaR that weighs the deepest losses more, by default the Coherent Second Moment (CSM).

The Conditional Value at Risk averages the losses beyond a threshold, so a loss twice as deep counts twice. The Higher Moment Coherent Risk measures those losses with a higher moment instead: of order 2 it takes the root mean square of the losses beyond the threshold, so a loss twice as deep counts four times inside the square, and the measure reacts more to fat tails than the CVaR does. It stays a coherent risk measure (Krokhmal 2007): it scales with the position, shifts with cash, rewards diversification and rises with the losses, which makes it a portfolio objective (the minimum CSM portfolio) that the variance and the VaR are not.

The formula is as follows (with the default order of 2 and an alpha of 0.05):

$$
\text{Loss} = - \text{Return}
$$

$$
\text{HMCR} = \min \;\text{over}\; \zeta \;\text{of}\; \zeta + \frac{1}{\alpha} \cdot (\operatorname{Mean}(\max(\text{Loss} - \zeta,\; 0)^{\text{order}}))^{\frac{1}{\text{order}}}
$$

Where $$\zeta$$ is a threshold (the minimum is found by bisection on the derivative, which the convexity of the objective makes increasing) and the mean runs over the n returns. With an order of 1 it is the CVaR in the minimization form of Rockafellar and Uryasev (2002). A higher order weighs the deepest losses more, so the HMCR rises with the order towards the worst return. The result is a return, negative for a loss, as the VaR, CVaR and EVaR of the Toolkit are.

**Also known as:** HMCR, Coherent Second Moment, CSM, higher moment risk, second moment coherent risk.

**References:**

- paper | Krokhmal, P.A. (2007). "Higher Moment Coherent Risk Measures." Quantitative Finance, 7(4), 373-387.
- paper | Rockafellar, R.T. and Uryasev, S. (2002). "Conditional Value-at-Risk for General Loss Distributions." Journal of Banking & Finance, 26(7), 1443-1471.
- library | Shares similar logic as PortfolioAnalytics (R)'s [extract_risk](https://github.com/cran/PortfolioAnalytics/blob/2.1.2/R/extractrisk.R#L22){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The data frequency for returns. Options are: "daily", "weekly", "monthly",
"quarterly", "yearly". Defaults to "daily".
- <u>order (float, optional):</u> The order p of the moment, at least 1. Defaults to 2.
- <u>alpha (float, optional):</u> The tail probability (e.g., 0.05 for the 95% confidence level).
Defaults to 0.05.
- <u>within_period (bool, optional):</u> Whether to calculate the HMCR within the specified period or for the
entire period. Thus whether to look at the HMCR within a specific year (if period = 'yearly') or look at
the entirety of all years. Defaults to False. Note that this requires intraday data when period =
'daily', since a single day only nests observations when intraday data was fetched.
- <u>rolling (int, optional):</u> The rolling window size to use for the calculation. If set, the HMCR is
calculated over a rolling window of this many periods across the full return history instead
of per `period`. Defaults to None.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the HMCR values over time. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series &#124; pd.DataFrame: HMCR values, per ticker, or per period (or date) and ticker.

**Notes:**

- The method retrieves historical return data based on the specified `period` and calculates the HMCR
for each asset in the Toolkit instance, each on its own returns.
- With growth, the method calculates the growth of HMCR values using the specified `lag`.
- The HMCR of order 1 is the exact tail average of Rockafellar and Uryasev (2002), which counts the
return at the boundary with a fraction; `get_conditional_value_at_risk` averages the returns up to the
interpolated quantile, so the two differ slightly.
- The objective follows Krokhmal (2007), with the moment as a mean over the n returns. PortfolioAnalytics'
CSM objective takes the Euclidean norm of the excess losses without the factor 1 / SQRT(n), which makes it
grow with the length of the sample until it equals the worst loss; the Toolkit keeps the mean, so the
measure does not depend on the number of returns.
- With n returns the minimum lies at the worst loss whenever n^(-1 / order) >= alpha, the tail then
holding less than one return's worth of the moment (for an order of 1, n <= 1 / alpha). For an order of 2
and an alpha of 0.05 that is any sample of 400 returns or fewer, so within a year of daily returns the CSM is the
worst day; use the whole history, a rolling window above 400 returns or a larger alpha.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["GLD", "SLV", "USO"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_higher_moment_coherent_risk()
```

Which returns:

|           |   Value |
|:----------|--------:|
| GLD       | -0.0511 |
| SLV       | -0.0798 |
| USO       | -0.107  |
| Benchmark | -0.052  |

---

## get_expected_quadratic_shortfall
Calculate the Expected Quadratic Shortfall (EQS) of an investment portfolio or asset's returns: the average squared loss in the worst alpha share of the periods.

Where the Conditional Value at Risk averages the worst alpha share of the returns, the Expected Quadratic Shortfall averages the worst alpha share of the squared losses, so a loss twice as deep counts four times. It is the semi-variance restricted to the tail: gains and small losses do not count. It is convex and rises with the losses, which makes it a portfolio objective that a linear program can minimize, but it is not a coherent risk measure: it is in squared returns, so doubling the position quadruples it, and adding cash does not lower it by that amount. Its square root is the root mean square of the tail losses, on the scale of the returns. For a coherent measure that weighs the tail by its second moment, see `get_higher_moment_coherent_risk` (the Coherent Second Moment).

The formula is as follows (with the default alpha of 0.05):

$$
\text{Squared Loss} = \max(- \text{Return},\; 0)^{2}
$$

$$
\text{EQS} = \min \;\text{over}\; \zeta \;\text{of}\; \zeta + \frac{1}{n \cdot \alpha} \cdot \sum \max(\text{Squared Loss} - \zeta,\; 0)
$$

Where the sum runs over the n returns. The minimum is the average of the n * alpha largest squared losses, the squared loss at the boundary counted with the fraction of it inside the tail (the Conditional Value at Risk of Rockafellar and Uryasev (2002) applied to the squared losses). The result is positive, in squared returns.

**Also known as:** EQS, expected squared shortfall, tail semi-variance.

**References:**

- paper | Rockafellar, R.T. and Uryasev, S. (2002). "Conditional Value-at-Risk for General Loss Distributions." Journal of Banking & Finance, 26(7), 1443-1471.
- library | Shares similar logic as PortfolioAnalytics (R)'s [extract_risk](https://github.com/cran/PortfolioAnalytics/blob/2.1.2/R/extractrisk.R#L22){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The data frequency for returns. Options are: "daily", "weekly", "monthly",
"quarterly", "yearly". Defaults to "daily".
- <u>alpha (float, optional):</u> The tail probability (e.g., 0.05 for the 95% confidence level).
Defaults to 0.05.
- <u>within_period (bool, optional):</u> Whether to calculate the EQS within the specified period or for the
entire period. Thus whether to look at the EQS within a specific year (if period = 'yearly') or look at
the entirety of all years. Defaults to False. Note that this requires intraday data when period =
'daily', since a single day only nests observations when intraday data was fetched.
- <u>rolling (int, optional):</u> The rolling window size to use for the calculation. If set, the EQS is
calculated over a rolling window of this many periods across the full return history instead
of per `period`. Defaults to None.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the EQS values over time. Defaults to False.
- <u>lag (int &#124; list[int], optional):</u> The lag to use for the growth calculation. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series &#124; pd.DataFrame: EQS values, per ticker, or per period (or date) and ticker.

**Notes:**

- The method retrieves historical return data based on the specified `period` and calculates the EQS
for each asset in the Toolkit instance, each on its own returns.
- With growth, the method calculates the growth of EQS values using the specified `lag`.
- The values are small for daily returns (a tail of 3% losses gives about 0.0009), so set `rounding`
to 6 or more decimals, or take the square root.
- PortfolioAnalytics' EQS objective squares the positive part of the portfolio returns, the gains, while
its ES and CSM objectives next to it work on the losses; the Toolkit squares the losses.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["GLD", "SLV", "USO"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_expected_quadratic_shortfall(period="yearly", within_period=True, rounding=6)
```

Which returns:

|      |      GLD |      SLV |      USO |   Benchmark |
|:-----|---------:|---------:|---------:|------------:|
| 2021 | 0.000533 | 0.00192  | 0.002941 |    0.000356 |
| 2022 | 0.000397 | 0.00117  | 0.004368 |    0.001163 |
| 2023 | 0.000303 | 0.001332 | 0.00198  |    0.000252 |
| 2024 | 0.00053  | 0.001643 | 0.001455 |    0.000389 |
| 2025 | 0.000904 | 0.002514 | 0.002213 |    0.000961 |

---

## get_marginal_value_at_risk
Calculate the Marginal Value at Risk (Marginal VaR) of each asset in a portfolio: how much the portfolio's VaR changes when the weight of that asset rises a little.

Ordinary VaR (see `get_value_at_risk`) treats each asset in isolation. Marginal VaR instead measures how much the *portfolio's* VaR would change for an infinitesimal increase in a given asset's portfolio weight - i.e. the sensitivity of portfolio risk to each holding, not the risk of the holding on its own.

The formula is as follows (with the default historic method):

$$
\text{Portfolio Return} = \sum(\text{weight}_{i} \cdot \text{Return}_{i})
$$

$$
\text{Beta}_{i} = \frac{\operatorname{Cov}(\text{Return}_{i},\; \text{Portfolio Return})}{\operatorname{Var}(\text{Portfolio Return})}
$$

$$
\text{Marginal VaR}_{i} = \text{Beta}_{i} \cdot \text{Portfolio VaR}
$$

Where the weights are normalized to sum to 1, the covariance and variance are sample estimates (with n - 1 in the denominator) on the dates all assets have a return (the returns of a date only some of them traded on are compounded into the next date all of them traded on), and Portfolio VaR is the VaR of the portfolio return under the chosen method (see `get_value_at_risk`). The beta-based sensitivity is exact for a zero-mean elliptical distribution and an approximation otherwise; the gaussian method uses the exact derivative instead, with $$z_{\alpha}$$ the standard normal quantile at alpha:

$$
\text{Gaussian Marginal VaR}_{i} = \text{Mean}_{i} + \frac{z_{\alpha} \cdot \operatorname{Cov}(\text{Return}_{i},\; \text{Portfolio Return})}{\operatorname{Std}(\text{Portfolio Return})}
$$

An asset with Beta_i > 1 contributes disproportionately to portfolio risk, while Beta_i < 1 (and especially Beta_i < 0) indicates a diversifying holding.

**Also known as:** Marginal VaR, MVaR.

**References:**

- paper | Garman, M.B. (1997). "Taking VaR to Pieces." Risk, 10(10), 70-71.
- paper | Litterman, R. (1996). "Hot Spots and Hedges." Goldman Sachs Risk Management Series.
- paper | Jorion, P. (2006). "Value at Risk: The New Benchmark for Managing Financial Risk." 3rd ed., McGraw-Hill, Chapter 7.
- library | Shares similar logic as PerformanceAnalytics (R)'s [VaR.Marginal](https://github.com/braverock/PerformanceAnalytics/blob/v2.0.4/R/VaR.Marginal.R#L1){:target="_blank"}

**Args:**

- <u>weights (dict[str, float] &#124; None, optional):</u> Portfolio weights
keyed by ticker. Normalized internally to sum to 1. Defaults to None, which
uses equal weights across every ticker in the Toolkit instance (excluding
the "Portfolio" and "Benchmark" pseudo-tickers, if present).
- <u>period (str, optional):</u> The data frequency. Options are: "daily", "weekly", "monthly", "quarterly",
"yearly". Defaults to "daily", since a whole-series estimate needs far more observations than a single
quarter or year holds.
- <u>column (str, optional):</u> The historical data column to use. Defaults to "Return".
- <u>alpha (float, optional):</u> The tail probability (e.g., 0.05 for the 95% confidence level).
Defaults to 0.05.
- <u>method (str, optional):</u> The estimator of the underlying portfolio VaR. Options are:
"historic" (historical), "gaussian" (gaussian), "cornish-fisher" (Cornish-Fisher), "studentt"
(Student-T). Defaults to "historic".
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
Calculate the Component Value at Risk (Component VaR) of each asset in a portfolio: the part of the portfolio's VaR that each holding accounts for.

Component VaR allocates total portfolio VaR across its constituent assets, such that the allocations sum exactly back to the portfolio VaR - an "Euler" (or "fully consistent") risk decomposition.

The formula is as follows (with the default historic method):

$$
\text{Component VaR}_{i} = \text{weight}_{i} \cdot \text{Marginal VaR}_{i}
$$

$$
\sum(\text{Component VaR}_{i}) = \text{Portfolio VaR}
$$

Where the weights are normalized to sum to 1 and Marginal $$\text{VaR}_{i}$$ is that of `get_marginal_value_at_risk`: Beta_i * Portfolio VaR by default, or the exact derivative with the gaussian method.

Where Marginal VaR measures each asset's risk *sensitivity*, Component VaR measures its actual *contribution* in the same units as portfolio VaR, making it directly usable to identify which holdings account for the largest share of portfolio risk.

Component VaR is the basis of risk budgeting: a holding with a 20% weight that accounts for 45% of the portfolio VaR stands out immediately, and a component with the opposite sign of the portfolio VaR marks a holding that hedges the rest. The components always add up to the portfolio VaR, but the beta-based allocation is exact only for normally (elliptically) distributed returns and an approximation for the historical distribution used by default.

**Also known as:** Component VaR, risk contribution.

**References:**

- paper | Garman, M.B. (1997). "Taking VaR to Pieces." Risk, 10(10), 70-71.
- paper | Litterman, R. (1996). "Hot Spots and Hedges." Goldman Sachs Risk Management Series.
- paper | Jorion, P. (2006). "Value at Risk: The New Benchmark for Managing Financial Risk." 3rd ed., McGraw-Hill, Chapter 7.
- library | Shares similar logic as PerformanceAnalytics (R)'s [VaR](https://github.com/braverock/PerformanceAnalytics/blob/v2.0.4/R/VaR.R#L329){:target="_blank"}
- library | Shares similar logic as Riskfolio-Lib's [Risk_Contribution](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/risk.html#RiskFunctions.Risk_Contribution){:target="_blank"}

**Args:**

- <u>weights (dict[str, float] &#124; None, optional):</u> Portfolio weights
keyed by ticker. Normalized internally to sum to 1. Defaults to None, which
uses equal weights across every ticker in the Toolkit instance (excluding
the "Portfolio" and "Benchmark" pseudo-tickers, if present).
- <u>period (str, optional):</u> The data frequency. Options are: "daily", "weekly", "monthly", "quarterly",
"yearly". Defaults to "daily", since a whole-series estimate needs far more observations than a single
quarter or year holds.
- <u>column (str, optional):</u> The historical data column to use. Defaults to "Return".
- <u>alpha (float, optional):</u> The tail probability (e.g., 0.05 for the 95% confidence level).
Defaults to 0.05.
- <u>method (str, optional):</u> The estimator of the underlying portfolio VaR. Options are:
"historic" (historical), "gaussian" (gaussian), "cornish-fisher" (Cornish-Fisher), "studentt"
(Student-T). Defaults to "historic".
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
Backtest a Value at Risk model against realized returns: whether its breaches come as often and as independently as they should.

A Value at Risk estimate is only useful if it is actually well-calibrated against reality. This method builds a rolling, out-of-sample VaR path (each VaR estimate uses only the `window` returns preceding it, never the return it is compared against) and tests it with Kupiec's Proportion of Failures test (is the overall breach rate consistent with `alpha`?), Christoffersen's independence and conditional coverage tests (are breaches spread out over time, or do they cluster together?), Christoffersen and Pelletier's duration test (does the time between breaches have no memory?), McNeil and Frey's exceedance residual test of the Expected Shortfall (are the losses beyond the VaR as large as the CVaR says?) and the tick loss, which ranks VaR models.

Regulators backtest VaR on the number of exceptions over the last 250 trading days (the Basel traffic-light approach at 99% confidence), and Kupiec's test formalises the same question. With few exceptions the test has little power, so a model that passes is not necessarily well calibrated. Clustered exceptions, which Christoffersen's and the duration test detect, are the usual failure of historical VaR when volatility rises; the GARCH method follows the volatility from day to day.

The formula is as follows (with the default historic method, an alpha of 0.05 and daily returns, for which the window is 252):

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

$$
\text{Conditional Coverage Statistic} = \text{Kupiec Statistic} + \text{Christoffersen Statistic}
$$

$$
\text{Duration Statistic} = 2 \cdot (\ln L(\hat{a},\; \hat{b}) - \ln L(a_{\text{tilde}},\; 1))
$$

$$
\text{McNeil-Frey Statistic} = \frac{\operatorname{mean}(e)}{\frac{\operatorname{std}(e)}{\sqrt{x}}},\;\; \text{with}\;\; e_{t} = \frac{\text{CVaR}_{t} - \text{Return}_{t}}{\text{Volatility}_{t}} \;\text{if Breach}_{t} = 1
$$

$$
\text{Tick Loss} = \frac{1}{n} \cdot \sum(\alpha - \text{Breach}_{t}) \cdot (\text{Return}_{t} - \text{VaR}_{t})
$$

Where n is the number of out-of-sample VaR estimates and x the number of breaches. L(pi) is the likelihood of the breach sequence with a single breach probability pi, and $$L (\pi_{01} , \pi_{11})$$ that of a first-order Markov chain in which the breach probability depends on whether the previous period was a breach. L(a, b) is the Weibull likelihood of the number of periods between breaches, with the periods before the first and after the last breach as censored durations, and $$b = 1$$ the exponential distribution of a model without memory ($$b_{\text{hat}}$$ below 1 means breaches cluster). CVaR_t is the Conditional Value at Risk of the same window and distribution and Volatility_t the standard deviation (with n - 1 in the denominator) of the window (the volatility forecast with the GARCH method); the McNeil-Frey p-value is the share of `n_bootstrap` resamples of the residuals less their mean whose statistic is at least as large (one-sided). The Kupiec and Christoffersen statistics are compared with a $$\chi^{2}$$ distribution with one degree of freedom and the conditional coverage statistic with two. The duration p-value is a Monte Carlo p-value, as Christoffersen and Pelletier (2004) use: (1 + the number of statistics at least as large) / 1,000 over 999 random orderings of the same breaches, the exact distribution under the null given the number of breaches (the $$\chi^{2}$$ distribution rejects a correct 5% VaR over 1,000 periods about 9% of the time at 5%).

With the GARCH method, $$\text{VaR}_{t} = \text{Mu}$$ + Volatility_t * $$F^{-1} (\alpha)$$ and CVaR_t = Mu + Volatility_t * $$E [z \vert z \leq F^{-1} (\alpha)]$$ come from the GARCH-family model `garch_method` with innovations `garch_distribution`, refitted every `refit_every` returns on the `window` returns before it (see `get_value_at_risk`).

**Also known as:** VaR validation, VaR backtest, POF test, conditional coverage test, duration test, exceedance residual test, quantile loss.

**References:**

- paper | Kupiec, P.H. (1995). "Techniques for Verifying the Accuracy of Risk Measurement Models." The Journal of Derivatives, 3(2), 73-84.
- paper | Christoffersen, P.F. (1998). "Evaluating Interval Forecasts." International Economic Review, 39(4), 841-862.
- paper | Christoffersen, P.F. and Pelletier, D. (2004). "Backtesting Value-at-Risk: A Duration-Based Approach." Journal of Financial Econometrics, 2(1), 84-108.
- paper | McNeil, A.J. and Frey, R. (2000). "Estimation of Tail-Related Risk Measures for Heteroscedastic Financial Time Series: An Extreme Value Approach." Journal of Empirical Finance, 7(3-4), 271-300.
- paper | González-Rivera, G., Lee, T.H. and Mishra, S. (2004). "Forecasting Volatility: A Reality Check Based on Option Pricing, Utility Function, Value-at-Risk, and Predictive Likelihood." International Journal of Forecasting, 20(4), 629-645.
- library | Shares similar logic as rugarch (R)'s [VaRTest](https://github.com/cran/rugarch/blob/1.5-6/R/rugarch-tests.R#L418){:target="_blank"} (Kupiec, Christoffersen, conditional coverage)
- library | Shares similar logic as rugarch (R)'s [VaRDurTest](https://github.com/cran/rugarch/blob/1.5-6/R/rugarch-tests.R#L469){:target="_blank"} (duration)
- library | Shares similar logic as rugarch (R)'s [ESTest](https://github.com/cran/rugarch/blob/1.5-6/R/rugarch-tests.R#L440){:target="_blank"} (McNeil-Frey)
- library | Shares similar logic as rugarch (R)'s [VaRloss](https://github.com/cran/rugarch/blob/1.5-6/R/rugarch-methods.R#L3839){:target="_blank"} (tick loss)

**Args:**

- <u>period (str, optional):</u> The data frequency for returns. Options are: "daily", "weekly", "monthly",
"quarterly", "yearly". Defaults to "daily".
- <u>method (str, optional):</u> The estimator of the rolling VaR. Options are: "historic" (the empirical
quantile), "gaussian" (normal distribution), "studentt" (Student-T distribution), "evt" (Extreme Value
Theory), "garch" (GARCH-family model). Defaults to "historic".
"studentt" and "evt" fit their distribution to every window, which takes minutes for
years of daily data, where "historic" and "gaussian" take well under a second. "garch" takes
one to five seconds for its first fit per ticker and a fraction of a second for every refit.
- <u>alpha (float, optional):</u> The tail probability for the VaR estimates (e.g., 0.05 for the 95%
confidence level). Defaults to 0.05. With "evt" it can be at most 0.05, since the Generalized
Pareto Distribution is fitted above the 95th percentile of losses; a larger `alpha` gives an
empty result (with a logged error).
- <u>window (int &#124; None, optional):</u> The rolling window (in number of return observations of
`period`) used to estimate each VaR value. Defaults to None, which uses a year of observations
with a minimum of 20 (252 daily, 52 weekly and 20 monthly, quarterly or yearly returns), and two
years with a minimum of 100 for "garch" (504 daily, 104 weekly and 100 otherwise).
- <u>test (str &#124; list[str], optional):</u> Which test(s) to run, one or a list of them. Options are: "kupiec"
(Kupiec's test), "christoffersen" (Christoffersen's independence test), "conditional_coverage"
(conditional coverage test), "duration" (duration test), "mcneil_frey" (McNeil-Frey test), "tick_loss"
(tick loss), "both" (Kupiec and Christoffersen), "all" (every test). Defaults to "both".
- <u>refit_every (int, optional):</u> Only used with the "garch" method. The number of returns between
two fits. Defaults to 21.
- <u>garch_method (str, optional):</u> Only used with the GARCH method. The variance model of `get_garch`.
Options are: "garch" (GARCH), "gjr" (GJR-GARCH), "egarch"
(EGARCH), "igarch" (IGARCH), "aparch" (APARCH), "tgarch" (threshold GARCH), "ngarch" (nonlinear GARCH),
"avgarch" (absolute value GARCH), "nagarch" (nonlinear asymmetric GARCH), "component" (component GARCH),
"figarch" (FIGARCH). Defaults to "garch".
- <u>garch_distribution (str, optional):</u> Only used with the GARCH method. The innovation distribution.
Options are: "normal" (normal), "t" (Student-t), "skewt" (Hansen's skewed
Student-t), "skewt_fernandez_steel" (Fernández and Steel's skewed Student-t), "ged" (generalized error
distribution), "johnson_su" (Johnson's SU). Defaults to "normal".
- <u>n_bootstrap (int, optional):</u> The number of bootstrap resamples of the McNeil-Frey test. Defaults
to 1000.
- <u>seed (int, optional):</u> The seed of the McNeil-Frey bootstrap. Defaults to 0.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The statistic and p-value of every requested test (named after the test), the
Weibull Shape of the duration test, the number of breaches of the McNeil-Frey test and the Tick
Loss, per asset.

**Notes:**

- The rolling VaR path is calculated over the full return history, not the `within_period` slices
used elsewhere in this module, since a meaningful rolling window generally needs more history than
a single sub-period provides. Each asset is rolled over its own available returns, so a shorter
history of one asset does not shorten the others.
- The conditional coverage statistic adds Kupiec's statistic over all n estimates and
Christoffersen's over the n - 1 transitions, as rugarch's VaRTest does.
- rugarch's ESTest tests the unscaled gaps CVaR_t - Return_t with a normal p-value; the McNeil-Frey
test here scales them by the volatility forecast and bootstraps the p-value, as in the paper. rugarch's
VaRloss smooths the breach indicator and reports the loss per period in percentage points; the Tick
Loss here is the exact average in decimals.

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
| Kupiec Statistic |   2.0936 |   1.8323 |   0.0402 |      0.1736 |
| P-Value          |   0.1479 |   0.1759 |   0.841  |      0.677  |

---

## get_acerbi_szekely_test
Backtest a Conditional Value at Risk (Expected Shortfall) model against realized returns with the Acerbi-Szekely (2014) Z2 statistic: whether the losses beyond the VaR are as severe as the CVaR predicted.

`get_var_backtest` above only backtests the VaR estimate itself -- it checks how often (and how independently) the VaR threshold is breached, but says nothing about the *severity* of the losses on those breach days, which is exactly the extra information a CVaR (Expected Shortfall) estimate is supposed to add over VaR. This method builds a rolling, out-of-sample CVaR (and VaR) path and compares the actual loss on each breach day to the CVaR that was supposed to describe the average loss on such days.

The formula is as follows (with the default historic method, an alpha of 0.05 and daily returns, for which the window is 252):

$$
Z_{2} = \frac{\sum\left(\frac{\text{Return}_{t} \cdot \text{Breach}_{t}}{\text{CVaR}_{t}}\right)}{n \cdot \alpha} - 1
$$

$$
\text{P-Value} = 1 - \Phi\left(\frac{Z_{2}}{\text{Standard Error}}\right)
$$

Where $$\text{VaR}_{t}$$ and CVaR_t are estimated from the `window` returns before t (see `get_var_backtest`), Breach_t is 1 if Return_t < $$\text{VaR}_{t}$$ and 0 otherwise, n is the number of estimates and the Standard Error is the sample standard deviation (with n - 1 in the denominator) of Z2 over `n_bootstrap` paired bootstrap resamples. Returns and CVaR are both negative, so Z2 is about 0 for a well-calibrated model and positive when the realized tail losses exceed the CVaR (the opposite sign of the paper, which counts losses as positive).

**Also known as:** Acerbi-Szekely test, ES backtest, Z2 test.

**References:**

- paper | Acerbi, C., & Szekely, B. (2014). "Back-Testing Expected Shortfall." RISK Magazine, 27(11), 76-81.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns. Options are: "daily", "weekly", "monthly",
"quarterly", "yearly". Defaults to "daily".
- <u>method (str, optional):</u> The estimator of the rolling VaR and CVaR. Options are: "historic" (the
empirical quantile), "gaussian" (normal distribution), "studentt" (Student-T distribution), "evt"
(Extreme Value Theory), "garch" (GARCH-family model). Defaults to "historic".
"studentt" and "evt" fit their distribution to every window, which takes minutes for
years of daily data, where "historic" and "gaussian" take well under a second. "garch" refits
a GARCH-family model every `refit_every` returns (see `get_var_backtest`).
- <u>alpha (float, optional):</u> The tail probability for the VaR/CVaR estimates (e.g., 0.05 for the 95%
confidence level). Defaults to 0.05. With "evt" it can be at most 0.05, since the Generalized
Pareto Distribution is fitted above the 95th percentile of losses; a larger `alpha` gives an
empty result (with a logged error).
- <u>window (int &#124; None, optional):</u> The rolling window (in number of return observations
of `period`) used to estimate each VaR/CVaR value. Defaults to None, which uses a year of
observations with a minimum of 20 (252 daily, 52 weekly and 20 monthly, quarterly or yearly
returns), and two years with a minimum of 100 for "garch".
- <u>refit_every (int, optional):</u> Only used with the "garch" method. The number of returns between
two fits. Defaults to 21.
- <u>garch_method (str, optional):</u> Only used with the GARCH method. The variance model of `get_garch`.
Options are: "garch" (GARCH), "gjr" (GJR-GARCH), "egarch"
(EGARCH), "igarch" (IGARCH), "aparch" (APARCH), "tgarch" (threshold GARCH), "ngarch" (nonlinear GARCH),
"avgarch" (absolute value GARCH), "nagarch" (nonlinear asymmetric GARCH), "component" (component GARCH),
"figarch" (FIGARCH). Defaults to "garch".
- <u>garch_distribution (str, optional):</u> Only used with the GARCH method. The innovation distribution.
Options are: "normal" (normal), "t" (Student-t), "skewt" (Hansen's skewed
Student-t), "skewt_fernandez_steel" (Fernández and Steel's skewed Student-t), "ged" (generalized error
distribution), "johnson_su" (Johnson's SU). Defaults to "normal".
- <u>n_bootstrap (int, optional):</u> The number of bootstrap resamples used to estimate the Standard
Error of Z2. Defaults to 1000.
- <u>seed (int, optional):</u> The seed for the bootstrap random number generator. Defaults to 0.
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
| Acerbi-Szekely Statistic | 0.1548 | 0.2446 | 0.1403 |      0.2268 |
| P-Value                  | 0.1685 | 0.0725 | 0.1939 |      0.0902 |

---

## get_garch
Calculate the conditional variance ($$\sigma_{t}^{2}$$) of the returns with a GARCH model: how volatile each period is expected to be given the shocks before it, as volatility clusters.

The model is a GARCH(1, 1) fitted to the returns, or one of its variants: the asymmetric GJR-GARCH(1, 1, 1) and EGARCH(1, 1), the integrated IGARCH(1, 1), the asymmetric power APARCH(1, 1) of Ding, Granger and Engle, the TGARCH, NGARCH, AVGARCH and NAGARCH sub-models of Hentschel's family GARCH, the component GARCH of Engle and Lee, the long-memory FIGARCH(1, d, 1) of Baillie, Bollerslev and Mikkelsen and the realized GARCH of Hansen, Huang and Shek. The innovations can follow a normal, Student-t, skewed Student-t, GED or Johnson SU distribution, and the returns can have a zero, constant, ARMA(1, 1), GARCH-in-mean or ARFIMA(1, d, 1) mean. Take the square root for the conditional volatility, see `get_garch_forecast` for the variance forecast beyond the last observation and `get_garch_parameters` for the fitted parameters and the fit diagnostics.

GARCH (Generalized autoregressive conditional heteroskedasticity) is stochastic model for time series, which is for instance used to model volatility clusters, stock return and inflation. It is a generalisation of the ARCH models.

GJR-GARCH extends GARCH with a leverage term that lets negative shocks (bad news) raise volatility by more than positive shocks of the same size, a well documented asymmetry in equity returns that symmetric GARCH cannot capture. EGARCH models the log of the conditional variance, which avoids having to constrain the parameters to keep the variance positive and, like GJR-GARCH, lets negative and positive shocks of the same size have a different impact on volatility.

IGARCH restricts Alpha + Beta to 1, so a shock never fades and the variance has no long-run level, as in the RiskMetrics EWMA (which also sets Omega to 0). APARCH models a power Delta of the volatility, estimated from the data, with a leverage rotation Gamma; it nests GARCH (Delta = 2, Gamma = 0), TGARCH (Delta = 1) and NGARCH (Gamma = 0). Hentschel's family GARCH measures the shock in units of the volatility, $$z_{t} = e_{t} / \sigma_{t}$$, and allows it to be shifted as well as rotated: AVGARCH is the absolute value model with both, and NAGARCH the variance model with a shift only. The component GARCH splits the variance into a long-run component $$q_{t}$$ that fades slowly (with Rho) and a short-run component that fades quickly (with Alpha + Beta).

FIGARCH lets a shock fade hyperbolically rather than by a fixed factor per period: the fractional difference D between 0 (GARCH) and 1 (IGARCH) sets how long the volatility remembers it, the long memory of the squared returns of most assets. The realized GARCH adds a second source of information on the volatility, a realized measure $$x_{t}$$ of every day, and models how it relates to the conditional variance; the Toolkit takes the daily Parkinson variance of the High and Low prices as that measure, in place of the intraday realized variance of the paper. The ARFIMA mean lets the returns themselves have a long memory, with a fractional difference between -0.5 and 0.5.

The formula is as follows:

$$
\text{GARCH:}\;\; \sigma_{t}^{2} = \Omega + \text{Alpha} \cdot r_{t-1}^{2} + \text{Beta} \cdot \sigma_{t-1}^{2},\;\; \text{with}\;\; \sigma_{1}^{2} = \Omega + (\text{Alpha} + \text{Beta}) \cdot \text{Backcast}
$$

$$
\text{GJR-GARCH:}\;\; \sigma_{t}^{2} = \Omega + (\text{Alpha} + \Gamma \cdot I_{t-1}) \cdot r_{t-1}^{2} + \text{Beta} \cdot \sigma_{t-1}^{2},\;\; \text{with}\;\; \sigma_{1}^{2} = \Omega + \left(\text{Alpha} + \frac{\Gamma}{2} + \text{Beta}\right) \cdot \text{Backcast}
$$

$$
\text{EGARCH:}\;\; \ln \sigma_{t}^{2} = \Omega + \text{Alpha} \cdot \left(\left|z_{t-1}\right| - \sqrt{\frac{2}{\pi}}\right) + \Gamma \cdot z_{t-1} + \text{Beta} \cdot \ln \sigma_{t-1}^{2},\;\; \text{with}\;\; z_{t} = \frac{r_{t}}{\sigma_{t}}\;\;\text{and}\;\; \ln \sigma_{1}^{2} = \Omega + \text{Beta} \cdot \ln(\text{Backcast})
$$

$$
\text{IGARCH:}\;\; \sigma_{t}^{2} = \Omega + \text{Alpha} \cdot e_{t-1}^{2} + (1 - \text{Alpha}) \cdot \sigma_{t-1}^{2},\;\; \text{with}\;\; \sigma_{1}^{2} = \Omega + \text{Backcast}
$$

$$
\text{APARCH:}\;\; \sigma_{t}^{\Delta} = \Omega + \text{Alpha} \cdot (\left|e_{t-1}\right| - \Gamma \cdot e_{t-1})^{\Delta} + \text{Beta} \cdot \sigma_{t-1}^{\Delta},\;\; \text{with}\;\; \sigma_{1}^{\Delta} = \Omega + (\text{Alpha} + \text{Beta}) \cdot \text{Backcast}^{\frac{\Delta}{2}}
$$

$$
\text{TGARCH:}\;\; \sigma_{t} = \Omega + \text{Alpha} \cdot (\left|e_{t-1}\right| - \Gamma \cdot e_{t-1}) + \text{Beta} \cdot \sigma_{t-1},\;\; \text{APARCH with}\; \Delta = 1
$$

$$
\text{NGARCH:}\;\; \sigma_{t}^{\Delta} = \Omega + \text{Alpha} \cdot \left|e_{t-1}\right|^{\Delta} + \text{Beta} \cdot \sigma_{t-1}^{\Delta},\;\; \text{APARCH with}\; \Gamma = 0
$$

$$
\text{AVGARCH:}\;\; \sigma_{t} = \Omega + \text{Alpha} \cdot \sigma_{t-1} \cdot (\left|z_{t-1} - \text{Shift}\right| - \Gamma \cdot (z_{t-1} - \text{Shift})) + \text{Beta} \cdot \sigma_{t-1}
$$

$$
\text{NAGARCH:}\;\; \sigma_{t}^{2} = \Omega + \text{Alpha} \cdot \sigma_{t-1}^{2} \cdot (z_{t-1} - \text{Shift})^{2} + \text{Beta} \cdot \sigma_{t-1}^{2}
$$

$$
\text{Component GARCH:}\;\; \sigma_{t}^{2} = q_{t} + \text{Alpha} \cdot (e_{t-1}^{2} - q_{t-1}) + \text{Beta} \cdot (\sigma_{t-1}^{2} - q_{t-1}),\;\; \text{with}\;\; \text{the long-run component}\; q_{t} = \Omega + \text{Rho} \cdot q_{t-1} + \Phi \cdot (e_{t-1}^{2} - \sigma_{t-1}^{2})\;\;\text{and}\;\; q_{1} = \sigma_{1}^{2} = \Omega + \text{Rho} \cdot \text{Backcast}
$$

$$
\text{FIGARCH:}\;\; \sigma_{t}^{2} = \frac{\Omega}{1 - \text{Beta}} + \sum_{k=1⟪\ldots \;\text{1000\}⟫} \lambda_{k} \cdot e_{t-k}^{2},\;\; \text{the ARCH}(\infty) \;\text{form of} \;(1 - \text{Beta}\; L) \sigma_{t}^{2} = \Omega + \left[1 - \text{Beta}\; L - (1 - \Phi L) (1 - L)^{D}\right] e_{t}^{2} \;\text{truncated at}\; \text{1,000} \;\text{lags},\;\; \text{with}\;\; \lambda_{1} = D + \Phi - \text{Beta},\;\; \frac{\text{the}\; \lambda_{k} \;\text{from the expansion of} \;(1 - \Phi L) (1 - L)^{D}}{1 - \text{Beta}\; L} \;\text{and the Backcast for every}\; e_{t-k}^{2} \;\text{before the first return}
$$

$$
\text{Realized GARCH:}\;\; \ln \sigma_{t}^{2} = \Omega + \text{Beta} \cdot \ln \sigma_{t-1}^{2} + \Gamma \cdot \ln x_{t-1}\;\;\text{and}\;\; \text{the measurement equation}\; \ln x_{t} = \Xi + \Phi \cdot \ln \sigma_{t}^{2} + \text{Tau}\; 1 \cdot z_{t} + \text{Tau}\; 2 \cdot (z_{t}^{2} - 1) + u_{t},\;\; u_{t} \sim N(0,\; \Sigma U^{2}),\;\; \text{with}\;\; x_{t} = \frac{\left(\ln\left(\frac{\text{High}_{t}}{\text{Low}_{t}}\right)\right)^{2}}{(4 \ln 2) \;\text{the daily Parkinson variance}}
$$

$$
\text{Zero mean:}\;\; e_{t} = r_{t};\;\; \text{constant mean:}\;\; e_{t} = r_{t} - \text{Mu};\;\; \text{ARMA mean:}\;\; e_{t} = r_{t} - \text{Mu} - \operatorname{AR}(1) \cdot r_{t-1} - \operatorname{MA}(1) \cdot e_{t-1} \;\text{from the second return},\;\; \text{with}\;\; e_{1} = 0 \;\text{before it};\;\; \text{GARCH-in-mean:}\;\; e_{t} = r_{t} - \text{Mu} - \Lambda \cdot \sigma_{t};\;\; \text{ARFIMA mean:}\;\; e_{t} = w_{t} - \operatorname{AR}(1) \cdot w_{t-1} - \operatorname{MA}(1) \cdot e_{t-1},\;\; \text{with}\;\; w_{t} = (1 - L)^{D(r_{t} - \text{Mu})} \;\text{over the returns from the first} \;(\text{Fractional}\; D \;\text{the}\; D \;\text{of the mean})
$$

Where $$r_{t}$$ are the returns (not demeaned), $$e_{t}$$ the residuals of the mean model (the returns themselves with the default zero mean, so $$r_{t} = e_{t}$$ in the first three lines), $$z_{t} = e_{t} / \sigma_{t}$$, $$I_{t - 1}$$ is 1 when $$r_{t - 1} < 0$$ and 0 otherwise, $$\sqrt{2 / \pi}$$ is the expected &#124;z&#124; of a standard normal shock and the Backcast is an exponentially weighted average (decay 0.94) of the first 75 squared residuals of the mean model at its starting values (the returns less their average for a constant or in-mean mean, the residuals of the least-squares AR(1) for the ARMA and ARFIMA means). The parameters maximize the log-likelihood of the innovation distribution, which for the default normal distribution means minimizing $$\sum (\ln \sigma_{t}^{2} + e_{t}^{2} / \sigma_{t}^{2})$$, under the constraints listed in `get_garch_parameters`; the log variance of EGARCH is kept within [-20, 20].

**Also known as:** GARCH, volatility clustering, conditional heteroscedasticity, GJR-GARCH, gjr garch, threshold GARCH, TGARCH, EGARCH, exponential GARCH, log-GARCH, integrated GARCH, IGARCH, asymmetric power ARCH, APARCH, power GARCH, family GARCH, fGARCH, NGARCH, nonlinear GARCH, AVGARCH, absolute value GARCH, NAGARCH, nonlinear asymmetric GARCH, component GARCH, CGARCH, GARCH-in-mean, ARCH-M, AR-GARCH, ARMA-GARCH, Student-t GARCH, skewed-t GARCH, standardized residuals, FIGARCH, fractionally integrated GARCH, long memory volatility, realized GARCH, RealGARCH, ARFIMA-GARCH, fractionally integrated ARMA.

**References:**

- paper | Bollerslev, T. (1986). "Generalized Autoregressive Conditional Heteroskedasticity." Journal of Econometrics, 31(3), 307-327.
- paper | Engle, R.F. and Bollerslev, T. (1986). "Modelling the Persistence of Conditional Variances." Econometric Reviews, 5(1), 1-50.
- paper | Ding, Z., Granger, C.W.J. and Engle, R.F. (1993). "A Long Memory Property of Stock Market Returns and a New Model." Journal of Empirical Finance, 1(1), 83-106.
- paper | Hentschel, L. (1995). "All in the Family: Nesting Symmetric and Asymmetric GARCH Models." Journal of Financial Economics, 39(1), 71-104.
- paper | Zakoian, J.M. (1994). "Threshold Heteroskedastic Models." Journal of Economic Dynamics and Control, 18(5), 931-955.
- paper | Higgins, M.L. and Bera, A.K. (1992). "A Class of Nonlinear ARCH Models." International Economic Review, 33(1), 137-158.
- paper | Engle, R.F. and Ng, V.K. (1993). "Measuring and Testing the Impact of News on Volatility." The Journal of Finance, 48(5), 1749-1778.
- paper | Engle, R.F. and Lee, G.G.J. (1999). "A Long-Run and Short-Run Component Model of Stock Return Volatility." In Cointegration, Causality and Forecasting, Oxford University Press, 475-497.
- paper | Engle, R.F., Lilien, D.M. and Robins, R.P. (1987). "Estimating Time Varying Risk Premia in the Term Structure: The ARCH-M Model." Econometrica, 55(2), 391-407.
- paper | Baillie, R.T., Bollerslev, T. and Mikkelsen, H.O. (1996). "Fractionally Integrated Generalized Autoregressive Conditional Heteroskedasticity." Journal of Econometrics, 74(1), 3-30.
- paper | Conrad, C. and Haag, B.R. (2006). "Inequality Constraints in the Fractionally Integrated GARCH Model." Journal of Financial Econometrics, 4(3), 413-449.
- paper | Hansen, P.R., Huang, Z. and Shek, H.H. (2012). "Realized GARCH: A Joint Model for Returns and Realized Measures of Volatility." Journal of Applied Econometrics, 27(6), 877-906.
- paper | Parkinson, M. (1980). "The Extreme Value Method for Estimating the Variance of the Rate of Return." Journal of Business, 53(1), 61-65.
- paper | Granger, C.W.J. and Joyeux, R. (1980). "An Introduction to Long-Memory Time Series Models and Fractional Differencing." Journal of Time Series Analysis, 1(1), 15-29.
- paper | Hosking, J.R.M. (1981). "Fractional Differencing." Biometrika, 68(1), 165-176.
- paper | Glosten, L.R., Jagannathan, R., and Runkle, D.E. (1993). "On the Relation between the Expected Value and the Volatility of the Nominal Excess Return on Stocks." The Journal of Finance, 48(5), 1779-1801.
- paper | Nelson, D.B. (1991). "Conditional Heteroskedasticity in Asset Returns: A New Approach." Econometrica, 59(2), 347-370.
- library | Referenced against arch's [GARCH](https://bashtage.github.io/arch/univariate/generated/arch.univariate.GARCH.html){:target="_blank"}
- library | Referenced against arch's [GARCH](https://bashtage.github.io/arch/univariate/generated/arch.univariate.GARCH.html){:target="_blank"} (GJR-GARCH)
- library | Referenced against arch's [EGARCH](https://bashtage.github.io/arch/univariate/generated/arch.univariate.EGARCH.html){:target="_blank"}
- library | Referenced against arch's [APARCH](https://bashtage.github.io/arch/univariate/generated/arch.univariate.APARCH.html){:target="_blank"} (APARCH, TGARCH, NGARCH)
- library | Referenced against arch's [FIGARCH](https://bashtage.github.io/arch/univariate/generated/arch.univariate.FIGARCH.html){:target="_blank"}
- library | Referenced against arch's [ARCHInMean](https://bashtage.github.io/arch/univariate/generated/arch.univariate.ARCHInMean.html){:target="_blank"} (GARCH-in-mean)
- library | Shares similar logic as rugarch (R)'s [ugarchspec](https://github.com/cran/rugarch/blob/1.5-6/R/rugarch-methods.R#L21){:target="_blank"} (sGARCH, iGARCH, apARCH, fGARCH, csGARCH, realGARCH, ARFIMA mean)
- library | Shares similar logic as rugarch (R)'s [ugarchfit](https://github.com/cran/rugarch/blob/1.5-6/R/rugarch-methods.R#L1059){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The data frequency for returns. Options are: "daily", "weekly", "monthly",
"quarterly", "yearly". Defaults to "daily".
- <u>time_steps (int, optional):</u> Time steps to calculate GARCH for. Defaults to None, which uses the length of the
returns.
- <u>optimization_t (int, optional):</u> Time steps to optimize GARCH for. It is only used if no weights are given.
Defaults to None, which uses the length of the returns.
- <u>within_period (bool, optional):</u> Whether to calculate GARCH within the specified period or for the entire
period. Thus whether to look at the GARCH within a specific year (if period = 'yearly') or look at the
entirety of all years. Defaults to False.
- <u>method (str, optional):</u> The model. Options are: "garch" (GARCH(1, 1)), "gjr" (GJR-GARCH(1, 1, 1)),
"egarch" (EGARCH(1, 1)), "igarch" (IGARCH(1, 1)), "aparch" (APARCH(1, 1)), "tgarch" (threshold GARCH),
"ngarch" (nonlinear GARCH), "avgarch" (absolute value GARCH), "nagarch" (nonlinear asymmetric GARCH),
"component" (component GARCH), "figarch" (FIGARCH(1, d, 1)), "realized" (realized GARCH(1, 1) on the
daily Parkinson variance). Defaults to "garch".
- <u>distribution (str, optional):</u> The distribution of the standardized innovations $$z_{t}$$. Options are: "normal"
(normal), "t" (Student-t, with a Shape v > 2), "skewt" (Hansen's skewed Student-t, with a Shape and a
Skew $$\lambda$$ in (-1, 1)), "skewt_fernandez_steel" (Fernández and Steel's skewed Student-t, the same
distribution with a Skew $$\xi = \sqrt{(1 + \lambda) / (1 - \lambda)}$$, as in R's rugarch), "ged" (generalized error
distribution, with a Shape v, 2 for the normal), "johnson_su" (Johnson's SU, with a Shape and a Skew).
Defaults to "normal".
- <u>mean (str, optional):</u> The mean model. Options are: "zero" (zero mean, the returns themselves are the
shocks), "constant" (constant mean Mu), "arma" (ARMA(1, 1)), "in_mean" (GARCH-in-mean, Mu + Lambda *
$$\sigma_{t}$$), "arfima" (ARFIMA(1, d, 1)). Defaults to "zero".
- <u>output (str, optional):</u> What to return. Options are: "variance" (the conditional variance $$\sigma_{t}^{2}$$),
"standardized_residuals" ($$z_{t} = e_{t} / \sigma_{t}$$, which should look like independent draws from the
chosen distribution when the model fits), "long_run_variance" (the long-run component $$q_{t}$$ of the
component GARCH). Defaults to "variance".
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
- The EGARCH fit is a deterministic multi-start search that takes far longer than the GARCH and
GJR-GARCH fits, about 45 seconds per ticker of daily returns. The AVGARCH and NAGARCH recursions and the
GARCH-in-mean filter also run step by step and take several times longer than the other models; the
realized GARCH (eight parameters) and the ARFIMA mean (a fractional difference over the whole sample in
every step of the search) take 10 to 15 seconds per ticker of ten years of daily returns, FIGARCH 2 to 5;
the others take one to a few seconds.
- The realized GARCH takes daily returns over the entire - <u>period (not within periods):</u> its realized measure is
the daily Parkinson variance, which leaves out the overnight move and so sits below the close-to-close
variance; Xi and Phi absorb that level. A day without a positive High-Low range takes the expected measure
given its return.
- FIGARCH keeps every ARCH(∞) weight non-negative, the condition of Conrad and Haag (2006) for a
non-negative variance, a wider region than the arch package's bounds (0 <= Phi <= (1 - D) / 2 and
Beta <= D + Phi); where the fit stays inside the arch bounds both agree.
- Every model other than GARCH, GJR-GARCH and EGARCH with normal innovations and a zero mean is fitted on
the returns divided by their standard deviation, which puts every parameter on a scale of about 1, and the
parameters are converted back (see `get_garch_parameters`).
- With growth, the method calculates the growth of GARCH values using the specified `lag`.

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
| 2025-12-27 |   0.0004 |    nan      |
| 2025-12-28 |   0.0004 |    nan      |
| 2025-12-29 |   0.0004 |      0.0001 |
| 2025-12-30 |   0.0004 |      0      |
| 2025-12-31 |   0.0004 |      0      |

---

## get_garch_forecast
Calculate the GARCH variance forecast ($$\sigma_{2}$$): the conditional variance a GARCH model expects for each period after the last return, as a volatility shock fades towards its long-run level.

The model is a GARCH(1, 1), or one of its variants (see `get_garch`): the asymmetric GJR-GARCH(1, 1, 1) and EGARCH(1, 1), IGARCH(1, 1), APARCH(1, 1), the TGARCH, NGARCH, AVGARCH and NAGARCH sub-models of family GARCH, the component GARCH, FIGARCH(1, d, 1) and the realized GARCH, with any of its innovation distributions and mean models.

GARCH (Generalized autoregressive conditional heteroskedasticity) is stochastic model for time series, which is for instance used to model volatility clusters, stock return and inflation. It is a generalisation of the ARCH models.

The formula is as follows:

$$
\text{GARCH:}\;\; \sigma_{n+h}^{2} = \sigma_{L}^{2} + (\sigma_{n+1}^{2} - \sigma_{L}^{2}) \cdot (\text{Alpha} + \text{Beta})^{h - 1},\;\; \text{with}\;\; \sigma_{L}^{2} = \frac{\Omega}{1 - \text{Alpha} - \text{Beta}}
$$

$$
\text{GJR-GARCH:}\;\; \sigma_{n+h}^{2} = \sigma_{L}^{2} + (\sigma_{n+1}^{2} - \sigma_{L}^{2}) \cdot \left(\text{Alpha} + \frac{\Gamma}{2} + \text{Beta}\right)^{h - 1},\;\; \text{with}\;\; \sigma_{L}^{2} = \frac{\Omega}{1 - \text{Alpha} - \frac{\Gamma}{2} - \text{Beta}}
$$

$$
\text{EGARCH:}\;\; \ln \sigma_{n+h}^{2} = L + \text{Beta}^{h - 1} \cdot (\ln \sigma_{n+1}^{2} - L),\;\; \text{with}\;\; L = \frac{\Omega}{1 - \text{Beta}}\;\;\text{and}\;\; \sigma_{n+h}^{2} = \exp(\ln \sigma_{n+h}^{2})
$$

$$
\text{IGARCH:}\;\; \sigma_{n+h}^{2} = \sigma_{n+1}^{2} + (h - 1) \cdot \Omega
$$

$$
\text{APARCH, TGARCH, NGARCH, AVGARCH and NAGARCH:}\;\; s_{n+h} = \Omega + P \cdot s_{n+h-1},\;\; \text{with}\;\; s = \sigma^{d} \;\text{the power of the model}(\Delta,\; 1 \;\text{for TGARCH and AVGARCH},\; 2 \;\text{for NAGARCH}),\;\; P \;\text{the persistence} \;(\text{see} \;\text{get\_garch\_parameters}) \;\text{and}\; \sigma_{n+h}^{2} = s_{n+h}^{\frac{2}{d}}
$$

$$
\text{Component GARCH:}\;\; \sigma_{n+h}^{2} = q_{n+h} + (\text{Alpha} + \text{Beta})^{h - 1} \cdot (\sigma_{n+1}^{2} - q_{n+1}),\;\; \text{with}\;\; q_{n+h} = \Omega + \text{Rho} \cdot q_{n+h-1}
$$

$$
\text{FIGARCH:}\;\; \sigma_{n+h}^{2} = \frac{\Omega}{1 - \text{Beta}} + \sum_{k=1⟪\ldots \;\text{1000\}⟫} \lambda_{k} \cdot E\left[e_{n+h-k}^{2}\right],\;\; \text{with the squared residuals up to the last return and the forecast variance}\; \sigma_{n+j}^{2} \;\text{in place of}\; e_{n+j}^{2} \;\text{after it}
$$

$$
\text{Realized GARCH:}\;\; \ln \sigma_{n+h}^{2} = \Omega + \Gamma \cdot \Xi + (\text{Beta} + \Gamma \cdot \Phi) \cdot \ln \sigma_{n+h-1}^{2}\;\;\text{and}\;\; \sigma_{n+h}^{2} = \exp(\ln \sigma_{n+h}^{2}),\;\; \text{the expected realized measure in place of the measure}
$$

Where n is the last observation, $$h = 1$$, ..., `forecast_steps` (10 by default) the forecast step, $$\sigma_{n + 1}^{2}$$ the one-step-ahead variance of the fitted recursion (see `get_garch`) and $$\sigma_{L}^{2}$$ the long-run variance. The leverage term of GJR-GARCH enters at its expectation, Gamma / 2, as a negative shock is as likely as a positive one; the shock terms of EGARCH drop out at their expectation of zero, so its forecast is the exponential of the expected log variance. The other models also take the shock terms at their expectation over the innovation distribution, which makes the recursion of the power of the volatility linear; transforming its forecast back, like the exponential of EGARCH, understates the expected variance somewhat (Jensen's inequality) when the power is not 2. With a skewed distribution the leverage term of GJR-GARCH enters at Gamma * $$E [z^{2} 1 (z < 0)]$$ instead of Gamma / 2, and EGARCH's shock term at Alpha * ($$E \vert z \vert - \sqrt{2 / \pi}$$). The mean model only changes the residuals the recursion runs on.

**Also known as:** volatility forecast, predicted volatility, GJR-GARCH forecast, EGARCH forecast, APARCH forecast, IGARCH forecast, component GARCH forecast.

**References:**

- paper | Finance Compact Plus Band 1, by Yvonne Seler Zimmerman and Heinz Zimmerman; ISBN: 978-3-907291-31-1
- paper | Glosten, L.R., Jagannathan, R., and Runkle, D.E. (1993). "On the Relation between the Expected Value and the Volatility of the Nominal Excess Return on Stocks." The Journal of Finance, 48(5), 1779-1801.
- paper | Nelson, D.B. (1991). "Conditional Heteroskedasticity in Asset Returns: A New Approach." Econometrica, 59(2), 347-370.
- paper | Ding, Z., Granger, C.W.J. and Engle, R.F. (1993). "A Long Memory Property of Stock Market Returns and a New Model." Journal of Empirical Finance, 1(1), 83-106.
- paper | Engle, R.F. and Lee, G.G.J. (1999). "A Long-Run and Short-Run Component Model of Stock Return Volatility." In Cointegration, Causality and Forecasting, Oxford University Press, 475-497.
- library | Referenced against arch's [GARCH](https://bashtage.github.io/arch/univariate/generated/arch.univariate.GARCH.html){:target="_blank"} (GJR-GARCH forecast)
- library | Referenced against arch's [GARCH](https://bashtage.github.io/arch/univariate/generated/arch.univariate.GARCH.html){:target="_blank"}
- library | Referenced against arch's [GARCH](https://bashtage.github.io/arch/univariate/generated/arch.univariate.GARCH.html){:target="_blank"} (GJR-GARCH)
- library | Referenced against arch's [EGARCH](https://bashtage.github.io/arch/univariate/generated/arch.univariate.EGARCH.html){:target="_blank"}
- library | Referenced against arch's [APARCH](https://bashtage.github.io/arch/univariate/generated/arch.univariate.APARCH.html){:target="_blank"} (APARCH, TGARCH, NGARCH)
- library | Referenced against arch's [FIGARCH](https://bashtage.github.io/arch/univariate/generated/arch.univariate.FIGARCH.html){:target="_blank"}
- library | Referenced against arch's [ARCHInMean](https://bashtage.github.io/arch/univariate/generated/arch.univariate.ARCHInMean.html){:target="_blank"} (GARCH-in-mean)
- library | Shares similar logic as rugarch (R)'s [ugarchforecast](https://github.com/cran/rugarch/blob/1.5-6/R/rugarch-methods.R#L1071){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The data frequency for returns. Options are: "daily", "weekly", "monthly",
"quarterly", "yearly". Defaults to "daily".
- <u>forecast_steps (int, optional):</u> Time steps to calculate GARCH and to forecast sigma_2 values for. Defaults to 10.
- <u>within_period (bool, optional):</u> Whether to calculate GARCH within each specified period or all
at once. Thus whether to look at the GARCH within each specific year (if period = 'yearly') or
look at the entirety of all years. Defaults to False.
- <u>method (str, optional):</u> The model. Options are: "garch" (GARCH(1, 1)), "gjr" (GJR-GARCH(1, 1, 1)),
"egarch" (EGARCH(1, 1)), "igarch" (IGARCH(1, 1)), "aparch" (APARCH(1, 1)), "tgarch" (threshold GARCH),
"ngarch" (nonlinear GARCH), "avgarch" (absolute value GARCH), "nagarch" (nonlinear asymmetric GARCH),
"component" (component GARCH), "figarch" (FIGARCH(1, d, 1)), "realized" (realized GARCH(1, 1) on the
daily Parkinson variance). Defaults to "garch".
- <u>distribution (str, optional):</u> The distribution of the standardized innovations $$z_{t}$$. Options are: "normal"
(normal), "t" (Student-t, with a Shape v > 2), "skewt" (Hansen's skewed Student-t, with a Shape and a
Skew $$\lambda$$ in (-1, 1)), "skewt_fernandez_steel" (Fernández and Steel's skewed Student-t, the same
distribution with a Skew $$\xi = \sqrt{(1 + \lambda) / (1 - \lambda)}$$, as in R's rugarch), "ged" (generalized error
distribution, with a Shape v, 2 for the normal), "johnson_su" (Johnson's SU, with a Shape and a Skew).
Defaults to "normal".
- <u>mean (str, optional):</u> The mean model. Options are: "zero" (zero mean, the returns themselves are the
shocks), "constant" (constant mean Mu), "arma" (ARMA(1, 1)), "in_mean" (GARCH-in-mean, Mu + Lambda *
$$\sigma_{t}$$), "arfima" (ARFIMA(1, d, 1)). Defaults to "zero".
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
- The EGARCH fit is a deterministic multi-start search that takes far longer than the GARCH and
GJR-GARCH fits, about 45 seconds per ticker of daily returns. The AVGARCH and NAGARCH recursions and the
GARCH-in-mean filter also run step by step and take several times longer than the other models; the
others take one to a few seconds per ticker of ten years of daily returns.
- Every model other than GARCH, GJR-GARCH and EGARCH with normal innovations and a zero mean is fitted on
the returns divided by their standard deviation, which puts every parameter on a scale of about 1, and the
parameters are converted back (see `get_garch_parameters`).
- With growth, the method calculates the growth of the forecasted sigma_2 values using
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
Calculate the parameters of a GARCH model fitted to the returns: how strongly volatility reacts to a shock, how long it lasts and the level it reverts to.

The model is a GARCH(1, 1), or one of its variants (see `get_garch`), fitted to the historical returns, with the estimated Omega, Alpha and Beta parameters for each asset, with the Gamma of the leverage effect for GJR-GARCH, EGARCH, APARCH, TGARCH and AVGARCH, the power Delta of APARCH and NGARCH, the Shift of AVGARCH and NAGARCH, the Rho and Phi of the long-run component of component GARCH, the Phi, D and Beta of FIGARCH, the Beta, Gamma and measurement equation (Xi, Phi, Tau 1, Tau 2, Sigma U) of the realized GARCH, the parameters of the mean model (Mu, AR(1), MA(1), Lambda, Fractional D) and the Shape and Skew of the innovation distribution. With the diagnostics, it adds the persistence, half-life and unconditional variance of the model, the log-likelihood and information criteria, and the standard and robust standard error of every parameter.

GARCH (Generalized autoregressive conditional heteroskedasticity) is a stochastic model for time series, used to model volatility clustering. A positive Gamma of GJR-GARCH, or a negative Gamma of EGARCH, indicates the presence of a leverage effect (negative shocks raise volatility by more than positive ones of the same size), which symmetric GARCH cannot represent.

The formula is as follows:

$$
\text{GARCH:}\;\; \sigma_{t}^{2} = \Omega + \text{Alpha} \cdot r_{t-1}^{2} + \text{Beta} \cdot \sigma_{t-1}^{2}
$$

$$
\text{GJR-GARCH:}\;\; \sigma_{t}^{2} = \Omega + (\text{Alpha} + \Gamma \cdot I_{t-1}) \cdot r_{t-1}^{2} + \text{Beta} \cdot \sigma_{t-1}^{2}
$$

$$
\text{EGARCH:}\;\; \ln \sigma_{t}^{2} = \Omega + \text{Alpha} \cdot \left(\left|z_{t-1}\right| - \sqrt{\frac{2}{\pi}}\right) + \Gamma \cdot z_{t-1} + \text{Beta} \cdot \ln \sigma_{t-1}^{2}
$$

$$
\text{Log-Likelihood} = - \sum\left(\ln \sigma_{t}^{2} + \frac{r_{t}^{2}}{\sigma_{t}^{2}}\right)(\text{up to constants})
$$

$$
\text{The other models:}\;\; \text{see get\_garch},\;\; \text{with}\;\; \text{Log-Likelihood} = \sum\left(\ln f(z_{t}) - \frac{\ln(\sigma_{t}^{2})}{2}\right),\;\; f \text{ the density of the standardized innovation distribution}
$$

$$
\text{Persistence} = \text{Alpha} + \text{Beta} \;(\text{GARCH}),\;\; \text{Alpha} + \Gamma \cdot E\left[z^{2} 1(z < 0)\right] + \text{Beta} \;(\text{GJR-GARCH}),\;\; \text{Beta (EGARCH), 1 (IGARCH)},\;\; \text{Alpha} \cdot E\left[(\left|z\right| - \Gamma \cdot z)^{\Delta}\right] + \text{Beta} \;(\text{APARCH},\; \text{TGARCH},\; \text{NGARCH}),\;\; \text{Alpha} \cdot E\left[(\left|z - \text{Shift}\right| - \Gamma \cdot (z - \text{Shift}))^{d}\right] + \text{Beta} \;(\text{AVGARCH},\; \text{NAGARCH}),\;\; \text{Rho (component GARCH)},\;\; 1 \;\text{for FIGARCH with}\; D > 0 (\Phi \;\text{with}\; D = 0) \;\text{or Beta} + \Gamma \cdot \Phi (\text{realized GARCH},\; \text{the persistence of the}\; \log \;\text{variance})
$$

$$
\text{Half-Life} = \frac{\ln(0.5)}{\ln(\text{Persistence})}
$$

$$
\text{Unconditional Variance} = \left(\frac{\Omega}{1 - \text{Persistence}}\right)^{\frac{2}{d}},\;\; \frac{\Omega}{1 - \text{Rho}} \;\text{for component GARCH},\;\; \exp\left(\frac{\Omega}{1 - \text{Beta}}\right) \;\text{for EGARCH},\;\; \exp\left(\frac{\Omega + \Gamma \cdot \Xi}{1 - \text{Beta} - \Gamma \cdot \Phi}\right) \;\text{for the realized GARCH and none} \;(\text{NaN}) \;\text{for IGARCH and FIGARCH with}\; D > 0
$$

$$
\text{AIC} = \frac{- 2 \;\text{LL} + 2 k}{n},\;\; \text{BIC} = \frac{- 2 \;\text{LL} + k \ln n}{n},\;\; \text{Shibata} = - \frac{2 \;\text{LL}}{n} + \ln\left(\frac{n + 2 k}{n}\right)\;\;\text{and}\;\; \text{Hannan-Quinn} = \frac{- 2 \;\text{LL} + 2 k \ln \ln n}{n}
$$

$$
\text{Standard Error} = \sqrt{\operatorname{diag}(H^{-1})}\;\;\text{and}\;\; \text{Robust Standard Error} = \sqrt{\operatorname{diag}(H^{-1} J H^{-1})}
$$

Where $$r_{t}$$ are the returns (not demeaned), $$I_{t - 1}$$ is 1 when $$r_{t - 1} < 0$$ and 0 otherwise and $$z_{t} = r_{t} / \sigma_{t}$$. The constraints are Omega, Alpha, Beta > 0 and Alpha + Beta < 1 for GARCH, Alpha + Gamma / 2 + Beta < 1 and Alpha + Gamma >= 0 for GJR-GARCH, and Omega in [-15, 5], Alpha and Gamma in [-1, 1] and &#124;Beta&#124; < 1 for EGARCH. The GARCH parameters are estimated by maximizing the Gaussian log-likelihood with L-BFGS-B, started from a domain-informed initial guess and from 32 points of a Sobol sequence, and the best fit is finished with Nelder-Mead. The search runs on the parameters scaled to their bounds, as Omega (of the order of a daily variance) and Alpha and Beta differ by orders of magnitude.

The variance recursion starts from a backcast, an exponentially weighted average (decay 0.94) of the first 75 squared returns, which stands in for both the squared return and the variance before the first observation (with the leverage term of GJR-GARCH at its expectation, Gamma / 2, and $$\ln \sigma_{1}^{2} = \text{Omega} + \text{Beta} \cdot \ln (\text{Backcast})$$ for EGARCH), and every observation enters the likelihood. This is the start the arch package uses, so the estimates agree with it.

The other models (and GARCH, GJR-GARCH and EGARCH with another distribution or mean) are fitted the same way on the returns divided by their standard deviation, with bounds for every parameter on that scale, and the parameters are converted back: Omega is multiplied by the scale to the power of the model (2, Delta, or 1 for TGARCH and AVGARCH; EGARCH's Omega gains 2 * (1 - Beta) * ln(scale)) and Mu by the scale. The constraints are a persistence below 1 (IGARCH sets Beta = 1 - Alpha), &#124;Gamma&#124; < 1 for the rotation of APARCH and family GARCH, Delta in [0.05, 4], 0 < Alpha + Beta < Rho < 1 and Phi < Beta for component GARCH, D in [0, 1], Beta in [0, 1) and every ARCH(∞) weight non-negative for FIGARCH (Conrad and Haag, 2006), Beta + Gamma * Phi < 1 for the realized GARCH, &#124;AR(1)&#124; and $$\vert \text{MA} (1) \vert < 1$$, a Fractional D in (-0.5, 0.5), a Shape in [2.05, 100] for the Student-t distributions, in [1.01, 50] for the GED and in [0.2, 20] for the Johnson SU, and a Skew in (-1, 1) for Hansen's, [0.1, 10] for Fernández and Steel's and [-10, 10] for the Johnson SU. The power models (APARCH and its sub-models) start from $$\sigma_{1}^{\text{Delta}} = \text{Omega} + (\text{Alpha} + \text{Beta}) \cdot \text{Backcast}^{\text{Delta} / 2}$$, as the arch package does, and the component model from $$q_{1} = \sigma_{1}^{2} = \text{Omega} + \text{Rho} \cdot \text{Backcast}$$. The realized GARCH divides its realized measure by the square of the scale, so Omega gains 2 * (1 - Beta - Gamma) * ln(scale) and Xi 2 * (1 - Phi) * ln(scale), and starts from $$\ln \sigma_{1}^{2} = \text{Omega} + \text{Beta} \cdot \ln (\text{Backcast}) + \text{Gamma}$$ * ln(Measure Backcast), the measure averaged like the squared returns. Its log-likelihood is the joint one of the returns and the measure (Hansen, Huang and Shek, 2012), so its information criteria do not compare with those of the other models.

The persistence is the factor by which a shock carries over to the next period on average, and the half-life the number of periods until half of it has faded. The expectations over the innovation distribution are evaluated numerically. The information criteria are per observation, as in R's rugarch, so the lowest value marks the preferred model among fits on the same returns. The standard errors come from the Hessian H of the log-likelihood and the robust ones (Bollerslev and Wooldridge, 1992) also from the outer product J of the scores of every observation, both by central finite differences; the robust ones remain valid when the innovation distribution is misspecified (quasi maximum likelihood).

Unlike `get_garch` and `get_garch_forecast`, which return a (forecasted) conditional variance path, this method returns the fitted parameters themselves. This is useful when the parameters are needed directly, for example to seed a separate volatility simulation.

For daily equity returns, the GARCH Alpha is typically between 0.05 and 0.15 and Alpha + Beta (the persistence) between 0.95 and 0.99, meaning a volatility shock fades over weeks rather than days. The long-run variance the model reverts to is Omega / (1 - Alpha - Beta). A fit far outside these ranges is a reason to check the data and the window before using the parameters.

**Also known as:** GARCH weights, GARCH coefficients, conditional variance parameters, GJR-GARCH parameters, EGARCH parameters, leverage parameters, APARCH parameters, degrees of freedom, persistence, half-life, unconditional variance, long-run variance, information criteria, GARCH standard errors.

**References:**

- paper | Finance Compact Plus Band 1, by Yvonne Seler Zimmerman and Heinz Zimmerman; ISBN: 978-3-907291-31-1
- paper | Glosten, L.R., Jagannathan, R., and Runkle, D.E. (1993). "On the Relation between the Expected Value and the Volatility of the Nominal Excess Return on Stocks." The Journal of Finance, 48(5), 1779-1801.
- paper | Nelson, D.B. (1991). "Conditional Heteroskedasticity in Asset Returns: A New Approach." Econometrica, 59(2), 347-370.
- paper | Ding, Z., Granger, C.W.J. and Engle, R.F. (1993). "A Long Memory Property of Stock Market Returns and a New Model." Journal of Empirical Finance, 1(1), 83-106.
- paper | Hentschel, L. (1995). "All in the Family: Nesting Symmetric and Asymmetric GARCH Models." Journal of Financial Economics, 39(1), 71-104.
- paper | Bollerslev, T. (1987). "A Conditionally Heteroskedastic Time Series Model for Speculative Prices and Rates of Return." The Review of Economics and Statistics, 69(3), 542-547.
- paper | Hansen, B.E. (1994). "Autoregressive Conditional Density Estimation." International Economic Review, 35(3), 705-730.
- paper | Fernández, C. and Steel, M.F.J. (1998). "On Bayesian Modeling of Fat Tails and Skewness." Journal of the American Statistical Association, 93(441), 359-371.
- paper | Johnson, N.L. (1949). "Systems of Frequency Curves Generated by Methods of Translation." Biometrika, 36(1/2), 149-176.
- paper | Bollerslev, T. and Wooldridge, J.M. (1992). "Quasi-Maximum Likelihood Estimation and Inference in Dynamic Models with Time-Varying Covariances." Econometric Reviews, 11(2), 143-172.
- library | Referenced against arch's [GARCH](https://bashtage.github.io/arch/univariate/generated/arch.univariate.GARCH.html){:target="_blank"}
- library | Referenced against arch's [GARCH](https://bashtage.github.io/arch/univariate/generated/arch.univariate.GARCH.html){:target="_blank"} (GJR-GARCH)
- library | Referenced against arch's [EGARCH](https://bashtage.github.io/arch/univariate/generated/arch.univariate.EGARCH.html){:target="_blank"}
- library | Referenced against arch's [APARCH](https://bashtage.github.io/arch/univariate/generated/arch.univariate.APARCH.html){:target="_blank"} (APARCH, TGARCH, NGARCH)
- library | Referenced against arch's [FIGARCH](https://bashtage.github.io/arch/univariate/generated/arch.univariate.FIGARCH.html){:target="_blank"}
- library | Referenced against arch's [ARCHInMean](https://bashtage.github.io/arch/univariate/generated/arch.univariate.ARCHInMean.html){:target="_blank"} (GARCH-in-mean)
- library | Referenced against arch's [GARCH](https://bashtage.github.io/arch/univariate/generated/arch.univariate.GARCH.html){:target="_blank"} (classic and robust standard errors, information criteria)
- library | Shares similar logic as rugarch (R)'s [ugarchspec](https://github.com/cran/rugarch/blob/1.5-6/R/rugarch-methods.R#L21){:target="_blank"} (sGARCH, iGARCH, apARCH, fGARCH, csGARCH, realGARCH, ARFIMA mean)
- library | Shares similar logic as rugarch (R)'s [ugarchfit](https://github.com/cran/rugarch/blob/1.5-6/R/rugarch-methods.R#L1059){:target="_blank"}
- library | Shares similar logic as rugarch (R)'s [persistence](https://github.com/cran/rugarch/blob/1.5-6/R/rugarch-methods.R#L2529){:target="_blank"}
- library | Shares similar logic as rugarch (R)'s [halflife](https://github.com/cran/rugarch/blob/1.5-6/R/rugarch-methods.R#L2490){:target="_blank"}
- library | Shares similar logic as rugarch (R)'s [uncvariance](https://github.com/cran/rugarch/blob/1.5-6/R/rugarch-methods.R#L3036){:target="_blank"}
- library | Shares similar logic as rugarch (R)'s [infocriteria](https://github.com/cran/rugarch/blob/1.5-6/R/rugarch-methods.R#L2063){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The data frequency for returns. Options are: "daily", "weekly", "monthly",
"quarterly", "yearly". Defaults to "daily".
- <u>optimization_t (int, optional):</u> Time steps of the returns series to use for the optimization.
Defaults to the full length of the returns series.
- <u>method (str, optional):</u> The model. Options are: "garch" (GARCH(1, 1)), "gjr" (GJR-GARCH(1, 1, 1)),
"egarch" (EGARCH(1, 1)), "igarch" (IGARCH(1, 1)), "aparch" (APARCH(1, 1)), "tgarch" (threshold GARCH),
"ngarch" (nonlinear GARCH), "avgarch" (absolute value GARCH), "nagarch" (nonlinear asymmetric GARCH),
"component" (component GARCH), "figarch" (FIGARCH(1, d, 1)), "realized" (realized GARCH(1, 1) on the
daily Parkinson variance). Defaults to "garch".
- <u>distribution (str, optional):</u> The distribution of the standardized innovations $$z_{t}$$. Options are: "normal"
(normal), "t" (Student-t, with a Shape v > 2), "skewt" (Hansen's skewed Student-t, with a Shape and a
Skew $$\lambda$$ in (-1, 1)), "skewt_fernandez_steel" (Fernández and Steel's skewed Student-t, the same
distribution with a Skew $$\xi = \sqrt{(1 + \lambda) / (1 - \lambda)}$$, as in R's rugarch), "ged" (generalized error
distribution, with a Shape v, 2 for the normal), "johnson_su" (Johnson's SU, with a Shape and a Skew).
Defaults to "normal".
- <u>mean (str, optional):</u> The mean model. Options are: "zero" (zero mean, the returns themselves are the
shocks), "constant" (constant mean Mu), "arma" (ARMA(1, 1)), "in_mean" (GARCH-in-mean, Mu + Lambda *
$$\sigma_{t}$$), "arfima" (ARFIMA(1, d, 1)). Defaults to "zero".
- <u>diagnostics (bool, optional):</u> Whether to add the Persistence, Half-Life (in periods), Unconditional
Variance, Log-Likelihood, AIC, BIC, Shibata and Hannan-Quinn criteria and the Standard Error and Robust
Standard Error of every parameter. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Omega, Alpha and Beta values per asset, with Gamma between Alpha and Beta for
GJR-GARCH and EGARCH, the other parameters of the model as listed above (Beta = 1 - Alpha for
IGARCH) and, with the diagnostics, the diagnostics below them.

**Notes:**

- The method retrieves historical return data based on the specified `period` and fits the model
for each asset in the Toolkit instance.
- Every asset is fitted on its own available returns, so an asset with a shorter history (or a gap)
does not shorten the sample of the others.
- GJR-GARCH nests GARCH ($$\gamma = 0$$), so its fit never ends at a lower log-likelihood than the
GARCH(1, 1) fit: if the search does, the GARCH weights with a Gamma of 0 are returned.
- EGARCH's log-variance parameterization is less constrained than plain GARCH, which makes it
prone to unstable, boundary-hugging fits on short return histories, which include quarterly
data over a few years. Prefer daily or weekly returns. Its fit is a deterministic multi-start search
that takes far longer than the others, about 45 seconds per ticker of daily returns.

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
| Alpha | 0.035851 | 0.057577 | 0.048624 |    0.153925 |
| Beta  | 0.87526  | 0.716127 | 0.940179 |    0.811124 |

---

## get_news_impact_curve
Calculate the news impact curve of Engle and Ng (1993) of a GARCH-family model fitted to the returns of each asset: how a shock of each size moves the next period's volatility, the conditional variance of the next period as a function of this period's shock, with this period's variance at the unconditional (long-run) variance of the model.

The curve shows how a model lets news move volatility. For GARCH it is a parabola that is symmetric around zero: a fall raises the next variance by as much as a rise of the same size. The asymmetric models (GJR-GARCH, EGARCH, APARCH, TGARCH, AVGARCH and NAGARCH) let it rise more steeply to the left when they find a leverage effect, so bad news raises volatility by more than good news, and the power models bend it into a different shape than a parabola.

The formula is as follows:

$$
\text{News Impact}(z) = \sigma_{t+1}^{2} \;\text{given}\; e_{t} = z \cdot \sigma\;\;\text{and}\;\; \sigma_{t}^{2} = \sigma^{2}
$$

Where z is the shock in unconditional standard deviations (-5 to 5 in steps of 0.5), $$\sigma^{2}$$ the unconditional variance of the model (see `get_garch_parameters`) and $$\sigma_{t + 1}^{2}$$ follows from the variance recursion of the model (see `get_garch`). The long-run component of component GARCH is also set to $$\sigma^{2}$$. IGARCH and FIGARCH (with D > 0) have no unconditional variance, so their curve is NaN; the curve of EGARCH is taken at exp(Omega / (1 - Beta)), the exponential of its long-run log variance. The shock of the realized GARCH moves the next log variance through its measurement equation (Hansen, Huang and Shek, 2012): News Impact(z) = exp(ln sigma^2 + Gamma * (Tau 1 * z + Tau $$2 \cdot (z^{2} - 1)$$)), with $$\sigma^{2}$$ its unconditional variance exp((Omega + Gamma * Xi) / (1 - Beta - Gamma * Phi)).

**Also known as:** news impact, leverage effect curve, asymmetric volatility response.

**References:**

- paper | Engle, R.F. and Ng, V.K. (1993). "Measuring and Testing the Impact of News on Volatility." The Journal of Finance, 48(5), 1749-1778.
- library | Shares similar logic as rugarch (R)'s [newsimpact](https://github.com/cran/rugarch/blob/1.5-6/R/rugarch-methods.R#L2287){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The data frequency for returns. Options are: "daily", "weekly", "monthly",
"quarterly", "yearly". Defaults to "daily".
- <u>method (str, optional):</u> The model. Options are: "garch" (GARCH(1, 1)), "gjr" (GJR-GARCH(1, 1, 1)),
"egarch" (EGARCH(1, 1)), "igarch" (IGARCH(1, 1)), "aparch" (APARCH(1, 1)), "tgarch" (threshold GARCH),
"ngarch" (nonlinear GARCH), "avgarch" (absolute value GARCH), "nagarch" (nonlinear asymmetric GARCH),
"component" (component GARCH), "figarch" (FIGARCH(1, d, 1)), "realized" (realized GARCH(1, 1) on the
daily Parkinson variance). Defaults to "garch".
- <u>distribution (str, optional):</u> The distribution of the standardized innovations $$z_{t}$$. Options are: "normal"
(normal), "t" (Student-t, with a Shape v > 2), "skewt" (Hansen's skewed Student-t, with a Shape and a
Skew $$\lambda$$ in (-1, 1)), "skewt_fernandez_steel" (Fernández and Steel's skewed Student-t, the same
distribution with a Skew $$\xi = \sqrt{(1 + \lambda) / (1 - \lambda)}$$, as in R's rugarch), "ged" (generalized error
distribution, with a Shape v, 2 for the normal), "johnson_su" (Johnson's SU, with a Shape and a Skew).
Defaults to "normal".
- <u>mean (str, optional):</u> The mean model. Options are: "zero" (zero mean, the returns themselves are the
shocks), "constant" (constant mean Mu), "arma" (ARMA(1, 1)), "in_mean" (GARCH-in-mean, Mu + Lambda *
$$\sigma_{t}$$), "arfima" (ARFIMA(1, d, 1)). Defaults to "zero".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The conditional variance of the next period per asset, indexed by the shock z.

**Notes:**

- Every asset is fitted on its own available returns, see `get_garch_parameters`.
- The variance is that of a single period of the chosen `period`; its square root is the volatility.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2016-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_news_impact_curve(method="gjr", rounding=6).iloc[::4]
```

Which returns:

|   Shock |     AAPL |     MSFT |   Benchmark |
|--------:|---------:|---------:|------------:|
|      -5 | 0.002689 | 0.001411 |    0.001215 |
|      -3 | 0.001218 | 0.000689 |    0.000523 |
|      -1 | 0.000483 | 0.000328 |    0.000176 |
|       1 | 0.000398 | 0.000288 |    0.000139 |
|       3 | 0.000452 | 0.000327 |    0.00019  |
|       5 | 0.000559 | 0.000404 |    0.000292 |

---

## get_garch_simulation
Calculate a GARCH simulation of each asset: the spread of the returns (or the conditional volatility) a GARCH-family model fitted to its returns expects for the periods after the last return.

The paths are summarized per period: the mean and the 5th, 25th, 50th, 75th and 95th percentiles.

Unlike `get_garch_forecast`, which gives the expected variance, the simulation shows the whole spread of outcomes the model implies, including the fat tails and skewness of the innovation distribution and the way a large shock raises the volatility of the periods after it. The percentiles of the cumulative return give a GARCH-based Value at Risk over the horizon.

The formula is as follows, for $$h = 1$$, ..., `forecast_steps`:

$$
e_{n+h} = \sigma_{n+h} \cdot z_{n+h}
$$

$$
r_{n+h} = \text{Mean}_{n+h} + e_{n+h}
$$

$$
\sigma_{n+h+1}^{2} \;\text{from the variance recursion of the model}(\text{see} \;\text{get\_garch})
$$

Where n is the last return, $$\sigma_{n + 1}^{2}$$ the one-step-ahead variance of the fitted model, z drawn from the fitted innovation distribution and Mean_(n+h) = 0, Mu, Mu + $$\text{AR} (1) \cdot r_{n + h - 1} + \text{MA} (1) \cdot e_{n + h - 1}$$ or Mu + $$\text{Lambda} \cdot \sigma_{n + h}$$ by the mean model (the last return and residual start the ARMA mean; the ARFIMA mean continues its fractional difference over every return). FIGARCH continues its sum over the squared residuals of the returns, and the realized GARCH draws its realized measure from the measurement equation with a normal error u ~ N(0, Sigma $$U^{2}$$). The cumulative return compounds the simulated returns, $$(1 + r_{n + 1}) \cdot \ldots \cdot (1 + r_{n + h}) - 1$$, treating them as simple returns.

With bootstrap fits, the bootstrap forecast density of Pascual, Romo and Ruiz (2006) replaces the fitted innovation distribution with the model's own standardized residuals and adds the uncertainty of the estimated parameters:

- z*_t drawn with replacement from the standardized residuals $$z_{t}$$ of the fit (and, for the realized GARCH, the measurement error of the same day)
- a series r*_1, ..., r*_n as long as the returns simulated from the fitted parameters with those draws, starting after the last return, and the model fitted to it again, `bootstrap_fits` times
- every refitted model filters the actual returns to its own $$\sigma_{n + 1}^{2}$$ and simulates `simulations` / `bootstrap_fits` of the paths from there with the resampled z*
- no bootstrap fits (0) keeps the fitted parameters and only resamples the residuals (the partial bootstrap)

The spread of the first period's volatility then shows the parameter uncertainty, which a simulation from the fitted parameters does not have.

**Also known as:** GARCH Monte Carlo, volatility simulation, GARCH scenarios, simulated return paths, GARCH bootstrap, bootstrap forecast density, ugarchboot, parameter uncertainty.

**References:**

- paper | Pascual, L., Romo, J. and Ruiz, E. (2006). "Bootstrap Prediction for Returns and Volatilities in GARCH Models." Computational Statistics & Data Analysis, 50(9), 2293-2312.
- library | Shares similar logic as rugarch (R)'s [ugarchsim](https://github.com/cran/rugarch/blob/1.5-6/R/rugarch-methods.R#L1090){:target="_blank"}
- library | Shares similar logic as rugarch (R)'s [ugarchpath](https://github.com/cran/rugarch/blob/1.5-6/R/rugarch-methods.R#L1105){:target="_blank"}
- library | Shares similar logic as rugarch (R)'s [ugarchboot](https://github.com/cran/rugarch/blob/1.5-6/R/rugarch-methods.R#L1210){:target="_blank"} (bootstrap forecast density)

**Args:**

- <u>period (str, optional):</u> The data frequency for returns. Options are: "daily", "weekly", "monthly",
"quarterly", "yearly". Defaults to "daily".
- <u>forecast_steps (int, optional):</u> The number of periods to simulate. Defaults to 10.
- <u>simulations (int, optional):</u> The number of simulated paths per asset. Defaults to 10,000.
- <u>seed (int &#124; None, optional):</u> The seed of the random draws, None for a different simulation every
time. Defaults to 0.
- <u>output (str, optional):</u> What to simulate. Options are: "returns" (the return of each period),
"cumulative_returns" (the compounded return from the last return to each period), "volatility" (the
conditional volatility sigma of each period). Defaults to "returns".
- <u>method (str, optional):</u> The model. Options are: "garch" (GARCH(1, 1)), "gjr" (GJR-GARCH(1, 1, 1)),
"egarch" (EGARCH(1, 1)), "igarch" (IGARCH(1, 1)), "aparch" (APARCH(1, 1)), "tgarch" (threshold GARCH),
"ngarch" (nonlinear GARCH), "avgarch" (absolute value GARCH), "nagarch" (nonlinear asymmetric GARCH),
"component" (component GARCH), "figarch" (FIGARCH(1, d, 1)), "realized" (realized GARCH(1, 1) on the
daily Parkinson variance). Defaults to "garch".
- <u>distribution (str, optional):</u> The distribution of the standardized innovations $$z_{t}$$. Options are: "normal"
(normal), "t" (Student-t, with a Shape v > 2), "skewt" (Hansen's skewed Student-t, with a Shape and a
Skew $$\lambda$$ in (-1, 1)), "skewt_fernandez_steel" (Fernández and Steel's skewed Student-t, the same
distribution with a Skew $$\xi = \sqrt{(1 + \lambda) / (1 - \lambda)}$$, as in R's rugarch), "ged" (generalized error
distribution, with a Shape v, 2 for the normal), "johnson_su" (Johnson's SU, with a Shape and a Skew).
Defaults to "normal".
- <u>mean (str, optional):</u> The mean model. Options are: "zero" (zero mean, the returns themselves are the
shocks), "constant" (constant mean Mu), "arma" (ARMA(1, 1)), "in_mean" (GARCH-in-mean, Mu + Lambda *
$$\sigma_{t}$$), "arfima" (ARFIMA(1, d, 1)). Defaults to "zero".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.
- <u>bootstrap_fits (int &#124; None, optional):</u> The number of bootstrap series the model is fitted to again
for the bootstrap forecast density of Pascual, Romo and Ruiz, 0 for the partial bootstrap that only
resamples the residuals. Defaults to None, which draws from the fitted innovation distribution.

**Returns:**

pd.DataFrame: The Mean, 5%, 25%, 50%, 75% and 95% of the simulated values per asset, indexed by the
periods after the last return.

**Notes:**

- Every asset is fitted on its own available returns, see `get_garch_parameters`.
- The paths of every asset are drawn independently of the other assets.
- Every bootstrap refit is a local search from the fitted parameters (with the multi-start search when it
starts or ends on a bound), about 0.5 seconds for GARCH(1, 1) on ten years of daily returns, several
seconds for FIGARCH, the realized GARCH and the ARFIMA mean.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2016-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_garch_simulation(
    output="cumulative_returns", distribution="t", show_columns="AAPL"
)
```

Which returns:

|            |    Mean |      5% |     25% |     50% |    75% |    95% |
|:-----------|--------:|--------:|--------:|--------:|-------:|-------:|
| 2026-01-01 |  0      | -0.0155 | -0.0054 | -0.0002 | 0.0053 | 0.0151 |
| 2026-01-02 | -0.0001 | -0.0227 | -0.0084 | -0.0001 | 0.0079 | 0.0225 |
| 2026-01-05 | -0.0002 | -0.0286 | -0.0106 | -0.0003 | 0.0102 | 0.0279 |
| 2026-01-06 | -0.0003 | -0.033  | -0.0126 | -0.0004 | 0.012  | 0.0326 |
| 2026-01-07 | -0.0003 | -0.038  | -0.0144 | -0.0002 | 0.0138 | 0.0372 |
| 2026-01-08 | -0.0002 | -0.0419 | -0.0159 | -0.0005 | 0.0152 | 0.0418 |
| 2026-01-09 | -0.0002 | -0.045  | -0.0176 | -0.0009 | 0.0167 | 0.0456 |
| 2026-01-12 | -0.0001 | -0.0487 | -0.0188 | -0.0004 | 0.0181 | 0.0497 |
| 2026-01-13 | -0.0001 | -0.0532 | -0.0201 | -0.0006 | 0.0193 | 0.0528 |
| 2026-01-14 | -0.0003 | -0.0561 | -0.0214 | -0.0007 | 0.0208 | 0.0561 |

---

## get_volatility
Calculate the Volatility: how much the returns of an investment portfolio or asset fluctuate in each period, from the daily prices.

Volatility measures the amount of dispersion or variability in returns. It is the square root of the Variance. A higher Volatility indicates greater variability, while a lower Volatility suggests that returns are closer to the mean.

By default this is the close-to-close Volatility, i.e. the standard deviation of the daily returns. One of five range-based estimators can be used instead, each of which uses more of the day's price action than just the close and is therefore more statistically efficient (i.e. needs fewer observations to reach the same precision), at the cost of additional assumptions about how prices move:

- Parkinson - uses the daily trading range (High vs Low) rather than the close-to-close return, assuming prices follow a continuous geometric Brownian motion with no drift and no overnight jumps.
- Garman-Klass - extends Parkinson by also incorporating the Open and Close, which allows it to account for the opening jump and makes it more efficient still (assuming, as Parkinson does, no drift and no overnight jumps beyond the modeled open).
- Rogers-Satchell - drift-independent, meaning it remains unbiased even when the underlying asset has a non-zero expected return over the period, at the cost of still assuming no overnight jumps.
- Yang-Zhang - a weighted combination of the overnight (close-to-open) Variance, the open-to-close Variance and the Rogers-Satchell Variance. It is both drift-independent and accounts for overnight jumps, which makes it the most statistically efficient of the range-based estimators implemented here.
- Garman-Klass Yang-Zhang - Garman-Klass with the squared overnight (close-to-open) return of Yang and Zhang added, so it accounts for overnight jumps while keeping the Garman-Klass term for the session (still assuming no drift).

The compounded Volatility keeps the close-to-close returns but scales them differently: rather than the square root of time, it gives the standard deviation of the period's return when the daily returns compound, the exact value for independent daily returns with the measured mean and variance. It exceeds the close-to-close Volatility when the returns are large (a cryptocurrency's yearly Volatility) and barely differs for small ones.

The formula for the close-to-close Volatility is as follows:

$$
\text{Volatility} = \operatorname{Std}(\text{Daily Returns within the period}) \cdot \sqrt{\text{Trading Days per Period}}
$$

Where Std is the sample standard deviation (with n - 1 in the denominator) and the trading days per period are 252 / 52 (weekly), 252 / 12 (monthly), 252 / 4 (quarterly) or 252 (yearly). A ticker with returns on weekends, such as a cryptocurrency, has a return on every calendar day and uses 365 days a year instead (365 / 52 weekly), so its Volatility is not understated against the stocks. The range-based estimators take the square root of a daily variance and scale it the same way, with H, L, O and C the daily High, Low, Open and Close, $$C_{- 1}$$ the previous Close, Mean the average and Var the sample variance (with n - 1 in the denominator) over the days in the period, and the compounded Volatility uses the daily returns directly:

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

$$
\text{Garman-Klass Yang-Zhang Variance} = \operatorname{Mean}\left(\ln\left(\frac{O}{C_{-1}}\right)^{2} + 0.5 \cdot \ln\left(\frac{H}{L}\right)^{2} - (2 \cdot \ln 2 - 1) \cdot \ln\left(\frac{C}{O}\right)^{2}\right)
$$

$$
\text{Compounded Volatility} = \sqrt{(\operatorname{Var}(r) + (1 + g)^{2})^{P} - (1 + g)^{2P}},\;\; \text{with } r \text{ the daily returns},\;\; g \;\text{their geometric mean} \;\left(\operatorname{PRODUCT}(1 + r)^{\frac{1}{n}} - 1 \;\text{over the}\; n \;\text{days}\right) \;\text{and}\; P \;\text{the trading days per period}
$$

With `rolling`, the result is the sample standard deviation of the last `rolling` returns of the chosen period itself, without scaling.

**Also known as:** standard deviation of returns. The range-based estimators are also known as Parkinson's range-based or high-low Volatility, Garman-Klass range-based Volatility, Rogers-Satchell drift-independent Volatility, Yang-Zhang drift-independent overnight-aware Volatility and GK-YZ Volatility.

**References:**

- paper | Parkinson, M. (1980). "The Extreme Value Method for Estimating the Variance of the Rate of Return." Journal of Business, 53(1), 61-65.
- paper | Garman, M.B., & Klass, M.J. (1980). "On the Estimation of Security Price Volatilities from Historical Data." Journal of Business, 53(1), 67-78.
- paper | Rogers, L.C.G., & Satchell, S.E. (1991). "Estimating Variance from High, Low and Closing Prices." Annals of Applied Probability, 1(4), 504-512.
- paper | Yang, D., & Zhang, Q. (2000). "Drift-Independent Volatility Estimation Based on High, Low, Open, and Close Prices." Journal of Business, 73(3), 477-492.
- library | Shares similar logic as TTR (R)'s [volatility](https://github.com/joshuaulrich/TTR/blob/v0.24.4/R/volatility.R#L139){:target="_blank"} (Parkinson, Garman-Klass, Rogers-Satchell, Yang-Zhang, Garman-Klass Yang-Zhang)
- library | Shares similar logic as backtesting.py's [compute_stats](https://github.com/kernc/backtesting.py/blob/0.6.4/backtesting/_stats.py#L140){:target="_blank"} (compounded, Volatility (Ann.) [%])

**Args:**

- <u>period (str, optional):</u> The data frequency for returns. Options are: "weekly", "monthly", "quarterly",
"yearly". Defaults to "quarterly" if the Toolkit is initialised with quarterly=True, otherwise
"yearly".
- <u>rolling (int, optional):</u> The rolling window size to use for the calculation. If set,
Volatility is calculated over a rolling window of this many periods (e.g. period='monthly'
and rolling=6 gives the rolling 6-month Volatility) instead of one value per `period`.
Only available for method="close_to_close". Defaults to None.
- <u>method (str, optional):</u> The Volatility estimator, as described above. Options are: "close_to_close"
(close-to-close), "parkinson" (Parkinson), "garman_klass" (Garman-Klass), "rogers_satchell"
(Rogers-Satchell), "yang_zhang" (Yang-Zhang), "garman_klass_yang_zhang" (Garman-Klass Yang-Zhang),
"compounded" (compounded). Defaults to "close_to_close".
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
- With growth, the method calculates the growth of Volatility values using the specified `lag`.
- backtesting.py (Zach Lûster) applies the compounded Volatility to the daily returns of a whole backtest
with 252 (or 365) days, and TTR scales the range-based estimators by a fixed number of days per year.

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
Calculate the Corsi (2009) Heterogeneous Autoregressive Realized Volatility (HAR-RV) forecast: the daily Realized Variance each asset is expected to have next, from its daily, weekly and monthly averages.

Volatility clustering happens across multiple, overlapping time horizons at once. HAR-RV captures this cheaply -- without the numerical optimization a GARCH-family fit requires (see `get_garch`) -- by regressing future daily Realized Variance on trailing daily, weekly and monthly average Realized Variance components. The daily Realized Variance itself can be constructed in several ways: the simplest is the squared daily return, while the OHLC range-based estimators (see `get_volatility`, which offers the same estimators) use the daily (pre-period-aggregation) term behind each of those estimators instead, which is more statistically efficient since it uses the daily trading range rather than only the close-to-close move.

The formula is as follows (with the squared return, a weekly window of 5 days, a monthly window of 22 days and a horizon of 1 day):

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

**Also known as:** HAR-RV model, Corsi's HAR model, Heterogeneous Autoregressive model.

**References:**

- paper | Corsi, F. (2009). "A Simple Approximate Long-Memory Model of Realized Volatility." Journal of Financial Econometrics, 7(2), 174-196.

**Args:**

- <u>estimator (str, optional):</u> How to construct the daily Realized Variance input. Options are:
"squared_return" (the squared daily return), "parkinson" (Parkinson), "garman_klass" (Garman-Klass),
"rogers_satchell" (Rogers-Satchell). Defaults to "squared_return".
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
- With growth, the method calculates the growth of the HAR-RV forecast values
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
Calculate the Excess Volatility: how much the returns of an investment portfolio or asset above the risk free rate fluctuate in each period.

Excess Volatility is the Volatility of the Excess Return, i.e. the daily return minus the risk free rate, scaled to the given period in the same way as the Volatility.

The formula is as follows:

$$
\text{Excess Volatility} = \operatorname{Std}(\text{Daily Return} - \text{Daily Risk Free Rate}) \cdot \sqrt{\text{Trading Days per Period}}
$$

Where Std is the sample standard deviation (with n - 1 in the denominator) over the days within the period, the annualized risk free rate is converted to the rate earned with each return (a trading day of it, 1 / 252 of a year, or for a ticker that trades on weekends the calendar days since its previous return, on 365 days a year), and the trading days per period are 252 / 52 (weekly), 252 / 12 (monthly), 252 / 4 (quarterly) or 252 (yearly), or 365 days a year for a ticker with returns on weekends. With `rolling`, the result is the sample standard deviation of the last `rolling` excess returns of the chosen period itself, without scaling, with the risk free rate compounded over the dates in each period on which the ticker has a return.

**Also known as:** standard deviation of excess returns.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns. Options are: "weekly", "monthly", "quarterly",
"yearly". Defaults to "quarterly" if the Toolkit is initialised with quarterly=True, otherwise
"yearly".
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
- With growth, the method calculates the growth of Excess Volatility values using
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
Calculate the Downside Deviation: how widely the returns of an investment portfolio or asset fall below a minimum acceptable return, the volatility of the losses.

The Downside Deviation, also known as semi-deviation, measures the dispersion of the returns below a minimum acceptable return (MAR), isolating the volatility of negative outcomes from the volatility of the overall return distribution. It underlies risk-adjusted return measures such as the Sortino Ratio and the Omega Ratio.

The formula is as follows:

$$
\text{Downside Deviation} = \sqrt{\frac{\sum \min(\text{Return}_{t} - \text{MAR},\; 0)^{2}}{n}}
$$

Where n is the number of all returns, so returns above the MAR count as a shortfall of zero rather than being left out.

With the mean as the minimum acceptable return it is the Semi-Deviation of Markowitz (1959), the dispersion below each sample's own mean:

$$
\text{Semi-Deviation} = \sqrt{\frac{\sum \min(\text{Return}_{t} - \text{Mean},\; 0)^{2}}{n - 1}}
$$

Divided by n - 1, as the sample variance is, since the mean is estimated from the same returns. Its square is the semi-variance.

**Also known as:** semi-deviation, semi-variance (its square), downside risk, downside volatility.

**References:**

- paper | Sortino, F.A. and Price, L.N. (1994). "Performance Measurement in a Downside Risk Framework." The Journal of Investing, 3(3), 59-64.
- paper | Markowitz, H.M. (1959). "Portfolio Selection: Efficient Diversification of Investments." John Wiley & Sons, chapter 9 (the semi-variance).
- library | Referenced against Riskfolio-Lib's [SemiDeviation](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/risk.html#RiskFunctions.SemiDeviation){:target="_blank"}
- library | Referenced against skfolio's [semi_deviation](https://skfolio.org/generated/skfolio.measures.semi_deviation.html){:target="_blank"}
- library | Shares similar logic as PerformanceAnalytics (R)'s [DownsideDeviation](https://github.com/braverock/PerformanceAnalytics/blob/v2.0.4/R/DownsideDeviation.R#L104){:target="_blank"}
- library | Shares similar logic as PerformanceAnalytics (R)'s [SemiDeviation](https://github.com/braverock/PerformanceAnalytics/blob/v2.0.4/R/SemiDeviation.R#L4){:target="_blank"}
- library | Shares similar logic as skfolio's [semi_variance](https://skfolio.org/generated/skfolio.measures.semi_variance.html){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The data frequency for returns. Options are: "daily", "weekly", "monthly",
"quarterly", "yearly". Defaults to "daily".
- <u>minimum_acceptable_return (float &#124; str, optional):</u> The minimum acceptable return (MAR) used as the
threshold below which returns are considered downside, per observation of the chosen `period`, or
"mean" for the Semi-Deviation below the mean. Defaults to 0.0.
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
- With growth, the method calculates the growth of the Downside Deviation values using
the specified `lag`.
- With the default MAR of 0 the result agrees with PerformanceAnalytics' DownsideDeviation over all
returns. With the mean as the MAR it agrees with Riskfolio-Lib's SemiDeviation and skfolio's
semi_deviation (skfolio's semi_variance is its square), while PerformanceAnalytics' SemiDeviation
divides by n.

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

## get_upside_deviation
Calculate the Upside Deviation: how widely the returns of an investment portfolio or asset rise above a minimum acceptable return, the volatility an investor welcomes.

The Upside Deviation is the mirror image of the Downside Deviation: it measures the dispersion of the returns above a minimum acceptable return (MAR), the volatility an investor welcomes. Next to the Downside Deviation it shows whether an asset's volatility comes from its gains or from its losses, and their ratio is the Variability Skewness (`get_volatility_skewness`).

The formula is as follows:

$$
\text{Upside Deviation} = \sqrt{\frac{\sum \max(\text{Return}_{t} - \text{MAR},\; 0)^{2}}{n}}
$$

Where n is the number of all returns, so returns below the MAR count as zero rather than being left out. Its square is the upside variance and the upper partial moment of order 1 the upside potential (`get_partial_moment` on the upper side).

**Also known as:** upside risk, upside volatility, upside semi-deviation.

**References:**

- paper | Bacon, C.R. (2008). "Practical Portfolio Performance Measurement and Attribution." John Wiley & Sons, chapter 4 (upside risk).
- library | Shares similar logic as PerformanceAnalytics (R)'s [UpsideRisk](https://github.com/braverock/PerformanceAnalytics/blob/v2.0.4/R/UpsideRisk.R#L54){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The data frequency for returns. Options are: "daily", "weekly", "monthly",
"quarterly", "yearly". Defaults to "daily".
- <u>minimum_acceptable_return (float, optional):</u> The minimum acceptable return (MAR) per
observation of the chosen `period` (e.g. per day), above which returns count as upside.
Defaults to 0.0.
- <u>within_period (bool, optional):</u> Whether to calculate the Upside Deviation within the specified period or
for the entire period. Thus whether to look at the Upside Deviation within a specific year (if period =
'yearly') or look at the entirety of all years. Defaults to False.
Note that this requires intraday data when period = 'daily', since a
single day only nests observations when intraday data was fetched.
- <u>rolling (int, optional):</u> The rolling window size to use for the calculation. If set, the Upside Deviation
is calculated over a rolling window of this many periods across the full return history
instead of per `period`. Defaults to None.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Upside Deviation values over time.
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

pd.Series &#124; pd.DataFrame: Upside Deviation values, per ticker, or per period (or date) and ticker.

**Notes:**

- The method retrieves historical return data based on the specified `period` and calculates the
Upside Deviation for each asset in the Toolkit instance, each on its own returns (a ticker that listed later
or misses a date another ticker traded is measured on the returns it has).
- With growth, the method calculates the growth of the Upside Deviation values using the
specified `lag`.
- The result agrees with the upside risk of PerformanceAnalytics' UpsideRisk over all returns.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["NEE", "DUK", "SO"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_upside_deviation(period="yearly", within_period=True)
```

Which returns:

|      |    NEE |    DUK |     SO |   Benchmark |
|:-----|-------:|-------:|-------:|------------:|
| 2021 | 0.0098 | 0.0077 | 0.0072 |      0.0062 |
| 2022 | 0.014  | 0.0091 | 0.0102 |      0.0105 |
| 2023 | 0.0112 | 0.0081 | 0.0085 |      0.0063 |
| 2024 | 0.0109 | 0.0076 | 0.0081 |      0.0058 |
| 2025 | 0.0124 | 0.0076 | 0.0078 |      0.0092 |

---

## get_volatility_skewness
Calculate the Volatility Skewness or Variability Skewness: whether the returns of an investment portfolio or asset spread out more on the gain side than on the loss side of a minimum acceptable return.

The Volatility Skewness (Bacon 2008) divides the upside variance by the downside variance around a minimum acceptable return (MAR): above 1 the returns spread out more on the gain side than on the loss side, below 1 the volatility comes mostly from losses. The Variability Skewness is its square root, the Upside Deviation over the Downside Deviation, on the scale of the returns. Both describe the asymmetry of the return distribution without the third moment, which a single extreme return can dominate.

The formula is as follows:

$$
\text{Volatility Skewness} = \frac{\sum \max(\text{Return}_{t} - \text{MAR},\; 0)^{2}}{\sum \max(\text{MAR} - \text{Return}_{t},\; 0)^{2}}
$$

$$
\text{Variability Skewness} = \sqrt{\text{Volatility Skewness}} = \frac{\text{Upside Deviation}}{\text{Downside Deviation}}
$$

Where the sums run over all returns of the sample, so it is the upside variance over the downside variance, both divided by the number of all returns. A sample without a return below the MAR gives NaN.

**Also known as:** variability skewness, upside to downside variance ratio.

**References:**

- paper | Bacon, C.R. (2008). "Practical Portfolio Performance Measurement and Attribution." John Wiley & Sons, chapter 4.
- library | Shares similar logic as PerformanceAnalytics (R)'s [VolatilitySkewness](https://github.com/braverock/PerformanceAnalytics/blob/v2.0.4/R/VolatilitySkewness.R#L41){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The data frequency for returns. Options are: "daily", "weekly", "monthly",
"quarterly", "yearly". Defaults to "daily".
- <u>minimum_acceptable_return (float, optional):</u> The minimum acceptable return (MAR) per
observation of the chosen `period` (e.g. per day). Defaults to 0.0.
- <u>method (str, optional):</u> The ratio. Options are: "volatility" (Volatility Skewness, the ratio of
the variances), "variability" (Variability Skewness, the ratio of the deviations). Defaults to
"volatility".
- <u>within_period (bool, optional):</u> Whether to calculate the Volatility Skewness within the specified period or
for the entire period. Thus whether to look at the Volatility Skewness within a specific year (if period =
'yearly') or look at the entirety of all years. Defaults to False.
Note that this requires intraday data when period = 'daily', since a
single day only nests observations when intraday data was fetched.
- <u>rolling (int, optional):</u> The rolling window size to use for the calculation. If set, the Volatility Skewness
is calculated over a rolling window of this many periods across the full return history
instead of per `period`. Defaults to None.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>growth (bool, optional):</u> Whether to calculate the growth of the Volatility Skewness values over time.
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

pd.Series &#124; pd.DataFrame: Volatility Skewness values, per ticker, or per period (or date) and ticker.

**Notes:**

- The method retrieves historical return data based on the specified `period` and calculates the
Volatility Skewness for each asset in the Toolkit instance, each on its own returns (a ticker that listed later
or misses a date another ticker traded is measured on the returns it has).
- With growth, the method calculates the growth of the Volatility Skewness values using the
specified `lag`.
- The result agrees with the volatility and variability statistics of PerformanceAnalytics'
VolatilitySkewness.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["SPY", "QQQ", "IWM"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.risk.get_volatility_skewness(period="yearly", within_period=True)
```

Which returns:

|      |    QQQ |    IWM |   Benchmark |
|:-----|-------:|-------:|------------:|
| 2021 | 1.1361 | 1.1843 |      1.2921 |
| 2022 | 0.8549 | 0.9106 |      0.9091 |
| 2023 | 1.7396 | 1.3442 |      1.4283 |
| 2024 | 1.0406 | 1.1335 |      1.1207 |
| 2025 | 1.2522 | 1.1954 |      1.289  |

---

## get_ewma_volatility
Calculate the exponentially weighted moving average (EWMA) Volatility: how volatile the daily returns of an investment portfolio or asset are now, weighing recent returns most, following RiskMetrics.

Unlike a fixed-window rolling Volatility, EWMA Volatility weights recent observations more heavily than older ones, so it reacts faster to changes in the underlying volatility regime. It is a simpler, more interpretable alternative to a full GARCH fit.

The formula is as follows:

$$
\text{EWMA Variance}(t) = \lambda \cdot \text{EWMA Variance}(t-1) + (1 - \lambda) \cdot \operatorname{Return}(t-1)^{2}
$$

$$
\text{EWMA Volatility}(t) = \sqrt{\text{EWMA Variance}(t)}
$$

Where lambda is 0.94 by default and Return(t-1) the previous daily return, so the value on a day only uses the returns before it. The recursion starts from the first squared return.

With the RiskMetrics decay factor of 0.94, about 70% of the weight sits on the last 20 trading days, so EWMA Volatility reacts within days to a market shock and falls back almost as quickly. The values are daily; multiply them by the square root of 252 (365 for a ticker that trades on weekends) for an annualized figure comparable with the yearly `get_volatility`.

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
- With growth, the method calculates the growth of the EWMA Volatility values using
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

