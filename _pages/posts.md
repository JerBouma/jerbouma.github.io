---
title: Articles
permalink: /articles
author_profile: false
classes: wide-sidebar
sidebar:
  nav: "articles"
---

This page includes a selection of articles I have written related to my open-source projects and financial background.

___

{% for post in site.posts %}
  {% include archive-single.html %}
{% endfor %}
