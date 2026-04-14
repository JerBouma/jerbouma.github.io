---
title: Articles
description: A selection of articles connecting open-source projects with financial theory.
permalink: /articles
layout: single
classes: custom-document
author_profile: false
---

A selection of articles I have written connecting my open-source projects with my financial background. The goal is to explain financial theory and demonstrate its practical application within these projects.

{% assign articles = site.pages | where: "collection", "article" | sort: "date" | reverse %}

{% comment %}Build sorted unique tag list{% endcomment %}
{% assign all_tags = "" | split: "" %}
{% for art in articles %}
  {% for tag in art.tags %}
    {% unless all_tags contains tag %}
      {% assign all_tags = all_tags | push: tag %}
    {% endunless %}
  {% endfor %}
{% endfor %}
{% assign all_tags = all_tags | sort_natural %}

{% if articles.size == 0 %}
<p class="lit-empty">No articles yet — check back soon.</p>
{% else %}
<div class="lit-filters" id="article-filters">
  <button class="lit-filter active" data-filter="all">All <span class="lit-count" data-count="all"></span></button>
  {% for tag in all_tags %}
  <button class="lit-filter" data-filter="{{ tag | slugify }}">{{ tag }} <span class="lit-count" data-count="{{ tag | slugify }}"></span></button>
  {% endfor %}
</div>

<div class="article-list" id="article-list">
{% for article in articles %}
  {% assign art_tag_slugs = "" %}
  {% for tag in article.tags %}
    {% assign slug = tag | slugify %}
    {% if art_tag_slugs == "" %}
      {% assign art_tag_slugs = slug %}
    {% else %}
      {% assign art_tag_slugs = art_tag_slugs | append: " " | append: slug %}
    {% endif %}
  {% endfor %}
  <a href="{{ article.url | relative_url }}" class="article-card" data-tags="{{ art_tag_slugs }}">
    <div class="article-card__meta">
      <span class="article-card__date">{{ article.date | date: "%b %-d, %Y" }}</span>
      {% if article.tags.size > 0 %}
      <div class="article-card__tags">
        {% for tag in article.tags %}<span class="lit-tag">{{ tag }}</span>{% endfor %}
      </div>
      {% endif %}
    </div>
    <h2 class="article-card__title">{{ article.title }}</h2>
    {% if article.excerpt %}<p class="article-card__excerpt">{{ article.excerpt | strip_html }}</p>{% endif %}
  </a>
{% endfor %}
</div>

<p class="lit-empty" id="articles-empty" style="display:none">No articles found for this tag.</p>

<script>
(function() {
  var filters = document.querySelectorAll('#article-filters .lit-filter');
  var cards   = document.querySelectorAll('#article-list .article-card');
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

  updateCounts();

  filters.forEach(function(btn) {
    btn.addEventListener('click', function() {
      filters.forEach(function(b) { b.classList.remove('active'); });
      btn.classList.add('active');
      applyFilter(btn.getAttribute('data-filter'));
    });
  });
})();
</script>
{% endif %}
