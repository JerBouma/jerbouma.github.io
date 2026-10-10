---
title: How to Find Stocks, ETFs and Funds with Claude
seo_title: "Find Stocks, ETFs and Funds with Claude"
date: 2026-10-10
last_modified_at: 2026-10-10
permalink: /articles/find-stocks-etfs-funds-with-claude
excerpt: "Claude can't list every company in a sector or every ETF of an issuer from memory. With the free, hosted Finance Database MCP server it searches 300,000+ stocks, ETFs, funds and indices by sector, country, exchange and ISIN, with no API key and no installation."
description: "Use Claude as a stock and ETF screener: the free Finance Database MCP server finds 300,000+ stocks, ETFs and funds by sector, country, exchange or ISIN."
layout: single
classes: wide-sidebar article-document
author_profile: false
collection: article
tags: [MCP Server]
share: true
image: /assets/images/projects/FinanceDatabaseMCP.jpg
---
Ask Claude *"which uranium ETFs can I buy?"* and you will probably get URA and URNM, the two best-known US funds. On October 10, 2026 the Finance Database listed 21 uranium ETF listings from ten issuers across eight markets, seven of them UCITS versions in London, Frankfurt and Milan. If you are a European investor, those are often the only ones you can buy, and they are exactly the ones a model's memory leaves out.

Finding things is a different problem from analyzing them. A language model reasons well about companies, but it lists them from memory, and memory favors the famous names, the US tickers and whatever was in the training data. The [Finance Database MCP server](/projects/financedatabase/mcp) gives Claude the [Finance Database](/projects/financedatabase) instead: 300,000+ equities, ETFs, funds, indices, currencies and cryptocurrencies, each categorized by sector, industry, country, exchange, market cap and issuer. This article connects it to Claude in about a minute and then works through eight real questions, from screening stocks to turning an ISIN into the right ticker.

<div class="ca-strip">
  <div><strong>1 minute</strong><span>to connect Claude Desktop, claude.ai or Claude Code</span></div>
  <div><strong>300,000+</strong><span>stocks, ETFs, funds, indices, currencies and cryptos</span></div>
  <div><strong>No API key</strong><span>no account, no sign-in, nothing to install</span></div>
  <div><strong>Free</strong><span>hosted server, open-source code</span></div>
</div>

<div class="article-cta">
  <p class="article-cta__title">Free, hosted and open source</p>
  <p>One URL gives Claude, ChatGPT, Cursor and other AI assistants a searchable, categorized database of 300,000+ financial instruments, with no API key needed.</p>
  <p class="article-cta__actions"><a href="/projects/financedatabase/mcp" class="hp-btn hp-btn--primary">Explore the server <i class="fas fa-arrow-right" aria-hidden="true"></i></a><a href="/projects/financedatabase/mcp#installation" class="hp-btn hp-btn--ghost">Install guide</a></p>
</div>

## What You Need

<div class="ca-cards">
  <div><i class="ca-icon fas fa-comments" aria-hidden="true"></i><p class="ca-card-title">A Claude account</p><p>Custom connectors work in claude.ai and Claude Desktop on every plan; the free plan allows one, so this can be it. Claude Code supports MCP servers on every plan.</p></div>
  <div><i class="ca-icon fas fa-unlock" aria-hidden="true"></i><p class="ca-card-title">Nothing else</p><p>The Finance Database is free and open source, so the server needs no API key, no account and no sign-in. Add the URL and start asking.</p></div>
</div>

If you would rather not use the hosted server, the [local installation](/projects/financedatabase/mcp#local-clients) runs the same server on your own machine with one `uvx` command, and the database is cached there after the first download.

## Connecting Claude Desktop or claude.ai

The steps are identical for the desktop app and the web app:

1. Click **Customize** in the left sidebar and open the **Connectors** tab.
2. Click **+** and select **Add custom connector**.
3. Enter a name, e.g. *Finance Database*, and paste the server URL:

    ```
    https://financedatabase.jeroenbouma.com/mcp
    ```

4. Click **Add**. The Finance Database now appears in your list of connectors.
5. Start a new chat and ask for a list of companies, ETFs or funds. There is no key prompt: the tools work right away.
{: .ca-steps}

The hosted server follows the database itself, which the community updates every week, so the answers stay current without anything to update on your side.

## Connecting Claude Code

In the terminal, one command registers the server for every future session:

```bash
claude mcp add --transport http finance-database https://financedatabase.jeroenbouma.com/mcp
```

Restart Claude Code and the tools are available. This works well for building on the results: Claude Code finds the universe through the server and writes the screen, notebook or watchlist file around it.

## What You Can Ask

You never have to name a tool or a filter value: ask in plain English and Claude checks which sectors, exchanges or categories exist before it searches. Below are eight real questions, each answered through the server on October 10, 2026. **The question is what you type, the table or chart is what comes back.** Paste any of them into Claude as they are, or swap in your own country, sector or issuer.

<div class="ca-nav">
  <a href="#european-chipmakers"><i class="fas fa-microchip" aria-hidden="true"></i>Europe's large chipmakers</a>
  <a href="#isin-to-ticker"><i class="fas fa-fingerprint" aria-hidden="true"></i>From ISIN to ticker</a>
  <a href="#uranium-etfs"><i class="fas fa-atom" aria-hidden="true"></i>Uranium ETFs</a>
  <a href="#vanguard-bond-etfs"><i class="fas fa-layer-group" aria-hidden="true"></i>Vanguard's bond ETFs</a>
  <a href="#dutch-financials"><i class="fas fa-landmark" aria-hidden="true"></i>Large Dutch financials</a>
  <a href="#sp-500-indices"><i class="fas fa-chart-area" aria-hidden="true"></i>678 S&amp;P 500 indices</a>
  <a href="#swiss-franc-pairs"><i class="fas fa-money-bill-transfer" aria-hidden="true"></i>Swiss franc pairs</a>
  <a href="#did-you-mean"><i class="fas fa-spell-check" aria-hidden="true"></i>When the filter is wrong</a>
</div>

### Which large European chipmakers are there, and where do they trade? {#european-chipmakers}

<div class="ca-q"><span class="ca-q__avatar"><i class="fas fa-user" aria-hidden="true"></i></span><p>Which large European semiconductor companies are there, and on which European exchanges do they trade?<span class="ca-q__tool">Finance Database MCP · show_options, equities</span></p></div>

<div class="ca-nums"><span><b>7</b>companies</span><span><b>18</b>European listings</span><span><b>4</b>of them Dutch</span></div>

| Company | Headquarters | Market cap | European listings |
|:---|:---|:---|:---|
| ASML Holding | Netherlands | Mega Cap | ASML.AS, ASME.DE, ASMF.DE, ASML.MI, ASML.VI |
| ASM International | Netherlands | Large Cap | ASM.AS |
| BE Semiconductor Industries | Netherlands | Large Cap | BESI.AS |
| Infineon Technologies | Germany | Large Cap | IFX.DE, IFX.SW, IFX.VI |
| NXP Semiconductors | Netherlands | Large Cap | VNX.DE, NXPI.VI, 0EDE.L |
| STMicroelectronics | Switzerland | Large Cap | STMPA.PA, STMMI.MI, SGM.DE, STMI.VI |
| Technoprobe | Italy | Large Cap | TPRO.MI |

Claude first asked which exchanges these companies trade on, found 23 (including US over-the-counter markets), and then searched only the main European exchanges. That step matters: without it the same search returns ASML on Nasdaq and Infineon's US over-the-counter line IFNNY, which are the same companies in dollars. Large Cap means a market value of $10 billion or more; Mega Cap starts at $200 billion.

<div class="ca-take"><p>Four of Europe's seven large chipmakers are Dutch, and only ASML is a Mega Cap. Ask for the home exchange when you want the ticker that trades in euros.</p></div>

### Which ticker belongs to this ISIN? {#isin-to-ticker}

<div class="ca-q"><span class="ca-q__avatar"><i class="fas fa-user" aria-hidden="true"></i></span><p>Which ticker belongs to ISIN US0378331005, and where else does it trade?<span class="ca-q__tool">Finance Database MCP · search_instruments</span></p></div>

<div class="ca-nums"><span><b>19</b>listings</span><span><b>15</b>exchanges</span><span><b>6</b>currencies</span></div>

{% include ft-chart.html id="fdb-isin-listings" src="/assets/data/article-charts.json" label="Listings of Apple's ISIN by country" %}

US0378331005 is Apple Inc., AAPL on Nasdaq. The ISIN (the International Securities Identification Number, the code on a broker statement or fund report) identifies the share; the ticker depends on where you trade it. Apple trades on eight German exchanges in euros, four lines in Buenos Aires, two in Santiago, as a depositary receipt in São Paulo, and in Mexico, Milan and Vienna. The search also accepts CUSIP and FIGI codes, and searches all asset classes at once.

<div class="ca-take"><p>One security, 19 tickers. The ISIN tells you what you own; the listing tells you where, and in which currency, you trade it.</p></div>

### Which uranium ETFs can I buy? {#uranium-etfs}

<div class="ca-q"><span class="ca-q__avatar"><i class="fas fa-user" aria-hidden="true"></i></span><p>Which uranium ETFs exist, and which of them are UCITS funds listed in Europe?<span class="ca-q__tool">Finance Database MCP · etfs</span></p></div>

<div class="ca-nums"><span><b>21</b>listings</span><span><b>10</b>issuers</span><span><b>7</b>UCITS listings in Europe</span></div>

{% include ft-chart.html id="fdb-uranium" src="/assets/data/article-charts.json" label="Uranium ETF listings by market" %}

Seven of the listings are US ETFs, from URA and URNM to Direxion's leveraged URAA. The UCITS versions, the European fund format most retail investors in the EU can buy, are Global X's URNU and URND, VanEck's NUCG and NUCL, WisdomTree's NCLR and Sprott's U3O8, listed in London, Frankfurt and Milan. Global X runs 9 of the 21 listings on its own, from Toronto and Tokyo to Mexico City.

<div class="ca-take"><p>The fund you have heard of is usually the US one. The database shows the European versions next to it, which is often the version you can actually buy.</p></div>

### Which bond ETFs does Vanguard list in the US? {#vanguard-bond-etfs}

<div class="ca-q"><span class="ca-q__avatar"><i class="fas fa-user" aria-hidden="true"></i></span><p>Which bond ETFs does Vanguard list in the US, by category?<span class="ca-q__tool">Finance Database MCP · show_options, etfs</span></p></div>

<div class="ca-nums"><span><b>35</b>US-listed bond ETFs</span><span><b>15</b>corporate bond ETFs</span><span><b>10</b>target maturity ETFs</span></div>

{% include ft-chart.html id="fdb-vanguard" src="/assets/data/article-charts.json" label="Vanguard's US-listed bond ETFs by category" %}

Corporate bonds make up the largest group, and ten of those 15 are target maturity ETFs that each hold bonds maturing in one year, from 2027 to 2036. The broad core is BND for US bonds, BNDX for international bonds and BNDW for both. Without the exchange filter the count rises to 266, because many of these ETFs are also listed in Europe.

<div class="ca-take"><p>An issuer's full lineup in one question, including the newer funds you would not think to ask about.</p></div>

### Which large Dutch financials are there? {#dutch-financials}

<div class="ca-q"><span class="ca-q__avatar"><i class="fas fa-user" aria-hidden="true"></i></span><p>Which Dutch financial companies on Euronext Amsterdam are Large or Mega Cap?<span class="ca-q__tool">Finance Database MCP · show_options, equities</span></p></div>

<div class="ca-nums"><span><b>19</b>financials on Euronext Amsterdam</span><span><b>7</b>Large Cap</span><span><b>0</b>Mega Cap</span></div>

| Company | Ticker | Industry group |
|:---|:---|:---|
| ABN AMRO Bank | ABN.AS | Banks |
| ING Groep | INGA.AS | Banks |
| Aegon | AGN.AS | Insurance |
| ASR Nederland | ASRNL.AS | Insurance |
| NN Group | NN.AS | Insurance |
| CVC Capital Partners | CVC.AS | Diversified Financials |
| Exor | EXO.AS | Diversified Financials |

Of the 19 Dutch financials listed in Amsterdam, seven are Large Cap and none reaches the $200 billion Mega Cap tier. The other 12 are smaller companies, investment funds and preference shares, which is why the size filter does most of the work here.

<div class="ca-take"><p>The size filter turns 19 names into the 7 that matter for a large-cap portfolio: three insurers, two banks and two diversified financials.</p></div>

### How many S&amp;P 500 indices are there? {#sp-500-indices}

<div class="ca-q"><span class="ca-q__avatar"><i class="fas fa-user" aria-hidden="true"></i></span><p>Find the S&amp;P 500 index and its total return, growth and value versions.<span class="ca-q__tool">Finance Database MCP · indices</span></p></div>

<div class="ca-nums"><span><b>678</b>indices with "S&amp;P 500" in the name</span><span><b>^GSPC</b>the S&amp;P 500</span><span><b>^SP500TR</b>total return</span></div>

| Symbol | Name | Category |
|:---|:---|:---|
| ^GSPC | S&P 500 | Large Cap |
| ^SP500TR | S&P 500 (TR) | Equities |
| ^SP500NTR | S&P 500 (Net TR) | Equities |
| ^SP500G | S&P 500 Growth | Growth |
| ^SP500V | S&P 500 Value | Value |
| ^SP5T5 | S&P 500 Top 50 | Large Cap |
| ^SPXHAUD | S&P 500 AUD Hdg | Currencies |

The headline ^GSPC is a price index: it leaves out dividends. For a performance comparison over many years the total return version, ^SP500TR, is the fair benchmark, and the net version deducts withholding tax on those dividends. The other 670 or so are variants by sector, factor, currency hedge and size.

<div class="ca-take"><p>Benchmark against the total return index, not the price index: over a decade the gap is the dividends.</p></div>

### Which currencies quote against the Swiss franc? {#swiss-franc-pairs}

<div class="ca-q"><span class="ca-q__avatar"><i class="fas fa-user" aria-hidden="true"></i></span><p>Which currency pairs quote against the Swiss franc?<span class="ca-q__tool">Finance Database MCP · currencies</span></p></div>

<div class="ca-nums"><span><b>46</b>pairs against CHF</span><span><b>329</b>cryptocurrencies quoted in EUR</span></div>

The database holds 46 pairs with the Swiss franc as quote currency, from AUD/CHF and CNY/CHF to USD/CHF (ticker CHF=X), and the same tools cover cryptocurrencies: 329 coins are quoted in euros alone. Like everything else here, these are symbols and classifications, ready to pass on for prices.

<div class="ca-take"><p>Currencies and crypto use the same questions as stocks: name the base or quote currency and get every pair.</p></div>

### What happens when a filter doesn't exist? {#did-you-mean}

<div class="ca-q"><span class="ca-q__avatar"><i class="fas fa-user" aria-hidden="true"></i></span><p>List the large technology companies in Germany.<span class="ca-q__tool">Finance Database MCP · equities</span></p></div>

The database uses the GICS sector names, so "Technology" is not a sector. The server answers with the closest match instead of an empty list:

```
The sector 'Technology' is not available in the database.
Did you mean 'Information Technology' instead of 'Technology'?
```

Claude can read the suggestion, retry with "Information Technology" and return the list. You can phrase things the way you normally would; the exact filter values are the server's problem.

<div class="ca-take"><p>Plain language in, exact classifications out. The suggestion is what keeps a typo from becoming an empty answer.</p></div>

Every list comes from the open [Finance Database](/projects/financedatabase), so you can check where a company is classified and correct it on GitHub if it is wrong. The [MCP server page](/projects/financedatabase/mcp#example-conversations) shows the full tool calls behind four of these questions.

<div class="article-cta">
  <p class="article-cta__title">Ask your own questions</p>
  <p>These eight examples use a fraction of what the database holds. Connect it in a minute and ask for any market, sector, issuer or identifier: the lists come from the database, not from memory.</p>
  <p class="article-cta__actions"><a href="/projects/financedatabase/mcp" class="hp-btn hp-btn--primary">Connect the server <i class="fas fa-arrow-right" aria-hidden="true"></i></a><a href="/projects/financedatabase/mcp#example-conversations" class="hp-btn hp-btn--ghost">More examples</a></p>
</div>

## From a List to an Analysis

A list is where most research starts, not where it ends. Once you know the seven large Dutch financials or the 35 Vanguard bond ETFs, the next questions are about numbers: which insurer is the most solvent, which bank earns the most on its equity, how the ETFs have performed. The Finance Database holds classifications, not prices or financial statements, so it hands that part over.

That is what the Finance Toolkit MCP server does, and the two connect in the same Claude conversation. Add both connectors and you can ask *"find the large Dutch insurers, then compare their solvency ratios and return on equity"* in one go: Claude takes the tickers from the Finance Database and the numbers from the Finance Toolkit. The steps for that second server are in [How to Connect Claude to Live Financial Data for Stock Analysis](/articles/connect-claude-to-financial-data).

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

> **Try this with the Finance Database MCP:** *"Find the Large and Mega Cap insurers headquartered in Europe, with the ticker of each company's home listing."*

{% include ft-charts-script.html %}
