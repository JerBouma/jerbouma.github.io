---
title: Financial Modelling with Python
excerpt: "How financial models are built today: what every component of a Python model does, how to work on it with AI coding agents, and a free agent kit that teaches any agent the same practices."
description: "How financial models are built today: what every component of a Python model does, how to work on it with AI coding agents, and a free agent kit for Claude Code, Copilot, Cursor and more."
permalink: /modelling/introduction
classes: wide-sidebar modelling-intro
redirect_from:
  - /modelling
author_profile: false
sidebar:
  nav: "modelling"
---

<p class="mi-lead">AI coding agents now write most of the code in a financial model. What they can't do for you is decide what a good model looks like. This guide is about exactly that: what every part of a model does, why it is there, and how you steer an agent to build it the way you would.</p>

I have spent thousands of hours building financial models in Python, at financial institutions and in open-source projects like the [Finance Toolkit](/projects/financetoolkit). The structure, the conventions and the testing approach in this guide come from that work, including the mistakes I learned the most from. Each chapter explains one component in depth, and how you work on it together with an agent.

## The Journey of a Model

From your first lines of Python to a model that an agent can extend safely, each chapter builds on the previous one. Start at the beginning, or jump to the question you have right now.

<div class="mi-path">
  {%- assign steps = "getting-started|Getting Started|Where do I begin?|Nail down the basics of Python, Pandas and NumPy, and learn when to let an assistant take over.|fa-graduation-cap;setting-up-your-project|Setting up your Project|What does a solid project need?|Dependencies with uv, linters, a Git workflow and the files that keep a model working for years.|fa-folder-open;structure-your-model|Structure your Model|Where does each piece of code go?|The Model-View-Controller pattern for financial models, and why it makes every change easy to review.|fa-sitemap;build-your-model|Build your Model|What does good model code look like?|Naming, type hints and docstrings, and the financial choices to check in every change.|fa-code;test-your-model|Test your Model|How do I know nothing broke?|Recorded tests that flag every changed number, whoever changed it.|fa-vial;working-with-ai|Working with AI|How do I make an agent follow all this?|Instruction files, rules, Skills, hooks and MCP servers, with a ready-made kit.|fa-robot" | split: ";" %}
  {%- for s in steps %}{% assign f = s | split: "|" %}
  <a class="mi-step" href="/modelling/{{ f[0] }}">
    <span class="mi-step__top"><i class="fas {{ f[4] }}" aria-hidden="true"></i><span class="mi-step__num">{{ forloop.index }}</span></span>
    <span class="mi-step__q">{{ f[2] }}</span>
    <strong class="mi-step__title">{{ f[1] }}</strong>
    <span class="mi-step__text">{{ f[3] }}</span>
    <span class="mi-step__more">Read chapter <i class="fas fa-arrow-right" aria-hidden="true"></i></span>
  </a>
  {%- endfor %}
</div>

## The Agent Kit

<div class="mi-kit">
  <div class="mi-kit__text">
    <p class="mi-kit__kicker">Free download</p>
    <h3>Teach any coding agent what this guide teaches you</h3>
    <p>Ready-made instruction files and skills that you copy into your repository. One <code>AGENTS.md</code> holds the rules from this guide (the structure, the conventions, the testing approach and the financial choices an agent should never make silently), and every tool's own file points to it. That way Claude Code, GitHub Copilot, Cursor, Codex, Gemini CLI and other agents all follow the same instructions.</p>
    <div class="mi-kit__actions">
      <a class="btn btn--info" href="/assets/files/financial-modelling-agent-kit.zip" download><i class="fas fa-download" aria-hidden="true"></i> Download the kit (.zip)</a>
      <a class="mi-kit__browse" href="https://github.com/JerBouma/jerbouma.github.io/tree/main/agent-kit" target="_blank" rel="noopener"><i class="fab fa-github" aria-hidden="true"></i> Browse the files</a>
    </div>
  </div>
  <ul class="mi-kit__files">
    <li><span class="mi-kit__name"><code>AGENTS.md</code></span><span>All instructions; read by Codex, Cursor, Copilot and most agents</span></li>
    <li><span class="mi-kit__name"><code>CLAUDE.md</code><code>GEMINI.md</code></span><span>Point Claude Code and Gemini CLI to the same instructions</span></li>
    <li><span class="mi-kit__name"><code>.github/</code></span><span>Copilot instructions, plus a rule for model files</span></li>
    <li><span class="mi-kit__name"><code>.cursor/rules/</code></span><span>Cursor rules, always on and for model files</span></li>
    <li><span class="mi-kit__name"><code>.claude/skills/</code></span><span>Four skills: add a metric, write tests, review a change, set up a project</span></li>
    <li><span class="mi-kit__name"><code>.claude/settings.json</code></span><span>A hook that formats and lints every edit</span></li>
  </ul>
</div>
