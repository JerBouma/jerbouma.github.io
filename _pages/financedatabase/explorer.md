---
permalink: /projects/financedatabase/explorer
title: Finance Database Explorer
seo_title: Explorer | Finance Database
excerpt: "Search and filter the Finance Database's equities, ETFs, indices, currencies and cryptocurrencies in your browser, and copy the same selection as Python code."
description: "Search the Finance Database in your browser: filter equities by country, sector, industry and market cap, ETFs by category and family, and indices, currencies and cryptocurrencies, then copy the selection as Python code or download it as CSV."
classes: wide-sidebar
author_profile: false
layout: single
redirect_from:
  - /projects/financedatabase/search
sidebar:
  nav: "financedatabase"
image: /assets/images/projects/FinanceDatabase.jpg
---

Search and filter the Finance Database without installing anything. Pick an asset class, type a ticker, name or ISIN, and narrow it down by country, sector, industry or category. Each dropdown shows how many matches a value would leave, and the bars break the selection down further: click one to filter on it. The Python code button shows the same selection with the `financedatabase` package, and the CSV button downloads it. <span class="fdx-updated"></span>

<div class="fdx-stats" aria-label="The Finance Database in numbers">
  <div class="fdx-stat"><span class="fdx-stat__n" data-stat="countries">110</span><span class="fdx-stat__l">countries</span></div>
  <div class="fdx-stat"><span class="fdx-stat__n" data-stat="exchanges">100+</span><span class="fdx-stat__l">exchanges</span></div>
  <div class="fdx-stat"><span class="fdx-stat__n" data-stat="industries">75</span><span class="fdx-stat__l">industries in 11 sectors</span></div>
  <div class="fdx-stat"><span class="fdx-stat__n" data-stat="etf_families">500+</span><span class="fdx-stat__l">ETF families</span></div>
</div>

<div id="fd-explorer" class="fdx" data-src="{{ '/assets/data/financedatabase/' | relative_url }}" data-version="{{ site.time | date: '%s' }}">
  <div class="fdx-tabs" role="tablist" aria-label="Asset class">
    <button type="button" role="tab" data-class="equities" aria-selected="true">Equities <span class="fdx-tab__count"></span></button>
    <button type="button" role="tab" data-class="etfs" aria-selected="false">ETFs <span class="fdx-tab__count"></span></button>
    <button type="button" role="tab" data-class="indices" aria-selected="false">Indices <span class="fdx-tab__count"></span></button>
    <button type="button" role="tab" data-class="currencies" aria-selected="false">Currencies <span class="fdx-tab__count"></span></button>
    <button type="button" role="tab" data-class="cryptos" aria-selected="false">Cryptocurrencies <span class="fdx-tab__count"></span></button>
  </div>
  <div class="fdx-search"><svg viewBox="0 0 20 20" aria-hidden="true"><circle cx="8.5" cy="8.5" r="5.5"/><path d="M13 13l4 4"/></svg><input type="search" class="fdx-query" data-find placeholder="Ticker, name or ISIN, e.g. ASML or bank" aria-label="Search by ticker, name or ISIN" autocomplete="off" spellcheck="false"></div>
  <div class="fdx-filters"></div>
  <div class="fdx-bar">
    <span class="fdx-count" aria-live="polite"></span>
    <label class="fdx-primary"><input type="checkbox" checked> Only primary listings</label>
    <button type="button" class="fdx-reset" hidden>Clear filters</button>
    <button type="button" class="fdx-python" aria-expanded="false" aria-controls="fdx-code-panel"><i class="fab fa-python" aria-hidden="true"></i> Python code</button>
    <button type="button" class="fdx-download" hidden><i class="fas fa-download" aria-hidden="true"></i> CSV</button>
  </div>
  <div class="fdx-code-panel" id="fdx-code-panel" hidden>
    <p class="fdx-code-lead">The same selection in Python:</p>
    <div class="language-python highlighter-rouge fdx-code"><div class="highlight"><pre class="highlight"><code>import financedatabase as fd</code></pre></div></div>
  </div>
  <p class="fdx-status">Loading…</p>
  <div class="fdx-insights" aria-label="Breakdown of the selection"></div>
  <div class="fdx-table-wrap"></div>
  <button type="button" class="fdx-more" hidden>Show more</button>
</div>

A company is often listed on many exchanges. ASML has 21 listings, from Amsterdam and NASDAQ to Frankfurt, Milan and Mexico City. With "Only primary listings" checked, each company shows up once, under its primary listing (ASML.AS for ASML). Uncheck it to see every listing. The [Getting Started](/projects/financedatabase/getting-started) page explains the `select` and `search` functions, and the [MCP server](/projects/financedatabase/mcp) answers the same questions in plain English from Claude or ChatGPT.

<script src="{{ '/assets/js/fd-explorer.js' | relative_url }}?v={{ site.time | date: '%s' }}" defer></script>
