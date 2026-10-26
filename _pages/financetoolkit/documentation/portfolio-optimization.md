---
title: Portfolio Optimization
seo_title: "Portfolio Optimization | Finance Toolkit"
seo_title_suffix: false
excerpt: The Portfolio Optimization module builds portfolios from the tickers of a Toolkit, from minimum variance, maximum Sharpe ratio and risk parity weights to the efficient frontier, risk contributions, stress tests and attribution.
description: The Portfolio Optimization module builds portfolios from the tickers of a Toolkit, from minimum variance, maximum Sharpe ratio and risk parity weights to the efficient frontier, risk contributions, stress tests and attribution.
author_profile: false
permalink: /projects/financetoolkit/docs/portfolio-optimization
classes: wide-sidebar
layout: single
sidebar:
    nav: "financetoolkit-docs-portfolio-optimization"
---

The Portfolio Optimization module builds portfolios from the tickers of a Toolkit: minimum variance, maximum Sharpe ratio, mean-variance, risk parity, Hierarchical Risk Parity, minimum CVaR and Black-Litterman weights, the efficient frontier, risk contributions, stress tests and attribution.

Use it in Claude, ChatGPT or another AI assistant through the [Finance Toolkit MCP](/projects/financetoolkit/mcp), or install the Python package:

```python
pip install financetoolkit -U
```

{% include algolia.html %}

{% include financetoolkit-getting-started/portfolio-optimization.md %}

## get_minimum_variance_weights
Calculate the weights of the minimum variance portfolio: the fully invested portfolio of the Toolkit's assets with the lowest volatility. It uses only the covariance matrix, not the expected returns, which makes it the most robust of the mean-variance portfolios to estimation error.

The weights minimize w'Σw subject to the weights summing to one and lying between the minimum and maximum weight, where Σ is the annualized covariance matrix of the returns.

For more information, see the following paper:

- Markowitz, H. (1952). "Portfolio Selection." The Journal of Finance, 7(1), 77-91.

**Also known as:** global minimum variance portfolio, GMV, lowest risk portfolio.

**Args:**

- <u>period (str, optional):</u> The frequency of the returns the covariance matrix is
estimated from (daily, weekly, monthly, quarterly or yearly). Defaults to
"daily".
- <u>minimum_weight (float, optional):</u> The lowest weight an asset may have; a
negative value allows short positions. Defaults to 0.
- <u>maximum_weight (float, optional):</u> The highest weight an asset may have.
Defaults to 1.
- <u>include_benchmark (bool, optional):</u> Whether to include the benchmark as an
asset. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.

**Returns:**

pd.DataFrame: Per asset and for the portfolio, the Weight, Expected Return,
Volatility, Sharpe Ratio and Risk Contribution (the share of the portfolio's
volatility). Returns and volatilities are annualized.

**Notes:**

- Only the periods in which every asset has a return are used, so an asset with a
short history shortens the sample of all assets.
- The expected returns are the historical average returns, annualized; the Sharpe
ratios use the average risk free rate over the same periods.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "JNJ", "XOM"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.portfolio.get_minimum_variance_weights()
```

Which returns:

|           |   Weight |   Expected Return |   Volatility |   Sharpe Ratio |   Risk Contribution |
|:----------|---------:|------------------:|-------------:|---------------:|--------------------:|
| AAPL      |   0.0212 |            0.1933 |       0.2786 |         0.5727 |              0.0212 |
| MSFT      |   0.2166 |            0.2017 |       0.2572 |         0.6532 |              0.2166 |
| JNJ       |   0.5821 |            0.0984 |       0.1673 |         0.3867 |              0.5821 |
| XOM       |   0.1801 |            0.291  |       0.2702 |         0.9522 |              0.1801 |
| Portfolio |   1      |            0.1575 |       0.135  |         0.9166 |              1      |

---

## get_maximum_sharpe_weights
Calculate the weights of the maximum Sharpe ratio portfolio: the fully invested portfolio with the highest expected return per unit of volatility above the risk free rate. It is the tangency portfolio, where a line from the risk free rate touches the efficient frontier.

The weights maximize (w'μ - r_f) / sqrt(w'Σw) subject to the weights summing to one and lying between the minimum and maximum weight, with μ the annualized expected returns, Σ the annualized covariance matrix and r_f the risk free rate.

For more information, see the following papers:

- Tobin, J. (1958). "Liquidity Preference as Behavior Towards Risk." The Review of Economic Studies, 25(2), 65-86.
- Sharpe, W.F. (1966). "Mutual Fund Performance." The Journal of Business, 39(1), 119-138.

**Also known as:** tangency portfolio, optimal risky portfolio, max Sharpe.

**Args:**

- <u>period (str, optional):</u> The frequency of the returns (daily, weekly, monthly,
quarterly or yearly). Defaults to "daily".
- <u>minimum_weight (float, optional):</u> The lowest weight an asset may have; a
negative value allows short positions. Defaults to 0.
- <u>maximum_weight (float, optional):</u> The highest weight an asset may have.
Defaults to 1.
- <u>include_benchmark (bool, optional):</u> Whether to include the benchmark as an
asset. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.

**Returns:**

pd.DataFrame: Per asset and for the portfolio, the Weight, Expected Return,
Volatility, Sharpe Ratio and Risk Contribution. Returns and volatilities are
annualized.

**Notes:**

- The expected returns are the historical average returns. They are the noisiest
input of the optimization, so the weights tend to concentrate in the assets that
happened to do best; a maximum weight or the Black-Litterman returns temper that.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "JNJ", "XOM"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.portfolio.get_maximum_sharpe_weights(maximum_weight=0.4)
```

Which returns:

|           |   Weight |   Expected Return |   Volatility |   Sharpe Ratio |   Risk Contribution |
|:----------|---------:|------------------:|-------------:|---------------:|--------------------:|
| AAPL      |   0.0293 |            0.1933 |       0.2786 |         0.5727 |              0.0287 |
| MSFT      |   0.3129 |            0.2017 |       0.2572 |         0.6532 |              0.3207 |
| JNJ       |   0.2578 |            0.0984 |       0.1673 |         0.3867 |              0.1137 |
| XOM       |   0.4    |            0.291  |       0.2702 |         0.9522 |              0.5369 |
| Portfolio |   1      |            0.2105 |       0.1568 |         1.1275 |              1      |

---

## get_mean_variance_weights
Calculate the weights of a mean-variance efficient portfolio. With a target return, it is the portfolio with the lowest volatility that expects that return. Without one, it is the portfolio that maximizes the investor's utility, the expected return minus half the risk aversion times the variance: w'μ - (λ/2) w'Σw.

A risk aversion of 2 to 4 is typical; 2.5 is the value commonly used for the market as a whole.

For more information, see the following paper:

- Markowitz, H. (1952). "Portfolio Selection." The Journal of Finance, 7(1), 77-91.

**Also known as:** Markowitz portfolio, efficient portfolio, quadratic utility portfolio.

**Args:**

- <u>target_return (float &#124; None, optional):</u> The annualized return the portfolio must
expect, e.g. 0.12 for 12%. Defaults to None, which uses the risk aversion.
- <u>risk_aversion (float, optional):</u> The investor's risk aversion λ; higher values
give less risky portfolios. Defaults to 2.5.
- <u>period (str, optional):</u> The frequency of the returns (daily, weekly, monthly,
quarterly or yearly). Defaults to "daily".
- <u>minimum_weight (float, optional):</u> The lowest weight an asset may have. Defaults
to 0.
- <u>maximum_weight (float, optional):</u> The highest weight an asset may have.
Defaults to 1.
- <u>include_benchmark (bool, optional):</u> Whether to include the benchmark as an
asset. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.

**Returns:**

pd.DataFrame: Per asset and for the portfolio, the Weight, Expected Return,
Volatility, Sharpe Ratio and Risk Contribution.

**Notes:**

- A target return outside what the assets can reach within the weight bounds
raises an error that states the reachable range.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "JNJ", "XOM"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.portfolio.get_mean_variance_weights(target_return=0.15)
```

Which returns:

|           |   Weight |   Expected Return |   Volatility |   Sharpe Ratio |   Risk Contribution |
|:----------|---------:|------------------:|-------------:|---------------:|--------------------:|
| AAPL      |   0.0219 |            0.1933 |       0.2786 |         0.5727 |              0.0211 |
| MSFT      |   0.2058 |            0.2017 |       0.2572 |         0.6532 |              0.1961 |
| JNJ       |   0.6256 |            0.0984 |       0.1673 |         0.3867 |              0.6549 |
| XOM       |   0.1467 |            0.291  |       0.2702 |         0.9522 |              0.1279 |
| Portfolio |   1      |            0.15   |       0.1355 |         0.8583 |              1      |

---

## get_efficient_frontier
Calculate the efficient frontier: the portfolios with the lowest volatility for each level of expected return, from the minimum variance portfolio up to the highest return the weight bounds allow. Every portfolio below the frontier takes more risk than needed for its return.

For more information, see the following paper:

- Markowitz, H. (1952). "Portfolio Selection." The Journal of Finance, 7(1), 77-91.

**Also known as:** Markowitz frontier, mean-variance frontier, risk-return frontier.

**Args:**

- <u>points (int, optional):</u> The number of portfolios on the frontier. Defaults to 20.
- <u>period (str, optional):</u> The frequency of the returns (daily, weekly, monthly,
quarterly or yearly). Defaults to "daily".
- <u>minimum_weight (float, optional):</u> The lowest weight an asset may have. Defaults
to 0.
- <u>maximum_weight (float, optional):</u> The highest weight an asset may have.
Defaults to 1.
- <u>include_benchmark (bool, optional):</u> Whether to include the benchmark as an
asset. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.

**Returns:**

pd.DataFrame: Per portfolio on the frontier (numbered from the lowest risk), its
annualized Expected Return, Volatility and Sharpe Ratio and the weight per asset.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "JNJ", "XOM"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.portfolio.get_efficient_frontier(points=5)
```

Which returns:

|   Portfolio |   Expected Return |   Volatility |   Sharpe Ratio |   AAPL |   MSFT |    JNJ |    XOM |
|------------:|------------------:|-------------:|---------------:|-------:|-------:|-------:|-------:|
|           1 |            0.1575 |       0.135  |         0.9166 | 0.0212 | 0.2166 | 0.5821 | 0.1801 |
|           2 |            0.1909 |       0.1439 |         1.0917 | 0.0178 | 0.265  | 0.388  | 0.3292 |
|           3 |            0.2243 |       0.1679 |         1.1349 | 0.0145 | 0.3133 | 0.194  | 0.4782 |
|           4 |            0.2576 |       0.2016 |         1.111  | 0.0111 | 0.3616 | 0      | 0.6274 |
|           5 |            0.291  |       0.2702 |         0.9522 | 0      | 0      | 0      | 1      |

---

## get_risk_parity_weights
Calculate the risk parity weights: the portfolio in which every asset contributes the same share of the volatility, or the share set by a risk budget. Volatile assets get smaller weights, and correlated assets share their risk budget, so no single asset dominates the portfolio's risk.

The weights solve w_i (Σw)_i / σ_p = b_i σ_p for every asset, found by minimizing the convex function 1/2 w'Σw - Σ b_i ln(w_i) and scaling the result to sum to one.

For more information, see the following papers:

- Maillard, S., Roncalli, T. and Teïletche, J. (2010). "The Properties of Equally Weighted Risk Contribution Portfolios." The Journal of Portfolio Management, 36(4), 60-70.
- Spinu, F. (2013). "An Algorithm for Computing Risk Parity Weights." SSRN Working Paper.

**Also known as:** equal risk contribution, ERC, risk budgeting.

**Args:**

- <u>risk_budget (dict[str, float] &#124; None, optional):</u> The share of the risk per
asset, e.g. {"AAPL": 0.4, "MSFT": 0.2, ...}; it is scaled to sum to one.
Defaults to None, an equal share for every asset.
- <u>period (str, optional):</u> The frequency of the returns (daily, weekly, monthly,
quarterly or yearly). Defaults to "daily".
- <u>include_benchmark (bool, optional):</u> Whether to include the benchmark as an
asset. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.

**Returns:**

pd.DataFrame: Per asset and for the portfolio, the Weight, Expected Return,
Volatility, Sharpe Ratio and Risk Contribution.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "JNJ", "XOM"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.portfolio.get_risk_parity_weights()
```

Which returns:

|           |   Weight |   Expected Return |   Volatility |   Sharpe Ratio |   Risk Contribution |
|:----------|---------:|------------------:|-------------:|---------------:|--------------------:|
| AAPL      |   0.1786 |            0.1933 |       0.2786 |         0.5727 |                0.25 |
| MSFT      |   0.2129 |            0.2017 |       0.2572 |         0.6532 |                0.25 |
| JNJ       |   0.3782 |            0.0984 |       0.1673 |         0.3867 |                0.25 |
| XOM       |   0.2303 |            0.291  |       0.2702 |         0.9522 |                0.25 |
| Portfolio |   1      |            0.1817 |       0.1452 |         1.0189 |                1    |

---

## get_hierarchical_risk_parity_weights
Calculate the Hierarchical Risk Parity (HRP) weights. The assets are clustered by their correlations, ordered so that similar assets sit next to each other, and the weight is split top-down between the two halves of every cluster in inverse proportion to their variance. It never inverts the covariance matrix, so it stays stable with many or highly correlated assets, where mean-variance weights become erratic.

As in the paper, the clustering uses the Euclidean distance between the columns of the correlation distance matrix √((1 - ρ) / 2): two assets are close when they relate to all the other assets in the same way. Some libraries cluster on the correlation distance itself, which can order the assets differently.

For more information, see the following paper:

- López de Prado, M. (2016). "Building Diversified Portfolios that Outperform Out of Sample." The Journal of Portfolio Management, 42(4), 59-69.

**Also known as:** HRP, hierarchical clustering portfolio.

**Args:**

- <u>linkage_method (str, optional):</u> The linkage of the hierarchical clustering:
"single", "complete", "average" or "ward". Defaults to "single", as in the
paper.
- <u>period (str, optional):</u> The frequency of the returns (daily, weekly, monthly,
quarterly or yearly). Defaults to "daily".
- <u>include_benchmark (bool, optional):</u> Whether to include the benchmark as an
asset. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.

**Returns:**

pd.DataFrame: Per asset and for the portfolio, the Weight, Expected Return,
Volatility, Sharpe Ratio and Risk Contribution.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "JNJ", "XOM"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.portfolio.get_hierarchical_risk_parity_weights()
```

Which returns:

|           |   Weight |   Expected Return |   Volatility |   Sharpe Ratio |   Risk Contribution |
|:----------|---------:|------------------:|-------------:|---------------:|--------------------:|
| AAPL      |   0.1287 |            0.1933 |       0.2786 |         0.5727 |              0.1599 |
| MSFT      |   0.1511 |            0.2017 |       0.2572 |         0.6532 |              0.1498 |
| JNJ       |   0.5206 |            0.0984 |       0.1673 |         0.3867 |              0.4742 |
| XOM       |   0.1996 |            0.291  |       0.2702 |         0.9522 |              0.2161 |
| Portfolio |   1      |            0.1647 |       0.1374 |         0.9534 |              1      |

---

## get_inverse_volatility_weights
Calculate inverse volatility weights: each asset's weight is proportional to one over its volatility, w_i = (1/σ_i) / Σ(1/σ_j). It is the simplest risk-based allocation and equals risk parity when all correlations are the same.

**Also known as:** naive risk parity, volatility weighting.

**Args:**

- <u>period (str, optional):</u> The frequency of the returns (daily, weekly, monthly,
quarterly or yearly). Defaults to "daily".
- <u>include_benchmark (bool, optional):</u> Whether to include the benchmark as an
asset. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.

**Returns:**

pd.DataFrame: Per asset and for the portfolio, the Weight, Expected Return,
Volatility, Sharpe Ratio and Risk Contribution.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "JNJ", "XOM"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.portfolio.get_inverse_volatility_weights()
```

Which returns:

|           |   Weight |   Expected Return |   Volatility |   Sharpe Ratio |   Risk Contribution |
|:----------|---------:|------------------:|-------------:|---------------:|--------------------:|
| AAPL      |   0.2092 |            0.1933 |       0.2786 |         0.5727 |              0.3023 |
| MSFT      |   0.2267 |            0.2017 |       0.2572 |         0.6532 |              0.2743 |
| JNJ       |   0.3484 |            0.0984 |       0.1673 |         0.3867 |              0.2083 |
| XOM       |   0.2157 |            0.291  |       0.2702 |         0.9522 |              0.2152 |
| Portfolio |   1      |            0.1832 |       0.1491 |         1.0028 |              1      |

---

## get_minimum_cvar_weights
Calculate the weights of the minimum Conditional Value at Risk (CVaR) portfolio: the fully invested portfolio whose average loss in the worst periods is the smallest. Unlike variance, CVaR only looks at the losses in the tail, so it accounts for skewed and fat-tailed returns.

The problem is solved as a linear programme over the historical returns: minimize VaR + 1/((1 - α)T) Σ max(0, -r_t'w - VaR), with α the confidence level and T the number of periods.

For more information, see the following paper:

- Rockafellar, R.T. and Uryasev, S. (2000). "Optimization of Conditional Value-at-Risk." Journal of Risk, 2(3), 21-41.

**Also known as:** minimum expected shortfall portfolio, mean-CVaR, tail risk optimization.

**Args:**

- <u>confidence_level (float, optional):</u> The confidence level of the CVaR, e.g. 0.95
for the average of the worst 5% of periods. Defaults to 0.95.
- <u>period (str, optional):</u> The frequency of the returns (daily, weekly, monthly,
quarterly or yearly). Defaults to "daily".
- <u>minimum_weight (float, optional):</u> The lowest weight an asset may have. Defaults
to 0.
- <u>maximum_weight (float, optional):</u> The highest weight an asset may have.
Defaults to 1.
- <u>include_benchmark (bool, optional):</u> Whether to include the benchmark as an
asset. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.

**Returns:**

pd.DataFrame: Per asset and for the portfolio, the Weight, Expected Return,
Volatility, Sharpe Ratio and Risk Contribution, with the portfolio's CVaR (per
period, as a loss) in the CVaR column.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "JNJ", "XOM"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.portfolio.get_minimum_cvar_weights()
```

Which returns:

|           |   Weight |   Expected Return |   Volatility |   Sharpe Ratio |   Risk Contribution |   CVaR |
|:----------|---------:|------------------:|-------------:|---------------:|--------------------:|-------:|
| AAPL      |   0      |            0.1933 |       0.2786 |         0.5727 |              0      | 0.0389 |
| MSFT      |   0.1823 |            0.2017 |       0.2572 |         0.6532 |              0.1507 | 0.0355 |
| JNJ       |   0.5966 |            0.0984 |       0.1673 |         0.3867 |              0.6006 | 0.0227 |
| XOM       |   0.2211 |            0.291  |       0.2702 |         0.9522 |              0.2488 | 0.0369 |
| Portfolio |   1      |            0.1598 |       0.136  |         0.9273 |              1      | 0.0189 |

---

## get_black_litterman_weights
Calculate the Black-Litterman expected returns and the weights they lead to. The starting point is the return the market implies through its capitalization weights: the excess return Π = δΣw_mkt at which holding the market is optimal, plus the risk free rate, so the Implied Return is a total return. Views then move these returns towards the investor's expectations, in proportion to the confidence in each view. The result avoids the extreme weights that historical average returns give.

Views are absolute ({"AAPL": 0.10}: AAPL returns 10% a year in total, risk free rate included) or relative ({"AAPL-MSFT": 0.02}: AAPL beats MSFT by 2% a year). Without a confidence, a view is as uncertain as the variance of the view portfolio scaled by tau; a confidence c scales that by (1 - c) / c, Idzorek's confidence method in the closed form of Walters (2014). The weights are the mean-variance portfolio of the Black-Litterman returns with the same risk aversion. Without views, or with relative views only, the risk free rate shifts every return by the same amount and leaves the weights unchanged; an absolute view is compared with the implied total return, so there it matters.

For more information, see the following papers:

- Black, F. and Litterman, R. (1992). "Global Portfolio Optimization." Financial Analysts Journal, 48(5), 28-43.
- He, G. and Litterman, R. (1999). "The Intuition Behind Black-Litterman Model Portfolios." Goldman Sachs Investment Management Research.
- Idzorek, T. (2005). "A Step-by-Step Guide to the Black-Litterman Model: Incorporating User-Specified Confidence Levels." Working paper.
- Walters, J. (2014). "The Black-Litterman Model in Detail." [https://ssrn.com/abstract=1314585](https://ssrn.com/abstract=1314585){:target="_blank"}

**Also known as:** BL model, equilibrium returns with views.

**Args:**

- <u>views (dict[str, float] &#124; None, optional):</u> The annualized views, absolute views
as total returns, as described above. Defaults to None, which returns the
market implied returns.
- <u>view_confidences (dict[str, float] &#124; None, optional):</u> The confidence per view,
between 0 and 1. Defaults to None, which sets each view's uncertainty to the
variance of the view scaled by tau.
- <u>market_weights (dict[str, float] &#124; None, optional):</u> The market weight per asset.
Defaults to None, which uses the market capitalizations of the assets.
- <u>risk_aversion (float, optional):</u> The risk aversion δ of the market. Defaults to
2.5.
- <u>tau (float, optional):</u> The uncertainty of the implied returns relative to the
covariance matrix. Defaults to 0.05.
- <u>period (str, optional):</u> The frequency of the returns the covariance matrix is
estimated from. Defaults to "daily".
- <u>minimum_weight (float, optional):</u> The lowest weight an asset may have. Defaults
to 0.
- <u>maximum_weight (float, optional):</u> The highest weight an asset may have.
Defaults to 1.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.

**Returns:**

pd.DataFrame: Per asset its Market Weight, Implied Return, Black-Litterman Return
(both annualized total returns) and the resulting Weight.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "JNJ", "XOM"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.portfolio.get_black_litterman_weights(
    views={"XOM": 0.10, "AAPL-MSFT": 0.02}
)
```

Which returns:

|      |   Market Weight |   Implied Return |   Black-Litterman Return |   Weight |
|:-----|----------------:|-----------------:|-------------------------:|---------:|
| AAPL |          0.4899 |           0.1752 |                   0.1769 |   0.4738 |
| MSFT |          0.376  |           0.1531 |                   0.155  |   0.3729 |
| JNJ  |          0.0614 |           0.0509 |                   0.052  |   0.0145 |
| XOM  |          0.0727 |           0.0709 |                   0.0853 |   0.1387 |

---

## get_risk_contributions
Calculate how much each asset contributes to the volatility of a portfolio. The marginal contribution is the change in portfolio volatility from a small increase in an asset's weight, (Σw)_i / σ_p; the risk contribution is the weight times that, and the contributions add up to the portfolio's volatility (Euler allocation). A large position in a calm asset can contribute less risk than a small one in a volatile asset.

For more information, see the following paper:

- Litterman, R. (1996). "Hot Spots and Hedges." The Journal of Portfolio Management, 23(5), 52-75.

**Also known as:** risk decomposition, marginal contribution to risk, risk budget.

**Args:**

- <u>weights (dict[str, float] &#124; None, optional):</u> The weight per asset. Defaults to
None, which uses the latest weights of the Portfolio the Toolkit came from,
or equal weights.
- <u>period (str, optional):</u> The frequency of the returns (daily, weekly, monthly,
quarterly or yearly). Defaults to "daily".
- <u>include_benchmark (bool, optional):</u> Whether to include the benchmark as an
asset. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.

**Returns:**

pd.DataFrame: Per asset and in total, the Weight, Marginal Contribution, Risk
Contribution and Percentage Contribution (annualized volatility terms).

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "JNJ", "XOM"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.portfolio.get_risk_contributions(
    weights={"AAPL": 0.4, "MSFT": 0.3, "JNJ": 0.2, "XOM": 0.1}
)
```

Which returns:

| Asset   |   Weight |   Marginal Contribution |   Risk Contribution |   Percentage Contribution |
|:--------|---------:|------------------------:|--------------------:|--------------------------:|
| AAPL    |      0.4 |                  0.2564 |              0.1025 |                    0.5529 |
| MSFT    |      0.3 |                  0.2116 |              0.0635 |                    0.3423 |
| JNJ     |      0.2 |                  0.0541 |              0.0108 |                    0.0584 |
| XOM     |      0.1 |                  0.0862 |              0.0086 |                    0.0465 |
| Total   |      1   |                nan      |              0.1855 |                    1      |

---

## get_stress_test
Calculate how a portfolio would have fared in historical market crises: the return of every asset and of the buy-and-hold portfolio from the start to the end of each scenario, next to the benchmark. The default scenarios run from the peak to the trough of the S&P 500: the Dot-com Crash, the Global Financial Crisis, the Euro Area Debt Crisis, the 2015-2016 and 2018 Q4 sell-offs, the COVID-19 Crash and the 2022 Rate Shock.

The prices are retrieved for each scenario, so the scenarios do not have to fall within the Toolkit's date range.

**Also known as:** historical scenario analysis, crisis replay, what-if analysis.

**Args:**

- <u>weights (dict[str, float] &#124; None, optional):</u> The weight per asset. Defaults to
None, which uses the latest weights of the Portfolio the Toolkit came from,
or equal weights.
- <u>scenarios (dict[str, tuple[str, str]] &#124; None, optional):</u> Custom scenarios as
{"name": ("start date", "end date")}. Defaults to None, the scenarios
above.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.

**Returns:**

pd.DataFrame: Per scenario its Start Date and End Date, the Portfolio Return,
the Benchmark Return, the Coverage (the share of the portfolio with prices in
the scenario) and the return of every asset.

**Notes:**

- An asset that was not listed yet at the start of a scenario has no return there;
the other weights are scaled up and the Coverage shows the share that had data.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "JNJ", "XOM"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.portfolio.get_stress_test()
```

Which returns:

| Scenario                | Start Date   | End Date   |   Portfolio Return |   Benchmark Return |   Coverage |    AAPL |    MSFT |     JNJ |     XOM |
|:------------------------|:-------------|:-----------|-------------------:|-------------------:|-----------:|--------:|--------:|--------:|--------:|
| Dot-com Crash           | 2000-03-24   | 2002-10-09 |            -0.22   |            -0.4751 |          1 | -0.8044 | -0.6061 |  0.6314 | -0.1009 |
| Global Financial Crisis | 2007-10-09   | 2009-03-09 |            -0.3836 |            -0.5519 |          1 | -0.504  | -0.4817 | -0.2658 | -0.2829 |
| Euro Area Debt Crisis   | 2011-04-29   | 2011-10-03 |            -0.0479 |            -0.1861 |          1 |  0.0697 | -0.0415 | -0.0386 | -0.1812 |
| 2015-2016 Sell-off      | 2015-05-21   | 2016-02-11 |            -0.0673 |            -0.1298 |          1 | -0.2769 |  0.0619 |  0.008  | -0.0624 |
| 2018 Q4 Sell-off        | 2018-09-20   | 2018-12-24 |            -0.2118 |            -0.1935 |          1 | -0.3303 | -0.1676 | -0.1292 | -0.2199 |
| COVID-19 Crash          | 2020-02-19   | 2020-03-23 |            -0.3271 |            -0.3372 |          1 | -0.3067 | -0.2739 | -0.2491 | -0.4789 |
| 2022 Rate Shock         | 2022-01-03   | 2022-10-12 |             0.0017 |            -0.245  |          1 | -0.2368 | -0.3212 | -0.0329 |  0.5976 |

---

## get_look_through_exposure
Calculate a portfolio's exposure after looking through its funds. An ETF's weight is spread over its own sectors, countries or holdings, a stock counts fully towards its own sector, country or itself, and everything is summed. It shows, for example, that a portfolio of a technology ETF and Apple holds far more Apple and technology than either position suggests. The benchmark's exposure and the difference (the active exposure) are shown next to it when the benchmark is a fund.

**Also known as:** look-through analysis, underlying exposure, X-ray.

**Args:**

- <u>weights (dict[str, float] &#124; None, optional):</u> The weight per asset. Defaults to
None, which uses the latest weights of the Portfolio the Toolkit came from,
or equal weights.
- <u>by (str, optional):</u> What to look through to: "sector", "country" or "holdings".
Defaults to "sector".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.

**Returns:**

pd.DataFrame: The Exposure per sector, country or holding, largest first, with
the Benchmark Exposure and Active Exposure where the benchmark is a fund.

**Notes:**

- Fund holdings lists often show only the largest positions; the rest is reported as
"Other". Assets without a known classification are "Unclassified".

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["QQQ", "AAPL", "XLE", "JNJ"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.portfolio.get_look_through_exposure()
```

Which returns:

| Sector                 |   Exposure |   Benchmark Exposure |   Active Exposure |
|:-----------------------|-----------:|---------------------:|------------------:|
| Technology             |     0.3965 |               0.3757 |            0.0208 |
| Healthcare             |     0.261  |               0.0994 |            0.1616 |
| Energy                 |     0.2512 |               0.0373 |            0.2139 |
| Communication Services |     0.029  |               0.0923 |           -0.0633 |
| Consumer Cyclical      |     0.0263 |               0.0896 |           -0.0633 |
| Consumer Defensive     |     0.0156 |               0.0495 |           -0.0339 |
| Industrials            |     0.0144 |               0.0803 |           -0.0659 |
| Utilities              |     0.0027 |               0.0204 |           -0.0177 |
| Basic Materials        |     0.0025 |               0.017  |           -0.0145 |
| Financial Services     |     0.0005 |               0.1208 |           -0.1203 |
| Cash & Others          |     0.0004 |               0      |            0.0004 |
| Real Estate            |     0      |               0.0175 |           -0.0175 |

---

## get_brinson_attribution
Calculate the Brinson-Fachler attribution of the portfolio's return over the benchmark, by sector, over the Toolkit's date range. The excess return is split into three effects per sector:

- Allocation: the reward for overweighting sectors that beat the benchmark (and underweighting those that lagged).
- Selection: the reward for holding better stocks than the benchmark within a sector.
- Interaction: the combined effect of both decisions.

The portfolio's sector returns come from its holdings (buy and hold from the start date). The benchmark's sector weights come from the benchmark fund and its sector returns from the Select Sector SPDR funds (XLK, XLF, XLV, ...), which track the sectors of the S&P 500.

For more information, see the following papers:

- Brinson, G.P. and Fachler, N. (1985). "Measuring Non-US Equity Portfolio Performance." The Journal of Portfolio Management, 11(3), 73-76.
- Brinson, G.P., Hood, L.R. and Beebower, G.L. (1986). "Determinants of Portfolio Performance." Financial Analysts Journal, 42(4), 39-44.

**Also known as:** performance attribution, BHB attribution, sector attribution.

**Args:**

- <u>weights (dict[str, float] &#124; None, optional):</u> The weight per asset at the start of
the date range. Defaults to None, which uses the latest weights of the
Portfolio the Toolkit came from, or equal weights.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.

**Returns:**

pd.DataFrame: Per sector and in total, the Portfolio Weight, Benchmark Weight,
Portfolio Return, Benchmark Return and the Allocation, Selection, Interaction
and Total Effect. The Total row's effects add up to the excess return.

**Notes:**

- The benchmark fund's sector weights are its current weights, applied to the whole
date range, and the sector funds stand in for the benchmark's sectors; for a
benchmark other than the S&P 500 this is an approximation.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "JNJ", "XOM", "JPM"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

toolkit.portfolio.get_brinson_attribution()
```

Which returns:

| Sector                 |   Portfolio Weight |   Benchmark Weight |   Portfolio Return |   Benchmark Return |   Allocation Effect |   Selection Effect |   Interaction Effect |   Total Effect |
|:-----------------------|-------------------:|-------------------:|-------------------:|-------------------:|--------------------:|-------------------:|---------------------:|---------------:|
| Basic Materials        |                0   |             0.017  |           nan      |             0.1115 |              0.0012 |             0      |              -0      |         0.0012 |
| Communication Services |                0   |             0.0923 |           nan      |             0.2249 |             -0.0042 |             0      |              -0      |        -0.0042 |
| Consumer Cyclical      |                0   |             0.0896 |           nan      |             0.0881 |              0.0082 |             0      |              -0      |         0.0082 |
| Consumer Defensive     |                0   |             0.0495 |           nan      |             0.0183 |              0.008  |             0      |              -0      |         0.008  |
| Energy                 |                0.2 |             0.0373 |             0.1625 |             0.0661 |             -0.0185 |             0.0036 |               0.0157 |         0.0008 |
| Financial Services     |                0.2 |             0.1208 |             0.371  |             0.152  |             -0.0022 |             0.0265 |               0.0173 |         0.0416 |
| Healthcare             |                0.2 |             0.0994 |             0.4809 |             0.1447 |             -0.0035 |             0.0334 |               0.0338 |         0.0637 |
| Industrials            |                0   |             0.0803 |           nan      |             0.1976 |             -0.0014 |             0      |              -0      |        -0.0014 |
| Real Estate            |                0   |             0.0175 |           nan      |             0.036  |              0.0025 |             0      |              -0      |         0.0025 |
| Technology             |                0.4 |             0.3758 |             0.1419 |             0.2489 |              0.0017 |            -0.0402 |              -0.0026 |        -0.0411 |
| Utilities              |                0   |             0.0204 |           nan      |             0.1511 |              0.0006 |             0      |              -0      |         0.0006 |
| Total                  |                1   |             1      |             0.2596 |             0.1798 |             -0.0077 |             0.0233 |               0.0642 |         0.0798 |

---

