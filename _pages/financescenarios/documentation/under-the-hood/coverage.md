---
title: Coverage
seo_title: "Coverage | Finance Scenarios"
seo_title_suffix: false
excerpt: "What Finance Scenarios can and can't do, and why: every factor, every calibration method, every measure and every known gap, in one place."
description: "What Finance Scenarios covers: every factor, calibration method, real-world and risk-neutral measure and known gap, with where each one lives."
author_profile: false
permalink: /projects/financescenarios/docs/coverage
classes: wide-sidebar
layout: single
docs_module_url: /projects/financescenarios/docs/architecture
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs-architecture"
---

Does Finance Scenarios cover the model, measure or Solvency II output you need, and if not, why not? Pick a topic or search across all of them: each card says in plain words what a feature does or what is still missing. Under **Technical details**, each card also gives where a feature is configured (the [settings profile or the factor set](/projects/financescenarios/docs/configuration#settings-profiles-and-factor-sets)), a minimal example of switching it on, and the precise notes for quants. An example shows only the keys involved: a list you write (under `countries`, or a list of entries) replaces the list in the profile you extend, so repeat the entries you still need.

{% include fs-coverage.html %}

[Configuration](/projects/financescenarios/docs/configuration#real-world-and-risk-neutral-measures) sets out which factors have a risk-neutral form, and each model's page covers its settings.
