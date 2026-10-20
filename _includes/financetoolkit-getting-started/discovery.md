## Getting Started

Every analysis starts with a list of tickers, and often you don't have one yet. The Discovery module is where you find it: complete lists of stocks, ETFs, indices, cryptocurrencies, forex pairs and commodities, a search by name, a stock screener, the day's market movers and the performance and valuation of whole sectors. Whatever it returns can go straight into the `Toolkit` for further analysis.

### Loading the Module

Discovery is a class of its own and needs only an API key. To initialize it:

```python
from financetoolkit import Discovery

API_KEY = "FINANCIAL_MODELING_PREP_KEY"

discovery = Discovery(api_key=API_KEY)
```

### Lists of Instruments

Each asset class has its own list function: `get_stock_list`, `get_etf_list`, `get_index_list`, `get_crypto_list`, `get_forex_list` and `get_commodity_list`. The stock list alone holds more than 90,000 symbols from exchanges around the world, each with its name.

To retrieve every available stock:

```python
discovery.get_stock_list()
```

### Searching for Instruments

A list that long is easier to search than to browse. `search_instruments` finds every instrument whose ticker or name matches a query, with the currency and exchange it trades on, which matters for companies listed in several places.

To find every instrument matching "Apple":

```python
discovery.search_instruments("Apple")
```

Which returns Apple's listings on several exchanges first, among others:

| Symbol  | Name       | Currency | Exchange               |
|:--------|:-----------|:---------|:-----------------------|
| AAPL    | Apple Inc. | USD      | NASDAQ Global Select   |
| AAPL.NE | Apple Inc. | CAD      | CBOE CA                |
| APC.DE  | Apple Inc. | EUR      | Deutsche Börse         |
| AAPL.MX | Apple Inc. | MXN      | Mexican Stock Exchange |

The results continue with partial matches such as the Appleseed Fund and Apple Hospitality REIT, so check the name before you use a ticker.

### Screening Stocks

The stock screener narrows the full universe down with lower and upper bounds on market cap, price, beta, volume and dividend, and filters on sector, industry, country and exchange. Each bound is optional, so a screen can be as broad or as narrow as you need.

To find stocks with a market cap up to $200 billion, a price between $100 and $200, a beta between 1 and 1.5, a daily volume between 100,000 and 2 million shares and a dividend between $1 and $2 per share:

```python
screener = discovery.get_stock_screener(
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
    is_etf=False,
)
```

The result holds each company's name, market cap, sector, industry, beta, price, dividend, volume, exchange, country and currency, plus the market cap converted to US dollars so that companies listed in other currencies compare directly. About two dozen stocks pass this screen, mostly mid-sized industrials and consumer companies, ranked by their market cap in US dollars below:

{% include ft-chart.html id="discovery-screener" src="/assets/data/financetoolkit-guides/discovery.json" label="Stocks that pass the screen, ranked by market cap in US dollars" %}

### Gainers, Losers and Most Active Stocks

The day's market movers are a quick way to spot what is drawing attention: the biggest gainers, the biggest losers and the most actively traded stocks, each with the price, the change in dollars and in percent, and the exchange.

To retrieve the first rows of each:

```python
discovery.get_biggest_gainers().head()

discovery.get_biggest_losers().head()

discovery.get_most_active_stocks().head()
```

The gainers and losers lists are dominated by small companies with large percentage moves, so they are a starting point for a closer look rather than a list to act on.

### Sector Performance and Valuation

Before you dive into individual stocks, it helps to know how their sector is doing. Pass a `date` to `get_sector_performance` for a snapshot of every sector on that day, or a `sector` or `industry` name to `get_sector_pe` for that sector's valuation over time. Together they tell you whether a move is sector-wide or specific to one company, and whether a sector trades rich or cheap compared to its own history. `get_industry_performance` and `get_industry_pe` do the same per industry.

To get the performance of every sector on 1 February 2024 and the P/E ratio of the Technology sector:

```python
discovery.get_sector_performance(date="2024-02-01")

discovery.get_sector_pe(sector="Technology")
```

The first gives the average change of the stocks in each sector on that day:

{% include ft-chart.html id="discovery-sector-performance" src="/assets/data/financetoolkit-guides/discovery.json" label="Average change per sector on 1 February 2024" %}

Utilities and consumer stocks rose about 2% that day while financial services fell by about the same amount, a split that a single index return would hide.

The second gives the daily P/E ratio of the Technology sector over the past year:

{% include ft-chart.html id="discovery-sector-pe" src="/assets/data/financetoolkit-guides/discovery.json" label="P/E ratio of the Technology sector over the past year" %}

### From Discovery to the Toolkit

The screener returns the tickers as its index, which is exactly what the `Toolkit` takes. That makes a screen the first step of an analysis: find the candidates, then compare their prices, statements, ratios and risk.

To run the same screen and load the resulting tickers into the Toolkit:

```python
from financetoolkit import Toolkit

tickers = discovery.get_stock_screener(
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
    is_etf=False,
).index.tolist()

companies = Toolkit(tickers=tickers, api_key=API_KEY)

companies.get_historical_data()
```

Without a `start_date` the Toolkit retrieves the last five years. The cumulative return of each screened stock over that period, with the S&P 500 in orange for reference:

{% include ft-chart.html id="discovery-screener-returns" src="/assets/data/financetoolkit-guides/discovery.json" label="Cumulative return of the screened stocks over five years, with the S&P 500" %}

Stocks that look alike on beta, price and dividend still end up far apart: some gained more than 200% while others lost money. From here, every other module, from [ratios](/projects/financetoolkit/docs/ratios#getting-started) to [risk](/projects/financetoolkit/docs/risk#getting-started), works on the same `companies` instance.

### More in the Discovery Module

The module also covers news (stock, crypto and forex news, press releases and search), the IPO calendar with disclosures and prospectuses, the stock split and earnings calendars, delisted companies, recent mergers and acquisitions, 8-K filings and the latest insider trades.

{% include ft-charts-script.html %}
