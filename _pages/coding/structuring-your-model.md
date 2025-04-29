---
title: Structure your Model
excerpt: Learn to structure your financial model with the MVC pattern. Code in Python, manage dependencies, and follow clear separation of concerns.
description: Learn to structure your financial model with the MVC pattern. Code in Python, manage dependencies, and follow clear separation of concerns.
author_profile: true
permalink: /modelling/structure-your-model
classes: wide-sidebar
author_profile: false
sidebar:
    nav: "modelling"
---

<script src="https://cdn.jsdelivr.net/npm/mermaid@10.6.0/dist/mermaid.min.js"></script>

The following guidelines explain how to structure a model. These guidelines serve as a reference, not strict rules. The primary goal is a structure that is understandable and maintainable.

<div style="display: flex; justify-content: space-between;margin-bottom:10px">
        <a href="/modelling/introduction" class="btn btn--info" style="flex: 1;margin-right:5px;">Introduction to Modelling</a>
        <a href="/modelling/getting-started" class="btn btn--info" style="flex: 1;margin-right:5px">Getting Started</a>
        <a href="/modelling/setting-up-your-project" class="btn btn--info" style="flex: 1;margin-right:5px">Setting up your Project</a>
        <a href="/modelling/structure-your-model" class="btn btn--warning" style="flex: 1;margin-right:5px">Structure your Model</a>
        <a href="/modelling/build-your-model" class="btn btn--info" style="flex: 1;margin-right:5px">Build your Model</a>
        <a href="/modelling/test-your-model" class="btn btn--info" style="flex: 1;margin-right:5px">Test your Model</a>
</div>

The preferred approach for structuring a model is the **Model, View, Controller (MVC)** pattern. This software design pattern is commonly used to separate user interfaces, data, and controlling logic. It emphasizes separating the software's business logic from its presentation. This "separation of concerns" facilitates a better division of labor and improves maintainability. Models and Views should ideally function independently, while Controllers depend on Models or a combination of Models and Views. Note that while many variations of this pattern exist (see [here](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller#See_also){: target="_blank"}), they all adhere to the same core principles.

The following diagrams illustrate different data flows within the MVC pattern, depending on the model's structure and purpose.

<div style="display: flex; justify-content: space-between;margin-bottom:10px">

{% raw %}
<div class="mermaid">
flowchart TB;
classDef boxfont fill:#3b9cba,stroke-width:0px,fill-opacity:0.7,color:white,radius:20px;
Step0["User"] -- Uses --> Step1["Controller"]:::boxfont
Step1["Controller"] -- Manipulates --> Step2["Model"]:::boxfont
Step2["Model"] -- Updates --> Step3["View"]:::boxfont
Step3["View"] -- Sees --> Step0["User"]:::boxfont
</div>
{% endraw %}

{% raw %}
<div class="mermaid">
flowchart TB;
classDef boxfont fill:#3b9cba,stroke-width:0px,fill-opacity:0.7,color:white,radius:20px;
Step0["User"] -- Uses -->  Step1["Controller"]:::boxfont
Step1["Controller"] -- Manipulates --> Step2["Model"]:::boxfont
Step2["Model"] -- Returns --> Step1["Controller"]:::boxfont
Step1["Controller"] -- Sees --> Step0["User"]:::boxfont
</div>
{% endraw %}

{% raw %}
<div class="mermaid">
flowchart TB;
classDef boxfont fill:#3b9cba,stroke-width:0px,fill-opacity:0.7,color:white,radius:20px;
Step0["User"] -- Uses -->  Step1["Controller"]:::boxfont
Step1["Controller 1"] -- Activates --> Step2["Controller 2"]:::boxfont
Step2["Controller 2"] -- Manipulates --> Step3["Model"]:::boxfont
Step3["Model"] -- Returns --> Step2["Controller 2"]:::boxfont
Step2["Controller 2"] -- Sees --> Step0["User"]:::boxfont
</div>
{% endraw %}

</div>

The power of the MVC pattern lies in its clear structure, making it immediately apparent which modules perform specific functions. For instance, if you need to find the Gross Margin ratio calculation or understand the data used for it, you know to look in the Model and Controller, respectively.

{: .notice--info }
**The Importance of Separation of Concerns for Financial Modelling**<br>The Model, View, Controller (MVC) structure is particularly effective for financial models because they often combine diverse datasets and complex calculations, requiring overarching logic to manage data flow correctly.<br><br>For example, during scenario analysis or time-based simulations, a dedicated module is needed to track the current period, scenario, dataset, etc. This is where the Controller comes in. The actual calculations should be independent of this tracking logic, which is why they are separated into the Model. Similarly, visualization is distinct from both calculation and control logic and is thus separated into the View.<br><br>This modular structure simplifies debugging, as each component has a specific purpose, making it easier to pinpoint formula or data issues. Conversely, combining calculation and data components makes identifying the source of issues more difficult.

### The Data Layer

The Model layer is where data manipulation occurs. This can range from complex calculations to simple data transformations. Ideally, Models should operate on various data inputs and have minimal dependencies.

<div class="mermaid">
flowchart LR;
classDef boxfont fill:#3b9cba,stroke-width:0px,fill-opacity:0.7,color:white,radius:20px;

Step0["User"]:::boxfont -- <b>Step 1<br></b>Provides Data -->  Step2["Profitability Model"]:::boxfont
Step2["Profitability Model"]:::boxfont <-- <b>Step 2<br></b>Calculates the Gross Margin -->  Step3["Get Gross Margin"]:::boxfont
Step2["Profitability Model"]:::boxfont  --<b>Step 3<br></b> Returns the Gross Margin --> Step0["User"]:::boxfont
</div>

For example, a Gross Margin calculation function shouldn't require input data with specific column names. Instead, it should accept generic inputs like two Series, Arrays, Floats, or Integers. This approach promotes creating "dumb" calculation functions, devoid of application-specific logic.

See the simplicity of such a model [here](https://github.com/JerBouma/FinanceToolkit/blob/main/financetoolkit/ratios/profitability_model.py) and below:

```python
def get_gross_margin(revenue: pd.Series, cost_of_goods_sold: pd.Series) -> pd.Series:
        """
        Calculate the gross margin, a profitability ratio that measures the percentage of
        revenue that exceeds the cost of goods sold.

        Args:
                revenue (float or pd.Series): Total revenue of the company.
                cost_of_goods_sold (float or pd.Series): Total cost of goods sold of the company.

        Returns:
                float | pd.Series: The gross margin percentage value.
        """
        return (revenue - cost_of_goods_sold) / revenue
```

Each function is categorized in a specific module. For example, the Gross Margin calculation belongs in the `profitability_model.py` module, alongside other profitability ratio functions. Similarly, other ratio categories like liquidity, solvency, efficiency, and valuation reside in their respective model files (`liquidity_model.py`, `solvency_model.py`, `efficiency_model.py`, and `valuation_model.py`, respectively).

### The Visualization Layer

The View layer is responsible for presenting data. This can be a table, a graph, a dashboard, etc. In some cases, the data structure (like a DataFrame) produced by the Model might suffice as a "View," making a dedicated View component optional.

<div class="mermaid">
flowchart LR;
classDef boxfont fill:#3b9cba,stroke-width:0px,fill-opacity:0.7,color:white,radius:20px;

Step0["User"]:::boxfont -- <b>Step 1<br></b>Provides Data -->  Step2["Profitability Model"]:::boxfont
Step2["Profitability Model"]:::boxfont <-- <b>Step 2<br></b>Calculates the Gross Margin -->  Step3["Get Gross Margin"]:::boxfont
Step2["Profitability Model"]:::boxfont  --<b>Step 3<br></b> Returns the Gross Margin --> Step0["User"]:::boxfont
Step0["User"]:::boxfont -- <b>Step 4<br></b>Provides Gross Margin -->  Step4["Profitability View"]:::boxfont
Step4["Profitability View"]:::boxfont <-- <b>Step 5<br></b>Plot the Gross Margin -->  Step5["Plot Gross Margin"]:::boxfont
Step4["Profitability View"]:::boxfont -- <b>Step 6<br></b>Shows the Gross Margin Plot --> Step0["User"]:::boxfont
</div>

See below how such a view could look like:

```python
def plot_gross_margin(gross_margin: pd.Series) -> pd.Series:
        """
        Plot the gross margin, a profitability ratio that measures the percentage of
        revenue that exceeds the cost of goods sold.

        Args:
                gross_margin (pd.Series): Gross Margin of the company.

        Returns:
                A plot of the gross margin.
        """
        gross_margin.plot(
                kind="bar",
                title="Gross Margin",
                ylabel="Gross Margin (%)",
                xlabel="Date",
                color="green"
        )
```

Similar to the Model layer, the View layer is typically organized into modules. For example, the Gross Margin plotting function belongs in the `profitability_view.py` module, along with other profitability visualization functions. Likewise, visualizations for other ratio categories reside in corresponding view files (`liquidity_view.py`, `solvency_view.py`, `efficiency_view.py`, and `valuation_view.py`, respectively).

### The Controlling Layer

The Controller layer contains the logic that connects the Model and View. It handles application-specific logic and data preparation. For example, when calculating the Gross Margin, the Controller extracts the 'Revenue' and 'Cost of Goods Sold' data from the specific dataset and passes it to the Model function.

<div class="mermaid">
flowchart LR;
classDef boxfont fill:#3b9cba,stroke-width:0px,fill-opacity:0.7,color:white,radius:20px;

Step0["User"]:::boxfont -- <b>Step 1<br></b>Request Data -->  Step3["Ratios Controller"]:::boxfont
Step3["Ratios Controller"]:::boxfont <-- <b>Step 2<br></b>Calculates the Gross Margin --> Step2["Profitability Model"]:::boxfont
Step3["Ratios Controller"]:::boxfont -- <b>Step 3<br></b>Shows the Gross Margin Data --> Step0["User"]:::boxfont
</div>

Crucially, the Controller should perform <u>no</u> core calculations; its role is purely to orchestrate data flow between the Model and View. Controller logic is often encapsulated within classes. For instance, the Gross Margin calculation might be accessed via a method within a `Ratios` class (see the actual code [here](https://github.com/JerBouma/FinanceToolkit/blob/main/financetoolkit/ratios/ratios_controller.py#L2310-L2374){: target="_blank"}):

```python
class Ratios:
        """
        The Ratios Module
        """
        def __init__(
                self,
                tickers: str | list[str],
                historical: pd.DataFrame,
                balance: pd.DataFrame,
                income: pd.DataFrame,
                cash: pd.DataFrame,
                quarterly: bool = False,
                rounding: int | None = 4,
        ):
                """
                Initializes the Ratios Controller Class. Remaining docstring omitted.
                """
                # The necessary data initialization is done here.

        def get_gross_margin(
                self,
                rounding: int | None = None,
                growth: bool = False,
                lag: int | list[int] = 1,
        ) -> pd.DataFrame:
                """
                Calculate the gross margin, a profitability ratio that measures the percentage of
                revenue that exceeds the cost of goods sold. Remaining docstring omitted.
                """
                gross_margin = profitability_model.get_gross_margin(
                                self._income_statement.loc[:, "Revenue", :],
                                self._income_statement.loc[:, "Cost of Goods Sold", :],
                        )

                if growth:
                        return calculate_growth(
                                gross_margin, lag=lag, rounding=rounding if rounding else self._rounding
                        )

                return gross_margin.round(rounding if rounding else self._rounding)
```

Unlike the Model and View layers, a single Controller module might handle multiple related functionalities. This is because the Controller acts as the central coordinator or "glue." So in this case, this function would fit in the `ratios_controller.py` module.

It's also possible, and sometimes beneficial, to have multiple Controllers. For example, the Finance Toolkit uses a main `toolkit_controller.py` for initialization.

<div class="mermaid">
flowchart LR;
classDef boxfont fill:#3b9cba,stroke-width:0px,fill-opacity:0.7,color:white,radius:20px;

Step0["User"]:::boxfont-- <b>Step 1<br></b>Initializes the FinanceToolkit -->  Step1["Toolkit Controller"]:::boxfont
Step1["Toolkit Controller"] <-- <b>Step 2<br></b>Asks for Fundamental Data --> Step2a["Fundamentals Model"]:::boxfont
Step1["Toolkit Controller"] <-- <b>Step 3<br></b>Asks for Historical Data --> Step2b["Historical Model"]:::boxfont
Step1["Toolkit Controller"] -- <b>Step 4<br></b>Initializes the Ratios Controller --> Step3["Ratios Controller"]:::boxfont
</div>

This main controller then initializes a dedicated `ratios_controller.py` responsible for ratio calculations. This separation prevents the main Toolkit Controller from becoming overloaded and allows the Ratios Controller to be potentially used independently. For example, in `toolkit_controller.py`, the Ratios Controller is initialized like this (see actual code [here](https://github.com/JerBouma/FinanceToolkit/blob/main/financetoolkit/toolkit_controller.py#L400-L523){: target="_blank"}):

```python
class Toolkit:
        """
        The Finance Toolkit
        """
        def __init__(
                self,
                tickers: list | str,
                api_key: str = "",
                start_date: str | None = None,
                end_date: str | None = None,
                quarterly: bool = False,
                rounding: int | None = 4,
        ):
                """
                Initializes an Toolkit object. Remaining docstring omitted.
                """
                # The necessary data initialization is done.

        def ratios(self) -> Ratios:
                """
                The Ratios Module. Remaining docstring omitted.
                """
                # The necessary data collection is done here as depicted in the graph above.

                return Ratios(
                        tickers=tickers,
                        historical=self._quarterly_historical_data
                        if self._quarterly
                        else self._yearly_historical_data,
                        balance=self._balance_sheet_statement,
                        income=self._income_statement,
                        cash=self._cash_flow_statement,
                        custom_ratios_dict=self._custom_ratios,
                        quarterly=self._quarterly,
                        rounding=self._rounding,
                )
```

### The Supportive Layer

In addition to the Model, View, and Controller modules, a `helpers` module can be beneficial. This module houses utility functions used across different parts of the application.

<div class="mermaid">
flowchart LR;
classDef boxfont fill:#3b9cba,stroke-width:0px,fill-opacity:0.7,color:white,radius:20px;

Step0["User"]:::boxfont -- <b>Step 1<br></b>Request Data -->  Step4["Ratios Controller"]:::boxfont
Step4["Ratios Controller"]:::boxfont <-- <b>Step 2<br></b>Calculates the Gross Margin --> Step2["Profitability Model"]:::boxfont
Step4["Ratios Controller"]:::boxfont <-- <b>Step 3<br></b>Calculates the Growth --> Step3["Helpers"]:::boxfont
Step4["Ratios Controller"]:::boxfont -- <b>Step 4<br></b>Shows the Growth of the Gross Margin --> Step0["User"]:::boxfont
</div>

For example, consider a function that calculates the growth of a pd.Series or pd.DataFrame. Since growth calculation might be needed for ratios, technical indicators, performance metrics, etc., placing it in a central `helpers` module avoids code duplication. See the actual code [here](https://github.com/JerBouma/FinanceToolkit/blob/main/financetoolkit/helpers.py#L129-L207){: target="_blank"} and an example below:

```python
def calculate_growth(
        dataset: pd.Series | pd.DataFrame,
        lag: int | list[int] = 1,
        rounding: int | None = 4,
        axis: str = "columns",
) -> pd.Series | pd.DataFrame:
        """
        Calculates growth for a given dataset. Defaults to a lag of 1
        (i.e. 1 year or 1 quarter).

        Args:
                dataset (pd.Series | pd.DataFrame): the dataset to calculate the growth values for.
                lag (int | str): the lag to use for the calculation. Defaults to 1.
                rounding (int | None): the number of decimals to round the results to.
                Defaults to 4.
                axis (str): the axis to use for the calculation. Defaults to "columns".

        Returns:
                pd.Series | pd.DataFrame: _description_
        """
        return dataset.pct_change(periods=lag, axis=axis).round(rounding)
```

Other examples of helper functions include reading data from files (e.g., XLSX, CSV) or handling common errors. Usually, a single `helpers` module suffices.

### Combining Everything

As discussed in the [Setting up your Project](/modelling/setting-up-your-project) page, the Model, View, and Controller components for Gross Margin calculations would typically reside in `profitability_model.py`, `profitability_view.py`, and `profitability_controller.py`, respectively. The `helpers.py` module is usually placed at the package's root level.

The Finance Toolkit applies this methodology, utilizing the structure shown in the final diagram:

<div class="mermaid">
flowchart TB;
classDef boxfont fill:#3b9cba,stroke-width:0px,fill-opacity:0.7,color:white,radius:20px;

Step0["User"] -- <b>Step 1<br></b>Initializes the FinanceToolkit -->  Step1["Toolkit Controller"]:::boxfont
Step1["Toolkit Controller"] <-- <b>Step 2<br></b>Asks for Fundamental Data --> Step2a["Fundamentals Model"]:::boxfont
Step1["Toolkit Controller"] <-- <b>Step 3<br></b>Asks for Historical Data --> Step2b["Historical Model"]:::boxfont
Step1["Toolkit Controller"] -- <b>Step 4<br></b>Initializes the Ratios Controller --> Step3["Ratios Controller"]:::boxfont
Step3["Ratios Controller"] -- <b>Step 5a<br></b>Calculates the Gross Margin --> Step2["Profitability Model"]:::boxfont
Step3["Ratios Controller"] -- <b>Step 5b<br></b>Optional Growth Calculation --> Step4["Helpers"]:::boxfont
Step3["Ratios Controller"] -- <b>Step 6<br></b>Shows the Gross Margin Data --> Step0["User"]:::boxfont
</div>

Following this structure, here's how you might execute the code:

```python
from financetoolkit import Toolkit

companies = Toolkit(['AMZN', 'ASML', 'META'], api_key='YOUR_API_KEY')

companies.ratios.get_gross_margin()
```

Which returns the following dataset leveraging the actual financial statements:

|      |   2013 |   2014 |   2015 |   2016 |   2017 |   2018 |   2019 |   2020 |   2021 |   2022 |
|:-----|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|
| AMZN | 0.2723 | 0.2948 | 0.3304 | 0.3509 | 0.3707 | 0.4025 | 0.4099 | 0.3957 | 0.4203 | 0.4381 |
| ASML | 0.3977 | 0.4264 | 0.4606 | 0.4481 | 0.4503 | 0.4311 | 0.4146 | 0.4863 | 0.5271 | 0.4965 |
| META | 0.7618 | 0.8273 | 0.8401 | 0.8629 | 0.8658 | 0.8325 | 0.8194 | 0.8058 | 0.8079 | 0.7835 |

Alternatively, the growth of the Gross Margin can be calculated as follows:

```python
companies.ratios.get_gross_margin(growth=True)
```

Which returns the growth of the Gross Margin leveraging the same financial statements:

|      |   2013 |   2014 |   2015 |    2016 |   2017 |    2018 |    2019 |    2020 |   2021 |    2022 |
|:-----|-------:|-------:|-------:|--------:|-------:|--------:|--------:|--------:|-------:|--------:|
| AMZN |        | 0.0828 | 0.1207 |  0.0621 | 0.0563 |  0.0858 |  0.0185 | -0.0347 | 0.0623 |  0.0422 |
| ASML |        | 0.0723 | 0.08   | -0.0271 | 0.005  | -0.0426 | -0.0384 |  0.173  | 0.0839 | -0.058  |
| META |        | 0.0859 | 0.0155 |  0.0272 | 0.0034 | -0.0386 | -0.0157 | -0.0165 | 0.0026 | -0.0303 |

With this structure in place, you are ready to start building your model. Visit [Build your Model](/modelling/build-your-model) to continue!

[Build your Model](/modelling/build-your-model){: .btn .btn--info .btn--large .align-center}
