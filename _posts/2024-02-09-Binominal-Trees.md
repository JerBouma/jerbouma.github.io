---
title:  Binomial Trees in the Finance Toolkit
permalink: /articles/binomial-trees
author_profile: true
classes: wide-sidebar
excerpt: "Binomial trees are a popular method for pricing options and other derivatives. The Finance Toolkit includes a function for binomial trees, which can be used to price European and American options. This article provides an overview of the binomial tree module and demonstrates how to use it to price options."
---
<script src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML" type="text/javascript"></script>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10.6.0/dist/mermaid.min.js"></script>


Binomial trees are a popular method for pricing options and other derivatives. The Finance Toolkit includes a function for binomial trees, which can be used to price European and American options. This article provides an overview of the binomial tree module and demonstrates how to use it to price options.

The binomial tree is based on up and down movements, which are determined by the volatility of the underlying asset. The formulas are as follows:

<div style="display: flex; justify-content: space-between;margin-bottom:10px" markdown="1">

$$ u = e^{\sigma \sqrt{\Delta t}} $$

$$ d = e^{-\sigma \sqrt{\Delta t}} $$

</div>

Where:
- $$ u $$ is the up movement
- $$ d $$ is the down movement
- $$ \sigma $$ is the volatility of the underlying asset
- $$ \Delta t $$ is the time step

The tree is constructed by moving up and down from the current price of the underlying asset. For example, if $$ u $$ is equal to 1.1 and $$ d $$ is equal to 0.9, a tree with 3 time steps would look like this:

{% raw %}
<div class="mermaid" style="text-align:center">
flowchart LR;
classDef boxfont fill:#3b9cba,stroke-width:0px,fill-opacity:0.7,color:white,radius:20px;
Step0["$100"]:::boxfont -- U --> Step1["$110"]:::boxfont
Step0["$100"] -- U --> Step2["$90"]:::boxfont

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

The option price is then calculated at the time of expiration (the final node) with the following formula for Call and Put option respectively:

<div style="display: flex; justify-content: space-between;margin-bottom:10px" markdown="1">

$$ C = max(S - K, 0) $$

$$ P = max(K - S, 0) $$

</div>

Where:
- $$ C $$ is the Call option price
- $$ P $$ is the Put option price
- $$ S $$ is the price of the underlying asset
- $$ K $$ is the strike price

Therefore, when reconstructing the tree, the option price at each node is calculated using the risk-neutral pricing formula:

<div style="display: flex; justify-content: space-between;margin-bottom:10px" markdown="1">

$$ p = \frac{e^{(r - y) \cdot \Delta t} - d}{u - d} $$

$$ q = 1 - p $$

</div>

Where:

- $$ p $$ is the probability of an up movement
- $$ q $$ is the probability of a down movement
- $$ r $$ is the risk-free interest rate
- $$ y $$ is the dividend yield
- $$ \Delta t $$ is the time step

## European Options

Given that European options can not be exercised early, this lead to the following formulas for the option price at each node for a Call Option:

<div style="display: flex; justify-content: space-between;margin-bottom:10px" markdown="1">

$$ C_u = e^{(-r - y) \cdot \Delta t} \cdot (p \cdot C_u + q \cdot C_d) $$

$$ C_d = e^{(-r - y) \cdot \Delta t} \cdot (p \cdot C_u + q \cdot C_d) $$

</div>

And the following formulas for the option price at each node for a Put Option:

<div style="display: flex; justify-content: space-between;margin-bottom:10px" markdown="1">

$$ P_u = e^{(-r - y) \cdot \Delta t} \cdot (p \cdot P_u + q \cdot P_d) $$

$$ P_d = e^{(-r - y) \cdot \Delta t} \cdot (p \cdot P_u + q \cdot P_d) $$

</div>

Where:

- $$ C_u $$ is the Call option price at the up node
- $$ C_d $$ is the Call option price at the down node
- $$ P_u $$ is the Put option price at the up node
- $$ P_d $$ is the Put option price at the down node

This results in the following binomial trees for Call and Put options, assuming the risk-free rate is 2%, dividend yield is 0.5%, volatility is 25%, the time to expiration is 1 year and the strike price is $100:

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
Step2["$6.73"] -- D --> Step5["$10.00"]:::boxfont

Step3["$45.13"] -- U --> Step6["$64.19"]:::boxfont
Step3["$45.13"] -- D --> Step7["$25.53"]:::boxfont

Step4["$13.11"] -- U --> Step7["$25.53"]:::boxfont
Step4["$13.11"] -- D --> Step8["$0.00"]:::boxfont

Step5["$10.00"] -- U --> Step8["$0.00"]:::boxfont
Step5["$10.00"] -- D --> Step9["$0.00"]:::boxfont
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
Step4["$13.75"] -- D --> Step8["$3.44"]:::boxfont

Step5["$13.75"] -- U --> Step8["$3.44"]:::boxfont
Step5["$13.75"] -- D --> Step9["$25.15"]:::boxfont

</div>
{% endraw %}

</div>
</div>

To interpret these results, the option price at the root node is the fair value of the option. The option price at the final node is the intrinsic value of the option. The option price at the intermediate nodes is the expected value of the option, discounted at the risk-free rate.

## American Options

There is a difference between European and American options. European options can only be exercised at expiration, while American options can be exercised at any time before expiration. The binomial tree for American options is constructed in the same way as for European options, but the option price at each node is calculated using the early exercise condition. The early exercise condition is the maximum of the intrinsic value of the option and the expected value of the option, discounted at the risk-free rate, this results in the following formulas:

This lead to the following formulas for the option price at each node for a Call Option:

<div style="display: flex; justify-content: space-between;margin-bottom:10px" markdown="1">

$$ C_u = max(S - K, C_\widehat{u}) $$

$$ C_d = max(S - K, C_\widehat{d}) $$

</div>

And the following formulas for the option price at each node for a Put Option:

<div style="display: flex; justify-content: space-between;margin-bottom:10px" markdown="1">

$$ P_u = max(K - S, P_\widehat{u}) $$

$$ P_d = max(K - S, P_\widehat{d}) $$

</div>

Where:

- $$ C_u $$ and $$ C_\widehat{u} $$ the actual and European Call option price at the up node respectively
- $$ C_d $$ and $$ C_\widehat{d} $$ the actual and European Call option price at the down node respectively
- $$ P_u $$ and $$ P_\widehat{u} $$ the actual and European Put option price at the up node respectively
- $$ P_d $$ and $$ P_\widehat{d} $$ the actual and European Put option price at the down node respectively

This results in the following binomial trees for Call and Put options, assuming the risk-free rate is 2%, dividend yield is 0.5%, volatility is 25%, the time to expiration is 1 year and the strike price is $90:

<div class="row">
<div markdown="1" class="fifty-column-left mobile-max-column-width">

**Call Option**

{% raw %}
<div class="mermaid">
flowchart TD;
classDef boxfont fill:#3b9cba,stroke-width:0px,fill-opacity:0.7,color:white,radius:20px;
classDef highlightfont fill:#d67f05,stroke-width:0px,fill-opacity:0.7,color:white,radius:20px;

Step0["$20.56"]:::highlightfont -- U --> Step1["$29.42"]:::boxfont
Step0["$20.56"] -- D --> Step2["$11.50"]:::highlightfont

Step1["$29.42"] -- U --> Step3["$45.13"]:::boxfont
Step1["$29.42"] -- D --> Step4["$13.11"]:::boxfont

Step2["$11.50"] -- U --> Step4["$13.11"]:::boxfont
Step2["$11.50"] -- D --> Step5["$10.00"]:::highlightfont

Step3["$45.13"] -- U --> Step6["$64.19"]:::boxfont
Step3["$45.13"] -- D --> Step7["$25.53"]:::boxfont

Step4["$13.11"] -- U --> Step7["$25.53"]:::boxfont
Step4["$13.11"] -- D --> Step8["$0.00"]:::boxfont

Step5["$10.00"] -- U --> Step8["$0.00"]:::boxfont
Step5["$10.00"] -- D --> Step9["$0.00"]:::boxfont
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
Step4["$13.75"] -- D --> Step8["$3.44"]:::boxfont

Step5["$13.75"] -- U --> Step8["$3.44"]:::boxfont
Step5["$13.75"] -- D --> Step9["$25.15"]:::boxfont

</div>
{% endraw %}

</div>
</div>

Given that the American option can be exercised at any time before expiration, the actual fair value of the option is higher than that of the European option when the option is in the money. This is because the option holder can exercise the option early and receive the intrinsic value of the option. As highlighted in the color <span style="color:#d67f05; font-weight:bold;">orange</span> in the binomial tree, the actual fair value of American the option is higher than that of the European option.

## Using the Finance Toolkit

The Finance Toolkit provides a function to calculate the binomial tree for both European and American options. You can install the Finance Toolkit by using the following command:

```bash
pip install financetoolkit -U
``` 

Let's start off with the actual model function, this function requires you to pass all inputs. Later on I'll show you how to work with actual company data.

{% include code_header.html %}
{% highlight python %}
from financetoolkit.options import binomial_trees_model

option_pay_off = binomial_trees_model.get_option_payoffs(
    stock_price=100,
    strike_price=90,
    years=1,
    timesteps=3,
    volatility=0.25,
    dividend_yield=0.005,
    risk_free_rate=0.02,
    put_option=False, # True for Put Option
    american_option=False # True for American Option
)
{% endhighlight %}

This returns the folowing  DataFrames for the European Call and Put options and the American Call and Put options respectively, which match up with binomial trees as mentioned above:

<div class="row">
<div markdown="1" class="fifty-column-left mobile-max-column-width">

**European Call Option**

|     |        0 |         1 |        2 |       3 |
|:----|---------:|----------:|---------:|--------:|
| UUU |  18.3183 |  29.4228  |  45.1286 | 64.1896 |
| UUD | nan      |   6.73261 |  13.1098 | 25.5274 |
| UDD | nan      | nan       |   0      |  0      |
| DDD | nan      | nan       | nan      |  0      |

<br>

**European Put Option**

|     |         0 |          1 |         2 |        3 |
|:----|----------:|-----------:|----------:|---------:|
| UUU |   3.92378 |   0.781139 |   0       |  0       |
| UUD | nan       |   7.39281  |   1.63935 |  0       |
| UDD | nan       | nan        |  13.7482  |  3.44045 |
| DDD | nan       | nan        | nan       | 25.1448  |

</div>

<div markdown="1" class="fifty-column-right mobile-max-column-width">

**American Call Option**

|     |        0 |        1 |        2 |       3 |
|:----|---------:|---------:|---------:|--------:|
| UUU |  20.5888 |  29.4228 |  45.1286 | 64.1896 |
| UUD | nan      |  11.4975 |  13.1098 | 25.5274 |
| UDD | nan      | nan      |  10      |  0      |
| DDD | nan      | nan      | nan      |  0      |

<br>

**American Put Option**

|     |         0 |          1 |         2 |        3 |
|:----|----------:|-----------:|----------:|---------:|
| UUU |   3.92378 |   0.781139 |   0       |  0       |
| UUD | nan       |   7.39281  |   1.63935 |  0       |
| UDD | nan       | nan        |  13.7482  |  3.44045 |
| DDD | nan       | nan        | nan       | 25.1448  |

</div>
</div>

Now let's work with actual company data, for this example I'll use the stock price of Apple Inc. (AAPL) and Microsoft Corporation (MSFT). Here, all required inputs will be collected automatically such as the risk-free rate, dividend yield and volatility.

{% include code_header.html %}
{% highlight python %}
from financetoolkit import Toolkit

companies = Toolkit(["AAPL", "MSFT"], api_key="FINANCIAL_MODELING_PREP_KEY")

# Obtain the Binominal Model with Time to Expiration of 16 Days
companies.options.get_binomial_model(show_input_info=True, time_to_expiration=16/365)
{% endhighlight %}

This returns insights into each component of the binomial tree model through the `show_input_info=True` parameter, which is useful for understanding the model's inputs and outputs. The output will look like this (with the 8th of February 2024 as starting date):

```plaintext
Based on the period 2013-02-11 to 2024-02-07 the following parameters were used:
Stock Price: AAPL (189.41), MSFT (414.05), Benchmark (498.1)
Volatility: AAPL (28.26%), MSFT (26.99%), Benchmark (17.46%)
Dividend Yield: AAPL (0.49%), MSFT (0.74%)
Up Movement: AAPL (101.89%), MSFT (101.8%)
Down Movement: AAPL (98.15%), MSFT (98.23%)
Risk Neutral Probability: AAPL (49.96%), MSFT (49.97%)
Risk Free Rate: 4.11%
```

The model itself calculates the binominal tree for a range of Strike Prices based on the stock price of the company. By default it takes all Strike Prices between 75% and 125% of the stock price in steps of 5. The output for Apple with a Strike Price of $190 will look like this:

| Movement   |   2024-02-07 |   2024-02-08 |   2024-02-10 |   2024-02-11 |   2024-02-13 |   2024-02-15 |   2024-02-16 |   2024-02-18 |   2024-02-19 |   2024-02-21 |   2024-02-23 |
|:-----------|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|
| UUUUUUUUUU |       <span style="color:#3b9cba; font-weight:bold;">4.32</span> |       6.10 |       8.39 |      11.22 |      14.51 |      18.18 |      22.05 |      26.02 |      30.06 |      34.18   |      38.38 |
| UUUUUUUUUD |     nan      |       2.53 |       3.80  |       5.57 |       7.91 |      10.85 |      14.31 |      18.09 |      21.98 |      25.94 |      29.98 |
| UUUUUUUUDD |     nan      |     nan      |       1.26 |       2.03 |       3.22 |       4.97 |       7.39 |      10.53 |      14.20 |      18.02  |      21.91 |
| UUUUUUUDDD |     nan      |     nan      |     nan      |       0.47 |       0.84 |       1.48 |       2.54 |       4.257  |       6.85 |      10.38 |      14.13  |
| UUUUUUDDDD |     nan      |     nan      |     nan      |     nan      |       0.10  |       0.21 |       0.42 |       0.83 |       1.66 |       3.32 |       6.63 |
| UUUUUDDDDD |     nan      |     nan      |     nan      |     nan      |     nan      |       0      |       0      |       0      |       0      |       0      |       0      |
| UUUUDDDDDD |     nan      |     nan      |     nan      |     nan      |     nan      |     nan      |       0      |       0      |       0      |       0      |       0      |
| UUUDDDDDDD |     nan      |     nan      |     nan      |     nan      |     nan      |     nan      |     nan      |       0      |       0      |       0      |       0      |
| UUDDDDDDDD |     nan      |     nan      |     nan      |     nan      |     nan      |     nan      |     nan      |     nan      |       0      |       0      |       0      |
| UDDDDDDDDD |     nan      |     nan      |     nan      |     nan      |     nan      |     nan      |     nan      |     nan      |     nan      |       0      |       0      |
| DDDDDDDDDD |     nan      |     nan      |     nan      |     nan      |     nan      |     nan      |     nan      |     nan      |     nan      |     nan      |       0      |

This represents a binominal tree for a Call Option with a Strike Price of $190 for Apple Inc. (AAPL) with a time to expiration of 16 days (23th of February, 2024) and 10 time steps. The actual fair value of the option is $4.32.

With this fair value calculation in hand, it is then possible to compare this to the actual option prices by looking at the options chains of the company. This can be done by using the `get_option_chains` method of the `options` module. Here, the time to expiration is set to `2024-02-23` which reflects the same timeframe as that of the binominal tree as shown above.

{% include code_header.html %}
{% highlight python %}

companies.options.get_option_chains(expiration_date="2024-02-23")
{% endhighlight %}

Then, Apple is selected to return the following selection of option prices (shrunken down to view the most relevant rows). Here, you can spot the actual option price for the Call Option with a Strike Price of $190:

|   Strike Price | Contract Symbol     | Currency   |   Last Price |   Change |   Percent Change |   Open Interest |   Bid |   Ask | Expiration   | Last Trade Date   |   Implied Volatility | In The Money   |   Volume |
|---------------:|:--------------------|:-----------|-------------:|---------:|-----------------:|----------------:|------:|------:|:-------------|:------------------|---------------------:|:---------------|---------:|
|            180 | AAPL240223C00180000 | USD        |        10    |        0 |                0 |             947 |     0 |     0 | 2024-02-23   | 2024-02-07        |               0      | True           |      263 |
|            185 | AAPL240223C00185000 | USD        |         5.75 |        0 |                0 |            4128 |     0 |     0 | 2024-02-23   | 2024-02-07        |               0      | True           |      449 |
|            190 | AAPL240223C00190000 | USD        |         <span style="color:#3b9cba; font-weight:bold;">2.67</span> |        0 |                0 |            8817 |     0 |     0 | 2024-02-23   | 2024-02-07        |               0.0039 | False          |     5594 |
|            195 | AAPL240223C00195000 | USD        |         0.95 |        0 |                0 |            7124 |     0 |     0 | 2024-02-23   | 2024-02-07        |               0.0313 | False          |     4149 |
|            200 | AAPL240223C00200000 | USD        |         0.34 |        0 |                0 |           17056 |     0 |     0 | 2024-02-23   | 2024-02-07        |               0.0625 | False          |     2927 |

As is visible, based on the binominal trees model, the actual fair value of the option is $4.32, while the actual option price is $2.67. This means that the option is undervalued, which could mean that the option could converge to its fair value in the future. This is a useful insight for investors who are looking to capitalize on fair value discrepancies in the options market.

As a bonus, it is also possible to use the Black Scholes model to perform these calculations. This can be done by using the `get_black_scholes_model` method of the `options` module. Here, the time to expiration is set to `2024-02-23` which reflects the same timeframe as that of the binominal tree as shown above.

{% include code_header.html %}
{% highlight python %}

companies.options.get_black_scholes_model(expiration_time_range=20)

{% endhighlight %}

When selecting for Apple Inc. (AAPL) the following output is returned (shrunken down to view the most relevant rows):

|   Strike Price |   2024-02-20 |   2024-02-21 |   2024-02-22 |   2024-02-23 |   2024-02-24 |   2024-02-25 |   2024-02-26 |
|---------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|
|            180 |        10.49 |        10.6  |        10.71 |        10.81 |        10.92 |        11.02 |        11.13 |
|            185 |         6.73 |         6.87 |         7.02 |         7.16 |         7.29 |         7.43 |         7.56 |
|            190 |         3.86 |         4.02 |         4.18 |         <span style="color:#3b9cba; font-weight:bold;">4.33</span> |         4.48 |         4.62 |         4.76 |
|            195 |         1.96 |         2.1  |         2.24 |         2.37 |         2.5  |         2.63 |         2.76 |
|            200 |         0.87 |         0.97 |         1.07 |         1.17 |         1.27 |         1.37 |         1.47 |

As you can see, both the Binomial Trees and Black Scholes model point to a similar fair value of the option, with the Binomial Tree returning a fair value of $4.32 and the Black Scholes model returning a fair value of $4.33.

{: .notice--info}
**Statistical Option Arbitrage**<br>
The method of evaluating the option price via the Binomial Tree or Black Scholes model and trading on the deviations based on the actual option prices is an actual method used within the financial industry and refers to the concept of "Statistical Option Arbitrage". For example see the article titled "*Statistical Arbitrage in the Black-Scholes Framework*" in the Journal of Financial and Quantitative Analysis ([here](https://www.researchgate.net/publication/263352435_Statistical_Arbitrage_in_the_Black-Scholes_Framework){:target="_blank"}) which proves the existence of statistical arbitrage opportunities in the Black-Scholes framework by considering trading strategies that consists of borrowing from the risk free rate and taking a long position in the stock until it hits a deterministic barrier level.

Did you find this article helpful? If you have any questions or suggestions, feel free to reach out to me via any of the links on the side.