---
title: Test your Model
seo_title: Test a Financial Model in Python with Pytest
excerpt: Explore model testing with Pytest. Set up tests mirroring model structure, ensuring accurate results through data recording and comparison.
description: Explore model testing with Pytest. Set up tests mirroring model structure, ensuring accurate results through data recording and comparison.
author_profile: true
permalink: /modelling/test-your-model
classes: wide-sidebar
author_profile: false
sidebar:
    nav: "modelling"
---

{% include mermaid.html %}

Tests are what make a model trustworthy over time, and they are what makes working with an AI assistant safe. Every change, whether it's a new feature, an updated dependency or a refactor by the assistant, can quietly change a result. A good test suite tells you exactly which number changed and where, so you can decide whether that change is correct.

As defined in [Setting up your Project](/modelling/setting-up-your-project), the model should always include a `tests` folder. The tests in this folder are run with [Pytest](https://docs.pytest.org/en/stable/){: target="_blank"}. The structure of the tests should mirror the structure of the model, in effect duplicating it. The main difference is that each test module filename is prefixed with `test_` so Pytest can discover it.

For example, to test the Gross Margin functionality from `profitability_model.py`, create a test function with the same name prefixed by `test_`. This looks like the following:

```python
def test_get_gross_margin(recorder):
    recorder.capture(
        get_gross_margin(
            revenue=pd.Series([100, 110, 120, 130, 80]),
            cost_of_goods_sold=pd.Series([30, 40, 60, 60, 20]),
        )
    )
```

This is a test created for the function defined in [Structure your Model](/modelling/structure-your-model). Graphically, the process looks like this:

<div class="mermaid">
flowchart LR;

Step0["User"] -- <b>Step 1<br></b>Execute Pytest --> Step1["Profitability Model Tests"]
Step1["Profitability Model Tests"] -- <b>Step 2<br></b>Run Test --> Step2["test_get_gross_margin"]
Step2["test_get_gross_margin"] -- <b>Step 3<br></b>Run Function with Test Data --> Step3["get_gross_margin"]
Step3["get_gross_margin"] -- <b>Step 4a<br></b>Return the Output --> Step2["test_get_gross_margin"]
Step2["test_get_gross_margin"] -- <b>Step 4b<br></b> (On Rewrite) Save the Output --> Step4["test_get_gross_margin.csv"]
Step2["test_get_gross_margin"] <-- <b>Step 5<br></b> Compare Result with Saved Output --> Step4["test_get_gross_margin.csv"]
Step2["test_get_gross_margin"] -- <b>Step 6<br></b>Return Test Result --> Step1["Profitability Model Tests"]
Step1["Profitability Model Tests"] -- <b>Step 7<br></b>Return Summarized Test Result --> Step0["User"]
</div>

The process above illustrates that data is saved to CSV when tests are run in rewrite mode. This means rerunning the test in this mode overwrites existing data, which is useful when you've identified that the expected output needs adjustment.

To support this process, a `conftest.py` file is included in the `tests` folder. This file defines fixtures usable across tests. For example, fixtures can handle exporting data to formats like JSON, CSV, or TXT. These fixtures are defined using `@pytest.fixture` (read more [here](https://docs.pytest.org/en/6.2.x/fixture.html){: target="_blank"}).

{: .notice--info}
Working with `conftest.py` can be challenging initially. Consider using the `conftest.py` found **[here](https://github.com/JerBouma/FinanceToolkit/blob/main/tests/conftest.py){: target="_blank"}** as a starting point for executing tests and writing results to files.

To see this in action, download or clone the [FinanceToolkit](https://github.com/JerBouma/FinanceToolkit){: target="_blank"} repository and install the required dependencies:

1. Install uv: `brew install uv`
2. Install the dependencies: `uv sync`

Run the tests by executing `pytest tests`. This command runs all tests defined in the `tests` folder, producing output similar to this:

```shell
(base) FinanceToolkit % pytest tests
============================= test session starts =============================
platform darwin -- Python 3.10.9, pytest-7.1.2, pluggy-1.0.0
rootdir: /Users/jeroenbouma/Documents/FinanceToolkit, configfile: pyproject.toml
collected 277 items                                                                                                                                                                   

tests/test_toolkit_controller.py ......                                         [  2%]
tests/models/test_alman_model.py ......                                         [  4%]
# ... (rest of the output omitted for brevity) ...
tests/technical/test_volatility_model.py ....                                   [ 100%]

============================= 277 passed in 65.18s (0:01:05) =============================
```

The `conftest.py` can define ways to rewrite the test output files when there are expected or validated differences. This is controlled by the `record-mode` option; setting it to `rewrite` redefines the expected output for failing tests. The output is stored in individual data files. This gives you a reliable way to check that results stay consistent. If discrepancies occur, you can verify them before accepting the changes. Use the following command:

```shell
pytest tests --record-mode="rewrite"
```

Or for individual tests:

```shell
pytest tests/ratios/test_profitability_model.py --record-mode="rewrite"
```

This generates CSV files (e.g., [tests/ratios/csv/test_get_gross_margin.csv](https://github.com/JerBouma/FinanceToolkit/blob/main/tests/ratios/csv/test_profitability_model/test_get_gross_margin.csv){: target="_blank"}) which are used for comparison when the test is run again. If changes are made to the calculation, the test framework automatically highlights the difference between the new result and the recorded result. Only after validating that the new result is correct should the test data be rewritten using the `--record-mode="rewrite"` flag.

![Testing Directory](/assets/images/modelling/test-your-model/testing-directory.png)

For example, changing the Gross Margin formula from `(revenue - cost_of_goods_sold) / revenue` to `(revenue - cost_of_goods_sold) / revenue - 1` (which is incorrect) causes the test to fail and display the following error, showing the difference between the expected and actual results:

```shell
(base) FinanceToolkit % pytest tests/ratios/test_profitability_model.py 
=========================== test session starts ========================================
platform darwin -- Python 3.10.9, pytest-7.1.2, pluggy-1.0.0
rootdir: /Users/jeroenbouma/Documents/FinanceToolkit, configfile: pyproject.toml
collected 16 items                                                                                                                                                                    

tests/ratios/test_profitability_model.py .E...............

============================ ERRORS ====================================================
ERROR at teardown of test_get_gross_margin

self = <tests.conftest.Recorder object at 0x293678a60>

    def assert_equal(self):
        record_list = self.__record_list
    
        for record in record_list:
            if record.record_changed:
>               raise AssertionError(
                    "Change detected\n"
                    f"Record    : {record.record_path}\n"
                    f"Expected  : {record.recorded[:self.display_limit]}\n"
                    f"Actual    : {record.captured[:self.display_limit]}\n"
                )
E               AssertionError: Change detected
E               Expected  : ,0
E               0,0.7
E               1,0.6363636363636364
E               2,0.5
E               3,0.5384615384615384
E               4,0.75
E               
E               Actual    : ,0
E               0,-0.30000000000000004
E               1,-0.36363636363636365
E               2,-0.5
E               3,-0.46153846153846156
E               4,-0.25

tests/conftest.py:226: AssertionError
================================ short test summary info ================================
ERROR tests/ratios/test_profitability_model.py::test_get_gross_margin - Change detected
================================ 16 passed, 1 error in 1.99s ============================
```

The test caught the mistake immediately and shows both the expected and the actual values, so you can see at a glance that every gross margin has dropped by exactly 1.

## Tests and AI Assistants

Let your assistant write the tests, together with every function it adds; it's a good rule for your instruction file. There are two things you have to own, though.

- **The expected values must come from somewhere independent.** A test that records whatever the function currently returns only proves that the function is consistent, not that it is correct. For a new calculation, verify the first recorded output yourself: calculate a few values by hand, compare them with a source such as an annual report, or use a textbook example. Only then does the recorded CSV become a trustworthy reference.
- **Never let an assistant rewrite recorded results to make a test pass.** When a test fails after a change, the failure is the information you need. Rerunning with `--record-mode="rewrite"` silences it. Look at the difference between the expected and actual values first, understand why the number changed, and only rewrite the recording when you are sure the new result is the correct one.

With these two habits, the test suite becomes the safety net that lets an assistant work quickly on your model without you losing track of the results. The final page shows how to set up your project so that an AI assistant works with all of these components. Visit [Working with AI](/modelling/working-with-ai) to continue!

[Working with AI](/modelling/working-with-ai){: .btn .btn--info .btn--large .align-center}
