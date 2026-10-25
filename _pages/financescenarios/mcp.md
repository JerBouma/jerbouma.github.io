---
permalink: /projects/financescenarios/mcp
title: Finance Scenarios MCP Server
seo_title: Finance Scenarios MCP Server
excerpt: "Connect Claude, ChatGPT, Cursor, VS Code or any other MCP client to Finance Scenarios, hosted or on your own machine, and ask how inflation, interest rates, stocks and your portfolio could develop, today or under a stress story, in plain English."
description: "Open-source MCP server for economic scenarios: simulate inflation, rates, stocks, currencies and portfolios under 40 stress regimes in Claude, ChatGPT or Cursor."
classes: wide-sidebar
author_profile: false
layout: single
last_modified_at: 2026-10-23
sitemap: false
noindex: true
search: false
sidebar:
  nav: "financescenarios-mcp"
image: assets/images/projects/financescenarios/banner.png
---

<div class="page-header-action notebook-viewer-actions"><a href="https://github.com/JerBouma/FinanceScenarios#mcp-server" target="_blank" rel="noopener"><i class="fab fa-github"></i> View on GitHub</a></div>

<div class="mcp-facts">
  <div class="mcp-fact"><strong>40</strong><span>stress regimes, from the 1970s to 2022</span></div>
  <div class="mcp-fact"><strong>Monthly</strong><span>calibrated on market data each month</span></div>
  <div class="mcp-fact"><strong>No API key</strong><span>no account, no sign-in</span></div>
  <div class="mcp-fact"><strong>Any client</strong><span>Claude, ChatGPT, Copilot, Cursor and more</span></div>
</div>

Ask an AI assistant where inflation and the 10-year yield will be in five years and you will usually get one number, with a disclaimer. Ask what a return of the 1970s would do to them and you get a story about the 1970s, not about an economy that starts from today's rates. Ask how likely your portfolio is to reach a goal and the answer is a guess.

The Finance Scenarios MCP server lets the assistant simulate instead of guess. It is an open-source [Model Context Protocol](https://modelcontextprotocol.io){:target="_blank"} (MCP) server that connects Claude, ChatGPT, GitHub Copilot, Cursor, Gemini and other assistants to [Finance Scenarios](/projects/financescenarios): thousands of correlated scenarios for inflation, interest rates, unemployment, stocks, currencies, gold and oil, calibrated each month on market data. Ask in plain English and the assistant runs the baseline, a stress regime, a one-factor shock or your portfolio, and answers with the range of outcomes.

## Why the Finance Scenarios MCP

Language models are good at explaining how the economy works and poor at quantifying what could happen next. A number from memory has no range, ignores where rates and inflation stand today, and changes from one chat to the next. A stress story told in words never says how far the long rate would move, or how often a portfolio would end below where it started.

<div class="mcp-compare">
<table>
<thead><tr><th></th><th>The model's memory</th><th>Finance Scenarios MCP</th></tr></thead>
<tbody>
<tr><th scope="row">Where the outlook comes from</th><td data-label="The model's memory">Whatever the model remembers</td><td data-label="Finance Scenarios MCP">Thousands of scenarios calibrated this month on market data</td></tr>
<tr><th scope="row">Uncertainty</th><td data-label="The model's memory">One number, or a vague range</td><td data-label="Finance Scenarios MCP">The median and p5 to p95 for every year</td></tr>
<tr><th scope="row">Stress stories</th><td data-label="The model's memory">A description of the past</td><td data-label="Finance Scenarios MCP">39 regimes replayed from today's starting point</td></tr>
<tr><th scope="row">Links between factors</th><td data-label="The model's memory">Implied, if at all</td><td data-label="Finance Scenarios MCP">Inflation moves the policy rate and the long rate through the model</td></tr>
<tr><th scope="row">Same question, two chats</th><td data-label="The model's memory">Two different answers</td><td data-label="Finance Scenarios MCP">The same answer</td></tr>
</tbody>
</table>
</div>

Every number comes from the calibration and the scenarios documented in the [Finance Scenarios documentation](/projects/financescenarios/docs), so an answer from a chat can be traced back to its model. The answers are ranges across scenarios, not forecasts.

The server pairs with the other two. The [Finance Database MCP server](/projects/financedatabase/mcp) finds the funds and shares to hold, the [Finance Toolkit MCP server](/projects/financetoolkit/mcp) analyzes them, and Finance Scenarios shows how they could develop.

## What You Can Ask

You never have to name a tool, a regime or a factor: ask in plain English and the assistant searches for the right regime and picks the tool. A few examples of what that covers:

<div class="mcp-uses">
  <div class="mcp-use"><i class="fas fa-chart-line" aria-hidden="true"></i><h3>Today's outlook</h3><p>"Where could US inflation, the Fed's rate and the 10-year yield be over the next five years?"</p><span>simulate: percentiles per factor and year</span></div>
  <div class="mcp-use"><i class="fas fa-fire" aria-hidden="true"></i><h3>Stress stories</h3><p>"What would a return of the 1970s stagflation do to US inflation and the 10-year?"</p><span>39 regimes, from Volcker to the 2008 crisis and 2022</span></div>
  <div class="mcp-use"><i class="fas fa-bolt" aria-hidden="true"></i><h3>One-factor shocks</h3><p>"What happens to rates and stocks if inflation reaches 8% within a year?"</p><span>a shock with its spillover and historical anchors</span></div>
  <div class="mcp-use"><i class="fas fa-chart-pie" aria-hidden="true"></i><h3>Portfolios and goals</h3><p>"How likely is a 60/40 portfolio to grow from 10,000 to 15,000 in ten years?"</p><span>value per year, drawdown, Value at Risk, chance of a goal</span></div>
  <div class="mcp-use"><i class="fas fa-clock-rotate-left" aria-hidden="true"></i><h3>Backtests</h3><p>"How did 80% VWCE.DE and 20% AGG do, year by year?"</p><span>tickers, factors or presets on monthly history</span></div>
  <div class="mcp-use"><i class="fas fa-magnifying-glass" aria-hidden="true"></i><h3>Explore what there is</h3><p>"Which stress regimes are about a housing crash?"</p><span>regimes, factors, portfolio presets and factor sets</span></div>
</div>

The [example conversations](#example-conversations) below show what that looks like for four questions, with the real results.

## Installation

Pick the [remote server](#remote-server) if you want to get going without installing anything, or the [local server](#local-clients) if you prefer to run the process yourself. Neither needs an API key.

### Remote Server

{% comment %}TODO: hosted URL at launch. Every https://financescenarios.jeroenbouma.com/mcp below is the address in server.json, not live yet.{% endcomment %}

Point your client at the URL below. There is no sign-in step: the tools are available as soon as the connector is added.

```
https://financescenarios.jeroenbouma.com/mcp
```

Pick your client below for the exact steps; most clients accept the URL through their settings or with a single command.

<div class="ft-tabs" markdown="1">

<details class="ft-details" id="remote-claude-desktop" markdown="1">
  <summary><i class="fas fa-robot"></i> <h3>Claude Desktop</h3></summary>

  1. Open **Claude Desktop** and click on **Customize**.
  2. Go to the **Connectors** tab, click on the "+" button and select **Add custom connector**.
  3. Enter a name, e.g. *Finance Scenarios*, and paste the URL:
     ```
     https://financescenarios.jeroenbouma.com/mcp
     ```
  4. Click "Add" and the Finance Scenarios tools are available in your conversations.

</details>

<details class="ft-details" id="remote-claude-ai" markdown="1">
  <summary><i class="fas fa-globe"></i> <h3>Claude.ai</h3></summary>

  1. Open [claude.ai](https://claude.ai){:target="_blank"} and click on **Customize** in the left sidebar.
  2. Go to the **Connectors** tab, click on the "+" button and select **Add custom connector**.
  3. Enter a name, e.g. *Finance Scenarios*, and paste the URL:
     ```
     https://financescenarios.jeroenbouma.com/mcp
     ```
  4. Click "Add" and the Finance Scenarios tools are available in your conversations.

</details>

<details class="ft-details" id="remote-claude-code" markdown="1">
  <summary><i class="fas fa-terminal"></i> <h3>Claude Code</h3></summary>

  1. Run the following command once in your terminal:
     ```bash
     claude mcp add --transport http finance-scenarios https://financescenarios.jeroenbouma.com/mcp
     ```
  2. Restart Claude Code and the Finance Scenarios tools appear automatically.

</details>

<details class="ft-details" id="remote-chatgpt" markdown="1">
  <summary><i class="fas fa-comment-dots"></i> <h3>ChatGPT</h3></summary>

  ChatGPT connects to custom MCP servers through **Developer mode** (available on paid ChatGPT plans):

  1. Open **Settings → Apps & Connectors → Advanced settings** and enable **Developer mode**.
  2. Back in **Apps & Connectors**, click **Create** and enter a name, e.g. *Finance Scenarios*, and the MCP server URL:
     ```
     https://financescenarios.jeroenbouma.com/mcp
     ```
  3. Select **No authentication** and click **Create**.
  4. In a new chat, open the **+** menu, enable the *Finance Scenarios* connector under **Developer mode** and start asking questions.

</details>

<details class="ft-details" id="remote-codex" markdown="1">
  <summary><i class="fas fa-code"></i> <h3>Codex CLI</h3></summary>

  1. Run the following command once in your terminal:
     ```bash
     codex mcp add finance-scenarios --url https://financescenarios.jeroenbouma.com/mcp
     ```
  2. Start `codex` and the Finance Scenarios tools are available in every session.

</details>

<details class="ft-details" id="remote-vs-code" markdown="1">
  <summary><i class="fab fa-microsoft"></i> <h3>VS Code and GitHub Copilot</h3></summary>

  1. Open the **Command Palette** (`Cmd+Shift+P` / `Ctrl+Shift+P`) and run **MCP: Add Server**.
  2. Select **HTTP** as the server type.
  3. Enter the URL `https://financescenarios.jeroenbouma.com/mcp` and name it *finance-scenarios*.
  4. VS Code writes the entry to `.vscode/mcp.json` (or your user profile) automatically and the tools show up in Copilot's **Agent** mode.

</details>

<details class="ft-details" id="remote-cursor" markdown="1">
  <summary><i class="fas fa-i-cursor"></i> <h3>Cursor</h3></summary>

  1. Open **Cursor Settings** (`Cmd+,` / `Ctrl+,`) and navigate to **Features → MCP Servers**.
  2. Click **+ Add new MCP server**.
  3. Set the type to **http** and paste the URL:
     ```
     https://financescenarios.jeroenbouma.com/mcp
     ```
  4. Name it *finance-scenarios* and click **Save**.

</details>

<details class="ft-details" id="remote-windsurf" markdown="1">
  <summary><i class="fas fa-wind"></i> <h3>Windsurf</h3></summary>

  1. Open **Windsurf Settings** and navigate to **MCP Servers**.
  2. Click **Add Server** and select **Remote / HTTP**.
  3. Paste the URL `https://financescenarios.jeroenbouma.com/mcp` and name it *finance-scenarios*.
  4. Click **Save** and reload the window.

</details>

<details class="ft-details" id="remote-gemini" markdown="1">
  <summary><i class="fab fa-google"></i> <h3>Gemini CLI</h3></summary>

  1. Run the following command once in your terminal:
     ```bash
     gemini mcp add --transport http finance-scenarios https://financescenarios.jeroenbouma.com/mcp
     ```
     Alternatively, add the entry to `~/.gemini/settings.json` by hand:
     ```json
     {
       "mcpServers": {
         "finance-scenarios": {
           "httpUrl": "https://financescenarios.jeroenbouma.com/mcp"
         }
       }
     }
     ```
  2. Start `gemini` and run `/mcp` to confirm the server is connected.

</details>

</div>

### Local Clients

The local server runs on your own machine and works with every client that supports the `stdio` transport. Install the package with its `mcp` extra:

{% comment %}TODO: pip/uvx install line at launch. Until the PyPI release, install from a checkout: pip install -e ".[mcp]".{% endcomment %}

```bash
pip install "financescenarios[mcp]"
```

That adds the `financescenarios-mcp` command (`python -m financescenarios.mcp_server` does the same). Pick your client below and add the snippet to its config file; if your client doesn't find the command, give the full path to it, e.g. the output of `which financescenarios-mcp`.

The very first question builds the month's data, which takes about a minute; after that the server answers from it and refreshes it once a month in the background. To have it ready beforehand, run `financescenarios-mcp-warm`, which also answers the baseline and every regime ahead of time.

<div class="ft-tabs" markdown="1">

<details class="ft-details" id="local-claude-desktop" markdown="1">
  <summary><i class="fas fa-robot"></i> <h3>Claude Desktop</h3></summary>

  Edit `claude_desktop_config.json` and add the entry inside `mcpServers`:

  - macOS: `~/Library/Application Support/Claude/`
  - Windows: `%APPDATA%\Claude\`
  - Linux: `~/.config/claude/`

  ```json
  {
    "mcpServers": {
      "finance-scenarios": {
        "command": "financescenarios-mcp"
      }
    }
  }
  ```

</details>

<details class="ft-details" id="local-claude-ai" markdown="1">
  <summary><i class="fas fa-globe"></i> <h3>Claude.ai</h3></summary>

  Claude.ai runs in the browser and cannot start a process on your machine, so it only connects to servers over HTTP. Use the [remote server](#remote-claude-ai) instead, or [host the server yourself](#self-hosting) behind a public URL.

</details>

<details class="ft-details" id="local-claude-code" markdown="1">
  <summary><i class="fas fa-terminal"></i> <h3>Claude Code</h3></summary>

  Run the following command once in your terminal:

  ```bash
  claude mcp add finance-scenarios -- financescenarios-mcp
  ```

  Or edit `~/.claude.json` (create it if needed) and merge the entry inside `mcpServers`:

  ```json
  {
    "mcpServers": {
      "finance-scenarios": {
        "command": "financescenarios-mcp"
      }
    }
  }
  ```

</details>

<details class="ft-details" id="local-chatgpt" markdown="1">
  <summary><i class="fas fa-comment-dots"></i> <h3>ChatGPT</h3></summary>

  ChatGPT only connects to MCP servers over HTTP and cannot start a local process. Use the [remote server](#remote-chatgpt) instead, or [host the server yourself](#self-hosting) behind a public URL.

</details>

<details class="ft-details" id="local-codex" markdown="1">
  <summary><i class="fas fa-code"></i> <h3>Codex CLI</h3></summary>

  Run the following command once in your terminal:

  ```bash
  codex mcp add finance-scenarios -- financescenarios-mcp
  ```

  Or add the entry to `~/.codex/config.toml`:

  ```toml
  [mcp_servers.finance-scenarios]
  command = "financescenarios-mcp"
  ```

</details>

<details class="ft-details" id="local-vs-code" markdown="1">
  <summary><i class="fab fa-microsoft"></i> <h3>VS Code and GitHub Copilot</h3></summary>

  Create or edit `.vscode/mcp.json` in your workspace root. VS Code uses `servers` as the top-level key (not `mcpServers`):

  ```json
  {
    "servers": {
      "finance-scenarios": {
        "command": "financescenarios-mcp"
      }
    }
  }
  ```

</details>

<details class="ft-details" id="local-cursor" markdown="1">
  <summary><i class="fas fa-i-cursor"></i> <h3>Cursor</h3></summary>

  Create or edit `.cursor/mcp.json` in your project (or `~/.cursor/mcp.json` for all projects):

  ```json
  {
    "mcpServers": {
      "finance-scenarios": {
        "command": "financescenarios-mcp"
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
      "finance-scenarios": {
        "command": "financescenarios-mcp"
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
      "finance-scenarios": {
        "command": "financescenarios-mcp"
      }
    }
  }
  ```

</details>

</div>

### Self-Hosting

To serve the scenarios to a team or to a browser-based client, run the server over HTTP:

```bash
financescenarios-mcp --transport streamable-http --port 8000
```

The repository also includes a `Dockerfile` and `docker-compose.yml`: `docker compose up -d` starts the server at `http://localhost:8000/mcp` and keeps the monthly data in a volume, and `docker compose run --rm finance-scenarios-mcp financescenarios-mcp-warm` builds the month ahead, for example from cron on the first day. `/health` answers health checks, and with `FINANCESCENARIOS_MCP_ANALYTICS=1` the server also publishes anonymous usage totals at `/stats`. The [architecture page](/projects/financescenarios/mcp/architecture#transports-and-self-hosting) has the details.

## Example Conversations

Four questions of the kind an investor, adviser or risk manager would ask, each answered through the server's tools. Every result below is the server's real output on 2026-10-23, from the October 2026 calibration at the default 1,000 scenarios, cut down where noted. The calibration is refreshed every month, so the numbers move over time.

<div class="ca-nav ca-nav--4">
  <a href="#ex-stagflation"><i class="fas fa-fire" aria-hidden="true"></i>The 1970s, from today</a>
  <a href="#ex-inflation-shock"><i class="fas fa-bolt" aria-hidden="true"></i>Inflation at 8% in a year</a>
  <a href="#ex-60-40"><i class="fas fa-chart-pie" aria-hidden="true"></i>A 60/40 portfolio and a goal</a>
  <a href="#ex-backtest"><i class="fas fa-clock-rotate-left" aria-hidden="true"></i>A world equity mix since 2010</a>
</div>

<div class="mcp-show" id="ex-stagflation" markdown="1">
<div class="ca-q"><span class="ca-q__avatar"><i class="fas fa-user" aria-hidden="true"></i></span><p>What would a return of the 1970s stagflation do to US inflation and the 10-year Treasury yield over the next ten years?</p></div>
<div class="mcp-show__meta"><span><b>2</b> tool calls</span><span><b>1,000</b> scenarios</span><span><b>2</b> factors over 10 years</span></div>
<details class="mcp-show__trace"><summary><i class="fas fa-list-check" aria-hidden="true"></i> What the assistant looked up</summary><ol><li><code>search</code><span>Regimes matching "1970s stagflation": 1970s Stagflation, Oil Crisis and Persistent High Inflation</span></li><li><code>simulate</code><span>regime <code>stagflation_1970s</code>, factors "inflation, long rate", horizons 1, 2, 3, 5 and 10 years</span></li></ol></details>

<div class="mcp-show__result" markdown="1">

| Year | Inflation, baseline | Inflation, 1970s | 10-year, baseline | 10-year, 1970s |
|:---|---:|---:|---:|---:|
| Today | 3.7% | 3.7% | 4.95% | 4.95% |
| 1 | 2.8% | 5.8% | 5.17% | 5.79% |
| 2 | 2.2% | 6.9% | 5.29% | 7.05% |
| 3 | 2.1% | 7.6% | 5.46% | 7.92% |
| 5 | 1.9% | 8.1% | 5.54% | 8.75% |
| 10 | 1.8% | 8.3% | 5.54% | 9.83% |

Medians across the scenarios. The server read "inflation" and "long rate" as the US factors.

</div>

<div class="mcp-show__verdict"><p class="mcp-show__label"><i class="fas fa-robot" aria-hidden="true"></i> The answer</p><p>In the baseline, US inflation eases from 3.7% today to around 2% within two years and the 10-year yield drifts up from 4.95% to about 5.5%. A return of the 1970s turns that around: inflation climbs to 6.9% in year two and settles above 8%, and the 10-year follows it up, to 8.75% by year five and 9.83% by year ten, 4.3 points above the baseline. The range is wide: in year ten nine in ten stagflation scenarios put the 10-year between 3.0% and 16.8%. Starting from today's rates, the climb takes years rather than months.</p></div>
<div class="ca-nums"><span><b>8.3%</b>inflation in year 10, against 1.8%</span><span><b>9.83%</b>10-year yield in year 10</span><span><b>+4.3</b>points on the 10-year</span></div>
</div>

<div class="mcp-show" id="ex-inflation-shock" markdown="1">
<div class="ca-q"><span class="ca-q__avatar"><i class="fas fa-user" aria-hidden="true"></i></span><p>What happens to interest rates, stocks and unemployment if US inflation reaches 8% within a year?</p></div>
<div class="mcp-show__meta"><span><b>1</b> tool call</span><span><b>5</b> factors</span><span><b>3</b> historical anchors</span></div>
<details class="mcp-show__trace"><summary><i class="fas fa-list-check" aria-hidden="true"></i> What the assistant looked up</summary><ol><li><code>simulate</code><span>shock_factor "inflation", shock_level "8%", shock_peak_year 1: the baseline, the shock and its three historical anchors (2022 Inflation and Rate Hikes, 1970s Stagflation, Oil Crisis)</span></li></ol></details>

<div class="mcp-show__result" markdown="1">

| Median | Year 1 | Year 2 | Year 3 | Year 5 | Baseline, year 3 |
|:---|---:|---:|---:|---:|---:|
| Inflation | 8.1% | 7.0% | 6.1% | 3.8% | 2.1% |
| Short rate | 6.5% | 9.4% | 10.3% | 8.7% | 4.4% |
| 10-year yield | 6.4% | 8.5% | 9.7% | 10.0% | 5.5% |
| US stocks, yearly return from today | 6.5% | 5.3% | 5.8% | 7.0% | 8.9% |
| Unemployment | 4.1% | 4.5% | 4.9% | 5.7% | 4.8% |

Stocks read as the annualized return from today to that year. Cut down from the answer's yearly rows over ten years.

</div>

<div class="mcp-show__verdict"><p class="mcp-show__label"><i class="fas fa-robot" aria-hidden="true"></i> The answer</p><p>The shock lifts inflation to 8.1% in year one and lets it ease to 3.8% by year five. Rates react through the model's policy rule: the short rate climbs from 4.0% today to 10.3% in year three and the 10-year to about 10%, more than four points above the baseline. Stocks return 6.5% in the first year against 9.6% in the baseline, and unemployment rises to 5.7% by year five. The server puts three historical episodes next to it, and they disagree on stocks: in year one the shock lowers the median stock return by 3.0 points, while the anchors range from 20.0 points higher (2022, when stocks rose before they fell) to 28.6 points lower (the 1970s) and 50.6 points lower (the Oil Crisis). The model's monthly correlation between inflation and US stocks since 2000 is only +0.08, while in history high inflation went with weak stock returns (<a href="https://doi.org/10.1016/0304-405X(77)90014-9" target="_blank">Fama and Schwert, 1977</a>), so the anchors are the harsher read.</p></div>
<div class="ca-nums"><span><b>10.3%</b>short rate in year 3</span><span><b>−3.0</b>points on stocks in year 1</span><span><b>−28.6</b>points in the 1970s anchor</span></div>
</div>

<div class="mcp-show" id="ex-60-40" markdown="1">
<div class="ca-q"><span class="ca-q__avatar"><i class="fas fa-user" aria-hidden="true"></i></span><p>I invest 10,000 in a 60/40 portfolio. How likely is it to reach 15,000 within ten years, and how bad could it get along the way?</p></div>
<div class="mcp-show__meta"><span><b>2</b> tool calls</span><span><b>1,000</b> scenarios</span><span><b>10</b> years</span></div>
<details class="mcp-show__trace"><summary><i class="fas fa-list-check" aria-hidden="true"></i> What the assistant looked up</summary><ol><li><code>search</code><span>Portfolio presets matching "60/40": 60/40 Balanced (60% US stocks, 40% US Treasury bonds) and Global 60/40</span></li><li><code>portfolio</code><span>holdings <code>balanced_60_40</code>, 10 years, goal 15,000, rebalanced yearly</span></li></ol></details>

<div class="mcp-show__result" markdown="1">

| Year | p5 | Median | p95 |
|:---|---:|---:|---:|
| 1 | 9,037 | 10,745 | 12,215 |
| 3 | 8,903 | 12,404 | 15,664 |
| 5 | 9,229 | 14,328 | 19,725 |
| 10 | 10,950 | 20,900 | 35,965 |

Value in US dollars. Cut down from the answer's yearly rows.

</div>

<div class="mcp-show__verdict"><p class="mcp-show__label"><i class="fas fa-robot" aria-hidden="true"></i> The answer</p><p>The goal is likely: 83.5% of scenarios end above 15,000 after ten years and 87.4% pass it at some point, in the median case after about 4.8 years. The median portfolio grows to 20,900, a yearly growth rate of 7.7%, and only 3.5% of scenarios end below the 10,000 invested. The way there is bumpier than the end point suggests: the median scenario falls 15.4% from a high at some point, and one in twenty falls 34% or more. In the worst one in twenty, the portfolio is still below its start after five years.</p></div>
<div class="ca-nums"><span><b>83.5%</b>chance of 15,000 by year 10</span><span><b>7.7%</b>median yearly growth</span><span><b>−15.4%</b>median deepest fall</span></div>
</div>

<div class="mcp-show" id="ex-backtest" markdown="1">
<div class="ca-q"><span class="ca-q__avatar"><i class="fas fa-user" aria-hidden="true"></i></span><p>How would 80% in a world equity fund like VWCE and 20% in US bonds have done since 2010?</p></div>
<div class="mcp-show__meta"><span><b>2</b> tool calls</span><span><b>200</b> months of history</span><span><b>17</b> calendar years</span></div>
<details class="mcp-show__trace"><summary><i class="fas fa-list-check" aria-hidden="true"></i> What the assistant looked up</summary><ol><li><code>backtest</code><span>holdings "VWCE.DE:0.8, AGG:0.2" from 2010: the holdings share history from July 2019 only, so it starts there</span></li><li><code>backtest</code><span>holdings "VT:0.8, AGG:0.2" from 2010, with Vanguard's US-listed world equity ETF in place of VWCE</span></li></ol></details>

<div class="mcp-show__result" markdown="1">

| Year | Value | Return |
|:---|---:|---:|
| 2010 | 11,631 | 16.3% |
| 2011 | 11,119 | −4.4% |
| 2015 | 15,354 | −1.4% |
| 2018 | 18,366 | −7.4% |
| 2019 | 22,553 | 22.8% |
| 2022 | 24,514 | −17.1% |
| 2025 | 39,358 | 19.4% |
| 2026, to September | 43,185 | 9.7% |

80% VT and 20% AGG, in US dollars, rebalanced yearly. Cut down from the answer's 17 calendar years.

</div>

<div class="mcp-show__verdict"><p class="mcp-show__label"><i class="fas fa-robot" aria-hidden="true"></i> The answer</p><p>VWCE itself only exists since July 2019, so the server started the first backtest there: 10,000 grew to 20,684 in US dollars by September 2026, 10.7% a year. To reach back to 2010 the assistant swapped in VT, which holds the same world index: 10,000 became 43,185, a yearly growth rate of 9.2%, with a volatility of 12.0%. Four calendar years lost money, 2022 the most at −17.1%, and the deepest fall from a high was 23.4%. That is one path of history; the portfolio tool shows the range of paths ahead.</p></div>
<div class="ca-nums"><span><b>43,185</b>from 10,000 since 2010</span><span><b>9.2%</b>yearly growth</span><span><b>−23.4%</b>deepest fall</span></div>
</div>

## FAQ

The questions that come up most often about the server and the scenarios behind it. Anything missing? Open an issue on [GitHub](https://github.com/JerBouma/FinanceScenarios/issues){:target="_blank"}.

<details class="ft-details" markdown="1">
  <summary><h3>Is the Finance Scenarios MCP server free?</h3></summary>

  Yes. The server and [Finance Scenarios](/projects/financescenarios) are open source under the MIT license (see the [repository](https://github.com/JerBouma/FinanceScenarios){:target="_blank"}), the hosted server is free to use and no API key or account is needed.

</details>

<details class="ft-details" markdown="1">
  <summary><h3>Which AI assistants and clients does it work with?</h3></summary>

  Any client that speaks the Model Context Protocol. There are step-by-step cards for Claude Desktop, claude.ai, Claude Code, ChatGPT, Codex CLI, VS Code, Cursor, Windsurf and Gemini CLI under [Remote Server](#remote-server) and [Local Clients](#local-clients).

</details>

<details class="ft-details" markdown="1">
  <summary><h3>Do I need to install Python?</h3></summary>

  Not for the [remote server](#remote-server), which needs nothing installed. The [local server](#local-clients) is part of the Python package: install it with its `mcp` extra and your client starts `financescenarios-mcp` itself.

</details>

<details class="ft-details" markdown="1">
  <summary><h3>What happens when I open the URL in my browser?</h3></summary>

  You get a short setup page: the URL is an endpoint for MCP clients, which talk to it with streaming requests a browser doesn't send, so the page shows how to add it to your assistant in three steps, with the local alternative. The same steps are under [Remote Server](#remote-server). To check that the server is up, open `/health`; `/stats` shows the anonymous usage totals as a dashboard.

</details>

<details class="ft-details" markdown="1">
  <summary><h3>What does the server simulate?</h3></summary>

  Two factor sets. The `default` set has 27 factors: inflation, short and long rates and unemployment for the US, the euro area and the UK, with global equities, gold, oil and the major currencies. The `broad` set has 74: the default plus Japan, Canada, Australia and India, US sectors and styles, more countries' equities, silver, copper, natural gas, five more currencies and SPY's dividend yield. A request runs on the default set unless a regime or holding needs the broad one. How each factor is modelled is in the [documentation](/projects/financescenarios/docs).

</details>

<details class="ft-details" id="faq-tools" markdown="1">
  <summary><h3>Which tools does the server expose?</h3></summary>

  Four. The assistant picks the tool; you only ask the question.

  | Tool | What it does |
  |:---|:---|
  | `search` | Finds stress regimes, a factor set's factors, the portfolio presets and the factor sets by keyword |
  | `simulate` | The percentiles of each factor per year: today's baseline, up to five regimes side by side, or a one-factor shock with its historical anchors |
  | `portfolio` | How holdings could develop: the value per year, the yearly growth rate, the deepest fall, Value at Risk, the chance of a loss and of reaching a goal, with monthly contributions or withdrawals |
  | `backtest` | How holdings did in the past on monthly history: the value at each year end, that year's return, the growth rate, the deepest fall and the volatility |

  Holdings are tickers (`VWCE.DE`, `AGG`), factors (`us_broad`, `gold`) or one of 13 presets (`balanced_60_40`); a ticker is described as a mix of the simulated factors, with its fit. Levels can be written as `0.08` or `8%`, and names as people use them: `inflation`, `long rate`, `stocks`, `euro area`. Every answer is one table of rows per scenario, factor and year, ready to chart, with notes on what was assumed or corrected, and it never exceeds 40,000 characters. The [architecture page](/projects/financescenarios/mcp/architecture) explains how it works under the hood.

</details>

<details class="ft-details" markdown="1">
  <summary><h3>How current is the data?</h3></summary>

  The server calibrates each factor set once a month on data up to that month, from Yahoo Finance, the OECD, EIOPA, the BIS and Ken French's data library, none of which need a key. Every answer says which month its data is from. Early in a new month the previous month's data keeps answering while this month's is built in the background, and the answer says so.

</details>

<details class="ft-details" markdown="1">
  <summary><h3>Are these forecasts?</h3></summary>

  No. Each answer is the spread of a thousand scenarios by default, from p5 to p95 around the median. A regime keeps the scenarios that tell its story, and a shock moves one factor and shows what tends to come with it. The same question on the same month's data gives the same answer, so a number can be checked.

</details>

<details class="ft-details" markdown="1">
  <summary><h3>Can I use it together with the Finance Toolkit and Finance Database MCP servers?</h3></summary>

  Yes. Add all three to your client: the [Finance Database](/projects/financedatabase/mcp) finds the funds and shares that match your question, the [Finance Toolkit](/projects/financetoolkit/mcp) analyzes them, and Finance Scenarios runs them through the coming years and the stress stories of the past.

</details>

<details class="ft-details" markdown="1">
  <summary><h3>What does the hosted server store about me?</h3></summary>

  It needs no account and stores no personal data. It keeps anonymous usage totals, such as calls per day and per tool and the kind of question asked, and counts unique users with a keyed hash of the IP address and user agent, which is never stored in readable form; tool arguments are not stored. The totals are published at `/stats`. If you prefer to keep everything on your own machine, use the [local server](#local-clients).

</details>

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Is the Finance Scenarios MCP server free?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes. The server and Finance Scenarios are open source under the MIT license (see the repository), the hosted server is free to use and no API key or account is needed."
      }
    },
    {
      "@type": "Question",
      "name": "Which AI assistants and clients does it work with?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Any client that speaks the Model Context Protocol. There are step-by-step cards for Claude Desktop, claude.ai, Claude Code, ChatGPT, Codex CLI, VS Code, Cursor, Windsurf and Gemini CLI under Remote Server and Local Clients."
      }
    },
    {
      "@type": "Question",
      "name": "Do I need to install Python?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Not for the remote server, which needs nothing installed. The local server is part of the Python package: install it with its mcp extra and your client starts financescenarios-mcp itself."
      }
    },
    {
      "@type": "Question",
      "name": "What happens when I open the URL in my browser?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "You get a short setup page: the URL is an endpoint for MCP clients, which talk to it with streaming requests a browser doesn't send, so the page shows how to add it to your assistant in three steps, with the local alternative. The same steps are under Remote Server. To check that the server is up, open /health; /stats shows the anonymous usage totals as a dashboard."
      }
    },
    {
      "@type": "Question",
      "name": "What does the server simulate?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Two factor sets. The default set has 27 factors: inflation, short and long rates and unemployment for the US, the euro area and the UK, with global equities, gold, oil and the major currencies. The broad set has 74: the default plus Japan, Canada, Australia and India, US sectors and styles, more countries' equities, silver, copper, natural gas, five more currencies and SPY's dividend yield. A request runs on the default set unless a regime or holding needs the broad one. How each factor is modelled is in the documentation."
      }
    },
    {
      "@type": "Question",
      "name": "Which tools does the server expose?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Four. The assistant picks the tool; you only ask the question. Holdings are tickers (VWCE.DE, AGG), factors (us_broad, gold) or one of 13 presets (balanced_60_40); a ticker is described as a mix of the simulated factors, with its fit. Levels can be written as 0.08 or 8%, and names as people use them: inflation, long rate, stocks, euro area. Every answer is one table of rows per scenario, factor and year, ready to chart, with notes on what was assumed or corrected, and it never exceeds 40,000 characters. The architecture page explains how it works under the hood."
      }
    },
    {
      "@type": "Question",
      "name": "How current is the data?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "The server calibrates each factor set once a month on data up to that month, from Yahoo Finance, the OECD, EIOPA, the BIS and Ken French's data library, none of which need a key. Every answer says which month its data is from. Early in a new month the previous month's data keeps answering while this month's is built in the background, and the answer says so."
      }
    },
    {
      "@type": "Question",
      "name": "Are these forecasts?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "No. Each answer is the spread of a thousand scenarios by default, from p5 to p95 around the median. A regime keeps the scenarios that tell its story, and a shock moves one factor and shows what tends to come with it. The same question on the same month's data gives the same answer, so a number can be checked."
      }
    },
    {
      "@type": "Question",
      "name": "Can I use it together with the Finance Toolkit and Finance Database MCP servers?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes. Add all three to your client: the Finance Database finds the funds and shares that match your question, the Finance Toolkit analyzes them, and Finance Scenarios runs them through the coming years and the stress stories of the past."
      }
    },
    {
      "@type": "Question",
      "name": "What does the hosted server store about me?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "It needs no account and stores no personal data. It keeps anonymous usage totals, such as calls per day and per tool and the kind of question asked, and counts unique users with a keyed hash of the IP address and user agent, which is never stored in readable form; tool arguments are not stored. The totals are published at /stats. If you prefer to keep everything on your own machine, use the local server."
      }
    }
  ]
}
</script>
{% comment %}TODO: installUrl is the hosted URL at launch.{% endcomment %}
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "Finance Scenarios MCP Server",
  "alternateName": "FinanceScenarios MCP",
  "url": "https://www.jeroenbouma.com/projects/financescenarios/mcp",
  "applicationCategory": "FinanceApplication",
  "operatingSystem": "Any",
  "softwareVersion": "0.1.0",
  "license": "https://github.com/JerBouma/FinanceScenarios/blob/main/LICENSE",
  "codeRepository": "https://github.com/JerBouma/FinanceScenarios",
  "installUrl": "https://financescenarios.jeroenbouma.com/mcp",
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
  "description": "Open-source Model Context Protocol server that gives Claude, ChatGPT, Cursor, VS Code and other AI assistants economic scenarios: thousands of correlated scenarios for inflation, interest rates, unemployment, stocks, currencies, gold and oil, calibrated each month, under 40 stress regimes or a one-factor shock, with portfolio simulations and backtests.",
  "featureList": [
    "Thousands of correlated scenarios, calibrated monthly",
    "40 stress regimes and one-factor shocks with historical anchors",
    "Portfolio simulation with goals, drawdowns and Value at Risk",
    "Backtests of tickers, factors and presets",
    "No API key, account or sign-in",
    "Works with any MCP-compatible client"
  ]
}
</script>

{% include mcp-page-script.html %}
