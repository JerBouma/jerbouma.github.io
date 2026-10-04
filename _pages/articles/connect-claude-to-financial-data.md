---
title: How to Connect Claude to Live Financial Data for Stock Analysis
seo_title: "Connect Claude to Live Financial Data"
date: 2026-09-11
last_modified_at: 2026-10-04
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
Ask Claude "what is Apple's operating margin this year?" and you get one of two answers: a polite explanation that it has no access to live data, or a confident number from its training data that may be a year or more out of date. Neither is useful when you are trying to analyze a stock. Large language models are good at reasoning about numbers, but they are not a data source, and if you ask them to compute a return on invested capital from memory you tend to get plausible-sounding mistakes.

The fix is to give Claude a tool that fetches and computes the numbers for it. The [Model Context Protocol](https://modelcontextprotocol.io){:target="_blank"} (MCP) is the open standard Anthropic built for this purpose, and the [Finance Toolkit MCP server](/projects/financetoolkit/mcp) is a free, hosted MCP server that gives Claude access to financial statements, 80+ financial ratios, valuation models, technical indicators, performance and risk metrics and macroeconomic data for 60+ countries. Every calculation runs through the open-source [Finance Toolkit](/projects/financetoolkit) Python library, so the number Claude reports is the same number you would get by running the code yourself.

This article walks through the setup for Claude Desktop, claude.ai and Claude Code, which takes about a minute, and then answers ten real questions through the server, from DuPont analyses and discounted cash flows to drawdowns and central bank policy, each with the chart Claude's data produces.

<div class="article-cta">
  <p class="article-cta__title">Free, hosted and open source</p>
  <p>One URL gives Claude, ChatGPT, Cursor and other AI assistants access to 500+ financial methods, financial statements and macro data for 60+ countries.</p>
  <p class="article-cta__actions"><a href="/projects/financetoolkit/mcp" class="hp-btn hp-btn--primary">Explore the server <i class="fas fa-arrow-right" aria-hidden="true"></i></a><a href="/projects/financetoolkit/mcp#installation" class="hp-btn hp-btn--ghost">Install guide</a></p>
</div>

## What You Need

You need two things, both free:

1. **A Claude account.** Custom MCP connectors are available on claude.ai and in Claude Desktop on every plan, including the free one (which is limited to a single custom connector, so this can be it). Claude Code supports MCP servers on every plan and through the API.
2. **A Financial Modeling Prep (FMP) API key.** The server pulls company data from [Financial Modeling Prep](/fmp){:target="_blank"}; the free plan (250 requests a day, 5 years of history, US-listed companies) is enough to follow this article. Paid plans add the full history and all exchanges. Macroeconomic data comes from the OECD and does not need a key.

You enter the FMP key once, through a standard OAuth login page that the hosted server opens on first use. The server never stores it; it is passed along with each request and forgotten afterwards. If you would rather not use the hosted version at all, the [local installation](/projects/financetoolkit/mcp#local-clients) runs the exact same server on your own machine with a single `uvx` command.

## Connecting Claude Desktop or claude.ai

The steps are identical for the desktop app and the web app:

1. Click **Customize** in the left sidebar and open the **Connectors** tab.
2. Click the **+** button and select **Add custom connector**.
3. Enter a name, e.g. *Finance Toolkit*, and paste the server URL:

    ```
    https://financetoolkit.jeroenbouma.com/mcp
    ```

4. Click **Add**. The Finance Toolkit now appears in your list of connectors.
5. Start a new chat and ask a financial question. On the first tool call Claude opens a browser window asking for your FMP API key; enter it once and you are done.

There is no package to install, no configuration file to edit and nothing to keep up to date, because the hosted server always runs the latest Finance Toolkit release.

## Connecting Claude Code

If you work in the terminal, one command registers the server for every future session:

```bash
claude mcp add --transport http finance-toolkit https://financetoolkit.jeroenbouma.com/mcp
```

Restart Claude Code and the Finance Toolkit tools are available. The first tool call triggers the same OAuth step for the FMP API key. This combination works well: Claude Code can pull the data through the MCP server and then write the Python, notebook or report around it, with the numbers coming from a real calculation rather than from the model's memory.

## What You Can Ask

Once connected, you never need to name a tool or an indicator. The server exposes the Finance Toolkit through 22 categorical tools (profitability, valuation, momentum, performance, risk, macroeconomics and so on) and Claude picks the right one from a plain-English question. Below are ten questions across company analysis, technical analysis, risk and macroeconomics. Every answer and every chart comes straight from the Finance Toolkit MCP server, with data up to October 2, 2026, so you can see what the output looks like before you connect anything.

**For each example, the question is what you type; the text and chart below it are what comes back. Once the [Finance Toolkit MCP server](/projects/financetoolkit/mcp) is connected, you can paste any of these questions into Claude as they are, or swap in your own tickers.**

## Company Analysis

### Which is more profitable, Apple or Microsoft?

> *"Compare the gross, operating and net margins of Apple and Microsoft over the last five years. Which one is more profitable?"*

Claude calls the `profitability` tool for both tickers and receives the margins for fiscal years 2021 through 2025:

{% include ft-chart.html id="claude-margins" src="/assets/data/article-charts.json" label="Margins of Apple and Microsoft" %}

On margins alone the answer is Microsoft, by a wide and consistent gap: about 22 percentage points more gross margin and roughly 9 points more net income per dollar of revenue in fiscal 2025. The next step is where the MCP server does more than a raw data feed would. Without being asked, Claude follows up with a second tool call for capital-efficiency metrics and finds that Apple's return on invested capital (70.38% in 2025 versus 30.64% for Microsoft) and return on assets (30.93% versus 18.00%) point the other way. **Microsoft earns more per dollar of revenue; Apple earns more per dollar of capital.** That is the kind of nuance a single headline number hides.

### What drives the difference between Coca-Cola and PepsiCo?

> *"Run a DuPont analysis on Coca-Cola and PepsiCo and explain what drives the difference in return on equity."*

The `models` tool splits return on equity into net profit margin, asset turnover and the equity multiplier:

{% include ft-chart.html id="claude-dupont" src="/assets/data/article-charts.json" label="DuPont analysis of Coca-Cola and PepsiCo" %}

The two companies reach a similar return on equity in completely different ways. Coca-Cola keeps 27 cents of every dollar of revenue as profit (2025), because it mostly sells concentrate and leaves the capital-heavy bottling to partners. PepsiCo keeps about 9 cents, but owns snack factories and distribution, turns its assets over roughly twice as fast (0.91 versus 0.47) and runs with more leverage (an equity multiplier of 5.3 versus 3.4). For most of the period that combination gave PepsiCo the higher return on equity, around 50% against roughly 40%. In 2025 the gap closed, at 43.2% for Coca-Cola and 42.6% for PepsiCo, as PepsiCo's margin dipped to 8.8%. Switch between the tabs to see which component moved.

### What growth is priced into Nvidia?

> *"What is the intrinsic value of Nvidia based on a discounted cash flow, and how does it compare to the current share price?"*

A discounted cash flow model is only as good as its growth assumption, so the useful answer is a range. Claude runs the `models` tool's intrinsic valuation with a 10% cost of capital, 3% terminal growth and five years of explicit forecasts, at four growth rates:

{% include ft-chart.html id="claude-dcf" src="/assets/data/article-charts.json" label="Nvidia DCF value per share at different growth rates" %}

At 15% annual free cash flow growth Nvidia is worth about $95 per share; at 25%, $139; at 35%, $200. The share price on October 2, 2026 was $233.95, which only fits once growth is close to 40% a year for five years. Turned around, that is the more useful conclusion: **the market is pricing in roughly 40% annual cash flow growth until 2030**, and the question becomes whether you believe that, rather than whether the stock is "cheap".

### Which carmaker is in the weakest financial position?

> *"Calculate the Altman Z-Score and Piotroski F-Score for Ford, General Motors and Stellantis."*

Both scores come from the `models` tool, the Altman Z-Score as a measure of distress risk and the Piotroski F-Score (0 to 9) as a checklist of improving or weakening fundamentals:

{% include ft-chart.html id="claude-distress" src="/assets/data/article-charts.json" label="Altman Z-Score and Piotroski F-Score of Ford, GM and Stellantis" %}

All three ended 2025 below 1.8, the traditional distress threshold of the Altman Z-Score: Ford at 0.79, General Motors at 1.25 and Stellantis at 0.86. The biggest change is Stellantis, which fell from 2.27 in 2023 as its operating result turned negative in 2025, and whose Piotroski score dropped to 2 out of 9 in both 2024 and 2025. A good analyst, and a good AI answer, adds the caveat: Ford and General Motors run large captive finance arms whose loan books inflate their liabilities, which pushes the Z-Score down structurally. The trend within each company says more than the comparison between them.

## Technical Analysis

### Is the semiconductor sector overbought?

> *"Is the semiconductor sector overbought? Look at the RSI for NVDA, AMD, TSM and ASML."*

The `momentum` tool returns the Relative Strength Index, here on weekly closes for 2026:

{% include ft-chart.html id="claude-rsi" src="/assets/data/article-charts.json" label="Weekly RSI of NVDA, AMD, TSM and ASML in 2026" %}

At the start of October 2026, AMD (71.4) and TSMC (71.6) are back above 70, the conventional overbought line, while Nvidia (61.3) and ASML (62.6) are not. AMD is the outlier of the year: it spent most of April to July above 70 and peaked at 84.6 in May. Nvidia never reached overbought territory in 2026 and touched 38.3 in March. An RSI above 70 says the recent move was strong, not that it has to reverse, so Claude usually pairs it with a trend indicator in the next step.

### Did Tesla have a golden cross or a death cross?

> *"Has Tesla had a golden cross or a death cross this year based on the 50-day and 200-day moving averages?"*

The `overlap` tool returns the moving averages. On daily data, Tesla's 50-day average fell below its 200-day average on April 9, 2026: a death cross. The chart shows the same picture on weekly data:

{% include ft-chart.html id="claude-tesla" src="/assets/data/article-charts.json" label="Tesla with its 10-week and 40-week moving averages" %}

There has been no golden cross since. On October 2 the 50-day average stood at $347.58 against $393.18 for the 200-day, a gap that has kept widening since July, when the share price fell to around $311. The price has since recovered to about $371, above the short average but still below the long one.

## Performance and Risk

### How did Amazon, Alphabet and Meta do on a risk-adjusted basis?

> *"Compute the Sharpe ratio, Sortino ratio, alpha and beta of Amazon, Alphabet and Meta against the S&P 500 since 2020."*

The `performance` tool calculates each metric per calendar year against the S&P 500:

{% include ft-chart.html id="claude-performance" src="/assets/data/article-charts.json" label="Sharpe ratio, Sortino ratio, beta and alpha of Amazon, Alphabet and Meta" %}

2022 was a bad year for all three on every risk-adjusted measure. 2023 belonged to Meta, with the highest Sharpe and Sortino ratios of the group and an alpha of 168% after its cost-cutting "year of efficiency". 2025 belonged to Alphabet: an alpha of 48% while Amazon (−12.5%) and Meta (−4.6%) lagged the market, and the lowest beta of the three at 1.03. The Sharpe and Sortino ratios are calculated from daily returns within each year, so compare them with each other rather than with annualised figures elsewhere.

### How much downside risk do Berkshire Hathaway, Visa and Costco carry?

> *"What is the 95% Value at Risk and the maximum drawdown of Berkshire Hathaway, Visa and Costco since 2020?"*

The `risk` tool answers with the daily Value at Risk, the Conditional Value at Risk (the average loss on the worst 5% of days) and the largest peak-to-trough fall since 2020:

{% include ft-chart.html id="claude-risk" src="/assets/data/article-charts.json" label="Value at Risk, CVaR and maximum drawdown of Berkshire Hathaway, Visa and Costco" %}

Berkshire Hathaway has the calmest day-to-day profile, with a daily VaR of −1.83%, close to the S&P 500's −1.76%. Visa has the fattest daily tail (a CVaR of −3.93%). The maximum drawdowns tell a different story: Costco, not Berkshire, had the smallest worst-case fall since 2020 (−20.3%), while Berkshire's −24.3% was slightly deeper than the market's −23.9%. **Daily risk and drawdown risk rank the same stocks differently**, which is why it is worth asking for both.

## Macroeconomics

Macroeconomic data comes from the OECD and the Global Macro Database and does not need an FMP key.

### How have unemployment rates developed since 2010?

> *"Show me the unemployment rate for the United States, Germany and Japan since 2010."*

{% include ft-chart.html id="claude-unemployment" src="/assets/data/article-charts.json" label="Unemployment rate of the United States, Germany and Japan since 2010" %}

The United States went from 9.6% in 2010 to 3.7% in 2019, jumped to 8.1% in 2020 and was back at 3.6% two years later. Germany barely moved during the pandemic (3.6% in 2020), because its short-time work scheme kept people employed while their hours were cut. Japan's rate has been flat at around 2.5% for years. The US labour market has loosened somewhat since, to 4.4% in 2025.

### How do inflation and interest rates compare in the US and the Eurozone?

> *"Compare inflation and central bank interest rates in the Eurozone and the United States over the last few years."*

{% include ft-chart.html id="claude-rates" src="/assets/data/article-charts.json" label="Inflation, policy rates and real policy rates in the US and the Eurozone" %}

Inflation peaked in 2022 on both sides of the Atlantic, at 8.0% in the US and 6.9% in Germany, with the Netherlands reaching 10.0%. The Federal Reserve raised rates earlier and further, to an average of 5.38% in 2023. The real policy rate (the policy rate minus inflation, in the third tab) shows the difference best: US monetary policy was restrictive in real terms from 2023, the Eurozone's only from 2024, after a real rate of −2.3% in 2023. Policy rates are annual averages.

Every one of these answers maps to a documented Finance Toolkit method, so if you want to know exactly how a number was calculated you can look it up in the [Finance Toolkit documentation](/projects/financetoolkit/docs) or read the source on GitHub. The [MCP server page](/projects/financetoolkit/mcp#ex-apple-microsoft) has the full conversation for the first example and five more, covering European bank solvency, semiconductor momentum, Alibaba versus Amazon, unemployment rates and ESG scores.

<div class="article-cta">
  <p class="article-cta__title">Ask your own questions</p>
  <p>These ten examples use a fraction of what the server can do. Connect it in a minute and ask about any company, index, sector or economy: the answers are calculated, not recalled from memory.</p>
  <p class="article-cta__actions"><a href="/projects/financetoolkit/mcp" class="hp-btn hp-btn--primary">Connect the server <i class="fas fa-arrow-right" aria-hidden="true"></i></a><a href="/projects/financetoolkit/mcp#example-conversations" class="hp-btn hp-btn--ghost">More examples</a></p>
</div>

## Tips for Better Answers

A few habits that make a noticeable difference when using Claude with financial data:

- **Name the period.** "Over the last five years" or "since 2020" avoids Claude defaulting to whatever range it feels like. Note that company data is reported per fiscal year, which for Apple ends in September and for Microsoft in June.
- **Ask for the definition when it matters.** Ratios such as P/E or ROIC have several accepted definitions. Ask Claude "which formula was used?" and it will tell you; the Finance Toolkit documents each one.
- **Let it chain.** The best answers come from letting Claude make several tool calls in a row: margins, then returns, then valuation. If it stops early, ask it to keep going.
- **Use a capable model for interpretation.** The server returns the same data to every model, but the depth of the analysis scales with the model. Claude Sonnet and Opus write useful narratives; smaller models return clean tables with less commentary.
- **Mind the free-plan limits.** The FMP free plan allows 250 requests a day; a broad screen across many tickers can use those up quickly. Start with a handful of companies.

## Not a Claude User?

The same server works with any MCP-compatible client. The [Finance Toolkit MCP server](/projects/financetoolkit/mcp#installation) page has step-by-step instructions for ChatGPT (Developer mode), Cursor, VS Code with GitHub Copilot, Windsurf, Codex CLI and Gemini CLI, plus the local installation for clients that only support stdio transport. If you would rather skip the assistant altogether, the [Finance Toolkit](/projects/financetoolkit) Python library exposes the same 500+ methods directly.

If you run into a problem or have an idea for a new tool, open an issue on [GitHub](https://github.com/JerBouma/FinanceToolkit/issues){:target="_blank"}; the server is open source and contributions are welcome.

<script src="/assets/js/ft-charts.js" defer></script>
