---
permalink: /projects/financedatabase/mcp/architecture
title: "Finance Database MCP Architecture"
seo_title: "Finance Database MCP Server Architecture"
excerpt: "How the Finance Database MCP server is built: one generated tool per asset class from config.yaml, typed filters with suggestions, bounded JSON responses, daily data caching and a stateless hosted server."
description: "How the open-source Finance Database MCP server works: one tool per asset class, typed filters, bounded JSON output, data caching and self-hosting."
classes: wide-sidebar
author_profile: false
layout: single
last_modified_at: 2026-10-10
sidebar:
  nav: "financedatabase-mcp"
---

<div class="page-header-action notebook-viewer-actions"><a href="https://github.com/JerBouma/FinanceDatabase/tree/main/financedatabase/mcp_server" target="_blank" rel="noopener"><i class="fab fa-github"></i> View on GitHub</a></div>

The MCP server lives entirely inside `financedatabase/mcp_server/` and is a thin layer over the Finance Database package itself. Each of the seven asset classes (equities, ETFs, funds, indices, currencies, cryptocurrencies and money markets) becomes one MCP tool, generated from a single `config.yaml`. Three utility tools help the model find symbols and valid filter values. The server needs no API key and keeps no user state.

**For developers.** If you just want to use the Finance Database through your assistant, the [Finance Database MCP Server](/projects/financedatabase/mcp) page covers installation, example prompts and the available tools. Everything below is implementation detail for those who want to extend, self-host or contribute to the server.
{: .notice--info}

## Module Overview
{: .heading-as-h3}

| Module | Role |
|:---|:---|
| `mcp_controller.py` | Entry points (`main`, `run_setup`, `run_inspector`), config loading, server assembly, `/health` route, transport wiring |
| `registry_model.py` | Builds and registers one tool per asset class, with a typed signature generated from the package's filters |
| `tools_model.py` | Registers the three utility tools: `search_categories`, `show_options` and `search_instruments` |
| `provider_model.py` | Query engine: caches one Finance Database instance per asset class, resolves filters, runs lazy queries and adds suggestions to errors |
| `coercion_model.py` | Turns loosely typed input from a model into clean values: booleans, clamped integers, comma-separated lists and "did you mean" matches |
| `formatting_model.py` | Converts a page of results into compact JSON with paging notes, and renders small Markdown tables |
| `analytics_model.py` | Optional anonymous usage counter behind `/stats`, off unless `FD_MCP_ANALYTICS` is set |
| `setup_model.py` | Interactive and CLI setup wizard: writes the server entry into client config files |
| `config.yaml` | Server instructions, output limits, cache lifetime, filter descriptions and the seven asset class definitions |
| `mcpb/` | Source of the MCP Bundle: `manifest.json`, build script and icon |

Downloading and caching the data happens in the package's own `cache_model.py` and `database_controller.py`, the same code paths as `import financedatabase as fd`.

## Startup Sequence
{: .heading-as-h3}

When the server process starts (`uvx --from financedatabase[mcp] financedatabase-mcp`), `mcp_controller._build_mcp_app()` runs these steps:

1. **Read `config.yaml`**: the server name and instructions, the output limits, the instance lifetime and the list of asset classes. Each asset class entry becomes an `AssetClassSpec` dataclass.
2. **Create the provider**: a `DatabaseProvider` is built from the specs. It loads no data yet; the first tool call for an asset class does that.
3. **Create the FastMCP instance**: with the server instructions from the config. FastMCP takes no version, so the server sets the installed `financedatabase` version itself. Clients see the package version in `serverInfo` rather than the MCP SDK's.
4. **Set up analytics**: only when `FD_MCP_ANALYTICS` is on. Otherwise this step returns nothing and no statistics file is written.
5. **Register tools**: `AssetToolRegistry` registers the seven asset class tools, then `UtilityToolRegistry` registers the three utility tools.
6. **Register routes**: `/stats` (when analytics are on) and `/health`, which returns `{"status": "ok"}`.
7. **Start the transport**: `main()` picks `--transport`, then `MCP_TRANSPORT`, then `stdio`. For HTTP transports it adds CORS middleware and starts Uvicorn.

## One Tool per Asset Class
{: .heading-as-h3}

The Finance Database has a small, fixed surface: seven asset classes, each with a `select()` method and a handful of filters, so each becomes its own tool. A model sees `equities`, `etfs`, `funds`, `indices`, `currencies`, `cryptos` and `moneymarkets`, and each tool lists exactly the filters that apply to it. There is no router or `indicator` parameter to learn.

`AssetToolRegistry._build_wrapper()` generates each tool from its `config.yaml` entry:

- The **filters** come from the package class's `FIELDS` attribute, so the MCP tool and `select()` can never drift apart. Equities get `country`, `sector`, `industry_group`, `industry`, `currency`, `exchange`, `mic`, `market` and `market_cap`; currencies get `base_currency` and `quote_currency`.
- Each filter gets its **description** from `filter_descriptions` in the config, with examples of real values (for example `'Information Technology'` for sector, `'NMS'` for exchange).
- The **common parameters** are added after the filters: `query`, `include_delisted` and `only_primary_listing` where the asset class supports them, then `show_columns`, `include_summary`, `limit` and `offset`.

The wrapper's `__signature__` is replaced with an `inspect.Signature` built from these parameters, so FastMCP generates an accurate JSON Schema for each tool. Every tool is annotated as read-only and idempotent.

Adding an asset class or changing a description is a config change.

## Filters and Arguments
{: .heading-as-h3}

`coercion_model.py` and `DatabaseProvider.resolve_filters()` accept the common shapes models send instead of rejecting them.

| Argument | Behavior |
|:---|:---|
| Filters | One value, a comma-separated string (`"Netherlands, Belgium"`) or a list. Matching ignores case. |
| `query` | Case-insensitive literal substring on symbol and name, so `S&P 500` or `BRK.B` need no escaping. An ISIN, CUSIP or FIGI matches exactly where the asset class has those columns. |
| `include_delisted` | Equities and ETFs only. Delisted entries are excluded by default; this includes them and adds a `delisted` column. |
| `only_primary_listing` | Equities, ETFs and funds. Keeps symbols without an exchange suffix such as `.L` or `.DE`. If none match, all matching listings are kept. |
| `show_columns` | Comma-separated column names, matched case-insensitively. The symbol column always comes first. An unknown column returns suggestions and the full column list. |
| `include_summary` | Adds the business or fund description. Off by default to keep responses small. |
| `limit` / `offset` | Page size and starting row. |

Splitting on commas is not enough on its own, because some valid values contain commas, such as the industry `Hotels, Restaurants & Leisure`. `resolve_values()` therefore re-joins the parts greedily: at each position it takes the longest run of parts that forms a known value.

Booleans accept `true`, `1` and `yes` as strings. Integers are parsed from strings or floats and clamped to their range, because a model asking for `limit=1000` should get the maximum rather than an error.

When a `query` is given, results are ranked: an exact symbol or identifier match first, then symbols starting with the query, then names starting with it. Ties go to primary listings, then larger market cap tiers, then shorter names. This is why `query="apple"` lists Apple Inc. before Apple Hospitality.

The filtering itself is the package's own logic on a Polars `LazyFrame`. Only the requested page and columns are collected, so a call reads 25 rows rather than the full table with every summary.

## Responses and Limits
{: .heading-as-h3}

Every asset class tool returns compact JSON from `formatting_model.format_page()`. A real response for Dutch financials with `limit=2`:

```json
{"asset_class":"equities","total":101,"returned":2,"offset":0,"limit":2,
 "columns":["symbol","name","currency","sector","industry_group","industry","exchange","country","market_cap"],
 "rows":[{"symbol":"0O4B.IL","name":"Van Lanschot Kempen NV cert. of shs", ...}, ...],
 "_notes":["Showing rows 1-2 of 101. Use offset=2 to get the next page, or narrow the filters."]}
```

The limits come from `config.yaml` and bound every call, so no request can return the full dataset:

| Limit | Value | Applies to |
|:---|:---|:---|
| `default_limit` | 25 | Rows per call when `limit` is not set |
| `max_limit` | 200 | Largest page; a higher `limit` is capped with a note |
| `max_text_length` | 300 | Characters per text value; longer values end in `…` |
| `default_options` | 100 | Values returned by `show_options` for one filter |
| `max_options` | 500 | Largest `show_options` limit |
| `overview_options` | 25 | Values per filter in the `show_options` overview |

The `_notes` field tells the model what to do next: the `offset` of the next page, or that nothing matched and `show_options` can check the values. JSON is written without whitespace and keeps non-ASCII characters such as in Société Générale.

## Data and Caching
{: .heading-as-h3}

The server answers from the published Finance Database files, not from a live API.

- **Source**: the typed Parquet files in the repository's `compression/` folder on GitHub. CI builds them from the database CSVs on every merge and every Sunday. If a Parquet file is missing, the package falls back to the older bz2 CSV and converts it to the same types.
- **First use**: the file for an asset class is downloaded on the first call that needs it and written to the cache directory atomically. The directory is `FINANCEDATABASE_CACHE_DIR` if set, otherwise the platform cache folder (for example `~/.cache/financedatabase` on Linux). In production it is a Docker volume, so restarts don't download again.
- **Updates**: a cached file is checked at most once a day with a conditional request carrying its ETag. An unchanged file is not downloaded again. If GitHub can't be reached, the cached copy is used.
- **Instances**: `DatabaseProvider` keeps one Finance Database instance per asset class, guarded by a lock, and rebuilds it after `instance_ttl_seconds` (86,400, so 24 hours). That rebuild is what triggers the daily update check. If a refresh fails, the previous instance is kept.

Setting `FINANCEDATABASE_MCP_LOCAL=1` makes the server read the compression files of a local checkout instead, which is useful when testing database changes before they are published.

## Errors and Suggestions
{: .heading-as-h3}

Every tool body runs inside `run_tool()`, which returns failures as text instead of raising, so the model gets a message explaining how to fix the call rather than a bare protocol error.

The most common mistake is a value that is close to, but not, a real one. Asking for `equities(sector="Technology")` returns:

```text
Invalid input for `equities`: The sector 'Technology' is not available in the database. Please check the available sectors using the 'show_options' method.
Did you mean 'Information Technology' instead of 'Technology'?
Available sector values: Communication Services, Consumer Discretionary, Consumer Staples, Energy, Financials, Health Care, Industrials, Information Technology, Materials, Real Estate, Utilities.
```

The first sentence is the package's own validation message. The provider then adds suggestions from `coercion_model.suggest()`, which combines `difflib` close matches (typos such as `Finacials`) with options that contain the value (partial names such as `Technology`). When a filter has 40 values or fewer they are all listed. For larger filters, such as countries or industries, the message gives the count and the exact `show_options` call to list them.

The same approach covers other mistakes: an unknown filter name, an unknown column in `show_columns` and an unknown asset class all return "Did you mean" suggestions with the valid choices.

## Utility Tools
{: .heading-as-h3}

`UtilityToolRegistry` registers three tools that work across asset classes:

- `search_categories`: a Markdown table of the asset classes with their tool name, number of entries, filters and a short description.
- `show_options`: the valid values of one filter for an asset class, optionally narrowed by other filters. For example, the industries of the Health Care sector in Germany. Without a `selection` it gives an overview of every filter.
- `search_instruments`: finds a ticker, name or ISIN across all asset classes at once, with the same ranking as `query`. Each row says which asset class tool holds the full record.

## Transports and Self-Hosting
{: .heading-as-h3}

`stdio` is the default and is what local clients such as Claude Desktop and VS Code use. While a tool runs, anything printed to stdout is redirected to stderr, so the JSON-RPC stream is never corrupted. `streamable-http` and `sse` are available for hosted deployments, configured with `--host` and `--port` or the `MCP_HOST` and `MCP_PORT` environment variables (default `0.0.0.0:8000`).

The repository's `Dockerfile` builds a `python:3.12-slim` image with `uv`, sets `MCP_TRANSPORT=streamable-http` and points `FINANCEDATABASE_CACHE_DIR` at `/data/financedatabase`. Its health check calls `/health`. `docker-compose.yml` adds a named volume for the cache, so a self-hosted server is one command:

```bash
docker compose up -d
```

The server then listens on `http://localhost:8000/mcp`.

The hosted server at `https://financedatabase.jeroenbouma.com/mcp` runs exactly this setup with Docker Compose on a dedicated container, behind Cloudflare, using about 130 MB of memory. It uses streamable HTTP with no API key, OAuth or sign-in.

With `FD_MCP_ANALYTICS=1`, `analytics_model.py` counts tool calls and publishes the totals at `/stats`: calls per day over the last 30 days, calls per tool with average duration, the success rate and uptime. It records no users, IP addresses or arguments. The counts are saved to a JSON file (`FD_MCP_STATS_FILE`, by default in the cache directory) every five calls and on shutdown. The hosted server has this switched on; a local installation does not. See the [privacy policy](https://github.com/JerBouma/FinanceDatabase/blob/main/PRIVACY.md){:target="_blank"} for details.

## Setup Wizard
{: .heading-as-h3}

`setup_model.py` powers both the interactive wizard (`financedatabase-mcp-setup`) and the non-interactive `--client` path. It supports six clients:

| Client | `--client` | Config file |
|:---|:---|:---|
| Claude Desktop | `claude-desktop` | `claude_desktop_config.json` in the platform's Claude folder |
| Claude Code | `claude-code` | `~/.claude.json` |
| VS Code | `vscode` | `.vscode/mcp.json` in the current folder |
| Cursor | `cursor` | `.cursor/mcp.json` in the current folder |
| Gemini CLI | `gemini` | `~/.gemini/settings.json` |
| Windsurf | `windsurf` | `~/.codeium/windsurf/mcp_config.json` |

The wizard writes a `finance-database` entry that starts the server through `uvx --from financedatabase[mcp] financedatabase-mcp`, so nothing needs to be installed first and no environment variables are needed. Other server entries in the file are left untouched. An existing entry is only replaced with `--overwrite` or after confirmation. If a client's config folder doesn't exist, the wizard prints the block to paste instead.

## MCP Bundle
{: .heading-as-h3}

The `mcpb/` folder holds the source of `financedatabase.mcpb`, an [MCP Bundle](https://github.com/modelcontextprotocol/mcpb){:target="_blank"} that installs the server into Claude Desktop with a double-click and no Python setup. The install asks for no API key.

`build-mcpb.sh` regenerates the tool list in `manifest.json` from `config.yaml` and stamps the version from the root `pyproject.toml`. By default the bundle depends on the published PyPI release pinned to that version. With `--local` it builds `financedatabase-local.mcpb` against the local checkout instead, for testing uncommitted changes end to end.

To install the bundle or connect a client, see the [installation section](/projects/financedatabase/mcp#installation) of the main page.
