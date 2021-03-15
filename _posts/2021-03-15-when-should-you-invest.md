---
layout: post
title: When Should You Invest?
---

![WhenShouldYouInvest](public/post_images/WhenShouldYouInvest.jfif)

When I see the stock market go down, I ask myself frequently if I should invest before it goes up again. I asked myself
this question a lot as the stock market plummeted due to the Coronacrisis. Seeing how many financial indicators exist
that claim to measure the current situation in the market gives the impression there is an ideal moment to invest.
**Thus, when exactly is that moment?**

Anticipating on the current situation in the market is referred to as [Market Timing](
https://www.investopedia.com/terms/m/markettiming.asp). You would buy (or sell) at specific dates you believe is the
ideal moment to do so based on (financial) news you have read and/or analysis you have done. Academics strongly believe
that it is impossible to time the market in such a way that you profit more than a Buy-and-Hold
strategy.<sup>[1](#Footnote1)</sup> With this theory in hand, what does this mean for the average investor?

Here is where Python comes into the play. I simulated two methods that invest $100,- every month over a 10-year period
in the largest indices according
to [Yahoo Finance](https://medium.com/r?url=https%3A%2F%2Ffinance.yahoo.com%2Fworld-indices) <sup>[2](#Footnote2)</sup>.
These two methods are:

1. **Same Day**: invest on the same day every month, simulated for the 1st day of the month until the 28th (to prevent
   not investing in February).
2. **‘Random’ Days**: invest on a random day every month, sampled 2000 times for every index to simulate trying to
   anticipate the market.

## Finding the Perfect Moment

First, let’s start off by looking at the returns of investing on the same day every month. To account for potential
[skewness](https://www.investopedia.com/terms/s/skewness.asp#:~:text=Skewness%20refers%20to%20distortion%20or,varies%20from%20a%20normal%20distribution.)
in the data, I use the median returns instead of the average returns. Note that it doesn’t matter how much return is
made but only how much more (or less) is made compared to the Random Days method.

![WhenShouldYouInvest](public/post_images/Month Days Graph.png)

As you can see it matters very little on what day you invest as the variability is very small (about 0.5%). On average
you will end up with a return of about 16.5%. Now let’s have a look at the median returns for the Random Days method.

![WhenShouldYouInvest](public/post_images/Random Days Graph.png)

One thing that you can see right away is the increase in variability. Whereas the choices between the Same Day Method
would only result in a small change, investing systematically at the wrong moments could penalise your returns by up to
2.3%. While the potential returns are higher (up to 18%) the median return is the same as the Same Day
method. <sup>[3](#Footnote3)</sup>

Therefore, since it is impossible to time the market (gain more than average), the average investor would gain about the
same return whether he or she invests completely random or on the same date each month. **Of course there are going to
be investors that are right (or wrong) more than average but this does not violate the conclusion. This is because with
enough investors, there is always someone who does better on average by pure chance just like there is always someone
that wins the lottery.** <sup>[4](#Footnote4)</sup>

## Emotional Investing

With this conclusion, this is exactly where many investors fall into a trap called the [Optimism Bias](
https://blog.prototypr.io/it-wont-happen-to-me-438e59d5ad42). This means that you believe that you are able to gain more
than average returns because you are not the “average investor”. This touches strongly on Behavioural Finance, the
discipline that studies the irrationality of an investor.

![WhenShouldYouInvest](public/post_images/Sheep.jfif)

A great example is.. myself. I currently work in the Finance domain and have a Master’s in Finance as well. Of course I
am better than the average investor right?! Wrong. My degree and experience do not make me an exception to the concept
of Market Timing as numerous studies have shown that even Investment Managers are not able to time the market
correctly.<sup>[1](#Footnote1)</sup>

Falling for behavioural biases like overreaction, tendency to buy high and sell low, herding behaviour and the optimism
bias causes you to gain lower returns than you would have gotten if you remained rational. Even when you understand that
these biases exists, you will still fall for them. Therefore, while the results of the two methods in a rational world
are the same, the influence of your own decisions causes you to gain a lower return on average if you attempt to invest
randomly or make an effort to time the market.

### So when should you invest? On the same day every month.

___
<a name="Footnote1">[1]</a> Some academic literature that supports the Market Timing theory:

- Sharpe, W. F. (1975). Likely Gains from Market Timing. Financial Analysts Journal, 31(2), 60–69.
- Bollen & Busse. (2001). On the Performance of Mutual Fund Managers. The Journal of Finance, LVI(3), 1075.
- Jagannathan, R., & Korajczyk, R. A. (2017). Assessing the Market Timing Performance of Managed Portfolios. The Journal
  of Business, 59(2), 217–235.

<a name="Footnote2">[2]</a>  The decisions for investing in indices and each month result from two concepts:

1. **Efficient Market Hypothesis**: all public information is accurately reflected in the price of an instrument.
   Therefore Fundamental and Technical analysis has no additional benefit when the (specific) market is efficient
   according to the paper by Eugen F. Fama titled “Efficient Capital Markets: A Review of Theory and Emperical Work” and
   recent work by Burton G. Malkiel titled “The Efficient Market Hypothesis and its Critics”. Note: this theory does not
   always hold due to information asymmetry (information is not available to all and sometimes is costly) and arbitrage
   is not cost- and risk free. However, it does generally hold for large markets like the ones mentioned on the Yahoo
   Finance page.
2. **Dollar Cost Averaging**: in an effort to reduce the volatility on an investment and to prevent holding off on
   investing until the right price, the total amount invested is spread out throughout the months.

<a name="Footnote3">[3]</a>  To check whether these results also hold for a specific index, I looked at the S&P 500 over
the same 10 year period. The Same Day results showed a median of 70.3% with a variability of 1.7% whereas the Random
Days method showed a median of 70.1% with a variability of 3.6%. While the difference between variability changed, this
still sends the same message as depicted in the graphs.

<a name="Footnote4">[4]</a>  As the Efficient Market Hypothesis states that the stock market follows a [Random Walk](
https://www.investopedia.com/terms/r/randomwalktheory.asp), you can calculate the lucky few. An example would be
guessing whether the S&P 500 has a positive or negative return the upcoming 15 years. This seems like nearly impossible
but with enough people, let’s say 1,000,000, there will be 30 people who guess all 15 years correctly. (0.5¹⁵ *
1,000,000)