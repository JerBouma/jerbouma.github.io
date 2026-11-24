---
title: Fixed Income
seo_title: "Bond and Fixed Income Analytics in Python | Finance Toolkit"
seo_title_suffix: false
excerpt: The Fixed Income module contains a wide variety of fixed income related calculations such as the Effective Yield, the Macaulay Duration, the Modified Duration Convexity, the Yield to Maturity and models such as Black and Bachelier to valuate derivative instruments such as Swaptions.
description: "Calculate bond yields, duration and convexity, fit yield curves and read Treasury, corporate and policy rates in Python with the Finance Toolkit."
author_profile: false
permalink: /projects/financetoolkit/docs/fixedincome
classes: wide-sidebar
layout: single
redirect_from:
    - /fixedincome
    - /projects/financetoolkit/fixed-income-notebook
    - /projects/financetoolkit/fixed-income-module
sidebar:
    nav: "financetoolkit-docs-fixedincome"
---

The Fixed Income module covers a wide variety of calculations including the Effective Yield, Macaulay Duration, Modified Duration, Convexity, Yield to Maturity and derivative pricing models such as Black and Bachelier (used for Swaptions and other instruments).

Use it in Claude, ChatGPT or another AI assistant through the [Finance Toolkit MCP](/projects/financetoolkit/mcp), or install the Python package:

```python
pip install financetoolkit -U
```

{% include docs-search.html %}

{% include financetoolkit-getting-started/fixed-income.md %}

## collect_bond_statistics
Collects the statistics of individual bonds from their market price: the yield to maturity, current yield, the Macaulay, modified, effective and dollar duration, DV01 and convexity, plus the present value on the Treasury zero-coupon curve and the Z-spread over it.

Treasuries come from the Treasury's daily FedInvest prices (see `get_treasury_securities`), corporate bonds from the holdings of bond ETFs (see `get_bond_universe`). Without bonds or an issuer the statistics are those of the benchmark Treasuries: the note or bond maturing closest to 2, 3, 5, 7, 10, 20 and 30 years after the price date, which is the latest issue of that maturity or one that matures a few months earlier. With only a maturity range they are those of every bill, note and bond maturing within it.

The fields are:

- Years to Maturity: counted on the bond's actual coupon dates, in actual days for Treasuries (actual/actual) and on the 30/360 Bond Basis for corporate bonds; a bill counts its days on a 365-day year.
- Accrued Interest: the coupon earned since the previous coupon date.
- Yield to Maturity: the rate that discounts the coupons and principal to the price plus the accrued interest, compounded twice a year.
- Current Yield: the annual coupon divided by the price.
- Macaulay's Duration: the weighted average time to receive the cash flows.
- Modified Duration: Macaulay's duration divided by 1 + YTM / 2.
- Effective Duration: the price change of a 1% move in the yield up and down.
- Dollar Duration: the modified duration times the full price, divided by 100.
- DV01: the price change, per 100 of par, of a one basis point move in the yield.
- Convexity: the second derivative of the price to the yield, divided by the price.
- Present Value: the clean price of the cash flows discounted with the Treasury zero-coupon curve of the price date.
- Z-Spread: the spread over that zero-coupon curve that prices the bond at its market price.

The formula is as follows:

$$
\operatorname{PV}(t) = \frac{\text{Cash Flow}(t)}{\left(1 + \frac{\text{YTM}}{2}\right)^{2t}},\;\; \text{with coupons of} \;\frac{\text{Coupon}}{2} \;\text{per 100 of par and the principal repaid with the last coupon}
$$

$$
\text{Dirty Price} = \sum(\operatorname{PV}(t)) = \text{Price} + \text{Accrued Interest},\;\; \text{over the remaining payment times } t \text{ in years}
$$

$$
\text{Current Yield} = \frac{\text{Coupon} \cdot 100}{\text{Price}}
$$

$$
\text{Macaulay's Duration} = \frac{\sum(t \cdot \operatorname{PV}(t))}{\text{Dirty Price}}
$$

$$
\text{Modified Duration} = \frac{\text{Macaulay's Duration}}{1 + \frac{\text{YTM}}{2}}
$$

$$
\text{Effective Duration} = \frac{\text{Dirty Price}(\text{YTM} - 0.01) - \text{Dirty Price}(\text{YTM} + 0.01)}{2 \cdot \text{Dirty Price} \cdot 0.01}
$$

$$
\text{Dollar Duration} = \frac{\text{Modified Duration} \cdot \text{Dirty Price}}{100}
$$

$$
\text{DV01} = \frac{\operatorname{Price}(\text{YTM} - 0.0001) - \operatorname{Price}(\text{YTM} + 0.0001)}{2}
$$

$$
\text{Convexity} = \frac{\text{Dirty Price}(\text{YTM} + 0.0001) + \text{Dirty Price}(\text{YTM} - 0.0001) - 2 \cdot \text{Dirty Price}}{\text{Dirty Price} \cdot 0.0001^{2}}
$$

$$
\text{Present Value} = \sum\left(\frac{\text{Cash Flow}(t)}{\left(1 + \frac{\text{Spot Rate}(t)}{2}\right)^{2t}}\right) - \text{Accrued Interest}
$$

$$
\text{Z-Spread solves Price} = \sum\left(\frac{\text{Cash Flow}(t)}{\left(1 + \frac{\text{Spot Rate}(t) + \text{Z-Spread}}{2}\right)^{2t}}\right) - \text{Accrued Interest}
$$

Where Spot Rate(t) is the Treasury zero-coupon rate of `get_zero_coupon_curve`, restated from annual to semi-annual compounding, interpolated linearly between the bills and the half-yearly coupon dates of the bootstrap, on which every par bond of the par yield curve prices at par. Bills pay no coupon and their yield is the bond-equivalent yield (see `get_bond_equivalent_yield`), simple interest up to half a year, so their durations and convexity follow from that pricing: a modified duration of t / (1 + YTM * t) up to half a year rather than t / (1 + YTM / 2). TIPS are priced on their inflation-adjusted principal, so their yield is a real yield and they have no present value or Z-spread on the nominal curve. Floating rate notes are left out.

To calculate these statistics for terms of your own, use the functions of `financetoolkit.fixedincome.bonds.bond_model` (get_bond_price, get_yield_to_maturity, get_macaulays_duration, get_modified_duration, get_effective_duration, get_dollar_duration, get_dv01, get_convexity and get_z_spread).

**Also known as:** bond data, fixed income statistics, bond analytics.

**Args:**

- <u>bonds (list[str] &#124; str &#124; None, optional):</u> CUSIPs or ISINs, a list or a
comma-separated string. Treasuries (CUSIPs starting with 912) come from
FedInvest, other bonds from the bond ETF holdings. Defaults to None.
- <u>issuer (list[str] &#124; str &#124; None, optional):</u> Part of an issuer's name, such as
"Apple", to select its bonds from the bond ETF holdings. Defaults to None.
- <u>etfs (list[str] &#124; str &#124; None, optional):</u> The bond ETFs whose holdings to select
bonds from, see `get_bond_universe`. Defaults to None, which reads LQD, IGSB
and USHY when bonds other than Treasuries or an issuer are given.
- <u>maturity_start (str &#124; None, optional):</u> The earliest maturity (YYYY-MM-DD).
Defaults to None.
- <u>maturity_end (str &#124; None, optional):</u> The latest maturity (YYYY-MM-DD). Defaults
to None.
- <u>date (str &#124; None, optional):</u> The day of the Treasury prices (YYYY-MM-DD). The
bond ETF holdings are always the latest. Defaults to None, the latest day
with prices.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results
to. Defaults to None, which uses the rounding of the class.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: One row per bond, indexed by CUSIP (Treasuries) or ISIN, with the
Issuer, Security Type, Coupon, Maturity, Price, Price Date and the statistics.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome()

statistics = fixedincome.collect_bond_statistics(date="2026-11-05")

statistics.iloc[[0, 2, 4, 6]].loc[:, "Maturity":].T
```

Which returns:

|                     | 91282CRU7   | 91282CRT0   | 91282CRF0   | 912810UW6   |
|:--------------------|:------------|:------------|:------------|:------------|
| Maturity            | 2028-10-31  | 2031-10-31  | 2036-08-15  | 2056-08-15  |
| Price               | 100.3125    | 100.6875    | 98.4375     | 98.125      |
| Price Date          | 2026-11-05  | 2026-11-05  | 2026-11-05  | 2026-11-05  |
| Years to Maturity   | 1.9862      | 4.9862      | 9.7772      | 29.7772     |
| Accrued Interest    | 0.0639      | 0.0656      | 1.0306      | 1.142       |
| Yield to Maturity   | 0.0446      | 0.0459      | 0.0483      | 0.0525      |
| Current Yield       | 0.0461      | 0.0472      | 0.047       | 0.0522      |
| Macaulay's Duration | 1.9195      | 4.4973      | 7.8771      | 15.2706     |
| Modified Duration   | 1.8777      | 4.3963      | 7.6914      | 14.8801     |
| Effective Duration  | 1.8779      | 4.3985      | 7.7036      | 15.0246     |
| Dollar Duration     | 1.8847      | 4.4294      | 7.6505      | 14.7715     |
| DV01                | 0.0188      | 0.0443      | 0.0765      | 0.1477      |
| Convexity           | 4.5145      | 22.7527     | 71.6857     | 333.2043    |
| Present Value       | 100.3147    | 100.7083    | 98.4039     | 98.098      |
| Z-Spread            | 0.0         | 0.0         | 0.0         | 0.0         |

---

## get_present_value
Calculates the present value of individual bonds: their coupons and principal discounted with the Treasury zero-coupon curve of the price date, next to the price they trade at. For a Treasury the two differ by how far the issue trades off the curve; for a corporate bond the present value is the price it would have without any credit or liquidity risk, and the gap with its price is what the Z-spread (`get_z_spread`) measures.

The formula is as follows:

$$
\text{Dirty Price} = \sum\left(\frac{C}{\left(1 + \frac{s(t_{i})}{2}\right)^{2 t_{i}}}\right) + \frac{F}{\left(1 + \frac{s(t_{n})}{2}\right)^{2 t_{n}}},\;\; \text{over}\;\; \text{the remaining coupons}\; i = 1,\; \ldots,\; n
$$

$$
\text{Accrued Interest} = C \cdot a
$$

$$
\text{Present Value} = \text{Dirty Price} - \text{Accrued Interest},\;\; \text{the clean price}
$$

where:

$$
C = \text{Coupon payment per half year},\;\; \frac{100 \cdot \text{Coupon}}{2}
$$

$$
s(t) = \text{Treasury zero-coupon rate at}\; t \;\text{years} \;(\text{get\_zero\_coupon\_curve}),\;\; \text{restated from annual to semi-annual compounding and interpolated linearly between the bills and the half-yearly coupon dates of the bootstrap}
$$

$$
a = \text{Elapsed fraction of the current coupon period},\;\; \text{0 on a coupon date}
$$

$$
t_{i} = \text{Time of the i-th cash flow in years},\;\; \text{on the bond's actual coupon dates}
$$

$$
F = \text{Face value of}\; 100
$$

The bonds are selected as in `collect_bond_statistics`: Treasuries by CUSIP from FedInvest, other bonds from the bond ETF holdings and, without bonds or an issuer, the benchmark Treasuries. TIPS have no present value on the nominal curve. To price terms of your own, use `bond_model.get_bond_price` (at one yield) or `bond_model.get_bond_price_from_curve` (on a curve).

**Also known as:** PV, bond pricing, discounted cash flows, theoretical price.

**Args:**

- <u>bonds (list[str] &#124; str &#124; None, optional):</u> CUSIPs or ISINs, see
`collect_bond_statistics`. Defaults to None.
- <u>issuer (list[str] &#124; str &#124; None, optional):</u> Part of an issuer's name, such as
"Apple". Defaults to None.
- <u>etfs (list[str] &#124; str &#124; None, optional):</u> The bond ETFs to select bonds from,
see `get_bond_universe`. Defaults to None.
- <u>maturity_start (str &#124; None, optional):</u> The earliest maturity (YYYY-MM-DD).
Defaults to None.
- <u>maturity_end (str &#124; None, optional):</u> The latest maturity (YYYY-MM-DD). Defaults
to None.
- <u>date (str &#124; None, optional):</u> The day of the Treasury prices (YYYY-MM-DD).
Defaults to None, the latest day with prices.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results
to. Defaults to None, which uses the rounding of the class.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: One row per bond with the Issuer, Security Type, Coupon, Maturity,
Price, Price Date and Present Value (per 100 of par).

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome()

present_values = fixedincome.get_present_value(date="2026-11-05")

present_values[["Coupon", "Maturity", "Price", "Present Value"]]
```

Which returns:

|           |   Coupon | Maturity   |    Price |   Present Value |
|:----------|---------:|:-----------|---------:|----------------:|
| 91282CRU7 |   0.0462 | 2028-10-31 | 100.312  |        100.315  |
| 91282CLR0 |   0.0412 | 2029-10-31 |  98.875  |         98.8812 |
| 91282CRT0 |   0.0475 | 2031-10-31 | 100.688  |        100.708  |
| 91282CRV5 |   0.0488 | 2033-10-31 | 101.062  |        101.04   |
| 91282CRF0 |   0.0462 | 2036-08-15 |  98.4375 |         98.4039 |
| 912810RU4 |   0.0288 | 2046-11-15 |  70.0312 |         69.9481 |
| 912810UW6 |   0.0512 | 2056-08-15 |  98.125  |         98.098  |

---

## get_duration
Calculates the duration of individual bonds at their yield to maturity. It has the option to calculate the following type of bond durations:

- Macaulay's Duration: The weighted average time to receive the bond's cash flows.
- Modified Duration: The Macaulay's duration divided by 1 plus the per-period yield (YTM / 2).
- Effective Duration: The percentage change in the bond price for a 1% change in the yield to maturity.
- Dollar Duration: The modified duration multiplied by the bond price, divided by 100.

These duration measures can be used to estimate the sensitivity of a bond's price to changes in interest rates as well as to compare the risk of different bonds. The modified duration is particularly useful for estimating the percentage change in the bond price for a 1% change in the yield to maturity. Note that it is a percentage sensitivity and therefore not the same as the dollar duration, the price value of a basis point (PVBP) or the dollar value of a 0.01% change (DV01), which are all expressed as a currency amount instead. The DV01 is part of `collect_bond_statistics`.

The formula is as follows (the default is the modified duration):

$$
\operatorname{PV}(t) = \frac{\text{Cash Flow}(t)}{\left(1 + \frac{\text{YTM}}{2}\right)^{2t}},\;\; \text{with coupons of} \;\frac{\text{Coupon}}{2} \;\text{per 100 of par and the principal repaid with the last coupon}
$$

$$
\text{Dirty Price} = \sum(\operatorname{PV}(t)),\;\; \text{over the remaining payment times } t \text{ in years on the actual coupon dates}
$$

$$
\text{Macaulay's Duration} = \frac{\sum(t \cdot \operatorname{PV}(t))}{\text{Dirty Price}}
$$

$$
\text{Modified Duration} = \frac{\text{Macaulay's Duration}}{1 + \frac{\text{YTM}}{2}}
$$

$$
\text{Effective Duration} = \frac{\text{Dirty Price}(\text{YTM} - 0.01) - \text{Dirty Price}(\text{YTM} + 0.01)}{2 \cdot \text{Dirty Price} \cdot 0.01}
$$

$$
\text{Dollar Duration} = \frac{\text{Modified Duration} \cdot \text{Dirty Price}}{100}
$$

Where YTM is the bond's yield to maturity at its market price, compounded twice a year (see `get_yield_to_maturity`). The bonds are selected as in `collect_bond_statistics`.

Modified duration is the first estimate of interest rate risk: a modified duration of 7 means the price falls by about 7% if the yield rises by one percentage point. The estimate worsens for larger moves, which convexity corrects (see `get_taylor_price_change`), and it assumes the cash flows are fixed. For callable bonds the relevant measure is an effective duration from a model that values the embedded option, which this method does not include. For terms of your own, use the duration functions of `bond_model`.

**Also known as:** Macaulay duration, modified duration, bond price sensitivity.

**Args:**

- <u>duration_type (str, optional):</u> The duration: "modified", "macaulay", "effective" or
"dollar". Defaults to "modified".
- <u>bonds (list[str] &#124; str &#124; None, optional):</u> CUSIPs or ISINs, see
`collect_bond_statistics`. Defaults to None.
- <u>issuer (list[str] &#124; str &#124; None, optional):</u> Part of an issuer's name, such as
"Apple". Defaults to None.
- <u>etfs (list[str] &#124; str &#124; None, optional):</u> The bond ETFs to select bonds from,
see `get_bond_universe`. Defaults to None.
- <u>maturity_start (str &#124; None, optional):</u> The earliest maturity (YYYY-MM-DD).
Defaults to None.
- <u>maturity_end (str &#124; None, optional):</u> The latest maturity (YYYY-MM-DD). Defaults
to None.
- <u>date (str &#124; None, optional):</u> The day of the Treasury prices (YYYY-MM-DD).
Defaults to None, the latest day with prices.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results
to. Defaults to None, which uses the rounding of the class.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: One row per bond with the Issuer, Security Type, Coupon, Maturity,
Price, Price Date and the duration (in years, or per 100 of par for the dollar
duration).

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome()

durations = fixedincome.get_duration(date="2026-11-05")

durations[["Security Type", "Coupon", "Maturity", "Price", "Modified Duration"]]
```

Which returns:

|           | Security Type   |   Coupon | Maturity   |    Price |   Modified Duration |
|:----------|:----------------|---------:|:-----------|---------:|--------------------:|
| 91282CRU7 | Note            |   0.0462 | 2028-10-31 | 100.312  |              1.8777 |
| 91282CLR0 | Note            |   0.0412 | 2029-10-31 |  98.875  |              2.7748 |
| 91282CRT0 | Note            |   0.0475 | 2031-10-31 | 100.688  |              4.3963 |
| 91282CRV5 | Note            |   0.0488 | 2033-10-31 | 101.062  |              5.8687 |
| 91282CRF0 | Note            |   0.0462 | 2036-08-15 |  98.4375 |              7.6914 |
| 912810RU4 | Bond            |   0.0288 | 2046-11-15 |  70.0312 |             13.6289 |
| 912810UW6 | Bond            |   0.0512 | 2056-08-15 |  98.125  |             14.8801 |

---

## get_yield_to_maturity
Calculates the yield to maturity of individual bonds from their market price. The yield to maturity is the internal rate of return of the bond, the discount rate that equates the present value of the bond's cash flows to its price.

The formula is as follows, solved for YTM:

$$
\text{Price} + C \cdot a = \sum\left(\frac{C}{\left(1 + \frac{\text{YTM}}{2}\right)^{2 t_{i}}}\right) + \frac{F}{\left(1 + \frac{\text{YTM}}{2}\right)^{2 t_{n}}},\;\; \text{over}\;\; \text{the remaining coupons}\; i = 1,\; \ldots,\; n
$$

where:

$$
C = \text{Coupon payment per half year},\;\; \frac{100 \cdot \text{Coupon}}{2}
$$

$$
a = \text{Elapsed fraction of the current coupon period},\;\; \text{in actual days for Treasuries (actual/actual) and on the 30/360 Bond Basis for corporate bonds, 0 on a coupon date}
$$

$$
t_{i} = \text{Time of the i-th cash flow in years},\;\; \text{on the bond's actual coupon dates}
$$

$$
F = \text{Face value of}\; 100
$$

The yield is a nominal annual rate compounded twice a year (bond-equivalent), as the Treasury and US corporate bond markets quote it, solved with the secant method. For a bill it is the bond-equivalent yield of its discount price (see `get_bond_equivalent_yield`), for TIPS the real yield. The bonds are selected as in `collect_bond_statistics`. For terms of your own, use `bond_model.get_yield_to_maturity`.

The yield to maturity is the return of a bond bought at this price and held to maturity, if every coupon is reinvested at the same yield and the issuer pays in full. It is the standard way to quote and compare bonds, but it is one average rate for all cash flows: bonds with the same maturity but different coupons have different yields even when both are priced in line with the same spot curve, which the Z-spread (`get_z_spread`) accounts for. For callable bonds the yield to worst is quoted instead, which `bond_model.get_yield_to_worst` calculates from a call schedule.

**Also known as:** YTM, bond return to maturity, redemption yield.

**Args:**

- <u>bonds (list[str] &#124; str &#124; None, optional):</u> CUSIPs or ISINs, see
`collect_bond_statistics`. Defaults to None.
- <u>issuer (list[str] &#124; str &#124; None, optional):</u> Part of an issuer's name, such as
"Apple". Defaults to None.
- <u>etfs (list[str] &#124; str &#124; None, optional):</u> The bond ETFs to select bonds from,
see `get_bond_universe`. Defaults to None.
- <u>maturity_start (str &#124; None, optional):</u> The earliest maturity (YYYY-MM-DD).
Defaults to None.
- <u>maturity_end (str &#124; None, optional):</u> The latest maturity (YYYY-MM-DD). Defaults
to None.
- <u>date (str &#124; None, optional):</u> The day of the Treasury prices (YYYY-MM-DD).
Defaults to None, the latest day with prices.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results
to. Defaults to None, which uses the rounding of the class.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: One row per bond with the Issuer, Security Type, Coupon, Maturity,
Price, Price Date and Yield to Maturity (decimal).

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome()

yields = fixedincome.get_yield_to_maturity(date="2026-11-05")

yields[["Security Type", "Coupon", "Maturity", "Price", "Yield to Maturity"]]
```

Which returns:

| Bond      | Security Type   |   Coupon | Maturity   |    Price |   Yield to Maturity |
|:----------|:----------------|---------:|:-----------|---------:|--------------------:|
| 91282CRU7 | Note            |   0.0462 | 2028-10-31 | 100.312  |              0.0446 |
| 91282CLR0 | Note            |   0.0412 | 2029-10-31 |  98.875  |              0.0453 |
| 91282CRT0 | Note            |   0.0475 | 2031-10-31 | 100.688  |              0.0459 |
| 91282CRV5 | Note            |   0.0488 | 2033-10-31 | 101.062  |              0.0469 |
| 91282CRF0 | Note            |   0.0462 | 2036-08-15 |  98.4375 |              0.0483 |
| 912810RU4 | Bond            |   0.0288 | 2046-11-15 |  70.0312 |              0.0533 |
| 912810UW6 | Bond            |   0.0512 | 2056-08-15 |  98.125  |              0.0525 |

---

## get_z_spread
Calculates the zero-volatility spread (Z-spread) of individual bonds over the Treasury zero-coupon curve. The Z-spread is the constant spread that, when added uniformly to every point of the curve, makes the present value of the bond's cash flows equal to its price.

Unlike a simple yield spread (the bond's yield to maturity minus a Treasury yield of the same maturity, the G-spread of `get_bond_universe`), the Z-spread is measured against the entire curve rather than a single point, which makes it a more accurate measure of the compensation an investor receives for a bond's credit and liquidity risk. For a Treasury it shows how far the issue trades off the curve, typically a few basis points.

The formula is as follows, solved for the Z-Spread with the secant method:

$$
\text{Price} = \sum\left(\frac{\text{Cash Flow}(t)}{\left(1 + \frac{\text{Spot Rate}(t) + \text{Z-Spread}}{2}\right)^{2t}}\right) - \text{Accrued Interest}
$$

Where each coupon is 100 * Coupon / 2, the principal is repaid with the last coupon, t is each remaining payment time in years on the bond's actual coupon dates and Spot Rate(t) is the Treasury zero-coupon rate of the price date (`get_zero_coupon_curve`), restated from annual to semi-annual compounding, interpolated linearly between the bills and the half-yearly coupon dates of the bootstrap and held flat beyond its first and last maturity.

The bonds are selected as in `collect_bond_statistics`. TIPS have no Z-spread on the nominal curve. For a bond with an embedded option the Z-spread includes the option's value, which an option-adjusted spread removes: the ICE BofA option-adjusted spreads of bond indices are in `get_ice_bofa_option_adjusted_spread`, and `short_rate_model.get_option_adjusted_spread` calculates one for a call schedule of your own. For terms of your own, use `bond_model.get_z_spread`.

**Also known as:** zero-volatility spread, static spread, credit spread.

**Args:**

- <u>bonds (list[str] &#124; str &#124; None, optional):</u> CUSIPs or ISINs, see
`collect_bond_statistics`. Defaults to None.
- <u>issuer (list[str] &#124; str &#124; None, optional):</u> Part of an issuer's name, such as
"Apple". Defaults to None.
- <u>etfs (list[str] &#124; str &#124; None, optional):</u> The bond ETFs to select bonds from,
see `get_bond_universe`. Defaults to None.
- <u>maturity_start (str &#124; None, optional):</u> The earliest maturity (YYYY-MM-DD).
Defaults to None.
- <u>maturity_end (str &#124; None, optional):</u> The latest maturity (YYYY-MM-DD). Defaults
to None.
- <u>date (str &#124; None, optional):</u> The day of the Treasury prices (YYYY-MM-DD).
Defaults to None, the latest day with prices.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results
to. Defaults to None, which uses the rounding of the class.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: One row per bond with the Issuer, Security Type, Coupon, Maturity,
Price, Price Date and Z-Spread (decimal, compounded twice a year).

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome(api_key="FINANCIAL_MODELING_PREP_KEY")

z_spreads = fixedincome.get_z_spread(
    issuer="Apple", maturity_start="2030-01-01", maturity_end="2035-12-31"
)

z_spreads[["Issuer", "Coupon", "Maturity", "Price", "Price Date", "Z-Spread"]]
```

Which returns:

|              | Issuer    |   Coupon | Maturity   |   Price | Price Date   |   Z-Spread |
|:-------------|:----------|---------:|:-----------|--------:|:-------------|-----------:|
| US037833EU05 | APPLE INC |   0.0415 | 2030-05-10 |  97.47  | 2026-11-20   |     0.0029 |
| US037833DU14 | APPLE INC |   0.0165 | 2030-05-11 |  89.625 | 2026-11-20   |     0.0027 |
| US037833EZ91 | APPLE INC |   0.042  | 2030-05-12 |  97.865 | 2026-11-20   |     0.0021 |
| US037833DY36 | APPLE INC |   0.0125 | 2030-08-20 |  87.44  | 2026-11-20   |     0.0029 |
| US037833ED89 | APPLE INC |   0.0165 | 2031-02-08 |  87.36  | 2026-11-20   |     0.0032 |
| US037833EJ59 | APPLE INC |   0.017  | 2031-08-05 |  86.265 | 2026-11-20   |     0.0031 |
| US037833FG02 | APPLE INC |   0.049  | 2031-11-09 |  99.495 | 2026-11-20   |     0.0031 |
| US037833FA32 | APPLE INC |   0.045  | 2032-05-12 |  97.5   | 2026-11-20   |     0.003  |
| US037833EP10 | APPLE INC |   0.0335 | 2032-08-08 |  91.8   | 2026-11-20   |     0.0027 |
| US037833EV87 | APPLE INC |   0.043  | 2033-05-10 |  95.59  | 2026-11-20   |     0.0033 |
| US037833FH84 | APPLE INC |   0.051  | 2033-11-09 |  98.93  | 2026-11-20   |     0.0049 |
| US037833FB15 | APPLE INC |   0.0475 | 2035-05-12 |  96.88  | 2026-11-20   |     0.0035 |

---

## get_key_rate_duration
Calculates the key rate durations of individual bonds on the Treasury zero-coupon curve: the price sensitivity to a shock at a single maturity ("key rate") of the curve while every other point is held fixed. Whereas `get_duration` with `duration_type='effective'` assumes the entire curve shifts in parallel, key rate durations show which segment of the curve a bond's price is exposed to. Because cash flows are discounted using linear interpolation between the curve's maturities, a shock at an inner maturity tapers off towards its neighbours and has no effect beyond them. The curve is held flat beyond its first and last maturities, so a shock at the first maturity moves every cash flow paid before it in full (and a shock at the last maturity every cash flow paid after it).

Summing the key rate durations across every maturity of the curve approximately reproduces the bond's effective (parallel-shift) duration on the curve. A barbell and a bullet with the same duration have very different key rate profiles and react differently when the curve steepens or flattens, which is why key rate durations are hedged with instruments at each key maturity. The profile also depends on which maturities the curve contains: the same bond shows different key rate durations on a curve with more or fewer points.

The formula is as follows:

$$
\text{Dirty Price} = \sum\left(\frac{\text{Cash Flow}(t)}{\left(1 + \frac{\text{Spot Rate}(t)}{2}\right)^{2t}}\right)
$$

$$
\text{Key Rate Duration} = - \frac{\text{Dirty Price}(\text{Key Rate} + \Delta y) - \text{Dirty Price}(\text{Key Rate} - \Delta y)}{2 \cdot \text{Dirty Price} \cdot \Delta y}
$$

Where each coupon is 100 * Coupon / 2, the principal is repaid with the last coupon, t is each remaining payment time in years on the bond's actual coupon dates, Spot Rate(t) is the Treasury zero-coupon rate of the price date (`get_zero_coupon_curve`), restated from annual to semi-annual compounding and interpolated linearly between the maturities the Treasury quotes (the key rates), and $$\Delta y$$ is the shock applied to the key rate only (1 basis point by default).

The bonds are selected as in `collect_bond_statistics`; TIPS have no key rate durations on the nominal curve. For terms or a curve of your own, use `bond_model.get_key_rate_duration`.

**Also known as:** partial duration, rate-specific duration, curve risk.

**Args:**

- <u>key_rate_maturity (float &#124; str &#124; list &#124; None, optional):</u> The maturities of the Treasury
curve to shock, in years or as labels such as '2Y' (one of the curve's maturities:
1M, 1.5M, 2M, 3M, 4M, 6M, 1Y, 2Y, 3Y, 5Y, 7Y, 10Y, 20Y and 30Y). Defaults to None,
which shocks every maturity of the curve.
- <u>yield_change (float, optional):</u> The shock to each key rate (decimal). Defaults to 0.0001.
- <u>bonds (list[str] &#124; str &#124; None, optional):</u> CUSIPs or ISINs, see
`collect_bond_statistics`. Defaults to None.
- <u>issuer (list[str] &#124; str &#124; None, optional):</u> Part of an issuer's name, such as
"Apple". Defaults to None.
- <u>etfs (list[str] &#124; str &#124; None, optional):</u> The bond ETFs to select bonds from,
see `get_bond_universe`. Defaults to None.
- <u>maturity_start (str &#124; None, optional):</u> The earliest maturity (YYYY-MM-DD).
Defaults to None.
- <u>maturity_end (str &#124; None, optional):</u> The latest maturity (YYYY-MM-DD). Defaults
to None.
- <u>date (str &#124; None, optional):</u> The day of the Treasury prices (YYYY-MM-DD).
Defaults to None, the latest day with prices.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results
to. Defaults to None, which uses the rounding of the class.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: One row per bond with the Issuer, Security Type, Coupon, Maturity,
Price, Price Date and a key rate duration per key rate maturity (in years).

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome()

key_rates = fixedincome.get_key_rate_duration(
    key_rate_maturity=["2Y", "5Y", "10Y", "30Y"], date="2026-11-05"
)

key_rates[["Coupon", "Maturity", "2Y", "5Y", "10Y", "30Y"]]
```

Which returns:

|           |   Coupon | Maturity   |     2Y |     5Y |    10Y |    30Y |
|:----------|---------:|:-----------|-------:|-------:|-------:|-------:|
| 91282CRU7 |   0.0462 | 2028-10-31 | 1.8043 | 0      | 0      | 0      |
| 91282CLR0 |   0.0412 | 2029-10-31 | 0.1101 | 0      | 0      | 0      |
| 91282CRT0 |   0.0475 | 2031-10-31 | 0.0842 | 4.0372 | 0      | 0      |
| 91282CRV5 |   0.0488 | 2033-10-31 | 0.0861 | 0.4068 | 0      | 0      |
| 91282CRF0 |   0.0462 | 2036-08-15 | 0.083  | 0.3598 | 5.9559 | 0      |
| 912810RU4 |   0.0288 | 2046-11-15 | 0.072  | 0.3122 | 1.6649 | 0.0255 |
| 912810UW6 |   0.0512 | 2056-08-15 | 0.0922 | 0.3998 | 2.1327 | 7.5183 |

---

## get_bucketed_delta
Calculates the bucketed delta of individual bonds on the Treasury curve: the change in each bond's present value, per 100 of par, when one maturity of the curve rises by a basis point, for every maturity the Treasury quotes. Where `get_key_rate_duration` shocks a zero-coupon rate with a tent around it, these deltas move the rates traders hedge with.

With method="par" (the par-rate delta) one par yield of the Treasury par curve rises by a basis point and the zero-coupon curve is bootstrapped again, so the deltas are the sensitivities to the notes and bonds of each maturity: a par bond maturing at a quoted maturity has a delta to that maturity only. They follow from the chain rule through the par-to-zero Jacobian of the bootstrap (see `curve_risk_model.get_par_rate_delta`):

$$
\text{PV} = \sum(\operatorname{CF}(t) \cdot (1 + \text{Zero Rate}(t))^{- t})
$$

$$
\text{Par Rate} \;\Delta(i) = \sum_{j}\left(\frac{\frac{\text{dPV}}{\text{dZero Rate}(j)} \cdot \text{dZero Rate}(j)}{\text{dPar Yield}(i)}\right) \cdot 0.0001
$$

With method="forward" (the forward-rate delta) the continuously compounded instantaneous forward rate between two neighbouring quoted maturities rises by a basis point, which moves every discount factor beyond it as well (see `curve_risk_model.get_forward_rate_delta`):

$$
\text{Forward Rate} \;\Delta(i) = \sum(\operatorname{CF}(t) \cdot (1 + \text{Zero Rate}(t))^{- t} \cdot - \operatorname{Overlap}(t,\; i)) \cdot 0.0001
$$

Where CF(t) are the bond's coupons (100 * Coupon / 2) and principal on its actual coupon dates, Zero Rate(t) is the Treasury zero-coupon curve of the price date (annually compounded, bootstrapped from the par yields with the zero rate of every coupon date, see `get_zero_coupon_curve`, and interpolated linearly), and Overlap(t, i) is the part of the bucket of maturity i (from the previous quoted maturity to i, the first from today and the last without an end) before t. The par yields are bond-equivalent yields, compounded twice a year beyond a year. The bump of the differences is 1 basis point by default; the deltas are always per +1 basis point, in dollars per 100 of par, negative for a long position. Summed over the maturities they give the change for a parallel shift of the par curve (par) or of the continuously compounded zero rates (forward). The bonds are discounted on the Treasury curve without a spread and selected as in `collect_bond_statistics`; TIPS have no delta on the nominal curve. For cash flows or a curve of your own, use `curve_risk_model`.

**Also known as:** bucketed PV01, par-rate risk, forward-rate risk, DV01 ladder, partial DV01.

**Args:**

- <u>method (Literal["par", "forward"], optional):</u> "par" for the par-rate delta or
"forward" for the forward-rate delta. Defaults to "par".
- <u>bump (float, optional):</u> The move of a rate up and down in the differences (decimal).
Defaults to 0.0001.
- <u>bonds (list[str] &#124; str &#124; None, optional):</u> CUSIPs or ISINs, see
`collect_bond_statistics`. Defaults to None.
- <u>issuer (list[str] &#124; str &#124; None, optional):</u> Part of an issuer's name, such as
"Apple". Defaults to None.
- <u>etfs (list[str] &#124; str &#124; None, optional):</u> The bond ETFs to select bonds from,
see `get_bond_universe`. Defaults to None.
- <u>maturity_start (str &#124; None, optional):</u> The earliest maturity (YYYY-MM-DD).
Defaults to None.
- <u>maturity_end (str &#124; None, optional):</u> The latest maturity (YYYY-MM-DD). Defaults
to None.
- <u>date (str &#124; None, optional):</u> The day of the Treasury prices (YYYY-MM-DD).
Defaults to None, the latest day with prices.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results
to. Defaults to None, which uses the rounding of the class.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: One row per bond with the Issuer, Security Type, Coupon, Maturity,
Price, Price Date and a delta per maturity of the Treasury curve.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome()

deltas = fixedincome.get_bucketed_delta(date="2026-11-05")

deltas[["Maturity", "2Y", "3Y", "5Y", "7Y", "10Y", "20Y", "30Y"]]
```

Which returns:

|           | Maturity   |      2Y |      3Y |      5Y |      7Y |     10Y |     20Y |     30Y |
|:----------|:-----------|--------:|--------:|--------:|--------:|--------:|--------:|--------:|
| 91282CRU7 | 2028-10-31 | -0.0186 |  0      |  0      |  0      |  0      |  0      |  0      |
| 91282CLR0 | 2029-10-31 | -0.0003 | -0.0272 |  0      |  0      |  0      |  0      |  0      |
| 91282CRT0 | 2031-10-31 |  0      | -0.0004 | -0.044  |  0      |  0      |  0      |  0      |
| 91282CRV5 | 2033-10-31 |  0      | -0.0001 | -0.0005 | -0.0589 |  0      |  0      |  0      |
| 91282CRF0 | 2036-08-15 |  0      |  0.0001 |  0.0001 | -0.0054 | -0.0718 |  0      |  0      |
| 912810RU4 | 2046-11-15 |  0.0002 |  0.0005 |  0.001  |  0.0019 |  0.0097 | -0.1131 | -0.0003 |
| 912810UW6 | 2056-08-15 |  0      |  0      |  0      |  0.0001 |  0.0003 | -0.0024 | -0.1471 |

---

## get_rate_shift_ladder
Calculates the parallel shift ladder of individual bonds on the Treasury zero-coupon curve: the profit or loss, per 100 of par, when the whole curve shifts up or down by each of a range of amounts, with the bond's delta and gamma to the shift. Where duration and convexity extrapolate from today's curve, the ladder reprices the bond at every shift, so it shows the full, asymmetric response to large moves.

The formula is as follows:

$$
\operatorname{PV}(\Delta) = \sum(\operatorname{CF}(t) \cdot (1 + \text{Zero Rate}(t) + \Delta)^{- t})
$$

$$
\operatorname{P\&L}(\Delta) = \operatorname{PV}(\Delta) - \operatorname{PV}(0)
$$

$$
\Delta = \frac{\operatorname{PV}(+ h) - \operatorname{PV}(- h)}{2h}
$$

$$
\Gamma = \frac{\operatorname{PV}(+ h) - 2 \cdot \operatorname{PV}(0) + \operatorname{PV}(- h)}{h^{2}}
$$

Where CF(t) are the bond's coupons (100 * Coupon / 2) and principal on its actual coupon dates, Zero Rate(t) is the Treasury zero-coupon curve of the price date (annually compounded, see `get_zero_coupon_curve`, interpolated linearly), so Δ shifts annually compounded zero rates, and h is 1 basis point. Delta and Gamma are per unit of rate, so P&L(Δ) ≈ Delta * Δ + $$0.5 \cdot \text{Gamma} \cdot \Delta^{2}$$ with Δ as a decimal: a Delta of -700 loses 0.07 for a 1 basis point rise. The bonds are discounted on the Treasury curve without a spread and selected as in `collect_bond_statistics`; TIPS have no ladder on the nominal curve. For cash flows or a curve of your own, and the delta and gamma at every shift, use `curve_risk_model.get_parallel_shift_ladder`.

**Also known as:** parallel shift report, scenario ladder, PV ladder, dollar gamma.

**Args:**

- <u>shifts (list[float] &#124; str &#124; None, optional):</u> The parallel shifts (decimals), e.g.
[-0.01, 0.01]; a shift of 0 (today's curve, the P&L of which is 0) and repeated
shifts are left out. Defaults to None, -200, -100, -50, -25, 25, 50, 100 and 200
basis points.
- <u>bonds (list[str] &#124; str &#124; None, optional):</u> CUSIPs or ISINs, see
`collect_bond_statistics`. Defaults to None.
- <u>issuer (list[str] &#124; str &#124; None, optional):</u> Part of an issuer's name, such as
"Apple". Defaults to None.
- <u>etfs (list[str] &#124; str &#124; None, optional):</u> The bond ETFs to select bonds from,
see `get_bond_universe`. Defaults to None.
- <u>maturity_start (str &#124; None, optional):</u> The earliest maturity (YYYY-MM-DD).
Defaults to None.
- <u>maturity_end (str &#124; None, optional):</u> The latest maturity (YYYY-MM-DD). Defaults
to None.
- <u>date (str &#124; None, optional):</u> The day of the Treasury prices (YYYY-MM-DD).
Defaults to None, the latest day with prices.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results
to. Defaults to None, which uses the rounding of the class.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: One row per bond with the Issuer, Security Type, Coupon, Maturity,
Price, Price Date, the P&L of every shift (labelled in basis points, such as '-100bp')
and the Delta and Gamma.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome()

ladder = fixedincome.get_rate_shift_ladder(date="2026-11-05")

ladder[["Maturity", "-200bp", "-50bp", "+50bp", "+200bp", "Delta", "Gamma"]]
```

Which returns:

|           | Maturity   |   -200bp |   -50bp |   +50bp |   +200bp |     Delta |     Gamma |
|:----------|:-----------|---------:|--------:|--------:|---------:|----------:|----------:|
| 91282CRU7 | 2028-10-31 |   3.7943 |  0.9284 | -0.9153 |  -3.5854 |  -184.36  |   521.782 |
| 91282CLR0 | 2029-10-31 |   5.5767 |  1.3548 | -1.3296 |  -5.1732 |  -268.428 |  1007.8   |
| 91282CRT0 | 2031-10-31 |   9.1613 |  2.1953 | -2.1354 |  -8.2008 |  -433.002 |  2397.28  |
| 91282CRV5 | 2033-10-31 |  12.4756 |  2.9498 | -2.8448 | -10.791  |  -579.318 |  4200.65  |
| 91282CRF0 | 2036-08-15 |  16.4436 |  3.8178 | -3.6394 | -13.579  |  -745.4   |  7130.76  |
| 912810RU4 | 2046-11-15 |  22.4745 |  4.8882 | -4.4764 | -15.7994 |  -935.114 | 16459.8   |
| 912810UW6 | 2056-08-15 |  35.7437 |  7.4714 | -6.6913 | -22.9696 | -1412.9   | 31157.5   |

---

## get_taylor_price_change
Estimates the percentage change in the price of individual bonds for a change in their yield, using a second-order Taylor series expansion that combines modified duration and convexity. With a from_date, the yield change is each bond's own change in yield from that day to the price date, and the realised change of its market price sits next to the estimate.

Modified duration alone only captures the first-order (linear) relationship between a bond's price and its yield, which understates the price increase for a yield decrease and overstates the price decrease for a yield increase because the true price-yield relationship is curved (convex), not linear. Adding a convexity term corrects for this and produces a substantially more accurate estimate, especially for larger yield changes.

The formula is as follows:

$$
\text{Modified Duration} = \frac{\frac{\sum(t \cdot \operatorname{PV}(t))}{\text{Dirty Price}}}{1 + \frac{\text{YTM}}{2}},\;\; \text{see get\_duration}
$$

$$
\text{Convexity} = \frac{\text{Dirty Price}(\text{YTM} + 0.0001) + \text{Dirty Price}(\text{YTM} - 0.0001) - 2 \cdot \text{Dirty Price}}{\text{Dirty Price} \cdot 0.0001^{2}}
$$

$$
\% \Delta \;\text{Price} \approx - \text{Modified Duration} \cdot \Delta y + 0.5 \cdot \text{Convexity} \cdot \Delta y^{2}
$$

Where YTM is the bond's yield to maturity at its market price, compounded twice a year (see `get_yield_to_maturity`), $$\Delta y$$ is the yield change (0.01 by default) and %ΔPrice is the change of the full (dirty) price as a decimal. The bonds are selected as in `collect_bond_statistics`. For terms of your own, use `bond_model.get_taylor_price_change`.

With a from_date, the Treasuries are selected on from_date (so the benchmark Treasuries are those that already traded then) and priced again on the price date (`date`):

$$
\text{Yield Change} = \operatorname{YTM}(\text{date}) - \operatorname{YTM}(\text{from\_date})
$$

$$
\text{Price Change} = \text{the Taylor estimate above},\;\; \text{with the modified duration},\;\; \text{convexity and YTM of}\; \text{from\_date} \;\text{and} \;\Delta y = \text{Yield Change}
$$

$$
\text{Realised Price Change} = \frac{\operatorname{Price}(\text{date})}{\operatorname{Price}(\text{from\_date})} - 1,\;\; \text{on the clean FedInvest prices}
$$

The Taylor estimate holds the time to maturity fixed, while the realised change also includes the pull of the price towards par over the period and is measured on the clean price, so the two differ slightly even for a small yield change; over a few days the difference is mostly the approximation itself. Only Treasuries have prices on earlier days, so other bonds are left out.

**Also known as:** duration-convexity approximation, second-order price approximation, realised bond price change.

**Args:**

- <u>yield_change (float &#124; None, optional):</u> The change in the yield to maturity (decimal),
negative for a fall. Defaults to None, which is 0.01, or each bond's own yield change
since from_date when that is given.
- <u>bonds (list[str] &#124; str &#124; None, optional):</u> CUSIPs or ISINs, see
`collect_bond_statistics`. Defaults to None.
- <u>issuer (list[str] &#124; str &#124; None, optional):</u> Part of an issuer's name, such as
"Apple". Defaults to None.
- <u>etfs (list[str] &#124; str &#124; None, optional):</u> The bond ETFs to select bonds from,
see `get_bond_universe`. Defaults to None.
- <u>maturity_start (str &#124; None, optional):</u> The earliest maturity (YYYY-MM-DD).
Defaults to None.
- <u>maturity_end (str &#124; None, optional):</u> The latest maturity (YYYY-MM-DD). Defaults
to None.
- <u>date (str &#124; None, optional):</u> The day of the Treasury prices (YYYY-MM-DD); a weekend or
holiday uses the business day before it. Defaults to None, the latest day with prices.
- <u>from_date (str &#124; None, optional):</u> The day (YYYY-MM-DD) to measure each Treasury's yield
and price change from, up to `date`; a weekend or holiday uses the business day before
it. Defaults to None, which estimates the price change for yield_change instead.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results
to. Defaults to None, which uses the rounding of the class.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: One row per bond with the Issuer, Security Type, Coupon, Maturity,
Price, Price Date and Price Change (decimal); with a from_date the From Price and
From Date before the Price and Price Date, followed by the Yield Change, Price Change
and Realised Price Change, all decimals.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome()

price_changes = fixedincome.get_taylor_price_change(yield_change=0.01, date="2026-11-05")

price_changes[["Security Type", "Coupon", "Maturity", "Price", "Price Change"]]
```

Which returns:

|           | Security Type   |   Coupon | Maturity   |    Price |   Price Change |
|:----------|:----------------|---------:|:-----------|---------:|---------------:|
| 91282CRU7 | Note            |   0.0462 | 2028-10-31 | 100.312  |        -0.0186 |
| 91282CLR0 | Note            |   0.0412 | 2029-10-31 |  98.875  |        -0.0273 |
| 91282CRT0 | Note            |   0.0475 | 2031-10-31 | 100.688  |        -0.0428 |
| 91282CRV5 | Note            |   0.0488 | 2033-10-31 | 101.062  |        -0.0567 |
| 91282CRF0 | Note            |   0.0462 | 2036-08-15 |  98.4375 |        -0.0733 |
| 912810RU4 | Bond            |   0.0288 | 2046-11-15 |  70.0312 |        -0.1242 |
| 912810UW6 | Bond            |   0.0512 | 2056-08-15 |  98.125  |        -0.1321 |

The price changes of the benchmark Treasuries from 28 October to 6 November 2026, each
for its own yield change:

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome()

price_changes = fixedincome.get_taylor_price_change(from_date="2026-10-28", date="2026-11-06")

price_changes.loc[:, "Maturity":].drop(columns=["From Date", "Price Date"])
```



|           | Maturity   |   From Price |   Price |   Yield Change |   Price Change |   Realised Price Change |
|:----------|:-----------|-------------:|--------:|---------------:|---------------:|------------------------:|
| 91282CDF5 | 2028-10-31 |      93.6562 | 94.0938 |        -0.002  |         0.0039 |                  0.0047 |
| 91282CLR0 | 2029-10-31 |      98.0938 | 98.7188 |        -0.0022 |         0.0061 |                  0.0064 |
| 91282CLU3 | 2031-10-31 |      96.6562 | 97.6562 |        -0.0023 |         0.01   |                  0.0103 |
| 91282CJJ1 | 2033-11-15 |      97.3438 | 98.5312 |        -0.002  |         0.0119 |                  0.0122 |
| 91282CRF0 | 2036-08-15 |      96.7812 | 98.2188 |        -0.0019 |         0.0147 |                  0.0149 |
| 912810RU4 | 2046-11-15 |      68.6875 | 69.9062 |        -0.0012 |         0.0171 |                  0.0177 |
| 912810UW6 | 2056-08-15 |      96.375  | 97.9688 |        -0.0011 |         0.0164 |                  0.0165 |

---

## get_bond_equivalent_yield
Calculates the bond-equivalent yield (BEY) of every Treasury bill from its price. Bills are quoted on a discount-yield basis, which understates the return an investor earns because it is computed on face value rather than the (lower) purchase price, and uses a 360-day rather than a 365-day year. The bond-equivalent yield restates the discount yield on a basis that is comparable to coupon-bearing notes and bonds.

The formula is as follows:

$$
\text{Discount Yield} = \frac{\frac{100 - \text{Price}}{100} \cdot 360}{\text{Days to Maturity}}
$$

$$
\text{BEY} = \frac{365 \cdot \text{Discount Yield}}{360 - \text{Days to Maturity} \cdot \text{Discount Yield}},\;\; \text{for 182.5 days or less}
$$

$$
\text{BEY} = \frac{- 2t + 2 \cdot \sqrt{t^{2} - (2t - 1) \cdot \left(1 - \frac{100}{\text{Price}}\right)}}{2t - 1},\;\; \text{with}\;\; t = \frac{\text{Days to Maturity}}{365},\;\; \text{for more than 182.5 days}
$$

A bill with half a year or less remaining takes the simple restatement onto the purchase price and a 365-day year. Beyond that an equivalent coupon-bearing note would have paid a coupon at the six month point, so the U.S. Treasury's semi-annually compounded solution (31 CFR 356, Appendix B) is used instead. Applying the simple formula to a 52-week bill instead overstates its yield, by about 4 to 7 basis points at discount yields of 4 to 5% (4.2265% instead of 4.1829% at a 4% discount yield).

The prices are the Treasury's daily FedInvest prices, see `get_treasury_securities`. To convert a discount yield of your own, use `bond_model.get_bond_equivalent_yield`.

**Also known as:** BEY, coupon-equivalent yield, investment rate, T-bill yield.

**Args:**

- <u>bonds (list[str] &#124; str &#124; None, optional):</u> The CUSIPs (or US ISINs) of the bills,
a list or a comma-separated string. Defaults to None, every bill.
- <u>date (str &#124; None, optional):</u> The day of the prices (YYYY-MM-DD). Defaults to None,
the latest day with prices.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results
to. Defaults to None, which uses the rounding of the class.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: One row per bill, indexed by CUSIP, with the Maturity, Days to
Maturity, Price, Discount Yield, Bond-Equivalent Yield and Price Date.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome()

bills = fixedincome.get_bond_equivalent_yield(date="2026-11-05")

bills.iloc[::4, :-1]
```

Which returns:

| CUSIP     | Maturity   |   Days to Maturity |   Price |   Discount Yield |   Bond-Equivalent Yield |
|:----------|:-----------|-------------------:|--------:|-----------------:|------------------------:|
| 912797VW4 | 2026-11-10 |                  5 | 99.9576 |           0.0306 |                  0.031  |
| 912797VY0 | 2026-11-24 |                 19 | 99.8075 |           0.0365 |                  0.0371 |
| 912797WE3 | 2026-12-08 |                 33 | 99.6551 |           0.0376 |                  0.0383 |
| 912797WG8 | 2026-12-22 |                 47 | 99.4978 |           0.0385 |                  0.0392 |
| 912797WN3 | 2027-01-05 |                 61 | 99.3367 |           0.0391 |                  0.04   |
| 912797WQ6 | 2027-01-19 |                 75 | 99.1819 |           0.0393 |                  0.0401 |
| 912797WS2 | 2027-02-02 |                 89 | 99.0271 |           0.0394 |                  0.0403 |
| 912797WZ6 | 2027-02-16 |                103 | 98.8582 |           0.0399 |                  0.0409 |
| 912797XB8 | 2027-03-02 |                117 | 98.6982 |           0.0401 |                  0.0411 |
| 912797WL7 | 2027-03-25 |                140 | 98.4401 |           0.0401 |                  0.0413 |
| 912797WV5 | 2027-04-22 |                168 | 98.1073 |           0.0406 |                  0.0419 |
| 912797VF1 | 2027-06-10 |                217 | 97.57   |           0.0403 |                  0.0418 |
| 912797WJ2 | 2027-09-30 |                329 | 96.2827 |           0.0407 |                  0.0424 |

---

## get_ice_bofa_option_adjusted_spread
The ICE BofA Option-Adjusted Spreads (OASs) are the calculated spreads between a computed OAS index of all bonds in a given maturity and rating category and a spot Treasury curve. An OAS index is constructed using each constituent bond's OAS, weighted by market capitalization.

The Option-Adjusted Spread (OAS) is the spread relative to a risk-free interest rate, usually quoted in basis points, that equates the theoretical present value of a series of uncertain cash flows to the market price of a fixed-income investment. The spread is added to the risk-free rate to compensate for the uncertainty of the cash flows. ICE adds it to the semi-annually compounded forward rates of the Treasury curve (ICE Bond Index Methodologies), so it is a semi-annually compounded spread.

See definitions:

- Ratings: [https://fred.stlouisfed.org/series/BAMLC0A4CBBB](https://fred.stlouisfed.org/series/BAMLC0A4CBBB){:target="_blank"}
- Maturity: [https://fred.stlouisfed.org/series/BAMLC1A0C13Y](https://fred.stlouisfed.org/series/BAMLC1A0C13Y){:target="_blank"}

**Args:**

- <u>maturity (bool, optional):</u> Whether to return the maturity option adjusted spread or the rating option adjusted spread.
Defaults to True (by maturity).
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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

The effective yield of an ICE BofA index is the yield of the index as a whole, aggregated from the yields of its constituent bonds and weighted by their market capitalisation. It is an index-level yield of the corporate bond market segment, not a statistic derived from any single bond's coupon; for the yield of a single bond, see the "Yield to Maturity" of `collect_bond_statistics` instead. ICE states each bond's yield in conventional terms, compounded at the bond's coupon frequency (ICE Bond Index Methodologies): twice a year for the US indices, so their effective yields compound semi-annually like Treasury yields.

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
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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

Yield to worst is the lowest potential yield that a bond can generate without the issuer defaulting. The standard US convention for this series is to use semi-annual coupon payments, whereas the standard in the foreign markets is to use coupon payments with frequencies of annual, semi-annual, quarterly, and monthly. These series state every index in semi-annual terms, so the yields are compounded twice a year whatever the coupon frequency.

See definitions:

- Ratings: [https://fred.stlouisfed.org/series/BAMLC0A4CBBBSYTW](https://fred.stlouisfed.org/series/BAMLC0A4CBBBSYTW){:target="_blank"}
- Maturity: [https://fred.stlouisfed.org/series/BAMLC1A0C13YSYTW](https://fred.stlouisfed.org/series/BAMLC1A0C13YSYTW){:target="_blank"}

**Args:**

- <u>maturity (bool, optional):</u> Whether to return the maturity yield to worst or the rating yield to worst.
Defaults to True (by maturity).
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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

Without a FRED API key the curve comes from the Treasury's own HQM files, which gives the same figures. When a FRED API key is set (see the `fred_api_key` parameter of the `FixedIncome` class), it comes from FRED, which republishes the Treasury's curve. The rates are returned as decimal fractions (0.0558 for 5.58%), semi-annual bond-equivalent as the Treasury publishes them.

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
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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
Computes the credit spread of high quality US corporate bonds per maturity: the Treasury's High Quality Market (HQM) corporate par yield minus the Treasury constant maturity yield, at 2, 5, 10 and 30 years, monthly. Both legs are par yields averaged over the month, so they are directly comparable. The spread is what investors demand for the default and liquidity risk of investment grade companies, and its shape across maturities, usually wider for longer maturities, shows how that compensation grows with time.

Unlike the ICE BofA option-adjusted spreads (see `get_ice_bofa_option_adjusted_spread`), of which FRED only carries the last three years, this spread covers decades, long enough to calibrate how credit spreads behave through several business cycles.

The formula is as follows:

$$
\text{HQM Spread} \;(\text{maturity}) = \text{HQM Corporate Par Yield} \;(\text{maturity}) - \text{Treasury Constant Maturity Yield} \;(\text{maturity}),\;\; \text{both monthly averages, for 2, 5, 10 and 30 years}
$$

Without a FRED API key both legs come from the Treasury, the HQM par yields from its HQM files and the Treasury yields as the monthly averages of its daily par yield curve, rounded to two decimals in percent as the Federal Reserve's H.15 release publishes them. That curve starts in 1990 and has no 30-year yield from February 2002 to February 2006, so the spread without a FRED API key starts in 1990 and leaves those 30-year months empty. When a FRED API key is set (see the `fred_api_key` parameter of the `FixedIncome` class), the Treasury yields are FRED's constant maturity series, from 1984. The spreads are returned as decimal fractions (0.0079 for 0.79 percentage points).

**Also known as:** corporate credit spread curve, credit spread term structure, investment grade spread.

**Args:**

- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to return the growth data or the actual data. Defaults to False.
- <u>lag (int, optional):</u> The number of periods to lag the growth data by. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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

- Germany: the average yield on debt securities outstanding of non-MFI corporations the Bundesbank publishes monthly from 1957 (monthly averages), all ratings together ("All ratings").
- Australia: the yields of non-financial corporate bonds rated A and BBB with a target tenor of 3, 5, 7 and 10 years the Reserve Bank of Australia publishes from 2005 (end of month), e.g. "BBB 10Y".
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
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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

The data comes from CEREP, the central repository where every credit rating agency registered in the European Union reports its ratings to ESMA, published twice a year with periods from 1989. It covers the global ratings of agencies such as S&P, Moody's, Fitch, DBRS and Scope, for corporates (non-financial, financial and insurance), sovereigns, structured finance and covered bonds, in each agency's own rating scale.

By default the matrix is withdrawal-adjusted, the convention of the agencies' own default studies: ratings withdrawn during the period are left out, so each row sums to 1. The matrix compares the rating at the start of the period with the rating at its end, so a default that was followed by a new rating within the period (as after a distressed exchange) shows as that new rating; get_default_rates counts every default within the period and is the measure to calibrate default rates on. With include_withdrawals=True they are a separate "Withdrawals" column, and with probabilities=False the counts are returned instead.

The formula is as follows (probabilities=True, the default):

$$
\text{Transition Probability} \;(\text{from},\; \text{to}) = \frac{\text{Count} \;(\text{from},\; \text{to})}{\sum(\text{Count} \;(\text{from},\; \text{every end category}))},\;\; \text{with the end categories the ratings and default, plus "Withdrawals" only when include\_withdrawals=True}
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
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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

The data comes from CEREP, the central repository where every credit rating agency registered in the European Union reports its ratings to ESMA, in each agency's own rating scale (AAA to C for S&P and Fitch, Aaa to C for Moody's). Only the years between the start and end date are retrieved, one request per year. CEREP answers slowly (up to half a minute per year), so a long history takes a few minutes the first time; each year is cached afterwards. The years before an agency reported to CEREP read as zero defaults and are left out, so the history starts at the first year with a default.

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
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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
Calculates the default probabilities that credit spreads imply. Investors in a corporate bond are compensated for the loss they expect from a default, so with a constant default intensity (hazard rate) $$\lambda$$ and a share R recovered on default the spread s is about $$\lambda (1 - R)$$, the "credit triangle":

$$\lambda = s / (1 - R)$$, P(default within t years) = $$1 - e^{- \lambda t}$$

The spreads are the latest ICE BofA option-adjusted spreads of the US corporate bond indices per rating (AAA to CCC) up to the end date, which need a FRED API key. For a spread of your own, use `short_rate_model.get_implied_default_probability`. Spreads also pay for liquidity and for the uncertainty of the losses, so these risk-neutral probabilities are higher than the default rates that are observed historically (see `get_default_rates`); the gap is the credit risk premium.

For more information, see the following book:

- Hull, J.C. (2022). "Options, Futures, and Other Derivatives." Pearson, 11th edition, chapter 24.

**Also known as:** implied default probability, hazard rate, credit triangle, risk-neutral default probability.

**Args:**

- <u>ratings (list[str] &#124; str &#124; None, optional):</u> The ratings: "AAA", "AA", "A", "BBB",
"BB", "B" or "CCC", as a list or a comma-separated string. Defaults to None,
every rating.
- <u>recovery_rate (float, optional):</u> The share of the face value recovered on
default, the scenario the probabilities assume. Defaults to 0.4, about the
average recovery of senior unsecured bonds.
- <u>horizons (list[float] &#124; str &#124; None, optional):</u> The horizons in years, as a list or
a comma-separated string. Defaults to None, which uses 1, 3, 5 and 10 years.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The Spread, the Hazard Rate and the default probability per horizon
as decimals, with a row per rating.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome(end_date="2026-11-05", fred_api_key="your_fred_api_key")

fixedincome.get_implied_default_probability()
```

Which returns:

| Rating   |   Spread |   Hazard Rate |   1Y Default Probability |   3Y Default Probability |   5Y Default Probability |   10Y Default Probability |
|:---------|---------:|--------------:|-------------------------:|-------------------------:|-------------------------:|--------------------------:|
| AAA      |   0.0048 |        0.008  |                   0.008  |                   0.0237 |                   0.0392 |                    0.0769 |
| AA       |   0.0069 |        0.0115 |                   0.0114 |                   0.0339 |                   0.0559 |                    0.1086 |
| A        |   0.0077 |        0.0128 |                   0.0128 |                   0.0378 |                   0.0622 |                    0.1204 |
| BBB      |   0.0116 |        0.0193 |                   0.0191 |                   0.0564 |                   0.0921 |                    0.1758 |
| BB       |   0.0213 |        0.0355 |                   0.0349 |                   0.101  |                   0.1626 |                    0.2988 |
| B        |   0.0367 |        0.0612 |                   0.0593 |                   0.1676 |                   0.2635 |                    0.4576 |
| CCC      |   0.132  |        0.22   |                   0.1975 |                   0.4831 |                   0.6671 |                    0.8892 |

---

## get_survival_curve
Bootstraps survival curves, the probability that a US corporate issuer has not defaulted after each horizon, from the ICE BofA option-adjusted spreads. The default time follows a hazard rate that is piecewise flat: constant between the maturities of the spreads it is bootstrapped from and held at its last value beyond them (Jarrow and Turnbull, 1995; O'Kane, 2008, ch. 7).

Each spread is read as a bond that trades at par: its coupon is the par yield of the Treasury zero-coupon curve plus the spread. The hazard rate up to its maturity is solved, in maturity order with the earlier ones fixed, so that the bond priced on the Treasury curve with that default risk is worth par again, every coupon and the principal paid only on survival and the recovery rate times the face value paid at default:

The formula is as follows:

$$
D_{s}(t) = P(t) \cdot \left(1 + \frac{s_{i}}{2}\right)^{- 2t},\;\; c_{i} = \frac{2 \cdot (1 - D_{s}(T_{i}))}{\sum(D_{s}(t_{k}))}
$$

$$
\text{Solve } \lambda_{i} \text{:}\;\; \frac{c_{i}}{2} \cdot \sum(P(t_{k}) Q(t_{k})) + P(T_{i}) Q(T_{i}) + R \text{∫}_{0}^{T_{i}} P(t) (- \operatorname{dQ}(t)) = 1
$$

$$
Q(t) = \exp(- \sum(\lambda_{j} \cdot (\min(t,\; T_{j}) - T_{j-1})^{} +))
$$

where $$s_{i}$$ is the option-adjusted spread of maturity $$T_{i}$$, compounded twice a year as ICE adds it to the semi-annual Treasury rates (an option-adjusted spread is a Z-spread once the call options are taken out), P(t) = (1 + r(t))^(-t) the discount factor of the annually compounded US Treasury zero-coupon curve (see `get_zero_coupon_curve`), $$t_{k}$$ the semi-annual coupon dates and R the recovery rate. The default integral is exact on the grid of the curve, hazard rate and coupon dates (ISDA CDS Standard Model). The credit triangle $$\lambda \approx s / (1 - R)$$ of `get_implied_default_probability` is its first-order version.

By maturity, the curve is bootstrapped from the six maturity buckets of the ICE BofA US Corporate Index (investment grade), each taken at its middle: 2, 4, 6, 8.5 and 12.5 years, and 20 years for 15+ years. By rating, each rating index (AAA to CCC and lower) has a single spread and so a flat hazard rate, bootstrapped from a par bond of 7 years; the hazard rate moves by less than 0.2% between 5 and 10 years.

The spreads are the latest up to the end date, and the Treasury curve that of the same day (or the last day before it). Spreads also pay for liquidity and the uncertainty of losses, so these risk-neutral survival probabilities are below those of the default rates observed (see `get_default_rates`).

For more information, see the following sources:

- Jarrow, R.A. and Turnbull, S.M. (1995). "Pricing Derivatives on Financial Securities Subject to Credit Risk." The Journal of Finance, 50(1), 53-85.
- O'Kane, D. (2008). "Modelling Single-name and Multi-name Credit Derivatives." Wiley, ch. 3 and 7.
- Markit (2009). "ISDA CDS Standard Model."

Referenced against QuantLib's PiecewiseFlatHazardRate and RiskyBondEngine.

**Also known as:** credit curve, hazard rate curve, default probability term structure, bond-implied default probabilities.

**Args:**

- <u>maturity (bool, optional):</u> Whether to bootstrap one curve from the maturity buckets
of the US Corporate Index, or a flat curve per rating. Defaults to True (by
maturity).
- <u>ratings (list[str] &#124; str &#124; None, optional):</u> The ratings: "AAA", "AA", "A", "BBB",
"BB", "B" or "CCC", as a list or a comma-separated string; giving them returns
the curves by rating. Defaults to None, every rating when maturity is False.
- <u>recovery_rate (float, optional):</u> The share of the face value recovered on
default. Defaults to 0.4, about the average recovery of senior unsecured bonds
and the ISDA standard.
- <u>horizons (list[float] &#124; str &#124; None, optional):</u> The horizons in years or as labels
such as "6M", as a list or a comma-separated string. Defaults to None, which
uses 1, 2, 3, 5, 7, 10, 15, 20 and 30 years.
- <u>hazard_rates (bool, optional):</u> Whether to return the hazard rate in force at each
horizon (continuous, per year) instead of the survival probability. Defaults
to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the FixedIncome rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The survival probabilities (or hazard rates) as decimals, with a row
per horizon and a column per curve: Corporate by maturity, or the ratings.

**Notes:**

ICE licenses only the most recent three years of every ICE BofA series to FRED,
so the end date must lie within them. The hazard rate between two maturities is a
forward rate of default: where the spreads flatten between two buckets, it falls
below the hazard rate of the bucket before.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome(end_date="2026-11-05", fred_api_key="your_fred_api_key")

fixedincome.get_survival_curve(maturity=False)
```

Which returns:

| Maturity   |    AAA |     AA |      A |    BBB |     BB |      B |    CCC |
|:-----------|-------:|-------:|-------:|-------:|-------:|-------:|-------:|
| 1Y         | 0.9921 | 0.9887 | 0.9873 | 0.981  | 0.9656 | 0.9418 | 0.8124 |
| 2Y         | 0.9842 | 0.9774 | 0.9749 | 0.9624 | 0.9323 | 0.887  | 0.66   |
| 3Y         | 0.9764 | 0.9663 | 0.9625 | 0.9442 | 0.9003 | 0.8353 | 0.5361 |
| 5Y         | 0.961  | 0.9445 | 0.9383 | 0.9087 | 0.8394 | 0.7409 | 0.3538 |
| 7Y         | 0.9459 | 0.9232 | 0.9147 | 0.8745 | 0.7826 | 0.6572 | 0.2335 |
| 10Y        | 0.9236 | 0.8921 | 0.8805 | 0.8257 | 0.7045 | 0.549  | 0.1252 |
| 15Y        | 0.8876 | 0.8427 | 0.8261 | 0.7503 | 0.5913 | 0.4067 | 0.0443 |
| 20Y        | 0.8531 | 0.7959 | 0.7752 | 0.6818 | 0.4963 | 0.3014 | 0.0157 |
| 30Y        | 0.7879 | 0.7101 | 0.6825 | 0.563  | 0.3497 | 0.1654 | 0.002  |

---

## get_credit_default_swap_spread
Calculates the CDS-equivalent spreads of US corporate credit: the par spreads of credit default swaps on the survival curves the ICE BofA option-adjusted spreads imply (see `get_survival_curve`). It turns the spreads of corporate bonds into the spread a protection buyer would pay each year to insure against a default of an issuer with that credit, by maturity or by rating.

The swaps follow the ISDA CDS Standard Model: the premium is paid quarterly on an ACT/360 basis, the premium accrued since the last payment is paid on default, and the protection pays (1 - R) of the notional at the time of default. The par spread is the premium at which both legs are worth the same:

The formula is as follows:

$$
\text{RPV01} = \sum(\tau_{k} P(t_{k}) Q(t_{k})) + \frac{365}{360} \cdot \sum(\text{∫\_t\_\{k-1\}}^{t}_{k} (t - t_{k-1}) P(t) (- \operatorname{dQ}(t)))
$$

$$
\text{Protection Leg} = (1 - R) \cdot \text{∫}_{0}^{T} P(t) (- \operatorname{dQ}(t))
$$

$$
\text{CDS Spread} = \frac{\text{Protection Leg}}{\text{RPV01}}
$$

where $$\tau_{k}$$ is the ACT/360 accrual of the k-th quarter, P(t) = (1 + r(t))^(-t) the discount factor of the annually compounded US Treasury zero-coupon curve, Q(t) the survival probability of the piecewise flat hazard rate curve and R the recovery rate. The integrals are exact on the grid of the curve, hazard rate and premium dates, as in the standard model. The spreads are discounted on the Treasury curve, the curve the option-adjusted spreads are measured over, rather than the swap curve dealers use, and the protection starts today without the standard model's step-in day.

The gap between a CDS-equivalent spread and the bond spread at the same maturity is a model basis: a bond loses its price less the recovery at default while a CDS pays the face value less the recovery, and the CDS premium stops at default. Traded CDS spreads also differ by the liquidity of each market, the cheapest-to-deliver option and the funding of the bonds.

For more information, see the following sources:

- O'Kane, D. (2008). "Modelling Single-name and Multi-name Credit Derivatives." Wiley, ch. 5 to 7.
- Markit (2009). "ISDA CDS Standard Model."
- Hull, J.C. and White, A. (2000). "Valuing Credit Default Swaps I: No Counterparty Default Risk." The Journal of Derivatives, 8(1), 29-40.

Referenced against QuantLib's CreditDefaultSwap with the IsdaCdsEngine and FinancePy's CDS. For a single name with spreads or hazard rates of your own, use `cds_model.get_credit_default_swap` and `cds_model.get_cds_implied_hazard_rates`.

**Also known as:** CDS spread, CDS-equivalent spread, credit default swap premium, bond-implied CDS spread.

**Args:**

- <u>maturity (bool, optional):</u> Whether to use the survival curve of the maturity
buckets of the US Corporate Index, or one per rating. Defaults to True (by
maturity).
- <u>ratings (list[str] &#124; str &#124; None, optional):</u> The ratings: "AAA", "AA", "A", "BBB",
"BB", "B" or "CCC", as a list or a comma-separated string; giving them returns
the spreads by rating. Defaults to None, every rating when maturity is False.
- <u>recovery_rate (float, optional):</u> The share of the face value recovered on
default, for the bonds and the swaps alike. Defaults to 0.4, the ISDA standard
for senior unsecured debt.
- <u>tenors (list[float] &#124; str &#124; None, optional):</u> The tenors of the swaps in years or as
labels such as "6M", as a list or a comma-separated string. Defaults to None,
which uses 1, 3, 5, 7 and 10 years.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the FixedIncome rounding.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The par CDS spreads as decimals (0.01 for 100 basis points), with a
row per tenor and a column per curve: Corporate by maturity, or the ratings.

**Notes:**

ICE licenses only the most recent three years of every ICE BofA series to FRED,
so the end date must lie within them.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome(end_date="2026-11-05", fred_api_key="your_fred_api_key")

fixedincome.get_credit_default_swap_spread()
```

Which returns:

| Maturity   |   Corporate |
|:-----------|------------:|
| 1Y         |      0.0061 |
| 3Y         |      0.0075 |
| 5Y         |      0.0091 |
| 7Y         |      0.0104 |
| 10Y        |      0.011  |

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

- <u>period (str, optional):</u> Whether to return the daily, weekly, monthly, quarterly or
yearly data. Weekly takes the last day of every week; quarterly and yearly
average the monthly averages of the complete quarters and years. Defaults to
"daily".
- <u>spread (bool, optional):</u> Whether to return the spreads over the 10-year Treasury
yield instead of the yields. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to return the growth data or the actual data. Defaults to False.
- <u>lag (int, optional):</u> The number of periods to lag the growth data by. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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

The spread and premium are returned as decimal fractions (0.0084 for 0.84 percentage points) and the probability as a fraction (0.108 for 10.8%).

**See definition:** [https://www.federalreserve.gov/econres/notes/feds-notes/updating-the-recession-risk-and-the-excess-bond-premium-20161006.html](https://www.federalreserve.gov/econres/notes/feds-notes/updating-the-recession-risk-and-the-excess-bond-premium-20161006.html){:target="_blank"}

**Also known as:** GZ spread, Gilchrist-Zakrajšek spread, EBP, credit market sentiment.

**Args:**

- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to return the growth data or the actual data. Defaults to False.
- <u>lag (int, optional):</u> The number of periods to lag the growth data by. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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

## get_corporate_borrowing_cost
Retrieves the composite cost of borrowing for non-financial corporations the European Central Bank publishes monthly from 2003, for the euro area and every member: the average interest rate on new bank loans to companies across maturities and loan sizes. Euro area companies borrow mostly from banks rather than in the bond market, which makes this the broadest measure of their cost of credit, and the closest freely available proxy for euro area corporate credit conditions, since euro area corporate bond indices are licensed data.

The rate is a decimal fraction (0.0377 for 3.77%).

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
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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

Weekly and monthly periods take the index on the last day of each period.

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
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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

## get_forward_rate
Calculates the implied forward rates between pairs of maturities of a country's zero-coupon (spot) yield curve on a day. The forward rate is the interest rate, implied by that day's curve, for a loan that starts at a future date: it follows from no-arbitrage pricing rather than being a forecast of future rates, and contains a term premium.

The formula is as follows:

$$
\text{Forward Rate} = \left(\frac{(1 + r_{2})^{t_{2}}}{(1 + r_{1})^{t_{1}}}\right)^{\frac{1}{t_{2} - t_{1}}} - 1
$$

where:

$$
r_{1} = \text{Zero-coupon rate at the near maturity},\;\; \text{read from the curve with the interpolation}
$$

$$
t_{1} = \text{Near maturity},\;\; \text{in years}
$$

$$
r_{2} = \text{Zero-coupon rate at the far maturity},\;\; \text{read from the curve with the interpolation}
$$

$$
t_{2} = \text{Far maturity},\;\; \text{in years}
$$

The curve is the zero-coupon curve of `get_zero_coupon_curve`, bootstrapped from the country's government bond par yields and annually compounded, so the forward rate is annually compounded as well. By default (interpolation="linear_par") it holds the zero rate of every coupon date the bootstrap solves for, not only those of the quoted maturities, and is linear between them; another interpolation bootstraps the curve with that interpolation, see `get_zero_coupon_curve`. For a curve of your own, use `yieldcurve_model.get_forward_rate`.

**Also known as:** implied forward rate, forward-forward rate.

**Args:**

- <u>near_maturity (float &#124; str &#124; list &#124; None, optional):</u> The nearer maturity (or
maturities), in years or as labels such as '6M'. Defaults to None, 1 to 5 years.
- <u>far_maturity (float &#124; str &#124; list &#124; None, optional):</u> The further maturity (or
maturities), in years or as labels such as '10Y'. Defaults to None, 5 to 10 years.
- <u>country (str, optional):</u> The country, see `get_zero_coupon_curve`. Defaults to
"United States".
- <u>date (str &#124; None, optional):</u> The day of the curve (YYYY-MM-DD), or the last day
before it with a curve. Defaults to None, the end date.
- <u>interpolation (str, optional):</u> How the zero-coupon curve is read between its
maturities: "linear_par", "linear_zero", "log_linear", "natural_cubic",
"monotone_cubic" or "monotone_convex", see `get_zero_coupon_curve`.
Defaults to "linear_par".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results
to. Defaults to None, which uses the rounding of the class.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The forward rate (decimal, annually compounded) for each combination
of near (rows) and far maturity (columns). Combinations where the far maturity is
not greater than the near maturity are NaN.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome()

fixedincome.get_forward_rate(
    near_maturity=[1, 2, 5], far_maturity=[5, 10, 30], date="2026-11-05"
)
```

Which returns:

|   Near Maturity |        5 |     10 |     30 |
|----------------:|---------:|-------:|-------:|
|               1 |   0.0473 | 0.0501 | 0.0548 |
|               2 |   0.0474 | 0.0505 | 0.0551 |
|               5 | nan      | 0.0524 | 0.056  |

---

## get_par_yield
Calculates the par yields of any maturity from a country's zero-coupon (spot) yield curve on a day. The par yield for a maturity is the coupon rate a newly issued bond of that maturity needs so that, discounted with the spot curve, its price equals par.

The government bond yield curve quotes par yields at its own maturities; this gives the par yield of any maturity in between (such as 4 or 15 years) from the zero-coupon rates of every coupon date the bootstrap of `get_zero_coupon_curve` solves for, so a maturity on a coupon date reprices the par yield the bootstrap assumed there and a maturity between coupon dates is interpolated on the zero-coupon rates.

The formula is as follows:

$$
\operatorname{DF}(t) = \frac{1}{\left(1 + \frac{\text{Spot Rate}\left(\frac{t}{\text{Frequency}}\right)}{\text{Frequency}}\right)^{t}},\;\; \text{the discount factor of a cash flow after } t \text{ coupon periods}
$$

$$
\text{Par Yield} = \frac{\text{Frequency} \cdot (1 - \operatorname{DF}(t_{n}))}{\sum(\operatorname{DF}(t_{i})) - a},\;\; \text{over}\;\; \text{the remaining coupons}\; i = 1,\; \ldots,\; n
$$

where Spot Rate(τ) is the zero-coupon rate of `get_zero_coupon_curve` at $$\tau$$ years, restated from annual compounding to the country's coupon frequency (twice a year, once for Sweden and Norway) and interpolated linearly between the bills and the coupon dates of the bootstrap (or read with another interpolation, see below), a is the elapsed fraction of the current coupon period (0 on a coupon date) and $$t_{i} = i - a$$ is the time of the i-th coupon in periods. With an interpolation other than "linear_par" the zero-coupon curve is bootstrapped with that interpolation (see `get_zero_coupon_curve`), so every quoted par yield reprices exactly and the maturities in between follow the interpolation. The par yield is a nominal annual coupon rate paid at the coupon frequency, like the government bond yield curve. For a curve of your own, use `yieldcurve_model.get_par_yield`.

**Also known as:** par rate, par coupon rate.

**Args:**

- <u>years_to_maturity (float &#124; str &#124; list &#124; None, optional):</u> The maturities, in years
or as labels such as '15Y'. Defaults to None, 1 to 30 years.
- <u>country (str, optional):</u> The country, see `get_zero_coupon_curve`. Defaults to
"United States".
- <u>date (str &#124; None, optional):</u> The day of the curve (YYYY-MM-DD), or the last day
before it with a curve. Defaults to None, the end date.
- <u>interpolation (str, optional):</u> How the zero-coupon curve is read between its
maturities: "linear_par", "linear_zero", "log_linear", "natural_cubic",
"monotone_cubic" or "monotone_convex", see `get_zero_coupon_curve`.
Defaults to "linear_par".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results
to. Defaults to None, which uses the rounding of the class.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series: The par yield (decimal) by maturity in years.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome()

fixedincome.get_par_yield(years_to_maturity=[1, 4, 8, 15, 25], date="2026-11-05")
```

Which returns:

|   Years to Maturity |   Par Yield |
|--------------------:|------------:|
|                   1 |      0.0428 |
|                   4 |      0.0456 |
|                   8 |      0.0475 |
|                  15 |      0.0505 |
|                  25 |      0.0526 |

---

## get_instantaneous_forward_curve
Calculates the instantaneous forward curve of a country's zero-coupon curve on a day: at every maturity t, the rate the curve implies for borrowing over an infinitesimal period starting at t. Where a zero rate averages the forward rates up to its maturity, the instantaneous forward shows each part of the curve on its own, which makes it the sharpest view of the curve's shape and the curve the Heath-Jarrow-Morton and Hull-White models start from.

The formula is as follows:

$$
f(t) = - \frac{d \ln P(t)}{\,\mathrm{d}t} = r(t) + t \cdot \frac{\operatorname{dr}(t)}{\,\mathrm{d}t}
$$

$$
r(t) = \frac{1}{t} \cdot \text{∫} \;f(s) \,\mathrm{d}s,\;\; \text{from 0 to } t
$$

where P(t) is the discount factor and r(t) the continuously compounded zero rate of maturity t, read from the zero-coupon curve of `get_zero_coupon_curve` (bootstrapped from the par yields) with the interpolation. As the forward rate is the slope of r(t) t, it shows every kink of the interpolation: it jumps at every maturity of "linear_zero" and "linear_par" and is flat between those of "log_linear". The default, Hagan and West's (2006) monotone convex method, gives a continuous forward curve that keeps the discrete forwards between the maturities and does not oscillate, which is why it is the default here (the other curve methods default to "linear_par", the curve of `get_zero_coupon_curve`). At a maturity of the curve itself the forward is that of the interval that starts there; beyond the last maturity the zero rate, and so the forward, is held at the last zero rate.

The instantaneous forward rate is continuously compounded, as it is defined.

For more information, see the following papers:

- Hagan, P.S. and West, G. (2006). "Interpolation Methods for Curve Construction." Applied Mathematical Finance, 13(2), 89-129.
- Hagan, P.S. and West, G. (2008). "Methods for Constructing a Yield Curve." Wilmott Magazine, May, 70-81.

Referenced against QuantLib's forward rates of its piecewise curves ([https://www.quantlib.org](https://www.quantlib.org){:target="_blank"}), see `get_zero_coupon_curve`.

**Also known as:** instantaneous forward rate, forward curve, short forward curve.

**Args:**

- <u>maturities (float &#124; str &#124; list &#124; None, optional):</u> The maturities, in years or as
labels such as '6M' (a list or a comma-separated string). Defaults to None,
3 and 6 months and 1 to 30 years.
- <u>country (str, optional):</u> The country, see `get_zero_coupon_curve`. Defaults to
"United States".
- <u>date (str &#124; None, optional):</u> The day of the curve (YYYY-MM-DD), or the last day
before it with a curve. Defaults to None, the end date.
- <u>interpolation (str, optional):</u> "monotone_convex", "linear_zero", "log_linear",
"natural_cubic", "monotone_cubic" or "linear_par", see
`get_zero_coupon_curve`. Defaults to "monotone_convex".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results
to. Defaults to None, which uses the rounding of the class.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The Instantaneous Forward Rate (continuously compounded) and the Zero
Rate (annually compounded, as `get_zero_coupon_curve`) by maturity in years.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome()

fixedincome.get_instantaneous_forward_curve(maturities=[0.5, 1, 2, 5, 10, 20, 30], date="2026-11-05")
```

Which returns:

|   Maturity |   Instantaneous Forward Rate |   Zero Rate |
|-----------:|-----------------------------:|------------:|
|        0.5 |                       0.0421 |      0.0423 |
|        1   |                       0.0441 |      0.0433 |
|        2   |                       0.0461 |      0.0451 |
|        5   |                       0.048  |      0.0465 |
|       10   |                       0.0536 |      0.0494 |
|       20   |                       0.0549 |      0.0552 |
|       30   |                       0.0485 |      0.0541 |

---

## get_smith_wilson_curve
Extends a country's government bond yield curve to any maturity with the Smith-Wilson method (Smith and Wilson, 2001), as EIOPA builds the Solvency II risk-free rate term structures: the curve prices every bill and par bond of the curve exactly and, beyond its last liquid point, converges to an ultimate forward rate (UFR). Insurers and pension funds discount liabilities of 50 to 100 years with such a curve, longer than any bond that trades.

The formula is as follows:

$$
P(t) = e^{- \omega t} + \Sigma_{j} \zeta_{j} W(t,\; u_{j})
$$

$$
W(t,\; u) = e^{- \omega (t + u)}\left[\alpha \min(t,\; u) - \text{½} e^{- \alpha \max(t,\; u)}(e^{\alpha \min(t,\; u)} - e^{- \alpha \min(t,\; u)})\right]
$$

$$
\zeta = C^{T}(C W C^{T})^{- 1}(m - C \mu),\;\; \text{with}\;\; \mu_{j} = e^{- \omega u_{j}}
$$

$$
\omega = \ln(1 + \text{UFR})
$$

where $$u_{j}$$ are the cash flow times of the instruments, C their cash flows and m their prices. The instruments are the curve's quotes of the day up to the last liquid point: the bills (a year or less) as zero-coupon bonds whose price follows from their yield in the country's quote convention, and the longer maturities as par bonds paying their par yield in coupons twice a year (once for Sweden and Norway) at a price of par. The Euro Area and German curves are zero-coupon curves, so every maturity is a zero-coupon bond.

Alpha sets how fast the forward rate converges to the UFR. By default it is set as EIOPA does: the smallest alpha of at least 0.05 for which the instantaneous forward rate at the convergence point lies within a basis point of $$\omega$$, with the convergence point at the later of 60 years and the last liquid point plus 40 years (see `smith_wilson_model.get_smith_wilson_alpha`).

The zero rates are annually compounded, as EIOPA publishes them and as `get_zero_coupon_curve` returns them, and the instantaneous forward rate is continuously compounded, so it converges to ln(1 + UFR).

For more information, see the following sources:

- Smith, A. and Wilson, T. (2001). "Fitting Yield Curves with Long Term Constraints." Research Notes, Bacon and Woodrow.
- EIOPA (2022). "Technical Documentation of the Methodology to Derive EIOPA's Risk-Free Interest Rate Term Structures." EIOPA-BoS-22/409.

Referenced against rateslib's SmithWilsonCurve ([https://rateslib.com](https://rateslib.com){:target="_blank"}) and EIOPA's October 2026 euro curve, whose Smith-Wilson coefficients, alpha (0.068369) and rates it reproduces from the same par swaps.

**Also known as:** Smith-Wilson extrapolation, UFR curve, Solvency II curve extrapolation, ultimate forward rate.

**Args:**

- <u>maturities (float &#124; str &#124; list &#124; None, optional):</u> The maturities, in years or as
labels such as '50Y' (a list or a comma-separated string). Defaults to None,
1, 2, 3, 5, 7, 10, 20, 30, 40, 50, 60, 80, 100 and 150 years.
- <u>country (str, optional):</u> The country, see `get_zero_coupon_curve`. Defaults to
"United States".
- <u>date (str &#124; None, optional):</u> The day of the curve (YYYY-MM-DD), or the last day
before it with a curve. Defaults to None, the end date.
- <u>ultimate_forward_rate (float, optional):</u> The UFR, annually compounded (decimal);
EIOPA publishes it every year per currency. Defaults to 0.033.
- <u>alpha (float &#124; None, optional):</u> The speed of convergence, above 0. Defaults to
None, EIOPA's convergence criterion.
- <u>last_liquid_point (float &#124; None, optional):</u> The longest maturity, in years, whose
quote the curve keeps. Defaults to None, the longest maturity of the curve.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results
to. Defaults to None, which uses the rounding of the class.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The Zero Rate (annually compounded), the Discount Factor and the
Instantaneous Forward Rate (continuously compounded) by maturity in years, and the
Alpha of the curve.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome()

fixedincome.get_smith_wilson_curve(date="2026-11-05")
```

Which returns:

|   Maturity |   Zero Rate |   Discount Factor |   Instantaneous Forward Rate |   Alpha |
|-----------:|------------:|------------------:|-----------------------------:|--------:|
|          1 |      0.0433 |            0.9585 |                       0.0444 |  0.1202 |
|          2 |      0.0451 |            0.9155 |                       0.0466 |  0.1202 |
|          3 |      0.0459 |            0.8741 |                       0.0459 |  0.1202 |
|          5 |      0.0465 |            0.7966 |                       0.0479 |  0.1202 |
|          7 |      0.0478 |            0.7213 |                       0.0506 |  0.1202 |
|         10 |      0.0494 |            0.6172 |                       0.0543 |  0.1202 |
|         20 |      0.0553 |            0.3407 |                       0.0579 |  0.1202 |
|         30 |      0.0541 |            0.2061 |                       0.0436 |  0.1202 |
|         40 |      0.0505 |            0.1393 |                       0.036  |  0.1202 |
|         50 |      0.0474 |            0.0986 |                       0.0336 |  0.1202 |
|         60 |      0.0451 |            0.0708 |                       0.0328 |  0.1202 |
|         80 |      0.0421 |            0.0369 |                       0.0325 |  0.1202 |
|        100 |      0.0403 |            0.0193 |                       0.0325 |  0.1202 |
|        150 |      0.0379 |            0.0038 |                       0.0325 |  0.1202 |

---

## get_yield_curve_spread
Calculates the spreads between pairs of maturities of a country's government bond yield curve on a day, e.g. the widely followed 10-year minus 2-year and 10-year minus 3-month Treasury spreads. A positive spread indicates a "normal" upward-sloping curve, while a negative spread ("inversion") has historically been used as a leading indicator of an economic slowdown.

The formula is as follows:

$$
\text{Yield Curve Spread} = \text{Long-Term Yield} - \text{Short-Term Yield}
$$

Where both yields are the par yields of `get_government_bond_yield_curve`, as the Treasury and FRED (T10Y2Y, T10Y3M) calculate the spreads, interpolated linearly for a maturity the curve does not quote. They keep the source's quote convention: for the United States bond-equivalent yields, compounded twice a year beyond a year and simple interest for the bill maturities up to half a year, so a spread against a bill yield mixes the two conventions, as the published spreads do. For the history of these spreads, take the difference of two columns of `get_government_bond_yield_curve`; for yields of your own, use `yieldcurve_model.get_yield_curve_spread`.

With `middle_maturity` it calculates butterflies instead, a measure of the curvature of the curve: twice how far the yield of a middle maturity (the body) lies above the average yield of a short and a long maturity (the wings), with the wings weighted equally as butterflies are quoted (2s5s10s). That average is the straight line through the wings only when the body lies midway between them, which 5 years does not in 2s5s10s:

$$
\text{Butterfly} = 2 \cdot \text{Middle Yield} - \text{Short Yield} - \text{Long Yield}
$$

A positive butterfly means the body yields more than the wings on average.

**Also known as:** term spread, yield curve slope, 10Y-2Y spread, fly, 2s5s10s.

**Args:**

- <u>long_maturity (float &#124; str &#124; list &#124; None, optional):</u> The longer maturity (or
maturities), in years or as labels such as '10Y'. Defaults to None, 5, 10 and
30 years, or 10 years for a butterfly.
- <u>short_maturity (float &#124; str &#124; list &#124; None, optional):</u> The shorter maturity (or
maturities), in years or as labels such as '3M'. Defaults to None, 3 months
and 2 years, or 2 years for a butterfly.
- <u>country (str, optional):</u> The country, see `get_government_bond_yield_curve`.
Defaults to "United States".
- <u>date (str &#124; None, optional):</u> The day of the curve (YYYY-MM-DD), or the last day
before it with a curve. Defaults to None, the end date.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results
to. Defaults to None, which uses the rounding of the class.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.
- <u>middle_maturity (float &#124; str &#124; list &#124; None, optional):</u> The middle maturity (or
maturities) of a butterfly, in years or as labels such as '5Y'. Defaults to
None, which calculates spreads.

**Returns:**

pd.DataFrame: The spread (decimal) for each combination of long (rows) and short
maturity (columns), or with `middle_maturity` the butterfly (decimal) for each
middle maturity (rows) and pair of wings (columns, short/long), NaN where the middle
maturity does not lie between the wings.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome()

fixedincome.get_yield_curve_spread(date="2026-11-05")
```

Which returns:

| Long Maturity   |     3M |     2Y |
|:----------------|-------:|-------:|
| 5Y              | 0.0042 | 0.0013 |
| 10Y             | 0.0067 | 0.0038 |
| 30Y             | 0.0108 | 0.0079 |

---

## get_breakeven_inflation_rate
Calculates the breakeven inflation rates of the US Treasury curve on a day: the nominal par yield minus the real (TIPS) par yield of the 5, 7, 10, 20 and 30-year maturities. It is the rate of inflation that would make an investor indifferent between holding a nominal Treasury and a TIPS of the same maturity, and is widely used as a market-implied measure of expected inflation.

The formula is as follows:

$$
\text{Breakeven Inflation Rate} = \text{Nominal Yield} - \text{Real Yield}
$$

Where both yields are the Treasury's par yield curve rates (nominal and real), quoted as bond-equivalent yields compounded twice a year, and the breakeven rate is their simple difference, as FRED publishes it as T5YIE and T10YIE, not (1 + Nominal) / (1 + Real) - 1.

The breakeven rate is often read as the market's expected inflation, but it also contains an inflation risk premium, which raises it, and a liquidity premium on inflation-linked bonds, which lowers it, so it rises and falls in market stress for reasons other than inflation expectations. The comparison is with CPI-U, the index TIPS pay on. The daily history, with the 5-year, 5-year forward rate, is `get_inflation_expectations` in the Economics module; for yields of your own, use `yieldcurve_model.get_breakeven_inflation_rate`.

**Also known as:** TIPS breakeven spread, inflation breakeven.

**Args:**

- <u>date (str &#124; None, optional):</u> The day (YYYY-MM-DD), or the last business day
before it. Defaults to None, the end date.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results
to. Defaults to None, which uses the rounding of the class.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The Nominal Yield, Real Yield and Breakeven Inflation Rate (decimals)
by maturity, with the date of the yields.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome()

fixedincome.get_breakeven_inflation_rate(date="2026-11-05")
```

Which returns:

| Maturity   |   Nominal Yield |   Real Yield |   Breakeven Inflation Rate | Date       |
|:-----------|----------------:|-------------:|---------------------------:|:-----------|
| 5 Year     |          0.0459 |       0.0233 |                     0.0226 | 2026-11-05 |
| 7 Year     |          0.047  |       0.0246 |                     0.0224 | 2026-11-05 |
| 10 Year    |          0.0484 |       0.026  |                     0.0224 | 2026-11-05 |
| 20 Year    |          0.0527 |       0.029  |                     0.0237 | 2026-11-05 |
| 30 Year    |          0.0525 |       0.0305 |                     0.022  | 2026-11-05 |

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
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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

Every curve comes from the official source:

- United States: the U.S. Department of the Treasury's par yield curve, 1 month to 30 years, from 1990.
- Euro Area: the yield curve the European Central Bank estimates from the bonds of all euro area central governments, 3 months to 30 years, from 2004, as zero-coupon (spot) rates of a Svensson model, continuously compounded.
- Germany: the term structure the Deutsche Bundesbank estimates from listed federal securities, 1 to 30 years, as zero-coupon (spot) rates of a Svensson model, continuously compounded.
- United Kingdom: the Bank of England's nominal par yields of gilts, 5, 10 and 20 years.
- Japan: the Ministry of Finance's Japanese government bond yields, 1 to 40 years, from 1974.
- Canada: the Bank of Canada's treasury bill yields (1 month to 1 year, weekly) and benchmark bond yields (2 to 30 years).
- Sweden: the Riksbank's treasury bill and government bond yields, 1 month to 10 years.
- Norway: Norges Bank's generic government bond yields, 3 to 10 years.
- Australia: the Reserve Bank of Australia's government bond yields interpolated to 2, 3, 5 and 10 years, from 2013.

With period="monthly", every other European Union member, such as France, Italy, Spain, the Netherlands and Poland, is included with its 10-year yield, the long-term interest rate for convergence purposes the ECB publishes monthly. For other countries, see `get_government_bond_yield` for the monthly 3-month and 10-year rates of around forty countries from the OECD. Only the requested countries are retrieved, and only the days that are not cached yet.

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
- <u>growth (bool, optional):</u> Whether to return the growth data or the actual data. Defaults to False.
- <u>lag (int, optional):</u> The number of periods to lag the data by. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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

With a FinancialModelingPrep API key the rates come from FinancialModelingPrep, and without one, or when the key's plan does not include them, from the U.S. Department of the Treasury directly, which gives the same figures.

These are par yields: the coupons at which a new Treasury of each maturity would price at par, interpolated by the Treasury from the most recently auctioned securities. Discounting individual cash flows needs zero-coupon (spot) rates bootstrapped from them; on a steep curve the two differ by several basis points at long maturities. The 10-year minus 2-year and 10-year minus 3-month spreads from this curve are the most watched recession indicators.

**Also known as:** the Treasury yield curve, the risk-free curve.

**Args:**

- <u>maturities (float &#124; str &#124; list &#124; None, optional):</u> The maturities to return, in years
or as labels such as "3M" and "10Y" (a list or a comma-separated string, e.g.
"2Y,10Y,30Y"), from 1M, 2M, 3M, 6M, 1Y, 2Y, 3Y, 5Y, 7Y, 10Y, 20Y and 30Y.
Defaults to None, which returns every maturity.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to return the growth data or the actual data. Defaults to False.
- <u>lag (int, optional):</u> The number of periods to lag the data by. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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

fixedincome.get_treasury_rates(maturities='3M,2Y,10Y,30Y')
```

Which returns:

| Date       |   3 Month |   2 Year |   10 Year |   30 Year |
|:-----------|----------:|---------:|----------:|----------:|
| 2024-01-02 |    0.0546 |   0.0433 |    0.0395 |    0.0408 |
| 2024-01-03 |    0.0548 |   0.0433 |    0.0391 |    0.0405 |
| 2024-01-04 |    0.0548 |   0.0438 |    0.0399 |    0.0413 |
| 2024-01-05 |    0.0547 |   0.044  |    0.0405 |    0.0421 |
| 2024-01-08 |    0.0549 |   0.0436 |    0.0401 |    0.0417 |
| 2024-01-09 |    0.0547 |   0.0436 |    0.0402 |    0.0418 |
| 2024-01-10 |    0.0546 |   0.0437 |    0.0404 |    0.042  |
| 2024-01-11 |    0.0546 |   0.0426 |    0.0398 |    0.0418 |
| 2024-01-12 |    0.0545 |   0.0414 |    0.0396 |    0.042  |

---

## get_zero_coupon_curve
Calculates the zero-coupon (spot) yield curve of a country by bootstrapping its government bond par yields. A par yield is the coupon at which a bond trades at par, so it mixes the discount rates of every coupon date; the zero-coupon rate of a maturity is the single rate that discounts a payment at that date. Zero-coupon rates are what bonds and other cash flows are discounted with, and what forward rates and the curve models (Nelson-Siegel, Vasicek) are built on.

Maturities up to one year are treasury bills, which pay no coupon, so their yield only needs converting to annual compounding: US bill yields are bond-equivalent yields (simple interest up to half a year), Canadian bill yields simple interest on a 365-day year and Swedish bill yields simple interest on a 360-day year. Beyond that the par yields are interpolated linearly to every coupon date and each discount factor follows from the earlier ones:

$$
P (t_{n}) = (1 - c / f \sum_{i < n} P (t_{i})) / (1 + c / f)
$$

with c the par yield of maturity $$t_{n}$$ and f the coupons per year (two, and one for Sweden and Norway). The curves of the Euro Area and Germany are estimated as zero-coupon curves by the ECB and the Bundesbank, which publish them continuously compounded; they are converted to annual compounding like the others. A curve needs a maturity of a year or less to start from, so the United Kingdom, Norway and Australia (and Canada before its bill yields start) are not covered.

How the curve is read between the quoted maturities is a choice (Hagan and West, 2006). By default (interpolation="linear_par") the par yields are interpolated linearly to every coupon date, as above, and the zero rates linearly between those dates. The other interpolations bootstrap the zero curve itself: the coupon dates of a bond lie between quoted maturities, so their discount factors are read from the curve with the interpolation, and the discount factor of each maturity is solved so that its par bond prices at par on that curve. For the interpolations whose shape depends on the maturities further out (the cubic splines and monotone convex) the bootstrap is repeated until the curve no longer changes (to 1e-13). They work on continuously compounded zero rates r(t), with $$P (t) = e^{- r (t) t}$$:

- "linear_zero": r(t) linear between the maturities.
- "log_linear": ln P(t) linear between the maturities, so the instantaneous forward rate is flat between them (piecewise flat forward, Hagan and West's raw interpolation).
- "natural_cubic": a natural cubic spline on r(t).
- "monotone_cubic": a cubic on r(t) with the slopes of the natural spline held by Hyman's (1983) filter, so it does not overshoot where the rates rise or fall.
- "monotone_convex": Hagan and West's (2006) monotone convex method on the forward rates, which keeps the discrete forwards between the maturities, gives a continuous forward curve and does not oscillate.

The zero rate before the first maturity is that of the first maturity (monotone convex extrapolates the forward instead) and beyond the last maturity it is held at the last one. The curves of the Euro Area and Germany are zero-coupon curves already, so the interpolation only matters between their maturities. Whatever the interpolation, the rates returned are annually compounded.

For more information, see the following papers:

- Hagan, P.S. and West, G. (2006). "Interpolation Methods for Curve Construction." Applied Mathematical Finance, 13(2), 89-129.
- Hyman, J.M. (1983). "Accurate Monotonicity Preserving Cubic Interpolation." SIAM Journal on Scientific and Statistical Computing, 4(4), 645-654.

The interpolations and their bootstrap are referenced against QuantLib's PiecewiseLinearZero, PiecewiseLogLinearDiscount, PiecewiseNaturalCubicZero, MonotonicCubicZeroCurve and PiecewiseConvexMonotoneForward (without forced positivity, quadraticity 0 and monotonicity 1), [https://www.quantlib.org](https://www.quantlib.org){:target="_blank"}. The monotone cubic sets the slope to zero at a local extremum of the zero rates, where QuantLib applies Hyman's extended filter.

**Also known as:** spot curve, zero curve, bootstrapped curve, discount curve, curve interpolation, monotone convex, flat forward.

**Args:**

- <u>countries (list[str] &#124; str, optional):</u> The countries, see
`get_government_bond_yield_curve`. Defaults to "United States".
- <u>period (str, optional):</u> Whether to use the daily, weekly or monthly curves.
Defaults to "daily".
- <u>interpolation (str, optional):</u> "linear_par", "linear_zero", "log_linear",
"natural_cubic", "monotone_cubic" or "monotone_convex". Defaults to
"linear_par".
- <u>maturities (float &#124; str &#124; list &#124; None, optional):</u> The maturities to return the
zero rates of, in years or as labels such as '4Y' (a list or a
comma-separated string). Defaults to None, the maturities the curve quotes.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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

The Nelson-Siegel model has a level $$\beta_{0}$$ (the yield at an infinite maturity), a slope $$\beta_{1}$$ (the short end minus the long end) and a curvature $$\beta_{2}$$ (a hump that peaks at about $$1.8 \tau_{1}$$ years):

$$
y (m) = \beta_{0} + \beta_{1} (1 - e^{- m / \tau_{1}}) / (m / \tau_{1}) + \beta_{2} [(1 - e^{- m / \tau_{1}}) / (m / \tau_{1}) - e^{- m / \tau_{1}}]
$$

Svensson adds a second curvature $$\beta_{3}$$ with its own decay $$\tau_{2}$$, which fits the long end better. With the dozen maturities a government curve has, the six Svensson parameters are weakly identified, as the level and the second curvature can offset each other; set svensson=False for the three factors to read as level, slope and curvature (Diebold and Li, 2006).

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
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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

## get_carry_and_roll_down
Calculates the carry and roll-down of zero-coupon government bonds on every date: the return in excess of financing that a bond of each maturity earns over the horizon if the yield curve stays as it is. The bond earns its own yield over the financing rate (the carry) and, as it ages, is priced at the yield of a shorter maturity, which on an upward sloping curve is lower, so its price rises (the roll-down). Together they are the return an unchanged curve gives, the bond carry of Koijen, Moskowitz, Pedersen and Vrugt (2018): the yield spread over the short rate plus the roll-down. It shows where on the curve a position is paid most for holding it, and where an inverted curve makes holding a bond cost money.

The formula is as follows:

$$
\text{Carry} = (1 + z(T))^{h} - (1 + r)^{h}
$$

$$
\text{Roll-Down} = \frac{(1 + z(T))^{T}}{(1 + z(T - h))^{T - h}} - (1 + z(T))^{h}
$$

$$
\text{Total} = \text{Carry} + \text{Roll-Down} = \frac{P(T - h)}{P(T)} - (1 + r)^{h}
$$

where:

$$
z(m) = \text{The zero-coupon rate of maturity}\; m,\;\; \text{annually compounded}
$$

$$
P(m) = (1 + z(m))^{- m},\;\; \text{the price of a zero-coupon bond paying 1 at } m
$$

$$
T = \text{The maturity of the bond},\;\; \text{in years}
$$

$$
h = \text{The horizon},\;\; \text{in years}
$$

$$
r = \text{The financing rate over the}\; \text{horizon:} \;\text{the zero-coupon rate of the horizon},\;\; z \text{(} h \text{)}
$$

The curve is the zero-coupon curve of `get_zero_coupon_curve`, bootstrapped from the government bond par yields of the day (or published as zero-coupon rates for the Euro Area and Germany) and annually compounded, with the zero rate of every coupon date the bootstrap solves for. z(T - h) and z(h) are interpolated linearly on it, as for `get_forward_rate`, and held flat below the shortest maturity, so where the curve starts beyond the horizon (Germany at one year) the financing rate is the shortest rate. Beyond the longest maturity L the curve is held flat as well, so a bond with T - h at or beyond L has a roll-down of 0 and only the carry (1 + z(L))^h - (1 + z(h))^h. Each bond is repriced exactly on the unchanged curve: the carry is what it earns over the financing if its own yield stays z(T), the roll-down the price change from its yield moving to z(T - h), valued at the horizon. Every value is a return over the horizon, not annualized. Germany and Japan quote maturities from one year, so a horizon of a year avoids the flat extrapolation there. For a curve or a financing rate of your own, use `yieldcurve_model.get_carry_and_roll_down`.

To first order, with $$D = (T - h) / (1 + z (T))$$ the modified duration (annual compounding) of the bond at the horizon, as Koijen et al. (2018) approximate it:

- Carry ≈ $$(z (T) - r) \times h$$
- Roll-Down ≈ $$- D \times (z (T - h) - z (T))$$

For more information, see the following sources:

- Koijen, R.S.J., Moskowitz, T.J., Pedersen, L.H. and Vrugt, E.B. (2018). "Carry." Journal of Financial Economics, 127(2), 197-225.
- Ilmanen, A. (2011). "Expected Returns: An Investor's Guide to Harvesting Market Rewards." Wiley, chapter 9.

**Also known as:** bond carry, rolldown, roll yield, horizon return on an unchanged curve.

**Args:**

- <u>countries (list[str] &#124; str, optional):</u> The countries, see
`get_zero_coupon_curve`. Defaults to "United States".
- <u>period (str, optional):</u> Whether to use the daily, weekly or monthly curves.
Defaults to "daily".
- <u>horizon (float &#124; str, optional):</u> The holding period, in years or as a label such
as "3M" or "1Y". Defaults to 0.25 (three months).
- <u>maturities (list[float &#124; str] &#124; str &#124; None, optional):</u> The maturities of the
bonds, in years or as labels such as "2Y" (a list or a comma-separated
string). A maturity shorter than the horizon is NaN. Defaults to None, every
maturity of the curve longer than the horizon.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The Carry, Roll-Down and Total as decimals (returns over the
horizon), indexed by date with a column per country, component and maturity. A
date whose curve has no maturity of a year or less to bootstrap from (such as
Canada before its bill yields of the day are published) is left out.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome(start_date='2026-10-19', end_date='2026-10-23')

carry_and_roll_down = fixedincome.get_carry_and_roll_down(maturities='2Y,5Y,10Y,30Y')

carry_and_roll_down['United States']['Total']
```

Which returns:

|            |     2Y |     5Y |    10Y |    30Y |
|:-----------|-------:|-------:|-------:|-------:|
| 2026-10-19 | 0.0024 | 0.0022 | 0.0033 | 0.002  |
| 2026-10-20 | 0.0025 | 0.0022 | 0.0031 | 0.0019 |
| 2026-10-21 | 0.0026 | 0.0021 | 0.0032 | 0.0019 |
| 2026-10-22 | 0.0021 | 0.0017 | 0.0028 | 0.002  |
| 2026-10-23 | 0.0022 | 0.0019 | 0.003  | 0.002  |

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
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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

## get_term_premium
Retrieves the Treasury term premia of Adrian, Crump and Moench (2013), as the Federal Reserve Bank of New York estimates them daily from 1961 for maturities of 1 to 10 years. A Treasury yield is split into the average short rate investors expect over the bond's life and the term premium: the extra yield they demand for holding a long bond instead of rolling over short ones. The split tells whether a move in long yields comes from expected monetary policy or from compensation for risk, such as inflation and fiscal uncertainty.

Adrian, T., Crump, R. K., & Moench, E. (2013). Pricing the Term Structure with Linear Regressions. Journal of Financial Economics, 110(1), 110-138. [https://doi.org/10.1016/j.jfineco.2013.04.009](https://doi.org/10.1016/j.jfineco.2013.04.009){:target="_blank"}

Three components are returned per maturity: the "Term Premium", the "Expected Short Rate" (the risk-neutral yield, the yield if investors were indifferent to risk) and the "Fitted Yield" of the model, which is their sum. The model is fitted to the zero-coupon Treasury curve of Gürkaynak, Sack and Wright (2007), so every value is a continuously compounded zero-coupon rate, as a decimal fraction (0.0067 for 0.67%). Weekly and monthly periods take the last day of each period, matching the New York Fed's own month-end series.

The term premium is a model estimate rather than an observed price: it rests on the model's five pricing factors (principal components of the yield curve), and other models, such as that of Kim and Wright (2005), give different levels with similar movements.

**See definition:** [https://www.newyorkfed.org/research/data_indicators/term-premia-tabs](https://www.newyorkfed.org/research/data_indicators/term-premia-tabs){:target="_blank"}

**Also known as:** ACM term premium, Treasury term premium, risk-neutral yield, expected short rate, bond risk premium.

**Args:**

- <u>period (str, optional):</u> Whether to return the daily, weekly or monthly data.
Defaults to "daily".
- <u>maturity_years (list[int] &#124; str &#124; None, optional):</u> The maturities in years to keep,
from 1 to 10, e.g. [2, 5, 10] (or "2,5,10"). Defaults to None, which keeps every
maturity.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>growth (bool, optional):</u> Whether to return the growth data or the actual data. Defaults to False.
- <u>lag (int, optional):</u> The number of periods to lag the growth data by. Defaults to 1.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. When
combined with growth=True, standardizes the growth values instead of the raw
values. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The rates, indexed by date with a column per component ("Term
Premium", "Expected Short Rate" and "Fitted Yield") and maturity ("1Y" to "10Y").

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome(start_date='2026-05-01', end_date='2026-10-31')

term_premium = fixedincome.get_term_premium(period='monthly', maturity_years=[2, 5, 10])

term_premium['Term Premium']
```

Which returns:

|         |     2Y |     5Y |    10Y |
|:--------|-------:|-------:|-------:|
| 2026-05 | 0.0011 | 0.003  | 0.0066 |
| 2026-06 | 0.0004 | 0.0018 | 0.0051 |
| 2026-07 | 0.0018 | 0.0043 | 0.0083 |
| 2026-08 | 0.0015 | 0.0038 | 0.0076 |
| 2026-09 | 0.0042 | 0.0057 | 0.0089 |
| 2026-10 | 0.0024 | 0.0037 | 0.0068 |

---

## get_eiopa_risk_free_rate
Retrieves the risk-free interest rate term structures the European Insurance and Occupational Pensions Authority (EIOPA) publishes monthly: the curves European insurers must discount their liabilities with under Solvency II. They cover the euro and the currencies of every country of the European Economic Area, plus Switzerland, the United Kingdom, Australia, Canada, China, Colombia, Hong Kong, Japan, Taiwan and the United States, for maturities of 1 to 150 years. Beyond the last liquid maturity each curve converges to the ultimate forward rate (UFR), as Solvency II prescribes.

Four curves are published: the basic spot curve (curve="spot_no_va"), the spot curve with the volatility adjustment (curve="spot_with_va"), and the basic curve after the interest rate shocks of the Solvency II standard formula (curve="shock_up" and curve="shock_down"). EIOPA ships the shocked worksheets as formulas without computed values, so they are computed here with those formulas: upwards by the relative shock per maturity and at least one percentage point, downwards by the relative shock with negative rates left unchanged. Every value is a decimal fraction (0.0358 for 3.58%), at the end of the month the release is for, and an annually compounded spot rate, as Solvency II defines the term structure: a rate r discounts a payment in t years with (1 + r)^(-t).

EIOPA's page links the releases from January 2023; each is a separate file, so only the months between the start and end date are downloaded, and a release is cached for a year since it does not change.

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
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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
\text{Type 1 Equity Charge} = 0.39 + \text{Symmetric Adjustment},\;\; \text{for equities listed in the EEA or OECD}
$$

$$
\text{Type 2 Equity Charge} = 0.49 + \text{Symmetric Adjustment},\;\; \text{for other equities}
$$

Every value is a decimal fraction (0.0771 for 7.71%). Weekly and monthly periods take the value on the last day of each period, which is the value insurers apply at that reporting date.

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
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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
Retrieves the UK yield curves the Bank of England estimates daily from 1985, for maturities from 0.5 years to 40 years (25 years for OIS): the nominal spot curve of UK government bonds (gilts) and the spot curve of overnight index swaps on SONIA (OIS, from 2009). Unlike the par yields of 5, 10 and 20 years in `get_government_bond_yield_curve`, these are zero-coupon spot rates over the full range of maturities with history back to 1985. The Bank of England publishes them continuously compounded, and they are returned that way: a spot rate r discounts a payment in t years with exp(-r t).

The Bank of England's real and implied inflation curves are part of `economics.get_real_yield_curve` and `economics.get_breakeven_inflation_expectations` (countries='United Kingdom').

The archive is a set of large files, of which only those covering the requested years are read, and they are cached since past years do not change. Weekly and monthly periods take the curve on the last day of each period.

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
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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

## get_inflation_swap_rate
Calculates the zero-coupon and year-on-year inflation swap rates the government bond market implies: the fair fixed rates of swaps on US CPI-U inflation (from Treasury and TIPS yields) or euro area HICP inflation excluding tobacco (from nominal and inflation-linked German federal securities).

A zero-coupon inflation swap pays the growth of the price index over its life against a fixed rate compounded over the same years; a year-on-year swap pays each year's inflation against a fixed rate every year. With nominal and real zero-coupon curves, the forward index of maturity T is $$I (0) \cdot P_{\text{real}} (T)$$ / P_nominal(T) (Jarrow and Yildirim, 2003), so the zero-coupon swap rate is the zero-coupon breakeven inflation rate and the year-on-year swap rate the discount-weighted average of the forward year-on-year rates (Kerkhof, 2005; Brigo and Mercurio, 2006, ch. 15).

The formula is as follows:

$$
\text{Zero-Coupon Inflation Swap Rate:}\;\; K(T) = \frac{1 + n(T)}{1 + r(T)} - 1
$$

$$
\text{Forward Year-on-Year Rate:}\;\; f_{i} = \frac{(1 + K(i))^{i}}{(1 + K(i - 1))^{i - 1}} - 1
$$

$$
\text{Year-on-Year Inflation Swap Rate} = \frac{\sum(P(i) f_{i})}{\sum(P(i))},\;\; \text{over}\;\; i = 1,\; \ldots,\; T
$$

where n(T) and r(T) are the annually compounded nominal and real zero-coupon rates of maturity T and P(i) = (1 + n(i))^(-i) the nominal discount factor. The nominal zero rates are bootstrapped from the government par yield curve (see `get_zero_coupon_curve`), the real ones from the real par yields of the inflation-linked bonds with their coupons (twice a year for TIPS, once for German inflation-linked German federal securities), held at the shortest quoted real yield before its maturity. Every rate is annually compounded. The year-on-year rates carry no convexity adjustment, which needs the volatilities of real and nominal rates: it is a few basis points up to ten years.

Referenced against QuantLib's ZeroCouponInflationSwap and YearOnYearInflationSwap (fairRate) on the same forward index.

**Also known as:** ZCIS rate, YoY swap rate, zero-coupon breakeven inflation, inflation swap curve.

**Args:**

- <u>country (str, optional):</u> "United States" (CPI-U, Treasury and TIPS curves) or
"Germany" (euro area HICP excluding tobacco, Bundesbank curves). Defaults to
"United States".
- <u>date (str &#124; None, optional):</u> The day (YYYY-MM-DD), or the last day before it with a
real yield curve. Defaults to None, the end date.
- <u>maturities (list[float] &#124; str &#124; None, optional):</u> The swap maturities in years, or
labels such as "5Y", as a list or a comma-separated string, all positive. A
maturity beyond the longest of the nominal and real curves holds their zero
rates flat from there, which is logged. Defaults to None, the maturities of
the real yield curve.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the rounding of the class.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per maturity (in years), the Nominal Zero Rate, Real Zero Rate,
Zero-Coupon Inflation Swap Rate and Year-on-Year Inflation Swap Rate (decimals,
annually compounded; the year-on-year rate only for whole years) and the Date of
the curves.

**Notes:**

- The rates are breakevens of government bonds. Traded inflation swaps are quoted a
few basis points above them (the inflation swap basis), which reflects the
liquidity of inflation-linked bonds and the funding of the hedge.
- The breakevens include the inflation risk premium, so they are not a pure forecast
of inflation.
- The index of the swaps is observed with the lag of the bonds (three months for TIPS
and inflation-linked German federal securities).

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome(start_date="2026-10-01", end_date="2026-11-20")

fixedincome.get_inflation_swap_rate(
    show_columns=["Zero-Coupon Inflation Swap Rate", "Year-on-Year Inflation Swap Rate", "Date"]
)
```

Which returns:

|   Maturity |   Zero-Coupon Inflation Swap Rate |   Year-on-Year Inflation Swap Rate | Date       |
|-----------:|----------------------------------:|-----------------------------------:|:-----------|
|          5 |                            0.0217 |                             0.0216 | 2026-11-20 |
|          7 |                            0.0215 |                             0.0215 | 2026-11-20 |
|         10 |                            0.0215 |                             0.0215 | 2026-11-20 |
|         20 |                            0.0242 |                             0.0234 | 2026-11-20 |
|         30 |                            0.0211 |                             0.022  | 2026-11-20 |

---

## get_forward_inflation_index
Calculates the forward US consumer price index (CPI-U, not seasonally adjusted) of every coming month from the inflation swap rates the Treasury and TIPS curves imply, with the monthly seasonality of the CPI.

The zero-coupon inflation swap rates fix the growth of the index over whole years (see `get_inflation_swap_rate`). Between them, prices rise faster in some months than in others, so each month's forward index is moved by its seasonal factor relative to that of the base month (Belgrade, Benhamou and Koehler, 2004; Kerkhof, 2005). The seasonal factors are estimated from the CPI history: the average log change of each calendar month above the average of all months, accumulated over the year and scaled so that the twelve factors multiply to 1.

The formula is as follows:

$$
I(m) = \frac{I(0) \cdot \left(1 + K\left(\frac{m}{12}\right)\right)^{\frac{m}{12}} \cdot S_{monthofm}}{S_{basemonth}}
$$

$$
K(T) = \frac{1 + n(T)}{1 + r(T)} - 1
$$

$$
s_{k} = \operatorname{MEAN}\left(\ln\left(\frac{I_{t}}{I_{t-1}}\right) \;\text{in calendar month}\; k\right) - \operatorname{MEAN}\left(\ln\left(\frac{I_{t}}{I_{t-1}}\right)\right)
$$

$$
S_{k} = \exp(s_{1} + \ldots + s_{k}),\;\; \text{scaled so that PRODUCT}(S_{k}) = 1
$$

where I(0) is the CPI of the base month, m the months after it, K the annually compounded zero-coupon inflation swap rate (interpolated linearly between whole years), n and r the annually compounded nominal and real zero rates of the Treasury and TIPS curves and S the seasonal factors (all 1 without seasonality). The base month is the third month before the date's month, the CPI the reference CPI of TIPS starts from on the first of the month (31 CFR 356), so the breakevens price the inflation from it on.

Referenced against QuantLib's ZeroInflationIndex forecasts on a ZeroInflationCurve with MultiplicativePriceSeasonality.

**Also known as:** forward CPI, CPI fixing curve, inflation index curve, seasonal adjustment of inflation swaps.

**Args:**

- <u>date (str &#124; None, optional):</u> The day (YYYY-MM-DD) of the curves, or the last day
before it with a real yield curve. Defaults to None, the end date.
- <u>years (int, optional):</u> The number of years of months after the base month.
Defaults to 5.
- <u>seasonality (bool, optional):</u> Whether to apply the monthly seasonal factors.
Defaults to True.
- <u>seasonality_years (int, optional):</u> The years of CPI history before the base month
the seasonal factors are estimated on. The keyless BLS API covers about three
years; a FRED API key gives the rest. Defaults to 10.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the rounding of the class.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per month after the base month, the Forward CPI (with the seasonal
factors when seasonality is True), the Trend CPI (without them), the Seasonal
Factor relative to the base month and the Zero-Coupon Inflation Swap Rate of the
horizon (annually compounded).

**Notes:**

- Without a FRED API key the seasonality is estimated on the CPI the BLS returns
(about three years before the base month), which is logged.
- The swap rates are breakevens of government bonds, see `get_inflation_swap_rate`.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome(start_date="2026-10-01", end_date="2026-11-20")

fixedincome.get_forward_inflation_index(years=1)
```

Which returns:

| Month   |   Forward CPI |   Trend CPI |   Seasonal Factor |   Zero-Coupon Inflation Swap Rate |
|:--------|--------------:|------------:|------------------:|----------------------------------:|
| 2026-09 |       335.388 |     335.524 |            0.9996 |                            0.0196 |
| 2026-10 |       335.709 |     336.068 |            0.9989 |                            0.0196 |
| 2026-11 |       334.568 |     336.613 |            0.9939 |                            0.0196 |
| 2026-12 |       334.306 |     337.16  |            0.9915 |                            0.0196 |
| 2027-01 |       335.731 |     337.707 |            0.9941 |                            0.0196 |
| 2027-02 |       337.16  |     338.255 |            0.9968 |                            0.0196 |
| 2027-03 |       339.026 |     338.804 |            1.0007 |                            0.0196 |
| 2027-04 |       340.487 |     339.354 |            1.0033 |                            0.0196 |
| 2027-05 |       341.337 |     339.904 |            1.0042 |                            0.0196 |
| 2027-06 |       341.073 |     340.456 |            1.0018 |                            0.0196 |
| 2027-07 |       341.073 |     341.008 |            1.0002 |                            0.0196 |
| 2027-08 |       341.562 |     341.562 |            1      |                            0.0196 |

---

## get_loan_payment
Calculates the monthly payment of a new 30-year fixed-rate mortgage at every weekly US mortgage rate: what the same loan costs a buyer at each date, with the total interest over its life, the interest in its first payment and how the payment compares with the one at the start date. By default the loan is 400,000 US dollars, so the payment of the same house at the same price can be followed through the rate cycle (1,611.86 a month at the 2.65% of January 2021, 2,709.74 at 7.18%, 68.1% more).

The loan is an annuity, repaid in equal payments. The formula is as follows:

$$
\text{Payment} = \frac{L \cdot r}{1 - (1 + r)^{-n}},\;\; \text{or}\;\; \frac{L}{n} \;\text{when}\; r \;\text{is zero}
$$

$$
\text{Total Interest} = \text{Payment} \cdot n - L
$$

$$
\text{First Payment Interest} = L \cdot r
$$

$$
\text{Change} = \frac{\text{Payment}}{\operatorname{Payment}(\text{first date})} - 1
$$

Where:

$$
L = \text{Principal},\;\; \text{the amount borrowed}
$$

$$
r = \frac{\text{Rate}}{\text{payments per year}},\;\; \text{the rate per payment}
$$

$$
n = \text{years} \cdot \text{payments per year},\;\; \text{the number of payments}
$$

US mortgage rates are quoted as a nominal annual rate compounded monthly, so the rate per payment is the annual rate divided by twelve (7.18% is 0.5983% a month). The rate is the weekly average 30-year fixed rate of Freddie Mac's Primary Mortgage Market Survey (the rate of `Economics.get_mortgage_rate_30_year`), from FRED when a FRED API key is set and from Freddie Mac otherwise. For a rate of your own, use `loan_model.get_loan_payment`, which takes a number or a series of rates.

**Also known as:** mortgage payment, monthly payment, annuity payment, mortgage calculator, loan calculator, cost of a mortgage.

**Args:**

- <u>principal (float, optional):</u> The amount borrowed. Defaults to 400,000.
- <u>years (float, optional):</u> The term of the loan in years. The rate stays the 30-year
fixed mortgage rate for another term. Defaults to 30.
- <u>payments_per_year (int, optional):</u> The number of payments per year. Defaults to 12.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the rounding of the class.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per survey date the Rate (a decimal), the Payment, the Total Interest
over the life of the loan and the First Payment Interest, in the currency of the
principal, and the Change of the Payment since the first date (a decimal), as the
Change of `get_affordable_loan`. The change between two other dates follows from
narrowing start_date to the first of them.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome(start_date='2021-01-01', end_date='2026-11-06')

fixedincome.get_loan_payment().iloc[[0, -1]]
```

Which returns:

| Date       |   Rate |   Payment |   Total Interest |   First Payment Interest |   Change |
|:-----------|-------:|----------:|-----------------:|-------------------------:|---------:|
| 2021-01-07 | 0.0265 |   1611.86 |           180268 |                  883.333 |   0      |
| 2026-11-05 | 0.0718 |   2709.74 |           575506 |                 2393.33  |   0.6811 |

---

## get_affordable_loan
Calculates the loan a fixed monthly payment carries at every weekly US mortgage rate: the 30-year fixed-rate mortgage the payment repays, and how that loan compares with the one it carried at the start date. By default the payment is the one a 400,000 US dollar loan had at the first rate of the range, so the answer is how much house the same monthly budget buys as rates move (the 1,611.86 a month of a 400,000 loan at 2.65% carries 237,935 at 7.18%).

The loan is an annuity, repaid in equal payments. The formula is as follows:

$$
\text{Affordable Loan} = \frac{P \cdot (1 - (1 + r)^{-n})}{r},\;\; \text{or}\;\; P \cdot n \;\text{when}\; r \;\text{is zero}
$$

$$
\text{Change} = \frac{\text{Affordable Loan}}{\text{Affordable Loan}(\text{first date})} - 1
$$

Where:

$$
P = \text{Payment per period}
$$

$$
r = \frac{\text{Rate}}{\text{payments per year}},\;\; \text{the rate per payment}
$$

$$
n = \text{years} \cdot \text{payments per year},\;\; \text{the number of payments}
$$

US mortgage rates are quoted as a nominal annual rate compounded monthly, so the rate per payment is the annual rate divided by twelve. The rate is the weekly average 30-year fixed rate of Freddie Mac's Primary Mortgage Market Survey, from FRED when a FRED API key is set and from Freddie Mac otherwise. For a rate of your own, use `loan_model.get_affordable_loan`.

**Also known as:** affordability, how much can I borrow, mortgage affordability, borrowing capacity, loan amount from payment.

**Args:**

- <u>payment (float &#124; None, optional):</u> The payment per period. Defaults to None, the
payment of a loan of principal at the first rate between the start and end date.
- <u>principal (float, optional):</u> The loan whose payment at the first rate is used when
no payment is given. Defaults to 400,000.
- <u>years (float, optional):</u> The term of the loan in years. The rate stays the 30-year
fixed mortgage rate for another term. Defaults to 30.
- <u>payments_per_year (int, optional):</u> The number of payments per year. Defaults to 12.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the rounding of the class.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per survey date the Rate (a decimal), the Payment, the Affordable Loan
and its Change since the first date (a decimal).

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome(start_date='2021-01-01', end_date='2026-11-06')

fixedincome.get_affordable_loan().iloc[[0, -1]]
```

Which returns:

| Date       |   Rate |   Payment |   Affordable Loan |   Change |
|:-----------|-------:|----------:|------------------:|---------:|
| 2021-01-07 | 0.0265 | 1611.8552 |       400000.0000 |   0.0000 |
| 2026-11-05 | 0.0718 | 1611.8552 |       237935.0883 |  -0.4052 |

---

## get_amortization_schedule
Calculates the amortization schedule of a new 30-year fixed-rate mortgage at the US mortgage rate of a date: per monthly payment the part that is interest, the part that repays the loan and the balance left. Early payments are mostly interest, the more so the higher the rate: the first payment of a 400,000 US dollar loan at 7.18% is 2,393.33 of interest and 316.41 of repayment.

The formula is as follows:

$$
\operatorname{Interest}(k) = \operatorname{Balance}(k - 1) \cdot r
$$

$$
\operatorname{Principal}(k) = \text{Payment} - \operatorname{Interest}(k)
$$

$$
\operatorname{Balance}(k) = \operatorname{Balance}(k - 1) - \operatorname{Principal}(k),\;\; \text{with}\;\; \operatorname{Balance}(0) = L
$$

Where L is the principal, r = Rate / payments per year the rate per payment and Payment the annuity payment of `get_loan_payment`. US mortgage rates are quoted as a nominal annual rate compounded monthly. The rate is the weekly average 30-year fixed rate of Freddie Mac's Primary Mortgage Market Survey on the date (the last survey on or before it), from FRED when a FRED API key is set and from Freddie Mac otherwise. For a rate of your own, use `loan_model.get_amortization_schedule`.

**Also known as:** amortization table, mortgage schedule, repayment schedule, interest and principal per payment, remaining balance.

**Args:**

- <u>principal (float, optional):</u> The amount borrowed. Defaults to 400,000.
- <u>years (float, optional):</u> The term of the loan in years. The rate stays the 30-year
fixed mortgage rate for another term. Defaults to 30.
- <u>payments_per_year (int, optional):</u> The number of payments per year. Defaults to 12.
- <u>date (str &#124; None, optional):</u> The date of the rate (YYYY-MM-DD). Defaults to None, the
latest rate up to the end date.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the rounding of the class.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per payment number (1 to years * payments per year) the Rate (a
decimal), the Payment, the Interest, the Principal repaid and the Balance after it.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome(start_date='2026-01-01', end_date='2026-11-06')

fixedincome.get_amortization_schedule().iloc[[0, 1, 2, 119, 239, 359]]
```

Which returns:

|   Payment Number |   Rate |   Payment |   Interest |   Principal |     Balance |
|-----------------:|-------:|----------:|-----------:|------------:|------------:|
|                1 | 0.0718 | 2709.7393 |  2393.3333 |    316.4060 | 399683.5940 |
|                2 | 0.0718 | 2709.7393 |  2391.4402 |    318.2992 | 399365.2948 |
|                3 | 0.0718 | 2709.7393 |  2389.5357 |    320.2036 | 399045.0912 |
|              120 | 0.0718 | 2709.7393 |  2066.2399 |    643.4995 | 344689.0688 |
|              240 | 0.0718 | 2709.7393 |  1393.1739 |   1316.5655 | 231525.8632 |
|              360 | 0.0718 | 2709.7393 |    16.1168 |   2693.6225 |      0.0000 |

---

## get_treasury_auctions
Retrieves the results of the US Treasury auctions held between the start and end date: every bill, note, bond, TIPS and floating rate note the Treasury sold, with the yield it sold at, how many times the offering was bid (the bid-to-cover ratio) and who bought it. Auction results are the most direct read of the demand for US government debt: a lower bid-to-cover ratio or a smaller share for indirect bidders (which include foreign central banks) at a large auction is a sign of weak demand.

The data comes from the Treasury's Fiscal Data API, from 1979 on. The Yield is the high yield of notes and bonds and the investment rate (the bond equivalent yield) of bills; the High Discount Rate is the discount rate bills are quoted at. The Bid-to-Cover Ratio is the Treasury's, which leaves out the Federal Reserve's (SOMA) bids, while the Total Tendered and Total Accepted include them, so their ratio is lower when the Federal Reserve rolls over maturing holdings. The bidder shares are each class's part of the competitive awards: primary dealers (who must bid at every auction), direct bidders (buying for their own account) and indirect bidders (bidding through a dealer, such as foreign and international monetary authorities and investment funds). Auctions that are announced but not yet held, and older auctions for which the Treasury did not publish a breakdown, show NaN for the missing results.

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
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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

## get_bond_universe
Retrieves thousands of individual US dollar bonds with their price, yield to maturity, modified duration and spread over Treasuries, read from the holdings of bond ETFs.

Individual bond prices are not published for free, but bond ETFs publish their holdings every day: each bond's coupon and maturity (in its name), its par amount and its market value, from which the price follows. By default this reads the iShares iBoxx $ Investment Grade Corporate Bond ETF (LQD), the iShares 0-5 Year Investment Grade Corporate Bond ETF (IGSB) and the iShares Broad USD High Yield Corporate Bond ETF (USHY): together about 8,000 investment grade and high yield corporate bonds. A bond held by several funds is listed once, with the funds that hold it, at the median of their prices on the latest Price Date among them.

The formula is as follows:

$$
\text{Price} = \frac{\text{Market Value}}{\text{Par Amount}} \cdot 100 \;(\text{a clean price per 100 of par})
$$

$$
\text{Yield to Maturity:}\;\; \text{the rate } y \text{ at which the coupons and principal},\;\; \text{discounted at} \;\left(1 + \frac{y}{2}\right) \;\text{per half year},\;\; \text{are worth the clean price plus accrued interest (see get\_yield\_to\_maturity)}
$$

$$
\text{Modified Duration} = \frac{\text{Macaulay Duration}}{1 + \frac{y}{2}} \;(\text{see} \;\text{get\_duration})
$$

$$
\text{G-Spread} = \text{Yield to Maturity} - \text{Treasury Par Yield at the bond's maturity},\;\; \text{on the bond's Price Date}
$$

Coupons are semi-annual, the US convention for corporate bonds, and the yield is a nominal annual rate compounded twice a year (bond-equivalent), like the Treasury par yields it is compared with. The coupon periods fall on the bond's actual coupon dates, counted back from maturity (on the last day of the month for a bond maturing on a month's last day), and the time in the current period is counted on the 30/360 Bond Basis, the day count of US corporate bonds: 30 days to a month and 180 days to a coupon period. The Treasury par yield at a maturity is interpolated linearly between the maturities of the US Treasury par yield curve on the price date (held at the 1-month and 30-year yield beyond them).

**Also known as:** corporate bond prices, bond yields, bond screener, credit spreads per bond, G-spread.

**Args:**

- <u>etfs (list[str] &#124; str &#124; None, optional):</u> The bond ETFs to read the holdings of, as
a list or a comma-separated string. The holdings must name each bond as
"ISSUER COUPON% MM/DD/YYYY" with its ISIN and par amount, as iShares funds
do. Defaults to None, which uses LQD, IGSB and USHY.
- <u>issuer (list[str] &#124; str &#124; None, optional):</u> Keeps the bonds whose issuer contains
this text (case-insensitive), e.g. "APPLE" or "JPMORGAN", or any of several.
Defaults to None, every issuer.
- <u>maturity_start (str &#124; None, optional):</u> Keeps the bonds maturing on or after this
date (YYYY-MM-DD). Defaults to None.
- <u>maturity_end (str &#124; None, optional):</u> Keeps the bonds maturing on or before this
date (YYYY-MM-DD). Defaults to None.
- <u>bonds (list[str] &#124; str &#124; None, optional):</u> Keeps the bonds with these ISINs or
CUSIPs, as a list or a comma-separated string. Defaults to None, every bond.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the rounding of the class.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: One row per bond, indexed by ISIN, with the Issuer, CUSIP, Coupon
(decimal), Maturity, whether it is a Rule 144A bond, the Price per 100 of par, the
Yield to Maturity and G-Spread (decimals), the Modified Duration (years), the
Price Date and the Funds that hold it, sorted by issuer and maturity.

**Notes:**

- The prices are the funds' own end-of-day valuations (iShares uses evaluated bid
prices), not trades. iShares publish the holdings valued at the previous business
day's close, which is the Price Date; FinancialModelingPrep serves only the latest
holdings, so there is no history. For the Treasuries the funds hold, the yields are
within about a basis point of the FedInvest prices of the same day (see
`get_treasury_securities`).
- Each bond is valued as of its Price Date: the accrued interest, the years to
maturity and the Treasury par yield of the G-Spread are those of that day, not of a
later settlement date.
- Only holdings that publish an ISIN are read. A US ISIN shows that a bond is a US
security, which an ISIN built from the CUSIP does not: the euro and sterling notes
of US companies carry US CUSIPs as well. FinancialModelingPrep gives no ISINs for
the funds of Vanguard, Schwab and Invesco, whose valuation dates also differ from
the date of the feed (the Vanguard holdings are those of the last month end), so
their bonds are left out, with a warning.
- The yield is to maturity. A callable bond that trades above its call price
yields less to its call date (the yield to worst), which is common among high
yield bonds; call schedules are not in the holdings.
- The fund prints the coupon to two decimals (2.125% shows as 2.13%), which moves the
yield by well under a basis point a year of maturity.
- Left out, with a count in the log: lines that are not fixed-coupon bonds (cash,
futures, swaps), floating rate notes, bank notes marked fixed-to-floating
("FXD-FRN", which switch to a floating coupon before maturity), inflation-linked
bonds, mortgage pools, perpetual bonds, holdings without an ISIN, bonds without a
US ISIN (the funds of other currencies) and prices outside 1 to 300. A
fixed-to-floating note the fund does not mark as such is kept, and its yield
assumes the fixed coupon to maturity.
- Requires a FinancialModelingPrep API key for the holdings; the Treasury curve needs
none.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome(api_key="FINANCIAL_MODELING_PREP_KEY")

bonds = fixedincome.get_bond_universe(issuer="APPLE INC")

bonds[["Coupon", "Maturity", "Price", "Yield to Maturity", "Modified Duration", "G-Spread"]].head()
```

Which returns:

| ISIN         |   Coupon | Maturity   |   Price |   Yield to Maturity |   Modified Duration |   G-Spread |
|:-------------|---------:|:-----------|--------:|--------------------:|--------------------:|-----------:|
| US037833EC07 |   0.012  | 2028-02-08 |   95.85 |              0.0475 |              1.1795 |     0.0021 |
| US037833ET32 |   0.04   | 2028-05-10 |   98.9  |              0.0478 |              1.4091 |     0.0022 |
| US037833EY27 |   0.04   | 2028-05-12 |   98.87 |              0.048  |              1.4144 |     0.0023 |
| US037833EH93 |   0.014  | 2028-08-05 |   94.55 |              0.0476 |              1.6476 |     0.0016 |
| US037833FD70 |   0.0465 | 2028-11-09 |   99.74 |              0.0479 |              1.8577 |     0.0016 |

---

## get_issuer_spreads
Compares the credit spreads of bond issuers at the same maturities: the G-Spread (yield to maturity minus the Treasury par yield) of each issuer at, for example, 2, 5 and 10 years, interpolated between the issuer's own bonds from `get_bond_universe`. Picking one bond per issuer by hand compares bonds of different maturities, and spreads rise with maturity; at the same maturity the difference is the credit.

The formula is as follows:

$$
\text{Spread} \;(\text{issuer},\; T) = s(a) + \frac{(s(b) - s(a)) \cdot (T - a)}{b - a}
$$

Where a and b are the years to maturity of the issuer's bonds closest below and above T and s their G-Spreads (see `get_bond_universe`). Bonds of the same maturity count with their average spread, and a maturity outside the range of the issuer's bonds has no spread, as a spread curve is not extrapolated.

**Also known as:** issuer spread curve, credit curve, spread at a maturity, interpolated G-spread, credit spread comparison.

**Args:**

- <u>issuer (list[str] &#124; str &#124; None, optional):</u> The issuers, each kept by the text its
name contains (case-insensitive), e.g. "APPLE,BOEING". Defaults to None, every
issuer in the funds.
- <u>maturity_years (list[float] &#124; str &#124; float &#124; None, optional):</u> The maturities in years,
as a list or comma-separated, e.g. "2,5,10". Defaults to None, which uses 2, 3,
5, 7, 10, 20 and 30 years.
- <u>etfs (list[str] &#124; str &#124; None, optional):</u> The bond ETFs to read the bonds from (see
`get_bond_universe`). Defaults to None, LQD, IGSB and USHY.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the rounding of the class.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per issuer (the name the funds give it) the G-Spread at each
maturity (decimals, columns such as "5Y"), the number of Bonds and the Shortest
and Longest years to maturity among them.

**Notes:**

- An issuer's bonds of one name can differ in seniority, and the funds list a
finance subsidiary (such as Ford Motor Credit) under its own name, apart from its
parent.
- The spreads are those of `get_bond_universe`: to maturity, at the funds' evaluated
prices of the previous business day. A callable bond priced above its call price
has a lower yield to worst.
- Requires a FinancialModelingPrep API key for the holdings.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome(api_key="FINANCIAL_MODELING_PREP_KEY")

fixedincome.get_issuer_spreads(issuer="APPLE INC,BOEING,INTEL", maturity_years="2,5,10")
```

Which returns:

| Issuer            |     2Y |     5Y |    10Y |   Bonds |   Shortest |   Longest |
|:------------------|-------:|-------:|-------:|--------:|-----------:|----------:|
| APPLE INC         | 0.0016 | 0.0031 | 0.0057 |      43 |     1.2167 |   35.7167 |
| BOEING CO         | 0.0065 | 0.0091 | 0.0105 |      20 |     1.1972 |   37.4472 |
| INTEL CORPORATION | 0.0074 | 0.0118 | 0.0157 |      35 |     1.2222 |   36.2222 |

---

## get_treasury_securities
Retrieves every marketable US Treasury (bills, notes, bonds, TIPS and floating rate notes) with its price, yield to maturity and modified duration on a day, without an API key.

Where the Treasury par yield curve gives one yield per constant maturity, this lists the roughly 460 securities themselves, from the Bureau of the Fiscal Service's daily FedInvest prices: the prices the Treasury values its own accounts at. That shows where individual issues trade off the curve (old and new issues of the same maturity, the cheapest notes to deliver into futures) and gives the yield of any maturity date.

The formula is as follows:

$$
\text{Notes and bonds:}\;\; \text{Yield to Maturity is the rate } y \text{ at which the coupons and principal},\;\; \text{discounted at} \;\left(1 + \frac{y}{2}\right) \;\text{per half year},\;\; \text{are worth the clean price plus accrued interest (see get\_yield\_to\_maturity)}
$$

$$
\text{Bills:}\;\; \text{Discount Yield} = \frac{\frac{100 - \text{Price}}{100} \cdot 360}{\text{Days}},\;\; \text{restated as the bond-equivalent yield (see get\_bond\_equivalent\_yield)}
$$

$$
\text{Modified Duration} = \frac{\text{Macaulay Duration}}{1 + \frac{y}{2}} \;(\text{see} \;\text{get\_duration})
$$

$$
\text{Floating rate notes:}\;\; \text{Yield to Maturity} = \text{Index Rate} + \text{Discount Margin and the Modified Duration is the index duration} \;(\text{see} \;\text{get\_treasury\_floating\_rate\_notes})
$$

Coupons are semi-annual and fall on the actual coupon dates, counted back from maturity (on the last day of the month for a note maturing on a month's last day, such as 30 April); the time in the current period is counted in actual days (actual/actual, the Treasury convention). Yields are nominal annual rates compounded twice a year (bond-equivalent), as the Treasury quotes them. For TIPS the price is per 100 of inflation-adjusted principal, so the yield is the real yield (see `get_treasury_inflation_protected_securities` for the index ratio and breakeven). Floating rate notes accrue at the 13-week bill rate plus a spread, which resets every week: their yield is the index rate plus the discount margin, simple interest on actual/360 compounded at each quarterly payment, the rate at which the Treasury's pricing formula gives the price, and their duration that to the index rate, which their coupons follow, so it is close to zero. The Coupon of a floating rate note is the rate it accrues at, as FedInvest lists it.

**See definition:** [https://www.treasurydirect.gov/GA-FI/FedInvest/selectSecurityPriceDate](https://www.treasurydirect.gov/GA-FI/FedInvest/selectSecurityPriceDate){:target="_blank"}

**Also known as:** Treasury bond prices, Treasury yields per security, CUSIP yields, off-the-run Treasuries, FedInvest prices.

**Args:**

- <u>date (str &#124; None, optional):</u> The day (YYYY-MM-DD); a weekend or holiday uses the
business day before it. Defaults to None, the latest day with prices.
- <u>security_type (list[str] &#124; str &#124; None, optional):</u> The kind of security: "Bill",
"Note", "Bond", "TIPS" or "FRN", or several (a list or a comma-separated
string). Defaults to None, which returns every kind.
- <u>bonds (list[str] &#124; str &#124; None, optional):</u> Keeps the securities with these CUSIPs
(or their US ISINs), as a list or a comma-separated string. Defaults to None,
every security.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the rounding of the class.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: One row per security, indexed by CUSIP, with the Security Type,
Coupon (decimal), Maturity, Price per 100 of par, Yield to Maturity (decimal),
Modified Duration (years) and Price Date, sorted by maturity.

**Notes:**

- The price is the end-of-day price. It is published the next business day, so the
latest day uses the bid (FedInvest's Sell price) until then.
- One request per day; a day with end-of-day prices is cached for good.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome()

treasuries = fixedincome.get_treasury_securities(date="2026-11-05", security_type="Note,Bond")

treasuries.loc[treasuries["Maturity"].between("2035-01-01", "2036-12-31")]
```

Which returns:

| CUSIP     | Security Type   |   Coupon | Maturity   |   Price |   Yield to Maturity |   Modified Duration | Price Date   |
|:----------|:----------------|---------:|:-----------|--------:|--------------------:|--------------------:|:-------------|
| 91282CMM0 | Note            |   0.0462 | 2035-02-15 | 99.0312 |              0.0477 |              6.7323 | 2026-11-05   |
| 91282CNC1 | Note            |   0.0425 | 2035-05-15 | 96.3125 |              0.0478 |              6.8997 | 2026-11-05   |
| 91282CNT4 | Note            |   0.0425 | 2035-08-15 | 96.125  |              0.048  |              7.1425 | 2026-11-05   |
| 91282CPJ4 | Note            |   0.04   | 2035-11-15 | 94.1562 |              0.0481 |              7.2897 | 2026-11-05   |
| 912810FT0 | Bond            |   0.045  | 2036-02-15 | 98.875  |              0.0465 |              7.4268 | 2026-11-05   |
| 91282CPZ8 | Note            |   0.0412 | 2036-02-15 | 94.9062 |              0.0481 |              7.5011 | 2026-11-05   |
| 91282CQQ7 | Note            |   0.0438 | 2036-05-15 | 96.625  |              0.0482 |              7.5126 | 2026-11-05   |
| 91282CRF0 | Note            |   0.0462 | 2036-08-15 | 98.4375 |              0.0483 |              7.6914 | 2026-11-05   |

---

## get_fitted_bond_curve
Fits the US Treasury zero-coupon curve to the prices of every Treasury note and bond on a day, from the Treasury's FedInvest prices. Where `get_zero_coupon_curve` bootstraps the dozen constant maturity par yields of the Treasury's own curve, this takes the roughly 330 notes and bonds themselves, so the curve reflects what trades and each bond's residual shows whether it is rich (priced above the curve) or cheap (below it), the relative value view of a bond desk.

The curve minimizes the weighted squared differences between the bonds' prices and their prices on the curve, with weights inversely proportional to duration, as Gürkaynak, Sack and Wright (2007) fit the Federal Reserve's Treasury curve. A price error is about the duration times the price times the yield error, so the weights reduce the weight of the long bonds' larger price errors, while still giving a basis point of a long bond more weight than one of a short bond (equal weight in yield would need $$1 / D^{2}$$).

The formula is as follows:

$$
\min \Sigma_{i} w_{i} (P_{i}^{\text{model}} - P_{i})^{2},\;\; \text{with}\;\; P_{i}^{\text{model}} = \Sigma_{k} \text{CF}_{\text{ik}} d(t_{ik})\;\;\text{and}\;\; w_{i} = \frac{1}{D_{i}}
$$

where $$P_{i}$$ is the clean price plus accrued interest of bond i, $$\text{CF}_{ik}$$ its coupons and principal at times $$t_{ik}$$ (actual days / 365 from the price date, on its actual coupon dates), $$D_{i}$$ its modified duration and d(t) the discount function of the method:

- "svensson": $$d (t) = e^{- y (t) t}$$, with y(t) the Svensson (1994) zero rate $$\beta_{0} + \beta_{1} (1 - e^{- t / \tau_{1}}) / (t / \tau_{1}) + \beta_{2} [(1 - e^{- t / \tau_{1}}) / (t / \tau_{1}) - e^{- t / \tau_{1}}] + \beta_{3} [(1 - e^{- t / \tau_{2}}) / (t / \tau_{2}) - e^{- t / \tau_{2}}]$$, the model of the Federal Reserve's curve (Gürkaynak, Sack and Wright, 2007)
- "nelson_siegel": the same without $$\beta_{3}$$ (Nelson and Siegel, 1987)
- "exponential_spline": $$d (t) = \sum_{k = 1}^{9} a_{k} e^{- k \kappa t}$$ with $$\sum a_{k} = 1$$, the exponential basis of Vasicek and Fong (1982)
- "cubic_spline": d(t) a cubic spline with $$d (0) = 1$$ and about $$\sqrt{n}$$ basis functions for n bonds, with knots at quantiles of the maturities so that as many bonds mature between every two knots (McCulloch, 1975)

The Nelson-Siegel and Svensson fits are a bounded nonlinear least squares from fixed starts (the model fitted to the bonds' yields at their durations, and its betas with first decays of 0.5, 1, 2 and 5 years), with the bounds of `get_nelson_siegel_svensson`; a fit whose parameters are not identified (a flat ridge of equally good fits) raises an error rather than return an arbitrary point on it. The splines are linear in their coefficients and fitted exactly. As Gürkaynak, Sack and Wright do, bills, TIPS, floating rate notes and notes and bonds within three months of maturity are left out. Each day uses its own prices only. For prices of your own, use `fitted_curve_model.fit_bond_curve`.

The fitted zero rates are annually compounded, like those of `get_zero_coupon_curve`, while the models are fitted on continuously compounded rates, so the betas compare with the Federal Reserve's; the instantaneous forward rate is continuously compounded. Yields of the bonds are bond-equivalent (compounded twice a year), as the Treasury quotes them.

For more information, see the following papers:

- McCulloch, J.H. (1975). "The Tax-Adjusted Yield Curve." The Journal of Finance, 30(3), 811-830.
- Vasicek, O.A. and Fong, H.G. (1982). "Term Structure Modeling Using Exponential Splines." The Journal of Finance, 37(2), 339-348.
- Nelson, C.R. and Siegel, A.F. (1987). "Parsimonious Modeling of Yield Curves." The Journal of Business, 60(4), 473-489.
- Svensson, L.E.O. (1994). "Estimating and Interpreting Forward Interest Rates: Sweden 1992-1994." NBER Working Paper 4871.
- Gürkaynak, R.S., Sack, B. and Wright, J.H. (2007). "The U.S. Treasury Yield Curve: 1961 to the Present." Journal of Monetary Economics, 54(8), 2291-2304.

Referenced against QuantLib's FittedBondDiscountCurve with NelsonSiegelFitting, SvenssonFitting, ExponentialSplinesFitting and CubicBSplinesFitting ([https://www.quantlib.org](https://www.quantlib.org){:target="_blank"}).

**Also known as:** fitted yield curve, Treasury curve fitting, rich cheap analysis, bond relative value, Svensson curve on bond prices, spline curve.

**Args:**

- <u>method (str, optional):</u> "svensson", "nelson_siegel", "exponential_spline" or
"cubic_spline". Defaults to "svensson".
- <u>maturities (float &#124; str &#124; list &#124; None, optional):</u> The maturities to return the
curve at, in years or as labels such as '6M' (a list or a comma-separated
string). Defaults to None, 6 months and 1, 2, 3, 5, 7, 10, 20 and 30 years.
- <u>date (str &#124; None, optional):</u> The day of the prices (YYYY-MM-DD); a weekend or
holiday uses the business day before it. Defaults to None, the latest day
with prices.
- <u>residuals (bool, optional):</u> Whether to return every bond with its price and yield
on the curve and its residuals instead of the curve. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results
to. Defaults to None, which uses the rounding of the class.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The Zero Rate (annually compounded), the Discount Factor and the
Instantaneous Forward Rate (continuously compounded) by maturity in years; or,
with residuals=True, per bond (by CUSIP) its Security Type, Coupon, Maturity,
Price, Fitted Price (clean, on the curve), Price Residual (Price minus Fitted
Price, positive for a bond that is rich), Yield to Maturity, Fitted Yield and Yield
Residual (Yield to Maturity minus Fitted Yield, positive for a bond that is cheap).

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome()

fixedincome.get_fitted_bond_curve(date="2026-11-05")
```

Which returns:

|   Maturity |   Zero Rate |   Discount Factor |   Instantaneous Forward Rate |
|-----------:|------------:|------------------:|-----------------------------:|
|        0.5 |      0.0428 |            0.9792 |                       0.0435 |
|        1   |      0.0441 |            0.9577 |                       0.0451 |
|        2   |      0.0455 |            0.9149 |                       0.046  |
|        3   |      0.046  |            0.8738 |                       0.046  |
|        5   |      0.0466 |            0.7964 |                       0.0472 |
|        7   |      0.0475 |            0.7225 |                       0.0504 |
|       10   |      0.0496 |            0.6162 |                       0.0555 |
|       20   |      0.0549 |            0.3432 |                       0.0578 |
|       30   |      0.0546 |            0.2032 |                       0.0461 |

---

## get_treasury_floating_rate_notes
Calculates the discount margin, yield and durations of every US Treasury floating rate note (FRN) from its FedInvest price, with the Treasury's own pricing formula (31 CFR 356, Appendix B, IV).

A Treasury FRN pays, each quarter, the interest accrued day by day at the index rate (the high rate of the latest 13-week bill auction, as a money market yield) plus a fixed spread set at its first auction. Its price is close to par, and how far it is from par is read as the discount margin: the margin over the index rate at which the projected interest and principal are worth the price plus accrued interest. A note trading below par has a discount margin above its spread.

The formula is as follows:

$$
\text{Index Rate} = \frac{d}{1 - \frac{d \cdot t}{360}},\;\; \text{from the high rate } d \text{ of the 13-week bill auction of } t \text{ days (see frn\_model.get\_index\_rate)}
$$

$$
\text{Accrued Interest} = \frac{\Sigma_{j} 100 \cdot \max(r_{j} + s,\; 0)}{360} \;\text{over the days since the last interest payment},\;\; \text{each at the index rate } r_{j} \text{ of its day}
$$

$$
\text{Price} + \text{Accrued Interest} = \frac{\Sigma_{i} A_{i}}{\Pi_{k<=i} \left(1 + \frac{(r + m) \cdot (T_{k} - T_{k-1})}{360}\right)},\;\; \text{with}\;\; A_{i} = \frac{100 \cdot \max(r + s,\; 0)}{360} \cdot (T_{i} - T_{i-1}),\;\; \text{the accrued interest added to the first payment and 100 to the last}
$$

- Discount Margin m: the margin that solves the price equation

$$
\text{Yield} = r + m,\;\; \text{simple interest on actual/360, compounded at each payment}
$$

$$
\text{Index Duration} = \frac{P(r - 0.0001) - P(r + 0.0001)}{2 \cdot P \cdot 0.0001}
$$

$$
\text{Spread Duration} = \frac{P(m - 0.0001) - P(m + 0.0001)}{2 \cdot P \cdot 0.0001}
$$

where s is the spread, r the index rate that applies to the price date (held for every later day), $$T_{i}$$ the quarterly interest payment dates and P the price plus accrued interest. Each day accrues at the index rate of the most recent 13-week bill auction held before it, except that an auction held in the two business days before an issue or interest payment date applies from the day after that date (the lockout, which 31 CFR 356 applies only to those dates, so not to a price date between them). The coupons follow the index, so the index duration is close to zero, while the spread duration, the price change for a change in the discount margin, is about the time to maturity.

The pricing reproduces the Treasury's: the reopening of 91282CRD5 on 25 September 2026 at a discount margin of 0.040% prices at 100.015499 with accrued interest of 0.603670, as announced. Referenced against FinancePy's BondFRN (dirty_price_from_dm, discount_margin and modified_credit_duration), which agree on the same cash flows.

**See definition:** [https://www.ecfr.gov/current/title-31/part-356/appendix-Appendix%20B%20to%20Part%20356](https://www.ecfr.gov/current/title-31/part-356/appendix-Appendix%20B%20to%20Part%20356){:target="_blank"}

**Also known as:** FRN discount margin, floating rate note yield, Treasury FRN spread, spread duration, credit duration, quoted margin.

**Args:**

- <u>date (str &#124; None, optional):</u> The day of the FedInvest prices (YYYY-MM-DD); a weekend
or holiday uses the business day before it. Defaults to None, the latest day
with prices.
- <u>bonds (list[str] &#124; str &#124; None, optional):</u> Keeps the notes with these CUSIPs (or
their US ISINs). Defaults to None, every floating rate note.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the rounding of the class.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: One row per note, indexed by CUSIP, with the Maturity, the clean Price
and Accrued Interest per 100 of par, the Spread, Index Rate, Discount Margin and
Yield (decimals), the Index Duration and Spread Duration (years) and the Price Date.

**Notes:**

- The price date is taken as the settlement date; the market settles a day later.
- The spreads and the 13-week bill rates come from TreasuryDirect's auction data. The
business days of the lockout are weekdays, without the holidays.
- The Treasury pays a minimum daily interest of zero; the formula keeps that floor.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome()

frns = fixedincome.get_treasury_floating_rate_notes(date="2026-11-19")

frns[["Maturity", "Price", "Spread", "Index Rate", "Discount Margin", "Yield", "Spread Duration"]]
```

Which returns:

| CUSIP     | Maturity   |   Price |   Spread |   Index Rate |   Discount Margin |   Yield |   Spread Duration |
|:----------|:-----------|--------:|---------:|-------------:|------------------:|--------:|------------------:|
| 91282CMJ7 | 2027-01-31 | 100.028 |   0.001  |        0.042 |           -0.0005 |  0.0415 |            0.2011 |
| 91282CMX6 | 2027-04-30 | 100.1   |   0.0016 |        0.042 |           -0.0007 |  0.0413 |            0.4431 |
| 91282CNQ0 | 2027-07-31 | 100.133 |   0.0016 |        0.042 |           -0.0004 |  0.0416 |            0.6905 |
| 91282CPG0 | 2027-10-31 | 100.218 |   0.0019 |        0.042 |           -0.0004 |  0.0415 |            0.9352 |
| 91282CPX3 | 2028-01-31 | 100.132 |   0.001  |        0.042 |           -0.0001 |  0.0418 |            1.1776 |
| 91282CQM6 | 2028-04-30 | 100.154 |   0.001  |        0.042 |           -0.0001 |  0.0419 |            1.4119 |
| 91282CRD5 | 2028-07-31 | 100.076 |   0.0005 |        0.042 |            0      |  0.042  |            1.6494 |
| 91282CRS2 | 2028-10-31 | 100.023 |   0.0004 |        0.042 |            0.0003 |  0.0422 |            1.8841 |

---

## get_treasury_inflation_protected_securities
Calculates the index ratio, inflation-adjusted price and breakeven inflation rate of every US Treasury Inflation-Protected Security (TIPS) from its FedInvest price.

TIPS pay a fixed real coupon on a principal that grows with the Consumer Price Index (CPI-U, not seasonally adjusted). They are quoted per 100 of inflation-adjusted principal, a real price whose yield is a real yield; what a buyer pays per 100 of par is that price times the index ratio, the inflation accrued since the security's dated date. The nominal Treasury yield of the same maturity less the real yield is the inflation rate at which the two earn the same: the breakeven inflation rate of the security.

The formula is as follows:

$$
\text{Ref CPI} \;(\text{Date}) = \text{CPI}_{M-3} + \frac{t - 1}{D} \cdot (\text{CPI}_{M-2} - \text{CPI}_{M-3}),\;\; \text{for day } t \text{ of month } M \text{ with } D \text{ days}
$$

$$
\text{Index Ratio} = \frac{\text{Ref CPI} \;(\text{Date})}{\text{Ref CPI}} \;(\text{Dated Date})
$$

$$
\text{Adjusted Price} = \text{Price} \cdot \text{Index Ratio},\;\; \text{and}\;\; \text{Adjusted Accrued Interest} = \text{Accrued Interest} \cdot \text{Index Ratio}
$$

$$
\text{Real Yield:}\;\; \text{the rate } y \text{ at which the real coupons and principal},\;\; \text{discounted at} \;\left(1 + \frac{y}{2}\right) \;\text{per half year},\;\; \text{are worth the price plus accrued interest (see get\_yield\_to\_maturity)}
$$

$$
\text{Breakeven Inflation Rate} = \text{Nominal Yield} - \text{Real Yield}
$$

where the reference CPI and the index ratio are truncated to six decimal places and rounded to five (31 CFR 356, Appendix B, I.B), the reference CPI of the dated date is the one TreasuryDirect publishes with the security, and the Nominal Yield is the Treasury par yield (bond-equivalent, compounded semi-annually) at the security's maturity on the price date, interpolated linearly between the curve's maturities. Yields are compounded semi-annually; the time in the current coupon period is counted in actual days (actual/actual). A month the BLS did not report the CPI for (October 2025) takes the index number the Treasury announced in its place, from the last twelve-month change.

Referenced against QuantLib's CPI interpolation (CPI.laggedFixing, linear, three months' lag) and CPIBond, and FinancePy's InflationBond (inflation_principal and inflation_accrued_interest). The Treasury's own figures are reproduced: the reference CPI of 30 November 2026 is 336.87467, the index ratio of 91282CRE3 on that day 1.00870.

**See definition:** [https://www.treasurydirect.gov/marketable-securities/tips/](https://www.treasurydirect.gov/marketable-securities/tips/){:target="_blank"}

**Also known as:** TIPS index ratio, inflation-adjusted principal, real yield, TIPS breakeven, inflation compensation, reference CPI.

**Args:**

- <u>date (str &#124; None, optional):</u> The day of the FedInvest prices (YYYY-MM-DD); a weekend
or holiday uses the business day before it. Defaults to None, the latest day
with prices.
- <u>bonds (list[str] &#124; str &#124; None, optional):</u> Keeps the TIPS with these CUSIPs (or their
US ISINs). Defaults to None, every TIPS.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the rounding of the class.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: One row per TIPS, indexed by CUSIP, with the Coupon (decimal), Maturity,
the real Price per 100 of inflation-adjusted principal, the Reference CPI, Index
Ratio, Adjusted Price and Adjusted Accrued Interest per 100 of par, the Real Yield,
Nominal Yield and Breakeven Inflation Rate (decimals), the real Modified Duration
(years) and the Price Date.

**Notes:**

- The price date is taken as the settlement date; the market settles a day later.
- At maturity the Treasury repays at least the par amount (the deflation floor); the
real yield leaves that option out, which matters only for a security whose index
ratio is close to or below 1.
- The CPI comes from the BLS's keyless API, which covers about the last three years;
a date before that needs a FRED API key.
- The breakeven rate compares with the par yield curve, not with a nominal note of the
same maturity, and leaves out the inflation risk premium and the liquidity of TIPS.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome()

tips = fixedincome.get_treasury_inflation_protected_securities(date="2026-11-19")

tips[["Maturity", "Index Ratio", "Real Yield", "Nominal Yield", "Breakeven Inflation Rate"]].tail()
```

Which returns:

| CUSIP     | Maturity   |   Index Ratio |   Real Yield |   Nominal Yield |   Breakeven Inflation Rate |
|:----------|:-----------|--------------:|-------------:|----------------:|---------------------------:|
| 912810TE8 | 2052-02-15 |        1.2076 |       0.0327 |          0.0541 |                     0.0214 |
| 912810TP3 | 2053-02-15 |        1.1309 |       0.0329 |          0.0541 |                     0.0212 |
| 912810TY4 | 2054-02-15 |        1.0953 |       0.0329 |          0.0541 |                     0.0212 |
| 912810UH9 | 2055-02-15 |        1.0653 |       0.0328 |          0.0541 |                     0.0213 |
| 912810US5 | 2056-02-15 |        1.0372 |       0.0326 |          0.054  |                     0.0214 |

---

## get_treasury_forward_prices
Calculates the forward price of every US Treasury bill, note and bond: the price for delivery at a later date at which buying the security today with money borrowed in the repo market and selling it forward breaks even (Tuckman and Serrat, 2022, Fixed Income Securities, ch. 13). The difference with today's price is the carry: the coupon income less the cost of financing the position.

The formula is as follows:

$$
\text{Forward Price} = (P + \text{AI}_{0}) \cdot \left(1 + \frac{r \cdot d}{360}\right) - \Sigma_{k} c_{k} \cdot \left(1 + \frac{r \cdot (d - d_{k})}{360}\right) - \text{AI}_{T}
$$

$$
\text{Carry} = \text{Price} - \text{Forward Price}
$$

- Forward Yield: the yield to maturity, compounded semi-annually, at the forward price on the forward date (see `get_yield_to_maturity`; for a bill its bond-equivalent yield)

where P is the clean price, $$\text{AI}_{0}$$ and $$\text{AI}_{T}$$ the accrued interest (actual/actual) on the price date and the forward date, r the repo rate (simple interest, actual/360), d the days to the forward date and $$c_{k}$$ the coupons paid $$d_{k}$$ days from the price date, which earn the repo rate until the forward date. A positive carry (coupon income above the repo cost) makes the forward price lower than the price. The implied repo rate of a quoted forward price inverts this formula (see `bond_futures_model.get_implied_repo_rate`).

Referenced against QuantLib's BondForward (equal without a coupon in between; with one within 0.0001 per 100, as QuantLib discounts the coupon on the repo curve rather than reinvesting it at simple interest) and rateslib's FixedRateBond.fwd_from_repo.

**Also known as:** bond forward price, repo carry, forward drop, cost of carry, forward yield, bond forward.

**Args:**

- <u>forward_date (str &#124; None, optional):</u> The forward (delivery) date (YYYY-MM-DD).
Defaults to None, three months after the price date.
- <u>repo_rate (float &#124; None, optional):</u> The repo rate (decimal, simple interest on
actual/360) to the forward date. Defaults to None, which uses the tri-party
general collateral rate (TGCR) of the price date, the overnight rate of repo
against Treasuries, held for the whole term.
- <u>date (str &#124; None, optional):</u> The day of the FedInvest prices (YYYY-MM-DD); a weekend
or holiday uses the business day before it. Defaults to None, the latest day
with prices.
- <u>security_type (list[str] &#124; str &#124; None, optional):</u> "Bill", "Note" or "Bond", or
several. Defaults to None, all three.
- <u>bonds (list[str] &#124; str &#124; None, optional):</u> Keeps the securities with these CUSIPs
(or their US ISINs). Defaults to None, every security.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the rounding of the class.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: One row per security maturing after the forward date, indexed by
CUSIP, with the Security Type, Coupon (decimal), Maturity, the Price, Forward Price
and Carry per 100 of par, the Forward Yield and Repo Rate (decimals), the Forward
Date and the Price Date.

**Notes:**

- The overnight TGCR stands in for the term repo rate; a security in demand trades
special, at a lower repo rate, which raises its forward price.
- TIPS and floating rate notes are left out: their coupons are not fixed in dollars.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome()

forwards = fixedincome.get_treasury_forward_prices(
    forward_date="2027-02-19", date="2026-11-19", security_type="Note"
)

forwards.loc[
    forwards["Maturity"].between("2036-01-01", "2036-12-31"),
    ["Maturity", "Price", "Forward Price", "Carry", "Forward Yield", "Repo Rate"],
]
```

Which returns:

| CUSIP     | Maturity   |   Price |   Forward Price |   Carry |   Forward Yield |   Repo Rate |
|:----------|:-----------|--------:|----------------:|--------:|----------------:|------------:|
| 91282CPZ8 | 2036-02-15 | 93.3438 |         93.2471 |  0.0967 |          0.0507 |      0.0388 |
| 91282CQQ7 | 2036-05-15 | 95.0312 |         94.8621 |  0.1691 |          0.0508 |      0.0388 |
| 91282CRF0 | 2036-08-15 | 96.8125 |         96.6263 |  0.1862 |          0.0508 |      0.0388 |
| 91282CRX1 | 2036-11-15 | 99.6562 |         99.3742 |  0.282  |          0.0508 |      0.0388 |

---

## get_treasury_futures_basis
Calculates the conversion factor, basis and implied repo rate of every Treasury that can be delivered into a CME US Treasury futures contract, and which of them is the cheapest to deliver.

The seller of a Treasury futures contract delivers a Treasury of its choice from a basket of eligible ones and receives the futures price times that security's conversion factor, plus accrued interest. The factors put securities of different coupons and maturities on one scale, but not exactly, so one of them is the cheapest to deliver: the one whose purchase today, financed in repo and delivered into the futures, earns the most (the highest implied repo rate). The futures price tracks that security (Burghardt and Belton, 2005, The Treasury Bond Basis; Hull, 2022, Options, Futures and Other Derivatives, ch. 6.2).

The formula is as follows:

$$
\text{Conversion Factor} = a \cdot \left(\frac{c}{2} + C + d\right) - \text{b:} \;\text{the price per 1 of par at}\; a 6\% \;\text{yield on the first day of the delivery month},\;\; \text{with}\;\; a = \frac{1}{1.03^{\frac{v}{6}}},\;\; b = \frac{\frac{c}{2} \cdot (6 - v)}{6},\;\; C = \frac{1}{1.03^{2n}(\text{or}\; 1.03^{2n + 1} \;\text{from 7 months})},\;\; d = \frac{c}{0.06} \cdot (1 - C),\;\; n \;\text{and}\; z \;\text{the whole years and months to maturity and}\; v = z \;\text{below 7 months} \;(\text{CME Group},\; \text{"Calculating} \text{U.S.} \;\text{Treasury Futures Conversion}\; \text{Factors"})
$$

$$
\text{Invoice Price} = F \cdot \text{CF} + \text{AI}_{T}
$$

$$
\text{Gross Basis} = P - F \cdot \text{CF}
$$

$$
\text{Carry} = P - \text{Forward Price},\;\; \text{the coupon income less the repo cost to delivery (see get\_treasury\_forward\_prices)}
$$

$$
\text{Net Basis} = \text{Gross Basis} - \text{Carry}
$$

$$
\text{Implied Repo Rate} = \frac{F \cdot \text{CF} + \text{AI}_{T} + \Sigma_{k} c_{k} - (P + \text{AI}_{0})}{\frac{(P + \text{AI}_{0}) \cdot d}{360} - \frac{\Sigma_{k} c_{k} \cdot (d - d_{k})}{360}}
$$

where c is the coupon, P the clean price (FedInvest), F the futures price, $$\text{AI}_{0}$$ and $$\text{AI}_{T}$$ the accrued interest on the price date and the delivery date, d the days to the delivery date and $$c_{k}$$ the coupons paid before it. The months to maturity are rounded down to whole quarters for the 10-year (ZN), Ultra 10-year (TN), bond (ZB) and Ultra bond (UB) contracts and to whole months for the 2-year (ZT) and 5-year (ZF) ones. Rates are simple interest on actual/360. The cheapest to deliver has the highest implied repo rate and the lowest net basis.

The conversion factors equal those of FinancePy's BondFuture and rateslib's BondFuture (CME conventions) and Hull's examples (1.4623 for a 10% coupon with 20 years and 2 months). Referenced against FinancePy's BondFuture and rateslib's BondFuture (gross_basis, net_basis, implied_repo).

**See definition:** [https://www.cmegroup.com/trading/interest-rates/treasury-conversion-factors.html](https://www.cmegroup.com/trading/interest-rates/treasury-conversion-factors.html){:target="_blank"}

**Also known as:** cheapest to deliver, CTD, Treasury basis, implied repo rate, IRR, conversion factor, net basis, gross basis, invoice price, delivery basket.

**Args:**

- <u>contract (str, optional):</u> The futures contract: "ZT" (2-year note), "ZF" (5-year
note), "ZN" (10-year note), "TN" (Ultra 10-year note), "ZB" (bond) or "UB"
(Ultra bond). Defaults to "ZN".
- <u>contract_month (str &#124; None, optional):</u> The delivery month (YYYY-MM), March, June,
September or December. Defaults to None, the first of those months that starts
after the price date.
- <u>repo_rate (float &#124; None, optional):</u> The repo rate (decimal, simple interest on
actual/360) to the delivery date, for the carry and net basis. Defaults to
None, the tri-party general collateral rate (TGCR) of the price date.
- <u>date (str &#124; None, optional):</u> The day of the FedInvest prices (YYYY-MM-DD); a weekend
or holiday uses the business day before it. Defaults to None, the latest day
with prices.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the rounding of the class.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: One row per deliverable, indexed by CUSIP and sorted from the highest
implied repo rate, with the Coupon (decimal), Maturity, Price, Conversion Factor,
Futures Price, Invoice Price, Gross Basis, Carry and Net Basis (per 100 of par),
the Implied Repo Rate and Repo Rate (decimals), whether it is the Cheapest to
Deliver, the Futures Symbol, Delivery Date and Price Date.

**Notes:**

- The basket follows CME's contract rules, applied to the FedInvest securities: ZT
(original term up to 5 years 3 months, from 1 year 9 months remaining on the first
day of the delivery month to 2 years on its last day), ZF (original term up to 5
years 3 months, at least 4 years 2 months remaining), ZN (notes with 6 years 6 months
to 8 years remaining), TN (original 10-year notes with 9 years 5 months to 10 years),
ZB (bonds with 15 to 25 years) and UB (bonds with 25 years or more). The original
terms come from TreasuryDirect's auction data. CME publishes the basket itself; a
security issued after the price date is not in it here.
- The futures price is the settlement price of the contract month from Yahoo Finance
(such as ZNZ26.CBT) on the price date, or the last day before it. FedInvest prices
are not taken at the time of the futures settlement, so on a day the market moves a
lot the basis carries part of that move. Before its end-of-day prices are published
(the next business day) the latest day uses the bid.
- Delivery is taken on the last delivery day: the last business day of the delivery
month for ZN, TN, ZB and UB, the third business day of the next month for ZT and
ZF. The short's options on what and when to deliver are left out, so the net basis
of the cheapest to deliver is the value the market puts on them. Business days are
weekdays, without the holidays.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome()

basis = fixedincome.get_treasury_futures_basis(contract="ZN", contract_month="2026-12", date="2026-11-19")

basis[["Maturity", "Price", "Conversion Factor", "Gross Basis", "Net Basis", "Implied Repo Rate"]]
```

Which returns:

| CUSIP     | Maturity   |    Price |   Conversion Factor |   Gross Basis |   Net Basis |   Implied Repo Rate |
|:----------|:-----------|---------:|--------------------:|--------------:|------------:|--------------------:|
| 91282CRJ2 | 2033-08-31 |  97.5    |              0.9202 |        0.0738 |     -0.0024 |              0.039  |
| 91282CHT1 | 2033-08-15 |  93.9688 |              0.887  |        0.0576 |      0.0453 |              0.0347 |
| 91282CRC7 | 2033-07-31 |  96.8438 |              0.9136 |        0.1163 |      0.0614 |              0.0334 |
| 91282CRM5 | 2033-09-30 | 100.344  |              0.9451 |        0.2813 |      0.1617 |              0.0251 |
| 91282CQW4 | 2033-06-30 |  96.2188 |              0.9069 |        0.2007 |      0.1586 |              0.0249 |
| 91282CJJ1 | 2033-11-15 |  97.4062 |              0.9177 |        0.2448 |      0.1638 |              0.0244 |
| 91282CRV5 | 2033-10-31 |  99.625  |              0.9382 |        0.2931 |      0.1796 |              0.0234 |
| 91282CJZ5 | 2034-02-15 |  94.25   |              0.887  |        0.3389 |      0.3137 |              0.0106 |
| 91282CKQ3 | 2034-05-15 |  96.375  |              0.9055 |        0.5052 |      0.4341 |              0.0002 |
| 91282CLF6 | 2034-08-15 |  93      |              0.8732 |        0.5499 |      0.5333 |             -0.0098 |
| 91282CLW9 | 2034-11-15 |  95.1875 |              0.8927 |        0.6729 |      0.6109 |             -0.0162 |

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
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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

The rates change on the dates the Governing Council's decisions take effect. Weekly, monthly, quarterly and yearly data hold the rate in force on the last day of each period, so the current period shows the rate so far.

See source: [https://data.ecb.europa.eu/main-figures/](https://data.ecb.europa.eu/main-figures/){:target="_blank"}

**Also known as:** ECB rates, deposit facility rate.

**Args:**

- <u>rate (str, optional):</u> The rate to return. Defaults to None, which returns all rates.
Choose between 'refinancing', 'lending' or 'deposit'.
- <u>period (str, optional):</u> Whether to return the daily, weekly, monthly, quarterly or
yearly data. Defaults to 'daily'.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>standardize (bool, optional):</u> Whether to standardize (Z-Score) the result. Defaults to False.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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

## get_short_rate_model
Calibrates the Vasicek and Cox-Ingersoll-Ross (CIR) short-rate models to the history of a country's short-term government bond yield and compares the zero-coupon curve each model implies with today's. Short-rate models describe how the interest rate moves, pulled back to a long-run mean b at a speed a with a volatility $$\sigma$$:

$$
\text{Vasicek (1977):}\;\; \,\mathrm{d}r = a (b - r) \,\mathrm{d}t + \sigma \,\mathrm{d}W
$$

$$
\text{CIR (1985):}\;\; \,\mathrm{d}r = a (b - r) \,\mathrm{d}t + \sigma \sqrt{r} \,\mathrm{d}W
$$

In CIR the volatility shrinks as the rate approaches zero, so the rate stays positive when $$2 ab \geq \sigma^{2}$$ (the Feller condition, Feller 1951, reported as the Feller Ratio $$2 ab / \sigma^{2}$$, which meets it at 1 or more) and can otherwise touch zero; in Vasicek it can turn negative. The models describe a continuously compounded short rate, so the yields are converted to continuous compounding first (US bill yields from their bond-equivalent quote). Both give bond prices, and so a full zero-coupon curve, in closed form. The parameters are estimated by regressing the change of the rate on its level over the period (CIR on the changes scaled by the square root of the rate, which needs a rate above zero throughout). The half-life is the time it takes to close half the gap to the long-run mean, ln(2) / a.

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
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per model (columns Vasicek and CIR) the Speed of Mean Reversion, the
Long-Run Mean, the Volatility, the Current Rate, the Half-Life in years and (CIR
only) the Feller Ratio, then the zero-coupon rate per maturity (continuously compounded), with the market's
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
| Feller Ratio            |  nan      | 1.6148 | nan      |
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

The speed of mean reversion and the volatility are calibrated to the history of the rate, see `get_short_rate_model`. In the Vasicek and CIR models the rate is pulled to the long-run mean of that history. The Hull-White (1990) model replaces it with a mean that varies over time and follows from today's zero-coupon curve, so that the model reproduces the discount factors of that curve (its expected short rate lies above the forward rate by the convexity term $$\sigma^{2} (1 - e^{- at})^{2} / (2 a^{2})$$):

$$
dr = [\theta (t) - a r] dt + \sigma dW,\quad \theta (t) = \partial f / \partial t + a f (t) + \sigma^{2} (1 - e^{- 2 at}) / (2 a)
$$

with f the instantaneous forward rate. The paths start at today's rate and are simulated with an Euler scheme (CIR's are kept at or above zero) or, with scheme="exact", by drawing the rate at the end of every step from its exact distribution given the rate at the start: normal for Vasicek and Hull-White ($$r' = r e^{- a \Delta} + m (1 - e^{- a \Delta}) + \sigma \sqrt{(1 - e^{- 2 a \Delta}) / (2 a)} Z$$, with m the mean of the step) and a scaled non-central chi-squared for CIR (Glasserman, 2003, Monte Carlo Methods in Financial Engineering, sections 3.3 and 3.4). The exact scheme has no discretization error at any step size, and its CIR rate stays at or above zero without being cut off, which matters most when the Feller ratio of `get_short_rate_model` is below 1.

The simulated short rates are continuously compounded, the rate these models describe: the quoted yield of the short_rate maturity is converted from its quote convention (for US bills the bond-equivalent yield) and the zero-coupon curve of the Hull-White mean from annual compounding.

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
- <u>scheme (str, optional):</u> "euler" or "exact". Defaults to "euler".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

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

## get_swaption_price
Calculates the prices of European or Bermudan swaptions, the right to enter an interest rate swap at the option's expiry, for a grid of expiries and swap tenors in a one-factor short-rate model fitted to today's government zero-coupon curve. A payer swaption is the right to pay the fixed rate (it gains when rates rise), a receiver swaption the right to receive it. Without a strike every swaption is at the money: struck at the forward swap rate of its expiry and tenor on the same curve (`get_swap_rate` with curve="government" and forward_start the expiry).

Two models reproduce the curve and so price at-the-money swaptions consistently:

$$
\text{Hull-White (1990):}\;\; \,\mathrm{d}r = \left[\theta(t) - a r\right] \,\mathrm{d}t + \sigma \,\mathrm{d}W,\;\; \text{Vasicek with a time-varying mean, so rates are normal and can turn negative}
$$

$$
\text{CIR++ (Brigo and Mercurio, 2001):}\;\; r = x + \phi(t),\;\; \text{with}\;\; x \;\text{a Cox-Ingersoll-Ross process}\; \,\mathrm{d}x = a (b - x) \,\mathrm{d}t + \sigma \sqrt{x} \,\mathrm{d}W \;\text{and}\; \phi \;\text{the deterministic shift that fits the curve},\;\; \text{so the volatility grows with the level of rates}
$$

The speed of mean reversion a and the volatility $$\sigma$$ (and for CIR++ the long-run mean b) are calibrated to the history of the short_rate yield between the start and end date, see `get_short_rate_model`; CIR++ starts its process at today's short rate. The price follows from Jamshidian's (1989) decomposition: at expiry the payer swaption is a put on a coupon bond paying the fixed rate, which in a one-factor model splits into puts on its zero-coupon bonds, each priced in closed form (see `short_rate_model.get_swaption` and `get_zero_coupon_bond_option`).

A Bermudan swaption (exercise="bermudan", Hull-White only) can also be exercised on every fixed payment date after the expiry, into the rest of a swap that ends at the expiry plus the tenor (co-terminal, "10 non-call 1"). It has no closed form and is valued on a Hull-White trinomial tree fitted exactly to the zero curve with the two-stage procedure of Hull and White (1994), with at most 1/50 of a year between two dates of the tree, comparing at every exercise date the value of the swap with the value of waiting (see `trinomial_tree_model.get_bermudan_swaption`). It is worth at least the European swaption of the same expiry, tenor and strike.

The formula is as follows:

$$
c_{i} = K \tau_{i},\;\; \text{plus 1 on the last date } T_{n}
$$

$$
x^{*} \;\text{solves} \;\sum(c_{i} P(T,\; T_{i} ; x^{*})) = 1,\;\; X_{i} = P(T,\; T_{i} ; x^{*})
$$

$$
\text{Payer Swaption} = \sum(c_{i} \;\text{ZBP}(T,\; T_{i},\; X_{i}))
$$

$$
\text{Receiver Swaption} = \sum(c_{i} \;\text{ZBC}(T,\; T_{i},\; X_{i}))
$$

$$
\text{Bermudan:}\;\; \text{Option} = \max(E\left[\text{Option next date}\right] \cdot e^{- r \Delta t},\; \pm (1 - B(T_{k}))) \;\text{at}\; T_{0} = T,\;\; T_{1} \text{, } \ldots , T_{n - 1},\;\; \text{with} \;B(T_{k}) \;\text{the coupon bond's payments after}\; T_{k} \;\text{on the tree} \;(+ \text{for a payer},\; - \text{for a receiver})
$$

with T the expiry, $$T_{i}$$ the fixed payment dates every 1 / fixed_frequency years after it, $$\tau_{i} = 1$$ / fixed_frequency, K the strike, P(T, T_i; x) the bond price at expiry in state x of the model and ZBP and ZBC the zero-coupon bond puts and calls of the model. The price is per 1 of notional (0.01 is 1% of the notional).

The short rate and the model parameters are continuously compounded (the yield is converted from its quote convention, as in `get_short_rate_model`). The zero-coupon curve is that of the end date, bootstrapped from the par yields and annually compounded, and the strike is a nominal annual rate paid fixed_frequency times a year, with no day count. The calibration uses the history up to the end date only.

For more information, see the following sources:

- Jamshidian, F. (1989). "An Exact Bond Option Formula." Journal of Finance, 44(1), 205-209.
- Hull, J. and White, A. (1990). "Pricing Interest-Rate-Derivative Securities." The Review of Financial Studies, 3(4), 573-592.
- Brigo, D. and Mercurio, F. (2001). "A Deterministic-Shift Extension of Analytically Tractable and Time-Homogeneous Short-Rate Models." Finance and Stochastics, 5(3), 369-387.
- Hull, J. and White, A. (1994). "Numerical Procedures for Implementing Term Structure Models I: Single-Factor Models." Journal of Derivatives, 2(1), 7-16.

Referenced against QuantLib's `JamshidianSwaptionEngine` with `HullWhite` and `ExtendedCoxIngersollRoss`, and for Bermudan swaptions its `TreeSwaptionEngine` with `HullWhite`.

**Also known as:** swaption price, Bermudan swaption, Hull-White swaption, CIR++ swaption, Jamshidian decomposition, interest rate option.

**Args:**

- <u>expiries (float &#124; str &#124; list &#124; None, optional):</u> The expiries of the swaptions, in
years or as labels such as '6M'. Defaults to None, 1, 2, 5 and 10 years.
- <u>tenors (float &#124; str &#124; list &#124; None, optional):</u> The tenors of the underlying swaps,
in years or as labels such as '10Y'. Defaults to None, 1, 2, 5, 10 and 30
years.
- <u>model (str, optional):</u> "hull_white" or "cir++". Defaults to "hull_white".
- <u>swaption_type (str, optional):</u> "payer" or "receiver". Defaults to "payer".
- <u>strike (float &#124; None, optional):</u> The fixed rate of the swaps (decimal). Defaults
to None, the at-the-money forward swap rate of each expiry and tenor.
- <u>fixed_frequency (int, optional):</u> The fixed payments per year. Defaults to 1.
- <u>country (str, optional):</u> The country, see `get_government_bond_yield_curve`.
Defaults to "United States".
- <u>short_rate (str, optional):</u> The maturity of the yield used as the short rate,
such as "1M", "3M" or "6M". Defaults to "3M".
- <u>period (str, optional):</u> Whether to calibrate on daily, weekly or monthly rates.
Defaults to "daily".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.
- <u>exercise (str, optional):</u> "european" (at the expiry only) or "bermudan" (on every
fixed payment date from the expiry on, Hull-White only). Defaults to
"european".

**Returns:**

pd.DataFrame: The swaption price per 1 of notional, by expiry in years (rows) and
tenor in years (columns).

**Notes:**

- One factor moves the whole curve, so the model ties the volatilities of all
expiries and tenors to two parameters; fitted to the history of a short rate it
does not match the volatilities that swaption markets quote.
- CIR++ needs a rate above zero throughout the calibration period (see
`get_short_rate_model`), and the Feller Ratio there shows whether its process stays
away from zero.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome(start_date='2000-01-01', end_date='2026-10-23')

fixedincome.get_swaption_price(short_rate='6M')
```

Which returns:

|   Expiry |      1 |      2 |      5 |     10 |     30 |
|---------:|-------:|-------:|-------:|-------:|-------:|
|        1 | 0.0021 | 0.0039 | 0.008  | 0.012  | 0.0154 |
|        2 | 0.0027 | 0.005  | 0.0103 | 0.0154 | 0.0198 |
|        5 | 0.0032 | 0.0061 | 0.0125 | 0.0185 | 0.024  |
|       10 | 0.003  | 0.0055 | 0.0114 | 0.0167 | 0.0221 |

---

## get_swap_rate
Calculates the par swap rates and annuities of interest rate swaps of any maturity on a single curve: the fixed rate at which a new fixed-for-floating swap is worth nothing, and the present value of receiving 1 a year on its fixed leg. With a forward start, these are the forward swap rates and annuities that price a swaption.

On a single curve, which both projects the floating rate and discounts, a floating leg that resets at the start of each period is worth par at its start, so the swap rate follows from the discount factors alone (Hull, 2022, Options, Futures and Other Derivatives, ch. 7; Andersen and Piterbarg, 2010, Interest Rate Modeling, ch. 5).

The formula is as follows:

$$
\text{Annuity} = \sum(\tau_{i} \cdot P(t_{i})),\;\; \text{over the fixed payment dates } t_{1} \text{, } \ldots , t_{n}
$$

$$
\text{Swap Rate} = \frac{P(t_{0}) - P(t_{n})}{\text{Annuity}}
$$

where P(t) = (1 + r(t))^(-t) is the discount factor of the annually compounded zero rate r(t) of the curve (interpolated linearly between its maturities), $$t_{0}$$ the start of the swap and $$\tau_{i} = 1$$ / fixed_frequency the accrual of a fixed period (a short first period when the maturity is not a whole number of periods). The swap rate is a nominal annual rate paid fixed_frequency times a year on year fractions with no calendar (a regular 30/360 schedule). The value of a basis point on the fixed rate (PV01) of a swap is Annuity * Notional * 0.0001.

The default curve is EIOPA's risk-free rate term structure, which EIOPA derives from the swap rates of each currency (for the euro, swap rates minus a credit risk adjustment) and publishes at each month end; curve="government" uses the zero-coupon curve of the government bond yield curve of the day instead, whose par rates are those of government bonds rather than swaps. To value a swap of your own, with a fixed rate, a current fixing and its DV01, use `swap_model.get_swap_value`.

Referenced against QuantLib's VanillaSwap with the DiscountingSwapEngine, FinancePy's IborSwap and rateslib's IRS on the same discount factors.

**Also known as:** par swap rate, swap curve, interest rate swap rate, forward swap rate, PV01, swap annuity, PVBP.

**Args:**

- <u>maturities (float &#124; str &#124; list &#124; None, optional):</u> The maturities (tenors) of the
swaps, in years or as labels such as '10Y'. Defaults to None, 1, 2, 3, 5, 7, 10,
15, 20 and 30 years.
- <u>country (str, optional):</u> The country or currency area of the curve, as EIOPA
(curve="eiopa") or `get_government_bond_yield_curve` (curve="government") names
it. Defaults to "United States".
- <u>curve (str, optional):</u> "eiopa" for the EIOPA risk-free rate term structure of the
last month end on or before the date, or "government" for the zero-coupon curve
of the government bond yield curve of the date (see `get_zero_coupon_curve`).
Defaults to "eiopa".
- <u>fixed_frequency (int, optional):</u> The number of fixed payments per year. Defaults to
1 (annual, as euro and US dollar overnight index swaps pay).
- <u>forward_start (float &#124; str, optional):</u> The start of the swaps, in years or as a
label such as '1Y', for forward starting swaps. Defaults to 0, swaps that start
today.
- <u>date (str &#124; None, optional):</u> The day of the curve (YYYY-MM-DD). Defaults to None,
the end date.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results
to. Defaults to None, which uses the rounding of the class.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The Swap Rate (decimal, compounded fixed_frequency times a year) and
the Annuity (years, per unit of notional) by maturity in years.

**Notes:**

- EIOPA's curves start at 1 year, so a shorter maturity discounts at the 1-year zero
rate; beyond the last liquid point (20 years for the euro, 50 for the US dollar)
they converge to the ultimate forward rate, a regulatory assumption rather than a
market price.
- A single curve leaves out the basis between the overnight and the term rates
(SOFR against term SOFR, €STR against Euribor), so these are the rates of swaps on
the curve's own rate.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome(start_date='2026-10-01', end_date='2026-11-20')

fixedincome.get_swap_rate(maturities=[1, 2, 5, 10, 30], country='Euro Area')
```

Which returns:

|   Maturity |   Swap Rate |   Annuity |
|-----------:|------------:|----------:|
|          1 |      0.0314 |    0.9696 |
|          2 |      0.0327 |    1.9072 |
|          5 |      0.0329 |    4.5437 |
|         10 |      0.0334 |    8.3984 |
|         30 |      0.0332 |   18.7673 |

---

## get_forward_rate_agreement
Calculates the rates of forward rate agreements (FRAs) from a zero-coupon curve: the simple interest rate, fixed today, of a loan that starts and ends at future dates. A "3x6" FRA covers the three months that start three months from now.

At no arbitrage the FRA rate is the simple forward rate implied by the discount factors of the two dates (Hull, 2022, Options, Futures and Other Derivatives, ch. 4.7). A FRA that pays a fixed rate K and receives the floating rate is worth Notional * $$\tau$$ * (FRA Rate - K) * P(end), see `forward_model.get_forward_rate_agreement`.

The formula is as follows:

$$
\tau = \frac{(\text{End} - \text{Start}) \cdot 365}{\text{Days in Year}}
$$

$$
\text{FRA Rate} = \frac{\frac{P(\text{Start})}{P(\text{End})} - 1}{\tau}
$$

where P(t) = (1 + r(t))^(-t) is the discount factor of the annually compounded zero rate r(t) of the curve, interpolated linearly between its maturities, the times are years (a month is a twelfth of a year) and Days in Year is 360 on ACT/360, the money market day count of US dollar and euro rates, or 365 on ACT/365. The FRA rate is simple interest on that day count.

The default curve is the zero-coupon curve of the government bond yield curve of the day (see `get_zero_coupon_curve`), whose bills price the first months; curve="eiopa" uses EIOPA's swap-based risk-free rate term structure of the last month end, which starts at 1 year.

Referenced against QuantLib's ForwardRateAgreement, FinancePy's IborFRA and rateslib's FRA on the same discount factors.

**Also known as:** FRA, forward rate agreement, forward-forward rate, simple forward rate.

**Args:**

- <u>fras (str &#124; list[str] &#124; None, optional):</u> The FRAs as "start x end" in months, as a
list or comma-separated, e.g. "3x6,6x12". Defaults to None, 1x4, 3x6, 6x9, 6x12,
9x12, 12x18 and 12x24.
- <u>country (str, optional):</u> The country or currency area of the curve, see
`get_government_bond_yield_curve` (or EIOPA's names with curve="eiopa").
Defaults to "United States".
- <u>curve (str, optional):</u> "government" for the zero-coupon curve of the government
bond yield curve of the date, or "eiopa" for EIOPA's risk-free rate term
structure of the last month end on or before it. Defaults to "government".
- <u>day_count (str, optional):</u> The day count of the FRA rate, "act/360" or "act/365".
Defaults to "act/360".
- <u>date (str &#124; None, optional):</u> The day of the curve (YYYY-MM-DD). Defaults to None,
the end date.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results
to. Defaults to None, which uses the rounding of the class.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per FRA the Start and End (years) and the FRA Rate (decimal, simple
interest on the day count).

**Notes:**

- Government bill and bond yields sit below the interbank and overnight rates FRAs
are settled on (the swap spread), so on the government curve these are risk-free
forward rates rather than market FRA quotes.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome(start_date='2026-11-01', end_date='2026-11-20')

fixedincome.get_forward_rate_agreement()
```

Which returns:

| FRA   |   Start |    End |   FRA Rate |
|:------|--------:|-------:|-----------:|
| 1x4   |  0.0833 | 0.3333 |     0.0429 |
| 3x6   |  0.25   | 0.5    |     0.0433 |
| 6x9   |  0.5    | 0.75   |     0.0449 |
| 6x12  |  0.5    | 1      |     0.0458 |
| 9x12  |  0.75   | 1      |     0.0461 |
| 12x18 |  1      | 1.5    |     0.0463 |
| 12x24 |  1      | 2      |     0.0475 |

---

## get_asset_swap_spread
Calculates the par and the market value asset swap spreads of US dollar corporate bonds over the swap curve: the spread over the floating rate at which a swap that pays away the bond's coupons turns the bond into a floating rate asset worth what the investor pays. It measures a bond's credit and liquidity against swaps rather than against government bonds, as banks that fund at floating rates see it (O'Kane, 2000, "Introduction to Asset Swaps", Lehman Brothers; Tuckman and Serrat, 2022, Fixed Income Securities, ch. 18).

In a par asset swap the investor pays par for the bond and the swap together, and the swap settles the difference between par and the bond's price; in a market value asset swap the investor pays the bond's price and the floating leg runs on that amount.

The formula is as follows:

$$
\text{Curve Price} = 100 \cdot \left(\sum\left(\frac{c}{2} \cdot P(t_{i})\right) + P(t_{n})\right),\;\; \text{the dirty price of the bond on the swap curve}
$$

$$
\text{Annuity} = \sum(\delta_{j} \cdot P(s_{j})),\;\; \text{over the floating payment dates } s_{j}
$$

$$
\text{Par Asset Swap Spread} = \frac{\text{Curve Price} - \text{Dirty Price}}{100 \cdot \text{Annuity}}
$$

$$
\text{Market Value Asset Swap Spread} = \frac{\text{Curve Price} - \text{Dirty Price}}{\text{Dirty Price} \cdot \text{Annuity}}
$$

where P(t) = (1 + r(t))^(-t) is the discount factor of the annually compounded US dollar zero rate r(t) of the curve on the bond's Price Date, c the coupon rate, $$t_{i}$$ the semi-annual coupon dates counted back from maturity in years on the 30/360 Bond Basis (as `get_bond_universe` prices the bonds), Dirty Price = Price + Accrued Interest per 100 of par, and $$\delta_{j} = 1$$ / float_frequency the accrual of the floating periods from the Price Date to maturity (a short first period). The spreads are simple annual rates on the floating leg.

The default curve is EIOPA's US dollar risk-free rate term structure, which EIOPA derives from US dollar swap rates, of the last month end on or before each bond's Price Date; curve="government" uses the Treasury zero-coupon curve of the Price Date instead, which gives the asset swap spread over Treasuries. For a bond and curve of your own, use `swap_model.get_asset_swap_spread`.

Referenced against QuantLib's AssetSwap (fairSpread, par and market value) on the same discount factors.

**Also known as:** ASW, asset swap spread, par-par asset swap, proceeds asset swap, market value asset swap.

**Args:**

- <u>issuer (list[str] &#124; str &#124; None, optional):</u> Keeps the bonds whose issuer contains this
text (case-insensitive), e.g. "APPLE", or any of several. Defaults to None,
every issuer.
- <u>bonds (list[str] &#124; str &#124; None, optional):</u> Keeps the bonds with these ISINs or
CUSIPs, as a list or a comma-separated string. Defaults to None, every bond.
- <u>maturity_start (str &#124; None, optional):</u> Keeps the bonds maturing on or after this
date (YYYY-MM-DD). Defaults to None.
- <u>maturity_end (str &#124; None, optional):</u> Keeps the bonds maturing on or before this
date (YYYY-MM-DD). Defaults to None.
- <u>etfs (list[str] &#124; str &#124; None, optional):</u> The bond ETFs to read the bonds from (see
`get_bond_universe`). Defaults to None, LQD, IGSB and USHY.
- <u>curve (str, optional):</u> "eiopa" for EIOPA's US dollar risk-free rate term structure,
or "government" for the Treasury zero-coupon curve. Defaults to "eiopa".
- <u>float_frequency (int, optional):</u> The number of floating payments per year of the
swap. Defaults to 4 (quarterly).
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the rounding of the class.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: One row per bond, indexed by ISIN, with the Issuer, Coupon (decimal),
Maturity, Price (clean, per 100 of par), the Par Asset Swap Spread and Market Value
Asset Swap Spread (decimals) and the Price Date.

**Notes:**

- EIOPA publishes its curve at each month end, so the curve can be up to a month and
a half older than the bond prices; curve="government" uses the curve of the same day.
- The bonds and their prices are those of `get_bond_universe`; a callable bond is
treated as a bullet bond to maturity.
- Requires a FinancialModelingPrep API key for the holdings.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome(end_date='2026-11-20', api_key="FINANCIAL_MODELING_PREP_KEY")

spreads = fixedincome.get_asset_swap_spread(issuer="APPLE INC")

spreads[["Coupon", "Maturity", "Price", "Par Asset Swap Spread", "Market Value Asset Swap Spread"]].head()
```

Which returns:

| ISIN         |   Coupon | Maturity   |   Price |   Par Asset Swap Spread |   Market Value Asset Swap Spread |
|:-------------|---------:|:-----------|--------:|------------------------:|---------------------------------:|
| US037833EC07 |   0.012  | 2028-02-08 |   95.85 |                  0.0039 |                           0.0041 |
| US037833ET32 |   0.04   | 2028-05-10 |   98.9  |                  0.0042 |                           0.0042 |
| US037833EY27 |   0.04   | 2028-05-12 |   98.87 |                  0.0043 |                           0.0044 |
| US037833EH93 |   0.014  | 2028-08-05 |   94.55 |                  0.0036 |                           0.0038 |
| US037833FD70 |   0.0465 | 2028-11-09 |   99.74 |                  0.0039 |                           0.0039 |

---

## get_i_spread
Calculates the I-spread (interpolated spread) of US dollar corporate bonds: the yield to maturity over the par swap rate of the bond's maturity. The I-spread compares a bond with the swap curve the way the G-spread compares it with Treasuries (Tuckman and Serrat, 2022, Fixed Income Securities, ch. 18); the difference between the two is the swap spread at the bond's maturity.

The formula is as follows:

$$
\text{I-Spread} = \text{Yield to Maturity} - \text{Swap Rate}(T)
$$

where the Yield to Maturity is that of `get_bond_universe` (a nominal annual rate compounded twice a year) and Swap Rate(T) the par swap rate of `get_swap_rate` for the bond's years to maturity T on the 30/360 Bond Basis, with semi-annual fixed payments so that both rates are compounded alike (a short first period when T is not a whole number of half years). The swap rate is priced on the annually compounded US dollar zero curve of the bond's Price Date.

The default curve is EIOPA's US dollar risk-free rate term structure, which EIOPA derives from US dollar swap rates, of the last month end on or before each bond's Price Date; curve="government" uses the Treasury zero-coupon curve, which makes the I-spread a spread over the Treasury par curve, close to the G-Spread. For a bond and curve of your own, use `swap_model.get_i_spread`.

**Also known as:** interpolated spread, I-spread, spread over swaps, swap spread of a bond.

**Args:**

- <u>issuer (list[str] &#124; str &#124; None, optional):</u> Keeps the bonds whose issuer contains this
text (case-insensitive), e.g. "APPLE", or any of several. Defaults to None,
every issuer.
- <u>bonds (list[str] &#124; str &#124; None, optional):</u> Keeps the bonds with these ISINs or
CUSIPs, as a list or a comma-separated string. Defaults to None, every bond.
- <u>maturity_start (str &#124; None, optional):</u> Keeps the bonds maturing on or after this
date (YYYY-MM-DD). Defaults to None.
- <u>maturity_end (str &#124; None, optional):</u> Keeps the bonds maturing on or before this
date (YYYY-MM-DD). Defaults to None.
- <u>etfs (list[str] &#124; str &#124; None, optional):</u> The bond ETFs to read the bonds from (see
`get_bond_universe`). Defaults to None, LQD, IGSB and USHY.
- <u>curve (str, optional):</u> "eiopa" for EIOPA's US dollar risk-free rate term structure,
or "government" for the Treasury zero-coupon curve. Defaults to "eiopa".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the rounding of the class.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: One row per bond, indexed by ISIN, with the Issuer, Coupon (decimal),
Maturity, the Yield to Maturity, Swap Rate, I-Spread and G-Spread (decimals) and
the Price Date.

**Notes:**

- EIOPA publishes its curve at each month end, so the curve can be up to a month and
a half older than the bond prices; curve="government" uses the curve of the same day.
- The yield is to maturity: a callable bond priced above its call price yields less
to its call date.
- Requires a FinancialModelingPrep API key for the holdings.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome(end_date='2026-11-20', api_key="FINANCIAL_MODELING_PREP_KEY")

spreads = fixedincome.get_i_spread(issuer="APPLE INC")

spreads[["Coupon", "Maturity", "Yield to Maturity", "Swap Rate", "I-Spread", "G-Spread"]].head()
```

Which returns:

| ISIN         |   Coupon | Maturity   |   Yield to Maturity |   Swap Rate |   I-Spread |   G-Spread |
|:-------------|---------:|:-----------|--------------------:|------------:|-----------:|-----------:|
| US037833EC07 |   0.012  | 2028-02-08 |              0.0475 |      0.0434 |     0.0041 |     0.0021 |
| US037833ET32 |   0.04   | 2028-05-10 |              0.0478 |      0.0436 |     0.0042 |     0.0022 |
| US037833EY27 |   0.04   | 2028-05-12 |              0.048  |      0.0436 |     0.0044 |     0.0023 |
| US037833EH93 |   0.014  | 2028-08-05 |              0.0476 |      0.0437 |     0.0038 |     0.0016 |
| US037833FD70 |   0.0465 | 2028-11-09 |              0.0479 |      0.044  |     0.0039 |     0.0016 |

---

## get_fx_forward_rates
Calculates FX forward rates by covered interest parity: the exchange rate, agreed today, at which currencies are exchanged at a future date. Exchanging today and depositing abroad, or depositing at home and exchanging forward, must give the same, so the forward rate is the spot rate carried at the difference between the two currencies' interest rates: the currency with the higher rate trades at a forward discount (Hull, 2022, Options, Futures and Other Derivatives, ch. 5.10).

The formula is as follows:

$$
\text{Forward Rate} = \text{Spot Rate} \cdot \left(\frac{1 + r_{\text{country}}(T)}{1 + r_{\text{base}}(T)}\right)^{T}
$$

$$
\text{Forward Points} = (\text{Forward Rate} - \text{Spot Rate}) \cdot \text{10,000}
$$

where the Spot Rate is in units of the country's currency per unit of the base country's currency, from the daily exchange rates against the US dollar the Bank for International Settlements compiles (the last day with a rate on or before the date), and r_country(T) and $$r_{\text{base}} (T)$$ are the annually compounded zero rates of the two currencies at the tenor T in years (a month is a twelfth of a year). The value of a forward you hold follows from `forward_model.get_fx_forward_rate`.

The default curves are EIOPA's risk-free rate term structures, which EIOPA derives from the swap rates of each currency and publishes at each month end for the euro and about 20 other currencies; they start at 1 year, so a shorter tenor uses the 1-year zero rate. curve="government" uses the zero-coupon curves of the government bond yield curves of the date, whose bills price the first months, for the countries that have one (see `get_zero_coupon_curve`).

Referenced against QuantLib's FxForward, FinancePy's FXForward and rateslib's forward_fx on the same discount factors.

**Also known as:** FX forward, currency forward, forward exchange rate, forward points, swap points, covered interest parity, outright forward.

**Args:**

- <u>countries (list[str] &#124; str &#124; None, optional):</u> The countries or currency areas whose
currency is quoted, as EIOPA and the BIS name them (e.g. "Euro Area", "Japan").
Defaults to None, the Euro Area, the United Kingdom, Japan, Switzerland, Canada
and Australia.
- <u>base_country (str, optional):</u> The country of the base currency, one unit of which
the rates are quoted against. Defaults to "United States".
- <u>tenors (float &#124; str &#124; list &#124; None, optional):</u> The tenors, in years or as labels such
as '3M' or '5Y'. Defaults to None, 1, 3 and 6 months and 1, 2, 5 and 10 years.
- <u>curve (str, optional):</u> "eiopa" for EIOPA's risk-free rate term structures of the last
month end on or before the date, or "government" for the zero-coupon curves of the
government bond yield curves of the date. Defaults to "eiopa".
- <u>points (bool, optional):</u> Whether to return the forward points, (Forward Rate - Spot
Rate) * 10,000, instead of the forward rates. Defaults to False.
- <u>date (str &#124; None, optional):</u> The day (YYYY-MM-DD). Defaults to None, the end date.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the rounding of the class.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per country the Spot Rate and the forward rate (or the forward points)
of each tenor, in units of the country's currency per unit of the base currency.

**Notes:**

- The market quotes forward points of yen pairs per 100 rather than 10,000; the points
here are per 10,000 for every pair.
- The spot rate is the BIS rate of the day, while EIOPA's curves are those of the last
month end; curve="government" takes the curves of the same day.
- Covered interest parity leaves out the cross-currency basis, which makes US dollar
forwards trade some basis points of carry away from the parity rate.

**As an example:**

```python
from financetoolkit import FixedIncome

fixedincome = FixedIncome(start_date='2026-11-01', end_date='2026-11-20')

fixedincome.get_fx_forward_rates()
```

Which returns:

| Country        |   Spot Rate |       1M |       3M |       6M |       1Y |       2Y |       5Y |      10Y |
|:---------------|------------:|---------:|---------:|---------:|---------:|---------:|---------:|---------:|
| Euro Area      |      0.91   |   0.9091 |   0.9073 |   0.9046 |   0.8993 |   0.8896 |   0.8609 |   0.8101 |
| United Kingdom |      0.7581 |   0.7582 |   0.7584 |   0.7587 |   0.7593 |   0.7621 |   0.7694 |   0.7826 |
| Japan          |    159.296  | 158.945  | 158.247  | 157.205  | 155.141  | 151.547  | 143.133  | 133.421  |
| Switzerland    |      0.8402 |   0.8373 |   0.8315 |   0.8229 |   0.806  |   0.7752 |   0.6944 |   0.5763 |
| Canada         |      1.4291 |   1.4275 |   1.4243 |   1.4196 |   1.4103 |   1.3957 |   1.3589 |   1.3098 |
| Australia      |      1.4848 |   1.4857 |   1.4875 |   1.4903 |   1.4958 |   1.5011 |   1.5256 |   1.5828 |

---

