---
title: Articles
permalink: /articles
redirect_from: 
  - /categories
author_profile: false
classes: wide-sidebar
sidebar:
  nav: "articles"
---

This page includes a selection of articles I have written related to my open-source projects and financial background. It is meant to explain financial theory and how this theory can be directly applied in a variety of my open-source projects. For example, the first article I have written is related to the Binomial Trees in which I explain the theory and how the methods can be used within the [Finance Toolkit](/projects/financetoolkit){:target="_blank"} project. 

___

{% for post in site.posts %}
  {% include archive-single.html %}
{% endfor %}
