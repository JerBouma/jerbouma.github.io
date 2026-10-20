---
title: "Options"
seo_title: "Options Guide | Finance Toolkit"
seo_title_suffix: false
excerpt: "How to price options, read option chains and implied volatility, and calculate every Greek with the Finance Toolkit's Options module."
description: "Price options with Black-Scholes and binomial trees, read option chains and implied volatility, and calculate first to third order Greeks in Python."
author_profile: false
permalink: /projects/financetoolkit/docs/getting-started/options
classes: wide-sidebar
layout: single
redirect_from:
  - /projects/financetoolkit/options-notebook
sidebar:
  nav: "financetoolkit-guides"
---

The Options module prices options and calculates the sensitivities that drive their value. It covers the Black-Scholes model and the binomial model, the option chains as they currently trade and the implied volatility behind them, and the first, second and third order Greeks. All inputs (the stock price, its volatility, the dividend yield and the risk-free rate) come from the data the Toolkit already collects, so a single call returns a full grid of strike prices and expiration dates for every ticker.

This guide uses Apple, Microsoft, Alphabet and Amazon, with price history from 2005 onwards.

## Loading the Data

The Options module is part of the `Toolkit` class. The historical prices, from which the module derives the volatility, and the treasury rates, which serve as the risk-free rate, are collected on the first call and reused after that. The start date therefore also sets the period over which the volatility is measured.

To load the data for the four companies:

```python
import pandas as pd

from financetoolkit import Toolkit

companies = Toolkit(
    ["AAPL", "MSFT", "GOOGL", "AMZN"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2005-01-01",
)
```

## Black-Scholes Model

The Black-Scholes model gives the theoretical value of a European option from five inputs: the stock price, the strike price, the time to expiration, the volatility and the risk-free rate (plus the dividend yield). By default the module uses the latest stock price, strike prices from 75% to 125% of that price in steps of 5, and every day over the next 30 days as the expiration date.

To calculate the value of a call option for every ticker, strike and expiration date:

```python
companies.options.get_black_scholes_model()
```

Which gives, with a tab per company and a line for three of the expiration dates:

{% include ft-chart.html id="options-black-scholes" src="/assets/data/financetoolkit-guides/options.json" label="Black-Scholes value of a call option by strike price for Apple, Microsoft, Alphabet and Amazon" %}

Deep in-the-money options are worth little more than the difference between the stock price and the strike, whatever the expiration date. Near the money the time value takes over: with Apple at about $340, a $340 call is worth around $10 with a month to go and less than $2 a day before it expires. Pass `put_option=True` for puts.

## Binomial Model

The binomial model builds a tree of possible stock prices: in each time step the price moves up or down by a factor that follows from the volatility and the length of the step. The option value is then calculated backwards from expiration, node by node. Unlike Black-Scholes it can value American options, which can be exercised at any time before expiration, while European options can only be exercised at expiration. By default the tree spans one year in ten steps.

To value American call options with the binomial model:

```python
companies.options.get_binomial_model(american_option=True)
```

Which gives the value of the option at every node of the tree. For Apple's $340 call, the first five steps are, with each row the number of down moves so far:

| Down moves | Today | Step 1 | Step 2 | Step 3 | Step 4 |
|:-----------|------:|-------:|-------:|-------:|-------:|
| 0 | 41.80 | 58.96 | 81.17 | 108.85 | 141.96 |
| 1 | | 24.43 | 36.53 | 53.30 | 75.64 |
| 2 | | | 12.13 | 19.50 | 30.68 |
| 3 | | | | 4.60 | 8.11 |
| 4 | | | | | 1.02 |

The value today, $41.80, is the option price for a one-year expiration; every column further to the right is one step (about five weeks) closer to expiration.

## Option Chains and Implied Volatility

Both models above are theoretical. The option chains show the contracts as they currently trade, with bid, ask, volume, open interest and the implied volatility per strike. The implied volatility is the volatility at which the Black-Scholes value equals the market price, so it is the market's own estimate of future volatility. The expiration date has to be one that is currently listed: call `get_option_chains(show_expiration_dates=True)` to see which ones are available.

To get the option chains and the implied volatility for one expiration date:

```python
option_chains = companies.options.get_option_chains(expiration_date="2027-12-17")

implied_volatility = companies.options.get_implied_volatility(expiration_date="2027-12-17")
```

Which gives, for Apple's calls around the money with the stock at about $340:

| Strike | Last price | Bid | Ask | Volume | Open interest | Implied volatility | In the money |
|-------:|-----------:|----:|----:|-------:|--------------:|-------------------:|:------------:|
| 320 | 59.30 | 58.30 | 60.15 | 24 | 4,824 | 35.3% | Yes |
| 330 | 55.50 | 52.00 | 54.15 | 1 | 1,677 | 34.4% | Yes |
| 340 | 47.40 | 46.55 | 49.25 | 6 | 1,901 | 34.1% | No |
| 350 | 42.35 | 41.95 | 43.05 | 50 | 2,351 | 32.6% | No |
| 360 | 38.70 | 36.95 | 38.55 | 3 | 1,860 | 32.2% | No |

And the implied volatility for strikes from 60% to 150% of the current price, with a tab per company:

{% include ft-chart.html id="options-implied-volatility" src="/assets/data/financetoolkit-guides/options.json" label="Implied volatility by strike price for Apple, Microsoft, Alphabet and Amazon" %}

For most of them the implied volatility falls as the strike rises, the familiar volatility skew: the market pays more for protection against a large fall than the lognormal distribution of Black-Scholes assumes. The line is noisy because it is backed out from the last traded price of each contract, and contracts that rarely trade carry stale prices.

## Stock Price Simulation

Underneath the binomial model is the tree of stock prices itself. Each step multiplies the price by an up or a down factor, and because an up move followed by a down move ends at the same price as the reverse, the tree recombines: after ten steps there are only eleven possible prices.

To simulate the stock prices of the binomial tree in ten steps:

```python
stock_price_simulations = companies.options.get_stock_price_simulation(timesteps=10)
```

Which gives the tree for each company, with a line for each number of down moves:

{% include ft-chart.html id="options-simulation" src="/assets/data/financetoolkit-guides/options.json" label="Binomial tree of simulated stock prices for Apple, Microsoft, Alphabet and Amazon" %}

## Greeks

The Greeks measure how the value of an option changes when one of its inputs changes. Delta is the change in the option price for a change in the stock price, which is also the number of shares needed to hedge one option. It runs from 0 for far out-of-the-money calls to 1 for deep in-the-money calls.

To calculate the Delta for every ticker, strike and expiration date:

```python
companies.options.get_delta()
```

Which gives, with a tab per company:

{% include ft-chart.html id="options-delta" src="/assets/data/financetoolkit-guides/options.json" label="Delta of a call option by strike price for Apple, Microsoft, Alphabet and Amazon" %}

The closer to expiration, the steeper the curve: a day before expiry, an option is close to either fully in or fully out of the money, while with a month to go there is still a real chance it ends up on the other side.

Every Greek accepts the same parameters to change the grid: `start_date` sets the date of the stock price, `strike_price_range` the range of strikes around it and `expiration_time_range` the number of days to expiration. With `show_input_info=True` the Toolkit logs the inputs it used: the stock price on that date, the annualized volatility, the dividend yield and the risk-free rate (1.88% at the start of 2020). To calculate the Dual Gamma, the second derivative of the option value to the strike price, from 2 January 2020 with strikes within 20% of the price and expirations up to 180 days:

```python
companies.options.get_dual_gamma(
    start_date="2020-01-02",
    strike_price_range=0.2,
    expiration_time_range=180,
    show_input_info=True,
)
```

Which gives the Dual Gamma for expirations of about 30, 90 and 180 days, with a tab per company:

{% include ft-chart.html id="options-dual-gamma" src="/assets/data/financetoolkit-guides/options.json" label="Dual Gamma by strike price for Apple, Microsoft, Alphabet and Amazon" %}

Dual Gamma peaks at the money and flattens as the expiration date moves further away, because a longer time to expiration spreads the probability of where the stock ends up over a wider range of strikes.

## All Greeks at Once

Rather than calling each Greek separately, the `collect_` functions return all of them: `collect_first_order_greeks`, `collect_second_order_greeks`, `collect_third_order_greeks` or, for everything, `collect_all_greeks`.

To collect every Greek for every ticker, strike and expiration date:

```python
companies.options.collect_all_greeks()
```

Which gives, for Apple with a month to expiration and strikes below, at and above the money:

| Greek | Strike 320 | Strike 340 | Strike 360 |
|:------|-----------:|-----------:|-----------:|
| Delta | 0.8151 | 0.5276 | 0.2385 |
| Dual Delta | -0.7918 | -0.4965 | -0.2156 |
| Vega | 0.2552 | 0.3808 | 0.2965 |
| Theta | -0.1481 | -0.1931 | -0.1432 |
| Rho | 20.1321 | 13.4121 | 6.1661 |
| Epsilon | -21.9859 | -14.2317 | -6.4334 |
| Lambda | 11.8597 | 17.3627 | 24.0724 |
| Gamma | 0.0107 | 0.0160 | 0.0125 |
| Dual Gamma | 0.0121 | 0.0160 | 0.0111 |
| Vanna | -0.8459 | 0.0057 | 0.9351 |
| Charm | 1.2071 | -0.2735 | -1.7349 |
| Vomma | 72.6358 | -0.0379 | 63.6195 |
| Vera | -24.8440 | -2.8716 | 22.8669 |
| Veta | -0.0072 | -0.0065 | -0.0083 |
| Partial Derivative | 0.0121 | 0.0160 | 0.0111 |
| Speed | -0.0004 | -0.0001 | 0.0003 |
| Zomma | -0.0108 | -0.0616 | -0.0212 |
| Color | 0.0240 | 0.1015 | 0.0288 |
| Ultima | -633.9987 | -2.5876 | -600.4301 |

The at-the-money option has the highest Gamma, Vega and Theta: it is the most sensitive to a move in the stock and to a change in volatility, and loses the most value per day. Lambda, the percentage change in the option price for a percentage change in the stock price, is the highest for the out-of-the-money option, which is what makes those options a leveraged bet.

## Greeks Against the Stock Price

The Toolkit calculates the Greeks over a range of strike prices, but every formula is also available as a plain function in `financetoolkit.options.greeks_model`. That makes it straightforward to vary any other input instead, such as the stock price.

To calculate the Delta of a call and a put and the Gamma of a $100 strike option with six months to expiration, for stock prices from $50 to $149:

```python
from financetoolkit.options import greeks_model

STRIKE_PRICE = 100
RISK_FREE_RATE = 0.05
TIME_TO_EXPIRATION = 180 / 365
VOLATILITY = 0.2
DIVIDEND_YIELD = 0.01

delta_values_call = {}
delta_values_put = {}
gamma_values = {}

for stock_price in range(50, 150, 1):
    delta_values_call[stock_price] = greeks_model.get_delta(
        stock_price=stock_price,
        strike_price=STRIKE_PRICE,
        risk_free_rate=RISK_FREE_RATE,
        time_to_expiration=TIME_TO_EXPIRATION,
        volatility=VOLATILITY,
        dividend_yield=DIVIDEND_YIELD,
    )

    delta_values_put[stock_price] = greeks_model.get_delta(
        stock_price=stock_price,
        strike_price=STRIKE_PRICE,
        risk_free_rate=RISK_FREE_RATE,
        time_to_expiration=TIME_TO_EXPIRATION,
        volatility=VOLATILITY,
        dividend_yield=DIVIDEND_YIELD,
        put_option=True,
    )

    gamma_values[stock_price] = greeks_model.get_gamma(
        stock_price=stock_price,
        strike_price=STRIKE_PRICE,
        risk_free_rate=RISK_FREE_RATE,
        time_to_expiration=TIME_TO_EXPIRATION,
        volatility=VOLATILITY,
        dividend_yield=DIVIDEND_YIELD,
    )

greeks = pd.DataFrame(
    {
        "$100 Call Delta": delta_values_call,
        "$100 Put Delta": delta_values_put,
        "$100 Gamma": gamma_values,
    }
)
```

Which gives Delta and Gamma in separate tabs, since they are on very different scales:

{% include ft-chart.html id="options-delta-gamma" src="/assets/data/financetoolkit-guides/options.json" label="Delta and Gamma of a $100 strike option against the stock price" %}

The call Delta rises from 0 to 1 as the stock moves from far below to far above the strike, and the put Delta mirrors it from -1 to 0. Gamma, the slope of that curve, peaks just below the strike: that is where Delta changes the fastest and where hedging an option position takes the most rebalancing.

<div class="fs-ref"><a href="/projects/financetoolkit/docs/options"><i class="fas fa-book" aria-hidden="true"></i>Full reference: Options</a></div>

{% include ft-charts-script.html %}
