---
permalink: /projects/financetoolkit/mcp/architecture
title: Finance Toolkit MCP Architecture
seo_title: Finance Toolkit MCP Server Architecture
excerpt: "How the Finance Toolkit MCP server is built: the router pattern that packs 600+ methods into 25 categorical tools, the startup sequence, dispatch categories, OAuth 2.1 with PKCE and API key handling."
description: "How the open-source Finance Toolkit MCP server works: the router pattern behind its 25 categorical tools, startup sequence, OAuth 2.1 and API key handling."
classes: wide-sidebar
author_profile: false
layout: single
last_modified_at: 2026-09-11
redirect_from:
  - /projects/financetoolkit/mcp-architecture
sidebar:
  nav: "financetoolkit-mcp"
image: /assets/images/projects/FinanceToolkitMCP.jpg
---

<div class="page-header-action notebook-viewer-actions"><a href="https://github.com/JerBouma/FinanceToolkit/tree/main/financetoolkit/mcp_server" target="_blank" rel="noopener"><i class="fab fa-github"></i> View on GitHub</a></div>

The MCP server lives entirely inside `financetoolkit/mcp_server/` and is structured around a **router pattern**: rather than exposing every one of the 600+ Finance Toolkit methods as a separate MCP tool (which would overwhelm an LLM's tool list), the server groups them into 25 categorical master tools. Each master tool accepts an `indicator` parameter that selects the exact metric at call time.

**For developers.** If you just want to use the Finance Toolkit through your assistant, the [Finance Toolkit MCP Server](/projects/financetoolkit/mcp) page covers installation, example prompts and the available tools. Everything below is implementation detail for those who want to extend or contribute to the server.
{: .notice--info}

## Module Overview
{: .heading-as-h3}

| Module | Role |
|:---|:---|
| `mcp_controller.py` | Entry points (`main`, `setup`, `inspector`), config loading, server assembly, transport wiring |
| `auth_model.py` | Per-request FMP API key resolution, token encryption and verification, OAuth 2.1 routes, HTTP auth middleware |
| `registry_controller.py` | Builds and registers the categorical router tools on the FastMCP instance |
| `inspection_controller.py` | Static introspection of controller classes: method discovery and signature building |
| `provider_model.py` | Routes tool calls to the correct Finance Toolkit module; manages Toolkit instance caching |
| `cache_model.py` | Thread-safe SQLite cache for DataFrame results with TTL-based eviction |
| `tools_model.py` | Registers the three built-in search tools (categories, metrics per category, metric search) |
| `formatting_model.py` | Converts any Finance Toolkit result (DataFrame, Series, dict, scalar) to compact JSON, applies `limit` and `show_columns`, and cuts oversized answers to their most recent rows |
| `coercion_model.py` | Best-effort type coercion for string values arriving from LLMs |
| `setup_model.py` | Interactive and CLI setup wizard: writes client configs |

## Startup Sequence
{: .heading-as-h3}

When the server process starts (`uvx … financetoolkit-mcp`), `mcp_controller._build_mcp_app()` runs the following steps in order:

1. **Load environment**: resolves the FMP API key from the process environment, a local `.env` file, or the global Finance Toolkit config path (`~/.config/financetoolkit/.env`). When the key is already present in the environment (e.g. injected by the client's `env` block) the file lookup is skipped entirely.
2. **Read `config.yaml`**: a single YAML file in the same package directory drives all registration: which controller classes exist (`module_class_map`), which methods to skip (`skip_methods`), which parameters the wrapper always handles (`init_handled_params`), and the full ordered list of tool groups (`tool_groups`).
3. **Instantiate subsystems**: a `ToolkitProvider` (with its `SQLiteCache`), a `ControllerInspector`, a `ToolRegistry`, and a `UtilityToolRegistry` are all constructed and wired together.
4. **Register tools**: `ToolRegistry.register_all_tools()` registers the router groups, then `UtilityToolRegistry.register_all_tools()` registers the utility tools.
5. **Register OAuth routes**: `register_auth_routes(mcp)` attaches the OAuth 2.1 endpoints and the `/health` route to the FastMCP instance.
6. **Start transport**: the `MCP_TRANSPORT` environment variable selects the runtime mode. `stdio` (the default) is used for local clients; `sse` and `streamable-http` are used for hosted deployments. For HTTP transports, `MCPAuthMiddleware` and `CORSMiddleware` are layered onto the Starlette app before Uvicorn starts. The server listens on `MCP_HOST`, which defaults to `127.0.0.1` (this computer only), and behind a reverse proxy `FORWARDED_ALLOW_IPS` names the proxies whose forwarded headers it trusts. A hosted server also answers a call with a timeout after 180 seconds and lets each user (an API key) run at most three calls at a time.

## The Router Pattern
{: .heading-as-h3}

`ToolRegistry` reads the `tool_groups` list from `config.yaml`. Each entry is converted to a `RouterGroupSpec` NamedTuple that describes one master tool: its name, the controller class to introspect, and how methods are discovered.

For each group, `ControllerInspector` either:
- **Parses the source** of a nominated `collect_*` method on the controller class to find every `self.get_*()` call in the order they appear, or
- **Falls back** to an alphabetical scan of all `get_` methods on the class.

This produces an ordered list of indicator names. `_build_router_wrapper()` then constructs a single `wrapper(**kwargs)` closure that:

1. Reads the `indicator` argument and matches it to the method list (with fuzzy-match suggestions on typos).
2. Coerces all typed parameters from strings via `coercion_model.coerce_value()`.
3. Validates required inputs (`tickers` for equity tools, date formats).
4. Delegates to `ToolkitProvider.call_method()`.
5. Passes the result through `formatting_model.format_result()` and returns compact JSON, with `_notes` on anything left out, ignored, assumed or converted.

The wrapper's `__signature__` is replaced with a proper `inspect.Signature` so that FastMCP can introspect it and generate accurate JSON Schema for the LLM. Each parameter's description comes from the docstrings of the methods behind the tool, so the assistant reads the same explanation as the documentation.

## Dispatch Categories
{: .heading-as-h3}

Every tool group has a `category` that controls how `ToolkitProvider` routes the call:

| Category | Behavior |
|:---|:---|
| `ticker` | Instantiates a `Toolkit(tickers=…)` object and calls a method on one of its sub-modules (e.g. `ratios`, `models`, `options`) |
| `toolkit` | Same Toolkit instance, but calls a method directly on the `Toolkit` class (e.g. `get_historical_data`) |
| `standalone` | Instantiates `Economics` or `FixedIncome` directly, no tickers required |
| `discovery` | Instantiates `Discovery(api_key=…)`, no tickers or dates required |
| `mixed` | Per-method routing table: each indicator maps to its own `(module, category)` pair |

`ToolkitProvider` caches `Toolkit` instances by a key derived from tickers, date range, quarterly flag, and a hash of the API key, so repeated calls for the same parameters reuse an existing instance. Standalone module instances are cached the same way. The provider keeps at most 64 `Toolkit` instances and 4 `Economics`, `FixedIncome` and `Discovery` instances, and drops the least recently used one first; an `Economics` instance holds the Global Macro Database, so one copy of that dataset is shared per process. Full DataFrame results are written to and read from `SQLiteCache` with configurable TTL.

## OAuth 2.1 and API Key Resolution
{: .heading-as-h3}

This section is only relevant for **hosted deployments** that run the server over an HTTP transport (`MCP_TRANSPORT=sse` or `MCP_TRANSPORT=streamable-http`). For local clients running over stdio the API key comes from the environment and no OAuth handshake is needed.

### Why OAuth at all?
{: .heading-as-h4}

When the server is hosted at a remote URL, MCP clients (Claude Desktop, VS Code, Cursor, …) need a standard way to authenticate without the user manually pasting credentials into a config file. The MCP specification defines an OAuth 2.1 profile for exactly this purpose. The Finance Toolkit server implements that profile in full, including the PKCE extension that protects against authorization code interception.

The server carries **no user database**: it never writes the FMP API key to disk. Instead, the key is sealed inside an encrypted token that the client holds and sends with every request.

### The OAuth Flow Step by Step
{: .heading-as-h4}

The complete flow from first connection to authorized tool call:

1. **Discovery:** The MCP client connects to `/mcp` or `/sse` without a token. `MCPAuthMiddleware` returns HTTP 401 with a `WWW-Authenticate: Bearer resource_metadata="…/.well-known/oauth-protected-resource"` header. The client fetches that URL to learn the authorization server location, then fetches `/.well-known/oauth-authorization-server` for the full OAuth metadata (authorization endpoint, token endpoint, PKCE methods, scopes).

2. **Dynamic client registration:** The client POSTs its `client_name` and `redirect_uris` to `/oauth/register`. The server returns a `client_id` that holds the name and redirect URIs, signed with a key derived from the server secret, so registration stores nothing and the redirect URIs cannot be swapped: an authorization only goes back to one of the client's own URIs.

3. **Authorization request:** The client generates a PKCE `code_verifier` (a cryptographically random string) and derives `code_challenge = BASE64URL(SHA-256(code_verifier))`. It redirects the user's browser to `/oauth/authorize?client_id=…&redirect_uri=…&code_challenge=…&code_challenge_method=S256&state=…`.

4. **User consent:** The server renders a branded HTML page asking for the user's FMP API key. The user enters the key and clicks "Authorize". The form POSTs to `/oauth/authorize`.

5. **Authorization code issuance:** The server keeps the FMP key, `client_id`, `redirect_uri`, `code_challenge` and `code_challenge_method` in memory under a random, single-use authorization code that expires after 5 minutes. The browser is redirected to `redirect_uri?code=<code>&state=<state>`.

6. **Token exchange:** The client POSTs to `/oauth/token` with `grant_type=authorization_code`, the `code`, and the original `code_verifier`. The server: (a) takes the code out of memory, so it works only once and only before it expires, (b) checks that `client_id` and `redirect_uri` match the authorization, and (c) validates PKCE by computing `BASE64URL(SHA-256(code_verifier))` and comparing it with the stored `code_challenge` using a constant-time `hmac.compare_digest`. If all checks pass, the server issues an access token that lasts 24 hours and a refresh token that lasts 90 days. Both hold the FMP key (and the FRED key, when given) encrypted. When the access token expires, the client POSTs `grant_type=refresh_token` and receives a new pair, so a client in use stays signed in.

7. **Authorized requests:** The client sends every subsequent MCP request with an `Authorization: Bearer <access_token>` header. `MCPAuthMiddleware` intercepts the request, calls `get_api_key_from_request()`, which decrypts the token, checks that it is an access token that has not expired, and reads the FMP key from it. The key is then available to `ToolkitProvider.call_method()` via `resolve_api_key()` for the lifetime of that request only. Nothing is written to disk.

### Token Encryption
{: .heading-as-h4}

The access and refresh tokens are encrypted with Fernet (AES-128-CBC with an HMAC-SHA256) under a key derived from the server secret, so a token that shows up in a log, a proxy or another client does not reveal the keys. The secret is loaded from the `FT_MCP_SECRET_KEY` environment variable if set, or generated on first run and kept in `~/.config/financetoolkit/.mcp_secret`. Rotating it ends every token at once.

### API Key Resolution Order
{: .heading-as-h4}

`resolve_api_key()` checks the following sources in priority order for every tool call:

| Priority | Source | Used when |
|:---|:---|:---|
| 1 | `x-fmp-api-key` / `x-financial-modeling-prep-api-key` header | Direct header injection (advanced clients) |
| 2 | `Authorization: Bearer <token>` header | Standard OAuth access token (holds the FMP key, encrypted) |
| 3 | `fmp_api_key` / `api_key` / `fmp_key` query parameter | Query-string access (fallback) |
| 4 | `FINANCIAL_MODELING_PREP_API_KEY` env var | Local stdio transport or server-wide default |

When an access token is found in any of these positions, it is decrypted and its expiry checked before the key is read. An expired or invalid token is answered with a 401 so the client signs in again, and is never passed on as a key. Any other string is accepted as a bare API key. The env-var path is checked last so that a per-request key from an OAuth flow always takes precedence.

The optional FRED key follows the same pattern through `resolve_fred_api_key()`: the `x-fred-api-key` header, a `fred_api_key` claim on the bearer token, a `fred_api_key` / `fred_key` query parameter, and finally the `FRED_API_KEY` environment variable as the server-wide fallback. It is resolved per request and passed to the Economics and Fixed Income modules; when it is absent those modules simply skip the handful of FRED-backed indicators and everything else continues to work.

### Security Properties
{: .heading-as-h4}

- **No server-side credential storage**: the FMP API key lives only in the user's browser during the consent step, in memory for the at most 5 minutes until the authorization code is exchanged, and in the encrypted access token (24 hours) and refresh token (90 days) held by the MCP client. The server never writes it to a database or log.
- **PKCE (S256)**: prevents an attacker who intercepts the authorization code redirect from exchanging the code for a token, because they do not have the `code_verifier` that only the originating client holds.
- **Encrypted tokens**: tokens are encrypted and authenticated, so a forged or tampered token is rejected before any key is read, and a token in a log reveals nothing. An access token only works as an access token and a refresh token only as a refresh token.
- **Constant-time comparison**: `hmac.compare_digest` is used for PKCE validation and for the signed `client_id`, removing timing side-channels.
- **Endpoint isolation**: `MCPAuthMiddleware` only protects `/sse`, `/messages`, and `/mcp`. The discovery endpoints (`/.well-known/*`), OAuth routes (`/oauth/*`), and `/health` are always open so clients can complete the authorization flow without a chicken-and-egg problem.
- **stdio is unaffected**: all of the above is bypassed entirely for local stdio clients. The FMP key is read once at startup from the process environment and never touches the HTTP layer.

## Utility Tools
{: .heading-as-h3}

`UtilityToolRegistry` registers three tools that operate on the tool index rather than routing to a controller:

- `search_metric_categories`: lists all registered categories and the number of tools in each.
- `search_by_category`: lists every indicator within a given category.
- `search_metrics`: ranks individual indicators, not tools, and returns the tool together with the indicator name. It understands analyst wording ("how expensive is the stock", "bankruptcy risk", "option greeks"), abbreviations such as P/E and VaR, and typos.

Looking up a ticker by name or ISIN is not part of this server: the [Finance Database MCP server](/projects/financedatabase/mcp) does that. When a client connects, the server sends instructions that point the assistant to `search_metrics` first.

## Setup Wizard
{: .heading-as-h3}

`setup_model.py` powers both the interactive wizard (`financetoolkit-mcp-setup`) and the non-interactive `--client` CLI path. It locates and merges the `finance-toolkit` MCP entry into each client's JSON config file without disturbing other server entries, and writes the FMP API key to `~/.config/financetoolkit/.env`.
