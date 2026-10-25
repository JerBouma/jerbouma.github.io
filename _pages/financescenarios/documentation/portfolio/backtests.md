---
title: Backtests
seo_title: "Backtests | Finance Scenarios"
seo_title_suffix: false
excerpt: "How Finance Scenarios checks a portfolio against history: the same rules run on what prices did, several mixes on one shared calendar, a benchmark comparison and a Fama-French factor regression."
description: "Backtests in Finance Scenarios: realized history as one scenario, a shared calendar for several mixes, tracking error, beta, Sharpe ratio and active share, and Fama-French three- and five-factor exposure."
author_profile: false
permalink: /projects/financescenarios/docs/portfolio/backtests
classes: wide-sidebar
layout: single
docs_module_url: /projects/financescenarios/docs/portfolio
redirect_from:
    - /projects/financescenarios/portfolio-analysis-notebook
    - /projects/financescenarios/docs/reference/history-and-metrics
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs-portfolio"
---

A simulation says what could happen; a backtest says what did. The same rebalancing, cashflow and fee rules that run on the scenarios run on realized history as one path, so a mix can be checked against what its holdings actually did, set against a benchmark, and regressed on the factors that explain its returns.

## A Backtest {#backtesting-against-history}

`Portfolio.backtest` runs each mix through realized prices, as one historical scenario per mix. Several mixes share one calendar, the dates on which every holding of every mix has a price, so no mix skips a crisis the others go through; a holding with a short history shortens the window for all of them. With one path, statistics across scenarios (Value at Risk, Expected Shortfall, success rates) collapse to a single number, while CAGR, volatility, drawdown and factor exposure stay fully meaningful.

<div class="fs-callout" markdown="1">
Use a backtest as a check on the simulation, not as a forecast.
</div>

The examples on this page use the default settings and factor set of the [overview](/projects/financescenarios/docs#simulating-scenarios), whose history the backtest reads. To backtest three mixes, rebalanced once a year:

```python
from financescenarios import Portfolio, Scenarios

scenarios = Scenarios.from_profiles(
    settings="default", factor_set="default", api_key="FINANCIAL_MODELING_PREP_KEY"
)

backtest = Portfolio.backtest(scenarios, ["balanced_60_40", "all_weather", "permanent_portfolio"])
history = backtest.compute(initial_value=100_000, rebalance_every=12)

backtest.risk_metrics(history)  # one row per mix
```

From August 2000 to October 2026, 100,000 grew to 545,686 in the 60/40, 542,849 in All Weather and 551,770 in the Permanent Portfolio, about 6.7% a year each, but on different roads: the deepest falls were 27.8%, 21.1% and 15.0%. When plotted:

{% include ft-chart.html id="portfolio-backtest" src="/assets/data/financescenarios-guides/portfolio.json" label="Value of 100,000 in the 60/40, All Weather and the Permanent Portfolio month by month since August 2000, rebalanced once a year" %}

## Factor Exposure

Factor exposure shows how a portfolio actually behaved over history, which is how a mandate is checked or performance explained.

<div class="fs-facts">
  <div><span>Input</span><b>Realized returns (a backtest)</b></div>
  <div><span>Method</span><b>Ordinary least squares on excess returns</b></div>
  <div><span>Model</span><b>Fama-French five factors (default) or three</b></div>
  <div><span>Data</span><b>Kenneth French's Data Library</b></div>
</div>

The portfolio's excess return is regressed on the Fama-French factors by ordinary least squares:

$$
R_t - R_{f,t} = \alpha + \sum_i \beta_i F_{i,t} + \varepsilon_t
$$

where $$R_t - R_{f,t}$$ is the return above the risk-free rate, $$\alpha$$ the part the factors do not explain, and $$\beta_i$$ the loading on factor $$F_i$$: the market (Mkt-RF), small versus large companies (SMB), cheap versus expensive (HML), robust versus weak profitability (RMW) and companies that invest conservatively versus aggressively (CMA). The model is the five-factor one of [Fama and French (2015)](https://doi.org/10.1016/j.jfineco.2014.10.010){:target="_blank"} by default, or the three-factor one of [Fama and French (1993)](https://doi.org/10.1016/0304-405X(93)90023-5){:target="_blank"}, with factor data from Kenneth French's [Data Library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html){:target="_blank"}, which defines each factor in its [description of the Fama/French 5 factors (2x3)](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/f-f_5_factors_2x3.html){:target="_blank"}.

`factor_exposure` runs the regression on each mix's monthly returns, bought and held over the backtest's dates, or on a computed path such as a rebalanced one. To calculate it for the three mixes:

```python
backtest.factor_exposure()
```

Which returns, with $$\alpha$$ a monthly return:

| portfolio | Mkt-RF | SMB | HML | RMW | CMA | alpha | r_squared | observations |
|:----------|-------:|----:|----:|----:|----:|------:|----------:|-------------:|
| 60/40 Balanced | 0.5369 | -0.0687 | -0.0447 | 0.1215 | -0.0116 | 0.0007 | 0.8615 | 312 |
| All Weather | 0.2039 | -0.0620 | -0.1435 | 0.2162 | 0.0335 | 0.0029 | 0.1318 | 312 |
| Permanent Portfolio | 0.2173 | -0.0615 | -0.1418 | 0.2017 | 0.0473 | 0.0033 | 0.1240 | 312 |

The 60/40 carries a market beta of 0.54, close to its 60% in stocks and more than twice that of the other two, and the five factors explain 86% of its moves against 13% and 12% of theirs. As a check, the same regression on 100% US stocks gives a beta of 1.00 and an R-squared of 0.99. A "balanced" portfolio with a beta near 1 would be an equity portfolio in disguise. When plotted:

{% include ft-chart.html id="portfolio-exposure" src="/assets/data/financescenarios-guides/portfolio.json" label="Loadings of the 60/40, All Weather and the Permanent Portfolio on the five Fama-French factors, August 2000 to October 2026" %}

<div class="fs-callout fs-callout--limits" markdown="1">
<p class="fs-callout__title">Limits</p>

- Only realized returns can be regressed; a simulated scenario has no calendar to line up with real factor history.
- The factors are US equity factors. A non-US portfolio's betas describe its co-movement with the US market, not its own market's style.
- The three- and five-factor files build SMB differently, so the two models give slightly different size betas.
</div>

## Benchmarks

Against a benchmark, another mix or an index, `benchmark` measures how far a portfolio strays and what it earns for it. With $$r_{p,t}$$ and $$r_{b,t}$$ the portfolio's and the benchmark's returns over each period and $$P$$ periods a year:

| Measure | Formula |
|:--|:--|
| Tracking error | $$\operatorname{sd}(r_{p,t} - r_{b,t})\,\sqrt{P}$$ |
| Beta | $$\operatorname{cov}(r_{p,t}, r_{b,t}) / \operatorname{var}(r_{b,t})$$ |
| Relative CAGR | The portfolio's CAGR less the benchmark's |
| Relative Sharpe ratio | The difference of $$\overline{r}/\operatorname{sd}(r)\,\sqrt{P}$$, the return per unit of risk of [Sharpe (1966)](https://doi.org/10.1086/294846){:target="_blank"}, here without subtracting a risk-free rate |
| Active share | $$\tfrac{1}{2}\sum_k \lvert w_{p,k} - w_{b,k}\rvert$$, half the sum of the absolute weight differences ([Cremers and Petajisto, 2009](https://doi.org/10.1093/rfs/hhp057){:target="_blank"}), for mixes with constant weights |

On a backtest every measure reads the one realized path. On simulated runs that share their scenarios and seed, every measure is taken within each scenario, the way an investor lives through it, and the median is reported, with the tracking error's spread across scenarios; averaging the scenarios first would cancel most of the deviations. Two different runs compare their mean paths. Deposits and withdrawals are taken out of each period's return, $$r_t = (V_t - C_t)/V_{t-1} - 1$$, and the CAGR is the time-weighted one, as in `risk_metrics`, so a saver's deposits don't read as outperformance.

To compare the three mixes with holding US stocks only:

```python
stocks_only = backtest.compute({"us_broad": 1.0}, initial_value=100_000, rebalance_every=12)

backtest.benchmark(history, stocks_only, benchmark_weights={"us_broad": 1.0})
```

Which returns:

| portfolio | tracking_error | correlation | beta | relative_cagr | relative_sharpe_ratio | active_share |
|:----------|---------------:|------------:|-----:|--------------:|----------------------:|-------------:|
| 60/40 Balanced | 0.0688 | 0.9724 | 0.5628 | -0.0154 | 0.1865 | 0.4000 |
| All Weather | 0.1365 | 0.4311 | 0.2266 | -0.0156 | 0.2552 | 0.7000 |
| Permanent Portfolio | 0.1329 | 0.4690 | 0.2170 | -0.0150 | 0.3711 | 0.7500 |

Each mix gave up about 1.5 percentage points a year of return against stocks alone and improved its Sharpe ratio, the Permanent Portfolio the most, by 0.37.

## References

<details class="ft-details" markdown="1">
<summary><i class="fas fa-book"></i> <b>Papers and sources cited on this page</b> <span class="ft-details__meta">6</span></summary>

- Cremers, K.J.M., Petajisto, A. (2009). "How Active Is Your Fund Manager? A New Measure That Predicts Performance." Review of Financial Studies, 22(9), 3329-3365. [https://doi.org/10.1093/rfs/hhp057](https://doi.org/10.1093/rfs/hhp057){:target="_blank"}
- Fama, E.F., French, K.R. (1993). "Common Risk Factors in the Returns on Stocks and Bonds." Journal of Financial Economics, 33(1), 3-56. [doi.org](https://doi.org/10.1016/0304-405X(93)90023-5){:target="_blank"}
- Fama, E.F., French, K.R. (2015). "A five-factor asset pricing model." Journal of Financial Economics, 116(1), 1-22. [https://doi.org/10.1016/j.jfineco.2014.10.010](https://doi.org/10.1016/j.jfineco.2014.10.010){:target="_blank"}
- Kenneth R. French. Data Library. [mba.tuck.dartmouth.edu](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html){:target="_blank"}
- Kenneth R. French. Description of Fama/French 5 Factors (2x3). [mba.tuck.dartmouth.edu](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/f-f_5_factors_2x3.html){:target="_blank"}
- Sharpe, W.F. (1966). "Mutual Fund Performance." The Journal of Business, 39(S1), 119-138. [https://doi.org/10.1086/294846](https://doi.org/10.1086/294846){:target="_blank"}

</details>

{% include ft-charts-script.html %}
