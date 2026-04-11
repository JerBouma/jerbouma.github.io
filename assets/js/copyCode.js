/**
 * copyCode.js
 *
 * Auto-injects a macOS-style code header (traffic-light dots, language label,
 * and a Copy button) into every fenced code block.
 */
(function () {
  'use strict';

  const LANG_LABELS = {
    python: 'Python', bash: 'Bash', sh: 'Shell', shell: 'Shell',
    javascript: 'JavaScript', js: 'JavaScript', typescript: 'TypeScript',
    ts: 'TypeScript', json: 'JSON', yaml: 'YAML', yml: 'YAML',
    html: 'HTML', css: 'CSS', scss: 'SCSS', ruby: 'Ruby',
    text: 'Text', plaintext: 'Text', sql: 'SQL', r: 'R',
    java: 'Java', cpp: 'C++', c: 'C', go: 'Go', rust: 'Rust',
    kotlin: 'Kotlin', swift: 'Swift', php: 'PHP',
  };

  function getLang(container) {
    for (const cls of container.classList) {
      const m = cls.match(/^language-(.+)$/);
      if (m && m[1] !== 'plaintext') {
        const key = m[1].toLowerCase();
        return LANG_LABELS[key] || m[1].charAt(0).toUpperCase() + m[1].slice(1);
      }
    }
    return null;
  }

  function getCodeText(container) {
    const el =
      container.querySelector('pre.highlight code') ||
      container.querySelector('pre code') ||
      container.querySelector('code');
    return el ? el.innerText : container.innerText;
  }

  function wireCopyButton(btn, getText) {
    btn.addEventListener('click', () => {
      const text = typeof getText === 'function' ? getText() : getText;
      window.navigator.clipboard.writeText(text).catch(() => {
        const ta = document.createElement('textarea');
        ta.value = text;
        ta.style.cssText = 'position:fixed;opacity:0';
        document.body.appendChild(ta);
        ta.select();
        document.execCommand('copy');
        document.body.removeChild(ta);
      });
      btn.innerHTML = '<i class="fas fa-check"></i><span>Copied!</span>';
      btn.classList.add('copied');
      setTimeout(() => {
        btn.innerHTML = '<i class="fas fa-copy"></i><span>Copy</span>';
        btn.classList.remove('copied');
      }, 2000);
    });
  }

  function createHeader(lang) {
    const header = document.createElement('div');
    header.className = 'code-header';

    // Language label (left side)
    if (lang) {
      const label = document.createElement('span');
      label.className = 'code-lang';
      label.textContent = lang;
      header.appendChild(label);
    }

    // Copy button (right side)
    const btn = document.createElement('button');
    btn.className = 'copy-code-button';
    btn.setAttribute('aria-label', 'Copy code to clipboard');
    btn.innerHTML = '<i class="fas fa-copy"></i><span>Copy</span>';

    header.appendChild(btn);
    return { header, btn };
  }

  function injectHeaders() {
    document.querySelectorAll('div.highlighter-rouge').forEach((container) => {
      if (container.querySelector(':scope > .code-header')) return;

      const lang = getLang(container);
      const { header, btn } = createHeader(lang);
      container.insertBefore(header, container.firstChild);
      wireCopyButton(btn, () => getCodeText(container));
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', injectHeaders);
  } else {
    injectHeaders();
  }
})();
