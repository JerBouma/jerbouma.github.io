---
title: How to Connect Claude to Live Financial Data for Stock Analysis
seo_title: "Connect Claude to Financial Data for Stock Analysis (Free MCP Server)"
seo_title_suffix: false
date: 2026-09-11
last_modified_at: 2026-09-11
permalink: /articles/connect-claude-to-financial-data
excerpt: "Claude cannot see today's prices or the latest financial statements on its own. With the free, hosted Finance Toolkit MCP server you connect Claude Desktop, claude.ai or Claude Code to live financial data and 500+ analysis methods in about a minute, no installation required."
description: "Connect Claude to live financial data in a minute with the free Finance Toolkit MCP server: stock analysis, ratios, technical indicators and macro data."
layout: single
classes: wide-sidebar article-document
author_profile: false
collection: article
tags: [Finance Toolkit, MCP Server, Claude]
share: true
image: /assets/images/projects/FinanceToolkitMCP.jpg
---
Ask Claude "what is Apple's operating margin this year?" and you get one of two answers: a polite explanation that it has no access to live data, or a confident number from its training data that may be a year or more out of date. Neither is useful when you are trying to analyse a stock. Large language models are excellent at reasoning about numbers but they are not a data source, and asking them to compute a return on invested capital from memory is a recipe for plausible-sounding mistakes.

The fix is to give Claude a tool that fetches and computes the numbers for it. The [Model Context Protocol](https://modelcontextprotocol.io){:target="_blank"} (MCP) is the open standard Anthropic built for exactly this, and the [Finance Toolkit MCP server](/projects/financetoolkit/mcp) is a free, hosted MCP server that gives Claude access to financial statements, 150+ financial ratios, valuation models, technical indicators, performance and risk metrics and macroeconomic data for 60+ countries. Every calculation runs through the open-source [Finance Toolkit](/projects/financetoolkit) Python library, so the number Claude reports is the same number you would get by running the code yourself.

This article walks through the setup for Claude Desktop, claude.ai and Claude Code, shows what you can ask once it is connected, and ends with a worked example. The whole thing takes about a minute.

**The full installation guide, including ChatGPT, Cursor, VS Code, Codex CLI and Gemini CLI, lives on the [Finance Toolkit MCP server](/projects/financetoolkit/mcp) page. The source code is on [GitHub](https://github.com/JerBouma/FinanceToolkit){:target="_blank"}.**

## What You Need

Two things, both free:

1. **A Claude account.** Custom MCP connectors are available on claude.ai and in Claude Desktop on every plan, including the free one (which is limited to a single custom connector, so this can be it). Claude Code supports MCP servers on every plan and through the API.
2. **A Financial Modeling Prep (FMP) API key.** The server pulls company data from [Financial Modeling Prep](/fmp){:target="_blank"}; the free plan (250 requests a day, 5 years of history, US-listed companies) is enough to follow this article. Paid plans unlock the full history and all exchanges. Macroeconomic data comes from the OECD and does not need a key.

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

That is the entire setup. There is no package to install, no configuration file to edit and nothing to keep up to date: the hosted server always runs the latest Finance Toolkit release.

## Connecting Claude Code

If you work in the terminal, one command registers the server for every future session:

```bash
claude mcp add --transport http finance-toolkit https://financetoolkit.jeroenbouma.com/mcp
```

Restart Claude Code and the Finance Toolkit tools are available. The first tool call triggers the same OAuth step for the FMP API key. This is a particularly powerful combination: Claude Code can pull the data through the MCP server and then write the Python, notebook or report around it, with the numbers coming from a real calculation rather than from the model's memory.

## What You Can Ask

Once connected, you never need to name a tool or an indicator. The server exposes the Finance Toolkit through 22 categorical tools (profitability, valuation, momentum, performance, risk, macroeconomics and so on) and Claude picks the right one from a plain-English question. A few prompts to start with:

**Company analysis**

- Compare the gross, operating and net margins of Apple and Microsoft over the last five years. Which one is more profitable?
- Run a DuPont analysis on Coca-Cola and PepsiCo and explain what drives the difference in return on equity.
- What is the intrinsic value of Nvidia based on a discounted cash flow, and how does it compare to the current share price?
- Calculate the Altman Z-Score and Piotroski F-Score for Ford, General Motors and Stellantis.

**Technical analysis**

- Is the semiconductor sector overbought? Look at the RSI, MACD and Bollinger Bands for NVDA, AMD, TSM and ASML.
- Has Tesla had a golden cross or a death cross this year based on the 50-day and 200-day moving averages?

**Performance and risk**

- Compute the Sharpe ratio, Sortino ratio, alpha and beta of Amazon, Alphabet and Meta against the S&P 500 since 2020.
- What is the 95% Value at Risk and the maximum drawdown of a portfolio of Berkshire Hathaway, Visa and Costco?

**Macroeconomics**

- Show me the unemployment rate for the United States, Germany and Japan since 2010.
- Compare inflation and central bank interest rates in the Eurozone and the United States over the last three years.

Every one of these maps to a documented Finance Toolkit method, so if you want to know exactly how a number was calculated you can look it up in the [Finance Toolkit documentation](/projects/financetoolkit/docs) or read the source on GitHub.

## A Worked Example: Apple versus Microsoft

Take the first prompt above. Asked *"Compare Apple with Microsoft, which company is the most profitable?"*, Claude calls the `profitability` tool for both tickers, receives the margins for fiscal years 2021 through 2025 and lays them out:

| Metric | Company | 2021 | 2022 | 2023 | 2024 | 2025 |
|:--|:--|--:|--:|--:|--:|--:|
| Gross Margin | AAPL | 41.78% | 43.31% | 44.13% | 46.21% | 46.91% |
| Gross Margin | MSFT | 68.93% | 68.40% | 68.92% | 69.76% | 68.82% |
| Operating Margin | AAPL | 29.78% | 30.29% | 29.82% | 31.51% | 31.97% |
| Operating Margin | MSFT | 41.59% | 42.06% | 41.77% | 44.64% | 45.62% |
| Net Profit Margin | AAPL | 25.88% | 25.31% | 25.31% | 23.97% | 26.92% |
| Net Profit Margin | MSFT | 36.45% | 36.69% | 34.15% | 35.96% | 36.15% |

On margins alone the answer is Microsoft, by a wide and consistent gap: roughly 22 percentage points more net income per dollar of revenue in fiscal 2025. What makes the MCP server more useful than a raw data feed is what happens next. Without being asked, Claude follows up with a second tool call for capital-efficiency metrics and finds that Apple's return on invested capital (70.38% in 2025 versus 30.64% for Microsoft) and return on assets (30.93% versus 18.00%) point the other way. Its conclusion, that Microsoft is the more profitable business per dollar of revenue while Apple extracts more value per dollar of capital, is the kind of nuance that a single headline number hides.

The [full conversation](/projects/financetoolkit/mcp#ex-apple-microsoft), along with five other examples covering European bank solvency, semiconductor momentum, Alibaba versus Amazon, unemployment rates and ESG scores, is on the MCP server page.

## Tips for Better Answers

A few habits that make a noticeable difference when using Claude with financial data:

- **Name the period.** "Over the last five years" or "since 2020" avoids Claude defaulting to whatever range it feels like. Note that company data is reported per fiscal year, which for Apple ends in September and for Microsoft in June.
- **Ask for the definition when it matters.** Ratios such as P/E or ROIC have several accepted definitions. Ask Claude "which formula was used?" and it will tell you; the Finance Toolkit documents each one.
- **Let it chain.** The best answers come from letting Claude make several tool calls in a row: margins, then returns, then valuation. If it stops early, ask it to keep going.
- **Use a capable model for interpretation.** The server returns the same data to every model, but the depth of the analysis scales with the model. Claude Sonnet and Opus write genuinely useful narratives; smaller models return clean tables with less commentary.
- **Mind the free-plan limits.** The FMP free plan allows 250 requests a day; a broad screen across many tickers can use those up quickly. Start with a handful of companies.

## Not a Claude User?

The same server works with any MCP-compatible client. The [Finance Toolkit MCP server](/projects/financetoolkit/mcp#installation) page has step-by-step instructions for ChatGPT (Developer mode), Cursor, VS Code with GitHub Copilot, Windsurf, Codex CLI and Gemini CLI, plus the local installation for clients that only support stdio transport. If you would rather skip the assistant altogether, the [Finance Toolkit](/projects/financetoolkit) Python library exposes the same 500+ methods directly.

If you run into a problem or have an idea for a new tool, open an issue on [GitHub](https://github.com/JerBouma/FinanceToolkit/issues){:target="_blank"}; the server is open source and contributions are welcome.
