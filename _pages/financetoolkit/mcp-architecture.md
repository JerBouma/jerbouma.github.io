---
permalink: /projects/financetoolkit/mcp/architecture
title: Finance Toolkit MCP Architecture
seo_title: Finance Toolkit MCP Server Architecture
excerpt: "How the Finance Toolkit MCP server is built: the router pattern that packs 500+ methods into 22 tools, the startup sequence, dispatch categories, OAuth 2.1 with PKCE and API key handling."
description: "How the open-source Finance Toolkit MCP server works: the router pattern behind its 22 tools, startup sequence, OAuth 2.1 and API key handling."
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

The MCP server lives entirely inside `financetoolkit/mcp_server/` and is structured around a **router pattern**: rather than exposing every one of the 500+ Finance Toolkit methods as a separate MCP tool (which would overwhelm an LLM's tool list), the server groups them into 22 categorical master tools. Each master tool accepts an `indicator` parameter that selects the exact metric at call time.

**For developers.** If you just want to use the Finance Toolkit through your assistant, the [Finance Toolkit MCP Server](/projects/financetoolkit/mcp) page covers installation, example prompts and the available tools. Everything below is implementation detail for those who want to extend or contribute to the server.
{: .notice--info}

## Module Overview
{: .heading-as-h3}

| Module | Role |
|:---|:---|
| `mcp_controller.py` | Entry points (`main`, `setup`, `inspector`), config loading, server assembly, transport wiring |
| `auth_model.py` | Per-request FMP API key resolution, JWT signing/verification, OAuth 2.1 routes, HTTP auth middleware |
| `registry_controller.py` | Builds and registers the categorical router tools on the FastMCP instance |
| `inspection_controller.py` | Static introspection of controller classes: method discovery and signature building |
| `provider_model.py` | Routes tool calls to the correct Finance Toolkit module; manages Toolkit instance caching |
| `cache_model.py` | Thread-safe SQLite cache for DataFrame results with TTL-based eviction |
| `tools_model.py` | Registers the four built-in utility tools (list, search, instrument lookup) |
| `formatting_model.py` | Converts any Finance Toolkit result (DataFrame, Series, dict, scalar) to Markdown |
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
6. **Start transport**: the `MCP_TRANSPORT` environment variable selects the runtime mode. `stdio` (the default) is used for local clients; `sse` and `streamable-http` are used for hosted deployments. For HTTP transports, `MCPAuthMiddleware` and `CORSMiddleware` are layered onto the Starlette app before Uvicorn starts.

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
5. Passes the result through `formatting_model.format_result()` and returns a Markdown string.

The wrapper's `__signature__` is replaced with a proper `inspect.Signature` so that FastMCP can introspect it and generate accurate JSON Schema for the LLM.

## Dispatch Categories
{: .heading-as-h3}

Every tool group has a `category` that controls how `ToolkitProvider` routes the call:

| Category | Behaviour |
|:---|:---|
| `ticker` | Instantiates a `Toolkit(tickers=…)` object and calls a method on one of its sub-modules (e.g. `ratios`, `models`, `options`) |
| `toolkit` | Same Toolkit instance, but calls a method directly on the `Toolkit` class (e.g. `get_historical_data`) |
| `standalone` | Instantiates `Economics` or `FixedIncome` directly, no tickers required |
| `discovery` | Instantiates `Discovery(api_key=…)`, no tickers or dates required |
| `mixed` | Per-method routing table: each indicator maps to its own `(module, category)` pair |

`ToolkitProvider` caches `Toolkit` instances by a key derived from tickers, date range, quarterly flag, and a hash of the API key, so repeated calls for the same parameters reuse an existing instance. Standalone module instances are cached the same way. Full DataFrame results are written to and read from `SQLiteCache` with configurable TTL.

## OAuth 2.1 and API Key Resolution
{: .heading-as-h3}

This section is only relevant for **hosted deployments** that run the server over an HTTP transport (`MCP_TRANSPORT=sse` or `MCP_TRANSPORT=streamable-http`). For local clients running over stdio the API key comes from the environment and no OAuth handshake is needed.

### Why OAuth at all?
{: .heading-as-h4}

When the server is hosted at a remote URL, MCP clients (Claude Desktop, VS Code, Cursor, …) need a standard way to authenticate without the user manually pasting credentials into a config file. The MCP specification defines an OAuth 2.1 profile for exactly this purpose. The Finance Toolkit server implements that profile in full, including the PKCE extension that protects against authorization code interception.

Crucially, the server carries **no persistent user database**: it never stores the FMP API key on disk or in memory beyond the lifetime of a single request. Instead, the key is sealed inside a cryptographically signed JWT that travels with the request.

### The OAuth Flow Step by Step
{: .heading-as-h4}

The complete flow from first connection to authorized tool call:

1. **Discovery:** The MCP client connects to `/mcp` or `/sse` without a token. `MCPAuthMiddleware` returns HTTP 401 with a `WWW-Authenticate: Bearer resource_metadata="…/.well-known/oauth-protected-resource"` header. The client fetches that URL to learn the authorization server location, then fetches `/.well-known/oauth-authorization-server` for the full OAuth metadata (authorization endpoint, token endpoint, PKCE methods, scopes).

2. **Dynamic client registration:** The client POSTs its `client_name` and `redirect_uris` to `/oauth/register`. The server issues a random `client_id` without storing anything server-side; the client holds onto it for the rest of the flow.

3. **Authorization request:** The client generates a PKCE `code_verifier` (a cryptographically random string) and derives `code_challenge = BASE64URL(SHA-256(code_verifier))`. It redirects the user's browser to `/oauth/authorize?client_id=…&redirect_uri=…&code_challenge=…&code_challenge_method=S256&state=…`.

4. **User consent:** The server renders a branded HTML page asking for the user's FMP API key. The user enters the key and clicks "Authorize". The form POSTs to `/oauth/authorize`.

5. **Authorization code issuance:** The server bundles the FMP key, `client_id`, `redirect_uri`, `code_challenge`, and `code_challenge_method` into a JWT payload, signs it with HMAC-SHA256 using the server secret, and sets a 5-minute expiry. The resulting signed token is the authorization code. The browser is redirected to `redirect_uri?code=<jwt>&state=<state>`.

6. **Token exchange:** The client POSTs to `/oauth/token` with `grant_type=authorization_code`, the `code` JWT, and the original `code_verifier`. The server: (a) verifies the JWT signature and expiry, (b) checks `client_id` and `redirect_uri` match what is in the code payload, and (c) validates PKCE by computing `BASE64URL(SHA-256(code_verifier))` and comparing it with the `code_challenge` stored in the code using a constant-time `hmac.compare_digest`. If all checks pass, the server issues a long-lived access token: another HMAC-SHA256 JWT containing the FMP key, this time with a one-year expiry.

7. **Authorized requests:** The client sends every subsequent MCP request with an `Authorization: Bearer <access_token>` header. `MCPAuthMiddleware` intercepts the request, calls `get_api_key_from_request()`, which calls `verify_jwt()` to check the signature and expiry, and extracts the FMP key from the token payload. The key is then available to `ToolkitProvider.call_method()` via `resolve_api_key()` for the lifetime of that request only. Nothing is written to disk.

### JWT Signing
{: .heading-as-h4}

The server generates and verifies all JWTs itself using a 256-bit HMAC-SHA256 secret. The secret is loaded from the `FT_MCP_SECRET_KEY` environment variable if set, or automatically generated on first run and persisted to `~/.config/financetoolkit/.mcp_secret`. All comparisons use `hmac.compare_digest` to prevent timing attacks.

### API Key Resolution Order
{: .heading-as-h4}

`resolve_api_key()` checks the following sources in priority order for every tool call:

| Priority | Source | Used when |
|:---|:---|:---|
| 1 | `x-fmp-api-key` / `x-financial-modeling-prep-api-key` header | Direct header injection (advanced clients) |
| 2 | `Authorization: Bearer <token>` header | Standard OAuth access token (JWT containing the FMP key) |
| 3 | `fmp_api_key` / `api_key` / `fmp_key` query parameter | Query-string access (fallback) |
| 4 | `FINANCIAL_MODELING_PREP_API_KEY` env var | Local stdio transport or server-wide default |

When a JWT is found in any of these positions, `verify_jwt()` validates the signature and expiry before extracting the key. A raw (non-JWT) string is accepted as a bare API key. The env-var path is checked last so that a per-request key from an OAuth flow always takes precedence.

The optional FRED key follows the same pattern through `resolve_fred_api_key()`: the `x-fred-api-key` header, a `fred_api_key` claim on the bearer token, a `fred_api_key` / `fred_key` query parameter, and finally the `FRED_API_KEY` environment variable as the server-wide fallback. It is resolved per request and passed to the Economics and Fixed Income modules; when it is absent those modules simply skip the handful of FRED-backed indicators and everything else continues to work.

### Security Properties
{: .heading-as-h4}

- **No server-side credential storage**: the FMP API key lives only in the user's browser during the consent step, in the short-lived authorization code JWT (5 minutes), and in the long-lived access token JWT (1 year) held by the MCP client. The server never writes it to a database or log.
- **PKCE (S256)**: prevents an attacker who intercepts the authorization code redirect from exchanging the code for a token, because they do not have the `code_verifier` that only the originating client holds.
- **Signed tokens**: HMAC-SHA256 signatures mean forged or tampered tokens are rejected before any key is extracted.
- **Constant-time comparison**: `hmac.compare_digest` is used for both PKCE validation and JWT signature verification, removing timing side-channels.
- **Endpoint isolation**: `MCPAuthMiddleware` only protects `/sse`, `/messages`, and `/mcp`. The discovery endpoints (`/.well-known/*`), OAuth routes (`/oauth/*`), and `/health` are always open so clients can complete the authorization flow without a chicken-and-egg problem.
- **stdio is unaffected**: all of the above is bypassed entirely for local stdio clients. The FMP key is read once at startup from the process environment and never touches the HTTP layer.

## Utility Tools
{: .heading-as-h3}

`UtilityToolRegistry` registers four tools that operate on the tool index rather than routing to a controller:

- `search_categories`: returns a Markdown table of all registered categories and tool counts.
- `search_by_category`: lists every indicator within a given category.
- `search_metrics`: token-based fuzzy search across all tool names and descriptions, with typo tolerance via `difflib.get_close_matches`.
- `search_instruments`: proxies a live `Discovery.search_instruments()` call for ticker/ISIN/name lookups.

## Setup Wizard
{: .heading-as-h3}

`setup_model.py` powers both the interactive wizard (`financetoolkit-mcp-setup`) and the non-interactive `--client` CLI path. It locates and merges the `finance-toolkit` MCP entry into each client's JSON config file without disturbing other server entries, and writes the FMP API key to `~/.config/financetoolkit/.env`.
