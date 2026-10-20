---
permalink: /projects/financedatabase
software:
  name: "Finance Database"
  repository: "https://github.com/JerBouma/FinanceDatabase"
  download: "https://pypi.org/project/financedatabase/"
title: Finance Database
excerpt: The Finance Database features 300,000+ symbols containing Equities, ETFs, Indices, Currencies and Cryptocurrencies. It therefore allows you to obtain a broad overview of sectors, industries, types of investments and much more.
description: "The Finance Database is an open-source Python package with 300,000+ symbols: equities, ETFs, indices, currencies and cryptocurrencies."
classes: wide-sidebar
author_profile: false
redirect_from:
  - /financedatabase
sidebar:
  nav: "financedatabase"
---

<div class="page-header-action notebook-viewer-actions"><a href="https://github.com/JerBouma/FinanceDatabase" target="_blank" rel="noopener"><i class="fab fa-github"></i> View on GitHub</a></div>

{%- assign fd = site.data.projects.maintained | where: "name", "Finance Database" | first %}
{%- assign fd_stars = fd.stats | where: "icon", "fa-star" | first %}
{%- assign fd_dl = fd.stats | where: "icon", "fa-download" | first %}
<div class="ft-hero">
  <div class="mcp-video-wrapper ft-hero__video">
    <video class="mcp-demo-video" autoplay muted playsinline controls preload="auto" width="1920" height="1080"
           poster="/assets/images/projects/financedatabase-launch.jpg"
           aria-label="From the names everyone knows to every symbol in the Finance Database, sorted by asset class, sector, industry and country, down to Tokyo Electron's seven listings: 300,000+ symbols.">
      <source src="/assets/video/financedatabase-launch.mp4" type="video/mp4">
    </video>
  </div>
  <div class="mcp-facts ft-hero__facts">
    <div class="mcp-fact"><strong>300,000+</strong><span>symbols</span></div>
    <div class="mcp-fact"><strong>{{ fd_stars.value }}</strong><span>GitHub stars</span></div>
    <div class="mcp-fact"><strong>{{ fd_dl.value }}</strong><span>downloads</span></div>
  </div>
</div>

As a private investor, the amount of information you can find on the internet is rather daunting. With millions of companies and derivatives on the market, it is hard to understand what types of companies or ETFs are available. The most traded companies and ETFs are easy to find because they are known to the public (for example, Microsoft, Tesla, S&P 500 ETF or an All-World ETF), but what else is out there is often unknown.

**This is why I created the Finance Database**, a database featuring 300,000+ symbols containing Equities, ETFs, Indices, Currencies and Cryptocurrencies, plus the Funds and Money Markets it held until October 2026. It allows you to obtain a broad overview of sectors, industries, types of investments and much more, entirely for free. Everything is stored in CSV files that anyone can read and edit, so the database grows and improves through the community.

The database is explicitly _not_ meant to provide up-to-date fundamentals or stock data, as those are easy to obtain (with the help of this database) through the [Finance Toolkit](/projects/financetoolkit). Instead, it shows which products exist in each country, industry and sector and gives the most essential information about each of them. With this information, you can analyze specific areas of the financial world or find a product that is otherwise hard to find. By using both, it is possible to do a fully-fledged competitive analysis with the tickers found in the Finance Database loaded into the Finance Toolkit.

<img src="/assets/images/projects/FinanceDatabase.jpg" alt="Finance Database" width="100%"/>

## Installation

Before installation, consider starring the project on GitHub which helps others find the project as well.

<a href="https://github.com/JerBouma/FinanceDatabase" target="_blank"><img width="1353" alt="image" src="https://github.com/JerBouma/FinanceDatabase/assets/46355364/4132edde-72f9-4e32-adfe-8872207f46ff"></a>

Installing the Finance Database only requires the following (Python 3.11 or newer):

```bash
pip install financedatabase -U
```

Then within Python use:

```python
import financedatabase as fd

equities = fd.Equities()
```

No API key is needed. Each asset class is downloaded once and cached locally, see [Questions & Answers](#questions--answers) for how the cache works.

## Functionality
{: .heading-as-h1}
This section is an introduction to the Finance Database. The Getting Started Notebook contains many more examples, including the full output of each query.

[Find the Getting Started Notebook](/projects/financedatabase/getting-started){: .btn .btn--warning .btn--large .align-center}

A basic example of how to use the Finance Database is shown below. Every code snippet in the sections that follow builds on this same `equities` instance. Initialization of each asset class is only required <u>once</u>, so save it to a variable to query the database much more quickly.

```python
import financedatabase as fd

# Initialize the Equities database
equities = fd.Equities()

# Select all equities
equities.select()
```

A portion of the output is shown below. The tables in this section are cut off to five entries and a selection of the columns due to the sheer size of the database.

| symbol   | name                     | currency   | sector                 | industry                                   | exchange   | market               | country       | market_cap   | isin         |
|:---------|:-------------------------|:-----------|:-----------------------|:-------------------------------------------|:-----------|:---------------------|:--------------|:-------------|:-------------|
| AAPL     | Apple Inc.               | USD        | Information Technology | Computers & Hardware                       | NMS        | NASDAQ Global Select | United States | Mega Cap     | US0378331005 |
| ASML.AS  | ASML Holding N.V.        | EUR        | Information Technology | Semiconductors & Chip Equipment            | AMS        | Euronext Amsterdam   | Netherlands   | Mega Cap     | NL0010273215 |
| 7203.T   | Toyota Motor Corporation | JPY        | Consumer Discretionary | Automobiles                                | JPX        | Tokyo Stock Exchange | Japan         | Mega Cap     | JP3633400001 |
| NESN.SW  | Nestle S.A.              | CHF        | Consumer Staples       | Food Products                              | EBS        | SIX Swiss Exchange   | Switzerland   | Mega Cap     | CH0038863350 |
| SAP.DE   | SAP SE                   | EUR        | Information Technology | Software                                   | GER        | XETRA                | Germany       | Mega Cap     | DE0007164600 |

And below the actively listed equities are counted per sector.

{% include ft-chart.html id="sectors" src="/assets/data/financedatabase-charts.json" label="Actively listed equities per sector" %}

Each asset class has the same three functions: `select` to filter on the database's categories, `search` to look for any text in any column and `show_options` to see which values a category can take. The asset classes are `fd.Equities()`, `fd.ETFs()`, `fd.Indices()`, `fd.Currencies()` and `fd.Cryptos()`, which are updated weekly from official exchange and market sources.

Three capabilities cut across all of them:

- **Lists of values.** Every filter accepts a single value or a list, e.g. `country=['Netherlands', 'Belgium']`, returning the entries that match any of them.
- **`only_primary_listing` and `exclude_delisted`.** A company is often listed on many exchanges. `only_primary_listing=True` keeps only its primary listing, and delisted symbols are left out by default (`exclude_delisted=False` to include them).
- **pandas or Polars.** Queries run lazily with [Polars](https://pola.rs/){:target="_blank"} and return a pandas DataFrame by default, or a Polars DataFrame with `as_pandas=False`.

### Exploring the Options

With `show_options`, all possible options are given per column. **This is useful as it doesn't require loading the larger data files.**

```python
# Show the options of every column of the equities
options = fd.show_options("equities")

# Select the sectors
options["sector"]
```

This returns the eleven sectors used for equities:

```text
['Communication Services', 'Consumer Discretionary', 'Consumer Staples',
 'Energy', 'Financials', 'Health Care', 'Industrials',
 'Information Technology', 'Materials', 'Real Estate', 'Utilities']
```

Once an asset class is loaded, `show_options` is also available on the class itself, where it shows the options that remain after filtering. For example, the industries of the financial companies in the Netherlands:

```python
# Show the industries of financial companies in the Netherlands
equities.show_options(
    selection="industry",
    sector="Financials",
    country="Netherlands",
)
```

Which returns:

```text
['Banks', 'Capital Markets', 'Consumer Lending', 'Insurance',
 'Payments & Specialty Finance']
```

And below the number of companies in each of these industries is shown. Each company is counted once, however many exchanges it is listed on: listings that share an ISIN, share class FIGI, website or the first word of their name (such as Aegon and its perpetual bonds) are combined.

{% include ft-chart.html id="options" src="/assets/data/financedatabase-charts.json" label="Financial companies in the Netherlands per industry" %}

The options of every column can be shown this way, including `currency`, `exchange`, `market`, `country` and `market_cap` (Mega, Large, Mid, Small, Micro and Nano Cap). **Find [the Notebook](/projects/financedatabase/getting-started).**

### Selecting Equities

Given these options, it becomes possible to filter the database on the categories you are interested in. For example, the 'Insurance' companies in the 'United States', one row per company. The `sector` can be omitted here since the industry already implies 'Financials'.

```python
# Select the primary listings of insurance companies in the United States
equities.select(
    country="United States",
    industry="Insurance",
    only_primary_listing=True,
)
```

This returns about 130 companies, of which a few of the larger ones are shown below.

| symbol   | name                             | currency   | sector     | industry   | exchange   | market                  | country       | market_cap   |
|:---------|:---------------------------------|:-----------|:-----------|:-----------|:-----------|:------------------------|:--------------|:-------------|
| AFL      | Aflac Incorporated               | USD        | Financials | Insurance  | NYQ        | New York Stock Exchange | United States | Large Cap    |
| AJG      | Arthur J. Gallagher & Co.        | USD        | Financials | Insurance  | NYQ        | New York Stock Exchange | United States | Large Cap    |
| BRO      | Brown & Brown, Inc.              | USD        | Financials | Insurance  | NYQ        | New York Stock Exchange | United States | Large Cap    |
| CINF     | Cincinnati Financial Corporation | USD        | Financials | Insurance  | NMS        | NASDAQ Global Select    | United States | Large Cap    |
| PGR      | Progressive Corporation          | USD        | Financials | Insurance  | NYQ        | New York Stock Exchange | United States | Large Cap    |

Without `only_primary_listing=True`, the same query returns more than 400 listings on more than 20 exchanges, because every exchange a company trades on is shown by default. Progressive, for example, also appears as `PGV.F` (Frankfurt), `PGV.SG` (Stuttgart), `PGR.MX` (Mexico) and `P1GR34.SA` (B3). The primary listing of a company is its listing on the main exchange of its home market, or without one its listing on the largest main exchange abroad. It is worked out from the data itself, so it works for companies anywhere: for ASML it is `ASML.AS` on Euronext Amsterdam, not `ASML` on NASDAQ or `ASMLF` over the counter. To get the listings in a particular country instead, such as the US listings of ASML, filter on the `exchange`, `market` or `currency`.

For the Netherlands, it makes sense to select the market "Euronext Amsterdam" (exchange "AMS"), here together with the market cap:

```python
# Select the large insurance companies on Euronext Amsterdam
equities.select(
    country="Netherlands",
    industry="Insurance",
    market="Euronext Amsterdam",
    market_cap="Large Cap",
)
```

This gives the following three companies:

| symbol   | name               | currency   | sector     | industry   | exchange   | market             | country     | market_cap   | isin         |
|:---------|:-------------------|:-----------|:-----------|:-----------|:-----------|:-------------------|:------------|:-------------|:-------------|
| AGN.AS   | Aegon N.V.         | EUR        | Financials | Insurance  | AMS        | Euronext Amsterdam | Netherlands | Large Cap    | BMG0112X1056 |
| ASRNL.AS | ASR Nederland N.V. | EUR        | Financials | Insurance  | AMS        | Euronext Amsterdam | Netherlands | Large Cap    | NL0011872643 |
| NN.AS    | NN Group N.V.      | EUR        | Financials | Insurance  | AMS        | Euronext Amsterdam | Netherlands | Large Cap    | NL0010773842 |

Every filter also accepts a list, so both queries can be combined into one with `country=["Netherlands", "United States"]` and `market=["Euronext Amsterdam", "New York Stock Exchange", "NASDAQ Global Select"]`. Equities can be selected on `country`, `sector`, `industry_group`, `industry`, `currency`, `exchange`, `mic`, `market` and `market_cap`. **Find [the Notebook](/projects/financedatabase/getting-started).**

### Searching the Database

If the categorization doesn't lead to the results you are looking for, `search` filters on any column via a custom string. If the text is found anywhere in the column, the entry is returned. Searches are not case sensitive unless `case_sensitive=True` is set, `index` searches the symbol and, just like `select`, every argument accepts a list.

```python
# Search for robotics or education companies with equipment on the Frankfurt Stock Exchange
equities.search(
    summary=["Robotics", "Education"],
    industry="Equipment",
    market="Frankfurt",
    index=".F",
)
```

This returns the instruments listed on the Frankfurt Stock Exchange in an industry containing "Equipment" and with "Robotics" or "Education" in their summary. Filtering on `index=".F"` is an alternative way to find the exchange or market you are looking for.

| symbol | name                                                        | currency | sector                 | industry                              | exchange | market                   | country        | market_cap |
|:-------|:------------------------------------------------------------|:---------|:-----------------------|:--------------------------------------|:---------|:-------------------------|:---------------|:-----------|
| 1YO.F  | Yangtze Optical Fibre And Cable Joint Stock Limited Company | EUR      | Information Technology | Networking & Communications Equipment | FRA      | Frankfurt Stock Exchange | China          | Large Cap  |
| 2IU.F  | Boxlight Corporation                                        | EUR      | Information Technology | Networking & Communications Equipment | FRA      | Frankfurt Stock Exchange | United States  | Nano Cap   |
| 49V.F  | Vertiv Holdings Co                                          | EUR      | Industrials            | Electrical Equipment                  | FRA      | Frankfurt Stock Exchange | United States  | Large Cap  |
| A1Z1.F | eEnergy Group Plc                                           | EUR      | Industrials            | Electrical Equipment                  | FRA      | Frankfurt Stock Exchange | United Kingdom | Nano Cap   |
| A8B.F  | Ambarella, Inc.                                             | EUR      | Information Technology | Semiconductors & Chip Equipment       | FRA      | Frankfurt Stock Exchange | United States  | Mid Cap    |

And below the results are counted per industry.

{% include ft-chart.html id="search" src="/assets/data/financedatabase-charts.json" label="Frankfurt search results per industry" %}

The `search` function works on every column of every asset class, including `name`, `isin`, `cusip` and `figi`. **Find [the Notebook](/projects/financedatabase/getting-started).**

### Exploring Other Asset Classes

All of these functions are also available for the other asset classes. The only difference is the class name and the columns. For example, ETFs use `fd.ETFs()` and are selected on `category_group`, `category` and `family` instead.

```python
# Initialize the ETFs database
etfs = fd.ETFs()

# Select the Fixed Income ETFs of Vanguard
etfs.select(
    category_group="Fixed Income",
    family="Vanguard Asset Management",
)
```

For example, see some of the Vanguard bond ETFs listed in Berlin below:

| symbol   | name                                                            | currency   | category_group   | category               | family                    | exchange   |
|:---------|:----------------------------------------------------------------|:-----------|:-----------------|:-----------------------|:--------------------------|:-----------|
| 0250.BE  | Vanguard Intermediate-Term Corporate Bond Index Fund ETF Shares | EUR        | Fixed Income     | Corporate Bonds        | Vanguard Asset Management | BER        |
| 0251.BE  | Vanguard Short-Term Corporate Bond Index Fund ETF Shares        | EUR        | Fixed Income     | Corporate Bonds        | Vanguard Asset Management | BER        |
| 0252.BE  | Vanguard Total World Bond ETF                                   | EUR        | Fixed Income     | Investment Grade Bonds | Vanguard Asset Management | BER        |
| 025L.BE  | Vanguard Total International Bond Index Fund ETF Shares         | EUR        | Fixed Income     | Investment Grade Bonds | Vanguard Asset Management | BER        |
| 025N.BE  | Vanguard Long-Term Corporate Bond Index Fund ETF Shares         | EUR        | Fixed Income     | Corporate Bonds        | Vanguard Asset Management | BER        |

The same applies to `search`, for example to find semiconductor indices across providers and countries:

```python
# Initialize the Indices database
indices = fd.Indices()

# Search for indices with "Semiconductor" in their name
indices.search(name="Semiconductor")
```

Which returns semiconductor indices from the US, South Korea and Taiwan, including their price, net and total return variants, of which a few are shown below:

| symbol   | name                                | currency | category_group         | category   | exchange |
|:---------|:------------------------------------|:---------|:-----------------------|:-----------|:---------|
| ^SOX     | PHLX Semiconductor                  | USD      | Information Technology | Technology | NIM      |
| ^ICESEMI | ICE Semiconductor Index             | USD      | Information Technology | Technology | NYS      |
| ^NQSSSE  | Nasdaq US Smart Semiconductor Index | USD      | Information Technology | Technology | NIM      |
| ^KQ47    | Kosdaq Semiconductors Index         | KRW      | Information Technology | Technology | KOE      |
| SEC.TW   | TSEC semiconductor subindex         | TWD      | Information Technology | Technology | TAI      |

And below all actively listed ETFs are divided over their category groups.

{% include ft-chart.html id="etfs" src="/assets/data/financedatabase-charts.json" label="Actively listed ETFs per category group" %}

The categories of each asset class can again be found with `show_options`, e.g. `fd.Indices().show_options(selection="category")` returns the index categories, from 'Corporate Bonds' and 'Emerging Markets' to 'Small Cap' and 'Value'. Cryptocurrencies are selected on `cryptocurrency` and `currency` and currencies on `base_currency` and `quote_currency`. **Find [the Notebook](/projects/financedatabase/getting-started).**

### Combining with the Finance Toolkit

The Finance Database has a direct integration with the [Finance Toolkit](/projects/financetoolkit), making it possible to do financial analysis on the instruments you've found. Any selection can be loaded into the Finance Toolkit with `to_toolkit`.

To be able to get started, you need to obtain an API Key from FinancialModelingPrep. This gives access to 30+ years of financial statements, both annual and quarterly. Note that the Free plan is limited to 250 requests each day, 5 years of data and only features companies listed on US exchanges.

[Obtain an API Key from FinancialModelingPrep](/fmp){: .btn .btn--warning .btn--large .align-center target="_blank"}

Returning to the three large insurance companies in the Netherlands:

```python
# Select the large insurance companies on Euronext Amsterdam
dutch_insurance_companies = equities.select(
    country="Netherlands",
    industry="Insurance",
    market="Euronext Amsterdam",
    market_cap="Large Cap",
)

# Load them into the Finance Toolkit
toolkit = dutch_insurance_companies.to_toolkit(
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2017-12-31",
)

# Obtain historical market data for all tickers
historical_data = toolkit.get_historical_data()

# Select the results for ASR Nederland
historical_data.xs("ASRNL.AS", axis=1, level=1)
```

For example, a portion of the historical data for ASR Nederland is shown below.

| date       |   Open |   High |   Low |   Close |   Adj Close |   Volume |   Dividends |   Return |   Cumulative Return |
|:-----------|-------:|-------:|------:|--------:|------------:|---------:|------------:|---------:|--------------------:|
| 2026-10-05 |  71.5  |  72.36 | 71.4  |   72.16 |       72.16 |   375435 |           0 |   0.0095 |              3.4346 |
| 2026-10-06 |  72.44 |  73.24 | 72.4  |   72.62 |       72.62 |   430005 |           0 |   0.0064 |              3.4564 |
| 2026-10-07 |  72.56 |  72.58 | 71.8  |   71.88 |       71.88 |   356698 |           0 |  -0.0102 |              3.4212 |
| 2026-10-08 |  71.52 |  72.1  | 71.1  |   71.32 |       71.32 |   504492 |           0 |  -0.0078 |              3.3946 |
| 2026-10-09 |  71.84 |  71.9  | 71.38 |   71.48 |       71.48 |   285470 |           0 |   0.0022 |              3.4022 |

And below the cumulative returns of Aegon, ASR Nederland and NN Group are plotted, including the S&P 500 as benchmark.

{% include ft-chart.html id="toolkit" src="/assets/data/financedatabase-charts.json" label="Cumulative returns of Aegon, ASR Nederland and NN Group against the S&P 500" %}

Now let's make it more advanced by calculating the profitability ratios for each company:

```python
# Collect all Profitability Ratios for all tickers
profitability_ratios = toolkit.ratios.collect_profitability_ratios()

# Select the results for ASR Nederland
profitability_ratios.loc["ASRNL.AS"]
```

For example, see some of the profitability ratios of ASR Nederland below.

|                                 |   2018 |   2019 |   2020 |   2021 |    2022 |   2023 |   2024 |   2025 |
|:--------------------------------|-------:|-------:|-------:|-------:|--------:|-------:|-------:|-------:|
| Net Profit Margin               | 0.1055 | 0.116  | 0.0811 | 0.091  |  0.1666 | 0.0814 | 0.0427 | 0.024  |
| Income Before Tax Profit Margin | 0.1564 | 0.1515 | 0.1104 | 0.1231 |  0.2202 | 0.1089 | 0.0688 | 0.0328 |
| Effective Tax Rate              | 0.2168 | 0.1983 | 0.2075 | 0.2233 |  0.2609 | 0.2181 | 0.2699 | 0.1882 |
| Return on Assets                | 0.0107 | 0.0144 | 0.0083 | 0.0118 | -0.0259 | 0.0098 | 0.0061 | 0.0036 |
| Return on Equity                | 0.1118 | 0.16   | 0.0982 | 0.1305 | -0.2591 | 0.1427 | 0.0969 | 0.0552 |

And below these and other profitability ratios of ASR Nederland, each with its latest value, the change over the period and its trend.

{% include ft-chart.html id="ratios" src="/assets/data/financedatabase-charts.json" label="Profitability ratios of ASR Nederland" %}

This works for the other asset classes too. For example, Ethereum quoted in BTC, CAD, EUR, GBP and USD can be loaded with `fd.Cryptos().select(cryptocurrency="ETH").to_toolkit(api_key="FINANCIAL_MODELING_PREP_KEY")`, after which `get_historical_data(period="quarterly")` returns its quarterly returns in each currency. **This is just a small snippet of what is available within the Finance Toolkit. For more information, see [the Finance Toolkit page](/projects/financetoolkit) or [the example Notebook](/projects/financetoolkit/getting-started).**

## MCP Server
{: .heading-as-h1}
The Finance Database MCP Server gives any AI assistant that supports the [Model Context Protocol](https://modelcontextprotocol.io){:target="_blank"} (MCP), such as Claude, Copilot, Cursor or Windsurf, direct access to the equities, ETFs, indices, currencies and cryptocurrencies in the database. Ask in plain English for, say, every mid cap semiconductor company in Taiwan or the bond ETFs of a given issuer, and the assistant queries the database on your behalf. Filter values ignore accents and accept common synonyms, so 'Holland', 'Tech' or 'megacap' work just as well as 'Netherlands', 'Information Technology' or 'Mega Cap'. No API key is needed.

Connect to the hosted server at `https://financedatabase.jeroenbouma.com/mcp` with nothing to install, or run it locally with `uvx --from "financedatabase[mcp]" financedatabase-mcp-setup`, which adds the server to your client's configuration automatically. Combine it with the [Finance Toolkit MCP Server](/projects/financetoolkit/mcp) to go from a list of symbols to their financial statements, ratios and prices.

[Explore the Finance Database MCP Server](/projects/financedatabase/mcp){: .btn .btn--warning .btn--large .align-center}

## Questions & Answers
{: .heading-as-h1}
This section includes frequently asked questions. If you have any questions that are not answered here, consider creating an [Issue](https://github.com/JerBouma/FinanceDatabase/issues){:target="_blank"} or reach out to me via the contact details below.

> **How is the data obtained?**

The data is an aggregation of publicly available sources: the official listing directories that exchanges publish (such as Nasdaq Trader, HKEX, NSE, the Japan Exchange Group, ASX, TSX, Deutsche Börse Xetra, Euronext and SIX Swiss Exchange), open reference data (OpenFIGI, SEC EDGAR, the ISO 4217 currency lists, CoinGecko) and contributions from the community. I strictly maintain the rule that all data in this database must be freely accessible to everyone. Data requiring paid subscriptions is never included. Information that companies charge for is typically owned and maintained by those companies, making public sharing of such data a violation of their Terms of Service (ToS). However, publicly available data can be freely shared (read more about [the legality of web scraping](https://techcrunch.com/2022/04/18/web-scraping-legal-court/){:target="_blank"}). This database will always remain <u>completely free</u>.

> **What categorization method is used?**

Equities are classified in this database's own three levels: 11 sectors, which are divided into industry groups and then industries. Every valid combination is listed in [`scripts/categories.json`](https://github.com/JerBouma/FinanceDatabase/blob/main/scripts/categories.json){:target="_blank"}. The categories are curated by hand and from public sources, and the weekly update classifies new companies the same way. All categorizations in the database are independently developed and can be freely modified.

> **How can I find out which countries, sectors and/or industries exist within the database without needing to check the database manually?**

For this you can use the `show_options` function, either for an asset class as a whole (`fd.show_options("equities")`), which doesn't require any data to be loaded, or on a loaded asset class to see the options that remain after filtering. See [Exploring the Options](#exploring-the-options) for more information.

> **When I try to collect data I notice that not all tickers return output, why is that?**

Some tickers are merely holdings of companies and therefore do not really have any data attached to them. Therefore, it makes sense that not all tickers return data. If you are still in doubt, search the ticker on Google to see if there is really no data available. If you can't find anything about the ticker, consider updating the database by visiting the [Contributing Guidelines](https://github.com/JerBouma/FinanceDatabase/blob/main/CONTRIBUTING.md){:target="_blank"}.

> **How is the database kept up to date?**

Every Sunday (and after every change to the database) an automated update runs on GitHub Actions:

| Asset class | What the weekly update does | Source |
|:--|:--|:--|
| **Equities** | Adds new listings on NASDAQ, NYSE and NYSE American and refreshes their market cap tiers; adds new equities in Hong Kong, India, Japan, Australia and Canada. A ticker that is replaced by a new one is marked delisted. Bonds, notes, warrants and other papers that are not company shares are kept out. | [US-Stock-Symbols](https://github.com/rreichel3/US-Stock-Symbols){:target="_blank"}, HKEX, NSE, JPX, ASX, TSX/TSXV |
| **ETFs** | Adds new ETFs in the United States, Hong Kong, India, Japan, Canada, Germany (Xetra), Euronext (Amsterdam, Paris, Brussels, Lisbon, Oslo) and Switzerland. A new line of an existing fund takes its name and categories; blank categories are filled from the fund's other listings or, where clearly decisive, from its name. | Nasdaq Trader, HKEX, NSE, JPX, TSX, Deutsche Börse, Euronext, SIX, Börse Frankfurt |
| **Cryptocurrencies** | Adds the coins in the top 500 by market cap against the usual quote currencies and removes coins that are no longer listed anywhere. | CoinGecko |
| **Currencies** | Adds new currencies (such as SLE or ZWG) with their usual pairs and removes withdrawn ones (such as HRK after Croatia adopted the euro). | ISO 4217 (SIX) |
| **Indices** | Adds the indices Euronext publishes and keeps the categories of ETF iNAVs in line with the index they track. | Euronext |

Each source is applied on its own, so a source that is unavailable or changes its format is skipped for that week without affecting the others, and implausible changes (such as a large share of market cap tiers changing at once) are not applied. Before anything is committed, the update is checked against the previous version of the database and undone if it would introduce duplicate symbols, symbols in two asset classes, changed columns or a large loss of rows. Delisted tickers are kept on purpose, marked as delisted, for historical research. The scripts and their rules are described in [scripts/README.md](https://github.com/JerBouma/FinanceDatabase/blob/main/scripts/README.md){:target="_blank"}.

Not everything can be automated. Classifications of existing companies, corporate events outside the automated sources (mergers, renames, migrations) and exchanges without a public listing directory still rely on the community. If you notice outdated information, please consider contributing through the [Contributing Guidelines](https://github.com/JerBouma/FinanceDatabase/blob/main/CONTRIBUTING.md){:target="_blank"}.

> **What happened to Funds and Money Markets?**

Since October 2026, funds and money markets are no longer maintained. Unlike exchange-listed instruments, mutual and money market funds have no public source that keeps them current worldwide, and the data had become outdated (many funds closed or merged, many new ones missing). `fd.Funds()` and `fd.MoneyMarkets()` remain available in the Python package as they are, with a warning when loaded, but they are no longer part of the MCP server. Funds that trade on a stock exchange under a regular ticker, such as listed open-ended funds in China or listed funds on Euronext Amsterdam, were moved to the ETFs so they stay maintained and searchable.

> **Is the data downloaded every time I use the package?**

No. Each dataset is downloaded once and cached in your user cache folder (or the folder set in `FINANCEDATABASE_CACHE_DIR`). Once a day the package checks for a newer version and only downloads it when it changed; offline, the cached copy is used. Queries run lazily with [Polars](https://pola.rs/){:target="_blank"} and return pandas by default, or Polars with `as_pandas=False`, e.g. `equities.select(country="Canada", as_pandas=False)`.

## Contributing
{: .heading-as-h1}
First of all, thank you for taking the time to contribute (or at least read the Contributing Guidelines)!

[Find the Contributing Guidelines](https://github.com/JerBouma/FinanceDatabase/blob/main/CONTRIBUTING.md){: .btn .btn--warning .btn--large .align-center target="_blank"}

The Finance Database serves the role of providing anyone with any type of financial product categorization entirely for free. To achieve this, it relies on community involvement to add, edit and remove tickers over time. This is made easy enough that anyone, even those with a lack of coding experience, can contribute because of the use of CSV files that can be manually edited with ease.

Below are those that made significant contributions to the project. Thank you!

| User              | Contribution |
| ----------------- | ------------ |
| [dokson](https://github.com/dokson){:target="_blank"} | Made very significant contributions to the quality of the database in #138, #139, #140, #141, #142, #143, #144, #145, #146 and #147, added the MIC column (#149), enriched the FIGIs and added 709 missing tickers (#150, #151) and fixed the CI workflows (#154). |
| [JonArnfred](https://github.com/JonArnfred){:target="_blank"} | Built the identifier validation that now checks every pull request (#159), filled missing share class FIGIs (#158), made the database workflow preserve CSV values exactly as written (#166) and fixed the test suite (#160). |
| [AlfaStake](https://github.com/AlfaStake){:target="_blank"} | Added ISIN codes for ETFs (#124) and corrected and enriched 229 equity ISINs (#126). |
| [pettijohn](https://github.com/pettijohn){:target="_blank"} | Added missing currencies and company names from SEC data (#135, #136). |
| [desaijimmy](https://github.com/desaijimmy){:target="_blank"} | Made changes to Equities dataset including the Split of Daimler to Mercedes-Benz and Daimler Trucks |
| [nindogo](https://github.com/nindogo){:target="_blank"} | Introduced a variety of new equities from the Nairobi Securities Exchange and introduced the country Kenya into the dataset. |
| [colin99d](https://github.com/colin99d){:target="_blank"} | Helped in the conversion of the Finance Database package to Object-Oriented, making the code much more efficient. |

## Contact
{: .heading-as-h1}
If you have any questions about the Finance Database or would like to share with me what you have been working on, feel free to reach out to me via:

- **Website**: [jeroenbouma.com](/)
- **LinkedIn:** https://www.linkedin.com/in/boumajeroen/
- **Email:** jer.bouma@gmail.com

If you'd like to support my efforts, either help me out via the [Contributing Guidelines](https://github.com/JerBouma/FinanceDatabase/blob/main/CONTRIBUTING.md){:target="_blank"} or [Sponsor Me](https://github.com/sponsors/JerBouma){:target="_blank"}.

[![Star History Chart](https://star-history.dera.page/svg?repos=JerBouma/FinanceDatabase&type=Date)](https://star-history.dera.page/#JerBouma/FinanceDatabase&Date){:target="_blank"}

{% include ft-charts-script.html %}
