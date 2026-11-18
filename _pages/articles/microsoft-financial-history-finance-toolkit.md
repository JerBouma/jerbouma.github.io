---
title: How Microsoft Has Changed Since Its IPO
date: 2026-06-14
last_modified_at: 2026-11-18
permalink: /articles/microsoft-financial-history-finance-toolkit
excerpt: "Microsoft's revenue went from $198 million in 1986 to $282 billion in 2025. Under Steve Ballmer it nearly quadrupled while shareholders lost money, and forty years of financials show three different companies under one name."
description: "Microsoft's financial history from its 1986 IPO to 2025: revenue growth by CEO era, margins, the balance sheet, free cash flow, ROE versus ROIC and valuation."
layout: single
classes: wide-sidebar article-document
author_profile: false
collection: article
tags: [Fundamental Analysis]
share: true
cover:
  image: /assets/images/articles/microsoft-financial-history-finance-toolkit/cover.jpg
  alt: "A 1980s computer room with terminals, tape drives and staff at work."
  credit: "US Census Bureau computer room, 1980s, public domain"
  link: "https://commons.wikimedia.org/wiki/File:US_Census_Bureau_computer_room_1980s.jpg"
---

Microsoft went public on March 13, 1986 ([Wikipedia](https://en.wikipedia.org/wiki/History_of_Microsoft){:target="_blank"}). In the fiscal year that ended that June, its revenue was $198 million. In fiscal 2025 it was $282 billion, about 1,400 times as much, and a share bought at the IPO had risen more than 5,000-fold by the end of 2025.

How did the company underneath that record change? The financials show a different business under each chief executive. Under Bill Gates revenue grew 40% a year. Under Steve Ballmer it nearly quadrupled while shareholders lost money over 14 years, and under Satya Nadella Microsoft became a cloud company that spends almost a quarter of its revenue on capital expenditure. Growth and the return on capital can change completely while the name and the ticker stay the same, which is easy to miss in a long track record. I use Microsoft's annual financial statements for fiscal 1986 to 2025 and its share price up to the end of 2025, both as collected by FinancialModelingPrep.

## Ballmer and Nadella Grew Revenue at the Same Pace

The three eras line up with the three CEOs: Gates until 2000, Ballmer from 2000 to 2014 and Nadella since. On a log scale the slope of a line is its growth rate, so a company growing at a steady pace draws a straight line.

Revenue and net income per fiscal year, on a log scale:

{% capture code_revenue %}
```python
# pip install financetoolkit
import pandas as pd
from financetoolkit import Economics, Toolkit

toolkit = Toolkit(tickers=["MSFT"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="1986-01-01")

income_statement = toolkit.get_income_statement()
income_statement = income_statement.loc[["Revenue", "Net Income"], "1986":"2025"]

# Revenue growth per CEO era, nominal and in 2025 dollars (US CPI averaged over each July to June fiscal year)
economics = Economics(start_date="1985-07-01")

cpi = economics.get_consumer_price_index(countries="United States", period="monthly")
cpi = cpi["United States"]
cpi_fiscal_year = cpi.groupby(cpi.index.year + (cpi.index.month >= 7)).mean()

revenue = income_statement.loc["Revenue"]
revenue.index = revenue.index.year
real_revenue = revenue / cpi_fiscal_year.loc[1986:2025] * cpi_fiscal_year.loc[2025]

eras = {"Bill Gates": (1986, 2000), "Steve Ballmer": (2000, 2014), "Satya Nadella": (2014, 2025), "1986 to 2025": (1986, 2025)}
growth = pd.DataFrame(
    {
        era: {
            "Nominal": (revenue[end] / revenue[start]) ** (1 / (end - start)) - 1,
            "Real": (real_revenue[end] / real_revenue[start]) ** (1 / (end - start)) - 1,
            "Real, times as much": real_revenue[end] / real_revenue[start],
        }
        for era, (start, end) in eras.items()
    }
)
```
{% endcapture %}
{% include ft-chart.html id="msft-revenue" src="/assets/data/article-charts.json" label="Microsoft revenue and net income" code=code_revenue mcp="What were Microsoft's revenue and net income in every fiscal year from 1986 to 2025?" %}

The steep part of the line is the Gates era, when Windows and Office rode the spread of the PC. Microsoft was a licensing business: once the software was written, another copy cost next to nothing. After 2000 the line flattens, and from then on revenue grew at about 10% to 11% a year under both of his successors.

Growth per year in each CEO era:

| CEO | Fiscal years | Revenue | Net income | Shareholder return, with dividends |
|---|---|---|---|---|
| Bill Gates | 1986 to 2000 | 40% | 48% | 57% |
| Steve Ballmer | 2000 to 2014 | 10% | 6% | -1% |
| Satya Nadella | 2014 to 2025 | 11% | 15% | 26% |

**Revenue grew at about the same pace under Ballmer and Nadella, while the shares returned -1% a year in one era and 26% a year in the other.** Net income grew far faster under Nadella than under Ballmer, and the price the market paid for those earnings moved in opposite directions. Ballmer took over at the top of the dot-com bubble, with the shares at 83 times earnings at the end of 1999. By the end of 2013 that multiple was 14.5, so a growing business sat under a share price that went nowhere. Under Nadella the multiple rose again.

## Net Margin Recovered While Gross Margin Did Not

Gross margin is the share of revenue left after the direct cost of what is sold. Net margin is the share left after every cost, including tax. The two measure different things for Microsoft: the first shows what kind of business it runs, the second how well it covers its overheads.

Gross and net margin per fiscal year:

{% capture code_margins %}
```python
# pip install financetoolkit
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["MSFT"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="1986-01-01")

profitability_ratios = toolkit.ratios.collect_profitability_ratios()
margins = profitability_ratios.loc[["Gross Margin", "Net Profit Margin"], "1986":"2025"]

# The 2018 tax charge: the net margin of 2018 at the effective tax rate of 2017, and the low tax rate of 2019
tax = profitability_ratios.loc[["Income Before Tax Profit Margin", "Effective Tax Rate"], "2017":"2019"]
net_margin_2018_at_2017_tax_rate = tax.loc["Income Before Tax Profit Margin", "2018"] * (1 - tax.loc["Effective Tax Rate", "2017"])
```
{% endcapture %}
{% include ft-chart.html id="msft-margins" src="/assets/data/article-charts.json" label="Microsoft gross and net margins" code=code_margins mcp="What were Microsoft's gross margin and net profit margin in every fiscal year from 1986 to 2025?" %}

Gross margin peaked at 92% in 1996, which is what pure software economics look like. The move into hardware (Xbox, Surface), services and cloud infrastructure brought real direct costs with it, such as data centres and the power to run them. The gross margin bottomed at 64% in 2016 and has stayed below 70% since, so the cloud company runs on a structurally lower gross margin than the licensing company did.

Net margin reached 41% in 2000, sat lower for most of the next two decades and was back at 36% in 2025. The two sharp dips are one-off charges: the $7.5 billion impairment of the phone business bought from Nokia in 2015 (as the 2015 Annual Report states it), and in 2018 a tax charge from the US tax reform of late 2017. Leaving those aside, the recovery comes from operating leverage. Revenue tripled between 2015 and 2025 while operating expenses grew much more slowly, so more of each extra dollar of cloud and subscription revenue was left as profit.

## Goodwill Went From Zero to $120 Billion

Goodwill is the part of an acquisition's price above the value of the assets bought, so it grows when a company buys rather than builds.

Cash and short-term investments, long-term debt and goodwill at the end of each fiscal year:

{% capture code_balance %}
```python
# pip install financetoolkit
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["MSFT"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="1986-01-01")

balance_sheet = toolkit.get_balance_sheet_statement()
balance_sheet = balance_sheet.loc[["Cash and Short Term Investments", "Long Term Debt", "Goodwill"], "1995":"2025"]
```
{% endcapture %}
{% include ft-chart.html id="msft-balance" src="/assets/data/article-charts.json" label="Microsoft cash, debt and goodwill" code=code_balance mcp="How did Microsoft's cash and short-term investments, long-term debt and goodwill change in every fiscal year from 1995 to 2025?" %}

For its first two decades Microsoft built rather than bought, and it carried no long-term debt to speak of. Cash piled up to $61 billion in 2004, until a special dividend in fiscal 2005 took it down to $38 billion. The first debt arrived in 2009. Microsoft did not need the money, but borrowing at low rates to fund buybacks was cheaper than bringing cash held abroad back to the US and paying tax on it. Long-term debt peaked at $76 billion in 2017 and was down to $40 billion by 2025.

**Goodwill went from zero before 2006 to $120 billion in 2025, and most of it came under Nadella.** LinkedIn ($26 billion), Nuance ($20 billion) and Activision Blizzard ($69 billion) were the largest deals ([Wikipedia](https://en.wikipedia.org/wiki/List_of_mergers_and_acquisitions_by_Microsoft){:target="_blank"}), and each shows up as a step in the line. Activision alone accounts for the jump in fiscal 2024, which is also the main reason the cash balance fell from its 2020 level.

## Capital Spending Rose From 6% to 23% of Revenue

Free cash flow is the cash from operations minus capital expenditure, the money left after maintaining and expanding the asset base. It is harder to flatter than earnings, and it is what pays for dividends and buybacks.

Operating cash flow, capital expenditure and free cash flow at five-year intervals:

{% capture code_fcf %}
```python
# pip install financetoolkit
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["MSFT"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="1986-01-01")

cash_flow = toolkit.get_cash_flow_statement()
cash_flow = cash_flow.loc[["Operating Cash Flow", "Capital Expenditure", "Free Cash Flow"], ["1995", "2000", "2005", "2010", "2015", "2020", "2025"]]
```
{% endcapture %}
{% include ft-chart.html id="msft-fcf" src="/assets/data/article-charts.json" label="Microsoft free cash flow" code=code_fcf mcp="What were Microsoft's operating cash flow, capital expenditure and free cash flow in 1995, 2000, 2005, 2010, 2015, 2020 and 2025?" %}

Microsoft generated $72 billion in free cash flow in fiscal 2025. It comes from subscription and consumption revenue that grows without a matching rise in costs, and from customers who rarely leave once their work runs on Microsoft's software. That is my reading of it, as the cash flow statement shows how much cash came in but says nothing about why.

However, capital expenditure rose more than tenfold between 2015 and 2025, most of it on data centres for Azure and AI services, and went from 6% of revenue to 23%.

Operating cash flow has grown fast enough to absorb it, but in 2015 about 80% of operating cash flow was left as free cash flow, and in 2025 only 53%. Whether this spending earns a return close to the old software business is the main capital allocation question for Microsoft, and the free cash flow line is where it shows first.

## Financing Lifted ROE and Inflation Lifted Growth

A forty-year record of one company has a few traps of its own, and the return on equity is the first. Return on equity (ROE) and return on assets (ROA) divide net income by shareholders' equity and by total assets. Return on invested capital (ROIC) divides operating income after tax by all the capital in the business, debt plus equity. The gap between ROE and ROIC gives a rough idea of how much of the return to shareholders comes from the way the company is financed.

Return on equity, assets and invested capital per fiscal year:

{% capture code_returns %}
```python
# pip install financetoolkit
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["MSFT"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="1986-01-01")

profitability_ratios = toolkit.ratios.collect_profitability_ratios()
returns = profitability_ratios.loc[["Return on Equity", "Return on Assets", "Return on Invested Capital"], "1987":"2025"]
```
{% endcapture %}
{% include ft-chart.html id="msft-returns" src="/assets/data/article-charts.json" label="Microsoft ROE, ROA and ROIC" code=code_returns mcp="What were Microsoft's return on equity, return on assets and return on invested capital in every fiscal year from 1987 to 2025?" %}

In the early years the three lines sit close together. With no debt, an ROE of 38% in 1990 meant the business itself was that profitable, and ROIC was 35%. That changed after 2014. Debt more than tripled between 2014 and 2019 while buybacks and dividends kept the equity base from growing much, and ROE pulled away from ROIC.

**In 2019 ROE was 42% and ROIC 22%, a gap of 21 points that came from the way Microsoft was financed.** Since then Microsoft has paid down debt and its equity has grown with retained earnings, and by 2025 the gap had narrowed to 7.5 points.

That leaves an ROIC of 26% in 2025, which is high for a company of this size but below the 35% or more of 1990 to 1992. Return on assets says the same: it fell from 31% in 1990 to 18% in 2025, as data centres and acquisitions made the asset base much heavier than that of a software company.

Single years with a one-off charge are the second trap. In fiscal 2018 Microsoft paid 55% of its pre-tax profit in tax, against 15% the year before, because of the charge from the US tax reform. At the 2017 tax rate its net margin would have been 28% instead of 15%.

The charge also reaches ratios that look unrelated. ROIC taxes operating income at that same 55% rate, so it drops to 9% in 2018, and the price-to-earnings ratio in the next chart jumps to 48 at the end of that year because the earnings fell. The Nokia write-down does the same to 2015, and any average or median over these years carries both. Fiscal 2019 errs the other way, as its tax rate of 10% flatters both ROE and ROIC in the year their gap was widest.

The third trap is inflation, as a dollar of revenue in 1986 bought far more than one in 2025. Deflated by the US consumer price index, the 1,400-fold rise in revenue becomes about 490-fold in 2025 dollars, and the 40% a year under Gates becomes 36%.

Rerun in real terms, the finding of the first section holds. In real terms revenue grew 7.4% a year under Ballmer and 8.3% under Nadella, against 10% and 11% in nominal terms, so the two eras stay about a point apart. Inflation was a little higher under Nadella, which takes slightly more off his figure.

## Looking Ahead

Next to the financial history, the valuation shows what the market expects from Microsoft, and the company's own past gives a useful scale for it.

The price-to-earnings and price-to-free-cash-flow ratios, measured at the end of each year:

{% capture code_valuation %}
```python
# pip install financetoolkit
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["MSFT"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="1986-01-01")

valuation_ratios = toolkit.ratios.collect_valuation_ratios()
valuation = valuation_ratios.loc[["Price-to-Earnings", "Price-to-Free-Cash-Flow"], "1989":"2025"]
```
{% endcapture %}
{% include ft-chart.html id="msft-valuation" src="/assets/data/article-charts.json" label="Microsoft price-to-earnings and price-to-free-cash-flow ratios" code=code_valuation mcp="What were Microsoft's price-to-earnings and price-to-free-cash-flow ratios in every year from 1989 to 2025?" %}

At the end of 2025 the shares traded at 35.5 times earnings, close to their median of 33 since 1989. The price-to-free-cash-flow ratio of 50 is far above its median of 28 and the highest since 1999. The gap between the two ratios is the capital spending shown earlier: free cash flow has fallen behind earnings. The ratio can come down in two ways: free cash flow catches up as the spending starts to pay off, or the share price falls.

Beta measures how much the stock moves with the S&P 500 (1 means in line). The return versus the S&P 500 is the stock's return in the year minus that of the index, in percentage points:

| Metric | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|--------|------|------|------|------|------|------|
| Beta | 1.15 | 1.16 | 1.28 | 1.17 | 1.19 | 0.88 |
| Return vs S&P 500 | +24 | +24 | -10 | +32 | -12 | -2 |

For most of the Nadella era the stock moved slightly more than the market. In 2025 its beta fell to 0.88, so the market treated it more like a defensive holding than before. Microsoft beat the index in three of these six years, by the most in 2023 (32 points), and lagged it in 2022 and 2024 while the business kept growing.

What I would watch from here are three ratios from the charts above: capital expenditure as a share of revenue, the share of operating cash flow left as free cash flow, and ROIC. As the Ballmer years show, a long record of growth says little on its own about the return to shareholders, which also depends on the price paid at the start. Like any company history, these ratios describe what has happened and what the price assumes, and they are no forecast of the share price.

### Data and method

- **Source:** Microsoft's annual income statements, balance sheets and cash flow statements for fiscal 1986 to 2025, and daily share prices of Microsoft and the S&P 500 ETF (SPY) to the end of 2025, all from [FinancialModelingPrep](/fmp){:target="_blank"}. The US consumer price index is the Bureau of Labor Statistics' CPI-U, monthly, as published by the Bank for International Settlements. The IPO date and offer price, the Nokia write-down and the acquisition prices are from Wikipedia.
- **How the series is built:** Microsoft's fiscal year ends on June 30, so "2025" is July 2024 to June 2025. The valuation ratios divide the share price at the end of the calendar year by the earnings or free cash flow per share of the fiscal year that ended that June.
- **What I did to it:** growth per year in the table is the compound annual rate between the first and last fiscal year of each era. For the real figures I averaged the monthly consumer price index over each July to June fiscal year and restated revenue in fiscal 2025 dollars. The 2018 net margin at the 2017 tax rate is the pre-tax margin of 2018 times one minus the effective tax rate of 2017. The cash flow chart shows capital expenditure as negative values, as the cash flow statement reports it, and keeps every fifth year. The ROE, ROA and ROIC chart starts in 1987 because the averages need the balance sheet of the year before. The total return of the shares uses year-end prices adjusted for splits and dividends, from the end of 1986 (the first year-end after the IPO), 1999 and 2013 (the year-ends before Ballmer and Nadella took over) to the end of the era. ROE and ROA use average equity and assets. ROIC is operating income taxed at the effective tax rate, divided by average debt plus equity, without deducting cash. The medians of the two valuation ratios are taken over 1989 to 2025. Beta is calculated each calendar year from daily returns against SPY.
- **Limits:** the 2015 and 2018 figures carry large one-off charges, so single years can mislead. The IPO comparison uses the $21 offer price adjusted for later stock splits. The full 40 years need a paid FinancialModelingPrep plan, as the free plan covers five years.
- **Reproduce it:** the charts are made with the [Finance Toolkit](/projects/financetoolkit), my open-source Python library, using its [financial statements](/projects/financetoolkit/docs), [ratios](/projects/financetoolkit/docs/ratios) and, for beta and the returns in the tables, [performance](/projects/financetoolkit/docs/performance) modules. The Python button on each chart shows the code and its MCP button a question that returns the same data.
- **Further reading:** Aswath Damodaran, [Return on Capital (ROC), Return on Invested Capital (ROIC) and Return on Equity (ROE): Measurement and Implications](https://pages.stern.nyu.edu/~adamodar/pdfiles/papers/returnmeasures.pdf){:target="_blank"} (2007), on how these returns are measured and why dividends and buybacks lift the return on equity. Microsoft's [2015 Annual Report](https://www.microsoft.com/investor/reports/ar15/index.html){:target="_blank"} and [2018 Annual Report](https://www.microsoft.com/investor/reports/ar18/index.html){:target="_blank"}, which set out the impairment charges on the phone business and the $13.7 billion net charge from the US tax reform.

{% include ft-charts-script.html %}
