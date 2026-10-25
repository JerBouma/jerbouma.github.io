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
- Convexity: The second derivative of the bond price with respect to the yield to maturity, divided by the price.
- Prices between coupon dates: the present value is the clean (quoted) price, while the durations, DV01 and convexity are sensitivities of the full (dirty) price; on a coupon date the two prices coincide.

The formula is as follows:

$$
\operatorname{PV}(t) = \text{Cash Flow} (t) / (1 + \text{YTM} / \text{Frequency}) ^{\text{Frequency} \cdot t},\;\; \text{with each coupon equal to Par Value} \cdot \text{Coupon Rate} / \text{Frequency and the par value repaid with the last coupon}
$$

$$
\text{Dirty Price} = \operatorname{SUM}(\operatorname{PV}(t)),\;\; \text{over the remaining payment times t in years (fractional between coupon dates)}
$$

$$
\text{Present Value} = \text{Dirty Price} - \text{Accrued Interest},\;\; \text{the clean price (see get\_present\_value)}
$$

$$
\text{Current Yield} = \text{Par Value} \cdot \text{Coupon Rate} / \text{Present Value}
$$

$$
\text{Effective Yield} = (1 + \text{Coupon Rate} / \text{Frequency}) ^{\text{Frequency}} - 1
$$

$$
\text{Macaulay's Duration} = \operatorname{SUM}(t \cdot \operatorname{PV}(t)) / \text{Dirty Price}
$$

$$
\text{Modified Duration} = \text{Macaulay's Duration} / (1 + \text{YTM} / \text{Frequency})
$$

$$
\text{Effective Duration} = (\text{Dirty Price} (\text{YTM} - 0.01) - \text{Dirty Price} (\text{YTM} + 0.01)) / (2 \cdot \text{Dirty Price} \cdot 0.01)
$$

$$
\text{Dollar Duration} = \text{Modified Duration} \cdot \text{Dirty Price} / 100
$$

$$
\text{DV01} = (\text{Present Value} (\text{YTM} - 0.0001) - \text{Present Value} (\text{YTM} + 0.0001)) / 2
$$

$$
\text{Convexity} = (\text{Dirty Price} (\text{YTM} + 0.0001) + \text{Dirty Price} (\text{YTM} - 0.0001) - 2 \cdot \text{Dirty Price}) / (\text{Dirty Price} \cdot 0.0001 ^{2})
$$

Where YTM is the yield to maturity, a nominal annual rate compounded `frequency` times a year (0.08 and annual by default). The Effective Yield restates the coupon rate, not the yield to maturity.

These statistics can be used to evaluate the bond's performance as opposed to other bonds or to estimate the bond's sensitivity to changes in interest rates to be able to apply a hedging strategy.

**Also known as:** bond data, fixed income statistics.

**Args:**

- <u>par_value (float):</u> The face value of the bond. Defaults to 100.
- <u>coupon_rate (float):</u> The annual coupon rate (in decimal). Defaults to 0.05.
- <u>years_to_maturity (float):</u> The number of years until the bond matures. Defaults to 5.
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

|                     |    Value |
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

Note how the effective duration sits just above the modified duration: the two
measure the same sensitivity, but the symmetric 100 basis point repricing of the
effective duration also picks up the third-order term of the price-yield
relationship, about -P'''(y) * Δy^2 / (6 * P), which the analytical modified
duration leaves out. The convexity (second-order) terms cancel in the symmetric
difference.

---

## get_present_value
Calculates the bond prices for different coupon rates and years to maturity. The bond price is the present value of the bond's future cash flows, which includes the coupon payments and the par value of the bond at maturity.

The formula is as follows:

$$
\text{Dirty Price} = \operatorname{SUM}(C / (1 + r) ^{t_{i}}) + F / (1 + r) ^{t_{n}},\;\; \text{over} \;\; \text{the remaining coupons}\; i = 1,\;\; \text{...},\;\; \text{n}
$$

$$
\text{Accrued Interest} = C \cdot a
$$

$$
\text{Bond Price} = \text{Dirty Price} - \text{Accrued Interest},\;\; \text{the clean price}
$$

where:

$$
C = \text{Coupon payment per period},\;\; \text{Par Value} \cdot \text{Coupon Rate} / \text{Frequency}
$$

$$
r = \text{Yield to maturity per period},\;\; \text{Yield to Maturity} / \text{Frequency} (a \;\text{nominal annual rate compounded}\; \text{frequency} \;\text{times}\; a \;\text{year},\; 0.08 \;\text{and annual by default})
$$

$$
a = \text{Elapsed fraction of the current coupon period},\;\; \text{in periods of equal length (30/360)},\;\; \text{0 on a coupon date}
$$

$$
t_{i} = i - a,\;\; \text{the time of the i-th cash flow in coupon periods},\;\; \text{so}\; t_{n} = \text{Years to Maturity} \cdot \text{Frequency}
$$

$$
F = \text{Face value of the bond}
$$

On a coupon date this is Bond Price = (C / r) * (1 - (1 + r)^-n) + F / (1 + r)^n.

The bond price is used to determine the fair value of the bond and to compare the bond's price to its market price to determine if the bond is overvalued or undervalued.

The coupon schedule runs back from maturity, so a maturity that is not a whole number of coupon periods (2.5 years of annual coupons) discounts every cash flow over its fractional number of periods, and the price is the clean (quoted) price: the full price minus the coupon interest accrued since the previous coupon date, matching QuantLib's clean price with a 30/360 count. On a coupon date the two coincide.

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

|   Coupon Rate |       5 |      10 |      15 |
|--------------:|--------:|--------:|--------:|
|          0.03 | 80.0364 | 66.4496 | 57.2026 |
|          0.05 | 88.0219 | 79.8698 | 74.3216 |
|          0.07 | 96.0073 | 93.2899 | 91.4405 |

---

## get_duration
Calculates the bond duration for different coupon rates and years to maturity. It has the option to calculate the following type of bond durations:

- Macaulay's Duration: The weighted average time to receive the bond's cash flows.
- Modified Duration: The Macaulay's duration divided by 1 plus the per-period yield (yield to maturity divided by the frequency).
- Effective Duration: The percentage change in the bond price for a 1% change in the yield to maturity.
- Dollar Duration: The modified duration multiplied by the bond price, divided by 100.

These duration measures can be used to estimate the sensitivity of a bond's price to changes in interest rates as well as to compare the risk of different bonds. The modified duration is particularly useful for estimating the percentage change in the bond price for a 1% change in the yield to maturity. Note that it is a percentage sensitivity and therefore not the same as the dollar duration, the price value of a basis point (PVBP) or the dollar value of a 0.01% change (DV01), which are all expressed as a currency amount instead. The dollar duration is available through this method via `duration_type='dollar'` and the DV01 is calculated separately, see `collect_bond_statistics`.

The formula is as follows (the default is the modified duration):

$$
\operatorname{PV}(t) = \text{Cash Flow} (t) / (1 + \text{YTM} / \text{Frequency}) ^{\text{Frequency} \cdot t},\;\; \text{with each coupon equal to Par Value} \cdot \text{Coupon Rate} / \text{Frequency and the par value repaid with the last coupon}
$$

$$
\text{Dirty Price} = \operatorname{SUM}(\operatorname{PV}(t)),\;\; \text{over the remaining payment times t in years (fractional between coupon dates)}
$$

$$
\text{Macaulay's Duration} = \operatorname{SUM}(t \cdot \operatorname{PV}(t)) / \text{Dirty Price}
$$

$$
\text{Modified Duration} = \text{Macaulay's Duration} / (1 + \text{YTM} / \text{Frequency})
$$

$$
\text{Effective Duration} = (\text{Dirty Price} (\text{YTM} - 0.01) - \text{Dirty Price} (\text{YTM} + 0.01)) / (2 \cdot \text{Dirty Price} \cdot 0.01)
$$

$$
\text{Dollar Duration} = \text{Modified Duration} \cdot \text{Dirty Price} / 100
$$

Where YTM is the yield to maturity (compounded at the coupon frequency, 0.08 and annual by default).

Modified duration is the first estimate of interest rate risk: a modified duration of 7 means the price falls by about 7% if the yield rises by one percentage point. The estimate worsens for larger moves, which convexity corrects (see `get_taylor_price_change`), and it assumes the cash flows are fixed. For callable bonds and mortgage-backed securities the relevant measure is an effective duration from a model that values the embedded option, which this method does not include.

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

|   Coupon Rate |      5 |     10 |      15 |
|--------------:|-------:|-------:|--------:|
|          0.03 | 4.3312 | 7.8207 | 10.3951 |
|          0.05 | 4.1774 | 7.2645 |  9.4072 |
|          0.07 | 4.0491 | 6.8683 |  8.7891 |

---

## get_yield_to_maturity
Calculates the yield to maturity for a bond. The yield to maturity is the internal rate of return of the bond, which is the discount rate that equates the present value of the bond's cash flows to its market price. The yield to maturity is used to estimate the bond's return and to compare the bond's return to other investments.

The formula is as follows, solved for r:

$$
\text{Bond Price} = \operatorname{SUM}(C / (1 + r) ^{t_{i}}) + F / (1 + r) ^{t_{n}} - C \cdot a,\;\; \text{over} \;\; \text{the remaining coupons}\; i = 1,\;\; \text{...},\;\; \text{n}
$$

$$
\text{Yield to Maturity} = r \cdot \text{Frequency}
$$

where:

$$
C = \text{Coupon payment per period},\;\; \text{Par Value} \cdot \text{Coupon Rate} / \text{Frequency}
$$

$$
r = \text{Yield to maturity per period}
$$

$$
a = \text{Elapsed fraction of the current coupon period},\;\; \text{in periods of equal length (30/360)},\;\; \text{0 on a coupon date}
$$

$$
t_{i} = i - a,\;\; \text{the time of the i-th cash flow in coupon periods},\;\; \text{so}\; t_{n} = \text{Years to Maturity} \cdot \text{Frequency}
$$

$$
F = \text{Face value of the bond}
$$

The Bond Price is the clean price, the dirty price minus the accrued coupon C * a, as in `get_present_value`.

The goal is to find the yield to maturity that satisfies the equation above. This is done using the secant method which is an iterative method that converges to the root of a function. The bond price is read as a clean (quoted) price, and a maturity between coupon dates discounts each cash flow over its fractional number of periods, in the same way as `get_present_value`, so the yield is a nominal annual rate compounded `frequency` times per year.

The yield to maturity is the return of a bond bought at this price and held to maturity, if every coupon is reinvested at the same yield and the issuer pays in full. It is the standard way to quote and compare bonds, but it is one average rate for all cash flows: bonds with the same maturity but different coupons have different yields even when both are priced in line with the same spot curve, and for callable bonds the yield to worst is quoted instead.

**Also known as:** YTM, bond return to maturity.

**Args:**

- <u>par_value (float):</u> The par value (face value) of the bond, the amount repaid at maturity. Defaults to 100.
- <u>coupon_rate (float, optional):</u> The coupon rate of the bond. Defaults to 0.05.
- <u>years_to_maturity (float, optional):</u> The years to maturity of the bond in years. Defaults to None.
- <u>bond_price (float, optional):</u> The clean (quoted) price of the bond. Defaults to None, a range of
prices around the par value.
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

The formula is as follows:

$$
\text{Forward Rate} = ((1 + r_{2}) ^{t_{2}} / (1 + r_{1}) ^{t_{1}}) ^{1 / (t_{2} - t_{1})} - 1
$$

where:

$$
r_{1} = \text{Spot rate at the near maturity},\;\; \text{interpolated linearly from the curve}
$$

$$
t_{1} = \text{Near maturity},\;\; \text{in years}
$$

$$
r_{2} = \text{Spot rate at the far maturity},\;\; \text{interpolated linearly from the curve}
$$

$$
t_{2} = \text{Far maturity},\;\; \text{in years}
$$

The spot rates are read as effective annual (annually compounded) rates and the forward rate is annually compounded as well.

**Also known as:** implied forward rate, forward-forward rate.

**Args:**

- <u>spot_rates (pd.Series &#124; dict, optional):</u> The zero-coupon (spot) yield curve
in decimals, read as effective annual (annually compounded) rates, indexed
by maturity in years (a number, or a label such as '6M' or '10Y'). Defaults to a sample curve.
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

The formula is as follows:

$$
\operatorname{DF}(t) = 1 / (1 + \text{Spot Rate} (t / \text{Frequency}) / \text{Frequency}) ^{t},\;\; \text{the discount factor of a cash flow after t coupon periods}
$$

$$
\text{Par Yield} = \text{Frequency} \cdot (1 - \operatorname{DF}(t_{n})) / (\operatorname{SUM}(\operatorname{DF}(t_{i})) - a),\;\; \text{over} \;\; \text{the remaining coupons}\; i = 1,\;\; \text{...},\;\; \text{n}
$$

where Spot Rate(τ) is the spot curve interpolated linearly at τ years and read as a nominal annual rate compounded `frequency` times a year (annual by default), a is the elapsed fraction of the current coupon period (0 on a coupon date) and t_i = i - a is the time of the i-th coupon in periods, so t_n = Years to Maturity * Frequency. On a coupon date this is the textbook Frequency * (1 - DF(n)) / SUM(DF(k)); for a maturity between coupon dates the par yield is the coupon at which the clean price, without accrued interest, equals par (see `yieldcurve_model.get_par_yield`). The par yield is a nominal annual coupon rate paid `frequency` times a year.

**Also known as:** par rate, par coupon rate.

**Args:**

- <u>spot_rates (pd.Series &#124; dict, optional):</u> The zero-coupon (spot) yield curve
in decimals, read as nominal annual rates compounded `frequency` times per
year, indexed by maturity in years (a number, or a label such as '6M' or '10Y'). Defaults to a sample curve.
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

The formula is as follows:

$$
\text{Yield Curve Spread} = \text{Long-Term Yield} - \text{Short-Term Yield}
$$

Where both yields are interpolated linearly from the curve and subtracted as given, in the compounding of the curve passed.

**Also known as:** term spread, yield curve slope.

**Args:**

- <u>spot_rates (pd.Series &#124; dict, optional):</u> The yield curve in decimals, indexed
by maturity in years (a number, or a label such as '6M' or '10Y'). Defaults to a sample curve.
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

The formula is as follows:

$$
\text{Breakeven Inflation Rate} = \text{Nominal Yield} - \text{Real Yield}
$$

Where both yields are interpolated linearly from their curves and subtracted as given, in the compounding of the curves passed (the simple difference, not (1 + Nominal) / (1 + Real) - 1).

The breakeven rate is often read as the market's expected inflation, but it also contains an inflation risk premium, which raises it, and a liquidity premium on inflation-linked bonds, which lowers it, so it rises and falls in market stress for reasons other than inflation expectations. For the United States the comparison is with CPI-U, the index TIPS pay on. Survey expectations (`get_inflation_expectations` in the Economics module) are the usual cross-check.

**Also known as:** TIPS breakeven spread, inflation breakeven.

**Args:**

- <u>nominal_rates (pd.Series &#124; dict, optional):</u> The nominal (non-inflation-protected)
yield curve in decimals, indexed by maturity in years (a number, or a label such as '6M' or '10Y').
Defaults to a sample curve.
- <u>real_rates (pd.Series &#124; dict, optional):</u> The real (inflation-protected) yield
curve in decimals, indexed by maturity in years (a number, or a label such as '6M' or '10Y').
Defaults to a sample curve.
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

The formula is as follows, solved for the Z-Spread:

$$
\text{Clean Price} = \operatorname{SUM}(\text{Cash Flow} (t) / (1 + (\text{Spot Rate} (t) + \text{Z-Spread}) / \text{Frequency}) ^{\text{Frequency} \cdot t}) - \text{Accrued Interest}
$$

Where each coupon is Par Value * Coupon Rate / Frequency, the par value is repaid with the last coupon, t is each remaining payment time in years and Spot Rate(t) is the benchmark spot rate (compounded at the coupon frequency) interpolated linearly between the curve's maturities and held flat beyond its first and last maturity.

The Z-spread depends on the benchmark curve: against the government curve it measures credit and liquidity risk together, against the swap curve mostly the credit risk relative to banks. It should be calculated with a zero-coupon (spot) curve; a par yield curve such as the Treasury's is close but not the same. For a bond with an embedded option the Z-spread includes the option's value, which the option-adjusted spread removes.

**Also known as:** zero-volatility spread, static spread.

**Args:**

- <u>par_value (float):</u> The par value (face value) of the bond.
- <u>coupon_rate (float, optional):</u> The coupon rate of the bond. Defaults to 0.05.
- <u>years_to_maturity (float, optional):</u> The years to maturity of the bond in years. Defaults to None.
- <u>bond_price (float, optional):</u> The clean (quoted) price of the bond. Defaults to None, a range of
prices around the par value.
- <u>spot_rates (pd.Series &#124; dict, optional):</u> The benchmark zero-coupon (spot)
yield curve in decimals, read as nominal annual rates compounded `frequency`
times per year, indexed by maturity in years (a number, or a label such as '6M' or '10Y'). Defaults to a sample curve.
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

## get_option_adjusted_spread
Calculates the option-adjusted spread (OAS) of a callable bond: the spread over the risk-free curve at which the bond's model price, with the issuer calling the bond whenever that is in its interest, equals its market price. A callable bond pays a higher yield because the issuer can redeem it early when rates fall, which caps its price. The Z-spread lumps that option together with the credit and liquidity premium; the OAS takes the value of the option out, so callable and straight bonds can be compared on their credit spread alone.

The interest rate is modeled with a Ho-Lee binomial tree of twenty steps per coupon period, calibrated to the zero-coupon curve (with the short rate's volatility in absolute terms, 0.01 being 100 basis points a year). The bond is valued backwards through the tree, capped at the call price on every coupon date from the first call date, and the spread added to every rate in the tree is solved for. The bond price is the clean price: between coupon dates the interest accrued since the last coupon is added to it, as a buyer pays it on top. At that spread the method also returns:

- Straight Bond Price: the price of the same bond without the call.
- Option Value: the straight bond price minus the market price, the value of the call to the issuer.
- Effective Duration and Effective Convexity: the price change for a 100 basis point shift of the curve up and down at an unchanged OAS, which account for the call (a callable bond's convexity turns negative when the call is near).

For more information, see the following sources:

- Ho, T.S.Y. and Lee, S.-B. (1986). "Term Structure Movements and Pricing Interest Rate Contingent Claims." Journal of Finance, 41(5), 1011-1029.
- Fabozzi, F.J. (2016). "Bond Markets, Analysis, and Strategies." Pearson, 9th edition, chapter 18.

**Also known as:** OAS, option-adjusted spread of a callable bond, effective duration, negative convexity.

**Args:**

- <u>bond_price (float &#124; list[float], optional):</u> The market (clean) price of the bond,
or several prices. Defaults to 100.
- <u>coupon_rate (float, optional):</u> The annual coupon rate. Defaults to 0.05.
- <u>years_to_maturity (float, optional):</u> The years to maturity. Defaults to 10.
- <u>call_price (float &#124; None, optional):</u> The price at which the issuer can call the
bond, None for a bond without a call. Defaults to 100.
- <u>years_to_first_call (float, optional):</u> The years until the bond can first be
called. Defaults to 2.
- <u>volatility (float, optional):</u> The volatility of the short rate in absolute terms.
Defaults to 0.01.
- <u>frequency (int, optional):</u> The coupon payments per year. Defaults to 2.
- <u>par_value (float, optional):</u> The par value of the bond. Defaults to 100.
- <u>spot_rates (pd.Series &#124; dict &#124; None, optional):</u> The zero-coupon curve (annually
compounded) by maturity in years. Defaults to None, which uses the US
Treasury zero-coupon curve of the end date (see `get_zero_coupon_curve`).
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.

**Returns:**

pd.DataFrame: The Option-Adjusted Spread, Straight Bond Price, Option Value,
Effective Duration and Effective Convexity, with a column per bond price.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome()

fixedincome.get_option_adjusted_spread(
    bond_price=[98, 100, 102],
    coupon_rate=0.05,
    years_to_maturity=10,
    years_to_first_call=2,
    spot_rates={1: 0.036, 2: 0.035, 5: 0.037, 10: 0.041, 20: 0.047, 30: 0.047},
)
```

Which returns:

|                        |        98 |       100 |       102 |
|:-----------------------|----------:|----------:|----------:|
| Option-Adjusted Spread |    0.0057 |    0.0012 |   -0.0039 |
| Straight Bond Price    |  103.338  |  107.146  |  111.637  |
| Option Value           |    5.3382 |    7.1458 |    9.6374 |
| Effective Duration     |    4.743  |    4.1973 |    3.6058 |
| Effective Convexity    | -102.679  | -106.054  | -100.365  |

---

## get_bond_equivalent_yield
Converts a money-market discount yield (e.g. quoted for Treasury bills) into a bond-equivalent yield (BEY). Money-market instruments are often quoted on a discount-yield basis, which understates the actual return an investor earns because it is computed on face value rather than the (lower) purchase price, and uses a 360-day rather than a 365-day year. The bond-equivalent yield restates the discount yield on a basis that is comparable to coupon-bearing bonds and notes.

The formula is as follows:

$$
\text{BEY} = 365 \cdot \text{Discount Yield} / (360 - \text{Days to Maturity} \cdot \text{Discount Yield}),\;\; \text{for 182.5 days or less}
$$

$$
\text{Price} = 1 - \text{Discount Yield} \cdot \text{Days to Maturity} / 360,\;\; \text{per unit of face value}
$$

$$
\text{BEY} = (- 2t + 2 \cdot \sqrt{t ^{2} - (2t - 1) \cdot (1 - 1 / \text{Price})}) / (2t - 1),\;\; \text{with}\; t = \text{Days to Maturity} / 365,\;\; \text{for more than 182.5 days}
$$

A bill with half a year or less remaining takes the simple restatement onto the purchase price and a 365-day year. Beyond that an equivalent coupon-bearing note would have paid a coupon at the six month point, so the U.S. Treasury's semi-annually compounded solution (31 CFR 356, Appendix B) is used instead, see `bond_model.get_bond_equivalent_yield`. Applying the simple formula to a 52-week bill instead overstates its yield by roughly seven basis points.

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
Calculates the key rate duration of a bond for one or more individual maturity points ("key rates") on the yield curve. Whereas `get_duration` with `duration_type='effective'` assumes the entire curve shifts in parallel, key rate duration measures the bond's price sensitivity to a shock at a single tenor of the curve while every other point is held fixed. Because cash flows are discounted using linear interpolation between the curve's tenors, a shock at an inner tenor tapers off towards its neighboring tenors and has no effect beyond them. The curve is held flat beyond its first and last tenors, so a shock at the first tenor moves every cash flow paid before it in full (and a shock at the last tenor every cash flow paid after it).

Summing the key rate durations across every tenor of the curve approximately reproduces the bond's effective (parallel-shift) duration, but key rate duration additionally reveals which segment of the curve the bond's price is most exposed to - information that is essential for constructing curve-neutral hedges or identifying "twist" risk.

A barbell and a bullet with the same duration have very different key rate profiles and react differently when the curve steepens or flattens, which is why key rate durations are hedged with instruments at each key maturity. Because a shock at one maturity tapers off to its neighbours, the profile also depends on which maturities the curve contains: the same bond shows different key rate durations on a curve with more or fewer points.

The formula is as follows:

$$
\text{Dirty Price} = \operatorname{SUM}(\text{Cash Flow} (t) / (1 + \text{Spot Rate} (t) / \text{Frequency}) ^{\text{Frequency} \cdot t})
$$

$$
\text{Key Rate Duration} = - (\text{Dirty Price} (\text{Key Rate} + \Delta y) - \text{Dirty Price} (\text{Key Rate} - \Delta y)) / (2 \cdot \text{Dirty Price} \cdot \Delta y)
$$

Where each coupon is Par Value * Coupon Rate / Frequency, the par value is repaid with the last coupon, t is each remaining payment time in years, Spot Rate(t) is the spot rate (compounded at the coupon frequency) interpolated linearly between the curve's maturities and Δy is the shock applied to the key rate only (1 basis point by default).

**Also known as:** partial duration, rate-specific duration.

**Args:**

- <u>par_value (float, optional):</u> The par value (face value) of the bond. Defaults to 100.
- <u>coupon_rate (float, optional):</u> The coupon rate of the bond. Defaults to 0.05.
- <u>years_to_maturity (float &#124; list, optional):</u> The years to maturity of the
bond (or bonds). If not provided, a range of years to maturity will be used.
- <u>spot_rates (pd.Series &#124; dict, optional):</u> The zero-coupon (spot) yield curve
used to discount the bond's cash flows, in decimals, read as nominal annual
rates compounded `frequency` times per year and indexed by maturity in years (a number, or a label such as '6M' or '10Y').
Defaults to a sample curve.
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

The formula is as follows:

$$
\text{Modified Duration} = \operatorname{SUM}(t \cdot \operatorname{PV}(t)) / \text{Dirty Price} / (1 + \text{YTM} / \text{Frequency}),\;\; \text{see get\_duration}
$$

$$
\text{Convexity} = (\text{Dirty Price} (\text{YTM} + 0.0001) + \text{Dirty Price} (\text{YTM} - 0.0001) - 2 \cdot \text{Dirty Price}) / (\text{Dirty Price} \cdot 0.0001 ^{2})
$$

$$
\%\Delta \;\text{Price} \approx - \text{Modified Duration} \cdot \Delta y + 0.5 \cdot \text{Convexity} \cdot \Delta y ^{2}
$$

Where YTM is the yield to maturity, a nominal annual rate compounded `frequency` times a year (0.08 and annual by default), Δy is the yield change (0.01 by default) and %ΔPrice is the change of the full (dirty) price as a decimal, which on a coupon date equals the clean price `get_present_value` returns.

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

- Black Model: A mathematical model used for pricing financial derivatives, its primary applications are for pricing options on future contracts, bond options, interest rate caps and floors, and swaptions. For more information, see: [https://en.wikipedia.org/wiki/Black_model](https://en.wikipedia.org/wiki/Black_model){:target="_blank"}
- Bachelier Model: A deviation of the Black Model that is used for pricing future contracts. It is a simple model that assumes the price of the underlying asset follows a normal distribution with constant volatility. This is in contrast to the Black Model which assumes the price of the underlying asset follows a log-normal distribution. For more information, see: [https://en.wikipedia.org/wiki/Bachelier_model](https://en.wikipedia.org/wiki/Bachelier_model){:target="_blank"}

Both models are applied to European swaptions here, the right to enter an interest rate swap at the strike rate; caps, floors and bond options are not implemented.

It is possible to alter all parameters within the models, e.g. strike rate, volatility, years to maturity, risk-free rate, notional amount, and whether the holder is the receiver or payer of the derivative. Next to that, you can provide lists of strike rates and years to maturity to calculate the derivative price for several scenarios at once.

Exercising a swaption is not a single payment at expiration - it is the right to enter a swap that exchanges cash flows at every payment date over the underlying swap's tenor. The price therefore discounts the option payoff by the swap's annuity (present value of a basis point) rather than a single discount factor to expiration, which is why the tenor and payment frequency of the underlying swap matter.

Note that a swaption's price scales with the tenor of the underlying swap (a right to enter a longer-dated swap is worth more, since it exchanges cash flows over more payment dates) - pass `tenor` explicitly to price a swaption whose underlying swap tenor differs from its years to maturity, e.g. a 1-year option into a 5-year swap: `tenor=5, years_to_maturity=1`.

The two models do not quote volatility on the same basis, and this matters a great deal. Black's model, being lognormal, reads `volatility` as a fraction of the forward rate, so 0.20 is a 20% volatility. The Bachelier model, being normal, reads it as an absolute movement in rate units, so 0.0065 is 65 basis points. On a 3.25% forward those two quotes describe the same market, but swapping one for the other misprices the swaption by a factor of roughly thirty. By default `volatility` is therefore interpreted on whichever basis the chosen model is defined in; set `volatility_type` explicitly to supply a quote on the other basis and have it converted, using the at-the-money approximation sigma_normal ≈ sigma_lognormal * forward_rate.

Black's model is undefined at a zero or negative forward or strike rate because it takes the logarithm of their ratio, and raises rather than returning a silent NaN in that case. Use the Bachelier model for the negative rates seen in the euro area and Japan.

The formula is as follows (Black's model and a receiver swaption are the defaults):

$$
\text{Annuity} = (1 / \text{Payment Frequency}) \cdot \operatorname{SUM}(e ^{- r \cdot t_{i}}),\;\; \text{over} \;\; \text{the swap's payment times}\; t_{i} = T + i / \text{Payment Frequency for}\; i = 1,\;\; \text{...},\;\; \text{Tenor} \cdot \text{Payment Frequency} (\text{the tenor defaults to}\; T)
$$

$$
\text{Black}\; d_{1} = (\ln(F / K) + \sigma ^{2} \cdot T / 2) / (\sigma \cdot \sqrt{T}),\;\; d_{2} = d_{1} - \sigma \cdot \sqrt{T},\;\; \text{with sigma the lognormal volatility}
$$

$$
\text{Black Payer Payoff} = F \cdot N(d_{1}) - K \cdot N(d_{2})
$$

$$
\text{Black Receiver Payoff} = K \cdot N(- d_{2}) - F \cdot N(- d_{1})
$$

$$
\text{Bachelier}\; d = (F - K) / (\sigma_{N} \cdot \sqrt{T}),\;\; \text{with sigma\_N the normal volatility}
$$

$$
\text{Bachelier Payer Payoff} = (F - K) \cdot N(d) + \sigma_{N} \cdot \sqrt{T} \cdot n(d)
$$

$$
\text{Bachelier Receiver Payoff} = (K - F) \cdot N(- d) + \sigma_{N} \cdot \sqrt{T} \cdot n(- d)
$$

$$
\text{Swaption Price} = \text{Notional} \cdot \text{Annuity} \cdot \text{Payoff}
$$

Where F is the forward swap rate, K is the strike rate, T is the years to maturity (expiry) of the option, r is the continuously compounded risk-free rate (the forward rate when not given), N is the cumulative standard normal distribution and n its density. A volatility quoted on the other basis is converted with σ_N = σ * F.

**Also known as:** bond derivative pricing, fixed income derivative, swaption pricing.

**Args:**

- <u>model (str, optional):</u> The type of model to use for calculating the derivative price. Defaults to "black".
- <u>forward_rate (float, optional):</u> The forward rate as derived from the swap curve. Defaults to 0.05.
- <u>strike_rate (float &#124; list, optional):</u> The strike rate for the derivative. Defaults to None which means it calculates the
derivative price a range of strike prices. Can also be a list of strike rates (e.g. [0.01, 0.02, 0.03, 0.04, 0.05]).
- <u>volatility (float, optional):</u> The volatility of the underlying swap rate, quoted on the
basis given by `volatility_type`. Defaults to 0.01, read as a 1% lognormal volatility
by the Black model and as 100 basis points of normal volatility by the Bachelier model.
- <u>years_to_maturity (float &#124; list, optional):</u> The years to maturity of the derivative. Defaults to None, which
returns the price for 1 to 10 years. Can also be a list of years to maturity (e.g. [1, 2.3, 2.5, 3])
- <u>risk_free_rate (float, optional):</u> The risk-free interest rate used to discount the swap's payment dates,
read as a continuously compounded rate on a flat curve (discount factor exp(-r * t)). Defaults to None,
which uses the forward rate; as the forward rate is a swap rate on the swap's own compounding, pass the
continuously compounded rate explicitly for an exact annuity.
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

In the example below the result has one column per expiry date and one row per strike.
The strikes below the 3.25% forward are worthless because a receiver swaption only
pays when the fixed rate it locks in exceeds the prevailing forward, and at a 1%
lognormal volatility a 50 basis point gap is far out of reach.

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

Which returns:

|   Strike Rate |   2026-12-31 |   2027-12-31 |   2030-12-30 |   2035-12-29 |
|--------------:|-------------:|-------------:|-------------:|-------------:|
|        0.0275 |         0    |         0    |          0   |          0   |
|        0.0325 |      1224.91 |      3300.15 |      11280.4 |      25086.1 |
|        0.0375 |     47237.2  |     89991.1  |     194547   |     305934   |
|        0.0425 |     94474.3  |    179982    |     389094   |     611868   |

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
Defaults to None, which returns the monthly data (quarterly when the class was
created with quarterly=True).
- <u>growth (bool, optional):</u> Whether to return the growth data or the actual data. Defaults to False.
- <u>lag (int, optional):</u> The number of periods to lag the growth data by. Defaults to 1.
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

long_term_interest_rate.loc[:, ['Japan', 'United States', 'Germany']]
```

Which returns:

|         |   Japan |   United States |   Germany |
|:--------|--------:|----------------:|----------:|
| 2023-05 |  0.0043 |          0.0357 |    0.0234 |
| 2023-06 |  0.004  |          0.0375 |    0.0238 |
| 2023-07 |  0.0059 |          0.039  |    0.0246 |
| 2023-08 |  0.0064 |          0.0417 |    0.0255 |
| 2023-09 |  0.0076 |          0.0438 |    0.0266 |
| 2023-10 |  0.0095 |          0.048  |    0.0282 |
| 2023-11 |  0.0066 |          0.045  |    0.026  |
| 2023-12 |  0.0062 |          0.0402 |    0.021  |

---

## get_government_bond_yield_curve
Retrieves the government bond yield curve of a variety of countries, every maturity a country's government borrows at, from treasury bills to bonds of 30 years and more. The yield curve is the basis for discounting cash flows and pricing bonds, and its shape is one of the most watched signals in markets: an inverted curve, with short rates above long rates, has preceded most recessions.

Every curve comes from the official source without an API key:

- United States: the U.S. Department of the Treasury's par yield curve, 1 month to 30 years, from 1990.
- Euro Area: the yield curve the European Central Bank estimates from the bonds of all euro area central governments, 3 months to 30 years, from 2004, as zero-coupon (spot) rates of a Svensson model, continuously compounded.
- Germany: the term structure the Deutsche Bundesbank estimates from listed federal securities, 1 to 30 years, as zero-coupon (spot) rates of a Svensson model, continuously compounded.
- United Kingdom: the Bank of England's nominal par yields of gilts, 5, 10 and 20 years.
- Japan: the Ministry of Finance's Japanese government bond yields, 1 to 40 years, from 1974.
- Canada: the Bank of Canada's treasury bill yields (1 month to 1 year, weekly) and benchmark bond yields (2 to 30 years).
- Sweden: the Riksbank's treasury bill and government bond yields, 1 month to 10 years.
- Norway: Norges Bank's generic government bond yields, 3 to 10 years.
- Australia: the Reserve Bank of Australia's government bond yields interpolated to 2, 3, 5 and 10 years, from 2013.

With period="monthly", every other European Union member, such as France, Italy, Spain, the Netherlands and Poland, is included with its 10-year yield, the long-term interest rate for convergence purposes the ECB publishes monthly. For other countries no official source publishes a curve without a key; see `get_government_bond_yield` for the monthly 3-month and 10-year rates of around forty countries from the OECD. Only the requested countries are retrieved, and only the days that are not cached yet.

The yields are returned as decimal fractions per annum (0.0419 for 4.19%), with one column per country and maturity, sorted from the shortest to the longest maturity. Each curve is returned as its source publishes it: the Euro Area and Germany curves are continuously compounded zero-coupon rates, while the other countries publish par or benchmark bond yields, which compound with the coupon frequency of their bonds. The two are not interchangeable: a continuously compounded zero rate r equals an annually compounded zero rate of exp(r) - 1, and a par yield is the coupon rate at which a bond prices at par, which differs from the zero rate of the same maturity whenever the curve is not flat. Weekly and monthly periods take the yields on the last trading day of each period (weeks end on Friday).

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

These are par yields: the coupons at which a new Treasury of each maturity would price at par, interpolated by the Treasury from the most recently auctioned securities. Discounting individual cash flows needs zero-coupon (spot) rates bootstrapped from them; on a steep curve the two differ by several basis points at long maturities. The 10-year minus 2-year and 10-year minus 3-month spreads from this curve are the most watched recession indicators.

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

The rates are decimal fractions, so they feed straight into the bond-pricing methods
above. Multiply by 100 to recover the published Treasury figures.

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

## get_zero_coupon_curve
Calculates the zero-coupon (spot) yield curve of a country by bootstrapping its government bond par yields. A par yield is the coupon at which a bond trades at par, so it mixes the discount rates of every coupon date; the zero-coupon rate of a maturity is the single rate that discounts a payment at that date. Zero-coupon rates are what bonds and other cash flows are discounted with, and what forward rates and the curve models (Nelson-Siegel, Vasicek) are built on.

Maturities up to one year are treasury bills, which pay no coupon, so their yield only needs converting to annual compounding: US bill yields are bond-equivalent yields (simple interest up to half a year), Canadian bill yields simple interest on a 365-day year and Swedish bill yields simple interest on a 360-day year. Beyond that the par yields are interpolated linearly to every coupon date and each discount factor follows from the earlier ones:

P(t_n) = (1 - c/f Σ_{i<n} P(t_i)) / (1 + c/f)

with c the par yield of maturity t_n and f the coupons per year (two, and one for Sweden and Norway). The curves of the Euro Area and Germany are estimated as zero-coupon curves by the ECB and the Bundesbank, which publish them continuously compounded; they are converted to annual compounding like the others. A curve needs a maturity of a year or less to start from, so the United Kingdom, Norway and Australia (and Canada before its bill yields start) are not covered.

**Also known as:** spot curve, zero curve, bootstrapped curve, discount curve.

**Args:**

- <u>countries (list[str] &#124; str, optional):</u> The countries, see
`get_government_bond_yield_curve`. Defaults to "United States".
- <u>period (str, optional):</u> Whether to use the daily, weekly or monthly curves.
Defaults to "daily".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.

**Returns:**

pd.DataFrame: The zero-coupon rates as decimals (annually compounded), indexed by
date with a column per country and maturity.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome(start_date='2026-10-19', end_date='2026-10-23')

zero_curve = fixedincome.get_zero_coupon_curve()

zero_curve['United States'][['1Y', '2Y', '5Y', '10Y', '20Y', '30Y']]
```

Which returns:

|            |     1Y |     2Y |     5Y |    10Y |    20Y |    30Y |
|:-----------|-------:|-------:|-------:|-------:|-------:|-------:|
| 2026-10-19 | 0.0455 | 0.0484 | 0.0501 | 0.0526 | 0.0581 | 0.0564 |
| 2026-10-20 | 0.0456 | 0.0486 | 0.0501 | 0.0522 | 0.0573 | 0.0556 |
| 2026-10-21 | 0.0457 | 0.0488 | 0.0502 | 0.0523 | 0.0572 | 0.0556 |
| 2026-10-22 | 0.0446 | 0.0471 | 0.0485 | 0.0506 | 0.0557 | 0.0545 |
| 2026-10-23 | 0.0449 | 0.0475 | 0.0489 | 0.051  | 0.0563 | 0.0548 |

---

## get_nelson_siegel_svensson
Fits the Nelson-Siegel-Svensson model to the zero-coupon yield curve of a country on every date. The model describes a whole curve with a few parameters, which smooths out the noise of individual maturities, gives a yield for any maturity in between and turns the history of curves into a history of a handful of factors. It is the model central banks such as the ECB, the Bundesbank and the Federal Reserve (Gürkaynak, Sack and Wright) publish their curves with.

The Nelson-Siegel model has a level β0 (the yield at an infinite maturity), a slope β1 (the short end minus the long end) and a curvature β2 (a hump that peaks at about 1.8 τ1 years):

y(m) = β0 + β1 (1 - e^(-m/τ1)) / (m/τ1) + β2 [(1 - e^(-m/τ1)) / (m/τ1) - e^(-m/τ1)]

Svensson adds a second curvature β3 with its own decay τ2, which fits the long end better. With the dozen maturities a government curve has, the six Svensson parameters are weakly identified, as the level and the second curvature can offset each other; set svensson=False for the three factors to read as level, slope and curvature (Diebold and Li, 2006).

Given the decays the betas follow exactly from least squares, so the decays are searched on a grid and refined for every date. The second decay is kept at least 1.5 times the first and the first at least a third of the shortest maturity, and the level at or above the lower of zero and the longest yield (as Gürkaynak, Sack and Wright keep it at or above zero), so that the curve extrapolates sensibly beyond the maturities it is fitted to. The curve is the zero-coupon curve of `get_zero_coupon_curve`, so the countries are those it covers that have at least as many maturities as the model has parameters. The model is fitted to the continuously compounded rates, as the ECB, the Bundesbank and the Federal Reserve fit it, so the parameters compare with theirs; the yields at `maturities` are annually compounded, like those of `get_zero_coupon_curve`.

For more information, see the following papers:

- Nelson, C.R. and Siegel, A.F. (1987). "Parsimonious Modeling of Yield Curves." The Journal of Business, 60(4), 473-489.
- Svensson, L.E.O. (1994). "Estimating and Interpreting Forward Interest Rates: Sweden 1992-1994." NBER Working Paper 4871.
- Diebold, F.X. and Li, C. (2006). "Forecasting the Term Structure of Government Bond Yields." Journal of Econometrics, 130(2), 337-364.
- Gürkaynak, R.S., Sack, B. and Wright, J.H. (2007). "The U.S. Treasury Yield Curve: 1961 to the Present." Journal of Monetary Economics, 54(8), 2291-2304.

**Also known as:** NSS, Svensson curve, Nelson-Siegel curve, yield curve fitting, level slope curvature factors.

**Args:**

- <u>countries (list[str] &#124; str, optional):</u> The countries, see
`get_zero_coupon_curve`. Defaults to "United States".
- <u>period (str, optional):</u> Whether to fit the daily, weekly or monthly curves.
Defaults to "daily".
- <u>svensson (bool, optional):</u> Whether to fit the Svensson model (True) or the
Nelson-Siegel model (False). Defaults to True.
- <u>maturities (list[float &#124; str] &#124; str &#124; None, optional):</u> The maturities, in years or
as labels such as "3M" and "10Y" (a list or a comma-separated string), to
return the fitted zero-coupon yields at instead of the parameters. Defaults
to None, which returns the parameters.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.

**Returns:**

pd.DataFrame: Per date, the parameters (Beta 0 to Beta 3 as continuously
compounded rates, Tau 1 and Tau 2 in years) and the Root Mean Squared Error of the
fit, or the fitted (annually compounded) yields, with a column per country and
parameter (or maturity).

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome(start_date='2026-10-19', end_date='2026-10-23')

fixedincome.get_nelson_siegel_svensson(countries='Germany')
```

Which returns:

|            |   Beta 0 |   Beta 1 |   Beta 2 |   Beta 3 |   Tau 1 |   Tau 2 |   Root Mean Squared Error |
|:-----------|---------:|---------:|---------:|---------:|--------:|--------:|--------------------------:|
| 2026-10-19 |   0.0409 |  -0.0173 |   0.0418 |  -0.051  |  1.1799 |  1.7805 |                         0 |
| 2026-10-20 |   0.0408 |  -0.0172 |   0.0411 |  -0.0505 |  1.1997 |  1.7996 |                         0 |
| 2026-10-21 |   0.0406 |  -0.0168 |   0.0308 |  -0.041  |  1.1497 |  1.8913 |                         0 |
| 2026-10-22 |   0.0397 |  -0.0161 |   0.0313 |  -0.0385 |  1.1471 |  1.8929 |                         0 |
| 2026-10-23 |   0.0395 |  -0.0154 |   0.0365 |  -0.0462 |  1.2162 |  1.8245 |                         0 |

---

## get_yield_curve_principal_components
Calculates the principal components of a country's government bond yield curve: the few independent movements that explain nearly all of how the curve changes. Litterman and Scheinkman (1991) found that three components explain over 95% of the changes of Treasury yields: a parallel shift (level, PC1, loading about equally on every maturity), a steepening (slope, PC2, with opposite signs at the short and long end) and a bending (curvature, PC3, moving the middle against both ends). Hedging a bond portfolio against the first two covers most of its interest rate risk.

The components are the eigenvectors of the covariance matrix of the yield changes (or levels), sorted by the share of the variance they explain. Their sign is arbitrary, so PC1 is oriented as a rise in all yields (its loadings sum to a positive number), PC2 as a steepening (the longest maturity loads above the shortest) and the others so that their loadings sum to a positive number. Maturities that are only published for part of the period (such as the 4-month Treasury bill from 2022) are left out, so that the analysis covers the full period.

For more information, see the following paper:

- Litterman, R. and Scheinkman, J. (1991). "Common Factors Affecting Bond Returns." The Journal of Fixed Income, 1(1), 54-61.

**Also known as:** PCA of the yield curve, level slope curvature, term structure factors.

**Args:**

- <u>country (str, optional):</u> The country, see `get_government_bond_yield_curve`.
Defaults to "United States".
- <u>period (str, optional):</u> Whether to use the daily, weekly or monthly curves.
Defaults to "daily".
- <u>components (int, optional):</u> The number of components. Defaults to 3.
- <u>changes (bool, optional):</u> Whether to analyze the changes of the yields, the usual
choice as yields themselves are not stationary, or their levels. Defaults to True.
- <u>scores (bool, optional):</u> Whether to return the value of every component per date
(the scores) instead of the loadings. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.

**Returns:**

pd.DataFrame: The loadings per maturity and component, with the share of the
variance each component explains as the last row, or the scores per date.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome(start_date='2016-01-01', end_date='2025-12-31')

fixedincome.get_yield_curve_principal_components(period='monthly')
```

Which returns:

| Maturity           |    PC1 |     PC2 |     PC3 |
|:-------------------|-------:|--------:|--------:|
| 1M                 | 0.1332 | -0.6209 |  0.3084 |
| 3M                 | 0.1713 | -0.4809 |  0.1636 |
| 6M                 | 0.225  | -0.3809 | -0.0592 |
| 1Y                 | 0.2789 | -0.2545 | -0.2647 |
| 2Y                 | 0.3538 | -0.0249 | -0.4383 |
| 3Y                 | 0.3676 |  0.0701 | -0.3617 |
| 5Y                 | 0.3733 |  0.1595 | -0.1347 |
| 7Y                 | 0.3636 |  0.1907 |  0.0399 |
| 10Y                | 0.3434 |  0.1972 |  0.2136 |
| 20Y                | 0.3052 |  0.1888 |  0.4277 |
| 30Y                | 0.2855 |  0.1773 |  0.4831 |
| Explained Variance | 0.732  |  0.1938 |  0.0501 |

---

## get_short_rate_model
Calibrates the Vasicek and Cox-Ingersoll-Ross (CIR) short-rate models to the history of a country's short-term government bond yield and compares the zero-coupon curve each model implies with today's. Short-rate models describe how the interest rate moves, pulled back to a long-run mean b at a speed a with a volatility σ:

$$
\text{Vasicek (1977):}\;\; \text{dr} = a (b - r) \text{dt} + \sigma \;\text{dW}
$$

$$
\text{CIR (1985):}\;\; \text{dr} = a (b - r) \text{dt} + \sigma \;\text{sqrt} (r) \text{dW}
$$

In CIR the volatility shrinks as the rate approaches zero, so the rate stays positive when 2ab ≥ σ² (the Feller condition) and can otherwise touch zero; in Vasicek it can turn negative. The models describe a continuously compounded short rate, so the yields are converted to continuous compounding first (US bill yields from their bond-equivalent quote). Both give bond prices, and so a full zero-coupon curve, in closed form. The parameters are estimated by regressing the change of the rate on its level over the period (CIR on the changes scaled by the square root of the rate, which needs a rate above zero throughout). The half-life is the time it takes to close half the gap to the long-run mean, ln(2) / a.

A model calibrated to the history does not reproduce today's curve, which is what the comparison with the market shows; the Hull-White model of `get_short_rate_simulation` adds a time-varying mean that does.

For more information, see the following papers:

- Vasicek, O. (1977). "An Equilibrium Characterization of the Term Structure." Journal of Financial Economics, 5(2), 177-188.
- Cox, J.C., Ingersoll, J.E. and Ross, S.A. (1985). "A Theory of the Term Structure of Interest Rates." Econometrica, 53(2), 385-407.

**Also known as:** short rate model, mean reversion of interest rates, Vasicek model, CIR model, equilibrium term structure model.

**Args:**

- <u>country (str, optional):</u> The country, see `get_government_bond_yield_curve`.
Defaults to "United States".
- <u>short_rate (str, optional):</u> The maturity of the yield used as the short rate,
such as "1M", "3M" or "6M". Defaults to "3M".
- <u>period (str, optional):</u> Whether to calibrate on daily, weekly or monthly rates.
Defaults to "daily".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.

**Returns:**

pd.DataFrame: Per model (columns Vasicek and CIR) the Speed of Mean Reversion, the
Long-Run Mean, the Volatility, the Current Rate and the Half-Life in years, then
the zero-coupon rate per maturity (continuously compounded), with the market's
zero-coupon rates in the Market column.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome(start_date='2000-01-01', end_date='2026-10-23')

fixedincome.get_short_rate_model(short_rate='6M')
```

Which returns:

| Parameter               |   Vasicek |    CIR |   Market |
|:------------------------|----------:|-------:|---------:|
| Speed of Mean Reversion |    0.0873 | 0.1481 | nan      |
| Long-Run Mean           |    0.0144 | 0.017  | nan      |
| Volatility              |    0.0059 | 0.0558 | nan      |
| Current Rate            |    0.0425 | 0.0425 |   0.0425 |
| Half-Life               |    7.9398 | 4.6816 | nan      |
| Zero Rate 1M            |    0.0424 | 0.0424 |   0.041  |
| Zero Rate 1.5M          |    0.0424 | 0.0423 |   0.041  |
| Zero Rate 2M            |    0.0423 | 0.0422 |   0.0415 |
| Zero Rate 3M            |    0.0422 | 0.0421 |   0.042  |
| Zero Rate 4M            |    0.0421 | 0.0419 |   0.0427 |
| Zero Rate 6M            |    0.0419 | 0.0416 |   0.0425 |
| Zero Rate 1Y            |    0.0413 | 0.0407 |   0.0439 |
| Zero Rate 2Y            |    0.0402 | 0.039  |   0.0464 |
| Zero Rate 3Y            |    0.0391 | 0.0375 |   0.047  |
| Zero Rate 5Y            |    0.0371 | 0.0347 |   0.0477 |
| Zero Rate 7Y            |    0.0353 | 0.0324 |   0.0485 |
| Zero Rate 10Y           |    0.0328 | 0.0297 |   0.0497 |
| Zero Rate 20Y           |    0.0269 | 0.0242 |   0.0548 |
| Zero Rate 30Y           |    0.0232 | 0.0216 |   0.0534 |

---

## get_short_rate_simulation
Simulates the future path of a country's short-term interest rate with the Hull-White, Vasicek or Cox-Ingersoll-Ross model and summarizes the distribution of the paths per step: the mean and the 5th, 25th, 50th, 75th and 95th percentiles. Simulated rate paths value interest rate derivatives and path-dependent products (such as mortgages with prepayment), and stress the interest income of a balance sheet.

The speed of mean reversion and the volatility are calibrated to the history of the rate, see `get_short_rate_model`. In the Vasicek and CIR models the rate is pulled to the long-run mean of that history. The Hull-White (1990) model replaces it with a mean that varies over time and follows from today's zero-coupon curve, so that the model reproduces the discount factors of that curve (its expected short rate lies above the forward rate by the convexity term σ² (1 - e^(-at))² / (2a²)):

dr = [θ(t) - a r] dt + σ dW, θ(t) = ∂f/∂t + a f(t) + σ² (1 - e^(-2at)) / (2a)

with f the instantaneous forward rate. The paths are simulated with an Euler scheme starting at today's rate (CIR's are kept at or above zero).

For more information, see the following paper:

- Hull, J. and White, A. (1990). "Pricing Interest-Rate-Derivative Securities." The Review of Financial Studies, 3(4), 573-592.

**Also known as:** interest rate simulation, Hull-White model, Monte Carlo short rate, interest rate scenarios.

**Args:**

- <u>model (str, optional):</u> "hull_white", "vasicek" or "cir". Defaults to "hull_white".
- <u>country (str, optional):</u> The country, see `get_government_bond_yield_curve`.
Defaults to "United States".
- <u>short_rate (str, optional):</u> The maturity of the yield used as the short rate,
such as "1M", "3M" or "6M". Defaults to "3M".
- <u>period (str, optional):</u> Whether to calibrate on daily, weekly or monthly rates.
Defaults to "daily".
- <u>years (float, optional):</u> The horizon in years. Defaults to 10.
- <u>steps_per_year (int, optional):</u> The steps per year. Defaults to 12.
- <u>paths (int, optional):</u> The number of simulated paths. Defaults to 10,000.
- <u>seed (int &#124; None, optional):</u> The random seed, None for a different simulation
every time. Defaults to 0.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.

**Returns:**

pd.DataFrame: The Mean and the percentiles of the simulated rate (as decimals),
indexed by the time in years.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome(start_date='2000-01-01', end_date='2026-10-23')

simulation = fixedincome.get_short_rate_simulation(
    short_rate='6M', years=5, steps_per_year=1
)

simulation
```

Which returns:

|   Years |   Mean |     5% |    25% |    50% |    75% |    95% |
|--------:|-------:|-------:|-------:|-------:|-------:|-------:|
|       0 | 0.0425 | 0.0425 | 0.0425 | 0.0425 | 0.0425 | 0.0425 |
|       1 | 0.0489 | 0.0393 | 0.0449 | 0.0489 | 0.0529 | 0.0587 |
|       2 | 0.0483 | 0.035  | 0.0429 | 0.0483 | 0.0537 | 0.0614 |
|       3 | 0.0485 | 0.0332 | 0.0421 | 0.0484 | 0.0547 | 0.0643 |
|       4 | 0.0493 | 0.0324 | 0.0423 | 0.0492 | 0.0563 | 0.0666 |
|       5 | 0.0503 | 0.0322 | 0.0427 | 0.0503 | 0.0579 | 0.0689 |

---

## get_treasury_auctions
Retrieves the results of the US Treasury auctions held between the start and end date: every bill, note, bond, TIPS and floating rate note the Treasury sold, with the yield it sold at, how many times the offering was bid (the bid-to-cover ratio) and who bought it. Auction results are the most direct read of the demand for US government debt: a lower bid-to-cover ratio or a smaller share for indirect bidders (which include foreign central banks) at a large auction is a sign of weak demand.

The data comes from the Treasury's Fiscal Data API, from 1979 on, without an API key. The Yield is the high yield of notes and bonds and the investment rate (the bond equivalent yield) of bills; the High Discount Rate is the discount rate bills are quoted at. The Bid-to-Cover Ratio is the Treasury's, which leaves out the Federal Reserve's (SOMA) bids, while the Total Tendered and Total Accepted include them, so their ratio is lower when the Federal Reserve rolls over maturing holdings. The bidder shares are each class's part of the competitive awards: primary dealers (who must bid at every auction), direct bidders (buying for their own account) and indirect bidders (bidding through a dealer, such as foreign and international monetary authorities and investment funds). Auctions that are announced but not yet held, and older auctions for which the Treasury did not publish a breakdown, show NaN for the missing results.

**See definition:** [https://fiscaldata.treasury.gov/datasets/treasury-securities-auctions-data/](https://fiscaldata.treasury.gov/datasets/treasury-securities-auctions-data/){:target="_blank"}

**Also known as:** Treasury auction results, bid-to-cover ratio, auction demand, indirect bidders, Treasury issuance.

**Args:**

- <u>security_type (list[str] &#124; str &#124; None, optional):</u> The kind of security: "Bill",
"Cash Management Bill", "Note", "Bond", "TIPS" or "FRN", or several (a list or
a comma-separated string). Defaults to None, which returns every kind.
- <u>security_term (str &#124; None, optional):</u> The term as the Treasury writes it, such as
"13-Week", "10-Year" or "30-Year". Defaults to None, which returns every term.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which keeps the precision the Treasury publishes.

**Returns:**

pd.DataFrame: One row per auction, indexed by the auction date, with the security,
its dates, the Coupon Rate, Yield and High Discount Rate as decimals, the
Bid-to-Cover Ratio, the amounts in dollars and the bidder shares as decimals.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome(start_date='2025-01-01', end_date='2026-10-23')

auctions = fixedincome.get_treasury_auctions(security_type='Note', security_term='10-Year')

auctions[['Security Term', 'Reopening', 'Yield', 'Bid-to-Cover Ratio', 'Indirect Bidder Share']].tail()
```

Which returns:

| Auction Date   | Security Term   | Reopening   |   Yield |   Bid-to-Cover Ratio |   Indirect Bidder Share |
|:---------------|:----------------|:------------|--------:|---------------------:|------------------------:|
| 2025-08-06     | 10-Year         | No          | 0.04255 |                 2.35 |                  0.6423 |
| 2025-11-12     | 10-Year         | No          | 0.04074 |                 2.43 |                  0.67   |
| 2026-02-11     | 10-Year         | No          | 0.04177 |                 2.39 |                  0.6454 |
| 2026-05-12     | 10-Year         | No          | 0.04468 |                 2.4  |                  0.6395 |
| 2026-08-12     | 10-Year         | No          | 0.04683 |                 2.53 |                  0.7673 |

---

## get_ice_bofa_option_adjusted_spread
The ICE BofA Option-Adjusted Spreads (OASs) are the calculated spreads between a computed OAS index of all bonds in a given maturity and rating category and a spot Treasury curve. An OAS index is constructed using each constituent bond's OAS, weighted by market capitalization.

The Option-Adjusted Spread (OAS) is the spread relative to a risk-free interest rate, usually quoted in basis points, that equates the theoretical present value of a series of uncertain cash flows to the market price of a fixed-income investment. The spread is added to the risk-free rate to compensate for the uncertainty of the cash flows.

See definitions:

- Ratings: [https://fred.stlouisfed.org/series/BAMLC0A4CBBB](https://fred.stlouisfed.org/series/BAMLC0A4CBBB){:target="_blank"}
- Maturity: [https://fred.stlouisfed.org/series/BAMLC1A0C13Y](https://fred.stlouisfed.org/series/BAMLC1A0C13Y){:target="_blank"}

**Args:**

- <u>maturity (bool, optional):</u> Whether to return the maturity option adjusted spread or the rating option adjusted spread.
Defaults to True (by maturity).
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. Defaults to False.

**Notes:**

ICE licenses only the most recent three years of every ICE BofA series to FRED. A
start_date earlier than that returns fewer rows rather than an error, and the example
below falls out of that window over time. Go to the ICE source directly for longer
histories.

**Returns:**

pd.DataFrame: A DataFrame containing the Option Adjusted Spread as decimal fractions, like
every other rate. The FRED series are published in percent and are divided by 100 here, so
a 0.77% (77 basis point) spread is returned as 0.0077.

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
| 2024-01-01 |    nan      |    nan      |    nan      |     nan      |      nan      |    nan      |
| 2024-01-02 |      0.0078 |      0.0095 |      0.0109 |       0.0128 |        0.0133 |      0.0119 |
| 2024-01-03 |      0.008  |      0.0098 |      0.0113 |       0.0133 |        0.0136 |      0.0122 |
| 2024-01-04 |      0.008  |      0.0098 |      0.0112 |       0.0133 |        0.0135 |      0.0122 |
| 2024-01-05 |      0.008  |      0.0098 |      0.0112 |       0.0132 |        0.0134 |      0.0121 |
| 2024-01-08 |      0.0079 |      0.0098 |      0.0112 |       0.0132 |        0.0134 |      0.012  |
| 2024-01-09 |      0.0078 |      0.0096 |      0.011  |       0.013  |        0.0131 |      0.0117 |
| 2024-01-10 |      0.0077 |      0.0094 |      0.0108 |       0.0128 |        0.0128 |      0.0113 |
| 2024-01-11 |      0.0075 |      0.0094 |      0.0107 |       0.0128 |        0.0127 |      0.0113 |
| 2024-01-12 |      0.0074 |      0.0094 |      0.0107 |       0.0128 |        0.0126 |      0.0112 |
| 2024-01-15 |      0.0074 |      0.0094 |      0.0107 |       0.0128 |        0.0125 |      0.0111 |

---

## get_ice_bofa_effective_yield
This data represents the effective yield of the ICE BofA Indices, When the last calendar day of the month takes place on the weekend, weekend observations will occur as a result of month ending accrued interest adjustments.

The effective yield of an ICE BofA index is the yield of the index as a whole, aggregated from the yields of its constituent bonds and weighted by their market capitalisation. It is an index-level yield of the corporate bond market segment, not a statistic derived from any single bond's coupon - for the single-bond coupon-reinvestment calculation, see the "Effective Yield" row of `collect_bond_statistics` instead.

The FRED series are published in percent and are converted to decimals here, so a 5.40% BBB index yield is returned as 0.054.

See definitions:

- Ratings: [https://fred.stlouisfed.org/series/BAMLC0A4CBBBEY](https://fred.stlouisfed.org/series/BAMLC0A4CBBBEY){:target="_blank"}
- Maturity: [https://fred.stlouisfed.org/series/BAMLC1A0C13YEY](https://fred.stlouisfed.org/series/BAMLC1A0C13YEY){:target="_blank"}

**Also known as:** ICE BofA corporate bond yield, credit yield.

**Args:**

- <u>maturity (bool, optional):</u> Whether to return the maturity effective yield or the rating effective yield.
Defaults to True (by maturity).
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. Defaults to False.

**Notes:**

ICE licenses only the most recent three years of every ICE BofA series to FRED. A
start_date earlier than that returns fewer rows rather than an error, and the example
below falls out of that window over time. Go to the ICE source directly for longer
histories.

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
Defaults to True (by maturity).
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. Defaults to False.

**Notes:**

ICE licenses only the most recent three years of every ICE BofA series to FRED. A
start_date earlier than that returns fewer rows rather than an error, and the example
below falls out of that window over time. Go to the ICE source directly for longer
histories.

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
Defaults to True (by maturity).
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. Defaults to False.

**Notes:**

ICE licenses only the most recent three years of every ICE BofA series to FRED. A
start_date earlier than that returns fewer rows rather than an error, and the example
below falls out of that window over time. Go to the ICE source directly for longer
histories.

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

The formula is as follows:

$$
\text{HQM Spread} (\text{maturity}) = \text{HQM Corporate Par Yield} (\text{maturity}) - \text{Treasury Constant Maturity Yield} (\text{maturity}),\;\; \text{both monthly averages},\;\; \text{for 2},\;\; \text{5},\;\; \text{10 and 30 years}
$$

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

The formula is as follows (probabilities=True, the default):

$$
\text{Transition Probability} (\text{from},\; \text{to}) = \text{Count} (\text{from},\; \text{to}) / \operatorname{SUM}(\text{Count} (\text{from},\; \text{every end category})),\;\; \text{with the end categories the ratings and default},\;\; \text{plus "Withdrawals" only when include\_withdrawals=True}
$$

A single year's matrix rests on few observations in the top and bottom rows: an AAA row with few issuers is often 100% stable one year and shows a downgrade the next. Credit models therefore use the average over many years, or a longer horizon, and check how far the latest year deviates from it, which also shows where in the credit cycle the year stands.

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

Default rates rise steeply down the rating scale, from close to zero for investment grade to tens of percent a year for CCC, and because they cluster in recessions a probability of default calibrated on calm years understates the risk. Practitioners average over a full cycle, often decades, for through-the-cycle estimates and use the worst years for stress scenarios. Rates for the top ratings rest on very few defaults.

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

## get_implied_default_probability
Calculates the default probabilities that credit spreads imply. Investors in a corporate bond are compensated for the loss they expect from a default, so with a constant default intensity (hazard rate) λ and a share R recovered on default the spread s is about λ (1 - R), the "credit triangle":

λ = s / (1 - R), P(default within t years) = 1 - e^(-λt)

By default the spreads are the latest ICE BofA option-adjusted spreads of the US corporate bond indices per rating (AAA to CCC), which need a FRED API key. Spreads also pay for liquidity and for the uncertainty of the losses, so these risk-neutral probabilities are higher than the default rates that are observed historically (see `get_default_rates`); the gap is the credit risk premium.

For more information, see the following book:

- Hull, J.C. (2022). "Options, Futures, and Other Derivatives." Pearson, 11th edition, chapter 24.

**Also known as:** implied default probability, hazard rate, credit triangle, risk-neutral default probability.

**Args:**

- <u>spreads (str &#124; float &#124; dict &#124; pd.Series &#124; None, optional):</u> The credit spread as a
decimal (0.01 for 100 basis points), or several by name as a dictionary,
Series or string such as "BBB:0.011, B:0.031". Defaults to None, which uses
the latest ICE BofA option-adjusted spread per rating.
- <u>recovery_rate (float, optional):</u> The share of the face value recovered on
default. Defaults to 0.4.
- <u>horizons (list[float] &#124; str &#124; None, optional):</u> The horizons in years, as a list or
a comma-separated string. Defaults to None, which uses 1, 3, 5 and 10 years.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.

**Returns:**

pd.DataFrame: The Spread, the Hazard Rate and the default probability per horizon
as decimals, with a row per spread.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome()

fixedincome.get_implied_default_probability(
    spreads={'BBB': 0.011, 'BB': 0.021, 'B': 0.031, 'CCC': 0.087}
)
```

Which returns:

| Name   |   Spread |   Hazard Rate |   1Y Default Probability |   3Y Default Probability |   5Y Default Probability |   10Y Default Probability |
|:-------|---------:|--------------:|-------------------------:|-------------------------:|-------------------------:|--------------------------:|
| BBB    |    0.011 |        0.0183 |                   0.0182 |                   0.0535 |                   0.0876 |                    0.1675 |
| BB     |    0.021 |        0.035  |                   0.0344 |                   0.0997 |                   0.1605 |                    0.2953 |
| B      |    0.031 |        0.0517 |                   0.0504 |                   0.1436 |                   0.2277 |                    0.4035 |
| CCC    |    0.087 |        0.145  |                   0.135  |                   0.3527 |                   0.5157 |                    0.7654 |

---

## get_moodys_corporate_bond_yields
Retrieves Moody's seasoned corporate bond yields for Aaa (the highest rating) and Baa (the lowest investment grade rating) US corporate bonds, the longest running corporate bond yield benchmark there is: daily from 1986 and monthly from 1919.

With spread=True the spreads over the 10-year Treasury yield are returned instead, together with the Baa minus Aaa spread, the classic measure of default risk in the academic literature (e.g. Fama and French, 1989), which widens sharply in recessions. Monthly spreads start in 1953, when the monthly 10-year Treasury yield does.

Monthly values are the averages over the month, as Moody's publishes them; weekly values are the yields on the last day of each week (weeks end on Friday).

The formula is as follows (spread=True only):

$$
\text{Aaa} = \text{Aaa Yield} - \text{10-Year} \;\text{Treasury Yield},\;\; \text{and Baa likewise}
$$

$$
\text{Baa} - \text{Aaa} = \text{Baa Yield} - \text{Aaa Yield}
$$

Monthly spreads subtract the monthly average 10-year Treasury constant maturity yield; daily spreads are the ones FRED publishes against the daily 10-year yield.

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

Up to the last liquid point the curve follows market rates (for the euro, swap rates minus a credit risk adjustment); beyond it the curve is extrapolated towards the ultimate forward rate, so long maturities reflect the regulatory assumption more than market prices. Insurers that are allowed to apply the volatility adjustment discount with that curve, and the shocked curves give the interest rate risk capital requirement of the standard formula.

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
[1, 2, 5, 10, 20, 30] (or "1,2,5,10,20,30") for the key points of the curve. Defaults to None, which
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

|         |   ('Euro Area', '1Y') |   ('United Kingdom', '1Y') |   ('Euro Area', '10Y') |   ('United Kingdom', '10Y') |   ('Euro Area', '30Y') |   ('United Kingdom', '30Y') |   ('Euro Area', '60Y') |   ('United Kingdom', '60Y') |   ('Euro Area', '150Y') |   ('United Kingdom', '150Y') |
|:--------|----------------------:|---------------------------:|-----------------------:|----------------------------:|-----------------------:|----------------------------:|-----------------------:|----------------------------:|------------------------:|-----------------------------:|
| 2026-07 |                0.0283 |                     0.0415 |                 0.0316 |                      0.0468 |                 0.0337 |                      0.0518 |                 0.0335 |                      0.0443 |                  0.0332 |                       0.0375 |
| 2026-09 |                0.0327 |                     0.0445 |                 0.0358 |                      0.0501 |                 0.0351 |                      0.0533 |                 0.0342 |                      0.0447 |                  0.0335 |                       0.0376 |

---

## get_eiopa_symmetric_adjustment
Retrieves the symmetric adjustment of the equity capital charge of Solvency II, the "equity dampener" EIOPA publishes, daily from 1991, and the equity charges of the standard formula it results in. The adjustment raises the charge when equity prices are above their three-year average and lowers it when they are below, between -10% and +10%, so insurers are not forced to sell equities into a falling market. With get_eiopa_risk_free_rate it completes the market inputs of the standard formula's market risk module.

The formula is as follows:

$$
\text{Type}\; 1 \;\text{Equity Charge} = 0.39 + \text{Symmetric Adjustment},\;\; \text{for equities listed in the EEA or OECD}
$$

$$
\text{Type}\; 2 \;\text{Equity Charge} = 0.49 + \text{Symmetric Adjustment},\;\; \text{for other equities Every value is a decimal fraction (0.0771 for 7.71\%). No API key is needed. Weekly and monthly periods take the value on the last day of each period},\;\; \text{which is the value insurers apply at that reporting date}
$$

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
| 2026-09 |      0.0133 |          0.0091 |           0.0122 |  0.0015 |

---

## get_euribor_rates
Euribor rates, short for Euro Interbank Offered Rate, are the interest rates at which a panel of European banks lend funds to one another in the interbank market. These rates are fixed daily by the European Money Markets Institute (EMMI) and serve as a benchmark for various financial products and contracts, including mortgages, loans, and derivatives, across the Eurozone.

Euribor is fixed for maturities of one week to 12 months; this method returns the 1, 3, 6 and 12-month rates as monthly averages of the daily fixings, from the European Central Bank, as decimals. Longer maturities carry a term premium but also reflect where markets expect short rates to go, so the curve inverts when cuts are expected.

For more information, see for example: [https://data.ecb.europa.eu/data/datasets/FM/FM.M.U2.EUR.RT.MM.EURIBOR6MD_.HSTA](https://data.ecb.europa.eu/data/datasets/FM/FM.M.U2.EUR.RT.MM.EURIBOR6MD_.HSTA){:target="_blank"}

**Also known as:** euro interbank offered rate, eurozone money market.

**Args:**

- <u>maturities (str &#124; list &#124; None, optional):</u> The maturities to retrieve, from "1M", "3M", "6M" and "1Y",
as a list or a comma-separated string ("1M,3M").
Defaults to None, which retrieves all four.
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

With ample excess liquidity in the banking system the deposit facility rate is the rate that steers money markets: the euro short-term rate (€STR) trades just below it. The marginal lending rate forms the top of the corridor and the deposit facility rate the bottom, with the main refinancing rate in between; the main refinancing rate matters more when banks rely on the ECB's weekly operations for funding.

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

SOFR is the US dollar reference rate that replaced dollar LIBOR in loans and derivatives. Being secured by Treasuries, it usually trades a few basis points from the effective federal funds rate but jumps at month and quarter ends and when reserves get scarce, so the spread between its 1st and 99th percentiles, or between SOFR and the EFFR, is watched as a sign of strain in the repo market.

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

