---
title:  Binomial Trees in the Finance Toolkit
permalink: /articles/binomial-trees
author_profile: true
classes: wide-sidebar
excerpt: "Binomial trees are a popular method for pricing options and other derivatives. The Finance Toolkit includes a function for binomial trees, which can price European and American options. This article provides an overview of the binomial tree module and demonstrates its use in option pricing."
---
<script src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML" type="text/javascript"></script>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10.6.0/dist/mermaid.min.js"></script>


Binomial trees are a widely used method for pricing options and other derivatives. The Finance Toolkit features a function for binomial trees capable of pricing both European and American options. This article outlines the binomial tree module and shows how to apply it to option pricing.

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
classDef boxfont fill:#3b9cba,stroke-width:0px,fill-opacity:0.7,color:white,radius:20px;
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

European options can only be exercised at expiration. Therefore, the option price at each node is calculated by discounting the expected future value back one time step. This leads to the following formulas for the Call option price at a given node:

<div style="display: flex; justify-content: space-between;margin-bottom:10px" markdown="1">

$$ C = e^{-(r - y) \cdot \Delta t} \cdot (p \cdot C_u + q \cdot C_d) $$

</div>

And the following formula for the Put option price at a given node:

<div style="display: flex; justify-content: space-between;margin-bottom:10px" markdown="1">

$$ P = e^{-(r - y) \cdot \Delta t} \cdot (p \cdot P_u + q \cdot P_d) $$

</div>

Where:

- $$ C $$ is the Call option price at the current node.
- $$ C_u $$ is the Call option price at the next up node.
- $$ C_d $$ is the Call option price at the next down node.
- $$ P $$ is the Put option price at the current node.
- $$ P_u $$ is the Put option price at the next up node.
- $$ P_d $$ is the Put option price at the next down node.

This results in the following binomial trees for Call and Put options, assuming a risk-free rate of 2%, dividend yield of 0.5%, volatility of 25%, time to expiration of 1 year, 3 time steps, and a strike price of $100:

<div class="row">
<div markdown="1" class="fifty-column-left mobile-max-column-width">

**Call Option**

{% raw %}
<div class="mermaid">
flowchart TD;
classDef boxfont fill:#3b9cba,stroke-width:0px,fill-opacity:0.7,color:white,radius:20px;

Step0["$18.32"]:::boxfont -- U --> Step1["$29.42"]:::boxfont
Step0["$18.32"] -- D --> Step2["$6.73"]:::boxfont

Step1["$29.42"] -- U --> Step3["$45.13"]:::boxfont
Step1["$29.42"] -- D --> Step4["$13.11"]:::boxfont

Step2["$6.73"] -- U --> Step4["$13.11"]:::boxfont
Step2["$6.73"] -- D --> Step5["$0.00"]:::boxfont

Step3["$45.13"] -- U --> Step6["$64.19"]:::boxfont
Step3["$45.13"] -- D --> Step7["$25.53"]:::boxfont

Step4["$13.11"] -- U --> Step7["$25.53"]:::boxfont
Step4["$13.11"] -- D --> Step8["$0.00"]:::boxfont

Step5["$0.00"] -- U --> Step8["$0.00"]:::boxfont
Step5["$0.00"] -- D --> Step9["$0.00"]:::boxfont
</div>
{% endraw %}

</div>

<div markdown="1" class="fifty-column-right mobile-max-column-width">

**Put Option**

{% raw %}
<div class="mermaid">

flowchart TD;
classDef boxfont fill:#3b9cba,stroke-width:0px,fill-opacity:0.7,color:white,radius:20px;

Step0["$3.92"]:::boxfont -- U --> Step1["$0.78"]:::boxfont
Step0["$3.92"] -- D --> Step2["$7.39"]:::boxfont

Step1["$0.78"] -- U --> Step3["$0.00"]:::boxfont
Step1["$0.78"] -- D --> Step4["$1.64"]:::boxfont

Step2["$7.39"] -- U --> Step4["$1.64"]:::boxfont
Step2["$7.39"] -- D --> Step5["$13.75"]:::boxfont

Step3["$0.00"] -- U --> Step6["$0.00"]:::boxfont
Step3["$0.00"] -- D --> Step7["$0.00"]:::boxfont

Step4["$1.64"] -- U --> Step7["$0.00"]:::boxfont
Step4["$1.64"] -- D --> Step8["$3.44"]:::boxfont

Step5["$13.75"] -- U --> Step8["$3.44"]:::boxfont
Step5["$13.75"] -- D --> Step9["$25.15"]:::boxfont

</div>
{% endraw %}

</div>
</div>

To interpret these results, the option price at the root node (time 0) represents the fair value of the option today. The prices at the final nodes (expiration) represent the intrinsic value (payoff) of the option. Prices at intermediate nodes represent the expected discounted value of the option at those points in time.

## American Options

A key difference exists between European and American options: European options can only be exercised at expiration, whereas American options can be exercised at any time up to and including expiration. The binomial tree for American options is constructed similarly to the European one, but the calculation at each node incorporates the possibility of early exercise. The value at each node is the maximum of the option's intrinsic value (if exercised immediately) and its expected discounted value (if held).

This leads to the following formulas for the option price at each node for an American Call Option:

<div style="display: flex; justify-content: space-between;margin-bottom:10px" markdown="1">

$$ C = max(S - K, e^{-(r - y) \cdot \Delta t} \cdot (p \cdot C_u + q \cdot C_d)) $$

</div>

And the following formula for the option price at each node for an American Put Option:

<div style="display: flex; justify-content: space-between;margin-bottom:10px" markdown="1">

$$ P = max(K - S, e^{-(r - y) \cdot \Delta t} \cdot (p \cdot P_u + q \cdot P_d)) $$

</div>

Where:

- $$ C $$ is the American Call option price at the current node.
- $$ P $$ is the American Put option price at the current node.
- $$ S $$ is the underlying asset price at the current node.
- $$ K $$ is the strike price.
- Other variables ($$r, y, \Delta t, p, q, C_u, C_d, P_u, P_d$$) are as defined previously.

This results in the following binomial trees for American Call and Put options, using the same parameters as before (risk-free rate 2%, dividend yield 0.5%, volatility 25%, 1 year to expiration, 3 time steps) but with a strike price of $90:

<div class="row">
<div markdown="1" class="fifty-column-left mobile-max-column-width">

**Call Option**

{% raw %}
<div class="mermaid">
flowchart TD;
classDef boxfont fill:#3b9cba,stroke-width:0px,fill-opacity:0.7,color:white,radius:20px;
classDef highlightfont fill:#d67f05,stroke-width:0px,fill-opacity:0.7,color:white,radius:20px;

Step0["$20.59"]:::boxfont -- U --> Step1["$32.10"]:::highlightfont
Step0["$20.59"] -- D --> Step2["$11.50"]:::boxfont

Step1["$32.10"] -- U --> Step3["$47.64"]:::highlightfont
Step1["$32.10"] -- D --> Step4["$17.64"]:::highlightfont

Step2["$11.50"] -- U --> Step4["$17.64"]:::highlightfont
Step2["$11.50"] -- D --> Step5["$5.00"]:::highlightfont

Step3["$47.64"] -- U --> Step6["$64.19"]:::highlightfont
Step3["$47.64"] -- D --> Step7["$25.53"]:::highlightfont

Step4["$17.64"] -- U --> Step7["$25.53"]:::highlightfont
Step4["$17.64"] -- D --> Step8["$0.00"]:::boxfont

Step5["$5.00"] -- U --> Step8["$0.00"]:::boxfont
Step5["$5.00"] -- D --> Step9["$0.00"]:::boxfont
</div>
{% endraw %}

</div>

<div markdown="1" class="fifty-column-right mobile-max-column-width">

**Put Option**

{% raw %}
<div class="mermaid">

flowchart TD;
classDef boxfont fill:#3b9cba,stroke-width:0px,fill-opacity:0.7,color:white,radius:20px;
classDef highlightfont fill:#d67f05,stroke-width:0px,fill-opacity:0.7,color:white,radius:20px;

Step0["$4.00"]:::boxfont -- U --> Step1["$0.81"]:::boxfont
Step0["$4.00"] -- D --> Step2["$7.56"]:::boxfont

Step1["$0.81"] -- U --> Step3["$0.00"]:::boxfont
Step1["$0.81"] -- D --> Step4["$1.69"]:::boxfont

Step2["$7.56"] -- U --> Step4["$1.69"]:::boxfont
Step2["$7.56"] -- D --> Step5["$13.98"]:::highlightfont

Step3["$0.00"] -- U --> Step6["$0.00"]:::boxfont
Step3["$0.00"] -- D --> Step7["$0.00"]:::boxfont

Step4["$1.69"] -- U --> Step7["$0.00"]:::boxfont
Step4["$1.69"] -- D --> Step8["$3.44"]:::boxfont

Step5["$13.98"] -- U --> Step8["$3.44"]:::boxfont
Step5["$13.98"] -- D --> Step9["$25.15"]:::highlightfont

</div>
{% endraw %}

</div>
</div>

Because the American option can be exercised early, its fair value can be higher than that of an equivalent European option, especially when the option is deep in the money. This occurs because the holder can capture the intrinsic value immediately rather than waiting. The nodes highlighted in <span style="color:#d67f05; font-weight:bold;">orange</span> in the binomial trees show where the American option's value (due to potential early exercise) exceeds the calculated European value at that node.

## Using the Finance Toolkit

The Finance Toolkit provides a function to calculate the binomial tree for both European and American options. Install the toolkit using pip:

```bash
pip install financetoolkit -U
```

Let's first demonstrate the core model function, which requires manual input of all parameters. Later, we'll show how to use it with real company data.

{% include code_header.html %}
{% highlight python %}
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
{% endhighlight %}

This code generates DataFrames representing the binomial trees for European Call, European Put, American Call, and American Put options, respectively. The values in these DataFrames correspond to the nodes in the binomial trees shown earlier:

<div class="row">
<div markdown="1" class="fifty-column-left mobile-max-column-width">

**European Call Option (Strike $90)**

|     |        0 |         1 |        2 |       3 |
|:----|---------:|----------:|---------:|--------:|
| UUU |  20.5888 |  32.1034  |  47.6431 | 64.1896 |
| UUD | nan      |  11.4975  |  17.6385 | 25.5274 |
| UDD | nan      | nan       |   5      |  0      |
| DDD | nan      | nan       | nan      |  0      |

<br>

**European Put Option (Strike $90)**

|     |         0 |          1 |         2 |        3 |
|:----|----------:|-----------:|----------:|---------:|
| UUU |   3.99601 |   0.813419 |   0       |  0       |
| UUD | nan       |   7.56254  |   1.69359 |  0       |
| UDD | nan       | nan        |  13.9826  |  3.44045 |
| DDD | nan       | nan        | nan       | 25.1448  |

</div>

<div markdown="1" class="fifty-column-right mobile-max-column-width">

**American Call Option (Strike $90)**

|     |        0 |        1 |        2 |       3 |
|:----|---------:|---------:|---------:|--------:|
| UUU |  20.5888 |  32.1034 |  47.6431 | 64.1896 |
| UUD | nan      |  11.4975 |  17.6385 | 25.5274 |
| UDD | nan      | nan      |   5      |  0      |
| DDD | nan      | nan      | nan      |  0      |

<br>

**American Put Option (Strike $90)**

|     |         0 |          1 |         2 |        3 |
|:----|----------:|-----------:|----------:|---------:|
| UUU |   4.00311 |   0.813419 |   0       |  0       |
| UUD | nan       |   7.56254  |   1.69359 |  0       |
| UDD | nan       | nan        |  13.9826  |  3.44045 |
| DDD | nan       | nan        | nan       | 25.1448  |

</div>
</div>
*(Note: Slight differences compared to the manually calculated trees might arise from rounding in the manual example or precise calculations in the code.)*

Now, let's apply this using actual company data. We'll use Apple Inc. (AAPL) and Microsoft Corporation (MSFT). The toolkit automatically fetches necessary inputs like the current stock price, risk-free rate, dividend yield, and calculates historical volatility.

{% include code_header.html %}
{% highlight python %}
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
{% endhighlight %}

Setting `show_input_info=True` provides insights into the parameters used for the calculation, which is helpful for understanding the model's inputs. The output might look similar to this (based on data up to February 7, 2024):

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

The model calculates the binomial tree for a range of strike prices relative to the current stock price (by default, 75% to 125% in 5-unit increments). Here's a sample output for an Apple European Call option with a $190 strike price and 10 time steps expiring on Feb 23, 2024:

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

This table represents the binomial tree for a European Call Option on Apple (AAPL) with a $190 strike price, expiring on February 23, 2024 (16 days from Feb 7), using 10 time steps. The calculated fair value of this option today (at the root node) is $4.32.

With this calculated fair value, we can compare it to the actual market price of the option using the `get_option_chains` method. We specify the same expiration date (`2024-02-23`) to match the binomial model's timeframe.

{% include code_header.html %}
{% highlight python %}
# Get option chain data for the specific expiration date
option_chains = companies.options.get_option_chains(expiration_date="2024-02-23")

# Display the relevant part for AAPL (e.g., filtering the DataFrame)
# print(option_chains['AAPL'][option_chains['AAPL']['Strike Price'] == 190])
{% endhighlight %}

Selecting the Apple data reveals the following market prices (showing relevant rows around the $190 strike):

|   Strike Price | Contract Symbol     | Currency   |   Last Price |   Change |   Percent Change |   Open Interest |   Bid |   Ask | Expiration   | Last Trade Date   |   Implied Volatility | In The Money   |   Volume |
|---------------:|:--------------------|:-----------|-------------:|---------:|-----------------:|----------------:|------:|------:|:-------------|:------------------|---------------------:|:---------------|---------:|
|            180 | AAPL240223C00180000 | USD        |        10.00 |     0.00 |             0.00 |             947 |  9.90 | 10.05 | 2024-02-23   | 2024-02-07        |               0.2930 | True           |      263 |
|            185 | AAPL240223C00185000 | USD        |         5.75 |    -0.10 |            -1.71 |            4128 |  5.70 |  5.80 | 2024-02-23   | 2024-02-07        |               0.2637 | True           |      449 |
|            190 | AAPL240223C00190000 | USD        |         <span style="color:#3b9cba; font-weight:bold;">2.67</span> |    -0.13 |            -4.64 |            8817 |  2.66 |  2.69 | 2024-02-23   | 2024-02-07        |               0.2383 | False          |     5594 |
|            195 | AAPL240223C00195000 | USD        |         0.95 |    -0.08 |            -7.77 |            7124 |  0.94 |  0.96 | 2024-02-23   | 2024-02-07        |               0.2217 | False          |     4149 |
|            200 | AAPL240223C00200000 | USD        |         0.34 |    -0.03 |            -8.11 |           17056 |  0.33 |  0.34 | 2024-02-23   | 2024-02-07        |               0.2129 | False          |     2927 |
*(Note: Bid/Ask and other market data added for context if available from the source)*

The binomial tree model calculated a fair value of $4.32 for the $190 strike call, while the market's last traded price was $2.67 (with a bid-ask spread around that). This suggests the option might be undervalued according to the model. Such discrepancies could indicate potential trading opportunities if an investor believes the price will converge towards the theoretical fair value.

As an alternative pricing model, the Black-Scholes formula can also be used. The Finance Toolkit provides this via the `get_black_scholes_model` method. Here, we calculate prices for options expiring within the next 20 days.

{% include code_header.html %}
{% highlight python %}
# Calculate Black-Scholes prices for options expiring within 20 days
black_scholes_results = companies.options.get_black_scholes_model(expiration_time_range=20)

# Display relevant part for AAPL Call options around the $190 strike
# print(black_scholes_results['AAPL']['Call'][['Strike Price', '2024-02-23']])
{% endhighlight %}

Selecting the results for Apple Inc. (AAPL) Call options expiring on Feb 23, 2024, shows the following (relevant rows):

|   Strike Price |   2024-02-20 |   2024-02-21 |   2024-02-22 |   2024-02-23 |   2024-02-24 |   2024-02-25 |   2024-02-26 |
|---------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|
|            180 |        10.49 |        10.60 |        10.71 |        10.81 |        10.92 |        11.02 |        11.13 |
|            185 |         6.73 |         6.87 |         7.02 |         7.16 |         7.29 |         7.43 |         7.56 |
|            190 |         3.86 |         4.02 |         4.18 |         <span style="color:#3b9cba; font-weight:bold;">4.33</span> |         4.48 |         4.62 |         4.76 |
|            195 |         1.96 |         2.10 |         2.24 |         2.37 |         2.50 |         2.63 |         2.76 |
|            200 |         0.87 |         0.97 |         1.07 |         1.17 |         1.27 |         1.37 |         1.47 |

Interestingly, both the Binomial Tree ($4.32) and the Black-Scholes model ($4.33) yield very similar fair values for the $190 strike call option expiring on Feb 23, 2024. This consistency strengthens the observation that the market price ($2.67) appears low compared to theoretical models.

{: .notice--info}
**Statistical Option Arbitrage**<br>
Comparing theoretical option prices (from models like Binomial Trees or Black-Scholes) with actual market prices to identify and trade on discrepancies is a strategy used in finance, sometimes referred to as "Statistical Option Arbitrage." While pure risk-free arbitrage is rare, statistical arbitrage aims to exploit persistent deviations based on historical patterns and model assumptions. For academic context, see articles like "*Statistical Arbitrage in the Black-Scholes Framework*" in the Journal of Financial and Quantitative Analysis ([link](https://www.researchgate.net/publication/263352435_Statistical_Arbitrage_in_the_Black-Scholes_Framework){:target="_blank"}), which explores theoretical possibilities for such strategies.

Did you find this article helpful? If you have questions or suggestions, please reach out via the links provided.