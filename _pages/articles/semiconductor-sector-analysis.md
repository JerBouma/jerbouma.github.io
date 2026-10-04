---
title: Competitor and Sector Analysis with the Finance Toolkit
date: 2026-07-07
last_modified_at: 2026-10-02
permalink: /articles/semiconductor-sector-analysis-finance-toolkit
excerpt: "The semiconductor sector from 2010 to 2025 through the Finance Toolkit: how revenue shifted, why gross margins drifted apart, and the two real competitive battles in the industry, Intel vs AMD and NVIDIA vs AMD."
description: "Semiconductor sector analysis with the Finance Toolkit in Python: revenue, margins and ROIC across Intel, AMD, NVIDIA, Qualcomm, Broadcom and TI."
layout: single
classes: wide-sidebar article-document
author_profile: false
collection: article
tags: [Fundamental Analysis]
share: true
---

In 2010, Intel generated $43.6 billion in revenue and its nearest competitor in logic chips, AMD, generated $6.5 billion. NVIDIA was a $3.3 billion company still best known for gaming graphics cards. Qualcomm was growing rapidly on the smartphone wave. Broadcom and Texas Instruments were mid-sized analog and connectivity specialists.

By 2025 the same six companies look very different. NVIDIA has grown to $130.5 billion in revenue driven almost entirely by AI infrastructure demand. Intel sits at $52.9 billion, down from its 2020 peak of $77.9 billion, and is now reporting losses. AMD has reached $34.6 billion and crossed Intel's gross margin for the first time in the company's history.

In this article I track that shift through the financial data with the Finance Toolkit, both in Python and through the MCP server for those who prefer to work conversationally.

**For more information on Finance Toolkit, have a look [here](https://github.com/JerBouma/FinanceToolkit){:target="_blank"}. To run the same analysis conversationally, explore the [Finance Toolkit MCP server](/projects/financetoolkit/mcp).**

> **Try this with the Finance Toolkit MCP:** *"Let's do a deep dive in the Semiconductor industry. What trends do you see in the last 10 years? And what about the fundamentals?"*

## Setting Things Up

Start by installing the Finance Toolkit:

```bash
pip install financetoolkit
```

Then import the library and define a universe of tickers. The example below uses six semiconductor companies: Intel, AMD, NVIDIA, Qualcomm, Broadcom, and Texas Instruments.

```python
import pandas as pd
from financetoolkit import Toolkit

sector = Toolkit(
    tickers=["INTC", "AMD", "NVDA", "QCOM", "AVGO", "TXN"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2010-01-01"
)
```

Get your FMP API key at [jeroenbouma.com/fmp](/fmp){:target="_blank"}. A paid plan is required to access the full 15-year history used here.

## Revenue: How the Landscape Shifted

When you pull 15 years of income statements, the first thing you notice is NVIDIA's revenue. Compared to it, everything else looks like normal cyclical variation.

```python
income = sector.get_income_statement()

revenue = income.loc["Revenue"][
    ["2010", "2014", "2018", "2022", "2025"]
] / 1e9
```

Which returns:

{% include ft-chart.html id="semis-revenue" src="/assets/data/article-charts.json" label="Semiconductor revenue" %}

Several things stand out. Intel peaked somewhere between 2020 and 2022, then contracted, a pattern without precedent in the company's history. NVIDIA's inflection is visible between 2022 and 2025: revenue grew from $26.9 billion to $130.5 billion in three years. Broadcom's growth looks smooth in this chart, but the jump from $4.3 billion in 2014 to $20.8 billion in 2018 was almost entirely acquisition-driven, as the company absorbed Avago Technologies, Brocade, and CA Technologies in rapid succession. TXN and QCOM, the two companies least exposed to the AI compute buildout, show the flattest trajectories.

> **Try this with the Finance Toolkit MCP:** *"Pull annual revenue for Intel, AMD, NVIDIA, Qualcomm, Broadcom, and Texas Instruments from 2010 to 2025. Which company had the highest revenue in 2010 and which did in 2025?"*

## Gross Margins: The Fabless Advantage

Revenue shows who is growing, while gross margins show who controls their cost structure. In semiconductors, the key structural divide is between integrated device manufacturers (companies that design and fabricate their own chips) and fabless companies that outsource manufacturing to foundries like TSMC.

```python
gross_margin = sector.ratios.get_gross_margin()

margins = gross_margin[["2010", "2014", "2018", "2022", "2025"]] * 100
```

Which returns:

{% include ft-chart.html id="semis-margins" src="/assets/data/article-charts.json" label="Semiconductor gross margins" %}

The largest move in the chart is Intel's, from 66% gross margins in 2010 to 34.8% in 2025. The proximate cause is that Intel's manufacturing processes fell behind TSMC's, first by one node generation, then two, so Intel's chips cost more to produce while competitors using TSMC got access to better processes at lower cost. As a result, Intel's cost-per-chip disadvantage compounds with every product cycle.

NVIDIA went in the opposite direction: from 35.4% in 2010 to 75.0% in 2025. A fabless company with a near-monopoly on AI training hardware can charge what the market bears, and the market has been willing to pay very high prices for H100 and Blackwell GPUs. NVIDIA's gross margin today is higher than Intel's ever was.

AMD transitioned from a company with 33% gross margins in 2014 (a period when it was fighting for survival) to 49.5% in 2025. In 2022, AMD's gross margin crossed above Intel's for the first time. That crossover has more to do with manufacturing than with products: as a fabless company using TSMC, AMD gained access to better nodes while Intel's own fabs struggled.

> **Try this with the Finance Toolkit MCP:** *"Show gross margins for Intel, AMD, NVIDIA, and Qualcomm from 2010 to 2025. When did AMD's gross margin first exceed Intel's?"*

## Intel vs AMD: The x86 CPU Battle

Not every company in this sector competes with every other. Texas Instruments makes analog chips for industrial and automotive customers; it does not compete with NVIDIA for AI data center revenue. Qualcomm sells ARM-based mobile processors and has never produced an x86 chip. Broadcom targets networking and storage controllers.

In x86 CPUs, the actual competition is between two companies, Intel and AMD. Every server, desktop, and laptop CPU socket holds a chip made by one of them. Market share gained by one is market share lost by the other.

```python
cpu_rivals = ["INTC", "AMD"]
years = ["2010", "2014", "2018", "2020", "2022", "2024", "2025"]

cpu_revenue = income.loc["Revenue"].loc[cpu_rivals, years] / 1e9
cpu_margins = sector.ratios.get_gross_margin().loc[cpu_rivals, years] * 100
cpu_roic = sector.ratios.get_return_on_invested_capital().loc[cpu_rivals, years] * 100
```

Which returns:

{% include ft-chart.html id="semis-intc-amd" src="/assets/data/article-charts.json" label="Intel versus AMD" %}

From 2010 to 2017, Intel was dominant by every metric. AMD spent this period losing money, cutting headcount, and struggling to produce a competitive architecture. Its gross margins compressed from 45.6% to below 30% in 2015 and 2016 as it competed on price with inferior products.

The inflection came in 2017 when AMD launched the Zen architecture under Lisa Su. The first Ryzen CPUs and EPYC server chips could compete with Intel's best products. The financial data lags the product cycle: revenue did not break meaningfully higher until 2021-2022, and gross margin recovery tracked along with product mix shifting toward EPYC.

By 2022, AMD's gross margin had exceeded Intel's, a reversal that would have seemed implausible in 2015. By 2024 and 2025, Intel's ROIC had turned negative, meaning the company was destroying capital. Intel's $5 billion investment in foundry capacity between 2020 and 2024 has not yet returned the expected margins, and the company returned a net loss in 2025.

AMD's ROIC of 6.8% in 2025 is modest, reflecting the Xilinx acquisition ($35 billion, 2022) which considerably expanded the invested capital base. The business is generating reasonable returns on operating assets; the acquisition debt is working against the ratio.

> **Try this with the Finance Toolkit MCP:** *"Compare Intel and AMD's revenue, gross margin, and return on invested capital from 2010 to 2025. When did AMD first surpass Intel on gross margin?"*

## NVIDIA vs AMD: The GPU and AI Accelerator Race

AMD and NVIDIA have been GPU competitors since AMD's 2006 acquisition of ATI Technologies. Both companies design discrete graphics chips for gaming, professional workstations, and data center compute. In 2010, the two companies were comparable in size. By 2025, the gap was $130.5 billion versus $34.6 billion, and almost all of that divergence is explained by AI infrastructure.

```python
gpu_rivals = ["NVDA", "AMD"]

gpu_revenue = income.loc["Revenue"].loc[gpu_rivals, years] / 1e9
gpu_margins = sector.ratios.get_gross_margin().loc[gpu_rivals, years] * 100
gpu_roic = sector.ratios.get_return_on_invested_capital().loc[gpu_rivals, years] * 100
```

Which returns:

{% include ft-chart.html id="semis-nvda-amd" src="/assets/data/article-charts.json" label="NVIDIA versus AMD" %}

Through 2020, the two companies moved roughly in parallel. AMD and NVIDIA were neck-and-neck on revenue. The ROIC numbers for 2020 (AMD at 50.2%, NVIDIA at 24.3%) actually show AMD leading, a reflection of AMD's lean capital base at that moment before the Xilinx acquisition.

The separation happened in 2021 and accelerated through 2022 to 2025. The driver is AI training infrastructure rather than gaming GPUs, where AMD's Radeon line still competes with NVIDIA's GeForce range. NVIDIA's H100 and Blackwell GPUs, running on CUDA, became the default hardware for training large language models. The software built around CUDA over 15 years proved nearly impossible for AMD to replicate quickly with its ROCm platform.

The effect shows up in ROIC: NVIDIA earned a 102.6% return on invested capital in 2025, against 6.8% for AMD. Both companies make GPUs, but only NVIDIA has a software moat.

AMD's position in this race is structurally harder than its Intel rivalry. Against Intel, AMD competes on x86 CPU performance, a problem of engineering execution. Against NVIDIA, AMD competes on AI software ecosystem depth, a problem of developer adoption and network effects that is slower and more expensive to overcome.

> **Try this with the Finance Toolkit MCP:** *"Compare NVIDIA and AMD's revenue and return on invested capital from 2018 to 2025. How large is the ROIC gap in 2025 and what explains it?"*

## What the Market Is Pricing In

The financial history explains the divergence so far, and current valuations show where the market expects each company to go.

```python
pe = sector.ratios.get_price_to_earnings_ratio()
ev_ebitda = sector.ratios.get_ev_to_ebitda_ratio()

current_valuation = pd.DataFrame({
    "P/E": pe["2025"],
    "EV/EBITDA": ev_ebitda["2025"]
}).sort_values("EV/EBITDA")
```

Which returns:

{% include ft-chart.html id="semis-valuation" src="/assets/data/article-charts.json" label="Semiconductor valuation multiples" %}

Qualcomm is the cheapest name on EV/EBITDA at 14.2x, pricing in limited AI exposure and the ARM licensing exposure risk. Texas Instruments at 21.3x is being valued as a stable analog business with cyclical revenue sensitivity.

Intel cannot be valued on P/E (the company is reporting losses) and its EV/EBITDA of 19.1x is elevated relative to the earnings power the business is currently generating. The market is either pricing in a recovery or pricing in acquisition optionality. The gross margin and ROIC data suggest recovery will take years.

NVIDIA at 63.5x P/E and 55.5x EV/EBITDA is expensive in absolute terms. Whether those multiples are justified depends on whether AI infrastructure CapEx remains elevated and whether NVIDIA maintains its software ecosystem lead. At 102.6% ROIC in 2025, the business is exceptionally profitable; the open question is how long that advantage lasts.

AMD at 80.8x P/E trades at a premium to NVIDIA despite lower ROIC and competition on two fronts. The premium reflects expectations for ROIC recovery as the Xilinx acquisition amortizes and as AI GPU shipments scale, which leaves real execution risk.

> **Try this with the Finance Toolkit MCP:** *"Show current P/E and EV/EBITDA for Intel, AMD, NVIDIA, Qualcomm, Broadcom, and Texas Instruments. Which is the cheapest on each metric?"*

{% include ft-charts-script.html %}
