---
title: Resume
excerpt: "Quantitative Investment Strategist with a background in quantitative finance, years of Python work and a number of open-source projects."
description: "Quantitative Investment Strategist with a background in quantitative finance, years of Python work and a number of open-source projects."
permalink: /resume
redirect_from:
  - /cv
layout: single
classes: custom-document
author_profile: false
---

<div class="row">
<div markdown="1" class="seventy-column">

{% for paragraph in site.data.resume.intro %}{{ paragraph }}

{% endfor %}
<div class="resume-facts">
<div class="resume-facts__row"><span class="resume-facts__label">Expertise</span><span class="resume-facts__items resume-facts__text">{% for g in site.data.resume.expertise %}<span class="expertise-key expertise-{{ g.key }}">{{ g.group }}</span>{% endfor %}</span></div>
<div class="resume-facts__row"><span class="resume-facts__label">Languages</span><span class="resume-facts__items resume-facts__text">{% for l in site.data.resume.languages %}{{ l.name }}{% unless forloop.last %}, {% endunless %}{% endfor %} (professional)</span></div>
</div>

<p class="resume-download"><a href="/assets/files/jeroen-bouma-cv.pdf" class="btn btn--info" download="Jeroen Bouma - CV.pdf"><i class="fas fa-file-pdf" aria-hidden="true"></i> Download CV (PDF)</a></p>

</div>

<div markdown="1" class="thirty-column">

<img src="/assets/images/default/bio-photo.jpg" alt="Portrait photo of Jeroen Bouma" class='testimoninals'>

</div>
</div>

{% include resume-timeline.html %}
