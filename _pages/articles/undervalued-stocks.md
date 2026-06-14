---
title: Screening for Undervalued Stocks with the Finance Toolkit
date: 2026-06-14
permalink: /articles/screening-undervalued-stocks-finance-toolkit
excerpt: "Learn how to build a systematic stock screen using the Finance Toolkit. Pull valuation multiples across a universe of stocks, apply multi-metric filters, and overlay profitability metrics to separate genuine value from value traps."
description: "Build a Python-based stock screener using P/E, EV/EBITDA, ROIC, and gross margins with the Finance Toolkit."
layout: single
classes: custom-document
author_profile: false
collection: article
tags: [Finance Toolkit, Fundamental Analysis, Stock Screening]
share: true
---

With thousands of publicly listed companies, finding undervalued stocks by hand is impractical. A systematic screen changes that: pull valuation multiples across an entire universe, filter by multiple criteria simultaneously, and overlay profitability metrics to separate genuine value from value traps. The Finance Toolkit makes each of those steps a few lines of Python.

This article walks through a complete screening process from universe definition to a final shortlist. It uses 15 stocks across five sectors to illustrate the logic, a real screen would cast a wider net, and the Discovery module supports that too.

**For more information on Finance Toolkit, have a look [here](https://github.com/JerBouma/FinanceToolkit). To explore the Finance Toolkit MCP, see [here](https://www.jeroenbouma.com/projects/financetoolkit/mcp).**

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
    api_key="YOUR_FMP_API_KEY",
    start_date="2022-01-01"
)
```

Get your FMP API key at [jeroenbouma.com/fmp](https://www.jeroenbouma.com/fmp). The free plan covers five years of history; a paid plan unlocks deeper history and a larger universe.

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

The spread is immediately visible. BAC and MRK trade below 15x earnings. WMT trades at 46x. INTC appears at the top of the sort only because its P/E is negative — the company reported a net loss — which is why sorting by a single metric is dangerous without additional filters.

A few other readings worth noting. KO trades at 57x free cash flow despite a relatively modest P/E of 23x, suggesting either elevated CapEx or capital structure effects. P/B of 55.3x for AAPL reflects the reality that Apple has bought back so much equity it has almost none left — a reminder that P/B is most useful for asset-heavy sectors like financials and energy.

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

JPM passes the P/E filter but misses on EV/EBITDA at 18.7x — marginally above the threshold. CVX passes on EV/EBITDA (8.9x) but its P/E of 23x falls just outside the cut. Five stocks pass both filters: BAC, JNJ, MRK, PFE, and XOM.

Note that EV/EBITDA is less meaningful for banks, where the concept of enterprise value and operating earnings work differently from industrial companies. JPM at 16x P/E with a P/FCF of 8.9x deserves separate consideration using bank-specific metrics like price-to-tangible-book and return on equity.

## Step 3: The Quality Overlay

Cheap on valuation is not the same as undervalued. The value trap problem is real: stocks trade at low multiples because investors expect deteriorating earnings, balance sheet stress, or structural decline. Before acting on any of the five candidates, the profitability picture needs to hold up.

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

# Apply the filtering from Step 2
quality.loc[value_candidates]
```

Which returns:

| Ticker | ROE | ROIC | Gross Margin |
|--------|----:|-----:|-------------:|
| BAC | 9.7% | 4.8% | 56.1% |
| JNJ | 35.0% | 33.0% | 72.8% |
| MRK | 36.9% | 28.1% | 71.8% |
| PFE | 8.8% | 11.3% | 70.3% |
| XOM | 10.7% | 14.8% | 21.7% |

The table separates the field. JNJ and MRK both earn above 28% on invested capital with gross margins above 71%. These are not cheap because the business is deteriorating — they are cheap because pharmaceutical stocks have faced broader sector pressure, patent cliff concerns (MRK), and litigation overhangs (JNJ). The underlying profitability is intact.

XOM earns 14.8% ROIC, which is solid for an energy company operating with significant fixed asset bases. The thin gross margin of 21.7% reflects the commodity economics of oil refining and distribution rather than a structural weakness. The risk here is cyclical: energy earnings compress when oil prices fall.

PFE at 11.3% ROIC is borderline. Its gross margin of 70.3% confirms the underlying pharmaceutical business generates strong economics, but the headline return metrics are depressed by the revenue reset after COVID vaccine revenues ran off. Whether this is a genuine recovery opportunity or a prolonged restructuring depends on the pipeline.

BAC at 4.8% ROIC would look like a disqualifier in an industrial context. For a bank, where assets are funded by deposits rather than equity, ROE of 9.7% is the more relevant metric. That said, it suggests the market's discount is modest rather than an obvious bargain.

## Step 4: The Final Screen
This is where the rubber meets the road. After narrowing our universe down to fundamentally sound businesses, the final screen applies a strict Return on Invested Capital (ROIC) threshold albeit somewhat arbitrary defined.

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

BAC falls out at 4.8% ROIC under the industrial threshold, though the banking context warrants separate analysis. The remaining four represent meaningfully different risk profiles.

JNJ and MRK are the strongest combination of value and quality in this screen. Both earn well above their cost of capital, carry strong franchise positions, and trade at multiples that imply no earnings growth — which is conservative given both have significant product pipelines. XOM offers commodity exposure with decent capital efficiency and a low EV/EBITDA of 9.3x, appropriate for investors comfortable with oil cycle risk. PFE is the speculative recovery candidate: the business model is intact, the discount is real, but the recovery timeline is uncertain.

## Conclusion

Each of these names requires analysis the Toolkit can support but cannot automate: debt maturity profiles, near-term earnings catalysts, management capital allocation track records, and sector-specific risk factors. MRK’s patent cliff on Keytruda is a known risk not captured in trailing ROIC. XOM’s capital expenditure plans depend heavily on a commodity price path no screen can forecast.

The output of this screen is a watchlist, not a buy list. What it does efficiently is eliminate the 11 stocks where the combination of price and quality does not justify closer attention.