---
title: "Risk"
seo_title: "Risk Guide | Finance Toolkit"
seo_title_suffix: false
excerpt: "How to measure tail risk, drawdowns and volatility of stocks and a benchmark with the Finance Toolkit's Risk module."
description: "Measure Value at Risk, Conditional VaR, drawdowns, the Ulcer Index, EWMA volatility and the Hurst Exponent in Python with the Finance Toolkit."
author_profile: false
permalink: /projects/financetoolkit/docs/getting-started/risk
classes: wide-sidebar
layout: single
redirect_from:
  - /projects/financetoolkit/risk-notebook
sidebar:
  nav: "financetoolkit-guides"
---

The Risk module answers the question that comes before any return figure: what could go wrong, and how badly? It calculates Value at Risk (VaR), Conditional Value at Risk (CVaR), drawdown measures, the Ulcer Index, EWMA and GARCH volatility, the Hurst Exponent and more, for every ticker you load and for the benchmark next to them. Every metric works on the same historical data, so you can look at it per week, month, quarter or year without preparing anything yourself.

This guide uses Microsoft, Apple, Amazon and Meta from 2013 onwards, with the S&P 500 as the benchmark.

## Loading the Data

The Risk module is part of the `Toolkit` class, so the only setup is choosing the tickers and the start date. To load the data for the four companies:

```python
from financetoolkit import Toolkit

companies = Toolkit(
    ["MSFT", "AAPL", "AMZN", "META"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2013-01-01",
)
```

The historical prices and the treasury rates are collected the first time you call a risk function and reused for every call after that.

## Value at Risk and Conditional Value at Risk

Value at Risk is the loss that is not exceeded with a given probability: with the default `alpha=0.05`, a monthly VaR of -8% means that in 95% of months the return was better than -8%. Conditional Value at Risk (also called Expected Shortfall) is the average loss in the months that were worse than the VaR. VaR tells you where the tail starts, CVaR tells you how heavy it is, which is why risk managers and regulators increasingly prefer the latter.

The `period` parameter sets the return frequency. Without anything else, you get one figure per ticker for the whole sample, based on its monthly returns. To calculate both for monthly returns since 2013:

```python
value_at_risk = companies.risk.get_value_at_risk(period="monthly")

conditional_value_at_risk = companies.risk.get_conditional_value_at_risk(period="monthly")
```

Which gives the following, with Meta the riskiest of the four on both measures and the S&P 500, as a diversified index, the least risky:

|           |   VaR (95%) |   CVaR (95%) |
|:----------|------------:|-------------:|
| MSFT      |       -7.8% |       -10.7% |
| AAPL      |      -11.0% |       -12.8% |
| AMZN      |      -10.8% |       -14.2% |
| META      |      -11.9% |       -17.9% |
| Benchmark |       -6.0% |        -8.3% |

With `within_period=True` the module instead calculates the metric for each period from the daily returns within it, so you see how the daily tail risk changed from month to month. Adding `rolling=12` turns the monthly VaR into a rolling twelve-month window, which smooths out a single calm or turbulent month. To calculate all three:

```python
monthly_var = companies.risk.get_value_at_risk(period="monthly", within_period=True)

monthly_cvar = companies.risk.get_conditional_value_at_risk(period="monthly", within_period=True)

rolling_var = companies.risk.get_value_at_risk(period="monthly", rolling=12)
```

Which shows the spikes in tail risk around the COVID-19 crash of March 2020 and the 2022 sell-off, with the tabs switching between the three views:

{% include ft-chart.html id="risk-var" src="/assets/data/financetoolkit-guides/risk.json" label="Monthly VaR, CVaR and rolling 12-month VaR of Microsoft, Apple, Amazon, Meta and the S&P 500" %}

VaR also accepts `distribution="gaussian"`, `"studentt"`, `"cornish-fisher"` or `"evt"` (a Peak-over-Threshold fit for the tail) when you'd rather not rely on the historical distribution alone.

## The Ulcer Index and Growth

The Ulcer Index measures the depth and duration of declines from the most recent high, so it only punishes downside volatility. Each function accepts `growth=True` (and a `lag`) to show the change over time instead of the level, which makes it easy to see in which years the stress rose. To calculate the year-on-year change in the Ulcer Index:

```python
companies.risk.get_ulcer_index(period="yearly", growth=True)
```

Which shows 2022 standing out, when the Ulcer Index of the S&P 500 more than tripled and that of Meta roughly tripled, followed by a sharp fall in 2023 as markets recovered:

{% include ft-chart.html id="risk-ulcer" src="/assets/data/financetoolkit-guides/risk.json" label="Year-on-year change in the Ulcer Index" %}

## Conditional Drawdown at Risk and the Tail Ratio

VaR and CVaR look at returns one period at a time. The Conditional Drawdown at Risk (CDaR) applies the same idea to the drawdown series: rather than asking how bad one period could be, it asks how deep the cumulative peak-to-trough loss could get. That is the measure that matters to an investor who holds through a bad stretch. The Tail Ratio compares the size of the best-case tail of returns (the 95th percentile) to the worst-case tail (the 5th percentile); above 1 means the gains outsize the losses.

To calculate the quarterly CDaR and the yearly Tail Ratio:

```python
conditional_drawdown_at_risk = companies.risk.get_conditional_drawdown_at_risk(
    period="quarterly", within_period=True
)

tail_ratio = companies.risk.get_tail_ratio(period="yearly", within_period=True)
```

Which gives the following, where the Tail Ratio dropped below 1 for every ticker in 2022 and rose above it for every ticker in 2023:

{% include ft-chart.html id="risk-cdar-tail" src="/assets/data/financetoolkit-guides/risk.json" label="Quarterly Conditional Drawdown at Risk and yearly Tail Ratio" %}

## Drawdown Duration and Recovery Time

The size of a drawdown is only half the story; how long it lasts matters just as much to anyone who has to explain it. The Maximum Drawdown Duration is the number of trading days the worst decline in each period took, from the peak to the trough. The Maximum Drawdown Recovery Time is the number of trading days it then took to get back to the previous high, and is empty when the price had not recovered by the end of the period. To calculate both per year:

```python
drawdown_duration = companies.risk.get_maximum_drawdown_duration(
    period="yearly", within_period=True
)

recovery_time = companies.risk.get_maximum_drawdown_recovery_time(
    period="yearly", within_period=True
)
```

Which shows 2022 as the year in which the worst decline lasted for most of the year (around 200 to 250 trading days for every ticker) without a recovery before year-end:

{% include ft-chart.html id="risk-drawdown-duration" src="/assets/data/financetoolkit-guides/risk.json" label="Maximum drawdown duration and recovery time per year in trading days" %}

## EWMA Volatility and the Hurst Exponent

The EWMA volatility follows the RiskMetrics methodology: it weights recent returns more heavily than older ones (with a decay factor `lambda_` of 0.94 by default), so it reacts to a change in the volatility regime much faster than a fixed rolling window. The Hurst Exponent says something about the character of a return series: below 0.5 it tends to mean-revert, around 0.5 it behaves like a random walk and above 0.5 it tends to trend.

To calculate the daily EWMA volatility and the Hurst Exponent of each ticker:

```python
ewma_volatility = companies.risk.get_ewma_volatility()

hurst_exponent = companies.risk.get_hurst_exponent()
```

The EWMA volatility below is shown at the end of each week, and peaks in March 2020 for Microsoft, Apple and the S&P 500 at a daily volatility of 5% to 7%:

{% include ft-chart.html id="risk-ewma" src="/assets/data/financetoolkit-guides/risk.json" label="EWMA volatility of Microsoft, Apple, Amazon, Meta and the S&P 500" %}

The Hurst Exponent is one number per ticker, and for these five it ends up between about 0.46 and 0.49, just under 0.5. Daily returns of large, liquid stocks behave close to a random walk, with at most a slight tendency to mean-revert.

## Returns against the Maximum Drawdown

Putting the returns next to the drawdowns shows how much pain came with the gains. To get the weekly returns and the maximum drawdown in each quarter:

```python
weekly_returns = companies.get_historical_data(period="weekly")["Return"]

maximum_drawdown = companies.risk.get_maximum_drawdown(period="quarterly", within_period=True)
```

The weekly returns look like noise around zero, with the large moves clustered in a few turbulent periods:

{% include ft-chart.html id="risk-returns" src="/assets/data/financetoolkit-guides/risk.json" label="Weekly returns of Microsoft, Apple, Amazon, Meta and the S&P 500" %}

The quarterly maximum drawdown makes those periods explicit. The S&P 500 lost about a third of its value within the first quarter of 2020, and Meta's worst quarter, early 2022, came with a drawdown of about 45%:

{% include ft-chart.html id="risk-max-drawdown" src="/assets/data/financetoolkit-guides/risk.json" label="Maximum drawdown per quarter" %}

## Using the Risk Models with Your Own Data

Every metric in the module is a plain function underneath, which you can call on any pandas Series or DataFrame of returns. That is useful for a fund's own return history, a backtest or simulated returns that don't come from a ticker. The models live in `financetoolkit.risk`. To calculate a set of statistics for four series of random returns:

```python
import random

import pandas as pd

from financetoolkit.risk import evar_model, risk_model, var_model

return_statistics = {}

for seed, stock_name in enumerate(["Stock A", "Stock B", "Stock C", "Stock D"], start=1):
    random.seed(seed)
    returns = pd.Series([random.randint(-15, 15) / 100 for _ in range(100)])

    return_statistics[stock_name] = {
        "Standard Deviation": returns.std(),
        "Skewness": risk_model.get_skewness(returns=returns),
        "Kurtosis": risk_model.get_kurtosis(returns=returns),
        "Max Drawdown": risk_model.get_max_drawdown(returns=returns),
        "Value at Risk": var_model.get_var_historic(returns=returns, alpha=0.05),
        "Entropic Value at Risk": evar_model.get_evar_gaussian(returns=returns, alpha=0.05),
    }

pd.DataFrame(return_statistics).round(4)
```

Which returns the statistics per series, with a negative (excess) kurtosis as you would expect from uniformly distributed returns, and the Entropic VaR as the most conservative of the tail measures:

|                    |   Stock A |   Stock B |   Stock C |   Stock D |
|:-------------------|----------:|----------:|----------:|----------:|
| Standard Deviation |    0.0934 |    0.0889 |    0.0865 |    0.0938 |
| Skewness           |   -0.1721 |   -0.0527 |   -0.1820 |    0.1677 |
| Kurtosis           |   -1.1688 |   -1.1309 |   -1.0048 |   -1.3330 |
| Max Drawdown       |   -0.5058 |   -0.6082 |   -0.4528 |   -0.6631 |
| Value at Risk      |   -0.1500 |   -0.1305 |   -0.1305 |   -0.1400 |
| Entropic Value at Risk |   -0.2176 |   -0.2023 |   -0.1970 |   -0.2311 |

The module covers many more metrics than shown here, among them [GARCH](/projects/financetoolkit/docs/risk#get_garch), [GJR-GARCH](/projects/financetoolkit/docs/risk#get_gjr_garch) and [EGARCH](/projects/financetoolkit/docs/risk#get_egarch) with forecasts, [copulas](/projects/financetoolkit/docs/risk#get_best_fitting_copula), [CoVaR](/projects/financetoolkit/docs/risk#get_covar), [marginal](/projects/financetoolkit/docs/risk#get_marginal_value_at_risk) and [component VaR](/projects/financetoolkit/docs/risk#get_component_value_at_risk) and [VaR backtests](/projects/financetoolkit/docs/risk#get_var_backtest).

<div class="fs-ref"><a href="/projects/financetoolkit/docs/risk"><i class="fas fa-book" aria-hidden="true"></i>Full reference: Risk</a></div>

{% include ft-charts-script.html %}
