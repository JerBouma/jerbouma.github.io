---
title: Structure your Model
excerpt: All of my talks, both personal and professional, are included here. This include presentations at a variety of universities and webinars.
description: All of my talks, both personal and professional, are included here. This include presentations at a variety of universities and webinars.
author_profile: true
permalink: /modelling/structure-your-model
classes: wide-sidebar
author_profile: false
sidebar:
  nav: "modelling"
---

<script src="https://cdn.jsdelivr.net/npm/mermaid@10.6.0/dist/mermaid.min.js"></script>

To understand how to structure a model, the following guidelines are given. These guidelines are meant to be used as a reference and are not meant to be followed strictly. The most important thing is that the model is structured in a way that is understandable and maintainable.

<div class="mermaid">
flowchart LR;
classDef boxfont fill:#3b9cba,stroke-width:0px,color:white,radius:20px,font-weight:bold;
classDef currentfont fill:#d67f05,stroke-width:0px,color:white,radius:20px,font-weight:bold;

Step0[<a href="/modelling/introduction" style="color:white;text-decoration:none">Introduction</a>]:::boxfont --> Step1[<a href="/modelling/getting-started" style="color:white;text-decoration:none">Getting Started</a>]:::boxfont

Step1[<a href="/modelling/getting-started" style="color:white;text-decoration:none">Getting Started</a>] --> Step2[<a href="/modelling/setting-up-your-project" style="color:white;text-decoration:none">Setting up your Project</a>]:::boxfont

Step2[<a href="/modelling/setting-up-your-project" style="color:white;text-decoration:none">Setting up your Project</a>] -->  Step3[<a href="/modelling/structure-your-model" style="color:white;text-decoration:none">Structure your Model</a>]:::currentfont

Step3[<a href="/modelling/structure-your-model" style="color:white;text-decoration:none">Structure your Model</a>] --> Step4[<a href="/modelling/build-your-model" style="color:white;text-decoration:none">Build your Model</a>]:::boxfont

Step4[<a href="/modelling/build-your-model" style="color:white;text-decoration:none">Build your Model</a>] <--> Step5[<a href="/modelling/test-your-model" style="color:white;text-decoration:none">Test your Model</a>]:::boxfont
</div>

The preferred logic of creating a model is the **Model, View and Controller (MVC)** pattern. This is a pattern in software design commonly used to implement user interfaces, data, and controlling logic. It emphasizes a separation between the software's business logic and display. This "separation of concerns" provides for a better division of labor and improved maintenance. Models and Views should be able to function on their own whereas Controllers are reliant on either a Model or a combination of Models and Views.

The following diagrams illustrate the different flows of the MVC pattern depending on how you structured your model and what the purpose of your model is.

<div class="row">
<div markdown="1" class="thirty-column mobile-max-column-width">

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
</div>

<div markdown="1" class="thirty-column mobile-max-column-width">

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

</div>

<div markdown="1" class="thirty-column mobile-max-column-width">

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
</div>

What makes the MVC pattern so powerful is that it is immediately clear in the structure of the model what modules do what. If I am looking for the calculation of the Gross Margin ratio or want to understand what data is being passed on for this calculation, I know exactly where to look (the model and controller respectively).

{: .notice--info }
**The Importance of Separation of Concerns**<br>The concept of separating functionality based on their role within the model is to me so powerful with this pattern that I tend to apply it any model I have created. Note that there are many variations of this infrastructure (see [here](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller#See_also){: target="_blank"}) but all of them return to the same core principles.

### The Data Layer

The data layer of the application which is where the data is manipulated. This can be anything from calculations to simple data transformations. The importance of these models is that they work on any dataset and have as little requirements as feasibly possible.

<div class="mermaid">
flowchart LR;
classDef boxfont fill:#3b9cba,stroke-width:0px,fill-opacity:0.7,color:white,radius:20px;

Step0["User"]:::boxfont -- <b>Step 1<br></b>Provides Data -->  Step2["Profitability Model"]:::boxfont
Step2["Profitability Model"]:::boxfont <-- <b>Step 2<br></b>Calculates the Gross Margin -->  Step3["Get Gross Margin"]:::boxfont
Step2["Profitability Model"]:::boxfont  --<b>Step 3<br></b> Returns the Gross Margin --> Step0["User"]:::boxfont
</div>

For example, when calculating the Gross Margin, it should not be required to have a dataset with a specific column name. Instead, it should be possible to pass two Series, Arrays, Floats or Integers to do this calculation. This is referred to as the ability of doing "dumb" calculations, there is no flavouring done for the specific need.

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

Each function is categorized in a specific module. For example, the Gross Margin calculation is categorized under the `profitability_model.py` module which contains all of the other profitability ratios. The same applies to the other ratio categories such as liquidity, solvency, efficiency and valuation which can be found in `liquidity_model.py`, `solvency_model.py`, `efficiency_model.py` and `valuation_model.py` respectively.

### The Visualization Layer

This is meant to display data in a specific way. This can be a table, a graph, a dashboard, etc. It is definitely possible that the DataFrame that the model produces can already be considered as a "View" and therefore this is an optional addition.

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

Similar to the Data Layer, the Visualization Layer is also split up into different modules. For example, the Gross Margin plot is categorized under the `profitability_view.py` module which contains all of the other plot functionalities for the profitability ratios. The same applies to the other ratio categories such as liquidity, solvency, efficiency and valuation which can be found in `liquidity_view.py`, `solvency_view.py`, `efficiency_view.py` and `valuation_view.py` respectively.

### The Controlling Layer

These are functionalities that tie both the Model and View together. This is what adds in the dataset-specific flavouring. E.g. when calculating the Gross Margin, the controller will pass onto the model the correct columns of the dataset that contain the Revenue and the Cost of Goods Sold.

<div class="mermaid">
flowchart LR;
classDef boxfont fill:#3b9cba,stroke-width:0px,fill-opacity:0.7,color:white,radius:20px;

Step0["User"]:::boxfont -- <b>Step 1<br></b>Request Data -->  Step3["Ratios Controller"]:::boxfont
Step3["Ratios Controller"]:::boxfont <-- <b>Step 2<br></b>Calculates the Gross Margin --> Step2["Profitability Model"]:::boxfont
Step3["Ratios Controller"]:::boxfont -- <b>Step 3<br></b>Shows the Gross Margin Data --> Step0["User"]:::boxfont
</div>

Note that within the Controller there are <u>no</u> calculations done, this is purely meant to pass on the correct data to the View or Model. The controller functions are almost always wrapped inside a class, e.g. for the Gross Margin calculation, this is wrapped inside the `Ratios` class as follows (see the actual code [here](https://github.com/JerBouma/FinanceToolkit/blob/main/financetoolkit/ratios/ratios_controller.py#L2310-L2374){: target="_blank"}):


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

Different from the Data and Visualization Layer, the Controller is not split up into different modules. This is because the Controller is meant to be the "glue" between the Model and the View. So in this case, this function would fit in the `ratios_controller.py` module. 

As shown below, it is also possible to have multiple Controllers. For example, the Finance Toolkit has a `toolkit_controller.py` which is the main controller that is used to initialize the Toolkit. 

<div class="mermaid">
flowchart LR;
classDef boxfont fill:#3b9cba,stroke-width:0px,fill-opacity:0.7,color:white,radius:20px;

Step0["User"]:::boxfont-- <b>Step 1<br></b>Initializes the FinanceToolkit -->  Step1["Toolkit Controller"]:::boxfont
Step1["Toolkit Controller"] <-- <b>Step 2<br></b>Asks for Fundamental Data --> Step2a["Fundamentals Model"]:::boxfont
Step1["Toolkit Controller"] <-- <b>Step 3<br></b>Asks for Historical Data --> Step2b["Historical Model"]:::boxfont
Step1["Toolkit Controller"] -- <b>Step 4<br></b>Initializes the Ratios Controller --> Step3["Ratios Controller"]:::boxfont
</div>

This controller is then used to initialize the `ratios_controller.py` which is used to calculate the ratios. This is done to ensure that the Toolkit Controller is not overloaded with functions and that the Ratios Controller can be used separately. For example, in the `toolkit_controller.py`, the Ratios Controller is initialized as follows (see actual code [here](https://github.com/JerBouma/FinanceToolkit/blob/main/financetoolkit/toolkit_controller.py#L400-L523){: target="_blank"}):


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

Next to the Models, Views and Controller modules, it can be helpful to have a `helpers` module. This module is meant to contain functions that are used throughout the entirety of the package.

<div class="mermaid">
flowchart LR;
classDef boxfont fill:#3b9cba,stroke-width:0px,fill-opacity:0.7,color:white,radius:20px;

Step0["User"]:::boxfont -- <b>Step 1<br></b>Request Data -->  Step4["Ratios Controller"]:::boxfont
Step4["Ratios Controller"]:::boxfont <-- <b>Step 2<br></b>Calculates the Gross Margin --> Step2["Profitability Model"]:::boxfont
Step4["Ratios Controller"]:::boxfont <-- <b>Step 3<br></b>Calculates the Growth --> Step3["Helpers"]:::boxfont
Step4["Ratios Controller"]:::boxfont -- <b>Step 4<br></b>Shows the Growth of the Gross Margin --> Step0["User"]:::boxfont
</div>

For example, a function that calculates the growth of a pd.Series or pd.DataFrame. This function can be used in multiple places (calculating growth can be relevant for ratios, technical indicators, performance metrics and more) and therefore it is useful to put it into the helpers module. See the actual code [here](https://github.com/JerBouma/FinanceToolkit/blob/main/financetoolkit/helpers.py#L129-L207){: target="_blank"} and below an example:

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

Other type of helper functions could be reading datasets from xlsx or csv files and handling common errors. It is often not necessary to split up the `helpers` module into different modules.

### Combining Everything

As seen in the [Setting up your Project](/modelling/setting-up-your-project) page, the Model, View and Controller for Gross Margin calculation will be named `profitability_model.py`, `profitability_view.py` and `profitability_controller.py` respectively. The `helpers.py` module will be placed in the root of the package.

The same methodology is applied to the Finance Toolkit in which the structure of the last graph, as depicted at the top of this page, is used. 

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

Following this structure, this would be how it looks when executing each:

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



Once you have done these steps it's time to start build your model. Visit [Build your Model](/modelling/build-your-model) to continue!

[Build your Model](/modelling/build-your-model){: .btn .btn--info .btn--large .align-center}