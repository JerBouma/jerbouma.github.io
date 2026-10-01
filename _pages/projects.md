---
title: Projects
permalink: /projects
excerpt: I apply much of the finance theory I've learned using Python.
description: I apply much of the finance theory I've learned using Python.
layout: single
classes: custom-document projects-v2
author_profile: false
---
{%- assign d = site.data.projects %}

<div class="row">
<div markdown="1" class="sixty-column mobile-max-column-width" markdown="1">
I discovered Python during my university studies and quickly saw how much it could do in finance. Since then I have spent a lot of my time programming in it, both building internal models at companies like a.s.r. asset management and PGGM and working on the open-source projects on this page.

At financial institutions I kept seeing the same models and calculations being built again and again. That made me a strong advocate for open source, because it means people and firms no longer have to rely only on proprietary models. By sharing my work openly, I want to make financial knowledge and tools available to anyone who wants to use them, and give others something to build on.
</div>
<div class="fourty-column mobile-max-column-width">
<div class="pj-gh">
  <div class="pj-gh__who">
    <img src="https://avatars.githubusercontent.com/u/46355364?v=4" alt="Jeroen Bouma">
    <span><strong>Jeroen Bouma</strong>@JerBouma</span>
  </div>
  <div class="pj-gh__stats">
    <span><strong>{{ d.github.stars }}</strong>stars</span>
    <span><strong>{{ d.github.downloads }}</strong>downloads</span>
    <span><strong>{{ d.github.followers }}</strong>followers</span>
  </div>
  <a href="https://github.com/JerBouma" class="hp-btn hp-btn--ghost" target="_blank" rel="noopener"><i class="fab fa-github" aria-hidden="true"></i> View GitHub profile</a>
</div>
</div>
</div>

<div class="hp pj">

<section class="pj-flow" data-reveal aria-label="How the tools fit together">
  <a class="pj-flow__step" href="/projects/financedatabase">
    <i class="fas fa-database" aria-hidden="true"></i>
    <span class="pj-flow__verb">Find</span>
    <strong>Finance Database</strong>
    <span>Which companies, ETFs and funds exist in a market</span>
  </a>
  <i class="fas fa-arrow-right pj-flow__arrow" aria-hidden="true"></i>
  <a class="pj-flow__step" href="/projects/financetoolkit">
    <i class="fas fa-toolbox" aria-hidden="true"></i>
    <span class="pj-flow__verb">Analyse</span>
    <strong>Finance Toolkit</strong>
    <span>Ratios, models, risk and performance for each of them</span>
  </a>
  <i class="fas fa-arrow-right pj-flow__arrow" aria-hidden="true"></i>
  <a class="pj-flow__step" href="/projects/financetoolkit/mcp">
    <i class="fas fa-robot" aria-hidden="true"></i>
    <span class="pj-flow__verb">Ask</span>
    <strong>Finance Toolkit MCP</strong>
    <span>The same analysis from Claude, ChatGPT or Copilot</span>
  </a>
</section>

<section class="hp-section pj-section">
  <p class="hp-kicker">Maintained</p>
  <h2 class="hp-h2">Open-source tools I build</h2>
  {%- for p in d.maintained %}
  <article class="pj-card" data-reveal>
    <div class="pj-card__top">
      <div class="pj-card__side">
        <a class="pj-card__media" href="{{ p.url }}"><img src="{{ p.image }}" alt="{{ p.name }} banner" loading="lazy"></a>
        <div class="pj-figures">{% for s in p.stats %}<span><i class="fas {{ s.icon }}" aria-hidden="true"></i><strong>{{ s.value }}</strong>{{ s.label }}</span>{% endfor %}</div>
      </div>
      <div class="pj-card__body">
        <p class="pj-card__since">Since {{ p.since }}</p>
        <h3><a href="{{ p.url }}">{{ p.name }}</a></h3>
        <p class="pj-card__lead">{{ p.lead }}</p>
        <div class="pj-card__actions">
          <a class="hp-btn hp-btn--primary" href="{{ p.url }}">Explore <i class="fas fa-arrow-right" aria-hidden="true"></i></a>
          {%- for l in p.links %}
          <a class="hp-link" href="{{ l.url }}">{{ l.label }} <i class="fas fa-arrow-right" aria-hidden="true"></i></a>
          {%- endfor %}
          <a class="hp-link" href="{{ p.github }}" target="_blank" rel="noopener" aria-label="{{ p.name }} on GitHub"><i class="fab fa-github" aria-hidden="true"></i> GitHub</a>
        </div>
      </div>
    </div>
    {%- if p.companion %}{% assign c = p.companion %}
    <div class="pj-card__top pj-companion">
      <a class="pj-card__media" href="{{ c.url }}"><img src="{{ c.image }}" alt="{{ c.name }} banner" loading="lazy"></a>
      <div class="pj-card__body">
        <p class="pj-card__since">Since {{ c.since }}</p>
        <h3><a href="{{ c.url }}">{{ c.name }}</a></h3>
        <p class="pj-card__lead">{{ c.lead }}</p>
        <div class="pj-card__actions">
          <a class="hp-btn hp-btn--primary" href="{{ c.url }}">Explore <i class="fas fa-arrow-right" aria-hidden="true"></i></a>
          {%- for l in c.links %}
          <a class="hp-link" href="{{ l.url }}">{{ l.label }} <i class="fas fa-arrow-right" aria-hidden="true"></i></a>
          {%- endfor %}
        </div>
      </div>
    </div>
    {%- endif %}
  </article>
  {%- endfor %}
</section>

<section class="hp-section pj-section">
  <p class="hp-kicker">Contributed to</p>
  <h2 class="hp-h2">Open source at OpenBB</h2>
  {%- for p in d.contributed %}
  <article class="pj-wide" data-reveal>
    <a class="pj-wide__media" href="{{ p.url }}"><img src="{{ p.image }}" alt="{{ p.name }} banner" loading="lazy"></a>
    <div>
      <p class="pj-card__since">{{ p.years }}</p>
      <h3><a href="{{ p.url }}">{{ p.name }}</a></h3>
      <p class="pj-card__text">{{ p.text }}</p>
      <div class="pj-card__actions">
        <div class="pj-stats">{% for s in p.stats %}<span><i class="fas {{ s.icon }}" aria-hidden="true"></i><strong>{{ s.value }}</strong> {{ s.label }}</span>{% endfor %}</div>
        <a class="hp-link" href="{{ p.url }}">More about OpenBB <i class="fas fa-arrow-right" aria-hidden="true"></i></a>
      </div>
    </div>
  </article>
  {%- endfor %}
</section>

<section class="hp-section pj-section">
  <p class="hp-kicker">Archived</p>
  <h2 class="hp-h2">Earlier projects</h2>
  <p class="pj-note">These still work and are still installed, but I no longer maintain them.</p>
  <div class="pj-archive">
    {%- for p in d.archived %}
    <a class="pj-small" href="{{ p.url }}" data-reveal>
      <span class="pj-small__tag">Archived</span>
      <h3>{{ p.name }}</h3>
      <p>{{ p.text }}</p>
      <div class="pj-stats">{% for s in p.stats %}<span><i class="fas {{ s.icon }}" aria-hidden="true"></i><strong>{{ s.value }}</strong> {{ s.label }}</span>{% endfor %}</div>
    </a>
    {%- endfor %}
  </div>
</section>

<section class="hp-cta" data-reveal>
  <h2 class="hp-h2">Building your own financial models?</h2>
  <p>My guide on Financial Modelling with Python covers the basics, project setup, structure, and how to build and test a model, including common mistakes I've seen in both open-source and proprietary models.</p>
  <div class="hp-actions hp-actions--center">
    <a href="/modelling/introduction" class="hp-btn hp-btn--primary">Read the guide <i class="fas fa-arrow-right" aria-hidden="true"></i></a>
  </div>
</section>

</div>

<script>
(function () {
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!reduce && 'IntersectionObserver' in window) {
    document.documentElement.classList.add('hp-js');
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px' });
    document.querySelectorAll('[data-reveal]').forEach(function (s) { io.observe(s); });
  }
})();
</script>
