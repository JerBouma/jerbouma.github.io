---
title: Test your Model
excerpt: Explore model testing with Pytest. Set up tests mirroring model structure, ensuring accurate results through data recording and comparison. 
description: Explore model testing with Pytest. Set up tests mirroring model structure, ensuring accurate results through data recording and comparison.
author_profile: true
permalink: /modelling/test-your-model
classes: wide-sidebar
author_profile: false
sidebar:
  nav: "modelling"
---

<script src="https://cdn.jsdelivr.net/npm/mermaid@10.6.0/dist/mermaid.min.js"></script>

As defined in [Setting up your Project](/modelling/setting-up-your-project), the model should always include a `tests` folder. This utilizes [Pytest](https://docs.pytest.org/en/){: target="_blank"} to run tests. The tests should be structured in the same way as the model. And is a duplication of the model in terms of structure. The only difference is that each individual module will have `test_` in front so that Pytest can recognize the file as a test.

<div class="mermaid">
flowchart LR;
classDef boxfont fill:#3b9cba,stroke-width:0px,color:white,radius:20px,font-weight:bold;
classDef currentfont fill:#d67f05,stroke-width:0px,color:white,radius:20px,font-weight:bold;

Step0[<a href="/modelling/introduction" style="color:white;text-decoration:none">Introduction</a>]:::boxfont --> Step1[<a href="/modelling/getting-started" style="color:white;text-decoration:none">Getting Started</a>]:::boxfont

Step1[<a href="/modelling/getting-started" style="color:white;text-decoration:none">Getting Started</a>] --> Step2[<a href="/modelling/setting-up-your-project" style="color:white;text-decoration:none">Setting up your Project</a>]:::boxfont

Step2[<a href="/modelling/setting-up-your-project" style="color:white;text-decoration:none">Setting up your Project</a>] -->  Step3[<a href="/modelling/structure-your-model" style="color:white;text-decoration:none">Structure your Model</a>]:::boxfont

Step3[<a href="/modelling/structure-your-model" style="color:white;text-decoration:none">Structure your Model</a>] --> Step4[<a href="/modelling/build-your-model" style="color:white;text-decoration:none">Build your Model</a>]:::boxfont

Step4[<a href="/modelling/build-your-model" style="color:white;text-decoration:none">Build your Model</a>] <--> Step5[<a href="/modelling/test-your-model" style="color:white;text-decoration:none">Test your Model</a>]:::currentfont
</div>

As an example, when the Gross Margin functionality, obtained from the `profitability_model.py` needs to be tested, a function should be created that contains the same function name as within the `profitability_model.py` file with the exception that `test_` is included. This looks like the following:

```python
def test_get_gross_margin(recorder):
    recorder.capture(
        get_gross_margin(
            revenue=pd.Series([100, 110, 120, 130, 80]),
            cost_of_goods_sold=pd.Series([30, 40, 60, 60, 20]),
        )
    )
```

This is a test that would be created for the function that was defined in [Structure your Model](/modelling/structure-your-model). Graphically the process would look as follows:

<div class="mermaid">
flowchart LR;

classDef boxfont fill:#3b9cba,stroke-width:0px,fill-opacity:0.7,color:white,radius:20px;

Step0["User"]:::boxfont -- <b>Step 1<br></b>Execute Pytest --> Step1["Profitability Model Tests"]:::boxfont
Step1["Profitability Model Tests"] -- <b>Step 2<br></b>Run Test --> Step2["test_get_gross_margin"]:::boxfont
Step2["test_get_gross_margin"] -- <b>Step 3<br></b>Run Function with Test Data --> Step3["get_gross_margin"]:::boxfont
Step3["get_gross_margin"] -- <b>Step 4a<br></b>Return the Output --> Step2["test_get_gross_margin"]
Step2["test_get_gross_margin"] -- <b>Step 4b<br></b> (On Rewrite) Save the Output --> Step4["test_get_gross_margin.csv"]:::boxfont
Step2["test_get_gross_margin"] <-- <b>Step 5<br></b> Compare Result with Saved Output --> Step4["test_get_gross_margin.csv"]:::boxfont
Step2["test_get_gross_margin"] -- <b>Step 6<br></b>Return Test Result --> Step1["Profitability Model Tests"]
Step1["Profitability Model Tests"] -- <b>Step 7<br></b>Return Summarized Test Result --> Step0["User"]
</div>

The process above shows that the data is saved to CSV on rewrite, this means that if you reinitialize the test, it will overwrite the existing data. This is for example relevant when you have identified that the output needed to be adjusted.

To accompany the process, a `conftest.py` file is included in the `tests` folder. This file is meant to define fixtures that can be used in the tests. For example, I find it important that the data is exported to e.g. JSON, CSV, TXT and more. This all needs to be defined with `@pytest.fixture` (read more [here](https://docs.pytest.org/en/6.2.x/fixture.html){: target="_blank"}).

{: .notice--info}
Working with a `conftest.py` is a quite difficult concept to understand at first and therefore, I'd recommend acquiring the `conftest.py` as found **[here](https://github.com/JerBouma/FinanceToolkit/blob/main/tests/conftest.py){: target="_blank"}** to automatically be able to execute tests and write them to the relevant file.

To be able to see this in action, download or clone the [FinanceToolkit](https://github.com/JerBouma/FinanceToolkit){: target="_blank"} repository and install the required dependencies by doing the following:

1. Install pipx: `pip install pipx`
2. Install Poetry: `pipx install poetry`
3. Install the dependencies: `poetry install`

You can run the tests by executing `pytest tests`. This will run all tests that are defined in the `tests` folder which shows the following:

```shell
(base) FinanceToolkit % pytest tests
============================= test session starts =============================
platform darwin -- Python 3.10.9, pytest-7.1.2, pluggy-1.0.0
rootdir: /Users/jeroenbouma/Documents/FinanceToolkit, configfile: pyproject.toml
collected 277 items                                                                                                                                                                   

tests/test_toolkit_controller.py ......                                         [  2%]
tests/models/test_alman_model.py ......                                         [  4%]
tests/models/test_dupont_model.py ..                                            [  5%]
tests/models/test_enterprise_model.py .                                         [  5%]
tests/models/test_intrinsic_model.py .                                          [  5%]
tests/models/test_models_controller.py .....                                    [  7%]
tests/models/test_wacc_model.py ...                                             [  8%]
tests/performance/test_performance_controller.py ...............                [ 14%]
tests/performance/test_performance_model.py ...................                 [ 20%]
tests/ratios/test_efficiency_model.py ............                              [ 25%]
tests/ratios/test_liquidity_model.py .......                                    [ 27%]
tests/ratios/test_profitability_model.py ................                       [ 33%]
tests/ratios/test_ratios_controller.py ...................                      [ 58%]
tests/ratios/test_solvency_model.py ..........                                  [ 62%]
tests/ratios/test_valuation_model.py .....................                      [ 70%]
tests/risk/test_risk_controller.py .......                                      [ 72%]
tests/risk/test_risk_model.py .............                                     [ 77%]
tests/technical/test_breadth_model.py .....                                     [ 79%]
tests/technical/test_momentum_model.py ...............                          [ 84%]
tests/technical/test_overlap_model.py .....                                     [ 86%]
tests/technical/test_technical_controller.py .................................. [ 98%]
tests/technical/test_volatility_model.py ....                                   [ 100%]

============================= 277 passed in 65.18s (0:01:05) =============================
```

Within the `conftest.py` I have defined ways to rewrite the tests if there are differences that I can explain. This is done by defining the `record-mode` which can be `rewrite` in case the tests need to be redefined. Any output will be stored in individual datafiles. This is a very powerful way to ensure that the results remain the same and if not, it can be verified that the changes are correct. This can be done through:

```shell
pytest tests --record-mode="rewrite"
```

Or for individual tests:

```shell
pytest tests/ratios/test_profitability_model.py --record-mode="rewrite"
```

This generates CSV files ([tests/ratios/csv/test_get_gross_margin.csv](https://github.com/JerBouma/FinanceToolkit/blob/main/tests/ratios/csv/test_profitability_model/test_get_gross_margin.csv){: target="_blank"}) which are used to compare the result once the test is ran again. So if any changes are made to the calculation, it will automatically give me the difference between the two results and only if I (or a tester) can validate that the new result is correct, the test should be rewritten.

![Testing Directory](/assets/images/modelling/test-your-model/testing-directory.png)

For example, if I change the Gross Margin formula from `(revenue - cost_of_goods_sold) / revenue` to `(revenue - cost_of_goods_sold) / revenue - 1` (which is incorrect), the test will fail and show the following:

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