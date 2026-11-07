---
title: Explained
seo_title: "Explained | Insights"
description: "Short videos that explain the financial news and financial concepts with real data from the Finance Toolkit MCP: prices, financial statements, valuation, risk and more."
permalink: /insights/explained
redirect_from:
  - /explained
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

<section class="hp-section pj-section" id="shorts">
  <p class="hp-kicker">Watch</p>
  <h2 class="hp-h2">The shorts</h2>
  <div class="ar-filters yt-filters" id="yt-filters">
    <button class="ar-filter active" data-series="all">All <span class="lit-count">{{ shorts | size }}</span></button>
    {%- for pl in yt.playlists %}
    <button class="ar-filter" data-series="{{ pl.key }}">{{ pl.name }} <span class="lit-count">{{ shorts | where: "series", pl.key | size }}</span></button>
    {%- endfor %}
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

  function show(series) {
    var shown = 0;
    cards.forEach(function (card) {
      var ok = series === 'all' || card.dataset.series === series;
      card.hidden = !ok;
      if (ok) shown++;
    });
    document.getElementById('yt-empty').hidden = shown > 0;
    seriesBtns.forEach(function (b) { b.classList.toggle('active', b.dataset.series === series); });
  }

  seriesBtns.forEach(function (b) { b.addEventListener('click', function () { show(b.dataset.series); }); });
  document.querySelectorAll('.yt-series__show').forEach(function (b) {
    b.addEventListener('click', function () {
      show(b.dataset.series);
      document.getElementById('shorts').scrollIntoView({ behavior: reduce ? 'auto' : 'smooth' });
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
