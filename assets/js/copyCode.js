/**
 * copyCode.js
 *
 * Auto-injects a macOS-style code header (with traffic-light dots and a copy
 * button) into every .highlighter-rouge and .language-python block that does
 * NOT already have a manually-inserted .code-header immediately before it.
 *
 * Also keeps compatibility with explicitly placed {% include code_header.html %}
 * siblings by wiring up any pre-existing .copy-code-button elements.
 */
(function () {
  'use strict';

  // ── Helpers ──────────────────────────────────────────────────────────────

  function getCodeText(container) {
    // Prefer the innerText of the <code> element inside pre.highlight
    const codeEl =
      container.querySelector('pre.highlight code') ||
      container.querySelector('pre code') ||
      container.querySelector('code');
    return codeEl ? codeEl.innerText : container.innerText;
  }

  function animateCopyButton(btn) {
    btn.classList.remove('fa-copy');
    btn.classList.add('fa-check');
    setTimeout(() => {
      btn.classList.remove('fa-check');
      btn.classList.add('fa-copy');
    }, 2000);
  }

  function wireCopyButton(btn, getText) {
    btn.addEventListener('click', () => {
      const text = typeof getText === 'function' ? getText() : getText;
      window.navigator.clipboard.writeText(text).catch(() => {
        // Fallback for older browsers / insecure contexts
        const ta = document.createElement('textarea');
        ta.value = text;
        ta.style.position = 'fixed';
        ta.style.opacity = '0';
        document.body.appendChild(ta);
        ta.select();
        document.execCommand('copy');
        document.body.removeChild(ta);
      });
      animateCopyButton(btn);
    });
  }

  function createHeader() {
    const header = document.createElement('div');
    header.className = 'code-header';

    const btn = document.createElement('button');
    btn.className = 'copy-code-button fas fa-copy';
    btn.setAttribute('aria-label', 'Copy code to clipboard');

    header.appendChild(btn);
    return { header, btn };
  }

  // ── Main injection logic ─────────────────────────────────────────────────

  function injectHeaders() {
    const containers = document.querySelectorAll(
      'div.highlighter-rouge, div.language-python'
    );

    containers.forEach((container) => {
      // Skip if a manual code-header already sits immediately before this
      // container in the DOM (legacy {% include code_header.html %} pattern)
      const prev = container.previousElementSibling;
      if (prev && prev.classList.contains('code-header')) {
        return; // handled below in legacy wiring
      }

      // Skip if we already injected a header into this container
      if (container.querySelector(':scope > .code-header')) {
        return;
      }

      const { header, btn } = createHeader();

      // Prepend the header as first child so it sits inside the container
      container.insertBefore(header, container.firstChild);

      wireCopyButton(btn, () => getCodeText(container));
    });
  }

  // ── Legacy: wire any manually-placed .copy-code-button siblings ──────────

  function wireLegacyButtons() {
    // These are buttons inside a .code-header that was placed *before* a
    // code container via {% include code_header.html %}
    document.querySelectorAll('.code-header > .copy-code-button').forEach((btn) => {
      // Find the associated code block (next sibling that contains a pre)
      const header = btn.closest('.code-header');
      if (!header) return;

      // Look for the code content in the following sibling container
      let sibling = header.nextElementSibling;
      while (sibling) {
        const codeEl =
          sibling.querySelector('pre.highlight code') ||
          sibling.querySelector('pre code') ||
          sibling.querySelector('code');
        if (codeEl) {
          wireCopyButton(btn, () => codeEl.innerText);
          break;
        }
        sibling = sibling.nextElementSibling;
      }
    });
  }

  // ── Init ─────────────────────────────────────────────────────────────────

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      injectHeaders();
      wireLegacyButtons();
    });
  } else {
    injectHeaders();
    wireLegacyButtons();
  }
})();