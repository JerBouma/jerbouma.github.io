---
title: Screening for Undervalued Stocks with the Finance Toolkit
seo_title: "Screening for Undervalued Stocks in Python"
date: 2026-06-14
last_modified_at: 2026-11-17
permalink: /articles/screening-undervalued-stocks-finance-toolkit
excerpt: "Merck traded at 14 times its fiscal 2025 earnings and Walmart at 41 times, yet Merck earned more on its capital. A two-pass screen of 15 large caps, valuation first and quality second, shows how to separate cheap from merely low-priced."
description: "A stock screen in Python on P/E, EV/EBITDA, ROIC and gross margins across 15 large caps, separating real value from value traps with the Finance Toolkit."
layout: single
classes: wide-sidebar article-document
author_profile: false
collection: article
tags: [Fundamental Analysis]
share: true
---

At the end of their 2025 fiscal years, Merck traded at 14.2 times earnings and Walmart at 40.6 times. On the multiple alone, Merck is the bargain and Walmart the expensive one. Yet Merck also earned more on its capital: a return on invested capital of 19.4%, against 13.2% for Walmart. A low multiple and a strong business at the same time is what a value screen is looking for, and it is rarer than either on its own.

The difficulty is that a low multiple is just as often a warning. Stocks get cheap because investors expect earnings to fall, the balance sheet to strain or the industry to shrink, the classic value trap. In this article I build a two-pass screen on 15 large caps across technology, healthcare, consumer staples, financials and energy: valuation multiples first, then profitability to test whether the low price is deserved. It ends with a watchlist of two names, and with the reasons the other thirteen dropped out. A real screen would cast a wider net, which the [Discovery module](/projects/financetoolkit/docs/discovery) supports, but fifteen names are enough to show the logic.

The data comes from the [Finance Toolkit](https://github.com/JerBouma/FinanceToolkit){:target="_blank"}, and every chart has a Python button with the code behind it and an MCP button with a question that gets the same data from the [Finance Toolkit MCP server](/projects/financetoolkit/mcp). Everything uses fiscal year 2025, the latest year all fifteen companies have reported, with data retrieved on October 14, 2026. Fiscal years don't line up: Microsoft's 2025 ends in June, Apple's in September and Walmart's in January 2026. The code needs an FMP API key, which you can get at [jeroenbouma.com/fmp](/fmp){:target="_blank"}.

## The Valuation Map: Five Stocks Are Cheap on Two Measures

The first pass uses four [valuation ratios](/projects/financetoolkit/docs/ratios). P/E (price over earnings per share) and EV/EBITDA (enterprise value, so equity plus net debt, over operating earnings before depreciation) are the usual entry points. Price to free cash flow and price to book are cross-checks that accounting choices move less easily.

The four ratios for all fifteen companies in fiscal 2025, sorted by P/E:

| Ticker | P/E | P/FCF | P/B | EV/EBITDA |
|--------|----:|------:|----:|----------:|
| INTC | -670.9 | -36.2 | 1.6 | 23.6 |
| BAC | 14.1 | 32.4 | 1.5 | 14.2 |
| MRK | 14.2 | 20.9 | 4.9 | 10.0 |
| JPM | 15.9 | -6.0 | 2.6 | 18.5 |
| PFE | 17.4 | 14.8 | 1.6 | 9.1 |
| XOM | 17.6 | 21.5 | 2.0 | 9.1 |
| JNJ | 18.5 | 25.1 | 6.1 | 15.8 |
| CVX | 22.4 | 16.6 | 1.5 | 8.6 |
| KO | 22.6 | 55.9 | 9.2 | 22.6 |
| IBM | 26.0 | 22.8 | 8.4 | 18.8 |
| META | 28.0 | 36.8 | 7.8 | 17.1 |
| GOOGL | 28.9 | 52.1 | 9.2 | 25.6 |
| MSFT | 35.2 | 50.1 | 10.4 | 22.6 |
| AAPL | 36.3 | 41.2 | 55.2 | 28.6 |
| WMT | 40.6 | 59.5 | 8.9 | 21.6 |

The spread is wide: Bank of America and Merck trade at about 14 times earnings, Walmart at 40.6. Intel sorts to the top only because its P/E is negative: a net loss so small that the ratio runs to -670.9, which means nothing. That is why sorting on a single metric misleads without further filters.

The cross-checks add their own warnings. Coca-Cola trades at 55.9 times free cash flow on a P/E of 22.6, a gap that points at cash going into capital spending and working capital rather than into free cash flow. Apple's price to book of 55.2 reflects years of buybacks that left it with little book equity, a reminder that P/B works best for asset-heavy businesses such as banks and energy companies. And JPMorgan's negative P/FCF says more about how a bank's cash flow statement moves with its loan book and trading positions than about its value.

Plotting the two main multiples against each other shows where the cheap corner is:

{% capture code_screen_valuation %}
```python
# pip install financetoolkit
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT", "INTC", "IBM", "JNJ", "PFE", "MRK", "KO", "WMT", "JPM", "BAC", "XOM", "CVX", "META", "GOOGL"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2022-01-01")

pe = toolkit.ratios.get_price_to_earnings_ratio()["2025"]
ev_ebitda = toolkit.ratios.get_ev_to_ebitda_ratio()["2025"]
```
{% endcapture %}
{% include ft-chart.html id="screen-valuation" src="/assets/data/article-charts.json" label="P/E against EV/EBITDA for 14 large caps, fiscal 2025" code=code_screen_valuation mcp="What were the P/E ratio and the EV/EBITDA of AAPL, MSFT, INTC, IBM, JNJ, PFE, MRK, KO, WMT, JPM, BAC, XOM, CVX, META and GOOGL in fiscal 2025, and which of them were below 20 times earnings and 18 times EBITDA at the same time?" %}

## The Filter: Requiring Two Multiples to Agree

A single multiple is easy to distort through one-time charges, accounting choices or an unusual capital structure. The filter therefore requires two to pass at the same time: a P/E below 20 and an EV/EBITDA below 18, with negative earners excluded. The dashed lines in the chart above are these thresholds.

Five stocks pass both filters: Bank of America, Merck, Pfizer, Exxon Mobil and Johnson & Johnson. The near misses are as informative as the passes. JPMorgan clears the P/E filter but misses on EV/EBITDA at 18.5, just above the threshold. Chevron is the mirror image: the lowest EV/EBITDA of the fifteen at 8.6, but a P/E of 22.4 after its 2025 earnings fell.

**For the two banks, EV/EBITDA is a poor fit**: deposits and debt are their raw material rather than their financing, so enterprise value and operating earnings don't mean what they mean for an industrial company. Bank of America passes on paper, and JPMorgan deserves a separate look with bank-specific measures such as price to tangible book and return on equity.

## The Quality Test: Which Low Multiples Are Deserved?

A low valuation doesn't make a stock undervalued. Before any of the five goes on a watchlist, its profitability has to hold up. Three [profitability ratios](/projects/financetoolkit/docs/ratios) do most of the work. Return on equity (ROE) is net income over average shareholders' equity. Return on invested capital (ROIC) here is net income over the average of debt plus equity, so it measures the return on all the capital the business uses, regardless of how it is financed. The gross margin shows how much of each dollar of sales is left after the direct cost of producing it, a rough measure of pricing power.

I use ROIC without subtracting dividends from net income. With dividends subtracted it measures what the company reinvests, and that would penalise exactly the steady dividend payers a value screen tends to find. The second tab adds the same ROIC from 2022 on, because a value trap is usually a trend before it shows up in a single year.

The three ratios for the five candidates, and their ROIC since 2022:

{% capture code_screen_quality %}
```python
# pip install financetoolkit
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["JNJ", "MRK", "XOM", "PFE", "BAC"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2022-01-01")

roe = toolkit.ratios.get_return_on_equity()["2025"]
roic = toolkit.ratios.get_return_on_invested_capital()
gross_margin = toolkit.ratios.get_gross_margin()["2025"]
```
{% endcapture %}
{% include ft-chart.html id="screen-quality" src="/assets/data/article-charts.json" label="Return on equity, ROIC and gross margin of the five value candidates" code=code_screen_quality mcp="Show the fiscal 2025 return on equity, return on invested capital and gross margin of JNJ, MRK, XOM, PFE and BAC, and their return on invested capital for every fiscal year from 2022 to 2025." %}

The candidates split into two groups. Johnson & Johnson and Merck earn 22.6% and 19.4% on invested capital with gross margins of 67.9% and 72.0%. Their low multiples reflect pressure across pharmaceuticals, with Merck's Keytruda patent expiry ahead and Johnson & Johnson's litigation, rather than a weakening business. Merck's dip to 0.5% in 2023 was a one-off: a large acquisition charge for research in progress, after which ROIC was back above 21% the following year.

Exxon Mobil and Pfizer are the opposite story when you look at the trend. Exxon's ROIC fell every year, from 23.9% in 2022 to 9.3% in 2025, as oil and gas prices came down from their 2022 peak; its gross margin of 21.7% reflects the commodity economics of refining and distribution. Pfizer's ROIC collapsed from 25.6% in 2022 to 1.5% in 2023 once COVID vaccine revenue ran off, and has stayed around 5% since. A gross margin of 70.3% says the underlying drug business still has pricing power, but **a low multiple on earnings that have already reset is not the same as a low multiple on earnings that are intact**.

Bank of America earns 3.6% on invested capital, which would disqualify an industrial company. For a bank funded largely by deposits, ROE of 9.7% is the more relevant measure, and it suggests the market's discount is fair rather than an obvious bargain.

## The Shortlist: Where Quality Comes Cheap

The final step applies a quality threshold: an ROIC above 10%. The level is a judgment call; it roughly separates businesses that earn well above a typical cost of capital from those that don't.

The candidates that earn more than 10% on invested capital, sorted by ROIC:

| Ticker | ROE | ROIC | Gross Margin |
|--------|----:|-----:|-------------:|
| JNJ | 35.0% | 22.6% | 67.9% |
| MRK | 36.9% | 19.4% | 72.0% |

Two names remain. Exxon Mobil misses at 9.3%, which shows how much a hard cutoff decides: a year earlier it would have passed. Pfizer and Bank of America fall away clearly.

Placing all fifteen stocks on a map of quality against price shows what the screen does:

{% capture code_screen_final %}
```python
# pip install financetoolkit
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["AAPL", "MSFT", "INTC", "IBM", "JNJ", "PFE", "MRK", "KO", "WMT", "JPM", "BAC", "XOM", "CVX", "META", "GOOGL"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2022-01-01")

roic = toolkit.ratios.get_return_on_invested_capital()["2025"]
ev_ebitda = toolkit.ratios.get_ev_to_ebitda_ratio()["2025"]
```
{% endcapture %}
{% include ft-chart.html id="screen-final" src="/assets/data/article-charts.json" label="ROIC against EV/EBITDA for all 15 stocks, fiscal 2025" code=code_screen_final mcp="Compare the fiscal 2025 return on invested capital and EV/EBITDA of AAPL, MSFT, INTC, IBM, JNJ, PFE, MRK, KO, WMT, JPM, BAC, XOM, CVX, META and GOOGL. Which ones earn more than 10 percent on invested capital at less than 18 times EBITDA?" %}

Quality is not scarce in this universe. Apple (61.9%), Alphabet (32.0%), Microsoft (24.8%), Meta (22.7%) and Coca-Cola (17.1%) all earn more on their capital than the 10% threshold, but at 17 to 29 times EBITDA. Johnson & Johnson and Merck are the two that combine an ROIC near 20% with EV/EBITDA of 15.8 and 10.0. In the bottom left, Pfizer, Chevron and Exxon Mobil are cheaper still, at 8.6 to 9.1 times EBITDA, but earn 5.0% to 9.3% on their capital.

## Conclusion: A Watchlist, Not a Buy List

The screen reduced fifteen stocks to two, and the reasons the others dropped out are as useful as the result: Intel and Pfizer on earnings that have collapsed or reset, Chevron and Exxon Mobil on falling returns as commodity prices normalised, the banks on metrics that don't fit them, and most of technology and consumer staples on price rather than quality.

What the screen can't tell you is whether the market's reasons for the low multiples are right. Merck's trailing ROIC says nothing about revenue after Keytruda loses patent protection, and Johnson & Johnson's says nothing about the outcome of its litigation. Those need analysis the Toolkit can support but not automate: pipelines, debt maturities, capital allocation and the catalysts in the next few quarters. The thresholds are also choices: an ROIC limit of 9% instead of 10% would have kept Exxon Mobil on the list.

The output of this screen is a watchlist rather than a buy list. What it does well is take thirteen names off the desk quickly, for reasons you can check, so the time goes to the two where price and quality point the same way. This is an illustration of a method, not investment advice.

{% include ft-charts-script.html %}
