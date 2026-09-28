---
title: Financial Modelling with Python
excerpt: "What I learned building financial models in Python at financial institutions: how to set them up, avoid the usual pitfalls and keep them maintainable."
description: "What I learned building financial models in Python at financial institutions: how to set them up, avoid the usual pitfalls and keep them maintainable."
author_profile: true
permalink: /modelling/introduction
classes: wide-sidebar
redirect_from:
  - /modelling
author_profile: false
sidebar:
  nav: "modelling"
---

Python has found its way into the financial industry in recent years. It is simple, readable and has an extensive set of libraries, which is why many financial analysts and quantitative researchers now prefer it. I have spent thousands of hours using Python, both for my own projects and for institutional applications.

Along the way I learned how to design sophisticated financial models and algorithms, with a structure that holds up, does its job and stays easy to maintain. Maintaining models, making sure they handle new data correctly and adapting them when the situation changes are exactly the areas where I made mistakes and learned the most. On these pages I share that knowledge and experience, so that you can hopefully avoid the same pitfalls.

This guide covers getting started with Python, setting up a project, and structuring, building, and testing a model. The practices I describe are the ones that worked for me across the different roles I have had. **You can browse the content using the sidebar or the cards below.**

<div class="bento-grid bento-grid--compact">

  <a href="/modelling/getting-started" class="bento-card">
    <div class="bento-content">
      <i class="fas fa-graduation-cap bento-icon"></i>
      <h2>Getting Started with Python</h2>
      <p>Where to begin if you are new to Python: the basics, setting up Jupyter Notebooks, and working toward your first project, with practical tips on coding tools, Git, and building financial models from scratch.</p>
    </div>
  </a>

  <a href="/modelling/setting-up-your-project" class="bento-card">
    <div class="bento-content">
      <i class="fas fa-folder-open bento-icon"></i>
      <h2>Setting up your Project</h2>
      <p>The basics of setting up a project: directory structure, dependency management with uv, Git workflows, linters, and the configuration files that keep your model maintainable for years.</p>
    </div>
  </a>

  <a href="/modelling/structure-your-model" class="bento-card">
    <div class="bento-content">
      <i class="fas fa-sitemap bento-icon"></i>
      <h2>Structure your Model</h2>
      <p>How to apply the Model-View-Controller (MVC) pattern to financial models, what the data, visualization, and control layers do, and why keeping them separate matters for maintainable code.</p>
    </div>
  </a>

  <a href="/modelling/build-your-model" class="bento-card" style="grid-column: span 6;">
    <div class="bento-content">
      <i class="fas fa-code bento-icon"></i>
      <h2>Build your Model</h2>
      <p>Writing clean and consistent Python: PEP 8 styling, naming conventions, docstrings, type annotations, and the coding patterns that make a model easy to read and work on together.</p>
    </div>
  </a>

  <a href="/modelling/test-your-model" class="bento-card" style="grid-column: span 6;">
    <div class="bento-content">
      <i class="fas fa-vial bento-icon"></i>
      <h2>Test your Model</h2>
      <p>Using Pytest to build a test suite that mirrors the structure of your model, with expected outputs recorded to CSV so that regressions are detected automatically whenever the underlying calculations change.</p>
    </div>
  </a>

</div>

Have suggestions? This entire website is open-source, so feel free to contribute [here](https://github.com/JerBouma/jerbouma.github.io){: target="_blank"}!