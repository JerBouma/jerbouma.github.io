---
title: History Explained
description: "One event from economic history every Sunday: what happened, the mechanism behind it and the numbers, charted with the Finance Toolkit."
excerpt: "One event from economic history every Sunday, with the numbers behind it."
permalink: /history
layout: single
classes: custom-document projects-v2 articles-v2
author_profile: false
---

Every Sunday I pick one event from economic history, from the Black Death to the oil shocks and the euro's launch, and look at what the data says happened. Each article comes with a short on YouTube, and every chart has the Finance Toolkit code and the MCP question behind it, so you can check the numbers yourself.

{%- assign articles = site.pages | where: "series", "history" | sort: "date" | reverse %}
{%- assign latest = articles | first %}

<div class="hp pj ar">

{%- if latest %}
{%- assign latest_words = latest.content | number_of_words %}
<section class="pj-section ar-first">
  <p class="hp-kicker">This week</p>
  <a class="ar-feature" href="{{ latest.url | relative_url }}" data-reveal>
    <p class="ar-meta">{{ latest.date | date: "%B %-d, %Y" }} · {{ latest_words | divided_by: 220 | at_least: 1 }} min read</p>
    <h2>{{ latest.title }}</h2>
    <p class="ar-feature__text">{{ latest.excerpt | strip_html }}</p>
    <div class="ar-feature__foot">
      <div class="ar-tags">{% for tag in latest.tags %}<span>{{ tag }}</span>{% endfor %}</div>
      <span class="ar-go">Read the article <i class="fas fa-arrow-right" aria-hidden="true"></i></span>
    </div>
  </a>
</section>
{%- endif %}

{%- if articles.size > 1 %}
<section class="hp-section pj-section">
  <p class="hp-kicker">Earlier weeks</p>
  <h2 class="hp-h2">The series so far</h2>
  <div class="ar-grid">
  {%- for article in articles offset: 1 %}
    {%- assign words = article.content | number_of_words %}
    <a href="{{ article.url | relative_url }}" class="ar-card">
      <p class="ar-meta">{{ article.date | date: "%b %-d, %Y" }} · {{ words | divided_by: 220 | at_least: 1 }} min read</p>
      <h3>{{ article.title }}</h3>
      {%- if article.excerpt %}<p class="ar-card__text">{{ article.excerpt | strip_html }}</p>{% endif %}
      <div class="ar-tags">{% for tag in article.tags %}<span>{{ tag }}</span>{% endfor %}</div>
    </a>
  {%- endfor %}
  </div>
</section>
{%- endif %}

<section class="hp-section pj-section">
  <a class="hp-link" href="{{ '/insights' | relative_url }}">All insights <i class="fas fa-arrow-right" aria-hidden="true"></i></a>
</section>

</div>
