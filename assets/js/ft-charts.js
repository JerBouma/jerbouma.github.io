/*
 * Interactive charts on /projects/financetoolkit.
 *
 * Every <div class="ft-chart" data-chart="…"> is filled from
 * /assets/data/financetoolkit-charts.json (written by
 * _scripts/financetoolkit_charts.py) and drawn with ECharts. Charts follow the
 * site's light/dark theme, resize with the page and are only drawn once they
 * scroll into view.
 */
(function () {
  var boxes = Array.prototype.slice.call(document.querySelectorAll('.ft-chart[data-chart]'));
  if (!boxes.length) return;

  var ECHARTS = 'https://cdn.jsdelivr.net/npm/echarts@5.5.1/dist/echarts.min.js';
  var DATA = '/assets/data/financetoolkit-charts.json';
  var PALETTE = ['#38bdf8', '#818cf8', '#f97316', '#34d399', '#f472b6', '#fbbf24', '#a78bfa'];
  var instances = [];

  function loadScript(src) {
    return new Promise(function (resolve, reject) {
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

  function formatter(fmt) {
    return function (v) {
      if (v === null || v === undefined || isNaN(v)) return '–';
      switch (fmt) {
        case 'percent': return (v * 100).toFixed(Math.abs(v) < 0.1 ? 2 : 1) + '%';
        case 'billions': return '$' + v.toFixed(0) + 'B';
        case 'multiple': return v.toFixed(2) + 'x';
        case 'price': return '$' + v.toFixed(2);
        case 'ratio': return v.toFixed(2);
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
    var many = spec.x.length > 40;
    var series = spec.series.map(function (s, i) {
      var isClose = spec.cloud && s.name === 'Close';
      return {
        name: s.name,
        type: isBar ? 'bar' : 'line',
        data: s.data,
        showSymbol: !many && !isBar,
        symbolSize: 6,
        smooth: false,
        connectNulls: false,
        barMaxWidth: 34,
        itemStyle: { color: isClose ? css('--text-primary', '#f8fafc') : PALETTE[i % PALETTE.length], borderRadius: isBar ? [4, 4, 0, 0] : 0 },
        lineStyle: { width: isClose ? 2.2 : 1.8 },
        emphasis: { focus: 'series' }
      };
    });
    if (spec.cloud) series = cloudSeries(spec).concat(series);
    var legendNames = spec.series.map(function (s) { return s.name; });
    return {
      animationDuration: 600,
      color: PALETTE,
      textStyle: { fontFamily: 'inherit', color: text },
      grid: { left: 8, right: 28, top: 44, bottom: (many ? 56 : 12) + (spec.xname ? 26 : 0), containLabel: true },
      legend: { data: legendNames, top: 0, left: 0, textStyle: { color: text, fontSize: 12 }, icon: 'roundRect', itemWidth: 12, itemHeight: 8, type: 'scroll', pageTextStyle: { color: muted } },
      tooltip: {
        trigger: 'axis',
        backgroundColor: css('--masthead-bg', '#0f1115'),
        borderColor: grid,
        textStyle: { color: css('--text-primary', '#f8fafc'), fontSize: 12 },
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
        // many bars (the portfolio tickers): show every label, slanted
        axisLabel: isBar && spec.x.length > 10 ? { color: muted, interval: 0, rotate: 45, fontSize: 11 } : { color: muted, hideOverlap: true }
      },
      yAxis: {
        type: 'value',
        scale: !isBar,
        splitLine: { lineStyle: { color: grid } },
        axisLabel: { color: muted, formatter: fmt }
      },
      dataZoom: many ? [{ type: 'inside' }, { type: 'slider', height: 18, bottom: 8, borderColor: grid, fillerColor: 'rgba(56, 189, 248, 0.15)', textStyle: { color: muted }, handleStyle: { color: muted } }] : [],
      series: series
    };
  }

  function render(box, chart) {
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
    box.appendChild(head);
    box.appendChild(canvas);

    var instance = window.echarts.init(canvas, null, { renderer: 'canvas' });
    var current = 0;
    function draw() { instance.setOption(option(specs[current]), true); }
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

  var ready = null;
  function start() {
    if (!ready) {
      ready = Promise.all([loadScript(ECHARTS), fetch(DATA).then(function (r) { return r.json(); })])
        .then(function (r) { return r[1]; });
    }
    return ready;
  }

  function show(box) {
    start().then(function (data) {
      var chart = data.charts[box.getAttribute('data-chart')];
      if (chart) render(box, chart);
    }).catch(function () {
      box.innerHTML = '<p class="ft-chart__error">The chart could not be loaded.</p>';
    });
  }

  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { io.unobserve(e.target); show(e.target); } });
    }, { rootMargin: '300px 0px' });
    boxes.forEach(function (b) { io.observe(b); });
  } else {
    boxes.forEach(show);
  }

  // redraw with the new colours when the light/dark toggle is used
  new MutationObserver(function () {
    instances.forEach(function (c) { c.draw(); });
  }).observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
})();
