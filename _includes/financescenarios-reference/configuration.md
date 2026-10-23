## Reference

The reference is generated from the docstrings in the package, so it says what `help(...)` says in Python: what each class and function does, a worked example with real output where the docstring has one, and the arguments and return value folded underneath.

Everything on this page imports as follows:

```python
from financescenarios import ScenariosConfig, EngineConfig, ToolkitConfig, InterestRateConfig, InflationConfig, UnemploymentConfig, EquityConfig, FXConfig, CreditConfig, CommodityConfig, DividendYieldConfig, DividendGrowthConfig, RealEstateConfig, YieldCurveConfig, OUBeliefs, InterestRateBeliefs, EquityBeliefs, BeliefPath, Profile, list_presets, load_profiles, load_config, load_profile_library, scaffold_project
from financescenarios.config.config_model import CreditTermStructureConfig
from financescenarios.config.config_model import HjmConfig
from financescenarios.config.config_model import CreditMigrationConfig
from financescenarios.config.config_model import LeadingIndicatorConfig
from financescenarios.config.config_model import MortalityConfig
from financescenarios.config.config_model import CorrelationsConfig
from financescenarios.config.config_model import FixedCorrelation
```

### ScenariosConfig

The full configuration of a run: when it starts, how it executes, which factors it simulates and which views
override their history.

Every run is built from one `ScenariosConfig`, so it is also the record of a study's assumptions: the history each
factor is fitted on, the models chosen, and every belief (a long-run inflation target, a lower equity premium) laid
over the fit. You rarely write one by hand: `load_profiles` builds it from a named settings profile and factor
set, and `load_config` from two YAML files. It can also be built straight from a dictionary with
`ScenariosConfig.model_validate`. Each top-level key is one section:

| Key | What it sets |
|:----|:-------------|
| `start_date` | The first date of the simulation; the only required key. |
| `engine` | The number of scenarios, steps and their frequency, the seed and how shocks are drawn (see below). |
| `toolkit` | The history the factors are fitted on (start and end date) and any extra tickers. |
| `reporting` | The currency results can be converted into. |
| `interest_rates`, `inflation`, `unemployment` | One entry per country, at least one each. |
| `equities` | One entry per index or ETF, at least one. |
| `fx`, `commodities`, `credit`, `dividend_yield`, `dividend_growth` | Optional lists, empty by default. |
| `yield_curve`, `credit_term_structure`, `hjm`, `real_estate` | Optional factors, switched on with `enabled: true`. |
| `leading_indicator`, `credit_migration`, `climate`, `mortality` | The same. |
| `external_scenario_source` | A published scenario set (GOES or DNB) used for some factors instead. |
| `correlations` | Correlations stated as values, as a published model fixes them, instead of estimated. |
| `published_model` | Reproduce a published model (`ahlgrim`, `hibbert`, `wilkie`) as its paper ran it, no data. |

How shocks are drawn matters for the tails. With `shock_distribution: student_t` the joint shocks have fat tails and
tail dependence: extreme moves are more frequent and tend to arrive in several factors at once, as in 2008 or 2020,
where under the default Gaussian shocks a joint crash is far rarer. `antithetic: true` pairs every scenario with its
mirror image (the same shocks with the opposite sign), which cancels much of the sampling noise in averages and
valuations for the same number of scenarios; it does not change the model, only how precisely a given number of
scenarios measures it.

Interest rates, inflation and unemployment are written per country, as `{defaults: {...}, countries: [{name: ...},
...]}`, so shared settings are given once. The configuration is checked as it is built: a misspelt key, a duplicate
factor name or settings that do not fit together raise an error before any data is fetched. `describe()` lists the
factors it would simulate, `tickers` the tickers it would download, and `factor_categories` and `factor_labels` give
each factor's category and display name.

**As an example:**

```python
from datetime import date

from financescenarios.config.config_model import ScenariosConfig

config = ScenariosConfig.model_validate(
    {
        "start_date": date(2026, 10, 1),
        "engine": {"n_simulations": 2000, "n_steps": 12, "frequency": "monthly", "seed": 42},
        "interest_rates": {"countries": [{"name": "United States"}]},
        "inflation": {"countries": [{"name": "United States"}]},
        "unemployment": {"countries": [{"name": "United States"}]},
        "equities": [{"name": "us_broad", "ticker": "SPY", "period": "monthly"}],
    }
)
config.describe()
```

Which returns:

| category | n_factors | factors |
|:---------|----------:|:--------|
| equities | 1 | us_broad |
| inflation | 1 | united_states_inflation |
| interest_rates | 1 | united_states_short_rate |
| unemployment | 1 | united_states_unemployment |

and `config.tickers` is `['^IRX', 'SPY']`: the 13-week Treasury yield for the short rate, and SPY.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
class ScenariosConfig(_StrictModel):
    start_date: date
    engine: EngineConfig = Field(default_factory=EngineConfig)
    reporting: ReportingConfig = Field(default_factory=ReportingConfig)
    interest_rates: list[InterestRateConfig] = Field(default_factory=lambda: [InterestRateConfig()], description='One interest rate per country or region, each its own correlated factor; at least one. Written in YAML as {defaults: {...}, countries: [{name: ..., <overrides>}, ...]}, or as a list of entries.')
    inflation: list[InflationConfig] = Field(default_factory=lambda: [InflationConfig()], description='One inflation rate per country, each its own correlated factor; at least one. Written as {defaults, countries}, like interest_rates.')
    equities: list[EquityConfig] = Field(default_factory=lambda: [EquityConfig()], description='One entry per equity index, sector, region or style, each its own correlated regime-switching factor; at least one.')
    unemployment: list[UnemploymentConfig] = Field(default_factory=lambda: [UnemploymentConfig()], description="One unemployment rate per region, each paired with that region's inflation through a Phillips curve; at least one. Written as {defaults, countries}, like interest_rates.")
    yield_curve: YieldCurveConfig = Field(default_factory=YieldCurveConfig)
    credit_term_structure: CreditTermStructureConfig = Field(default_factory=CreditTermStructureConfig)
    hjm: HjmConfig = Field(default_factory=HjmConfig)
    real_estate: RealEstateConfig = Field(default_factory=RealEstateConfig)
    credit: list[CreditConfig] = Field(default_factory=list, description='Credit spreads by maturity, rating bucket or country; none by default.')
    leading_indicator: LeadingIndicatorConfig = Field(default_factory=LeadingIndicatorConfig)
    credit_migration: CreditMigrationConfig = Field(default_factory=CreditMigrationConfig)
    climate: ClimateConfig = Field(default_factory=ClimateConfig)
    fx: list[FXConfig] = Field(default_factory=list, description='Exchange rates against the US dollar, one per currency; none by default.')
    commodities: list[CommodityConfig] = Field(default_factory=list, description='Commodities, each mean-reverting in its log price, as in Schwartz (1997); none by default.')
    dividend_yield: list[DividendYieldConfig] = Field(default_factory=list, description="Dividend yields, each mean-reverting in its log, as in Ahlgrim, D'Arcy and Gorvett (2005); none by default.")
    dividend_growth: list[DividendGrowthConfig] = Field(default_factory=list, description='Dividend growth as in Wilkie (1986), each tied to an inflation and a dividend_yield entry; none by default.')
    mortality: MortalityConfig = Field(default_factory=MortalityConfig)
    correlations: CorrelationsConfig = Field(default_factory=CorrelationsConfig, description='Correlations stated as values instead of estimated from history; none by default.')
    published_model: Literal['ahlgrim', 'hibbert', 'wilkie'] | None = Field(default=None, description="Reproduce this published model as its paper ran it, with no data: every parameter comes from the factor set's beliefs and every starting value from the paper (Ahlgrim, D'Arcy and Gorvett's workbook, Hibbert, Mowbray and Turnbull's calibration A, Wilkie's neutral start), so calibration needs no Finance Toolkit and the run is the same offline. The factor set must state every parameter of the model; unemployment may then be left out, as Hibbert's and Wilkie's models have none. None (the default) fits every factor on its history.")
    toolkit: ToolkitConfig = Field(default_factory=ToolkitConfig)
    external_scenario_source: ExternalScenarioSourceConfig = Field(default_factory=ExternalScenarioSourceConfig)
```

</details>

#### ScenariosConfig.factor_categories

Every factor this configuration simulates, mapped to its category ("equities", "inflation", ...).

It covers every name a simulated run holds, including the helper series some models add next to the factor you
configured: a two-factor commodity's short- and long-term components ("commodities_state") and the moving
long-run target of a two-factor rate or inflation ("interest_rates_target", "inflation_target").

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
scenariosconfig.factor_categories  # property -> dict[str, str]
```

**Returns:**

<u>dict[str, str]:</u> factor name -> category.

</details>

#### ScenariosConfig.factor_labels

Every factor's display name for charts and tables, such as "Inflation — United States" or "US Broad — Equity".

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
scenariosconfig.factor_labels  # property -> dict[str, 'FactorLabel']
```

**Returns:**

<u>dict[str, FactorLabel]:</u> factor name -> display label, for the same names as `factor_categories`.

</details>

#### ScenariosConfig.describe

What this configuration would simulate, one row per category, before any data is fetched or fitted.

It sits next to `CalibrationResult.describe()` (what the fit said) and `ScenarioSet.describe()` (where the run
landed).

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
describe() -> pl.DataFrame
```

**Returns:**

<u>pl.DataFrame:</u> "category", "n_factors", "factors" (comma-separated names, in configuration order), sorted by category.

</details>

#### ScenariosConfig.with_equity

Return a copy of this configuration with one more equity added, such as a sector or regional ETF.

Each equity is its own correlated factor in the run, fitted to its ticker's history and named by `name`, the
name you use for it in portfolios, regimes and results. The configuration you call this on is left as it was,
so several variants can be built from one base. Any other equity setting (`period`, `currency`, `method`,
`beliefs`, ...) can be passed by keyword, as in an `equities` entry of a factor set.

The new configuration is checked like any other: a name already used by another factor raises, as it would
when written in a factor set.

**As an example:**

```python
import polars as pl

from financescenarios import load_profiles

config = load_profiles(factor_set_id="default").with_equity("tech", "XLK")
config.describe().filter(pl.col("category") == "equities")
```

Which returns:

| category | n_factors | factors |
|:---------|----------:|:--------|
| equities | 6 | us_broad, small_cap, europe, japan, emerging_markets, tech |

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
with_equity(name: str, ticker: str, **fields: Any) -> 'ScenariosConfig'
```

**Args:**

- <u>name (str):</u> the factor's name, e.g. "tech"; unique across all factors.
- <u>ticker (str):</u> the ticker to fit it to, e.g. "XLK".
- <u>fields (Any):</u> any other `EquityConfig` setting, e.g. `period="weekly"`.

**Returns:**

<u>ScenariosConfig:</u> a new configuration with the equity appended to `equities`.

**Raises:**

- <u>pydantic.ValidationError:</u> if the name is already used, or a setting is unknown or does not fit.

</details>

#### ScenariosConfig.tickers

Every market ticker this configuration downloads history for: the rates, equities, commodities and dividend
series, the Treasury yields behind a yield curve or a risk-neutral forward curve, and any extra tickers.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
scenariosconfig.tickers  # property -> list[str]
```

**Returns:**

<u>list[str]:</u> the unique tickers, in the order they first appear.

</details>

### Configuration Classes

#### EngineConfig

How a run is simulated: how many scenarios, how many steps of what length, and how the random shocks are drawn.

More scenarios make percentiles and averages more precise (the error of an average shrinks with the square root of
the count), at a cost in time and memory. The shocks are what makes the scenarios differ, and their shape sets the
tails: Gaussian by default, or Student-t (`shock_distribution: student_t`) for fat tails in which large moves are
more frequent and tend to hit several markets at once. Antithetic sampling pairs every scenario with its mirror
image, which measures averages more precisely for the same number of scenarios without changing the model.

The correlations that tie the factors together are estimated from their historical changes, each pair on the
history the two share, and pulled toward zero by an amount set by the data (`correlation_shrinkage`), since a
correlation estimated from a few years of data is noisy and the noise is worst in the extremes.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
class EngineConfig(_StrictModel):
    n_simulations: int = Field(gt=0, le=100000, default=1000, description='The number of scenarios to simulate.')
    n_steps: int = Field(gt=0, le=10000, default=52, description='The number of time steps in each scenario.')
    frequency: str = Field(default='weekly', description=f'The length of one step, one of {list(FREQUENCY_TO_TIME_STEP)}.')
    seed: int | None = Field(default=None, description='Fix it to get the same scenarios on every run.')
    antithetic: bool = Field(default=False, description='Pair every scenario with its mirror image (the opposite shocks), which measures averages more precisely for the same number of scenarios. n_simulations must be even.')
    shock_distribution: Literal['gaussian', 'student_t'] = Field(default='gaussian', description="'gaussian' (the default) or 'student_t', whose fat tails make extreme moves more frequent and more likely to hit several factors at once. Each factor's volatility means the same either way; only the shape of the tails changes.")
    degrees_of_freedom: float = Field(default=12.0, gt=2, description="Student-t degrees of freedom, only used when shock_distribution='student_t'. Lower means fatter tails and stronger tail dependence; must be > 2 for finite variance. The default is the fit of Kole, Koedijk and Verbeek (2007, Table 2: nu = 12.1) to daily stock, government bond and real estate returns (https://doi.org/10.1016/j.jbankfin.2006.09.010); 4-6 fits hourly to daily currency returns.")
    correlation_method: Literal['pairwise', 'complete_case'] = Field(default='pairwise', description="How the correlations are estimated. 'pairwise' (the default) uses each pair's own shared history, so one factor with a short history only affects its own pairs; a pair that overlaps too little is set to 0 and listed in correlation_fallback_pairs. 'complete_case' cuts every factor to the one window they all share, which gives a consistent matrix but lets a single short history shrink every estimate. Pairwise is the practice Higham (2002, section 1) describes for stock correlations: each pair's sample correlation uses only the days on which both stocks have data, and the result is then repaired to the nearest valid matrix (https://doi.org/10.1093/imanum/22.3.329).")
    correlation_shrinkage: float | Literal['auto'] = Field(default='auto', description="How much the sample correlation matrix is shrunk before use. 'auto' (the default) shrinks toward no correlation by the data-driven intensity of Schafer and Strimmer (2005, section 2.4, target D, eq. 10, which shrinks the off-diagonal entries to zero), larger when correlations rest on few observations (https://doi.org/10.2202/1544-6115.1175). A number in [0, 1] instead blends the matrix that far toward its own average correlation (0.1 was the earlier default), Ledoit and Wolf's (2004) target, which they rule out for assets from different classes such as stocks and bonds (footnote 4, https://doi.org/10.3905/jpm.2004.110): rates, inflation, equities and FX are such a mix.")
    shared_equity_regimes: bool = Field(default=False, description="Draw every regime-switching equity's regime changes from one shared stream of random numbers instead of one stream each, so markets tend to enter and leave their crisis regimes together, as they do. Each entry keeps its own fitted transition probabilities, so the paths still differ where those differ. Without it, independent regime paths dilute the simulated correlation between equities: on the core factor set the mean gap to the calibrated correlations fell from 0.094 to 0.044.")
```

</details>

##### EngineConfig.time_step

Time increment per step, in years, derived from `frequency`.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
engineconfig.time_step  # property -> float
```

</details>

#### ToolkitConfig

Settings for the embedded Finance Toolkit `Toolkit` instance: Finance Scenarios'
sole calibration data source. `Scenarios.from_config_file()`/`from_config()` build
this `Toolkit` automatically; a caller never constructs one directly.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
class ToolkitConfig(_StrictModel):
    start_date: date | None = Field(default=None, description='Start of the historical data window pulled for calibration.')
    end_date: date | None = Field(default=None, description="End of the historical data window pulled for calibration (default: today). Useful to cap a calibration window before a specific event, e.g. an interest_rates[] entry with method='wilkie_consols' assumes the inflation-adjusted real yield stays positive throughout the fit window, an assumption that broke down during the 2020-2022 COVID/ZIRP era; capping end_date before that period keeps the model usable as a legacy calibration.")
    extra_tickers: list[str] = Field(default_factory=list, description='Tickers to include beyond interest_rates[i].ticker/equities[i].ticker, e.g. for a factor with no dedicated config field yet.')
    benchmark_ticker: str | None = Field(default=None, description="FinanceToolkit's benchmark ticker. Left as None by default since FinanceToolkit silently drops a ticker from the list when it matches the benchmark.")
    progress_bar: bool = False
```

</details>

#### InterestRateConfig

One interest rate in the run: a country's short or long rate, fitted to its history and simulated as its own
correlated factor. `ScenariosConfig.interest_rates` holds one or more of these, at least one.

By default the rate is mean-reverting (Hull-White): pulled toward a long-run level at its historical speed, with
shocks of its historical size, and free to go negative, as euro, yen and Swiss franc rates did. The data comes
from a Treasury-yield ticker (`source: ticker`, US), the OECD's short and long rates (`source: oecd`, worldwide) or
the Global Macro Database (`source: gmdb`, more countries, yearly only); `history_source` can fit the speed and
level on more than a century of data instead. The default factor set goes further: its short rates follow the
balanced-approach rule from the market's expected path (`policy_rule: balanced`, `expected_path: market`) and its
long rates are their short rate's expected path plus a term premium (`expectations_hypothesis: true`).

The model can be changed with `method`:

- `hull_white` (default): mean-reverting, can go negative.
- `cir`: shocks shrink as the rate nears zero, so it stays positive.
- `wilkie_consols`: Wilkie's (1986) long yield, expected inflation plus a real yield. It assumes real yields stay
  positive, which US long yields broke from 2008 to 2017, so end the data window in 2007 (`settings/wilkie`).
- `hibbert_two_factor`: the short rate reverts to a long rate that itself moves, so the whole level of rates can drift
  for years. Hibbert, Mowbray and Turnbull (2001, section 5.1.1) model the real short rate this way and add inflation
  on top; here the structure is applied to the nominal rate, an approximation.
- `knw` and `knw_sv`: the rate and a paired inflation entry are fitted jointly, as in De Nederlandsche Bank's
  scenario set; `knw_sv` adds a stochastic volatility the two share, which an equity can join.
- `cp2022`: a zero rate of De Nederlandsche Bank's own model, CP2022, with the parameters DNB publishes every
  quarter (`Cp2022`); `maturity` (1 to 100 years) and `curve` (`nominal` or the euro-area `real` curve) pick it.
  Every `cp2022` entry of a run, inflation and equity included, is one output of the same model.

Other options shape the economics further. `volatility_model: garch` lets calm and turbulent periods alternate.
`condition_on_business_cycle` tilts the rate with the leading indicator. `long_run_anchor` pulls the rate toward
EIOPA's forward rates (the Solvency II reference) or the median of DNB's scenario set instead of its own fitted
level. `real_rate` models the real rate instead and adds simulated inflation to it, the Fisher construction of
Ahlgrim, D'Arcy and Gorvett (2005) and Hibbert, Mowbray and Turnbull (2001). `zero_lower_bound` floors it at 0%.
`beliefs` overrides the fit with your own view (see
`InterestRateBeliefs`). Only `hull_white` and `cir` take `condition_on_business_cycle`, a `history_source` or a
`long_run_anchor`, only `hull_white` takes `volatility_model: garch`, and beliefs apply to constant-volatility,
real-world `hull_white` and `cir` entries. `knw` and `knw_sv` pair one rate with one inflation entry: both set the
same method and name each other, at the same `period`.

`policy_rule` makes a short rate follow a monetary-policy rule instead of one long-run level. Each step it closes
part of its gap to the rate the rule prescribes for the scenario's simulated inflation (`inflation_name`) and
unemployment (`unemployment_name`): the neutral real rate plus inflation, plus 0.5 times inflation's gap to
`inflation_target`, minus 1 (`taylor`, Taylor (1993, p. 202, eq. 1)) or 2 (`balanced`) times unemployment's gap to
`longer_run_unemployment`, as in the Federal Reserve's Monetary Policy Report (2026, Box 4, Table A). The rate
never goes below `effective_lower_bound`, while a shadow rate underneath keeps following the rule (Black (1995)),
so a deep recession holds the rate at the floor until the rule climbs back above it. The floor defaults to the
lowest policy rate each central bank has set: 0% for USD (the Federal Reserve's 0 to 0.25% target range of
2008-2015 and 2020-2022), -0.50% for EUR (the ECB's deposit facility rate, 18 September 2019 to 27 July 2022) and
0.10% for GBP (Bank Rate, 19 March 2020 to 16 December 2021); 0% elsewhere. The speed of that partial adjustment,
as in Clarida, Galí and Gertler (2000), is the Federal Reserve's inertial rule's (`policy_rule_speed: inertial`,
0.85 of last quarter's rate kept, Board of Governors (2018, table "Examples of Policy Rules")): 0.65 a year, a gap
halving in about a year; `fitted` fits it on history, falling back to the inertial speed when the rate shows no
adjustment. `policy_rule_weights: fitted` fits the rule's weights too, on the rate's own history with its paired
inflation and unemployment as the simulation reads them (Clarida, Galí and Gertler (2000, section II, eqs.
(1)-(4)), by least squares), jointly with the speed, which must then be `fitted`; when a response is not
significant at 5% or has the wrong sign, or the rate closes no gap to any rule, the published weights stay. Only
the volatility is always fitted, leaving out the months the rate was held at its floor while the rule prescribed
less. The target is 2% for the Federal Reserve (2026, Statement on Longer-Run Goals,
paragraph 4), the ECB (2021, strategy statement, paragraph 5) and the Bank of England (HM Treasury (2025), remit
letter). The neutral real rate defaults to 1.2% for USD (the FOMC's Summary of Economic Projections, September
2026, Table 1: a longer-run federal funds rate of 3.2% less 2% inflation), 0.09% for EUR (the Holston, Laubach and
Williams (2023) model's euro-area estimate for 2026Q2) and 1.0% for GBP (a judgement: the midpoint of the range in
the Bank of England's Monetary Policy Report (2025, Box A)). The longer-run unemployment defaults to the official
estimate for the paired unemployment entry's country: 4.2% for the United States (the same Table 1), and the
European Commission's NAWRU for 2027 for France (7.16%), the United Kingdom (4.21%) and Germany (3.48%) (AMECO,
variable ZNAWRU, Spring 2026 forecast); elsewhere it is that entry's fitted level of the same kind. The paired
unemployment entry settles at that level in a long calm stretch, the FOMC's reading of its longer-run projections
as the values reached in the absence of further shocks (SEP, note to Table 1), and averages the recessions' push
above it; with that entry's `natural_rate_anchor: average` the level is its average over the cycle instead, the
zero-mean gap the European Commission builds its NAWRU on (Havik et al. (2014, section 2.4.2)). Either way its
speed, inflation sensitivity and volatility stay as fitted, and a `long_run_mean` belief on it still wins
(`UnemploymentConfig`). The rule measures slack from that level, the textbook unemployment gap. A calibration as
of a past date (`Scenarios.out_of_sample`) reads each of these values as it was published by then: in 2007 the New
York Fed's Laubach and Williams estimate of 2.14% for the US neutral rate and the Congressional Budget Office's
5.0% natural rate, for example (`dated_values_model.value_as_of`). The rule takes precedence over
`long_run_anchor` and `history_source`, and needs a real-world `hull_white` short rate with constant volatility
and no `condition_on_business_cycle`; no inflation entry may condition on it.

`expected_path: market` starts the rule's expected path from the market instead of the rule's own
prescription. A rule pulls the rate toward the neutral real rate plus the target within a year or two, as that
target was estimated at the time, while markets can expect something else for years, as they priced rates near
zero for years ahead from 2009 on. The expected path is then the one the government curve's forward rates
implied on the calibration date, less the term premium of Adrian, Crump and Moench (2013, section 2.4), as the
New York Fed estimates it for each maturity: for the dollar the curve is the New York Fed's own fit of the Treasury
zero-coupon curve, the yields that premium is estimated on (the Treasury par curve, bootstrapped, with no premium
taken out when it cannot be read); for the euro the Bundesbank's zero-coupon curve of Federal securities and for
the pound the Bank of England's gilt spot curve. No official premium is published for the euro or the pound, so
each gets its own: the same regressions run on its own month-end curve over its OECD 3-month rate, as Malik and
Meldrum (2016) run them on the gilt curve; the Treasury premium stands in only when that fit cannot be made, as
term premia have moved together across countries (Wright (2011); Jotikasthira, Le and Lundblad (2015)).
For a dollar rate on the 13-week bill (`^IRX`) the path past today is quoted as the bill's bank discount rate,
the basis `^IRX` quotes (the US Treasury's Daily Treasury Bill Rates), 7 basis points below the curve's
continuously compounded rate at 4%, so the path starts on the basis of today's rate.
That path is read for ten years, the longest maturity the premium is estimated for, and then closes its gap to the
rule's steady state at the short rate's own speed of mean reversion, the speed its expectations long rate reads it
with, so both describe one expected path (Vasicek (1977, section 5, eq. 25)). The rule still sets how the rate
responds: it acts on the gaps of each scenario's inflation and unemployment to their expected paths, with its
weights, speed, volatility and floor unchanged, so what the market already priced in is not counted twice, and a
scenario whose inflation and unemployment follow their expected paths follows the market's path. The expected
paths are the calibrated model's median inflation and unemployment without regimes, beliefs or shocks (the median,
as inflation's rare spikes lift its average above where most scenarios are), worked out once at calibration from a
baseline run of 4,000 scenarios and stored with it. They are fixed functions of time, as the deterministic shift
of Brigo and Mercurio (2001) is, so a regime, a belief or a shock that lifts inflation in every scenario lifts the
rate's target by 1 + a times as much (1.5 with the published weights), and each scenario's rate answers its own
gaps whatever the number of scenarios. A
calibration saved before they were stored reads each step's median across the run's own scenarios instead, with
a warning: a move common to every scenario then moves that median too and the rule does not answer it. While the
market path holds, the level the rule measures slack from cancels out of its target, so
`longer_run_unemployment` only sets where the paired unemployment entry settles; it applies again when the rate
falls back to the rule's own path. An
`expectations_hypothesis` long rate on such a short rate reads the same path: the path's average over its
maturity, plus the share of the short rate's gap to the path still expected. A calibration as of a past date
reads the curve and the premium of that date; the premium is the New York Fed's current estimate, fitted on the
whole sample. Without a curve the rate follows the rule's own path, with a warning and a calibration note.

Beliefs keep their meaning on a policy-rule rate. A `long_run_mean` path (`BeliefPath`) prescribes the rate up to
its last anchor, as a supervisory stress scenario prescribes the policy rate: the Federal Reserve's 2026 severely
adverse scenario takes the 3-month Treasury rate from 3.7% to 0.1% within half a year (Board of Governors of the
Federal Reserve System (2026, p. 14)). Up to that anchor the rate is pulled toward the path instead of the rule's
rate, at the rule's speed, with the path interpolated as on any rate; after it the rule sets the rate again, at
once or, with `converge_over_years`, handing over in a straight line over that many years. One `long_run_mean`
for the whole run would switch the rule off for good, so it is refused: `neutral_real_rate` moves where the rule
settles. A shock moves the shadow rate, so the floor still holds, and the rate closes it at the rule's speed;
`mean_reversion_speed` and `volatility` replace the rule's speed and the fitted volatility.

References for `policy_rule`:

- Taylor (1993): https://doi.org/10.1016/0167-2231(93)90009-L
- Federal Reserve, Monetary Policy Report July 2026: https://www.federalreserve.gov/monetarypolicy/2026-07-mpr-part2.htm
- Clarida, Galí and Gertler (2000): https://doi.org/10.1162/003355300554692
- FOMC, Statement on Longer-Run Goals: https://www.federalreserve.gov/monetarypolicy/files/fomc_longerrungoals.pdf
- ECB strategy statement (2021): https://www.ecb.europa.eu/home/search/review/html/ecb.strategyreview_monpol_strategy_statement.en.html
- HM Treasury remit letter (2025): https://www.gov.uk/government/publications/monetary-policy-remit-budget-2025/letter-from-chancellor-of-the-exchequer-to-govenor-of-the-bank-of-england
- FOMC, Summary of Economic Projections, September 2026: https://www.federalreserve.gov/monetarypolicy/fomcprojtabl20260916.htm
- New York Fed, Holston, Laubach and Williams estimates: https://www.newyorkfed.org/research/policy/rstar
- European Commission, AMECO NAWRU (ZNAWRU): https://ec.europa.eu/economy_finance/ameco/wq/series?fullVariable=1.0.0.0.ZNAWRU&countries=FRA,GBR,DEU&years=2027&lastYear=0&yearOrder=ASC
- European Commission, AMECO unemployment rate (ZUTN): https://ec.europa.eu/economy_finance/ameco/wq/series?fullVariable=1.0.0.0.ZUTN&countries=FRA,GBR,DEU&years=2025&lastYear=0&yearOrder=ASC
- Congressional Budget Office, Budget and Economic Data (noncyclical rate of unemployment): https://www.cbo.gov/data/budget-economic-data
- Bureau of Labor Statistics, unemployment rate (LNS14000000): https://data.bls.gov/timeseries/LNS14000000
- Bank of England, Monetary Policy Report February 2025: https://www.bankofengland.co.uk/monetary-policy-report/2025/february-2025
- Federal Reserve, Policy Rules and How Policymakers Use Them (2018), inertial rule: https://www.federalreserve.gov/monetarypolicy/policy-rules-and-how-policymakers-use-them.htm
- Black (1995): https://doi.org/10.1111/j.1540-6261.1995.tb05182.x
- Federal Reserve, 2026 Final Supervisory Stress Test Scenarios: https://www.federalreserve.gov/publications/files/2026-final-supervisory-stress-test-scenarios-20260204.pdf
- Federal Reserve, open market operations (target ranges): https://www.federalreserve.gov/monetarypolicy/openmarket.htm
- ECB, key interest rates (deposit facility -0.50%, 2019-2022): https://www.ecb.europa.eu/stats/policy_and_exchange_rates/key_ecb_interest_rates/html/index.en.html
- Bank of England, Bank Rate history (0.10%, 2020-2021): https://www.bankofengland.co.uk/boeapps/database/Bank-Rate.asp

References for `expected_path: market`:

- Adrian, Crump and Moench (2013): https://doi.org/10.1016/j.jfineco.2013.04.009
- Federal Reserve Bank of New York, Treasury term premia (ACM): https://www.newyorkfed.org/research/data_indicators/term-premia-tabs
- Wright (2011): https://doi.org/10.1257/aer.101.4.1514
- Jotikasthira, Le and Lundblad (2015): https://doi.org/10.1016/j.jfineco.2014.09.004
- Malik and Meldrum (2016): https://doi.org/10.1016/j.jbankfin.2016.02.006
- Vasicek (1977): https://doi.org/10.1016/0304-405x(77)90016-2
- Kozicki and Tinsley (2001): https://doi.org/10.1016/s0304-3932(01)00054-x
- Brigo and Mercurio (2001): https://doi.org/10.1007/pl00013541
- U.S. Department of the Treasury, Daily Treasury Bill Rates (bank discount rate): https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_bill_rates&field_tdr_date_value=202610
- Schich (1997), Deutsche Bundesbank Discussion Paper 4/97: https://www.bundesbank.de/resource/blob/622394/ab816caf466eeea7dd2fef26d0fbfc30/mL/1997-10-01-dkp-04-data.pdf

`expectations_hypothesis` builds a long rate on its short rate (`short_rate_name`) in each scenario: the short
rate expected over the long rate's maturity, from the short rate's own speed and long-run level (its anchor or
policy rule included), plus a term premium, as in Campbell and Shiller (1991, section 2, eq. 1). Two rates that
each revert on their own, linked only by correlated shocks, let the gap between them wander, so a curve that
inverts can stay inverted for decades; with the long rate built on the short rate, the curve inverts when the
short rate jumps and steepens again as it falls back. The term premium reverts toward a long-run level and moves
with the short rate's gap to its own long-run level, fitted on the entry's history (its `history_source` when
set); `term_premium` sets that long-run level instead. The expected path takes precedence over the long rate's
own `long_run_anchor`: with EIOPA anchors the long rate settles near EIOPA's 10-year forward rate plus the
premium, and `term_premium: 0` keeps it near the forward rate. A `long_run_mean` path on the long rate prescribes
it up to its last anchor, as a stress scenario prescribes the 10-year yield: the long rate is pulled toward the
path at the term premium's speed, and after the last anchor (or over `converge_over_years`) it follows its short
rate's expected path plus the premium again; a path on the short rate moves that expected path with it, while
the premium still reads the short rate's gap to the policy rule's steady state, as fitted, so a higher prescribed
short rate lifts the long rate. One `long_run_mean` for the whole run is refused, since `term_premium` sets where
the premium settles. A shock jumps the long rate through its term premium, which then reverts at its own speed.
With `total_move` (see `InterestRateBeliefs`) the shocks are the yield's whole move from its starting level
instead: the long rate is held there plus the shocks so far until the last one, as a path prescribes it, so a
regime that sets the short rate's path and states the 10-year's recorded move counts that move once.

On a policy-rule short rate the expected path settles at the rule's steady state but reverts at the short rate's
own speed, a Hull-White fit on the data the premium is fitted on: the rule's speed (0.65 a year) is how fast the
rate closes its gap to a target that inflation and unemployment keep moving, not how long a gap lasts. On the
OECD's yearly rates from 1950 to 2025 that speed is 0.114 a year for the US, 0.192 for Germany and 0.099 for the
UK, so a 10-year yield carries 0.60, 0.44 and 0.63 of a short-rate move rather than 0.15; the New York Fed's
expected average short rate over ten years (ACMRNY10, the risk-neutral yield of Adrian, Crump and Moench (2013,
section 2.4)) loads 0.59 on the 3-month bill, monthly from June 1961 to September 2026. Its term premium also
moves with the short rate's change in the same step (gamma), fitted on the same data: -0.107 for the US, -0.082
for Germany and -0.255 for the UK, as ACM's premium falls 0.12 for every point the bill rises in yearly-average
changes from 1962 to 2025, so a short-rate jump moves the 10-year by D + gamma at once. The calibration notes
record the speed, the data it comes from and gamma.

Yearly averages smooth away part of the premium's moves, so a premium fitted on them and simulated a month at a
time moves less than history's did. `history_period: monthly` fits it a month at a time instead, on the series the
run simulates: the OECD's monthly rates (Germany from 1960, the United Kingdom's short rate only from 1986) or,
with `history_source: ticker`, the long rate's ticker and its short rate's further back (`^TNX` on `^IRX` from
1962, as the OECD's monthly US short rate is an interbank rate, not the bill). On the dollar's month-ends from 1962
to 2025 the premium reverts at 0.45 a year to 1.45%, with beta 0.37, gamma -0.19 and a volatility of 0.0095
against 0.0068 on the same years' averages; simulated monthly it reproduces history's 12-month moves in the long
rate (1.14 points against 1.15) and its spread to the bill (1.27 against 1.25), and refitted monthly it gives each
parameter back, as one fitted on yearly averages does not. On out-of-sample backtests from 2000 to 2022, though,
it lowered the long rates' skill on the 18 origins no choice was made on (US +0.24 to +0.19, euro +0.19 to +0.10,
UK +0.23 to +0.13), so the default keeps the yearly fit.

References for `expectations_hypothesis`:

- Campbell and Shiller (1991): https://doi.org/10.2307/2298008
- Adrian, Crump and Moench (2013): https://doi.org/10.1016/j.jfineco.2013.04.009
- Federal Reserve Bank of New York, Treasury term premia (ACM): https://www.newyorkfed.org/research/data_indicators/term-premia-tabs

For a market-consistent valuation, `measure: risk_neutral` with `risk_neutral_forward_curve: true` makes the rate
reproduce today's Treasury curve, or EIOPA's risk-free curve with `risk_neutral_curve: eiopa`, rather than
history; `Scenarios.simulate(measure="risk_neutral")` sets up the EIOPA version for you.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
class InterestRateConfig(_StrictModel):
    name: str = 'interest_rate'
    source: Literal['ticker', 'oecd', 'gmdb'] = Field(default='ticker', description="'ticker' (a Yahoo Finance Treasury-yield ticker, US only), 'oecd' (the OECD short- or long-term rate of country, monthly, quarterly or yearly) or 'gmdb' (the Global Macro Database, which covers countries outside the OECD, yearly only).")
    currency: str = Field(default='USD', description="The currency this rate belongs to, a three-letter ISO code such as 'EUR'. Used to convert results into the reporting currency and to pick long_run_anchor's curve.")
    measure: Literal['real_world', 'risk_neutral'] = Field(default='real_world', description="'real_world' (fitted on history, the default) or 'risk_neutral' (matched to today's market: a flat path at today's rate, or today's forward curve with risk_neutral_forward_curve). A risk_neutral entry takes no beliefs.")
    method: Literal['hull_white', 'cir', 'wilkie_consols', 'hibbert_two_factor', 'knw', 'knw_sv', 'cp2022'] = 'hull_white'
    ticker: str = Field(default='^IRX', description="With source='ticker': the Treasury-yield ticker, e.g. ^IRX (13-week), ^FVX (5-year), ^TNX (10-year) or ^TYX (30-year).")
    country: str = Field(default='United States', description="With source 'oecd' or 'gmdb' (or a history_source): the country.")
    term: Literal['short', 'long'] = Field(default='short', description="With source 'oecd' or 'gmdb': the short-term or the long-term rate.")
    period: str = Field(default='daily', description='The frequency of the history the rate is fitted on: any for a ticker, monthly, quarterly or yearly for oecd, yearly for gmdb. Left unset, it is daily for a ticker, monthly for oecd and yearly for gmdb.')
    volatility_model: Literal['constant', 'garch'] = Field(default='constant', description="'constant' (the default) or 'garch' (GARCH(1,1) time-varying volatility of Bollerslev (1986)); 'garch' needs method='hull_white'.")
    condition_on_business_cycle: bool = Field(default=False, description="Add an additive drift term on the leading indicator's step-to-step change (business-cycle conditioning). Requires leading_indicator.enabled=true; incompatible with volatility_model='garch'.")
    risk_neutral_forward_curve: bool = Field(default=False, description="With measure='risk_neutral' and method='hull_white': simulate a Hull-White rate whose drift reproduces today's forward curve (from the four Treasury tenors), with speed and volatility fitted on history, instead of a flat path at today's rate.")
    risk_neutral_curve: Literal['treasury', 'eiopa'] = Field(default='treasury', description="With risk_neutral_forward_curve: the curve the rate reproduces. 'treasury' (the default) fits Nelson-Siegel to the four Treasury tenors; 'eiopa' takes EIOPA's risk-free curve for this entry's currency (USD, EUR or GBP), the curve Solvency II's best estimate discounts with. Simulate(measure='risk_neutral') picks 'eiopa' for those currencies.")
    risk_neutral_volatility_fit: Literal['yield_curve', 'short_rate'] = Field(default='yield_curve', description="With risk_neutral_forward_curve: where the Hull-White volatility comes from. 'yield_curve' (the default) fits it to how much yields at several maturities have moved; 'short_rate' takes the short rate's own historical volatility. The speed is the short rate's historical speed either way.")
    inflation_name: str = Field(default='inflation', description="With method 'wilkie_consols', 'knw' or 'knw_sv': the name of the inflation entry this rate is paired with. A wilkie_consols rate is fitted at that entry's period.")
    inflation_weight: float = Field(default=1.0, description="With method='wilkie_consols': Wilkie's CW, the weight on inflation; fixed, not fitted. Wilkie (1986, section 3.15) sets CW = 1.0.")
    inflation_decay: float = Field(default=0.05, gt=0, lt=1, description="With method='wilkie_consols': Wilkie's CD, how fast past inflation fades; fixed, not fitted. Wilkie (1986, section 3.15, Reduced Standard Basis) sets CD = 0.05.")
    target_source: Literal['long_term_rate', 'ewma'] = Field(default='long_term_rate', description="With method='hibbert_two_factor': what the rate reverts toward. 'long_term_rate' (the default) fetches the same country's long rate (target_term or target_ticker) and simulates it as a second factor, '<name>_target'; 'ewma' uses a moving average of this rate's own path (target_smoothing) instead.")
    target_term: Literal['short', 'long'] = Field(default='long', description="With target_source='long_term_rate' and source 'oecd' or 'gmdb': the target's term, which must differ from term (the same term would be the same series).")
    target_ticker: str = Field(default='^TNX', description="With target_source='long_term_rate' and source='ticker': the target's ticker, which must differ from ticker.")
    target_smoothing: float = Field(default=0.05, gt=0, lt=1, description="With target_source='ewma': the weight of each new observation in the moving average; smaller is a slower target. Fixed, not fitted.")
    history_source: Literal['millennium', 'jst', 'oecd', 'ticker'] | None = Field(default=None, description="Fit the dynamics (speed, volatility, long-run level) on decades or centuries of history instead of the recent window, at the maturity term names; today's level and the correlation series still come from source. 'oecd': the OECD's short- or long-term rate of country, yearly from 1950 (monthly from the 1950s or 1960s with history_period: monthly); 'millennium': the Bank of England's Bank Rate from 1694 or long government bond (consols) yields (country 'United Kingdom'); 'jst': the Jordà-Schularick-Taylor bill return of country from 1870, short only (needs accept_licence); 'ticker': an expectations_hypothesis long rate's own ticker and its short rate's, the instruments the run simulates, from Yahoo Finance's first closes (^IRX 1960, ^TNX 1962). Real-world hull_white or cir with constant volatility only.")
    history_start_year: int | None = Field(default=None, description='With history_source: leave out years before this one, e.g. 1900.')
    history_period: Literal['yearly', 'monthly'] = Field(default='yearly', description="With history_source on an expectations_hypothesis long rate: how often its long history is sampled for the term premium's fit. 'yearly' (default) reads one value a year (the OECD's yearly average, a ticker's year-end close); 'monthly' reads one a month (the OECD's monthly rates, a ticker's month-end closes), the step a monthly run simulates, since a yearly average smooths away part of the premium's month-to-month moves and of its same-step response to the short rate. 'oecd' or 'ticker' only.")
    accept_licence: bool = Field(default=False, description="Confirms non-commercial use, which history_source 'jst' requires (CC BY-NC-SA 4.0).")
    real_rate: bool = Field(default=False, description="Model the real rate and add inflation to it: the process (hull_white or hibbert_two_factor) is fitted on the rate minus the paired inflation entry (`inflation_name`), the ex-post real rate of Ahlgrim, D'Arcy and Gorvett (2005, section 3), and a hibbert_two_factor target likewise on the long rate minus inflation; the simulated rate is that real rate plus the scenario's simulated inflation each step, so nominal rates and inflation move together, as their nominal rate is real rate plus inflation (eq. 3.15) and as in Hibbert, Mowbray and Turnbull (2001, section 5.1.4). Beliefs then state the real rate's process, and the fitted parameters are the real rate's. Off by default: the nominal rate is fitted and simulated itself.")
    lower_bound: float | None = Field(default=None, description="The lowest rate recorded, as zero_lower_bound records 0: the process evolves underneath and the rate every path and linked factor sees is max(rate, lower_bound), such as Wilkie's (1986, section 4.5) minimum Consols yield CMIN of 0.5%. None (the default) leaves the rate unfloored. Real-world entries only.")
    zero_lower_bound: bool = Field(default=False, description='Keep this rate at or above 0%, as some scenario generators do. The model still evolves underneath as a shadow rate that may go negative, with every negative rate replaced by zero, as in Black (1995); the rate every path, discount factor and linked factor sees is max(shadow, 0), so a rate that touched zero climbs back from where the shadow went rather than from 0. Off by default: negative rates did happen (euro, yen, Swiss franc). Real-world entries only.')
    history_volatility: Literal['history', 'recent'] = Field(default='history', description="With history_source: 'history' (default) takes the volatility from the long history along with the speed and level; 'recent' keeps the volatility fitted on the recent window, so a calm or volatile recent era sets how much the rate swings while the long history sets how fast it reverts.")
    long_run_anchor: Literal['eiopa', 'dnb'] | None = Field(default=None, description="Pull the rate toward an official curve's forward rates instead of one fitted long-run level: 'eiopa' uses EIOPA's risk-free curve for this entry's currency (USD, EUR or GBP), the 1-year forward rate for term short and the 10-year forward for term long, starting at every scenario date, ending at EIOPA's ultimate forward rate (Solvency II's reference). 'dnb' (EUR only) follows the median of De Nederlandsche Bank's real-world scenario set instead, its 1-year or 10-year nominal rate, the reference for Dutch pension funds. Speed and volatility stay fitted. An explicit beliefs.long_run_mean takes precedence. hull_white or cir, real_world, constant volatility only.")
    policy_rule: Literal['none', 'taylor', 'balanced'] = Field(default='none', description="Pull the rate toward the rate a monetary-policy rule prescribes for each scenario's simulated inflation (inflation_name) and unemployment (unemployment_name) instead of one long-run level: 'taylor' (Taylor (1993)) or 'balanced' (the Federal Reserve's balanced-approach rule, twice the weight on unemployment). The speed is the Federal Reserve's inertial rule's (policy_rule_speed) and the volatility is fitted on history given the rule. Takes precedence over long_run_anchor and history_source. A real-world hull_white short rate with constant volatility, without condition_on_business_cycle. A beliefs.long_run_mean path prescribes the rate up to its last anchor, after which the rule sets it again; shocks move the shadow rate.")
    policy_rule_speed: Literal['inertial', 'fitted'] = Field(default='inertial', description="With policy_rule: how fast the rate closes its gap to the rule. 'inertial' (default) takes the Federal Reserve's inertial rule, 0.85 of last quarter's rate kept, 0.65 a year; 'fitted' fits it on history and falls back to the inertial speed, with a warning, when the rate shows no adjustment.")
    policy_rule_weights: Literal['published', 'fitted'] = Field(default='published', description="With policy_rule: where the rule's weights on inflation and unemployment come from. 'published' (default) takes the rule's (0.5 and 1 for taylor, 0.5 and 2 for balanced); 'fitted' fits them on the rate's own history with its paired inflation and unemployment, the partial-adjustment rule of Clarida, Galí and Gertler (2000), jointly with the speed (policy_rule_speed: fitted), and keeps the published weights, with a warning, when a response is not significant at 5% or has the wrong sign.")
    unemployment_name: str = Field(default='unemployment', description="With policy_rule: the unemployment entry the rule reads; a country entry defaults to its own country's, e.g. 'eurozone_unemployment'.")
    inflation_target: float = Field(default=0.02, description="With policy_rule: the central bank's inflation target, as a decimal; 2% for the Federal Reserve, the ECB and the Bank of England.")
    neutral_real_rate: float | None = Field(default=None, description="With policy_rule: the real rate that neither stimulates nor restrains the economy. Left unset, the central bank's own estimate for currency: USD 1.2%, EUR 0.09%, GBP 1.0%.")
    longer_run_unemployment: float | None = Field(default=None, description="With policy_rule: the official natural rate of unemployment; the paired unemployment entry settles at it in a calm stretch (or averages it over the cycle, with that entry's natural_rate_anchor: average). Left unset, the official estimate for that entry's country (United States 4.2%, the FOMC's longer-run median; France 7.16%, United Kingdom 4.21%, Germany 3.48%, the European Commission's NAWRU), otherwise the entry's fitted calm level. With expected_path: market the rule's gap is measured from unemployment's expected path instead, so this only sets where unemployment settles.")
    effective_lower_bound: float | None = Field(default=None, description="With policy_rule: the floor under the simulated rate, while its shadow rate keeps following the rule. Left unset, the lowest policy rate the currency's central bank has set: USD 0%, EUR -0.50% (the ECB's deposit facility rate), GBP 0.10% (Bank Rate); 0% for other currencies.")
    expected_path: Literal['rule', 'market'] = Field(default='rule', description="With policy_rule: where the rate's expected path comes from. 'rule' (default) is the rule's own prescription; 'market' is the path the government curve's forward rates implied on the calibration date (the New York Fed's fit of the Treasury curve for USD, the Bundesbank's curve for EUR, the Bank of England's gilt curve for GBP), less an ACM term premium (the New York Fed's for USD; for EUR and GBP one fitted on that same curve, with the US premium only as a fallback), converging to the rule's steady state after ten years, with the rule acting on the gaps of the simulated inflation and unemployment to their expected paths: the calibrated model's medians without regimes, beliefs or shocks, stored at calibration. longer_run_unemployment then only sets where unemployment settles, as the level slack is measured from cancels out. USD, EUR or GBP.")
    expectations_hypothesis: bool = Field(default=False, description="With term='long': make this long rate the short rate expected over its maturity plus a mean-reverting term premium fitted on history, so the gap between the two reverts as it has historically instead of wandering. The expected path follows short_rate_name's own model, its long-run anchor or policy rule included (a policy rule's path reverts at the short rate's own speed on the premium's history, not the rule's, and its premium also reads the short rate's same-step change), and takes precedence over this entry's own long_run_anchor. A real-world hull_white rate with constant volatility, without condition_on_business_cycle. A beliefs.long_run_mean path prescribes the long rate up to its last anchor, after which its short rate's expected path and the premium set it again; shocks move the term premium, or with beliefs.total_move are the yield's whole move from its start.")
    short_rate_name: str = Field(default='interest_rate', description="With expectations_hypothesis: the short-rate entry whose expected path the long rate follows; a country entry defaults to its own country's, e.g. 'eurozone_short_rate'.")
    term_premium: float | None = Field(default=None, description="With expectations_hypothesis: the term premium's long-run level as a decimal, in place of the fitted one; 0 makes the long rate settle where the short rate's expected path averages.")
    maturity: int = Field(default=1, ge=1, le=100, description="With method='cp2022': the maturity of the zero rate in years, 1 to 100.")
    curve: Literal['nominal', 'real'] = Field(default='nominal', description="With method='cp2022': the nominal euro curve or the euro-area real (HICP-linked) curve.")
    beliefs: InterestRateBeliefs = Field(default_factory=InterestRateBeliefs)
```

</details>

#### InflationConfig

One country's consumer price inflation, fitted to its history and simulated as its own correlated factor.
`ScenariosConfig.inflation` holds one or more of these, at least one.

By default inflation is mean-reverting (an Ornstein-Uhlenbeck process, as in Ahlgrim, D'Arcy and Gorvett (2005)):
pulled back toward a long-run rate at its historical speed, so a spike fades over a few years rather than becoming
the new normal, and deflation is possible but rare. The data is the OECD's consumer price index (`source: oecd`,
monthly to yearly) or the Global Macro Database (`source: gmdb`, more countries, yearly only).

The model can be changed with `method`:

- `ou` (default): mean-reverting toward one long-run rate.
- `wilkie_ar1`: Wilkie's (1986) original inflation model, a simple autoregression.
- `hibbert_two_factor`: inflation reverts to an "expected inflation" level that itself moves (Hibbert, Mowbray
  and Turnbull (2001)), so inflation regimes can persist for years.
- `regime_switching`: inflation moves between a calm regime and a high, volatile one, each with its own level and
  shock size (Hamilton (1989)), so a 1970s or a 2021-22 can start from a calm today; fit it on the OECD's history
  since 1956 with `history_source: oecd`. Its long-run mean is anchored to the country's sourced long-run
  expectation by moving both regimes' levels (`long_run_anchor`), so the regimes stay as far apart as history
  put them. Where the high regime of a long record cannot meet the expectation with a calm level of zero or more,
  as on the UK's record since 1956, the calm level stops at zero and the mean stays above the expectation, with a
  warning; `history_start_year` fits the regimes on the current monetary regime only instead,
  as [Benati (2008, section 2.1.1 and Appendix B.3)](https://www.ecb.europa.eu/pub/pdf/scpwps/ecbwp851.pdf) reads
  inflation's persistence regime by regime (the UK's inflation targeting from 8 October 1992).
- `knw` and `knw_sv`: fitted jointly with a paired interest rate, as in De Nederlandsche Bank's scenario set.
- `cp2022`: the inflation of De Nederlandsche Bank's CP2022 model with its quarterly parameters (`Cp2022`):
  `index: hicp` for the euro area's, `index: dutch_cpi` for the Dutch CPI, the HICP's plus a spread that
  follows CPB's forecasts.

`volatility_model: garch` lets calm and turbulent periods alternate, `condition_on_business_cycle` tilts inflation
with the leading indicator, `condition_on_interest_rate` lets it respond to changes in a paired rate, and `beliefs`
overrides the fit with your own view, such as a central bank's 2% target (see `OUBeliefs`). These options apply
to `ou` only, and GARCH entries keep their fitted parameters. `regime_switching` takes two beliefs, in the
long-run mean's terms: `long_run_mean`, one level or a `BeliefPath`, moves both regimes' levels by its gap to
the anchored mean, so the mean follows it (interpolated, held after the last anchor or converging back with
`converge_over_years`, as on an `ou` entry) while the regimes keep their gap, shocks and switching; and `shocks`
jump inflation, which then reverts at the regimes' own speed. Its speed and shock sizes stay as fitted.

Under `measure: risk_neutral`, a `knw_sv` entry takes the pair's market-consistent fit, and an `ou` entry moves
around the market's breakeven inflation curve (nominal minus inflation-linked bond yields) of the United States,
the United Kingdom, Germany or the euro area, read with no API key, with the speed and volatility of its own
history (`source` and `period`), so its expected price index matches the curve and caps and floors on indexation
get a time value; `risk_neutral_volatility: none` follows the curve exactly instead.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
class InflationConfig(_StrictModel):
    name: str = 'inflation'
    country: str = Field(default='United States', description='The country whose consumer price inflation to fit.')
    source: Literal['oecd', 'gmdb'] = Field(default='oecd', description="'oecd' (the OECD consumer price index, monthly, quarterly or yearly) or 'gmdb' (the Global Macro Database, which covers countries outside the OECD, yearly only).")
    currency: str = Field(default='USD', description='The currency of this inflation series, a three-letter ISO code; used when converting results.')
    measure: Literal['real_world', 'risk_neutral'] = Field(default='real_world', description="'real_world' (fitted on history, the default) or 'risk_neutral', with method 'knw_sv' (the market-consistent fit of the pair) or 'ou' (today's breakeven inflation curve of the United States, the United Kingdom, Germany or the euro area). A risk_neutral entry takes no beliefs.")
    period: str = Field(default='monthly', description='The frequency of the history inflation is fitted on: monthly, quarterly or yearly.')
    method: Literal['ou', 'wilkie_ar1', 'hibbert_two_factor', 'regime_switching', 'knw', 'knw_sv', 'cp2022'] = Field(default='ou', description="'ou' (mean-reverting, the default), 'wilkie_ar1' (the AR(1) of Wilkie (1986)), 'hibbert_two_factor' (reverts to a moving target, see target_source), 'regime_switching' (a calm and a high, volatile regime, Hamilton (1989); fit it on a long history with history_source), 'knw' (jointly fitted with interest_rate_name's rate) or 'knw_sv' (knw with stochastic volatility). Only 'ou' takes GARCH, conditioning or beliefs.")
    target_source: Literal['coarser_period', 'ewma'] = Field(default='coarser_period', description="With method='hibbert_two_factor': what inflation reverts toward. 'coarser_period' (the default) fetches the same country's inflation at target_period and simulates it as a second factor, '<name>_target'; 'ewma' uses a moving average of this entry's own path (target_smoothing) instead.")
    target_period: Literal['quarterly', 'yearly'] = Field(default='yearly', description="With target_source='coarser_period': the target's frequency, coarser than period (monthly allows quarterly or yearly, quarterly only yearly). Growth over a longer window is larger, so the fitted reversion speed has no direct years-to-close-the-gap reading.")
    target_smoothing: float = Field(default=0.05, gt=0, lt=1, description="With target_source='ewma': the weight of each new observation in the moving average; smaller is a slower target. Fixed, not fitted.")
    tips_breakeven_decay: float = Field(default=0.7308, gt=0, description="With measure='risk_neutral' and method='ou': the Nelson-Siegel decay (lambda) of the breakeven curve fit, the same default as yield_curve: Diebold and Li's (2006) 0.0609 a month x 12.")
    risk_neutral_volatility: Literal['history', 'none'] = Field(default='history', description="With measure='risk_neutral' and method='ou': 'history' (the default) makes inflation random around the breakeven curve, with the speed and volatility of its own history (source and period), so caps and floors on indexation get a time value; 'none' follows the breakeven curve exactly in every scenario.")
    volatility_model: Literal['constant', 'garch'] = Field(default='constant', description="'constant' (the default) or 'garch' (GARCH(1,1) time-varying volatility of Bollerslev (1986)).")
    condition_on_business_cycle: bool = Field(default=False, description="Add an additive drift term on the leading indicator's step-to-step change (business-cycle conditioning). Requires leading_indicator.enabled=true; incompatible with volatility_model='garch'.")
    condition_on_interest_rate: bool = Field(default=False, description="Add a drift term on the step-to-step change of interest_rate_name's rate, a modelling judgement that inflation moves with the paired nominal rate (fitted, not imposed). Not with volatility_model='garch' or condition_on_business_cycle, since the fit takes one covariate.")
    interest_rate_name: str = Field(default='interest_rate', description="With condition_on_interest_rate or method 'knw' or 'knw_sv': the name of the interest_rates entry this inflation is paired with.")
    ou_fit: Literal['year_apart', 'step'] = Field(default='year_apart', description="How the 'ou' fits (constant, garch or conditioned) and both 'hibbert_two_factor' legs read persistence: 'year_apart' (the default) regresses each value on the value a year earlier, since neighbouring monthly year-over-year rates share 11 months; 'step' on the previous observation, the fit before October 2026, which reads that overlap as slow mean reversion. Yearly data give the same result.")
    history_source: Literal['millennium', 'shiller', 'oecd'] | None = Field(default=None, description="Fit the dynamics (speed, volatility, long-run level) on centuries of history instead of the recent window; today's level and the correlation series still come from source. 'millennium': UK consumer price inflation from 1210 (country 'United Kingdom'); 'shiller': US December-to-December inflation from 1872 (country 'United States'); 'oecd': the OECD's inflation of country at this entry's period, from 1956 for the major economies, read a year apart. Real-world ou with constant volatility, wilkie_ar1, whose yearly AR(1) is then fitted on that history as Wilkie (1986) fitted his on UK data from 1919, or regime_switching, whose regimes are fitted on it.")
    history_start_year: int | None = Field(default=None, description='With history_source: leave out years before this one, e.g. 1900.')
    long_run_anchor: Literal['expectations', 'fitted'] | None = Field(default=None, description="With method='regime_switching': 'expectations' (the default) moves both regimes' levels so the long-run mean is today's sourced long-run expectation for the country (US 2.30%, the Philadelphia Fed's Survey of Professional Forecasters; euro area 2.0%, the ECB's; UK 2%, the Bank of England's target), keeping the gap between them, and reads today's regime off the recent data again with the moved levels; 'fitted' keeps the history's own levels. A beliefs.long_run_mean (one level or a path) then moves both levels from there, so the long-run mean follows it.")
    index: Literal['hicp', 'dutch_cpi'] = Field(default='hicp', description="With method='cp2022': the euro-area HICP or the Dutch CPI, which follows the HICP plus a spread set by CPB's forecasts (Technical Appendix, sec. 8).")
    beliefs: OUBeliefs = Field(default_factory=OUBeliefs)
```

</details>

#### UnemploymentConfig

Unemployment factor settings: one entry per country. `ScenariosConfig.unemployment` holds at least one; each entry
becomes its own correlated factor, keyed by `name`, mean-reverting with a Phillips-curve term on the inflation entry
named by `inflation_name` (Ahlgrim, D'Arcy and Gorvett (2005, eq. 3.19)). It has no `period` of its own: it is
fitted at that inflation entry's period, which must be yearly for `source: gmdb`.

Two opt-in cycle links make unemployment answer to the rest of the scenario. With `condition_on_equity` it rises
after the `equity_name` market's return over the past year falls short of normal (read three months on); a
rally does not speed its fall, which comes from its own pull back to normal, so it rises fast and falls slowly, as
Neftçi (1984) and Sichel (1993) find. With `condition_on_term_spread` it rises after the curve between
`long_rate_name` and `short_rate_name` flattens below its average of the five years before (read six months on).
Both are fitted on December-to-December changes (OECD unemployment, inflation and rates since 1955, Shiller's S&P
Composite total return) on what unemployment's own level and inflation leave unexplained, following Okun (1962,
p. 99), Estrella and Hardouvelis (1991, section II.C, p. 559) and Estrella and Mishkin (1998, p. 50); see
`Unemployment.calibrate_cycle_links`. With the equity link the long-run mean stays unemployment's average over the
cycle and it settles lower while markets are calm (4.3% on US history, against an average of 5.8%); a policy rule's
natural rate places either level (`natural_rate_anchor`). The equity link needs
`country: United States`, the only keyless history long enough; a `countries[]` entry's rate names default to its
own country's `<name>_short_rate` and `<name>_long_rate`. Each link reads values from earlier steps only, so it
fixes no simulation order and cannot form a loop with a rate that reads unemployment.

`history_source: oecd` fits the speed, natural rate, Phillips-curve sensitivity and volatility on the OECD's
December-to-December changes since 1955 instead of the recent window (`Unemployment.calibrate_history`): fitted
since 2000, April 2020 alone quadruples the volatility and puts scenarios below 3.4%, the lowest US rate since 1955,
in one month in seven.

`regime_switching` gives unemployment an expansion, in which it drifts down to a calm level, and a recession, in
which it rises sharply, switching as a Markov chain: Hamilton's (1989) model, fitted by maximum likelihood on the
OECD's monthly history (`Unemployment.calibrate_regimes`). On US data since 1956 recessions take 13% of months and
last ten months on average, against 12% and 10.3 months for the NBER's recessions since 1955. The cycle links then
move the chance of a recession starting instead of pushing unemployment themselves, so a run's recessions come as
often as its own market falls or its own curve flattens below its recent average. The long-run mean is the
average over expansions and recessions, and expansions settle below it. A `long_run_mean` belief, one level or a
`BeliefPath`, sets that average the same way, moving both regimes' levels with it, so the average over the cycle
follows the path while recessions still push above it; `shocks` jump the rate, which then reverts at its fitted
speed in whichever regime each scenario is.

Either option replaces the window's own fit, so a window that shows no pull toward a normal level (one that ends
in a surge, as at the end of 2009) no longer fails the entry: it keeps today's rate and the window's series, which
a policy rule reads, with a calibration note.

An entry a policy-rule rate reads is placed against that rule's official natural rate (its
`longer_run_unemployment`), and `natural_rate_anchor` says which level the official rate is. With `calm` (the
default) it is the level unemployment settles at in a long calm stretch, the FOMC's reading of its longer-run
projection as the rate reached in the absence of further shocks (SEP, note to Table 1), and recessions lift the
average over the cycle above it by the fitted push. That is the plucking model of [Dupraz, Nakamura and Steinsson
(2019, sections 1 and 2.2)](https://doi.org/10.3386/w26351): unemployment's fluctuations are rises above a resting
point of low unemployment, not symmetric swings around a natural rate. With `average` the official rate is
unemployment's average over the cycle, the calm level sitting the push below it: the European Commission's NAWRU
is estimated so that the unemployment gap averages zero over the cycle ([Havik et al. (2014, section
2.4.2)](https://ec.europa.eu/economy_finance/publications/economic_paper/2014/pdf/ecp535_en.pdf)). On the US
regimes since 1984 that puts the calm level at 2.7% and a quarter of a run's months below 3.4%, the lowest US rate
since 1969, where `calm` keeps it to 4%; on the whole US record since 1956 the calm reading averages 6.0%, against
5.8% in the data. A calibration as of a past date reads the official rate as published by then.

`history_start_year` fits the long-history dynamics, the regimes or the cycle links on the years from then on
only. On the OECD's US record since 1956 recessions push the average 1.8 points above the calm level; on the Great
Moderation era from 1984, the break [McConnell and Perez-Quiros (2000)](https://doi.org/10.1257/aer.90.5.1464) and
[Stock and Watson (2002, section 3)](https://doi.org/10.1086/ma.17.3585284) date to 1984:I, it is 1.5 points. With
the calm reading the shorter sample only narrows the bands: on backtests from 2000 to 2022 the US 90% coverage
fell from 0.70 to 0.62 at the same skill, so the default set fits on the whole history.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
class UnemploymentConfig(_StrictModel):
    name: str = 'unemployment'
    country: str = 'United States'
    source: Literal['oecd', 'gmdb'] = Field(default='oecd', description="'oecd' (FinanceToolkit's OECD unemployment rate, worldwide within the OECD roster) or 'gmdb' (its Global Macro Database; covers countries outside the OECD roster; requires the paired inflation[i].period to be 'yearly', since this entry has no period of its own).")
    inflation_name: str = Field(default='inflation', description="Which configured inflation[i].name drives this entry's Phillips-curve term.")
    condition_on_business_cycle: bool = Field(default=False, description="Add a second drift term, on the leading indicator's step-to-step change, next to the inflation term. Requires leading_indicator.enabled=true, with leading_indicator.period equal to the paired inflation entry's period.")
    condition_on_equity: bool = Field(default=False, description="Let unemployment rise after the equity_name market's past-year return falls short of normal (rallies do not speed its fall), with a sensitivity fitted on US history since 1955; the long-run mean stays the average over the cycle. Requires equity_name and country='United States'.")
    equity_name: str | None = Field(default=None, description='With condition_on_equity: the real-world equities[i].name whose return drives it.')
    condition_on_term_spread: bool = Field(default=False, description="Let unemployment rise after the curve between long_rate_name and short_rate_name flattens below its average of the five years before, half a year later, fitted on the country's OECD history since 1955.")
    short_rate_name: str | None = Field(default=None, description="With condition_on_term_spread: the short interest_rates[i].name; a countries[] entry defaults to its own '<name>_short_rate'.")
    long_rate_name: str | None = Field(default=None, description="With condition_on_term_spread: the long interest_rates[i].name; a countries[] entry defaults to its own '<name>_long_rate'.")
    history_source: Literal['oecd'] | None = Field(default=None, description="Fit the speed, natural rate, Phillips-curve sensitivity and volatility on the OECD's December-to-December changes since 1955 instead of the recent window, so one extraordinary month (April 2020) cannot set them; today's rate still comes from source. Not with condition_on_business_cycle.")
    regime_switching: bool = Field(default=False, description="Give unemployment an expansion and a recession regime (Hamilton 1989), fitted on the OECD's monthly history since 1955; condition_on_equity and condition_on_term_spread then move the chance of a recession starting. Not with condition_on_business_cycle. A beliefs.long_run_mean (one level or a path) moves both regimes' levels, so the average over the cycle follows it.")
    history_start_year: int | None = Field(default=None, ge=1956, description="With history_source, regime_switching or a cycle link: fit them on the OECD's history from this year on, e.g. 1984 for the US Great Moderation or 1993 for the UK's inflation-targeting era; the signals still read the months before it. None (the default) takes the whole history, from 1955.")
    natural_rate_anchor: Literal['calm', 'average'] = Field(default='calm', description="With a policy-rule rate reading this entry: which level that rule's official natural rate (longer_run_unemployment) sets. 'calm' (default): the level reached in a long calm stretch, the FOMC's longer-run rate without further shocks, so recessions lift the average above it, as unemployment is plucked up from a floor near the natural rate (Dupraz, Nakamura and Steinsson (2019, sections 1 and 2.2)); 'average': the average over the cycle, as the European Commission's NAWRU is estimated with a gap that averages zero (Havik et al. (2014, section 2.4.2)), with the calm level the recessions' push below it, which on the US regimes since 1984 puts a quarter of a run's months below 3.4%, the lowest US rate since 1969.")
    beliefs: UnemploymentBeliefs = Field(default_factory=UnemploymentBeliefs)
```

</details>

#### EquityConfig

One equity market in the run: a broad index, a sector, a region or a style, each from one ticker and simulated as
its own correlated factor. `ScenariosConfig.equities` holds one or more of these, at least one.

By default the returns switch between regimes, as in Hardy (2001): a calm one with steady gains and a turbulent one
with losses and high volatility, each fitted to the ticker's history along with how often the market moves between
them. This gives what a single bell curve misses: crashes cluster, volatility stays high once it rises, and the
distribution of returns has a fat left tail. `shared_equity_regimes` in the engine settings makes markets enter and
leave their turbulent regime together. `condition_on_inflation` makes the turbulent regime far more likely when the
simulated inflation of `inflation_name` runs high, as in Filardo (1994): stocks earned a negative real return in
years with inflation above 5%. The regimes stay the ticker's own; how strongly inflation moves them is read from
US history since `inflation_history_start_year` through those regimes (`inflation_history`). Under
`shared_equity_regimes` every inflation-conditioned entry still switches on the shared draws, each with its own
odds. `regime_history` takes how often and how long the market is calm or turbulent from a long index of it
(Ken French's US market since 1926, or since `inflation_history_start_year` with inflation-driven switching; the
Nikkei 225 since 1965), at the ticker's own average return and
volatility, since a fund's twenty years hold too few bear markets to pin that down. For the same reason
`expected_return: risk_free_plus_premium` replaces that average return with the simulated short rate plus a long-run
premium (`equity_premium`, by default the 3.77% a year stocks earned above bills across 16 countries from 1870 to
2015 in Jordà, Knoll, Kuvshinov, Schularick and Taylor (2019, Table II)), keeping the regimes as fitted.

Other methods tie equities to the rest of the economy: `wilkie_derived` builds the price from a dividend index and a
dividend yield as in Wilkie (1986), `hibbert_regime_switching` fits the regimes to returns in excess of a short rate,
so equities earn a premium over cash, `knw_sv` shares stochastic volatility with rates and inflation, and `cp2022`
is the equity index of De Nederlandsche Bank's CP2022 model, with the parameters DNB publishes (`Cp2022`). Under
`measure: risk_neutral` the market earns the risk-free rate less its dividend yield, with a volatility from option
prices. `asset_class` stands in a listed fund for an asset class without a public index, such as private equity or
infrastructure. `beliefs` overrides the fit with your own view (see `EquityBeliefs`).

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
class EquityConfig(_StrictModel):
    name: str = 'equity'
    ticker: str = 'SPY'
    asset_class: str | None = Field(default=None, description="An asset class without a public return index, e.g. 'Private Equity', 'Infrastructure', 'Hedge Funds' or 'Private Credit' (a key of ASSET_CLASS_PROXIES): sets ticker to the listed fund the Finance Toolkit's economics.get_asset_class_proxies uses for it. Listed prices are marked to market daily, so they swing more and move more with equities than the appraisal-based returns private funds report, and they are net of the fund's fees.")
    currency: str = Field(default='USD', description='The currency the ticker is listed in, which is not always the market it tracks (VGK and EWJ are USD-listed); used when converting results.')
    measure: Literal['real_world', 'risk_neutral'] = Field(default='real_world', description="'real_world' (fitted on history, the default) or 'risk_neutral' (geometric Brownian motion growing at the risk-free rate minus the dividend yield, with the volatility from volatility_source). A risk_neutral entry takes no beliefs.")
    volatility_source: Literal['implied', 'svi', 'realized', 'heston'] = Field(default='implied', description="Only used when measure='risk_neutral': where the flat GBM volatility comes from. 'implied' (default) averages the Black-Scholes implied volatilities of the out-of-the-money call and put nearest today's price, at the first expiration at least a week away. 'svi' reads the ATM value off FinanceToolkit's SVI-fitted, calendar-arbitrage-checked volatility surface (options.get_volatility_surface) at the longest fitted expiration: smoothed across the whole smile instead of passing one quote's noise straight through, and a longer expiry is the better match for a GBM simulated over years. 'realized' skips options data entirely and uses the annualized standard deviation of historical log-returns (the right choice for tickers without a liquid options market, e.g. most sector/regional/style ETFs). 'heston' fits the Heston (1993) stochastic-volatility model to the SVI surface at six expirations from one to twelve months, so the simulated paths carry the market's smile and volatility term structure instead of one flat volatility. 'implied', 'svi' and 'heston' fall back to realized volatility (flat GBM) with a logged warning when options data is unavailable.")
    n_regimes: int = Field(gt=1, default=2)
    period: str = 'monthly'
    method: Literal['regime_switching', 'wilkie_derived', 'hibbert_regime_switching', 'knw_sv', 'cp2022'] = Field(default='regime_switching', description="'regime_switching' (a Markov regime-switching fit, the default), 'wilkie_derived' (Wilkie (1986): the price is dividend_growth_name's dividend index over dividend_yield_name's yield, with no fit of its own), 'hibbert_regime_switching' (Hibbert, Mowbray and Turnbull (2001): regimes fitted to returns in excess of nominal_rate_name's rate) or 'knw_sv' (DNB's KNW model: returns earn nominal_rate_name's rate plus a fitted premium, with the rate's stochastic volatility). All but 'regime_switching' are real-world only.")
    dividend_growth_name: str | None = Field(default=None, description="Required when method='wilkie_derived'. Which configured dividend_growth[i].name this entry's price numerator reads.")
    dividend_yield_name: str | None = Field(default=None, description="Required when method='wilkie_derived'. Which configured dividend_yield[i].name this entry's price denominator reads.")
    nominal_rate_name: str | None = Field(default=None, description="Required with method 'hibbert_regime_switching' or 'knw_sv': the name of the interest_rates entry whose rate the returns are measured over, at the same period. For 'knw_sv' that entry must use method='knw_sv' too. With expected_return 'risk_free_plus_premium' it names the short rate the premium is earned over (any period), defaulting to the run's short rate in this entry's currency.")
    condition_on_business_cycle: bool = Field(default=False, description="Let the odds of switching regime depend on the leading indicator, as in Filardo (1994), instead of a drift term as for other factors. Requires leading_indicator.enabled=true, method='regime_switching' and leading_indicator.period equal to engine.frequency.")
    condition_on_inflation: bool = Field(default=False, description="Let the odds of switching regime follow the level of inflation_name's simulated inflation, as in Filardo (1994): high inflation makes the turbulent regime far more likely. The regimes are ticker's own; how strongly inflation moves them is read from US history (inflation_history) from inflation_history_start_year. Requires method='regime_switching', measure='real_world', period and engine.frequency 'monthly'; not with condition_on_business_cycle or history_source.")
    inflation_name: str = Field(default='inflation', description="With condition_on_inflation: the inflation entry whose level drives the switching, e.g. 'united_states_inflation'. It needs period 'monthly' and a method other than 'knw' or 'knw_sv'.")
    inflation_history: Literal['us_market', 'us_small_caps'] = Field(default='us_market', description="With condition_on_inflation: the US history the inflation sensitivity is read from, through this entry's own regimes: 'us_market' (the CRSP value-weighted market from Ken French's data library, for broad indices) or 'us_small_caps' (the market plus the size factor SMB, for small-cap tickers such as IWM).")
    inflation_history_start_year: int = Field(default=_INFLATION_HISTORY_START_YEAR, ge=1872, description='With condition_on_inflation: the first year of the US history the inflation sensitivity is read from. 1946 (the default) leaves out the deflation of the 1930s, when stocks fell as prices fell.')
    regime_history: Literal['us_market', 'us_small_caps', 'europe', 'japan', 'emerging_markets'] | None = Field(default=None, description="Fit how often and how long the market is calm or turbulent on a long index history instead of the ticker's own: 'us_market' (the CRSP US market from Ken French's data library, from 1926), 'us_small_caps' (the same plus the size factor SMB), 'europe' (Ken French's European market in US dollars, from 1990), 'japan' (the Nikkei 225, from 1965) or 'emerging_markets' (Ken French's emerging markets in US dollars, from 1989). The switching is held at the index's and each regime's mean and volatility are fitted on the ticker by maximum likelihood (Hardy (2001), https://doi.org/10.1080/10920277.2001.10595984). Real-world, monthly regime_switching only. With condition_on_inflation it must name the same US history as inflation_history, and the regimes and their switching are read from it from inflation_history_start_year. None (the default) fits everything on the ticker.")
    history_source: Literal['shiller', 'jst'] | None = Field(default=None, description="Fit the regimes on long history instead of the ticker's: 'shiller' is the US S&P Composite total return, monthly from 1871; 'jst' the yearly equity total return of history_country from 1870 (needs accept_licence). Today's price and the correlation series still come from ticker. Real-world regime_switching without condition_on_business_cycle or condition_on_inflation only.")
    history_country: str = Field(default='United States', description="The JST country for history_source 'jst'.")
    history_start_year: int | None = Field(default=None, description='With history_source: leave out years before this one, e.g. 1950.')
    accept_licence: bool = Field(default=False, description="Confirms non-commercial use, which history_source 'jst' requires (CC BY-NC-SA 4.0).")
    expected_return: Literal['sample', 'risk_free_plus_premium'] = Field(default='sample', description="'sample' (the default) keeps the average return of the ticker's own years. 'risk_free_plus_premium' earns the simulated short rate plus equity_premium instead: every regime mean moves by the same amount, so the regimes, their volatilities and their switching stay as fitted. With switching that follows inflation, the premium is earned on average over the regime shares a pilot run of the inflation entry gives (simulated moments, McFadden (1989), https://doi.org/10.2307/1913621), more in calm-inflation years and less in high-inflation ones. The short rate is nominal_rate_name, or else the run's short rate in this entry's currency (the US rate for a USD-listed VGK, since in dollars a European fund earns dollar cash plus the European premium when currencies follow interest parity); if that rate fails to calibrate, the entry keeps its sample return for the run, with a warning and a calibration note. Real-world regime_switching only.")
    equity_premium: float | None = Field(default=None, gt=-0.5, lt=0.5, description="With expected_return 'risk_free_plus_premium': the long-run geometric (compound) return above the short rate, as a decimal. None uses 0.0377, the equity return above bills across 16 countries from 1870 to 2015 in Jordà, Knoll, Kuvshinov, Schularick and Taylor (2019, Table II).")
    beliefs: EquityBeliefs = Field(default_factory=EquityBeliefs)
```

</details>

#### FXConfig

Exchange rate settings: opt-in, one entry per currency (an empty `fx` list simulates none). Each entry is a
geometric Brownian motion on one currency's exchange rate against the US dollar, from end-of-period BIS rates or
OECD averages (`source: oecd`, monthly at the finest) or the Global Macro Database (`source: gmdb`, yearly only),
correlated with the rest of the model. `drift_mode` picks where the trend comes from; `ppp` also pulls the real
exchange rate back toward parity over a few years.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
class FXConfig(_StrictModel):
    name: str = 'fx'
    country: str = Field(default='EA20', description="The country (or currency area) whose currency is paired against the US dollar. The OECD exchange-rate series is keyed by currency area, not member state: 'EA20' is the euro area, and an individual member ('Germany', 'France', ...) has no series of its own there, unlike interest_rates/inflation/unemployment, which do take a member state's name.")
    currency: str | None = Field(default=None, description="The ISO code of the currency this pair quotes against the dollar, e.g. 'EUR'. Read by financescenarios.reporting to convert into that currency. When unset it is taken from an interest_rates/inflation entry with the same country, or 'EUR' for the OECD's euro-area codes ('EA20', 'EA19', 'Euro Area').")
    source: Literal['oecd', 'gmdb'] = Field(default='oecd', description="'oecd' (FinanceToolkit's OECD exchange rate, period='monthly'/'quarterly'/'yearly') or 'gmdb' (its Global Macro Database; covers countries outside the OECD roster, period='yearly' only).")
    period: str = 'monthly'
    measure: Literal['real_world', 'risk_neutral'] = Field(default='real_world', description="'real_world' (fitted on history, the default) or 'risk_neutral' (the no-arbitrage drift in the US dollar measure of Garman and Kohlhagen (1983), https://doi.org/10.1016/S0261-5606(83)80001-1: each step the foreign minus the US short rate simulated by this run's interest_rates entries for both currencies, plus the variance, so a foreign deposit converted to dollars and discounted at the US rate keeps its value on average; with the historical volatility). A risk_neutral entry takes no beliefs.")
    drift_mode: Literal['historical', 'irp', 'random_walk', 'ppp'] = Field(default='random_walk', description="'random_walk' (the default) keeps the historical volatility but drops the trend, so the median rate stays at today's level instead of extrapolating the sample's appreciation, as in Meese and Rogoff (1983), https://doi.org/10.1016/0022-1996(83)90017-X; exchange rates hold to purchasing power parity at long horizons in Hibbert, Mowbray and Turnbull (2001, section 9.3). 'historical' carries the fitted drift forward (7.1% a year for the yen on 2021-2026 data, a currency view no provider builds in); 'irp' (uncovered interest rate parity, a real-world view) makes each step's drift the difference between the simulated foreign_rate_name and domestic_rate_name rates; measure='risk_neutral' is its covered-parity counterpart, for pricing. 'ppp' (purchasing power parity at long horizons) keeps the random walk's volatility, moves the rate with the gap between the simulated foreign_inflation_name and domestic_inflation_name inflation and pulls the real exchange rate toward ppp_anchor with a half-life of ppp_half_life years, Rogoff (1996, section 5.B, p. 656), https://ideas.repec.org/a/aea/jeclit/v34y1996i2p647-668.html.")
    ppp_half_life: float = Field(default=PPP_HALF_LIFE_YEARS, gt=0, description="With drift_mode='ppp': the years for half of a deviation from purchasing power parity to fade. 4 is the middle of the three to five years the long-horizon studies agree on in Rogoff (1996, section 5.B, p. 656).")
    ppp_anchor: Literal['history', 'today'] = Field(default='history', description="With drift_mode='ppp': the level the real exchange rate reverts to. 'history' (the default) is its average since toolkit.start_date, the rate adjusted by the OECD consumer price indices of the two inflation entries' countries, the purchasing power parity level of Rogoff (1996, section 5); without both entries, or without a price index reaching to within a year of the last rate, it warns and uses today's. 'today' reverts to today's real rate: no view on whether the dollar is dear. The historical anchor is uncertain: a 26-year average of a real rate with a four-year half-life is known only to about sigma / (kappa * sqrt(T)) = 0.1 in logs, about as far as the euro and the pound sit from it, so today's level is within one standard error.")
    end_of_period: bool = Field(default=True, description="Fit on the rate at the end of each period (BIS) rather than its average: changes of averages keep about two-thirds of a random walk's variance (Working (1960), https://doi.org/10.2307/1907574). With source 'gmdb', which has averages only, the volatility is scaled up by that factor instead. False fits the OECD or GMDB averages as they are.")
    domestic_rate_name: str | None = Field(default=None, description="Required with drift_mode='irp': the name of the interest_rates entry for the US dollar leg.")
    foreign_rate_name: str | None = Field(default=None, description="With drift_mode='irp': the name of the interest_rates entry for the foreign leg; by default '<country>_short_rate', e.g. 'japan_short_rate' for country 'Japan'.")
    domestic_inflation_name: str | None = Field(default=None, description="With drift_mode='ppp': the inflation entry for the US dollar leg; by default the run's United States inflation entry.")
    foreign_inflation_name: str | None = Field(default=None, description="With drift_mode='ppp': the inflation entry for the foreign leg; by default the inflation entry of this pair's currency. Without both entries the inflation gap is zero and the real rate reverts to today's.")
    beliefs: FXBeliefs = Field(default_factory=FXBeliefs)
```

</details>

#### CreditConfig

Credit factor settings: opt-in, one entry per credit spread (an empty `credit` list simulates none). Each entry is
a mean-reverting process on one spread series, correlated with the rest of the model; `dimension` picks the series.
Belief overrides only apply when `volatility_model` is "constant".

| dimension | Series | Coverage |
|:----------|:-------|:---------|
| `maturity`, `rating` | ICE BofA option-adjusted spread by maturity or rating bucket | United States, daily |
| `moodys` | Moody's Aaa or Baa yield over the 10-year Treasury, or Baa minus Aaa | United States, from 1953 |
| `corporate` | Corporate bond spread over government bonds, per `country` | Germany, Australia, monthly |
| `borrowing_cost` | ECB cost of new bank loans to companies, a rate level | Euro area or a member, monthly |

There is no euro or UK spread by rating: those indices are licensed data.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
class CreditConfig(_StrictModel):
    name: str = 'credit'
    currency: str = Field(default='USD', description="The spread's currency: USD for the US sources, defaulting to EUR for 'corporate' Germany and 'borrowing_cost', AUD for 'corporate' Australia. Read by financescenarios.reporting.")
    dimension: Literal['maturity', 'rating', 'moodys', 'corporate', 'borrowing_cost'] = Field(default='maturity', description="Which spread to fit: the ICE BofA option-adjusted spread by 'maturity' (uses maturity_bucket, one of credit_controller.MATURITY_BUCKETS) or by 'rating' (uses rating_bucket, one of credit_controller.RATING_BUCKETS), both with three years of history on FRED; or 'moodys': Moody's Aaa or Baa yield over the 10-year Treasury, or Baa minus Aaa (rating_bucket one of credit_controller.MOODYS_BUCKETS), monthly from 1953; 'corporate': a country's corporate bond spread over its government bonds (country 'Germany', rating_bucket 'All ratings', from 1957; or 'Australia', rating_bucket e.g. 'BBB 10Y', from 2005); or 'borrowing_cost': the ECB's composite cost of new bank loans to companies (country 'Euro Area' or a member, from 2003), a rate level rather than a spread. The last two are monthly.")
    country: str | None = Field(default=None, description="Used when dimension is 'corporate' (default 'Germany') or 'borrowing_cost' (default 'Euro Area'); must stay unset otherwise.")
    maturity_bucket: str = Field(default='7-10 Years', description="One of credit_controller.MATURITY_BUCKETS. Used when dimension='maturity'.")
    rating_bucket: str = Field(default='BBB', description="One of credit_controller.RATING_BUCKETS for dimension='rating', of credit_controller.MOODYS_BUCKETS ('Aaa', 'Baa', 'Baa - Aaa') for dimension='moodys', or of credit_controller.CORPORATE_BUCKETS[country] for dimension='corporate' (default 'All ratings').")
    period: str = 'daily'
    volatility_model: Literal['constant', 'garch'] = Field(default='constant', description="'constant' (the default) or 'garch' (GARCH(1,1) time-varying volatility of Bollerslev (1986)).")
    condition_on_business_cycle: bool = Field(default=False, description="Add an additive drift term on the leading indicator's step-to-step change (business-cycle conditioning). Requires leading_indicator.enabled=true; incompatible with volatility_model='garch'.")
    beliefs: CreditBeliefs = Field(default_factory=CreditBeliefs)
```

</details>

#### CommodityConfig

Commodity factor settings: opt-in, one entry per futures ticker (an empty `commodities` list simulates none).
`method: single_factor` (the default) is Schwartz's (1997) mean-reverting log price; `method: schwartz_smith` is
Schwartz and Smith's (2000) two-factor model, a short-term deviation and a long-term equilibrium simulated as the
extra factors `<name>_chi` and `<name>_xi`; `method: random_walk` is a log-price random walk for a commodity held as
an asset, such as gold, drifting with `inflation_name`'s simulated inflation. Each is correlated with the rest of
the model.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
class CommodityConfig(_StrictModel):
    name: str = 'commodity'
    ticker: str = Field(default='CL=F', description="Any commodity/futures ticker the Toolkit instance includes, e.g. CL=F (WTI crude), GC=F (gold), NG=F (natural gas), HG=F (copper). method='schwartz_smith' needs a ticker with a futures curve in the Finance Toolkit: crude oil, natural gas, gold, silver, copper, corn, wheat or soybeans.")
    currency: str = Field(default='USD', description='The currency the price is quoted in, USD by convention; used when converting results.')
    period: str = 'daily'
    method: Literal['single_factor', 'schwartz_smith', 'random_walk'] = Field(default='single_factor', description="'single_factor' (default): Schwartz (1997) mean-reverting log-price process. 'schwartz_smith': Schwartz and Smith (2000) two-factor process (short-term deviation + long-term equilibrium), simulated as f'{name}_chi'/f'{name}_xi'. 'random_walk': a log-price random walk with no long-run level, for a commodity held as an asset such as gold, whose mine supply adds about 1.5% a year to the stock above ground, Erb and Harvey (2013, pp. 28-29), https://doi.org/10.2469/faj.v69.n4.1; only its volatility is fitted.")
    inflation_name: str | None = Field(default=None, description="With method='random_walk': the inflation entry whose simulated rate the price drifts with, so its median real price stays at today's level, the long-run zero real return of gold in Erb and Harvey (2013, p. 11). Unset, the median price itself stays at today's level.")
    measure: Literal['real_world', 'risk_neutral'] = Field(default='real_world', description="'real_world' (P-measure, the default) or 'risk_neutral' (Q-measure, calibrated against the ticker's real observed forward curve). Only 'schwartz_smith' has a defined risk-neutral version.")
    contracts: int = Field(default=12, gt=0, description="With method='schwartz_smith': how many monthly futures contracts to fetch for the fit.")
    long_term_window_years: float = Field(default=3.0, gt=0, description="With method='schwartz_smith': the trailing window, in years, whose average stands in for the long-term equilibrium price. 3 years is a judgement, several times the half-life of the short-term deviations (ln 2 / 1.49, about half a year, in Schwartz and Smith (2000, Table 2)).")
    volatility_model: Literal['constant', 'garch'] = Field(default='constant', description="method='single_factor' only: 'constant' (Schwartz's own log-price OU fit) or 'garch' (GARCH(1,1) time-varying volatility of Bollerslev (1986)). Incompatible with method='schwartz_smith'.")
    condition_on_business_cycle: bool = Field(default=False, description="method='single_factor' only: add an additive drift term on the leading indicator's step-to-step change (business-cycle conditioning). Requires leading_indicator.enabled=true; incompatible with volatility_model='garch' and with method='schwartz_smith'.")
    beliefs: CommodityBeliefs = Field(default_factory=CommodityBeliefs)
```

</details>

#### DividendYieldConfig

Dividend yield factor settings: opt-in, one entry per ticker (an empty `dividend_yield` list simulates none). Each
entry is an Ahlgrim, D'Arcy and Gorvett (2005) mean-reverting process on the log of the ticker's trailing dividend
yield, correlated with the rest of the model. `condition_on_inflation` adds Wilkie's (1986) inflation term, fitted
at the period of the `inflation_name` entry; `inflation_term: level` takes it in Wilkie's own form (section 3.5), in
which the yield's normal level moves with inflation. `volatility_follows_equity` gives the log yield the volatility
of an equity entry's current regime, as Hibbert, Mowbray and Turnbull (2001, section 5.2.2) do. Beliefs can state a
published parameter set, including a speed of 0, the random walk of Ahlgrim, D'Arcy and Gorvett (2005, section 3).

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
class DividendYieldConfig(_StrictModel):
    name: str = 'dividend_yield'
    ticker: str = Field(default='SPY', description='Any dividend-paying ticker the Toolkit instance includes.')
    currency: str = Field(default='USD', description="The ticker's listing currency. A yield is a ratio and is never converted; this only labels it.")
    window: int = Field(default=252, gt=0, description='Trading days of trailing dividends summed for one yield observation.')
    period: str = 'daily'
    condition_on_inflation: bool = Field(default=False, description="Add Wilkie's (1986) inflation-sensitivity term to the fit. Requires inflation_name to match a configured inflation[i].name; forces this entry's calibration period to that entry's period. Incompatible with a belief override.")
    inflation_name: str = Field(default='inflation', description="Used when condition_on_inflation=true. Which configured inflation[i].name this entry's inflation-sensitivity term reads its step-to-step change from.")
    volatility_model: Literal['constant', 'garch'] = Field(default='constant', description="'constant' (Ahlgrim/D'Arcy/Gorvett's own log-yield OU fit) or 'garch' (GARCH(1,1) time-varying volatility of Bollerslev (1986)). Incompatible with condition_on_inflation=true.")
    condition_on_business_cycle: bool = Field(default=False, description="Add an additive drift term on the leading indicator's step-to-step change (business-cycle conditioning). Requires leading_indicator.enabled=true; incompatible with volatility_model='garch' and with condition_on_inflation=true.")
    inflation_term: Literal['change', 'level'] = Field(default='change', description="With condition_on_inflation, how inflation enters. 'change' (the default) adds w times the change in inflation and pulls ln y itself toward its normal level; 'level' is Wilkie's (1986, section 3.5) own form, lnY(t) = YW * inflation(t) + YN(t), in which the pull acts on YN(t), the log yield less its inflation term, so the yield's normal level rises with inflation.")
    volatility_follows_equity: str | None = Field(default=None, description="The name of a regime-switching equity entry whose current regime's volatility the log yield takes each step, as in Hibbert, Mowbray and Turnbull (2001, section 5.2.2): the yield swings more when the market is in its volatile regime. None (the default) keeps one fitted volatility.")
    beliefs: DividendYieldBeliefs = Field(default_factory=DividendYieldBeliefs)
```

</details>

#### DividendGrowthConfig

Dividend growth factor settings: opt-in, one entry per ticker, following Wilkie (1986). Each entry is driven by an
inflation entry (`inflation_name`) and a dividend yield entry (`dividend_yield_name`). It has no `period` of its
own: it is fitted at the inflation entry's period, which the dividend yield entry must share. `yield_residual_lag:
year` reads the yield's surprise a year back, Wilkie's yearly lag, on any step; beliefs can state his parameters in
his yearly terms (see `DividendGrowthBeliefs`).

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
class DividendGrowthConfig(_StrictModel):
    name: str = 'dividend_growth'
    ticker: str = Field(default='SPY', description='Any dividend-paying ticker the Toolkit instance includes.')
    currency: str = Field(default='USD', description="The ticker's listing currency; used when converting results.")
    window: int = Field(default=252, gt=0, description='Trading days of trailing dividends summed for one dividend index observation.')
    inflation_name: str = Field(default='inflation', description="Which configured inflation[i].name this entry's dlnQ(t) term reads. Also forces this entry's calibration period to that inflation entry's period.")
    dividend_yield_name: str = Field(default='dividend_yield', description="Which configured dividend_yield[i].name this entry's YE(t-1) term reads its own shock from. Must resolve to the same period as inflation_name's entry.")
    carried_forward_weight: float = Field(default=0.2, gt=0, lt=1, description="DD, the yearly weight of current inflation in the carried-forward inflation average, converted to the fit's period. Wilkie (1986, section 3.9) sets DW = 0.8, DD = 0.2 and DX = 0.2 in both his bases; section 3.8 feeds DD times the current inflation rate into the dividend model each year.")
    yield_residual_lag: Literal['step', 'year'] = Field(default='step', description="How far back the dividend yield's surprise YE is read. 'step' (the default) is the previous step; 'year' is a year back, Wilkie's (1986, section 3.7) YE(t-1) in his yearly model, so a monthly run spreads last year's yield surprise over this year's dividends as his yearly step does.")
    beliefs: DividendGrowthBeliefs = Field(default_factory=DividendGrowthBeliefs)
```

</details>

#### RealEstateConfig

Real estate factor settings: opt-in. A mean-reverting process on property price growth (Ahlgrim, D'Arcy and Gorvett
2005, eq. 3.18, who fit two separate Ornstein-Uhlenbeck models for real estate on NCREIF quarterly returns;
https://www.casact.org/sites/default/files/old/05pcas_ahlgrim-darcy-gorvett.pdf), correlated with the rest of the
model. Belief overrides only apply when `volatility_model` is "constant". `condition_on_interest_rate` slows growth
in the year after `interest_rate_name`'s rate rises, with a sensitivity fitted on the OECD's house prices and long
rate since 1971 (Iacoviello (2005, section I, Figure 1, p. 741); see `RealEstate.calibrate_rate_link`); it reads
the rate a year back, so it fixes no simulation order. `history_source: oecd` fits the speed and volatility of
growth on the OECD's house prices since 1971 (`RealEstate.calibrate_history`): fitted since 2000, the 2006-2011
bust and the 2021 boom set the swings, and a quarter of 30-year scenarios lose more than the 20% the US index lost
in its worst decade. With it, `volatility_model: regime_switching` lets growth's shocks switch between a calm and a
turbulent stretch fitted on the same history (Hamilton (1989); Hardy (2001)), so a bust year such as 2008 has a
real chance; see `RealEstate.calibrate_history`.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
class RealEstateConfig(_StrictModel):
    enabled: bool = False
    country: str = 'United States'
    currency: str = 'USD'
    period: str = 'quarterly'
    source: Literal['house_price', 'commercial'] = Field(default='house_price', description="'house_price' (default): OECD residential house-price growth via get_house_prices(). 'commercial': FRED's (IMF-sourced) US commercial real estate price index growth via get_commercial_real_estate_prices() instead; United States only (that call takes no country argument) and quarterly-only (no annual series), so requires country='United States' and period='quarterly'; also requires a FRED API key. Neither option is a substitute for Ahlgrim, D'Arcy and Gorvett's (2005) original calibration, which used NCREIF's appraisal-smoothed commercial-property index: no open NCREIF equivalent exists; 'commercial' is transaction-based index data, not appraisal-based (see https://www.jeroenbouma.com/projects/financescenarios/docs/coverage).")
    volatility_model: Literal['constant', 'garch', 'regime_switching'] = Field(default='constant', description="'constant' (the default), 'garch' (GARCH(1,1) time-varying volatility of Bollerslev (1986)) or 'regime_switching' (calm and turbulent stretches of shocks fitted on the OECD's quarter-on-quarter house-price growth since 1971 by maximum likelihood, Hamilton (1989), as in Crawford and Fratantoni (2003), https://doi.org/10.1111/1540-6229.00064; needs history_source='oecd').")
    condition_on_business_cycle: bool = Field(default=False, description="Add an additive drift term on the leading indicator's step-to-step change (business-cycle conditioning). Requires leading_indicator.enabled=true; incompatible with volatility_model='garch'.")
    ou_fit: Literal['year_apart', 'step'] = Field(default='year_apart', description="How persistence is read from the year-over-year growth: 'year_apart' (the default) regresses each value on the value a year earlier, since neighbouring quarterly readings share three quarters; 'step' on the previous quarter, the fit before October 2026, which reads that overlap as slow mean reversion.")
    condition_on_interest_rate: bool = Field(default=False, description="Let house-price growth slow in the year after interest_rate_name's rate rises, with a sensitivity fitted on the country's OECD house prices and long rate since 1971 (Iacoviello (2005)). source='house_price' with constant volatility, without condition_on_business_cycle.")
    interest_rate_name: str | None = Field(default=None, description='With condition_on_interest_rate: the interest_rates[i].name of the long rate mortgages follow.')
    history_source: Literal['oecd'] | None = Field(default=None, description="Fit the speed and volatility of growth on the OECD's house prices since 1971 instead of the recent window, whose 2006-2011 bust and 2021 boom inflate the swings; the normal growth rate and today's growth stay. source='house_price' with constant volatility, without condition_on_business_cycle.")
    beliefs: OUBeliefs = Field(default_factory=OUBeliefs)
```

</details>

#### YieldCurveConfig

Nelson-Siegel dynamic yield curve settings: opt-in, alongside the single-tenor
interest_rate factor. When enabled, adds three correlated factors (rate_level,
rate_slope, rate_curvature) to the simulation, calibrated from historical
multi-tenor treasury yields (see `source`).

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
class YieldCurveConfig(_StrictModel):
    enabled: bool = False
    period: str = 'daily'
    decay: float = Field(default=0.7308, gt=0, description='Nelson-Siegel decay parameter (lambda), annualized. Diebold and Li (2006, section 3) use a monthly λ = 0.0609, the value that maximizes the loading on the medium-term factor at exactly 30 months; x 12 = 0.7308.')
    source: Literal['yahoo', 'treasury', 'government'] = Field(default='yahoo', description="'yahoo' (default) calibrates against the four Yahoo Finance Treasury-yield tickers (3-month, 5-, 10- and 30-year). 'treasury' calibrates against the official daily 12-tenor Treasury par curve (1 Month through 30 Year) via FinanceToolkit's fixedincome.get_treasury_rates(): a much denser cross-section for the same three-factor Nelson-Siegel fit, especially at the short end the Yahoo set barely covers. Requires an FMP API key and period='daily' (the Treasury publishes daily); falls back to 'yahoo' with a logged warning when the fetch fails. Tenor columns the Treasury only started publishing partway through the window (e.g. '2 Month', 2018) are dropped rather than truncating every other tenor's history. 'government' calibrates against the official government bond yield curve of `country` via FinanceToolkit's fixedincome.get_government_bond_yield_curve() (no API key): the US Treasury, the ECB's euro area curve, the Bundesbank, the Bank of England, Japan's Ministry of Finance, the Bank of Canada, the Riksbank or Norges Bank; period daily, weekly or monthly. It never falls back to the US curve, since that would silently simulate the wrong country.")
    country: str = Field(default='United States', description=f"With source='government': the country whose curve to fit, one of {list(GOVERNMENT_CURVE_COUNTRIES)}.")
    beliefs: YieldCurveBeliefs = Field(default_factory=YieldCurveBeliefs)
```

</details>

#### CreditTermStructureConfig

Nelson-Siegel credit spread curve settings: opt-in, alongside the single spreads of `credit`. When enabled, adds
three correlated factors (`credit_level`, `credit_slope`, `credit_curvature`) fitted like `yield_curve` to the
corporate spread at several maturities, from the Treasury's High Quality Market curve or a bond-level panel
(`source`).

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
class CreditTermStructureConfig(_StrictModel):
    enabled: bool = False
    source: Literal['hqm', 'bond_panel'] = Field(default='hqm', description="'hqm' (default): the US Treasury's High Quality Market corporate spread curve at 2, 5, 10 and 30 years, monthly from 1984, through the Finance Toolkit (needs a FRED key; kilobytes). 'bond_panel': the Open Source Bond Asset Pricing TRACE panel, 2002-2025 (a 1.8 GB download that needs well over 1 GB of memory to average).")
    period: str = Field(default='monthly', description="Resampling frequency before fitting; source='hqm' is monthly, quarterly or yearly. For the bond panel 'daily' works but is not recommended: single-bond noise fits an unrealistically fast mean reversion at that frequency.")
    decay: float = Field(default=0.7308, gt=0, description="Nelson-Siegel decay parameter (lambda), annualized; same default as yield_curve, so the curves add: Diebold and Li's (2006) 0.0609 a month, which puts the curvature peak at 30 months.")
    tenors: list[float] = Field(default=[1.0, 2.0, 3.0, 5.0, 7.0, 10.0, 15.0, 20.0], description="Maturity points (years) the bond panel is binned into before fitting; at least 3 required for the cross-sectional Nelson-Siegel regression. Unused by source='hqm', which comes at its own 2, 5, 10 and 30 years.")
    beliefs: YieldCurveBeliefs = Field(default_factory=YieldCurveBeliefs)
```

</details>

#### HjmConfig

Two-factor Gaussian Heath-Jarrow-Morton forward curve settings: opt-in. When enabled, adds two correlated factors
(`hjm_factor_1`, `hjm_factor_2`) whose drift follows from the no-arbitrage condition rather than a fit, calibrated
on the same four Treasury yields as `yield_curve` but independently of it.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
class HjmConfig(_StrictModel):
    enabled: bool = False
    period: str = 'daily'
    decay: float = Field(default=0.7308, gt=0, description="Nelson-Siegel decay parameter (lambda) for HJM's own anchor curve fit; Diebold and Li's (2006) 0.0609 a month x 12, as for yield_curve.")
    kappa_bounds: tuple[float, float] = Field(default=(0.01, 6.0), description="Search bounds for both factors' volatility_decay, a judgement with no published value. The 0.01 floor is a half-life of about 70 years; a floor of 0.03 to 0.10 tempers the convexity at long horizons.")
    beliefs: HjmBeliefs = Field(default_factory=HjmBeliefs)
```

</details>

#### CreditMigrationConfig

Rating migration and default driven by a simulated credit cycle: opt-in. Adds the `credit_cycle` factor (a
standard normal index, high in good years), calibrated from a rating agency's transition counts and yearly
default rates in ESMA's CEREP repository; `rating_migration(result, holdings)` then rolls a portfolio's ratings
forward along it. See `credit_migration_controller.CreditMigration`.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
class CreditMigrationConfig(_StrictModel):
    enabled: bool = False
    agency: str = Field(default='S&P', description='The rating agency as CEREP names it, e.g. \'S&P\', "Moody\'s".')
    rating_type: Literal['corporate', 'sovereign', 'structured_finance', 'covered_bonds'] = 'corporate'
    region: str | None = Field(default=None, description='Limit to rated entities in one region; all by default.')
    matrix_years: int | None = Field(default=None, ge=1, description='Years of transition counts pooled into the matrix; by default every year of the default-rate history, since Basel Framework CRE36.79 requires the longer observation period whenever a source spans one and its data are relevant and material (https://www.bis.org/basel_framework/chapter/CRE/36.htm).')
    currency: str = 'USD'
    period: Literal['yearly'] = Field(default='yearly', description='The cycle is fitted on yearly default rates.')
    beliefs: OUBeliefs = Field(default_factory=OUBeliefs)
```

</details>

#### LeadingIndicatorConfig

Leading indicator factor settings: opt-in. A mean-reverting process on the OECD
Composite Leading Indicator, correlation-linked to the rest of the model. Factors with
`condition_on_business_cycle: true` also use it in their drift (see `LeadingIndicator`).
Belief overrides currently only apply when `volatility_model` is `"constant"`.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
class LeadingIndicatorConfig(_StrictModel):
    enabled: bool = False
    country: str = 'United States'
    currency: str = 'USD'
    period: str = 'monthly'
    volatility_model: Literal['constant', 'garch'] = Field(default='constant', description="'constant' (the default) or 'garch' (GARCH(1,1) time-varying volatility of Bollerslev (1986)).")
    beliefs: OUBeliefs = Field(default_factory=OUBeliefs)
```

</details>

#### MortalityConfig

Mortality/longevity factor settings: opt-in. The Cairns, Blake and Dowd (2006)
two-factor stochastic mortality model (kappa1 level, kappa2 age-slope), each
simulated as a random walk with drift, correlation-linked to the rest of the
model. Its data either come with the call (`source: supplied`, the default: pass a
historical mortality-rate surface, age x calendar year, and its ages to
Scenarios.calibrate()/simulate()) or from Eurostat's life tables through the Finance
Toolkit (`source: eurostat`, any European Economic Area `country`; see
mortality_controller.py).

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
class MortalityConfig(_StrictModel):
    enabled: bool = False
    period: str = 'yearly'
    source: Literal['supplied', 'eurostat'] = Field(default='supplied', description="'supplied' (default): pass a mortality table to calibrate()/simulate(). 'eurostat': fetch `country`'s life table (death probabilities by age, yearly from 1960 for most countries) through the Finance Toolkit, no API key needed.")
    country: str = Field(default='Germany', description="European Economic Area country for source='eurostat'.")
    sex: Literal['total', 'male', 'female'] = Field(default='total', description="Life table for source='eurostat'.")
    min_age: int = Field(default=60, ge=0, description="Youngest age fitted with source='eurostat'; Cairns, Blake and Dowd (2006) fit mortality rates above age 60.")
    max_age: int = Field(default=84, le=94, description="Oldest age fitted with source='eurostat'. Above 84 keeps only recent years: Eurostat extended its life tables from an open 85+ group to 95+ from reference year 2014; at most 94, since the 95-and-over group has a death probability of 1.")
    beliefs: MortalityBeliefs = Field(default_factory=MortalityBeliefs)
```

</details>

#### CorrelationsConfig

Correlations stated as values instead of estimated, the way a published model states its own.

By default every pair of factors gets the correlation of its historical changes, shrunk and repaired (see
`EngineConfig`). A published scenario generator fixes them as parameters instead: Ahlgrim, D'Arcy and Gorvett
(2005) set the real short rate and inflation shocks at -0.3 in their model's input sheet, and Hibbert, Mowbray and
Turnbull (2001, Exhibit 7.1B) the equity and dividend yield shocks at -0.95, every pair they do not list at zero.
`fixed` lists such pairs; `unlisted: zero` sets every other pair to zero, so the matrix is the paper's own. The
stated matrix is still repaired to the nearest valid one if its values contradict each other, and a pair naming a
factor the run does not simulate (one that failed to calibrate) is skipped with a warning. A two-factor entry's
slow leg is its own factor, `<name>_target`.

As an example, the shocks of a real short rate, its moving target and inflation as in Ahlgrim, D'Arcy and Gorvett
(2005):

```yaml
correlations:
  unlisted: zero
  fixed:
    - {factors: [interest_rate, interest_rate_target], value: 0.5}
    - {factors: [interest_rate, inflation], value: -0.3}
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
class CorrelationsConfig(_StrictModel):
    fixed: list[FixedCorrelation] = Field(default_factory=list, description='Pairs whose correlation is stated rather than estimated.')
    unlisted: Literal['history', 'zero'] = Field(default='history', description="'history' (the default) estimates every pair not in `fixed`; 'zero' sets it to zero, as a published model that lists its correlations does.")
```

</details>

##### CorrelationsConfig.as_pairs

The fixed pairs as (factor, factor) -> correlation, for `Dependence`.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
as_pairs() -> dict[tuple[str, str], float]
```

</details>

#### FixedCorrelation

One correlation stated as a value: the two factors' shocks and how strongly they move together.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
class FixedCorrelation(_StrictModel):
    factors: tuple[str, str] = Field(description='The two factors, by name, e.g. [interest_rate, inflation].')
    value: float = Field(ge=-1, le=1, description="Their shocks' correlation, between -1 and 1.")
```

</details>

### Beliefs

#### OUBeliefs

Your views on a mean-reverting factor (an interest rate, inflation, ...), laid over its historical fit. A field
left unset keeps the fitted value.

History is a guide, not a forecast: a fit on the last twenty years may put the long-run short rate at 1.5% when your
house view is 3%. `long_run_mean` sets the level the factor is pulled toward, either one number for the whole
horizon or a `BeliefPath` that moves over time ("9% next year, 2.5% by year eight"). `mean_reversion_speed` sets
how quickly shocks fade and `volatility` how large they are. `shocks` add one-off jumps at chosen years, from which
the factor then reverts on its own. A `BeliefPath` applies to constant-volatility factors without business-cycle
conditioning. Three models read these beliefs in their own terms, so a stress regime means the same on them: on
regime-switching inflation `long_run_mean` moves the long-run mean, by moving both regimes' levels; on a
policy-rule short rate and an expectations-hypothesis long rate a path prescribes the rate up to its last anchor,
after which the model sets it again (see `InflationConfig` and `InterestRateConfig`).

Two more models read them in their own terms, so a published parameter set can be stated directly. On a
`wilkie_ar1` inflation and a `wilkie_consols` rate, whose models are yearly AR(1)s, the speed is the yearly
persistence as a rate, -ln(QA), and the volatility is the yearly shock size as an Ornstein-Uhlenbeck volatility,
QSD * sqrt(2 * speed / (1 - QA^2)), so the yearly AR(1) is Wilkie's exactly; on `wilkie_consols` the long-run mean
is the real yield's level, CMU. On a `hibbert_two_factor` entry the speed and volatility are the fast leg's, and
`target_mean_reversion_speed`, `target_long_run_mean` and `target_volatility` set its moving target's own
Ornstein-Uhlenbeck process (the `<name>_target` factor); the fast leg has no long-run mean of its own.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
class OUBeliefs(_StrictModel):
    mean_reversion_speed: float | None = Field(default=None, gt=0)
    long_run_mean: float | BeliefPath | None = None
    volatility: float | None = Field(default=None, gt=0)
    target_mean_reversion_speed: float | None = Field(default=None, gt=0, description="hibbert_two_factor only: the speed of the moving target's own reversion.")
    target_long_run_mean: float | None = Field(default=None, description='hibbert_two_factor only: the level the moving target reverts to.')
    target_volatility: float | None = Field(default=None, gt=0, description="hibbert_two_factor only: the moving target's volatility.")
    shocks: list[Shock] = Field(default_factory=list, description='One-off jumps applied at specific simulated years.')
```

</details>

#### InterestRateBeliefs

Your views on an interest rate, laid over its historical fit, as in `OUBeliefs`, plus whether its shocks are the
rate's whole move.

A stress regime that replays an episode states how far the 10-year yield moved, as history records it, and often
sets the policy rate's path as well. The recorded move is the yield's whole move: the change in the short rates
expected over the bond's life plus the change in its term premium, the split of Campbell and Shiller (1991,
section 2, eq. 1) that Adrian, Crump and Moench (2013, section 2.4) estimate for the 10-year Treasury yield. A long
rate that reverts on its own moves with its short rate only through correlated shocks, so the move belongs on top
of wherever each scenario stands, which is what a shock does. A long rate built on its short rate's expected path
already moves with a prescribed policy path, so the same shocks would count the expected-path part twice.

`total_move: true` says the shocks are the whole move, measured from the rate's starting level. A long rate built
on its short rate's expected path (`expectations_hypothesis`) is then held at its starting level plus the shocks
so far, pulled there at its term premium's speed and with its volatility, until the last shock, after which the
expected path and the premium take over from where the rate stands: the premium takes whatever part of the stated
move the short rate's expected path does not explain. Every other rate adds the shocks as usual, so its scenarios
do not change. The shocks must then be additive, and a `long_run_mean` path, which already prescribes the rate,
cannot be combined with it.

**As an example:**

The 1994 Bond Massacre regime raises the short rate by 2.79 points and states the 10-year yield's 2.63-point rise
from October 1993 to November 1994 (FRED GS10) as the yield's whole move:

```yaml
beliefs:
  interest_rates.united_states_long_rate:
    total_move: true
    shocks:
      - {year: 0.25, magnitude: 0.00658}
      - {year: 0.5, magnitude: 0.00658}
      - {year: 0.75, magnitude: 0.00658}
      - {year: 1.0, magnitude: 0.00658}
```

**References:**

- Campbell, J.Y., Shiller, R.J. (1991). "Yield Spreads and Interest Rate Movements: A Bird's Eye View." The Review of Economic Studies, 58(3), 495-514. Section 2, eq. (1). <https://doi.org/10.2307/2298008>
- Adrian, T., Crump, R.K., Moench, E. (2013). "Pricing the Term Structure with Linear Regressions." Journal of Financial Economics, 110(1), 110-138. Section 2.4, the risk-neutral yields and the term premium. <https://doi.org/10.1016/j.jfineco.2013.04.009>

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
class InterestRateBeliefs(OUBeliefs):
    total_move: bool = Field(default=False, description="Read the shocks as the rate's whole move from its starting level, including what its short rate brings, instead of adding them to wherever each scenario stands.")
```

**Attributes:**

- <u>total_move (bool):</u> read the shocks as the rate's whole move from its starting level, including what its short rate brings; False (the default) adds them to wherever each scenario stands.

</details>

#### EquityBeliefs

Your views on an equity market, laid over its regime-switching fit. A field left unset keeps the fitted value.

`regime_means` and `regime_volatilities` set each regime's yearly log-return and volatility, one value per regime
from the weakest to the strongest, so you can lower the calm regime's return (a lower equity premium) or deepen the
turbulent one. `transition_matrix` sets the chances of moving between the regimes per period of the entry
(`period`, monthly by default), in the same order: row i holds the chances of each regime next period given
regime i now, as a published model states them (Hibbert, Mowbray and Turnbull (2001, Exhibit 7.1A) stay in their
calm regime with 0.929 a month and in their volatile one with 0.879). The long-run share of time in each regime
follows from it. `shocks` add one-off falls or jumps at chosen years, such as a regulator's stress path.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
class EquityBeliefs(_StrictModel):
    regime_means: list[float] | None = None
    regime_volatilities: list[float] | None = None
    transition_matrix: list[list[float]] | None = Field(default=None, description='Chances of moving between regimes per period of the entry, row i the regime now and column j the regime next period, ordered from the weakest regime to the strongest; each row sums to 1.')
    shocks: list[Shock] = Field(default_factory=list, description="One-off jumps in the price: each multiplies the price at its year by exp(magnitude), a log-return (-0.3 is about a 26% fall), after which the regimes continue from the shocked price. Additive only; stress_test_regime fills these from a regulator's stock-market path.")
```

</details>

#### BeliefPath

A view on where a mean-reverting factor is heading over time, rather than one long-run level for the whole
horizon: "inflation at 9% in a year, 5% in three, 2.5% by year eight".

Each anchor sets the level the factor is pulled toward at that horizon; between anchors the target moves in a
straight line, and before the first it holds at the first. The factor still has its own volatility and reversion
speed, so scenarios scatter around the path and lag behind a fast-moving target rather than tracking it exactly.
Where a plain number says "the long-run level is X", a `BeliefPath` says "X now, Y in 5 years, Z in 10".

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
class BeliefPath(BaseModel):
    anchors: dict[float, float] = Field(description='horizon in years from t=0 -> target long_run_mean value.')
    converge_over_years: float | None = Field(default=None, gt=0, description='Years, past the last anchor, over which the target converges linearly to long_run_mean before holding flat there. None (default) holds flat at the last anchor forever.')
```

**Attributes:**

- <u>anchors (dict[float, float]):</u> years from the start -> the long-run level targeted then; at least one.
- <u>converge_over_years (float &#124; None):</u> after the last anchor, move the target back to the factor's own long-run level over this many years. Defaults to None, which holds the last anchor's level.

</details>

##### BeliefPath.terminal_value

The level targeted at the furthest anchor, the path's single-number summary.

<details class="ft-details fs-api" markdown="1">
<summary><b>Signature</b></summary>

```python
beliefpath.terminal_value  # property -> float
```

</details>

### Presets and Profiles

#### Profile

One named settings profile or factor set, read from its YAML file with any `extends` chain merged in.

`load_profile_library` returns these, keyed by id; `load_profiles` merges a settings profile and a factor set into
one configuration; `list_presets` shows them as a table.

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
class Profile(BaseModel):
    id: str
    name: str
    description: str = ''
    data: dict[str, Any] = Field(default_factory=dict)
```

**Attributes:**

- <u>id (str):</u> the file name without ".yaml", e.g. "long_horizon"; the name you pass to `Scenarios.from_profiles`.
- <u>name (str):</u> a short, readable label, e.g. "Long Horizon"; the `id` when the file sets none.
- <u>description (str):</u> what the profile is for; "" when the file sets none.
- <u>data (dict[str, Any]):</u> the profile's settings, ready to merge into a configuration.

</details>

#### list_presets

List every ready-made preset you can name, with the call that takes it.

There are four kinds: settings profiles and factor sets (for `Scenarios.from_profiles`), regimes (its `regime=`)
and portfolios (for `Portfolio.from_preset`). A local folder of the same name, such as one `scaffold_project` wrote,
is read instead of the bundled copy, exactly as those calls do.

**As an example:**

```python
from financescenarios import list_presets

list_presets(kind="settings")
```

Which returns (without the 'description' column):

| kind | id | use_with | name |
|:-----|:---|:---------|:-----|
| settings | ahlgrim | Scenarios.from_profiles(settings="ahlgrim") | Ahlgrim 2005 |
| settings | default | Scenarios.from_profiles(settings="default") | Default |
| settings | goes | Scenarios.from_profiles(settings="goes") | NAIC GOES |
| settings | hibbert | Scenarios.from_profiles(settings="hibbert") | Hibbert 2001 |
| settings | long_horizon | Scenarios.from_profiles(settings="long_horizon") | Long Horizon |
| settings | wilkie | Scenarios.from_profiles(settings="wilkie") | Wilkie 1986 |

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
list_presets(kind: str | None = None) -> pl.DataFrame
```

**Args:**

- <u>kind (str &#124; None):</u> "settings", "factor-sets", "regimes" or "portfolios"; None (the default) lists all four.

**Returns:**

<u>pl.DataFrame:</u> one row per preset: 'kind', 'id' (the name to pass), 'use_with' (the call and argument that takes it), 'name' and 'description'.

**Raises:**

- <u>ValueError:</u> if `kind` is not one of the four.

</details>

#### load_profiles

Load a configuration from a named settings profile and a named factor set, such as "default" and "broad".

A settings profile says how a run executes (start date, steps, number of scenarios, seed); a factor set says what it
simulates: which factors, fitted on which history, and the beliefs laid over that fit. Each is one YAML file picked
by name, and may start with `extends: <name>` to build on another profile. Swapping one never changes the other.
This is what `Scenarios.from_profiles` uses, and `list_presets` shows every name you can pass.

**As an example:**

```python
from financescenarios import load_profiles

config = load_profiles(settings_id="long_horizon", factor_set_id="default")
config.describe()
```

Which returns (cut to four of the nine categories):

| category | n_factors | factors |
|:---------|----------:|:--------|
| commodities | 2 | gold, crude_oil |
| equities | 5 | us_broad, small_cap, europe, japan, emerging_markets |
| fx | 3 | eur, gbp, jpy |
| inflation | 3 | united_states_inflation, eurozone_inflation, united_kingdom_inflation |

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
load_profiles(
    settings_dir: str | Path = 'settings',
    settings_id: str = 'default',
    factor_sets_dir: str | Path = 'factor-sets',
    factor_set_id: str = 'default',
) -> ScenariosConfig
```

**Args:**

- <u>settings_dir (str &#124; Path):</u> the settings folder; "settings" by default, the bundled presets when it does not exist.
- <u>settings_id (str):</u> the settings profile's name, e.g. "long_horizon"; "default" by default.
- <u>factor_sets_dir (str &#124; Path):</u> the factor-set folder; "factor-sets" by default, the bundled presets when it does not exist.
- <u>factor_set_id (str):</u> the factor set's name, e.g. "broad"; "default" by default.

**Returns:**

<u>ScenariosConfig:</u> the validated configuration, merged from both profiles.

**Raises:**

- <u>FileNotFoundError:</u> if either profile, or one it extends, does not exist; the message lists the names available.
- <u>ValueError:</u> if an `extends` chain loops back on itself.
- <u>pydantic.ValidationError:</u> if the merged fields do not form a valid configuration.

</details>

#### load_config

Load a configuration from two YAML files: one for how the run executes, one for what it simulates.

`config_path` holds the run settings (`start_date`, `engine`, `toolkit`, `reporting`) and `factors_path` the factor
definitions (`interest_rates`, `inflation`, `equities`, `fx`, ...). Keeping them apart means changing what is
simulated never touches how the run executes, and the other way around. A section left out of both files takes its
default. To pick named, ready-made profiles instead of file paths, use `load_profiles`.

**As an example:**

```python
from financescenarios import Scenarios, load_config

config = load_config("my-project/config.yaml")  # reads my-project/factors.yaml too
scenarios = Scenarios.from_config(config)
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
load_config(config_path: str | Path, factors_path: str | Path | None = None) -> ScenariosConfig
```

**Args:**

- <u>config_path (str &#124; Path):</u> the run-settings YAML file.
- <u>factors_path (str &#124; Path &#124; None):</u> the factor-definitions YAML file; a `factors.yaml` next to `config_path` by default. Without that default file every factor takes its default; a path you pass must exist.

**Returns:**

<u>ScenariosConfig:</u> the validated configuration, merged from both files.

**Raises:**

- <u>FileNotFoundError:</u> if `config_path`, or a `factors_path` you pass, does not exist.
- <u>ValueError:</u> if a file is not valid YAML or does not hold a mapping of keys to values.
- <u>pydantic.ValidationError:</u> if the merged fields do not form a valid configuration, e.g. a misspelt key.

</details>

#### load_profile_library

Load every profile in a folder, one YAML file per profile, each with its `extends` chain merged in.

Use it to see what a folder holds; to run with one profile, `load_profiles` (or `Scenarios.from_profiles`) reads
only the files it needs. `list_presets` gives the same overview as a table.

**As an example:**

```python
from financescenarios import load_profile_library

profiles = load_profile_library("settings")
{profile_id: profile.name for profile_id, profile in profiles.items()}
```

Which returns:

```
{'ahlgrim': 'Ahlgrim 2005', 'default': 'Default', 'goes': 'NAIC GOES', 'hibbert': 'Hibbert 2001',
 'long_horizon': 'Long Horizon', 'wilkie': 'Wilkie 1986'}
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
load_profile_library(directory: str | Path) -> dict[str, Profile]
```

**Args:**

- <u>directory (str &#124; Path):</u> the profiles folder, e.g. "settings" or "factor-sets"; the bundled presets when no such folder exists.

**Returns:**

<u>dict[str, Profile]:</u> every profile, keyed by its id (the file name without ".yaml").

**Raises:**

- <u>FileNotFoundError:</u> if the folder does not exist and is not one of the bundled preset folders.
- <u>ValueError:</u> if a file is not valid YAML or its `extends` chain loops back on itself.

</details>

#### scaffold_project

Copy the bundled presets into a folder you can edit: settings profiles, factor sets, regimes and portfolios, plus a
`.env` template for API keys.

The bundled presets work without this: `Scenarios.from_profiles` and `list_presets` read them straight from the
package. Scaffold only when you want to change them. Once a `settings/`, `factor-sets/`, `regimes/` or `portfolios/`
folder exists where Python runs, it is read instead of the bundled copy. A `.gitignore` that keeps `.env` out of git
and a `README.md` explaining the folders are written too.

**As an example:**

```python
from financescenarios import Scenarios, scaffold_project

scaffold_project("my-project")
scenarios = Scenarios.from_profiles(settings_dir="my-project/settings", factor_sets_dir="my-project/factor-sets")
```

<details class="ft-details fs-api" markdown="1">
<summary><b>Arguments and returns</b></summary>

```python
scaffold_project(target_dir: str | Path, force: bool = False) -> list[Path]
```

**Args:**

- <u>target_dir (str &#124; Path):</u> the folder to write into, created if missing.
- <u>force (bool):</u> overwrite files that already exist; False by default, which skips them, so running it again only fills in what is missing.

**Returns:**

<u>list[Path]:</u> every file written: the presets folder by folder, then `.env`, `.gitignore` and `README.md`.

</details>
