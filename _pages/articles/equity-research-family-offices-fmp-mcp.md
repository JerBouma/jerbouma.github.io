---
title: "Equity Research for Family Offices with the FMP MCP Server"
seo_title: "Equity Research for Family Offices with AI"
date: 2026-07-23
last_modified_at: 2026-10-14
permalink: /articles/equity-research-family-offices-fmp-mcp
excerpt: "On July 17, 2026, Axon closed at $510.28, analysts averaged $658.56 and a DCF said $94.30. A full diligence pass for a concentrated portfolio, from returns to insider sales and 13F flows, run question by question through the FMP MCP server."
description: "How family offices can run equity research diligence, from financial health to insider activity and ownership, with the FMP MCP server in Claude Desktop."
layout: single
classes: wide-sidebar article-document
author_profile: false
collection: article
tags: [MCP Server, Fundamental Analysis]
share: true
---

On July 17, 2026, Axon Enterprise closed at $510.28. The analysts covering it put their average price target at $658.56, a standard levered discounted cash flow model put the shares at $94.30, and the company's return on invested capital for 2025 was negative. Three readings of the same stock, the highest price seven times the lowest, and each one comes from a different part of the diligence file.

A family office running $150 million usually doesn't have a five-person research desk to build that file, and neither does a small fund with eight names in the book. The diligence bar doesn't drop with the headcount, though. If anything it goes up: in a concentrated portfolio every position carries real weight, and there's no long tail of other holdings to average out a mistake. The FMP MCP server doesn't replace judgment, but it compresses the mechanical part of diligence (pulling statements, estimates, insider filings and institutional flow) into a conversation in Claude Desktop. The alternative is a terminal subscription that costs more than a junior analyst's salary and still needs someone to operate it.

Below I walk through an equity research pass on Axon Enterprise (AXON), the maker of Tasers and body cameras for law enforcement, question by question. Every answer shown is what the server returned on July 17, 2026; the Finance Toolkit dashboard at the end uses prices up to the same day.

**For more information on the FMP MCP server, see [FMP's documentation](https://site.financialmodelingprep.com/developer/docs/mcp-server){:target="_blank"}. To see what it adds on top of FMP, have a look at the [Finance Toolkit MCP server](/projects/financetoolkit/mcp).**

## Setting Things Up

The FMP MCP server connects to Claude Desktop as a remote connector, so there is nothing to install locally. Under Settings, then Connectors, then Add custom connector, the URL follows this pattern:

```
https://financialmodelingprep.com/mcp?apikey=FINANCIAL_MODELING_PREP_KEY
```

Paste that in with your key, give it a name, and Claude has direct access to FMP's statements, analyst data, insider filings and institutional ownership records for the rest of the session.

Get an API key at [jeroenbouma.com/fmp](/fmp){:target="_blank"}. The free tier covers 250 requests a day, which is plenty to run everything below.

## Financial Health: Returns Fell While the Multiple Doubled

Any investment story first needs the numbers to support it. FMP's key metrics bundle return on equity, return on invested capital and EV/EBITDA into a single answer, the kind of thing that normally means pulling three statements and building the ratios by hand.

<div class="mcp-show">
<div class="ca-q"><span class="ca-q__avatar"><i class="fas fa-user" aria-hidden="true"></i></span><p>Pull Axon Enterprise's (AXON) key financial metrics for the last five fiscal years and show me how ROE, ROIC, and EV/EBITDA have moved.<span class="ca-q__tool">FMP MCP · key metrics</span></p></div>
<div class="mcp-show__meta"><span><b>5</b> fiscal years</span><span><b>3</b> ratios and the statements behind them</span></div>
<div class="mcp-show__grid">
<div class="mcp-show__cell mcp-show__cell--wide">{% include ft-chart.html id="axon-fmp-metrics" src="/assets/data/article-charts.json" label="Axon's ROE, ROIC, EV/EBITDA, revenue and EBITDA, fiscal 2021 to 2025" %}</div>
</div>
<div class="ca-nums"><span><b>6.0% → −1.1%</b>ROIC, 2023 to 2025</span><span><b>105.1x → 236.1x</b>EV/EBITDA, 2023 to 2025</span><span><b>$2.78B</b>revenue 2025, from $0.86B in 2021</span></div>
</div>

This is uncomfortable on its own: ROIC peaked in 2023 at 6.0% and has since gone negative, while the EV/EBITDA multiple more than doubled over the same stretch, to 236.1 by 2025 (the 2021 multiple is negative because EBITDA was a loss that year). Revenue more than tripled in four years, but EBITDA fell from $437 million in 2024 to $196 million in 2025. **The multiple is expanding faster than the returns funding it**, and that tension is worth flagging before sizing a position.

## Analyst Estimates: Agreement on Revenue, Not on Margins

A small fund without in-house sell-side coverage can still use consensus, as long as it doesn't treat it as a target to chase. The spread between analysts is usually more useful than the average.

<div class="mcp-show">
<div class="ca-q"><span class="ca-q__avatar"><i class="fas fa-user" aria-hidden="true"></i></span><p>Show me the current analyst price target range and consensus for AXON, plus 2026 through 2028 revenue and EPS estimates.<span class="ca-q__tool">FMP MCP · price targets, analyst estimates</span></p></div>
<div class="mcp-show__meta"><span><b>21</b> ratings: 17 buy, 4 hold, 0 sell</span><span><b>3</b> years of estimates</span></div>
<div class="mcp-show__grid">
<div class="mcp-show__cell mcp-show__cell--wide">{% include ft-chart.html id="axon-fmp-targets" src="/assets/data/article-charts.json" label="Axon's analyst price targets against its share price on July 17, 2026" %}</div>
</div>
<div class="mcp-show__result" markdown="1">

| Fiscal year | Revenue | Growth | Adjusted EPS | Growth | Analysts |
|-------------|--------:|-------:|-------------:|-------:|---------:|
| 2026E | $3.66B | +32% | $7.69 | +22% | ~13 |
| 2027E | $4.73B | +29% | $10.64 | +38% | ~14 |
| 2028E | $6.08B | +29% | $13.89 | +31% | ~10 |

</div>
<div class="ca-nums"><span><b>$658.56</b>average target, +29%</span><span><b>$440 to $820</b>target range</span><span><b>$510.28</b>share price</span></div>
</div>

The price targets show a consensus of $658.56 against a share price of $510.28 that day: the shares traded about 22.5% below where analysts collectively see them heading, or roughly 29% upside. The estimates further out are more revealing. By 2028, the analysts covering AXON put net income anywhere from $573 million to $1.81 billion, a range wider than the company's entire 2025 net income of $124.9 million. **They agree on the revenue trajectory and disagree sharply on what margin structure survives three years out**, and that disagreement says more than the consensus price target does.

## A DCF That Can't Price the Growth

A DCF is a pressure test: does the current price only make sense under aggressive assumptions, or does it hold up under conservative ones? That matters more when a fund holds six positions than when it holds three hundred, because there's no portfolio-level averaging to absorb being wrong on one name.

<div class="mcp-show">
<div class="ca-q"><span class="ca-q__avatar"><i class="fas fa-user" aria-hidden="true"></i></span><p>Run a levered discounted cash flow valuation on AXON and compare it to the current share price.<span class="ca-q__tool">FMP MCP · levered DCF</span></p></div>
<div class="mcp-show__grid">
<div class="mcp-show__cell mcp-show__cell--wide">{% include ft-chart.html id="axon-fmp-dcf" src="/assets/data/article-charts.json" label="Axon's levered DCF value against its share price on July 17, 2026" %}</div>
</div>
<div class="ca-nums"><span><b>$94.30</b>levered DCF value</span><span><b>$510.28</b>share price</span><span><b>5.4x</b>price over model value</span></div>
</div>

The number that comes back looks alarming at first: a DCF value of $94.30 against a share price of $510.28, so the shares trade at 5.4 times the model's value. The model isn't really saying the market is wrong. A standard WACC-and-terminal-growth template can't capture a company compounding revenue in the 30%+ range, so the entire bull case for AXON has to be carried by assumptions the template doesn't make for you. Running it doesn't answer the valuation question, but it does show how much of the investment case rests on judgment rather than arithmetic, which is worth knowing before writing the position up.

## What Management Said: "We Passed the Inflection Point"

Ratios describe what already happened, while earnings calls are often the only source for what management believes is coming. Tracking how the language shifts from quarter to quarter is a real edge for a team that can't sit in on every call live.

<div class="mcp-show">
<div class="ca-q"><span class="ca-q__avatar"><i class="fas fa-user" aria-hidden="true"></i></span><p>Pull the transcript from AXON's most recent earnings call and tell me what the CEO said about growth.<span class="ca-q__tool">FMP MCP · earnings call transcript</span></p></div>
<div class="mcp-show__meta"><span><b>Q1 2026</b> earnings call</span><span><b>May 6</b> 2026</span></div>
<div class="mcp-show__verdict"><p class="mcp-show__label"><i class="fas fa-quote-left" aria-hidden="true"></i> CEO Patrick Smith</p><p>"I'm more convinced than ever that we're building something the world genuinely needs. [...] Today, I think we passed the inflection point."</p></div>
<div class="mcp-show__result" markdown="1">

| Q1 2026 | Result | Year on year |
|---------|-------:|-------------:|
| Revenue | $807M | +34%, the ninth quarter in a row above 30% |
| Full-year revenue guidance | raised | to 30% to 32% growth |
| AI bookings | | +140% |
| AI product revenue | | +700%, from a small base |
| Dedrone (counter-drone) revenue | | +300%, bookings +500% |
| International revenue | 20% of total | +100% |
| Annual recurring revenue | $1.5B | +35% |
| Net revenue retention | 125% | |
| Future contracted bookings | $14.3B | +44% |

</div>
</div>

Claude pulls the full transcript of the call on May 6, 2026, and picks out the key line along with the numbers management used to back it. "Passed the inflection point" is the kind of phrase worth tracking against what the same person said the quarter before and the quarter after. Done manually across a dozen transcripts, that is not a two-minute exercise, which is why most small teams don't do it and why it's worth automating.

## Insider Sales: Routine, Not a Signal

Insider selling is often read as a bad signal by reflex, but most of it is small, scheduled and meaningless. The actual job is telling routine activity apart from something that changes the picture.

<div class="mcp-show">
<div class="ca-q"><span class="ca-q__avatar"><i class="fas fa-user" aria-hidden="true"></i></span><p>Show me the most recent insider transactions for AXON, including who traded, how much, and at what price.<span class="ca-q__tool">FMP MCP · insider trading</span></p></div>
<div class="mcp-show__meta"><span><b>10</b> transactions, May 22 to July 8, 2026</span><span><b>8</b> sales, <b>2</b> grants</span></div>
<div class="mcp-show__result" markdown="1">

| Date | Insider | Role | Type | Shares | Price | Value |
|------|---------|------|------|-------:|------:|------:|
| Jul 8, 2026 | Leon Kant | Director (new) | Grant | 600 | $0 | |
| Jul 8, 2026 | Vivek Mohindra | Director (new) | Grant | 600 | $0 | |
| Jul 7, 2026 | Patrick W. Smith | CEO | Sale | ~20,000 | ~$640 ($627 to $663) | ~$12.8M |
| Jun 5, 2026 | Joshua Isner | President | Sale | 4,590 | ~$493 average | ~$2.3M |
| Jun 4, 2026 | Patrick W. Smith | CEO | Sale | 20,000 | $500 | $10.0M |
| Jun 4, 2026 | Cameron Brooks | Chief Revenue Officer | Sale | 1,242 | $500 | $0.6M |
| Jun 4, 2026 | Elizabeth Coughlin | Chief Human Officer | Sale | 1,554 | $485 | $0.8M |
| Jun 1, 2026 | Jeri Williams | Director | Sale | 629 | ~$470 average | ~$0.3M |
| Jun 1, 2026 | Caitlin Kalinowski | Director | Sale | 564 | ~$479 average | ~$0.3M |
| May 22, 2026 | Isaiah Fields | Chief Legal Officer | Sale | 2,000 | $400 | $0.8M |

</div>
</div>

The transactions that come back show Patrick Smith selling in two blocks of about 20,000 shares a month apart, other executives and directors selling smaller amounts between late May and early June, and two newly appointed directors receiving stock awards of 600 shares each. None of it looks conviction-driven; the pattern is consistent with scheduled 10b5-1 plans doing what they're built to do. Being able to rule something out with confidence is worth as much here as spotting a real signal.

## Institutional Flow: Fewer Holders, Same Ownership

Before taking a meaningful position, it helps to know whether a fund is early or late relative to institutional flow. A stock where ownership just climbed from 80% to 83% of the float in one quarter is a different setup than one where the same institutions are quietly leaving.

<div class="mcp-show">
<div class="ca-q"><span class="ca-q__avatar"><i class="fas fa-user" aria-hidden="true"></i></span><p>Show me institutional ownership trends for AXON from the latest 13F filings, including how many holders opened new positions versus closed them.<span class="ca-q__tool">FMP MCP · institutional ownership</span></p></div>
<div class="mcp-show__meta"><span><b>4</b> quarters of 13F filings</span><span>latest for the quarter ending <b>March 31</b> 2026</span></div>
<div class="mcp-show__grid">
<div class="mcp-show__cell mcp-show__cell--wide">{% include ft-chart.html id="axon-fmp-13f" src="/assets/data/article-charts.json" label="Axon's institutional holders, positions opened and closed, and share of the float held" %}</div>
</div>
<div class="ca-nums"><span><b>1,250 → 1,101</b>institutional holders</span><span><b>+142 → −95</b>positions opened minus closed</span><span><b>82.7% → 83.3%</b>share of the float held</span></div>
</div>

The result is more mixed than a single snapshot would suggest. Total institutional holders slipped from 1,250 in Q2 2025 to 1,101 by Q1 2026, and the balance between new positions opened and positions closed has flipped, from a net of +142 in Q2 2025 to -95 in the latest filing. Ownership of the float has held up, at 83.3% against 82.7% in Q2 2025, which means existing holders are largely staying put even as fewer new funds step in and more trim out. That points to interest cooling off rather than a rush for the exit. Keep in mind that 13F counts for the latest quarter still move as late filings come in.

## Where FMP Stops and the Finance Toolkit MCP Picks Up

Everything above comes straight out of FMP's raw endpoints, and for pulling a specific number, filing or quarter, that's the right tool. What it does only to a more limited extent is combine those raw numbers into the computed research output an analyst would also like to see, such as a Piotroski score, a Sharpe ratio against a benchmark, a five-factor Fama-French regression or a DuPont breakdown of what's actually driving ROE.

The [Finance Toolkit MCP](/projects/financetoolkit/mcp) extends FMP's endpoints in that direction. It's built directly on top of FMP's data, using the same API key, so there's no second account or separate integration to manage. Asked for a health check across seven areas, it works through each of them in turn:

<div class="mcp-show">
<div class="ca-q"><span class="ca-q__avatar"><i class="fas fa-user" aria-hidden="true"></i></span><p>Explore the areas of efficiency, liquidity, profitability, solvency, valuation, performance and risk for AXON. How healthy is the company?</p></div>
<div class="mcp-show__meta"><span><b>8</b> tools</span><span><b>5</b> fiscal years</span><span>prices up to <b>July 17</b> 2026</span></div>
<details class="mcp-show__trace"><summary><i class="fas fa-list-check" aria-hidden="true"></i> The steps behind the answer</summary><ol><li><code>liquidity</code><span>Current ratio and quick ratio, fiscal 2021 to 2025</span></li><li><code>solvency</code><span>Debt to equity</span></li><li><code>efficiency</code><span>Asset turnover and cash conversion cycle</span></li><li><code>profitability</code><span>Gross margin, operating margin, return on equity and return on invested capital</span></li><li><code>valuation</code><span>EV/sales, price-to-book and free cash flow yield</span></li><li><code>performance</code><span>Total return and beta per year against the S&amp;P 500 (SPY)</span></li><li><code>risk</code><span>Volatility per year and maximum drawdown since January 2021</span></li><li><code>market_data</code><span>Cash flow statement: stock-based compensation</span></li></ol></details>
<div class="mcp-show__grid">
<div class="mcp-show__cell">{% include ft-chart.html id="axon-ft-profit" src="/assets/data/article-charts.json" label="Axon's margins, return on equity and ROIC, fiscal 2021 to 2025" %}</div>
<div class="mcp-show__cell">{% include ft-chart.html id="axon-ft-balance" src="/assets/data/article-charts.json" label="Axon's current ratio, quick ratio and debt to equity, fiscal 2021 to 2025" %}</div>
<div class="mcp-show__cell">{% include ft-chart.html id="axon-ft-valuation" src="/assets/data/article-charts.json" label="Axon's EV/sales and price-to-book, fiscal 2021 to 2025" %}</div>
<div class="mcp-show__cell">{% include ft-chart.html id="axon-ft-returns" src="/assets/data/article-charts.json" label="Axon's total return per year against the S&P 500" %}</div>
</div>
<div class="mcp-show__verdict"><p class="mcp-show__label"><i class="fas fa-lightbulb" aria-hidden="true"></i> What the data shows</p><p>Axon is a healthy business and a risky stock. The balance sheet is strong: a current ratio of 2.53, a quick ratio of 1.81 and debt to equity of 0.59 leave no sign of distress, and the cash conversion cycle shortened from 194 days in 2021 to 163 in 2025. The income statement is thin: a gross margin near 60% but an operating margin of −2.2%, a return on equity of 4.5% and an ROIC of 2.8% in 2025, weighed down by $634 million of stock-based compensation, 23% of revenue. The shares are priced for growth, at 20.7 times sales and 17.5 times book with a free cash flow yield of 0.13%, and they move like it: a 130.1% gain in 2024, then −4.5% in 2025 and −10.2% in 2026 up to July 17, while the S&amp;P 500 rose 17.8% and 9.6%.</p></div>
<div class="ca-nums"><span><b>52.9%</b>volatility 2025, S&amp;P 500 19.5%</span><span><b>−60.3%</b>maximum drawdown since 2021</span><span><b>1.08</b>beta 2025</span></div>
</div>

There is little friction between the two: ask for a ratio the Finance Toolkit computes, and it pulls the underlying statements from FMP, runs the calculation and returns the answer in the same conversation, with the same connector setup. Each number maps to a documented method in the [Finance Toolkit documentation](/projects/financetoolkit/docs), so an analyst can check how it was calculated.

## What This Means for a Small Team

For Axon, the file now holds a coherent picture: a company growing revenue above 30% a year with a strong balance sheet, a GAAP income statement that doesn't yet show it, a valuation that needs that growth to continue for years, insiders selling on schedule and institutions holding rather than adding. None of that is a decision, and none of it is investment advice. It is the groundwork a decision needs, assembled in an afternoon rather than a week.

The limits are worth stating. The FMP answers are snapshots: estimates, price targets and 13F counts change from week to week, and what's shown here is what the server returned on July 17, 2026. A template DCF can't value a company like this, and consensus can't tell you which analyst is right about margins. For a family office or small fund already running the prompts above, adding the Finance Toolkit MCP as a second connector puts computed analysis on top of the raw data pulls, without turning a two-person team into a data engineering project.

> **Try this with the Finance Toolkit MCP:** *"For AXON, compare the gross margin, operating margin and ROIC since 2021 with its EV/sales, and show its yearly return and maximum drawdown against the S&P 500. Is the valuation supported by the profitability?"*

{% include ft-charts-script.html %}
