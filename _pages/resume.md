---
title: Resume
excerpt: "Quantitative Investment Strategist who analyzes financial information and turns it into investment conclusions, backed by deep expertise in Python and AI."
description: "Quantitative Investment Strategist who analyzes financial information and turns it into investment conclusions, backed by deep expertise in Python and AI."
permalink: /resume
redirect_from:
  - /cv
layout: single
classes: custom-document resume-v2
author_profile: false
---
{%- assign r = site.data.resume %}

<div class="row">
<div markdown="1" class="seventy-column">

{% for paragraph in r.intro %}{{ paragraph }}

{% endfor %}
<div class="resume-facts">
<div class="resume-facts__row"><span class="resume-facts__label">Expertise</span><span class="resume-facts__items resume-facts__text">{% for g in r.expertise %}<span class="expertise-key expertise-{{ g.key }}">{{ g.group }}</span>{% endfor %}</span></div>
<div class="resume-facts__row"><span class="resume-facts__label">Languages</span><span class="resume-facts__items resume-facts__text">{% for l in r.languages %}{{ l.name }}{% unless forloop.last %}, {% endunless %}{% endfor %} (professional)</span></div>
</div>

<p class="resume-download"><a href="/assets/files/jeroen-bouma-cv.pdf" class="btn btn--info" download="Jeroen Bouma - CV.pdf"><i class="fas fa-file-pdf" aria-hidden="true"></i> Download CV (PDF)</a></p>

</div>

<div markdown="1" class="thirty-column">

<img src="/assets/images/default/bio-photo.jpg" alt="Portrait photo of Jeroen Bouma" class='testimoninals'>

</div>
</div>

<div class="hp rj">

<nav class="rj-map" aria-label="Chapters">
  {%- for ch in r.chapters %}
  <a class="rj-map__step{% if forloop.first %} is-now{% endif %}" href="#{{ ch.id }}">
    <span class="rj-map__dot" aria-hidden="true"></span>
    <span class="rj-map__years">{{ ch.years }}</span>
    <span class="rj-map__name">{{ ch.short }}</span>
  </a>
  {%- endfor %}
</nav>

{% include resume-journey.html %}

<section class="hp-section rj-expertise" data-reveal>
  <p class="hp-kicker">Expertise</p>
  <h2 class="hp-h2">What I work on</h2>
  <div class="rj-expertise__grid">
    {%- for g in r.expertise %}
    <div class="rj-expertise__group rj-expertise__group--{{ g.key }}">
      <h3>{{ g.group }}</h3>
      <div class="rj-tags">{% for x in g.items %}<span class="rj-tag rj-tag--{{ g.key }}">{{ x }}</span>{% endfor %}</div>
    </div>
    {%- endfor %}
  </div>
  <p class="rj-languages"><i class="fas fa-language" aria-hidden="true"></i> {% for l in r.languages %}{{ l.name }}{% unless forloop.last %} and {% endunless %}{% endfor %}, both at a professional level</p>
</section>

<section class="hp-section rj-beyond" data-reveal>
  <p class="hp-kicker">Beyond work</p>
  <h2 class="hp-h2">Hobbies</h2>
  <div class="rj-beyond__grid">
    {%- for h in r.hobbies %}
    <div class="rj-hobby">
      <i class="fas {% case h.label %}{% when 'Tinkering' %}fa-microchip{% when 'Food & Wine' %}fa-champagne-glasses{% else %}fa-person-running{% endcase %}" aria-hidden="true"></i>
      <h3>{{ h.label }}</h3>
      <p>{{ h.text }}</p>
    </div>
    {%- endfor %}
  </div>
</section>

<section class="hp-cta" data-reveal>
  <h2 class="hp-h2">The short version</h2>
  <p>Everything above on two pages, ready to print or forward.</p>
  <div class="hp-actions hp-actions--center">
    <a href="/assets/files/jeroen-bouma-cv.pdf" class="hp-btn hp-btn--primary" download="Jeroen Bouma - CV.pdf"><i class="fas fa-file-pdf" aria-hidden="true"></i> Download CV (PDF)</a>
    <a href="https://www.linkedin.com/in/boumajeroen/" class="hp-btn hp-btn--ghost" target="_blank" rel="noopener"><i class="fab fa-linkedin" aria-hidden="true"></i> LinkedIn</a>
  </div>
</section>

</div>

<script>
(function () {
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // fade sections in as they scroll into view
  if (!reduce && 'IntersectionObserver' in window) {
    document.documentElement.classList.add('hp-js');
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px' });
    document.querySelectorAll('[data-reveal]').forEach(function (s) { io.observe(s); });
  }

  // the rail fills as you travel down the journey, and the map marks the
  // chapter you are in
  var journey = document.getElementById('journey');
  var fill = journey && journey.querySelector('.rj-rail__fill');
  var steps = document.querySelectorAll('.rj-map__step');
  var chapters = journey ? journey.querySelectorAll('.rj-chapter') : [];
  var ticking = false;
  function update() {
    ticking = false;
    var box = journey.getBoundingClientRect(), mid = window.innerHeight * 0.55;
    var p = Math.min(Math.max((mid - box.top) / box.height, 0), 1);
    if (fill) fill.style.transform = 'scaleY(' + (reduce ? 1 : p) + ')';
    var current = -1;
    chapters.forEach(function (c, i) { if (c.getBoundingClientRect().top < mid) current = i; });
    steps.forEach(function (s, i) { s.classList.toggle('is-current', i === current); });
  }
  if (journey) {
    window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
    window.addEventListener('resize', update);
    update();
  }
})();
</script>
