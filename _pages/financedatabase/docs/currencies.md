---
title: "Currencies"
permalink: /projects/financedatabase/docs/currencies
seo_title: "Currencies | Finance Database"
seo_title_suffix: false
excerpt: "Select and search currency pairs by base and quote currency with the Finance Database in Python, with examples and their output."
description: "Select and search currency pairs by base and quote currency with the Finance Database in Python, with examples and their output."
classes: wide-sidebar
author_profile: false
layout: single
sidebar:
  nav: "financedatabase"
image: /assets/images/projects/FinanceDatabase.jpg
---

<div class="page-header-action notebook-viewer-actions"><a href="/projects/financedatabase/explorer?class=currencies"><i class="fas fa-magnifying-glass"></i> Database Explorer</a><a href="https://github.com/JerBouma/FinanceDatabase" target="_blank" rel="noopener"><i class="fab fa-github"></i> View on GitHub</a></div>

Currency pairs, selectable by base and quote currency. The symbols follow Yahoo Finance, such as EURUSD=X; the Finance Toolkit writes them without the suffix (EURUSD). To browse them without code, open the currencies in the [Database Explorer](/projects/financedatabase/explorer?class=currencies).

## select

Select currency pairs based on the base and quote currency.

Returns all currency pairs when no input is given.

`currencies.select` accepts the following parameters:

<div class="docs-params"><div class="docs-params__table"><table>
<thead><tr><th>Parameter</th><th>Type</th><th>Description</th><th>Default</th></tr></thead>
<tbody>
<tr><td><code>base_currency</code></td><td><code>str | list</code></td><td>Base currencies to filter on.</td><td></td></tr>
<tr><td><code>quote_currency</code></td><td><code>str | list</code></td><td>Quote currencies to filter on.</td><td></td></tr>
<tr><td><code>as_pandas</code></td><td><code>bool</code></td><td>Return pandas, else Polars. Defaults to True.</td><td><code>True</code></td></tr>
</tbody>
</table></div></div>

**Returns:** FinanceFrame | pl.DataFrame: The currencies matching every filter.

As an example:

```python
import financedatabase as fd

currencies = fd.Currencies()

currencies.select(base_currency="EUR")[
    ["name", "base_currency", "quote_currency", "exchange"]
].head()
```

Which returns:

| symbol   | name    | base_currency   | quote_currency   | exchange   |
|:---------|:--------|:----------------|:-----------------|:-----------|
| EURAED=X | EUR/AED | EUR             | AED              | CCY        |
| EURAFN=X | EUR/AFN | EUR             | AFN              | CCY        |
| EURALL=X | EUR/ALL | EUR             | ALL              | CCY        |
| EURAMD=X | EUR/AMD | EUR             | AMD              | CCY        |
| EURAOA=X | EUR/AOA | EUR             | AOA              | CCY        |

---

## search

Search columns with regular expressions; a list of queries matches any of them.

`currencies.search` accepts the following parameters:

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

To find the currency pairs that quote the Japanese yen:

```python
import financedatabase as fd

currencies = fd.Currencies()

currencies.search(quote_currency="JPY")[["name", "base_currency", "quote_currency"]].head(10)
```

Which returns:

| symbol   | name    | base_currency   | quote_currency   |
|:---------|:--------|:----------------|:-----------------|
| AEDJPY=X | AED/JPY | AED             | JPY              |
| ARSJPY=X | ARS/JPY | ARS             | JPY              |
| AUDJPY=X | AUD/JPY | AUD             | JPY              |
| AUXJPY=X | AUX/JPY | AUX             | JPY              |
| BDTJPY=X | BDT/JPY | BDT             | JPY              |
| BHDJPY=X | BHD/JPY | BHD             | JPY              |
| BRLJPY=X | BRL/JPY | BRL             | JPY              |
| BWPJPY=X | BWP/JPY | BWP             | JPY              |
| CADJPY=X | CAD/JPY | CAD             | JPY              |
| CHFJPY=X | CHF/JPY | CHF             | JPY              |

---

## show_options

Show the available values of the currencies filters.

The options can be narrowed down with the same filters as select().

`currencies.show_options` accepts the following parameters:

<div class="docs-params"><div class="docs-params__table"><table>
<thead><tr><th>Parameter</th><th>Type</th><th>Description</th><th>Default</th></tr></thead>
<tbody>
<tr><td><code>selection</code></td><td><code>str | None</code></td><td>The filter to show, None for every filter.</td><td></td></tr>
<tr><td><code>base_currency</code></td><td><code>str | list</code></td><td>Base currencies to filter on.</td><td></td></tr>
<tr><td><code>quote_currency</code></td><td><code>str | list</code></td><td>Quote currencies to filter on.</td><td></td></tr>
<tr><td><code>as_pandas</code></td><td><code>bool</code></td><td>Return numpy arrays, else Polars. Defaults to True.</td><td><code>True</code></td></tr>
</tbody>
</table></div></div>

**Returns:** dict | np.ndarray | pl.Series: The sorted values, a dict for every filter.

As an example:

```python
import financedatabase as fd

currencies = fd.Currencies()

currencies.show_options(selection="quote_currency", base_currency="EUR")[:5]
```

Which returns:

```
AED, AFN, ALL, AMD, AOA
```

---
