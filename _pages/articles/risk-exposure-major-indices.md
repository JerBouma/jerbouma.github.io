---
title: Understanding Risk Exposure Across Major Indices
date: 2026-07-21
last_modified_at: 2026-07-26
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

In the week of March 31 to April 6, 2025, the S&P 500 ETF fell 5.85%. A weekly move like that is not unusual in itself; it happens most years. What stands out is that the rest of 2025 behaved close to normal around it. That single week is enough to push the S&P 500's kurtosis for the year to 26, roughly nine times its typical reading in a calmer year like 2023. Volatility alone would not show this, but kurtosis does.

That is a good reason to look beyond plain volatility when measuring risk. The Finance Toolkit's risk module covers Value at Risk, Conditional Value at Risk, maximum drawdown, the Ulcer Index, GARCH volatility, skewness, and kurtosis, each describing a different shape of risk that a single standard deviation number flattens into one figure. In this article I run all five across six major indices: the S&P 500 (SPY), Nasdaq 100 (QQQ), Dow Jones (DIA), Russell 2000 (IWM), MSCI EAFE developed markets (EFA), and MSCI Emerging Markets (EEM). **For more information on Finance Toolkit, have a look [here](https://github.com/JerBouma/FinanceToolkit){:target="_blank"}. To run the same analysis conversationally, explore the [Finance Toolkit MCP server](/projects/financetoolkit/mcp).**

## Setting Things Up

```bash
pip install financetoolkit
```

```python
from financetoolkit import Toolkit

indices = Toolkit(
    tickers=["SPY", "QQQ", "DIA", "IWM", "EFA", "EEM"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2019-01-01"
)
```

Get your FMP API key at [jeroenbouma.com/fmp](/fmp){:target="_blank"}. The free plan covers five years of history, enough to span the period used here.

## Value at Risk and Conditional VaR: How Bad Could a Bad Week Get?

Value at Risk (VaR) at the 95% confidence level answers one specific question: in the worst 5% of weeks, how much do you lose? Conditional Value at Risk (CVaR) answers the harder follow-up: once you are already in that worst 5%, how much do you actually lose on average? CVaR is always worse than VaR; the question is by how much.

```python
var = indices.risk.get_value_at_risk(period="yearly")
cvar = indices.risk.get_conditional_value_at_risk(period="yearly")
```

Which returns:

{% include ft-chart.html id="risk-var" src="/assets/data/article-charts.json" label="Value at Risk and Conditional Value at Risk" %}

IWM carries the worst or second-worst CVaR almost every year, including 2024 at -2.9% when most other indices were calm, which shows that small-cap stress can build even when large-cap headlines stay quiet. The gap between VaR and CVaR says more: for SPY in 2020, VaR was -3.2% but CVaR was -5.5%, meaning the average outcome inside that worst-5%-of-weeks bucket was nearly twice as bad as the threshold itself. That gap widens in every index during 2020 and 2022, the two broadest drawdown years in this dataset, and narrows again in calmer years like 2023.

> **Try this with the Finance Toolkit MCP:** *"Calculate the yearly Value at Risk and Conditional Value at Risk for SPY, QQQ, DIA, IWM, EFA, and EEM from 2019 to 2025. Which index has the worst tail risk, and in which years does the gap between VaR and CVaR widen the most?"*

## Maximum Drawdown: The Worst Case Each Index Actually Lived Through

VaR and CVaR are statistical estimates, whereas maximum drawdown is the actual peak-to-trough loss an investor in each index lived through.

```python
max_drawdown = indices.risk.get_maximum_drawdown(period="yearly")
```

Which returns:

{% include ft-chart.html id="risk-drawdown" src="/assets/data/article-charts.json" label="Maximum drawdown per year" %}

2020's COVID crash hit IWM hardest at -41.1%, deeper than any other index in any year of this dataset, consistent with small-caps having less balance sheet cushion and less liquid trading during a panic. DIA, by contrast, never has the worst drawdown of any year. Its blue-chip composition made it the most resilient of the six in 2022 (-22.0%), although in the 2020 crash only IWM fell further. In the 2022 bear market it was tech's turn: QQQ's -35.2% drawdown was the worst of that year, driven by the same rate-hike sensitivity that put growth stocks at the center of the selloff. EEM had the worst showing in 2019 and 2021, both years with no broad global crisis, which shows that emerging markets can draw down on their own schedule, independent of US conditions.

> **Try this with the Finance Toolkit MCP:** *"Show the yearly maximum drawdown for SPY, QQQ, DIA, IWM, EFA, and EEM from 2019 to 2025. Which index had the single worst drawdown, and which index was most resilient across all years?"*

## Skewness: Which Years Had Fatter Downside Than Upside

Skewness measures asymmetry. A return distribution with negative skew has a longer, fatter left tail, infrequent but severe losses outweighing the frequency of gains. Positive skew is the opposite: frequent small losses, occasional large gains.

```python
skewness = indices.risk.get_skewness(period="yearly")
```

Which returns:

{% include ft-chart.html id="risk-skew" src="/assets/data/article-charts.json" label="Skewness of weekly returns" %}

Every index ran negative in 2019 and 2020, the two years dominated by sharp, sudden selloffs (the late-2018 spillover and the COVID crash) rather than steady grinding declines. EFA and EEM show the most extreme negative skew of the whole chart in 2020, at -1.19 and -1.23, consistent with international markets taking a sharper, more concentrated hit than US large caps that year. In 2022 skew turns mildly positive almost everywhere, since that bear market ground lower week after week rather than crashing in a handful of sessions, the opposite shape of risk from 2020 despite a similarly large drawdown. 2025's positive skew across the board, led by SPY at 1.52, reflects a year of mostly steady gains punctuated by the occasional sharp upside snap-back rather than a string of small losses.

> **Try this with the Finance Toolkit MCP:** *"Calculate yearly skewness for these six indices from 2019 to 2025. Which years show the most negative skew, and what does that imply about how those losses happened?"*

## Kurtosis: Why 2025 Doesn't Look Like a Normal Year

Kurtosis measures how fat the tails are relative to a normal distribution, regardless of which direction. High kurtosis means more extreme weeks than a bell curve would predict, in either direction.

```python
kurtosis = indices.risk.get_kurtosis(period="yearly")
```

Which returns:

{% include ft-chart.html id="risk-kurtosis" src="/assets/data/article-charts.json" label="Kurtosis of weekly returns" %}

This is where the April 2025 tariff-shock week shows up most clearly. SPY's kurtosis of 26.1 in 2025 is more than double the next-highest reading anywhere else in the chart, and roughly nine times its calmest year (2023, at 2.81). QQQ and EFA show the same pattern, both above 19, while IWM's 2025 kurtosis of 8.73 is the lowest of the six, since small-caps had already been grinding through elevated volatility most of the year and one more sharp week barely moved the distribution's shape. 2020 is the only other year that comes close, when every index posted double-digit kurtosis during the COVID crash. It is worth reading this next to the skewness chart above: 2025 had positive skew (more upside than downside on average) and extreme kurtosis (one week dominating the whole year's tail risk) at the same time. The two look contradictory, but they describe different things.

> **Try this with the Finance Toolkit MCP:** *"Calculate yearly kurtosis for SPY, QQQ, DIA, IWM, EFA, and EEM from 2019 to 2025. Which year and which index show the most extreme tail risk, and what does the skewness for that same year and index suggest about the direction of that risk?"*

## What This Means for Portfolio Construction

None of the measures in this article is sufficient on its own. Volatility alone would have missed the April 2025 shock entirely, since the rest of the year was unusually calm. Maximum drawdown alone would have missed that 2020 and 2022 were the same depth of loss but completely different in shape (one a crash, the other a grind). CVaR alone would have missed that IWM's tail risk shows up in quiet years like 2024 as much as in crisis years.

Side by side, they give a more complete picture: Dow Jones (DIA) has been the most consistently resilient by drawdown across this entire period, Russell 2000 (IWM) carries the worst tail risk almost regardless of which metric you use, and emerging markets (EEM) move on their own schedule independent of what the US indices are doing. None of that changes the case for diversification; it just makes clearer what each piece of a portfolio is buying protection against.

> **Try this with the Finance Toolkit MCP:** *"Based on Value at Risk, CVaR, maximum drawdown, skewness, and kurtosis for SPY, QQQ, DIA, IWM, EFA, and EEM since 2019, which index has the most favorable risk profile overall, and which carries risk that a simple volatility number would understate?"*

<script src="/assets/js/ft-charts.js" defer></script>
