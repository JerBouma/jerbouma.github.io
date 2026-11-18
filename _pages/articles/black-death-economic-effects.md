---
title: "The Black Death's Economic Effects on English Wages"
seo_title: "The Black Death's Economic Effects on Wages"
date: 2026-11-17
last_modified_at: 2026-11-18
permalink: /articles/black-death-economic-effects
excerpt: "England lost 46% of its population between 1348 and 1351. Real wages roughly doubled over the next century and stayed high until the population came back."
description: "Economic effects of the Black Death in England: population fell 46% in three years and real wages doubled, from the Bank of England's data since 1086."
layout: single
classes: wide-sidebar article-document
author_profile: false
collection: article
tags: [Macroeconomics, History]
share: true
standfirst: "The plague of 1348 to 1351 killed almost half of England. The survivors could suddenly ask for more, and the Bank of England's millennium of data shows how much more they got and how long it lasted."
key_points:
  - "England's population fell 46% between 1348 and 1351, and by 1450 it was 60% below its 1348 level."
  - "The real wage averaged 201 between 1450 and 1499, double its level before the plague (1340 to 1347 = 100)."
  - "Pay rose while prices did not, and the gains lasted until the population came back in the sixteenth century."
cover:
  image: /assets/images/articles/black-death-economic-effects/cover.jpg
  alt: "A scorched landscape in which an army of skeletons sweeps across the countryside and cuts down people of every rank."
  credit: "The Triumph of Death, c. 1562, Pieter Bruegel the Elder, Museo del Prado, public domain"
  link: "https://commons.wikimedia.org/wiki/File:The_Triumph_of_Death_by_Pieter_Bruegel_the_Elder.jpg"
  creator: "Pieter Bruegel the Elder"
  license: "https://creativecommons.org/publicdomain/mark/1.0/"
---

In 1348, England had 4.81 million people. Three years later, after the Black Death had passed through, it had 2.60 million. That is a fall of 46%, the largest three-year drop in population in the Bank of England's record of the English economy, which starts in 1086.

What happens to wages, prices and output when nearly half of the workforce disappears while the land, the buildings and the tools are all still there? In England, the real wage of an ordinary worker roughly doubled within a century, mostly because pay rose while prices did not, and it stayed high for as long as the population stayed low. That makes it one of the clearest natural experiments on what scarce labour does to its price. This first article of a weekly series on economic history follows England from 1250 to 1700 with the Bank of England's "[A millennium of macroeconomic data](https://www.bankofengland.co.uk/statistics/research-datasets){:target="_blank"}".

## Almost Half of England Gone in Three Years

The population of England, in millions, recovered from the famine of the 1310s and then fell by almost half in three years:

{% capture code_population %}
```python
# pip install financetoolkit
from financetoolkit import Economics

economics = Economics(start_date="1086-01-01")

population = economics.get_millennium_of_macroeconomic_data(series="Population (England)")
population = population.loc["1300":"1500"] / 1000  # in millions
```
{% endcapture %}
{% include ft-chart.html id="bd-population" src="/assets/data/article-charts.json" label="Population of England, 1300 to 1500" code=code_population mcp="How did the population of England change between 1300 and 1500, according to the Bank of England's millennium of macroeconomic data?" %}

The Great Famine of 1315 to 1317 shows up as a fall from 4.69 million in 1315 to 4.12 million in 1325, after which it grew again to its peak of 4.81 million in 1348.

**England lost 46% of its people in three years and kept losing them: by 1450 it had 1.90 million, 60% fewer than in 1348.** Plague returned every decade or two, and the population did not pass its 1348 level again until 1622. For an economist, that is a lasting fall in labour compared to land.

## Real Wages Roughly Doubled

The workers who survived could buy far more with a day's work. The real consumption wage measures that: the nominal day wage divided by the price of a basket of what workers bought, mostly food, fuel and clothing. With the average of 1340 to 1347, the eight years before the plague, at 100:

{% capture code_wages %}
```python
# pip install financetoolkit
from financetoolkit import Economics

economics = Economics(start_date="1086-01-01")

wages = economics.get_millennium_of_macroeconomic_data(series="Real consumption wages")

# the plague waves: the average real wage of the ten years after the first plague
# year compared to the ten years before, in %
real_wage = wages["Real consumption wages"]


def wave_change(year, window=10):
    before = real_wage.loc[str(year - window) : str(year - 1)].mean()
    after = real_wage.loc[str(year + 1) : str(year + window)].mean()
    return (after / before - 1) * 100


waves = {year: wave_change(year) for year in [1348, 1361, 1369, 1375]}
any_year = sum(wave_change(year) for year in range(1260, 1691)) / len(range(1260, 1691))

# as an index with the average of 1340 to 1347 at 100
wages = wages / wages.loc["1340":"1347"].mean() * 100
wages = wages.loc["1300":"1550"]
```
{% endcapture %}
{% include ft-chart.html id="bd-wages" src="/assets/data/article-charts.json" label="Real consumption wages in England, 1300 to 1550" code=code_wages mcp="What happened to real consumption wages in England between 1300 and 1550, using the Bank of England's millennium of macroeconomic data, and in which year did they peak?" %}

Wages jumped from one year to the next with the harvest, by around 11% on average before 1348, so single years say little. Averaged over periods, the real wage climbed step by step, from 136 in the 1350s to 162 between 1360 and 1399 and 193 in the first half of the fifteenth century. It slid back once the population grew again: 167 between 1500 and 1549, 129 in the second half of the sixteenth century and 102 between 1600 and 1649, close to where it started.

**Between 1450 and 1499 the real wage averaged 201, double its level before the plague.** The rise took decades, partly because in 1349 the Crown issued the Ordinance of Labourers, followed by the Statute of Labourers in 1351, which tried to hold wages at their pre-plague levels and made it an offence to ask for more.

After 1348 to 1349, plague returned across England in 1361 to 1362, 1369 and 1375. Comparing the average real wage of the ten years after each first plague year with the ten years before, it rose by 28.3% around the Black Death, 2.9% around 1361 to 1362, 9.5% around 1369 and 22.5% around 1375, or 15.8% on average. The same comparison for every year from 1260 to 1690 comes to 0.8%, so in an ordinary decade the real wage barely moved.

The second wave of 1361 to 1362 left the smallest mark, even though the historian Philip Slavin argues it did more lasting demographic damage than the Black Death itself. That each wave pushed wages up by thinning the workforce again is my reading. The population series is interpolated between benchmark years and doesn't show the later waves, so the data shows the timing, not the cause.

## Pay Rose While Prices Did Not

A higher real wage can come from higher pay or from lower prices. To see which, here are nominal earnings per head and the consumer price index, both with the average of 1340 to 1347 at 100:

{% capture code_pay_prices %}
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
{% endcapture %}
{% include ft-chart.html id="bd-pay-prices" src="/assets/data/article-charts.json" label="Earnings per head and consumer prices in England, 1330 to 1450" code=code_pay_prices mcp="Compare earnings per head and the consumer price index of England from 1330 to 1450 in the Bank of England's millennium of macroeconomic data, both as an index with the average of 1340 to 1347 at 100." %}

Both went up at first, and prices rose by almost 20% in both 1350 and 1351. Then the two lines separated, and between 1400 and 1449 prices averaged 116 while earnings averaged 223.

**Nominal pay more than doubled while prices ended only slightly higher, so the gain in real wages came from pay.** Given the Statute of Labourers, that is quite remarkable. Employers who needed people to bring in the harvest had to compete for them, and the data suggests the law could slow that competition but could not stop it. The labour laws were one of the grievances behind the Peasants' Revolt of 1381.

## Shorter Hours Made Each Hour Worth Even More

The dataset also estimates average weekly hours. Dividing weekly earnings by those hours and by consumer prices gives real pay per hour. Weekly hours and, in the second tab, real pay per hour next to the real wage, with 1340 to 1347 at 100:

{% capture code_hours %}
```python
# pip install financetoolkit
from financetoolkit import Economics

economics = Economics(start_date="1086-01-01")

data = economics.get_millennium_of_macroeconomic_data(
    series=["Average weekly hours worked", "Earnings per head", "Consumer price index", "Real consumption wages"]
)
hours = data["Average weekly hours worked"].loc["1300":"1650"]

# weekly earnings per hour worked, divided by consumer prices
data["Real pay per hour"] = data["Earnings per head"] / data["Average weekly hours worked"] / data["Consumer price index"]
pay = data[["Real pay per hour", "Real consumption wages"]]

# as an index with the average of 1340 to 1347 at 100
pay = pay / pay.loc["1340":"1347"].mean() * 100
pay = pay.loc["1330":"1450"]
```
{% endcapture %}
{% include ft-chart.html id="bd-hours" src="/assets/data/article-charts.json" label="Weekly hours worked and real pay per hour in England, 1300 to 1650" code=code_hours mcp="Using the Bank of England's millennium of macroeconomic data, how did average weekly hours worked in England change between 1300 and 1650, and what happened to earnings per head divided by weekly hours and by the consumer price index between 1330 and 1450?" %}

Hours had already fallen a long way since the famine years, from 52 a week in 1315 to 31 in 1348. They kept falling after the plague, to about 25 by 1380, and averaged 30 again between 1400 and 1449.

**Between 1360 and 1399, real pay per hour averaged 211, about 30% above the real wage of 162.** Next to buying more with a day's work, workers needed fewer days to earn a year's living, and part of the gain was taken as time off. The hours estimate is partly built from the same wage data, so I trust the direction more than the size.

## Less Output, More of It per Person

For living standards, the question is output per person. Real GDP, real GDP per head and export volumes, again with 1340 to 1347 at 100:

{% capture code_output %}
```python
# pip install financetoolkit
from financetoolkit import Economics

economics = Economics(start_date="1086-01-01")

data = economics.get_millennium_of_macroeconomic_data(
    series=["Real GDP of England at market prices", "Population (England)", "Export volumes"]
)
data["Real GDP per head"] = data["Real GDP of England at market prices"] / data["Population (England)"]
data = data[["Real GDP of England at market prices", "Real GDP per head", "Export volumes"]]

# as an index with the average of 1340 to 1347 at 100
data = data / data.loc["1340":"1347"].mean() * 100
data = data.loc["1330":"1450"]
```
{% endcapture %}
{% include ft-chart.html id="bd-output" src="/assets/data/article-charts.json" label="Real GDP, real GDP per head and export volumes of England, 1330 to 1450" code=code_output mcp="How did real GDP, real GDP per head and export volumes of England change from 1330 to 1450 in the Bank of England's millennium of macroeconomic data, compared to the average of 1340 to 1347?" %}

Real GDP fell to 69 by 1351 and averaged 59 between 1400 and 1449, so the economy shrank by about 40% while the population fell by close to 60%.

**Real GDP per head moved the other way and averaged 138 between 1400 and 1449, because the same land and tools were shared among fewer people.** The worst land went out of use, and farmers moved from grain to sheep and cattle, which needed fewer hands. The marginal worker became more productive, and that showed up in wages.

Exports, mostly wool and woollen cloth, held up far better than the population. Between 1360 and 1399 they averaged 41% above the weak 1340s and about 12% below 1300 to 1339, so with half the people, exports per head rose by about two thirds.

## More Than Four Times as Much Coin per Person

Money became more plentiful per person as well. Coin in circulation is the silver and gold money in use, in pounds of the time. Coin per person and, in the second tab, the total in millions of pounds:

{% capture code_coin %}
```python
# pip install financetoolkit
from financetoolkit import Economics

economics = Economics(start_date="1086-01-01")

data = economics.get_millennium_of_macroeconomic_data(
    series=["Coin in circulation outside the Bank of England", "Population (England)"]
)
data = data.loc["1300":"1500"]

# coin in £ million and population in thousands, so this is £ per person
data["Coin per person"] = data["Coin in circulation outside the Bank of England"] * 1_000_000 / (data["Population (England)"] * 1000)
```
{% endcapture %}
{% include ft-chart.html id="bd-coin" src="/assets/data/article-charts.json" label="Coin in circulation in England, per person and in total, 1300 to 1500" code=code_coin mcp="Using the Bank of England's millennium of macroeconomic data, how did coin in circulation and coin in circulation per person in England change between 1300 and 1500?" %}

Coin per person rose from about £0.14 in 1348 to £0.63 in 1380. Part of that is the same money shared among half the people, but the total also rose, from £0.66 million to £1.53 million. Consumer prices were about the same in 1380 as in 1348, so the extra coin did not show up as inflation.

**Coin per person rose more than fourfold between 1348 and 1380.** The starting point was low, as the total had more than halved since 1319. The total fell back to about £0.60 million by 1500, with a low of £0.46 million in 1464, during what the historian John Day called "[The Great Bullion Famine of the Fifteenth Century](https://academic.oup.com/past/article-abstract/79/1/3/1435469){:target="_blank"}", a shortage of silver and gold across Europe. That same year had the lowest consumer prices of the century, and the real wage peaked.

## The Gains Lasted Until the Population Came Back

The real wage fell back as the population came back. Both from 1250 to 1700, with 1340 to 1347 at 100:

{% capture code_long_run %}
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
{% endcapture %}
{% include ft-chart.html id="bd-long-run" src="/assets/data/article-charts.json" label="Population and real wages in England, 1250 to 1700" code=code_long_run mcp="Compare the population of England and the real consumption wage from 1250 to 1700 in the Bank of England's millennium of macroeconomic data. When were both back at their levels from before the Black Death?" %}

Once the population grew again, nearly doubling between 1500 and 1600, the real wage slid back, and between 1600 and 1649 it averaged 102, about where it was before the plague. This time prices did the work, as consumer prices rose more than fourfold between the second half of the 15th century and the first half of the 17th, while earnings per head little more than doubled. Hours rose as well, from 31 in 1500 to 48 in 1600, so the extra time off was lost too.

**Apart from a few years around 1510, the real wage did not reach its late 15th-century average again until 1865.** This is the pattern Thomas Malthus described in 1798, where wages rise when people are scarce and fall when the population catches up. Real GDP per head stayed roughly level through the 1500s and early 1600s, so the fall in wages did not come from lower output per person. Where the difference went, the data does not say, although landowners collecting higher rents as land became scarce again are a likely part of it.

## Then and Now: War Made Labour Scarce Again

The dataset has a later episode of scarce labour. During the First World War the armed forces drew men out of the workforce, and the UK unemployment rate fell from 3.6% in 1913 to 0.3% in 1916. The labour share of income, the part of national income paid to workers, and the unemployment rate from 1905 to 1925, with average weekly hours in the second tab:

{% capture code_then_now %}
```python
# pip install financetoolkit
from financetoolkit import Economics

economics = Economics(start_date="1086-01-01")

data = economics.get_millennium_of_macroeconomic_data(
    series=["Labour share, whole economy excluding rents", "Unemployment rate", "Average weekly hours worked"]
)
data = data.loc["1905":"1925"]
```
{% endcapture %}
{% include ft-chart.html id="bd-then-now" src="/assets/data/article-charts.json" label="Labour share, unemployment rate and weekly hours in the UK, 1905 to 1925" code=code_then_now mcp="Using the Bank of England's millennium of macroeconomic data, how did the labour share of income, the unemployment rate and average weekly hours worked in the UK change between 1905 and 1925?" %}

**Labour's share of income rose from 66.6% in 1913 to 74.3% in 1920.** After the war, workers again took part of the gain as time off, and weekly hours fell from 55.6 in 1918 to 48.3 in 1920.

The scarcity ended in the slump of 1921, when unemployment jumped to 11%, yet hours stayed at about 46 a week through 1925 and the labour share stayed above 73%. Modern labour shocks are far smaller, and modern economies replace workers with machines more easily than a 14th-century farm. The mechanism is the same, though, and so are the series to watch for it: the working-age population, the unemployment rate, average hours and the labour share of income.

The next article in the series looks at a more recent shock, the oil price crash of 2014 to 2016.

### Data and method

**Source:** the Bank of England's "[A millennium of macroeconomic data for the UK](https://www.bankofengland.co.uk/statistics/research-datasets){:target="_blank"}" (version 3.1), 1250 to 1700 for England and 1905 to 1925 for the UK.

**How the series is built:** population is estimated for benchmark years and interpolated between them. Earnings and the real wage are based on daily wage rates of English labourers, and hours before 1770 on Humphries and Weisdorf (2016). Exports are mostly wool and woollen cloth, in 2013 prices, and coin is an end-of-year estimate in pounds of the time.

**What I did to it:** I indexed most series to the average of 1340 to 1347 and averaged the noisy ones over periods. Real pay per hour is earnings per head divided by weekly hours and by the consumer price index. Real GDP and exports are divided by population, and for coin per person I converted coin from millions of pounds and population from thousands before dividing. For the plague waves I compared the average real wage of the ten years after the first plague year with the ten years before, and the baseline does this for every year from 1260 to 1690. The windows overlap: the ten years after 1361 include the wave of 1369.

**Limits:** the figures are reconstructions, and the hours series is tentative. The real wage tracks particular groups of workers and one basket of goods. The data covers England only, while the plague hit all of Europe. The plague-wave comparison rests on four waves, and with five-year windows instead of ten the 1369 wave shows a fall of 3.1%.

**Reproduce it:** the charts are made with the [Finance Toolkit](/projects/financetoolkit), my open-source Python library, which reads this dataset directly ([Economics docs](/projects/financetoolkit/docs/economics)). The Python button on each chart shows the code and the MCP button a question that returns the same data.

**Further reading:** Stephen Broadberry, Bruce Campbell, Alexander Klein, Mark Overton and Bas van Leeuwen, "[British Economic Growth, 1270-1870](https://kar.kent.ac.uk/45320/){:target="_blank"}" (Cambridge University Press, 2015), the reconstruction of output and population that the dataset's early figures draw on. Jane Humphries and Jacob Weisdorf, "[Unreal Wages? Real Income and Economic Growth in England, 1260-1850](https://researchonline.lse.ac.uk/id/eprint/90328/){:target="_blank"}" (The Economic Journal, 2019), on why day wages overstate medieval incomes. Philip Slavin, "[Plague Strikes Back: The Pestis Secunda of 1361-62 and Its Demographic Consequences in England and Wales](https://www.stir.ac.uk/research/hub/publication/2233876){:target="_blank"}" (Journal of Medieval and Early Modern Studies, 2024), on the second wave.

{% include ft-charts-script.html %}
