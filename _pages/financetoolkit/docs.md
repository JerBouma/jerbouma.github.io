---
title: Docs
excerpt: I am strongly analytical, have a keen sense of long-term investment strategy and have a “can do” attitude. This is proven by my achievements within the Finance domain by working as an ALM Advisor at PGGM, one of the largest pension funds in the Netherlands, and working as a Product Manager for OpenBB, a fintech start-up democratising access to investment research. Furthermore, I have a strong educational background in Finance, CFA level 1 and the post-master education titled Registered Financial Analyst (VBA/RBA) completed. This education not only discusses much of the relevant theory but also gives many examples of how these theories are currently applied within a multitude of different investment organisations.
description: I am strongly analytical, have a keen sense of long-term investment strategy and have a “can do” attitude. This is proven by my achievements within the Finance domain by working as an ALM Advisor at PGGM, one of the largest pension funds in the Netherlands, and working as a Product Manager for OpenBB, a fintech start-up democratising access to investment research. Furthermore, I have a strong educational background in Finance, CFA level 1 and the post-master education titled Registered Financial Analyst (VBA/RBA) completed. This education not only discusses much of the relevant theory but also gives many examples of how these theories are currently applied within a multitude of different investment organisations.
author_profile: false
permalink: /projects/financetoolkit/docs/
classes: wide-sidebar
layout: single
redirect_from:
  - /docs
sidebar:
  nav: "financetoolkit-docs"
---

This page includes all the documentation for the Finance Toolkit. Each functionality includes an example of how to use it and is therefore an excellent way to better understand how to use each functionality. These examples are also directly embedded in the code. For simplicity sake, only the controller modules are included here given that the models themselves should be relatively straightforward. Make sure to also have a look at the example notebooks as found [here](/projects/financetoolkit/#how-to-guides-for-the-financetoolkit).

{% include docstring_viewer.html
fileUrl='https://api.github.com/repos/JerBouma/FinanceToolkit/contents/financetoolkit/base/toolkit_controller.py'
title='## Toolkit Module'
description='The Toolkit Module is meant to be a collection of useful functions that collect and parse data. These is historical data, fundamental data (balance, income and cash flow statements) as well as several others metrics from Financial Modeling Prep like enterprise values, company profiles and more. From this module, you are able to access the related modules as well.' %}

{% include docstring_viewer.html
fileUrl='https://api.github.com/repos/JerBouma/FinanceToolkit/contents/financetoolkit/base/ratios_controller.py'
title='## Ratios module'
description='The Ratios Module contains over 50+ ratios that can be used to analyse companies. These ratios are divided into 5 categories: profitability, liquidity, solvency, efficiency and valuation. Each ratio is calculated using the data from the Toolkit module.' %}

{% include docstring_viewer.html
fileUrl='https://api.github.com/repos/JerBouma/FinanceToolkit/contents/financetoolkit/base/models_controller.py'
title='## Models Module'
description='The Models module is meant to execute well-known models such as DUPONT and the Discounted Cash Flow (DCF) model. These models are also directly related to the data retrieved from the Toolkit module.' %}
