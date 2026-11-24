---
title: Portfolio Optimization
seo_title: "Portfolio Optimization in Python | Finance Toolkit"
seo_title_suffix: false
excerpt: The Portfolio Optimization module builds portfolios from the tickers of a Toolkit, from minimum variance, maximum Sharpe ratio and risk parity weights to the efficient frontier, risk contributions, stress tests and attribution.
description: "Build minimum variance, maximum Sharpe and risk parity portfolios, plot the efficient frontier and run stress tests and attribution in Python."
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

{% include docs-search.html %}

{% include financetoolkit-getting-started/portfolio-optimization.md %}

## get_risk_contributions
Calculate how much each asset contributes to the risk of a portfolio.

The risk is measured as the volatility, expected shortfall (CVaR), semideviation, mean absolute deviation, Conditional Drawdown at Risk (CDaR) or one of the Risk module's tail, dispersion and drawdown measures. The marginal contribution is the change in the portfolio's risk from a small increase in an asset's weight; the risk contribution is the weight times that, and the contributions add up to the portfolio's risk (Euler allocation). A large position in a calm asset can contribute less risk than a small one in a volatile asset.

- The volatility: the marginal contribution is $$(\Sigma w)_{i} / \sigma_{p}$$, with $$\Sigma$$ the annualized covariance matrix.
- The expected shortfall is the average loss in the periods in which the portfolio's return is at or below its Value at Risk, and the marginal contribution of an asset is its average loss in those same periods, $$- E [r_{i} \vert r_{p} \leq \text{VaR}]$$, so the contributions show which assets lose in the portfolio's worst periods. These are per period (e.g. daily), like the Finance Toolkit's historical CVaR, and not annualized.
- The semideviation: the downside deviation of the portfolio's return below zero, $$\text{SD}^{-} = \sqrt{\sum \min (r_{p,t} , 0)^{2} / T}$$, with the marginal contribution $$\sum \min (r_{p,t} , 0) r_{i,t} / (T \text{SD}^{-})$$: an asset contributes by losing in the periods in which the portfolio loses. Per period, not annualized.
- The mean absolute deviation of the portfolio's return, $$\sum \vert r_{p,t} - \mu_{p} \vert / T$$, with the marginal contribution $$\sum \operatorname{sign} (r_{p,t} - \mu_{p}) (r_{i,t} - \mu_{i}) / T$$. Per period, not annualized.
- The Conditional Drawdown at Risk, the average of the worst $$\alpha$$ share of the drawdowns of the uncompounded cumulative return (the drawdowns the minimum drawdown optimization minimizes). Each drawdown is the sum of the assets' drawdowns from the portfolio's peak, so the marginal contribution of an asset is its average drawdown over the portfolio's worst drawdown periods (Goldberg and Mahmoud, 2017).
- The other measures: the historical Value at Risk and Entropic Value at Risk, the worst return, the Gini mean difference, the Tail Gini, the first lower partial moment below zero, the square root of the fourth central moment, and the maximum and average drawdown, Drawdown at Risk, Entropic Drawdown at Risk and Ulcer Index of the uncompounded cumulative return, as the Risk module calculates them, losses positive. The marginal contribution is found by central finite differences, $$(\rho (w + h e_{i}) - \rho (w - h e_{i})) / 2 h$$ with $$h = 1 e - 7$$ (1e-4 for the entropic measures); the risk contribution is the weight times that (half of it for the kurtosis measure, whose square root of the fourth moment doubles when the weights double twice over), so the contributions add up to the measure. Per period, not annualized.

**Also known as:** risk decomposition, marginal contribution to risk, risk budget, component expected shortfall, component CVaR, downside risk contribution, drawdown contribution.

**References:**

- paper | Litterman, R. (1997). "Hot Spots and Hedges." The Journal of Portfolio Management, 23(5), 52-75.
- paper | Tasche, D. (2000). "Conditional Expectations as Quantile Derivatives." Working paper, arXiv math/0104190.
- paper | Scaillet, O. (2004). "Nonparametric Estimation and Sensitivity Analysis of Expected Shortfall." Mathematical Finance, 14(1), 115-129.
- paper | Sortino, F. A. and Price, L. N. (1994). "Performance Measurement in a Downside Risk Framework." The Journal of Investing, 3(3), 59-64.
- paper | Konno, H. and Yamazaki, H. (1991). "Mean-Absolute Deviation Portfolio Optimization Model and Its Applications to Tokyo Stock Market." Management Science, 37(5), 519-531.
- paper | Goldberg, L. R. and Mahmoud, O. (2017). "Drawdown: From Practice to Theory and Back Again." Mathematics and Financial Economics, 11(3), 275-297.
- library | Referenced against Riskfolio-Lib's [Risk_Contribution](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/risk.html#RiskFunctions.Risk_Contribution){:target="_blank"} (CVaR)
- library | Referenced against Riskfolio-Lib's [Risk_Contribution](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/risk.html#RiskFunctions.Risk_Contribution){:target="_blank"} (other risk measures)
- library | Shares similar logic as Riskfolio-Lib's [Risk_Contribution](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/risk.html#RiskFunctions.Risk_Contribution){:target="_blank"} (volatility)

**Args:**

- <u>weights (dict[str, float] &#124; None, optional):</u> The weight per asset. Defaults to
None, which uses the latest weights of the Portfolio the Toolkit came from,
or equal weights.
- <u>risk_measure (str, optional):</u> The risk measure. Options are: "volatility" (of the covariance estimate),
"cvar" (the expected shortfall), "semideviation" (below a return of zero), "mad" (the mean absolute
deviation), "cdar" (the Conditional Drawdown at Risk), "var" (historical Value at Risk), "evar"
(Entropic Value at Risk), "worst_realization" (the largest loss), "gini_mean_difference" (Gini mean
difference), "tail_gini" (Tail Gini), "lower_partial_moment" (first lower partial moment below
zero), "kurtosis" (square root of the fourth central moment), "maximum_drawdown" (maximum drawdown),
"average_drawdown" (average drawdown), "drawdown_at_risk" (Drawdown at Risk),
"entropic_drawdown_at_risk" (Entropic Drawdown at Risk), "ulcer_index" (Ulcer Index). Defaults to
"volatility".
- <u>alpha (float, optional):</u> The tail probability of the tail measures (the
expected shortfall, CDaR, VaR, EVaR, Tail Gini, Drawdown at Risk and EDaR),
e.g. 0.05 for the worst 5% of periods or drawdowns. Defaults to 0.05.
- <u>period (str, optional):</u> The frequency of the returns. Options are: "daily" (daily returns), "weekly"
(weekly returns), "monthly" (monthly returns), "quarterly" (quarterly returns), "yearly" (yearly
returns). Defaults to "daily".
- <u>covariance (str, optional):</u> The estimator of the covariance matrix. The shrinkage and denoised
estimators stabilize the weights when there are many assets compared to the number of periods.
Options are: "sample" (the sample covariance, ddof=1), "ledoit_wolf" (shrunk towards the scaled
identity, Ledoit and Wolf, 2004), "ledoit_wolf_constant_correlation" (shrunk towards the average
correlation, Ledoit and Wolf, 2004), "ledoit_wolf_single_factor" (shrunk towards the covariance that
the benchmark as a single factor implies, Ledoit and Wolf, 2003), "oas" (Oracle Approximating
Shrinkage, Chen et al., 2010), "shrunk" (a fixed 10% towards the scaled identity), "semicovariance"
(the co-movement below a zero return, Estrada, 2008), "exponential" (exponentially weighted, recent
periods weigh most, RiskMetrics), "denoised" (the eigenvalues of the correlation matrix that random
returns could produce averaged, Laloux et al., 2000), "denoised_spectral" (those eigenvalues set to
zero), "denoised_shrink" (the noise correlations shrunk towards their diagonal, López de Prado,
2020), "gerber" (co-movements beyond half a standard deviation, Gerber et al., 2022), "factor" (the
covariance of the Fama and French five factor model with OLS loadings, Fama and French, 1993),
"minimum_covariance_determinant" (the reweighted covariance of the half of the periods with the
smallest covariance determinant, robust to outliers, Rousseeuw and Van Driessen, 1999), "jlogo" (the
sparse inverse covariance on the TMFG planar graph of the correlations, Barfuss et al., 2016),
"geodesic" (10% towards the scaled identity along the geodesic of the positive definite matrices,
Bhatia, 2007), "regime_adjusted_ew" (exponentially weighted with a half-life of 40 periods, rescaled
by the recent realized against predicted risk, Paleologo, 2025), "nercome" (eigenvectors from one
part of the periods and the variances along them from the other, averaged over random splits, Lam,
2016), "ccc_garch" (the next-period covariance of GARCH(1, 1) volatilities with constant
correlations, Bollerslev, 1990), "mm" (the robust MM-estimator, Maronna et al., 2019), "rocke"
(Rocke's robust S-estimator, Maronna et al., 2019). Defaults to "sample".
- <u>covariance_span (int, optional):</u> The span in periods of the exponentially weighted covariance; the
weight of a period halves after about span / 2.9 periods. Defaults to 180.
- <u>include_benchmark (bool, optional):</u> Whether to include the benchmark as an
asset. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per asset and in total, the Weight, Marginal Contribution, Risk
Contribution and Percentage Contribution: annualized volatility terms, or per period
terms of the other measures, with losses and drawdowns positive. For the kurtosis
measure the marginal contribution is the derivative of the measure and the risk
contribution half the weight times it. The assets held (a weight other than zero)
are listed, over the periods in which each of them has a return; a loaded asset
without weight does not shorten the sample.

**Notes:**

- The Value at Risk and Drawdown at Risk are the Risk module's quantiles, interpolated
between two periods, where Riskfolio-Lib takes a single period (the $$\text{⌈} \alpha T \text{⌉} - th$$ worst), so
their contributions mix two periods and differ from Riskfolio-Lib's; the other
measures match Riskfolio-Lib's to 1e-8.

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
    weights={"AAPL": 0.4, "MSFT": 0.3, "JNJ": 0.2, "XOM": 0.1},
    risk_measure="cvar",
)
```

Which returns:

| Asset   |   Weight |   Marginal Contribution |   Risk Contribution |   Percentage Contribution |
|:--------|---------:|------------------------:|--------------------:|--------------------------:|
| AAPL    |      0.4 |                  0.0352 |              0.0141 |                    0.5365 |
| MSFT    |      0.3 |                  0.0306 |              0.0092 |                    0.3492 |
| JNJ     |      0.2 |                  0.0082 |              0.0016 |                    0.0625 |
| XOM     |      0.1 |                  0.0136 |              0.0014 |                    0.0518 |
| Total   |      1   |                nan      |              0.0263 |                    1      |

---

## get_diversification_metrics
Calculate how diversified a portfolio is, by the concentration of its weights and by how its risk spreads over independent sources.

- Herfindahl-Hirschman Index: $$\sum w_{i}^{2}$$, from 1/N for equal weights to 1 for a single asset.
- Effective Number of Assets: $$1 / \sum w_{i}^{2}$$, the number of equally weighted assets that would be as concentrated.
- Diversification Ratio: the weighted average volatility of the assets over the portfolio's volatility, $$w' \sigma / \sqrt{w' \Sigma w}$$; one for a single asset, higher as the assets move less together (Choueifaty and Coignard, 2008).
- Effective Number of Bets: the covariance matrix is split into uncorrelated principal components, $$p_{k}$$ is the share of the portfolio's variance from component k, and the number of bets is $$\exp (- \sum p_{k} \ln p_{k})$$: 1 when all risk comes from one source and N when it spreads evenly over all of them (Meucci, 2009). Equal weights in assets that all follow the market are many assets but close to one bet.

**Also known as:** concentration, HHI, effective N, ENB, diversification ratio.

**References:**

- paper | Choueifaty, Y. and Coignard, Y. (2008). "Toward Maximum Diversification." The Journal of Portfolio Management, 35(1), 40-51.
- paper | Meucci, A. (2009). "Managing Diversification." Risk, 22(5), 74-79.
- library | Referenced against skfolio's [Portfolio](https://skfolio.org/generated/skfolio.portfolio.Portfolio.html){:target="_blank"} (diversification and effective_number_assets)

**Args:**

- <u>weights (dict[str, float] &#124; None, optional):</u> The weight per asset. Defaults to
None, which uses the latest weights of the Portfolio the Toolkit came from,
or equal weights.
- <u>period (str, optional):</u> The frequency of the returns. Options are: "daily" (daily returns), "weekly"
(weekly returns), "monthly" (monthly returns), "quarterly" (quarterly returns), "yearly" (yearly
returns). Defaults to "daily".
- <u>covariance (str, optional):</u> The estimator of the covariance matrix. The shrinkage and denoised
estimators stabilize the weights when there are many assets compared to the number of periods.
Options are: "sample" (the sample covariance, ddof=1), "ledoit_wolf" (shrunk towards the scaled
identity, Ledoit and Wolf, 2004), "ledoit_wolf_constant_correlation" (shrunk towards the average
correlation, Ledoit and Wolf, 2004), "ledoit_wolf_single_factor" (shrunk towards the covariance that
the benchmark as a single factor implies, Ledoit and Wolf, 2003), "oas" (Oracle Approximating
Shrinkage, Chen et al., 2010), "shrunk" (a fixed 10% towards the scaled identity), "semicovariance"
(the co-movement below a zero return, Estrada, 2008), "exponential" (exponentially weighted, recent
periods weigh most, RiskMetrics), "denoised" (the eigenvalues of the correlation matrix that random
returns could produce averaged, Laloux et al., 2000), "denoised_spectral" (those eigenvalues set to
zero), "denoised_shrink" (the noise correlations shrunk towards their diagonal, López de Prado,
2020), "gerber" (co-movements beyond half a standard deviation, Gerber et al., 2022), "factor" (the
covariance of the Fama and French five factor model with OLS loadings, Fama and French, 1993),
"minimum_covariance_determinant" (the reweighted covariance of the half of the periods with the
smallest covariance determinant, robust to outliers, Rousseeuw and Van Driessen, 1999), "jlogo" (the
sparse inverse covariance on the TMFG planar graph of the correlations, Barfuss et al., 2016),
"geodesic" (10% towards the scaled identity along the geodesic of the positive definite matrices,
Bhatia, 2007), "regime_adjusted_ew" (exponentially weighted with a half-life of 40 periods, rescaled
by the recent realized against predicted risk, Paleologo, 2025), "nercome" (eigenvectors from one
part of the periods and the variances along them from the other, averaged over random splits, Lam,
2016), "ccc_garch" (the next-period covariance of GARCH(1, 1) volatilities with constant
correlations, Bollerslev, 1990), "mm" (the robust MM-estimator, Maronna et al., 2019), "rocke"
(Rocke's robust S-estimator, Maronna et al., 2019). Defaults to "sample".
- <u>covariance_span (int, optional):</u> The span in periods of the exponentially weighted covariance; the
weight of a period halves after about span / 2.9 periods. Defaults to 180.
- <u>include_benchmark (bool, optional):</u> Whether to include the benchmark as an
asset. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series: The Herfindahl-Hirschman Index, Effective Number of Assets,
Diversification Ratio and Effective Number of Bets of the portfolio, from
the covariance of the assets held (a weight other than zero) over the periods
in which each of them has a return.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "JNJ", "XOM"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.portfolio.get_diversification_metrics(
    weights={"AAPL": 0.4, "MSFT": 0.3, "JNJ": 0.2, "XOM": 0.1}
)
```

Which returns:

|                            |   Portfolio |
|:---------------------------|------------:|
| Herfindahl-Hirschman Index |      0.3    |
| Effective Number of Assets |      3.3333 |
| Diversification Ratio      |      1.343  |
| Effective Number of Bets   |      1.1298 |

---

## get_portfolio_risk_metrics
Calculate the return and risk of a portfolio with given weights over the Toolkit's date range, next to the benchmark.

The portfolio's return in each period is the weighted return of its assets, $$r_{p,t} = \sum w_{i} r_{i,t}$$, which holds the weights constant by rebalancing to them every period. The measures use the formulas of the Performance and Risk modules:

$$
\text{Annualized Return:}\;\; \text{the geometric average},\;\; \prod(1 + r_{t})^{\frac{P}{T}} - 1,\;\; \text{with } P \text{ the periods per year and } T \text{ the number of periods}
$$

- Annualized Volatility: the standard deviation (ddof=1) times $$\sqrt{P}$$.

- Sharpe Ratio: the average return above the risk free rate over its standard deviation, annualized with $$\sqrt{P}$$ (Sharpe, 1966).

- Sortino Ratio: the average return above the risk free rate over its downside deviation below zero, annualized with $$\sqrt{P}$$ (Sortino and Price, 1994).

- Maximum Drawdown: the largest fall of the compounded value from its peak.

- Value at Risk: the $$\alpha$$ quantile of the returns per period (historical).

- Conditional Value at Risk: the average return at or below the Value at Risk per period (historical).

Losses, drawdowns, the Value at Risk and the Conditional Value at Risk are negative returns, as in the Risk module.

**Also known as:** portfolio risk report, risk summary, risk metrics of weights.

**References:**

- paper | Sharpe, W. F. (1966). "Mutual Fund Performance." The Journal of Business, 39(1), 119-138.
- paper | Sortino, F. A. and Price, L. N. (1994). "Performance Measurement in a Downside Risk Framework." The Journal of Investing, 3(3), 59-64.
- paper | Rockafellar, R. T. and Uryasev, S. (2002). "Conditional Value-at-Risk for General Loss Distributions." Journal of Banking & Finance, 26(7), 1443-1471.

**Args:**

- <u>weights (dict[str, float] &#124; None, optional):</u> The weight per asset. Defaults to
None, which uses the latest weights of the Portfolio the Toolkit came from,
or equal weights.
- <u>alpha (float, optional):</u> The tail probability of the Value at Risk and the
Conditional Value at Risk, e.g. 0.05 for the worst 5% of periods.
Defaults to 0.05.
- <u>period (str, optional):</u> The frequency of the returns. Options are: "daily" (daily returns), "weekly"
(weekly returns), "monthly" (monthly returns), "quarterly" (quarterly returns), "yearly" (yearly
returns). Defaults to "daily".
- <u>include_benchmark (bool, optional):</u> Whether to include the benchmark as an
asset. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The Annualized Return, Annualized Volatility, Sharpe Ratio,
Sortino Ratio, Maximum Drawdown, Value at Risk and Conditional Value at Risk of
the Portfolio and, when there is one, the Benchmark over the same periods:
those in which every asset held (a weight other than zero) has a return, so a
loaded asset without weight does not shorten the sample.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "JNJ", "XOM"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.portfolio.get_portfolio_risk_metrics(
    weights={"AAPL": 0.4, "MSFT": 0.3, "JNJ": 0.2, "XOM": 0.1}
)
```

Which returns:

|                           |   Portfolio |   Benchmark |
|:--------------------------|------------:|------------:|
| Annualized Return         |      0.1847 |      0.1472 |
| Annualized Volatility     |      0.1855 |      0.1711 |
| Sharpe Ratio              |      0.8247 |      0.6912 |
| Sortino Ratio             |      1.211  |      0.996  |
| Maximum Drawdown          |     -0.1977 |     -0.245  |
| Value at Risk             |     -0.0185 |     -0.0166 |
| Conditional Value at Risk |     -0.0263 |     -0.0248 |

---

## get_discrete_allocation
Calculate how many whole shares to buy of each asset to hold weights with a portfolio value, at the latest traded (split-adjusted) closing price.

Weights rarely come out in whole shares, so some cash is left over and the weights held differ a little from the targets; the smaller the portfolio value compared to the share prices, the larger the difference. With $$t_{i} = w_{i} V$$ the target amount of asset i and $$p_{i}$$ its price:

- The integer programme: the number of shares $$n_{i}$$ that minimizes the absolute deviation from the target amounts with the leftover cash c counted as a holding with a target of zero, $$\min \sum \vert t_{i} - n_{i} p_{i} \vert + c$$ with $$\sum n_{i} p_{i} + c = V$$ and $$c \geq 0$$, solved as an integer programme (Cornuejols, Peña and Tütüncü, 2018).
- The greedy allocation: every position is first rounded down to whole shares and the leftover cash then buys one more share at a time of the asset furthest below its target amount, while its price fits the cash. Quick and close to the integer programme, which can do better by leaving out a share of one asset to buy more of another.

A short weight becomes a negative number of shares, with the proceeds funding the long positions: weights that sum to one keep a net investment of the portfolio value. Short positions are rounded to a larger short, so the leftover cash is never negative. The integer programme holds a long position at no more than the whole shares that reach its target, but leaves the size of a short position open: one more share short raises the cash for a long share that is further below its own target, which can lower the total deviation.

**Also known as:** share allocation, whole share rounding, lot sizing, order sizes.

**References:**

- paper | Cornuejols, G., Peña, J. and Tütüncü, R. (2018). "Optimization Methods in Finance." 2nd edition, Cambridge University Press.
- library | Shares similar logic as PyPortfolioOpt's [DiscreteAllocation.lp_portfolio](https://pyportfolioopt.readthedocs.io/en/latest/Postprocessing.html#pypfopt.discrete_allocation.DiscreteAllocation.lp_portfolio){:target="_blank"} (integer programme)
- library | Shares similar logic as PyPortfolioOpt's [DiscreteAllocation.greedy_portfolio](https://pyportfolioopt.readthedocs.io/en/latest/Postprocessing.html#pypfopt.discrete_allocation.DiscreteAllocation.greedy_portfolio){:target="_blank"} (greedy allocation)

**Args:**

- <u>weights (dict[str, float] &#124; None, optional):</u> The weight per asset, e.g. those
of one of the optimizers. Defaults to None, which uses the latest weights
of the Portfolio the Toolkit came from, or equal weights.
- <u>portfolio_value (float, optional):</u> The amount to invest, in the currency of
the prices. Defaults to 10000.
- <u>method (str, optional):</u> Options are: "integer" (the integer programme), "greedy" (the greedy
allocation). Defaults to "integer".
- <u>include_benchmark (bool, optional):</u> Whether to include the benchmark as an
asset. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per asset the Price, Shares, Amount (shares times price),
Target Weight and Weight held (the amount over the portfolio value), a
Leftover Cash row and a Total row that sums to the portfolio value.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "JNJ", "XOM"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

weights = toolkit.portfolio.get_maximum_sharpe_weights()["Weight"]

toolkit.portfolio.get_discrete_allocation(
    weights=weights.drop("Portfolio").to_dict(), portfolio_value=25000
)
```

Which returns:

| Asset         |   Price |   Shares |   Amount |   Target Weight |   Weight |
|:--------------|--------:|---------:|---------:|----------------:|---------:|
| AAPL          |  271.86 |        1 |   271.86 |          0.014  |   0.0109 |
| MSFT          |  483.62 |       16 |  7737.92 |          0.3121 |   0.3095 |
| JNJ           |  206.95 |       24 |  4966.8  |          0.1998 |   0.1987 |
| XOM           |  120.34 |       99 | 11913.7  |          0.4741 |   0.4765 |
| Leftover Cash |  nan    |      nan |   109.76 |          0      |   0.0044 |
| Total         |  nan    |      nan | 25000    |          1      |   1      |

---

## get_optimization_backtest
Backtest the portfolio optimizers out of sample against equal weights (1/N) and the benchmark.

On every rebalancing date (the last trading day of each month, quarter or year) each optimizer sets its weights from the daily returns of the `lookback` trading days up to and including that date, and the portfolio holds them from the next day on, so no weight is estimated with a return it is then measured on (walk-forward). Between rebalancing dates the weights drift with the prices, as those of a portfolio that does not trade. The 1/N portfolio is rebalanced to equal weights on the same dates and the benchmark is bought and held.

Each rebalancing trades from the drifted weights to the new ones. Its turnover is $$\sum \vert w_{i,\text{new}} - w_{i,\text{drifted}} \vert$$ and its cost the transaction cost times the turnover, taken from the portfolio's value, so the returns shown are after costs (DeMiguel, Garlappi and Uppal, 2009). With a maximum turnover, a portfolio trades towards its new weights only as far as the limit allows. DeMiguel et al. found that none of fourteen optimizers consistently beat 1/N out of sample, because the estimation error in the expected returns outweighs the gain from optimizing; a backtest shows whether that holds for these assets.

**Also known as:** walk-forward backtest, out-of-sample backtest, rolling optimization, 1/N comparison.

**References:**

- paper | DeMiguel, V., Garlappi, L. and Uppal, R. (2009). "Optimal Versus Naive Diversification: How Inefficient Is the 1/N Portfolio Strategy?" The Review of Financial Studies, 22(5), 1915-1953.
- paper | Konno, H. and Yamazaki, H. (1991). "Mean-Absolute Deviation Portfolio Optimization Model and Its Applications to Tokyo Stock Market." Management Science, 37(5), 519-531.
- paper | Estrada, J. (2008). "Mean-Semivariance Optimization: A Heuristic Approach." Journal of Applied Finance, 18(1), 57-72.
- paper | Rubin, D. B. (1981). "The Bayesian Bootstrap." The Annals of Statistics, 9(1), 130-134.

**Args:**

- <u>methods (list[str] &#124; str &#124; None, optional):</u> The optimizers to backtest, as a list or comma separated.
Options are: "minimum_variance" (Minimum Variance), "maximum_sharpe" (Maximum Sharpe),
"mean_variance" (a risk aversion of 2.5), "risk_parity" (Risk Parity), "hierarchical_risk_parity"
(Hierarchical Risk Parity), "inverse_volatility" (Inverse Volatility), "maximum_diversification"
(Maximum Diversification), "hierarchical_equal_risk_contribution" (Hierarchical Equal Risk
Contribution), "nested_clustered_optimization" (minimum variance within and across the clusters),
"minimum_cvar" (95%), "minimum_drawdown" (the 95% CDaR), "maximum_omega" (a minimum acceptable
return of 0), "maximum_cvar_ratio" (95%), "minimum_mad" (the lowest mean absolute deviation, Konno
and Yamazaki, 1991), "minimum_semideviation" (the lowest semideviation below a return of 0, Estrada,
2008), "random" (weights drawn uniformly from all long-only portfolios, a flat Dirichlet, with a
generator seeded at 0 so the backtest is reproducible), "equal_weight" (Equal Weight). Equal weights
and the benchmark are always included. Defaults to None, which backtests minimum variance, maximum
Sharpe, risk parity, Hierarchical Risk Parity, maximum diversification and inverse volatility.
- <u>rebalancing (str, optional):</u> How often the weights are set anew. Options are: "monthly" (every month),
"quarterly" (every quarter), "yearly" (every year). Defaults to "monthly".
- <u>lookback (int, optional):</u> The number of daily returns each estimation uses.
The backtest starts on the first rebalancing date with that many returns
up to and including it. Defaults to 252, a year of trading days.
- <u>transaction_cost (float, optional):</u> The cost per unit of weight traded, e.g.
0.001 for 10 basis points. The first investment is free, so every
portfolio starts from the same value. Defaults to 0.
- <u>maximum_turnover (float &#124; None, optional):</u> The highest turnover of a
rebalancing, e.g. 0.2. Defaults to None, no limit.
- <u>covariance (str, optional):</u> The estimator of the covariance matrix. The shrinkage and denoised
estimators stabilize the weights when there are many assets compared to the number of periods.
Options are: "sample" (the sample covariance, ddof=1), "ledoit_wolf" (shrunk towards the scaled
identity, Ledoit and Wolf, 2004), "ledoit_wolf_constant_correlation" (shrunk towards the average
correlation, Ledoit and Wolf, 2004), "ledoit_wolf_single_factor" (shrunk towards the covariance that
the benchmark as a single factor implies, Ledoit and Wolf, 2003), "oas" (Oracle Approximating
Shrinkage, Chen et al., 2010), "shrunk" (a fixed 10% towards the scaled identity), "semicovariance"
(the co-movement below a zero return, Estrada, 2008), "exponential" (exponentially weighted, recent
periods weigh most, RiskMetrics), "denoised" (the eigenvalues of the correlation matrix that random
returns could produce averaged, Laloux et al., 2000), "denoised_spectral" (those eigenvalues set to
zero), "denoised_shrink" (the noise correlations shrunk towards their diagonal, López de Prado,
2020), "gerber" (co-movements beyond half a standard deviation, Gerber et al., 2022), "factor" (the
covariance of the Fama and French five factor model with OLS loadings, Fama and French, 1993),
"minimum_covariance_determinant" (the reweighted covariance of the half of the periods with the
smallest covariance determinant, robust to outliers, Rousseeuw and Van Driessen, 1999), "jlogo" (the
sparse inverse covariance on the TMFG planar graph of the correlations, Barfuss et al., 2016),
"geodesic" (10% towards the scaled identity along the geodesic of the positive definite matrices,
Bhatia, 2007), "regime_adjusted_ew" (exponentially weighted with a half-life of 40 periods, rescaled
by the recent realized against predicted risk, Paleologo, 2025), "nercome" (eigenvectors from one
part of the periods and the variances along them from the other, averaged over random splits, Lam,
2016), "ccc_garch" (the next-period covariance of GARCH(1, 1) volatilities with constant
correlations, Bollerslev, 1990), "mm" (the robust MM-estimator, Maronna et al., 2019), "rocke"
(Rocke's robust S-estimator, Maronna et al., 2019). Defaults to "sample".
- <u>covariance_span (int, optional):</u> The span in periods of the exponentially weighted covariance; the
weight of a period halves after about span / 2.9 periods. Defaults to 180.
- <u>expected_returns (str, optional):</u> The estimator of the expected returns. Options are: "mean" (the
historical average), "geometric" (the compounded average), "exponential" (the exponentially weighted
average, recent periods weigh most), "exponential_geometric" (that average compounded over a year),
"capm" (the returns the Capital Asset Pricing Model implies from each asset's beta to the benchmark,
Sharpe, 1964), "bayes_stein" (the averages shrunk towards that of the minimum variance portfolio,
Jorion, 1986), "james_stein" (the averages shrunk towards their grand mean, James and Stein, 1961),
"bodnar_okhrin_parolya" (the averages and their grand mean combined with optimal weights, Bodnar,
Okhrin and Parolya, 2019). Defaults to "mean".
- <u>expected_returns_span (int, optional):</u> The span in periods of the exponentially weighted expected
returns. Defaults to 180.
- <u>minimum_weight (float &#124; dict[str, float], optional):</u> The lowest weight of
every asset, or per asset, for the optimizers that take weight bounds (all
but inverse volatility, nested clustered optimization and random).
Defaults to 0.
- <u>maximum_weight (float &#124; dict[str, float], optional):</u> The highest weight of
every asset, or per asset, for the optimizers that take weight bounds.
Defaults to 1.
- <u>output (str, optional):</u> Options are: "summary" (the performance of each portfolio), "returns" (the daily
returns after costs), "weights" (the weights set on each rebalancing date). Defaults to "summary".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: For the summary, per portfolio the Annualized Return
(geometric), Annualized Volatility, Sharpe Ratio (the annualized average return
above the risk free rate over the volatility), Maximum Drawdown, Average
Turnover per rebalancing, Annualized Costs, and the In-Sample Return and
In-Sample Sharpe Ratio: what the weights expected when they were set (see the
Notes). For the returns, the
daily returns after costs of every portfolio and the benchmark. For
the weights, the weights each optimizer set on each rebalancing date.

**Notes:**

- The returns are daily total returns (from adjusted closing prices). The
estimates use the days on which every asset has a return; the portfolios earn
the returns of every day, so a day on which one market is closed (its assets
return 0%, the next day covers both) still counts for the others, up to the
last day of the data. An asset whose returns end earlier (delisted or
acquired) ends the estimates and rebalancing on its last return; the portfolios
then hold it at 0% up to the end, and a warning says so. Each portfolio and the
benchmark are measured over the days they have a return.
- Returns on every calendar day (such as those of cryptocurrencies, with returns
on Saturdays and Sundays) are annualized with 365 days a year, returns on
trading days with 252, for the estimates and for each portfolio and the
benchmark on its own.
- When an optimizer finds no weights on a rebalancing date (e.g. the maximum Sharpe
ratio when no asset beat the risk free rate over the lookback), the portfolio
keeps its drifted weights until the next date, and a warning says how often.
Before its first weights it holds nothing and has no returns, so it starts
later than the others, and with weight bounds no portfolio meets it has no
returns at all.
- The In-Sample Return is the average over the rebalancing dates of w · mu, the
annualized return the weights set on a date expected from the estimates of
their own window (with the chosen expected return and covariance estimators),
and the In-Sample Sharpe Ratio the average of (w · mu - rf) / sqrt(w' Sigma w).
This is the promise an optimizer makes, on the same dates as the realised
return next to it, so the gap between the two is the estimation error that
DeMiguel et al. describe. The in-sample return is arithmetic, the realised
Annualized Return geometric, which is lower by about half the variance.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "JNJ", "XOM"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.portfolio.get_optimization_backtest(transaction_cost=0.001)
```

Which returns:

| Portfolio                |   Annualized Return |   Annualized Volatility |   Sharpe Ratio |   Maximum Drawdown |   Average Turnover |   Annualized Costs |   In-Sample Return |   In-Sample Sharpe Ratio |
|:-------------------------|--------------------:|------------------------:|---------------:|-------------------:|-------------------:|-------------------:|-------------------:|-------------------------:|
| Minimum Variance         |              0.0891 |                  0.1375 |         0.4061 |            -0.1268 |             0.0667 |             0.0008 |             0.1163 |                   0.6525 |
| Maximum Sharpe           |              0.0828 |                  0.2124 |         0.2971 |            -0.2776 |             0.4378 |             0.0052 |             0.3317 |                   1.4328 |
| Risk Parity              |              0.1242 |                  0.1469 |         0.6056 |            -0.1439 |             0.0428 |             0.0005 |             0.1429 |                   0.7982 |
| Hierarchical Risk Parity |              0.1003 |                  0.1382 |         0.4784 |            -0.135  |             0.0474 |             0.0006 |             0.1176 |                   0.6484 |
| Maximum Diversification  |              0.1225 |                  0.1426 |         0.6085 |            -0.1357 |             0.0617 |             0.0007 |             0.1468 |                   0.8404 |
| Inverse Volatility       |              0.122  |                  0.151  |         0.5798 |            -0.1484 |             0.0415 |             0.0005 |             0.1408 |                   0.7745 |
| Equal Weight             |              0.1407 |                  0.1624 |         0.6519 |            -0.1594 |             0.0388 |             0.0005 |             0.1582 |                   0.8381 |
| Benchmark                |              0.1285 |                  0.1799 |         0.545  |            -0.221  |           nan      |           nan      |           nan      |                 nan      |

---

## get_expected_returns_estimate
Estimate the annualized expected return of every asset with every estimator the optimizers take, side by side.

It shows how much the choice moves the input that mean-variance weights are most sensitive to.

- Mean: the historical average return per period times P, the number of periods in a year.
- Geometric: the compounded average, $$(\Pi (1 + r_{t}))^{P / T} - 1$$ over the T periods.
- Exponential: the exponentially weighted average with $$\alpha = 2$$ / (span + 1), times P.
- Exponential Geometric: that average compounded, (1 + m)^P - 1.
- CAPM: $$r_{f} + \beta_{i} (E [r_{m}] - r_{f})$$ with the benchmark as the market (Sharpe, 1964).
- Bayes-Stein: the averages shrunk towards the average return of the minimum variance portfolio, $$\mu = (1 - \phi) \hat{\mu} + \phi \mu_{0} 1$$ with $$\phi = (N + 2) / ((N + 2) + T (\hat{\mu} - \mu_{0} 1)' \Sigma^{- 1} (\hat{\mu} - \mu_{0} 1))$$ and $$\Sigma = S (T - 1) / (T - N - 2)$$ (Jorion, 1986).
- James-Stein: the averages shrunk towards their grand mean $$\bar{\mu}$$, $$\mu = (1 - \beta) \hat{\mu} + \beta \bar{\mu} 1$$ with $$\beta = (\sum \lambda_{k} - 2 \max \lambda_{k}) / (T \text{‖} \hat{\mu} - \bar{\mu} 1 \text{‖}^{2})$$ clipped to [0, 1] and $$\lambda_{k}$$ the eigenvalues of the sample covariance.
- Bodnar-Okhrin-Parolya: $$\mu = \alpha \hat{\mu} + \beta b$$ with the grand mean as the target b and the weights $$\alpha$$ and $$\beta$$ of Bodnar, Okhrin and Parolya (2019).
- Centroid: the returns that only an ordering of the assets implies (Almgren and Chriss, 2006), $$\mu_{i} = c_{i} \sigma_{i}$$ with $$\sigma_{i}$$ the annualized volatility and $$c_{i}$$ the expected value of the i-th largest of N standard normal draws, approximated by $$c_{j} = \Phi^{- 1} ((N + 1 - j - \alpha) / (N - 2 \alpha + 1))$$ with $$\alpha = 0.4424 - 0.1185 N^{- 0.21}$$; assets ranked together share the average c of their positions. It takes the ranking, from the highest expected return to the lowest, from anywhere: a view, or the scores of any metric of the Toolkit.

**Also known as:** shrunk mu, shrinkage expected returns, CAGR, geometric mean return, centroid returns, ranking returns, returns from an ordering.

**References:**

- paper | James, W. and Stein, C. (1961). "Estimation with Quadratic Loss." Proceedings of the Fourth Berkeley Symposium on Mathematical Statistics and Probability, 1, 361-379.
- paper | Jorion, P. (1986). "Bayes-Stein Estimation for Portfolio Analysis." Journal of Financial and Quantitative Analysis, 21(3), 279-292.
- paper | Bodnar, T., Okhrin, O. and Parolya, N. (2019). "Optimal Shrinkage Estimator for High-Dimensional Mean Vector." Journal of Multivariate Analysis, 170, 63-79.
- paper | Almgren, R. and Chriss, N. (2006). "Optimal Portfolios from Ordering Information." Journal of Risk, 9(1), 1-47.
- library | Referenced against PyPortfolioOpt's [mean_historical_return](https://pyportfolioopt.readthedocs.io/en/latest/ExpectedReturns.html#pypfopt.expected_returns.mean_historical_return){:target="_blank"} (geometric average)
- library | Referenced against PyPortfolioOpt's [ema_historical_return](https://pyportfolioopt.readthedocs.io/en/latest/ExpectedReturns.html#pypfopt.expected_returns.ema_historical_return){:target="_blank"} (exponentially weighted averages)
- library | Referenced against PyPortfolioOpt's [capm_return](https://pyportfolioopt.readthedocs.io/en/latest/ExpectedReturns.html#pypfopt.expected_returns.capm_return){:target="_blank"} (CAPM return)
- library | Referenced against Riskfolio-Lib's [mean_vector](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/parameters.html#ParamsEstimation.mean_vector){:target="_blank"} (the exponential recursion)
- library | Referenced against skfolio's [ShrunkMu](https://skfolio.org/generated/skfolio.moments.ShrunkMu.html){:target="_blank"} (James-Stein)
- library | Referenced against skfolio's [ShrunkMu](https://skfolio.org/generated/skfolio.moments.ShrunkMu.html){:target="_blank"} (Bodnar-Okhrin)
- library | Shares similar logic as skfolio's [ShrunkMu](https://skfolio.org/generated/skfolio.moments.ShrunkMu.html){:target="_blank"} (Bayes-Stein)
- library | Shares similar logic as Riskfolio-Lib's [mean_vector](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/parameters.html#ParamsEstimation.mean_vector){:target="_blank"} (James-Stein)
- library | Shares similar logic as Riskfolio-Lib's [mean_vector](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/parameters.html#ParamsEstimation.mean_vector){:target="_blank"} (Bodnar-Okhrin-Parolya)
- library | Shares similar logic as PortfolioAnalytics (R)'s [ac.ranking](https://github.com/cran/PortfolioAnalytics/blob/2.1.2/R/ac_ranking.R#L31){:target="_blank"} (centroid)
- library | Shares similar logic as PortfolioAnalytics (R)'s [centroid.complete.mc](https://github.com/cran/PortfolioAnalytics/blob/2.1.2/R/ac_ranking.R#L97){:target="_blank"} (centroid)

**Args:**

- <u>method (str &#124; list[str] &#124; None, optional):</u> The estimators. Options are: "mean" (the historical average),
"geometric" (the compounded average), "exponential" (the exponentially weighted average, recent
periods weigh most), "exponential_geometric" (that average compounded over a year), "capm" (the
returns the Capital Asset Pricing Model implies from each asset's beta to the benchmark, Sharpe,
1964), "bayes_stein" (the averages shrunk towards that of the minimum variance portfolio, Jorion,
1986), "james_stein" (the averages shrunk towards their grand mean, James and Stein, 1961),
"bodnar_okhrin_parolya" (the averages and their grand mean combined with optimal weights, Bodnar,
Okhrin and Parolya, 2019), "centroid" (the returns an ordering of the assets implies, Almgren and
Chriss, 2006). Defaults to None, all of them (CAPM only when there is a benchmark, Centroid only
with a ranking).
- <u>period (str, optional):</u> The frequency of the returns. Options are: "daily" (daily returns), "weekly"
(weekly returns), "monthly" (monthly returns), "quarterly" (quarterly returns), "yearly" (yearly
returns). Defaults to "daily".
- <u>span (int, optional):</u> The span in periods of the exponential averages.
Defaults to 180.
- <u>adjust (bool, optional):</u> Whether the exponential averages normalize the weights over the whole history
rather than follow the recursion $$m_{t} = \alpha r_{t} + (1 - \alpha) m_{t - 1}$$. Defaults to True.
- <u>ranking (list &#124; dict &#124; pd.Series &#124; None, optional):</u> The ordering of the centroid estimator, from the
highest expected return to the lowest: a list of every asset (["MSFT", "AAPL", ...]), whose entries
can be lists of assets ranked together (["MSFT", ["AAPL", "JNJ"], "XOM"]), or a score per asset
({"AAPL": 2.1, ...} or a pd.Series, higher is better, equal scores ranked together). Defaults to
None.
- <u>include_benchmark (bool, optional):</u> Whether to include the benchmark as an
asset. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The annualized expected return per asset (rows) and estimator
(columns), from the periods in which every asset has a return.

**Notes:**

- The geometric and exponential geometric averages are compounded annual returns; the
others are arithmetic returns per period times P, without compounding.
- James-Stein needs at least three assets to shrink (with two, its $$\beta$$ is negative
and clipped to 0); skfolio and Riskfolio-Lib leave $$\beta$$ unclipped. Bayes-Stein
uses Jorion's Σ, where skfolio's and Riskfolio-Lib's Bayes-Stein estimators use S.
- The centroid values follow, within 0.01, the mean of sorted normal draws that
PortfolioAnalytics' centroid.complete.mc simulates. PortfolioAnalytics takes the order
from the lowest return up and rescales the centroid to lie between -0.05 and 0.05,
where here it is scaled by each asset's volatility, so every asset's return over its
volatility is its centroid value.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "JNJ", "XOM"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.portfolio.get_expected_returns_estimate(
    show_columns=["Mean", "Geometric", "Bayes-Stein", "James-Stein", "Bodnar-Okhrin-Parolya"]
)
```

Which returns:

|      |   Mean |   Geometric |   Bayes-Stein |   James-Stein |   Bodnar-Okhrin-Parolya |
|:-----|-------:|------------:|--------------:|--------------:|------------------------:|
| AAPL | 0.1932 |      0.1672 |        0.1673 |        0.1932 |                  0.1291 |
| MSFT | 0.2017 |      0.1838 |        0.1695 |        0.2017 |                  0.1222 |
| JNJ  | 0.0987 |      0.0884 |        0.1418 |        0.0987 |                  0.2051 |
| XOM  | 0.2911 |      0.2898 |        0.1937 |        0.2911 |                  0.0503 |

---

## get_covariance_estimate
Estimate the annualized covariance matrix of the assets, with one of the estimators the optimizers take.

Its parameters can be set, and it can be shown as a correlation matrix.

- Sample: the sample covariance (ddof=1).
- Ledoit-Wolf, Ledoit-Wolf constant correlation, Ledoit-Wolf single factor and Oracle Approximating Shrinkage: shrinkage with an estimated intensity (Ledoit and Wolf, 2003, 2004; Chen et al., 2010).
- Fixed shrinkage: $$\Sigma = (1 - \delta) S + \delta$$ (tr(S) / N) I with a fixed intensity $$\delta$$, the shrinkage.
- Semicovariance: the co-movement below a zero return (Estrada, 2008).
- Exponential: exponentially weighted with $$\alpha = 2$$ / (span + 1) (RiskMetrics).
- Denoised: the eigenvalues of the correlation matrix below the Marčenko-Pastur upper edge averaged (constant residual eigenvalue), set to zero (spectral), or their part of the correlation shrunk towards its diagonal (targeted shrinkage), C_signal + $$\alpha$$ C_noise + ($$1 - \alpha$$) diag(C_noise) with $$\alpha$$ the denoise alpha (López de Prado, 2020).
- Gerber: $$\Sigma = D G D$$ with G the Gerber statistic of the moves beyond the Gerber threshold in standard deviations: statistic $$0 (n_{c} - n_{d}) / (n_{c} + n_{d})$$, $$1 (n_{c} - n_{d}) / (T - n_{n})$$ or 2 H / √(diag(H) diag(H)') (Gerber et al., 2022).
- Detoned: the first principal components of the correlation matrix, the market, removed and the rest rescaled to a unit diagonal (López de Prado, 2020). It is singular, so the optimizers do not take it; it suits clustering as the detoned codependence.
- Factor: $$\Sigma = B \sum_{f} B' + D$$, the covariance a time series factor model implies, with B the loadings of the assets on the factors (the Fama and French five factors by default), $$\sum_{f}$$ the covariance of the factors and D the variances of the residuals, all with ddof=1 (Fama and French, 1993; Connor, 1995). The loadings come from OLS on every factor, a stepwise selection or a principal components regression (see get_factor_loadings), on the periods both the assets and the factors have.
- Minimum Covariance Determinant: the covariance of the h = ⌈(T + N + 1) / 2⌉ periods whose covariance matrix has the smallest determinant, found with the C-steps of FAST-MCD from random subsets (with the seed), made consistent at the normal distribution and reweighted: the periods with a Mahalanobis distance below the 97.5% quantile of $$\chi_{N}^{2}$$ are kept and their covariance is multiplied by $$c = 0.975 / F_{N + 2} (\chi_{N}^{2} (0.975))$$ (Rousseeuw and Van Driessen, 1999; Croux and Haesbroeck, 1999). Crashes and data errors barely move it.
- j-LoGo: $$\Sigma = J^{- 1}$$ with $$J = \Sigma_{C} [S_{\text{CC}}]^{- 1} - \Sigma_{S} [S_{\text{SS}}]^{- 1}$$ the sparse inverse covariance over the 4-cliques C and separators S of the Triangulated Maximally Filtered Graph of the similarities $$(1 + \rho) / 2$$, a planar graph with 3(N - 2) links (Massara et al., 2017; Barfuss et al., 2016). With four or fewer assets every pair is linked and it is the sample covariance.
- Geodesic: $$\Sigma = S^{\tfrac{1}{2}} (S^{- \tfrac{1}{2}} T S^{- \tfrac{1}{2}})^{\delta} S^{\tfrac{1}{2}}$$ with T = (tr(S) / N) I and $$\delta$$ the shrinkage, which keeps the eigenvectors of S and interpolates its eigenvalues geometrically, $$\lambda^{1 - \delta}$$ (tr(S) / N)^δ (Bhatia, 2007; Musolas et al., 2021).
- Regime adjusted exponentially weighted: $$\phi^{2} S_{T}$$ with $$S_{t} = \lambda S_{t - 1} + (1 - \lambda) r_{t} r_{t}'$$ (around zero, bias-corrected, $$\lambda$$ = 2^(-1 / half_life)) and $$\phi$$ the exponential average (half-life half_life / 2) of $$\vert w' r_{t} \vert / \sqrt{w' S_{t - 1} w} / \sqrt{2 / \pi}$$ for the inverse volatility portfolio w, clipped to [0.7, 1.6] (Paleologo, 2025).
- Denoised and detoned: the denoised correlation with its first principal components removed and rescaled to a unit diagonal, the order of López de Prado (2020, section 2.6). Singular, like the detoned estimate.
- NERCOME: $$\Sigma = (1 / M) \sum_{s} P_{1}$$ diag(P_1' $$S_{2} P_{1}$$) P_1' over $$M = 50$$ random splits of the periods into a first part of m and the rest, with $$P_{1}$$ the eigenvectors of the first part's sample covariance and $$S_{2}$$ the second part's: eigenvalues that are not fitted to the same noise as the eigenvectors (Abadir, Distaso and Žikeš, 2014; Lam, 2016). m is chosen from $$2 \sqrt{T}$$, 0.2T, ..., 0.8T, $$T - 2.5 \sqrt{T}$$ and $$T - 1.5 \sqrt{T}$$ by the smallest $$\text{‖} \text{avg} (\sum_{m} - S_{2}) \text{‖}^{2}$$ (Lam, 2016), and the splits drawn with the seed.
- CCC-GARCH: the next-period covariance of the constant conditional correlation model of Bollerslev (1990), $$\Sigma_{T} + 1 = D R D$$ with D the GARCH(1, 1) volatilities forecast for the next period, $$\sigma_{i,T}^{2} + 1 = \omega_{i} + \alpha_{i} \epsilon_{i,T}^{2} + \beta_{i} \sigma_{i,T}^{2}$$, and R the correlation of the standardized residuals $$\epsilon_{t} / \sigma_{t}$$ of the returns around their average. It follows the volatility now, not its average over the history.
- MM-estimator: robust to almost half the periods being outliers and 95% as efficient in its shape (the correlations and variance ratios) as the sample covariance for normal returns: an S-estimator with Tukey's bisquare $$\rho (d) = 1 - (1 - (d / c)^{2})^{3}$$ (the scatter with the smallest scale s solving avg $$\rho (d_{t} / \sqrt{s}) = (1 - N / T) / 2$$), followed by a bisquare M-step with a larger c at that scale (Tatsuoka and Tyler, 2000; Salibián-Barrera, Van Aelst and Willems, 2006). Both are iteratively reweighted means and covariances, with weights that fall to zero for periods far from the bulk.
- Rocke's S-estimator: the translated biweight of Rocke (1996) on the squared distances, $$\rho (x) = ((x - 1) / (4 \gamma)) (3 - ((x - 1) / \gamma)^{2})$$ + ½ within $$\gamma$$ of 1 (0 below, 1 above), with $$\gamma = \min (\chi_{N}^{2} (0.995) / N - 1 , 1)$$, made consistent at the normal distribution through the median distance, which keeps its robustness for many assets (Maronna, Martin, Yohai and Salibián-Barrera, 2019).

**Also known as:** covariance estimator, risk model, shrunk covariance, Gerber covariance, denoised covariance, detoned correlation, factor covariance, factor risk model, robust covariance, MCD, FastMCD, TMFG, LoGo, sparse inverse covariance, geodesic shrinkage, regime adjusted EWMA covariance, short-term volatility update, NERCOME, split-sample covariance, CCC-GARCH, constant conditional correlation, MM-estimator, S-estimator, Rocke estimator, translated biweight.

**References:**

- paper | Ledoit, O. and Wolf, M. (2004). "A Well-Conditioned Estimator for Large-Dimensional Covariance Matrices." Journal of Multivariate Analysis, 88(2), 365-411.
- paper | Gerber, S., Markowitz, H. M., Ernst, P. A., Miao, Y., Javid, B. and Sargen, P. (2022). "The Gerber Statistic: A Robust Co-Movement Measure for Portfolio Optimization." The Journal of Portfolio Management, 48(3), 87-102.
- paper | López de Prado, M. (2020). "Machine Learning for Asset Managers." Cambridge University Press, chapter 2.
- paper | Fama, E. F. and French, K. R. (1993). "Common Risk Factors in the Returns on Stocks and Bonds." Journal of Financial Economics, 33(1), 3-56.
- paper | Connor, G. (1995). "The Three Types of Factor Models: A Comparison of Their Explanatory Power." Financial Analysts Journal, 51(3), 42-46.
- paper | Rousseeuw, P. J. and Van Driessen, K. (1999). "A Fast Algorithm for the Minimum Covariance Determinant Estimator." Technometrics, 41(3), 212-223.
- paper | Croux, C. and Haesbroeck, G. (1999). "Influence Function and Efficiency of the Minimum Covariance Determinant Scatter Matrix Estimator." Journal of Multivariate Analysis, 71(2), 161-190.
- paper | Massara, G. P., Di Matteo, T. and Aste, T. (2017). "Network Filtering for Big Data: Triangulated Maximally Filtered Graph." Journal of Complex Networks, 5(2), 161-178.
- paper | Barfuss, W., Massara, G. P., Di Matteo, T. and Aste, T. (2016). "Parsimonious Modeling with Information Filtering Networks." Physical Review E, 94(6), 062306.
- paper | Bhatia, R. (2007). "Positive Definite Matrices." Princeton University Press.
- paper | Musolas, A., Smith, S. T. and Marzouk, Y. (2021). "Geodesically Parameterized Covariance Estimation." SIAM Journal on Matrix Analysis and Applications, 42(2), 528-556.
- paper | Paleologo, G. A. (2025). "The Elements of Quantitative Investing." Wiley Finance.
- paper | Abadir, K. M., Distaso, W. and Žikeš, F. (2014). "Design-Free Estimation of Variance Matrices." Journal of Econometrics, 181(2), 165-180.
- paper | Lam, C. (2016). "Nonparametric Eigenvalue-Regularized Precision or Covariance Matrix Estimator." The Annals of Statistics, 44(3), 928-953.
- paper | Bollerslev, T. (1990). "Modelling the Coherence in Short-Run Nominal Exchange Rates: A Multivariate Generalized ARCH Model." The Review of Economics and Statistics, 72(3), 498-505.
- paper | Rocke, D. M. (1996). "Robustness Properties of S-Estimators of Multivariate Location and Shape in High Dimension." The Annals of Statistics, 24(3), 1327-1345.
- paper | Tatsuoka, K. S. and Tyler, D. E. (2000). "On the Uniqueness of S-Functionals and M-Functionals under Nonelliptical Distributions." The Annals of Statistics, 28(4), 1219-1243.
- paper | Salibián-Barrera, M., Van Aelst, S. and Willems, G. (2006). "Principal Components Analysis Based on Multivariate MM Estimators with Fast and Robust Bootstrap." Journal of the American Statistical Association, 101(475), 1198-1211.
- paper | Maronna, R. A., Martin, R. D., Yohai, V. J. and Salibián-Barrera, M. (2019). "Robust Statistics: Theory and Methods (with R)." 2nd edition, Wiley.
- library | Referenced against scikit-learn's [LedoitWolf](https://scikit-learn.org/stable/modules/generated/sklearn.covariance.LedoitWolf.html){:target="_blank"}
- library | Referenced against scikit-learn's [OAS](https://scikit-learn.org/stable/modules/generated/sklearn.covariance.OAS.html){:target="_blank"}
- library | Referenced against PyPortfolioOpt's [CovarianceShrinkage.shrunk_covariance](https://pyportfolioopt.readthedocs.io/en/latest/RiskModels.html#pypfopt.risk_models.CovarianceShrinkage.shrunk_covariance){:target="_blank"}
- library | Referenced against PyPortfolioOpt's [semicovariance](https://pyportfolioopt.readthedocs.io/en/latest/RiskModels.html#pypfopt.risk_models.semicovariance){:target="_blank"}
- library | Referenced against PyPortfolioOpt's [exp_cov](https://pyportfolioopt.readthedocs.io/en/latest/RiskModels.html#pypfopt.risk_models.exp_cov){:target="_blank"}
- library | Referenced against skfolio's [DenoiseCovariance](https://skfolio.org/generated/skfolio.moments.DenoiseCovariance.html){:target="_blank"} (constant residual eigenvalue)
- library | Referenced against Riskfolio-Lib's [denoiseCov](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/auxiliary.html#AuxFunctions.denoiseCov){:target="_blank"} (spectral and targeted shrinkage)
- library | Referenced against skfolio's [GerberCovariance](https://skfolio.org/generated/skfolio.moments.GerberCovariance.html){:target="_blank"} (statistics 1 and 2)
- library | Referenced against Riskfolio-Lib's [gerber_cov_stat0](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/auxiliary.html#GerberStatistic.gerber_cov_stat0){:target="_blank"} (statistic 0)
- library | Referenced against skfolio's [DetoneCovariance](https://skfolio.org/generated/skfolio.moments.DetoneCovariance.html){:target="_blank"} (sample covariance)
- library | Referenced against Riskfolio-Lib's [risk_factors](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/parameters.html#ParamsEstimation.risk_factors){:target="_blank"} (factor)
- library | Referenced against Riskfolio-Lib's [loadings_matrix](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/parameters.html#ParamsEstimation.loadings_matrix){:target="_blank"} (backward selection, every factor kept)
- library | Referenced against scikit-learn's [MinCovDet](https://scikit-learn.org/stable/modules/generated/sklearn.covariance.MinCovDet.html){:target="_blank"}
- library | Referenced against Riskfolio-Lib's [covar_matrix](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/parameters.html#ParamsEstimation.covar_matrix){:target="_blank"} (j-LoGo)
- library | Referenced against skfolio's [GeodesicShrinkageCovariance](https://skfolio.org/generated/skfolio.moments.GeodesicShrinkageCovariance.html){:target="_blank"}
- library | Referenced against skfolio's [RegimeAdjustedEWCovariance](https://skfolio.org/generated/skfolio.moments.RegimeAdjustedEWCovariance.html){:target="_blank"} (its defaults)
- library | Shares similar logic as PyPortfolioOpt's [CovarianceShrinkage.ledoit_wolf](https://pyportfolioopt.readthedocs.io/en/latest/RiskModels.html#pypfopt.risk_models.CovarianceShrinkage.ledoit_wolf){:target="_blank"}
- library | Shares similar logic as PyPortfolioOpt's [CovarianceShrinkage.oracle_approximating](https://pyportfolioopt.readthedocs.io/en/latest/RiskModels.html#pypfopt.risk_models.CovarianceShrinkage.oracle_approximating){:target="_blank"}
- library | Shares similar logic as scikit-learn's [ShrunkCovariance](https://scikit-learn.org/stable/modules/generated/sklearn.covariance.ShrunkCovariance.html){:target="_blank"}
- library | Shares similar logic as skfolio's [ShrunkCovariance](https://skfolio.org/generated/skfolio.moments.ShrunkCovariance.html){:target="_blank"}
- library | Shares similar logic as Riskfolio-Lib's [covar_matrix](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/parameters.html#ParamsEstimation.covar_matrix){:target="_blank"} (fixed shrinkage)
- library | Shares similar logic as RiskLabAI's [denoise_cov](https://github.com/RiskLabAI/RiskLabAI.py/blob/v3.2.0/src/RiskLabAI/data/denoise/denoising.py#L376){:target="_blank"}
- library | Shares similar logic as Riskfolio-Lib's [gerber_cov_stat1](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/auxiliary.html#GerberStatistic.gerber_cov_stat1){:target="_blank"} (statistic 1)
- library | Shares similar logic as Riskfolio-Lib's [gerber_cov_stat2](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/auxiliary.html#GerberStatistic.gerber_cov_stat2){:target="_blank"} (statistic 2)
- library | Shares similar logic as skfolio's [FactorModel](https://skfolio.org/generated/skfolio.prior.FactorModel.html){:target="_blank"} (factor)
- library | Shares similar logic as RiskLabAI's [nercome_denoised_covariance](https://github.com/RiskLabAI/RiskLabAI.py/blob/v3.2.0/src/RiskLabAI/data/denoise/nercome.py#L54){:target="_blank"}
- library | Shares similar logic as PortfolioAnalytics (R)'s [CCCgarch.MM](https://github.com/cran/PortfolioAnalytics/blob/2.1.2/R/moment.functions.R#L22){:target="_blank"}
- library | Shares similar logic as PortfolioAnalytics (R)'s [custom.covRob.MM](https://github.com/cran/PortfolioAnalytics/blob/2.1.2/R/custom.covRob.R#L29){:target="_blank"}
- library | Shares similar logic as PortfolioAnalytics (R)'s [custom.covRob.Rocke](https://github.com/cran/PortfolioAnalytics/blob/2.1.2/R/custom.covRob.R#L57){:target="_blank"}

**Args:**

- <u>method (str, optional):</u> The estimator. Options are: "sample" (the sample covariance, ddof=1),
"ledoit_wolf" (shrunk towards the scaled identity, Ledoit and Wolf, 2004),
"ledoit_wolf_constant_correlation" (shrunk towards the average correlation, Ledoit and Wolf, 2004),
"ledoit_wolf_single_factor" (shrunk towards the covariance that the benchmark as a single factor
implies, Ledoit and Wolf, 2003), "oas" (Oracle Approximating Shrinkage, Chen et al., 2010), "shrunk"
(a fixed 10% towards the scaled identity), "semicovariance" (the co-movement below a zero return,
Estrada, 2008), "exponential" (exponentially weighted, recent periods weigh most, RiskMetrics),
"denoised" (the eigenvalues of the correlation matrix that random returns could produce averaged,
Laloux et al., 2000), "denoised_spectral" (those eigenvalues set to zero), "denoised_shrink" (the
noise correlations shrunk towards their diagonal, López de Prado, 2020), "gerber" (co-movements
beyond half a standard deviation, Gerber et al., 2022), "detoned" (the correlation without its first
principal components, López de Prado, 2020), "factor" (the covariance a time series factor model
implies, Connor, 1995), "minimum_covariance_determinant" (the reweighted covariance of the half of
the periods with the smallest covariance determinant, robust to outliers, Rousseeuw and Van
Driessen, 1999), "jlogo" (the sparse inverse covariance on the TMFG planar graph of the
correlations, Barfuss et al., 2016), "geodesic" (10% towards the scaled identity along the geodesic
of the positive definite matrices, Bhatia, 2007), "regime_adjusted_ew" (exponentially weighted with
a half-life of 40 periods, rescaled by the recent realized against predicted risk, Paleologo, 2025),
"denoised_detoned" (the denoised correlation with its first principal components removed, López de
Prado, 2020), "nercome" (eigenvectors from one part of the periods and the variances along them from
the other, averaged over random splits, Lam, 2016), "ccc_garch" (the next-period covariance of
GARCH(1, 1) volatilities with constant correlations, Bollerslev, 1990), "mm" (the robust
MM-estimator, Maronna et al., 2019), "rocke" (Rocke's robust S-estimator, Maronna et al., 2019).
Defaults to "sample".
- <u>period (str, optional):</u> The frequency of the returns. Options are: "daily" (daily returns), "weekly"
(weekly returns), "monthly" (monthly returns), "quarterly" (quarterly returns), "yearly" (yearly
returns). Defaults to "daily".
- <u>span (int, optional):</u> The span in periods of the exponentially weighted estimate. Defaults to 180.
- <u>shrinkage (float, optional):</u> The fixed intensity $$\delta$$ of the fixed and geodesic shrinkage, between 0 and 1.
Defaults to 0.1 (PyPortfolioOpt defaults to 0.2 for the fixed shrinkage).
- <u>gerber_threshold (float, optional):</u> The threshold of the Gerber estimate in standard deviations, between
0 and 1. Defaults to 0.5.
- <u>gerber_statistic (int, optional):</u> The Gerber statistic. Options are: 0 (the original statistic), 1 (the
positive semidefinite variant), 2 (the matrix form). Defaults to 1.
- <u>denoise_alpha (float, optional):</u> The share $$\alpha$$ of the noise correlations the targeted shrinkage keeps,
between 0 and 1. Defaults to 0.
- <u>components (int, optional):</u> The number of principal components the detoned estimates remove. Defaults to
1.
- <u>factor_selection (str, optional):</u> How the factor estimate takes the loadings. Options are: "ols" (every
factor), "forward" (stepwise by the p-values, 0.05), "backward" (stepwise by the p-values, 0.05),
"pcr" (principal components regression keeping 95% of the variance). Defaults to "ols".
- <u>factors (pd.DataFrame &#124; None, optional):</u> The factor returns of the factor estimate, one column per
factor, at the frequency of the period. Defaults to None, the Fama and French five factors of the
region.
- <u>region (str, optional):</u> The region of the Fama and French factors. Options are: "United States",
"Developed", "Developed ex US", "Europe", "Japan", "Asia Pacific ex Japan", "North America".
Defaults to "United States".
- <u>half_life (float, optional):</u> The half-life in periods of the exponential weights of the regime adjusted
estimate. Defaults to 40, skfolio's default as well.
- <u>seed (int &#124; None, optional):</u> The seed of the random subsets of the Minimum Covariance Determinant, which
also starts the MM and Rocke estimators, and of the random splits of NERCOME (numpy's default
generator), so the same returns give the same estimate. Defaults to 0.
- <u>correlation (bool, optional):</u> Whether to return the correlation matrix of
the estimate instead. Defaults to False.
- <u>include_benchmark (bool, optional):</u> Whether to include the benchmark as an
asset. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The annualized covariance matrix (the covariance per period
times the number of periods in a year), or the correlation matrix, from the
periods in which every asset has a return.

**Notes:**

- The Gerber thresholds and D use standard deviations with ddof=1, where skfolio
and Riskfolio-Lib use ddof=0; their result equals this one with the threshold
multiplied by $$\sqrt{T / (T - 1)}$$ and the covariance by T / (T - 1).
- The fixed shrinkage shrinks the sample covariance with ddof=1 (as PyPortfolioOpt);
skfolio, scikit-learn and Riskfolio-Lib shrink the one divided by T.
- The Minimum Covariance Determinant divides by the number of periods kept (ddof=0),
as in scikit-learn, since the consistency factors assume it. Its random subsets
differ from scikit-learn's, so the two can end in different local minima of the
determinant, a few percent apart on small samples. PyPortfolioOpt's
min_cov_determinant returns the raw estimate (scikit-learn's fast_mcd), without
the consistency factor and the reweighting.
- The regime adjusted estimate takes the returns around zero, as skfolio does by
default, and uses the whole history, where the exponential estimate takes a span of
180 periods.
- NERCOME estimates the covariance itself, as Lam (2016) does; RiskLabAI's
nercome_denoised_covariance splits at 2T / 3 and estimates the correlation of the
standardized returns, so its variances are the sample ones.
- CCC-GARCH fits every GARCH(1, 1) by Gaussian likelihood from the arch package's
backcast (see get_garch); PortfolioAnalytics' CCCgarch.MM uses fGarch and a
constant volatility for an asset whose $$\alpha$$ is below 0.01. A GARCH fit takes a few
seconds per asset on daily returns.
- The MM and Rocke estimators start from the minimum covariance determinant (with the
seed) and from the sample covariance and keep the smaller S scale; RobStatTM's
covRobMM and covRobRocke, which PortfolioAnalytics calls, start from the
kurtosis-based estimate of Peña and Prieto (2007), so on small samples the two can end
in different local minima. Rocke's estimator suits ten or more assets; with fewer, $$\gamma$$ =
1 and its weights are low for many ordinary periods, so the MM-estimator is the more
efficient there (Maronna et al., 2019).

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "JNJ", "XOM"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.portfolio.get_covariance_estimate(method="gerber")
```

Which returns:

|      |   AAPL |   MSFT |    JNJ |    XOM |
|:-----|-------:|-------:|-------:|-------:|
| AAPL | 0.0776 | 0.0288 | 0.0044 | 0.0054 |
| MSFT | 0.0288 | 0.0661 | 0.0021 | 0.0015 |
| JNJ  | 0.0044 | 0.0021 | 0.028  | 0.0041 |
| XOM  | 0.0054 | 0.0015 | 0.0041 | 0.073  |

---

## get_random_matrix_statistics
Fit the Marčenko-Pastur distribution to the eigenvalues of the correlation matrix of the assets, to see how much of it random returns alone could produce.

The eigenvalues of the correlation matrix of T periods of N unrelated returns with variance $$\sigma^{2}$$ fall between the edges $$\lambda -$$ and $$\lambda +$$ of the Marčenko-Pastur distribution; an eigenvalue above $$\lambda +$$ is signal (the market, sectors, styles), the ones below it are indistinguishable from noise and are what the denoised covariance estimators average, remove or shrink (López de Prado, 2020, chapter 2).

The formula is as follows:

$$
f(\lambda) = \frac{q}{(2 \pi \sigma^{2} \lambda) \sqrt{(\lambda + - \lambda) (\lambda - \lambda -)}} \;\text{for}\; \lambda - \leq \lambda \leq \lambda +,\;\; \text{with}\;\; q = \frac{T}{N}
$$

$$
\lambda \pm = \sigma^{2}\left(1 \pm \sqrt{\frac{1}{q}}\right)^{2}
$$

$$
\sigma^{2} \;\text{minimizes}\; \Sigma_{x} (f(x) - k(x))^{2} \;\text{over}\; \text{1,000} \;\text{points}\; x \;\text{between}\; \lambda - \text{and}\; \lambda +,\;\; \text{with } k \text{ a Gaussian kernel density of the eigenvalues (bandwidth 0.01)},\;\; \text{from}\; \sigma^{2} = 0.5 \;\text{and between}\; 0.00001 \;\text{and}\; 0.99999 (\text{López} \,\mathrm{d}e \;\text{Prado},\; 2020,\; \text{section}\; 2.4)
$$

- signal eigenvalues: $$\lambda_{k} > \lambda +$$

**Also known as:** Marchenko-Pastur, Marcenko-Pastur fit, random matrix theory, RMT, eigenvalue spectrum, noise eigenvalues, signal eigenvalues.

**References:**

- paper | Marčenko, V. A. and Pastur, L. A. (1967). "Distribution of Eigenvalues for Some Sets of Random Matrices." Mathematics of the USSR-Sbornik, 1(4), 457-483.
- paper | Laloux, L., Cizeau, P., Potters, M. and Bouchaud, J.-P. (2000). "Random Matrix Theory and Financial Correlations." International Journal of Theoretical and Applied Finance, 3(3), 391-397.
- paper | López de Prado, M. (2020). "Machine Learning for Asset Managers." Cambridge University Press, chapter 2.
- library | Shares similar logic as RiskLabAI's [find_max_eval](https://github.com/RiskLabAI/RiskLabAI.py/blob/v3.2.0/src/RiskLabAI/data/denoise/denoising.py#L138){:target="_blank"}
- library | Shares similar logic as RiskLabAI's [marcenko_pastur_pdf](https://github.com/RiskLabAI/RiskLabAI.py/blob/v3.2.0/src/RiskLabAI/data/denoise/denoising.py#L26){:target="_blank"}

**Args:**

- <u>output (str, optional):</u> Options are: "summary" (one row: the Periods, Assets, Noise Variance $$\sigma^{2}$$, Lower
Edge $$\lambda -$$, Upper Edge $$\lambda +$$, Largest Eigenvalue, the number of Signal Eigenvalues and their Signal Share
of the trace N), "eigenvalues" (every eigenvalue from the largest, its Explained Variance $$\lambda / N$$ and
whether it is Signal). Defaults to "summary".
- <u>period (str, optional):</u> The frequency of the returns. Options are: "daily" (daily returns), "weekly"
(weekly returns), "monthly" (monthly returns), "quarterly" (quarterly returns), "yearly" (yearly
returns). Defaults to "daily".
- <u>include_benchmark (bool, optional):</u> Whether to include the benchmark as an
asset. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The summary of the fit or the table of eigenvalues, from the
periods in which every asset has a return.

**Notes:**

- The fit is the one the denoised covariance estimators use. RiskLabAI's find_max_eval
fits the same density with scikit-learn's KernelDensity at as many points as there are
eigenvalues rather than the book's 1,000, which moves $$\sigma^{2}$$ by a few percent for 30
assets. With few assets the eigenvalues are too few to pin the density down, so $$\sigma^{2}$$ is
a rough guide there; the distribution describes many assets.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "JNJ", "XOM", "JPM", "PG", "KO", "NVDA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.portfolio.get_random_matrix_statistics(output="eigenvalues")
```

Which returns:

|              |   Eigenvalue |   Explained Variance | Signal   |
|:-------------|-------------:|---------------------:|:---------|
| Eigenvalue 1 |       2.8514 |               0.3564 | True     |
| Eigenvalue 2 |       1.7917 |               0.224  | True     |
| Eigenvalue 3 |       1.0929 |               0.1366 | False    |
| Eigenvalue 4 |       0.6159 |               0.077  | False    |
| Eigenvalue 5 |       0.5604 |               0.0701 | False    |
| Eigenvalue 6 |       0.4081 |               0.051  | False    |
| Eigenvalue 7 |       0.3617 |               0.0452 | False    |
| Eigenvalue 8 |       0.3178 |               0.0397 | False    |

---

## get_codependence_matrix
Calculate how much every pair of assets moves together.

It is the codependence that the hierarchical optimizers (HRP, HERC, NCO) and get_asset_clusters take as their codependence, or the distance they cluster on.

- Pearson: the correlation of the covariance estimate, distance $$\sqrt{(1 - \rho) / 2}$$.
- Spearman and Kendall: the rank correlations of the returns, distance $$\sqrt{(1 - \rho) / 2}$$.
- Gerber: the Gerber statistic (see get_covariance_estimate), distance $$\sqrt{(1 - \rho) / 2}$$.
- Detoned: the correlation without its first principal components, distance $$\sqrt{(1 - \rho) / 2}$$.
- Distance correlation: dCor = √(dCov²(x, y) / √(dCov²(x, x) dCov²(y, y))) from the doubly centred distances $$\vert x_{s} - x_{t} \vert$$ (Székely, Rizzo and Bakirov, 2007), zero only for independent returns; distance √(1 - dCor).
- Mutual information: I(X, Y) / min(H(X), H(Y)) from histograms with the given bins (natural logarithms); distance the variation of information (H(X) + H(Y) - 2 I(X, Y)) / H(X, Y) (Meilă, 2007).
- Lower tail dependence: $$P (r_{j} \leq q_{j} (\alpha) \vert r_{i} \leq q_{i} (\alpha))$$; distance -ln $$\lambda$$ (λ at least 1e-8).
- Absolute angular: $$\vert \rho \vert$$ of the Pearson correlation, distance $$\sqrt{1 - \vert \rho \vert}$$ (López de Prado, 2020, chapter 3), and squared angular: $$\rho^{2}$$, distance $$\sqrt{1 - \rho^{2}}$$, the same construction on the squared correlation, which put assets that move strongly against each other close together, as hedges of one another.
- GNPR: the Generic Non-Parametric Representation distance of Marti et al. (2016), $$d^{2} = \theta d_{1}^{2} + (1 - \theta) d_{0}^{2}$$ with $$\theta$$ the GNPR theta, $$d_{1}^{2} = 3 / (T (T^{2} - 1)) \sum_{t} (R_{i,t} - R_{j,t})^{2}$$ of the ranks R of the returns ($$(1 - \rho_{S}) / 2$$ without ties) and $$d_{0}^{2}$$ = ½ $$\sum_{b} (\sqrt{g_{i,b}} - \sqrt{g_{j,b}})^{2}$$ the squared Hellinger distance between the histograms g of the returns, with bins the GNPR bandwidth wide; codependence $$1 - d^{2}$$. $$\theta = 1$$ compares only how the assets move together, $$\theta = 0$$ only how their returns are distributed.

**Also known as:** codependence, distance correlation, mutual information, variation of information, tail dependence matrix, correlation distance, angular distance, absolute angular distance, squared angular distance, GNPR, copula distance.

**References:**

- paper | Mantegna, R. N. (1999). "Hierarchical Structure in Financial Markets." The European Physical Journal B, 11(1), 193-197.
- paper | Székely, G. J., Rizzo, M. L. and Bakirov, N. K. (2007). "Measuring and Testing Dependence by Correlation of Distances." The Annals of Statistics, 35(6), 2769-2794.
- paper | Meilă, M. (2007). "Comparing Clusterings - An Information Based Distance." Journal of Multivariate Analysis, 98(5), 873-895.
- paper | Marti, G., Andler, S., Nielsen, F. and Donnat, P. (2016). "Clustering Financial Time Series: How Long Is Enough?" Proceedings of the Twenty-Fifth International Joint Conference on Artificial Intelligence (IJCAI-16), 2583-2589.
- paper | Hacine-Gharbi, A. and Ravier, P. (2018). "A Binning Formula of Bi-histogram for Joint Entropy Estimation Using Mean Square Error Minimization." Pattern Recognition Letters, 101, 21-28.
- paper | López de Prado, M. (2020). "Machine Learning for Asset Managers." Cambridge University Press, chapter 3.
- library | Referenced against skfolio's [DistanceCorrelation](https://skfolio.org/generated/skfolio.distance.DistanceCorrelation.html){:target="_blank"}
- library | Referenced against skfolio's [MutualInformation](https://skfolio.org/generated/skfolio.distance.MutualInformation.html){:target="_blank"}
- library | Referenced against Riskfolio-Lib's [mutual_info_matrix](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/auxiliary.html#AuxFunctions.mutual_info_matrix){:target="_blank"} (Hacine-Gharbi bins)
- library | Referenced against Riskfolio-Lib's [ltdi_matrix](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/auxiliary.html#AuxFunctions.ltdi_matrix){:target="_blank"}
- library | Shares similar logic as Riskfolio-Lib's [codep_dist](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/auxiliary.html#AuxFunctions.codep_dist){:target="_blank"}
- library | Shares similar logic as skfolio's [CovarianceDistance](https://skfolio.org/generated/skfolio.distance.CovarianceDistance.html){:target="_blank"} (Pearson correlation)
- library | Shares similar logic as skfolio's [DistanceCorrelation](https://skfolio.org/generated/skfolio.distance.DistanceCorrelation.html){:target="_blank"}
- library | Shares similar logic as skfolio's [MutualInformation](https://skfolio.org/generated/skfolio.distance.MutualInformation.html){:target="_blank"}
- library | Shares similar logic as Riskfolio-Lib's [dcorr_matrix](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/auxiliary.html#AuxFunctions.dcorr_matrix){:target="_blank"}
- library | Shares similar logic as Riskfolio-Lib's [var_info_matrix](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/auxiliary.html#AuxFunctions.var_info_matrix){:target="_blank"}

**Args:**

- <u>method (str, optional):</u> The codependence. Options are: "pearson" (Pearson correlation), "spearman"
(Spearman correlation), "kendall" (Kendall correlation), "gerber" (Gerber statistic), "detoned"
(detoned correlation), "distance" (distance correlation), "mutual_information" (mutual information),
"lower_tail" (lower tail dependence), "absolute_angular" (absolute angular codependence),
"squared_angular" (squared angular codependence), "gnpr" (GNPR codependence). Defaults to "pearson".
- <u>period (str, optional):</u> The frequency of the returns. Options are: "daily" (daily returns), "weekly"
(weekly returns), "monthly" (monthly returns), "quarterly" (quarterly returns), "yearly" (yearly
returns). Defaults to "daily".
- <u>covariance (str, optional):</u> The covariance estimator whose correlation the Pearson codependence is (see
get_covariance_estimate). Options are: "sample" (sample covariance), "ledoit_wolf" (Ledoit-Wolf),
"ledoit_wolf_constant_correlation" (Ledoit-Wolf constant correlation), "ledoit_wolf_single_factor"
(Ledoit-Wolf single factor), "oas" (Oracle Approximating Shrinkage), "shrunk" (fixed shrinkage),
"semicovariance" (semicovariance), "exponential" (exponentially weighted), "denoised" (denoised,
constant residual eigenvalue), "denoised_spectral" (denoised, spectral), "denoised_shrink"
(denoised, targeted shrinkage), "gerber" (Gerber), "factor" (factor model),
"minimum_covariance_determinant" (Minimum Covariance Determinant), "jlogo" (j-LoGo), "geodesic"
(geodesic shrinkage), "regime_adjusted_ew" (regime adjusted exponentially weighted), "nercome"
(NERCOME), "ccc_garch" (CCC-GARCH), "mm" (MM-estimator), "rocke" (Rocke's S-estimator). Defaults to
"sample".
- <u>distance (bool, optional):</u> Whether to return the distance matrix the
clustering works on instead. Defaults to False.
- <u>gerber_threshold (float, optional):</u> The threshold of the Gerber statistic in standard deviations.
Defaults to 0.5.
- <u>gerber_statistic (int, optional):</u> The Gerber statistic. Options are: 0 (the original statistic), 1 (the
positive semidefinite variant), 2 (the matrix form). Defaults to 1.
- <u>components (int, optional):</u> The number of principal components the detoned correlation removes. Defaults
to 1.
- <u>bins (str &#124; int, optional):</u> The number of histogram bins of the mutual information, or the rule per
pair. Options are: "freedman" (Freedman and Diaconis, skfolio's default), "hacine_gharbi"
(Hacine-Gharbi, López de Prado's choice), or an integer. Defaults to "freedman".
- <u>alpha (float, optional):</u> The share of the lowest returns that forms the tail of the lower tail
dependence. Defaults to 0.05.
- <u>gnpr_theta (float, optional):</u> The weight $$\theta$$ of the co-movement in the GNPR distance, between 0 and 1.
Defaults to 0.5.
- <u>gnpr_bandwidth (float, optional):</u> The width of the histogram bins of the GNPR distance, in returns per
period. Defaults to 0.01.
- <u>include_benchmark (bool, optional):</u> Whether to include the benchmark as an
asset. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The codependence (or distance) matrix of the assets, from the
periods in which every asset has a return.

**Notes:**

- The distance correlation builds a matrix of $$T \times T$$ distances per asset, so it
takes longer on many daily periods.
- Riskfolio-Lib's mutual information defaults to Knuth's bins, skfolio's to
Freedman-Diaconis; with the same bins, both equal this one.
- The absolute and squared angular distances take the whole of $$1 - \vert \rho \vert$$ and $$1 - \rho^{2}$$;
half of them, as the correlation distance takes of $$1 - \rho$$, gives a distance √2 times
smaller with the same clusters.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "JNJ", "XOM"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.portfolio.get_codependence_matrix(method="distance")
```

Which returns:

|      |   AAPL |   MSFT |    JNJ |    XOM |
|:-----|-------:|-------:|-------:|-------:|
| AAPL | 1      | 0.5974 | 0.1659 | 0.1473 |
| MSFT | 0.5974 | 1      | 0.1173 | 0.0876 |
| JNJ  | 0.1659 | 0.1173 | 1      | 0.1513 |
| XOM  | 0.1473 | 0.0876 | 0.1513 | 1      |

---

## get_asset_clusters
Group the assets into clusters of assets that move together, the clusters that HERC and NCO allocate across.

- Hierarchical clustering: a hierarchical clustering on the distance of the codependence (see get_codependence_matrix), cut into the given number of clusters or, without a number, at the sharpest bend of the within-cluster dispersion (the two-order difference of the gap statistic, Yue, Wang and Wei, 2008), as HERC and NCO do, or at the highest standardized silhouette (López de Prado, 2020).
- FTCA: the Fast Threshold Clustering Algorithm of Varadi (2013). Among the assets not yet clustered, take the one with the highest average codependence (H) and the lowest (L). If H and L are codependent above the threshold, they form a cluster with every remaining asset whose average codependence with H and L is above it; otherwise H forms a cluster with the remaining assets above the threshold with H, and then L with those above it with L. This repeats until every asset belongs to a cluster. It needs no number of clusters.
- ONC: the Optimal Number of Clusters algorithm of López de Prado and Lewis (2019). Every asset is the point given by its row of the distance matrix. For $$k = 2$$ to N - 1 clusters, k-means runs ten times (from k-means++ starts drawn with the seed), and the clustering with the highest quality $$E [S] / \sqrt{V} [S]$$ of the silhouette coefficients $$S_{i} = (b_{i} - a_{i}) / \max (a_{i} , b_{i})$$ is kept. The clusters of below-average quality are then clustered again on their own, and their new clusters kept when they raise the average quality above that of the clusters they replace (López de Prado, 2020, snippets 4.1 and 4.2). It finds the number of clusters itself, needs no tree and suits uneven groups of assets.

**Also known as:** asset clustering, FTCA, correlation clusters, ONC, optimal number of clusters, k-means clustering.

**References:**

- paper | Varadi, D. (2013). "The Fast Threshold Clustering Algorithm (FTCA)." CSS Analytics.
- paper | López de Prado, M. and Lewis, M. J. (2019). "Detection of False Investment Strategies Using Unsupervised Learning Methods." Quantitative Finance, 19(9), 1555-1565.
- paper | Yue, S., Wang, X. and Wei, M. (2008). "Application of Two-Order Difference to Gap Statistic." Transactions of Tianjin University, 14(3), 217-221.
- paper | López de Prado, M. (2020). "Machine Learning for Asset Managers." Cambridge University Press.
- library | Referenced against skfolio's [HierarchicalClustering](https://skfolio.org/generated/skfolio.cluster.HierarchicalClustering.html){:target="_blank"} (hierarchical)
- library | Referenced against ffn's [calc_ftca](https://github.com/pmorissette/ffn/blob/v1.4.1/ffn/core.py#L2297){:target="_blank"}
- library | Shares similar logic as RiskLabAI's [cluster_k_means_top](https://github.com/RiskLabAI/RiskLabAI.py/blob/v3.2.0/src/RiskLabAI/cluster/clustering.py#L194){:target="_blank"} (López de Prado, Machine Learning for Asset Managers, snippet 4.2)

**Args:**

- <u>method (str, optional):</u> Options are: "hierarchical" (hierarchical clustering), "ftca" (Fast Threshold
Clustering Algorithm), "onc" (Optimal Number of Clusters). Defaults to "hierarchical".
- <u>period (str, optional):</u> The frequency of the returns. Options are: "daily" (daily returns), "weekly"
(weekly returns), "monthly" (monthly returns), "quarterly" (quarterly returns), "yearly" (yearly
returns). Defaults to "daily".
- <u>codependence (str, optional):</u> The codependence the assets are clustered on (see
get_codependence_matrix). Defaults to. Options are: "pearson" (the linear correlation of the
covariance matrix), "spearman" (the rank correlation of the returns, Spearman, 1904), "kendall" (the
rank correlation $$\tau_{b}$$ of the returns, Kendall, 1938), "gerber" (co-movements beyond half a standard
deviation, Gerber et al., 2022), "detoned" (the correlation without the market component, López de
Prado, 2020), "distance" (the distance correlation, Székely et al., 2007, through √(1 - dCor)),
"mutual_information" (through the variation of information, Meilă, 2007), "lower_tail" (how often
two assets fall into their lowest 5% of returns together, through -ln $$\lambda$$), "absolute_angular" ($$\vert \rho \vert$$
through $$\sqrt{1 - \vert \rho \vert}$$, López de Prado, 2020), "squared_angular" ($$\rho^{2}$$ through $$\sqrt{1 - \rho^{2}}$$, López de Prado,
2020), "gnpr" (the rank co-movement and the difference between the return distributions, $$\theta = 0.5$$,
Marti et al., 2016). Defaults to "pearson".
- <u>covariance (str, optional):</u> The covariance estimator whose correlation the Pearson codependence is.
Options are: "sample" (sample covariance), "ledoit_wolf" (Ledoit-Wolf),
"ledoit_wolf_constant_correlation" (Ledoit-Wolf constant correlation), "ledoit_wolf_single_factor"
(Ledoit-Wolf single factor), "oas" (Oracle Approximating Shrinkage), "shrunk" (fixed shrinkage),
"semicovariance" (semicovariance), "exponential" (exponentially weighted), "denoised" (denoised,
constant residual eigenvalue), "denoised_spectral" (denoised, spectral), "denoised_shrink"
(denoised, targeted shrinkage), "gerber" (Gerber), "factor" (factor model),
"minimum_covariance_determinant" (Minimum Covariance Determinant), "jlogo" (j-LoGo), "geodesic"
(geodesic shrinkage), "regime_adjusted_ew" (regime adjusted exponentially weighted), "nercome"
(NERCOME), "ccc_garch" (CCC-GARCH), "mm" (MM-estimator), "rocke" (Rocke's S-estimator). Defaults to
"sample".
- <u>linkage_method (str, optional):</u> The linkage of the hierarchical clustering. Options are: "single"
(single linkage), "complete" (complete linkage), "average" (average linkage), "ward" (Ward's
method), "dbht" (the Directed Bubble Hierarchical Tree of Song, Di Matteo and Aste, 2012, which
finds the number of clusters itself in the TMFG planar graph of the codependence). Defaults to
"ward".
- <u>clusters (int &#124; None, optional):</u> The number of clusters of the hierarchical clustering, or the most
clusters ONC tries. Defaults to None, chosen by the two-order difference of the gap statistic (by
the DBHT itself for its linkage; up to N - 1 for ONC).
- <u>cluster_criterion (str, optional):</u> How the hierarchical clustering chooses the number of clusters when
it is not given. Options are: "two_difference_gap" (the two-order difference of the gap statistic),
"standardized_silhouette" (the highest mean over standard deviation of the silhouette coefficients).
Defaults to "two_difference_gap".
- <u>threshold (float, optional):</u> The codependence above which FTCA puts assets in one cluster. Defaults to
0.5.
- <u>seed (int &#124; None, optional):</u> The seed of the k-means starts of ONC (numpy's default generator), so the
same returns give the same clusters. Defaults to 0.
- <u>include_benchmark (bool, optional):</u> Whether to include the benchmark as an
asset. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The Cluster of every asset, numbered from 1 (for FTCA in the
order the clusters are formed, for ONC in the order of their first asset).

**Notes:**

- ONC follows the comparisons of López de - <u>Prado (2020, snippet 4.2):</u> it clusters
again when at least two clusters are below the average quality and keeps the new
clusters when their quality is the higher one. A cluster whose silhouettes are
all equal (one asset alone) has no quality and is left as it is. Across seeds the
clusters of well-separated groups agree; where groups overlap, a k-means start can
settle elsewhere, which the seed fixes.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "JNJ", "XOM"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.portfolio.get_asset_clusters(method="ftca")
```

Which returns:

|      |   Cluster |
|:-----|----------:|
| AAPL |         1 |
| MSFT |         1 |
| JNJ  |         2 |
| XOM  |         3 |

---

## get_coskewness_matrix
Calculate the coskewness matrix M3 of the assets, the third co-moments of their returns: how the return of one asset moves with the joint variation of two others.

The skewness of a portfolio with weights w is w'M3(w ⊗ w) / σ_p³, so M3 is the input of mean-variance-skewness optimizations and the modified (Cornish-Fisher) VaR of a portfolio.

The formula is as follows:

$$
m_{ijk} = \Sigma_{t} w_{t} (r_{ti} - \mu_{i}) (r_{tj} - \mu_{j}) (r_{tk} - \mu_{k})
$$

$$
\text{Sample:}\;\; w_{t} = \frac{1}{T};\;\; \text{exponential:}\;\; w_{t} = \frac{\lambda^{T - t}}{\sum \lambda^{T - s}} \;\text{with}\; \lambda = 1 - \frac{2}{\text{span} + 1};\;\; \text{semi:}\;\; w_{t} = 1 / T \;\text{with} \;\min(r_{ti} - \mu_{i},\; 0) \;\text{in place of every deviation} \;(\text{only returns below the average count});\;\; \text{CCC-GARCH:}\;\; w_{t} = \frac{1}{T \;\text{on the standardized residuals of the CCC-GARCH}(1,\; 1) \;\text{model at the next-period volatilities}},\;\; z_{i,t} \sigma_{i,T} + \frac{1}{s(z_{i}) (\text{Bollerslev},\; 1990 ; \;\text{see}\; \text{get\_covariance\_estimate})},\;\; \text{the next-period coskewness of the model}
$$

$$
\text{standardized:}\;\; \frac{m_{ijk}}{\sigma_{i} \sigma_{j} \sigma_{k}} \;\text{with}\; \sigma^{2} = \Sigma_{t} w_{t} (r_{t} - \mu)^{2}
$$

**Also known as:** coskewness, third co-moment matrix, M3.

**References:**

- paper | Jondeau, E. and Rockinger, M. (2006). "Optimal Portfolio Allocation under Higher Moments." European Financial Management, 12(1), 29-55.
- paper | Martellini, L. and Ziemann, V. (2010). "Improved Estimates of Higher-Order Comoments and Implications for Portfolio Selection." The Review of Financial Studies, 23(4), 1467-1502.
- library | Shares similar logic as PerformanceAnalytics (R)'s [M3.MM](https://github.com/cran/PerformanceAnalytics/blob/2.1.0/R/MultivariateMoments.R#L34){:target="_blank"} (sample)
- library | Shares similar logic as PerformanceAnalytics (R)'s [M3.ewma](https://github.com/cran/PerformanceAnalytics/blob/2.1.0/R/MultivariateMoments.R#L1486){:target="_blank"} (exponential)
- library | Shares similar logic as PortfolioAnalytics (R)'s [CCCgarch.MM](https://github.com/cran/PortfolioAnalytics/blob/2.1.2/R/moment.functions.R#L22){:target="_blank"} (CCC-GARCH)

**Args:**

- <u>method (str, optional):</u> The estimator of the co-moments. Options are: "sample" (equal weights),
"exponential" (exponentially weighted), "semi" (lower semi co-moment), "ccc_garch" (CCC-GARCH
scenarios). Defaults to "sample".
- <u>period (str, optional):</u> The frequency of the returns. Options are: "daily" (daily returns), "weekly"
(weekly returns), "monthly" (monthly returns), "quarterly" (quarterly returns), "yearly" (yearly
returns). Defaults to "daily".
- <u>span (int, optional):</u> The span in periods of the exponential weights. Defaults to 180.
- <u>standardized_moments (bool, optional):</u> Whether to divide by the product of the
standard deviations, so the diagonal $$m_{\text{iii}}$$ is the skewness of each asset
and the entries are comparable across frequencies. Defaults to True.
- <u>include_benchmark (bool, optional):</u> Whether to include the benchmark as an
asset. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: One row per asset i and one column per pair of assets (j, k), from
the periods in which every asset has a return, per period (not annualized).

**Notes:**

- The unstandardized sample matrix follows the same formula as PerformanceAnalytics'
M3.MM. Its M3.ewma (default $$\lambda = 0.97$$, a span of about 65.7) assumes returns with a
zero mean; the exponential estimate takes the deviations from the average return and
follows the same formula as M3.ewma on the demeaned returns.
- Unstandardized co-moments of daily returns are of the order of 1e-6, below the
default rounding of 4 decimals; a higher rounding shows them.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "JNJ"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

# The coskewness of each pair of assets with AAPL
toolkit.portfolio.get_coskewness_matrix().loc[:, "AAPL"]
```

Which returns:

|      |   AAPL |    MSFT |     JNJ |
|:-----|-------:|--------:|--------:|
| AAPL | 0.4539 |  0.3026 |  0.0257 |
| MSFT | 0.3026 |  0.198  | -0.0169 |
| JNJ  | 0.0257 | -0.0169 | -0.168  |

---

## get_cokurtosis_matrix
Calculate the cokurtosis matrix M4 of the assets, the fourth co-moments of their returns: how often assets have extreme returns at the same time.

The kurtosis of a portfolio with weights w is w'M4(w ⊗ w ⊗ w) / σ_p⁴, the input of kurtosis-aware optimizations and the modified (Cornish-Fisher) VaR of a portfolio.

The formula is as follows:

$$
m_{\text{ijkl}} = \Sigma_{t} w_{t} (r_{ti} - \mu_{i}) (r_{tj} - \mu_{j}) (r_{tk} - \mu_{k}) (r_{tl} - \mu_{l})
$$

$$
\text{Sample:}\;\; w_{t} = \frac{1}{T};\;\; \text{exponential:}\;\; w_{t} = \frac{\lambda^{T - t}}{\sum \lambda^{T - s}} \;\text{with}\; \lambda = 1 - \frac{2}{\text{span} + 1};\;\; \text{semi:}\;\; w_{t} = 1 / T \;\text{with} \;\min(r_{ti} - \mu_{i},\; 0) \;\text{in place of every deviation},\;\; \text{the lower semi cokurtosis};\;\; \text{CCC-GARCH:}\;\; w_{t} = \frac{1}{T \;\text{on the standardized residuals of the CCC-GARCH}(1,\; 1) \;\text{model at the next-period volatilities}} \;(\text{see}\; \text{get\_coskewness\_matrix}),\;\; \text{the next-period cokurtosis of the model}
$$

$$
\text{standardized:}\;\; \frac{m_{\text{ijkl}}}{\sigma_{i} \sigma_{j} \sigma_{k} \sigma_{l}} \;\text{with}\; \sigma^{2} = \Sigma_{t} w_{t} (r_{t} - \mu)^{2}
$$

**Also known as:** cokurtosis, fourth co-moment matrix, M4, semi cokurtosis.

**References:**

- paper | Jondeau, E. and Rockinger, M. (2006). "Optimal Portfolio Allocation under Higher Moments." European Financial Management, 12(1), 29-55.
- paper | Cajas, D. (2022). "Convex Optimization of Portfolio Kurtosis." SSRN 4202967.
- library | Shares similar logic as PerformanceAnalytics (R)'s [M4.MM](https://github.com/cran/PerformanceAnalytics/blob/2.1.0/R/MultivariateMoments.R#L72){:target="_blank"} (sample)
- library | Shares similar logic as PerformanceAnalytics (R)'s [M4.ewma](https://github.com/cran/PerformanceAnalytics/blob/2.1.0/R/MultivariateMoments.R#L1543){:target="_blank"} (exponential)
- library | Shares similar logic as Riskfolio-Lib's [cokurt_matrix](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/parameters.html#ParamsEstimation.cokurt_matrix){:target="_blank"} (sample and semi, as N² × N²)
- library | Shares similar logic as PortfolioAnalytics (R)'s [CCCgarch.MM](https://github.com/cran/PortfolioAnalytics/blob/2.1.2/R/moment.functions.R#L22){:target="_blank"} (CCC-GARCH)

**Args:**

- <u>method (str, optional):</u> The estimator of the co-moments. Options are: "sample" (equal weights),
"exponential" (exponentially weighted), "semi" (lower semi co-moment), "ccc_garch" (CCC-GARCH
scenarios). Defaults to "sample".
- <u>period (str, optional):</u> The frequency of the returns. Options are: "daily" (daily returns), "weekly"
(weekly returns), "monthly" (monthly returns), "quarterly" (quarterly returns), "yearly" (yearly
returns). Defaults to "daily".
- <u>span (int, optional):</u> The span in periods of the exponential weights. Defaults to 180.
- <u>standardized_moments (bool, optional):</u> Whether to divide by the product of the
standard deviations, so the diagonal $$m_{\text{iiii}}$$ is the kurtosis of each asset
(3 for a normal distribution, not the excess). Defaults to True.
- <u>include_benchmark (bool, optional):</u> Whether to include the benchmark as an
asset. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: One row per asset i and one column per triple of assets
(j, k, l), $$N \times N^{3}$$, from the periods in which every asset has a return, per
period (not annualized).

**Notes:**

- The unstandardized sample matrix follows the same formula as PerformanceAnalytics'
M4.MM; Riskfolio-Lib's cokurt_matrix holds the sample and semi cokurtosis as an
$$N^{2} \times N^{2}$$ matrix. The exponential estimate follows the same formula as M4.ewma on the
demeaned returns.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

# The cokurtosis of each pair of assets with AAPL twice
toolkit.portfolio.get_cokurtosis_matrix().loc[:, ("AAPL", "AAPL")]
```

Which returns:

|      |   AAPL |   MSFT |
|:-----|-------:|-------:|
| AAPL | 9.5182 | 6.0896 |
| MSFT | 6.0896 | 4.8517 |

---

## get_estimation_uncertainty
Calculate how uncertain the estimates of the expected returns and the covariance matrix are.

Both are estimated again on many simulated histories of the same length, and the spread of those estimates gives a confidence interval for every expected return and covariance and a standard error for every expected return. These are the box uncertainty sets of robust (worst-case) mean-variance optimization.

- The stationary bootstrap of Politis and Romano (1994), blocks of a random length with a geometric distribution of mean block_size, wrapping from the last period to the first.
- The circular block bootstrap: blocks of block_size periods that wrap around.
- The moving block bootstrap: blocks of block_size periods that start where a whole block fits (Künsch, 1989).
- The normal distribution: histories drawn from a multivariate normal distribution with the average returns and the sample covariance.

Block bootstraps keep the dependence between consecutive returns, such as volatility clustering, that drawing single periods would break.

**Also known as:** bootstrapped expected returns, uncertainty set, estimation error, block bootstrap.

**References:**

- paper | Politis, D. N. and Romano, J. P. (1994). "The Stationary Bootstrap." Journal of the American Statistical Association, 89(428), 1303-1313.
- paper | Künsch, H. R. (1989). "The Jackknife and the Bootstrap for General Stationary Observations." The Annals of Statistics, 17(3), 1217-1241.
- paper | Tütüncü, R. H. and Koenig, M. (2004). "Robust Asset Allocation." Annals of Operations Research, 132, 157-187.
- library | Shares similar logic as Riskfolio-Lib's [bootstrapping](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/parameters.html#ParamsEstimation.bootstrapping){:target="_blank"}
- library | Shares similar logic as Riskfolio-Lib's [normal_simulation](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/parameters.html#ParamsEstimation.normal_simulation){:target="_blank"} (normal distribution)
- library | Shares similar logic as skfolio's [BootstrapMuUncertaintySet](https://skfolio.org/generated/skfolio.uncertainty_set.BootstrapMuUncertaintySet.html){:target="_blank"}

**Args:**

- <u>method (str, optional):</u> How the histories are simulated. Options are: "stationary" (stationary
bootstrap), "circular" (circular block bootstrap), "moving" (moving block bootstrap), "normal"
(multivariate normal draws). Defaults to "stationary".
- <u>period (str, optional):</u> The frequency of the returns. Options are: "daily" (daily returns), "weekly"
(weekly returns), "monthly" (monthly returns), "quarterly" (quarterly returns), "yearly" (yearly
returns). Defaults to "daily".
- <u>n_bootstrap (int, optional):</u> The number of simulated histories. Defaults to
1000 (as skfolio; Riskfolio-Lib draws 6000).
- <u>block_size (int, optional):</u> The (average) number of periods in a block.
Defaults to 3 (as Riskfolio-Lib's window).
- <u>confidence_level (float, optional):</u> The confidence level of the bounds, the
(1 - c) / 2 and (1 + c) / 2 percentiles of the estimates. Defaults to 0.95.
- <u>seed (int &#124; None, optional):</u> The seed of the random draws, so the result repeats; None draws a new one
every time. Defaults to 0.
- <u>output (str, optional):</u> Options are: "expected_returns" (the Expected Return, Lower, Upper and Standard
Error per asset), "covariance" (the Lower and Upper bound of every covariance). Defaults to
"expected_returns".
- <u>include_benchmark (bool, optional):</u> Whether to include the benchmark as an
asset. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The annualized estimates and their bounds (the averages per
period, their bounds and standard errors and the covariances times the number
of periods in a year, without compounding).

**Notes:**

- The bounds of the covariances hold per entry and are not adjusted to form
positive semidefinite matrices. Riskfolio-Lib draws with the arch package, so
its bounds agree with these in distribution, not draw for draw.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "JNJ", "XOM"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.portfolio.get_estimation_uncertainty()
```

Which returns:

|      |   Expected Return |   Lower |   Upper |   Standard Error |
|:-----|------------------:|--------:|--------:|-----------------:|
| AAPL |            0.1932 | -0.0568 |  0.4194 |           0.1207 |
| MSFT |            0.2017 | -0.0032 |  0.3985 |           0.1045 |
| JNJ  |            0.0987 | -0.0518 |  0.2328 |           0.0756 |
| XOM  |            0.2911 |  0.063  |  0.5191 |           0.1179 |

---

## get_factor_loadings
Estimate the loadings of a time series factor model.

It is the regression of every asset's returns on factor returns, by default the five factors of Fama and French (market, size, value, profitability and investment), $$r_{i,t} = \alpha_{i} + \sum_{f} \beta_{i,f} F_{f,t} + \epsilon_{i,t}$$. The loadings are what the factor covariance, the factor risk contributions, the factor attribution and the augmented and Bayesian Black-Litterman models build on.

- Ordinary least squares on every factor.
- Forward selection: starting without factors, add the factor with the lowest p-value as long as every p-value stays at or below the threshold (or, with another criterion, as long as it improves); the factors left out load zero.
- Backward selection: starting with every factor, drop the one with the highest p-value until all are at or below the threshold (or as long as dropping one improves the criterion). Both stepwise selections keep at least the single best factor on the p-value.
- Principal components regression: the standardized factors' first principal components that explain the given share of their variance as regressors, mapped back to loadings on the factors, which removes the instability that correlated factors give OLS (Jolliffe, 1982).

The Alpha is the annualized intercept, $$\alpha$$ times the number of periods in a year. The R Squared is the share of an asset's variance the factors explain and the Residual Volatility (ddof=1, annualized) what they leave, the idiosyncratic risk the factor covariance keeps on the diagonal.

**Also known as:** factor exposures, factor betas, loadings matrix, stepwise regression, principal components regression.

**References:**

- paper | Fama, E. F. and French, K. R. (1993). "Common Risk Factors in the Returns on Stocks and Bonds." Journal of Financial Economics, 33(1), 3-56.
- paper | Fama, E. F. and French, K. R. (2015). "A Five-Factor Asset Pricing Model." Journal of Financial Economics, 116(1), 1-22.
- paper | Connor, G. (1995). "The Three Types of Factor Models: A Comparison of Their Explanatory Power." Financial Analysts Journal, 51(3), 42-46.
- paper | Jolliffe, I. T. (1982). "A Note on the Use of Principal Components in Regression." Journal of the Royal Statistical Society, Series C, 31(3), 300-303.
- library | Referenced against Riskfolio-Lib's [loadings_matrix](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/parameters.html#ParamsEstimation.loadings_matrix){:target="_blank"} (backward selection, every factor kept)
- library | Referenced against Riskfolio-Lib's [PCR](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/parameters.html#ParamsEstimation.PCR){:target="_blank"}
- library | Shares similar logic as Riskfolio-Lib's [forward_regression](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/parameters.html#ParamsEstimation.forward_regression){:target="_blank"}
- library | Shares similar logic as Riskfolio-Lib's [backward_regression](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/parameters.html#ParamsEstimation.backward_regression){:target="_blank"}

**Args:**

- <u>selection (str, optional):</u> Options are: "ols" (every factor), "forward" (forward selection), "backward"
(backward selection), "pcr" (principal components regression). Defaults to "ols".
- <u>criterion (str, optional):</u> What the stepwise selections compare. Options are: "pvalue" (p-value), "aic"
(Akaike information criterion), "bic" (Schwarz information criterion), "r_squared" (R squared),
"adjusted_r_squared" (adjusted R squared). Defaults to "pvalue".
- <u>threshold (float, optional):</u> The highest p-value a selected factor may have.
Defaults to 0.05.
- <u>components (float, optional):</u> The principal components the principal components regression keeps: a
number of 1 or more, or between 0 and 1 the share of the variance of the standardized factors to
explain. Defaults to 0.95.
- <u>factors (pd.DataFrame &#124; None, optional):</u> The factor returns, one column per
factor, at the frequency of the period. Defaults to None, the Fama and
French five factors of the region.
- <u>region (str, optional):</u> The region of the Fama and French factors. Options are: "United States",
"Developed", "Developed ex US", "Europe", "Japan", "Asia Pacific ex Japan", "North America".
Defaults to "United States".
- <u>period (str, optional):</u> The frequency of the returns. Options are: "daily" (daily returns), "weekly"
(weekly returns), "monthly" (monthly returns), "quarterly" (quarterly returns), "yearly" (yearly
returns). Defaults to "daily".
- <u>include_benchmark (bool, optional):</u> Whether to include the benchmark as an
asset. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per asset the Alpha (annualized), the loading on every factor,
the R Squared and the Residual Volatility (annualized), from the periods in
which every asset and every factor has a return.

**Notes:**

- The Fama and French factors are excess returns while the asset returns are
total returns, so the Alpha holds the risk free rate. Ken French publishes the
factors about a month after each month ends, so the latest weeks are left out.
- OLS gives the loadings of Riskfolio-Lib's loadings_matrix as a backward selection at a
threshold of 1; the AIC and BIC are defined as statsmodels defines them
(Riskfolio-Lib's AIC and SIC).

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "JNJ", "XOM"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.portfolio.get_factor_loadings(selection="forward")
```

Which returns:

|      |   Alpha |   Mkt-RF |     SMB |     HML |     RMW |     CMA |   R Squared |   Residual Volatility |
|:-----|--------:|---------:|--------:|--------:|--------:|--------:|------------:|----------------------:|
| AAPL |  0.0726 |   1.1791 | -0.2683 | -0.3519 |  0      |  0.3824 |      0.6004 |                0.1761 |
| MSFT |  0.0851 |   1.0449 | -0.321  | -0.3811 |  0.3329 | -0.2635 |      0.6806 |                0.1453 |
| JNJ  |  0.0387 |   0.2901 | -0.1045 |  0.1992 |  0.1657 |  0      |      0.0868 |                0.1599 |
| XOM  |  0.1409 |   0.7905 | -0.2442 |  1.0268 | -0.4884 |  0.2562 |      0.3934 |                0.2105 |

---

## get_factor_risk_contributions
Calculate how much each factor, by default the five factors of Fama and French, contributes to the risk of a portfolio, rather than each asset.

The portfolio's exposure to the factors is y = B'w, with B the loadings of the assets on the factors (see get_factor_loadings), and the marginal risk of the factors follows from that of the assets $$m = \partial \rho / \partial w$$ (see get_risk_contributions) through the pseudo-inverse of B': $$\partial \rho / \partial y$$ = pinv(B')'m. A factor contributes its exposure times its marginal risk, and the part of the weights the factors cannot span forms an Other factor, so the contributions add up to the risk measure (Meucci, 2009; Roncalli and Weisang, 2016). With fewer assets than factors the factors span every portfolio and Other is zero.

The risk measure is any of get_risk_contributions: the volatility (annualized), the expected shortfall, the drawdowns or the other measures of the Risk module (per period).

**Also known as:** factor risk decomposition, factor risk budget, risk factor contributions.

**References:**

- paper | Meucci, A. (2009). "Managing Diversification." Risk, 22(5), 74-79.
- paper | Roncalli, T. and Weisang, G. (2016). "Risk Parity Portfolios with Risk Factors." Quantitative Finance, 16(3), 377-388.
- paper | Fama, E. F. and French, K. R. (2015). "A Five-Factor Asset Pricing Model." Journal of Financial Economics, 116(1), 1-22.
- library | Referenced against Riskfolio-Lib's [Factors_Risk_Contribution](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/risk.html#RiskFunctions.Factors_Risk_Contribution){:target="_blank"}

**Args:**

- <u>weights (dict[str, float] &#124; None, optional):</u> The weight per asset. Defaults to
None, which uses the latest weights of the Portfolio the Toolkit came from,
or equal weights.
- <u>risk_measure (str, optional):</u> A risk measure of get_risk_contributions. Options are: "volatility" (of
the covariance estimate), "cvar" (the expected shortfall), "semideviation" (below a return of zero),
"mad" (the mean absolute deviation), "cdar" (the Conditional Drawdown at Risk), "var" (historical
Value at Risk), "evar" (Entropic Value at Risk), "worst_realization" (the largest loss),
"gini_mean_difference" (Gini mean difference), "tail_gini" (Tail Gini), "lower_partial_moment"
(first lower partial moment below zero), "kurtosis" (square root of the fourth central moment),
"maximum_drawdown" (maximum drawdown), "average_drawdown" (average drawdown), "drawdown_at_risk"
(Drawdown at Risk), "entropic_drawdown_at_risk" (Entropic Drawdown at Risk), "ulcer_index" (Ulcer
Index). Defaults to "volatility".
- <u>alpha (float, optional):</u> The tail probability of the tail measures, e.g.
0.05 for the worst 5% of periods. Defaults to 0.05.
- <u>selection (str, optional):</u> How the loadings are estimated (see get_factor_loadings). Options are: "ols"
(every factor), "forward" (forward selection), "backward" (backward selection), "pcr" (principal
components regression). Defaults to "ols".
- <u>factors (pd.DataFrame &#124; None, optional):</u> The factor returns, one column per
factor, at the frequency of the period. Defaults to None, the Fama and
French five factors of the region.
- <u>region (str, optional):</u> The region of the Fama and French factors. Options are: "United States",
"Developed", "Developed ex US", "Europe", "Japan", "Asia Pacific ex Japan", "North America".
Defaults to "United States".
- <u>period (str, optional):</u> The frequency of the returns. Options are: "daily" (daily returns), "weekly"
(weekly returns), "monthly" (monthly returns), "quarterly" (quarterly returns), "yearly" (yearly
returns). Defaults to "daily".
- <u>include_benchmark (bool, optional):</u> Whether to include the benchmark as an
asset. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per factor, Other and in total, the Exposure, Marginal
Contribution, Risk Contribution and Percentage Contribution, on the periods in
which the assets held and the factors all have a return.

**Notes:**

- Riskfolio-Lib's Factors_Risk_Contribution uses the same inputs with OLS loadings: the
volatility uses the sample covariance (ddof=1) of the asset returns, annualized,
and the other measures their historical returns.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "JNJ", "XOM"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.portfolio.get_factor_risk_contributions(
    weights={"AAPL": 0.4, "MSFT": 0.3, "JNJ": 0.2, "XOM": 0.1}
)
```

Which returns:

| Factor   |   Exposure |   Marginal Contribution |   Risk Contribution |   Percentage Contribution |
|:---------|-----------:|------------------------:|--------------------:|--------------------------:|
| Mkt-RF   |     0.9376 |                  0.1727 |              0.1619 |                    0.873  |
| SMB      |    -0.1694 |                 -0.0254 |              0.0043 |                    0.0232 |
| HML      |    -0.1765 |                 -0.0437 |              0.0077 |                    0.0415 |
| RMW      |     0.2806 |                  0.0337 |              0.0095 |                    0.051  |
| CMA      |     0.1144 |                  0.0184 |              0.0021 |                    0.0113 |
| Other    |   nan      |                nan      |              0      |                    0      |
| Total    |   nan      |                nan      |              0.1855 |                    1      |

---

## get_entropy_pooling
Reweight the historical periods so that they agree with views on the assets, by Entropy Pooling (Meucci, 2008).

These are the probabilities of the periods closest to equal probabilities in relative entropy, $$\sum p_{t} \ln (p_{t} T)$$, under which the views hold. The returns themselves stay as they were, so the posterior keeps the fat tails and co-movements of the history; only how much each period counts changes. The posterior expected returns and covariance matrix follow from the probabilities.

Views are annualized, like those of get_black_litterman_weights:

- views: the expected return of an asset ({"AAPL": 0.10}, an arithmetic return a year) or the difference of two ({"AAPL-MSFT": 0.02}).
- volatility_views: the annualized volatility of an asset ({"AAPL": 0.25}).
- correlation_views: the correlation of two assets ({"AAPL-MSFT": 0.5}).
- ranking: an ordering of the expected returns, from the highest to the lowest (["XOM", "MSFT", "AAPL"]), the ranking views of Meucci (2008): the inequalities $$E_{p} [r_{k + 1}] \leq E_{p} [r_{k}]$$ for every pair of neighbours, imposed with the views on the expected returns. Only the order is stated, not by how much.

A view is an equality (a number) or an inequality, a pair (">=", 0.10) or ("<=", 0.10). The views on volatilities hold the means found with the mean views, and the views on correlations hold both the means and the volatilities, the sequential treatment of Meucci, Ardia and Keel (2011), in the order skfolio's EntropyPooling takes them. The problem is solved through its dual with SciPy's L-BFGS-B.

With opinions, a list of views of several experts, each a dictionary with the keys "views", "volatility_views", "correlation_views" and "ranking", every opinion gets its own posterior and these are pooled with the opinion weights (equal by default; any weight left to sum to one goes to the equal prior probabilities): linearly, $$p = \sum \pi_{k} p_{k}$$ (Stone, 1961), or logarithmically, p ∝ $$\Pi p_{k,k}^{\pi}$$ (Genest and Zidek, 1986), optionally weighing down opinions far from the consensus by exp(-α KL(p_k ‖ c)) with $$\alpha$$ the divergence penalty.

**Also known as:** fully flexible views, fully flexible probabilities, opinion pooling, views on scenarios, ranking views, ordering views.

**References:**

- paper | Meucci, A. (2008). "Fully Flexible Views: Theory and Practice." Risk, 21(10), 97-102.
- paper | Stone, M. (1961). "The Opinion Pool." The Annals of Mathematical Statistics, 32(4), 1339-1342.
- paper | Genest, C. and Zidek, J. V. (1986). "Combining Probability Distributions: A Critique and an Annotated Bibliography." Statistical Science, 1(1), 114-135.
- library | Referenced against skfolio's [EntropyPooling](https://skfolio.org/generated/skfolio.prior.EntropyPooling.html){:target="_blank"}
- library | Referenced against skfolio's [OpinionPooling](https://skfolio.org/generated/skfolio.prior.OpinionPooling.html){:target="_blank"}

**Args:**

- <u>views (dict &#124; None, optional):</u> The annualized expected return views. Defaults
to None.
- <u>volatility_views (dict &#124; None, optional):</u> The annualized volatility views.
Defaults to None.
- <u>correlation_views (dict &#124; None, optional):</u> The correlation views. Defaults to
None.
- <u>ranking (list[str] &#124; None, optional):</u> Assets from the highest expected return
to the lowest, at least two. Defaults to None.
- <u>opinions (list[dict] &#124; None, optional):</u> The views of several experts to pool,
instead of views, volatility_views, correlation_views and ranking. Defaults
to None.
- <u>opinion_weights (list[float] &#124; None, optional):</u> The weight of every opinion,
summing to at most one. Defaults to None, equal weights.
- <u>pooling (str, optional):</u> How the opinions are pooled. Options are: "linear" (arithmetic mixture),
"logarithmic" (geometric mixture). Defaults to "linear".
- <u>divergence_penalty (float, optional):</u> The penalty $$\alpha$$ on an opinion's relative
entropy to the consensus. Defaults to 0.
- <u>output (str, optional):</u> Options are: "moments" (the prior and posterior expected return and volatility
per asset), "covariance" (the posterior covariance matrix), "probabilities" (the prior and posterior
probability of every period), "summary" (the relative entropy and the effective number of periods).
Defaults to "moments".
- <u>period (str, optional):</u> The frequency of the returns. Options are: "daily" (daily returns), "weekly"
(weekly returns), "monthly" (monthly returns), "quarterly" (quarterly returns), "yearly" (yearly
returns). Defaults to "daily".
- <u>include_benchmark (bool, optional):</u> Whether to include the benchmark as an
asset. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The output chosen: the expected returns (arithmetic averages
times the number of periods in a year) and volatilities (annualized), the
annualized covariance matrix, the probabilities, or the Relative Entropy,
Effective Number of Scenarios (exp of the entropy of the probabilities, T for
equal ones) and the number of Scenarios.

**Notes:**

- The posterior covariance is the probability-weighted covariance $$\sum p_{t} (r_{t} - \mu)$$
$$(r_{t} - \mu)'$$ with $$\mu = \sum p_{t} r_{t}$$, without a small-sample correction, the basis on
which the views are imposed, so a volatility view comes back exactly. skfolio
applies numpy's correction for weights, $$1 / (1 - \sum p_{t}^{2})$$, on top, which raises
the variance by about 1 / T (0.1% for daily data, 3% for 36 monthly returns).
- The prior volatility is the sample standard deviation of the returns (ddof=1),
as elsewhere in the Finance Toolkit. With equal probabilities the posterior's
basis gives a volatility $$\sqrt{(T - 1) / T}$$ times the prior's, so without views
the two columns differ by that factor.
- With mean and volatility views the probabilities agree with skfolio's EntropyPooling
to 1e-9; with correlation views the views are met here more tightly and the posterior
lies at least as close to the prior (a lower relative entropy).
- A ranking is the set of relative views ("MSFT-XOM": ("<=", 0)) that
PortfolioAnalytics' meucci.ranking imposes, which takes the order from the lowest
expected return to the highest. A ranking the history already follows leaves the
probabilities equal.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "JNJ", "XOM"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.portfolio.get_entropy_pooling(
    views={"AAPL": 0.05, "XOM-JNJ": (">=", 0.02)},
    volatility_views={"MSFT": 0.30},
)
```

Which returns:

|      |   Prior Return |   Posterior Return |   Prior Volatility |   Posterior Volatility |
|:-----|---------------:|-------------------:|-------------------:|-----------------------:|
| AAPL |         0.1932 |             0.05   |             0.2786 |                 0.3151 |
| MSFT |         0.2017 |             0.118  |             0.2571 |                 0.3    |
| JNJ  |         0.0987 |             0.0698 |             0.1673 |                 0.1696 |
| XOM  |         0.2911 |             0.264  |             0.2702 |                 0.2762 |

---

## get_return_contributions
Calculate how much each asset added to the portfolio's return in every period.

The periods are weeks, months, quarters or years, and the contributions of the assets add up to the portfolio's return of that period. Every day an asset contributes its weight at the start of the day times its return, $$c_{i,t} = w_{i,t} - 1 r_{i,t}$$, which add up to the portfolio's daily return $$R_{t} = \sum c_{i,t}$$. Over a longer period the daily contributions are carried by the growth of the portfolio since the period began: $$C_{i} = \sum_{t} c_{i,t} \Pi_{s < t} (1 + R_{s})$$, the contribution in money divided by the value at the start of the period, so the contributions add up to the compounded return $$\Pi (1 + R_{t}) - 1$$ (Bacon, 2008).

The weights are the latest weights of the Portfolio the Toolkit came from, as they moved from day to day, or, when weights are given (or there is no Portfolio), those weights restored every day.

**Also known as:** contribution to return, return attribution by asset, performance contribution.

**References:**

- paper | Bacon, C. R. (2008). "Practical Portfolio Performance Measurement and Attribution." 2nd edition, Wiley, chapter 5.
- library | Shares similar logic as PerformanceAnalytics (R)'s [to.period.contributions](https://github.com/cran/PerformanceAnalytics/blob/2.1.0/R/to.period.contributions.R#L45){:target="_blank"}

**Args:**

- <u>weights (dict[str, float] &#124; None, optional):</u> The weight per asset. Defaults to
None, which uses the weights of the Portfolio the Toolkit came from over
time, or equal weights.
- <u>period (str, optional):</u> The period to add the contributions up over. Options are: "daily" (daily
returns), "weekly" (weekly returns), "monthly" (monthly returns), "quarterly" (quarterly returns),
"yearly" (yearly returns). Defaults to "monthly".
- <u>include_benchmark (bool, optional):</u> Whether to include the benchmark as an
asset. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per period the contribution of every asset held and the
Portfolio return, compounded within the period.

**Notes:**

- The contributions follow PerformanceAnalytics' to.period.contributions of the daily
contributions; with given weights these are rebalanced every day, not left to drift.
- With fixed weights (given, or equal ones) the periods start on the first day on
which every asset held has a return, so an asset that was not listed yet does not
count as a return of 0, as in get_portfolio_risk_metrics. Within the sample a day
on which an asset has no return (it did not trade) is a contribution of 0.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "JNJ", "XOM"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.portfolio.get_return_contributions(
    weights={"AAPL": 0.4, "MSFT": 0.3, "JNJ": 0.2, "XOM": 0.1}, period="yearly"
)
```

Which returns:

| Date   |    AAPL |    MSFT |     JNJ |     XOM |   Portfolio |
|:-------|--------:|--------:|--------:|--------:|------------:|
| 2021   |  0.1698 |  0.1574 |  0.0289 |  0.0514 |      0.4074 |
| 2022   | -0.1049 | -0.0914 |  0.0105 |  0.0655 |     -0.1204 |
| 2023   |  0.1833 |  0.1649 | -0.0136 | -0.0046 |      0.3301 |
| 2024   |  0.1263 |  0.0396 | -0.0087 |  0.0116 |      0.1689 |
| 2025   |  0.0598 |  0.04   |  0.0889 |  0.0187 |      0.2074 |

---

## get_stress_test
Calculate how a portfolio would have fared in historical market crises.

It shows the return of every asset and of the buy-and-hold portfolio from the start to the end of each scenario, next to the benchmark. The default scenarios run from the peak to the trough of the S&P 500: the Dot-com Crash, the Global Financial Crisis, the Euro Area Debt Crisis, the 2015-2016 and 2018 Q4 sell-offs, the COVID-19 Crash and the 2022 Rate Shock.

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
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per scenario its Start Date and End Date, the Portfolio Return,
the Benchmark Return, the Coverage (the share of the portfolio's gross
exposure with prices in the scenario, from 0 to 1) and the return of every
asset.

**Notes:**

- An asset that was not listed yet at the start of a scenario has no return there;
the other weights are scaled up to a net weight of one and the Coverage shows
the share of the gross exposure, $$\sum \vert w_{i} \vert$$ over the assets with prices / $$\sum \vert w_{i} \vert$$,
that had data.
- When the assets with prices have a net weight of zero or less (only the short
positions of a long-short portfolio), they cannot be scaled up to the
portfolio, so the Portfolio Return of that scenario is empty and a warning is
logged, as it is when none of the assets has prices.

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
Calculate a portfolio's exposure after looking through its funds.

An ETF's weight is spread over its own sectors, countries or holdings, a stock counts fully towards its own sector, country or itself, and everything is summed. It shows, for example, that a portfolio of a technology ETF and Apple holds far more Apple and technology than either position suggests. The benchmark's exposure and the difference (the active exposure) are shown next to it when the benchmark is a fund.

**Also known as:** look-through analysis, underlying exposure, X-ray.

**Args:**

- <u>weights (dict[str, float] &#124; None, optional):</u> The weight per asset. Defaults to
None, which uses the latest weights of the Portfolio the Toolkit came from,
or equal weights.
- <u>by (str, optional):</u> What to look through to. Options are: "sector" (the sectors), "country" (the
countries), "holdings" (the holdings). Defaults to "sector".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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
Calculate the Brinson-Fachler attribution of the portfolio's return over the benchmark, by sector, over the Toolkit's date range.

The excess return is split into three effects per sector:

- Allocation: the reward for overweighting sectors that beat the benchmark (and underweighting those that lagged).
- Selection: the reward for holding better stocks than the benchmark within a sector.
- Interaction: the combined effect of both decisions.

The portfolio's sector returns come from its holdings (buy and hold from the start date). A stock counts towards its own sector and a fund is looked through to its sector weightings, as in get_look_through_exposure, so that QQQ counts as mostly Technology rather than as the sector of its issuer. The benchmark's sector weights come from the benchmark fund and its sector returns from the Select Sector SPDR funds (XLK, XLF, XLV, ...), which track the sectors of the S&P 500.

With a period, the range is split into sub-periods (weeks, months, quarters or years). Every sub-period gets its own attribution with the weights at its start, and the effects are linked into effects over the whole range that add up to the compounded excess return. The holdings are bought at the start and held without rebalancing, so the portfolio's weights drift with the returns of its assets; the benchmark's sector weights drift with the returns of the sector funds in the same way. The compounded returns of the sub-periods therefore equal the returns of the attribution without a period, and only the effects differ: they reflect the weights held in each sub-period rather than those at the start.

The formula is as follows:

$$
\text{Allocation}_{t} = (w_{p,t} - w_{b,t}) \cdot (r_{b,t} - B_{t})
$$

$$
\text{Selection}_{t} = w_{b,t} \cdot (r_{p,t} - r_{b,t})
$$

$$
\text{Interaction}_{t} = (w_{p,t} - w_{b,t}) \cdot (r_{p,t} - r_{b,t})
$$

$$
\text{Cariño:}\;\; \text{Linked Effect} = \Sigma_{t} \left(\frac{k_{t}}{K}\right) \cdot \text{Effect}_{t},\;\; \text{with}\;\; k_{t} = \frac{\ln(1 + R_{t}) - \ln(1 + B_{t})}{R_{t} - B_{t}}\;\;\text{and}\;\; K = \frac{\ln(1 + R) - \ln(1 + B)}{R - B},\;\; \text{or}\;\; \frac{1}{1 + R_{t}} \;\text{and} \;\frac{1}{1 + R} \;\text{when the returns are equal}
$$

$$
\text{Menchero:}\;\; \text{Linked Effect} = \Sigma_{t} (M + \alpha_{t}) \cdot \text{Effect}_{t},\;\; \text{with}\;\; M = \frac{\frac{R - B}{T}}{(1 + R)^{\frac{1}{T}} - (1 + B)^{\frac{1}{T}}}\;\;\text{and}\;\; \alpha_{t} = \frac{R - B - M x \Sigma_{s} (R_{s} - B_{s})}{\Sigma_{s} (R_{s} - B_{s})^{2} x (R_{t} - B_{t})}
$$

Here $$w_{p,t}$$ and $$w_{b,t}$$ are the sector weights at the start of sub-period t, $$r_{p,t}$$ and $$r_{b,t}$$ the sector returns, $$R_{t}$$ and $$B_{t}$$ the portfolio and benchmark returns in the sub-period, R and B those returns compounded over all T sub-periods. Without a period the first three lines apply once to the whole range.

**Also known as:** performance attribution, BHB attribution, sector attribution.

**References:**

- paper | Brinson, G.P. and Fachler, N. (1985). "Measuring Non-US Equity Portfolio Performance." The Journal of Portfolio Management, 11(3), 73-76.
- paper | Brinson, G.P., Hood, L.R. and Beebower, G.L. (1986). "Determinants of Portfolio Performance." Financial Analysts Journal, 42(4), 39-44.
- paper | Cariño, D.R. (1999). "Combining Attribution Effects Over Time." The Journal of Performance Measurement, 3(4), 5-14.
- paper | Menchero, J. (2000). "An Optimized Approach to Linking Attribution Effects Over Time." The Journal of Performance Measurement, 5(1), 36-42.
- paper | Bacon, C. (2004). Practical Portfolio Performance Measurement and Attribution. Wiley, pp. 191-196.

**Args:**

- <u>weights (dict[str, float] &#124; None, optional):</u> The weight per asset at the start of
the date range. Defaults to None, which uses the latest weights of the
Portfolio the Toolkit came from, or equal weights.
- <u>period (str &#124; None, optional):</u> The sub-periods whose attributions are linked, each ending on the last
trading day of the calendar period. Options are: "weekly", "monthly", "quarterly", "yearly". Defaults
to None, which attributes the whole range as one period.
- <u>linking (str, optional):</u> How the effects of the sub-periods are linked when a period is given. Options
are: "carino" (Cariño, 1999), "menchero" (Menchero, 2000). Defaults to "carino".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per sector and in total, the Portfolio Weight, Benchmark Weight
(at the start of the range), Portfolio Return, Benchmark Return (over the whole
range) and the Allocation, Selection, Interaction and Total Effect, linked over
the sub-periods when a period is given. The Total row's effects add up to the
excess return.

**Notes:**

- The benchmark fund's sector weights are its current weights, applied to the whole
date range, and the sector funds stand in for the benchmark's sectors; for a
benchmark other than the S&P 500 this is an approximation.
- A fund's weight is spread over its current sector weightings and every part earns
the fund's own return, as the return of a fund's sectors separately is not known.
Assets without a sector are "Unclassified" and compared with the benchmark as a
whole.
- A sector whose sector fund has no price within a few trading days of the start of
the range (XLC starts on 2018-06-19, XLRE on 2015-10-08) has no benchmark return,
since the fund's return from its first price covers only part of the range. The
sector keeps its benchmark weight rather than handing it to the other sectors, a
warning names the fund and its first date, and the benchmark's total return, every
allocation effect, the sector's selection and interaction effects and the Total
row's effects are empty. With a period this holds for the sub-periods that start
before the fund's first price, and as the linking of the effects depends on the
benchmark return compounded over the whole range, all linked effects are empty. A
range that starts at the fund's first price can be attributed in full.
- Cariño's linking scales each sub-period by its logarithmic excess return relative
to the whole range; Menchero's keeps the scaling as close as possible to one
factor for every sub-period. Both make the linked effects add up exactly to the
compounded portfolio return minus the compounded benchmark return.

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

## get_factor_attribution
Attribute the return of a portfolio in every period to factors, by default the five factors of Fama and French (market, size, value, profitability and investment).

It shows the part of the return its exposure to each factor explains, and the specific return that is left. The loadings of the assets on the factors come from a regression over the whole period (see get_factor_loadings), and the portfolio's exposure to a factor is the weighted sum of its assets' loadings.

- Exposure_f,t = $$\sum_{i} w_{i,t} \beta_{i,f}$$
- Contribution_f,t = Exposure_f,t × Factor Return_f,t
- Common Return = $$\sum_{f}$$ Contribution_f,t
- Specific Return = Total Return - Common Return
- Tilt Return = $$\sum_{f}$$ Average Exposure_f × Factor Return_f,t
- Timing Return = Common Return - Tilt Return

The Specific Return holds the alphas of the assets (and the risk free rate, as the Fama and French factors are excess returns) and their residual returns. The Tilt Return is what the average exposure earned and the Timing Return what moving the exposures around it added, which is zero for weights that stay the same.

The weights are those of the Portfolio the Toolkit came from at the end of the period before, or, when weights are given (or there is no Portfolio), those weights restored every period.

**Also known as:** performance attribution to risk factors, factor return attribution, returns-based attribution, common and specific returns.

**References:**

- paper | Grinold, R. C. and Kahn, R. N. (2000). "Active Portfolio Management." 2nd edition, McGraw-Hill, chapter 17.
- paper | Fama, E. F. and French, K. R. (2015). "A Five-Factor Asset Pricing Model." Journal of Financial Economics, 116(1), 1-22.
- library | Referenced against empyrical's [perf_attrib](https://github.com/stefan-jansen/empyrical-reloaded/blob/0.7.3/src/empyrical/perf_attrib.py#L5){:target="_blank"}
- library | Shares similar logic as empyrical's [compute_exposures](https://github.com/stefan-jansen/empyrical-reloaded/blob/0.7.3/src/empyrical/perf_attrib.py#L139){:target="_blank"}
- library | Shares similar logic as pyfolio's [perf_attrib](https://github.com/stefan-jansen/pyfolio-reloaded/blob/0.9.9/src/pyfolio/perf_attrib.py#L29){:target="_blank"}

**Args:**

- <u>weights (dict[str, float] &#124; None, optional):</u> The weight per asset. Defaults to
None, which uses the weights of the Portfolio the Toolkit came from over
time, or equal weights.
- <u>selection (str, optional):</u> How the loadings are estimated (see get_factor_loadings). Options are: "ols"
(every factor), "forward" (forward selection), "backward" (backward selection), "pcr" (principal
components regression). Defaults to "ols".
- <u>factors (pd.DataFrame &#124; None, optional):</u> The factor returns, one column per
factor, at the frequency of the period. Defaults to None, the Fama and
French five factors of the region.
- <u>region (str, optional):</u> The region of the Fama and French factors. Options are: "United States",
"Developed", "Developed ex US", "Europe", "Japan", "Asia Pacific ex Japan", "North America".
Defaults to "United States".
- <u>period (str, optional):</u> The frequency of the returns. Options are: "daily" (daily returns), "weekly"
(weekly returns), "monthly" (monthly returns), "quarterly" (quarterly returns), "yearly" (yearly
returns). Defaults to "daily".
- <u>include_benchmark (bool, optional):</u> Whether to include the benchmark as an
asset. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per period the contribution of every factor and the Common,
Specific, Total, Tilt and Timing Return, on the periods in which the assets and
the factors all have a return.

**Notes:**

- The loadings are estimated on the whole period, so the attribution of an early
period uses information from later ones; it explains the past, it does not
forecast.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "JNJ", "XOM"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.portfolio.get_factor_attribution(
    weights={"AAPL": 0.4, "MSFT": 0.3, "JNJ": 0.2, "XOM": 0.1}, period="monthly"
).tail(4).T
```

Which returns:

|                 |   2025-09 |   2025-10 |   2025-11 |   2025-12 |
|:----------------|----------:|----------:|----------:|----------:|
| Mkt-RF          |    0.0297 |    0.017  |   -0.0012 |   -0.003  |
| SMB             |    0.0043 |    0.0028 |   -0.0033 |    0.0004 |
| HML             |    0.0019 |    0.0058 |   -0.0068 |   -0.0042 |
| RMW             |   -0.005  |   -0.013  |    0.0032 |    0.0006 |
| CMA             |   -0.003  |   -0.0055 |    0.0008 |    0.0005 |
| Common Return   |    0.0278 |    0.0071 |   -0.0072 |   -0.0058 |
| Specific Return |    0.0256 |    0.0227 |    0.0284 |   -0.0055 |
| Total Return    |    0.0534 |    0.0298 |    0.0213 |   -0.0113 |
| Tilt Return     |    0.0278 |    0.0071 |   -0.0072 |   -0.0058 |
| Timing Return   |    0      |    0      |    0      |    0      |

---

## get_minimum_variance_weights
Calculate the weights of the minimum variance portfolio: the fully invested portfolio of the Toolkit's assets with the lowest volatility.

It uses only the covariance matrix, not the expected returns, which makes it the most robust of the mean-variance portfolios to estimation error.

The weights minimize $$w' \Sigma w$$ subject to the weights summing to one and lying between the minimum and maximum weight, where $$\Sigma$$ is the annualized covariance matrix of the returns.

An L2 regularization $$\gamma$$ adds the penalty $$\gamma$$ w'w, so the weights minimize $$w' (\Sigma + \gamma I) w$$, a ridge on the weights. With the weights summing to one, w'w is the squared distance from the equal weights plus 1/N, so a higher $$\gamma$$ moves the portfolio towards equal weights, which tempers the estimation error in $$\Sigma$$.

**Also known as:** global minimum variance portfolio, GMV, lowest risk portfolio.

**References:**

- paper | Markowitz, H. (1952). "Portfolio Selection." The Journal of Finance, 7(1), 77-91.
- paper | DeMiguel, V., Garlappi, L., Nogales, F. J. and Uppal, R. (2009). "A Generalized Approach to Portfolio Optimization: Improving Performance by Constraining Portfolio Norms." Management Science, 55(5), 798-812.
- paper | Hoerl, A. E. and Kennard, R. W. (1970). "Ridge Regression: Biased Estimation for Nonorthogonal Problems." Technometrics, 12(1), 55-67.
- library | Referenced against PyPortfolioOpt's [EfficientFrontier.min_volatility](https://pyportfolioopt.readthedocs.io/en/latest/MeanVariance.html#pypfopt.efficient_frontier.EfficientFrontier.min_volatility){:target="_blank"}
- library | Referenced against PyPortfolioOpt's [objective_functions.L2_reg](https://pyportfolioopt.readthedocs.io/en/latest/MeanVariance.html#pypfopt.objective_functions.L2_reg){:target="_blank"}
- library | Referenced against skfolio's [MeanRisk](https://skfolio.org/generated/skfolio.optimization.MeanRisk.html){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The frequency of the returns the covariance matrix is estimated from. Options
are: "daily" (daily returns), "weekly" (weekly returns), "monthly" (monthly returns), "quarterly"
(quarterly returns), "yearly" (yearly returns). Defaults to "daily".
- <u>covariance (str, optional):</u> The estimator of the covariance matrix. The shrinkage and denoised
estimators stabilize the weights when there are many assets compared to the number of periods.
Options are: "sample" (the sample covariance, ddof=1), "ledoit_wolf" (shrunk towards the scaled
identity, Ledoit and Wolf, 2004), "ledoit_wolf_constant_correlation" (shrunk towards the average
correlation, Ledoit and Wolf, 2004), "ledoit_wolf_single_factor" (shrunk towards the covariance that
the benchmark as a single factor implies, Ledoit and Wolf, 2003), "oas" (Oracle Approximating
Shrinkage, Chen et al., 2010), "shrunk" (a fixed 10% towards the scaled identity), "semicovariance"
(the co-movement below a zero return, Estrada, 2008), "exponential" (exponentially weighted, recent
periods weigh most, RiskMetrics), "denoised" (the eigenvalues of the correlation matrix that random
returns could produce averaged, Laloux et al., 2000), "denoised_spectral" (those eigenvalues set to
zero), "denoised_shrink" (the noise correlations shrunk towards their diagonal, López de Prado,
2020), "gerber" (co-movements beyond half a standard deviation, Gerber et al., 2022), "factor" (the
covariance of the Fama and French five factor model with OLS loadings, Fama and French, 1993),
"minimum_covariance_determinant" (the reweighted covariance of the half of the periods with the
smallest covariance determinant, robust to outliers, Rousseeuw and Van Driessen, 1999), "jlogo" (the
sparse inverse covariance on the TMFG planar graph of the correlations, Barfuss et al., 2016),
"geodesic" (10% towards the scaled identity along the geodesic of the positive definite matrices,
Bhatia, 2007), "regime_adjusted_ew" (exponentially weighted with a half-life of 40 periods, rescaled
by the recent realized against predicted risk, Paleologo, 2025), "nercome" (eigenvectors from one
part of the periods and the variances along them from the other, averaged over random splits, Lam,
2016), "ccc_garch" (the next-period covariance of GARCH(1, 1) volatilities with constant
correlations, Bollerslev, 1990), "mm" (the robust MM-estimator, Maronna et al., 2019), "rocke"
(Rocke's robust S-estimator, Maronna et al., 2019). Defaults to "sample".
- <u>covariance_span (int, optional):</u> The span in periods of the exponentially weighted covariance; the
weight of a period halves after about span / 2.9 periods. Defaults to 180.
- <u>minimum_weight (float &#124; dict[str, float], optional):</u> The lowest weight of
every asset, or per asset, e.g. {"AAPL": 0.05} (the others keep 0); a
negative value allows short positions. Defaults to 0.
- <u>maximum_weight (float &#124; dict[str, float], optional):</u> The highest weight of
every asset, or per asset, e.g. {"AAPL": 0.3} (the others keep 1).
Defaults to 1.
- <u>sector_bounds (dict[str, tuple[float, float]] &#124; None, optional):</u> The minimum
and maximum total weight per sector, e.g. {"Technology": (0, 0.4)}, with
the sector of each asset from its company profile. Defaults to None.
- <u>country_bounds (dict[str, tuple[float, float]] &#124; None, optional):</u> The minimum
and maximum total weight per country, named in full or by its two-letter
code, e.g. {"United States": (0, 0.6)}, with the country of each asset
from its company profile. Defaults to None.
- <u>net_exposure (float, optional):</u> The sum of the weights: 1 for a fully invested
portfolio, 0 for a market neutral one (which needs a negative
minimum_weight). At 0 the portfolio with the lowest variance holds nothing,
so all weights are 0. The rest, 1 minus the net exposure, is a Cash row at
the risk free rate (negative when borrowed above one), which the Portfolio's
Expected Return and Sharpe Ratio include. Defaults to 1.
- <u>gross_exposure (float &#124; None, optional):</u> The highest sum of the absolute
weights, which limits the leverage of a long-short portfolio, e.g. 1.6 for
a 130/30 portfolio. Defaults to None, no limit.
- <u>current_weights (dict[str, float] &#124; None, optional):</u> The weights held now,
e.g. {"AAPL": 0.5, "MSFT": 0.5} (an asset left out is not held), which
the turnover is measured from; they add a Turnover column, $$\vert w_{i} - w_{0,i} \vert$$
per asset and its sum for the portfolio. Defaults to None, which uses
the latest weights of the Portfolio the Toolkit came from when a maximum
turnover or transaction cost needs them.
- <u>maximum_turnover (float &#124; None, optional):</u> The highest turnover
$$\sum \vert w_{i} - w_{0,i} \vert$$ from the current weights, e.g. 0.2 to trade at most 10%
of the portfolio each way. Defaults to None, no limit.
- <u>l2_regularization (float, optional):</u> The weight $$\gamma$$ of the L2 penalty $$\gamma$$ w'w on
the weights, in annualized variance units, which pulls the portfolio
towards equal weights and spreads it over more assets, e.g. 0.05. It is
PyPortfolioOpt's $$L_{2,\text{reg}}$$ gamma on an annualized covariance matrix; on a
covariance matrix per period, that gamma is $$\gamma$$ divided by the number of
periods in a year. Defaults to 0, no penalty.
- <u>include_benchmark (bool, optional):</u> Whether to include the benchmark as an
asset. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per asset and for the portfolio, the Weight, Expected Return,
Volatility, Sharpe Ratio and Risk Contribution (the share of the portfolio's
volatility). Returns and volatilities are annualized.

**Notes:**

- Only the periods in which every asset has a return are used, so an asset with a
short history shortens the sample of all assets.
- The expected returns are the historical average returns, annualized; the Sharpe
ratios use the average risk free rate over the same periods.
- Every optimizer with weight bounds takes the same constraints. Sector and
country bounds limit the total weight of the assets in a group (an asset
without a sector or country, such as the benchmark, is in none). A gross
exposure limit is linearized with one extra variable $$t_{i} \geq \vert w_{i} \vert$$ per asset
($$t_{i} \geq w_{i} , t_{i} \geq - w_{i} , \sum t_{i}$$ ≤ the limit), so the solution stays exact. A
maximum turnover from the current weights is linearized the same way, with one
variable $$d_{i} \geq \vert w_{i} - w_{0,i} \vert$$ per asset and $$\sum d_{i}$$ ≤ the limit (Lobo, Fazel and
Boyd, 2007). A combination of constraints no portfolio can meet raises an
error before the optimization runs.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "JNJ", "XOM"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.portfolio.get_minimum_variance_weights(
    sector_bounds={"Healthcare": (0, 0.4)}, maximum_weight={"XOM": 0.15}
)
```

Which returns:

|           |   Weight |   Expected Return |   Volatility |   Sharpe Ratio |   Risk Contribution |
|:----------|---------:|------------------:|-------------:|---------------:|--------------------:|
| AAPL      |   0.1225 |            0.1932 |       0.2786 |         0.5725 |              0.1683 |
| MSFT      |   0.3275 |            0.2017 |       0.2571 |         0.6534 |              0.4499 |
| JNJ       |   0.4    |            0.0987 |       0.1673 |         0.3884 |              0.2624 |
| XOM       |   0.15   |            0.2911 |       0.2702 |         0.9524 |              0.1194 |
| Portfolio |   1      |            0.1729 |       0.1463 |         0.9513 |              1      |

---

## get_maximum_sharpe_weights
Calculate the weights of the maximum Sharpe ratio portfolio.

It is the fully invested portfolio with the highest expected return per unit of volatility above the risk free rate. It is the tangency portfolio, where a line from the risk free rate touches the efficient frontier.

The weights maximize $$(w' \mu - r_{f}) / \sqrt{w' \Sigma w}$$ subject to the weights summing to one and lying between the minimum and maximum weight, with $$\mu$$ the annualized expected returns, $$\Sigma$$ the annualized covariance matrix and $$r_{f}$$ the risk free rate.

An L2 regularization $$\gamma$$ adds the penalty $$\gamma$$ w'w to the variance in the denominator, $$(w' \mu - r_{f}) / \sqrt{w' (\Sigma + \gamma I) w}$$, which moves the portfolio towards equal weights.

**Also known as:** tangency portfolio, optimal risky portfolio, max Sharpe.

**References:**

- paper | Tobin, J. (1958). "Liquidity Preference as Behavior Towards Risk." The Review of Economic Studies, 25(2), 65-86.
- paper | Sharpe, W.F. (1966). "Mutual Fund Performance." The Journal of Business, 39(1), 119-138.
- paper | DeMiguel, V., Garlappi, L., Nogales, F. J. and Uppal, R. (2009). "A Generalized Approach to Portfolio Optimization: Improving Performance by Constraining Portfolio Norms." Management Science, 55(5), 798-812.
- paper | Hoerl, A. E. and Kennard, R. W. (1970). "Ridge Regression: Biased Estimation for Nonorthogonal Problems." Technometrics, 12(1), 55-67.
- library | Referenced against PyPortfolioOpt's [EfficientFrontier.max_sharpe](https://pyportfolioopt.readthedocs.io/en/latest/MeanVariance.html#pypfopt.efficient_frontier.EfficientFrontier.max_sharpe){:target="_blank"}
- library | Referenced against PyPortfolioOpt's [objective_functions.L2_reg](https://pyportfolioopt.readthedocs.io/en/latest/MeanVariance.html#pypfopt.objective_functions.L2_reg){:target="_blank"}
- library | Referenced against skfolio's [MeanRisk](https://skfolio.org/generated/skfolio.optimization.MeanRisk.html){:target="_blank"} (with transaction costs)

**Args:**

- <u>period (str, optional):</u> The frequency of the returns. Options are: "daily" (daily returns), "weekly"
(weekly returns), "monthly" (monthly returns), "quarterly" (quarterly returns), "yearly" (yearly
returns). Defaults to "daily".
- <u>covariance (str, optional):</u> The estimator of the covariance matrix. The shrinkage and denoised
estimators stabilize the weights when there are many assets compared to the number of periods.
Options are: "sample" (the sample covariance, ddof=1), "ledoit_wolf" (shrunk towards the scaled
identity, Ledoit and Wolf, 2004), "ledoit_wolf_constant_correlation" (shrunk towards the average
correlation, Ledoit and Wolf, 2004), "ledoit_wolf_single_factor" (shrunk towards the covariance that
the benchmark as a single factor implies, Ledoit and Wolf, 2003), "oas" (Oracle Approximating
Shrinkage, Chen et al., 2010), "shrunk" (a fixed 10% towards the scaled identity), "semicovariance"
(the co-movement below a zero return, Estrada, 2008), "exponential" (exponentially weighted, recent
periods weigh most, RiskMetrics), "denoised" (the eigenvalues of the correlation matrix that random
returns could produce averaged, Laloux et al., 2000), "denoised_spectral" (those eigenvalues set to
zero), "denoised_shrink" (the noise correlations shrunk towards their diagonal, López de Prado,
2020), "gerber" (co-movements beyond half a standard deviation, Gerber et al., 2022), "factor" (the
covariance of the Fama and French five factor model with OLS loadings, Fama and French, 1993),
"minimum_covariance_determinant" (the reweighted covariance of the half of the periods with the
smallest covariance determinant, robust to outliers, Rousseeuw and Van Driessen, 1999), "jlogo" (the
sparse inverse covariance on the TMFG planar graph of the correlations, Barfuss et al., 2016),
"geodesic" (10% towards the scaled identity along the geodesic of the positive definite matrices,
Bhatia, 2007), "regime_adjusted_ew" (exponentially weighted with a half-life of 40 periods, rescaled
by the recent realized against predicted risk, Paleologo, 2025), "nercome" (eigenvectors from one
part of the periods and the variances along them from the other, averaged over random splits, Lam,
2016), "ccc_garch" (the next-period covariance of GARCH(1, 1) volatilities with constant
correlations, Bollerslev, 1990), "mm" (the robust MM-estimator, Maronna et al., 2019), "rocke"
(Rocke's robust S-estimator, Maronna et al., 2019). Defaults to "sample".
- <u>covariance_span (int, optional):</u> The span in periods of the exponentially weighted covariance; the
weight of a period halves after about span / 2.9 periods. Defaults to 180.
- <u>expected_returns (str, optional):</u> The estimator of the expected returns. Options are: "mean" (the
historical average), "geometric" (the compounded average), "exponential" (the exponentially weighted
average, recent periods weigh most), "exponential_geometric" (that average compounded over a year),
"capm" (the returns the Capital Asset Pricing Model implies from each asset's beta to the benchmark,
Sharpe, 1964), "bayes_stein" (the averages shrunk towards that of the minimum variance portfolio,
Jorion, 1986), "james_stein" (the averages shrunk towards their grand mean, James and Stein, 1961),
"bodnar_okhrin_parolya" (the averages and their grand mean combined with optimal weights, Bodnar,
Okhrin and Parolya, 2019). Defaults to "mean".
- <u>expected_returns_span (int, optional):</u> The span in periods of the exponentially weighted expected
returns. Defaults to 180.
- <u>minimum_weight (float &#124; dict[str, float], optional):</u> The lowest weight of
every asset, or per asset, e.g. {"AAPL": 0.05} (the others keep 0); a
negative value allows short positions. Defaults to 0.
- <u>maximum_weight (float &#124; dict[str, float], optional):</u> The highest weight of
every asset, or per asset, e.g. {"AAPL": 0.3} (the others keep 1).
Defaults to 1.
- <u>sector_bounds (dict[str, tuple[float, float]] &#124; None, optional):</u> The minimum
and maximum total weight per sector, e.g. {"Technology": (0, 0.4)}, with
the sector of each asset from its company profile. Defaults to None.
- <u>country_bounds (dict[str, tuple[float, float]] &#124; None, optional):</u> The minimum
and maximum total weight per country, named in full or by its two-letter
code, e.g. {"United States": (0, 0.6)}, with the country of each asset
from its company profile. Defaults to None.
- <u>net_exposure (float, optional):</u> The sum of the weights: 1 for a fully invested
portfolio, 0 for a market neutral one (which needs a negative
minimum_weight). The rest, 1 minus the net exposure, is a Cash row at the
risk free rate (negative when borrowed above one), which the Portfolio's
Expected Return and Sharpe Ratio include. Defaults to 1.
- <u>gross_exposure (float &#124; None, optional):</u> The highest sum of the absolute
weights, which limits the leverage of a long-short portfolio, e.g. 1.6 for
a 130/30 portfolio. Defaults to None, no limit.
- <u>current_weights (dict[str, float] &#124; None, optional):</u> The weights held now,
e.g. {"AAPL": 0.5, "MSFT": 0.5} (an asset left out is not held), which
the turnover is measured from; they add a Turnover column, $$\vert w_{i} - w_{0,i} \vert$$
per asset and its sum for the portfolio. Defaults to None, which uses
the latest weights of the Portfolio the Toolkit came from when a maximum
turnover or transaction cost needs them.
- <u>maximum_turnover (float &#124; None, optional):</u> The highest turnover
$$\sum \vert w_{i} - w_{0,i} \vert$$ from the current weights, e.g. 0.2 to trade at most 10%
of the portfolio each way. Defaults to None, no limit.
- <u>transaction_cost (float, optional):</u> The cost per unit of weight traded
from the current weights, e.g. 0.001 for 10 basis points, subtracted once
from the portfolio's annualized expected return. It adds a Transaction
Cost column, the cost times $$\vert w_{i} - w_{0,i} \vert$$ per asset and their sum for the
portfolio, whose Expected Return and Sharpe Ratio are after it. Defaults
to 0.
- <u>l2_regularization (float, optional):</u> The weight $$\gamma$$ of the L2 penalty $$\gamma$$ w'w on
the weights, in annualized variance units, which pulls the portfolio
towards equal weights and spreads it over more assets, e.g. 0.05. It is
PyPortfolioOpt's $$L_{2,\text{reg}}$$ gamma on an annualized covariance matrix; on a
covariance matrix per period, that gamma is $$\gamma$$ divided by the number of
periods in a year. Defaults to 0, no penalty.
- <u>include_benchmark (bool, optional):</u> Whether to include the benchmark as an
asset. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per asset and for the portfolio, the Weight, Expected Return,
Volatility, Sharpe Ratio and Risk Contribution. Returns and volatilities are
annualized.

**Notes:**

- The expected returns are the noisiest input of the optimization, so with the
historical averages the weights tend to concentrate in the assets that happened
to do best. A maximum weight, the CAPM or shrunk (Bayes-Stein, James-Stein,
Bodnar-Okhrin-Parolya) expected returns or the Black-Litterman returns temper
that.
- A transaction cost lowers the expected return of the portfolio by the cost
times the turnover from the current weights, so the optimizer only trades when
the gain in Sharpe ratio pays for it. The cost
is taken once from an annualized return, which spreads it over a year of
holding the portfolio. The Portfolio row shows the expected return and Sharpe
ratio after the cost, the ones the optimizer maximized.

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
Calculate the weights of a mean-variance efficient portfolio.

With a target return, it is the portfolio with the lowest volatility that expects that return. With a target volatility $$\sigma^{*}$$, it is the portfolio with the highest expected return whose annualized volatility is at most $$\sigma^{*}$$: $$\max w' \mu$$ subject to $$w' \Sigma w \leq \sigma^{*2}$$. Without either, it is the portfolio that maximizes the investor's utility, the expected return minus half the risk aversion times the variance: $$w' \mu - (\lambda / 2) w' \Sigma w$$.

A risk aversion of 2 to 4 is typical; 2.5 is the value commonly used for the market as a whole.

An L2 regularization $$\gamma$$ adds the penalty $$\gamma$$ w'w, which moves the portfolio towards equal weights: with a target return the weights minimize $$w' (\Sigma + \gamma I) w$$, the utility becomes $$w' \mu - (\lambda / 2) w' \Sigma w - \gamma$$ w'w and with a target volatility the weights maximize $$w' \mu - \gamma$$ w'w, with the volatility limit still on $$w' \Sigma w$$.

**Also known as:** Markowitz portfolio, efficient portfolio, quadratic utility portfolio.

**References:**

- paper | Markowitz, H. (1952). "Portfolio Selection." The Journal of Finance, 7(1), 77-91.
- paper | Merton, R. C. (1972). "An Analytic Derivation of the Efficient Portfolio Frontier." Journal of Financial and Quantitative Analysis, 7(4), 1851-1872.
- paper | DeMiguel, V., Garlappi, L., Nogales, F. J. and Uppal, R. (2009). "A Generalized Approach to Portfolio Optimization: Improving Performance by Constraining Portfolio Norms." Management Science, 55(5), 798-812.
- paper | Hoerl, A. E. and Kennard, R. W. (1970). "Ridge Regression: Biased Estimation for Nonorthogonal Problems." Technometrics, 12(1), 55-67.
- library | Referenced against PyPortfolioOpt's [EfficientFrontier.efficient_return](https://pyportfolioopt.readthedocs.io/en/latest/MeanVariance.html#pypfopt.efficient_frontier.EfficientFrontier.efficient_return){:target="_blank"} (target return)
- library | Referenced against PyPortfolioOpt's [EfficientFrontier.efficient_risk](https://pyportfolioopt.readthedocs.io/en/latest/MeanVariance.html#pypfopt.efficient_frontier.EfficientFrontier.efficient_risk){:target="_blank"} (target volatility)
- library | Referenced against PyPortfolioOpt's [EfficientFrontier.max_quadratic_utility](https://pyportfolioopt.readthedocs.io/en/latest/MeanVariance.html#pypfopt.efficient_frontier.EfficientFrontier.max_quadratic_utility){:target="_blank"} (risk aversion)
- library | Referenced against PyPortfolioOpt's [objective_functions.L2_reg](https://pyportfolioopt.readthedocs.io/en/latest/MeanVariance.html#pypfopt.objective_functions.L2_reg){:target="_blank"}

**Args:**

- <u>target_return (float &#124; None, optional):</u> The annualized return the portfolio must
expect, e.g. 0.12 for 12%, with the cash of a net exposure other than one
at the risk free rate. Defaults to None, which uses the target
volatility or the risk aversion.
- <u>risk_aversion (float, optional):</u> The investor's risk aversion $$\lambda$$; higher values
give less risky portfolios. Not used with a target return or target
volatility. Defaults to 2.5.
- <u>period (str, optional):</u> The frequency of the returns. Options are: "daily" (daily returns), "weekly"
(weekly returns), "monthly" (monthly returns), "quarterly" (quarterly returns), "yearly" (yearly
returns). Defaults to "daily".
- <u>covariance (str, optional):</u> The estimator of the covariance matrix. The shrinkage and denoised
estimators stabilize the weights when there are many assets compared to the number of periods.
Options are: "sample" (the sample covariance, ddof=1), "ledoit_wolf" (shrunk towards the scaled
identity, Ledoit and Wolf, 2004), "ledoit_wolf_constant_correlation" (shrunk towards the average
correlation, Ledoit and Wolf, 2004), "ledoit_wolf_single_factor" (shrunk towards the covariance that
the benchmark as a single factor implies, Ledoit and Wolf, 2003), "oas" (Oracle Approximating
Shrinkage, Chen et al., 2010), "shrunk" (a fixed 10% towards the scaled identity), "semicovariance"
(the co-movement below a zero return, Estrada, 2008), "exponential" (exponentially weighted, recent
periods weigh most, RiskMetrics), "denoised" (the eigenvalues of the correlation matrix that random
returns could produce averaged, Laloux et al., 2000), "denoised_spectral" (those eigenvalues set to
zero), "denoised_shrink" (the noise correlations shrunk towards their diagonal, López de Prado,
2020), "gerber" (co-movements beyond half a standard deviation, Gerber et al., 2022), "factor" (the
covariance of the Fama and French five factor model with OLS loadings, Fama and French, 1993),
"minimum_covariance_determinant" (the reweighted covariance of the half of the periods with the
smallest covariance determinant, robust to outliers, Rousseeuw and Van Driessen, 1999), "jlogo" (the
sparse inverse covariance on the TMFG planar graph of the correlations, Barfuss et al., 2016),
"geodesic" (10% towards the scaled identity along the geodesic of the positive definite matrices,
Bhatia, 2007), "regime_adjusted_ew" (exponentially weighted with a half-life of 40 periods, rescaled
by the recent realized against predicted risk, Paleologo, 2025), "nercome" (eigenvectors from one
part of the periods and the variances along them from the other, averaged over random splits, Lam,
2016), "ccc_garch" (the next-period covariance of GARCH(1, 1) volatilities with constant
correlations, Bollerslev, 1990), "mm" (the robust MM-estimator, Maronna et al., 2019), "rocke"
(Rocke's robust S-estimator, Maronna et al., 2019). Defaults to "sample".
- <u>covariance_span (int, optional):</u> The span in periods of the exponentially weighted covariance; the
weight of a period halves after about span / 2.9 periods. Defaults to 180.
- <u>expected_returns (str, optional):</u> The estimator of the expected returns. Options are: "mean" (the
historical average), "geometric" (the compounded average), "exponential" (the exponentially weighted
average, recent periods weigh most), "exponential_geometric" (that average compounded over a year),
"capm" (the returns the Capital Asset Pricing Model implies from each asset's beta to the benchmark,
Sharpe, 1964), "bayes_stein" (the averages shrunk towards that of the minimum variance portfolio,
Jorion, 1986), "james_stein" (the averages shrunk towards their grand mean, James and Stein, 1961),
"bodnar_okhrin_parolya" (the averages and their grand mean combined with optimal weights, Bodnar,
Okhrin and Parolya, 2019). Defaults to "mean".
- <u>expected_returns_span (int, optional):</u> The span in periods of the exponentially weighted expected
returns. Defaults to 180.
- <u>minimum_weight (float &#124; dict[str, float], optional):</u> The lowest weight of
every asset, or per asset, e.g. {"AAPL": 0.05} (the others keep 0); a
negative value allows short positions. Defaults to 0.
- <u>maximum_weight (float &#124; dict[str, float], optional):</u> The highest weight of
every asset, or per asset, e.g. {"AAPL": 0.3} (the others keep 1).
Defaults to 1.
- <u>sector_bounds (dict[str, tuple[float, float]] &#124; None, optional):</u> The minimum
and maximum total weight per sector, e.g. {"Technology": (0, 0.4)}, with
the sector of each asset from its company profile. Defaults to None.
- <u>country_bounds (dict[str, tuple[float, float]] &#124; None, optional):</u> The minimum
and maximum total weight per country, named in full or by its two-letter
code, e.g. {"United States": (0, 0.6)}, with the country of each asset
from its company profile. Defaults to None.
- <u>net_exposure (float, optional):</u> The sum of the weights: 1 for a fully invested
portfolio, 0 for a market neutral one (which needs a negative
minimum_weight). The rest, 1 minus the net exposure, is a Cash row at the
risk free rate (negative when borrowed above one), which the Portfolio's
Expected Return and Sharpe Ratio include. Defaults to 1.
- <u>gross_exposure (float &#124; None, optional):</u> The highest sum of the absolute
weights, which limits the leverage of a long-short portfolio, e.g. 1.6 for
a 130/30 portfolio. Defaults to None, no limit.
- <u>current_weights (dict[str, float] &#124; None, optional):</u> The weights held now,
e.g. {"AAPL": 0.5, "MSFT": 0.5} (an asset left out is not held), which
the turnover is measured from; they add a Turnover column, $$\vert w_{i} - w_{0,i} \vert$$
per asset and its sum for the portfolio. Defaults to None, which uses
the latest weights of the Portfolio the Toolkit came from when a maximum
turnover or transaction cost needs them.
- <u>maximum_turnover (float &#124; None, optional):</u> The highest turnover
$$\sum \vert w_{i} - w_{0,i} \vert$$ from the current weights, e.g. 0.2 to trade at most 10%
of the portfolio each way. Defaults to None, no limit.
- <u>transaction_cost (float, optional):</u> The cost per unit of weight traded
from the current weights, e.g. 0.001 for 10 basis points, subtracted once
from the portfolio's annualized expected return. It adds a Transaction
Cost column, the cost times $$\vert w_{i} - w_{0,i} \vert$$ per asset and their sum for the
portfolio, whose Expected Return and Sharpe Ratio are after it. Defaults
to 0.
- <u>target_volatility (float &#124; None, optional):</u> The highest annualized volatility
of the portfolio (the volatility per period times the square root of the
number of periods in a year), e.g. 0.15 for 15%. Cannot be combined with
a target return. Defaults to None, which uses the target return or the
risk aversion.
- <u>l2_regularization (float, optional):</u> The weight $$\gamma$$ of the L2 penalty $$\gamma$$ w'w on
the weights, in annualized variance units, which pulls the portfolio
towards equal weights and spreads it over more assets, e.g. 0.05. It is
PyPortfolioOpt's $$L_{2,\text{reg}}$$ gamma on an annualized covariance matrix; on a
covariance matrix per period, that gamma is $$\gamma$$ divided by the number of
periods in a year. Defaults to 0, no penalty.
- <u>include_benchmark (bool, optional):</u> Whether to include the benchmark as an
asset. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per asset and for the portfolio, the Weight, Expected Return,
Volatility, Sharpe Ratio and Risk Contribution.

**Notes:**

- A target return outside what the assets can reach within the constraints
raises an error that states the reachable range.
- A target volatility below that of the minimum variance portfolio within the
constraints raises an error that states that volatility. Above the volatility
of the highest return portfolio the target does not bind, and that portfolio
is returned.
- A target return and a target volatility together are refused: on the efficient
frontier the one fixes the other.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "JNJ", "XOM"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.portfolio.get_mean_variance_weights(
    target_return=0.3, minimum_weight=-0.5, gross_exposure=1.6
)
```

Which returns:

|           |   Weight |   Expected Return |   Volatility |   Sharpe Ratio |   Risk Contribution |
|:----------|---------:|------------------:|-------------:|---------------:|--------------------:|
| AAPL      |   0.0057 |            0.1932 |       0.2786 |         0.5725 |              0.0027 |
| MSFT      |   0.4234 |            0.2017 |       0.2571 |         0.6534 |              0.2149 |
| JNJ       |  -0.2459 |            0.0987 |       0.1673 |         0.3884 |              0.0022 |
| XOM       |   0.8168 |            0.2911 |       0.2702 |         0.9524 |              0.7803 |
| Portfolio |   1      |            0.3    |       0.2521 |         1.0561 |              1      |

---

## get_efficient_frontier
Calculate the efficient frontier.

These are the portfolios with the lowest volatility for each level of expected return, from the minimum variance portfolio up to the highest return the weight bounds allow. Every portfolio below the frontier takes more risk than needed for its return.

An L2 regularization $$\gamma$$ minimizes $$w' (\Sigma + \gamma I) w$$ for each target return, which moves every portfolio towards equal weights; the volatility shown stays $$\sqrt{w' \Sigma w}$$.

**Also known as:** Markowitz frontier, mean-variance frontier, risk-return frontier.

**References:**

- paper | Markowitz, H. (1952). "Portfolio Selection." The Journal of Finance, 7(1), 77-91.
- paper | DeMiguel, V., Garlappi, L., Nogales, F. J. and Uppal, R. (2009). "A Generalized Approach to Portfolio Optimization: Improving Performance by Constraining Portfolio Norms." Management Science, 55(5), 798-812.
- paper | Hoerl, A. E. and Kennard, R. W. (1970). "Ridge Regression: Biased Estimation for Nonorthogonal Problems." Technometrics, 12(1), 55-67.
- library | Referenced against PyPortfolioOpt's [objective_functions.L2_reg](https://pyportfolioopt.readthedocs.io/en/latest/MeanVariance.html#pypfopt.objective_functions.L2_reg){:target="_blank"}

**Args:**

- <u>points (int, optional):</u> The number of portfolios on the frontier. Defaults to 20.
- <u>period (str, optional):</u> The frequency of the returns. Options are: "daily" (daily returns), "weekly"
(weekly returns), "monthly" (monthly returns), "quarterly" (quarterly returns), "yearly" (yearly
returns). Defaults to "daily".
- <u>covariance (str, optional):</u> The estimator of the covariance matrix. The shrinkage and denoised
estimators stabilize the weights when there are many assets compared to the number of periods.
Options are: "sample" (the sample covariance, ddof=1), "ledoit_wolf" (shrunk towards the scaled
identity, Ledoit and Wolf, 2004), "ledoit_wolf_constant_correlation" (shrunk towards the average
correlation, Ledoit and Wolf, 2004), "ledoit_wolf_single_factor" (shrunk towards the covariance that
the benchmark as a single factor implies, Ledoit and Wolf, 2003), "oas" (Oracle Approximating
Shrinkage, Chen et al., 2010), "shrunk" (a fixed 10% towards the scaled identity), "semicovariance"
(the co-movement below a zero return, Estrada, 2008), "exponential" (exponentially weighted, recent
periods weigh most, RiskMetrics), "denoised" (the eigenvalues of the correlation matrix that random
returns could produce averaged, Laloux et al., 2000), "denoised_spectral" (those eigenvalues set to
zero), "denoised_shrink" (the noise correlations shrunk towards their diagonal, López de Prado,
2020), "gerber" (co-movements beyond half a standard deviation, Gerber et al., 2022), "factor" (the
covariance of the Fama and French five factor model with OLS loadings, Fama and French, 1993),
"minimum_covariance_determinant" (the reweighted covariance of the half of the periods with the
smallest covariance determinant, robust to outliers, Rousseeuw and Van Driessen, 1999), "jlogo" (the
sparse inverse covariance on the TMFG planar graph of the correlations, Barfuss et al., 2016),
"geodesic" (10% towards the scaled identity along the geodesic of the positive definite matrices,
Bhatia, 2007), "regime_adjusted_ew" (exponentially weighted with a half-life of 40 periods, rescaled
by the recent realized against predicted risk, Paleologo, 2025), "nercome" (eigenvectors from one
part of the periods and the variances along them from the other, averaged over random splits, Lam,
2016), "ccc_garch" (the next-period covariance of GARCH(1, 1) volatilities with constant
correlations, Bollerslev, 1990), "mm" (the robust MM-estimator, Maronna et al., 2019), "rocke"
(Rocke's robust S-estimator, Maronna et al., 2019). Defaults to "sample".
- <u>covariance_span (int, optional):</u> The span in periods of the exponentially weighted covariance; the
weight of a period halves after about span / 2.9 periods. Defaults to 180.
- <u>expected_returns (str, optional):</u> The estimator of the expected returns. Options are: "mean" (the
historical average), "geometric" (the compounded average), "exponential" (the exponentially weighted
average, recent periods weigh most), "exponential_geometric" (that average compounded over a year),
"capm" (the returns the Capital Asset Pricing Model implies from each asset's beta to the benchmark,
Sharpe, 1964), "bayes_stein" (the averages shrunk towards that of the minimum variance portfolio,
Jorion, 1986), "james_stein" (the averages shrunk towards their grand mean, James and Stein, 1961),
"bodnar_okhrin_parolya" (the averages and their grand mean combined with optimal weights, Bodnar,
Okhrin and Parolya, 2019). Defaults to "mean".
- <u>expected_returns_span (int, optional):</u> The span in periods of the exponentially weighted expected
returns. Defaults to 180.
- <u>minimum_weight (float &#124; dict[str, float], optional):</u> The lowest weight of
every asset, or per asset, e.g. {"AAPL": 0.05} (the others keep 0); a
negative value allows short positions. Defaults to 0.
- <u>maximum_weight (float &#124; dict[str, float], optional):</u> The highest weight of
every asset, or per asset, e.g. {"AAPL": 0.3} (the others keep 1).
Defaults to 1.
- <u>sector_bounds (dict[str, tuple[float, float]] &#124; None, optional):</u> The minimum
and maximum total weight per sector, e.g. {"Technology": (0, 0.4)}, with
the sector of each asset from its company profile. Defaults to None.
- <u>country_bounds (dict[str, tuple[float, float]] &#124; None, optional):</u> The minimum
and maximum total weight per country, named in full or by its two-letter
code, e.g. {"United States": (0, 0.6)}, with the country of each asset
from its company profile. Defaults to None.
- <u>net_exposure (float, optional):</u> The sum of the weights: 1 for a fully invested
portfolio, 0 for a market neutral one (which needs a negative
minimum_weight). At 0 the portfolio with the lowest variance holds nothing,
so the first portfolio of the frontier has all weights 0 and no Sharpe ratio
(NaN). The rest, 1 minus the net exposure, earns the risk free rate
(borrowed at it above one) in the Expected Return and Sharpe Ratio. Defaults
to 1.
- <u>gross_exposure (float &#124; None, optional):</u> The highest sum of the absolute
weights, which limits the leverage of a long-short portfolio, e.g. 1.6 for
a 130/30 portfolio. Defaults to None, no limit.
- <u>current_weights (dict[str, float] &#124; None, optional):</u> The weights held now,
e.g. {"AAPL": 0.5, "MSFT": 0.5} (an asset left out is not held), which
the turnover is measured from; they add a Turnover column, $$\vert w_{i} - w_{0,i} \vert$$
per asset and its sum for the portfolio. Defaults to None, which uses
the latest weights of the Portfolio the Toolkit came from when a maximum
turnover or transaction cost needs them.
- <u>maximum_turnover (float &#124; None, optional):</u> The highest turnover
$$\sum \vert w_{i} - w_{0,i} \vert$$ from the current weights, e.g. 0.2 to trade at most 10%
of the portfolio each way. Defaults to None, no limit.
- <u>l2_regularization (float, optional):</u> The weight $$\gamma$$ of the L2 penalty $$\gamma$$ w'w on
the weights, in annualized variance units, which pulls the portfolio
towards equal weights and spreads it over more assets, e.g. 0.05. It is
PyPortfolioOpt's $$L_{2,\text{reg}}$$ gamma on an annualized covariance matrix; on a
covariance matrix per period, that gamma is $$\gamma$$ divided by the number of
periods in a year. Defaults to 0, no penalty.
- <u>include_benchmark (bool, optional):</u> Whether to include the benchmark as an
asset. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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
Calculate the risk parity weights: the portfolio in which every asset contributes the same share of the volatility, or the share set by a risk budget.

Volatile assets get smaller weights, and correlated assets share their risk budget, so no single asset dominates the portfolio's risk.

The weights solve $$w_{i} (\Sigma w)_{i} / \sigma_{p} = b_{i} \sigma_{p}$$ for every asset, found by minimizing the convex function $$\tfrac{1}{2} w' \Sigma w - \sum b_{i} \ln (w_{i})$$ and scaling the result to sum to one.

With another risk measure $$\rho$$ of the historical returns, every asset contributes its share of that measure instead, $$w_{i} \partial \rho / \partial w_{i} = b_{i} \rho (w)$$: the solution of $$\min \rho (y)$$ subject to $$\sum b_{i} \ln (y_{i}) \geq 0$$ and $$y \geq 0$$, scaled to $$w = y / \sum y$$ (Roncalli, 2013). The measures that are linear programmes, and the Gini mean difference and Tail Gini measures, are solved exactly with cutting planes (Kelley, 1960): the concave $$\sum b_{i} \ln (y_{i})$$ lies below each of its tangents, which are added as linear constraints where the linear programme's solution needs them. The semideviation and the Ulcer Index are minimized with SLSQP as $$\rho (y) - \sum b_{i} \ln (y_{i})$$. The measures are those of get_mean_risk_weights plus the Conditional Value at Risk (Rockafellar and Uryasev, 2000), and the Conditional Drawdown at Risk of the uncompounded cumulative return (Chekhlov, Uryasev and Zabarankin, 2005), without the worst realization and the range, whose contributions come from a single period.

**Also known as:** equal risk contribution, ERC, risk budgeting.

**References:**

- paper | Maillard, S., Roncalli, T. and Teïletche, J. (2010). "The Properties of Equally Weighted Risk Contribution Portfolios." The Journal of Portfolio Management, 36(4), 60-70.
- paper | Spinu, F. (2013). "An Algorithm for Computing Risk Parity Weights." SSRN Working Paper.
- paper | Richard, J.-C. and Roncalli, T. (2019). "Constrained Risk Budgeting Portfolios: Theory, Algorithms, Applications & Puzzles." arXiv:1902.05710.
- paper | Roncalli, T. (2013). "Introduction to Risk Parity and Budgeting." Chapman & Hall/CRC, Boca Raton.
- paper | Rockafellar, R. T. and Uryasev, S. (2000). "Optimization of Conditional Value-at-Risk." Journal of Risk, 2(3), 21-41.
- paper | Chekhlov, A., Uryasev, S. and Zabarankin, M. (2005). "Drawdown Measure in Portfolio Optimization." International Journal of Theoretical and Applied Finance, 8(1), 13-58.
- paper | Kelley, J. E. (1960). "The Cutting-Plane Method for Solving Convex Programs." Journal of the Society for Industrial and Applied Mathematics, 8(4), 703-712.
- library | Referenced against skfolio's [RiskBudgeting](https://skfolio.org/generated/skfolio.optimization.RiskBudgeting.html){:target="_blank"} (volatility)
- library | Referenced against skfolio's [RiskBudgeting](https://skfolio.org/generated/skfolio.optimization.RiskBudgeting.html){:target="_blank"} (other risk measures)
- library | Referenced against Riskfolio-Lib's [Portfolio.rp_optimization](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/portfolio.html#Portfolio.Portfolio.rp_optimization){:target="_blank"} (other risk measures)

**Args:**

- <u>risk_budget (dict[str, float] &#124; None, optional):</u> The share of the risk per
asset, e.g. {"AAPL": 0.4, "MSFT": 0.2, ...}, positive for every asset;
it is scaled to sum to one. A budget that names an asset outside the
portfolio or leaves an asset out raises a ValueError that lists them.
Defaults to None, an equal share for every asset.
- <u>period (str, optional):</u> The frequency of the returns. Options are: "daily" (daily returns), "weekly"
(weekly returns), "monthly" (monthly returns), "quarterly" (quarterly returns), "yearly" (yearly
returns). Defaults to "daily".
- <u>covariance (str, optional):</u> The estimator of the covariance matrix. The shrinkage and denoised
estimators stabilize the weights when there are many assets compared to the number of periods.
Options are: "sample" (the sample covariance, ddof=1), "ledoit_wolf" (shrunk towards the scaled
identity, Ledoit and Wolf, 2004), "ledoit_wolf_constant_correlation" (shrunk towards the average
correlation, Ledoit and Wolf, 2004), "ledoit_wolf_single_factor" (shrunk towards the covariance that
the benchmark as a single factor implies, Ledoit and Wolf, 2003), "oas" (Oracle Approximating
Shrinkage, Chen et al., 2010), "shrunk" (a fixed 10% towards the scaled identity), "semicovariance"
(the co-movement below a zero return, Estrada, 2008), "exponential" (exponentially weighted, recent
periods weigh most, RiskMetrics), "denoised" (the eigenvalues of the correlation matrix that random
returns could produce averaged, Laloux et al., 2000), "denoised_spectral" (those eigenvalues set to
zero), "denoised_shrink" (the noise correlations shrunk towards their diagonal, López de Prado,
2020), "gerber" (co-movements beyond half a standard deviation, Gerber et al., 2022), "factor" (the
covariance of the Fama and French five factor model with OLS loadings, Fama and French, 1993),
"minimum_covariance_determinant" (the reweighted covariance of the half of the periods with the
smallest covariance determinant, robust to outliers, Rousseeuw and Van Driessen, 1999), "jlogo" (the
sparse inverse covariance on the TMFG planar graph of the correlations, Barfuss et al., 2016),
"geodesic" (10% towards the scaled identity along the geodesic of the positive definite matrices,
Bhatia, 2007), "regime_adjusted_ew" (exponentially weighted with a half-life of 40 periods, rescaled
by the recent realized against predicted risk, Paleologo, 2025), "nercome" (eigenvectors from one
part of the periods and the variances along them from the other, averaged over random splits, Lam,
2016), "ccc_garch" (the next-period covariance of GARCH(1, 1) volatilities with constant
correlations, Bollerslev, 1990), "mm" (the robust MM-estimator, Maronna et al., 2019), "rocke"
(Rocke's robust S-estimator, Maronna et al., 2019). Defaults to "sample".
- <u>covariance_span (int, optional):</u> The span in periods of the exponentially weighted covariance; the
weight of a period halves after about span / 2.9 periods. Defaults to 180.
- <u>minimum_weight (float &#124; dict[str, float], optional):</u> The lowest weight of
every asset, or per asset, e.g. {"AAPL": 0.05} (the others keep 0); it
cannot be negative. Defaults to 0.
- <u>maximum_weight (float &#124; dict[str, float], optional):</u> The highest weight of
every asset, or per asset, e.g. {"AAPL": 0.3} (the others keep 1).
Defaults to 1.
- <u>sector_bounds (dict[str, tuple[float, float]] &#124; None, optional):</u> The minimum
and maximum total weight per sector, e.g. {"Technology": (0, 0.4)}, with
the sector of each asset from its company profile. Defaults to None.
- <u>country_bounds (dict[str, tuple[float, float]] &#124; None, optional):</u> The minimum
and maximum total weight per country, named in full or by its two-letter
code, e.g. {"United States": (0, 0.6)}, with the country of each asset
from its company profile. Defaults to None.
- <u>risk_measure (str, optional):</u> The risk the assets share. Options are: "volatility" (of the covariance
estimator), "mad" (mean absolute deviation, Konno and Yamazaki, 1991), "semideviation" (below a zero
return), "lower_partial_moment" (below a zero return), "gini_mean_difference" (Yitzhaki, 1982),
"tail_gini" (Furman et al., 2017), "cvar_range" (the CVaR of the losses and of the gains),
"tail_gini_range" (the Tail Gini of the losses and of the gains), "ulcer_index" (of the uncompounded
cumulative return), "cvar" (Rockafellar and Uryasev, 2002), "cdar" (Chekhlov et al., 2005). Defaults
to "volatility".
- <u>alpha (float, optional):</u> The tail probability of the CVaR, CDaR, CVaR
range and Tail Gini measures, e.g. 0.05 for the worst 5% of periods.
Defaults to 0.05.
- <u>include_benchmark (bool, optional):</u> Whether to include the benchmark as an
asset. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per asset and for the portfolio, the Weight, Expected Return,
Volatility, Sharpe Ratio and Risk Contribution (of the volatility). With
another risk measure, also that measure (per period, positive for a loss,
named after it, e.g. "CVaR") of every asset on its own and of the portfolio,
and each asset's share of the portfolio's measure, e.g. "CVaR Contribution"
($$w_{i} \partial \rho / \partial w_{i} / \rho (w)$$ with central finite differences).

**Notes:**

- Weight, sector and country bounds turn it into constrained risk budgeting
(Richard and Roncalli, 2019): the bounds are linear constraints on $$w = y / \sum y$$,
so the problem stays convex. Where a bound
binds, the risk contributions can no longer all match the budget.
- Risk parity holds long positions only and is fully invested, so it takes no
negative minimum weight and no net or gross exposure.
- The other risk measures are per period of the chosen frequency and taken of the
historical returns, not of the covariance estimator. The CVaR, the CDaR, the
Ulcer Index and the Tail Gini measures follow a few periods and have kinks: at
the optimum the budget holds for one of the slopes on either side of a kink,
while the central finite differences of the contribution column average them,
so that column can differ from the budget by a few percent.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "JNJ", "XOM"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.portfolio.get_risk_parity_weights(sector_bounds={"Healthcare": (0, 0.3)})
```

Which returns:

|           |   Weight |   Expected Return |   Volatility |   Sharpe Ratio |   Risk Contribution |
|:----------|---------:|------------------:|-------------:|---------------:|--------------------:|
| AAPL      |   0.1991 |            0.1932 |       0.2786 |         0.5725 |              0.2763 |
| MSFT      |   0.2388 |            0.2017 |       0.2571 |         0.6534 |              0.2816 |
| JNJ       |   0.3    |            0.0987 |       0.1673 |         0.3884 |              0.1575 |
| XOM       |   0.2621 |            0.2911 |       0.2702 |         0.9524 |              0.2846 |
| Portfolio |   1      |            0.1925 |       0.1523 |         1.0429 |              1      |

---

## get_hierarchical_risk_parity_weights
Calculate the Hierarchical Risk Parity (HRP) weights, which split the risk over clusters of similar assets without inverting the covariance matrix.

The assets are clustered by their correlations, ordered so that similar assets sit next to each other, and the weight is split top-down between the two halves of every cluster in inverse proportion to their variance. It never inverts the covariance matrix, so it stays stable with many or highly correlated assets, where mean-variance weights become erratic.

As in the paper, the clustering uses the Euclidean distance between the columns of the correlation distance matrix $$\sqrt{(1 - \rho) / 2}$$: two assets are close when they relate to all the other assets in the same way. Some libraries cluster on the correlation distance itself, which can order the assets differently.

The risk of each half is that of its inverse risk portfolio, every asset weighted by the inverse of its own risk: the variance by default, as in the paper, or another risk measure of the historical returns, such as the CVaR, which splits by the losses in the worst periods, or the CDaR, which splits by the drawdowns. Raffinot (2017, 2018) allocates across hierarchical clusters with such measures.

**Also known as:** HRP, hierarchical clustering portfolio.

**References:**

- paper | López de Prado, M. (2016). "Building Diversified Portfolios that Outperform Out of Sample." The Journal of Portfolio Management, 42(4), 59-69.
- paper | Raffinot, T. (2017). "Hierarchical Clustering-Based Asset Allocation." The Journal of Portfolio Management, 44(2), 89-99.
- paper | Raffinot, T. (2018). "The Hierarchical Equal Risk Contribution Portfolio." SSRN 3237540.
- library | Referenced against Riskfolio-Lib's [HCPortfolio](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/hcportfolio.html#HCPortfolio.HCPortfolio){:target="_blank"} (HRP)
- library | Referenced against skfolio's [HierarchicalRiskParity](https://skfolio.org/generated/skfolio.optimization.HierarchicalRiskParity.html){:target="_blank"}
- library | Shares similar logic as PyPortfolioOpt's [HRPOpt](https://pyportfolioopt.readthedocs.io/en/latest/OtherOptimizers.html#pypfopt.hierarchical_portfolio.HRPOpt){:target="_blank"}
- library | Shares similar logic as RiskLabAI's [hrp](https://github.com/RiskLabAI/RiskLabAI.py/blob/v3.2.0/src/RiskLabAI/optimization/hrp.py#L169){:target="_blank"}

**Args:**

- <u>linkage_method (str, optional):</u> The linkage of the hierarchical clustering. Options are: "single"
(single linkage), "complete" (complete linkage), "average" (average linkage), "ward" (Ward's
method), "dbht" (the Directed Bubble Hierarchical Tree of Song, Di Matteo and Aste, 2012, on the
TMFG planar graph of the codependence, ordered by the distance itself). Defaults to "single".
- <u>codependence (str, optional):</u> The codependence the assets are clustered on. The rank correlations depend
only on the order of the returns, so a few extreme returns weigh less; the
distance correlation and mutual information also capture non-linear co-movement.
Options are: "pearson" (the linear correlation of the covariance matrix),
"spearman" (the rank correlation of the returns, Spearman, 1904), "kendall" (the
rank correlation $$\tau_{b}$$ of the returns, Kendall, 1938), "gerber" (co-movements
beyond half a standard deviation, Gerber et al., 2022), "detoned" (the
correlation without the market component, López de Prado, 2020), "distance" (the
distance correlation, Székely et al., 2007, through √(1 - dCor)),
"mutual_information" (through the variation of information, Meilă, 2007),
"lower_tail" (how often two assets fall into their lowest 5% of returns
together, through -ln $$\lambda$$), "absolute_angular" ($$\vert \rho \vert$$ through $$\sqrt{1 - \vert \rho \vert}$$, López de
Prado, 2020), "squared_angular" ($$\rho^{2}$$ through $$\sqrt{1 - \rho^{2}}$$, López de Prado, 2020),
"gnpr" (the rank co-movement and the difference between the return
distributions, $$\theta = 0.5$$, Marti et al., 2016). Defaults to "pearson".
- <u>period (str, optional):</u> The frequency of the returns. Options are: "daily" (daily returns), "weekly"
(weekly returns), "monthly" (monthly returns), "quarterly" (quarterly returns), "yearly" (yearly
returns). Defaults to "daily".
- <u>covariance (str, optional):</u> The estimator of the covariance matrix. The shrinkage and denoised
estimators stabilize the weights when there are many assets compared to the number of periods.
Options are: "sample" (the sample covariance, ddof=1), "ledoit_wolf" (shrunk towards the scaled
identity, Ledoit and Wolf, 2004), "ledoit_wolf_constant_correlation" (shrunk towards the average
correlation, Ledoit and Wolf, 2004), "ledoit_wolf_single_factor" (shrunk towards the covariance that
the benchmark as a single factor implies, Ledoit and Wolf, 2003), "oas" (Oracle Approximating
Shrinkage, Chen et al., 2010), "shrunk" (a fixed 10% towards the scaled identity), "semicovariance"
(the co-movement below a zero return, Estrada, 2008), "exponential" (exponentially weighted, recent
periods weigh most, RiskMetrics), "denoised" (the eigenvalues of the correlation matrix that random
returns could produce averaged, Laloux et al., 2000), "denoised_spectral" (those eigenvalues set to
zero), "denoised_shrink" (the noise correlations shrunk towards their diagonal, López de Prado,
2020), "gerber" (co-movements beyond half a standard deviation, Gerber et al., 2022), "factor" (the
covariance of the Fama and French five factor model with OLS loadings, Fama and French, 1993),
"minimum_covariance_determinant" (the reweighted covariance of the half of the periods with the
smallest covariance determinant, robust to outliers, Rousseeuw and Van Driessen, 1999), "jlogo" (the
sparse inverse covariance on the TMFG planar graph of the correlations, Barfuss et al., 2016),
"geodesic" (10% towards the scaled identity along the geodesic of the positive definite matrices,
Bhatia, 2007), "regime_adjusted_ew" (exponentially weighted with a half-life of 40 periods, rescaled
by the recent realized against predicted risk, Paleologo, 2025), "nercome" (eigenvectors from one
part of the periods and the variances along them from the other, averaged over random splits, Lam,
2016), "ccc_garch" (the next-period covariance of GARCH(1, 1) volatilities with constant
correlations, Bollerslev, 1990), "mm" (the robust MM-estimator, Maronna et al., 2019), "rocke"
(Rocke's robust S-estimator, Maronna et al., 2019). Defaults to "sample".
- <u>covariance_span (int, optional):</u> The span in periods of the exponentially weighted covariance; the
weight of a period halves after about span / 2.9 periods. Defaults to 180.
- <u>minimum_weight (float &#124; dict[str, float], optional):</u> The lowest weight of
every asset, or per asset, e.g. {"AAPL": 0.05} (the others keep 0); it
cannot be negative. Defaults to 0.
- <u>maximum_weight (float &#124; dict[str, float], optional):</u> The highest weight of
every asset, or per asset, e.g. {"AAPL": 0.3} (the others keep 1).
Defaults to 1.
- <u>risk_measure (str, optional):</u> The risk measure of the splits. Options are: "variance" (of the covariance
matrix), "volatility" (of the covariance matrix), "mad" (mean absolute deviation, Konno and
Yamazaki, 1991), "semideviation" (below the minimum acceptable return), "lower_partial_moment"
(first order), "worst_realization" (the worst return), "gini_mean_difference" (Yitzhaki, 1982),
"tail_gini" (Furman et al., 2017), "range" (the best minus the worst return), "cvar_range" (the CVaR
of the losses and of the gains), "tail_gini_range" (the Tail Gini of the losses and of the gains),
"ulcer_index" (of the uncompounded cumulative return), "cvar" (Rockafellar and Uryasev, 2002),
"cdar" (Chekhlov et al., 2005). Defaults to "variance".
- <u>alpha (float, optional):</u> The tail probability of the CVaR, CDaR, CVaR
range and Tail Gini measures, e.g. 0.05 for the worst 5% of periods.
Defaults to 0.05.
- <u>minimum_acceptable_return (float &#124; str, optional):</u> The threshold of the semideviation and the lower
partial moment, as a return per period of the chosen frequency, or "mean" for each asset's average
return. Defaults to 0.
- <u>include_benchmark (bool, optional):</u> Whether to include the benchmark as an
asset. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per asset and for the portfolio, the Weight, Expected Return,
Volatility, Sharpe Ratio and Risk Contribution, and with a risk measure of the
returns, that measure per period (e.g. "CVaR").

**Notes:**

- Weight bounds move each split just enough to keep both halves within the sum of
their assets' bounds.
- The risk measures of the returns are per period of the chosen frequency and not
annualized, and only their ratios between the halves matter. They equal the weights of
Riskfolio-Lib's HCPortfolio and skfolio's HierarchicalRiskParity with the same risk
measure on the same asset order; those cluster on the correlation distance itself
rather than the distance between its columns, which can order the assets differently.
- A split only moves weight between the two halves of a cluster, so sector and
country bounds, which cut across the clusters, do not apply; neither do short
positions or a net or gross exposure, as HRP is long only and fully invested.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "JNJ", "XOM"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.portfolio.get_hierarchical_risk_parity_weights(maximum_weight={"JNJ": 0.3})
```

Which returns:

|           |   Weight |   Expected Return |   Volatility |   Sharpe Ratio |   Risk Contribution |
|:----------|---------:|------------------:|-------------:|---------------:|--------------------:|
| AAPL      |   0.1287 |            0.1932 |       0.2786 |         0.5725 |              0.1307 |
| MSFT      |   0.1511 |            0.2017 |       0.2571 |         0.6534 |              0.1184 |
| JNJ       |   0.3    |            0.0987 |       0.1673 |         0.3884 |              0.1503 |
| XOM       |   0.4201 |            0.2911 |       0.2702 |         0.9524 |              0.6006 |
| Portfolio |   1      |            0.2073 |       0.1569 |         1.1059 |              1      |

---

## get_schur_complementary_weights
Calculate the Schur Complementary Allocation weights, which run from Hierarchical Risk Parity ($$\gamma = 0$$) towards the minimum variance portfolio ($$\gamma$$ near 1).

HRP splits every cluster between its two halves by their own variances and ignores how the two halves move together; the minimum variance portfolio uses exactly that, through the Schur complements of the inverse covariance matrix, but becomes unstable when the covariance matrix is noisy. Schur Complementary Allocation augments the covariance block of each half with a share $$\gamma$$ of what the other half tells about it, and then splits as HRP does on the augmented blocks.

For a cluster split into halves with covariance blocks A and D and the block B between them, the formula is as follows:

$$
A_{c} = A - \gamma B D^{- 1} B'
$$

$$
\tilde{A} = (I - \gamma B D^{- 1} M')^{- 1} A_{c},\;\; \text{made symmetric, with } M \text{ the step-up matrix that spreads the assets of the other half over those of this one (the identity for halves of equal size)},\;\; \text{so that}\; \tilde{A}^{- 1} 1 = A_{c}^{- 1}(1 - \gamma B D^{- 1} \;\text{M'1}),\;\; \text{the minimum variance weights of the half up to a scale}
$$

$$
\alpha = 1 - \frac{\nu(\tilde{A})}{\nu(\tilde{A}) + \nu(\tilde{D})},\;\; \text{the share of the first half, with } \nu \text{ the variance of the inverse variance portfolio of a block}
$$

The halves are then split further on Ã and D̃. The assets are clustered and ordered as in Hierarchical Risk Parity, so $$\gamma = 0$$ gives its weights.

**Also known as:** Schur complementary portfolio, Schur allocation.

**References:**

- paper | Cotton, P. (2024). "Schur Complementary Allocation: A Unification of Hierarchical Risk Parity and Minimum Variance Portfolios." arXiv 2411.05807.
- paper | López de Prado, M. (2016). "Building Diversified Portfolios that Outperform Out of Sample." The Journal of Portfolio Management, 42(4), 59-69.
- library | Referenced against skfolio's [SchurComplementary](https://skfolio.org/generated/skfolio.optimization.SchurComplementary.html){:target="_blank"}

**Args:**

- <u>gamma (float, optional):</u> How much of the covariance between the halves of a
cluster the splits use, between 0 (Hierarchical Risk Parity) and 1.
Defaults to 0.5.
- <u>linkage_method (str, optional):</u> The linkage of the hierarchical clustering, as in Hierarchical Risk
Parity. Options are: "single" (single linkage), "complete" (complete linkage), "average" (average
linkage), "ward" (Ward's method), "dbht" (the Directed Bubble Hierarchical Tree of Song, Di Matteo
and Aste, 2012). Defaults to "single".
- <u>codependence (str, optional):</u> The codependence the assets are clustered on (see
get_hierarchical_risk_parity_weights). Defaults to. Options are: "pearson" (the
linear correlation of the covariance matrix), "spearman" (the rank correlation
of the returns, Spearman, 1904), "kendall" (the rank correlation $$\tau_{b}$$ of the
returns, Kendall, 1938), "gerber" (co-movements beyond half a standard
deviation, Gerber et al., 2022), "detoned" (the correlation without the market
component, López de Prado, 2020), "distance" (the distance correlation, Székely
et al., 2007, through √(1 - dCor)), "mutual_information" (through the variation
of information, Meilă, 2007), "lower_tail" (how often two assets fall into their
lowest 5% of returns together, through -ln $$\lambda$$), "absolute_angular" ($$\vert \rho \vert$$ through
$$\sqrt{1 - \vert \rho \vert}$$, López de Prado, 2020), "squared_angular" ($$\rho^{2}$$ through $$\sqrt{1 - \rho^{2}}$$,
López de Prado, 2020), "gnpr" (the rank co-movement and the difference between
the return distributions, $$\theta = 0.5$$, Marti et al., 2016). Defaults to "pearson".
- <u>period (str, optional):</u> The frequency of the returns. Options are: "daily" (daily returns), "weekly"
(weekly returns), "monthly" (monthly returns), "quarterly" (quarterly returns), "yearly" (yearly
returns). Defaults to "daily".
- <u>covariance (str, optional):</u> The estimator of the covariance matrix (see
get_hierarchical_risk_parity_weights). A shrinkage estimator such as "ledoit_wolf" keeps the
augmented blocks positive definite at a higher gamma. Defaults to. Options are: "sample" (the sample
covariance, ddof=1), "ledoit_wolf" (shrunk towards the scaled identity, Ledoit and Wolf, 2004),
"ledoit_wolf_constant_correlation" (shrunk towards the average correlation, Ledoit and Wolf, 2004),
"ledoit_wolf_single_factor" (shrunk towards the covariance that the benchmark as a single factor
implies, Ledoit and Wolf, 2003), "oas" (Oracle Approximating Shrinkage, Chen et al., 2010), "shrunk"
(a fixed 10% towards the scaled identity), "semicovariance" (the co-movement below a zero return,
Estrada, 2008), "exponential" (exponentially weighted, recent periods weigh most, RiskMetrics),
"denoised" (the eigenvalues of the correlation matrix that random returns could produce averaged,
Laloux et al., 2000), "denoised_spectral" (those eigenvalues set to zero), "denoised_shrink" (the
noise correlations shrunk towards their diagonal, López de Prado, 2020), "gerber" (co-movements
beyond half a standard deviation, Gerber et al., 2022), "factor" (the covariance of the Fama and
French five factor model with OLS loadings, Fama and French, 1993), "minimum_covariance_determinant"
(the reweighted covariance of the half of the periods with the smallest covariance determinant,
robust to outliers, Rousseeuw and Van Driessen, 1999), "jlogo" (the sparse inverse covariance on the
TMFG planar graph of the correlations, Barfuss et al., 2016), "geodesic" (10% towards the scaled
identity along the geodesic of the positive definite matrices, Bhatia, 2007), "regime_adjusted_ew"
(exponentially weighted with a half-life of 40 periods, rescaled by the recent realized against
predicted risk, Paleologo, 2025), "nercome" (eigenvectors from one part of the periods and the
variances along them from the other, averaged over random splits, Lam, 2016), "ccc_garch" (the
next-period covariance of GARCH(1, 1) volatilities with constant correlations, Bollerslev, 1990),
"mm" (the robust MM-estimator, Maronna et al., 2019), "rocke" (Rocke's robust S-estimator, Maronna
et al., 2019). Defaults to "sample".
- <u>covariance_span (int, optional):</u> The span in periods of the exponentially weighted covariance; the
weight of a period halves after about span / 2.9 periods. Defaults to 180.
- <u>minimum_weight (float &#124; dict[str, float], optional):</u> The lowest weight of
every asset, or per asset, e.g. {"AAPL": 0.05} (the others keep 0); it
cannot be negative. Defaults to 0.
- <u>maximum_weight (float &#124; dict[str, float], optional):</u> The highest weight of
every asset, or per asset, e.g. {"AAPL": 0.3} (the others keep 1).
Defaults to 1.
- <u>include_benchmark (bool, optional):</u> Whether to include the benchmark as an
asset. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per asset and for the portfolio, the Weight, Expected Return,
Volatility, Sharpe Ratio and Risk Contribution. Returns and volatilities are
annualized.

**Notes:**

- Weight bounds move each split just enough to keep both halves within the sum of
their assets' bounds, as in Hierarchical Risk Parity; the method is long only
and fully invested.
- The portfolio's variance need not fall as gamma rises: the augmented blocks can
make a split worse when the covariance matrix is poorly conditioned. skfolio
by default caps gamma where the variance stops falling;
here gamma is used as given, so compare the Volatility with that of a lower
gamma. When an augmented block is not positive definite, the method returns an
error that asks for a lower gamma or a shrinkage covariance estimator.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "JNJ", "XOM"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.portfolio.get_schur_complementary_weights(gamma=0.5)
```

Which returns:

|           |   Weight |   Expected Return |   Volatility |   Sharpe Ratio |   Risk Contribution |
|:----------|---------:|------------------:|-------------:|---------------:|--------------------:|
| AAPL      |   0.1146 |            0.1932 |       0.2786 |         0.5725 |              0.136  |
| MSFT      |   0.1448 |            0.2017 |       0.2571 |         0.6534 |              0.1365 |
| JNJ       |   0.5231 |            0.0987 |       0.1673 |         0.3884 |              0.479  |
| XOM       |   0.2175 |            0.2911 |       0.2702 |         0.9526 |              0.2485 |
| Portfolio |   1      |            0.1663 |       0.1372 |         0.9663 |              1      |

---

## get_stacking_weights
Calculate the weights of a stacked portfolio.

Several optimizers each give their portfolio, and a final optimizer divides the weight over those portfolios as if they were assets, judged by the returns each earns out of sample. Each optimizer has its own strengths (inverse volatility is robust, maximum diversification spreads the risk, HRP avoids inverting the covariance matrix, minimum CVaR guards the tail); stacking combines them by how they hold up rather than choosing one.

The formula is as follows:

$$
w = W v,\;\; \text{with } W \text{ the } N \times K \text{ matrix whose column } k \text{ holds the weights of method } k \text{ optimized on all periods, and } v \text{ the weights the final method gives the } K \text{ portfolios}
$$

- The final method is optimized on the returns of the K portfolios. With folds, the periods are cut into that many consecutive blocks; for each block the methods are optimized on the other periods and their portfolios earn the block's returns, so every return the final method sees is out of sample (a K-fold cross-validation without shuffling). Without folds it uses the in-sample returns R W, which favours the methods that fit the past best.

**Also known as:** stacking, stacked generalization, ensemble optimization.

**References:**

- paper | Wolpert, D. H. (1992). "Stacked Generalization." Neural Networks, 5(2), 241-259.
- library | Referenced against skfolio's [StackingOptimization](https://skfolio.org/generated/skfolio.optimization.StackingOptimization.html){:target="_blank"}

**Args:**

- <u>methods (str &#124; list[str] &#124; None, optional):</u> The optimizers to combine, a list or a comma-separated
string, each with its default settings. Options are: "minimum_variance" (Minimum Variance),
"maximum_sharpe" (Maximum Sharpe), "risk_parity" (Risk Parity), "inverse_volatility" (Inverse
Volatility), "maximum_diversification" (Maximum Diversification), "hierarchical_risk_parity"
(Hierarchical Risk Parity), "hierarchical_equal_risk_contribution" (Hierarchical Equal Risk
Contribution), "nested_clustered_optimization" (Nested Clustered Optimization),
"schur_complementary" (Schur Complementary), "minimum_cvar" (Minimum CVaR), "minimum_drawdown"
(Minimum Drawdown), "minimum_mad" (Minimum MAD), "minimum_semideviation" (Minimum Semideviation),
"equal_weight" (Equal Weight). Defaults to None, which uses "inverse_volatility",
"maximum_diversification", "hierarchical_risk_parity" and "minimum_cvar".
- <u>final_method (str, optional):</u> The optimizer that weights the methods' portfolios. Options are:
"minimum_variance" (Minimum Variance), "maximum_sharpe" (Maximum Sharpe), "risk_parity" (Risk
Parity), "inverse_volatility" (Inverse Volatility), "maximum_diversification" (Maximum
Diversification), "hierarchical_risk_parity" (Hierarchical Risk Parity),
"hierarchical_equal_risk_contribution" (Hierarchical Equal Risk Contribution),
"nested_clustered_optimization" (Nested Clustered Optimization), "schur_complementary" (Schur
Complementary), "minimum_cvar" (Minimum CVaR), "minimum_drawdown" (Minimum Drawdown), "minimum_mad"
(Minimum MAD), "minimum_semideviation" (Minimum Semideviation), "equal_weight" (Equal Weight).
Defaults to "minimum_variance".
- <u>folds (int &#124; None, optional):</u> The number of consecutive blocks of the
cross-validation, at least 2, or None to use the in-sample returns.
Defaults to 5.
- <u>period (str, optional):</u> The frequency of the returns. Options are: "daily" (daily returns), "weekly"
(weekly returns), "monthly" (monthly returns), "quarterly" (quarterly returns), "yearly" (yearly
returns). Defaults to "daily".
- <u>covariance (str, optional):</u> The estimator of the covariance matrix of the methods that use one (see
get_minimum_variance_weights). Defaults to. Options are: "sample" (the sample covariance, ddof=1),
"ledoit_wolf" (shrunk towards the scaled identity, Ledoit and Wolf, 2004),
"ledoit_wolf_constant_correlation" (shrunk towards the average correlation, Ledoit and Wolf, 2004),
"ledoit_wolf_single_factor" (shrunk towards the covariance that the benchmark as a single factor
implies, Ledoit and Wolf, 2003), "oas" (Oracle Approximating Shrinkage, Chen et al., 2010), "shrunk"
(a fixed 10% towards the scaled identity), "semicovariance" (the co-movement below a zero return,
Estrada, 2008), "exponential" (exponentially weighted, recent periods weigh most, RiskMetrics),
"denoised" (the eigenvalues of the correlation matrix that random returns could produce averaged,
Laloux et al., 2000), "denoised_spectral" (those eigenvalues set to zero), "denoised_shrink" (the
noise correlations shrunk towards their diagonal, López de Prado, 2020), "gerber" (co-movements
beyond half a standard deviation, Gerber et al., 2022), "factor" (the covariance of the Fama and
French five factor model with OLS loadings, Fama and French, 1993), "minimum_covariance_determinant"
(the reweighted covariance of the half of the periods with the smallest covariance determinant,
robust to outliers, Rousseeuw and Van Driessen, 1999), "jlogo" (the sparse inverse covariance on the
TMFG planar graph of the correlations, Barfuss et al., 2016), "geodesic" (10% towards the scaled
identity along the geodesic of the positive definite matrices, Bhatia, 2007), "regime_adjusted_ew"
(exponentially weighted with a half-life of 40 periods, rescaled by the recent realized against
predicted risk, Paleologo, 2025), "nercome" (eigenvectors from one part of the periods and the
variances along them from the other, averaged over random splits, Lam, 2016), "ccc_garch" (the
next-period covariance of GARCH(1, 1) volatilities with constant correlations, Bollerslev, 1990),
"mm" (the robust MM-estimator, Maronna et al., 2019), "rocke" (Rocke's robust S-estimator, Maronna
et al., 2019). Defaults to "sample".
- <u>covariance_span (int, optional):</u> The span in periods of the exponentially weighted covariance; the
weight of a period halves after about span / 2.9 periods. Defaults to 180.
- <u>expected_returns (str, optional):</u> The estimator of the expected returns of "maximum_sharpe" (see
get_maximum_sharpe_weights). Defaults to. Options are: "mean" (the historical average), "geometric"
(the compounded average), "exponential" (the exponentially weighted average, recent periods weigh
most), "exponential_geometric" (that average compounded over a year), "capm" (the returns the
Capital Asset Pricing Model implies from each asset's beta to the benchmark, Sharpe, 1964),
"bayes_stein" (the averages shrunk towards that of the minimum variance portfolio, Jorion, 1986),
"james_stein" (the averages shrunk towards their grand mean, James and Stein, 1961),
"bodnar_okhrin_parolya" (the averages and their grand mean combined with optimal weights, Bodnar,
Okhrin and Parolya, 2019). Defaults to "mean".
- <u>expected_returns_span (int, optional):</u> The span in periods of the exponentially weighted expected
returns. Defaults to 180.
- <u>include_benchmark (bool, optional):</u> Whether to include the benchmark as an
asset. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per asset and for the portfolio, the Weight, Expected Return,
Volatility, Sharpe Ratio and Risk Contribution of the stacked portfolio, and a
column per method with its weights, whose Portfolio row is the method's weight
in the stacked portfolio. Returns and volatilities are annualized.

**Notes:**

- Every method and the final method are long only and fully invested and use their
default settings; the risk free rate of the maximum Sharpe ratio is the Toolkit's
average over the periods it is optimized on.
- skfolio's StackingOptimization uses 5-fold cross-validation by default as well;
its blocks follow scikit-learn's KFold, the same consecutive blocks with the
first ones one period longer when the periods do not divide evenly.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "JNJ", "XOM"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.portfolio.get_stacking_weights()[
    [
        "Weight",
        "Maximum Diversification",
        "Hierarchical Risk Parity",
        "Minimum CVaR",
    ]
]
```

Which returns:

|           |   Weight |   Maximum Diversification |   Hierarchical Risk Parity |   Minimum CVaR |
|:----------|---------:|--------------------------:|---------------------------:|---------------:|
| AAPL      |   0.1287 |                    0.0922 |                     0.1287 |         0      |
| MSFT      |   0.1511 |                    0.2349 |                     0.1511 |         0.1823 |
| JNJ       |   0.5207 |                    0.4195 |                     0.5207 |         0.5968 |
| XOM       |   0.1995 |                    0.2534 |                     0.1995 |         0.2209 |
| Portfolio |   1      |                    0      |                     1      |         0      |

---

## get_hierarchical_equal_risk_contribution_weights
Calculate the Hierarchical Equal Risk Contribution (HERC) weights, which split the weight top-down over clusters of similar assets by their risk.

The assets are clustered by their correlations and the dendrogram is cut into clusters. Within a cluster every asset gets a weight in inverse proportion to its variance; between clusters the weight is split top-down along the dendrogram, each branch getting a weight in inverse proportion to its risk, the sum of the variances of its clusters. Unlike Hierarchical Risk Parity, which halves the ordered list of assets, the splits follow the tree, so assets that belong together are never split up, and the weight is allocated over the clusters rather than over the assets: riskier clusters get less.

The clustering uses the correlation distance $$\sqrt{(1 - \rho) / 2}$$ with Ward linkage, as in the paper. Without a number of clusters, it is the one at the sharpest bend of the pooled within-cluster dispersion, the two-order difference of the gap statistic (Yue, Wang and Wei, 2008; Tibshirani, Walther and Hastie, 2001), or with the standardized silhouette the one whose clusters have the highest mean over standard deviation of the silhouette coefficients (López de Prado, 2020; Rousseeuw, 1987).

The risk of a cluster is that of its inverse risk portfolio: the variance by default, or, as in the paper, another risk measure of the historical returns, such as the CVaR or the CDaR. With equal weights within the clusters, the assets of a cluster share its weight equally while the clusters are still split by the risk of their inverse risk portfolios, the HERC2 variant of Cajas.

**Also known as:** HERC, hierarchical clustering-based risk parity.

**References:**

- paper | Raffinot, T. (2018). "The Hierarchical Equal Risk Contribution Portfolio." SSRN 3237540.
- paper | Raffinot, T. (2017). "Hierarchical Clustering-Based Asset Allocation." The Journal of Portfolio Management, 44(2), 89-99.
- paper | López de Prado, M. (2020). "Machine Learning for Asset Managers." Cambridge University Press.
- paper | Rousseeuw, P. J. (1987). "Silhouettes: A Graphical Aid to the Interpretation and Validation of Cluster Analysis." Journal of Computational and Applied Mathematics, 20, 53-65.
- library | Referenced against skfolio's [HierarchicalEqualRiskContribution](https://skfolio.org/generated/skfolio.optimization.HierarchicalEqualRiskContribution.html){:target="_blank"}
- library | Referenced against Riskfolio-Lib's [HCPortfolio](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/hcportfolio.html#HCPortfolio.HCPortfolio){:target="_blank"} (HERC and HERC2)

**Args:**

- <u>linkage_method (str, optional):</u> The linkage of the hierarchical clustering; Ward's method is the
paper's. Options are: "single" (single linkage), "complete" (complete linkage), "average" (average
linkage), "ward" (Ward's method), "dbht" (the Directed Bubble Hierarchical Tree of Song, Di Matteo
and Aste, 2012, whose own clusters are used without a number of clusters). Defaults to "ward".
- <u>clusters (int &#124; None, optional):</u> The number of clusters. Defaults to None,
chosen by the two-order difference of the gap statistic.
- <u>cluster_criterion (str, optional):</u> How the number of clusters is chosen when it is not given. Options
are: "two_difference_gap" (the sharpest bend of the within-cluster dispersion, Yue, Wang and Wei,
2008), "standardized_silhouette" (the highest mean over standard deviation of the silhouette
coefficients, López de Prado, 2020). Defaults to "two_difference_gap".
- <u>codependence (str, optional):</u> The codependence the assets are clustered on. The rank correlations depend
only on the order of the returns, so a few extreme returns weigh less; the
distance correlation and mutual information also capture non-linear co-movement.
Options are: "pearson" (the linear correlation of the covariance matrix),
"spearman" (the rank correlation of the returns, Spearman, 1904), "kendall" (the
rank correlation $$\tau_{b}$$ of the returns, Kendall, 1938), "gerber" (co-movements
beyond half a standard deviation, Gerber et al., 2022), "detoned" (the
correlation without the market component, López de Prado, 2020), "distance" (the
distance correlation, Székely et al., 2007, through √(1 - dCor)),
"mutual_information" (through the variation of information, Meilă, 2007),
"lower_tail" (how often two assets fall into their lowest 5% of returns
together, through -ln $$\lambda$$), "absolute_angular" ($$\vert \rho \vert$$ through $$\sqrt{1 - \vert \rho \vert}$$, López de
Prado, 2020), "squared_angular" ($$\rho^{2}$$ through $$\sqrt{1 - \rho^{2}}$$, López de Prado, 2020),
"gnpr" (the rank co-movement and the difference between the return
distributions, $$\theta = 0.5$$, Marti et al., 2016). Defaults to "pearson".
- <u>period (str, optional):</u> The frequency of the returns. Options are: "daily" (daily returns), "weekly"
(weekly returns), "monthly" (monthly returns), "quarterly" (quarterly returns), "yearly" (yearly
returns). Defaults to "daily".
- <u>covariance (str, optional):</u> The estimator of the covariance matrix, which also gives the correlations
that are clustered. The shrinkage and denoised estimators stabilize the weights when there are many
assets compared to the number of periods. Options are: "sample" (the sample covariance, ddof=1),
"ledoit_wolf" (shrunk towards the scaled identity, Ledoit and Wolf, 2004),
"ledoit_wolf_constant_correlation" (shrunk towards the average correlation, Ledoit and Wolf, 2004),
"ledoit_wolf_single_factor" (shrunk towards the covariance that the benchmark as a single factor
implies, Ledoit and Wolf, 2003), "oas" (Oracle Approximating Shrinkage, Chen et al., 2010), "shrunk"
(a fixed 10% towards the scaled identity), "semicovariance" (the co-movement below a zero return,
Estrada, 2008), "exponential" (exponentially weighted, recent periods weigh most, RiskMetrics),
"denoised" (the eigenvalues of the correlation matrix that random returns could produce averaged,
Laloux et al., 2000), "denoised_spectral" (those eigenvalues set to zero), "denoised_shrink" (the
noise correlations shrunk towards their diagonal, López de Prado, 2020), "gerber" (co-movements
beyond half a standard deviation, Gerber et al., 2022), "factor" (the covariance of the Fama and
French five factor model with OLS loadings, Fama and French, 1993), "minimum_covariance_determinant"
(the reweighted covariance of the half of the periods with the smallest covariance determinant,
robust to outliers, Rousseeuw and Van Driessen, 1999), "jlogo" (the sparse inverse covariance on the
TMFG planar graph of the correlations, Barfuss et al., 2016), "geodesic" (10% towards the scaled
identity along the geodesic of the positive definite matrices, Bhatia, 2007), "regime_adjusted_ew"
(exponentially weighted with a half-life of 40 periods, rescaled by the recent realized against
predicted risk, Paleologo, 2025), "nercome" (eigenvectors from one part of the periods and the
variances along them from the other, averaged over random splits, Lam, 2016), "ccc_garch" (the
next-period covariance of GARCH(1, 1) volatilities with constant correlations, Bollerslev, 1990),
"mm" (the robust MM-estimator, Maronna et al., 2019), "rocke" (Rocke's robust S-estimator, Maronna
et al., 2019). Defaults to "sample".
- <u>covariance_span (int, optional):</u> The span in periods of the exponentially weighted covariance; the
weight of a period halves after about span / 2.9 periods. Defaults to 180.
- <u>minimum_weight (float &#124; dict[str, float], optional):</u> The lowest weight of
every asset, or per asset, e.g. {"AAPL": 0.05} (the others keep 0); it
cannot be negative. Defaults to 0.
- <u>maximum_weight (float &#124; dict[str, float], optional):</u> The highest weight of
every asset, or per asset, e.g. {"AAPL": 0.3} (the others keep 1).
Defaults to 1.
- <u>sector_bounds (dict[str, tuple[float, float]] &#124; None, optional):</u> The minimum
and maximum total weight per sector, e.g. {"Technology": (0, 0.4)}, with
the sector of each asset from its company profile. Defaults to None.
- <u>country_bounds (dict[str, tuple[float, float]] &#124; None, optional):</u> The minimum
and maximum total weight per country, named in full or by its two-letter
code, e.g. {"United States": (0, 0.6)}, with the country of each asset
from its company profile. Defaults to None.
- <u>risk_measure (str, optional):</u> The risk measure of the clusters. Options are: "variance" (of the
covariance matrix), "volatility" (of the covariance matrix), "mad" (mean absolute deviation, Konno
and Yamazaki, 1991), "semideviation" (below the minimum acceptable return), "lower_partial_moment"
(first order), "worst_realization" (the worst return), "gini_mean_difference" (Yitzhaki, 1982),
"tail_gini" (Furman et al., 2017), "range" (the best minus the worst return), "cvar_range" (the CVaR
of the losses and of the gains), "tail_gini_range" (the Tail Gini of the losses and of the gains),
"ulcer_index" (of the uncompounded cumulative return), "cvar" (Rockafellar and Uryasev, 2002),
"cdar" (Chekhlov et al., 2005). Defaults to "variance".
- <u>alpha (float, optional):</u> The tail probability of the CVaR, CDaR, CVaR
range and Tail Gini measures, e.g. 0.05 for the worst 5% of periods.
Defaults to 0.05.
- <u>minimum_acceptable_return (float &#124; str, optional):</u> The threshold of the semideviation and the lower
partial moment, as a return per period of the chosen frequency, or "mean" for each asset's average
return. Defaults to 0.
- <u>within_clusters (str, optional):</u> The weights within a cluster. Options are: "inverse_risk" (inverse to
each asset's risk), "equal" (equal weights, HERC2). Defaults to "inverse_risk".
- <u>include_benchmark (bool, optional):</u> Whether to include the benchmark as an
asset. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per asset and for the portfolio, the Weight, Expected Return,
Volatility, Sharpe Ratio and Risk Contribution, with a risk measure of the
returns that measure per period (e.g. "CDaR"), and the Cluster of every asset
(numbered from 1). Returns and volatilities are annualized.

**Notes:**

- Weight, sector and country bounds are applied after the allocation: when the
weights fall outside them, they move to the weights within the bounds with the
smallest relative change, $$\sum (w_{i} / w_{\text{HERC},i} - 1)^{2}$$.
- The risk measures of the returns are per period of the chosen frequency and not
annualized. With the same clusters, the weights equal those of Riskfolio-Lib's
HCPortfolio and skfolio's HierarchicalEqualRiskContribution with the same risk
measure. Riskfolio-Lib's own
two-order difference sums the standard deviation of the distances within each
cluster, which can pick another number of clusters.
- HERC is long only and fully invested, so short positions and a net or gross
exposure do not apply.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "JNJ", "XOM"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.portfolio.get_hierarchical_equal_risk_contribution_weights()[
    ["Weight", "Volatility", "Sharpe Ratio", "Risk Contribution", "Cluster"]
]
```

Which returns:

|           |   Weight |   Volatility |   Sharpe Ratio |   Risk Contribution |   Cluster |
|:----------|---------:|-------------:|---------------:|--------------------:|----------:|
| AAPL      |   0.2917 |       0.2786 |         0.5725 |              0.412  |         1 |
| MSFT      |   0.3425 |       0.2571 |         0.6534 |              0.4348 |         1 |
| JNJ       |   0.2645 |       0.1673 |         0.3884 |              0.1009 |         2 |
| XOM       |   0.1014 |       0.2702 |         0.9524 |              0.0523 |         3 |
| Portfolio |   1      |       0.1715 |         0.8592 |              1      |       nan |

---

## get_nested_clustered_optimization_weights
Calculate the Nested Clustered Optimization (NCO) weights, optimized within clusters of similar assets and then across the clusters.

The assets are clustered by their correlations, the objective is optimized within every cluster, and then once more across the clusters, each cluster acting as one asset that holds its own optimal portfolio. Estimation noise in the covariance matrix mostly sits among correlated assets, which is what makes mean-variance weights unstable; by optimizing within and across clusters separately, NCO keeps that noise contained and the weights steadier out of sample.

With W the matrix whose column k holds the optimal weights within cluster k, the clusters have the expected returns $$W' \mu$$ and the covariance matrix $$W' \Sigma W$$; the weights across the clusters v are optimal for those, and the weight of every asset is $$w = W v$$. The clusters are found as in HERC (correlation distance, Ward linkage, the number of clusters from the two-order difference of the gap statistic) and the covariance matrix is denoised by default, as in the paper. With another risk measure than the variance, the minimum variance objective minimizes that measure of the historical returns and the risk parity objective equalizes its risk contributions, within the clusters and across them on the returns of the clusters' portfolios, as Riskfolio-Lib's HCPortfolio does.

**Also known as:** NCO, nested clustered optimisation.

**References:**

- paper | López de Prado, M. (2019). "A Robust Estimator of the Efficient Frontier." SSRN 3469961.
- paper | López de Prado, M. (2020). "Machine Learning for Asset Managers." Cambridge University Press, chapter 7.
- library | Referenced against Riskfolio-Lib's [HCPortfolio](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/hcportfolio.html#HCPortfolio.HCPortfolio){:target="_blank"} (NCO)
- library | Shares similar logic as skfolio's [NestedClustersOptimization](https://skfolio.org/generated/skfolio.optimization.NestedClustersOptimization.html){:target="_blank"}
- library | Shares similar logic as RiskLabAI's [get_optimal_portfolio_weights_nco](https://github.com/RiskLabAI/RiskLabAI.py/blob/v3.2.0/src/RiskLabAI/optimization/nco.py#L49){:target="_blank"}

**Args:**

- <u>objective (str, optional):</u> The objective at both levels. Options are: "minimum_variance" (the lowest
risk), "maximum_sharpe" (the highest Sharpe ratio), "risk_parity" (equal risk contribution).
Defaults to "minimum_variance".
- <u>linkage_method (str, optional):</u> The linkage of the hierarchical clustering. Options are: "single"
(single linkage), "complete" (complete linkage), "average" (average linkage), "ward" (Ward's
method), "dbht" (the Directed Bubble Hierarchical Tree of Song, Di Matteo and Aste, 2012, whose own
clusters are used without a number of clusters). Defaults to "ward".
- <u>clusters (int &#124; None, optional):</u> The number of clusters. Defaults to None,
chosen by the two-order difference of the gap statistic.
- <u>cluster_criterion (str, optional):</u> How the number of clusters is chosen when it is not given. Options
are: "two_difference_gap" (the sharpest bend of the within-cluster dispersion, Yue, Wang and Wei,
2008), "standardized_silhouette" (the highest mean over standard deviation of the silhouette
coefficients, López de Prado, 2020), "onc" (the Optimal Number of Clusters algorithm of López de
Prado and Lewis, 2019). Defaults to "two_difference_gap".
- <u>codependence (str, optional):</u> The codependence the assets are clustered on. The rank correlations depend
only on the order of the returns, so a few extreme returns weigh less; the
distance correlation and mutual information also capture non-linear co-movement.
Options are: "pearson" (the linear correlation of the covariance matrix),
"spearman" (the rank correlation of the returns, Spearman, 1904), "kendall" (the
rank correlation $$\tau_{b}$$ of the returns, Kendall, 1938), "gerber" (co-movements
beyond half a standard deviation, Gerber et al., 2022), "detoned" (the
correlation without the market component, López de Prado, 2020), "distance" (the
distance correlation, Székely et al., 2007, through √(1 - dCor)),
"mutual_information" (through the variation of information, Meilă, 2007),
"lower_tail" (how often two assets fall into their lowest 5% of returns
together, through -ln $$\lambda$$), "absolute_angular" ($$\vert \rho \vert$$ through $$\sqrt{1 - \vert \rho \vert}$$, López de
Prado, 2020), "squared_angular" ($$\rho^{2}$$ through $$\sqrt{1 - \rho^{2}}$$, López de Prado, 2020),
"gnpr" (the rank co-movement and the difference between the return
distributions, $$\theta = 0.5$$, Marti et al., 2016). Defaults to "pearson".
- <u>period (str, optional):</u> The frequency of the returns. Options are: "daily" (daily returns), "weekly"
(weekly returns), "monthly" (monthly returns), "quarterly" (quarterly returns), "yearly" (yearly
returns). Defaults to "daily".
- <u>covariance (str, optional):</u> The estimator of the covariance matrix, which also gives the correlations
that are clustered: "denoised" (the eigenvalues of the correlation matrix that random returns could
produce averaged, Laloux et al., 2000). Options are: "sample" (the sample covariance, ddof=1),
"ledoit_wolf" (shrunk towards the scaled identity, Ledoit and Wolf, 2004),
"ledoit_wolf_constant_correlation" (shrunk towards the average correlation, Ledoit and Wolf, 2004),
"ledoit_wolf_single_factor" (shrunk towards the covariance that the benchmark as a single factor
implies, Ledoit and Wolf, 2003), "oas" (Oracle Approximating Shrinkage, Chen et al., 2010), "shrunk"
(a fixed 10% towards the scaled identity), "semicovariance" (the co-movement below a zero return,
Estrada, 2008), "exponential" (exponentially weighted, recent periods weigh most, RiskMetrics),
"denoised" (the eigenvalues of the correlation matrix that random returns could produce averaged,
Laloux et al., 2000), "denoised_spectral" (those eigenvalues set to zero), "denoised_shrink" (the
noise correlations shrunk towards their diagonal, López de Prado, 2020), "gerber" (co-movements
beyond half a standard deviation, Gerber et al., 2022), "factor" (the covariance of the Fama and
French five factor model with OLS loadings, Fama and French, 1993), "minimum_covariance_determinant"
(the reweighted covariance of the half of the periods with the smallest covariance determinant,
robust to outliers, Rousseeuw and Van Driessen, 1999), "jlogo" (the sparse inverse covariance on the
TMFG planar graph of the correlations, Barfuss et al., 2016), "geodesic" (10% towards the scaled
identity along the geodesic of the positive definite matrices, Bhatia, 2007), "regime_adjusted_ew"
(exponentially weighted with a half-life of 40 periods, rescaled by the recent realized against
predicted risk, Paleologo, 2025), "nercome" (eigenvectors from one part of the periods and the
variances along them from the other, averaged over random splits, Lam, 2016), "ccc_garch" (the
next-period covariance of GARCH(1, 1) volatilities with constant correlations, Bollerslev, 1990),
"mm" (the robust MM-estimator, Maronna et al., 2019), "rocke" (Rocke's robust S-estimator, Maronna
et al., 2019). Defaults to "denoised".
- <u>covariance_span (int, optional):</u> The span in periods of the exponentially weighted covariance; the
weight of a period halves after about span / 2.9 periods. Defaults to 180.
- <u>expected_returns (str, optional):</u> The estimator of the expected returns of the "maximum_sharpe"
objective. Options are: "mean" (the historical average), "geometric" (the compounded average),
"exponential" (the exponentially weighted average, recent periods weigh most),
"exponential_geometric" (that average compounded over a year), "capm" (the returns the Capital Asset
Pricing Model implies from each asset's beta to the benchmark, Sharpe, 1964), "bayes_stein" (the
averages shrunk towards that of the minimum variance portfolio, Jorion, 1986), "james_stein" (the
averages shrunk towards their grand mean, James and Stein, 1961), "bodnar_okhrin_parolya" (the
averages and their grand mean combined with optimal weights, Bodnar, Okhrin and Parolya, 2019).
Defaults to "mean".
- <u>expected_returns_span (int, optional):</u> The span in periods of the exponentially weighted expected
returns. Defaults to 180.
- <u>risk_measure (str, optional):</u> The risk measure of the minimum variance and risk parity objectives (see
get_mean_risk_weights); the volatility gives the weights of the variance, and the maximum Sharpe
ratio takes the variance only. Options are: "variance" (of the covariance matrix), "volatility" (of
the covariance matrix), "mad" (mean absolute deviation, Konno and Yamazaki, 1991), "semideviation"
(below the minimum acceptable return), "lower_partial_moment" (first order), "worst_realization"
(the worst return), "gini_mean_difference" (Yitzhaki, 1982), "tail_gini" (Furman et al., 2017),
"range" (the best minus the worst return), "cvar_range" (the CVaR of the losses and of the gains),
"tail_gini_range" (the Tail Gini of the losses and of the gains), "ulcer_index" (of the uncompounded
cumulative return), "cvar" (Rockafellar and Uryasev, 2002), "cdar" (Chekhlov et al., 2005). Defaults
to "variance".
- <u>alpha (float, optional):</u> The tail probability of the CVaR, CDaR, CVaR
range and Tail Gini measures, e.g. 0.05 for the worst 5% of periods.
Defaults to 0.05.
- <u>minimum_acceptable_return (float &#124; str, optional):</u> The threshold of the semideviation and the lower
partial moment, as a return per period of the chosen frequency, or "mean" for each asset's average
return. Defaults to 0.
- <u>include_benchmark (bool, optional):</u> Whether to include the benchmark as an
asset. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per asset and for the portfolio, the Weight, Expected Return,
Volatility, Sharpe Ratio and Risk Contribution, with a risk measure of the
returns that measure per period (e.g. "MAD"), and the Cluster of every asset
(numbered from 1). Returns and volatilities are annualized.

**Notes:**

- Both levels are long only and fully invested. Weight, sector and country
bounds and a net or gross exposure do not apply: the weight of an asset is the
product of its weight within its cluster and the cluster's weight, from two
separate problems, so a bound on it is not a constraint either problem can
hold.
- With the maximum Sharpe ratio objective, a cluster without an asset whose expected
return exceeds the risk free rate holds its minimum variance portfolio. Across the
clusters, at least one cluster needs an expected return above it.
- The paper clusters with k-means and solves both levels without bounds,
allowing short positions. Here the clustering is hierarchical, as in HERC.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "JNJ", "XOM"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.portfolio.get_nested_clustered_optimization_weights()[
    ["Weight", "Volatility", "Sharpe Ratio", "Risk Contribution", "Cluster"]
]
```

Which returns:

|           |   Weight |   Volatility |   Sharpe Ratio |   Risk Contribution |   Cluster |
|:----------|---------:|-------------:|---------------:|--------------------:|----------:|
| AAPL      |   0.1081 |       0.2786 |         0.5725 |              0.1106 |         1 |
| MSFT      |   0.1388 |       0.2571 |         0.6534 |              0.1362 |         1 |
| JNJ       |   0.575  |       0.1673 |         0.3884 |              0.575  |         3 |
| XOM       |   0.1782 |       0.2702 |         0.9524 |              0.1782 |         2 |
| Portfolio |   1      |       0.1366 |         0.9061 |              1      |       nan |

---

## get_inverse_volatility_weights
Calculate inverse volatility weights: each asset's weight is proportional to one over its volatility, $$w_{i} = (1 / \sigma_{i}) / \sum (1 / \sigma_{j})$$.

It is the simplest risk-based allocation and equals risk parity when all correlations are the same.

**Also known as:** naive risk parity, volatility weighting.

**References:**

- library | Shares similar logic as skfolio's [InverseVolatility](https://skfolio.org/generated/skfolio.optimization.InverseVolatility.html){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The frequency of the returns. Options are: "daily" (daily returns), "weekly"
(weekly returns), "monthly" (monthly returns), "quarterly" (quarterly returns), "yearly" (yearly
returns). Defaults to "daily".
- <u>covariance (str, optional):</u> The estimator of the covariance matrix. The shrinkage and denoised
estimators stabilize the weights when there are many assets compared to the number of periods.
Options are: "sample" (the sample covariance, ddof=1), "ledoit_wolf" (shrunk towards the scaled
identity, Ledoit and Wolf, 2004), "ledoit_wolf_constant_correlation" (shrunk towards the average
correlation, Ledoit and Wolf, 2004), "ledoit_wolf_single_factor" (shrunk towards the covariance that
the benchmark as a single factor implies, Ledoit and Wolf, 2003), "oas" (Oracle Approximating
Shrinkage, Chen et al., 2010), "shrunk" (a fixed 10% towards the scaled identity), "semicovariance"
(the co-movement below a zero return, Estrada, 2008), "exponential" (exponentially weighted, recent
periods weigh most, RiskMetrics), "denoised" (the eigenvalues of the correlation matrix that random
returns could produce averaged, Laloux et al., 2000), "denoised_spectral" (those eigenvalues set to
zero), "denoised_shrink" (the noise correlations shrunk towards their diagonal, López de Prado,
2020), "gerber" (co-movements beyond half a standard deviation, Gerber et al., 2022), "factor" (the
covariance of the Fama and French five factor model with OLS loadings, Fama and French, 1993),
"minimum_covariance_determinant" (the reweighted covariance of the half of the periods with the
smallest covariance determinant, robust to outliers, Rousseeuw and Van Driessen, 1999), "jlogo" (the
sparse inverse covariance on the TMFG planar graph of the correlations, Barfuss et al., 2016),
"geodesic" (10% towards the scaled identity along the geodesic of the positive definite matrices,
Bhatia, 2007), "regime_adjusted_ew" (exponentially weighted with a half-life of 40 periods, rescaled
by the recent realized against predicted risk, Paleologo, 2025), "nercome" (eigenvectors from one
part of the periods and the variances along them from the other, averaged over random splits, Lam,
2016), "ccc_garch" (the next-period covariance of GARCH(1, 1) volatilities with constant
correlations, Bollerslev, 1990), "mm" (the robust MM-estimator, Maronna et al., 2019), "rocke"
(Rocke's robust S-estimator, Maronna et al., 2019). Defaults to "sample".
- <u>covariance_span (int, optional):</u> The span in periods of the exponentially weighted covariance; the
weight of a period halves after about span / 2.9 periods. Defaults to 180.
- <u>include_benchmark (bool, optional):</u> Whether to include the benchmark as an
asset. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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

## get_maximum_omega_weights
Calculate the weights of the portfolio with the highest Omega ratio over the historical returns: the gains above a minimum acceptable return divided by the losses below it.

The Omega ratio uses the whole return distribution instead of its mean and variance, so it rewards positive skew and penalizes fat left tails that a Sharpe ratio overlooks.

With $$\tau$$ the minimum acceptable return, $$\Omega (w) = 1 + (\bar{r}' w - \tau) / E [\max (0 , \tau - r_{t}' w)]$$. This ratio is maximized exactly as a linear programme with the Charnes-Cooper transformation: with $$y = \kappa w$$ and $$\kappa > 0$$, maximize $$\bar{r}' y - \tau \kappa$$ subject to $$\sum \max (0 , \tau \kappa - r_{t}' y) / T = 1$$ and the weight constraints, then $$w = y / \kappa$$.

**Also known as:** Omega optimization, maximum gain-loss ratio.

**References:**

- paper | Keating, C. and Shadwick, W. F. (2002). "A Universal Performance Measure." Journal of Performance Measurement, 6(3), 59-84.
- paper | Kapsos, M., Christofides, N. and Rustem, B. (2014). "Worst-Case Robust Omega Ratio." European Journal of Operational Research, 234(2), 499-507.
- library | Referenced against Riskfolio-Lib's [Portfolio.optimization](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/portfolio.html#Portfolio.Portfolio.optimization){:target="_blank"} (first lower partial moment)

**Args:**

- <u>minimum_acceptable_return (float, optional):</u> The threshold between gains and
losses, as a return per period of the chosen frequency (e.g. 0.0002 a day).
Defaults to 0.
- <u>period (str, optional):</u> The frequency of the returns. Options are: "daily" (daily returns), "weekly"
(weekly returns), "monthly" (monthly returns), "quarterly" (quarterly returns), "yearly" (yearly
returns). Defaults to "daily".
- <u>expected_returns (str, optional):</u> The estimator of the expected returns. Options are: "mean" (the
historical average), "geometric" (the compounded average), "exponential" (the exponentially weighted
average, recent periods weigh most), "exponential_geometric" (that average compounded over a year),
"capm" (the returns the Capital Asset Pricing Model implies from each asset's beta to the benchmark,
Sharpe, 1964), "bayes_stein" (the averages shrunk towards that of the minimum variance portfolio,
Jorion, 1986), "james_stein" (the averages shrunk towards their grand mean, James and Stein, 1961),
"bodnar_okhrin_parolya" (the averages and their grand mean combined with optimal weights, Bodnar,
Okhrin and Parolya, 2019). Defaults to "mean".
- <u>expected_returns_span (int, optional):</u> The span in periods of the exponentially weighted expected
returns. Defaults to 180.
- <u>minimum_weight (float &#124; dict[str, float], optional):</u> The lowest weight of
every asset, or per asset, e.g. {"AAPL": 0.05} (the others keep 0); a
negative value allows short positions. Defaults to 0.
- <u>maximum_weight (float &#124; dict[str, float], optional):</u> The highest weight of
every asset, or per asset, e.g. {"AAPL": 0.3} (the others keep 1).
Defaults to 1.
- <u>sector_bounds (dict[str, tuple[float, float]] &#124; None, optional):</u> The minimum
and maximum total weight per sector, e.g. {"Technology": (0, 0.4)}, with
the sector of each asset from its company profile. Defaults to None.
- <u>country_bounds (dict[str, tuple[float, float]] &#124; None, optional):</u> The minimum
and maximum total weight per country, named in full or by its two-letter
code, e.g. {"United States": (0, 0.6)}, with the country of each asset
from its company profile. Defaults to None.
- <u>net_exposure (float, optional):</u> The sum of the weights: 1 for a fully invested
portfolio, 0 for a market neutral one. The rest, 1 minus the net exposure,
is a Cash row at the risk free rate (negative when borrowed above one),
which the Portfolio's Expected Return and Sharpe Ratio include. Defaults to
1.
- <u>gross_exposure (float &#124; None, optional):</u> The highest sum of the absolute
weights, which limits the leverage of a long-short portfolio, e.g. 1.6 for
a 130/30 portfolio. Defaults to None, no limit.
- <u>current_weights (dict[str, float] &#124; None, optional):</u> The weights held now,
e.g. {"AAPL": 0.5, "MSFT": 0.5} (an asset left out is not held), which
the turnover is measured from; they add a Turnover column, $$\vert w_{i} - w_{0,i} \vert$$
per asset and its sum for the portfolio. Defaults to None, which uses
the latest weights of the Portfolio the Toolkit came from when a maximum
turnover needs them.
- <u>maximum_turnover (float &#124; None, optional):</u> The highest turnover
$$\sum \vert w_{i} - w_{0,i} \vert$$ from the current weights, e.g. 0.2 to trade at most 10%
of the portfolio each way. Defaults to None, no limit.
- <u>include_benchmark (bool, optional):</u> Whether to include the benchmark as an
asset. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per asset and for the portfolio, the Weight, Expected Return,
Volatility, Sharpe Ratio and Risk Contribution, with the Omega Ratio of every
asset on its own and of the portfolio.

**Notes:**

- Some portfolio within the constraints needs an average return above the minimum
acceptable return; otherwise no Omega ratio is above one and the method returns
an error that says so.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "JNJ", "XOM"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.portfolio.get_maximum_omega_weights()[
    ["Weight", "Expected Return", "Volatility", "Risk Contribution", "Omega Ratio"]
]
```

Which returns:

|           |   Weight |   Expected Return |   Volatility |   Risk Contribution |   Omega Ratio |
|:----------|---------:|------------------:|-------------:|--------------------:|--------------:|
| AAPL      |   0.0594 |            0.1932 |       0.2786 |              0.0615 |        1.1306 |
| MSFT      |   0.2822 |            0.2017 |       0.2571 |              0.2875 |        1.1459 |
| JNJ       |   0.2697 |            0.0987 |       0.1673 |              0.1258 |        1.1083 |
| XOM       |   0.3887 |            0.2911 |       0.2702 |              0.5251 |        1.1954 |
| Portfolio |   1      |            0.2082 |       0.1551 |              1      |        1.2567 |

---

## get_mean_risk_weights
Calculate the weights of a mean-risk portfolio with a risk measure other than the volatility.

It is the portfolio with the lowest risk, the lowest risk at a target return, or the highest ratio of the average excess return to the risk.

The risk is measured on the historical returns, so measures that only count losses (the semideviation, the lower partial moment, the worst realization, the CVaR, the Tail Gini) leave upside swings unpenalized, and the Ulcer Index and the drawdown measures penalize deep and long drawdowns, which are what investors feel and what ends strategies. The minimum CVaR portfolio only looks at the losses in the tail, so it accounts for skewed and fat-tailed returns; its maximum ratio portfolio is the maximum STARR (CVaR ratio) portfolio of Martin, Rachev and Siboulet (2003), the maximum Sharpe ratio portfolio with the tail loss in place of the volatility.

The risk measures $$\rho (w)$$ of the portfolio's returns $$X_{t} = r_{t}' w$$ over T periods, with $$\alpha$$ the tail probability and $$\tau$$ the minimum acceptable return, are:

- The mean absolute deviation $$\sum \vert X_{t} - \bar{X} \vert / T$$ (Konno and Yamazaki, 1991).
- The semideviation: $$\sqrt{\sum \min (X_{t} - \tau , 0)^{2} / T}$$, or $$\sqrt{\sum \min (X_{t} - \bar{X} , 0)^{2} / (T - 1)}$$ below the mean (Markowitz, 1959; Estrada, 2008).
- The first lower partial moment $$\sum \max (\tau - X_{t} , 0) / T$$ (Bawa, 1975), or below each asset's mean.
- The worst realization: the largest loss -min $$X_{t}$$ (Young, 1998).
- The Gini mean difference: the average absolute difference between the returns of two periods, $$\sum_{i} \sum_{j} \vert X_{i} - X_{j} \vert / (T (T - 1))$$ (Yitzhaki, 1982).
- The Tail Gini: the Tail Gini of the losses beyond the $$\alpha$$ quantile (Furman, Wang and Zitikis, 2017; Cajas, 2021).
- The range: the largest gain plus the largest loss, $$\max X_{t} - \min X_{t}$$.
- The CVaR range: the CVaR of the losses plus that of the gains, the average of the best $$\alpha$$ share of the returns minus the average of the worst (Cajas, 2021).
- The Tail Gini range: the Tail Gini of the losses plus that of the gains.
- The Ulcer Index: $$\sqrt{\sum D_{t}^{2} / T}$$ with $$D_{t}$$ the drawdowns of the uncompounded cumulative return (Martin and McCann, 1989).
- The Conditional Value at Risk, the average loss in the worst $$\alpha$$ share of the periods, $$\text{VaR} + \sum \max (0 , - X_{t} - \text{VaR}) / (\alpha T)$$ at its minimum over the VaR (Rockafellar and Uryasev, 2000).
- The Conditional Drawdown at Risk, the average of the worst $$\alpha$$ share of the drawdowns $$D_{t}$$, $$\zeta + \sum \max (0 , D_{t} - \zeta) / (\alpha T)$$ at its minimum over $$\zeta$$ (Chekhlov, Uryasev and Zabarankin, 2005).
- The maximum drawdown: the largest drawdown $$\max D_{t}$$.
- The average drawdown $$\sum D_{t} / T$$.

The drawdowns $$D_{t} = u_{t} - Y_{t}$$ are those of the uncompounded cumulative return $$Y_{t} = \sum_{s \leq t} X_{s}$$ below its running peak $$u_{t} = \max (0 , \max_{s \leq t} Y_{s})$$, from $$u_{0} = 0$$.

The objectives are:

$$
\text{The minimum risk:}\;\; \text{minimize } \rho (w),\;\; \text{at the target return}\; \mu' w = \text{target when given}
$$

$$
\text{The maximum ratio:}\;\; \frac{\text{maximize} \;(\mu - r_{f}) \;\text{'w}}{\rho(w)} \;\text{with the Charnes-Cooper transformation}\; y = \kappa w,\;\; \kappa > 0 \;(\text{Charnes and Cooper},\; 1962) \;\text{:} \;\text{maximize} \;(\mu - r_{f}) \;\text{'y} \;\text{subject to} \;\rho(y) \leq 1 \;\text{and the weight constraints},\;\; \text{then}\; w = \frac{y}{\kappa}
$$

The mean absolute deviation, the lower partial moment, the worst realization, the ranges, the CVaR range, the CVaR and the drawdown measures are solved exactly as linear programmes with HiGHS. The Gini mean difference and the Tail Gini measures are ordered weighted averages of the sorted returns, convex because their weights rise with the rank (Cajas, 2021), and are solved exactly with cutting planes (Kelley, 1960) stabilized as in Ben-Ameur and Neto (2007): every sorted order of the returns gives a linear lower bound of the measure, which is added where the linear programme's solution needs it. The semideviation and the Ulcer Index have continuous gradients and are minimized with SLSQP.

**Also known as:** mean-MAD, mean-semivariance, minimax, mean-Gini, mean-Ulcer, Sortino-optimal or Gini-optimal portfolio, minimum CVaR weights, minimum expected shortfall portfolio, mean-CVaR, tail risk optimization, maximum CVaR ratio weights, maximum STARR, stable tail adjusted return ratio, maximum return-to-CVaR, mean-CVaR tangency portfolio, minimum drawdown weights, minimum CDaR, minimum maximum drawdown, minimum average drawdown, drawdown optimization.

**References:**

- paper | Konno, H. and Yamazaki, H. (1991). "Mean-Absolute Deviation Portfolio Optimization Model and Its Applications to Tokyo Stock Market." Management Science, 37(5), 519-531.
- paper | Markowitz, H. (1959). "Portfolio Selection: Efficient Diversification of Investments." John Wiley & Sons, New York.
- paper | Estrada, J. (2008). "Mean-Semivariance Optimization: A Heuristic Approach." Journal of Applied Finance, 18(1), 57-72.
- paper | Bawa, V. S. (1975). "Optimal Rules for Ordering Uncertain Prospects." Journal of Financial Economics, 2(1), 95-121.
- paper | Young, M. R. (1998). "A Minimax Portfolio Selection Rule with Linear Programming Solution." Management Science, 44(5), 673-683.
- paper | Yitzhaki, S. (1982). "Stochastic Dominance, Mean Variance, and Gini's Mean Difference." The American Economic Review, 72(1), 178-185.
- paper | Furman, E., Wang, R. and Zitikis, R. (2017). "Gini-Type Measures of Risk and Variability: Gini Shortfall, Capital Allocations, and Heavy-Tailed Risks." Journal of Banking & Finance, 83, 70-84.
- paper | Cajas, D. (2021). "OWA Portfolio Optimization: A Disciplined Convex Programming Framework." SSRN Working Paper 3988927.
- paper | Martin, P. G. and McCann, B. B. (1989). "The Investor's Guide to Fidelity Funds." John Wiley & Sons, New York.
- paper | Rockafellar, R. T. and Uryasev, S. (2000). "Optimization of Conditional Value-at-Risk." Journal of Risk, 2(3), 21-41.
- paper | Martin, R. D., Rachev, S. T. and Siboulet, F. (2003). "Phi-Alpha Optimal Portfolios and Extreme Risk Management." Wilmott Magazine, November, 70-83.
- paper | Chekhlov, A., Uryasev, S. and Zabarankin, M. (2005). "Drawdown Measure in Portfolio Optimization." International Journal of Theoretical and Applied Finance, 8(1), 13-58.
- paper | Charnes, A. and Cooper, W. W. (1962). "Programming with Linear Fractional Functionals." Naval Research Logistics Quarterly, 9(3-4), 181-186.
- paper | Kelley, J. E. (1960). "The Cutting-Plane Method for Solving Convex Programs." Journal of the Society for Industrial and Applied Mathematics, 8(4), 703-712.
- paper | Ben-Ameur, W. and Neto, J. (2007). "Acceleration of Cutting-Plane and Column Generation Algorithms: Applications to Network Design." Networks, 49(1), 3-17.
- library | Referenced against skfolio's [MeanRisk](https://skfolio.org/generated/skfolio.optimization.MeanRisk.html){:target="_blank"}
- library | Referenced against Riskfolio-Lib's [Portfolio.optimization](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/portfolio.html#Portfolio.Portfolio.optimization){:target="_blank"}
- library | Referenced against Riskfolio-Lib's [Portfolio.owa_optimization](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/portfolio.html#Portfolio.Portfolio.owa_optimization){:target="_blank"} (Tail Gini)

**Args:**

- <u>risk_measure (str, optional):</u> The risk measure. Options are: "mad" (mean absolute deviation, Konno and
Yamazaki, 1991), "semideviation" (below the minimum acceptable return), "lower_partial_moment"
(first order), "worst_realization" (the worst return), "gini_mean_difference" (Yitzhaki, 1982),
"tail_gini" (Furman et al., 2017), "range" (the best minus the worst return), "cvar_range" (the CVaR
of the losses and of the gains), "tail_gini_range" (the Tail Gini of the losses and of the gains),
"ulcer_index" (of the uncompounded cumulative return), "cvar" (Rockafellar and Uryasev, 2002),
"cdar" (Chekhlov et al., 2005), "maximum_drawdown" (of the uncompounded cumulative return),
"average_drawdown" (of the uncompounded cumulative return). Defaults to "mad".
- <u>objective (str, optional):</u> Options are: "minimum_risk" (the lowest risk), "maximum_ratio" (the highest
average excess return per unit of risk). Defaults to "minimum_risk".
- <u>target_return (float &#124; None, optional):</u> The annualized expected return the
minimum risk portfolio must have, e.g. 0.12 for 12%, with the cash of a
net exposure other than one at the risk free rate. Defaults to None,
no target.
- <u>alpha (float, optional):</u> The tail probability of the CVaR, the CVaR
range, the CDaR and the Tail Gini measures, e.g. 0.05 for the worst 5% of
periods (or drawdowns). Defaults to 0.05.
- <u>minimum_acceptable_return (float &#124; str, optional):</u> The threshold of the semideviation and the lower
partial moment, as a return per period of the chosen frequency (e.g. 0.0002 a day), or "mean" for
each asset's average return. Defaults to 0.
- <u>period (str, optional):</u> The frequency of the returns. Options are: "daily" (daily returns), "weekly"
(weekly returns), "monthly" (monthly returns), "quarterly" (quarterly returns), "yearly" (yearly
returns). Defaults to "daily".
- <u>expected_returns (str, optional):</u> The estimator of the expected returns of the ratio and the target
return. Options are: "mean" (the historical average), "geometric" (the compounded average),
"exponential" (the exponentially weighted average, recent periods weigh most),
"exponential_geometric" (that average compounded over a year), "capm" (the returns the Capital Asset
Pricing Model implies from each asset's beta to the benchmark, Sharpe, 1964), "bayes_stein" (the
averages shrunk towards that of the minimum variance portfolio, Jorion, 1986), "james_stein" (the
averages shrunk towards their grand mean, James and Stein, 1961), "bodnar_okhrin_parolya" (the
averages and their grand mean combined with optimal weights, Bodnar, Okhrin and Parolya, 2019).
Defaults to "mean".
- <u>expected_returns_span (int, optional):</u> The span in periods of the exponentially weighted expected
returns. Defaults to 180.
- <u>minimum_weight (float &#124; dict[str, float], optional):</u> The lowest weight of
every asset, or per asset, e.g. {"AAPL": 0.05} (the others keep 0); a
negative value allows short positions. Defaults to 0.
- <u>maximum_weight (float &#124; dict[str, float], optional):</u> The highest weight of
every asset, or per asset, e.g. {"AAPL": 0.3} (the others keep 1).
Defaults to 1.
- <u>sector_bounds (dict[str, tuple[float, float]] &#124; None, optional):</u> The minimum
and maximum total weight per sector, e.g. {"Technology": (0, 0.4)}, with
the sector of each asset from its company profile. Defaults to None.
- <u>country_bounds (dict[str, tuple[float, float]] &#124; None, optional):</u> The minimum
and maximum total weight per country, named in full or by its two-letter
code, e.g. {"United States": (0, 0.6)}, with the country of each asset
from its company profile. Defaults to None.
- <u>net_exposure (float, optional):</u> The sum of the weights: 1 for a fully invested
portfolio, 0 for a market neutral one (which needs a negative
minimum_weight). At 0 the portfolio with the lowest CVaR holds nothing, so
all weights are 0, and for the drawdown measures a net exposure of 0 is
refused, as holding nothing has no drawdown. The rest, 1 minus the net
exposure, is a Cash row at the risk free rate (negative when borrowed above
one), which the Portfolio's Expected Return and Sharpe Ratio include.
Defaults to 1.
- <u>gross_exposure (float &#124; None, optional):</u> The highest sum of the absolute
weights, which limits the leverage of a long-short portfolio, e.g. 1.6 for
a 130/30 portfolio. Defaults to None, no limit.
- <u>current_weights (dict[str, float] &#124; None, optional):</u> The weights held now,
e.g. {"AAPL": 0.5, "MSFT": 0.5} (an asset left out is not held), which
the turnover is measured from; they add a Turnover column, $$\vert w_{i} - w_{0,i} \vert$$
per asset and its sum for the portfolio. Defaults to None, which uses
the latest weights of the Portfolio the Toolkit came from when a maximum
turnover needs them.
- <u>maximum_turnover (float &#124; None, optional):</u> The highest turnover
$$\sum \vert w_{i} - w_{0,i} \vert$$ from the current weights, e.g. 0.2 to trade at most 10%
of the portfolio each way. Defaults to None, no limit.
- <u>include_benchmark (bool, optional):</u> Whether to include the benchmark as an
asset. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per asset and for the portfolio, the Weight, Expected Return,
Volatility, Sharpe Ratio and Risk Contribution (of the volatility), with the
risk measure (per period, positive for a loss, named after it, e.g. "MAD")
and its ratio (the average excess return per period over the measure, e.g.
"MAD Ratio") of every asset on its own and of the portfolio.

**Notes:**

- The risk measures are per period of the chosen frequency and not annualized;
the drawdowns of the Ulcer Index, the CDaR and the maximum and average drawdown
are those of the uncompounded cumulative return (the sum of the returns, as in
Chekhlov, Uryasev and Zabarankin), which scales with the weights and keeps the
problem linear, as in Riskfolio-Lib and skfolio: they are absolute drawdowns of
a portfolio that keeps its invested amount constant. The compounded drawdowns
of the risk module, relative to the peak value, are close for small drawdowns
and smaller for large ones.
- The CVaR and the CDaR are the values the linear programmes minimize: the average
of the worst $$\alpha$$ share of the periods (or drawdowns), with a fraction of the
boundary period when $$\alpha T$$ is not a whole number (Rockafellar and Uryasev,
2002), as in the expected shortfall contributions.
- Riskfolio-Lib's MAD is half of the mean absolute deviation and its lower partial
moments divide by T - 1, and skfolio's lower partial moment is below the mean;
those scale the measure but leave the weights the same. The Gini mean
difference here is that of the Risk module, $$\sum_{i} \sum_{j} \vert X_{i} - X_{j} \vert / (T (T - 1))$$.
- The risk free rate is the Toolkit's, averaged over the returns and converted to
a rate per period. For the maximum ratio, some portfolio within the constraints
needs an average return above it; otherwise the method returns an error that
says so.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "JNJ", "XOM"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.portfolio.get_mean_risk_weights(
    risk_measure="gini_mean_difference", objective="maximum_ratio"
)[["Weight", "Expected Return", "Gini Mean Difference", "Gini Mean Difference Ratio"]]
```

Which returns:

|           |   Weight |   Expected Return |   Gini Mean Difference |   Gini Mean Difference Ratio |
|:----------|---------:|------------------:|-----------------------:|-----------------------------:|
| AAPL      |   0.0562 |            0.1932 |                 0.0185 |                       0.0342 |
| MSFT      |   0.307  |            0.2017 |                 0.0174 |                       0.0384 |
| JNJ       |   0.1846 |            0.0987 |                 0.0112 |                       0.0231 |
| XOM       |   0.4521 |            0.2911 |                 0.0187 |                       0.0545 |
| Portfolio |   1      |            0.2226 |                 0.0113 |                       0.0662 |

---

## get_critical_line_weights
Calculate the corner portfolios of the efficient frontier with the critical line algorithm of Markowitz (1956).

These are the exact points where an asset enters or leaves the portfolio. Between two neighbouring corners the efficient weights move along a straight line, so the corners describe the whole long-only (or bounded) frontier without a grid of target returns. The minimum variance portfolio (the last corner) and the maximum Sharpe ratio portfolio follow from them exactly.

Every efficient portfolio minimizes ½ $$w' \Sigma w - \lambda \mu' w$$ subject to the weights summing to one and lying between their bounds, for some $$\lambda \geq 0$$, the risk tolerance (the inverse of the risk aversion). The algorithm starts at the portfolio with the highest expected return ($$\lambda$$ = ∞) and lowers $$\lambda$$. For the assets strictly between their bounds (the free assets F, the others B are at a bound) the first-order conditions are a linear system:

$$
\Sigma_{\text{FF}} w_{F} + \gamma 1 = \lambda \mu_{F} - \Sigma_{\text{FB}} w_{B}
$$

$$
\text{1'w}_{F} = 1 - \text{1'w}_{B}
$$

so the weights are affine in $$\lambda$$ until a free asset reaches a bound or the gradient $$(\Sigma w)_{j} - \lambda \mu_{j} + \gamma$$ of a bound asset changes sign, which frees it. That $$\lambda$$ is a corner. On the line between two corners the Sharpe ratio has a single stationary point, which gives the maximum Sharpe ratio portfolio in closed form.

**Also known as:** CLA, corner portfolios, turning points of the efficient frontier.

**References:**

- paper | Markowitz, H. (1956). "The Optimization of a Quadratic Function Subject to Linear Constraints." Naval Research Logistics Quarterly, 3(1-2), 111-133.
- paper | Bailey, D. H. and López de Prado, M. (2013). "An Open-Source Implementation of the Critical-Line Algorithm for Portfolio Optimization." Algorithms, 6(1), 169-196.
- library | Referenced against PyPortfolioOpt's [CLA](https://pyportfolioopt.readthedocs.io/en/latest/OtherOptimizers.html#pypfopt.cla.CLA){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The frequency of the returns. Options are: "daily" (daily returns), "weekly"
(weekly returns), "monthly" (monthly returns), "quarterly" (quarterly returns), "yearly" (yearly
returns). Defaults to "daily".
- <u>covariance (str, optional):</u> The estimator of the covariance matrix. Options are: "sample" (the sample
covariance, ddof=1), "ledoit_wolf" (shrunk towards the scaled identity, Ledoit and Wolf, 2004),
"ledoit_wolf_constant_correlation" (shrunk towards the average correlation, Ledoit and Wolf, 2004),
"ledoit_wolf_single_factor" (shrunk towards the covariance that the benchmark as a single factor
implies, Ledoit and Wolf, 2003), "oas" (Oracle Approximating Shrinkage, Chen et al., 2010), "shrunk"
(a fixed 10% towards the scaled identity), "semicovariance" (the co-movement below a zero return,
Estrada, 2008), "exponential" (exponentially weighted, recent periods weigh most, RiskMetrics),
"denoised" (the eigenvalues of the correlation matrix that random returns could produce averaged,
Laloux et al., 2000), "denoised_spectral" (those eigenvalues set to zero), "denoised_shrink" (the
noise correlations shrunk towards their diagonal, López de Prado, 2020), "gerber" (co-movements
beyond half a standard deviation, Gerber et al., 2022), "factor" (the covariance of the Fama and
French five factor model with OLS loadings, Fama and French, 1993), "minimum_covariance_determinant"
(the reweighted covariance of the half of the periods with the smallest covariance determinant,
robust to outliers, Rousseeuw and Van Driessen, 1999), "jlogo" (the sparse inverse covariance on the
TMFG planar graph of the correlations, Barfuss et al., 2016), "geodesic" (10% towards the scaled
identity along the geodesic of the positive definite matrices, Bhatia, 2007), "regime_adjusted_ew"
(exponentially weighted with a half-life of 40 periods, rescaled by the recent realized against
predicted risk, Paleologo, 2025), "nercome" (eigenvectors from one part of the periods and the
variances along them from the other, averaged over random splits, Lam, 2016), "ccc_garch" (the
next-period covariance of GARCH(1, 1) volatilities with constant correlations, Bollerslev, 1990),
"mm" (the robust MM-estimator, Maronna et al., 2019), "rocke" (Rocke's robust S-estimator, Maronna
et al., 2019). Defaults to "sample".
- <u>covariance_span (int, optional):</u> The span in periods of the exponentially weighted covariance; the
weight of a period halves after about span / 2.9 periods. Defaults to 180.
- <u>expected_returns (str, optional):</u> The estimator of the expected returns. Options are: "mean" (the
historical average), "geometric" (the compounded average), "exponential" (the exponentially weighted
average, recent periods weigh most), "exponential_geometric" (that average compounded over a year),
"capm" (the returns the Capital Asset Pricing Model implies from each asset's beta to the benchmark,
Sharpe, 1964), "bayes_stein" (the averages shrunk towards that of the minimum variance portfolio,
Jorion, 1986), "james_stein" (the averages shrunk towards their grand mean, James and Stein, 1961),
"bodnar_okhrin_parolya" (the averages and their grand mean combined with optimal weights, Bodnar,
Okhrin and Parolya, 2019). Defaults to "mean".
- <u>expected_returns_span (int, optional):</u> The span in periods of the exponentially weighted expected
returns. Defaults to 180.
- <u>minimum_weight (float &#124; dict[str, float], optional):</u> The lowest weight of
every asset, or per asset, e.g. {"AAPL": 0.05} (the others keep 0); a
negative value allows short positions. Defaults to 0.
- <u>maximum_weight (float &#124; dict[str, float], optional):</u> The highest weight of
every asset, or per asset, e.g. {"AAPL": 0.3} (the others keep 1).
Defaults to 1.
- <u>include_benchmark (bool, optional):</u> Whether to include the benchmark as an
asset. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: One row per corner portfolio, from "Corner 1" (the highest
expected return) to the minimum variance portfolio, followed by the "Minimum
Variance" and "Maximum Sharpe" portfolios, each with its Lambda (the risk
tolerance $$\lambda$$ at which it is optimal), the annualized Expected Return,
Volatility and Sharpe Ratio and the weight per asset.

**Notes:**

- The critical line algorithm takes the weight bounds and the budget only; for
sector, country, gross exposure or turnover constraints use
get_efficient_frontier, which solves each target return numerically.
- $$\lambda$$ is in the units of the annualized expected returns and covariance. The first
corner is optimal for every $$\lambda$$ at or above its own, and the last one, at $$\lambda = 0$$,
is the minimum variance portfolio, so it is listed twice.
- PyPortfolioOpt's CLA lists the first portfolio twice (at $$\lambda$$ = ∞ and at the first
corner); here it appears once.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "JNJ", "XOM"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.portfolio.get_critical_line_weights().drop(columns="Sharpe Ratio")
```

Which returns:

| Portfolio        |   Lambda |   Expected Return |   Volatility |   AAPL |   MSFT |    JNJ |    XOM |
|:-----------------|---------:|------------------:|-------------:|-------:|-------:|-------:|-------:|
| Corner 1         |   0.7508 |            0.2911 |       0.2702 | 0      | 0      | 0      | 1      |
| Corner 2         |   0.2405 |            0.2591 |       0.2031 | 0      | 0.3583 | 0      | 0.6417 |
| Corner 3         |   0.224  |            0.2578 |       0.2016 | 0.0103 | 0.3619 | 0      | 0.6278 |
| Corner 4         |   0      |            0.1577 |       0.135  | 0.0211 | 0.2167 | 0.5821 | 0.1801 |
| Minimum Variance |   0      |            0.1577 |       0.135  | 0.0211 | 0.2167 | 0.5821 | 0.1801 |
| Maximum Sharpe   |   0.147  |            0.2234 |       0.167  | 0.014  | 0.312  | 0.2    | 0.474  |

---

## get_worst_case_mean_variance_weights
Calculate the weights of a worst-case (robust) mean-variance portfolio.

It is the portfolio that is optimal for the least favourable expected returns within a confidence region around the estimates, instead of for the estimates themselves. The expected returns are the noisiest input of a mean-variance optimization, and the worst case penalizes the portfolios whose return rests most on them.

With $$\mu$$ the annualized expected returns, $$\Sigma$$ the annualized covariance matrix, $$\sum_{\mu} = \Sigma$$ × (periods per year) / T the covariance of the annualized average over T periods and $$\alpha$$ the confidence level, the worst-case return R(w) is:

$$
\text{An ellipsoid:}\;\; \mu' w - \kappa \sqrt{w' \Sigma_{\mu} w} \;\text{with}\; \kappa^{2} = \chi_{n}^{2}(\alpha),\;\; \text{the lowest return over the joint confidence ellipsoid of the } n \text{ expected returns (Goldfarb and Iyengar, 2003)}
$$

$$
\text{A box:}\;\; \mu' w - \delta' \left|w\right| \;\text{with}\; \delta_{i} = \frac{z_{1+\alpha}}{2 \sqrt{\Sigma_{\mu},\; \text{ii}}},\;\; \text{the lowest return when each expected return can lie anywhere in its own confidence interval (Tütüncü and Koenig, 2004)}
$$

The objectives replace the expected return $$\mu' w$$ by R(w):

- The maximum Sharpe ratio: maximize $$(R (w) - r_{f}) / \sqrt{w' \Sigma w}$$, solved with the Charnes-Cooper transformation (Charnes and Cooper, 1962).
- The utility: maximize $$R (w) - (\lambda / 2) w' \Sigma w$$ with $$\lambda$$ the risk aversion.
- The minimum variance: minimize $$w' \Sigma w$$ subject to R(w) ≥ the target return.

R(w) is concave, so every objective is a convex problem, solved with SLSQP.

**Also known as:** robust mean-variance, robust Markowitz, max-min portfolio, uncertainty set optimization.

**References:**

- paper | Goldfarb, D. and Iyengar, G. (2003). "Robust Portfolio Selection Problems." Mathematics of Operations Research, 28(1), 1-38.
- paper | Tütüncü, R. H. and Koenig, M. (2004). "Robust Asset Allocation." Annals of Operations Research, 132, 157-187.
- paper | Charnes, A. and Cooper, W. W. (1962). "Programming with Linear Fractional Functionals." Naval Research Logistics Quarterly, 9(3-4), 181-186.
- library | Referenced against Riskfolio-Lib's [Portfolio.wc_optimization](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/portfolio.html#Portfolio.Portfolio.wc_optimization){:target="_blank"} (box)
- library | Referenced against skfolio's [MeanRisk](https://skfolio.org/generated/skfolio.optimization.MeanRisk.html){:target="_blank"} (with an EmpiricalMuUncertaintySet)

**Args:**

- <u>uncertainty (str, optional):</u> The uncertainty set of the expected returns. Options are: "box" (a
confidence interval per estimate), "ellipsoid" (the joint confidence region). Defaults to "box".
- <u>confidence_level (float, optional):</u> The confidence level of the uncertainty
set, e.g. 0.95. A higher level widens the set and gives more cautious
weights. Defaults to 0.95.
- <u>objective (str, optional):</u> Options are: "maximum_sharpe" (the highest worst-case Sharpe ratio),
"utility" (the highest worst-case utility), "minimum_variance" (the lowest variance, which needs a
target return). Defaults to "maximum_sharpe".
- <u>risk_aversion (float, optional):</u> The risk aversion $$\lambda$$ of the utility; higher
values give less risky portfolios. Defaults to 2.5.
- <u>target_return (float &#124; None, optional):</u> The lowest annualized worst-case
return of the minimum variance objective, e.g. 0.1 for 10%, with the cash
of a net exposure other than one at the risk free rate. Defaults to
None.
- <u>period (str, optional):</u> The frequency of the returns. Options are: "daily" (daily returns), "weekly"
(weekly returns), "monthly" (monthly returns), "quarterly" (quarterly returns), "yearly" (yearly
returns). Defaults to "daily".
- <u>covariance (str, optional):</u> The estimator of the covariance matrix, as in get_maximum_sharpe_weights.
Options are: "sample" (the sample covariance, ddof=1), "ledoit_wolf" (shrunk towards the scaled
identity, Ledoit and Wolf, 2004), "ledoit_wolf_constant_correlation" (shrunk towards the average
correlation, Ledoit and Wolf, 2004), "ledoit_wolf_single_factor" (shrunk towards the covariance that
the benchmark as a single factor implies, Ledoit and Wolf, 2003), "oas" (Oracle Approximating
Shrinkage, Chen et al., 2010), "shrunk" (a fixed 10% towards the scaled identity), "semicovariance"
(the co-movement below a zero return, Estrada, 2008), "exponential" (exponentially weighted, recent
periods weigh most, RiskMetrics), "denoised" (the eigenvalues of the correlation matrix that random
returns could produce averaged, Laloux et al., 2000), "denoised_spectral" (those eigenvalues set to
zero), "denoised_shrink" (the noise correlations shrunk towards their diagonal, López de Prado,
2020), "gerber" (co-movements beyond half a standard deviation, Gerber et al., 2022), "factor" (the
covariance of the Fama and French five factor model with OLS loadings, Fama and French, 1993),
"minimum_covariance_determinant" (the reweighted covariance of the half of the periods with the
smallest covariance determinant, robust to outliers, Rousseeuw and Van Driessen, 1999), "jlogo" (the
sparse inverse covariance on the TMFG planar graph of the correlations, Barfuss et al., 2016),
"geodesic" (10% towards the scaled identity along the geodesic of the positive definite matrices,
Bhatia, 2007), "regime_adjusted_ew" (exponentially weighted with a half-life of 40 periods, rescaled
by the recent realized against predicted risk, Paleologo, 2025), "nercome" (eigenvectors from one
part of the periods and the variances along them from the other, averaged over random splits, Lam,
2016), "ccc_garch" (the next-period covariance of GARCH(1, 1) volatilities with constant
correlations, Bollerslev, 1990), "mm" (the robust MM-estimator, Maronna et al., 2019), "rocke"
(Rocke's robust S-estimator, Maronna et al., 2019). Defaults to "sample".
- <u>covariance_span (int, optional):</u> The span in periods of the exponentially weighted covariance; the
weight of a period halves after about span / 2.9 periods. Defaults to 180.
- <u>expected_returns (str, optional):</u> The estimator of the expected returns, as in
get_maximum_sharpe_weights. Options are: "mean" (the historical average), "geometric" (the
compounded average), "exponential" (the exponentially weighted average, recent periods weigh most),
"exponential_geometric" (that average compounded over a year), "capm" (the returns the Capital Asset
Pricing Model implies from each asset's beta to the benchmark, Sharpe, 1964), "bayes_stein" (the
averages shrunk towards that of the minimum variance portfolio, Jorion, 1986), "james_stein" (the
averages shrunk towards their grand mean, James and Stein, 1961), "bodnar_okhrin_parolya" (the
averages and their grand mean combined with optimal weights, Bodnar, Okhrin and Parolya, 2019).
Defaults to "mean".
- <u>expected_returns_span (int, optional):</u> The span in periods of the exponentially weighted expected
returns. Defaults to 180.
- <u>minimum_weight (float &#124; dict[str, float], optional):</u> The lowest weight of
every asset, or per asset, e.g. {"AAPL": 0.05} (the others keep 0); a
negative value allows short positions. Defaults to 0.
- <u>maximum_weight (float &#124; dict[str, float], optional):</u> The highest weight of
every asset, or per asset, e.g. {"AAPL": 0.3} (the others keep 1).
Defaults to 1.
- <u>sector_bounds (dict[str, tuple[float, float]] &#124; None, optional):</u> The minimum
and maximum total weight per sector, e.g. {"Technology": (0, 0.4)}, with
the sector of each asset from its company profile. Defaults to None.
- <u>country_bounds (dict[str, tuple[float, float]] &#124; None, optional):</u> The minimum
and maximum total weight per country, named in full or by its two-letter
code, e.g. {"United States": (0, 0.6)}, with the country of each asset
from its company profile. Defaults to None.
- <u>net_exposure (float, optional):</u> The sum of the weights: 1 for a fully invested
portfolio. The rest, 1 minus the net exposure, is a Cash row at the risk
free rate (negative when borrowed above one), which the Portfolio's Expected
Return and Sharpe Ratio include. Defaults to 1.
- <u>gross_exposure (float &#124; None, optional):</u> The highest sum of the absolute
weights, which limits the leverage of a long-short portfolio, e.g. 1.6 for
a 130/30 portfolio. Defaults to None, no limit.
- <u>current_weights (dict[str, float] &#124; None, optional):</u> The weights held now,
e.g. {"AAPL": 0.5, "MSFT": 0.5} (an asset left out is not held), which
the turnover is measured from; they add a Turnover column, $$\vert w_{i} - w_{0,i} \vert$$
per asset and its sum for the portfolio. Defaults to None, which uses
the latest weights of the Portfolio the Toolkit came from when a maximum
turnover needs them.
- <u>maximum_turnover (float &#124; None, optional):</u> The highest turnover
$$\sum \vert w_{i} - w_{0,i} \vert$$ from the current weights, e.g. 0.2 to trade at most 10%
of the portfolio each way. Defaults to None, no limit.
- <u>include_benchmark (bool, optional):</u> Whether to include the benchmark as an
asset. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per asset and for the portfolio, the Weight, Expected Return,
Volatility, Sharpe Ratio and Risk Contribution, with the Worst-Case Return
and the Worst-Case Sharpe Ratio of every asset on its own and of the
portfolio. Returns and volatilities are annualized.

**Notes:**

- Only the uncertainty of the expected returns is modelled. Uncertainty sets on
the covariance matrix (as in Riskfolio-Lib's worst-case optimization) need
semidefinite programming, which is not available with SciPy's solvers.
- $$\sum_{\mu} = \Sigma / T$$ is the covariance of the historical average. For the other
expected return estimators it is an approximation of their uncertainty.
- The box of each expected return is its own two-sided confidence interval
from the normal distribution. Riskfolio-Lib estimates its box and ellipsoid
by bootstrapping by default; with the same $$\delta$$, $$\sum_{\mu}$$ and $$\kappa$$ the weights agree.
- skfolio's EmpiricalMuUncertaintySet uses only the variances of $$\sum_{\mu}$$ by default;
the full $$\sum_{\mu}$$ here equals its full-matrix option.
- With the ellipsoid, $$\sum_{\mu} = \Sigma$$ × (periods per year) / T is proportional to Σ, so
every Sharpe ratio falls by the same $$\kappa$$ √((periods per year) / T) and the
maximum Sharpe portfolio equals that of get_maximum_sharpe_weights. The
ellipsoid changes the weights of the utility and minimum variance objectives,
and the box changes those of all three.
- skfolio's EmpiricalMuUncertaintySet shares the ellipsoid $$\kappa^{2} = \chi_{n}^{2} (\alpha)$$ and $$\sum_{\mu} = \Sigma / T$$.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "JNJ", "XOM"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.portfolio.get_worst_case_mean_variance_weights(
    confidence_level=0.9, maximum_weight=0.5
)[["Weight", "Expected Return", "Worst-Case Return", "Worst-Case Sharpe Ratio"]]
```

Which returns:

|           |   Weight |   Expected Return |   Worst-Case Return |   Worst-Case Sharpe Ratio |
|:----------|---------:|------------------:|--------------------:|--------------------------:|
| AAPL      |      0   |            0.1932 |             -0.0122 |                   -0.1649 |
| MSFT      |      0.5 |            0.2017 |              0.0121 |                   -0.084  |
| JNJ       |      0   |            0.0987 |             -0.0247 |                   -0.349  |
| XOM       |      0.5 |            0.2911 |              0.0919 |                    0.2152 |
| Portfolio |      1   |            0.2464 |              0.052  |                    0.0941 |

---

## get_distributionally_robust_cvar_weights
Calculate the weights of the distributionally robust mean-CVaR portfolio.

It is the portfolio that minimizes the expected loss plus the risk aversion times the Conditional Value at Risk (CVaR) under the least favourable distribution of the returns within a Wasserstein ball around the historical returns. The historical returns are one sample of the distribution; the ball holds every distribution that lies within a transport distance $$\epsilon$$ of it, so the portfolio is protected against distributions with heavier losses than the sample happened to show.

With $$X = \xi' w$$ the portfolio return, $$\alpha$$ the tail probability, $$\rho$$ the risk aversion and $$\epsilon$$ the radius, the weights minimize

- sup over Q in the ball of $$E_{Q} [- X] + \rho \text{CVaR}_{\alpha} , Q (- X)$$,

where the distance between two distributions is the least average 1-norm change in the returns of the assets that turns one into the other (the type-1 Wasserstein distance), and returns stay at or above -100%. Mohajerin Esfahani and Kuhn (2018) show that this worst case is a linear programme: with the CVaR written as min over $$\tau$$ of $$\tau + E [\max (- X - \tau , 0)] / \alpha$$ the loss is the maximum of two linear pieces, and its worst case is $$\min \lambda \epsilon + \sum s_{t} / T$$ over $$\lambda \geq 0$$ with $$s_{t}$$ bounding each piece in period t after the most harmful shift of the returns. Per asset that shift is either none or down to -100%, so the programme has n + 2 + T + 2n variables and is solved exactly with HiGHS. At a radius of 0 it is the historical mean-CVaR portfolio.

**Also known as:** Wasserstein robust CVaR, DRO CVaR, distributionally robust mean-CVaR.

**References:**

- paper | Mohajerin Esfahani, P. and Kuhn, D. (2018). "Data-Driven Distributionally Robust Optimization Using the Wasserstein Metric: Performance Guarantees and Tractable Reformulations." Mathematical Programming, 171(1-2), 115-166.
- paper | Rockafellar, R. T. and Uryasev, S. (2000). "Optimization of Conditional Value-at-Risk." Journal of Risk, 2(3), 21-41.
- library | Referenced against skfolio's [DistributionallyRobustCVaR](https://skfolio.org/generated/skfolio.optimization.DistributionallyRobustCVaR.html){:target="_blank"}

**Args:**

- <u>alpha (float, optional):</u> The tail probability $$\alpha$$ of the CVaR, e.g. 0.05
for the average of the worst 5% of periods. Defaults to 0.05.
- <u>wasserstein_radius (float, optional):</u> The radius $$\epsilon$$ of the Wasserstein ball, in
returns per period of the chosen frequency: the average total change in
the returns of all assets that the distributions considered may have.
Defaults to 0.0005, which suits daily returns (see the Notes).
- <u>risk_aversion (float, optional):</u> The weight $$\rho$$ of the CVaR against the
expected loss; a high value gives the minimum worst-case CVaR portfolio.
Defaults to 1.
- <u>period (str, optional):</u> The frequency of the returns. Options are: "daily" (daily returns), "weekly"
(weekly returns), "monthly" (monthly returns), "quarterly" (quarterly returns), "yearly" (yearly
returns). Defaults to "daily".
- <u>minimum_weight (float &#124; dict[str, float], optional):</u> The lowest weight of
every asset, or per asset, e.g. {"AAPL": 0.05} (the others keep 0); a
negative value allows short positions. Defaults to 0.
- <u>maximum_weight (float &#124; dict[str, float], optional):</u> The highest weight of
every asset, or per asset, e.g. {"AAPL": 0.3} (the others keep 1).
Defaults to 1.
- <u>sector_bounds (dict[str, tuple[float, float]] &#124; None, optional):</u> The minimum
and maximum total weight per sector, e.g. {"Technology": (0, 0.4)}, with
the sector of each asset from its company profile. Defaults to None.
- <u>country_bounds (dict[str, tuple[float, float]] &#124; None, optional):</u> The minimum
and maximum total weight per country, named in full or by its two-letter
code, e.g. {"United States": (0, 0.6)}, with the country of each asset
from its company profile. Defaults to None.
- <u>net_exposure (float, optional):</u> The sum of the weights: 1 for a fully invested
portfolio. The rest, 1 minus the net exposure, is a Cash row at the risk
free rate (negative when borrowed above one), which the Portfolio's Expected
Return and Sharpe Ratio include. Defaults to 1.
- <u>gross_exposure (float &#124; None, optional):</u> The highest sum of the absolute
weights, which limits the leverage of a long-short portfolio, e.g. 1.6 for
a 130/30 portfolio. Defaults to None, no limit.
- <u>current_weights (dict[str, float] &#124; None, optional):</u> The weights held now,
e.g. {"AAPL": 0.5, "MSFT": 0.5} (an asset left out is not held), which
the turnover is measured from; they add a Turnover column, $$\vert w_{i} - w_{0,i} \vert$$
per asset and its sum for the portfolio. Defaults to None, which uses
the latest weights of the Portfolio the Toolkit came from when a maximum
turnover needs them.
- <u>maximum_turnover (float &#124; None, optional):</u> The highest turnover
$$\sum \vert w_{i} - w_{0,i} \vert$$ from the current weights, e.g. 0.2 to trade at most 10%
of the portfolio each way. Defaults to None, no limit.
- <u>include_benchmark (bool, optional):</u> Whether to include the benchmark as an
asset. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per asset and for the portfolio, the Weight, Expected Return,
Volatility, Sharpe Ratio and Risk Contribution, with the historical CVaR and
the Worst-Case CVaR over the Wasserstein ball (per period, positive for a
loss) of every asset on its own and of the portfolio.

**Notes:**

- The radius is in returns per period, so it depends on the frequency. For a
long-only portfolio and a small radius the worst case adds
$$\epsilon (1 + \rho / \alpha)$$ max_i $$w_{i}$$ to the historical objective: the least
favourable distribution moves the asset with the largest weight down in the
tail periods, which favours spreading the weights. With daily returns a radius
of about 0.002 or more already gives equal weights, so the default is 0.0005
(skfolio's is 0.02).
- The worst-case CVaR of an asset or portfolio is the same programme with the
weights fixed, without the expected loss.
- skfolio's DistributionallyRobustCVaR has the same formulation (a 1-norm transport
cost, returns of at least -100%) and the same $$\alpha = 0.05$$ (its $$\beta = 0.95$$) and $$\rho = 1$$ by
default.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "JNJ", "XOM"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.portfolio.get_distributionally_robust_cvar_weights()[
    ["Weight", "Expected Return", "CVaR", "Worst-Case CVaR"]
]
```

Which returns:

|           |   Weight |   Expected Return |   CVaR |   Worst-Case CVaR |
|:----------|---------:|------------------:|-------:|------------------:|
| AAPL      |   0.0581 |            0.1932 | 0.039  |            0.049  |
| MSFT      |   0.2543 |            0.2017 | 0.0356 |            0.0456 |
| JNJ       |   0.4117 |            0.0987 | 0.0227 |            0.0327 |
| XOM       |   0.2759 |            0.2911 | 0.0373 |            0.0473 |
| Portfolio |   1      |            0.1835 | 0.0199 |            0.0241 |

---

## get_maximum_diversification_weights
Calculate the weights of the maximum diversification portfolio.

It is the fully invested portfolio with the highest diversification ratio, the weighted average volatility of its assets divided by its own volatility. The ratio is one for a single asset and grows as the assets move less together, so the portfolio holds the assets that diversify each other most. It needs no expected returns, and when every asset has the same Sharpe ratio it is also the maximum Sharpe ratio portfolio.

The weights maximize $$\text{DR} (w) = w' \sigma / \sqrt{w' \Sigma w}$$ subject to the weights summing to one and lying between the minimum and maximum weight, with $$\sigma$$ the volatilities of the assets and $$\Sigma$$ their annualized covariance matrix. The square of the ratio is the number of independent risk factors a long-only portfolio effectively holds.

**Also known as:** most diversified portfolio, MDP, maximum diversification ratio.

**References:**

- paper | Choueifaty, Y. and Coignard, Y. (2008). "Toward Maximum Diversification." The Journal of Portfolio Management, 35(1), 40-51.
- paper | Choueifaty, Y., Froidure, T. and Reynier, J. (2013). "Properties of the Most Diversified Portfolio." Journal of Investment Strategies, 2(2), 49-70.
- library | Referenced against skfolio's [MaximumDiversification](https://skfolio.org/generated/skfolio.optimization.MaximumDiversification.html){:target="_blank"}

**Args:**

- <u>period (str, optional):</u> The frequency of the returns the covariance matrix is estimated from. Options
are: "daily" (daily returns), "weekly" (weekly returns), "monthly" (monthly returns), "quarterly"
(quarterly returns), "yearly" (yearly returns). Defaults to "daily".
- <u>covariance (str, optional):</u> The estimator of the covariance matrix. The shrinkage and denoised
estimators stabilize the weights when there are many assets compared to the number of periods.
Options are: "sample" (the sample covariance, ddof=1), "ledoit_wolf" (shrunk towards the scaled
identity, Ledoit and Wolf, 2004), "ledoit_wolf_constant_correlation" (shrunk towards the average
correlation, Ledoit and Wolf, 2004), "ledoit_wolf_single_factor" (shrunk towards the covariance that
the benchmark as a single factor implies, Ledoit and Wolf, 2003), "oas" (Oracle Approximating
Shrinkage, Chen et al., 2010), "shrunk" (a fixed 10% towards the scaled identity), "semicovariance"
(the co-movement below a zero return, Estrada, 2008), "exponential" (exponentially weighted, recent
periods weigh most, RiskMetrics), "denoised" (the eigenvalues of the correlation matrix that random
returns could produce averaged, Laloux et al., 2000), "denoised_spectral" (those eigenvalues set to
zero), "denoised_shrink" (the noise correlations shrunk towards their diagonal, López de Prado,
2020), "gerber" (co-movements beyond half a standard deviation, Gerber et al., 2022), "factor" (the
covariance of the Fama and French five factor model with OLS loadings, Fama and French, 1993),
"minimum_covariance_determinant" (the reweighted covariance of the half of the periods with the
smallest covariance determinant, robust to outliers, Rousseeuw and Van Driessen, 1999), "jlogo" (the
sparse inverse covariance on the TMFG planar graph of the correlations, Barfuss et al., 2016),
"geodesic" (10% towards the scaled identity along the geodesic of the positive definite matrices,
Bhatia, 2007), "regime_adjusted_ew" (exponentially weighted with a half-life of 40 periods, rescaled
by the recent realized against predicted risk, Paleologo, 2025), "nercome" (eigenvectors from one
part of the periods and the variances along them from the other, averaged over random splits, Lam,
2016), "ccc_garch" (the next-period covariance of GARCH(1, 1) volatilities with constant
correlations, Bollerslev, 1990), "mm" (the robust MM-estimator, Maronna et al., 2019), "rocke"
(Rocke's robust S-estimator, Maronna et al., 2019). Defaults to "sample".
- <u>covariance_span (int, optional):</u> The span in periods of the exponentially weighted covariance; the
weight of a period halves after about span / 2.9 periods. Defaults to 180.
- <u>minimum_weight (float &#124; dict[str, float], optional):</u> The lowest weight of
every asset, or per asset, e.g. {"AAPL": 0.05} (the others keep 0); a
negative value allows short positions. Defaults to 0.
- <u>maximum_weight (float &#124; dict[str, float], optional):</u> The highest weight of
every asset, or per asset, e.g. {"AAPL": 0.3} (the others keep 1).
Defaults to 1.
- <u>sector_bounds (dict[str, tuple[float, float]] &#124; None, optional):</u> The minimum
and maximum total weight per sector, e.g. {"Technology": (0, 0.4)}, with
the sector of each asset from its company profile. Defaults to None.
- <u>country_bounds (dict[str, tuple[float, float]] &#124; None, optional):</u> The minimum
and maximum total weight per country, named in full or by its two-letter
code, e.g. {"United States": (0, 0.6)}, with the country of each asset
from its company profile. Defaults to None.
- <u>net_exposure (float, optional):</u> The sum of the weights: 1 for a fully invested
portfolio, 0 for a market neutral one (which needs a negative
minimum_weight). The rest, 1 minus the net exposure, is a Cash row at the
risk free rate (negative when borrowed above one), which the Portfolio's
Expected Return and Sharpe Ratio include. Defaults to 1.
- <u>gross_exposure (float &#124; None, optional):</u> The highest sum of the absolute
weights, which limits the leverage of a long-short portfolio, e.g. 1.6 for
a 130/30 portfolio. Defaults to None, no limit.
- <u>current_weights (dict[str, float] &#124; None, optional):</u> The weights held now,
e.g. {"AAPL": 0.5, "MSFT": 0.5} (an asset left out is not held), which
the turnover is measured from; they add a Turnover column, $$\vert w_{i} - w_{0,i} \vert$$
per asset and its sum for the portfolio. Defaults to None, which uses
the latest weights of the Portfolio the Toolkit came from when a maximum
turnover or transaction cost needs them.
- <u>maximum_turnover (float &#124; None, optional):</u> The highest turnover
$$\sum \vert w_{i} - w_{0,i} \vert$$ from the current weights, e.g. 0.2 to trade at most 10%
of the portfolio each way. Defaults to None, no limit.
- <u>include_benchmark (bool, optional):</u> Whether to include the benchmark as an
asset. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per asset and for the portfolio, the Weight, Expected Return,
Volatility, Sharpe Ratio and Risk Contribution, with the Diversification Ratio
of the portfolio (one for every asset on its own). Returns and volatilities are
annualized.

**Notes:**

- The ratio is maximized directly, so it works with any weight bounds, including
short positions; with a negative minimum weight the ratio no longer counts
independent risk factors.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "JNJ", "XOM"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.portfolio.get_maximum_diversification_weights()[
    ["Weight", "Volatility", "Sharpe Ratio", "Risk Contribution", "Diversification Ratio"]
]
```

Which returns:

|           |   Weight |   Volatility |   Sharpe Ratio |   Risk Contribution |   Diversification Ratio |
|:----------|---------:|-------------:|---------------:|--------------------:|------------------------:|
| AAPL      |   0.0923 |       0.2786 |         0.5727 |              0.1145 |                     1   |
| MSFT      |   0.2349 |       0.2572 |         0.6532 |              0.2687 |                     1   |
| JNJ       |   0.4194 |       0.1673 |         0.3867 |              0.3122 |                     1   |
| XOM       |   0.2533 |       0.2702 |         0.9522 |              0.3046 |                     1   |
| Portfolio |   1      |       0.1405 |         1.043  |              1      |                     1.6 |

---

## get_minimum_tracking_error_weights
Calculate the weights of the portfolio of the Toolkit's assets that follows the benchmark most closely.

It is the fully invested portfolio with the lowest tracking error, the volatility of its return minus the benchmark's. With the information ratio as the objective it is instead the portfolio with the highest information ratio, the expected return above the benchmark per unit of tracking error, which is what an active manager measured against the benchmark maximizes.

The tracking error is $$\text{TE} (w) = \sqrt{\operatorname{Var} (R w - r_{b})} = \sqrt{w' \Sigma_{\text{AA}} w - 2 w' \Sigma_{\text{Ab}} + \sigma_{b}^{2}}$$, with $$\Sigma_{\text{AA}}$$ the annualized covariance matrix of the assets, $$\Sigma_{\text{Ab}}$$ their covariances with the benchmark and $$\sigma_{b}^{2}$$ the benchmark's variance. The information ratio is $$(w' \mu + (1 - \Sigma w) r_{f} - \mu_{b}) / \text{TE} (w)$$, with $$\mu$$ and $$\mu_{b}$$ the annualized expected returns and the part not invested at the risk free rate $$r_{f}$$, which leaves the tracking error as it is. The weights sum to the net exposure, one by default, and lie between the minimum and maximum weight; the benchmark is the Toolkit's (SPY by default) and is not one of the assets.

**Also known as:** index tracking, benchmark tracking, minimum active risk, maximum information ratio portfolio.

**References:**

- paper | Roll, R. (1992). "A Mean/Variance Analysis of Tracking Error." The Journal of Portfolio Management, 18(4), 13-22.
- paper | Jorion, P. (2003). "Portfolio Optimization with Tracking-Error Constraints." Financial Analysts Journal, 59(5), 70-82.
- paper | Grinold, R.C. and Kahn, R.N. (2000). "Active Portfolio Management." 2nd edition, McGraw-Hill.
- library | Referenced against skfolio's [BenchmarkTracker](https://skfolio.org/generated/skfolio.optimization.BenchmarkTracker.html){:target="_blank"} (tracking error)
- library | Referenced against PyPortfolioOpt's [objective_functions.ex_post_tracking_error](https://pyportfolioopt.readthedocs.io/en/latest/MeanVariance.html#pypfopt.objective_functions.ex_post_tracking_error){:target="_blank"} (tracking error)
- library | Referenced against skfolio's [MeanRisk](https://skfolio.org/generated/skfolio.optimization.MeanRisk.html){:target="_blank"} (information ratio)

**Args:**

- <u>objective (str, optional):</u> Options are: "tracking_error" (the lowest tracking error),
"information_ratio" (the highest information ratio). Defaults to "tracking_error".
- <u>period (str, optional):</u> The frequency of the returns. Options are: "daily" (daily returns), "weekly"
(weekly returns), "monthly" (monthly returns), "quarterly" (quarterly returns), "yearly" (yearly
returns). Defaults to "daily".
- <u>covariance (str, optional):</u> The estimator of the covariance matrix of the assets and the benchmark.
Options are: "sample" (the sample covariance, ddof=1), "ledoit_wolf" (shrunk towards the scaled
identity, Ledoit and Wolf, 2004), "ledoit_wolf_constant_correlation" (shrunk towards the average
correlation, Ledoit and Wolf, 2004), "ledoit_wolf_single_factor" (shrunk towards the covariance that
the benchmark as a single factor implies, Ledoit and Wolf, 2003), "oas" (Oracle Approximating
Shrinkage, Chen et al., 2010), "shrunk" (a fixed 10% towards the scaled identity), "semicovariance"
(the co-movement below a zero return, Estrada, 2008), "exponential" (exponentially weighted, recent
periods weigh most, RiskMetrics), "denoised" (the eigenvalues of the correlation matrix that random
returns could produce averaged, Laloux et al., 2000), "denoised_spectral" (those eigenvalues set to
zero), "denoised_shrink" (the noise correlations shrunk towards their diagonal, López de Prado,
2020), "gerber" (co-movements beyond half a standard deviation, Gerber et al., 2022), "factor" (the
covariance of the Fama and French five factor model with OLS loadings, Fama and French, 1993),
"minimum_covariance_determinant" (the reweighted covariance of the half of the periods with the
smallest covariance determinant, robust to outliers, Rousseeuw and Van Driessen, 1999), "jlogo" (the
sparse inverse covariance on the TMFG planar graph of the correlations, Barfuss et al., 2016),
"geodesic" (10% towards the scaled identity along the geodesic of the positive definite matrices,
Bhatia, 2007), "regime_adjusted_ew" (exponentially weighted with a half-life of 40 periods, rescaled
by the recent realized against predicted risk, Paleologo, 2025), "nercome" (eigenvectors from one
part of the periods and the variances along them from the other, averaged over random splits, Lam,
2016), "ccc_garch" (the next-period covariance of GARCH(1, 1) volatilities with constant
correlations, Bollerslev, 1990), "mm" (the robust MM-estimator, Maronna et al., 2019), "rocke"
(Rocke's robust S-estimator, Maronna et al., 2019). Defaults to "sample".
- <u>covariance_span (int, optional):</u> The span in periods of the exponentially weighted covariance; the
weight of a period halves after about span / 2.9 periods. Defaults to 180.
- <u>expected_returns (str, optional):</u> The estimator of the expected returns. Options are: "mean" (the
historical average), "geometric" (the compounded average), "exponential" (the exponentially weighted
average, recent periods weigh most), "exponential_geometric" (that average compounded over a year),
"capm" (the returns the Capital Asset Pricing Model implies from each asset's beta to the benchmark,
Sharpe, 1964), "bayes_stein" (the averages shrunk towards that of the minimum variance portfolio,
Jorion, 1986), "james_stein" (the averages shrunk towards their grand mean, James and Stein, 1961),
"bodnar_okhrin_parolya" (the averages and their grand mean combined with optimal weights, Bodnar,
Okhrin and Parolya, 2019). Defaults to "mean".
- <u>expected_returns_span (int, optional):</u> The span in periods of the exponentially weighted expected
returns. Defaults to 180.
- <u>minimum_weight (float &#124; dict[str, float], optional):</u> The lowest weight of
every asset, or per asset, e.g. {"AAPL": 0.05} (the others keep 0); a
negative value allows short positions. Defaults to 0.
- <u>maximum_weight (float &#124; dict[str, float], optional):</u> The highest weight of
every asset, or per asset, e.g. {"AAPL": 0.3} (the others keep 1).
Defaults to 1.
- <u>sector_bounds (dict[str, tuple[float, float]] &#124; None, optional):</u> The minimum
and maximum total weight per sector, e.g. {"Technology": (0, 0.4)}, with
the sector of each asset from its company profile. Defaults to None.
- <u>country_bounds (dict[str, tuple[float, float]] &#124; None, optional):</u> The minimum
and maximum total weight per country, named in full or by its two-letter
code, e.g. {"United States": (0, 0.6)}, with the country of each asset
from its company profile. Defaults to None.
- <u>net_exposure (float, optional):</u> The sum of the weights: 1 for a fully invested
portfolio, 0 for a market neutral one (which needs a negative
minimum_weight). The rest, 1 minus the net exposure, is a Cash row at the
risk free rate (negative when borrowed above one), which the Portfolio's
Expected Return and Sharpe Ratio include. Defaults to 1.
- <u>gross_exposure (float &#124; None, optional):</u> The highest sum of the absolute
weights, which limits the leverage of a long-short portfolio, e.g. 1.6 for
a 130/30 portfolio. Defaults to None, no limit.
- <u>current_weights (dict[str, float] &#124; None, optional):</u> The weights held now,
e.g. {"AAPL": 0.5, "MSFT": 0.5} (an asset left out is not held), which
the turnover is measured from; they add a Turnover column, $$\vert w_{i} - w_{0,i} \vert$$
per asset and its sum for the portfolio. Defaults to None, which uses
the latest weights of the Portfolio the Toolkit came from when a maximum
turnover or transaction cost needs them.
- <u>maximum_turnover (float &#124; None, optional):</u> The highest turnover
$$\sum \vert w_{i} - w_{0,i} \vert$$ from the current weights, e.g. 0.2 to trade at most 10%
of the portfolio each way. Defaults to None, no limit.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per asset and for the portfolio, the Weight, Expected Return,
Volatility, Sharpe Ratio and Risk Contribution, and against the benchmark the
Active Return, Tracking Error and Information Ratio (each asset on its own and
the portfolio). Returns, volatilities and tracking errors are annualized.

**Notes:**

- Only the periods in which every asset and the benchmark have a return are used.
- With the sample covariance the tracking error equals the annualized standard
deviation (ddof=1) of the historical active returns $$R w - r_{b}$$.
- The information ratio needs an asset that expects more than the benchmark;
otherwise no portfolio has a positive information ratio and an error is raised.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "JNJ", "XOM"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.portfolio.get_minimum_tracking_error_weights()[
    ["Weight", "Expected Return", "Active Return", "Tracking Error", "Information Ratio"]
]
```

Which returns:

|           |   Weight |   Expected Return |   Active Return |   Tracking Error |   Information Ratio |
|:----------|---------:|------------------:|----------------:|-----------------:|--------------------:|
| AAPL      |   0.249  |            0.1933 |          0.0411 |           0.1861 |              0.2209 |
| MSFT      |   0.3641 |            0.2017 |          0.0495 |           0.1693 |              0.2923 |
| JNJ       |   0.2149 |            0.0984 |         -0.0538 |           0.2113 |             -0.2545 |
| XOM       |   0.172  |            0.291  |          0.1388 |           0.2658 |              0.5224 |
| Portfolio |   1      |            0.1928 |          0.0406 |           0.0881 |              0.4603 |

---

## get_growth_optimal_weights
Calculate the weights of the growth optimal (Kelly) portfolio.

It is the fully invested portfolio with the highest expected logarithmic growth of wealth, which in the long run ends up with more wealth than any other strategy with near certainty. Because the full Kelly portfolio is volatile and sensitive to errors in the expected returns, investors often hold a fraction of it (fractional Kelly) and keep the rest in cash.

The exact method maximizes the average log return over the historical returns, $$(1 / T) \sum \ln (1 + r_{t}' w)$$. The approximate method maximizes its second-order approximation $$w' \mu$$ - ½ $$w' \Sigma w$$, which is a mean-variance portfolio with a risk aversion of one; it uses the expected returns and covariance matrix instead of the returns themselves. Both keep the weights summing to one and between the minimum and maximum weight. The weights are then multiplied by the fraction and the remainder, 1 - fraction, is held in cash at the risk free rate (borrowed when the fraction is above one).

**Also known as:** Kelly portfolio, log-optimal portfolio, maximum geometric return, fractional Kelly.

**References:**

- paper | Kelly, J.L. (1956). "A New Interpretation of Information Rate." Bell System Technical Journal, 35(4), 917-926.
- paper | Breiman, L. (1961). "Optimal Gambling Systems for Favorable Games." Proceedings of the Fourth Berkeley Symposium on Mathematical Statistics and Probability, 1, 65-78.
- paper | Thorp, E.O. (2006). "The Kelly Criterion in Blackjack, Sports Betting and the Stock Market." Handbook of Asset and Liability Management, 1, 385-428.
- library | Referenced against Riskfolio-Lib's [Portfolio.optimization](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/portfolio.html#Portfolio.Portfolio.optimization){:target="_blank"} (Kelly criterion)

**Args:**

- <u>method (str, optional):</u> Options are: "exact" (the historical log returns), "approximate" (the
mean-variance approximation). Defaults to "exact".
- <u>fraction (float, optional):</u> The share of the growth optimal portfolio to hold,
e.g. 0.5 for half Kelly; the rest is cash. Defaults to 1.
- <u>period (str, optional):</u> The frequency of the returns. Options are: "daily" (daily returns), "weekly"
(weekly returns), "monthly" (monthly returns), "quarterly" (quarterly returns), "yearly" (yearly
returns). Defaults to "daily".
- <u>covariance (str, optional):</u> The estimator of the covariance matrix, used by the "approximate" method and
for the volatility and risk contributions. Options are: "sample" (the sample covariance, ddof=1),
"ledoit_wolf" (shrunk towards the scaled identity, Ledoit and Wolf, 2004),
"ledoit_wolf_constant_correlation" (shrunk towards the average correlation, Ledoit and Wolf, 2004),
"ledoit_wolf_single_factor" (shrunk towards the covariance that the benchmark as a single factor
implies, Ledoit and Wolf, 2003), "oas" (Oracle Approximating Shrinkage, Chen et al., 2010), "shrunk"
(a fixed 10% towards the scaled identity), "semicovariance" (the co-movement below a zero return,
Estrada, 2008), "exponential" (exponentially weighted, recent periods weigh most, RiskMetrics),
"denoised" (the eigenvalues of the correlation matrix that random returns could produce averaged,
Laloux et al., 2000), "denoised_spectral" (those eigenvalues set to zero), "denoised_shrink" (the
noise correlations shrunk towards their diagonal, López de Prado, 2020), "gerber" (co-movements
beyond half a standard deviation, Gerber et al., 2022), "factor" (the covariance of the Fama and
French five factor model with OLS loadings, Fama and French, 1993), "minimum_covariance_determinant"
(the reweighted covariance of the half of the periods with the smallest covariance determinant,
robust to outliers, Rousseeuw and Van Driessen, 1999), "jlogo" (the sparse inverse covariance on the
TMFG planar graph of the correlations, Barfuss et al., 2016), "geodesic" (10% towards the scaled
identity along the geodesic of the positive definite matrices, Bhatia, 2007), "regime_adjusted_ew"
(exponentially weighted with a half-life of 40 periods, rescaled by the recent realized against
predicted risk, Paleologo, 2025), "nercome" (eigenvectors from one part of the periods and the
variances along them from the other, averaged over random splits, Lam, 2016), "ccc_garch" (the
next-period covariance of GARCH(1, 1) volatilities with constant correlations, Bollerslev, 1990),
"mm" (the robust MM-estimator, Maronna et al., 2019), "rocke" (Rocke's robust S-estimator, Maronna
et al., 2019). Defaults to "sample".
- <u>covariance_span (int, optional):</u> The span in periods of the exponentially weighted covariance; the
weight of a period halves after about span / 2.9 periods. Defaults to 180.
- <u>expected_returns (str, optional):</u> The estimator of the expected returns. Options are: "mean" (the
historical average), "geometric" (the compounded average), "exponential" (the exponentially weighted
average, recent periods weigh most), "exponential_geometric" (that average compounded over a year),
"capm" (the returns the Capital Asset Pricing Model implies from each asset's beta to the benchmark,
Sharpe, 1964), "bayes_stein" (the averages shrunk towards that of the minimum variance portfolio,
Jorion, 1986), "james_stein" (the averages shrunk towards their grand mean, James and Stein, 1961),
"bodnar_okhrin_parolya" (the averages and their grand mean combined with optimal weights, Bodnar,
Okhrin and Parolya, 2019). Defaults to "mean".
- <u>expected_returns_span (int, optional):</u> The span in periods of the exponentially weighted expected
returns. Defaults to 180.
- <u>minimum_weight (float &#124; dict[str, float], optional):</u> The lowest weight of
every asset, or per asset, e.g. {"AAPL": 0.05} (the others keep 0); a
negative value allows short positions. Defaults to 0.
- <u>maximum_weight (float &#124; dict[str, float], optional):</u> The highest weight of
every asset, or per asset, e.g. {"AAPL": 0.3} (the others keep 1).
Defaults to 1.
- <u>sector_bounds (dict[str, tuple[float, float]] &#124; None, optional):</u> The minimum
and maximum total weight per sector, e.g. {"Technology": (0, 0.4)}, with
the sector of each asset from its company profile. Defaults to None.
- <u>country_bounds (dict[str, tuple[float, float]] &#124; None, optional):</u> The minimum
and maximum total weight per country, named in full or by its two-letter
code, e.g. {"United States": (0, 0.6)}, with the country of each asset
from its company profile. Defaults to None.
- <u>net_exposure (float, optional):</u> The sum of the weights: 1 for a fully
invested portfolio, 0 for a market neutral one (which needs a negative
minimum_weight). Defaults to 1.
- <u>gross_exposure (float &#124; None, optional):</u> The highest sum of the absolute
weights, which limits the leverage of a long-short portfolio, e.g. 1.6 for
a 130/30 portfolio. Defaults to None, no limit.
- <u>include_benchmark (bool, optional):</u> Whether to include the benchmark as an
asset. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per asset, for the Cash (when the fraction is not one) and for the
portfolio, the Weight, Expected Return, Volatility, Sharpe Ratio and Risk
Contribution, with the Log Growth, the annualized average log return of each
asset on its own and of the portfolio. Returns and volatilities are annualized.

**Notes:**

- With historical average returns the full Kelly weights tend to concentrate in the
assets that happened to grow fastest; a fraction below one or a maximum weight
tempers that. The expected returns only enter the approximate method; the
exact method uses the returns themselves.
- The log growth is the average of ln(1 + r) per period times the number of periods
in a year, so the growth of daily returns is comparable to that of monthly ones.
- The weight bounds, sector and country bounds and exposures apply to the full
Kelly portfolio; the fraction then scales it, so the weights sum to the fraction
times the net exposure and the rest is cash.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "JNJ", "XOM"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.portfolio.get_growth_optimal_weights(fraction=0.5, maximum_weight=0.4)
```

Which returns:

|           |   Weight |   Expected Return |   Volatility |   Sharpe Ratio |   Risk Contribution |   Log Growth |
|:----------|---------:|------------------:|-------------:|---------------:|--------------------:|-------------:|
| AAPL      |      0.1 |            0.1933 |       0.2786 |         0.5727 |              0.2141 |       0.1547 |
| MSFT      |      0.2 |            0.2017 |       0.2572 |         0.6532 |              0.4118 |       0.1687 |
| JNJ       |      0   |            0.0984 |       0.1673 |         0.3867 |              0      |       0.0844 |
| XOM       |      0.2 |            0.291  |       0.2702 |         0.9522 |              0.374  |       0.2544 |
| Cash      |      0.5 |            0.0337 |       0      |       nan      |              0      |       0.0337 |
| Portfolio |      1   |            0.1347 |       0.0959 |         1.0531 |              1      |       0.1301 |

---

## get_resampled_efficient_weights
Calculate the weights of the resampled efficient portfolio (Michaud resampling).

It is the average of the optimal weights over many return histories that could have been observed instead of the actual one. A single optimization takes the estimated expected returns and covariances at face value and piles into the assets whose estimates happen to be highest; averaging over resampled histories only gives an asset a large weight when it earns it in most of them, which makes the weights more diversified and more stable from one estimate to the next.

Every draw has as many periods as the returns. With parametric resampling, as in Michaud, the draws come from a multivariate normal distribution with the estimated expected returns and covariance; with the bootstrap they are periods of the actual returns drawn with replacement, which keeps their fat tails and skew. The objective is optimized on the sample mean and sample covariance of every draw within the constraints, and the weights are averaged.

**Also known as:** Michaud resampling, resampled efficiency, resampled efficient frontier, portfolio resampling.

**References:**

- paper | Michaud, R. O. (1998). "Efficient Asset Management: A Practical Guide to Stock Portfolio Optimization and Asset Allocation." Harvard Business School Press.
- paper | Scherer, B. (2002). "Portfolio Resampling: Review and Critique." Financial Analysts Journal, 58(6), 98-109.
- library | Referenced against Riskfolio-Lib's [Portfolio.optimization](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/portfolio.html#Portfolio.Portfolio.optimization){:target="_blank"} (every draw)

**Args:**

- <u>objective (str, optional):</u> The portfolio optimized in every draw. Options are: "maximum_sharpe" (the
highest Sharpe ratio), "minimum_variance" (the lowest variance), "mean_variance" (the utility with
the risk aversion). Defaults to "maximum_sharpe".
- <u>resamples (int, optional):</u> The number of resampled return histories. The
average settles as their number grows; 500 keeps the weights within
about a percentage point of their limit for a handful of assets.
Defaults to 500.
- <u>resampling (str, optional):</u> How the histories are drawn. Options are: "parametric" (a multivariate
normal distribution with the estimated expected returns and covariance), "bootstrap" (the actual
periods, drawn with replacement). Defaults to "parametric".
- <u>seed (int &#124; None, optional):</u> The seed of the random draws; the same seed
gives the same weights. Defaults to 0; None draws anew on every call.
- <u>risk_aversion (float, optional):</u> The risk aversion of the mean-variance objective. Defaults to 2.5.
- <u>period (str, optional):</u> The frequency of the returns. Options are: "daily" (daily returns), "weekly"
(weekly returns), "monthly" (monthly returns), "quarterly" (quarterly returns), "yearly" (yearly
returns). Defaults to "daily".
- <u>covariance (str, optional):</u> The estimator of the covariance matrix the "parametric" draws come from and
the table reports. Options are: "sample" (the sample covariance, ddof=1), "ledoit_wolf" (shrunk
towards the scaled identity, Ledoit and Wolf, 2004), "ledoit_wolf_constant_correlation" (shrunk
towards the average correlation, Ledoit and Wolf, 2004), "ledoit_wolf_single_factor" (shrunk towards
the covariance that the benchmark as a single factor implies, Ledoit and Wolf, 2003), "oas" (Oracle
Approximating Shrinkage, Chen et al., 2010), "shrunk" (a fixed 10% towards the scaled identity),
"semicovariance" (the co-movement below a zero return, Estrada, 2008), "exponential" (exponentially
weighted, recent periods weigh most, RiskMetrics), "denoised" (the eigenvalues of the correlation
matrix that random returns could produce averaged, Laloux et al., 2000), "denoised_spectral" (those
eigenvalues set to zero), "denoised_shrink" (the noise correlations shrunk towards their diagonal,
López de Prado, 2020), "gerber" (co-movements beyond half a standard deviation, Gerber et al.,
2022), "factor" (the covariance of the Fama and French five factor model with OLS loadings, Fama and
French, 1993), "minimum_covariance_determinant" (the reweighted covariance of the half of the
periods with the smallest covariance determinant, robust to outliers, Rousseeuw and Van Driessen,
1999), "jlogo" (the sparse inverse covariance on the TMFG planar graph of the correlations, Barfuss
et al., 2016), "geodesic" (10% towards the scaled identity along the geodesic of the positive
definite matrices, Bhatia, 2007), "regime_adjusted_ew" (exponentially weighted with a half-life of
40 periods, rescaled by the recent realized against predicted risk, Paleologo, 2025), "nercome"
(eigenvectors from one part of the periods and the variances along them from the other, averaged
over random splits, Lam, 2016), "ccc_garch" (the next-period covariance of GARCH(1, 1) volatilities
with constant correlations, Bollerslev, 1990), "mm" (the robust MM-estimator, Maronna et al., 2019),
"rocke" (Rocke's robust S-estimator, Maronna et al., 2019). Defaults to "sample".
- <u>covariance_span (int, optional):</u> The span in periods of the exponentially weighted covariance; the
weight of a period halves after about span / 2.9 periods. Defaults to 180.
- <u>expected_returns (str, optional):</u> The estimator of the expected returns the "parametric" draws are
centred on. Options are: "mean" (the historical average), "geometric" (the compounded average),
"exponential" (the exponentially weighted average, recent periods weigh most),
"exponential_geometric" (that average compounded over a year), "capm" (the returns the Capital Asset
Pricing Model implies from each asset's beta to the benchmark, Sharpe, 1964), "bayes_stein" (the
averages shrunk towards that of the minimum variance portfolio, Jorion, 1986), "james_stein" (the
averages shrunk towards their grand mean, James and Stein, 1961), "bodnar_okhrin_parolya" (the
averages and their grand mean combined with optimal weights, Bodnar, Okhrin and Parolya, 2019).
Defaults to "mean".
- <u>expected_returns_span (int, optional):</u> The span in periods of the exponentially weighted expected
returns. Defaults to 180.
- <u>minimum_weight (float &#124; dict[str, float], optional):</u> The lowest weight of
every asset, or per asset, e.g. {"AAPL": 0.05} (the others keep 0); a
negative value allows short positions. Defaults to 0.
- <u>maximum_weight (float &#124; dict[str, float], optional):</u> The highest weight of
every asset, or per asset, e.g. {"AAPL": 0.3} (the others keep 1).
Defaults to 1.
- <u>sector_bounds (dict[str, tuple[float, float]] &#124; None, optional):</u> The minimum
and maximum total weight per sector, e.g. {"Technology": (0, 0.4)}, with
the sector of each asset from its company profile. Defaults to None.
- <u>country_bounds (dict[str, tuple[float, float]] &#124; None, optional):</u> The minimum
and maximum total weight per country, named in full or by its two-letter
code, e.g. {"United States": (0, 0.6)}, with the country of each asset
from its company profile. Defaults to None.
- <u>net_exposure (float, optional):</u> The sum of the weights: 1 for a fully invested
portfolio, 0 for a market neutral one. The rest, 1 minus the net exposure,
is a Cash row at the risk free rate (negative when borrowed above one),
which the Portfolio's Expected Return and Sharpe Ratio include. Defaults to
1.
- <u>gross_exposure (float &#124; None, optional):</u> The highest sum of the absolute
weights, which limits the leverage of a long-short portfolio, e.g. 1.6 for
a 130/30 portfolio. Defaults to None, no limit.
- <u>current_weights (dict[str, float] &#124; None, optional):</u> The weights held now,
e.g. {"AAPL": 0.5, "MSFT": 0.5} (an asset left out is not held), which
the turnover is measured from; they add a Turnover column, $$\vert w_{i} - w_{0,i} \vert$$
per asset and its sum for the portfolio. Defaults to None, which uses
the latest weights of the Portfolio the Toolkit came from when a maximum
turnover needs them.
- <u>maximum_turnover (float &#124; None, optional):</u> The highest turnover
$$\sum \vert w_{i} - w_{0,i} \vert$$ from the current weights, e.g. 0.2 to trade at most 10%
of the portfolio each way. Defaults to None, no limit.
- <u>include_benchmark (bool, optional):</u> Whether to include the benchmark as an
asset. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per asset and for the portfolio, the Weight (the average over
the draws), Expected Return, Volatility, Sharpe Ratio and Risk Contribution
from the estimated expected returns and covariance, with the Weight Standard
Deviation over the draws per asset: how uncertain the optimal weight of the
asset is. Returns and volatilities are annualized.

**Notes:**

- The constraints are linear (or convex, for the gross exposure and turnover), so
the average of weights that meet them meets them too.
- The expected returns and covariance of every draw are its sample mean and
sample covariance; the estimators above set the distribution the parametric
draws come from. A draw without a solution (e.g. one in which no asset beats
the risk free rate for the maximum Sharpe ratio) is left out of the average,
with a warning that says how many were.
- The resampled portfolio is not on the efficient frontier of the estimates: it
gives up some expected Sharpe ratio, measured on those estimates, for weights
that depend less on them (Scherer, 2002).

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "JNJ", "XOM"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.portfolio.get_resampled_efficient_weights()[
    ["Weight", "Expected Return", "Volatility", "Sharpe Ratio", "Weight Standard Deviation"]
]
```

Which returns:

|           |   Weight |   Expected Return |   Volatility |   Sharpe Ratio |   Weight Standard Deviation |
|:----------|---------:|------------------:|-------------:|---------------:|----------------------------:|
| AAPL      |   0.097  |            0.1932 |       0.2786 |         0.5725 |                      0.1559 |
| MSFT      |   0.2598 |            0.2017 |       0.2571 |         0.6534 |                      0.212  |
| JNJ       |   0.2171 |            0.0987 |       0.1673 |         0.3884 |                      0.2159 |
| XOM       |   0.4261 |            0.2911 |       0.2702 |         0.9524 |                      0.2297 |
| Portfolio |   1      |            0.2166 |       0.1622 |         1.1273 |                    nan      |

---

## get_black_litterman_weights
Calculate the Black-Litterman expected returns and the weights they lead to.

The starting point is the return the market implies through its capitalization weights: the excess return $$\Pi = \delta \Sigma w_{\text{mkt}}$$ at which holding the market is optimal, plus the risk free rate, so the Implied Return is a total return. Views then move these returns towards the investor's expectations, in proportion to the confidence in each view. The result avoids the extreme weights that historical average returns give.

Views are absolute ({"AAPL": 0.10}: AAPL returns 10% a year in total, risk free rate included) or relative ({"AAPL-MSFT": 0.02}: AAPL beats MSFT by 2% a year). Without a confidence, a view is as uncertain as the variance of the view portfolio scaled by tau; a confidence c scales that by (1 - c) / c, Idzorek's confidence method in the closed form of Walters (2014). The weights are the mean-variance portfolio of the Black-Litterman returns with the same risk aversion. Without views, or with relative views only, the risk free rate shifts every return by the same amount and leaves the weights unchanged; an absolute view is compared with the implied total return, so there it matters.

The risk aversion is 2.5 by default, the value He and Litterman (1999) use for the world market, or the one the benchmark implies: $$\delta = (E [r_{m}] - r_{f}) / \sigma_{m}^{2}$$, the benchmark's annualized average excess return over its annualized variance on the same periods as the assets.

Two variants put views on factors, by default the five factors of Fama and French (Mkt-RF, SMB, HML, RMW and CMA), with loadings from an OLS regression of the assets on the factors (see get_factor_loadings):

- The augmented model (Cheung, 2009): the assets and the factors form one vector with covariance [$$[\Sigma , B \Sigma_{f}] , [\sum_{f} B' , \sum_{f}]$$] and implied returns [$$\delta \Sigma w ; \delta \Sigma_{f}$$ B'w], the factor premiums the market implies, and the Black-Litterman update takes views on both, so a view on a factor ({"HML": 0.03}, value beats growth by 3% a year) moves every asset through its covariance with that factor. Factor views are premiums, without the risk free rate.
- The Bayesian model (Kolm and Ritter, 2017): the prior is the factor model itself, the historical average factor returns $$\mu_{f}$$ with uncertainty $$\tau \Sigma_{f}$$, the views on the factors update them to $$\hat{\Pi}$$ with uncertainty Ŝ, and the assets follow: $$\mu = \alpha + B \hat{\Pi}$$ and $$\sum_{\text{post}} = B \Sigma_{f} B' + D$$ + BŜB', with $$\alpha$$ the intercepts and D the residual variances. It needs factor views and no market weights; the Prior Return is $$\alpha + B \mu_{f}$$, the average return of every asset, and the weights are the mean-variance portfolio of $$\mu$$ and $$\sum_{\text{post}}$$.

The Posterior Volatility is the square root of the diagonal of the posterior covariance matrix $$\Sigma + M$$ (He and Litterman, 1999), with $$M = ((\tau \Sigma)^{- 1} + P' \Omega^{- 1} P)^{- 1}$$ the uncertainty that remains in the Black-Litterman returns: the volatility to expect for each asset once the estimation error of its return is counted too. The weights use $$\Sigma$$ itself, so that without views they are the market weights.

**Also known as:** BL model, equilibrium returns with views, augmented Black-Litterman, Bayesian Black-Litterman, factor views.

**References:**

- paper | Black, F. and Litterman, R. (1992). "Global Portfolio Optimization." Financial Analysts Journal, 48(5), 28-43.
- paper | He, G. and Litterman, R. (1999). "The Intuition Behind Black-Litterman Model Portfolios." Goldman Sachs Investment Management Research.
- paper | Idzorek, T. (2005). "A Step-by-Step Guide to the Black-Litterman Model: Incorporating User-Specified Confidence Levels." Working paper.
- paper | Walters, J. (2014). "The Black-Litterman Model in Detail." [https://ssrn.com/abstract=1314585](https://ssrn.com/abstract=1314585){:target="_blank"}
- paper | Cheung, W. (2009). "The Augmented Black-Litterman Model: A Ranking-Free Approach to Factor-Based Portfolio Construction and Beyond." [https://ssrn.com/abstract=1347648](https://ssrn.com/abstract=1347648){:target="_blank"}
- paper | Kolm, P. and Ritter, G. (2017). "On the Bayesian Interpretation of Black-Litterman." European Journal of Operational Research, 258(2), 564-572.
- library | Referenced against Riskfolio-Lib's [augmented_black_litterman](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/parameters.html#ParamsEstimation.augmented_black_litterman){:target="_blank"}
- library | Referenced against Riskfolio-Lib's [black_litterman_bayesian](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/parameters.html#ParamsEstimation.black_litterman_bayesian){:target="_blank"}
- library | Shares similar logic as PyPortfolioOpt's [BlackLittermanModel](https://pyportfolioopt.readthedocs.io/en/latest/BlackLitterman.html#pypfopt.black_litterman.BlackLittermanModel){:target="_blank"} (standard)
- library | Shares similar logic as Riskfolio-Lib's [black_litterman](https://riskfolio-lib.readthedocs.io/en/latest/riskfoliolib/parameters.html#ParamsEstimation.black_litterman){:target="_blank"} (standard)
- library | Shares similar logic as PyPortfolioOpt's [market_implied_risk_aversion](https://pyportfolioopt.readthedocs.io/en/latest/BlackLitterman.html#pypfopt.black_litterman.market_implied_risk_aversion){:target="_blank"}

**Args:**

- <u>views (dict[str, float] &#124; None, optional):</u> The annualized views, absolute views
as total returns, as described above. Defaults to None, which returns the
market implied returns.
- <u>view_confidences (dict[str, float] &#124; None, optional):</u> The confidence per view,
between 0 and 1. Defaults to None, which sets each view's uncertainty to the
variance of the view scaled by tau.
- <u>market_weights (dict[str, float] &#124; None, optional):</u> The market weight per asset.
Defaults to None, which uses the market capitalizations of the assets.
- <u>risk_aversion (float &#124; str, optional):</u> The risk aversion $$\delta$$ of the market, or
"market" for the one the benchmark implies, $$(E [r_{m}] - r_{f}) / \sigma_{m}^{2}$$, with
the benchmark's arithmetic average return and variance (ddof=1) per
period both annualized by the number of periods in a year. Defaults to
2.5.
- <u>tau (float, optional):</u> The uncertainty of the implied returns relative to the
covariance matrix. Defaults to 0.05.
- <u>method (str, optional):</u> Options are: "standard" (views on assets), "augmented" (views on assets and
factors), "bayesian" (views on factors of the factor model). Defaults to "standard".
- <u>factor_views (dict[str, float] &#124; None, optional):</u> The annualized views on factors, a premium ({"HML":
0.03}) or the difference of two ({"SMB-HML": 0.01}), for the augmented and Bayesian models. Defaults
to None.
- <u>factor_view_confidences (dict[str, float] &#124; None, optional):</u> The confidence per
factor view, between 0 and 1. Defaults to None, which sets each view's
uncertainty to the variance of the view scaled by tau.
- <u>factors (pd.DataFrame &#124; None, optional):</u> The factor returns, one column per
factor, at the frequency of the period. Defaults to None, the Fama and
French five factors of the region.
- <u>region (str, optional):</u> The region of the Fama and French factors. Defaults to
"United States".
- <u>period (str, optional):</u> The frequency of the returns the covariance matrix is estimated from. Options
are: "daily" (daily returns), "weekly" (weekly returns), "monthly" (monthly returns), "quarterly"
(quarterly returns), "yearly" (yearly returns). Defaults to "daily".
- <u>covariance (str, optional):</u> The estimator of the covariance matrix. The shrinkage and denoised
estimators stabilize the weights when there are many assets compared to the number of periods.
Options are: "sample" (the sample covariance, ddof=1), "ledoit_wolf" (shrunk towards the scaled
identity, Ledoit and Wolf, 2004), "ledoit_wolf_constant_correlation" (shrunk towards the average
correlation, Ledoit and Wolf, 2004), "ledoit_wolf_single_factor" (shrunk towards the covariance that
the benchmark as a single factor implies, Ledoit and Wolf, 2003), "oas" (Oracle Approximating
Shrinkage, Chen et al., 2010), "shrunk" (a fixed 10% towards the scaled identity), "semicovariance"
(the co-movement below a zero return, Estrada, 2008), "exponential" (exponentially weighted, recent
periods weigh most, RiskMetrics), "denoised" (the eigenvalues of the correlation matrix that random
returns could produce averaged, Laloux et al., 2000), "denoised_spectral" (those eigenvalues set to
zero), "denoised_shrink" (the noise correlations shrunk towards their diagonal, López de Prado,
2020), "gerber" (co-movements beyond half a standard deviation, Gerber et al., 2022), "factor" (the
covariance of the Fama and French five factor model with OLS loadings, Fama and French, 1993),
"minimum_covariance_determinant" (the reweighted covariance of the half of the periods with the
smallest covariance determinant, robust to outliers, Rousseeuw and Van Driessen, 1999), "jlogo" (the
sparse inverse covariance on the TMFG planar graph of the correlations, Barfuss et al., 2016),
"geodesic" (10% towards the scaled identity along the geodesic of the positive definite matrices,
Bhatia, 2007), "regime_adjusted_ew" (exponentially weighted with a half-life of 40 periods, rescaled
by the recent realized against predicted risk, Paleologo, 2025), "nercome" (eigenvectors from one
part of the periods and the variances along them from the other, averaged over random splits, Lam,
2016), "ccc_garch" (the next-period covariance of GARCH(1, 1) volatilities with constant
correlations, Bollerslev, 1990), "mm" (the robust MM-estimator, Maronna et al., 2019), "rocke"
(Rocke's robust S-estimator, Maronna et al., 2019). Defaults to "sample".
- <u>covariance_span (int, optional):</u> The span in periods of the exponentially weighted covariance; the
weight of a period halves after about span / 2.9 periods. Defaults to 180.
- <u>minimum_weight (float &#124; dict[str, float], optional):</u> The lowest weight of
every asset, or per asset, e.g. {"AAPL": 0.05} (the others keep 0); a
negative value allows short positions. Defaults to 0.
- <u>maximum_weight (float &#124; dict[str, float], optional):</u> The highest weight of
every asset, or per asset, e.g. {"AAPL": 0.3} (the others keep 1).
Defaults to 1.
- <u>sector_bounds (dict[str, tuple[float, float]] &#124; None, optional):</u> The minimum
and maximum total weight per sector, e.g. {"Technology": (0, 0.4)}, with
the sector of each asset from its company profile. Defaults to None.
- <u>country_bounds (dict[str, tuple[float, float]] &#124; None, optional):</u> The minimum
and maximum total weight per country, named in full or by its two-letter
code, e.g. {"United States": (0, 0.6)}, with the country of each asset
from its company profile. Defaults to None.
- <u>net_exposure (float, optional):</u> The sum of the weights: 1 for a fully invested
portfolio, 0 for a market neutral one (which needs a negative
minimum_weight). The rest, 1 minus the net exposure, is a Cash row at the
risk free rate (negative when borrowed above one), which the Portfolio's
Expected Return and Sharpe Ratio include. Defaults to 1.
- <u>gross_exposure (float &#124; None, optional):</u> The highest sum of the absolute
weights, which limits the leverage of a long-short portfolio, e.g. 1.6 for
a 130/30 portfolio. Defaults to None, no limit.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the Toolkit's rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per asset its Market Weight, Implied Return, Black-Litterman Return
(both annualized total returns), Posterior Volatility (annualized) and the
resulting Weight; with the Bayesian model the Prior Return in place of the
Market Weight and Implied Return.

**Notes:**

- The risk aversion the market implies is refused when the benchmark earned no more than
the risk free rate over the period, as that implies no positive risk aversion.
- The factor models are estimated on the periods in which the assets and the
factors all have a return.
- The augmented model agrees with Riskfolio-Lib's augmented_black_litterman (with $$\tau$$ =
1 / T, its choice) when the loadings hold no intercept: Riskfolio-Lib adds the
intercepts to the posterior returns when they do, which Cheung (2009) does not.
It does not invert the stacked covariance, which is singular when an asset is
itself a factor (the benchmark and Mkt-RF), where Riskfolio-Lib's inverse
loses its accuracy.
- The Bayesian model takes the prior $$N (\mu_{f} , \tau \Sigma_{f})$$; Riskfolio-Lib's
black_litterman_bayesian takes $$N (\mu_{f} , \sum_{f})$$ with views of uncertainty
$$\tau p' \Sigma_{f} p$$, $$\tau = 1 / T$$, which gives the result here with a tau of 1 and a confidence
of T / (T + 1) for every view.

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

|      |   Market Weight |   Implied Return |   Black-Litterman Return |   Posterior Volatility |   Weight |
|:-----|----------------:|-----------------:|-------------------------:|-----------------------:|---------:|
| AAPL |          0.4861 |           0.1751 |                   0.1772 |                 0.2846 |   0.4727 |
| MSFT |          0.3834 |           0.1538 |                   0.1556 |                 0.2631 |   0.3768 |
| JNJ  |          0.0647 |           0.0511 |                   0.0522 |                 0.1714 |   0.016  |
| XOM  |          0.0658 |           0.0697 |                   0.0847 |                 0.2736 |   0.1345 |

---

