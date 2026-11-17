---
title: "Documentation"
permalink: /projects/financedatabase/docs
seo_title: "Documentation | Finance Database"
seo_title_suffix: false
excerpt: "The Finance Database documentation: every function of the Python package with its parameters, examples and their output, for equities, ETFs, indices, currencies and cryptocurrencies."
description: "The Finance Database documentation: every function of the Python package with its parameters, examples and their output, for equities, ETFs, indices, currencies and cryptocurrencies."
classes: wide-sidebar
author_profile: false
layout: single
redirect_from:
  - /projects/financedatabase/getting-started
  - /projects/financedatabase/documentation
  - /projects/financedatabase/querying-netherlands
  - /projects/financedatabase/technical-analysis
  - /projects/financedatabase/dupont-analysis
  - /projects/financetoolkit/finance-database
sidebar:
  nav: "financedatabase"
image: /assets/images/projects/FinanceDatabase.jpg
---

<div class="page-header-action notebook-viewer-actions"><a href="/projects/financedatabase/explorer"><i class="fas fa-magnifying-glass"></i> Database Explorer</a><a href="https://github.com/JerBouma/FinanceDatabase" target="_blank" rel="noopener"><i class="fab fa-github"></i> View on GitHub</a></div>

The Finance Database is a Python package that classifies 300,000+ stocks, ETFs and indices, as well as currencies and cryptocurrencies. Every asset class has a page with its three functions: `show_options` lists the values a filter accepts, `select` filters on them and `search` finds text in any column. This page covers the functions all asset classes share. Every example on these pages is run against the database, so each output is what the package returns.

Install the Finance Database with:

```bash
pip install financedatabase -U
```

| Asset class | Class | Filters |
|:--|:--|:--|
| [Equities](/projects/financedatabase/docs/equities) | `fd.Equities()` | country, sector, industry group, industry, market cap, market, exchange, currency |
| [ETFs](/projects/financedatabase/docs/etfs) | `fd.ETFs()` | category group, category, family, exchange, currency |
| [Indices](/projects/financedatabase/docs/indices) | `fd.Indices()` | category group, category, exchange, currency |
| [Currencies](/projects/financedatabase/docs/currencies) | `fd.Currencies()` | base currency, quote currency |
| [Cryptocurrencies](/projects/financedatabase/docs/cryptos) | `fd.Cryptos()` | cryptocurrency, currency |

To look through the database without writing any code, use the [Database Explorer](/projects/financedatabase/explorer). It shows the Python code for whatever you select.

## show_options

Show the category options of an asset class without initializing it.

`fd.show_options` accepts the following parameters:

<div class="docs-params"><div class="docs-params__table"><table>
<thead><tr><th>Parameter</th><th>Type</th><th>Description</th><th>Default</th></tr></thead>
<tbody>
<tr><td><code>selection</code></td><td><code>str | None</code></td><td>The asset class, e.g. &#x27;equities&#x27; or &#x27;etfs&#x27;.</td><td></td></tr>
<tr><td><code>base_url</code></td><td><code>str</code></td><td>The URL of the compressed files. Defaults to GitHub.</td><td><code>GitHub</code></td></tr>
<tr><td><code>use_local_location</code></td><td><code>bool</code></td><td>Use the compressed files of a local repository copy. Defaults to False.</td><td><code>False</code></td></tr>
<tr><td><code>as_pandas</code></td><td><code>bool</code></td><td>Return numpy arrays, else Polars. Defaults to True.</td><td><code>True</code></td></tr>
</tbody>
</table></div></div>

**Returns:** dict: Category names mapped to their possible values.

As an example:

```python
import financedatabase as fd

fd.show_options("equities")["sector"]
```

Which returns:

```
Communication Services, Consumer Discretionary, Consumer Staples, Energy, Financials, Health Care, Industrials, Information Technology, Materials, Real Estate, Utilities
```

---

## to_toolkit

Convert the FinanceFrame to a Finance Toolkit object for its tickers.

`to_toolkit` accepts the following parameters:

<div class="docs-params"><div class="docs-params__table"><table>
<thead><tr><th>Parameter</th><th>Type</th><th>Description</th><th>Default</th></tr></thead>
<tbody>
<tr><td><code>api_key</code></td><td><code>str | None</code></td><td>API key, see https://www.jeroenbouma.com/fmp.</td><td></td></tr>
<tr><td><code>start_date</code></td><td><code>str | None</code></td><td>Start date (YYYY-MM-DD), 10 years ago if None.</td><td></td></tr>
<tr><td><code>end_date</code></td><td><code>str | None</code></td><td>End date (YYYY-MM-DD), today if None.</td><td></td></tr>
<tr><td><code>quarterly</code></td><td><code>bool</code></td><td>Quarterly statements. Defaults to False.</td><td><code>False</code></td></tr>
<tr><td><code>use_cached_data</code></td><td><code>bool | str</code></td><td>Cached data, or its path. Defaults to False.</td><td><code>False</code></td></tr>
<tr><td><code>risk_free_rate</code></td><td><code>str</code></td><td>13w, 5y, 10y or 30y. Defaults to &quot;10y&quot;.</td><td><code>&quot;10y&quot;</code></td></tr>
<tr><td><code>benchmark_ticker</code></td><td><code>str | None</code></td><td>Benchmark ticker. Defaults to &quot;SPY&quot;.</td><td><code>&quot;SPY&quot;</code></td></tr>
<tr><td><code>enforce_source</code></td><td><code>str | None</code></td><td>Data source, None for both.</td><td></td></tr>
<tr><td><code>convert_currency</code></td><td><code>bool | None</code></td><td>Convert statement currencies.</td><td></td></tr>
<tr><td><code>intraday_period</code></td><td><code>str | None</code></td><td>Intraday period such as 1min or 1hour.</td><td></td></tr>
<tr><td><code>rounding</code></td><td><code>int | None</code></td><td>Decimal places. Defaults to 4.</td><td><code>4</code></td></tr>
<tr><td><code>remove_invalid_tickers</code></td><td><code>bool</code></td><td>Remove invalid tickers. Defaults to False.</td><td><code>False</code></td></tr>
<tr><td><code>sleep_timer</code></td><td><code>bool | None</code></td><td>Sleep when the rate limit is reached.</td><td></td></tr>
<tr><td><code>progress_bar</code></td><td><code>bool</code></td><td>Show a progress bar. Defaults to True.</td><td><code>True</code></td></tr>
</tbody>
</table></div></div>

**Returns:** Toolkit: Finance Toolkit object with data for the tickers in this DataFrame.

To calculate the return on invested capital of the chipmakers listed in Amsterdam:

```python
import financedatabase as fd

equities = fd.Equities()

chipmakers = equities.select(
    country="Netherlands",
    industry="Semiconductors & Chip Equipment",
    market="Euronext Amsterdam",
)

toolkit = chipmakers.to_toolkit(
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
    progress_bar=False,
)

toolkit.ratios.get_return_on_invested_capital()
```

Which returns:

|         |   2021 |   2022 |   2023 |   2024 |   2025 |
|:--------|-------:|-------:|-------:|-------:|-------:|
| ASM.AS  | 0.1973 | 0.1933 | 0.1879 | 0.18   | 0.1889 |
| ASML.AS | 0.3348 | 0.3989 | 0.4906 | 0.358  | 0.4108 |
| BESI.AS | 0.3447 | 0.27   | 0.2126 | 0.2114 | 0.1486 |

---
