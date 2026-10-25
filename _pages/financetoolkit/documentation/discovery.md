---
title: Discovery
seo_title: "Discovery Module | Finance Toolkit"
seo_title_suffix: false
excerpt: The Discovery Module contains lists of companies, cryptocurrencies, forex, commodities, etfs and indices including screeners, quotes, performance metrics and more to find and select tickers to use in the Finance Toolkit.
description: "Reference for every function and parameter in the Finance Toolkit's Discovery module: screeners, quotes and lists of stocks, crypto, ETFs and indices."
author_profile: false
permalink: /projects/financetoolkit/docs/discovery
classes: wide-sidebar
layout: single
redirect_from:
    - /discovery
    - /projects/financetoolkit/discovery-notebook
sidebar:
    nav: "financetoolkit-docs-discovery"
---

The Discovery Module contains lists of companies, cryptocurrencies, forex, commodities, ETFs and indices including screeners, quotes, performance metrics and more to find and select tickers to use in the Finance Toolkit.

Use it in Claude, ChatGPT or another AI assistant through the [Finance Toolkit MCP](/projects/financetoolkit/mcp), or install the Python package:

```python
pip install financetoolkit -U
```

{% include algolia.html %}

{% include financetoolkit-getting-started/discovery.md %}

## search_instruments
The search instruments function allows you to search for a company or financial instrument by name. It returns a dataframe with all the symbols that match the query.

An ISIN or CUSIP search returns every listing of the security, most traded first, so the primary listing leads (e.g. AAPL before AAPL.MX). The Market Cap of each listing is in the listing's own currency.

**Also known as:** find companies, lookup stocks, ticker search, instrument search.

**Args:**

- <u>query (str):</u> A query to search for, e.g. 'META'.
- <u>search_method (str, optional):</u> The field to search against. Valid options are 'symbol', 'name',
'cik', 'cusip', and 'isin'. Defaults to 'name'.

**Returns:**

pd.DataFrame: A dataframe with all the symbols that match the query.

**As an example:**

```python
from financetoolkit import Discovery

discovery = Discovery(api_key="FINANCIAL_MODELING_PREP_KEY")

discovery.search_instruments(query='META')
```

Which returns:

| Symbol   | Name             | Currency   | Exchange              | Exchange Code   |
|:---------|:-----------------|:-----------|:----------------------|:----------------|
| MVCO     | Metavesco, Inc.  | USD        | Other OTC             | OTC             |
| MTCR     | Metacrine, Inc.  | USD        | NASDAQ Capital Market | NASDAQ          |
| MEVRUSD  | Metaverse VR USD | USD        | CCC                   | CRYPTO          |
| MCAPUSD  | Meta Capital USD | USD        | CCC                   | CRYPTO          |

---

## get_stock_screener
Screen stocks based on a set of criteria. This can be useful to find companies that match a specific criteria or your analysis. Further filtering can be done by utilising the Finance Toolkit and calculating the relevant ratios to filter by. This can be:

- Market capitalization (market_cap_higher, market_cap_lower)
- Price (price_higher, price_lower)
- Beta (beta_higher, beta_lower)
- Volume (volume_higher, volume_lower)
- Dividend (dividend_higher, dividend_lower)
- Classification (sector, industry, country, exchange, is_etf)

The result is capped at `limit` companies, 1000 by default. Getting back exactly that many means the list was truncated, which is warned about in the log; narrow the criteria or raise the limit to see the remainder.

**Also known as:** filter stocks, financial criteria screener.

**Args:**

- <u>market_cap_higher (int):</u> The minimum market capitalization of the stock in US dollars
(not in millions), e.g. 1_000_000_000 for $1 billion.
- <u>market_cap_lower (int):</u> The maximum market capitalization of the stock in US dollars.
- <u>price_higher (int):</u> The minimum price of the stock.
- <u>price_lower (int):</u> The maximum price of the stock.
- <u>beta_higher (int):</u> The minimum beta of the stock.
- <u>beta_lower (int):</u> The maximum beta of the stock.
- <u>volume_higher (int):</u> The minimum volume of the stock, in shares traded.
- <u>volume_lower (int):</u> The maximum volume of the stock.
- <u>dividend_higher (int):</u> The minimum dividend of the stock, as an amount per share
over the last annual period rather than as a yield.
- <u>dividend_lower (int):</u> The maximum dividend of the stock.
- <u>sector (str &#124; None):</u> The sector to restrict the screen to, e.g. "Energy".
- <u>industry (str &#124; None):</u> The industry to restrict the screen to, e.g. "Biotechnology".
- <u>country (str &#124; None):</u> The two-letter country code to restrict the screen to, e.g. "US".
- <u>exchange (str &#124; None):</u> The exchange code to restrict the screen to, e.g. "NASDAQ".
- <u>is_etf (bool &#124; None):</u> Whether to restrict the screen to ETFs or to exclude them.
- <u>limit (int):</u> The maximum number of companies to return. Defaults to 1000.
- <u>primary_only (bool):</u> Whether to keep only the home listing of each company (on an
exchange in its own country, the most traded one among several) rather than
every listing (e.g. ING in Amsterdam, New York, Toronto and Frankfurt).
Defaults to False.

Market caps are in each listing's own currency in "Market Cap" and in US dollars in
"Market Cap (USD)", which the market cap bounds and the ranking use.

**Returns:**

pd.DataFrame: A dataframe with all the symbols that match the query. An empty
dataframe is returned when nothing matches.

**As an example:**

```python
from financetoolkit import Discovery

discovery = Discovery(api_key="FINANCIAL_MODELING_PREP_KEY")

discovery.get_stock_screener(
    market_cap_higher=1000000,
    market_cap_lower=200000000000,
    price_higher=100,
    price_lower=200,
    beta_higher=1,
    beta_lower=1.5,
    volume_higher=100000,
    volume_lower=2000000,
    dividend_higher=1,
    dividend_lower=2,
    is_etf=False
)
```

Which returns:

| Symbol   | Name                                         |   Market Cap | Sector             | Industry                            |   Beta |   Price |   Dividend |   Volume |   avgVolume | Exchange                | Exchange Code   | Country   | Currency   |   Market Cap (USD) |
|:---------|:---------------------------------------------|-------------:|:-------------------|:------------------------------------|-------:|--------:|-----------:|---------:|------------:|:------------------------|:----------------|:----------|:-----------|-------------------:|
| WPM.TO   | Wheaton Precious Metals Corp.                |  7.68348e+10 | Basic Materials    | Gold                                | 1.243  |  169.18 |     1.0425 |   549294 |      784311 | Toronto Stock Exchange  | TSX             | CA        | CAD        |        5.48769e+10 |
| ODFL     | Old Dominion Freight Line, Inc.              |  3.79958e+10 | Industrials        | Trucking                            | 1.204  |  182.7  |     1.15   |  1993098 |     1766126 | NASDAQ Global Select    | NASDAQ          | US        | USD        |        3.79958e+10 |
| EXPD     | Expeditors International of Washington, Inc. |  2.55055e+10 | Industrials        | Integrated Freight & Logistics      | 1.064  |  196.21 |     1.58   |   989988 |     1040746 | New York Stock Exchange | NYSE            | US        | USD        |        2.55055e+10 |
| IHG      | InterContinental Hotels Group PLC            |  2.37383e+10 | Consumer Cyclical  | Travel Lodging                      | 1.028  |  162.4  |     1.231  |   333742 |      219735 | New York Stock Exchange | NYSE            | GB        | USD        |        2.37383e+10 |
| TOL      | Toll Brothers, Inc.                          |  1.28914e+10 | Consumer Cyclical  | Residential Construction            | 1.302  |  139.9  |     1.03   |   996905 |      996604 | New York Stock Exchange | NYSE            | US        | USD        |        1.28914e+10 |
| RRX      | Regal Rexnord Corporation                    |  9.84697e+09 | Industrials        | Industrial - Machinery              | 1.069  |  147.92 |     1.4    |   833290 |     1254610 | New York Stock Exchange | NYSE            | US        | USD        |        9.84697e+09 |
| TFII     | TFI International Inc.                       |  9.24671e+09 | Industrials        | Trucking                            | 1.469  |  112.5  |     1.88   |   217798 |      316092 | New York Stock Exchange | NYSE            | CA        | USD        |        9.24671e+09 |
| TKR      | The Timken Company                           |  7.57622e+09 | Industrials        | Manufacturing - Tools & Accessories | 1.183  |  109.33 |     1.42   |   836982 |      921212 | New York Stock Exchange | NYSE            | US        | USD        |        7.57622e+09 |
| SSD      | Simpson Manufacturing Co., Inc.              |  7.55594e+09 | Basic Materials    | Construction Materials              | 1.318  |  184.36 |     1.18   |   489272 |      287909 | New York Stock Exchange | NYSE            | US        | USD        |        7.55594e+09 |
| AGCO     | AGCO Corporation                             |  7.43037e+09 | Industrials        | Agricultural - Machinery            | 1.074  |  106.1  |     1.18   |   574467 |     1028668 | New York Stock Exchange | NYSE            | US        | USD        |        7.43037e+09 |
| AWI      | Armstrong World Industries, Inc.             |  7.10776e+09 | Basic Materials    | Construction Materials              | 1.158  |  168.18 |     1.356  |   432292 |      400187 | New York Stock Exchange | NYSE            | US        | USD        |        7.10776e+09 |
| JCOM     | Ziff Davis, Inc.                             |  6.75066e+09 | Technology         | Software - Infrastructure           | 1.0328 |  142.84 |     1.76   |   355657 |      357547 | NASDAQ Global Select    | NASDAQ          | US        | USD        |        6.75066e+09 |
| VCTR     | Victory Capital Holdings, Inc.               |  6.61843e+09 | Financial Services | Asset Management                    | 1.133  |  107.6  |     1.98   |   379475 |      645526 | NASDAQ Global Select    | NASDAQ          | US        | USD        |        6.61843e+09 |
| ENS      | EnerSys                                      |  5.98971e+09 | Industrials        | Electrical Equipment & Parts        | 1.186  |  166.08 |     1.075  |   374598 |      537471 | New York Stock Exchange | NYSE            | US        | USD        |        5.98971e+09 |
| CAKE     | The Cheesecake Factory Incorporated          |  5.39256e+09 | Consumer Cyclical  | Restaurants                         | 1.037  |  108.37 |     1.17   |  1802234 |     1574028 | NASDAQ Global Select    | NASDAQ          | US        | USD        |        5.39256e+09 |
| EXP      | Eagle Materials Inc.                         |  5.35929e+09 | Basic Materials    | Construction Materials              | 1.335  |  174.71 |     1      |   432955 |      442898 | New York Stock Exchange | NYSE            | US        | USD        |        5.35929e+09 |
| SIG      | Signet Jewelers Limited                      |  4.49001e+09 | Consumer Cyclical  | Luxury Goods                        | 1.104  |  117.18 |     1.37   |   860622 |      862382 | New York Stock Exchange | NYSE            | BM        | USD        |        4.49001e+09 |
| MCRI     | Monarch Casino & Resort, Inc.                |  2.01951e+09 | Consumer Cyclical  | Gambling, Resorts & Casinos         | 1.405  |  112.68 |     1.2    |   142490 |      156229 | NASDAQ Global Select    | NASDAQ          | US        | USD        |        2.01951e+09 |
| ALG      | Alamo Group Inc.                             |  1.77915e+09 | Industrials        | Industrial - Machinery              | 1.078  |  146.18 |     1.36   |   208708 |      169615 | New York Stock Exchange | NYSE            | US        | USD        |        1.77915e+09 |

---

## get_stock_list
The stock list function returns a complete list of all the symbols that can be used in the Finance Toolkit. These are over 60.000 symbols.

**Returns:**

pd.DataFrame: A dataframe with all the symbols in the toolkit.

**As an example:**

```python
from financetoolkit import Discovery

discovery = Discovery(api_key="FINANCIAL_MODELING_PREP_KEY")

stock_list = discovery.get_stock_list()

# The total list equals over 60.000 rows
stock_list.iloc[38000:38010]
```

Which returns:

| Symbol        | Name                                             |
|:--------------|:-------------------------------------------------|
| DRNYX         | BNY Mellon New York Tax Exempt Bond Fund, Inc.   |
| DRNZ          | REX Drone ETF                                    |
| DRO.AX        | DroneShield Limited                              |
| DROCX         | Diamond Hill Research Opportunities Fund Class C |
| DROME.AT      | Dromeas S.A.                                     |
| DRON.DE       | Defiance Drone UCITS ETF USD                     |
| DRON.L        | Defiance Drone UCITS ETF USD                     |
| DRONACHRYA.BO | Droneacharya Aerial Innovation                   |
| DRONE.NS      | Drone Destination Ltd.                           |
| DROOF         | Deliveroo plc                                    |

---

## get_stock_shares_float
Returns the shares float for each company. The shares float is the number of shares available for trading for each company. It also includes the number of shares outstanding and the date. The free float is the share of the outstanding shares that is available for trading, as a decimal (0.85 is 85%).

**Returns:**

pd.DataFrame: A dataframe with the shares float for each company.

**As an example:**

```python
from financetoolkit import Discovery

discovery = Discovery(api_key="FINANCIAL_MODELING_PREP_KEY")

shares_float = discovery.get_stock_shares_float()

shares_float.iloc[50000:50010]
```

Which returns:

| Symbol   | Date                |   Free Float |   Float Shares |   Outstanding Shares |
|:---------|:--------------------|-------------:|---------------:|---------------------:|
| IMFP     | NaT                 |     0        |    0           |          2.11197e+06 |
| IMG      | 2026-08-02 20:04:15 |     0.813132 |    7.30965e+06 |          8.9895e+06  |
| IMG.TO   | 2026-10-24 09:52:25 |     0.997654 |    5.6966e+08  |          5.71e+08    |
| IMGI     | NaT                 |     0        |    0           |          1.19912e+10 |
| IMGN     | NaT                 |     0.887214 |    2.47847e+08 |          2.79354e+08 |
| IMGP.L   | 2026-10-23 22:27:50 |     0.980184 |    3.62615e+07 |          3.69946e+07 |
| IMGX     | NaT                 |     0        |    0           |          6.42041e+09 |
| IMH      | 2026-08-05 02:12:51 |     0.57308  |    2.09569e+07 |          3.65689e+07 |
| IMH.BK   | 2026-10-24 08:24:50 |     0.247494 |    5.86566e+07 |          2.37002e+08 |
| IMHC     | NaT                 |     0.217776 |    4.5493e+07  |          2.08898e+08 |

---

## get_sectors_performance
Returns the historical performance of every sector, one column per sector.

The values are the average change of the companies in that sector listed on an exchange (NASDAQ by default) on that date, as a decimal (0.0125 is +1.25%). One API call is made per sector.

Without a date range the API hands back only the earliest days it holds, so the last year up to today is retrieved unless `start_date` and `end_date` say otherwise.

**Args:**

- <u>start_date (str &#124; None):</u> The start date to filter data with, e.g. "2024-01-01".
Defaults to a year ago.
- <u>end_date (str &#124; None):</u> The end date to filter data with, e.g. "2024-12-31".
Defaults to today.
- <u>exchange (str, optional):</u> The exchange whose companies are averaged, "NASDAQ", "NYSE"
or "AMEX". Defaults to "NASDAQ".

**Returns:**

pd.DataFrame: A dataframe with the sectors performance for each sector.

**As an example:**

```python
from financetoolkit import Discovery

discovery = Discovery(api_key="FINANCIAL_MODELING_PREP_KEY")

sectors_performance = discovery.get_sectors_performance()

sectors_performance.tail()
```

Which returns:

| Date       |   Basic Materials |   Communication Services |   Consumer Cyclical |   Consumer Defensive |      Energy |   Financial Services |   Healthcare |   Industrials |   Real Estate |   Technology |    Utilities |
|:-----------|------------------:|-------------------------:|--------------------:|---------------------:|------------:|---------------------:|-------------:|--------------:|--------------:|-------------:|-------------:|
| 2026-10-19 |       0.00875661  |              -0.00107542 |          0.022757   |           0.00868844 | -0.00464467 |          -0.00881873 |  0.000189793 |   -0.00922967 |   -0.017014   |  -0.00402035 | -0.0337457   |
| 2026-10-20 |      -0.000397105 |              -0.00517301 |          0.00326353 |          -0.0077103  | -0.00762765 |           0.0113436  |  0.0203693   |    0.0078808  |    0.0143695  |   0.00333534 |  0.000870726 |
| 2026-10-21 |       0.00524548  |              -0.00377267 |          0.00255038 |           0.00805013 | -0.00226659 |           0.00122279 |  0.0128648   |   -0.00171778 |   -0.010997   |   0.0036553  |  0.00699986  |
| 2026-10-22 |       0.0158222   |              -0.0267501  |         -0.0112764  |           0.0126416  | -0.019561   |           0.0161104  |  0.00804433  |   -0.0265981  |   -0.0313195  |  -0.0187846  | -0.024581    |
| 2026-10-23 |      -0.00121107  |               0.00150168 |         -0.00270255 |          -0.0133687  |  0.0308545  |           0.0101811  | -0.00300935  |    0.00179638 |    0.00460377 |   0.00759818 | -0.00308007  |

---

## get_biggest_gainers
Returns the biggest gainers for the day. This includes the symbol, the name, the price, the change and the change percentage. The change percentage ("Change %") is a decimal (0.0125 is +1.25%).

**Returns:**

pd.DataFrame: A dataframe with the biggest gainers for the day.

**As an example:**

```python
from financetoolkit import Discovery

discovery = Discovery(api_key="FINANCIAL_MODELING_PREP_KEY")

biggest_gainers = discovery.get_biggest_gainers()

biggest_gainers.head(10)
```

Which returns:

| Symbol   |   Price | Name                           |   Change |   Change % | Exchange   |
|:---------|--------:|:-------------------------------|---------:|-----------:|:-----------|
| AIOK     | 12.02   | AI OKTO Corp.                  |   7.77   |   1.82824  | NASDAQ     |
| CLRO     |  3.25   | ClearOne, Inc.                 |   1.33   |   0.692708 | NASDAQ     |
| LYCA     | 30      | Lycia Therapeutics Inc.        |  12      |   0.666667 | NASDAQ     |
| BOLT     |  6.27   | Bolt Biotherapeutics, Inc.     |   2.08   |   0.49642  | NASDAQ     |
| MYND     |  0.24   | Mynd.ai, Inc.                  |   0.0772 |   0.474201 | AMEX       |
| ESLA     |  0.985  | Estrella Immunopharma, Inc.    |   0.2582 |   0.355256 | NASDAQ     |
| GPUS     |  0.1689 | Hyperscale Data, Inc.          |   0.0429 |   0.340476 | AMEX       |
| JYD      |  1.83   | Jayud Global Logistics Limited |   0.45   |   0.326087 | NASDAQ     |
| HTCO     |  1.53   | High-Trend International Group |   0.36   |   0.307692 | NASDAQ     |
| IMC      |  8.99   | IMC Rare Earths Ltd            |   1.99   |   0.284286 | AMEX       |

---

## get_biggest_losers
Returns the biggest losers for the day. This includes the symbol, the name, the price, the change and the change percentage. The change percentage ("Change %") is a decimal (0.0125 is +1.25%).

**Returns:**

pd.DataFrame: A dataframe with the biggest losers for the day.

**As an example:**

```python
from financetoolkit import Discovery

discovery = Discovery(api_key="FINANCIAL_MODELING_PREP_KEY")

biggest_losers = discovery.get_biggest_losers()

biggest_losers.head(10)
```

Which returns:

| Symbol   |   Price | Name                                         |   Change |   Change % | Exchange   |
|:---------|--------:|:---------------------------------------------|---------:|-----------:|:-----------|
| AARD     |  1.39   | Aardvark Therapeutics, Inc. Common Stock     |  -2.56   |  -0.648101 | NASDAQ     |
| SHFS     |  0.1324 | SHF Holdings, Inc.                           |  -0.2105 |  -0.613882 | NASDAQ     |
| KCAI     | 15      | KraneShares China Alpha Index ETF            | -17.055  |  -0.532054 | AMEX       |
| DAVI     |  6      | Davion Healthcare Plc                        |  -5.65   |  -0.484978 | NASDAQ     |
| POM      |  1.17   | Pomdoctor Limited                            |  -0.86   |  -0.423645 | NASDAQ     |
| NCPL     |  1.33   | Netcapital Inc.                              |  -0.9    |  -0.403587 | NASDAQ     |
| ADVGX    |  9.02   | North Square Select Small Cap Fund - Class I |  -5.97   |  -0.398265 | NASDAQ     |
| NANO     |  6.13   | Forge Nano Holdings Inc. Common Stock        |  -3.97   |  -0.393069 | NASDAQ     |
| MGNX     |  2.25   | MacroGenics, Inc.                            |  -1.38   |  -0.380165 | NASDAQ     |
| LNAI     |  0.2946 | Lunai Bioworks Inc.                          |  -0.1754 |  -0.373192 | NASDAQ     |

---

## get_most_active_stocks
Returns the most active stocks for the day. This includes the symbol, the name, the price, the change and the change percentage. The change percentage ("Change %") is a decimal (0.0125 is +1.25%).

**Returns:**

pd.DataFrame: A dataframe with the most active stocks for the day.

**As an example:**

```python
from financetoolkit import Discovery

discovery = Discovery(api_key="FINANCIAL_MODELING_PREP_KEY")

most_active_stocks = discovery.get_most_active_stocks()

most_active_stocks.head(10)
```

Which returns:

| Symbol   |    Price | Name                                     |   Change |   Change % | Exchange   |
|:---------|---------:|:-----------------------------------------|---------:|-----------:|:-----------|
| GPUS     |   0.1689 | Hyperscale Data, Inc.                    |   0.0429 |  0.340476  | AMEX       |
| XXII     |   0.1977 | 22nd Century Group, Inc.                 |  -0.018  | -0.0834492 | NASDAQ     |
| SHFS     |   0.1324 | SHF Holdings, Inc.                       |  -0.2105 | -0.613882  | NASDAQ     |
| NVD      |   4.19   | GraniteShares 2x Short NVDA Daily ETF    |   0.04   |  0.0096386 | NASDAQ     |
| LUCD     |   0.411  | Lucid Diagnostics Inc.                   |   0.0833 |  0.254196  | NASDAQ     |
| SPCX     | 147.49   | Space Exploration Technologies Corp.     |   2.74   |  0.0189292 | NASDAQ     |
| T        |  20.93   | AT&T Inc.                                |  -1.81   | -0.0795954 | NYSE       |
| SOXL     |  83.56   | Direxion Daily Semiconductor Bull 3X ETF |   1.45   |  0.0176592 | AMEX       |
| NU       |  15.16   | Nu Holdings Ltd.                         |   0.43   |  0.0291921 | NYSE       |
| NOK      |   8.14   | Nokia Oyj                                |   0.26   |  0.0329949 | NYSE       |

---

## get_delisted_stocks
The delisted stocks function returns a page of delisted stocks including the IPO and delisted date.

The endpoint hands out at most 100 rows per call, so this is one page of the list rather than the whole of it. Walk `page` upwards until an empty frame comes back to collect everything.

**Args:**

- <u>page (int):</u> The page of results to retrieve, starting at 0. Defaults to 0.
- <u>limit (int):</u> The number of results per page, capped at 100 by the API. Defaults to 100.

**Returns:**

pd.DataFrame: A dataframe with one page of delisted stocks.

**As an example:**

```python
from financetoolkit import Discovery

discovery = Discovery(api_key="FINANCIAL_MODELING_PREP_KEY")

delisted_stocks = discovery.get_delisted_stocks()

delisted_stocks.head(10)
```

Which returns:

| Symbol    | Name                                                     | Exchange   | IPO Date   | Delisted Date   |
|:----------|:---------------------------------------------------------|:-----------|:-----------|:----------------|
| 472230.KQ | SK Securities No.11 SPAC                                 | KOE        | 2024-03-04 | 2026-10-12      |
| 473050.KQ | Yuanta SPAC 15                                           | KOE        | 2024-02-29 | 2026-10-12      |
| 7183.T    | Anshin Guarantor Service Co., Ltd.                       | JPX        | 2015-11-20 | 2026-10-09      |
| 7490.T    | Nissin Shoji Co.,Ltd.                                    | JPX        | 2001-01-19 | 2026-10-09      |
| 9691.T    | Ryomo Systems Co.,Ltd.                                   | JPX        | 2000-01-06 | 2026-10-09      |
| ACVA      | ACV Auctions Inc.                                        | NYSE       | 2021-03-24 | 2026-10-16      |
| ADDS      | Hedgeye Index Adds ETF                                   | AMEX       | 2026-05-28 | 2026-10-20      |
| AELV      | Harbor AlphaEdge Large Cap Value ETF                     | AMEX       | 2026-08-31 | 2026-10-15      |
| ALARF.PA  | Adeunis Société anonyme                                  | PAR        | 2017-10-16 | 2026-10-15      |
| ALBG      | Themes ETF Trust - Leverage Shares 2X Long ALB Daily ETF | NASDAQ     | 2026-01-13 | 2026-10-20      |

---

## get_crypto_list
The crypto list function returns a complete list of all crypto symbols that can be used in the Finance Toolkit. These are over 4.000 symbols.

**Returns:**

pd.DataFrame: A dataframe with all the symbols in the toolkit.

**As an example:**

```python
from financetoolkit import Discovery

discovery = Discovery(api_key="FINANCIAL_MODELING_PREP_KEY")

crypto_list = discovery.get_crypto_list()

crypto_list.head(10)
```

Which returns:

| Symbol       | Name                                 | Exchange   | ICO Date   |   Circulating Supply |   Total Supply |
|:-------------|:-------------------------------------|:-----------|:-----------|---------------------:|---------------:|
| .ALPHAUSD    | .Alpha USD                           | CCC        | 2022-03-16 |          0           |  nan           |
| 00USD        | 00 Token USD                         | CCC        | 2022-10-11 |          2.32688e+08 |    1e+09       |
| 0NEUSD       | Stone USD                            | CCC        | 2022-04-26 |          9.77209e+14 |    9.77213e+14 |
| 0X0USD       | 0x0.ai USD                           | CCC        | 2023-01-31 |          8.68563e+08 |    8.9125e+08  |
| 0X1USD       | 0x1.tools: AI Multi-tool Plaform USD | CCC        | 2023-01-04 |          0           |  nan           |
| 0XAUSD       | 0xApe USD                            | CCC        | 2022-11-26 |          0           |  nan           |
| 0XBTCUSD     | 0xBitcoin USD                        | CCC        | 2018-06-04 |          9.70675e+06 |    2.09989e+07 |
| 0XENCRYPTUSD | Encryption AI USD                    | CCC        | 2023-04-27 |          8.68563e+08 |  nan           |
| 0XGASUSD     | 0xGasless USD                        | CCC        | 2023-06-07 |          9.52864e+06 |  nan           |
| 0XMRUSD      | 0xMonero USD                         | CCC        | 2022-09-01 |          1.86525e+06 |    1.86525e+06 |

---

## get_forex_list
The forex list function returns a complete list of all forex symbols that can be used in the Finance Toolkit. These are over 1.000 symbols.

**Returns:**

pd.DataFrame: A dataframe with the forex symbols.

**As an example:**

```python
from financetoolkit import Discovery

discovery = Discovery(api_key="FINANCIAL_MODELING_PREP_KEY")

forex_list = discovery.get_forex_list()

forex_list.head(10)
```

Which returns:

| Symbol   | From Currency   | To Currency   | From Name                   | To Name                |
|:---------|:----------------|:--------------|:----------------------------|:-----------------------|
| AEDAUD   | AED             | AUD           | United Arab Emirates Dirham | Australian Dollar      |
| AEDBHD   | AED             | BHD           | United Arab Emirates Dirham | Bahraini Dinar         |
| AEDCAD   | AED             | CAD           | United Arab Emirates Dirham | Canadian Dollar        |
| AEDCHF   | AED             | CHF           | United Arab Emirates Dirham | Swiss Franc            |
| AEDDKK   | AED             | DKK           | United Arab Emirates Dirham | Danish Krone           |
| AEDEUR   | AED             | EUR           | United Arab Emirates Dirham | Euro                   |
| AEDGBP   | AED             | GBP           | United Arab Emirates Dirham | British Pound Sterling |
| AEDILS   | AED             | ILS           | United Arab Emirates Dirham | Israeli New Shekel     |
| AEDINR   | AED             | INR           | United Arab Emirates Dirham | Indian Rupee           |
| AEDJOD   | AED             | JOD           | United Arab Emirates Dirham | Jordanian Dinar        |

---

## get_commodity_list
The commodity list function returns a complete list of all commodity symbols that can be used in the Finance Toolkit.

**Returns:**

pd.DataFrame: A dataframe with all the commodities available.

**As an example:**

```python
from financetoolkit import Discovery

discovery = Discovery(api_key="FINANCIAL_MODELING_PREP_KEY")

commodity_list = discovery.get_commodity_list()

commodity_list.head(10)
```

Which returns:

| Symbol   | Name                   |   Exchange | Trade Month   | Currency   |
|:---------|:-----------------------|-----------:|:--------------|:-----------|
| ALIUSD   | Aluminum Futures       |        nan | Jan           | USD        |
| BZUSD    | Brent Crude Oil        |        nan | Dec           | USD        |
| CCUSD    | Cocoa                  |        nan | Dec           | USD        |
| CLUSD    | Crude Oil              |        nan | Dec           | USD        |
| CTUSX    | Cotton                 |        nan | Dec           | USX        |
| DCUSD    | Class III Milk Futures |        nan | Nov           | USD        |
| DXUSD    | US Dollar              |        nan | Sep           | USD        |
| ESUSD    | E-Mini S&P 500         |        nan | Dec           | USD        |
| GCUSD    | Gold Futures           |        nan | Dec           | USD        |
| GFUSX    | Feeder Cattle Futures  |        nan | Jan           | USX        |

---

## get_etf_list
The etf list function returns a complete list of all etf symbols that can be used in the Finance Toolkit.

**Returns:**

pd.DataFrame: A dataframe with all the etf symbols.

**As an example:**

```python
from financetoolkit import Discovery

discovery = Discovery(api_key="FINANCIAL_MODELING_PREP_KEY")

etf_list = discovery.get_etf_list()

etf_list.head(10)
```

Which returns:

| Symbol    | Name                                               |
|:----------|:---------------------------------------------------|
| 0050.TW   | Yuanta/P-shares Taiwan Top 50 ETF                  |
| 00981A.TW | UPAMC Taiwan Stock Growth Active ETF Units         |
| 00XL.DE   | WisdomTree Copper - EUR Daily Hedged               |
| 00XP.DE   | WisdomTree Natural Gas - EUR Daily Hedged          |
| 00XR.DE   | WisdomTree Silver - EUR Daily Hedged               |
| 00XS.DE   | WisdomTree Wheat - EUR Daily Hedged                |
| 00XT.DE   | WisdomTree Brent Crude Oil - EUR Daily Hedged      |
| 020Y.L    | iShares € Govt Bond 20yr Target Duration UCITS ETF |
| 069500.KS | Samsung KODEX 200 ETF                              |
| 069660.KS | Kiwoom KIWOOM 200 ETF                              |

---

## get_index_list
The index list function returns a complete list of all index symbols that can be used in the Finance Toolkit.

**Returns:**

pd.DataFrame: A dataframe with all the index symbols.

**As an example:**

```python
from financetoolkit import Discovery

discovery = Discovery(api_key="FINANCIAL_MODELING_PREP_KEY")

index_list = discovery.get_index_list()

index_list.head(10)
```

Which returns:

| Symbol          | Name                                          | Exchange   | Currency   |
|:----------------|:----------------------------------------------|:-----------|:-----------|
| 000001.SS       | SSE Composite Index                           | SHH        | CNY        |
| 399967.SZ       | CSI National Defense                          | SHZ        | CNY        |
| 512.HK          | CES China HK Mainland Index                   | HKSE       | HKD        |
| DE000SLA30S3.SG | Solactive Equal Weight Canada Oil & Gas Index | STU        | EUR        |
| DX-Y.NYB        | US Dollar Index                               | ICEF       | USD        |
| FTSEMIB.MI      | FTSE MIB Index                                | MIL        | EUR        |
| IDX30.JK        | IDX30                                         | JKT        | IDR        |
| IMOEX.ME        | MOEX Russia Index                             | MCX        | RUB        |
| ITLMS.MI        | FTSE Italia All-Share Index                   | MIL        | EUR        |
| KOSPI200.KS     | KOSPI 200 Index                               | KSC        | KRW        |

---

## get_index_constituents
Returns the current constituents of an index (the S&P 500, the NASDAQ 100 or the Dow Jones Industrial Average) with their sector, sub-sector, headquarters, the date they were added, CIK and founding year. The symbols make a Toolkit of the whole index, for example to measure market breadth from every constituent (`toolkit.technicals.get_market_breadth`) or to rank them by relative strength.

These are today's members only. Breadth, relative strength or returns of past dates computed from them leave out the companies that were removed from the index since, often after falling behind, so the history is biased towards the survivors (survivorship bias), the more so the further back it goes.

**Also known as:** index members, index constituents, S&P 500 components.

**Args:**

- <u>index (str, optional):</u> "S&P 500", "NASDAQ 100" or "Dow Jones". Defaults to
"S&P 500".

**Returns:**

pd.DataFrame: The constituents, indexed by symbol.

**As an example:**

```python
from financetoolkit import Discovery

discovery = Discovery(api_key="FINANCIAL_MODELING_PREP_KEY")

constituents = discovery.get_index_constituents("Dow Jones")

constituents[["Name", "Sector", "Date Added"]].head()
```

Which returns:

| Symbol   | Name                       | Sector             | Date Added   |
|:---------|:---------------------------|:-------------------|:-------------|
| AAPL     | Apple Inc.                 | Technology         | 2015-03-19   |
| AMGN     | Amgen Inc.                 | Healthcare         | 2020-08-31   |
| AMZN     | Amazon.com, Inc.amazon.com | Consumer Cyclical  | 2024-02-26   |
| AXP      | American Express Company   | Financial Services | 1982-08-30   |
| BA       | The Boeing Company         | Industrials        | 1987-03-12   |

---

## get_stock_news
Returns the latest stock market news articles. This includes the ticker symbol (when applicable), publisher, title, a short snippet, and the article URL.

**Also known as:** stock news feed, market news headlines.

**Args:**

- <u>pages (int, optional):</u> The number of pages to collect, each page is a
separate API call, e.g. pages=5 makes 5 calls. Defaults to 1.
- <u>limit (int, optional):</u> The number of articles to return per page. Defaults to 100.
- <u>start_date (str, optional):</u> The start date to filter data with.
- <u>end_date (str, optional):</u> The end date to filter data with.

**Returns:**

pd.DataFrame: A dataframe with the latest stock market news articles.

**As an example:**

```python
from financetoolkit import Discovery

discovery = Discovery(api_key="FINANCIAL_MODELING_PREP_KEY")

stock_news = discovery.get_stock_news(limit=5)

stock_news[["Symbol", "Publisher", "Title"]]
```

Which returns:

| Published Date      | Symbol   | Publisher       | Title                                                                                                        |
|:--------------------|:---------|:----------------|:-------------------------------------------------------------------------------------------------------------|
| 2026-10-24 14:21:24 | MSFT     | Seeking Alpha   | Microsoft Q1: A $744 Billion AI Reckoning Is Coming                                                          |
| 2026-10-24 14:19:01 | BKNG     | The Motley Fool | Advance Auto Parts vs. Booking Holdings: Which Consumer Stock Is a Better Buy in 2026?                       |
| 2026-10-24 14:15:00 | MGHL     | The Motley Fool | Energy Transfer vs. Kinder Morgan: Which Natural Gas Pipeline Stock Is the Better Buy for the AI Power Boom? |
| 2026-10-24 14:10:02 | AAP      | The Motley Fool | Advance Auto Parts vs. Dick's Sporting Goods: Are Consumers Focusing on Car Repair or Exercise More in 2026? |
| 2026-10-24 14:02:45 | LOT      | MarketBeat      | Lotus Technology Targets EBIT Profitability Before 2030 as Deliveries, Margins Improve                       |

---

## get_general_news
Returns the latest general news articles, spanning macroeconomic and broad market coverage rather than a specific ticker.

**Also known as:** general market news, macro news feed.

**Args:**

- <u>pages (int, optional):</u> The number of pages to collect, each page is a
separate API call, e.g. pages=5 makes 5 calls. Defaults to 1.
- <u>limit (int, optional):</u> The number of articles to return per page. Defaults to 100.

**Returns:**

pd.DataFrame: A dataframe with the latest general news articles.

**As an example:**

```python
from financetoolkit import Discovery

discovery = Discovery(api_key="FINANCIAL_MODELING_PREP_KEY")

general_news = discovery.get_general_news(limit=5)

general_news[["Publisher", "Title"]]
```

Which returns:

| Published Date      | Publisher                     | Title                                                                                 |
|:--------------------|:------------------------------|:--------------------------------------------------------------------------------------|
| 2026-10-24 10:51:32 | Seeking Alpha                 | Setbacks Mounting On The AI Data Center Front                                         |
| 2026-10-24 10:28:42 | Investors Business Daily      | Stock Market Action Plan: A Preelection Week Primer                                   |
| 2026-10-24 09:00:00 | Seeking Alpha                 | Buying Main Street's Pain Won't Work This Time                                        |
| 2026-10-24 08:03:04 | Bloomberg Markets and Finance | Making Advanced MicroChips Takes a Global Ecosystem                                   |
| 2026-10-24 08:00:00 | Market Watch                  | AI fever ignites a boom in thematic ETFs as fund managers hunt for their next big hit |

---

## get_press_releases
Returns the latest official company press releases, such as earnings announcements, mergers, and other corporate communications.

**Also known as:** corporate announcements, company press releases.

**Args:**

- <u>pages (int, optional):</u> The number of pages to collect, each page is a
separate API call, e.g. pages=5 makes 5 calls. Defaults to 1.
- <u>limit (int, optional):</u> The number of articles to return per page. Defaults to 100.
- <u>start_date (str, optional):</u> The start date to filter data with.
- <u>end_date (str, optional):</u> The end date to filter data with.

**Returns:**

pd.DataFrame: A dataframe with the latest company press releases.

**As an example:**

```python
from financetoolkit import Discovery

discovery = Discovery(api_key="FINANCIAL_MODELING_PREP_KEY")

press_releases = discovery.get_press_releases(limit=5)

press_releases[["Symbol", "Publisher", "Title"]]
```

Which returns:

| Published Date      | Symbol   | Publisher     | Title                                                                                                                                                                                        |
|:--------------------|:---------|:--------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 2026-10-24 12:42:00 | FTK      | Newsfile Corp | FTK FINAL DEADLINE: ROSEN, GLOBAL INVESTOR COUNSEL, Encourages Flotek Industries, Inc. Investors to Secure Counsel Before Important October 26 Deadline in Securities Class Action - FTK     |
| 2026-10-24 12:23:00 | HIMS     | Newsfile Corp | HIMS DEADLINE NOTICE: ROSEN, LEADING TRIAL ATTORNEYS, Encourages Hims & Hers Health, Inc. Investors to Secure Counsel Before Important November 2 Deadline in Securities Class Action - HIMS |
| 2026-10-24 12:01:00 | PZZA     | Business Wire | PZZA Deadline: Rosen Law Firm Urges Papa John's International, Inc. (NASDAQ: PZZA) Stockholders to Contact the Firm for Information About Their Rights                                       |
| 2026-10-24 11:20:00 | ASTS     | PRNewsWire    | ASTS Deadline in 20 Days: AST SpaceMobile, Inc Class Action Lawsuit: Investors Face November 13, 2026, Deadline - Kessler Topaz Meltzer & Check, LLP                                         |
| 2026-10-24 11:18:00 | PFE      | Business Wire | Pfizer's 25-Valent Pediatric Pneumococcal Conjugate Vaccine Candidate Shows Robust Phase 2 Data at IDWeek 2026                                                                               |

---

## get_crypto_news
Returns the latest cryptocurrency news articles.

**Also known as:** crypto news feed, digital asset news.

**Args:**

- <u>pages (int, optional):</u> The number of pages to collect, each page is a
separate API call, e.g. pages=5 makes 5 calls. Defaults to 1.
- <u>limit (int, optional):</u> The number of articles to return per page. Defaults to 100.

**Returns:**

pd.DataFrame: A dataframe with the latest cryptocurrency news articles.

**As an example:**

```python
from financetoolkit import Discovery

discovery = Discovery(api_key="FINANCIAL_MODELING_PREP_KEY")

crypto_news = discovery.get_crypto_news(limit=5)

crypto_news[["Symbol", "Publisher", "Title"]]
```

Which returns:

| Published Date      | Symbol   | Publisher    | Title                                                                                                                     |
|:--------------------|:---------|:-------------|:--------------------------------------------------------------------------------------------------------------------------|
| 2026-10-24 14:30:07 | BTCUSD   | Bitcoin      | Bitcoin Price Sinks to $79,146 as Liquidations Rock Weekend Trading                                                       |
| 2026-10-24 14:24:15 | AVAXUSD  | CryptoTicker | Avalanche (AVAX) 10.3 Percent Weaker in Seven Days, Grayscale Opens In-Kind Subscriptions From $235,800: What Matters Now |
| 2026-10-24 14:22:33 | GAINSUSD | Tokenpost    | MemeCore Rises 25.65% to Lead Gains Among Top 90 Cryptocurrencies                                                         |
| 2026-10-24 14:21:36 | XRPUSD   | Tokenpost    | Mason Versluis Puts $5.89 XRP Expectation in Bull-Run Post                                                                |
| 2026-10-24 14:19:04 | WOOUSD   | Tokenpost    | WOO Network Token (WOO) Rose 12.63% in Five Minutes to $0.01195                                                           |

---

## get_forex_news
Returns the latest forex news articles.

**Also known as:** forex news feed, currency market news.

**Args:**

- <u>pages (int, optional):</u> The number of pages to collect, each page is a
separate API call, e.g. pages=5 makes 5 calls. Defaults to 1.
- <u>limit (int, optional):</u> The number of articles to return per page. Defaults to 100.

**Returns:**

pd.DataFrame: A dataframe with the latest forex news articles.

**As an example:**

```python
from financetoolkit import Discovery

discovery = Discovery(api_key="FINANCIAL_MODELING_PREP_KEY")

forex_news = discovery.get_forex_news(limit=5)

forex_news[["Symbol", "Publisher", "Title"]]
```

Which returns:

| Published Date      | Symbol   | Publisher    | Title                                                                   |
|:--------------------|:---------|:-------------|:------------------------------------------------------------------------|
| 2026-10-24 13:05:25 | XAUUSD   | Forexcom     | Gold Does Something it Hasn't Done in a Year, is Larger Risk-Off Afoot? |
| 2026-10-24 03:02:41 | EURUSD   | Action Forex | EUR/USD Weekly Outlook                                                  |
| 2026-10-24 02:55:26 | GBPUSD   | Action Forex | GBP/USD Weekly Outlook                                                  |
| 2026-10-24 02:51:02 | USDCHF   | Action Forex | USD/CHF Weekly Outlook                                                  |
| 2026-10-24 02:46:58 | AUDUSD   | Action Forex | AUD/USD Weekly Report                                                   |

---

## search_stock_news
Searches stock market news articles by one or more ticker symbols.

**Also known as:** ticker news search, company news lookup.

**Args:**

- <u>symbols (str &#124; list[str]):</u> One or more ticker symbols, e.g. "AAPL" or
["AAPL", "MSFT"].
- <u>pages (int, optional):</u> The number of pages to collect, each page is a
separate API call, e.g. pages=5 makes 5 calls. Defaults to 1.
- <u>limit (int, optional):</u> The number of articles to return per page. Defaults to 100.
- <u>start_date (str, optional):</u> The start date to filter data with.
- <u>end_date (str, optional):</u> The end date to filter data with.

**Returns:**

pd.DataFrame: A dataframe with stock news articles matching the given symbols.

**As an example:**

```python
from financetoolkit import Discovery

discovery = Discovery(api_key="FINANCIAL_MODELING_PREP_KEY")

stock_news = discovery.search_stock_news(symbols="AAPL", limit=5)

stock_news[["Symbol", "Publisher", "Title"]]
```

Which returns:

| Published Date      | Symbol   | Publisher        | Title                                                                                                              |
|:--------------------|:---------|:-----------------|:-------------------------------------------------------------------------------------------------------------------|
| 2026-10-24 13:17:00 | AAPL     | The Motley Fool  | Apple Joins Nvidia in the $5 Trillion Club. Here's Which Stock I Think Can Get to $10 Trillion First.              |
| 2026-10-24 11:50:52 | AAPL     | 24/7 Wall Street | PC Sales Just Crashed 21% as AI Eats the World's Memory Chips                                                      |
| 2026-10-24 07:15:37 | AAPL     | 24/7 Wall Street | Apple Just Passed Nvidia as the World's Most Valuable Company on iPhone Duo Day                                    |
| 2026-10-24 03:45:00 | AAPL     | The Motley Fool  | Apple Is One of the Most Profitable Businesses in the World. Here's Why the Stock Is Worth $295 a Share Right Now. |
| 2026-10-23 17:30:02 | AAPL     | The Motley Fool  | Will Apple Take Over Your (Smart) Home?                                                                            |

---

## search_press_releases
Searches company press releases by one or more ticker symbols.

**Also known as:** press release search, corporate announcement lookup.

**Args:**

- <u>symbols (str &#124; list[str]):</u> One or more ticker symbols, e.g. "AAPL" or
["AAPL", "MSFT"].
- <u>pages (int, optional):</u> The number of pages to collect, each page is a
separate API call, e.g. pages=5 makes 5 calls. Defaults to 1.
- <u>limit (int, optional):</u> The number of articles to return per page. Defaults to 100.
- <u>start_date (str, optional):</u> The start date to filter data with.
- <u>end_date (str, optional):</u> The end date to filter data with.

**Returns:**

pd.DataFrame: A dataframe with press releases matching the given symbols.

**As an example:**

```python
from financetoolkit import Discovery

discovery = Discovery(api_key="FINANCIAL_MODELING_PREP_KEY")

press_releases = discovery.search_press_releases(symbols="AAPL", limit=5)

press_releases[["Symbol", "Publisher", "Title"]]
```

Which returns:

| Published Date      | Symbol   | Publisher     | Title                                                                                                                                                                   |
|:--------------------|:---------|:--------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 2026-10-07 07:30:00 | AAPL     | Newsfile Corp | RETRANSMISSION: QIMC Announces Thermogenic Wet-Gas Signature in 86% of Soil-Gas Samples at New Salem-Apple River, Nova Scotia, Next to Its 30% Clean Hydrogen Discovery |
| 2026-10-06 09:00:00 | AAPL     | Newsfile Corp | QIMC Announces Thermogenic Wet-Gas Signature in 86% of Soil-Gas Samples at New Salem-Apple River, Nova Scotia, Next to Its 30% Clean Hydrogen Discovery                 |

---

## search_crypto_news
Searches cryptocurrency news articles by one or more coin/token symbols.

**Also known as:** crypto news search, coin news lookup.

**Args:**

- <u>symbols (str &#124; list[str]):</u> One or more crypto symbols, e.g. "BTCUSD" or
["BTCUSD", "ETHUSD"].
- <u>pages (int, optional):</u> The number of pages to collect, each page is a
separate API call, e.g. pages=5 makes 5 calls. Defaults to 1.
- <u>limit (int, optional):</u> The number of articles to return per page. Defaults to 100.
- <u>start_date (str, optional):</u> The start date to filter data with.
- <u>end_date (str, optional):</u> The end date to filter data with.

**Returns:**

pd.DataFrame: A dataframe with crypto news articles matching the given symbols.

**As an example:**

```python
from financetoolkit import Discovery

discovery = Discovery(api_key="FINANCIAL_MODELING_PREP_KEY")

crypto_news = discovery.search_crypto_news(symbols="BTCUSD", limit=5)

crypto_news[["Symbol", "Publisher", "Title"]]
```

Which returns:

| Published Date      | Symbol   | Publisher    | Title                                                                               |
|:--------------------|:---------|:-------------|:------------------------------------------------------------------------------------|
| 2026-10-24 14:30:07 | BTCUSD   | Bitcoin      | Bitcoin Price Sinks to $79,146 as Liquidations Rock Weekend Trading                 |
| 2026-10-24 14:14:02 | BTCUSD   | CryptoTicker | Ether Below $2,300: Twice as Weak as Bitcoin                                        |
| 2026-10-24 14:05:00 | BTCUSD   | Cointribune  | Bitcoin Sinks to $79,750 As Crypto Liquidations Surge                               |
| 2026-10-24 14:02:02 | BTCUSD   | Tokenpost    | Tether Gets 15 Commitments for Bitcoin (BTC) Mining Toolkit Integrations            |
| 2026-10-24 13:44:36 | BTCUSD   | The Block    | Crypto longs lose $404 million in four hours as bitcoin briefly slips below $80,000 |

---

## search_forex_news
Searches forex news articles by one or more currency pair symbols.

**Also known as:** forex news search, currency pair news lookup.

**Args:**

- <u>symbols (str &#124; list[str]):</u> One or more forex pairs, e.g. "EURUSD" or
["EURUSD", "GBPUSD"].
- <u>pages (int, optional):</u> The number of pages to collect, each page is a
separate API call, e.g. pages=5 makes 5 calls. Defaults to 1.
- <u>limit (int, optional):</u> The number of articles to return per page. Defaults to 100.
- <u>start_date (str, optional):</u> The start date to filter data with.
- <u>end_date (str, optional):</u> The end date to filter data with.

**Returns:**

pd.DataFrame: A dataframe with forex news articles matching the given symbols.

**As an example:**

```python
from financetoolkit import Discovery

discovery = Discovery(api_key="FINANCIAL_MODELING_PREP_KEY")

forex_news = discovery.search_forex_news(symbols="EURUSD", limit=5)

forex_news[["Symbol", "Publisher", "Title"]]
```

Which returns:

| Published Date      | Symbol   | Publisher    | Title                                                                                       |
|:--------------------|:---------|:-------------|:--------------------------------------------------------------------------------------------|
| 2026-10-24 03:02:41 | EURUSD   | Action Forex | EUR/USD Weekly Outlook                                                                      |
| 2026-10-23 14:34:11 | EURUSD   | FX Street    | EUR/USD Weekly Forecast: Next bounce could be a trap                                        |
| 2026-10-23 14:01:37 | EURUSD   | FX Street    | EUR/USD Price Forecast: 200-week SMA offers last line of defense against deeper losses      |
| 2026-10-23 12:51:14 | EURUSD   | FXEmpire     | U.S. Dollar Rebounds As Oil Prices Gain 3%: Analysis For EUR/USD, GBP/USD, USD/CAD, USD/JPY |
| 2026-10-23 09:46:41 | EURUSD   | FX Street    | Euro: Fiscal risks cap upside against US Dollar – BBH                                       |

---

## get_ipo_calendar
Returns the calendar of upcoming and recent initial public offerings (IPOs), including expected pricing, exchange, and share count. This is distinct from the "IPO Date" field on a company's profile, which only shows a single past date.

Note that the date range is limited to a maximum of 90 days.

**Also known as:** IPO pipeline, upcoming listings.

**Args:**

- <u>start_date (str, optional):</u> The start date to filter data with.
- <u>end_date (str, optional):</u> The end date to filter data with.

**Returns:**

pd.DataFrame: A dataframe with upcoming and recent IPOs.

**As an example:**

```python
from financetoolkit import Discovery

discovery = Discovery(api_key="FINANCIAL_MODELING_PREP_KEY")

ipo_calendar = discovery.get_ipo_calendar(start_date="2024-01-01", end_date="2024-06-01")

ipo_calendar.head()
```

Which returns:

| Symbol    | Date                | Date (ISO)               | Company                  | Exchange   | Status   |        Shares | Price Range   |   Deal Size |    Market Cap |
|:----------|:--------------------|:-------------------------|:-------------------------|:-----------|:---------|--------------:|:--------------|------------:|--------------:|
| ARTMS.IS  | 2024-03-03 00:00:00 | 2024-03-04T00:00:00.000Z | ARTEMIS HALI             | IST        | Priced   | nan           | 57.00 - 57.00 |   nan       |   1.20534e+09 |
| 472230.KQ | 2024-03-03 00:00:00 | 2024-03-04T00:00:00.000Z | SK Securities No.11 SPAC | KOE        | Priced   |   3.89671e+06 | 2000 - 2130   |     8.3e+09 |   8.7255e+09  |
| 0JUZ.L    | 2024-03-03 00:00:00 | 2024-03-04T00:00:00.000Z | Edgio, Inc.              | LSE        | Priced   | nan           | 10.07 - 10.07 |   nan       |   9.22057e+08 |
| PLAN.NS   | 2024-03-04 00:00:00 | 2024-03-05T00:00:00.000Z | Platinum Industries Ltd  | NSE        | Priced   |   1.05843e+07 | 171 - 226.75  |     2.4e+09 | nan           |
| 473370.KQ | 2024-03-04 00:00:00 | 2024-03-05T00:00:00.000Z | BNK SPAC 2               | KOE        | Priced   |   4.12776e+06 | 2000 - 2035   |     8.4e+09 |   8.44105e+09 |

---

## get_ipo_disclosures
Returns IPO disclosure filings - the regulatory filings made ahead of an IPO, including filing dates, effectiveness dates, and CIK numbers, with direct links to the official SEC documents.

**Also known as:** pre-IPO SEC filings, IPO regulatory disclosures.

**Args:**

- <u>start_date (str, optional):</u> The start date to filter data with.
- <u>end_date (str, optional):</u> The end date to filter data with.

**Returns:**

pd.DataFrame: A dataframe with IPO disclosure filings.

**As an example:**

```python
from financetoolkit import Discovery

discovery = Discovery(api_key="FINANCIAL_MODELING_PREP_KEY")

ipo_disclosures = discovery.get_ipo_disclosures(start_date="2024-01-01", end_date="2024-06-01")

ipo_disclosures.head()
```

Which returns:

| Symbol   | Filing Date   | Accepted Date   | Effectiveness Date   |        CIK | Form   | URL                                                                                    |
|:---------|:--------------|:----------------|:---------------------|-----------:|:-------|:---------------------------------------------------------------------------------------|
| AAIT     | 2024-05-23    | 2024-05-23      | 2024-05-23           | 0001100663 | CERT   | https://www.sec.gov/Archives/edgar/data/1100663/000141783524000090/8A_Cert_IBMS.pdf    |
| AAIT     | 2024-03-21    | 2024-03-20      | 2024-03-21           | 0001100663 | CERT   | https://www.sec.gov/Archives/edgar/data/1100663/000135445724000177/IBAT_8-ACert.pdf    |
| AAIT     | 2024-03-14    | 2024-03-14      | 2024-03-14           | 0001100663 | CERT   | https://www.sec.gov/Archives/edgar/data/1100663/000141783524000057/8A_Cert_iShares.pdf |
| AAIT     | 2024-05-23    | 2024-05-23      | 2024-05-23           | 0001100663 | CERT   | https://www.sec.gov/Archives/edgar/data/1100663/000141783524000091/8A_Cert_IBHK.pdf    |
| AAIT     | 2024-05-22    | 2024-05-22      | 2024-05-22           | 0001100663 | CERT   | https://www.sec.gov/Archives/edgar/data/1100663/000114336224000162/IBDZIBIK052224.pdf  |

---

## get_ipo_prospectuses
Returns IPO prospectus filings, including public offering price, discounts and commissions, and proceeds before expenses, with links to the official SEC prospectus documents.

**Also known as:** IPO pricing details, S-1/424B4 filings.

**Args:**

- <u>start_date (str, optional):</u> The start date to filter data with.
- <u>end_date (str, optional):</u> The end date to filter data with.

**Returns:**

pd.DataFrame: A dataframe with IPO prospectus filings.

**As an example:**

```python
from financetoolkit import Discovery

discovery = Discovery(api_key="FINANCIAL_MODELING_PREP_KEY")

ipo_prospectuses = discovery.get_ipo_prospectuses(start_date="2024-01-01", end_date="2024-06-01")

ipo_prospectuses.head()
```

Which returns:

| Symbol   | Accepted Date   | Filing Date   | IPO Date   |        CIK |   Public Price Per Share |   Public Price Total |   Discounts and Commissions Per Share |   Discounts and Commissions Total |   Proceeds Before Expenses Per Share |   Proceeds Before Expenses Total | Form   | URL                                                                                   |
|:---------|:----------------|:--------------|:-----------|-----------:|-------------------------:|---------------------:|--------------------------------------:|----------------------------------:|-------------------------------------:|---------------------------------:|:-------|:--------------------------------------------------------------------------------------|
| ACON     | 2024-02-27      | 2024-02-27    | 2022-04-21 | 0001635077 |                     0.58 |           3.0015e+06 |                                  0.04 |                            210105 |                                 0.54 |                          2791.39 | 424B4  | https://www.sec.gov/Archives/edgar/data/1635077/000168316824001189/aclarion_424b4.htm |
| ACONW    | 2024-02-27      | 2024-02-27    | 2024-02-25 | 0001635077 |                     0.58 |           3.0015e+06 |                                  0.04 |                            210105 |                                 0.54 |                          2791.39 | 424B4  | https://www.sec.gov/Archives/edgar/data/1635077/000168316824001189/aclarion_424b4.htm |

---

## get_stock_splits_calendar
Returns the calendar of upcoming and recent stock splits across all companies, including the split date and ratio. Same calendar pattern as the earnings and dividend calendars.

Note that the date range is limited to a maximum of 90 days.

**Also known as:** split schedule, upcoming stock splits.

**Args:**

- <u>start_date (str, optional):</u> The start date to filter data with.
- <u>end_date (str, optional):</u> The end date to filter data with.

**Returns:**

pd.DataFrame: A dataframe with upcoming and recent stock splits.

**As an example:**

```python
from financetoolkit import Discovery

discovery = Discovery(api_key="FINANCIAL_MODELING_PREP_KEY")

splits_calendar = discovery.get_stock_splits_calendar(start_date="2024-01-01", end_date="2024-06-01")

splits_calendar.head()
```

Which returns:

| Symbol    | Date                |   Numerator |   Denominator | Split Type   |
|:----------|:--------------------|------------:|--------------:|:-------------|
| 005810.KS | 2024-03-04 00:00:00 |           3 |             2 | stock-split  |
| 1160.HK   | 2024-03-04 00:00:00 |          73 |            56 | stock-split  |
| 1ET.F     | 2024-03-04 00:00:00 |           1 |             3 | stock-split  |
| DOHOME.BK | 2024-03-04 00:00:00 |          23 |            22 | stock-split  |
| IFBD      | 2024-03-04 00:00:00 |           1 |             8 | stock-split  |

---

## get_sector_performance
Returns sector performance - the average price change, as a decimal (0.0125 means +1.25%), of the companies listed on an exchange (NASDAQ by default) in each sector. Provide exactly one of `date` (a snapshot across all sectors on that date) or `sector` (the historical time series for one sector).

**Also known as:** sector performance snapshot, sector performance history, sector trend.

**Args:**

- <u>date (str, optional):</u> The date to retrieve a snapshot for, e.g. "2024-02-01".
- <u>sector (str, optional):</u> The sector to retrieve the history for, e.g. "Energy".
- <u>start_date (str, optional):</u> The start of the history of one sector. Defaults to a year
ago.
- <u>end_date (str, optional):</u> The end of the history of one sector. Defaults to today.
- <u>exchange (str, optional):</u> The exchange whose companies are averaged, "NASDAQ", "NYSE"
or "AMEX". Defaults to "NASDAQ".

**Returns:**

pd.DataFrame: A dataframe with sector performance, indexed by Sector
(snapshot) or Date (historical).

**As an example:**

```python
from financetoolkit import Discovery

discovery = Discovery(api_key="FINANCIAL_MODELING_PREP_KEY")

sector_snapshot = discovery.get_sector_performance(date="2024-02-01")

sector_snapshot.head()

sector_history = discovery.get_sector_performance(sector="Energy")

sector_history.tail()
```

Which returns:

| Date                | Sector   | Exchange   |   Average Change |
|:--------------------|:---------|:-----------|-----------------:|
| 2026-10-19 00:00:00 | Energy   | NASDAQ     |      -0.00464467 |
| 2026-10-20 00:00:00 | Energy   | NASDAQ     |      -0.00762765 |
| 2026-10-21 00:00:00 | Energy   | NASDAQ     |      -0.00226659 |
| 2026-10-22 00:00:00 | Energy   | NASDAQ     |      -0.019561   |
| 2026-10-23 00:00:00 | Energy   | NASDAQ     |       0.0308545  |

---

## get_industry_performance
Returns industry performance - the average price change, as a decimal (0.0125 means +1.25%), of the companies listed on an exchange (NASDAQ by default) in each industry. Provide exactly one of `date` (a snapshot across all industries on that date) or `industry` (the historical time series for one industry).

**Also known as:** industry performance snapshot, industry performance history, industry trend.

**Args:**

- <u>date (str, optional):</u> The date to retrieve a snapshot for, e.g. "2024-02-01".
- <u>industry (str, optional):</u> The industry to retrieve the history for, e.g. "Biotechnology".
- <u>start_date (str, optional):</u> The start of the history of one industry. Defaults to a year
ago.
- <u>end_date (str, optional):</u> The end of the history of one industry. Defaults to today.
- <u>exchange (str, optional):</u> The exchange whose companies are averaged, "NASDAQ", "NYSE"
or "AMEX". Defaults to "NASDAQ".

**Returns:**

pd.DataFrame: A dataframe with industry performance, indexed by Industry
(snapshot) or Date (historical).

**As an example:**

```python
from financetoolkit import Discovery

discovery = Discovery(api_key="FINANCIAL_MODELING_PREP_KEY")

industry_snapshot = discovery.get_industry_performance(date="2024-02-01")

industry_snapshot.head()

industry_history = discovery.get_industry_performance(industry="Biotechnology")

industry_history.tail()
```

Which returns:

| Date                | Industry      | Exchange   |   Average Change |
|:--------------------|:--------------|:-----------|-----------------:|
| 2026-10-19 00:00:00 | Biotechnology | NASDAQ     |       0.00476346 |
| 2026-10-20 00:00:00 | Biotechnology | NASDAQ     |       0.0238001  |
| 2026-10-21 00:00:00 | Biotechnology | NASDAQ     |       0.00810473 |
| 2026-10-22 00:00:00 | Biotechnology | NASDAQ     |       0.00288922 |
| 2026-10-23 00:00:00 | Biotechnology | NASDAQ     |      -0.00890932 |

---

## get_sector_pe
Returns sector price-to-earnings (P/E) ratios of the companies listed on an exchange (NASDAQ by default) in each sector. Provide exactly one of `date` (a snapshot across all sectors on that date) or `sector` (the historical time series for one sector).

**Also known as:** sector P/E snapshot, sector P/E history, sector valuation trend.

**Args:**

- <u>date (str, optional):</u> The date to retrieve a snapshot for, e.g. "2024-02-01".
- <u>sector (str, optional):</u> The sector to retrieve the history for, e.g. "Energy".
- <u>start_date (str, optional):</u> The start of the history of one sector. Defaults to a year
ago.
- <u>end_date (str, optional):</u> The end of the history of one sector. Defaults to today.
- <u>exchange (str, optional):</u> The exchange whose companies are averaged, "NASDAQ", "NYSE"
or "AMEX". Defaults to "NASDAQ".

**Returns:**

pd.DataFrame: A dataframe with sector P/E ratios, indexed by Sector
(snapshot) or Date (historical).

**As an example:**

```python
from financetoolkit import Discovery

discovery = Discovery(api_key="FINANCIAL_MODELING_PREP_KEY")

sector_pe = discovery.get_sector_pe(date="2024-02-01")

sector_pe.head()

sector_pe_history = discovery.get_sector_pe(sector="Energy")

sector_pe_history.tail()
```

Which returns:

| Date                | Sector   | Exchange   |   PE Ratio |
|:--------------------|:---------|:-----------|-----------:|
| 2026-10-19 00:00:00 | Energy   | NASDAQ     |    14.6685 |
| 2026-10-20 00:00:00 | Energy   | NASDAQ     |    14.5791 |
| 2026-10-21 00:00:00 | Energy   | NASDAQ     |    14.6875 |
| 2026-10-22 00:00:00 | Energy   | NASDAQ     |    14.2938 |
| 2026-10-23 00:00:00 | Energy   | NASDAQ     |    14.8163 |

---

## get_industry_pe
Returns industry price-to-earnings (P/E) ratios of the companies listed on an exchange (NASDAQ by default) in each industry. Provide exactly one of `date` (a snapshot across all industries on that date) or `industry` (the historical time series for one industry).

**Also known as:** industry P/E snapshot, industry P/E history, industry valuation trend.

**Args:**

- <u>date (str, optional):</u> The date to retrieve a snapshot for, e.g. "2024-02-01".
- <u>industry (str, optional):</u> The industry to retrieve the history for, e.g. "Biotechnology".
- <u>start_date (str, optional):</u> The start of the history of one industry. Defaults to a year
ago.
- <u>end_date (str, optional):</u> The end of the history of one industry. Defaults to today.
- <u>exchange (str, optional):</u> The exchange whose companies are averaged, "NASDAQ", "NYSE"
or "AMEX". Defaults to "NASDAQ".

**Returns:**

pd.DataFrame: A dataframe with industry P/E ratios, indexed by Industry
(snapshot) or Date (historical).

**As an example:**

```python
from financetoolkit import Discovery

discovery = Discovery(api_key="FINANCIAL_MODELING_PREP_KEY")

industry_pe = discovery.get_industry_pe(date="2024-02-01")

industry_pe.head()

industry_pe_history = discovery.get_industry_pe(industry="Biotechnology")

industry_pe_history.tail()
```

Which returns:

| Date                | Industry      | Exchange   |   PE Ratio |
|:--------------------|:--------------|:-----------|-----------:|
| 2026-10-19 00:00:00 | Biotechnology | NASDAQ     |    14.4179 |
| 2026-10-20 00:00:00 | Biotechnology | NASDAQ     |    14.6683 |
| 2026-10-21 00:00:00 | Biotechnology | NASDAQ     |    14.7217 |
| 2026-10-22 00:00:00 | Biotechnology | NASDAQ     |    15.0816 |
| 2026-10-23 00:00:00 | Biotechnology | NASDAQ     |    15.0327 |

---

## get_mergers_acquisitions_latest
Returns the most recent mergers and acquisitions deal announcements, including the acquirer and target companies and a link to the underlying SEC filing.

**Also known as:** M&A feed, deal announcements.

**Args:**

- <u>limit (int, optional):</u> The number of results to return. Defaults to 100.
- <u>page (int, optional):</u> The page number to retrieve. Defaults to 0.

**Returns:**

pd.DataFrame: A dataframe with the latest mergers and acquisitions.

**As an example:**

```python
from financetoolkit import Discovery

discovery = Discovery(api_key="FINANCIAL_MODELING_PREP_KEY")

mergers_acquisitions = discovery.get_mergers_acquisitions_latest(limit=5)

mergers_acquisitions[["Company Name", "Targeted Company Name", "Transaction Date"]]
```

Which returns:

| Symbol   | Company Name                            | Targeted Company Name      | Transaction Date   |
|:---------|:----------------------------------------|:---------------------------|:-------------------|
| ADT      | Star Equity Holdings, Inc.              | Star Equity Holdings, Inc. | 2026-10-19         |
| IPXG     | Inflection Point Acquisition Corp. VII* | Intuitive Machines, Inc.   | 2026-10-08         |
| IPXG     | Inflection Point Acquisition Corp. VII* | Intuitive Machines, Inc.   | 2026-10-08         |
| IPXGU    | Inflection Point Acquisition Corp. VII  | Intuitive Machines, Inc.   | 2026-10-08         |
| IPXGW    | Inflection Point Acquisition Corp. VII  | Intuitive Machines, Inc.   | 2026-10-08         |

---

## get_earnings_calendar
Returns the earnings releases of all companies in a date range: the reported and estimated earnings per share (EPS) and revenue. Upcoming releases only have the estimates, so this also shows which companies report in the coming days. This is the market-wide counterpart of Toolkit.get_earnings_calendar, which covers the tickers of a Toolkit instance over their full history.

Note that the date range is limited to a maximum of 90 days.

**Also known as:** earnings season, earnings release dates, upcoming earnings.

**Args:**

- <u>start_date (str, optional):</u> The start date to filter data with.
- <u>end_date (str, optional):</u> The end date to filter data with.

**Returns:**

pd.DataFrame: A dataframe with the earnings releases, sorted by date.

**As an example:**

```python
from financetoolkit import Discovery

discovery = Discovery(api_key="FINANCIAL_MODELING_PREP_KEY")

earnings_calendar = discovery.get_earnings_calendar(start_date="2026-10-01", end_date="2026-10-03")

earnings_calendar.head()
```

Which returns:

| Symbol    | Date                |     EPS |   Estimated EPS |       Revenue |   Estimated Revenue | Last Updated   |
|:----------|:--------------------|--------:|----------------:|--------------:|--------------------:|:---------------|
| 000270.KS | 2026-10-01 00:00:00 | 5550.38 |        5378.62  |   3.08555e+13 |         3.18109e+13 | 2026-10-24     |
| 032350.KS | 2026-10-01 00:00:00 | 1718    |        1718     |   2.12223e+11 |         2.1315e+11  | 2026-10-24     |
| 0ENN.L    | 2026-10-01 00:00:00 |  nan    |           3.09  | nan           |         1.51e+09    | 2026-10-24     |
| 0JZS.L    | 2026-10-01 00:00:00 |    0.86 |           0.755 |   2.0248e+09  |         1.97614e+09 | 2026-10-24     |
| 0OHK.L    | 2026-10-01 00:00:00 |   10    |          11.1   |   7.2503e+09  |         7.10111e+09 | 2026-10-24     |

---

## get_sec_filings_8k
Returns the most recent 8-K filings with the SEC. Companies file an 8-K to announce a material event between their periodic reports, such as results, an acquisition, a change of management or a new financing, which makes the stream of 8-K filings an early signal of company news.

**Also known as:** current reports, material event filings, SEC filings.

**Args:**

- <u>start_date (str, optional):</u> The start date to filter data with. Defaults to 30 days ago.
- <u>end_date (str, optional):</u> The end date to filter data with. Defaults to today.
- <u>limit (int, optional):</u> The number of results to return. Defaults to 100.
- <u>page (int, optional):</u> The page number to retrieve. Defaults to 0.

**Returns:**

pd.DataFrame: A dataframe with the latest 8-K filings.

**As an example:**

```python
from financetoolkit import Discovery

discovery = Discovery(api_key="FINANCIAL_MODELING_PREP_KEY")

filings = discovery.get_sec_filings_8k(start_date="2026-10-01", end_date="2026-10-02", limit=5)

filings[["Accepted Date", "Has Financials", "Final Link"]]
```

Which returns:

| Symbol   | Accepted Date       | Has Financials   | Final Link                                                                           |
|:---------|:--------------------|:-----------------|:-------------------------------------------------------------------------------------|
| EQBK     | 2026-10-02 21:50:55 | True             | https://www.sec.gov/Archives/edgar/data/1227500/000119312526412873/d16704dex991.htm  |
| VST      | 2026-10-02 20:12:47 | False            | https://www.sec.gov/Archives/edgar/data/1692819/000114036126038468/ef20083016_8k.htm |
| CODX     | 2026-10-02 19:38:44 | False            | https://www.sec.gov/Archives/edgar/data/1692415/000149315226045652/form8-k.htm       |
| MOBXW    | 2026-10-02 19:20:24 | False            | https://www.sec.gov/Archives/edgar/data/1855467/000149315226045639/form8-k.htm       |
| CLAYU    | 2026-10-02 19:20:24 | False            | https://www.sec.gov/Archives/edgar/data/1855467/000149315226045639/form8-k.htm       |

---

## get_insider_trading_latest
Returns the most recent trades by company insiders (officers, directors and shareholders owning more than 10%), as reported in their Form 4 filings: who traded, the type of transaction, the number of shares and the price. Insiders know their company best, so clusters of buying in particular can be worth a closer look.

**Also known as:** insider trades, Form 4 filings, insider transactions.

**Args:**

- <u>date (str, optional):</u> Only return the trades filed on this date. Defaults to None,
which returns the most recent trades.
- <u>limit (int, optional):</u> The number of results to return. Defaults to 100.
- <u>page (int, optional):</u> The page number to retrieve. Defaults to 0.

**Returns:**

pd.DataFrame: A dataframe with the latest insider trades.

**As an example:**

```python
from financetoolkit import Discovery

discovery = Discovery(api_key="FINANCIAL_MODELING_PREP_KEY")

insider_trading = discovery.get_insider_trading_latest(limit=5)

insider_trading[["Reporting Name", "Transaction Type", "Securities Transacted", "Price"]]
```

Which returns:

| Symbol   | Reporting Name   | Transaction Type   |   Securities Transacted |    Price |
|:---------|:-----------------|:-------------------|------------------------:|---------:|
| BPRE     | Ruddy Jordan B.  | P-Purchase         |                    2040 |  12.2484 |
| NTRA     | Sheena Jonathan  | S-Sale             |                     200 | 406.5    |
| NTRA     | Sheena Jonathan  | S-Sale             |                     962 | 408.258  |
| NTRA     | Sheena Jonathan  | S-Sale             |                     627 | 409.893  |
| NTRA     | Sheena Jonathan  | S-Sale             |                     605 | 411.317  |

---

