---
name: write-model-tests
description: Write or update Pytest tests for financial model functions, with recorded expected outputs. Use when adding tests, when a function has no test yet, or when a test fails after a change.
---

# Writing model tests

1. **Mirror the structure.** A function in `<package>/<category>/<module>.py` is tested in
   `tests/<category>/test_<module>.py`, in a function named `test_<function_name>`.
2. **Use small inputs you can check by hand**, for example five periods of revenue and cost,
   including at least one edge case where it matters (a zero, a negative value or a `NaN`).
3. **Record the output** with the recorder fixture from `tests/conftest.py`:

   ```python
   def test_get_gross_margin(recorder):
       recorder.capture(
           get_gross_margin(
               revenue=pd.Series([100, 110, 120, 130, 80]),
               cost_of_goods_sold=pd.Series([30, 40, 60, 60, 20]),
           )
       )
   ```

4. **Verify the first recording.** For a new test, compute at least one value by hand and
   compare it with the recorded output before relying on it. A recording only proves that a
   result stays the same, not that it is correct.
5. **When a test fails after a change,** do not rewrite the recording. Report the expected and
   actual values, explain why the result changed, and only rewrite
   (`--record-mode=rewrite`) after the change has been confirmed to be correct.
6. Run the affected test file, then the full suite.
