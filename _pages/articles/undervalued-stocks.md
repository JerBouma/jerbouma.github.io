---
title: How to Screen for Undervalued Stocks Without Value Traps
seo_title: "Screening for Undervalued Stocks and Value Traps"
date: 2026-06-14
last_modified_at: 2026-11-18
permalink: /articles/screening-undervalued-stocks-finance-toolkit
excerpt: "Merck traded at 14.5 times its fiscal 2025 earnings and Walmart at 40.8 times, yet Merck earned more on its capital. Screening 15 large caps on price first and quality second leaves three names that are both cheap and profitable."
description: "A two-pass stock screen of 15 large caps on P/E, EV/EBITDA, ROIC and gross margin in fiscal 2025 that separates cheap stocks from value traps."
layout: single
classes: wide-sidebar article-document
author_profile: false
collection: article
tags: [Fundamental Analysis]
share: true
cover:
  image: /assets/images/articles/undervalued-stocks/cover.jpg
  alt: "Three prospectors pan for gold beside a wooden sluice in a creek bed, 1889."
  credit: "Washing and panning gold, Rockerville, 1889, John Grabill, public domain"
  link: "https://commons.wikimedia.org/wiki/File:Grabill_-_Washing_and_panning_gold.jpg"
---

At the end of 2025, Merck traded at 14.5 times its fiscal 2025 earnings and Walmart at 40.8 times, which makes Merck the bargain on the multiple alone. Yet Merck also earned more on its capital, with a return on invested capital (ROIC) of 21.7% against 13.6% for Walmart.

So how do you tell a stock that is cheap from one that is cheap for a reason? In a screen of fifteen large caps, asking two valuation multiples to agree and then requiring an ROIC above 10% leaves three names: Merck, Johnson & Johnson and Pfizer. The second step matters because stocks often get cheap when investors expect earnings to fall, and a screen on price alone fills up with those value traps. The fifteen companies cover technology, healthcare, consumer staples, financials and energy, with ratios from their filings and share prices for fiscal 2025. The result is a watchlist for further research, and none of it is investment advice.

## The Multiples Run From 14 to 41 Times Earnings

The first pass uses four valuation ratios. The price-to-earnings ratio (P/E) divides the share price by earnings per share. EV/EBITDA divides enterprise value, which is market cap plus net debt, by operating earnings before depreciation and amortisation, so it compares companies however they are financed. Price to free cash flow (P/FCF) and price to book (P/B) are cross-checks that accounting choices move less easily.

The four ratios for all fifteen companies in fiscal 2025, sorted by P/E:

| Ticker | P/E | P/FCF | P/B | EV/EBITDA |
|--------|----:|------:|----:|----------:|
| INTC | -626.1 | -33.8 | 1.5 | 19.8 |
| BAC | 14.3 | 32.9 | 1.5 | -3.9 |
| MRK | 14.5 | 21.4 | 5.0 | 10.2 |
| JPM | 16.1 | -6.1 | 2.6 | 4.7 |
| XOM | 18.0 | 21.9 | 2.0 | 9.3 |
| PFE | 18.2 | 15.6 | 1.6 | 8.2 |
| JNJ | 18.8 | 25.5 | 6.2 | 16.0 |
| CVX | 23.0 | 17.0 | 1.5 | 8.8 |
| KO | 23.0 | 56.9 | 9.4 | 22.7 |
| IBM | 26.5 | 23.2 | 8.6 | 19.1 |
| META | 28.1 | 36.8 | 7.8 | 16.7 |
| GOOGL | 29.0 | 52.2 | 9.2 | 25.0 |
| MSFT | 35.5 | 50.4 | 10.5 | 22.3 |
| AAPL | 36.4 | 41.3 | 55.3 | 28.6 |
| WMT | 40.8 | 59.9 | 9.0 | 21.7 |

Bank of America and Merck are the cheapest on earnings at about 14 times, and Walmart the most expensive at about 41. Intel tops the sort only because a small net loss turns its P/E negative, at -626.1, a number that means nothing. Bank of America's EV/EBITDA is negative for another reason: the cash on its balance sheet is larger than its market cap plus debt, so its enterprise value drops below zero. **Sorted on one multiple, the list starts with a loss-maker and a bank with a negative enterprise value.**

The cross-checks add their own warnings. Coca-Cola trades at 56.9 times free cash flow on a P/E of 23.0, which means much of its profit goes into capital spending and working capital before it becomes free cash flow. Next to that, Apple's price to book of 55.3 reflects years of buybacks that left it with little book equity, a reminder that P/B works best for asset-heavy businesses such as banks and energy companies. JPMorgan's negative P/FCF says more about how a bank's cash flow moves with its loan book and trading positions than about its value.

## Five Stocks Pass When Two Multiples Must Agree

One multiple is easy to distort through a one-time charge or an unusual capital structure. The filter therefore asks for two at the same time: a P/E below 20 and an EV/EBITDA below 18, with negative values left out.

The two multiples plotted against each other, with the thresholds as dashed lines:

{% capture code_screen_valuation %}
```python
# pip install financetoolkit
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT", "INTC", "IBM", "JNJ", "PFE", "MRK", "KO", "WMT", "JPM", "BAC", "XOM", "CVX", "META", "GOOGL"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2022-01-01")

pe = toolkit.ratios.get_price_to_earnings_ratio()["2025"]
ev_ebitda = toolkit.ratios.get_ev_to_ebitda_ratio()["2025"]
```
{% endcapture %}
{% include ft-chart.html id="screen-valuation" src="/assets/data/article-charts.json" label="P/E against EV/EBITDA for 14 large caps, fiscal 2025" code=code_screen_valuation mcp="What were the P/E ratio and the EV/EBITDA of AAPL, MSFT, INTC, IBM, JNJ, PFE, MRK, KO, WMT, JPM, BAC, XOM, CVX, META and GOOGL in fiscal 2025, and which of them were below 20 times earnings and 18 times EBITDA at the same time, leaving out negative ratios?" %}

Five stocks land in the cheap corner: Merck, JPMorgan, Exxon Mobil, Pfizer and Johnson & Johnson. Bank of America clears the P/E filter but drops out on its negative EV/EBITDA. Chevron misses the other way, at 8.8 times EBITDA but 23.0 times earnings after its 2025 profit fell.

**EV/EBITDA is a poor fit for the two banks.** Deposits and debt are what a bank works with, so enterprise value and operating earnings don't mean what they mean for an industrial company. JPMorgan passes on paper at 4.7 times EBITDA and Bank of America fails on a negative enterprise value, and both deserve a separate look with bank measures such as price to tangible book and return on equity.

## Three of the Five Earn More Than 10% on Their Capital

A low multiple is only interesting when the business behind it holds up, and three profitability ratios test that. Return on equity (ROE) is net income over average shareholders' equity. [Return on invested capital](/projects/financetoolkit/docs/ratios/return-on-invested-capital-roic) is net operating profit after tax (NOPAT) over the average of debt plus equity, so it measures the return on all the capital a business uses, however it is financed. The gross margin is the share of sales left after the direct cost of producing them, a rough measure of pricing power.

A value trap usually shows up as a falling trend before it shows up in a single year. The three ratios for the five candidates in fiscal 2025, with their ROIC since 2022 in the second tab:

{% capture code_screen_quality %}
```python
# pip install financetoolkit
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["MRK", "JNJ", "PFE", "XOM", "JPM"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2022-01-01")

roe = toolkit.ratios.get_return_on_equity()["2025"]
roic = toolkit.ratios.get_return_on_invested_capital().loc[:, :"2025"]
gross_margin = toolkit.ratios.get_gross_margin()["2025"]
```
{% endcapture %}
{% include ft-chart.html id="screen-quality" src="/assets/data/article-charts.json" label="Return on equity, ROIC and gross margin of the five value candidates" code=code_screen_quality mcp="Show the fiscal 2025 return on equity, return on invested capital and gross margin of MRK, JNJ, PFE, XOM and JPM, and their return on invested capital for every fiscal year from 2022 to 2025." %}

Three of the five earn more than 10% on invested capital. Merck and Johnson & Johnson lead at 21.7% and 17.7%, and keep about 70% of sales as gross profit. Their low multiples most likely reflect the patent expiry ahead for Merck's cancer drug Keytruda and the litigation Johnson & Johnson faces, and so far neither shows up in their returns. That is my reading, since the ratios show the gap between price and return and say nothing about its cause. Merck's dip in 2023 came from a one-off charge for research it bought with an acquisition, and by 2024 its ROIC was back where it had been.

Pfizer is where the trend matters most. Its ROIC fell from 28.1% in 2022 to 3.0% in 2023 once COVID vaccine revenue ran off, and has recovered to 11.2% since. Its gross margin of 74.3%, the highest of the five, says the drug business still has pricing power. However, **a low multiple on earnings that have already reset is a different thing from a low multiple on earnings that are intact.**

Exxon Mobil's ROIC fell every year, from 20.3% in 2022 to 7.9% in 2025, as oil and gas prices came down from their 2022 peak. JPMorgan earns 4.8% on invested capital, which would rule out an industrial company. For a bank funded mostly by deposits, its ROE of 15.8% is the more relevant measure, and judging it needs the bank measures this screen doesn't use.

## The Shortlist Trades at Half the Multiple of Other Quality Stocks

The last step keeps the candidates with an ROIC above 10%. The level is a judgment call. It roughly separates businesses that earn well above a typical cost of capital from those that don't.

The candidates that earn more than 10% on invested capital, sorted by ROIC:

| Ticker | ROE | ROIC | Gross Margin |
|--------|----:|-----:|-------------:|
| MRK | 36.9% | 21.7% | 72.0% |
| JNJ | 35.0% | 17.7% | 67.9% |
| PFE | 8.9% | 11.2% | 74.3% |

A hard cutoff decides a lot here. Pfizer passes at 11.2% but would have missed a year earlier at 9.5%, and Exxon Mobil misses at 7.9% but would just have passed in 2024 at 10.0%.

All fifteen stocks on a map of return on capital against the EBITDA multiple:

{% capture code_screen_final %}
```python
# pip install financetoolkit
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT", "INTC", "IBM", "JNJ", "PFE", "MRK", "KO", "WMT", "JPM", "BAC", "XOM", "CVX", "META", "GOOGL"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2022-01-01")

roic_history = toolkit.ratios.get_return_on_invested_capital()
roic = roic_history["2025"]
ev_ebitda = toolkit.ratios.get_ev_to_ebitda_ratio()["2025"]

# sensitivity check: move each threshold one notch, or average ROIC over three years
pe = toolkit.ratios.get_price_to_earnings_ratio()["2025"]
roic_average = roic_history.loc[:, "2023":"2025"].mean(axis=1)


def shortlist(max_pe=20, max_ev_ebitda=18, min_roic=0.10, returns=roic):
    cheap = (pe > 0) & (pe < max_pe) & (ev_ebitda > 0) & (ev_ebitda < max_ev_ebitda)
    return list(returns[cheap & (returns > min_roic)].sort_values(ascending=False).index)


variants = {
    "Base case": shortlist(),
    "P/E below 18": shortlist(max_pe=18),
    "P/E below 22": shortlist(max_pe=22),
    "EV/EBITDA below 16": shortlist(max_ev_ebitda=16),
    "EV/EBITDA below 20": shortlist(max_ev_ebitda=20),
    "ROIC above 8%": shortlist(min_roic=0.08),
    "ROIC above 12%": shortlist(min_roic=0.12),
    "Three-year average ROIC": shortlist(returns=roic_average),
}
```
{% endcapture %}
{% include ft-chart.html id="screen-final" src="/assets/data/article-charts.json" label="ROIC against EV/EBITDA for all 15 stocks, fiscal 2025" code=code_screen_final mcp="Compare the fiscal 2025 return on invested capital and EV/EBITDA of AAPL, MSFT, INTC, IBM, JNJ, PFE, MRK, KO, WMT, JPM, BAC, XOM, CVX, META and GOOGL. Which ones earn more than 10 percent on invested capital while trading below 20 times earnings and 18 times EBITDA?" %}

High returns are easy to find in this group: most of the fifteen clear the threshold. The seven that aren't on the shortlist, from Apple to Meta, trade at a median of 22.3 times EBITDA, against 10.2 for Merck, Johnson & Johnson and Pfizer. **The shortlist trades at about half the EBITDA multiple of the other high-return stocks.**

Meta is the closest call. At 16.7 times EBITDA it sits in the same corner as the shortlist, but its P/E of 28.1 kept it out of the first pass. Chevron and Exxon Mobil are about as cheap as Pfizer on EBITDA, but earn 5.1% and 7.9% on their capital.

## One Notch on the P/E Line Leaves Only Merck

The three cutoffs are round numbers I picked, and the shortlist leans on them more than the charts suggest. Johnson & Johnson and Pfizer trade at 18.8 and 18.2 times earnings, just under the line of 20. The shortlist when each threshold moves one notch either way, or when the 2025 ROIC is replaced by its average over 2023 to 2025:

| Variant | Shortlist | Change |
|---------|-----------|--------|
| Base case: P/E 20, EV/EBITDA 18, ROIC 10% | MRK, JNJ, PFE | |
| P/E below 18 | MRK | JNJ and PFE drop |
| P/E below 22 | MRK, JNJ, PFE | None |
| EV/EBITDA below 16 | MRK, PFE | JNJ drops |
| EV/EBITDA below 20 | MRK, JNJ, PFE | None |
| ROIC above 8% | MRK, JNJ, PFE | None |
| ROIC above 12% | MRK, JNJ | PFE drops |
| Three-year average ROIC | JNJ, MRK, XOM | PFE drops, XOM joins |

Loosening a cutoff adds nobody, because the next names out fail on another measure. Chevron is cheap on EBITDA but trades at 23.0 times earnings, IBM would pass a looser EV/EBITDA limit but trades at 26.5 times earnings, and Exxon Mobil stays just under an 8% ROIC floor at 7.9%.

Tightening by the same notch takes at least one name off every time. With a P/E limit of 18 only Merck is left, an EV/EBITDA limit of 16 drops Johnson & Johnson at 16.0, and an ROIC floor of 12% drops Pfizer. **Merck is the only name that passes in every variant.**

Using a single year also means the screen sees only the end of each trend. On ROIC averaged over 2023 to 2025, Pfizer drops out at 7.9% because its 2023 collapse is still in the average, and Exxon Mobil comes in at 10.2% on the strength of its earlier years. Merck stays in at 14.8%, even with its 2023 charge included. Which version is right depends on whether you see the bad year as a one-off, and the screen can't decide that for you.

Next to that, the universe is small and picked by hand. With fifteen names, a single company can move the medians in the previous section, and in a wider universe more stocks would sit close to each cutoff. The fiscal years also end in different months. Every multiple uses the share price of 31 December 2025, so Microsoft's P/E sets that price against earnings for a year that ended in June, and Walmart's against a year that ended a month after it, in January 2026.

## What This Means for a Value Watchlist

The screen took fifteen stocks down to three, and the reasons the others dropped out are as useful as the result: Intel on collapsed earnings, Chevron and Exxon Mobil on falling profits and returns as commodity prices normalised, the banks on metrics that don't fit them, and most of technology and consumer staples on price.

A single year can't show whether a low multiple is new or normal for the company. The EBITDA multiple and ROIC of each name on the watchlist since 2022:

| | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|
| **Merck**, EV/EBITDA | 13.6x | 45.0x | 11.2x | 10.2x |
| Merck, ROIC | 21.4% | 0.8% | 21.9% | 21.7% |
| **Johnson & Johnson**, EV/EBITDA | 17.4x | 13.2x | 12.3x | 16.0x |
| Johnson & Johnson, ROIC | 15.9% | 19.3% | 18.1% | 17.7% |
| **Pfizer**, EV/EBITDA | 7.1x | 20.8x | 9.0x | 8.2x |
| Pfizer, ROIC | 28.1% | 3.0% | 9.5% | 11.2% |

Merck's 10.2 times EBITDA in 2025 is the lowest of its four years, while its ROIC held at about 22% outside the 2023 charge, so the gap between price and return has widened. Johnson & Johnson went the other way: its multiple rose from 12.3 to 16.0 in 2025 on a steady return, which means it was cheaper on this measure a year earlier.

Pfizer traded at about the same EBITDA multiple in 2025 as in 2022, 8.2 against 7.1, on an ROIC that fell from 28.1% to 11.2%. Its enterprise value fell along with its EBITDA, so on its own history it is no cheaper than in 2022, when it earned far more on its capital.

The screen can't tell you whether the market's reasons for the low multiples are right. Merck's trailing ROIC says nothing about revenue after Keytruda loses patent protection, Johnson & Johnson's nothing about the outcome of its litigation, and Pfizer's nothing about whether its recovery continues. Those need work on pipelines, debt maturities and capital allocation, and the previous section shows how much the thresholds themselves decide.

The two series in the watchlist table are the ones to follow for each name: whether the return on capital holds as the patent and litigation questions play out, and whether the multiple moves with it. What the screen does well is take twelve names off the desk quickly, for reasons you can check, so the research time goes to the three where price and quality point the same way. It illustrates a method and is not investment advice.

### Data and method

**Source.** Annual financial statements of fifteen US large caps from company filings via FinancialModelingPrep, and their share prices from FinancialModelingPrep, fiscal years 2022 to 2025, retrieved on November 17, 2026.

**How the series is built.** Each ratio uses the fiscal year as the company reports it, and fiscal years don't line up: Microsoft's 2025 ends in June, Apple's in September and Walmart's in January 2026. Fiscal 2025 is the latest year all fifteen have reported. The share price in every multiple is the close of 31 December 2025.

**What I did to it.** ROIC is operating income taxed at the effective tax rate (NOPAT), over the average of total debt plus total equity. ROE is net income over average equity. The screen keeps the stocks with a positive P/E below 20 and a positive EV/EBITDA below 18, and of those the ones with an ROIC above 10%. Negative multiples (Intel's P/E, Bank of America's EV/EBITDA) are dropped from the filter instead of counted as cheap, and Intel is left out of the first chart, where its negative P/E would squash the axis. Walmart's year to January 2026 counts as its fiscal 2025, and the fiscal 2026 figures Microsoft and Apple have already reported are left out, so all fifteen compare on the same year. The 2023 charges of Merck and Pfizer stay in, without adjustment. The medians in the fourth section are of the seven stocks with an ROIC above 10% that are not on the shortlist, and of the shortlist itself. The sensitivity table moves one threshold at a time and keeps the other two at their base level. Its three-year ROIC is the plain average of 2023, 2024 and 2025, and its code sits under the Python button of the ROIC against EV/EBITDA chart. The last table shows EV/EBITDA and not P/E, because the 2023 charges pushed the P/E of Merck into the hundreds and that of Pfizer into the seventies.

**Limits.** The screen uses trailing ratios for a single year, which can't see the earnings ahead. Fifteen names are enough to show the logic, but a real screen would cast a wider net. Other data providers define some of these ratios differently, and their numbers can differ from the ones here.

**Reproduce it.** The charts and tables are made with the [Finance Toolkit](/projects/financetoolkit), my open-source Python library. The Python button on each chart shows the code, and its MCP button a question that returns the same data from the [MCP server](/projects/financetoolkit/mcp). The code needs an FMP API key, which you can get at [jeroenbouma.com/fmp](/fmp){:target="_blank"}. The [Discovery module](/projects/financetoolkit/docs/discovery) can build a wider universe to screen.

**Further reading.** Robert Novy-Marx (2013), The Other Side of Value: The Gross Profitability Premium, Journal of Financial Economics ([working paper](https://www.nber.org/papers/w15940){:target="_blank"}), which finds that gross profits over assets predict returns about as well as book to market, and that adding profitability improves a value strategy. Clifford Asness, Andrea Frazzini and Lasse Heje Pedersen (2019), [Quality Minus Junk](https://link.springer.com/article/10.1007/s11142-018-9470-2){:target="_blank"}, Review of Accounting Studies, which finds that the market pays more for profitable, safe and growing companies, but not by a large margin.

{% include ft-charts-script.html %}
