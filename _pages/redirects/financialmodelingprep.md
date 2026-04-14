---
title: FinancialModelingPrep
excerpt: This page redirects to FinancialModelingPrep's subscription page in which you can get an API key at a 15% discount.
description: This page redirects to FinancialModelingPrep's subscription page in which you can get an API key at a 15% discount.
permalink: /fmp
redirect_from:
  - /financialmodelingprep
layout: splash
sitemap: false
author_profile: false
---

<meta http-equiv="Refresh" content="3; url=https://site.financialmodelingprep.com/pricing-plans?couponCode=jeroen"/>

<div class="redirect-page">
  <div class="redirect-page__icon">↗</div>
  <h1 class="redirect-page__title">Redirecting you to FinancialModelingPrep</h1>
  <p class="redirect-page__message">You're being redirected to FinancialModelingPrep's pricing page. This is an affiliate link that gives you a <strong>15% discount</strong> on any plan.</p>
  <div class="redirect-page__countdown">Redirecting in <span id="countdown">3</span>s…</div>
  <a href="https://site.financialmodelingprep.com/pricing-plans?couponCode=jeroen" class="btn btn--warning btn--large">Go now</a>
</div>

<style>
.redirect-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 6rem 2rem 8rem;
  min-height: 60vh;
}

.redirect-page__icon {
  font-size: clamp(4rem, 12vw, 7rem);
  line-height: 1;
  background: linear-gradient(135deg, var(--accent-color), #818cf8);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 1.5rem;
}

.redirect-page__title {
  font-size: clamp(1.4rem, 3.5vw, 2rem);
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 1rem;
}

.redirect-page__message {
  font-size: 1.05rem;
  color: var(--text-muted);
  max-width: 520px;
  margin-bottom: 2rem;
  line-height: 1.7;
}

.redirect-page__countdown {
  font-size: 0.95rem;
  color: var(--text-muted);
  margin-bottom: 2rem;
  font-variant-numeric: tabular-nums;
}
</style>

<script>
(function() {
  var n = 3;
  var el = document.getElementById('countdown');
  var iv = setInterval(function() {
    n--;
    if (el) el.textContent = n;
    if (n <= 0) {
      clearInterval(iv);
      window.location.href = 'https://site.financialmodelingprep.com/pricing-plans?couponCode=jeroen';
    }
  }, 1000);
})();
</script>