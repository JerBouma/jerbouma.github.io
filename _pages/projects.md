---
permalink: /projects
title: Projects
excerpt: I apply much of the finance theory I've learned using Python, a language in which I have invested thousands of development hours. My work spans Data Science & Machine Learning, Fundamental, Algorithmic, and Technical Analysis, GUIs, web-based dashboards, and various other topics. On this page, you can find all the major Python projects I actively maintain.
description: I apply much of the finance theory I've learned using Python, a language in which I have invested thousands of development hours. My work spans Data Science & Machine Learning, Fundamental, Algorithmic, and Technical Analysis, GUIs, web-based dashboards, and various other topics. On this page, you can find all the major Python projects I actively maintain.
classes: wide-no-sidebar
author_profile: false
---
<div class="row">
<div markdown="1" class="sixty-column mobile-max-column-width" markdown="1">
When I discovered Python during my university studies, I was immediately captivated by its incredible versatility in the financial domain. Since then, I have devoted countless hours to programming in this language, whether developing internal models for companies like a.s.r. asset management and PGGM or contributing to open-source projects (as demonstrated on this page). Witnessing the repetition of models and calculations within financial institutions has made me a strong advocate for open source, as it liberates individuals and firms from relying solely on proprietary models.
</div>
<div markdown="1" class="fourty-column mobile-max-column-width" markdown="1">

[![Jeroen Bouma's GitHub stats](https://github-readme-stats.vercel.app/api?username=JerBouma&show_icons=true&theme=graywhite&include_all_commits=true&count_private=true&hide=contribs)](https://github.com/JerBouma){:target="_blank"}
</div>
</div>

{: .notice--info}
**Looking to get into Financial Modelling?**<br>
Have a look at my [in-depth guide on Financial Modelling with Python](/modelling/introduction){: target="_blank"}, which covers the basics, project setup, structure, and how to build and test a financial model. The purpose of this guide is to share my findings over the years and highlight common mistakes I've observed in both open-source and proprietary models.

## [Finance Toolkit](/projects/financetoolkit)

<div class="row">
<div markdown="1" class="sixty-column mobile-max-column-width">
This open-source package provides over 150 financial ratios, indicators, and performance measurements, implemented straightforwardly to ensure complete transparency of the calculation methods. This enables you to avoid reliance on metrics from external providers and perform efficient calculations directly from financial statements. It promotes a uniform calculation method that is accessible and understandable to everyone.

The Finance Toolkit complements the Finance Database well. By utilizing both, you can perform a comprehensive competitive analysis using tickers from the Finance Database as input for the Finance Toolkit.

[View this Project](/projects/financetoolkit){: .btn .btn--info}
</div>
<div markdown="1" class="fourty-column mobile-max-column-width">
<a href="/projects/financetoolkit"><img src="https://user-images.githubusercontent.com/46355364/242269801-198d47bd-e1b3-492d-acc4-5d9f02d1d009.jpg" width="400"></a>
[![Readme Card](https://github-readme-stats.vercel.app/api/pin/?username=jerbouma&repo=financetoolkit)](/projects/financetoolkit)

[![PyPi Version](https://img.shields.io/pypi/v/financetoolkit)](https://pypi.org/project/financetoolkit/){:target="_blank"}
[![PYPI Downloads](https://static.pepy.tech/badge/financetoolkit/month)](https://pepy.tech/project/financetoolkit){:target="_blank"}
</div>
</div>

## [Finance Database](/projects/financedatabase)

<div class="row">
<div markdown="1" class="sixty-column mobile-max-column-width">
This database features over 300,000 symbols, including Equities, ETFs, Funds, Indices, Currencies, Cryptocurrencies, and Money Markets. It allows you to gain a broad overview of sectors, industries, investment types, and much more.

The explicit aim of this database is not to provide up-to-date fundamentals or stock data, as these can be easily obtained (using symbols from this database) with tools like yfinance or FundamentalAnalysis. Instead, it provides insights into the products available in each country, industry, and sector, offering essential information about each one. With this information, you can analyze specific areas of the financial world or locate hard-to-find products.

[View this Project](/projects/financedatabase){: .btn .btn--info}
</div>
<div markdown="1" class="fourty-column mobile-max-column-width">
<a href="/projects/financedatabase"><img src="https://user-images.githubusercontent.com/46355364/220746807-669cdbc1-ac67-404c-b0bb-4a3d67d9931f.jpg" width="400"></a>
[![Readme Card](https://github-readme-stats.vercel.app/api/pin/?username=jerbouma&repo=financedatabase)](/projects/financedatabase)

[![PyPi Version](https://img.shields.io/pypi/v/financedatabase)](https://pypi.org/project/financedatabase/){:target="_blank"}
[![PYPI Downloads](https://static.pepy.tech/badge/financedatabase/month)](https://pepy.tech/project/financedatabase){:target="_blank"}
</div>
</div>

## [The Passive Investor](/projects/thepassiveinvestor)

<div class="row">
<div markdown="1" class="sixty-column mobile-max-column-width">
With the large increase in available ETFs, choosing the best investment can be challenging. Numerous providers exist (iShares, Vanguard, Invesco), and ETFs vary based on underlying strategies (e.g., High Yield, Super Dividends, Equal Weighted).

This variety is evident when searching for an S&P 500 ETF, where over 20 different options are available. With this package, I aim to simplify investment decision-making and management.

[View this Project](/projects/thepassiveinvestor){: .btn .btn--info}
</div>
<div markdown="1" class="fourty-column mobile-max-column-width">
<a href="/projects/thepassiveinvestor"><img src="https://github.com/JerBouma/ThePassiveInvestor/assets/46355364/48f40d07-bbc7-47c0-ae22-9cdb30a9308f" width="400"></a>
[![Readme Card](https://github-readme-stats.vercel.app/api/pin/?username=jerbouma&repo=thepassiveinvestor)](/projects/thepassiveinvestor)

[![PyPi Version](https://img.shields.io/pypi/v/thepassiveinvestor)](https://pypi.org/project/thepassiveinvestor/){:target="_blank"}
[![PYPI Downloads](https://static.pepy.tech/badge/thepassiveinvestor/month)](https://pepy.tech/project/thepassiveinvestor){:target="_blank"}
</div>
</div>

## [Personal Finance](/projects/personalfinance)

<div class="row">
<div markdown="1" class="sixty-column mobile-max-column-width">
With PersonalFinance, I aim to simplify personal finance management. By defining categories with appropriate keywords, you ensure the model categorizes transactions according to your specifications. This is effective because it's not a generic model trained on a large, diverse dataset of global transactions. Instead, it's trained on your data, enabling it to accurately categorize transactions specific to your financial habits.

To handle variations without requiring exact matches, the package uses the Levenshtein distance to measure string similarity. Complex logic is intentionally limited so that the categorization remains intuitive and understandable.

[View this Project](/projects/personalfinance){: .btn .btn--info}
</div>
<div markdown="1" class="fourty-column mobile-max-column-width">
<a href="/projects/personalfinance"><img src="https://github-production-user-asset-6210df.s3.amazonaws.com/46355364/275324611-33a88b7d-f48f-42f0-83ae-d0950a3aed6e.jpg" width="400"></a>
[![Readme Card](https://github-readme-stats.vercel.app/api/pin/?username=jerbouma&repo=personalfinance)](/projects/personalfinance)

[![PyPi Version](https://img.shields.io/pypi/v/personalfinance)](https://pypi.org/project/personalfinance/){:target="_blank"}
[![PYPI Downloads](https://static.pepy.tech/badge/personalfinance/month)](https://pepy.tech/project/personalfinance){:target="_blank"}
</div>
</div>

## [OpenBB](/projects/openbbterminal)

<div class="row">
<div markdown="1" class="sixty-column mobile-max-column-width">
The OpenBB Platform provides access to data on equities, options, crypto, forex, macroeconomics, fixed income, and more. It also offers a broad range of extensions to tailor the user experience.

During my time at OpenBB, I made significant code contributions to the OpenBB Platform (formerly the OpenBB Terminal). My contributions focused on areas such as Macro and Microeconomics, Econometrics, Fundamental Analysis, and more. I am proud to have worked on this project and excited about its future direction. As a competitor to Bloomberg, Reuters, and FactSet, OpenBB is a platform poised for long-term impact.

[View this Project](/projects/openbbterminal){: .btn .btn--info}
</div>
<div markdown="1" class="fourty-column mobile-max-column-width">
<a href="/projects/openbbterminal"><img src="https://github.com/OpenBB-finance/OpenBBTerminal/raw/develop/images/openbb_gradient.png" width="400"></a>
[![Readme Card](https://github-readme-stats.vercel.app/api/pin/?username=OpenBB-finance&repo=OpenBBTerminal)](/projects/openbbterminal)

[![PyPi Version](https://img.shields.io/pypi/v/openbb)](https://pypi.org/project/openbb/){:target="_blank"}
[![PYPI Downloads](https://static.pepy.tech/badge/openbb/month)](https://pepy.tech/project/openbb){:target="_blank"}
</div>
</div>