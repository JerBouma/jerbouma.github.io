---
layout: splash
title: "Jeroen Bouma"
description: "Jeroen Bouma — Quantitative Investment Strategist and Python developer. Creator of Finance Toolkit and Finance Database, open-source financial analysis libraries with 10,000+ GitHub stars."
excerpt: "Quantitative Investment Strategist and Python developer. Creator of Finance Toolkit and Finance Database."
classes: custom-splash
---

<div class="hero-section">
  <div class="hero-glow blob-1"></div>
  <div class="hero-glow blob-2"></div>
  <div class="hero-inner">
    <div class="hero-text">
      <h1 class="hero-title">Hi there, I'm  <span class="hero-signature">Jeroen Bouma</span></h1>
      <p class="hero-tagline">Quantitative Investment Strategist</p>
      <p class="hero-bio">
        I combine a formal Quantitative Finance background with deep Python expertise across Asset-Liability Management (ALM), Solvency II Legislation, Portfolio Optimization and Artificial Intelligence. My Open-Source projects, including the <a href="/projects/financetoolkit">Finance Toolkit</a> and <a href="/projects/financedatabase">Finance Database</a>, have over 10,000 GitHub Stars combined.
      </p>
    </div>
    <div class="hero-photo">
      <img src="/assets/images/default/bio-photo.jpg" alt="Jeroen Bouma">
    </div>
  </div>
</div>

<div class="stats-band" aria-label="Key statistics">
  <a href="/projects" class="stat-item">
    <span class="stat-number" data-stat="stars" data-target="12000" data-suffix="+">0+</span>
    <span class="stat-label">GitHub Stars</span>
  </a>
  <a href="/projects/financetoolkit" class="stat-item">
    <span class="stat-number" data-stat="ratios" data-target="180" data-suffix="+">0+</span>
    <span class="stat-label">Financial Ratios</span>
  </a>
  <div class="stat-item">
    <span class="stat-number" data-stat="downloads" data-target="50000" data-suffix="+">0+</span>
    <span class="stat-label" style="font-size: 0.60rem;">Downloads per Month</span>
  </div>
</div>

<div class="bento-grid">

  <a href="/resume" class="bento-card">
    <div class="bento-content">
      <i class="fas fa-briefcase bento-icon"></i>
      <h2>Professional Experience</h2>
      <p>A career spanning Quantitative Asset Management, Open Source development, and Finance education.</p>
    </div>
  </a>

  <a href="/projects" class="bento-card">
    <div class="bento-content">
      <i class="fas fa-code-branch bento-icon"></i>
      <h2>Open-Source Projects</h2>
      <p>Python libraries for Financial Datasets and Financial Modelling built for Transparency and Reusability.</p>
    </div>
  </a>

  <a href="/modelling" class="bento-card">
    <div class="bento-content">
      <i class="fas fa-chart-line bento-icon"></i>
      <h2>Financial Modelling</h2>
      <p>In-depth guides on using Python to create Professional Financial Models that last.</p>
    </div>
  </a>

  <a href="/talks" class="bento-card">
    <div class="bento-content">
      <i class="fas fa-microphone bento-icon"></i>
      <h2>Appearances</h2>
      <p>Recorded Talks, Articles, and a curated reading list on Financial Markets and Open Source.</p>
    </div>
  </a>
</div>

<script>
(function () {
  var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* -- Count-up -- */
  function fmt(n, target) {
    return target >= 1000 ? n.toLocaleString('en-US') : String(n);
  }
  function countUp(el) {
    var target = parseInt(el.getAttribute('data-target'), 10);
    var suffix = el.getAttribute('data-suffix') || '';
    if (reduced) { el.textContent = fmt(target, target) + suffix; return; }
    var duration = 1600, start = null;
    function step(ts) {
      if (!start) start = ts;
      var p = Math.min((ts - start) / duration, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = fmt(Math.round(eased * target), target) + (p >= 1 ? suffix : '');
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  var starsEl = document.querySelector('.stat-number[data-stat="stars"]');
  var ratiosEl = document.querySelector('.stat-number[data-stat="ratios"]');
  var dlEl = document.querySelector('.stat-number[data-stat="downloads"]');

  /* -- Live GitHub stars -- */
  var ghRepos = ['JerBouma/FinanceToolkit', 'JerBouma/FinanceDatabase', 'JerBouma/ThePassiveInvestor', 'JerBouma/PersonalFinance'];
  var starsPromise = starsEl ? Promise.all(ghRepos.map(function (repo) {
    return fetch('https://api.github.com/repos/' + repo)
      .then(function (r) { return r.json(); })
      .then(function (d) { return d.stargazers_count || 0; })
      .catch(function () { return 0; });
  })).then(function (counts) {
    var total = counts.reduce(function (a, b) { return a + b; }, 0);
    if (total > 0) starsEl.setAttribute('data-target', Math.floor(total / 100) * 100);
  }).catch(function () {}) : Promise.resolve();

  /* -- Live PyPI monthly downloads disabled — fixed at 50k+ -- */
  var dlPromise = Promise.resolve();

  /* -- Animate after live data resolves (falls back to hardcoded targets on error) -- */
  Promise.all([starsPromise, dlPromise]).then(function () {
    [starsEl, ratiosEl, dlEl].forEach(function (el) { if (el) countUp(el); });
  });

  /* -- Rotating tagline -- */
  var rotating = document.querySelector('.hero-rotating');
  if (!rotating || reduced) return;
  var words = (rotating.getAttribute('data-words') || '').split('|').filter(Boolean);
  if (words.length < 2) return;
  var idx = 0;
  setInterval(function () {
    rotating.style.opacity = '0';
    setTimeout(function () {
      idx = (idx + 1) % words.length;
      rotating.textContent = words[idx];
      rotating.style.opacity = '1';
    }, 300);
  }, 3200);
}());
</script>

<div class="section-divider"></div>

<h2 class="section-title text-center gradient-title">Testimonials</h2>

<div class="testimonial-slider">

  <div class="testimonial-slide">
    <div class="testimonial-content">
      <div class="testimonial-image">
        <a href="/resume"><img src="/assets/images/testimonials/MinhHoang.jpeg" alt="MinhHoang" class="testimoninals"></a>
      </div>
      <div class="testimonial-text">
        <strong>Minh Hoang - Product Manager at OpenBB</strong>
        <em>"I highly recommend Jeroen as an asset in any organization. Jeroen led and executed OpenBB's go-to-market initiatives, including Academia, with exceptional skill. It is not easy to find Jeroen's combination of solid finance knowledge and Programming knowledge."</em>
        <div class="testimonial-action">
          <a href="/resume" class="btn btn--info">Read More</a>
        </div>
      </div>
    </div>
  </div>

  <div class="testimonial-slide">
    <div class="testimonial-content">
      <div class="testimonial-image">
        <a href="/resume"><img src="/assets/images/testimonials/SriChilukuri.jpeg" alt="SriChilukuri" class="testimoninals"></a>
      </div>
      <div class="testimonial-text">
        <strong>Sri Chilukuri - VP of Product Marketing at OpenBB</strong>
        <em>"Jeroen has been a delight to work with. With his expertise in investment research and "can do" attitude, he quickly transformed himself into an excellent product marketing manager at OpenBB. In fact, I would not hesitate to say that he was often the lone sane voice in helping steer the heavily engineering-centric company in the right business direction."</em>
        <div class="testimonial-action">
          <a href="/resume" class="btn btn--info">Read More</a>
        </div>
      </div>
    </div>
  </div>

  <div class="testimonial-slide">
    <div class="testimonial-content">
      <div class="testimonial-image">
        <a href="/resume"><img src="/assets/images/testimonials/LuukvanBenthem.jpeg" alt="LuukvanBenthem" class="testimoninals"></a>
      </div>
      <div class="testimonial-text">
        <strong>Luuk van Benthem - Senior ALM Adviseur at PGGM</strong>
        <em>"Jeroen joined our team just at the right time. As we were considering a full redevelopment of our ALM model, Jeroen's knowledge of Python first greatly helped us in the decision process. In the implementation phase Jeroen played a key role on the development of the technical side of the model. Meanwhile he did a good job at educating our team on these new topics and providing good documentation."</em>
        <div class="testimonial-action">
          <a href="/resume" class="btn btn--info">Read More</a>
        </div>
      </div>
    </div>
  </div>

  <div class="testimonial-slide">
    <div class="testimonial-content">
      <div class="testimonial-image">
        <a href="/resume"><img src="/assets/images/testimonials/PascalJanssen.jpeg" alt="PascalJanssen" class="testimoninals"></a>
      </div>
      <div class="testimonial-text">
        <strong>Pascal Janssen - Strategisch ALM Adviseur at PGGM</strong>
        <em>"(Written in Dutch) Jeroen is zeer bedreven in alle facetten van programmeren in Python. Zijn kennis en ervaring op het gebied van Python hebben een grote meerwaarde geleverd voor mijn afdeling. Jeroen is scherp als het aankomt op het juist implementeren van code in Python. Daarnaast is hij ook bedreven in het draaiend krijgen en houden van Python op werkplekken en de ondersteuning die hierbij nodig is."</em>
        <div class="testimonial-action">
          <a href="/resume" class="btn btn--info">Read More</a>
        </div>
      </div>
    </div>
  </div>

  <div class="testimonial-slide">
    <div class="testimonial-content">
      <div class="testimonial-image">
        <a href="/resume"><img src="/assets/images/testimonials/DidierLopes.jpeg" alt="DidierLopes" class="testimoninals"></a>
      </div>
      <div class="testimonial-text">
        <strong>Didier Lopes - CEO at OpenBB</strong>
        <em>"On the 13th of October 2021, I received an email from Jeroen about adding one of his finance GitHub packages to the OpenBB Terminal. After digging into his open source projects and his achievements I was very impressed. When we had a chat regarding how to work together, I offered him a job on the spot. Jeroen was at the intersection of finance, programming and open source - which is a combination that is very hard to find - even today."</em>
        <div class="testimonial-action">
          <a href="/resume" class="btn btn--info">Read More</a>
        </div>
      </div>
    </div>
  </div>

</div>

<div class="testimonial-controls">
  <button class="testimonial-btn" id="testimonial-prev" aria-label="Previous testimonial"><i class="fas fa-chevron-left"></i></button>
  <div class="testimonial-dots" id="testimonial-dots"></div>
  <button class="testimonial-btn" id="testimonial-next" aria-label="Next testimonial"><i class="fas fa-chevron-right"></i></button>
</div>

<script>
document.addEventListener("DOMContentLoaded", function() {
  const slides = document.querySelectorAll('.testimonial-slide');
  const dotsContainer = document.getElementById('testimonial-dots');
  let currentIndex = 0;
  let timer;

  // Build dots
  slides.forEach((_, i) => {
    const dot = document.createElement('button');
    dot.className = 'testimonial-dot' + (i === 0 ? ' active' : '');
    dot.setAttribute('aria-label', 'Go to testimonial ' + (i + 1));
    dot.addEventListener('click', () => { goTo(i); resetTimer(); });
    dotsContainer.appendChild(dot);
  });

  function goTo(index) {
    currentIndex = index;
    slides.forEach((slide) => {
      slide.style.transform = `translateX(-${currentIndex * 100}%)`;
    });
    document.querySelectorAll('.testimonial-dot').forEach((dot, i) => {
      dot.classList.toggle('active', i === currentIndex);
    });
  }

  function resetTimer() {
    clearInterval(timer);
    timer = setInterval(() => goTo((currentIndex + 1) % slides.length), 10000);
  }

  document.getElementById('testimonial-prev').addEventListener('click', () => {
    goTo((currentIndex - 1 + slides.length) % slides.length);
    resetTimer();
  });

  document.getElementById('testimonial-next').addEventListener('click', () => {
    goTo((currentIndex + 1) % slides.length);
    resetTimer();
  });

  if (slides.length > 1) {
    resetTimer();
  }
});
</script>
