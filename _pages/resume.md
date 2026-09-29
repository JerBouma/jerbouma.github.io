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
<p class="resume-download"><a href="/assets/files/jeroen-bouma-cv.pdf" class="btn btn--outline" download="Jeroen Bouma - CV.pdf"><i class="fas fa-file-pdf" aria-hidden="true"></i> Download CV (PDF)</a></p>

</div>

<div markdown="1" class="thirty-column">

<img src="/assets/images/default/bio-photo.jpg" alt="Portrait photo of Jeroen Bouma" class='testimoninals'>

</div>
</div>

{% include resume-timeline.html %}
