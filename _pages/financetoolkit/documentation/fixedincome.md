---
title: Fixed Income
excerpt: The Fixed Income module contains a wide variety of fixed income related calculations such as the Effective Yield, the Macaulay Duration, the Modified Duration Convexity, the Yield to Maturity and models such as Black and Bachelier to valuate derivative instruments such as Swaptions. 
description: The Fixed Income module contains a wide variety of fixed income related calculations such as the Effective Yield, the Macaulay Duration, the Modified Duration Convexity, the Yield to Maturity and models such as Black and Bachelier to valuate derivative instruments such as Swaptions. 
author_profile: false
permalink: /projects/financetoolkit/docs/fixedincome
classes: wide-sidebar
layout: single
redirect_from:
    - /fixedincome
sidebar:
    nav: "financetoolkit-docs-fixedincome"
---

The Fixed Income module contains a wide variety of fixed income related calculations such as the Effective Yield, the Macaulay Duration, the Modified Duration Convexity, the Yield to Maturity and models such as Black and Bachelier to valuate derivative instruments such as Swaptions. 

To install the FinanceToolkit it simply requires the following:

{% include code_header.html %}
{% highlight bash %}
pip install financetoolkit -U
{% endhighlight %}

If you are looking for documentation regarding the toolkit, discovery, ratios, models, technicals, risk, performance and economics, please have a look below:

<div style="display: flex; justify-content: space-between;" class="show-on-desktop">
    <a href="/projects/financetoolkit/docs" class="btn btn--info" style="flex: 1;font-size:10px;margin-right:5px">Toolkit</a>
    <a href="/projects/financetoolkit/docs/discovery" class="btn btn--info" style="flex: 1;font-size:10px;margin-right:5px">Discovery</a>
    <a href="/projects/financetoolkit/docs/ratios" class="btn btn--info" style="flex: 1;font-size:10px;margin-right:5px">Ratios</a>
    <a href="/projects/financetoolkit/docs/models" class="btn btn--info" style="flex: 1;font-size:10px;margin-right:5px">Models</a>
    <a href="/projects/financetoolkit/docs/options" class="btn btn--info" style="flex: 1;font-size:10px;margin-right:5px">Options</a>
    <a href="/projects/financetoolkit/docs/technicals" class="btn btn--info" style="flex: 1;font-size:10px;margin-right:5px">Technicals</a>
    <a href="/projects/financetoolkit/docs/fixedincome" class="btn btn--warning" style="flex: 1;font-size:10px;margin-right:5px">Fixed Income</a>
    <a href="/projects/financetoolkit/docs/risk" class="btn btn--info" style="flex: 1;font-size:10px;margin-right:5px">Risk</a>
    <a href="/projects/financetoolkit/docs/performance" class="btn btn--info" style="flex: 1;font-size:10px;margin-right:5px">Performance</a>
    <a href="/projects/financetoolkit/docs/economics" class="btn btn--info" style="flex: 1;font-size:10px; ">Economics</a>
</div>

{% include algolia.html %}

## __init__
Initializes the Fixed Income Controller Class.

**Args:**
 - <u>start_date (str | None, optional):</u> The start date to retrieve data from. Defaults to None.
 - <u>end_date (str | None, optional):</u> The end date to retrieve data from. Defaults to None.
 - <u>quarterly (bool, optional):</u> Whether to return the data quarterly. Defaults to True.
 - <u>rounding (int | None, optional):</u> The number of decimals to round the results to. Defaults to None.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import FixedIncome

fixedincome = FixedIncome(
start_date='2024-01-01',
end_date='2024-01-15',
)

fixedincome.get_ice_bofa_effective_yield(maturity=False)
{% endhighlight %}


Which returns:

| Date | AAA | AA | A | BBB | BB | B | CCC |
 |:-----------|-------:|-------:|-------:|-------:|-------:|-------:|-------:|
 | 2024-01-01 | 0.0456 | 0.047 | 0.0505 | 0.054 | 0.0613 | 0.0752 | 0.1319 |
 | 2024-01-02 | 0.0459 | 0.0473 | 0.0509 | 0.0543 | 0.0622 | 0.0763 | 0.1333 |
 | 2024-01-03 | 0.0459 | 0.0474 | 0.051 | 0.0544 | 0.0634 | 0.0779 | 0.1358 |
 | 2024-01-04 | 0.0466 | 0.0481 | 0.0518 | 0.0551 | 0.0639 | 0.0784 | 0.1367 |
 | 2024-01-05 | 0.047 | 0.0485 | 0.0521 | 0.0554 | 0.0641 | 0.0787 | 0.137 |
 | 2024-01-08 | 0.0465 | 0.0481 | 0.0517 | 0.055 | 0.0633 | 0.0776 | 0.1365 |
 | 2024-01-09 | 0.0464 | 0.048 | 0.0516 | 0.0548 | 0.0629 | 0.0771 | 0.1359 |
 | 2024-01-10 | 0.0464 | 0.048 | 0.0515 | 0.0547 | 0.0622 | 0.0762 | 0.1351 |
 | 2024-01-11 | 0.0456 | 0.0472 | 0.0507 | 0.054 | 0.0619 | 0.076 | 0.1344 |
 | 2024-01-12 | 0.0451 | 0.0467 | 0.0502 | 0.0534 | 0.0613 | 0.0753 | 0.1338 |
 | 2024-01-15 | 0.0451 | 0.0467 | 0.0501 | 0.0533 | 0.0611 | 0.0751 | 0.1328 |

## collect_bond_statistics
Collect the bond statistics for a given bond which includes the following fields:


- Par Value: The face value of the bond. 
- Coupon Rate: The annual coupon rate (in decimal). 
- Years to Maturity: The number of years until the bond matures. 
- Yield to Maturity: The yield to maturity of the bond (in decimal). 
- Frequency: The number of coupon payments per year. 
- Present Value: The present value of the bond. 
- Current Yield: The annual coupon payment divided by the bond price. 
- Macaulay's Duration: The weighted average time to receive the bond's cash flows. 
- Modified Duration: The Macaulay's duration divided by 1 plus the yield to maturity. 
- Effective Duration: The percentage change in the bond price for a 1% change in the yield to maturity. 
- Dollar Duration: The modified duration multiplied by the bond price. 
- DV01: The dollar value of a 0.01% change in yield to maturity. 
- Convexity: The second derivative of the bond price with respect to the yield to maturity.

These statistics can be used to evaluate the bond's performance as opposed to other bonds or to estimate the bond's sensitivity to changes in interest rates to be able to apply a hedging strategy.

**Args:**
 - <u>par_value (float):</u> The face value of the bond. Defaults to 100.
 - <u>coupon_rate (float):</u> The annual coupon rate (in decimal). Defaults to 0.05.
 - <u>years_to_maturity (int):</u> The number of years until the bond matures. Defaults to 5.
 - <u>yield_to_maturity (float):</u> The yield to maturity of the bond (in decimal). Defaults to 0.08.
 - <u>frequency (int):</u> The number of coupon payments per year. Defaults to 1.
 - <u>show_input_info (bool, optional):</u> Whether to display input information. Defaults to True.

 **Returns:**
 pd.Series: A pandas Series containing the bond statistics.
## get_present_value
Calculates the bond prices for different coupon rates and years to maturity. The bond price is the present value of the bond's future cash flows, which includes the coupon payments and the par value of the bond at maturity. The bond price is calculated using the following formula:


- Bond Price = (C / r) * (1 - (1 + r)^
-n) + F / (1 + r)^n

where:


- C = Coupon payment per period 
- r = Yield to maturity per period 
- n = Number of periods 
- F = Face value of the bond

The bond price is used to determine the fair value of the bond and to compare the bond's price to its market price to determine if the bond is overvalued or undervalued.

**Args:**
 - <u>par_value (float):</u> The par value (face value) of the bond.
 - <u>coupon_rate (float, optional):</u> The coupon rate of the bond. If not provided, a range of coupon rates will be used.
 - <u>years_to_maturity (float, optional):</u> The years to maturity of the bond in years. If not provided, a range of years to maturity will be used.
 - <u>yield_to_maturity (float, optional):</u> The yield to maturity of the bond. If not provided, a default value of 0.05 will be used.
 - <u>frequency (int, optional):</u> The frequency of coupon payments per year. Defaults to 1.
 - <u>show_input_info (bool, optional):</u> Whether to display input information. Defaults to True.

 **Returns:**
 pandas.DataFrame: A DataFrame containing the bond prices for different coupon rates and years to maturity.
## get_duration
Calculates the bond duration for different coupon rates and years to maturity. It has the option to calculate the following type of bond durations:


- Macaulay's Duration: The weighted average time to receive the bond's cash flows. 
- Modified Duration: The Macaulay's duration divided by 1 plus the yield to maturity. 
- Effective Duration: The percentage change in the bond price for a 1% change in the yield to maturity. 
- Dollar Duration: The modified duration multiplied by the bond price.

These duration measures can be used to estimate the sensitivity of a bond's price to changes in interest rates as well as to compare the risk of different bonds. The modified duration is particularly useful for estimating the percentage change in the bond price for a 1% change in the yield to maturity. This is also known as the bond's price value of a basis point (PVBP), or the bond's dollar duration (DD) or dollar value of a .01% change (DV01).

**Args:**
 - <u>duration_type (str, optional):</u> The type of duration to calculate. Defaults to 'modified' but can also
 be 'macaulay', 'effective' or 'dollar'.
 - <u>par_value (float, optional):</u> The par value (face value) of the bond. Defaults to None.
 - <u>coupon_rate (float, optional):</u> The coupon rate of the bond. If not provided, a range of coupon
 rates will be used. Defaults to None.
 - <u>years_to_maturity (float, optional):</u> The years to maturity of the bond in years. If not provided, a range of years
 to maturity will be used. Defaults to None.
 - <u>yield_to_maturity (float, optional):</u> The yield to maturity of the bond. If not provided, a default
 value of 0.05 will be used. Defaults to None.
 - <u>frequency (int, optional):</u> The frequency of coupon payments per year. Defaults to 1.
 - <u>show_input_info (bool, optional):</u> Whether to display input information. Defaults to True.

 **Returns:**
 pandas.DataFrame: A DataFrame containing the bond duration for different coupon rates and years to maturity.
## get_yield_to_maturity
Calculates the yield to maturity for a bond. The yield to maturity is the internal rate of return of the bond, which is the discount rate that equates the present value of the bond's cash flows to its market price. The yield to maturity is used to estimate the bond's return and to compare the bond's return to other investments.

The yield to maturity is calculated using the following formula:


- Bond Price = (C / r) * (1 - (1 + r)^
-n) + F / (1 + r)^n

where:


- C = Coupon payment per period 
- r = Yield to maturity per period 
- n = Number of periods 
- F = Face value of the bond

The goal is to find the yield to maturity that satisfies the equation above. This is done using the Newton
-Raphson method which is an iterative method that converges to the root of a function.

**Args:**
 - <u>par_value (float):</u> The par value (face value) of the bond. This is the original price when it was issued by the issuer.
 - <u>coupon_rate (float, optional):</u> The coupon rate of the bond. Defaults to None.
 - <u>years_to_maturity (float, optional):</u> The years to maturity of the bond in years. Defaults to None.
 - <u>bond_price (float, optional):</u> The price of the bond. Defaults to None.
 - <u>frequency (int, optional):</u> The number of coupon payments per year. Defaults to 1.
 - <u>guess (float, optional):</u> The initial guess for the yield to maturity. Defaults to 0.05.
 - <u>tolerance (float, optional):</u> The tolerance level for convergence. Defaults to 0.0001.
 - <u>max_iterations (int, optional):</u> The maximum number of iterations for convergence. Defaults to 100.
 - <u>show_input_info (bool, optional):</u> Whether to display input information. Defaults to True.

 **Returns:**
 pandas.DataFrame: A DataFrame containing the yield to maturity for different bond prices and years to maturity.
## get_derivative_price
Calculates the derivative price for a fixed income instrument.

It is possible to use two different models to calculate the derivative price:


- Black Model: A mathematical model used for pricing financial derivatives, its primary applications are for pricing options on future contracts, bond options, interest rate cap and floors, and swaptions. For more information, see: [https://en.wikipedia.org/wiki/Black_model](https://en.wikipedia.org/wiki/Black_model){:target="_blank"} 
- Bachelier Model: A deviation of the Black Model that is used for pricing future contracts. It is a simple model that assumes the price of the underlying asset follows a normal distribution with constant volatility. This is in contrast to the Black Model which assumes the price of the underlying asset follows a log
-normal distribution. For more information, see: [https://en.wikipedia.org/wiki/Bachelier_model](https://en.wikipedia.org/wiki/Bachelier_model){:target="_blank"}

It is possible to alter all parameters within the models, e.g. strike rate, volatility, years to maturity, risk
-free rate, notional amount, and whether the holder is the receiver or payer of the derivative. Next to that, you can provide lists of values for the fixed rate, strike rate, volatility, and years to maturity to calculate the derivative price for multiple scenarios outside of the standard sample.

**Args:**
 - <u>model (str, optional):</u> The type of model to use for calculating the derivative price. Defaults to "black".
 - <u>forward_rate (float, optional):</u> The forward rate as derived from the swap curve. Defaults to None.
 - <u>strike_rate (float | list, optional):</u> The strike rate for the derivative. Defaults to None which means it calculates the
 derivative price a range of strike prices. Can also be a list of strike rates (e.g. [0.01, 0.02, 0.03, 0.04, 0.05]).
 - <u>volatility (float, optional):</u> The volatility of the underlying asset. Defaults to None.
 - <u>years_to_maturity (float | list, optional):</u> The years to maturity of the derivative in years. Defaults to None which means it plots
 the derivative price for the next 10 years. Can also be a list of years to maturity (e.g. [1, 2.3, 2.5, 3])
 - <u>risk_free_rate (float, optional):</u> The risk-free interest rate. Defaults to None which means it is equal to the fixed rate.
 - <u>notional (float, optional):</u> The notional amount of the derivative. Defaults to 10_000_000.
 - <u>is_receiver (bool, optional):</u> True if the holder is the receiver of the derivative, False if the holder is the payer. Defaults to True.
 - <u>include_payoff (bool, optional):</u> True to include the payoff in the output, False otherwise. Defaults to False.
 - <u>show_input_info (bool, optional):</u> True to display input information, False otherwise. Defaults to True.

 **Returns:**
 pandas.DataFrame: The Black derivative prices rounded to the specified decimal places.
 pandas.- <u>DataFrame (optional):</u> The Black derivative payoffs rounded to the specified decimal places if include_payoff is True.

 For example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import FixedIncome

fixedincome = FixedIncome()

# You can also provide lists of values for the strike rate and years to maturity
# to define your own strike rates and years to maturity to display in the DataFrame
fixedincome.get_derivative_price(model_type='black', forward_rate=0.0325)
{% endhighlight %}


Which returns:

| Strike Rate | 2025-04-21 | 2026-04-21 | 2027-04-21 | 2028-04-20 | 2029-04-20 | 2030-04-20 | 2031-04-20 | 2032-04-19 | 2033-04-19 | 2034-04-19 |
 |--------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|
 | 0.005 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
 | 0.01 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
 | 0.015 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
 | 0.02 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
 | 0.025 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
 | 0.03 | 0 | 0 | 0 | 0.04 | 0.25 | 0.9 | 2.3 | 4.68 | 8.22 | 12.98 |
 | 0.035 | 24200.6 | 23426.7 | 22677.6 | 21952.5 | 21251.2 | 20573.2 | 19918.5 | 19286.4 | 18676.5 | 18088 |
 | 0.04 | 72601.7 | 70280.1 | 68032.7 | 65857.2 | 63751.2 | 61712.6 | 59739.2 | 57828.9 | 55979.6 | 54189.6 |
 | 0.045 | 121003 | 117133 | 113388 | 109762 | 106252 | 102854 | 99565.3 | 96381.4 | 93299.4 | 90315.9 |
 | 0.05 | 169404 | 163987 | 158743 | 153667 | 148753 | 143996 | 139391 | 134934 | 130619 | 126442 |
 | 0.055 | 217805 | 210840 | 204098 | 197571 | 191254 | 185138 | 179218 | 173487 | 167939 | 162569 |
 | 0.06 | 266206 | 257694 | 249453 | 241476 | 233754 | 226280 | 219044 | 212039 | 205259 | 198695 |
 | 0.065 | 314607 | 304547 | 294808 | 285381 | 276255 | 267421 | 258870 | 250592 | 242578 | 234821 |
 | 0.07 | 363008 | 351400 | 340163 | 329286 | 318756 | 308563 | 298696 | 289144 | 279898 | 270948 |
 | 0.075 | 411410 | 398254 | 385518 | 373191 | 361257 | 349705 | 338522 | 327697 | 317218 | 307074 |
 | 0.08 | 459811 | 445107 | 430874 | 417095 | 403758 | 390846 | 378348 | 366250 | 354538 | 343200 |
 | 0.085 | 508212 | 491960 | 476229 | 461000 | 446258 | 431988 | 418174 | 404802 | 391858 | 379327 |
 | 0.09 | 556613 | 538814 | 521584 | 504905 | 488759 | 473130 | 458000 | 443355 | 429177 | 415453 |
 | 0.095 | 605014 | 585667 | 566939 | 548810 | 531260 | 514272 | 497827 | 481907 | 466497 | 451580 |
 | 0.1 | 653415 | 632521 | 612294 | 592714 | 573761 | 555413 | 537653 | 520460 | 503817 | 487706 |
 | 0.105 | 701816 | 679374 | 657649 | 636619 | 616262 | 596555 | 577479 | 559012 | 541137 | 523832 |
 | 0.11 | 750217 | 726227 | 703004 | 680524 | 658762 | 637697 | 617305 | 597565 | 578456 | 559959 |
 | 0.115 | 798619 | 773081 | 748359 | 724429 | 701263 | 678839 | 657131 | 636118 | 615776 | 596085 |
 | 0.12 | 847020 | 819934 | 793715 | 768334 | 743764 | 719980 | 696957 | 674670 | 653096 | 632211 |
 | 0.125 | 895421 | 866787 | 839070 | 812238 | 786265 | 761122 | 736783 | 713223 | 690416 | 668338 |
 | 0.13 | 943822 | 913641 | 884425 | 856143 | 828766 | 802264 | 776609 | 751775 | 727735 | 704464 |

## get_government_bond_yield
Long
-term interest rates refer to government bonds maturing in ten years. Rates are mainly determined by the price charged by the lender, the risk from the borrower and the fall in the capital value. Long
-term interest rates are generally averages of daily rates, measured as a percentage. These interest rates are implied by the prices at which the government bonds are traded on financial markets, not the interest rates at which the loans were issued.

In all cases, they refer to bonds whose capital repayment is guaranteed by governments. Long
-term interest rates are one of the determinants of business investment. Low long term interest rates encourage investment in new equipment and high interest rates discourage it. Investment is, in turn, a major source of economic growth

See definition: [https://data.oecd.org/interest/long
-term
-interest
-rates.htm](https://data.oecd.org/interest/long
-term
-interest
-rates.htm){:target="_blank"}

Short
-term interest rates are the rates at which short
-term borrowings are effected between financial institutions or the rate at which short
-term government paper is issued or traded in the market. Short
-term interest rates are generally averages of daily rates, measured as a percentage.

Short
-term interest rates are based on three
-month money market rates where available. Typical standardised names are "money market rate" and "treasury bill rate".

See definition: [https://data.oecd.org/interest/short
-term
-interest
-rates.htm](https://data.oecd.org/interest/short
-term
-interest
-rates.htm){:target="_blank"}

**Args:**
 - <u>short_term (bool, optional):</u> Whether to return the short-term interest rate. Defaults to False.
 This means that the long-term interest rate will be returned.
 - <u>period (str | None, optional):</u> Whether to return the monthly, quarterly or the annual data.
 - <u>forecast (bool, optional):</u> Whether to return the forecasted data. Defaults to False.
 - <u>growth (bool, optional):</u> Whether to return the growth data or the actual data.
 - <u>lag (int, optional):</u> The number of periods to lag the data by.
 - <u>rounding (int | None, optional):</u> The number of decimals to round the results to. Defaults to None.

 **Returns:**
 pd.DataFrame: A DataFrame containing the Long Term Interest Rate.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import FixedIncome

fixedincome = FixedIncome(start_date='2023-05-01', end_date='2023-12-31')

long_term_interest_rate = fixedincome.get_government_bond_yield(short_term=False, period='monthly')

long_term_interest_rate.loc[:, ['Japan', 'United States', 'Brazil']]
{% endhighlight %}


Which returns:

| | Japan | United States | Brazil |
 |:--------|--------:|----------------:|---------:|
 | 2023-05 | 0.0043 | 0.0357 | 0.0728 |
 | 2023-06 | 0.004 | 0.0375 | 0.0728 |
 | 2023-07 | 0.0059 | 0.039 | 0.07 |
 | 2023-08 | 0.0064 | 0.0417 | 0.07 |
 | 2023-09 | 0.0076 | 0.0438 | 0.07 |
 | 2023-10 | 0.0095 | 0.048 | 0.0655 |
 | 2023-11 | 0.0066 | 0.045 | 0.0655 |

## get_european_central_bank_rates
The Governing Council of the ECB sets the key interest rates for the euro area. The available rates are:


- Main refinancing operations (refinancing) 
- Marginal lending facility (lending) 
- Deposit facility (deposit)

The main refinancing operations (MRO) rate is the interest rate banks pay when they borrow money from the ECB for one week. When they do this, they have to provide collateral to guarantee that the money will be paid back.

The marginal lending facility rate is the interest rate banks pay when they borrow from the ECB overnight. When they do this, they have to provide collateral, for example securities, to guarantee that the money will be paid back.

The deposit facility rate is one of the three interest rates the ECB sets every six weeks as part of its monetary policy. The rate defines the interest banks receive for depositing money with the central bank overnight.

See source: [https://data.ecb.europa.eu/main
-figures/](https://data.ecb.europa.eu/main
-figures/){:target="_blank"}

**Args:**
 - <u>rate (str, optional):</u> The rate to return. Defaults to None, which returns all rates.
 Choose between 'refinancing', 'lending' or 'deposit'.

 **Returns:**
 pd.DataFrame: A DataFrame containing the ECB rates.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import FixedIncome

fixedincome = FixedIncome(start_date='2023-12-01')

fixedincome.get_european_central_bank_rates()
{% endhighlight %}


Which returns:

| | Refinancing | Lending | Deposit |
 |:-----------|--------------:|----------:|----------:|
 | 2023-12-01 | 0.045 | 0.0475 | 0.04 |
 | 2023-12-02 | 0.045 | 0.0475 | 0.04 |
 | 2023-12-03 | 0.045 | 0.0475 | 0.04 |
 | 2023-12-04 | 0.045 | 0.0475 | 0.04 |
 | 2023-12-05 | 0.045 | 0.0475 | 0.04 |
 | 2023-12-06 | 0.045 | 0.0475 | 0.04 |
 | 2023-12-07 | 0.045 | 0.0475 | 0.04 |
 | 2023-12-08 | 0.045 | 0.0475 | 0.04 |
 | 2023-12-09 | 0.045 | 0.0475 | 0.04 |
 | 2023-12-10 | 0.045 | 0.0475 | 0.04 |
 | 2023-12-11 | 0.045 | 0.0475 | 0.04 |
 | 2023-12-12 | 0.045 | 0.0475 | 0.04 |
 | 2023-12-13 | 0.045 | 0.0475 | 0.04 |
 | 2023-12-14 | 0.045 | 0.0475 | 0.04 |
 | 2023-12-15 | 0.045 | 0.0475 | 0.04 |
 | 2023-12-16 | 0.045 | 0.0475 | 0.04 |
 | 2023-12-17 | 0.045 | 0.0475 | 0.04 |
 | 2023-12-18 | 0.045 | 0.0475 | 0.04 |

## get_federal_reserve_rates
Get the Federal Reserve rates as published by the Federal Reserve Bank of New York. The federal funds market consists of domestic unsecured borrowings in U.S. dollars by depository institutions from other depository institutions and certain other entities, primarily government
-sponsored enterprises.

The following rates are available:


- Effective Federal Funds Rate (EFFR) 
- Overnight Bank Funding Rate (OBFR) 
- Tri
-Party General Collateral Rate (TGCR) 
- Broad General Collateral Rate (BGCR) 
- Secured Overnight Financing Rate (SOFR)

The effective federal funds rate (EFFR) is calculated as a volume
-weighted median of overnight federal funds transactions reported in the FR 2420 Report of Selected Money Market Rates.

The overnight bank funding rate (OBFR) is calculated as a volume
-weighted median of overnight federal funds transactions, Eurodollar transactions, and the domestic deposits reported as “Selected Deposits” in the FR 2420 Report.

The TGCR is calculated as a volume
-weighted median of transaction
-level tri
-party repo data collected from the Bank of New York Mellon.

The BGCR is calculated as a volume
-weighted median of transaction
-level tri
-party repo data collected from the Bank of New York Mellon as well as GCF Repo transaction data obtained from the U.S. Department of the Treasury’s Office of Financial Research (OFR).

The SOFR is calculated as a volume
-weighted median of transaction
-level tri
-party repo data collected from the Bank of New York Mellon as well as GCF Repo transaction data and data on bilateral Treasury repo transactions cleared through FICC's DVP service, which are obtained from the U.S. Department of the Treasury’s Office of Financial Research (OFR).

The New York Fed publishes the rates for the prior business day on the New York Fed’s website between 8:00 and 9:00 a.m.

See source: [https://www.newyorkfed.org/markets/reference
-rates/](https://www.newyorkfed.org/markets/reference
-rates/){:target="_blank"}

**Args:**
 - <u>rate (str):</u> The rate to return. Defaults to 'EFFR' (Effective Federal Funds Rate).

 **Returns:**
 pd.DataFrame: A DataFrame containing the Federal Reserve rates including the rate,
 percentiles, volume and upper and lower bounds.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import FixedIncome

fixedincome = FixedIncome(start_date='2023-12-01')

effr = fixedincome.get_federal_reserve_rates()

effr.loc[:, ['Rate', '1st Percentile', '25th Percentile', '75th Percentile', '99th Percentile']]
{% endhighlight %}


Which returns:

| Effective Date | Rate | 1st Percentile | 25th Percentile | 75th Percentile | 99th Percentile |
 |:-----------------|-------:|-----------------:|------------------:|------------------:|------------------:|
 | 2023-12-01 | 0.0533 | 0.053 | 0.0532 | 0.0533 | 0.0544 |
 | 2023-12-04 | 0.0533 | 0.053 | 0.0532 | 0.0533 | 0.0545 |
 | 2023-12-05 | 0.0533 | 0.053 | 0.0532 | 0.0533 | 0.0545 |
 | 2023-12-06 | 0.0533 | 0.053 | 0.0532 | 0.0533 | 0.0545 |
 | 2023-12-07 | 0.0533 | 0.053 | 0.0531 | 0.0534 | 0.0545 |
 | 2023-12-08 | 0.0533 | 0.053 | 0.0532 | 0.0533 | 0.0545 |
 | 2023-12-11 | 0.0533 | 0.053 | 0.0532 | 0.0533 | 0.0545 |
 | 2023-12-12 | 0.0533 | 0.053 | 0.0531 | 0.0533 | 0.0544 |
 | 2023-12-13 | 0.0533 | 0.053 | 0.0531 | 0.0533 | 0.0545 |
 | 2023-12-14 | 0.0533 | 0.053 | 0.0531 | 0.0533 | 0.0535 |

## get_euribor_rates
Euribor rates, short for Euro Interbank Offered Rate, are the interest rates at which a panel of European banks lend funds to one another in the interbank market. These rates are published daily by the European Money Markets Institute (EMMI) and serve as a benchmark for various financial products and contracts, including mortgages, loans, and derivatives, across the Eurozone.

The Euribor rates are determined for different maturities, typically ranging from overnight to 12 months The most common maturities are 1 month, 3 months, 6 months, and 12 months. Each maturity represents the time period for which the funds are borrowed, with longer maturities generally implying higher interest rates due to increased uncertainty and risk over longer time horizons.

For more information, see for example: [https://data.ecb.europa.eu/data/datasets/FM/FM.M.U2.EUR.RT.MM.EURIBOR6MD_.HSTA](https://data.ecb.europa.eu/data/datasets/FM/FM.M.U2.EUR.RT.MM.EURIBOR6MD_.HSTA){:target="_blank"}

**Args:**
 - <u>maturities (str | list | None, optional):</u> Maturities for which to retrieve rates. Defaults to None.
 When set to None, it will retrieve rates for 1 month, 3 months, 6 months, and 12 months.
 - <u>nominal (bool, optional):</u> Flag indicating whether to retrieve nominal rates. Defaults to True.
 - <u>rounding (int | None, optional):</u> Rounding precision for the rates. Defaults to None.

 **Returns:**
 pandas.DataFrame: DataFrame containing the Euribor rates for the specified maturities.

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import FixedIncome

fixedincome = FixedIncome(start_date='2023-12-01')

euribor_rates = fixedincome.get_euribor_rates()
{% endhighlight %}


Which returns:

| | 1-Month | 3-Month | 6-Month | 12-Month |
 |:--------|----------:|----------:|----------:|-----------:|
 | 2023-12 | 0.0386 | 0.0393 | 0.0392 | 0.0367 |
 | 2024-01 | 0.0387 | 0.0393 | 0.0389 | 0.0361 |
 | 2024-02 | 0.0387 | 0.0392 | 0.039 | 0.0367 |
 | 2024-03 | 0.0385 | 0.0392 | 0.0389 | 0.0372 |

## get_ice_bofa_option_adjusted_spread
The ICE BofA Option
-Adjusted Spreads (OASs) are the calculated spreads between a computed OAS index of all bonds in a given maturity and rating category and a spot Treasury curve. An OAS index is constructed using each constituent bond's OAS, weighted by market capitalization.

The Option
-Adjusted Spread (OAS) is the spread relative to a risk
-free interest rate, usually measured in basis points (bp), that equates the theoretical present value of a series of uncertain cash flows to the market price of a fixed
-income investment. The spread is added to the risk
-free rate to compensate for the uncertainty of the cash flows.

See definitions:


- Ratings: [https://fred.stlouisfed.org/series/BAMLC0A4CBBB](https://fred.stlouisfed.org/series/BAMLC0A4CBBB){:target="_blank"} 
- Maturity: [https://fred.stlouisfed.org/series/BAMLC1A0C13Y](https://fred.stlouisfed.org/series/BAMLC1A0C13Y){:target="_blank"}

**Args:**
 - <u>maturity (bool, optional):</u> Whether to return the maturity option adjusted spread or the rating option adjusted spread.
 - <u>rounding (int | None, optional):</u> The number of decimals to round the results to. Defaults to None.

 **Returns:**
 pd.DataFrame: A DataFrame containing the Option Adjusted Spread

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import FixedIncome

fixedincome = FixedIncome(
start_date='2024-01-01',
end_date='2024-01-15',
)

fixedincome.get_option_adjusted_spread()
{% endhighlight %}


Which returns:

| Date | 1-3 Years | 3-5 Years | 5-7 Years | 7-10 Years | 10-15 Years | 15+ Years |
 |:-----------|------------:|------------:|------------:|-------------:|--------------:|------------:|
 | 2024-01-01 | 77 | 94 | 108.5 | 127 | 131.5 | 118 |
 | 2024-01-02 | 78 | 95 | 109 | 128 | 133 | 119 |
 | 2024-01-03 | 80 | 98 | 113 | 133 | 136 | 122 |
 | 2024-01-04 | 80 | 98 | 112 | 133 | 135 | 122 |
 | 2024-01-05 | 80 | 98 | 112 | 132 | 134 | 121 |
 | 2024-01-08 | 79 | 98 | 112 | 132 | 134 | 120 |
 | 2024-01-09 | 78 | 96 | 110 | 130 | 131 | 117 |
 | 2024-01-10 | 77 | 94 | 108 | 128 | 128 | 113 |
 | 2024-01-11 | 75 | 94 | 107 | 128 | 127 | 113 |
 | 2024-01-12 | 74 | 94 | 107 | 128 | 126 | 112 |
 | 2024-01-15 | 74 | 94 | 107 | 128 | 125 | 111 |

## get_ice_bofa_effective_yield
This data represents the effective yield of the ICE BofA Indices, When the last calendar day of the month takes place on the weekend, weekend observations will occur as a result of month ending accrued interest adjustments.

The Effective Yield is the yield of a bond, calculated by dividing the bond's coupon payments by its market price. The effective yield is not the same as the stated yield, which is the yield on the bond's coupon payments divided by the bond's principal value. The effective yield is a more accurate measure of a bond's return, as it takes into account the fact that the investor will not hold the bond to maturity and will likely sell it before it matures.

See definitions:


- Ratings: [https://fred.stlouisfed.org/series/BAMLC0A4CBBBEY](https://fred.stlouisfed.org/series/BAMLC0A4CBBBEY){:target="_blank"} 
- Maturity: [https://fred.stlouisfed.org/series/BAMLC1A0C13YEY](https://fred.stlouisfed.org/series/BAMLC1A0C13YEY){:target="_blank"}

**Args:**
 - <u>maturity (bool, optional):</u> Whether to return the maturity effective yield or the rating effective yield.
 - <u>rounding (int | None, optional):</u> The number of decimals to round the results to. Defaults to None.

 **Returns:**
 pd.DataFrame: A DataFrame containing the Gross Domestic Product

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import FixedIncome

fixedincome = FixedIncome(
start_date='2024-01-01',
end_date='2024-01-15',
)

fixedincome.get_effective_yield(maturity=False)
{% endhighlight %}


Which returns:

| Date | AAA | AA | A | BBB | BB | B | CCC |
 |:-----------|-------:|-------:|-------:|-------:|-------:|-------:|-------:|
 | 2024-01-01 | 0.0456 | 0.047 | 0.0505 | 0.054 | 0.0613 | 0.0752 | 0.1319 |
 | 2024-01-02 | 0.0459 | 0.0473 | 0.0509 | 0.0543 | 0.0622 | 0.0763 | 0.1333 |
 | 2024-01-03 | 0.0459 | 0.0474 | 0.051 | 0.0544 | 0.0634 | 0.0779 | 0.1358 |
 | 2024-01-04 | 0.0466 | 0.0481 | 0.0518 | 0.0551 | 0.0639 | 0.0784 | 0.1367 |
 | 2024-01-05 | 0.047 | 0.0485 | 0.0521 | 0.0554 | 0.0641 | 0.0787 | 0.137 |
 | 2024-01-08 | 0.0465 | 0.0481 | 0.0517 | 0.055 | 0.0633 | 0.0776 | 0.1365 |
 | 2024-01-09 | 0.0464 | 0.048 | 0.0516 | 0.0548 | 0.0629 | 0.0771 | 0.1359 |
 | 2024-01-10 | 0.0464 | 0.048 | 0.0515 | 0.0547 | 0.0622 | 0.0762 | 0.1351 |
 | 2024-01-11 | 0.0456 | 0.0472 | 0.0507 | 0.054 | 0.0619 | 0.076 | 0.1344 |
 | 2024-01-12 | 0.0451 | 0.0467 | 0.0502 | 0.0534 | 0.0613 | 0.0753 | 0.1338 |
 | 2024-01-15 | 0.0451 | 0.0467 | 0.0501 | 0.0533 | 0.0611 | 0.0751 | 0.1328 |

## get_ice_bofa_total_return
This data represents the total return of the ICE BofA Indices, When the last calendar day of the month takes place on the weekend, weekend observations will occur as a result of month ending accrued interest adjustments.

The total return is the actual rate of return of an investment or a pool of investments over a given evaluation period. Total return includes interest, capital gains, dividends and distributions realized over a given period of time.

See definitions:


- Ratings: [https://fred.stlouisfed.org/series/BAMLC0A4CBBBEY](https://fred.stlouisfed.org/series/BAMLC0A4CBBBEY){:target="_blank"} 
- Maturity: [https://fred.stlouisfed.org/series/BAMLC1A0C13YEY](https://fred.stlouisfed.org/series/BAMLC1A0C13YEY){:target="_blank"}

**Args:**
 - <u>maturity (bool, optional):</u> Whether to return the maturity total return or the rating total return.
 - <u>rounding (int | None, optional):</u> The number of decimals to round the results to. Defaults to None.

 **Returns:**
 pd.DataFrame: A DataFrame containing the Gross Domestic Product

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import FixedIncome

fixedincome = FixedIncome(
start_date='2024-01-01',
end_date='2024-01-15',
)

fixedincome.get_total_return(maturity=True)
{% endhighlight %}


Which returns:

| Date | 1-3 Years | 3-5 Years | 5-7 Years | 7-10 Years | 10-15 Years | 15+ Years |
 |:-----------|------------:|------------:|------------:|-------------:|--------------:|------------:|
 | 2024-01-01 | 1913.78 | 2487.68 | 809.13 | 585.705 | 4206.25 | 4358.69 |
 | 2024-01-02 | 1912.73 | 2484.25 | 807.62 | 584.32 | 4193.7 | 4343.71 |
 | 2024-01-03 | 1912.18 | 2483.95 | 807.54 | 583.84 | 4194.39 | 4339.07 |
 | 2024-01-04 | 1910.86 | 2477.9 | 804.35 | 580.42 | 4163.24 | 4289.24 |
 | 2024-01-05 | 1910.86 | 2475.75 | 802.82 | 578.73 | 4148.31 | 4262.52 |
 | 2024-01-08 | 1912.48 | 2480.39 | 804.97 | 580.71 | 4167.04 | 4302.16 |
 | 2024-01-09 | 1913.5 | 2482.27 | 805.72 | 581.26 | 4173.04 | 4303.34 |
 | 2024-01-10 | 1914.12 | 2483.6 | 806.21 | 581.29 | 4175.16 | 4304.82 |
 | 2024-01-11 | 1918.28 | 2492.25 | 809.94 | 583.92 | 4200.49 | 4330.72 |
 | 2024-01-12 | 1922.1 | 2498.89 | 812.41 | 585.2 | 4213.47 | 4338.43 |
 | 2024-01-15 | 1922.67 | 2499.76 | 812.67 | 585.41 | 4215.34 | 4340.24 |

## get_ice_bofa_yield_to_worst
This data represents the semi
-annual yield to worst of the ICE BofA Indices, When the last calendar day of the month takes place on the weekend, weekend observations will occur as a result of month ending accrued interest adjustments.

Yield to worst is the lowest potential yield that a bond can generate without the issuer defaulting. The standard US convention for this series is to use semi
-annual coupon payments, whereas the standard in the foreign markets is to use coupon payments with frequencies of annual, semi
-annual, quarterly, and monthly.

See definitions:


- Ratings: [https://fred.stlouisfed.org/series/BAMLC0A4CBBBEY](https://fred.stlouisfed.org/series/BAMLC0A4CBBBEY){:target="_blank"} 
- Maturity: [https://fred.stlouisfed.org/series/BAMLC1A0C13YEY](https://fred.stlouisfed.org/series/BAMLC1A0C13YEY){:target="_blank"}

**Args:**
 - <u>maturity (bool, optional):</u> Whether to return the maturity yield to worst or the rating yield to worst.
 - <u>rounding (int | None, optional):</u> The number of decimals to round the results to. Defaults to None.

 **Returns:**
 pd.DataFrame: A DataFrame containing the Gross Domestic Product

 As an example:
{% include code_header.html %}
{% highlight python %}
from financetoolkit import FixedIncome

fixedincome = FixedIncome(
start_date='2024-01-01',
end_date='2024-01-15',
)

fixedincome.get_yield_to_worst(maturity=False)
{% endhighlight %}


Which returns:

| Date | AAA | AA | A | BBB | BB | B | CCC |
 |:-----------|-------:|-------:|-------:|-------:|-------:|-------:|-------:|
 | 2024-01-01 | 0.0456 | 0.0472 | 0.0503 | 0.0542 | 0.0645 | 0.0786 | 0.1316 |
 | 2024-01-02 | 0.046 | 0.0475 | 0.0506 | 0.0546 | 0.0652 | 0.0796 | 0.1329 |
 | 2024-01-03 | 0.0461 | 0.0475 | 0.0507 | 0.0547 | 0.0662 | 0.081 | 0.1353 |
 | 2024-01-04 | 0.0468 | 0.0483 | 0.0515 | 0.0554 | 0.0665 | 0.0814 | 0.136 |
 | 2024-01-05 | 0.0471 | 0.0486 | 0.0518 | 0.0557 | 0.0667 | 0.0816 | 0.1362 |
 | 2024-01-08 | 0.0466 | 0.0482 | 0.0514 | 0.0553 | 0.066 | 0.0806 | 0.1359 |
 | 2024-01-09 | 0.0465 | 0.0481 | 0.0513 | 0.0551 | 0.0656 | 0.0803 | 0.1353 |
 | 2024-01-10 | 0.0465 | 0.0481 | 0.0512 | 0.0551 | 0.065 | 0.0795 | 0.1345 |
 | 2024-01-11 | 0.0458 | 0.0473 | 0.0504 | 0.0543 | 0.0648 | 0.0793 | 0.134 |
 | 2024-01-12 | 0.0453 | 0.0468 | 0.0499 | 0.0537 | 0.0642 | 0.0786 | 0.1335 |
 | 2024-01-15 | 0.0452 | 0.0468 | 0.0498 | 0.0537 | 0.064 | 0.0784 | 0.1325 |

