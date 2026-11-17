---
title: "Cryptocurrencies"
permalink: /projects/financedatabase/docs/cryptos
seo_title: "Cryptocurrencies | Finance Database"
seo_title_suffix: false
excerpt: "Select and search cryptocurrencies by coin and quote currency with the Finance Database in Python, with examples and their output."
description: "Select and search cryptocurrencies by coin and quote currency with the Finance Database in Python, with examples and their output."
classes: wide-sidebar
author_profile: false
layout: single
sidebar:
  nav: "financedatabase"
image: /assets/images/projects/FinanceDatabase.jpg
---

<div class="page-header-action notebook-viewer-actions"><a href="/projects/financedatabase/explorer?class=cryptos"><i class="fas fa-magnifying-glass"></i> Database Explorer</a><a href="https://github.com/JerBouma/FinanceDatabase" target="_blank" rel="noopener"><i class="fab fa-github"></i> View on GitHub</a></div>

Cryptocurrencies, selectable by coin and the currency they are quoted in. The symbols follow Yahoo Finance, such as BTC-USD; the Finance Toolkit writes them without the dash (BTCUSD). To browse them without code, open the cryptocurrencies in the [Database Explorer](/projects/financedatabase/explorer?class=cryptos).

## select

Select cryptocurrencies based on the cryptocurrency and the currency it is quoted in.

Returns all cryptocurrencies when no input is given.

`cryptos.select` accepts the following parameters:

<div class="docs-params"><div class="docs-params__table"><table>
<thead><tr><th>Parameter</th><th>Type</th><th>Description</th><th>Default</th></tr></thead>
<tbody>
<tr><td><code>cryptocurrency</code></td><td><code>str | list</code></td><td>Cryptocurrencies to filter on.</td><td></td></tr>
<tr><td><code>currency</code></td><td><code>str | list</code></td><td>Currencies to filter on.</td><td></td></tr>
<tr><td><code>as_pandas</code></td><td><code>bool</code></td><td>Return pandas, else Polars. Defaults to True.</td><td><code>True</code></td></tr>
</tbody>
</table></div></div>

**Returns:** FinanceFrame | pl.DataFrame: The cryptocurrencies matching every filter.

As an example:

```python
import financedatabase as fd

cryptos = fd.Cryptos()

cryptos.select(cryptocurrency="ETH")[["name", "cryptocurrency", "currency", "exchange"]]
```

Which returns:

| symbol   | name         | cryptocurrency   | currency   | exchange   |
|:---------|:-------------|:-----------------|:-----------|:-----------|
| ETH-BTC  | Ethereum BTC | ETH              | BTC        | CCC        |
| ETH-CAD  | Ethereum CAD | ETH              | CAD        | CCC        |
| ETH-EUR  | Ethereum EUR | ETH              | EUR        | CCC        |
| ETH-GBP  | Ethereum GBP | ETH              | GBP        | CCC        |
| ETH-INR  | Ethereum INR | ETH              | INR        | CCC        |
| ETH-JPY  | Ethereum JPY | ETH              | JPY        | CCC        |
| ETH-KRW  | Ethereum KRW | ETH              | KRW        | CCC        |
| ETH-RUB  | Ethereum RUB | ETH              | RUB        | CCC        |
| ETH-USD  | Ethereum USD | ETH              | USD        | CCC        |

---

## search

Search columns with regular expressions; a list of queries matches any of them.

`cryptos.search` accepts the following parameters:

<div class="docs-params"><div class="docs-params__table"><table>
<thead><tr><th>Parameter</th><th>Type</th><th>Description</th><th>Default</th></tr></thead>
<tbody>
<tr><td><code>**kwargs</code></td><td><code>str | list</code></td><td>Column names and search queries, e.g. symbol=&quot;TSLA&quot;.</td><td></td></tr>
<tr><td><code>case_sensitive</code></td><td><code>bool</code></td><td>Case-sensitive search. Defaults to False.</td><td><code>False</code></td></tr>
<tr><td><code>only_primary_listing</code></td><td><code>bool</code></td><td>Only primary listings. Defaults to False.</td><td><code>False</code></td></tr>
<tr><td><code>index</code></td><td><code>str</code></td><td>Search within the DataFrame index. Defaults to None.</td><td><code>None</code></td></tr>
<tr><td><code>exclude_delisted</code></td><td><code>bool</code></td><td>Exclude delisted entries. Defaults to True.</td><td><code>True</code></td></tr>
<tr><td><code>as_pandas</code></td><td><code>bool</code></td><td>Return pandas, else Polars. Defaults to True.</td><td><code>True</code></td></tr>
</tbody>
</table></div></div>

**Returns:** pd.DataFrame | pl.DataFrame: The rows matching every query.

To find Solana in every currency it is quoted in:

```python
import financedatabase as fd

cryptos = fd.Cryptos()

cryptos.search(name="Solana")[["name", "cryptocurrency", "currency", "exchange"]].head(10)
```

Which returns:

| symbol   | name       | cryptocurrency   | currency   | exchange   |
|:---------|:-----------|:-----------------|:-----------|:-----------|
| SOL-ETH  | Solana ETH | SOL              | ETH        | CCC        |
| SOL-EUR  | Solana EUR | SOL              | EUR        | CCC        |
| SOL-GBP  | Solana GBP | SOL              | GBP        | CCC        |
| SOL-INR  | Solana INR | SOL              | INR        | CCC        |
| SOL-JPY  | Solana JPY | SOL              | JPY        | CCC        |
| SOL-KRW  | Solana KRW | SOL              | KRW        | CCC        |
| SOL-RUB  | Solana RUB | SOL              | RUB        | CCC        |
| SOL-USD  | Solana USD | SOL              | USD        | CCC        |

---

## show_options

Show the available values of the cryptocurrencies filters.

The options can be narrowed down with the same filters as select().

`cryptos.show_options` accepts the following parameters:

<div class="docs-params"><div class="docs-params__table"><table>
<thead><tr><th>Parameter</th><th>Type</th><th>Description</th><th>Default</th></tr></thead>
<tbody>
<tr><td><code>selection</code></td><td><code>str | None</code></td><td>The filter to show, None for every filter.</td><td></td></tr>
<tr><td><code>cryptocurrency</code></td><td><code>str | list</code></td><td>Cryptocurrencies to filter on.</td><td></td></tr>
<tr><td><code>currency</code></td><td><code>str | list</code></td><td>Currencies to filter on.</td><td></td></tr>
<tr><td><code>as_pandas</code></td><td><code>bool</code></td><td>Return numpy arrays, else Polars. Defaults to True.</td><td><code>True</code></td></tr>
</tbody>
</table></div></div>

**Returns:** dict | np.ndarray | pl.Series: The sorted values, a dict for every filter.

As an example:

```python
import financedatabase as fd

cryptos = fd.Cryptos()

cryptos.show_options(selection="currency", cryptocurrency="ETH")
```

Which returns:

```
BTC, CAD, EUR, GBP, INR, JPY, KRW, RUB, USD
```

---
