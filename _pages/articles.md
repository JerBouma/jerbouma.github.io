---
title: Articles
permalink: /articles
redirect_from:
  - /categories
author_profile: false
excerpt: "This page features a selection of articles I've written about my open-source projects and financial background. These articles explain financial theory and demonstrate its direct application within several of my open-source projects."
classes: wide-sidebar
sidebar:
  nav: "articles"
---

This page presents a selection of articles I have written connecting my open-source projects with my financial background. The goal is to explain financial theory and demonstrate its practical application within these projects. For example, one article focuses on Binomial Trees, detailing the theory and its implementation within the [Finance Toolkit](/projects/financetoolkit){:target="_blank"} project.

___

{% for post in site.posts %}
  {% include archive-single.html %}
{% endfor %}

