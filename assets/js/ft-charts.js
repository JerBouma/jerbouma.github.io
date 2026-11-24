/*
 * Interactive charts on /projects/financetoolkit and the articles.
 *
 * Every <div class="ft-chart" data-chart="…"> is filled from
 * /assets/data/financetoolkit-charts.json (written by
 * _scripts/financetoolkit_charts.py), or from the file in its data-src
 * attribute (the articles use /assets/data/article-charts.json), and drawn
 * with ECharts, which is served from this site (assets/js/lib) so no
 * third-party CDN or content blocker can hold it up. ECharts and the data
 * start loading as soon as the page opens; each chart is drawn once it
 * scrolls into view. Charts follow the site's light/dark theme and resize
 * with the page.
 */
(function () {
  // Every chart gets ECharts' accessibility description (aria-label on the chart: its
  // type, series and values), so screen readers get more than an unlabelled canvas.
  function initChart(canvas) {
    var inst = window.echarts.init(canvas, null, { renderer: 'canvas' });
    var setOption = inst.setOption.bind(inst);
    inst.setOption = function (option, a, b) {
      if (option && typeof option === 'object' && !option.aria) option.aria = { enabled: true };
      // printing: draw the final state at once, there is no time for an animation
      if (option && typeof option === 'object' && window.__ftPrinting) option.animation = false;
      return setOption(option, a, b);
    };
    return inst;
  }

  // The Python and MCP buttons in an article chart's top right (_includes/ft-chart.html
  // with code= or mcp=) dim the chart and lay the code or the question over it, one at a
  // time; the same button, Escape or a click on the dimmed chart closes it
  // (the Notes button is added once the chart is drawn, so clicks are handled on the box)
  Array.prototype.forEach.call(document.querySelectorAll('.ft-chart-box'), function (box) {
    function show(button) {
      Array.prototype.forEach.call(box.querySelectorAll('.ft-chart-action[data-panel]'), function (b) {
        var on = b === button;
        b.setAttribute('aria-expanded', on ? 'true' : 'false');
        b.classList.toggle('is-on', on);
        box.querySelector('.ft-chart-panel[data-panel="' + b.getAttribute('data-panel') + '"]').hidden = !on;
      });
      box.classList.toggle('is-open', !!button);
      toggle.classList.toggle('is-on', !!button);
    }
    var actions = box.querySelector('.ft-chart-actions');
    // when the buttons don't leave the title enough room they fold into one menu button
    var toggle = document.createElement('button');
    toggle.type = 'button';
    toggle.className = 'ft-chart-actions__toggle';
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-label', 'Python, MCP, notes and data');
    toggle.title = 'Python, MCP, notes and data';
    // drawn inline, so it shows even before (or without) the icon font
    toggle.innerHTML = '<svg viewBox="0 0 16 16" width="16" height="16" aria-hidden="true" focusable="false">' +
      '<path d="M2.5 4h11M2.5 8h11M2.5 12h11" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" fill="none"/></svg>';
    actions.insertBefore(toggle, actions.firstChild);
    function menu(open) {
      actions.classList.toggle('is-menu', open);
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    }
    toggle.addEventListener('click', function () { menu(!actions.classList.contains('is-menu')); });
    document.addEventListener('click', function (e) {
      if (actions.classList.contains('is-menu') && !actions.contains(e.target)) menu(false);
    });
    box.ftFit = function () {
      var head = box.querySelector('.ft-chart__title');
      actions.classList.remove('is-collapsed');
      var full = actions.offsetWidth;
      // the title keeps at least 300px next to the buttons, or the buttons fold away; only the
      // title shares a row with them, so the subtitle and tabs below use the full width
      var collapse = box.clientWidth - full - 32 < 300;
      actions.classList.toggle('is-collapsed', collapse);
      if (!collapse) menu(false);
      if (head) head.style.paddingRight = (actions.offsetWidth + 16) + 'px';
    };
    // refit when the box resizes and when the buttons themselves change width (fonts loading,
    // the Notes and Data buttons arriving)
    if (window.ResizeObserver) {
      var ro = new ResizeObserver(function () { if (!actions.classList.contains('is-menu')) box.ftFit(); });
      ro.observe(box);
      ro.observe(actions);
    }
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { box.ftFit(); });
    box.ftFit();
    box.addEventListener('click', function (e) {
      if (e.target.closest('.ft-chart-action')) menu(false);
      var button = e.target.closest('.ft-chart-action[data-panel]');
      if (button) return show(button.getAttribute('aria-expanded') === 'true' ? null : button);
      if (!box.classList.contains('is-open') || e.target.closest('.ft-chart-action')) return;
      var panel = e.target.closest('.ft-chart-panel');
      if (!panel || e.target === panel) show(null);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && box.classList.contains('is-open')) show(null);
    });
    // the MCP card's Copy button copies the question
    var copy = box.querySelector('.ft-chart-panel__copy');
    if (copy) copy.addEventListener('click', function () {
      var q = box.querySelector('.ft-chart-panel__question').textContent.trim();
      var label = copy.querySelector('span');
      (navigator.clipboard ? navigator.clipboard.writeText(q) : Promise.reject()).then(function () {
        label.textContent = 'Copied';
        setTimeout(function () { label.textContent = 'Copy'; }, 1600);
      }, function () {});
    });
  });

  var boxes = Array.prototype.slice.call(document.querySelectorAll('.ft-chart[data-chart]'));
  if (!boxes.length) return;

  var ECHARTS = '/assets/js/lib/echarts-5.5.1-site.min.js';
  var DATA = '/assets/data/financetoolkit-charts.json';
  var PALETTE = ['#38bdf8', '#818cf8', '#f97316', '#34d399', '#f472b6', '#fbbf24', '#a78bfa'];
  var instances = [];

  var loading = null;
  function loadScript(src) {
    return loading = loading || new Promise(function (resolve, reject) {
      if (window.echarts) return resolve();
      var s = document.createElement('script');
      s.src = src; s.async = true; s.onload = resolve; s.onerror = reject;
      document.head.appendChild(s);
    });
  }

  function css(name, fallback) {
    var v = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
    return v || fallback;
  }

  // a palette colour (#rrggbb) at the given opacity
  function fade(hex, alpha) {
    var n = parseInt(hex.slice(1), 16);
    return 'rgba(' + (n >> 16) + ', ' + ((n >> 8) & 255) + ', ' + (n & 255) + ', ' + alpha + ')';
  }

  function formatter(fmt) {
    return function (v) {
      if (v === null || v === undefined || isNaN(v)) return '–';
      switch (fmt) {
        case 'percent': return (v * 100).toFixed(Math.abs(v) < 0.1 ? 2 : 1) + '%';
        case 'billions': {
          var a = Math.abs(v);
          return (v < 0 ? '-$' : '$') + a.toFixed(a < 1 && a !== 0 ? 2 : a < 10 && a !== 0 ? 1 : 0) + 'B';
        }
        case 'number': return v.toFixed(1);
        case 'amount': return Math.round(v).toLocaleString('en-US');
        // large counts such as volumes: 1.2B, 340M, 12K
        case 'compact': {
          var a = Math.abs(v), sign = v < 0 ? '-' : '';
          if (a >= 1e9) return sign + (a / 1e9).toFixed(a >= 1e10 ? 0 : 1) + 'B';
          if (a >= 1e6) return sign + (a / 1e6).toFixed(a >= 1e7 ? 0 : 1) + 'M';
          if (a >= 1e3) return sign + (a / 1e3).toFixed(a >= 1e4 ? 0 : 1) + 'K';
          return sign + a.toFixed(0);
        }
        case 'usd': {
          var a = Math.abs(v);
          if (a === 0) return '$0';
          if (a >= 1e12) return '$' + (v / 1e12).toFixed(2) + 'T';
          if (a >= 1e9) return '$' + (v / 1e9).toFixed(0) + 'B';
          return '$' + (v / 1e6).toFixed(0) + 'M';
        }
        case 'multiple': return v.toFixed(2) + 'x';
        case 'price': return '$' + v.toFixed(2);
        case 'ratio': return v.toFixed(2);
        // small values such as daily variances or option Greeks: three significant digits
        case 'decimal': return v === 0 ? '0' : Math.abs(v) >= 1 ? v.toFixed(2) : String(Number(v.toPrecision(3)));
        default: return Math.abs(v) >= 100 ? v.toFixed(0) : v.toFixed(3);
      }
    };
  }

  // the Ichimoku cloud: shade the band between Leading Span A and B
  function cloudSeries(spec) {
    var a = spec.series.filter(function (s) { return s.name === spec.cloud[0]; })[0];
    var b = spec.series.filter(function (s) { return s.name === spec.cloud[1]; })[0];
    if (!a || !b) return [];
    var low = a.data.map(function (v, i) { return v === null || b.data[i] === null ? null : Math.min(v, b.data[i]); });
    var band = a.data.map(function (v, i) { return v === null || b.data[i] === null ? null : Math.abs(v - b.data[i]); });
    return [
      { name: '_low', type: 'line', data: low, stack: 'cloud', symbol: 'none', lineStyle: { opacity: 0 }, tooltip: { show: false }, silent: true },
      { name: 'Cloud', type: 'line', data: band, stack: 'cloud', symbol: 'none', lineStyle: { opacity: 0 }, areaStyle: { color: 'rgba(129, 140, 248, 0.18)' }, tooltip: { show: false }, silent: true }
    ];
  }

  function option(spec) {
    var text = css('--text-secondary', '#cbd5e1');
    var muted = css('--text-muted', '#94a3b8');
    var grid = css('--card-border', 'rgba(255,255,255,0.1)');
    var fmt = formatter(spec.format);
    var isBar = spec.type === 'bar';
    var many = spec.x.length > 60;
    var series = spec.series.map(function (s, i) {
      var isClose = (spec.cloud || spec.overlay) && s.name === 'Close';
      // a reference line (a threshold such as RSI 70): dashed, muted, no markers
      if (s.reference) {
        return { name: s.name, type: 'line', data: s.data, showSymbol: false, silent: true, z: 1,
          lineStyle: { type: 'dashed', width: 1.5, color: muted }, itemStyle: { color: muted }, tooltip: { show: false } };
      }
      return {
        name: s.name,
        type: isBar ? 'bar' : 'line',
        // highlight: the index of one bar to set apart, e.g. a benchmark among the stocks
        data: isBar && spec.highlight !== undefined && spec.series.length === 1
          ? s.data.map(function (v, j) { return j === spec.highlight ? { value: v, itemStyle: { color: PALETTE[2] } } : v; })
          : s.data,
        // dots: markers only, for a level that jumps (the Parabolic SAR)
        showSymbol: s.dots || (!many && !isBar),
        symbolSize: s.dots ? 3 : 6,
        showAllSymbol: s.dots ? true : 'auto',
        smooth: false,
        connectNulls: false,
        // one series gets wide bars, several share the room of their category
        barMaxWidth: spec.series.filter(function (x) { return !x.reference; }).length === 1 ? 72 : 34,
        itemStyle: { color: isClose ? css('--text-primary', '#f8fafc') : (s.color || PALETTE[i % PALETTE.length]), borderRadius: isBar && !spec.stack ? [4, 4, 0, 0] : 0 },
        lineStyle: { width: s.dots ? 0 : isClose ? 2.2 : 1.8, type: s.dashed ? 'dashed' : 'solid' },
        emphasis: { focus: 'series' },
        smooth: !!spec.smooth,
        // area: fill under the line, fading out (drawdowns, cumulative values)
        areaStyle: s.area ? { opacity: 1, color: new window.echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: fade(s.color || PALETTE[i % PALETTE.length], s.area === 'down' ? 0.02 : 0.35) },
          { offset: 1, color: fade(s.color || PALETTE[i % PALETTE.length], s.area === 'down' ? 0.35 : 0.02) }]) } : undefined,
        // stack: series add up (the parts of a total)
        stack: spec.stack && !s.reference ? 'total' : undefined,
        // axis: 1 puts a series on a second y axis on the right, with format2
        yAxisIndex: s.axis === 1 ? 1 : 0,
        tooltip: s.axis === 1 ? { valueFormatter: formatter(spec.format2) } : undefined
      };
    });
    // bands: shaded periods such as recessions or crises, labelled at the top
    if (spec.bands && series.length) {
      series[0].markArea = { silent: true, itemStyle: { color: 'rgba(148, 163, 184, 0.12)' },
        label: { color: muted, fontSize: 11, position: 'insideTop' },
        data: spec.bands.map(function (b) { return [{ name: b.label || '', xAxis: b.from }, { xAxis: b.to }]; }) };
    }
    // markers: vertical lines at events, labelled
    if (spec.markers && series.length) {
      series[0].markLine = { silent: true, symbol: 'none', lineStyle: { color: muted, type: 'dashed', width: 1 },
        label: { color: muted, fontSize: 11, formatter: '{b}' },
        data: spec.markers.map(function (m) { return { name: m.label || '', xAxis: m.x }; }) };
    }
    if (spec.cloud) series = cloudSeries(spec).concat(series);
    var legendNames = spec.series.filter(function (s) { return !s.reference; }).map(function (s) { return s.name; });
    // direct labels: a line chart of two to five series names each line at its end,
    // in its colour, instead of a legend to match colours against (FT, Datawrapper).
    // Phones keep the legend, where the names would take a third of the width.
    var lines = spec.series.filter(function (s) { return !s.reference; });
    var direct = !isBar && !spec.stack && !spec.cloud && spec.legend !== true && spec.directLabels !== false &&
      lines.length >= 2 && lines.length <= 5 && window.innerWidth >= 700 && !lines.some(function (s) { return s.axis === 1; }) &&
      lines.every(function (s) { return s.data.length && s.data[s.data.length - 1] !== null && s.data[s.data.length - 1] !== undefined; });
    var labelRoom = 0;
    if (direct) {
      series.forEach(function (se, i) {
        var src = spec.series[i];
        if (!src || src.reference) return;
        var color = src.color || PALETTE[i % PALETTE.length];
        se.endLabel = { show: true, formatter: '{a}', color: color, fontSize: 12, fontWeight: 600, distance: 6 };
        se.labelLayout = { moveOverlap: 'shiftY' };
        se.emphasis = { focus: 'series', endLabel: { show: true } };
      });
      labelRoom = Math.min(170, 14 + 7 * Math.max.apply(null, lines.map(function (s) { return String(s.name).length; })));
    }
    return {
      animationDuration: 600,
      color: PALETTE,
      textStyle: { fontFamily: 'inherit', color: text, fontSize: 13 },
      grid: { left: 8, right: direct ? labelRoom : 28, top: direct ? 16 : 44, bottom: 12 + (spec.xname ? 26 : 0), containLabel: true },
      legend: { show: !direct, data: legendNames, top: 0, left: 0, textStyle: { color: text, fontSize: 13 }, icon: 'roundRect', itemWidth: 12, itemHeight: 8, type: 'scroll', pageTextStyle: { color: muted } },
      tooltip: {
        trigger: 'axis',
        backgroundColor: css('--masthead-bg', '#0f1115'),
        borderColor: grid,
        textStyle: { color: css('--text-primary', '#f8fafc'), fontSize: 13 },
        valueFormatter: fmt,
        axisPointer: { type: isBar ? 'shadow' : 'line', lineStyle: { color: muted } }
      },
      xAxis: {
        type: 'category',
        data: spec.x,
        name: spec.xname || '',
        nameLocation: 'middle',
        nameGap: 30,
        nameTextStyle: { color: muted },
        boundaryGap: isBar,
        axisLine: { lineStyle: { color: grid } },
        axisTick: { show: false },
        // many bars (the portfolio tickers): show every label, slanted; a long run of
        // years as bars (more than 60) labels only every few years, like a line
        axisLabel: isBar && !many && (spec.x.length > 10 || Math.max.apply(null, spec.x.map(function (v) { return String(v).length; })) > 8) ? { color: muted, interval: 0, rotate: 45, fontSize: 11 } : { color: muted, hideOverlap: true, fontSize: 12.5 }
      },
      yAxis: [{
        // log: a log scale, for growth over a long stretch (cumulative returns)
        type: spec.log ? 'log' : 'value',
        logBase: 10,
        scale: !isBar && !spec.stack && !spec.series.some(function (s) { return s.area; }),
        splitLine: { lineStyle: { color: grid } },
        axisLabel: { color: muted, formatter: fmt, fontSize: 12.5 }
      }].concat(spec.series.some(function (s) { return s.axis === 1; }) ? [{
        type: 'value',
        scale: true,
        splitLine: { show: false },
        axisLabel: { color: muted, formatter: formatter(spec.format2), fontSize: 12.5 }
      }] : []),
      series: series
    };
  }

  // Extended DuPont: five component panels that multiply into Return on Equity
  function renderDupont(box, chart) {
    box.innerHTML = '';
    box.classList.add('ft-chart--dupont');
    var head = document.createElement('div');
    head.className = 'ft-chart__head';
    var title = document.createElement('p');
    title.className = 'ft-chart__title';
    title.textContent = chart.title;
    head.appendChild(title);
    var tabs = document.createElement('div');
    tabs.className = 'ft-chart__tabs';
    tabs.setAttribute('role', 'tablist');
    chart.tabs.forEach(function (s, i) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'ft-chart__tab' + (i === 0 ? ' is-active' : '');
      b.textContent = s.label;
      b.setAttribute('role', 'tab');
      tabs.appendChild(b);
    });
    // one company needs no tab to pick it
    if (chart.tabs.length > 1) head.appendChild(tabs);
    var strip = document.createElement('div');
    strip.className = 'ft-dupont';
    box.appendChild(head);
    box.appendChild(strip);
    if (chart.tabs.length > 1) compactTabs(tabs);

    var minis = [];
    function panel(part, op, isResult) {
      var card = document.createElement('div');
      card.className = 'ft-dupont__part' + (isResult ? ' is-result' : '');
      if (op) {
        var o = document.createElement('span');
        o.className = 'ft-dupont__op';
        o.textContent = op;
        o.setAttribute('aria-hidden', 'true');
        card.appendChild(o);
      }
      var name = document.createElement('p');
      name.className = 'ft-dupont__name';
      card.appendChild(name);
      var value = document.createElement('p');
      value.className = 'ft-dupont__value';
      card.appendChild(value);
      var canvas = document.createElement('div');
      canvas.className = 'ft-dupont__canvas';
      card.appendChild(canvas);
      strip.appendChild(card);
      var inst = initChart(canvas);
      if ('ResizeObserver' in window) new ResizeObserver(function () { inst.resize(); }).observe(canvas);
      minis.push({ inst: inst, name: name, value: value, isResult: isResult });
    }
    for (var i = 0; i < 5; i++) panel(null, i === 0 ? null : '×', false);
    panel(null, '=', true);

    var current = 0;
    function draw() {
      var spec = chart.tabs[current];
      var parts = spec.components.concat([spec.result]);
      var last = spec.years.length - 1;
      var muted = css('--text-muted', '#94a3b8');
      var text = css('--text-secondary', '#cbd5e1');
      parts.forEach(function (part, i) {
        var m = minis[i];
        var fmt = formatter(part.format);
        var color = m.isResult ? '#c084fc' : PALETTE[i % PALETTE.length];
        m.name.textContent = part.name;
        m.value.textContent = fmt(part.data[last]);
        m.inst.setOption({
          animationDuration: 500,
          textStyle: { fontFamily: 'inherit' },
          grid: { left: 6, right: 6, top: spec.years.length <= 4 ? 22 : 8, bottom: 22 },
          tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' }, valueFormatter: fmt, backgroundColor: css('--masthead-bg', '#0f1115'), borderColor: css('--card-border', 'rgba(255,255,255,0.1)'), textStyle: { color: css('--text-primary', '#f8fafc'), fontSize: 13 } },
          xAxis: { type: 'category', data: spec.years, axisLine: { lineStyle: { color: css('--card-border', 'rgba(255,255,255,0.1)') } }, axisTick: { show: false }, axisLabel: { color: muted, fontSize: 12, interval: function (i) { return i === 0 || i === spec.years.length - 1; } } },
          yAxis: { type: 'value', show: false, min: 0 },
          series: [{
            name: part.name, type: 'bar', data: part.data, barMaxWidth: 26,
            itemStyle: { color: color, borderRadius: [4, 4, 0, 0] },
            // with many years the bars are not labelled (the latest value is shown
            // above the panel; hover shows each year)
            label: { show: spec.years.length <= 4, position: 'top', formatter: function (p) { return fmt(p.value); }, color: text, fontSize: 11 }
          }]
        }, true);
      });
    }
    draw();
    instances.push({ draw: draw });
    Array.prototype.forEach.call(tabs.children, function (b, i) {
      b.addEventListener('click', function () {
        current = i;
        Array.prototype.forEach.call(tabs.children, function (x, j) { x.classList.toggle('is-active', j === i); });
        draw();
      });
    });
  }

  // one card per ratio: the latest value, the change since the first year and
  // a small trend line over the years
  // the change between two values: percentage points for a percent metric,
  // otherwise in the metric's own format (a ratio, a multiple, a score)
  function change(a, b, fmt) {
    var d = b - a;
    if (fmt === 'percent' || !fmt) return (d >= 0 ? '+' : '') + (d * 100).toFixed(1) + ' pp';
    return (d >= 0 ? '+' : '–') + formatter(fmt)(Math.abs(d));
  }

  function renderKpis(box, chart) {
    box.innerHTML = '';
    var head = document.createElement('div');
    head.className = 'ft-chart__head';
    var title = document.createElement('p');
    title.className = 'ft-chart__title';
    // the years follow the title, unless the spec says period: false
    title.textContent = chart.title + (chart.period === false ? '' : ', ' + chart.series[0].name + '–' + chart.series[chart.series.length - 1].name);
    head.appendChild(title);
    var grid = document.createElement('div');
    // four cards as two rows of two rather than three and one
    grid.className = 'ft-kpis' + (chart.x.length === 4 ? ' ft-kpis--2x2' : '');
    box.appendChild(head);
    box.appendChild(grid);
    var fmt = formatter(chart.format);
    var years = chart.series.map(function (s) { return s.name; });
    var cards = chart.x.map(function (name, r) {
      var data = chart.series.map(function (s) { return s.data[r]; });
      var first = data[0], last = data[data.length - 1];
      var diff = last - first;
      var card = document.createElement('div');
      card.className = 'ft-kpis__card';
      card.innerHTML = '<p class="ft-kpis__name">' + name + '</p>' +
        '<p class="ft-kpis__value">' + fmt(last) + '</p>' +
        '<p class="ft-kpis__delta ' + (diff >= 0 ? 'is-up' : 'is-down') + '">' + (diff >= 0 ? '<i class="fas fa-arrow-trend-up" aria-hidden="true"></i> ' : '<i class="fas fa-arrow-trend-down" aria-hidden="true"></i> ') + change(first, last, chart.format) + ' since ' + years[0] + '</p>';
      var canvas = document.createElement('div');
      canvas.className = 'ft-kpis__canvas';
      card.appendChild(canvas);
      grid.appendChild(card);
      var inst = initChart(canvas);
      if ('ResizeObserver' in window) new ResizeObserver(function () { inst.resize(); }).observe(canvas);
      return { inst: inst, data: data, up: diff >= 0 };
    });
    function draw() {
      var muted = css('--text-muted', '#94a3b8');
      var text = css('--text-secondary', '#cbd5e1');
      cards.forEach(function (c) {
        var color = c.up ? '#34d399' : '#f472b6';
        c.inst.setOption({
          animationDuration: 500,
          textStyle: { fontFamily: 'inherit' },
          grid: { left: 20, right: 20, top: 26, bottom: 26 },
          tooltip: { trigger: 'axis', valueFormatter: fmt, backgroundColor: css('--masthead-bg', '#0f1115'), borderColor: css('--card-border', 'rgba(255,255,255,0.1)'), textStyle: { color: css('--text-primary', '#f8fafc'), fontSize: 13 } },
          xAxis: { type: 'category', data: years, boundaryGap: false, axisLine: { show: false }, axisTick: { show: false }, axisLabel: { color: muted, fontSize: 12, interval: function (i) { return i === 0 || i === years.length - 1; } } },
          yAxis: { type: 'value', show: false, scale: true },
          series: [{
            type: 'line', data: c.data, smooth: false, symbolSize: 7,
            lineStyle: { width: 2.5, color: color }, itemStyle: { color: color },
            areaStyle: { color: { type: 'linear', x: 0, y: 0, x2: 0, y2: 1, colorStops: [{ offset: 0, color: color + '55' }, { offset: 1, color: color + '00' }] } },
            // only the first and last value; hover shows the others
            label: { show: true, position: 'top', formatter: function (p) { return p.dataIndex === 0 || p.dataIndex === c.data.length - 1 ? fmt(p.value) : ''; }, color: text, fontSize: 11 }
          }]
        }, true);
      });
    }
    draw();
    instances.push({ draw: draw });
  }

  // Two companies side by side: one card per metric with both latest values,
  // the gap between them and a trend chart with the gap shaded
  function renderCompare(box, chart) {
    box.innerHTML = '';
    var head = document.createElement('div');
    head.className = 'ft-chart__head';
    var title = document.createElement('p');
    title.className = 'ft-chart__title';
    title.textContent = chart.title + (chart.period === false ? '' : ', fiscal ' + chart.x[0] + '–' + chart.x[chart.x.length - 1]);
    head.appendChild(title);
    var grid = document.createElement('div');
    grid.className = 'ft-compare';
    box.appendChild(head);
    box.appendChild(grid);
    var fmt = formatter(chart.format);
    var colors = [PALETTE[0], PALETTE[1]];
    var names = chart.names || {};
    var last = chart.x.length - 1;
    var cards = chart.metrics.map(function (m) {
      var a = m.series[0], b = m.series[1];
      var gap = b.data[last] - a.data[last];
      var gapText = chart.format === 'percent' || !chart.format ? (Math.abs(gap) * 100).toFixed(1) + ' pp' : formatter(chart.format)(Math.abs(gap));
      var leader = gap >= 0 ? b : a;
      var sides = m.series.map(function (s, i) {
        var diff = s.data[last] - s.data[0];
        return '<div class="ft-compare__side">' +
          '<p class="ft-compare__who"><span style="background:' + colors[i] + '"></span>' + (names[s.name] || s.name) + '</p>' +
          '<p class="ft-compare__value">' + fmt(s.data[last]) + '</p>' +
          '<p class="ft-kpis__delta ' + (diff >= 0 ? 'is-up' : 'is-down') + '">' + change(s.data[0], s.data[last], chart.format) + ' since ' + chart.x[0] + '</p></div>';
      }).join('');
      var card = document.createElement('div');
      card.className = 'ft-compare__card';
      card.innerHTML = '<div class="ft-compare__top"><p class="ft-kpis__name">' + m.name + '</p>' +
        '<span class="ft-compare__gap" style="--c:' + colors[m.series.indexOf(leader)] + '" title="' + (names[leader.name] || leader.name) + ' leads by ' + gapText + '">' + leader.name + ' +' + gapText + '</span></div>' +
        '<div class="ft-compare__sides">' + sides + '</div>';
      var canvas = document.createElement('div');
      canvas.className = 'ft-compare__canvas';
      card.appendChild(canvas);
      grid.appendChild(card);
      var inst = initChart(canvas);
      if ('ResizeObserver' in window) new ResizeObserver(function () { inst.resize(); }).observe(canvas);
      return { inst: inst, m: m };
    });
    function draw() {
      var muted = css('--text-muted', '#94a3b8');
      var text = css('--text-secondary', '#cbd5e1');
      cards.forEach(function (c) {
        var a = c.m.series[0].data, b = c.m.series[1].data;
        var low = a.map(function (v, i) { return Math.min(v, b[i]); });
        var band = a.map(function (v, i) { return Math.abs(v - b[i]); });
        var lines = c.m.series.map(function (s, i) {
          return {
            name: names[s.name] || s.name, type: 'line', data: s.data, symbolSize: 6, z: 3,
            lineStyle: { width: 2.5, color: colors[i] }, itemStyle: { color: colors[i] },
            label: { show: true, position: 'top', color: text, fontSize: 11, formatter: function (p) { return p.dataIndex === 0 || p.dataIndex === last ? fmt(p.value) : ''; } }
          };
        });
        c.inst.setOption({
          animationDuration: 500,
          textStyle: { fontFamily: 'inherit' },
          grid: { left: 22, right: 22, top: 24, bottom: 26 },
          tooltip: { trigger: 'axis', valueFormatter: fmt, backgroundColor: css('--masthead-bg', '#0f1115'), borderColor: css('--card-border', 'rgba(255,255,255,0.1)'), textStyle: { color: css('--text-primary', '#f8fafc'), fontSize: 13 } },
          xAxis: { type: 'category', data: chart.x, boundaryGap: false, axisLine: { show: false }, axisTick: { show: false }, axisLabel: { color: muted, fontSize: 12, interval: function (i) { return i === 0 || i === last; } } },
          yAxis: { type: 'value', show: false, scale: true },
          series: [
            { name: '_low', type: 'line', data: low, stack: 'gap', symbol: 'none', lineStyle: { opacity: 0 }, tooltip: { show: false }, silent: true },
            { name: '_gap', type: 'line', data: band, stack: 'gap', symbol: 'none', lineStyle: { opacity: 0 }, areaStyle: { color: 'rgba(129, 140, 248, 0.14)' }, tooltip: { show: false }, silent: true }
          ].concat(lines)
        }, true);
      });
    }
    draw();
    instances.push({ draw: draw });
  }

  // A bar chart with only a few bars across named categories (three tickers, a
  // statistic and its critical value) leaves thin bars stranded in a wide
  // plot. It reads better as cards: one per category, its value large with a
  // slim track against the largest, or with several series a row per series
  // on the card's own scale (so a statistic and a critical value each get
  // theirs). Years and other ordered axes keep their bars; `cards: false` in
  // the spec opts out and `cards: true` opts in.
  var ORDERED = /^(-?[\d.]+|\d{4}(-\d{2}(-\d{2})?)?|\d{4}-?Q[1-4])$/;

  function asCards(chart) {
    if (chart.cards !== undefined) return !!chart.cards;
    if (chart.type !== 'bar' || chart.stack || !chart.series || !chart.x) return false;
    var series = chart.series.filter(function (s) { return !s.reference; });
    if (!series.length || series.some(function (s) { return s.axis === 1; })) return false;
    if (chart.x.length * series.length > 6) return false;
    return !chart.x.some(function (x) { return ORDERED.test(String(x).trim()); });
  }

  function renderCards(box, chart) {
    box.innerHTML = '';
    var head = document.createElement('div');
    head.className = 'ft-chart__head';
    var title = document.createElement('p');
    title.className = 'ft-chart__title';
    title.textContent = chart.title;
    head.appendChild(title);
    box.appendChild(head);
    var fmt = formatter(chart.format);
    var series = chart.series.filter(function (s) { return !s.reference; });
    var grid = document.createElement('div');
    grid.className = 'ft-cards' + (series.length > 1 ? ' ft-cards--rows' : '');
    var columns = series.length > 1 ? Math.min(chart.x.length, 3) : (chart.x.length > 5 ? 3 : chart.x.length);
    grid.style.setProperty('--n', columns);
    // on a phone three cards still fit side by side; four or more go two by two
    var narrow = series.length > 1 ? 1 : (columns === 3 && chart.x.length === 3 ? 3 : Math.min(columns, 2));
    grid.style.setProperty('--n-narrow', narrow);
    if (narrow === 2 && chart.x.length % 2) grid.classList.add('ft-cards--odd');
    function track(value, max, color) {
      var width = value === null || value === undefined || !max ? 0 : Math.max(2, Math.abs(value) / max * 100);
      return '<span class="ft-cards__track"><span style="width:' + width + '%;background:' + color + '"></span></span>';
    }
    function abs(values) { return Math.max.apply(null, values.filter(function (v) { return v !== null && v !== undefined; }).map(Math.abs).concat([0])); }
    if (series.length === 1) {
      var data = series[0].data, max = abs(data);
      chart.x.forEach(function (name, i) {
        var v = data[i];
        var color = v !== null && v < 0 ? PALETTE[4] : PALETTE[0];
        var card = document.createElement('div');
        card.className = 'ft-cards__card';
        card.innerHTML = '<p class="ft-cards__name">' + name + '</p><p class="ft-cards__value">' + fmt(v) + '</p>' + track(v, max, color);
        grid.appendChild(card);
      });
    } else {
      chart.x.forEach(function (name, i) {
        var values = series.map(function (s) { return s.data[i]; }), max = abs(values);
        var rows = series.map(function (s, j) {
          var color = s.color || PALETTE[j % PALETTE.length];
          return '<li><span class="ft-cards__who"><i style="background:' + color + '"></i>' + s.name + '</span>' +
            track(values[j], max, color) + '<b>' + fmt(values[j]) + '</b></li>';
        }).join('');
        var card = document.createElement('div');
        card.className = 'ft-cards__card';
        card.innerHTML = '<p class="ft-cards__name">' + name + '</p><ul class="ft-cards__rows">' + rows + '</ul>';
        grid.appendChild(card);
      });
    }
    box.appendChild(grid);
  }

  function chrome(spec) {
    // the shared title row, returns the canvas to draw in
    return function (box, height) {
      box.innerHTML = '';
      var head = document.createElement('div');
      head.className = 'ft-chart__head';
      var title = document.createElement('p');
      title.className = 'ft-chart__title';
      title.textContent = spec.title;
      head.appendChild(title);
      if (spec.legend) {
        var legend = document.createElement('p');
        legend.className = 'ft-chart__legend';
        legend.innerHTML = spec.legend;
        head.appendChild(legend);
      }
      var canvas = document.createElement('div');
      canvas.className = 'ft-chart__canvas';
      if (height) canvas.style.height = height + 'px';
      box.appendChild(head);
      box.appendChild(canvas);
      var inst = initChart(canvas);
      if ('ResizeObserver' in window) new ResizeObserver(function () { inst.resize(); }).observe(canvas);
      return inst;
    };
  }

  function axisColors() {
    return { text: css('--text-secondary', '#cbd5e1'), muted: css('--text-muted', '#94a3b8'), grid: css('--card-border', 'rgba(255,255,255,0.1)') };
  }

  function tooltipStyle() {
    return { backgroundColor: css('--masthead-bg', '#0f1115'), borderColor: css('--card-border', 'rgba(255,255,255,0.1)'), textStyle: { color: css('--text-primary', '#f8fafc'), fontSize: 13 } };
  }

  // Horizontal bars, largest at the top, with the value at the end of each bar
  function renderHbar(box, chart) {
    var inst = chrome(chart)(box, Math.max(320, chart.x.length * 34 + 60));
    var fmt = formatter(chart.format);
    function draw() {
      var c = axisColors();
      inst.setOption({
        animationDuration: 600,
        textStyle: { fontFamily: 'inherit' },
        grid: { left: 8, right: 64, top: 8, bottom: 8, containLabel: true },
        tooltip: Object.assign({ trigger: 'axis', axisPointer: { type: 'shadow' }, valueFormatter: fmt }, tooltipStyle()),
        xAxis: { type: 'value', splitNumber: 4, splitLine: { lineStyle: { color: c.grid } }, axisLabel: { color: c.muted, formatter: fmt, hideOverlap: true } },
        yAxis: { type: 'category', data: chart.x.slice().reverse(), axisLine: { show: false }, axisTick: { show: false }, axisLabel: { color: c.text, fontSize: 13 } },
        series: [{
          name: chart.series[0].name, type: 'bar', barMaxWidth: 22,
          // highlight: index of a bar to set apart, e.g. the share price next to model values
          data: chart.series[0].data.map(function (v, i) { return i === chart.highlight ? { value: v, itemStyle: { color: PALETTE[2] } } : v; }).reverse(),
          itemStyle: { color: PALETTE[0], borderRadius: [0, 4, 4, 0] },
          label: { show: true, position: 'right', color: c.text, fontSize: 12, formatter: function (p) { return fmt(p.value); } }
        }]
      }, true);
    }
    draw();
    instances.push({ draw: draw });
  }

  // Regression coefficients with their 95% confidence interval; significant
  // coefficients in colour, stars by p-value
  function renderCoef(box, chart) {
    var stars = function (p) { return p < 0.001 ? '***' : p < 0.01 ? '**' : p < 0.05 ? '*' : ''; };
    var spec = Object.assign({ legend: '<span>* p &lt; 0.05</span><span>** p &lt; 0.01</span><span>*** p &lt; 0.001</span><span><i style="background:' + PALETTE[0] + '"></i>significant</span><span><i class="is-muted"></i>not significant</span>' }, chart);
    var inst = chrome(spec)(box, chart.height || Math.max(340, chart.x.length * 38 + 60));
    var n = chart.x.length;
    var rev = function (a) { return a.slice().reverse(); };
    var x = rev(chart.x), coef = rev(chart.coef), low = rev(chart.low), high = rev(chart.high), p = rev(chart.p);
    function draw() {
      var c = axisColors();
      var whisker = css('--text-primary', '#f8fafc');
      inst.setOption({
        animationDuration: 600,
        textStyle: { fontFamily: 'inherit' },
        grid: { left: 8, right: 48, top: 8, bottom: 8, containLabel: true },
        tooltip: Object.assign({
          trigger: 'axis', axisPointer: { type: 'shadow' },
          formatter: function (items) {
            var i = items[0].dataIndex;
            return '<b>' + x[i] + '</b><br>Coefficient ' + coef[i].toFixed(4) + '<br>95% interval ' + low[i].toFixed(3) + ' to ' + high[i].toFixed(3) + '<br>p-value ' + p[i].toFixed(4) + ' ' + stars(p[i]);
          }
        }, tooltipStyle()),
        // wide enough for every interval, with room for the stars on the right
        xAxis: {
          type: 'value', splitLine: { lineStyle: { color: c.grid } }, axisLabel: { color: c.muted, formatter: function (v) { return v.toFixed(2); } },
          // always with zero on the axis, so every bar starts from it
          min: Math.floor(Math.min(0, Math.min.apply(null, low)) * 10) / 10,
          max: Math.ceil((Math.max(0, Math.max.apply(null, high)) + 0.04) * 10) / 10
        },
        yAxis: { type: 'category', data: x, axisLine: { show: false }, axisTick: { show: false }, axisLabel: { color: c.text, fontSize: 13 } },
        series: [
          {
            type: 'bar', data: coef.map(function (v, i) { return { value: v, itemStyle: { color: p[i] < 0.05 ? PALETTE[0] : 'rgba(148, 163, 184, 0.45)' } }; }),
            barMaxWidth: 20, itemStyle: { borderRadius: 4 }, z: 2
          },
          {
            type: 'custom', z: 3, silent: true, tooltip: { show: false },
            data: x.map(function (_, i) { return [low[i], high[i], i]; }),
            renderItem: function (params, api) {
              var a = api.coord([api.value(0), api.value(2)]), b = api.coord([api.value(1), api.value(2)]);
              var cap = api.size([0, 1])[1] * 0.18;
              var style = { stroke: whisker, lineWidth: 1.4, opacity: 0.85 };
              var label = stars(p[api.value(2)]);
              var children = [
                { type: 'line', shape: { x1: a[0], y1: a[1], x2: b[0], y2: b[1] }, style: style },
                { type: 'line', shape: { x1: a[0], y1: a[1] - cap, x2: a[0], y2: a[1] + cap }, style: style },
                { type: 'line', shape: { x1: b[0], y1: b[1] - cap, x2: b[0], y2: b[1] + cap }, style: style }
              ];
              if (label) children.push({ type: 'text', style: { text: label, x: b[0] + 6, y: b[1], verticalAlign: 'middle', fill: whisker, font: 'bold 13px sans-serif' } });
              return { type: 'group', children: children };
            }
          }
        ]
      }, true);
    }
    draw();
    instances.push({ draw: draw });
  }

  // Labelled points, e.g. quality (ROIC) against price (EV/EBITDA)
  function renderScatter(box, chart) {
    var inst = chrome(chart)(box, chart.height || 380);
    var fx = formatter(chart.xformat), fy = formatter(chart.yformat);
    var xs = chart.points.map(function (pt) { return pt.x; });
    var xMin = Math.min.apply(null, xs), xSpan = Math.max.apply(null, xs) - xMin;
    // highlight: one point's index, or a list of them (e.g. the stocks that pass a screen)
    var marked = [].concat(chart.highlight === undefined ? [] : chart.highlight);
    function draw() {
      var c = axisColors();
      // lines: dashed thresholds, e.g. [{"axis": "x", "value": 20, "label": "P/E 20"}]
      var lines = (chart.lines || []).map(function (l) {
        var d = { name: l.label || '', label: { formatter: l.label || '', color: c.muted, fontSize: 11, position: l.axis === 'x' ? 'end' : 'insideEndTop' } };
        d[l.axis === 'x' ? 'xAxis' : 'yAxis'] = l.value;
        return d;
      });
      inst.setOption({
        animationDuration: 600,
        textStyle: { fontFamily: 'inherit' },
        grid: { left: 8, right: 24, top: 34, bottom: 30, containLabel: true },
        tooltip: Object.assign({ trigger: 'item', formatter: function (p) { return '<b>' + p.data.name + '</b><br>' + chart.xname + ': ' + fx(p.data.value[0]) + '<br>' + chart.yname + ': ' + fy(p.data.value[1]); } }, tooltipStyle()),
        xAxis: { type: 'value', scale: true, splitNumber: 4, name: chart.xname, nameLocation: 'middle', nameGap: 28, nameTextStyle: { color: c.muted }, splitLine: { lineStyle: { color: c.grid } }, axisLabel: { color: c.muted, formatter: fx, hideOverlap: true } },
        yAxis: { type: 'value', scale: true, name: chart.yname, nameTextStyle: { color: c.muted, align: 'left' }, splitLine: { lineStyle: { color: c.grid } }, axisLabel: { color: c.muted, formatter: fy } },
        series: [{
          type: 'scatter', symbolSize: 18,
          // pos: where a point's name goes when it would cover a neighbour ('left', 'top', 'topleft', 'bottom', 'bottomleft')
          // points in the right-hand third carry their name on the left, so the plot
          // can use the full width instead of keeping a margin free for labels
          data: chart.points.map(function (pt, i) {
            var d = { name: pt.name, value: [pt.x, pt.y], itemStyle: { color: marked.indexOf(i) >= 0 ? PALETTE[2] : PALETTE[0], opacity: 0.9 } };
            // a name that would run past the right edge of the plot goes on the left
            var plotW = inst.getWidth() - 80;
            var px = xSpan > 0 ? (pt.x - xMin) / xSpan * plotW : 0;
            var pos = pt.pos || (px + 14 + pt.name.length * 6.6 > plotW ? 'left' : null);
            // 'topleft': above the point and ending at it, for a point at the right edge
            if (pos === 'topleft') d.label = { position: 'top', align: 'right', offset: [8, 0] };
            else if (pos === 'bottomleft') d.label = { position: 'bottom', align: 'right', offset: [8, 0] };
            else if (pos) d.label = { position: pos };
            return d;
          }),
          label: { show: true, position: 'right', color: c.text, fontSize: 12, formatter: function (p) { return p.data.name; } },
          // points close together: push their names apart instead of printing them over each other
          labelLayout: { moveOverlap: 'shiftY' },
          markLine: lines.length ? { silent: true, symbol: 'none', lineStyle: { type: 'dashed', width: 1.5, color: c.muted }, data: lines } : undefined
        }].concat(chart.curve ? [{
          // curve: a line through [x, y] pairs under the points, e.g. an efficient frontier
          type: 'line', data: chart.curve, showSymbol: false, silent: true, z: 1,
          lineStyle: { width: 2, color: PALETTE[1] }, tooltip: { show: false }
        }] : [])
      }, true);
    }
    draw();
    instances.push({ draw: draw });
  }

  // A correlation matrix as a heatmap, blue for positive, pink for negative
  function renderHeatmap(box, chart) {
    var n = chart.x.length;
    var inst = chrome(chart)(box, chart.height || Math.max(260, chart.y.length * 46 + 110));
    var data = [];
    chart.values.forEach(function (row, i) { row.forEach(function (v, j) { if (v !== null) data.push([j, i, v]); }); });
    // cell labels: in the chart's format (e.g. percent), else two decimals
    var cell = chart.format ? formatter(chart.format) : function (v) { return v.toFixed(chart.digits !== undefined ? chart.digits : 2); };
    function draw() {
      var c = axisColors();
      inst.setOption({
        animationDuration: 500,
        textStyle: { fontFamily: 'inherit' },
        grid: { left: 8, right: 8, top: 8, bottom: 40, containLabel: true },
        tooltip: Object.assign({ formatter: function (p) { return chart.x[p.data[0]] + ' · ' + chart.y[p.data[1]] + ': <b>' + cell(p.data[2]) + '</b>'; } }, tooltipStyle()),
        xAxis: { type: 'category', data: chart.x, splitArea: { show: false }, axisLine: { show: false }, axisTick: { show: false }, axisLabel: { color: c.text, fontSize: 12, interval: 0, rotate: n > 6 ? 40 : 0 } },
        yAxis: { type: 'category', data: chart.y, inverse: true, axisLine: { show: false }, axisTick: { show: false }, axisLabel: { color: c.text, fontSize: 12, interval: 0 } },
        visualMap: { min: chart.min !== undefined ? chart.min : -1, max: chart.max !== undefined ? chart.max : 1, calculable: false, orient: 'horizontal', left: 'center', bottom: 0, itemWidth: 10, itemHeight: 120, textStyle: { color: c.muted }, inRange: { color: (function (c) { return chart.reverse ? c.slice().reverse() : c; })(chart.scale === 'sequential' ? ['rgba(148,163,184,0.15)', '#38bdf8'] : ['#f472b6', 'rgba(148,163,184,0.15)', '#38bdf8']) } },
        series: [{ type: 'heatmap', data: data, label: { show: true, color: css('--text-primary', '#f8fafc'), fontSize: 12, formatter: function (p) { return cell(p.data[2]); } }, itemStyle: { borderColor: css('--card-bg', '#1e293b'), borderWidth: 2, borderRadius: 4 } }]
      }, true);
    }
    draw();
    instances.push({ draw: draw });
  }

  // Percentile fan: the 5-95% and 25-75% bands with the median. Several series
  // (e.g. stress regimes) each get their 5-95% band and median in their own colour.
  function renderFan(box, chart) {
    var inst = chrome(chart)(box, 380);
    function draw() { inst.setOption(fanOption(chart), true); }
    draw();
    instances.push({ draw: draw });
  }

  function fanOption(chart) {
    var fmt = formatter(chart.format);
    var single = chart.series.length === 1;
    // the centre line and outer band are the median and 5–95% unless named, e.g. an estimate's average and low to high
    var mid = chart.center || 'median', outer = chart.range || '5–95%';
    function band(low, high, name, color, opacity, stack) {
      return [
        { name: '_' + stack, type: 'line', data: low, stack: stack, symbol: 'none', lineStyle: { opacity: 0 }, tooltip: { show: false }, silent: true },
        { name: name, type: 'line', data: high.map(function (v, i) { return v === null || low[i] === null ? null : v - low[i]; }), stack: stack, symbol: 'none', lineStyle: { opacity: 0 }, areaStyle: { color: color, opacity: opacity }, tooltip: { show: false }, silent: true }
      ];
    }
    var c = axisColors(), series = [], legend = [];
      chart.series.forEach(function (s, i) {
        var color = single ? PALETTE[0] : PALETTE[i % PALETTE.length];
        series = series.concat(band(s.q05, s.q95, single ? outer : s.name + ' ' + outer, color, single ? 0.18 : 0.07, 'o' + i));
        if (single && s.q25) series = series.concat(band(s.q25, s.q75, '25–75%', color, 0.3, 'i' + i));
        series.push({ name: single ? mid.charAt(0).toUpperCase() + mid.slice(1) : s.name, type: 'line', data: s.q5, showSymbol: false, lineStyle: { width: 2.2, color: color }, itemStyle: { color: color }, z: 5 });
        legend.push(single ? mid.charAt(0).toUpperCase() + mid.slice(1) : s.name);
      });
      return {
        animationDuration: 600,
        textStyle: { fontFamily: 'inherit' },
        legend: { data: legend, top: 0, left: 0, textStyle: { color: c.text, fontSize: 13 }, icon: 'roundRect', itemWidth: 12, itemHeight: 8, type: 'scroll' },
        grid: { left: 8, right: 24, top: 40, bottom: 12, containLabel: true },
        tooltip: Object.assign({ trigger: 'axis', formatter: function (items) {
          var i = items[0].dataIndex, out = '<b>' + chart.x[i] + '</b>';
          chart.series.forEach(function (s) {
            out += '<br>' + (single ? '' : s.name + ': ') + mid + ' ' + fmt(s.q5[i]) + (single && s.q25 ? '<br>25–75%: ' + fmt(s.q25[i]) + ' to ' + fmt(s.q75[i]) : '') + '<br>' + (single ? '' : '&nbsp;&nbsp;') + outer + ': ' + fmt(s.q05[i]) + ' to ' + fmt(s.q95[i]);
          });
          return out;
        } }, tooltipStyle()),
        xAxis: { type: 'category', data: chart.x, boundaryGap: false, axisLine: { lineStyle: { color: c.grid } }, axisTick: { show: false }, axisLabel: { color: c.muted, hideOverlap: true } },
        yAxis: { type: 'value', scale: true, splitLine: { lineStyle: { color: c.grid } }, axisLabel: { color: c.muted, formatter: fmt } },
        series: series
      };
  }

  // Histogram of outcomes with labelled vertical marker lines
  function renderHist(box, chart) {
    var inst = chrome(chart)(box, 360);
    var fmt = formatter(chart.format);
    function draw() {
      var c = axisColors(), text = css('--text-primary', '#f8fafc');
      inst.setOption({
        animationDuration: 600,
        textStyle: { fontFamily: 'inherit' },
        grid: { left: 8, right: 24, top: 64, bottom: 30, containLabel: true },
        tooltip: Object.assign({ trigger: 'item', formatter: function (p) { return fmt(p.data[0] - chart.width / 2) + ' to ' + fmt(p.data[0] + chart.width / 2) + '<br><b>' + p.data[1] + '</b> scenarios'; } }, tooltipStyle()),
        xAxis: { type: 'value', scale: true, name: chart.xname, nameLocation: 'middle', nameGap: 28, nameTextStyle: { color: c.muted }, splitLine: { show: false }, axisLabel: { color: c.muted, formatter: fmt, hideOverlap: true } },
        yAxis: { type: 'value', splitLine: { lineStyle: { color: c.grid } }, axisLabel: { color: c.muted } },
        series: [{
          type: 'bar', barWidth: '92%', barCategoryGap: 0, itemStyle: { color: PALETTE[0], opacity: 0.75, borderRadius: [2, 2, 0, 0] },
          data: chart.bins.map(function (b, i) { return [b, chart.counts[i]]; }),
          markLine: {
            symbol: 'none', silent: true,
            label: { color: text, fontSize: 12, formatter: function (p) { return p.name + ': ' + fmt(p.value); } },
            lineStyle: { type: 'dashed', width: 1.5 },
            data: chart.markers.map(function (m, i) { return { name: m.label, xAxis: m.value, label: { distance: 4 + (i % 2) * 18, formatter: m.label + ': ' + fmt(m.value) }, lineStyle: { color: [PALETTE[2], PALETTE[1], PALETTE[3]][i % 3] } }; })
          }
        }]
      }, true);
    }
    draw();
    instances.push({ draw: draw });
  }


  // Tab buttons that would wrap onto more lines become one dropdown with the same
  // choices; the buttons come back when there is room again
  function compactTabs(tabs) {
    var head = tabs.parentElement;
    var buttons = Array.prototype.slice.call(tabs.children);
    var select = document.createElement('select');
    select.className = 'ft-chart__select';
    select.setAttribute('aria-label', 'Choose a view');
    buttons.forEach(function (b, i) {
      var o = document.createElement('option');
      o.value = String(i);
      o.textContent = b.textContent;
      select.appendChild(o);
    });
    tabs.insertAdjacentElement('afterend', select);
    select.addEventListener('change', function () { buttons[Number(select.value)].click(); });
    tabs.addEventListener('click', function () {
      buttons.forEach(function (b, i) { if (b.classList.contains('is-active')) select.value = String(i); });
    });
    var needed = 0;
    function fit() {
      if (!needed) {
        // the buttons' own width on one line, measured once while they are shown
        head.classList.remove('is-compact');
        needed = buttons.reduce(function (w, b) { return w + b.getBoundingClientRect().width; }, 0) + 4 * (buttons.length - 1);
      }
      head.classList.toggle('is-compact', needed > head.clientWidth);
    }
    fit();
    if ('ResizeObserver' in window) new ResizeObserver(fit).observe(head);
    else window.addEventListener('resize', fit);
  }

  // Several charts of one section in one frame, one tab each (like `tabs`, but
  // each tab can be any kind of chart: a heatmap, a scatter, coefficients...).
  // A tab is drawn the first time it is shown, so it gets its real width.
  function renderPanels(box, chart) {
    box.innerHTML = '';
    var head = document.createElement('div');
    head.className = 'ft-chart__head';
    var title = document.createElement('p');
    title.className = 'ft-chart__title';
    title.textContent = chart.title;
    head.appendChild(title);
    var tabs = document.createElement('div');
    tabs.className = 'ft-chart__tabs';
    tabs.setAttribute('role', 'tablist');
    head.appendChild(tabs);
    box.appendChild(head);
    var subs = chart.panels.map(function (panel, i) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'ft-chart__tab' + (i === 0 ? ' is-active' : '');
      b.textContent = panel.label;
      b.setAttribute('role', 'tab');
      tabs.appendChild(b);
      var sub = document.createElement('div');
      sub.className = 'ft-chart ft-chart--panel';
      if (i > 0) sub.hidden = true;
      box.appendChild(sub);
      return sub;
    });
    compactTabs(tabs);
    var drawn = [];
    function show(i) {
      subs.forEach(function (sub, j) { sub.hidden = j !== i; });
      Array.prototype.forEach.call(tabs.children, function (x, j) { x.classList.toggle('is-active', j === i); });
      if (!drawn[i]) { drawn[i] = true; render(subs[i], Object.assign({}, chart.panels[i], { title: '' })); }
    }
    Array.prototype.forEach.call(tabs.children, function (b, i) { b.addEventListener('click', function () { show(i); }); });
    show(0);
  }

  // A technical analysis chart as the indicator is usually drawn: the price as
  // candlesticks with the overlays on it (bands, averages, stops), and an
  // indicator in its own panel underneath with its usual levels, on one time
  // axis that zooms both. spec: x, ohlc ([open, close, low, high] per day),
  // overlays [{name, data, color, dashed, dots}], fill [upper, lower] (the band
  // between two overlays), lower {series [{name, data, bar, color}], levels,
  // format, min, max}, zoom (the number of days shown at first).
  function renderTa(box, chart) {
    box.innerHTML = '';
    var head = document.createElement('div');
    head.className = 'ft-chart__head';
    var title = document.createElement('p');
    title.className = 'ft-chart__title';
    title.textContent = chart.title || '';
    head.appendChild(title);
    if (chart.subtitle) {
      var sub = document.createElement('p');
      sub.className = 'ft-chart__subtitle';
      sub.textContent = chart.subtitle;
      head.appendChild(sub);
    }
    box.appendChild(head);
    var canvas = document.createElement('div');
    canvas.className = 'ft-chart__canvas';
    canvas.style.height = (chart.lower ? 600 : 440) + 'px';
    box.appendChild(canvas);
    var inst = initChart(canvas);
    var UP = '#22c55e', DOWN = '#ef4444';
    function draw() {
      var text = css('--text-secondary', '#cbd5e1'), muted = css('--text-muted', '#94a3b8'), grid = css('--card-border', 'rgba(255,255,255,0.1)');
      var fmt = formatter(chart.format), lowFmt = formatter(chart.lower && chart.lower.format || 'ratio');
      var lower = chart.lower;
      var grids = lower ? [{ left: 8, right: 16, top: 40, height: '48%', containLabel: true }, { left: 8, right: 16, top: '63%', bottom: 56, containLabel: true }]
                        : [{ left: 8, right: 16, top: 40, bottom: 56, containLabel: true }];
      var axisX = function (i) {
        return { type: 'category', data: chart.x, gridIndex: i, boundaryGap: true, axisLine: { lineStyle: { color: grid } }, axisTick: { show: false },
          axisLabel: { show: !lower || i === 1, color: muted, hideOverlap: true, fontSize: 12 }, axisPointer: { label: { show: false } } };
      };
      // the price as candlesticks (left out for indicators of a whole market, such as breadth)
      var series = chart.ohlc ? [{
        name: chart.priceName || 'Price', type: 'candlestick', data: chart.ohlc.map(function (d) { return d || ['-', '-', '-', '-']; }), xAxisIndex: 0, yAxisIndex: 0, barMaxWidth: 8,
        itemStyle: { color: UP, color0: DOWN, borderColor: UP, borderColor0: DOWN }
      }] : [];
      var names = chart.ohlc ? [chart.priceName || 'Price'] : [];
      (chart.overlays || []).forEach(function (o, i) {
        var color = o.color || PALETTE[(i + 1) % PALETTE.length];
        series.push({ name: o.name, type: 'line', data: o.data, xAxisIndex: 0, yAxisIndex: 0, symbol: 'circle',
          showSymbol: !!o.dots, showAllSymbol: !!o.dots, symbolSize: o.dots ? 3 : 4, connectNulls: false, step: o.step ? 'end' : false,
          itemStyle: { color: color }, lineStyle: { width: o.dots ? 0 : 1.6, color: color, type: o.dashed ? 'dashed' : 'solid' } });
        names.push(o.name);
      });
      // the band between two overlays, shaded (Bollinger Bands, channels, the Ichimoku cloud)
      if (chart.fill) {
        var up = chart.overlays.filter(function (o) { return o.name === chart.fill[0]; })[0];
        var dn = chart.overlays.filter(function (o) { return o.name === chart.fill[1]; })[0];
        if (up && dn) {
          // one colour for the band, or two (fill_colors): the first where fill[0] is on top
          var colors = chart.fill_colors || [up.color || PALETTE[1], up.color || PALETTE[1]];
          [0, 1].forEach(function (side) {
            if (side === 1 && !chart.fill_colors) return;
            var on = function (i) {
              var a = up.data[i], b = dn.data[i];
              if (a === null || b === null) return false;
              return chart.fill_colors ? (side === 0 ? a >= b : a < b) : true;
            };
            var low = dn.data.map(function (v, i) { return on(i) ? Math.min(v, up.data[i]) : null; });
            var width = dn.data.map(function (v, i) { return on(i) ? Math.abs(up.data[i] - v) : null; });
            var stack = 'band' + side;
            series.unshift(
              { name: '_low' + side, type: 'line', data: low, stack: stack, symbol: 'none', lineStyle: { opacity: 0 }, silent: true, tooltip: { show: false }, xAxisIndex: 0, yAxisIndex: 0 },
              { name: '_band' + side, type: 'line', data: width, stack: stack, symbol: 'none', lineStyle: { opacity: 0 }, areaStyle: { color: fade(colors[side], 0.14) }, silent: true, tooltip: { show: false }, xAxisIndex: 0, yAxisIndex: 0 });
          });
        }
      }
      var yAxes = [{ type: 'value', scale: true, gridIndex: 0, splitLine: { lineStyle: { color: grid } }, axisLabel: { color: muted, formatter: fmt, fontSize: 12 } }];
      if (lower) {
        yAxes.push({ type: 'value', scale: lower.min === undefined, min: lower.min, max: lower.max, gridIndex: 1, splitNumber: 3,
          splitLine: { lineStyle: { color: grid } }, axisLabel: { color: muted, formatter: lowFmt, fontSize: 12 } });
        lower.series.forEach(function (l, i) {
          var color = l.color || PALETTE[(i + (chart.overlays || []).length + 1) % PALETTE.length];
          var item = { name: l.name, type: l.bar ? 'bar' : 'line', data: l.data, xAxisIndex: 1, yAxisIndex: 1, symbol: 'none', connectNulls: false,
            itemStyle: { color: color }, lineStyle: { width: 1.6, color: color } };
          // a histogram above and below zero: positive bars green, negative red
          if (l.bar && l.signed) item.data = l.data.map(function (v) { return v === null ? null : { value: v, itemStyle: { color: v >= 0 ? fade(UP, 0.7) : fade(DOWN, 0.7) } }; });
          if (i === 0 && lower.levels) {
            item.markLine = { silent: true, symbol: 'none', label: { show: true, position: 'end', color: muted, fontSize: 11, formatter: function (p) { return lowFmt(p.value); } },
              lineStyle: { color: muted, type: 'dashed', width: 1 }, data: lower.levels.map(function (v) { return { yAxis: v }; }) };
          }
          series.push(item);
          names.push(l.name);
        });
      }
      // half the period at first on a phone, where a year of candles is too dense to read
      var zoom = chart.zoom && canvas.clientWidth < 600 ? Math.round(chart.zoom / 2) : chart.zoom;
      var start = zoom && chart.x.length > zoom ? 100 * (1 - zoom / chart.x.length) : 0;
      inst.setOption({
        animation: false,
        textStyle: { fontFamily: 'inherit', color: text, fontSize: 13 },
        legend: { data: names, top: 0, left: 0, textStyle: { color: text, fontSize: 12.5 }, icon: 'roundRect', itemWidth: 12, itemHeight: 8, type: 'scroll' },
        tooltip: { trigger: 'axis', axisPointer: { type: 'cross', link: [{ xAxisIndex: 'all' }], lineStyle: { color: muted } },
          backgroundColor: css('--masthead-bg', '#0f1115'), borderColor: grid, textStyle: { color: css('--text-primary', '#f8fafc'), fontSize: 12.5 },
          valueFormatter: function (v) { return typeof v === 'number' ? fmt(v) : v; } },
        axisPointer: { link: [{ xAxisIndex: 'all' }] },
        grid: grids,
        xAxis: lower ? [axisX(0), axisX(1)] : [axisX(0)],
        yAxis: yAxes,
        dataZoom: [
          { type: 'inside', xAxisIndex: lower ? [0, 1] : [0], start: start, end: 100 },
          { type: 'slider', xAxisIndex: lower ? [0, 1] : [0], start: start, end: 100, bottom: 8, height: 22, borderColor: grid,
            textStyle: { color: muted }, fillerColor: 'rgba(56, 189, 248, 0.12)', dataBackground: { lineStyle: { color: muted }, areaStyle: { color: 'rgba(148,163,184,0.15)' } } }
        ],
        series: series
      }, true);
    }
    draw();
    instances.push({ instance: inst, draw: draw });
    if ('ResizeObserver' in window) new ResizeObserver(function () { inst.resize(); }).observe(canvas);
  }

  function render(box, chart) {
    if (chart.type === 'ta') return renderTa(box, chart);
    if (chart.type === 'panels') return renderPanels(box, chart);
    if (asCards(chart)) return renderCards(box, chart);
    if (chart.type === 'dupont') return renderDupont(box, chart);
    if (chart.type === 'kpis') return renderKpis(box, chart);
    if (chart.type === 'compare') return renderCompare(box, chart);
    if (chart.type === 'hbar') return renderHbar(box, chart);
    if (chart.type === 'coef') return renderCoef(box, chart);
    if (chart.type === 'scatter') return renderScatter(box, chart);
    if (chart.type === 'fan') return renderFan(box, chart);
    if (chart.type === 'hist') return renderHist(box, chart);
    if (chart.type === 'heatmap') return renderHeatmap(box, chart);
    var specs = chart.type === 'tabs' ? chart.tabs : [chart];
    box.innerHTML = '';
    var head = document.createElement('div');
    head.className = 'ft-chart__head';
    var title = document.createElement('p');
    title.className = 'ft-chart__title';
    title.textContent = chart.title || specs[0].title || '';
    head.appendChild(title);
    var tabs;
    if (specs.length > 1) {
      tabs = document.createElement('div');
      tabs.className = 'ft-chart__tabs';
      tabs.setAttribute('role', 'tablist');
      specs.forEach(function (s, i) {
        var b = document.createElement('button');
        b.type = 'button';
        b.className = 'ft-chart__tab' + (i === 0 ? ' is-active' : '');
        b.textContent = s.label;
        b.setAttribute('role', 'tab');
        tabs.appendChild(b);
      });
      head.appendChild(tabs);
    }
    var canvas = document.createElement('div');
    canvas.className = 'ft-chart__canvas';
    if (chart.height) canvas.style.height = chart.height + 'px';
    box.appendChild(head);
    box.appendChild(canvas);
    if (tabs) compactTabs(tabs);

    var instance = initChart(canvas);
    var current = 0;
    function draw() { instance.setOption(specs[current].type === 'fan' ? fanOption(specs[current]) : option(specs[current]), true); }
    draw();
    instances.push({ instance: instance, draw: draw });
    if (tabs) {
      Array.prototype.forEach.call(tabs.children, function (b, i) {
        b.addEventListener('click', function () {
          current = i;
          Array.prototype.forEach.call(tabs.children, function (x, j) { x.classList.toggle('is-active', j === i); });
          draw();
        });
      });
    }
    if ('ResizeObserver' in window) new ResizeObserver(function () { instance.resize(); }).observe(canvas);
    else window.addEventListener('resize', function () { instance.resize(); });
  }

  var ready = {};
  var fresh = {};
  function start(src) {
    if (!ready[src]) {
      ready[src] = Promise.all([loadScript(ECHARTS), fetch(src).then(function (r) { return r.json(); })])
        .then(function (r) { return r[1]; });
    }
    return ready[src];
  }

  // the chart, plus its optional "subtitle" (what is plotted: unit, base, period)
  // under the title and its "source" line under the chart
  function draw(box, spec) {
    render(box, spec);
    var title = box.querySelector('.ft-chart__title');
    if (spec.subtitle && title && !box.querySelector('.ft-chart__subtitle')) {
      var sub = document.createElement('p');
      sub.className = 'ft-chart__subtitle';
      sub.textContent = spec.subtitle;
      title.insertAdjacentElement('afterend', sub);
    }
    if (spec.source && !box.querySelector('.ft-chart__source')) {
      var src = document.createElement('p');
      src.className = 'ft-chart__source';
      src.textContent = 'Source: ' + spec.source;
      box.appendChild(src);
    }
    addNotes(box, spec);
    addDataButton(box, spec);
    var holder = box.closest('.ft-chart-box');
    if (holder && holder.ftFit) holder.ftFit();
  }

  // A "Notes" button next to Python and MCP for the chart's `note`: how the data is built and
  // what to keep in mind when reading it, one paragraph per string, in a panel over the chart
  function addNotes(box, spec) {
    var holder = box.closest('.ft-chart-box');
    var actions = holder && holder.querySelector('.ft-chart-actions');
    if (!spec.note || !actions || actions.querySelector('[data-panel="notes"]')) return;
    var panel = document.createElement('div');
    panel.className = 'ft-chart-panel';
    panel.setAttribute('data-panel', 'notes');
    panel.hidden = true;
    var card = document.createElement('div');
    card.className = 'ft-chart-panel__card';
    card.innerHTML = '<p class="ft-chart-panel__label"><i class="fas fa-circle-info" aria-hidden="true"></i> About this chart</p>';
    [].concat(spec.note).forEach(function (text) {
      var p = document.createElement('p');
      p.className = 'ft-chart-panel__text';
      p.textContent = text;
      card.appendChild(p);
    });
    if (spec.source) {
      var src = document.createElement('p');
      src.className = 'ft-chart-panel__note';
      src.textContent = 'Source: ' + spec.source;
      card.appendChild(src);
    }
    panel.appendChild(card);
    holder.appendChild(panel);
    var button = document.createElement('button');
    button.type = 'button';
    button.className = 'ft-chart-action';
    button.setAttribute('data-panel', 'notes');
    button.setAttribute('aria-expanded', 'false');
    button.title = 'How this chart is built and what to keep in mind';
    button.innerHTML = '<i class="fas fa-circle-info" aria-hidden="true"></i><span>Notes</span>';
    actions.appendChild(button);
  }

  // The chart's data as CSV rows: one row per x value (or per point, or per heatmap row),
  // one column per series; tabs and compare cards become one table with "View: Series" columns.
  // Values are as stored, so percentages are fractions (0.25 is 25%).
  function csvRows(spec) {
    function table(views) {
      var xs = [], cols = [];
      views.forEach(function (v) {
        (v.x || []).forEach(function (x) { if (xs.indexOf(x) < 0) xs.push(x); });
        (v.series || []).forEach(function (se) {
          var at = {};
          (v.x || []).forEach(function (x, i) { at[x] = se.data[i]; });
          cols.push({ name: !v.prefix ? se.name : v.series.length === 1 ? v.prefix : v.prefix + ': ' + se.name, at: at });
        });
      });
      if (!xs.length || !cols.length) return null;
      var rows = [[spec.xname || ''].concat(cols.map(function (c) { return c.name; }))];
      xs.forEach(function (x) { rows.push([x].concat(cols.map(function (c) { return c.at[x]; }))); });
      return rows;
    }
    if (spec.type === 'tabs') {
      var views = spec.tabs.filter(function (t) { return t.x && t.series; })
        .map(function (t) { return { x: t.x, series: t.series, prefix: spec.tabs.length > 1 ? t.label : '' }; });
      return views.length === spec.tabs.length ? table(views) : null;
    }
    if (spec.type === 'compare') {
      return table(spec.metrics.map(function (m) {
        return { x: spec.x, prefix: m.name, series: m.series.map(function (se) {
          return { name: (spec.names && spec.names[se.name]) || se.name, data: se.data };
        }) };
      }));
    }
    if (spec.type === 'scatter') {
      return [['Name', spec.xname || 'x', spec.yname || 'y']].concat(spec.points.map(function (p) { return [p.name, p.x, p.y]; }));
    }
    if (spec.type === 'heatmap') {
      return [[''].concat(spec.x)].concat(spec.y.map(function (y, i) { return [y].concat(spec.values[i]); }));
    }
    if (spec.x && spec.series) return table([{ x: spec.x, series: spec.series }]);
    return null;
  }

  function csvText(rows) {
    return rows.map(function (r) {
      return r.map(function (v) {
        if (v === null || v === undefined) return '';
        var t = String(v);
        return /[",\n]/.test(t) ? '"' + t.replace(/"/g, '""') + '"' : t;
      }).join(',');
    }).join('\n') + '\n';
  }

  // a "Data" button next to Python and MCP that downloads the plotted series
  function addDataButton(box, spec) {
    var holder = box.closest('.ft-chart-box');
    var actions = holder && holder.querySelector('.ft-chart-actions');
    if (!actions || actions.querySelector('[data-download]')) return;
    var rows;
    try { rows = csvRows(spec); } catch (e) { rows = null; }
    if (!rows) return;
    var button = document.createElement('button');
    button.type = 'button';
    button.className = 'ft-chart-action';
    button.setAttribute('data-download', '');
    button.title = 'Download the data in this chart (CSV)';
    button.innerHTML = '<i class="fas fa-download" aria-hidden="true"></i><span>Data</span>';
    button.addEventListener('click', function () {
      var url = URL.createObjectURL(new Blob([csvText(rows)], { type: 'text/csv' }));
      var a = document.createElement('a');
      a.href = url;
      a.download = box.getAttribute('data-chart') + '.csv';
      document.body.appendChild(a);
      a.click();
      a.remove();
      setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
    });
    actions.appendChild(button);
  }

  function show(box) {
    if (box.ftShown) return;
    box.ftShown = true;
    var src = box.getAttribute('data-src') || DATA;
    // a chart that carries its own data (the docs pages' example results)
    if (src === 'inline') {
      var spec = JSON.parse(box.querySelector('script[type="application/json"]').textContent);
      loadScript(ECHARTS).then(function () { draw(box, spec); }).catch(function () {
        box.innerHTML = '<p class="ft-chart__error">The chart could not be loaded.</p>';
      });
      return;
    }
    start(src).then(function (data) {
      var id = box.getAttribute('data-chart');
      if (data.charts[id]) return draw(box, data.charts[id]);
      // not in this copy of the data (a cached file from before a deploy):
      // fetch it once more past every cache, and show an error if it is still missing
      if (!fresh[src]) {
        fresh[src] = fetch(src, { cache: 'reload' }).then(function (r) { return r.json(); });
      }
      return fresh[src].then(function (d) {
        if (!d.charts[id]) throw new Error('missing chart ' + id);
        draw(box, d.charts[id]);
      });
    }).catch(function () {
      box.innerHTML = '<p class="ft-chart__error">The chart could not be loaded.</p>';
    });
  }

  // fetch ECharts and every data file the page uses once the page has loaded
  // (a chart near the screen starts them sooner), so the charts are ready by
  // the time they scroll into view without competing with the first paint
  window.addEventListener('load', function () {
    boxes.map(function (b) { return b.getAttribute('data-src') || DATA; })
      .filter(function (src, i, all) { return src !== 'inline' && all.indexOf(src) === i; })
      .forEach(function (src) { start(src).catch(function () {}); });
  });

  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { io.unobserve(e.target); show(e.target); } });
    // well ahead of the viewport: a chart grows by its subtitle, source and tabs
    // when it is drawn, and drawn out of sight that growth moves nothing the
    // reader is looking at (no layout shift)
    }, { rootMargin: '1500px 0px' });
    boxes.forEach(function (b) { io.observe(b); });
    // charts that are not reached by scrolling (a fast fling, a jump from the
    // table of contents) are drawn in the background once the page has settled,
    // one at a time and only while the browser is idle, so none stays a grey
    // placeholder and none delays the first interaction
    var idle = window.requestIdleCallback || function (fn) { return setTimeout(function () { fn({ timeRemaining: function () { return 0; } }); }, 200); };
    // they start on the reader's first scroll, click or key press (or after 8
    // seconds), so loading the page itself does no drawing beyond the first screen
    var started = false;
    function begin() {
      if (started) return;
      started = true;
      ['scroll', 'pointerdown', 'keydown'].forEach(function (t) { window.removeEventListener(t, begin); });
      var rest = boxes.slice();
      (function next() {
        idle(function () {
          var box = rest.shift();
          while (box && box.ftShown) box = rest.shift();
          if (!box) return;
          io.unobserve(box);
          show(box);
          setTimeout(next, 250);
        }, { timeout: 3000 });
      })();
    }
    window.addEventListener('load', function () {
      ['scroll', 'pointerdown', 'keydown'].forEach(function (t) { window.addEventListener(t, begin, { passive: true }); });
      setTimeout(begin, 8000);
    });
  } else {
    boxes.forEach(show);
  }

  // redraw with the new colours when the light/dark toggle is used
  new MutationObserver(function () {
    instances.forEach(function (c) { c.draw(); });
  }).observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });

  // printing (or saving as PDF): paper is white, so the page and its charts switch to
  // the light theme, charts are drawn without animation, and the theme comes back after
  var themeBeforePrint = null;
  window.addEventListener('beforeprint', function () {
    window.__ftPrinting = true;
    var root = document.documentElement;
    themeBeforePrint = root.getAttribute('data-theme');
    root.setAttribute('data-theme', 'light');
    instances.forEach(function (c) { c.draw(); });
  });
  window.addEventListener('afterprint', function () {
    window.__ftPrinting = false;
    var root = document.documentElement;
    if (themeBeforePrint === null) root.removeAttribute('data-theme'); else root.setAttribute('data-theme', themeBeforePrint);
    instances.forEach(function (c) { c.draw(); });
  });
})();
