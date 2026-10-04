---
title: How to Connect Claude to Live Financial Data for Stock Analysis
seo_title: "Connect Claude to Live Financial Data"
date: 2026-09-11
last_modified_at: 2026-10-05
permalink: /articles/connect-claude-to-financial-data
excerpt: "Claude cannot see today's prices or the latest financial statements on its own. With the free, hosted Finance Toolkit MCP server you connect Claude Desktop, claude.ai or Claude Code to live financial data and 500+ analysis methods in about a minute, no installation required."
description: "Connect Claude to live financial data in a minute with the free Finance Toolkit MCP server: stock analysis, ratios, technical indicators and macro data."
layout: single
classes: wide-sidebar article-document
author_profile: false
collection: article
tags: [MCP Server]
share: true
image: /assets/images/projects/FinanceToolkitMCP.jpg
---
Ask Claude *"what is Apple's operating margin this year?"* and you get one of two answers: a polite explanation that it has no access to live data, or a confident number from its training data that may be a year or more out of date. Language models are good at reasoning about numbers, but they are not a data source, and asked to compute a return on invested capital from memory they tend to produce plausible-sounding mistakes.

The fix is to give Claude a tool that fetches and computes the numbers for it. The [Model Context Protocol](https://modelcontextprotocol.io){:target="_blank"} (MCP) is the open standard Anthropic built for exactly this, and the [Finance Toolkit MCP server](/projects/financetoolkit/mcp) is a free, hosted server that connects Claude to financial statements, 80+ ratios, valuation models, risk and performance metrics, technical indicators and macro data for 60+ countries. Every calculation runs through the open-source [Finance Toolkit](/projects/financetoolkit), so the number Claude reports is the number you would get by running the code yourself.

<div class="ca-strip">
  <div><strong>1 minute</strong><span>to connect Claude Desktop, claude.ai or Claude Code</span></div>
  <div><strong>500+</strong><span>financial methods behind 22 tools</span></div>
  <div><strong>10</strong><span>real questions answered below, with charts</span></div>
  <div><strong>Free</strong><span>hosted server, open-source code</span></div>
</div>

<div class="article-cta">
  <p class="article-cta__title">Free, hosted and open source</p>
  <p>One URL gives Claude, ChatGPT, Cursor and other AI assistants access to 500+ financial methods, financial statements and macro data for 60+ countries.</p>
  <p class="article-cta__actions"><a href="/projects/financetoolkit/mcp" class="hp-btn hp-btn--primary">Explore the server <i class="fas fa-arrow-right" aria-hidden="true"></i></a><a href="/projects/financetoolkit/mcp#installation" class="hp-btn hp-btn--ghost">Install guide</a></p>
</div>

## What You Need

<div class="ca-cards">
  <div><i class="ca-icon fas fa-comments" aria-hidden="true"></i><p class="ca-card-title">A Claude account</p><p>Custom connectors work in claude.ai and Claude Desktop on every plan; the free plan allows one, so this can be it. Claude Code supports MCP servers on every plan.</p></div>
  <div><i class="ca-icon fas fa-key" aria-hidden="true"></i><p class="ca-card-title">A Financial Modeling Prep key</p><p>Company data comes from <a href="/fmp" target="_blank">Financial Modeling Prep</a>. The free plan (250 requests a day, five years of US data) is enough for this article. Macro data needs no key.</p></div>
</div>

You enter the key once, on a standard OAuth page the server opens on first use. It is passed along with each request and never stored. If you would rather not use the hosted server, the [local installation](/projects/financetoolkit/mcp#local-clients) runs the same server on your own machine with one `uvx` command.

## Connecting Claude Desktop or claude.ai

The steps are identical for the desktop app and the web app:

1. Click **Customize** in the left sidebar and open the **Connectors** tab.
2. Click **+** and select **Add custom connector**.
3. Enter a name, e.g. *Finance Toolkit*, and paste the server URL:

    ```
    https://financetoolkit.jeroenbouma.com/mcp
    ```

4. Click **Add**. The Finance Toolkit now appears in your list of connectors.
5. Start a new chat and ask a financial question. On the first tool call a browser window asks for your FMP key; enter it once and you are done.
{: .ca-steps}

There is nothing to install and nothing to keep up to date: the hosted server always runs the latest Finance Toolkit release.

## Connecting Claude Code

In the terminal, one command registers the server for every future session:

```bash
claude mcp add --transport http finance-toolkit https://financetoolkit.jeroenbouma.com/mcp
```

Restart Claude Code and the tools are available; the first tool call triggers the same one-time key prompt. This combination works well for building on the numbers: Claude Code pulls the data through the server and writes the Python, notebook or report around it.

## What You Can Ask

You never have to name a tool or an indicator: ask in plain English and Claude picks the right one. Below are ten real questions, each answered through the server with data up to October 2, 2026. **The question is what you type, the chart is what comes back.** Paste any of them into Claude as they are, or swap in your own tickers.

<div class="ca-nav">
  <a href="#apple-or-microsoft"><i class="fas fa-building" aria-hidden="true"></i>Apple or Microsoft</a>
  <a href="#coca-cola-versus-pepsico"><i class="fas fa-bottle-water" aria-hidden="true"></i>Coca-Cola vs PepsiCo</a>
  <a href="#growth-priced-into-nvidia"><i class="fas fa-microchip" aria-hidden="true"></i>Nvidia's priced-in growth</a>
  <a href="#carmakers-financial-health"><i class="fas fa-car" aria-hidden="true"></i>Carmakers' financial health</a>
  <a href="#semiconductors-overbought"><i class="fas fa-gauge-high" aria-hidden="true"></i>Are semis overbought?</a>
  <a href="#tesla-moving-averages"><i class="fas fa-chart-line" aria-hidden="true"></i>Tesla's death cross</a>
  <a href="#risk-adjusted-performance"><i class="fas fa-trophy" aria-hidden="true"></i>Big Tech risk-adjusted</a>
  <a href="#downside-risk"><i class="fas fa-shield-halved" aria-hidden="true"></i>Downside risk</a>
  <a href="#unemployment-since-2010"><i class="fas fa-briefcase" aria-hidden="true"></i>Unemployment since 2010</a>
  <a href="#inflation-and-rates"><i class="fas fa-landmark" aria-hidden="true"></i>Inflation and rates</a>
</div>

### Which is more profitable, Apple or Microsoft? {#apple-or-microsoft}

<div class="ca-q"><span class="ca-q__avatar"><i class="fas fa-user" aria-hidden="true"></i></span><p>Compare the gross, operating and net margins of Apple and Microsoft over the last five years. Which one is more profitable?<span class="ca-q__tool">Finance Toolkit MCP · profitability</span></p></div>

{% include ft-chart.html id="claude-margins" src="/assets/data/article-charts.json" label="Margins of Apple and Microsoft" %}

On margins the answer is Microsoft, by a wide and steady gap. Without being asked, Claude then checks capital efficiency, and that points the other way: Apple's return on invested capital was 70.38% in 2025 against 30.64% for Microsoft.

<div class="ca-take"><p>Microsoft earns more per dollar of revenue; Apple earns more per dollar of capital. A single headline number would hide that.</p></div>

### What drives the difference between Coca-Cola and PepsiCo? {#coca-cola-versus-pepsico}

<div class="ca-q"><span class="ca-q__avatar"><i class="fas fa-user" aria-hidden="true"></i></span><p>Run a DuPont analysis on Coca-Cola and PepsiCo and explain what drives the difference in return on equity.<span class="ca-q__tool">Finance Toolkit MCP · models · DuPont analysis</span></p></div>

<div class="ca-nums"><span><b>43.2% vs 42.6%</b>ROE 2025</span><span><b>27% vs 9%</b>net margin</span><span><b>0.47 vs 0.91</b>asset turnover</span></div>

{% include ft-chart.html id="claude-dupont" src="/assets/data/article-charts.json" label="DuPont analysis of Coca-Cola and PepsiCo" %}

Coca-Cola mostly sells concentrate and leaves the capital-heavy bottling to partners, so it keeps 27 cents of every dollar as profit. PepsiCo owns its snack factories and distribution: thinner margins, but it turns its assets over twice as fast and uses more leverage (an equity multiplier of 5.3 versus 3.4). Switch between the tabs to see each component.

<div class="ca-take"><p>A similar return on equity, built in opposite ways: Coca-Cola through margin, PepsiCo through volume and leverage.</p></div>

### What growth is priced into Nvidia? {#growth-priced-into-nvidia}

<div class="ca-q"><span class="ca-q__avatar"><i class="fas fa-user" aria-hidden="true"></i></span><p>What is the intrinsic value of Nvidia based on a discounted cash flow, and how does it compare to the current share price?<span class="ca-q__tool">Finance Toolkit MCP · models · intrinsic valuation</span></p></div>

A DCF is only as good as its growth assumption, so Claude runs it at four growth rates (10% cost of capital, 3% terminal growth, five years):

{% include ft-chart.html id="claude-dcf" src="/assets/data/article-charts.json" label="Nvidia DCF value per share at different growth rates" %}

<div class="ca-take"><p>The share price of $233.95 only fits with roughly 40% annual cash flow growth for five years. The question is whether you believe that, not whether the stock is cheap.</p></div>

### Which carmaker is in the weakest financial position? {#carmakers-financial-health}

<div class="ca-q"><span class="ca-q__avatar"><i class="fas fa-user" aria-hidden="true"></i></span><p>Calculate the Altman Z-Score and Piotroski F-Score for Ford, General Motors and Stellantis.<span class="ca-q__tool">Finance Toolkit MCP · models · Altman Z-Score, Piotroski F-Score</span></p></div>

<div class="ca-nums"><span><b>0.79</b>Ford Z-Score</span><span><b>1.25</b>GM Z-Score</span><span><b>0.86</b>Stellantis Z-Score</span><span><b>2 / 9</b>Stellantis Piotroski</span></div>

{% include ft-chart.html id="claude-distress" src="/assets/data/article-charts.json" label="Altman Z-Score and Piotroski F-Score of Ford, GM and Stellantis" %}

All three ended 2025 below 1.8, the classic distress threshold. Stellantis moved the most, from 2.27 in 2023 as its operating result turned negative. A good answer adds the caveat: Ford and GM run large car-finance arms whose loan books inflate liabilities and push the score down structurally.

<div class="ca-take"><p>Read the trend within each company, not the gap between them. Stellantis is the one that deteriorated.</p></div>

### Is the semiconductor sector overbought? {#semiconductors-overbought}

<div class="ca-q"><span class="ca-q__avatar"><i class="fas fa-user" aria-hidden="true"></i></span><p>Is the semiconductor sector overbought? Look at the RSI for NVDA, AMD, TSM and ASML.<span class="ca-q__tool">Finance Toolkit MCP · momentum · RSI</span></p></div>

<div class="ca-nums"><span><b>71.4</b>AMD</span><span><b>71.6</b>TSMC</span><span><b>61.3</b>Nvidia</span><span><b>62.6</b>ASML</span></div>

{% include ft-chart.html id="claude-rsi" src="/assets/data/article-charts.json" label="Weekly RSI of NVDA, AMD, TSM and ASML in 2026" %}

AMD was the outlier of the year, above 70 for most of April to July with a peak of 84.6 in May. Nvidia never reached overbought territory in 2026 and touched 38.3 in March.

<div class="ca-take"><p>AMD and TSMC are back above 70; Nvidia and ASML are not. An RSI above 70 says the move was strong, not that it must reverse.</p></div>

### Did Tesla have a golden cross or a death cross? {#tesla-moving-averages}

<div class="ca-q"><span class="ca-q__avatar"><i class="fas fa-user" aria-hidden="true"></i></span><p>Has Tesla had a golden cross or a death cross this year based on the 50-day and 200-day moving averages?<span class="ca-q__tool">Finance Toolkit MCP · overlap · moving averages</span></p></div>

<div class="ca-nums"><span><b>April 9</b>death cross</span><span><b>$347.58</b>50-day average</span><span><b>$393.18</b>200-day average</span></div>

{% include ft-chart.html id="claude-tesla" src="/assets/data/article-charts.json" label="Tesla with its 10-week and 40-week moving averages" %}

The 50-day average fell below the 200-day on April 9, 2026, and there has been no golden cross since. The gap kept widening after the July drop to around $311; the price has recovered to about $371, above the short average but still below the long one.

<div class="ca-take"><p>A death cross in April, and the trend has not turned since.</p></div>

### How did Amazon, Alphabet and Meta do on a risk-adjusted basis? {#risk-adjusted-performance}

<div class="ca-q"><span class="ca-q__avatar"><i class="fas fa-user" aria-hidden="true"></i></span><p>Compute the Sharpe ratio, Sortino ratio, alpha and beta of Amazon, Alphabet and Meta against the S&P 500 since 2020.<span class="ca-q__tool">Finance Toolkit MCP · performance</span></p></div>

<div class="ca-nums"><span><b>+168%</b>Meta alpha 2023</span><span><b>+48%</b>Alphabet alpha 2025</span><span><b>1.03</b>Alphabet beta 2025</span></div>

{% include ft-chart.html id="claude-performance" src="/assets/data/article-charts.json" label="Sharpe ratio, Sortino ratio, beta and alpha of Amazon, Alphabet and Meta" %}

2022 was bad for all three on every measure. 2023 belonged to Meta after its "year of efficiency", 2025 to Alphabet, with the market's best alpha of the three and the lowest beta. The Sharpe and Sortino ratios are calculated within each year, so compare them with each other rather than with annualised figures elsewhere.

<div class="ca-take"><p>No single winner: leadership rotated from Meta in 2023 to Alphabet in 2025.</p></div>

### How much downside risk do Berkshire Hathaway, Visa and Costco carry? {#downside-risk}

<div class="ca-q"><span class="ca-q__avatar"><i class="fas fa-user" aria-hidden="true"></i></span><p>What is the 95% Value at Risk and the maximum drawdown of Berkshire Hathaway, Visa and Costco since 2020?<span class="ca-q__tool">Finance Toolkit MCP · risk · VaR, CVaR, maximum drawdown</span></p></div>

{% include ft-chart.html id="claude-risk" src="/assets/data/article-charts.json" label="Value at Risk, CVaR and maximum drawdown of Berkshire Hathaway, Visa and Costco" %}

Berkshire has the calmest days, with a daily VaR of −1.83%, close to the S&P 500. Visa has the fattest daily tail (CVaR −3.93%). But Costco had the smallest worst-case fall since 2020 (−20.3%), while Berkshire's −24.3% was slightly deeper than the market's.

<div class="ca-take"><p>Daily risk and drawdown risk rank the same stocks differently. Ask for both.</p></div>

### How have unemployment rates developed since 2010? {#unemployment-since-2010}

<div class="ca-q"><span class="ca-q__avatar"><i class="fas fa-user" aria-hidden="true"></i></span><p>Show me the unemployment rate for the United States, Germany and Japan since 2010.<span class="ca-q__tool">Finance Toolkit MCP · jobs · unemployment rate</span></p></div>

{% include ft-chart.html id="claude-unemployment" src="/assets/data/article-charts.json" label="Unemployment rate of the United States, Germany and Japan since 2010" %}

The US went from 9.6% in 2010 to 3.7% in 2019, jumped to 8.1% in 2020 and was back at 3.6% two years later; it has loosened to 4.4% since. Japan has been flat at about 2.5% for years.

<div class="ca-take"><p>Germany barely moved in 2020 (3.6%): its short-time work scheme kept people employed while hours were cut.</p></div>

### How do inflation and interest rates compare in the US and the Eurozone? {#inflation-and-rates}

<div class="ca-q"><span class="ca-q__avatar"><i class="fas fa-user" aria-hidden="true"></i></span><p>Compare inflation and central bank interest rates in the Eurozone and the United States over the last few years.<span class="ca-q__tool">Finance Toolkit MCP · macroeconomics, rates</span></p></div>

<div class="ca-nums"><span><b>8.0%</b>US inflation 2022</span><span><b>6.9%</b>Germany 2022</span><span><b>5.38%</b>Fed rate 2023 avg</span></div>

{% include ft-chart.html id="claude-rates" src="/assets/data/article-charts.json" label="Inflation, policy rates and real policy rates in the US and the Eurozone" %}

The Federal Reserve raised rates earlier and further. The real policy rate, the policy rate minus inflation in the third tab, shows the difference best. Policy rates are annual averages.

<div class="ca-take"><p>US policy was restrictive in real terms from 2023; the Eurozone only from 2024, after a real rate of −2.3% in 2023.</p></div>

Every answer maps to a documented Finance Toolkit method, so you can look up exactly how a number was calculated in the [documentation](/projects/financetoolkit/docs). The [MCP server page](/projects/financetoolkit/mcp#example-conversations) has the full conversations for six more questions.

<div class="article-cta">
  <p class="article-cta__title">Ask your own questions</p>
  <p>These ten examples use a fraction of what the server can do. Connect it in a minute and ask about any company, index, sector or economy: the answers are calculated, not recalled from memory.</p>
  <p class="article-cta__actions"><a href="/projects/financetoolkit/mcp" class="hp-btn hp-btn--primary">Connect the server <i class="fas fa-arrow-right" aria-hidden="true"></i></a><a href="/projects/financetoolkit/mcp#example-conversations" class="hp-btn hp-btn--ghost">More examples</a></p>
</div>

## Tips for Better Answers

<div class="ca-cards ca-cards--3">
  <div><i class="ca-icon fas fa-calendar-days" aria-hidden="true"></i><p class="ca-card-title">Name the period</p><p>"Since 2020" avoids Claude picking a range for you. Company data follows fiscal years: September for Apple, June for Microsoft.</p></div>
  <div><i class="ca-icon fas fa-book" aria-hidden="true"></i><p class="ca-card-title">Ask for the definition</p><p>P/E and ROIC have several definitions. Ask "which formula was used?"; every one is documented.</p></div>
  <div><i class="ca-icon fas fa-link" aria-hidden="true"></i><p class="ca-card-title">Let it chain</p><p>The best answers come from several tool calls in a row: margins, then returns, then valuation. If it stops early, ask it to continue.</p></div>
  <div><i class="ca-icon fas fa-brain" aria-hidden="true"></i><p class="ca-card-title">Pick a capable model</p><p>Every model gets the same data; the depth of the interpretation scales with the model.</p></div>
  <div><i class="ca-icon fas fa-gauge" aria-hidden="true"></i><p class="ca-card-title">Mind the free plan</p><p>FMP's free plan allows 250 requests a day. A broad screen can use that quickly, so start with a few companies.</p></div>
  <div><i class="ca-icon fas fa-code" aria-hidden="true"></i><p class="ca-card-title">Build on it</p><p>In Claude Code, ask for the notebook or script around the answer; the numbers stay the server's.</p></div>
</div>

## Not a Claude User?

The same server works with any MCP-compatible client, each with step-by-step instructions on the [Finance Toolkit MCP server](/projects/financetoolkit/mcp#installation) page:

<div class="ca-clients">
  <span><i class="fas fa-comment-dots" aria-hidden="true"></i>ChatGPT</span>
  <span><i class="fab fa-microsoft" aria-hidden="true"></i>VS Code and GitHub Copilot</span>
  <span><i class="fas fa-i-cursor" aria-hidden="true"></i>Cursor</span>
  <span><i class="fas fa-wind" aria-hidden="true"></i>Windsurf</span>
  <span><i class="fas fa-code" aria-hidden="true"></i>Codex CLI</span>
  <span><i class="fab fa-google" aria-hidden="true"></i>Gemini CLI</span>
</div>

Clients that only support the stdio transport can use the local installation. If you would rather skip the assistant altogether, the [Finance Toolkit](/projects/financetoolkit) Python library exposes the same 500+ methods directly. Problems or ideas for a new tool are welcome as an issue on [GitHub](https://github.com/JerBouma/FinanceToolkit/issues){:target="_blank"}.

<script src="/assets/js/ft-charts.js" defer></script>
