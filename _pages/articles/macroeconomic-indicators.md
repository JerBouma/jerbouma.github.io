---
title: One Inflation Shock, Five Different Policy Responses
seo_title: "Real Interest Rates in Five Economies Since 2019"
date: 2026-07-14
last_modified_at: 2026-11-18
permalink: /articles/macroeconomic-indicators-finance-toolkit
excerpt: "At the end of 2022 Brazil's policy rate was 13.75%, above its 9.3% inflation, while the US, UK, Germany and Japan kept theirs below inflation. From 2021 to 2025 Brazil's real policy rate averaged 6.1%, and the other four averaged below zero."
description: "Inflation, central bank policy rates, real interest rates, unemployment and government debt in the US, UK, Germany, Japan and Brazil from 2019 to 2025."
layout: single
classes: wide-sidebar article-document
author_profile: false
collection: article
tags: [Macroeconomics]
share: true
standfirst: "Five central banks faced the same inflation shock, and only one kept its rate above inflation. The real policy rate shows which of them tightened, and what that meant for jobs and debt."
key_points:
  - "From 2021 to 2025 Brazil's real policy rate averaged 6.1%, while the United States, the United Kingdom, Germany and Japan all averaged below zero."
  - "The Fed raised its rate by more than five percentage points, while US unemployment rose by less than one."
  - "Measured monthly, Brazil's average real rate falls from 6.1% to 4.9%, and leaving out 2022 lifts the US to -0.2% and the UK to -0.5%."
cover:
  image: /assets/images/articles/macroeconomic-indicators/cover.jpg
  alt: "A bird's-eye watercolour of the Bank of England, drawn as if in ruins, its banking halls open to view."
  credit: "Aerial cutaway view of Soane's Bank of England, 1830, Joseph Gandy, public domain"
  link: "https://commons.wikimedia.org/wiki/File:Aerial_cutaway_view_of_Soane%27s_Bank_of_England_by_JM_Gandy_1830.jpg"
  creator: "Joseph Gandy"
  license: "https://creativecommons.org/publicdomain/mark/1.0/"
---

At the end of 2022 the Bank of England's policy rate was 3.5%, while consumer prices in the United Kingdom had risen 9.1% over the year. In Brazil the central bank's rate stood at 13.75%, comfortably above the country's own inflation of 9.3%.

How differently did large economies come through the same inflation shock? The real policy rate, the central bank's rate minus inflation, shows it best: Brazil kept it positive in every year from 2021 and averaged 6.1% up to 2025, while the United States, the United Kingdom, Germany and Japan all averaged below zero. The real rate is what decides whether monetary policy restrains spending, and whether savers and lenders are paid for waiting or lose to inflation. I follow these five economies from 2019 to 2025 through inflation, policy rates, real rates, unemployment and government debt, with yearly figures from the Global Macro Database.

## Brazil's Inflation Came First and Rose Furthest

The global inflation spike is usually talked about as one event, but it reached these five economies at different times. Inflation here is the yearly change in consumer prices.

Brazil's inflation took off in 2021, a year before the other four:

{% capture code_inflation %}
```python
# pip install financetoolkit
from financetoolkit import Economics

economics = Economics(start_date="2019-01-01", end_date="2025-12-31")

inflation = economics.get_inflation_rate(countries=["United States", "United Kingdom", "Germany", "Japan", "Brazil"], period="yearly")

# the total rise in prices from 2019 to 2025 (the table below the chart)
price_increase = (1 + inflation.loc["2020":"2025"]).prod() - 1
```
{% endcapture %}
{% include ft-chart.html id="macro-inflation" src="/assets/data/article-charts.json" label="Consumer price inflation by country" code=code_inflation mcp="What was the yearly inflation rate of the United States, United Kingdom, Germany, Japan and Brazil from 2019 to 2025, which country's inflation rose first, and how much did prices rise in total in each country between 2019 and 2025?" %}

By then Brazil was at 8.3%, while Japan still had slightly falling prices. The developed economies caught up in 2022, with the UK peaking at 9.1%. Brazil was also the first to come down: its inflation halved to 4.6% in 2023, when the UK's was still above 7%.

Compounded from 2019 to 2025, those yearly rates leave Brazil's price level far ahead of the rest:

| Country | Rise in consumer prices, 2019 to 2025 |
|---|---|
| Brazil | 40.0% |
| United Kingdom | 28.3% |
| United States | 26.0% |
| Germany | 25.1% |
| Japan | 11.9% |

**Prices in Brazil rose 40% over these six years, against about a quarter in the US, the UK and Germany.** That total is what a holder of cash or nominal bonds had to earn over the period just to stand still.

Japan's prices rose by less than half as much as those three. By 2025, though, Japan's 3.2% was higher than the US and German rates.

The different timing carried straight through to interest rates, because each central bank moves on its own country's data. The policy rate is the rate a central bank sets for overnight lending to banks, its main lever against inflation.

Brazil started hiking a year before the Federal Reserve and the Bank of England:

{% capture code_rates %}
```python
# pip install financetoolkit
from financetoolkit import Economics

economics = Economics(start_date="2019-01-01", end_date="2025-12-31")

policy_rate = economics.get_central_bank_policy_rate(countries=["United States", "United Kingdom", "Germany", "Japan", "Brazil"], period="yearly")
```
{% endcapture %}
{% include ft-chart.html id="macro-rates" src="/assets/data/article-charts.json" label="Central bank policy rates" code=code_rates mcp="Show the yearly central bank policy rate for the United States, United Kingdom, Germany, Japan and Brazil from 2019 to 2025. Which country hiked first, which hiked the most, and which barely moved?" %}

Brazil's rate went from 2.0% at the end of 2020 to 13.75% two years later. It then cut to 11.75% in 2023 while the Fed and the Bank of England were still raising, and turned around again when inflation came back, so by 2025 its policy rate was 15%, higher than at the 2022 peak. The European Central Bank, whose rate stands in for Germany here, was the slowest of the four to start hiking.

Japan barely took part. The Bank of Japan held its rate at -0.1% through the whole inflation shock and only reached 0.75% in 2025. After more than a decade of fighting deflation, it looked through 3% inflation and left its rate where it was.

## Only Brazil Kept Its Real Policy Rate Above Zero

Which of these hikes actually tightened policy? Only the ones that took the rate above inflation, and a nominal rate says little about that on its own: 4% is tight with 1% inflation and loose with 9%. I calculate the real policy rate as the policy rate minus inflation in the same year, so a negative figure means money lent at the central bank's rate lost purchasing power over the year.

Germany, the UK and the US spent 2021 and 2022 well below zero, while Brazil stayed above it:

{% capture code_real_rates %}
```python
# pip install financetoolkit
from financetoolkit import Economics

economics = Economics(start_date="2019-01-01", end_date="2025-12-31")

real_policy_rate = economics.get_real_interest_rate(countries=["United States", "United Kingdom", "Germany", "Japan", "Brazil"], rate_type="policy", period="yearly")

# the average and lowest real rate from 2021 to 2025 (the table below the chart)
summary = real_policy_rate.loc["2021":"2025"].agg(["mean", "min"])
```
{% endcapture %}
{% include ft-chart.html id="macro-real-rates" src="/assets/data/article-charts.json" label="Real central bank policy rates" code=code_real_rates mcp="What was the real central bank policy rate, the policy rate minus inflation, of the United States, United Kingdom, Germany, Japan and Brazil each year from 2019 to 2025, and what were each country's average and lowest real rate from 2021 to 2025?" %}

In 2022, the worst year of the shock, all four developed economies had negative real rates, and Germany's fell furthest, to -8.2%. Nominal hikes of four to five percentage points took time to get ahead of inflation, so the US only got back above zero in 2023 and the UK in 2024. Japan's real rate has been negative in every year since 2022.

Brazil's real rate, on the other hand, rose every year from 2022 and reached 10.0% in 2025. Averaged over 2021 to 2025, it is the only one of the five with a positive figure in either column:

| Country | Average real policy rate, 2021 to 2025 | Lowest yearly value |
|---|---|---|
| Brazil | 6.1% | 0.9% |
| United States | -0.9% | -4.6% |
| United Kingdom | -1.5% | -5.6% |
| Japan | -2.2% | -3.4% |
| Germany | -2.7% | -8.2% |

**In the yearly figures, Brazil's was the only one of the five central banks that kept its rate above inflation from 2021 onwards.**

## Higher Rates Cost Few Jobs

Sharp rate hikes are supposed to cool the labour market, and in these five economies they did so only a little. The unemployment rate is the share of the labour force looking for work without finding it.

US unemployment barely rose after the Fed started hiking, and Brazil's kept falling:

{% capture code_unemployment %}
```python
# pip install financetoolkit
from financetoolkit import Economics

economics = Economics(start_date="2019-01-01", end_date="2025-12-31")

unemployment = economics.get_unemployment_rate(countries=["United States", "United Kingdom", "Germany", "Japan", "Brazil"], period="yearly")
```
{% endcapture %}
{% include ft-chart.html id="macro-unemployment" src="/assets/data/article-charts.json" label="Unemployment rates" code=code_unemployment mcp="What was the yearly unemployment rate of the United States, United Kingdom, Germany, Japan and Brazil from 2019 to 2025, and did it rise when central banks raised rates?" %}

The one large jump in the chart is the pandemic: US unemployment went to 8.1% in 2020 and was back at its 2019 level by 2022, the year the Fed started hiking. It stayed there in 2023 and only crept up to 4.3% by 2025, when the Fed was already cutting. **The Fed raised its rate by more than five percentage points and unemployment rose by less than one.** The real rate likely explains part of this, because US policy only became restrictive in real terms in 2023, and then only by a little. That is my reading: the yearly data shows the timing but cannot prove the cause.

Germany's unemployment rose by about as much as the US's, and the UK's rose the most of the five, about one percentage point from 2022 to 2025. Brazil went the other way: with the highest policy rate of the five in every year, its unemployment still fell from 13.8% in 2020 to 6.0% in 2025. Japan's rate barely moved, and neither did its unemployment.

## US and UK Debt Stayed Well Above Pre-Pandemic Levels

The pandemic pushed all five debt ratios up in 2020, and they came back at very different speeds. Government debt to GDP compares what a government owes with what the economy produces in a year. Higher rates make that debt more expensive to carry, while inflation raises nominal GDP and shrinks the ratio.

The US and UK ratios came only part of the way back from 2020 and rose again after 2022 (Japan and Brazil don't have a 2025 figure yet, so the chart ends in 2024):

{% capture code_debt %}
```python
# pip install financetoolkit
from financetoolkit import Economics

economics = Economics(start_date="2019-01-01", end_date="2024-12-31")

debt_to_gdp = economics.get_government_debt_to_gdp_ratio(countries=["United States", "United Kingdom", "Germany", "Japan", "Brazil"])
```
{% endcapture %}
{% include ft-chart.html id="macro-debt" src="/assets/data/article-charts.json" label="Government debt to GDP" code=code_debt mcp="Compare government debt to GDP for the United States, United Kingdom, Germany, Japan and Brazil from 2019 to 2024. Which countries reduced their debt burden after the 2020 spike, and which kept climbing?" %}

All five ratios are below their 2020 peak, but they differ a lot in how far they came back. The US reached 122% of GDP in 2024 and the UK 100%, and both were higher than in 2022. **The US and UK ended 2024 about 13.5 and 15 percentage points above their 2019 debt ratios.** Germany is only a few points above its 2019 level and Brazil is back where it started.

Japan's ratio is far above the rest, at 214% of GDP in 2024, but it has come down from 229% in 2020. With inflation above the policy rate every year since 2022, prices lifted nominal GDP while borrowing stayed cheap, which shrinks the ratio without any repayment. Brazil had high inflation too, but with a real rate of 7% to 10% from 2023 its debt was far more expensive to carry, and its ratio rose again after 2022.

## Year-End Rates Flatter the Hiking Years

In a year of hikes, the yearly real rates above make policy look tighter than it was for most of the year, because they set the rate at the end of the year against the inflation of the whole year. A monthly real rate, the policy rate at the end of each month minus inflation over the twelve months to that month, shows how much this matters.

Measured three ways, the average from 2021 to 2025 keeps Brazil first, and leaving out 2022 brings the US and UK close to zero:

{% capture code_real_rates_check %}
```python
# pip install financetoolkit
from financetoolkit import Economics

economics = Economics(start_date="2019-01-01", end_date="2025-12-31")

real_policy_rate = economics.get_real_interest_rate(countries=["United States", "United Kingdom", "Germany", "Japan", "Brazil"], rate_type="policy", period="yearly")
monthly_real_policy_rate = economics.get_real_interest_rate(countries=["United States", "United Kingdom", "Euro Area", "Japan", "Brazil"], rate_type="policy")

# the average real policy rate from 2021 to 2025, measured three ways (the chart)
yearly = real_policy_rate.loc["2021":"2025"].mean()
yearly_without_2022 = real_policy_rate.loc[["2021", "2023", "2024", "2025"]].mean()
monthly = monthly_real_policy_rate.loc["2021-01":"2025-12"].mean()

# Brazil in 2021: the yearly figure against the average of its twelve months
brazil_2021 = real_policy_rate.loc["2021", "Brazil"], monthly_real_policy_rate.loc["2021", "Brazil"].mean()
```
{% endcapture %}
{% include ft-chart.html id="macro-real-rates-check" src="/assets/data/article-charts.json" label="Average real policy rates measured three ways" code=code_real_rates_check mcp="What was the average real central bank policy rate of the United States, United Kingdom, Germany, Japan and Brazil from 2021 to 2025 with yearly data, with yearly data leaving out 2022, and with monthly data using the euro area in place of Germany? And what was Brazil's monthly real policy rate in each month of 2021?" %}

Brazil is the clearest case. Its yearly real rate for 2021 is 0.9%, because the 9.25% it ended the year at is set against the inflation of the whole year. Month by month, its rate was below inflation throughout 2021, by 3.5 percentage points on average, and only stayed above it from May 2022.

**Measured monthly, Brazil's average real rate from 2021 to 2025 falls from 6.1% to 4.9%, and it is still the only one of the five above zero.** The monthly figures also use the ECB's own rate against euro area inflation, in place of the yearly database's rate for Germany. On that basis the euro area averaged -2.0% against Germany's -2.7%, which lifts it from last place to fourth, just above Japan.

The yearly averages lean heavily on 2022, the year inflation peaked. Leaving it out lifts the US to -0.2% and the UK to -0.5%, close to zero, while Japan is at -2.0% and Brazil rises slightly. In every version Brazil comes first and the US and UK next, and only Germany and Japan swap places at the bottom. How far below zero the US and UK were, though, depends mostly on that one year.

## What This Means for the Next Cycle

For a professional, the real policy rate is the measure to watch. A positive one restrains spending and is costly for a heavily indebted government. A negative one erodes the real value of debt and of savings alike.

Five countries in mostly yearly figures show the direction and the order of events well, but not whether the same pattern holds elsewhere. Within them, Brazil shows the first case, with a real rate of 10% in 2025 and a labour market that had not turned by then. Japan shows the second, and its debt ratio is the series to follow as the Bank of Japan moves its rate closer to inflation.

The US and UK sit in between. Their real rates were back just above zero by 2025, while their debt ratios were still well above 2019, so every percentage point of real rate costs their budgets more than it did before the pandemic.

### Data and method

- **Source:** the [Global Macro Database](https://www.globalmacrodata.com){:target="_blank"} (Müller, Xu, Lehbib and Chen, 2025) in its September 2026 release, which combines 167 sources, among them the IMF, the OECD, the World Bank and Eurostat, into one yearly panel per country. I use 2019 to 2025 (to 2024 for debt). The monthly check uses the policy rates of the Bank for International Settlements (BIS) and consumer prices from Eurostat, the Office for National Statistics, the Statistics Bureau of Japan and the BIS.
- **How the series are built:** inflation is the yearly change in the consumer price index. The policy rate is the central bank's rate at the end of each year, with the euro area rate for Germany. For the US, UK, Japan and Brazil it matches the December rates the BIS publishes. Debt to GDP is the database's consolidated general and central government figure.
- **What I did to it:** I left out the years the database projects from the IMF's World Economic Outlook, and ended the debt chart in 2024 because Japan and Brazil have no 2025 figure. The real policy rate is the policy rate minus the same year's inflation. The total price rise compounds the yearly inflation rates from 2020 to 2025, and the averages are simple averages of the yearly figures. For the monthly check I took the policy rate at the end of each month minus inflation over the previous twelve months and averaged the months from January 2021 to December 2025. The euro area replaces Germany there, with the ECB's main refinancing rate up to September 17, 2024 and its deposit rate after that, as the BIS reports it. The US has no inflation figure for October 2025, so its average covers 59 months instead of 60.
- **Limits:** the real rate uses the inflation of the same year, measured afterwards, not the inflation people expected when the rate was set. Countries define and survey unemployment differently, so I compare each country's unemployment with its own history. The latest year of each series can still be revised.
- **Reproduce it:** the charts are made with the [Finance Toolkit](/projects/financetoolkit), my open-source Python library, which reads these datasets directly. The Python button on each chart shows the code and the MCP button a question that returns the same data. The functions are documented under [Economics](/projects/financetoolkit/docs/economics).
- **Further reading:** Müller, Xu, Lehbib and Chen (2025), [The Global Macro Database: A New International Macroeconomic Dataset](https://www.nber.org/papers/w33714){:target="_blank"}, NBER Working Paper 33714, on how the data is put together. Taylor (1993), [Discretion versus Policy Rules in Practice](https://ideas.repec.org/a/eee/crcspp/v39y1993ip195-214.html){:target="_blank"}, Carnegie-Rochester Conference Series on Public Policy, the Taylor rule. Holston, Laubach and Williams (2023), [Measuring the Natural Rate of Interest after COVID-19](https://www.newyorkfed.org/research/staff_reports/sr1063){:target="_blank"}, New York Fed Staff Report 1063, on the neutral real rate.

{% include ft-charts-script.html %}
