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
tags: [Finance Toolkit, Fundamental Analysis, MCP Server]
share: true
---

In the week of March 31 to April 6, 2025, the S&P 500 ETF fell 5.85%. That alone is not unusual; weekly moves like that happen most years. What is unusual is what the rest of 2025 looked like around it: a year that otherwise behaved close to normal, with one week that did not. That single week is enough to push the S&P 500's kurtosis for the year to 26, roughly six times its typical reading in a calmer year like 2023. Volatility alone would not tell you that. Kurtosis does.

That is the case for looking past plain volatility when measuring risk. The Finance Toolkit's risk module covers Value at Risk, Conditional Value at Risk, maximum drawdown, the Ulcer Index, GARCH volatility, skewness, and kurtosis, each describing a different shape of risk that a single standard deviation number flattens into one figure. This article runs all five across six major indices: the S&P 500 (SPY), Nasdaq 100 (QQQ), Dow Jones (DIA), Russell 2000 (IWM), MSCI EAFE developed markets (EFA), and MSCI Emerging Markets (EEM). **For more information on Finance Toolkit, have a look [here](https://github.com/JerBouma/FinanceToolkit){:target="_blank"}. To run the same analysis conversationally, explore the [Finance Toolkit MCP server](/projects/financetoolkit/mcp).**

## Setting Things Up

```bash
pip install financetoolkit
```

```python
from financetoolkit import Toolkit

indices = Toolkit(
    tickers=["SPY", "QQQ", "DIA", "IWM", "EFA", "EEM"],
    api_key="YOUR_FMP_API_KEY",
    start_date="2019-01-01"
)
```

Get your FMP API key at [jeroenbouma.com/fmp](/fmp){:target="_blank"}. The free plan covers five years of history, enough to span the period used here.

## Value at Risk and Conditional VaR: How Bad Could a Bad Week Get?

Value at Risk (VaR) at the 95% confidence level answers one specific question: in the worst 5% of weeks, how much do you lose? Conditional Value at Risk (CVaR) answers the harder follow-up: once you are already in that worst 5%, how much do you actually lose on average? CVaR is always worse than VaR, the question is by how much.

```python
var = indices.risk.get_value_at_risk(period="yearly")
cvar = indices.risk.get_conditional_value_at_risk(period="yearly")
```

Which returns (Value at Risk):

| Year | SPY | QQQ | DIA | IWM | EFA | EEM |
|------|----:|----:|----:|----:|----:|----:|
| 2019 | -1.2% | -1.6% | -1.2% | -1.5% | -1.1% | -1.5% |
| 2020 | -3.2% | -3.5% | -3.2% | -3.5% | -2.6% | -2.6% |
| 2021 | -1.3% | -2.0% | -1.4% | -2.3% | -1.4% | -2.0% |
| 2022 | -2.6% | -3.5% | -2.0% | -2.8% | -2.3% | -2.3% |
| 2023 | -1.4% | -1.7% | -1.1% | -1.7% | -1.4% | -1.5% |
| 2024 | -1.3% | -1.9% | -1.1% | -1.9% | -1.5% | -1.7% |
| 2025 | -1.7% | -2.1% | -1.6% | -2.0% | -1.3% | -1.6% |

And Conditional Value at Risk:

| Year | SPY | QQQ | DIA | IWM | EFA | EEM |
|------|----:|----:|----:|----:|----:|----:|
| 2019 | -2.0% | -2.4% | -2.0% | -2.4% | -1.8% | -2.2% |
| 2020 | -5.5% | -5.5% | -6.0% | -6.6% | -5.3% | -5.7% |
| 2021 | -1.9% | -2.7% | -1.8% | -2.9% | -2.0% | -2.6% |
| 2022 | -3.4% | -4.3% | -2.8% | -3.6% | -3.0% | -3.0% |
| 2023 | -1.6% | -2.0% | -1.4% | -2.4% | -1.9% | -2.1% |
| 2024 | -1.9% | -2.7% | -1.5% | -2.9% | -1.9% | -2.2% |
| 2025 | -2.8% | -3.4% | -2.4% | -3.1% | -2.0% | -2.5% |

IWM carries the worst or second-worst CVaR almost every year, including 2024 at -2.9% when most other indices were calm, a reminder that small-cap stress can build even when large-cap headlines stay quiet. The gap between VaR and CVaR is the more interesting read: for SPY in 2020, VaR was -3.2% but CVaR was -5.5%, meaning the average outcome inside that worst-5%-of-weeks bucket was nearly twice as bad as the threshold itself. That gap widens in every index during 2020 and 2022, the two broadest drawdown years in this dataset, and narrows again in calmer years like 2023.

> **Try this with the Finance Toolkit MCP:** *"Calculate the yearly Value at Risk and Conditional Value at Risk for SPY, QQQ, DIA, IWM, EFA, and EEM from 2019 to 2025. Which index has the worst tail risk, and in which years does the gap between VaR and CVaR widen the most?"*

## Maximum Drawdown: The Worst Case Each Index Actually Lived Through

VaR and CVaR are statistical estimates. Maximum drawdown is not an estimate, it is the actual peak-to-trough loss an investor in each index lived through.

```python
max_drawdown = indices.risk.get_maximum_drawdown(period="yearly")
```

Which returns:

| Year | SPY | QQQ | DIA | IWM | EFA | EEM |
|------|----:|----:|----:|----:|----:|----:|
| 2019 | -6.6% | -11.0% | -6.9% | -9.9% | -8.5% | -13.1% |
| 2020 | -34.1% | -28.6% | -37.1% | -41.1% | -34.0% | -33.9% |
| 2021 | -5.4% | -10.9% | -6.6% | -12.5% | -7.0% | -18.2% |
| 2022 | -25.4% | -35.2% | -22.0% | -27.3% | -30.3% | -33.3% |
| 2023 | -10.3% | -10.9% | -9.0% | -18.3% | -11.6% | -14.1% |
| 2024 | -8.4% | -13.5% | -6.1% | -10.1% | -11.1% | -11.7% |
| 2025 | -19.0% | -22.9% | -16.1% | -23.9% | -14.1% | -15.0% |

2020's COVID crash hit IWM hardest at -41.1%, deeper than any other index in any year of this dataset, consistent with small-caps having less balance sheet cushion and less liquid trading during a panic. DIA, by contrast, never has the worst drawdown of any year, its blue-chip composition acting as the most resilient of the six across both 2020 and 2022. The 2022 bear market flips the script on tech: QQQ's -35.2% drawdown was the worst of that year, driven by the same rate-hike sensitivity that made growth stocks the epicenter of the selloff. EEM had the worst showing in 2019 and 2021, both years with no broad global crisis, a reminder that emerging markets can drawdown on their own schedule independent of US conditions.

> **Try this with the Finance Toolkit MCP:** *"Show the yearly maximum drawdown for SPY, QQQ, DIA, IWM, EFA, and EEM from 2019 to 2025. Which index had the single worst drawdown, and which index was most resilient across all years?"*

## Skewness: Which Years Had Fatter Downside Than Upside

Skewness measures asymmetry. A return distribution with negative skew has a longer, fatter left tail, infrequent but severe losses outweighing the frequency of gains. Positive skew is the opposite: frequent small losses, occasional large gains.

```python
skewness = indices.risk.get_skewness(period="yearly")
```

Which returns:

| Year | SPY | QQQ | DIA | IWM | EFA | EEM |
|------|----:|----:|----:|----:|----:|----:|
| 2019 | -0.59 | -0.43 | -0.65 | -0.36 | -0.56 | -0.53 |
| 2020 | -0.61 | -0.61 | -0.52 | -0.98 | -1.19 | -1.23 |
| 2021 | -0.34 | -0.27 | -0.37 | -0.03 | -0.56 | -0.20 |
| 2022 | 0.05 | 0.10 | -0.04 | 0.09 | 0.37 | 0.72 |
| 2023 | -0.04 | 0.10 | -0.03 | 0.33 | -0.21 | -0.03 |
| 2024 | -0.52 | -0.41 | 0.04 | 0.05 | -0.43 | 0.06 |
| 2025 | 1.52 | 1.31 | 0.79 | 0.33 | 0.39 | 0.20 |

Every index ran negative in 2019 and 2020, the two years dominated by sharp, sudden selloffs (the late-2018 spillover and the COVID crash) rather than steady grinding declines. EFA and EEM show the most extreme negative skew of the whole table in 2020, at -1.19 and -1.23, consistent with international markets taking a sharper, more concentrated hit than US large caps that year. 2022 flips to mildly positive skew almost everywhere, since that bear market ground lower week after week rather than crashing in a handful of sessions, the opposite shape of risk from 2020 despite a similarly large drawdown. 2025's positive skew across the board, led by SPY at 1.52, reflects a year of mostly steady gains punctuated by the occasional sharp upside snap-back rather than a string of small losses.

> **Try this with the Finance Toolkit MCP:** *"Calculate yearly skewness for these six indices from 2019 to 2025. Which years show the most negative skew, and what does that imply about how those losses happened?"*

## Kurtosis: Why 2025 Doesn't Look Like a Normal Year

Kurtosis measures how fat the tails are relative to a normal distribution, regardless of which direction. High kurtosis means more extreme weeks than a bell curve would predict, in either direction.

```python
kurtosis = indices.risk.get_kurtosis(period="yearly")
```

Which returns:

| Year | SPY | QQQ | DIA | IWM | EFA | EEM |
|------|----:|----:|----:|----:|----:|----:|
| 2019 | 6.05 | 5.35 | 6.26 | 4.49 | 5.59 | 4.48 |
| 2020 | 10.06 | 8.68 | 11.29 | 8.53 | 11.60 | 11.00 |
| 2021 | 3.59 | 3.86 | 3.69 | 2.99 | 3.58 | 3.43 |
| 2022 | 3.32 | 3.14 | 3.38 | 2.96 | 4.09 | 6.00 |
| 2023 | 2.81 | 2.86 | 3.19 | 3.80 | 3.55 | 3.37 |
| 2024 | 4.70 | 3.90 | 5.71 | 4.77 | 3.61 | 4.20 |
| 2025 | 26.14 | 20.50 | 17.56 | 8.73 | 19.13 | 11.16 |

This is where the April 2025 tariff-shock week shows up most clearly. SPY's kurtosis of 26.1 in 2025 is more than double the next-highest reading anywhere else in the table, and roughly nine times its calmest year (2023, at 2.81). QQQ and EFA show the same pattern, both above 19, while IWM's 2025 kurtosis of 8.73 is the lowest of the six, since small-caps had already been grinding through elevated volatility most of the year and one more sharp week barely moved the distribution's shape. 2020 is the only other year that comes close, when every index posted double-digit kurtosis during the COVID crash. The lesson sits side by side with the skewness table above: 2025 had positive skew (more upside than downside on average) and extreme kurtosis (one week dominating the whole year's tail risk) at the same time, two measurements that look contradictory until you remember they describe different things.

> **Try this with the Finance Toolkit MCP:** *"Calculate yearly kurtosis for SPY, QQQ, DIA, IWM, EFA, and EEM from 2019 to 2025. Which year and which index show the most extreme tail risk, and what does the skewness for that same year and index suggest about the direction of that risk?"*

## What This Means for Portfolio Construction

No single number in this article tells the full story on its own. Volatility alone would have missed the April 2025 shock entirely, since the rest of the year was unusually calm. Maximum drawdown alone would have missed that 2020 and 2022 were the same depth of loss but completely different in shape, one a crash, one a grind. CVaR alone would have missed that IWM's tail risk shows up in quiet years like 2024 as much as in crisis years.

Putting them side by side gives a more honest picture: Dow Jones (DIA) has been the most consistently resilient by drawdown across this entire period, Russell 2000 (IWM) carries the worst tail risk almost regardless of which metric you use, and emerging markets (EEM) move on their own schedule independent of what the US indices are doing. None of that changes the diversification argument, it just specifies what each piece of a portfolio is actually buying protection against.

> **Try this with the Finance Toolkit MCP:** *"Based on Value at Risk, CVaR, maximum drawdown, skewness, and kurtosis for SPY, QQQ, DIA, IWM, EFA, and EEM since 2019, which index has the most favorable risk profile overall, and which carries risk that a simple volatility number would understate?"*
