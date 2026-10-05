---
permalink: /projects/financetoolkit/mcp
title: Finance Toolkit MCP Server
excerpt: "Connect Claude, ChatGPT, Cursor, VS Code or any other MCP client to the Finance Toolkit, hosted or on your own machine, and analyze stocks, financial statements, technical indicators and macro data in plain English."
description: "Open-source MCP server for stock analysis: 500+ financial methods, valuation models, technical indicators and macro data in Claude, ChatGPT or Cursor."
classes: wide-sidebar
author_profile: false
layout: single
last_modified_at: 2026-10-05
redirect_from:
  - /mcp
  - /projects/financetoolkit/mcp-server
sidebar:
  nav: "financetoolkit-mcp"
image: /assets/images/projects/FinanceToolkitMCP.jpg
---

<div class="page-header-action notebook-viewer-actions"><a href="https://github.com/JerBouma/FinanceToolkit#mcp-server" target="_blank" rel="noopener"><i class="fab fa-github"></i> View on GitHub</a></div>

Ask an AI assistant for Apple's return on invested capital and you will usually get a number. Whether it is right depends on what the model remembers from its training data, which of the several definitions it picked and whether the arithmetic held up along the way. Ask twice and you may get two different answers.

The Finance Toolkit MCP server takes the calculation out of the model's hands. It is an open-source [Model Context Protocol](https://modelcontextprotocol.io){:target="_blank"} (MCP) server that connects Claude, ChatGPT, GitHub Copilot, Cursor, Gemini and other assistants to the [Finance Toolkit](/projects/financetoolkit): current financial statements and market data, and 500+ documented methods that turn them into ratios, valuations, risk metrics, technical indicators and macroeconomic series. The assistant decides what to calculate and explains the result; the numbers themselves come from code you can read.

<div class="mcp-facts">
  <div class="mcp-fact"><strong>500+</strong><span>ratios, models, risk metrics, indicators and macro series in 22 tools</span></div>
  <div class="mcp-fact"><strong>Calculated</strong><span>not recalled: the same question returns the same number in any model</span></div>
  <div class="mcp-fact"><strong>Free</strong><span>hosted at one URL, or run locally; MIT-licensed source code</span></div>
  <div class="mcp-fact"><strong>Any client</strong><span>Claude, ChatGPT, Copilot, Cursor, Windsurf, Gemini, Codex</span></div>
</div>

<div class="mcp-video-wrapper">
  <video class="mcp-demo-video" autoplay muted playsinline loop preload="metadata"
         width="1280" height="720" poster="/assets/images/projects/FinanceToolkitMCP.jpg">
    <source src="/assets/video/mcp-demo.mp4" type="video/mp4">
  </video>
</div>

## Why the Finance Toolkit MCP

There is a growing number of MCP servers for financial data, from the official Financial Modeling Prep and Yahoo Finance servers to dozens of community wrappers. Most of them expose raw API endpoints, such as a quote, an income statement or a list of prices, and leave the analysis to the language model. That is exactly where language models are least reliable.

<div class="mcp-compare">
<table>
<thead><tr><th></th><th>Raw data servers</th><th>Finance Toolkit MCP</th></tr></thead>
<tbody>
<tr><th scope="row">What the assistant receives</th><td data-label="Raw data servers">Prices and financial statements</td><td data-label="Finance Toolkit MCP">Calculated ratios, models, risk metrics and indicators, plus the underlying data</td></tr>
<tr><th scope="row">Who does the arithmetic</th><td data-label="Raw data servers">The language model</td><td data-label="Finance Toolkit MCP">The open-source Finance Toolkit</td></tr>
<tr><th scope="row">Same question, two chats</th><td data-label="Raw data servers">Often two different numbers</td><td data-label="Finance Toolkit MCP">The same number</td></tr>
<tr><th scope="row">Definitions</th><td data-label="Raw data servers">Implicit, chosen by the model</td><td data-label="Finance Toolkit MCP"><a href="/projects/financetoolkit/docs">Documented</a> for every metric</td></tr>
<tr><th scope="row">Macroeconomic data</th><td data-label="Raw data servers">Rarely included</td><td data-label="Finance Toolkit MCP">60+ countries from the OECD, the Global Macro Database and FRED</td></tr>
</tbody>
</table>
</div>

The Finance Toolkit behind the server has been downloaded over 600,000 times and every formula is in the [documentation](/projects/financetoolkit/docs), so a number from a chat can be traced back to its calculation. I designed the 22 categorical tools so that small and large models alike use them reliably.

If you only need a quote or a headline number, a raw data server is fine. If you want to ask *"which of these banks is the most solvent, and why"* and get an answer you can defend, that is what I built this server for.

## What You Can Ask

You never have to name a tool or an indicator: ask in plain English and the assistant picks the right one. A few examples of what that covers:

<div class="mcp-uses">
  <div class="mcp-use"><i class="fas fa-building" aria-hidden="true"></i><h3>Company fundamentals</h3><p>"Which is more profitable, Apple or Microsoft, and does that change when you look at return on capital?"</p><span>profitability, efficiency, liquidity, solvency</span></div>
  <div class="mcp-use"><i class="fas fa-scale-balanced" aria-hidden="true"></i><h3>Valuation and credit</h3><p>"What growth is priced into Nvidia's share price based on a discounted cash flow?"</p><span>valuation, models (DCF, WACC, DuPont, Altman Z)</span></div>
  <div class="mcp-use"><i class="fas fa-shield-halved" aria-hidden="true"></i><h3>Performance and risk</h3><p>"Compare the Value at Risk and maximum drawdown of Berkshire Hathaway, Visa and Costco since 2020."</p><span>performance, risk, options</span></div>
  <div class="mcp-use"><i class="fas fa-chart-line" aria-hidden="true"></i><h3>Technical analysis</h3><p>"Is the semiconductor sector overbought? Check the RSI and moving averages of NVDA, AMD and ASML."</p><span>momentum, overlap, volatility, breadth</span></div>
  <div class="mcp-use"><i class="fas fa-earth-europe" aria-hidden="true"></i><h3>Macro and rates</h3><p>"How do real interest rates in the US and the Eurozone compare since the inflation peak?"</p><span>macroeconomics, rates, jobs, government, fixed income</span></div>
  <div class="mcp-use"><i class="fas fa-square-root-variable" aria-hidden="true"></i><h3>Econometrics</h3><p>"Regress Apple's weekly returns on its suppliers and peers. Which coefficients are significant?"</p><span>econometrics</span></div>
</div>

The [example conversations](#example-conversations) below show what that looks like for four larger questions, from an investment case to the economic cycle.



## Installation

Pick the [remote server](#remote-server) if you want to get going without installing anything, or the [local server](#local-clients) if you prefer to run the process yourself. Each section lists the same clients, so you can switch between the two at any time.

### Remote Server

Point your client at the URL below. On first use it opens an OAuth page asking for your [FMP API key](/fmp){:target="_blank"}; enter it once and the server takes it from there.

```
https://financetoolkit.jeroenbouma.com/mcp
```

Pick your client below for the exact steps; most clients accept the URL through their settings or with a single command.

<div class="ft-tabs" markdown="1">

<details class="ft-details" id="remote-claude-desktop" markdown="1">
  <summary><i class="fas fa-robot"></i> <h3>Claude Desktop</h3></summary>

  1. Open **Claude Desktop** and click on **Customize**.
  2. Go to the **Connectors** tab, click on the "+" button and select **Add custom connector**.
  3. Enter a name, e.g. *Finance Toolkit*, and paste the URL:
     ```
     https://financetoolkit.jeroenbouma.com/mcp
     ```
  4. Click "Add" to add the Finance Toolkit MCP server to your list of connectors.
  5. On first use Claude Desktop opens a browser window asking for your [FMP API key](/fmp){:target="_blank"}. Enter it once and the server remembers it.

</details>

<details class="ft-details" id="remote-claude-ai" markdown="1">
  <summary><i class="fas fa-globe"></i> <h3>Claude.ai</h3></summary>

  1. Open [claude.ai](https://claude.ai){:target="_blank"} and click on **Customize** in the left sidebar.
  2. Go to the **Connectors** tab, click on the "+" button and select **Add custom connector**.
  3. Enter a name, e.g. *Finance Toolkit*, and paste the URL:
     ```
     https://financetoolkit.jeroenbouma.com/mcp
     ```
  4. Click "Add" to add the Finance Toolkit MCP server to your list of connectors.
  5. On first use Claude.ai opens a browser window asking for your [FMP API key](/fmp){:target="_blank"}. Enter it once and the server remembers it.

</details>

<details class="ft-details" id="remote-claude-code" markdown="1">
  <summary><i class="fas fa-terminal"></i> <h3>Claude Code</h3></summary>

  1. Run the following command once in your terminal:
     ```bash
     claude mcp add --transport http finance-toolkit https://financetoolkit.jeroenbouma.com/mcp
     ```
  2. Restart Claude Code and the Finance Toolkit tools appear automatically. The first tool call opens the browser for the OAuth step where you enter your [FMP API key](/fmp){:target="_blank"}.

</details>

<details class="ft-details" id="remote-chatgpt" markdown="1">
  <summary><i class="fas fa-comment-dots"></i> <h3>ChatGPT</h3></summary>

  ChatGPT connects to custom MCP servers through **Developer mode** (available on paid ChatGPT plans):

  1. Open **Settings → Apps & Connectors → Advanced settings** and enable **Developer mode**.
  2. Back in **Apps & Connectors**, click **Create** and enter a name, e.g. *Finance Toolkit*, and the MCP server URL:
     ```
     https://financetoolkit.jeroenbouma.com/mcp
     ```
  3. Select **OAuth** as the authentication method and click **Create**. A browser window asks for your [FMP API key](/fmp){:target="_blank"}; enter it once.
  4. In a new chat, open the **+** menu, enable the *Finance Toolkit* connector under **Developer mode** and start asking questions.

</details>

<details class="ft-details" id="remote-codex" markdown="1">
  <summary><i class="fas fa-code"></i> <h3>Codex CLI</h3></summary>

  1. Run the following command once in your terminal:
     ```bash
     codex mcp add finance-toolkit --url https://financetoolkit.jeroenbouma.com/mcp
     ```
  2. Authenticate with `codex mcp login finance-toolkit`, which opens the browser for the OAuth step where you enter your [FMP API key](/fmp){:target="_blank"}.
  3. Start `codex` and the Finance Toolkit tools are available in every session.

</details>

<details class="ft-details" id="remote-vs-code" markdown="1">
  <summary><i class="fab fa-microsoft"></i> <h3>VS Code and GitHub Copilot</h3></summary>

  1. Open the **Command Palette** (`Cmd+Shift+P` / `Ctrl+Shift+P`) and run **MCP: Add Server**.
  2. Select **HTTP** as the server type.
  3. Enter the URL `https://financetoolkit.jeroenbouma.com/mcp` and name it *finance-toolkit*.
  4. VS Code writes the entry to `.vscode/mcp.json` (or your user profile) automatically and the tools show up in Copilot's **Agent** mode.
  5. On first tool call VS Code opens an OAuth prompt for your [FMP API key](/fmp){:target="_blank"}.

</details>

<details class="ft-details" id="remote-cursor" markdown="1">
  <summary><i class="fas fa-i-cursor"></i> <h3>Cursor</h3></summary>

  1. Open **Cursor Settings** (`Cmd+,` / `Ctrl+,`) and navigate to **Features → MCP Servers**.
  2. Click **+ Add new MCP server**.
  3. Set the type to **http** and paste the URL:
     ```
     https://financetoolkit.jeroenbouma.com/mcp
     ```
  4. Name it *finance-toolkit* and click **Save**.
  5. On first tool call Cursor opens an OAuth prompt for your [FMP API key](/fmp){:target="_blank"}.

</details>

<details class="ft-details" id="remote-windsurf" markdown="1">
  <summary><i class="fas fa-wind"></i> <h3>Windsurf</h3></summary>

  1. Open **Windsurf Settings** and navigate to **MCP Servers**.
  2. Click **Add Server** and select **Remote / HTTP**.
  3. Paste the URL `https://financetoolkit.jeroenbouma.com/mcp` and name it *finance-toolkit*.
  4. Click **Save** and reload the window.
  5. On first tool call Windsurf opens an OAuth prompt for your [FMP API key](/fmp){:target="_blank"}.

</details>

<details class="ft-details" id="remote-gemini" markdown="1">
  <summary><i class="fab fa-google"></i> <h3>Gemini CLI</h3></summary>

  1. Run the following command once in your terminal:
     ```bash
     gemini mcp add --transport http finance-toolkit https://financetoolkit.jeroenbouma.com/mcp
     ```
     Alternatively, add the entry to `~/.gemini/settings.json` by hand:
     ```json
     {
       "mcpServers": {
         "finance-toolkit": {
           "httpUrl": "https://financetoolkit.jeroenbouma.com/mcp"
         }
       }
     }
     ```
  2. Start `gemini` and run `/mcp` to confirm the server is connected; the first tool call opens the OAuth prompt for your [FMP API key](/fmp){:target="_blank"}.

</details>

</div>

### Local Clients

The local server runs on your own machine through `uvx` and works with every client that supports the `stdio` transport. The setup wizard finds your client's config file and writes the entry, including your API key, for you:

```bash
uvx --from "financetoolkit[mcp]" financetoolkit-mcp-setup
```

If you prefer to do it by hand, pick your client below and add the snippet to its config file, replacing `FINANCIAL_MODELING_PREP_KEY` with your [FMP API key](/fmp){:target="_blank"}. The [API keys and environment variables](#local-api-keys) card at the end covers the `.env` file option and the optional FRED key.

<div class="ft-tabs" markdown="1">

<details class="ft-details" id="local-claude-desktop" markdown="1">
  <summary><i class="fas fa-robot"></i> <h3>Claude Desktop</h3></summary>

  **Easiest installation is via the MCPB bundle**, which handles configuration automatically. Download the [Finance Toolkit MCPB bundle](https://github.com/JerBouma/FinanceToolkit/releases/latest/download/financetoolkit.mcpb){:target="_blank"} and double-click it to start installation.

  Alternatively, edit `claude_desktop_config.json` and add the entry inside `mcpServers`:

  - macOS: `~/Library/Application Support/Claude/`
  - Windows: `%APPDATA%\Claude\`
  - Linux: `~/.config/claude/`

  ```json
  {
    "mcpServers": {
      "finance-toolkit": {
        "command": "uvx",
        "args": ["--from", "financetoolkit[mcp]", "financetoolkit-mcp"],
        "env": { "FINANCIAL_MODELING_PREP_API_KEY": "FINANCIAL_MODELING_PREP_KEY" }
      }
    }
  }
  ```

</details>

<details class="ft-details" id="local-claude-ai" markdown="1">
  <summary><i class="fas fa-globe"></i> <h3>Claude.ai</h3></summary>

  Claude.ai runs in the browser and cannot start a process on your machine, so it only connects to servers over HTTP. Use the [remote server](#remote-claude-ai) instead, or run the local server with `MCP_TRANSPORT=streamable-http` behind a public URL of your own.

</details>

<details class="ft-details" id="local-claude-code" markdown="1">
  <summary><i class="fas fa-terminal"></i> <h3>Claude Code</h3></summary>

  Run the following command once in your terminal:

  ```bash
  claude mcp add --transport stdio finance-toolkit --env FINANCIAL_MODELING_PREP_API_KEY=FINANCIAL_MODELING_PREP_KEY -- uvx --from "financetoolkit[mcp]" financetoolkit-mcp
  ```

  Or edit `~/.claude.json` (create it if needed) and merge the entry inside `mcpServers`:

  ```json
  {
    "mcpServers": {
      "finance-toolkit": {
        "command": "uvx",
        "args": ["--from", "financetoolkit[mcp]", "financetoolkit-mcp"],
        "env": { "FINANCIAL_MODELING_PREP_API_KEY": "FINANCIAL_MODELING_PREP_KEY" }
      }
    }
  }
  ```

</details>

<details class="ft-details" id="local-chatgpt" markdown="1">
  <summary><i class="fas fa-comment-dots"></i> <h3>ChatGPT</h3></summary>

  ChatGPT only connects to MCP servers over HTTP and cannot start a local process. Use the [remote server](#remote-chatgpt) instead, or run the local server with `MCP_TRANSPORT=streamable-http` behind a public URL of your own.

</details>

<details class="ft-details" id="local-codex" markdown="1">
  <summary><i class="fas fa-code"></i> <h3>Codex CLI</h3></summary>

  Run the following command once in your terminal:

  ```bash
  codex mcp add finance-toolkit --env FINANCIAL_MODELING_PREP_API_KEY=FINANCIAL_MODELING_PREP_KEY -- uvx --from "financetoolkit[mcp]" financetoolkit-mcp
  ```

  Or add the entry to `~/.codex/config.toml`:

  ```toml
  [mcp_servers.finance-toolkit]
  command = "uvx"
  args = ["--from", "financetoolkit[mcp]", "financetoolkit-mcp"]
  env = { FINANCIAL_MODELING_PREP_API_KEY = "FINANCIAL_MODELING_PREP_KEY" }
  ```

</details>

<details class="ft-details" id="local-vs-code" markdown="1">
  <summary><i class="fab fa-microsoft"></i> <h3>VS Code and GitHub Copilot</h3></summary>

  **Workspace**: create or edit `.vscode/mcp.json` in your workspace root. VS Code uses `servers` as the top-level key (not `mcpServers`):

  ```json
  {
    "servers": {
      "finance-toolkit": {
        "command": "uvx",
        "args": ["--from", "financetoolkit[mcp]", "financetoolkit-mcp"],
        "env": { "FINANCIAL_MODELING_PREP_API_KEY": "FINANCIAL_MODELING_PREP_KEY" }
      }
    }
  }
  ```

  **Global (all workspaces)**: add the same block under `"mcp"` in your user `settings.json`:

  - macOS: `~/Library/Application Support/Code/User/settings.json`
  - Windows: `%APPDATA%\Code\User\settings.json`
  - Linux: `~/.config/Code/User/settings.json`

  ```json
  {
    "mcp": {
      "servers": {
        "finance-toolkit": {
          "command": "uvx",
          "args": ["--from", "financetoolkit[mcp]", "financetoolkit-mcp"],
          "env": { "FINANCIAL_MODELING_PREP_API_KEY": "FINANCIAL_MODELING_PREP_KEY" }
        }
      }
    }
  }
  ```

</details>

<details class="ft-details" id="local-cursor" markdown="1">
  <summary><i class="fas fa-i-cursor"></i> <h3>Cursor</h3></summary>

  **Workspace**: create or edit `.cursor/mcp.json` in your workspace root:

  ```json
  {
    "mcpServers": {
      "finance-toolkit": {
        "command": "uvx",
        "args": ["--from", "financetoolkit[mcp]", "financetoolkit-mcp"],
        "env": { "FINANCIAL_MODELING_PREP_API_KEY": "FINANCIAL_MODELING_PREP_KEY" }
      }
    }
  }
  ```

  **Global (all projects)**: create or edit `~/.cursor/mcp.json`:

  ```json
  {
    "mcpServers": {
      "finance-toolkit": {
        "command": "uvx",
        "args": ["--from", "financetoolkit[mcp]", "financetoolkit-mcp"],
        "env": { "FINANCIAL_MODELING_PREP_API_KEY": "FINANCIAL_MODELING_PREP_KEY" }
      }
    }
  }
  ```

</details>

<details class="ft-details" id="local-windsurf" markdown="1">
  <summary><i class="fas fa-wind"></i> <h3>Windsurf</h3></summary>

  Edit `~/.codeium/windsurf/mcp_config.json` (create it if needed):

  ```json
  {
    "mcpServers": {
      "finance-toolkit": {
        "command": "uvx",
        "args": ["--from", "financetoolkit[mcp]", "financetoolkit-mcp"],
        "env": { "FINANCIAL_MODELING_PREP_API_KEY": "FINANCIAL_MODELING_PREP_KEY" }
      }
    }
  }
  ```

</details>

<details class="ft-details" id="local-gemini" markdown="1">
  <summary><i class="fab fa-google"></i> <h3>Gemini CLI</h3></summary>

  Edit `~/.gemini/settings.json` (create it if needed):

  ```json
  {
    "mcpServers": {
      "finance-toolkit": {
        "command": "uvx",
        "args": ["--from", "financetoolkit[mcp]", "financetoolkit-mcp"],
        "env": { "FINANCIAL_MODELING_PREP_API_KEY": "FINANCIAL_MODELING_PREP_KEY" }
      }
    }
  }
  ```

</details>

</div>

<details class="ft-details ft-details--warning" id="local-api-keys" markdown="1">
  <summary><i class="fas fa-key"></i> <h3>API keys and environment variables</h3></summary>

  In every snippet `uvx` is the *command* and the rest are *args*. The `env` block takes either `FINANCIAL_MODELING_PREP_API_KEY` with the key inline, or `FINANCETOOLKIT_ENV_FILE` with the path to a `.env` file that contains `FINANCIAL_MODELING_PREP_API_KEY=FINANCIAL_MODELING_PREP_KEY`; when both are present the inline key wins.

  A second key, `FRED_API_KEY`, is optional and free. It is only needed for a handful of US-only indicators without an OECD or FMP equivalent (nonfarm payrolls, initial jobless claims, the 30-year mortgage rate, the TIPS real yield curve and breakeven inflation expectations). The setup wizard picks it up automatically from your environment or `.env` file; [register for one here](https://fred.stlouisfed.org/docs/api/api_key.html){:target="_blank"}.

  `financetoolkit[mcp]` also installs the `econometrics` extra, so `statsmodels` and `linearmodels` come along and the `econometrics` tool works out of the box.

</details>

## Example Conversations

Four questions of the kind an analyst or portfolio manager would ask, each answered by Claude through the server. None of them is a single lookup: Claude decides which calculations it needs, chains them across tools and builds its conclusion on the results. Every number and chart below comes from a Finance Toolkit calculation, with data up to October 2, 2026.

The server returns the same calculated data to every model, and I designed its 22 tools to be simple enough for smaller models as well: GPT-5 mini, Claude Haiku and similar models pick the right tools and report the same numbers. A larger model mostly adds depth, such as the follow-up calculations and caveats you see here.

<div class="ca-nav ca-nav--4">
  <a href="#ex-asml"><i class="fas fa-microchip" aria-hidden="true"></i>An investment case for ASML</a>
  <a href="#ex-bank-solvency"><i class="fas fa-landmark" aria-hidden="true"></i>Europe's most solid bank</a>
  <a href="#ex-us-cycle"><i class="fas fa-earth-americas" aria-hidden="true"></i>Where is the US cycle?</a>
  <a href="#ex-diversification"><i class="fas fa-shuffle" aria-hidden="true"></i>What really diversifies?</a>
</div>

<div class="mcp-show" id="ex-asml">
<div class="ca-q"><span class="ca-q__avatar"><i class="fas fa-user" aria-hidden="true"></i></span><p>Build an investment case for ASML against Applied Materials, Lam Research and KLA: profitability, valuation, returns and risk. Is its premium justified?</p></div>
<div class="mcp-show__meta"><span><b>6</b> tool calls</span><span><b>4</b> companies</span><span><b>130+</b> calculated values</span></div>
<details class="mcp-show__trace"><summary><i class="fas fa-list-check" aria-hidden="true"></i> What Claude calculated</summary><ol><li><code>profitability</code><span>Return on invested capital, 2020 to 2025</span></li><li><code>profitability</code><span>Gross margin, 2020 to 2025</span></li><li><code>valuation</code><span>EV/EBITDA, 2020 to 2026</span></li><li><code>valuation</code><span>Price-to-earnings, 2020 to 2026</span></li><li><code>performance</code><span>Annual returns since 2021, against the S&P 500</span></li><li><code>risk</code><span>Maximum drawdown since 2021</span></li></ol></details>

<div class="mcp-show__grid">
<div class="mcp-show__cell">{% include ft-chart.html id="mcp-asml-quality" src="/assets/data/article-charts.json" label="ROIC and gross margin of ASML and peers" %}</div>
<div class="mcp-show__cell">{% include ft-chart.html id="mcp-asml-price" src="/assets/data/article-charts.json" label="ROIC against EV/EBITDA" %}</div>
<div class="mcp-show__cell mcp-show__cell--wide">{% include ft-chart.html id="mcp-asml-risk" src="/assets/data/article-charts.json" label="Growth of a dollar and maximum drawdown" %}</div>
</div>
<div class="mcp-show__verdict"><p class="mcp-show__label"><i class="fas fa-robot" aria-hidden="true"></i> Claude's conclusion</p><p>ASML's premium has turned into a discount. It earned the highest return on invested capital of the four in 2025 (33.0%), yet trades at 27.6 times EBITDA, below KLA (30.7x) and Lam Research (34.8x). The market has rewarded the peers' cyclical recovery instead: a dollar in ASML at the start of 2021 grew to $3.93, against $8.42 for KLA and $7.70 for Lam. KLA stands out on quality and resilience, with the highest gross margin (60.9%) and the shallowest drawdown (−35%), but it has also re-rated the most since.</p></div>
<div class="ca-nums"><span><b>33.0%</b>ASML ROIC 2025, the highest</span><span><b>27.6x vs 34.8x</b>EV/EBITDA, ASML vs Lam</span><span><b>$3.93 vs $8.42</b>$1 since 2021, ASML vs KLA</span></div>
</div>

<div class="mcp-show" id="ex-bank-solvency">
<div class="ca-q"><span class="ca-q__avatar"><i class="fas fa-user" aria-hidden="true"></i></span><p>Which of Europe's largest banks is the most solid, and does the market pay for it?</p></div>
<div class="mcp-show__meta"><span><b>5</b> tool calls</span><span><b>9</b> banks</span><span><b>80+</b> calculated values</span></div>
<details class="mcp-show__trace"><summary><i class="fas fa-list-check" aria-hidden="true"></i> What Claude calculated</summary><ol><li><code>models</code><span>Equity multiplier (total assets per unit of equity)</span></li><li><code>solvency</code><span>Debt to equity and debt service coverage</span></li><li><code>profitability</code><span>Return on equity, 2023 to 2025</span></li><li><code>valuation</code><span>Price to book, 2025</span></li><li><code>market_data</code><span>Balance sheets, converted to US dollars</span></li></ol></details>
<p class="mcp-show__note"><i class="fas fa-circle-info" aria-hidden="true"></i> Intesa Sanpaolo's price to book comes out at an implausible 0.29. Claude traces it to the share count: from 2024 the data reports about 0.5 billion ADR shares instead of roughly 3 billion, so book value per share is six times too high. It leaves Intesa out of the valuation comparison rather than presenting it as the cheapest bank.</p>
<div class="mcp-show__grid">
<div class="mcp-show__cell">{% include ft-chart.html id="mcp-banks-lev" src="/assets/data/article-charts.json" label="Equity multiplier of nine European banks" %}</div>
<div class="mcp-show__cell">{% include ft-chart.html id="mcp-banks-value" src="/assets/data/article-charts.json" label="Return on equity against price to book" %}</div>
<div class="mcp-show__cell mcp-show__cell--wide">{% include ft-chart.html id="mcp-banks-roe" src="/assets/data/article-charts.json" label="Return on equity since 2023" %}</div>
</div>
<div class="mcp-show__verdict"><p class="mcp-show__label"><i class="fas fa-robot" aria-hidden="true"></i> Claude's conclusion</p><p>UniCredit is the most solid bank of the group and the most profitable: the thickest equity buffer (an equity multiplier of 12.6x), the highest debt service coverage and a return on equity of 17.3%. The market does pay for it, at 1.64 times book, the highest multiple of the group. The cheapest banks are cheap for a reason: BNP Paribas trades at 0.68 times book with a 9.2% return on equity and among the most leverage, Société Générale earns 7.2%.</p></div>
<div class="ca-nums"><span><b>12.6x</b>UniCredit equity multiplier, lowest</span><span><b>17.3%</b>UniCredit return on equity</span><span><b>1.64x vs 0.68x</b>price to book, UniCredit vs BNP</span></div>
</div>

<div class="mcp-show" id="ex-us-cycle">
<div class="ca-q"><span class="ca-q__avatar"><i class="fas fa-user" aria-hidden="true"></i></span><p>Where is the US economy in the cycle? Look at the yield curve, inflation, the policy rate, unemployment and growth.</p></div>
<div class="mcp-show__meta"><span><b>5</b> tool calls</span><span><b>4</b> years of daily yields</span><span><b>1,100+</b> data points</span></div>
<details class="mcp-show__trace"><summary><i class="fas fa-list-check" aria-hidden="true"></i> What Claude calculated</summary><ol><li><code>rates</code><span>US Treasury yield curve, daily since 2022</span></li><li><code>macroeconomics</code><span>Inflation rate</span></li><li><code>rates</code><span>Central bank policy rate</span></li><li><code>jobs</code><span>Unemployment rate</span></li><li><code>macroeconomics</code><span>Real GDP growth</span></li></ol></details>

<div class="mcp-show__grid">
<div class="mcp-show__cell mcp-show__cell--wide">{% include ft-chart.html id="mcp-macro-curve" src="/assets/data/article-charts.json" label="US 10-year minus 2-year Treasury spread" %}</div>
<div class="mcp-show__cell">{% include ft-chart.html id="mcp-macro-rates" src="/assets/data/article-charts.json" label="US inflation against the policy rate" %}</div>
<div class="mcp-show__cell">{% include ft-chart.html id="mcp-macro-real" src="/assets/data/article-charts.json" label="US unemployment and real GDP growth" %}</div>
</div>
<div class="mcp-show__verdict"><p class="mcp-show__label"><i class="fas fa-robot" aria-hidden="true"></i> Claude's conclusion</p><p>Late in the cycle, but not in recession. The yield curve inverted from July 2022 to September 2024, at its deepest −1.08 percentage points in July 2023, the classic recession signal. The recession never came: real GDP grew 2.5% to 2.9% a year in 2022 to 2024, and unemployment rose only gradually, from 3.6% to 4.4%. With inflation back at 1.9% in 2025 and the policy rate at 4.3%, the real policy rate is still clearly positive, which leaves the Fed room to ease. The curve is upward sloping again, at +0.45 percentage points.</p></div>
<div class="ca-nums"><span><b>+0.45 pp</b>10y − 2y spread today</span><span><b>1.9%</b>inflation 2025</span><span><b>4.3%</b>policy rate 2025</span><span><b>4.4%</b>unemployment 2025</span></div>
</div>

<div class="mcp-show" id="ex-diversification">
<div class="ca-q"><span class="ca-q__avatar"><i class="fas fa-user" aria-hidden="true"></i></span><p>My portfolio is heavy in Nvidia and Microsoft. Which of JPMorgan, ExxonMobil and Johnson & Johnson actually diversifies it?</p></div>
<div class="mcp-show__meta"><span><b>3</b> tool calls</span><span><b>5</b> stocks plus the S&P 500</span><span><b>3</b> years of weekly returns</span></div>
<details class="mcp-show__trace"><summary><i class="fas fa-list-check" aria-hidden="true"></i> What Claude calculated</summary><ol><li><code>performance</code><span>Correlation matrix of weekly returns, October 2023 to October 2026</span></li><li><code>performance</code><span>Quarterly returns</span></li><li><code>risk</code><span>Maximum drawdown</span></li></ol></details>

<div class="mcp-show__grid">
<div class="mcp-show__cell">{% include ft-chart.html id="mcp-div-corr" src="/assets/data/article-charts.json" label="Correlation matrix of weekly returns" %}</div>
<div class="mcp-show__cell">{% include ft-chart.html id="mcp-div-quarters" src="/assets/data/article-charts.json" label="Quarterly returns of NVDA, MSFT, XOM and JNJ" %}</div>
</div>
<div class="mcp-show__verdict"><p class="mcp-show__label"><i class="fas fa-robot" aria-hidden="true"></i> Claude's conclusion</p><p>ExxonMobil and Johnson & Johnson are the real diversifiers; JPMorgan mostly adds more market exposure. JPMorgan moves with Nvidia (a correlation of 0.34) and with the market (0.63). ExxonMobil and J&amp;J are negatively correlated with both Nvidia and Microsoft and barely related to the S&amp;P 500. The quarters that matter confirm it: in the first quarter of 2025, Nvidia fell 19.3% and Microsoft 10.7% while ExxonMobil rose 11.6% and J&amp;J 15.6%, and in the first quarter of 2026 Microsoft lost 23.3% while ExxonMobil gained 41.9%.</p></div>
<div class="ca-nums"><span><b>−0.23</b>MSFT and XOM correlation</span><span><b>0.63</b>JPM and S&amp;P 500 correlation</span><span><b>+41.9% vs −23.3%</b>Q1 2026, XOM vs MSFT</span></div>
</div>

## FAQ

The questions that come up most often about the server, its data sources and how it compares to other financial MCP servers. Anything missing? Open an issue on [GitHub](https://github.com/JerBouma/FinanceToolkit/issues){:target="_blank"}.

<details class="ft-details" markdown="1">
  <summary><h3>Is the Finance Toolkit MCP server free?</h3></summary>

  Yes. The server and the [Finance Toolkit](/projects/financetoolkit) it is built on are open source under the MIT license (see the [repository](https://github.com/JerBouma/FinanceToolkit){:target="_blank"}) and the hosted server is free to use. The only thing you need is a [Financial Modeling Prep API key](/fmp){:target="_blank"}; the free plan is enough to try the server, and the paid plans add full history, all exchanges and higher request limits.

</details>

<details class="ft-details" markdown="1">
  <summary><h3>Which AI assistants and clients does it work with?</h3></summary>

  Any client that speaks the Model Context Protocol. There are step-by-step cards for Claude Desktop, claude.ai, Claude Code, ChatGPT, Codex CLI, VS Code, Cursor, Windsurf and Gemini CLI under [Remote Server](#remote-server) and [Local Clients](#local-clients); other clients work the same way with the URL or the `uvx` command from those cards.

</details>

<details class="ft-details" markdown="1">
  <summary><h3>How do I add the server to my client?</h3></summary>

  For the remote server, give your client the URL and enter your FMP API key on the OAuth page that opens the first time:

  ```
  https://financetoolkit.jeroenbouma.com/mcp
  ```

  Clients with a command line take it in one go, for example Claude Code:

  ```bash
  claude mcp add --transport http finance-toolkit https://financetoolkit.jeroenbouma.com/mcp
  ```

  For the local server, let the wizard write the config entry for you:

  ```bash
  uvx --from "financetoolkit[mcp]" financetoolkit-mcp-setup
  ```

  The exact steps and settings dialogs per client are in the [Remote Server](#remote-server) and [Local Clients](#local-clients) cards.

</details>

<details class="ft-details" markdown="1">
  <summary><h3>Do I need to install Python?</h3></summary>

  No. The [remote server](#remote-server) needs nothing installed. The [local server](#local-clients) runs through [uv](https://docs.astral.sh/uv/getting-started/installation/){:target="_blank"}, which downloads the right Python and the package by itself, so even then you never install Python or run `pip` yourself.

</details>

<details class="ft-details" markdown="1">
  <summary><h3>Can I run the server locally?</h3></summary>

  Yes. Run the setup wizard and pick your client, it writes the config entry including your API key:

  ```bash
  uvx --from "financetoolkit[mcp]" financetoolkit-mcp-setup
  ```

  Or add the entry to your client's MCP config by hand:

  ```json
  {
    "mcpServers": {
      "finance-toolkit": {
        "command": "uvx",
        "args": ["--from", "financetoolkit[mcp]", "financetoolkit-mcp"],
        "env": { "FINANCIAL_MODELING_PREP_API_KEY": "FINANCIAL_MODELING_PREP_KEY" }
      }
    }
  }
  ```

  Config file locations per client are in the [Local Clients](#local-clients) cards, the `.env` file option and the optional FRED key in the [API keys and environment variables](#local-api-keys) card, and Claude Desktop users can skip all of this with the [MCPB bundle](#local-claude-desktop).

</details>

<details class="ft-details" markdown="1">
  <summary><h3>Is my Financial Modeling Prep API key stored on the server?</h3></summary>

  No. During the OAuth login your key is sealed inside a signed token that your MCP client holds and sends with every request; the server reads it for the duration of that request and never writes it to disk or a database. The full flow is on the [Under the Hood](/projects/financetoolkit/mcp/architecture#oauth-21-and-api-key-resolution) page.

</details>

<details class="ft-details" markdown="1">
  <summary><h3>What data does the server cover?</h3></summary>

  Company data comes from [Financial Modeling Prep](/fmp){:target="_blank"}: historical prices, financial statements, profiles, ESG scores and estimates for stocks and ETFs on exchanges worldwide, subject to your FMP plan. Macroeconomic data comes from the OECD and, optionally, [FRED](https://fred.stlouisfed.org/docs/api/api_key.html){:target="_blank"}. [Which tools does the server expose?](#faq-tools) lists what is computed on top of that, and the [Finance Toolkit documentation](/projects/financetoolkit/docs) describes every metric and model in detail.

</details>

<details class="ft-details" id="faq-tools" markdown="1">
  <summary><h3>Which tools does the server expose?</h3></summary>

  The 500+ Finance Toolkit methods are grouped into 22 categorical tools, each taking an `indicator` parameter that selects the exact metric (e.g. `valuation` with `indicator='get_price_to_earnings_ratio'`), plus four search tools to navigate them. You never pick these by hand: the assistant chooses the tool and indicator from your plain-English question. Equity tools accept `tickers` (e.g. `'AAPL,MSFT'`), macro tools accept `countries` (e.g. `'United States,Germany'`), and all accept `start_date`, `end_date` and `quarterly`. Every tool returns data as standardized Markdown.

| Category | Tool | Description |
|:---|:---|:---|
| Fundamentals | `discovery` | Stock and ETF screener, gainers/losers, most active |
| Fundamentals | `market_data` | Historical prices, financial statements, company profile, real-time quote |
| Fundamentals | `environment` | ESG scores, carbon footprint, renewable energy usage |
| Fundamentals | `performance` | Sharpe ratio, Sortino ratio, Alpha, Beta, CAPM, Fama-French, Carhart, market timing |
| Fundamentals | `risk` | Value at Risk, CVaR, GARCH/EGARCH/GJR-GARCH, max drawdown, copulas, realized volatility |
| Fundamentals | `options` | Black-Scholes pricing, binomial tree, Greeks, implied volatility, exotic options |
| Econometrics | `econometrics` | Regression (OLS/WLS/GLS, logit, probit, quantile, Fama-MacBeth), panel data, causal inference (IV-2SLS, difference-in-differences, regression discontinuity, propensity score matching, synthetic control), unit root and cointegration tests, Granger causality, ARIMA/VAR/VECM forecasting and event studies |
| Ratios and Models | `efficiency` | Asset/inventory turnover, days of sales outstanding, cash conversion cycle |
| Ratios and Models | `liquidity` | Current ratio, quick ratio, cash ratio, working capital |
| Ratios and Models | `profitability` | Gross/net/operating margin, ROE, ROA, ROIC, ROCE |
| Ratios and Models | `solvency` | Debt-to-equity, interest coverage, net debt to EBITDA |
| Ratios and Models | `valuation` | P/E, EPS, EV/EBITDA, P/B, P/S, dividend yield, free cash flow yield |
| Ratios and Models | `models` | WACC, DuPont analysis, Altman Z-Score, Piotroski F-Score, intrinsic value, FCFF/FCFE, Tobin's Q, five bankruptcy scores |
| Technical Indicators | `momentum` | RSI, MACD, Stochastic oscillator, Williams %R, Aroon |
| Technical Indicators | `overlap` | SMA, EMA, Bollinger Bands, Keltner Channels |
| Technical Indicators | `volatility` | Average True Range, True Range, volatility series |
| Technical Indicators | `breadth` | McClellan oscillator, OBV, Advance/Decline line, Chaikin |
| Macro and Fixed Income | `macroeconomics` | GDP, CPI, inflation, trade balances, investment, consumption |
| Macro and Fixed Income | `government` | Government debt, deficit, expenditure, revenue, tax rates |
| Macro and Fixed Income | `jobs` | Unemployment, population, poverty, income inequality |
| Macro and Fixed Income | `rates` | Central bank rates, government bond yields, EURIBOR, US Treasury par yield curve, TIPS real yields |
| Macro and Fixed Income | `fixed_income` | Bond duration, present value, YTM, derivative pricing, par/forward rates, Z-spread, key rate duration |
| Search | `search_categories` | Lists all categories and the number of tools each contains |
| Search | `search_by_category` | Lists every metric available within a given category |
| Search | `search_metrics` | Fuzzy keyword search across all metrics with typo tolerance |
| Search | `search_instruments` | Look up ticker symbols by company name, ISIN, CIK, CUSIP or symbol |

  Each tool wraps dozens of underlying Finance Toolkit functions; the [Finance Toolkit documentation](/projects/financetoolkit/docs) describes every metric, model and parameter that can be reached through them. To explore interactively, run `uvx --from "financetoolkit[mcp]" financetoolkit-mcp-inspector`.

</details>

<details class="ft-details" markdown="1">
  <summary><h3>How is this different from the Financial Modeling Prep or Yahoo Finance MCP servers?</h3></summary>

  Those servers return raw data and leave the calculations to the language model. The Finance Toolkit MCP computes 500+ metrics, ratios, models and indicators with the open-source [Finance Toolkit](/projects/financetoolkit) code, so the numbers are consistent, documented and reproducible regardless of which model you use. [Why the Finance Toolkit MCP](#why-the-finance-toolkit-mcp) goes into this in more depth.

</details>

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Is the Finance Toolkit MCP server free?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes. The server and the Finance Toolkit it is built on are open source under the MIT license (see the repository) and the hosted server is free to use. The only thing you need is a Financial Modeling Prep API key; the free plan is enough to try the server, and the paid plans add full history, all exchanges and higher request limits."
      }
    },
    {
      "@type": "Question",
      "name": "Which AI assistants and clients does it work with?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Any client that speaks the Model Context Protocol. There are step-by-step cards for Claude Desktop, claude.ai, Claude Code, ChatGPT, Codex CLI, VS Code, Cursor, Windsurf and Gemini CLI under Remote Server and Local Clients; other clients work the same way with the URL or the uvx command from those cards."
      }
    },
    {
      "@type": "Question",
      "name": "How do I add the server to my client?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "For the remote server, give your client the URL and enter your FMP API key on the OAuth page that opens the first time: https://financetoolkit.jeroenbouma.com/mcp Clients with a command line take it in one go, for example Claude Code: claude mcp add --transport http finance-toolkit https://financetoolkit.jeroenbouma.com/mcp For the local server, let the wizard write the config entry for you: uvx --from \"financetoolkit[mcp]\" financetoolkit-mcp-setup The exact steps and settings dialogs per client are in the Remote Server and Local Clients cards."
      }
    },
    {
      "@type": "Question",
      "name": "Do I need to install Python?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "No. The remote server needs nothing installed. The local server runs through uv, which downloads the right Python and the package by itself, so even then you never install Python or run pip yourself."
      }
    },
    {
      "@type": "Question",
      "name": "Can I run the server locally?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes. Run the setup wizard and pick your client, it writes the config entry including your API key: uvx --from \"financetoolkit[mcp]\" financetoolkit-mcp-setup Or add the entry to your client's MCP config by hand: { \"mcpServers\": { \"finance-toolkit\": { \"command\": \"uvx\", \"args\": [\"--from\", \"financetoolkit[mcp]\", \"financetoolkit-mcp\"], \"env\": { \"FINANCIAL_MODELING_PREP_API_KEY\": \"FINANCIAL_MODELING_PREP_KEY\" } } } } Config file locations per client are in the Local Clients cards, the .env file option and the optional FRED key in the API keys and environment variables card, and Claude Desktop users can skip all of this with the MCPB bundle."
      }
    },
    {
      "@type": "Question",
      "name": "Is my Financial Modeling Prep API key stored on the server?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "No. During the OAuth login your key is sealed inside a signed token that your MCP client holds and sends with every request; the server reads it for the duration of that request and never writes it to disk or a database. The full flow is on the Under the Hood page."
      }
    },
    {
      "@type": "Question",
      "name": "What data does the server cover?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Company data comes from Financial Modeling Prep: historical prices, financial statements, profiles, ESG scores and estimates for stocks and ETFs on exchanges worldwide, subject to your FMP plan. Macroeconomic data comes from the OECD and, optionally, FRED. The question on which tools the server exposes lists what is computed on top of that, and the Finance Toolkit documentation describes every metric and model in detail."
      }
    },
    {
      "@type": "Question",
      "name": "Which tools does the server expose?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "The 500+ Finance Toolkit methods are grouped into 22 categorical tools, each taking an indicator parameter that selects the exact metric, plus four search tools to navigate them: discovery, market_data, environment, performance, risk, options, econometrics, efficiency, liquidity, profitability, solvency, valuation, models, momentum, overlap, volatility, breadth, macroeconomics, government, jobs, rates, fixed_income, search_categories, search_by_category, search_metrics and search_instruments. The assistant chooses the tool and indicator from your plain-English question; equity tools accept tickers, macro tools accept countries, and all accept start_date, end_date and quarterly. Every tool returns data as standardized Markdown."
      }
    },
    {
      "@type": "Question",
      "name": "How is this different from the Financial Modeling Prep or Yahoo Finance MCP servers?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Those servers return raw data and leave the calculations to the language model. The Finance Toolkit MCP computes 500+ metrics, ratios, models and indicators with the open-source Finance Toolkit code, so the numbers are consistent, documented and reproducible regardless of which model you use. Why the Finance Toolkit MCP goes into this in more depth."
      }
    }
  ]
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "Finance Toolkit MCP Server",
  "alternateName": "FinanceToolkit MCP",
  "url": "https://www.jeroenbouma.com/projects/financetoolkit/mcp",
  "applicationCategory": "FinanceApplication",
  "operatingSystem": "Any",
  "softwareVersion": "2.2.0",
  "license": "https://github.com/JerBouma/FinanceToolkit/blob/main/LICENSE",
  "codeRepository": "https://github.com/JerBouma/FinanceToolkit",
  "installUrl": "https://financetoolkit.jeroenbouma.com/mcp",
  "offers": {
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "USD"
  },
  "author": {
    "@type": "Person",
    "name": "Jeroen Bouma",
    "url": "https://www.jeroenbouma.com"
  },
  "description": "Open-source Model Context Protocol server that gives Claude, ChatGPT, Cursor, VS Code and other AI assistants access to 500+ financial analysis methods: ratios, valuation models, technical indicators, risk metrics and macroeconomic data.",
  "featureList": [
    "500+ financial methods, models and indicators",
    "Hosted server, no installation required",
    "OAuth 2.1 with PKCE, API key never stored",
    "Macroeconomic data for 60+ countries",
    "Works with any MCP-compatible client"
  ]
}
</script>

<script>
document.addEventListener("DOMContentLoaded", function () {
  // Close all example chat cards except the one being revealed
  function closeOtherChatCards(keepOpen) {
    document.querySelectorAll("details.mcp-chat").forEach(function (d) {
      if (d !== keepOpen) d.open = false;
    });
  }

  // Open targeted <details> card when navigating to its anchor
  function revealHashTarget() {
    if (!location.hash) return;
    var el;
    try { el = document.querySelector(location.hash); } catch (e) { return; }
    if (!el) return;
    var details = el.closest("details");
    if (details) {
      if (details.classList.contains("mcp-chat")) closeOtherChatCards(details);
      details.open = true;
      setTimeout(function () { el.scrollIntoView({ block: "start" }); }, 50);
    }
  }

  // Capture-phase handler: opens the <details> BEFORE smooth-scroll fires,
  // so the element is visible when the browser tries to scroll to it.
  document.addEventListener("click", function (e) {
    var a = e.target.closest("a[href]");
    if (!a) return;
    var href = a.getAttribute("href");
    if (!href) return;
    var hash;
    if (href.charAt(0) === "#") {
      hash = href;
    } else {
      try {
        var url = new URL(href, location.href);
        if (url.pathname === location.pathname) hash = url.hash;
      } catch (err) {}
    }
    if (!hash) return;
    var target;
    try { target = document.querySelector(hash); } catch (err) { return; }
    if (!target) return;
    var details = target.closest("details");
    if (details) {
      if (details.classList.contains("mcp-chat")) closeOtherChatCards(details);
      details.open = true;
    }
  }, true);

  // The client cards in each installation section become horizontal tabs.
  // Without JavaScript they stay as the original collapsible cards.
  function activateTab(details) {
    var group = details.closest(".ft-tabs");
    if (!group) return;
    group.querySelectorAll(":scope > details").forEach(function (d) {
      var on = d === details;
      d.open = on;
      d.classList.toggle("is-active", on);
    });
    group.querySelectorAll(".ft-tabs__tab").forEach(function (b) {
      var on = b.dataset.target === details.id;
      b.classList.toggle("is-active", on);
      b.setAttribute("aria-selected", on ? "true" : "false");
    });
  }

  document.querySelectorAll(".ft-tabs").forEach(function (group) {
    var cards = group.querySelectorAll(":scope > details");
    if (!cards.length) return;
    var bar = document.createElement("div");
    bar.className = "ft-tabs__bar";
    bar.setAttribute("role", "tablist");
    cards.forEach(function (d) {
      var icon = d.querySelector("summary i");
      var b = document.createElement("button");
      b.type = "button";
      b.className = "ft-tabs__tab";
      b.setAttribute("role", "tab");
      b.dataset.target = d.id;
      b.innerHTML = (icon ? icon.outerHTML + " " : "") + d.querySelector("summary h3").textContent;
      b.addEventListener("click", function () { activateTab(d); });
      bar.appendChild(b);
    });
    group.insertBefore(bar, cards[0]);
    group.classList.add("is-tabbed");
    activateTab(cards[0]); // Claude Desktop is the default
  });

  // links to a client (e.g. #remote-chatgpt) select its tab
  var openDetails = revealHashTarget;
  revealHashTarget = function () {
    if (location.hash) {
      var el; try { el = document.querySelector(location.hash); } catch (e) { el = null; }
      var d = el && el.closest(".ft-tabs > details");
      if (d) activateTab(d);
    }
    openDetails();
  };
  document.addEventListener("click", function (e) {
    var a = e.target.closest("a[href*='#']");
    if (!a) return;
    var el; try { el = document.querySelector(new URL(a.href).hash); } catch (err) { return; }
    var d = el && el.closest(".ft-tabs > details");
    if (d) activateTab(d);
  });

  window.addEventListener("hashchange", revealHashTarget);
  revealHashTarget();

  // Reinforce autoplay: the HTML attribute is a hint browsers can suppress.
  // Explicit play() covers fresh navigations; canplay covers slow connections;
  // pageshow covers bfcache (back/forward); click is the last-resort fallback.
  (function () {
    var v = document.querySelector(".mcp-demo-video");
    if (!v) return;
    function tryPlay() { var p = v.play(); if (p && p.catch) p.catch(function () {}); }
    tryPlay();
    v.addEventListener("canplay", tryPlay);
    window.addEventListener("pageshow", function (e) { if (e.persisted) tryPlay(); });
    v.addEventListener("click", tryPlay);
  })();

});
</script>

{% include ft-charts-script.html %}
