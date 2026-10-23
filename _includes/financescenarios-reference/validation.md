## Reference

The reference is generated from the docstrings in the package, so it says what `help(...)` says in Python: what each class and function does, a worked example with real output where the docstring has one, and the arguments and return value folded underneath.

Everything on this page imports as follows:

```python
from financescenarios import Relationships, RelationshipRegion, Realism, RealismFactor, OutOfSample, OutOfSampleEvaluation
from financescenarios.validation.naic_goes.naic_goes_controller import NaicGoes
from financescenarios.validation.dnb.dnb_controller import Dnb
from financescenarios.validation.published_frameworks.published_frameworks_controller import compare_published
from financescenarios.validation.published_frameworks.published_frameworks_controller import held_up
```

### Relationships

Checks that a run respects the economic patterns a validator expects from scenarios: central banks raise rates
when inflation rises and cut them when unemployment rises, inflation falls when unemployment rises, the long rate
follows the short rate, an inverted curve comes before a downturn, stocks lose in real terms in high-inflation
years, and so on. None of these is fitted directly: the calibration fits each factor on its own history and links
them through correlated shocks and a few built-in drifts, so whether the scenarios reproduce them is a property
of the whole model, worth measuring before the scenarios drive an asset-liability study or a stress test.

Every relationship is measured identically on history and on each scenario: the same year-end observations (so a
year-over-year inflation rate is never differenced month to month), the same transformation (yearly changes,
the next year's change, a bucket or a band) and the same statistic (a regression slope, a correlation or a
difference of averages). History is one long path, from the 1950s for the OECD series and from 1871 for
Shiller's US stock market data; each scenario is one possible path. The table gives the historical value with
its data and years, the median and 5-95% range across scenarios, and a grade: "fail" when the median scenario
has the opposite direction to history, "warn" when the direction is right but the size is more than a factor of
two off, "pass" otherwise. Where history is itself inconclusive (within two standard errors of zero, Newey and West's
(1987) error, as yearly levels persist and two-year changes overlap) the median only has to fall within that
interval. A five-year run has five yearly observations per scenario, so its range is
wide; simulate 30 years or more for a sharper reading.

| Relationship | Statistic | Source of the expectation |
|:-------------|:----------|:--------------------------|
| Policy rate reacts to inflation, unemployment | slopes of yearly rate changes | Taylor (1993), Federal Reserve |
| Rates near neutral at target, higher above it | mean rate, above vs at target | Taylor (1993), the 2% targets |
| Phillips curve | slope of yearly changes | Phillips (1958) |
| Bear markets with rising unemployment | correlation | the business cycle |
| Long rate moves with the short rate | slope of yearly changes | Campbell and Shiller (1991) |
| Inverted curve precedes higher unemployment | slope on the curve | Estrella and Hardouvelis (1991) |
| Real equity returns by inflation level | mean real return, above 5% vs below 3% | Fama and Schwert (1977) |
| Higher rates slow house prices | slope, one year later | Iacoviello (2005) |
| Oil prices pass into inflation | slope of yearly changes | Hooker (2002) |
| Rate differential and the currency | slope, one year later | Fama (1984) |
| Credit spreads widen with unemployment | slope of yearly changes | Gilchrist and Zakrajšek (2012) |

**As an example:**

```python
from financescenarios import Scenarios

scenarios = Scenarios.from_profiles(settings="default", factor_set="default")
result = scenarios.simulate(n_simulations=2000, years=30)
scenarios.check_relationships(result)
```

**References:**

- Taylor, J.B. (1993). "Discretion versus policy rules in practice." Carnegie-Rochester Conference Series on Public Policy, 39, 195-214; the rule is eq. 1 on p. 202. <https://doi.org/10.1016/0167-2231(93>)90009-L
- Board of Governors of the Federal Reserve System (2026). "Monetary Policy Report", July 2026, Part 2, Box 4, Monetary Policy Rules in the Current Environment, Table A, p. 43: the rules written with the unemployment gap. <https://www.federalreserve.gov/monetarypolicy/files/20260710_mprfullreport.pdf>
- FOMC (2026). "Statement on Longer-Run Goals and Monetary Policy Strategy", paragraph 4: 2% PCE inflation. <https://www.federalreserve.gov/monetarypolicy/files/FOMC_LongerRunGoals.pdf>
- ECB (2021). "The ECB's monetary policy strategy statement", paragraph 5: 2% over the medium term, symmetric. <https://www.ecb.europa.eu/mopo/strategy/strategy-review/ecb.strategyreview_monpol_strategy_statement.en.html>
- Shiller, R.J. U.S. stock market data since 1871. <https://shillerdata.com/>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
Relationships(economics: Economics | None = None)
```

**Args:**

- <u>economics (Economics &#124; None):</u> a Finance Toolkit `Economics` instance whose window starts in 1871 or earlier; built on first use when omitted. No API key is needed.

</details>

#### Relationships.economics

The Finance Toolkit `Economics` the long history comes from, reaching back to 1850.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
relationships.economics  # property -> Economics
```

</details>

#### Relationships.check

Measure every relationship on history and on the run, and grade it.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
check(
    result: ScenarioSet,
    config: ScenariosConfig,
    history: list[HistoricalSeries] | None = None,
    regions: list[RelationshipRegion] | None = None,
) -> pl.DataFrame
```

**Args:**

- <u>result (ScenarioSet):</u> the run; its step must divide a year (monthly, quarterly or yearly).
- <u>config (ScenariosConfig):</u> the configuration it was simulated from, which says which factor is which.
- <u>history (list[HistoricalSeries] &#124; None):</u> the factors' own histories, used for parts without a long OECD or Shiller series (the oil price, a credit spread, a non-US equity); None leaves those out.
- <u>regions (list[RelationshipRegion] &#124; None):</u> the economies to check; None builds one per currency of the configured short rates (`default_regions`).

**Returns:**

<u>pl.DataFrame:</u> one row per relationship and economy: "relationship", "region", "status", "history", "simulated_median", "simulated_p5", "simulated_p95", "simulated_pooled", "scenarios", "unit", "expected", "measure", "history_source", "history_error" and "detail".

**Raises:**

- <u>ValueError:</u> if the run's step does not divide a year.

</details>

#### Relationships.history

The year-end history of every part an economy has in the run: the OECD series of the country each part
stands for, Shiller's US data for a US equity, and a factor's own history otherwise.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
history(
    region: RelationshipRegion,
    roles: dict[str, str],
    own_history: dict[str, HistoricalSeries],
) -> YearlySample
```

**Args:**

- <u>region (RelationshipRegion):</u> the economy.
- <u>roles (dict[str, str]):</u> part -> simulated factor name, the parts the run holds.
- <u>own_history (dict[str, HistoricalSeries]):</u> factor name -> its own history.

**Returns:**

<u>YearlySample:</u> one row of year-end values per part.

</details>

#### Relationships.shiller

Shiller's monthly US stock market data since 1871 (prices, dividends, earnings, the consumer price index and
the real total-return price), fetched once per instance; None when it cannot be read.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
shiller() -> pd.DataFrame | None
```

</details>

### RelationshipRegion

One economy whose relationships are checked: which simulated factor plays each part, and which country's long
history it is compared with.

`default_regions` builds one per currency of the configured interest rates; build your own to check other factors,
such as a European equity against euro-area unemployment.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
class RelationshipRegion(BaseModel):
    name: str
    currency: str
    inflation_target: float | None = None
    short_rate: str | None = None
    long_rate: str | None = None
    inflation: str | None = None
    unemployment: str | None = None
    equity: str | None = None
    house_prices: str | None = None
    oil: str | None = None
    exchange_rate: str | None = None
    us_short_rate: str | None = None
    credit_spread: str | None = None
    countries: dict[str, str] = {}
    shiller_equity: bool = False
```

**Attributes:**

- <u>name (str):</u> the economy's display name, e.g. "United States".
- <u>currency (str):</u> its currency, e.g. "USD"; picks the inflation target.
- <u>inflation_target (float &#124; None):</u> the central bank's inflation target (0.02 is 2%); None skips the at-target check.
- <u>short_rate, long_rate, inflation, unemployment (str &#124; None):</u> the factor names of the economy's short and long interest rate, consumer price inflation and unemployment rate.
- <u>equity (str &#124; None):</u> an equity total-return index of this economy.
- <u>house_prices (str &#124; None):</u> its house-price growth (the real_estate factor).
- <u>oil (str &#124; None):</u> an oil price.
- <u>exchange_rate (str &#124; None):</u> its currency per US dollar, e.g. euros per dollar.
- <u>us_short_rate (str &#124; None):</u> the US short rate, the other leg of the rate differential.
- <u>credit_spread (str &#124; None):</u> a corporate credit spread.
- <u>countries (dict[str, str]):</u> part -> the country whose OECD history it is compared with, e.g. {"unemployment": "France"}.
- <u>shiller_equity (bool):</u> compare the equity with Shiller's US total return since 1871 instead of its own history.

</details>

#### RelationshipRegion.roles

Part -> simulated factor name, for the parts this economy has; equity_inflation reads the inflation factor.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
roles() -> dict[str, str]
```

</details>

### Realism

Checks that every factor's scenarios stay within what its history has shown, and reach its extremes about as
often as history did: the range of its level, its largest one-year rise and fall, the deepest and longest
drawdowns of a price, and the regimes a rate or inflation can sit in for years (inflation above 5%, a short rate
at the zero lower bound, an inverted curve). A calibration fits each factor's moves on a few decades of data;
nothing in the fit itself stops a mean-reverting rate from wandering below anything a central bank has set, or
an equity from losing more in a decade than the US market did in the Great Depression, nor keeps a calm window's
fit from ruling out a 1970s. Scenarios that do either drive capital and liability numbers with a world that never
happens, so this is worth measuring before a run feeds an asset-liability study.

Every statistic is measured identically on the factor's longest record and on each scenario, read at year ends as
in the relationship checks: OECD series from the 1950s for rates, inflation and unemployment; Shiller's nominal
US home price index since 1890 for US house prices; each equity market's long index (`EQUITY_LONG_HISTORIES`:
Shiller's US total return since 1871, Ken French's US small caps since 1926, European market since 1990 and
emerging markets since 1989, the Nikkei 225 since 1965); the World Bank's Pink Sheet since 1971 for commodities;
and exchange rates in real terms, the rate times US over foreign consumer prices, since relative purchasing power
parity moves the nominal rate with the inflation gap. Where the record is a longer one, a second one stays beside
it (the factor's own history, or the OECD's house prices), and a real range keeps its nominal reading.

The grade compares frequencies, on both sides, not the single most extreme path. History is cut into every window
as long as the run, each read like a scenario, and at the most extreme level history reached in at least two
separate episodes the share of scenarios reaching it is set against the share of windows that did: inside the 90%
Wilson band of that share passes, inside the 99% band warns, outside fails, too rarely being a tail too thin and too
often one too fat. Overlapping windows share most of their years, so the band rests on history's years over the
window length, a handful of independent windows, and the table says how many. Beyond history's worst, a single
event whose frequency history cannot tell, the 1-in-200 rule remains: the worst widened by a tolerance (half a
typical year's move, or one year for a stretch) and a margin (one and a half moves, or three years) may each be
passed by at most the share of scenarios that once in 200 years over the run implies, the 99.5% one-year level of
Solvency II, European Parliament and Council (2009, Article 101(3)): 14% of 30-year scenarios. Any scenario in an
impossible state, such as zero unemployment or a negative price, fails.

| Kind | Statistics |
|:-----|:-----------|
| Rates, inflation, unemployment, house-price growth, spreads | range, largest one-year rise and fall |
| Exchange rates | real range (the nominal one beside it), largest one-year rise and fall |
| Equities, commodities | largest one-year rise and fall, worst 10-year drawdown, longest drawdown within 10 years |
| House prices | also the worst 10-year fall in the price index and its longest drawdown |
| Short rates | longest stretch at the zero lower bound (at or below 0.5%) |
| Long rates | longest curve inversion (the long rate below the short rate) |
| Inflation | longest stretch above 5%, deflation below -10% two years running |

`check_parameters` adds the guardrails on the fitted parameters themselves: fits at a bound, half-lives outside 0.1
to 50 years, long-run levels outside history's range, volatility far from the realised one, and equity crisis
regimes far more frequent or longer than the same model fitted on the long US record.

**As an example:**

```python
from financescenarios import Scenarios

scenarios = Scenarios.from_profiles(settings="default", factor_set="default")
result = scenarios.simulate(n_simulations=1000, years=30)
scenarios.check_realism(result)
```

**References:**

- European Parliament and Council (2009). "Directive 2009/138/EC (Solvency II)", Article 101(3): the capital requirement is calibrated to a 99.5% Value-at-Risk over one year. <https://eur-lex.europa.eu/eli/dir/2009/138/oj>
- Shiller, R.J. U.S. stock market data since 1871. <https://shillerdata.com/>
- French, K.R. Data Library. <https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html>
- World Bank. Commodity Markets, "Pink Sheet" data, monthly prices. <https://www.worldbank.org/en/research/commodity-markets>
- Shiller, R.J. (2015). "Irrational Exuberance", 3rd edition, Princeton University Press, Figure 3.1, as updated by the author: US home prices since 1890. <https://shillerdata.com/>
- Wilson, E.B. (1927). "Probable Inference, the Law of Succession, and Statistical Inference." Journal of the American Statistical Association, 22(158), 209-212. <https://doi.org/10.1080/01621459.1927.10502953>
- Working, H. (1960). "Note on the Correlation of First Differences of Averages in a Random Chain." Econometrica, 28(4), 916-918. <https://doi.org/10.2307/1907574>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
Realism(
    economics: Economics | None = None,
    relationships: Relationships | None = None,
    long_history: LongHistory | None = None,
    cache_dir: str | Path | None = None,
)
```

**Args:**

- <u>economics (Economics &#124; None):</u> a Finance Toolkit `Economics` instance whose window starts in 1871 or earlier; built on first use when omitted. No API key is needed.
- <u>relationships (Relationships &#124; None):</u> the relationship checks whose history reader and cache to share. Defaults to None, a new one on `economics`.
- <u>long_history (LongHistory &#124; None):</u> the reader of the equity markets' long indices. Defaults to None, a new one on the same `Economics`.
- <u>cache_dir (str &#124; Path &#124; None):</u> where the Pink Sheet and Shiller's home prices are kept once downloaded. Defaults to None, the validation cache (`default_cache_dir`).

</details>

#### Realism.long_history

The long-history reader the equity markets' long indices come through, on the same `Economics`.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
realism.long_history  # property -> LongHistory
```

</details>

#### Realism.check

Measure every factor's range, moves, drawdowns and stretches on history, on its windows as long as the run and
on every scenario, and grade how often the scenarios reach history's recurring extremes against how often its
windows did, and how often they go beyond its worst.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
check(
    result: ScenarioSet,
    config: ScenariosConfig,
    history: list[HistoricalSeries] | None = None,
    factors: list[RealismFactor] | None = None,
    summary: bool = False,
) -> pl.DataFrame
```

**Args:**

- <u>result (ScenarioSet):</u> the run; its step must divide a year (monthly, quarterly or yearly).
- <u>config (ScenariosConfig):</u> the configuration it was simulated from, which says what each factor is.
- <u>history (list[HistoricalSeries] &#124; None):</u> the factors' own histories: the yardstick for factors without a longer record (credit spreads, or an equity or commodity outside the long-history tables) and the second column beside it otherwise; None leaves the first ungraded.
- <u>factors (list[RealismFactor] &#124; None):</u> the factors to check; None takes every configured one (`default_realism_factors`).
- <u>summary (bool):</u> return one row per factor, its worst status and the metrics that warn or fail, instead of one row per metric. Defaults to False.

**Returns:**

<u>pl.DataFrame:</u> one row per factor and metric: "factor", "kind", "metric", "status" (the worse of "envelope_status" and "frequency_status"), "envelope_status", "frequency_status", "tail" ("as history", "too thin", "too fat" or "single event"), "history", "secondary_history", "simulated_median", "simulated_extreme", "tolerance", "margin", "beyond_history", "beyond_tolerance", "beyond_margin", "allowed", "recurring_level", "recurring_episodes", "history_share", "share_low", "share_high", "independent_windows", "simulated_share", "nominal_history", "nominal_extreme", "scenarios", "unit", "history_source", "secondary_history_source" and "detail"; with `summary`, "factor", "kind", "status" and "flagged".

**Raises:**

- <u>ValueError:</u> if the run's step does not divide a year.

</details>

#### Realism.history

A factor's year-end history, and its short rate's for a long rate: the OECD series of its country, Shiller's
data or the long index of its market for an equity (`RealismFactor.long_history`), and its own history
otherwise. An equity whose long index cannot be read falls back to its own history.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
history(factor: RealismFactor, own_history: dict[str, HistoricalSeries]) -> YearlySample
```

**Args:**

- <u>factor (RealismFactor):</u> the factor.
- <u>own_history (dict[str, HistoricalSeries]):</u> factor name -> its own history.

**Returns:**

<u>YearlySample:</u> one row of year-end values per part.

</details>

#### Realism.secondary_history

A second record at year ends, read beside a longer one: the OECD's house prices beside Shiller's, and the
factor's own (calibration) history otherwise; None when the factor is read against its own history anyway or
has none.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
secondary_history(
    factor: RealismFactor,
    own_history: dict[str, HistoricalSeries],
) -> YearlySample | None
```

**Args:**

- <u>factor (RealismFactor):</u> the factor.
- <u>own_history (dict[str, HistoricalSeries]):</u> factor name -> its own history.

**Returns:**

<u>YearlySample &#124; None:</u> one row of year-end values per part.

</details>

#### Realism.home_prices

Year-over-year growth of Shiller's nominal US home price index since 1890, from the Figure 3.1 workbook on
his data page, keyless; downloaded once into the validation cache (under "shiller"; delete the file to fetch
a newer edition) and read once per instance; None when it cannot be read.

**References:**

- Shiller, R.J. (2015). "Irrational Exuberance", 3rd edition, Princeton University Press, Figure 3.1, as updated by the author. <https://shillerdata.com/>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
home_prices() -> tuple[np.ndarray, np.ndarray] | None
```

**Returns:**

<u>tuple[np.ndarray, np.ndarray] &#124; None:</u> the years and their growth over the year before.

</details>

#### Realism.commodity_prices

A commodity's year-end (December average) price in the World Bank's Pink Sheet from `PINK_SHEET_FIRST_YEAR`;
None when the workbook or the series cannot be read.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
commodity_prices(series: str) -> tuple[np.ndarray, np.ndarray] | None
```

**Args:**

- <u>series (str):</u> the Pink Sheet series, e.g. "Gold" or "Crude oil, Brent".

**Returns:**

<u>tuple[np.ndarray, np.ndarray] &#124; None:</u> the years and their December prices.

</details>

#### Realism.pink_sheet

The rows of the World Bank's Pink Sheet "Monthly Prices" sheet: monthly average commodity prices in US dollars
since 1960, keyless. Downloaded once into the validation cache (`default_cache_dir`, under "world_bank"; delete
the file to fetch a newer edition) and read once per instance; None when it cannot be read.

**References:**

- World Bank. Commodity Markets, "Pink Sheet" data, monthly prices. <https://www.worldbank.org/en/research/commodity-markets>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
pink_sheet() -> list[tuple[Any, ...]] | None
```

**Returns:**

<u>list[tuple] &#124; None:</u> the sheet's rows.

</details>

#### Realism.long_index

A long index history's year-end levels (`LongHistory.regime_history_returns` compounded into an index),
read once per instance; None when it cannot be read.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
long_index(name: str) -> tuple[np.ndarray, np.ndarray] | None
```

**Args:**

- <u>name (str):</u> "us_market", "us_small_caps", "europe", "japan" or "emerging_markets".

**Returns:**

<u>tuple[np.ndarray, np.ndarray] &#124; None:</u> the years and their year-end index levels.

</details>

#### Realism.regime_record

The regime-switching model fitted on the US market's month-end total returns since 1926 (Ken French's CRSP
value-weighted market, `LongHistory.regime_history_returns("us_market")`), the long record an equity's
crisis regime is compared with; fitted once per instance, None when the data cannot be read or the fit fails.

Month-end returns, like the ones every equity is fitted on, not Shiller's, whose monthly prices are averages
of daily closes: averaging a random walk smooths its changes to about two thirds of their variance and gives
them an autocorrelation of about a quarter (Working (1960)), which would lengthen the record's regimes.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
regime_record(n_regimes: int = 2) -> RegimeParams | None
```

**Args:**

- <u>n_regimes (int):</u> the number of regimes. Defaults to 2.

**Returns:**

<u>RegimeParams &#124; None:</u> the fitted regimes, regime 0 the one with the lowest mean.

</details>

#### Realism.check_parameters

Every guardrail on every calibrated factor's parameters: fit bounds, half-lives, long-run levels, volatility
and equity regimes, each with the fit that produced it.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
check_parameters(
    result: ScenarioSet,
    config: ScenariosConfig,
    calibrated_params: Mapping[str, BaseModel],
    long_run_anchors: dict[str, dict[str, float]] | None = None,
    history: list[HistoricalSeries] | None = None,
    flagged_only: bool = False,
) -> pl.DataFrame
```

**Args:**

- <u>result (ScenarioSet):</u> the run simulated from these parameters.
- <u>config (ScenariosConfig):</u> its configuration, which says how each factor was fitted.
- <u>calibrated_params (Mapping[str, BaseModel]):</u> factor name -> its calibrated parameters (`CalibrationResult.calibrated_params`).
- <u>long_run_anchors (dict[str, dict[str, float]] &#124; None):</u> rate -> its long-run anchor path (`CalibrationResult.long_run_anchors`). Defaults to None.
- <u>history (list[HistoricalSeries] &#124; None):</u> the factors' own histories, the yardstick of the volatility of factors fitted on them. Defaults to None.
- <u>flagged_only (bool):</u> keep only the guardrails that warn or fail. Defaults to False.

**Returns:**

<u>pl.DataFrame:</u> one row per factor and guardrail: "factor", "check", "parameter", "status", "value", "yardstick", "fit" and "detail".

</details>

### RealismFactor

One simulated factor checked against its own long history: what kind of series it is, and where that history
comes from.

`default_realism_factors` builds one per rate, inflation, unemployment, equity, exchange rate, commodity, house-price
and credit factor of a configuration; build your own to compare a factor with another country's record.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
class RealismFactor(BaseModel):
    factor: str
    kind: RealismKind
    country: str | None = None
    long_history: LongHistoryName | None = None
    short_rate: str | None = None
    commodity_series: str | None = None
    inflation: str | None = None
    us_inflation: str | None = None
    price_country: str | None = None
```

**Attributes:**

- <u>factor (str):</u> the simulated factor's name, e.g. "united_states_short_rate".
- <u>kind (str):</u> what it is: "short_rate", "long_rate", "inflation", "unemployment", "house_prices", "credit_spread", "equity", "commodity" or "exchange_rate".
- <u>country (str &#124; None):</u> the country whose OECD series is its history, e.g. "Germany"; None reads the factor's own history (an equity, a commodity, a credit spread).
- <u>long_history (str &#124; None):</u> for an equity, the long index history it is read against (see `EQUITY_LONG_HISTORIES`): "shiller" for Shiller's US total return since 1871, or "us_market", "us_small_caps", "europe", "japan" or "emerging_markets"; for US house prices, "shiller_home_prices", Shiller's nominal US home price index since 1890. None reads the OECD's or the factor's own history.
- <u>short_rate (str &#124; None):</u> for a long rate, the short rate of the same currency, so the length of curve inversions can be read.
- <u>commodity_series (str &#124; None):</u> for a commodity, the World Bank Pink Sheet series it is read against, e.g. "Gold" (see `COMMODITY_LONG_HISTORIES`); None reads its own history.
- <u>inflation, us_inflation (str &#124; None):</u> for an exchange rate (foreign currency per US dollar), the simulated inflation of its currency and of the US, so its range is read in real terms, S * P_US / P_foreign; None reads it in nominal terms only.
- <u>price_country (str &#124; None):</u> the country whose OECD consumer prices deflate the exchange rate's history, e.g. "Germany" for the euro.

</details>

#### RealismFactor.roles

Part -> simulated factor name, in the parts the relationship suite's history reader knows.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
roles() -> dict[str, str]
```

</details>

#### RealismFactor.region

The economy, as the relationship suite's history reader takes it: one part per role, with its country.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
region() -> RelationshipRegion
```

</details>

#### RealismFactor.price_roles

For an exchange rate read in real terms, part -> the simulated inflation behind each price level.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
price_roles() -> dict[str, str]
```

</details>

#### RealismFactor.price_region

The countries whose OECD consumer price levels deflate the exchange rate's history.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
price_region() -> RelationshipRegion
```

</details>

### OutOfSample

A run calibrated as of a past date, set against what happened next: the scenarios, the realized paths on the same
dates, and how the one held the other.

`table` has one row per factor and year ahead (the realized value, the scenarios' 5th to 95th percentiles, where
the realized value fell in them, whether the 50% and 90% bands held it, and the CRPS); `tails` how often the
scenarios reach history's worst and best year; `scores` one row per factor summarizing both; `notes` every choice
made so the calibration saw nothing after `as_of`. `plot()` draws the fan charts with what happened on top.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
class OutOfSample(BaseModel):
    as_of: date
    years: int
    history_start: date | None
    scenarios: ScenarioSet
    realized: ScenarioSet
    table: pl.DataFrame
    tails: pl.DataFrame
    scores: pl.DataFrame
    notes: list[str] = []
    calibration_failures: dict[str, str] = {}
```

**Attributes:**

- <u>as_of (date):</u> the date the calibration saw up to, and the run's start.
- <u>years (int):</u> the years simulated.
- <u>history_start (date &#124; None):</u> the first day of the fitting window.
- <u>scenarios (ScenarioSet):</u> the simulated run.
- <u>realized (ScenarioSet):</u> what happened, one path on the run's dates (NaN where nothing was published yet).
- <u>table (pl.DataFrame):</u> the yearly rows, see `score_rows`.
- <u>tails (pl.DataFrame):</u> the tail rows, see `tail_rows`.
- <u>scores (pl.DataFrame):</u> one row per factor, see `score_out_of_sample`.
- <u>notes (list[str]):</u> what was switched off, dropped or kept, and why.
- <u>calibration_failures (dict[str, str]):</u> factors that did not calibrate, with the reason.

</details>

#### OutOfSample.plot

Fan charts of the scenarios with what actually happened drawn on top.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
plot(factors: str | Sequence[str] | None = None, ax: Axes | None = None) -> Figure
```

**Args:**

- <u>factors (str &#124; Sequence[str] &#124; None):</u> one factor, several (a grid), or None for every factor scored.
- <u>ax (Axes &#124; None):</u> an Axes to draw a single factor into. Defaults to None, a new figure.

**Returns:**

<u>matplotlib.figure.Figure:</u> the figure.

</details>

### OutOfSampleEvaluation

Out-of-sample runs from several origins, scored together: one row per factor of band coverage against its nominal
level (Christoffersen (1998)), PIT uniformity (Diebold, Gunther and Tay (1998)), CRPS (Gneiting and Raftery
(2007), in Ferro's (2014) fair version) and how often the scenarios reach history's worst and best year.

**References:**

- Christoffersen, P.F. (1998). "Evaluating Interval Forecasts." International Economic Review, 39(4), 841-862. <https://doi.org/10.2307/2527341>
- Kupiec, P.H. (1995). "Techniques for Verifying the Accuracy of Risk Measurement Models." The Journal of Derivatives, 3(2), 73-84. <https://doi.org/10.3905/jod.1995.407942>
- Diebold, F.X., Gunther, T.A., Tay, A.S. (1998). "Evaluating Density Forecasts with Applications to Financial Risk Management." International Economic Review, 39(4), 863-883. <https://doi.org/10.2307/2527342>
- Gneiting, T., Raftery, A.E. (2007). "Strictly Proper Scoring Rules, Prediction, and Estimation." Journal of the American Statistical Association, 102(477), 359-378. <https://doi.org/10.1198/016214506000001437>
- Ferro, C.A.T. (2014). "Fair scores for ensemble forecasts." Quarterly Journal of the Royal Meteorological Society, 140(683), 1917-1923. <https://doi.org/10.1002/qj.2270>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
class OutOfSampleEvaluation(BaseModel):
    years: int
    runs: list[OutOfSample]
    skipped: dict[date, str] = {}
    scores: pl.DataFrame
```

**Attributes:**

- <u>years (int):</u> the years each run simulates.
- <u>runs (list[OutOfSample]):</u> every origin that ran, oldest first.
- <u>skipped (dict[date, str]):</u> origins that could not run, with the reason.
- <u>scores (pl.DataFrame):</u> one row per factor, see `score_out_of_sample`.

</details>

#### OutOfSampleEvaluation.table

Every origin's yearly rows in one table.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
outofsampleevaluation.table  # property -> pl.DataFrame
```

</details>

#### OutOfSampleEvaluation.tails

Every origin's tail rows in one table.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
outofsampleevaluation.tails  # property -> pl.DataFrame
```

</details>

#### OutOfSampleEvaluation.notes

Each origin's notes.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
outofsampleevaluation.notes  # property -> dict[date, list[str]]
```

</details>

#### OutOfSampleEvaluation.plot

One factor's fan chart from every origin, with what happened drawn on top.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
plot(factor: str, ax: Axes | None = None) -> Figure
```

**Args:**

- <u>factor (str):</u> the factor.
- <u>ax (Axes &#124; None):</u> an Axes to draw all origins into, one after another. Defaults to None, a new figure.

**Returns:**

<u>matplotlib.figure.Figure:</u> the figure.

</details>

### NaicGoes

The NAIC's Generator of Economic Scenarios (GOES), the prescribed generator of the Valuation Manual for US
principle-based reserves (VM-20 for life, VM-21 for variable annuities), but companies may use their own, as a
benchmark for this run's US interest rates. Conning publishes it monthly at
[naic.conning.com/scenariofiles](https://naic.conning.com/scenariofiles): 10,000 scenarios in the base set (the
"# Total Scenarios" of its statistics workbook) and the 16 deterministic SERT scenarios.

NAIC (2026, VM-20, Appendix 1, section E, p. 20-88) lets a company generate its interest-rate and equity or bond fund
return scenarios, in part or in full, with its own generator instead of the prescribed one, provided their use
satisfies section 2.G. That generator must meet the requirements of Appendix 1 (NAIC (2026, VM-20, section 7.G.3)),
and for variable annuities its scenarios must not give a materially lower total asset requirement (TAR) than the
prescribed ones (NAIC (2026, VM-21, section 8.E), the Valuation Manual's 1 January 2026 edition). Holding a run's US
Treasury rates up against the regulator's own percentile bands shows whether it lets rates go as high and as low as
the prescribed set does. A run with much narrower bands understates interest-rate risk in anything valued on it; much
wider bands overstate it. `compare_interest_rates` reports the differences; `check_acceptance` holds the run to the
acceptance criteria NAIC sets GOES itself (the workbook's Acceptance Criteria_Dashboard sheet: the 1-year yield's
99.5th percentile at or below 18%, no 1-year below -1%, the S&P 500's gross wealth factors and more), with a pass or
fail per criterion. The NAIC files carry Conning's terms of use: they
are downloaded to a local cache for your own use, not redistributed.

**References:**

- NAIC (2026). "Valuation Manual", 1 January 2026 edition: VM-20 Section 7.G and Appendix 1; VM-21 Section 8. <https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf>
- NAIC / Conning. "NAIC Economic Scenario Files." <https://naic.conning.com/scenariofiles>

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
NaicGoes(vintage: str, cache_dir: Path | None = None)
```

</details>

#### NaicGoes.vintage

The release this benchmark reads, e.g. to report which one `latest()` picked.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
naicgoes.vintage  # property -> str
```

</details>

#### NaicGoes.latest

The benchmark for the most recent release the NAIC publishes.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
NaicGoes.latest(cache_dir: Path | None = None) -> 'NaicGoes'
```

</details>

#### NaicGoes.fetch_treasury_percentiles

The NAIC's percentile bands of US Treasury yields per maturity and projection month, the distribution the
prescribed scenario set implies.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fetch_treasury_percentiles() -> pl.DataFrame
```

**Returns:**

<u>pl.DataFrame:</u> `tenor` (e.g. "10yr"), `statistic` (e.g. "p5", "p50", "mean"), `projection_month` and `value`.

</details>

#### NaicGoes.fetch_sert_scenarios

The NAIC's SERT scenarios: a small set of named, prescribed paths for Treasury yields and fund returns, used for
stress testing rather than as a distribution.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fetch_sert_scenarios() -> pl.DataFrame
```

**Returns:**

<u>pl.DataFrame:</u> `scenario`, `time_step` (months from the start), `variable` and `value`.

</details>

#### NaicGoes.compare_interest_rates

Compare a simulated US interest rate's percentile bands with the NAIC's for the same maturity, month by month.

The maturity is worked out from the rate's configuration (the 10-year Treasury yield is compared with the NAIC's
10-year band), or given as `tenor`. Read the result in two ways: the median shows whether the run's central path
drifts where the NAIC's does, and the outer percentiles whether the run allows rates as extreme as the prescribed
set. A gap that widens with the horizon points at the long-run level or the volatility; a gap in the first months
points at the starting point.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
compare_interest_rates(
    scenario_set: ScenarioSet,
    config: ScenariosConfig,
    factor_name: str,
    tenor: str | None = None,
    month_offset: int = 0,
) -> pl.DataFrame
```

**Args:**

- <u>scenario_set (ScenarioSet):</u> a monthly run; the NAIC's bands are monthly.
- <u>config (ScenariosConfig):</u> the configuration that produced the run.
- <u>factor_name (str):</u> the interest rate to compare.
- <u>tenor (str &#124; None):</u> the NAIC maturity, e.g. "10yr". Defaults to None, read from the rate's configuration.
- <u>month_offset (int):</u> how many months into the run the NAIC's first projection month sits; 0 by default.

**Returns:**

<u>pl.DataFrame:</u> per projection month and percentile, the simulated value, the NAIC's and the difference.

**Raises:**

- <u>ValueError:</u> if the factor is not a configured interest rate, its maturity has no NAIC match, or the run is not monthly.

</details>

#### NaicGoes.fetch_acceptance_criteria

The thresholds of the GOES acceptance criteria as this release states them, read from its statistics workbook's
`Acceptance Criteria_Dashboard` sheet, so a check follows NAIC's revisions.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
fetch_acceptance_criteria() -> naic_goes_model.AcceptanceThresholds
```

**Returns:**

<u>AcceptanceThresholds:</u> the thresholds of T1, T2, T4, T5, T6 and the E1 gross wealth factor targets.

</details>

#### NaicGoes.check_acceptance

Hold a run up against the GOES acceptance criteria, the pass marks NAIC sets its own generator: the upper tail
(T1), negative rates (T2), low-for-long (T4), the spread of long averages (T5) and the mean-reversion benchmark
(T6) on the 1-year and 20-year Treasury yields, and the S&P 500's gross wealth factors (E1).

A company may use its own generator if it meets the Valuation Manual's requirements (VM-20, Appendix 1), so a
check against the bar GOES itself is held to shows how close a run is. The 1-year and 20-year yields are the
run's own when it simulates them, and otherwise read off its neighbouring Treasury yields in a straight line
(the 1-year from the 3-month and 5-year, the 20-year from the 10-year and 30-year). The thresholds are the
release's own; GOES failed T4 and one part of T5 on the 30 September 2026 release.

**As an example:**

```python
from financescenarios import Scenarios
from financescenarios.validation.naic_goes.naic_goes_controller import NaicGoes

scenarios = Scenarios.from_profiles(settings="goes", factor_set="goes")
result = scenarios.simulate(years=30, n_simulations=10_000)
NaicGoes(vintage="20260930").check_acceptance(result, scenarios.config, equity_name="us_broad")
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
check_acceptance(
    scenario_set: ScenarioSet,
    config: ScenariosConfig,
    equity_name: str | None = None,
    tolerance: float = naic_goes_model.E1_DEFAULT_TOLERANCE,
) -> pl.DataFrame
```

**Args:**

- <u>scenario_set (ScenarioSet):</u> a monthly run of at least 30 years.
- <u>config (ScenariosConfig):</u> the configuration that produced it, to find each Treasury yield's maturity.
- <u>equity_name (str &#124; None):</u> the equity whose total return is checked against E1, e.g. "us_broad". Defaults to None, no E1.
- <u>tolerance (float):</u> E1's relative tolerance, by default 0.10; NAIC gives the targets without one.

**Returns:**

<u>pl.DataFrame:</u> `criterion`, `statistic`, `value`, `lower`, `upper` and `passed` (null where NAIC only reviews the statistic).

**Raises:**

- <u>ValueError:</u> if the run is not monthly, or its Treasury yields do not span the 1-year and 20-year.

</details>

### Dnb

De Nederlandsche Bank's scenario sets as a benchmark: the 20,000 scenarios over 100 years Dutch pension funds
must use, real world (the P-set) or market consistent (the Q-set, calibrated to market prices including
swaptions), generated with the model the Commissie Parameters specified in 2022. DNB publishes the 20,000
scenarios as Excel workbooks every quarter; each workbook holds one yearly column per
horizon year, 1 to 100 (checked on the 2026Q3 sets).

An independent, regulator-reviewed set of scenarios to hold a run up against. For a euro run it answers whether
the spread of interest rates, inflation and equity returns looks like the one the Dutch regulator prescribes;
for a market-consistent run, the Q-set is a reference calibrated to swaption prices, which free market data
cannot otherwise provide. A run that differs from DNB's is not wrong, but the difference should be one you can
explain, such as a different view on long-run rates. To use DNB's paths in a run instead of comparing, see
`external_scenario_source: {provider: dnb}`.

The data come through the Finance Toolkit, with no API key. DNB's workbook is
about 180 MB, so the first read takes a minute or two and much memory; it is cached afterwards.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios.validation.dnb.dnb_controller import Dnb

dnb = Dnb(Toolkit(["SPY"]))
dnb.compare(result, "eurozone_long_rate", "Nominal rate 10Y")
```

**References:**

- De Nederlandsche Bank. "DNB publiceert definitieve scenariosets bij Wet toekomst pensioenen." <https://www.dnb.nl/voor-de-sector/open-boek-toezicht/sectoren/pensioenfondsen/dnb-publiceert-definitieve-scenariosets-bij-wet-toekomst-pensioenen/>
- Commissie Parameters (2022). "Technical Appendix: Specification of the CP2022 Model." <https://www.rijksoverheid.nl/documenten/rapporten/2022/11/29/bijlage-2-technische-appendix>

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
Dnb(toolkit: Toolkit)
```

</details>

#### Dnb.distribution

DNB's distribution of one variable per year of the horizon.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
distribution(
    variable: str,
    measure: str = 'real_world',
    quantiles: Sequence[float] = _DEFAULT_QUANTILES,
) -> pl.DataFrame
```

**Args:**

- <u>variable (str):</u> "Nominal rate 1Y", "5Y", "10Y", "20Y" or "30Y", "Real rate EU 10Y", "Equity return", "Inflation EU" or "Inflation NL".
- <u>measure (str):</u> "real_world" (the P-set) or "market_consistent" (the Q-set).
- <u>quantiles (Sequence[float]):</u> the quantiles, each in [0, 1].

**Returns:**

<u>pl.DataFrame:</u> a "year" column and one column per quantile, named as the quantile ("0.05").

**Raises:**

- <u>ValueError:</u> if nothing comes back for the variable.

</details>

#### Dnb.compare

Set a run's factor beside DNB's matching variable, quantile by quantile, at every whole year both cover. The
columns and the reading are those of `compare_with_scenario_set`: equity is compared as yearly returns, rates and
inflation as levels.

A run whose quantiles track DNB's tells a story about the future similar to the one the Dutch regulator
prescribes; a gap that widens with the years shows where the run's long-term behaviour (mean reversion, long-run
levels, volatility) differs from DNB's. Neither set is "right", but a gap is something to be able to explain.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
compare(
    scenario_set: ScenarioSet,
    factor: str,
    variable: str,
    measure: str = 'real_world',
    quantiles: Sequence[float] = _DEFAULT_QUANTILES,
) -> pl.DataFrame
```

**Args:**

- <u>scenario_set (ScenarioSet):</u> the run.
- <u>factor (str):</u> the factor to compare.
- <u>variable (str):</u> DNB's matching variable, see `distribution`.
- <u>measure (str):</u> "real_world" for a real-world run, "market_consistent" for a risk-neutral one.
- <u>quantiles (Sequence[float]):</u> the quantiles to compare.

**Returns:**

<u>pl.DataFrame:</u> per year, this run's and DNB's quantiles and their difference.

</details>

#### Dnb.compare_moments

Set a run's mean, spread and percentiles beside DNB's at each of `years`, for every factor named in
`factors`, and for equity also the return it compounds to from the start (`dnb_model.compare_moments`).

Where `compare` lines up quantiles, this answers the questions a reproduction is judged on: does the run's
1-year rate average what DNB's does in ten years, is its spread as wide, and does equity compound to the same
return over a century? DNB's set is read in a separate process (`dnb_moments`), as its workbook is large.

**As an example:**

```python
from financetoolkit import Toolkit

from financescenarios import Scenarios
from financescenarios.validation.dnb.dnb_controller import Dnb

result = Scenarios.from_profiles("dnb", "dnb").simulate()
Dnb(Toolkit(["SPY"])).compare_moments(result, {"Nominal rate 10Y": "euro_10y", "Equity return": "world_equity"})
```

Which returns, for DNB's 2026Q4 set and 2,000 scenarios, the 10-year rate's mean of 2.31% in year 10 against
DNB's 2.31%, with a standard deviation of 1.29% against 1.29%, and equity compounding to a median of 5.65% a
year over 100 years against DNB's 5.61%.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
compare_moments(
    scenario_set: ScenarioSet,
    factors: dict[str, str],
    years: Sequence[int] = dnb_model.DNB_YEARS,
    measure: str = 'real_world',
) -> pl.DataFrame
```

**Args:**

- <u>scenario_set (ScenarioSet):</u> the run.
- <u>factors (dict[str, str]):</u> DNB's variable to the run's factor, e.g. {"Nominal rate 10Y": "euro_10y", "Equity return": "world_equity"}.
- <u>years (Sequence[int]):</u> the horizon years; 1, 5, 10, 30 and 100 by default.
- <u>measure (str):</u> "real_world" (the P-set) or "market_consistent" (the Q-set).

**Returns:**

<u>pl.DataFrame:</u> per variable and year the run's and DNB's mean, sd, p5, p50 and p95, their differences and the ratio of the sds.

</details>

#### Dnb.compare_correlations

Set a run's correlations across scenarios beside DNB's, pair by pair at each of `years`
(`dnb_model.compare_correlations`): for one, whether equity falls in the scenarios where the 1-year rate
rises, as strongly as in DNB's set (-0.49 in year 1 of the 2026Q4 set).

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
compare_correlations(
    scenario_set: ScenarioSet,
    factors: dict[str, str],
    pairs: Sequence[tuple[str, str]] = dnb_model.DNB_CORRELATION_PAIRS,
    years: Sequence[int] = dnb_model.DNB_CORRELATION_YEARS,
    measure: str = 'real_world',
) -> pl.DataFrame
```

**Args:**

- <u>scenario_set (ScenarioSet):</u> the run.
- <u>factors (dict[str, str]):</u> DNB's variable to the run's factor.
- <u>pairs (Sequence[tuple[str, str]]):</u> pairs of DNB's variables; pairs naming a variable missing from `factors` are left out.
- <u>years (Sequence[int]):</u> the horizon years; 1, 10 and 30 by default.
- <u>measure (str):</u> "real_world" (the P-set) or "market_consistent" (the Q-set).

**Returns:**

<u>pl.DataFrame:</u> "first", "second", "year", "run", "dnb" and "difference".

</details>

### compare_published

Check a reference factor set against the numbers its paper reports for its own model.

The `ahlgrim`, `hibbert` and `wilkie` factor sets state their papers' published parameters and starting values, so
run as the sets run, from the papers' own start dates and over their horizons, they should reproduce the tables
of Ahlgrim, D'Arcy and Gorvett (2005, Tables 1 and 2), Hibbert, Mowbray and Turnbull (2001, Exhibit 7.2A) and
Wilkie (1986, Table 3). This runs the set without data (`simulate_published`) and compares every reported mean,
standard deviation, percentile and correlation the package can recompute. A difference counts as Monte Carlo
error when it is within four standard errors of the difference between the two estimates (batch means for this
run's, scaled to the paper's number of scenarios for the paper's) plus half the paper's last printed digit.

**As an example:**

```python
from financescenarios.validation.published_frameworks.published_frameworks_controller import compare_published

compare_published("wilkie")
```

Which returns (the first 3 of 91 rows, all within):

| source | variable | statistic | horizon | published | simulated | tolerance | within |
|:-------|:---------|:----------|--------:|----------:|----------:|----------:|:-------|
| Table 3 | GQ | mean | 1.0 | 0.0537 | 0.0538 | 0.0076 | true |
| Table 3 | GQ | mean | 5.0 | 0.0537 | 0.0531 | 0.0055 | true |
| Table 3 | GQ | mean | 10.0 | 0.0514 | 0.0526 | 0.0043 | true |

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
compare_published(framework: str, n_simulations: int = 10000, seed: int = 2001) -> pl.DataFrame
```

**Args:**

- <u>framework (str):</u> "ahlgrim", "hibbert" or "wilkie".
- <u>n_simulations (int):</u> the number of scenarios. Defaults to 10,000.
- <u>seed (int):</u> the random seed. Defaults to 2001.

**Returns:**

<u>pl.DataFrame:</u> one row per published number: source, variable, statistic, horizon (years; 0 for a statistic pooled over the horizon), published, simulated, tolerance and within.

</details>

### held_up

How a published model held up: its fan, run from its paper's start date as the reference factor set runs it,
laid over what actually happened since, year by year.

A model published with its parameters makes a forecast one can check years later. Ahlgrim, D'Arcy and Gorvett
(2005) start from the US market of June 2004, Hibbert, Mowbray and Turnbull (2001) from end-March 2001 and Wilkie
(1986) from his neutral start, dated 1986; their papers set them on US, UK and UK data. Each anniversary's
realized value (the OECD's short and long rates, year-on-year CPI inflation, unemployment, share prices and US
house-price growth, all keyless) is placed in the fan: the share of years inside the 50% and 90% bands, the PITs
and the CRPS against a forecast of no change. The years share one path of history, so these describe what
happened rather than test calibration, and the OECD series are stand-ins for the papers' own (the 3-month rate for
a 1-month one, a 10-year gilt for Consols, a share price index for Wilkie's and Hibbert's indices, house prices for
NCREIF's commercial property).

**As an example:**

```python
from financescenarios.validation.published_frameworks.published_frameworks_controller import held_up

rows, scores = held_up("wilkie")
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
held_up(
    framework: str,
    n_simulations: int | None = None,
    seed: int = 2001,
    toolkit: Any = None,
) -> tuple[pl.DataFrame, pl.DataFrame]
```

**Args:**

- <u>framework (str):</u> "ahlgrim", "hibbert" or "wilkie".
- <u>n_simulations (int &#124; None):</u> the number of scenarios. Defaults to None, the paper's own.
- <u>seed (int):</u> the random seed. Defaults to 2001.
- <u>toolkit (Toolkit &#124; None):</u> the Finance Toolkit to read the OECD data with. Defaults to None, a keyless one.

**Returns:**

<u>tuple[pl.DataFrame, pl.DataFrame]:</u> the rows of `held_up_rows` (the fan's percentiles and the realized value per factor and year, the chart data) and the scores of `held_up_scores` per factor.

</details>

### How It Is Calculated

The model functions behind this page, each with the formula it implements.

#### policy_reaction

How far the short rate moves with inflation and with unemployment, the reaction a Taylor rule prescribes.

One regression of each year's change in the short rate on the same year's changes in inflation and unemployment.
With a steady neutral rate and natural unemployment rate, the Taylor (1993, p. 202, eq. 1) rule written with the
unemployment gap, as in Federal Reserve (2026, Monetary Policy Report, Part 2, Box 4, Table A, p. 43), gives slopes
of +1.5 and -1.0 (the balanced-approach rule -2.0), so the changes carry the rule's own coefficients without
estimating either unobserved level.

The formula is as follows:

$$
\operatorname{di}(t) = c + b_{\pi} \cdot \operatorname{dpi}(t) + b_{u} \cdot \operatorname{du}(t) + e(t)
$$

Where i is the short rate, pi inflation, u unemployment and d the change over one year, year end to year end.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
policy_reaction(
    history: YearlySample,
    simulation: YearlySample,
    region: RelationshipRegion,
) -> list[RelationshipResult]
```

**Returns:**

<u>list[RelationshipResult]:</u> the reaction to inflation (b_pi) and to unemployment (b_u).

</details>

#### rates_at_target

Rates are near neutral when inflation is at the central bank's target and higher when it is well above it.

The statistic is the average short rate at year ends with inflation more than 2 points above target, less the
average with inflation within half a point of it. Both bands are judgement. The detail gives the at-target level,
the run's reading of the neutral rate. Inflation is the consumer price index the run simulates, while the Federal
Reserve targets the PCE price index, which tends to run a little lower, and history before a target was set is
read against today's 2%.

The formula is as follows:

$$
D = \operatorname{mean}(i(t) | \pi(t) > \pi \cdot + 0.02) - \operatorname{mean}(i(t) | | \pi(t) - \pi \cdot | \leq 0.005)
$$

Where i is the short rate, pi inflation and pi* the target.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
rates_at_target(
    history: YearlySample,
    simulation: YearlySample,
    region: RelationshipRegion,
) -> list[RelationshipResult]
```

</details>

#### phillips_curve

Inflation falls in the years unemployment rises: the Phillips curve read in yearly changes, which removes the
drifting natural rate and inflation expectations that make the levels relationship unstable.

The formula is as follows:

$$
\operatorname{dpi}(t) = c + b \cdot \operatorname{du}(t) + e(t)
$$

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
phillips_curve(
    history: YearlySample,
    simulation: YearlySample,
    region: RelationshipRegion,
) -> list[RelationshipResult]
```

</details>

#### long_rate_comovement

The long rate moves with the short rate, by less than one for one, as a long yield averages expected short rates.

The formula is as follows:

$$
\operatorname{dL}(t) = c + b \cdot \operatorname{di}(t) + e(t)
$$

Where L is the long rate and i the short rate.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
long_rate_comovement(
    history: YearlySample,
    simulation: YearlySample,
    region: RelationshipRegion,
) -> list[RelationshipResult]
```

</details>

#### inverted_curve

A flat or inverted yield curve comes before rising unemployment within two years.

The slope uses every year end, so it is defined in every scenario; the detail gives the plain reading, the average
rise in unemployment over the next two years after a year end with the long rate below the short rate.

The formula is as follows:

$$
u(t + 2) - u(t) = c + b \cdot (L(t) - i(t)) + e(t)
$$

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
inverted_curve(
    history: YearlySample,
    simulation: YearlySample,
    region: RelationshipRegion,
) -> list[RelationshipResult]
```

</details>

#### equity_unemployment

Bear markets come with rising unemployment: the correlation between a year's equity total return and the change in
unemployment over that year and the next, since stock prices fall ahead of the labour market.

The formula is as follows:

$$
\rho = \operatorname{corr}(R(t),\; u(t + 1) - u(t - 1))
$$

Where R(t) is the total return over year t.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
equity_unemployment(
    history: YearlySample,
    simulation: YearlySample,
    region: RelationshipRegion,
) -> list[RelationshipResult]
```

</details>

#### inflation_equity_buckets

Equities lose in real terms in high-inflation years: the average real total return in years with inflation above
5%, less the average in years below 3%. The detail adds the 3-5% bucket.

Each year's real return deflates its total return by the same year's December-to-December inflation, the reading
Shiller's real total-return series gives on history; a scenario's inflation at the year end is its year-over-year
rate. History starts in `first_year`.

The formula is as follows:

$$
r(t) = (1 + R(t)) / (1 + \pi(t)) - 1
$$

$$
D = \operatorname{mean}(r(t) | \pi(t) > 5\%) - \operatorname{mean}(r(t) | \pi(t) < 3\%)
$$

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
inflation_equity_buckets(
    history: YearlySample,
    simulation: YearlySample,
    region: RelationshipRegion,
    first_year: int = INFLATION_BUCKET_FIRST_YEAR,
) -> list[RelationshipResult]
```

</details>

#### rates_house_prices

Higher rates slow house prices with a lag: the change in house-price growth over the next year against this
year's change in the long rate, which mortgage rates follow.

The formula is as follows:

$$
g(t + 1) - g(t) = c + b \cdot \operatorname{dL}(t) + e(t)
$$

Where g is year-over-year house-price growth and L the long rate.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
rates_house_prices(
    history: YearlySample,
    simulation: YearlySample,
    region: RelationshipRegion,
) -> list[RelationshipResult]
```

</details>

#### oil_inflation

Oil price rises pass into inflation within the year.

The formula is as follows:

$$
\operatorname{dpi}(t) = c + b \cdot (O(t) / O(t - 1) - 1) + e(t)
$$

Where O is the oil price at the year end.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
oil_inflation(
    history: YearlySample,
    simulation: YearlySample,
    region: RelationshipRegion,
) -> list[RelationshipResult]
```

</details>

#### rate_differential_currency

The currency's move over the next year against its interest-rate gap with the US: uncovered interest parity
expects the higher-rate currency to weaken by the gap (a slope of +1), while history often shows a slope below
zero, the forward premium puzzle; the grade follows history.

The formula is as follows:

$$
\ln(X(t + 1) / X(t)) = c + b \cdot (i(t) - i_{US}(t)) + e(t)
$$

Where X is the currency per US dollar, so a rise is a weaker currency.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
rate_differential_currency(
    history: YearlySample,
    simulation: YearlySample,
    region: RelationshipRegion,
) -> list[RelationshipResult]
```

</details>

#### credit_unemployment

Credit spreads widen in the years unemployment rises.

The formula is as follows:

$$
\operatorname{ds}(t) = c + b \cdot \operatorname{du}(t) + e(t)
$$

Where s is the credit spread.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
credit_unemployment(
    history: YearlySample,
    simulation: YearlySample,
    region: RelationshipRegion,
) -> list[RelationshipResult]
```

</details>

#### frequency_band

The Wilson score interval of a share read on `windows` independent observations, at `z` standard errors.

The formula is as follows:

$$
c = (p + z ^{2} / (2n)) / (1 + z ^{2} / n)
$$

$$
h = z \cdot \sqrt{p \cdot (1 - p) / n + z ^{2} / (4n ^{2})} / (1 + z ^{2} / n)
$$

Where p is the share, n the number of windows and the band runs from c - h to c + h.

**References:**

- Wilson, E.B. (1927). "Probable Inference, the Law of Succession, and Statistical Inference." Journal of the American Statistical Association, 22(158), 209-212. <https://doi.org/10.1080/01621459.1927.10502953>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
frequency_band(share: float, windows: float, z: float) -> tuple[float, float]
```

**Args:**

- <u>share (float):</u> the share p.
- <u>windows (float):</u> the effective number of windows n.
- <u>z (float):</u> the number of standard errors.

**Returns:**

<u>tuple[float, float]:</u> the band's low and high ends.

</details>

{% raw %}
#### with_real_exchange_rate

Add the real exchange rate to history and to the run, so an exchange rate's range is read in real terms: relative
purchasing power parity moves the nominal rate with the inflation gap between the two currencies, so a nominal
range is the wrong yardstick over decades.

On history it reads the consumer price levels; on the run, each scenario's price levels start from history's
latest and grow with its own simulated inflation (the run's "price_level" and "us_price_level" are those
cumulative indices, 1 at the start).

The formula is as follows:

$$
Q(t) = S(t) \cdot P_{US}(t) / P_{\text{foreign}}(t)
$$

Where S is the foreign currency per US dollar and P a consumer price level, so a rise is a cheaper foreign currency
in real terms.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
with_real_exchange_rate(
    history: YearlySample,
    simulation: YearlySample,
) -> tuple[YearlySample, YearlySample]
```

**Args:**

- <u>history (YearlySample):</u> with "exchange_rate", "price_level" and "us_price_level".
- <u>simulation (YearlySample):</u> with "exchange_rate" and the two cumulative price indices.

**Returns:**

<u>tuple[YearlySample, YearlySample]:</u> both with "real_exchange_rate" added, or unchanged when a part is missing.

</details>
{% endraw %}

#### compare_with_scenario_set

The quantiles of one simulated factor beside DNB's at every whole year both cover.

How the spread of this run's scenarios for, say, a long interest rate compares with the spread in
the scenarios the Dutch regulator prescribes, year by year. Similar quantiles mean the run tells a similar
story about how high or low the variable can go; a steady gap shows where this run's calibration differs.

The formula is as follows:

$$
r_{t} = P_{t} / P_{t-1} - 1
$$

$$
D(q,\; t) = Q_{q}(x_{t}) - B(q,\; t)
$$

Where P_t is an equity factor's simulated price at whole year t (no return exists at year 0), x_t the compared
value across simulations (r_t for an equity, the level otherwise), Q_q its q-quantile, B(q, t) DNB's and
D(q, t) the "difference_q" column.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
compare_with_scenario_set(
    scenario_set: ScenarioSet,
    factor: str,
    variable: str,
    benchmark: pl.DataFrame,
    quantiles: Sequence[float],
) -> pl.DataFrame
```

**Args:**

- <u>scenario_set (ScenarioSet):</u> the run.
- <u>factor (str):</u> its factor to compare.
- <u>variable (str):</u> DNB's variable, e.g. "Nominal rate 10Y", "Inflation EU" or "Equity return". An equity factor is compared as its year-on-year return, the others as their level.
- <u>benchmark (pl.DataFrame):</u> DNB's distribution: a "year" column and one column per quantile, named as the quantile (e.g. "0.05").
- <u>quantiles (Sequence[float]):</u> the quantiles to compare; each must be a column of `benchmark`.

**Returns:**

<u>pl.DataFrame:</u> "year", and per quantile q the columns "run_q", "dnb_q" and "difference_q" (run minus DNB).

**Raises:**

- <u>KeyError:</u> if `factor` is not in the run.
- <u>ValueError:</u> if a quantile is missing from `benchmark` or the two share no year.

</details>
