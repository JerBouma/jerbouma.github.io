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
Collects the statistics of individual bonds from their market price: the yield to maturity, current yield, the Macaulay, modified, effective and dollar duration, DV01 and convexity, plus the present value on the Treasury zero-coupon curve and the Z-spread over it.

Treasuries come from the Treasury's daily FedInvest prices without an API key (see `get_treasury_securities`), corporate bonds from the holdings of bond ETFs (see `get_bond_universe`). Without bonds or an issuer the statistics are those of the benchmark Treasuries: the note or bond maturing closest to 2, 3, 5, 7, 10, 20 and 30 years after the price date, which is the latest issue of that maturity or one that matures a few months earlier. With only a maturity range they are those of every bill, note and bond maturing within it.

The fields are:

- Years to Maturity: counted on the bond's actual coupon dates (actual/actual).
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
\operatorname{PV}(t) = \text{Cash Flow} (t) / (1 + \text{YTM} / 2) ^{2t},\;\; \text{with coupons of Coupon} / 2 \;\text{per}\; 100 \;\text{of par and the principal repaid with the last coupon}
$$

$$
\text{Dirty Price} = \operatorname{SUM}(\operatorname{PV}(t)) = \text{Price} + \text{Accrued Interest},\;\; \text{over the remaining payment times t in years}
$$

$$
\text{Current Yield} = \text{Coupon} \cdot 100 / \text{Price}
$$

$$
\text{Macaulay's Duration} = \operatorname{SUM}(t \cdot \operatorname{PV}(t)) / \text{Dirty Price}
$$

$$
\text{Modified Duration} = \text{Macaulay's Duration} / (1 + \text{YTM} / 2)
$$

$$
\text{Effective Duration} = (\text{Dirty Price} (\text{YTM} - 0.01) - \text{Dirty Price} (\text{YTM} + 0.01)) / (2 \cdot \text{Dirty Price} \cdot 0.01)
$$

$$
\text{Dollar Duration} = \text{Modified Duration} \cdot \text{Dirty Price} / 100
$$

$$
\text{DV01} = (\operatorname{Price}(\text{YTM} - 0.0001) - \operatorname{Price}(\text{YTM} + 0.0001)) / 2
$$

$$
\text{Convexity} = (\text{Dirty Price} (\text{YTM} + 0.0001) + \text{Dirty Price} (\text{YTM} - 0.0001) - 2 \cdot \text{Dirty Price}) / (\text{Dirty Price} \cdot 0.0001 ^{2})
$$

$$
\text{Present Value} = \operatorname{SUM}(\text{Cash Flow} (t) / (1 + \text{Spot Rate} (t) / 2) ^{2t}) - \text{Accrued Interest}
$$

$$
\text{Z-Spread solves Price} = \operatorname{SUM}(\text{Cash Flow} (t) / (1 + (\text{Spot Rate} (t) + \text{Z-Spread}) / 2) ^{2t}) - \text{Accrued Interest}
$$

Where Spot Rate(t) is the Treasury zero-coupon rate of `get_zero_coupon_curve`, restated from annual to semi-annual compounding, interpolated linearly between its maturities. Bills pay no coupon and their yield is the bond-equivalent yield (see `get_bond_equivalent_yield`). TIPS are priced on their inflation-adjusted principal, so their yield is a real yield and they have no present value or Z-spread on the nominal curve. Floating rate notes are left out.

To calculate these statistics for terms of your own, use the functions of `financetoolkit.fixedincome.bond_model` (get_bond_price, get_yield_to_maturity, get_macaulays_duration, get_modified_duration, get_effective_duration, get_dollar_duration, get_dv01, get_convexity and get_z_spread).

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
| Present Value       | 100.3147    | 100.7082    | 98.4008     | 98.028      |
| Z-Spread            | 0.0         | 0.0         | 0.0         | -0.0001     |

---

## get_present_value
Calculates the present value of individual bonds: their coupons and principal discounted with the Treasury zero-coupon curve of the price date, next to the price they trade at. For a Treasury the two differ by how far the issue trades off the curve; for a corporate bond the present value is the price it would have without any credit or liquidity risk, and the gap with its price is what the Z-spread (`get_z_spread`) measures.

The formula is as follows:

$$
\text{Dirty Price} = \operatorname{SUM}(C / (1 + s(t_{i}) / 2) ^{2 t_{i}}) + F / (1 + s(t_{n}) / 2) ^{2 t_{n}},\;\; \text{over} \;\; \text{the remaining coupons}\; i = 1,\;\; \text{...},\;\; \text{n}
$$

$$
\text{Accrued Interest} = C \cdot a
$$

$$
\text{Present Value} = \text{Dirty Price} - \text{Accrued Interest},\;\; \text{the clean price}
$$

where:

$$
C = \text{Coupon payment per half year},\;\; 100 \cdot \text{Coupon} / 2
$$

$$
s(t) = \text{Treasury zero-coupon rate at}\; t \;\text{years} (\text{get\_zero\_coupon\_curve}),\;\; \text{restated from annual to semi-annual compounding and interpolated linearly between its maturities}
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
| 91282CLR0 |   0.0412 | 2029-10-31 |  98.875  |         98.8811 |
| 91282CRT0 |   0.0475 | 2031-10-31 | 100.688  |        100.708  |
| 91282CRV5 |   0.0488 | 2033-10-31 | 101.062  |        101.039  |
| 91282CRF0 |   0.0462 | 2036-08-15 |  98.4375 |         98.4008 |
| 912810RU4 |   0.0288 | 2046-11-15 |  70.0312 |         69.9175 |
| 912810UW6 |   0.0512 | 2056-08-15 |  98.125  |         98.028  |

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
\operatorname{PV}(t) = \text{Cash Flow} (t) / (1 + \text{YTM} / 2) ^{2t},\;\; \text{with coupons of Coupon} / 2 \;\text{per}\; 100 \;\text{of par and the principal repaid with the last coupon}
$$

$$
\text{Dirty Price} = \operatorname{SUM}(\operatorname{PV}(t)),\;\; \text{over the remaining payment times t in years on the actual coupon dates}
$$

$$
\text{Macaulay's Duration} = \operatorname{SUM}(t \cdot \operatorname{PV}(t)) / \text{Dirty Price}
$$

$$
\text{Modified Duration} = \text{Macaulay's Duration} / (1 + \text{YTM} / 2)
$$

$$
\text{Effective Duration} = (\text{Dirty Price} (\text{YTM} - 0.01) - \text{Dirty Price} (\text{YTM} + 0.01)) / (2 \cdot \text{Dirty Price} \cdot 0.01)
$$

$$
\text{Dollar Duration} = \text{Modified Duration} \cdot \text{Dirty Price} / 100
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
\text{Price} + C \cdot a = \operatorname{SUM}(C / (1 + \text{YTM} / 2) ^{2 t_{i}}) + F / (1 + \text{YTM} / 2) ^{2 t_{n}},\;\; \text{over} \;\; \text{the remaining coupons}\; i = 1,\;\; \text{...},\;\; \text{n}
$$

where:

$$
C = \text{Coupon payment per half year},\;\; 100 \cdot \text{Coupon} / 2
$$

$$
a = \text{Elapsed fraction of the current coupon period},\;\; \text{in actual days (actual/actual)},\;\; \text{0 on a coupon date}
$$

$$
t_{i} = \text{Time of the i-th cash flow in years},\;\; \text{on the bond's actual coupon dates}
$$

$$
F = \text{Face value of}\; 100
$$

The yield is a nominal annual rate compounded twice a year (bond-equivalent), as the Treasury and US corporate bond markets quote it, solved with the secant method. For a bill it is the bond-equivalent yield of its discount price (see `get_bond_equivalent_yield`), for TIPS the real yield. The bonds are selected as in `collect_bond_statistics`. For terms of your own, use `bond_model.get_yield_to_maturity`.

The yield to maturity is the return of a bond bought at this price and held to maturity, if every coupon is reinvested at the same yield and the issuer pays in full. It is the standard way to quote and compare bonds, but it is one average rate for all cash flows: bonds with the same maturity but different coupons have different yields even when both are priced in line with the same spot curve, which the Z-spread (`get_z_spread`) accounts for. For callable bonds the yield to worst is quoted instead.

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
\text{Price} = \operatorname{SUM}(\text{Cash Flow} (t) / (1 + (\text{Spot Rate} (t) + \text{Z-Spread}) / 2) ^{2t}) - \text{Accrued Interest}
$$

Where each coupon is 100 * Coupon / 2, the principal is repaid with the last coupon, t is each remaining payment time in years on the bond's actual coupon dates and Spot Rate(t) is the Treasury zero-coupon rate of the price date (`get_zero_coupon_curve`), restated from annual to semi-annual compounding, interpolated linearly between its maturities and held flat beyond its first and last maturity.

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
| US037833EU05 | APPLE INC |   0.0415 | 2030-05-10 |   97.95 | 2026-11-05   |     0.0024 |
| US037833DU14 | APPLE INC |   0.0165 | 2030-05-11 |   89.69 | 2026-11-05   |     0.0033 |
| US037833EZ91 | APPLE INC |   0.042  | 2030-05-12 |   98.25 | 2026-11-05   |     0.002  |
| US037833DY36 | APPLE INC |   0.0125 | 2030-08-20 |   87.72 | 2026-11-05   |     0.0027 |
| US037833ED89 | APPLE INC |   0.0165 | 2031-02-08 |   87.78 | 2026-11-05   |     0.0029 |
| US037833EJ59 | APPLE INC |   0.017  | 2031-08-05 |   86.74 | 2026-11-05   |     0.0027 |
| US037833FG02 | APPLE INC |   0.049  | 2031-11-09 |   99.83 | 2026-11-05   |     0.0035 |
| US037833FA32 | APPLE INC |   0.045  | 2032-05-12 |   98.35 | 2026-11-05   |     0.0022 |
| US037833EP10 | APPLE INC |   0.0335 | 2032-08-08 |   92.53 | 2026-11-05   |     0.0022 |
| US037833EV87 | APPLE INC |   0.043  | 2033-05-10 |   95.84 | 2026-11-05   |     0.0038 |
| US037833FH84 | APPLE INC |   0.051  | 2033-11-09 |   99.77 | 2026-11-05   |     0.0044 |
| US037833FB15 | APPLE INC |   0.0475 | 2035-05-12 |   97.91 | 2026-11-05   |     0.0028 |

---

## get_key_rate_duration
Calculates the key rate durations of individual bonds on the Treasury zero-coupon curve: the price sensitivity to a shock at a single maturity ("key rate") of the curve while every other point is held fixed. Whereas `get_duration` with `duration_type='effective'` assumes the entire curve shifts in parallel, key rate durations show which segment of the curve a bond's price is exposed to. Because cash flows are discounted using linear interpolation between the curve's maturities, a shock at an inner maturity tapers off towards its neighbours and has no effect beyond them. The curve is held flat beyond its first and last maturities, so a shock at the first maturity moves every cash flow paid before it in full (and a shock at the last maturity every cash flow paid after it).

Summing the key rate durations across every maturity of the curve approximately reproduces the bond's effective (parallel-shift) duration on the curve. A barbell and a bullet with the same duration have very different key rate profiles and react differently when the curve steepens or flattens, which is why key rate durations are hedged with instruments at each key maturity. The profile also depends on which maturities the curve contains: the same bond shows different key rate durations on a curve with more or fewer points.

The formula is as follows:

$$
\text{Dirty Price} = \operatorname{SUM}(\text{Cash Flow} (t) / (1 + \text{Spot Rate} (t) / 2) ^{2t})
$$

$$
\text{Key Rate Duration} = - (\text{Dirty Price} (\text{Key Rate} + \Delta y) - \text{Dirty Price} (\text{Key Rate} - \Delta y)) / (2 \cdot \text{Dirty Price} \cdot \Delta y)
$$

Where each coupon is 100 * Coupon / 2, the principal is repaid with the last coupon, t is each remaining payment time in years on the bond's actual coupon dates, Spot Rate(t) is the Treasury zero-coupon rate of the price date (`get_zero_coupon_curve`), restated from annual to semi-annual compounding and interpolated linearly between its maturities, and Δy is the shock applied to the key rate only (1 basis point by default).

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

## get_taylor_price_change
Estimates the percentage change in the price of individual bonds for a change in their yield, using a second-order Taylor series expansion that combines modified duration and convexity.

Modified duration alone only captures the first-order (linear) relationship between a bond's price and its yield, which understates the price increase for a yield decrease and overstates the price decrease for a yield increase because the true price-yield relationship is curved (convex), not linear. Adding a convexity term corrects for this and produces a substantially more accurate estimate, especially for larger yield changes.

The formula is as follows:

$$
\text{Modified Duration} = \operatorname{SUM}(t \cdot \operatorname{PV}(t)) / \text{Dirty Price} / (1 + \text{YTM} / 2),\;\; \text{see get\_duration}
$$

$$
\text{Convexity} = (\text{Dirty Price} (\text{YTM} + 0.0001) + \text{Dirty Price} (\text{YTM} - 0.0001) - 2 \cdot \text{Dirty Price}) / (\text{Dirty Price} \cdot 0.0001 ^{2})
$$

$$
\%\Delta \;\text{Price} \approx - \text{Modified Duration} \cdot \Delta y + 0.5 \cdot \text{Convexity} \cdot \Delta y ^{2}
$$

Where YTM is the bond's yield to maturity at its market price, compounded twice a year (see `get_yield_to_maturity`), Δy is the yield change (0.01 by default) and %ΔPrice is the change of the full (dirty) price as a decimal. The bonds are selected as in `collect_bond_statistics`. For terms of your own, use `bond_model.get_taylor_price_change`.

**Also known as:** duration-convexity approximation, second-order price approximation.

**Args:**

- <u>yield_change (float, optional):</u> The change in the yield to maturity (decimal), negative
for a fall. Defaults to 0.01.
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

**Returns:**

pd.DataFrame: One row per bond with the Issuer, Security Type, Coupon, Maturity,
Price, Price Date and Price Change (decimal).

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

---

## get_bond_equivalent_yield
Calculates the bond-equivalent yield (BEY) of every Treasury bill from its price. Bills are quoted on a discount-yield basis, which understates the return an investor earns because it is computed on face value rather than the (lower) purchase price, and uses a 360-day rather than a 365-day year. The bond-equivalent yield restates the discount yield on a basis that is comparable to coupon-bearing notes and bonds.

The formula is as follows:

$$
\text{Discount Yield} = (100 - \text{Price}) / 100 \cdot 360 / \text{Days to Maturity}
$$

$$
\text{BEY} = 365 \cdot \text{Discount Yield} / (360 - \text{Days to Maturity} \cdot \text{Discount Yield}),\;\; \text{for 182.5 days or less}
$$

$$
\text{BEY} = (- 2t + 2 \cdot \sqrt{t ^{2} - (2t - 1) \cdot (1 - 100 / \text{Price})}) / (2t - 1),\;\; \text{with}\; t = \text{Days to Maturity} / 365,\;\; \text{for more than 182.5 days}
$$

A bill with half a year or less remaining takes the simple restatement onto the purchase price and a 365-day year. Beyond that an equivalent coupon-bearing note would have paid a coupon at the six month point, so the U.S. Treasury's semi-annually compounded solution (31 CFR 356, Appendix B) is used instead. Applying the simple formula to a 52-week bill instead overstates its yield by roughly seven basis points.

The prices are the Treasury's daily FedInvest prices, see `get_treasury_securities`. To convert a discount yield of your own, use `bond_model.get_bond_equivalent_yield`.

**Also known as:** BEY, coupon-equivalent yield, investment rate, T-bill yield.

**Args:**

- <u>bonds (list[str] &#124; str &#124; None, optional):</u> The CUSIPs (or US ISINs) of the bills,
a list or a comma-separated string. Defaults to None, every bill.
- <u>date (str &#124; None, optional):</u> The day of the prices (YYYY-MM-DD). Defaults to None,
the latest day with prices.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results
to. Defaults to None, which uses the rounding of the class.

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

## get_forward_rate
Calculates the implied forward rates between pairs of maturities of a country's zero-coupon (spot) yield curve on a day. The forward rate is the interest rate, implied by that day's curve, for a loan that starts at a future date: it follows from no-arbitrage pricing rather than being a forecast of future rates, and contains a term premium.

The formula is as follows:

$$
\text{Forward Rate} = ((1 + r_{2}) ^{t_{2}} / (1 + r_{1}) ^{t_{1}}) ^{1 / (t_{2} - t_{1})} - 1
$$

where:

$$
r_{1} = \text{Zero-coupon rate at the near maturity},\;\; \text{interpolated linearly from the curve}
$$

$$
t_{1} = \text{Near maturity},\;\; \text{in years}
$$

$$
r_{2} = \text{Zero-coupon rate at the far maturity},\;\; \text{interpolated linearly from the curve}
$$

$$
t_{2} = \text{Far maturity},\;\; \text{in years}
$$

The curve is the zero-coupon curve of `get_zero_coupon_curve`, bootstrapped from the country's government bond par yields and annually compounded, so the forward rate is annually compounded as well. For a curve of your own, use `yieldcurve_model.get_forward_rate`.

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
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results
to. Defaults to None, which uses the rounding of the class.

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

The government bond yield curve quotes par yields at its own maturities; this gives the par yield of any maturity in between (such as 4 or 15 years) with the interpolation done on the zero-coupon rates, where it belongs, rather than on the par yields.

The formula is as follows:

$$
\operatorname{DF}(t) = 1 / (1 + \text{Spot Rate} (t / \text{Frequency}) / \text{Frequency}) ^{t},\;\; \text{the discount factor of a cash flow after t coupon periods}
$$

$$
\text{Par Yield} = \text{Frequency} \cdot (1 - \operatorname{DF}(t_{n})) / (\operatorname{SUM}(\operatorname{DF}(t_{i})) - a),\;\; \text{over} \;\; \text{the remaining coupons}\; i = 1,\;\; \text{...},\;\; \text{n}
$$

where Spot Rate(τ) is the zero-coupon rate of `get_zero_coupon_curve` at τ years, restated from annual compounding to the country's coupon frequency (twice a year, once for Sweden and Norway) and interpolated linearly, a is the elapsed fraction of the current coupon period (0 on a coupon date) and t_i = i - a is the time of the i-th coupon in periods. The par yield is a nominal annual coupon rate paid at the coupon frequency, like the government bond yield curve. For a curve of your own, use `yieldcurve_model.get_par_yield`.

**Also known as:** par rate, par coupon rate.

**Args:**

- <u>years_to_maturity (float &#124; str &#124; list &#124; None, optional):</u> The maturities, in years
or as labels such as '15Y'. Defaults to None, 1 to 30 years.
- <u>country (str, optional):</u> The country, see `get_zero_coupon_curve`. Defaults to
"United States".
- <u>date (str &#124; None, optional):</u> The day of the curve (YYYY-MM-DD), or the last day
before it with a curve. Defaults to None, the end date.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results
to. Defaults to None, which uses the rounding of the class.

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
|                  15 |      0.0507 |
|                  25 |      0.0527 |

---

## get_yield_curve_spread
Calculates the spreads between pairs of maturities of a country's government bond yield curve on a day, e.g. the widely followed 10-year minus 2-year and 10-year minus 3-month Treasury spreads. A positive spread indicates a "normal" upward-sloping curve, while a negative spread ("inversion") has historically been used as a leading indicator of an economic slowdown.

The formula is as follows:

$$
\text{Yield Curve Spread} = \text{Long-Term Yield} - \text{Short-Term Yield}
$$

Where both yields are the par yields of `get_government_bond_yield_curve`, as the Treasury and FRED (T10Y2Y, T10Y3M) calculate the spreads, interpolated linearly for a maturity the curve does not quote. For the history of these spreads, take the difference of two columns of `get_government_bond_yield_curve`; for yields of your own, use `yieldcurve_model.get_yield_curve_spread`.

**Also known as:** term spread, yield curve slope, 10Y-2Y spread.

**Args:**

- <u>long_maturity (float &#124; str &#124; list &#124; None, optional):</u> The longer maturity (or
maturities), in years or as labels such as '10Y'. Defaults to None, 5, 10 and
30 years.
- <u>short_maturity (float &#124; str &#124; list &#124; None, optional):</u> The shorter maturity (or
maturities), in years or as labels such as '3M'. Defaults to None, 3 months
and 2 years.
- <u>country (str, optional):</u> The country, see `get_government_bond_yield_curve`.
Defaults to "United States".
- <u>date (str &#124; None, optional):</u> The day of the curve (YYYY-MM-DD), or the last day
before it with a curve. Defaults to None, the end date.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results
to. Defaults to None, which uses the rounding of the class.

**Returns:**

pd.DataFrame: The spread (decimal) for each combination of long (rows) and short
maturity (columns).

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

Where both yields are the Treasury's par yield curve rates (nominal and real), the simple difference FRED publishes as T5YIE and T10YIE, not (1 + Nominal) / (1 + Real) - 1.

The breakeven rate is often read as the market's expected inflation, but it also contains an inflation risk premium, which raises it, and a liquidity premium on inflation-linked bonds, which lowers it, so it rises and falls in market stress for reasons other than inflation expectations. The comparison is with CPI-U, the index TIPS pay on. The daily history, with the 5-year, 5-year forward rate, is `get_inflation_expectations` in the Economics module; for yields of your own, use `yieldcurve_model.get_breakeven_inflation_rate`.

**Also known as:** TIPS breakeven spread, inflation breakeven.

**Args:**

- <u>date (str &#124; None, optional):</u> The day (YYYY-MM-DD), or the last business day
before it. Defaults to None, the end date.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results
to. Defaults to None, which uses the rounding of the class.

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
- <u>growth (bool, optional):</u> Whether to return the growth data or the actual data. Defaults to False.
- <u>lag (int, optional):</u> The number of periods to lag the data by. Defaults to 1.
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
- <u>growth (bool, optional):</u> Whether to return the growth data or the actual data. Defaults to False.
- <u>lag (int, optional):</u> The number of periods to lag the data by. Defaults to 1.
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

## get_bond_universe
Retrieves thousands of individual US dollar bonds with their price, yield to maturity, modified duration and spread over Treasuries, read from the holdings of bond ETFs.

Individual bond prices are not published for free, but bond ETFs publish their holdings every day: each bond's coupon and maturity (in its name), its par amount and its market value, from which the price follows. By default this reads the iShares iBoxx $ Investment Grade Corporate Bond ETF (LQD), the iShares 0-5 Year Investment Grade Corporate Bond ETF (IGSB) and the iShares Broad USD High Yield Corporate Bond ETF (USHY): together about 8,000 investment grade and high yield corporate bonds. A bond held by several funds is listed once, with the funds that hold it.

The formula is as follows:

$$
\text{Price} = \text{Market Value} / \text{Par Amount} \cdot 100 (a \;\text{clean price per}\; 100 \;\text{of par})
$$

$$
\text{Yield to Maturity:}\;\; \text{the rate y at which the coupons and principal},\;\; \text{discounted at} (1 + y / 2) \text{per half year},\;\; \text{are worth the clean price plus accrued interest (see get\_yield\_to\_maturity)}
$$

$$
\text{Modified Duration} = \text{Macaulay Duration} / (1 + y / 2) (\text{see}\; \text{get\_duration})
$$

$$
\text{G-Spread} = \text{Yield to Maturity} - \text{Treasury Par Yield at the bond's maturity}
$$

Coupons are semi-annual, the US convention for corporate bonds, and the yield is a nominal annual rate compounded twice a year (bond-equivalent), like the Treasury par yields it is compared with. The coupon periods fall on the bond's actual coupon dates, counted back from maturity, and the time in the current period is counted in actual days. The Treasury par yield at a maturity is interpolated linearly between the maturities of the US Treasury par yield curve on the price date (held at the 1-month and 30-year yield beyond them).

**Also known as:** corporate bond prices, bond yields, bond screener, credit spreads per bond, G-spread.

**Args:**

- <u>etfs (list[str] &#124; str &#124; None, optional):</u> The bond ETFs to read the holdings of, as
a list or a comma-separated string. The holdings must name each bond as
"ISSUER COUPON% MM/DD/YYYY" with a par amount, as iShares funds do. Defaults
to None, which uses LQD, IGSB and USHY.
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
- The yield is to maturity. A callable bond that trades above its call price
yields less to its call date (the yield to worst), which is common among high
yield bonds; call schedules are not in the holdings.
- The fund prints the coupon to two decimals (2.125% shows as 2.13%), which moves the
yield by well under a basis point a year of maturity.
- Left out, with a count in the log: lines that are not fixed-coupon bonds (cash,
futures, swaps), floating rate notes, bank notes marked fixed-to-floating
("FXD-FRN", which switch to a floating coupon before maturity), inflation-linked
bonds, mortgage pools, perpetual bonds, bonds without a US ISIN (the funds of
other currencies) and prices outside 1 to 300. A fixed-to-floating note the fund
does not mark as such is kept, and its yield assumes the fixed coupon to maturity.
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
| US037833EC07 |   0.012  | 2028-02-08 |   95.96 |              0.0454 |              1.2213 |     0.0021 |
| US037833ET32 |   0.04   | 2028-05-10 |   99.12 |              0.0461 |              1.4224 |     0.0024 |
| US037833EY27 |   0.04   | 2028-05-12 |   99.09 |              0.0463 |              1.4275 |     0.0025 |
| US037833EH93 |   0.014  | 2028-08-05 |   94.67 |              0.046  |              1.6896 |     0.0019 |
| US037833FD70 |   0.0465 | 2028-11-09 |   99.95 |              0.0468 |              1.8564 |     0.0022 |

---

## get_treasury_securities
Retrieves every marketable US Treasury (bills, notes, bonds, TIPS and floating rate notes) with its price, yield to maturity and modified duration on a day, without an API key.

Where the Treasury par yield curve gives one yield per constant maturity, this lists the roughly 460 securities themselves, from the Bureau of the Fiscal Service's daily FedInvest prices: the prices the Treasury values its own accounts at. That shows where individual issues trade off the curve (old and new issues of the same maturity, the cheapest notes to deliver into futures) and gives the yield of any maturity date.

The formula is as follows:

$$
\text{Notes and bonds:}\;\; \text{Yield to Maturity is the rate y at which the coupons and principal},\;\; \text{discounted at} (1 + y / 2) \text{per half year},\;\; \text{are worth the clean price plus accrued interest (see get\_yield\_to\_maturity)}
$$

$$
\text{Bills:}\;\; \text{Discount Yield} = (100 - \text{Price}) / 100 \cdot 360 / \text{Days},\;\; \text{restated as the bond-equivalent yield (see get\_bond\_equivalent\_yield)}
$$

$$
\text{Modified Duration} = \text{Macaulay Duration} / (1 + y / 2) (\text{see}\; \text{get\_duration})
$$

Coupons are semi-annual and fall on the actual coupon dates, counted back from maturity; the time in the current period is counted in actual days (actual/actual, the Treasury convention). Yields are nominal annual rates compounded twice a year (bond-equivalent), as the Treasury quotes them. For TIPS the price is per 100 of inflation-adjusted principal, so the yield is the real yield. Floating rate notes reset their coupon every week, so they have a price but no yield or duration.

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

No API key is needed: without a FRED API key the curve comes from the Treasury's own HQM files, which gives the same figures. When a FRED API key is set (see the `fred_api_key` parameter of the `FixedIncome` class), it comes from FRED, which republishes the Treasury's curve. The rates are returned as decimal fractions (0.0558 for 5.58%), semi-annual bond-equivalent as the Treasury publishes them.

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
Computes the credit spread of high quality US corporate bonds per maturity: the Treasury's High Quality Market (HQM) corporate par yield minus the Treasury constant maturity yield, at 2, 5, 10 and 30 years, monthly. Both legs are par yields averaged over the month, so they are directly comparable. The spread is what investors demand for the default and liquidity risk of investment grade companies, and its shape across maturities, usually wider for longer maturities, shows how that compensation grows with time.

Unlike the ICE BofA option-adjusted spreads (see `get_ice_bofa_option_adjusted_spread`), of which FRED only carries the last three years, this spread covers decades, long enough to calibrate how credit spreads behave through several business cycles.

The formula is as follows:

$$
\text{HQM Spread} (\text{maturity}) = \text{HQM Corporate Par Yield} (\text{maturity}) - \text{Treasury Constant Maturity Yield} (\text{maturity}),\;\; \text{both monthly averages},\;\; \text{for 2},\;\; \text{5},\;\; \text{10 and 30 years}
$$

No API key is needed: without a FRED API key both legs come from the Treasury, the HQM par yields from its HQM files and the Treasury yields as the monthly averages of its daily par yield curve, rounded to two decimals in percent as the Federal Reserve's H.15 release publishes them. That curve starts in 1990 and has no 30-year yield from February 2002 to February 2006, so the keyless spread starts in 1990 and leaves those 30-year months empty. When a FRED API key is set (see the `fred_api_key` parameter of the `FixedIncome` class), the Treasury yields are FRED's constant maturity series, from 1984. The spreads are returned as decimal fractions (0.0079 for 0.79 percentage points).

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

## get_term_premium
Retrieves the Treasury term premia of Adrian, Crump and Moench (2013), as the Federal Reserve Bank of New York estimates them daily from 1961 for maturities of 1 to 10 years. A Treasury yield is split into the average short rate investors expect over the bond's life and the term premium: the extra yield they demand for holding a long bond instead of rolling over short ones. The split tells whether a move in long yields comes from expected monetary policy or from compensation for risk, such as inflation and fiscal uncertainty.

Adrian, T., Crump, R. K., & Moench, E. (2013). Pricing the Term Structure with Linear Regressions. Journal of Financial Economics, 110(1), 110-138. [https://doi.org/10.1016/j.jfineco.2013.04.009](https://doi.org/10.1016/j.jfineco.2013.04.009){:target="_blank"}

Three components are returned per maturity: the "Term Premium", the "Expected Short Rate" (the risk-neutral yield, the yield if investors were indifferent to risk) and the "Fitted Yield" of the model, which is their sum. The model is fitted to the zero-coupon Treasury curve of Gürkaynak, Sack and Wright (2007), so every value is a continuously compounded zero-coupon rate, as a decimal fraction (0.0067 for 0.67%). No API key is needed. Weekly and monthly periods take the last day of each period, matching the New York Fed's own month-end series.

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

