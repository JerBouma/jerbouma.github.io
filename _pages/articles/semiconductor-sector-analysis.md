---
title: "Semiconductor Sector Analysis: How NVIDIA Overtook Intel"
seo_title: "Semiconductor Sector Analysis: NVIDIA, Intel and AMD"
date: 2026-07-07
last_modified_at: 2026-11-18
permalink: /articles/semiconductor-sector-analysis-finance-toolkit
excerpt: "In 2010 Intel earned 54% of the combined revenue of six large US chipmakers and NVIDIA 4%. By 2025 NVIDIA earned half, and gross margins and return on capital show how it happened."
description: "Semiconductor sector analysis from 2010 to 2025: revenue, gross margins, ROIC and valuation multiples of Intel, AMD, NVIDIA, Qualcomm, Broadcom and TI."
layout: single
classes: wide-sidebar article-document
author_profile: false
collection: article
tags: [Fundamental Analysis]
share: true
cover:
  image: /assets/images/articles/semiconductor-sector-analysis/cover.jpg
  alt: "A microscope photograph of a processor die, a dense grid of cache blocks and logic."
  credit: "Pentium II die shot, Martijn Boer, public domain"
  link: "https://commons.wikimedia.org/wiki/File:Intel-pentium-ii-dixon-die-shot-high-resolution-stitched.jpg"
---

In 2010, Intel earned 54% of the combined revenue of six large US chipmakers: Intel, AMD, NVIDIA, Qualcomm, Broadcom and Texas Instruments. NVIDIA, then best known for gaming graphics cards, earned 4%. By 2025 the order had flipped, with NVIDIA earning half of the group's revenue and Intel 12%.

How does a sector change hands that quickly? The financial statements show it happened in two steps. First, Intel's gross margin nearly halved as its own factories fell behind the contract manufacturers that AMD, NVIDIA and the other chip designers use. Then, from 2023, demand for AI training hardware gave NVIDIA a return on invested capital that no other company in the group came close to. For Intel and AMD the margin moved before the revenue did, which is why gross margin and return on capital are the first numbers I would check when competition in an industry starts to shift. I follow the six companies through the annual statements in their filings from 2010 to 2025.

## NVIDIA Went From 4% to Half of the Group's Revenue

Revenue is the simplest way to see who matters in a sector. NVIDIA's fiscal year ends in late January, so its 2025 runs to January 2026.

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

# sensitivity check: NVIDIA's four quarters to October 2025 instead of its fiscal year to January 2026
nvidia = Toolkit(tickers=["NVDA"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2024-10-01", quarterly=True)
nvidia_income = nvidia.get_income_statement()
nvidia_quarters = nvidia_income.loc["Revenue"] / 1e9
shifted = revenue["2025"].copy()
shifted["NVDA"] = nvidia_quarters["2024Q4":"2025Q3"].sum()
shifted_share = shifted / shifted.sum()

# the 2010 base with Broadcom Corporation and Xilinx, which Broadcom (then Avago) and AMD bought later
acquired = Toolkit(tickers=["BRCM", "XLNX"], api_key="FINANCIAL_MODELING_PREP_KEY", start_date="2010-01-01")
acquired_income = acquired.get_income_statement()
acquired_revenue = acquired_income.xs("Revenue", level=1)["2010"] / 1e9
base_2010 = revenue["2010"].sum() + acquired_revenue.sum()
intel_share_2010 = revenue.loc["INTC", "2010"] / base_2010
amd_share_2010 = (revenue.loc["AMD", "2010"] + acquired_revenue["XLNX"]) / base_2010
broadcom_growth = revenue.loc["AVGO", "2025"] / (revenue.loc["AVGO", "2010"] + acquired_revenue["BRCM"])
```
{% endcapture %}
{% include ft-chart.html id="semis-revenue" src="/assets/data/article-charts.json" label="Semiconductor revenue" code=code_revenue mcp="What was the annual revenue of Intel, AMD, NVIDIA, Qualcomm, Broadcom and Texas Instruments since 2010, and what share of their combined revenue did each company have in 2010 and in 2025?" %}

Intel's revenue peaked around 2020 and had shrunk by about a third by 2025. NVIDIA grew from $27.0 billion in 2022 to $215.9 billion in 2025, about 2.7 times what all six companies earned together in 2010. Broadcom's jump between 2014 and 2018 came mostly from acquisitions, as Avago Technologies bought LSI, Broadcom Corporation, whose name it took, and Brocade.

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

NVIDIA went the other way, from 40% in 2010 to 71% in 2025, after a peak of 75% in 2024. With almost no competition in AI training hardware, it could charge what customers would pay.

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

## AMD Caught Intel, but NVIDIA Earned 86% on Its Capital

Not every company here competes with every other, as Texas Instruments, Qualcomm and Broadcom mostly sell analog, phone and networking chips. The real contests are Intel against AMD in x86 processors, which run most PCs and servers, and AMD against NVIDIA in graphics chips, a market AMD entered when it bought ATI Technologies in 2006.

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

From 2010 to 2017 Intel led on every measure. AMD lost money in most of those years, and its gross margin fell from 46% in 2010 to 33% in 2014. The turn came in 2017, when AMD launched its Zen architecture under Lisa Su, with Ryzen processors for PCs and EPYC for servers. AMD's margin recovered first and its revenue followed from 2020.

Intel's gross margin was already sliding, from 62% in 2018 to 56% in 2020, while its revenue was still growing. In 2022 AMD's gross margin passed it, 44.9% against 42.6%, and stayed ahead in every year after that. By 2025 the money Intel spent on building its own foundry business had not brought its margins back, and its ROIC was about zero.

AMD's ROIC is low too, but for another reason. It fell from 27.6% in 2020 to 3.8% in 2022, the year AMD closed its all-stock purchase of Xilinx, announced at $35 billion. Paying in shares added tens of billions of dollars to AMD's equity, which is part of the capital ROIC divides by, and the amortisation of Xilinx's intangible assets lowers its operating profit every year.

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

Until 2022 the two moved roughly in parallel. NVIDIA overtook AMD on revenue between 2014 and 2018, and in 2020 AMD even had the higher ROIC, 27.6% against 22.6%, because its capital base was still small before the Xilinx deal. The split came from 2023, when NVIDIA's H100 and later Blackwell GPUs became the default hardware for training large language models. Most of that software is written for CUDA, NVIDIA's programming platform since 2007, and AMD's own platform, ROCm, had not caught up by 2025.

**NVIDIA earned 86% on its invested capital in 2025, after 98% in 2024, against 6% for AMD.** Both companies sell GPUs, so I would put most of that gap down to the software and the customers built around NVIDIA's chips. That is my reading, as the statements show how large the gap is and when it opened, but not what caused it.

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

NVIDIA, the most profitable business of the six, traded below AMD and Broadcom on both measures, and its P/E was only a few points above Qualcomm's 34.1x and Texas Instruments' 31.9x.

Qualcomm had the lowest EV/EBITDA of the group at 13.8x, which fits a business with less exposure to AI spending. Intel's small loss in 2025 gives a P/E of -626, which the chart leaves out. Its EV/EBITDA of 19.8x was well above Qualcomm's while its ROIC was about zero, so the price counts on a recovery that had not shown up in the statements by 2025.

## NVIDIA's Late Fiscal Year and Takeovers Shift the Shares

The first trap is the calendar. NVIDIA's 2025 runs to 25 January 2026, a month past the years of Intel, AMD and Texas Instruments. Its quarterly revenue rose from $39.3 billion to $68.1 billion over that year, so moving the window by a quarter changes the total.

**Counting NVIDIA's four quarters to October 2025 instead lowers its 2025 share from 50.3% to 46.7%, still close to three times Broadcom's.** The order of the six doesn't change, but 'half' depends on which twelve months count as NVIDIA's 2025.

The second trap is the 2010 base. I picked the six because they are large today, and their 2010 figures leave out companies they bought later. Broadcom Corporation, which Avago bought in 2016, earned $6.8 billion in 2010 and Xilinx $2.4 billion. Both are inside Broadcom's and AMD's 2025 revenue but not in their 2010 figures. With Broadcom Corporation counted in 2010, Broadcom's revenue grew about 7 times by 2025 rather than 30 times.

Adding the two to the 2010 total lowers Intel's share that year from 54.0% to 48.5%. AMD, with Xilinx counted at both ends, went from 9.9% of the group to 8.1%, a small loss where the table shows a flat share.

## What This Means for Sector Analysis

The six companies share a label, but only two pairs compete head to head, so comparing each company with its real rival says more than comparing it with the sector. In both pairs the gross margin and ROIC showed the direction before revenue did.

When I look at this group again, I would start with Intel's gross margin next to AMD's, which shows whether Intel's foundry spending is closing the cost gap. Next to that, NVIDIA's gross margin and ROIC are where pressure from competitors, or from customers designing their own AI chips, would show up first. For AMD, ROIC is the number to follow as the Xilinx amortisation runs off. The multiples only show what the market priced in at the end of 2025, and nothing in the statements says whether that will prove right.

### Data and method

- **Source:** annual income statements, balance sheets and ratios of Intel, AMD, NVIDIA, Qualcomm, Broadcom and Texas Instruments from the companies' filings via FinancialModelingPrep, fiscal years 2010 to 2025, retrieved on 18 November 2026. The valuation multiples also use share prices from FinancialModelingPrep, and the checks on the revenue shares use NVIDIA's quarterly statements and the 2010 statements of Broadcom Corporation and Xilinx.
- **How the series is built:** each year is a company's fiscal year, labelled by the calendar year it mostly falls in. Intel, AMD and Texas Instruments report on calendar years, Qualcomm's year ends in late September, Broadcom's in early November and NVIDIA's in late January.
- **What I did to it:** Every NVIDIA year is labelled one year lower than in NVIDIA's own reports (its fiscal 2026 is 2025 here), and Xilinx's year to April 2011 is 2010. Revenue is converted to billions of US dollars, not adjusted for inflation, and the revenue shares divide each company's revenue by the six companies' total for that year. Gross margins are averaged over 2010 to 2014 and 2021 to 2025 in the second table. ROIC is operating income taxed at the effective tax rate, divided by average equity plus average debt. The multiples use the share price at the end of each fiscal year, and Intel's negative 2025 P/E is dropped from the chart.
- **Limits:** the group is six US companies. TSMC, Samsung and the equipment makers are left out, so the revenue shares are shares of these six.
- **Reproduce it:** the charts are made with the [Finance Toolkit](/projects/financetoolkit), my open-source Python library, using its [ratios module](/projects/financetoolkit/docs/ratios) and data from [FinancialModelingPrep](/fmp){:target="_blank"} (the full history from 2010 needs a paid plan). The Python button on each chart shows the code and its MCP button a question that returns the same data.
- **Further reading:** Aswath Damodaran (2007), [Return on Capital (ROC), Return on Invested Capital (ROIC) and Return on Equity (ROE): Measurement and Implications](https://pages.stern.nyu.edu/~adamodar/pdfiles/papers/returnmeasures.pdf){:target="_blank"}, NYU Stern, on how goodwill and acquisition accounting lower returns on capital for years after a deal. AMD (2022), [AMD Completes Acquisition of Xilinx](https://ir.amd.com/news-events/press-releases/detail/1047/amd-completes-acquisition-of-xilinx){:target="_blank"}, with the all-stock terms. NVIDIA (2026), [NVIDIA Announces Financial Results for Fourth Quarter and Fiscal 2026](https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-fourth-quarter-and-fiscal-2026){:target="_blank"}, for the year that ended on 25 January 2026.

{% include ft-charts-script.html %}
