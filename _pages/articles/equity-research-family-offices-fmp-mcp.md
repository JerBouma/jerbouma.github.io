---
title: "The Research Team You Can't Afford to Hire: Equity Research for Family Offices with the FMP MCP Server"
seo_title: "Equity Research for Family Offices with AI"
date: 2026-07-23
last_modified_at: 2026-07-26
permalink: /articles/equity-research-family-offices-fmp-mcp
excerpt: "A practical look at running equity research diligence for a concentrated portfolio using the FMP MCP server in Claude Desktop, prompt by prompt."
description: "How family offices can run equity research diligence, from financial health to insider activity and ownership, with the FMP MCP server in Claude Desktop."
layout: single
classes: wide-sidebar article-document
author_profile: false
collection: article
tags: [MCP Server, Fundamental Analysis]
share: true
---

A family office running $150 million usually doesn't have a five-person research desk, and neither does a small fund with eight names in the book. The diligence bar doesn't drop with the headcount, though. If anything it goes up: in a concentrated portfolio every position carries real weight, and there's no long tail of other holdings to average out a mistake.

That is where the FMP MCP server is useful. It doesn't replace judgment, but it does compress the mechanical part of diligence (pulling statements, estimates, insider filings, and institutional flow) into a conversation in Claude Desktop. The alternative is a terminal subscription that costs more than a junior analyst's salary and still needs someone to operate it.

Below I walk through an equity research pass on Axon Enterprise (AXON), the maker of Tasers and body cameras for law enforcement, using the FMP MCP server end to end. I ran every prompt below against the FMP MCP before writing this, so what's described is what it actually returned.

**For more information on the FMP MCP server, see [FMP's documentation](https://site.financialmodelingprep.com/developer/docs/mcp-server){:target="_blank"}. To see what it adds on top of FMP, have a look at the [Finance Toolkit MCP server](/projects/financetoolkit/mcp).**

## Setting Things Up

The FMP MCP server connects to Claude Desktop as a remote connector, so there is nothing to install locally. Under Settings, then Connectors, then Add custom connector, the URL follows this pattern:

```
https://financialmodelingprep.com/mcp?apikey=FINANCIAL_MODELING_PREP_KEY
```

Paste that in with your key, give it a name, and Claude has direct access to FMP's statements, analyst data, insider filings, and institutional ownership records for the rest of the session.

Get an API key at [jeroenbouma.com/fmp](/fmp){:target="_blank"}. The free tier covers 250 requests a day, which is plenty to run everything below.

## Building the Diligence File: Financial Health at a Glance

Any investment story first needs the numbers to support it. FMP's key metrics endpoint bundles return on equity, return on invested capital, and EV/EBITDA into a single call, the kind of thing that normally means pulling three statements and building the ratios by hand.

![Claude Desktop response showing AXON's ROE, ROIC, and EV/EBITDA trend](/assets/images/articles/equity-research-family-offices-fmp-mcp/financial-health-metrics.png)

*"Pull Axon Enterprise's (AXON) key financial metrics for the last five fiscal years and show me how ROE, ROIC, and EV/EBITDA have moved."*

This is uncomfortable on its own: ROIC peaked in 2023 at 6% and has since gone negative, while the EV/EBITDA multiple more than doubled over the same stretch, past 236x by 2025. The multiple is expanding faster than the returns funding it, and that tension is worth flagging before sizing a position.

## Where the Market Disagrees With Itself: Analyst Estimates and Price Targets

A small fund without in-house sell-side coverage can still use consensus, as long as it doesn't treat it as a target to chase. The spread between analysts is usually more useful than the average.

![Claude Desktop response showing AXON's analyst price targets and revenue and EPS estimates](/assets/images/articles/equity-research-family-offices-fmp-mcp/analyst-estimates-price-targets.png)

*"Show me the current analyst price target range and consensus for AXON, plus 2026 through 2028 revenue and EPS estimates."*

The response comes back in two parts. The price targets show a consensus of $658.56 against a share price of $510.28 that day, about 22.5% below where analysts collectively see it heading, or roughly 29% upside. The estimates further out are more revealing: by 2028, the analysts covering AXON put net income anywhere from $573 million to $1.81 billion, a range wider than the company's entire 2025 net income. They agree on the revenue trajectory and disagree sharply on what margin structure survives three years out, and that disagreement says more than the consensus price target does.

## A Sanity Check on Valuation

A DCF is a pressure test: does the current price only make sense under aggressive assumptions, or does it hold up under conservative ones? That matters more when a fund holds six positions than when it holds three hundred, because there's no portfolio-level averaging to absorb being wrong on one name.

![Claude Desktop response showing a levered DCF valuation for AXON versus its share price](/assets/images/articles/equity-research-family-offices-fmp-mcp/dcf-valuation.png)

*"Run a levered discounted cash flow valuation on AXON and compare it to the current share price."*

The number that comes back looks alarming at first: a DCF value of $94.30 against a share price of $510.28. The model isn't really saying the market is wrong. A standard WACC-and-terminal-growth template can't capture a company compounding revenue in the 30%+ range, so the entire bull case for AXON has to be carried by assumptions the template doesn't make for you. Running this doesn't answer the valuation question, but it does show how much of the investment case rests on judgment rather than arithmetic, which is worth knowing before writing the position up.

## What Management Actually Said

Ratios describe what already happened, while earnings calls are often the only source for what management believes is coming. Tracking how the language shifts from quarter to quarter is a real edge for a team that can't sit in on every call live.

![Claude Desktop response showing AXON's most recent earnings call transcript](/assets/images/articles/equity-research-family-offices-fmp-mcp/earnings-call-transcript.png)

*"Pull the transcript from AXON's most recent earnings call and tell me what the CEO said about growth."*

Claude pulls the full Q1 2026 transcript from May 6, 2026, and picks out the key line: CEO Patrick Smith telling investors "I'm more convinced than ever that we're building something the world genuinely needs... Today, I think we passed the inflection point." "Passed the inflection point" is the kind of phrase worth tracking against what the same person said the quarter before and the quarter after. Done manually across a dozen transcripts, that is not a two-minute exercise, which is why most small teams don't do it and why it's worth automating.

## Following the Insiders

Insider selling is often read as a bad signal by reflex, but most of it is small, scheduled, and meaningless. The actual job is telling routine activity apart from something that changes the picture.

![Claude Desktop response showing AXON's most recent insider transactions](/assets/images/articles/equity-research-family-offices-fmp-mcp/insider-transactions.png)

*"Show me the most recent insider transactions for AXON, including who traded, how much, and at what price."*

The transactions that come back show Patrick Smith selling in small tranches, and a couple of newly appointed directors also picked up small stock awards around the same time. None of it looks conviction-driven; it looks like a scheduled 10b5-1 plan doing what it's built to do. Being able to rule something out with confidence is worth as much here as spotting a real signal.

## Who Else Is In This Trade

Before taking a meaningful position, it helps to know whether a fund is early or late relative to institutional flow. A stock where ownership just climbed from 80% to 83% of float in one quarter is a different setup than one where the same institutions are quietly leaving.

![Claude Desktop response showing AXON's institutional ownership trends from 13F filings](/assets/images/articles/equity-research-family-offices-fmp-mcp/institutional-ownership.png)

*"Show me institutional ownership trends for AXON from the latest 13F filings, including how many holders opened new positions versus closed them."*

The result is more mixed than a single snapshot would suggest. Total institutional holders slipped from 1,250 in Q2 2025 to 1,101 by Q1 2026, and the balance between new positions opened and positions closed has flipped, from a net of +142 two quarters ago to -95 in the latest filing. Ownership of float has actually held up, sitting at 83.3% versus 82.7% a year earlier, which means existing holders are largely staying put even as fewer new funds step in and more trim out. That points to interest cooling off rather than a rush for the exit.

## Where FMP Stops and the Finance Toolkit MCP Picks Up

Everything above comes straight out of FMP's raw endpoints, and for pulling a specific number, filing, or quarter, that's the right tool. What it does only to a more limited extent is combine those raw numbers into the computed research output an analyst would also like to see, such as a Piotroski score, a Sharpe ratio against a benchmark, a five-factor Fama-French regression, or a DuPont breakdown of what's actually driving ROE.

The [Finance Toolkit MCP](/projects/financetoolkit/mcp) extends FMP's endpoints in that direction. It's built directly on top of FMP's data, using the same API key, so there's no second account or separate integration to manage.

![Claude Desktop response showing the Finance Toolkit MCP's health overview across efficiency, liquidity, profitability, solvency, valuation, performance, and risk for AXON](/assets/images/articles/equity-research-family-offices-fmp-mcp/finance-toolkit-health-overview.png)

*"Explore the areas of efficiency, liquidity, profitability, solvency, valuation, performance and risk for AXON. How healthy is the company?"*

There is little friction between the two: ask for a ratio the Finance Toolkit computes, and it pulls the underlying statements from FMP, runs the calculation, and returns the answer in the same conversation, with the same connector setup.

For a family office or small fund already running the prompts above, adding the Finance Toolkit MCP as a second connector puts computed analysis on top of the raw data pulls, without turning a two-person team into a data engineering project.
