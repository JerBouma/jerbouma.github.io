---
title: Discovery
seo_title: Discovery Module – Finance Toolkit Docs
excerpt: The Discovery Module contains lists of companies, cryptocurrencies, forex, commodities, etfs and indices including screeners, quotes, performance metrics and more to find and select tickers to use in the Finance Toolkit.
description: "Reference for every function and parameter in the Finance Toolkit's Discovery module: screeners, quotes and lists of stocks, crypto, ETFs and indices."
author_profile: false
permalink: /projects/financetoolkit/docs/discovery
classes: wide-sidebar
layout: single
redirect_from:
    - /discovery
sidebar:
    nav: "financetoolkit-docs-discovery"
---

The Discovery Module contains lists of companies, cryptocurrencies, forex, commodities, ETFs and indices including screeners, quotes, performance metrics and more to find and select tickers to use in the Finance Toolkit.

To install the FinanceToolkit it simply requires the following:

```python
pip install financetoolkit -U
```

{% include algolia.html %}

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

| Symbol   | Name             | Currency   | Exchange                       | Exchange Code   |
|:---------|:-----------------|:-----------|:-------------------------------|:----------------|
| MVCO     | Metavesco, Inc.  | USD        | Other OTC                      | OTC             |
| MTCR     | Metacrine, Inc.  | USD        | NASDAQ Capital Market          | NASDAQ          |
| MEVRUSD  | Metaverse VR USD | USD        | CCC                            | CRYPTO          |
| MCAPUSD  | Meta Capital USD | USD        | CCC                            | CRYPTO          |
| MLX.AX   | Metals X Limited | AUD        | Australian Securities Exchange | ASX             |

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

- <u>market_cap_higher (int):</u> The minimum market capitalization of the stock, in the
currency of the listing rather than in millions.
- <u>market_cap_lower (int):</u> The maximum market capitalization of the stock.
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

| Symbol   | Name                                         |   Market Cap | Sector             | Industry                            |   Beta |   Price |   Dividend |   Volume | Exchange                | Exchange Code   | Country   |
|:---------|:---------------------------------------------|-------------:|:-------------------|:------------------------------------|-------:|--------:|-----------:|---------:|:------------------------|:----------------|:----------|
| JCI      | Johnson Controls International plc           |  94453267417 | Basic Materials    | Construction Materials              | 1.28   |  155.93 |     1.6    |  1850585 | New York Stock Exchange | NYSE            | IE        |
| WPM.TO   | Wheaton Precious Metals Corp.                |  86465416946 | Basic Materials    | Gold                                | 1.242  |  190.4  |     1.0425 |   666411 | Toronto Stock Exchange  | TSX             | CA        |
| ODFL     | Old Dominion Freight Line, Inc.              |  36521310178 | Industrials        | Trucking                            | 1.204  |  175.61 |     1.15   |  1668932 | NASDAQ Global Select    | NASDAQ          | US        |
| EXPD     | Expeditors International of Washington, Inc. |  24961462350 | Industrials        | Integrated Freight & Logistics      | 1.064  |  190.85 |     1.58   |   832787 | New York Stock Exchange | NYSE            | US        |
| IHG      | InterContinental Hotels Group PLC            |  23623790857 | Consumer Cyclical  | Travel Lodging                      | 1.028  |  159.9  |     1.231  |   118360 | New York Stock Exchange | NYSE            | GB        |
| FTT.TO   | Finning International Inc.                   |  13927322149 | Industrials        | Industrial - Distribution           | 1.206  |  106.67 |     1.256  |   391781 | Toronto Stock Exchange  | TSX             | CA        |
| TOL      | Toll Brothers, Inc.                          |  12512028060 | Consumer Cyclical  | Residential Construction            | 1.302  |  133.86 |     1.02   |  1075161 | New York Stock Exchange | NYSE            | US        |
| ALB      | Albemarle Corporation                        |  12117785390 | Basic Materials    | Chemicals - Specialty               | 1.359  |  102.75 |     1.625  |  1930624 | New York Stock Exchange | NYSE            | US        |
| RRX      | Regal Rexnord Corporation                    |  10928726799 | Industrials        | Industrial - Machinery              | 1.069  |  164.17 |     1.4    |  1223281 | New York Stock Exchange | NYSE            | US        |
| TFII     | TFI International Inc.                       |   9234383550 | Industrials        | Trucking                            | 1.474  |  112.35 |     1.88   |   395535 | New York Stock Exchange | NYSE            | CA        |
| AVT      | Avnet, Inc.                                  |   8409929025 | Technology         | Technology Distributors             | 1.082  |  102.53 |     1.42   |   875063 | NASDAQ Global Select    | NASDAQ          | US        |
| TKR      | The Timken Company                           |   7985612995 | Industrials        | Manufacturing - Tools & Accessories | 1.183  |  114.91 |     1.42   |   765869 | New York Stock Exchange | NYSE            | US        |
| AGCO     | AGCO Corporation                             |   7643963439 | Industrials        | Agricultural - Machinery            | 1.074  |  109.15 |     1.18   |  1202778 | New York Stock Exchange | NYSE            | US        |
| SSD      | Simpson Manufacturing Co., Inc.              |   7043699726 | Basic Materials    | Construction Materials              | 1.318  |  171.22 |     1.18   |   358330 | New York Stock Exchange | NYSE            | US        |
| VCTR     | Victory Capital Holdings, Inc.               |   6994104206 | Financial Services | Asset Management                    | 1.134  |  111.85 |     1.98   |   621512 | NASDAQ Global Select    | NASDAQ          | US        |
| AWI      | Armstrong World Industries, Inc.             |   6860101916 | Basic Materials    | Construction Materials              | 1.158  |  162.32 |     1.356  |   411142 | New York Stock Exchange | NYSE            | US        |
| JCOM     | Ziff Davis, Inc.                             |   6750661252 | Technology         | Software - Infrastructure           | 1.0328 |  142.84 |     1.76   |   355657 | NASDAQ Global Select    | NASDAQ          | US        |
| ENS      | EnerSys                                      |   6652878434 | Industrials        | Electrical Equipment & Parts        | 1.186  |  182.49 |     1.075  |   494854 | New York Stock Exchange | NYSE            | US        |
| CAKE     | The Cheesecake Factory Incorporated          |   5315840946 | Consumer Cyclical  | Restaurants                         | 1.037  |  106.99 |     1.17   |   867736 | NASDAQ Global Select    | NASDAQ          | US        |
| EXP      | Eagle Materials Inc.                         |   5138116938 | Basic Materials    | Construction Materials              | 1.335  |  167.5  |     1      |   614728 | New York Stock Exchange | NYSE            | US        |
| SIG      | Signet Jewelers Limited                      |   4065914724 | Consumer Cyclical  | Luxury Goods                        | 1.105  |  103.38 |     1.34   |   600993 | New York Stock Exchange | NYSE            | BM        |
| HCI      | HCI Group, Inc.                              |   2383572598 | Financial Services | Insurance - Property & Casualty     | 1.048  |  186.73 |     1.6    |   148652 | New York Stock Exchange | NYSE            | US        |
| MCRI     | Monarch Casino & Resort, Inc.                |   2117901825 | Consumer Cyclical  | Gambling, Resorts & Casinos         | 1.405  |  118.17 |     1.2    |   249420 | NASDAQ Global Select    | NASDAQ          | US        |
| ALG      | Alamo Group Inc.                             |   1909327953 | Industrials        | Industrial - Machinery              | 1.078  |  156.91 |     1.32   |   112409 | New York Stock Exchange | NYSE            | US        |
| OPY      | Oppenheimer Holdings Inc.                    |   1254113226 | Financial Services | Financial - Capital Markets         | 1.096  |  118.22 |     1.76   |   116502 | New York Stock Exchange | NYSE            | US        |

---

## get_stock_list
The stock list function returns a complete list of all the symbols that can be used in the Finance Toolkit. These are over 60.000 symbols.

Returns: pd.DataFrame: A dataframe with all the symbols in the toolkit.


```python
from financetoolkit import Discovery

discovery = Discovery(api_key="FINANCIAL_MODELING_PREP_KEY")

stock_list = discovery.get_stock_list()

# The total list equals over 60.000 rows
stock_list.iloc[38000:38010]
```

Which returns:

| Symbol   | Name                                 |
|:---------|:-------------------------------------|
| DS-PD    | Drive Shack Inc.                     |
| DS.TO    | Dividend Select 15 Corp.             |
| DS2P.L   | L&G DAX Daily 2x Short UCITS ETF EUR |
| DSAC     | Daedalus Special Acquisition Corp.   |
| DSACU    | Daedalus Special Acquisition Corp.   |
| DSACW    | Daedalus Special Acquisition Corp.   |
| DSAI.CN  | DeepSpatial Inc.                     |
| DSAIF    | DeepSpatial Inc.                     |
| DSAQ     | Direct Selling Acquisition Corp.     |
| DSAQ-UN  | Direct Selling Acquisition Corp.     |

---

## get_stock_shares_float
Returns the shares float for each company. The shares float is the number of shares available for trading for each company. It also includes the number of shares outstanding and the date.

Returns: pd.DataFrame: A dataframe with the shares float for each company.


```python
from financetoolkit import Discovery

discovery = Discovery(api_key="FINANCIAL_MODELING_PREP_KEY")

shares_float = discovery.get_stock_shares_float()

shares_float.iloc[50000:50010]
```

Which returns:

| Symbol        | Date                |   Free Float |   Float Shares |   Outstanding Shares |
|:--------------|:--------------------|-------------:|---------------:|---------------------:|
| INDI          | 2026-10-07 22:37:55 |      98.543  |    2.0821e+08  |          2.11289e+08 |
| INDI.L        | 2026-08-04 14:04:36 |      17.345  |    3.17368e+07 |          1.82974e+08 |
| INDIACEM.BO   | 2026-10-08 04:02:55 |      16.9962 |    5.26707e+07 |          3.09897e+08 |
| INDIACEM.NS   | 2026-10-08 04:22:30 |      16.9962 |    5.26707e+07 |          3.09897e+08 |
| INDIAGLYCO.BO | 2026-10-07 22:54:30 |      35.1773 |    2.35782e+07 |          6.70268e+07 |
| INDIAGLYCO.NS | 2026-10-07 20:18:30 |      35.531  |    2.38153e+07 |          6.70268e+07 |
| INDIAHOME.BO  | 2026-10-07 22:47:20 |      11.1708 |    1.59539e+06 |          1.42818e+07 |
| INDIAHOMES.BO | 2026-10-08 04:07:13 |      89.4614 |    3.56129e+08 |          3.98081e+08 |
| INDIAMART.BO  | 2026-10-07 23:11:10 |      41.9782 |    2.5247e+07  |          6.01431e+07 |
| INDIAMART.NS  | 2026-10-07 22:38:20 |      41.9782 |    2.5247e+07  |          6.01431e+07 |

---

## get_sectors_performance
Returns the historical performance of every sector, one column per sector.

The values are the average percentage change of the companies in that sector on that date, so 1.25 means +1.25% and not +125%. One API call is made per sector because the combined endpoint this used to read was retired and now answers with an empty response.

Without a date range the API hands back only the earliest days it holds, so the last year up to today is retrieved unless `start_date` and `end_date` say otherwise.

**Args:**

- <u>start_date (str &#124; None):</u> The start date to filter data with, e.g. "2024-01-01".
Defaults to a year ago.
- <u>end_date (str &#124; None):</u> The end date to filter data with, e.g. "2024-12-31".
Defaults to today.

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

| Date       |   Basic Materials |   Communication Services |   Consumer Cyclical |   Consumer Defensive |   Energy |   Financial Services |   Healthcare |   Industrials |   Real Estate |   Technology |   Utilities |
|:-----------|------------------:|-------------------------:|--------------------:|---------------------:|---------:|---------------------:|-------------:|--------------:|--------------:|-------------:|------------:|
| 2024-02-26 |           -2.0728 |                  -1.454  |              0.7303 |               0.324  |  -0.1413 |              -0.0491 |       2.7031 |       -1.2333 |        0.4945 |       0.2893 |     -1.5214 |
| 2024-02-27 |            2.8956 |                   1.0041 |             -0.7125 |               0.1136 |   2.5373 |               3.0268 |       9.1978 |       -0.5179 |        0.7542 |       0.0419 |      4.6884 |
| 2024-02-28 |            4.343  |                  -0.8573 |             -0.9692 |              -0.0826 |  -3.6163 |               1.8261 |      -0.9719 |        1.0113 |       -0.2592 |      -0.6251 |      1.6461 |
| 2024-02-29 |           -1.3336 |                   0.7907 |              1.2483 |               3.4536 |   0.6259 |              -0.5633 |      -1.4379 |       -4.1022 |        1.7541 |       1.2096 |      9.9286 |
| 2024-03-01 |            0.8526 |                   0.0092 |              1.5435 |              -3.7427 |   1.399  |              -0.8531 |       2.544  |        0.1322 |        0.1964 |       1.6327 |     -2.0912 |

---

## get_biggest_gainers
Returns the biggest gainers for the day. This includes the symbol, the name, the price, the change and the change percentage.

Returns: pd.DataFrame: A dataframe with the biggest gainers for the day.


```python
from financetoolkit import Discovery

discovery = Discovery(api_key="FINANCIAL_MODELING_PREP_KEY")

biggest_gainers = discovery.get_biggest_gainers()

biggest_gainers.head(10)
```

Which returns:

| Symbol   |   Price | Name                                 |   Change |   Change % | Exchange   |
|:---------|--------:|:-------------------------------------|---------:|-----------:|:-----------|
| CCAQU    | 19.49   | Collective Acquisition Corp.         |   8.81   |    82.4906 | NASDAQ     |
| BIYA     |  2.3    | Baiya International Group Inc.       |   0.935  |    68.4982 | NASDAQ     |
| ALISU    | 16.65   | Calisa Acquisition Corp Units        |   5.84   |    54.0241 | NASDAQ     |
| AMPGZ    |  0.18   | Amplitech Group, Inc. Series B Right |   0.055  |    44      | NASDAQ     |
| BSP      | 41.07   | Bending Spoons S.p.A.                |   8      |    24.1911 | NASDAQ     |
| ALPXR    |  0.1911 | Alpex Acquisition Corp. Rt           |   0.0311 |    19.4375 | NASDAQ     |
| CANG     |  3.58   | Cango Inc.                           |   0.56   |    18.5431 | NYSE       |
| CCG      |  5.77   | Cheche Group Inc.                    |   0.8    |    16.0966 | NASDAQ     |
| AIFU     | 12.85   | AIFU Inc.                            |   1.67   |    14.9374 | NASDAQ     |
| AMBR     |  2.28   | Amber International Holding Ltd      |   0.29   |    14.5729 | NASDAQ     |

---

## get_biggest_losers
Returns the biggest losers for the day. This includes the symbol, the name, the price, the change and the change percentage.

Returns: pd.DataFrame: A dataframe with the biggest losers for the day.


```python
from financetoolkit import Discovery

discovery = Discovery(api_key="FINANCIAL_MODELING_PREP_KEY")

biggest_losers = discovery.get_biggest_losers()

biggest_losers.head(10)
```

Which returns:

| Symbol   |   Price | Name                                                |    Change |   Change % | Exchange   |
|:---------|--------:|:----------------------------------------------------|----------:|-----------:|:-----------|
| BULG     | 21.1116 | Leverage Shares 2x Long BULL Daily ETF              | -12.9859  |   -38.0846 | NASDAQ     |
| AIXI     |  1.32   | Xiao-I Corporation                                  |  -0.53    |   -28.6486 | NASDAQ     |
| AVAT     |  1.66   | Avalanche Treasury Corporation Class A Common Stock |  -0.41    |   -19.8068 | NASDAQ     |
| BULL     |  5.89   | Webull Corporation Class A Ordinary Shares          |  -1.39    |   -19.0934 | NASDAQ     |
| BBUL     | 12.8794 | GraniteShares 2x Long BB Daily ETF                  |  -2.6906  |   -17.2807 | NASDAQ     |
| BRNX     |  1.53   | BrenX Ltd.                                          |  -0.27    |   -15      | NASDAQ     |
| BURU     |  1.03   | Nuburu, Inc.                                        |  -0.17    |   -14.1667 | AMEX       |
| ALMR     | 27.77   | Alamar Biosciences, Inc.                            |  -4.49    |   -13.9182 | NASDAQ     |
| BLIN     |  0.7821 | Bridgeline Digital, Inc.                            |  -0.11035 |   -12.3648 | NASDAQ     |
| CDLX     |  2.28   | Cardlytics, Inc.                                    |  -0.32    |   -12.3077 | NASDAQ     |

---

## get_most_active_stocks
Returns the most active stocks for the day. This includes the symbol, the name, the price, the change and the change percentage.

Returns: pd.DataFrame: A dataframe with the most active stocks for the day.


```python
from financetoolkit import Discovery

discovery = Discovery(api_key="FINANCIAL_MODELING_PREP_KEY")

most_active_stocks = discovery.get_most_active_stocks()

most_active_stocks.head(10)
```

Which returns:

| Symbol   |   Price | Name                                       |   Change |   Change % | Exchange   |
|:---------|--------:|:-------------------------------------------|---------:|-----------:|:-----------|
| AAL      |   12.85 | American Airlines Group Inc.               |  -0.15   |   -1.15385 | NASDAQ     |
| AGNC     |    8.46 | AGNC Investment Corp.                      |  -0.24   |   -2.75862 | NASDAQ     |
| APLD     |   23.81 | Applied Digital Corp.                      |  -1.53   |   -6.03788 | NASDAQ     |
| BBD      |    4.34 | Banco Bradesco S.A.                        |  -0.17   |   -3.7694  | NYSE       |
| BITO     |   11.14 | ProShares Bitcoin ETF                      |  -0.31   |   -2.70742 | AMEX       |
| BIYA     |    2.3  | Baiya International Group Inc.             |   0.935  |   68.4982  | NASDAQ     |
| BULL     |    5.89 | Webull Corporation Class A Ordinary Shares |  -1.39   |  -19.0934  | NASDAQ     |
| CDE      |   16.5  | Coeur Mining, Inc.                         |  -0.67   |   -3.90215 | NYSE       |
| CPHI     |    0.85 | China Pharma Holdings, Inc.                |   0.2089 |   32.5846  | AMEX       |
| CTVA     |   14.45 | Corteva, Inc.                              |   0.54   |    3.8821  | NYSE       |

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

| Symbol   | Name                                                         | Exchange   | IPO Date   | Delisted Date   |
|:---------|:-------------------------------------------------------------|:-----------|:-----------|:----------------|
| 0232.HK  | Continental Aerospace Technologies Holding Limited           | HKSE       | 1991-12-12 | 2026-09-22      |
| 0V4O.L   | Lomiko Metals Inc.                                           | LSE        | 2022-12-07 | 2026-10-06      |
| 1948.T   | The Kodensha Co., Ltd.                                       | JPX        | 2001-01-04 | 2026-09-25      |
| 3856.T   | Abalance Corp                                                | JPX        | 2007-09-19 | 2026-09-25      |
| 4800.T   | Oricon Inc.                                                  | JPX        | 2002-03-21 | 2026-09-25      |
| 7082.T   | Jimoty, Inc.                                                 | JPX        | 2020-02-10 | 2026-09-29      |
| 7426.T   | Yamadai Corporation                                          | JPX        | 1995-02-01 | 2026-09-30      |
| 9508.T   | Kyushu Electric Power Co. Inc.                               | JPX        | 2001-01-01 | 2026-10-01      |
| ACT.DE   | AlzChem Group AG                                             | XETRA      | 2004-08-12 | 2026-09-18      |
| AETH     | Bitwise Trendwise Ether and Treasuries Rotation Strategy ETF | AMEX       | 2023-10-03 | 2026-10-02      |

---

## get_crypto_list
The crypto list function returns a complete list of all crypto symbols that can be used in the Finance Toolkit. These are over 4.000 symbols.

Returns: pd.DataFrame: A dataframe with all the symbols in the toolkit.


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

Returns: pd.DataFrame: A dataframe with the forex symbols.


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

Returns: pd.DataFrame: A dataframe with all the commodities available.


```python
from financetoolkit import Discovery

discovery = Discovery(api_key="FINANCIAL_MODELING_PREP_KEY")

commodity_list = discovery.get_commodity_list()

commodity_list.head(10)
```

Which returns:

| Symbol   | Name                   |   Exchange | Trade Month   | Currency   |
|:---------|:-----------------------|-----------:|:--------------|:-----------|
| ALIUSD   | Aluminum Futures       |        nan | Dec           | USD        |
| BZUSD    | Brent Crude Oil        |        nan | Dec           | USD        |
| CCUSD    | Cocoa                  |        nan | Dec           | USD        |
| CLUSD    | Crude Oil              |        nan | Nov           | USD        |
| CTUSX    | Cotton                 |        nan | Nov           | USX        |
| DCUSD    | Class III Milk Futures |        nan | Dec           | USD        |
| DXUSD    | US Dollar              |        nan | Sep           | USD        |
| ESUSD    | E-Mini S&P 500         |        nan | Dec           | USD        |
| GCUSD    | Gold Futures           |        nan | Dec           | USD        |
| GFUSX    | Feeder Cattle Futures  |        nan | Nov           | USX        |

---

## get_etf_list
The etf list function returns a complete list of all etf symbols that can be used in the Finance Toolkit.

Returns: pd.DataFrame: A dataframe with all the etf symbols.


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
The index list function returns a complete list of all etf symbols that can be used in the Finance Toolkit.

Returns: pd.DataFrame: A dataframe with all the index symbols.


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

| Published Date      | Symbol   | Publisher           | Title                                                                                                                                                                                   |
|:--------------------|:---------|:--------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 2026-10-08 04:00:00 | RYCEF    | Invezz              | Rolls-Royce share price is facing turbulence: here's why                                                                                                                                |
| 2026-10-08 04:00:00 | PHOS     | Newsfile Corp       | Nevada Organic Phosphate Continues 2026 Drill Program with MM26-11 at Murdock Mountain                                                                                                  |
| 2026-10-08 04:00:00 | BHV      | PRNewsWire          | Biohaven Enters Strategic Licensing Agreement with Ono Pharma for Extracellular IgG Degraders in Japan and Select Asian Regions, Lead Candidate BHV-1300 in Phase 3 for Graves' Disease |
| 2026-10-08 03:55:00 | POAHY    | WSJ                 | Porsche AG Increases Stake in Manthey Racing to 67%                                                                                                                                     |
| 2026-10-08 03:45:11 | FAMDF    | Proactive Investors | Futura Medical revises sale timetable as finance director steps down                                                                                                                    |

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

| Published Date      | Publisher                     | Title                                                                                               |
|:--------------------|:------------------------------|:----------------------------------------------------------------------------------------------------|
| 2026-10-08 03:25:22 | CNBC                          | Indian billionaire's firm backing Trump refinery plan emerges top Venezuelan oil buyer outside U.S. |
| 2026-10-08 02:39:31 | FXEmpire                      | First Light News: Bond Yields Remain Elevated & Equities Slip Lower                                 |
| 2026-10-08 02:22:25 | Bloomberg Markets and Finance | Oil Prices Rise as US Said to Consider Iran Strike Options                                          |
| 2026-10-08 01:30:49 | CNBC                          | America shut out Chinese EVs. Britain welcomed them — and now faces a difficult choice              |
| 2026-10-08 01:09:31 | Reuters                       | India denies bias in satellite internet approvals after Musk's 'oligarchs' jab                      |

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

| Published Date      | Symbol   | Publisher     | Title                                                                                                                                                                                   |
|:--------------------|:---------|:--------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 2026-10-08 04:00:00 | BHV      | PRNewsWire    | Biohaven Enters Strategic Licensing Agreement with Ono Pharma for Extracellular IgG Degraders in Japan and Select Asian Regions, Lead Candidate BHV-1300 in Phase 3 for Graves' Disease |
| 2026-10-08 04:00:00 | PHOS     | Newsfile Corp | Nevada Organic Phosphate Continues 2026 Drill Program with MM26-11 at Murdock Mountain                                                                                                  |
| 2026-10-08 03:30:00 | CCB      | Newsfile Corp | Kaplan Fox Encourages Coastal Financial Corporation (CCB) Investors with Significant Losses to Contact the Firm Before December 1, 2026                                                 |
| 2026-10-08 03:15:00 | FOX      | Newsfile Corp | Kaplan Fox Encourages Alphabet Inc. (GOOGL, GOOG) Investors with Significant Losses to Contact the Firm Before December 1, 2026                                                         |
| 2026-10-08 03:10:00 | CELH     | Newsfile Corp | Kaplan Fox Encourages Celsius Holdings, Inc. (CELH) Investors with Significant Losses to Contact the Firm Before November 3, 2026                                                       |

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

| Published Date      | Symbol   | Publisher   | Title                                                                            |
|:--------------------|:---------|:------------|:---------------------------------------------------------------------------------|
| 2026-10-08 03:34:41 | USDKGUSD | Crypto news | Kyrgyzstan shuts $50M USDKG months after UK sanctions                            |
| 2026-10-08 03:28:00 | KISHUUSD | Tokenpost   | Kishu Inu Founder Charged With Wire Fraud Over Alleged $9 Million Gain           |
| 2026-10-08 03:26:14 | ETHUSD   | Cryptonews  | What is Crypto Bunker Mode? Ethereum's Justin Drake Warns of a Possible AI Break |
| 2026-10-08 03:25:24 | SOLUSD   | UToday      | Samsung Brings Solana to 82 Million Phones                                       |
| 2026-10-08 03:16:50 | XRPUSD   | Crypto news | Ripple challenges Wall Street banks with leveraged ETF financing push            |

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

| Published Date      | Symbol   | Publisher    | Title                                                                                                   |
|:--------------------|:---------|:-------------|:--------------------------------------------------------------------------------------------------------|
| 2026-10-08 03:24:28 | GBPUSD   | FX Street    | British Pound: Downside seen limited near 1.3140 against US Dollar - UOB                                |
| 2026-10-08 03:20:35 | NZDUSD   | FX Street    | NZD/USD Price Forecast: Drifting closer to 18-month lows at 0.5580                                      |
| 2026-10-08 03:13:24 | XAUUSD   | Action Forex | Could Gold's Selloff Run Out of Road Below 4,000?                                                       |
| 2026-10-08 02:58:04 | EURUSD   | FX Street    | EUR/USD to 1.1065? Gold threatens $4,100 as Bitcoin tests support [Video]                               |
| 2026-10-08 02:54:45 | EURUSD   | FX Street    | EUR/USD continental collision: 7th-order institutional demand slab meets -23.0° downward rail at 1.1190 |

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

| Published Date      | Symbol   | Publisher             | Title                                                                                                                    |
|:--------------------|:---------|:----------------------|:-------------------------------------------------------------------------------------------------------------------------|
| 2026-10-07 16:37:01 | AAPL     | Fool - Investing News | Nvidia Earned About Twice as Much as Apple Last Quarter. Its Stock Is Worth Only About 20% More.                         |
| 2026-10-07 16:03:51 | AAPL     | 247 Wallst            | You Have $150,000 in Savings and Have Never Owned a Single Investment. These 3 ETFs Are Enough to Build a Real Portfolio |
| 2026-10-07 14:03:09 | AAPL     | CNBC Television       | Apple looks to smart home devices                                                                                        |
| 2026-10-07 13:56:34 | AAPL     | Bloomberg Technology  | Apple Partners With LG on New Smart Home Devices                                                                         |
| 2026-10-07 12:41:37 | AAPL     | MarketBeat            | Morgan Stanley Is Bullish on Apple—But With a Catch                                                                      |

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
| 2026-10-05 03:05:00 | AAPL     | Newsfile Corp | TempraMed Announces VIVI Cap Smart Connectivity with Apple Health and Google Fit, Providing Better Health Outcomes and Data Tracking                                    |
| 2026-09-28 09:00:00 | AAPL     | Newsfile Corp | QIMC Ties New Salem-Apple River Helium Zones to a Buried Basement Structure: Gravity, Magnetics and Geochemistry Converge on a Single Fault-Bounded Ramp                |
| 2026-09-25 13:21:00 | AAPL     | Business Wire | Hagens Berman: Credit Unions Win Class Certification in Class-Action Lawsuit Against Apple Alleging Illicit Revenue from Apple Pay Fees                                 |

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

| Published Date      | Symbol   | Publisher   | Title                                                                                           |
|:--------------------|:---------|:------------|:------------------------------------------------------------------------------------------------|
| 2026-10-08 02:59:34 | BTCUSD   | Tokenpost   | Bitcoin Total Demand Returns Positive as Spot Demand Recovers                                   |
| 2026-10-08 02:50:50 | BTCUSD   | Tokenpost   | Bitcoin Tests $82,000 Support After $487 Million ETF Outflows                                   |
| 2026-10-08 02:43:16 | BTCUSD   | Tokenpost   | Bitcoin Falls Into $82,500 Area as Brent Crude Reclaims $102                                    |
| 2026-10-08 02:40:12 | BTCUSD   | Cryptonews  | Bitcoin Price Prediction: Hawkish FOMC Minutes, Oil Price, and Rising Yields Send BTC Below 83K |
| 2026-10-08 02:17:06 | BTCUSD   | Tokenpost   | Crypto Market Cap Drops 4.44% to $2.83 Trillion as Bitcoin Slides                               |

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

| Published Date      | Symbol   | Publisher   | Title                                                                                                   |
|:--------------------|:---------|:------------|:--------------------------------------------------------------------------------------------------------|
| 2026-10-08 02:58:04 | EURUSD   | FX Street   | EUR/USD to 1.1065? Gold threatens $4,100 as Bitcoin tests support [Video]                               |
| 2026-10-08 02:54:45 | EURUSD   | FX Street   | EUR/USD continental collision: 7th-order institutional demand slab meets -23.0° downward rail at 1.1190 |
| 2026-10-08 02:21:34 | EURUSD   | FX Street   | Euro: Downside risks persist toward 1.1140 against US Dollar - UOB                                      |
| 2026-10-08 02:02:13 | EURUSD   | FX Street   | EUR/USD Price Forecast: Holds below 1.1200, bearish tone prevails amid oversold conditions              |
| 2026-10-07 21:58:23 | EURUSD   | FX Street   | Euro recovers to near 1.1200 on softer US Dollar, eyes on France debt concerns                          |

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

| Symbol    | Date                | Company                  | Exchange   | Status   |        Shares | Price Range   |    Market Cap |
|:----------|:--------------------|:-------------------------|:-----------|:---------|--------------:|:--------------|--------------:|
| 001359.SZ | 2024-03-27 00:00:00 | Pamica Co Ltd            | SHZ        | Priced   |   3.09241e+07 | 17.39 - 26.08 |   8.065e+08   |
| 001389.SZ | 2024-04-01 00:00:00 | Delton Tech Ltd          | SHZ        | Priced   |   1.42666e+07 | 17.43 - 51.68 |   7.373e+08   |
| 036220.KQ | 2024-03-12 00:00:00 | Osang Healthcare Co.,Ltd | KOE        | Priced   |   1.84138e+07 | 15320 - 20000 |   8.80054e+10 |
| 0917.HK   | 2024-05-23 00:00:00 | Qunabox Group Ltd        | HKSE       | Expected | nan           | nan           |   1.91787e+09 |
| 0EG8.L    | 2024-03-26 00:00:00 | Finnair Oyj              | LSE        | Priced   | nan           | 2.91 - 2.91   | nan           |

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

| Symbol   | Filing Date   | Accepted Date   | Effectiveness Date   |     CIK | Form   |
|:---------|:--------------|:----------------|:---------------------|--------:|:-------|
| AAIT     | 2024-03-14    | 2024-03-14      | 2024-03-14           | 1100663 | CERT   |
| AAIT     | 2024-05-22    | 2024-05-22      | 2024-05-22           | 1100663 | CERT   |
| AAIT     | 2024-01-18    | 2024-01-18      | 2024-01-18           | 1100663 | CERT   |
| AAIT     | 2024-03-21    | 2024-03-20      | 2024-03-21           | 1100663 | CERT   |
| AAIT     | 2024-05-23    | 2024-05-23      | 2024-05-23           | 1100663 | CERT   |

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

| Symbol   | IPO Date   |   Public Price Per Share |   Public Price Total | Form   |
|:---------|:-----------|-------------------------:|---------------------:|:-------|
| ACON     | 2022-04-21 |                     0.58 |           3.0015e+06 | 424B4  |
| ACONW    | 2024-02-25 |                     0.58 |           3.0015e+06 | 424B4  |
| ADEX     | 2021-03-02 |                     1    |           7          | S-1    |
| ADEX     | 2021-03-02 |                     1    |           7          | S-1/A  |
| ADEX-WT  | 2024-01-07 |                     1    |           7          | S-1    |

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
| 0010.KL   | 2024-03-21 00:00:00 |           1 |             4 | stock-split  |
| 001270.SZ | 2024-05-07 00:00:00 |          13 |            10 | stock-split  |
| 001296.SZ | 2024-05-30 00:00:00 |           7 |             5 | stock-split  |
| 001309.SZ | 2024-04-26 00:00:00 |          13 |            10 | stock-split  |
| 001358.SZ | 2024-04-24 00:00:00 |           7 |             5 | stock-split  |

---

## get_sector_performance
Returns sector performance - the average price change per sector. Provide exactly one of `date` (a snapshot across all sectors on that date) or `sector` (the historical time series for one sector).

**Also known as:** sector performance snapshot, sector performance history, sector trend.

**Args:**

- <u>date (str, optional):</u> The date to retrieve a snapshot for, e.g. "2024-02-01".
- <u>sector (str, optional):</u> The sector to retrieve the history for, e.g. "Energy".
- <u>start_date (str, optional):</u> The start of the history of one sector. Defaults to a year
ago.
- <u>end_date (str, optional):</u> The end of the history of one sector. Defaults to today.

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
| 2024-02-26 00:00:00 | Energy   | NASDAQ     |        -0.141335 |
| 2024-02-27 00:00:00 | Energy   | NASDAQ     |         2.5373   |
| 2024-02-28 00:00:00 | Energy   | NASDAQ     |        -3.61631  |
| 2024-02-29 00:00:00 | Energy   | NASDAQ     |         0.625943 |
| 2024-03-01 00:00:00 | Energy   | NASDAQ     |         1.399    |

---

## get_industry_performance
Returns industry performance - the average price change per industry. Provide exactly one of `date` (a snapshot across all industries on that date) or `industry` (the historical time series for one industry).

**Also known as:** industry performance snapshot, industry performance history, industry trend.

**Args:**

- <u>date (str, optional):</u> The date to retrieve a snapshot for, e.g. "2024-02-01".
- <u>industry (str, optional):</u> The industry to retrieve the history for, e.g. "Biotechnology".
- <u>start_date (str, optional):</u> The start of the history of one industry. Defaults to a year
ago.
- <u>end_date (str, optional):</u> The end of the history of one industry. Defaults to today.

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
| 2024-02-26 00:00:00 | Biotechnology | NASDAQ     |         3.05736  |
| 2024-02-27 00:00:00 | Biotechnology | NASDAQ     |         9.45945  |
| 2024-02-28 00:00:00 | Biotechnology | NASDAQ     |        -0.838124 |
| 2024-02-29 00:00:00 | Biotechnology | NASDAQ     |        -1.46899  |
| 2024-03-01 00:00:00 | Biotechnology | NASDAQ     |         2.61434  |

---

## get_sector_pe
Returns sector price-to-earnings (P/E) ratios. Provide exactly one of `date` (a snapshot across all sectors on that date) or `sector` (the historical time series for one sector).

**Also known as:** sector P/E snapshot, sector P/E history, sector valuation trend.

**Args:**

- <u>date (str, optional):</u> The date to retrieve a snapshot for, e.g. "2024-02-01".
- <u>sector (str, optional):</u> The sector to retrieve the history for, e.g. "Energy".
- <u>start_date (str, optional):</u> The start of the history of one sector. Defaults to a year
ago.
- <u>end_date (str, optional):</u> The end of the history of one sector. Defaults to today.

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
| 2024-02-26 00:00:00 | Energy   | NASDAQ     |    5.64705 |
| 2024-02-27 00:00:00 | Energy   | NASDAQ     |    5.73411 |
| 2024-02-28 00:00:00 | Energy   | NASDAQ     |    5.46423 |
| 2024-02-29 00:00:00 | Energy   | NASDAQ     |    5.43205 |
| 2024-03-01 00:00:00 | Energy   | NASDAQ     |    5.41659 |

---

## get_industry_pe
Returns industry price-to-earnings (P/E) ratios. Provide exactly one of `date` (a snapshot across all industries on that date) or `industry` (the historical time series for one industry).

**Also known as:** industry P/E snapshot, industry P/E history, industry valuation trend.

**Args:**

- <u>date (str, optional):</u> The date to retrieve a snapshot for, e.g. "2024-02-01".
- <u>industry (str, optional):</u> The industry to retrieve the history for, e.g. "Biotechnology".
- <u>start_date (str, optional):</u> The start of the history of one industry. Defaults to a year
ago.
- <u>end_date (str, optional):</u> The end of the history of one industry. Defaults to today.

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
| 2024-02-26 00:00:00 | Biotechnology | NASDAQ     |   0.177825 |
| 2024-02-27 00:00:00 | Biotechnology | NASDAQ     |   0.161566 |
| 2024-02-28 00:00:00 | Biotechnology | NASDAQ     |   0.154047 |
| 2024-02-29 00:00:00 | Biotechnology | NASDAQ     |   7.58288  |
| 2024-03-01 00:00:00 | Biotechnology | NASDAQ     |   8.12904  |

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

| Symbol   | Company Name                    | Targeted Company Name          | Transaction Date   |
|:---------|:--------------------------------|:-------------------------------|:-------------------|
| HTB      | HomeTrust Bancshares, Inc.      | Blue Ridge Bankshares, Inc.    | 2026-10-02         |
| HTBI     | HomeTrust Bancshares, Inc.      | Blue Ridge Bankshares, Inc.    | 2026-10-02         |
| IRT      | INDEPENDENCE REALTY TRUST, INC. | Centerspace                    | 2026-09-23         |
| JMSB     | John Marshall Bancorp, Inc.     | Eagle Financial Services, Inc. | 2026-10-02         |
| PATK     | PATRICK INDUSTRIES INC          | LCI Industries                 | 2026-09-23         |

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
| 000270.KS | 2026-10-01 00:00:00 | 5550.38 |        5609.44  |   3.1043e+13  |         3.14307e+13 | 2026-10-08     |
| 032350.KS | 2026-10-01 00:00:00 | 1718    |        1718     |   2.13512e+11 |         2.1315e+11  | 2026-10-08     |
| 0ENN.L    | 2026-10-01 00:00:00 |  nan    |           3.09  | nan           |         1.51e+09    | 2026-10-08     |
| 0JZS.L    | 2026-10-01 00:00:00 |    0.86 |           0.755 |   2.0248e+09  |         1.97614e+09 | 2026-10-08     |
| 0OHK.L    | 2026-10-01 00:00:00 |    9.81 |          11.1   |   7.2503e+09  |         7.10111e+09 | 2026-10-08     |

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
| CLAYU    | 2026-10-02 19:20:24 | False            | https://www.sec.gov/Archives/edgar/data/1855467/000149315226045639/form8-k.htm       |
| MOBXW    | 2026-10-02 19:20:24 | False            | https://www.sec.gov/Archives/edgar/data/1855467/000149315226045639/form8-k.htm       |

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

| Symbol   | Reporting Name          | Transaction Type   |   Securities Transacted |   Price |
|:---------|:------------------------|:-------------------|------------------------:|--------:|
| HNGE     | Perez Daniel Antonio    | C-Conversion       |                    4100 |   0     |
| HNGE     | Perez Daniel Antonio    | S-Sale             |                    4100 | 100.198 |
| HNGE     | Perez Daniel Antonio    | C-Conversion       |                    4100 |   0     |
| GRAB     | Ong Chin Yin            | S-Sale             |                   38000 |   3.09  |
| PALI     | Jones Mitchell Lawrence | M-Exempt           |                 2620850 |   0     |

---

