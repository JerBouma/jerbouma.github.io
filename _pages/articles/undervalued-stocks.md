---
title: Screening for Undervalued Stocks with the Finance Toolkit
seo_title: "Screening for Undervalued Stocks in Python"
date: 2026-06-14
last_modified_at: 2026-10-02
permalink: /articles/screening-undervalued-stocks-finance-toolkit
excerpt: "How to build a systematic stock screen with the Finance Toolkit: pull valuation multiples across a universe of stocks, filter on several metrics at once and add profitability metrics to tell real value from value traps."
description: "Build a Python-based stock screener using P/E, EV/EBITDA, ROIC, and gross margins with the Finance Toolkit."
layout: single
classes: wide-sidebar article-document
author_profile: false
collection: article
tags: [Fundamental Analysis]
share: true
---

With thousands of publicly listed companies, finding undervalued stocks by hand is impractical. A systematic screen makes it manageable: you pull valuation multiples across an entire universe, filter on several criteria at once, and overlay profitability metrics to separate real value from value traps. With the Finance Toolkit, each of those steps takes a few lines of Python.

In this article I walk through a complete screening process, from defining the universe to a final shortlist. It uses 15 stocks across five sectors to illustrate the logic. A real screen would cast a wider net, which the Discovery module also supports.

**For more information on Finance Toolkit, have a look [here](https://github.com/JerBouma/FinanceToolkit){:target="_blank"}. To run the same analysis conversationally, explore the [Finance Toolkit MCP server](/projects/financetoolkit/mcp).**

> **Try this with the Finance Toolkit MCP:** *"Screen 15 stocks across technology, healthcare, consumer staples, financials, and energy for P/E below 20, EV/EBITDA below 18, and ROIC above 10%. Show the valuation and quality metrics side by side."*

## Setting Things Up

Start by installing the Finance Toolkit:

```bash
pip install financetoolkit
```

Then import the library and define a universe of tickers. The example below uses 15 stocks across technology, healthcare, consumer staples, financials, and energy.

```python
import pandas as pd
from financetoolkit import Toolkit

screener = Toolkit(
    tickers=[
        "AAPL", "MSFT", "INTC", "IBM",
        "JNJ", "PFE", "MRK",
        "KO", "WMT",
        "JPM", "BAC",
        "XOM", "CVX",
        "META", "GOOGL"
    ],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2022-01-01"
)
```

Get your FMP API key at [jeroenbouma.com/fmp](/fmp){:target="_blank"}. The free plan covers five years of history; a paid plan gives access to deeper history and a larger universe.

## Step 1: Pulling Valuation Multiples

The first pass uses four ratios to get a broad picture of relative cheapness. P/E and EV/EBITDA are the most common entry points; P/FCF and P/B provide cross-checks that are harder to manipulate.

```python
# Capture the most recent annual date, in this case 2025
pe = screener.ratios.get_price_to_earnings_ratio()["2025"]
pfcf = screener.ratios.get_price_to_free_cash_flow_ratio()["2025"]
pb = screener.ratios.get_price_to_book_ratio()["2025"]
ev_ebitda = screener.ratios.get_ev_to_ebitda_ratio()["2025"]

# Combine each into one DataFrame
valuation = pd.DataFrame({
    "P/E": pe,
    "P/FCF": pfcf,
    "P/B": pb,
    "EV/EBITDA": ev_ebitda
}).sort_values("P/E")
```

Which returns:

| Ticker | P/E | P/FCF | P/B | EV/EBITDA |
|--------|----:|------:|----:|----------:|
| INTC | - | - | 1.6 | 19.1 |
| BAC | 14.3 | 32.9 | 1.5 | 14.4 |
| MRK | 14.5 | 21.4 | 5.0 | 10.2 |
| JPM | 16.2 | 8.9 | 2.6 | 18.7 |
| XOM | 18.0 | 21.9 | 2.0 | 9.3 |
| PFE | 18.3 | 15.6 | 1.6 | 9.4 |
| JNJ | 18.8 | 25.5 | 6.2 | 16.0 |
| CVX | 23.0 | 17.0 | 1.5 | 8.9 |
| KO | 23.0 | 56.9 | 9.4 | 22.9 |
| IBM | 26.5 | 24.3 | 8.6 | 21.8 |
| META | 28.1 | 36.8 | 7.8 | 17.1 |
| GOOGL | 29.0 | 52.2 | 9.2 | 25.7 |
| MSFT | 35.5 | 50.4 | 10.5 | 22.7 |
| AAPL | 36.4 | 41.3 | 55.3 | 28.7 |
| WMT | 46.3 | 71.1 | 9.9 | 22.6 |

The spread is wide: BAC and MRK trade below 15x earnings while WMT trades at 46x. INTC appears at the top of the sort only because its P/E is negative (the company reported a net loss), which is why sorting by a single metric is misleading without additional filters.

A few other readings are worth noting. KO trades at 57x free cash flow despite a relatively modest P/E of 23x, suggesting either elevated CapEx or capital structure effects. The P/B of 55.3x for AAPL reflects that Apple has bought back so much equity that it has almost none left, which is a reminder that P/B is most useful for asset-heavy sectors like financials and energy.

## Step 2: Applying the Filter

A single-metric screen is easy to game by accounting choices, one-time charges, or unusual capital structures. The approach here requires two metrics to pass simultaneously: a P/E below 20x and an EV/EBITDA below 18x, with negative earners excluded.

```python
# Apply thorough filtering
value_candidates = valuation[
    (valuation["P/E"] > 0) &
    (valuation["P/E"] < 20) &
    (valuation["EV/EBITDA"] < 18)
]

# List the available companies
list(value_candidates.index)
```

Which returns:

```
['BAC', 'JNJ', 'MRK', 'PFE', 'XOM']
```

JPM passes the P/E filter but misses on EV/EBITDA at 18.7x, marginally above the threshold. CVX passes on EV/EBITDA (8.9x) but its P/E of 23x falls just outside the cut. Five stocks pass both filters: BAC, JNJ, MRK, PFE, and XOM.

Note that EV/EBITDA is less meaningful for banks, where the concept of enterprise value and operating earnings work differently from industrial companies. JPM at 16x P/E with a P/FCF of 8.9x deserves separate consideration using bank-specific metrics like price-to-tangible-book and return on equity.

## Step 3: The Quality Overlay

A low valuation does not automatically make a stock undervalued. Stocks often trade at low multiples because investors expect deteriorating earnings, balance sheet stress, or structural decline, which is the classic value trap. Before acting on any of the five candidates, the profitability picture needs to hold up.

```python
# Collect data from the most recent year
roe = screener.ratios.get_return_on_equity()["2025"]
roic = screener.ratios.get_return_on_invested_capital()["2025"]
gross_margin = screener.ratios.get_gross_margin()["2025"]

# Combine them into one DataFrame
quality = pd.DataFrame({
    "ROE": roe,
    "ROIC": roic,
    "Gross Margin": gross_margin
})

# Keep the candidates from Step 2
quality = quality.loc[value_candidates.index]
quality
```

Which returns:

| Ticker | ROE | ROIC | Gross Margin |
|--------|----:|-----:|-------------:|
| BAC | 9.7% | 4.8% | 56.1% |
| JNJ | 35.0% | 33.0% | 72.8% |
| MRK | 36.9% | 28.1% | 71.8% |
| PFE | 8.8% | 11.3% | 70.3% |
| XOM | 10.7% | 14.8% | 21.7% |

This table separates the candidates. JNJ and MRK both earn above 28% on invested capital with gross margins above 71%. Their low valuations come from broader pressure on pharmaceutical stocks, patent cliff concerns (MRK), and litigation overhangs (JNJ) rather than from a deteriorating business, and the underlying profitability is intact.

XOM earns 14.8% ROIC, which is solid for an energy company operating with large fixed asset bases. The thin gross margin of 21.7% reflects the commodity economics of oil refining and distribution rather than a structural weakness. The risk here is cyclical: energy earnings compress when oil prices fall.

PFE at 11.3% ROIC is borderline. Its gross margin of 70.3% confirms the underlying pharmaceutical business generates strong economics, but the headline return metrics are depressed by the revenue reset after COVID vaccine revenues ran off. Whether this is a real recovery opportunity or a prolonged restructuring depends on the pipeline.

BAC at 4.8% ROIC would look like a disqualifier in an industrial context. For a bank, where assets are funded by deposits rather than equity, ROE of 9.7% is the more relevant metric. That said, it suggests the market's discount is modest rather than an obvious bargain.

## Step 4: The Final Screen
After narrowing the universe down to fundamentally sound businesses, the final screen applies a strict, if somewhat arbitrarily chosen, Return on Invested Capital (ROIC) threshold.

```python
# Apply a strict threshold on ROIC
final_screen = quality[
  quality["ROIC"] > 0.10].sort_values("ROIC", ascending=False)
```

Which returns:

| Ticker | ROE | ROIC | Gross Margin |
|--------|----:|-----:|-------------:|
| JNJ | 35.0% | 33.0% | 72.8% |
| MRK | 36.9% | 28.1% | 71.8% |
| XOM | 10.7% | 14.8% | 21.7% |
| PFE | 8.8% | 11.3% | 70.3% |

BAC falls out at 4.8% ROIC under the industrial threshold, though the banking context warrants separate analysis. The remaining four have quite different risk profiles.

JNJ and MRK are the strongest combination of value and quality in this screen. Both earn well above their cost of capital, carry strong franchise positions, and trade at multiples that imply no earnings growth, which is conservative given both have significant product pipelines. XOM offers commodity exposure with decent capital efficiency and a low EV/EBITDA of 9.3x, appropriate for investors comfortable with oil cycle risk. PFE is the speculative recovery candidate: the business model is intact and the discount is real, but the recovery timeline is uncertain.

## Conclusion

Each of these names requires analysis the Toolkit can support but cannot automate: debt maturity profiles, near-term earnings catalysts, management capital allocation track records, and sector-specific risk factors. MRK’s patent cliff on Keytruda is a known risk not captured in trailing ROIC. XOM’s capital expenditure plans depend heavily on a commodity price path no screen can forecast.

The output of this screen is a watchlist rather than a buy list. What it does well is eliminate the 11 stocks where the combination of price and quality does not justify closer attention.