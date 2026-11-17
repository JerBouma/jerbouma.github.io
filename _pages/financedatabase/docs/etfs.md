---
title: "ETFs"
permalink: /projects/financedatabase/docs/etfs
seo_title: "ETFs | Finance Database"
seo_title_suffix: false
excerpt: "Select and search ETFs by category group, category, family and exchange with the Finance Database in Python, with examples and their output."
description: "Select and search ETFs by category group, category, family and exchange with the Finance Database in Python, with examples and their output."
classes: wide-sidebar
author_profile: false
layout: single
sidebar:
  nav: "financedatabase"
image: /assets/images/projects/FinanceDatabase.jpg
---

<div class="page-header-action notebook-viewer-actions"><a href="/projects/financedatabase/explorer?class=etfs"><i class="fas fa-magnifying-glass"></i> Database Explorer</a><a href="https://github.com/JerBouma/FinanceDatabase" target="_blank" rel="noopener"><i class="fab fa-github"></i> View on GitHub</a></div>

Exchange-traded funds, selectable by category group (such as Equities or Fixed Income), category, fund family and exchange. To browse them without code, open the ETFs in the [Database Explorer](/projects/financedatabase/explorer?class=etfs).

## select

Select ETFs based on the category group, category, family and other criteria.

Returns all ETFs when no input is given.

`etfs.select` accepts the following parameters:

<div class="docs-params"><div class="docs-params__table"><table>
<thead><tr><th>Parameter</th><th>Type</th><th>Description</th><th>Default</th></tr></thead>
<tbody>
<tr><td><code>category_group</code></td><td><code>str | list</code></td><td>Category groups to filter on.</td><td></td></tr>
<tr><td><code>category</code></td><td><code>str | list</code></td><td>Categories to filter on.</td><td></td></tr>
<tr><td><code>family</code></td><td><code>str | list</code></td><td>Families to filter on.</td><td></td></tr>
<tr><td><code>currency</code></td><td><code>str | list</code></td><td>Currencies to filter on.</td><td></td></tr>
<tr><td><code>exchange</code></td><td><code>str | list</code></td><td>Exchanges to filter on.</td><td></td></tr>
<tr><td><code>mic</code></td><td><code>str | list</code></td><td>MICs to filter on.</td><td></td></tr>
<tr><td><code>only_primary_listing</code></td><td><code>bool</code></td><td>Only primary listings. Defaults to False.</td><td><code>False</code></td></tr>
<tr><td><code>exclude_delisted</code></td><td><code>bool</code></td><td>Exclude delisted ETFs. Defaults to True.</td><td><code>True</code></td></tr>
<tr><td><code>as_pandas</code></td><td><code>bool</code></td><td>Return pandas, else Polars. Defaults to True.</td><td><code>True</code></td></tr>
</tbody>
</table></div></div>

**Returns:** FinanceFrame | pl.DataFrame: The ETFs matching every filter.

As an example:

```python
import financedatabase as fd

etfs = fd.ETFs()

etfs.select(
    category_group="Equities",
    category="Large Cap",
    family="BlackRock Asset Management",
    only_primary_listing=True,
)[["name", "currency", "category", "exchange"]].head()
```

Which returns:

| symbol   | name                           | currency   | category   | exchange   |
|:---------|:-------------------------------|:-----------|:-----------|:-----------|
| 1329.T   | iShares Core Nikkei 225 ETF    | JPY        | Large Cap  | JPX        |
| 1364.T   | iShares JPX-Nikkei 400 ETF     | JPY        | Large Cap  | JPX        |
| 1475.T   | iShares Core TOPIX ETF         | JPY        | Large Cap  | JPX        |
| 2563.T   | iShares S&P 500 JPY Hedged ETF | JPY        | Large Cap  | JPX        |
| 2834.HK  | ISHARES NASDAQ 100 ETF-HKD     | HKD        | Large Cap  | HKG        |

To find bond ETFs from Vanguard:

```python
etfs.select(category_group="Fixed Income", family="Vanguard Asset Management", only_primary_listing=True)[
    ["name", "category", "currency", "exchange"]
].head(10)
```

Which returns:

| symbol   | name                                                               | category               | currency   | exchange   |
|:---------|:-------------------------------------------------------------------|:-----------------------|:-----------|:-----------|
| 0LN3.L   | Vanguard Scottsdale Funds - Vanguard Short-Term Corporate Bond ETF | Corporate Bonds        | USD        | LSE        |
| 0VOO.L   | Vanguard Scottsdale Funds - Vanguard Long-Term Corporate Bond ETF  | Corporate Bonds        | USD        | LSE        |
| BIV      | Vanguard Intermediate-Term Bond Index Fund ETF Shares              | Investment Grade Bonds | USD        | PCX        |
| BIV.MX   | Vanguard Intermediate-Term Bond Index Fund ETF Shares              | Investment Grade Bonds | MXN        | MEX        |
| BLV      | Vanguard Long-Term Bond Index Fund ETF Shares                      | Investment Grade Bonds | USD        | PCX        |
| BLV.MX   | Vanguard Long-Term Bond Index Fund ETF Shares                      | Investment Grade Bonds | MXN        | MEX        |
| BND      | Vanguard Total Bond Market Index Fund ETF Shares                   | Investment Grade Bonds | USD        | NMS        |
| BND.MX   | Vanguard Total Bond Market Index Fund ETF Shares                   | Investment Grade Bonds | MXN        | MEX        |
| BNDP     | Vanguard Core-Plus Bond Index ETF                                  | Blend                  | USD        | NGM        |
| BNDW     | Vanguard Total World Bond ETF                                      | Investment Grade Bonds | USD        | NGM        |

---

## search

Search columns with regular expressions; a list of queries matches any of them.

`etfs.search` accepts the following parameters:

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

To find ETFs whose summary mentions robotics:

```python
import financedatabase as fd

etfs = fd.ETFs()

etfs.search(summary="robotics", only_primary_listing=True)[["name", "category", "family", "exchange"]].head(10)
```

Which returns:

| symbol    | name                                                        | category          | family                              | exchange   |
|:----------|:------------------------------------------------------------|:------------------|:------------------------------------|:-----------|
| 00851.TW  | Taishin SG Global AI and Robotics Select ETF                | nan               | Taishin Securities Investment Trust | TAI        |
| 2638.T    | Global X Japan Robotics & AI ETF                            | Developed Markets | Global X Funds                      | JPX        |
| 276990.KS | Kodex Global Robotics & Automation                          | Developed Markets | Samsung Asset Management            | KSC        |
| 2807.HK   | Global X China Robotics                                     | Emerging Markets  | Global X Funds                      | HKG        |
| 2B76.DE   | iShares Automation & Robotics UCITS ETF USD (Acc)           | Developed Markets | BlackRock Asset Management          | GER        |
| 2B7F.DE   | iShares Automation & Robotics UCITS ETF USD (Dist)          | Developed Markets | BlackRock Asset Management          | GER        |
| 3093.HK   | Fullgoal ETF Series - Fullgoal Hang Seng HK-US Robotics ETF | Developed Markets | nan                                 | HKG        |
| ARKI.L    | ARK Artificial Intelligence & Robotics UCITS ETF AccumUSD   | Developed Markets | ARK ETF Trust                       | LSE        |
| ARKQ      | ARK Autonomous Technology & Robotics ETF                    | Developed Markets | ARK ETF Trust                       | BTS        |
| BOT.NZ    | Smart Automation and Robotics ETF                           | Developed Markets | Smartshares                         | NZE        |

---

## show_options

Show the available values of the ETFs filters.

The options can be narrowed down with the same filters as select().

`etfs.show_options` accepts the following parameters:

<div class="docs-params"><div class="docs-params__table"><table>
<thead><tr><th>Parameter</th><th>Type</th><th>Description</th><th>Default</th></tr></thead>
<tbody>
<tr><td><code>selection</code></td><td><code>str | None</code></td><td>The filter to show, None for every filter.</td><td></td></tr>
<tr><td><code>category_group</code></td><td><code>str | list</code></td><td>Category groups to filter on.</td><td></td></tr>
<tr><td><code>category</code></td><td><code>str | list</code></td><td>Categories to filter on.</td><td></td></tr>
<tr><td><code>family</code></td><td><code>str | list</code></td><td>Families to filter on.</td><td></td></tr>
<tr><td><code>currency</code></td><td><code>str | list</code></td><td>Currencies to filter on.</td><td></td></tr>
<tr><td><code>exchange</code></td><td><code>str | list</code></td><td>Exchanges to filter on.</td><td></td></tr>
<tr><td><code>mic</code></td><td><code>str | list</code></td><td>MICs to filter on.</td><td></td></tr>
<tr><td><code>exclude_delisted</code></td><td><code>bool</code></td><td>Exclude delisted ETFs. Defaults to True.</td><td><code>True</code></td></tr>
<tr><td><code>as_pandas</code></td><td><code>bool</code></td><td>Return numpy arrays, else Polars. Defaults to True.</td><td><code>True</code></td></tr>
</tbody>
</table></div></div>

**Returns:** dict | np.ndarray | pl.Series: The sorted values, a dict for every filter.

As an example:

```python
import financedatabase as fd

etfs = fd.ETFs()

etfs.show_options(selection="category", category_group="Fixed Income")
```

Which returns:

```
Blend, Bonds, Cash, Commercial Real Estate, Corporate Bonds, Developed Markets, Emerging Markets, Government Bonds, High Yield Bonds, Inflation-Protected Securities, Investment Grade Bonds, Large Cap, … (15 in total)
```

---
