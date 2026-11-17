---
title: "Indices"
permalink: /projects/financedatabase/docs/indices
seo_title: "Indices | Finance Database"
seo_title_suffix: false
excerpt: "Select and search indices by category group, category, currency and exchange with the Finance Database in Python, with examples and their output."
description: "Select and search indices by category group, category, currency and exchange with the Finance Database in Python, with examples and their output."
classes: wide-sidebar
author_profile: false
layout: single
sidebar:
  nav: "financedatabase"
image: /assets/images/projects/FinanceDatabase.jpg
---

<div class="page-header-action notebook-viewer-actions"><a href="/projects/financedatabase/explorer?class=indices"><i class="fas fa-magnifying-glass"></i> Database Explorer</a><a href="https://github.com/JerBouma/FinanceDatabase" target="_blank" rel="noopener"><i class="fab fa-github"></i> View on GitHub</a></div>

Indices, selectable by category group, category, currency and exchange. To browse them without code, open the indices in the [Database Explorer](/projects/financedatabase/explorer?class=indices).

## select

Select indices based on the category group, category, currency and other criteria.

Returns all indices when no input is given.

`indices.select` accepts the following parameters:

<div class="docs-params"><div class="docs-params__table"><table>
<thead><tr><th>Parameter</th><th>Type</th><th>Description</th><th>Default</th></tr></thead>
<tbody>
<tr><td><code>category_group</code></td><td><code>str | list</code></td><td>Category groups to filter on.</td><td></td></tr>
<tr><td><code>category</code></td><td><code>str | list</code></td><td>Categories to filter on.</td><td></td></tr>
<tr><td><code>currency</code></td><td><code>str | list</code></td><td>Currencies to filter on.</td><td></td></tr>
<tr><td><code>exchange</code></td><td><code>str | list</code></td><td>Exchanges to filter on.</td><td></td></tr>
<tr><td><code>mic</code></td><td><code>str | list</code></td><td>MICs to filter on.</td><td></td></tr>
<tr><td><code>as_pandas</code></td><td><code>bool</code></td><td>Return pandas, else Polars. Defaults to True.</td><td><code>True</code></td></tr>
</tbody>
</table></div></div>

**Returns:** FinanceFrame | pl.DataFrame: The indices matching every filter.

As an example:

```python
import financedatabase as fd

indices = fd.Indices()

indices.select(category_group="Equities", category="Large Cap", currency="EUR")[
    ["name", "currency", "category", "exchange"]
].head()
```

Which returns:

| symbol   | name              | currency   | category   | exchange   |
|:---------|:------------------|:-----------|:-----------|:-----------|
| 0020.Z   | ESTX LRB50 NR EUR | EUR        | Large Cap  | ZRH        |
| 0022.Z   | ESTX LRB50 PR EUR | EUR        | Large Cap  | ZRH        |
| 002A.Z   | ESTX LR50 NR EUR  | EUR        | Large Cap  | ZRH        |
| 002C.Z   | ESTX LR50 PR EUR  | EUR        | Large Cap  | ZRH        |
| 002G.Z   | ESTX LR100 NR EUR | EUR        | Large Cap  | ZRH        |

---

## search

Search columns with regular expressions; a list of queries matches any of them.

`indices.search` accepts the following parameters:

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

To find the Euro Stoxx 50 indices:

```python
import financedatabase as fd

indices = fd.Indices()

indices.search(name="Euro Stoxx 50")[["name", "currency", "category", "exchange"]].head(10)
```

Which returns:

| symbol   | name                           | currency   | category   | exchange   |
|:---------|:-------------------------------|:-----------|:-----------|:-----------|
| 4QDU.DE  | IN.INV.EURO STOXX 50 EUR       | EUR        | Equities   | GER        |
| X2H1.DE  | IN.INV.EURO STOXX 50 GBP       | GBP        | Equities   | GER        |
| ^FEZ-EU  | FRESCO DOW JONES EURO STOXX 50 | USD        | Equities   | ASE        |
| ^FEZ-IV  | FRESCO DOW JONES EURO STOXX 50 | USD        | Equities   | ASE        |
| ^FEZ-NV  | FRESCO DOW JONES EURO STOXX 50 | USD        | Equities   | ASE        |
| ^FEZ-TC  | FRESCO DOW JONES EURO STOXX 50 | USD        | Equities   | ASE        |

---

## show_options

Show the available values of the indices filters.

The options can be narrowed down with the same filters as select().

`indices.show_options` accepts the following parameters:

<div class="docs-params"><div class="docs-params__table"><table>
<thead><tr><th>Parameter</th><th>Type</th><th>Description</th><th>Default</th></tr></thead>
<tbody>
<tr><td><code>selection</code></td><td><code>str | None</code></td><td>The filter to show, None for every filter.</td><td></td></tr>
<tr><td><code>category_group</code></td><td><code>str | list</code></td><td>Category groups to filter on.</td><td></td></tr>
<tr><td><code>category</code></td><td><code>str | list</code></td><td>Categories to filter on.</td><td></td></tr>
<tr><td><code>currency</code></td><td><code>str | list</code></td><td>Currencies to filter on.</td><td></td></tr>
<tr><td><code>exchange</code></td><td><code>str | list</code></td><td>Exchanges to filter on.</td><td></td></tr>
<tr><td><code>mic</code></td><td><code>str | list</code></td><td>MICs to filter on.</td><td></td></tr>
<tr><td><code>as_pandas</code></td><td><code>bool</code></td><td>Return numpy arrays, else Polars. Defaults to True.</td><td><code>True</code></td></tr>
</tbody>
</table></div></div>

**Returns:** dict | np.ndarray | pl.Series: The sorted values, a dict for every filter.

As an example:

```python
import financedatabase as fd

indices = fd.Indices()

indices.show_options(selection="category_group")
```

Which returns:

```
Alternatives, Cash, Commodities, Communication Services, Consumer Discretionary, Consumer Staples, Currencies, Derivatives, Energy, Equities, Financials, Fixed Income, … (18 in total)
```

---
