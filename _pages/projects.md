---
permalink: /projects
title: Projects
excerpt: Much of the Finance theory I have learned, I apply within Python which I have spend thousands of hours developing in. This is in the fields of Data Science & Machine Learning, Fundamental, Algorithmic and Technical Analysis, GUIs and web-based dashboards as well as various other topics. On this page you are able to find all major Python projects I am actively maintaining.
description: Much of the Finance theory I have learned, I apply within Python which I have spend thousands of hours developing in. This is in the fields of Data Science & Machine Learning, Fundamental, Algorithmic and Technical Analysis, GUIs and web-based dashboards as well as various other topics. On this page you are able to find all major Python projects I am actively maintaining.
classes: wide-no-sidebar
author_profile: false
---
<div class="row">
<div markdown="1" class="sixty-column mobile-max-column-width" markdown="1">
When I discovered Python during my time in University, I was immediately captivated by its incredible versatility in the financial domain. Since then, I have devoted countless hours to programming in this language, whether it's developing internal models for companies like a.s.r. asset management and PGGM or contributing to open-source projects (as demonstrated on this page). Witnessing the repetition of models and calculations within financial institutions has made me a strong advocate for open-source, as it liberates individuals and firms from relying solely on proprietary models.
</div>
<div markdown="1" class="fourty-column mobile-max-column-width" markdown="1">

[![Jeroen Bouma's GitHub stats](https://github-readme-stats.vercel.app/api?username=JerBouma&show_icons=true&theme=graywhite&include_all_commits=true&count_private=true&hide=contribs)](https://github.com/JerBouma){:target="_blank"}
</div>
</div>

{: .notice--info}
**Looking to get into Financial Modelling?**<br>
Have a look at my [in-depth guide on Financial Modelling with Python](/modelling/introduction){: target="_blank"} which goes over the basics, setting up a project, structure, build and test a financial model. The purpose with this guide is to share my findings over the years and common mistakes that I've found both in open-source and proprietary models.

## [Finance Toolkit](/projects/financetoolkit)

<div class="row">
<div markdown="1" class="sixty-column mobile-max-column-width">
This package is an open-source toolkit in which 100+ financial ratios indicators and performance measurements are written down in the most simplistic way allowing for complete transparency of the calculation method. This allows you to not have to rely on metrics from other providers and, given a financial statement, allow for efficient manual calculations. This leads to one uniform method of calculation being applied that is available and understood by everyone.

The Finance Toolkit is complimented very well with the Finance Database and by utilising both, it is possible to do a fully-fledged competitive analysis with the tickers found from the FinanceDatabase inputted into the FinanceToolkit.

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
This database features 300.000+ symbols containing Equities, ETFs, Funds, Indices, Currencies, Cryptocurrencies and Money Markets. It therefore allows you to obtain a broad overview of sectors, industries, types of investments and much more.

The aim of this database is explicitly not to provide up-to-date fundamentals or stock data as those can be obtained with ease (with the help of this database) by using yfinance or FundamentalAnalysis. Instead, it gives insights into the products that exist in each country, industry and sector and gives the most essential information about each product. With this information, you can analyse specific areas of the financial world and/or find a product that is hard to find.

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
With a large increase in ETFs available, it can become difficult to make the best choice in what you wish to invest. There are many different providers (iShares, Vanguard, Invesco) as well as with changes to the underlying stocks (i.e. High Yield, Super Dividends, Equal Weighted).

This is quickly reflected when looking for a S&P 500 ETF as there are over 20 different ETFs available. With this package, I wish to make investment decisions easier to make and manage.

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
With PersonalFinance I want to make it easier to manage your personal finance. Through defining each category with appropriate keywords, you can be sure that the model will categorise transactions how you defined them. This is because it is not a generic model that is trained on a large dataset of transactions from all over the world. It is trained on your own data, which means that it will be able to categorise transactions that are specific to you.

To assist in not needing to get *exact* matches, the package makes use of the Levenshtein distance to determine how similar two strings are. There is a limited amount of Mumbo Jumbo going on here on purpose so that it still becomes logical why it is categorised as such.

[View this Project](/projects/personalfinance){: .btn .btn--info}
</div>
<div markdown="1" class="fourty-column mobile-max-column-width">
<a href="/projects/personalfinance"><img src="https://github-production-user-asset-6210df.s3.amazonaws.com/46355364/275324611-33a88b7d-f48f-42f0-83ae-d0950a3aed6e.jpg" width="400"></a>
[![Readme Card](https://github-readme-stats.vercel.app/api/pin/?username=jerbouma&repo=personalfinance)](/projects/personalfinance)

[![PyPi Version](https://img.shields.io/pypi/v/personalfinance)](https://pypi.org/project/financedatabase/){:target="_blank"}
[![PYPI Downloads](https://static.pepy.tech/badge/personalfinance/month)](https://pepy.tech/project/personalfinance){:target="_blank"}
</div>
</div>

## [OpenBB](/projects/openbbterminal)

<div class="row">
<div markdown="1" class="sixty-column mobile-max-column-width">
The OpenBB Platform offers access to equity, options, crypto, forex, macro economy, fixed income, and more while also offering a broad range of extensions to enhance the user experience according to their needs.

During my time at OpenBB, I have made major code contributions to the OpenBB Platform, formerly known as the OpenBB Terminal. These are in the area of Macro and Micro Economics, Econometrics, Fundamental Analysis and much more. I am proud having worked on this project and I am excited to see where it will go in the future. Being a competitor to Bloomberg, Reuters and FactSet, OpenBB is a platform that is here to stay.

[View this Project](/projects/openbbterminal){: .btn .btn--info}
</div>
<div markdown="1" class="fourty-column mobile-max-column-width">
<a href="/projects/openbbterminal"><img src="https://github.com/OpenBB-finance/OpenBBTerminal/raw/develop/images/openbb_gradient.png" width="400"></a>
[![Readme Card](https://github-readme-stats.vercel.app/api/pin/?username=OpenBB-finance&repo=OpenBBTerminal)](/projects/openbbterminal)

[![PyPi Version](https://img.shields.io/pypi/v/openbb)](https://pypi.org/project/openbb/){:target="_blank"}
[![PYPI Downloads](https://static.pepy.tech/badge/openbb/month)](https://pepy.tech/project/openbb){:target="_blank"}
</div>
</div>