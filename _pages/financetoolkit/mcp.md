---
permalink: /projects/financetoolkit/mcp
title: Finance Toolkit MCP Server
seo_title: "Finance Toolkit MCP Server: Financial Data & Stock Analysis for Claude, ChatGPT & Cursor"
seo_title_suffix: false
excerpt: "Connect Claude, ChatGPT, Cursor, VS Code or any other MCP client to the Finance Toolkit, hosted or on your own machine, and analyse stocks, financial statements, technical indicators and macro data in plain English."
description: "Open-source MCP server for stock analysis: 500+ financial ratios, valuation models, technical indicators and macro data in Claude, ChatGPT or Cursor."
classes: wide-sidebar
author_profile: false
layout: single
last_modified_at: 2026-09-11
redirect_from:
  - /mcp
  - /projects/financetoolkit/mcp-server
sidebar:
  nav: "financetoolkit-mcp"
image: /assets/images/projects/FinanceToolkitMCP.jpg
---

<div class="page-header-action notebook-viewer-actions"><a href="https://github.com/JerBouma/FinanceToolkit#mcp-server" target="_blank" rel="noopener"><i class="fab fa-github"></i> View on GitHub</a></div>

The Finance Toolkit MCP Server is an open-source [Model Context Protocol](https://modelcontextprotocol.io){:target="_blank"} (MCP) server that gives AI assistants such as Claude, ChatGPT, Cursor, GitHub Copilot and Gemini access to financial data and the 500+ analysis methods of the [Finance Toolkit](/projects/financetoolkit). Ask a question in plain English and the assistant fetches the data and runs the calculation for you: compare financial statements, screen on ratios, compute technical indicators or pull macroeconomic data, all with the same transparent, open-source formulas as the Python package.

The server comes in two flavours that expose exactly the same tools. The **remote server** is hosted at `https://financetoolkit.jeroenbouma.com/mcp` and needs nothing installed; the **local server** runs on your own machine through `uvx` and keeps your API key on your device. Both need a [Financial Modeling Prep API key](/fmp){:target="_blank"} for company data.

<div class="mcp-video-wrapper">
  <video class="mcp-demo-video" autoplay muted playsinline loop preload="metadata"
         poster="/assets/images/projects/FinanceToolkitMCP.jpg">
    <source src="/assets/video/mcp-demo.mp4" type="video/mp4">
  </video>
</div>

## Installation

Pick the [remote server](#remote-server) if you want to get going without installing anything, or the [local server](#local-clients) if you prefer to run the process yourself. Each section lists the same clients, so you can switch between the two at any time.

### Remote Server

Point your client at the URL below. On first use it opens an OAuth page asking for your [FMP API key](/fmp){:target="_blank"}; enter it once and the server takes it from there.

```
https://financetoolkit.jeroenbouma.com/mcp
```

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

### Local Clients

The local server runs on your own machine through `uvx` and works with every client that supports the `stdio` transport. The setup wizard finds your client's config file and writes the entry, including your API key, for you:

```bash
uvx --from "financetoolkit[mcp]" financetoolkit-mcp-setup
```

Prefer to do it by hand? Use the snippets below and replace `YOUR_API_KEY_HERE` with your [FMP API key](/fmp){:target="_blank"}. See [API keys and environment variables](#local-api-keys) for the `.env` file option and the optional FRED key.

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
        "env": { "FINANCIAL_MODELING_PREP_API_KEY": "YOUR_API_KEY_HERE" }
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
  claude mcp add --transport stdio finance-toolkit --env FINANCIAL_MODELING_PREP_API_KEY=YOUR_API_KEY_HERE -- uvx --from "financetoolkit[mcp]" financetoolkit-mcp
  ```

  Or edit `~/.claude.json` (create it if needed) and merge the entry inside `mcpServers`:

  ```json
  {
    "mcpServers": {
      "finance-toolkit": {
        "command": "uvx",
        "args": ["--from", "financetoolkit[mcp]", "financetoolkit-mcp"],
        "env": { "FINANCIAL_MODELING_PREP_API_KEY": "YOUR_API_KEY_HERE" }
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
  codex mcp add finance-toolkit --env FINANCIAL_MODELING_PREP_API_KEY=YOUR_API_KEY_HERE -- uvx --from "financetoolkit[mcp]" financetoolkit-mcp
  ```

  Or add the entry to `~/.codex/config.toml`:

  ```toml
  [mcp_servers.finance-toolkit]
  command = "uvx"
  args = ["--from", "financetoolkit[mcp]", "financetoolkit-mcp"]
  env = { FINANCIAL_MODELING_PREP_API_KEY = "YOUR_API_KEY_HERE" }
  ```

</details>

<details class="ft-details" id="local-vs-code" markdown="1">
  <summary><i class="fab fa-microsoft"></i> <h3>VS Code and GitHub Copilot</h3></summary>

  **Workspace** — create or edit `.vscode/mcp.json` in your workspace root. VS Code uses `servers` as the top-level key (not `mcpServers`):

  ```json
  {
    "servers": {
      "finance-toolkit": {
        "command": "uvx",
        "args": ["--from", "financetoolkit[mcp]", "financetoolkit-mcp"],
        "env": { "FINANCIAL_MODELING_PREP_API_KEY": "YOUR_API_KEY_HERE" }
      }
    }
  }
  ```

  **Global (all workspaces)** — add the same block under `"mcp"` in your user `settings.json`:

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
          "env": { "FINANCIAL_MODELING_PREP_API_KEY": "YOUR_API_KEY_HERE" }
        }
      }
    }
  }
  ```

</details>

<details class="ft-details" id="local-cursor" markdown="1">
  <summary><i class="fas fa-i-cursor"></i> <h3>Cursor</h3></summary>

  **Workspace** — create or edit `.cursor/mcp.json` in your workspace root:

  ```json
  {
    "mcpServers": {
      "finance-toolkit": {
        "command": "uvx",
        "args": ["--from", "financetoolkit[mcp]", "financetoolkit-mcp"],
        "env": { "FINANCIAL_MODELING_PREP_API_KEY": "YOUR_API_KEY_HERE" }
      }
    }
  }
  ```

  **Global (all projects)** — create or edit `~/.cursor/mcp.json`:

  ```json
  {
    "mcpServers": {
      "finance-toolkit": {
        "command": "uvx",
        "args": ["--from", "financetoolkit[mcp]", "financetoolkit-mcp"],
        "env": { "FINANCIAL_MODELING_PREP_API_KEY": "YOUR_API_KEY_HERE" }
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
        "env": { "FINANCIAL_MODELING_PREP_API_KEY": "YOUR_API_KEY_HERE" }
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
        "env": { "FINANCIAL_MODELING_PREP_API_KEY": "YOUR_API_KEY_HERE" }
      }
    }
  }
  ```

</details>

<details class="ft-details" id="local-api-keys" markdown="1">
  <summary><i class="fas fa-key"></i> <h3>API keys and environment variables</h3></summary>

  In every snippet `uvx` is the *command* and the rest are *args*. The `env` block takes either `FINANCIAL_MODELING_PREP_API_KEY` with the key inline, or `FINANCETOOLKIT_ENV_FILE` with the path to a `.env` file that contains `FINANCIAL_MODELING_PREP_API_KEY=your_key_here`; when both are present the inline key wins.

  A second key, `FRED_API_KEY`, is optional and free. It only unlocks a handful of US-only indicators without an OECD or FMP equivalent (nonfarm payrolls, initial jobless claims, the 30-year mortgage rate, the TIPS real yield curve and breakeven inflation expectations). The setup wizard picks it up automatically from your environment or `.env` file; [register for one here](https://fred.stlouisfed.org/docs/api/api_key.html){:target="_blank"}.

  `financetoolkit[mcp]` also installs the `econometrics` extra, so `statsmodels` and `linearmodels` come along and the `econometrics` tool works out of the box.

</details>

## Why the Finance Toolkit MCP

There are a growing number of MCP servers for financial data, from the official Financial Modeling Prep and Yahoo Finance servers to dozens of community wrappers. Most of them do one thing: expose raw API endpoints (a quote, an income statement, a list of prices) and leave the analysis to the language model. That is exactly where models are least reliable: an LLM asked to compute a return on invested capital or a Sharpe ratio from raw statements will happily make arithmetic and definitional mistakes, and two chats will rarely agree on the same number.

The Finance Toolkit MCP takes the opposite approach. It is a thin layer over the [Finance Toolkit](/projects/financetoolkit), a Python package with 500+ financial methods that has been downloaded well over a million times, and every number the assistant reports is computed by the same open-source code you can read on GitHub:

- **Analysis, not just data.** 150+ financial ratios, valuation and credit models (WACC, DuPont, Altman Z-Score, intrinsic value), performance and risk metrics (Sharpe, Sortino, alpha, beta, Value at Risk, GARCH), 30+ technical indicators, options pricing and Greeks, fixed income and a full econometrics toolbox.
- **Macro included.** GDP, inflation, unemployment, interest rates and government finances for 60+ countries from the OECD and FRED, next to the company data from Financial Modeling Prep.
- **Transparent and consistent.** Every formula is documented in the [Finance Toolkit documentation](/projects/financetoolkit/docs), so the same question returns the same number regardless of which model asks it.
- **Hosted and open source.** Connect to the hosted server in a minute, or run it locally with a single `uvx` command. The [source code](https://github.com/JerBouma/FinanceToolkit){:target="_blank"} is MIT-licensed.
- **Model-agnostic.** The 22 categorical tools are designed to be understood by small and large models alike, from GPT-5 mini to Claude Opus; the [example conversations](#example-conversations) below show both ends of that range.

If you only need a quote or a headline number, a raw data server is fine. If you want to ask *"which of these banks is the most solvent and why"* and get a defensible answer, this is the server built for it.

## Example Conversations

A core goal in building this MCP was to make it useful across the full spectrum of models: the server should return the right data regardless of which AI you use, and the depth of interpretation should scale naturally with the model's capability. The conversations below show that in practice.

<details class="mcp-chat" id="ex-apple-microsoft" markdown="1">
<summary class="mcp-chat__bar">
<span class="mcp-chat__avatar mcp-chat__avatar--user"><i class="fas fa-user"></i></span>
<h3 class="mcp-chat__q">Compare Apple with Microsoft, what company is the most profitable?</h3>
<span class="mcp-chat__model"><i class="fas fa-brain"></i>Claude Sonnet 4.6</span>
<span class="mcp-chat__toggle"><i class="fas fa-chevron-down"></i></span>
</summary>

<div class="mcp-chat__reply" markdown="1">
<div class="mcp-chat__reply-tag"><span class="mcp-chat__avatar mcp-chat__avatar--ai"><i class="fas fa-robot"></i></span>Finance Toolkit Analyst</div>

Across the five-year window from 2021 to 2025, Microsoft and Apple present genuinely different profitability profiles depending on the analytical lens applied, a nuance that institutional research rarely collapses into a single verdict. The data below, derived directly from the Finance Toolkit MCP server, covers gross margin, operating margin, and net profit margin across both companies from fiscal year 2021 through fiscal year 2025.

Microsoft commands a structurally superior margin stack at every level of the income statement. Its software and cloud-heavy revenue mix consistently produces gross margins in the 68–70% range, reflecting the near-zero marginal cost of licensing and Azure compute, while Apple's hardware-weighted mix constrains gross margins to the 42–47% band despite meaningful Services segment expansion.

| Metric | Company | 2021 | 2022 | 2023 | 2024 | 2025 |
|:--|:--|--:|--:|--:|--:|--:|
| Gross Margin | AAPL | 41.78% | 43.31% | 44.13% | 46.21% | 46.91% |
| Gross Margin | MSFT | 68.93% | 68.40% | 68.92% | 69.76% | 68.82% |
| Operating Margin | AAPL | 29.78% | 30.29% | 29.82% | 31.51% | 31.97% |
| Operating Margin | MSFT | 41.59% | 42.06% | 41.77% | 44.64% | 45.62% |
| Net Profit Margin | AAPL | 25.88% | 25.31% | 25.31% | 23.97% | 26.92% |
| Net Profit Margin | MSFT | 36.45% | 36.69% | 34.15% | 35.96% | 36.15% |

The margin story, however, is not the complete picture. When shifting from income-statement efficiency to capital deployment efficiency, Apple's financial engineering inverts the comparison dramatically. Apple carries a deliberately compressed equity base, the result of decades of aggressive share repurchases, which mechanically inflates its Return on Equity to levels that appear extraordinary, consistently exceeding 170% in recent years. The following table captures ROE, Return on Invested Capital, and Return on Assets for the same period.

| Metric | Company | 2022 | 2023 | 2024 | 2025 |
|:--|:--|--:|--:|--:|--:|
| Return on Equity | AAPL | 175.46% | 171.95% | 157.41% | 171.42% |
| Return on Equity | MSFT | 47.15% | 38.82% | 37.13% | 33.28% |
| Return on Invested Capital | AAPL | 59.90% | 60.68% | 60.19% | 70.38% |
| Return on Invested Capital | MSFT | 38.73% | 34.74% | 33.71% | 30.64% |
| Return on Assets | AAPL | 28.36% | 27.50% | 26.13% | 30.93% |
| Return on Assets | MSFT | 20.82% | 18.63% | 19.07% | 18.00% |

The verdict depends precisely on what one means by "most profitable." On a pure income statement basis (gross, operating, and net margins), **Microsoft is unambiguously the more profitable business**, generating roughly 22 percentage points more net income per dollar of revenue than Apple in fiscal year 2025 (36.15% vs. 26.92%). This structural advantage reflects Microsoft's software and cloud economics, where incremental revenue has near-zero marginal cost.

Apple, by contrast, leads on every capital efficiency metric: its ROIC of 70.38% in 2025 versus Microsoft's 30.64% indicates that Apple extracts significantly more economic value from each dollar of invested capital. Its ROA advantage (30.93% vs. 18.00%) is similarly consistent across the full sample. The ROE comparison is analytically distorted by Apple's balance sheet structure and is better set aside in favor of ROIC as the cleanest apples-to-apples measure.

For a more complete picture, the analysis could be extended into DuPont decomposition to isolate whether Apple's ROIC lead is driven by asset turnover, operational leverage, or financial leverage, all of which the Finance Toolkit supports natively.

</div>
</details>

<details class="mcp-chat" id="ex-bank-solvency" markdown="1">
<summary class="mcp-chat__bar">
<span class="mcp-chat__avatar mcp-chat__avatar--user"><i class="fas fa-user"></i></span>
<h3 class="mcp-chat__q">When looking at biggest banks in Europe, which one seems to be the most solvent?</h3>
<span class="mcp-chat__model"><i class="fas fa-brain"></i>Claude Sonnet 4.6</span>
<span class="mcp-chat__toggle"><i class="fas fa-chevron-down"></i></span>
</summary>

<div class="mcp-chat__reply" markdown="1">
<div class="mcp-chat__reply-tag"><span class="mcp-chat__avatar mcp-chat__avatar--ai"><i class="fas fa-robot"></i></span>Finance Toolkit Analyst</div>

Assessing solvency across Europe's nine largest listed banking groups (HSBC, BNP Paribas (BNPQY), Deutsche Bank (DB), Banco Santander (SAN), Barclays (BCS), UniCredit (UNCRY), Société Générale (SCGLY), ING, and Intesa Sanpaolo (ISNPY)) requires examining leverage in multiple dimensions simultaneously. Because banks operate with inherently high financial leverage by design, the equity multiplier and debt-to-assets ratio are the most discriminating solvency signals, with the debt service coverage ratio providing a cash-flow-based cross-check. Taken together, the data point to **UniCredit** and **Intesa Sanpaolo** as the standout names for solvency quality within this cohort.

The debt-to-equity ratio captures the proportion of debt relative to shareholders' equity. A lower reading indicates a more conservative capital structure relative to the equity cushion available to absorb losses. The six-year progression below reveals a clear dispersion across the group, with BNP Paribas and Santander consistently carrying the heaviest debt loads relative to equity, while HSBC and Intesa Sanpaolo trend toward the lower end.

| Ticker | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|:-------|-----:|-----:|-----:|-----:|-----:|-----:|
| ISNPY  | 1.62 | 1.58 | 1.61 | 2.22 | 2.24 | 2.13 |
| HSBC   | 1.85 | 1.91 | 1.10 | 2.22 | 1.26 | 2.68 |
| UNCRY  | 2.24 | 2.01 | 1.82 | 1.91 | 1.95 | 2.57 |
| BCS    | 2.15 | 2.38 | 2.65 | 2.46 | 2.56 | 2.81 |
| DB     | 3.28 | 2.30 | 2.70 | 1.93 | 1.91 | 3.18 |
| SCGLY  | 2.31 | 2.13 | 2.11 | 2.38 | 2.30 | 4.12 |
| ING    | 1.42 | 2.12 | 2.37 | 2.87 | 3.34 | 3.32 |
| SAN    | 3.53 | 3.45 | 4.36 | 2.98 | 4.50 | 4.40 |
| BNPQY  | 6.40 | 6.34 | 2.56 | 5.23 | 5.43 | 6.22 |

The equity multiplier, total assets divided by equity, provides a balance-sheet-wide view of financial leverage and is a core input into DuPont decomposition. A lower multiplier implies a thicker equity buffer relative to the entire asset base. The 2025 cross-section is particularly telling: UniCredit stands at just 12.6x, the lowest among all nine peers, followed closely by Intesa Sanpaolo at 14.5x and Santander at 16.8x. By contrast, BNP Paribas (20.7x), Société Générale (21.0x), Barclays (20.3x), and ING (20.3x) are meaningfully more leveraged. Importantly, UniCredit's multiplier has compressed steadily from 15.1x in 2021 to 12.6x in 2025, signalling a deliberate and sustained de-leveraging trajectory.

| Ticker | 2021 | 2022 | 2023 | 2024 | 2025 |
|:-------|-----:|-----:|-----:|-----:|-----:|
| UNCRY  | 15.10 | 14.09 | 12.85 | 12.34 | 12.64 |
| ISNPY  | 15.86 | 16.33 | 15.46 | 14.66 | 14.50 |
| SAN    | 16.48 | 17.09 | 17.49 | 17.18 | 16.82 |
| HSBC   | 14.43 | 15.11 | 15.89 | 15.73 | 16.57 |
| DB     | 20.38 | 18.97 | 17.99 | 17.50 | 17.69 |
| ING    | 17.11 | 18.24 | 18.94 | 19.27 | 20.31 |
| BCS    | 19.97 | 20.74 | 21.18 | 20.75 | 20.30 |
| BNPQY  | 23.21 | 23.24 | 21.55 | 20.14 | 20.67 |
| SCGLY  | 21.10 | 20.46 | 20.33 | 20.08 | 20.96 |

The debt-to-assets ratio corroborates this ranking. HSBC (0.153), Deutsche Bank (0.178), and Intesa Sanpaolo (0.145) hold the smallest debt loads as a share of the total balance sheet in 2025, while BNP Paribas (0.294) and Santander (0.266) are again the outliers on the high end. The debt service coverage ratio provides the critical cash-flow validation: UniCredit (0.228) and Intesa Sanpaolo (0.181) post the highest readings in 2025, meaning their operating earnings are most comfortably covering their debt obligations, a distinction that separates balance-sheet strength from earnings-backed solvency capacity.

| Ticker | D/A 2025 | Equity Mult 2025 | DSCR 2025 |
|:-------|----------:|-----------------:|----------:|
| UNCRY  | 0.201 | 12.64 | 0.228 |
| ISNPY  | 0.145 | 14.50 | 0.181 |
| HSBC   | 0.153 | 16.57 | 0.120 |
| DB     | 0.178 | 17.69 | 0.010 |
| BCS    | 0.142 | 20.30 | 0.013 |
| SCGLY  | 0.186 | 20.96 | 0.012 |
| ING    | 0.161 | 20.31 | 0.011 |
| SAN    | 0.266 | 16.82 | 0.014 |
| BNPQY  | 0.294 | 20.67 | 0.013 |

Synthesizing across all three dimensions, **UniCredit (UNCRY)** emerges as the most solvent major European bank. Its equity multiplier of 12.6x is the lowest in the peer group by a meaningful margin, its trend has been consistently improving over six years, and its debt service coverage ratio of 0.228 is the highest in the cohort, confirming that the balance-sheet strength is underpinned by genuine earnings power rather than accounting structure alone. **Intesa Sanpaolo (ISNPY)** is the clear runner-up, posting the second-best equity multiplier and second-best DSCR. At the other end of the spectrum, BNP Paribas is the most leveraged name across nearly every metric, and Société Générale's equity multiplier spiked to 21.0x in 2025, flagging elevated structural leverage risk in that institution.

Logical extensions of this analysis within the Finance Toolkit ecosystem would include examining capital allocation quality via return on equity and return on invested capital for these same banks, running a rolling volatility and maximum drawdown comparison to understand how solvency strength translates into price resilience, or stress-testing via the Altman Z-Score model where data coverage permits.

</div>
</details>

<details class="mcp-chat" id="ex-semiconductor-overbought" markdown="1">
<summary class="mcp-chat__bar">
<span class="mcp-chat__avatar mcp-chat__avatar--user"><i class="fas fa-user"></i></span>
<h3 class="mcp-chat__q">Tell me something about the Semiconductor industry, is it overbought?</h3>
<span class="mcp-chat__model"><i class="fas fa-brain"></i>Claude Sonnet 4.6</span>
<span class="mcp-chat__toggle"><i class="fas fa-chevron-down"></i></span>
</summary>

<div class="mcp-chat__reply" markdown="1">
<div class="mcp-chat__reply-tag"><span class="mcp-chat__avatar mcp-chat__avatar--ai"><i class="fas fa-robot"></i></span>Finance Toolkit Analyst</div>

The following analysis covers eight representative semiconductor names spanning the full value chain: fabless designers (NVDA, AMD, QCOM), integrated device manufacturers (INTC, MU), a pure-play foundry (TSM), a diversified chip infrastructure leader (AVGO), and the European lithography monopoly (ASML), using RSI momentum, trailing P/E multiples, and risk-adjusted Sharpe ratios sourced entirely from the Finance Toolkit MCP server.

**Momentum: The Sector Was Overbought in Late April and Early May and Has Since Cooled**

The most telling technical story of 2026 is a sharp overbought surge that peaked between late April and mid-May and has since largely normalised as of the June 4 close. The table below presents trailing 14-day RSI readings (Wilder smoothing) across the cohort for the last ten trading sessions. Readings above 70 flag overbought conditions; readings below 30 indicate oversold pressure.

| Date       | NVDA  | AMD   | INTC  | QCOM  | AVGO  | TSM   | MU    | ASML  | SPY (Benchmark) |
|:-----------|------:|------:|------:|------:|------:|------:|------:|------:|----------------:|
| 2026-05-21 | 57.76 | 69.90 | 67.42 | 64.93 | 53.30 | 56.91 | 66.92 | 59.44 | 67.29 |
| 2026-05-22 | 53.71 | **72.59** | 68.18 | **71.75** | 53.09 | 55.47 | 65.07 | 62.23 | 68.86 |
| 2026-05-26 | 53.26 | **77.07** | **70.23** | **74.09** | 56.46 | 58.79 | **74.86** | 62.13 | **71.36** |
| 2026-05-27 | 51.04 | **74.08** | 67.99 | 65.63 | 56.38 | 62.79 | **76.45** | 58.26 | **71.20** |
| 2026-05-28 | 52.60 | **76.71** | 66.83 | 68.14 | 58.45 | 63.56 | **75.68** | 58.89 | **73.28** |
| 2026-05-29 | 49.41 | **75.98** | 59.19 | 69.99 | 65.92 | 59.53 | **78.01** | 59.48 | **74.19** |
| 2026-06-01 | 60.39 | **73.70** | 53.51 | 59.41 | 69.75 | 65.80 | **80.73** | 60.85 | **75.18** |
| 2026-06-02 | 58.79 | **75.23** | 52.10 | 62.68 | **74.75** | 69.11 | **81.80** | 66.73 | **75.69** |
| 2026-06-03 | 51.14 | **77.78** | 56.33 | 65.03 | **73.34** | 63.15 | **82.37** | 68.14 | 67.97 |
| 2026-06-04 | 54.44 | **70.57** | 55.31 | 62.03 | 48.08 | 65.77 | 69.66 | **70.16** | 69.74 |

The data paints a diverging picture within the sector. AMD and MU have been the momentum leaders: AMD has printed an RSI above 70 in every one of the last nine sessions and MU pushed as high as 82 on June 3 before cooling to 69.66 on the last close. AVGO is the clearest reversal: it climbed from the low 50s to 74.75 on June 2 and then collapsed to 48.08 in just two sessions, possibly reflecting rotation out of AI-infrastructure adjacent names. NVDA, by contrast, has spent the entire window in neutral territory between 49 and 60, and INTC has faded from a 70 reading on May 26 to 55. The broader SPY benchmark sits at 69.74, itself just below the overbought line after six consecutive sessions above 70 through June 2, meaning much of the sector's momentum is a broad-market phenomenon rather than a semiconductor-specific one. Notably, the cohort touched genuinely overbought readings of 85–89 on AMD (April 24), INTC (May 1), QCOM and MU (May 11) earlier in the spring, coinciding with the US-China trade truce news and renewed AI capex guidance from hyperscalers. That wave has largely receded.

**Valuation: Multiples Remain Structurally Elevated for AI-Exposed Names**

The overbought question cannot be answered through momentum alone: RSI describes the speed of price change, not whether the underlying business justifies the price. The following table presents trailing annual P/E ratios for the cohort from 2021 through 2026 (2026 where available).

| Ticker | 2021  | 2022  | 2023   | 2024   | 2025    | 2026  |
|:-------|------:|------:|-------:|-------:|--------:|------:|
| NVDA   | 170.5 | 38.0  | 284.3  | 112.5  | 63.5    | 44.6  |
| AMD    | 55.9  | 77.1  | 280.5  | 120.5  | 80.8    |       |
| AVGO   | 44.3  | 21.1  | 33.8   | 187.9  | 72.6    |       |
| ASML   | 49.0  | 36.3  | 34.4   | 34.6   | 36.9    |       |
| MU     | 18.1  | 6.5   | —      | 120.9  | 37.6    |       |
| QCOM   | 23.2  | 9.7   | 22.5   | 17.1   | 34.1    |       |
| TSM    | 29.1  | 11.9  | 19.4   | 29.0   | 28.4    |       |
| INTC   | 10.6  | 13.6  | 125.3  | —      | —       |       |

NVDA's P/E compression from its stratospheric 284x in 2023 to 44.6x on a current-year basis is meaningful progress, but at 44x it still prices in enormous earnings growth expectations that leave little room for execution disappointment. AMD at 80.8x and AVGO at 72.6x for 2025 are similarly demanding. In contrast, TSM trades at a comparatively modest 28x, QCOM at 34x, and ASML at 37x, multiples that, while not cheap, are more defensible given their structural moat positions in leading-edge foundry, mobile/auto connectivity, and EUV lithography respectively. INTC remains the sector's distressed outlier, posting deeply negative earnings in 2024 and 2025 as its restructuring and process-technology catch-up remains unresolved.

**Risk-Adjusted Returns: 2022 Was the Only Losing Year, and 2026 Is Off to a Strong Start**

Sharpe ratios on an annual basis show how much excess return (versus the 10-year Treasury yield) each name delivered per unit of volatility. The Finance Toolkit reports these on a per-observation basis, i.e. the mean of the daily excess returns within each year divided by their standard deviation, so the figures are not annualised (multiply by roughly 15.9, the square root of 252, to compare against published annual Sharpe ratios). The table below covers each name since 2021, with 2026 running through June 4.

| Year | NVDA   | AMD    | INTC   | QCOM   | AVGO   | TSM    | MU     | ASML   | SPY    |
|:-----|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|
| 2021 | 0.126  | 0.078  | 0.019  | 0.045  | 0.105  | 0.029  | 0.045  | 0.092  | 0.120  |
| 2022 | -0.053 | -0.066 | -0.096 | -0.055 | -0.017 | -0.064 | -0.071 | -0.032 | -0.052 |
| 2023 | 0.170  | 0.121  | 0.116  | 0.063  | 0.144  | 0.074  | 0.100  | 0.071  | 0.098  |
| 2024 | 0.131  | -0.017 | -0.099 | 0.018  | 0.099  | 0.108  | 0.010  | -0.003 | 0.095  |
| 2025 | 0.052  | 0.074  | 0.076  | 0.027  | 0.061  | 0.075  | 0.140  | 0.076  | 0.046  |
| 2026 | 0.069  | 0.205  | 0.217  | 0.104  | 0.072  | 0.149  | 0.255  | 0.166  | 0.106  |

Two patterns stand out. First, 2022 is the only year in which every name in the cohort posted a negative Sharpe ratio, the rate-shock year in which the sector sold off alongside the broader market. Second, the leadership has rotated: NVDA and AVGO were the standout risk-adjusted performers in 2023 and 2024, but in 2026 year-to-date MU (0.255), INTC (0.217) and AMD (0.205) lead by a wide margin while NVDA (0.069) has dropped to the bottom of the group, below the SPY benchmark (0.106). This is consistent with the RSI picture above: the momentum has migrated from the AI-accelerator leader toward memory, foundry and the turnaround names. AVGO's 2026 reading of 0.072 also confirms that its early-June reversal has eroded most of its risk-adjusted lead for the year.

**Synthesis: Pockets of Overbought Momentum, Not a Sector-Wide Extreme**

The semiconductor sector is not uniformly overbought as of June 4, 2026. The data reveals a sector that has already corrected from a genuine late-April to mid-May overbought peak and now shows selective, rather than broad, momentum excess. AMD and ASML still sit just above the 70 line and MU only dipped below it on the last session, so those three warrant caution on a pure momentum basis. AVGO has unwound its surge most aggressively, NVDA has spent the entire window in neutral territory, and INTC, QCOM and TSM are elevated but well below the overbought threshold. Valuations remain the persistent structural concern: NVDA, AMD, and AVGO carry multiples that require continued AI-driven earnings acceleration to justify, while ASML, QCOM, and TSM offer more moderate entry points from a fundamental standpoint. For investors monitoring the sector, the logical next steps within the Finance Toolkit ecosystem would include drilling into individual-name volatility profiles using GARCH forecasts, running rolling Sharpe analyses to capture momentum-regime shifts, or examining sector-level factor exposures through Fama-French decomposition to isolate whether excess returns are attributable to market beta, size, or value factors.

</div>
</details>

The examples above use **Claude Sonnet 4.6**, which layers substantial qualitative reasoning on top of the raw numbers. The examples below use **GPT-5 mini**, a lighter, faster model that returns clean, structured data without the added narrative. Both work well with the Finance Toolkit MCP; the depth of interpretation scales with the model you choose.

<details class="mcp-chat" id="ex-alibaba-amazon" markdown="1">
<summary class="mcp-chat__bar">
<span class="mcp-chat__avatar mcp-chat__avatar--user"><i class="fas fa-user"></i></span>
<h3 class="mcp-chat__q">Compare the financial performance of Alibaba and Amazon over the last 5 years</h3>
<span class="mcp-chat__model"><i class="fas fa-microchip"></i>GPT-5 mini</span>
<span class="mcp-chat__toggle"><i class="fas fa-chevron-down"></i></span>
</summary>

<div class="mcp-chat__reply" markdown="1">
<div class="mcp-chat__reply-tag"><span class="mcp-chat__avatar mcp-chat__avatar--ai"><i class="fas fa-robot"></i></span>Finance Toolkit Analyst</div>

Over the last five years Amazon has outgrown Alibaba in absolute scale and delivered larger revenue and market‑cap expansion, while Alibaba showed steadier margin improvement and a sharp profitability rebound by 2025.  

Below are the core yearly figures (2021–2025) used to compare scale and bottom‑line performance; revenue, net income and market capitalization are in USD (Alibaba's CNY statements converted at the prevailing exchange rate) and rounded to one decimal where helpful. Alibaba's fiscal year ends in March, so its "2025" column covers April 2024 to March 2025.

Looking at revenue and net income, Amazon is much larger in absolute revenue and produced a large net‑income rebound after 2022.

| Year | AMZN Revenue (bn) | BABA Revenue (bn) | AMZN Net Income (bn) | BABA Net Income (bn) |
|:-----|------------------:|------------------:|---------------------:|---------------------:|
| 2021 | 469.8             | 112.5             | 33.4                 | 23.6                 |
| 2022 | 514.0             | 122.5             | -2.7                 | 8.9                  |
| 2023 | 574.8             | 122.2             | 30.4                 | 10.2                 |
| 2024 | 638.0             | 128.9             | 59.2                 | 10.9                 |
| 2025 | 716.9             | 142.4             | 77.8                 | 18.5                 |

When we compare per‑share and profitability metrics, both companies recovered after mid‑period weakness but Amazon delivered higher EPS and stronger returns on capital in recent years.

Looking at EPS (annual). Note that Alibaba reports earnings per share in CNY and per American Depositary Share (one ADS equals eight ordinary shares), so the two columns are not directly comparable in level, only in trend:

| Year | AMZN EPS (USD) | BABA EPS (CNY per ADS) |
|:-----|---------------:|-----------------------:|
| 2021 | 3.24     | 55.60    |
| 2022 | -0.27    | 22.96    |
| 2023 | 2.90     | 27.68    |
| 2024 | 5.53     | 31.60    |
| 2025 | 7.17     | 55.12    |

Return on equity (ROE) shows Amazon moving to materially higher ROE from 2023 onward; Alibaba improved but stayed below Amazon’s peak ROE. ROE and ROIC are computed on average balances, so the first year of the window is omitted.

| Year | AMZN ROE | BABA ROE |
|:-----|---------:|---------:|
| 2022 | -0.0191 | 0.0546  |
| 2023 | 0.1749  | 0.0650  |
| 2024 | 0.2429  | 0.0702  |
| 2025 | 0.2229  | 0.1199  |

Return on invested capital (ROIC) follows the same pattern: Amazon shows larger ROIC from 2023 while Alibaba’s ROIC notably improved by 2025.

| Year | AMZN ROIC | BABA ROIC |
|:-----|----------:|----------:|
| 2022 | -0.0101  | 0.0468   |
| 2023 | 0.0976   | 0.0556   |
| 2024 | 0.1571   | 0.0730   |
| 2025 | 0.1584   | 0.1219   |

Market capitalization (year‑end) shows Amazon’s much larger market value throughout the period.

| Year | AMZN Market Cap (bn) | BABA Market Cap (bn) |
|:-----|---------------------:|---------------------:|
| 2021 | 1717.2               | 326.4                |
| 2022 | 855.9                | 239.9                |
| 2023 | 1594.2               | 204.6                |
| 2024 | 2352.1               | 215.8                |
| 2025 | 2499.1               | 354.0                |

Amazon is the dominant scale and value creator by revenue and market cap and converted that scale into rising ROE/ROIC and large net income gains after 2022, while Alibaba delivered steadier margin improvement and a notable profitability recovery by 2025 but remained materially smaller in absolute terms.

</div>
</details>

<details class="mcp-chat" id="ex-unemployment" markdown="1">
<summary class="mcp-chat__bar">
<span class="mcp-chat__avatar mcp-chat__avatar--user"><i class="fas fa-user"></i></span>
<h3 class="mcp-chat__q">Show me the unemployment rate for the United States and Germany since 2010.</h3>
<span class="mcp-chat__model"><i class="fas fa-microchip"></i>GPT-5 mini</span>
<span class="mcp-chat__toggle"><i class="fas fa-chevron-down"></i></span>
</summary>

<div class="mcp-chat__reply" markdown="1">
<div class="mcp-chat__reply-tag"><span class="mcp-chat__avatar mcp-chat__avatar--ai"><i class="fas fa-robot"></i></span>Finance Toolkit Analyst</div>

Since 2010 Germany's unemployment rate fell from about 6.6% to roughly 3.0% and has stayed near that level, while the United States fell from about 9.6% in 2010, spiked in 2020, and is averaging roughly 4.3% so far in 2026. The table below shows the annual average unemployment rates (percent, OECD harmonised definition) for the United States and Germany from 2010 through 2026, where the 2026 figure is the year-to-date average.

|      |   Germany |   United States |
|:-----|----------:|----------------:|
| 2010 |     6.575 |           9.608 |
| 2011 |     5.517 |           8.933 |
| 2012 |     5.083 |           8.075 |
| 2013 |     4.95  |           7.358 |
| 2014 |     4.708 |           6.158 |
| 2015 |     4.367 |           5.275 |
| 2016 |     3.908 |           4.875 |
| 2017 |     3.567 |           4.358 |
| 2018 |     3.208 |           3.892 |
| 2019 |     2.975 |           3.675 |
| 2020 |     3.625 |           8.092 |
| 2021 |     3.575 |           5.35  |
| 2022 |     3.067 |           3.633 |
| 2023 |     3.025 |           3.625 |
| 2024 |     3.352 |           4.081 |
| 2025 |     3.152 |           4.369 |
| 2026 (YTD) |     3.061 |           4.307 |

</div>
</details>


<details class="mcp-chat" id="ex-semiconductor-esg" markdown="1">
<summary class="mcp-chat__bar">
<span class="mcp-chat__avatar mcp-chat__avatar--user"><i class="fas fa-user"></i></span>
<h3 class="mcp-chat__q">When looking at the Semiconductor industry, what company seems to be the most sustainable?</h3>
<span class="mcp-chat__model"><i class="fas fa-microchip"></i>GPT-5 mini</span>
<span class="mcp-chat__toggle"><i class="fas fa-chevron-down"></i></span>
</summary>

<div class="mcp-chat__reply" markdown="1">
<div class="mcp-chat__reply-tag"><span class="mcp-chat__avatar mcp-chat__avatar--ai"><i class="fas fa-robot"></i></span>Finance Toolkit Analyst</div>

I'll fetch ESG scores for a set of leading semiconductor companies (NVDA, AMD, INTC, ASML, TSM, TXN, QCOM, AVGO, MRVL, ON) to identify the most sustainable firm.

ASML clearly stands out as the most sustainable company in this semiconductor sample, scoring far higher on the Finance Toolkit ESG metric than its peers in 2026.

The latest (2026) ESG scores for the sampled semiconductor companies are shown below.

| Ticker |   ESG Score (2026) |
|:-------|-------------------:|
| ASML   |             95.65  |
| TSM    |             83.13  |
| INTC   |             80.08  |
| TXN    |             78.38  |
| AMD    |             78.02  |
| ON     |             68.06  |
| NVDA   |             67.99  |
| MRVL   |             67.59  |
| QCOM   |             67.36  |
| AVGO   |             62.56  |

ASML’s lead is supported by very strong component scores in 2026, which indicate balanced performance across environmental, social, and governance factors.

| Score Type       | 2026 |
|:-----------------|-----:|
| Environmental    | 95.84 |
| Social           | 98.92 |
| Governance       | 92.20 |

</div>
</details>

## Available Tools

The server groups the 500+ Finance Toolkit methods into 22 categorical master tools, each taking an `indicator` parameter that selects the exact metric, e.g. `valuation` with `indicator='get_price_to_earnings_ratio'`. You never set this by hand: the assistant picks the right tool and indicator from your plain-English question. Equity tools accept `tickers` (e.g. `'AAPL,MSFT'`), macro tools accept `countries` (e.g. `'United States,Germany'`), and all accept `start_date`, `end_date` and `quarterly`.

To explore what's available, ask the assistant to run the built-in `search_categories`, `search_by_category` or `search_metrics` tools, or launch the interactive inspector with `uvx --from "financetoolkit[mcp]" financetoolkit-mcp-inspector`. The full catalogue (every tool returns data as standardised Markdown) is grouped below. Each master tool wraps dozens of underlying Finance Toolkit functions; to understand **every** metric, model and parameter that can ultimately be reached through these tools, see the full Finance Toolkit documentation.

[Browse the Finance Toolkit Documentation](/projects/financetoolkit/docs){: .btn .btn--info .btn--large}

<details class="ft-details" markdown="1">
  <summary><h3>Fundamentals</h3></summary>

  These tools provide a wide range of fundamental data points and financial metrics for companies, including historical prices, financial statements, company profiles, ESG scores, and performance/risk metrics.

| Tool | Description |
|:---|:---|
| `discovery` | Stock and ETF screener, gainers/losers, most active |
| `market_data` | Historical prices, financial statements, company profile, real-time quote |
| `environment` | ESG scores, carbon footprint, renewable energy usage |
| `performance` | Sharpe ratio, Sortino ratio, Alpha, Beta, CAPM, Fama-French, Carhart, market timing |
| `risk` | Value at Risk, CVaR, GARCH/EGARCH/GJR-GARCH, max drawdown, copulas, realized volatility |
| `options` | Black-Scholes pricing, binomial tree, Greeks, implied volatility, exotic options |

</details>

<details class="ft-details" markdown="1">
  <summary><h3>Econometrics</h3></summary>

  This tool runs statistical tests and estimators on price and return series, for diagnosing the properties of a series or estimating causal effects rather than reading off a pre-computed metric.

| Tool | Description |
|:---|:---|
| `econometrics` | Regression (OLS/WLS/GLS, logit, probit, quantile, Fama-MacBeth), panel data (fixed/random effects, Hausman), causal inference (IV-2SLS, difference-in-differences, regression discontinuity, propensity score matching, synthetic control), unit root and cointegration tests, Granger causality, diagnostics, ARIMA/VAR/VECM forecasting and event studies |

</details>

<details class="ft-details" markdown="1">
  <summary><h3>Financial Ratios and Models</h3></summary>

  These tools compute a wide range of financial ratios and models that are commonly used for fundamental analysis, valuation, and credit risk assessment. They can be applied to any company with available financial statement data.

| Tool | Description |
|:---|:---|
| `efficiency` | Asset/inventory turnover, days of sales outstanding, cash conversion cycle |
| `liquidity` | Current ratio, quick ratio, cash ratio, working capital |
| `profitability` | Gross/net/operating margin, ROE, ROA, ROIC, ROCE |
| `solvency` | Debt-to-equity, interest coverage, net debt to EBITDA |
| `valuation` | P/E, EPS, EV/EBITDA, P/B, P/S, dividend yield, free cash flow yield |
| `models` | WACC, DuPont analysis, Altman Z-Score, Piotroski F-Score, intrinsic value, FCFF/FCFE, Tobin's Q, five bankruptcy scores |

</details>

<details class="ft-details" markdown="1">
  <summary><h3>Technical Indicators</h3></summary>

  These tools compute a wide range of technical indicators used for momentum, trend, volatility, and breadth analysis. They can be applied to any instrument with historical price data.

| Tool | Description |
|:---|:---|
| `momentum` | RSI, MACD, Stochastic oscillator, Williams %R, Aroon |
| `overlap` | SMA, EMA, Bollinger Bands, Keltner Channels |
| `volatility` | Average True Range, True Range, volatility series |
| `breadth` | McClellan oscillator, OBV, Advance/Decline line, Chaikin |

</details>

<details class="ft-details" markdown="1">
  <summary><h3>Macro Economics and Fixed Income</h3></summary>

  These tools provide insights into the broader economic environment and fixed income valuations, helping you understand the macro conditions that can impact financial markets.

| Tool | Description |
|:---|:---|
| `macroeconomics` | GDP, CPI, inflation, trade balances, investment, consumption |
| `government` | Government debt, deficit, expenditure, revenue, tax rates |
| `jobs` | Unemployment, population, poverty, income inequality |
| `rates` | Central bank rates, government bond yields, EURIBOR, US Treasury par yield curve, TIPS real yields |
| `fixed_income` | Bond duration, present value, YTM, derivative pricing, par/forward rates, Z-spread, key rate duration |

</details>

<details class="ft-details" markdown="1">
  <summary><h3>Utility Tools</h3></summary>

These tools help you navigate the available functionality before making any data call.

| Tool | Description |
|:---|:---|
| `search_categories` | Lists all registered categories and the number of tools each contains |
| `search_by_category` | Lists every metric available within a given category |
| `search_metrics` | Fuzzy keyword search across all metrics with typo tolerance |
| `search_instruments` | Look up ticker symbols by company name, ISIN, CIK, CUSIP, or symbol |

</details>

## FAQ

The questions that come up most often about the server, its data sources and how it compares to other financial MCP servers. Anything missing? Open an issue on [GitHub](https://github.com/JerBouma/FinanceToolkit/issues){:target="_blank"}.

<details class="ft-details" markdown="1">
  <summary><h3>Is the Finance Toolkit MCP server free?</h3></summary>

  Yes. The server and the Finance Toolkit it is built on are open source (MIT license) and the hosted server at financetoolkit.jeroenbouma.com is free to use. The only thing you need is a Financial Modeling Prep API key; FMP offers a free plan (250 requests a day, 5 years of history, US-listed companies) that is enough to try the server, and paid plans for full history, all exchanges and higher request limits.

</details>

<details class="ft-details" markdown="1">
  <summary><h3>Which AI assistants and clients does it work with?</h3></summary>

  Any client that supports the Model Context Protocol: Claude Desktop, claude.ai, Claude Code, ChatGPT (Developer mode), Codex CLI, Cursor, VS Code with GitHub Copilot, Windsurf, Gemini CLI and many more. The hosted server uses the standard streamable HTTP transport with OAuth 2.1, and the local server uses stdio.

</details>

<details class="ft-details" markdown="1">
  <summary><h3>Do I need to install Python?</h3></summary>

  No. The hosted server requires no installation at all: add the URL to your client and enter your FMP API key once. Python (or rather uv) is only needed if you prefer to run the server locally with uvx.

</details>

<details class="ft-details" markdown="1">
  <summary><h3>Is my Financial Modeling Prep API key stored on the server?</h3></summary>

  No. During the OAuth login your key is sealed inside a signed token that your MCP client holds and sends with every request. The server reads the key from that token for the duration of a single request and never writes it to disk or to a database. The full flow is documented on the architecture page.

</details>

<details class="ft-details" markdown="1">
  <summary><h3>What data does the server cover?</h3></summary>

  Company data comes from Financial Modeling Prep: historical prices, financial statements, profiles, ESG scores and estimates for stocks and ETFs on exchanges worldwide, subject to your FMP plan. Macroeconomic data (GDP, inflation, unemployment, interest rates, government finances) comes from the OECD and, optionally, FRED, and needs no additional key except for a handful of US-only FRED series.

</details>

<details class="ft-details" markdown="1">
  <summary><h3>How is this different from the Financial Modeling Prep or Yahoo Finance MCP servers?</h3></summary>

  Those servers return raw data and leave the calculations to the language model. The Finance Toolkit MCP computes 500+ metrics, ratios, models and indicators with the open-source Finance Toolkit code, so the numbers are consistent, documented and reproducible regardless of which model you use.

</details>

<details class="ft-details" markdown="1">
  <summary><h3>Can I run the server locally?</h3></summary>

  Yes. Run uvx --from "financetoolkit[mcp]" financetoolkit-mcp-setup to configure Claude Desktop, Claude Code, Cursor, VS Code, Gemini CLI or Windsurf automatically, or add the uvx command to your client's MCP configuration by hand. Claude Desktop users can also install the one-click MCPB bundle.

</details>

<details class="ft-details" markdown="1">
  <summary><h3>Does the server work with ChatGPT?</h3></summary>

  Yes. ChatGPT supports custom MCP servers through Developer mode on its paid plans: create a connector with the server URL, choose OAuth authentication and enter your FMP API key once.

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
        "text": "Yes. The server and the Finance Toolkit it is built on are open source (MIT license) and the hosted server at financetoolkit.jeroenbouma.com is free to use. The only thing you need is a Financial Modeling Prep API key; FMP offers a free plan (250 requests a day, 5 years of history, US-listed companies) that is enough to try the server, and paid plans for full history, all exchanges and higher request limits."
      }
    },
    {
      "@type": "Question",
      "name": "Which AI assistants and clients does it work with?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Any client that supports the Model Context Protocol: Claude Desktop, claude.ai, Claude Code, ChatGPT (Developer mode), Codex CLI, Cursor, VS Code with GitHub Copilot, Windsurf, Gemini CLI and many more. The hosted server uses the standard streamable HTTP transport with OAuth 2.1, and the local server uses stdio."
      }
    },
    {
      "@type": "Question",
      "name": "Do I need to install Python?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "No. The hosted server requires no installation at all: add the URL to your client and enter your FMP API key once. Python (or rather uv) is only needed if you prefer to run the server locally with uvx."
      }
    },
    {
      "@type": "Question",
      "name": "Is my Financial Modeling Prep API key stored on the server?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "No. During the OAuth login your key is sealed inside a signed token that your MCP client holds and sends with every request. The server reads the key from that token for the duration of a single request and never writes it to disk or to a database. The full flow is documented on the architecture page."
      }
    },
    {
      "@type": "Question",
      "name": "What data does the server cover?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Company data comes from Financial Modeling Prep: historical prices, financial statements, profiles, ESG scores and estimates for stocks and ETFs on exchanges worldwide, subject to your FMP plan. Macroeconomic data (GDP, inflation, unemployment, interest rates, government finances) comes from the OECD and, optionally, FRED, and needs no additional key except for a handful of US-only FRED series."
      }
    },
    {
      "@type": "Question",
      "name": "How is this different from the Financial Modeling Prep or Yahoo Finance MCP servers?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Those servers return raw data and leave the calculations to the language model. The Finance Toolkit MCP computes 500+ metrics, ratios, models and indicators with the open-source Finance Toolkit code, so the numbers are consistent, documented and reproducible regardless of which model you use."
      }
    },
    {
      "@type": "Question",
      "name": "Can I run the server locally?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes. Run uvx --from \"financetoolkit[mcp]\" financetoolkit-mcp-setup to configure Claude Desktop, Claude Code, Cursor, VS Code, Gemini CLI or Windsurf automatically, or add the uvx command to your client's MCP configuration by hand. Claude Desktop users can also install the one-click MCPB bundle."
      }
    },
    {
      "@type": "Question",
      "name": "Does the server work with ChatGPT?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes. ChatGPT supports custom MCP servers through Developer mode on its paid plans: create a connector with the server URL, choose OAuth authentication and enter your FMP API key once."
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
    "500+ financial ratios, models and indicators",
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
