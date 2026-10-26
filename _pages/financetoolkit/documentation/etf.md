---
title: ETF
seo_title: "ETF Module | Finance Toolkit"
seo_title_suffix: false
excerpt: The ETF module analyzes exchange-traded funds, from their holdings, sector and country weightings to their tracking, concentration, overlap, valuation and liquidity.
description: The ETF module analyzes exchange-traded funds, from their holdings, sector and country weightings to their tracking, concentration, overlap, valuation and liquidity.
author_profile: false
permalink: /projects/financetoolkit/docs/etf
classes: wide-sidebar
layout: single
sidebar:
    nav: "financetoolkit-docs-etf"
---

The ETF module analyzes exchange-traded funds: their holdings, sector and country weightings, tracking against what they follow, concentration, the overlap between funds, valuation and liquidity.

Use it in Claude, ChatGPT or another AI assistant through the [Finance Toolkit MCP](/projects/financetoolkit/mcp), or install the Python package:

```python
pip install financetoolkit -U
```

{% include algolia.html %}

{% include financetoolkit-getting-started/etf.md %}

## get_holdings
Get the holdings of every fund: each asset it holds with the number of shares, the market value and the weight in the fund (as a decimal). This shows what the fund is actually exposed to and how concentrated it is; get_concentration and get_overlap summarize the weights.

Tickers that are not an ETF or fund have no holdings and return no data. They are not removed from the Toolkit instance.

**Also known as:** fund holdings, ETF constituents, fund portfolio.

**Args:**

- <u>overwrite (bool, optional):</u> Whether to retrieve the holdings again. Defaults to False.
- <u>show_columns (list[str] &#124; None, optional):</u> A list of column names to keep in the
result. Invalid names are reported and ignored. Defaults to None, which keeps
every column.
- <u>limit (int &#124; None, optional):</u> The number of largest holdings (by weight) to keep per
fund, e.g. 10 for the top 10, or of the smallest for a negative number, e.g.
-10. Defaults to None, which keeps every holding. The holdings carry no sector or
country; get_sector_weightings and get_country_weightings break the fund down by
those.

**Returns:**

pd.DataFrame &#124; None: The holdings per fund, indexed by asset (only by asset for a
single fund). None without an API key.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["QQQ", "VTI"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.etf.get_holdings().loc["QQQ"].head()
```

Which returns:

| Asset   | Name                       | ISIN         | CUSIP     |      Shares |    Weight |   Market Value | Updated At          |
|:--------|:---------------------------|:-------------|:----------|------------:|----------:|---------------:|:--------------------|
| NVDA    | NVIDIA Corp                | US67066G1040 | 67066G104 | 1.80964e+08 | 0.0850518 |    4.32937e+10 | 2026-10-07 14:14:58 |
| AAPL    | Apple Inc                  | US0378331005 | 037833100 | 1.09586e+08 | 0.0718253 |    3.65611e+10 | 2026-10-07 14:14:58 |
| MSFT    | Microsoft Corp             | US5949181045 | 594918104 | 5.57574e+07 | 0.057978  |    2.95124e+10 | 2026-10-07 14:14:58 |
| MU      | Micron Technology Inc      | US5951121038 | 595112103 | 2.34119e+07 | 0.0480888 |    2.44785e+10 | 2026-10-07 14:14:58 |
| AMD     | Advanced Micro Devices Inc | US0079031078 | 007903107 | 3.38406e+07 | 0.043174  |    2.19767e+10 | 2026-10-07 14:14:58 |

---

## get_information
Get everything Financial Modeling Prep publishes about every fund: its name, identifiers, issuer, asset class, domicile, inception date, expense ratio (as a decimal), assets under management, net asset value, number of holdings, description and website. The expense ratio in particular determines how much of the return is lost to costs every year. get_profile adds the latest price, the premium or discount to the NAV and the dollar volume to the key figures.

Tickers that are not an ETF or fund return no data. They are not removed from the Toolkit instance.

**Also known as:** fund profile, ETF profile, fund information.

**Args:**

- <u>overwrite (bool, optional):</u> Whether to retrieve the information again. Defaults to
False.

**Returns:**

pd.DataFrame &#124; None: The information (rows) per fund (columns). None without an API
key.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["QQQ", "VTI"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.etf.get_information().drop(["Description", "Website"])
```

Which returns:

|                         | QQQ                         | VTI                                         |
|:------------------------|:----------------------------|:--------------------------------------------|
| Name                    | Invesco QQQ Trust, Series 1 | Vanguard Morningstar Total Stock Market ETF |
| ISIN                    | US46090E1038                | US9229087690                                |
| CUSIP                   | 46090E103                   | 922908769                                   |
| Asset Class             | Equity                      | Large Cap Equity                            |
| Domicile                | US                          | US                                          |
| ETF Company             | Invesco                     | Vanguard                                    |
| Inception Date          | 1999-03-10                  | 2001-05-24                                  |
| Expense Ratio           | 0.0018                      | 0.0003                                      |
| Assets Under Management | 508484484641                | 2300000000000                               |
| Average Volume          | 39278732                    | 3259438                                     |
| NAV                     | 759.5                       | 381.13                                      |
| NAV Currency            | USD                         | USD                                         |
| Holdings Count          | 102                         | 3598                                        |
| Actively Trading        | True                        | True                                        |
| Updated At              | 2026-10-08T01:48:10.006Z    | 2026-10-08T02:22:30.046Z                    |

---

## get_country_weightings
Get how every fund is allocated across countries, as decimals, the largest weights of the first fund first. Two funds tracking similar markets can differ considerably here, which matters for the currency and political risk the fund carries.

Tickers that are not an ETF or fund return no data. They are not removed from the Toolkit instance.

**Also known as:** country allocation, geographic exposure, country exposure.

**Args:**

- <u>overwrite (bool, optional):</u> Whether to retrieve the weightings again. Defaults to
False.

**Returns:**

pd.DataFrame &#124; None: The weight per country (rows) and fund (columns). None without
an API key.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["QQQ", "VTI"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.etf.get_country_weightings().head()
```

Which returns:

| Country        |    QQQ |    VTI |
|:---------------|-------:|-------:|
| United States  | 0.9445 | 0.9733 |
| United Kingdom | 0.0164 | 0.0048 |
| Netherlands    | 0.0135 | 0.0003 |
| Canada         | 0.0096 | 0.0007 |
| Singapore      | 0.0074 | 0.0025 |

---

## get_sector_weightings
Get how every fund is allocated across sectors, as decimals, the largest weights of the first fund first. This shows whether a fund that looks broad is in fact concentrated in a few sectors, such as technology in many large-cap indices.

Tickers that are not an ETF or fund return no data. They are not removed from the Toolkit instance.

**Also known as:** sector allocation, sector exposure, sector breakdown.

**Args:**

- <u>overwrite (bool, optional):</u> Whether to retrieve the weightings again. Defaults to
False.

**Returns:**

pd.DataFrame &#124; None: The weight per sector (rows) and fund (columns). None without an
API key.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["QQQ", "VTI"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.etf.get_sector_weightings()
```

Which returns:

| Sector                 |      QQQ |      VTI |
|:-----------------------|---------:|---------:|
| Technology             | 0.603104 | 0.365041 |
| Communication Services | 0.117791 | 0.086689 |
| Consumer Cyclical      | 0.098732 | 0.089865 |
| Consumer Defensive     | 0.057355 | 0.042514 |
| Industrials            | 0.055378 | 0.088185 |
| Healthcare             | 0.036579 | 0.099808 |
| Utilities              | 0.010639 | 0.019731 |
| Basic Materials        | 0.009198 | 0.022242 |
| Cash & Others          | 0.004737 | 0.001929 |
| Energy                 | 0.004538 | 0.037377 |
| Financial Services     | 0.001949 | 0.123878 |
| Real Estate            | 0        | 0.022741 |

---

## get_profile
Get the profile of every fund: its name, issuer, asset class, domicile, inception date, expense ratio, assets under management, net asset value (NAV), latest price and the premium or discount of that price to the NAV, the number of holdings and the average daily volume and dollar volume. The expense ratio is what holding the fund costs every year; a premium means buying it costs more than the holdings are worth, which happens in stress for funds of less liquid assets such as bonds. The NAV is the latest Financial Modeling Prep publishes and the NAV Date the New York close it was struck at (the last 16:00 close before its update), so the premium compares the close on the NAV Date with the NAV (SEC Rule 6c-11), not the latest Price. It is empty without a close within three days before the NAV Date (an end date in the past), when the NAV is in another currency than the listing (a close in pence, GBp or GBX, is compared in pounds) and, with a logged warning, when it exceeds 50% either way, which is a data error rather than a price. With stale_nav=True the premium is given however old the NAV is: it compares the NAV with the last close on or before the NAV Date, or with the latest close when the prices end before the NAV Date or the NAV has no date. A NAV days older than the close then mostly shows how the market moved since, not what the fund trades at.

**Also known as:** ETF profile, expense ratio, assets under management, premium discount.

**Args:**

- <u>stale_nav (bool, optional):</u> Whether to give the premium for a NAV that is not
current, comparing it with the nearest close available. Defaults to False,
which leaves the premium empty without a close within three days before the
NAV Date.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the rounding of the Toolkit.

**Returns:**

pd.DataFrame: The profile fields (rows) per fund (columns).

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["VOO", "QQQ", "AGG"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-10-01",
)

toolkit.etf.get_profile()
```

Which returns:

|                         | VOO                  | QQQ                         | AGG                                  |
|:------------------------|:---------------------|:----------------------------|:-------------------------------------|
| Name                    | Vanguard S&P 500 ETF | Invesco QQQ Trust, Series 1 | iShares Core U.S. Aggregate Bond ETF |
| ETF Company             | Vanguard             | Invesco                     | IShares                              |
| Asset Class             | Large Cap Equity     | Equity                      | Fixed Income                         |
| Domicile                | US                   | US                          | US                                   |
| Inception Date          | 2010-09-07           | 1999-03-10                  | 2003-09-22                           |
| Expense Ratio           | 0.0003               | 0.0018                      | 0.0003                               |
| Assets Under Management | 1700000000000        | 475210352597                | 139388224538                         |
| NAV                     | 698.45               | 704.38                      | 96.07                                |
| NAV Date                | 2026-10-23           | 2026-10-23                  | 2026-10-23                           |
| Price                   | 698.58               | 704.4                       | 95.96                                |
| Premium/Discount        | 0.0002               | 0.0                         | -0.0011                              |
| Holdings Count          | 505                  | 102                         | 13445                                |
| Average Volume          | 8676842.9444         | 49390737.9087               | 9471894.381                          |
| Average Dollar Volume   | 5668940453.2057      | 32197925675.0503            | 933890010.5428                       |

---

## get_tracking
Measure how closely every fund tracks the Benchmark of the Toolkit, which for an index fund should be the index it follows (set benchmark_ticker to a total return index or to another fund of the same index). Per fund:

- Tracking Difference: the annualized return of the fund minus that of the Benchmark over the period, as issuers report it. An index fund trails its index by roughly its expense ratio; less points to securities lending income, more to a costly or loose replication.

- Tracking Error: the annualized volatility of the per-period return difference, how far the fund strays from the index from period to period.

- Correlation, Beta and R Squared of the fund's returns with the Benchmark's.

With yearly=True the tracking difference is given per calendar year instead, the return of the fund minus that of the Benchmark. The daily closes of two funds can differ by the timing of their last trade, which adds noise to a daily tracking error; fund reports usually measure it from monthly returns.

**Also known as:** tracking difference, tracking error, index tracking.

**Args:**

- <u>period (str, optional):</u> The return frequency (daily, weekly, monthly, quarterly or
yearly). Defaults to "daily".
- <u>yearly (bool, optional):</u> Whether to return the tracking difference per year.
Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the rounding of the Toolkit.

**Returns:**

pd.DataFrame: The tracking measures (rows) per fund (columns), or the tracking
difference per year (rows).

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["VOO", "IVV", "SPLG"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    benchmark_ticker="SPY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.etf.get_tracking(period="monthly")
```

Which returns:

|                     |    VOO |    IVV |    SPLG |
|:--------------------|-------:|-------:|--------:|
| Tracking Difference | 0.0008 | 0.0007 | -0      |
| Tracking Error      | 0.0011 | 0.0018 |  0.0021 |
| Correlation         | 1      | 0.9999 |  0.9999 |
| Beta                | 0.9994 | 1.0014 |  0.9986 |
| R Squared           | 0.9999 | 0.9999 |  0.9998 |

---

## get_concentration
Measure how concentrated every fund is from its holdings: the number of holdings, the largest holding and its weight, the weight of the ten largest (shares of the fund), the Herfindahl-Hirschman index (the sum of the squared weights, after scaling the weights of the holdings to sum to one, so cash and holdings without a weight do not dilute it) and the effective number of holdings (one over that index). A fund of 500 holdings whose ten largest make up a third of it behaves like a fund of far fewer stocks; the effective number says how many equally weighted holdings would give the same concentration.

**Also known as:** fund concentration, top 10 weight, Herfindahl index, effective number of holdings.

**Args:**

- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the rounding of the Toolkit.

**Returns:**

pd.DataFrame: The concentration measures (rows) per fund (columns).

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(["VOO", "QQQ", "RSP"], api_key="FINANCIAL_MODELING_PREP_KEY")

toolkit.etf.get_concentration()
```

Which returns:

|                              | VOO     | QQQ     | RSP      |
|:-----------------------------|:--------|:--------|:---------|
| Number of Holdings           | 507.0   | 105.0   | 507.0    |
| Largest Holding              | NVDA    | NVDA    | PTC      |
| Largest Weight               | 0.084   | 0.0814  | 0.003    |
| Top 10 Weight                | 0.3913  | 0.4665  | 0.0266   |
| Herfindahl-Hirschman Index   | 0.023   | 0.0316  | 0.002    |
| Effective Number of Holdings | 43.4661 | 31.6935 | 497.7398 |

---

## get_overlap
Measure how much the funds hold of the same: for every pair of funds the sum, over the holdings they share, of the smaller of the two weights. An overlap of 0.8 means 80% of the two portfolios is the same, so holding both adds little diversification.

**Also known as:** ETF overlap, portfolio overlap, holdings overlap.

**Args:**

- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the rounding of the Toolkit.

**Returns:**

pd.DataFrame: The overlap of every pair of funds, as decimals.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(["VOO", "QQQ", "VTI", "SCHD"], api_key="FINANCIAL_MODELING_PREP_KEY")

toolkit.etf.get_overlap()
```

Which returns:

|      |    VOO |    QQQ |    VTI |   SCHD |
|:-----|-------:|-------:|-------:|-------:|
| VOO  | 1.0017 | 0.556  | 0.8911 | 0.0764 |
| QQQ  | 0.556  | 1.0014 | 0.4994 | 0.0516 |
| VTI  | 0.8911 | 0.4994 | 1.0005 | 0.071  |
| SCHD | 0.0764 | 0.0516 | 0.071  | 1      |

---

## get_look_through_valuation
Value every fund through its holdings: the price-to-earnings, price-to-book, price-to-sales and price-to-free-cash-flow ratio, the dividend yield and the net profit margin of its largest holdings, weighted by their weight in the fund. The multiples are weighted harmonic means, the multiple of the fund as a whole, so one holding with a very high multiple does not dominate. The coverage is the share of the fund's weight held in holdings with a usable, non-zero price-to-earnings ratio; more holdings raise it at the cost of more requests.

The ratios are the trailing twelve month ratios Financial Modeling Prep calculates for every holding.

**Also known as:** look-through valuation, fund P/E, weighted average P/E, portfolio valuation.

**Args:**

- <u>holdings (int, optional):</u> The number of largest holdings to value per fund.
Defaults to 25.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the rounding of the Toolkit.

**Returns:**

pd.DataFrame: The valuation measures and the coverage (rows) per fund (columns).

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(["VOO", "QQQ", "SCHD"], api_key="FINANCIAL_MODELING_PREP_KEY")

toolkit.etf.get_look_through_valuation()
```

Which returns:

|                         |     VOO |     QQQ |    SCHD |
|:------------------------|--------:|--------:|--------:|
| Price-to-Earnings       | 26.616  | 31.6436 | 20.7484 |
| Price-to-Book           |  8.3525 | 10.2411 |  4.7307 |
| Price-to-Sales          |  7.5579 |  7.0579 |  2.2584 |
| Price-to-Free-Cash-Flow | 59.957  | 53.445  | 17.0266 |
| Dividend Yield          |  0.0047 |  0.0038 |  0.0308 |
| Net Profit Margin       |  0.3673 |  0.3113 |  0.1583 |
| Coverage                |  0.5324 |  0.7154 |  0.8077 |

---

## get_liquidity
Measure how liquid every fund is to trade over the last year of the period: its average daily volume and dollar volume, that dollar volume relative to the fund's assets under management, and the price impact of trading 100 million dollars in a day (the Amihud, 2002, illiquidity: the average absolute daily return per dollar traded, scaled to 100 million). An ETF can also be traded through its holdings, so a thinly traded fund of liquid holdings is easier to trade than its own volume suggests; a fund whose holdings are themselves illiquid (small companies, high yield bonds) is not.

For more information, see the following paper:

- Amihud, Y. (2002). "Illiquidity and Stock

**Returns:** Cross-Section and Time-Series
Effects." Journal of Financial Markets, 5(1), 31-56.

Also known as: ETF liquidity, dollar volume, Amihud illiquidity, price impact.

**Args:**

- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which keeps the full precision (the price impact of the largest
funds is a fraction of a basis point).

**Returns:**

pd.DataFrame: The liquidity measures (rows) per fund (columns).

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["VOO", "QQQ", "ARKK"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

toolkit.etf.get_liquidity(rounding=6)
```

Which returns:

|                               |               VOO |                QQQ |             ARKK |
|:------------------------------|------------------:|-------------------:|-----------------:|
| Average Volume                |    7734399.056000 |    48666218.588000 |  10799597.760000 |
| Average Dollar Volume         | 4400329488.944520 | 26740006060.354679 | 719035298.234000 |
| Dollar Volume to Assets       |          0.002588 |           0.056270 |         0.090822 |
| Price Impact per $100 Million |          0.000179 |           0.000036 |         0.002990 |

---

