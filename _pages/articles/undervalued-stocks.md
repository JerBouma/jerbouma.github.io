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

At the end of their 2025 fiscal years, Merck traded at 14.5 times earnings and Walmart at 40.8 times. On the multiple alone, Merck is the bargain and Walmart the expensive one. Yet Merck also earned more on its capital: a return on invested capital of 21.7%, against 13.6% for Walmart. A low multiple and a strong business at the same time is what a value screen is looking for, and it is rarer than either on its own.

The difficulty is that a low multiple is just as often a warning. Stocks get cheap because investors expect earnings to fall, the balance sheet to strain or the industry to shrink, the classic value trap. In this article I build a two-pass screen on 15 large caps across technology, healthcare, consumer staples, financials and energy: valuation multiples first, then profitability to test whether the low price is deserved. It ends with a watchlist of three names, and with the reasons the other twelve dropped out. A real screen would cast a wider net, which the [Discovery module](/projects/financetoolkit/docs/discovery) supports, but fifteen names are enough to show the logic.

The data comes from the [Finance Toolkit](https://github.com/JerBouma/FinanceToolkit){:target="_blank"}, and every chart has a Python button with the code behind it and an MCP button with a question that gets the same data from the [Finance Toolkit MCP server](/projects/financetoolkit/mcp). Everything uses fiscal year 2025, the latest year all fifteen companies have reported, with data retrieved on November 17, 2026. Fiscal years don't line up: Microsoft's 2025 ends in June, Apple's in September and Walmart's in January 2026. The code needs an FMP API key, which you can get at [jeroenbouma.com/fmp](/fmp){:target="_blank"}.

## The Valuation Map: Five Stocks Are Cheap on Two Measures

The first pass uses four [valuation ratios](/projects/financetoolkit/docs/ratios). P/E (price over earnings per share) and EV/EBITDA (enterprise value, so equity plus net debt, over operating earnings before depreciation) are the usual entry points. Price to free cash flow and price to book are cross-checks that accounting choices move less easily.

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

The spread is wide: Bank of America and Merck trade at 14.3 and 14.5 times earnings, Walmart at 40.8. Intel sorts to the top only because its P/E is negative: a net loss so small that the ratio runs to -626.1, which means nothing. Bank of America has a negative EV/EBITDA of -3.9 for a similar reason: its enterprise value comes out at about -$157 billion, because the cash on its balance sheet is larger than its market cap plus debt. That is why sorting on a single metric misleads without further filters.

The cross-checks add their own warnings. Coca-Cola trades at 56.9 times free cash flow on a P/E of 23.0, a gap that points at cash going into capital spending and working capital rather than into free cash flow. Apple's price to book of 55.3 reflects years of buybacks that left it with little book equity, a reminder that P/B works best for asset-heavy businesses such as banks and energy companies. And JPMorgan's negative P/FCF says more about how a bank's cash flow statement moves with its loan book and trading positions than about its value.

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
{% include ft-chart.html id="screen-valuation" src="/assets/data/article-charts.json" label="P/E against EV/EBITDA for 14 large caps, fiscal 2025" code=code_screen_valuation mcp="What were the P/E ratio and the EV/EBITDA of AAPL, MSFT, INTC, IBM, JNJ, PFE, MRK, KO, WMT, JPM, BAC, XOM, CVX, META and GOOGL in fiscal 2025, and which of them were below 20 times earnings and 18 times EBITDA at the same time, leaving out negative ratios?" %}

## The Filter: Requiring Two Multiples to Agree

A single multiple is easy to distort through one-time charges, accounting choices or an unusual capital structure. The filter therefore requires two to pass at the same time: a P/E below 20 and an EV/EBITDA below 18, with negative earners excluded. The dashed lines in the chart above are these thresholds.

Five stocks pass both filters: Merck, JPMorgan, Exxon Mobil, Pfizer and Johnson & Johnson. The near misses tell you as much as the passes. Bank of America clears the P/E filter at 14.3, but its negative EV/EBITDA takes it out. Chevron misses the other way: 8.8 times EBITDA, one of the lowest of the fifteen, but a P/E of 23.0 after its 2025 earnings fell.

**For the two banks, EV/EBITDA is a poor fit**: deposits and debt are their raw material rather than their financing, so enterprise value and operating earnings don't mean what they mean for an industrial company. JPMorgan passes on paper at 4.7 times EBITDA, Bank of America drops out on a negative enterprise value, and both deserve a separate look with bank-specific measures such as price to tangible book and return on equity.

## The Quality Test: Which Low Multiples Are Deserved?

A low valuation doesn't make a stock undervalued. Before any of the five goes on a watchlist, its profitability has to hold up. Three [profitability ratios](/projects/financetoolkit/docs/ratios) do most of the work. Return on equity (ROE) is net income over average shareholders' equity. Return on invested capital (ROIC) is net operating profit after tax (NOPAT) over the average of debt plus equity, so it measures the return on all the capital the business uses, regardless of how it is financed. The gross margin shows how much of each dollar of sales is left after the direct cost of producing it, a rough measure of pricing power.

Because it starts from operating profit, ROIC isn't moved by how much interest a company pays or how much it pays out in dividends. The second tab adds the same ROIC from 2022 on, because a value trap is usually a trend before it shows up in a single year.

The three ratios for the five candidates, and their ROIC since 2022:

{% capture code_screen_quality %}
```python
# pip install financetoolkit
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["MRK", "JNJ", "PFE", "XOM", "JPM"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2022-01-01")

roe = toolkit.ratios.get_return_on_equity()["2025"]
roic = toolkit.ratios.get_return_on_invested_capital()
gross_margin = toolkit.ratios.get_gross_margin()["2025"]
```
{% endcapture %}
{% include ft-chart.html id="screen-quality" src="/assets/data/article-charts.json" label="Return on equity, ROIC and gross margin of the five value candidates" code=code_screen_quality mcp="Show the fiscal 2025 return on equity, return on invested capital and gross margin of MRK, JNJ, PFE, XOM and JPM, and their return on invested capital for every fiscal year from 2022 to 2025." %}

The candidates split into three groups. Merck and Johnson & Johnson earn 21.7% and 17.7% on invested capital with gross margins of 72.0% and 67.9%. Their low multiples reflect pressure across pharmaceuticals, with Merck's Keytruda patent expiry ahead and Johnson & Johnson's litigation, rather than a weakening business. Merck's dip to 0.8% in 2023 was a one-off: a large acquisition charge for research in progress, after which ROIC was back at 21.9% the following year.

Pfizer and Exxon Mobil are the ones where the trend matters. Pfizer's ROIC collapsed from 28.1% in 2022 to 3.0% in 2023 once COVID vaccine revenue ran off, and has come back since, to 9.5% in 2024 and 11.2% in 2025. Its gross margin of 74.3%, the highest of the five, says the underlying drug business still has pricing power. But its ROE was only 8.9%, and **a low multiple on earnings that have already reset is not the same as a low multiple on earnings that are intact**. Exxon's ROIC fell every year, from 20.3% in 2022 to 7.9% in 2025, as oil and gas prices came down from their 2022 peak; its gross margin of 21.7% reflects the commodity economics of refining and distribution.

JPMorgan earns 4.8% on invested capital, which would disqualify an industrial company. For a bank funded largely by deposits, its ROE of 15.8% is the more relevant measure, and a P/E of 16.1 on that return doesn't look like an obvious bargain or an obvious trap. Deciding which needs the bank measures this screen doesn't use.

## The Shortlist: Where Quality Comes Cheap

The final step applies a quality threshold: an ROIC above 10%. The level is a judgment call; it roughly separates businesses that earn well above a typical cost of capital from those that don't.

The candidates that earn more than 10% on invested capital, sorted by ROIC:

| Ticker | ROE | ROIC | Gross Margin |
|--------|----:|-----:|-------------:|
| MRK | 36.9% | 21.7% | 72.0% |
| JNJ | 35.0% | 17.7% | 67.9% |
| PFE | 8.9% | 11.2% | 74.3% |

Three names remain. A hard cutoff decides a lot here: Pfizer passes at 11.2% but would have missed a year earlier at 9.5%, and Exxon Mobil misses at 7.9% but would just have passed in 2024 at 10.0%. JPMorgan falls away clearly at 4.8%.

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
{% include ft-chart.html id="screen-final" src="/assets/data/article-charts.json" label="ROIC against EV/EBITDA for all 15 stocks, fiscal 2025" code=code_screen_final mcp="Compare the fiscal 2025 return on invested capital and EV/EBITDA of AAPL, MSFT, INTC, IBM, JNJ, PFE, MRK, KO, WMT, JPM, BAC, XOM, CVX, META and GOOGL. Which ones earn more than 10 percent on invested capital while trading below 20 times earnings and 18 times EBITDA?" %}

Quality is easy to find in this universe. Apple (62.0%), Alphabet (26.0%), Microsoft (25.8%), Coca-Cola (14.7%), Walmart (13.6%) and IBM (13.5%) all earn more on their capital than the 10% threshold, but at 19 to 29 times EBITDA. Meta earns 22.0% at 16.7 times EBITDA, so it sits in the same corner as the shortlist on this chart, but its P/E of 28.1 kept it out of the first pass. Merck, Johnson & Johnson and Pfizer are the three that combine an ROIC above 10% with EV/EBITDA of 10.2, 16.0 and 8.2. Chevron and Exxon Mobil are about as cheap at 8.8 and 9.3 times EBITDA, but earn 5.1% and 7.9% on their capital.

## Conclusion: A Watchlist, Not a Buy List

The screen reduced fifteen stocks to three, and the reasons the others dropped out are as useful as the result: Intel on earnings that have collapsed, Chevron and Exxon Mobil on falling returns as commodity prices normalised, the banks on metrics that don't fit them, and most of technology and consumer staples on price rather than quality.

What the screen can't tell you is whether the market's reasons for the low multiples are right. Merck's trailing ROIC says nothing about revenue after Keytruda loses patent protection, Johnson & Johnson's says nothing about the outcome of its litigation, and Pfizer's says nothing about whether its recovery since 2023 continues. Those need analysis the Toolkit can support but not automate: pipelines, debt maturities, capital allocation and the catalysts in the next few quarters. The thresholds are also choices: an ROIC limit of 12% instead of 10% would have dropped Pfizer, and one of 7.5% would have kept Exxon Mobil.

The output of this screen is a watchlist rather than a buy list. What it does well is take twelve names off the desk quickly, for reasons you can check, so the time goes to the three where price and quality point the same way. This is an illustration of a method, not investment advice.

{% include ft-charts-script.html %}
