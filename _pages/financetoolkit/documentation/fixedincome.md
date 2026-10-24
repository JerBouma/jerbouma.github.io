---
title: Fixed Income
seo_title: "Fixed Income Module | Finance Toolkit"
seo_title_suffix: false
excerpt: The Fixed Income module contains a wide variety of fixed income related calculations such as the Effective Yield, the Macaulay Duration, the Modified Duration Convexity, the Yield to Maturity and models such as Black and Bachelier to valuate derivative instruments such as Swaptions.
description: "Reference for every function and parameter in the Finance Toolkit's Fixed Income module: yield, duration, convexity, Black and Bachelier models."
author_profile: false
permalink: /projects/financetoolkit/docs/fixedincome
classes: wide-sidebar
layout: single
redirect_from:
    - /fixedincome
    - /projects/financetoolkit/fixed-income-notebook
sidebar:
    nav: "financetoolkit-docs-fixedincome"
---

The Fixed Income module covers a wide variety of calculations including the Effective Yield, Macaulay Duration, Modified Duration, Convexity, Yield to Maturity and derivative pricing models such as Black and Bachelier (used for Swaptions and other instruments).

Use it in Claude, ChatGPT or another AI assistant through the [Finance Toolkit MCP](/projects/financetoolkit/mcp), or install the Python package:

```python
pip install financetoolkit -U
```

{% include algolia.html %}

{% include financetoolkit-getting-started/fixed-income.md %}

## collect_bond_statistics
Collect the bond statistics for a given bond which includes the following fields:

- Par Value: The face value of the bond.
- Coupon Rate: The annual coupon rate (in decimal).
- Years to Maturity: The number of years until the bond matures.
- Yield to Maturity: The yield to maturity of the bond (in decimal).
- Frequency: The number of coupon payments per year.
- Present Value: The present value of the bond.
- Current Yield: The annual coupon payment divided by the bond price.
- Effective Yield: The annualised yield that accounts for the compounding of the coupon payments made within the year.
- Macaulay's Duration: The weighted average time to receive the bond's cash flows.
- Modified Duration: The Macaulay's duration divided by 1 plus the per-period yield (yield to maturity divided by the frequency).
- Effective Duration: The percentage price change per unit change in yield, obtained by repricing the bond symmetrically 1% above and 1% below the current yield.
- Dollar Duration: The modified duration multiplied by the bond price, divided by 100.
- DV01: The currency change in the bond's price, per par value of face, for a one basis point (0.01%) change in the yield to maturity.
- Convexity: The second derivative of the bond price with respect to the yield to maturity.

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

fixedincome = FixedIncome(end_date="2025-12-31")

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

|                     |        0 |
|:--------------------|---------:|
| Par Value           | 100      |
| Coupon Rate         |   0.05   |
| Years to Maturity   |   5      |
| Yield to Maturity   |   0.08   |
| Frequency           |   1      |
| Present Value       |  88.0219 |
| Current Yield       |   0.0568 |
| Effective Yield     |   0.05   |
| Macaulay's Duration |   4.5116 |
| Modified Duration   |   4.1774 |
| Effective Duration  |   4.1798 |
| Dollar Duration     |   3.677  |
| DV01                |   0.0368 |
| Convexity           |  22.4017 |

Note how the effective duration sits just above the modified duration for every
bond: the two measure the same sensitivity, and their small difference is exactly
the convexity picked up by repricing over a 100 basis point shift rather than
differentiating at a point.

---

## get_present_value
Calculates the bond prices for different coupon rates and years to maturity. The bond price is the present value of the bond's future cash flows, which includes the coupon payments and the par value of the bond at maturity. The bond price is calculated using the following formula:

$$
\text{Bond Price} = (C / r) \cdot (1 - (1 + r) ^{-n}) + F / (1 + r) ^{n}
$$

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

fixedincome = FixedIncome(end_date="2025-12-31")

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

fixedincome = FixedIncome(end_date="2025-12-31")

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

$$
\text{Bond Price} = (C / r) \cdot (1 - (1 + r) ^{-n}) + F / (1 + r) ^{n}
$$

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

fixedincome = FixedIncome(end_date="2025-12-31")

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

$$
\text{Forward Rate} = ((1 + r_{2}) ^{t_{2}} / (1 + r_{1}) ^{t_{1}}) ^{1 / (t_{2} - t_{1})} - 1
$$

where:

- r1 = Spot rate at the near maturity
- t1 = Near maturity, in years
- r2 = Spot rate at the far maturity
- t2 = Far maturity, in years

**Also known as:** implied forward rate, forward-forward rate.

**Args:**

- <u>spot_rates (pd.Series &#124; dict, optional):</u> The zero-coupon (spot) yield curve,
indexed by maturity in years (in decimal). Defaults to a sample curve.
- <u>near_maturity (float &#124; list, optional):</u> The nearer maturity (or maturities),
in years. If not provided, a range of near maturities will be used.
- <u>far_maturity (float &#124; list, optional):</u> The further maturity (or maturities),
in years. If not provided, a range of far maturities will be used.
- <u>show_input_info (bool, optional):</u> Whether to display input information. Defaults to True.

**Returns:**

pandas.DataFrame: A DataFrame containing the forward rate for each combination
of near and far maturity. Combinations where the far maturity is not greater
than the near maturity are returned as NaN.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome(end_date="2025-12-31")

fixedincome.get_forward_rate(
    near_maturity=[1, 2, 3],
    far_maturity=[5, 10],
    show_input_info=False,
)
```

Which returns:

|   Near Maturity |     5 |     10 |
|----------------:|------:|-------:|
|               1 | 0.04  | 0.0456 |
|               2 | 0.042 | 0.047  |
|               3 | 0.044 | 0.0483 |

---

## get_par_yield
Calculates the par yield curve implied by a zero-coupon (spot) yield curve. The par yield for a given maturity is the coupon rate that would need to be attached to a newly-issued bond of that maturity so that, once its cash flows are discounted with the spot curve, its price equals its par value exactly.

This is the curve that is typically quoted for on-the-run government bonds, as opposed to the theoretical spot curve which is usually bootstrapped rather than directly observed.

The par yield is calculated using the following formula:

$$
\text{Par Yield} = \text{frequency} \cdot (1 - \operatorname{DF}(n)) / \operatorname{SUM}(\operatorname{DF}(k))
$$

where DF(k) = 1 / (1 + spot_rate(k / frequency) / frequency)^k is the discount factor for the cash flow at period k, spot_rate(t) is obtained by interpolating the spot curve at time t (in years), and n = years_to_maturity * frequency is the number of coupon periods.

**Also known as:** par rate, par coupon rate.

**Args:**

- <u>spot_rates (pd.Series &#124; dict, optional):</u> The zero-coupon (spot) yield curve,
indexed by maturity in years (in decimal). Defaults to a sample curve.
- <u>years_to_maturity (float &#124; list, optional):</u> The maturity (or maturities), in
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

fixedincome = FixedIncome(end_date="2025-12-31")

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

$$
\text{Yield Curve Spread} = \text{Long-Term Yield} - \text{Short-Term Yield}
$$

**Also known as:** term spread, yield curve slope.

**Args:**

- <u>spot_rates (pd.Series &#124; dict, optional):</u> The yield curve, indexed by
maturity in years (in decimal). Defaults to a sample curve.
- <u>long_maturity (float &#124; list, optional):</u> The longer maturity (or maturities),
in years. If not provided, a range of long maturities will be used.
- <u>short_maturity (float &#124; list, optional):</u> The shorter maturity (or
maturities), in years. If not provided, a range of short maturities
will be used.
- <u>show_input_info (bool, optional):</u> Whether to display input information. Defaults to True.

**Returns:**

pandas.DataFrame: A DataFrame containing the yield curve spread for each
combination of long and short maturity.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome(end_date="2025-12-31")

fixedincome.get_yield_curve_spread(
    long_maturity=[10, 30],
    short_maturity=[1, 2],
    show_input_info=False,
)
```

Which returns:

|   Long Maturity |     1 |     2 |
|----------------:|------:|------:|
|              10 | 0.014 | 0.012 |
|              30 | 0.02  | 0.018 |

---

## get_breakeven_inflation_rate
Calculates the breakeven inflation rate implied by a nominal and a real (inflation-protected) yield curve, e.g. the U.S. Treasury nominal curve versus the TIPS (Treasury Inflation-Protected Securities) curve. It is the rate of inflation that would make an investor indifferent between holding a nominal bond and an inflation-protected bond of the same maturity, and is widely used as a market-implied measure of expected inflation.

The rate for each maturity is obtained by linearly interpolating the supplied curves, so `maturity` does not need to coincide exactly with a maturity present in `nominal_rates` or `real_rates`.

The breakeven inflation rate is calculated using the following formula:

$$
\text{Breakeven Inflation Rate} = \text{Nominal Yield} - \text{Real Yield}
$$

**Also known as:** TIPS breakeven spread, inflation breakeven.

**Args:**

- <u>nominal_rates (pd.Series &#124; dict, optional):</u> The nominal (non-inflation-protected)
yield curve, indexed by maturity in years (in decimal). Defaults to a sample curve.
- <u>real_rates (pd.Series &#124; dict, optional):</u> The real (inflation-protected) yield
curve, indexed by maturity in years (in decimal). Defaults to a sample curve.
- <u>maturity (float &#124; list, optional):</u> The maturity (or maturities), in years,
to calculate the breakeven inflation rate for. If not provided, a range
of maturities will be used.
- <u>show_input_info (bool, optional):</u> Whether to display input information. Defaults to True.

**Returns:**

pandas.Series: A Series containing the breakeven inflation rate for each
requested maturity, i.e. the breakeven inflation curve.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome(end_date="2025-12-31")

fixedincome.get_breakeven_inflation_rate(
    maturity=[1, 5, 10, 30],
    show_input_info=False,
)
```

Which returns:

|   Maturity |   Breakeven Inflation Rate |
|-----------:|---------------------------:|
|          1 |                      0.022 |
|          5 |                      0.026 |
|         10 |                      0.028 |
|         30 |                      0.03  |

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
- <u>spot_rates (pd.Series &#124; dict, optional):</u> The benchmark zero-coupon (spot)
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

fixedincome = FixedIncome(end_date="2025-12-31")

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
|           95 | 0.0243 | 0.0137 | 0.0103 |
|          100 | 0.0124 | 0.007  | 0.0053 |
|          105 | 0.0012 | 0.0007 | 0.0005 |

---

## get_bond_equivalent_yield
Converts a money-market discount yield (e.g. quoted for Treasury bills) into a bond-equivalent yield (BEY). Money-market instruments are often quoted on a discount-yield basis, which understates the actual return an investor earns because it is computed on face value rather than the (lower) purchase price, and uses a 360-day rather than a 365-day year. The bond-equivalent yield restates the discount yield on a basis that is comparable to coupon-bearing bonds and notes.

The bond-equivalent yield is calculated using the following formula:

$$
\text{BEY} = 365 \cdot \text{Discount Yield} / (360 - \text{Days to Maturity} \cdot \text{Discount Yield})
$$

for a bill with half a year or less remaining. Beyond that an equivalent coupon-bearing note would have paid a coupon at the six month point, so the U.S. Treasury's semi-annually compounded solution (31 CFR 356, Appendix B) is used instead - see `bond_model.get_bond_equivalent_yield`. Applying the simple formula to a 52-week bill instead overstates its yield by roughly seven basis points.

**Also known as:** BEY, coupon-equivalent yield, investment rate.

**Args:**

- <u>discount_yield (float &#124; list, optional):</u> The money-market discount yield of
the instrument (in decimal). If not provided, a range of discount yields
will be used.
- <u>days_to_maturity (float &#124; list, optional):</u> The number of days until the
instrument matures. If not provided, a range of typical T-bill maturities
will be used.
- <u>show_input_info (bool, optional):</u> Whether to display input information. Defaults to True.

**Returns:**

pandas.DataFrame: A DataFrame containing the bond-equivalent yield for
different discount yields and days to maturity.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome(end_date="2025-12-31")

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
- <u>years_to_maturity (float &#124; list, optional):</u> The years to maturity of the
bond (or bonds). If not provided, a range of years to maturity will be used.
- <u>spot_rates (pd.Series &#124; dict, optional):</u> The zero-coupon (spot) yield curve
used to discount the bond's cash flows, indexed by maturity in years (in
decimal). Defaults to a sample curve.
- <u>key_rate_maturity (float &#124; list, optional):</u> The maturity (or maturities), in
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

fixedincome = FixedIncome(end_date="2025-12-31")

fixedincome.get_key_rate_duration(
    coupon_rate=0.05,
    years_to_maturity=[5, 10],
    key_rate_maturity=[2, 5, 10],
    show_input_info=False,
)
```

Which returns:

|   Years to Maturity |      2 |      5 |      10 |
|--------------------:|-------:|-------:|--------:|
|                   5 | 0.0862 | 4.0561 | -0      |
|                  10 | 0.0862 | 0.377  |  6.4666 |

---

## get_taylor_price_change
Estimates the percentage change in a bond's price for a given change in yield, using a second-order Taylor series expansion that combines modified duration and convexity.

Modified duration alone only captures the first-order (linear) relationship between a bond's price and its yield, which understates the price increase for a yield decrease and overstates the price decrease for a yield increase because the true price-yield relationship is curved (convex), not linear. Adding a convexity term corrects for this and produces a substantially more accurate estimate, especially for larger yield changes.

This method calls `get_modified_duration` and `get_convexity` from `bond_model.py` directly rather than recomputing them.

The Taylor approximation is calculated using the following formula:

$$
\%\Delta \;\text{Price} \approx - \text{Modified Duration} \cdot \Delta y + 0.5 \cdot \text{Convexity} \cdot \Delta y ^{2}
$$

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

fixedincome = FixedIncome(end_date="2025-12-31")

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
|          0.03 | -0.0421 | -0.0744 | -0.097  |
|          0.05 | -0.0407 | -0.0693 | -0.088  |
|          0.07 | -0.0394 | -0.0656 | -0.0824 |

---

## get_derivative_price
Calculates the derivative price for a fixed income instrument.

It is possible to use two different models to calculate the derivative price:

- Black Model: A mathematical model used for pricing financial derivatives, its primary applications are for pricing options on future contracts, bond options, interest rate cap and floors, and swaptions. For more information, see: [https://en.wikipedia.org/wiki/Black_model](https://en.wikipedia.org/wiki/Black_model){:target="_blank"}
- Bachelier Model: A deviation of the Black Model that is used for pricing future contracts. It is a simple model that assumes the price of the underlying asset follows a normal distribution with constant volatility. This is in contrast to the Black Model which assumes the price of the underlying asset follows a log-normal distribution. For more information, see: [https://en.wikipedia.org/wiki/Bachelier_model](https://en.wikipedia.org/wiki/Bachelier_model){:target="_blank"}

It is possible to alter all parameters within the models, e.g. strike rate, volatility, years to maturity, risk-free rate, notional amount, and whether the holder is the receiver or payer of the derivative. Next to that, you can provide lists of values for the fixed rate, strike rate, volatility, and years to maturity to calculate the derivative price for multiple scenarios outside of the standard sample.

Exercising a swaption is not a single payment at expiration - it is the right to enter a swap that exchanges cash flows at every payment date over the underlying swap's tenor. The price therefore discounts the option payoff by the swap's annuity (present value of a basis point) rather than a single discount factor to expiration, which is why the tenor and payment frequency of the underlying swap matter.

Note that a swaption's price scales with the tenor of the underlying swap (a right to enter a longer-dated swap is worth more, since it exchanges cash flows over more payment dates) - pass `tenor` explicitly to price a swaption whose underlying swap tenor differs from its years to maturity, e.g. a 1-year option into a 5-year swap: `tenor=5, years_to_maturity=1`.

The two models do not quote volatility on the same basis, and this matters a great deal. Black's model, being lognormal, reads `volatility` as a fraction of the forward rate, so 0.20 is a 20% volatility. The Bachelier model, being normal, reads it as an absolute movement in rate units, so 0.0065 is 65 basis points. On a 3.25% forward those two quotes describe the same market, but swapping one for the other misprices the swaption by a factor of roughly thirty. By default `volatility` is therefore interpreted on whichever basis the chosen model is defined in; set `volatility_type` explicitly to supply a quote on the other basis and have it converted, using the at-the-money approximation sigma_normal ≈ sigma_lognormal * forward_rate.

Black's model is undefined at a zero or negative forward or strike rate because it takes the logarithm of their ratio, and raises rather than returning a silent NaN in that case. Use the Bachelier model for the negative rates seen in the euro area and Japan.

**Also known as:** bond derivative pricing, fixed income derivative, swaption pricing.

**Args:**

- <u>model (str, optional):</u> The type of model to use for calculating the derivative price. Defaults to "black".
- <u>forward_rate (float, optional):</u> The forward rate as derived from the swap curve. Defaults to 0.05.
- <u>strike_rate (float &#124; list, optional):</u> The strike rate for the derivative. Defaults to None which means it calculates the
derivative price a range of strike prices. Can also be a list of strike rates (e.g. [0.01, 0.02, 0.03, 0.04, 0.05]).
- <u>volatility (float, optional):</u> The volatility of the underlying swap rate, quoted on the
basis given by `volatility_type`. Defaults to 0.01, read as a 1% lognormal volatility
by the Black model and as 100 basis points of normal volatility by the Bachelier model.
- <u>years_to_maturity (float &#124; list, optional):</u> The years to maturity of the derivative in years. Defaults to None which means it plots
the derivative price for the next 10 years. Can also be a list of years to maturity (e.g. [1, 2.3, 2.5, 3])
- <u>risk_free_rate (float, optional):</u> The risk-free interest rate. Defaults to None which means it is equal to the fixed rate.
- <u>notional (float, optional):</u> The notional amount of the derivative. Defaults to 10_000_000.
- <u>tenor (float &#124; None, optional):</u> The tenor (length in years) of the underlying swap. Defaults to None,
which means it is equal to years_to_maturity for each scenario.
- <u>payment_frequency (int, optional):</u> Number of fixed-leg payments per year on the underlying swap
(e.g. 1 for annual, 2 for semi-annual, 4 for quarterly). Defaults to 2 (semi-annual).
- <u>is_receiver (bool, optional):</u> True if the holder is the receiver of the derivative, False if the holder is the payer. Defaults to True.
- <u>volatility_type (str &#124; None, optional):</u> The convention `volatility` is quoted on, either
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

fixedincome = FixedIncome(end_date="2025-12-31")

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
Get the government bond yield for a variety of countries over time from the OECD. By default this is the long-term (10-year) government bond yield; set short_term=True to get the short-term (3-month) rate instead. The two maturities are described below.

Long-term (short_term=False): long-term interest rates refer to government bonds maturing in ten years. Rates are mainly determined by the price charged by the lender, the risk from the borrower and the fall in the capital value. Long-term interest rates are generally averages of daily rates, measured as a percentage. These interest rates are implied by the prices at which the government bonds are traded on financial markets, not the interest rates at which the loans were issued.

In all cases, they refer to bonds whose capital repayment is guaranteed by governments. Long-term interest rates are one of the determinants of business investment. Low long term interest rates encourage investment in new equipment and high interest rates discourage it. Investment is, in turn, a major source of economic growth.

**See definition:** [https://data.oecd.org/interest/long-term-interest-rates.htm](https://data.oecd.org/interest/long-term-interest-rates.htm){:target="_blank"}

Short-term (short_term=True): short-term interest rates are the rates at which short-term borrowings are effected between financial institutions or the rate at which short-term government paper is issued or traded in the market. Short-term interest rates are generally averages of daily rates, measured as a percentage. They are based on three-month money market rates where available; the OECD source specifically returns the 3-month interbank offered rate rather than a government bill yield, so for most countries it tracks the central bank's policy rate closely.

**See definition:** [https://data.oecd.org/interest/short-term-interest-rates.htm](https://data.oecd.org/interest/short-term-interest-rates.htm){:target="_blank"}

**Also known as:** treasury yield, bond yield by maturity.

**Args:**

- <u>short_term (bool, optional):</u> Whether to return the short-term interest rate. Defaults to False.
This means that the long-term interest rate will be returned.
- <u>period (str &#124; None, optional):</u> Whether to return the monthly, quarterly or the annual data.
- <u>growth (bool, optional):</u> Whether to return the growth data or the actual data.
- <u>lag (int, optional):</u> The number of periods to lag the data by.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.DataFrame: A DataFrame containing the long-term (10-year) government bond yield, or the
short-term (3-month) interest rate when short_term=True.

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
| 2023-12 |  0.0062 |          0.0402 |   0.0655 |

---

## get_government_bond_yield_curve
Retrieves the government bond yield curve of a variety of countries, every maturity a country's government borrows at, from treasury bills to bonds of 30 years and more. The yield curve is the basis for discounting cash flows and pricing bonds, and its shape is one of the most watched signals in markets: an inverted curve, with short rates above long rates, has preceded most recessions.

Every curve comes from the official source without an API key:

- United States: the U.S. Department of the Treasury's par yield curve, 1 month to 30 years, from 1990.
- Euro Area: the yield curve the European Central Bank estimates from the bonds of all euro area central governments, 3 months to 30 years, from 2004.
- Germany: the term structure the Deutsche Bundesbank estimates from listed federal securities, 1 to 30 years.
- United Kingdom: the Bank of England's nominal par yields of gilts, 5, 10 and 20 years.
- Japan: the Ministry of Finance's Japanese government bond yields, 1 to 40 years, from 1974.
- Canada: the Bank of Canada's treasury bill yields (1 month to 1 year, weekly) and benchmark bond yields (2 to 30 years).
- Sweden: the Riksbank's treasury bill and government bond yields, 1 month to 10 years.
- Norway: Norges Bank's generic government bond yields, 3 to 10 years.
- Australia: the Reserve Bank of Australia's government bond yields interpolated to 2, 3, 5 and 10 years, from 2013.

With period="monthly", every other European Union member, such as France, Italy, Spain, the Netherlands and Poland, is included with its 10-year yield, the long-term interest rate for convergence purposes the ECB publishes monthly. For other countries no official source publishes a curve without a key; see `get_government_bond_yield` for the monthly 3-month and 10-year rates of around forty countries from the OECD. Only the requested countries are retrieved, and only the days that are not cached yet.

The yields are returned as decimal fractions per annum (0.0419 for 4.19%), with one column per country and maturity, sorted from the shortest to the longest maturity. Weekly and monthly periods take the yields on the last trading day of each period (weeks end on Friday).

**Also known as:** yield curve, term structure of interest rates, sovereign curve, treasury curve, bund curve, gilt curve, JGB curve.

**Args:**

- <u>countries (list[str] &#124; str &#124; None, optional):</u> The countries to retrieve, from
"United States", "Euro Area", "Germany", "United Kingdom", "Japan", "Canada",
"Sweden", "Norway" and "Australia", and with period="monthly" any European
Union member.
Defaults to None, which retrieves every country.
- <u>period (str, optional):</u> Whether to return the daily, weekly or monthly data.
Defaults to "daily".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to return the growth data or the actual data.
- <u>lag (int, optional):</u> The number of periods to lag the data by.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.DataFrame: A DataFrame with the yields as decimals, indexed by date with a
column per country and maturity.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome(start_date='2026-09-28', end_date='2026-10-01')

yield_curve = fixedincome.get_government_bond_yield_curve(
    countries=['United States', 'Germany']
)

yield_curve['Germany'][['1Y', '2Y', '5Y', '10Y', '20Y', '30Y']]
```

Which returns:

|            |     1Y |     2Y |     5Y |    10Y |    20Y |    30Y |
|:-----------|-------:|-------:|-------:|-------:|-------:|-------:|
| 2026-09-28 | 0.031  | 0.0332 | 0.0344 | 0.0369 | 0.0393 | 0.0401 |
| 2026-09-29 | 0.0307 | 0.0329 | 0.0341 | 0.0368 | 0.0394 | 0.0403 |
| 2026-09-30 | 0.0304 | 0.0324 | 0.0336 | 0.0364 | 0.039  | 0.0399 |
| 2026-10-01 | 0.0302 | 0.0321 | 0.0335 | 0.0366 | 0.0394 | 0.0403 |

---

## get_treasury_rates
Retrieves the daily U.S. Treasury par yield curve rates as officially published by the U.S. Department of the Treasury, covering every maturity from 1 Month through 30 Year in a single dataset. This is the official, risk-free curve widely used as the discount curve for bond valuation and as the benchmark for credit spreads.

No API key is needed: with a FinancialModelingPrep API key the rates come from FinancialModelingPrep, and without one, or when the key's plan does not include them, from the U.S. Department of the Treasury directly, which gives the same figures.

**Also known as:** the Treasury yield curve, the risk-free curve.

**Args:**

- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.
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

fixedincome = FixedIncome(start_date='2024-01-01', end_date='2024-01-15')

fixedincome.get_treasury_rates()
```

Which returns:

| Date       |   1 Month |   2 Month |   3 Month |   6 Month |   1 Year |   2 Year |   3 Year |   5 Year |   7 Year |   10 Year |   20 Year |   30 Year |
|:-----------|----------:|----------:|----------:|----------:|---------:|---------:|---------:|---------:|---------:|----------:|----------:|----------:|
| 2024-01-02 |    0.0555 |    0.0554 |    0.0546 |    0.0524 |   0.048  |   0.0433 |   0.0409 |   0.0393 |   0.0395 |    0.0395 |    0.0425 |    0.0408 |
| 2024-01-03 |    0.0554 |    0.0554 |    0.0548 |    0.0525 |   0.0481 |   0.0433 |   0.0407 |   0.039  |   0.0392 |    0.0391 |    0.0421 |    0.0405 |
| 2024-01-04 |    0.0556 |    0.0548 |    0.0548 |    0.0525 |   0.0485 |   0.0438 |   0.0414 |   0.0397 |   0.0399 |    0.0399 |    0.043  |    0.0413 |
| 2024-01-05 |    0.0554 |    0.0548 |    0.0547 |    0.0524 |   0.0484 |   0.044  |   0.0417 |   0.0402 |   0.0404 |    0.0405 |    0.0437 |    0.0421 |
| 2024-01-08 |    0.0554 |    0.0548 |    0.0549 |    0.0524 |   0.0482 |   0.0436 |   0.0411 |   0.0397 |   0.0399 |    0.0401 |    0.0433 |    0.0417 |
| 2024-01-09 |    0.0553 |    0.0546 |    0.0547 |    0.0524 |   0.0482 |   0.0436 |   0.0409 |   0.0397 |   0.04   |    0.0402 |    0.0433 |    0.0418 |
| 2024-01-10 |    0.0553 |    0.0546 |    0.0546 |    0.0523 |   0.0482 |   0.0437 |   0.041  |   0.0399 |   0.0401 |    0.0404 |    0.0435 |    0.042  |
| 2024-01-11 |    0.0554 |    0.0547 |    0.0546 |    0.0522 |   0.0475 |   0.0426 |   0.0402 |   0.039  |   0.0395 |    0.0398 |    0.0432 |    0.0418 |
| 2024-01-12 |    0.0555 |    0.0547 |    0.0545 |    0.0516 |   0.0465 |   0.0414 |   0.0392 |   0.0384 |   0.0391 |    0.0396 |    0.0432 |    0.042  |

---

## get_ice_bofa_option_adjusted_spread
The ICE BofA Option-Adjusted Spreads (OASs) are the calculated spreads between a computed OAS index of all bonds in a given maturity and rating category and a spot Treasury curve. An OAS index is constructed using each constituent bond's OAS, weighted by market capitalization.

The Option-Adjusted Spread (OAS) is the spread relative to a risk-free interest rate, usually measured in basis points (bp), that equates the theoretical present value of a series of uncertain cash flows to the market price of a fixed-income investment. The spread is added to the risk-free rate to compensate for the uncertainty of the cash flows.

See definitions:

- Ratings: [https://fred.stlouisfed.org/series/BAMLC0A4CBBB](https://fred.stlouisfed.org/series/BAMLC0A4CBBB){:target="_blank"}
- Maturity: [https://fred.stlouisfed.org/series/BAMLC1A0C13Y](https://fred.stlouisfed.org/series/BAMLC1A0C13Y){:target="_blank"}

**Args:**

- <u>maturity (bool, optional):</u> Whether to return the maturity option adjusted spread or the rating option adjusted spread.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.
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
| 2024-01-01 |         nan |         nan |         nan |          nan |           nan |         nan |
| 2024-01-02 |          78 |          95 |         109 |          128 |           133 |         119 |
| 2024-01-03 |          80 |          98 |         113 |          133 |           136 |         122 |
| 2024-01-04 |          80 |          98 |         112 |          133 |           135 |         122 |
| 2024-01-05 |          80 |          98 |         112 |          132 |           134 |         121 |
| 2024-01-08 |          79 |          98 |         112 |          132 |           134 |         120 |
| 2024-01-09 |          78 |          96 |         110 |          130 |           131 |         117 |
| 2024-01-10 |          77 |          94 |         108 |          128 |           128 |         113 |
| 2024-01-11 |          75 |          94 |         107 |          128 |           127 |         113 |
| 2024-01-12 |          74 |          94 |         107 |          128 |           126 |         112 |
| 2024-01-15 |          74 |          94 |         107 |          128 |           125 |         111 |

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
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.
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

| Date       |      AAA |       AA |        A |      BBB |       BB |        B |      CCC |
|:-----------|---------:|---------:|---------:|---------:|---------:|---------:|---------:|
| 2024-01-01 | nan      | nan      | nan      | nan      | nan      | nan      | nan      |
| 2024-01-02 |   0.0459 |   0.0473 |   0.0509 |   0.0543 |   0.0622 |   0.0763 |   0.1333 |
| 2024-01-03 |   0.0459 |   0.0474 |   0.051  |   0.0544 |   0.0634 |   0.0779 |   0.1358 |
| 2024-01-04 |   0.0466 |   0.0481 |   0.0518 |   0.0551 |   0.0639 |   0.0784 |   0.1367 |
| 2024-01-05 |   0.047  |   0.0485 |   0.0521 |   0.0554 |   0.0641 |   0.0787 |   0.137  |
| 2024-01-08 |   0.0465 |   0.0481 |   0.0517 |   0.055  |   0.0633 |   0.0776 |   0.1365 |
| 2024-01-09 |   0.0464 |   0.048  |   0.0516 |   0.0548 |   0.0629 |   0.0771 |   0.1359 |
| 2024-01-10 |   0.0464 |   0.048  |   0.0515 |   0.0547 |   0.0622 |   0.0762 |   0.1351 |
| 2024-01-11 |   0.0456 |   0.0472 |   0.0507 |   0.054  |   0.0619 |   0.076  |   0.1344 |
| 2024-01-12 |   0.0451 |   0.0467 |   0.0502 |   0.0534 |   0.0613 |   0.0753 |   0.1338 |
| 2024-01-15 |   0.0451 |   0.0467 |   0.0501 |   0.0533 |   0.0611 |   0.0751 |   0.1328 |

---

## get_ice_bofa_total_return
This data represents the total return of the ICE BofA Indices, When the last calendar day of the month takes place on the weekend, weekend observations will occur as a result of month ending accrued interest adjustments.

The total return is the actual rate of return of an investment or a pool of investments over a given evaluation period. Total return includes interest, capital gains, dividends and distributions realized over a given period of time.

See definitions:

- Ratings: [https://fred.stlouisfed.org/series/BAMLCC0A4BBBTRIV](https://fred.stlouisfed.org/series/BAMLCC0A4BBBTRIV){:target="_blank"}
- Maturity: [https://fred.stlouisfed.org/series/BAMLCC1A013YTRIV](https://fred.stlouisfed.org/series/BAMLCC1A013YTRIV){:target="_blank"}

**Args:**

- <u>maturity (bool, optional):</u> Whether to return the maturity total return or the rating total return.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.
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
| 2024-01-01 |      nan    |      nan    |      nan    |       nan    |        nan    |      nan    |
| 2024-01-02 |     1912.73 |     2484.25 |      807.62 |       584.32 |       4193.7  |     4343.71 |
| 2024-01-03 |     1912.18 |     2483.95 |      807.54 |       583.84 |       4194.39 |     4339.07 |
| 2024-01-04 |     1910.86 |     2477.9  |      804.35 |       580.42 |       4163.24 |     4289.24 |
| 2024-01-05 |     1910.86 |     2475.75 |      802.82 |       578.73 |       4148.31 |     4262.52 |
| 2024-01-08 |     1912.48 |     2480.39 |      804.97 |       580.71 |       4167.04 |     4302.16 |
| 2024-01-09 |     1913.5  |     2482.27 |      805.72 |       581.26 |       4173.04 |     4303.34 |
| 2024-01-10 |     1914.12 |     2483.6  |      806.21 |       581.29 |       4175.16 |     4304.82 |
| 2024-01-11 |     1918.28 |     2492.25 |      809.94 |       583.92 |       4200.49 |     4330.72 |
| 2024-01-12 |     1922.1  |     2498.89 |      812.41 |       585.2  |       4213.47 |     4338.43 |
| 2024-01-15 |     1922.67 |     2499.76 |      812.67 |       585.41 |       4215.34 |     4340.24 |

---

## get_ice_bofa_yield_to_worst
This data represents the semi-annual yield to worst of the ICE BofA Indices, When the last calendar day of the month takes place on the weekend, weekend observations will occur as a result of month ending accrued interest adjustments.

Yield to worst is the lowest potential yield that a bond can generate without the issuer defaulting. The standard US convention for this series is to use semi-annual coupon payments, whereas the standard in the foreign markets is to use coupon payments with frequencies of annual, semi-annual, quarterly, and monthly.

See definitions:

- Ratings: [https://fred.stlouisfed.org/series/BAMLC0A4CBBBSYTW](https://fred.stlouisfed.org/series/BAMLC0A4CBBBSYTW){:target="_blank"}
- Maturity: [https://fred.stlouisfed.org/series/BAMLC1A0C13YSYTW](https://fred.stlouisfed.org/series/BAMLC1A0C13YSYTW){:target="_blank"}

**Args:**

- <u>maturity (bool, optional):</u> Whether to return the maturity yield to worst or the rating yield to worst.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.
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

| Date       |      AAA |       AA |        A |      BBB |       BB |        B |      CCC |
|:-----------|---------:|---------:|---------:|---------:|---------:|---------:|---------:|
| 2024-01-01 | nan      | nan      | nan      | nan      | nan      | nan      | nan      |
| 2024-01-02 |   0.046  |   0.0475 |   0.0506 |   0.0546 |   0.0652 |   0.0796 |   0.1329 |
| 2024-01-03 |   0.0461 |   0.0475 |   0.0507 |   0.0547 |   0.0662 |   0.081  |   0.1353 |
| 2024-01-04 |   0.0468 |   0.0483 |   0.0515 |   0.0554 |   0.0665 |   0.0814 |   0.136  |
| 2024-01-05 |   0.0471 |   0.0486 |   0.0518 |   0.0557 |   0.0667 |   0.0816 |   0.1362 |
| 2024-01-08 |   0.0466 |   0.0482 |   0.0514 |   0.0553 |   0.066  |   0.0806 |   0.1359 |
| 2024-01-09 |   0.0465 |   0.0481 |   0.0513 |   0.0551 |   0.0656 |   0.0803 |   0.1353 |
| 2024-01-10 |   0.0465 |   0.0481 |   0.0512 |   0.0551 |   0.065  |   0.0795 |   0.1345 |
| 2024-01-11 |   0.0458 |   0.0473 |   0.0504 |   0.0543 |   0.0648 |   0.0793 |   0.134  |
| 2024-01-12 |   0.0453 |   0.0468 |   0.0499 |   0.0537 |   0.0642 |   0.0786 |   0.1335 |
| 2024-01-15 |   0.0452 |   0.0468 |   0.0498 |   0.0537 |   0.064  |   0.0784 |   0.1325 |

---

## get_hqm_corporate_bond_yield_curve
Retrieves the High Quality Market (HQM) corporate bond yield curve of the U.S. Department of the Treasury: the yields of high quality (AAA, AA and A rated) US corporate bonds by maturity, from 6 months to 100 years, monthly from 1984. The Treasury builds it for discounting long-dated liabilities, which is why it is the prescribed discount curve for US corporate pension obligations, and its long history makes it a natural basis for modelling how corporate yields and spreads move.

Two curves are available. Spot rates (rate="spot") are zero-coupon yields, the rate to discount a single payment at that maturity, for 17 maturities. Par yields (rate="par") are the coupons a bond priced at par would pay, for 2, 5, 10 and 30 years, comparable to the Treasury par yield curve (see `get_treasury_rates`). Every value is the average over the month.

The data comes from FRED, which republishes the Treasury's curve, so a free FRED API key is required. The rates are returned as decimal fractions (0.0558 for 5.58%).

**See definition:** [https://home.treasury.gov/data/treasury-coupon-issues-and-corporate-bond-yield-curves](https://home.treasury.gov/data/treasury-coupon-issues-and-corporate-bond-yield-curves){:target="_blank"}

**Also known as:** HQM curve, corporate bond yield curve, pension discount curve, AA corporate curve.

**Args:**

- <u>rate (str, optional):</u> "spot" for the spot rates or "par" for the par yields.
Defaults to "spot".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to return the growth data or the actual data. Defaults to False.
- <u>lag (int, optional):</u> The number of periods to lag the growth data by. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.DataFrame: The monthly average rates, indexed by month with a column per maturity.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome(start_date='2026-03-01', end_date='2026-08-31')

fixedincome.get_hqm_corporate_bond_yield_curve()[['1Y', '5Y', '10Y', '30Y', '100Y']]
```

Which returns:

|         |     1Y |     5Y |    10Y |    30Y |   100Y |
|:--------|-------:|-------:|-------:|-------:|-------:|
| 2026-03 | 0.0406 | 0.0447 | 0.0514 | 0.0614 | 0.0653 |
| 2026-04 | 0.0408 | 0.0449 | 0.0513 | 0.0612 | 0.065  |
| 2026-05 | 0.0414 | 0.0467 | 0.0528 | 0.0622 | 0.0656 |
| 2026-06 | 0.0422 | 0.0472 | 0.0527 | 0.0611 | 0.0641 |
| 2026-07 | 0.0433 | 0.0488 | 0.0545 | 0.0643 | 0.0677 |
| 2026-08 | 0.0431 | 0.0497 | 0.0558 | 0.0665 | 0.0702 |

---

## get_hqm_corporate_bond_spread
Computes the credit spread of high quality US corporate bonds per maturity: the Treasury's High Quality Market (HQM) corporate par yield minus the Treasury constant maturity yield, at 2, 5, 10 and 30 years, monthly from 1984. Both legs are par yields averaged over the month, so they are directly comparable. The spread is what investors demand for the default and liquidity risk of investment grade companies, and its shape across maturities, usually wider for longer maturities, shows how that compensation grows with time.

Unlike the ICE BofA option-adjusted spreads (see `get_ice_bofa_option_adjusted_spread`), of which FRED only carries the last three years, this spread covers four decades, long enough to calibrate how credit spreads behave through several business cycles.

The data comes from FRED, so a free FRED API key is required. The spreads are returned as decimal fractions (0.0079 for 0.79 percentage points).

**Also known as:** corporate credit spread curve, credit spread term structure, investment grade spread.

**Args:**

- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to return the growth data or the actual data. Defaults to False.
- <u>lag (int, optional):</u> The number of periods to lag the growth data by. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.DataFrame: The monthly spreads, indexed by month with a column per maturity.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome(start_date='2026-03-01', end_date='2026-08-31')

fixedincome.get_hqm_corporate_bond_spread()
```

Which returns:

|         |     2Y |     5Y |    10Y |    30Y |
|:--------|-------:|-------:|-------:|-------:|
| 2026-03 | 0.0048 | 0.006  | 0.0078 | 0.0091 |
| 2026-04 | 0.0042 | 0.0053 | 0.0071 | 0.0084 |
| 2026-05 | 0.0037 | 0.005  | 0.007  | 0.0082 |
| 2026-06 | 0.0035 | 0.0049 | 0.0071 | 0.0083 |
| 2026-07 | 0.0035 | 0.0053 | 0.0075 | 0.0092 |
| 2026-08 | 0.0036 | 0.0056 | 0.0079 | 0.0095 |

---

## get_corporate_bond_yields
Retrieves the yields of corporate bonds of a variety of countries, by rating where the source splits them, monthly and with long histories: the input for a credit spread factor outside the United States, where corporate bond indices by rating (iBoxx, ICE BofA) are licensed data.

- Germany: the average yield on debt securities outstanding of non-MFI corporations the Bundesbank publishes monthly from 1957 (monthly averages), all ratings together ("All ratings"). No API key is needed.
- Australia: the yields of non-financial corporate bonds rated A and BBB with a target tenor of 3, 5, 7 and 10 years the Reserve Bank of Australia publishes from 2005 (end of month), e.g. "BBB 10Y". No API key is needed.
- United States: Moody's seasoned Aaa and Baa corporate bond yields, from 1919. This requires a FRED API key (the fred_api_key of the FixedIncome class); see get_moodys_corporate_bond_yields for daily data.

With spread=True each yield is returned as a spread over government bonds: for Germany over the yield on public debt securities outstanding (from 1956), for Australia over the Australian government bond yield of the same tenor (end of month, interpolated between 5 and 10 years for 7 years, from 2013), and for the United States over the 10-year Treasury yield.

The yields are decimal fractions (0.0446 for 4.46%), with one column per country and rating.

**See definition:** [https://www.bundesbank.de/en/statistics/money-and-capital-markets](https://www.bundesbank.de/en/statistics/money-and-capital-markets){:target="_blank"}

**Also known as:** corporate credit spread, corporate bond yield by rating, euro credit spread, BBB spread.

**Args:**

- <u>countries (list[str] &#124; str &#124; None, optional):</u> The countries to retrieve, from
"Germany", "Australia" and "United States". Defaults to None, which
retrieves every country available, the United States only with a FRED API
key.
- <u>spread (bool, optional):</u> Whether to return the spread over government bonds
instead of the yield. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to return the growth data or the actual data. Defaults to False.
- <u>lag (int, optional):</u> The number of periods to lag the growth data by. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.DataFrame: The yields (or spreads) as decimals, indexed by month with a column
per country and rating.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome(start_date='2026-03-01', end_date='2026-08-31')

corporate_bond_yields = fixedincome.get_corporate_bond_yields(
    countries=['Germany', 'Australia'], spread=True
)

corporate_bond_yields.loc[
    :, (slice(None), ['All ratings', 'A 5Y', 'BBB 5Y', 'BBB 10Y'])
].droplevel(0, axis=1)
```

Which returns:

|         |   All ratings |   A 5Y |   BBB 5Y |   BBB 10Y |
|:--------|--------------:|-------:|---------:|----------:|
| 2026-03 |        0.01   | 0.0097 |   0.0123 |    0.0114 |
| 2026-04 |        0.0091 | 0.0085 |   0.011  |    0.01   |
| 2026-05 |        0.0086 | 0.0089 |   0.011  |    0.0097 |
| 2026-06 |        0.0084 | 0.0086 |   0.0103 |    0.0088 |
| 2026-07 |        0.0085 | 0.0085 |   0.0102 |    0.0086 |
| 2026-08 |        0.0085 | 0.0083 |   0.0099 |    0.0084 |

---

## get_rating_transition_matrix
Retrieves the rating transition matrix of a credit rating agency: for every rating at the start of a period, the share of ratings that ended the period in each rating category, in default or withdrawn. It is the input of rating migration and default models, such as the Jarrow-Lando-Turnbull model, and of credit portfolio models.

The data comes from CEREP, the central repository where every credit rating agency registered in the European Union reports its ratings to ESMA, published twice a year with periods from 1989. It covers the global ratings of agencies such as S&P, Moody's, Fitch, DBRS and Scope, for corporates (non-financial, financial and insurance), sovereigns, structured finance and covered bonds, in each agency's own rating scale. No API key is needed.

By default the matrix is withdrawal-adjusted, the convention of the agencies' own default studies: ratings withdrawn during the period are left out, so each row sums to 1. The matrix compares the rating at the start of the period with the rating at its end, so a default that was followed by a new rating within the period (as after a distressed exchange) shows as that new rating; get_default_rates counts every default within the period and is the measure to calibrate default rates on. With include_withdrawals=True they are a separate "Withdrawals" column, and with probabilities=False the counts are returned instead.

**See definition:** [https://registers.esma.europa.eu/cerep-publication/](https://registers.esma.europa.eu/cerep-publication/){:target="_blank"}

**Also known as:** rating migration matrix, credit migration matrix, transition probabilities.

**Args:**

- <u>agency (str, optional):</u> The rating agency, e.g. "S&P", "Moody's", "Fitch",
"DBRS", "Scope" or "Kroll", or the CEREP code of any registered agency.
Defaults to "S&P".
- <u>rating_type (str, optional):</u> "corporate", "sovereign", "structured_finance" or
"covered_bonds". Defaults to "corporate".
- <u>year (int &#124; None, optional):</u> The first year of the period. Defaults to None,
which takes the latest year published.
- <u>horizon (int, optional):</u> The length of the period in years, from 1 January of
year. Defaults to 1.
- <u>probabilities (bool, optional):</u> Whether to return the share of ratings per row
instead of the number. Defaults to True.
- <u>include_withdrawals (bool, optional):</u> Whether to keep the ratings withdrawn
during the period as a "Withdrawals" column. Defaults to False.
- <u>region (str &#124; None, optional):</u> The area of the rated entities: "Africa",
"America", "Asia", "Europe", "EU members", "International" or "Oceania".
Defaults to None, which covers all of them.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.

**Returns:**

pd.DataFrame: The transition matrix, with a row per rating at the start of the
period and a column per rating at its end.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome(end_date="2025-12-31")

transition_matrix = fixedincome.get_rating_transition_matrix(agency='S&P', year=2025)

transition_matrix.loc['AAA':'CCC', ['AAA', 'AA', 'A', 'BBB', 'BB', 'B', 'CCC', 'D']]
```

Which returns:

| From Rating   |   AAA |     AA |      A |    BBB |     BB |      B |    CCC |      D |
|:--------------|------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|
| AAA           |     1 | 0      | 0      | 0      | 0      | 0      | 0      | 0      |
| AA            |     0 | 0.9518 | 0.0482 | 0      | 0      | 0      | 0      | 0      |
| A             |     0 | 0.0135 | 0.9646 | 0.0219 | 0      | 0      | 0      | 0      |
| BBB           |     0 | 0.0006 | 0.0355 | 0.9563 | 0.007  | 0.0006 | 0      | 0      |
| BB            |     0 | 0      | 0      | 0.0353 | 0.9283 | 0.0353 | 0.0011 | 0      |
| B             |     0 | 0      | 0      | 0      | 0.0387 | 0.9001 | 0.0558 | 0.0023 |
| CCC           |     0 | 0      | 0      | 0      | 0      | 0.18   | 0.76   | 0.03   |

---

## get_default_rates
Retrieves the one-year default rates per rating of a credit rating agency, year by year from 1989: the share of the ratings outstanding at the start of each year that defaulted within it. The history of default rates per rating calibrates the default intensity of credit risk models and shows how defaults cluster in recessions.

The data comes from CEREP, the central repository where every credit rating agency registered in the European Union reports its ratings to ESMA, in each agency's own rating scale (AAA to C for S&P and Fitch, Aaa to C for Moody's). Only the years between the start and end date are retrieved, one request per year. No API key is needed. CEREP answers slowly (up to half a minute per year), so a long history takes a few minutes the first time; each year is cached afterwards. The years before an agency reported to CEREP read as zero defaults and are left out, so the history starts at the first year with a default.

**See definition:** [https://registers.esma.europa.eu/cerep-publication/](https://registers.esma.europa.eu/cerep-publication/){:target="_blank"}

**Also known as:** default frequency, annual default rate by rating, historical default rates.

**Args:**

- <u>agency (str, optional):</u> The rating agency, e.g. "S&P", "Moody's", "Fitch",
"DBRS", "Scope" or "Kroll", or the CEREP code of any registered agency.
Defaults to "S&P".
- <u>rating_type (str, optional):</u> "corporate", "sovereign", "structured_finance" or
"covered_bonds". Defaults to "corporate".
- <u>region (str &#124; None, optional):</u> The area of the rated entities: "Africa",
"America", "Asia", "Europe", "EU members", "International" or "Oceania".
Defaults to None, which covers all of them.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.

**Returns:**

pd.DataFrame: The default rates as decimals, indexed by year with a column per
rating.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome(start_date='2018-01-01', end_date='2025-12-31')

default_rates = fixedincome.get_default_rates(agency='S&P')

default_rates[['BBB', 'BB', 'B', 'CCC']]
```

Which returns:

|      |    BBB |     BB |      B |    CCC |
|:-----|-------:|-------:|-------:|-------:|
| 2018 | 0      | 0      | 0.0094 | 0.2617 |
| 2019 | 0.0016 | 0      | 0.0182 | 0.3534 |
| 2020 | 0      | 0.0097 | 0.038  | 0.4661 |
| 2021 | 0      | 0      | 0.0039 | 0.0895 |
| 2022 | 0      | 0.0046 | 0.0115 | 0.1402 |
| 2023 | 0.0006 | 0.001  | 0.0138 | 0.3116 |
| 2024 | 0      | 0.0021 | 0.0188 | 0.2852 |
| 2025 | 0      | 0.0011 | 0.0146 | 0.252  |

---

## get_moodys_corporate_bond_yields
Retrieves Moody's seasoned corporate bond yields for Aaa (the highest rating) and Baa (the lowest investment grade rating) US corporate bonds, the longest running corporate bond yield benchmark there is: daily from 1986 and monthly from 1919.

With spread=True the spreads over the 10-year Treasury yield are returned instead, together with the Baa minus Aaa spread, the classic measure of default risk in the academic literature (e.g. Fama and French, 1989), which widens sharply in recessions. Monthly spreads start in 1953, when the monthly 10-year Treasury yield does.

Monthly values are the averages over the month, as Moody's publishes them; weekly values are the yields on the last day of each week (weeks end on Friday).

The data comes from FRED, so a free FRED API key is required. The yields and spreads are returned as decimal fractions (0.0675 for 6.75%).

**Also known as:** Moody's Aaa, Moody's Baa, corporate bond yields by rating, default spread, credit spread.

**Args:**

- <u>period (str, optional):</u> Whether to return the daily, weekly or monthly data.
Defaults to "daily".
- <u>spread (bool, optional):</u> Whether to return the spreads over the 10-year Treasury
yield instead of the yields. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to return the growth data or the actual data. Defaults to False.
- <u>lag (int, optional):</u> The number of periods to lag the growth data by. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.DataFrame: The "Aaa" and "Baa" yields, or with spread=True the "Aaa", "Baa" and
"Baa - Aaa" spreads.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome(start_date='2026-03-01', end_date='2026-08-31')

fixedincome.get_moodys_corporate_bond_yields(period='monthly', spread=True)
```

Which returns:

|         |    Aaa |    Baa |   Baa - Aaa |
|:--------|-------:|-------:|------------:|
| 2026-03 | 0.0123 | 0.0179 |      0.0056 |
| 2026-04 | 0.011  | 0.0171 |      0.0061 |
| 2026-05 | 0.0108 | 0.0162 |      0.0054 |
| 2026-06 | 0.0105 | 0.0153 |      0.0048 |
| 2026-07 | 0.0116 | 0.0159 |      0.0043 |
| 2026-08 | 0.012  | 0.0164 |      0.0044 |

---

## get_excess_bond_premium
Retrieves the credit spread of Gilchrist and Zakrajšek (2012) and its excess bond premium, monthly from 1973, as the Federal Reserve Board updates them. The GZ credit spread is the average spread of US corporate bonds over Treasuries with the same cash flows, built bond by bond from the secondary market. The excess bond premium is the part of that spread that expected defaults do not explain: a measure of investors' appetite for credit risk, and one of the best predictors of economic activity in the literature. The Recession Probability column is the probability of a recession over the next twelve months the premium implies.

Gilchrist, S., & Zakrajšek, E. (2012). Credit Spreads and Business Cycle Fluctuations. American Economic Review, 102(4), 1692-1720. [https://doi.org/10.1257/aer.102.4.1692](https://doi.org/10.1257/aer.102.4.1692){:target="_blank"}

No API key is needed. The spread and premium are returned as decimal fractions (0.0084 for 0.84 percentage points) and the probability as a fraction (0.108 for 10.8%).

**See definition:** [https://www.federalreserve.gov/econres/notes/feds-notes/updating-the-recession-risk-and-the-excess-bond-premium-20161006.html](https://www.federalreserve.gov/econres/notes/feds-notes/updating-the-recession-risk-and-the-excess-bond-premium-20161006.html){:target="_blank"}

**Also known as:** GZ spread, Gilchrist-Zakrajšek spread, EBP, credit market sentiment.

**Args:**

- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to return the growth data or the actual data. Defaults to False.
- <u>lag (int, optional):</u> The number of periods to lag the growth data by. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.DataFrame: The "GZ Credit Spread", "Excess Bond Premium" and "Recession
Probability", indexed by month.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome(start_date='2026-02-01', end_date='2026-07-31')

fixedincome.get_excess_bond_premium()
```

Which returns:

| date    |   GZ Credit Spread |   Excess Bond Premium |   Recession Probability |
|:--------|-------------------:|----------------------:|------------------------:|
| 2026-02 |             0.0097 |               -0.0026 |                  0.1222 |
| 2026-03 |             0.0103 |               -0.0026 |                  0.1208 |
| 2026-04 |             0.0092 |               -0.002  |                  0.1374 |
| 2026-05 |             0.0083 |               -0.0037 |                  0.0951 |
| 2026-06 |             0.0086 |               -0.0028 |                  0.1152 |
| 2026-07 |             0.0084 |               -0.0031 |                  0.1093 |

---

## get_eiopa_risk_free_rate
Retrieves the risk-free interest rate term structures the European Insurance and Occupational Pensions Authority (EIOPA) publishes monthly: the curves European insurers must discount their liabilities with under Solvency II. They cover the euro and the currencies of every country of the European Economic Area, plus Switzerland, the United Kingdom, Australia, Canada, China, Colombia, Hong Kong, Japan, Taiwan and the United States, for maturities of 1 to 150 years. Beyond the last liquid maturity each curve converges to the ultimate forward rate (UFR), as Solvency II prescribes.

Four curves are published: the basic spot curve (curve="spot_no_va"), the spot curve with the volatility adjustment (curve="spot_with_va"), and the basic curve after the interest rate shocks of the Solvency II standard formula (curve="shock_up" and curve="shock_down"). EIOPA ships the shocked worksheets as formulas without computed values, so they are computed here with those formulas: upwards by the relative shock per maturity and at least one percentage point, downwards by the relative shock with negative rates left unchanged. Every value is a decimal fraction (0.0358 for 3.58%), at the end of the month the release is for.

No API key is needed. EIOPA's page links the releases from January 2023; each is a separate file, so only the months between the start and end date are downloaded, and a release is cached for a year since it does not change.

**See definition:** [https://www.eiopa.europa.eu/tools-and-data/risk-free-interest-rate-term-structures_en](https://www.eiopa.europa.eu/tools-and-data/risk-free-interest-rate-term-structures_en){:target="_blank"}

**Also known as:** Solvency II discount curve, EIOPA RFR, risk-free rate term structure, UFR curve.

**Args:**

- <u>countries (list[str] &#124; str &#124; None, optional):</u> The currencies or countries to include,
as EIOPA names them, e.g. 'Euro Area', 'United Kingdom' or 'United States'.
Defaults to None, which returns all of them.
- <u>curve (str, optional):</u> "spot_no_va", "spot_with_va", "shock_up" or "shock_down".
Defaults to "spot_no_va".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to return the growth data or the actual data. Defaults to False.
- <u>lag (int, optional):</u> The number of periods to lag the growth data by. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>maturity_years (list[int] &#124; None, optional):</u> The maturities in years to keep, e.g.
[1, 2, 5, 10, 20, 30] for the key points of the curve. Defaults to None, which
keeps every maturity from 1 to 150 years.

**Returns:**

pd.DataFrame: The rates, indexed by month with a column per currency or country and
maturity ("1Y" to "150Y").

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome(start_date='2026-07-01', end_date='2026-09-30')

curves = fixedincome.get_eiopa_risk_free_rate(countries=['Euro Area', 'United Kingdom'])

curves.loc[:, (slice(None), ['1Y', '10Y', '30Y', '60Y', '150Y'])]
```

Which returns:

|         |   ('Euro Area', '1Y') |   ('United Kingdom', '1Y') |   ('Euro Area', '10Y') |   ('United Kingdom', '10Y') |   ('Euro Area', '30Y') |
|:--------|----------------------:|---------------------------:|-----------------------:|----------------------------:|-----------------------:|
| 2026-07 |                0.0283 |                     0.0415 |                 0.0316 |                      0.0468 |                 0.0337 |
| 2026-08 |                0.0292 |                     0.0418 |                 0.0327 |                      0.0473 |                 0.0345 |
| 2026-09 |                0.0327 |                     0.0445 |                 0.0358 |                      0.0501 |                 0.0351 |

---

## get_eiopa_symmetric_adjustment
Retrieves the symmetric adjustment of the equity capital charge of Solvency II, the "equity dampener" EIOPA publishes, daily from 1991, and the equity charges of the standard formula it results in. The adjustment raises the charge when equity prices are above their three-year average and lowers it when they are below, between -10% and +10%, so insurers are not forced to sell equities into a falling market. With get_eiopa_risk_free_rate it completes the market inputs of the standard formula's market risk module.

The "Type 1 Equity Charge" (equities listed in the EEA or OECD) is 39% plus the adjustment and the "Type 2 Equity Charge" (other equities) 49% plus the adjustment. Every value is a decimal fraction (0.0771 for 7.71%). No API key is needed. Weekly and monthly periods take the value on the last day of each period, which is the value insurers apply at that reporting date.

**See definition:** [https://www.eiopa.europa.eu/tools-and-data/symmetric-adjustment-equity-capital-charge_en](https://www.eiopa.europa.eu/tools-and-data/symmetric-adjustment-equity-capital-charge_en){:target="_blank"}

**Also known as:** equity dampener, symmetric adjustment, Solvency II equity charge.

**Args:**

- <u>period (str, optional):</u> Whether to return the daily, weekly or monthly data.
Defaults to "daily".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to return the growth data or the actual data. Defaults to False.
- <u>lag (int, optional):</u> The number of periods to lag the growth data by. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.DataFrame: The symmetric adjustment and the type 1 and type 2 equity charges,
indexed by date.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome(start_date='2026-04-01', end_date='2026-09-30')

fixedincome.get_eiopa_symmetric_adjustment(period='monthly')
```

Which returns:

|         |   Symmetric Adjustment |   Type 1 Equity Charge |   Type 2 Equity Charge |
|:--------|-----------------------:|-----------------------:|-----------------------:|
| 2026-04 |                 0.0767 |                 0.4667 |                 0.5667 |
| 2026-05 |                 0.0868 |                 0.4768 |                 0.5768 |
| 2026-06 |                 0.0894 |                 0.4794 |                 0.5794 |
| 2026-07 |                 0.0951 |                 0.4851 |                 0.5851 |
| 2026-08 |                 0.0938 |                 0.4838 |                 0.5838 |
| 2026-09 |                 0.0771 |                 0.4671 |                 0.5671 |

---

## get_bank_of_england_yield_curve
Retrieves the UK yield curves the Bank of England estimates daily from 1985, for maturities from 0.5 years to 40 years (25 years for OIS): the nominal spot curve of UK government bonds (gilts) and the spot curve of overnight index swaps on SONIA (OIS, from 2009). Unlike the par yields of 5, 10 and 20 years in `get_government_bond_yield_curve`, these are zero-coupon spot rates over the full range of maturities with history back to 1985.

The Bank of England's real and implied inflation curves are part of `economics.get_real_yield_curve` and `economics.get_breakeven_inflation_expectations` (countries='United Kingdom').

No API key is needed. The archive is a set of large files, of which only those covering the requested years are read, and they are cached since past years do not change. Weekly and monthly periods take the curve on the last day of each period.

**See definition:** [https://www.bankofengland.co.uk/statistics/yield-curves](https://www.bankofengland.co.uk/statistics/yield-curves){:target="_blank"}

**Also known as:** gilt curve, UK spot curve, SONIA OIS curve.

**Args:**

- <u>curve (str, optional):</u> "nominal" or "ois". Defaults to "nominal".
- <u>period (str, optional):</u> Whether to return the daily, weekly or monthly data.
Defaults to "daily".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to return the growth data or the actual data. Defaults to False.
- <u>lag (int, optional):</u> The number of periods to lag the growth data by. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.DataFrame: The spot rates as decimals, indexed by date with a column per
maturity in years, in steps of half a year.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome(start_date='2026-04-01', end_date='2026-09-30')

fixedincome.get_bank_of_england_yield_curve(period='monthly')[
    ['1Y', '3Y', '5Y', '10Y', '20Y', '30Y']
]
```

Which returns:

|         |     1Y |     3Y |     5Y |    10Y |    20Y |    30Y |
|:--------|-------:|-------:|-------:|-------:|-------:|-------:|
| 2026-04 | 0.0426 | 0.0433 | 0.0447 | 0.0506 | 0.0573 | 0.0581 |
| 2026-05 | 0.0403 | 0.0414 | 0.043  | 0.0486 | 0.0555 | 0.0563 |
| 2026-06 | 0.0402 | 0.041  | 0.0427 | 0.0483 | 0.0552 | 0.0561 |
| 2026-07 | 0.0417 | 0.0438 | 0.0456 | 0.051  | 0.058  | 0.0589 |
| 2026-08 | 0.0418 | 0.0441 | 0.046  | 0.0514 | 0.0582 | 0.0591 |
| 2026-09 | 0.0442 | 0.0478 | 0.0494 | 0.054  | 0.0598 | 0.06   |

---

## get_corporate_borrowing_cost
Retrieves the composite cost of borrowing for non-financial corporations the European Central Bank publishes monthly from 2003, for the euro area and every member: the average interest rate on new bank loans to companies across maturities and loan sizes. Euro area companies borrow mostly from banks rather than in the bond market, which makes this the broadest measure of their cost of credit, and the closest freely available proxy for euro area corporate credit conditions, since euro area corporate bond indices are licensed data.

No API key is needed. The rate is a decimal fraction (0.0377 for 3.77%).

**See definition:** [https://data.ecb.europa.eu/data/datasets/MIR](https://data.ecb.europa.eu/data/datasets/MIR){:target="_blank"}

**Also known as:** cost of borrowing for corporations, euro area lending rate, corporate credit cost.

**Args:**

- <u>countries (list[str] &#124; str &#124; None, optional):</u> The countries to include, e.g.
'Euro Area' or ['Germany', 'Italy']. Defaults to None, which returns all of them.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to return the growth data or the actual data. Defaults to False.
- <u>lag (int, optional):</u> The number of periods to lag the growth data by. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.DataFrame: The rate, indexed by month with a column per country.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome(start_date='2026-03-01', end_date='2026-08-31')

fixedincome.get_corporate_borrowing_cost(
    countries=['Euro Area', 'Germany', 'France', 'Italy', 'Spain']
)
```

Which returns:

|         |   Euro Area |   Germany |   France |   Italy |   Spain |
|:--------|------------:|----------:|---------:|--------:|--------:|
| 2026-03 |      0.0358 |    0.0381 |   0.035  |  0.0349 |  0.0328 |
| 2026-04 |      0.0362 |    0.0378 |   0.0353 |  0.0365 |  0.0345 |
| 2026-05 |      0.0363 |    0.0372 |   0.0352 |  0.0377 |  0.0351 |
| 2026-06 |      0.0379 |    0.04   |   0.0367 |  0.0377 |  0.0355 |
| 2026-07 |      0.038  |    0.0398 |   0.0363 |  0.0386 |  0.037  |
| 2026-08 |      0.0377 |    0.0388 |   0.037  |  0.0385 |  0.0363 |

---

## get_financial_stress_index
Retrieves the Composite Indicator of Systemic Stress (CISS) the European Central Bank publishes daily for the euro area, its largest members, the United Kingdom, the United States and China, back to 1980 for some. The index combines stress in money, bond, equity and foreign exchange markets and among financial intermediaries into a number between 0 (calm) and 1 (crisis), weighting the segments more heavily when they are stressed at the same time; it peaked in 2008 and in the euro area debt crisis.

Hollo, D., Kremer, M., & Lo Duca, M. (2012). CISS - A Composite Indicator of Systemic Stress in the Financial System. ECB Working Paper No. 1426.

No API key is needed. Weekly and monthly periods take the index on the last day of each period.

**See definition:** [https://data.ecb.europa.eu/data/datasets/CISS](https://data.ecb.europa.eu/data/datasets/CISS){:target="_blank"}

**Also known as:** CISS, systemic stress, financial stress, financial conditions.

**Args:**

- <u>countries (list[str] &#124; str &#124; None, optional):</u> The areas to include, e.g. 'Euro Area'
or ['United States', 'United Kingdom']. Defaults to None, which returns all of them.
- <u>period (str, optional):</u> Whether to return the daily, weekly or monthly data.
Defaults to "daily".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to return the growth data or the actual data. Defaults to False.
- <u>lag (int, optional):</u> The number of periods to lag the growth data by. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.

**Returns:**

pd.DataFrame: The index, indexed by date with a column per area.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome(start_date='2026-04-01', end_date='2026-09-30')

fixedincome.get_financial_stress_index(
    countries=['Euro Area', 'United States', 'United Kingdom', 'China'], period='monthly'
)
```

Which returns:

|         |   Euro Area |   United States |   United Kingdom |   China |
|:--------|------------:|----------------:|-----------------:|--------:|
| 2026-04 |      0.004  |          0.0134 |           0.0222 |  0.0199 |
| 2026-05 |      0.0058 |          0.0069 |           0.0309 |  0.0059 |
| 2026-06 |      0.0098 |          0.0095 |           0.0072 |  0.0308 |
| 2026-07 |      0.0129 |          0.0493 |           0.0075 |  0.0209 |
| 2026-08 |      0.0205 |          0.0194 |           0.0011 |  0.0072 |
| 2026-09 |      0.0132 |          0.0092 |           0.0122 |  0.0015 |

---

## get_euribor_rates
Euribor rates, short for Euro Interbank Offered Rate, are the interest rates at which a panel of European banks lend funds to one another in the interbank market. These rates are published daily by the European Money Markets Institute (EMMI) and serve as a benchmark for various financial products and contracts, including mortgages, loans, and derivatives, across the Eurozone.

The Euribor rates are determined for different maturities, typically ranging from overnight to 12 months. The most common maturities are 1 month, 3 months, 6 months, and 12 months. Each maturity represents the time period for which the funds are borrowed, with longer maturities generally implying higher interest rates due to increased uncertainty and risk over longer time horizons.

For more information, see for example: [https://data.ecb.europa.eu/data/datasets/FM/FM.M.U2.EUR.RT.MM.EURIBOR6MD_.HSTA](https://data.ecb.europa.eu/data/datasets/FM/FM.M.U2.EUR.RT.MM.EURIBOR6MD_.HSTA){:target="_blank"}

**Also known as:** euro interbank offered rate, eurozone money market.

**Args:**

- <u>maturities (str &#124; list &#124; None, optional):</u> Maturities for which to retrieve rates. Defaults to None.
When set to None, it will retrieve rates for 1 month, 3 months, 6 months, and 12 months.
- <u>nominal (bool, optional):</u> Whether to retrieve the nominal Euribor fixings or their real
(inflation-adjusted) counterpart. The ECB only publishes a real Euribor for the 3-month
maturity, so nominal=False returns that maturity alone and warns about any others that
were requested rather than silently answering them with a nominal rate. Defaults to True.
- <u>rounding (int &#124; None, optional):</u> Rounding precision for the rates. Defaults to None.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. Defaults to False.

**Returns:**

pandas.DataFrame: DataFrame containing the Euribor rates for the specified maturities.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome(start_date='2023-12-01', end_date="2025-12-31")

euribor_rates = fixedincome.get_euribor_rates()
```

Which returns:

|         |   1-Month |   3-Month |   6-Month |   12-Month |
|:--------|----------:|----------:|----------:|-----------:|
| 2023-12 |    0.0386 |    0.0393 |    0.0393 |     0.0368 |
| 2024-01 |    0.0387 |    0.0393 |    0.0389 |     0.0361 |
| 2024-02 |    0.0387 |    0.0392 |    0.039  |     0.0367 |
| 2024-03 |    0.0385 |    0.0392 |    0.0389 |     0.0372 |
| 2024-04 |    0.0385 |    0.0389 |    0.0384 |     0.037  |
| 2024-05 |    0.0382 |    0.0381 |    0.0379 |     0.0368 |
| 2024-06 |    0.0363 |    0.0372 |    0.0371 |     0.0365 |
| 2024-07 |    0.0362 |    0.0368 |    0.0364 |     0.0353 |
| 2024-08 |    0.036  |    0.0355 |    0.0342 |     0.0317 |
| 2024-09 |    0.0344 |    0.0343 |    0.0326 |     0.0294 |
| 2024-10 |    0.0321 |    0.0317 |    0.03   |     0.0269 |
| 2024-11 |    0.0307 |    0.0301 |    0.0279 |     0.0251 |
| 2024-12 |    0.0289 |    0.0282 |    0.0263 |     0.0244 |
| 2025-01 |    0.0279 |    0.027  |    0.0261 |     0.0253 |
| 2025-02 |    0.0261 |    0.0252 |    0.0246 |     0.0241 |
| 2025-03 |    0.024  |    0.0244 |    0.0239 |     0.024  |
| 2025-04 |    0.0224 |    0.0225 |    0.022  |     0.0214 |
| 2025-05 |    0.0209 |    0.0209 |    0.0212 |     0.0208 |
| 2025-06 |    0.0193 |    0.0198 |    0.0205 |     0.0208 |
| 2025-07 |    0.0189 |    0.0199 |    0.0206 |     0.0208 |
| 2025-08 |    0.0189 |    0.0202 |    0.0208 |     0.0211 |
| 2025-09 |    0.019  |    0.0203 |    0.021  |     0.0217 |
| 2025-10 |    0.0191 |    0.0203 |    0.0211 |     0.0219 |
| 2025-11 |    0.0191 |    0.0204 |    0.0213 |     0.0222 |
| 2025-12 |    0.0192 |    0.0205 |    0.0214 |     0.0227 |

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
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. Defaults to False.

**Returns:**

pd.DataFrame: A DataFrame containing the ECB rates.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome(start_date='2023-12-01', end_date="2025-12-31")

fixedincome.get_european_central_bank_rates()
```

Which returns:

|            |   Refinancing |   Lending |   Deposit |
|:-----------|--------------:|----------:|----------:|
| 2025-12-22 |        0.0215 |     0.024 |      0.02 |
| 2025-12-23 |        0.0215 |     0.024 |      0.02 |
| 2025-12-24 |        0.0215 |     0.024 |      0.02 |
| 2025-12-25 |        0.0215 |     0.024 |      0.02 |
| 2025-12-26 |        0.0215 |     0.024 |      0.02 |
| 2025-12-27 |        0.0215 |     0.024 |      0.02 |
| 2025-12-28 |        0.0215 |     0.024 |      0.02 |
| 2025-12-29 |        0.0215 |     0.024 |      0.02 |
| 2025-12-30 |        0.0215 |     0.024 |      0.02 |
| 2025-12-31 |        0.0215 |     0.024 |      0.02 |

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
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. Defaults to False.

**Returns:**

pd.DataFrame: A DataFrame containing the Federal Reserve rates including the rate,
percentiles, volume and upper and lower bounds.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome(start_date='2023-12-01', end_date="2025-12-31")

effr = fixedincome.get_federal_reserve_rates()

effr.loc[:, ['Rate', '1st Percentile', '25th Percentile', '75th Percentile', '99th Percentile']]
```

Which returns:

| Effective Date   |   Rate |   1st Percentile |   25th Percentile |   75th Percentile |   99th Percentile |
|:-----------------|-------:|-----------------:|------------------:|------------------:|------------------:|
| 2025-12-17       | 0.0364 |            0.036 |            0.0363 |            0.0365 |            0.0366 |
| 2025-12-18       | 0.0364 |            0.036 |            0.0364 |            0.0365 |            0.0366 |
| 2025-12-19       | 0.0364 |            0.036 |            0.0364 |            0.0365 |            0.0365 |
| 2025-12-22       | 0.0364 |            0.036 |            0.0364 |            0.0365 |            0.0365 |
| 2025-12-23       | 0.0364 |            0.036 |            0.0363 |            0.0365 |            0.0365 |
| 2025-12-24       | 0.0364 |            0.036 |            0.0364 |            0.0365 |            0.0365 |
| 2025-12-26       | 0.0364 |            0.036 |            0.0363 |            0.0365 |            0.0365 |
| 2025-12-29       | 0.0364 |            0.036 |            0.0363 |            0.0365 |            0.0368 |
| 2025-12-30       | 0.0364 |            0.036 |            0.0364 |            0.0365 |            0.0368 |
| 2025-12-31       | 0.0364 |            0.036 |            0.0364 |            0.0365 |            0.0369 |

---

