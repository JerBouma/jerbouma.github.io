---
title: YouTube Shorts
seo_title: "YouTube Shorts | Insights"
description: "Short videos that explain the financial news and financial concepts with real data from the Finance Toolkit MCP: prices, financial statements, valuation, risk and more."
permalink: /insights/youtube
redirect_from:
  - /youtube
  - /shorts
layout: single
classes: custom-document projects-v2 articles-v2 youtube-v2
author_profile: false
---

{%- assign yt = site.data.youtube %}
{%- assign shorts = site.data.youtube_shorts %}
{%- assign used = "" | split: "" %}
{%- for s in shorts %}{% for k in s.concepts %}{% unless used contains k %}{% assign used = used | push: k %}{% endunless %}{% endfor %}{% endfor %}

On my [YouTube channel](https://www.youtube.com/channel/UCgcSx8WAvm9uLF3xu2b6crA) I explain the financial news and the concepts behind it in under a minute. Every number in these shorts comes from the [Finance Toolkit MCP server](/projects/financetoolkit/mcp), the same server any AI assistant can connect to, so each short doubles as an example of a question you can ask your own assistant. The description of each short says which data was used and where the news came from.

<div class="hp pj yt">

<section class="pj-section yt-first">
  <p class="hp-kicker">Two series</p>
  <h2 class="hp-h2">News Explained and Finance Explained</h2>
  <div class="yt-stats">
    <div><strong>{{ shorts | size }}</strong><span>shorts so far</span></div>
    {%- for pl in yt.playlists %}{% assign n = shorts | where: "series", pl.key | size %}
    <div class="yt-stats--{{ pl.key }}"><strong>{{ n }}</strong><span>{{ pl.name }}</span></div>
    {%- endfor %}
    <div><strong>{{ used | size }}</strong><span>Finance Toolkit MCP concepts used</span></div>
  </div>
  <div class="yt-series">
    {%- for pl in yt.playlists %}{% assign n = shorts | where: "series", pl.key | size %}
    <div class="yt-series__card yt-series__card--{{ pl.key }}">
      <p class="yt-series__icon"><i class="fas fa-{{ pl.icon }}" aria-hidden="true"></i></p>
      <h3>{{ pl.name }}</h3>
      <p class="yt-series__tagline">{{ pl.tagline }}</p>
      <p class="yt-series__text">{{ pl.text }}</p>
      <div class="yt-series__foot">
        <button class="hp-link yt-series__show" type="button" data-series="{{ pl.key }}">Show the {{ n }} shorts <i class="fas fa-arrow-right" aria-hidden="true"></i></button>
        <a class="hp-link" href="https://www.youtube.com/playlist?list={{ pl.id }}" target="_blank" rel="noopener">Playlist on YouTube <i class="fas fa-arrow-up-right-from-square" aria-hidden="true"></i></a>
      </div>
    </div>
    {%- endfor %}
  </div>
</section>

<section class="hp-section pj-section">
  <p class="hp-kicker">What the MCP calculated</p>
  <h2 class="hp-h2">Every short, mapped to the Finance Toolkit MCP</h2>
  <p class="yt-lead">Each row is a short and each column a concept from the Finance Toolkit MCP, with the tool an AI assistant calls for it. The bars show how often a concept is used. Choose a column to see only the shorts that use it.</p>
  <div class="yt-map-wrap">
  <div class="yt-map" id="yt-map" style="--yt-cols: {{ yt.concepts | size }}">
    <div class="yt-map__corner">
      <span class="yt-dot yt-dot--news"></span> News Explained<br>
      <span class="yt-dot yt-dot--finance"></span> Finance Explained
    </div>
    {%- assign most = 1 %}
    {%- for c in yt.concepts %}{% assign n = 0 %}{% for s in shorts %}{% if s.concepts contains c.key %}{% assign n = n | plus: 1 %}{% endif %}{% endfor %}{% if n > most %}{% assign most = n %}{% endif %}{% endfor %}
    {%- for c in yt.concepts %}
    {%- assign n = 0 %}{% for s in shorts %}{% if s.concepts contains c.key %}{% assign n = n | plus: 1 %}{% endif %}{% endfor %}
    <button class="yt-map__col" type="button" data-concept="{{ c.key }}" title="{{ c.label }}: {{ n }} shorts, the {{ c.tool }} tool"{% if n == 0 %} disabled{% endif %}>
      <span class="yt-map__bar"><span style="height: {{ n | times: 100 | divided_by: most }}%"></span></span>
      <span class="yt-map__n">{{ n }}</span>
      <i class="fas fa-{{ c.icon }}" aria-hidden="true"></i>
      <span class="yt-map__label">{{ c.label }}</span>
      <code>{{ c.tool }}</code>
    </button>
    {%- endfor %}
    {%- for s in shorts %}
    <a class="yt-map__row{% if forloop.index > 12 %} yt-map__row--more{% endif %}" href="#short-{{ s.id }}" data-short="{{ s.id }}">
      <span class="yt-dot yt-dot--{{ s.series }}"></span>
      <span class="yt-map__title">{{ s.title }}</span>
      <span class="yt-map__date">{{ s.published | date: "%b %-d" }}</span>
    </a>
    {%- for c in yt.concepts %}
    <span class="yt-map__cell{% if forloop.parentloop.index > 12 %} yt-map__row--more{% endif %}" data-concept="{{ c.key }}">{% if s.concepts contains c.key %}<span class="yt-dot yt-dot--{{ s.series }}" title="{{ c.label }}"></span>{% endif %}</span>
    {%- endfor %}
    {%- endfor %}
  </div>
  </div>
  {%- if shorts.size > 12 %}
  <button class="hp-link yt-map__more" type="button" id="yt-map-more">Show all {{ shorts | size }} shorts <i class="fas fa-chevron-down" aria-hidden="true"></i></button>
  {%- endif %}
</section>

<section class="hp-section pj-section" id="shorts">
  <p class="hp-kicker">Watch</p>
  <h2 class="hp-h2">The shorts</h2>
  <div class="ar-filters yt-filters" id="yt-filters">
    <button class="ar-filter active" data-series="all">All <span class="lit-count">{{ shorts | size }}</span></button>
    {%- for pl in yt.playlists %}
    <button class="ar-filter" data-series="{{ pl.key }}">{{ pl.name }} <span class="lit-count">{{ shorts | where: "series", pl.key | size }}</span></button>
    {%- endfor %}
    <button class="ar-filter yt-filters__concept" id="yt-concept" type="button" hidden></button>
  </div>
  <div class="yt-grid" id="yt-grid">
    {%- for s in shorts %}{% include short-card.html short=s %}{% endfor %}
  </div>
  <p class="lit-empty" id="yt-empty" hidden>No shorts in this selection yet.</p>
</section>

<section class="hp-cta" data-reveal>
  <h2 class="hp-h2">Ask your own AI the same questions</h2>
  <p>Connect the Finance Toolkit MCP server to Claude, ChatGPT or another AI assistant, and it can calculate every number in these shorts for any company, fund or country.</p>
  <div class="hp-actions hp-actions--center">
    <a href="/projects/financetoolkit/mcp" class="hp-btn hp-btn--primary">Set up the MCP server <i class="fas fa-arrow-right" aria-hidden="true"></i></a>
    <a href="{{ yt.channel }}" class="hp-btn hp-btn--ghost" target="_blank" rel="noopener"><i class="fab fa-youtube" aria-hidden="true"></i> Watch on YouTube</a>
  </div>
</section>

</div>

<script>
document.addEventListener('DOMContentLoaded', function () {
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!reduce && 'IntersectionObserver' in window) {
    document.documentElement.classList.add('hp-js');
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px' });
    document.querySelectorAll('[data-reveal]').forEach(function (s) { io.observe(s); });
  }

  var cards = document.querySelectorAll('#yt-grid .yt-card');
  var seriesBtns = document.querySelectorAll('#yt-filters [data-series]');
  var conceptBtn = document.getElementById('yt-concept');
  var cols = document.querySelectorAll('#yt-map .yt-map__col');
  var state = { series: 'all', concept: null };

  function apply() {
    var shown = 0;
    cards.forEach(function (card) {
      var ok = (state.series === 'all' || card.dataset.series === state.series) &&
               (!state.concept || (' ' + card.dataset.concepts + ' ').indexOf(' ' + state.concept + ' ') !== -1);
      card.hidden = !ok;
      if (ok) shown++;
    });
    document.getElementById('yt-empty').hidden = shown > 0;
    seriesBtns.forEach(function (b) { b.classList.toggle('active', b.dataset.series === state.series); });
    cols.forEach(function (c) { c.classList.toggle('active', c.dataset.concept === state.concept); });
    document.getElementById('yt-map').classList.toggle('has-concept', !!state.concept);
    document.querySelectorAll('#yt-map .yt-map__cell').forEach(function (c) { c.classList.toggle('active', c.dataset.concept === state.concept); });
    if (state.concept) {
      var col = document.querySelector('#yt-map .yt-map__col[data-concept="' + state.concept + '"]');
      conceptBtn.innerHTML = col.querySelector('.yt-map__label').textContent + ' <span aria-hidden="true">×</span>';
      conceptBtn.setAttribute('aria-label', 'Show all concepts again');
      conceptBtn.hidden = false;
    } else {
      conceptBtn.hidden = true;
    }
  }

  function showShorts() { document.getElementById('shorts').scrollIntoView({ behavior: reduce ? 'auto' : 'smooth' }); }

  seriesBtns.forEach(function (b) { b.addEventListener('click', function () { state.series = b.dataset.series; apply(); }); });
  conceptBtn.addEventListener('click', function () { state.concept = null; apply(); });
  cols.forEach(function (c) {
    c.addEventListener('click', function () {
      state.concept = state.concept === c.dataset.concept ? null : c.dataset.concept;
      apply();
      if (state.concept) showShorts();
    });
  });
  document.querySelectorAll('.yt-series__show').forEach(function (b) {
    b.addEventListener('click', function () { state.series = b.dataset.series; state.concept = null; apply(); showShorts(); });
  });

  var more = document.getElementById('yt-map-more');
  if (more) more.addEventListener('click', function () {
    document.getElementById('yt-map').classList.add('show-all');
    more.remove();
  });

  // a row in the map opens its short: show it (whatever the filter) and highlight it
  document.querySelectorAll('#yt-map .yt-map__row').forEach(function (row) {
    row.addEventListener('click', function (e) {
      var card = document.getElementById('short-' + row.dataset.short);
      if (!card) return;
      e.preventDefault();
      if (card.hidden) { state = { series: 'all', concept: null }; apply(); }
      card.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'center' });
      card.classList.remove('is-picked'); void card.offsetWidth; card.classList.add('is-picked');
    });
  });

  // play a short in place; the player only loads from YouTube on click
  document.querySelectorAll('.yt-card__media').forEach(function (media) {
    function play() {
      var iframe = document.createElement('iframe');
      iframe.setAttribute('allowfullscreen', '');
      iframe.setAttribute('title', media.getAttribute('aria-label').replace(/^Play /, ''));
      iframe.setAttribute('allow', 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture');
      iframe.setAttribute('src', 'https://www.youtube-nocookie.com/embed/' + media.dataset.videoId + '?autoplay=1&rel=0&playsinline=1');
      media.innerHTML = '';
      media.appendChild(iframe);
      media.removeAttribute('role'); media.removeAttribute('tabindex');
    }
    media.addEventListener('click', play, { once: true });
    media.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); play(); } });
  });
});
</script>
