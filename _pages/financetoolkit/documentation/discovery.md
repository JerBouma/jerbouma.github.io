---
title: Discovery
excerpt: The Discovery Module contains lists of companies, cryptocurrencies, forex, commodities, etfs and indices including screeners, quotes, performance metrics and more to find and select tickers to use in the Finance Toolkit.
description: The Discovery Module contains lists of companies, cryptocurrencies, forex, commodities, etfs and indices including screeners, quotes, performance metrics and more to find and select tickers to use in the Finance Toolkit.
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

| Symbol   | Name                                  | Currency   | Exchange               | Exchange Code   |
|:---------|:--------------------------------------|:-----------|:-----------------------|:----------------|
| META     | Meta Platforms, Inc.                  | USD        | NASDAQ Global Select   | NASDAQ          |
| META.L   | WisdomTree Industrial Metals Enhanced | USD        | London Stock Exchange  | LSE             |
| METAUSD  | Metadium USD                          | USD        | CCC                    | CRYPTO          |
| META.MI  | WisdomTree Industrial Metals Enhanced | EUR        | Milan                  | MIL             |
| META.JK  | PT Nusantara Infrastructure Tbk       | IDR        | Jakarta Stock Exchange | JKT             |


---

## get_stock_screener
Screen stocks based on a set of criteria. This can be useful to find companies that match a specific criteria or your analysis. Further filtering can be done by utilising the Finance Toolkit and calculating the relevant ratios to filter by. This can be:

- Market capitalization (market_cap_higher, market_cap_lower)
- Price (price_higher, price_lower)
- Beta (beta_higher, beta_lower)
- Volume (volume_higher, volume_lower)
- Dividend (dividend_higher, dividend_lower)

Note that the limit is 1000 companies. Thus if you hit the 1000, it is recommended to narrow down your search to prevent companies from being excluded simply because of this limit.

**Also known as:** filter stocks, financial criteria screener.

**Args:**

- <u>market_cap_higher (int):</u> The minimum market capitalization of the stock.
- <u>market_cap_lower (int):</u> The maximum market capitalization of the stock.
- <u>price_higher (int):</u> The minimum price of the stock.
- <u>price_lower (int):</u> The maximum price of the stock.
- <u>beta_higher (int):</u> The minimum beta of the stock.
- <u>beta_lower (int):</u> The maximum beta of the stock.
- <u>volume_higher (int):</u> The minimum volume of the stock.
- <u>volume_lower (int):</u> The maximum volume of the stock.
- <u>dividend_higher (int):</u> The minimum dividend of the stock.
- <u>dividend_lower (int):</u> The maximum dividend of the stock.

**Returns:**

pd.DataFrame: A dataframe with all the symbols that match the query.

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

| Symbol   | Name              |   Market Cap | Sector            | Industry               |   Beta |   Price |   Dividend |   Volume | Exchange                | Exchange Code   | Country   |
|:---------|:------------------|-------------:|:------------------|:-----------------------|-------:|--------:|-----------:|---------:|:------------------------|:----------------|:----------|
| NKE      | NIKE, Inc.        | 163403295604 | Consumer Cyclical | Footwear & Accessories |  1.079 | 107.36  |       1.48 |  1045865 | New York Stock Exchange | NYSE            | US        |
| SAF.PA   | Safran SA         |  66234006559 | Industrials       | Aerospace & Defense    |  1.339 | 160.16  |       1.35 |   119394 | Paris                   | EURONEXT        | FR        |
| ROST     | Ross Stores, Inc. |  46724188589 | Consumer Cyclical | Apparel Retail         |  1.026 | 138.785 |       1.34 |   169879 | NASDAQ Global Select    | NASDAQ          | US        |
| HES      | Hess Corporation  |  44694706090 | Energy            | Oil & Gas E&P          |  1.464 | 145.51  |       1.75 |   123147 | New York Stock Exchange | NYSE            | US        |


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

| Symbol      | Name                         |   Price | Exchange                        | Exchange Code   |
|:------------|:-----------------------------|--------:|:--------------------------------|:----------------|
| LEO.V       | Lion Copper and Gold Corp.   |   0.09  | Toronto Stock Exchange Ventures | TSX             |
| LEOF.TA     | Lewinsky-Ofer Ltd.           | 263.1   | Tel Aviv                        | TLV             |
| LEON        | Leone Asset Management, Inc. |   0.066 | Other OTC                       | OTC             |
| LEON.SW     | Leonteq AG                   |  34.35  | Swiss Exchange                  | SIX             |
| LER.AX      | Leaf Resources Limited       |   0.014 | Australian Securities Exchange  | ASX             |
| LERTHAI.BO  | LERTHAI FINANCE LIMITED      | 265     | Bombay Stock Exchange           | BSE             |
| LES.WA      | Less S.A.                    |   0.22  | Warsaw Stock Exchange           | WSE             |
| LESAF       | Le Saunda Holdings Limited   |   0.071 | Other OTC                       | PNK             |
| LESHAIND.BO | Lesha Industries Limited     |   4.68  | Bombay Stock Exchange           | BSE             |
| LESL        | Leslie's, Inc.               |   6.91  | NASDAQ Global Select            | NASDAQ          |


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

| Symbol   | Date                |   Free Float |   Float Shares |   Outstanding Shares |
|:---------|:--------------------|-------------:|---------------:|---------------------:|
| OPY.AX   | NaT                 |     51.4746  |      119853548 |          2.3284e+08  |
| OPYGY    | NaT                 |      4.49504 |       60892047 |          1.35465e+09 |
| OQAL     | 2024-01-01 13:12:23 |      0       |              0 |     226543           |
| OQLGF    | 2023-12-31 21:48:07 |      0.6765  |        1150607 |          1.70082e+08 |
| OR       | 2024-01-02 05:18:03 |     99.3281  |      183921869 |          1.85166e+08 |
| OR-R.BK  | 2024-01-01 05:29:30 |     23.153   |     2778360000 |          1.2e+10     |
| OR.BK    | 2024-01-02 03:52:39 |     22.7847  |     2734164000 |          1.2e+10     |
| OR.PA    | 2024-01-02 07:57:35 |     45.2727  |      242084445 |          5.34725e+08 |
| OR.SW    | 2023-12-31 13:38:10 |     45.2727  |      355743960 |          7.8578e+08  |
| OR.TO    | 2023-12-31 17:56:33 |     99.3317  |      183928535 |          1.85166e+08 |


---

## get_sectors_performance
Returns the sectors performance for each sector. This features the sector performance over the last months.

Returns: pd.DataFrame: A dataframe with the sectors performance for each sector.


```python
from financetoolkit import Discovery

discovery = Discovery(api_key="FINANCIAL_MODELING_PREP_KEY")

sectors_performance = discovery.get_sectors_performance()

sectors_performance.tail()
```

Which returns:

| Date       |   Utilities |   Basic Materials |   Communication Services |   Consumer Cyclical |   Consumer Defensive |   Energy |   Financial Services |   Healthcare |   Industrials |   Real Estate |   Technology |
|:-----------|------------:|------------------:|-------------------------:|--------------------:|---------------------:|---------:|---------------------:|-------------:|--------------:|--------------:|-------------:|
| 2023-12-27 |     0.13511 |           0.40986 |                 -0.23963 |             0.10358 |              0.48048 | -0.27499 |              0.30153 |      0.75715 |       0.30234 |       0.35946 |      0.02372 |
| 2023-12-28 |     0.80513 |          -0.45131 |                 -0.15858 |            -0.45874 |              0.03828 | -0.81641 |              0.02954 |     -0.01345 |       0.22808 |       0.59612 |     -0.15283 |
| 2023-12-29 |    -0.01347 |          -0.14525 |                 -0.15072 |            -0.58879 |              0.18141 | -0.42463 |             -0.34718 |     -0.082   |      -0.2181  |      -0.52222 |     -0.57062 |
| 2024-01-01 |    -0.01347 |          -0.14536 |                 -0.15074 |            -0.58877 |              0.18141 | -0.41917 |             -0.34753 |     -0.08193 |      -0.21821 |      -0.52216 |     -0.5708  |
| 2024-01-02 |    -0.01347 |          -0.14536 |                 -0.15074 |            -0.58877 |              0.18141 | -0.41917 |             -0.34779 |     -0.08193 |      -0.21823 |      -0.52281 |     -0.57073 |


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

| Symbol   | Name                                                   |   Change |   Price |   Change % |
|:---------|:-------------------------------------------------------|---------:|--------:|-----------:|
| AAME     | Atlantic American Corporation                          |   0.3001 |  2.4501 |    13.9581 |
| ADAP     | Adaptimmune Therapeutics plc                           |   0.1029 |  0.793  |    14.9109 |
| ADTX     | Aditxt, Inc.                                           |   1.81   |  6.63   |    37.5519 |
| AFMD     | Affimed N.V.                                           |   0.0861 |  0.625  |    15.977  |
| AIH      | Aesthetic Medical International Holdings Group Limited |   0.1016 |  0.6896 |    17.2789 |
| ANTE     | AirNet Technology Inc.                                 |   0.1229 |  0.8299 |    17.3833 |
| APRE     | Aprea Therapeutics, Inc.                               |   1.04   |  4.7    |    28.4153 |
| ASTR     | Astra Space, Inc.                                      |   0.55   |  2.28   |    31.7919 |
| BHG      | Bright Health Group, Inc.                              |   2.37   |  7.63   |    45.057  |
| BROG     | Brooge Energy Limited                                  |   0.73   |  3.68   |    24.7458 |


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

| Symbol   | Name                                       |   Change |   Price |   Change % |
|:---------|:-------------------------------------------|---------:|--------:|-----------:|
| AGAE     | Allied Gaming & Entertainment Inc.         |  -0.2    |  1.06   |   -15.873  |
| AVTX     | Avalo Therapeutics, Inc.                   |  -2.7339 |  9.1    |   -23.1023 |
| BAYAR    | Bayview Acquisition Corp Right             |  -0.03   |  0.12   |   -20      |
| BBLG     | Bone Biologics Corporation                 |  -1.48   |  4.52   |   -24.6667 |
| BKYI     | BIO-key International, Inc.                |  -0.6    |  3      |   -16.6667 |
| BREA     | Brera Holdings PLC Class B Ordinary Shares |  -0.2064 |  0.6112 |   -25.2446 |
| BTBT     | Bit Digital, Inc.                          |  -0.86   |  4.23   |   -16.8959 |
| BTCS     | BTCS Inc.                                  |  -0.69   |  1.63   |   -29.7414 |
| BTDR     | Bitdeer Technologies Group                 |  -3.36   |  9.86   |   -25.416  |
| BYN      | Banyan Acquisition Corporation             |  -2.035  | 10.9    |   -15.7325 |


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

| Symbol   | Name                           |   Change |   Price |   Change % |
|:---------|:-------------------------------|---------:|--------:|-----------:|
| AAPL     | Apple Inc.                     |    -1.05 |  192.53 |    -0.5424 |
| ADTX     | Aditxt, Inc.                   |     1.81 |    6.63 |    37.5519 |
| AMD      | Advanced Micro Devices, Inc.   |    -1.35 |  147.41 |    -0.9075 |
| AMZN     | Amazon.com, Inc.               |    -1.44 |  151.94 |    -0.9388 |
| BAC      | Bank of America Corporation    |    -0.21 |   33.67 |    -0.6198 |
| BITF     | Bitfarms Ltd.                  |    -0.41 |    2.91 |   -12.3494 |
| BITO     | ProShares Bitcoin Strategy ETF |    -0.33 |   20.49 |    -1.585  |
| CAN      | Canaan Inc.                    |    -0.5  |    2.31 |   -17.7936 |
| CLSK     | CleanSpark, Inc.               |    -2.08 |   11.03 |   -15.8657 |
| DISH     | DISH Network Corporation       |     0.11 |    5.77 |     1.9435 |


---

## get_delisted_stocks
The delisted stocks function returns a complete list of all delisted stocks including the IPO and delisted date.

Returns: pd.DataFrame: A dataframe with all the delisted stocks.


```python
from financetoolkit import Discovery

discovery = Discovery(api_key="FINANCIAL_MODELING_PREP_KEY")

delisted_stocks = discovery.get_delisted_stocks()

delisted_stocks.head(10)
```

Which returns:

| Symbol   | Name                                         | Exchange   | IPO Date   | Delisted Date   |
|:---------|:---------------------------------------------|:-----------|:-----------|:----------------|
| AAIC     | Arlington Asset Investment Corp.             | NYSE       | 1997-12-23 | 2023-12-14      |
| ABCM     | Abcam plc                                    | NASDAQ     | 2010-12-03 | 2023-12-12      |
| ADZ      | DB Agriculture Short ETN                     | AMEX       | 2008-04-16 | 2023-10-27      |
| AENZ     | Aenza S.A.A.                                 | NYSE       | 2013-07-24 | 2023-12-08      |
| AKUMQ    | Akumin Inc                                   | NASDAQ     | 2018-03-08 | 2023-10-25      |
| ALTMW    | Kinetik Holdings Inc - Warrants (09/11/2023) | NASDAQ     | 2017-05-01 | 2023-11-07      |
| ARCE     | Arco Platform Limited                        | NASDAQ     | 2018-09-26 | 2023-12-07      |
| ARTEW    | Artemis Strategic Investment Corporation     | NASDAQ     | 2021-11-22 | 2023-11-03      |
| ASPAU    | Abri SPAC I, Inc.                            | NASDAQ     | 2021-08-10 | 2023-11-02      |
| AVID     | Avid Technology, Inc.                        | NASDAQ     | 1993-03-12 | 2023-11-07      |


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

| Symbol       | Name                                 | Currency   | Exchange   |
|:-------------|:-------------------------------------|:-----------|:-----------|
| .ALPHAUSD    | .Alpha USD                           | USD        | CCC        |
| 00USD        | 00 Token USD                         | USD        | CCC        |
| 0NEUSD       | Stone USD                            | USD        | CCC        |
| 0X0USD       | 0x0.ai USD                           | USD        | CCC        |
| 0X1USD       | 0x1.tools: AI Multi-tool Plaform USD | USD        | CCC        |
| 0XAUSD       | 0xApe USD                            | USD        | CCC        |
| 0XBTCUSD     | 0xBitcoin USD                        | USD        | CCC        |
| 0XENCRYPTUSD | Encryption AI USD                    | USD        | CCC        |
| 0XGASUSD     | 0xGasless USD                        | USD        | CCC        |
| 0XMRUSD      | 0xMonero USD                         | USD        | CCC        |


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

| Symbol   | Name    | Currency   | Exchange   |
|:---------|:--------|:-----------|:-----------|
| AEDAUD   | AED/AUD | AUD        | CCY        |
| AEDBHD   | AED/BHD | BHD        | CCY        |
| AEDCAD   | AED/CAD | CAD        | CCY        |
| AEDCHF   | AED/CHF | CHF        | CCY        |
| AEDDKK   | AED/DKK | DKK        | CCY        |
| AEDEUR   | AED/EUR | EUR        | CCY        |
| AEDGBP   | AED/GBP | GBP        | CCY        |
| AEDILS   | AED/ILS | ILS        | CCY        |
| AEDINR   | AED/INR | INR        | CCY        |
| AEDJOD   | AED/JOD | JOD        | CCY        |


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

| Symbol   | Name                   | Currency   | Exchange   |
|:---------|:-----------------------|:-----------|:-----------|
| ALIUSD   | Aluminum Futures       | USD        | COMEX      |
| BZUSD    | Brent Crude Oil        | USD        | ICE        |
| CCUSD    | Cocoa                  | USD        | ICE        |
| CLUSD    | Crude Oil              | USD        | CME        |
| CTUSX    | Cotton                 | USX        | ICE        |
| DCUSD    | Class III Milk Futures | USD        | CME        |
| DXUSD    | US Dollar              | USD        | ICE        |
| ESUSD    | E-Mini S&P 500         | USD        | CME        |
| GCUSD    | Gold Futures           | USD        | CME        |
| GFUSX    | Feeder Cattle Futures  | USX        | CME        |


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

| Symbol    | Name                                                                                            |      Price | Exchange              | Exchange Code   |
|:----------|:------------------------------------------------------------------------------------------------|-----------:|:----------------------|:----------------|
| 01002T.TW | Cathay No.1 REIT                                                                                |    17.29   | Taiwan                | TAI             |
| 020Y.L    | iShares IV Public Limited Company - iShares Euro Government Bond 20yr Target Duration UCITS ETF |     3.9522 | London Stock Exchange | LSE             |
| 069500.KS | KODEX 200                                                                                       | 36390      | KSE                   | KSC             |
| 069660.KS | KOSEF 200                                                                                       | 36370      | KSE                   | KSC             |
| 091160.KS | Kodex Semicon                                                                                   | 36840      | KSE                   | KSC             |
| 091170.KS | Kodex Banks                                                                                     |  6695      | KSE                   | KSC             |
| 091180.KS | Kodex Autos                                                                                     | 19450      | KSE                   | KSC             |
| 091220.KS | Mirae Asset TIGER Banks ETF                                                                     |  6845      | KSE                   | KSC             |
| 091230.KS | Mirae Asset TIGER Semicon ETF                                                                   | 38400      | KSE                   | KSC             |
| 098560.KS | Mirae Asset TIGER Media & Telecom ETF                                                           |  7335      | KSE                   | KSC             |


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

| Symbol      | Name                          | Currency   | Exchange               |
|:------------|:------------------------------|:-----------|:-----------------------|
| 000001.SS   | SSE Composite Index           | CNY        | Shanghai               |
| 399967.SZ   | CSI NATIONAL DEFENSE          | CNY        | Shenzhen               |
| 512.HK      | CES CHINA HK MAINLAND INDEX   | HKD        | HKSE                   |
| DX-Y.NYB    | US Dollar/USDX - Index - Cash | USD        | ICE Futures            |
| FTSEMIB.MI  | FTSE MIB Index                | EUR        | Milan                  |
| IAR.BA      | MERVAL ARGENTINA              | USD        | Buenos Aires           |
| IDX30.JK    | IDX30                         | IDR        | Jakarta Stock Exchange |
| IMOEX.ME    | MOEX Russia Index             | RUB        | MCX                    |
| ITLMS.MI    | FTSE Italia All-Share Index   | EUR        | Milan                  |
| KOSPI200.KS | KOSPI 200 Index               | KRW        | KSE                    |


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

| Published Date       | Symbol   | Publisher                  | Title                                                                         |
|:---------------------|:---------|:---------------------------|:-------------------------------------------------------------------------------|
| 2026-07-07 11:02:16  | VOD      | Proactive Investors        | Starlink threat to BT, Vodafone and other telecoms is 'limited', says analyst  |
| 2026-07-07 11:01:15  | TNDM     | Zacks Investment Research  | Does TNDM Stock Still Deserve a Place in Your Portfolio?                       |
| 2026-07-07 11:01:13  | OMCL     | Zacks Investment Research  | What's Fueling Omnicell Stock's 52.6% Rally Over the Past Year?                |
| 2026-07-07 11:01:10  | AMAT     | Zacks Investment Research  | Best Momentum Stock to Buy for July 7th                                       |
| 2026-07-07 11:01:09  | GS       | Zacks Investment Research  | Goldman Sachs (GS) Earnings Expected to Grow: What to Know Ahead of Next Week's Release |


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

| Published Date       | Publisher                  | Title                                                                      |
|:---------------------|:----------------------------|:---------------------------------------------------------------------------|
| 2026-07-07 10:56:10  | Zacks Investment Research   | ASE Technology Surges 169% YTD: Should You Still Buy the Stock?             |
| 2026-07-07 10:53:31  | NYTimes                     | Companies Brace for Fresh Political Uncertainty at U.S. Agencies           |
| 2026-07-07 10:41:20  | Zacks Investment Research   | Why LATAM (LTM) is a Top Value Stock for the Long-Term                     |
| 2026-07-07 10:35:53  | Reuters                     | AI startup CEO pleaded guilty in US to trading on insider tips from lawyers |
| 2026-07-07 10:30:10  | Fox Business                | TENSIONS RISING: Trump delivers unmistakable warning                       |


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

| Published Date       | Symbol   | Publisher     | Title                                                                              |
|:---------------------|:---------|:--------------|:-------------------------------------------------------------------------------------|
| 2026-07-07 11:01:00  | VERI     | GlobeNewsWire | Portnoy Law Firm Announces Class Action on Behalf of Veritone, Inc. Investors        |
| 2026-07-07 11:00:00  | VSH      | GlobeNewsWire | Vishay Intertechnology Standard-Level 40 V MOSFETs Prevent False Triggering...       |
| 2026-07-07 11:00:00  | TBBK     | GlobeNewsWire | Old National Bancorp Announces Schedule for Second-Quarter Earnings Release...       |
| 2026-07-07 10:59:00  | SRAD     | GlobeNewsWire | Portnoy Law Firm Announces Class Action on Behalf of Sportradar Group AG Investors   |
| 2026-07-07 10:58:00  | CVLT     | GlobeNewsWire | Portnoy Law Firm Announces Class Action on Behalf of Commvault Systems, Inc. Investors |


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

| Published Date       | Symbol   | Publisher      | Title                                                                    |
|:---------------------|:---------|:---------------|:------------------------------------------------------------------------|
| 2026-07-07 10:54:44  | STAKEUSD | Crypto Briefing | Former Tether investment chief seeks to sell 1% stake in the stablecoin giant |
| 2026-07-07 10:53:57  | BTCUSD   | AMBCrypto       | Tether backs Brazil's Mercado Bitcoin while USDT faces growing restrictions in Europe |
| 2026-07-07 10:50:00  | BTCUSD   | UToday          | Satoshi's Bitcoin Saved? Digital Chamber Steps In to Protest $240 Billion Court Seizure |
| 2026-07-07 10:38:15  | BTCUSD   | Crypto Economy  | Binance Rolls Out New Bitcoin Yield Product to Help Holders Boost Returns Without Selling |
| 2026-07-07 10:37:19  | BTCUSD   | Crypto Briefing | $470B of Bitcoin at risk from advancing quantum computing               |


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

| Published Date       | Symbol   | Publisher    | Title                                                                        |
|:---------------------|:---------|:-------------|:-------------------------------------------------------------------------------|
| 2026-07-07 10:16:59  | AUDUSD   | Action Forex | AUDUSD – Recovery Faces Increased Headwinds from Initial Fibo Resistance       |
| 2026-07-07 10:11:55  | EURGBP   | FX Street    | EUR/GBP Price Forecast: Bearish bias persists below 0.8600                      |
| 2026-07-07 09:59:12  | GBPUSD   | FX Street    | British Pound: Capped by layered resistance against US Dollar – Scotiabank      |
| 2026-07-07 09:29:14  | XAUUSD   | FXEmpire     | Gold Price Analysis – Gold Clings to $4,000 Floor Facing Heavy MA Resistance    |
| 2026-07-07 09:21:33  | XAGUSD   | FXEmpire     | Silver Price Analysis – Silver Holds Above $60 as Strong Dollar Restricts Gains |


---

## search_stock_news
Searches stock market news articles by one or more ticker symbols.

**Also known as:** ticker news search, company news lookup.

**Args:**

- <u>symbols (str \| list[str]):</u> One or more ticker symbols, e.g. "AAPL" or
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

| Published Date       | Symbol   | Publisher       | Title                                                                       |
|:---------------------|:---------|:----------------|:-------------------------------------------------------------------------------|
| 2026-07-07 10:46:52  | AAPL     | Benzinga        | Walmart, Apple And Nike May Be Agentic AI's First Winners. Grocery May Be The First Loser |
| 2026-07-07 10:20:11  | AAPL     | Forbes          | Why Investors Fell Back In Love With Apple's Cheap AI Strategy               |
| 2026-07-07 09:26:50  | AAPL     | Benzinga        | Forget the iPhone. Apple's AI Story May Belong to Macs                       |
| 2026-07-07 08:55:03  | AAPL     | 247 Wallst      | Stock Market Live July 7, 2026: S&P 500 (SPY) Drops on Tech Concerns          |
| 2026-07-07 08:44:43  | AAPL     | The Motley Fool | How Apple Can Actually Benefit From the Memory Supply Shortage               |


---

## search_press_releases
Searches company press releases by one or more ticker symbols.

**Also known as:** press release search, corporate announcement lookup.

**Args:**

- <u>symbols (str \| list[str]):</u> One or more ticker symbols, e.g. "AAPL" or
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

| Published Date       | Symbol   | Publisher     | Title                                                                          |
|:---------------------|:---------|:--------------|:-----------------------------------------------------------------------------------|
| 2026-06-19 17:00:00  | AAPL     | PRNewsWire    | Xiao-I Corporation Provides Update on First-Instance Rulings in Patent Litigation...|
| 2026-06-17 09:00:00  | AAPL     | Business Wire | Addigy Expands Identity for Apple Fleets: IdP-Native Login, FileVault...            |
| 2026-06-16 13:23:00  | AAPL     | GlobeNewsWire | Pennsylvania Expansion Continues: Apple Blossom Joins Legend Senior Living          |
| 2026-06-09 14:28:00  | AAPL     | GlobeNewsWire | Charlotte Volsch, Apple Valley, California Broker, Named Among Real Trends 2026...  |
| 2026-06-09 09:58:00  | AAPL     | Business Wire | MIKROE develops Spatial Anchor R1 & S1 for Apple Vision Pro                         |


---

## search_crypto_news
Searches cryptocurrency news articles by one or more coin/token symbols.

**Also known as:** crypto news search, coin news lookup.

**Args:**

- <u>symbols (str \| list[str]):</u> One or more crypto symbols, e.g. "BTCUSD" or
["BTCUSD", "ETHUSD"].
- <u>pages (int, optional):</u> The number of pages to collect, each page is a
separate API call, e.g. pages=5 makes 5 calls. Defaults to 1.
- <u>limit (int, optional):</u> The number of articles to return per page. Defaults to 100.

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

| Published Date       | Symbol   | Publisher      | Title                                                                        |
|:---------------------|:---------|:---------------|:---------------------------------------------------------------------------------|
| 2026-07-07 10:53:57  | BTCUSD   | AMBCrypto       | Tether backs Brazil's Mercado Bitcoin while USDT faces growing restrictions in Europe |
| 2026-07-07 10:50:00  | BTCUSD   | UToday          | Satoshi's Bitcoin Saved? Digital Chamber Steps In to Protest $240 Billion Court Seizure |
| 2026-07-07 10:38:15  | BTCUSD   | Crypto Economy  | Binance Rolls Out New Bitcoin Yield Product to Help Holders Boost Returns Without Selling |
| 2026-07-07 10:37:19  | BTCUSD   | Crypto Briefing | $470B of Bitcoin at risk from advancing quantum computing                    |
| 2026-07-07 10:27:30  | BTCUSD   | CryptoSlate     | Bitcoin dominance hits one-month low as altcoin winners start breaking away  |


---

## search_forex_news
Searches forex news articles by one or more currency pair symbols.

**Also known as:** forex news search, currency pair news lookup.

**Args:**

- <u>symbols (str \| list[str]):</u> One or more forex pairs, e.g. "EURUSD" or
["EURUSD", "GBPUSD"].
- <u>pages (int, optional):</u> The number of pages to collect, each page is a
separate API call, e.g. pages=5 makes 5 calls. Defaults to 1.
- <u>limit (int, optional):</u> The number of articles to return per page. Defaults to 100.

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

| Published Date       | Symbol   | Publisher    | Title                                                                    |
|:---------------------|:---------|:-------------|:-------------------------------------------------------------------------|
| 2026-07-07 07:16:08  | EURUSD   | FX Street    | Euro: Upside bias held above strong support against US Dollar – UOB     |
| 2026-07-07 06:56:14  | EURUSD   | Action Forex | EUR/USD Analysis: Who Is in Control?                                    |
| 2026-07-07 06:53:07  | EURUSD   | Forexcom     | EUR/USD forecast: Dollar holds the upper hand as traders await Fed minutes |
| 2026-07-07 02:15:13  | EURUSD   | FX Street    | Euro Summer range holds against US Dollar – Commerzbank                  |
| 2026-07-07 01:58:21  | EURUSD   | FX Street    | EUR/USD Price Forecast: Turns broadly sideways below 20-day EMA          |


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

| Symbol   | Date       | Company                                     | Exchange   | Status   |     Shares | Price Range   |   Market Cap |
|:---------|:-----------|:---------------------------------------------|:-----------|:---------|-----------:|:--------------|-------------:|
| SMTK     | 2024-05-31 | SmartKem, Inc.                                | NASDAQ     | Expected |        nan |               |          nan |
| NEWTG    | 2024-05-31 | NewtekOne, Inc. 8.50% Fixed Rate Senior Notes  | NASDAQ     | Expected |        nan |               |          nan |
| KDLY     | 2024-05-31 | Kindly MD, Inc.                                | NASDAQ     | Priced   |    1240910 |               |      6825005 |
| KDLYW    | 2024-05-31 | Kindly MD, Inc. Warrants                       | NASDAQ     | Expected |        nan |               |          nan |
| SECR     | 2024-05-31 | IndexIQ Active ETF Trust                       | NYSE       | Expected |        nan |               |          nan |


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

| Symbol   | Filing Date   | Accepted Date   | Effectiveness Date   | CIK        | Form   |
|:---------|:--------------|:-----------------|:----------------------|:-----------|:-------|
| BIPH     | 2024-05-31    | 2024-05-31       | 2024-05-31             | 0001406234 | CERT   |
| BIPJ     | 2024-05-31    | 2024-05-31       | 2024-05-31             | 0001406234 | CERT   |
| BRIPF    | 2024-05-31    | 2024-05-31       | 2024-05-31             | 0001406234 | CERT   |
| NAKAW    | 2024-05-31    | 2024-05-31       | 2024-05-31             | 0001946573 | CERT   |
| BIPI     | 2024-05-31    | 2024-05-31       | 2024-05-31             | 0001406234 | CERT   |


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
|:---------|:-----------|--------------------------:|----------------------:|:-------|
| LUCYW    | 2022-08-14 |                     73    |                4024429 | S-1    |
| LBGJ     | 2024-05-29 |                      5    |               25000000 | F-1/A  |
| CDIX     | 2005-12-21 |                      5    |                8000000 | S-1/A  |
| LUCY     | 2022-08-13 |                     73    |                4024429 | S-1    |
| ERES     | 2023-07-02 |                      0.02 |                    100 | S-1/A  |


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

| Symbol       | Date       |   Numerator |   Denominator | Split Type   |
|:-------------|:-----------|------------:|---------------:|:-------------|
| ALZ.ST       | 2024-05-31 |         617 |            500 | stock-split  |
| RCSL4.SA     | 2024-05-31 |           1 |              4 | stock-split  |
| BFG.NZ       | 2024-05-31 |           3 |             10 | stock-split  |
| CRTX.L       | 2024-05-31 |           1 |            160 | stock-split  |
| DAVANGERE.NS | 2024-05-31 |          10 |              1 | stock-split  |


---

## get_sector_performance
Returns sector performance - the average price change per sector. Provide exactly one of `date` (a snapshot across all sectors on that date) or `sector` (the historical time series for one sector).

**Also known as:** sector performance snapshot, sector performance history, sector trend.

**Args:**

- <u>date (str, optional):</u> The date to retrieve a snapshot for, e.g. "2024-02-01".
- <u>sector (str, optional):</u> The sector to retrieve the history for, e.g. "Energy".

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

| Sector                 | Date       | Exchange   |   Average Change |
|:------------------------|:-----------|:-----------|------------------:|
| Basic Materials         | 2024-02-01 | NASDAQ     |          -0.31481 |
| Communication Services  | 2024-02-01 | NASDAQ     |           0.85070 |
| Consumer Cyclical       | 2024-02-01 | NASDAQ     |           1.81130 |
| Consumer Defensive      | 2024-02-01 | NASDAQ     |           1.74347 |
| Energy                  | 2024-02-01 | NASDAQ     |           0.63975 |


---

## get_industry_performance
Returns industry performance - the average price change per industry. Provide exactly one of `date` (a snapshot across all industries on that date) or `industry` (the historical time series for one industry).

**Also known as:** industry performance snapshot, industry performance history, industry trend.

**Args:**

- <u>date (str, optional):</u> The date to retrieve a snapshot for, e.g. "2024-02-01".
- <u>industry (str, optional):</u> The industry to retrieve the history for, e.g. "Biotechnology".

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

| Industry                    | Date       | Exchange   |   Average Change |
|:-----------------------------|:-----------|:-----------|------------------:|
| Advertising Agencies         | 2024-02-01 | NASDAQ     |            3.8660 |
| Aerospace & Defense          | 2024-02-01 | NASDAQ     |            0.5853 |
| Agricultural Farm Products   | 2024-02-01 | NASDAQ     |            1.6564 |
| Agricultural Inputs          | 2024-02-01 | NASDAQ     |            0.5436 |
| Agricultural - Machinery     | 2024-02-01 | NASDAQ     |            1.4934 |


---

## get_sector_pe
Returns sector price-to-earnings (P/E) ratios. Provide exactly one of `date` (a snapshot across all sectors on that date) or `sector` (the historical time series for one sector).

**Also known as:** sector P/E snapshot, sector P/E history, sector valuation trend.

**Args:**

- <u>date (str, optional):</u> The date to retrieve a snapshot for, e.g. "2024-02-01".
- <u>sector (str, optional):</u> The sector to retrieve the history for, e.g. "Energy".

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

| Sector                 | Date       | Exchange   |   PE Ratio |
|:------------------------|:-----------|:-----------|------------:|
| Basic Materials         | 2024-02-01 | NASDAQ     |     15.6877 |
| Communication Services  | 2024-02-01 | NASDAQ     |     25.9425 |
| Consumer Cyclical       | 2024-02-01 | NASDAQ     |     55.2588 |
| Consumer Defensive      | 2024-02-01 | NASDAQ     |     31.7298 |
| Energy                  | 2024-02-01 | NASDAQ     |     14.4114 |


---

## get_industry_pe
Returns industry price-to-earnings (P/E) ratios. Provide exactly one of `date` (a snapshot across all industries on that date) or `industry` (the historical time series for one industry).

**Also known as:** industry P/E snapshot, industry P/E history, industry valuation trend.

**Args:**

- <u>date (str, optional):</u> The date to retrieve a snapshot for, e.g. "2024-02-01".
- <u>industry (str, optional):</u> The industry to retrieve the history for, e.g. "Biotechnology".

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

| Industry                    | Date       | Exchange   |   PE Ratio |
|:-----------------------------|:-----------|:-----------|------------:|
| Advertising Agencies         | 2024-02-01 | NASDAQ     |     71.0960 |
| Aerospace & Defense          | 2024-02-01 | NASDAQ     |     46.0186 |
| Agricultural Farm Products   | 2024-02-01 | NASDAQ     |      7.4529 |
| Agricultural Inputs          | 2024-02-01 | NASDAQ     |     58.9849 |
| Agricultural - Machinery     | 2024-02-01 | NASDAQ     |     10.3538 |


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

| Symbol   | Company Name                 | Targeted Company Name                 | Transaction Date   |
|:---------|:------------------------------|:-----------------------------------------|:---------------------|
| THRM     | GENTHERM Inc                  | Modine Manufacturing Company              | 2026-07-02            |
| DBCAU    | D. Boral Acquisition I Corp.   | D. Boral ARC Acquisition I Corp. Cl A     | 2026-07-01            |
| DBCA     | D. Boral Acquisition I Corp.   | D. Boral ARC Acquisition I Corp. Cl A     | 2026-07-01            |
| CYCCP    | Cyclacel Pharmaceuticals, Inc. | Bio Green Med Solution, Inc.              | 2026-06-16            |
| CYCC     | Cyclacel Pharmaceuticals, Inc. | Bio Green Med Solution, Inc.              | 2026-06-16            |


---

