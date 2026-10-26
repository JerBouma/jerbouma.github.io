## Getting Started

Two funds that both say "US large caps" can hold very different portfolios. One follows the market weights and leans on a handful of technology giants, another weighs every company the same, a third screens for dividends. The ETF module looks inside a fund: what it costs and trades at, what it holds, how concentrated that is, how much two funds share, what the holdings are valued at, how closely an index fund follows its index and how easily the fund trades.

Every function works the same for bond, commodity and international funds. This section compares four funds that all invest in large US companies: the Vanguard S&P 500 ETF (VOO), the Invesco S&P 500 Equal Weight ETF (RSP), the Invesco QQQ Trust, which follows the Nasdaq-100 (QQQ), and the Schwab U.S. Dividend Equity ETF (SCHD).

### Loading the Data

The ETF module is part of the `Toolkit` class and works on the funds among its tickers. Funds publish only their current holdings, so the `Toolkit` runs up to today. To load the four funds:

```python
from financetoolkit import Toolkit

funds = Toolkit(["VOO", "RSP", "QQQ", "SCHD"], api_key="FINANCIAL_MODELING_PREP_KEY")
```

Tickers that are not a fund return no data in this module, while every other module of the `Toolkit` works on them as usual.

### The Profile and the Premium to NAV

The profile gives the basics of every fund: issuer, asset class, inception date, expense ratio, assets under management, the net asset value (NAV) and the latest price. The premium or discount compares the closing price on the NAV's date with the NAV, the way funds report it. For a fund of liquid US stocks it stays within a few hundredths of a percent; for funds of less liquid assets, such as bonds, it can widen in stress. To get the profiles and keep the main rows:

```python
profile = funds.etf.get_profile()

profile.loc[["Expense Ratio", "Assets Under Management", "NAV", "Price", "Premium/Discount", "Holdings Count"]]
```

Which returns:

|                         | VOO           | RSP         | QQQ          | SCHD         |
|:------------------------|:--------------|:------------|:-------------|:-------------|
| Expense Ratio           | 0.0003        | 0.002       | 0.0018       | 0.0006       |
| Assets Under Management | 1700000000000 | 99391417395 | 475858211608 | 118697006995 |
| NAV                     | 698.45        | 216.53      | 704.35       | 35.26        |
| Price                   | 703.72        | 217.09      | 713.52       | 35.155       |
| Premium/Discount        | 0.0002        | 0.0         | 0.0001       | 0.0003       |
| Holdings Count          | 505           | 505         | 102          | 102          |

`get_information` returns everything else the issuer publishes about a fund, including its identifiers, description and website.

### Holdings and Weightings

The holdings are the companies a fund owns, with the number of shares, the market value and the weight of each. `limit` keeps the largest holdings per fund and `show_columns` the columns that matter. To get the five largest holdings of each fund with their weights:

```python
funds.etf.get_holdings(limit=5, show_columns=["Name", "Weight"])
```

Which returns:

|                  | Name                  |   Weight |
|:-----------------|:----------------------|---------:|
| ('VOO', 'NVDA')  | NVIDIA Corp           |   0.0840 |
| ('VOO', 'AAPL')  | Apple Inc             |   0.0739 |
| ('VOO', 'MSFT')  | Microsoft Corp        |   0.0579 |
| ('VOO', 'AMZN')  | Amazon.com Inc        |   0.0372 |
| ('VOO', 'GOOGL') | Alphabet Inc          |   0.0307 |
| ('RSP', 'PTC')   | PTC Inc               |   0.0030 |
| ('RSP', 'MRNA')  | Moderna Inc           |   0.0029 |
| ('RSP', 'ACN')   | Accenture PLC         |   0.0028 |
| ('RSP', 'IT')    | Gartner Inc           |   0.0027 |
| ('RSP', 'HAS')   | Hasbro Inc            |   0.0026 |
| ('QQQ', 'NVDA')  | NVIDIA Corp           |   0.0810 |
| ('QQQ', 'AAPL')  | Apple Inc             |   0.0808 |
| ('QQQ', 'MSFT')  | Microsoft Corp        |   0.0620 |
| ('QQQ', 'MU')    | Micron Technology Inc |   0.0436 |
| ('QQQ', 'AMZN')  | Amazon.com Inc        |   0.0426 |
| ('SCHD', 'PG')   | PROCTER & GAMBLE      |   0.0441 |
| ('SCHD', 'TXN')  | TEXAS INSTRUMENT      |   0.0431 |
| ('SCHD', 'KO')   | COCA-COLA             |   0.0425 |
| ('SCHD', 'CVX')  | CHEVRON               |   0.0421 |
| ('SCHD', 'UNH')  | UNITEDHEALTH GROUP    |   0.0418 |

The equal-weighted RSP rebalances every quarter back to the same weight for each company, so its largest holdings are simply the ones that rose most since the last rebalance.

The holdings carry no sector or country, which is what `get_sector_weightings` and `get_country_weightings` are for. All four funds hold US companies almost entirely, so here the country weightings say little; they matter for global and emerging market funds. To get the weight of every sector in each fund:

```python
funds.etf.get_sector_weightings()
```

When plotted, one bar per fund:

{% include ft-chart.html id="etf-sectors" src="/assets/data/financetoolkit-guides/etf.json" label="Sector weightings of VOO, RSP, QQQ and SCHD" %}

### Concentration and Overlap

The number of holdings overstates how spread out a fund is when a few holdings carry most of the weight. The concentration measures it in three ways: the weight of the top 10 holdings, the Herfindahl-Hirschman index (the sum of the squared weights) and the effective number of holdings, one divided by that index: the number of equally weighted holdings that would be as concentrated. The overlap measures how much two funds hold of the same, the sum over their shared holdings of the smaller of the two weights. To calculate both:

```python
concentration = funds.etf.get_concentration()

overlap = funds.etf.get_overlap()
```

Which gives the following for the concentration:

|                              | VOO     | RSP     | QQQ     | SCHD    |
|:-----------------------------|:--------|:--------|:--------|:--------|
| Number of Holdings           | 507     | 507     | 105     | 100     |
| Largest Holding              | NVDA    | PTC     | NVDA    | PG      |
| Largest Weight               | 0.0840  | 0.0030  | 0.0810  | 0.0441  |
| Top 10 Weight                | 0.3913  | 0.0267  | 0.4664  | 0.4141  |
| Herfindahl-Hirschman Index   | 0.0230  | 0.0020  | 0.0316  | 0.0298  |
| Effective Number of Holdings | 43.4661 | 497.537 | 31.6617 | 33.5502 |

VOO holds 507 companies but is as concentrated as 43 equally weighted ones, about as concentrated as SCHD with its 100 holdings, and combining VOO and QQQ adds less than it seems, since more than half of their portfolios is the same. When plotted, with the overlap of every pair of funds in the last tab:

{% include ft-chart.html id="etf-concentration" src="/assets/data/financetoolkit-guides/etf.json" label="Top 10 weight, effective number of holdings and overlap of VOO, RSP, QQQ and SCHD" %}

### Look-Through Valuation

A fund has no earnings of its own, but its holdings do. The look-through valuation calculates the price-to-earnings, price-to-book, price-to-sales and price-to-free-cash-flow ratio, the dividend yield and the net profit margin of a fund's largest holdings, weighted by their weight in the fund. The multiples are weighted harmonic means, the multiple of the fund as a whole, so one holding with a very high multiple does not dominate. The coverage is the share of the fund's weight that these holdings represent. To value the 50 largest holdings of each fund:

```python
funds.etf.get_look_through_valuation(holdings=50)
```

Which returns:

|                         |     VOO |     RSP |     QQQ |    SCHD |
|:------------------------|--------:|--------:|--------:|--------:|
| Price-to-Earnings       | 26.7975 | 31.8900 | 31.9913 | 20.8778 |
| Price-to-Book           |  7.7024 |  7.6524 | 10.6063 |  3.9979 |
| Price-to-Sales          |  6.2095 |  2.6712 |  6.8421 |  1.9274 |
| Price-to-Free-Cash-Flow | 49.1603 | 22.4902 | 43.3711 | 15.8149 |
| Dividend Yield          |  0.0064 |  0.0088 |  0.0048 |  0.0318 |
| Net Profit Margin       |  0.3342 |  0.1139 |  0.2979 |  0.1531 |
| Coverage                |  0.6445 |  0.1190 |  0.8734 |  0.9673 |

The coverage shows how far to trust each figure: the 50 largest holdings make up 97% of SCHD, but only 12% of the equal-weighted RSP, whose multiples therefore describe a small part of the fund. Raising `holdings` raises the coverage at the cost of more requests. When plotted, one tab per measure:

{% include ft-chart.html id="etf-valuation" src="/assets/data/financetoolkit-guides/etf.json" label="Look-through price-to-earnings ratio, dividend yield and coverage of VOO, RSP, QQQ and SCHD" %}

### Tracking an Index

An index fund should deliver the return of its index minus its costs. The tracking difference is the annualized return of the fund minus that of the benchmark, the tracking error the annualized volatility of the difference from day to day. The benchmark of the `Toolkit` is the one the fund is measured against, so for an index fund it should be the index itself or another fund that tracks it. To compare two S&P 500 funds, VOO and the iShares Core S&P 500 ETF (IVV), with the largest one, the SPDR S&P 500 ETF Trust (SPY), from 2021 to 2025:

```python
index_funds = Toolkit(
    ["VOO", "IVV"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
    benchmark_ticker="SPY",
)

tracking = index_funds.etf.get_tracking()

yearly_tracking = index_funds.etf.get_tracking(yearly=True)
```

Which gives the following for the whole period:

|                     |    VOO |    IVV |
|:--------------------|-------:|-------:|
| Tracking Difference | 0.0008 | 0.0007 |
| Tracking Error      | 0.0081 | 0.0073 |
| Correlation         | 0.9990 | 0.9991 |
| Beta                | 0.9847 | 0.9890 |
| R Squared           | 0.9979 | 0.9983 |

Both funds beat SPY by less than a tenth of a percentage point a year, about the difference between their expense ratios of 0.03% and SPY's 0.0945%. The daily tracking error mostly reflects the timing of the funds' last trades at the close, which is why fund reports usually measure it from monthly returns with `period="monthly"`. When plotted, the tracking difference per year:

{% include ft-chart.html id="etf-tracking" src="/assets/data/financetoolkit-guides/etf.json" label="Tracking difference of VOO and IVV against SPY per year" %}

### Liquidity

A fund's own trading volume says how easily it can be bought and sold in the market. The liquidity measures it over the last year with the average volume and dollar volume, the dollar volume relative to the assets under management and the price impact per $100 million traded (the Amihud measure). To calculate it:

```python
funds.etf.get_liquidity()
```

Which returns:

|                               |       VOO |       RSP |        QQQ |      SCHD |
|:------------------------------|----------:|----------:|-----------:|----------:|
| Average Volume                |   8665395 |  12876800 |   49293458 |  21587171 |
| Average Dollar Volume         | 5.663e+09 | 2.582e+09 | 3.2146e+10 | 6.771e+08 |
| Dollar Volume to Assets       |    0.0033 |    0.0260 |     0.0676 |    0.0057 |
| Price Impact per $100 Million |    0.0001 |    0.0003 |     0.0000 |    0.0008 |

When plotted, the average dollar volume traded per day:

{% include ft-chart.html id="etf-liquidity" src="/assets/data/financetoolkit-guides/etf.json" label="Average daily dollar volume of VOO, RSP, QQQ and SCHD" %}

{% include ft-charts-script.html %}
