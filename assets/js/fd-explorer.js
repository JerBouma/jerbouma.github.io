/**
 * The Finance Database explorer (/projects/financedatabase/explorer).
 *
 * Loads one asset class at a time from /assets/data/financedatabase/<class>.json
 * (written in the deploy by _scripts/build_fd_explorer.py) and filters it in the
 * browser: a search over symbol, name and ISIN, a dropdown per classification
 * with the number of matches each value would give, and the same selection as
 * Python code. The selection is kept in the address, so it can be shared.
 */
(function () {
  'use strict';

  var root = document.getElementById('fd-explorer');
  if (!root) return;

  var BASE = root.getAttribute('data-src');
  var VERSION = root.getAttribute('data-version');
  var PAGE = 50;

  var CLASSES = {
    equities: { label: 'Equities', py: 'Equities', variable: 'equities',
      filters: ['country', 'sector', 'industry_group', 'industry', 'market_cap', 'market', 'currency'],
      table: ['country', 'sector', 'industry', 'market_cap', 'market'] },
    etfs: { label: 'ETFs', py: 'ETFs', variable: 'etfs',
      filters: ['category_group', 'category', 'family', 'exchange', 'currency'],
      table: ['category', 'family', 'exchange', 'currency'] },
    indices: { label: 'Indices', py: 'Indices', variable: 'indices',
      filters: ['category_group', 'category', 'exchange', 'currency'],
      table: ['category_group', 'category', 'exchange', 'currency'] },
    currencies: { label: 'Currencies', py: 'Currencies', variable: 'currencies',
      filters: ['base_currency', 'quote_currency'],
      table: ['base_currency', 'quote_currency'] },
    cryptos: { label: 'Cryptocurrencies', py: 'Cryptos', variable: 'cryptos',
      filters: ['cryptocurrency', 'currency'],
      table: ['cryptocurrency', 'currency', 'exchange'] }
  };

  // the bars under the filters: per card, the first column of the chain that
  // isn't filtered yet (pick a sector and the card breaks it down by industry group)
  var BREAKDOWN = {
    equities: [['sector', 'industry_group', 'industry'], ['country', 'market'], ['market_cap']],
    etfs: [['category_group', 'category'], ['family'], ['currency', 'exchange']],
    indices: [['category_group', 'category'], ['exchange'], ['currency']],
    currencies: [['base_currency'], ['quote_currency']],
    cryptos: [['currency'], ['exchange']]
  };
  var TOP = 7;

  var LABELS = {
    country: 'Country', sector: 'Sector', industry_group: 'Industry Group', industry: 'Industry',
    market_cap: 'Market Cap', market: 'Market', exchange: 'Exchange', currency: 'Currency',
    category_group: 'Category Group', category: 'Category', family: 'Family',
    base_currency: 'Base Currency', quote_currency: 'Quote Currency', cryptocurrency: 'Cryptocurrency'
  };

  var el = {
    tabs: root.querySelector('.fdx-tabs'),
    query: root.querySelector('.fdx-query'),
    filters: root.querySelector('.fdx-filters'),
    primary: root.querySelector('.fdx-primary'),
    primaryInput: root.querySelector('.fdx-primary input'),
    reset: root.querySelector('.fdx-reset'),
    count: root.querySelector('.fdx-count'),
    tableWrap: root.querySelector('.fdx-table-wrap'),
    table: null,
    insights: root.querySelector('.fdx-insights'),
    more: root.querySelector('.fdx-more'),
    download: root.querySelector('.fdx-download'),
    code: root.querySelector('.fdx-code code'),
    status: root.querySelector('.fdx-status')
  };

  var cache = {};
  var state = { cls: 'equities', q: '', filters: {}, primary: true, shown: PAGE };
  var data = null;   // the loaded asset class
  var matches = [];  // row indices of the current selection

  // ── loading ─────────────────────────────────────────────

  function load(cls) {
    if (cache[cls]) return Promise.resolve(cache[cls]);
    return fetch(BASE + cls + '.json?v=' + VERSION)
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(function (d) {
        var col = {};
        d.columns.forEach(function (c, i) { col[c] = i; });
        d.col = col;
        // lowercase search text per row: symbol, name and ISIN
        d.text = d.rows.map(function (r) {
          return [r[col.symbol], r[col.name], col.isin !== undefined ? r[col.isin] : ''].join('\u0001').toLowerCase();
        });
        d.primaryAt = d.primary ? d.columns.length : -1;
        cache[cls] = d;
        return d;
      });
  }

  function counts() {
    fetch(BASE + 'index.json?v=' + VERSION).then(function (r) { return r.json(); }).then(function (d) {
      Object.keys(d.counts).forEach(function (cls) {
        var b = el.tabs.querySelector('[data-class="' + cls + '"] .fdx-tab__count');
        if (b) b.textContent = d.counts[cls].toLocaleString('en-US');
      });
      var u = root.querySelector('.fdx-updated');
      animateStats(d.stats || {});
      if (u && d.updated) u.textContent = 'Data of ' + new Date(d.updated + 'T00:00:00').toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' }) + '.';
    }).catch(function () {});
  }

  // ── filtering ───────────────────────────────────────────

  function value(row, c) {
    var v = row[data.col[c]];
    return typeof v === 'number' ? (v < 0 ? null : data.values[c][v]) : v;
  }

  // 0 exact symbol, 1 symbol starts with it, 2 name starts with it, 3 a word
  // in the name starts with it, 4 anywhere (also the ISIN); -1 no match
  function rank(i, q) {
    var t = data.text[i];
    var at = t.indexOf(q);
    if (at < 0) return -1;
    var sym = t.slice(0, t.indexOf('\u0001'));
    if (sym === q) return 0;
    if (at === 0) return 1;
    var name = t.slice(sym.length + 1);
    if (name.indexOf(q) === 0) return 2;
    if (new RegExp('[^a-z0-9]' + q.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).test(name)) return 3;
    return 4;
  }

  function passes(row, skip) {
    if (state.primary && data.primaryAt >= 0 && !row[data.primaryAt]) return false;
    for (var c in state.filters) {
      if (c === skip) continue;
      var v = row[data.col[c]];
      if (v !== state.filters[c]) return false;
    }
    return true;
  }

  function select() {
    var q = state.q.trim().toLowerCase();
    var ranked = [];
    for (var i = 0; i < data.rows.length; i++) {
      if (!passes(data.rows[i])) continue;
      if (!q) { ranked.push(i); continue; }
      var r = rank(i, q);
      if (r >= 0) ranked.push(r * 1e7 + i);
    }
    if (q) {
      ranked.sort(function (a, b) { return a - b; });
      ranked = ranked.map(function (x) { return x % 1e7; });
    }
    matches = ranked;
  }

  // per filter: how many rows each value gives with the other filters and the search
  function facetCounts(c) {
    var q = state.q.trim().toLowerCase();
    var n = new Array(data.values[c].length).fill(0);
    var at = data.col[c];
    for (var i = 0; i < data.rows.length; i++) {
      var row = data.rows[i];
      if (row[at] < 0 || !passes(row, c)) continue;
      if (q && data.text[i].indexOf(q) < 0) continue;
      n[row[at]]++;
    }
    return n;
  }

  // ── rendering ───────────────────────────────────────────

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (ch) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[ch]; });
  }

  function renderFilters() {
    var conf = CLASSES[state.cls];
    el.filters.innerHTML = '';
    conf.filters.forEach(function (c) {
      var n = facetCounts(c);
      var label = document.createElement('label');
      label.className = 'fdx-filter' + (state.filters[c] !== undefined ? ' is-set' : '');
      var span = document.createElement('span');
      span.textContent = LABELS[c];
      var sel = document.createElement('select');
      sel.setAttribute('data-filter', c);
      var opts = ['<option value="">All</option>'];
      data.values[c].forEach(function (v, i) {
        if (!n[i] && state.filters[c] !== i) return;
        opts.push('<option value="' + i + '"' + (state.filters[c] === i ? ' selected' : '') + '>' + esc(v) + ' (' + n[i].toLocaleString('en-US') + ')</option>');
      });
      sel.innerHTML = opts.join('');
      label.appendChild(span);
      label.appendChild(sel);
      el.filters.appendChild(label);
    });
    el.primary.hidden = data.primaryAt < 0;
    el.primaryInput.checked = state.primary;
    el.reset.hidden = !state.q && !Object.keys(state.filters).length;
  }

  function renderInsights() {
    var cards = BREAKDOWN[state.cls].map(function (chain) {
      var c = chain.filter(function (x) { return state.filters[x] === undefined; })[0];
      if (!c) return '';
      var at = data.col[c], n = {}, known = 0;
      matches.forEach(function (i) {
        var v = data.rows[i][at];
        if (v < 0) return;
        n[v] = (n[v] || 0) + 1; known++;
      });
      var top = Object.keys(n).sort(function (a, b) { return n[b] - n[a]; });
      if (top.length < 2) return '';
      var shown = top.slice(0, TOP), rest = 0;
      top.slice(TOP).forEach(function (k) { rest += n[k]; });
      var max = n[shown[0]];
      var filterable = CLASSES[state.cls].filters.indexOf(c) >= 0;
      var bars = shown.map(function (k) {
        var pct = (100 * n[k] / known);
        return '<' + (filterable ? 'button type="button" data-col="' + c + '" data-val="' + k + '"' : 'div') + ' class="fdx-bar-row" title="' + esc(data.values[c][k]) + '">' +
          '<span class="fdx-bar-row__label">' + esc(data.values[c][k]) + '</span>' +
          '<span class="fdx-bar-row__track"><span class="fdx-bar-row__fill" style="width:' + (100 * n[k] / max).toFixed(1) + '%"></span></span>' +
          '<span class="fdx-bar-row__n">' + (pct >= 10 ? pct.toFixed(0) : pct.toFixed(1)) + '%</span>' +
          '</' + (filterable ? 'button' : 'div') + '>';
      }).join('');
      var more = rest ? '<p class="fdx-card__more">+ ' + (top.length - TOP).toLocaleString('en-US') + ' more, ' + (100 * rest / known).toFixed(0) + '% of the selection</p>' : '';
      return '<div class="fdx-card"><p class="fdx-card__title">By ' + LABELS[c].toLowerCase() + ' <span>' + top.length.toLocaleString('en-US') + '</span></p>' + bars + more + '</div>';
    }).filter(Boolean);
    el.insights.innerHTML = cards.join('');
    el.insights.hidden = !cards.length;
    el.insights.setAttribute('data-cards', cards.length);
  }

  // the headline numbers count up once, unless the reader prefers less motion
  function animateStats(stats) {
    var still = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    document.querySelectorAll('[data-stat]').forEach(function (node) {
      var target = stats[node.getAttribute('data-stat')];
      if (!target) return;
      if (still) { node.textContent = target.toLocaleString('en-US'); return; }
      var start = performance.now(), ms = 1100;
      (function tick(now) {
        var t = Math.min(1, (now - start) / ms), e = 1 - Math.pow(1 - t, 3);
        node.textContent = Math.round(target * e).toLocaleString('en-US');
        if (t < 1) requestAnimationFrame(tick);
      })(start);
    });
  }

  function renderTable() {
    var conf = CLASSES[state.cls];
    // made here rather than in the page, so the site's table wrapper leaves it alone
    if (!el.table) { el.table = document.createElement('table'); el.table.className = 'fdx-table'; el.tableWrap.appendChild(el.table); }
    var cols = ['symbol', 'name'].concat(conf.table);
    var head = '<thead><tr>' + cols.map(function (c) {
      return '<th scope="col">' + (c === 'symbol' ? 'Symbol' : c === 'name' ? 'Name' : LABELS[c]) + '</th>';
    }).join('') + '</tr></thead>';
    var body = matches.slice(0, state.shown).map(function (i) {
      var row = data.rows[i];
      return '<tr>' + cols.map(function (c) {
        var v = value(row, c);
        if (c === 'symbol') return '<td class="fdx-symbol">' + esc(v) + '</td>';
        return '<td>' + (v ? esc(v) : '<span class="fdx-empty">–</span>') + '</td>';
      }).join('') + '</tr>';
    }).join('');
    el.table.innerHTML = head + '<tbody>' + body + '</tbody>';
    el.count.textContent = matches.length === 1 ? '1 match' : matches.length.toLocaleString('en-US') + ' matches';
    el.more.hidden = matches.length <= state.shown;
    el.more.textContent = 'Show ' + Math.min(PAGE, matches.length - state.shown) + ' more';
    el.download.hidden = !matches.length;
  }

  // the same selection with the financedatabase package
  function renderCode() {
    var conf = CLASSES[state.cls];
    var args = [];
    var q = state.q.trim();
    if (q) args.push('name="' + q.replace(/["\\]/g, '\\$&') + '"');
    conf.filters.forEach(function (c) {
      if (state.filters[c] !== undefined) args.push(c + '="' + data.values[c][state.filters[c]].replace(/["\\]/g, '\\$&') + '"');
    });
    if (state.primary && data.primaryAt >= 0) args.push('only_primary_listing=True');
    var method = q ? 'search' : 'select';
    var span = function (cls, t) { return '<span class="' + cls + '">' + esc(t) + '</span>'; };
    var argHtml = args.map(function (a) {
      var k = a.slice(0, a.indexOf('=')), v = a.slice(a.indexOf('=') + 1);
      return span('n', k) + span('o', '=') + (v === 'True' ? span('bp', v) : span('s2', v));
    }).join(span('p', ',') + ' ');
    el.code.innerHTML =
      span('kn', 'import') + ' ' + span('nn', 'financedatabase') + ' ' + span('k', 'as') + ' ' + span('nn', 'fd') + '\n\n' +
      span('n', conf.variable) + ' ' + span('o', '=') + ' ' + span('n', 'fd') + span('p', '.') + span('nc', conf.py) + span('p', '()') + '\n\n' +
      span('n', conf.variable) + span('p', '.') + span('nf', method) + span('p', '(') + argHtml + span('p', ')');
  }

  function render(filtersToo) {
    select();
    if (filtersToo !== false) renderFilters();
    renderInsights();
    renderTable();
    renderCode();
    writeUrl();
  }

  // ── address ─────────────────────────────────────────────

  function writeUrl() {
    var p = new URLSearchParams();
    if (state.cls !== 'equities') p.set('class', state.cls);
    if (state.q) p.set('q', state.q);
    Object.keys(state.filters).forEach(function (c) { p.set(c, data.values[c][state.filters[c]]); });
    if (!state.primary) p.set('all_listings', '1');
    var s = p.toString();
    history.replaceState(null, '', location.pathname + (s ? '?' + s : '') + location.hash);
  }

  function readUrl() {
    var p = new URLSearchParams(location.search);
    if (CLASSES[p.get('class')]) state.cls = p.get('class');
    state.q = p.get('q') || '';
    state.primary = !p.get('all_listings');
    return p;
  }

  function applyUrlFilters(p) {
    state.filters = {};
    CLASSES[state.cls].filters.forEach(function (c) {
      var v = p.get(c);
      if (v === null) return;
      var i = data.values[c].indexOf(v);
      if (i >= 0) state.filters[c] = i;
    });
  }

  // ── events ──────────────────────────────────────────────

  function open(cls, params) {
    state.cls = cls;
    state.shown = PAGE;
    el.tabs.querySelectorAll('[data-class]').forEach(function (b) {
      b.setAttribute('aria-selected', b.getAttribute('data-class') === cls ? 'true' : 'false');
    });
    root.classList.add('is-loading');
    el.status.textContent = 'Loading ' + CLASSES[cls].label.toLowerCase() + '…';
    el.status.hidden = false;
    load(cls).then(function (d) {
      if (state.cls !== cls) return;
      data = d;
      if (params) applyUrlFilters(params); else state.filters = {};
      root.classList.remove('is-loading');
      el.status.hidden = true;
      render();
    }).catch(function () {
      root.classList.remove('is-loading');
      el.status.textContent = 'The data couldn’t be loaded. Try again later, or use the financedatabase package below.';
    });
  }

  el.tabs.addEventListener('click', function (e) {
    var b = e.target.closest('[data-class]');
    if (b && b.getAttribute('data-class') !== state.cls) open(b.getAttribute('data-class'));
  });

  var timer;
  el.query.addEventListener('input', function () {
    clearTimeout(timer);
    timer = setTimeout(function () {
      state.q = el.query.value;
      state.shown = PAGE;
      if (data) render();
    }, 150);
  });

  el.filters.addEventListener('change', function (e) {
    var c = e.target.getAttribute('data-filter');
    if (!c) return;
    if (e.target.value === '') delete state.filters[c]; else state.filters[c] = +e.target.value;
    state.shown = PAGE;
    render();
  });

  el.primaryInput.addEventListener('change', function () {
    state.primary = el.primaryInput.checked;
    state.shown = PAGE;
    render();
  });

  el.reset.addEventListener('click', function () {
    state.q = '';
    el.query.value = '';
    state.filters = {};
    state.shown = PAGE;
    render();
  });

  el.insights.addEventListener('click', function (e) {
    var b = e.target.closest('[data-col]');
    if (!b) return;
    state.filters[b.getAttribute('data-col')] = +b.getAttribute('data-val');
    state.shown = PAGE;
    render();
  });

  el.more.addEventListener('click', function () {
    state.shown += PAGE;
    renderTable();
  });

  // the Python code of the selection, shown and hidden with its button
  var python = root.querySelector('.fdx-python'), panel = root.querySelector('.fdx-code-panel');
  python.addEventListener('click', function () {
    var show = panel.hidden;
    panel.hidden = !show;
    python.setAttribute('aria-expanded', show ? 'true' : 'false');
    python.classList.toggle('is-on', show);
  });

  el.download.addEventListener('click', function () {
    var cols = data.columns;
    var cell = function (v) { v = v == null ? '' : String(v); return /[",\n]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v; };
    var lines = [cols.join(',')].concat(matches.map(function (i) {
      return cols.map(function (c) { return cell(value(data.rows[i], c)); }).join(',');
    }));
    var a = document.createElement('a');
    a.href = URL.createObjectURL(new Blob([lines.join('\n')], { type: 'text/csv' }));
    a.download = 'financedatabase-' + state.cls + '.csv';
    document.body.appendChild(a);
    a.click();
    setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 0);
  });

  // ── start ───────────────────────────────────────────────

  var params = readUrl();
  el.query.value = state.q;
  counts();
  open(state.cls, params);
})();
