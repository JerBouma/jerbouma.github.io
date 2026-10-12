---
title: How to Find and Analyze Stocks and ETFs with Claude
seo_title: "Find and Analyze Stocks and ETFs with Claude"
date: 2026-10-10
last_modified_at: 2026-10-13
permalink: /articles/find-stocks-and-etfs-with-claude
redirect_from:
  - /articles/find-stocks-etfs-funds-with-claude
excerpt: "Claude lists companies and ETFs from memory, and memory goes stale. Connect the free Finance Database MCP server to find every stock, ETF or index that fits a question, then the Finance Toolkit MCP server to analyze them: margins, returns, drawdowns and currency effects, in one conversation."
description: "Use Claude as a stock and ETF screener and analyst: find 300,000+ stocks, ETFs and indices with the Finance Database MCP, then analyze them with the Finance Toolkit."
layout: single
classes: wide-sidebar article-document
author_profile: false
collection: article
tags: [MCP Server]
share: true
image: /assets/images/projects/FinanceDatabaseMCP.jpg
---
Since January 2020, Vanguard's short-term Treasury ETF turned 100 into 112.8. Its extended-duration Treasury ETF turned the same 100 into 53.7, and only reached its lowest point in September 2026. Both sit in the same category, from the same issuer, holding the same government's bonds. A list of "Vanguard Treasury ETFs" tells you none of that; the analysis of each one does.

That is the gap this article closes. A language model reasons well about companies and funds, but it lists them from memory, and memory goes stale: delisted names, wrong sizes, missing listings. The [Finance Database MCP server](/projects/financedatabase/mcp) gives Claude the [Finance Database](/projects/financedatabase) instead, 300,000+ stocks, ETFs and indices, each categorized by sector, industry, country, exchange, market cap and issuer. The [Finance Toolkit MCP server](/projects/financetoolkit/mcp) then analyzes whatever it finds: financial ratios, returns, drawdowns. This article connects both in a few minutes and works through six questions that do exactly that, search first and analysis second.

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

The steps are identical for the desktop app and the web app:

1. Click **Customize** in the left sidebar and open the **Connectors** tab.
2. Click **+** and select **Add custom connector**.
3. Enter a name, e.g. *Finance Database*, and paste the server URL:

    ```
    https://financedatabase.jeroenbouma.com/mcp
    ```

4. Click **Add**. The Finance Database now appears in your list of connectors.
5. Repeat for the Finance Toolkit with `https://financetoolkit.jeroenbouma.com/mcp`. On its first tool call a browser window asks for your FMP key; enter it once.
{: .ca-steps}

The Finance Database server follows the database itself, which is updated every week, so the lists stay current without anything to update on your side.

## What You Can Ask

Below are six real questions, each answered through both servers on October 12, 2026. Each starts with a search in the Finance Database and continues with an analysis in the Finance Toolkit. **The question is what you type, the chart is what comes back.** Paste any of them into Claude as they are, or swap in your own country, sector or issuer.

<div class="ca-nav">
  <a href="#european-chipmakers"><i class="fas fa-microchip" aria-hidden="true"></i>Europe's chipmakers</a>
  <a href="#drinks-makers"><i class="fas fa-wine-glass" aria-hidden="true"></i>Drinks makers</a>
  <a href="#vanguard-treasuries"><i class="fas fa-landmark" aria-hidden="true"></i>Treasury ETFs</a>
  <a href="#uranium-ucits"><i class="fas fa-atom" aria-hidden="true"></i>US vs UCITS</a>
  <a href="#apple-in-euros"><i class="fas fa-euro-sign" aria-hidden="true"></i>Apple in euros</a>
  <a href="#sp-500-dividends"><i class="fas fa-chart-area" aria-hidden="true"></i>Dividends</a>
</div>

### How profitable are Europe's large chipmakers? {#european-chipmakers}

<div class="ca-q"><span class="ca-q__avatar"><i class="fas fa-user" aria-hidden="true"></i></span><p>Find the large European semiconductor companies, then compare their operating margins over the last five years.<span class="ca-q__tool">Finance Database MCP · equities → Finance Toolkit MCP · profitability</span></p></div>

<div class="ca-nums"><span><b>7</b>companies found</span><span><b>34.6%</b>ASML 2025</span><span><b>27.5% → 2.7%</b>STMicroelectronics since 2022</span></div>

{% include ft-chart.html id="fdb-chip-margins" src="/assets/data/article-charts.json" label="Operating margins of Europe's large chipmakers" %}

The search returns seven companies with 18 listings on European exchanges, from ASML and Infineon to Technoprobe. The second step runs each through the Finance Toolkit's [operating margin](/projects/financetoolkit/docs/ratios/operating-margin), operating income as a share of revenue. Same industry, very different businesses: the equipment makers ASML, ASM International and BE Semiconductor Industries kept margins around 29% to 35% in 2025, while the chipmakers Infineon and STMicroelectronics went from roughly a quarter of revenue at their peak to 13.9% and 2.7%. Margins are per fiscal year, and NXP is measured on its primary listing in New York.

<div class="ca-take"><p>The search gives the peer group; the analysis shows how different its members are. A sector average would hide a range from 2.7% to 34.6%.</p></div>

### Which of Europe's smaller drinks makers earns the most? {#drinks-makers}

<div class="ca-q"><span class="ca-q__avatar"><i class="fas fa-user" aria-hidden="true"></i></span><p>Find Europe's mid and small-cap drinks makers, then compare their operating margin and return on equity for 2025.<span class="ca-q__tool">Finance Database MCP · equities → Finance Toolkit MCP · profitability</span></p></div>

<div class="ca-nums"><span><b>25.3%</b>Laurent-Perrier operating margin</span><span><b>31.3%</b>Kofola return on equity</span><span><b>4.1%</b>Rémy Cointreau return on equity</span></div>

{% include ft-chart.html id="fdb-drinks" src="/assets/data/article-charts.json" label="Operating margin and return on equity of Europe's mid and small-cap drinks makers" %}

The search finds the beverage makers between $300 million and $10 billion, from Campari and Rémy Cointreau to Fever-Tree, Irn-Bru maker A.G. Barr and Spa water from Spadel. The analysis then splits them two ways. Champagne house Laurent-Perrier keeps the most of each euro of sales, an operating margin of 25.3%. The best return on shareholders' money comes from Kofola, a Czech soft drinks maker that few investors outside Central Europe follow: 31.3%, ahead of Royal Unibrew at 23.8%. The famous spirits names trail: Campari at 9.0% and Rémy Cointreau at 4.1%, after its cognac sales fell back.

Return on equity also rises with debt, so a high number is a reason to look closer, not a verdict. That is the point of having the analysis next to the list.

<div class="ca-take"><p>The names everyone knows are not the ones earning the most. A screen that stops at the famous brands would have missed the best returns in the group.</p></div>

### How much did Vanguard's Treasury ETFs fall? {#vanguard-treasuries}

<div class="ca-q"><span class="ca-q__avatar"><i class="fas fa-user" aria-hidden="true"></i></span><p>Which Treasury ETFs does Vanguard list in the US, and how did each one perform since 2020?<span class="ca-q__tool">Finance Database MCP · etfs → Finance Toolkit MCP · market data</span></p></div>

<div class="ca-nums"><span><b>112.8</b>short-term, from 100</span><span><b>53.7</b>extended duration, from 100</span><span><b>-59.8%</b>worst fall, September 2026</span></div>

{% include ft-chart.html id="fdb-treasuries" src="/assets/data/article-charts.json" label="Value of 100 invested in Vanguard's US Treasury ETFs since 2020" %}

The search returns five Treasury ETFs; four of them have traded since 2020 (the fifth, VTG, only started in July 2025). With distributions reinvested, 100 in the short-term VGSH grew to 112.8, while the intermediate VGIT ended at 102.8, the long-term VGLT at 72.9 and the extended-duration EDV at 53.7. The difference is duration: how far a bond's price moves when interest rates change. When rates rose in 2022, the short fund barely moved and the long ones fell hard. EDV's worst point, 59.8% below its peak, came only in September 2026.

<div class="ca-take"><p>"Treasury ETF" says what a fund holds, not how it behaves. The category is the same; the risk is not.</p></div>

### Did the UCITS version keep up with the US fund? {#uranium-ucits}

<div class="ca-q"><span class="ca-q__avatar"><i class="fas fa-user" aria-hidden="true"></i></span><p>Which uranium ETFs are UCITS funds listed in Europe, and did the UCITS version of URA keep up with the US fund?<span class="ca-q__tool">Finance Database MCP · etfs → Finance Toolkit MCP · market data</span></p></div>

<div class="ca-nums"><span><b>31</b>uranium ETF listings</span><span><b>18</b>of them UCITS</span><span><b>209.9 vs 207.0</b>US vs UCITS, from 100</span></div>

{% include ft-chart.html id="fdb-uranium-perf" src="/assets/data/article-charts.json" label="Value of 100 invested in URA and its UCITS version URNU" %}

European retail investors generally need UCITS funds, so the US fund everyone talks about is often not the one they can buy. The search finds 31 uranium ETF listings, 18 of them UCITS versions in London, Frankfurt, Paris, Milan and Zurich, including URNU, Global X's European twin of URA. The analysis compares the two in the same currency: since January 2023, 100 in URA became 209.9 and 100 in URNU 207.0. Both fell about 36% from peak to trough in early 2025.

<div class="ca-take"><p>The UCITS twin tracked the US fund within a few points over almost four years. Investors who can only buy the European version gave up very little.</p></div>

### What did Apple return in euros? {#apple-in-euros}

<div class="ca-q"><span class="ca-q__avatar"><i class="fas fa-user" aria-hidden="true"></i></span><p>Which ticker belongs to ISIN US0378331005, where else does it trade, and how did it do in euros compared with dollars since January 2025?<span class="ca-q__tool">Finance Database MCP · search_instruments → Finance Toolkit MCP · market data</span></p></div>

<div class="ca-nums"><span><b>19</b>listings of one ISIN</span><span><b>139.3</b>in dollars, from 100</span><span><b>127.0</b>in euros, from 100</span></div>

{% include ft-chart.html id="fdb-apple-fx" src="/assets/data/article-charts.json" label="Apple in dollars on Nasdaq and in euros on Xetra since January 2025" %}

The ISIN, the code on a broker statement, belongs to Apple, and the search finds it on 19 listings across 15 exchanges in six currencies. The analysis compares two of them: AAPL on Nasdaq in dollars and APC.DE on Xetra in euros. Since January 2025, 100 became 139.3 in dollars and 127.0 in euros. Same company, same shares; the gap is the dollar's fall against the euro.

<div class="ca-take"><p>For a euro investor, the currency was a third of the story. The listing you buy decides which return you see.</p></div>

### How much do dividends add to the S&amp;P 500? {#sp-500-dividends}

<div class="ca-q"><span class="ca-q__avatar"><i class="fas fa-user" aria-hidden="true"></i></span><p>Find the S&amp;P 500 and its total return version, then compare them since 2016.<span class="ca-q__tool">Finance Database MCP · indices → Finance Toolkit MCP · market data</span></p></div>

<div class="ca-nums"><span><b>895</b>indices with "S&amp;P 500" in the name</span><span><b>406.4</b>price index, from 100</span><span><b>487.4</b>total return, from 100</span></div>

{% include ft-chart.html id="fdb-sp500-tr" src="/assets/data/article-charts.json" label="The S&P 500 price index and total return index since 2016" %}

The search finds 895 indices with "S&P 500" in the name, from sector and factor variants to currency-hedged ones, and picks out ^GSPC, the headline price index, and ^SP500TR, the total return version. Since January 2016, the price index turned 100 into 406.4; with dividends reinvested it became 487.4, about a fifth more.

<div class="ca-take"><p>The headline index leaves out the dividends. Benchmark a fund against the total return version, or it will look better than it is.</p></div>

### What happens when a filter doesn't match? {#did-you-mean}

<div class="ca-q"><span class="ca-q__avatar"><i class="fas fa-user" aria-hidden="true"></i></span><p>List the megacap tech companies in Holland.<span class="ca-q__tool">Finance Database MCP · equities</span></p></div>

The database uses formal names: the sector "Information Technology", the country "Netherlands" and the tier "Mega Cap". The server translates everyday words into those names, so "Tech", "Holland" and "megacap" go straight to ASML, and accents are optional ("Cote d'Ivoire" finds the Ivory Coast). When a word is simply misspelled, it answers with the closest matches instead of an empty list:

```
The country 'Netherland' is not available in the database.
Did you mean 'Netherlands' or 'Thailand' or 'Switzerland' or 'New Zealand' instead of 'Netherland'?
```

<div class="ca-take"><p>Plain language in, exact classifications out. You can phrase things the way you normally would; the exact filter values are the server's problem.</p></div>

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

The same server works with any MCP-compatible client, each with step-by-step instructions on the [Finance Database MCP server](/projects/financedatabase/mcp#installation) page:

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
