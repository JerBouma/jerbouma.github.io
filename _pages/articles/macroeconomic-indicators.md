---
title: Tracking Macroeconomic Indicators with the Finance Toolkit
seo_title: "Tracking Macroeconomic Indicators in Python"
date: 2026-07-14
last_modified_at: 2026-11-17
permalink: /articles/macroeconomic-indicators-finance-toolkit
excerpt: "Compare inflation, central bank policy rates, unemployment, and government debt across five major economies using the Finance Toolkit's Economics module, no API key required."
description: "Track inflation, policy rates, unemployment and debt-to-GDP across the US, UK, Germany, Japan and Brazil with the Finance Toolkit's Economics module."
layout: single
classes: wide-sidebar article-document
author_profile: false
collection: article
tags: [Macroeconomics]
share: true
---

In 2022, Brazil's central bank had its policy rate at 13.75% while the Bank of Japan's was at -0.1%. Both countries were facing the same global shock, a wave of post-pandemic inflation that touched nearly every economy, and they responded in almost opposite ways: Brazil was years into an aggressive tightening cycle, whereas Japan had not raised rates above zero in over a decade.

To me, that is the most interesting part of macro data: how differently economies move through the same event. The Finance Toolkit's Economics module pulls unemployment, GDP growth, inflation, government debt, central bank rates, and bond yields for 60+ countries going back, in some series, over a century, sourced from the OECD and the Global Macro Database. Unlike the rest of the Toolkit, none of this requires an FMP API key. It is public macro data and free to query.

In this article I track five economies (the United States, United Kingdom, Germany, Japan, and Brazil) from 2019 through the 2021-2023 inflation shock and the years since, with yearly figures for each. The data comes from the [Finance Toolkit](https://github.com/JerBouma/FinanceToolkit){:target="_blank"}. Every chart has a Python button with the code behind it and an MCP button with a question that gets the same data from the [Finance Toolkit MCP server](/projects/financetoolkit/mcp). The full list of supported countries and indicators is in the [documentation](/projects/financetoolkit/docs); this article sticks to five economies chosen for contrast rather than completeness.

## Inflation: One Shock, Different Timing

The global inflation spike gets talked about as a single event, but the data shows it arrived in waves.

The yearly inflation rate of the five economies from 2019 to 2025:

{% capture code_inflation %}
```python
# pip install financetoolkit
from financetoolkit import Economics

economics = Economics(start_date="2019-01-01", end_date="2025-12-31")

inflation = economics.get_inflation_rate(countries=["United States", "United Kingdom", "Germany", "Japan", "Brazil"], period="yearly")
```
{% endcapture %}
{% include ft-chart.html id="macro-inflation" src="/assets/data/article-charts.json" label="Inflation by country" code=code_inflation mcp="What was the yearly inflation rate of the United States, United Kingdom, Germany, Japan and Brazil from 2019 to 2025, and which country's inflation peaked first?" %}

Brazil's inflation took off a full year before the others, hitting 8.3% in 2021 while the US was still at 4.7% and Japan was in mild deflation at -0.2%. By 2022 the developed economies had caught up (Germany at 6.9%, the UK at 7.9%, the US at 8.0%), but Brazil had already peaked and was on its way back down to 4.6% by 2023. Japan never had a real inflation problem by international standards; its highest reading in this entire window is 3.3%, a number that would have counted as a good year almost anywhere else.

## Central Banks Respond, But Not on the Same Clock

Inflation timing explains a lot of what comes next, because central banks move in response to their own country's data rather than anyone else's.

The central bank policy rate of each economy from 2019 to 2025:

{% capture code_rates %}
```python
# pip install financetoolkit
from financetoolkit import Economics

economics = Economics(start_date="2019-01-01", end_date="2025-12-31")

policy_rate = economics.get_central_bank_policy_rate(countries=["United States", "United Kingdom", "Germany", "Japan", "Brazil"], period="yearly")
```
{% endcapture %}
{% include ft-chart.html id="macro-rates" src="/assets/data/article-charts.json" label="Central bank policy rates" code=code_rates mcp="Show the yearly central bank policy rate for the United States, United Kingdom, Germany, Japan and Brazil from 2019 to 2025. Which country hiked first, which hiked the most, and which barely moved?" %}

Brazil started hiking in 2021, a full year ahead of the Federal Reserve and the Bank of England, and took its policy rate from 2.0% to 13.75% in eighteen months, the steepest tightening cycle of the five. By the time the Fed and the Bank of England started moving in 2022, Brazil was already near its peak. The European Central Bank (the rate driving Germany's number here) lagged furthest behind, staying negative until mid-2022 and not clearing 3% until 2023.

Japan is the biggest outlier. The Bank of Japan held its policy rate at -0.10% through the entire inflation shock, only inching to 0.25% in 2024 and 0.50% in 2025. After more than a decade of fighting deflation, the BOJ treated even a 3% inflation print as something to look through rather than react to, the opposite of how every other central bank in this table behaved.

## The Labor Market Question: Did Higher Rates Cost Jobs?

The textbook expectation is that aggressive rate hikes cool the labor market, but the data only partly supports that.

The yearly unemployment rate of the five economies from 2019 to 2025:

{% capture code_unemployment %}
```python
# pip install financetoolkit
from financetoolkit import Economics

economics = Economics(start_date="2019-01-01", end_date="2025-12-31")

unemployment = economics.get_unemployment_rate(countries=["United States", "United Kingdom", "Germany", "Japan", "Brazil"], period="yearly")
```
{% endcapture %}
{% include ft-chart.html id="macro-unemployment" src="/assets/data/article-charts.json" label="Unemployment rates" code=code_unemployment mcp="What was the yearly unemployment rate of the United States, United Kingdom, Germany, Japan and Brazil from 2019 to 2025, and did it rise when central banks raised rates?" %}

The US is the clearest case of a pandemic-driven spike rather than a rate-driven one: unemployment jumped to 8.1% in 2020 from lockdowns, then fell back to 3.6% by 2022, the same year the Fed started its steepest hikes since the 1980s. Unemployment barely moved after that, which sums up the soft landing debate in a single line of the chart: rates rose nearly five points and the labor market hardly reacted.

Brazil shows the opposite. Despite running the highest policy rate of any country here for three straight years, Brazilian unemployment fell every year from 2020 onward, from 13.8% to 7.2% by 2025. High rates did not stop the labor market from healing; whatever was driving Brazilian employment had little to do with the cost of borrowing at the margin. Germany and Japan, the two economies with the smallest rate moves, also show the smallest unemployment swings, which is closer to what theory predicts.

## Government Debt: Who Paid Down the COVID Bill?

Inflation and rate hikes affect more than households and businesses. They also change the math on government debt: both the cost of servicing it and the rate at which it gets inflated away.

Government debt as a share of GDP for the five economies from 2019 to 2025:

{% capture code_debt %}
```python
# pip install financetoolkit
from financetoolkit import Economics

economics = Economics(start_date="2019-01-01", end_date="2025-12-31")

debt_to_gdp = economics.get_government_debt_to_gdp_ratio(countries=["United States", "United Kingdom", "Germany", "Japan", "Brazil"])
```
{% endcapture %}
{% include ft-chart.html id="macro-debt" src="/assets/data/article-charts.json" label="Government debt to GDP" code=code_debt mcp="Compare government debt to GDP for the United States, United Kingdom, Germany, Japan and Brazil from 2019 to 2025. Which countries reduced their debt burden after the 2020 spike, and which kept climbing?" %}

Japan's debt-to-GDP ratio of roughly 249% is far above every other country here, more than double the United States and nearly two and a half times the United Kingdom. It has stayed in a tight band for years, which is itself notable: a decade of near-zero rates means rolling over that debt costs almost nothing, a luxury the BOJ's reluctance to hike helps preserve.

The US and UK both jumped sharply in 2020 from COVID stimulus, 108% to 132% for the US and 86% to 106% for the UK, and neither has come close to working that back down; both sit higher in 2025 than they did in 2022. Germany and Brazil show the opposite pattern: both peaked in 2020-2021 and have since declined, Germany from 67.9% to 62.1%, Brazil from 96.0% to a low of 83.9% in 2022 before drifting back up to 92.0%. Brazil's case is partly mechanical. The same high inflation that pushed its central bank to 13.75% also inflated away a chunk of the real value of its debt, the kind of side effect that does not show up if you only look at the policy rate in isolation.

## What This Means for the Next Cycle

Looking at these four indicators side by side for the same five countries shows something that any one of them alone would miss. Rather than following a single global business cycle, each economy absorbed the same global shock and is unwinding it on its own schedule, shaped by its starting debt level, its central bank's tolerance for inflation, and the structure of its labor market.

Brazil moved first and is furthest along in normalizing, having hiked early, peaked early, and started easing while the US and UK were still raising. Japan is the mirror image, having barely participated in the global tightening cycle and only now taking its first tentative steps away from negative rates after more than a decade. The US delivered the cleanest soft landing in the group: a sharp hiking cycle with almost no labor market damage, though its debt-to-GDP ratio shows the COVID stimulus bill has not gone away. Germany comes closest to the textbook: moderate inflation, moderate hikes, and the only economy in the group steadily reducing its debt burden.

Going forward, I would watch whether Japan's exit from negative rates accelerates as inflation proves more persistent than the BOJ expects, whether US and UK debt-to-GDP keeps climbing without consequence, and whether Brazil's early-mover advantage on rate cuts gives it room to support growth while the others are still catching up.

{% include ft-charts-script.html %}
