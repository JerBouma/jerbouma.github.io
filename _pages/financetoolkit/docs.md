---
title: Docs
excerpt: This the documentation of the FinanceToolkit. This is an open-source toolkit in which all relevant financial ratios (50+), indicators and performance measurements are written down in the most simplistic way allowing for complete transparency of the calculation method.
description: This the documentation of the FinanceToolkit. This is an open-source toolkit in which all relevant financial ratios (50+), indicators and performance measurements are written down in the most simplistic way allowing for complete transparency of the calculation method.
author_profile: false
permalink: /projects/financetoolkit/docs
classes: wide-sidebar
layout: single
redirect_from:
  - /docs
sidebar:
  nav: "financetoolkit-docs"
---

This page includes all the documentation for the Finance Toolkit. Each functionality includes an example of how to use it and is therefore an excellent way to better understand how to use each functionality. These examples are also directly embedded in the code. For simplicity sake, only the controller modules are included here given that the models themselves should be relatively straightforward. Make sure to also have a look at the example notebooks as found [here](/projects/financetoolkit#how-to-guides-for-the-financetoolkit).

{% include docstring_viewer.html
fileUrl='https://api.github.com/repos/JerBouma/FinanceToolkit/contents/financetoolkit/base/toolkit_controller.py'
title='Toolkit Module'
description='The Toolkit Module is meant to be a collection of useful functions that collect and parse data. These is historical data, fundamental data (balance, income and cash flow statements) as well as several others metrics from Financial Modeling Prep like enterprise values, company profiles and more. From this module, you are able to access the related modules as well.' %}

{% include docstring_viewer.html
fileUrl='https://api.github.com/repos/JerBouma/FinanceToolkit/contents/financetoolkit/base/ratios_controller.py'
title='Ratios Module'
description='The Ratios Module contains over 50+ ratios that can be used to analyse companies. These ratios are divided into 5 categories: profitability, liquidity, solvency, efficiency and valuation. Each ratio is calculated using the data from the Toolkit module.' %}

{% include docstring_viewer.html
fileUrl='https://api.github.com/repos/JerBouma/FinanceToolkit/contents/financetoolkit/base/models_controller.py'
title='Models Module'
description='The Models module is meant to execute well-known models such as DUPONT and the Discounted Cash Flow (DCF) model. These models are also directly related to the data retrieved from the Toolkit module.' %}
