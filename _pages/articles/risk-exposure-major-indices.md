---
title: Understanding Risk Exposure Across Major Indices
seo_title: "Risk Exposure Across Major Indices"
date: 2026-07-21
last_modified_at: 2026-11-17
permalink: /articles/risk-exposure-major-indices-finance-toolkit
excerpt: "Compare Value at Risk, Conditional Value at Risk, maximum drawdown, skewness, and kurtosis across the S&P 500, Nasdaq 100, Dow Jones, Russell 2000, EAFE, and Emerging Markets with the Finance Toolkit."
description: "Measure tail risk across SPY, QQQ, DIA, IWM, EFA and EEM with Value at Risk, CVaR, maximum drawdown, skewness and kurtosis in the Finance Toolkit."
layout: single
classes: wide-sidebar article-document
author_profile: false
collection: article
tags: [Risk & Derivatives]
share: true
---

On April 4, 2025, two days after the US tariff announcement, the S&P 500 ETF fell 5.85% in a single day. Five days later, on April 9, it rose 10.5%. Between 2019 and 2025 these six indices only had daily falls of that size during the 2020 COVID crash and in those April days. Outside of them, 2025 was a fairly normal year. Those few days are enough to push the S&P 500's kurtosis for the year to 26.6, roughly nine times its reading in a calmer year like 2023. Leave out the six trading days from April 3 to April 10 and it drops to 4.4. Volatility alone would not show this, but kurtosis does.

That is a good reason to look beyond plain volatility when measuring risk. The Finance Toolkit's risk module covers Value at Risk, Conditional Value at Risk, maximum drawdown, the Ulcer Index, GARCH volatility, skewness, and kurtosis, each describing a different shape of risk that a single standard deviation number flattens into one figure. In this article I run five of them across six major indices: the S&P 500 (SPY), Nasdaq 100 (QQQ), Dow Jones (DIA), Russell 2000 (IWM), MSCI EAFE developed markets (EFA), and MSCI Emerging Markets (EEM). The data covers the daily returns of 2019 through 2025 and comes from the [Finance Toolkit](https://github.com/JerBouma/FinanceToolkit){:target="_blank"}, with prices from Financial Modeling Prep (you can get a key at [jeroenbouma.com/fmp](/fmp){:target="_blank"}). Every chart has a Python button with the code behind it and an MCP button with a question for the [Finance Toolkit MCP server](/projects/financetoolkit/mcp) that gets the same data.

## Value at Risk and Conditional VaR: How Bad Could a Bad Day Get?

Value at Risk (VaR) at the 95% confidence level answers one specific question: on the worst 5% of trading days, how much do you lose at least? Conditional Value at Risk (CVaR) answers the harder follow-up: once you are already in that worst 5%, how much do you actually lose on average? CVaR is always worse than VaR; the question is by how much.

The Value at Risk and Conditional Value at Risk of each index per year:

{% capture code_var %}
```python
# pip install financetoolkit
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["SPY", "QQQ", "DIA", "IWM", "EFA", "EEM"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2019-01-01", end_date="2025-12-31", benchmark_ticker=None)

var = toolkit.risk.get_value_at_risk(period="yearly", within_period=True)
cvar = toolkit.risk.get_conditional_value_at_risk(period="yearly", within_period=True)
```
{% endcapture %}
{% include ft-chart.html id="risk-var" src="/assets/data/article-charts.json" label="Value at Risk and Conditional Value at Risk" code=code_var mcp="What were the Value at Risk and Conditional Value at Risk at the 95 percent confidence level of SPY, QQQ, DIA, IWM, EFA and EEM, measured within each calendar year from 2019 to 2025, and in which years does the gap between the two widen the most?" %}

IWM has the worst or second-worst CVaR in every year, including 2024 at -2.9% when most other indices were calm, which shows that small-cap stress can build even when large-cap headlines stay quiet. The gap between VaR and CVaR says more: for SPY in 2020, VaR was -3.15% but CVaR was -5.45%, so the average day inside the worst 5% was about 1.7 times as bad as the threshold itself. That gap widens in every index in 2020, to about 3 percentage points for IWM and EEM, and again in 2025 because of the April days. 2022, the other deep drawdown year, has worse VaR readings but a gap close to 2019's, which fits a bear market made of many bad days rather than a few extreme ones. For most indices the gap is narrowest in 2023, when SPY's CVaR was only 0.2 percentage points below its VaR.

## Maximum Drawdown: The Worst Case Each Index Actually Lived Through

VaR and CVaR are statistical estimates, whereas maximum drawdown is the actual peak-to-trough loss an investor in each index lived through.

The maximum drawdown of each index per year:

{% capture code_drawdown %}
```python
# pip install financetoolkit
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["SPY", "QQQ", "DIA", "IWM", "EFA", "EEM"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2019-01-01", end_date="2025-12-31", benchmark_ticker=None)

max_drawdown = toolkit.risk.get_maximum_drawdown(period="yearly", within_period=True)
```
{% endcapture %}
{% include ft-chart.html id="risk-drawdown" src="/assets/data/article-charts.json" label="Maximum drawdown per year" code=code_drawdown mcp="What was the maximum drawdown of SPY, QQQ, DIA, IWM, EFA and EEM within each calendar year from 2019 to 2025, which index had the single worst drawdown and which was the most resilient?" %}

2020's COVID crash hit IWM hardest at -41.1%, deeper than any other index in any year of this dataset, consistent with small-caps having less balance sheet cushion and less liquid trading during a panic. DIA, by contrast, never has the worst drawdown of any year. Its blue-chip composition made it the most resilient of the six in 2022 (-20.8%), although in the 2020 crash only IWM fell further. In the 2022 bear market it was tech's turn: QQQ's -34.8% drawdown was the worst of that year, driven by the same rate-hike sensitivity that put growth stocks at the center of the selloff. EEM had the worst showing in 2019 and 2021, both years with no broad global crisis, which shows that emerging markets can draw down on their own schedule, independent of US conditions.

## Skewness: Which Years Had Fatter Downside Than Upside

Skewness measures asymmetry. A return distribution with negative skew has a longer, fatter left tail, infrequent but severe losses outweighing the frequency of gains. Positive skew is the opposite: frequent small losses, occasional large gains.

The skewness of each index's returns per year:

{% capture code_skew %}
```python
# pip install financetoolkit
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["SPY", "QQQ", "DIA", "IWM", "EFA", "EEM"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2019-01-01", end_date="2025-12-31", benchmark_ticker=None)

skewness = toolkit.risk.get_skewness(period="yearly", within_period=True)
```
{% endcapture %}
{% include ft-chart.html id="risk-skew" src="/assets/data/article-charts.json" label="Skewness of daily returns" code=code_skew mcp="What was the skewness of the returns of SPY, QQQ, DIA, IWM, EFA and EEM within each calendar year from 2019 to 2025, and which years show the most negative skew?" %}

Every index ran negative in 2019 and 2020, two years with sharp, sudden selloffs (the trade-war days of August 2019 and the COVID crash) rather than steady grinding declines. EFA and EEM show the most extreme negative skew of the whole chart in 2020, at -1.21 and -1.24, consistent with international markets taking a sharper, more concentrated hit than US large caps that year. In 2022 skew turns mildly positive for five of the six, since that bear market ground lower day after day rather than crashing in a handful of sessions. That is the opposite shape of risk from 2020, even though every index still fell between 20% and 35% from its peak. 2025's positive skew across the board, led by SPY at 1.51, comes mostly from one day: the 10.5% jump on April 9, when the tariffs were paused. Leave that day out and SPY's skewness for 2025 flips to -1.51.

## Kurtosis: Why 2025 Doesn't Look Like a Normal Year

Kurtosis measures how fat the tails are relative to a normal distribution, regardless of which direction. High kurtosis means more extreme days than a bell curve would predict, in either direction. A normal distribution has a kurtosis of 3.

The kurtosis of each index's returns per year:

{% capture code_kurtosis %}
```python
# pip install financetoolkit
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["SPY", "QQQ", "DIA", "IWM", "EFA", "EEM"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2019-01-01", end_date="2025-12-31", benchmark_ticker=None)

kurtosis = toolkit.risk.get_kurtosis(period="yearly", within_period=True)
```
{% endcapture %}
{% include ft-chart.html id="risk-kurtosis" src="/assets/data/article-charts.json" label="Kurtosis of daily returns" code=code_kurtosis mcp="What was the kurtosis of the returns of SPY, QQQ, DIA, IWM, EFA and EEM within each calendar year from 2019 to 2025, and which year and index show the most extreme tails?" %}

This is where the April 2025 tariff shock shows up most clearly. SPY's kurtosis of 26.6 in 2025 is more than double the highest reading of any other year (EFA's 11.9 in 2020), and roughly nine times its calmest year (2023, at 2.84). QQQ and EFA show the same pattern, both above 20, while IWM's 2025 kurtosis of 8.89 is the lowest of the six. Small caps already moved more on an ordinary day, so the April days stood out less against the rest of the year. 2020 is the only other year that comes close, when four of the six indices posted double-digit kurtosis during the COVID crash. It is worth reading this next to the skewness chart above: 2025 had positive skew (the biggest single move was a gain) and extreme kurtosis (a handful of April days dominating the whole year's tail risk) at the same time. The two look contradictory, but they describe different things.

## What This Means for Portfolio Construction

None of the measures in this article is sufficient on its own. Volatility alone would have shown 2025 as a somewhat more volatile year, not that a handful of April days caused most of it. Maximum drawdown alone would have missed that the deep losses of 2020 and 2022 were completely different in shape (one a crash, the other a grind). CVaR alone would have missed that IWM's tail risk shows up in quiet years like 2024 as much as in crisis years.

Side by side, they give a more complete picture: Dow Jones (DIA) has been the most consistently resilient by drawdown across this entire period, Russell 2000 (IWM) carries the worst tail risk almost regardless of which metric you use, and emerging markets (EEM) move on their own schedule independent of what the US indices are doing. None of that changes the case for diversification; it just makes clearer what each piece of a portfolio is buying protection against.

{% include ft-charts-script.html %}
