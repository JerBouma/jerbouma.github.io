---
title: "Economics"
seo_title: "Economics Guide | Finance Toolkit"
seo_title_suffix: false
excerpt: "How to compare GDP, inflation, consumer confidence, interest rates, house prices and unemployment across countries with the Finance Toolkit's Economics module."
description: "Compare GDP, inflation, consumer confidence, interest rates, house prices and unemployment for 60+ countries in Python with the Finance Toolkit."
author_profile: false
permalink: /projects/financetoolkit/docs/getting-started/economics
classes: wide-sidebar
layout: single
redirect_from:
  - /projects/financetoolkit/economics-notebook
sidebar:
  nav: "financetoolkit-guides"
---

The Economics module puts the macro backdrop next to the company data: GDP, inflation, consumer and business confidence, interest rates, house prices, unemployment and dozens of other indicators for 60+ countries, each returned as a DataFrame with one column per country. It is the place to start when you want to know whether a slowdown is local or global, how far real rates have moved, or which housing markets ran ahead of the rest.

Every function needs no API key and follows the same pattern, so once you know one indicator you know them all. This guide uses data from 2015 onwards.

## Loading the Module

The Economics module can be imported on its own, or reached through `companies.economics` after you initialise a `Toolkit`. Here it is imported directly. To set it up with data from 2015 onwards:

```python
from financetoolkit import Economics

economics = Economics(start_date="2015-01-01")
```

Nothing is downloaded until you call a function, and each indicator is collected for every country it covers, so selecting countries afterwards is a plain column selection.

## Gross Domestic Product and Inflation

The two most fundamental macro indicators are Gross Domestic Product (GDP) and the inflation rate. With `inflation_adjusted=True` the GDP is in constant prices, so it shows real growth rather than growth flattered by inflation. Each country reports in its own currency, which makes the levels impossible to compare directly; dividing by the first year turns them into an index where 2015 is 100. To get real GDP for the four largest economies and rebase it:

```python
gdp = economics.get_gross_domestic_product(inflation_adjusted=True)

gdp_index = gdp.loc[:, ["United States", "China", "Germany", "Japan"]]
gdp_index = gdp_index / gdp_index.iloc[0] * 100
```

Which shows how differently the four economies have grown since 2015, with China's real output about 70% higher, the United States about 27% higher and Germany and Japan only 5% to 8% higher:

{% include ft-chart.html id="economics-gdp" src="/assets/data/financetoolkit-guides/economics.json" label="Real GDP of the United States, China, Germany and Japan, 2015 = 100" %}

The inflation rate is returned as a decimal fraction (0.03 is 3%), like every rate in the Finance Toolkit. To get it for four countries with very different inflation histories:

```python
inflation = economics.get_inflation_rate()

inflation.loc[:, ["United States", "United Kingdom", "Brazil", "Turkey"]]
```

Which gives the annual inflation rate per country, with Turkey's inflation in a different league from the rest at more than 50% in 2023 and 2024:

{% include ft-chart.html id="economics-inflation" src="/assets/data/financetoolkit-guides/economics.json" label="Inflation rate of the United States, United Kingdom, Brazil and Turkey" %}

## Smoothing with Rolling and Trailing Windows

Most functions in the Economics module accept `rolling` and `trailing`. `rolling=<n>` applies a simple moving average over `n` periods, which takes the noise out of a volatile series, and `trailing=<n>` sums over the last `n` periods, for example to turn a quarterly flow into a trailing annual figure. Inflation is annual by default, so a rolling window of 3 gives a three-year average. To calculate it:

```python
smoothed_inflation = economics.get_inflation_rate(rolling=3)

smoothed_inflation.loc[:, ["United States", "United Kingdom", "Brazil", "Turkey"]]
```

Which flattens the 2021-2023 spike into a broader hump, with the three-year average for the United States peaking above 5% and coming back to about 3% by 2025:

{% include ft-chart.html id="economics-inflation-rolling" src="/assets/data/financetoolkit-guides/economics.json" label="Three-year rolling average inflation rate" %}

The same parameters work next to `growth=True` and `standardize=True`, the latter converting a series into standard deviations from its own mean so that indicators on different scales can be compared.

## Consumer Confidence

Confidence indicators are survey-based and move ahead of the hard data, which makes them useful for spotting a turn in consumer spending before it shows up in retail sales or GDP. The Consumer Confidence Index (CCI) is set so that its long-term average is 100: a reading below 100 means households are more pessimistic than usual about their finances and the economy. To get the monthly index and select five countries:

```python
cci = economics.get_consumer_confidence_index()

cci.loc[:, ["United States", "South Africa", "China", "Spain", "Germany"]]
```

Which shows the sharp drops in 2020 and again in 2022, when inflation hit household budgets, and confidence in the United States still near its lowest point of the period:

{% include ft-chart.html id="economics-cci" src="/assets/data/financetoolkit-guides/economics.json" label="Consumer Confidence Index for the United States, South Africa, China, Spain and Germany" %}

The Business Confidence Index (`get_business_confidence_index`) and the Composite Leading Indicator (`get_composite_leading_indicator`) work the same way.

## Interest Rates

The long-term interest rate is the yield on 10-year government bonds, the short-term rate the 3-month interbank or treasury rate. Together they give the slope of the yield curve, and the short rate tracks the policy rate of the central bank closely. Both accept `period` to choose monthly, quarterly or annual data. To get both on a quarterly basis:

```python
countries = ["United States", "United Kingdom", "Japan", "Germany", "France", "Canada"]

long_term_interest_rates = economics.get_long_term_interest_rate(period="quarterly")
short_term_interest_rates = economics.get_short_term_interest_rate(period="quarterly")

long_term_interest_rates.loc[:, countries]
short_term_interest_rates.loc[:, countries]
```

Which shows the end of the low-rate era: short rates went from around zero (and below zero in the euro area) to more than 5% in the United States and the United Kingdom in 2023, while Japan stayed far below the rest on both measures:

{% include ft-chart.html id="economics-rates" src="/assets/data/financetoolkit-guides/economics.json" label="Long-term and short-term interest rates by country" %}

Germany and France share the euro area's short-term rate, which is why their lines overlap in the short-term tab.

## House Prices

House prices reflect both the economic situation of a country and its policies, from interest rates to building permits and tax rules. The house price index is set to 100 in 2015 for every country, so the values show the cumulative change since then. To get the index for all countries and select five of them:

```python
house_prices = economics.get_house_prices()

house_prices[["Australia", "United States", "United Kingdom", "Spain", "Brazil"]]
```

Which shows prices in the United States up more than 80% since 2015, and Spain, after a steadier climb, rising fast enough in 2024 and 2025 to draw level with it:

{% include ft-chart.html id="economics-house-prices" src="/assets/data/financetoolkit-guides/economics.json" label="House price index for Australia, the United States, the United Kingdom, Spain and Brazil" %}

The index is nominal, so high inflation shows up in it directly: Turkey's index went from 100 in 2015 to more than 2,000, which is why it is left out of the chart.

## Calling the Data Models Directly

The Economics class is a thin layer over the models that collect the data, so you can also call those models yourself. That is useful when you want the full history rather than the window set by `start_date`, as the models return everything the source has. To get the quarterly unemployment rate for all countries straight from the OECD model:

```python
from financetoolkit.economics import oecd_model

unemployment_rate = oecd_model.get_unemployment_rate(period="quarterly")

unemployment_rate.loc["1990":, ["United States", "Germany", "Japan", "Spain", "Canada"]]
```

Which shows how differently labour markets behave: Spain's unemployment peaked above 26% in 2013, the United States and Canada saw a short spike to around 13% in 2020, and Japan's never went above about 5.5%:

{% include ft-chart.html id="economics-unemployment" src="/assets/data/financetoolkit-guides/economics.json" label="Quarterly unemployment rate for the United States, Germany, Japan, Spain and Canada since 1990" %}

The series goes back to 1955 for some countries; the selection above starts in 1990 to keep the comparison readable.

<div class="fs-ref"><a href="/projects/financetoolkit/docs/economics"><i class="fas fa-book" aria-hidden="true"></i>Full reference: Economics</a></div>

{% include ft-charts-script.html %}
