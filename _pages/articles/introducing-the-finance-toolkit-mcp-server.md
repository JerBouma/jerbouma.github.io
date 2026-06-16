---
title: Introducing the Finance Toolkit MCP Server
date: 2026-06-12
permalink: /articles/introducing-the-finance-toolkit-mcp-server
excerpt: "Learn how the Finance Toolkit MCP server exposes 200+ financial ratios, indicators, and performance measurements to any AI assistant that supports the Model Context Protocol. This allows you to ask questions in plain English and receive structured answers without writing Python code."
description: "Learn how the Finance Toolkit MCP server exposes 200+ financial ratios, indicators, and performance measurements to any AI assistant that supports the Model Context Protocol."
layout: single
classes: wide-sidebar article-document
author_profile: false
collection: article
tags: [Finance Toolkit, Fundamental Analysis, MCP Server]
share: true
---
On the 6th of May, 2023, Microsoft's Price-to-Earnings ratio was reported as 28.93 by Stockopedia, 32.05 by Morningstar, 32.66 by Macrotrends, 33.67 by the Wall Street Journal, and 34.4 by Companies Market Cap. Every one of those numbers is "correct." They just use different definitions of earnings, different share counts, and different rounding. None of the providers publish the formula, so there is no way to know which one matches the calculation you actually want.

That inconsistency is why I built the Finance Toolkit: an open-source Python library where every ratio, indicator, and model is implemented in plain, readable code you can audit yourself. It covers 200+ metrics across equities, options, currencies, crypto, ETFs, indices, and macroeconomic data going back over a century, all sourced from 30+ years of financial statements. On top of the library sits an MCP server that exposes the same 200+ metrics to any AI assistant that supports the Model Context Protocol, so you (or your assistant) never have to choose between writing Python and asking a question in plain English.

**The source code for every calculation is on [GitHub](https://github.com/JerBouma/FinanceToolkit). The MCP server documentation lives [here](https://www.jeroenbouma.com/projects/financetoolkit/mcp).**

## Setting Things Up

The Python library and the MCP server are the same engine with two different front doors. Start with the Python side, since understanding it makes the MCP tool calls easier to reason about later.

Start by installing the Finance Toolkit:

```bash
pip install financetoolkit -U
```

Then import the library and create a Toolkit instance. Each section below swaps in a different ticker universe, since the point is showing the breadth of what one consistent API can pull, but the syntax never changes.

```python
from financetoolkit import Toolkit

companies = Toolkit(
    tickers=["MSFT", "AAPL"],
    api_key="YOUR_FMP_API_KEY",
    start_date="2020-01-01"
)
```

Get your FMP API key at [jeroenbouma.com/fmp](https://www.jeroenbouma.com/fmp). The free plan covers five years of history and 250 requests a day; a paid plan unlocks the full 30+ years and quarterly data, at a 15% discount through that (affiliat) link. I do provide means to provide your own data as well, see [here](https://www.jeroenbouma.com/projects/financetoolkit/external-datasets).

## From Code to Conversation: the MCP Server

Writing Python is not always the fastest way to get an answer, and getting an AI assistant to reason accurately over financial data by itself usually falls short: web search is unreliable, scraped data is inconsistent across sources (see the PE example above), and models hallucinate numbers when they cannot find them. The Finance Toolkit MCP server fixes this by giving any MCP-compatible assistant direct, structured access to the same 200+ metrics, backed by the transparent calculation methods in the library.

You do not need a local Python environment to use it. A single command configures your AI client automatically:

```bash
uvx --from "financetoolkit[mcp]" financetoolkit-mcp-setup
```

This supports Claude Desktop, Claude Code, GitHub Copilot in VS Code, Cursor, Windsurf, and Gemini. If you use Claude Desktop specifically, there is also a one-click MCPB bundle on the [latest GitHub release](https://github.com/JerBouma/FinanceToolkit/releases/latest) that skips the terminal entirely. Either way, you will be asked for the same FMP API key used above, and the free plan is enough to get started.

Once it is running, the server groups the 200+ Finance Toolkit methods into about 21 categorical tools. You never name a function or set a parameter yourself; the assistant picks the right tool from your question and returns structured output. The depth of interpretation scales with the model: Claude Sonnet layers in qualitative reasoning on top of the numbers, while smaller models like GPT-5 mini return clean structured data without the narrative. Both work, since the server is built to support either.

Within Claude Desktop, it will look like below once setup.

<p align="center">
  <img src="https://dev-to-uploads.s3.amazonaws.com/uploads/articles/q0o5322rfem76oub01l5.png" alt="Finance Toolkit MCP server configured in Claude Desktop" width="600">
  <br><em>Once everything is setup, you should see the Finance Toolkit as one of the available connectors.</em>
</p>

## Equity Analysis: Margins, Returns, and Multiples Side by Side

The Finance Toolkit was built with equity research first, which is why this is the deepest category: profitability, valuation, efficiency, liquidity, and solvency ratios, plus models like WACC, DuPont decomposition, the Altman Z-Score, and the Piotroski F-Score. A good stress test for any of these is an industry where growth rates differ wildly between names that are nominally in the same business: semiconductors.

```python
from financetoolkit import Toolkit

chips = Toolkit(
    tickers=["NVDA", "AMD", "ASML", "TSM", "AVGO", "INTC", "QCOM", "TXN", "AMAT"],
    api_key="YOUR_FMP_API_KEY",
    start_date="2015-01-01"
)

cumulative_return = chips.get_historical_data()
pe = chips.ratios.get_price_to_earnings_ratio()["2025"]
ev_ebitda = chips.ratios.get_ev_to_ebitda_ratio()["2025"]
eps_growth = chips.ratios.get_earnings_per_share(growth=True)["2025"]
revenue_per_share = chips.ratios.get_revenue_per_share()["2025"]
```

Which returns:

| Ticker | Cumulative Return (2015-2025) | P/E (2025) | EV/EBITDA (2025) | EPS Growth (2025) | Revenue/Share (2025) |
|--------|-------------------------------:|-----------:|------------------:|-------------------:|-----------------------:|
| NVDA | +42,215% | 63.5x | 55.5x | +146.2% | $5.26 |
| AMD | +20,344% | 80.8x | 52.2x | +164.3% | $21.17 |
| AVGO | +3,935% | 72.6x | 50.5x | +286.2% | $13.16 |
| AMAT | +2,347% | 29.7x | 23.8x | +0.6% | $35.11 |
| TSM | +1,981% | 28.4x | 18.0x | +57.2% | $23.75 |
| ASML | +1,762% | 36.9x | 28.0x | +45.0% | $98.67 |
| QCOM | +297% | 34.1x | 14.2x | -44.1% | $40.08 |
| TXN | +585% | 31.9x | 21.3x | +4.8% | $19.37 |
| INTC | +352% | - | 19.1x | -98.75% | $10.88 |

The dispersion inside one industry is the whole story here: NVDA turned a 2015 position into roughly 421 times its starting value, while INTC is (compared to NVDA) essentially flat a decade later, its P/E reported as negative because it posted a net loss and its EPS collapsing 98.75% in 2025 alone. AVGO's EPS growth of 286.2% outpaces even NVDA, reflecting the VMware acquisition layered on top of its AI networking business rather than organic chip sales growth, worth separating out before reading too much into the headline number. ASML trades at the richest EV/EBITDA multiple in the group (28.0x) despite the slowest revenue-per-share base of the bunch in absolute growth terms, a premium the market assigns to its effective monopoly on the EUV lithography machines every leading-edge fab depends on.

A call with the Finance Toolkit MCP would return an answer such as below.

<p align="center">
  <img src="https://dev-to-uploads.s3.amazonaws.com/uploads/articles/hbwucatw62srxqu3qc3v.png" alt="Finance Toolkit MCP response comparing semiconductor equity ratios" width="600">
  <br><em>Semiconductors went from a cyclical industrial sector to the backbone of AI infrastructure over the last decade and the market priced that transition in full. NVDA and AMD returned over 150x since 2015 while the S&P 500 compounded quietly at the bottom of the same chart.</em>
</p>

## Technical Analysis: Is the Market Overbought?

Technical indicators work off OHLC price data, so they apply to any asset class the Toolkit supports, not just equities. RSI, MACD, the Stochastic Oscillator, and Bollinger Bands are all available, grouped under categories like momentum, volatility, and overlap. The clearest stress test for a momentum indicator is a market shock, so this one looks at European sector ETFs through the 2020 Corona crash and the year that followed.

```python
from financetoolkit import Toolkit

sectors = Toolkit(
    tickers=["EXV9.DE", "EXV1.DE", "EXV4.DE", "EXI5.DE", "EXV3.DE", "EXH9.DE", "EXH1.DE"],
    api_key="YOUR_FMP_API_KEY",
    start_date="2019-11-01"
)
rsi = sectors.technicals.get_relative_strength_index(period="monthly")
```

These are iShares STOXX Europe 600 sector UCITS ETFs: EXV9.DE (Travel & Leisure), EXV1.DE (Banks), EXV4.DE (Health Care), EXI5.DE (Real Estate), EXV3.DE (Technology), EXH9.DE (Utilities), and EXH1.DE (Oil & Gas).

Which returns:

| Date | Travel & Leisure | Banks | Health Care | Real Estate | Technology | Utilities | Oil & Gas |
|------|------------------:|------:|-------------:|-------------:|------------:|-----------:|-----------:|
| 2019-12 | 63.3 | 51.4 | 77.0 | 70.4 | 72.7 | 89.7 | 51.1 |
| 2020-03 | 26.9 | 31.9 | 65.9 | 36.2 | 53.2 | 51.9 | 26.8 |
| 2020-06 | 30.2 | 26.2 | 70.2 | 39.5 | 59.1 | 59.9 | 21.4 |
| 2020-09 | 34.9 | 28.9 | 61.5 | 44.0 | 61.6 | 57.6 | 19.3 |
| 2021-01 | 40.7 | 35.4 | 48.4 | 40.7 | 61.0 | 57.9 | 34.5 |
| 2021-05 | 77.0 | 79.0 | 63.3 | 75.3 | 80.9 | 71.2 | 61.1 |
| 2021-12 | 61.7 | 79.5 | 79.1 | 74.5 | 83.3 | 65.9 | 76.3 |

Oil & Gas was the most oversold sector of the whole crisis, bottoming at an RSI of 19.3 in September 2020, well past the typical oversold line of 30, and it stayed depressed there for most of the year as travel demand collapse fed straight through to fuel demand. Banks were close behind, troughing at 26.2 in June 2020 and not climbing back above the 40 mark until November, longer than any other sector here took to recover. Health Care and Technology never came close to oversold even at the worst of the March 2020 crash, with RSI bottoming at 65.9 and 53.2 respectively, the closest thing to a flight-to-quality signal in this dataset.

The more striking part is the reversal. The same two sectors that bottomed hardest, Oil & Gas and Banks, both closed 2021 deep in overbought territory at 76.3 and 79.5, a swing of roughly 50 to 60 RSI points in eighteen months. That is the kind of regime change a single point-in-time RSI reading would never catch; it only shows up when you pull the full series.

A call with the Finance Toolkit MCP is showing what I mean:

<p align="center">
  <img src="https://dev-to-uploads.s3.amazonaws.com/uploads/articles/ef2dxd12heokum126nsl.png" alt="Finance Toolkit MCP response on European sector RSI during the 2020 crash" width="600">
  <br><em>The COVID crash was swift but uneven. Airlines collapsed into extreme oversold territory with RSI hitting 22 in April 2020. Alevel that signals panic selling, not fundamental repricing. Technology barely dipped. Oil & Gas, untouched by the initial shock, swung to RSI 91 a year later as the energy cycle turned.</em>
</p>

## Risk and Performance: What the Fama-French Factors Reveal About South American Stocks

Beta and alpha alone treat "the market" as the only systematic risk that matters. The Fama-French five-factor model goes further, decomposing returns into exposure to the market (Mkt-RF), company size (SMB), value versus growth (HML), profitability (RMW), and investment intensity (CMA), plus an R-squared that tells you how much of the return that combination actually explains. South American equities are a good test case, since they mix commodity exporters, banks, and a tech name that behaves nothing like the rest of the region.

```python
from financetoolkit import Toolkit

south_america = Toolkit(
    tickers=["PBR", "YPF", "VALE", "SCCO", "ITUB", "CIB", "MELI", "GGB"],
    api_key="YOUR_FMP_API_KEY",
    start_date="2021-01-01"
)
fama_french = south_america.performance.get_fama_and_french_model(period="yearly")
```

Which returns, for 2025:

| Ticker | Mkt-RF | SMB | HML | RMW | CMA | R² |
|--------|-------:|----:|----:|----:|----:|---:|
| ITUB (Itau, bank) | 0.0167 | -0.0023 | -0.0071 | -0.0116 | -0.0051 | 0.683 |
| SCCO (Southern Copper, mining) | 0.0146 | 0.0000 | -0.0047 | -0.0117 | -0.0033 | 0.529 |
| VALE (Vale, mining) | 0.0118 | 0.0042 | -0.0086 | 0.0032 | -0.0103 | 0.511 |
| CIB (Bancolombia, bank) | 0.0109 | -0.0029 | 0.0024 | -0.0107 | -0.0101 | 0.340 |
| MELI (MercadoLibre, e-commerce) | 0.0087 | -0.0001 | -0.0005 | -0.0023 | -0.0049 | 0.122 |
| YPF (YPF, energy) | 0.0067 | 0.0023 | -0.0027 | -0.0041 | -0.0008 | 0.192 |
| GGB (Gerdau, steel) | 0.0063 | -0.0029 | -0.0014 | -0.0110 | -0.0009 | 0.276 |
| PBR (Petrobras, energy) | 0.0057 | -0.0017 | 0.0002 | -0.0037 | 0.0009 | 0.169 |

The R-squared column is the most useful read here, since it tells you how reliable the rest of the row is. ITUB's 2025 regression explains 68.3% of its return variance through these five factors, the highest in the group and typical of a large, liquid bank whose returns track broad risk factors closely. MELI sits at the other extreme: only 12.2% of its return is explained by the model, which fits a company whose price action is driven far more by idiosyncratic growth narrative and earnings surprises than by size, value, or investment-style exposures.

That gap widens when you look at the trend across years rather than a single snapshot:

| Ticker | 2021 | 2022 | 2023 | 2024 | 2025 |
|--------|-----:|-----:|-----:|-----:|-----:|
| MELI R² | 0.619 | 0.347 | 0.213 | 0.334 | 0.122 |
| VALE R² | 0.131 | 0.196 | 0.408 | 0.489 | 0.511 |
| SCCO R² | 0.149 | 0.288 | 0.299 | 0.471 | 0.529 |

MELI's R-squared has fallen almost every year since 2021, from 0.619 to 0.122, meaning the five-factor model explains less and less of its return over time as the stock has decoupled further from traditional risk factors. VALE and SCCO show the opposite pattern, with explanatory power roughly tripling over the same five years as both mining names became more tightly linked to broad market and value-style risk during the commodity cycle. None of that shows up in a beta or alpha calculation alone, which is the case for running the full factor model instead of stopping at single-factor CAPM.

A call with the Finance Toolkit MCP would return an answer such as below.

<p align="center">
  <img src="https://dev-to-uploads.s3.amazonaws.com/uploads/articles/mcpyhbr1gwkezepzvss0.png" alt="Finance Toolkit MCP response on the Fama-French factor model for South American equities" width="600">
  <br><em>The Fama-French 5-factor model decomposes stock returns into market beta, size, value, profitability, and investment exposure. Applied to South American industries, it reveals that MercadoLibre behaves more like a US growth stock than a Latin American consumer play while energy names like Petrobras and YPF are primarily market-beta bets with a secondary value tilt.</em>
</p>

## Macroeconomic Analysis: Tracking Asia's Growth Engines

Macroeconomic data goes back over a century and covers 60+ countries: unemployment, GDP growth, inflation, trade balances, government debt, central bank rates, and government bond yields, sourced from the [OECD](https://www.oecd.org/en/data/indicators.html?orderBy=mostRelevant&page=0&facetTags=oecd-languages%3Aen) and the [Global Macro Database](https://www.globalmacrodata.com/). It is available through the `economics` module on a Toolkit instance, or as a fully standalone module if you only need macro data.

```python
from financetoolkit import Economics

economics = Economics(start_date="2020-01-01")

gdp_growth = economics.get_gross_domestic_product(
    countries=["India", "Vietnam", "Indonesia", "China", "South Korea"],
    growth=True
)
```

Which returns:

| Country | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---------|-----:|-----:|-----:|-----:|-----:|-----:|
| India | -1.2% | 18.9% | 14.2% | 9.6% | 10.1% | 10.4% |
| Vietnam | 4.4% | 5.5% | 12.5% | 7.1% | 10.4% | 9.6% |
| Indonesia | -2.5% | 9.9% | 15.4% | 6.7% | 7.6% | 7.7% |
| China | 3.5% | 11.7% | 5.0% | 4.6% | 4.5% | 6.4% |
| South Korea | 0.9% | 7.9% | 4.6% | 3.3% | 5.5% | 4.0% |

India has held growth above 9.5% every year since the 2020 contraction, while China has settled into a slower mid-single-digit pace after its 2021 reopening spike. South Korea, the most mature economy in this group, tracks closest to developed-market growth rates throughout. None of this required scraping a single government website or reconciling conflicting definitions across sources, which is the same problem this whole project started from.

A call with the Finance Toolkit MCP would return an answer such as below.

<p align="center">
  <img src="https://dev-to-uploads.s3.amazonaws.com/uploads/articles/6o1jp35n33itf807nhx5.png" alt="Finance Toolkit MCP response on GDP growth across Asian economies" width="600">
  <br><em>Investment as a share of GDP is one of the cleanest leading indicators of structural economic development. Vietnam and India led the region in the 2000s, fuelling their infrastructure and manufacturing buildouts. Bangladesh has been rising steadily since 2010. The hallmark of an economy still in the upgrading phase, not yet plateauing like Malaysia or Thailand.</em>
</p>