---
title: "The Black Death's Economic Effects on English Wages"
seo_title: "The Black Death's Economic Effects on Wages"
date: 2026-11-17
last_modified_at: 2026-11-17
permalink: /articles/black-death-economic-effects
excerpt: "England lost 46% of its population between 1348 and 1351. Real wages roughly doubled over the next century, then fell back as the population recovered."
description: "The economic effects of the Black Death in England: population fell 46% in three years and real wages doubled, shown with the Bank of England's data since 1086."
layout: single
classes: wide-sidebar article-document
author_profile: false
collection: article
tags: [Macroeconomics]
share: true
---

In 1348, England had about 4.81 million people. Three years later, after the Black Death had passed through, it had 2.60 million. That is a fall of 46%, the largest three-year drop in population in the Bank of England's record of the English and British economy, which starts in 1086. Over the next century, the real wage of an ordinary worker roughly doubled.

The economic effects of the Black Death are one of the clearest natural experiments in economic history. Labour suddenly became scarce while the land, the buildings and the tools were all still there. What happens to wages, prices and output when nearly half of the workforce disappears? And how long does it last? This is the first article in a weekly series on events from economic history, and in it I follow England from the decades before the plague to the 1600s, when the population had come back. The data is the Bank of England's "[A millennium of macroeconomic data](https://www.bankofengland.co.uk/statistics/research-datasets){:target="_blank"}" (version 3.1), around eighty annual series on the English and UK economy. **All data comes from the [Finance Toolkit](https://github.com/JerBouma/FinanceToolkit){:target="_blank"}, and the same questions can be asked in plain English through the [Finance Toolkit MCP server](/projects/financetoolkit/mcp).**

## Almost Half of England Gone in Three Years

The population of England from 1300 to 1500, in millions:

{% include ft-chart.html id="bd-population" src="/assets/data/article-charts.json" label="Population of England, 1300 to 1500" %}

<details class="chart-code" markdown="block">
<summary><i class="fas fa-code" aria-hidden="true"></i> <span class="chart-code__show">Show the code</span><span class="chart-code__hide">Hide the code</span></summary>

```python
# pip install financetoolkit
from financetoolkit import Economics

economics = Economics(start_date="1086-01-01")

population = economics.get_millennium_of_macroeconomic_data(series="Population (England)")
population = population.loc["1300":"1500"] / 1000  # in millions
```

</details>

The population was already under pressure before the plague. The Great Famine of 1315 to 1317 is visible as a decline from 4.69 million in 1315 to 4.12 million in 1325, after which it grew again to 4.81 million in 1348, the highest level in the record until then. Then it collapsed to 2.60 million by 1351.

A note of caution is due here. Nobody counted the people of England in 1348, so these figures are reconstructions by economic historians from manor records, tax returns, prices and wages. The population is estimated for benchmark years and filled in between them, which is why it falls by the same 18.5% in each of the years 1349, 1350 and 1351. The level of a single year is uncertain. The size and direction of the change over a decade is far more reliable, so that is what this article looks at, mostly as averages over a period.

**The plague was followed by a long decline: by 1450, England had 1.90 million people, 60% fewer than in 1348.** Further outbreaks of plague returned every decade or two, and the population did not grow back to its 1348 level until 1622, almost three centuries later. For an economist, that makes it a lasting change in the amount of labour compared to the amount of land.

## Real Wages Roughly Doubled

The real consumption wage is the nominal wage divided by the price of a basket of the things workers bought, mostly food, fuel and clothing. It says how much a day's work could buy. From 1300 to 1550 it moved as follows:

{% include ft-chart.html id="bd-wages" src="/assets/data/article-charts.json" label="Real consumption wages in England, 1300 to 1550" %}

<details class="chart-code" markdown="block">
<summary><i class="fas fa-code" aria-hidden="true"></i> <span class="chart-code__show">Show the code</span><span class="chart-code__hide">Hide the code</span></summary>

```python
# pip install financetoolkit
from financetoolkit import Economics

economics = Economics(start_date="1086-01-01")

wages = economics.get_millennium_of_macroeconomic_data(series="Real consumption wages")
wages = wages.loc["1300":"1550"]
```

</details>

Wages jumped from one year to the next with the harvest, by around 11% on average in the decades before 1348, so single years say little. Taking the average of 1340 to 1347 as the starting point (100), the real wage was 136 in the 1350s, 162 between 1360 and 1399 and 193 in the first half of the 15th century. Between 1450 and 1499 it averaged 201, double the level before the plague, and it peaked in 1464.

**The workers who survived could buy roughly twice as much with a day's work as their parents could.** Next to that, the rise took decades, and there was a reason for that. In 1349 the Crown issued the Ordinance of Labourers, followed by the Statute of Labourers in 1351, which tried to hold wages at their pre-plague levels and made it an offence to ask for more.

## Pay Rose While Prices Did Not

A higher real wage can come from higher pay or from lower prices. To see which, I put nominal earnings per head and the consumer price index side by side, both as an index with the average of 1340 to 1347 at 100:

{% include ft-chart.html id="bd-pay-prices" src="/assets/data/article-charts.json" label="Earnings per head and consumer prices in England, 1330 to 1450" %}

<details class="chart-code" markdown="block">
<summary><i class="fas fa-code" aria-hidden="true"></i> <span class="chart-code__show">Show the code</span><span class="chart-code__hide">Hide the code</span></summary>

```python
# pip install financetoolkit
from financetoolkit import Economics

economics = Economics(start_date="1086-01-01")

data = economics.get_millennium_of_macroeconomic_data(
    series=["Earnings per head", "Consumer price index"]
)

# as an index with the average of 1340 to 1347 at 100
data = data / data.loc["1340":"1347"].mean() * 100
data = data.loc["1330":"1450"]
```

</details>

In the first years after the plague both went up: prices rose by 19.6% in 1350 and 19.1% in 1351, and by 1351 they were at 134 while earnings per head were at 190. After that the two lines separate. Prices drifted back down to an average of 116 between 1400 and 1449, while earnings kept rising to an average of 223.

**Nominal pay more than doubled while prices ended only slightly higher, so the gain in real wages came from pay.** Given the Statute of Labourers, that is quite remarkable. Employers who needed people to bring in the harvest had to compete for them, and the data suggests the law could slow that competition but not stop it. It stayed a source of tension: the labour laws were one of the grievances behind the Peasants' Revolt of 1381.

## Less Output, More of It per Person

Fewer people produce less. The question for living standards is what happened to output per person. Real GDP and real GDP per head, again with 1340 to 1347 at 100:

{% include ft-chart.html id="bd-output" src="/assets/data/article-charts.json" label="Real GDP and real GDP per head of England, 1330 to 1450" %}

<details class="chart-code" markdown="block">
<summary><i class="fas fa-code" aria-hidden="true"></i> <span class="chart-code__show">Show the code</span><span class="chart-code__hide">Hide the code</span></summary>

```python
# pip install financetoolkit
from financetoolkit import Economics

economics = Economics(start_date="1086-01-01")

data = economics.get_millennium_of_macroeconomic_data(
    series=["Real GDP of England at market prices", "Population (England)"]
)
data["Real GDP per head"] = data["Real GDP of England at market prices"] / data["Population (England)"]
data = data[["Real GDP of England at market prices", "Real GDP per head"]]

# as an index with the average of 1340 to 1347 at 100
data = data / data.loc["1340":"1347"].mean() * 100
data = data.loc["1330":"1450"]
```

</details>

Real GDP fell to 69 in 1351 and averaged 59 between 1400 and 1449. The economy as a whole shrank by about 40%, close to the loss of people. Real GDP per head moved the other way: 125 in 1351 and 138 on average between 1400 and 1449.

**Each remaining worker produced more, because the same land and tools were shared among fewer people.** The worst land went out of use, and farmers moved from labour-intensive grain growing to sheep and cattle, which needed fewer hands. This is the textbook result of a fall in the amount of labour compared to the other factors of production: the marginal worker becomes more productive, and that shows up in wages.

## The Gains Lasted Until the Population Came Back

The last chart puts population and real wages on the same scale from 1250 to 1700, both with 1340 to 1347 at 100:

{% include ft-chart.html id="bd-long-run" src="/assets/data/article-charts.json" label="Population and real wages in England, 1250 to 1700" %}

<details class="chart-code" markdown="block">
<summary><i class="fas fa-code" aria-hidden="true"></i> <span class="chart-code__show">Show the code</span><span class="chart-code__hide">Hide the code</span></summary>

```python
# pip install financetoolkit
from financetoolkit import Economics

economics = Economics(start_date="1086-01-01")

data = economics.get_millennium_of_macroeconomic_data(
    series=["Population (England)", "Real consumption wages"]
)

# as an index with the average of 1340 to 1347 at 100
data = data / data.loc["1340":"1347"].mean() * 100
data = data.loc["1250":"1700"]
```

</details>

The two lines are close to mirror images. While the population stayed low, between 1.90 and 2.20 million throughout the 15th century, real wages stayed high. Once the population started growing again in the 1500s, from 2.20 million in 1500 to 4.11 million in 1600, the real wage fell: from 201 between 1450 and 1499 to 167 in the first half of the 16th century, 129 in the second half and 102 between 1600 and 1649. That is back to where it was before the plague. Prices did most of the work this time: between the second half of the 15th century and the first half of the 17th, consumer prices rose more than fourfold, while earnings per head little more than doubled.

**The real wage did not reach its late 15th century level again until 1865, well into the Industrial Revolution.** This pattern, where wages rise when people are scarce and fall when the population catches up, is what Thomas Malthus described in 1798, and pre-industrial England follows it quite closely. Real GDP per head, by contrast, stayed around 135 to 145 through the 1500s and early 1600s, so the fall in wages did not come from a fall in output per person. The data alone does not say where the difference went, though landowners collecting higher rents as land became scarce again are a likely part of it.

## What the Black Death Shows About Labour Scarcity

The Black Death is an extreme case, but the mechanism is one that economists still use. When labour becomes scarce compared to capital and land, its price goes up, and attempts to cap it by law work poorly when employers compete for the same workers. In England the effect was large (a doubling of the real wage) and lasting (more than a century). It reversed as soon as the population recovered.

For a professional today, the closest modern relatives are labour supply shocks: an ageing workforce, a sharp change in migration or a pandemic that keeps people out of work for a while. The scale is far smaller, and a modern economy can replace labour with capital far more easily than a 14th-century farm could. The direction of the effect is the same, which is why demographics belong in a long-term view of wages, inflation and the share of income that goes to labour.

There are clear limits to this. The figures are reconstructions, especially before 1500, and the population is interpolated between benchmark years. The real wage tracks a particular group of workers and a particular basket of goods. And the data covers England only, while the plague hit all of Europe, with different results in different places. Even so, every series in the dataset points the same way after 1348.

The next article in the series looks at a much more recent shock: the oil price crash of 2014 to 2016.

> **Try this with the Finance Toolkit MCP:** *"Using the Bank of England's millennium of macroeconomic data, compare the population of England and the real consumption wage from 1300 to 1650. How much did the population fall during the Black Death, how far did real wages rise afterwards, and when were both back at their pre-plague levels?"*

{% include ft-charts-script.html %}
