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

The Fixed Income module covers a wide variety of calculations including the Effective Yield, Macaulay Duration, Modified Duration, Convexity, Yield to Maturity and derivative pricing models such as Black and Bachelier (used for Swaptions and other instruments).

To install the FinanceToolkit it simply requires the following:

```python
pip install financetoolkit -U
```

{% include algolia.html %}

## collect_bond_statistics
Collect the bond statistics for a given bond which includes the following fields:

- Par Value: The face value of the bond. - Coupon Rate: The annual coupon rate (in decimal). - Years to Maturity: The number of years until the bond matures. - Yield to Maturity: The yield to maturity of the bond (in decimal). - Frequency: The number of coupon payments per year. - Present Value: The present value of the bond. - Current Yield: The annual coupon payment divided by the bond price. - Effective Yield: The annualised yield that accounts for the compounding of the coupon payments made within the year. - Macaulay's Duration: The weighted average time to receive the bond's cash flows. - Modified Duration: The Macaulay's duration divided by 1 plus the per-period yield (yield to maturity divided by the frequency). - Effective Duration: The percentage price change per unit change in yield, obtained by repricing the bond symmetrically 1% above and 1% below the current yield. - Dollar Duration: The modified duration multiplied by the bond price, divided by 100. - DV01: The currency change in the bond's price, per par value of face, for a one basis point (0.01%) change in the yield to maturity. - Convexity: The second derivative of the bond price with respect to the yield to maturity.

These statistics can be used to evaluate the bond's performance as opposed to other bonds or to estimate the bond's sensitivity to changes in interest rates to be able to apply a hedging strategy.

**Also known as:** bond data, fixed income statistics.

**Args:**

- <u>par_value (float):</u> The face value of the bond. Defaults to 100.
- <u>coupon_rate (float):</u> The annual coupon rate (in decimal). Defaults to 0.05.
- <u>years_to_maturity (int):</u> The number of years until the bond matures. Defaults to 5.
- <u>yield_to_maturity (float):</u> The yield to maturity of the bond (in decimal). Defaults to 0.08.
- <u>frequency (int):</u> The number of coupon payments per year. Defaults to 1.
- <u>show_input_info (bool, optional):</u> Whether to display input information. Defaults to True.

**Returns:**

pd.Series: A pandas Series containing the bond statistics.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome()

# This is one example and below a collection of different bonds is shown with different characteristics
fixedincome.collect_bond_statistics(
    par_value=100,
    coupon_rate=0.05,
    years_to_maturity=5,
    yield_to_maturity=0.08,
    frequency=1,
)
```

Which returns:

|                     |   Bond 1 |   Bond 2 |   Bond 3 |   Bond 4 |   Bond 5 |   Bond 6 |
|:--------------------|---------:|---------:|---------:|---------:|---------:|---------:|
| Par Value           | 100      | 250      |  50      | 1000     |  85      | 320      |
| Coupon Rate         |   0.05   |   0.02   |   0.075  |    0     |   0.15   |   0.015  |
| Years to Maturity   |   5      |  10      |   2      |   10     |   3      |   1      |
| Yield to Maturity   |   0.08   |   0.021  |   0.03   |    0     |   0.16   |   0.04   |
| Frequency           |   1      |   1      |   4      |    1     |   2      |  12      |
| Present Value       |  88.0219 | 247.766  |  54.3518 | 1000     |  83.0353 | 312.171  |
| Current Yield       |   0.0568 |   0.0202 |   0.069  |    0     |   0.1535 |   0.0154 |
| Effective Yield     |   0.05   |   0.02   |   0.0771 |    0     |   0.1556 |   0.0151 |
| Macaulay's Duration |   4.5116 |   9.1576 |   1.8819 |   10     |   2.5167 |   0.9931 |
| Modified Duration   |   4.1774 |   8.9693 |   1.8679 |   10     |   2.3302 |   0.9898 |
| Effective Duration  |   4.1798 |   8.9874 |   1.8681 |   10.022 |   2.3307 |   0.9898 |
| Dollar Duration     |   3.677  |  22.2228 |   1.0152 |  100     |   1.9349 |   3.0897 |
| DV01                |   0.0368 |   0.2222 |   0.0102 |    1     |   0.0193 |   0.0309 |
| Convexity           |  22.4017 |  93.7509 |   4.0849 |  110     |   7.0923 |   1.0662 |

Note how the effective duration sits just above the modified duration for every
bond: the two measure the same sensitivity, and their small difference is exactly
the convexity picked up by repricing over a 100 basis point shift rather than
differentiating at a point.


---

## get_present_value
Calculates the bond prices for different coupon rates and years to maturity. The bond price is the present value of the bond's future cash flows, which includes the coupon payments and the par value of the bond at maturity. The bond price is calculated using the following formula:

- Bond Price = (C / r) * (1 - (1 + r)^-n) + F / (1 + r)^n

where:

- C = Coupon payment per period
- r = Yield to maturity per period
- n = Number of periods
- F = Face value of the bond

The bond price is used to determine the fair value of the bond and to compare the bond's price to its market price to determine if the bond is overvalued or undervalued.

**Also known as:** PV, bond pricing, discounted cash flows.

**Args:**

- <u>par_value (float):</u> The par value (face value) of the bond.
- <u>coupon_rate (float, optional):</u> The coupon rate of the bond. If not provided, a range of coupon rates will be used.
- <u>years_to_maturity (float, optional):</u> The years to maturity of the bond in years. If not provided, a range of years to maturity will be used.
- <u>yield_to_maturity (float, optional):</u> The yield to maturity of the bond. Defaults to 0.08.
- <u>frequency (int, optional):</u> The frequency of coupon payments per year. Defaults to 1.
- <u>show_input_info (bool, optional):</u> Whether to display input information. Defaults to True.

**Returns:**

pandas.DataFrame: A DataFrame containing the bond prices for different coupon rates and years to maturity.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome()

fixedincome.get_present_value(
    coupon_rate=[0.03, 0.05, 0.07],
    years_to_maturity=[5, 10, 15],
    show_input_info=False,
)
```

Which returns:

|   Coupon Rate |     5 |    10 |    15 |
|--------------:|------:|------:|------:|
|          0.03 | 80.04 | 66.45 | 57.2  |
|          0.05 | 88.02 | 79.87 | 74.32 |
|          0.07 | 96.01 | 93.29 | 91.44 |


---

## get_duration
Calculates the bond duration for different coupon rates and years to maturity. It has the option to calculate the following type of bond durations:

- Macaulay's Duration: The weighted average time to receive the bond's cash flows.
- Modified Duration: The Macaulay's duration divided by 1 plus the per-period yield (yield to maturity divided by the frequency).
- Effective Duration: The percentage change in the bond price for a 1% change in the yield to maturity.
- Dollar Duration: The modified duration multiplied by the bond price, divided by 100.

These duration measures can be used to estimate the sensitivity of a bond's price to changes in interest rates as well as to compare the risk of different bonds. The modified duration is particularly useful for estimating the percentage change in the bond price for a 1% change in the yield to maturity. Note that it is a percentage sensitivity and therefore not the same as the dollar duration, the price value of a basis point (PVBP) or the dollar value of a 0.01% change (DV01), which are all expressed as a currency amount instead. The dollar duration is available through this method via `duration_type='dollar'` and the DV01 is calculated separately, see `collect_bond_statistics`.

**Also known as:** Macaulay duration, modified duration, bond price sensitivity.

**Args:**

- <u>duration_type (str, optional):</u> The type of duration to calculate. Defaults to 'modified' but can also
be 'macaulay', 'effective' or 'dollar'.
- <u>par_value (float, optional):</u> The par value (face value) of the bond. Defaults to 100.
- <u>coupon_rate (float, optional):</u> The coupon rate of the bond. If not provided, a range of coupon
rates will be used. Defaults to None.
- <u>years_to_maturity (float, optional):</u> The years to maturity of the bond in years. If not provided, a range of years
to maturity will be used. Defaults to None.
- <u>yield_to_maturity (float, optional):</u> The yield to maturity of the bond. Defaults to 0.08.
- <u>frequency (int, optional):</u> The frequency of coupon payments per year. Defaults to 1.
- <u>show_input_info (bool, optional):</u> Whether to display input information. Defaults to True.

**Returns:**

pandas.DataFrame: A DataFrame containing the bond duration for different coupon rates and years to maturity.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome()

fixedincome.get_duration(
    duration_type='modified',
    coupon_rate=[0.03, 0.05, 0.07],
    years_to_maturity=[5, 10, 15],
    show_input_info=False,
)
```

Which returns:

|   Coupon Rate |    5 |   10 |    15 |
|--------------:|-----:|-----:|------:|
|          0.03 | 4.33 | 7.82 | 10.4  |
|          0.05 | 4.18 | 7.26 |  9.41 |
|          0.07 | 4.05 | 6.87 |  8.79 |


---

## get_yield_to_maturity
Calculates the yield to maturity for a bond. The yield to maturity is the internal rate of return of the bond, which is the discount rate that equates the present value of the bond's cash flows to its market price. The yield to maturity is used to estimate the bond's return and to compare the bond's return to other investments.

The yield to maturity is calculated using the following formula:

- Bond Price = (C / r) * (1 - (1 + r)^-n) + F / (1 + r)^n

where:

- C = Coupon payment per period
- r = Yield to maturity per period
- n = Number of periods
- F = Face value of the bond

The goal is to find the yield to maturity that satisfies the equation above. This is done using the secant method which is an iterative method that converges to the root of a function.

**Also known as:** YTM, bond return to maturity.

**Args:**

- <u>par_value (float):</u> The par value (face value) of the bond. This is the original price when it was issued by the issuer.
- <u>coupon_rate (float, optional):</u> The coupon rate of the bond. Defaults to 0.05.
- <u>years_to_maturity (float, optional):</u> The years to maturity of the bond in years. Defaults to None.
- <u>bond_price (float, optional):</u> The price of the bond. Defaults to None.
- <u>frequency (int, optional):</u> The number of coupon payments per year. Defaults to 1.
- <u>guess (float, optional):</u> The initial guess for the yield to maturity. Defaults to 0.05.
- <u>tolerance (float, optional):</u> The tolerance level for convergence. Defaults to 0.0001.
- <u>max_iterations (int, optional):</u> The maximum number of iterations for convergence. Defaults to 100.
- <u>show_input_info (bool, optional):</u> Whether to display input information. Defaults to True.

**Returns:**

pandas.DataFrame: A DataFrame containing the yield to maturity for different bond prices and years to maturity.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome()

fixedincome.get_yield_to_maturity(
    coupon_rate=0.05,
    years_to_maturity=[5, 10, 15],
    bond_price=[95, 100, 105],
    show_input_info=False,
)
```

Which returns:

|   Bond Price |      5 |     10 |     15 |
|-------------:|-------:|-------:|-------:|
|           95 | 0.0619 | 0.0567 | 0.055  |
|          100 | 0.05   | 0.05   | 0.05   |
|          105 | 0.0388 | 0.0437 | 0.0453 |


---

## get_forward_rate
Calculates the implied forward rate between pairs of points on a zero-coupon (spot) yield curve. The forward rate is the interest rate, implied by today's yield curve, for a loan that starts at a future date - it is derived purely from no-arbitrage pricing rather than a forecast of future rates.

The rate for each maturity is obtained by linearly interpolating the supplied spot curve, so `near_maturity` and `far_maturity` do not need to coincide exactly with a maturity present in `spot_rates`.

The forward rate is calculated using the following formula:

- Forward Rate = ((1 + r2)^t2 / (1 + r1)^t1)^(1 / (t2 - t1)) - 1

where:

- r1 = Spot rate at the near maturity
- t1 = Near maturity, in years
- r2 = Spot rate at the far maturity
- t2 = Far maturity, in years

**Also known as:** implied forward rate, forward-forward rate.

**Args:**

- <u>spot_rates (pd.Series \| dict, optional):</u> The zero-coupon (spot) yield curve,
indexed by maturity in years (in decimal). Defaults to a sample curve.
- <u>near_maturity (float \| list, optional):</u> The nearer maturity (or maturities),
in years. If not provided, a range of near maturities will be used.
- <u>far_maturity (float \| list, optional):</u> The further maturity (or maturities),
in years. If not provided, a range of far maturities will be used.
- <u>show_input_info (bool, optional):</u> Whether to display input information. Defaults to True.

**Returns:**

pandas.DataFrame: A DataFrame containing the forward rate for each combination
of near and far maturity. Combinations where the far maturity is not greater
than the near maturity are returned as NaN.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome()

fixedincome.get_forward_rate(
    near_maturity=[1, 2, 3],
    far_maturity=[5, 10],
    show_input_info=False,
)
```

Which returns:

|   Near Maturity |     5 |     10 |
|-----------------:|------:|-------:|
|                1 |  0.04 | 0.0456 |
|                2 | 0.042 |  0.047 |
|                3 | 0.044 | 0.0483 |


---

## get_par_yield
Calculates the par yield curve implied by a zero-coupon (spot) yield curve. The par yield for a given maturity is the coupon rate that would need to be attached to a newly-issued bond of that maturity so that, once its cash flows are discounted with the spot curve, its price equals its par value exactly.

This is the curve that is typically quoted for on-the-run government bonds, as opposed to the theoretical spot curve which is usually bootstrapped rather than directly observed.

The par yield is calculated using the following formula:

- Par Yield = frequency * (1 - DF(n)) / SUM(DF(k))

where DF(k) = 1 / (1 + spot_rate(k / frequency) / frequency)^k is the discount factor for the cash flow at period k, spot_rate(t) is obtained by interpolating the spot curve at time t (in years), and n = years_to_maturity * frequency is the number of coupon periods.

**Also known as:** par rate, par coupon rate.

**Args:**

- <u>spot_rates (pd.Series \| dict, optional):</u> The zero-coupon (spot) yield curve,
indexed by maturity in years (in decimal). Defaults to a sample curve.
- <u>years_to_maturity (float \| list, optional):</u> The maturity (or maturities), in
years, to calculate the par yield for. If not provided, a range of years
to maturity will be used.
- <u>frequency (int, optional):</u> The number of coupon payments per year. Defaults to 1.
- <u>par_value (float, optional):</u> The face value of the bond. Defaults to 100.
- <u>show_input_info (bool, optional):</u> Whether to display input information. Defaults to True.

**Returns:**

pandas.Series: A Series containing the par yield for each requested maturity,
i.e. the par yield curve.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome()

fixedincome.get_par_yield(
    years_to_maturity=[1, 2, 3, 5, 10],
    show_input_info=False,
)
```

Which returns:

|   Years to Maturity |   Par Yield |
|--------------------:|------------:|
|                   1 |      0.03   |
|                   2 |      0.032  |
|                   3 |      0.0339 |
|                   5 |      0.0377 |
|                  10 |      0.0431 |


---

## get_yield_curve_spread
Calculates the spread between pairs of points on a yield curve, e.g. the widely followed 10-year minus 2-year Treasury spread. A positive spread indicates a "normal" upward-sloping curve, while a negative spread ("inversion") has historically been used as a leading indicator of an economic slowdown.

The rate for each maturity is obtained by linearly interpolating the supplied curve, so `long_maturity` and `short_maturity` do not need to coincide exactly with a maturity present in `spot_rates`.

The yield curve spread is calculated using the following formula:

- Yield Curve Spread = Long-Term Yield - Short-Term Yield

**Also known as:** term spread, yield curve slope.

**Args:**

- <u>spot_rates (pd.Series \| dict, optional):</u> The yield curve, indexed by
maturity in years (in decimal). Defaults to a sample curve.
- <u>long_maturity (float \| list, optional):</u> The longer maturity (or maturities),
in years. If not provided, a range of long maturities will be used.
- <u>short_maturity (float \| list, optional):</u> The shorter maturity (or
maturities), in years. If not provided, a range of short maturities
will be used.
- <u>show_input_info (bool, optional):</u> Whether to display input information. Defaults to True.

**Returns:**

pandas.DataFrame: A DataFrame containing the yield curve spread for each
combination of long and short maturity.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome()

fixedincome.get_yield_curve_spread(
    long_maturity=[10, 30],
    short_maturity=[1, 2],
    show_input_info=False,
)
```

Which returns:

|   Long Maturity |     1 |     2 |
|-----------------:|------:|------:|
|               10 | 0.014 | 0.012 |
|               30 |  0.02 | 0.018 |


---

## get_breakeven_inflation_rate
Calculates the breakeven inflation rate implied by a nominal and a real (inflation-protected) yield curve, e.g. the U.S. Treasury nominal curve versus the TIPS (Treasury Inflation-Protected Securities) curve. It is the rate of inflation that would make an investor indifferent between holding a nominal bond and an inflation-protected bond of the same maturity, and is widely used as a market-implied measure of expected inflation.

The rate for each maturity is obtained by linearly interpolating the supplied curves, so `maturity` does not need to coincide exactly with a maturity present in `nominal_rates` or `real_rates`.

The breakeven inflation rate is calculated using the following formula:

- Breakeven Inflation Rate = Nominal Yield - Real Yield

**Also known as:** TIPS breakeven spread, inflation breakeven.

**Args:**

- <u>nominal_rates (pd.Series \| dict, optional):</u> The nominal (non-inflation-protected)
yield curve, indexed by maturity in years (in decimal). Defaults to a sample curve.
- <u>real_rates (pd.Series \| dict, optional):</u> The real (inflation-protected) yield
curve, indexed by maturity in years (in decimal). Defaults to a sample curve.
- <u>maturity (float \| list, optional):</u> The maturity (or maturities), in years,
to calculate the breakeven inflation rate for. If not provided, a range
of maturities will be used.
- <u>show_input_info (bool, optional):</u> Whether to display input information. Defaults to True.

**Returns:**

pandas.Series: A Series containing the breakeven inflation rate for each
requested maturity, i.e. the breakeven inflation curve.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome()

fixedincome.get_breakeven_inflation_rate(
    maturity=[1, 5, 10, 30],
    show_input_info=False,
)
```

Which returns:

|   Maturity |   Breakeven Inflation Rate |
|-----------:|----------------------------:|
|          1 |                       0.022 |
|          5 |                       0.026 |
|         10 |                       0.028 |
|         30 |                        0.03 |


---

## get_z_spread
Calculates the zero-volatility spread (Z-spread) for a bond given a benchmark zero-coupon (spot) yield curve. The Z-spread is the constant spread that, when added uniformly to every point of the benchmark curve, makes the present value of the bond's discounted cash flows equal to its observed market price.

Unlike a simple yield spread (the bond's yield to maturity minus a benchmark yield of the same maturity), the Z-spread is measured against the entire curve rather than a single point, which makes it a more accurate measure of the compensation an investor receives for a bond's credit and liquidity risk.

The Z-spread is found iteratively using the secant method, in the same way that `get_yield_to_maturity` solves for the yield to maturity.

**Also known as:** zero-volatility spread, static spread.

**Args:**

- <u>par_value (float):</u> The par value (face value) of the bond.
- <u>coupon_rate (float, optional):</u> The coupon rate of the bond. Defaults to 0.05.
- <u>years_to_maturity (float, optional):</u> The years to maturity of the bond in years. Defaults to None.
- <u>bond_price (float, optional):</u> The price of the bond. Defaults to None.
- <u>spot_rates (pd.Series \| dict, optional):</u> The benchmark zero-coupon (spot)
yield curve, indexed by maturity in years (in decimal). Defaults to a sample curve.
- <u>frequency (int, optional):</u> The number of coupon payments per year. Defaults to 1.
- <u>guess (float, optional):</u> The initial guess for the Z-spread. Defaults to 0.01.
- <u>tolerance (float, optional):</u> The tolerance level for convergence. Defaults to 0.0001.
- <u>max_iterations (int, optional):</u> The maximum number of iterations for convergence. Defaults to 100.
- <u>show_input_info (bool, optional):</u> Whether to display input information. Defaults to True.

**Returns:**

pandas.DataFrame: A DataFrame containing the Z-spread for different bond prices and years to maturity.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome()

fixedincome.get_z_spread(
    coupon_rate=0.05,
    years_to_maturity=[5, 10, 15],
    bond_price=[95, 100, 105],
    show_input_info=False,
)
```

Which returns:

|   Bond Price |      5 |     10 |     15 |
|-------------:|-------:|-------:|-------:|
|            95 | 0.0243 | 0.0137 | 0.0103 |
|           100 | 0.0124 |  0.007 | 0.0053 |
|           105 | 0.0012 | 0.0007 | 0.0005 |


---

## get_bond_equivalent_yield
Converts a money-market discount yield (e.g. quoted for Treasury bills) into a bond-equivalent yield (BEY). Money-market instruments are often quoted on a discount-yield basis, which understates the actual return an investor earns because it is computed on face value rather than the (lower) purchase price, and uses a 360-day rather than a 365-day year. The bond-equivalent yield restates the discount yield on a basis that is comparable to coupon-bearing bonds and notes.

The bond-equivalent yield is calculated using the following formula:

- BEY = 365 * Discount Yield / (360 - Days to Maturity * Discount Yield)

for a bill with half a year or less remaining. Beyond that an equivalent coupon-bearing note would have paid a coupon at the six month point, so the U.S. Treasury's semi-annually compounded solution (31 CFR 356, Appendix B) is used instead - see `bond_model.get_bond_equivalent_yield`. Applying the simple formula to a 52-week bill instead overstates its yield by roughly seven basis points.

**Also known as:** BEY, coupon-equivalent yield, investment rate.

**Args:**

- <u>discount_yield (float \| list, optional):</u> The money-market discount yield of
the instrument (in decimal). If not provided, a range of discount yields
will be used.
- <u>days_to_maturity (float \| list, optional):</u> The number of days until the
instrument matures. If not provided, a range of typical T-bill maturities
will be used.
- <u>show_input_info (bool, optional):</u> Whether to display input information. Defaults to True.

**Returns:**

pandas.DataFrame: A DataFrame containing the bond-equivalent yield for
different discount yields and days to maturity.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome()

fixedincome.get_bond_equivalent_yield(
    discount_yield=[0.03, 0.05, 0.07],
    days_to_maturity=[90, 180, 360],
    show_input_info=False,
)
```

Which returns:

|   Discount Yield |     90 |    180 |    360 |
|-----------------:|-------:|-------:|-------:|
|             0.03 | 0.0306 | 0.0309 | 0.0311 |
|             0.05 | 0.0513 | 0.052  | 0.0527 |
|             0.07 | 0.0722 | 0.0735 | 0.0749 |

The 360-day column is computed with the Treasury's semi-annually compounded formula
rather than the simple one, because a bill of that length would have paid a coupon
halfway through if it were a note.


---

## get_key_rate_duration
Calculates the key rate duration of a bond for one or more individual maturity points ("key rates") on the yield curve. Whereas `get_duration` with `duration_type='effective'` assumes the entire curve shifts in parallel, key rate duration measures the bond's price sensitivity to a shock at a single tenor of the curve while every other point is held fixed. Because cash flows are discounted using linear interpolation between the curve's tenors, a shock at one tenor tapers off towards its neighboring tenors and has no effect beyond them.

Summing the key rate durations across every tenor of the curve approximately reproduces the bond's effective (parallel-shift) duration, but key rate duration additionally reveals which segment of the curve the bond's price is most exposed to - information that is essential for constructing curve-neutral hedges or identifying "twist" risk.

**Also known as:** partial duration, rate-specific duration.

**Args:**

- <u>par_value (float, optional):</u> The par value (face value) of the bond. Defaults to 100.
- <u>coupon_rate (float, optional):</u> The coupon rate of the bond. Defaults to 0.05.
- <u>years_to_maturity (float \| list, optional):</u> The years to maturity of the
bond (or bonds). If not provided, a range of years to maturity will be used.
- <u>spot_rates (pd.Series \| dict, optional):</u> The zero-coupon (spot) yield curve
used to discount the bond's cash flows, indexed by maturity in years (in
decimal). Defaults to a sample curve.
- <u>key_rate_maturity (float \| list, optional):</u> The maturity (or maturities), in
years, of the curve point(s) to shock. Must be present in the index of
`spot_rates`. Defaults to every maturity in `spot_rates`.
- <u>frequency (int, optional):</u> The number of coupon payments per year. Defaults to 1.
- <u>yield_change (float, optional):</u> The size of the shock applied to each key
rate, up and down (in decimal). Defaults to 0.0001 (1 basis point).
- <u>show_input_info (bool, optional):</u> Whether to display input information. Defaults to True.

**Returns:**

pandas.DataFrame: A DataFrame containing the key rate duration for different
bond maturities and key rate maturities.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome()

fixedincome.get_key_rate_duration(
    coupon_rate=0.05,
    years_to_maturity=[5, 10],
    key_rate_maturity=[2, 5, 10],
    show_input_info=False,
)
```

Which returns:

|   Years to Maturity |      2 |      5 |     10 |
|---------------------:|-------:|-------:|-------:|
|                    5 | 0.0862 | 4.0561 |     -0 |
|                   10 | 0.0862 |  0.377 | 6.4666 |


---

## get_taylor_price_change
Estimates the percentage change in a bond's price for a given change in yield, using a second-order Taylor series expansion that combines modified duration and convexity.

Modified duration alone only captures the first-order (linear) relationship between a bond's price and its yield, which understates the price increase for a yield decrease and overstates the price decrease for a yield increase because the true price-yield relationship is curved (convex), not linear. Adding a convexity term corrects for this and produces a substantially more accurate estimate, especially for larger yield changes.

This method calls `get_modified_duration` and `get_convexity` from `bond_model.py` directly rather than recomputing them.

The Taylor approximation is calculated using the following formula:

- %ΔPrice ≈ -Modified Duration * Δy + 0.5 * Convexity * Δy^2

**Also known as:** duration-convexity approximation, second-order price approximation.

**Args:**

- <u>par_value (float, optional):</u> The par value (face value) of the bond. Defaults to 100.
- <u>coupon_rate (float, optional):</u> The coupon rate of the bond. If not provided,
a range of coupon rates will be used.
- <u>years_to_maturity (float, optional):</u> The years to maturity of the bond in
years. If not provided, a range of years to maturity will be used.
- <u>yield_to_maturity (float, optional):</u> The current yield to maturity of the
bond. Defaults to 0.08.
- <u>frequency (int, optional):</u> The number of coupon payments per year. Defaults to 1.
- <u>yield_change (float, optional):</u> The hypothetical change in yield to
maturity, e.g. 0.01 for a 100 basis point increase. Defaults to 0.01.
- <u>show_input_info (bool, optional):</u> Whether to display input information. Defaults to True.

**Returns:**

pandas.DataFrame: A DataFrame containing the estimated percentage price
change for different coupon rates and years to maturity.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome()

fixedincome.get_taylor_price_change(
    coupon_rate=[0.03, 0.05, 0.07],
    years_to_maturity=[5, 10, 15],
    yield_to_maturity=0.08,
    yield_change=0.01,
    show_input_info=False,
)
```

Which returns:

|   Coupon Rate |       5 |      10 |      15 |
|--------------:|--------:|--------:|--------:|
|          0.03 | -0.0421 | -0.0744 |  -0.097 |
|          0.05 | -0.0407 | -0.0693 |  -0.088 |
|          0.07 | -0.0394 | -0.0656 | -0.0824 |


---

## get_derivative_price
Calculates the derivative price for a fixed income instrument.

It is possible to use two different models to calculate the derivative price:

- Black Model: A mathematical model used for pricing financial derivatives, its primary applications are for pricing options on future contracts, bond options, interest rate cap and floors, and swaptions. For more information, see: [https://en.wikipedia.org/wiki/Black_model](https://en.wikipedia.org/wiki/Black_model){:target="_blank"} - Bachelier Model: A deviation of the Black Model that is used for pricing future contracts. It is a simple model that assumes the price of the underlying asset follows a normal distribution with constant volatility. This is in contrast to the Black Model which assumes the price of the underlying asset follows a log-normal distribution. For more information, see: [https://en.wikipedia.org/wiki/Bachelier_model](https://en.wikipedia.org/wiki/Bachelier_model){:target="_blank"}

It is possible to alter all parameters within the models, e.g. strike rate, volatility, years to maturity, risk-free rate, notional amount, and whether the holder is the receiver or payer of the derivative. Next to that, you can provide lists of values for the fixed rate, strike rate, volatility, and years to maturity to calculate the derivative price for multiple scenarios outside of the standard sample.

Exercising a swaption is not a single payment at expiration - it is the right to enter a swap that exchanges cash flows at every payment date over the underlying swap's tenor. The price therefore discounts the option payoff by the swap's annuity (present value of a basis point) rather than a single discount factor to expiration, which is why the tenor and payment frequency of the underlying swap matter.

Note that a swaption's price scales with the tenor of the underlying swap (a right to enter a longer-dated swap is worth more, since it exchanges cash flows over more payment dates) - pass `tenor` explicitly to price a swaption whose underlying swap tenor differs from its years to maturity, e.g. a 1-year option into a 5-year swap: `tenor=5, years_to_maturity=1`.

The two models do not quote volatility on the same basis, and this matters a great deal. Black's model, being lognormal, reads `volatility` as a fraction of the forward rate, so 0.20 is a 20% volatility. The Bachelier model, being normal, reads it as an absolute movement in rate units, so 0.0065 is 65 basis points. On a 3.25% forward those two quotes describe the same market, but swapping one for the other misprices the swaption by a factor of roughly thirty. By default `volatility` is therefore interpreted on whichever basis the chosen model is defined in; set `volatility_type` explicitly to supply a quote on the other basis and have it converted, using the at-the-money approximation sigma_normal ≈ sigma_lognormal * forward_rate.

Black's model is undefined at a zero or negative forward or strike rate because it takes the logarithm of their ratio, and raises rather than returning a silent NaN in that case. Use the Bachelier model for the negative rates seen in the euro area and Japan.

**Also known as:** bond derivative pricing, fixed income derivative, swaption pricing.

**Args:**

- <u>model (str, optional):</u> The type of model to use for calculating the derivative price. Defaults to "black".
- <u>forward_rate (float, optional):</u> The forward rate as derived from the swap curve. Defaults to None.
- <u>strike_rate (float \| list, optional):</u> The strike rate for the derivative. Defaults to None which means it calculates the
derivative price a range of strike prices. Can also be a list of strike rates (e.g. [0.01, 0.02, 0.03, 0.04, 0.05]).
- <u>volatility (float, optional):</u> The volatility of the underlying swap rate, quoted on the
basis given by `volatility_type`. Defaults to 0.01, read as a 1% lognormal volatility
by the Black model and as 100 basis points of normal volatility by the Bachelier model.
- <u>years_to_maturity (float \| list, optional):</u> The years to maturity of the derivative in years. Defaults to None which means it plots
the derivative price for the next 10 years. Can also be a list of years to maturity (e.g. [1, 2.3, 2.5, 3])
- <u>risk_free_rate (float, optional):</u> The risk-free interest rate. Defaults to None which means it is equal to the fixed rate.
- <u>notional (float, optional):</u> The notional amount of the derivative. Defaults to 10_000_000.
- <u>tenor (float \| None, optional):</u> The tenor (length in years) of the underlying swap. Defaults to None,
which means it is equal to years_to_maturity for each scenario.
- <u>payment_frequency (int, optional):</u> Number of fixed-leg payments per year on the underlying swap
(e.g. 1 for annual, 2 for semi-annual, 4 for quarterly). Defaults to 2 (semi-annual).
- <u>is_receiver (bool, optional):</u> True if the holder is the receiver of the derivative, False if the holder is the payer. Defaults to True.
- <u>volatility_type (str \| None, optional):</u> The convention `volatility` is quoted on, either
'lognormal' (relative to the forward rate) or 'normal' (absolute, in rate units).
Defaults to None, which uses the convention the chosen model is natively defined in:
'lognormal' for the Black model and 'normal' for the Bachelier model.
- <u>include_payoff (bool, optional):</u> True to include the payoff in the output, False otherwise. Defaults to False.
- <u>show_input_info (bool, optional):</u> True to display input information, False otherwise. Defaults to True.

**Returns:**

pandas.DataFrame: The derivative prices rounded to the specified decimal places.
pandas.- <u>DataFrame (optional):</u> The derivative payoffs rounded to the specified decimal places if include_payoff is True.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome()

fixedincome.get_derivative_price(
    model='black',
    forward_rate=0.0325,
    strike_rate=[0.0275, 0.0325, 0.0375, 0.0425],
    years_to_maturity=[1, 2, 5, 10],
    show_input_info=False,
)
```

---

## get_government_bond_yield
Long-term interest rates refer to government bonds maturing in ten years. Rates are mainly determined by the price charged by the lender, the risk from the borrower and the fall in the capital value. Long-term interest rates are generally averages of daily rates, measured as a percentage. These interest rates are implied by the prices at which the government bonds are traded on financial markets, not the interest rates at which the loans were issued.

In all cases, they refer to bonds whose capital repayment is guaranteed by governments. Long-term interest rates are one of the determinants of business investment. Low long term interest rates encourage investment in new equipment and high interest rates discourage it. Investment is, in turn, a major source of economic growth.

**See definition:** [https://data.oecd.org/interest/long-term-interest-rates.htm](https://data.oecd.org/interest/long-term-interest-rates.htm){:target="_blank"}

Short-term interest rates are the rates at which short-term borrowings are effected between financial institutions or the rate at which short-term government paper is issued or traded in the market. Short-term interest rates are generally averages of daily rates, measured as a percentage.

Short-term interest rates are based on three-month money market rates where available. Typical standardised names are "money market rate" and "treasury bill rate".

**See definition:** [https://data.oecd.org/interest/short-term-interest-rates.htm](https://data.oecd.org/interest/short-term-interest-rates.htm){:target="_blank"}

**Also known as:** treasury yield, bond yield by maturity.

**Args:**

- <u>short_term (bool, optional):</u> Whether to return the short-term interest rate. Defaults to False.
This means that the long-term interest rate will be returned.
- <u>period (str \| None, optional):</u> Whether to return the monthly, quarterly or the annual data.
- <u>growth (bool, optional):</u> Whether to return the growth data or the actual data.
- <u>lag (int, optional):</u> The number of periods to lag the data by.
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.DataFrame: A DataFrame containing the Long Term Interest Rate.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome(start_date='2023-05-01', end_date='2023-12-31')

long_term_interest_rate = fixedincome.get_government_bond_yield(short_term=False, period='monthly')

long_term_interest_rate.loc[:, ['Japan', 'United States', 'Brazil']]
```

Which returns:

|         |   Japan |   United States |   Brazil |
|:--------|--------:|----------------:|---------:|
| 2023-05 |  0.0043 |          0.0357 |   0.0728 |
| 2023-06 |  0.004  |          0.0375 |   0.0728 |
| 2023-07 |  0.0059 |          0.039  |   0.07   |
| 2023-08 |  0.0064 |          0.0417 |   0.07   |
| 2023-09 |  0.0076 |          0.0438 |   0.07   |
| 2023-10 |  0.0095 |          0.048  |   0.0655 |
| 2023-11 |  0.0066 |          0.045  |   0.0655 |


---

## get_treasury_rates
Retrieves the daily U.S. Treasury par yield curve rates as officially published by the U.S. Department of the Treasury, covering every maturity from 1 Month through 30 Year in a single dataset. This is the official, risk-free curve widely used as the discount curve for bond valuation and as the benchmark for credit spreads.

**Also known as:** the Treasury yield curve, the risk-free curve.

**Args:**

- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to return the growth data or the actual data.
- <u>lag (int, optional):</u> The number of periods to lag the data by.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Notes:**

The underlying endpoint caps each request at 90 calendar days of data, so this method
paginates in 90-day windows to cover the full start_date to end_date range the class
was initialized with. A long range therefore issues many requests -- be mindful of
this on a Free plan's daily request limit and consider a narrower start_date where
possible.

The U.S. Department of the Treasury publishes these rates in percentage points (a
ten-year yield of 3.95%), but they are converted to decimals here (0.0395) so that
they match every other rate method in this module -- `get_euribor_rates`,
`get_european_central_bank_rates`, `get_federal_reserve_rates`,
`get_government_bond_yield` and the ICE BofA yield methods -- as well as the risk-free
rate returned by `Toolkit.get_treasury_data`. They can therefore be passed directly
into `get_present_value`, `get_z_spread`, `get_par_yield` and `get_key_rate_duration`,
each of which is documented as taking a rate in decimal form.

This changed in v2.2.0: prior versions returned percentage points from this one method
alone, which silently overstated a yield by a factor of 100 whenever the result was fed
into any of the bond-pricing methods above. Multiply by 100 to recover the published
Treasury figures.

**Returns:**

pd.DataFrame: A DataFrame containing the Treasury par yield curve rates, as decimals,
with one column per maturity.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome(
    start_date='2024-01-01',
    end_date='2024-01-15',
    api_key='FINANCIAL_MODELING_PREP_KEY',
)

fixedincome.get_treasury_rates()
```

Which returns:

| Date       |   1 Month |   3 Month |   1 Year |   2 Year |   10 Year |   30 Year |
|:-----------|----------:|----------:|---------:|---------:|----------:|----------:|
| 2024-01-02 |    0.0555 |    0.0546 |   0.048  |   0.0433 |    0.0395 |    0.0408 |
| 2024-01-03 |    0.0554 |    0.0548 |   0.0481 |   0.0433 |    0.0391 |    0.0405 |
| 2024-01-04 |    0.0556 |    0.0548 |   0.0485 |   0.0438 |    0.0399 |    0.0413 |
| 2024-01-05 |    0.0554 |    0.0547 |   0.0484 |   0.044  |    0.0405 |    0.0421 |


---

## get_ice_bofa_option_adjusted_spread
The ICE BofA Option-Adjusted Spreads (OASs) are the calculated spreads between a computed OAS index of all bonds in a given maturity and rating category and a spot Treasury curve. An OAS index is constructed using each constituent bond's OAS, weighted by market capitalization.

The Option-Adjusted Spread (OAS) is the spread relative to a risk-free interest rate, usually measured in basis points (bp), that equates the theoretical present value of a series of uncertain cash flows to the market price of a fixed-income investment. The spread is added to the risk-free rate to compensate for the uncertainty of the cash flows.

See definitions:

- Ratings: [https://fred.stlouisfed.org/series/BAMLC0A4CBBB](https://fred.stlouisfed.org/series/BAMLC0A4CBBB){:target="_blank"}
- Maturity: [https://fred.stlouisfed.org/series/BAMLC1A0C13Y](https://fred.stlouisfed.org/series/BAMLC1A0C13Y){:target="_blank"}

**Args:**

- <u>maturity (bool, optional):</u> Whether to return the maturity option adjusted spread or the rating option adjusted spread.
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. Defaults to False.

**Notes:**

ICE restricted the history it licenses to FRED in April 2026: every ICE BofA series now
carries only the most recent three years of observations. A start_date earlier than that
silently returns fewer rows rather than an error, and the example below will fall out of
range in time. Go to the ICE source directly for longer histories.

**Returns:**

pd.DataFrame: A DataFrame containing the Option Adjusted Spread, in basis points. The FRED
series are published in percent and are multiplied by 100 here, so a 0.77% spread is
returned as 77.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome(
    start_date='2024-01-01',
    end_date='2024-01-15',
)

fixedincome.get_ice_bofa_option_adjusted_spread()
```

Which returns:

| Date       |   1-3 Years |   3-5 Years |   5-7 Years |   7-10 Years |   10-15 Years |   15+ Years |
|:-----------|------------:|------------:|------------:|-------------:|--------------:|------------:|
| 2024-01-01 |          77 |          94 |       108.5 |          127 |         131.5 |         118 |
| 2024-01-02 |          78 |          95 |       109   |          128 |         133   |         119 |
| 2024-01-03 |          80 |          98 |       113   |          133 |         136   |         122 |
| 2024-01-04 |          80 |          98 |       112   |          133 |         135   |         122 |
| 2024-01-05 |          80 |          98 |       112   |          132 |         134   |         121 |
| 2024-01-08 |          79 |          98 |       112   |          132 |         134   |         120 |
| 2024-01-09 |          78 |          96 |       110   |          130 |         131   |         117 |
| 2024-01-10 |          77 |          94 |       108   |          128 |         128   |         113 |
| 2024-01-11 |          75 |          94 |       107   |          128 |         127   |         113 |
| 2024-01-12 |          74 |          94 |       107   |          128 |         126   |         112 |
| 2024-01-15 |          74 |          94 |       107   |          128 |         125   |         111 |


---

## get_ice_bofa_effective_yield
This data represents the effective yield of the ICE BofA Indices, When the last calendar day of the month takes place on the weekend, weekend observations will occur as a result of month ending accrued interest adjustments.

The effective yield of an ICE BofA index is the yield of the index as a whole, aggregated from the yields of its constituent bonds and weighted by their market capitalisation, on the same compounded (effective annual) basis that the accompanying Semi-Annual Yield to Worst series is quoted on a semi-annual basis. It is an index-level yield of the corporate bond market segment, not a statistic derived from any single bond's coupon - for the single-bond coupon-reinvestment calculation, see the "Effective Yield" row of `collect_bond_statistics` instead.

The FRED series are published in percent and are converted to decimals here, so a 5.40% BBB index yield is returned as 0.054.

See definitions:

- Ratings: [https://fred.stlouisfed.org/series/BAMLC0A4CBBBEY](https://fred.stlouisfed.org/series/BAMLC0A4CBBBEY){:target="_blank"}
- Maturity: [https://fred.stlouisfed.org/series/BAMLC1A0C13YEY](https://fred.stlouisfed.org/series/BAMLC1A0C13YEY){:target="_blank"}

**Also known as:** ICE BofA corporate bond yield, credit yield.

**Args:**

- <u>maturity (bool, optional):</u> Whether to return the maturity effective yield or the rating effective yield.
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. Defaults to False.

**Notes:**

ICE restricted the history it licenses to FRED in April 2026: every ICE BofA series now
carries only the most recent three years of observations. A start_date earlier than that
silently returns fewer rows rather than an error, and the example below will fall out of
range in time. Go to the ICE source directly for longer histories.

**Returns:**

pd.DataFrame: A DataFrame containing the ICE BofA Effective Yield

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome(
    start_date='2024-01-01',
    end_date='2024-01-15',
)

fixedincome.get_ice_bofa_effective_yield(maturity=False)
```

Which returns:

| Date       |    AAA |     AA |      A |    BBB |     BB |      B |    CCC |
|:-----------|-------:|-------:|-------:|-------:|-------:|-------:|-------:|
| 2024-01-01 | 0.0456 | 0.047  | 0.0505 | 0.054  | 0.0613 | 0.0752 | 0.1319 |
| 2024-01-02 | 0.0459 | 0.0473 | 0.0509 | 0.0543 | 0.0622 | 0.0763 | 0.1333 |
| 2024-01-03 | 0.0459 | 0.0474 | 0.051  | 0.0544 | 0.0634 | 0.0779 | 0.1358 |
| 2024-01-04 | 0.0466 | 0.0481 | 0.0518 | 0.0551 | 0.0639 | 0.0784 | 0.1367 |
| 2024-01-05 | 0.047  | 0.0485 | 0.0521 | 0.0554 | 0.0641 | 0.0787 | 0.137  |
| 2024-01-08 | 0.0465 | 0.0481 | 0.0517 | 0.055  | 0.0633 | 0.0776 | 0.1365 |
| 2024-01-09 | 0.0464 | 0.048  | 0.0516 | 0.0548 | 0.0629 | 0.0771 | 0.1359 |
| 2024-01-10 | 0.0464 | 0.048  | 0.0515 | 0.0547 | 0.0622 | 0.0762 | 0.1351 |
| 2024-01-11 | 0.0456 | 0.0472 | 0.0507 | 0.054  | 0.0619 | 0.076  | 0.1344 |
| 2024-01-12 | 0.0451 | 0.0467 | 0.0502 | 0.0534 | 0.0613 | 0.0753 | 0.1338 |
| 2024-01-15 | 0.0451 | 0.0467 | 0.0501 | 0.0533 | 0.0611 | 0.0751 | 0.1328 |


---

## get_ice_bofa_total_return
This data represents the total return of the ICE BofA Indices, When the last calendar day of the month takes place on the weekend, weekend observations will occur as a result of month ending accrued interest adjustments.

The total return is the actual rate of return of an investment or a pool of investments over a given evaluation period. Total return includes interest, capital gains, dividends and distributions realized over a given period of time.

See definitions:

- Ratings: [https://fred.stlouisfed.org/series/BAMLCC0A4BBBTRIV](https://fred.stlouisfed.org/series/BAMLCC0A4BBBTRIV){:target="_blank"}
- Maturity: [https://fred.stlouisfed.org/series/BAMLCC1A013YTRIV](https://fred.stlouisfed.org/series/BAMLCC1A013YTRIV){:target="_blank"}

**Args:**

- <u>maturity (bool, optional):</u> Whether to return the maturity total return or the rating total return.
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. Defaults to False.

**Notes:**

ICE restricted the history it licenses to FRED in April 2026: every ICE BofA series now
carries only the most recent three years of observations. A start_date earlier than that
silently returns fewer rows rather than an error, and the example below will fall out of
range in time. Go to the ICE source directly for longer histories.

**Returns:**

pd.DataFrame: A DataFrame containing the ICE BofA Total Return, as an index level rather
than a rate of return. It is not rescaled, since the FRED series' unit is already an index.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome(
    start_date='2024-01-01',
    end_date='2024-01-15',
)

fixedincome.get_ice_bofa_total_return(maturity=True)
```

Which returns:

| Date       |   1-3 Years |   3-5 Years |   5-7 Years |   7-10 Years |   10-15 Years |   15+ Years |
|:-----------|------------:|------------:|------------:|-------------:|--------------:|------------:|
| 2024-01-01 |     1913.78 |     2487.68 |      809.13 |      585.705 |       4206.25 |     4358.69 |
| 2024-01-02 |     1912.73 |     2484.25 |      807.62 |      584.32  |       4193.7  |     4343.71 |
| 2024-01-03 |     1912.18 |     2483.95 |      807.54 |      583.84  |       4194.39 |     4339.07 |
| 2024-01-04 |     1910.86 |     2477.9  |      804.35 |      580.42  |       4163.24 |     4289.24 |
| 2024-01-05 |     1910.86 |     2475.75 |      802.82 |      578.73  |       4148.31 |     4262.52 |
| 2024-01-08 |     1912.48 |     2480.39 |      804.97 |      580.71  |       4167.04 |     4302.16 |
| 2024-01-09 |     1913.5  |     2482.27 |      805.72 |      581.26  |       4173.04 |     4303.34 |
| 2024-01-10 |     1914.12 |     2483.6  |      806.21 |      581.29  |       4175.16 |     4304.82 |
| 2024-01-11 |     1918.28 |     2492.25 |      809.94 |      583.92  |       4200.49 |     4330.72 |
| 2024-01-12 |     1922.1  |     2498.89 |      812.41 |      585.2   |       4213.47 |     4338.43 |
| 2024-01-15 |     1922.67 |     2499.76 |      812.67 |      585.41  |       4215.34 |     4340.24 |


---

## get_ice_bofa_yield_to_worst
This data represents the semi-annual yield to worst of the ICE BofA Indices, When the last calendar day of the month takes place on the weekend, weekend observations will occur as a result of month ending accrued interest adjustments.

Yield to worst is the lowest potential yield that a bond can generate without the issuer defaulting. The standard US convention for this series is to use semi-annual coupon payments, whereas the standard in the foreign markets is to use coupon payments with frequencies of annual, semi-annual, quarterly, and monthly.

See definitions:

- Ratings: [https://fred.stlouisfed.org/series/BAMLC0A4CBBBSYTW](https://fred.stlouisfed.org/series/BAMLC0A4CBBBSYTW){:target="_blank"}
- Maturity: [https://fred.stlouisfed.org/series/BAMLC1A0C13YSYTW](https://fred.stlouisfed.org/series/BAMLC1A0C13YSYTW){:target="_blank"}

**Args:**

- <u>maturity (bool, optional):</u> Whether to return the maturity yield to worst or the rating yield to worst.
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. Defaults to False.

**Notes:**

ICE restricted the history it licenses to FRED in April 2026: every ICE BofA series now
carries only the most recent three years of observations. A start_date earlier than that
silently returns fewer rows rather than an error, and the example below will fall out of
range in time. Go to the ICE source directly for longer histories.

**Returns:**

pd.DataFrame: A DataFrame containing the ICE BofA Yield to Worst. The FRED series are
published in percent and are converted to decimals here, so 5.42% is returned as 0.0542.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome(
    start_date='2024-01-01',
    end_date='2024-01-15',
)

fixedincome.get_ice_bofa_yield_to_worst(maturity=False)
```

Which returns:

| Date       |    AAA |     AA |      A |    BBB |     BB |      B |    CCC |
|:-----------|-------:|-------:|-------:|-------:|-------:|-------:|-------:|
| 2024-01-01 | 0.0456 | 0.0472 | 0.0503 | 0.0542 | 0.0645 | 0.0786 | 0.1316 |
| 2024-01-02 | 0.046  | 0.0475 | 0.0506 | 0.0546 | 0.0652 | 0.0796 | 0.1329 |
| 2024-01-03 | 0.0461 | 0.0475 | 0.0507 | 0.0547 | 0.0662 | 0.081  | 0.1353 |
| 2024-01-04 | 0.0468 | 0.0483 | 0.0515 | 0.0554 | 0.0665 | 0.0814 | 0.136  |
| 2024-01-05 | 0.0471 | 0.0486 | 0.0518 | 0.0557 | 0.0667 | 0.0816 | 0.1362 |
| 2024-01-08 | 0.0466 | 0.0482 | 0.0514 | 0.0553 | 0.066  | 0.0806 | 0.1359 |
| 2024-01-09 | 0.0465 | 0.0481 | 0.0513 | 0.0551 | 0.0656 | 0.0803 | 0.1353 |
| 2024-01-10 | 0.0465 | 0.0481 | 0.0512 | 0.0551 | 0.065  | 0.0795 | 0.1345 |
| 2024-01-11 | 0.0458 | 0.0473 | 0.0504 | 0.0543 | 0.0648 | 0.0793 | 0.134  |
| 2024-01-12 | 0.0453 | 0.0468 | 0.0499 | 0.0537 | 0.0642 | 0.0786 | 0.1335 |
| 2024-01-15 | 0.0452 | 0.0468 | 0.0498 | 0.0537 | 0.064  | 0.0784 | 0.1325 |


---

## get_euribor_rates
Euribor rates, short for Euro Interbank Offered Rate, are the interest rates at which a panel of European banks lend funds to one another in the interbank market. These rates are published daily by the European Money Markets Institute (EMMI) and serve as a benchmark for various financial products and contracts, including mortgages, loans, and derivatives, across the Eurozone.

The Euribor rates are determined for different maturities, typically ranging from overnight to 12 months. The most common maturities are 1 month, 3 months, 6 months, and 12 months. Each maturity represents the time period for which the funds are borrowed, with longer maturities generally implying higher interest rates due to increased uncertainty and risk over longer time horizons.

For more information, see for example: [https://data.ecb.europa.eu/data/datasets/FM/FM.M.U2.EUR.RT.MM.EURIBOR6MD_.HSTA](https://data.ecb.europa.eu/data/datasets/FM/FM.M.U2.EUR.RT.MM.EURIBOR6MD_.HSTA){:target="_blank"}

**Also known as:** euro interbank offered rate, eurozone money market.

**Args:**

- <u>maturities (str \| list \| None, optional):</u> Maturities for which to retrieve rates. Defaults to None.
When set to None, it will retrieve rates for 1 month, 3 months, 6 months, and 12 months.
- <u>nominal (bool, optional):</u> Whether to retrieve the nominal Euribor fixings or their real
(inflation-adjusted) counterpart. The ECB only publishes a real Euribor for the 3-month
maturity, so nominal=False returns that maturity alone and warns about any others that
were requested rather than silently answering them with a nominal rate. Defaults to True.
- <u>rounding (int \| None, optional):</u> Rounding precision for the rates. Defaults to None.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. Defaults to False.

**Returns:**

pandas.DataFrame: DataFrame containing the Euribor rates for the specified maturities.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome(start_date='2023-12-01')

euribor_rates = fixedincome.get_euribor_rates()
```

Which returns:

|         |   1-Month |   3-Month |   6-Month |   12-Month |
|:--------|----------:|----------:|----------:|-----------:|
| 2023-12 |    0.0386 |    0.0393 |    0.0392 |     0.0367 |
| 2024-01 |    0.0387 |    0.0393 |    0.0389 |     0.0361 |
| 2024-02 |    0.0387 |    0.0392 |    0.039  |     0.0367 |
| 2024-03 |    0.0385 |    0.0392 |    0.0389 |     0.0372 |


---

## get_european_central_bank_rates
The Governing Council of the ECB sets the key interest rates for the euro area. The available rates are:

- Main refinancing operations (refinancing)
- Marginal lending facility (lending)
- Deposit facility (deposit)

The main refinancing operations (MRO) rate is the interest rate banks pay when they borrow money from the ECB for one week. When they do this, they have to provide collateral to guarantee that the money will be paid back.

The marginal lending facility rate is the interest rate banks pay when they borrow from the ECB overnight. When they do this, they have to provide collateral, for example securities, to guarantee that the money will be paid back.

The deposit facility rate is one of the three interest rates the ECB sets every six weeks as part of its monetary policy. The rate defines the interest banks receive for depositing money with the central bank overnight.

See source: [https://data.ecb.europa.eu/main-figures/](https://data.ecb.europa.eu/main-figures/){:target="_blank"}

**Also known as:** ECB rates, deposit facility rate.

**Args:**

- <u>rate (str, optional):</u> The rate to return. Defaults to None, which returns all rates.
Choose between 'refinancing', 'lending' or 'deposit'.
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. Defaults to False.

**Returns:**

pd.DataFrame: A DataFrame containing the ECB rates.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome(start_date='2023-12-01')

fixedincome.get_european_central_bank_rates()
```

Which returns:

|            |   Refinancing |   Lending |   Deposit |
|:-----------|--------------:|----------:|----------:|
| 2023-12-01 |         0.045 |    0.0475 |      0.04 |
| 2023-12-02 |         0.045 |    0.0475 |      0.04 |
| 2023-12-03 |         0.045 |    0.0475 |      0.04 |
| 2023-12-04 |         0.045 |    0.0475 |      0.04 |
| 2023-12-05 |         0.045 |    0.0475 |      0.04 |
| 2023-12-06 |         0.045 |    0.0475 |      0.04 |
| 2023-12-07 |         0.045 |    0.0475 |      0.04 |
| 2023-12-08 |         0.045 |    0.0475 |      0.04 |
| 2023-12-09 |         0.045 |    0.0475 |      0.04 |
| 2023-12-10 |         0.045 |    0.0475 |      0.04 |
| 2023-12-11 |         0.045 |    0.0475 |      0.04 |
| 2023-12-12 |         0.045 |    0.0475 |      0.04 |
| 2023-12-13 |         0.045 |    0.0475 |      0.04 |
| 2023-12-14 |         0.045 |    0.0475 |      0.04 |
| 2023-12-15 |         0.045 |    0.0475 |      0.04 |
| 2023-12-16 |         0.045 |    0.0475 |      0.04 |
| 2023-12-17 |         0.045 |    0.0475 |      0.04 |
| 2023-12-18 |         0.045 |    0.0475 |      0.04 |


---

## get_federal_reserve_rates
Get the Federal Reserve rates as published by the Federal Reserve Bank of New York. The federal funds market consists of domestic unsecured borrowings in U.S. dollars by depository institutions from other depository institutions and certain other entities, primarily government-sponsored enterprises.

The following rates are available:

- Effective Federal Funds Rate (EFFR)
- Overnight Bank Funding Rate (OBFR)
- Tri-Party General Collateral Rate (TGCR)
- Broad General Collateral Rate (BGCR)
- Secured Overnight Financing Rate (SOFR)

The effective federal funds rate (EFFR) is calculated as a volume-weighted median of overnight federal funds transactions reported in the FR 2420 Report of Selected Money Market Rates.

The overnight bank funding rate (OBFR) is calculated as a volume-weighted median of overnight federal funds transactions, Eurodollar transactions, and the domestic deposits reported as “Selected Deposits” in the FR 2420 Report.

The TGCR is calculated as a volume-weighted median of transaction-level tri-party repo data collected from the Bank of New York Mellon.

The BGCR is calculated as a volume-weighted median of transaction-level tri-party repo data collected from the Bank of New York Mellon as well as GCF Repo transaction data obtained from the U.S. Department of the Treasury's Office of Financial Research (OFR).

The SOFR is calculated as a volume-weighted median of transaction-level tri-party repo data collected from the Bank of New York Mellon as well as GCF Repo transaction data and data on bilateral Treasury repo transactions cleared through FICC's DVP service, which are obtained from the U.S. Department of the Treasury's Office of Financial Research (OFR).

The New York Fed publishes the rates for the prior business day on the New York Fed's website between 8:00 and 9:00 a.m.

See source: [https://www.newyorkfed.org/markets/reference-rates/](https://www.newyorkfed.org/markets/reference-rates/){:target="_blank"}

**Also known as:** Fed rates, federal funds rate, FOMC rate.

**Args:**

- <u>rate (str):</u> The rate to return. Defaults to 'EFFR' (Effective Federal Funds Rate).
- <u>rounding (int \| None, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. Defaults to False.

**Returns:**

pd.DataFrame: A DataFrame containing the Federal Reserve rates including the rate,
percentiles, volume and upper and lower bounds.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome(start_date='2023-12-01')

effr = fixedincome.get_federal_reserve_rates()

effr.loc[:, ['Rate', '1st Percentile', '25th Percentile', '75th Percentile', '99th Percentile']]
```

Which returns:

| Effective Date   |   Rate |   1st Percentile |   25th Percentile |   75th Percentile |   99th Percentile |
|:-----------------|-------:|-----------------:|------------------:|------------------:|------------------:|
| 2023-12-01       | 0.0533 |            0.053 |            0.0532 |            0.0533 |            0.0544 |
| 2023-12-04       | 0.0533 |            0.053 |            0.0532 |            0.0533 |            0.0545 |
| 2023-12-05       | 0.0533 |            0.053 |            0.0532 |            0.0533 |            0.0545 |
| 2023-12-06       | 0.0533 |            0.053 |            0.0532 |            0.0533 |            0.0545 |
| 2023-12-07       | 0.0533 |            0.053 |            0.0531 |            0.0534 |            0.0545 |
| 2023-12-08       | 0.0533 |            0.053 |            0.0532 |            0.0533 |            0.0545 |
| 2023-12-11       | 0.0533 |            0.053 |            0.0532 |            0.0533 |            0.0545 |
| 2023-12-12       | 0.0533 |            0.053 |            0.0531 |            0.0533 |            0.0544 |
| 2023-12-13       | 0.0533 |            0.053 |            0.0531 |            0.0533 |            0.0545 |
| 2023-12-14       | 0.0533 |            0.053 |            0.0531 |            0.0533 |            0.0535 |


---

