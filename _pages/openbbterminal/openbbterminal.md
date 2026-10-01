---
permalink: /projects/openbbterminal
title: OpenBB Terminal
excerpt: "My contributions to the OpenBB Platform, formerly the OpenBB Terminal, mostly in economics, econometrics and fundamental analysis."
description: "Jeroen Bouma's contributions to the OpenBB Terminal and OpenBB Platform, an open-source Bloomberg alternative: economics, econometrics and fundamentals."
classes: wide-no-sidebar
author_profile: false
redirect_from:
  - /openbbterminal
---
{%- assign pr = "https://github.com/openbq-org/OpenBB/pull/" -%}

<div class="page-header-action notebook-viewer-actions"><a href="https://github.com/openbq-org/OpenBB" target="_blank" rel="noopener"><i class="fab fa-github"></i> View on GitHub</a></div>

During my time at OpenBB, I made major code contributions to the OpenBB Platform, formerly known as the OpenBB Terminal, mostly in Macro and Micro Economics, Econometrics, Fundamental Analysis and Portfolio Analysis. OpenBB set out to compete with Bloomberg, Reuters and FactSet through open source, and I am proud to have worked on it.

I led many of the academic initiatives, presenting the software at several universities in Europe (see the [Appearances](/appearances) page), and shared a lot of my financial knowledge with the team. This also resulted in several presentations that were given at webinars and conferences. For more information about the platform itself, have a look at the website of [OpenBB](https://openbb.co/){:target="_blank"}.

<div class="obb-stats">
  <span><strong>83</strong>merged pull requests</span>
  <span><strong>Oct 2021 – Apr 2023</strong>first as a contributor, then as Product Manager</span>
  <span><strong>6</strong>areas of the terminal</span>
</div>

## What I worked on

Below is a summary of my pull requests, grouped by area. They relate to the OpenBB Terminal, the predecessor of the current OpenBB Platform. You can also [browse all of them on GitHub](https://github.com/openbq-org/OpenBB/pulls?q=is%3Apr+is%3Aclosed+author%3AJerBouma+sort%3Acomments-desc){:target="_blank"}.

### Before joining: bringing in my own projects

My first contributions came in October 2021, as an outside contributor. I added the [Finance Database]({{ pr }}869){:target="_blank"} to the Stocks and ETF menus, so you could look up companies and ETFs by sector, industry and country from within the terminal, and added [ETF reports]({{ pr }}857){:target="_blank"} based on The Passive Investor. A [ticker search]({{ pr }}945){:target="_blank"} in the Stocks menu followed. These contributions are what led to the job offer at OpenBB.

### Economy and macroeconomics

- [Upgraded the Economy menu]({{ pr }}1444){:target="_blank"} with macro data from EconDB and FRED, and the option to plot any combination of indicators together in one multi-axis chart.
- [Consumer Price Index]({{ pr }}4350){:target="_blank"} data for many countries.
- [Country performance]({{ pr }}4514){:target="_blank"}: nominal, real and forecasted GDP, government debt-to-GDP, deficits, revenue, spending, trust in government and the components of inflation such as food and energy, so countries can be compared side by side.
- Smaller improvements to the [macro data transformations]({{ pr }}4125){:target="_blank"} and the [treasury data]({{ pr }}4413){:target="_blank"} in the Fixed Income menu.

### Econometrics

- Built the [Econometrics menu]({{ pr }}1403){:target="_blank"}, which replaced the old Custom menu. It lets you load your own datasets next to data from the terminal and explore the relationships between them with OLS and panel regressions, Granger causality, cointegration, unit root and normality tests.
- Wrote the [Econometrics guide and an example routine]({{ pr }}1966){:target="_blank"} that walks through a full analysis.

### Fundamental analysis and stocks

- Added multi-year financial statements to the [Sector and Industry Analysis]({{ pr }}1341){:target="_blank"} menu, so companies within a sector could be compared over a longer horizon, and [adjusted the comparisons for currency]({{ pr }}1518){:target="_blank"}.
- [Merged the Due Diligence menu into Fundamental Analysis]({{ pr }}4055){:target="_blank"}, regrouping its functionality and making it far less dependent on Yahoo Finance, which often broke. This was followed by [removing the remaining reliance on yfinance]({{ pr }}4176){:target="_blank"} outside market data.
- [Moved the terminal to version 2 of the Finance Database]({{ pr }}4319){:target="_blank"}, which made searching through 180,000+ tickers much faster, and [improved the ticker search]({{ pr }}4084){:target="_blank"}.
- Reworked the [market cap and enterprise value]({{ pr }}4424){:target="_blank"} command to show its full history, which I used in the academic presentations.

### Portfolio analysis

- Added [portfolio attribution against a benchmark]({{ pr }}1773){:target="_blank"}: allocation differences by asset, sector, country and region, based on an order book you load yourself, to judge whether active management added value.
- Fixed the portfolio engine [assigning prices to the wrong tickers]({{ pr }}4147){:target="_blank"} and made portfolios from the [optimization menu]({{ pr }}4149){:target="_blank"} usable in the portfolio menu.
- Wrote the [Portfolio and Portfolio Optimization guides]({{ pr }}3357){:target="_blank"}.

### Documentation and guides

A large part of my work went into making the terminal understandable for new users.

- Started the [Guides]({{ pr }}1833){:target="_blank"}, a handbook explaining how each menu works, and wrote many of them: [Getting Started]({{ pr }}1837){:target="_blank"}, [Stocks]({{ pr }}1833){:target="_blank"}, [ETFs]({{ pr }}1973){:target="_blank"}, [Funds]({{ pr }}1979){:target="_blank"}, [Forex]({{ pr }}2011){:target="_blank"}, [Crypto]({{ pr }}2015){:target="_blank"}, [Economy]({{ pr }}2016){:target="_blank"} and [Scripts and Routines]({{ pr }}2027){:target="_blank"}.
- Connected the terminal to its documentation: the [`about` command]({{ pr }}2048){:target="_blank"} opens the documentation page of the menu or command you are in.
- Documented [every API key]({{ pr }}3780){:target="_blank"} the terminal supports and added [installation videos]({{ pr }}3903){:target="_blank"} for Windows, macOS, Docker, Python and the SDK.
- Added a [`survey` command]({{ pr }}2174){:target="_blank"} to collect user feedback.

<a href="https://github.com/openbq-org/OpenBB/pulls?q=is%3Apr+is%3Aclosed+author%3AJerBouma+sort%3Acomments-desc" target="_blank"><img width="1512" alt="My pull requests on the OpenBB repository" src="https://github.com/JerBouma/jerbouma.github.io/assets/46355364/b2fa3e34-63c2-4ad6-b2f3-b249f489983e"></a>
