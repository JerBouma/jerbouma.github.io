---
name: review-model-change
description: Review a change to the financial model before it is committed, checking the financial choices as well as the code. Use when asked to review a diff, a branch or a pull request, or before finishing a larger task.
---

# Reviewing a model change

Read the full diff, then go through these checks. Report findings per check, with the file and
line, and say explicitly when a check passed.

1. **Formula.** Does each calculation match the intended definition? Name the definition used
   when several are common.
2. **Units and conventions.** Fractions versus percentages, signs of costs and outflows, simple
   versus log returns, currencies.
3. **Periods and alignment.** Annual versus quarterly data, lags and shifts, annualisation
   factors (252 trading days versus 365 calendar days), look-ahead in time series.
4. **Missing data.** Division by zero, missing periods, companies without a line item. Look for
   silent `fillna`, `dropna` or forward-filling that changes results.
5. **Hidden assumptions.** Hardcoded rates, dates or tickers that should be parameters or
   constants.
6. **Structure.** Calculations only in model files, data selection in controllers, plotting in
   views; existing helpers reused; names, type hints and docstrings follow the conventions.
7. **Tests.** Every changed function is tested; recorded outputs were not rewritten without an
   explanation; the full suite and linters pass.

End with a short verdict: ready to commit, or the list of changes needed.
