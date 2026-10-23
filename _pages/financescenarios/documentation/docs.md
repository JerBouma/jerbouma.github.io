---
title: Documentation
seo_title: "Finance Scenarios Documentation"
seo_title_suffix: false
excerpt: "Finance Scenarios is an open-source economic scenario generator: thousands of joint scenarios for interest rates, inflation, equities, currencies, credit and more, linked the way they have been historically."
description: "Finance Scenarios documentation: what the economic scenario generator models, a first run from choosing settings to reading the distribution, how factors are linked, and real-world vs risk-neutral runs."
author_profile: false
permalink: /projects/financescenarios/docs
classes: wide-sidebar
layout: single
redirect_from:
    - /projects/financescenarios/getting-started
    - /projects/financescenarios/docs/reference
    - /projects/financescenarios/docs/reference/scenarios
    - /projects/financescenarios/docs/reference/scenario-set
sitemap: false
noindex: true
search: false
sidebar:
    nav: "financescenarios-docs"
---

{% include financescenarios-docs/scenarios-intro.md %}

To install Finance Scenarios it simply requires the following:

```bash
pip install financescenarios -U
```

{% include financescenarios-getting-started/getting-started.md %}

{% include financescenarios-docs/scenarios-how-it-works.md %}

{% include financescenarios-reference/docs.md %}
