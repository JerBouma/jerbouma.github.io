# Financial Model: Agent Instructions

<!--
Part of the Financial Modelling Agent Kit from https://www.jeroenbouma.com/modelling/introduction.
Replace everything in <angle brackets> with the details of your own project, delete what does
not apply, and keep this file short: it is read at the start of every session.
-->

<Project name> is a Python package that <one sentence on what the model calculates, for whom>.

The people working on this model care most about three things: every number can be traced back
to a documented formula, the structure stays predictable, and no result changes without someone
noticing. Optimize for that over cleverness or brevity.

## Commands

- Install: `uv sync`
- Run all tests: `uv run pytest tests`
- Run one test file: `uv run pytest tests/<category>/test_<category>_model.py`
- Lint and format: `uv run pre-commit run --all-files`

Run the tests and the linters before you consider a task done.

## Structure

The model follows a Model-View-Controller structure. Put code in the right layer:

- `<package>/<category>/<category>_model.py`: calculations only. Pure functions that take
  `pd.Series`, `pd.DataFrame` or floats and return the same. No data loading, no plotting,
  no printing, no knowledge of column names.
- `<package>/<category>/<category>_view.py`: plots and tables. Takes results, returns figures.
- `<package>/<category>/<category>_controller.py`: selects the right data, calls model
  functions and helpers, and returns the result. No calculations in the controller.
- `<package>/helpers.py`: shared utilities (growth, data reading, error handling). Reuse these
  instead of writing a new version.
- `tests/` mirrors the package. Every function has a test in the matching `test_<module>.py`.

If you are unsure where something belongs, ask before writing it.

## Conventions

- PEP 8, enforced by the linters. Line length <122>.
- Type hints on every function signature.
- Google-style docstrings. For a calculation, the docstring states the formula and, for
  non-standard definitions, the source.
- Descriptive names: `gross_margin`, not `gm`; `calculate_` or `get_` for functions.
- No magic numbers. A risk-free rate, tax rate or number of trading days is a parameter with a
  documented default or a named constant.
- Percentages are stored as fractions (0.25, not 25).
- <Add your own domain rules, e.g. "returns are simple returns unless stated", "annualize with
  252 trading days", "statements are in reported currency".>

## Financial choices

These change results. Never decide them silently; state the choice, and ask when it is not
obvious from this file or the existing code:

- Which definition of a metric is used (many ratios have several accepted definitions).
- Units, signs and conventions (fractions vs percentages, cost signs, simple vs log returns).
- Periods and alignment (annual vs quarterly, lags, annualization factor).
- How missing data is handled. Let `NaN` propagate; never fill or drop silently.
- Which data source is used.

## Tests

- Every new or changed function gets a test with small, hand-checkable inputs.
- Expected results are recorded with the `recorder` fixture in `tests/conftest.py`.
- For a new calculation, verify at least one expected value by hand and show it in your summary.
- Never rerun tests with `--record-mode=rewrite` to make a failing test pass. Show the difference
  between the expected and the actual values and explain why the result changed instead.

## Skills

Step-by-step instructions for recurring tasks live in `.claude/skills/<name>/SKILL.md`. Your tool
may load them automatically; if it does not, read the matching file before starting the task:

- `add-financial-metric`: adding a ratio, indicator or model.
- `write-model-tests`: writing or updating tests for model functions.
- `review-model-change`: reviewing a change before it is committed.
- `set-up-model-project`: setting up a new project with this structure.

## Working style

- Prefer small, focused changes. Ask for a plan to be approved before larger changes.
- Work on a branch; never commit directly to `main`.
- End every task with a short summary: what changed, which financial choices were made, and how
  the result was checked.
