---
title: How to Find and Analyze Stocks and ETFs with Claude
seo_title: "Find and Analyze Stocks and ETFs with Claude"
date: 2026-10-10
last_modified_at: 2026-10-13
permalink: /articles/find-stocks-and-etfs-with-claude
redirect_from:
  - /articles/find-stocks-etfs-funds-with-claude
excerpt: "Claude lists companies and ETFs from memory, and memory goes stale. Connect the free Finance Database MCP server to find every stock, ETF or index that fits a question, then the Finance Toolkit MCP server to analyze them: margins, returns, drawdowns and currency effects, in one conversation."
description: "Use Claude as a stock and ETF screener and analyst: find 300,000+ instruments with the Finance Database MCP, then analyze them with the Finance Toolkit."
layout: single
classes: wide-sidebar article-document
author_profile: false
collection: article
tags: [MCP Server]
share: true
image: /assets/images/projects/FinanceDatabaseMCP.jpg
---
Every peer comparison starts with a list of peers, and below the large caps that list is hard to get right. Ask an AI assistant for Europe's mid and small-cap drinks makers and you get a list that sounds about right. Look closer and it mixes things up: companies that still trade described as delisted, market caps off by a factor of five or more, micro caps presented as small caps. Language models answer from memory, and memory goes stale.

So I gave the assistant a database instead. The same question then returns twelve companies that all still trade, from Campari and Rémy Cointreau to Kofola, a Czech soft drinks maker few investors outside Central Europe follow, and the analysis that follows finds Kofola earning the highest return on equity in the group, mostly with debt, while Rémy Cointreau lost 69% since 2021.

The [Finance Database MCP server](/projects/financedatabase/mcp) gives Claude the [Finance Database](/projects/financedatabase): 300,000+ stocks, ETFs and indices, each categorized by sector, industry, country, exchange, market cap and issuer. The [Finance Toolkit MCP server](/projects/financetoolkit/mcp) then analyzes whatever it finds: ratios and what drives them, valuations, correlations, drawdowns and currency effects. This article connects both in a few minutes and works through six questions that do exactly that, search first and analysis second.

<div class="ca-strip">
  <div><strong>2 connectors</strong><span>one to find, one to analyze, in the same conversation</span></div>
  <div><strong>300,000+</strong><span>stocks, ETFs, indices, currencies and cryptos to search</span></div>
  <div><strong>500+</strong><span>financial methods to run on what you find</span></div>
  <div><strong>Free</strong><span>hosted servers, open-source code</span></div>
</div>

<div class="article-cta">
  <p class="article-cta__title">Free, hosted and open source</p>
  <p>One URL gives Claude, ChatGPT, Cursor and other AI assistants a searchable, categorized database of 300,000+ financial instruments, with no API key needed. Add the Finance Toolkit server next to it to analyze the results.</p>
  <p class="article-cta__actions"><a href="/projects/financedatabase/mcp" class="hp-btn hp-btn--primary">Explore the server <i class="fas fa-arrow-right" aria-hidden="true"></i></a><a href="/projects/financedatabase/mcp#installation" class="hp-btn hp-btn--ghost">Install guide</a></p>
</div>

## What You Need

<div class="ca-cards ca-cards--3">
  <div><i class="ca-icon fas fa-comments" aria-hidden="true"></i><p class="ca-card-title">A Claude account</p><p>Custom connectors work in claude.ai and Claude Desktop on every plan; the free plan allows one, paid plans allow more.</p></div>
  <div><i class="ca-icon fas fa-magnifying-glass" aria-hidden="true"></i><p class="ca-card-title">The Finance Database server</p><p>For the search. It is free and open source, so it needs no API key, no account and no sign-in.</p></div>
  <div><i class="ca-icon fas fa-calculator" aria-hidden="true"></i><p class="ca-card-title">The Finance Toolkit server</p><p>For the analysis. It needs a <a href="/fmp" target="_blank">Financial Modeling Prep</a> key; the free plan is enough to start.</p></div>
</div>

If you would rather run them yourself, both servers also install locally with one `uvx` command; see the [Finance Database](/projects/financedatabase/mcp#local-clients) and [Finance Toolkit](/projects/financetoolkit/mcp#local-clients) server pages.

## Connecting Claude Desktop or claude.ai

The steps are identical for the desktop app and the web app. You add two connectors, one for each server:

1. Click **Customize** in the left sidebar and open the **Connectors** tab.
2. Click **+** and select **Add custom connector**.
3. Name it *Finance Database*, paste the URL below and click **Add**. No key or sign-in is needed.

    ```
    https://financedatabase.jeroenbouma.com/mcp
    ```

4. Click **+** and **Add custom connector** again, name it *Finance Toolkit*, paste the URL below and click **Add**.

    ```
    https://financetoolkit.jeroenbouma.com/mcp
    ```

5. The first time Claude uses the Finance Toolkit, a browser window asks for your [FMP API key](/fmp){:target="_blank"}. Enter it once and the server remembers it. Both servers now appear in your list of connectors.
{: .ca-steps}

The Finance Database server follows the database itself, which is updated every week, so the lists stay current without anything to update on your side.

## What You Can Ask

Below are six real questions, answered through both servers on October 12, 2026, with prices up to October 9. None of them is a lookup. Each starts with a search in the Finance Database that builds the group, and continues with several Finance Toolkit calculations on it. The insight comes from the combination: a model working from memory can name a few drinks makers, but it cannot tell you which one earns its return on equity with debt, or that long-dated Treasuries started moving with stocks in 2022. Paste any question into Claude as it is, or swap in your own country, sector or issuer.

<div class="ca-nav">
  <a href="#drinks-makers"><i class="fas fa-wine-glass" aria-hidden="true"></i>Drinks makers</a>
  <a href="#european-chipmakers"><i class="fas fa-microchip" aria-hidden="true"></i>Europe's chipmakers</a>
  <a href="#vanguard-treasuries"><i class="fas fa-landmark" aria-hidden="true"></i>Treasury ETFs</a>
  <a href="#uranium-ucits"><i class="fas fa-atom" aria-hidden="true"></i>Uranium ETFs</a>
  <a href="#apple-in-euros"><i class="fas fa-coins" aria-hidden="true"></i>Apple in six currencies</a>
  <a href="#sp-500-dividends"><i class="fas fa-chart-area" aria-hidden="true"></i>The S&amp;P 500, three ways</a>
</div>

### Which of Europe's smaller drinks makers is the best business? {#drinks-makers}

<div class="mcp-show">
<div class="ca-q"><span class="ca-q__avatar"><i class="fas fa-user" aria-hidden="true"></i></span><p>Find Europe's mid and small-cap drinks makers. Which one is the best business? Compare their return on equity and what drives it, their debt, their valuation and how the shares did since 2021.</p></div>
<div class="mcp-show__meta"><span><b>12</b> companies found</span><span><b>8</b> tool calls</span><span><b>2</b> servers</span></div>
<details class="mcp-show__trace"><summary><i class="fas fa-list-check" aria-hidden="true"></i> The steps behind the answer</summary><ol><li><code>equities</code><span>Finance Database: industry Beverages, Mid and Small Cap, European countries, primary listings</span></li><li><code>profitability</code><span>Return on equity, operating margin and net margin, fiscal 2025</span></li><li><code>efficiency</code><span>Asset turnover, fiscal 2025</span></li><li><code>models</code><span>DuPont analysis: the equity multiplier (assets per unit of equity)</span></li><li><code>solvency</code><span>Net debt to EBITDA, fiscal 2025</span></li><li><code>valuation</code><span>EV/EBITDA, fiscal 2025</span></li><li><code>performance</code><span>Total return since January 2021, dividends included</span></li><li><code>risk</code><span>Maximum drawdown since January 2021</span></li></ol></details>

<div class="mcp-show__grid">
<div class="mcp-show__cell mcp-show__cell--wide">{% include ft-chart.html id="fdb-drinks-roe" src="/assets/data/article-charts.json" label="Return on equity of Europe's mid and small-cap drinks makers and its three drivers" %}</div>
<div class="mcp-show__cell">{% include ft-chart.html id="fdb-drinks-lev" src="/assets/data/article-charts.json" label="Return on equity against the equity multiplier" %}</div>
<div class="mcp-show__cell">{% include ft-chart.html id="fdb-drinks-value" src="/assets/data/article-charts.json" label="Operating margin against EV/EBITDA" %}</div>
<div class="mcp-show__cell mcp-show__cell--wide">{% include ft-chart.html id="fdb-drinks-market" src="/assets/data/article-charts.json" label="Net debt to EBITDA, total return and maximum drawdown since 2021" %}</div>
</div>
<div class="mcp-show__verdict"><p class="mcp-show__label"><i class="fas fa-lightbulb" aria-hidden="true"></i> What the data shows</p><p>Kofola, a Czech soft drinks maker, has the highest return on equity in the group at 31.3%, but it comes from its balance sheet, not its margins: it carries 5.2 of assets for every unit of equity, more than any other company here, on a net margin of only 6.3%. Without the leverage, the strongest businesses are Malteries Franco-Belges (a 27.9% net margin and net cash) and Laurent-Perrier (the best operating margin at 25.3%, at 8.2 times EBITDA, among the lowest valuations in the group). The famous names did worst for shareholders: since January 2021, Rémy Cointreau lost 69% and Fever-Tree 62%, dividends included, while Kofola returned 177%.</p></div>
<div class="ca-nums"><span><b>31.3%</b>Kofola return on equity</span><span><b>5.2x</b>Kofola equity multiplier, the highest</span><span><b>+177% vs −69%</b>Kofola vs Rémy Cointreau since 2021</span></div>
</div>

### Are Europe's large chipmakers priced for their profits? {#european-chipmakers}

<div class="mcp-show">
<div class="ca-q"><span class="ca-q__avatar"><i class="fas fa-user" aria-hidden="true"></i></span><p>Find the large European semiconductor companies. Compare their operating margins over five years, their return on equity against their valuation, how closely the shares move together and how they did since 2021.</p></div>
<div class="mcp-show__meta"><span><b>7</b> companies found</span><span><b>18</b> European listings</span><span><b>6</b> tool calls</span></div>
<details class="mcp-show__trace"><summary><i class="fas fa-list-check" aria-hidden="true"></i> The steps behind the answer</summary><ol><li><code>equities</code><span>Finance Database: industry Semiconductors, Large and Mega Cap, European exchanges</span></li><li><code>profitability</code><span>Operating margin, 2020 to 2025, and return on equity, fiscal 2025</span></li><li><code>valuation</code><span>EV/EBITDA, fiscal 2025</span></li><li><code>performance</code><span>Correlation of weekly returns since March 2022</span></li><li><code>market_data</code><span>Growth of 100 since January 2021, dividends included</span></li><li><code>risk</code><span>Maximum drawdown since January 2021</span></li></ol></details>

<div class="mcp-show__grid">
<div class="mcp-show__cell">{% include ft-chart.html id="fdb-chip-margins" src="/assets/data/article-charts.json" label="Operating margins of Europe's large chipmakers" %}</div>
<div class="mcp-show__cell">{% include ft-chart.html id="fdb-chip-value" src="/assets/data/article-charts.json" label="Return on equity against EV/EBITDA" %}</div>
<div class="mcp-show__cell">{% include ft-chart.html id="fdb-chip-corr" src="/assets/data/article-charts.json" label="Correlation of weekly returns of Europe's large chipmakers" %}</div>
<div class="mcp-show__cell">{% include ft-chart.html id="fdb-chip-market" src="/assets/data/article-charts.json" label="Growth of 100 and maximum drawdown since 2021" %}</div>
</div>
<div class="mcp-show__verdict"><p class="mcp-show__label"><i class="fas fa-lightbulb" aria-hidden="true"></i> What the data shows</p><p>The seven are two groups under one label. The equipment makers ASML, ASM International and BE Semiconductor kept operating margins near 30% to 35% and turned 100 into 405 to 475 since January 2021; the chipmakers Infineon, NXP and STMicroelectronics turned it into 144 to 181. The correlations show the same split: ASML moves most with ASM International (0.81), Infineon with STMicroelectronics (0.76). Valuations follow the cycle more than profitability: STMicroelectronics trades at 11 times EBITDA on a return on equity of 0.9%, BE Semiconductor at 52 times on 28.7%. ASML pairs the highest return on equity (50.5%) with a mid-range 28 times.</p></div>
<div class="ca-nums"><span><b>50.5%</b>ASML return on equity, the highest</span><span><b>0.81</b>ASML and ASM International correlation</span><span><b>475 vs 148</b>100 since 2021, ASM International vs STMicroelectronics</span></div>
</div>

### Do Vanguard's Treasury ETFs still protect a stock portfolio? {#vanguard-treasuries}

<div class="mcp-show">
<div class="ca-q"><span class="ca-q__avatar"><i class="fas fa-user" aria-hidden="true"></i></span><p>Which Treasury ETFs does Vanguard list in the US? Compare how each did since 2020, year by year and against the S&amp;P 500, and check whether they still move against stocks.</p></div>
<div class="mcp-show__meta"><span><b>5</b> ETFs found</span><span><b>12</b> years of weekly returns</span><span><b>5</b> tool calls</span></div>
<details class="mcp-show__trace"><summary><i class="fas fa-list-check" aria-hidden="true"></i> The steps behind the answer</summary><ol><li><code>etfs</code><span>Finance Database: family Vanguard, category Treasury Bonds, US exchanges</span></li><li><code>market_data</code><span>Weekly prices with distributions since 2014, plus VOO for the S&amp;P 500</span></li><li><code>performance</code><span>Calendar-year returns, 2020 to 2026</span></li><li><code>performance</code><span>Correlation with the S&amp;P 500, 2014 to 2021 and 2022 to 2026</span></li><li><code>risk</code><span>Volatility and maximum drawdown since 2020</span></li></ol></details>

<div class="mcp-show__grid">
<div class="mcp-show__cell">{% include ft-chart.html id="fdb-treasuries" src="/assets/data/article-charts.json" label="Value of 100 invested in Vanguard's US Treasury ETFs since 2020" %}</div>
<div class="mcp-show__cell">{% include ft-chart.html id="fdb-treas-corr" src="/assets/data/article-charts.json" label="Correlation of Vanguard's Treasury ETFs with the S&P 500 before and after 2022" %}</div>
<div class="mcp-show__cell">{% include ft-chart.html id="fdb-treas-years" src="/assets/data/article-charts.json" label="Calendar-year returns of Vanguard's Treasury ETFs and VOO" %}</div>
<div class="mcp-show__cell">{% include ft-chart.html id="fdb-treas-risk" src="/assets/data/article-charts.json" label="Annual return against volatility since 2020" %}</div>
</div>
<div class="mcp-show__verdict"><p class="mcp-show__label"><i class="fas fa-lightbulb" aria-hidden="true"></i> What the data shows</p><p>Long Treasuries stopped working as a hedge. From 2014 to 2021, all four funds moved against the S&amp;P 500 in a typical week, with correlations between −0.20 and −0.38. Since 2022 they move with it, at +0.14 to +0.16. In 2022 the extended-duration EDV lost 39.2% in the same year the S&amp;P 500 lost 18.2%, and it has not come back: since 2020 it lost 8.5% a year, with more volatility (20.4%) than the S&amp;P 500 itself (18.8%). Only the short-term VGSH earned a real return since 2020, 1.8% a year; the intermediate VGIT made 0.5%.</p></div>
<div class="ca-nums"><span><b>−0.38 → +0.14</b>VGSH correlation with stocks</span><span><b>−39.2%</b>EDV in 2022</span><span><b>20.4% vs 18.8%</b>volatility, EDV vs S&amp;P 500</span></div>
</div>

### Is every uranium ETF the same bet? {#uranium-ucits}

<div class="mcp-show">
<div class="ca-q"><span class="ca-q__avatar"><i class="fas fa-user" aria-hidden="true"></i></span><p>Find the uranium ETFs, including the UCITS versions listed in Europe. How did the main ones do since February 2023, year by year and against their worst fall, and did the UCITS version keep up with the US fund?</p></div>
<div class="mcp-show__meta"><span><b>31</b> listings found</span><span><b>18</b> of them UCITS</span><span><b>6</b> compared in US dollars</span></div>
<details class="mcp-show__trace"><summary><i class="fas fa-list-check" aria-hidden="true"></i> The steps behind the answer</summary><ol><li><code>etfs</code><span>Finance Database: "uranium" in the name, every exchange and currency</span></li><li><code>search_instruments</code><span>Finance Database: Cameco, one of the largest uranium miners, as a reference</span></li><li><code>market_data</code><span>Prices with distributions since February 2023, US dollar listings</span></li><li><code>performance</code><span>Calendar-year returns and the correlation of weekly returns</span></li><li><code>risk</code><span>Maximum drawdown since February 2023</span></li></ol></details>

<div class="mcp-show__grid">
<div class="mcp-show__cell mcp-show__cell--wide">{% include ft-chart.html id="fdb-uranium-growth" src="/assets/data/article-charts.json" label="Value of 100 invested in uranium ETFs and Cameco since February 2023" %}</div>
<div class="mcp-show__cell mcp-show__cell--medium">{% include ft-chart.html id="fdb-uranium-corr" src="/assets/data/article-charts.json" label="Correlation of weekly returns of uranium ETFs and Cameco" %}</div>
<div class="mcp-show__cell">{% include ft-chart.html id="fdb-uranium-years" src="/assets/data/article-charts.json" label="Calendar-year returns of uranium ETFs" %}</div>
<div class="mcp-show__cell">{% include ft-chart.html id="fdb-uranium-risk" src="/assets/data/article-charts.json" label="Total return against maximum drawdown of uranium ETFs" %}</div>
</div>
<div class="mcp-show__verdict"><p class="mcp-show__label"><i class="fas fa-lightbulb" aria-hidden="true"></i> What the data shows</p><p>One label, two different bets. The broad funds URA and NLR, which also hold utilities and reactor builders, doubled since February 2023 (+100% and +96%). The pure miner funds lagged, URNM at +45% and the junior miners in URNJ at +15%, and fell further on the way: −51% and −59% at their worst. The gap opened in 2024, when NLR rose 14% and the miner funds lost 14% and 18%. The UCITS twin URNU moved with URA week by week (a correlation of 0.95) but ended ten points behind, at +90%. And Cameco, a single stock, returned 219%, more than any of the funds.</p></div>
<div class="ca-nums"><span><b>+100% vs +45%</b>URA vs miners fund URNM</span><span><b>0.95</b>URA and UCITS twin URNU</span><span><b>+219%</b>Cameco on its own</span></div>
</div>

### What did Apple return in each currency? {#apple-in-euros}

<div class="mcp-show">
<div class="ca-q"><span class="ca-q__avatar"><i class="fas fa-user" aria-hidden="true"></i></span><p>Which ticker belongs to ISIN US0378331005, where else does it trade, and what did it return on each listing since January 2025?</p></div>
<div class="mcp-show__meta"><span><b>19</b> listings of one ISIN</span><span><b>15</b> exchanges</span><span><b>6</b> currencies</span></div>
<details class="mcp-show__trace"><summary><i class="fas fa-list-check" aria-hidden="true"></i> The steps behind the answer</summary><ol><li><code>search_instruments</code><span>Finance Database: the ISIN, every listing with its exchange and currency</span></li><li><code>market_data</code><span>Prices of seven listings, one per market, since January 2025</span></li><li><code>market_data</code><span>Exchange rates of the dollar against the euro, peso, real and others</span></li></ol></details>

<div class="mcp-show__grid">
<div class="mcp-show__cell mcp-show__cell--medium">{% include ft-chart.html id="fdb-isin-listings" src="/assets/data/article-charts.json" label="Listings of Apple's ISIN by country" %}</div>
<div class="mcp-show__cell">{% include ft-chart.html id="fdb-apple-listings" src="/assets/data/article-charts.json" label="Apple's return on each of seven listings since January 2025" %}</div>
<div class="mcp-show__cell">{% include ft-chart.html id="fdb-apple-dollar" src="/assets/data/article-charts.json" label="The dollar against five currencies since January 2025" %}</div>
<div class="mcp-show__cell mcp-show__cell--wide">{% include ft-chart.html id="fdb-apple-fx" src="/assets/data/article-charts.json" label="Apple on Nasdaq, Xetra, Buenos Aires and São Paulo since January 2025" %}</div>
</div>
<div class="mcp-show__verdict"><p class="mcp-show__label"><i class="fas fa-lightbulb" aria-hidden="true"></i> What the data shows</p><p>One share, returns from 12% to 92%. In dollars, Apple rose 39.1% since January 2025. On Xetra in euros it rose 25.6%, because the dollar lost 8.0% against the euro; in São Paulo it rose 12.1%, as the dollar lost 19.5% against the real. In Buenos Aires it rose 91.9%, most of it the peso's fall: the dollar rose 47% against it. The two charts side by side explain each other: each listing is roughly Apple's dollar return plus the currency move.</p></div>
<div class="ca-nums"><span><b>39.1%</b>in dollars</span><span><b>25.6%</b>in euros on Xetra</span><span><b>91.9%</b>in Argentine pesos</span></div>
</div>

### How much do dividends and weighting change the S&amp;P 500? {#sp-500-dividends}

<div class="mcp-show">
<div class="ca-q"><span class="ca-q__avatar"><i class="fas fa-user" aria-hidden="true"></i></span><p>Find the S&amp;P 500, its total return version and its equal-weight version, and compare them since 2016, year by year.</p></div>
<div class="mcp-show__meta"><span><b>895</b> indices with "S&amp;P 500" in the name</span><span><b>4</b> versions compared</span><span><b>11</b> years</span></div>
<details class="mcp-show__trace"><summary><i class="fas fa-list-check" aria-hidden="true"></i> The steps behind the answer</summary><ol><li><code>indices</code><span>Finance Database: "S&amp;P 500" in the name, from sector and factor variants to currency-hedged ones</span></li><li><code>etfs</code><span>Finance Database: the equal-weight S&amp;P 500 ETF, RSP</span></li><li><code>market_data</code><span>^GSPC, ^SP500TR, ^SPXEW and RSP since January 2016</span></li><li><code>performance</code><span>Calendar-year returns, 2016 to 2026</span></li></ol></details>

<div class="mcp-show__grid">
<div class="mcp-show__cell">{% include ft-chart.html id="fdb-sp500-tr" src="/assets/data/article-charts.json" label="The S&P 500 price, total return and equal-weight versions since 2016" %}</div>
<div class="mcp-show__cell">{% include ft-chart.html id="fdb-sp500-years" src="/assets/data/article-charts.json" label="Calendar-year returns of the S&P 500 versions" %}</div>
</div>
<div class="mcp-show__verdict"><p class="mcp-show__label"><i class="fas fa-lightbulb" aria-hidden="true"></i> What the data shows</p><p>Since January 2016, 100 in the headline index became 388; with dividends reinvested, it became 466. The bigger choice was the weighting. The equal-weight index, which gives each of the 500 companies the same weight, reached 280, or 337 with dividends through the RSP fund. Equal weight beat the index in 2016, 2021 and 2022, then trailed the total return version by 7 to 13 points a year from 2023 to 2025, as a handful of large companies carried the index.</p></div>
<div class="ca-nums"><span><b>466 vs 388</b>with and without dividends</span><span><b>337</b>equal weight, with dividends</span><span><b>−12.6 points</b>equal weight vs index, 2023</span></div>
</div>

Every list comes from the open [Finance Database](/projects/financedatabase) and every number from a documented [Finance Toolkit](/projects/financetoolkit/docs) method, so you can check both. The Finance Toolkit server answers many more questions on its own, from valuation models to macro data, in [How to Connect Claude to Live Financial Data for Stock Analysis](/articles/connect-claude-to-financial-data).

<div class="article-cta">
  <p class="article-cta__title">Ask your own questions</p>
  <p>These six examples use a fraction of what the two servers can do together. Connect them in a few minutes and ask for any market, sector, issuer or fund, and then for the numbers behind it.</p>
  <p class="article-cta__actions"><a href="/projects/financedatabase/mcp" class="hp-btn hp-btn--primary">Connect the server <i class="fas fa-arrow-right" aria-hidden="true"></i></a><a href="/projects/financetoolkit/mcp" class="hp-btn hp-btn--ghost">Finance Toolkit server</a></p>
</div>

## Tips for Better Answers

<div class="ca-cards ca-cards--3">
  <div><i class="ca-icon fas fa-building-columns" aria-hidden="true"></i><p class="ca-card-title">Name the exchange</p><p>Most large companies have many listings. "On Euronext Amsterdam" or "on US exchanges" gets you the ticker you will actually use.</p></div>
  <div><i class="ca-icon fas fa-ruler" aria-hidden="true"></i><p class="ca-card-title">Use the size tiers</p><p>Market cap comes in tiers: Mega ($200B+), Large ($10B+), Mid ($2B+), Small ($300M+), Micro and Nano. "Large or Mega Cap" is a quick way to cut a long list.</p></div>
  <div><i class="ca-icon fas fa-list-ul" aria-hidden="true"></i><p class="ca-card-title">Ask what exists first</p><p>"Which industries are there in Health Care?" shows the exact categories before you filter on one.</p></div>
  <div><i class="ca-icon fas fa-fingerprint" aria-hidden="true"></i><p class="ca-card-title">Use identifiers</p><p>An ISIN, CUSIP or FIGI from a statement or fund report is the most precise way to find a security.</p></div>
  <div><i class="ca-icon fas fa-arrow-down-wide-short" aria-hidden="true"></i><p class="ca-card-title">Ask for the count</p><p>Answers come 25 rows at a time. Ask how many there are in total and Claude pages through or narrows the search.</p></div>
  <div><i class="ca-icon fas fa-link" aria-hidden="true"></i><p class="ca-card-title">Pair it</p><p>Use the Finance Database to find, and the Finance Toolkit to analyze: the tickers carry over between the two.</p></div>
</div>

## Not a Claude User?

Both servers work with any MCP-compatible client. The links below go to the steps for the Finance Database; the [Finance Toolkit MCP server](/projects/financetoolkit/mcp) page has the same steps for the Finance Toolkit, including where to enter your FMP key:

<div class="ca-clients">
  <a href="/projects/financedatabase/mcp#remote-chatgpt"><i class="fas fa-comment-dots" aria-hidden="true"></i>ChatGPT<i class="fas fa-arrow-right ca-clients__go" aria-hidden="true"></i></a>
  <a href="/projects/financedatabase/mcp#remote-vs-code"><i class="fab fa-microsoft" aria-hidden="true"></i>VS Code and GitHub Copilot<i class="fas fa-arrow-right ca-clients__go" aria-hidden="true"></i></a>
  <a href="/projects/financedatabase/mcp#remote-cursor"><i class="fas fa-i-cursor" aria-hidden="true"></i>Cursor<i class="fas fa-arrow-right ca-clients__go" aria-hidden="true"></i></a>
  <a href="/projects/financedatabase/mcp#remote-windsurf"><i class="fas fa-wind" aria-hidden="true"></i>Windsurf<i class="fas fa-arrow-right ca-clients__go" aria-hidden="true"></i></a>
  <a href="/projects/financedatabase/mcp#remote-codex"><i class="fas fa-code" aria-hidden="true"></i>Codex CLI<i class="fas fa-arrow-right ca-clients__go" aria-hidden="true"></i></a>
  <a href="/projects/financedatabase/mcp#remote-gemini"><i class="fab fa-google" aria-hidden="true"></i>Gemini CLI<i class="fas fa-arrow-right ca-clients__go" aria-hidden="true"></i></a>
</div>

If you would rather skip the assistant, the [Finance Database](/projects/financedatabase) Python package gives you the same data in pandas with `pip install financedatabase`. Wrong classifications and missing symbols are welcome as an issue or pull request on [GitHub](https://github.com/JerBouma/FinanceDatabase){:target="_blank"}.

> **Try this with the Finance Database and Finance Toolkit MCP servers:** *"Find the listed water utilities in Europe, then compare their dividend yield and debt to equity over the last five years."*

{% include ft-charts-script.html %}
