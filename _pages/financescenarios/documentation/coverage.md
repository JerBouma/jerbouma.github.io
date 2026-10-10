---
title: Coverage
seo_title: Coverage – Finance Scenarios
excerpt: "What Finance Scenarios can and can't do, and why: every factor, every calibration method, every measure and every known gap, in one place."
description: "What Finance Scenarios covers: every factor, calibration method, real-world and risk-neutral measure and known gap, with where each one lives."
author_profile: false
permalink: /projects/financescenarios/docs/coverage
classes: wide-sidebar
layout: single
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

What Finance Scenarios can and can't do, and why. Pick a topic to see its features or search across all of them. Each card says in plain words what a feature does or what is still missing. **Technical details** shows where it lives in the configuration and code, with the precise notes for quants.

When a run uses something that has a known, more capable alternative that isn't available yet, `Scenarios.calibrate(config)` says so in a notice (at INFO level, so `set_log_level("INFO")` shows it).

{% include fs-coverage.html %}

## References

`KnwSvQ` has the full Q-measure math for `knw`/`knw_sv`; [configuration](/projects/financescenarios/docs/configuration#real-world-and-risk-neutral-measures)'s Real-world and risk-neutral measures section has the risk-neutral scope of every factor that accepts `measure: "risk_neutral"` (interest_rates, inflation, equities, fx and commodities). Each factor's own class docstring (`help(InterestRates)`, `help(Equities)`, ...) is the most detailed source for that specific factor, including its Scope notes.
