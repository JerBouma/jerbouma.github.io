---
title: Introducing the Finance Toolkit MCP Server
date: 2026-06-12
last_modified_at: 2026-10-14
permalink: /articles/introducing-the-finance-toolkit-mcp-server
excerpt: "The Finance Toolkit MCP server gives Claude, ChatGPT and other AI assistants 500+ documented financial calculations at one hosted URL. Four worked questions show what comes back: semiconductor valuations, European sectors through the 2020 crash, Fama-French factors in South America and Asia's investment cycle."
description: "The free, hosted Finance Toolkit MCP server gives Claude, ChatGPT and other AI assistants 500+ auditable methods: ratios, risk, factor models and macro data."
layout: single
classes: wide-sidebar article-document
author_profile: false
collection: article
tags: [MCP Server]
share: true
---
On the 6th of May, 2023, Microsoft's Price-to-Earnings ratio was reported as 28.93 by Stockopedia, 32.05 by Morningstar, 32.66 by Macrotrends, 33.67 by the Wall Street Journal, and 34.4 by Companies Market Cap. Every one of those numbers is "correct." They just use different definitions of earnings, different share counts and different rounding. None of the providers publish the formula, so there is no way to know which one matches the calculation you actually want. Ask an AI assistant for the same number and it inherits the problem: it picks one of those figures from a web search, or recalls one from its training data, and when it finds nothing it may produce a plausible-looking number of its own.

That inconsistency is why I built the Finance Toolkit, an open-source Python library where every ratio, indicator and model is plain, readable code you can audit. The Finance Toolkit MCP server puts the same 500+ methods behind the [Model Context Protocol](https://modelcontextprotocol.io){:target="_blank"}, so Claude, ChatGPT, Copilot, Cursor and other assistants calculate the number instead of recalling it. It is hosted at one URL, so there is nothing to install. This article shows how to connect it and works through four questions, from semiconductor valuations to Asia's investment cycle, with every tool call and result.

**The source code for every calculation is on [GitHub](https://github.com/JerBouma/FinanceToolkit){:target="_blank"}. Installation steps for every client are on the [Finance Toolkit MCP server](/projects/financetoolkit/mcp) page.**

<div class="ca-strip">
  <div><strong>1 URL</strong><span>hosted server, nothing to install</span></div>
  <div><strong>500+</strong><span>financial methods behind 22 tools, plus 3 search tools</span></div>
  <div><strong>4</strong><span>worked questions below, with every tool call</span></div>
  <div><strong>Free</strong><span>open source, MIT-licensed</span></div>
</div>

## Connecting the Server

The hosted server lives at this URL:

```
https://financetoolkit.jeroenbouma.com/mcp
```

Company data comes from [Financial Modeling Prep](/fmp){:target="_blank"} (FMP), so the server needs an FMP API key. You don't paste it into a config file: the first time your assistant calls the server, it opens an OAuth page that asks for the key, and you enter it once. The free plan covers five years of history and 250 requests a day; a paid plan adds the full 30+ years and quarterly data, at a 15% discount through that (affiliate) link. Macroeconomic data needs no key.

In Claude Desktop or claude.ai the steps are the same:

1. Click **Customize** in the left sidebar and open the **Connectors** tab.
2. Click **+** and select **Add custom connector**.
3. Name it *Finance Toolkit*, paste the URL above and click **Add**.
4. Ask a financial question in a new chat. On the first tool call a browser window asks for your FMP key.
{: .ca-steps}

Every other client has its own installation card on the [MCP server page](/projects/financetoolkit/mcp#installation):

<div class="ca-clients">
  <a href="/projects/financetoolkit/mcp#remote-claude-code"><i class="fas fa-terminal" aria-hidden="true"></i>Claude Code<i class="fas fa-arrow-right ca-clients__go" aria-hidden="true"></i></a>
  <a href="/projects/financetoolkit/mcp#remote-chatgpt"><i class="fas fa-comment-dots" aria-hidden="true"></i>ChatGPT<i class="fas fa-arrow-right ca-clients__go" aria-hidden="true"></i></a>
  <a href="/projects/financetoolkit/mcp#remote-vs-code"><i class="fab fa-microsoft" aria-hidden="true"></i>VS Code and GitHub Copilot<i class="fas fa-arrow-right ca-clients__go" aria-hidden="true"></i></a>
  <a href="/projects/financetoolkit/mcp#remote-cursor"><i class="fas fa-i-cursor" aria-hidden="true"></i>Cursor<i class="fas fa-arrow-right ca-clients__go" aria-hidden="true"></i></a>
  <a href="/projects/financetoolkit/mcp#remote-windsurf"><i class="fas fa-wind" aria-hidden="true"></i>Windsurf<i class="fas fa-arrow-right ca-clients__go" aria-hidden="true"></i></a>
  <a href="/projects/financetoolkit/mcp#remote-gemini"><i class="fab fa-google" aria-hidden="true"></i>Gemini CLI<i class="fas fa-arrow-right ca-clients__go" aria-hidden="true"></i></a>
</div>

If you would rather run the server on your own machine, the local route uses the same code. One command finds the configuration file of Claude Desktop, Claude Code, VS Code, Cursor, Windsurf or Gemini and writes the entry, including your key:

```bash
uvx --from "financetoolkit[mcp]" financetoolkit-mcp-setup
```

For Claude Desktop there is also a one-click MCPB bundle on the [latest GitHub release](https://github.com/JerBouma/FinanceToolkit/releases/latest){:target="_blank"}. The [local installation cards](/projects/financetoolkit/mcp#local-clients) cover each client by hand.

## One Engine, Two Front Doors

The Python library and the MCP server run the same calculations. The server groups the 500+ methods into 22 categorical tools, such as `profitability`, `valuation`, `models`, `performance`, `risk`, `momentum` and `macroeconomics`. Each takes an `indicator` that selects the exact metric, for example `valuation` with `indicator='get_price_to_earnings_ratio'`. Three search tools (`search_metric_categories`, `search_by_category` and `search_metrics`) help the assistant find the right one. You never name a tool yourself: you ask in plain English, and the assistant picks the tool, the indicator and the period.

Every tool call maps to one line of Python, so you can reproduce any answer below. Install the library with `pip install financetoolkit -U`, then:

```python
from financetoolkit import Toolkit

companies = Toolkit(
    tickers=["MSFT", "AAPL"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2020-01-01",
)

pe = companies.ratios.get_price_to_earnings_ratio()
```

The server returns the same numbers to every model. A larger model mostly adds depth: more follow-up calculations and better caveats. Smaller models pick the right tools and report the same figures. You can also [use your own data instead](/projects/financetoolkit/external-datasets) in the Python library.

## What You Can Ask

Below are four questions an analyst or portfolio manager might ask, each answered through the hosted server. Every step lists the tool and indicator that were called, and every chart shows what those calls returned: prices up to October 13, 2026, financial statements up to fiscal 2025 and macroeconomic data up to 2025, retrieved on October 14, 2026. The "What the data shows" box is my reading of those numbers. Below each answer is the same calculation in Python.

<div class="ca-nav ca-nav--4">
  <a href="#semiconductors"><i class="fas fa-microchip" aria-hidden="true"></i>Chipmakers: priced for growth?</a>
  <a href="#europe-2020"><i class="fas fa-gauge-high" aria-hidden="true"></i>Europe's sectors through 2020</a>
  <a href="#fama-french"><i class="fas fa-earth-americas" aria-hidden="true"></i>Fama-French in South America</a>
  <a href="#asia-investment"><i class="fas fa-industry" aria-hidden="true"></i>Asia's investment cycle</a>
</div>

### Which chipmakers are priced for their growth? {#semiconductors}

Semiconductors are a good test for equity ratios, because growth rates differ wildly between companies that are nominally in the same business. EV/EBITDA compares the value of the whole company, debt included, with its operating cash earnings, which makes it less sensitive to leverage and one-off charges than the P/E.

<div class="mcp-show">
<div class="ca-q"><span class="ca-q__avatar"><i class="fas fa-user" aria-hidden="true"></i></span><p>Compare NVDA, AMD, AVGO, TSM, ASML, AMAT, QCOM, TXN and INTC. How did the shares do since 2015, how fast did earnings grow last year, how profitable are they, and what does the market pay for them?</p></div>
<div class="mcp-show__meta"><span><b>9</b> companies</span><span><b>5</b> tool calls</span><span><b>11</b> years of prices</span></div>
<details class="mcp-show__trace"><summary><i class="fas fa-list-check" aria-hidden="true"></i> The steps behind the answer</summary><ol><li><code>performance</code><span>get_returns: yearly and cumulative, rebased to 1 at the end of 2015, with SPY for the S&amp;P 500</span></li><li><code>valuation</code><span>get_price_to_earnings_ratio, fiscal 2021 to 2025</span></li><li><code>valuation</code><span>get_ev_to_ebitda_ratio, fiscal 2021 to 2025</span></li><li><code>valuation</code><span>get_earnings_per_share with growth=true, fiscal 2021 to 2025</span></li><li><code>profitability</code><span>get_operating_margin, fiscal 2021 to 2025</span></li></ol></details>

<div class="mcp-show__grid">
<div class="mcp-show__cell">{% include ft-chart.html id="mcpi-chips-growth" src="/assets/data/article-charts.json" label="Growth of one dollar invested in nine chipmakers and the S&P 500 since the end of 2015" %}</div>
<div class="mcp-show__cell">{% include ft-chart.html id="mcpi-chips-value" src="/assets/data/article-charts.json" label="Earnings per share growth against EV/EBITDA, fiscal 2025" %}</div>
<div class="mcp-show__cell">{% include ft-chart.html id="mcpi-chips-multiples" src="/assets/data/article-charts.json" label="P/E and EV/EBITDA of nine chipmakers, fiscal 2025" %}</div>
<div class="mcp-show__cell">{% include ft-chart.html id="mcpi-chips-margin" src="/assets/data/article-charts.json" label="Operating margin of six chipmakers, fiscal 2021 to 2025" %}</div>
</div>
<div class="mcp-show__verdict"><p class="mcp-show__label"><i class="fas fa-lightbulb" aria-hidden="true"></i> What the data shows</p><p>The dispersion inside one industry is extreme. A dollar in Nvidia at the end of 2015 grew to $286, in AMD to $211, while Intel grew to $3.78, the only one of the nine behind the S&amp;P 500 ($4.54). On fiscal 2025 numbers, Nvidia is not the expensive one: 34.2 times EBITDA and 38.0 times earnings, for 66.7% EPS growth and a 60.4% operating margin. AMD (52.1x) and Broadcom (50.2x) cost more, and their EPS growth of 164% and 286% is partly a rebound from depressed years (Broadcom's EPS fell 62.6% in 2024). TSMC pairs a 50.8% operating margin with 56.7% EPS growth at 17.9 times EBITDA, the second-lowest multiple in the group after Qualcomm, whose EPS fell 44.1%. Intel's P/E of −671 says only that it barely lost money: its EPS fell 98.75% on a −4.2% operating margin.</p></div>
<div class="ca-nums"><span><b>$286 vs $3.78</b>$1 since 2015, Nvidia vs Intel</span><span><b>34.2x</b>Nvidia EV/EBITDA, below AMD and Broadcom</span><span><b>50.8%</b>TSMC operating margin at 17.9x EBITDA</span></div>
</div>

Fiscal years are aligned to the calendar year they mostly fall in, so Nvidia's fiscal year to January 2026 shows as 2025, and ASML's and TSMC's statements are converted to US dollars to match their US listings. The server says both in the notes of its answer. In Python:

```python
from financetoolkit import Toolkit

chips = Toolkit(
    tickers=["NVDA", "AMD", "AVGO", "TSM", "ASML", "AMAT", "QCOM", "TXN", "INTC"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2015-01-02",
)

growth_of_one_dollar = chips.performance.get_returns(period="yearly", cumulative=True)
pe = chips.ratios.get_price_to_earnings_ratio()
ev_ebitda = chips.ratios.get_ev_to_ebitda_ratio()
eps_growth = chips.ratios.get_earnings_per_share(growth=True)
operating_margin = chips.ratios.get_operating_margin()
```

### How did Europe's sectors move through the 2020 crash? {#europe-2020}

Technical indicators work off price data, so they apply to ETFs as well as stocks. The Relative Strength Index (RSI) compares the size of recent gains with recent losses on a scale of 0 to 100: below 30 is conventionally oversold, above 70 overbought. A market shock is the clearest test, so this question looks at seven iShares STOXX Europe 600 sector ETFs listed in Germany: EXV9.DE (Travel & Leisure), EXV1.DE (Banks), EXV4.DE (Health Care), EXI5.DE (Real Estate), EXV3.DE (Technology), EXH9.DE (Utilities) and EXH1.DE (Oil & Gas).

<div class="mcp-show">
<div class="ca-q"><span class="ca-q__avatar"><i class="fas fa-user" aria-hidden="true"></i></span><p>How did European sectors move through the 2020 crash and the recovery? Use the weekly RSI of the iShares STOXX Europe 600 sector ETFs, and add their drawdowns and annual returns for 2020 and 2021.</p></div>
<div class="mcp-show__meta"><span><b>7</b> sector ETFs</span><span><b>3</b> tool calls</span><span><b>108</b> weeks of RSI</span></div>
<details class="mcp-show__trace"><summary><i class="fas fa-list-check" aria-hidden="true"></i> The steps behind the answer</summary><ol><li><code>momentum</code><span>get_relative_strength_index, weekly, September 2019 to December 2021</span></li><li><code>risk</code><span>get_maximum_drawdown over the daily series, 2020 to 2021</span></li><li><code>performance</code><span>get_returns, yearly, 2020 and 2021</span></li></ol></details>

<div class="mcp-show__grid">
<div class="mcp-show__cell mcp-show__cell--wide">{% include ft-chart.html id="mcpi-eu-rsi" src="/assets/data/article-charts.json" label="Weekly RSI of seven STOXX Europe 600 sector ETFs, December 2019 to December 2021" %}</div>
<div class="mcp-show__cell">{% include ft-chart.html id="mcpi-eu-drawdown" src="/assets/data/article-charts.json" label="Maximum drawdown of seven European sector ETFs, 2020 to 2021" %}</div>
<div class="mcp-show__cell">{% include ft-chart.html id="mcpi-eu-returns" src="/assets/data/article-charts.json" label="Returns of seven European sector ETFs in 2020 and 2021" %}</div>
<div class="mcp-show__cell mcp-show__cell--medium">{% include ft-chart.html id="mcpi-eu-low" src="/assets/data/article-charts.json" label="Lowest weekly RSI of seven European sector ETFs in 2020" %}</div>
</div>
<div class="mcp-show__verdict"><p class="mcp-show__label"><i class="fas fa-lightbulb" aria-hidden="true"></i> What the data shows</p><p>Every sector fell in the same weeks; the recovery split them in two. In the week to March 22, 2020, the RSI of Oil &amp; Gas dropped to 15.4 and Travel &amp; Leisure to 16.1, far below the oversold line of 30. Health Care bottomed at 29.9 a week earlier and was back above 50 by mid-April. Banks stayed below 50 until the week of November 9, 2020, when the first vaccine trial results came out, and Oil &amp; Gas spent all but one week of that stretch below 50 too. They ended 2020 down 26.6% and 22.5% while Technology and Utilities gained about 12%. In 2021 the order reversed: Banks returned 39.4%, the best of the seven. Travel &amp; Leisure, with the deepest drawdown (−55.3%), gained only 0.8% in 2021, and its RSI fell back to 27.3 in early December, after the Omicron variant appeared.</p></div>
<div class="ca-nums"><span><b>15.4</b>Oil &amp; Gas RSI, March 2020</span><span><b>−55.3%</b>Travel &amp; Leisure maximum drawdown</span><span><b>−26.6% → +39.4%</b>Banks, 2020 to 2021</span></div>
</div>

A single RSI reading would miss all of this; the regime change only shows up in the full series. The returns are in euros, the currency the ETFs trade in. In Python:

```python
from financetoolkit import Toolkit

sector_etfs = ["EXV9.DE", "EXV1.DE", "EXV4.DE", "EXI5.DE", "EXV3.DE", "EXH9.DE", "EXH1.DE"]

rsi = Toolkit(
    tickers=sector_etfs,
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2019-09-02",
    end_date="2021-12-31",
).technicals.get_relative_strength_index(period="weekly")

crisis = Toolkit(
    tickers=sector_etfs,
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2020-01-02",
    end_date="2021-12-31",
)
drawdown = crisis.risk.get_maximum_drawdown(period="daily")
returns = crisis.performance.get_returns(period="yearly")
```

### How much of a South American stock does the US factor model explain? {#fama-french}

Beta and alpha treat the market as the only systematic risk. The Fama-French five-factor model adds four more: company size (SMB, small minus big), value versus growth (HML, high minus low book-to-market), profitability (RMW, robust minus weak) and investment (CMA, conservative minus aggressive). The R-squared says how much of a stock's return that combination explains. The Toolkit regresses each calendar year of daily excess returns on the US factors from [Kenneth French's data library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html){:target="_blank"}. US-listed South American stocks are a good test, since they mix commodity exporters, banks and an e-commerce company.

<div class="mcp-show">
<div class="ca-q"><span class="ca-q__avatar"><i class="fas fa-user" aria-hidden="true"></i></span><p>Run the Fama-French five-factor model on Petrobras, YPF, Vale, Southern Copper, Itaú, Bancolombia, MercadoLibre and Gerdau for every year since 2021. How much do the factors explain, and which exposures stand out?</p></div>
<div class="mcp-show__meta"><span><b>8</b> stocks</span><span><b>1</b> tool call</span><span><b>48</b> regressions</span></div>
<details class="mcp-show__trace"><summary><i class="fas fa-list-check" aria-hidden="true"></i> The steps behind the answer</summary><ol><li><code>performance</code><span>get_fama_and_french_model, yearly, multiple regression on all five factors, 2021 to October 2026</span></li></ol></details>

<div class="mcp-show__grid">
<div class="mcp-show__cell mcp-show__cell--wide">{% include ft-chart.html id="mcpi-ff-r2" src="/assets/data/article-charts.json" label="R-squared of the Fama-French five-factor model for six South American stocks, 2021 to 2026" %}</div>
<div class="mcp-show__cell">{% include ft-chart.html id="mcpi-ff-loadings" src="/assets/data/article-charts.json" label="Fama-French factor loadings of eight South American stocks in 2025" %}</div>
<div class="mcp-show__cell">{% include ft-chart.html id="mcpi-ff-trend" src="/assets/data/article-charts.json" label="Market and value loadings of Petrobras, YPF, Southern Copper and MercadoLibre over time" %}</div>
<div class="mcp-show__cell mcp-show__cell--medium">{% include ft-chart.html id="mcpi-ff-r2-2025" src="/assets/data/article-charts.json" label="R-squared of the five-factor model for eight South American stocks in 2025" %}</div>
</div>
<div class="mcp-show__verdict"><p class="mcp-show__label"><i class="fas fa-lightbulb" aria-hidden="true"></i> What the data shows</p><p>For most of these stocks, the US factors explain little. In 2025 the R-squared ranged from 0.16 for Itaú to 0.41 for Southern Copper, so more than half of every stock's daily return variance came from something else: currencies, local rates, commodity prices and politics. MercadoLibre was the exception early on, at 0.69 in 2022, when it traded like a US growth stock, before dropping to 0.12 in 2024. Its profitability (RMW) loading was negative in every year from 2021 to 2025 (−1.11 in 2025): its returns moved like those of less profitable, growth-style companies. Petrobras carried a value (HML) tilt in every year, between 0.13 and 1.14. In 2026 so far, the two oil companies decoupled from the US market: market loadings of −0.30 for Petrobras and −0.11 for YPF, with an R-squared of 0.06 and 0.11, while Southern Copper's rose to 2.15.</p></div>
<div class="ca-nums"><span><b>0.16 to 0.41</b>R-squared range in 2025</span><span><b>0.69 → 0.12</b>MercadoLibre, 2022 to 2024</span><span><b>−0.30</b>Petrobras market loading, 2026</span></div>
</div>

None of that shows up in a beta on its own, which is the case for running the full model. The 2026 regressions cover the year so far, as far as the French data library has been updated. In Python:

```python
from financetoolkit import Toolkit

south_america = Toolkit(
    tickers=["PBR", "YPF", "VALE", "SCCO", "ITUB", "CIB", "MELI", "GGB"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
)

fama_french = south_america.performance.get_fama_and_french_model(period="yearly")
```

### Is Asia's investment boom fading? {#asia-investment}

Macroeconomic data comes from the [Global Macro Database](https://www.globalmacrodata.com/){:target="_blank"} and the [OECD](https://www.oecd.org/en/data/indicators.html){:target="_blank"}, covers 60+ countries and goes back over a century. Investment as a share of GDP is one of the clearest measures of how an economy is building: a high ratio funds factories, housing and infrastructure, and a falling one usually means an economy is maturing or slowing its build-out.

<div class="mcp-show">
<div class="ca-q"><span class="ca-q__avatar"><i class="fas fa-user" aria-hidden="true"></i></span><p>Compare investment as a share of GDP in India, Vietnam, Indonesia, China, South Korea and Bangladesh since 2000. How fast are they growing now, and how much of that is inflation?</p></div>
<div class="mcp-show__meta"><span><b>6</b> economies</span><span><b>3</b> tool calls</span><span><b>26</b> years of data</span></div>
<details class="mcp-show__trace"><summary><i class="fas fa-list-check" aria-hidden="true"></i> The steps behind the answer</summary><ol><li><code>macroeconomics</code><span>get_investment_to_gdp_ratio, 2000 to 2025</span></li><li><code>macroeconomics</code><span>get_gross_domestic_product with growth=true, 2015 to 2025</span></li><li><code>macroeconomics</code><span>get_inflation_rate, 2025</span></li></ol></details>

<div class="mcp-show__grid">
<div class="mcp-show__cell mcp-show__cell--wide">{% include ft-chart.html id="mcpi-asia-investment" src="/assets/data/article-charts.json" label="Investment as a share of GDP in six Asian economies, 2000 to 2025" %}</div>
<div class="mcp-show__cell mcp-show__cell--wide">{% include ft-chart.html id="mcpi-asia-growth" src="/assets/data/article-charts.json" label="Nominal GDP growth in six Asian economies, 2015 to 2025" %}</div>
<div class="mcp-show__cell mcp-show__cell--wide">{% include ft-chart.html id="mcpi-asia-prices" src="/assets/data/article-charts.json" label="Nominal GDP growth against inflation in 2025" %}</div>
<div class="mcp-show__cell mcp-show__cell--medium">{% include ft-chart.html id="mcpi-asia-inflation" src="/assets/data/article-charts.json" label="Inflation in six Asian economies, 2015 to 2025" %}</div>
</div>
<div class="mcp-show__verdict"><p class="mcp-show__label"><i class="fas fa-lightbulb" aria-hidden="true"></i> What the data shows</p><p>China still invests the largest share, but less than it did: 39.1% of GDP in 2025, down from a peak of 46.3% in 2011 and the lowest since 2002. India peaked earlier, at 41.1% in 2010, fell to 29.0% in 2020 and recovered to 34.4%; Indonesia (34.9%) now invests a slightly larger share. South Korea's 29.2% is its lowest in the 26 years of data. Growth needs inflation next to it: Bangladesh grew 10.2% in nominal terms in 2025, but with 10.0% inflation, while India grew 8.8% with 2.1% inflation. Vietnam combined the fastest nominal growth (11.6%) with 3.3% inflation. China's nominal growth of 4.0% came with flat consumer prices (−0.1%).</p></div>
<div class="ca-nums"><span><b>46.3% → 39.1%</b>China's investment share, 2011 to 2025</span><span><b>10.2% vs 10.0%</b>Bangladesh nominal growth vs inflation</span><span><b>11.6%</b>Vietnam nominal growth, 2025</span></div>
</div>

Consumer price inflation is not the GDP deflator, so nominal growth minus inflation is only a rough guide to real growth. In Python, the macro data needs no Toolkit instance and no API key:

```python
from financetoolkit import Economics

economics = Economics(start_date="2000-01-01")

investment_share = economics.get_investment_to_gdp_ratio()
nominal_gdp_growth = economics.get_gross_domestic_product(growth=True)
inflation = economics.get_inflation_rate()
```

## What This Means for Analysts

Each of the four answers combines several calculations, and each would be hard to get right from a model's memory: a P/E for the right fiscal year, a weekly RSI through a crash, 48 factor regressions, and a ratio from a macro database. With the server, the assistant decides what to calculate and explains the result, but the numbers come from documented code. If you doubt a figure, the [documentation](/projects/financetoolkit/docs) gives the formula, and the Python lines above reproduce it.

The limits are the usual ones. The data is only as good as the filings and the provider, and fiscal years, currencies and share classes need the care the server's notes point out. The 2015 start of the chip comparison needs a paid FMP plan, since the free plan covers five years. RSI readings, factor loadings and investment ratios describe what happened; they don't forecast it. None of this is investment advice.

The [MCP server page](/projects/financetoolkit/mcp#example-conversations) has four more worked conversations, and [How to Connect Claude to Live Financial Data](/articles/connect-claude-to-financial-data) has ten shorter questions to try. Problems or ideas for a new tool are welcome as an issue on [GitHub](https://github.com/JerBouma/FinanceToolkit/issues){:target="_blank"}.

> **Try this with the Finance Toolkit MCP:** *"Compare the operating margin, return on invested capital and EV/EBITDA of ASML, Applied Materials, Lam Research and KLA over the last five years. Which one does the market pay the most for per unit of return on capital?"*

{% include ft-charts-script.html %}
