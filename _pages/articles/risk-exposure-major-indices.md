---
title: What Volatility Misses About Risk in Major Indices
seo_title: "Tail Risk Across Major Indices"
date: 2026-07-21
last_modified_at: 2026-11-18
permalink: /articles/risk-exposure-major-indices-finance-toolkit
excerpt: "Six trading days in April 2025 pushed the S&P 500's kurtosis to 26.6, nine times its 2023 reading, while its volatility rose by about half. Five risk measures across six major indices show what volatility misses."
description: "Value at Risk, CVaR, maximum drawdown, skewness and kurtosis for SPY, QQQ, DIA, IWM, EFA and EEM from 2019 to 2025, and what volatility alone misses."
layout: single
classes: wide-sidebar article-document
author_profile: false
collection: article
tags: [Risk & Derivatives]
share: true
standfirst: "Volatility weighs every trading day alike. Five tail measures across six index ETFs show which years had their risk packed into a handful of days, and why that calls for different protection."
key_points:
  - "Six trading days in April 2025 pushed SPY's kurtosis to 26.6, about nine times its 2023 reading, while its volatility was only about 1.5 times its 2023 level."
  - "In 2020 SPY's historical CVaR was -5.45%, against -4.25% under a normal distribution with the same volatility, so the worst days were about 30% worse than volatility implied."
  - "A single day can flip a yearly reading: leave out April 9 and SPY's skewness for 2025 becomes -1.51 instead of 1.51."
cover:
  image: /assets/images/articles/risk-exposure-major-indices/cover.jpg
  alt: "A huge clawed wave curls over fishing boats, with Mount Fuji small in the distance."
  credit: "Under the Wave off Kanagawa, Katsushika Hokusai, Art Institute of Chicago, CC0"
  link: "https://commons.wikimedia.org/wiki/File:1952.343_-_Under_the_Wave_off_Kanagawa_(Kanagawa_oki_nami.jpg"
  creator: "Katsushika Hokusai"
  license: "https://creativecommons.org/publicdomain/zero/1.0/"
---

On April 9, 2025, the day the US paused most of its new tariffs, the S&P 500 ETF (SPY) rose 10.5%, its largest daily gain between 2019 and 2025. Five days earlier it had fallen 5.85%. Those few days pushed the kurtosis of SPY's daily returns for 2025, a measure of how fat the tails are, to 26.6. That is about nine times its reading in 2023.

How much of a year's risk can a handful of days carry, and which measures show it? In 2025 those days set most of the year's tail risk, and volatility is the measure that shows it least. SPY's volatility, by comparison, was only about 1.5 times its 2023 level. Leave out the six trading days from April 3 to April 10 and the kurtosis drops to 4.4, close to its 2024 reading. A standard deviation spreads risk evenly over the year, so it can't tell a year of many bad days from a year with a few extreme ones, and those call for different protection. I compare five measures across six index ETFs, the S&P 500 (SPY), Nasdaq 100 (QQQ), Dow Jones (DIA), Russell 2000 (IWM), MSCI EAFE (EFA) and MSCI Emerging Markets (EEM), with daily prices from FinancialModelingPrep for 2019 to 2025.

## In 2020 the Worst Days Were About 30% Worse Than Volatility Implied

How much worse were the worst days than volatility implied? Value at Risk (VaR) at 95% confidence is the daily loss that is only exceeded on the worst 5% of trading days, and [Conditional Value at Risk](/projects/financetoolkit/docs/risk/conditional-value-at-risk-cvar) (CVaR) is the average loss on those days. Both can be read from the actual returns (historical) or from a normal distribution with the same mean and volatility, which is what volatility alone implies. Where the historical figure sits beyond the normal one, the tail was fatter than volatility suggests.

Compare the historical and normal CVaR of 2020 with those of 2022, with one tab per index:

{% capture code_var %}
```python
# pip install financetoolkit
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["SPY", "QQQ", "DIA", "IWM", "EFA", "EEM"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2019-01-01", end_date="2025-12-31", benchmark_ticker=None)

normal_var = toolkit.risk.get_value_at_risk(period="yearly", within_period=True, distribution="gaussian")
historical_var = toolkit.risk.get_value_at_risk(period="yearly", within_period=True)
normal_cvar = toolkit.risk.get_conditional_value_at_risk(period="yearly", within_period=True, distribution="gaussian")
historical_cvar = toolkit.risk.get_conditional_value_at_risk(period="yearly", within_period=True)
```
{% endcapture %}
{% include ft-chart.html id="risk-var" src="/assets/data/article-charts.json" label="Normal and historical Value at Risk and Conditional Value at Risk" code=code_var mcp="What were the Value at Risk and Conditional Value at Risk at the 95 percent confidence level of SPY, QQQ, DIA, IWM, EFA and EEM within each calendar year from 2019 to 2025, both historical and under a normal distribution, and in which years did the historical CVaR go furthest beyond the normal CVaR?" %}

In 2020 SPY's historical CVaR was -5.45%, while a normal distribution with the same volatility put it at -4.25%. **The worst days of 2020 were about 30% worse than volatility implied, and every index shows a gap of at least 24% that year.**

In 2022 the two were close to equal for all six indices, which fits a bear market made of many bad days and few extreme ones. The calm year 2019, on the other hand, had SPY's historical CVaR 29% beyond the normal one, driven by the trade-war selloffs of May and August.

The year 2025 sits between the two. The April days pushed up volatility for the whole year, so the normal VaR was more cautious than the historical one in every index, and still SPY's historical CVaR ended up 12% beyond its normal value. Next to that, IWM has the worst or second-worst historical CVaR in every year, including 2024 at -2.9%, a calm year for SPY and DIA.

## Small Caps Fell the Furthest, 41.1% in 2020

VaR and CVaR come from the spread of daily returns, so they say nothing about how far a fall runs over weeks. Maximum drawdown does: it is the actual fall from a peak to the lowest point after it, measured here within each calendar year, so it is the loss of someone who bought at that year's high and held on to its low.

The darkest rows are 2020 and 2022, where a deeper fall has a stronger colour:

{% capture code_drawdown %}
```python
# pip install financetoolkit
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["SPY", "QQQ", "DIA", "IWM", "EFA", "EEM"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2019-01-01", end_date="2025-12-31", benchmark_ticker=None)

max_drawdown = toolkit.risk.get_maximum_drawdown(period="yearly", within_period=True)
```
{% endcapture %}
{% include ft-chart.html id="risk-drawdown" src="/assets/data/article-charts.json" label="Maximum drawdown per year" code=code_drawdown mcp="What was the maximum drawdown of SPY, QQQ, DIA, IWM, EFA and EEM within each calendar year from 2019 to 2025, which index had the single worst drawdown and which was the most resilient?" %}

**The COVID crash took IWM down 41.1% in 2020, the deepest fall of any index in any year here.** That fits small caps having less balance sheet cushion and thinner trading in a panic. This is my reading of it, since the data shows how far they fell and not why. In 2022 it was the Nasdaq's turn: QQQ fell 34.8%, the worst of that year, in the year [the Fed, the Bank of England and the ECB raised rates against inflation](/articles/macroeconomic-indicators-finance-toolkit). Growth stocks, whose earnings lie furthest ahead, are the most exposed to higher rates.

DIA never had the worst drawdown of a year, and in 2022 it held up best of the six at 20.8%, although in the 2020 crash only IWM fell further. EEM had the worst year in 2019 and 2021, two years without a global crisis, which shows that emerging markets can draw down on their own schedule.

## One Day Turned the Skew of 2025 Positive

Crash years and slow bear markets leave different marks on the skew. Skewness measures whether the bad days or the good days are the more extreme: negative skew means a longer left tail, with rare but large losses, while positive skew means the largest moves were gains.

The sudden selloffs of 2019 and 2020 show as negative skew in every index, pink for negative and blue for positive:

{% capture code_skew %}
```python
# pip install financetoolkit
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["SPY", "QQQ", "DIA", "IWM", "EFA", "EEM"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2019-01-01", end_date="2025-12-31", benchmark_ticker=None)

skewness = toolkit.risk.get_skewness(period="yearly", within_period=True)
```
{% endcapture %}
{% include ft-chart.html id="risk-skew" src="/assets/data/article-charts.json" label="Skewness of daily returns" code=code_skew mcp="What was the skewness of the returns of SPY, QQQ, DIA, IWM, EFA and EEM within each calendar year from 2019 to 2025, and which years show the most negative skew?" %}

Those were the trade-war days of August 2019 and the COVID crash, and EFA and EEM were the most negative in 2020, at -1.21 and -1.24. In 2022 the skew turned slightly positive for five of the six. That bear market went down day after day without one big crash, even though every index fell between 20% and 35% from its peak.

In 2025 every index had positive skew, led by SPY at 1.51. That comes almost entirely from April 9 and its 10.5% jump. **Leave out that one day and SPY's skewness for 2025 becomes -1.51.** With one year of daily data, a single day can flip the sign, so a yearly skewness is best read next to the days behind it.

## Six Trading Days Pushed SPY's Kurtosis to 26.6

The April days show most clearly in the kurtosis. It measures how often extreme days happen, in either direction, compared with a bell curve, which has a kurtosis of 3.

The 2025 row, and SPY's cell in it, stands out from every other year:

{% capture code_kurtosis %}
```python
# pip install financetoolkit
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["SPY", "QQQ", "DIA", "IWM", "EFA", "EEM"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2019-01-01", end_date="2025-12-31", benchmark_ticker=None)

kurtosis = toolkit.risk.get_kurtosis(period="yearly", within_period=True)
volatility = toolkit.risk.get_volatility(period="yearly")
```
{% endcapture %}
{% include ft-chart.html id="risk-kurtosis" src="/assets/data/article-charts.json" label="Kurtosis of daily returns" code=code_kurtosis mcp="What was the kurtosis of the returns of SPY, QQQ, DIA, IWM, EFA and EEM within each calendar year from 2019 to 2025, and which year and index show the most extreme tails?" %}

SPY's 26.6 in 2025 is more than double the highest reading of any other year, EFA's 11.9 in 2020. QQQ and EFA were above 20 in 2025 as well. The only other year with high readings across the board is 2020, with four of the six indices above 10 during the COVID crash.

IWM's 2025 kurtosis of 8.9 was the lowest of the six. Small caps already move more on an ordinary day, so the April days stood out less against the rest of their year. For SPY, volatility (the annualised standard deviation of daily returns) and kurtosis rank the years quite differently:

| Year | SPY volatility | SPY kurtosis |
|---|---|---|
| 2022 | 24.2% | 3.4 |
| 2023 | 13.1% | 2.8 |
| 2025 | 19.5% | 26.6 |

**By volatility, 2025 was a calmer year for SPY than 2022, and by kurtosis it was the most extreme of the seven.** Volatility weighs every day of the year, while kurtosis weighs the largest moves most. Read next to the skewness chart, 2025 had its biggest move on the upside and its tails set by a handful of April days.

## At 99% Confidence the 2020 Gap Grows to 71%

Every figure so far rests on a few choices: a 95% confidence level, calendar-year windows, prices that include dividends and averages over seven years. Each of them can change the reading, starting with the confidence level. At 99% the CVaR is the average of the worst 1% of days, which is two or three days in a year.

At 99% the gap between historical and normal CVaR in 2020 more than doubles in every index, with one tab per index:

{% capture code_tail %}
```python
# pip install financetoolkit
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["SPY", "QQQ", "DIA", "IWM", "EFA", "EEM"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2019-01-01", end_date="2025-12-31", benchmark_ticker=None)

normal_cvar_95 = toolkit.risk.get_conditional_value_at_risk(period="yearly", within_period=True, distribution="gaussian")
historical_cvar_95 = toolkit.risk.get_conditional_value_at_risk(period="yearly", within_period=True)
normal_cvar_99 = toolkit.risk.get_conditional_value_at_risk(period="yearly", alpha=0.01, within_period=True, distribution="gaussian")
historical_cvar_99 = toolkit.risk.get_conditional_value_at_risk(period="yearly", alpha=0.01, within_period=True)

gap_95 = historical_cvar_95 / normal_cvar_95 - 1
gap_99 = historical_cvar_99 / normal_cvar_99 - 1

# The deepest fall over the whole period, which can span two calendar years
drawdown_series = toolkit.risk.get_drawdown_series(period="daily")
deepest_drawdown = drawdown_series.min()
deepest_date = drawdown_series.idxmin()

# Price returns leave out dividends, total returns (Adj Close) include them
historical = toolkit.get_historical_data()
price_returns = historical["Close"].pct_change().loc["2023"]
price_cvar_2023 = price_returns[price_returns <= price_returns.quantile(0.05)].mean()
ex_dividend_day = [price_returns.loc["2023-06-07", "EFA"], historical["Return"].loc["2023-06-07", "EFA"]]

# The yearly averages of the last section, without 2020
max_drawdown = toolkit.risk.get_maximum_drawdown(period="yearly", within_period=True)
average_drawdown_without_2020 = max_drawdown[max_drawdown.index.year != 2020].mean()
average_cvar_without_2020 = historical_cvar_95[historical_cvar_95.index.year != 2020].mean()
```
{% endcapture %}
{% include ft-chart.html id="risk-tail" src="/assets/data/article-charts.json" label="Historical CVaR beyond the normal CVaR at 95 and 99 percent confidence" code=code_tail mcp="For SPY, QQQ, DIA, IWM, EFA and EEM, how far did the historical Conditional Value at Risk go beyond the Conditional Value at Risk under a normal distribution within each calendar year from 2019 to 2025, at both the 95 and the 99 percent confidence level?" %}

At 95% SPY's worst days of 2020 were 28% worse than a normal distribution implied, which the first section rounds to about 30%. At 99% the gap is 71%, and no index is below 61%. **At 99% confidence the worst days of 2020 were 71% worse than volatility implied, so the 30% is the cautious figure.**

The year 2025 moves the most, from 12% to 58% for SPY, because its worst 1% are all April days. 2022 stays near or below zero at both levels, so the reading of that bear market as many bad days and few extreme ones holds. Each 99% figure rests on two or three days, which makes it far noisier than the 95% one, and that is why the yearly charts use 95%.

Calendar years can also cut a fall in two. EEM peaked in February 2021 and reached its low in October 2022, a fall of 39.8% that the drawdown chart splits into 16.6% in 2021 and 32.7% in 2022. Over the whole period only IWM's 41.1% in 2020 went deeper.

Prices without dividends add losses that never happened. EFA pays most of its dividend in June, and on June 7, 2023, its ex-dividend day, the price fell 2.7% while the total return was -0.9%. With that day and the December one counted as losses, EFA's 2023 historical CVaR becomes -1.87% on prices against -1.70% on total returns. All figures here use total returns, which matters most for EFA and EEM, the two funds where dividends add the most to the return.

One year also carries the averages in the next section. Without 2020, QQQ has the deepest average drawdown at 17.3% and the worst average CVaR at -2.91%, just ahead of IWM at 16.8% and -2.86%. IWM's place at the top of both columns comes from the COVID crash.

## What This Means for Portfolio Construction

Averaged over the yearly figures from 2019 to 2025, each measure ranks the indices differently:

| Index | Yearly maximum drawdown | Daily historical CVaR | Kurtosis |
|---|---|---|---|
| S&P 500 (SPY) | -15.3% | -2.69% | 8.3 |
| Nasdaq 100 (QQQ) | -18.9% | -3.28% | 7.0 |
| Dow Jones (DIA) | -14.4% | -2.55% | 7.4 |
| Russell 2000 (IWM) | -20.2% | -3.39% | 5.3 |
| MSCI EAFE (EFA) | -16.2% | -2.47% | 7.5 |
| Emerging Markets (EEM) | -19.2% | -2.84% | 6.3 |

With 2020 included, IWM had the deepest drawdowns and the worst CVaR, so by the usual loss measures it carried the most risk. It also had the lowest kurtosis, with or without 2025. Its risk is spread over many volatile days, which volatility and VaR already pick up. SPY is the other way around: one of the smaller drawdowns and the highest average kurtosis at 8.3, which is 5.2 without 2025, so more of its risk sat in a few days that volatility smooths over.

DIA had the smallest average drawdown at 14.4% and EFA the mildest CVaR, while EEM drew down in years without a US crisis. For diversification this means each index brings its own kind of risk to a portfolio, and one volatility figure per index hides which kind that is.

Besides volatility, I would watch how far the historical CVaR sits beyond the normal one, which grows when losses cluster in a few days, and the yearly kurtosis, which shows when a handful of days set the tail of a whole year. Each yearly figure rests on about 250 trading days, so a single day can move it, as April 9 showed. When both measures are high, as in 2020, a stress test built on that year's worst days says more than its standard deviation.

### Data and method

- **Source:** daily adjusted closing prices of the SPY, QQQ, DIA, IWM, EFA and EEM ETFs from FinancialModelingPrep, from January 2, 2019 to December 31, 2025.
- **How the series is built:** daily returns from adjusted closing prices, so dividends are included. The ETFs stand in for their indices and include their fund costs.
- **What I did to it:** the six ETFs share the New York trading calendar and have 1,760 trading days each with no gaps, so nothing was filled or dropped. Daily returns are the change in the adjusted close, so January 2, 2019 has no return and 2019 counts 251 returns. Each measure is computed within each calendar year: VaR and CVaR at 95% confidence, both historical and normal (a normal distribution with that year's mean and standard deviation), maximum drawdown from that year's prices, sample skewness and kurtosis (the Pearson definition, 3 for a normal distribution) and annualised volatility. The table in the last section averages the seven yearly figures. For the April 2025 comparisons I removed the named days from the 2025 returns and computed the measure again. The sensitivity check repeats the CVaR at 99% confidence, and the price comparison uses the unadjusted close.
- **Limits:** seven years, with 99% confidence only as a check. I left out the Cornish-Fisher VaR, which adjusts the normal VaR for skewness and kurtosis, because it breaks down at readings as extreme as 2025's: it gives SPY a smaller VaR for 2025 than for 2023. EFA and EEM trade in New York while their home markets close earlier, so part of a move can show up a day late in those two.
- **Reproduce it:** the charts are made with the [Finance Toolkit](/projects/financetoolkit), my open-source Python library, using its [risk module](/projects/financetoolkit/docs/risk) and prices from [FinancialModelingPrep](/fmp){:target="_blank"}. The Python button on each chart shows the code and its MCP button a question that returns the same data.
- **Further reading:** Philippe Artzner, Freddy Delbaen, Jean-Marc Eber and David Heath, "[Coherent Measures of Risk](https://people.math.ethz.ch/~delbaen/ftp/preprints/CoherentMF.pdf){:target="_blank"}" (Mathematical Finance, 1999), on why VaR can fail as a risk measure and what a sound one needs. R. Tyrrell Rockafellar and Stanislav Uryasev, "[Optimization of Conditional Value-at-Risk](https://sites.math.washington.edu/~rtr/papers/rtr179-CVaR1.pdf){:target="_blank"}" (Journal of Risk, 2000), which shows how to minimise the CVaR of a portfolio with linear programming. Basel Committee on Banking Supervision, "[Minimum capital requirements for market risk](https://www.bis.org/bcbs/publ/d457.htm){:target="_blank"}" (2019), the standard whose internal models approach for banks' market risk capital uses expected shortfall, the same measure as CVaR.

{% include ft-charts-script.html %}
