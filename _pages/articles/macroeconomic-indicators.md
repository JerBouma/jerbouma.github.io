---
title: Tracking Macroeconomic Indicators with the Finance Toolkit
date: 2026-07-14
permalink: /articles/macroeconomic-indicators-finance-toolkit
excerpt: "Compare inflation, central bank policy rates, unemployment, and government debt across five major economies using the Finance Toolkit's Economics module, no API key required."
description: "Track macroeconomic indicators including inflation rate, central bank policy rate, unemployment rate, and government debt-to-GDP across the United States, United Kingdom, Germany, Japan, and Brazil with the Finance Toolkit."
layout: single
classes: wide-sidebar article-document
author_profile: false
collection: article
tags: [Finance Toolkit, Fundamental Analysis, MCP Server]
share: true
---

In 2022, Brazil's central bank had its policy rate at 13.75%. The Bank of Japan's was at -0.1%. Both countries were responding to the same global shock, a wave of post-pandemic inflation that touched nearly every economy on earth, and they responded in almost opposite ways. One was years into an aggressive tightening cycle. The other had not raised rates above zero in over a decade.

That divergence is the most interesting thing macro data shows you: not that economies move together, but how differently they move through the same event. The Finance Toolkit's Economics module pulls unemployment, GDP growth, inflation, government debt, central bank rates, and bond yields for 60+ countries going back, in some series, over a century, sourced from the OECD and the Global Macro Database. Unlike the rest of the Toolkit, none of this requires an FMP API key. It is public macro data, free to query.

This article tracks five economies, the United States, United Kingdom, Germany, Japan, and Brazil, through the 2021-2023 inflation shock and the years since. **For more information on Finance Toolkit, have a look [here](https://github.com/JerBouma/FinanceToolkit){:target="_blank"}. To explore the Finance Toolkit MCP, see [here](https://www.jeroenbouma.com/projects/financetoolkit/mcp).**

## Setting Things Up

The Economics module works standalone, no ticker, no API key:

```bash
pip install financetoolkit
```

```python
from financetoolkit import Economics

economics = Economics(start_date="2019-01-01")
```

Every method below takes a `countries` argument. The full list of supported countries and indicators is in the [documentation](https://www.jeroenbouma.com/projects/financetoolkit/docs); this article sticks to five economies chosen for contrast rather than completeness.

## Inflation: One Shock, Different Timing

The global inflation spike gets talked about as a single event, but the data shows it arrived in waves, not all at once.

```python
inflation = economics.get_inflation_rate(
    countries=["United States", "United Kingdom", "Germany", "Japan", "Brazil"]
)
```

Which returns:

| Year | Germany | United Kingdom | Japan | Brazil | United States |
|------|--------:|----------------:|------:|-------:|---------------:|
| 2019 | 1.3% | 1.8% | 0.5% | 3.7% | 1.8% |
| 2020 | 0.5% | 1.0% | 0.0% | 3.2% | 1.2% |
| 2021 | 3.1% | 2.5% | -0.2% | 8.3% | 4.7% |
| 2022 | 6.9% | 7.9% | 2.5% | 9.3% | 8.0% |
| 2023 | 5.9% | 6.8% | 3.3% | 4.6% | 4.1% |
| 2024 | 2.4% | 2.6% | 2.2% | 4.3% | 3.0% |
| 2025 | 2.0% | 2.1% | 2.0% | 3.6% | 1.9% |

Brazil's inflation took off a full year before the others, hitting 8.3% in 2021 while the US was still at 4.7% and Japan was in mild deflation at -0.2%. By 2022 the developed economies caught up, Germany at 6.9%, the UK at 7.9%, the US at 8.0%, but Brazil had already peaked and was on its way back down to 4.6% by 2023. Japan never had a real inflation problem by international standards; its highest reading in this entire window is 3.3%, a number that would have counted as a good year almost anywhere else.

> **Try this with the Finance Toolkit MCP:** *"Compare the inflation rate for the United States, United Kingdom, Germany, Japan, and Brazil from 2019 to 2025. Which country's inflation peaked first?"*

## Central Banks Respond, But Not on the Same Clock

Inflation timing explains a lot of what comes next, because central banks move in response to their own country's data, not anyone else's.

```python
policy_rate = economics.get_central_bank_policy_rate(
    countries=["United States", "United Kingdom", "Germany", "Japan", "Brazil"]
)
```

Which returns:

| Year | Germany | United Kingdom | Japan | Brazil | United States |
|------|--------:|----------------:|------:|-------:|---------------:|
| 2019 | -0.45% | 0.75% | -0.10% | 4.50% | 1.625% |
| 2020 | -0.50% | 0.10% | -0.10% | 2.00% | 0.125% |
| 2021 | -0.50% | 0.25% | -0.10% | 9.25% | 0.125% |
| 2022 | 0.44% | 3.50% | -0.10% | 13.75% | 4.375% |
| 2023 | 3.63% | 5.25% | -0.10% | 11.75% | 5.375% |
| 2024 | 3.81% | 4.75% | 0.25% | 12.25% | 4.375% |
| 2025 | 2.88% | 4.13% | 0.50% | 8.31% | 4.255% |

Brazil started hiking in 2021, a full year ahead of the Federal Reserve and the Bank of England, and took its policy rate from 2.0% to 13.75% in eighteen months, the steepest tightening cycle of the five. By the time the Fed and the Bank of England started moving in 2022, Brazil was already near its peak. The European Central Bank (the rate driving Germany's number here) lagged furthest behind, staying negative until mid-2022 and not clearing 3% until 2023.

Japan is the outlier that matters most. The Bank of Japan held its policy rate at -0.10% through the entire inflation shock, only inching to 0.25% in 2024 and 0.50% in 2025. After more than a decade of fighting deflation, the BOJ treated even a 3% inflation print as something to look through rather than react to, a complete reversal of how every other central bank in this table behaved.

> **Try this with the Finance Toolkit MCP:** *"Show the central bank policy rate for the same five countries from 2019 to 2025. Which country hiked first, which hiked the most, and which barely moved at all?"*

## The Labor Market Question: Did Higher Rates Cost Jobs?

The textbook expectation is that aggressive rate hikes cool the labor market. The data only partly agrees.

```python
unemployment = economics.get_unemployment_rate(
    countries=["United States", "United Kingdom", "Germany", "Japan", "Brazil"]
)
```

Which returns:

| Year | Germany | United Kingdom | Japan | Brazil | United States |
|------|--------:|----------------:|------:|-------:|---------------:|
| 2019 | 3.0% | 3.9% | 2.4% | 12.0% | 3.7% |
| 2020 | 3.6% | 4.7% | 2.8% | 13.8% | 8.1% |
| 2021 | 3.6% | 4.6% | 2.8% | 13.2% | 5.4% |
| 2022 | 3.1% | 3.9% | 2.6% | 9.3% | 3.6% |
| 2023 | 3.0% | 4.0% | 2.6% | 8.0% | 3.6% |
| 2024 | 3.4% | 4.3% | 2.5% | 7.2% | 4.1% |
| 2025 | 3.2% | 4.1% | 2.5% | 7.2% | 4.4% |

The US is the clearest case of a pandemic-driven spike rather than a rate-driven one: unemployment jumped to 8.1% in 2020 from lockdowns, then fell back to 3.6% by 2022, the same year the Fed started its steepest hikes since the 1980s. Unemployment barely moved after that. That is the soft landing debate in one row of a table: rates rose nearly five points and the labor market shrugged.

Brazil tells the opposite story in the most striking way. Despite running the highest policy rate of any country here for three straight years, Brazilian unemployment fell every single year from 2020 onward, from 13.8% to 7.2% by 2025. High rates did not stop the labor market from healing; whatever was driving Brazilian employment had little to do with the cost of borrowing at the margin. Germany and Japan, the two economies with the smallest rate moves, also show the smallest unemployment swings, which is closer to what theory predicts.

> **Try this with the Finance Toolkit MCP:** *"Pull the unemployment rate for these five countries from 2019 to 2025. Did unemployment rise when central banks raised rates, and which country shows the clearest soft landing?"*

## Government Debt: Who Paid Down the COVID Bill?

Inflation and rate hikes affect more than households and businesses, they change the math on government debt, both the cost of servicing it and the rate at which it gets inflated away.

```python
debt_to_gdp = economics.get_government_debt_to_gdp_ratio(
    countries=["United States", "United Kingdom", "Germany", "Japan", "Brazil"]
)
```

Which returns:

| Year | Germany | United Kingdom | Japan | Brazil | United States |
|------|--------:|----------------:|------:|-------:|---------------:|
| 2019 | 58.6% | 85.7% | 236.4% | 87.1% | 108.0% |
| 2020 | 67.9% | 105.8% | 258.4% | 96.0% | 131.8% |
| 2021 | 67.9% | 105.1% | 253.7% | 88.9% | 124.5% |
| 2022 | 64.8% | 99.6% | 256.3% | 83.9% | 118.6% |
| 2023 | 62.7% | 100.0% | 249.7% | 84.7% | 118.7% |
| 2024 | 62.7% | 101.8% | 251.2% | 87.6% | 121.0% |
| 2025 | 62.1% | 103.8% | 248.7% | 92.0% | 124.1% |

Japan's debt-to-GDP ratio of roughly 249% dwarfs every other country here, more than double the United States and nearly two and a half times the United Kingdom. It has stayed in a tight band for years, which is itself notable: a decade of near-zero rates means rolling over that debt costs almost nothing, a luxury the BOJ's reluctance to hike helps preserve.

The US and UK both jumped sharply in 2020 from COVID stimulus, 108% to 132% for the US and 86% to 106% for the UK, and neither has come close to working that back down; both sit higher in 2025 than they did in 2022. Germany and Brazil show the opposite pattern: both peaked in 2020-2021 and have since declined, Germany from 67.9% to 62.1%, Brazil from 96.0% to a low of 83.9% in 2022 before drifting back up to 92.0%. Brazil's case is partly mechanical. The same high inflation that pushed its central bank to 13.75% also inflated away a chunk of the real value of its debt, the kind of side effect that does not show up if you only look at the policy rate in isolation.

> **Try this with the Finance Toolkit MCP:** *"Compare government debt-to-GDP for these five countries from 2019 to 2025. Which countries reduced their debt burden after the COVID spike, and which kept climbing?"*

## What This Means for the Next Cycle

Pulling these four indicators side by side for the same five countries makes a point that looking at any one of them alone would miss: there is no single global business cycle, only a global shock that each economy absorbed and is unwinding on its own schedule, shaped by its starting debt level, its central bank's tolerance for inflation, and the structure of its labor market.

Brazil moved first and is furthest along in normalizing, having hiked early, peaked early, and started easing while the US and UK were still raising. Japan is the mirror image, having barely participated in the global tightening cycle and only now taking its first tentative steps away from negative rates after more than a decade. The US delivered the cleanest soft landing in the group: a sharp hiking cycle with almost no labor market damage, though its debt-to-GDP ratio shows the COVID stimulus bill has not gone away. Germany is the closest thing to textbook here, moderate inflation, moderate hikes, and the only economy in the group steadily reducing its debt burden.

What to watch next: whether Japan's exit from negative rates accelerates as inflation proves more persistent than the BOJ expects, whether US and UK debt-to-GDP keeps climbing without consequence, and whether Brazil's early-mover advantage on rate cuts gives it room to support growth while the others are still catching up.

> **Try this with the Finance Toolkit MCP:** *"Based on inflation, policy rates, unemployment, and debt-to-GDP for the United States, United Kingdom, Germany, Japan, and Brazil since 2019, which country is furthest along in normalizing after the pandemic shock, and which is most exposed if rates stay higher for longer?"*
