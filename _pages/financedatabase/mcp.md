---
permalink: /projects/financedatabase/mcp
title: Finance Database MCP Server
seo_title: Finance Database MCP Server
excerpt: "Connect Claude, ChatGPT, Cursor, VS Code or any other MCP client to the Finance Database, hosted or on your own machine, and find equities, ETFs, funds, indices, currencies and cryptos in plain English."
description: "Open-source MCP server for the Finance Database: find 300,000+ equities, ETFs, funds and indices by sector, country or issuer in Claude, ChatGPT or Cursor."
classes: wide-sidebar
author_profile: false
layout: single
last_modified_at: 2026-10-10
sidebar:
  nav: "financedatabase-mcp"
image: /assets/images/projects/FinanceDatabaseMCP.jpg
---

<div class="page-header-action notebook-viewer-actions"><a href="https://github.com/JerBouma/FinanceDatabase#mcp-server" target="_blank" rel="noopener"><i class="fab fa-github"></i> View on GitHub</a></div>

Ask an AI assistant for every large European semiconductor company and you will usually get a list. Whether it is complete depends on what the model remembers, and the tickers it gives may be the US over-the-counter lines rather than the shares on Euronext or Xetra. Ask for the bond ETFs of an issuer and you get the famous ones, not all of them.

The Finance Database MCP server gives the assistant the database instead of its memory. It is an open-source [Model Context Protocol](https://modelcontextprotocol.io){:target="_blank"} (MCP) server that connects Claude, ChatGPT, GitHub Copilot, Cursor, Gemini and other assistants to the [Finance Database](/projects/financedatabase): 300,000+ equities, ETFs, funds, indices, currencies, cryptocurrencies and money markets, each categorized by sector, industry, country, exchange, market cap, issuer or category. Ask in plain English and the assistant filters the database on your behalf.

<div class="mcp-facts">
  <div class="mcp-fact"><strong>300,000+</strong><span>equities, ETFs, funds, indices, currencies, cryptos and money markets</span></div>
  <div class="mcp-fact"><strong>No API key</strong><span>no account, no sign-in: connect and start asking</span></div>
  <div class="mcp-fact"><strong>Free</strong><span>hosted at one URL, or run locally; MIT-licensed source code</span></div>
  <div class="mcp-fact"><strong>Any client</strong><span>Claude, ChatGPT, Copilot, Cursor, Windsurf, Gemini, Codex</span></div>
</div>

<img src="/assets/images/projects/FinanceDatabaseMCP.jpg" alt="Finance Database MCP: a table of European semiconductor companies returned by the server" width="100%"/>

## Why the Finance Database MCP

Language models are good at reasoning about companies and poor at listing them. A list from memory misses smaller names, mixes up share classes and listings, and stops at whatever the training data happened to contain. A web search finds articles about companies, not a complete universe you can filter.

<div class="mcp-compare">
<table>
<thead><tr><th></th><th>The model's memory</th><th>Finance Database MCP</th></tr></thead>
<tbody>
<tr><th scope="row">Where the list comes from</th><td data-label="The model's memory">Whatever the model remembers</td><td data-label="Finance Database MCP">300,000+ categorized symbols</td></tr>
<tr><th scope="row">Completeness</th><td data-label="The model's memory">The well-known names</td><td data-label="Finance Database MCP">Every match, with the total count</td></tr>
<tr><th scope="row">Tickers</th><td data-label="The model's memory">Often one listing, not always the right one</td><td data-label="Finance Database MCP">Every listing, with exchange and currency</td></tr>
<tr><th scope="row">Identifiers</th><td data-label="The model's memory">Guessed</td><td data-label="Finance Database MCP">Search by ISIN, CUSIP or FIGI</td></tr>
<tr><th scope="row">Same question, two chats</th><td data-label="The model's memory">Two different lists</td><td data-label="Finance Database MCP">The same list</td></tr>
</tbody>
</table>
</div>

The Finance Database holds classifications, not prices or financial statements. That makes it the natural first step of an analysis: find the universe here, then pass the tickers to the [Finance Toolkit MCP server](/projects/financetoolkit/mcp) for their financial statements, ratios, valuation and risk.

## What You Can Ask

You never have to name a tool or a filter value: ask in plain English and the assistant looks up the valid options and picks the right tool. A few examples of what that covers:

<div class="mcp-uses">
  <div class="mcp-use"><i class="fas fa-building" aria-hidden="true"></i><h3>Screen companies</h3><p>"Which Dutch financial companies are Large or Mega Cap?"</p><span>equities by country, sector, industry, exchange and market cap</span></div>
  <div class="mcp-use"><i class="fas fa-fingerprint" aria-hidden="true"></i><h3>Find a symbol</h3><p>"Which ticker belongs to ISIN US0378331005, and where is it listed?"</p><span>search by ticker, name, ISIN, CUSIP or FIGI</span></div>
  <div class="mcp-use"><i class="fas fa-layer-group" aria-hidden="true"></i><h3>ETFs and funds</h3><p>"What bond ETFs does Vanguard list in the US?"</p><span>by category, issuer, currency and exchange</span></div>
  <div class="mcp-use"><i class="fas fa-earth-europe" aria-hidden="true"></i><h3>Listings and exchanges</h3><p>"On which European exchanges do the large chipmakers trade?"</p><span>exchanges, market identifier codes, primary listings</span></div>
  <div class="mcp-use"><i class="fas fa-chart-area" aria-hidden="true"></i><h3>Indices, currencies and crypto</h3><p>"Which currency pairs quote against the Swiss franc?"</p><span>indices, currency pairs, cryptocurrencies, money markets</span></div>
  <div class="mcp-use"><i class="fas fa-list-ul" aria-hidden="true"></i><h3>Explore the categories</h3><p>"Which industries are there in the Health Care sector?"</p><span>every valid value of a filter, narrowed by other filters</span></div>
</div>

The [example conversations](#example-conversations) below show what that looks like for four questions, with the real results.

## Installation

Pick the [remote server](#remote-server) if you want to get going without installing anything, or the [local server](#local-clients) if you prefer to run the process yourself. Neither needs an API key.

### Remote Server

Point your client at the URL below. There is no sign-in step: the tools are available as soon as the connector is added.

```
https://financedatabase.jeroenbouma.com/mcp
```

Pick your client below for the exact steps; most clients accept the URL through their settings or with a single command. The [privacy policy](https://github.com/JerBouma/FinanceDatabase/blob/main/PRIVACY.md){:target="_blank"} describes what the hosted server processes.

<div class="ft-tabs" markdown="1">

<details class="ft-details" id="remote-claude-desktop" markdown="1">
  <summary><i class="fas fa-robot"></i> <h3>Claude Desktop</h3></summary>

  1. Open **Claude Desktop** and click on **Customize**.
  2. Go to the **Connectors** tab, click on the "+" button and select **Add custom connector**.
  3. Enter a name, e.g. *Finance Database*, and paste the URL:
     ```
     https://financedatabase.jeroenbouma.com/mcp
     ```
  4. Click "Add" and the Finance Database tools are available in your conversations.

</details>

<details class="ft-details" id="remote-claude-ai" markdown="1">
  <summary><i class="fas fa-globe"></i> <h3>Claude.ai</h3></summary>

  1. Open [claude.ai](https://claude.ai){:target="_blank"} and click on **Customize** in the left sidebar.
  2. Go to the **Connectors** tab, click on the "+" button and select **Add custom connector**.
  3. Enter a name, e.g. *Finance Database*, and paste the URL:
     ```
     https://financedatabase.jeroenbouma.com/mcp
     ```
  4. Click "Add" and the Finance Database tools are available in your conversations.

</details>

<details class="ft-details" id="remote-claude-code" markdown="1">
  <summary><i class="fas fa-terminal"></i> <h3>Claude Code</h3></summary>

  1. Run the following command once in your terminal:
     ```bash
     claude mcp add --transport http finance-database https://financedatabase.jeroenbouma.com/mcp
     ```
  2. Restart Claude Code and the Finance Database tools appear automatically.

</details>

<details class="ft-details" id="remote-chatgpt" markdown="1">
  <summary><i class="fas fa-comment-dots"></i> <h3>ChatGPT</h3></summary>

  ChatGPT connects to custom MCP servers through **Developer mode** (available on paid ChatGPT plans):

  1. Open **Settings → Apps & Connectors → Advanced settings** and enable **Developer mode**.
  2. Back in **Apps & Connectors**, click **Create** and enter a name, e.g. *Finance Database*, and the MCP server URL:
     ```
     https://financedatabase.jeroenbouma.com/mcp
     ```
  3. Select **No authentication** and click **Create**.
  4. In a new chat, open the **+** menu, enable the *Finance Database* connector under **Developer mode** and start asking questions.

</details>

<details class="ft-details" id="remote-codex" markdown="1">
  <summary><i class="fas fa-code"></i> <h3>Codex CLI</h3></summary>

  1. Run the following command once in your terminal:
     ```bash
     codex mcp add finance-database --url https://financedatabase.jeroenbouma.com/mcp
     ```
  2. Start `codex` and the Finance Database tools are available in every session.

</details>

<details class="ft-details" id="remote-vs-code" markdown="1">
  <summary><i class="fab fa-microsoft"></i> <h3>VS Code and GitHub Copilot</h3></summary>

  1. Open the **Command Palette** (`Cmd+Shift+P` / `Ctrl+Shift+P`) and run **MCP: Add Server**.
  2. Select **HTTP** as the server type.
  3. Enter the URL `https://financedatabase.jeroenbouma.com/mcp` and name it *finance-database*.
  4. VS Code writes the entry to `.vscode/mcp.json` (or your user profile) automatically and the tools show up in Copilot's **Agent** mode.

</details>

<details class="ft-details" id="remote-cursor" markdown="1">
  <summary><i class="fas fa-i-cursor"></i> <h3>Cursor</h3></summary>

  1. Open **Cursor Settings** (`Cmd+,` / `Ctrl+,`) and navigate to **Features → MCP Servers**.
  2. Click **+ Add new MCP server**.
  3. Set the type to **http** and paste the URL:
     ```
     https://financedatabase.jeroenbouma.com/mcp
     ```
  4. Name it *finance-database* and click **Save**.

</details>

<details class="ft-details" id="remote-windsurf" markdown="1">
  <summary><i class="fas fa-wind"></i> <h3>Windsurf</h3></summary>

  1. Open **Windsurf Settings** and navigate to **MCP Servers**.
  2. Click **Add Server** and select **Remote / HTTP**.
  3. Paste the URL `https://financedatabase.jeroenbouma.com/mcp` and name it *finance-database*.
  4. Click **Save** and reload the window.

</details>

<details class="ft-details" id="remote-gemini" markdown="1">
  <summary><i class="fab fa-google"></i> <h3>Gemini CLI</h3></summary>

  1. Run the following command once in your terminal:
     ```bash
     gemini mcp add --transport http finance-database https://financedatabase.jeroenbouma.com/mcp
     ```
     Alternatively, add the entry to `~/.gemini/settings.json` by hand:
     ```json
     {
       "mcpServers": {
         "finance-database": {
           "httpUrl": "https://financedatabase.jeroenbouma.com/mcp"
         }
       }
     }
     ```
  2. Start `gemini` and run `/mcp` to confirm the server is connected.

</details>

</div>

### Local Clients

The local server runs on your own machine through `uvx` and works with every client that supports the `stdio` transport. The setup wizard finds the config file of Claude Desktop, Claude Code, VS Code, Cursor, Gemini CLI or Windsurf and writes the entry for you:

```bash
uvx --from "financedatabase[mcp]" financedatabase-mcp-setup
```

If you prefer to do it by hand, pick your client below and add the snippet to its config file. The database is downloaded on first use, cached on your machine and checked for updates at most once a day, exactly like the Python package.

<div class="ft-tabs" markdown="1">

<details class="ft-details" id="local-claude-desktop" markdown="1">
  <summary><i class="fas fa-robot"></i> <h3>Claude Desktop</h3></summary>

  **Easiest installation is via the MCPB bundle**, which handles configuration automatically. Download the [Finance Database MCPB bundle](https://github.com/JerBouma/FinanceDatabase/releases/latest/download/financedatabase.mcpb), double-click it and click **Install** in Claude Desktop.

  Alternatively, edit `claude_desktop_config.json` and add the entry inside `mcpServers`:

  - macOS: `~/Library/Application Support/Claude/`
  - Windows: `%APPDATA%\Claude\`
  - Linux: `~/.config/claude/`

  ```json
  {
    "mcpServers": {
      "finance-database": {
        "command": "uvx",
        "args": ["--from", "financedatabase[mcp]", "financedatabase-mcp"]
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
  claude mcp add finance-database -- uvx --from "financedatabase[mcp]" financedatabase-mcp
  ```

  Or edit `~/.claude.json` (create it if needed) and merge the entry inside `mcpServers`:

  ```json
  {
    "mcpServers": {
      "finance-database": {
        "command": "uvx",
        "args": ["--from", "financedatabase[mcp]", "financedatabase-mcp"]
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
  codex mcp add finance-database -- uvx --from "financedatabase[mcp]" financedatabase-mcp
  ```

  Or add the entry to `~/.codex/config.toml`:

  ```toml
  [mcp_servers.finance-database]
  command = "uvx"
  args = ["--from", "financedatabase[mcp]", "financedatabase-mcp"]
  ```

</details>

<details class="ft-details" id="local-vs-code" markdown="1">
  <summary><i class="fab fa-microsoft"></i> <h3>VS Code and GitHub Copilot</h3></summary>

  Create or edit `.vscode/mcp.json` in your workspace root. VS Code uses `servers` as the top-level key (not `mcpServers`):

  ```json
  {
    "servers": {
      "finance-database": {
        "command": "uvx",
        "args": ["--from", "financedatabase[mcp]", "financedatabase-mcp"]
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
      "finance-database": {
        "command": "uvx",
        "args": ["--from", "financedatabase[mcp]", "financedatabase-mcp"]
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
      "finance-database": {
        "command": "uvx",
        "args": ["--from", "financedatabase[mcp]", "financedatabase-mcp"]
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
      "finance-database": {
        "command": "uvx",
        "args": ["--from", "financedatabase[mcp]", "financedatabase-mcp"]
      }
    }
  }
  ```

</details>

</div>

`financedatabase-mcp-inspector` opens the [MCP Inspector](https://github.com/modelcontextprotocol/inspector){:target="_blank"} in your browser, so you can try every tool by hand.

### Self-Hosting

To serve the database to a team or to a browser-based client, run the server over HTTP:

```bash
uvx --from "financedatabase[mcp]" financedatabase-mcp --transport streamable-http --port 8000
```

The repository also includes a `Dockerfile` and `docker-compose.yml`: `docker compose up -d` starts the server at `http://localhost:8000/mcp` and keeps the downloaded database in a volume. `/health` answers health checks, and with `FD_MCP_ANALYTICS=1` the server also publishes anonymous usage totals at `/stats`. The [architecture page](/projects/financedatabase/mcp/architecture#transports-and-self-hosting) has the details.

## Example Conversations

Four questions of the kind an analyst or portfolio manager would ask, each answered through the server's tools. Every result below is the server's real output on 2026-10-10, cut down where noted. The database is updated every week, so the counts move over time.

<div class="ca-nav ca-nav--4">
  <a href="#ex-semiconductors"><i class="fas fa-microchip" aria-hidden="true"></i>Europe's large chipmakers</a>
  <a href="#ex-isin"><i class="fas fa-fingerprint" aria-hidden="true"></i>One ISIN, many listings</a>
  <a href="#ex-vanguard"><i class="fas fa-layer-group" aria-hidden="true"></i>Vanguard's bond ETFs</a>
  <a href="#ex-dutch-financials"><i class="fas fa-landmark" aria-hidden="true"></i>Large Dutch financials</a>
</div>

<div class="mcp-show" id="ex-semiconductors" markdown="1">
<div class="ca-q"><span class="ca-q__avatar"><i class="fas fa-user" aria-hidden="true"></i></span><p>Which large European semiconductor companies are there, and on which European exchanges do they trade?</p></div>
<div class="mcp-show__meta"><span><b>2</b> tool calls</span><span><b>14</b> countries</span><span><b>18</b> listings found</span></div>
<details class="mcp-show__trace"><summary><i class="fas fa-list-check" aria-hidden="true"></i> What the assistant looked up</summary><ol><li><code>show_options</code><span>The exchanges where large European chipmakers are listed: 23, from Amsterdam and Xetra to US over-the-counter markets</span></li><li><code>equities</code><span>Semiconductors &amp; Semiconductor Equipment, Large and Mega Cap, headquartered in 14 European countries, listed on 13 European exchanges</span></li></ol></details>

<div class="mcp-show__result" markdown="1">

| Company | Headquarters | Market cap | European listings |
|:---|:---|:---|:---|
| ASML Holding | Netherlands | Mega Cap | ASML.AS, ASME.DE, ASMF.DE, ASML.MI, ASML.VI |
| ASM International | Netherlands | Large Cap | ASM.AS |
| BE Semiconductor Industries | Netherlands | Large Cap | BESI.AS |
| Infineon Technologies | Germany | Large Cap | IFX.DE, IFX.SW, IFX.VI |
| NXP Semiconductors | Netherlands | Large Cap | VNX.DE, NXPI.VI, 0EDE.L |
| STMicroelectronics | Switzerland | Large Cap | STMPA.PA, STMMI.MI, SGM.DE, STMI.VI |
| Technoprobe | Italy | Large Cap | TPRO.MI |

</div>

<div class="mcp-show__verdict"><p class="mcp-show__label"><i class="fas fa-robot" aria-hidden="true"></i> The answer</p><p>Seven companies, and four of them are Dutch: ASML, ASM International, BE Semiconductor Industries and NXP. ASML is the only Mega Cap and trades on five European venues, from Amsterdam (ASML.AS, its home listing) to Xetra, Milan and Vienna. Without the exchange filter the same search also returns US listings such as ASML and NXPI on Nasdaq and over-the-counter lines such as IFNNY, which is why the assistant first checked where these companies trade.</p></div>
<div class="ca-nums"><span><b>7</b>large European chipmakers</span><span><b>18</b>listings on European exchanges</span><span><b>5</b>European venues for ASML</span></div>
</div>

<div class="mcp-show" id="ex-isin" markdown="1">
<div class="ca-q"><span class="ca-q__avatar"><i class="fas fa-user" aria-hidden="true"></i></span><p>Which ticker belongs to ISIN US0378331005, and where else does it trade?</p></div>
<div class="mcp-show__meta"><span><b>1</b> tool call</span><span><b>19</b> listings</span><span><b>6</b> currencies</span></div>
<details class="mcp-show__trace"><summary><i class="fas fa-list-check" aria-hidden="true"></i> What the assistant looked up</summary><ol><li><code>search_instruments</code><span>The ISIN across all seven asset classes at once: 19 matches, all equities</span></li></ol></details>

<div class="mcp-show__result" markdown="1">

| Market | Listings | Currency |
|:---|:---|:---|
| United States (Nasdaq) | AAPL | USD |
| Germany (8 exchanges, including Xetra and Frankfurt) | APC.DE, APC.F, APC.BE, APC.DU, APC.HM, APC.HA, APC.MU, APC.SG | EUR |
| Argentina (Buenos Aires) | AAPL.BA, AAPLB.BA, AAPLC.BA, AAPLD.BA | ARS, USD |
| Chile (Santiago) | AAPL.SN, AAPLCL.SN | USD, CLP |
| Brazil (B3) | AAPL34.SA | BRL |
| Mexico, Italy, Austria | AAPL.MX, AAPL.MI, AAPL.VI | MXN, EUR |

</div>

<div class="mcp-show__verdict"><p class="mcp-show__label"><i class="fas fa-robot" aria-hidden="true"></i> The answer</p><p>US0378331005 is Apple Inc., ticker AAPL on Nasdaq. The same share trades on 15 exchanges in 6 currencies: eight German exchanges in euros, four lines in Buenos Aires, two in Santiago, a depositary receipt in São Paulo, and Mexico, Milan and Vienna. The ISIN identifies the security; the ticker you use depends on where and in which currency you want to trade it.</p></div>
<div class="ca-nums"><span><b>19</b>listings of one ISIN</span><span><b>15</b>exchanges</span><span><b>8</b>of them in Germany</span></div>
</div>

<div class="mcp-show" id="ex-vanguard" markdown="1">
<div class="ca-q"><span class="ca-q__avatar"><i class="fas fa-user" aria-hidden="true"></i></span><p>Which bond ETFs does Vanguard list in the US, by category?</p></div>
<div class="mcp-show__meta"><span><b>2</b> tool calls</span><span><b>10</b> categories checked</span><span><b>35</b> ETFs</span></div>
<details class="mcp-show__trace"><summary><i class="fas fa-list-check" aria-hidden="true"></i> What the assistant looked up</summary><ol><li><code>show_options</code><span>The categories of Vanguard's Fixed Income ETFs: 10, from Corporate Bonds to Treasury Bonds</span></li><li><code>etfs</code><span>Vanguard, Fixed Income, listed on NYSE Arca, Nasdaq and the NYSE</span></li></ol></details>

<div class="mcp-show__result" markdown="1">

| Category | ETFs | Examples |
|:---|---:|:---|
| Corporate Bonds | 15 | VCSH, VCIT, VCLT, VTC, and ten target maturity ETFs for 2027 to 2036 |
| Investment Grade Bonds | 7 | BND, BNDX, BNDW, BIV, BLV, VCRB, VMBS |
| Treasury Bonds | 5 | VGSH, VGIT, VGLT, EDV, VTG |
| Blend | 2 | BNDP, VPLS |
| Municipal Bonds | 2 | VTEB, VTES |
| Inflation-Protected Securities | 2 | VTIP, VTP |
| Government Bonds | 1 | VGVT |
| Emerging Markets | 1 | VWOB |

</div>

<div class="mcp-show__verdict"><p class="mcp-show__label"><i class="fas fa-robot" aria-hidden="true"></i> The answer</p><p>Vanguard lists 35 bond ETFs on US exchanges. Corporate bonds make up the largest group, 15, and ten of those are the target maturity ETFs that each hold bonds maturing in one year from 2027 to 2036. The broad core is BND for US bonds, BNDX for international bonds and BNDW for both. Without the exchange filter the count rises to 266, because many of these ETFs are also listed in Europe.</p></div>
<div class="ca-nums"><span><b>35</b>US-listed bond ETFs</span><span><b>10</b>target maturity ETFs</span><span><b>8</b>categories</span></div>
</div>

<div class="mcp-show" id="ex-dutch-financials" markdown="1">
<div class="ca-q"><span class="ca-q__avatar"><i class="fas fa-user" aria-hidden="true"></i></span><p>Which Dutch financial companies on Euronext Amsterdam are Large or Mega Cap?</p></div>
<div class="mcp-show__meta"><span><b>2</b> tool calls</span><span><b>4</b> industries</span><span><b>7</b> companies</span></div>
<details class="mcp-show__trace"><summary><i class="fas fa-list-check" aria-hidden="true"></i> What the assistant looked up</summary><ol><li><code>show_options</code><span>The industries of Dutch financial companies on Euronext Amsterdam: Banks, Capital Markets, Diversified Financial Services and Insurance</span></li><li><code>equities</code><span>Netherlands, Financials, Large and Mega Cap, Euronext Amsterdam</span></li></ol></details>

<div class="mcp-show__result" markdown="1">

| Company | Ticker | Industry group |
|:---|:---|:---|
| ABN AMRO Bank | ABN.AS | Banks |
| ING Groep | INGA.AS | Banks |
| Aegon | AGN.AS | Insurance |
| ASR Nederland | ASRNL.AS | Insurance |
| NN Group | NN.AS | Insurance |
| CVC Capital Partners | CVC.AS | Diversified Financials |
| Exor | EXO.AS | Diversified Financials |

</div>

<div class="mcp-show__verdict"><p class="mcp-show__label"><i class="fas fa-robot" aria-hidden="true"></i> The answer</p><p>Seven companies, all Large Cap: none reaches the Mega Cap tier of $200 billion. Three are insurers (Aegon, ASR Nederland and NN Group), two are banks (ABN AMRO and ING) and two are diversified financials (CVC Capital Partners and Exor). These tickers go straight into the Finance Toolkit MCP server to compare their solvency and profitability.</p></div>
<div class="ca-nums"><span><b>7</b>Large Cap financials</span><span><b>3</b>insurers</span><span><b>0</b>Mega Caps</span></div>
</div>

## Tools

The server has one tool per asset class and three tools to search and explore. The assistant picks the tool; you only ask the question.

| Tool | What it does |
|:---|:---|
| `equities` | Stocks by country, sector, industry group, industry, currency, exchange, market identifier code, market or market cap tier |
| `etfs` | ETFs by category group, category, issuer family, currency or exchange |
| `funds` | Mutual funds by category group, category, fund family, currency or exchange |
| `indices` | Market indices by category group, category, currency or exchange |
| `currencies` | Currency pairs by base and quote currency |
| `cryptos` | Cryptocurrency pairs by coin and the currency they are quoted in |
| `moneymarkets` | Money market funds by currency or fund family |
| `search_instruments` | Find a symbol by ticker, name, ISIN, CUSIP or FIGI across all asset classes at once |
| `show_options` | Every valid value of a filter, such as all sectors or countries, optionally narrowed by other filters |
| `search_categories` | The asset classes with their size, filters and description |

Every filter accepts several comma-separated values, and every asset class tool also takes a free-text query on symbol and name. Results come back as compact tables of 25 rows by default and at most 200, with a note on how to get the next page, so no answer ever floods the conversation. A filter value that doesn't exist returns a suggestion: ask for the sector "Technology" and the server answers "Did you mean 'Information Technology'?". The [architecture page](/projects/financedatabase/mcp/architecture) explains how it works under the hood.

## FAQ

The questions that come up most often about the server and the data behind it. Anything missing? Open an issue on [GitHub](https://github.com/JerBouma/FinanceDatabase/issues){:target="_blank"}.

<details class="ft-details" markdown="1">
  <summary><h3>Is the Finance Database MCP server free?</h3></summary>

  Yes. The server and the [Finance Database](/projects/financedatabase) are open source under the MIT license (see the [repository](https://github.com/JerBouma/FinanceDatabase){:target="_blank"}), the hosted server is free to use and no API key or account is needed.

</details>

<details class="ft-details" markdown="1">
  <summary><h3>Which AI assistants and clients does it work with?</h3></summary>

  Any client that speaks the Model Context Protocol. There are step-by-step cards for Claude Desktop, claude.ai, Claude Code, ChatGPT, Codex CLI, VS Code, Cursor, Windsurf and Gemini CLI under [Remote Server](#remote-server) and [Local Clients](#local-clients).

</details>

<details class="ft-details" markdown="1">
  <summary><h3>Do I need to install Python?</h3></summary>

  No. The [remote server](#remote-server) needs nothing installed. The [local server](#local-clients) runs through [uv](https://docs.astral.sh/uv/getting-started/installation/){:target="_blank"}, which downloads the right Python and the package by itself, and the Claude Desktop bundle installs everything in one click.

</details>

<details class="ft-details" markdown="1">
  <summary><h3>Opening the URL in my browser shows "Not Acceptable". Is it down?</h3></summary>

  No. The URL is an endpoint for MCP clients, which talk to it with streaming requests a browser doesn't send, so a browser gets "Not Acceptable: Client must accept text/event-stream". Add the URL to your assistant as described under [Remote Server](#remote-server) instead. To check that the server is up, open [/health](https://financedatabase.jeroenbouma.com/health){:target="_blank"}.

</details>

<details class="ft-details" markdown="1">
  <summary><h3>What data does the server cover?</h3></summary>

  The full Finance Database: 300,000+ equities, ETFs, funds, indices, currencies, cryptocurrencies and money markets with their classifications, such as sector, industry, country, exchange, market cap tier, ETF category and issuer, and identifiers such as ISIN, CUSIP and FIGI. It holds no prices or financial statements; for those, pair it with the [Finance Toolkit MCP server](/projects/financetoolkit/mcp).

</details>

<details class="ft-details" markdown="1">
  <summary><h3>How current is the data?</h3></summary>

  The database is maintained on [GitHub](https://github.com/JerBouma/FinanceDatabase){:target="_blank"} and republished on every change and every week. The server downloads the published files on first use, caches them and checks for updates at most once a day, so it follows the database without a new release.

</details>

<details class="ft-details" markdown="1">
  <summary><h3>Can I use it together with the Finance Toolkit MCP server?</h3></summary>

  Yes, and that is what it is designed for. Add both servers to your client: the Finance Database finds the companies, ETFs or funds that match your question, and the [Finance Toolkit MCP server](/projects/financetoolkit/mcp) analyzes them, from financial statements and ratios to valuation and risk.

</details>

<details class="ft-details" markdown="1">
  <summary><h3>What does the hosted server store about me?</h3></summary>

  It needs no account and stores no personal data. It counts anonymous usage totals, such as calls per day and per tool, which are published at [/stats](https://financedatabase.jeroenbouma.com/stats){:target="_blank"}. The [privacy policy](https://github.com/JerBouma/FinanceDatabase/blob/main/PRIVACY.md){:target="_blank"} has the details. If you prefer to keep everything on your own machine, use the [local server](#local-clients).

</details>

<details class="ft-details" markdown="1">
  <summary><h3>How do I contribute or report a wrong classification?</h3></summary>

  The Finance Database is community-managed. Open an issue or a pull request on [GitHub](https://github.com/JerBouma/FinanceDatabase){:target="_blank"} with the symbol and the correction; once it is merged, every server picks it up within a day.

</details>
