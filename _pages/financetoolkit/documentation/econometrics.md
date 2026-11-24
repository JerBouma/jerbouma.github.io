---
title: Econometrics
seo_title: "Econometrics in Python | Finance Toolkit"
seo_title_suffix: false
excerpt: The Econometrics module contains statistical tests and estimators for financial time series and panel data, including unit root and cointegration tests, regression estimators, causal inference methods, diagnostics, forecasting and event studies.
description: "Run unit root and cointegration tests, regressions and forecasts on financial and economic data in Python with the Finance Toolkit's Econometrics module."
author_profile: false
permalink: /projects/financetoolkit/docs/econometrics
classes: wide-sidebar
layout: single
redirect_from:
    - /econometrics
    - /projects/financetoolkit/econometrics-notebook
sidebar:
    nav: "financetoolkit-docs-econometrics"
---

The Econometrics module contains statistical tests and estimators for financial time series and panel data. It covers unit root and cointegration tests, regression estimators (OLS, WLS, GLS, quantile, logit, probit, Fama-MacBeth), causal inference methods (instrumental variables, difference-in-differences, regression discontinuity, propensity score matching, synthetic control), panel data estimators, specification and diagnostic tests, time series forecasting (ARIMA, VAR, VECM) and event studies.

Use it in Claude, ChatGPT or another AI assistant through the [Finance Toolkit MCP](/projects/financetoolkit/mcp), or in Python. Unlike the other modules, this one depends on `statsmodels` and `linearmodels`. These are bundled in the optional `econometrics` extra, so install the Finance Toolkit with:

```python
pip install "financetoolkit[econometrics]" -U
```

{% include docs-search.html %}

{% include financetoolkit-getting-started/econometrics.md %}

## get_iv_2sls
Fit an Instrumental Variables regression via Two-Stage Least Squares (2SLS) of `dependent_ticker` on `endogenous_ticker`, instrumented by `instrument_tickers`.

**Also known as:** IV, 2SLS, IV-2SLS.

For more information about the method, and why plain OLS on an asset suspected of reverse-causality/omitted-confounder bias against another asset is unreliable, see `causal_inference_model.get_iv_2sls`.

A natural use case in a multi-asset return panel: suppose `endogenous_ticker`'s return is suspected to be simultaneously determined together with `dependent_ticker`'s return (e.g. two closely related assets that react to each other intraday, or one asset's return partly reflects news about the other) -- plain OLS of one on the other is then biased. An `instrument_tickers` asset that moves `endogenous_ticker` for reasons unrelated to `dependent_ticker`'s own error term (e.g. a supplier/peer whose moves affect `endogenous_ticker` but only reach `dependent_ticker`, if at all, THROUGH `endogenous_ticker`) allows recovering a cleaner estimate of the causal pass-through.

The formula is as follows:

$$
Z = \left[1,\; \text{exogenous tickers},\; \text{instruments}\right]\;\;\text{and}\;\; X = \left[1,\; \text{exogenous tickers},\; \text{endogenous tickers}\right],\;\; \text{all in column (Return by default), the constant only with add\_constant=True}
$$

$$
\text{Stage 1:}\;\; \hat{X} = Z(Z' Z)^{- 1} Z' X,\;\; \text{the fitted values of each endogenous ticker regressed on } Z
$$

$$
\text{Stage 2:}\;\; \hat{\beta} = (\hat{X}' X)^{- 1} \hat{X}' y
$$

$$
\operatorname{Cov}(\hat{\beta}) = \hat{\sigma}^{2} \cdot (\hat{X}' \hat{X})^{- 1},\;\; \text{with}\;\; \hat{\sigma}^{2} = \frac{\sum(y_{t} - x_{t}' \hat{\beta})^{2}}{n - k} \;(\text{linearmodels}\; \text{IV2SLS} \;\text{with}\; \text{cov\_type} = \text{"unadjusted"} \;\text{and debiased} = \text{True})
$$

**Args:**

- <u>dependent_ticker (str):</u> The dependent (predicted) asset.
- <u>endogenous_ticker (str &#124; list[str]):</u> The endogenous regressor asset(s) --
suspected correlated with the error term.
- <u>instrument_tickers (str &#124; list[str]):</u> The excluded instrument asset(s),
correlated with `endogenous_ticker` but assumed uncorrelated with the error
term. Must supply at least as many instruments as endogenous regressors.
- <u>exogenous_tickers (str &#124; list[str] &#124; None, optional):</u> Other, non-instrumented
control asset(s) included as-is in both stages. Defaults to None.
- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to regress on. Defaults to
"Return".
- <u>add_constant (bool, optional):</u> Whether to include an intercept. Defaults to True.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: A coefficient table (Coefficient, CORRECTED Std. Error, t-Statistic,
P-Value), indexed by regressor name -- see `causal_inference_model.get_iv_2sls` for
why these standard errors differ from (and correct) what a naive two-OLS-calls
approach would report.

**Notes:**

- Requires linearmodels (`pip install financetoolkit[econometrics]`).

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["SMCI", "NVDA", "TSM"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_iv_2sls(
    dependent_ticker="SMCI", endogenous_ticker="NVDA", instrument_tickers="TSM"
)
```

Which returns:

|           |   Coefficient |   Std. Error |   t-Statistic |   P-Value |
|:----------|--------------:|-------------:|--------------:|----------:|
| Intercept |       -0.0008 |       0.0027 |       -0.2931 |    0.7697 |
| NVDA      |        1.2518 |       0.1094 |       11.441  |    0      |

---

## get_difference_in_differences
Fit a Difference-in-Differences (DiD) regression estimating the effect of some event on `treatment_date` for `treated_tickers`, relative to `control_tickers`.

**Also known as:** DiD, DD, difference-in-differences estimator.

For more information about the method, and why the `Treated x Post` interaction coefficient IS the DiD treatment-effect estimate, see `causal_inference_model.get_difference_in_differences`.

Builds a stacked (ticker, date) panel from every ticker in `treated_tickers` and `control_tickers`: each observation's outcome is that ticker's return on that date, `Treated` is 1 for every observation belonging to a `treated_tickers` asset (regardless of date) and 0 for `control_tickers` assets, and `Post` is 1 for observations on or after `treatment_date` (regardless of asset). This answers "did `treated_tickers` behave differently after `treatment_date`, beyond both their normal average gap versus `control_tickers` and the common market-wide move over that same before/after window?" -- e.g. isolating the effect of an event (an index-inclusion announcement, a regulatory change affecting only some tickers, an earnings surprise) that hits `treated_tickers` but not `control_tickers`, at a known date.

With returns as the outcome, the `Treated x Post` coefficient is the change in the average return per period after the event, not the price impact around it, which is what `get_event_study` measures. The panel stacks tickers observed on the same dates, whose returns are correlated, while the standard errors treat every observation as independent, so the p-value tends to be too low for closely related tickers. The estimate rests on parallel trends, so the first check is whether both groups moved alike before the event.

The formula is as follows:

$$
y_{it} = \beta_{0} + \beta_{1} \cdot \text{Treated}_{i} + \beta_{2} \cdot \text{Post}_{t} + \delta \cdot (\text{Treated}_{i} \cdot \text{Post}_{t}) + \epsilon_{it},\;\; \text{fitted by OLS with classical standard errors on the stacked (ticker, date) panel of column (Return by default)}
$$

$$
\text{Treated}_{i} = 1 \;\text{for} \;\text{treated\_tickers},\;\; \text{Post}_{t} = 1 \;\text{on or after} \;\text{treatment\_date}
$$

$$
\hat{\delta} = (\operatorname{mean}(y_{\text{treated},\text{post}}) - \operatorname{mean}(y_{\text{treated},\text{pre}})) - (\operatorname{mean}(y_{\text{control},\text{post}}) - \operatorname{mean}(y_{\text{control},\text{pre}}))
$$

**Args:**

- <u>treated_tickers (str &#124; list[str]):</u> The asset(s) subject to the event/treatment.
- <u>treatment_date (str):</u> The date the event/treatment occurs, in the same format
accepted by `pd.Timestamp`. Observations on or after this date are `Post = 1`; with
periods longer than a day, a period counts from its last day, so the period that holds the
treatment date is the first treated one.
- <u>control_tickers (str &#124; list[str] &#124; None, optional):</u> The untreated comparison
asset(s). Defaults to None, which uses every ticker NOT in `treated_tickers`,
excluding "Benchmark" (pass `control_tickers="Benchmark"` to use the benchmark as
the control group).
- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to use as the outcome.
Defaults to "Return".
- <u>add_constant (bool, optional):</u> Whether to include an intercept. Defaults to True.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: A coefficient table (Coefficient, Std. Error, t-Statistic, P-Value)
with rows `Intercept`, `Treated`, `Post` and `Treated x Post` -- the last of
which is the DiD treatment-effect estimate.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["NVDA", "INTC"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_difference_in_differences(
    treated_tickers="NVDA",
    control_tickers="INTC",
    treatment_date="2023-06-01",
    period="monthly",
)
```

Which returns:

|                |   Coefficient |   Std. Error |   t-Statistic |   P-Value |
|:---------------|--------------:|-------------:|--------------:|----------:|
| Intercept      |       -0.0126 |       0.0262 |       -0.4796 |    0.6324 |
| Treated        |        0.0669 |       0.0371 |        1.8059 |    0.0736 |
| Post           |        0.0291 |       0.0362 |        0.8043 |    0.4229 |
| Treated x Post |       -0.0246 |       0.0511 |       -0.4813 |    0.6312 |

---

## get_regression_discontinuity
Estimate a Sharp Regression Discontinuity (RDD): the jump in `dependent_ticker` exactly where `running_variable_ticker` crosses `cutoff`.

**Also known as:** RDD, sharp RD.

For more information about the method, see `causal_inference_model.get_regression_discontinuity`.

Treats `running_variable_ticker`'s value as the running variable that (hypothetically) triggers some discrete change once it crosses `cutoff` -- e.g. testing whether `dependent_ticker`'s return behaves discontinuously around a round-number/threshold level of another asset or indicator (a psychological price level, an index-inclusion market-cap threshold, a macro indicator's policy-relevant threshold) fed in as `running_variable_ticker`. Fits separate local linear regressions of `dependent_ticker`'s return on the (cutoff-centered) `running_variable_ticker` value, one on each side of `cutoff`, and reports the gap between the two fitted lines exactly at the cutoff.

The formula is as follows:

$$
\tilde{x}_{t} = x_{t} - \text{cutoff},\;\; \text{keeping the observations with} \;\left|\tilde{x}_{t}\right| < h,\;\; \text{where}\;\; x_{t} \;\text{is the running ticker's} \;\text{column} \;(\text{Return by default}) \;\text{and}\; h = \text{bandwidth},\;\; \text{or half the range of } x_{t} \text{ by default}
$$

$$
\text{Each side (} \tilde{x}_{t} < 0 \text{ and } \tilde{x}_{t} \geq 0 \text{):}\;\; y_{t} = a + b \cdot \tilde{x}_{t} + e_{t},\;\; \text{fitted by OLS} \;(\text{kernel} = \text{"uniform"},\; \text{the default}) \;\text{or by WLS with weights}\; 1 - \frac{\left|\tilde{x}_{t}\right|}{h} \;(\text{kernel} = \text{"triangular"})
$$

$$
\text{Discontinuity} = a_{\text{right}} - a_{\text{left}},\;\; \text{with}\;\; \text{SE} = \sqrt{\operatorname{SE}(a_{\text{right}})^{2} + \operatorname{SE}(a_{\text{left}})^{2}}
$$

$$
t = \frac{\text{Discontinuity}}{\text{SE}},\;\; \text{with a Student-t distribution on the two sides' residual degrees of freedom combined}
$$

**Args:**

- <u>dependent_ticker (str):</u> The outcome asset.
- <u>running_variable_ticker (str):</u> The asset (or column) whose value determines
which side of `cutoff` an observation falls on.
- <u>cutoff (float):</u> The threshold value of `running_variable_ticker` at which the
discontinuity is estimated.
- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to use for both series.
Defaults to "Return".
- <u>bandwidth (float &#124; None, optional):</u> The maximum distance from `cutoff` an
observation may be to be included in either local regression. Defaults to
None, which uses half of the running variable's observed range -- see
`causal_inference_model.get_regression_discontinuity` for why this is a
deliberately naive default.
- <u>kernel (str, optional):</u> One of "uniform" or "triangular". Defaults to "uniform".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: A one-column results table with the discontinuity estimate, its
standard error/t-statistic/p-value, and the cutoff/bandwidth/sample sizes used.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["COIN", "BTCUSD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2022-01-01",
    end_date="2025-12-31",
)

# COIN's return on days Bitcoin rises versus days it falls
toolkit.econometrics.get_regression_discontinuity(
    dependent_ticker="COIN", running_variable_ticker="BTCUSD", cutoff=0
)
```

Which returns:

|               |    Value |
|:--------------|---------:|
| Discontinuity |   0.0031 |
| Std. Error    |   0.0027 |
| t-Statistic   |   1.1191 |
| P-Value       |   0.2633 |
| Cutoff        |   0      |
| Bandwidth     |   0.1497 |
| N Left        | 729      |
| N Right       | 728      |

---

## get_propensity_score_matching
Estimate the Average Treatment effect on the Treated (ATT) of `treatment_ticker` exceeding `treatment_threshold` on `dependent_ticker`'s return, via Propensity Score Matching (PSM) on `covariate_tickers`.

**Also known as:** PSM, nearest-neighbor propensity matching.

For more information about the method, see `causal_inference_model.get_propensity_score_matching`.

Derives a binary "treatment" indicator the same way `get_binary_choice_regression` derives its binary outcome: 1 if `treatment_ticker`'s return in a given period exceeds `treatment_threshold` (0.0, i.e. a positive return, by default), else 0. This lets PSM answer e.g. "on periods where `treatment_ticker` has an outsized/positive move, is `dependent_ticker`'s return different than it would otherwise be -- comparing only periods that LOOK similar on `covariate_tickers` (to control for the possibility that `treatment_ticker` tends to move on the same periods/regimes that also independently affect `dependent_ticker`)?"

The formula is as follows:

$$
D_{t} = 1 \;\text{if the treatment ticker's} \;\text{column} \;(\text{Return by default}) \;\text{is above} \;\text{treatment\_threshold} \;(0 \;\text{by default}),\;\; \text{else 0}
$$

$$
e(x_{t}) = \frac{1}{1 + \exp(- x_{t}' \beta)},\;\; \text{a logit of } D_{t} \text{ on the covariate tickers (plus a constant)}
$$

$$
\text{Matching on}\; \ell_{t} = \ln\left(\frac{e}{1 - e}\right) \;\text{:} \;\text{each treated period},\;\; \text{in order},\;\; \text{takes the nearest unmatched control period} \;(\text{one-to-one},\; \text{without replacement}) \;\text{if} \;\left|\ell_{\text{treated}} - \ell_{\text{control}}\right| \leq \text{caliper},\;\; \text{which defaults to 0.2 × the standard deviation (ddof=1) of ℓ}
$$

$$
\text{ATT} = \frac{1}{m} \cdot \sum(y_{\text{treated}} - y_{\text{control}}) \;\text{over the}\; m \;\text{matched pairs}
$$

$$
\text{SE} = \frac{\operatorname{std}(y_{\text{treated}} - y_{\text{control}},\; \text{ddof} = 1)}{\sqrt{m}},\;\; \text{with a Student-t distribution with}\; m - 1 \;\text{degrees of freedom}
$$

**Args:**

- <u>dependent_ticker (str):</u> The outcome asset.
- <u>treatment_ticker (str):</u> The asset whose return, once it exceeds
`treatment_threshold`, defines the treatment indicator.
- <u>covariate_tickers (str &#124; list[str]):</u> The asset(s) used as covariates to
estimate the propensity score -- should include asset(s) believed to drive
selection into "treatment".
- <u>treatment_threshold (float, optional):</u> The return threshold defining
treatment. Defaults to 0.0.
- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to use. Defaults to "Return".
- <u>caliper (float &#124; None, optional):</u> The maximum allowed logit-propensity-score
matching distance. Defaults to None, which uses Austin's (2011) rule of thumb
-- see `causal_inference_model.get_propensity_score_matching`.
- <u>add_constant (bool, optional):</u> Whether to include an intercept in the
propensity score model. Defaults to True.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series: The ATT estimate, its standard error/t-statistic/p-value, and the
number of matched pairs/treated/control observations.

**Notes:**

- Requires statsmodels (`pip install financetoolkit[econometrics]`).

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["XOM", "USO"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

# XOM's return on days USO rises more than 2%, matched on the Benchmark's return
toolkit.econometrics.get_propensity_score_matching(
    dependent_ticker="XOM",
    treatment_ticker="USO",
    covariate_tickers="Benchmark",
    treatment_threshold=0.02,
)
```

Which returns:

|               |     Value |
|:--------------|----------:|
| ATT           |    0.0163 |
| Std. Error    |    0.0016 |
| t-Statistic   |    9.9366 |
| P-Value       |    0      |
| Matched Pairs |  181      |
| N Treated     |  185      |
| N Control     | 1069      |

---

## get_synthetic_control
Construct a Synthetic Control for `treated_ticker` from a weighted combination of `donor_tickers` (Abadie, Diamond & Hainmueller, 2010), and estimate the effect of an event/intervention as the post-`treatment_period` gap between `treated_ticker`'s actual and synthetic counterfactual return path.

When a single company or market experiences an event (an acquisition, a regulatory change, an index inclusion) and there is no single obvious comparison, the synthetic control builds one from the data: a weighted average of unaffected "donor" tickers, with weights chosen so it tracks the treated ticker as closely as possible before the event. If that pre-event fit is good, the synthetic control's path after the event estimates what would have happened without it, and the gap is the estimated effect.

The formula is as follows:

$$
\text{Weights:}\;\; w^{*} = \operatorname*{arg\,min}_{w} \left\|\text{treated\_pre} - \text{donors\_pre} \, w\right\|^{2},\;\; \text{subject to}\; w \geq 0 \;\text{and sum}(w) = 1 (\text{SLSQP}),\;\; \text{with pre the dates before treatment\_period}
$$

$$
\text{Synthetic control:}\;\; \text{synthetic}_{t} = \text{donors}_{t} \, w^{*},\;\; \text{for every period } t
$$

$$
\text{Treatment effect:}\;\; \text{gap}_{t} = \text{treated}_{t} - \text{synthetic}_{t},\;\; \text{for every post-event period } t
$$

$$
\text{Average Treatment Effect} = \text{mean of}\; \text{gap}_{t} \;\text{over the post-event periods}
$$

$$
\text{RMSPE ratio} = \frac{\sqrt{\operatorname{mean}(\text{gap\_post}^{2})}}{\sqrt{\operatorname{mean}(\text{gap\_pre}^{2})}}
$$

$$
\text{P-Value} = \text{the share of the treated ticker's and every placebo donor's RMSPE ratios that are at least the treated ticker's ratio}
$$

- All series are the tickers' `column` (Return by default)

Unlike difference-in-differences, this does not require the treated and comparison units to follow parallel trends, as the synthetic control is built to match the treated ticker's own pre-event path. Because there is only one treated unit, the p-value comes from placebo tests: the procedure is rerun with each donor as if it were treated, and the treated ticker's post/pre fit ratio is compared with theirs. Matching is done on the pre-event outcome path only, a common simplification of the original method.

For more information about the method, see the following papers:

- Abadie, A., Diamond, A., & Hainmueller, J. (2010). "Synthetic Control Methods for Comparative Case Studies: Estimating the Effect of California's Tobacco Control Program." Journal of the American Statistical Association, 105(490), 493-505.
- Abadie, A. (2021). "Using Synthetic Controls: Feasibility, Data Requirements, and Methodological Aspects." Journal of Economic Literature, 59(2), 391-425.

**Also known as:** SCM, synthetic control method.

**Args:**

- <u>treated_ticker (str):</u> The asset believed to be affected by an event/
intervention starting at `treatment_period`.
- <u>treatment_period (str):</u> The first post-treatment period -- periods at or
after this value (within `period`'s index) are treated as post-treatment,
everything before as pre-treatment (used to fit the synthetic control's
weights).
- <u>donor_tickers (str &#124; list[str] &#124; None, optional):</u> The ticker(s) forming
the donor pool the synthetic control is built from. Defaults to None,
meaning every other Toolkit ticker (subject to `include_benchmark`).
- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to use. Defaults to "Return".
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" in the
default donor pool (has no effect when donor_tickers is given explicitly).
Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series: The average post-treatment effect, pre/post RMSPE and their
ratio, the placebo-based p-value, and the donor pool/period counts.

**Notes:**

- Needs at least 2 donor tickers -- with only 1-2 Toolkit tickers loaded,
pass `donor_tickers` explicitly (e.g. including "Benchmark") or (better)
construct the Toolkit with more tickers, since small donor pools give both a
poorly-identified synthetic control and a very coarse placebo p-value (with
`k` donors, the smallest achievable p-value is `1 / (k + 1)`).

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["BA", "AIR.PA", "LMT", "GD", "RTX", "NOC"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2023-01-01",
    end_date="2024-12-31",
)

# Boeing after the 737 MAX 9 grounding, with the other aerospace companies as donors
toolkit.econometrics.get_synthetic_control(treated_ticker="BA", treatment_period="2024-01-08")
```

Which returns:

|                          |    Value |
|:-------------------------|---------:|
| Average Treatment Effect |  -0.0017 |
| Pre-Treatment RMSPE      |   0.0156 |
| Post-Treatment RMSPE     |   0.0204 |
| RMSPE Ratio              |   1.3094 |
| P-Value                  |   0.5    |
| N Donors                 |   5      |
| N Pre-Periods            | 260      |
| N Post-Periods           | 255      |

---

## get_event_study
Perform a market-model event study around a single event date, following the methodology in MacKinlay, A.C. (1997), "Event Studies in Economics and Finance," Journal of Economic Literature, 35(1), 13-39 -- the canonical reference and still the dominant approach used to measure the stock-price impact of corporate events (earnings announcements, M&A deals, index additions/deletions, dividend changes, regulatory actions, etc.).

A market model (`Return_t = alpha + beta * Benchmark_Return_t + e_t`) is fit via OLS over a clean "estimation window" ending `gap_days` before the event, then the Abnormal Return on each day of the "event window" around the event is the actual return minus the market-model-predicted expected return. These are cumulated into the Cumulative Abnormal Return (CAR) -- the stock-price impact attributable to the event, after stripping out what would have been expected from general market movements alone -- along with a t-test of whether CAR is significantly different from zero.

The `event_date` is the first trading day on which the news can be priced, so for results released after the close it is the next trading day. The CAR runs from `pre_event_days` before to `post_event_days` after it (21 trading days by default), which also captures any leak ahead of the announcement. The t-test treats the abnormal returns as independent and uses the residual Variance of the estimation window, so a single event is weak evidence; studies average the CARs of many events of the same kind.

The formula is as follows:

$$
\text{Market model:}\;\; R_{t} = \alpha + \beta \cdot R_{m,t} + \epsilon_{t},\;\; \text{fitted by OLS on the daily column (Return by default) of the ticker and the Benchmark over the estimation\_window (250) trading days that end gap\_days (30) trading days before the event}
$$

$$
\text{AR}_{t} = R_{t} - (\hat{\alpha} + \hat{\beta} \cdot R_{m,t}),\;\; \text{for}\;\; t = - \text{pre\_event\_days} \;\ldots + \text{post\_event\_days} \;(10 \;\text{and}\; 10)
$$

$$
\text{CAR} = \sum \;\text{AR}_{t} \;\text{over the}\; L = \text{pre\_event\_days} + \text{post\_event\_days} + 1 \;\text{event-window days}
$$

$$
t = \frac{\text{CAR}}{\sqrt{L \cdot \hat{\sigma}^{2}}},\;\; \text{with}\;\; \hat{\sigma}^{2} = \frac{\sum \hat{\epsilon}_{t}^{2}}{N - 2} \;\text{over the}\; N \;\text{estimation-window days and a Student-t distribution with}\; N - 2 \;\text{degrees of freedom}
$$

**Also known as:** CAR analysis, abnormal returns analysis, market model event study.

**Args:**

- <u>event_date (str):</u> The date of the event (e.g. "2023-05-04"). Must fall
within the Toolkit instance's daily historical data; a date without
trading (a weekend or holiday) moves to the next trading day.
- <u>dependent_ticker (str &#124; None, optional):</u> The ticker being studied.
Defaults to the first ticker in the Toolkit instance.
- <u>column (str, optional):</u> The historical data column to use. Defaults to
"Return".
- <u>estimation_window (int, optional):</u> Number of trading days used to
estimate the market model. Defaults to 250 (~one trading year).
- <u>gap_days (int, optional):</u> Number of trading days between the end of the
estimation window and the event date. Defaults to 30.
- <u>pre_event_days (int, optional):</u> Number of trading days before the event
date included in the event window. Defaults to 10.
- <u>post_event_days (int, optional):</u> Number of trading days after the event
date included in the event window. Defaults to 10.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the
results to. Defaults to None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series: The Cumulative Abnormal Return (CAR), its t-statistic and
p-value, the market-model alpha and beta, and the number of estimation-
window observations used.

**Notes:**

- Always uses daily data -- event windows are measured in trading days, so
quarterly/yearly granularity would not be meaningful here.
- The market/benchmark return series is the Toolkit instance's `"Benchmark"`
column.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["NVDA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2022-01-01",
    end_date="2023-12-31",
)

# NVDA's abnormal return around its May 2023 earnings release
toolkit.econometrics.get_event_study(event_date="2023-05-25")
```

Which returns:

|                                |    Value |
|:-------------------------------|---------:|
| Cumulative Abnormal Return     |   0.2041 |
| CAR t-statistic                |   1.9464 |
| CAR p-value                    |   0.0527 |
| Alpha                          |   0.0018 |
| Beta                           |   2.0762 |
| Estimation Window Observations | 250      |

---

## get_arch_lm_test
Calculate Engle's Lagrange Multiplier (LM) test for ARCH effects, or the weighted portmanteau ARCH test of Fisher and Gallagher (2012).

The test regresses squared, mean-demeaned returns on `lags` of themselves and tests whether the resulting R-squared is significantly different from zero. A significant result (low p-value) indicates that the return series exhibits volatility clustering, and a GARCH-family model is an appropriate choice for it. A high p-value suggests fitting GARCH would not be meaningful, since there is no detectable time-varying volatility to model.

The formula is as follows:

$$
\epsilon_{t} = r_{t} - \operatorname{mean}(r),\;\; \text{the returns of period demeaned by their sample mean}
$$

$$
\text{Auxiliary regression:}\;\; \epsilon_{t}^{2} = a_{0} + \sum_{i=1}^{q} a_{i} \cdot \epsilon_{t-i}^{2} + u_{t},\;\; \text{with}\;\; q = \text{lags} \;(5 \;\text{by default})
$$

$$
\text{ARCH-LM} = (T - q) \cdot R^{2},\;\; \text{chi-squared with } q \text{ degrees of freedom},\;\; \text{where}\; T - q \;\text{is the number of observations in the auxiliary regression}
$$

$$
\text{weighted} = \text{True:} Q_{W} = T \cdot \sum_{k=1}^{q}\left(\frac{q - k + 1}{q}\right) \cdot \rho_{k}^{2},\;\; \text{with } \rho_{k} \text{ the autocorrelation of } \epsilon_{t}^{2} \text{ at lag } k,\;\; \text{and the p-value from the}\; \Gamma \;\text{distribution with shape} \;\frac{\frac{3(q + 1)^{2} q}{(4(2q^{2} + 3q + 1)) \;\text{and scale} \;2(2q^{2} + 3q + 1)}}{\operatorname{3q}(q + 1)},\;\; \text{which has the mean and variance of } Q_{W}
$$

The weighted test of Fisher and Gallagher (2012) gives the first lags the most weight, so a test over many lags is not diluted by the later ones and keeps its power; it is the ARCH test R's rugarch reports for a fitted GARCH model.

For more information about the method, see the following papers:

- Engle, R.F. (1982). "Autoregressive Conditional Heteroscedasticity with Estimates of the Variance of United Kingdom Inflation." Econometrica, 50(4), 987-1008.
- Fisher, T.J. and Gallagher, C.M. (2012). "New Weighted Portmanteau Statistics for Time Series Goodness of Fit Testing." Journal of the American Statistical Association, 107(498), 777-787.

**Also known as:** ARCH-LM test, Engle's ARCH test, weighted ARCH-LM test, McLeod-Li test.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>within_period (bool, optional):</u> Whether to calculate the test within the specified period or for
the entire period. Thus whether to look at the test within a specific year (if period = 'yearly')
or look at the entirety of all years. Defaults to False. Note that this requires intraday data
when period = 'daily', since a single day only nests observations when intraday data was fetched.
- <u>lags (int, optional):</u> The number of lags to test for ARCH effects. Defaults to 5.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the
assets tested. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.
- <u>weighted (bool, optional):</u> Whether to calculate the weighted portmanteau test of
Fisher and Gallagher (2012) instead of Engle's regression. Defaults to False.

**Returns:**

pd.DataFrame: The ARCH-LM (or weighted ARCH-LM) statistic and its p-value per asset.

**Notes:**

- The method retrieves historical return data based on the specified `period` and runs the ARCH-LM
test for each asset in the Toolkit instance.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["BTCUSD", "^GSPC", "EURUSD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_arch_lm_test()
```

Which returns:

|                   |   BTCUSD |   ^GSPC |   EURUSD |
|:------------------|---------:|--------:|---------:|
| ARCH-LM Statistic |  55.2071 | 165.389 |  67.7588 |
| P-Value           |   0      |   0     |   0      |

---

## get_jarque_bera_test
Calculate the Jarque-Bera test for normality.

The test combines sample skewness and excess kurtosis into a single statistic that is chi-squared distributed with 2 degrees of freedom under the null hypothesis that returns are normally distributed. A significant result (low p-value) indicates that returns are not normally distributed, which is relevant when choosing between e.g. gaussian and Student-T based Value at Risk models.

The formula is as follows:

$$
\text{JB} = \frac{n}{6} \cdot \left(S^{2} + \frac{(K - 3)^{2}}{4}\right),\;\; \text{chi-squared with 2 degrees of freedom}
$$

$$
S = \frac{m_{3}}{m_{2}^{\frac{3}{2}}}\;\;\text{and}\;\; K = \frac{m_{4}}{m_{2}^{2}},\;\; \text{with}\;\; m_{k} = \frac{1}{n} \cdot \sum(r_{t} - \operatorname{mean}(r))^{k} \;\text{the} \;(\text{biased}) \;\text{central moments of the returns of} \;\text{period}
$$

For more information about the method, see the following paper:

- Jarque, C.M. and Bera, A.K. (1987). "A Test for Normality of Observations and Regression Residuals." International Statistical Review, 55(2), 163-172.

**Also known as:** JB test, normality test.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>within_period (bool, optional):</u> Whether to calculate the test within the specified period or for
the entire period. Thus whether to look at the test within a specific year (if period = 'yearly')
or look at the entirety of all years. Defaults to False. Note that this requires intraday data
when period = 'daily', since a single day only nests observations when intraday data was fetched.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the
assets tested. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The Jarque-Bera statistic and its p-value per asset.

**Notes:**

- The method retrieves historical return data based on the specified `period` and runs the
Jarque-Bera test for each asset in the Toolkit instance.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["^GSPC", "BTCUSD", "TLT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_jarque_bera_test(period="monthly")
```

Which returns:

|                       |   ^GSPC |   BTCUSD |    TLT |
|:----------------------|--------:|---------:|-------:|
| Jarque-Bera Statistic |  2.6001 |   1.0834 | 0.6166 |
| P-Value               |  0.2725 |   0.5818 | 0.7347 |

---

## get_ljung_box_test
Calculate the Ljung-Box test for autocorrelation, or the weighted Ljung-Box test of Fisher and Gallagher (2012).

The test aggregates the squared Autocorrelation Function up to lag `h` into a single statistic that is chi-squared distributed with `h` degrees of freedom under the null hypothesis that the series exhibits no autocorrelation up to that lag. A significant result (low p-value) indicates that the series is autocorrelated, which is relevant both as a standalone diagnostic (e.g. to check whether a return series follows a random walk) and as a residual diagnostic after fitting a model (e.g. checking that GARCH residuals are no longer autocorrelated).

The formula is as follows:

$$
Q = n \cdot (n + 2) \cdot \sum_{k=1}^{h} \frac{\rho_{k}^{2}}{n - k},\;\; \text{chi-squared with } h \text{ degrees of freedom},\;\; h = \text{lags} \;(10 \;\text{by default})
$$

$$
\rho_{k} = \frac{\sum_{t=k+1}^{n}(r_{t} - \operatorname{mean}(r)) \cdot (r_{t-k} - \operatorname{mean}(r))}{\sum_{t=1}^{n}(r_{t} - \operatorname{mean}(r))^{2}},\;\; \text{the sample autocorrelation of the returns of period at lag } k
$$

$$
\text{weighted} = \text{True:} Q_{W} = \frac{n \cdot (n + 2) \cdot \sum_{k=1}^{h}\left(\frac{h - k + 1}{h}\right) \cdot \rho_{k}^{2}}{n - k},\;\; \text{with the p-value from the}\; \Gamma \;\text{distribution with shape} \;\frac{\frac{3(h + 1)^{2} h}{(4(2h^{2} + 3h + 1)) \;\text{and scale} \;2(2h^{2} + 3h + 1)}}{\operatorname{3h}(h + 1)},\;\; \text{which has the mean and variance of } Q_{W}
$$

The weighted test of Fisher and Gallagher (2012) gives the first lags the most weight, so a test over many lags is not diluted by the later ones and keeps its power; it is the Ljung-Box test R's rugarch reports for a fitted GARCH model.

For more information about the method, see the following papers:

- Ljung, G.M., & Box, G.E.P. (1978). "On a Measure of Lack of Fit in Time Series Models." Biometrika, 65(2), 297-303.
- Fisher, T.J. and Gallagher, C.M. (2012). "New Weighted Portmanteau Statistics for Time Series Goodness of Fit Testing." Journal of the American Statistical Association, 107(498), 777-787.

**Also known as:** Ljung-Box Q test, portmanteau test, weighted Ljung-Box test.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>within_period (bool, optional):</u> Whether to calculate the test within the specified period or for
the entire period. Thus whether to look at the test within a specific year (if period = 'yearly')
or look at the entirety of all years. Defaults to False. Note that this requires intraday data
when period = 'daily', since a single day only nests observations when intraday data was fetched.
- <u>lags (int, optional):</u> The number of lags to test for autocorrelation up to. Defaults to 10.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the
assets tested. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.
- <u>weighted (bool, optional):</u> Whether to calculate the weighted Ljung-Box test of
Fisher and Gallagher (2012). Defaults to False.

**Returns:**

pd.DataFrame: The Ljung-Box (or weighted Ljung-Box) statistic and its p-value per
asset.

**Notes:**

- The method retrieves historical return data based on the specified `period` and runs the
Ljung-Box test for each asset in the Toolkit instance.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["WMT", "COST", "TGT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_ljung_box_test()
```

Which returns:

|                     |     WMT |    COST |     TGT |
|:--------------------|--------:|--------:|--------:|
| Ljung-Box Statistic | 12.8794 | 10.9863 | 11.9887 |
| P-Value             |  0.2305 |  0.3586 |  0.2858 |

---

## get_variance_ratio_test
Calculate the Lo-MacKinlay Variance Ratio test for the random walk hypothesis.

The test compares the Variance of `q`-period (overlapping) returns, the sum of `q` consecutive returns, to `q` times the Variance of single-period returns. Under the random walk hypothesis these should be equal, giving a Variance Ratio of 1. A Variance Ratio above 1 with a significant (low) p-value indicates positive autocorrelation (momentum/trending behavior), while a Variance Ratio below 1 with a significant p-value indicates negative autocorrelation (mean-reversion).

The result holds two statistics. The homoskedastic z(q) assumes a constant volatility; daily returns cluster in volatility, and under such heteroskedasticity z(q) rejects the random walk too often. The heteroskedasticity-robust z*(q) of Lo and MacKinlay stays valid when volatility clusters and is the safer reading for returns. `get_arch_lm_test` shows whether a series has that volatility clustering.

The formula is as follows:

$$
\operatorname{VR}(q) = \frac{\sigma^{2}(q)}{\sigma^{2}(1)},\;\; \text{with}\;\; \sigma^{2}(1) = \frac{\sum(r_{t} - \mu)^{2}}{n - 1}\;\;\text{and}\;\; \sigma^{2}(q) = \frac{\sum(r_{t} + \ldots + r_{t-q+1} - q \cdot \mu)^{2}}{m} \;\text{over the overlapping q-period sums},\;\; m = q \cdot (n - q + 1) \cdot \left(1 - \frac{q}{n}\right) \;\text{and}\; \mu \;\text{the mean return} \;(\text{the unbiased estimators of Lo}\; \text{\&} \;\text{MacKinlay}),\;\; q = 2 \;\text{by default}
$$

$$
z(q) = \frac{\operatorname{VR}(q) - 1}{\sqrt{\phi(q)}},\;\; \text{with}\;\; \phi(q) = \frac{2 \cdot (2q - 1) \cdot (q - 1)}{3q \cdot n}
$$

$$
z^{*}(q) = \frac{\sqrt{n} \cdot (\operatorname{VR}(q) - 1)}{\sqrt{\theta(q)}},\;\; \text{with}\;\; \theta(q) = \sum_{k=1}^{q-1} 4 \cdot \left(1 - \frac{k}{q}\right)^{2} \cdot \delta(k)\;\;\text{and}\;\; \delta(k) = \frac{n \cdot \sum_{t=k+1}^{n}(r_{t} - \mu)^{2} \cdot (r_{t-k} - \mu)^{2}}{(\sum_{t=1}^{n}(r_{t} - \mu)^{2})^{2}}
$$

$$
\text{P-Value} = 2 \cdot (1 - \Phi(\left|z\right|)) \;\text{for both statistics},\;\; \text{with } \Phi \text{ the standard normal CDF}
$$

For more information about the method, see the following paper:

- Lo, A.W., & MacKinlay, A.C. (1988). "Stock Market Prices Do Not Follow Random Walks: Evidence from a Simple Specification Test." Review of Financial Studies, 1(1), 41-66.

**Also known as:** Lo-MacKinlay test, VR test.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>within_period (bool, optional):</u> Whether to calculate the test within the specified period or for
the entire period. Thus whether to look at the test within a specific year (if period = 'yearly')
or look at the entirety of all years. Defaults to False. Note that this requires intraday data
when period = 'daily', since a single day only nests observations when intraday data was fetched.
- <u>q (int, optional):</u> The number of periods to sum returns over. Defaults to 2.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the
assets tested. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The Variance Ratio, the homoskedastic test statistic and its p-value,
and the heteroskedasticity-robust test statistic and its p-value per asset.

**Notes:**

- The method retrieves historical return data based on the specified `period` and runs the
Variance Ratio test for each asset in the Toolkit instance.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["XLE", "XLF", "XLK"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_variance_ratio_test()
```

Which returns:

|                                 |    XLE |    XLF |     XLK |
|:--------------------------------|-------:|-------:|--------:|
| Variance Ratio                  | 1.0249 | 1.0249 |  0.9611 |
| Variance Ratio Statistic        | 0.8815 | 0.8805 | -1.3774 |
| P-Value                         | 0.3781 | 0.3786 |  0.1684 |
| Robust Variance Ratio Statistic | 0.6193 | 0.6256 | -0.9679 |
| Robust P-Value                  | 0.5358 | 0.5316 |  0.3331 |

---

## get_cusum_test
Calculate a CUSUM test for the stability of the returns over time: the CUSUM of the OLS residuals of Ploberger and Krämer (1992), the CUSUM of the recursive residuals of Brown, Durbin and Evans (1975) or the CUSUM of the log price of Chu, Stinchcombe and White (1996).

method="ols" fits a constant-mean model to the returns and cumulates the (scaled) OLS residuals into a path that behaves like a Brownian Bridge under the null hypothesis of a stable mean. A stable mean keeps the path close to zero, while a mean shift partway through the series (a structural break, e.g. a regime change) drags the path away from zero; the test statistic is the maximum absolute value of that path.

method="recursive" cumulates the one-step-ahead forecast errors of the mean return, each from the returns before it (the recursive residuals). Under a stable mean they are independent, so their path is a Brownian motion; a break makes the errors after it share a sign and the path drifts out of two lines that widen with time. It reacts to a break later in the sample better than the OLS version, which compares every return with the mean of the whole sample.

method="chu_stinchcombe_white" asks whether the log price has risen by more since an earlier date than a random walk with the volatility up to now allows, the structural break test López de Prado (2018) uses on prices. It is one-sided: it detects a rise, such as a breakout or a bubble. With `time_series=True` it gives the statistic, its critical value and the verdict per date, each from the returns up to that date only.

The formula is as follows, with $$r_{t}$$ the returns of `period` and n the number of returns:

$$
\text{method} = \text{"ols":} \hat{e}_{t} = r_{t} - \operatorname{mean}(r),\;\; \text{CUSUM} = \max \;\text{over}\; k \;\text{of} \;\frac{\left|\sum_{t=1}^{k} \hat{e}_{t}\right|}{\hat{\sigma} \cdot \sqrt{n}},\;\; \text{with}\;\; \hat{\sigma}^{2} = \frac{\sum \hat{e}_{t}^{2}}{n - 1},\;\; \text{and}\;\; \text{P-Value} = P(\sup \left|B(s)\right| > \text{CUSUM}) \;\text{for a Brownian Bridge}\; B \;(\text{the Kolmogorov distribution})
$$

$$
\text{method} = \text{"recursive":} w_{t} = \frac{r_{t} - \operatorname{mean}(r_{1} \ldots r_{t-1})}{\sqrt{1 + \frac{1}{t - 1}}} \;\text{for}\; t = 2 \ldots n,\;\; W_{j} = \frac{\sum_{t=2}^{j} w_{t}}{\hat{\sigma}} \;\text{with}\; \hat{\sigma}^{2} = \frac{\sum w_{t}^{2}}{n - 1},\;\; \text{CUSUM} = \max \;\text{over}\; j \;\text{of} \;\frac{\left|W_{j}\right|}{\sqrt{n - 1} + \frac{2(j - 1)}{\sqrt{n - 1}}}\;\;\text{and}\;\; \text{P-Value} = 2 \cdot (1 - \Phi(3 \cdot \text{CUSUM}) + \exp(- 4 \cdot \text{CUSUM}^{2}) \cdot \Phi(\text{CUSUM})),\;\; \text{the probability that a Brownian motion crosses the lines} \;\pm \;\text{CUSUM} \cdot \left(\sqrt{n - 1} + \frac{2(j - 1)}{\sqrt{n - 1}}\right)
$$

$$
\text{method} = \text{"chu\_stinchcombe\_white":} y_{t} = \sum \ln(1 + r_{t}),\;\; \text{the log price},\;\; S_{n,t} = \frac{y_{t} - y_{n}}{\hat{\sigma}_{t} \cdot \sqrt{t - n}} \;\text{with}\; \hat{\sigma}_{t}^{2} \;\text{the mean of the squared changes of}\; y \;\text{up to}\; t,\;\; \text{CUSUM} = \max \;\text{over}\; n < t \;\text{of}\; S_{n,t} \;\text{at the last date}\; t \;\text{and its critical value} \;\sqrt{4.6 + \ln(t - n)} \;\text{at that}\; n (5\%)
$$

- Stability is rejected at 5% when the p-value is below 0.05 (or the CUSUM above its critical value)

For more information about the method, see the following papers:

- Ploberger, W., & Kramer, W. (1992). "The CUSUM Test with OLS Residuals." Econometrica, 60(2), 271-285.
- Brown, R.L., Durbin, J. and Evans, J.M. (1975). "Techniques for Testing the Constancy of Regression Relationships over Time." Journal of the Royal Statistical Society, Series B, 37(2), 149-192.
- Chu, C.-S.J., Stinchcombe, M. and White, H. (1996). "Monitoring Structural Change." Econometrica, 64(5), 1045-1065.
- Homm, U. and Breitung, J. (2012). "Testing for Speculative Bubbles in Stock Markets: A Comparison of Alternative Methods." Journal of Financial Econometrics, 10(1), 198-231.
- López de Prado, M. (2018). "Advances in Financial Machine Learning." Wiley, section 17.3 (17.3.2 for the Chu-Stinchcombe-White test).
- Referenced against statsmodels' breaks_cusumolsresid and recursive_olsresiduals.

**Also known as:** CUSUM test, CUSUM of OLS residuals test, Ploberger-Kramer test, recursive CUSUM test, Brown-Durbin-Evans test, Chu-Stinchcombe-White test, CSW CUSUM, structural break test.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>within_period (bool, optional):</u> Whether to calculate the test within the specified period or for
the entire period. Thus whether to look at the test within a specific year (if period = 'yearly')
or look at the entirety of all years. Defaults to False. Note that this requires intraday data
when period = 'daily', since a single day only nests observations when intraday data was fetched.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the
assets tested. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.
- <u>method (Literal["ols", "recursive", "chu_stinchcombe_white"], optional):</u> The CUSUM of the OLS
residuals, of the recursive residuals or of the log price. Defaults to "ols".
- <u>time_series (bool, optional):</u> Whether to return the statistic, its critical value and
whether stability is rejected per date (method="chu_stinchcombe_white" only, as the
other two scale their path with the whole sample). Defaults to False.

**Returns:**

pd.DataFrame: The CUSUM statistic, its p-value, the number of observations used, the
1%/5%/10% critical values, and whether stability is rejected at the 5% level, per
asset; for method="chu_stinchcombe_white" the statistic, its 5% critical value, the
observations and the verdict at the last date, or with time_series=True per date. An
asset with fewer than 10 observations has NaN values.

**Notes:**

- The method retrieves historical return data based on the specified `period` and runs the
CUSUM test for each asset in the Toolkit instance.
- statsmodels' recursive_olsresiduals scales the recursive path with the standard
deviation of the recursive residuals around their mean; Brown, Durbin and Evans (1975)
use the residual variance of the full-sample fit, as here. The Chu-Stinchcombe-White
statistic divides by the volatility $$\hat{\sigma}_{t}$$ and $$\hat{\sigma}_{t}^{2}$$ averages the t - 1 squared changes, as in
López de Prado (2018, section 17.3.2).
- The critical value of the Chu-Stinchcombe-White test is the 5% value Homm and Breitung
(2012) simulated; it has no p-value.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["BA", "AIR.PA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

# The critical values are the asymptotic Brownian Bridge boundaries, so they
# are the same constants for every asset.
toolkit.econometrics.get_cusum_test()
```

Which returns:

|                       |        BA |    AIR.PA |
|:----------------------|----------:|----------:|
| CUSUM Statistic       |    0.6789 |    0.4439 |
| P-Value               |    0.746  |    0.9892 |
| Observations          | 1254      | 1280      |
| Critical Value 1%     |    1.63   |    1.63   |
| Critical Value 5%     |    1.36   |    1.36   |
| Critical Value 10%    |    1.22   |    1.22   |
| Reject Stability (5%) |    0      |    0      |

---

## get_sign_bias_test
Calculate the sign bias test of Engle and Ng (1993) on the standardized residuals of a GARCH-family model fitted to the returns: does a fall raise the volatility by more than the model expects (sign bias), and do large falls or large rises (negative and positive size bias)?

A symmetric GARCH(1, 1) lets a fall and a rise of the same size raise the volatility equally. In equity returns falls tend to raise it by more (the leverage effect), so after a fall the squared standardized residuals stay larger than the model expects. The test regresses them on the sign and the size of the shock before them; a significant sign or negative size bias says the model misses that asymmetry and an asymmetric model, such as method="gjr" or method="aparch", fits better.

The formula is as follows:

$$
e_{t} \;\text{the residuals of the} \;\text{mean} \;\text{model and}\; z_{t} = \frac{e_{t}}{\sigma_{t} \;\text{the standardized residuals of the GARCH-family} \;\text{method} \;(\operatorname{GARCH}(1,\; 1) \;\text{by default}) \;\text{fitted to the returns of} \;\text{period}},\;\; \text{see toolkit.risk.get\_garch}
$$

$$
z_{t}^{2} = c_{0} + c_{1} \cdot S^{-} \;\text{}_{t-1} + c_{2} \cdot S^{-} \;\text{}_{t-1} \cdot e_{t-1} + c_{3} \cdot S^{+} \;\text{}_{t-1} \cdot e_{t-1} + u_{t} \;\text{by OLS},\;\; \text{with}\;\; S^{-} \;\text{}_{t-1} = 1 \;\text{when}\; e_{t-1} < 0 \;\text{and 0 otherwise and}\; S^{+} \;\text{}_{t-1} = 1 - S^{-} \;\text{}_{t-1}
$$

- Sign Bias, Negative Size Bias and Positive Size Bias: the t-statistics of $$c_{1}$$, $$c_{2}$$ and $$c_{3}$$, with two-sided p-values from the t-distribution with n - 4 degrees of freedom

$$
\text{Joint Statistic} = n \cdot R^{2},\;\; \text{chi-squared with 3 degrees of freedom, with } n \text{ the observations of the regression}
$$

For more information about the method, see the following paper:

- Engle, R.F. and Ng, V.K. (1993). "Measuring and Testing the Impact of News on Volatility." The Journal of Finance, 48(5), 1749-1778.
- Referenced against signbias of R's rugarch ([https://cran.r-project.org/package=rugarch](https://cran.r-project.org/package=rugarch){:target="_blank"}), whose t-statistics in the rugarch vignette it reproduces.

**Also known as:** sign bias test, Engle-Ng test, size bias test, leverage effect test, asymmetric volatility test, GARCH residual diagnostics.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>method (str, optional):</u> The GARCH-family model fitted to the returns, see
`toolkit.risk.get_garch` (e.g. "garch", "gjr", "aparch"). Defaults to "garch".
- <u>distribution (str, optional):</u> The innovation distribution of the model ("normal", "t",
"skewt", "skewt_fernandez_steel", "ged" or "johnson_su"). Defaults to "normal".
- <u>mean (str, optional):</u> The mean model ("zero", "constant", "arma" or "in_mean").
Defaults to "zero".
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the
assets tested. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The t-statistic and p-value of the sign bias, negative size bias and
positive size bias, the joint statistic and its p-value, and the observations of the
regression, per asset.

**Notes:**

- Every asset is fitted on its own returns, as in `toolkit.risk.get_garch`; the
fit takes a second or more per asset of daily returns.
- rugarch reports the absolute t-statistics and a Wald statistic as the joint test; the
signed t-statistics show the direction (a negative size bias is negative when
larger falls raise the volatility by more) and the joint statistic is the $$n \cdot R^{2}$$ of
Engle and Ng (1993).

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["^GSPC", "GLD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2016-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_sign_bias_test()
```

Which returns:

|                                |     ^GSPC |       GLD |
|:-------------------------------|----------:|----------:|
| Sign Bias t-Statistic          |    3.9418 |    0.6116 |
| Sign Bias P-Value              |    0.0001 |    0.5409 |
| Negative Size Bias t-Statistic |   -0.0432 |    1.864  |
| Negative Size Bias P-Value     |    0.9656 |    0.0624 |
| Positive Size Bias t-Statistic |   -0.0972 |    0.066  |
| Positive Size Bias P-Value     |    0.9225 |    0.9474 |
| Joint Statistic                |   27.0353 |    3.8098 |
| Joint P-Value                  |    0      |    0.2827 |
| Observations                   | 2512      | 2512      |

---

## get_pearson_goodness_of_fit_test
Calculate the adjusted Pearson goodness of fit test of Palm (1996) and Vlaar and Palm (1993) on the standardized residuals of a GARCH-family model fitted to the returns: do they follow the innovation distribution the model assumes?

Each standardized residual is turned into the probability of a value at most as large under the fitted distribution, which is uniform between 0 and 1 when the distribution fits. The probabilities are counted in equally wide bins and the counts compared with the equal number every bin should hold. Daily returns have fatter tails than a GARCH model with normal innovations allows, so the test usually rejects the normal distribution; a Student-t (distribution="t") or skewed Student-t fits better when its p-value is larger.

The formula is as follows:

- $$z_{t}$$ the standardized residuals of the GARCH-family `method` (GARCH(1, 1) by default) with the `distribution` and `mean` model fitted to the returns of `period`, see `toolkit.risk.get_garch`

$$
u_{t} = F(z_{t}),\;\; \text{with } F \text{ the distribution function of the fitted standardized innovation distribution (with its fitted Shape and Skew)}
$$

$$
n_{i} = \text{the number of}\; u_{t} \;\text{in} \;\left[\frac{i - 1}{g},\; \frac{i}{\text{g)}} \;\text{for}\; i = 1 \ldots g\right],\;\; \text{with}\;\; g = \text{bins} \;(20 \;\text{by default})
$$

$$
\text{Pearson Statistic} = \frac{\sum_{i=1}^{g}\left(n_{i} - \frac{n}{g}\right)^{2}}{\frac{n}{g}},\;\; \text{chi-squared with}\; g - 1 \;\text{degrees of freedom}
$$

For more information about the method, see the following papers:

- Palm, F.C. (1996). "GARCH Models of Volatility." In Handbook of Statistics, Vol. 14, Elsevier, 209-240.
- Vlaar, P.J.G. and Palm, F.C. (1993). "The Message in Weekly Exchange Rates in the European Monetary System: Mean Reversion, Conditional Heteroscedasticity, and Jumps." Journal of Business & Economic Statistics, 11(3), 351-360.
- Referenced against gof of R's rugarch ([https://cran.r-project.org/package=rugarch](https://cran.r-project.org/package=rugarch){:target="_blank"}), which reports it for 20, 30, 40 and 50 bins.

**Also known as:** adjusted Pearson goodness of fit test, chi-squared goodness of fit test, probability integral transform test, GARCH distribution test, GARCH residual diagnostics.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>bins (int, optional):</u> The number of equally wide bins of the probabilities. Defaults to 20.
- <u>method (str, optional):</u> The GARCH-family model fitted to the returns, see
`toolkit.risk.get_garch` (e.g. "garch", "gjr", "aparch"). Defaults to "garch".
- <u>distribution (str, optional):</u> The innovation distribution of the model and of the test
("normal", "t", "skewt", "skewt_fernandez_steel", "ged" or "johnson_su"). Defaults
to "normal".
- <u>mean (str, optional):</u> The mean model ("zero", "constant", "arma" or "in_mean").
Defaults to "zero".
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the
assets tested. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The Pearson statistic, its p-value, the number of bins and the
observations, per asset.

**Notes:**

- Every asset is fitted on its own returns, as in `toolkit.risk.get_garch`; the
fit takes a second or more per asset of daily returns.
- The parameters of the distribution are estimated with the model, which makes the
chi-squared p-value somewhat too large (Palm, 1996); read it as a guide.
- rugarch leaves the empty bins above the highest occupied bin out of the sum; every
empty bin counts here.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["^GSPC", "GLD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2016-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_pearson_goodness_of_fit_test(distribution="t")
```

Which returns:

|                   |     ^GSPC |       GLD |
|:------------------|----------:|----------:|
| Pearson Statistic |   82.4238 |   44.302  |
| P-Value           |    0      |    0.0009 |
| Bins              |   20      |   20      |
| Observations      | 2513      | 2513      |

---

## get_nyblom_test
Calculate the parameter stability test of Nyblom (1989) and Hansen (1992) on a GARCH-family model fitted to the returns: did its parameters stay the same over the sample, or did the volatility process change (a calmer or more turbulent regime, a change in how quickly shocks fade)?

At the maximum of the likelihood the scores of every parameter (the derivatives of the log-likelihood of each return) sum to zero over the whole sample. When a parameter changes during the sample, their running sum wanders far from zero in between. The test measures that wandering for every parameter on its own and for all of them together, relative to the variance of the scores.

The formula is as follows:

- $$s_{t}$$ the scores of return t: the derivatives of its log-likelihood with respect to the parameters of the GARCH-family `method` (GARCH(1, 1) by default) with the `distribution` and `mean` model fitted to the returns of `period`, see `toolkit.risk.get_garch_parameters`

$$
S_{t} = \sum_{i=1}^{t} s_{i}\;\;\text{and}\;\; V = \sum_{t} s_{t} \cdot s_{t}',\;\; \text{with } T \text{ the number of returns in the likelihood}
$$

$$
\text{Individual Statistic of parameter}\; j = \frac{\sum_{t} S_{t,j}^{2}}{T \cdot V_{jj}}
$$

$$
\text{Joint Statistic} = \frac{\sum_{t} S_{t}' \cdot V^{- 1} \cdot S_{t}}{T}
$$

$$
\text{P-values from the limiting distribution},\;\; \sum_{j=1}^{k} \;\text{∫} \;B_{j}(r)^{2} \,\mathrm{d}r \;\text{over}\; k \;\text{independent Brownian bridges},\;\; \text{with}\;\; k = 1 \;\text{for an individual statistic and the number of parameters for the joint statistic},\;\; \text{by Imhof's (1961) integral}
$$

Large statistics (small p-values) say the parameter is not stable. A parameter that the fit leaves on a bound of its search (such as an Omega or Alpha of 0) has scores that do not sum to zero, which inflates its statistic and the joint statistic.

For more information about the method, see the following papers:

- Nyblom, J. (1989). "Testing for the Constancy of Parameters Over Time." Journal of the American Statistical Association, 84(405), 223-230.
- Hansen, B.E. (1992). "Testing for Parameter Instability in Linear Models." Journal of Policy Modeling, 14(4), 517-533.
- Referenced against nyblom of R's rugarch ([https://cran.r-project.org/package=rugarch](https://cran.r-project.org/package=rugarch){:target="_blank"}), which compares the statistics with Hansen's tabulated critical values (0.470 for one parameter at 5%); the critical values here are those of the limiting distribution itself (0.461 for one parameter, the 5% point of the Cramér-von Mises distribution).

**Also known as:** Nyblom test, Hansen stability test, parameter constancy test, parameter instability test, GARCH stability test, structural change in GARCH.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>method (str, optional):</u> The GARCH-family model fitted to the returns, see
`toolkit.risk.get_garch` (e.g. "garch", "gjr", "aparch"). Defaults to "garch".
- <u>distribution (str, optional):</u> The innovation distribution of the model ("normal", "t",
"skewt", "skewt_fernandez_steel", "ged" or "johnson_su"). Defaults to "normal".
- <u>mean (str, optional):</u> The mean model ("zero", "constant", "arma", "in_mean" or
"arfima"). Defaults to "zero".
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the
assets tested. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The joint statistic, its p-value and 5% critical value, the statistic and
p-value of every parameter, the 5% critical value of one parameter and the observations,
per asset.

**Notes:**

- Every asset is fitted on its own returns, as in `toolkit.risk.get_garch`; the fit takes a
second or more per asset of daily returns.
- The scores are central finite differences of the log-likelihood, as for the robust
standard errors of `toolkit.risk.get_garch_parameters(diagnostics=True)`.
- The test is conservative on a fitted GARCH: on 500 simulated GARCH(1, 1) samples of 1,000
observations with normal innovations, refitted each time, the joint test at 5% rejects about 2% of
the time and those of Omega, Alpha and Beta 2% to 2.6%, so a rejection is a strong signal and a
parameter change of moderate size can go unnoticed.
- method="realized" needs a realized measure the test does not take; use the other models.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["^GSPC", "GLD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2016-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_nyblom_test()
```

Which returns:

|                                |     ^GSPC |       GLD |
|:-------------------------------|----------:|----------:|
| Joint Statistic                |    1.2495 |    1.2938 |
| Joint P-Value                  |    0.0164 |    0.0134 |
| Joint Critical Value (5%)      |    1.0002 |    1.0002 |
| Omega Statistic                |    0.4851 |    0.4856 |
| Omega P-Value                  |    0.0435 |    0.0433 |
| Alpha Statistic                |    0.3316 |    0.4274 |
| Alpha P-Value                  |    0.1104 |    0.0612 |
| Beta Statistic                 |    0.682  |    0.3219 |
| Beta P-Value                   |    0.0141 |    0.1174 |
| Individual Critical Value (5%) |    0.4614 |    0.4614 |
| Observations                   | 2513      | 2513      |

---

## get_gmm_moment_test
Calculate the GMM orthogonality test of Hansen (1982) on the standardized residuals of a GARCH-family model fitted to the returns: do they have the mean, variance, skewness and kurtosis of the innovation distribution the model assumes, and are their squares, cubes and fourth powers free of autocorrelation?

A correctly specified model leaves standardized residuals that are independent draws from its innovation distribution, so a set of moments has a known value. Each moment is tested on its own with a t-statistic; the autocorrelations of the squares (Q2: volatility clustering the model misses), cubes (Q3) and fourth powers (Q4) and all conditions together are tested with Wald statistics.

The formula is as follows:

- $$z_{t}$$ the standardized residuals of the GARCH-family `method` (GARCH(1, 1) by default) with the `distribution` and `mean` model fitted to the returns of `period`, see `toolkit.risk.get_garch`, and s and $$\kappa$$ the skewness and kurtosis (not excess) of the fitted innovation distribution

$$
\text{Mean:}\;\; E\left[z_{t}\right] = 0;\;\; \text{Variance:}\;\; E\left[z_{t}^{2} - 1\right] = 0;\;\; \text{Skewness:}\;\; E\left[z_{t}^{3} - s\right] = 0;\;\; \text{Kurtosis:}\;\; E\left[z_{t}^{4} - \kappa\right] = 0
$$

$$
\text{Q2:}\;\; E\left[(z_{t}^{2} - 1) (z_{t-j}^{2} - 1)\right] = 0,\;\; \text{Q3:}\;\; E\left[(z_{t}^{3} - s) (z_{t-j}^{3} - s)\right] = 0\;\;\text{and}\;\; \text{Q4:}\;\; E\left[(z_{t}^{4} - \kappa) (z_{t-j}^{4} - \kappa)\right] = 0 \;\text{for}\; j = 1,\; \ldots,\; \text{lags}
$$

- $$g_{t}$$ the conditions of return t over the T returns after the first `lags` and ḡ their average

$$
S \text{ their covariance under the null of independent innovations:}\;\; \text{m\_\{a+\}ᵦ} - m_{a} \cdot \text{mᵦ} \;\text{between the Mean, Variance, Skewness and Kurtosis conditions} \;(\text{powers a and}\; b),\;\; \text{with}\;\; m_{k} = E\left[z^{k}\right] \;\text{of the fitted innovation distribution},\;\; (E [a_{t} \cdot c_{t}])^{2} \text{ between the products of the centred powers a and } c \text{ at the same lag, and 0 between different lags and between the moments and the products}
$$

$$
\text{t-Statistic} = \frac{\bar{g}_{i}}{\sqrt{\frac{S_{ii}}{T}}},\;\; \text{with two-sided p-values from the normal distribution}
$$

$$
\text{Q2},\;\; Q_{3} \;\text{and Q4 Statistic} = T \cdot \bar{g}' \cdot S^{- 1} \cdot \bar{g} \;\text{over their} \;\text{lags} \;\text{conditions},\;\; \text{chi-squared with lags degrees of freedom};\;\; \text{Joint Statistic over all}\; 4 + 3 \cdot \text{lags} \;\text{conditions},\;\; \text{chi-squared with}\; 4 + 3 \cdot \text{lags} \;\text{degrees of freedom}
$$

For more information about the method, see the following paper:

- Hansen, L.P. (1982). "Large Sample Properties of Generalized Method of Moments Estimators." Econometrica, 50(4), 1029-1054.
- Referenced against GMMTest of R's rugarch ([https://cran.r-project.org/package=rugarch](https://cran.r-project.org/package=rugarch){:target="_blank"}) as its documentation defines the conditions M1 to M4, Q2 to Q4 and the joint J test, with the covariance of the lagged conditions under the null (see the Notes).

**Also known as:** GMM orthogonality test, moment test, Hansen J test of standardized residuals, GARCH residual diagnostics, conditional moment test.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>lags (int, optional):</u> The number of lags of the Q2, Q3 and Q4 conditions. Defaults to 1.
- <u>method (str, optional):</u> The GARCH-family model fitted to the returns, see
`toolkit.risk.get_garch` (e.g. "garch", "gjr", "aparch"). Defaults to "garch".
- <u>distribution (str, optional):</u> The innovation distribution of the model and of its
skewness and kurtosis ("normal", "t", "skewt", "skewt_fernandez_steel", "ged" or
"johnson_su"). Defaults to "normal".
- <u>mean (str, optional):</u> The mean model ("zero", "constant", "arma", "in_mean" or
"arfima"). Defaults to "zero".
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the
assets tested. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The t-statistic and p-value of the Mean, Variance, Skewness and Kurtosis
conditions, the Q2, Q3, Q4 and Joint statistics with their p-values, the lags and the
observations, per asset.

**Notes:**

- Every asset is fitted on its own returns, as in `toolkit.risk.get_garch`.
- The parameters are estimated, which the covariance of the conditions leaves out (as in
rugarch), so read the p-values as a guide.
- The conditions are correlated ($$z_{t}$$ with $$z_{t}^{3}$$, $$z_{t}^{2}$$ with $$z_{t}^{4}$$, Q2 with Q4), so the joint test can reject
while none of the individual tests does: a negative skewness without the fatter tails that usually
come with it is such a combination.
- The covariance of the conditions is the one the null implies, where rugarch takes the sample covariance
of all conditions. That sample covariance rests on 8th and 16th moments of the residuals: on simulated
normal innovations its joint test at 5% rejects about 20% of the time at 2,500 observations, against
about 5% here (7% at 1,000).
- The Kurtosis condition needs a finite 8th moment of the innovations (a Student-t with a Shape above
8); with a fitted Shape of 8 or less its variance is the sample one, and its test and the joint test
reject too often.
- On the residuals of a fitted GARCH(1, 1) with normal innovations, the Variance condition is close to
zero by construction (the score of Omega is a weighted sum of $$z_{t}^{2} - 1$$), so its test, and the Kurtosis
test that moves with it, hardly ever reject.
- A Student-t with a Shape of 4 or less has no kurtosis (3 or less: no skewness); its Kurtosis
and Q4 (Skewness and Q3) conditions are then NaN and left out of the joint statistic.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["^GSPC", "GLD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2016-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_gmm_moment_test(distribution="t")
```

Which returns:

|                      |     ^GSPC |       GLD |
|:---------------------|----------:|----------:|
| Mean t-Statistic     |    2.8645 |    3.1991 |
| Mean P-Value         |    0.0042 |    0.0014 |
| Variance t-Statistic |    0.0518 |   -0.2087 |
| Variance P-Value     |    0.9587 |    0.8347 |
| Skewness t-Statistic |   -3.1211 |   -0.0336 |
| Skewness P-Value     |    0.0018 |    0.9732 |
| Kurtosis t-Statistic |   -0.9237 |   -2.5345 |
| Kurtosis P-Value     |    0.3556 |    0.0113 |
| Q2 Statistic         |    0.8937 |    0.3027 |
| Q2 P-Value           |    0.3445 |    0.5822 |
| Q3 Statistic         |    0.0555 |    0.0347 |
| Q3 P-Value           |    0.8138 |    0.8522 |
| Q4 Statistic         |    0.0295 |    0.0019 |
| Q4 P-Value           |    0.8635 |    0.9654 |
| Joint Statistic      |  -26.0374 |  386.094  |
| Joint P-Value        |    1      |    0      |
| Lags                 |    1      |    1      |
| Observations         | 2512      | 2512      |

---

## get_markov_regime_switching
Fit a Markov regime switching model to every asset: the mean and volatility of its returns depend on a regime that is not observed and switches from one period to the next with fixed probabilities (Hamilton, 1989). With two regimes the model typically separates calm markets (a higher mean and a low volatility) from turbulent ones (a lower mean and a high volatility), and it says which regime the market is most likely in today, how persistent each regime is and how long it lasts on average.

The regimes are ordered from the lowest to the highest volatility, so Regime 1 is the calmest. With switching_variance=False all regimes share one volatility, and they are ordered from the lowest to the highest mean instead, so Regime 1 is the one with the lowest mean. The expected duration of a regime is 1 / (1 - p), with p the probability of staying in it, in periods. The share is the part of the periods in which the regime was the most likely one.

The likelihood of a mixture of regimes has local optima, so the model is fitted from its default starting values and from the best of 20 random perturbations of them, and the fit with the highest likelihood is kept. The random perturbations come from NumPy's global random state, so when competing optima are close, repeated calls can differ slightly; call np.random.seed beforehand for results that can be reproduced.

The formula is as follows:

$$
y_{t} = \mu_{S_{t}} + \sigma_{S_{t}} \cdot \epsilon_{t},\;\; \text{with } y_{t} \text{ the column series (Return by default)},\;\; \epsilon_{t} \;\text{standard normal and}\; S_{t} \in \{1,\; \ldots,\; K\} \;\text{the regime},\;\; K = \text{regimes} \;(2 \;\text{by default});\;\; \sigma_{S_{t}} = \sigma \;\text{for every regime when}\; \text{switching\_variance} = \text{False}
$$

$$
P(S_{t} = j \mid S_{t-1} = i) = p_{ij},\;\; \text{a first-order Markov chain with constant transition probabilities}
$$

- $$\mu$$, $$\sigma$$ and $$p_{ij}$$ are fitted by Maximum Likelihood with the Hamilton filter (statsmodels MarkovRegression), keeping the best of the default start and 20 random perturbations

$$
\text{Smoothed probabilities} \;P(S_{t} = j \mid y_{1} \ldots y_{T}) \;\text{per date};\;\; \text{Expected Duration} = \frac{1}{1 - p_{jj}} \;\text{periods};\;\; \text{Share} = \text{the fraction of dates where regime}\; j \;\text{has the highest smoothed probability};\;\; \text{Current Regime} = \text{that regime on the last date},\;\; \text{with its smoothed probability}
$$

For more information, see the following paper:

- Hamilton, J.D. (1989). "A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle." Econometrica, 57(2), 357-384.

**Also known as:** Markov switching model, hidden Markov model, regime detection, bull and bear regimes.

**Args:**

- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or
yearly). Defaults to "daily".
- <u>column (str, optional):</u> The historical data column to model. Defaults to "Return".
- <u>regimes (int, optional):</u> The number of regimes. Defaults to 2.
- <u>switching_variance (bool, optional):</u> Whether the volatility switches with the
regime as well as the mean. Defaults to True.
- <u>probabilities (bool, optional):</u> Whether to return the smoothed probability of
every regime per date instead of the summary. Defaults to False.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the
assets. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per asset the Mean, Volatility, Probability of Staying, Expected
Duration and Share of every regime, and the Current Regime with its probability;
or, with probabilities=True, the probability of every regime per date.

**Notes:**

- Requires statsmodels (`pip install financetoolkit[econometrics]`).

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2015-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_markov_regime_switching(period="weekly")
```

Which returns:

|                                 |    AAPL |    MSFT |
|:--------------------------------|--------:|--------:|
| Regime 1 Mean                   |  0.009  |  0.0065 |
| Regime 1 Volatility             |  0.0236 |  0.0217 |
| Regime 1 Probability of Staying |  0.917  |  0.9528 |
| Regime 1 Expected Duration      | 12.0479 | 21.194  |
| Regime 1 Share                  |  0.5436 |  0.6411 |
| Regime 2 Mean                   |  0.0006 |  0.0021 |
| Regime 2 Volatility             |  0.0488 |  0.0455 |
| Regime 2 Probability of Staying |  0.91   |  0.9209 |
| Regime 2 Expected Duration      | 11.1105 | 12.6346 |
| Regime 2 Share                  |  0.4564 |  0.3589 |
| Current Regime                  |  1      |  1      |
| Current Regime Probability      |  0.8877 |  0.8087 |

---

## get_structural_breaks
Find the dates at which the mean of every asset's series shifts, with the Bai and Perron (1998, 2003) method for multiple structural breaks. For every number of breaks the break dates that minimize the sum of squared residuals around a mean per segment are found exactly (by dynamic programming), and the number of breaks is chosen by the Bayesian information criterion. Every segment covers at least a share of the observations (the integer part of that share times the number of observations, as in Bai and Perron), so a break is not fitted to a few outliers.

The BIC works well for series without serial correlation, such as returns, but tends to choose too many breaks when the series is serially correlated (Bai and Perron, 2003), as levels such as inflation or interest rates are: a persistent swing then looks like a shift in the mean. For such series, compare the segments for a few values of breaks rather than relying on the chosen number alone.

Breaks show when a series changed character, such as the regimes of inflation or of interest rates, or a change in the average return of an asset. Unlike the Chow test, the break dates do not have to be known in advance.

The formula is as follows:

$$
y_{t} = \mu_{j} + \epsilon_{t} \;\text{for the dates of segment}\; j = 1,\; \ldots,\; m + 1,\;\; \text{with } y_{t} \text{ the column series (Return by default) and } m \text{ breaks}
$$

$$
\operatorname{SSR}(m) = \min \;\text{over the break dates of} \;\sum_{j} \sum_{t \in \text{segment j}}(y_{t} - \bar{y}_{j})^{2},\;\; \text{found exactly by dynamic programming},\;\; \text{with}\;\; \text{every segment at least}\; h = \max(\lfloor \;\text{minimum\_segment} \cdot T \rfloor,\; 2) \;\text{observations} \;(\text{minimum\_segment} = 0.15 \;\text{by default})
$$

$$
\operatorname{BIC}(m) = T \cdot \ln\left(\frac{\operatorname{SSR}(m)}{T}\right) + (2m + 1) \cdot \ln(T),\;\; \text{for}\;\; m = 0,\; \ldots,\; \text{max\_breaks} \;(5 \;\text{by default});\;\; \text{the } m \text{ with the lowest BIC is chosen unless breaks is given}
$$

- Per segment: its Start, End, Observations, Mean $$\bar{y}_{j}$$ and Standard Deviation (ddof=1)

For more information, see the following papers:

- Bai, J. and Perron, P. (1998). "Estimating and Testing Linear Models with Multiple Structural Changes." Econometrica, 66(1), 47-78.
- Bai, J. and Perron, P. (2003). "Computation and Analysis of Multiple Structural Change Models." Journal of Applied Econometrics, 18(1), 1-22.

**Also known as:** Bai-Perron test, multiple structural breaks, change point detection, regime shifts.

**Args:**

- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or
yearly). Defaults to "daily".
- <u>column (str, optional):</u> The historical data column to analyze. Defaults to
"Return"; use "Adj Close" (or "Level" with standalone data) for the series
itself, such as an inflation rate.
- <u>max_breaks (int, optional):</u> The most breaks considered. Defaults to 5.
- <u>minimum_segment (float, optional):</u> The smallest segment as a share of the
observations (the trimming). Defaults to 0.15.
- <u>breaks (int &#124; None, optional):</u> The number of breaks to find instead of choosing
it by the BIC. Defaults to None.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the
assets. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per asset and segment the Start, End, Observations, Mean and
Standard Deviation, with the BIC of the chosen number of breaks.

**As an example:**

```python
from financetoolkit import Economics, Econometrics

economics = Economics(start_date="1960-01-01", end_date="2025-12-31")

inflation = economics.get_inflation_rate(countries="United States", period="yearly")

econometrics = Econometrics(data=inflation)

econometrics.get_structural_breaks(column="Level", max_breaks=3)
```

Which returns:

|                      | Start      | End        |   Observations |   Mean |   Standard Deviation |      BIC |
|:---------------------|:-----------|:-----------|---------------:|-------:|---------------------:|---------:|
| ('United States', 1) | 1960-12-31 | 1972-12-31 |             13 | 0.0282 |               0.0169 | -519.037 |
| ('United States', 2) | 1973-12-31 | 1982-12-31 |             10 | 0.0876 |               0.0269 | -519.037 |
| ('United States', 3) | 1983-12-31 | 2025-12-31 |             43 | 0.0285 |               0.0143 | -519.037 |

---

## get_change_points
Find the dates at which the mean, the volatility or both of every asset's series change, with the PELT (Pruned Exact Linear Time) method of Killick, Fearnhead and Eckley (2012). It finds the exact segmentation that minimizes the Gaussian cost of every segment plus a penalty per change, with no upper limit on the number of changes, and prunes the candidate dates that can no longer be the last change, so it runs in about linear time.

Where `get_structural_breaks` (Bai and Perron) looks for shifts in the mean with a common variance and at most a few breaks, PELT with the default cost="mean_variance" also splits the series where the volatility changes, which for returns separates calm and turbulent periods; cost="variance" keeps the mean fixed and only lets the volatility change, cost="mean" only the mean. Every segment is dated after the fact with the whole series, as a description of the past rather than a signal on the day.

The formula is as follows, with $$y_{t}$$ the `column` series (Return by default), n observations and a segment s of $$n_{s}$$ observations:

$$
\text{cost} = \text{"mean\_variance":} \;C(s) = n_{s} \cdot \ln(\hat{\sigma}_{s}^{2}),\;\; \text{with}\;\; \hat{\sigma}_{s}^{2} = \frac{\sum_{t \in \text{s}}(y_{t} - \bar{y}_{s})^{2}}{n_{s}}
$$

$$
\text{cost} = \text{"variance":} \;C(s) = n_{s} \cdot \ln\left(\frac{\sum_{t \in \text{s}}(y_{t} - \bar{y})^{2}}{n_{s}}\right),\;\; \text{with ȳ the mean of the whole series}
$$

$$
\text{cost} = \text{"mean":} \;C(s) = \frac{\sum_{t \in \text{s}}(y_{t} - \bar{y}_{s})^{2}}{\hat{\sigma}^{2}},\;\; \text{with}\;\; \hat{\sigma} = \frac{\operatorname{MAD}(\Delta y)}{(0.6745 \cdot \sqrt{2}) \;\text{the robust standard deviation from the changes of the series}}
$$

- The segmentation minimizes $$\sum C (s)$$ + β·(number of changes), every segment at least `minimum_segment` observations (5 by default)

$$
\beta = (p + 1) \cdot \ln(n),\;\; \text{the BIC},\;\; \text{with}\;\; p = 2 \;\text{parameters per segment for}\; \text{"mean\_variance"} \;\text{and 1 for}\; \text{"mean"} \;\text{and}\; \text{"variance"} \;\text{plus 1 for the date of the change},\;\; \text{unless penalty is given}
$$

- Per segment: its Start, End, Observations, Mean and Standard Deviation (ddof=1)

For more information, see the following papers:

- Killick, R., Fearnhead, P. and Eckley, I.A. (2012). "Optimal Detection of Changepoints With a Linear Computational Cost." Journal of the American Statistical Association, 107(500), 1590-1598.
- Jackson, B. et al. (2005). "An Algorithm for Optimal Partitioning of Data on an Interval." IEEE Signal Processing Letters, 12(2), 105-108.
- Referenced against ruptures' Pelt ([https://github.com/deepcharles/ruptures](https://github.com/deepcharles/ruptures){:target="_blank"}) and RiskLabAI's pelt_change_points ([https://github.com/RiskLabAI/RiskLabAI.py](https://github.com/RiskLabAI/RiskLabAI.py){:target="_blank"}), which call ruptures; the change points equal those of an exhaustive search.

**Also known as:** PELT, change point detection, changepoints, variance change points, volatility regimes, segmentation, multiple structural breaks.

**Args:**

- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or
yearly). Defaults to "daily".
- <u>column (str, optional):</u> The historical data column to analyze. Defaults to
"Return"; use "Adj Close" (or "Level" with standalone data) for the series
itself, such as an inflation rate.
- <u>cost (str, optional):</u> What may change between segments: "mean_variance" (both),
"variance" (the volatility around the mean of the series) or "mean" (the mean).
Defaults to "mean_variance".
- <u>penalty (float &#124; None, optional):</u> The penalty $$\beta$$ per change; a larger one finds
fewer changes. Defaults to None, the BIC $$(p + 1) \cdot \ln (n)$$.
- <u>minimum_segment (int, optional):</u> The fewest observations of a segment. A segment of
two nearly equal values has a variance close to zero, which the Gaussian cost
rewards without bound, so the variance costs need a few more. Defaults to 5.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the
assets. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per asset and segment the Start, End, Observations, Mean and
Standard Deviation, with the Penalty used.

**Notes:**

- Daily returns have fat tails, so the Gaussian cost splits them more often than a
volatility model would: weekly or monthly returns, or a larger penalty, give fewer
and longer segments.
- A variance is floored at 1e-6 times that of the whole series, so a segment of
equal values has a finite cost; ruptures adds 1e-6 to it instead.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["QQQ", "TLT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2016-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_change_points(period="monthly", cost="variance")
```

Which returns:

|            | Start   | End     |   Observations |    Mean |   Standard Deviation |   Penalty |
|:-----------|:--------|:--------|---------------:|--------:|---------------------:|----------:|
| ('QQQ', 1) | 2016-02 | 2018-09 |             32 |  0.0196 |               0.0319 |    9.5582 |
| ('QQQ', 2) | 2018-10 | 2025-12 |             87 |  0.0161 |               0.0587 |    9.5582 |
| ('TLT', 1) | 2016-02 | 2025-12 |            119 | -0.0002 |               0.0393 |    9.5582 |

---

## get_time_varying_beta
Estimate the alpha and beta of every asset as they change over time, with the Kalman filter. The regression $$y_{t} = \alpha_{t} + \beta_{t} x_{t} + \epsilon_{t}$$ lets both coefficients take a random step every period; how large those steps are, and how much noise surrounds the regression, is estimated by maximum likelihood. A beta that drifts, such as a stock becoming more sensitive to the market, shows up without choosing the window of a rolling regression, while a beta that is constant stays flat.

Every alpha and beta is the filtered estimate, updated with the observations up to its date only. The three variances that set how fast the estimates adapt are estimated on the whole sample, however, so the path is not entirely what would have been known at the time. The filter starts without prior knowledge of the coefficients, so the first date (or the first few, when the independent series starts with zeros) cannot separate the alpha from the beta and is NaN.

By default every asset is regressed on the Benchmark of the Toolkit (or, with standalone data, on the second series).

The formula is as follows:

$$
y_{t} = \alpha_{t} + \beta_{t} \cdot x_{t} + \epsilon_{t},\;\; \epsilon_{t} \sim N(0,\; \sigma_{\epsilon}^{2}),\;\; \text{with } y_{t} \text{ the asset's and } x_{t} \text{ the independent asset's column series (Return by default), on the dates both have}
$$

$$
\alpha_{t} = \alpha_{t-1} + \eta_{t}\;\;\text{and}\;\; \beta_{t} = \beta_{t-1} + \zeta_{t},\;\; \eta_{t} \sim N(0,\; \sigma_{\alpha}^{2}) \;\text{and}\; \zeta_{t} \sim N(0,\; \sigma_{\beta}^{2}) \;\text{:} \;\text{random walks}
$$

- $$\sigma_{\epsilon}^{2}$$, $$\sigma_{\alpha}^{2}$$ and $$\sigma_{\beta}^{2}$$ are fitted by Maximum Likelihood with the Kalman filter (diffusely initialized) on the series divided by their standard deviations, and scaled back

- Alpha and Beta are the filtered states $$E [\alpha_{t} , \beta_{t} \vert y_{1} \ldots y_{t}]$$; the Beta Standard Error is the square root of the filtered variance of $$\beta_{t}$$

For more information, see the following book:

- Durbin, J. and Koopman, S.J. (2012). "Time Series Analysis by State Space Methods." Oxford University Press, 2nd edition.

**Also known as:** Kalman filter beta, rolling beta, dynamic beta, state space regression.

**Args:**

- <u>dependent_tickers (str &#124; list[str] &#124; None, optional):</u> The assets whose beta is
estimated. Defaults to None, which uses every asset except the independent one.
- <u>independent_ticker (str &#124; None, optional):</u> The asset the beta is measured
against. Defaults to None, which uses the Benchmark or the second series.
- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or
yearly). Defaults to "daily".
- <u>column (str, optional):</u> The historical data column to use. Defaults to "Return".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per date and asset the Alpha, the Beta and the standard error of
the beta, NaN on the first date(s) where they are not yet identified.

**Notes:**

- Requires statsmodels (`pip install financetoolkit[econometrics]`).

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2015-01-01",
    end_date="2025-12-31",
)

beta = toolkit.econometrics.get_time_varying_beta(period="monthly")

beta.xs("Beta", axis=1, level=1).iloc[12::24]
```

Which returns:

| Date    |   AAPL |   MSFT |
|:--------|-------:|-------:|
| 2016-02 | 1.2708 | 1.5813 |
| 2018-02 | 1.1427 | 1.3183 |
| 2020-02 | 1.3197 | 1.1153 |
| 2022-02 | 1.2496 | 0.9853 |
| 2024-02 | 1.2526 | 0.9525 |

---

## get_dcc_garch
Estimate the correlation between every pair of assets as it changes over time, with the dynamic conditional correlation (DCC) GARCH(1,1) model of Engle (2002). Every asset gets its own GARCH(1,1) volatility, and the correlation of the standardized returns follows a GARCH-like recursion around their long-run correlation. Correlations between assets tend to rise in crises, exactly when diversification is needed most. A rolling correlation sees that late and depends on its window; the DCC model updates the correlation every period, with a (how strongly it reacts to news) and b (how persistent it is) estimated by maximum likelihood.

The formula is as follows:

$$
z_{i,t} = \frac{r_{i,t} - \operatorname{mean}(r_{i})}{\sigma_{i,t}},\;\; \text{with}\;\; r_{i,t} \;\text{the} \;\text{column} \;\text{series} \;(\text{Return by default}) \;\text{on the dates all assets have and}\; \sigma_{i,t}^{2} = \omega + \alpha \cdot u_{i,t-1}^{2} + \beta \cdot \sigma_{i,t-1}^{2} \;\text{each asset's GARCH}(1,\; 1) \;\text{variance of the demeaned returns}\; u (\text{GARCH Persistence} = \alpha + \beta)
$$

$$
Q_{t} = (1 - a - b) \cdot \bar{Q} + a \cdot z_{t-1} \cdot z_{t-1}' + b \cdot Q_{t-1},\;\; \text{with}\;\; \bar{Q} \;\text{the sample correlation of}\; z \;\text{and}\; Q_{0} = \bar{Q}
$$

$$
R_{t} = \operatorname{diag}(Q_{t})^{- \frac{1}{2}} \cdot Q_{t} \cdot \operatorname{diag}(Q_{t})^{- \frac{1}{2}},\;\; \text{the conditional correlations}
$$

- a and b maximize the correlation log-likelihood $$- \tfrac{1}{2} \cdot \sum_{t} (\ln \vert R_{t} \vert + z_{t}' \cdot R_{t}^{- 1} \cdot z_{t})$$, with a, $$b \geq 0$$ and $$a + b < 1$$

For more information, see the following paper:

- Engle, R. (2002). "Dynamic Conditional Correlation: A Simple Class of Multivariate Generalized Autoregressive Conditional Heteroskedasticity Models." Journal of Business & Economic Statistics, 20(3), 339-350.

**Also known as:** DCC-GARCH, dynamic conditional correlation, time-varying correlation, multivariate GARCH.

**Args:**

- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or
yearly). Defaults to "daily".
- <u>column (str, optional):</u> The historical data column to use. Defaults to "Return".
- <u>parameters (bool, optional):</u> Whether to return the estimated parameters (a, b and
the GARCH persistence of every asset) instead of the correlations. Defaults
to False.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the
assets. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The conditional correlation of every pair of assets per date, or
the parameters of the model.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "XOM"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2018-01-01",
    end_date="2025-12-31",
)

correlations = toolkit.econometrics.get_dcc_garch()

correlations.resample("Y").mean().round(4)
```

Which returns:

| Date   |   AAPL / MSFT |   AAPL / XOM |   MSFT / XOM |
|:-------|--------------:|-------------:|-------------:|
| 2018   |        0.6047 |       0.2794 |       0.2729 |
| 2019   |        0.578  |       0.2982 |       0.2641 |
| 2020   |        0.6665 |       0.2879 |       0.226  |
| 2021   |        0.6199 |       0.1384 |       0.0786 |
| 2022   |        0.7084 |       0.2283 |       0.1692 |
| 2023   |        0.5802 |       0.1706 |       0.0386 |
| 2024   |        0.5378 |       0.1018 |       0.0237 |
| 2025   |        0.4636 |       0.1991 |       0.114  |

---

## get_pairs_trading
Calculate the statistics of trading the spread between every pair of assets. The hedge ratio follows from regressing one log price on the other; what remains is the spread, and when the two are cointegrated the spread reverts to its mean. Its z-score says how far it is from that mean in standard deviations, and threshold rules trade on it: short the spread (sell the first asset, buy the hedge ratio of the second) once the z-score rises above the entry threshold, buy it once it falls below minus the threshold, and close the position once the z-score crosses the exit threshold on its way back (below it for a short, above minus it for a long). A z-score that jumps past the band in one period still closes the position, and one that lands beyond the entry threshold on the other side reverses it. The half-life says how many periods the spread takes to close half its gap to the mean.

Gatev, Goetzmann and Rouwenhorst (2006) open a position when the normalized prices of a pair drift two standard deviations (of their formation period) apart and close it when the prices cross, which is an exit threshold of 0; closing at 0.5 is a common variant that takes profits before the spread is fully back at its mean.

The hedge ratio and intercept are estimated on the whole period, so the spread, and with it every z-score and signal, uses information from after its date. A rolling window only makes the mean and standard deviation of the z-score backward-looking; a backtest without look-ahead estimates the hedge ratio on a formation period and trades in the period after it. The Engle-Granger p-value says whether there is a mean-reverting relationship to trade at all (below 0.05).

The formula is as follows:

$$
y_{t} = c + h \cdot x_{t} + s_{t},\;\; \text{fitted by OLS on the dates both have},\;\; \text{with}\; y_{t} \;\text{and}\; x_{t} \;\text{the} \;(\log,\; \text{when}\; \text{log\_prices} = \text{True}) \;\text{column} \;\text{levels} \;(\text{Adj Close by default}) \;\text{:} h \;\text{the Hedge Ratio},\;\; c \text{ the Intercept and } s_{t} \text{ the Spread}
$$

$$
\text{Z-Score}_{t} = \frac{s_{t} - \operatorname{mean}(s)}{\operatorname{std}(s) (\text{ddof} = 1)},\;\; \text{over the full sample or a rolling window}
$$

- Signal: -1 from Z > `entry_z_score` until Z < `exit_z_score`, +1 from Z < -`entry_z_score` until Z > -`exit_z_score`, 0 otherwise (2.0 and 0.5 by default)

$$
\text{Half-Life} = - \frac{\ln(2)}{\ln(1 + \lambda)},\;\; \text{with}\;\; \lambda \;\text{from}\; \Delta s_{t} = a + \lambda \cdot s_{t-1} + \epsilon_{t} (\text{infinite when}\; \lambda \;\text{is} \;(\text{nearly}) \;\text{zero or positive})
$$

- Cointegration P-Value: the Engle-Granger test of $$y_{t}$$ on $$x_{t}$$

For more information, see the following papers:

- Gatev, E., Goetzmann, W.N. and Rouwenhorst, K.G. (2006). "Pairs Trading: Performance of a Relative-Value Arbitrage Rule." The Review of Financial Studies, 19(3), 797-827.
- Engle, R.F. and Granger, C.W.J. (1987). "Co-Integration and Error Correction: Representation, Estimation, and Testing." Econometrica, 55(2), 251-276.

**Also known as:** statistical arbitrage, spread trading, z-score strategy, half-life of mean reversion.

**Args:**

- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or
yearly). Defaults to "daily".
- <u>column (str, optional):</u> The price column. Defaults to "Adj Close".
- <u>window (int &#124; None, optional):</u> The rolling window of the z-score. Defaults to
None, which uses the full sample.
- <u>entry_z_score (float, optional):</u> The z-score at which a position is opened.
Defaults to 2.0.
- <u>exit_z_score (float, optional):</u> The z-score whose crossing on the way back closes
a position (0 closes when the spread is back at its mean). Defaults to 0.5.
- <u>log_prices (bool, optional):</u> Whether to use log prices, so the hedge ratio is an
elasticity. Defaults to True.
- <u>time_series (bool, optional):</u> Whether to return the Spread, Z-Score and Signal
per date instead of the summary. Defaults to False.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the
assets. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per pair the Hedge Ratio, Intercept, Half-Life (in periods),
Cointegration P-Value, the latest Z-Score and Signal (1 long, -1 short, 0 flat)
and the Number of Trades (positions opened, a reversal counting as a new one);
or, with time_series=True, the Spread, Z-Score and Signal per date.

**Notes:**

- Requires statsmodels (`pip install financetoolkit[econometrics]`).

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["KO", "PEP"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2015-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_pairs_trading(window=60)
```

Which returns:

|               |   Hedge Ratio |   Intercept |   Half-Life |   Cointegration P-Value |   Z-Score |   Signal |   Number of Trades |
|:--------------|--------------:|------------:|------------:|------------------------:|----------:|---------:|-------------------:|
| ('KO', 'PEP') |        0.8685 |     -0.3098 |     290.448 |                  0.8345 |     0.684 |        0 |                 42 |

---

## get_optimal_trading_rule
Find the profit-taking and stop-loss levels with the highest Sharpe ratio for a long position in every asset, when its log price follows the mean-reverting Ornstein-Uhlenbeck process fitted to it, with the Monte Carlo method of López de Prado (2018, chapter 13).

The process is fitted to the log prices by a regression of each on the one before it, which gives how persistent the price is (Phi), the level it reverts to (the Long-Run Mean) and the size of its shocks (Sigma). Thousands of paths of that process are then simulated from the last price, and every pair of a profit-taking and a stop-loss level on a mesh, in units of Sigma, is tried on the same paths: a position is closed once the price rises above the profit-taking level, falls below the stop-loss level or has been held for the maximum holding period. The rule with the highest Sharpe ratio of the gains is the optimal one. A price far below its long-run mean (a positive Forecast) favours a wide profit-taking level, one above it a tight stop-loss; for a price that hardly reverts (Phi close to 1, a long Half-Life) the Sharpe ratios are close to zero and the rule matters little.

The formula is as follows, with $$p_{t}$$ the log of the `column` (Adj Close by default):

$$
p_{t} = c + \phi \cdot p_{t-1} + \sigma \cdot \epsilon_{t} \;\text{by OLS},\;\; \text{with}\; \sigma \;\text{the standard deviation of the residuals} \;(n - 2 \;\text{degrees of freedom}),\;\; \text{Long-Run Mean} = \frac{c}{1 - \phi},\;\; \text{Half-Life} = - \frac{\ln(2)}{\ln(\phi)}\;\;\text{and}\;\; \text{Forecast} = \frac{\text{Long-Run Mean} - p_{0}}{\sigma},\;\; \text{with } p_{0} \text{ the last log price}
$$

$$
y_{t} = \frac{p_{t} - p_{0}}{\sigma} = (1 - \phi) \cdot \text{Forecast} + \phi \cdot y_{t-1} + \epsilon_{t},\;\; y_{0} = 0,\;\; \epsilon_{t} \sim N(0,\; 1),\;\; \text{for paths paths (10,000 by default) of at most maximum\_holding\_period steps (100 by default)}
$$

$$
\text{For every profit-taking } \bar{\pi} \text{ and stop-loss } \pi \text{̲} \text{ in \{} h \text{, 2h, ..., maximum\_threshold\}},\;\; h = \frac{\text{maximum\_threshold}}{\text{grid\_size}} \;(0.5 \;\text{to 10 by default}) \;\text{:} \;\text{the gain of a path is}\; y_{t} \;\text{at the first}\; t \;\text{with}\; y_{t} > \bar{\pi} \;\text{or}\; y_{t} < - \text{pi̲},\;\; \text{or at the maximum holding period}
$$

$$
\text{Sharpe Ratio} = \frac{\text{mean}}{\text{standard deviation} \;(\text{ddof} = 1) \;\text{of the gains}};\;\; \text{the rule with the highest is reported with its Mean and Standard Deviation (in } \sigma \text{) and Average Holding Period}
$$

For more information, see the following book:

- López de Prado, M. (2018). "Advances in Financial Machine Learning." Wiley, chapter 13, "Backtesting on Synthetic Data".
- Referenced against RiskLabAI's ou_rule_metrics ([https://github.com/RiskLabAI/RiskLabAI.py](https://github.com/RiskLabAI/RiskLabAI.py){:target="_blank"}), the closed-form gain and exit time of the continuous process, which the simulation agrees with once the levels are moved out by 0.5826 Sigma for the discrete monitoring (Broadie, Glasserman and Kou, 1997).

**Also known as:** optimal trading rule, OTR, profit-taking and stop-loss, Ornstein-Uhlenbeck trading rule, mean reversion trading rule, synthetic backtest.

**Args:**

- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or
yearly). Defaults to "daily".
- <u>column (str, optional):</u> The price column. Defaults to "Adj Close".
- <u>maximum_threshold (float, optional):</u> The widest profit-taking and stop-loss level,
in units of Sigma. Defaults to 10.0.
- <u>grid_size (int, optional):</u> The number of levels on each side of the mesh, so the
mesh has grid_size² rules. Defaults to 20.
- <u>maximum_holding_period (int, optional):</u> The most periods a position is held.
Defaults to 100.
- <u>paths (int, optional):</u> The number of simulated paths. Defaults to 10000.
- <u>seed (int, optional):</u> The seed of the simulation. Defaults to 0.
- <u>log_prices (bool, optional):</u> Whether to fit the process to the log prices. Pass False
for a series that can be zero or negative, such as a spread. Defaults to True.
- <u>grid (bool, optional):</u> Whether to return every rule of the mesh instead of the
optimal one. Defaults to False.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the
assets. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per asset the Phi, Half-Life (in periods), Sigma, Long-Run Mean (of the
log price), Forecast, the optimal Profit-Taking and Stop-Loss (in Sigma), and the
Mean and Standard Deviation of the gain (in Sigma), its Sharpe Ratio and the Average
Holding Period; with grid=True the Mean, Standard Deviation, Sharpe Ratio and
Average Holding Period of every rule, per asset, Profit-Taking and Stop-Loss.

**Notes:**

- Every rule is tried on the same paths, so the differences between neighbouring rules
are not simulation noise; the paths follow from the seed, so the result is the same
on every run. With a wide stop-loss a few large losses decide the standard deviation,
so the Sharpe ratio of such a rule can move by 0.1 or more with another seed at
10,000 paths; more paths narrow it.
- López de Prado draws new paths for every rule, closes a position one period after the
maximum holding period and takes the standard deviation with ddof=0.
- The rule is for a long position. For a short position, analyze the negative of the
log prices (`Econometrics(data=...)` with log_prices=False), whose rise is a fall
in the price.
- The simulation takes about a second per asset with the defaults.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["PFE", "KO"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_optimal_trading_rule()
```

Which returns:

|                        |      PFE |       KO |
|:-----------------------|---------:|---------:|
| Phi                    |   0.9977 |   0.9969 |
| Half-Life              | 303.568  | 222.457  |
| Sigma                  |   0.0158 |   0.01   |
| Long-Run Mean          |   3.3005 |   4.1335 |
| Forecast               |   9.5111 |  -9.4587 |
| Profit-Taking          |   6      |   0.5    |
| Stop-Loss              |  10      |   0.5    |
| Mean                   |   1.3971 |  -0.0498 |
| Standard Deviation     |   7.018  |   1.2679 |
| Sharpe Ratio           |   0.1991 |  -0.0393 |
| Average Holding Period |  55.5542 |   1.5936 |

---

## get_diebold_mariano_test
Compare the forecast accuracy of two volatility forecasting methods against realized (squared return) Variance, per asset, via the Diebold-Mariano (1995) test.

Rather than comparing two different assets, this compares two different ways of forecasting the *same* asset's next-day Variance -- e.g. the simpler exponentially weighted (EWMA, see `Risk.get_ewma_volatility`) approach against a plain rolling-window Standard Deviation -- to determine whether one is significantly more accurate than the other for a given asset.

The squared return is a noisy stand-in for the true Variance. Patton (2011) shows that the squared-error loss still ranks two volatility forecasts correctly with such a proxy, while the absolute-error loss can rank them the wrong way round, so `loss="squared"` is the safer choice. A negative statistic favors `method_a`.

The formula is as follows:

- Realized Variance: $$r_{t}^{2}$$

$$
\text{EWMA forecast ("ewma"):}\;\; \sigma_{t}^{2} = \lambda \cdot \sigma_{t-1}^{2} + (1 - \lambda) \cdot r_{t-1}^{2},\;\; \text{with}\;\; \lambda = \text{lambda\_} \;(0.94 \;\text{by default}),\;\; \text{so the forecast for}\; t \;\text{uses returns up to}\; t - 1
$$

- Rolling forecast ("rolling"): the sample variance (ddof=1) of the `window_size` (22 by default) returns up to t - 1

$$
d_{t} = L(r_{t}^{2} - f_{a,t}) - L(r_{t}^{2} - f_{b,t}),\;\; \text{with}\;\; L(e) = e^{2}(\text{loss} = \text{"squared"}) \;\text{or} \;\left|e\right| \;(\text{loss} = \text{"absolute"})
$$

$$
\text{DM} = \frac{\operatorname{mean}(d)}{\sqrt{\frac{\gamma_{0}}{n}}} \cdot \sqrt{\frac{n - 1}{n}},\;\; \text{with}\;\; \gamma_{0} = \frac{1}{n} \cdot \sum(d_{t} - \operatorname{mean}(d))^{2} \;\text{and the Harvey, Leybourne and Newbold} \;(1997) \;\text{correction for a one-step horizon}
$$

$$
\text{P-Value} = 2 \cdot P(T > \left|\text{DM}\right|) \;\text{for a Student-t distribution with}\; n - 1 \;\text{degrees of freedom}
$$

For more information about the method, see the following papers:

- Diebold, F.X., & Mariano, R.S. (1995). "Comparing Predictive Accuracy." Journal of Business & Economic Statistics, 13(3), 253-263.
- Patton, A.J. (2011). "Volatility Forecast Comparison Using Imperfect Volatility Proxies." Journal of Econometrics, 160(1), 246-256.

**Also known as:** DM test, forecast comparison test.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily", since `window_size` is expressed in return observations of this
frequency.
- <u>method_a (str, optional):</u> The first volatility forecasting method, one of "ewma" or "rolling".
Defaults to "ewma".
- <u>method_b (str, optional):</u> The second (competing) volatility forecasting method, one of "ewma"
or "rolling". Defaults to "rolling".
- <u>window_size (int, optional):</u> The rolling window size used by the "rolling" method. Defaults to
22 (approximately one trading month).
- <u>lambda_ (float, optional):</u> The decay factor used by the "ewma" method. Defaults to 0.94.
- <u>loss (str, optional):</u> The loss function to compare forecast errors with, one of "squared" or
"absolute". Defaults to "squared".
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the
assets tested. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The Diebold-Mariano statistic, its p-value, the mean loss differential (negative
favors `method_a`) and the number of observations used, per asset.

**Notes:**

- Both forecasts for period t use only the returns up to, and including, period t - 1, so this
is a genuinely out-of-sample forecast comparison rather than an in-sample fit comparison.
- Each asset uses its own return history, so an asset with a shorter history does not shorten
the comparison of the others.
- Like `Risk.get_var_backtest`, this is calculated over the full return history rather than the
`within_period` slices used elsewhere in this module, since the rolling/EWMA forecasts need more
history than a single sub-period provides.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["XOM", "CVX", "SHEL", "BP"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_diebold_mariano_test(method_a="ewma", method_b="rolling")
```

Which returns:

|                           |       XOM |       CVX |      SHEL |        BP |
|:--------------------------|----------:|----------:|----------:|----------:|
| Diebold-Mariano Statistic |   -3.9115 |   -4.9425 |   -1.8262 |   -1.3358 |
| P-Value                   |    0.0001 |    0      |    0.0681 |    0.1818 |
| Mean Loss Differential    |    0      |    0      |    0      |    0      |
| Observations              | 1232      | 1232      | 1232      | 1232      |

---

## get_arima_forecast
Fit an ARIMA(p, d, q) model to every ticker's price series in the Toolkit instance and forecast `forecast_steps` periods ahead.

**Also known as:** Box-Jenkins model, autoregressive integrated moving average.

An ARIMA(p, d, q) model differences the series `d` times to remove a (stochastic) trend, then fits an autoregressive-moving-average model to the result -- see `time_series_model.get_arima_forecast` for the full formula, estimation method (exact Maximum Likelihood via the Kalman filter) and its practical caveats.

The formula is as follows:

$$
y'_{t} = \Delta^{d} Y_{t},\;\; \text{the} \;\text{column} \;\text{level} \;(\text{Adj Close by default}) \;\text{differenced}\; d \;\text{times} \;(d = 1 \;\text{by default})
$$

$$
y'_{t} - \mu = \sum_{i=1}^{p} \phi_{i} \cdot (y'_{t-i} - \mu) + \epsilon_{t} + \sum_{j=1}^{q} \theta_{j} \cdot \epsilon_{t-j},\;\; \text{with}\;\; p = q = 1 \;\text{by default}\;\;\text{and}\;\; \mu \;\text{the mean} \;(d = 0) \;\text{or drift} \;(d \geq 1) \;\text{of}\; y'_{t} \;\text{when}\; \text{include\_constant} = \text{True},\;\; \text{and}\;\; \mu = 0 \;\text{otherwise}
$$

- Fitted by exact Maximum Likelihood via the Kalman filter (statsmodels ARIMA)

$$
\text{Forecast:}\;\; \text{the conditional mean}\; E\left[Y_{T+h} \mid Y_{1} \ldots Y_{T}\right] \;\text{for}\; h = 1 \ldots \;\text{forecast\_steps},\;\; \text{in levels}
$$

**Args:**

- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to fit. Defaults to
"Adj Close".
- <u>p (int, optional):</u> The autoregressive order. Defaults to 1.
- <u>d (int, optional):</u> The number of times to difference the series. Defaults
to 1 (the typical choice for a non-stationary price level series).
- <u>q (int, optional):</u> The moving-average order. Defaults to 1.
- <u>forecast_steps (int, optional):</u> The number of periods ahead to forecast.
Defaults to 5.
- <u>include_constant (bool, optional):</u> Whether to estimate the mean of the
differenced series (its drift for `d >= 1`). Defaults to True -- see
`time_series_model.get_arima_forecast` for when to set this to False.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among
the tickers forecast. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the
results to. Defaults to None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The `forecast_steps`-ahead forecast, one column per ticker,
indexed `1, ..., forecast_steps` (periods ahead, not a continuation of the
historical date index). Each ticker's ARIMA model is fit independently on
its own history; a ticker without enough data has an empty (NaN) column.

**Notes:**

- The method retrieves historical price data based on the specified `period`
for every ticker in the Toolkit instance and fits an ARIMA model to each.
- See `time_series_model.get_arima_forecast`'s `Notes` for this estimator's
practical limitations (in particular, keep `p + q` small).
- Requires statsmodels (`pip install financetoolkit[econometrics]`).

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["GCUSD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_arima_forecast(forecast_steps=10)
```

Which returns:

|   Step |   GCUSD |
|-------:|--------:|
|      1 | 4348.34 |
|      2 | 4348.38 |
|      3 | 4350.82 |
|      4 | 4352.47 |
|      5 | 4354.38 |
|      6 | 4356.2  |
|      7 | 4358.05 |
|      8 | 4359.89 |
|      9 | 4361.73 |
|     10 | 4363.57 |

---

## get_var_forecast
Fit a Vector Autoregression (VAR) across every ticker in the Toolkit instance and forecast `forecast_steps` periods ahead.

A VAR models several series jointly: each ticker's value is regressed on `lags` past values of all tickers, including its own. Each asset's future can therefore depend on its own history and on the history of the others, without deciding in advance which one drives which.

The formula is as follows:

$$
Y_{t} = c + \sum_{l=1}^{\text{lags}}(\Phi_{l} \cdot Y_{t-l}) + e_{t},\;\; \text{with}\;\; Y_{t} \;\text{every ticker's} \;\text{column} \;(\text{Return by default}) \;\text{and} \;\text{lags} = 1 \;\text{by default}
$$

- Each equation is an OLS regression on a constant and the `lags` lagged values of all tickers

$$
\text{Forecast:}\;\; \hat{Y}_{T+h} = c + \sum_{l=1}^{\text{lags}}(\Phi_{l} \cdot \hat{Y}_{T+h-l}),\;\; \text{with}\;\; \hat{Y}_{s} = Y_{s} \;\text{for}\; s \leq T
$$

Where `Y_t` holds the values of all tickers at time `t` and each `Phi_l` is a matrix of coefficients. Because every equation has the same regressors, the model is estimated exactly by a separate OLS regression per ticker. Forecasts are produced by running the fitted equations forward one step at a time, feeding each forecast back in as the most recent lag. The coefficients show how shocks spread between assets; `get_impulse_response_function` and `get_variance_decomposition` summarise that, and `get_granger_causality` tests whether one ticker helps predict another. A VAR assumes stationary series, so returns are generally more suitable than prices (see `get_unit_root_test`).

For more information about the method, see the following paper:

- Sims, C.A. (1980). "Macroeconomics and Reality." Econometrica, 48(1), 1-48.

**Also known as:** VAR model, vector autoregressive model.

**Args:**

- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to model. Defaults to
"Return".
- <u>lags (int, optional):</u> The VAR order. Defaults to 1.
- <u>forecast_steps (int, optional):</u> The number of periods ahead to forecast.
Defaults to 5.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among
the tickers modeled jointly. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the
results to. Defaults to None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The `forecast_steps`-ahead forecast, one column per ticker,
indexed `1, ..., forecast_steps` (periods ahead).

**Notes:**

- The method retrieves historical data based on the specified `period` for every
ticker in the Toolkit instance and fits the VAR model jointly across all of them.
- Unlike `get_vecm_forecast`, this operates on `column` directly (typically
"Return", a stationary series) rather than price levels -- a VAR in levels is
misspecified for non-stationary series (see
`cointegration_model.get_johansen_cointegration`); use `get_vecm_forecast`
instead if the assets' price levels are cointegrated.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["^VIX", "^VIX3M"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_var_forecast(column="Adj Close", forecast_steps=20)
```

Which returns:

|   Step |    ^VIX |   ^VIX3M |
|-------:|--------:|---------:|
|      1 | 15.2712 |  18.3667 |
|      2 | 15.5578 |  18.5342 |
|      3 | 15.8138 |  18.6846 |
|      4 | 16.0425 |  18.82   |
|      5 | 16.2471 |  18.9418 |
|      6 | 16.4301 |  19.0517 |
|      7 | 16.5941 |  19.1509 |
|      8 | 16.7411 |  19.2406 |
|      9 | 16.873  |  19.322  |
|     10 | 16.9915 |  19.3958 |
|     11 | 17.0981 |  19.4629 |
|     12 | 17.1942 |  19.5241 |
|     13 | 17.2808 |  19.58   |
|     14 | 17.359  |  19.6311 |
|     15 | 17.4298 |  19.6781 |
|     16 | 17.494  |  19.7213 |
|     17 | 17.5523 |  19.7611 |
|     18 | 17.6053 |  19.7979 |
|     19 | 17.6536 |  19.8321 |
|     20 | 17.6978 |  19.8639 |

---

## get_impulse_response_function
Fit a Vector Autoregression (VAR) across every ticker in the Toolkit instance and trace out the Impulse Response Function (IRF) -- how a shock to each ticker propagates through the whole system over `periods` periods ahead. The shock is one standard deviation of the orthogonalized innovation when `orthogonalized=True` (the default) and a unit shock to the reduced-form residual when `orthogonalized=False`.

**Also known as:** IRF.

A natural companion to `get_var_forecast`: rather than forecasting the levels forward, this traces out each ticker's dynamic response to a shock in every ticker (including itself) -- see `time_series_model.get_impulse_response_function` for the full formula, the Cholesky-orthogonalization used to identify the shocks, and why the ordering of tickers is an identifying assumption.

The formula is as follows:

$$
\Psi_{0} = I\;\;\text{and}\;\; \Psi_{n} = \sum_{l=1}^{\min(n,p)} \Phi_{l} \cdot \Psi_{n-l},\;\; \text{the moving-average matrices of the VAR(} p \text{) fitted on every ticker's column (Return by default)},\;\; p = \text{lags} \;(1 \;\text{by default})
$$

$$
\Sigma_{u} = \frac{\hat{U}' \hat{U}}{T - k \cdot p - 1} = P \cdot P',\;\; \text{with } P \text{ the lower-triangular Cholesky factor}
$$

$$
\Theta_{n} = \Psi_{n} \cdot P (\text{orthogonalized} = \text{True},\; \text{a one-standard-deviation shock}) \;\text{or}\; \Theta_{n} = \Psi_{n} (\text{orthogonalized} = \text{False},\; \text{a unit reduced-form shock})
$$

$$
\text{Response of ticker } i \text{, } n \text{ periods after a shock to ticker } j \text{:}\;\; \Theta_{n} [i , j],\;\; \text{for}\;\; n = 0 \ldots \;\text{periods}
$$

**Args:**

- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to model. Defaults to
"Return".
- <u>lags (int, optional):</u> The VAR order. Defaults to 1.
- <u>periods (int, optional):</u> The number of periods ahead to trace the response
out to. Defaults to 10.
- <u>orthogonalized (bool, optional):</u> Whether to orthogonalize the shocks via a
Cholesky decomposition of the residual covariance matrix -- see
`time_series_model.get_impulse_response_function`. Defaults to True.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among
the tickers modeled jointly. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the
results to. Defaults to None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Each shock ticker's response table, one column per response
ticker, concatenated side by side under a top-level column per shock
ticker, indexed `0, ..., periods` (horizon, `0` = impact response).

**Notes:**

- The ordering of the tickers modeled determines which ticker is treated as
contemporaneously prior to the others. That ordering follows the Toolkit
instance's own ticker order and is not configurable here -- reorder the
Toolkit instance's tickers themselves to change the Cholesky identification
order -- see `time_series_model.get_impulse_response_function`'s `Notes`.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["^VIX", "^OVX"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_impulse_response_function(column="Adj Close", periods=20)
```

Which returns:

|   Horizon |   ('^VIX', '^VIX') |   ('^VIX', '^OVX') |   ('^OVX', '^VIX') |   ('^OVX', '^OVX') |
|----------:|-------------------:|-------------------:|-------------------:|-------------------:|
|         0 |             1.7975 |             1.1106 |             0      |             2.4048 |
|         1 |             1.6806 |             1.1595 |             0.022  |             2.2148 |
|         2 |             1.5725 |             1.1956 |             0.0407 |             2.0416 |
|         3 |             1.4723 |             1.2207 |             0.0565 |             1.8834 |
|         4 |             1.3794 |             1.2361 |             0.0698 |             1.7389 |
|         5 |             1.2933 |             1.2433 |             0.0807 |             1.6069 |
|         6 |             1.2133 |             1.2434 |             0.0897 |             1.4861 |
|         7 |             1.1389 |             1.2374 |             0.097  |             1.3755 |
|         8 |             1.0698 |             1.2262 |             0.1027 |             1.2743 |
|         9 |             1.0054 |             1.2106 |             0.1071 |             1.1814 |
|        10 |             0.9454 |             1.1914 |             0.1104 |             1.0963 |
|        11 |             0.8895 |             1.1691 |             0.1126 |             1.0181 |
|        12 |             0.8374 |             1.1444 |             0.114  |             0.9462 |
|        13 |             0.7887 |             1.1176 |             0.1146 |             0.8801 |
|        14 |             0.7432 |             1.0893 |             0.1145 |             0.8193 |
|        15 |             0.7006 |             1.0597 |             0.1139 |             0.7633 |
|        16 |             0.6608 |             1.0292 |             0.1129 |             0.7117 |
|        17 |             0.6236 |             0.9981 |             0.1114 |             0.664  |
|        18 |             0.5886 |             0.9667 |             0.1096 |             0.6201 |
|        19 |             0.5559 |             0.9351 |             0.1075 |             0.5794 |
|        20 |             0.5252 |             0.9034 |             0.1052 |             0.5418 |

---

## get_variance_decomposition
Fit a Vector Autoregression (VAR) across every ticker in the Toolkit instance and compute the (orthogonalized) Forecast Error Variance Decomposition (FEVD) -- what fraction of each ticker's `h`-step-ahead forecast error variance is attributable to each ticker's own structural shock, for `h = 1, ..., periods`.

**Also known as:** FEVD, variance decomposition.

The other natural companion to `get_var_forecast` (alongside `get_impulse_response_function`, which the FEVD is built from) -- see `time_series_model.get_variance_decomposition` for the full formula. A large own-shock share at short horizons that decays as the horizon grows is the classic signature of a ticker that is initially self-driven but increasingly explained by the rest of the system over time.

The formula is as follows:

$$
\Theta_{n} = \Psi_{n} \cdot P,\;\; \text{the orthogonalized moving-average matrices of get\_impulse\_response\_function, from a VAR(} p \text{) on every ticker's column (Return by default)},\;\; p = \text{lags} \;(1 \;\text{by default})
$$

$$
\text{Share of ticker j's shock in ticker i's h-step forecast error variance:}\;\; \omega_{ij}(h) = \frac{\sum_{n=0}^{h-1} \Theta_{n}\left[i,\; j\right]^{2}}{\sum_{m=1}^{k} \sum_{n=0}^{h-1} \Theta_{n}\left[i,\; m\right]^{2}},\;\; \text{for}\;\; h = 1 \ldots \;\text{periods}
$$

**Args:**

- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to model. Defaults to
"Return".
- <u>lags (int, optional):</u> The VAR order. Defaults to 1.
- <u>periods (int, optional):</u> The forecast horizon to decompose out to.
Defaults to 10.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among
the tickers modeled jointly. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the
results to. Defaults to None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Each response ticker's variance-share table (one column per
shock ticker, rows summing to 1), concatenated side by side under a
top-level column per response ticker, indexed `1, ..., periods` (horizon).

**Notes:**

- See `get_impulse_response_function`'s `Notes` on the Cholesky ordering --
the same identifying assumption applies here.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["^VIX", "^GVZ"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_variance_decomposition(column="Adj Close", periods=20)
```

Which returns:

|   Horizon |   ('^VIX', '^VIX') |   ('^VIX', '^GVZ') |   ('^GVZ', '^VIX') |   ('^GVZ', '^GVZ') |
|----------:|-------------------:|-------------------:|-------------------:|-------------------:|
|         1 |             1      |             0      |             0.1832 |             0.8168 |
|         2 |             1      |             0      |             0.1925 |             0.8075 |
|         3 |             0.9999 |             0.0001 |             0.2016 |             0.7984 |
|         4 |             0.9998 |             0.0002 |             0.2104 |             0.7896 |
|         5 |             0.9997 |             0.0003 |             0.219  |             0.781  |
|         6 |             0.9996 |             0.0004 |             0.2273 |             0.7727 |
|         7 |             0.9995 |             0.0005 |             0.2354 |             0.7646 |
|         8 |             0.9993 |             0.0007 |             0.2432 |             0.7568 |
|         9 |             0.9991 |             0.0009 |             0.2506 |             0.7494 |
|        10 |             0.9989 |             0.0011 |             0.2578 |             0.7422 |
|        11 |             0.9987 |             0.0013 |             0.2647 |             0.7353 |
|        12 |             0.9985 |             0.0015 |             0.2714 |             0.7286 |
|        13 |             0.9983 |             0.0017 |             0.2777 |             0.7223 |
|        14 |             0.9981 |             0.0019 |             0.2837 |             0.7163 |
|        15 |             0.9978 |             0.0022 |             0.2895 |             0.7105 |
|        16 |             0.9976 |             0.0024 |             0.2949 |             0.7051 |
|        17 |             0.9974 |             0.0026 |             0.3002 |             0.6998 |
|        18 |             0.9971 |             0.0029 |             0.3051 |             0.6949 |
|        19 |             0.9969 |             0.0031 |             0.3098 |             0.6902 |
|        20 |             0.9967 |             0.0033 |             0.3142 |             0.6858 |

---

## get_vecm_forecast
Fit a Vector Error Correction Model (VECM) across every (cointegrated) ticker in the Toolkit instance and forecast `forecast_steps` periods ahead.

**Also known as:** VECM, error correction model (for the multivariate/cointegrated case).

A VECM keeps a VAR's short-run dynamics while ALSO letting each asset's price change react to how far the system currently sits from its long-run equilibrium (the cointegrating relationship(s) among the tickers, taken from `cointegration_model.get_johansen_cointegration`) -- see `time_series_model.get_vecm_forecast` for the full formula, estimation method and verification notes.

The formula is as follows:

$$
\text{Rank}\; r = \text{the number of leading Johansen trace statistics} \;(\text{det\_order} = 0,\; \text{k\_ar\_diff} \;\text{lags}) \;\text{that exceed their critical value at} \;\text{significance} \;(5\% \;\text{by default});\;\; r = 0 \;\text{raises an error}
$$

$$
\Delta Y_{t} = \alpha \cdot \beta' \cdot Y_{t-1} + \sum_{i=1}^{k} \Gamma_{i} \cdot \Delta Y_{t-i} + c + \epsilon_{t},\;\; \text{with } Y_{t} \text{ every ticker's column level (Adj Close by default)},\;\; k = \text{k\_ar\_diff} \;(1 \;\text{by default}) \;\text{and}\; c \;\text{a constant outside the cointegrating relation} \;(\text{statsmodels VECM with deterministic} = \text{"co"}),\;\; \text{fitted by Maximum Likelihood}
$$

- Forecast: the fitted recursion run forward `forecast_steps` periods, in levels

**Args:**

- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to model. Defaults to
"Adj Close" -- a VECM needs price LEVELS (non-stationary, cointegrated
series), not returns, the same input `get_johansen_cointegration` expects.
- <u>k_ar_diff (int, optional):</u> The number of lagged first differences to
include as short-run dynamics. Defaults to 1.
- <u>forecast_steps (int, optional):</u> The number of periods ahead to forecast.
Defaults to 5.
- <u>significance (float, optional):</u> The significance level (one of 0.01, 0.05,
0.10) at which the Johansen trace test determines the cointegrating rank.
Defaults to 0.05.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among
the tickers modeled jointly. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the
results to. Defaults to None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The `forecast_steps`-ahead forecast, on the price-level
scale, one column per ticker, indexed `1, ..., forecast_steps` (periods
ahead).

**Raises:**

ValueError: If the Johansen test does not reject a cointegrating rank of 0
for the Toolkit instance's tickers at `significance` -- a VECM is not
appropriate for non-cointegrated assets; use `get_var_forecast` on their
returns instead.

**Notes:**

- The method retrieves historical price data based on the specified `period`
for every ticker in the Toolkit instance and fits the VECM jointly across all
of them.
- Requires statsmodels (`pip install financetoolkit[econometrics]`).

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["GOOGL", "GOOG"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

# The two share classes of Alphabet are cointegrated: their prices cannot drift apart.
toolkit.econometrics.get_vecm_forecast()
```

Which returns:

|   Step |   GOOGL |    GOOG |
|-------:|--------:|--------:|
|      1 | 312.569 | 313.352 |
|      2 | 312.75  | 313.553 |
|      3 | 312.929 | 313.747 |
|      4 | 313.109 | 313.941 |
|      5 | 313.289 | 314.135 |

---

## get_forecast_error
Calculate the forecast error between every unordered pair of tickers' series in the Toolkit instance, the Root Mean Squared Error (method="rmse") or the Mean Absolute Error (method="mae").

This controller method compares two ASSETS' series directly, treating one as a naive "forecast" proxy for the other -- a simple, tracking-error style measure of how closely two series move together in absolute deviation terms (e.g. a portfolio versus a benchmark, or one asset as a naive stand-in forecast for a similar one). For evaluating an actual FORECASTING MODEL (ARIMA/VAR) rather than one asset as a naive proxy for another, use `get_out_of_sample_validation` instead.

The formula for method="rmse" is as follows:

$$
\text{RMSE} = \sqrt{\frac{1}{n} \cdot \sum(a_{t} - b_{t})^{2}},\;\; \text{with } a_{t} \text{ and } b_{t} \text{ the two tickers' column (Return by default) on the } n \text{ dates where both have data}
$$

The formula for method="mae" is as follows:

$$
\text{MAE} = \frac{1}{n} \cdot \sum\left|a_{t} - b_{t}\right|,\;\; \text{with } a_{t} \text{ and } b_{t} \text{ the two tickers' column (Return by default) on the } n \text{ dates where both have data}
$$

Both are expressed in the units of the series itself (e.g. a return difference) and answer "how far apart are the two series in a typical period"; a lower value means the two tickers track each other more closely. The RMSE squares the differences and is therefore dominated by a few large gaps, while in the MAE every difference counts in proportion to its size, so the MAE is robust to occasional outliers.

For a fund against its index the RMSE comes close to the tracking error but is not the same: the tracking error (`Performance.get_tracking_error`) is the Standard Deviation of the return differences, which leaves out their average, while the RMSE includes it. Both are per period, so a daily RMSE is usually multiplied by the square root of 252 to annualize it.

**Also known as:** RMSE, RMSD (Root Mean Squared Deviation), MAE, MAD (Mean Absolute Deviation), forecast accuracy.

**Args:**

- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to compare. Defaults to
"Return".
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the
tickers paired up. Defaults to False.
- <u>method (str, optional):</u> The error measure, "rmse" for the Root Mean Squared Error or
"mae" for the Mean Absolute Error. Defaults to "rmse".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the
results to. Defaults to None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series: The RMSE or the MAE (named "RMSE" or "MAE"), indexed by unordered
`(Ticker A, Ticker B)` pair.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["IVV", "VOO"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_forecast_error(include_benchmark=True)
```

Which returns:

|                      |   RMSE |
|:---------------------|-------:|
| ('IVV', 'VOO')       | 0.0004 |
| ('IVV', 'Benchmark') | 0.0009 |
| ('VOO', 'Benchmark') | 0.001  |

---

## get_out_of_sample_validation
Out-of-sample validate an ARIMA or VAR forecast of every ticker in the Toolkit instance -- fit only on a training portion of the history, forecast the held-out remainder, and score the forecast against what actually happened.

**Also known as:** hold-out validation, train/test split validation.

See `forecast_evaluation_model.get_out_of_sample_validation` for the general harness this wraps. Since that function takes a raw Python callable (not serializable for e.g. the MCP-facing tool layer), this controller method instead hardcodes the choice between the two Part-1 forecasting models via the `model` string:

- `model="arima"`: `time_series_model.get_arima_forecast` is fit on each ticker's own training-period series (`p`, `d`, `q`, `include_constant` control the model, same as `get_arima_forecast`).
- `model="var"`: `time_series_model.get_var_forecast` is fit on the training-period series of each ticker together with `other_tickers` (`lags` controls the VAR order, defaulting to every other ticker in the Toolkit instance if not given); only that ticker's own forecast column is scored against its holdout.

The formula is as follows:

- Training sample: the first int(`train_fraction`·n) observations (80% by default) of the `column` level (Adj Close by default); the remaining H observations are the holdout

- $$\hat{Y}_{t}$$: the H-step forecast of the model fitted on the training sample only, an ARIMA(p, d, q) (model="arima", ARIMA(1, 1, 1) by default) or a VAR(`lags`) on the ticker and `other_tickers` (model="var")

$$
\text{RMSE} = \sqrt{\frac{1}{H} \cdot \sum(Y_{t} - \hat{Y}_{t})^{2}}\;\;\text{and}\;\; \text{MAE} = \frac{1}{H} \cdot \sum\left|Y_{t} - \hat{Y}_{t}\right|,\;\; \text{over the holdout}
$$

**Args:**

- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to validate. Defaults
to "Adj Close".
- <u>model (str, optional):</u> Either "arima" or "var". Defaults to "arima".
- <u>train_fraction (float, optional):</u> The fraction of observations used for
training; the remainder is the holdout. Defaults to 0.8.
- <u>p (int, optional):</u> The ARIMA autoregressive order (`model="arima"` only).
Defaults to 1.
- <u>d (int, optional):</u> The ARIMA differencing order (`model="arima"` only).
Defaults to 1.
- <u>q (int, optional):</u> The ARIMA moving-average order (`model="arima"` only).
Defaults to 1.
- <u>include_constant (bool, optional):</u> Whether the ARIMA model estimates a
free intercept (`model="arima"` only). Defaults to True.
- <u>lags (int, optional):</u> The VAR order (`model="var"` only). Defaults to 1.
- <u>other_tickers (list[str] &#124; None, optional):</u> The other assets to include in
the VAR system alongside the ticker being validated (`model="var"` only).
Defaults to None, meaning every other ticker in the Toolkit instance.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among
the tickers validated (and, for `model="var"`, among the default
`other_tickers`). Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the
results to. Defaults to None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: `RMSE`, `MAE` and `Holdout Observations`, one column per
ticker. With `model="arima"` each ticker uses its own history and a ticker
without enough data has an empty (NaN) column.

**Raises:**

ValueError: If `model` is not "arima" or "var", or (for `model="var"`)
fewer than 2 tickers are available to form a VAR system.

**Notes:**

- Requires statsmodels with `model="arima"`, the default; `model="var"` does not
(`pip install financetoolkit[econometrics]`).

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["BTCUSD", "ETHUSD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_out_of_sample_validation()
```

Which returns:

|                      |   BTCUSD |   ETHUSD |
|:---------------------|---------:|---------:|
| RMSE                 | 11424.9  |  1003.11 |
| MAE                  |  9896.95 |   842.37 |
| Holdout Observations |   366    |   366    |

---

## get_berkowitz_test
Test the one-period-ahead density forecasts of a return model with Berkowitz's likelihood ratio test.

A Value at Risk backtest only looks at one quantile; a density forecast says how likely every return is. The test transforms each realized return with the distribution function of its forecast (the probability integral transform, PIT), which is uniform and independent over time when the forecasts are right, takes the normal quantile of the PITs and tests whether those are independent standard normal: a mean away from 0 means the forecasts are biased, a standard deviation above 1 that they understate the risk and an autocorrelation that they miss its dynamics. With `alpha`, only the tail below the alpha quantile is tested, the part a Value at Risk at `alpha` depends on.

The formula is as follows (with the default model="garch" and daily returns, for which the window is 504):

$$
\text{PIT}_{t} = F\left(\frac{\text{Return}_{t} - \text{Mu}}{\text{Volatility}_{t}}\right),\;\; \text{from a GARCH(1, 1) with normal innovations fitted on the 504 returns before } t \text{, refitted every 21 returns}
$$

$$
z_{t} = \Phi^{-1} (\text{PIT}_{t})\;\;\text{and}\;\; z_{t} - \mu = \rho (z_{t-1} - \mu) + \epsilon_{t},\;\; \text{with}\; \epsilon_{t} \sim N(0,\; \sigma^{2})
$$

$$
\text{Berkowitz Statistic} = - 2 (\ln L(0,\; 1,\; 0) - \ln L(\hat{\mu},\; \hat{\sigma},\; \hat{\rho})),\;\; \text{compared with a } \chi^{2} \text{ distribution with 3 degrees of freedom}
$$

$$
\text{With alpha:}\;\; \text{every}\; z_{t} \;\text{above}\; q = \Phi^{-1} (\alpha) \;\text{is censored at}\; q,\;\; \text{the AR}(1) \;\text{term is left out and the statistic} \;\mathord{-} 2 (\ln L(0,\; 1) - \ln L(\hat{\mu},\; \hat{\sigma})) \;\text{is compared with}\; a \chi^{2} \;\text{distribution with 2 degrees of freedom}
$$

Where L is the exact Gaussian AR(1) likelihood (see `forecast_evaluation_model.get_berkowitz_test`) and F the distribution function of the standardized innovations with their fitted Shape and Skew. model="gaussian" uses a normal distribution with the mean and standard deviation (ddof=1) of the `window_size` returns before t and model="ewma" a normal distribution with mean zero and the RiskMetrics variance with decay `lambda_`.

For more information about the method, see the following papers:

- Berkowitz, J. (2001). "Testing Density Forecasts, With Applications to Risk Management." Journal of Business & Economic Statistics, 19(4), 465-474.
- Diebold, F.X., Gunther, T.A. and Tay, A.S. (1998). "Evaluating Density Forecasts with Applications to Financial Risk Management." International Economic Review, 39(4), 863-883.
- rugarch: BerkowitzTest ([https://cran.r-project.org/package=rugarch](https://cran.r-project.org/package=rugarch){:target="_blank"}).

**Also known as:** density forecast test, PIT test, Berkowitz LR test.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly or yearly).
Defaults to "daily".
- <u>model (str, optional):</u> The density forecast, "garch", "gaussian" or "ewma". Defaults to "garch".
- <u>alpha (float &#124; None, optional):</u> The tail probability of the tail test. Defaults to None, which tests
the whole density.
- <u>window_size (int &#124; None, optional):</u> The number of returns of every window or GARCH fit. Defaults to
None, which uses two years of observations with a minimum of 100 for "garch" (504 daily returns) and
a year with a minimum of 20 for "gaussian".
- <u>lambda_ (float, optional):</u> The decay factor of model="ewma". Defaults to 0.94.
- <u>refit_every (int, optional):</u> The number of returns between two GARCH fits. Defaults to 21.
- <u>garch_method (str, optional):</u> The GARCH variance model, one of the methods of `Risk.get_garch`.
Defaults to "garch".
- <u>garch_distribution (str, optional):</u> The GARCH innovation distribution (normal, t, skewt,
skewt_fernandez_steel, ged or johnson_su). Defaults to "normal".
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the assets tested. Defaults
to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The Berkowitz statistic, its p-value, the fitted Mean, Standard Deviation and
Autocorrelation (NaN for the tail test) of z, the number of observations and, with `alpha`, of
tail observations, per asset.

**Notes:**

- Every forecast only uses the returns before it, and each asset uses its own return history.
- rugarch's BerkowitzTest fits the AR(1) by least squares, conditional on the first observation; the
statistic here maximizes the exact likelihood of the paper, which differs by about 1% of the statistic
on 800 observations.
- A GARCH fit takes one to five seconds per asset and every refit a fraction of a second.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["QQQ", "TLT", "GLD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2019-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_berkowitz_test()
```

Which returns:

|                     |       QQQ |       TLT |       GLD |
|:--------------------|----------:|----------:|----------:|
| Berkowitz Statistic |    8.5086 |    3.9236 |    3.8163 |
| P-Value             |    0.0366 |    0.2698 |    0.282  |
| Mean                |   -0.0443 |   -0.0153 |    0.0396 |
| Standard Deviation  |    1.0494 |    0.9641 |    1.0273 |
| Autocorrelation     |   -0.0028 |   -0.0176 |    0.002  |
| Observations        | 1255      | 1255      | 1255      |

---

## get_hong_li_test
Test the one-period-ahead density forecasts of a return model with the nonparametric test of Hong and Li.

Correct density forecasts turn the realized returns into probability integral transforms (PITs) that are independent and uniform on (0, 1), so every pair of a PIT and the PIT j periods before it is spread evenly over the unit square. The test estimates the joint density of those pairs with a kernel and measures how far it is from flat, for every lag: a forecast density of the wrong shape (too thin tails, a missed skew) and dependence the model misses (volatility clustering it does not follow) both move it away. Where `get_berkowitz_test` checks the mean, variance and first autocorrelation of the normal quantiles of the PITs, this test looks at the whole joint density.

The formula is as follows (with the default model="garch" and daily returns, for which the window is 504):

$$
\text{PIT}_{t} = F\left(\frac{\text{Return}_{t} - \text{Mu}}{\text{Volatility}_{t}}\right),\;\; \text{from a GARCH(1, 1) with normal innovations fitted on the 504 returns before } t \text{, refitted every 21 returns (see get\_berkowitz\_test)}
$$

$$
g_{j}(x_{1},\; x_{2}) = \frac{\Sigma_{t} K_{h}(x_{1},\; \text{PIT}_{t}) K_{h}(x_{2},\; \text{PIT}_{t-j})}{n - j},\;\; \text{with}\;\; K_{h} \;\text{the boundary-modified quartic kernel and}\; h = S n^{- \frac{1}{6}},\;\; S \text{ the standard deviation of the PITs}
$$

$$
M(j) = \text{∫∫} \;(g_{j}(x_{1},\; x_{2}) - 1)^{2} \,\mathrm{d}x_{1} \,\mathrm{d}x_{2} \;\text{over the unit square}
$$

$$
Q(j) = \frac{h ((n - j) M(j) - A_{h})}{\sqrt{V}} \;\text{}_{0} \;\text{for}\; j = 1,\; \ldots,\; \text{lags}
$$

$$
W = \frac{\Sigma_{j} Q(j)}{\text{√} \;\text{lags}},\;\; \text{the portmanteau statistic}
$$

Where $$A_{h}$$ and $$V_{0}$$ are the centring and scaling constants of Hong and Li (2005), see `forecast_evaluation_model.get_hong_li_test`. Only large values reject. The statistics are standard normal under the null only as the sample grows, and slowly, so the p-values come from their distribution simulated under the null (independent uniform PITs) for the same number of PITs and lags, see `forecast_evaluation_model.get_hong_li_p_value`. model="gaussian" and model="ewma" give the density forecasts of `get_berkowitz_test`.

For more information about the method, see the following papers:

- Hong, Y. and Li, H. (2005). "Nonparametric Specification Testing for Continuous-Time Models with Applications to Term Structure of Interest Rates." The Review of Financial Studies, 18(1), 37-84.
- Diebold, F.X., Gunther, T.A. and Tay, A.S. (1998). "Evaluating Density Forecasts with Applications to Financial Risk Management." International Economic Review, 39(4), 863-883.
- Referenced against HLTest of R's rugarch ([https://cran.r-project.org/package=rugarch](https://cran.r-project.org/package=rugarch){:target="_blank"}) as its documentation defines it.

**Also known as:** Hong-Li test, nonparametric density forecast test, PIT independence and uniformity test, HL portmanteau test.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly or yearly).
Defaults to "daily".
- <u>model (str, optional):</u> The density forecast, "garch", "gaussian" or "ewma". Defaults to "garch".
- <u>lags (int, optional):</u> The number of lags of the portmanteau statistic. Defaults to 4.
- <u>window_size (int &#124; None, optional):</u> The number of returns of every window or GARCH fit. Defaults to
None, which uses two years of observations with a minimum of 100 for "garch" (504 daily returns) and
a year with a minimum of 20 for "gaussian".
- <u>lambda_ (float, optional):</u> The decay factor of model="ewma". Defaults to 0.94.
- <u>refit_every (int, optional):</u> The number of returns between two GARCH fits. Defaults to 21.
- <u>garch_method (str, optional):</u> The GARCH variance model, one of the methods of `Risk.get_garch` other
than "realized". Defaults to "garch".
- <u>garch_distribution (str, optional):</u> The GARCH innovation distribution (normal, t, skewt,
skewt_fernandez_steel, ged or johnson_su). Defaults to "normal".
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the assets tested. Defaults
to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The statistic Q(j) and its p-value for every lag, the portmanteau W and its p-value,
the bandwidth and the number of observations, per asset.

**Notes:**

- Every forecast only uses the returns before it, and each asset uses its own return history.
- The asymptotic normal distribution is reached slowly: on simulated independent uniform PITs every Q(j)
has a mean of about 0 and a standard deviation of about 1.2 at 500 to 2,000 observations, and as the
Q(j) share the estimate of the marginal density of the PITs (a correlation of about 0.45), W has one of
about 1.8 with 4 lags. Compared with the standard normal distribution W would reject a correct model at
5% about 16% to 20% of the time; with the simulated null distribution about 4.4% (1,000 PITs). The
simulation treats the PITs as those of a known model: estimating the model parameters does not change
the asymptotic distribution (Hong and Li, 2005), and the GARCH parameters here come from the returns
before each forecast.
- A GARCH fit takes one to five seconds per asset and every refit a fraction of a second.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["QQQ", "TLT", "GLD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2019-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_hong_li_test()
```

Which returns:

|                |       QQQ |       TLT |       GLD |
|:---------------|----------:|----------:|----------:|
| Q(1) Statistic |    7.1786 |    4.2855 |    4.451  |
| Q(1) P-Value   |    0      |    0.0016 |    0.0012 |
| Q(2) Statistic |    4.7805 |    2.5799 |    3.4082 |
| Q(2) P-Value   |    0.0006 |    0.0273 |    0.0075 |
| Q(3) Statistic |    3.666  |    2.833  |    2.463  |
| Q(3) P-Value   |    0.0049 |    0.0187 |    0.0323 |
| Q(4) Statistic |    4.8672 |    2.2805 |    5.7016 |
| Q(4) P-Value   |    0.0006 |    0.0418 |    0.0001 |
| W Statistic    |   10.2461 |    5.9894 |    8.0119 |
| W P-Value      |    0.0001 |    0.005  |    0.0007 |
| Bandwidth      |    0.0855 |    0.0855 |    0.0847 |
| Observations   | 1255      | 1255      | 1255      |

---

## get_directional_accuracy_test
Test whether a return forecast predicts the direction of the next return better than chance, with the Pesaran-Timmermann or the Anatolyev-Gerko test.

A forecast that is right about the sign more than half of the time is not necessarily useful: in a rising market a forecast that is always positive is right on most days. The Pesaran-Timmermann test compares the share of correct signs with the share expected if the forecast and the returns were independent. The Anatolyev-Gerko test weighs each sign by the size of the return: it is the excess return of going long when the forecast is positive and short when it is negative over that of the same share of long positions held at random, so it asks whether the forecast would have made money.

The formula is as follows (with the default forecast="momentum" and daily returns, for which the window is 252):

$$
\text{Forecast}_{t} = \operatorname{mean}(\text{Return}_{t-252},\; \ldots,\; \text{Return}_{t-1})
$$

$$
P = \frac{1}{n} \sum 1 \{\text{Forecast}_{t} \cdot \text{Return}_{t} > 0\},\;\; P^{*} = P_{y} P_{x} + (1 - P_{y}) (1 - P_{x})
$$

$$
\text{Pesaran-Timmermann Statistic} = \frac{P - P^{*}}{\sqrt{V(P) - V(P^{*})}}
$$

$$
\text{Anatolyev-Gerko Statistic} = \frac{A - B}{\sqrt{V}},\;\; \text{with}\;\; A = \frac{1}{n} \sum \;\operatorname{sign}(\text{Forecast}_{t}) \;\text{Return}_{t}\;\;\text{and}\;\; B = \operatorname{mean}(\operatorname{sign}(\text{Forecast})) \cdot \operatorname{mean}(\text{Return})
$$

$$
\text{P-Value} = P(N(0,\; 1) > \text{Statistic})
$$

Where $$P_{y}$$ and $$P_{x}$$ are the shares of positive returns and forecasts, $$V (P) = P^{*} (1 - P^{*}) / n$$, V(P*) = (2 P_y - 1)^2 $$P_{x} (1 - P_{x}) / n$$ + (2 P_x - 1)^2 $$P_{y} (1 - P_{y}) / n + 4 P_{y} P_{x} (1 - P_{y}) (1 - P_{x}) / n^{2}$$ and $$V = 4 p (1 - p) \Sigma$$ (Return_t - mean(Return))^2 / $$n^{2}$$ with p = (1 + mean(sign(Forecast))) / 2. forecast="autoregressive" forecasts each return with a + b · Return_(t-1), the least-squares AR(1) over the `window_size` pairs of returns before it. Both statistics are standard normal under the null hypothesis of no directional predictability; the p-value is one-sided.

For more information about the methods, see the following papers:

- Pesaran, M.H. and Timmermann, A. (1992). "A Simple Nonparametric Test of Predictive Performance." Journal of Business & Economic Statistics, 10(4), 461-465.
- Anatolyev, S. and Gerko, A. (2005). "A Trading Approach to Testing for Predictability." Journal of Business & Economic Statistics, 23(4), 455-461.
- Moskowitz, T.J., Ooi, Y.H. and Pedersen, L.H. (2012). "Time Series Momentum." Journal of Financial Economics, 104(2), 228-250.
- rugarch: DACTest ([https://cran.r-project.org/package=rugarch](https://cran.r-project.org/package=rugarch){:target="_blank"}).

**Also known as:** directional accuracy test, market timing test, sign test, PT test, AG test, DAC test.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly or yearly).
Defaults to "daily".
- <u>method (str, optional):</u> The test, "pesaran_timmermann" or "anatolyev_gerko". Defaults to
"pesaran_timmermann".
- <u>forecast (str, optional):</u> The return forecast, "momentum" (the mean of the previous `window_size`
returns) or "autoregressive" (the rolling AR(1)). Defaults to "momentum".
- <u>window_size (int &#124; None, optional):</u> The number of returns of every forecast window. Defaults to None,
which uses a year of observations with a minimum of 20 (252 daily, 52 weekly and 20 monthly,
quarterly or yearly returns).
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the assets tested. Defaults
to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The statistic, its one-sided p-value, the Directional Accuracy (the share of correctly
predicted signs) and the number of observations, per asset.

**Notes:**

- Every forecast only uses the returns before it, and each asset uses its own return history.
- A return or forecast of exactly zero counts as a wrong sign in P and as no position in A.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["QQQ", "TLT", "GLD", "USO"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2010-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_directional_accuracy_test(period="monthly", window_size=12)
```

Which returns:

|                              |      QQQ |      TLT |      GLD |      USO |
|:-----------------------------|---------:|---------:|---------:|---------:|
| Pesaran-Timmermann Statistic |   0.7683 |  -1.195  |   1.307  |  -0.9591 |
| P-Value                      |   0.2211 |   0.8839 |   0.0956 |   0.8312 |
| Directional Accuracy         |   0.6313 |   0.4581 |   0.5475 |   0.4637 |
| Observations                 | 179      | 179      | 179      | 179      |

---

## get_model_confidence_set
Find the volatility forecasting models that cannot be told apart from the best one with the Model Confidence Set (MCS) of Hansen, Lunde and Nason.

The Diebold-Mariano test compares two forecasts; the MCS compares any number of them. Every model forecasts the next period's variance of each asset from the returns before it, and its loss against the squared return is recorded. Starting from all models, the MCS tests whether they are equally good and, if not, eliminates the worst and tests again, until the remaining models cannot be told apart. The models left over form a set that contains the best model with a probability of at least 1 - alpha; the MCS p-value of a model says at which size it would leave the set.

The formula is as follows (with the defaults statistic="max", loss="qlike" and daily returns):

$$
\text{Loss}_{i,t} = \frac{\text{Return}_{t}^{2}}{\text{Forecast}_{i,t}} + \ln(\text{Forecast}_{i,t}),\;\; \text{or}\;\; (\text{Return}_{t}^{2} - \text{Forecast}_{i,t})^{2} \;\text{with loss} = \text{"squared"}
$$

$$
d_{i} = \operatorname{mean}(\text{Loss}_{i}) - \frac{1}{m} \Sigma_{j} \;\text{mean}(\text{Loss}_{j})\;\;\text{and}\;\; t_{i} = \frac{d_{i}}{\sqrt{\operatorname{Var}(d_{i})}}
$$

$$
T = \max_{i} t_{i},\;\; \text{with}\;\; \text{P-Value} = \frac{1}{B} \Sigma_{b} 1 \{T^{*}_{b} \geq T\} \;\text{over}\; B \;\text{stationary bootstrap resamples}
$$

- while the p-value is below alpha, the model with the largest $$t_{i}$$ is eliminated and the test repeated

$$
\text{MCS P-Value of a model} = \text{the largest p-value of the steps up to its elimination} \;(1 \;\text{for the last model})
$$

Where m is the number of models still in the set, $$\operatorname{Var} (d_{i})$$ the bootstrap variance of $$d_{i}$$ and T*_b the statistic of the b-th resample centered at the full sample (see `forecast_evaluation_model.get_model_confidence_set`, also for statistic="range", the largest $$\vert t_{ij} \vert$$ of all pairs). The forecasts of the models are:

- "ewma": the RiskMetrics variance $$\lambda \cdot \sigma_{t - 1}^{2} + (1 - \lambda) \cdot r_{t - 1}^{2}$$ with $$\lambda$$ = `lambda_`
- "rolling": the sample variance (ddof=1) of the `window_size` returns before t
- "garch", "gjr" and the other methods of `Risk.get_garch`: the one-step variance of the GARCH-family model with a constant mean and normal innovations (quasi-maximum likelihood), refitted every `refit_every` returns on the `garch_window_size` returns before t

Every model is compared on the dates all of them have a forecast. The squared-error loss and QLIKE rank volatility forecasts correctly with the squared return as a noisy proxy of the true variance (Patton 2011); QLIKE (written without the terms that do not depend on the forecast) is less sensitive to the largest returns.

For more information about the method, see the following papers:

- Hansen, P.R., Lunde, A. and Nason, J.M. (2011). "The Model Confidence Set." Econometrica, 79(2), 453-497.
- Patton, A.J. (2011). "Volatility Forecast Comparison Using Imperfect Volatility Proxies." Journal of Econometrics, 160(1), 246-256.
- arch: MCS ([https://arch.readthedocs.io](https://arch.readthedocs.io){:target="_blank"}) and rugarch: mcsTest ([https://cran.r-project.org/package=rugarch](https://cran.r-project.org/package=rugarch){:target="_blank"}).

**Also known as:** MCS, model confidence set, Hansen-Lunde-Nason test, forecast model selection.

**Args:**

- <u>period (str, optional):</u> The data frequency for returns (daily, weekly, monthly, quarterly or yearly).
Defaults to "daily".
- <u>models (list[str] &#124; None, optional):</u> The forecasting models to compare, at least two of "ewma",
"rolling" and the methods of `Risk.get_garch` (such as "garch" and "gjr"). Defaults to None, which
compares "ewma", "rolling", "garch" and "gjr".
- <u>loss (str, optional):</u> The loss of a forecast, "qlike" or "squared". Defaults to "qlike". The squared
losses of daily variances are of the order of 1e-7, so they need a larger `rounding` to show.
- <u>statistic (str, optional):</u> The test statistic, "max" or "range". Defaults to "max".
- <u>alpha (float, optional):</u> The size of the test. Defaults to 0.1, the 90% model confidence set.
- <u>n_bootstrap (int, optional):</u> The number of bootstrap resamples. Defaults to 1000.
- <u>block_size (int &#124; None, optional):</u> The average block length of the stationary bootstrap. Defaults to
None, which uses the cube root of the number of periods, rounded.
- <u>window_size (int, optional):</u> The window of the "rolling" model. Defaults to 22 (about a month).
- <u>lambda_ (float, optional):</u> The decay factor of the "ewma" model. Defaults to 0.94.
- <u>garch_window_size (int &#124; None, optional):</u> The number of returns of every GARCH fit. Defaults to None,
which uses two years of observations with a minimum of 100 (504 daily returns).
- <u>refit_every (int, optional):</u> The number of returns between two GARCH fits. Defaults to 21.
- <u>random_state (int, optional):</u> The seed of the bootstrap. Defaults to 42.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the assets. Defaults to
False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per asset and model the Average Loss, the MCS P-Value, whether the model is In
Confidence Set and its Rank (1 for the last model standing).

**Notes:**

- Every forecast only uses the returns before it, and each asset uses its own return history.
- A GARCH fit takes one to five seconds per asset and every refit a fraction of a second.
- In samples of a few hundred periods statistic="range" eliminates a model too often (about 14% of the
time at alpha=0.1 with four equally good models over 250 periods, against 8% for "max"), a property of
the range statistic with the stationary bootstrap that arch's MCS shares; prefer "max" for short
samples.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["QQQ", "TLT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2019-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_model_confidence_set()
```

Which returns:

|                    |   Average Loss |   MCS P-Value | In Confidence Set   |   Rank |
|:-------------------|---------------:|--------------:|:--------------------|-------:|
| ('QQQ', 'gjr')     |        -7.7142 |         1     | True                |      1 |
| ('QQQ', 'ewma')    |        -7.67   |         0.25  | True                |      2 |
| ('QQQ', 'garch')   |        -7.6562 |         0.25  | True                |      3 |
| ('QQQ', 'rolling') |        -7.6442 |         0.206 | True                |      4 |
| ('TLT', 'ewma')    |        -8.2518 |         1     | True                |      1 |
| ('TLT', 'garch')   |        -8.2407 |         0.576 | True                |      2 |
| ('TLT', 'gjr')     |        -8.2405 |         0.576 | True                |      3 |
| ('TLT', 'rolling') |        -8.2155 |         0.101 | True                |      4 |

---

## get_ols
Fit an Ordinary Least Squares (OLS) regression of `dependent_ticker` on `independent_tickers`, using the selected `column` (returns by default) of each ticker.

OLS estimates the coefficients that minimise the sum of squared residuals, i.e. the line (or plane) that best explains the dependent ticker from the independent tickers.

The formula is as follows:

$$
\hat{\beta} = (X' X)^{- 1} X' y,\;\; \text{with } y \text{ the dependent ticker's column (Return by default) and } X \text{ the independent tickers' column plus a constant column (add\_constant=True)}
$$

$$
\operatorname{Cov}(\hat{\beta}) = \hat{\sigma}^{2} \cdot (X' X)^{- 1},\;\; \text{with}\;\; \hat{\sigma}^{2} = \frac{e' e}{n - k} \;(\text{cov\_type} = \text{"nonrobust"})
$$

$$
\operatorname{Cov}(\hat{\beta}) = (X' X)^{- 1} \cdot (\sum \omega_{t} \cdot x_{t}x_{t}') \cdot (X' X)^{- 1} \;\text{for}\; \text{"HC0"} \;\text{to}\; \text{"HC3"},\;\; \text{with}\;\; \omega_{t} = e_{t}^{2}(\text{HC0}),\;\; \frac{e_{t}^{2} \cdot n}{n - k} \;(\text{HC1}),\;\; \frac{\frac{e_{t}^{2}}{(1 - h_{t}) \;(\text{HC2}) \;\text{or}\; e_{t}^{2}}}{(1 - h_{t})^{2}(\text{HC3}) \;\text{and}\; h_{t}} = x_{t}'(X' X)^{- 1} x_{t}
$$

$$
\operatorname{Cov}(\hat{\beta}) = (X' X)^{- 1} \cdot \left(\sum_{t} g_{t}g_{t}' + \sum_{j}\left(1 - \frac{j}{L + 1}\right) \cdot \sum_{t}(g_{t}g_{t-j}' + g_{t-j}g_{t}')\right) \cdot (X' X)^{- 1} \;\text{for}\; \text{"HAC"},\;\; \text{with}\;\; g_{t} = x_{t}e_{t}\;\;\text{and}\;\; L = \text{maxlags};\;\; \frac{\frac{\text{"cluster"} \;\text{sums}\; g_{t} \;\text{within each cluster and scales the sandwich by} \;G}{G - 1} \cdot (n - 1)}{n - k},\;\; \text{with } G \text{ the number of clusters}
$$

$$
t = \frac{\hat{\beta}_{j}}{\operatorname{SE}(\hat{\beta}_{j})},\;\; \text{with p-values from a Student-t distribution with}\; n - k \;\text{degrees of freedom for}\; \text{cov\_type} = \text{"nonrobust"} \;\text{and from the standard normal distribution for the robust estimators} \;(\text{"HC0"} \;\text{to}\; \text{"HC3"},\; \text{"cluster"} \;\text{and}\; \text{"HAC"}),\;\; \text{which are asymptotic results}
$$

$$
R^{2} = 1 - \frac{e' e}{\sum(y_{t} - \operatorname{mean}(y))^{2}}
$$

The "HAC" covariance is the Newey-West (Bartlett) estimator without a small-sample degrees-of-freedom correction (statsmodels' default), so its standard errors are slightly smaller than those of software that scales them by n / (n - k).

Each coefficient is the expected change in `dependent_ticker` for a one-unit change in that independent ticker, holding the others fixed, and the intercept is what remains when all of them are zero. With returns this is the familiar way to estimate how strongly one asset moves with others (e.g. a beta against an index).

Under the classical assumptions (linearity, no perfect multicollinearity, homoskedastic and uncorrelated errors) OLS is the Best Linear Unbiased Estimator (Gauss-Markov). The coefficients stay unbiased when the errors are heteroskedastic, but the classical standard errors do not: check with `get_heteroskedasticity_test` and, if needed, refit with a robust `cov_type` such as "HC1" (or "HC3" for small samples), or "HAC" when the errors are also autocorrelated.

For more information about the HAC covariance, see the following paper:

- Newey, W.K. & West, K.D. (1987). "A Simple, Positive Semi-Definite, Heteroskedasticity and Autocorrelation Consistent Covariance Matrix." Econometrica, 55(3), 703-708.

**Also known as:** linear regression, least squares regression.

**Args:**

- <u>dependent_ticker (str &#124; None, optional):</u> The dependent (predicted) asset.
Defaults to None, meaning the Toolkit instance's first ticker.
- <u>independent_tickers (str &#124; list[str] &#124; None, optional):</u> The independent
(predictor) asset(s). Defaults to None, meaning every other ticker in
the Toolkit instance besides `dependent_ticker`.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" in the
default independent ticker(s) (has no effect when independent_tickers is given
explicitly). Defaults to False.
- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to regress on. Defaults to "Return".
- <u>add_constant (bool, optional):</u> Whether to include an intercept. Defaults to True.
- <u>cov_type (str, optional):</u> Which covariance estimator to use for the standard errors --
one of "nonrobust" (classical, assumes homoskedastic errors), "HC0"/"HC1"/"HC2"/"HC3"
(heteroskedasticity-robust), "cluster" (cluster-robust, requires `clusters`) or "HAC"
(Newey-West, heteroskedasticity-and-autocorrelation-consistent, uses `maxlags`).
Use `get_heteroskedasticity_test` to check for heteroskedasticity and
`get_ljung_box_test` to check for autocorrelation first. Defaults to "nonrobust".
- <u>clusters (pd.Series &#124; None, optional):</u> The cluster label for each observation
(e.g. a coarser time bucket derived from the return index, to correct for
within-period correlation), required when `cov_type="cluster"`. Aligned to the
regression's own index before use, so it may be indexed by the full period
index even though the regression drops periods with missing data. Defaults
to None.
- <u>maxlags (int &#124; None, optional):</u> The maximum lag to include when estimating the
HAC (Newey-West) covariance matrix, only used when `cov_type="HAC"`. Defaults to
None, meaning the Newey & West (1994) rule of thumb `floor(4 * (n / 100)^(2/9))`
with `n` the number of observations.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: A coefficient table (Coefficient, Std. Error, t-Statistic, P-Value),
indexed by regressor name.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["XOM", "USO"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

# XOM (the first ticker) is dependent; USO and the Benchmark are independent.
# dependent_ticker and independent_tickers choose others, cov_type='HC1' gives
# heteroskedasticity-robust and cov_type='HAC' (with maxlags) Newey-West standard errors.
toolkit.econometrics.get_ols(include_benchmark=True)
```

Which returns:

|           |   Coefficient |   Std. Error |   t-Statistic |   P-Value |
|:----------|--------------:|-------------:|--------------:|----------:|
| Intercept |        0.0005 |       0.0004 |        1.5047 |    0.1327 |
| USO       |        0.4878 |       0.0172 |       28.4214 |    0      |
| Benchmark |        0.366  |       0.0333 |       10.9991 |    0      |

---

## get_wls
Fit a Weighted Least Squares (WLS) regression of `dependent_ticker` on `independent_tickers`.

When the error variance differs across observations (heteroskedasticity) with a known or estimable structure, `Var(e_i) = sigma^2 / w_i`, OLS remains unbiased but is no longer the most efficient estimator. WLS restores efficiency by minimising the weighted sum of squared residuals, so noisier observations (low weight) count less than precise ones (high weight).

The formula is as follows:

$$
\hat{\beta} = (X' W X)^{- 1} X' W y,\;\; \text{with}\;\; W = \operatorname{diag}(\text{weights}),\;\; \text{the same as OLS of} \;\sqrt{w_{t}} \cdot y_{t} \;\text{on} \;\sqrt{w_{t}} \cdot x_{t}
$$

$$
\operatorname{Cov}(\hat{\beta}) = \hat{\sigma}^{2} \cdot (X' W X)^{- 1},\;\; \text{with}\;\; \hat{\sigma}^{2} = \frac{\sum w_{t} \cdot e_{t}^{2}}{n - k} \;(\text{cov\_type} = \text{"nonrobust"})
$$

$$
t = \frac{\hat{\beta}_{j}}{\operatorname{SE}(\hat{\beta}_{j})},\;\; \text{with p-values from a Student-t distribution with}\; n - k \;\text{degrees of freedom for}\; \text{cov\_type} = \text{"nonrobust"} \;\text{and from the standard normal distribution for the robust estimators};\;\; \text{"HAC" is the Newey-West estimator without a small-sample correction}
$$

- y is the dependent ticker's `column` (Return by default) and X the independent tickers' `column` plus a constant, on the dates where the returns and `weights` all have data

With equal weights WLS reduces to OLS. A typical use is down-weighting periods of high volatility, so that a few turbulent periods do not dominate the estimated relationship. By default (weights="feasible") the weights are estimated from the regression itself with the feasible GLS procedure of Wooldridge (2016): the logarithm of the squared OLS residuals is regressed on the independent tickers, and each period's weight is 1 / exp(fitted value), the inverse of its estimated error variance. Use `get_heteroskedasticity_test` to establish whether heteroskedasticity is present before choosing WLS over OLS.

For more information about the feasible weights, see the following book:

- Wooldridge, J.M. (2016). "Introductory Econometrics: A Modern Approach", 6th edition, Section 8.4. Cengage Learning.

**Also known as:** weighted regression, feasible WLS.

**Args:**

- <u>weights (pd.Series &#124; str, optional):</u> The (positive) weight of each observation,
aligned to the same period index as the return data (e.g. `1 / rolling_variance`),
or "feasible" to estimate them from the regression's own residuals with the
feasible GLS procedure of Wooldridge (2016). Defaults to "feasible".
- <u>dependent_ticker (str &#124; None, optional):</u> The dependent (predicted) asset.
Defaults to None, meaning the Toolkit instance's first ticker.
- <u>independent_tickers (str &#124; list[str] &#124; None, optional):</u> The independent
(predictor) asset(s). Defaults to None, meaning every other ticker in
the Toolkit instance besides `dependent_ticker`.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" in the
default independent ticker(s) (has no effect when independent_tickers is given
explicitly). Defaults to False.
- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to regress on. Defaults to "Return".
- <u>add_constant (bool, optional):</u> Whether to include an intercept. Defaults to True.
- <u>cov_type (str, optional):</u> Which covariance estimator to use, applied to the weighted/
transformed problem -- see `get_ols`'s `cov_type` for the full list of options.
Defaults to "nonrobust".
- <u>clusters (pd.Series &#124; None, optional):</u> The cluster label for each observation,
required when `cov_type="cluster"`. Defaults to None.
- <u>maxlags (int &#124; None, optional):</u> The maximum lag to include when estimating the
HAC (Newey-West) covariance matrix, only used when `cov_type="HAC"`. Defaults to
None, meaning the Newey & West (1994) rule of thumb (see `get_ols`).
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: A coefficient table (Coefficient, Std. Error, t-Statistic, P-Value),
indexed by regressor name.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

# AAPL (the first ticker) is dependent, MSFT is independent; the weights are estimated
toolkit.econometrics.get_wls(period="weekly")
```

Which returns:

|           |   Coefficient |   Std. Error |   t-Statistic |   P-Value |
|:----------|--------------:|-------------:|--------------:|----------:|
| Intercept |        0.0012 |       0.0019 |        0.6263 |    0.5317 |
| MSFT      |        0.6356 |       0.0596 |       10.6643 |    0      |

---

## get_gls
Fit a Generalized Least Squares (GLS) regression of `dependent_ticker` on `independent_tickers`, given a known error covariance structure `omega`.

GLS generalises WLS to an arbitrary error covariance matrix `Var(e) = sigma^2 * Omega`. Where WLS only corrects for heteroskedasticity (a diagonal `Omega`), GLS also corrects for correlation between the errors of different observations, such as the autocorrelation that is common in financial time series (a non-diagonal `Omega`).

The formula is as follows:

$$
\hat{\beta} = (X' \Omega^{- 1} X)^{- 1} X' \Omega^{- 1} y
$$

$$
\operatorname{Cov}(\hat{\beta}) = \hat{\sigma}^{2} \cdot (X' \Omega^{- 1} X)^{- 1},\;\; \text{with}\;\; \hat{\sigma}^{2} = \frac{e' \Omega^{- 1} e}{n - k}
$$

- y is the dependent ticker's `column` (Return by default) and X the independent tickers' `column` plus a constant (add_constant=True)

Under a correctly specified `Omega` this is the most efficient linear unbiased estimator. By default (omega="ar1") `Omega` is estimated from the regression itself as an AR(1) error structure, $$e_{t} = \rho \cdot e_{t - 1} + u_{t}$$: $$\rho$$ is the slope of the OLS residuals on their own lag and $$\Omega_{ij} = \rho^{\vert i - j \vert}$$, which makes this the Prais-Winsten estimator. Any other structure can be supplied as `omega`. `get_durbin_watson_test` helps establish whether the residuals are autocorrelated in the first place.

For more information about the method, see the following paper:

- Aitken, A.C. (1935). "On Least Squares and Linear Combinations of Observations." Proceedings of the Royal Society of Edinburgh, 55, 42-48.
- Prais, S.J. and Winsten, C.B. (1954). "Trend Estimators and Serial Correlation." Cowles Commission Discussion Paper No. 383.

**Also known as:** GLS, Prais-Winsten.

**Args:**

- <u>omega (pd.DataFrame &#124; str, optional):</u> The (symmetric, positive-definite) error
covariance structure, up to a scalar, shape `(n, n)`, or "ar1" to estimate an
AR(1) structure from the regression's own residuals (Prais-Winsten). Defaults
to "ar1".
- <u>dependent_ticker (str &#124; None, optional):</u> The dependent (predicted) asset.
Defaults to None, meaning the Toolkit instance's first ticker.
- <u>independent_tickers (str &#124; list[str] &#124; None, optional):</u> The independent
(predictor) asset(s). Defaults to None, meaning every other ticker in
the Toolkit instance besides `dependent_ticker`.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" in the
default independent ticker(s) (has no effect when independent_tickers is given
explicitly). Defaults to False.
- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to regress on. Defaults to "Return".
- <u>add_constant (bool, optional):</u> Whether to include an intercept. Defaults to True.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: A coefficient table (Coefficient, Std. Error, t-Statistic, P-Value),
indexed by regressor name.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

# AAPL (the first ticker) is dependent, MSFT is independent; Omega is estimated (AR(1))
toolkit.econometrics.get_gls(period="weekly")
```

Which returns:

|           |   Coefficient |   Std. Error |   t-Statistic |   P-Value |
|:----------|--------------:|-------------:|--------------:|----------:|
| Intercept |        0.0012 |       0.0017 |        0.7282 |    0.4671 |
| MSFT      |        0.6312 |       0.0576 |       10.9557 |    0      |

---

## get_binary_choice_regression
Fit a binary choice regression of whether `dependent_ticker`'s return is positive on `independent_tickers`, the Logistic Regression (method="logit") or the Probit Regression (method="probit").

The dependent variable is turned into a binary outcome (1 when the return is positive, 0 otherwise) and the model estimates the probability of that outcome through a link function that maps any value onto the 0 to 1 range: the logistic (sigmoid) function for the Logit model and the standard normal cumulative distribution function for the Probit model.

The formula for method="logit" is as follows:

$$
y_{t} = 1 \;\text{if the dependent ticker's} \;\text{column} \;(\text{Return by default}) \;\text{is above}\; 0,\;\; \text{else 0}
$$

$$
P(y_{t} = 1 \mid x_{t}) = \frac{1}{1 + \exp(- x_{t}' \beta)},\;\; \text{with } x_{t} \text{ the independent tickers' column plus a constant}
$$

$$
\hat{\beta} = \operatorname*{arg\,max} \sum\left[y_{t} \cdot \ln(p_{t}) + (1 - y_{t}) \cdot \ln(1 - p_{t})\right],\;\; \text{solved by Newton-Raphson (statsmodels Logit)}
$$

$$
\text{Pseudo}\; R^{2} = 1 - \frac{\ln L(\hat{\beta})}{\ln L_{0}} \;(\text{McFadden}),\;\; \text{with } L_{0} \text{ the likelihood of a constant-only model}
$$

The formula for method="probit" is as follows:

$$
y_{t} = 1 \;\text{if the dependent ticker's} \;\text{column} \;(\text{Return by default}) \;\text{is above}\; 0,\;\; \text{else 0}
$$

$$
P(y_{t} = 1 \mid x_{t}) = \Phi(x_{t}' \beta),\;\; \text{with } x_{t} \text{ the independent tickers' column plus a constant}
$$

$$
\hat{\beta} = \operatorname*{arg\,max} \sum\left[y_{t} \cdot \ln(p_{t}) + (1 - y_{t}) \cdot \ln(1 - p_{t})\right],\;\; \text{solved by Newton-Raphson (statsmodels Probit)}
$$

$$
\text{Pseudo}\; R^{2} = 1 - \frac{\ln L(\hat{\beta})}{\ln L_{0}} \;(\text{McFadden}),\;\; \text{with } L_{0} \text{ the likelihood of a constant-only model}
$$

Where `Φ` is the standard normal CDF. Both models are fitted by Maximum Likelihood. Logit coefficients are log-odds: a one-unit increase in an independent ticker changes the log-odds of a positive return by that coefficient, holding the others fixed, so a positive coefficient means a higher probability of a positive return. A positive Probit coefficient also means a higher probability of a positive return, but its size is not a log-odds ratio. In practice Probit and Logit give very similar fitted probabilities; Probit is the convention in parts of the econometrics literature and underlies two-step estimators such as the Heckman selection correction. Both answer "does this asset tend to be up when the others move this way" rather than "by how much", which is what `get_ols` estimates.

The coefficients are per unit of the independent ticker's return, and a unit is a return of 100%: a Logit coefficient of 90 on the benchmark means the log-odds of an up period rise by about 0.9 for every 1% the benchmark moves. With returns of the same period as regressors the model describes co-movement and predicts nothing; a forecast needs regressors known in advance, such as the returns of the previous period.

For more information about the methods, see the following papers:

- Berkson, J. (1944). "Application of the Logistic Function to Bio-Assay." Journal of the American Statistical Association, 39(227), 357-365.
- Bliss, C.I. (1934). "The Method of Probits." Science, 79(2037), 38-39.

**Also known as:** logistic regression, logit model, logit regression, probit regression, probit model, binary response model.

**Args:**

- <u>dependent_ticker (str &#124; None, optional):</u> The dependent asset (whose
up/down direction is predicted). Defaults to None, meaning the Toolkit
instance's first ticker.
- <u>independent_tickers (str &#124; list[str] &#124; None, optional):</u> The independent
(predictor) asset(s). Defaults to None, meaning every other ticker in
the Toolkit instance besides `dependent_ticker`.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" in the
default independent ticker(s) (has no effect when independent_tickers is given
explicitly). Defaults to False.
- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to derive returns from. Defaults to
"Return".
- <u>add_constant (bool, optional):</u> Whether to include an intercept. Defaults to True.
- <u>method (str, optional):</u> The link function, "logit" for the Logistic Regression or
"probit" for the Probit Regression. Defaults to "logit".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: A coefficient table (Coefficient, Std. Error, z-Statistic, P-Value),
indexed by regressor name.

**Notes:**

- The dependent variable is derived as `1` if the dependent ticker's return in the given
period is positive, `0` otherwise -- this method predicts the *direction*, not the
magnitude, of the dependent asset's return.
- Requires statsmodels (`pip install financetoolkit[econometrics]`).

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

# AAPL (the first ticker) is dependent; the Benchmark is independent
toolkit.econometrics.get_binary_choice_regression(include_benchmark=True)
```

Which returns:

|           |   Coefficient |   Std. Error |   z-Statistic |   P-Value |
|:----------|--------------:|-------------:|--------------:|----------:|
| Intercept |       -0.0275 |       0.15   |       -0.1836 |    0.8543 |
| Benchmark |      164.846  |      25.4127 |        6.4868 |    0      |

---

## get_quantile_regression
Fit a Quantile Regression of `dependent_ticker` on `independent_tickers` at quantile `tau`.

Where OLS estimates how the average (conditional mean) of the dependent ticker depends on the independent tickers, Quantile Regression estimates how a chosen quantile of it does. It minimises an asymmetric ("pinball") loss that is smallest at the conditional `tau`-quantile.

The formula is as follows:

$$
\hat{\beta}(\tau) = \operatorname*{arg\,min} \sum(\tau \cdot \max(u_{t},\; 0) + (1 - \tau) \cdot \max(- u_{t},\; 0)),\;\; \text{with}\;\; u_{t} = y_{t} - x_{t}' \beta\;\;\text{and}\;\; \tau = \text{tau} \;(0.5 \;\text{by default})
$$

- y is the dependent ticker's `column` (Return by default) and X the independent tickers' `column` plus a constant (add_constant=True)

- $$\text{SE} (\hat{\beta})$$: statsmodels' kernel sandwich estimator (Epanechnikov kernel, Hall-Sheather bandwidth), or, when `n_bootstrap` > 0, the standard deviation (ddof=1) of $$\hat{\beta}$$ over `n_bootstrap` resampled-pairs fits

With `tau = 0.5` this is the median regression, which is far less sensitive to outliers than OLS. Fitting at several quantiles (e.g. 0.05, 0.5 and 0.95) shows how the whole distribution of returns responds to the independent tickers, for example whether an asset's sensitivity to the market is larger in sell-offs (low quantiles) than in normal periods, which is directly relevant for downside risk.

Comparing the coefficients at a low `tau` with those at `tau=0.5`, or with the betas from `get_ols`, shows whether the sensitivity to the market rises in sell-offs. The table has no p-values: a coefficient more than about two standard errors from zero is significant at the 5% level.

For more information about the method, see the following paper:

- Koenker, R., & Bassett, G. (1978). "Regression Quantiles." Econometrica, 46(1), 33-50.

**Also known as:** QR.

**Args:**

- <u>dependent_ticker (str &#124; None, optional):</u> The dependent (predicted) asset.
Defaults to None, meaning the Toolkit instance's first ticker.
- <u>independent_tickers (str &#124; list[str] &#124; None, optional):</u> The independent
(predictor) asset(s). Defaults to None, meaning every other ticker in
the Toolkit instance besides `dependent_ticker`.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" in the
default independent ticker(s) (has no effect when independent_tickers is given
explicitly). Defaults to False.
- <u>tau (float, optional):</u> The quantile to fit, in (0, 1). Defaults to 0.5 (the median).
- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to regress on. Defaults to "Return".
- <u>add_constant (bool, optional):</u> Whether to include an intercept. Defaults to True.
- <u>n_bootstrap (int, optional):</u> The number of bootstrap resamples used for coefficient
standard errors, overriding `statsmodels`' default analytic (kernel density-based)
standard errors. Defaults to 0 (use the analytic standard errors).
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: A coefficient table (Coefficient, Std. Error), indexed by regressor name.

**Notes:**

- Requires statsmodels (`pip install financetoolkit[econometrics]`).

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["BAC", "KRE"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

# BAC (the first ticker) is dependent; KRE and the Benchmark are independent.
# tau=0.05 describes how the worst 5% of days respond.
toolkit.econometrics.get_quantile_regression(include_benchmark=True, tau=0.05)
```

Which returns:

|           |   Coefficient |   Std. Error |
|:----------|--------------:|-------------:|
| Intercept |       -0.0146 |       0.0006 |
| KRE       |        0.5271 |       0.0484 |
| Benchmark |        0.3965 |       0.1133 |

---

## get_fama_macbeth_regression
Fit a Fama-MacBeth (1973) two-pass cross-sectional regression: `asset_tickers` is treated as the cross-section of test assets, `factor_tickers` as the risk factor(s) whose risk premia are estimated -- the standard procedure for testing whether a proposed risk factor is actually priced.

The method runs in two passes:

1. Time-series pass (per asset): regress each asset's returns on the factor(s) to estimate its factor loadings (betas).
2. Cross-sectional pass (per period): regress that period's returns of all assets on those betas, which gives one estimate of each factor's risk premium per period.

The formula is as follows:

$$
\text{First pass:}\;\; R_{i,t} = \alpha_{i} + \beta_{i}' \cdot F_{t} + e_{i,t},\;\; \text{for each asset } i \text{, over the full sample}
$$

$$
\text{Second pass:}\;\; R_{i,t} = \gamma_{0,t} + \gamma_{t}' \cdot \beta_{i} + u_{i,t},\;\; \text{for each period } t \text{ (gamma\_0,} t \text{ only with add\_constant=True)}
$$

$$
\text{Risk premium:}\;\; \hat{\gamma} = \text{mean}_{t}(\gamma_{t})
$$

$$
\text{Standard error:}\;\; \operatorname{SE}(\hat{\gamma}) = \frac{\text{std}_{t}(\gamma_{t})}{\sqrt{T}},\;\; \text{with ddof=1}
$$

$$
t = \frac{\hat{\gamma}}{\operatorname{SE}(\hat{\gamma})},\;\; \text{with p-values from a Student-t distribution with}\; T - 1 \;\text{degrees of freedom}
$$

- R are the asset tickers' `column` (Return by default) and F the factor tickers' `column` (the Benchmark by default)

The risk premium is the average of the per-period estimates, and its standard error comes from how much those estimates vary over time. That is the method's key contribution: it accounts for correlation between the assets' residuals without having to model it. A significant positive premium means investors are compensated for exposure to the factor. This uses a single full-sample set of betas (the textbook variant), not the original rolling-window betas.

The first-pass betas are estimates, which makes the second-pass standard errors too small; the Shanken (1992) correction, not applied here, widens them. The returns are not in excess of the risk-free rate, so the intercept is the return of a zero-beta asset, which should be close to the risk-free rate if the factors price the assets.

For more information about the method, see the following papers:

- Fama, E.F. & MacBeth, J.D. (1973). "Risk, Return, and Equilibrium: Empirical Tests." Journal of Political Economy, 81(3), 607-636.
- Shanken, J. (1992). "On the Estimation of Beta-Pricing Models." Review of Financial Studies, 5(1), 1-33.
- Cochrane, J.H. (2005). "Asset Pricing." Princeton University Press, Chapter 12.

**Also known as:** two-pass regression, Fama-MacBeth procedure.

**Args:**

- <u>factor_tickers (str &#124; list[str] &#124; None, optional):</u> The ticker(s) whose
returns are used as the risk factor(s) (e.g. "Benchmark" for a
single-factor/CAPM-style test). Defaults to None, meaning `["Benchmark"]`.
- <u>asset_tickers (str &#124; list[str] &#124; None, optional):</u> The ticker(s) forming the
cross-section of test assets. Defaults to None, meaning every Toolkit
ticker (including "Benchmark") not already used as a factor.
- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to regress on. Defaults to "Return".
- <u>add_constant (bool, optional):</u> Whether to include an intercept in the
second-pass cross-sectional regression. Defaults to True.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: A coefficient table (Risk Premium, Std. Error, t-Statistic,
P-Value), indexed by factor name (plus "Intercept" if present).

**Notes:**

- The cross-sectional second pass needs strictly more assets than factors
(plus an intercept, if `add_constant=True`) to be identified -- with only a
couple of Toolkit tickers loaded, either pass `add_constant=False` or (better)
construct the Toolkit with many tickers, since Fama-MacBeth is fundamentally a
many-asset cross-sectional technique (dozens of assets is typical in practice),
not a limitation of this method's implementation.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "JPM", "XOM", "JNJ", "PG", "KO", "WMT", "CAT", "NEE"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

# The Benchmark (the default factor) is the single risk factor and the ten
# stocks are the test assets.
toolkit.econometrics.get_fama_macbeth_regression(period="monthly")
```

Which returns:

|           |   Risk Premium |   Std. Error |   t-Statistic |   P-Value |
|:----------|---------------:|-------------:|--------------:|----------:|
| Intercept |         0.0066 |       0.0058 |        1.1505 |    0.2547 |
| Benchmark |         0.0101 |       0.008  |        1.2668 |    0.2103 |

---

## get_fixed_effects
Fit a Fixed Effects ("within") estimator explaining a panel of `dependent_tickers` (the entities) by a regressor `x`, controlling for entity-specific (and/or time-specific) fixed effects.

**Also known as:** within estimator, FE, least squares dummy variable (LSDV) estimator.

Unlike this module's other regression methods (`get_ols`, `get_wls`, ...), which each compare a handful of individual ticker return series on equal footing, this treats `dependent_tickers` as a genuine panel of entities -- e.g. every stock in the `Toolkit` instance -- observed over time. The regressor `x` is built in exactly one of two ways (provide exactly one of the two arguments below):

- `independent_tickers`: a COMMON factor (or factors) applied identically to every entity at each date (e.g. a market benchmark, mirroring a Fama-French-style factor regression).
- `independent_column`: a PER-ENTITY regressor -- each entity's own value of a *different* historical data column (e.g. does `"Volume"` explain `"Return"`, across the panel).

Fixed Effects removes any purely entity-specific, time-invariant characteristic (e.g. a stock's typical risk premium) before estimating the regressor's coefficient(s), by demeaning every variable by its entity's mean. See `panel_data_model.get_fixed_effects` for the full formula and references.

The formula is as follows:

$$
\tilde{y}_{it} = y_{it} - \text{mean}_{t}(y_{it})\;\;\text{and}\;\; \tilde{x}_{it} = x_{it} - \text{mean}_{t}(x_{it}) (\text{entity\_effects} = \text{True},\; \text{the default});\;\; \text{time\_effects=True also removes each date's mean (two-way fixed effects)}
$$

$$
\hat{\beta}_{\text{FE}} = (\tilde{X}' \tilde{X})^{- 1} \tilde{X}' \tilde{y},\;\; \text{without a separate constant (linearmodels PanelOLS, unadjusted covariance)}
$$

$$
\text{Entity Effect:}\;\; \alpha_{i} = \text{mean}_{t}(y_{it} - x_{it}' \hat{\beta}_{\text{FE}});\;\; \text{Time Effect:}\;\; \lambda_{t} = \text{mean}_{i}(y_{it} - x_{it}' \hat{\beta}_{\text{FE}})
$$

- $$y_{it}$$ is each dependent ticker's `column` (Return by default)

**Args:**

- <u>independent_tickers (str &#124; list[str] &#124; None, optional):</u> The factor
ticker(s), whose `column` values are broadcast identically to every
entity at each date. Mutually exclusive with `independent_column`.
- <u>independent_column (str &#124; None, optional):</u> A different historical data
column, taken per-entity from each of `dependent_tickers`' own data, to
use as the regressor. Mutually exclusive with `independent_tickers`.
- <u>dependent_tickers (str &#124; list[str] &#124; None, optional):</u> The panel of
entity tickers to explain. Defaults to None, meaning every ticker in
the `Toolkit` instance (other than `independent_tickers`, if given).
- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly,
quarterly, or yearly). Defaults to "daily".
- <u>column (str, optional):</u> The dependent variable's historical data
column. Defaults to "Return".
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the
entities. Defaults to False.
- <u>entity_effects (bool, optional):</u> Whether to control for time-invariant
entity-specific characteristics. Defaults to True.
- <u>time_effects (bool, optional):</u> Whether to control for entity-invariant,
time-specific shocks. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the
results to. Defaults to None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: A coefficient table (Coefficient, Std. Error,
t-Statistic, P-Value) for the regressor(s), indexed by name, with the
recovered entity (and/or time) fixed-effect intercepts appended as
additional rows (only the Coefficient column is populated for those).

**Raises:**

ValueError: If both or neither of `independent_tickers`/
`independent_column` are given, or (see `panel_data_model.
get_fixed_effects`) if there are not enough observations for the
requested fixed effects, or the fixed effects absorb the regressor: the
common factor of `independent_tickers` is identical for every entity at
each date, so it cannot be combined with `time_effects=True`.

**Notes:**

- Requires linearmodels (`pip install financetoolkit[econometrics]`).

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["XOM", "CVX", "SHEL", "BP", "TTE"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_fixed_effects(independent_tickers="Benchmark")
```

Which returns:

|                     |   Coefficient |   Std. Error |   t-Statistic |   P-Value |
|:--------------------|--------------:|-------------:|--------------:|----------:|
| Benchmark           |        0.5795 |       0.0183 |       31.7272 |         0 |
| Entity Effect: BP   |        0.0004 |     nan      |      nan      |       nan |
| Entity Effect: CVX  |        0.0004 |     nan      |      nan      |       nan |
| Entity Effect: SHEL |        0.0005 |     nan      |      nan      |       nan |
| Entity Effect: TTE  |        0.0004 |     nan      |      nan      |       nan |
| Entity Effect: XOM  |        0.0008 |     nan      |      nan      |       nan |

---

## get_random_effects
Fit a Random Effects estimator explaining a panel of `dependent_tickers` (the entities) by a regressor `x`, via Swamy-Arora feasible Generalized Least Squares.

**Also known as:** RE, GLS panel estimator, Swamy-Arora estimator.

See `get_fixed_effects` for how `dependent_tickers`/`independent_tickers`/ `independent_column` are shaped into a panel, and `panel_data_model.get_random_effects` for the full estimator formula, references, and how it compares to Fixed Effects. Unlike Fixed Effects, Random Effects retains and estimates a single, population-average intercept rather than one intercept per entity -- more efficient than Fixed Effects if entity effects are indeed uncorrelated with the regressor(s) (see `get_hausman_test` to check that assumption).

The formula is as follows:

$$
\theta_{i} = 1 - \sqrt{\frac{\sigma_{\epsilon}^{2}}{\sigma_{\epsilon}^{2} + T_{i} \cdot \sigma_{u}^{2}}},\;\; \text{with the Swamy-Arora estimates of the idiosyncratic (} \sigma_{\epsilon}^{2} \text{) and entity (} \sigma_{u}^{2} \text{) variance components}
$$

$$
y^{*}_{it} = y_{it} - \theta_{i} \cdot \text{mean}_{t}(y_{it})\;\;\text{and}\;\; x^{*}_{it} = x_{it} - \theta_{i} \cdot \text{mean}_{t}(x_{it}),\;\; \text{the constant becoming}\; 1 - \theta_{i}
$$

$$
\hat{\beta}_{\text{RE}} = \text{OLS of} \;y^{*} \;\text{on} \;x^{*} \;(\text{linearmodels RandomEffects}),\;\; \text{with } y_{it} \text{ each dependent ticker's column (Return by default)}
$$

**Args:**

- <u>independent_tickers (str &#124; list[str] &#124; None, optional):</u> The factor
ticker(s), whose `column` values are broadcast identically to every
entity at each date. Mutually exclusive with `independent_column`.
Since this `Toolkit` instance's historical data is aligned onto a
common calendar across tickers, a broadcast factor's entity mean is
identical for every entity, leaving no between-entity variation to
identify Random Effects' between-regression step -- prefer
`independent_column` here unless `dependent_tickers` genuinely differ
in their date coverage (e.g. different listing histories).
- <u>independent_column (str &#124; None, optional):</u> A different historical data
column, taken per-entity from each of `dependent_tickers`' own data, to
use as the regressor. Mutually exclusive with `independent_tickers`.
- <u>dependent_tickers (str &#124; list[str] &#124; None, optional):</u> The panel of
entity tickers to explain. Defaults to None, meaning every ticker in
the `Toolkit` instance (other than `independent_tickers`, if given).
- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly,
quarterly, or yearly). Defaults to "daily".
- <u>column (str, optional):</u> The dependent variable's historical data
column. Defaults to "Return".
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the
entities. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the
results to. Defaults to None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: A coefficient table (Coefficient, Std. Error,
t-Statistic, P-Value), indexed by regressor name plus "Intercept".

**Raises:**

ValueError: If both or neither of `independent_tickers`/
`independent_column` are given, or (see `panel_data_model.
get_random_effects`) if there are not enough entities or observations
to estimate the model.

**Notes:**

- Requires linearmodels (`pip install financetoolkit[econometrics]`).

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["JPM", "BAC", "C", "WFC"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_random_effects(independent_tickers="Benchmark")
```

Which returns:

|           |   Coefficient |   Std. Error |   t-Statistic |   P-Value |
|:----------|--------------:|-------------:|--------------:|----------:|
| Intercept |        0.0003 |       0.0002 |        1.7192 |    0.0856 |
| Benchmark |        0.9788 |       0.0183 |       53.4931 |    0      |

---

## get_hausman_test
Calculate the Hausman specification test comparing a Fixed Effects and a Random Effects fit of `dependent_tickers` (the panel of entities) on a regressor `x`.

**Also known as:** Hausman specification test, fixed versus random effects test.

Random Effects is more efficient than Fixed Effects but relies on entity effects being uncorrelated with the regressor(s) -- if that assumption is violated, Random Effects is inconsistent while Fixed Effects remains consistent regardless. See `panel_data_model.get_hausman_test` for the full formula and references, and `get_fixed_effects`/`get_random_effects` for how the two models being compared are estimated (including how `independent_tickers`/`independent_column` shape the panel, and why `independent_column` is generally the more reliable choice here).

The formula is as follows:

$$
H = (\hat{\beta}_{\text{FE}} - \hat{\beta}_{\text{RE}})' \cdot \left[\operatorname{Var}(\hat{\beta}_{\text{FE}}) - \operatorname{Var}(\hat{\beta}_{\text{RE}})\right]^{- 1} \cdot (\hat{\beta}_{\text{FE}} - \hat{\beta}_{\text{RE}}),\;\; \text{over the } k \text{ slope coefficients the two models share (a pseudo-inverse when the difference is singular)}
$$

$$
\text{With variance} = \text{"efficient"} \;\text{Var}(\hat{\beta}_{\text{FE}}) \;\text{is scaled by}\; s_{\text{RE}}^{2} / s_{\text{FE}}^{2},\;\; \text{with variance} = \frac{\text{"consistent"} \;\text{Var}(\hat{\beta}_{\text{RE}}) \;\text{by}\; s_{\text{FE}}^{2}}{s_{\text{RE}}^{2}},\;\; \text{so both rest on one disturbance variance (Stata's sigmamore and sigmaless)}
$$

- H is chi-squared with k degrees of freedom; Random Effects is rejected when the p-value is below 0.05

- A negative H means that $$\operatorname{Var} (\hat{\beta}_{\text{FE}}) - \operatorname{Var} (\hat{\beta}_{\text{RE}})$$ is not positive definite in the sample: the P-Value and the preference are then NaN, and the "efficient" or "consistent" variance gives a statistic

- $$\hat{\beta}_{\text{FE}}$$ comes from `get_fixed_effects` with entity effects only and $$\hat{\beta}_{\text{RE}}$$ from `get_random_effects`

**Args:**

- <u>independent_tickers (str &#124; list[str] &#124; None, optional):</u> The factor
ticker(s), whose `column` values are broadcast identically to every
entity at each date. Mutually exclusive with `independent_column`.
- <u>independent_column (str &#124; None, optional):</u> A different historical data
column, taken per-entity from each of `dependent_tickers`' own data, to
use as the regressor. Mutually exclusive with `independent_tickers`.
- <u>dependent_tickers (str &#124; list[str] &#124; None, optional):</u> The panel of
entity tickers to explain. Defaults to None, meaning every ticker in
the `Toolkit` instance (other than `independent_tickers`, if given).
- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly,
quarterly, or yearly). Defaults to "daily".
- <u>column (str, optional):</u> The dependent variable's historical data
column. Defaults to "Return".
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the
entities. Defaults to False.
- <u>variance (str, optional):</u> The variances compared: "separate" (each model's own),
"efficient" (both based on the residual variance of Random Effects) or "consistent"
(both based on the residual variance of Fixed Effects). Defaults to "separate".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the
results to. Defaults to None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series: The Hausman statistic, its degrees of freedom, its p-value,
and whether Fixed Effects is preferred over Random Effects at the 5%
level (NaN with the P-Value when the statistic is negative).

**Raises:**

ValueError: If both or neither of `independent_tickers`/
`independent_column` are given, or (see `panel_data_model.
get_hausman_test`) if there are not enough observations or entities to
fit either model, or the two estimators share no common regressors to
compare.

**Notes:**

- Requires linearmodels (`pip install financetoolkit[econometrics]`).

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT", "AMZN"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_hausman_test(independent_column="Volume", period="weekly")
```

Which returns:

|                           |   Value |
|:--------------------------|--------:|
| Hausman Statistic         |  0.5866 |
| Degrees of Freedom        |  1      |
| P-Value                   |  0.4438 |
| Prefer Fixed Effects (5%) |  0      |

---

## get_level_significance
Calculate how unusual the latest value of every series is: its percentile in the series' own history and the last dates the series was at least as high ("the highest since") and at least as low ("the lowest since"), next to its change since the first observation and the highest and lowest values of the range with their dates and the change from them.

Where `get_move_significance` (Risk) measures how unusual a move is, this measures how unusual a level is, which is the question for rates and macroeconomic series: a 10-year yield of 5.13% is "the highest since May 2002" when no month since then was as high, and an unemployment rate can be the lowest in decades without any single large move. Through the Toolkit it measures the prices of the tickers ("the highest close since"); with `Econometrics(data=...)` any series, such as the interest rates, inflation or unemployment of `Economics` and the yield curves of `FixedIncome`.

The formula is as follows:

$$
\text{Percentile} = \frac{\operatorname{Count}(x(s) < x(T)) + 0.5 \cdot \operatorname{Count}(x(s) = x(T))}{\operatorname{Count}(s)},\;\; \text{over}\; s < T
$$

$$
\text{Rank} = 1 + \operatorname{Count}(x(s) > x(T)),\;\; \text{over}\; s < \text{T:} 1 \;\text{for the highest of the history}
$$

$$
\text{Highest Since} = \text{the last date}\; s < T \;\text{with} \;x(s) \geq x(T)
$$

$$
\text{Lowest Since} = \text{the last date}\; s < T \;\text{with} \;x(s) \leq x(T)
$$

$$
\text{Change Since Start} = \frac{x(T) - x(0)}{\left|x(0)\right|}
$$

$$
\text{Change From Highest} = \frac{x(T) - \max(x)}{\left|\max(x)\right|}
$$

$$
\text{Change From Lowest} = \frac{x(T) - \min(x)}{\left|\min(x)\right|}
$$

$$
\text{Multiple Since Start} = \frac{x(T)}{x(0)}
$$

$$
\text{Annualised Change} = \left(\frac{x(T)}{x(0)}\right)^{\frac{1}{\text{years}}} - 1,\;\; \text{years between the two dates}
$$

$$
\text{Largest Drawdown} = \min \;\text{over}\; t \;\text{of} \;\frac{x(t) - \max(x(s),\; s \leq t)}{\left|\max(x(s),\; s \leq t)\right|}
$$

$$
\text{Recovery Date} = \text{the first date after the trough with}\; x \geq \text{the peak before it}
$$

$$
\text{First Above Level} = \text{the first date}\; s \;\text{with} \;x(s) > \text{level}
$$

$$
\text{Above Level Since} = \text{the first date of the run above the level the latest value is in}
$$

$$
\text{Last Above Level} = \text{the last date}\; s < T \;\text{with} \;x(s) > \text{level}
$$

$$
\text{Last At Or Below Level} = \text{the last date}\; s < T \;\text{with} \;x(s) \leq \text{level}
$$

$$
\text{Observations Above Level} = \operatorname{Count}(x(s) > \text{level}),\;\; \text{over}\; s \leq T
$$

$$
\text{Observations At Or Below Level} = \operatorname{Count}(x(s) \leq \text{level}),\;\; \text{over}\; s \leq T
$$

Where x(T) is the latest value of a series, x(0) its first observation and s runs over its earlier observations. An earlier value equal to the latest one counts as half (the percentile rank), so a policy rate that has not changed for years sits in the middle of its own ties. Highest Since is NaN when no earlier value was as high, which makes the latest value the highest of the history; Lowest Since likewise. The Change Since Start is the change between the first and the latest observation in the range, so the start and end date choose the two dates to compare (housing starts from January 2021 to their latest month with period="monthly"); it is relative to the absolute first value, so a rise from a negative value is positive, and NaN when the first value is zero. The Highest and Lowest are the peak and trough of the range, the latest value included, with the first dates they were reached, so the start date works as the anchor of an event window: the rise from the start to the peak, the date of the peak and the fall from it to the latest value. The changes from them are relative to their absolute values, and NaN when they are zero. With `Econometrics(data=..., changes="difference")` every change, the Largest Drawdown included, is a difference in the unit of the series instead (percentage points for a rate: a 10-year yield from 5.29% to 4.94% is -0.0035), and the Multiple Since Start and Annualised Change are NaN.

**Also known as:** highest since, lowest since, record high, multi-year high, level percentile, historical percentile, how unusual is the latest value, change since, change between two dates, cumulative change, event window, peak, trough, drawdown from the peak, change from the high, change from the low, multiple, compound annual growth rate (CAGR), annualised change, peak to trough, time to recover the peak, change in percentage points, how often at or below a level, the last time above a level.

**Args:**

- <u>period (str &#124; None, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or
yearly); the weekly to yearly periods take the last value of each period. Defaults to
None, which is "daily": the series at the dates they are observed, so a monthly
series is compared month by month.
- <u>column (str, optional):</u> The historical data column to measure. Defaults to "Close", the
traded close of the tickers and the series themselves with data=.
- <u>spread_over (str &#124; None, optional):</u> The name of a series to subtract from every
other series, so the spreads over it are measured instead (named "<series> -
<spread_over>"), e.g. producer price inflation over consumer price inflation.
The spread exists on the dates both series have, so with period="daily" a weekly
series minus a daily one is measured on the weekly dates. Defaults to None, which
measures the series themselves.
- <u>ratio (bool, optional):</u> Whether to divide every other series by the spread_over
series instead of subtracting it (named "<series> / <spread_over>"), e.g.
exports over GDP or one country's yield over another's. Defaults to False.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the assets.
Defaults to False.
- <u>level (float &#124; None, optional):</u> A level to compare every series with, such as an
earlier peak, which adds the Level, the First Above Level (the first date the
series exceeded it), Above Level Since (the date it has been above it since
without a break, empty when the latest value is not above it), the Last Above
Level and Last At Or Below Level (the last date before the latest observation
on either side of it, empty when there is none) and the Observations Above
Level and Observations At Or Below Level (how many observations of the range,
the latest included, are on either side of it: "6 weeks at or below 203,000
between 1970 and 2020"). Defaults to None, which leaves them out.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the rounding of the class (4 unless set otherwise).
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per series the Start Date, Start Value and number of Observations of its
history, the Latest Date and Latest Value, the Change Since Start (decimal), the
Multiple Since Start and Annualised Change (decimal, the compound annual rate, NaN
unless both values are positive), the Percentile (decimal), the Rank (1 for the
highest of the history: "the 3rd highest since" the Start Date), the Highest Since and
Lowest Since dates, the Highest and Lowest with their Highest Date and Lowest Date
and the Change From Highest and Change From Lowest (decimals), and the Largest
Drawdown (decimal) with its Drawdown Peak Date (the last date at the peak before the
trough), Drawdown Trough Date and Recovery Date (NaN while it has not recovered),
and with a level the Level, First Above
Level, Above Level Since, Last Above Level, Last At Or Below Level, Observations
Above Level and Observations At Or Below Level. The dates are text: the dates of the observations, e.g.
2002-05-31 for a monthly series, or the periods, e.g. 2002-05 with period="monthly".

**Notes:**

- The answer depends on the history it is measured against: the history starts at the start
date of the data, so "the highest since" can at most reach back to that date, and a
later start date gives a higher percentile for a value near the top. Choose a start date
far enough back, and read the Start Date column to see where each history begins.
- Each series uses its own history, so a series that starts later has a shorter one.
- The latest value is the last observation up to the end date, which can be older than the
end date for a series published with a lag; Latest Date says which it is.

**As an example:**

```python
from financetoolkit import Economics, Econometrics

economics = Economics(start_date='2000-01-01', end_date='2026-10-31', rounding=None)

long_term_rates = economics.get_long_term_interest_rate(
    countries=['United States', 'Germany', 'Japan'], period='monthly'
)

econometrics = Econometrics(data=long_term_rates)

econometrics.get_level_significance(level=0.05).T
```

Which returns:

|                                | United States   | Germany    | Japan      |
|:-------------------------------|:----------------|:-----------|:-----------|
| Start Date                     | 2000-01-31      | 2000-01-31 | 2000-01-31 |
| Start Value                    | 0.0666          | 0.0554     | 0.0169     |
| Observations                   | 322             | 322        | 322        |
| Latest Date                    | 2026-10-31      | 2026-10-31 | 2026-10-31 |
| Latest Value                   | 0.0513          | 0.0342     | 0.0276     |
| Change Since Start             | -0.2297         | -0.3834    | 0.6292     |
| Multiple Since Start           | 0.7703          | 0.6166     | 1.6292     |
| Annualised Change              | -0.0097         | -0.0179    | 0.0184     |
| Percentile                     | 0.9377          | 0.6854     | 0.9907     |
| Rank                           | 21              | 102        | 4          |
| Highest Since                  | 2002-05-31      | 2026-09-30 | 2026-09-30 |
| Lowest Since                   | 2026-09-30      | 2026-08-31 | 2026-06-30 |
| Highest                        | 0.0666          | 0.0554     | 0.0305     |
| Highest Date                   | 2000-01-31      | 2000-01-31 | 2026-09-30 |
| Change From Highest            | -0.2297         | -0.3834    | -0.0967    |
| Lowest                         | 0.0062          | -0.0065    | -0.0028    |
| Lowest Date                    | 2020-07-31      | 2019-08-31 | 2019-08-31 |
| Change From Lowest             | 7.2742          | 6.2626     | 10.8393    |
| Largest Drawdown               | -0.9069         | -1.1172    | -1.1431    |
| Drawdown Peak Date             | 2000-01-31      | 2000-01-31 | 2006-04-30 |
| Drawdown Trough Date           | 2020-07-31      | 2019-08-31 | 2019-08-31 |
| Recovery Date                  | nan             | nan        | 2025-12-31 |
| Level                          | 0.05            | 0.05       | 0.05       |
| First Above Level              | 2000-01-31      | 2000-01-31 | nan        |
| Above Level Since              | 2026-10-31      | nan        | nan        |
| Last Above Level               | 2007-06-30      | 2002-06-30 | nan        |
| Last At Or Below Level         | 2026-09-30      | 2026-09-30 | 2026-09-30 |
| Observations Above Level       | 28              | 17         | 0          |
| Observations At Or Below Level | 294             | 305        | 322        |

---

## get_move_significance
Calculate how unusual each move of every series is: the change in units of its trailing volatility and of its trailing Value at Risk, its percentile among the earlier moves and the date of the last move at least as large in the same direction ("the largest one-day rise since").

This is `get_move_significance` (Risk) for any series rather than the returns of the Toolkit's tickers: with `Econometrics(data=..., changes="difference")` a yield, rate or spread moves in points, so a rise of the 2-year Treasury yield from 4.56% to 4.73% is a move of 0.0017, measured against the earlier daily moves of the same yield. Where `get_level_significance` asks how unusual a level is, this asks how unusual a change is.

The formula is as follows:

$$
\text{Volatility Multiple}(t) = \frac{\operatorname{Change}(t)}{\sigma(\operatorname{Change}(t - \text{window}),\; \ldots,\; \operatorname{Change}(t - 1))}
$$

$$
\text{VaR Multiple}(t) = \frac{\operatorname{Change}(t)}{\left|\operatorname{Quantile}(\operatorname{Change}(t - \text{window}),\; \ldots,\; \operatorname{Change}(t - 1) ; \alpha)\right|}
$$

$$
\operatorname{Percentile}(t) = \frac{\operatorname{Count}(\left|\operatorname{Change}(s)\right| < \left|\operatorname{Change}(t)\right|) + 0.5 \cdot \operatorname{Count}(\left|\operatorname{Change}(s)\right| = \left|\operatorname{Change}(t)\right|)}{\operatorname{Count}(s)},\;\; \text{over}\; s < t
$$

$$
\text{Largest Since}(t) = \max(s < t \text{:} \;\text{Change}(s) \leq \operatorname{Change}(t)) \;\text{if Change}(t) < 0
$$

$$
\text{Largest Since}(t) = \max(s < t \text{:} \;\text{Change}(s) \geq \operatorname{Change}(t)) \;\text{if Change}(t) > 0
$$

The Change is the series' change as `changes` defines it: a percentage change by default, the difference with `changes="difference"` and the series itself with `changes="none"`. The volatility $$\sigma$$ uses ddof=1 and the quantile is the historic Value at Risk, interpolated linearly. Each measure only uses the changes before the period itself (no look-ahead), and Largest Since compares falls with falls and rises with rises, as a headline does. An earlier change of the same size counts as half in the percentile (the mid-rank, as in `get_level_significance`), so a rate that is unchanged on most days puts an unchanged day in the middle of its ties. The VaR Multiple is NaN when the trailing alpha quantile is zero or positive, as there is no loss to scale the change by.

**Also known as:** sigma move, largest move since, biggest daily rise since, standardized change, yield move significance.

**Args:**

- <u>period (str &#124; None, optional):</u> The data frequency (daily, weekly, monthly, quarterly
or yearly). Defaults to None, which is daily.
- <u>window (int &#124; None, optional):</u> The number of earlier changes the volatility is
measured over, which the percentile also needs at least. Defaults to None, which
uses a year of observations with a minimum of 20 (252 daily, 52 weekly and 20
monthly, quarterly or yearly changes). With `Econometrics(data=...)` and the
"daily" period, a year is counted in each series' own observations, from the
median spacing of its dates: 20 changes for a monthly or quarterly series and
52 for a weekly one.
- <u>alpha (float, optional):</u> The tail probability of the trailing historic Value at Risk
the VaR Multiple divides by (0.05 for the 95% VaR). Defaults to 0.05.
- <u>include_benchmark (bool, optional):</u> Whether to include the benchmark of a Toolkit.
Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the rounding of the class (4 unless set otherwise).
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Return (the change), Volatility Multiple, VaR Multiple, Percentile and
Largest Since (the date as text, NaN when there is none) per series, with time as the
index and the measures and series as the column levels.

**Notes:**

- The history a move is compared with starts at the start of the data: the volatility,
the VaR and the percentile are NaN until `window` changes are available, and Largest
Since is NaN when no earlier move was as large, which makes the move the largest since
the start. Choose an early start date for a long history.
- Each series uses its own history and only the dates it has a value for, so a market
holiday is not a move of zero.

**As an example:**

```python
from financetoolkit import Econometrics, FixedIncome

fixedincome = FixedIncome(start_date='2025-01-01', end_date='2026-11-10', rounding=None)

treasury_rates = fixedincome.get_treasury_rates(maturities=['2Y', '10Y'])

econometrics = Econometrics(data=treasury_rates, changes='difference')

econometrics.get_move_significance().loc['2026-11-10'].unstack(level=0)
```

Which returns:

|         |   Return |   Volatility Multiple |   VaR Multiple |   Percentile | Largest Since   |
|:--------|---------:|----------------------:|---------------:|-------------:|:----------------|
| 2 Year  |   0.0017 |                3.5345 |         2.4286 |       0.9935 | 2025-04-09      |
| 10 Year |   0.001  |                2.2808 |         1.6667 |       0.9633 | 2026-09-23      |

---

## get_window_change_by_year
Calculate the change of every series over the same months of every year, such as February to October, with the rank of every year's change and the last earlier year with a change at least as large ("the largest since").

Where `get_level_significance` measures one window, from the start date to the latest value, this compares the same window across years: "US consumer prices rose 3.3% from February to October, the most since 2022" is the Change, Rank and Largest Since of the latest year. Through the Toolkit it measures the prices of the tickers (a seasonal pattern, such as the return from May to October); with `Econometrics(data=...)` any series, such as the consumer price indices of `Economics`.

The formula is as follows:

$$
\text{Change} \;(y) = \frac{x(\text{to\_month},\; y) - x(\text{from\_month},\; y)}{\left|x(\text{from\_month},\; y)\right|}
$$

$$
\text{Rank} \;(y) = \text{the position of Change} \;(y) \;\text{among the changes of every year},\;\; \text{1 for the largest}
$$

$$
\text{Largest Since} \;(y) = \text{the last year}\; s < y \;\text{with Change} \;(s) \geq \text{Change} \;(y)
$$

Where x(m, y) is the value of month m in year y, the last value of the month for a daily series. A window that ends in an earlier month than it starts (November to February) runs into the next year and is labelled by the year it ends; the same month for both gives the change over twelve months. A year without the value of either month has no change, so the current year is empty until its last month is published. Largest Since is empty (<NA>) when no earlier year had a change as large. With `Econometrics(data=..., changes="difference")` the Change is x(to_month, y) - x(from_month, y), in percentage points for a rate.

**Also known as:** same period each year, seasonal change, year-to-date comparison, change from February to October, largest since, fastest since, seasonality.

**Args:**

- <u>from_month (int, optional):</u> The month the window starts, 1 (January) to 12
(December). Defaults to 1.
- <u>to_month (int, optional):</u> The month the window ends, 1 to 12. Defaults to 12,
which with from_month=1 is the change from January to December.
- <u>column (str, optional):</u> The historical data column to measure. Defaults to
"Close", the traded close of the tickers and the series themselves with data=.
- <u>spread_over (str &#124; None, optional):</u> The name of a series to subtract from every
other series, so the spreads over it are measured instead. Defaults to None.
- <u>ratio (bool, optional):</u> Whether to divide every other series by the spread_over
series instead of subtracting it (named "<series> / <spread_over>"). Defaults
to False.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the
assets. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the rounding of the class (4 unless set
otherwise).
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per year (rows) and series the Start Value, End Value, Change
(decimal), Rank and Largest Since (columns, a level per series); the Rank and
Largest Since are whole numbers, <NA> when there is none.

**Notes:**

- The ranks and "largest since" depend on the history: start the data early enough,
as a year before the start date is not compared.
- The change uses the levels, so the series should be an index or a price, not a
rate: the change in an inflation rate is a relative change of a rate.

**As an example:**

```python
from financetoolkit import Economics, Econometrics

economics = Economics(start_date='2019-01-01', end_date='2026-10-31')

consumer_price_index = economics.get_consumer_price_index(
    countries=['United States', 'Euro Area']
)

econometrics = Econometrics(data=consumer_price_index)

econometrics.get_window_change_by_year(from_month=2, to_month=10)['United States']
```

Which returns:

|   Year |   Start Value |   End Value |   Change | Rank   | Largest Since   |
|-------:|--------------:|------------:|---------:|:-------|:----------------|
|   2019 |       115.923 |     118.019 |   0.0181 | 5      | <NA>            |
|   2020 |       118.629 |     119.414 |   0.0066 | 7      | 2019            |
|   2021 |       120.618 |     126.843 |   0.0516 | 1      | <NA>            |
|   2022 |       130.112 |     136.668 |   0.0504 | 2      | 2021            |
|   2023 |       137.965 |     141.098 |   0.0227 | 4      | 2022            |
|   2024 |       142.315 |     144.763 |   0.0172 | 6      | 2023            |
|   2025 |       146.331 |     nan     | nan      | <NA>   | <NA>            |
|   2026 |       149.863 |     154.782 |   0.0328 | 3      | 2022            |

---

## get_streaks
Calculate the streak every series is on: whether its latest value is positive, negative or zero, since when it has been without a break and how long that is, the run before it, and the longest earlier run of the same sign.

Where `get_level_significance` measures how unusual the latest level is, this measures how long a series has been on one side of zero, which is the question for inflation, growth and spreads: producer prices that fell year over year for 41 months in a row, a spread between two series that turned positive after three years, or a yield curve that has been inverted since a given month. With column="Return" it measures the changes instead: a price that rose for eight days in a row, or with `Econometrics(data=..., changes="difference")` an unemployment rate that rose for six months in a row. Through the Toolkit it measures the prices of the tickers; with `Econometrics(data=...)` any series, such as the economic calendar of `Economics` with as_series=True, its inflation rates or the yield curves of `FixedIncome`.

A run is a stretch of consecutive observations with the same sign (positive, negative or zero), counted in observations: months for a monthly series. The current run is the one the latest observation belongs to, the previous run the one just before it and the longest earlier run the longest run of the current sign before the current one (the most recent of them when several are as long).

**Also known as:** streak, run length, consecutive months, months in a row, how long has it been negative, first positive since.

**Args:**

- <u>period (str &#124; None, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or
yearly); the weekly to yearly periods take the last value of each period. Defaults to
None, which is "daily": the series at the dates they are observed, so a monthly
series is counted month by month.
- <u>column (str, optional):</u> The historical data column to measure. Defaults to "Close", the
traded close of the tickers and the series themselves with data=; "Return" measures
their changes.
- <u>spread_over (str &#124; None, optional):</u> The name of a series to subtract from every
other series, so the streaks of the spreads over it are measured instead (named
"<series> - <spread_over>"), e.g. producer price inflation over consumer price
inflation. The spread exists on the dates both series have, so with
period="daily" a weekly series minus a daily one is measured on the weekly dates.
Defaults to None, which measures the series themselves.
- <u>ratio (bool, optional):</u> Whether to divide every other series by the spread_over
series instead of subtracting it (named "<series> / <spread_over>"). Defaults
to False.
- <u>level (float &#124; None, optional):</u> The level the runs are measured against, so the
runs are above or below it ("27 years below 2%") with the signs "Above Level",
"Below Level" and "At Level". Defaults to None, which is zero: the sign of the
values.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the assets.
Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to.
Defaults to None, which uses the rounding of the class (4 unless set otherwise).
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per series the Start Date and number of Observations of its history,
the Latest Date and Latest Value, the Sign of the current run with its Run Start and
Run Length, the Previous Sign, Previous Run Start, Previous Run End and Previous Run
Length, and the Longest Earlier Run Start, End and Length. The dates are text (the
dates of the observations, or the periods, e.g. 2022-10 with period="monthly"), the
lengths are numbers of observations and a run that does not exist is NaN.

**Notes:**

- The runs are counted within the history, which starts at the start date of the data:
a run that began before it is counted from the first observation, which the Run Start
or Previous Run Start then equals.
- A value of exactly zero is a run of its own, so it ends a positive or negative run.
- Each series uses its own history, and the latest value is the last observation up to
the end date, which Latest Date shows.

**As an example:**

```python
from financetoolkit import Economics, Econometrics

economics = Economics(api_key="FINANCIAL_MODELING_PREP_KEY")

prices = economics.get_economic_calendar(
    start_date="2021-06-01",
    end_date="2026-11-09",
    countries="China",
    events="Producer Price Index YoY,Inflation Rate YoY",
    impact="All",
    as_series=True,
)

econometrics = Econometrics(
    data=prices["China"][["Producer Price Index YoY", "Inflation Rate YoY"]]
)

econometrics.get_streaks(period="monthly").T
```

Which returns:

|                            | Producer Price Index YoY   | Inflation Rate YoY   |
|:---------------------------|:---------------------------|:---------------------|
| Start Date                 | 2021-05                    | 2021-05              |
| Observations               | 66                         | 66                   |
| Latest Date                | 2026-10                    | 2026-10              |
| Latest Value               | 0.057                      | 0.007                |
| Sign                       | Positive                   | Positive             |
| Run Start                  | 2026-03                    | 2025-10              |
| Run Length                 | 8                          | 13                   |
| Previous Sign              | Negative                   | Negative             |
| Previous Run Start         | 2022-10                    | 2025-08              |
| Previous Run End           | 2026-02                    | 2025-09              |
| Previous Run Length        | 41                         | 2                    |
| Longest Earlier Run Start  | 2021-05                    | 2021-05              |
| Longest Earlier Run End    | 2022-09                    | 2023-05              |
| Longest Earlier Run Length | 17                         | 25                   |

---

## get_unit_root_test
Calculate a test for a unit root, per asset: the Augmented Dickey-Fuller (ADF) test (method="augmented_dickey_fuller"), the Phillips-Perron (PP) test (method="phillips_perron") or the Zivot-Andrews test, which allows for a single structural break at an unknown (endogenously estimated) date (method="zivot_andrews").

All three test the same null hypothesis: the series has a unit root (is a random walk, not mean-reverting); the alternative is that it is stationary. This is a standard first step before modeling a price series or spread with mean-reverting methods, since those methods assume stationarity. `get_kpss_test` is the complement with the null and the alternative swapped.

The ADF test regresses the first difference of the series on its own lagged level and `p` lags of its own first difference. The Phillips-Perron test instead corrects for heteroskedasticity and serial correlation in the errors nonparametrically via a Newey-West long-run variance estimate, rather than by adding lagged-difference terms to the regression, so PP and ADF should broadly agree on the same series.

The ADF and PP tests assume the deterministic component of the series (its constant and/or trend) is stable throughout the sample. If a series instead has a single one-time break -- e.g. a permanent level shift or a change in trend slope, such as a stock split, spin-off, or a structural shift in the business -- the ordinary ADF test is biased towards not rejecting the unit root even for a genuinely (trend-)stationary series with a break. The Zivot-Andrews test corrects for this by adding a break dummy to the ADF regression and choosing, for each asset, the break date that is most favorable to the stationary alternative -- which is why it needs its own (more negative) critical values rather than the ordinary ADF ones.

The formula for method="augmented_dickey_fuller" is as follows:

$$
\Delta Y_{t} = \alpha + \gamma \cdot Y_{t-1} + \sum_{i=1}^{p} \delta_{i} \cdot \Delta Y_{t-i} + \epsilon_{t},\;\; \text{with}\; Y_{t} \;\text{the} \;\text{column} \;\text{level} \;(\text{Adj Close by default}) \;\text{and regression} = \text{"c"} \;(\text{the default});\;\; \text{"ct"} \;\text{adds a trend}\; \beta \cdot t \;\text{and}\; \text{"n"} \;\text{drops}\; \alpha
$$

$$
\text{ADF} = \frac{\hat{\gamma}}{\operatorname{SE}(\hat{\gamma})},\;\; \text{compared with MacKinnon (1994, 2010) critical values and p-values}
$$

$$
p = \text{the number of lags that minimises the AIC},\;\; \text{searched from 0 up to max\_lag},\;\; \text{which defaults to} \;\min\left(\left\lceil 12 \cdot \left(\frac{n}{100}\right)^{\frac{1}{4}} \right\rceil,\; \left\lfloor \frac{n - 5}{3} \right\rfloor\right)
$$

The formula for method="phillips_perron" is as follows:

$$
Y_{t} = \alpha + \rho \cdot Y_{t-1} + u_{t} \;\text{fitted by OLS on the} \;\text{column} \;\text{level} \;(\text{Adj Close by default}),\;\; \text{with regression="c" (the default)};\;\; \text{"ct"} \;\text{adds a trend}\; \beta \cdot t
$$

$$
t_{\rho} = \frac{\hat{\rho} - 1}{\operatorname{SE}(\hat{\rho})},\;\; \gamma_{0} = \frac{\sum \hat{u}_{t}^{2}}{n}\;\;\text{and}\;\; s^{2} = \frac{\sum \hat{u}_{t}^{2}}{n - k},\;\; \text{with } k \text{ the number of coefficients}
$$

$$
\lambda^{2} = \gamma_{0} + 2 \cdot \sum_{j=1}^{l}\left(1 - \frac{j}{l + 1}\right) \cdot \gamma_{j},\;\; \text{with}\;\; \gamma_{j} = \frac{1}{n} \cdot \sum_{t=j+1}^{n} \hat{u}_{t} \cdot \hat{u}_{t-j}\;\;\text{and}\;\; l = \text{lags},\;\; \text{which defaults to int}\left(12 \cdot \left(\frac{n}{100}\right)^{\frac{1}{4}}\right)
$$

$$
Z_{t} = \sqrt{\frac{\gamma_{0}}{\lambda^{2}}} \cdot t_{\rho} - \frac{\lambda^{2} - \gamma_{0}}{2 \cdot \lambda \cdot s} \cdot n \cdot \operatorname{SE}(\hat{\rho})
$$

- The p-value is the MacKinnon (1994) approximation of the Dickey-Fuller distribution and the unit root is rejected at 5% when it is below 0.05, as in the ADF test; the critical values are the finite-sample MacKinnon (2010) ones for the number of observations

The formula for method="zivot_andrews" is as follows:

$$
\Delta Y_{t} = \mu + \theta \cdot \text{DU}_{t} + \beta \cdot t + \alpha \cdot Y_{t-1} + \sum_{i=1}^{p} c_{i} \cdot \Delta Y_{t-i} + \epsilon_{t},\;\; \text{with}\;\; Y_{t} \;\text{the} \;\text{column} \;\text{level} \;(\text{Adj Close by default}) \;\text{and}\; \text{DU}_{t} = 1 \;\text{after the break date}\; T_{B} \;\text{and 0 before it} \;(\text{regression} = \text{"c"},\; \text{the default})
$$

$$
\text{regression} = \text{"t"} \;\text{replaces}\; \theta \cdot \text{DU}_{t} \;\text{by a trend break}\; \gamma \cdot \text{DT}_{t},\;\; \text{with}\;\; \text{DT}_{t} = t - T_{B} \;\text{after the break and 0 before it},\;\; \text{and regression="ct" includes both}
$$

$$
\text{ZA} = \min \;\text{over}\; T_{B} \;\text{of} \;\frac{\hat{\alpha}}{\operatorname{SE}(\hat{\alpha})},\;\; \text{searching every break date outside the first and last trim (15\% by default) of the sample}
$$

$$
p = \text{the number of lags that minimises the AIC},\;\; \text{up to max\_lag (same default as the ADF test)}
$$

For more information about the methods, see the following papers:

- Dickey, D.A. and Fuller, W.A. (1979). "Distribution of the Estimators for Autoregressive Time Series with a Unit Root." Journal of the American Statistical Association, 74(366a), 427-431.
- Phillips, P.C.B., & Perron, P. (1988). "Testing for a Unit Root in Time Series Regression." Biometrika, 75(2), 335-346.
- Zivot, E., & Andrews, D.W.K. (1992). "Further Evidence on the Great Crash, the Oil-Price Shock, and the Unit-Root Hypothesis." Journal of Business & Economic Statistics, 10(3), 251-270.
- Perron, P. (1989). "The Great Crash, the Oil Price Shock, and the Unit Root Hypothesis." Econometrica, 57(6), 1361-1401.

**Also known as:** ADF test, augmented Dickey-Fuller test, PP test, Z_t test, ZA test, structural break unit root test, stationarity test.

**Args:**

- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to test. Defaults to "Adj Close".
- <u>method (str, optional):</u> The test, "augmented_dickey_fuller" for the Augmented Dickey-Fuller
test, "phillips_perron" for the Phillips-Perron test or "zivot_andrews" for the
Zivot-Andrews test with a structural break. Defaults to "augmented_dickey_fuller".
- <u>regression (str, optional):</u> Which deterministic terms to include. For
"augmented_dickey_fuller" one of "n" (none), "c" (constant) or "ct" (constant and trend);
for "phillips_perron" one of "c" or "ct" ("n" is not supported, see
`econometrics.unitroot_model.get_phillips_perron_test` for why); for "zivot_andrews"
which break to allow for, one of "c" (a break in the level/intercept), "t" (a break in
the trend slope) or "ct" (both). Defaults to "c".
- <u>max_lag (int, optional):</u> The maximum number of lagged differences to consider in the AIC
lag search of "augmented_dickey_fuller" and "zivot_andrews" (which selects a single lag
length and reuses it for every break date). Not used with "phillips_perron". Defaults to
the Schwert (1989) rule of thumb, capped at (n - 5) // 3 for short samples.
- <u>lags (int, optional):</u> The truncation lag for the Newey-West long-run variance estimate of
"phillips_perron"; not used by the other methods. Defaults to None, meaning the Schwert
(1989) rule ceil(12 * (n / 100) ** 0.25), capped for short samples as the ADF lag search is.
- <u>trim (float, optional):</u> The fraction of observations excluded from the candidate break
date search at the start and end of the sample, for "zivot_andrews" only. Must be in
[0, 1/3). Defaults to 0.15.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the
assets tested. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The test statistic ("ADF Statistic", "Phillips-Perron Statistic" or
"Zivot-Andrews Statistic"), its p-value, the lags used (the Newey-West truncation lag for
Phillips-Perron), the observations used, the 1%/5%/10% critical values, and whether the
unit root is rejected at the 5% level, per asset. The Zivot-Andrews test adds the
(0-indexed) position of the selected break date within the used sample ("Break Index").
With the ADF test an asset with fewer than 10 observations has NaN values.

**Notes:**

- The method retrieves historical price data based on the specified `period` and runs the
chosen test for each asset in the Toolkit instance.
- The Phillips-Perron p-value is MacKinnon's (1994) approximation and its critical values the
finite-sample MacKinnon (2010) ones.
- Requires statsmodels (`pip install financetoolkit[econometrics]`).

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["EURUSD", "USDJPY", "GBPUSD"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_unit_root_test()
```

Which returns:

|                       |      EURUSD |     USDJPY |      GBPUSD |
|:----------------------|------------:|-----------:|------------:|
| ADF Statistic         |   -1.83568  |   -1.68762 |   -1.81162  |
| P-Value               |    0.362896 |    0.4375  |    0.374708 |
| Lags Used             |    5        |    0       |    2        |
| Observations          | 1345        | 1351       | 1349        |
| Critical Value 1%     |   -3.43522  |   -3.4352  |   -3.43521  |
| Critical Value 5%     |   -2.86369  |   -2.86368 |   -2.86368  |
| Critical Value 10%    |   -2.56792  |   -2.56791 |   -2.56791  |
| Reject Unit Root (5%) |    0        |    0       |    0        |

---

## get_kpss_test
Calculate the Kwiatkowski-Phillips-Schmidt-Shin (KPSS) test for stationarity, per asset.

KPSS is the natural complement to the Augmented Dickey-Fuller test (`get_unit_root_test`): where the ADF null hypothesis is that the series HAS a unit root, the KPSS null hypothesis is that the series IS stationary, with a unit root as the alternative. Running both together is standard practice to triangulate a confident conclusion -- ADF rejecting a unit root and KPSS failing to reject stationarity together give a confident stationarity conclusion, while the two tests disagreeing flags an ambiguous case.

The formula is as follows:

$$
Y_{t} = \alpha + e_{t} \;\text{fitted by OLS on the} \;\text{column} \;\text{level} \;(\text{Adj Close by default}),\;\; \text{with regression="c" (the default)};\;\; \text{"ct"} \;\text{adds a trend}\; \beta \cdot t
$$

$$
S_{t} = \sum_{i=1}^{t} \hat{e}_{i}
$$

$$
\text{KPSS} = \frac{\sum_{t=1}^{n} S_{t}^{2}}{n^{2} \cdot \lambda^{2}}
$$

$$
\lambda^{2} = \frac{1}{n} \cdot \sum \hat{e}_{t}^{2} + \frac{2}{n} \cdot \sum_{s=1}^{l}\left(1 - \frac{s}{l + 1}\right) \cdot \sum_{t=s+1}^{n} \hat{e}_{t} \cdot \hat{e}_{t-s},\;\; \text{with}\;\; l = \text{lags} \;\text{or},\;\; \text{by default, the Hobijn, Franses and Ooms (2004) automatic bandwidth}
$$

- The p-value is interpolated from the KPSS (1992) critical value table, so it is bounded between 0.01 and 0.10

For more information about the method, see the following paper:

- Kwiatkowski, D., Phillips, P.C.B., Schmidt, P., & Shin, Y. (1992). "Testing the Null Hypothesis of Stationarity against the Alternative of a Unit Root." Journal of Econometrics, 54(1-3), 159-178.

**Also known as:** KPSS test, stationarity test.

**Args:**

- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to test. Defaults to "Adj Close".
- <u>regression (str, optional):</u> Which deterministic term to remove before testing, one of "c"
(constant, level-stationarity) or "ct" (constant and trend, trend-stationarity).
Defaults to "c".
- <u>lags (int, optional):</u> The truncation lag for the long-run variance estimate. Defaults
to `statsmodels`' automatic (Hobijn, Franses & Ooms, 2004) bandwidth selection.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the
assets tested. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The KPSS statistic, its p-value, truncation lag used, observations used,
1%/2.5%/5%/10% critical values, and whether stationarity is rejected at the 5% level,
per asset. An asset with fewer than 10 observations has NaN values.

**Notes:**

- The method retrieves historical price data based on the specified `period` and runs the
KPSS test for each asset in the Toolkit instance.
- Requires statsmodels (`pip install financetoolkit[econometrics]`).

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["^GSPC", "^N225"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_kpss_test()
```

Which returns:

|                          |      ^GSPC |      ^N225 |
|:-------------------------|-----------:|-----------:|
| KPSS Statistic           |    4.73448 |    4.79639 |
| P-Value                  |    0.01    |    0.01    |
| Lags Used                |   21       |   21       |
| Observations             | 1299       | 1298       |
| Critical Value 1%        |    0.739   |    0.739   |
| Critical Value 2.5%      |    0.574   |    0.574   |
| Critical Value 5%        |    0.463   |    0.463   |
| Critical Value 10%       |    0.347   |    0.347   |
| Reject Stationarity (5%) |    1       |    1       |

---

## get_engle_granger_cointegration
Calculate the Engle-Granger test for cointegration between every ordered pair of tickers in the Toolkit instance.

Two individually non-stationary series (e.g. two stock prices, each following a random walk) are cointegrated if some linear combination of them is stationary, i.e. they share a long-run equilibrium relationship even though each wanders on its own in the short run. This is the classic statistical foundation for pairs-trading: if two assets are cointegrated, deviations of the spread from its equilibrium level tend to revert, making the spread itself tradeable.

In pairs trading the slope of the regression of the dependent on the independent ticker is the hedge ratio, and its residual is the spread that is traded. Cointegration found in one window often breaks down in the next, so the relationship is usually tested again on a later sample before it is relied on. The result depends on which ticker is the dependent one, so the two orderings can disagree; `get_johansen_cointegration` tests the pair without that choice.

The formula is as follows:

$$
\text{Step 1:}\;\; A_{t} = \alpha + \beta \cdot B_{t} + u_{t},\;\; \text{the OLS regression of the dependent on the independent column level (Adj Close by default)}
$$

$$
\text{Step 2:}\;\; \Delta \hat{u}_{t} = \gamma \cdot \hat{u}_{t-1} + \sum_{i=1}^{p} \delta_{i} \cdot \Delta \hat{u}_{t-i} + \epsilon_{t},\;\; \text{an ADF regression without constant on the residuals}
$$

$$
\text{EG} = \frac{\hat{\gamma}}{\operatorname{SE}(\hat{\gamma})},\;\; \text{compared with the MacKinnon (1994, 2010) cointegration critical values and p-values for two variables}
$$

$$
p = \text{the number of lags that minimises the AIC},\;\; \text{up to max\_lag (same default as get\_unit\_root\_test)}
$$

For more information about the method, see the following paper:

- Engle, R.F. and Granger, C.W.J. (1987). "Co-integration and Error Correction: Representation, Estimation, and Testing." Econometrica, 55(2), 251-276.

**Also known as:** EG test, residual-based cointegration test, pairs-trading test.

**Args:**

- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to test. Defaults to "Adj Close".
- <u>max_lag (int, optional):</u> The maximum number of lagged differences to consider in the
underlying ADF test on the residuals. Defaults to the Schwert (1989) rule of thumb,
capped at (n - 5) // 3 for short samples.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the
tickers paired up. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: One row per ordered `(Dependent, Independent)` ticker pair, with the
Engle-Granger statistic, its p-value, 1%/5%/10% critical values, and whether
cointegration is found at the 5% level -- the test is not symmetric (normalizing on
the dependent ticker matters), so both orderings of every pair are included. A pair
with fewer than 10 common observations has NaN values.

**Notes:**

- The method retrieves historical price data based on the specified `period` for every
ticker in the Toolkit instance and runs the Engle-Granger test on every ordered pair.
- Requires statsmodels (`pip install financetoolkit[econometrics]`).

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["KO", "PEP"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

engle_granger = toolkit.econometrics.get_engle_granger_cointegration()

# The 1% and 10% critical values follow the same pattern as the 5% one.
engle_granger[["Engle-Granger Statistic", "P-Value", "Critical Value 5%", "Cointegrated (5%)"]]
```

Which returns:

|               |   Engle-Granger Statistic |   P-Value |   Critical Value 5% | Cointegrated (5%)   |
|:--------------|--------------------------:|----------:|--------------------:|:--------------------|
| ('KO', 'PEP') |                   -1.0266 |    0.8977 |              -3.341 | False               |
| ('PEP', 'KO') |                   -2.0565 |    0.4991 |              -3.341 | False               |

---

## get_johansen_cointegration
Calculate the Johansen test for cointegration among every ticker in the Toolkit instance.

The Engle-Granger test only handles two assets and imposes an arbitrary normalization (which asset is "dependent"). Johansen's test generalizes this to `N >= 2` assets at once by testing the rank of the long-run coefficient matrix in a Vector Error Correction Model (VECM) fit to all assets jointly. The estimated rank equals the number of independent cointegrating (long-run equilibrium) relationships among the assets: rank 0 means none of them are cointegrated, rank `N` means the whole system is already stationary in levels, and a rank in between means that many independent stationary combinations exist among the `N` individually non-stationary price series.

The formula is as follows:

$$
\Delta Y_{t} = \Pi \cdot Y_{t-1} + \sum_{i=1}^{k} \Gamma_{i} \cdot \Delta Y_{t-i} + \mu + \epsilon_{t},\;\; \text{with } Y_{t} \text{ the vector of column levels (Adj Close by default)},\;\; k = \text{k\_ar\_diff} \;(1 \;\text{by default}) \;\text{and the deterministic term}\; \mu \;\text{set by} \;\text{det\_order} \;\text{:} \;\text{none} \;(- 1,\; \text{Johansen's case}\; 1),\;\; \text{an unrestricted constant } \mu_{0} \text{ (0, the default, case 3) or a linear trend (1: the levels are linearly detrended before the test, evaluated against the case 5 critical values)}
$$

- $$\lambda_{1} \geq \ldots \geq \lambda_{N}$$: the eigenvalues of the reduced-rank regression of $$\Delta Y_{t}$$ on $$Y_{t - 1}$$, both corrected for the lagged differences and $$\mu$$

$$
\operatorname{Trace}(r) = - T \cdot \sum_{i=r+1}^{N} \ln(1 - \lambda_{i})
$$

$$
\operatorname{Max-Eigenvalue}(r) = - T \cdot \ln(1 - \lambda_{r+1})
$$

- Each statistic rejects "rank ≤ r" at the 5% level when it exceeds its 95% critical value

For more information about the method, see the following papers:

- Johansen, S. (1988). "Statistical Analysis of Cointegration Vectors." Journal of Economic Dynamics and Control, 12(2-3), 231-254.
- Johansen, S. (1991). "Estimation and Hypothesis Testing of Cointegration Vectors in Gaussian Vector Autoregressive Models." Econometrica, 59(6), 1551-1580.
- MacKinnon, J.G., Haug, A.A., & Michelis, L. (1999). "Numerical Distribution Functions of Likelihood Ratio Tests for Cointegration." Journal of Applied Econometrics, 14(5), 563-577.

**Also known as:** Johansen test, Johansen procedure, VECM rank test.

**Args:**

- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to test. Defaults to "Adj Close".
- <u>det_order (int, optional):</u> Which deterministic term to include: -1 (none,
Johansen's case 1), 0 (an unrestricted constant, case 3) or 1 (a linear trend,
evaluated against the case 5 critical values). The critical values are those of
MacKinnon, Haug & Michelis (1999). Defaults to 0.
- <u>k_ar_diff (int, optional):</u> The number of lagged first differences to include as
short-run dynamics. Defaults to 1.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the
tickers tested jointly. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: One row per candidate cointegration rank `r = 0, ..., N-1`, with the
corresponding eigenvalue, trace statistic, max-eigenvalue statistic, their 90%/95%/99%
critical values, and whether each is rejected at the 5% level. The estimated rank is the
first row (in rank order) that is NOT rejected. With fewer observations than the
VECM needs (the tickers times k_ar_diff + 1, plus the tickers, plus 3) every row
is NaN.

**Notes:**

- The method retrieves historical price data based on the specified `period` for every ticker
in the Toolkit instance and runs the Johansen test jointly across all of them.
- Requires statsmodels (`pip install financetoolkit[econometrics]`).

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["V", "MA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

johansen = toolkit.econometrics.get_johansen_cointegration()

# The maximum eigenvalue statistic columns follow the same pattern as the trace ones.
johansen[["Eigenvalue", "Trace Statistic", "Trace Critical Value 95%", "Reject (Trace, 5%)"]]
```

Which returns:

|        |   Eigenvalue |   Trace Statistic |   Trace Critical Value 95% | Reject (Trace, 5%)   |
|:-------|-------------:|------------------:|---------------------------:|:---------------------|
| r <= 0 |       0.0107 |           13.9015 |                    15.4943 | False                |
| r <= 1 |       0.0003 |            0.3612 |                     3.8415 | False                |

---

## get_granger_causality
Calculate the Granger causality test, for every ordered pair of tickers in the Toolkit instance, of whether the second helps predict the first.

"Granger causality" is a statement about predictive power, not true causation: one asset is said to Granger-cause another if past values of the first, combined with past values of the second itself, predict the second significantly better than past values of the second alone.

On daily data a significant result can reflect trading hours rather than information: of two markets that close at different times, the one that closes later already contains news the other only prices the next day, so it appears to predict it. The result also depends on `max_lag`, so it is usually checked at a few lag lengths, and across many pairs some significant results arise by chance alone.

The formula is as follows:

$$
\text{Restricted:}\;\; A_{t} = c + \sum_{i=1}^{p} a_{i} \cdot A_{t-i} + e_{t}
$$

$$
\text{Unrestricted:}\;\; A_{t} = c + \sum_{i=1}^{p} a_{i} \cdot A_{t-i} + \sum_{i=1}^{p} b_{i} \cdot B_{t-i} + u_{t}
$$

$$
F = \frac{\frac{\text{RSS}_{r} - \text{RSS}_{u}}{p}}{\frac{\text{RSS}_{u}}{T - 2p - 1}},\;\; \text{F-distributed with} \;(p,\; T - 2p - 1) \;\text{degrees of freedom}
$$

$$
\text{A is the dependent and } B \text{ the independent ticker's column (Return by default)},\;\; p = \text{max\_lag} \;(5 \;\text{by default}) \;\text{and}\; T \;\text{the number of observations after the lags}
$$

For more information about the method, see the following paper:

- Granger, C.W.J. (1969). "Investigating Causal Relations by Econometric Models and Cross-Spectral Methods." Econometrica, 37(3), 424-438.

**Also known as:** Granger causality test, predictive causality, lead-lag test.

**Args:**

- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to test. Defaults to "Return", since
Granger causality assumes a stationary series (unlike the ADF/Engle-Granger tests, which
operate on price levels on purpose).
- <u>max_lag (int, optional):</u> The number of lags of both assets to include in the regressions.
Defaults to 5.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the
tickers paired up. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: One row per ordered `(Dependent, Independent)` ticker pair, with the
F-statistic, its p-value, and whether the independent ticker is found to
Granger-cause the dependent ticker at the 5% level -- Granger causality is inherently
directional, so both orderings of every pair are included.

**Notes:**

- The method retrieves historical return data based on the specified `period` for every
ticker in the Toolkit instance and runs the Granger causality test on every ordered pair.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["CLUSD", "XLE"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_granger_causality()
```

Which returns:

|                  |   F-Statistic |   P-Value | Granger-Causes (5%)   |
|:-----------------|--------------:|----------:|:----------------------|
| ('CLUSD', 'XLE') |        4.2749 |    0.0007 | True                  |
| ('XLE', 'CLUSD') |        1.5533 |    0.1705 | False                 |

---

## get_fractional_difference
Calculate the fractional difference of a price series, per asset, (1 - L)^d applied to the log prices with a d between 0 and 1.

A price series has a unit root, so models that need a stationary input usually take returns, the first difference ($$d = 1$$), which throws away the memory of the series: the return of today says nothing about where the price stands. López de Prado (2018) shows that a fractional d, often between 0.2 and 0.6 for prices, already gives a stationary series that keeps most of that memory (a correlation with the prices well above that of the returns). Find the smallest such d with `get_minimum_fractional_difference`.

The formula is as follows, with $$X_{t}$$ the log of the `column` (Adj Close by default):

$$
\omega_{0} = 1,\;\; \omega_{k} = - \frac{\omega_{k-1} \cdot (d - k + 1)}{k},\;\; \text{the binomial weights of} \;(1 - L)^{d(\text{Hosking},\; 1981)}
$$

$$
\text{Fixed-width window} \;(\text{method} = \text{"fixed\_width"},\; \text{FFD}) \;\text{:} \tilde{X}_{t} = \sum_{k=0}^{l*} \omega_{k} \cdot X_{t-k},\;\; \text{with } l \text{* the last lag whose weight is at least the threshold (1e-5 by default) in absolute value, so every date has the same weights}
$$

$$
\text{Expanding window} \;(\text{method} = \text{"expanding"}) \;\text{:} \tilde{X}_{t} = \sum_{k=0}^{t} \omega_{k} \cdot X_{t-k} \;\text{over the whole history up to}\; t,\;\; \text{kept from the first date at which the share of the weight that falls before the start of the series},\;\; \frac{\sum(j > t)\left|\omega_{j}\right|}{\sum_{j=0}^{n-1}\left|\omega_{j}\right|},\;\; \text{is at most the threshold (0.01 by default)}
$$

$$
d = 0 \;\text{returns the}\; \log \;\text{prices},\;\; d = 1 \;\text{the}\; \log \;\text{returns}
$$

For more information, see the following sources:

- López de Prado, M. (2018). "Advances in Financial Machine Learning." Wiley, chapter 5 (Snippets 5.1 to 5.3).
- Hosking, J.R.M. (1981). "Fractional Differencing." Biometrika, 68(1), 165-176.
- Referenced against RiskLabAI's fractional_difference_std and fractional_difference_fixed ([https://github.com/RiskLabAI/RiskLabAI.py](https://github.com/RiskLabAI/RiskLabAI.py){:target="_blank"}); the weights, the skipped values and the series agree to 1e-14.

**Also known as:** fractional differentiation, fractionally differenced prices, FFD, fixed-width window fracdiff, memory-preserving stationarity transform.

**Args:**

- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to differentiate. Defaults to "Adj Close".
- <u>d (float, optional):</u> The order of differentiation, at least 0. Defaults to 0.4.
- <u>method (Literal["fixed_width", "expanding"], optional):</u> The fixed-width window (FFD) or the
expanding window. Defaults to "fixed_width".
- <u>threshold (float &#124; None, optional):</u> The smallest absolute weight kept by the fixed-width
window, or the largest share of weight left out by the expanding window. Defaults to
None, which is 1e-5 for "fixed_width" and 0.01 for "expanding".
- <u>log_prices (bool, optional):</u> Whether to take the natural logarithm of the series first.
Pass False for a series that can be zero or negative, such as a rate. Defaults to True.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the
assets. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None, which uses the rounding of the Toolkit (4 unless set otherwise).
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The fractionally differentiated series per asset and date, NaN for the
dates before the first full window.

**Notes:**

- Each asset is differentiated over the dates it has a value. With a threshold of 1e-5 the
fixed-width window spans about 3,400 observations for $$d = 0.2$$, 1,460 for $$d = 0.4$$ and 230
for $$d = 0.8$$, so a small d needs a long history: on a shorter one the result is NaN throughout. A
larger threshold shortens the window (1e-4: about 500, 280 and 64; 0.01: about 10).

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2016-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_fractional_difference(d=0.4).tail(5)
```

Which returns:

| Date       |   AAPL |   MSFT |
|:-----------|-------:|-------:|
| 2025-12-24 | 0.237  | 0.2441 |
| 2025-12-26 | 0.2332 | 0.2418 |
| 2025-12-29 | 0.2345 | 0.2401 |
| 2025-12-30 | 0.2313 | 0.241  |
| 2025-12-31 | 0.2274 | 0.2327 |

---

## get_minimum_fractional_difference
Calculate the minimum order of fractional differentiation d that makes the log prices stationary, per asset: the smallest d at which the fixed-width fractional difference passes the Augmented Dickey-Fuller test, the stationary series that keeps the most memory of the prices (López de Prado, 2018, section 5.6).

The formula is as follows, with $$X_{t}$$ the log of the `column` (Adj Close by default):

$$
\text{For}\; d = 0,\; 0.1,\; \ldots,\; 1 \;(\text{step}) \;\text{:} \tilde{X} = \operatorname{FFD}(X,\; d) \;\text{of} \;\text{get\_fractional\_difference} \;\text{with the weight threshold} \;(0.01 \;\text{by default}) \;\text{and the ADF test on}\; \tilde{X} \;\text{with} \;\text{get\_unit\_root\_test} \;(\text{constant},\; \text{lags by AIC up to} \;\text{max\_lag},\; 1 \;\text{by default}),\;\; \text{as in López de Prado's Snippet 5.4}
$$

$$
d^{*} = \text{the smallest}\; d \;\text{whose ADF p-value is below}\; 1 - \text{confidence} \;(0.05 \;\text{by default}),\;\; \frac{\text{refined in steps of step}}{10 \;\text{between the last}\; d \;\text{that fails and the first that passes}}
$$

$$
\text{Correlation} = \text{the correlation of}\; \tilde{X} \;\text{with}\; X \;\text{over the dates of}\; \tilde{X},\;\; \text{the memory kept}
$$

For more information, see the following sources:

- López de Prado, M. (2018). "Advances in Financial Machine Learning." Wiley, section 5.6 (Snippet 5.4).
- Dickey, D.A. and Fuller, W.A. (1979). "Distribution of the Estimators for Autoregressive Time Series with a Unit Root." Journal of the American Statistical Association, 74(366a), 427-431.
- Referenced against RiskLabAI's find_optimal_ffd_simple ([https://github.com/RiskLabAI/RiskLabAI.py](https://github.com/RiskLabAI/RiskLabAI.py){:target="_blank"}). It and López de Prado's Snippet 5.4 run the ADF test with a single lag and a weight threshold of 0.01, the defaults here.

**Also known as:** minimum d, optimal fractional differentiation, minimum FFD, memory-preserving stationarity.

**Args:**

- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to test. Defaults to "Adj Close".
- <u>confidence (float, optional):</u> The confidence of the ADF test: the p-value has to be below
1 - confidence. Defaults to 0.95.
- <u>step (float, optional):</u> The step of the grid of d from 0 to 1. Defaults to 0.1.
- <u>threshold (float, optional):</u> The smallest absolute weight of the fixed-width window. At
1e-5 the window of $$d = 0.1$$ spans about 4,000 observations and at 1e-4 about 500, so
on a few years of data a small d leaves too few values to test. Defaults to 0.01.
- <u>max_lag (int &#124; None, optional):</u> The largest lag of the ADF lag search. Defaults to 1, as
López de Prado (2018) uses. None searches up to min(ceil(12·(n / 100)^(1/4)),
(n - 5) // 3) lags by AIC, which on daily data picks many lags, weakens the test and
pushes the minimum d towards 1.
- <u>log_prices (bool, optional):</u> Whether to take the natural logarithm of the series first.
Pass False for a series that can be zero or negative, such as a rate. Defaults to True.
- <u>grid (bool, optional):</u> Whether to return the ADF test, the correlation and the window
width for every d tried instead of the minimum d per asset. Defaults to False.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the
assets. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None, which uses the rounding of the Toolkit (4 unless set otherwise).
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per asset, the Minimum d and, at that d, the ADF Statistic, P-Value, 5%
Critical Value, Correlation with the log prices, Window Width and Observations (NaN
when no d up to 1 passes); with grid=True the ADF Statistic, P-Value, Lags Used,
Observations, Critical Value 5%, Correlation, Window Width and Stationary per d.

**Notes:**

- Requires statsmodels (`pip install financetoolkit[econometrics]`) for the ADF test.
- A d whose window is longer than the history leaves fewer than 10 values to test and
shows NaN; pass a larger threshold or a longer history.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2016-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_minimum_fractional_difference()
```

Which returns:

|                   |      AAPL |      MSFT |
|:------------------|----------:|----------:|
| Minimum d         |    0.53   |    0.56   |
| ADF Statistic     |   -2.9108 |   -2.9734 |
| P-Value           |    0.0441 |    0.0375 |
| Critical Value 5% |   -2.8627 |   -2.8627 |
| Correlation       |    0.9917 |    0.9919 |
| Window Width      |   10      |    9      |
| Observations      | 2503      | 2504      |

---

## get_bubble_test
Calculate the GSADF test of Phillips, Shi and Yu (2015) or the SADF test of Phillips, Wu and Yu (2011) for explosive behaviour, a bubble, in the log prices, per asset.

The ADF test looks for mean reversion (a left tail); these tests look at the right tail: a price that grows faster than a random walk, as in a bubble, gives a large positive ADF statistic over the window of the bubble. The SADF test runs the ADF regression on every window from the first observation that is at least the minimum window long and takes the largest statistic; the GSADF test also moves the start of the window, so it finds a bubble that came after an earlier one collapsed. A statistic above its critical value rejects the random walk in favour of explosive behaviour somewhere in the sample; which dates are explosive follows from `get_bubble_episodes`.

The formula is as follows, with $$y_{t}$$ the log of the `column` (Adj Close by default) and T observations:

$$
\operatorname{ADF}(r_{1},\; r_{2}) = \frac{\hat{\beta}}{\operatorname{SE}(\hat{\beta}) \;\text{of}\; \Delta y_{t}} = \alpha + \beta \cdot y_{t-1} + \sum_{i=1}^{k} \gamma_{i} \cdot \Delta y_{t-i} + \epsilon_{t} \;\text{on the observations}\; r_{1} \;\text{to}\; r_{2},\;\; \text{with}\;\; k = \text{lag\_order}
$$

$$
w = \left\lfloor \left(0.01 + \frac{1.8}{\sqrt{T}}\right) \cdot T \right\rfloor,\;\; \text{the minimum window of PSY (2015)}
$$

$$
\text{SADF} = \max \;\text{over}\; r_{2} \geq w - 1 \;\text{of ADF}(0,\; r_{2})
$$

$$
\text{GSADF} = \max \;\text{over}\; r_{2} \;\text{of BSADF}(r_{2}),\;\; \text{with}\;\; \operatorname{BSADF}(r_{2}) = \max \;\text{over}\; r_{1} \leq r_{2} - w + 1 \;\text{of ADF}(r_{1},\; r_{2})
$$

$$
\text{Critical values and the p-value from} \;\text{replications} \;\text{random walks}\; y_{t} = y_{t-1} + \frac{1}{T} + \epsilon_{t},\;\; \epsilon_{t} \sim N(0,\; 1),\;\; \text{with the same } T \text{, } w \text{ and } k \text{: the 90\%, 95\% and 99\% quantiles of the simulated statistic and the share of simulated statistics at least as large}
$$

For more information, see the following papers:

- Phillips, P.C.B., Shi, S. and Yu, J. (2015). "Testing for Multiple Bubbles: Historical Episodes of Exuberance and Collapse in the S&P 500." International Economic Review, 56(4), 1043-1078.
- Phillips, P.C.B., Wu, Y. and Yu, J. (2011). "Explosive Behavior in the 1990s Nasdaq: When Did Exuberance Escalate Asset Values?" International Economic Review, 52(1), 201-226.
- López de Prado, M. (2018). "Advances in Financial Machine Learning." Wiley, section 17.4.2 (Snippets 17.1 to 17.4).
- Referenced against RiskLabAI's get_gsadf_statistic and simulate_psy_critical_values ([https://github.com/RiskLabAI/RiskLabAI.py](https://github.com/RiskLabAI/RiskLabAI.py){:target="_blank"}). Every window statistic agrees with statsmodels' adfuller to 1e-10, and the simulated critical values with those of PSY (2015, Table 1).

**Also known as:** GSADF test, SADF test, sup ADF, generalized sup ADF, PSY test, PWY test, explosive root test, right-tailed unit root test, bubble detection.

**Args:**

- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to test. Defaults to "Adj Close".
- <u>method (Literal["gsadf", "sadf"], optional):</u> The generalized (GSADF) or the forward (SADF)
test. Defaults to "gsadf".
- <u>lag_order (int, optional):</u> The number of lagged differences k in every ADF regression.
Defaults to 0, as PSY (2015) use.
- <u>minimum_window (int &#124; None, optional):</u> The smallest window in observations. Defaults to
None, floor((0.01 + 1.8 / √T)·T).
- <u>replications (int, optional):</u> The number of simulated random walks for the critical
values. Defaults to 2,000, as in - <u>PSY (2015):</u> the critical values serve every series of
the same length, so with 500 random walks the size of the test at 5% ranges from about
3.5% to 7% depending on the seed.
- <u>seed (int, optional):</u> The seed of the simulation. Defaults to 0.
- <u>log_prices (bool, optional):</u> Whether to take the natural logarithm of the series first.
Pass False for a series that can be zero or negative, such as a rate. Defaults to True.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the
assets. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None, which uses the rounding of the Toolkit (4 unless set otherwise).
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The GSADF (or SADF) statistic, its simulated p-value, the 10%, 5% and 1%
critical values (the 90%, 95% and 99% quantiles), the observations, minimum window,
lag order and replications, and whether the series is explosive at the 5% level, per
asset.

**Notes:**

- The test fits about $$(T - w)^{2} / 2$$ regressions per series and as many per simulated path,
each from window sums of prefix sums: about 0.14 seconds per path for ten years of daily
data and 0.04 for five, so 2,000 replications take about 5 minutes and 80 seconds, and
with lag_order=2 about 60% longer. Ten years of weekly data take about 16 seconds;
monthly data, as in PSY (2015), a few. The critical values depend
only on T, w, the lag order, the replications and the seed, so assets with the same
number of observations share one simulation, which is kept for the session.
- Each asset is tested over the dates it has a value.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["NVDA", "KO"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2016-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_bubble_test(period="weekly")
```

Which returns:

|                    |      NVDA |        KO |
|:-------------------|----------:|----------:|
| GSADF Statistic    |    1.5086 |    1.056  |
| P-Value            |    0.3165 |    0.6405 |
| Critical Value 10% |    1.9834 |    1.9834 |
| Critical Value 5%  |    2.2071 |    2.2071 |
| Critical Value 1%  |    2.8067 |    2.8067 |
| Observations       |  522      |  522      |
| Minimum Window     |   46      |   46      |
| Lags               |    0      |    0      |
| Replications       | 2000      | 2000      |
| Explosive (5%)     |    0      |    0      |

---

## get_bubble_episodes
Date-stamp the explosive episodes (bubbles) of the log prices, per asset, with the backward SADF (BSADF) sequence of Phillips, Shi and Yu (2015) or the forward ADF sequence of Phillips, Wu and Yu (2011).

For every date, the BSADF statistic is the largest ADF statistic of the windows that end on that date, so it only uses data up to the date: it rises once the prices start to grow explosively and falls back when the bubble collapses. A bubble starts on the first date its statistic crosses above the critical value of that date and ends on the last date before it falls back. PSY (2015) show that the backward windows date-stamp a bubble that follows an earlier one, which the forward sequence of PWY (2011) misses.

The formula is as follows, with $$y_{t}$$ the log of the `column` (Adj Close by default) and the $$\text{ADF} (r_{1} , r_{2})$$ statistics and minimum window w of `get_bubble_test`:

$$
\operatorname{BSADF}(r_{2}) = \max \;\text{over}\; r_{1} \leq r_{2} - w + 1 \;\text{of ADF}(r_{1},\; r_{2}) \;(\text{method} = \text{"gsadf"}),\;\; \text{or}\;\; \operatorname{ADF}(0,\; r_{2}) \;(\text{method} = \text{"sadf"})
$$

$$
\operatorname{cv}(r_{2}) = \text{the} \;\text{confidence} \;\text{quantile} \;(95\% \;\text{by default}) \;\text{of the same statistic at}\; r_{2} \;\text{over} \;\text{replications} \;\text{simulated random walks}\; y_{t} = y_{t-1} + \frac{1}{T} + \epsilon_{t}
$$

$$
\text{Bubble on } r_{2} \text{ when the statistic is above } cv (r_{2});\;\; \text{an episode is a run of such dates of at least minimum\_duration observations},\;\; \text{by default round}(\log(T)) (\delta \cdot \log(T) \;\text{with}\; \delta = 1 \;\text{in PSY},\; 2015)
$$

For more information, see the following papers:

- Phillips, P.C.B., Shi, S. and Yu, J. (2015). "Testing for Multiple Bubbles: Historical Episodes of Exuberance and Collapse in the S&P 500." International Economic Review, 56(4), 1043-1078.
- Phillips, P.C.B., Wu, Y. and Yu, J. (2011). "Explosive Behavior in the 1990s Nasdaq: When Did Exuberance Escalate Asset Values?" International Economic Review, 52(1), 201-226.
- Referenced against RiskLabAI's get_bsadf_sequence and get_bubble_episodes ([https://github.com/RiskLabAI/RiskLabAI.py](https://github.com/RiskLabAI/RiskLabAI.py){:target="_blank"}).

**Also known as:** BSADF, backward sup ADF, PSY date-stamping, bubble dating, explosive episodes, exuberance periods.

**Args:**

- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to test. Defaults to "Adj Close".
- <u>method (Literal["gsadf", "sadf"], optional):</u> The backward (BSADF, PSY) or the forward (ADF,
PWY) sequence. Defaults to "gsadf".
- <u>lag_order (int, optional):</u> The number of lagged differences k in every ADF regression.
Defaults to 0.
- <u>minimum_window (int &#124; None, optional):</u> The smallest window in observations. Defaults to
None, floor((0.01 + 1.8 / √T)·T).
- <u>confidence (float, optional):</u> The confidence of the critical value per date. Defaults to
0.95.
- <u>minimum_duration (int &#124; None, optional):</u> The fewest observations an episode lasts.
Defaults to None, round(log(T)).
- <u>replications (int, optional):</u> The number of simulated random walks for the critical
values. Defaults to 2,000, as in PSY (2015).
- <u>seed (int, optional):</u> The seed of the simulation. Defaults to 0.
- <u>log_prices (bool, optional):</u> Whether to take the natural logarithm of the series first.
Pass False for a series that can be zero or negative, such as a rate. Defaults to True.
- <u>time_series (bool, optional):</u> Whether to return the statistic, its critical value and
whether it is above it per date instead of the episodes. Defaults to False.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the
assets. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None, which uses the rounding of the Toolkit (4 unless set otherwise).
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: Per asset and episode, the Start and End date, the Duration in
observations, and the Peak Date and Peak Statistic (the largest statistic of the
episode); with time_series=True the BSADF (or ADF) statistic, Critical Value and Bubble
per date and asset.

**Notes:**

- The computation and its time are those of `get_bubble_test`, which shares the
simulation when called with the same settings.
- The critical value of a date is simulated for the observations up to it, so a date's
verdict only uses data up to that date.
- The critical value of a single date is lower than that of the GSADF test, which is the
largest statistic over all dates, so episodes can be dated while `get_bubble_test` does
not reject the random walk for the whole sample (as for NVDA below). PSY (2015) read
the dating as a monitoring device and the GSADF test as the verdict on the sample.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["NVDA", "KO"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2016-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_bubble_episodes(period="weekly")
```

Which returns:

|             | Start                 | End                   |   Duration | Peak Date             |   Peak Statistic |
|:------------|:----------------------|:----------------------|-----------:|:----------------------|-----------------:|
| ('NVDA', 1) | 2020-08-03/2020-08-09 | 2020-09-07/2020-09-13 |          6 | 2020-08-24/2020-08-30 |           1.0849 |
| ('NVDA', 2) | 2021-10-25/2021-10-31 | 2021-12-27/2022-01-02 |         10 | 2021-11-15/2021-11-21 |           1.409  |
| ('NVDA', 3) | 2023-05-22/2023-05-28 | 2023-07-31/2023-08-06 |         11 | 2023-06-12/2023-06-18 |           1.0915 |
| ('NVDA', 4) | 2024-01-29/2024-02-04 | 2025-01-20/2025-01-26 |         52 | 2024-06-10/2024-06-16 |           1.5086 |

---

## get_chow_dickey_fuller_test
Calculate the Chow-type Dickey-Fuller test for a switch from a random walk to explosive behaviour at an unknown date, per asset (López de Prado, 2018, section 17.3.3; Homm and Breitung, 2012).

The regression lets the log prices follow a random walk up to a break date and an explosive process after it, and the statistic is the t-statistic of the explosive coefficient. Every date in the middle of the sample is tried as the break; the largest statistic (SDFC) is compared with critical values simulated under a random walk, and its date is the most likely start of the explosive regime. Unlike the Chow test of `get_chow_test`, which tests a known break in the coefficients of a regression, the break date is unknown and the alternative is a bubble.

The formula is as follows, with $$y_{t}$$ the log of the `column` (Adj Close by default) minus its first value, so the test does not depend on the level of the prices:

$$
\Delta y_{t} = \delta \cdot y_{t-1} \cdot D_{t}(\tau) + \epsilon_{t},\;\; D_{t}(\tau) = 1 \;\text{after the break date}\; \tau \;\text{and 0 up to it}
$$

$$
\operatorname{DFC}(\tau) = \frac{\hat{\delta}}{\operatorname{SE}(\hat{\delta})},\;\; \text{with SE from the residuals of all}\; T - 1 \;\text{changes}
$$

$$
\text{SDFC} = \max \;\text{over}\; \tau \;\text{from} \;\left\lfloor \text{trim} \cdot T \right\rfloor \;\text{to}\; T - 1 - \left\lfloor \text{trim} \cdot T \right\rfloor \;\text{of DFC}(\tau),\;\; \text{the supremum over the break dates of Andrews (1993)}
$$

- Critical values and the p-value from `replications` Gaussian random walks of the same length started at zero

For more information, see the following sources:

- Homm, U. and Breitung, J. (2012). "Testing for Speculative Bubbles in Stock Markets: A Comparison of Alternative Methods." Journal of Financial Econometrics, 10(1), 198-231.
- Andrews, D.W.K. (1993). "Tests for Parameter Instability and Structural Change With Unknown Change Point." Econometrica, 61(4), 821-856.
- López de Prado, M. (2018). "Advances in Financial Machine Learning." Wiley, section 17.4.1.

The book writes the regression on the log prices as they are; here their first value is subtracted, so the statistic does not change with the price level.

**Also known as:** DFC, SDFC, Chow-type Dickey-Fuller, sup DFC, Homm-Breitung test, explosive break test.

**Args:**

- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to test. Defaults to "Adj Close".
- <u>trim (float, optional):</u> The share of observations at either end that is not tried as the
break date. Defaults to 0.15.
- <u>replications (int, optional):</u> The number of simulated random walks for the critical
values. Defaults to 1000.
- <u>seed (int, optional):</u> The seed of the simulation. Defaults to 0.
- <u>log_prices (bool, optional):</u> Whether to take the natural logarithm of the series first.
Pass False for a series that can be zero or negative, such as a rate. Defaults to True.
- <u>time_series (bool, optional):</u> Whether to return $$\text{DFC} (\tau)$$ per break date instead of the test.
Defaults to False.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the
assets. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None, which uses the rounding of the Toolkit (4 unless set otherwise).
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: The SDFC statistic, the break date, the simulated p-value, the 10%, 5% and 1%
critical values (the 90%, 95% and 99% quantiles), the observations and replications, and
whether the series turns explosive at the 5% level, per asset; with time_series=True
$$\text{DFC} (\tau)$$ per date and asset.

**Notes:**

- The test is right-tailed: a large positive statistic points to explosive behaviour after
the break date. A falling or mean-reverting series gives negative statistics.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["NVDA", "KO"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2016-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_chow_dickey_fuller_test()
```

Which returns:

|                    | NVDA       | KO         |
|:-------------------|:-----------|:-----------|
| SDFC Statistic     | 2.7139     | 1.0338     |
| Break Date         | 2019-06-03 | 2023-10-05 |
| P-Value            | 0.004      | 0.21       |
| Critical Value 10% | 1.4845     | 1.4845     |
| Critical Value 5%  | 1.8067     | 1.8067     |
| Critical Value 1%  | 2.4087     | 2.4087     |
| Observations       | 2514       | 2514       |
| Replications       | 1000       | 1000       |
| Explosive (5%)     | True       | False      |

---

## get_linear_regression
Calculate the rolling Linear Regression of a price series: the end point of the least-squares line over the window, its slope, intercept and angle, and the Time Series Forecast one period ahead.

Over every window, a straight line is fitted through the prices by ordinary least squares. Its end point is a moving average that lags less than a simple average, as it follows the trend of the window rather than its middle (Chande and Kroll call it the linear regression indicator), the slope is the trend in price per period, and the Time Series Forecast extends the line by one period. A price above a rising regression line is read as a confirmed uptrend, and the slope turning negative as the trend of the window turning down.

The formula is as follows, with time $$x = 0$$, ..., window - 1 from the oldest price of the window to the latest:

$$
\text{Slope} \;(b_{1}) = \frac{\operatorname{Sum}((x - \operatorname{Mean}(x)) \cdot (\text{Close} - \operatorname{Mean}(\text{Close})))}{\operatorname{Sum}((x - \operatorname{Mean}(x))^{2})}
$$

$$
\text{Intercept} \;(b_{0}) = \operatorname{Mean}(\text{Close}) - b_{1} \cdot \operatorname{Mean}(x),\;\; \text{the line at the oldest period of the window}
$$

$$
\text{Linear Regression} = b_{0} + b_{1} \cdot (\text{window} - 1),\;\; \text{the line at the latest period}
$$

$$
\text{Time Series Forecast} = b_{0} + b_{1} \cdot \text{window},\;\; \text{the line one period ahead}
$$

$$
\text{Angle} = \operatorname{arctan}(b_{1}) \;\text{in degrees}
$$

For more information, see the following sources:

- Chande, T.S. & Kroll, S. (1994). "The New Technical Trader." Wiley.
- Referenced against TA-Lib's LINEARREG, LINEARREG_SLOPE, LINEARREG_INTERCEPT, LINEARREG_ANGLE and TSF ([https://ta-lib.org/functions/linearreg.html](https://ta-lib.org/functions/linearreg.html){:target="_blank"}).
- pandas-ta-classic: linreg ([https://github.com/xgboosted/pandas-ta-classic](https://github.com/xgboosted/pandas-ta-classic){:target="_blank"}).
- Tulip Indicators: linreg, linregslope, linregintercept and tsf ([https://tulipindicators.org/linreg](https://tulipindicators.org/linreg){:target="_blank"}).

**Also known as:** LINEARREG, linear regression indicator, end-point moving average, least squares moving average, LSMA, TSF, time series forecast, linear regression slope, intercept, angle.

**Args:**

- <u>period (str &#124; None, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or
yearly). Defaults to None, which uses "daily".
- <u>column (str, optional):</u> The historical data column the statistic is calculated on: "Adj Close"
for the prices (the series as given with `Econometrics(data=...)`), "Close" for the
traded prices or "Return" for the returns (the changes of the series). Defaults to "Adj Close".
- <u>window (int, optional):</u> The number of periods the line is fitted over, at least 2.
Defaults to 14.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the assets.
Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame:
Linear Regression, Slope, Intercept, Angle and Time Series Forecast.

**Notes:**

- The method takes the `column` series of the specified `period` and calculates the Linear Regression for each
asset, each over the dates it has a value. The first value needs a full window of data from the start date.
- The columns agree with TA-Lib's LINEARREG, LINEARREG_SLOPE, LINEARREG_INTERCEPT, LINEARREG_ANGLE and TSF.
- The slope is in price per period and the angle depends on the scale of the prices, so neither compares
across securities with different share prices; the Correlation Trend Indicator
(`toolkit.technicals.get_correlation_trend_indicator`) does.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_linear_regression().xs("AAPL", level=1, axis="columns").tail(5)
```

Which returns:

| Date       |    Angle |   Intercept |   Linear Regression |   Slope |   Time Series Forecast |
|:-----------|---------:|------------:|--------------------:|--------:|-----------------------:|
| 2025-12-24 | -30.142  |     277.998 |             270.449 | -0.5807 |                269.868 |
| 2025-12-26 | -27.157  |     277.175 |             270.506 | -0.513  |                269.993 |
| 2025-12-29 | -23.7844 |     276.411 |             270.682 | -0.4407 |                270.241 |
| 2025-12-30 | -21.4583 |     275.809 |             270.7   | -0.3931 |                270.306 |
| 2025-12-31 | -17.2038 |     274.774 |             270.749 | -0.3096 |                270.44  |

---

## get_slope
Calculate the Slope of a price series: the average change in price per period over a window, the rise over the run between the price `window` periods ago and the latest price.

The formula is as follows:

$$
\text{Slope} = \frac{\text{Close} - \operatorname{Close}(t - \text{window})}{\text{window}}
$$

$$
\text{Angle} = \operatorname{arctan}(\text{Slope}) \;\text{in degrees}
$$

The slope over one period is the change from the previous close. Only the two ends of the window count: the least-squares slope, which uses every price of the window, is the Slope of `get_linear_regression`.

For more information, see the following sources:

- Referenced against pandas-ta-classic's slope ([https://github.com/xgboosted/pandas-ta-classic](https://github.com/xgboosted/pandas-ta-classic){:target="_blank"}).

**Also known as:** slope, rise over run, average change per period, angle.

**Args:**

- <u>period (str &#124; None, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or
yearly). Defaults to None, which uses "daily".
- <u>column (str, optional):</u> The historical data column the statistic is calculated on: "Adj Close"
for the prices (the series as given with `Econometrics(data=...)`), "Close" for the
traded prices or "Return" for the returns (the changes of the series). Defaults to "Adj Close".
- <u>window (int, optional):</u> The number of periods between the two prices. Defaults to 1.
- <u>as_angle (bool, optional):</u> Whether to return the angle of the slope in degrees instead
of the slope. Defaults to False.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the assets.
Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame:
Slope values, in price per period, or in degrees with `as_angle`.

**Notes:**

- The method takes the `column` series of the specified `period` and calculates the Slope for each asset, each
over the dates it has a value. The first value needs a full window of data from the start date.
- The slope agrees with pandas-ta-classic's slope and the angle its slope with as_angle=True and
to_degrees=True (pandas-ta-classic gives radians unless asked for degrees).
- The slope is in price per period, so it does not compare across securities with different share
prices.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_slope(window=5).tail(5)
```

Which returns:

| Date       |    AAPL |    MSFT |
|:-----------|--------:|--------:|
| 2025-12-24 |  0.3926 |  2.3604 |
| 2025-12-26 |  0.2412 |  0.7399 |
| 2025-12-29 |  0.0179 |  0.2341 |
| 2025-12-30 |  0.4205 |  0.5078 |
| 2025-12-31 | -0.0997 | -0.6407 |

---

## get_rolling_correlation
Calculate the rolling Pearson Correlation of every series with another over a window: with the benchmark, another ticker of the Toolkit (or series of the data) or another price column of the same ticker, such as the high against the low as in TA-Lib.

The correlation is +1 when the two series move up and down together in a straight-line relation, -1 when they move in opposite directions and around 0 when they are unrelated. By default it correlates the returns, so it shows whether the moves of two assets go together over the window. On price levels (column="Adj Close"), two series that both trend have a high correlation even when their daily moves are unrelated, so it then shows whether two prices follow the same course over the window rather than whether their returns are related.

The formula is as follows:

$$
\text{Correlation} = \frac{\operatorname{Covariance}(X,\; Y,\; \text{window})}{\operatorname{StdDev}(X,\; \text{window}) \cdot \operatorname{StdDev}(Y,\; \text{window})}
$$

with X the `column` series of each asset and Y that of `against`.

For more information, see the following sources:

- Pearson, K. (1895). "Notes on Regression and Inheritance in the Case of Two Parents." Proceedings of the Royal Society of London, 58, 240-242.
- Referenced against TA-Lib's CORREL ([https://ta-lib.org/functions/correl.html](https://ta-lib.org/functions/correl.html){:target="_blank"}).
- pandas-ta-classic: correl ([https://github.com/xgboosted/pandas-ta-classic](https://github.com/xgboosted/pandas-ta-classic){:target="_blank"}).

**Also known as:** CORREL, Pearson correlation coefficient, rolling correlation, correlation with the benchmark.

**Args:**

- <u>period (str &#124; None, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or
yearly). Defaults to None, which uses "daily".
- <u>column (str, optional):</u> The historical data column that is correlated: "Return" for the
returns (the changes of the series), "Adj Close" for the prices (the series as given
with `Econometrics(data=...)`) or another price column such as "High". Defaults to
"Return".
- <u>window (int, optional):</u> The number of periods. Defaults to 30.
- <u>against (str &#124; None, optional):</u> What to correlate with: a ticker of the Toolkit (or a
series of the data), such as "Benchmark" or "MSFT", or another column of the same
ticker, such as "Low" with column="High". Defaults to None, which uses the
Benchmark or, without one, the second series.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the assets.
Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame:
Correlation values between -1 and 1, a column per asset (the series it is correlated
with is left out, as its correlation with itself is 1).

**Notes:**

- The method takes the `column` series of the specified `period` and correlates each asset with
`against` over the dates both have a value, so a cryptocurrency's weekends do not count against
a stock.
- The correlation agrees with TA-Lib's CORREL and pandas-ta-classic's correl, which take the series as
given; TA-Lib's default compares the high with the low (column="High", against="Low").
- A window in which either series is flat has no correlation and is missing, where TA-Lib and pandas-ta-
classic give 0.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_rolling_correlation().tail(5)
```

Which returns:

| Date       |   AAPL |   MSFT |
|:-----------|-------:|-------:|
| 2025-12-24 | 0.4834 | 0.3484 |
| 2025-12-26 | 0.4882 | 0.3495 |
| 2025-12-29 | 0.5123 | 0.2947 |
| 2025-12-30 | 0.5132 | 0.3062 |
| 2025-12-31 | 0.4705 | 0.315  |

---

## get_rolling_median
Calculate the rolling Median of a price series: the middle price of the window.

The median is a moving average that a single outlier, such as one day with a spike, does not pull along, as it depends only on the order of the prices.

The formula is as follows:

$$
\text{Median} = \text{the middle value of the sorted prices of the window},\;\; \text{or the mean of the two middle values for an even window}
$$

For more information, see the following sources:

- Tukey, J.W. (1977). "Exploratory Data Analysis." Addison-Wesley, for running medians.
- Referenced against TA-Lib's MEDIAN ([https://ta-lib.org/functions/median.html](https://ta-lib.org/functions/median.html){:target="_blank"}).
- pandas-ta-classic: median ([https://github.com/xgboosted/pandas-ta-classic](https://github.com/xgboosted/pandas-ta-classic){:target="_blank"}).
- finta: SMM ([https://github.com/peerchemist/finta](https://github.com/peerchemist/finta){:target="_blank"}).

**Also known as:** MEDIAN, moving median, simple moving median, SMM.

**Args:**

- <u>period (str &#124; None, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or
yearly). Defaults to None, which uses "daily".
- <u>column (str, optional):</u> The historical data column the statistic is calculated on: "Adj Close"
for the prices (the series as given with `Econometrics(data=...)`), "Close" for the
traded prices or "Return" for the returns (the changes of the series). Defaults to "Adj Close".
- <u>window (int, optional):</u> The number of periods. Defaults to 30.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the assets.
Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame:
Median values.

**Notes:**

- The method takes the `column` series of the specified `period` and calculates the Median for each asset, each
over the dates it has a value. The first value needs a full window of data from the start date.
- The median agrees with TA-Lib's MEDIAN, pandas-ta-classic's median and finta's SMM (whose default window is
9).

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_rolling_median().tail(5)
```

Which returns:

| Date       |    AAPL |    MSFT |
|:-----------|--------:|--------:|
| 2025-12-24 | 273.408 | 481.221 |
| 2025-12-26 | 273.408 | 481.221 |
| 2025-12-29 | 273.408 | 481.221 |
| 2025-12-30 | 273.408 | 481.221 |
| 2025-12-31 | 273.408 | 480.468 |

---

## get_rolling_percentile
Calculate the rolling Percentile of a price series: the price below which a given share of the prices of the window lies, such as the median (0.5) or the upper quartile (0.75).

The formula is as follows, per method:

$$
\text{"nearest\_rank":}\;\; \text{the k-th smallest price of the window},\;\; k = \left\lceil \text{percentile} \cdot \text{window} \right\rceil \;(\text{Hyndman and Fan's definition}\; 1)
$$

$$
\text{"linear":}\;\; \text{interpolated between the two prices around position percentile} \cdot (\text{window} - 1) \;\text{of the sorted window},\;\; \text{counting from 0 (Hyndman and Fan's definition 7)}
$$

For more information, see the following sources:

- Hyndman, R.J. & Fan, Y. (1996). "Sample Quantiles in Statistical Packages." The American Statistician, 50(4), 361-365.
- Referenced against TA-Lib's PERCENTILE ([https://ta-lib.org/functions/percentile.html](https://ta-lib.org/functions/percentile.html){:target="_blank"}).
- pandas-ta-classic: quantile ([https://github.com/xgboosted/pandas-ta-classic](https://github.com/xgboosted/pandas-ta-classic){:target="_blank"}).

**Also known as:** PERCENTILE, quantile, rolling quantile, moving percentile.

**Args:**

- <u>period (str &#124; None, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or
yearly). Defaults to None, which uses "daily".
- <u>column (str, optional):</u> The historical data column the statistic is calculated on: "Adj Close"
for the prices (the series as given with `Econometrics(data=...)`), "Close" for the
traded prices or "Return" for the returns (the changes of the series). Defaults to "Adj Close".
- <u>window (int, optional):</u> The number of periods. Defaults to 100.
- <u>percentile (float, optional):</u> The percentile as a decimal between 0 and 1. Defaults
to 0.5.
- <u>method (str, optional):</u> "nearest_rank" or "linear". Defaults to "nearest_rank".
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the assets.
Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame:
Percentile values.

**Notes:**

- The method takes the `column` series of the specified `period` and calculates the Percentile for each asset,
each over the dates it has a value. The first value needs a full window of data from the start date.
- The nearest rank agrees with TA-Lib's PERCENTILE, and the linear interpolation pandas-ta-classic's
quantile.
- The percentile is a decimal (0.5 is the median) where TA-Lib takes a percentage.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_rolling_percentile(percentile=0.9).tail(5)
```

Which returns:

| Date       |    AAPL |    MSFT |
|:-----------|--------:|--------:|
| 2025-12-24 | 276.586 | 518.336 |
| 2025-12-26 | 276.586 | 517.138 |
| 2025-12-29 | 276.586 | 516.368 |
| 2025-12-30 | 276.586 | 516.368 |
| 2025-12-31 | 276.586 | 516.368 |

---

## get_percent_rank
Calculate the Percent Rank of a price series: the share of the previous `window` prices that are lower than the latest price.

A Percent Rank of 1 means the price is above every price of the window, a new high for the window, and 0 that it is at or below all of them. It ranks the price within its recent history, and Connors uses it in ConnorsRSI to rank the latest return.

The formula is as follows:

$$
\text{Percent Rank} = \frac{\operatorname{Count}(\operatorname{Close}(t - i) < \operatorname{Close}(t),\; i = 1,\; \ldots,\; \text{window})}{\text{window}}
$$

For more information, see the following sources:

- Connors, L., Alvarez, C. & Radtke, M. (2012). "An Introduction to ConnorsRSI." Connors Research Trading Strategy Series.
- Referenced against TA-Lib's PERCENTRANK ([https://ta-lib.org/functions/percentrank.html](https://ta-lib.org/functions/percentrank.html){:target="_blank"}).

**Also known as:** PERCENTRANK, percentile rank, percent rank.

**Args:**

- <u>period (str &#124; None, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or
yearly). Defaults to None, which uses "daily".
- <u>column (str, optional):</u> The historical data column the statistic is calculated on: "Adj Close"
for the prices (the series as given with `Econometrics(data=...)`), "Close" for the
traded prices or "Return" for the returns (the changes of the series). Defaults to "Adj Close".
- <u>window (int, optional):</u> The number of previous periods. Defaults to 100.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the assets.
Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame:
Percent Rank values as decimals.

**Notes:**

- The method takes the `column` series of the specified `period` and calculates the Percent Rank for each asset,
each over the dates it has a value. The first value needs a full window of data from the start date.
- The Percent Rank agrees with TA-Lib's PERCENTRANK divided by 100: a decimal between 0 and 1 where TA-Lib
gives a percentage.
- The latest price is compared with the `window` prices before it, so the first value needs `window` + 1
prices.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_percent_rank().tail(5)
```

Which returns:

| Date       |   AAPL |   MSFT |
|:-----------|-------:|-------:|
| 2025-12-24 |   0.83 |   0.2  |
| 2025-12-26 |   0.8  |   0.2  |
| 2025-12-29 |   0.82 |   0.2  |
| 2025-12-30 |   0.78 |   0.21 |
| 2025-12-31 |   0.73 |   0.13 |

---

## get_rolling_z_score
Calculate the rolling Z-Score of a price series: the number of standard deviations the price lies above or below its moving average.

A Z-Score of 2 puts the price two standard deviations above its average of the window, on the upper Bollinger Band of the same window measured with the sample standard deviation. Mean-reversion strategies read large absolute values as stretched prices.

The formula is as follows:

$$
\text{Z-Score} = \frac{\text{Close} - \operatorname{SMA}(\text{Close},\; \text{window})}{\operatorname{StdDev}(\text{Close},\; \text{window})}
$$

with the sample standard deviation (ddof=1).

For more information, see the following sources:

- Referenced against pandas-ta-classic's zscore ([https://github.com/xgboosted/pandas-ta-classic](https://github.com/xgboosted/pandas-ta-classic){:target="_blank"}).

**Also known as:** z-score, standard score, ZSCORE, normalized price.

**Args:**

- <u>period (str &#124; None, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or
yearly). Defaults to None, which uses "daily".
- <u>column (str, optional):</u> The historical data column the statistic is calculated on: "Adj Close"
for the prices (the series as given with `Econometrics(data=...)`), "Close" for the
traded prices or "Return" for the returns (the changes of the series). Defaults to "Adj Close".
- <u>window (int, optional):</u> The number of periods. Defaults to 30.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the assets.
Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame:
Z-Score values.

**Notes:**

- The method takes the `column` series of the specified `period` and calculates the Z-Score for each asset, each
over the dates it has a value. The first value needs a full window of data from the start date.
- The Z-Score agrees with pandas-ta-classic's zscore; its cdl_z applies the same score to the open, high, low
and close.
- A window of flat prices has no standard deviation and is missing, where pandas-ta-classic gives 0.
- The `standardize` parameter instead standardizes the result over the whole date range shown.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_rolling_z_score().tail(5)
```

Which returns:

| Date       |    AAPL |   MSFT |
|:-----------|--------:|-------:|
| 2025-12-24 | -0.2834 | 0.1807 |
| 2025-12-26 | -0.3665 | 0.2499 |
| 2025-12-29 | -0.2992 | 0.2546 |
| 2025-12-30 | -0.4439 | 0.4538 |
| 2025-12-31 | -0.7516 | 0.0311 |

---

## get_rolling_mean_absolute_deviation
Calculate the rolling Mean Absolute Deviation of a price series: the average distance of the prices of the window from their mean.

It measures the dispersion of the prices like the standard deviation, but without squaring the deviations, so a single large deviation weighs less. Lambert's Commodity Channel Index divides by it.

The formula is as follows:

$$
\text{Mean Absolute Deviation} = \operatorname{Mean}(\left|\operatorname{Close}(t - i) - \operatorname{SMA}(\text{Close},\; \text{window})\right|,\; i = 0,\; \ldots,\; \text{window} - 1)
$$

with the average of the window itself for every price of the window.

For more information, see the following sources:

- Lambert, D.R. (1980). "Commodity Channel Index: Tool for Trading Cyclic Trends." Commodities, October 1980.
- Referenced against TA-Lib's AVGDEV ([https://ta-lib.org/functions/avgdev.html](https://ta-lib.org/functions/avgdev.html){:target="_blank"}).
- pandas-ta-classic: mad and md ([https://github.com/xgboosted/pandas-ta-classic](https://github.com/xgboosted/pandas-ta-classic){:target="_blank"}).
- Tulip Indicators: md ([https://tulipindicators.org/md](https://tulipindicators.org/md){:target="_blank"}).

**Also known as:** AVGDEV, average deviation, mean deviation, MAD, MD.

**Args:**

- <u>period (str &#124; None, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or
yearly). Defaults to None, which uses "daily".
- <u>column (str, optional):</u> The historical data column the statistic is calculated on: "Adj Close"
for the prices (the series as given with `Econometrics(data=...)`), "Close" for the
traded prices or "Return" for the returns (the changes of the series). Defaults to "Adj Close".
- <u>window (int, optional):</u> The number of periods. Defaults to 14.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the assets.
Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame:
Mean Absolute Deviation values, in price units.

**Notes:**

- The method takes the `column` series of the specified `period` and calculates the Mean Absolute Deviation for
each asset, each over the dates it has a value. The first value needs a full window of data from the start
date.
- The deviation agrees with TA-Lib's AVGDEV, pandas-ta-classic's mad and md (whose default window is 30) and
Tulip Indicators' md.
- `toolkit.risk.get_mean_absolute_deviation` measures the daily returns within each period instead of
the prices over a rolling window.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_rolling_mean_absolute_deviation().tail(5)
```

Which returns:

| Date       |   AAPL |   MSFT |
|:-----------|-------:|-------:|
| 2025-12-24 | 2.5438 | 4.4227 |
| 2025-12-26 | 2.3046 | 4.653  |
| 2025-12-29 | 2.0477 | 4.4546 |
| 2025-12-30 | 1.8328 | 4.2249 |
| 2025-12-31 | 1.4702 | 3.8222 |

---

## get_rolling_standard_error
Calculate the rolling Standard Error of the mean of a price series: the standard deviation of the window divided by the square root of the number of periods.

It is the uncertainty of the moving average as an estimate of the mean price of the window: the moving average plus and minus two standard errors spans roughly where that mean lies.

The formula is as follows:

$$
\text{Standard Error} = \frac{\operatorname{StdDev}(\text{Close},\; \text{window})}{\sqrt{\text{window}}}
$$

with the sample standard deviation (ddof=1).

For more information, see the following sources:

- Referenced against pandas-ta-classic's stderr ([https://github.com/xgboosted/pandas-ta-classic](https://github.com/xgboosted/pandas-ta-classic){:target="_blank"}).
- Tulip Indicators: stderr ([https://tulipindicators.org/stderr](https://tulipindicators.org/stderr){:target="_blank"}).

**Also known as:** STDERR, standard error of the mean, SEM.

**Args:**

- <u>period (str &#124; None, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or
yearly). Defaults to None, which uses "daily".
- <u>column (str, optional):</u> The historical data column the statistic is calculated on: "Adj Close"
for the prices (the series as given with `Econometrics(data=...)`), "Close" for the
traded prices or "Return" for the returns (the changes of the series). Defaults to "Adj Close".
- <u>window (int, optional):</u> The number of periods. Defaults to 14.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the assets.
Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame:
Standard Error values, in price units.

**Notes:**

- The method takes the `column` series of the specified `period` and calculates the Standard Error for each
asset, each over the dates it has a value. The first value needs a full window of data from the start date.
- The standard error agrees with pandas-ta-classic's stderr. Tulip Indicators' stderr uses the population
standard deviation (ddof=0), which is sqrt((window - 1) / window) times this value.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_rolling_standard_error().tail(5)
```

Which returns:

| Date       |   AAPL |   MSFT |
|:-----------|-------:|-------:|
| 2025-12-24 | 0.7619 | 1.4639 |
| 2025-12-26 | 0.7182 | 1.4995 |
| 2025-12-29 | 0.6802 | 1.416  |
| 2025-12-30 | 0.6541 | 1.2939 |
| 2025-12-31 | 0.5702 | 1.2523 |

---

## get_rolling_entropy
Calculate the rolling Shannon Entropy of a price series: the entropy of the prices of the window taken as shares of their sum.

The entropy is at its maximum, log(window), when all prices of the window are equal, and falls as the prices spread out, so a lower entropy points to a larger move within the window. In base 2 it is measured in bits.

The formula is as follows:

$$
P(t - i) = \frac{\operatorname{Close}(t - i)}{\operatorname{Sum}(\text{Close},\; \text{window})},\;\; i = 0,\; \ldots,\; \text{window} - 1
$$

$$
\text{Entropy} = - \operatorname{Sum}(P \cdot \operatorname{log\_base}(P))
$$

For more information, see the following sources:

- Shannon, C.E. (1948). "A Mathematical Theory of Communication." Bell System Technical Journal, 27(3), 379-423.
- Referenced against pandas-ta-classic's entropy ([https://github.com/xgboosted/pandas-ta-classic](https://github.com/xgboosted/pandas-ta-classic){:target="_blank"}).

**Also known as:** ENTP, Shannon entropy, information entropy.

**Args:**

- <u>period (str &#124; None, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or
yearly). Defaults to None, which uses "daily".
- <u>column (str, optional):</u> The historical data column the statistic is calculated on: "Adj Close"
for the prices (the series as given with `Econometrics(data=...)`), "Close" for the
traded prices or "Return" for the returns (the changes of the series). Defaults to "Adj Close".
- <u>window (int, optional):</u> The number of periods. Defaults to 10.
- <u>base (float, optional):</u> The base of the logarithm. Defaults to 2.0, in bits.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the assets.
Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame:
Entropy values.

**Notes:**

- The method takes the `column` series of the specified `period` and calculates the Entropy for each asset, each
over the dates it has a value. The first value needs a full window of data from the start date.
- The entropy agrees with pandas-ta-classic's entropy.
- A window with a negative price or a sum of 0 has no entropy.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_rolling_entropy().tail(5)
```

Which returns:

| Date       |   AAPL |   MSFT |
|:-----------|-------:|-------:|
| 2025-12-24 | 3.3219 | 3.3219 |
| 2025-12-26 | 3.3219 | 3.3219 |
| 2025-12-29 | 3.3219 | 3.3219 |
| 2025-12-30 | 3.3219 | 3.3219 |
| 2025-12-31 | 3.3219 | 3.3219 |

---

## get_entropy
Calculate the Entropy of a series, by default the returns: how irregular and unpredictable it is, from the sample entropy of Richman and Moorman to the entropies of encoded returns of López de Prado.

An entropy is low for a series that repeats itself, trends or is driven by a few cycles, and high for a series that looks like noise. On daily returns, which are close to noise, most entropies sit near their maximum, so they are mainly of use to compare assets or periods with each other (e.g. with `window` for a rolling value) rather than as an absolute level.

The methods are as follows (with the default order $$m = 2$$ for the sample and approximate entropy and $$n = 3$$ for the permutation and SVD entropy):

$$
\text{Sample (Richman and Moorman, 2000):}\;\; \text{SampEn} = - \ln\left(\frac{A}{B}\right),\;\; \text{with}\;\; B \;\text{the number of pairs of templates of}\; m \;\text{values within a Chebyshev distance of}\; r = \text{tolerance} \cdot \operatorname{Std}(x) \;\text{of each other} \;(\text{a template not counted with itself}) \;\text{and}\; A \;\text{the same for}\; m + 1 \;\text{values}
$$

$$
\text{Approximate (Pincus, 1991):}\;\; \text{ApEn} = \Phi(m) - \Phi(m + 1),\;\; \Phi(m) = \operatorname{Mean}(\ln C_{i}(m)),\;\; C_{i} (m) \text{ the share of templates within } r \text{ of template } i \text{, itself included}
$$

$$
\text{Permutation (Bandt and Pompe, 2002):}\;\; H = - \operatorname{Sum}(p(\pi) \cdot \operatorname{log2}(p(\pi))) \;\text{over the ordinal patterns}\; \pi \;\text{of}\; n \;\text{values} \;\text{delay} \;\text{apart},\;\; \text{divided by log2(} n \text{!) when normalized}
$$

$$
\text{Spectral (Inouye et al., 1991):}\;\; H = - \operatorname{Sum}(p(f) \cdot \operatorname{log2}(p(f))),\;\; p \text{(} f \text{) the power spectrum (the periodogram or Welch's estimate) as shares of the total, divided by log2 of the number of frequencies when normalized}
$$

$$
\text{SVD (Roberts, Penny and Rezek, 1999):}\;\; H = - \operatorname{Sum}(s_{k} \cdot \operatorname{log2}(s_{k})),\;\; s_{k} \text{ the singular values of the delay embedding of } n \text{ values as shares of their sum, divided by log2(} n \text{) when normalized}
$$

$$
\text{Shannon:}\;\; \text{the plug-in estimate} - \frac{\operatorname{Sum}(p(w) \cdot \operatorname{log2}(p(w)))}{L} \;\text{over the words}\; w \;\text{of}\; L \;\text{symbols} \;(\text{word\_length}) \;\text{of the encoded returns},\;\; \text{in bits per symbol}
$$

- Lempel-Ziv: the number of distinct phrases of the Lempel-Ziv (1978) parsing of the encoded returns divided by their number.

$$
\text{Kontoyiannis (Kontoyiannis et al., 1998):}\;\; \operatorname{Mean}\left(\frac{\operatorname{log2}(i + 1)}{L_{i}}\right) \;\text{over the first half of the encoded returns},\;\; L_{i} \text{ one more than the longest match of the symbols from position } i \text{ with the } i \text{ symbols before it, in bits per symbol}
$$

The last three encode the returns into symbols first (`encoding`): "binary" (1 for a rise, 0 for a fall, returns of 0 left out), "quantile" (the decile of the return with bins=10) or "sigma" (the bucket of one standard deviation the return falls in).

For more information, see the following sources:

- Richman, J.S. & Moorman, J.R. (2000). "Physiological time-series analysis using approximate entropy and sample entropy." American Journal of Physiology - Heart and Circulatory Physiology, 278(6), H2039-H2049.
- Pincus, S.M. (1991). "Approximate entropy as a measure of system complexity." Proceedings of the National Academy of Sciences, 88(6), 2297-2301.
- Bandt, C. & Pompe, B. (2002). "Permutation entropy: a natural complexity measure for time series." Physical Review Letters, 88(17), 174102.
- Inouye, T. et al. (1991). "Quantification of EEG irregularity by use of the entropy of the power spectrum." Electroencephalography and Clinical Neurophysiology, 79(3), 204-210.
- Roberts, S.J., Penny, W. & Rezek, I. (1999). "Temporal and spatial complexity measures for electroencephalogram based brain-computer interfacing." Medical & Biological Engineering & Computing, 37(1), 93-98.
- Kontoyiannis, I., Algoet, P.H., Suhov, Y.M. & Wyner, A.J. (1998). "Nonparametric entropy estimation for stationary processes and random fields, with applications to English text." IEEE Transactions on Information Theory, 44(3), 1319-1327.
- López de Prado, M. (2018). "Advances in Financial Machine Learning." Wiley, chapter 18.
- Referenced against nolds' sampen ([https://github.com/CSchoel/nolds](https://github.com/CSchoel/nolds){:target="_blank"}), antropy's sample_entropy, app_entropy, perm_entropy, spectral_entropy and svd_entropy ([https://github.com/raphaelvallat/antropy](https://github.com/raphaelvallat/antropy){:target="_blank"}).

**Also known as:** SampEn, ApEn, ordinal pattern entropy, spectral entropy, SVD entropy, plug-in entropy, LZ entropy, Kontoyiannis entropy, entropy features.

**Args:**

- <u>method (str, optional):</u> The entropy, "sample", "approximate", "permutation",
"spectral", "svd", "shannon", "lempel_ziv" or "kontoyiannis". Defaults to "sample".
- <u>period (str &#124; None, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or
yearly). Defaults to None, which uses "daily".
- <u>column (str, optional):</u> The historical data column the entropy is calculated on:
"Return" for the returns (the changes of the series), "Adj Close" for the prices
(the series as given with `Econometrics(data=...)`) or "Close" for the traded
prices. Defaults to "Return".
- <u>window (int &#124; None, optional):</u> The number of periods of a rolling window. Defaults to
None, which calculates one value over the full history of every series.
- <u>order (int &#124; None, optional):</u> The template length m of the sample and approximate
entropy or the number of values n of the permutation and SVD entropy. Defaults to
None, which uses 2 for the sample and approximate and 3 for the permutation and
SVD entropy.
- <u>delay (int, optional):</u> The number of periods between the values of a pattern of the
permutation and SVD entropy. Defaults to 1.
- <u>tolerance (float, optional):</u> The tolerance r of the sample and approximate entropy
as a multiple of the standard deviation (ddof=1). Defaults to 0.2.
- <u>normalize (bool, optional):</u> Whether to divide the permutation, spectral and SVD
entropy by their maximum, so they lie between 0 and 1. Defaults to True.
- <u>estimator (str, optional):</u> The power spectrum of the spectral entropy, "periodogram"
or "welch" (segments of 256 periods with a Hann window). Defaults to "periodogram".
- <u>encoding (str, optional):</u> The encoding of the Shannon, Lempel-Ziv and Kontoyiannis
entropy, "binary", "quantile" or "sigma". Defaults to "binary".
- <u>bins (int, optional):</u> The number of quantiles of the "quantile" encoding. Defaults to 10.
- <u>word_length (int, optional):</u> The number of symbols per word of the Shannon entropy.
Defaults to 1.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the assets.
Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series &#124; pd.DataFrame:
The entropy per asset, or with `window` per date (a column per asset). The sample,
approximate and Lempel-Ziv entropies have no unit; the others are in bits (per symbol),
or between 0 and 1 when normalized.

**Notes:**

- Each asset is measured over the dates it has a value. With a window, the first value
needs a full window of data from the start date.
- The sample and approximate entropy compare every template with every other one, so
their time grows with the square of the number of observations: about 0.1 seconds for
ten years of daily returns, and about 2 seconds for a rolling window of a year over ten
years (6 seconds for a window of two years).
- The sample entropy is NaN when no two templates match (a very short series), where
nolds and antropy give infinity. The tolerance uses the sample standard deviation
(ddof=1) and includes a distance of exactly r, as in Richman and Moorman.
- The Shannon entropy counts every overlapping word, the last one included.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT", "NVDA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_entropy(method="permutation", window=252).tail(5)
```

Which returns:

| Date       |   AAPL |   MSFT |   NVDA |
|:-----------|-------:|-------:|-------:|
| 2025-12-24 | 0.9984 | 0.9911 | 0.9997 |
| 2025-12-26 | 0.998  | 0.9919 | 0.9995 |
| 2025-12-29 | 0.9982 | 0.9919 | 0.9993 |
| 2025-12-30 | 0.998  | 0.9921 | 0.9992 |
| 2025-12-31 | 0.9981 | 0.9919 | 0.9992 |

---

## get_lempel_ziv_complexity
Calculate the Lempel-Ziv Complexity of a series, by default of the direction of the returns: the number of new patterns needed to write the series down.

The returns are encoded into symbols (by default 1 for a rise and 0 for a fall) and parsed from the start into phrases, each the longest stretch that can be copied from earlier in the series plus one new symbol. A series that repeats itself needs few phrases, a random one many. Normalized, the complexity approaches 1 for independent, equally likely symbols and falls towards 0 for a regular series, so on daily returns it is mostly close to 1 and of use to compare assets or periods with each other.

The formula is as follows:

$$
c(N) = \text{the number of phrases of the Lempel-Ziv} \;(1976) \;\text{parsing of the}\; N \;\text{symbols}
$$

$$
\text{Normalized} \;c(N) = \frac{c(N) \cdot \log_{k}(N)}{N}
$$

with k the number of possible symbols: 2 for the "binary" encoding, `bins` for the "quantile" encoding and the number of distinct symbols for the "sigma" encoding.

For more information, see the following sources:

- Lempel, A. & Ziv, J. (1976). "On the complexity of finite sequences." IEEE Transactions on Information Theory, 22(1), 75-81.
- Kaspar, F. & Schuster, H.G. (1987). "Easily calculable measure for the complexity of spatiotemporal patterns." Physical Review A, 36(2), 842-848.
- López de Prado, M. (2018). "Advances in Financial Machine Learning." Wiley, chapter 18.
- Referenced against antropy's lziv_complexity ([https://github.com/raphaelvallat/antropy](https://github.com/raphaelvallat/antropy){:target="_blank"}).

**Also known as:** LZ complexity, LZ76, Lempel-Ziv-Welch complexity, LZC.

**Args:**

- <u>period (str &#124; None, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or
yearly). Defaults to None, which uses "daily".
- <u>column (str, optional):</u> The historical data column that is encoded: "Return" for the
returns (the changes of the series), "Adj Close" for the prices (the series as given
with `Econometrics(data=...)`) or "Close" for the traded prices. Defaults to "Return".
- <u>window (int &#124; None, optional):</u> The number of periods of a rolling window. Defaults to
None, which calculates one value over the full history of every series.
- <u>encoding (str, optional):</u> "binary" (1 for a positive and 0 for a negative value, values of
0 left out), "quantile" (the quantile of the value) or "sigma" (the bucket of one
standard deviation the value falls in). Defaults to "binary".
- <u>bins (int, optional):</u> The number of quantiles of the "quantile" encoding. Defaults to 10.
- <u>normalize (bool, optional):</u> Whether to normalize the number of phrases by N / log_k(N).
Defaults to True.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the assets.
Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series &#124; pd.DataFrame:
The (normalized) complexity per asset, or with `window` per date (a column per asset).

**Notes:**

- Each asset is measured over the dates it has a value. With a window, the first value
needs a full window of data from the start date.
- It equals antropy's lziv_complexity of the same symbols; antropy leaves the encoding to
the user (often above or below the median, which for returns is close to the sign).

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT", "NVDA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_lempel_ziv_complexity(window=252).tail(5)
```

Which returns:

| Date       |   AAPL |   MSFT |   NVDA |
|:-----------|-------:|-------:|-------:|
| 2025-12-24 | 1.0763 | 1.1396 | 1.1396 |
| 2025-12-26 | 1.0763 | 1.108  | 1.1396 |
| 2025-12-29 | 1.0763 | 1.108  | 1.1396 |
| 2025-12-30 | 1.0763 | 1.108  | 1.1396 |
| 2025-12-31 | 1.0763 | 1.108  | 1.1396 |

---

## get_hjorth_parameters
Calculate the Hjorth parameters of a series, by default the returns: its Activity, Mobility and Complexity, and the number of times it crosses zero.

The Activity is the variance. The Mobility, the standard deviation of the changes relative to that of the series, is a mean frequency: it is about Sqrt(2) = 1.41 for independent returns, lower when returns persist and higher when they alternate. The Complexity compares the Mobility of the changes with that of the series and grows as the series looks less like a single smooth wave. The Zero Crossings count how often the returns change sign.

The formula is as follows:

$$
\text{Activity} = \operatorname{Var}(x)
$$

$$
\text{Mobility} = \operatorname{Sqrt}\left(\frac{\operatorname{Var}(\,\mathrm{d}x)}{\operatorname{Var}(x)}\right)
$$

$$
\text{Complexity} = \frac{\operatorname{Sqrt}\left(\frac{\operatorname{Var}(\text{d2x})}{\operatorname{Var}(\,\mathrm{d}x)}\right)}{\text{Mobility}}
$$

$$
\text{Zero Crossings} = \text{the number of sign changes of}\; x,\;\; \text{values of exactly 0 skipped}
$$

with dx the first and d2x the second differences and Var the sample variance (ddof=1).

For more information, see the following sources:

- Hjorth, B. (1970). "EEG analysis based on time domain properties." Electroencephalography and Clinical Neurophysiology, 29(3), 306-310.
- Referenced against antropy's hjorth_params and num_zerocross ([https://github.com/raphaelvallat/antropy](https://github.com/raphaelvallat/antropy){:target="_blank"}).

**Also known as:** Hjorth activity, Hjorth mobility, Hjorth complexity, zero-crossing rate.

**Args:**

- <u>period (str &#124; None, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or
yearly). Defaults to None, which uses "daily".
- <u>column (str, optional):</u> The historical data column the parameters are calculated on:
"Return" for the returns (the changes of the series), "Adj Close" for the prices
(the series as given with `Econometrics(data=...)`) or "Close" for the traded
prices. Defaults to "Return".
- <u>window (int &#124; None, optional):</u> The number of periods of a rolling window. Defaults to
None, which calculates the parameters over the full history of every series.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the assets.
Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to None, which uses
the rounding of the Toolkit (4 unless set otherwise).
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame:
The Activity, Mobility, Complexity and Zero Crossings per asset (a row per asset), or
with `window` per date ((parameter, asset) columns).

**Notes:**

- Each asset is measured over the dates it has a value. With a window, the first value
needs a full window of data from the start date.
- antropy uses the population variance (ddof=0), which changes the Mobility and
Complexity by less than 0.1% for 1,000 observations, and counts a value of 0 as
positive in its zero crossings.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    tickers=["AAPL", "MSFT", "NVDA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_hjorth_parameters()
```

Which returns:

|      |   Activity |   Mobility |   Complexity |   Zero Crossings |
|:-----|-----------:|-----------:|-------------:|-----------------:|
| AAPL |     0.0003 |     1.4058 |       1.228  |              611 |
| MSFT |     0.0003 |     1.4267 |       1.2057 |              625 |
| NVDA |     0.0011 |     1.4484 |       1.2098 |              619 |

---

## get_two_sample_t_test
Calculate a two-sample t-test for a difference in mean `column` between every unordered pair of tickers in the Toolkit instance.

The test checks the null hypothesis that two samples come from distributions with the same mean, against the two-sided alternative that the means differ. Applied to returns it answers whether one asset has had a genuinely different average return than another, or whether the difference could be down to chance. By default this is Welch's t-test, which does not assume the two tickers have the same variance.

The formula is as follows:

$$
\text{Welch (the default):}\;\; t = \frac{\text{mean}_{a} - \text{mean}_{b}}{\sqrt{\frac{s_{a}^{2}}{n_{a}} + \frac{s_{b}^{2}}{n_{b}}}}
$$

$$
\text{Welch-Satterthwaite:}\;\; \text{df} = \frac{\left(\frac{s_{a}^{2}}{n_{a}} + \frac{s_{b}^{2}}{n_{b}}\right)^{2}}{\frac{\left(\frac{s_{a}^{2}}{n_{a}}\right)^{2}}{n_{a} - 1} + \frac{\left(\frac{s_{b}^{2}}{n_{b}}\right)^{2}}{n_{b} - 1}}
$$

$$
\text{Student} \;(\text{equal\_variance} = \text{True}) \;\text{:} t = \frac{\text{mean}_{a} - \text{mean}_{b}}{s_{p} \cdot \sqrt{\frac{1}{n_{a}} + \frac{1}{n_{b}}}},\;\; \text{with}\;\; s_{p}^{2} = \frac{(n_{a} - 1) \cdot s_{a}^{2} + (n_{b} - 1) \cdot s_{b}^{2}}{n_{a} + n_{b} - 2}\;\;\text{and}\;\; \text{df} = n_{a} + n_{b} - 2
$$

$$
s_{a}^{2} \;\text{and}\; s_{b}^{2} \;\text{are sample variances}(\text{ddof} = 1) \;\text{of the two tickers'} \;\text{column} \;(\text{Return by default}),\;\; \text{with a two-sided p-value}
$$

Setting `equal_variance=True` pools the two variances instead (Student's t-test), which is slightly more powerful but only valid when the variances are truly equal. Welch's version is the safer default since assets rarely share the same volatility. A low p-value (e.g. below 0.05) means the difference in means is statistically significant.

For more information about the method, see the following papers:

- Student (1908). "The Probable Error of a Mean." Biometrika, 6(1), 1-25.
- Welch, B.L. (1947). "The Generalization of 'Student's' Problem when Several Different Population Variances are Involved." Biometrika, 34(1/2), 28-35.

**Also known as:** independent samples t-test, Welch's t-test (default), Student's t-test (`equal_variance=True`).

**Args:**

- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to compare. Defaults to "Return".
- <u>equal_variance (bool, optional):</u> Whether to assume the two samples share a common
variance (Student's pooled t-test) instead of Welch's (unequal-variance) t-test.
Defaults to False.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the
tickers paired up. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.DataFrame: One row per unordered `(Ticker A, Ticker B)` pair, with the t-statistic,
degrees of freedom, its p-value, and the two sample means.

**Notes:**

- The two return series are compared as independent samples (not paired by date), which is
the standard use of a two-sample t-test -- if a date-by-date, paired comparison is needed
instead, take the difference of the two return series and run a one-sample test on it.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["MSFT", "ORCL", "SAP"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_two_sample_t_test()
```

Which returns:

|                  |   T-Statistic |   Degrees of Freedom |   P-Value |   Mean A |   Mean B |
|:-----------------|--------------:|---------------------:|----------:|---------:|---------:|
| ('MSFT', 'ORCL') |       -0.528  |              2176.24 |    0.5975 |   0.0008 |   0.0012 |
| ('MSFT', 'SAP')  |        0.1389 |              2504.05 |    0.8895 |   0.0008 |   0.0007 |
| ('ORCL', 'SAP')  |        0.6326 |              2210.92 |    0.5271 |   0.0012 |   0.0007 |

---

## get_f_test
Calculate a nested-model F-test for the joint significance of the regressors in `unrestricted_independent_tickers` that are not already in `restricted_independent_tickers`.

Two OLS regressions of `dependent_ticker` are fitted internally: a "restricted" one on `restricted_independent_tickers` and an "unrestricted" one that adds the extra tickers. The test checks the null hypothesis that the `q` extra tickers are jointly zero, i.e. that adding them does not explain the dependent ticker any better, by comparing how much the Residual Sum of Squares (RSS) drops when they are added.

The formula is as follows:

$$
F = \frac{\frac{\text{RSS}_{\text{restricted}} - \text{RSS}_{\text{unrestricted}}}{q}}{\frac{\text{RSS}_{\text{unrestricted}}}{n - k_{\text{unrestricted}}}}
$$

- Both models are OLS regressions of the dependent ticker's `column` (Return by default), with a constant when add_constant=True

Where `q = k_unrestricted - k_restricted` is the number of added regressors, `n` the number of observations and `k_unrestricted` the number of parameters of the larger model. Under the null, `F` follows an F(q, n - k_unrestricted) distribution. A low p-value means the extra tickers meaningfully improve the fit as a group, even when none of them is significant individually. `get_likelihood_ratio_test` is the asymptotic Maximum Likelihood counterpart.

**Also known as:** nested F-test, restricted vs. unrestricted F-test, partial F-test.

**Args:**

- <u>dependent_ticker (str):</u> The dependent (predicted) asset.
- <u>restricted_independent_tickers (str &#124; list[str]):</u> The independent asset(s) in the
restricted (smaller) model.
- <u>unrestricted_independent_tickers (str &#124; list[str]):</u> The independent asset(s) in the
unrestricted (larger) model -- must be a superset of `restricted_independent_tickers`.
- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>column (str, optional):</u> The historical data column to regress on. Defaults to "Return".
- <u>add_constant (bool, optional):</u> Whether to include an intercept in both models. Defaults
to True.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series: The F-statistic, its numerator/denominator degrees of freedom, its p-value,
and whether the added regressors are jointly significant at the 5% level.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_f_test(
    "AAPL", "MSFT", ["MSFT", "Benchmark"], period="weekly"
)
```

Which returns:

|                          |       0 |
|:-------------------------|--------:|
| F-Statistic              | 104.748 |
| Df Numerator             |   1     |
| Df Denominator           | 257     |
| P-Value                  |   0     |
| Reject Restrictions (5%) |   1     |

---

## get_likelihood_ratio_test
Calculate a nested-model Likelihood Ratio (LR) test, the Maximum Likelihood analogue of `get_f_test`, for the joint significance of the regressors in `unrestricted_independent_tickers` that are not already in `restricted_independent_tickers`.

As with `get_f_test`, a "restricted" and an "unrestricted" OLS regression of `dependent_ticker` are fitted internally and the null hypothesis is that the `q` extra tickers are jointly zero. Instead of an F-statistic, the two models are compared through the ratio of their likelihoods, which for linear models with normal errors reduces to a function of the two Residual Sums of Squares (RSS).

The formula is as follows:

$$
\text{LR} = - 2 \cdot (\ln L_{\text{restricted}} - \ln L_{\text{unrestricted}}) = n \cdot \ln\left(\frac{\text{RSS}_{\text{restricted}}}{\text{RSS}_{\text{unrestricted}}}\right)
$$

- Both models are OLS regressions of the dependent ticker's `column` (Return by default), with a constant when add_constant=True

Under the null this is asymptotically chi-squared distributed with `q` degrees of freedom. Where the F-test is exact in small samples under the classical assumptions, the LR test relies on a large-sample approximation: both agree for long return histories and can differ somewhat for short ones. A low p-value means the extra tickers meaningfully improve the model.

For more information about the method, see the following paper:

- Wilks, S.S. (1938). "The Large-Sample Distribution of the Likelihood Ratio for Testing Composite Hypotheses." Annals of Mathematical Statistics, 9(1), 60-62.

**Also known as:** LR test, Wilks' likelihood ratio test.

**Args:**

- <u>dependent_ticker (str):</u> The dependent (predicted) asset.
- <u>restricted_independent_tickers (str &#124; list[str]):</u> The independent asset(s) in the
restricted (smaller) model.
- <u>unrestricted_independent_tickers (str &#124; list[str]):</u> The independent asset(s) in the
unrestricted (larger) model -- must be a superset of `restricted_independent_tickers`.
- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>column (str, optional):</u> The historical data column to regress on. Defaults to "Return".
- <u>add_constant (bool, optional):</u> Whether to include an intercept in both models. Defaults
to True.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series: The LR statistic, its degrees of freedom, its p-value, and whether the added
regressors are jointly significant at the 5% level.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_likelihood_ratio_test(
    "AAPL", "MSFT", ["MSFT", "Benchmark"], period="weekly"
)
```

Which returns:

|                          |       0 |
|:-------------------------|--------:|
| LR Statistic             | 88.8863 |
| Degrees of Freedom       |  1      |
| P-Value                  |  0      |
| Reject Restrictions (5%) |  1      |

---

## get_wald_test
Calculate a Wald test of `q` general linear restriction(s) on the coefficients of an OLS regression of `dependent_ticker` on `independent_tickers`.

A single OLS regression is fitted internally and the test checks the null hypothesis `H0: R @ beta = r`, where `R` (`restriction_matrix`) encodes `q` linear restrictions on the coefficients and `r` (`restriction_values`) holds their hypothesised values (zero by default). This generalises the t-test reported for each coefficient to combinations of coefficients, for example that two coefficients are jointly zero, that a coefficient equals a specific value (such as a beta of exactly 1), or that two tickers have the same coefficient.

The formula is as follows:

$$
W = (R \, \hat{\beta} - r)' \, (R \, \operatorname{Cov}(\hat{\beta}) \, R')^{-1} \, (R \, \hat{\beta} - r)
$$

$$
F = \frac{W}{q},\;\; \text{F-distributed with} \;(q,\; n - k) \;\text{degrees of freedom}
$$

$$
\hat{\beta} \;\text{and the classical Cov}(\hat{\beta}) = \hat{\sigma}^{2} \cdot (X' X)^{- 1} \;\text{come from the OLS regression of the dependent ticker's} \;\text{column} \;(\text{Return by default}),\;\; \text{with a constant when add\_constant=True}
$$

Which is asymptotically chi-squared distributed with `q` degrees of freedom. `W / q` is reported alongside it as an F-statistic for small samples; for a single restriction it equals the squared t-statistic of that coefficient. A low p-value means the data reject the restriction(s).

For more information about the method, see the following paper:

- Wald, A. (1943). "Tests of Statistical Hypotheses Concerning Several Parameters When the Number of Observations is Large." Transactions of the American Mathematical Society, 54(3), 426-482.

**Also known as:** Wald chi-squared test.

**Args:**

- <u>restriction_matrix (pd.DataFrame &#124; np.ndarray &#124; list[list[float]]):</u> The `(q, k)`
restriction matrix `R`, one row per restriction, one column per coefficient in the
same order as `add_constant` (if True, "Intercept" first) followed by the
independent ticker(s), e.g. [[0, 1, 0], [0, 0, 1]].
- <u>dependent_ticker (str &#124; None, optional):</u> The dependent (predicted) asset.
Defaults to None, meaning the Toolkit instance's first ticker.
- <u>independent_tickers (str &#124; list[str] &#124; None, optional):</u> The independent
(predictor) asset(s), in the order the restriction matrix's columns
(after "Intercept", if `add_constant`) refer to them. Defaults to None,
meaning every other ticker in the Toolkit instance besides
`dependent_ticker`.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" in the
default independent ticker(s) (has no effect when independent_tickers is given
explicitly). Defaults to False.
- <u>restriction_values (pd.Series &#124; np.ndarray &#124; list[float] &#124; None, optional):</u> The
length-`q` vector of hypothesized values. Defaults to None, i.e. all restrictions
equal zero.
- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>column (str, optional):</u> The historical data column to regress on. Defaults to "Return".
- <u>add_constant (bool, optional):</u> Whether to include an intercept. Defaults to True.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series: The Wald (chi-squared) statistic and its p-value, the small-sample F-statistic
and its p-value, the number of restrictions, and whether they are rejected at the 5% level.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["AAPL", "MSFT"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

# H0: the coefficients on both MSFT and Benchmark are jointly zero.
toolkit.econometrics.get_wald_test(
    restriction_matrix=[[0, 1, 0], [0, 0, 1]],
    independent_tickers=["MSFT", "Benchmark"],
    period="weekly",
)
```

Which returns:

|                          |       0 |
|:-------------------------|--------:|
| Wald Statistic (Chi2)    | 269.191 |
| Chi2 P-Value             |   0     |
| F-Statistic              | 134.595 |
| F P-Value                |   0     |
| Restrictions (q)         |   2     |
| Reject Restrictions (5%) |   1     |

---

## get_hausman_wu_test
Calculate a regression-based Hausman-Wu test for the endogeneity of `suspect_ticker` in a regression of `dependent_ticker` on `suspect_ticker` (and, optionally, `other_independent_tickers`), using `instrument_tickers` as instruments for `suspect_ticker`.

OLS requires every regressor to be uncorrelated with the error term. When that fails, for example because of an omitted common driver, reverse causality or measurement error, the regressor is "endogenous" and OLS is biased; an instrumental-variables approach such as `get_iv_2sls` is then needed. This test checks whether that is the case before committing to a full IV fit, using two auxiliary OLS regressions:

1. Regress `suspect_ticker` on the instruments (and the other tickers, if given) and keep the residuals: the part of `suspect_ticker` that the instruments do not explain.
2. Regress `dependent_ticker` on `suspect_ticker`, those residuals (and the other tickers) and test whether the coefficient on the residuals is zero.

If `suspect_ticker` is exogenous the residuals add no information, so their coefficient should be statistically zero. A low p-value is evidence that `suspect_ticker` is endogenous and that the OLS estimate is unreliable. The test is only as good as the instruments: they must be correlated with `suspect_ticker` but not with the error term.

The formula is as follows:

$$
\text{Stage 1:}\;\; X_{t} = \pi_{0} + \pi' Z_{t} + \delta' W_{t} + v_{t},\;\; \text{the OLS regression of suspect\_ticker (} X \text{) on a constant, the instruments (} Z \text{) and other\_independent\_tickers (} W \text{), keeping the residuals } \hat{v}_{t}
$$

$$
\text{Stage 2:}\;\; y_{t} = \beta_{0} + \beta_{1} \cdot X_{t} + \rho \cdot \hat{v}_{t} + \gamma' W_{t} + \epsilon_{t},\;\; \text{the OLS regression of dependent\_ticker (} y \text{)}
$$

$$
t = \frac{\hat{\rho}}{\operatorname{SE}(\hat{\rho})},\;\; \text{with the classical OLS standard error and a Student-t distribution with}\; n - k \;\text{degrees of freedom};\;\; \text{endogeneity is flagged when the p-value is below 0.05}
$$

- All variables are the tickers' `column` (Return by default)

For more information about the method, see the following papers:

- Wu, D-M. (1973). "Alternative Tests of Independence Between Stochastic Regressors and Disturbances." Econometrica, 41(4), 733-750.
- Hausman, J.A. (1978). "Specification Tests in Econometrics." Econometrica, 46(6), 1251-1271.

**Also known as:** Hausman test, Durbin-Wu-Hausman test, regression test for endogeneity.

**Args:**

- <u>dependent_ticker (str):</u> The dependent (predicted) asset.
- <u>suspect_ticker (str):</u> The (possibly endogenous) asset being tested.
- <u>instrument_tickers (str &#124; list[str]):</u> One or more instrument asset(s) for
`suspect_ticker` -- assets correlated with `suspect_ticker` but assumed uncorrelated
with `dependent_ticker`'s error term.
- <u>other_independent_tickers (str &#124; list[str] &#124; None, optional):</u> Any other (assumed
exogenous) independent asset(s) to include. Defaults to None.
- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to regress on. Defaults to "Return".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series: The coefficient on the first-stage residuals, its t-statistic and p-value, and
whether `suspect_ticker` is flagged as endogenous at the 5% level.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["SMCI", "NVDA", "TSM"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_hausman_wu_test(
    dependent_ticker="SMCI", suspect_ticker="NVDA", instrument_tickers="TSM"
)
```

Which returns:

|                    |    Value |
|:-------------------|---------:|
| V-Hat Coefficient  |  -0.4021 |
| T-Statistic        |  -2.3377 |
| Degrees of Freedom | 246      |
| P-Value            |   0.0202 |
| Endogenous (5%)    |   1      |

---

## get_heteroskedasticity_test
Calculate a test for heteroskedasticity of a regression of `dependent_ticker` on `independent_tickers`, the Breusch-Pagan test (method="breusch_pagan") or White's test (method="white").

OLS standard errors assume that the residual variance is constant (homoskedasticity). Both tests regress the squared residuals of the regression on functions of the independent tickers and check whether they explain any of the residual variance, by testing whether the R-squared of that auxiliary regression is significantly different from zero. The Breusch-Pagan test uses only the original independent tickers. White's test is the more general version: its auxiliary regression uses each ticker, its square and every pairwise cross-product, so it also catches non-linear forms of heteroskedasticity.

The formula for method="breusch_pagan" is as follows:

$$
\text{Auxiliary regression:}\;\; e_{t}^{2} = a_{0} + a' \cdot x_{t} + v_{t},\;\; \text{with } e_{t} \text{ the OLS residuals and } x_{t} \text{ the independent tickers' column (Return by default)}
$$

$$
\text{LM} = n \cdot R^{2}_{\text{auxiliary}} \;(\text{Koenker's studentized form},\; \text{the statsmodels default})
$$

The formula for method="white" is as follows:

$$
e_{t}^{2} = a_{0} + \sum_{i}(a_{i} \cdot x_{it}) + \sum_{i}(b_{i} \cdot x_{it}^{2}) + \sum_{i<j}(c_{ij} \cdot x_{it} \cdot x_{jt}) + v_{t}
$$

$$
\text{LM} = n \cdot R^{2}_{\text{auxiliary}},\;\; \text{chi-squared with as many degrees of freedom as the auxiliary regression has terms besides } a_{0}
$$

- $$e_{t}$$ are the OLS residuals and $$x_{it}$$ the independent tickers' `column` (Return by default)

The Breusch-Pagan statistic is the studentized statistic of Koenker (1981), which does not assume normally distributed errors. It is asymptotically chi-squared distributed with `k - 1` degrees of freedom under the null hypothesis of homoskedasticity, where `k` is the number of parameters of the auxiliary regression. For both tests a low p-value means the residual variance moves with the independent tickers (for example, errors grow when the market moves more), so the regression's standard errors, t-statistics and p-values are unreliable even though the coefficients themselves remain unbiased. Remedies are a robust `cov_type` in `get_ols` or `get_wls`. Because it also detects non-linear patterns in the residual variance, White's test makes fewer assumptions than Breusch-Pagan, at the cost of power when there are many independent tickers, since the number of auxiliary terms grows quadratically.

For more information about the method, see the following papers:

- Breusch, T.S., & Pagan, A.R. (1979). "A Simple Test for Heteroscedasticity and Random Coefficient Variation." Econometrica, 47(5), 1287-1294.
- Koenker, R. (1981). "A Note on Studentizing a Test for Heteroscedasticity." Journal of Econometrics, 17(1), 107-112.
- White, H. (1980). "A Heteroskedasticity-Consistent Covariance Matrix Estimator and a Direct Test for Heteroskedasticity." Econometrica, 48(4), 817-838.

**Also known as:** BP test, Breusch-Pagan test, Breusch-Pagan-Godfrey test, White test, White's general test, heteroscedasticity test.

**Args:**

- <u>dependent_ticker (str &#124; None, optional):</u> The dependent (predicted) asset.
Defaults to None, meaning the Toolkit instance's first ticker.
- <u>independent_tickers (str &#124; list[str] &#124; None, optional):</u> The independent
(predictor) asset(s). Defaults to None, meaning every other ticker in
the Toolkit instance besides `dependent_ticker`.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" in the
default independent ticker(s) (has no effect when independent_tickers is given
explicitly). Defaults to False.
- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>column (str, optional):</u> The historical data column to regress on. Defaults to "Return".
- <u>add_constant (bool, optional):</u> Whether to include an intercept in the underlying
regression. Defaults to True.
- <u>method (str, optional):</u> The test, "breusch_pagan" for the Breusch-Pagan test (Koenker's
studentized form) or "white" for White's test. Defaults to "breusch_pagan".
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series: The LM statistic ("Breusch-Pagan Statistic" or "White Statistic"), its p-value,
and whether homoskedasticity is rejected at the 5% level.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["CAT", "DE"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

# CAT (the first ticker) is dependent; DE is independent
toolkit.econometrics.get_heteroskedasticity_test()
```

Which returns:

|                              |   Value |
|:-----------------------------|--------:|
| Breusch-Pagan Statistic      |  0.0129 |
| P-Value                      |  0.9096 |
| Reject Homoskedasticity (5%) |  0      |

---

## get_durbin_watson_test
Calculate the Durbin-Watson statistic for first-order autocorrelation in the residuals of a regression of `dependent_ticker` on `independent_tickers`.

OLS standard errors assume that the residuals of consecutive periods are uncorrelated. The Durbin-Watson statistic compares each residual with the one before it.

The formula is as follows:

$$
\text{DW} = \frac{\sum_{t=2}^{n}((e_{t} - e_{t-1})^{2})}{\sum_{t=1}^{n}(e_{t}^{2})}
$$

- $$e_{t}$$ are the residuals of the OLS regression of the dependent ticker's `column` (Return by default) on the independent tickers' `column`

- Interpretation: $$\text{DW} < 1.5$$ positive autocorrelation likely, $$\text{DW} > 2.5$$ negative autocorrelation likely, otherwise no strong evidence

The statistic ranges from 0 to 4. A value near 2 means no first-order autocorrelation; values below 2 point to positive autocorrelation (consecutive residuals tend to share the same sign, often a sign of an omitted trend or lagged effect) and values above 2 to negative autocorrelation (residuals tend to alternate in sign). Like heteroskedasticity, autocorrelation leaves the coefficients unbiased but makes the standard errors unreliable; a "HAC" `cov_type` in `get_ols`, or `get_gls` with an AR(1) `omega`, are common remedies. There is no exact p-value: the returned interpretation is a rule of thumb (below 1.5 is likely positive, above 2.5 likely negative autocorrelation).

For more information about the method, see the following paper:

- Durbin, J., & Watson, G.S. (1950). "Testing for Serial Correlation in Least Squares Regression I." Biometrika, 37(3/4), 409-428.

**Also known as:** DW statistic.

**Args:**

- <u>dependent_ticker (str &#124; None, optional):</u> The dependent (predicted) asset.
Defaults to None, meaning the Toolkit instance's first ticker.
- <u>independent_tickers (str &#124; list[str] &#124; None, optional):</u> The independent
(predictor) asset(s). Defaults to None, meaning every other ticker in
the Toolkit instance besides `dependent_ticker`.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" in the
default independent ticker(s) (has no effect when independent_tickers is given
explicitly). Defaults to False.
- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>column (str, optional):</u> The historical data column to regress on. Defaults to "Return".
- <u>add_constant (bool, optional):</u> Whether to include an intercept in the underlying
regression. Defaults to True.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series: The Durbin-Watson statistic and an approximate interpretation flag.

**Notes:**

- Unlike the other tests in this module, this does not carry a formal p-value/reject flag at a
stated significance level -- see `specification_tests_model.get_durbin_watson_test` for why.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["HD", "LOW"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

# HD (the first ticker) is dependent; LOW is independent
toolkit.econometrics.get_durbin_watson_test()
```

Which returns:

|                         | Value              |
|:------------------------|:-------------------|
| Durbin-Watson Statistic | 1.8584             |
| Interpretation          | No Strong Evidence |

---

## get_vif
Calculate the Variance Inflation Factor (VIF) of every ticker in the Toolkit instance, treated as regressors against one another.

Multicollinearity, where one regressor can (nearly) be predicted from the others, does not bias regression coefficients but inflates their standard errors. Individual coefficients can then look insignificant, and swing wildly between samples, even when the regressors jointly explain the dependent variable well. VIF measures this for each ticker by regressing it on all the other tickers.

The formula is as follows:

$$
\text{VIF}_{i} = \frac{1}{1 - R^{2}_{i}}
$$

$$
R^{2}_{i} \;\text{is the R-squared of the OLS regression of ticker i's} \;\text{column} \;(\text{Return by default}) \;\text{on a constant and every other ticker's} \;\text{column}
$$

Where `R^2_i` is the R-squared of regressing ticker `i` on all other tickers. A VIF of 1 means the ticker is uncorrelated with the others; a VIF of `V` means the variance of its coefficient is `V` times larger than it would be without multicollinearity. As a rule of thumb, a VIF above 10 (or above 5 for a stricter cutoff) signals problematic multicollinearity. This is common with assets that move closely together, such as several stocks from the same sector, and is worth checking before using them together as independent tickers in `get_ols` or the other regression methods.

**Also known as:** VIF.

**Args:**

- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to use. Defaults to "Return".
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" among the
regressors tested. Defaults to False.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series: The VIF of each asset, indexed by ticker.

**Notes:**

- Unlike the other methods in this module, `get_vif` has no `dependent_ticker` -- VIF is a
property of the regressors alone, independent of any particular dependent variable.
- `VIF > 10` is the conventional rule-of-thumb threshold for concerning multicollinearity.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["GOOGL", "META", "AMZN"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

toolkit.econometrics.get_vif()
```

Which returns:

|       |    VIF |
|:------|-------:|
| GOOGL | 1.4431 |
| META  | 1.8234 |
| AMZN  | 2.0804 |

---

## get_ramsey_reset_test
Calculate Ramsey's RESET test for functional form misspecification of a regression of `dependent_ticker` on `independent_tickers`.

If the true relationship is non-linear, or a relevant transformation or variable is missing, the fitted values of a linear regression still carry information about that missing piece. RESET tests for this by adding powers of the fitted values (`fitted^2`, ..., `fitted^power`) to the regression and checking whether they are jointly significant with an F-test that compares the original (restricted) and augmented (unrestricted) model.

The formula is as follows:

$$
\text{Augmented model:}\;\; y_{t} = x_{t}' \cdot \beta + \sum_{j=2}^{\text{power}}(\gamma_{j} \cdot \hat{y}_{t}^{j}) + u_{t},\;\; \text{with}\;\; \hat{y}_{t} \;\text{the fitted values of the original OLS regression and} \;\text{power} = 3 \;\text{by default}
$$

$$
F = \frac{\frac{\text{RSS}_{r} - \text{RSS}_{u}}{q}}{\frac{\text{RSS}_{u}}{n - k_{u}}}
$$

Where `RSS_r` and `RSS_u` are the residual sums of squares of both models, `q` is the number of added terms (`power - 1`), `n` the number of observations and `k_u` the number of parameters of the augmented model. Under the null hypothesis that the linear form is correct, `F` follows an $$F (q , n - k_{u})$$ distribution. A low p-value suggests the model is missing something, for example a squared or interaction term or a log transformation, without saying what; it is a signal to reconsider the specification, not a prescription.

For more information about the method, see the following paper:

- Ramsey, J.B. (1969). "Tests for Specification Errors in Classical Linear Least-Squares Regression Analysis." Journal of the Royal Statistical Society, Series B, 31(2), 350-371.

**Also known as:** RESET test, Ramsey RESET.

**Args:**

- <u>dependent_ticker (str &#124; None, optional):</u> The dependent (predicted) asset.
Defaults to None, meaning the Toolkit instance's first ticker.
- <u>independent_tickers (str &#124; list[str] &#124; None, optional):</u> The independent
(predictor) asset(s). Defaults to None, meaning every other ticker in
the Toolkit instance besides `dependent_ticker`.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" in the
default independent ticker(s) (has no effect when independent_tickers is given
explicitly). Defaults to False.
- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly).
Defaults to "daily".
- <u>column (str, optional):</u> The historical data column to regress on. Defaults to "Return".
- <u>add_constant (bool, optional):</u> Whether to include an intercept in the underlying
regression. Defaults to True.
- <u>power (int, optional):</u> The highest power of the fitted values to add. Defaults to 3.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series: The RESET F-statistic, its p-value, and whether correct specification is
rejected at the 5% level.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["NKE", "ADS.DE"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2025-01-01",
    end_date="2025-12-31",
)

# NKE (the first ticker) is dependent; ADS.DE is independent
toolkit.econometrics.get_ramsey_reset_test()
```

Which returns:

|                                   |   Value |
|:----------------------------------|--------:|
| RESET F-Statistic                 |  1.4847 |
| P-Value                           |  0.2285 |
| Reject Correct Specification (5%) |  0      |

---

## get_chow_test
Calculate the Chow test for a structural break at `break_date` in a regression of `dependent_ticker` on `independent_tickers`.

The sample is split at `break_date` into a "before" and "after" period, a regression is fitted on each part separately and on the full sample, and an F-test checks whether allowing the coefficients to differ between the two periods significantly reduces the residual sum of squares.

The formula is as follows:

$$
F = \frac{\frac{\text{RSS}_{\text{pooled}} - (\text{RSS}_{1} + \text{RSS}_{2})}{k}}{\frac{\text{RSS}_{1} + \text{RSS}_{2}}{n - 2k}}
$$

- The second sub-period starts at the first period that ends on or after `break_date` (the date itself with daily data, the month that contains it with period="monthly"), and `k` includes the constant when add_constant=True

Where `RSS_pooled` is the residual sum of squares of the full-sample regression, `RSS_1` and `RSS_2` those of the two sub-periods, `k` the number of parameters and `n` the total number of observations. Under the null hypothesis of no structural break (the same coefficients apply throughout), `F` follows an F(k, n - 2k) distribution. A low p-value means the relationship changed at `break_date`, for example an asset's beta shifting after a merger, a regulatory change or a market regime change, so a single regression over the full sample is misspecified. The break date must be chosen in advance; testing many candidate dates and keeping the most significant overstates the evidence.

For more information about the method, see the following paper:

- Chow, G.C. (1960). "Tests of Equality Between Sets of Coefficients in Two Linear Regressions." Econometrica, 28(3), 591-605.

**Also known as:** Chow breakpoint test.

**Args:**

- <u>break_date (str):</u> The date (e.g. "2021-06-30") at which to split the sample -- all
periods ending on or after this date, the period that contains it included, form
the "after" sub-sample, everything before it forms the "before" sub-sample.
- <u>dependent_ticker (str &#124; None, optional):</u> The dependent (predicted) asset.
Defaults to None, meaning the Toolkit instance's first ticker.
- <u>independent_tickers (str &#124; list[str] &#124; None, optional):</u> The independent
(predictor) asset(s). Defaults to None, meaning every other ticker in
the Toolkit instance besides `dependent_ticker`.
- <u>include_benchmark (bool, optional):</u> Whether to include "Benchmark" in the
default independent ticker(s) (has no effect when independent_tickers is given
explicitly). Defaults to False.
- <u>period (str, optional):</u> The data frequency (daily, weekly, monthly, quarterly, or yearly). Defaults to
"daily".
- <u>column (str, optional):</u> The historical data column to regress on. Defaults to "Return".
- <u>add_constant (bool, optional):</u> Whether to include an intercept in the underlying
regression(s). Defaults to True.
- <u>rounding (int &#124; None, optional):</u> The number of decimals to round the results to. Defaults to
None.
- <u>show_columns (str &#124; list[str] &#124; None):</u> The columns to keep, a name or a list of names, matched
on every column level, or the rows when no column has those names (such as the line
items of a financial statement). Names that do not exist are logged, and when none
exist the result is returned in full. Defaults to None, which keeps every column.

**Returns:**

pd.Series: The Chow F-statistic, its p-value, and whether no structural break is rejected
at the 5% level.

**Raises:**

ValueError: If `break_date` does not leave enough observations on either side of the
split to estimate the regression's parameters.

**As an example:**

```python
from financetoolkit import Toolkit

toolkit = Toolkit(
    ["NVDA"],
    api_key="FINANCIAL_MODELING_PREP_KEY",
    start_date="2021-01-01",
    end_date="2025-12-31",
)

# NVDA is dependent and the Benchmark independent, with a break at the launch of ChatGPT
toolkit.econometrics.get_chow_test(break_date="2022-11-30", include_benchmark=True)
```

Which returns:

|                                 |   Value |
|:--------------------------------|--------:|
| Chow F-Statistic                |  0.8161 |
| P-Value                         |  0.4424 |
| Reject No Structural Break (5%) |  0      |

---

