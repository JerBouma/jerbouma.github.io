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

Python has become the language of choice for many financial analysts and quantitative researchers. It is readable, has an extensive set of libraries and is used across the industry. I have spent thousands of hours with it, both for my own projects and for models at financial institutions.

Today, AI assistants such as ChatGPT, Claude and GitHub Copilot can write a large part of that code for you. That changes how models are built, but not what makes a model good. A model still needs a structure that holds up, calculations you can verify and tests that tell you when something breaks. If anything, understanding these components has become more important: when an assistant drafts a model in seconds, you are the one who has to judge whether it is correct, whether it fits the rest of the model and whether it will still work next year.

That is the focus of this guide. It is not a recipe that you should follow by hand step by step, but an explanation of what each part of a financial model does and why it is there, from the project setup to the structure, the code and the tests. Whether you type the code yourself or let an assistant draft it, knowing these components is what lets you steer, review and maintain the result. The practices I describe are the ones that worked for me, including the mistakes I learned the most from. **You can browse the content using the sidebar or the cards below.**

<div class="bento-grid bento-grid--compact">

  <a href="/modelling/getting-started" class="bento-card">
    <div class="bento-content">
      <i class="fas fa-graduation-cap bento-icon"></i>
      <h2>Getting Started with Python</h2>
      <p>Where to begin if you are new to Python: the basics, Jupyter Notebooks and your first project, and how to use AI assistants as a tutor rather than a shortcut.</p>
    </div>
  </a>

  <a href="/modelling/setting-up-your-project" class="bento-card">
    <div class="bento-content">
      <i class="fas fa-folder-open bento-icon"></i>
      <h2>Setting up your Project</h2>
      <p>What each part of a project is for: directory structure, dependency management with uv, linters, a Git workflow, and the instructions that help an AI assistant follow your conventions.</p>
    </div>
  </a>

  <a href="/modelling/structure-your-model" class="bento-card">
    <div class="bento-content">
      <i class="fas fa-sitemap bento-icon"></i>
      <h2>Structure your Model</h2>
      <p>How to apply the Model-View-Controller (MVC) pattern to financial models, what the data, visualization and control layers do, and why that separation makes code easier to review, also when an assistant wrote it.</p>
    </div>
  </a>

  <a href="/modelling/build-your-model" class="bento-card" style="grid-column: span 6;">
    <div class="bento-content">
      <i class="fas fa-code bento-icon"></i>
      <h2>Build your Model</h2>
      <p>Writing clean and consistent Python: PEP 8 styling, naming conventions, type hints and docstrings, and what to check before you accept code that an AI assistant wrote.</p>
    </div>
  </a>

  <a href="/modelling/test-your-model" class="bento-card" style="grid-column: span 6;">
    <div class="bento-content">
      <i class="fas fa-vial bento-icon"></i>
      <h2>Test your Model</h2>
      <p>Using Pytest to build a test suite that mirrors your model, with recorded expected outputs that catch every change in a calculation, whether you or an assistant made it.</p>
    </div>
  </a>

</div>

Have suggestions? This entire website is open-source, so feel free to contribute [here](https://github.com/JerBouma/jerbouma.github.io){: target="_blank"}!