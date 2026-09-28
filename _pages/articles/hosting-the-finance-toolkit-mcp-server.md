---
title: How I Host the Finance Toolkit MCP Server on a Mini PC
seo_title: "Self-Hosting an MCP Server with Proxmox and Cloudflare"
seo_title_suffix: false
date: 2026-09-28
last_modified_at: 2026-09-28
permalink: /articles/hosting-the-finance-toolkit-mcp-server
excerpt: "The hosted Finance Toolkit MCP server does not run in a cloud data centre. It runs in a small Linux container on a Mini PC at home, managed by Proxmox, with Cloudflare as the only door to the outside world. This article walks through how that setup fits together and why it works well for an MCP server."
description: "How the free Finance Toolkit MCP server is self-hosted on a Mini PC with Proxmox, an LXC container, Docker and Cloudflare, and what it takes to do the same."
layout: single
classes: wide-sidebar article-document
author_profile: false
collection: article
tags: [MCP Server]
share: true
image: /assets/images/projects/FinanceToolkitMCP.jpg
---
When people connect Claude, ChatGPT or Cursor to `https://financetoolkit.jeroenbouma.com/mcp`, they usually assume it runs on a cloud platform somewhere. It does not. The [Finance Toolkit MCP server](/projects/financetoolkit/mcp) runs on a Mini PC at my home, inside a Linux container managed by [Proxmox](https://www.proxmox.com/en/proxmox-virtual-environment/overview){:target="_blank"}, and [Cloudflare](https://www.cloudflare.com){:target="_blank"} handles everything between that container and the internet.

That may sound like a hobby setup for a public service, but an MCP server is an unusually good fit for it. It needs little compute, it holds no user data, and the parts that matter for a public endpoint (TLS, protection against abuse, a stable address) are exactly what Cloudflare already provides for free. This article explains how the pieces fit together and what to think about if you want to host an MCP server of your own.

**The code side of the server (the router pattern behind its 22 tools, the OAuth 2.1 flow and how API keys are handled) is covered on the [Under the Hood](/projects/financetoolkit/mcp/architecture) page. This article is about where and how it runs.**

## Why Not a Cloud Platform?

Cloud platforms are the obvious choice, and the server would run fine on any of them. For this particular workload, though, running it myself has a few clear advantages:

- **The workload is small.** The server does not run a language model. The assistant on the user's side does the reasoning; the server fetches data from [Financial Modeling Prep](/fmp){:target="_blank"} and the OECD and runs pandas calculations on it. That is a few hundred milliseconds of CPU per tool call, which any modern Mini PC handles without noticing.
- **The cost is predictable.** A Mini PC draws only a few watts when idle and already runs other services anyway. A free tool that gets popular on a pay-per-use platform can turn into a bill you did not plan for.
- **Nothing sensitive is stored.** Every user brings their own FMP API key, and that key travels inside a signed token held by their MCP client, not in a database on my side. If the machine disappeared tomorrow, no user data would go with it.
- **Full control.** Updating the server, reading its logs or trying a new version next to the live one is a matter of seconds, not a deployment pipeline.

The trade-off is that I am responsible for uptime and security myself. Most of this article is about how the setup keeps both of those manageable.

## The Setup at a Glance

A request from an assistant to the server passes through four layers:

| Layer | What it does |
|:---|:---|
| **Cloudflare** | Public DNS for `financetoolkit.jeroenbouma.com`, TLS certificates, caching rules, firewall and rate limiting. The only thing the internet talks to. |
| **Proxmox VE** | The hypervisor on the Mini PC. Runs several isolated containers and virtual machines side by side, each with its own resources. |
| **LXC container** | A lightweight Linux container dedicated to the MCP server, so it shares nothing with the other services on the machine. |
| **Finance Toolkit MCP** | The server itself, running the `streamable-http` transport on port 8000 behind Cloudflare. |

The rest of this article goes through these from the inside out.

## The Server: One Docker Image

The Finance Toolkit repository ships a [Dockerfile](https://github.com/JerBouma/FinanceToolkit/blob/main/Dockerfile){:target="_blank"} and a [Docker Compose file](https://github.com/JerBouma/FinanceToolkit/blob/main/docker-compose.yml){:target="_blank"} that run the server in its hosted configuration. The image is deliberately plain: a slim Python base, [uv](https://docs.astral.sh/uv/){:target="_blank"} to install the locked dependencies, and a few environment variables that switch the server from its default local mode to hosted mode:

```yaml
services:
  finance-toolkit-mcp:
    build: .
    restart: unless-stopped
    ports:
      - "8000:8000"
    environment:
      MCP_TRANSPORT: streamable-http
      MCP_HOST: "0.0.0.0"
      MCP_PORT: "8000"
      FT_MCP_SECRET_KEY: "${FT_MCP_SECRET_KEY}"
    volumes:
      - ft_cache:/root/.config/financetoolkit
    healthcheck:
      test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 15s

volumes:
  ft_cache:
```

Three settings do most of the work:

- **`MCP_TRANSPORT=streamable-http`** turns the server from a local stdio process into a web service. It also switches on the OAuth routes and the middleware that requires a valid token on `/mcp`.
- **`FT_MCP_SECRET_KEY`** is the secret used to sign every OAuth token. It belongs in an environment file on the host, never in the repository. If it changes, every issued token becomes invalid and users have to log in again, so it is set once and left alone.
- **The `/health` endpoint** gives Docker a way to check the server is actually answering, not just running. `restart: unless-stopped` brings it back after a crash or a reboot of the Mini PC.

Hosted mode also changes one behaviour on purpose: caching is off by default. Locally, the server caches downloaded data in a small SQLite database because there is only one user. On a shared server that would mean one user's data, fetched with their own paid FMP plan, could be served to someone else. So the hosted server fetches everything live, per request, with the caller's own key.

You can run this image on any machine with Docker and have your own copy of the server in a few minutes:

```bash
git clone https://github.com/JerBouma/FinanceToolkit.git
cd FinanceToolkit
FT_MCP_SECRET_KEY=$(openssl rand -hex 32) docker compose up -d
curl http://localhost:8000/health
```

## Proxmox: One Container Per Service

[Proxmox VE](https://www.proxmox.com/en/proxmox-virtual-environment/overview){:target="_blank"} turns the Mini PC into a small server that runs many isolated machines at once. It is free, open source and managed through a web interface, which makes it popular for home servers.

Proxmox offers two kinds of guests: full virtual machines and LXC containers. Containers share the host's kernel, so they start in seconds and use far less memory than a virtual machine, while still being isolated from each other with their own file system, network address and resource limits. For a Python web service that is the right trade-off, and the MCP server has its own container that runs nothing else.

That separation pays off in a few ways:

- **Isolation.** The MCP server is the only public-facing service in its container. Whatever happens inside it, it cannot touch the other containers on the machine.
- **Resource limits.** The container gets a fixed share of CPU cores and memory. A burst of heavy requests slows the MCP server down, but it cannot starve anything else on the host.
- **Snapshots and backups.** Proxmox can snapshot a container before an upgrade, so a version that misbehaves is rolled back in one click, and scheduled backups are built in.

## Cloudflare: The Only Way In

The container is never exposed to the internet directly. The DNS record for `financetoolkit.jeroenbouma.com` is proxied through Cloudflare, so every request lands on Cloudflare's network first and only then reaches the Mini PC. You can see this in the response headers of any request, for example the health check:

```bash
curl -sI https://financetoolkit.jeroenbouma.com/health
```

```
HTTP/2 200
content-type: application/json
server: cloudflare
cf-cache-status: DYNAMIC
```

Putting Cloudflare in front does several jobs that would otherwise be my problem:

- **TLS.** Cloudflare terminates HTTPS with a certificate it renews itself. MCP clients require HTTPS for remote servers and for OAuth, so this matters.
- **No open ports at home.** With a [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/){:target="_blank"}, a small `cloudflared` agent next to the service opens an outbound connection to Cloudflare, and Cloudflare sends traffic back through it. Nothing on the home router needs to be forwarded, and the home IP address is never published.
- **Protection.** Cloudflare's firewall and rate limiting stop floods and obvious abuse before they reach the Mini PC, which has far less capacity than Cloudflare's edge.
- **No caching of answers.** Every MCP call is personal (it runs with the caller's own API key), so nothing on `/mcp` may be cached. Cloudflare leaves these requests alone and passes them straight through, which is what the `cf-cache-status: DYNAMIC` header above confirms.

One detail that is easy to miss: the MCP protocol with `streamable-http` keeps some responses open while the server streams results back. Cloudflare supports this, but an aggressive timeout or a buffering proxy rule in between would break long tool calls. The default Cloudflare settings work without changes.

## How a Request Travels

Putting it all together, this is what happens when someone asks Claude for Apple's operating margin:

1. Claude decides to call the `profitability` tool and sends an MCP request to `https://financetoolkit.jeroenbouma.com/mcp`, with the user's access token in the `Authorization` header.
2. Cloudflare receives the request at its nearest data centre, checks it against the firewall rules and forwards it to the Mini PC.
3. Inside the container, the server verifies the token's signature with `FT_MCP_SECRET_KEY` and extracts the user's FMP API key from it.
4. The server calls Financial Modeling Prep with that key, runs the Finance Toolkit calculation and formats the result as a Markdown table.
5. The answer travels back the same way, and the key is forgotten as soon as the request is done.

The first time a user connects, the server has no token for them yet. It answers `/mcp` with a `401` and points the client to its OAuth metadata, which Cloudflare passes through like any other request:

```bash
curl -s https://financetoolkit.jeroenbouma.com/.well-known/oauth-authorization-server
```

The client then opens the login page, the user enters their FMP key once, and from then on every request carries the signed token. The [Under the Hood](/projects/financetoolkit/mcp/architecture#oauth-21-and-api-key-resolution) page covers that flow step by step.

## Keeping It Running

A public service on home hardware needs a little discipline:

- **Health checks at every layer.** A restart policy brings the server back when `/health` stops answering, Proxmox can start the container automatically when the Mini PC boots, and an external uptime check on the public `/health` URL catches anything broken between Cloudflare and the container.
- **Updates in a copy first.** Proxmox makes it cheap to clone the container, try a new Finance Toolkit release there and only then swap it in. A snapshot keeps the switch reversible.
- **Secrets outside the image.** The signing secret stays in an environment file, so the image itself can be rebuilt from the public repository at any time.
- **Accept that it is not a data centre.** A power cut or an internet outage at home takes the server down. For a free tool that is an acceptable risk, and anyone who needs guaranteed availability can run the [local server](/projects/financetoolkit/mcp#local-clients) or the Docker image on their own infrastructure.

## Doing This Yourself

Nothing here is specific to the Finance Toolkit. Any MCP server that supports an HTTP transport can be hosted the same way:

1. Install Proxmox on a spare PC or Mini PC and create an LXC container for the server.
2. Install Docker in the container and run the server with its HTTP transport, bound to a port inside the container.
3. Add a domain to Cloudflare and connect the container to it, ideally with a Cloudflare Tunnel so no ports need to be opened on your router.
4. Make sure the server's `/health` (or equivalent) endpoint works through the public URL, and point your MCP client at it.

If you do not want to host anything at all, the hosted server is free to use. The [Finance Toolkit MCP server](/projects/financetoolkit/mcp) page has setup steps for Claude, ChatGPT, Cursor, VS Code, Windsurf, Codex CLI and Gemini CLI, and [How to Connect Claude to Live Financial Data](/articles/connect-claude-to-financial-data) walks through a first session. The server's source code, including the Docker files used here, is on [GitHub](https://github.com/JerBouma/FinanceToolkit){:target="_blank"}.
