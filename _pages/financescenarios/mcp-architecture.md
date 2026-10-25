---
permalink: /projects/financescenarios/mcp/architecture
title: Finance Scenarios MCP Architecture
seo_title: Finance Scenarios MCP Server Architecture
excerpt: "How the Finance Scenarios MCP server is built: four tools described from config.yaml, monthly snapshots built ahead of time, a result cache, a limit on heavy runs, bounded JSON answers and a stateless hosted server."
description: "How the open-source Finance Scenarios MCP server works: four tools, monthly snapshots, a result cache, limits on heavy runs, bounded answers and self-hosting."
classes: wide-sidebar
author_profile: false
layout: single
last_modified_at: 2026-10-23
sitemap: false
noindex: true
search: false
sidebar:
  nav: "financescenarios-mcp"
---

<div class="page-header-action notebook-viewer-actions"><a href="https://github.com/JerBouma/FinanceScenarios/tree/main/financescenarios/mcp_server" target="_blank" rel="noopener"><i class="fab fa-github"></i> View on GitHub</a></div>

The MCP server lives entirely inside `financescenarios/mcp_server/` and is a thin layer over the Finance Scenarios package itself. It has four tools: `search` finds what the other three take, `simulate` runs the economy and markets, `portfolio` runs a set of holdings through the same scenarios and `backtest` holds them through history. Every answer comes from a **monthly snapshot**: a factor set calibrated once a month and stored with its history, so a question never downloads anything. The server needs no API key and keeps no user state.

**For developers.** If you just want to use Finance Scenarios through your assistant, the [Finance Scenarios MCP Server](/projects/financescenarios/mcp) page covers installation, example questions and the available tools. Everything below is implementation detail for those who want to extend, self-host or contribute to the server.
{: .notice--info}

## Module Overview
{: .heading-as-h3}

The server follows the package's own split: `_model.py` modules are pure functions without I/O, `_controller.py` modules orchestrate, and each tool family has a folder of its own.

| Module | Role |
|:---|:---|
| `mcp_server_controller.py` | Entry points (`main`, `run_warm`), config loading, server assembly, `/health` route, the setup page middleware and transport wiring |
| `tools/tools_controller.py` | Registers the four tools with their descriptions from `config.yaml` and runs every call: plan, cache lookup, compute, render |
| `tools/search/search_controller.py` | The `search` tool: regimes, a factor set's factors, portfolio presets and factor sets by keyword |
| `tools/simulate/simulate_controller.py` | The `simulate` tool: the baseline, up to five regimes side by side, or a one-factor shock with its historical anchors |
| `tools/holdings/holdings_controller.py` | The `portfolio` and `backtest` tools: holdings as tickers, factors or a preset, simulated or held on history |
| `provider/provider_controller.py` | The state behind the tools: the newest snapshot per factor set, the result cache, the regimes, the limit on heavy runs and the stdout guard |
| `request_model.py` | A parsed request (`Plan`), the memory budget, the factor set a request runs on, the factors it reports and a shock's normalized form |
| `answer_model.py` | Assembles an answer: the scenarios it names, the long table of percentiles, risk figures, holdings, calendar years and search results |
| `formatting_model.py` | Compact JSON, rounding, units in words, and the character cap that thins a table rather than cutting it off |
| `coercion_model.py` | Turns loosely typed input into clean values: `8%` or `0.08`, clamped integers, names however they are typed, holdings such as `VWCE.DE:0.6, us_broad:0.4`, and "did you mean" suggestions |
| `analytics/` | Optional usage counter behind `/stats` and its dashboard, off unless `FINANCESCENARIOS_MCP_ANALYTICS` is set |
| `setup_page_model.py` | The page a browser gets when it opens the MCP endpoint |
| `config.yaml` | Server instructions, limits, defaults, the factor sets served, the shock anchors, cache settings and every tool and parameter description |

Calibrating, simulating and caching happen in the package's own `snapshot` module, the same code paths as `Snapshot.load().summary(...)` in Python. Mapping a ticker onto the factors is the package's `map_ticker()`, the returns-based style analysis of [Sharpe (1992)](https://doi.org/10.3905/jpm.1992.409394){:target="_blank"}.

## Startup Sequence
{: .heading-as-h3}

When the server process starts (`financescenarios-mcp`), `main()` and `build_mcp_app()` run these steps:

1. **Pick the transport**: `--transport`, then `MCP_TRANSPORT`, then `stdio`. The log level comes from `FINANCESCENARIOS_MCP_LOG_LEVEL` (`WARNING` by default).
2. **Install the stdout guard**: before any thread starts, so a tool run can never write into the JSON-RPC stream (see [The Stdout Guard](#the-stdout-guard)).
3. **Read `config.yaml`**: the server name and instructions, the limits, the defaults, the factor sets served, the shock anchors, the cache settings and the tool descriptions.
4. **Create the FastMCP instance**: with the instructions and the website URL. The server sets the installed `financescenarios` version itself, so clients see the package version in `serverInfo` rather than the MCP SDK's.
5. **Create the provider**: a `ScenarioProvider` for the `default` and `broad` factor sets, with the concurrency and timeout from `config.yaml` or from `FINANCESCENARIOS_MCP_CONCURRENCY` and `FINANCESCENARIOS_MCP_TIMEOUT`. It loads no snapshot yet; the first call does that.
6. **Register the tools**: `ScenarioTools.register()` adds `search`, `simulate`, `portfolio` and `backtest`, each annotated as read-only and idempotent.
7. **Set up analytics**: only when `FINANCESCENARIOS_MCP_ANALYTICS` is on, which adds `/stats`. Otherwise no statistics file is written.
8. **Register `/health`**, which returns `{"status": "ok"}`.
9. **Warm up**, only with `FINANCESCENARIOS_MCP_WARM=1`: a background thread builds this month's snapshots and precomputes their answers while the server already accepts calls.
10. **Start the transport**: stdio directly, or SSE and streamable HTTP through Uvicorn with the setup page and CORS middleware.

## Four Tools
{: .heading-as-h3}

An economic scenario generator has a small surface: what to simulate, under which story, and for which holdings. Each of those is one tool, so a model never has to learn a router or an `indicator` parameter.

| Tool | What it takes | What it returns |
|:---|:---|:---|
| `search` | `kind` (regimes, factors, portfolios or factor sets), a `query` and a `category` | The matches, best first, each with the factor sets it runs on |
| `simulate` | A `regime` or a list of up to five, or a `shock_factor` with a `shock_level`, the `factors` to report, `years` or `horizons` | Percentiles (p5, p25, median, p75, p95) per factor and year, with the baseline's median and the difference |
| `portfolio` | `holdings` (tickers, factors or a preset id), `initial_value`, `monthly_contribution`, `goal`, `rebalance`, a regime or shock | The value per year (p5 to p95), the CAGR, the deepest fall, Value at Risk, the chance of a loss and of reaching the goal, and each holding's fit |
| `backtest` | `holdings`, `start_year`, `rebalance`, `currency` | The value at each year end with that year's return, the CAGR, the deepest fall and the volatility |

`_described()` builds each tool function from its method and gives every parameter its description from `config.yaml` through an `Annotated` type, so FastMCP generates an accurate JSON Schema and a missing description fails at startup rather than reaching a client. Changing what a model reads about a tool is a config change.

Every answer has the same shape: a few header fields (the factor set, the month the data is from, the start, the scenarios run, the units in words), then one long table as `columns` and `rows`, a row per scenario, factor and year, ready to chart, and `_notes` with whatever was assumed, corrected or left out.

## Requests, Snapshots and the Result Cache
{: .heading-as-h3}

Every call runs through `ScenarioTools._respond()` in four steps, each off the event loop in a worker thread:

1. **Plan**: the tool's planner parses the arguments into a `Plan`: the factor set it runs on, its normalized request (which doubles as the cache key and never holds an API key), whether it is heavy, and whether it runs a regime that keeps only part of its scenarios. Planning reads no data and takes no slot.
2. **Look up**: the answer of that request on the newest snapshot, from the result cache. A hit is answered at once.
3. **Compute**: on a miss, the plan runs on the snapshot behind the limit on heavy runs, and its answer is stored.
4. **Render**: the parse notes first, the answer's own notes next and the snapshot's age last, as JSON within the [character cap](#limits).

**Snapshots.** A snapshot is a factor set calibrated as of a month, stored with its monthly history, its configuration and, for the regimes that need one, a calibration of their own. Simulating from it downloads nothing. The server builds them without API keys, from Yahoo Finance, the OECD, EIOPA, the BIS and Ken French's data library (`use_environment_keys: false`). They are kept in `snapshots/<month>/` of the cache folder, `FINANCESCENARIOS_CACHE_DIR` or else `~/.cache/financescenarios`. A file lock keeps several processes from building the same snapshot twice, and the provider keeps the four most recently used snapshots loaded in memory (`snapshot_cache_size`).

**Monthly refresh.** When the newest snapshot is from an earlier month, the answer still comes from it, with a note such as "Data as of 2026-09; this month's refresh is running.", and one background thread builds this month's. A failed build is tried again after an hour, not on every request. Only a server with no snapshot at all builds one first, and says so in the answer. After a background build the provider calls `precompute()`, and each build drops all but the newest two months of snapshots, results and ticker mappings (`keep_months`).

**The result cache.** `ResultCache` keeps each answer as a JSON file named by the SHA-256 of the canonical request (keys sorted), the snapshot id and the package version, filed under the snapshot's month. The same question on the same snapshot always gets the same answer, so it is computed once. An answer larger than 512 kB is returned but not kept. An answer for a ticker fetched with a caller's own Financial Modeling Prep key is not kept either; its ticker mapping is.

**Warm-up.** `precompute()` answers the month's most likely questions ahead of time: the baseline and every one of the 39 named regimes that runs on the factor set, at the default settings (1,000 scenarios, seed 42, ten years). Asking for one of them, or for a shock's historical anchors, is then a cache read. `financescenarios-mcp-warm` does the build and the precompute for every factor set from the command line, and `--factor-set` limits it to one:

```bash
financescenarios-mcp-warm                      # every factor set served
financescenarios-mcp-warm --factor-set default # only one
```

Run it once a month, for example from cron on the first day, or start the server with `FINANCESCENARIOS_MCP_WARM=1`. The command writes its report to stdout as JSON and each problem as a line on stderr, followed by a summary. A problem is a snapshot that failed to build, an answer that failed to precompute, or a factor or regime the snapshot left out, and any of them makes it exit with code 1, so a cron job notices. A factor set whose build fails doesn't stop the others from warming.

## Regimes, Shocks and Anchors
{: .heading-as-h3}

A regime is a named stress story from the package's [regime library](/projects/financescenarios/docs/regimes), such as `stagflation_1970s` or `financial_crisis`. `simulate` takes it by id or name however it is typed: a close spelling runs with a note ("Read regime 'stagflaton 1970' as 'stagflation_1970s'"), and a phrase that is no regime's name runs the best search match when it scores well enough.

A shock moves one factor to a level by `shock_peak_year` and back to normal by `shock_normal_by_year`. It becomes a regime on the snapshot's calibration (`shock_regime()`), so the factors the model links to it follow through their own equations; the notes name those links. With `spillover` on (the default), the run also keeps the 30% of scenarios in which the shocked factor moved furthest its way (`spillover_share`), so the other factors show what tends to come with the move.

Each shock comes with up to three **historical anchors**: named regimes of the same move, listed per direction under `anchors` in `config.yaml` (an inflation rise is anchored by `inflation_shock_2022`, `stagflation_1970s`, `oil_crisis` and `energy_war_2022`). An anchor is used only when it runs on the factor set, sets or reaches the shocked factor, and its precomputed answer moves that factor the same way. The anchors are answered from the warm-up's cache, so they rarely cost a run.

The factor set is picked per request: the one asked for, or else the first served set that has every regime and factor holding the request needs, with a note when that is `broad`.

## Limits
{: .heading-as-h3}

The limits come from `config.yaml` and bound every call, so no answer floods the conversation and no request can take the machine:

| Limit | Value | Applies to |
|:---|:---|:---|
| `max_characters` | 40,000 | Characters per answer; a longer one has its table thinned, with a note |
| `max_simulations` | 5,000 | Scenarios per call (default 1,000, at least 100) |
| `max_years` | 30 | Years in `simulate` (default 10) |
| `max_portfolio_years` | 40 | Years in `portfolio` (default 10) |
| `max_factors` | 12 | Factors reported in one `simulate` call |
| `max_holdings` | 10 | Holdings in one portfolio |
| `max_regimes` | 5 | Regimes compared in one `simulate` call |
| `max_search_results` | 100 | Results per `search` (default 10) |
| `max_simulated_values` | 200,000,000 | Values a run of a narrowing regime may hold at its peak |
| `max_plain_values` | 80,000,000 | Values any other run may hold |

A value out of range is clamped with a note rather than refused: a model asking for `n_simulations=50000` gets 5,000. The two value budgets bound memory. `scenario_budget()` estimates a run's peak as the scenarios drawn times the factors and steps, plus the paths added for holdings, and lowers `n_simulations` with a note when the request would not fit. A regime that keeps only the scenarios telling its story draws them in batches of up to 20,000, which is why it gets the larger budget and runs alone.

When an answer is longer than 40,000 characters, `fit_to_size()` thins each series of the table to evenly spaced rows, always keeping its first and last year, and says so in a note that suggests fewer factors or `horizons=[...]`. Only when three rows a series are still too many does the table go, and the rest of the answer stays readable JSON.

## Concurrency and Timeouts
{: .heading-as-h3}

Simulations are CPU and memory heavy, so the provider lets only two run at once (`max_concurrent`, or `FINANCESCENARIOS_MCP_CONCURRENCY`). Planning, cache lookups and searches take no slot and are never held up by a running simulation.

A run of a regime that keeps only part of its scenarios takes the single narrowing slot and then every heavy slot, so it runs alone. The limits are sized for a regime that keeps 1 scenario in 83, which on the broad factor set at the default 1,000 scenarios needs about 3.1 GB, with each batch it draws freed before the next. The most selective shipped story, `credit_crunch`, keeps about 1 in 17. The warm-up precomputes it, so a request rarely needs one.

Each step of a request has 120 seconds (`timeout_seconds`, or `FINANCESCENARIOS_MCP_TIMEOUT`), including any wait for a slot. When that passes, the client gets a message rather than an error:

```text
`simulate` is taking longer than 120 seconds: the server is busy or the request is large. It keeps running and its answer is kept, so ask again in a minute, or lower n_simulations or years.
```

The work itself carries on in its thread and stores its answer, so asking again a minute later is a cache read. The background refresh of a snapshot also takes a heavy slot.

## Errors and Corrections
{: .heading-as-h3}

No tool raises to the client. Invalid input comes back as `Invalid input for <tool>: ...` with the fix, such as the closest regime ids and the `search` call that lists them, and any other failure as one line with its type, the traceback only in the server's log. An API key a caller sent is replaced by `***` in every message.

Many near misses never become errors. `coercion_model.py` reads `8%`, `"0.08"` and `8` as the same level, weights as decimals or percents (`VWCE.DE:60%, AGG:40%`), holdings without weights as equal shares, and weights that do not sum to one as scaled. Countries such as `US`, `UK` or `euro area` and plain factor names such as `inflation`, `long rate`, `stocks` or `euro` resolve to the factor of that country. Each correction is one line in `_notes`, so the assistant can say what was assumed.

## The Stdout Guard
{: .heading-as-h3}

Under stdio, stdout carries the JSON-RPC messages and nothing else, while the calibration and simulation code underneath may print progress. Swapping `sys.stdout` with `contextlib.redirect_stdout` is not safe once two tool runs overlap in threads: one run restoring the stream would undo the other's redirect.

`install_stdout_guard()` therefore replaces `sys.stdout` once, at startup and before any thread runs, with a `ThreadAwareStdout`. It keeps a per-thread counter: while a thread is inside `redirect_stdout_to_stderr()`, which wraps every tool run, the warm-up and the background refresh, what that thread writes goes to stderr. Every other thread, including the transport writing to the underlying buffer, keeps the real stdout.

## Transports and Self-Hosting
{: .heading-as-h3}

`stdio` is the default and is what local clients such as Claude Desktop and VS Code use. `streamable-http` and `sse` are for hosted deployments, configured with `--host` and `--port` or `MCP_HOST` and `MCP_PORT` (default `0.0.0.0:8000`). Uvicorn runs with proxy headers on, and CORS allows any origin and exposes `Mcp-Session-Id` for browser-based clients.

The repository's `Dockerfile` builds a `python:3.12-slim` image with `uv`, sets `MCP_TRANSPORT=streamable-http` and keeps the snapshots and answers in `FINANCESCENARIOS_CACHE_DIR=/data/financescenarios` and the Finance Toolkit's downloads in `FINANCE_TOOLKIT_CACHE_DB=/data/financetoolkit/cache.db`. `docker-compose.yml` puts both on named volumes, sets a 6 GB memory limit and passes the concurrency, timeout, warm-up and log level through from a `.env` file, so a self-hosted server is one command, and the month is built ahead with a second:

```bash
docker compose up -d
docker compose run --rm finance-scenarios-mcp financescenarios-mcp-warm
```

The server then listens on `http://localhost:8000/mcp`, and `/health` answers the container's health check.

**The setup page.** A browser that opens `/mcp` or `/sse` gets a short HTML page instead of an MCP error: what the server does, the URL to add as a remote connector, that no sign-in or API key is needed, an example question and a link to this documentation. `SetupPageMiddleware` serves it only to a `GET` that accepts `text/html` and not `text/event-stream`, so MCP clients, which post JSON-RPC or ask for an event stream, pass through untouched. The URL on the page is the address the browser opened, so it is right for every deployment.

**Usage statistics.** With `FINANCESCENARIOS_MCP_ANALYTICS=1`, the `analytics` package counts tool calls and publishes the totals at `/stats`: calls today and over the last 7 days, the average duration, calls and users per day over the last 30 days, unique and new users, calls per tool, and the kind of question asked (today's outlook, a stress regime or a one-factor shock). To tell users apart it combines the client's address (Cloudflare's `CF-Connecting-IP` or `X-Forwarded-For` behind a proxy) and user agent into an HMAC-SHA256 keyed hash and keeps its first 12 characters. The address and user agent themselves are never stored, and neither are tool arguments. The secret comes from `FINANCESCENARIOS_MCP_SECRET_KEY`; without it a random one is generated once and kept in a `.secret` file, readable by the owner only, next to the counts. The counts are saved to `FINANCESCENARIOS_MCP_STATS_FILE` (by default `mcp/stats.json` in the cache folder) every five calls and on shutdown. `/stats` returns JSON to scripts and a self-contained dashboard, with inline charts and no scripts, to a browser. A local installation has it off.

**API keys.** None are needed. A caller who wants a ticker the keyless sources don't cover can send their own Financial Modeling Prep key with the `x-fmp-api-key` header or the `fmp_api_key` query parameter over HTTP; under stdio the local `FINANCIAL_MODELING_PREP_API_KEY` is used. A hosted server never uses a key from its own environment for a remote caller.

To connect a client, see the [installation section](/projects/financescenarios/mcp#installation) of the main page.
