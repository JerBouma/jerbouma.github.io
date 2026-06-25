(function () {
  'use strict';

  function track(event, props) {
    if (typeof plausible === 'function') {
      plausible(event, props ? { props: props } : undefined);
    }
  }

  function getPage() {
    return window.location.pathname;
  }

  function getLinkLocation(el) {
    if (el.closest('.author__urls-wrapper')) return 'sidebar';
    if (el.closest('.site-footer, footer[role="contentinfo"]')) return 'footer';
    if (el.closest('.contact-channels')) return 'contact-card';
    if (el.closest('.bento-card')) return 'bento-card';
    if (el.closest('.page-header-action')) return 'page-header';
    if (el.closest('.github-profile-card')) return 'github-card';
    if (el.closest('.stats-band')) return 'stats-band';
    if (el.closest('.testimonial-content')) return 'testimonial';
    if (el.closest('.btn')) return 'cta-button';
    return 'content';
  }

  document.addEventListener('click', function (e) {
    // Code copy button
    if (e.target.closest('.copy-code-button')) {
      var container = e.target.closest('div.highlighter-rouge');
      var langEl = container && container.querySelector('.code-lang');
      track('Code Copy', {
        language: langEl ? langEl.textContent.trim() : 'unknown',
        page: getPage()
      });
      return;
    }

    var el = e.target.closest('a[href]');
    if (!el) return;

    var href = el.getAttribute('href') || '';
    var fullHref = el.href || '';
    var page = getPage();
    var loc = getLinkLocation(el);

    // Email links
    if (href.startsWith('mailto:')) {
      track('Email Click', { page: page, location: loc });
      return;
    }

    // Internal FMP referral paths (/fmp, /financialmodelingprep)
    if (href === '/fmp' || href === '/financialmodelingprep' ||
        href.startsWith('/fmp/') || href.startsWith('/financialmodelingprep/')) {
      track('FMP Outbound', { page: page, location: loc });
      return;
    }

    // Only proceed for external http(s) links
    var isExternal = false;
    try {
      var url = new URL(fullHref, window.location.href);
      isExternal = url.hostname !== window.location.hostname && url.protocol.startsWith('http');
    } catch (e) {}
    if (!isExternal) return;

    // GitHub links
    if (fullHref.includes('github.com')) {
      var repoMatch = fullHref.match(/github\.com\/JerBouma\/([^/?#]+)/i);
      var props = { page: page, location: loc };
      props.type = fullHref.includes('/sponsors/') ? 'sponsors' : repoMatch ? 'repo' : 'other';
      if (repoMatch) props.repo = repoMatch[1];
      track('GitHub Outbound', props);
      return;
    }

    // FinancialModelingPrep links
    if (fullHref.includes('financialmodelingprep.com') || fullHref.includes('jeroenbouma.com/fmp')) {
      track('FMP Outbound', { page: page, location: loc });
      return;
    }

    // All other external links
    var domain = '';
    try { domain = new URL(fullHref).hostname.replace(/^www\./, ''); } catch (e) {}
    track('Other Outbound', { page: page, location: loc, domain: domain });
  });

})();
