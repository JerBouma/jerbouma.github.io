---
name: add-financial-metric
description: Add a new financial ratio, indicator or model to the codebase, including the model function, controller method, test and documentation. Use when asked to add, implement or calculate a new metric.
---

# Adding a financial metric

1. **Pin down the definition.** Find the formula you will use. If more than one definition is
   common (for example which earnings measure a P/E ratio uses, or simple versus log returns),
   ask which one is wanted. Do not pick one silently.
2. **Find the right place.** Decide the category (profitability, liquidity, risk, ...) and open
   the matching `<category>_model.py` and `<category>_controller.py`. Check `helpers.py` and the
   existing functions for anything you can reuse.
3. **Write the model function.** A pure function in `<category>_model.py`:
   - inputs are `pd.Series`, `pd.DataFrame` or floats, with type hints;
   - a Google-style docstring that states the formula and its source if non-standard;
   - no data selection, plotting or printing;
   - missing values propagate as `NaN`; no silent filling or dropping;
   - no magic numbers: constants become parameters with documented defaults.
4. **Wire it up in the controller.** Add a method to `<category>_controller.py` that selects the
   inputs from the data and calls the model function. Support the same options as similar
   methods (for example `growth`, `lag` and `rounding`). No calculations here.
5. **Test it.** Add a test in the mirrored test file with small inputs you can check by hand
   (see the `write-model-tests` skill). Calculate one expected value by hand.
6. **Document it** where the project lists its metrics, if it does.
7. **Run the checks:** the full test suite and the linters.
8. **Summarise:** the definition used, the files changed and the value you checked by hand.
