---
title: Insights
description: "Insights on financial theory in practice: fundamental analysis, macroeconomics, risk and derivatives, and AI applied to financial data."
permalink: /insights
redirect_from:
  - /articles
  - /articles/
  - /insights/explained
  - /explained
  - /youtube
  - /shorts
layout: single
classes: custom-document projects-v2 articles-v2
author_profile: false
---

I write about the economy, financial markets and how financial theory is applied in practice: macroeconomics, fundamental analysis, risk and derivatives, and how AI assistants can work with financial data. Most articles come with code you can run yourself with the [Finance Toolkit](/projects/financetoolkit). A new part of the economic history series comes out every Sunday; to get every new article in a feed reader, use the [RSS feed](/feed.xml).

{%- assign articles = site.pages | where: "collection", "article" | sort: "date" | reverse %}
{%- assign all_tags = "" | split: "" %}
{%- for art in articles %}{% for tag in art.tags %}{% unless all_tags contains tag %}{% assign all_tags = all_tags | push: tag %}{% endunless %}{% endfor %}{% endfor %}
{%- assign all_tags = all_tags | sort_natural %}
{%- assign latest = articles | first %}

<div class="hp pj ar">

<section class="pj-section ar-first">
  <p class="hp-kicker">Latest</p>
  <a class="ar-feature{% if latest.cover.image %} ar-feature--cover{% endif %}" href="{{ latest.url | relative_url }}" data-reveal>
    {%- if latest.cover.image %}<div class="ar-feature__img">{% include article__thumb.html art=latest sizes="(min-width: 1100px) 560px, 100vw" eager=true %}</div>{% endif %}
    <div class="ar-feature__body">
    <p class="ar-meta">{{ latest.date | date: "%B %-d, %Y" }} · {{ latest.reading_minutes | default: 1 }} min read</p>
    <h2>{{ latest.title }}</h2>
    <p class="ar-feature__text">{{ latest.excerpt | strip_html }}</p>
    <div class="ar-feature__foot">
      <div class="ar-tags">{% for tag in latest.tags %}<span>{{ tag }}</span>{% endfor %}</div>
      <span class="ar-go">Read the article <i class="fas fa-arrow-right" aria-hidden="true"></i></span>
    </div>
    </div>
  </a>
</section>

{%- assign yt = site.data.youtube %}
{%- assign shorts = site.data.youtube_shorts %}
{%- if shorts.size > 0 %}
<section class="hp-section pj-section">
  <p class="hp-kicker">On YouTube</p>
  <h2 class="hp-h2">The news and finance, explained in under a minute</h2>
  <p class="yt-lead">Two series of shorts, News Explained and Finance Explained, with every number calculated by the Finance Toolkit MCP.</p>
  <div class="yt-teaser">
  {%- for s in shorts limit: 4 %}{% assign pl = yt.playlists | where: "key", s.series | first %}
    <a class="yt-teaser__item yt-teaser__item--{{ s.series }}" href="https://www.youtube.com/shorts/{{ s.id }}" target="_blank" rel="noopener">
      <div class="yt-teaser__img"><img src="https://i.ytimg.com/vi/{{ s.id }}/hq720.jpg" alt="" loading="lazy" width="1280" height="720"></div>
      <div class="yt-teaser__body">
        <p class="yt-teaser__series">{{ pl.name }}</p>
        <p class="yt-teaser__title">{{ s.title }}</p>
      </div>
    </a>
  {%- endfor %}
  </div>
  <a class="hp-link" href="{{ yt.channel }}/shorts" target="_blank" rel="noopener">All {{ shorts | size }} shorts on YouTube <i class="fas fa-arrow-right" aria-hidden="true"></i></a>
</section>
{%- endif %}

<section class="hp-section pj-section">
  <p class="hp-kicker">All insights</p>
  <h2 class="hp-h2">Browse by topic</h2>
  <div class="ar-filters" id="article-filters">
    <button class="ar-filter active" data-filter="all">All <span class="lit-count" data-count="all"></span></button>
    {%- for tag in all_tags %}
    <button class="ar-filter" data-filter="{{ tag | slugify }}">{{ tag }} <span class="lit-count" data-count="{{ tag | slugify }}"></span></button>
    {%- endfor %}
  </div>
  <div class="ar-grid" id="article-list">
  {%- for article in articles %}
    {%- assign slugs = "" | split: "" %}{% for tag in article.tags %}{% assign s = tag | slugify %}{% assign slugs = slugs | push: s %}{% endfor %}
    <a href="{{ article.url | relative_url }}" class="ar-card{% if article.cover.image %} ar-card--cover{% endif %}" data-tags="{{ slugs | join: ' ' }}">
      {%- if article.cover.image %}<div class="ar-card__img">{% include article__thumb.html art=article %}</div>{% endif %}
      <p class="ar-meta">{{ article.date | date: "%b %-d, %Y" }} · {{ article.reading_minutes | default: 1 }} min read</p>
      <h3>{{ article.title }}</h3>
      {%- if article.excerpt %}<p class="ar-card__text">{{ article.excerpt | strip_html }}</p>{% endif %}
      <div class="ar-tags">{% for tag in article.tags %}<span>{{ tag }}</span>{% endfor %}</div>
    </a>
  {%- endfor %}
  </div>
  <p class="lit-empty" id="articles-empty" style="display:none">No insights found for this topic.</p>
</section>

<section class="hp-cta" data-reveal>
  <h2 class="hp-h2">Run the analysis yourself</h2>
  <p>Every calculation in these insights is done with the Finance Toolkit, an open-source Python library with 500+ financial methods. You can also ask an AI assistant to run it for you through its MCP server.</p>
  <div class="hp-actions hp-actions--center">
    <a href="/projects/financetoolkit" class="hp-btn hp-btn--primary">Explore the Toolkit <i class="fas fa-arrow-right" aria-hidden="true"></i></a>
    <a href="/projects/financetoolkit/mcp" class="hp-btn hp-btn--ghost">Use it with AI</a>
  </div>
</section>

</div>

<script>
(function () {
  // fade the featured card and call to action in, like on the other pages
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce || !('IntersectionObserver' in window)) return;
  document.documentElement.classList.add('hp-js');
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -8% 0px' });
  document.querySelectorAll('[data-reveal]').forEach(function (s) { io.observe(s); });
})();

(function() {
  var filters = document.querySelectorAll('#article-filters .ar-filter');
  var cards   = document.querySelectorAll('#article-list .ar-card');
  var empty   = document.getElementById('articles-empty');

  function updateCounts() {
    filters.forEach(function(btn) {
      var f = btn.getAttribute('data-filter');
      var countEl = btn.querySelector('.lit-count');
      if (!countEl) return;
      if (f === 'all') {
        countEl.textContent = cards.length;
      } else {
        var n = 0;
        cards.forEach(function(card) {
          var tags = (card.getAttribute('data-tags') || '').split(' ');
          if (tags.indexOf(f) !== -1) n++;
        });
        countEl.textContent = n;
      }
    });
  }

  function applyFilter(filter) {
    var visible = 0;
    cards.forEach(function(card) {
      var tags = (card.getAttribute('data-tags') || '').split(' ');
      var show = filter === 'all' || tags.indexOf(filter) !== -1;
      card.style.display = show ? '' : 'none';
      if (show) visible++;
    });
    empty.style.display = visible === 0 ? '' : 'none';
  }

  function select(btn) {
    filters.forEach(function(b) { b.classList.remove('active'); });
    btn.classList.add('active');
    applyFilter(btn.getAttribute('data-filter'));
  }

  updateCounts();

  filters.forEach(function(btn) {
    btn.addEventListener('click', function() { select(btn); });
  });

  // /insights?tag=history (where /history redirects to) opens with that filter on
  var tag = new URLSearchParams(window.location.search).get('tag');
  var preset = tag && document.querySelector('#article-filters .ar-filter[data-filter="' + tag.toLowerCase().replace(/[^a-z0-9-]/g, '') + '"]');
  if (preset) {
    select(preset);
    var top = document.getElementById('article-filters').closest('section').getBoundingClientRect().top;
    window.scrollTo(0, top + window.pageYOffset - 80);
  }
})();
</script>
