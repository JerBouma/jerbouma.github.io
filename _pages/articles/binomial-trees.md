---
title: Binomial Trees in the Finance Toolkit
seo_title: "Binomial Option Pricing in Python"
date: 2024-02-09
last_modified_at: 2026-11-18
permalink: /articles/binomial-trees
excerpt: "Binomial trees are a popular method for pricing options and other derivatives. The Finance Toolkit includes a function for binomial trees, which can price European and American options. This article provides an overview of the binomial tree module and demonstrates its use in option pricing."
description: "How binomial trees price European and American options, step by step, with worked examples and Python code from the Finance Toolkit."
layout: single
classes: wide-sidebar article-document
author_profile: false
collection: article
tags: [Risk & Derivatives]
share: true
standfirst: "A binomial tree can value an option that may be exercised early, which the Black-Scholes formula can't. How much does early exercise add, and how close do the model prices come to the market?"
key_points:
  - "A three-step tree values a one-year European call with a $90 strike on a $100 stock at $16.03, and the put at $4.75."
  - "Early exercise lifts the American put to $4.88 from $4.75 in a three-step tree, but with 200 steps it adds only about 6 cents."
  - "For an Apple $190 call, the binomial tree ($4.32) and Black-Scholes ($4.33) agree, but both sit well above the market's $2.67 and share the same 28.26% historical volatility."
updates:
  - date: 2026-11-18
    note: "Added a section on how many steps the tree needs, with the early-exercise value of the put at up to 200 steps."
cover:
  image: /assets/images/articles/binomial-trees/cover.jpg
  alt: "Traders on the floor of the Chicago Board of Trade in 1949, watching the price boards."
  credit: "Chicago Board of Trade traders, 1949, Stanley Kubrick for LOOK, public domain"
  link: "https://commons.wikimedia.org/wiki/File:Chicago_Board_of_Trade_traders_cph.3d02368.jpg"
  creator: "Stanley Kubrick"
  license: "https://creativecommons.org/publicdomain/mark/1.0/"
---
{% include mermaid.html %}


A three-step binomial tree values a one-year call with a $90 strike on a $100 stock at $16.03. Allowing early exercise lifts the matching put to $4.88 from $4.75, while the call doesn't change. I built a binomial tree function into the Finance Toolkit that prices both European and American options. This article explains how the tree is built, how it values each type of option, and how the results for Apple compare with the market.

The binomial tree model is based on potential up and down movements in the underlying asset's price, determined by its volatility. The formulas for these movements are:

<div style="display: flex; justify-content: space-between;margin-bottom:10px" markdown="1">

$$ u = e^{\sigma \sqrt{\Delta t}} $$

$$ d = e^{-\sigma \sqrt{\Delta t}} $$

</div>

Where:
- $$ u $$ is the factor for an upward price movement.
- $$ d $$ is the factor for a downward price movement.
- $$ \sigma $$ is the volatility of the underlying asset.
- $$ \Delta t $$ is the length of a single time step.

The tree is constructed by applying these up and down factors sequentially from the current price of the underlying asset. For instance, if $$ u = 1.1 $$ and $$ d = 0.9 $$, a tree with 3 time steps starting from a price of $100 would look like this:

{% raw %}
<div class="mermaid" style="text-align:center">
flowchart LR;
classDef boxfont stroke-width:1.25px;
Step0["$100"]:::boxfont -- U --> Step1["$110"]:::boxfont
Step0["$100"] -- D --> Step2["$90"]:::boxfont

Step1["$110"] -- U --> Step4["$121"]:::boxfont

Step1["$110"] -- D --> Step3["$99"]:::boxfont
Step2["$90"] -- U --> Step3["$99"]:::boxfont

Step2["$90"] -- D --> Step5["$81"]:::boxfont

Step4["$121"] -- U --> Step7["$133"]:::boxfont
Step4["$121"] -- D --> Step6["$109"]:::boxfont

Step3["$99"] -- U --> Step6["$109"]:::boxfont
Step3["$99"] -- D --> Step8["$89"]:::boxfont

Step5["$81"] -- U --> Step8["$89"]:::boxfont
Step5["$81"] -- D --> Step9["$73"]:::boxfont


</div>
{% endraw %}

The option price is calculated at expiration (the final nodes) using the following formulas for Call and Put options, respectively:

<div style="display: flex; justify-content: space-between;margin-bottom:10px" markdown="1">

$$ C = max(S - K, 0) $$

$$ P = max(K - S, 0) $$

</div>

Where:
- $$ C $$ is the Call option price.
- $$ P $$ is the Put option price.
- $$ S $$ is the price of the underlying asset at expiration.
- $$ K $$ is the strike price.

To determine the option price at earlier nodes, the tree is evaluated backward from expiration using the risk-neutral pricing probabilities:

<div style="display: flex; justify-content: space-between;margin-bottom:10px" markdown="1">

$$ p = \frac{e^{(r - y) \cdot \Delta t} - d}{u - d} $$

$$ q = 1 - p $$

</div>

Where:

- $$ p $$ is the risk-neutral probability of an up movement.
- $$ q $$ is the risk-neutral probability of a down movement.
- $$ r $$ is the risk-free interest rate.
- $$ y $$ is the dividend yield.
- $$ \Delta t $$ is the time step.

## European Options

A European option can only be exercised at expiration, so its price at each node is the expected value one step later, discounted back one time step. This leads to the following formulas for the Call option price at a given node:

<div style="display: flex; justify-content: space-between;margin-bottom:10px" markdown="1">

$$ C = e^{-r \cdot \Delta t} \cdot (p \cdot C_u + q \cdot C_d) $$

</div>

And the following formula for the Put option price at a given node:

<div style="display: flex; justify-content: space-between;margin-bottom:10px" markdown="1">

$$ P = e^{-r \cdot \Delta t} \cdot (p \cdot P_u + q \cdot P_d) $$

</div>

Where:

- $$ C $$ is the Call option price at the current node.
- $$ C_u $$ is the Call option price at the next up node.
- $$ C_d $$ is the Call option price at the next down node.
- $$ P $$ is the Put option price at the current node.
- $$ P_u $$ is the Put option price at the next up node.
- $$ P_d $$ is the Put option price at the next down node.

With a risk-free rate of 2%, a dividend yield of 0.5%, volatility of 25%, 1 year to expiration, 3 time steps and a strike price of $90, the root nodes give a call worth $16.03 today and a put worth $4.75:

<div class="row">
<div markdown="1" class="fifty-column-left mobile-max-column-width">

**Call Option**

{% raw %}
<div class="mermaid">
flowchart TD;
classDef boxfont stroke-width:1.25px;
Step0["$16.03"]:::boxfont -- U --> Step1["$27.25"]:::boxfont
Step0["$16.03"] -- D --> Step2["$5.83"]:::boxfont
Step1["$27.25"] -- U --> Step3["$43.84"]:::boxfont
Step1["$27.25"] -- D --> Step4["$12.20"]:::boxfont
Step2["$5.83"] -- U --> Step4["$12.20"]
Step2["$5.83"] -- D --> Step5["$0.00"]:::boxfont
Step3["$43.84"] -- U --> Step6["$64.19"]:::boxfont
Step3["$43.84"] -- D --> Step7["$25.53"]:::boxfont
Step4["$12.20"] -- U --> Step7["$25.53"]
Step4["$12.20"] -- D --> Step8["$0.00"]:::boxfont
Step5["$0.00"] -- U --> Step8["$0.00"]
Step5["$0.00"] -- D --> Step9["$0.00"]:::boxfont
</div>
{% endraw %}

</div>

<div markdown="1" class="fifty-column-right mobile-max-column-width">

**Put Option**

{% raw %}
<div class="mermaid">
flowchart TD;
classDef boxfont stroke-width:1.25px;
Step0["$4.75"]:::boxfont -- U --> Step1["$0.91"]:::boxfont
Step0["$4.75"] -- D --> Step2["$8.37"]:::boxfont
Step1["$0.91"] -- U --> Step3["$0.00"]:::boxfont
Step1["$0.91"] -- D --> Step4["$1.77"]:::boxfont
Step2["$8.37"] -- U --> Step4["$1.77"]
Step2["$8.37"] -- D --> Step5["$14.60"]:::boxfont
Step3["$0.00"] -- U --> Step6["$0.00"]:::boxfont
Step3["$0.00"] -- D --> Step7["$0.00"]:::boxfont
Step4["$1.77"] -- U --> Step7["$0.00"]
Step4["$1.77"] -- D --> Step8["$3.44"]:::boxfont
Step5["$14.60"] -- U --> Step8["$3.44"]
Step5["$14.60"] -- D --> Step9["$25.14"]:::boxfont
</div>
{% endraw %}

</div>
</div>

To interpret these results, the option price at the root node (time 0) represents the fair value of the option today. The prices at the final nodes (expiration) represent the intrinsic value (payoff) of the option. Prices at intermediate nodes represent the expected discounted value of the option at those points in time.

## American Options

The main difference between European and American options is that European options can only be exercised at expiration, whereas American options can be exercised at any time up to and including expiration. The binomial tree for American options is constructed similarly to the European one, but the calculation at each node incorporates the possibility of early exercise. The value at each node is the maximum of the option's intrinsic value (if exercised immediately) and its expected discounted value (if held).

This leads to the following formulas for the option price at each node for an American Call Option:

<div style="display: flex; justify-content: space-between;margin-bottom:10px" markdown="1">

$$ C = max(S - K, e^{-r \cdot \Delta t} \cdot (p \cdot C_u + q \cdot C_d)) $$

</div>

And the following formula for the option price at each node for an American Put Option:

<div style="display: flex; justify-content: space-between;margin-bottom:10px" markdown="1">

$$ P = max(K - S, e^{-r \cdot \Delta t} \cdot (p \cdot P_u + q \cdot P_d)) $$

</div>

Where:

- $$ C $$ is the American Call option price at the current node.
- $$ P $$ is the American Put option price at the current node.
- $$ S $$ is the underlying asset price at the current node.
- $$ K $$ is the strike price.
- Other variables ($$r, y, \Delta t, p, q, C_u, C_d, P_u, P_d$$) are as defined previously.

With the same parameters as before (risk-free rate 2%, dividend yield 0.5%, volatility 25%, 1 year to expiration, 3 time steps and a strike price of $90), the American trees differ only where exercising early pays more than holding:

<div class="row">
<div markdown="1" class="fifty-column-left mobile-max-column-width">

**Call Option**

{% raw %}
<div class="mermaid">
flowchart TD;
classDef boxfont stroke-width:1.25px;
classDef highlightfont stroke-width:1.25px;
Step0["$16.03"]:::boxfont -- U --> Step1["$27.25"]:::boxfont
Step0["$16.03"] -- D --> Step2["$5.83"]:::boxfont
Step1["$27.25"] -- U --> Step3["$43.84"]:::boxfont
Step1["$27.25"] -- D --> Step4["$12.20"]:::boxfont
Step2["$5.83"] -- U --> Step4["$12.20"]
Step2["$5.83"] -- D --> Step5["$0.00"]:::boxfont
Step3["$43.84"] -- U --> Step6["$64.19"]:::boxfont
Step3["$43.84"] -- D --> Step7["$25.53"]:::boxfont
Step4["$12.20"] -- U --> Step7["$25.53"]
Step4["$12.20"] -- D --> Step8["$0.00"]:::boxfont
Step5["$0.00"] -- U --> Step8["$0.00"]
Step5["$0.00"] -- D --> Step9["$0.00"]:::boxfont
</div>
{% endraw %}

</div>

<div markdown="1" class="fifty-column-right mobile-max-column-width">

**Put Option**

{% raw %}
<div class="mermaid">
flowchart TD;
classDef boxfont stroke-width:1.25px;
classDef highlightfont stroke-width:1.25px;
Step0["$4.88"]:::highlightfont -- U --> Step1["$0.91"]:::boxfont
Step0["$4.88"] -- D --> Step2["$8.61"]:::highlightfont
Step1["$0.91"] -- U --> Step3["$0.00"]:::boxfont
Step1["$0.91"] -- D --> Step4["$1.77"]:::boxfont
Step2["$8.61"] -- U --> Step4["$1.77"]
Step2["$8.61"] -- D --> Step5["$15.07"]:::highlightfont
Step3["$0.00"] -- U --> Step6["$0.00"]:::boxfont
Step3["$0.00"] -- D --> Step7["$0.00"]:::boxfont
Step4["$1.77"] -- U --> Step7["$0.00"]
Step4["$1.77"] -- D --> Step8["$3.44"]:::boxfont
Step5["$15.07"] -- U --> Step8["$3.44"]
Step5["$15.07"] -- D --> Step9["$25.14"]:::boxfont
</div>
{% endraw %}

</div>
</div>

Because the American option can be exercised early, its fair value can be higher than that of an equivalent European option, especially when the option is deep in the money. The holder can take the intrinsic value straight away instead of waiting for expiration. The nodes highlighted in <span style="color:#d67f05; font-weight:bold;">orange</span> in the binomial trees show where the American option's value (due to potential early exercise) exceeds the calculated European value at that node.

In this example that only happens for the put. After two down moves the stock is at $74.93, and exercising the put there pays $15.07 straight away, more than the $14.60 that holding it is worth. That early-exercise value carries back through the tree, so the American put is worth $4.88 today against $4.75 for the European put. The American call is worth exactly the same as the European call, $16.03: with a dividend yield of only 0.5%, exercising a call early never beats holding it.

## How Many Steps Are Enough

Three steps keep the trees readable, but three steps is a coarse picture of a year. A tree with more steps moves in smaller jumps, and its price converges to the Black-Scholes price for the European call, $16.03. The same call priced with 1 to 200 steps, with the early-exercise value of the put in the second tab:

{% capture code_convergence %}
```python
# pip install financetoolkit
from financetoolkit.options import binomial_trees_model, black_scholes_model

inputs = dict(stock_price=100, strike_price=90, years=1, risk_free_rate=0.02,
              volatility=0.25, dividend_yield=0.005)

def price(steps, **kwargs):
    tree = binomial_trees_model.get_option_payoffs(timesteps=steps, **inputs, **kwargs)
    return tree.iloc[0, 0]  # the value today, at the root of the tree

call = {n: price(n) for n in range(1, 201)}
early_exercise = {
    n: price(n, put_option=True, american_option=True) - price(n, put_option=True)
    for n in range(1, 201)
}
black_scholes = black_scholes_model.get_black_scholes(100, 90, 0.02, 0.25, 1, 0.005)
```
{% endcapture %}
{% include ft-chart.html id="binom-convergence" src="/assets/data/article-charts.json" label="Binomial tree price of the European call and the value of early exercise of the put, by number of steps from 1 to 200" code=code_convergence %}

The price doesn't close in on Black-Scholes in a straight line. It zigzags from one number of steps to the next, because the strike sits at a different place between the final nodes each time. The three-step tree lands within a tenth of a cent of Black-Scholes by luck: with ten steps the tree is 16 cents off. The error only stays within 5 cents from 30 steps on, and within a cent from about 160 steps.

**The early-exercise value is about half what the small tree suggests.** In the three-step tree the right to exercise the put early is worth $0.13. With more steps it settles at about $0.06, so the American put is worth around $4.80 rather than $4.88. For a put this far out of the money, a three-step tree overstates what early exercise adds.

## Using the Finance Toolkit

The Finance Toolkit provides a function to calculate the binomial tree for both European and American options. Install the toolkit using pip:

```bash
pip install financetoolkit -U
```

The core model function takes every parameter by hand, which makes it easy to reproduce the four trees above before moving on to real company data:

```python
from financetoolkit.options import binomial_trees_model

# Calculate European Call option payoffs
option_pay_off_ec = binomial_trees_model.get_option_payoffs(
    stock_price=100,
    strike_price=90,
    years=1,
    timesteps=3,
    volatility=0.25,
    dividend_yield=0.005,
    risk_free_rate=0.02,
    put_option=False, # Set to True for Put Option
    american_option=False # Set to True for American Option
)

# Calculate European Put option payoffs
option_pay_off_ep = binomial_trees_model.get_option_payoffs(
    stock_price=100,
    strike_price=90,
    years=1,
    timesteps=3,
    volatility=0.25,
    dividend_yield=0.005,
    risk_free_rate=0.02,
    put_option=True,
    american_option=False
)

# Calculate American Call option payoffs
option_pay_off_ac = binomial_trees_model.get_option_payoffs(
    stock_price=100,
    strike_price=90,
    years=1,
    timesteps=3,
    volatility=0.25,
    dividend_yield=0.005,
    risk_free_rate=0.02,
    put_option=False,
    american_option=True
)

# Calculate American Put option payoffs
option_pay_off_ap = binomial_trees_model.get_option_payoffs(
    stock_price=100,
    strike_price=90,
    years=1,
    timesteps=3,
    volatility=0.25,
    dividend_yield=0.005,
    risk_free_rate=0.02,
    put_option=True,
    american_option=True
)
```

This code generates DataFrames representing the binomial trees for European Call, European Put, American Call, and American Put options, respectively. The values in these DataFrames correspond to the nodes in the binomial trees shown earlier:

**European Call Option (Strike $90)**

| Node |        0 |        1 |        2 |        3 |
|:----|---------:|---------:|---------:|---------:|
| UUU | 16.0335 | 27.2484 | 43.8416 | 64.1896 |
| DUU | nan | 5.8347 | 12.2042 | 25.5274 |
| DDU | nan | nan | 0.0000 | 0.0000 |
| DDD | nan | nan | nan | 0.0000 |

**European Put Option (Strike $90)**

| Node |        0 |        1 |        2 |        3 |
|:----|---------:|---------:|---------:|---------:|
| UUU | 4.7501 | 0.9135 | 0.0000 | 0.0000 |
| DUU | nan | 8.3711 | 1.7728 | 0.0000 |
| DDU | nan | nan | 14.6012 | 3.4404 |
| DDD | nan | nan | nan | 25.1448 |

**American Call Option (Strike $90)**

| Node |        0 |        1 |        2 |        3 |
|:----|---------:|---------:|---------:|---------:|
| UUU | 16.0335 | 27.2484 | 43.8416 | 64.1896 |
| DUU | nan | 5.8347 | 12.2042 | 25.5274 |
| DDU | nan | nan | 0.0000 | 0.0000 |
| DDD | nan | nan | nan | 0.0000 |

**American Put Option (Strike $90)**

| Node |        0 |        1 |        2 |        3 |
|:----|---------:|---------:|---------:|---------:|
| UUU | 4.8758 | 0.9135 | 0.0000 | 0.0000 |
| DUU | nan | 8.6150 | 1.7728 | 0.0000 |
| DDU | nan | nan | 15.0744 | 3.4404 |
| DDD | nan | nan | nan | 25.1448 |

The same function runs on real company data, here for Apple Inc. (AAPL) and Microsoft Corporation (MSFT). The Finance Toolkit fetches the current stock price, the risk-free rate and the dividend yield itself, and calculates historical volatility from past prices:

```python
from financetoolkit import Toolkit

# Initialize Toolkit with tickers and API key
# Replace "FINANCIAL_MODELING_PREP_KEY" with your actual key
companies = Toolkit(["AAPL", "MSFT"], api_key="FINANCIAL_MODELING_PREP_KEY")

# Calculate Binomial Model for options expiring in 16 days (approx)
# show_input_info=True displays the parameters used
binomial_results = companies.options.get_binomial_model(
    show_input_info=True,
    time_to_expiration=16/365,
    timesteps=10 # Example: using 10 timesteps
)
```

Setting `show_input_info=True` prints the parameters used for the calculation, which is helpful for understanding the model's inputs. The output might look similar to this (based on data up to February 7, 2024):

```plaintext
Based on the period 2013-02-11 to 2024-02-07 the following parameters were used:
Stock Price: AAPL (189.41), MSFT (414.05), Benchmark (498.1)
Volatility: AAPL (28.26%), MSFT (26.99%), Benchmark (17.46%)
Dividend Yield: AAPL (0.49%), MSFT (0.74%)
Up Movement: AAPL (101.89%), MSFT (101.8%)
Down Movement: AAPL (98.15%), MSFT (98.23%)
Risk Neutral Probability: AAPL (49.96%), MSFT (49.97%)
Risk Free Rate: 4.11%
Time Step (Delta t): 0.00438 years (16 days / 365 / 10 steps)
```

The model calculates the binomial tree for a range of strike prices relative to the current stock price (by default, 75% to 125% in 5-unit increments). For an Apple European Call option with a $190 strike price and 10 time steps, expiring on February 23, 2024, the root node in blue is the model's fair value today:

| Movement   |   2024-02-07 |   2024-02-08 |   2024-02-10 |   2024-02-11 |   2024-02-13 |   2024-02-15 |   2024-02-16 |   2024-02-18 |   2024-02-19 |   2024-02-21 |   2024-02-23 |
|:-----------|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|
| UUUUUUUUUU |       <span style="color:#3b9cba; font-weight:bold;">4.32</span> |       6.10 |       8.39 |      11.22 |      14.51 |      18.18 |      22.05 |      26.02 |      30.06 |      34.18   |      38.38 |
| UUUUUUUUUD |     nan      |       2.53 |       3.80  |       5.57 |       7.91 |      10.85 |      14.31 |      18.09 |      21.98 |      25.94 |      29.98 |
| UUUUUUUUDD |     nan      |     nan      |       1.26 |       2.03 |       3.22 |       4.97 |       7.39 |      10.53 |      14.20 |      18.02  |      21.91 |
| UUUUUUUDDD |     nan      |     nan      |     nan      |       0.47 |       0.84 |       1.48 |       2.54 |       4.26  |       6.85 |      10.38 |      14.13  |
| UUUUUUDDDD |     nan      |     nan      |     nan      |     nan      |       0.10  |       0.21 |       0.42 |       0.83 |       1.66 |       3.32 |       6.63 |
| UUUUUDDDDD |     nan      |     nan      |     nan      |     nan      |     nan      |       0.00  |       0.00 |       0.00 |       0.00 |       0.00 |       0.00 |
| UUUUDDDDDD |     nan      |     nan      |     nan      |     nan      |     nan      |     nan      |       0.00 |       0.00 |       0.00 |       0.00 |       0.00 |
| UUUDDDDDDD |     nan      |     nan      |     nan      |     nan      |     nan      |     nan      |     nan      |       0.00 |       0.00 |       0.00 |       0.00 |
| UUDDDDDDDD |     nan      |     nan      |     nan      |     nan      |     nan      |     nan      |     nan      |     nan      |       0.00 |       0.00 |       0.00 |
| UDDDDDDDDD |     nan      |     nan      |     nan      |     nan      |     nan      |     nan      |     nan      |     nan      |     nan      |       0.00 |       0.00 |
| DDDDDDDDDD |     nan      |     nan      |     nan      |     nan      |     nan      |     nan      |     nan      |     nan      |     nan      |     nan      |       0.00 |

That fair value is $4.32, for a call that expires 16 days after February 7, 2024. The `get_option_chains` method returns what the market charged for the same contract, with the same expiration date (`2024-02-23`) as the binomial model:

```python
# Get option chain data for the specific expiration date
option_chains = companies.options.get_option_chains(expiration_date="2024-02-23")

# Display the relevant part for AAPL (e.g., filtering the DataFrame)
# print(option_chains['AAPL'][option_chains['AAPL']['Strike Price'] == 190])
```

For Apple, the $190 call last traded at $2.67, below the model's value (rows around the $190 strike):

|   Strike Price | Contract Symbol     | Currency   |   Last Price |   Change |   Percent Change |   Open Interest |   Bid |   Ask | Expiration   | Last Trade Date   |   Implied Volatility | In The Money   |   Volume |
|---------------:|:--------------------|:-----------|-------------:|---------:|-----------------:|----------------:|------:|------:|:-------------|:------------------|---------------------:|:---------------|---------:|
|            180 | AAPL240223C00180000 | USD        |        10.00 |     0.00 |             0.00 |             947 |  9.90 | 10.05 | 2024-02-23   | 2024-02-07        |               0.2930 | True           |      263 |
|            185 | AAPL240223C00185000 | USD        |         5.75 |    -0.10 |            -1.71 |            4128 |  5.70 |  5.80 | 2024-02-23   | 2024-02-07        |               0.2637 | True           |      449 |
|            190 | AAPL240223C00190000 | USD        |         <span style="color:#3b9cba; font-weight:bold;">2.67</span> |    -0.13 |            -4.64 |            8817 |  2.66 |  2.69 | 2024-02-23   | 2024-02-07        |               0.2383 | False          |     5594 |
|            195 | AAPL240223C00195000 | USD        |         0.95 |    -0.08 |            -7.77 |            7124 |  0.94 |  0.96 | 2024-02-23   | 2024-02-07        |               0.2217 | False          |     4149 |
|            200 | AAPL240223C00200000 | USD        |         0.34 |    -0.03 |            -8.11 |           17056 |  0.33 |  0.34 | 2024-02-23   | 2024-02-07        |               0.2129 | False          |     2927 |

*Note: Bid/Ask and other market data added for context if available from the source*

The model's $4.32 is well above the $2.67 the market paid, with the bid and ask close to that last price. On the model's terms the call looks cheap. But the model takes Apple's [historical volatility](/articles/risk-exposure-major-indices-finance-toolkit) from prices between 2013 and 2024 (28.26%), while the option chain shows an implied volatility of 0.2383 for this strike. The market prices in less movement over the next 16 days than Apple's last 11 years would suggest.

The Black-Scholes formula is a second check, through the `get_black_scholes_model` method, here for options expiring within the next 20 days:

```python
# Calculate Black-Scholes prices for options expiring within 20 days
black_scholes_results = companies.options.get_black_scholes_model(expiration_time_range=20)

# Display relevant part for AAPL Call options around the $190 strike
# print(black_scholes_results['AAPL']['Call'][['Strike Price', '2024-02-23']])
```

For Apple's call options expiring on February 23, 2024, Black-Scholes lands within a cent of the binomial tree at the $190 strike:

|   Strike Price |   2024-02-20 |   2024-02-21 |   2024-02-22 |   2024-02-23 |   2024-02-24 |   2024-02-25 |   2024-02-26 |
|---------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|
|            180 |        10.49 |        10.60 |        10.71 |        10.81 |        10.92 |        11.02 |        11.13 |
|            185 |         6.73 |         6.87 |         7.02 |         7.16 |         7.29 |         7.43 |         7.56 |
|            190 |         3.86 |         4.02 |         4.18 |         <span style="color:#3b9cba; font-weight:bold;">4.33</span> |         4.48 |         4.62 |         4.76 |
|            195 |         1.96 |         2.10 |         2.24 |         2.37 |         2.50 |         2.63 |         2.76 |
|            200 |         0.87 |         0.97 |         1.07 |         1.17 |         1.27 |         1.37 |         1.47 |

The binomial tree ($4.32) and Black-Scholes ($4.33) give almost the same fair value for the $190 call expiring on February 23, 2024. That agreement is expected: with 10 steps the tree comes close to Black-Scholes, and both use the same 28.26% historical volatility. It doesn't confirm that the market's $2.67 is too low. My reading is that part of the gap comes from that one volatility input, which is why I would compare it with the implied volatility in the option chain before calling any contract mispriced.

{: .notice--info}
**Statistical Option Arbitrage**<br>
Comparing theoretical option prices (from models like Binomial Trees or Black-Scholes) with actual market prices to identify and trade on discrepancies is a strategy used in finance, sometimes referred to as "Statistical Option Arbitrage." While pure risk-free arbitrage is rare, statistical arbitrage aims to exploit persistent deviations based on historical patterns and model assumptions. For academic context, see Ahmet Göncü, "*Statistical Arbitrage in the Black-Scholes Framework*" (Quantitative Finance, 2015) ([researchgate.net](https://www.researchgate.net/publication/263352435_Statistical_Arbitrage_in_the_Black-Scholes_Framework){:target="_blank"}), which explores theoretical possibilities for such strategies.

{% include ft-charts-script.html %}
