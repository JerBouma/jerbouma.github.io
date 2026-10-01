---
title: Appearances
description: My public talks and appearances connecting finance theory with open-source Python.
permalink: /appearances
redirect_from:
  - /media
  - /activities
  - /talks
  - /videos
layout: single
classes: custom-document projects-v2 appearances-v2
author_profile: false
---

{%- assign d = site.data.appearances %}

I enjoy talking about how financial theory is put into practice, and about the role Python and open source play in that. Below are my public talks, lectures and webinars, from university campuses to product launches. **Would you like me to speak at your event? Reach out via the [contact page](/contact).**

<div class="hp pj ap">

<section class="hp-section pj-section">
  <p class="hp-kicker">In person</p>
  <h2 class="hp-h2">Talks and lectures</h2>
  {%- for a in d.talks %}{% include appearance-card.html item=a %}{% endfor %}
</section>

<section class="hp-section pj-section">
  <p class="hp-kicker">Online</p>
  <h2 class="hp-h2">Webinars and launches</h2>
  {%- for a in d.webinars %}{% include appearance-card.html item=a %}{% endfor %}
</section>

<section class="hp-cta" data-reveal>
  <h2 class="hp-h2">Looking for a speaker?</h2>
  <p>I'm happy to talk about quantitative finance, Python in the financial industry or open-source tools for financial analysis, at universities, societies and events.</p>
  <div class="hp-actions hp-actions--center">
    <a href="/contact" class="hp-btn hp-btn--primary">Get in touch <i class="fas fa-arrow-right" aria-hidden="true"></i></a>
  </div>
</section>

</div>

<script>
document.addEventListener('DOMContentLoaded', function () {
  // fade the cards in as they scroll into view, like on the other pages
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!reduce && 'IntersectionObserver' in window) {
    document.documentElement.classList.add('hp-js');
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px' });
    document.querySelectorAll('[data-reveal]').forEach(function (s) { io.observe(s); });
  }

  // YouTube lazy-embed: load thumbnail and swap for iframe on click
  document.querySelectorAll('.embed-youtube').forEach(function (container) {
    var img = new Image();
    img.src = 'https://img.youtube.com/vi/' + container.dataset.videoId + '/sddefault.jpg';
    img.addEventListener('load', function () { container.appendChild(img); });

    function play() {
      var iframe = document.createElement('iframe');
      iframe.setAttribute('frameborder', '0');
      iframe.setAttribute('allowfullscreen', '');
      iframe.setAttribute('allow', 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture');
      iframe.setAttribute('src', 'https://www.youtube.com/embed/' + container.dataset.videoId + '?rel=0&showinfo=0&autoplay=1');
      container.innerHTML = '';
      container.appendChild(iframe);
    }
    container.addEventListener('click', play);
    container.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); play(); } });
  });
});
</script>