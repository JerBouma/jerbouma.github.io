---
title: "Semiconductor Sector Analysis: How NVIDIA Overtook Intel"
seo_title: "Semiconductor Sector Analysis: NVIDIA, Intel and AMD"
date: 2026-07-07
last_modified_at: 2026-11-17
permalink: /articles/semiconductor-sector-analysis-finance-toolkit
excerpt: "In 2010 Intel earned 54% of the combined revenue of six large US chipmakers and NVIDIA 4%. By 2025 NVIDIA earned half, and gross margins and return on capital show how it happened."
description: "Semiconductor sector analysis from 2010 to 2025: revenue, gross margins, ROIC and valuation multiples of Intel, AMD, NVIDIA, Qualcomm, Broadcom and TI."
layout: single
classes: wide-sidebar article-document
author_profile: false
collection: article
tags: [Fundamental Analysis]
share: true
---

In 2010, Intel earned 54% of the combined revenue of six large US chipmakers: Intel, AMD, NVIDIA, Qualcomm, Broadcom and Texas Instruments. NVIDIA, then best known for gaming graphics cards, earned 4%. By 2025 the order had flipped, with NVIDIA earning half of the group's revenue and Intel 12%.

How does a sector change hands that quickly? The financial statements show it happened in two steps. First, Intel's gross margin nearly halved as its own factories fell behind the contract manufacturers that AMD, NVIDIA and the other chip designers use. Then, from 2023, demand for AI training hardware gave NVIDIA a return on invested capital that no other company in the group came close to. For Intel and AMD the margin moved before the revenue did, which is why gross margin and return on capital are the first numbers I would check when competition in an industry starts to shift. I follow the six companies through the annual financial statements in their filings from 2010 to 2025, and end with their valuation multiples for 2025.

## NVIDIA Went From 4% to Half of the Group's Revenue

Revenue is the simplest way to see who matters in a sector. One thing to know about the years: NVIDIA's fiscal year ends in late January and is labelled by the calendar year it mostly falls in, so NVIDIA's 2025 is the fiscal year that ended in January 2026.

Revenue per company in 2010, 2014, 2018, 2022 and 2025, in billions of dollars:

{% capture code_revenue %}
```python
# pip install financetoolkit
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["INTC", "AMD", "NVDA", "QCOM", "AVGO", "TXN"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2010-01-01")

income = toolkit.get_income_statement()
revenue = income.xs("Revenue", level=1)[["2010", "2014", "2018", "2022", "2025"]] / 1e9

# each company's share of the six companies' combined revenue
share = revenue / revenue.sum()
```
{% endcapture %}
{% include ft-chart.html id="semis-revenue" src="/assets/data/article-charts.json" label="Semiconductor revenue" code=code_revenue mcp="What was the annual revenue of Intel, AMD, NVIDIA, Qualcomm, Broadcom and Texas Instruments since 2010, and what share of their combined revenue did each company have in 2010 and in 2025?" %}

Until 2022 this looks like an ordinary cyclical industry. Intel's revenue peaked around 2020 and had shrunk by about a third by 2025. NVIDIA grew from $27.0 billion in 2022 to $215.9 billion in 2025, about 2.7 times what all six companies earned together in 2010. Broadcom's growth looks smooth in the chart, but most of its jump between 2014 and 2018 came from acquisitions, as Avago Technologies bought LSI, then Broadcom Corporation, whose name it took, and then Brocade.

Each company's share of the group's combined revenue:

| Company | 2010 | 2025 |
|---|---|---|
| Intel | 54.0% | 12.3% |
| NVIDIA | 4.4% | 50.3% |
| Broadcom | 2.6% | 14.9% |
| Qualcomm | 13.6% | 10.3% |
| AMD | 8.0% | 8.1% |
| Texas Instruments | 17.3% | 4.1% |
| Combined revenue | $80.7 billion | $429.3 billion |

**NVIDIA went from 4% of the group's revenue in 2010 to half of it in 2025, while Intel went from 54% to 12%.** AMD, for all its progress against Intel, had about the same share at both ends of the period. Texas Instruments, which sells analog chips into slower-growing industrial and car markets, shrank to the smallest share of the six.

## Intel's Gross Margin Fell From 66% to 35%

Gross margin is the share of revenue left after the direct cost of making the chips, so it shows both pricing power and how cheaply a company can produce. Here the sector splits in two: integrated device manufacturers such as Intel and Texas Instruments design and make their own chips, while fabless companies such as NVIDIA, AMD and Qualcomm design them and pay a foundry like TSMC to make them.

The gross margin of each company over the same years:

{% capture code_margins %}
```python
# pip install financetoolkit
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["INTC", "AMD", "NVDA", "QCOM", "AVGO", "TXN"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2010-01-01")

gross_margin = toolkit.ratios.get_gross_margin()
margins = gross_margin[["2010", "2014", "2018", "2022", "2025"]]

# the five-year averages in the table
first_five = gross_margin.loc[:, "2010":"2014"].mean(axis=1)
last_five = gross_margin.loc[:, "2021":"2025"].mean(axis=1)
```
{% endcapture %}
{% include ft-chart.html id="semis-margins" src="/assets/data/article-charts.json" label="Semiconductor gross margins" code=code_margins mcp="Show the gross margins of Intel, AMD, NVIDIA, Qualcomm, Broadcom and Texas Instruments since 2010, and the average of each over 2010 to 2014 and over 2021 to 2025." %}

**Intel's gross margin fell from 66% in 2010 to 35% in 2025, the largest move in the chart.** The main cause is that Intel's own processes fell behind TSMC's, first by one process generation and then by two, so its chips cost more to make while competitors that use TSMC got better processes at a lower cost.

NVIDIA went the other way, from 40% in 2010 to 71% in 2025, after a peak of 75% in 2024. Its 2025 margin is above Intel's best year in the data. A company with almost no competition in AI training hardware can charge what customers will pay, and they have paid a lot for its H100 and Blackwell GPUs.

Single years are noisy, as write-downs and product cycles move a margin by several points, so the table compares the averages of the first and the last five years:

| Company | Makes its own chips | 2010 to 2014 | 2021 to 2025 |
|---|---|---|---|
| Intel | Yes | 62.9% | 41.1% |
| Texas Instruments | Yes | 52.3% | 62.9% |
| NVIDIA | No | 50.7% | 68.1% |
| Broadcom | Mostly not | 47.0% | 65.5% |
| AMD | No | 36.8% | 47.6% |
| Qualcomm | No | 63.7% | 56.5% |

Texas Instruments makes its own chips too, and its average margin rose by more than ten points, as analog chips don't need the most advanced processes. Next to that, Qualcomm, which is fabless, saw its average margin fall. Intel's problem was being behind at the leading edge, where each new process costs the most, and owning the factories meant it carried that cost itself.

## AMD Passed Intel on Gross Margin in 2022

Not every company here competes with every other. Texas Instruments sells analog chips to industrial and car makers, Qualcomm sells ARM-based processors for phones and Broadcom sells networking and storage chips. In x86 processors, which run most PCs and servers, the competition is between Intel and AMD, so the market share one gains, the other loses.

Return on invested capital (ROIC) is after-tax operating profit divided by the equity and debt invested in the business, so it shows how much a company earns on the money tied up in it.

Revenue, gross margin and ROIC of Intel and AMD, each in its own tab:

{% capture code_intc_amd %}
```python
# pip install financetoolkit
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["INTC", "AMD"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2010-01-01")

years = ["2010", "2014", "2018", "2020", "2022", "2024", "2025"]

income = toolkit.get_income_statement()
revenue = income.xs("Revenue", level=1)[years] / 1e9
gross_margin = toolkit.ratios.get_gross_margin()[years]
roic = toolkit.ratios.get_return_on_invested_capital()[years]
```
{% endcapture %}
{% include ft-chart.html id="semis-intc-amd" src="/assets/data/article-charts.json" label="Intel versus AMD" code=code_intc_amd mcp="Compare Intel and AMD's revenue, gross margin and return on invested capital since 2010. When did AMD first surpass Intel on gross margin?" %}

From 2010 to 2017 Intel led on every measure. AMD lost money in most of those years and competed on price with weaker products, and its gross margin fell from 46% in 2010 to 33% in 2014.

The turn came in 2017, when AMD launched its Zen architecture under Lisa Su, with Ryzen processors for PCs and EPYC for servers. The statements lag the products: AMD's margin recovered first and its revenue followed from 2020, as more of its sales came from EPYC. Intel's gross margin was already sliding, from 62% in 2018 to 56% in 2020, while its revenue was still growing.

**In 2022 AMD's gross margin passed Intel's, 44.9% against 42.6%, and it stayed ahead in every year after that.** Intel's ROIC fell to -7.4% in 2024 and was about zero in 2025, a year with a small net loss. By 2025 the money Intel spent on building its own foundry business had not brought its margins back.

AMD's ROIC is low too, but for another reason. It fell from 27.6% in 2020 to 3.8% in 2022, the year AMD closed its all-stock purchase of Xilinx, announced at $35 billion. Paying in shares added tens of billions of dollars to AMD's equity, which is part of the capital ROIC divides by, and the amortisation of Xilinx's intangible assets lowers its operating profit every year, so much of the drop in the ratio comes from the deal itself.

## NVIDIA Earned 86% on Its Capital, AMD 6%

AMD and NVIDIA have competed in graphics chips since AMD bought ATI Technologies in 2006. Both design GPUs for gaming, workstations and data centres, and in 2010 AMD was the larger of the two, with $6.5 billion of revenue against NVIDIA's $3.5 billion.

The same three measures for NVIDIA and AMD:

{% capture code_nvda_amd %}
```python
# pip install financetoolkit
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["NVDA", "AMD"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2010-01-01")

years = ["2010", "2014", "2018", "2020", "2022", "2024", "2025"]

income = toolkit.get_income_statement()
revenue = income.xs("Revenue", level=1)[years] / 1e9
gross_margin = toolkit.ratios.get_gross_margin()[years]
roic = toolkit.ratios.get_return_on_invested_capital()[years]
```
{% endcapture %}
{% include ft-chart.html id="semis-nvda-amd" src="/assets/data/article-charts.json" label="NVIDIA versus AMD" code=code_nvda_amd mcp="Compare NVIDIA and AMD's revenue, gross margin and return on invested capital since 2010. How large is the ROIC gap in 2025?" %}

Until 2022 the two moved roughly in parallel. NVIDIA overtook AMD on revenue between 2014 and 2018, and in 2020 AMD even had the higher ROIC, 27.6% against 22.6%, because its capital base was still small before the Xilinx deal.

The split came from 2023 onwards, with demand for hardware to train AI models. NVIDIA's H100 and later Blackwell GPUs became the default hardware for training large language models, partly because most of that software is written for CUDA, NVIDIA's programming platform since 2007. AMD's own platform, ROCm, could not make up that head start quickly.

**NVIDIA earned 86% on its invested capital in 2025, after 98% in 2024, against 6% for AMD.** Both companies sell GPUs, so most of that gap comes from the software and the customers built around NVIDIA's chips.

For AMD this is a harder contest than the one with Intel. Against Intel it competes on processor performance, which is a matter of engineering. Against NVIDIA it has to win over developers who have already built on CUDA, which takes longer and costs more.

## AMD Traded at Twice NVIDIA's P/E in 2025

The price-to-earnings ratio (P/E) is the share price divided by earnings per share. EV/EBITDA compares the value of the whole company, debt included, with its operating profit before depreciation and amortisation, so it depends less on how a company is financed and on acquisition accounting. Both are snapshots at the end of each company's 2025 fiscal year and move with the share price.

The P/E and EV/EBITDA ratios of the six companies for 2025:

{% capture code_valuation %}
```python
# pip install financetoolkit
from financetoolkit import Toolkit

toolkit = Toolkit(tickers=["INTC", "AMD", "NVDA", "QCOM", "AVGO", "TXN"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2010-01-01")

pe = toolkit.ratios.get_price_to_earnings_ratio()["2025"]
pe = pe[pe > 0]  # a loss gives a negative P/E, which is left out
ev_ebitda = toolkit.ratios.get_ev_to_ebitda_ratio()["2025"]
```
{% endcapture %}
{% include ft-chart.html id="semis-valuation" src="/assets/data/article-charts.json" label="Semiconductor valuation multiples" code=code_valuation mcp="What were the P/E and EV/EBITDA ratios of Intel, AMD, NVIDIA, Qualcomm, Broadcom and Texas Instruments for fiscal 2025, which for NVIDIA ends in January 2026, and which company is the cheapest on each, leaving out a negative P/E?" %}

**AMD's P/E of 80.8x was more than twice NVIDIA's 38.1x, even though NVIDIA earned far more on its capital.** Part of that is the Xilinx amortisation, which lowers AMD's earnings. AMD was also the most expensive on EV/EBITDA at 51.4x, a measure taken before amortisation, so its price assumes a lot of growth, from AI GPUs and from a recovery in its return on capital.

NVIDIA, the most profitable business of the six, traded below AMD and Broadcom on both measures, and its P/E was only a few points above Qualcomm's 34.1x and Texas Instruments' 31.9x. Its multiples rest on AI spending staying high and on NVIDIA keeping its software lead.

Qualcomm had the lowest EV/EBITDA of the group at 13.8x, which fits a business with less exposure to AI spending. Intel can't be valued on P/E: its small loss in 2025 gives a P/E of -626, so the chart leaves it out. Its EV/EBITDA of 19.8x was well above Qualcomm's while its ROIC was about zero, so the price counts on a recovery that had not shown up in the statements by 2025.

## What This Means for Sector Analysis

The six companies share a label, but only two pairs compete head to head, so comparing each company with its real rival says more than comparing it with the sector. In both pairs the gross margin and ROIC showed the direction before revenue did. Intel's margin was falling while its revenue still grew, and AMD's margin recovered before its sales took off.

When I look at this group again, I would start with Intel's gross margin next to AMD's, which shows whether Intel's foundry spending is closing the cost gap. Next to that, NVIDIA's gross margin and ROIC are where pressure from competitors, or from customers designing their own AI chips, would show up first. For AMD, ROIC is the number to follow as the Xilinx amortisation runs off, since that recovery is part of what its multiple assumes. The multiples only show what the market priced in at the end of 2025, and nothing in the statements says whether that will prove right.

### Data and method

- **Source:** annual income statements, balance sheets and ratios of Intel, AMD, NVIDIA, Qualcomm, Broadcom and Texas Instruments from the companies' filings via FinancialModelingPrep, fiscal years 2010 to 2025, retrieved on 17 November 2026. The valuation multiples also use share prices from FinancialModelingPrep.
- **How the series is built:** each year is a company's fiscal year, labelled by the calendar year it mostly falls in. Intel, AMD and Texas Instruments report on calendar years, Qualcomm's year ends in late September, Broadcom's in early November and NVIDIA's in late January.
- **What I did to it:** revenue is in billions of US dollars, and the revenue shares are each company's revenue divided by the six companies' total for that year. Gross margin is gross profit over revenue, averaged over 2010 to 2014 and 2021 to 2025 in the second table. ROIC is operating income taxed at the effective tax rate, divided by average equity plus average debt. The multiples use the share price at the end of each fiscal year.
- **Limits:** the group is six US companies. TSMC, Samsung and the equipment makers are left out, so the revenue shares are shares of these six. Acquisitions (Broadcom, AMD) and write-downs move the ratios.
- **Reproduce it:** the charts are made with the [Finance Toolkit](/projects/financetoolkit), my open-source Python library, using its [ratios module](/projects/financetoolkit/docs/ratios) and data from [FinancialModelingPrep](/fmp){:target="_blank"} (the full history from 2010 needs a paid plan). The Python button on each chart shows the code and its MCP button a question that returns the same data.

{% include ft-charts-script.html %}
