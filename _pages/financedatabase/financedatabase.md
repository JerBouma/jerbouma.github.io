---
permalink: /projects/financedatabase
title: Finance Database
excerpt: The Finance Database features 300.000+ symbols containing Equities, ETFs, Funds, Indices, Currencies, Cryptocurrencies and Money Markets. It therefore allows you to obtain a broad overview of sectors, industries, types of investments and much more.
description: The Finance Database features 300.000+ symbols containing Equities, ETFs, Funds, Indices, Currencies, Cryptocurrencies and Money Markets. It therefore allows you to obtain a broad overview of sectors, industries, types of investments and much more.
classes: wide-no-sidebar
author_profile: false
---

<div class="row">
<div markdown="1" class="fifty-column-left mobile-max-column-width">

As a private investor, the sheer amount of information that can be found on the internet is rather daunting. Trying to understand what type of companies or ETFs are available is incredibly challenging with there being millions of companies and derivatives available on the market. Sure, the most traded companies and ETFs can quickly be found simply because they are known to the public (for example, Microsoft, Tesla, S&P500 ETF or an All-World ETF). However, what else is out there is often unknown.

**This database tries to solve that**. It features 300.000+ symbols containing Equities, ETFs, Funds, Indices, Currencies, Cryptocurrencies and Money Markets. It therefore allows you to obtain a broad overview of sectors, industries, types of investments and much more.

The aim of this database is explicitly _not_ to provide up-to-date fundamentals or stock data as those can be obtained with ease (with the help of this database) by using the [FinanceToolkit](/projects/FinanceToolkit). Instead, it gives insights into the products that exist in each country, industry and sector and gives the most essential information about each product. With this information, you can analyse specific areas of the financial world and/or find a product that is hard to find.


</div>
<div markdown="1" class="fifty-column-right mobile-max-column-width">

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

</div>
</div>

The Finance Database is used within:

<a href="https://openbb.co/"><img src="https://user-images.githubusercontent.com/46355364/229621010-bba16cc4-de85-4921-9d75-b30393aaf74b.png" width="300px" height="100px"></a><a href="https://app.noteable.io/f/242bc47d-9c85-4a30-b6e5-d7d201f6e2d6/Finance+Database.ipynb"><img src="https://user-images.githubusercontent.com/46355364/229618778-2c5f1369-77d5-4fa9-abd1-e79d324a861a.png" width="300px" height="100px"></a>

## Installation
The package `financedatabase` allows you to select specific CSV files as well as search through collected data with a specific query.

You can install the package with the following steps:
1. `pip install financedatabase`
2. (within Python) `import financedatabase as fd`

## Using the Finance Database
This section explains in detail how the database can be queried with the related `financedatabase` package, also see the Jupyter Notebook in which you can run the examples also demonstrated here.

___

<p><b><div align="center">Find code examples of all Asset Classes in the Jupyter Notebook <a href="/projects/financedatabase/getting-started">here</a>.</div></b></p>
___

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

> Apple Inc. designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories worldwide. It also sells various related services. The company offers iPhone, a line of smartphones; Mac, a line of personal computers; iPad, a line of multi-purpose tablets; and wearables, home, and accessories comprising AirPods, Apple TV, Apple Watch, Beats products, HomePod, iPod touch, and other Apple-branded and third-party accessories. It also provides AppleCare support services; cloud services store services; and operates various platforms, including the App Store, that allow customers to discover and download applications and digital content, such as books, music, video, games, and podcasts. In addition, the company offers various services, such as Apple Arcade, a game subscription service; Apple Music, which offers users a curated listening experience with on-demand radio stations; Apple News+, a subscription news and magazine service; Apple TV+, which offers exclusive original content; Apple Card, a co-branded credit card; and Apple Pay, a cashless payment service, as well as licenses its intellectual property. The company serves consumers, and small and mid-sized businesses; and the education, enterprise, and government markets. It sells and delivers third-party applications for its products through the App Store. The company also sells its products through its retail and online stores, and direct sales force; and third-party cellular network carriers, wholesalers, retailers, and resellers. Apple Inc. was founded in 1977 and is headquartered in Cupertino, California.

Find a more elaborate explanation with `help(equities.select)`:

We can use `equities.options` to obtain specific country, sector and industry options. For we can acquire all industries within the sector `Basic Materials` within the `United States`. This allows us to look at a specific industry in the United States in detail. 

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