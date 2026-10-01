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

How models are built has changed. AI coding assistants such as Claude Code, GitHub Copilot, Cursor and Codex now write most of the code, and I don't think anyone should build a financial model by hand anymore. What has not changed is what makes a model good: a structure that holds up, calculations you can verify and tests that tell you when something breaks. Your role moves from typing code to designing the model, directing the assistant and judging the result. That requires a deeper understanding of each component, not a shallower one.

That is what this guide is about. Every page explains what a part of a financial model does and why it is there, and how you work on it together with an assistant: what to ask for, what to write down so the assistant gets it right, and what to check before you accept the result. It is not a recipe to follow by hand, but the knowledge you need to steer an assistant towards a model you can trust. The practices I describe are the ones that worked for me, including the mistakes I learned the most from.

Whether you want to understand the code of a financial model in depth or mainly want to work well with AI assistants, the two go hand in hand: the better you understand the components, the better you can instruct and check the assistant. The last page, Working with AI, covers the files and tools that connect both. **You can browse the content using the sidebar or the cards below.**

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

  <a href="/modelling/working-with-ai" class="bento-card" style="grid-column: span 12;">
    <div class="bento-content">
      <i class="fas fa-robot bento-icon"></i>
      <h2>Working with AI</h2>
      <p>Setting up your project for AI coding assistants: instruction files like CLAUDE.md and AGENTS.md, rules, Skills, hooks and MCP servers, and a workflow that keeps every result verifiable.</p>
    </div>
  </a>

</div>

Have suggestions? This entire website is open-source, so feel free to contribute [here](https://github.com/JerBouma/jerbouma.github.io){: target="_blank"}!