---
permalink: /projects/financedatabase
title: Finance Database
excerpt: The Finance Database features 300.000+ symbols containing Equities, ETFs, Funds, Indices, Currencies, Cryptocurrencies and Money Markets. It therefore allows you to obtain a broad overview of sectors, industries, types of investments and much more.
description: The Finance Database features 300.000+ symbols containing Equities, ETFs, Funds, Indices, Currencies, Cryptocurrencies and Money Markets. It therefore allows you to obtain a broad overview of sectors, industries, types of investments and much more.
classes: wide-sidebar
author_profile: false
redirect_from:
  - /financedatabase
sidebar:
  nav: "financedatabase"
---

As a private investor, the sheer amount of information that can be found on the internet is rather daunting. Trying to understand what type of companies or ETFs are available is incredibly challenging with there being millions of companies and derivatives available on the market. Sure, the most traded companies and ETFs can quickly be found simply because they are known to the public (for example, Microsoft, Tesla, S&P500 ETF or an All-World ETF). However, what else is out there is often unknown.

**This database tries to solve that**. It features 300.000+ symbols containing Equities, ETFs, Funds, Indices, Currencies, Cryptocurrencies and Money Markets. It therefore allows you to obtain a broad overview of sectors, industries, types of investments and much more.

The aim of this database is explicitly _not_ to provide up-to-date fundamentals or stock data as those can be obtained with ease (with the help of this database) by using the [FinanceToolkit](https://github.com/JerBouma/FinanceToolkit). Instead, it gives insights into the products that exist in each country, industry and sector and gives the most essential information about each product. With this information, you can analyse specific areas of the financial world and/or find a product that is hard to find. See for examples on how you can combine this database, and the earlier mentioned packages the section [Examples](#Examples).

Some key statistics of the database:

| Product           | Quantity   | Sectors    | Industries    | Countries | Exchanges |
| ----------------- | ---------- | ---------- | ------------- | --------- | --------- |
| Equities          | 158.429    | 12         | 63            | 111       | 83        | 
| ETFs              | 36.786     | 295        | 22            | 111       | 53        |
| Funds             | 57.881     | 1541       | 52            | 111       | 34        |

| Product           | Quantity  | Category              |
| ----------------- | --------- | --------------------- |
| Currencies        | 2.556     | 175 Currencies        |
| Cryptocurrencies  | 3.367     | 352 Cryptocurrencies  |
| Indices           | 91.183    | 64 Exchanges          |
| Money Markets     | 1.367     | 3 Exchanges           |

The Finance Database is used within or referenced by:

<a href="https://openbb.co/"><img width="200" height="100" alt="OpenBB" src="https://github.com/JerBouma/FinanceDatabase/assets/46355364/cff58802-8f6e-48ec-9a5c-1a7795c3522c"></a><a href="https://app.noteable.io/f/242bc47d-9c85-4a30-b6e5-d7d201f6e2d6/Finance+Database.ipynb"><img alt="Noteable" width="200" height="100" src="https://github.com/JerBouma/FinanceDatabase/assets/46355364/1110feb5-3ad8-4f1c-b580-df661df4682d"></a><a href="https://algotrading101.com/learn/financedatabase-python-guide/"><img width="200" height="100" alt="AlgoTrading" src="https://github.com/JerBouma/FinanceDatabase/assets/46355364/4c113348-45fc-45fe-afb5-e043b738ee94"></a><a href="https://twitter.com/pyquantnews/status/1576185955677077504?lang=en"><img width="200" height="100" alt="PyQuantNews" src="https://github.com/JerBouma/FinanceDatabase/assets/46355364/8c9025fb-3830-4f41-95fd-e5e6d0f84758"></a><a href="https://alpha2phi.medium.com/investment-analysis-finance-database-61f47ecfe7ca"><img width="200" height="100" alt="Medium" src="https://github.com/JerBouma/FinanceDatabase/assets/46355364/dfbd0f4c-85eb-4de6-adba-345cb5189f31"></a>


## Installation

Before installation, consider starring the project on GitHub which helps others find the project as well.

<a href="https://github.com/JerBouma/FinanceDatabase"><img width="1353" alt="image" src="https://github.com/JerBouma/FinanceDatabase/assets/46355364/4132edde-72f9-4e32-adfe-8872207f46ff"></a>

To install the FinanceDatabase it simply requires the following:

```
pip install financedatabase -U
```

Then within Python use:

```python
import financedatabase as fd
```

## How-To Guides for the FinanceDatabase

This section contains a list of How-To guides for the Finance Database. These guides are meant to show you how to use the Finance Database and how to combine the Finance Database with financial analysis tools such as the Finance Toolkit. The guides are written in the form of Jupyter Notebooks. You can view the notebooks by clicking on the button below the description.

<div class="row">
<div markdown="1" class="fifty-column-left mobile-max-column-width">

### Getting Started with the Finance Database

The Finance Database itself is an incredibly large dataset that can be difficult to query if you don't know the specifics of how it is structured. This Notebook explains how to use the related package for the Finance Database and how to query it.

[Open the Notebook](/projects/financedatabase/getting-started){: .btn .btn--info}

</div>
<div markdown="1" class="fifty-column-right mobile-max-column-width">

### Query Companies in the Netherlands

As an exercise how to query and find specific data, this Notebook shows how to find all companies in the Netherlands and how to plot a pie chart to show the distribution of companies in each sector.

[Open the Notebook](/projects/financedatabase/querying-netherlands){: .btn .btn--info}

</div>
</div>
<div markdown="1" class="fifty-column-left mobile-max-column-width">

### Perform a Dupont Analysis on Companies

A great use-case for the data found in the Finance Database is to do competitive analysis in which companies are compared that compete for the same market. For example, in case I want to look into the Railroad companies in the United States that are marked as "Large Cap", I can directly search for this with the Finance Database and use the Finance Toolkit to do further research. This Notebook shows how to do that.

[Open the Notebook](/projects/financedatabase/dupont-analysis){: .btn .btn--info}

</div>

<div class="row">
<div markdown="1" class="fifty-column-right mobile-max-column-width">

### Apply Technical Analysis with ETFs

The Finance Database is a great way to find specific ETFs that are hard to find. For example, if you want to find all Biotech ETFs, you can do so with the Finance Database. With that information, it is then possible to do a technical analysis using the Finance Toolkit to get insights, in this case, of how these ETFs moved during the early stages of the Coronacrisis. This Notebook shows how to acquire these ETFs and how to perform a technical analysis on the ETFs.

[Open the Notebook](/projects/financedatabase/technical-analysis){: .btn .btn--info}

</div>
</div>

#  Basic Usage
This section explains in detail how the database can be queried with the related `financedatabase` package, also see the Jupyter Notebook in which you can run the examples also demonstrated here. You can find this document [here](https://www.jeroenbouma.com/projects/financedatabase/getting-started).

Same methods apply to all other asset classes as well. Columns may vary.

```python
import financedatabase as fd

# Initialize the Equities database
equities = fd.Equities()

# Obtain all countries from the database
equities_countries = equities.options('country')

# Obtain all sectors from the database
equities_sectors = equities.options('sector')

# Obtain all industry groups from the database
equities_industry_groups = equities.options('industry_group')

# Obtain all industries from a country from the database
equities_germany_industries = equities.options('industry', country='Germany')

# Obtain a selection from the database
equities_united_states = equities.select(country="United States")

# Obtain a detailed selection from the database
equities_usa_consumer_electronics = equities.select(country="United States", industry="Consumer Electronics")

# Search specific fields from the database with lists
equities_large_biotech = equities.search(
    summary="biotech", market_cap=["Large Cap", "Mega Cap"]
)
```

Scroll down below for a more elaborate explanation and detailed examples.

## Collecting information from the database

Please see the Jupyter Notebook for an elaborate explanation of each asset class. This includes Equities, ETFs, Funds, Indices, Currencies, Cryptocurrencies and Money Markets. You can find this document [here](https://www.jeroenbouma.com/projects/financedatabase/getting-started).

As an example for Equities, If you wish to collect data from all equities you can use the following:

```python
import financedatabase as fd

# Initialize the Equities database
equities = fd.Equities()

# Obtain all data available excluding international exchanges
equities.select()
```

Which returns the following DataFrame:

| symbol   | name                       | currency   | sector      | industry_group                                 | industry        | exchange   | market    | country       | state   | city        | zipcode    | website                         | market_cap   |
|:---------|:---------------------------|:-----------|:------------|:-----------------------------------------------|:----------------|:-----------|:----------|:--------------|:--------|:------------|:-----------|:--------------------------------|:-------------|
| A        | Agilent Technologies, Inc. | USD        | Health Care | Pharmaceuticals, Biotechnology & Life Sciences | Biotechnology   | NYQ        | us_market | United States | CA      | Santa Clara | 95051      | http://www.agilent.com          | Large Cap    |
| AA       | Alcoa Corporation          | USD        | Materials   | Materials                                      | Metals & Mining | NYQ        | us_market | United States | PA      | Pittsburgh  | 15212-5858 | http://www.alcoa.com            | Mid Cap      |
| AAALF    | Aareal Bank AG             | USD        | Financials  | Banks                                          | Banks           | PNK        | us_market | Germany       | nan     | Wiesbaden   | 65189      | http://www.aareal-bank.com      | Small Cap    |
| AAALY    | Aareal Bank AG             | USD        | Financials  | Banks                                          | Banks           | PNK        | us_market | Germany       | nan     | Wiesbaden   | 65189      | http://www.aareal-bank.com      | Small Cap    |
| AABB     | Asia Broadband, Inc.       | USD        | Materials   | Materials                                      | Metals & Mining | PNK        | us_market | United States | NV      | Las Vegas   | 89135      | http://www.asiabroadbandinc.com | Micro Cap    |

This returns approximately 20.000 different equities. Note that by default, only the American exchanges are selected. These are symbols like `TSLA` (Tesla) and `MSFT` (Microsoft) that tend to be recognized by a majority of data providers and therefore is the default. To disable this, you can set the `exclude_exchanges` argument to `False` which then results in approximately 155.000 different symbols. 

Note that the summary column is taken out on purpose to keep it organized for markdown. The summary is however very handy when it comes to querying specific words as found with the following description given for Apple. All of this information is available when you query the database.

Find a more elaborate explanation with `help(equities.select)`:

```text
Help on method select in module financedatabase.equities:

select(country: str = '', sector: str = '', industry: str = '', exclude_exchanges: bool = True, capitalize: bool = True) -> pandas.core.frame.DataFrame method of financedatabase.equities.Equities instance
    Description
    ----
    Returns all equities when no input is given and has the option to give
    a specific set of symbols for the country, sector and/or industry provided.
    
    The data depends on the combination of inputs. For example Country + Sector
    gives all symbols for a specific sector in a specific country.
    
    Input
    ----
    country (string, default is None)
        If filled, gives all data for a specific country.
    sector (string, default is None)
        If filled, gives all data for a specific sector.
    industry (string, default is None)
        If filled, gives all data for a specific industry.
    exclude_exchanges (boolean, default is True):
        Whether you want to exclude exchanges from the search. If False,
        you will receive multiple times the product from different exchanges.
    capitalize (boolean, default is True):
        Whether country, sector and industry needs to be capitalized. By default
        the values always are capitalized as that is also how it is represented
        in the csv files.
    base_url (string, default is GitHub location)
        The possibility to enter your own location if desired.
    use_local_location (string, default False)
        The possibility to select a local location (i.e. based on Windows path)
    
    Output
    ----
    equities_df (pd.DataFrame)
        Returns a dictionary with a selection or all data based on the input.
```

As an example, we can use `equities.options` to obtain specific country, sector and industry options. For we can acquire all industries within the sector `Basic Materials` within the `United States`. This allows us to look at a specific industry in the United States in detail. 

```python
industry_options = equities.options(selection='industry', country="United States", sector="Materials")
```

So with this information in hand, I can now query the industry `Metals & Mining` as follows:

```python
metals_and_mining_companies_usa = equities.select(country="United States", sector="Materials", industry="Metals & Mining")
```

This gives you a DataFrame with the following information:

| symbol   | name                                | currency   | sector    | industry_group   | industry        | exchange   | market    | country       | state   | city            | zipcode    | website                            | market_cap   |
|:---------|:------------------------------------|:-----------|:----------|:-----------------|:----------------|:-----------|:----------|:--------------|:--------|:----------------|:-----------|:-----------------------------------|:-------------|
| AA       | Alcoa Corporation                   | USD        | Materials | Materials        | Metals & Mining | NYQ        | us_market | United States | PA      | Pittsburgh      | 15212-5858 | http://www.alcoa.com               | Mid Cap      |
| AABB     | Asia Broadband, Inc.                | USD        | Materials | Materials        | Metals & Mining | PNK        | us_market | United States | NV      | Las Vegas       | 89135      | http://www.asiabroadbandinc.com    | Micro Cap    |
| AAGC     | All American Gold Corp.             | USD        | Materials | Materials        | Metals & Mining | PNK        | us_market | United States | WY      | Cheyenne        | 82001      | http://www.allamericangoldcorp.com | Nano Cap     |
| ABML     | American Battery Metals Corporation | USD        | Materials | Materials        | Metals & Mining | PNK        | us_market | United States | NV      | Incline Village | 89451      | http://www.batterymetals.com       | Small Cap    |
| ACNE     | Alice Consolidated Mines, Inc.      | USD        | Materials | Materials        | Metals & Mining | PNK        | us_market | United States | ID      | Wallace         | 83873-0469 | nan                                | nan          |

As you can imagine, looking at such a specific selection only yields a few results but picking the entire sector `Materials` would have returned 403 different companies (which excludes exchanges other than the United States).

## Searching the database extensively
All asset classes have the capability to search each column with `search`, for example `equities.search()`. Through how this functionality is developed you can define multiple columns and search throughoutly. For example:

```python
# Collect all Equities Database
equities = fd.Equities()

# Search Multiple Columns
equities.search(summary='automotive', currency='USD', country='Germany')
```

Which returns a selection of the DataFrame that matches all criteria. 

| symbol   | name                                        | currency   | sector                 | industry_group                | industry           | exchange   | market    | country   |   state | city                  |   zipcode | website                   | market_cap   |
|:---------|:--------------------------------------------|:-----------|:-----------------------|:------------------------------|:-------------------|:-----------|:----------|:----------|--------:|:----------------------|----------:|:--------------------------|:-------------|
| AFRMF    | Alphaform AG                                | USD        | Industrials            | Capital Goods                 | Machinery          | PNK        | us_market | Germany   |     nan | Feldkirchen           |     85622 | nan                       | Nano Cap     |
| AUUMF    | Aumann AG                                   | USD        | Industrials            | Capital Goods                 | Machinery          | PNK        | us_market | Germany   |     nan | Beelen                |     48361 | http://www.aumann.com     | Micro Cap    |
| BAMXF    | Bayerische Motoren Werke Aktiengesellschaft | USD        | Consumer Discretionary | Automobiles & Components      | Automobiles        | PNK        | us_market | Germany   |     nan | Munich                |     80788 | http://www.bmwgroup.com   | Large Cap    |
| BASFY    | BASF SE                                     | USD        | Materials              | Materials                     | Chemicals          | PNK        | us_market | Germany   |     nan | Ludwigshafen am Rhein |     67056 | http://www.basf.com       | Large Cap    |
| BDRFF    | Beiersdorf Aktiengesellschaft               | USD        | Consumer Staples       | Household & Personal Products | Household Products | PNK        | us_market | Germany   |     nan | Hamburg               |     20245 | http://www.beiersdorf.com | Large Cap    |

## Storing the database at a different location
If you wish to store the database at a different location (for example your own Fork) you can do so with the variable 
`base_url` which you can find in each of the asset classes. An example would be:
- `fd.Equities(base_url=<YOUR URL>)`

You can also store the database locally and point to your local location with the variable `base_url` and by setting
`use_local_location` to True. An example would be:
- `fd.Equities(base_url=<YOUR PATH>, use_local_location=True)`

# Questions & Answers
In this section you can find answers to commonly asked questions. In case the answer to your question is not here, 
consider creating an [Issue](https://github.com/JerBouma/FinanceDatabase/issues).

- **How is the data obtained?**
    - The data is an aggregation of a variety of sources. The rule that I hold with high regard is that all data needs to be entirely publicly available. Any data that requires API key access or requires a paid tier is never included in this database. Data that you are being charged for is often owned and maintained by the company you have a subscription at and therefore publicly sharing this information online is against their Terms of Service (ToS). However, data that is publicly available can freely be shared (read more about this subject [here](https://techcrunch.com/2022/04/18/web-scraping-legal-court/?guccounter=1&guce_referrer=aHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8&guce_referrer_sig=AQAAAJRZe3F6wCbuO_n8PJ9JtAHpOY4dF2gA_tO0gJF2PhfWUueUcRQataJwNS9FZlp9rH8f8_aiCBfA2v7wlHyXyVLUfMrca4kq0_m6CYSvK7eMk9zuEhnXJOvE0lrHWXSPTtL-lHP8UJD4SyWTpQ2BnCNx-kv3mG7GGn_G_3SGVvhP)) especially since this database will never cost any money.
- **What categorization method is used?**
    - The categorization for Equities is based on a loose approximation of GICS. No actual data is collected from this source and this database merely tries to reflect the sectors and industries as best as possible. This is completely done through manual curation. The actual datasets as curated by MSCI has not been used in the development of any part of this database and remains the most up to date, paid, solution. Other categorizations are entirely developed by the author and can freely be changed.
- **How can I contribute?**
    - Please see the [Contributing Guidelines](https://github.com/JerBouma/FinanceDatabase/blob/main/CONTRIBUTING.md). Thank you!
- **How can I find out which countries, sectors and/or industries exists within the database without needing to check the database manually?**
    - For this you can use the ``options`` function from the package attached to this database. Furthermore, it is also possible to use `equities = fd.Equities()` and then use `equities.options(selection='country')` or specific further with `equities.options(selection='sector', country='United States')`. Please see 
    [this example](#companies-in-the-netherlands)
- **When I try collect data I notice that not all tickers return output, why is that?**
    - Some tickers are merely holdings of companies and therefore do not really have any data attached to them. 
      Therefore, it makes sense that not all tickers return data. If you are still in doubt, search the ticker on 
      Google to see if there is really no data available. If you can't find anything about the ticker, consider updating the database by visiting the [Contributing Guidelines](https://github.com/JerBouma/FinanceDatabase/blob/main/CONTRIBUTING.md).
- **How does the database handle changes to companies over time - like symbol/exchange migration, mergers, bankruptcies, or symbols getting reused?**
    - For the American Exchanges, every Sunday the database automatically updates based on [this repository](https://github.com/rreichel3/US-Stock-Symbols). It also automatically checks if there were any market cap changes and converts assets accordingly. On purpose, most tickers are not removed even after becoming delisted. This is because it can be still of value for research to look into companies that no longer exist. When it comes to further automisation, this is what you usually pay a hefty fee for, think of Bloomberg at over $25.000 a year. Instead of requiring you to pay, this database is meant to be a community-driven project in which you help in identifiyng these companies. As news about migrations, mergers, bankruptcies and similar occur outside of the American exchanges it is up to the community to identify these and/or users to look into writing scripts that help with this. It is important to note that the vast majority of companies do not change as rapidly that this database becomes irrelevant before it is identified, e.g. a company like Facebook changing to META has already been updated. Furthermore, even though a company goes bankrupt, the old ticker is still relevant when it comes to historic data before the bankruptcy.
    
# User Contributions

This section is meant to thank those that contributed to the project. Looking to contribute as well? Have a look [here](https://github.com/JerBouma/FinanceDatabase/blob/main/CONTRIBUTING.md).

| User              | Contribution |
| ----------------- | ------------ | 
| [nindogo](https://github.com/nindogo)        | Introduced a variety of new equities from the Nairobi Securities Exchange and introduced the country Kenya into the dataset. |
| [colin99d](https://github.com/colin99d)        | Helped in the conversion of the Finance Database package to Object-Orientated, making the code much more efficient. |