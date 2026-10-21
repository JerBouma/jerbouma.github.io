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
  // charts only meant for the Medium images stay hidden and undrawn on the site
  var boxes = Array.prototype.slice.call(document.querySelectorAll('.ft-chart[data-chart]')).filter(function (b) {
    return !b.closest('.mcp-show__cell--medium') || window.mediumExport;
  });
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
      var isClose = spec.cloud && s.name === 'Close';
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
        showSymbol: !many && !isBar,
        symbolSize: 6,
        smooth: false,
        connectNulls: false,
        barMaxWidth: 34,
        itemStyle: { color: isClose ? css('--text-primary', '#f8fafc') : (s.color || PALETTE[i % PALETTE.length]), borderRadius: isBar && !spec.stack ? [4, 4, 0, 0] : 0 },
        lineStyle: { width: isClose ? 2.2 : 1.8, type: s.dashed ? 'dashed' : 'solid' },
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
    var legendNames = spec.series.map(function (s) { return s.name; });
    return {
      animationDuration: 600,
      color: PALETTE,
      textStyle: { fontFamily: 'inherit', color: text, fontSize: 13 },
      grid: { left: 8, right: 28, top: 44, bottom: (many ? 56 : 12) + (spec.xname ? 26 : 0), containLabel: true },
      legend: { data: legendNames, top: 0, left: 0, textStyle: { color: text, fontSize: 13 }, icon: 'roundRect', itemWidth: 12, itemHeight: 8, type: 'scroll', pageTextStyle: { color: muted } },
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
        // many bars (the portfolio tickers): show every label, slanted
        axisLabel: isBar && (spec.x.length > 10 || Math.max.apply(null, spec.x.map(function (v) { return String(v).length; })) > 8) ? { color: muted, interval: 0, rotate: 45, fontSize: 11 } : { color: muted, hideOverlap: true, fontSize: 12.5 }
      },
      yAxis: [{
        type: 'value',
        scale: !isBar && !spec.stack && !spec.series.some(function (s) { return s.area; }),
        splitLine: { lineStyle: { color: grid } },
        axisLabel: { color: muted, formatter: fmt, fontSize: 12.5 }
      }].concat(spec.series.some(function (s) { return s.axis === 1; }) ? [{
        type: 'value',
        scale: true,
        splitLine: { show: false },
        axisLabel: { color: muted, formatter: formatter(spec.format2), fontSize: 12.5 }
      }] : []),
      dataZoom: many ? [{ type: 'inside' }, { type: 'slider', height: 18, bottom: 8, borderColor: grid, fillerColor: 'rgba(56, 189, 248, 0.15)', textStyle: { color: muted }, handleStyle: { color: muted } }] : [],
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
    head.appendChild(tabs);
    var strip = document.createElement('div');
    strip.className = 'ft-dupont';
    box.appendChild(head);
    box.appendChild(strip);
    compactTabs(tabs);

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
      var inst = window.echarts.init(canvas, null, { renderer: 'canvas' });
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
    grid.className = 'ft-kpis';
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
      var inst = window.echarts.init(canvas, null, { renderer: 'canvas' });
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
      var inst = window.echarts.init(canvas, null, { renderer: 'canvas' });
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
      var inst = window.echarts.init(canvas, null, { renderer: 'canvas' });
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
    var inst = chrome(spec)(box, Math.max(340, chart.x.length * 38 + 60));
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
          min: Math.floor(Math.min.apply(null, low) * 10) / 10,
          max: Math.ceil((Math.max.apply(null, high) + 0.04) * 10) / 10
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
    var inst = chrome(chart)(box, 380);
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
        }]
      }, true);
    }
    draw();
    instances.push({ draw: draw });
  }

  // A correlation matrix as a heatmap, blue for positive, pink for negative
  function renderHeatmap(box, chart) {
    var n = chart.x.length;
    var inst = chrome(chart)(box, Math.max(260, chart.y.length * 46 + 110));
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

  function render(box, chart) {
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
    box.appendChild(head);
    box.appendChild(canvas);
    if (tabs) compactTabs(tabs);

    var instance = window.echarts.init(canvas, null, { renderer: 'canvas' });
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

  function show(box) {
    if (box.ftShown) return;
    box.ftShown = true;
    var src = box.getAttribute('data-src') || DATA;
    start(src).then(function (data) {
      var id = box.getAttribute('data-chart');
      if (data.charts[id]) return render(box, data.charts[id]);
      // not in this copy of the data (a cached file from before a deploy):
      // fetch it once more past every cache, and show an error if it is still missing
      if (!fresh[src]) {
        fresh[src] = fetch(src, { cache: 'reload' }).then(function (r) { return r.json(); });
      }
      return fresh[src].then(function (d) {
        if (!d.charts[id]) throw new Error('missing chart ' + id);
        render(box, d.charts[id]);
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
      .filter(function (src, i, all) { return all.indexOf(src) === i; })
      .forEach(function (src) { start(src).catch(function () {}); });
  });

  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { io.unobserve(e.target); show(e.target); } });
    }, { rootMargin: '300px 0px' });
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
})();
