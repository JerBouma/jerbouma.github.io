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

    // FMP affiliate link — highest-value conversion
    if (
      href === '/fmp' || href === '/financialmodelingprep' ||
      fullHref.includes('jeroenbouma.com/fmp') ||
      fullHref.includes('financialmodelingprep.com/pricing-plans')
    ) {
      track('FMP Affiliate Click', { page: page, location: loc });
      return;
    }

    // GitHub Sponsors
    if (fullHref.includes('github.com/sponsors/JerBouma')) {
      track('GitHub Sponsor Click', { page: page, location: loc });
      return;
    }

    // Buy Me A Coffee
    if (fullHref.includes('buymeacoffee.com')) {
      track('Buy Me Coffee Click', { page: page, location: loc });
      return;
    }

    // GitHub repo or profile links
    if (fullHref.includes('github.com/JerBouma')) {
      var repoMatch = fullHref.match(/github\.com\/JerBouma\/([^/?#]+)/i);
      if (repoMatch) {
        track('GitHub Repo Click', { repo: repoMatch[1], page: page, location: loc });
      } else {
        track('GitHub Profile Click', { page: page, location: loc });
      }
      return;
    }

    // LinkedIn
    if (fullHref.includes('linkedin.com')) {
      track('LinkedIn Click', { page: page, location: loc });
      return;
    }

    // Email
    if (href.startsWith('mailto:')) {
      track('Email Click', { page: page, location: loc });
      return;
    }

    // PyPI
    if (fullHref.includes('pypi.org/project/')) {
      var pkgMatch = fullHref.match(/pypi\.org\/project\/([\w-]+)/);
      track('PyPI Click', {
        package: pkgMatch ? pkgMatch[1] : 'unknown',
        page: page,
        location: loc
      });
      return;
    }

    // PePy download stats
    if (fullHref.includes('pepy.tech')) {
      track('PePy Stats Click', { page: page });
      return;
    }

    // MCP server URL copy / any click on code containing the MCP server URL
    if (fullHref.includes('financetoolkit.jeroenbouma.com')) {
      track('MCP Server Link Click', { page: page, location: loc });
      return;
    }

    // Amazon book links (literature page)
    if (fullHref.includes('amazon.com')) {
      track('Literature Outbound Click', { source: 'amazon', page: page });
      return;
    }

    // Academic papers (SSRN, journals, JSTOR, NBER)
    if (
      fullHref.includes('ssrn.com') ||
      fullHref.includes('jstor.org') ||
      fullHref.includes('nber.org') ||
      fullHref.includes('papers.ssrn')
    ) {
      track('Literature Outbound Click', { source: 'academic', page: page });
      return;
    }

    // LinkedIn activity/post links (appearances page)
    if (fullHref.includes('linkedin.com/feed/update')) {
      track('Appearance LinkedIn Click', { page: page });
      return;
    }

  });

})();
