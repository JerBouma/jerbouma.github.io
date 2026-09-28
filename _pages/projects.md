---
title: Projects
permalink: /projects
excerpt: I apply much of the finance theory I've learned using Python.
description: I apply much of the finance theory I've learned using Python.
layout: single
classes: custom-document
author_profile: false
---
<div class="row">
<div markdown="1" class="sixty-column mobile-max-column-width" markdown="1">
I discovered Python during my university studies and quickly saw how much it could do in finance. Since then I have spent a lot of my time programming in it, both building internal models at companies like a.s.r. asset management and PGGM and working on the open-source projects on this page.

At financial institutions I kept seeing the same models and calculations being built again and again. That made me a strong advocate for open source, because it means people and firms no longer have to rely only on proprietary models. By sharing my work openly, I want to make financial knowledge and tools available to anyone who wants to use them, and give others something to build on.
</div>
<div markdown="1" class="fourty-column mobile-max-column-width" markdown="1">

<div class="github-profile-card">
  <div class="github-card-header">
    <img src="https://avatars.githubusercontent.com/u/46355364?v=4" alt="Jeroen Bouma" class="github-card-avatar">
    <div class="github-card-identity">
      <strong>Jeroen Bouma</strong>
      <span class="github-card-username">@JerBouma</span>
    </div>
  </div>
  <div class="github-card-stats">
    <div class="github-stat">
      <span class="github-stat-value" id="gh-repos">—</span>
      <span class="github-stat-label">Repos</span>
    </div>
    <div class="github-stat">
      <span class="github-stat-value" id="gh-followers">—</span>
      <span class="github-stat-label">Followers</span>
    </div>
    <div class="github-stat">
      <span class="github-stat-value">10K+</span>
      <span class="github-stat-label">Stars</span>
    </div>
  </div>
  <a href="https://github.com/JerBouma" class="btn btn--info github-card-cta" target="_blank">View GitHub Profile</a>
</div>

<script>
fetch('https://api.github.com/users/JerBouma')
  .then(function(r) { return r.json(); })
  .then(function(data) {
    var repos = document.getElementById('gh-repos');
    var followers = document.getElementById('gh-followers');
    if (repos) repos.textContent = data.public_repos;
    if (followers) followers.textContent = data.followers >= 1000
      ? (data.followers / 1000).toFixed(1) + 'K'
      : data.followers;
  })
  .catch(function() {});
</script>
</div>
</div>

{: .notice--info}
**Looking to get into Financial Modelling?**<br>
Have a look at my [guide on Financial Modelling with Python](/modelling/introduction){: target="_blank"}, which covers the basics, project setup, structure, and how to build and test a financial model. In it I share what I have learned over the years and point out common mistakes I've seen in both open-source and proprietary models.

## [Finance Toolkit](/projects/financetoolkit)

<div class="row">
<div markdown="1" class="sixty-column mobile-max-column-width">
This open-source package contains 500+ financial methods, from ratios and indicators to performance measurements. Each one is implemented in a straightforward way, so you can see exactly how it is calculated. That means you do not have to rely on metrics from external providers: you calculate them directly from the financial statements, using the same method every time, and anyone can read and understand how.

The Finance Toolkit works well together with the Finance Database. You can take tickers from the Finance Database and use them as input for the Finance Toolkit to do a full competitive analysis.

[View this Project](/projects/financetoolkit){: .btn .btn--info}
</div>
<div markdown="1" class="fourty-column mobile-max-column-width">
<a href="/projects/financetoolkit"><img src="https://user-images.githubusercontent.com/46355364/242269801-198d47bd-e1b3-492d-acc4-5d9f02d1d009.jpg" alt="Finance Toolkit project banner" width="400"></a>

[![GitHub Stars](https://img.shields.io/github/stars/JerBouma/financetoolkit?style=social)](https://github.com/JerBouma/financetoolkit){:target="_blank"}
[![GitHub Forks](https://img.shields.io/github/forks/JerBouma/financetoolkit?style=social)](https://github.com/JerBouma/financetoolkit){:target="_blank"}
[![PyPi Version](https://img.shields.io/pypi/v/financetoolkit)](https://pypi.org/project/financetoolkit/){:target="_blank"}
[![PYPI Downloads](https://static.pepy.tech/badge/financetoolkit/month)](https://pepy.tech/projects/financetoolkit){:target="_blank"}
</div>
</div>

## [Finance Toolkit MCP](/projects/financetoolkit/mcp)

<div class="row">
<div markdown="1" class="sixty-column mobile-max-column-width">
The Finance Toolkit MCP Server makes the 500+ methods of the Finance Toolkit available to any AI assistant that supports the Model Context Protocol (MCP). You can ask Claude, ChatGPT, Cursor, Copilot or any other MCP-compatible assistant in plain English to analyse equities, benchmark performance, look at macro conditions or run technical indicators. Every number is computed with the same open-source formulas as the Python package.

The server is available in two flavours that expose exactly the same tools: a hosted remote server that needs nothing installed, and a local server that runs on your own machine through `uvx`.

[View this Project](/projects/financetoolkit/mcp){: .btn .btn--info}
</div>
<div markdown="1" class="fourty-column mobile-max-column-width">
<a href="/projects/financetoolkit/mcp"><img src="/assets/images/projects/FinanceToolkitMCP.jpg" alt="Finance Toolkit MCP Server project banner" width="400"></a>

[![GitHub Stars](https://img.shields.io/github/stars/JerBouma/financetoolkit?style=social)](https://github.com/JerBouma/financetoolkit){:target="_blank"}
[![GitHub Forks](https://img.shields.io/github/forks/JerBouma/financetoolkit?style=social)](https://github.com/JerBouma/financetoolkit){:target="_blank"}
[![PyPi Version](https://img.shields.io/pypi/v/financetoolkit)](https://pypi.org/project/financetoolkit/){:target="_blank"}
[![PYPI Downloads](https://static.pepy.tech/badge/financetoolkit/month)](https://pepy.tech/projects/financetoolkit){:target="_blank"}
</div>
</div>

## [Finance Database](/projects/financedatabase)

<div class="row">
<div markdown="1" class="sixty-column mobile-max-column-width">
This database contains over 300,000 symbols, including Equities, ETFs, Funds, Indices, Currencies, Cryptocurrencies, and Money Markets. It gives you a broad overview of sectors, industries, investment types and more.

The database deliberately does not provide up-to-date fundamentals or stock data, since you can easily get these (using symbols from this database) with tools like yfinance or FundamentalAnalysis. What it does show is which products are available in each country, industry and sector, with the basic information about each one. You can use that to analyze a specific part of the financial world or to find products that are otherwise hard to find.

[View this Project](/projects/financedatabase){: .btn .btn--info}
</div>
<div markdown="1" class="fourty-column mobile-max-column-width">
<a href="/projects/financedatabase"><img src="https://user-images.githubusercontent.com/46355364/220746807-669cdbc1-ac67-404c-b0bb-4a3d67d9931f.jpg" alt="Finance Database project banner" width="400"></a>

[![GitHub Stars](https://img.shields.io/github/stars/JerBouma/financedatabase?style=social)](https://github.com/JerBouma/financedatabase){:target="_blank"}
[![GitHub Forks](https://img.shields.io/github/forks/JerBouma/financedatabase?style=social)](https://github.com/JerBouma/financedatabase){:target="_blank"}
[![PyPi Version](https://img.shields.io/pypi/v/financedatabase)](https://pypi.org/project/financedatabase/){:target="_blank"}
[![PYPI Downloads](https://static.pepy.tech/badge/financedatabase/month)](https://pepy.tech/projects/financedatabase){:target="_blank"}
</div>
</div>

## [OpenBB](/projects/openbbterminal)

<div class="row">
<div markdown="1" class="sixty-column mobile-max-column-width">
The OpenBB Platform provides access to data on equities, options, crypto, forex, macroeconomics, fixed income, and more. It also has a wide range of extensions, so you can set it up the way you want.

During my time at OpenBB, I contributed a lot of code to the OpenBB Platform (formerly the OpenBB Terminal), mostly in areas such as Macro and Microeconomics, Econometrics and Fundamental Analysis. I am proud to have worked on it and look forward to seeing where it goes next. OpenBB competes with Bloomberg, Reuters and FactSet, and I expect it to have an impact for a long time.

[View this Project](/projects/openbbterminal){: .btn .btn--info}
</div>
<div markdown="1" class="fourty-column mobile-max-column-width">
<a href="/projects/openbbterminal"><img src="https://github.com/OpenBB-finance/OpenBB/raw/develop/images/openbb_gradient.png" alt="OpenBB Terminal project banner" width="400"></a>

[![GitHub Stars](https://img.shields.io/github/stars/OpenBB-finance/OpenBB?style=social)](https://github.com/OpenBB-finance/OpenBB){:target="_blank"}
[![GitHub Forks](https://img.shields.io/github/forks/OpenBB-finance/OpenBB?style=social)](https://github.com/OpenBB-finance/OpenBB){:target="_blank"}
[![PyPi Version](https://img.shields.io/pypi/v/openbb)](https://pypi.org/project/openbb/){:target="_blank"}
[![PYPI Downloads](https://static.pepy.tech/badge/openbb/month)](https://pepy.tech/projects/openbb){:target="_blank"}
</div>
</div>

## [The Passive Investor](/projects/thepassiveinvestor)

<div class="row">
<div markdown="1" class="sixty-column mobile-max-column-width">
With the large increase in available ETFs, choosing the best investment can be challenging. Numerous providers exist (iShares, Vanguard, Invesco), and ETFs vary based on underlying strategies (e.g., High Yield, Super Dividends, Equal Weighted).

This variety is evident when searching for an S&P 500 ETF, where over 20 different options are available. With this package, I want to make investment decisions easier to make and manage.

[View this Project](/projects/thepassiveinvestor){: .btn .btn--warning}

</div>
<div markdown="1" class="fourty-column mobile-max-column-width">
<a href="/projects/thepassiveinvestor"><img src="https://github.com/JerBouma/ThePassiveInvestor/assets/46355364/48f40d07-bbc7-47c0-ae22-9cdb30a9308f" alt="The Passive Investor project banner" width="400"></a>

[![GitHub Stars](https://img.shields.io/github/stars/JerBouma/thepassiveinvestor?style=social)](https://github.com/JerBouma/thepassiveinvestor){:target="_blank"}
[![GitHub Forks](https://img.shields.io/github/forks/JerBouma/thepassiveinvestor?style=social)](https://github.com/JerBouma/thepassiveinvestor){:target="_blank"}
[![PyPi Version](https://img.shields.io/pypi/v/thepassiveinvestor)](https://pypi.org/project/thepassiveinvestor/){:target="_blank"}
[![PYPI Downloads](https://static.pepy.tech/badge/thepassiveinvestor/month)](https://pepy.tech/projects/thepassiveinvestor){:target="_blank"}

*This project has been archived because I no longer maintain it.*
</div>
</div>

## [Personal Finance](/projects/personalfinance)

<div class="row">
<div markdown="1" class="sixty-column mobile-max-column-width">
With PersonalFinance, I wanted to make managing your personal finances simpler. You define categories with the keywords that belong to them, and the model categorizes your transactions accordingly. This works well because the model is trained on your own data rather than on a large, generic dataset of transactions from around the world, so it sorts transactions based on your own financial habits.

To handle variations without requiring exact matches, the package uses the Levenshtein distance to measure string similarity. I kept complex logic to a minimum on purpose, so it stays easy to see why a transaction ends up in a certain category.

[View this Project](/projects/personalfinance){: .btn .btn--warning}
</div>
<div markdown="1" class="fourty-column mobile-max-column-width">
<a href="/projects/personalfinance"><img src="https://github-production-user-asset-6210df.s3.amazonaws.com/46355364/275324611-33a88b7d-f48f-42f0-83ae-d0950a3aed6e.jpg" alt="Personal Finance project banner" width="400"></a>

[![GitHub Stars](https://img.shields.io/github/stars/JerBouma/personalfinance?style=social)](https://github.com/JerBouma/personalfinance){:target="_blank"}
[![GitHub Forks](https://img.shields.io/github/forks/JerBouma/personalfinance?style=social)](https://github.com/JerBouma/personalfinance){:target="_blank"}
[![PyPi Version](https://img.shields.io/pypi/v/personalfinance)](https://pypi.org/project/personalfinance/){:target="_blank"}
[![PYPI Downloads](https://static.pepy.tech/badge/personalfinance/month)](https://pepy.tech/projects/personalfinance){:target="_blank"}

*This project has been archived because I no longer maintain it.*
</div>
</div>