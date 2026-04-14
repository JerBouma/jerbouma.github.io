---
title: Literature
description: Financial literature, articles, and papers that inform my work in quantitative finance.
permalink: /literature
layout: single
classes: custom-document
author_profile: false
---

Most of the modelling I undertake is grounded in established financial literature. This is my repository of articles, books, and papers that capture my interest, primarily focusing on investing, economics, and behavioural finance. Click any title to access the source.

<div class="lit-filters" id="lit-filters">
  <button class="lit-filter active" data-filter="all">All <span class="lit-count" data-count="all"></span></button>
  <button class="lit-filter" data-filter="finance">Finance <span class="lit-count" data-count="finance"></span></button>
  <button class="lit-filter" data-filter="portfolio-optimisation">Portfolio Optimisation <span class="lit-count" data-count="portfolio-optimisation"></span></button>
  <button class="lit-filter" data-filter="factor-investing">Factor Investing <span class="lit-count" data-count="factor-investing"></span></button>
  <button class="lit-filter" data-filter="behavioral-finance">Behavioral Finance <span class="lit-count" data-count="behavioral-finance"></span></button>
  <button class="lit-filter" data-filter="private-equity">Private Equity <span class="lit-count" data-count="private-equity"></span></button>
  <button class="lit-filter" data-filter="esg">ESG <span class="lit-count" data-count="esg"></span></button>
  <button class="lit-filter" data-filter="quant-finance">Quant Finance <span class="lit-count" data-count="quant-finance"></span></button>
  <button class="lit-filter" data-filter="econometrics">Econometrics <span class="lit-count" data-count="econometrics"></span></button>
  <button class="lit-filter" data-filter="artificial-intelligence">Artificial Intelligence <span class="lit-count" data-count="artificial-intelligence"></span></button>
</div>

<div class="lit-grid" id="lit-grid">

<div class="lit-card" data-tags="portfolio-optimisation">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3469961" class="lit-card__title" target="_blank" rel="noopener">A Robust Estimator of the Efficient Frontier</a>
  <p class="lit-card__authors">Marcos M. Lopez de Prado</p>
  <p class="lit-card__summary">Convex optimization solutions tend to be unstable, to the point of entirely offsetting the benefits of optimization. For example, in the context of financial applications, it is known that portfolios optimized in-sample often underperform the naïve (equal weights) allocation out-of-sample. This instability can be traced back to two sources: (i) noise in the input variables; and (ii) signal structure that magnifies the estimation errors in the input variables. A first innovation of this paper is to introduce the nested clustered optimization algorithm (NCO), a method that tackles both sources of instability. Over the past 60 years, various approaches have been developed to address these two sources of instability. These approaches are flawed in the sense that different methods may be appropriate for different input variables, and it is unrealistic to expect that one method will dominate all the rest under all circumstances. Accordingly, a second innovation of this paper is to introduce MCOS, a Monte Carlo approach that estimates the allocation error produced by various optimization methods on a particular set of input variables. The result is a precise determination of what method is most robust to a particular case. Thus, rather than relying always on one particular approach, MCOS allows users to apply opportunistically whatever optimization method is best suited in a particular setting.</p>
  <div class="lit-card__tags"><span class="lit-tag">Portfolio Optimisation</span></div>
</div>

<div class="lit-card" data-tags="portfolio-optimisation">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://ideas.repec.org/p/sza/wpaper/wpapers328.html" class="lit-card__title" target="_blank" rel="noopener">A constrained hierarchical risk parity algorithm with cluster-based capital allocation</a>
  <p class="lit-card__authors">Johann Pfitzinger, Nico Katzke</p>
  <p class="lit-card__summary">Hierarchical Risk Parity (HRP) is a risk-based portfolio optimisation algorithm, which has been shown to generate diversified portfolios with robust out-of-sample properties without the need for a positive-definite return covariance matrix (Lopez de Prado 2016). The algorithm applies machine learning techniques to identify the underlying hierarchical correlation structure of the portfolio, allowing clusters of similar assets to compete for capital. The resulting allocation is both well-diversified over risk sources and intuitively appealing. This paper proposes a method of fully exploiting the information created by the clustering process, achieving enhanced out-of-sample risk and return characteristics. In addition, a practical approach to calculating HRP weights under box and group constraints is introduced. A comprehensive set of portfolio simulations over 6 equity universes demonstrates the appeal of the algorithm for portfolios consisting of 20 - 200 assets. HRP delivers highly diversified allocations with low volatility, low portfolio turnover and competitive performance metrics.</p>
  <div class="lit-card__tags"><span class="lit-tag">Portfolio Optimisation</span></div>
</div>

<div class="lit-card" data-tags="finance">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://img-cdn.tinkoffjournal.ru/-/taa-strat-vanguard.pdf" class="lit-card__title" target="_blank" rel="noopener">A primer on tactical asset allocation strategy evaluation</a>
  <p class="lit-card__authors">Vanguard</p>
  <p class="lit-card__summary">Tactical asset allocation (TAA) is a dynamic strategy that actively adjusts a portfolio’s strategic asset allocation (SAA) based on short-term market forecasts.</p>
  <div class="lit-card__tags"><span class="lit-tag">Finance</span></div>
</div>

<div class="lit-card" data-tags="finance">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1337708" class="lit-card__title" target="_blank" rel="noopener">Active vs. Passive Management: New Evidence from Exchange Traded Funds</a>
  <p class="lit-card__authors">Gerasimos G. Rompotis</p>
  <p class="lit-card__summary">This paper expands the debate about “active vs. passive” management using data from active and passive ETFs listed in the U.S. market. The results reveal that the active ETFs underperform both the corresponding passive ETFs and the market indexes.</p>
  <div class="lit-card__tags"><span class="lit-tag">Finance</span></div>
</div>

<div class="lit-card" data-tags="finance private-equity">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3623820" class="lit-card__title" target="_blank" rel="noopener">An Inconvenient Fact: Private Equity Returns &amp; The Billionaire Factory</a>
  <p class="lit-card__authors">Ludovic Phalippou</p>
  <p class="lit-card__summary">Only facing facts, disclosing all relevant information, having level playing rules, better education, and simplified structures can bring a superior overall equilibrium. This superior equilibrium, however, will probably generate fewer billionaires.</p>
  <div class="lit-card__tags"><span class="lit-tag">Finance</span><span class="lit-tag">Private Equity</span></div>
</div>

<div class="lit-card" data-tags="artificial-intelligence finance">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://caia.org/sites/default/files/artificial_intelligence_0.pdf" class="lit-card__title" target="_blank" rel="noopener">Artificial Intelligence</a>
  <p class="lit-card__authors">Frank Benham, Roberto Obregon, Timur Kaya Yontar</p>
  <p class="lit-card__summary">As a result, a successful implementation of A.I. leads to more informed decision making. Any investor should only invest in areas or use tools in their process that they understand and feel comfortable with, and this remains true with artificial intelligence.</p>
  <div class="lit-card__tags"><span class="lit-tag">Artificial Intelligence</span><span class="lit-tag">Finance</span></div>
</div>

<div class="lit-card" data-tags="finance">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://www.jstor.org/stable/2353018" class="lit-card__title" target="_blank" rel="noopener">Assessing the Market Timing Performance of Managed Portfolios</a>
  <p class="lit-card__authors">Ravi Jagannathan, Robert A. Korajczyk</p>
  <p class="lit-card__summary">We show theoretically and empirically that it is possible to construct portfolios that show artificial timing ability when no true timing ability exists.</p>
  <div class="lit-card__tags"><span class="lit-tag">Finance</span></div>
</div>

<div class="lit-card" data-tags="finance">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-book"></i> Book</span>
  </div>
  <a href="https://www.amazon.com/Asset-Management-Systematic-Investing-Association/dp/0199959323" class="lit-card__title" target="_blank" rel="noopener">Asset Management: A Systematic Approach to Factor Investing (Chapter 5)</a>
  <p class="lit-card__authors">Andrew Ang</p>
  <p class="lit-card__summary">Labor income is an asset, and for young investors the value of labor income usually dominates the rest of their financial holdings. An investor’s mix of assets changes as her labor income evolves over her life cycle, and an investor whose labor income is bond-like should reduce his holdings of equities as retirement approaches. While economic theory suggests annuities are ideal for retirees, few hold them.</p>
  <div class="lit-card__tags"><span class="lit-tag">Finance</span></div>
</div>

<div class="lit-card" data-tags="factor-investing finance">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-book"></i> Book</span>
  </div>
  <a href="https://www.amazon.com/Asset-Management-Systematic-Investing-Association/dp/0199959323" class="lit-card__title" target="_blank" rel="noopener">Asset Management: A Systematic Approach to Factor Investing (Chapter 2 &amp; 3)</a>
  <p class="lit-card__authors">Andrew Ang</p>
  <p class="lit-card__summary">This features Chapter 2 &amp; 3 of the book and discusses Preferences and Mean-Variance investing (Utility functions).</p>
  <div class="lit-card__tags"><span class="lit-tag">Factor Investing</span><span class="lit-tag">Finance</span></div>
</div>

<div class="lit-card" data-tags="factor-investing finance">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-book"></i> Book</span>
  </div>
  <a href="https://www.amazon.com/Asset-Management-Systematic-Investing-Association/dp/0199959323" class="lit-card__title" target="_blank" rel="noopener">Asset Management: A Systematic Approach to Factor Investing (Chapter 4)</a>
  <p class="lit-card__authors">Andrew Ang</p>
  <p class="lit-card__summary">In this chapter we discuss portfolio choice over long horizons and how an investor can dynamically change her portfolio in response to changing returns and investment opportunities.</p>
  <div class="lit-card__tags"><span class="lit-tag">Factor Investing</span><span class="lit-tag">Finance</span></div>
</div>

<div class="lit-card" data-tags="quant-finance">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-book"></i> Book</span>
  </div>
  <a href="https://www.amazon.com/Asset-Pricing-John-H-Cochrane/dp/0691121370" class="lit-card__title" target="_blank" rel="noopener">Asset Pricing</a>
  <p class="lit-card__authors">John Cochrane</p>
  <p class="lit-card__summary">Asset pricing theory tries to understand the prices or values of claims to uncertain payments. A low price implies a high rate of return, so one can also think of the theory as explaining why some assets pay higher average returns than others.</p>
  <div class="lit-card__tags"><span class="lit-tag">Quant Finance</span></div>
</div>

<div class="lit-card" data-tags="finance">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3197185" class="lit-card__title" target="_blank" rel="noopener">Buffet's Alpha</a>
  <p class="lit-card__authors">Andrea Frazzini, David Kabiller, Lasse Heje Pedersen</p>
  <p class="lit-card__summary">In summary, we found that Buffett has developed a unique access to leverage; that he has invested in safe, high-quality, cheap stocks; and that these key characteristics can largely explain his impressive performance.</p>
  <div class="lit-card__tags"><span class="lit-tag">Finance</span></div>
</div>

<div class="lit-card" data-tags="portfolio-optimisation">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://jpm.pm-research.com/content/42/4/59" class="lit-card__title" target="_blank" rel="noopener">Building Diversified Portfolios that Outperform Out of Sample</a>
  <p class="lit-card__authors">Marcos M. Lopez de Prado</p>
  <p class="lit-card__summary">In this article, the author introduces the Hierarchical Risk Parity (HRP) approach to address three major concerns of quadratic optimizers, in general, and Markowitz’s critical line algorithm (CLA), in particular: instability, concentration, and underperformance. HRP applies modern mathematics (graph theory and machine-learning techniques) to build a diversified portfolio based on the information contained in the covariance matrix. However, unlike quadratic optimizers, HRP does not require the invertibility of the covariance matrix. In fact, HRP can compute a portfolio on an ill-degenerated or even a singular covariance matrix—an impossible feat for quadratic optimizers. Monte Carlo experiments show that HRP delivers lower out-ofsample variance than CLA, even though minimum variance is CLA’s optimization objective. HRP also produces less risky portfolios out of sample compared to traditional risk parity methods.</p>
  <div class="lit-card__tags"><span class="lit-tag">Portfolio Optimisation</span></div>
</div>

<div class="lit-card" data-tags="finance">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3247356" class="lit-card__title" target="_blank" rel="noopener">Challenging the Conventional Wisdom on Active Management</a>
  <p class="lit-card__authors">K.J. Martijn Cremers</p>
  <p class="lit-card__summary">Its conclusion—that the data did “not support the existence of skilled or informed mutual fund portfolio managers”—was the capstone of an academic literature beginning with Jensen (1968) that formed the ‘conventional wisdom’ that active management does not create value for investors. Our review of the most recent literature suggests that the conventional wisdom is too negative on the value of active management.</p>
  <div class="lit-card__tags"><span class="lit-tag">Finance</span></div>
</div>

<div class="lit-card" data-tags="behavioral-finance finance">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://psycnet.apa.org/record/1985-05780-001" class="lit-card__title" target="_blank" rel="noopener">Choices, Values and Frames</a>
  <p class="lit-card__authors">Amos Tversky, Daniel Kahneman</p>
  <p class="lit-card__summary">The concepts of utility and value are commonly used in two distinct senses: (a) experience value, the degree of pleasure or pain, satisfaction or anguish in the actual experience of an outcome; and (b) decision value, the contribution of an anticipated outcome to the overall attractiveness or aversiveness of an option in a choice</p>
  <div class="lit-card__tags"><span class="lit-tag">Behavioral Finance</span><span class="lit-tag">Finance</span></div>
</div>

<div class="lit-card" data-tags="factor-investing finance">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://rady.ucsd.edu/faculty/directory/valkanov/pub/classes/mfe/docs/fama_french_jfe_1993.pdf" class="lit-card__title" target="_blank" rel="noopener">Common risk factors in the returns on stocks and bonds</a>
  <p class="lit-card__authors">Eugene F. Fama, Kenneth R. French</p>
  <p class="lit-card__summary">This paper identities five common risk factors in the returns on stocks and bonds. Most important, the five factors seem to explain average returns on stocks and bonds.</p>
  <div class="lit-card__tags"><span class="lit-tag">Factor Investing</span><span class="lit-tag">Finance</span></div>
</div>

<div class="lit-card" data-tags="portfolio-optimisation">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://ideas.repec.org/p/arx/papers/1902.05710.html" class="lit-card__title" target="_blank" rel="noopener">Constrained Risk Budgeting Portfolios: Theory, Algorithms, Applications &amp; Puzzles</a>
  <p class="lit-card__authors">Thierry Roncalli</p>
  <p class="lit-card__summary">This article develops the theory of risk budgeting portfolios, when we would like to impose weight constraints. It appears that the mathematical problem is more complex than the traditional risk budgeting problem. The formulation of the optimization program is particularly critical in order to determine the right risk budgeting portfolio. We also show that numerical solutions can be found using methods that are used in large-scale machine learning problems. Indeed, we develop an algorithm that mixes the method of cyclical coordinate descent (CCD), alternating direction method of multipliers (ADMM), proximal operators and Dykstra's algorithm. This theoretical body is then applied to some investment problems. In particular, we show how to dynamically control the turnover of a risk parity portfolio and how to build smart beta portfolios based on the ERC approach by improving the liquidity of the portfolio or reducing the small cap bias. Finally, we highlight the importance of the homogeneity property of risk measures and discuss the related scaling puzzle.</p>
  <div class="lit-card__tags"><span class="lit-tag">Portfolio Optimisation</span></div>
</div>

<div class="lit-card" data-tags="esg finance">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2939853" class="lit-card__title" target="_blank" rel="noopener">Corporate social responsibility, credit rating, and private debt contracting: new evidence from syndicated loan market.</a>
  <p class="lit-card__authors">Ha-Chin Yi, Kiyoung Chang, Suing C. Bae</p>
  <p class="lit-card__summary">We examine the impact of corporate social responsibility (CSR) activities on loan spreads of syndicated bank loans, with a particular interest in how CSR and credit ratings are interrelated as a joint determinant of loan spreads. Overall, our results provide strong evidence that CSR matters to the pricing of loan contracts beyond credit rating information and the results remain robust to the possible firm size effect and the endogeneity issues.</p>
  <div class="lit-card__tags"><span class="lit-tag">ESG</span><span class="lit-tag">Finance</span></div>
</div>

<div class="lit-card" data-tags="finance">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://www.ivey.uwo.ca/media/3775518/the_cross-section_of_expected_stock_returns.pdf" class="lit-card__title" target="_blank" rel="noopener">Cross Section of Expected Returns</a>
  <p class="lit-card__authors">Campbell R. Harvey</p>
  <p class="lit-card__summary">Our paper introduces a new multiple testing framework and provides historical cutoffs from the first empirical tests in 1967 to today. A new factor needs to clear a much higher hurdle, with a t-statistic greater than 3.0. We argue that most claimed research findings in financial economics are likely false.</p>
  <div class="lit-card__tags"><span class="lit-tag">Finance</span></div>
</div>

<div class="lit-card" data-tags="esg finance">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2708589" class="lit-card__title" target="_blank" rel="noopener">Do institutional investors drive corporate social responsibility?</a>
  <p class="lit-card__authors">Alexander Dyck, Hannes F. Wagner, Karl V. Lins, Lukas Roth</p>
  <p class="lit-card__summary">This paper assesses whether shareholders drive the environmental and social (E&amp;S) performance of firms worldwide. In cross section, investors increase firms’ E&amp;S performance when they come from countries with a strong community belief in the importance of E&amp;S issues, but not otherwise. As such, these institutional investors transplant their social norms regarding E&amp;S issues around the world.</p>
  <div class="lit-card__tags"><span class="lit-tag">ESG</span><span class="lit-tag">Finance</span></div>
</div>

<div class="lit-card" data-tags="finance">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2156623" class="lit-card__title" target="_blank" rel="noopener">Does Academic Research Destroy Stock Return Predictability</a>
  <p class="lit-card__authors">Jeffrey Pontiff, R. David Mclean</p>
  <p class="lit-card__summary">We study the out-of-sample and post-publication return predictability of 97 variables shown to predict cross-sectional stock returns. Our findings suggest that investors learn about mispricing from academic publications.</p>
  <div class="lit-card__tags"><span class="lit-tag">Finance</span></div>
</div>

<div class="lit-card" data-tags="finance private-equity">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://eprints.whiterose.ac.uk/147571/1/Does risk explain persistence in private equity performance.pdf" class="lit-card__title" target="_blank" rel="noopener">Does Risk Explain Persistence in PE Performance</a>
  <p class="lit-card__authors">Abdulkadir Mohamed, Armin Schwienbacher, Axel Buchner</p>
  <p class="lit-card__summary">This study examines the impact of fund-level risk on performance persistence as well as risk persistence in private equity. Consistent with Kaplan and Schoar (2005), we find that returns are persistent for VC and buyout funds for US funds.</p>
  <div class="lit-card__tags"><span class="lit-tag">Finance</span><span class="lit-tag">Private Equity</span></div>
</div>

<div class="lit-card" data-tags="portfolio-optimisation">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://onlinelibrary.wiley.com/doi/10.1111/1475-3995.00380" class="lit-card__title" target="_blank" rel="noopener">Dual stochastic dominance and quantile risk measures</a>
  <p class="lit-card__authors">Wlodzimierz Ogryczak</p>
  <p class="lit-card__summary">Following the seminal work by Markowitz, the portfolio selection problem is usually modeled as a bicriteria optimization problem where a reasonable trade–off between expected rate of return and risk is sought. In the classical Markowitz model, the risk is measured with variance. Several other risk measures have been later considered thus creating the entire family of mean–risk (Markowitz type) models. In this paper, we analyze mean–risk models using quantiles and tail characteristics of the distribution. Value at risk (VAR), defined as the maximum loss at a specified confidence level, is a widely used quantile risk measure. The corresponding second order quantile measure, called the worst conditional expectation or Tail VAR, represents the mean shortfall at a specified confidence level. It has more attractive theoretical properties and it leads to LP solvable portfolio optimization models in the case of discrete random variables, i.e., in the case of returns defined by their realizations under the specified scenarios. We show that the mean–risk models using the worst conditional expectation or some of its extensions are in harmony with the stochastic dominance order. For this purpose, we exploit duality relations of convex analysis to develop the quantile model of stochastic dominance for general distributions.</p>
  <div class="lit-card__tags"><span class="lit-tag">Portfolio Optimisation</span></div>
</div>

<div class="lit-card" data-tags="finance">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://caia.org/sites/default/files/dynamic_strategies_for_asset_allocation.pdf" class="lit-card__title" target="_blank" rel="noopener">Dynamic Strategies for Asset Allocation</a>
  <p class="lit-card__authors">André F. Perold, William F. Sharpe</p>
  <p class="lit-card__summary">The article compares multiple investment strategies. However, the key message is that none of the strategies dominate the others and are completely based on the behavior of the market.</p>
  <div class="lit-card__tags"><span class="lit-tag">Finance</span></div>
</div>

<div class="lit-card" data-tags="finance">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://www.jstor.org/stable/2325486" class="lit-card__title" target="_blank" rel="noopener">Efficient Capital Markets: A Review of Theory and Empirical Work</a>
  <p class="lit-card__authors">Eugene F. Fama</p>
  <p class="lit-card__summary">In short, the evidence in support of the efficient markets model is extensive, and (somewhat uniquely in economics) contradictory evidence is sparse. Nevertheless, we certainly do not want to leave the impression that all issues are closed. The old saw, &quot;much remains to be done,&quot; is relevant here as else- where</p>
  <div class="lit-card__tags"><span class="lit-tag">Finance</span></div>
</div>

<div class="lit-card" data-tags="finance">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://www.cfainstitute.org/-/media/documents/article/position-paper/investment-policy-statement-individual-investors.pdf" class="lit-card__title" target="_blank" rel="noopener">Elements of an Investment Policy Statement for Individual Investors</a>
  <p class="lit-card__authors">CFA Institute</p>
  <p class="lit-card__summary">The investment policy statement (IPS) serves as a strategic guide to the planning and implementation of an investment program. When implemented successfully, the IPS anticipates issues related to governance of the investment program, planning for appropriate asset allocation, implementing an investment program with internal and/or external managers, monitoring the results, risk management, and appropriate reporting.</p>
  <div class="lit-card__tags"><span class="lit-tag">Finance</span></div>
</div>

<div class="lit-card" data-tags="portfolio-optimisation">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://link.springer.com/article/10.1007/s10957-011-9968-2" class="lit-card__title" target="_blank" rel="noopener">Entropic value-at-risk: a new coherent risk measure</a>
  <p class="lit-card__authors">A. Ahmadi-Javid</p>
  <p class="lit-card__summary">This paper introduces the concept of entropic value-at-risk (EVaR), a new coherent risk measure that corresponds to the tightest possible upper bound obtained from the Chernoff inequality for the value-at-risk (VaR) as well as the conditional value-at-risk (CVaR). We show that a broad class of stochastic optimization problems that are computationally intractable with the CVaR is efficiently solvable when the EVaR is incorporated. We also prove that if two distributions have the same EVaR at all confidence levels, then they are identical at all points. The dual representation of the EVaR is closely related to the Kullback-Leibler divergence, also known as the relative entropy. Inspired by this dual representation, we define a large class of coherent risk measures, called g-entropic risk measures. The new class includes both the CVaR and the EVaR.</p>
  <div class="lit-card__tags"><span class="lit-tag">Portfolio Optimisation</span></div>
</div>

<div class="lit-card" data-tags="finance">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://www.jstor.org/stable/44095449" class="lit-card__title" target="_blank" rel="noopener">Estimating Market Values from Appraised Values without Assuming an Efficient Market</a>
  <p class="lit-card__authors">David Geltner</p>
  <p class="lit-card__summary">The purpose of the present study is to describe an approach to correcting the smoothing and lagging in the publicly reported appraisal-based indices without assuming a priori that the true market returns are uncorrelated or unpredictable.</p>
  <div class="lit-card__tags"><span class="lit-tag">Finance</span></div>
</div>

<div class="lit-card" data-tags="finance">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://www.tandfonline.com/doi/abs/10.2469/faj.v74.n2.6?journalCode=ufaj20" class="lit-card__title" target="_blank" rel="noopener">Everybody's doing it short volatility strategies and show financial insurers</a>
  <p class="lit-card__authors">Larry Harris, Vineer Bhansali</p>
  <p class="lit-card__summary">A low-yield, low-volatility environment has drawn market participants with different horizons into essentially similar volatility-contingent strategies based on a common nonlinear volatility risk factor. The growth of these correlated short volatility strategies creates risks that may trigger the next serious market crash</p>
  <div class="lit-card__tags"><span class="lit-tag">Finance</span></div>
</div>

<div class="lit-card" data-tags="factor-investing finance">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://research.vu.nl/en/publications/fundamental-factors-that-improve-your-investments-a-practical-gui" class="lit-card__title" target="_blank" rel="noopener">Fundamental Factors That Improve Your Investments: A Practical Guide</a>
  <p class="lit-card__authors">Alfred Slager, Philip Stork, Pim Lausberg</p>
  <p class="lit-card__summary">The development of a bespoke factor-based investing method will add to a thorough under standing of portfolio risks. This approach could increase the robustness of investment portfolios and improves diversification across the various asset categories.</p>
  <div class="lit-card__tags"><span class="lit-tag">Factor Investing</span><span class="lit-tag">Finance</span></div>
</div>

<div class="lit-card" data-tags="portfolio-optimisation">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://www.jstor.org/stable/4479577" class="lit-card__title" target="_blank" rel="noopener">Global Portfolio Optimization (Black-Litterman)</a>
  <p class="lit-card__authors">Fischer Black, Robert Litterman</p>
  <p class="lit-card__summary">Quantitative asset allocation models have not played the important role they should in global portfolio management. A good part of the problem is that such models are difficult to use and tend to result in portfolios that are badly behaved. Consideration of the global CAPM equilibrium can significantly improve the usefulness of these models. In particular, equilibrium returns for equities, bonds and currencies provide neutral starting points for estimating the set of expected excess returns needed to drive the portfolio optimization process. This set of neutral weights can then be tilted in accordance with the investor's views. If the investor has no particular views about asset returns, he can use the neutral values given by the equilibrium model. If the investor does have one or more views about the relative performances of assets, or their absolute performances, he can adjust equilibrium values in accordance with those views. Furthermore, the investor can control how strongly a particular view influences portfolio weights, in accordance with the degree of confidence with which he holds the view. This results in the Black Litterman model.</p>
  <div class="lit-card__tags"><span class="lit-tag">Portfolio Optimisation</span></div>
</div>

<div class="lit-card" data-tags="finance">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-book"></i> Book</span>
  </div>
  <a href="https://www.amazon.com/High-Growth-Handbook-Elad-Gil/dp/1732265100" class="lit-card__title" target="_blank" rel="noopener">High Growth Handbook</a>
  <p class="lit-card__authors">Elad Gil</p>
  <p class="lit-card__summary">This books gives a lot of insights on how to scale a start-up by sketching the neccesary roles and the common mistakes start-ups make during the scaling process.</p>
  <div class="lit-card__tags"><span class="lit-tag">Finance</span></div>
</div>

<div class="lit-card" data-tags="finance private-equity">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2597259" class="lit-card__title" target="_blank" rel="noopener">How Do Private Equity Investments Perform Compared to Public Equity?</a>
  <p class="lit-card__authors">Robert S. Harris, Steven N. Kaplan, Tim Jenkinson</p>
  <p class="lit-card__summary">We find marked differences between venture and buyout leading to a much more pronounced impact of accessing high performing funds in venture investing.</p>
  <div class="lit-card__tags"><span class="lit-tag">Finance</span><span class="lit-tag">Private Equity</span></div>
</div>

<div class="lit-card" data-tags="finance">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://papers.ssrn.com/sol3/papers.cfm?abstract_id=891719" class="lit-card__title" target="_blank" rel="noopener">How active is your fundmanager?</a>
  <p class="lit-card__authors">Antti Petajisto, K.J. Martijn Cremers</p>
  <p class="lit-card__summary">Funds with the highest Active Share, which represents the share of portfolio holdings that differ from the benchmark index holdings, significantly outperform their benchmarks, both before and after expenses, and they exhibit strong performance persistence. Non-index funds with the lowest Active Share underperform their benchmarks.</p>
  <div class="lit-card__tags"><span class="lit-tag">Finance</span></div>
</div>

<div class="lit-card" data-tags="econometrics">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-book"></i> Book</span>
  </div>
  <a href="https://www.amazon.com/Introductory-Econometrics-Modern-Approach-Economics/dp/1111531048" class="lit-card__title" target="_blank" rel="noopener">Introductory Econometrics</a>
  <p class="lit-card__authors">Jeffrey M. Woolridge</p>
  <p class="lit-card__summary">This book was used for the Empirical Economics lecture during my Masters. Helps to understand the very basics of Econometrics.</p>
  <div class="lit-card__tags"><span class="lit-tag">Econometrics</span></div>
</div>

<div class="lit-card" data-tags="behavioral-finance finance">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://www.tias.edu/docs/default-source/Kennisartikelen/investment-beliefs.pdf" class="lit-card__title" target="_blank" rel="noopener">Investment Beliefs</a>
  <p class="lit-card__authors">Alfred Slager, Kees Koedijk</p>
  <p class="lit-card__summary">Investment beliefs improve stakeholder governance by reducing possible conflicts of interest, and charge the innovative adaptability of an organization by setting guide lines for best practice.</p>
  <div class="lit-card__tags"><span class="lit-tag">Behavioral Finance</span><span class="lit-tag">Finance</span></div>
</div>

<div class="lit-card" data-tags="factor-investing finance">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://jpm.pm-research.com/content/40/5/127.short" class="lit-card__title" target="_blank" rel="noopener">Is Smart Beta really smart?</a>
  <p class="lit-card__authors">Burton G. Malkiel</p>
  <p class="lit-card__summary">The trick is to tilt (or flavor) the portfolio in some direction such as value versus growth, smaller versus larger companies, relatively strong stocks versus weak, and low-volatility stocks versus high volatility ones. This is referred to as Smart Beta.</p>
  <div class="lit-card__tags"><span class="lit-tag">Factor Investing</span><span class="lit-tag">Finance</span></div>
</div>

<div class="lit-card" data-tags="behavioral-finance finance">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://www.science.org/doi/10.1126/science.185.4157.1124" class="lit-card__title" target="_blank" rel="noopener">Judgment under Uncertainty: Heuristics and Biases</a>
  <p class="lit-card__authors">Amos Tversky, Daniel Kahneman</p>
  <p class="lit-card__summary">This article described three heuristics that are employed in making judgments under uncertainty: (i) representativeness, which is usually employed when people are asked to judge the probability that an object or event A belongs to class or process B; (ii) availability of instances or scenarios, which is often employed when people are asked to assess the frequency of a class or the plausibility of a particular development; and (iii) adjustment from an anchor, which is usually employed in numerical prediction when a relevant value is available. These heuristics are highly economical and usually effective, but they lead to systematic and predictable errors.</p>
  <div class="lit-card__tags"><span class="lit-tag">Behavioral Finance</span><span class="lit-tag">Finance</span></div>
</div>

<div class="lit-card" data-tags="quant-finance">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://www.jstor.org/stable/1926559" class="lit-card__title" target="_blank" rel="noopener">Lifetime Portfolio Selection By Dynamic Stochastic Programming</a>
  <p class="lit-card__authors">Paul A. Samuelson</p>
  
  <div class="lit-card__tags"><span class="lit-tag">Quant Finance</span></div>
</div>

<div class="lit-card" data-tags="finance">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://www.jstor.org/stable/4477805" class="lit-card__title" target="_blank" rel="noopener">Likely Gains from Market Timing</a>
  <p class="lit-card__authors">William F. Sharpe</p>
  <p class="lit-card__summary">The conclusion is fairly clear. Attempts to time the market are not likely to produce incremental re-turns of more than four per cent per year over the long run. Moreover, unless a manager can predict whether the market will be good or bad each year with considerable accuracy (e.g., be right at least seven times out of ten), he should probably avoid attempts to time the market altogether.</p>
  <div class="lit-card__tags"><span class="lit-tag">Finance</span></div>
</div>

<div class="lit-card" data-tags="portfolio-optimisation">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-book"></i> Book</span>
  </div>
  <a href="https://doi.org/10.1007/978-3-319-18482-1_2" class="lit-card__title" target="_blank" rel="noopener">Linear Models for Portfolio Optimization</a>
  <p class="lit-card__authors">Renata Mansini</p>
  <p class="lit-card__summary">Nowadays, Quadratic Programming (QP) models, like Markowitz model, are not hard to solve, thanks to technological and algorithmic progress. Nevertheless, Linear Programming (LP) models remain much more attractive from a computational point of view for several reasons. In order to guarantee that a portfolio takes advantage from diversification, no risk or safety measures can be a linear function of the weights of the assets. Is it possible to have linear models for portfolio optimization? How can we measure the risk or safety in order to have a linear model? In this chapter, we show how it is possible to achieve a linear form of the overall optimization problem for several different risk measures through the concept of scenarios for the rates of return. The variance is the classical statistical quantity used to measure the dispersion of a random variable from its mean. However, there are several other ways to measure dispersion. We introduce the mean absolute deviation (MAD), the Gini’s mean difference (GMD) as basic LP computable risk measures and the worst realization (Minimax) and the Conditional Value-at-Risk (CVaR) as basic LP computable safety measures. We show how from each risk measure it is possible to build its safety measure and vice versa. Ratio measures and further enhanced risk measures and shortfall risk measures based on the concept of risk as failure to achieve a defined target are also discussed.</p>
  <div class="lit-card__tags"><span class="lit-tag">Portfolio Optimisation</span></div>
</div>

<div class="lit-card" data-tags="artificial-intelligence finance portfolio-optimisation">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-book"></i> Book</span>
  </div>
  <a href="https://www.cambridge.org/core/elements/abs/machine-learning-for-asset-managers/6D9211305EA2E425D33A9F38D0AE3545" class="lit-card__title" target="_blank" rel="noopener">Machine Learning for Asset Managers</a>
  <p class="lit-card__authors">Marcos M. Lopez de Prado</p>
  <p class="lit-card__summary">Successful investment strategies are specific implementations of general theories. An investment strategy that lacks a theoretical justification is likely to be false. Hence, an asset manager should concentrate her efforts on developing a theory rather than on backtesting potential trading rules. The purpose of this Element is to introduce machine learning (ML) tools that can help asset managers discover economic and financial theories. ML is not a black box, and it does not necessarily overfit. ML tools complement rather than replace the classical statistical methods. Some of ML's strengths include (1) a focus on out-of-sample predictability over variance adjudication; (2) the use of computational methods to avoid relying on (potentially unrealistic) assumptions; (3) the ability to “learn” complex specifications, including nonlinear, hierarchical, and noncontinuous interaction effects in a high-dimensional space; and (4) the ability to disentangle the variable search from the specification search, robust to multicollinearity and other substitution effects.</p>
  <div class="lit-card__tags"><span class="lit-tag">Artificial Intelligence</span><span class="lit-tag">Finance</span><span class="lit-tag">Portfolio Optimisation</span></div>
</div>

<div class="lit-card" data-tags="finance">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-book"></i> Book</span>
  </div>
  <a href="https://www.amazon.com/Macroeconomics-Institutions-Instability-Financial-System/dp/0199655790" class="lit-card__title" target="_blank" rel="noopener">Macroeconomics</a>
  <p class="lit-card__authors">David Soskice, Wendy Carlin</p>
  <p class="lit-card__summary">The book used for all Macroeconomics topics.</p>
  <div class="lit-card__tags"><span class="lit-tag">Finance</span></div>
</div>

<div class="lit-card" data-tags="portfolio-optimisation">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2009778" class="lit-card__title" target="_blank" rel="noopener">Managing Risk Exposures Using the Risk Budgeting Approach</a>
  <p class="lit-card__authors">Benjamin Bruder, Thierry Roncalli</p>
  <p class="lit-card__summary">The ongoing economic crisis has profoundly changed the industry of the asset management, by putting risk management at the heart of most investment processes. This new risk-based investment style does not rely on returns forecasts and is therefore assumed to be more robust. In 2011, it has particularly encountered a great success with the achievement of minimum variance, ERC and risk parity strategies in portfolios of several large institutional investors. These portfolio constructions are special cases of a more general class of allocation models, known as the risk budgeting approach. In a risk budgeting portfolio, the risk contribution from each components is equal to the budget of risk defined by the portfolio manager. Unfortunately, even if risk budgeting techniques are widely used by market practitioners, they are few results about the behavior of such portfolios in the academic literature. In this paper, we derive the theoretical properties of the risk budgeting portfolio and show that its volatility is located between those of minimum variance and weight budgeting portfolios. We also discuss the existence, uniqueness and optimality of such a portfolio. In a second part of the paper, we propose several applications of risk budgeting techniques for risk-based allocation, like risk parity funds and strategic asset allocation, and equity and bond alternative indexations.</p>
  <div class="lit-card__tags"><span class="lit-tag">Portfolio Optimisation</span></div>
</div>

<div class="lit-card" data-tags="portfolio-optimisation">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://econpapers.repec.org/RePEc:inm:ormnsc:v:37:y:1991:i:5:p:519-531" class="lit-card__title" target="_blank" rel="noopener">Mean-Absolute Deviation Portfolio Optimization Model and Its Applications to Tokyo Stock Market</a>
  <p class="lit-card__authors">Hiroshi Konno</p>
  <p class="lit-card__summary">The purpose of this paper is to demonstrate that a portfolio optimization model using the L 1 risk (mean absolute deviation risk) function can remove most of the difficulties associated with the classical Markowitz's model while maintaining its advantages over equilibrium models. In particular, the L 1 risk model leads to a linear program instead of a quadratic program, so that a large-scale optimization problem consisting of more than 1,000 stocks may be solved on a real time basis. Numerical experiments using the historical data of NIKKEI 225 stocks show that the L 1 risk model generates a portfolio quite similar to that of the Markowitz's model within a fraction of time required to solve the latter.</p>
  <div class="lit-card__tags"><span class="lit-tag">Portfolio Optimisation</span></div>
</div>

<div class="lit-card" data-tags="finance">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-book"></i> Book</span>
  </div>
  <a href="https://www.amazon.com/Microeconomic-Theory-Basic-Principles-Extensions/dp/1305505794" class="lit-card__title" target="_blank" rel="noopener">Microeconomic Theory</a>
  <p class="lit-card__authors">Christopher Snyder, Walter Nicholson</p>
  <p class="lit-card__summary">This books aims at explaining Microeconomic theories like Utility functions, Supply/demand functions, Game Theory and Consumption models.</p>
  <div class="lit-card__tags"><span class="lit-tag">Finance</span></div>
</div>

<div class="lit-card" data-tags="behavioral-finance finance">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://www.nber.org/papers/w4369" class="lit-card__title" target="_blank" rel="noopener">Myopic Loss Aversion and the Equity Premium Puzzle</a>
  <p class="lit-card__authors">Richard H. Thaler, Shlomo Benartzi</p>
  <p class="lit-card__summary">Using simulations, we find that the size of the equity premium is consistent with the previously estimated parameters of prospect theory if investors evaluate their portfolios annually.</p>
  <div class="lit-card__tags"><span class="lit-tag">Behavioral Finance</span><span class="lit-tag">Finance</span></div>
</div>

<div class="lit-card" data-tags="finance">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://www.jstor.org/stable/2329556" class="lit-card__title" target="_blank" rel="noopener">On Persistence in Mutual Fund Performance</a>
  <p class="lit-card__authors">Mark M. Carhart</p>
  <p class="lit-card__summary">Using a sample free of survivor bias, I demonstrate that common factors in stock returns and investment expenses almost completely explain persistence in equity mutual funds' mean and risk-adjusted returns.</p>
  <div class="lit-card__tags"><span class="lit-tag">Finance</span></div>
</div>

<div class="lit-card" data-tags="portfolio-optimisation">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://www.sciencedirect.com/science/article/abs/pii/S037722171630861X?via%3Dihub" class="lit-card__title" target="_blank" rel="noopener">On the Bayesian interpretation of Black-Litterman</a>
  <p class="lit-card__authors">Gordon Ritter, Petter N. Kolm</p>
  <p class="lit-card__summary">We present the most general model of the type considered by Black and Litterman (1991) after fully clarifying the duality between Black-Litterman optimization and Bayesian regression. Our generalization is itself a special case of a Bayesian network or graphical model. As an example, we work out in full detail the treatment of views on factor risk premia in the context of APT. We also consider a more speculative example in which the portfolio manager specifies a view on realized volatility by trading a variance swap.</p>
  <div class="lit-card__tags"><span class="lit-tag">Portfolio Optimisation</span></div>
</div>

<div class="lit-card" data-tags="finance">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://www.jstor.org/stable/4479842" class="lit-card__title" target="_blank" rel="noopener">On the Risk of Stocks in the Long Run</a>
  <p class="lit-card__authors">Zvi Bodie</p>
  <p class="lit-card__summary">For guarantors of money-fixed annuities, the proposition that stocks in their portfolios are a better hedge the longer the maturity of their obligations is unambiguously wrong</p>
  <div class="lit-card__tags"><span class="lit-tag">Finance</span></div>
</div>

<div class="lit-card" data-tags="behavioral-finance finance">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://www.jstor.org/stable/222543" class="lit-card__title" target="_blank" rel="noopener">On the Timing Ability of Mutual Fund Managers</a>
  <p class="lit-card__authors">Jeffrey A. Busse, Nicholas P.B. Bollen</p>
  <p class="lit-card__summary">The daily timing coefficients of the majority of funds are significantly different from their synthetic counterparts. These results suggest that mutual funds may possess more timing ability than previously documented,</p>
  <div class="lit-card__tags"><span class="lit-tag">Behavioral Finance</span><span class="lit-tag">Finance</span></div>
</div>

<div class="lit-card" data-tags="portfolio-optimisation">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://www.risk.net/journal-risk/2161159/optimization-conditional-value-risk" class="lit-card__title" target="_blank" rel="noopener">Optimization of conditional value-at-risk</a>
  <p class="lit-card__authors">R. Tyrell Rockafellar</p>
  <p class="lit-card__summary">A new approach to optimizing or hedging a portfolio of financial instruments to reduce risk is presented and tested on applications. It focuses on minimizing conditional value-at-risk (CVaR) rather than minimizing value-at-risk (VaR), but portfolios with low CVaR necessarily have low VaR as well. CVaR, also called mean excess loss, mean shortfall, or tail VaR, is in any case considered to be a more consistent measure of risk than VaR. Central to the new approach is a technique for portfolio optimization which calculates VaR and optimizes CVaR simultaneously. This technique is suitable for use by investment companies, brokerage firms, mutual funds, and any business that evaluates risk. It can be combined with analytical or scenario-based methods to optimize portfolios with large numbers of instruments, in which case the calculations often come down to linear programming or nonsmooth programming. The methodology can also be applied to the optimization of percentiles in contexts outside of finance.</p>
  <div class="lit-card__tags"><span class="lit-tag">Portfolio Optimisation</span></div>
</div>

<div class="lit-card" data-tags="quant-finance">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-book"></i> Book</span>
  </div>
  <a href="https://www.amazon.com/Options-Futures-Other-Derivatives-9th/dp/0133456315" class="lit-card__title" target="_blank" rel="noopener">Options, Futures and Other Derivatives</a>
  <p class="lit-card__authors">John C. Hull</p>
  <p class="lit-card__summary">Options, Futures, and Other Derivatives can be used for a first course in derivatives or for a more advanced course. There are many different ways it can be used in the classroom.</p>
  <div class="lit-card__tags"><span class="lit-tag">Quant Finance</span></div>
</div>

<div class="lit-card" data-tags="portfolio-optimisation">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://journals.aps.org/pre/abstract/10.1103/PhysRevE.94.062306" class="lit-card__title" target="_blank" rel="noopener">Parsimonious modelling with information filtering networks</a>
  <p class="lit-card__authors">Wolfram Barfuss</p>
  <p class="lit-card__summary">We introduce a methodology to construct parsimonious probabilistic models. This method makes use of information filtering networks to produce a robust estimate of the global sparse inverse covariance from a simple sum of local inverse covariances computed on small subparts of the network. Being based on local and low-dimensional inversions, this method is computationally very efficient and statistically robust, even for the estimation of inverse covariance of high-dimensional, noisy, and short time series. Applied to financial data our method results are computationally more efficient than state-of-the-art methodologies such as Glasso producing, in a fraction of the computation time, models that can have equivalent or better performances but with a sparser inference structure. We also discuss performances with sparse factor models where we notice that relative performances decrease with the number of factors. The local nature of this approach allows us to perform computations in parallel and provides a tool for dynamical adaptation by partial updating when the properties of some variables change without the need of recomputing the whole model. This makes this approach particularly suitable to handle big data sets with large numbers of variables. Examples of practical application for forecasting, stress testing, and risk allocation in financial systems are also provided.</p>
  <div class="lit-card__tags"><span class="lit-tag">Portfolio Optimisation</span></div>
</div>

<div class="lit-card" data-tags="portfolio-optimisation">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://ideas.repec.org/h/wsi/wschap/9789812562586_0013.html" class="lit-card__title" target="_blank" rel="noopener">Portfolio Optimization With Drawdown Constraints</a>
  <p class="lit-card__authors">A. Chekhlov</p>
  <p class="lit-card__summary">We propose a new one-parameter family of risk measures, which is called Conditional Draw-down-at-Risk (CDaR). These measures of risk are functionals of the portfolio drawdown (underwater) curve considered in an active portfolio management. For some value of the tolerance parameter β, the CDaR is defined as the mean of the worst (1 - β) * 100% drawdowns. The CDaR risk measure includes the Maximal Drawdown and Average Drawdown as its limiting cases. For a particular example, we find the optimal portfolios for a case of Maximal Drawdown, a case of Average Drawdown, and several intermediate cases between these two. The CDaR family of risk measures is similar to Conditional Value-at-Risk (CVaR), which is also called Mean Shortfall, Mean Access loss, or Tail Value-at-Risk. Some recommendations on how to select the optimal risk measure for getting practically stable portfolios are provided. We solved a real life portfolio allocation problem using the proposed measures.</p>
  <div class="lit-card__tags"><span class="lit-tag">Portfolio Optimisation</span></div>
</div>

<div class="lit-card" data-tags="portfolio-optimisation">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="http://www.jstor.org/stable/2975974" class="lit-card__title" target="_blank" rel="noopener">Portfolio Selection</a>
  <p class="lit-card__authors">Harry Markowitz</p>
  <p class="lit-card__summary">The hypothesis (or maxim) that the investor does (or should) maximize discounted return must be rejected. If we ignore market imperfections the foregoing rule never implies that there is a diversified portfolio which is preferable to all non-diversified portfolios. Diversification is both observed and sensible; a rule of behavior which does not imply the superiority of diversification must be rejected both as a hypothesis and as a maxim.</p>
  <div class="lit-card__tags"><span class="lit-tag">Portfolio Optimisation</span></div>
</div>

<div class="lit-card" data-tags="portfolio-optimisation">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://www.sciencedirect.com/science/article/abs/pii/S0377221719301183?via%3Dihub" class="lit-card__title" target="_blank" rel="noopener">Portfolio optimization with entropic value-at-risk</a>
  <p class="lit-card__authors">A. Ahmadi-Javid</p>
  <p class="lit-card__summary">The entropic value-at-risk (EVaR) is a new coherent risk measure, which is an upper bound for both the value-at-risk (VaR) and conditional value-at-risk (CVaR). One of the important properties of the EVaR is that it is strongly monotone over its domain and strictly monotone over a broad sub-domain including all continuous distributions, whereas well-known monotone risk measures such as the VaR and CVaR lack this property. A key feature of a risk measure, besides its financial properties, is its applicability in large-scale sample based portfolio optimization. If the negative return of an investment portfolio is a differentiable convex function for any sampling observation, the portfolio optimization with the EVaR results in a differentiable convex program whose number of variables and constraints is independent of the sample size, which is not the case for the VaR and CVaR even if the portfolio rate linearly depends on the decision variables. This enables us to design an efficient algorithm using differentiable convex optimization. Our extensive numerical study indicates the high efficiency of the algorithm in large scales, when compared with the existing convex optimization software packages. The computational efficiency of the EVaR and CVaR approaches are generally similar, but the EVaR approach outperforms the other as the sample size increases. Moreover, the comparison of the portfolios obtained for a real case by the EVaR and CVaR approaches shows that the EVaR-based portfolios can have better best, mean, and worst return rates as well as Sharpe ratios.</p>
  <div class="lit-card__tags"><span class="lit-tag">Portfolio Optimisation</span></div>
</div>

<div class="lit-card" data-tags="esg finance">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3932484" class="lit-card__title" target="_blank" rel="noopener">Private Debt Fund Returns and General Partner Skills</a>
  <p class="lit-card__authors">Pascal Böni, Sophie Manigart</p>
  <p class="lit-card__summary">This paper examines net of fees private debt fund performance and general partner skills, i.e., performance persistence across funds and a general partner’s ability to time the market. We document market outperformance in the cross- section against bond and equity market benchmarks.</p>
  <div class="lit-card__tags"><span class="lit-tag">ESG</span><span class="lit-tag">Finance</span></div>
</div>

<div class="lit-card" data-tags="behavioral-finance finance">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://www.jstor.org/stable/1914185" class="lit-card__title" target="_blank" rel="noopener">Prospect Theory: An Analysis of Decision under Risk</a>
  <p class="lit-card__authors">Amos Tversky, Daniel Kahneman</p>
  <p class="lit-card__summary">This paper presents a critique of expected utility theory as a descriptive model of decision making under risk, and develops an alternative model, called prospect theory.</p>
  <div class="lit-card__tags"><span class="lit-tag">Behavioral Finance</span><span class="lit-tag">Finance</span></div>
</div>

<div class="lit-card" data-tags="finance">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://www.jstor.org/stable/3083270" class="lit-card__title" target="_blank" rel="noopener">Risk Aversion and Incentive Effects</a>
  <p class="lit-card__authors">Charles A. Holt, Susan K. Laury</p>
  <p class="lit-card__summary">One implication of these results is that, contrary to Kahneman and Tversky’s supposition, subjects facing hypothetical choices cannot imagine how they would actually behave under high-incentive conditions. Moreover, these differences are not symmetric: subjects typically underestimate the extent to which they will avoid risk. Second, the clear evidence for risk aversion, even with low stakes, suggests the potential danger of analyzing behavior under the simplifying assumption of risk neutrality.</p>
  <div class="lit-card__tags"><span class="lit-tag">Finance</span></div>
</div>

<div class="lit-card" data-tags="finance">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-book"></i> Book</span>
  </div>
  <a href="https://www.amazon.com/Management-Financial-Institutions-Wiley-Finance/dp/1118955943" class="lit-card__title" target="_blank" rel="noopener">Risk Managements and Financial Institutions</a>
  <p class="lit-card__authors">John C. Hull</p>
  <p class="lit-card__summary">The book is designed to be suitable for practicing managers as well as university students. Those studying for FMA and PRM qualifications will also find the book useful.</p>
  <div class="lit-card__tags"><span class="lit-tag">Finance</span></div>
</div>

<div class="lit-card" data-tags="portfolio-optimisation">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://www.mdpi.com/1911-8074/13/10/237/htm" class="lit-card__title" target="_blank" rel="noopener">Risk return trade-off in relaxed risk parity portfolio optimization</a>
  <p class="lit-card__authors">Roy Kwon, Vaughn Gambeta</p>
  <p class="lit-card__summary">This paper formulates a relaxed risk parity optimization model to control the balance of risk parity violation against the total portfolio performance. Risk parity has been criticized as being overly conservative and it is improved by re-introducing the asset expected returns into the model and permitting the portfolio to violate the risk parity condition. This paper proposes the incorporation of an explicit target return goal with an intuitive target return approach into a second-order-cone model of a risk parity optimization. When the target return is greater than risk parity return, a violation to risk parity allocations occurs that is controlled using a computational construct to obtain near-risk parity portfolios to retain as much risk parity-like traits as possible. This model is used to demonstrate empirically that higher returns can be achieved than risk parity without the risk contributions deviating dramatically from the risk parity allocations. Furthermore, this study reveals that the relaxed risk parity model exhibits advantageous traits of robustness to expected returns, which should not deter the use of expected returns in risk parity model.</p>
  <div class="lit-card__tags"><span class="lit-tag">Portfolio Optimisation</span></div>
</div>

<div class="lit-card" data-tags="portfolio-optimisation">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://link.springer.com/article/10.1023/B:ANOR.0000045281.41041.ed" class="lit-card__title" target="_blank" rel="noopener">Robust asset allocation</a>
  <p class="lit-card__authors">M. Koenig</p>
  <p class="lit-card__summary">This article addresses the problem of finding an optimal allocation of funds among different asset classes in a robust manner when the estimates of the structure of returns are unreliable. Instead of point estimates used in classical mean-variance optimization, moments of returns are described using uncertainty sets that contain all, or most, of their possible realizations. The approach presented here takes a conservative viewpoint and identifies asset mixes that have the best worst-case behavior. Techniques for generating uncertainty sets from historical data are discussed and numerical results that illustrate the stability of robust optimal asset mixes are reported.</p>
  <div class="lit-card__tags"><span class="lit-tag">Portfolio Optimisation</span></div>
</div>

<div class="lit-card" data-tags="portfolio-optimisation">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://jpm.pm-research.com/content/33/3/40" class="lit-card__title" target="_blank" rel="noopener">Robust portfolio optimization and management</a>
  <p class="lit-card__authors">Dessislava A. Pachamanova, Frank J. Fabozzi, Petter N. Kolm, Sergio M. Focardi</p>
  <p class="lit-card__summary">As quantitative techniques have become commonplace in the investment industry, the mitigation of estimation and model risk in portfolio management has grown in importance. Robust optimization, which incorporates estimation error directly into the portfolio optimization process, is typically used with conventional robust statistical estimation methods. This perspective on the robust optimization approach reviews useful practical extensions and discusses potential applications for robust portfolio optimization.</p>
  <div class="lit-card__tags"><span class="lit-tag">Portfolio Optimisation</span></div>
</div>

<div class="lit-card" data-tags="finance">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://www.sciencedirect.com/science/article/abs/pii/S0304405X14002542" class="lit-card__title" target="_blank" rel="noopener">Scale and Skill in Active Management</a>
  <p class="lit-card__authors">Lubos Pastor</p>
  <p class="lit-card__summary">We find strong evidence of decreasing returns at the industry level: As the size of the active mutual fund industry increases, a fund's ability to outperform passive benchmarks declines. We also find that the active management industry has become more skilled over time. Finally, we find that performance deteriorates over a typical fund's lifetime. This result can also be explained by industry-level decreasing returns to scale.</p>
  <div class="lit-card__tags"><span class="lit-tag">Finance</span></div>
</div>

<div class="lit-card" data-tags="portfolio-optimisation">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://www.jstor.org/stable/pdf/1808584.pdf" class="lit-card__title" target="_blank" rel="noopener">Stochastic Dominance, Mean Variance, and Gini's Mean Difference</a>
  <p class="lit-card__authors">Shlomo Yitzhaki</p>
  <p class="lit-card__summary">The connection between stochastic dominance and the Lorenz curve was first demonstrated by A. B. Atkinson. However, the use of Gini's mean difference has until now been restricted because the variance has many similar properties and is simpler to compute. In this paper it is shown that Gini's mean difference has some theoretical merits. When using the mean and Gini's mean difference instead of the mean and variance, necessary conditions on stochastic dominance are obtained. This enables us to reduce the size of the SD efficient set. Furthermore, using MG and MF enables us to construct efficient portfolios in the SD sense.</p>
  <div class="lit-card__tags"><span class="lit-tag">Portfolio Optimisation</span></div>
</div>

<div class="lit-card" data-tags="portfolio-optimisation">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1347648" class="lit-card__title" target="_blank" rel="noopener">The Augmented Black-Litterman Model: A Ranking-Free Approach to Factor-Based Portfolio Construction and Beyond</a>
  <p class="lit-card__authors">Wing Cheung</p>
  <p class="lit-card__summary">The Fama and French factor-ranking approach (1992, 1993, etc.) has been extensively applied in quantitative fund management. However, this approach suffers from hidden factor view, information inefficiency, etc. issues. Based on the Black--Litterman model (1992; as explained in Cheung 2010b), we develop a technique that endogenizes the ranking process and elegantly resolves these issues. This model explicitly seeks forward-looking factor views and smoothly blends them to deliver robust allocation to securities. Our numerical experiments show this is an intuitive and practical framework for factor-based portfolio construction, and beyond. This article features: (1) a new and unified framework for strategy combination, factor mimicking and security-specific bets; (2) an elegant and ranking-free approach to factor style construction; (3) worked examples based on the FTSE EUROTOP 100 universe; (4) insight into the classic issue of confidence parameter setting; and (5) implementation guidance in an appendix.</p>
  <div class="lit-card__tags"><span class="lit-tag">Portfolio Optimisation</span></div>
</div>

<div class="lit-card" data-tags="portfolio-optimisation">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1314585" class="lit-card__title" target="_blank" rel="noopener">The Black-Litterman Model in Detail</a>
  <p class="lit-card__authors">Jay Walters</p>
  <p class="lit-card__summary">In this paper we survey the literature on the Black-Litterman model. This survey is provided both as a chronology and a taxonomy as there are many claims on the model in the literature. We provide a complete description of the canonical model including full derivations from the underlying principles using both Theil's Mixed Estimation model and Bayes Theory. The various parameters of the model are considered, along with information on their computation or calibration. Further consideration is given to several of the key papers, with worked examples illustrating the concepts.</p>
  <div class="lit-card__tags"><span class="lit-tag">Portfolio Optimisation</span></div>
</div>

<div class="lit-card" data-tags="factor-investing finance">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2998754" class="lit-card__title" target="_blank" rel="noopener">The Death of Diversification Has Been Greatly Exaggerated</a>
  <p class="lit-card__authors">Antti Ilmanen, Jared Kizer</p>
  <p class="lit-card__summary">There is ample room for improvement by shifting the focus from asset class diversification to factor diversification.</p>
  <div class="lit-card__tags"><span class="lit-tag">Factor Investing</span><span class="lit-tag">Finance</span></div>
</div>

<div class="lit-card" data-tags="behavioral-finance finance">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://eml.berkeley.edu/~craine/EconH195/Fall_16/webpage/Malkiel_Efficient%20Mkts.pdf" class="lit-card__title" target="_blank" rel="noopener">The Efficient Market Hypothesis and Its Critics</a>
  <p class="lit-card__authors">Burton G. Malkiel</p>
  <p class="lit-card__summary">As long as stock markets exist, the collective judgment of investors will sometimes make mistakes. Undoubtedly, some market participants are demonstrably less than rational. However, I suspect that the end result will not be an abandonment of the belief of many in the profession that the stock market is remarkably efficient in its utilization of information.</p>
  <div class="lit-card__tags"><span class="lit-tag">Behavioral Finance</span><span class="lit-tag">Finance</span></div>
</div>

<div class="lit-card" data-tags="finance">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2732060" class="lit-card__title" target="_blank" rel="noopener">The Harm in Selecting Funds That Have Recently Outperformed</a>
  <p class="lit-card__authors">Bradford Cornell</p>
  <p class="lit-card__summary">Instead, the practical implication of our paper is that asset owners should focus on factors other than past performance when selecting managers. We offer possible criteria that could be employed in this context.</p>
  <div class="lit-card__tags"><span class="lit-tag">Finance</span></div>
</div>

<div class="lit-card" data-tags="portfolio-optimisation">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3237540" class="lit-card__title" target="_blank" rel="noopener">The Hierarchical Equal Risk Contribution Portfolio</a>
  <p class="lit-card__authors">Thomas Raffinot</p>
  <p class="lit-card__summary">Building upon the fundamental notion of hierarchy, the &quot;Hierarchical Risk Parity&quot; (HRP) and the &quot;Hierarchical Clustering based Asset Allocation&quot; (HCAA), the Hierarchical Equal Risk Contribution Portfolio (HERC) aims at diversifying capital allocation and risk allocation. HERC merges and enhances the machine learning approach of HCAA and the Top-Down recursive bisection of HRP. In more detail, the modified Top-Down recursive division is based on the shape of dendrogram, follows an Equal Risk Contribution allocation and is extended to downside risk measures such as conditional value at risk (CVaR) and Conditional Drawdown at Risk (CDaR). The out-of-sample performances of hierarchical clustering based portfolios are evaluated across two empirical datasets, which differ in terms of number of assets and composition of the universe (multi-assets and individual stocks). Empirical results highlight that HERC Portfolios based on downside risk measures achieve statistically better risk-adjusted performances, especially those based on the CDaR.</p>
  <div class="lit-card__tags"><span class="lit-tag">Portfolio Optimisation</span></div>
</div>

<div class="lit-card" data-tags="behavioral-finance finance">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://www.aeaweb.org/articles?id=10.1257/jep.1.1.197" class="lit-card__title" target="_blank" rel="noopener">The January Effect</a>
  <p class="lit-card__authors">Richard H. Thaler</p>
  <p class="lit-card__summary">A natural question to ask is whether these anomalies imply profitable trading strategies. This question turns out to be difficult to answer. In the case of small firms, small trading volume and large bid-ask spreads militate against big profit opportunities.</p>
  <div class="lit-card__tags"><span class="lit-tag">Behavioral Finance</span><span class="lit-tag">Finance</span></div>
</div>

<div class="lit-card" data-tags="portfolio-optimisation">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://doi.org/10.1016/B978-044453248-0.50015-0" class="lit-card__title" target="_blank" rel="noopener">The Kelly Criterion in Blackjack Sports Betting, and the Stock Market</a>
  <p class="lit-card__authors">Edward O. Thorp</p>
  <p class="lit-card__summary">We will present some useful formulas and methods to answer various natural questions about it that arise in blackjack and other gambling games. Then we illustrate its recent use in a successful casino sports betting system. Finally, we discuss its application to the securities markets where it has helped the author to make a thirty year total of 80 billion dollars worth of &quot;bets&quot;.</p>
  <div class="lit-card__tags"><span class="lit-tag">Portfolio Optimisation</span></div>
</div>

<div class="lit-card" data-tags="finance">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://jpm.pm-research.com/content/14/3/40" class="lit-card__title" target="_blank" rel="noopener">The Mechanics of Portfolio Insurance</a>
  <p class="lit-card__authors">Thomas J. O'Brien</p>
  <p class="lit-card__summary">The article has presented a line of analysis designed to clarify the mysteries of the basic portfolio insurance concept. A simplified abstraction of reality shows that portfolio insurance works. With an understanding of the mechanics and cost concepts presented here, the analyst may proceed to consider aspects of real-world application.</p>
  <div class="lit-card__tags"><span class="lit-tag">Finance</span></div>
</div>

<div class="lit-card" data-tags="factor-investing finance">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://papers.ssrn.com/sol3/papers.cfm?abstract_id=980865" class="lit-card__title" target="_blank" rel="noopener">The Volatility Effect</a>
  <p class="lit-card__authors">David C. Blitz, Pim van Vliet</p>
  <p class="lit-card__summary">We have shown that stocks with low historical volatility have superior risk-adjusted returns, both in terms of Sharpe ratios and in terms of CAPM alphas. The volatility effect is similar in size to classic effects such as value, size, and momentum, and largely remains after Fama-French adjustments and double-sorts.</p>
  <div class="lit-card__tags"><span class="lit-tag">Factor Investing</span><span class="lit-tag">Finance</span></div>
</div>

<div class="lit-card" data-tags="portfolio-optimisation">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <a href="https://web.stanford.edu/~boyd/papers/pdf/risk_bnd.pdf" class="lit-card__title" target="_blank" rel="noopener">The worst-case risk of a portfolio</a>
  <p class="lit-card__authors">Miguel Sousa Lobo, Stephen Boyd</p>
  <p class="lit-card__summary">We show how to compute in a numerically efficient way the maximum risk of a portfolio, given uncertainty in the means and covariances of asset returns. This is a semidefinite programming problem, and is readily solved by interior-point methods for convex optimization developed in recent years. While not as general, this approach is more accurate and much faster than Monte Carlo methods. The computational effort required grows gracefully, so that very large problems can be handled. The proposed approach is extended to portfolio selection, allowing for the design of portfolios which are robust with respect to model uncertainty.</p>
  <div class="lit-card__tags"><span class="lit-tag">Portfolio Optimisation</span></div>
</div>

<div class="lit-card" data-tags="portfolio-optimisation">
  <div class="lit-card__header">
    <span class="lit-badge"><i class="fas fa-file-alt"></i> Article</span>
  </div>
  <span class="lit-card__title"></span>
  
  
  <div class="lit-card__tags"><span class="lit-tag">Portfolio Optimisation</span></div>
</div>

</div>
<p class="lit-empty" id="lit-empty" style="display:none;">No entries match the selected filter.</p>

<script>
document.addEventListener('DOMContentLoaded', function () {
  var cards = Array.from(document.querySelectorAll('.lit-card'));
  var buttons = Array.from(document.querySelectorAll('.lit-filter'));
  var empty = document.getElementById('lit-empty');

  buttons.forEach(function (btn) {
    var filter = btn.dataset.filter;
    var countEl = btn.querySelector('.lit-count');
    if (!countEl) return;
    var n = filter === 'all'
      ? cards.length
      : cards.filter(function (c) { return c.dataset.tags.split(' ').indexOf(filter) !== -1; }).length;
    countEl.textContent = '(' + n + ')';
  });

  buttons.forEach(function (btn) {
    btn.addEventListener('click', function () {
      buttons.forEach(function (b) { b.classList.remove('active'); });
      btn.classList.add('active');
      var filter = btn.dataset.filter;
      var visible = 0;
      cards.forEach(function (card) {
        var show = filter === 'all' || card.dataset.tags.split(' ').indexOf(filter) !== -1;
        card.style.display = show ? '' : 'none';
        if (show) visible++;
      });
      empty.style.display = visible === 0 ? '' : 'none';
    });
  });
});
</script>
