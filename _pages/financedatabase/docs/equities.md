---
title: "Equities"
permalink: /projects/financedatabase/docs/equities
seo_title: "Equities | Finance Database"
seo_title_suffix: false
excerpt: "Select and search equities by country, sector, industry group, industry, market cap and exchange with the Finance Database in Python, with examples and their output."
description: "Select and search equities by country, sector, industry group, industry, market cap and exchange with the Finance Database in Python, with examples and their output."
classes: wide-sidebar
author_profile: false
layout: single
sidebar:
  nav: "financedatabase"
image: /assets/images/projects/FinanceDatabase.jpg
---

<div class="page-header-action notebook-viewer-actions"><a href="/projects/financedatabase/explorer"><i class="fas fa-magnifying-glass"></i> Database Explorer</a><a href="https://github.com/JerBouma/FinanceDatabase" target="_blank" rel="noopener"><i class="fab fa-github"></i> View on GitHub</a></div>

Company shares, selectable by country, sector, industry group, industry, market cap, market and exchange. The Finance Database has its own classification of 11 sectors, 25 industry groups and 75 industries. Many companies are listed on several exchanges: `only_primary_listing=True` keeps one listing per company. To browse them without code, open the equities in the [Database Explorer](/projects/financedatabase/explorer).

## select

Select equities by country, sector, industry group, industry and more.

Returns all equities when no input is given.

`equities.select` accepts the following parameters:

<div class="docs-params"><div class="docs-params__table"><table>
<thead><tr><th>Parameter</th><th>Type</th><th>Description</th><th>Default</th></tr></thead>
<tbody>
<tr><td><code>country</code></td><td><code>str | list</code></td><td>Countries to filter on.</td><td></td></tr>
<tr><td><code>sector</code></td><td><code>str | list</code></td><td>Sectors to filter on.</td><td></td></tr>
<tr><td><code>industry_group</code></td><td><code>str | list</code></td><td>Industry groups to filter on.</td><td></td></tr>
<tr><td><code>industry</code></td><td><code>str | list</code></td><td>Industries to filter on.</td><td></td></tr>
<tr><td><code>currency</code></td><td><code>str | list</code></td><td>Currencies to filter on.</td><td></td></tr>
<tr><td><code>exchange</code></td><td><code>str | list</code></td><td>Exchanges to filter on.</td><td></td></tr>
<tr><td><code>mic</code></td><td><code>str | list</code></td><td>MICs to filter on.</td><td></td></tr>
<tr><td><code>market</code></td><td><code>str | list</code></td><td>Markets to filter on.</td><td></td></tr>
<tr><td><code>market_cap</code></td><td><code>str | list</code></td><td>Market caps to filter on.</td><td></td></tr>
<tr><td><code>only_primary_listing</code></td><td><code>bool</code></td><td>Only primary listings. Defaults to False.</td><td><code>False</code></td></tr>
<tr><td><code>exclude_delisted</code></td><td><code>bool</code></td><td>Exclude delisted equities. Defaults to True.</td><td><code>True</code></td></tr>
<tr><td><code>as_pandas</code></td><td><code>bool</code></td><td>Return pandas, else Polars. Defaults to True.</td><td><code>True</code></td></tr>
</tbody>
</table></div></div>

**Returns:** FinanceFrame | pl.DataFrame: The equities matching every filter.

To find the primary listings of Dutch technology companies:

```python
import financedatabase as fd

equities = fd.Equities()

equities.select(country="Netherlands", sector="Information Technology", only_primary_listing=True)[
    ["name", "currency", "industry", "market", "market_cap"]
].head()
```

Which returns:

| symbol   | name                             | currency   | industry                        | market             | market_cap   |
|:---------|:---------------------------------|:-----------|:--------------------------------|:-------------------|:-------------|
| AMUND.AS | Almunda Professionals N.V.       | EUR        | IT Services                     | Euronext Amsterdam | Nano Cap     |
| ASM.AS   | ASM International N.V.           | EUR        | Semiconductors & Chip Equipment | Euronext Amsterdam | Large Cap    |
| ASML.AS  | ASML Holding N.V.                | EUR        | Semiconductors & Chip Equipment | Euronext Amsterdam | Mega Cap     |
| BESI.AS  | BE Semiconductor Industries N.V. | EUR        | Semiconductors & Chip Equipment | Euronext Amsterdam | Large Cap    |
| CMCOM.AS | CM.com N.V.                      | EUR        | Software                        | Euronext Amsterdam | Micro Cap    |

Every filter also accepts a list, which matches any of its values. To find the primary listings of Dutch and German chipmakers:

```python
equities.select(
    country=["Netherlands", "Germany"],
    industry="Semiconductors & Chip Equipment",
    only_primary_listing=True,
)[["name", "country", "market", "market_cap"]]
```

Which returns:

| symbol   | name                             | country     | market                    | market_cap   |
|:---------|:---------------------------------|:------------|:--------------------------|:-------------|
| 9TS.DU   | TubeSolar AG                     | Germany     | Dusseldorf Stock Exchange | Micro Cap    |
| AIXA.DE  | Aixtron Se                       | Germany     | XETRA                     | Mid Cap      |
| ASM.AS   | ASM International N.V.           | Netherlands | Euronext Amsterdam        | Large Cap    |
| ASML.AS  | ASML Holding N.V.                | Netherlands | Euronext Amsterdam        | Mega Cap     |
| BESI.AS  | BE Semiconductor Industries N.V. | Netherlands | Euronext Amsterdam        | Large Cap    |
| CTNK.HM  | centrotherm international AG     | Germany     | Hamburg Stock Exchange    | Micro Cap    |
| ELG.DE   | Elmos Semiconductor SE           | Germany     | XETRA                     | Mid Cap      |
| IFX.DE   | Infineon Technologies AG         | Germany     | XETRA                     | Large Cap    |
| NXPI     | NXP Semiconductors NV            | Netherlands | NASDAQ Global Select      | Large Cap    |
| QCE.HM   | Global PVQ SE                    | Germany     | Hamburg Stock Exchange    | Nano Cap     |

The first 10 of 15 rows.

---

## search

Search columns with regular expressions; a list of queries matches any of them.

`equities.search` accepts the following parameters:

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

As an example:

```python
import financedatabase as fd

fd.Equities().search(summary="semiconductor", country="Netherlands")
```

Which returns:

| symbol   | name                    | currency   | sector                 | industry_group   | industry                        | exchange   | market                                | country     | market_cap   |
|:---------|:------------------------|:-----------|:-----------------------|:-----------------|:--------------------------------|:-----------|:--------------------------------------|:------------|:-------------|
| 0EDE.L   | NXP Semiconductors N.V. | USD        | Information Technology | Semiconductors   | Semiconductors & Chip Equipment | LSE        | London Stock Exchange (international) | Netherlands | Large Cap    |
| 1ASML.MI | ASML Holding N.V.       | EUR        | Information Technology | Semiconductors   | Semiconductors & Chip Equipment | MIL        | Borsa Italiana                        | Netherlands | Mega Cap     |
| ASM.AS   | ASM International N.V.  | EUR        | Information Technology | Semiconductors   | Semiconductors & Chip Equipment | AMS        | Euronext Amsterdam                    | Netherlands | Large Cap    |
| ASM1N.MX | ASM International N.V.  | MXN        | Information Technology | Semiconductors   | Semiconductors & Chip Equipment | MEX        | Mexico Stock Exchange                 | Netherlands | Large Cap    |
| ASME.BE  | ASML Holding N.V.       | EUR        | Information Technology | Semiconductors   | Semiconductors & Chip Equipment | BER        | Berlin Stock Exchange                 | Netherlands | Mega Cap     |
| ASME.DE  | ASML Holding N.V.       | EUR        | Information Technology | Semiconductors   | Semiconductors & Chip Equipment | GER        | XETRA                                 | Netherlands | Mega Cap     |
| ASME.DU  | ASML Holding N.V.       | EUR        | Information Technology | Semiconductors   | Semiconductors & Chip Equipment | DUS        | Dusseldorf Stock Exchange             | Netherlands | Mega Cap     |
| ASME.F   | ASML Holding N.V.       | EUR        | Information Technology | Semiconductors   | Semiconductors & Chip Equipment | FRA        | Frankfurt Stock Exchange              | Netherlands | Mega Cap     |
| ASME.HA  | ASML Holding N.V.       | EUR        | Information Technology | Semiconductors   | Semiconductors & Chip Equipment | HAN        | Hanover Stock Exchange                | Netherlands | nan          |
| ASME.HM  | ASML Holding N.V.       | EUR        | Information Technology | Semiconductors   | Semiconductors & Chip Equipment | HAM        | Hamburg Stock Exchange                | Netherlands | Mega Cap     |

The first 10 of 61 rows.

The queries are regular expressions and can be combined with any column. To find primary listings in capital goods whose summary mentions robotics:

```python
equities.search(summary="robotics", industry_group="Capital Goods", only_primary_listing=True)[
    ["name", "country", "industry", "market"]
].head(10)
```

Which returns:

| symbol   | name   | country   | industry   | market   |
|----------|--------|-----------|------------|----------|

---

## show_options

Show the available values of the equities filters.

The options can be narrowed down with the same filters as select().

`equities.show_options` accepts the following parameters:

<div class="docs-params"><div class="docs-params__table"><table>
<thead><tr><th>Parameter</th><th>Type</th><th>Description</th><th>Default</th></tr></thead>
<tbody>
<tr><td><code>selection</code></td><td><code>str | None</code></td><td>The filter to show, None for every filter.</td><td></td></tr>
<tr><td><code>country</code></td><td><code>str | list</code></td><td>Countries to filter on.</td><td></td></tr>
<tr><td><code>sector</code></td><td><code>str | list</code></td><td>Sectors to filter on.</td><td></td></tr>
<tr><td><code>industry_group</code></td><td><code>str | list</code></td><td>Industry groups to filter on.</td><td></td></tr>
<tr><td><code>industry</code></td><td><code>str | list</code></td><td>Industries to filter on.</td><td></td></tr>
<tr><td><code>currency</code></td><td><code>str | list</code></td><td>Currencies to filter on.</td><td></td></tr>
<tr><td><code>exchange</code></td><td><code>str | list</code></td><td>Exchanges to filter on.</td><td></td></tr>
<tr><td><code>mic</code></td><td><code>str | list</code></td><td>MICs to filter on.</td><td></td></tr>
<tr><td><code>market</code></td><td><code>str | list</code></td><td>Markets to filter on.</td><td></td></tr>
<tr><td><code>market_cap</code></td><td><code>str | list</code></td><td>Market caps to filter on.</td><td></td></tr>
<tr><td><code>exclude_delisted</code></td><td><code>bool</code></td><td>Exclude delisted equities. Defaults to True.</td><td><code>True</code></td></tr>
<tr><td><code>as_pandas</code></td><td><code>bool</code></td><td>Return numpy arrays, else Polars. Defaults to True.</td><td><code>True</code></td></tr>
</tbody>
</table></div></div>

**Returns:** dict | np.ndarray | pl.Series: The sorted values, a dict for every filter.

As an example:

```python
import financedatabase as fd

equities = fd.Equities()

equities.show_options(selection="market_cap", country="Netherlands")
```

Which returns:

```
Large Cap, Mega Cap, Micro Cap, Mid Cap, Nano Cap, Small Cap
```

To see which industries exist among Dutch financial companies:

```python
equities.show_options(selection="industry", sector="Financials", country="Netherlands")
```

Which returns:

```
Banks, Capital Markets, Consumer Lending, Insurance, Payments & Specialty Finance
```

---
