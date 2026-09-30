---
layout: splash
title: "Jeroen Bouma"
description: "Jeroen Bouma, Quantitative Investment Strategist, creator of the open-source Finance Toolkit and Finance Database Python libraries (10,000+ GitHub stars)."
excerpt: "Quantitative Investment Strategist and Python developer. Creator of Finance Toolkit and Finance Database."
classes: custom-splash home-v2
---
{%- assign latest_articles = site.pages | where: "collection", "article" | sort: "date" | reverse -%}
<div class="hp">

<section class="hp-hero">
  <div class="hp-hero__glow" aria-hidden="true"></div>
  <div class="hp-hero__text">
    <h1 class="hp-title">Where quantitative finance <span class="hp-accent">meets AI.</span></h1>
    <p class="hp-lead">I'm <strong>Jeroen Bouma</strong>. I build quantitative and AI models within asset management, covering asset liability management, lifecycle investing, portfolio optimization and Solvency II internal model calculations. In my own time I create open-source tools like the <a href="/projects/financetoolkit">Finance Toolkit</a> and <a href="/projects/financedatabase">Finance Database</a>, used worldwide by developers, researchers and investors.</p>
    <div class="hp-actions">
      <a href="/resume" class="hp-btn hp-btn--primary">View my resume <i class="fas fa-arrow-right" aria-hidden="true"></i></a>
      <a href="/projects" class="hp-btn hp-btn--ghost">Explore my projects</a>
    </div>
  </div>
  <div class="hp-hero__visual">
    <div class="hp-portrait">
      <img src="/assets/images/default/bio-photo.jpg" alt="Jeroen Bouma" width="640" height="654" fetchpriority="high">
    </div>
  </div>
</section>

<section data-reveal class="hp-logos" aria-label="Where I have worked and studied">
  <p class="hp-logos__label">Experience and education</p>
  <div class="hp-logos__row">
    <span class="hp-logos__tile"><img src="/assets/images/resume/asr.png" alt="a.s.r. asset management" loading="lazy"></span>
    <span class="hp-logos__tile"><img src="/assets/images/resume/pggm.png" alt="PGGM" loading="lazy"></span>
    <span class="hp-logos__tile"><img src="/assets/images/resume/openbb.png" alt="OpenBB" loading="lazy"></span>
    <span class="hp-logos__tile"><img src="/assets/images/resume/cfasocietynetherlands.png" alt="CFA Society Netherlands" loading="lazy"></span>
    <span class="hp-logos__tile"><img src="/assets/images/resume/utrechtuniversity.png" alt="Utrecht University" loading="lazy"></span>
  </div>
</section>

<section data-reveal class="hp-section">
  <p class="hp-kicker">Explore</p>
  <h2 class="hp-h2">Everything in one place</h2>
  <div class="hp-pillars">
    <a class="hp-pillar" href="/resume">
      <i class="fas fa-briefcase" aria-hidden="true"></i>
      <h3>Experience</h3>
      <p>Investment strategy at a.s.r., ALM at PGGM and product management at OpenBB.</p>
      <span class="hp-more">Resume <i class="fas fa-arrow-right" aria-hidden="true"></i></span>
    </a>
    <a class="hp-pillar" href="/projects">
      <i class="fas fa-code-branch" aria-hidden="true"></i>
      <h3>Open Source Projects</h3>
      <p>The Finance Toolkit, Finance Database and an MCP server that brings them to AI assistants.</p>
      <span class="hp-more">Projects <i class="fas fa-arrow-right" aria-hidden="true"></i></span>
    </a>
    <a class="hp-pillar" href="/modelling/introduction">
      <i class="fas fa-cubes" aria-hidden="true"></i>
      <h3>Financial Modelling</h3>
      <p>A practical guide to building financial models in Python that stay maintainable.</p>
      <span class="hp-more">Guide <i class="fas fa-arrow-right" aria-hidden="true"></i></span>
    </a>
    <a class="hp-pillar" href="/appearances">
      <i class="fas fa-microphone" aria-hidden="true"></i>
      <h3>Talks &amp; Writing</h3>
      <p>Talks at universities and conferences, articles and a curated reading list.</p>
      <span class="hp-more">Media <i class="fas fa-arrow-right" aria-hidden="true"></i></span>
    </a>
  </div>
</section>

<section data-reveal class="hp-spotlight">
  <div class="hp-spotlight__text">
    <p class="hp-kicker">Featured project</p>
    <h2 class="hp-h2">The Finance Toolkit</h2>
    <p>An open-source Python library with 500+ financial methods, from ratios and valuation models to risk, performance and econometrics. Every formula is written out, so you can see exactly how a number is calculated. The MCP server makes all of it available to AI assistants such as Claude and ChatGPT.</p>
    <div class="hp-stats">
      <div><strong data-stars data-count>5,300+</strong><span>GitHub stars</span></div>
      <div><strong data-count>500+</strong><span>financial methods</span></div>
      <div><strong data-count>600,000+</strong><span>downloads</span></div>
    </div>
    <div class="hp-actions">
      <a href="/projects/financetoolkit" class="hp-btn hp-btn--primary">Explore the Finance Toolkit</a>
      <a href="/projects/financetoolkit/mcp" class="hp-btn hp-btn--ghost">Use it with AI</a>
    </div>
  </div>
  <div class="hp-code" data-tabs aria-label="Finance Toolkit examples">
    <div class="hp-code__bar"><span></span><span></span><span></span>
      <div class="hp-code__tabs" role="tablist">
        <button type="button" role="tab" class="hp-code__tab is-active" aria-selected="true" data-tab="valuation">Valuation</button>
        <button type="button" role="tab" class="hp-code__tab" aria-selected="false" data-tab="risk">Risk</button>
        <button type="button" role="tab" class="hp-code__tab" aria-selected="false" data-tab="macro">Macro</button>
        <button type="button" role="tab" class="hp-code__tab" aria-selected="false" data-tab="ratios">Ratios</button>
      </div>
    </div>
    <div class="hp-code__panel" role="tabpanel" data-panel="valuation">
<div class="hp-code__src"><span class="k">from</span> financetoolkit <span class="k">import</span> Toolkit

toolkit = Toolkit([<span class="s">"AAPL"</span>, <span class="s">"TSLA"</span>], api_key=API_KEY)

<span class="c"># Bankruptcy risk, built up from five balance sheet ratios</span>
toolkit.models.<span class="f">get_altman_z_score</span>().loc[<span class="s">"AAPL"</span>]</div>
      <div class="hp-code__out" style="--cols:4">
        <div class="hp-code__row hp-code__row--head"><span>AAPL</span><span>2023</span><span>2024</span><span>2025</span></div>
        <div class="hp-code__row"><span>EBIT / Total Assets</span><span>0.33</span><span>0.34</span><span>0.37</span></div>
        <div class="hp-code__row"><span>Market Value / Liabilities</span><span>10.48</span><span>12.53</span><span>14.29</span></div>
        <div class="hp-code__row"><span>Sales / Total Assets</span><span>1.09</span><span>1.07</span><span>1.16</span></div>
        <div class="hp-code__row"><span>Altman Z-Score</span><span>8.47</span><span>9.55</span><span>10.84</span></div>
      </div>
    </div>
    <div class="hp-code__panel" role="tabpanel" data-panel="risk" hidden>
<div class="hp-code__src"><span class="k">from</span> financetoolkit <span class="k">import</span> Toolkit

toolkit = Toolkit([<span class="s">"AMZN"</span>, <span class="s">"TSLA"</span>], api_key=API_KEY)

<span class="c"># Worst peak-to-trough decline in each year</span>
toolkit.risk.<span class="f">get_maximum_drawdown</span>()</div>
      <div class="hp-code__out" style="--cols:5">
        <div class="hp-code__row hp-code__row--head"><span></span><span>2020</span><span>2021</span><span>2022</span><span>2023</span></div>
        <div class="hp-code__row"><span>AMZN</span><span>-22.7%</span><span>-14.6%</span><span>-52.0%</span><span>-19.6%</span></div>
        <div class="hp-code__row"><span>TSLA</span><span>-60.6%</span><span>-36.3%</span><span>-72.7%</span><span>-28.2%</span></div>
      </div>
    </div>
    <div class="hp-code__panel" role="tabpanel" data-panel="macro" hidden>
<div class="hp-code__src"><span class="k">from</span> financetoolkit <span class="k">import</span> Economics

<span class="c"># No API key needed for macroeconomic data</span>
economics = Economics(start_date=<span class="s">"2022-01-01"</span>)

economics.<span class="f">get_unemployment_rate</span>(
    countries=[<span class="s">"Germany"</span>, <span class="s">"United States"</span>, <span class="s">"Japan"</span>],
    period=<span class="s">"quarterly"</span>)</div>
      <div class="hp-code__out" style="--cols:4">
        <div class="hp-code__row hp-code__row--head"><span></span><span>Germany</span><span>United States</span><span>Japan</span></div>
        <div class="hp-code__row"><span>2022Q2</span><span>3.1%</span><span>3.6%</span><span>2.6%</span></div>
        <div class="hp-code__row"><span>2022Q4</span><span>3.1%</span><span>3.6%</span><span>2.5%</span></div>
        <div class="hp-code__row"><span>2023Q1</span><span>3.0%</span><span>3.5%</span><span>2.6%</span></div>
      </div>
    </div>
    <div class="hp-code__panel" role="tabpanel" data-panel="ratios" hidden>
<div class="hp-code__src"><span class="k">from</span> financetoolkit <span class="k">import</span> Toolkit

toolkit = Toolkit([<span class="s">"AAPL"</span>, <span class="s">"TSLA"</span>], api_key=API_KEY)

<span class="c"># One of 150+ ratios, each with its formula documented</span>
toolkit.ratios.<span class="f">get_price_to_earnings_ratio</span>()</div>
      <div class="hp-code__out" style="--cols:4">
        <div class="hp-code__row hp-code__row--head"><span></span><span>2023</span><span>2024</span><span>2025</span></div>
        <div class="hp-code__row"><span>AAPL</span><span>31.39</span><span>41.16</span><span>36.42</span></div>
        <div class="hp-code__row"><span>TSLA</span><span>57.70</span><span>198.13</span><span>418.19</span></div>
      </div>
    </div>
  </div>
</section>

<section data-reveal class="hp-section hp-writing">
  <div class="hp-writing__head">
    <div>
      <p class="hp-kicker">Writing</p>
      <h2 class="hp-h2">Latest articles</h2>
    </div>
    <a href="/articles" class="hp-link">All articles <i class="fas fa-arrow-right" aria-hidden="true"></i></a>
  </div>
  <div class="hp-list">
    {%- for article in latest_articles limit: 3 %}
    <a class="hp-list__item" href="{{ article.url | relative_url }}">
      <span class="hp-list__date">{{ article.date | date: "%b %Y" }}</span>
      <span class="hp-list__title">{{ article.title }}</span>
      <i class="fas fa-arrow-right" aria-hidden="true"></i>
    </a>
    {%- endfor %}
  </div>
</section>

<section data-reveal class="hp-quote">
  <blockquote>“Jeroen was at the intersection of finance, programming and open source, which is a combination that is very hard to find.”</blockquote>
  <div class="hp-quote__who">
    <img src="/assets/images/testimonials/DidierLopes.jpeg" alt="Didier Lopes" loading="lazy">
    <div><strong>Didier Lopes</strong><span>CEO at OpenBB</span></div>
  </div>
  <a href="/resume" class="hp-link">Read more testimonials <i class="fas fa-arrow-right" aria-hidden="true"></i></a>
</section>

<section data-reveal class="hp-cta">
  <h2 class="hp-h2">Let's talk</h2>
  <p>A question about the projects, an idea for a collaboration or a talk? I'm always happy to hear from you.</p>
  <div class="hp-actions hp-actions--center">
    <a href="/contact" class="hp-btn hp-btn--primary">Get in touch</a>
    <a href="https://www.linkedin.com/in/boumajeroen/" class="hp-btn hp-btn--ghost" target="_blank"><i class="fab fa-linkedin" aria-hidden="true"></i> LinkedIn</a>
  </div>
</section>

</div>

<script>
(function () {
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // fade sections in as they scroll into view
  var sections = document.querySelectorAll('[data-reveal]');
  if (!reduce && 'IntersectionObserver' in window) {
    document.documentElement.classList.add('hp-js');
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -10% 0px' });
    sections.forEach(function (s) { io.observe(s); });
  }

  // count the spotlight numbers up once they are visible
  function countUp(el) {
    var text = el.textContent, target = parseInt(text.replace(/[^0-9]/g, ''), 10);
    if (!target || reduce) return;
    var start = null;
    function step(ts) {
      if (!start) start = ts;
      var p = Math.min((ts - start) / 1400, 1), v = Math.round(target * (1 - Math.pow(1 - p, 3)));
      el.textContent = v.toLocaleString('en-US') + (p === 1 ? '+' : '');
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  var counters = document.querySelectorAll('[data-count]');
  if ('IntersectionObserver' in window) {
    var co = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { countUp(e.target); co.unobserve(e.target); } });
    }, { threshold: 0.6 });
    counters.forEach(function (c) { co.observe(c); });
  }
})();

(function () {
  // Finance Toolkit example tabs: click to switch, rotate on their own until
  // someone picks one
  var box = document.querySelector('[data-tabs]');
  if (!box) return;
  var tabs = [].slice.call(box.querySelectorAll('[data-tab]'));
  function show(key) {
    tabs.forEach(function (t) { var on = t.getAttribute('data-tab') === key; t.classList.toggle('is-active', on); t.setAttribute('aria-selected', on); });
    box.querySelectorAll('[data-panel]').forEach(function (p) { p.hidden = p.getAttribute('data-panel') !== key; });
  }
  var timer = null;
  tabs.forEach(function (t) { t.addEventListener('click', function () { clearInterval(timer); show(t.getAttribute('data-tab')); }); });
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!reduce) {
    var i = 0;
    timer = setInterval(function () { i = (i + 1) % tabs.length; show(tabs[i].getAttribute('data-tab')); }, 6000);
    box.addEventListener('mouseenter', function () { clearInterval(timer); });
  }
})();

(function () {
  // live Finance Toolkit star count, rounded down to the hundred
  var targets = document.querySelectorAll('[data-stars]');
  if (!targets.length || !window.fetch) return;
  var repos = ['JerBouma/FinanceToolkit'];
  Promise.all(repos.map(function (r) {
    return fetch('https://api.github.com/repos/' + r).then(function (x) { return x.json(); }).then(function (d) { return d.stargazers_count || 0; }).catch(function () { return 0; });
  })).then(function (counts) {
    var total = counts.reduce(function (a, b) { return a + b; }, 0);
    if (total < 1000) return;
    var text = (Math.floor(total / 100) * 100).toLocaleString('en-US') + '+';
    targets.forEach(function (el) { el.textContent = text; });
  });
})();
</script>
