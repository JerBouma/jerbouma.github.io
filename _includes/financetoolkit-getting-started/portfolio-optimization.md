## Getting Started

Every portfolio answers the same question: how much to hold of each asset. The Portfolio Optimization module gives the answers the investment literature has settled on, from the mean-variance portfolios of Markowitz to risk parity, Hierarchical Risk Parity and Black-Litterman, and then examines the result: where its risk comes from, how it would have fared in past crises, what it holds once its funds are looked through and where its return came from against the benchmark. It works on the tickers of any `Toolkit` through `toolkit.portfolio`.

This section builds a multi-asset portfolio from six funds: US equities (VTI), developed markets outside the US (VEA), emerging markets (VWO), long-term US Treasuries (TLT), gold (GLD) and US real estate (VNQ), with returns from 2015 to 2025.

### Loading the Data

The module is part of the `Toolkit` class. To load the six funds:

```python
from financetoolkit import Toolkit

assets = Toolkit(
    ["VTI", "VEA", "VWO", "TLT", "GLD", "VNQ"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2015-01-01",
    end_date="2025-12-31",
)
```

Expected returns are the historical average returns and the covariance matrix is estimated from the daily returns, both annualized. Every method takes `period` to estimate them from weekly or monthly returns instead.

### Six Ways to Weight the Same Assets

The methods differ in what they assume can be estimated. With $$w$$ the weights, $$\mu$$ the expected returns, $$\Sigma$$ the covariance matrix and $$r_f$$ the risk-free rate:

- **Minimum variance** minimizes the portfolio variance $$w^\top \Sigma w$$. It ignores expected returns, which are by far the hardest input to estimate.
- **Maximum Sharpe** maximizes $$(w^\top \mu - r_f) / \sqrt{w^\top \Sigma w}$$, the tangency portfolio of Markowitz and Sharpe.
- **Risk parity** chooses the weights so that every asset contributes the same share of the portfolio's risk.
- **Hierarchical Risk Parity** (López de Prado, 2016) clusters the assets by their correlations and splits the weight top-down between the clusters, which needs no inversion of the covariance matrix.
- **Inverse volatility** weights each asset by $$1/\sigma_i$$, risk parity when all correlations would be equal.
- **Minimum CVaR** minimizes the average loss on the worst 5% of days rather than the variance.

To calculate all six:

```python
minimum_variance = assets.portfolio.get_minimum_variance_weights()
maximum_sharpe = assets.portfolio.get_maximum_sharpe_weights()
risk_parity = assets.portfolio.get_risk_parity_weights()
hierarchical_risk_parity = assets.portfolio.get_hierarchical_risk_parity_weights()
inverse_volatility = assets.portfolio.get_inverse_volatility_weights()
minimum_cvar = assets.portfolio.get_minimum_cvar_weights()
```

Each returns the weight per asset with its annualized expected return, volatility, Sharpe Ratio and risk contribution, and the same for the portfolio. For example, the maximum Sharpe portfolio:

|           |   Weight |   Expected Return |   Volatility |   Sharpe Ratio |   Risk Contribution |
|:----------|---------:|------------------:|-------------:|---------------:|--------------------:|
| VTI       |   0.4301 |            0.1385 |       0.1812 |         0.6185 |              0.4641 |
| VEA       |   0.0000 |            0.0914 |       0.1721 |         0.3777 |              0.0000 |
| VWO       |   0.0000 |            0.0767 |       0.1956 |         0.2569 |              0.0000 |
| TLT       |   0.0000 |            0.0036 |       0.1504 |        -0.1521 |              0.0000 |
| GLD       |   0.5699 |            0.1241 |       0.1475 |         0.6624 |              0.5359 |
| VNQ       |   0.0000 |            0.0679 |       0.2051 |         0.2023 |              0.0000 |
| Portfolio |   1.0000 |            0.1303 |       0.1173 |         0.8856 |              1.0000 |

This is the well-known weakness of mean-variance optimization: it puts everything in the two assets with the highest historical Sharpe Ratios, US equities and gold, and nothing in the other four. Small differences in estimated returns become large differences in weights. The methods that use only the covariance matrix spread the weight far more evenly, and risk parity gives every fund exactly a sixth of the risk. When plotted, the weights of each method and, in the second tab, each asset's share of the portfolio's risk:

{% include ft-chart.html id="portfolio-optimization-weights" src="/assets/data/financetoolkit-guides/portfolio-optimization.json" label="Weights and risk contributions of six funds under six optimization methods" %}

### The Efficient Frontier

The efficient frontier is the set of portfolios with the highest expected return for each level of volatility. Each point on it solves

$$
\min_w \; w^\top \Sigma w \quad \text{subject to} \quad w^\top \mu = \mu^*, \quad \textstyle\sum_i w_i = 1, \quad w_{\min} \le w_i \le w_{\max}
$$

for a target return $$\mu^*$$ between that of the minimum variance portfolio and that of the asset with the highest return. The weight bounds are the usual remedy for concentrated portfolios: `maximum_weight` caps every asset and a negative `minimum_weight` allows short positions. To calculate the frontier and the maximum Sharpe portfolio with at most 30% in any one fund:

```python
efficient_frontier = assets.portfolio.get_efficient_frontier(points=20)

capped_maximum_sharpe = assets.portfolio.get_maximum_sharpe_weights(maximum_weight=0.3)
```

Which gives for the capped maximum Sharpe portfolio:

|           |   Weight |   Expected Return |   Volatility |   Sharpe Ratio |   Risk Contribution |
|:----------|---------:|------------------:|-------------:|---------------:|--------------------:|
| VTI       |   0.3000 |            0.1385 |       0.1812 |         0.6185 |              0.4059 |
| VEA       |   0.2627 |            0.0914 |       0.1721 |         0.3777 |              0.3522 |
| VWO       |   0.0000 |            0.0767 |       0.1956 |         0.2569 |              0.0000 |
| TLT       |   0.1373 |            0.0036 |       0.1504 |        -0.1521 |              0.0271 |
| GLD       |   0.3000 |            0.1241 |       0.1475 |         0.6624 |              0.2147 |
| VNQ       |   0.0000 |            0.0679 |       0.2051 |         0.2023 |              0.0000 |
| Portfolio |   1.0000 |            0.1033 |       0.1108 |         0.6935 |              1.0000 |

The cap costs about a fifth of the Sharpe Ratio, 0.69 against 0.89, in exchange for a portfolio that no longer rests on two funds. The minimum variance portfolio has a volatility of 9.5%, below every fund on its own, which is diversification at work. When plotted, the frontier with the four portfolios and each fund on its own:

{% include ft-chart.html id="portfolio-optimization-frontier" src="/assets/data/financetoolkit-guides/portfolio-optimization.json" label="Efficient frontier of six funds with the minimum variance, maximum Sharpe and risk parity portfolios" %}

### Where the Risk Comes From

A portfolio's weights say little about its risk. The risk contribution of an asset is its weight times its marginal contribution to the portfolio volatility, and the contributions add up to that volatility:

$$
RC_i = w_i \, \frac{(\Sigma w)_i}{\sqrt{w^\top \Sigma w}}, \qquad \sum_i RC_i = \sigma_p
$$

To calculate the risk contributions, here of an equally weighted portfolio (pass `weights` for any other):

```python
assets.portfolio.get_risk_contributions()
```

Which gives:

| Asset   |   Weight |   Marginal Contribution |   Risk Contribution |   Percentage Contribution |
|:--------|---------:|------------------------:|--------------------:|--------------------------:|
| VTI     |   0.1667 |                  0.1538 |              0.0256 |                    0.2149 |
| VEA     |   0.1667 |                  0.1515 |              0.0252 |                    0.2116 |
| VWO     |   0.1667 |                  0.1613 |              0.0269 |                    0.2253 |
| TLT     |   0.1667 |                  0.0231 |              0.0038 |                    0.0322 |
| GLD     |   0.1667 |                  0.0585 |              0.0097 |                    0.0817 |
| VNQ     |   0.1667 |                  0.1677 |              0.0279 |                    0.2342 |
| Total   |   1.0000 |                         |              0.1193 |                    1.0000 |

The four equity and real estate funds hold two thirds of the weight but carry 89% of the risk, while Treasuries carry 3% with the same weight: they are nearly uncorrelated with the rest. This gap is what risk parity closes. When plotted, each fund's share of the weight against its share of the risk:

{% include ft-chart.html id="portfolio-optimization-risk" src="/assets/data/financetoolkit-guides/portfolio-optimization.json" label="Weight and share of the risk of each fund in an equally weighted portfolio" %}

### Black-Litterman

Black and Litterman (1992) start from the opposite end: instead of estimating expected returns from history, they derive the returns at which a reference portfolio is optimal, $$\Pi = \delta \Sigma w_{mkt}$$ with risk aversion $$\delta$$, and then move those returns towards the investor's views, each in proportion to its confidence. The result stays close to the reference portfolio wherever there is no view. Views are absolute (VWO returns 10% a year) or relative (gold beats Treasuries by 3% a year). For funds, market capitalizations mean little, so the reference here is a strategic allocation passed as `market_weights`. To calculate the Black-Litterman weights with two views:

```python
strategic_allocation = {"VTI": 0.35, "VEA": 0.15, "VWO": 0.05, "TLT": 0.30, "GLD": 0.10, "VNQ": 0.05}

assets.portfolio.get_black_litterman_weights(
    views={"VWO": 0.10, "GLD-TLT": 0.03},
    view_confidences={"VWO": 0.5, "GLD-TLT": 0.7},
    market_weights=strategic_allocation,
)
```

Which gives:

|     |   Market Weight |   Implied Return |   Black-Litterman Return |   Weight |
|:----|----------------:|-----------------:|-------------------------:|---------:|
| VTI |          0.3500 |           0.0686 |                   0.0822 |   0.3069 |
| VEA |          0.1500 |           0.0655 |                   0.0807 |   0.1306 |
| VWO |          0.0500 |           0.0658 |                   0.0854 |   0.2032 |
| TLT |          0.3000 |           0.0387 |                   0.0280 |   0.0181 |
| GLD |          0.1000 |           0.0402 |                   0.0505 |   0.2793 |
| VNQ |          0.0500 |           0.0690 |                   0.0790 |   0.0620 |

The relative view moves most of the Treasury weight into gold, and the view on emerging markets quadruples their weight, while US equities stay close to their strategic 35%. When plotted, the strategic and Black-Litterman weights and, in the second tab, the implied and Black-Litterman returns:

{% include ft-chart.html id="portfolio-optimization-black-litterman" src="/assets/data/financetoolkit-guides/portfolio-optimization.json" label="Strategic against Black-Litterman weights and implied against Black-Litterman returns of six funds" %}

### Stress Testing

Volatility describes ordinary days; a stress test replays the extraordinary ones. The return of every asset is measured from the peak to the trough of the S&P 500 in each crisis, and the portfolio's return is that of holding the weights throughout. The prices are retrieved per scenario, so the crises do not have to fall within the `Toolkit`'s dates, and `scenarios` adds your own. To replay the risk parity portfolio:

```python
risk_parity_weights = risk_parity["Weight"].drop("Portfolio").to_dict()

stress_test = assets.portfolio.get_stress_test(weights=risk_parity_weights)

stress_test[["Portfolio Return", "Benchmark Return"]]
```

Which gives, for the crises in which all six funds were listed:

| Scenario                |   Portfolio Return |   Benchmark Return |
|:------------------------|-------------------:|-------------------:|
| Global Financial Crisis |            -0.1841 |            -0.5519 |
| Euro Area Debt Crisis   |            -0.0110 |            -0.1861 |
| 2015-2016 Sell-off      |            -0.0530 |            -0.1298 |
| 2018 Q4 Sell-off        |            -0.0486 |            -0.1935 |
| COVID-19 Crash          |            -0.1435 |            -0.3372 |
| 2022 Rate Shock         |            -0.2381 |            -0.2450 |

In every crisis but one, Treasuries rose while equities fell, and the portfolio lost less than half of what the S&P 500 lost. The exception is 2022, when rising rates hit stocks and bonds at once and the portfolio fell almost as far as the market. When plotted:

{% include ft-chart.html id="portfolio-optimization-stress" src="/assets/data/financetoolkit-guides/portfolio-optimization.json" label="Return of the risk parity portfolio and the S&P 500 in six historical crises" %}

### Looking Through Funds

A portfolio of funds and stocks often holds more of the same than its positions suggest. The look-through exposure spreads each fund's weight over its own sectors, countries or holdings, counts each stock fully towards its own, and sums everything, with the benchmark next to it. To look through a portfolio of two funds and three stocks, by sector and by holding:

```python
mixed = Toolkit(["QQQ", "XLV", "AAPL", "MSFT", "JPM"], api_key="FINANCIAL_MODELING_PREP_KEY")

mixed_weights = {"QQQ": 0.4, "XLV": 0.2, "AAPL": 0.15, "MSFT": 0.15, "JPM": 0.1}

sector_exposure = mixed.portfolio.get_look_through_exposure(weights=mixed_weights)
holdings_exposure = mixed.portfolio.get_look_through_exposure(weights=mixed_weights, by="holdings")
```

Which gives by sector:

| Sector                 |   Exposure |   Benchmark Exposure |   Active Exposure |
|:-----------------------|-----------:|---------------------:|------------------:|
| Technology             |     0.5358 |               0.3757 |            0.1601 |
| Healthcare             |     0.2157 |               0.0994 |            0.1163 |
| Financial Services     |     0.1008 |               0.1208 |           -0.0200 |
| Communication Services |     0.0464 |               0.0923 |           -0.0459 |
| Consumer Cyclical      |     0.0421 |               0.0896 |           -0.0475 |
| Consumer Defensive     |     0.0250 |               0.0495 |           -0.0245 |
| Industrials            |     0.0230 |               0.0803 |           -0.0573 |
| Utilities              |     0.0044 |               0.0204 |           -0.0160 |
| Basic Materials        |     0.0039 |               0.0170 |           -0.0131 |
| Energy                 |     0.0019 |               0.0373 |           -0.0354 |
| Cash & Others          |     0.0009 |               0.0000 |            0.0009 |
| Real Estate            |     0.0000 |               0.0175 |           -0.0175 |

The 15% positions in Apple and Microsoft become 18.2% and 17.5% once the Nasdaq 100 fund is looked through, and more than half of the portfolio sits in technology, 16 percentage points more than in the S&P 500. When plotted, the sector exposure against the S&P 500 and, in the second tab, the ten largest holdings after looking through:

{% include ft-chart.html id="portfolio-optimization-look-through" src="/assets/data/financetoolkit-guides/portfolio-optimization.json" label="Look-through sector exposure against the S&P 500 and the largest holdings of a portfolio of funds and stocks" %}

### Brinson Attribution

The Brinson-Fachler attribution (Brinson and Fachler, 1985) explains the return over the benchmark by sector. With $$w_s$$ and $$b_s$$ the portfolio and benchmark weight of sector $$s$$, $$r_s$$ and $$\bar{r}_s$$ their returns in that sector and $$\bar{r}$$ the benchmark's total return:

$$
\text{Allocation}_s = (w_s - b_s)(\bar{r}_s - \bar{r}), \qquad \text{Selection}_s = b_s (r_s - \bar{r}_s), \qquad \text{Interaction}_s = (w_s - b_s)(r_s - \bar{r}_s)
$$

Allocation rewards overweighting sectors that beat the benchmark, selection rewards holding better stocks within a sector, and the three effects add up to the excess return. To attribute the 2025 return of a stock portfolio against the S&P 500:

```python
stocks = Toolkit(
    ["AAPL", "MSFT", "NVDA", "JNJ", "LLY", "JPM", "XOM"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

stock_weights = {"AAPL": 0.2, "MSFT": 0.2, "NVDA": 0.15, "JNJ": 0.1, "LLY": 0.1, "JPM": 0.15, "XOM": 0.1}

brinson_attribution = stocks.portfolio.get_brinson_attribution(weights=stock_weights)

brinson_attribution[["Portfolio Weight", "Benchmark Weight", "Allocation Effect", "Selection Effect", "Interaction Effect", "Total Effect"]]
```

Which gives:

| Sector                 |   Portfolio Weight |   Benchmark Weight |   Allocation Effect |   Selection Effect |   Interaction Effect |   Total Effect |
|:-----------------------|-------------------:|-------------------:|--------------------:|-------------------:|---------------------:|---------------:|
| Basic Materials        |             0.0000 |             0.0170 |              0.0012 |             0.0000 |               0.0000 |         0.0012 |
| Communication Services |             0.0000 |             0.0923 |             -0.0042 |             0.0000 |               0.0000 |        -0.0042 |
| Consumer Cyclical      |             0.0000 |             0.0896 |              0.0082 |             0.0000 |               0.0000 |         0.0082 |
| Consumer Defensive     |             0.0000 |             0.0495 |              0.0080 |             0.0000 |               0.0000 |         0.0080 |
| Energy                 |             0.1000 |             0.0373 |             -0.0071 |             0.0036 |               0.0060 |         0.0025 |
| Financial Services     |             0.1500 |             0.1208 |             -0.0008 |             0.0265 |               0.0064 |         0.0320 |
| Healthcare             |             0.2000 |             0.0994 |             -0.0035 |             0.0290 |               0.0293 |         0.0548 |
| Industrials            |             0.0000 |             0.0803 |             -0.0014 |             0.0000 |               0.0000 |        -0.0014 |
| Real Estate            |             0.0000 |             0.0175 |              0.0025 |             0.0000 |               0.0000 |         0.0025 |
| Technology             |             0.5500 |             0.3758 |              0.0120 |            -0.0190 |              -0.0088 |        -0.0158 |
| Utilities              |             0.0000 |             0.0204 |              0.0006 |             0.0000 |               0.0000 |         0.0006 |
| Total                  |             1.0000 |             1.0000 |              0.0155 |             0.0400 |               0.0329 |         0.0884 |

The portfolio returned 26.8% against 18.0% for the S&P 500. Most of the 8.8 percentage points came from picking stocks in healthcare and financials, while the overweight in technology was the right sector with the wrong stocks: Apple, Microsoft and Nvidia together lagged the sector. When plotted, the three effects per sector:

{% include ft-chart.html id="portfolio-optimization-brinson" src="/assets/data/financetoolkit-guides/portfolio-optimization.json" label="Allocation, selection and interaction effect per sector of a stock portfolio against the S&P 500" %}

The module covers more than shown here, among them [mean-variance weights](/projects/financetoolkit/docs/portfolio-optimization/mean-variance) for a target return or a risk aversion, [risk parity](/projects/financetoolkit/docs/portfolio-optimization/risk-parity) with a risk budget of your own, the linkage method of [Hierarchical Risk Parity](/projects/financetoolkit/docs/portfolio-optimization/hierarchical-risk-parity) and the confidence level of [minimum CVaR](/projects/financetoolkit/docs/portfolio-optimization/minimum-cvar). To follow a portfolio over time, with its transactions and rebalancing, see the [Portfolio](/projects/financetoolkit/docs/portfolio) module.

{% include ft-charts-script.html %}
