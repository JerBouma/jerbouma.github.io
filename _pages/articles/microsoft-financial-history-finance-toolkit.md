---
title: How Microsoft Has Changed Since Its IPO
date: 2026-06-14
permalink: /articles/microsoft-financial-history-finance-toolkit
excerpt: "Explore Microsoft's financial journey over 40 years using the Finance Toolkit. This article analyzes revenue, net income, and other key metrics to understand the company's transformation."
description: "Learn how Microsoft's financials have evolved since its IPO, with detailed analysis and Python code using the Finance Toolkit."
layout: single
classes: custom-document
author_profile: false
collection: article
tags: [Finance Toolkit, Fundamental Analysis]
share: true
---

March 13, 1986. Microsoft went public at $21 per share ([Wikipedia](https://en.wikipedia.org/wiki/History_of_Microsoft)). Split-adjusted, that works out to roughly $0.08. The stock closed 2025 at $484 (Finance Toolkit historical data), making it one of the most remarkable compounding records in market history: a return of more than 5,000x over four decades.

But the stock price alone obscures something more interesting. The Microsoft that went public in 1986 and the Microsoft that generates $282 billion in annual revenue today are not the same company. The financials show three distinct businesses operating under the same name, each shaped by a different CEO, a different product strategy, and a different relationship with capital. Pulling 40 years of data through the Finance Toolkit makes that transformation visible in a way that no headline number can.

This blogpost demonstrates using the Finance Toolkit to analyze Microsoft's financial history. It also includes MCP prompts at the end of each section so you can run the same analysis yourself. **For more information on Finance Toolkit, have a look [here](https://github.com/JerBouma/FinanceToolkit). To explore the Finance Toolkit MCP, see [here](https://www.jeroenbouma.com/projects/financetoolkit/mcp).**

## Setting Things Up

Start by installing the Finance Toolkit:

```bash
pip install financetoolkit
```

Then import the library and create a Toolkit instance for Microsoft, specifying the ticker, your FMP API key, and the start date for historical data:

```python
from financetoolkit import Toolkit

company = Toolkit(
    tickers=["MSFT"],
    api_key="YOUR_FMP_API_KEY",
    start_date="1986-01-01"
)
```

Get your FMP API key at [jeroenbouma.com/fmp](https://www.jeroenbouma.com/fmp). The free plan covers five years of history; a paid plan unlocks the full 40-year dataset used here.

## Revenue: Three Very Different Eras

Microsoft's revenue history divides cleanly into three phases, each corresponding to a CEO tenure: Bill Gates (1986-2000), Steve Ballmer (2000-2014), and Satya Nadella (2014-present).

```python
income_statement = company.get_income_statement()

revenue = income_statement.loc[
    ["Revenue", "Net Income"],
    ["1986", "1990", "1995", "2000", "2005", "2010", "2015", "2020", "2025"]
]
```

Which returns:

| Year | Revenue ($B) | Net Income ($B) |
|------|-------------|-----------------|
| 1986 | 0.2 | 0.04 |
| 1990 | 1.2 | 0.3 |
| 1995 | 5.9 | 1.5 |
| 2000 | 23.0 | 9.4 |
| 2005 | 39.8 | 12.3 |
| 2010 | 62.5 | 18.8 |
| 2015 | 93.6 | 12.2 |
| 2020 | 143.0 | 44.3 |
| 2025 | 281.7 | 101.8 |

The Gates era was extraordinary by any standard. Revenue grew from $197 million in 1986 to $23 billion in 2000, a 115-fold increase in 14 years driven almost entirely by Windows and Office on the back of the PC revolution. Microsoft was not really a technology company in the modern sense; it was a licensing machine with near-zero cost of reproduction and near-monopoly pricing power.

The Ballmer era is often described as a lost decade, but that framing is partly unfair. Revenue grew from $23 billion to $87 billion between 2000 and 2014 (Finance Toolkit income statement). That is real growth by any measure. What failed was not the business but the valuation. Ballmer inherited Microsoft at the height of the dot-com bubble, when the market was pricing in decades of compounding at rates no company could sustain. The stock went roughly nowhere for 14 years not because the business stagnated, but because the starting price was simply too high.

The 2015 net income of $12.2 billion against $93.6 billion in revenue reflects Nadella's first full year, when Microsoft took a $7.5 billion write-down on the Nokia acquisition ([Wikipedia](https://en.wikipedia.org/wiki/List_of_mergers_and_acquisitions_by_Microsoft)). Strip that out and the underlying business was already accelerating. By 2020, net income had grown to $44 billion. By 2025 it reached $102 billion, a number that would have seemed absurd when Nadella took over.

> **Try this in the Finance Toolkit MCP:** *"Show me Microsoft's annual revenue from 1986 to 2025, and identify the three distinct growth phases under Gates, Ballmer, and Nadella."*

## Profitability: Margins That Compress, Then Recover

The revenue story is straightforward. The margin story is more nuanced.

```python
ratios = company.ratios.collect_profitability_ratios()

margins = ratios.loc[
    ["Gross Margin", "Net Profit Margin"],
    ["1990", "1995", "2000", "2005", "2010", "2015", "2020", "2025"]
]
```

Which returns:

| Year | Gross Margin | Net Margin |
|------|-------------|------------|
| 1990 | 82.6% | 23.6% |
| 1995 | 89.8% | 24.5% |
| 2000 | 86.9% | 41.0% |
| 2005 | 84.8% | 30.8% |
| 2010 | 80.2% | 30.0% |
| 2015 | 64.7% | 13.0% |
| 2020 | 67.8% | 31.0% |
| 2025 | 68.8% | 36.2% |

Gross margins peaked near 90% in the mid-1990s, reflecting what pure software economics look like. Distributing a copy of Windows cost almost nothing once the disc was pressed. As Microsoft expanded into hardware (Xbox, Surface), services, and cloud infrastructure, the cost structure changed. Azure compute costs real money to run. So does gaming content, data center operations, and technical support at enterprise scale. By 2015, gross margins had compressed to 64.7%.

That compression has largely stabilized. Azure's gross margin has improved as the infrastructure matures and higher-margin software services (Azure AI, Microsoft 365, Copilot) grow as a share of the mix. The more important metric is net margin, which tells a different story: it has recovered to 36.2% in 2025, approaching the levels Microsoft achieved at the peak of its software monopoly in 2000. The 2015 net margin of 13% is an outlier caused by the Nokia write-down, not a structural deterioration.

The reason for the recovery is operating leverage. Revenue nearly tripled from 2015 to 2025, but operating expenses did not. Each additional dollar of cloud or subscription revenue drops to the bottom line at an increasingly favorable rate.

> **Try this in the Finance Toolkit MCP:** *"What were Microsoft's gross margin and net profit margin at five-year intervals from 1990 to 2025? Highlight where margins compressed and where they recovered."*

## The Balance Sheet Tells a Story by Decade

Early Microsoft had no debt. None. The business generated more cash than it could spend, and management had no desire to lever up. For most of the Gates era and the first half of the Ballmer era, the balance sheet was a cash accumulation machine.

```python
balance_sheet = company.get_balance_sheet_statement()

snapshot = balance_sheet.loc[
    ["Cash and Short Term Investments", "Long Term Debt", "Goodwill"],
    ["1995", "2000", "2005", "2010", "2015", "2020", "2025"]
]
```

Which returns:

| Year | Cash + Investments ($B) | Long-Term Debt ($B) | Goodwill ($B) |
|------|------------------------|--------------------|---------| 
| 1995 | 2.0 | 0.0 | 0.0 |
| 2000 | 23.8 | 0.0 | 0.0 |
| 2005 | 37.8 | 0.0 | 0.0 |
| 2010 | 36.8 | 4.9 | 12.4 |
| 2015 | 96.5 | 27.8 | 16.9 |
| 2020 | 136.5 | 59.6 | 43.4 |
| 2025 | 94.6 | 40.2 | 119.5 |

The first debt appeared in 2009 (Finance Toolkit balance sheet), not because Microsoft needed the money, but because borrowing at low rates to fund buybacks was more tax-efficient than repatriating overseas cash. By 2020, cash and investments had reached $136 billion while long-term debt stood at $60 billion. The net position was still comfortably positive, but the capital structure had become more aggressive.

The most striking shift is goodwill. It was zero for most of Microsoft's history because the company built rather than bought. That changed under Ballmer with acquisitions like aQuantive and Skype, and accelerated dramatically under Nadella. LinkedIn ($26 billion, 2016), GitHub ($7.5 billion, 2018), Nuance ($19 billion, 2022), and Activision Blizzard ($69 billion, 2023) turned Microsoft into one of the most acquisitive companies in tech ([Wikipedia](https://en.wikipedia.org/wiki/List_of_mergers_and_acquisitions_by_Microsoft)). Goodwill reached $119.5 billion in 2025.

The cash balance fell from $136 billion in 2020 to $94.6 billion in 2025, largely because of Activision. Long-term debt has declined from its peak of $66.7 billion in 2019 (Finance Toolkit balance sheet) to $40.2 billion in 2025 as Microsoft pays down the acquisition-related borrowing, a sign that the balance sheet is normalising after the deal.

## Free Cash Flow: The Number That Matters Most

Revenue and earnings can be managed. Free cash flow is harder to fake. It is also the number that ultimately determines what a company is worth. Not the earnings per share, not the operating income, but the actual cash that flows out of the business after maintaining and expanding the asset base.

```python
cash_flow = company.get_cash_flow_statement()

fcf_table = cash_flow.loc[
    ["Operating Cash Flow", "Capital Expenditure", "Free Cash Flow"],
    ["1995", "2000", "2005", "2010", "2015", "2020", "2025"]
]
```

Which returns:

| Year | Operating Cash Flow ($B) | CapEx ($B) | Free Cash Flow ($B) |
|------|------------------------|-----------|---------------------|
| 1995 | 2.0 | -0.5 | 1.5 |
| 2000 | 11.4 | -0.9 | 10.5 |
| 2005 | 16.6 | -0.8 | 15.8 |
| 2010 | 24.1 | -2.0 | 22.1 |
| 2015 | 29.7 | -5.9 | 23.7 |
| 2020 | 60.7 | -15.4 | 45.2 |
| 2025 | 136.2 | -64.6 | 71.6 |

Microsoft generated $71.6 billion in free cash flow in fiscal 2025, more than the entire annual revenue of companies like Netflix or Airbnb. It is the product of two converging forces: subscription and consumption revenue that scales without proportional cost increases, and a customer base that has locked itself into the Microsoft ecosystem so deeply that churn is structurally low.

There is a caveat embedded in those numbers. Capital expenditure has increased from $5.9 billion in 2015 to $64.6 billion in 2025, the vast majority of it AI infrastructure. Microsoft is making an enormous bet on data center capacity to support Azure AI and Copilot services. Whether that $65 billion in annual CapEx generates returns commensurate with its cost will be the defining capital allocation question of the next five years. For now, operating cash flow has grown fast enough to absorb it, but the ratio of FCF to operating cash flow has compressed.

> **Try this in the Finance Toolkit MCP:** *"What was Microsoft's free cash flow in 2015 and 2025? Show the operating cash flow and capital expenditure over time."*

## Return on Equity: What Buybacks and Leverage Changed

Return on equity sounds like a clean measure of profitability, but it is not always clean. ROE depends on the size of the equity base, which Microsoft has spent the last 15 years shrinking through aggressive buybacks and debt-funded capital return. A company can raise its ROE by buying back enough shares to reduce equity even if underlying profitability does not improve.

```python
profitability_ratios = company.ratios.collect_profitability_ratios()

profitability_ratios.loc[
    ["Return on Equity", "Return on Assets", "Return on Invested Capital"],
    ["1990", "1995", "2000", "2010", "2015", "2020", "2025"]
]
```

Which returns:

| Year | ROE | ROA | ROIC |
|------|-----|-----|------|
| 1990 | 37.7% | 30.6% | 36.9% |
| 1995 | 29.3% | 23.1% | 29.3% |
| 2000 | 27.0% | 20.7% | 27.0% |
| 2010 | 43.8% | 22.9% | 47.9% |
| 2015 | 14.4% | 7.0% | 19.4% |
| 2020 | 40.1% | 15.1% | 30.5% |
| 2025 | 33.3% | 18.0% | 30.6% |

The early Microsoft numbers are a reminder of what a capital-light monopoly looks like. ROE of 38% in 1990 with zero debt and no buybacks means the underlying business was genuinely that profitable. Those returns compressed through the 2000s as the business mix changed and the equity base remained large.

The 2015 figures are distorted by the Nokia write-down, which depressed net income and inflated the apparent collapse in ROA and ROE. By 2020 ROE had rebounded to 40%, though this partly reflects the equity base shrinking from buybacks rather than purely improved profitability. ROIC strips out the effects of capital structure and tells a cleaner story: Microsoft earns roughly 30-31% on invested capital today, which is very good but not dramatically different from what it earned in the 1990s. The business quality has been maintained; what changed is how the returns are distributed to shareholders.

Return on assets paints a similar picture. ROA of 18% in 2025 reflects that Microsoft now carries a much heavier asset base of cloud infrastructure, acquisitions, and data centers than the software company of the 1990s. The high-30s ROA of the Gates era is gone, but 18% is a strong number for a company of this size and scope.

## Looking Ahead

Forty years of operating history tell you what Microsoft has been. Valuation multiples tell you what the market thinks it will be. The tables below show where Microsoft's key ratios and risk-adjusted performance metrics have stood over the past six years, alongside the Alpha and Beta figures that put the stock's behaviour in market context.

```python
valuation_ratios = company.ratios.collect_valuation_ratios()

current_valuation = valuation_ratios.loc[
    ["Price-to-Earnings", "Price-to-Book", "Price-to-Free-Cash-Flow", "EV-to-EBITDA"],
    ["2020", "2021", "2022", "2023", "2024", "2025"]
]

performance = company.performance.collect_all_metrics()

alpha_beta_performance = performance.loc[
    ["2020", "2021", "2022", "2023", "2024", "2025"],
    ["Beta", "Alpha"]
]
```

Which returns:

| Metric | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|--------|------|------|------|------|------|------|
| P/E | 38.6 | 41.8 | 24.9 | 38.8 | 35.7 | 35.5 |
| P/B | 14.4 | 18.0 | 10.9 | 13.6 | 11.7 | 10.5 |
| P/FCF | 37.8 | 45.6 | 27.8 | 47.2 | 42.5 | 50.4 |
| EV/EBITDA | 27.0 | 32.2 | 19.1 | 27.9 | 24.5 | 22.7 |

| Metric | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|--------|------|------|------|------|------|------|
| Beta | 1.14 | 1.15 | 1.28 | 1.16 | 1.19 | 0.88 |
| Alpha | +0.25 | +0.24 | -0.09 | +0.33 | -0.11 | -0.02 |

At 35x earnings and 50x free cash flow, Microsoft is priced for sustained growth. The P/FCF ratio in particular looks stretched on the surface, but it needs to be read alongside the elevated CapEx. Microsoft spent $64.6 billion on capital expenditure in fiscal 2025, the vast majority of it on AI infrastructure. If that investment generates meaningful Azure revenue growth over the next three to five years, the normalized FCF picture is more attractive than the headline ratio suggests. If it does not, the multiple will prove optimistic.

Beta declining to 0.88 in 2025 is notable. For most of the Nadella era, Microsoft moved in line with or slightly above the broader market. A beta below 1 suggests the market increasingly treats it as a defensive-quality holding: a large, profitable, cash-generative business that belongs in portfolios regardless of the macro environment.

Alpha has been positive in most years, notably +0.33 in 2023 when Microsoft's AI positioning drove a 57% stock return (Finance Toolkit historical data) against the S&P 500's 26%. The negative alpha in 2022 and 2024 reflects years when the market rotated toward other sectors, not fundamental deterioration. The business compounded steadily throughout.

What to watch over the next few years: the pace of Azure growth (which funds everything else), margin expansion as the AI CapEx cycle matures, and whether Activision contributes enough to earnings to justify the $69 billion price tag. The financial track record over 40 years gives Microsoft the benefit of the doubt. But at these valuations, the margin for error is narrower than it has been at any point in the company's history outside the dot-com peak.
