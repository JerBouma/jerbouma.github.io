/*
 * Site-wide search (_includes/site-search.html, _plugins/site_search.rb).
 *
 * Two indexes load the first time the dialog opens:
 *   search.json          one row per page: title, url, section, description,
 *                        and for a Finance Toolkit function its method name
 *   search-content.json  every page's text cut at its h2/h3 headings:
 *                        [url, anchor, heading, text]
 * A page matches on its title, method name, section or description; a section
 * matches on its heading or text and links straight to that heading. Every
 * word typed has to match. Titles weigh most, so "sharpe ratio" puts the
 * Sharpe Ratio page first and its sections and mentions elsewhere after it.
 */
(function () {
  "use strict";

  var dialog = document.getElementById("site-search");
  if (!dialog || !dialog.showModal || !window.fetch) return;
  var input = document.getElementById("site-search-input");
  var list = document.getElementById("site-search-results");
  var hint = document.getElementById("site-search-hint");
  var IDLE = 'Try "sharpe ratio", "value at risk", "risk_free_rate" or "MCP server".';
  var MAX = 20;

  var pages = null, byUrl = {}, chunks = null, loading = null, failed = false;
  var active = -1, timer = null;

  // lower case, no accents, and "get_sharpe_ratio" or "sharpe-ratio" as words
  function norm(s) {
    return (s || "").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "")
      .replace(/[_\-\/’']/g, " "); // one for one, so positions match the original text
  }

  function load() {
    if (loading) return loading;
    function get(url) { return fetch(url).then(function (r) { if (!r.ok) throw r; return r.json(); }); }
    var p1 = get(dialog.dataset.pages).then(function (rows) {
      pages = rows.map(function (r) {
        var e = { r: r, t: norm(r.t), f: norm(r.f), s: norm(r.s), d: norm(r.d) };
        e.core = e.t.replace(/ \(.*\)$/, ""); // "value at risk (var)" is an exact hit for "value at risk"
        byUrl[r.u] = e;
        return e;
      });
      run();
    });
    // the page index alone already answers most searches; the text follows
    var p2 = get(dialog.dataset.content).then(function (rows) {
      chunks = rows.map(function (c) { return { u: c[0], a: c[1], h: c[2], x: c[3], nh: norm(c[2]), nx: norm(c[3]) }; });
      run();
    });
    loading = Promise.all([p1, p2]).catch(function () { failed = true; run(); });
    return loading;
  }

  function escapeRe(w) { return w.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"); }

  // per word: starts a word (titles, headings) and is a whole word, plural allowed (text)
  function matchers(words) {
    return words.map(function (w) {
      var e = escapeRe(w);
      return { w: w, start: new RegExp("(^|[^a-z0-9])" + e), whole: new RegExp("(^|[^a-z0-9])" + e + "(e?s)?([^a-z0-9]|$)") };
    });
  }

  function scorePage(e, ms, phrase) {
    var total = 0;
    for (var i = 0; i < ms.length; i++) {
      var m = ms[i], s = 0;
      if (m.start.test(e.t)) s = 10;
      else if (e.t.indexOf(m.w) >= 0) s = 6;
      else if (m.start.test(e.f)) s = 5;
      else if (m.start.test(e.s)) s = 2;
      else if (m.whole.test(e.d)) s = 1.5;
      if (!s) return 0;
      total += s;
    }
    if (e.core === phrase) total += 30;
    else if (e.core.indexOf(phrase) === 0) total += 15;
    else if (e.core.indexOf(phrase) >= 0) total += 8;
    else if (ms.length > 1 && e.d.indexOf(phrase) >= 0) total += 3;
    // the closer the title is to the query, the higher: "MCP Server" above a long article title
    total += 10 * Math.min(1, phrase.length / e.core.length);
    return total - e.r.u.split("/").length * 0.1;
  }

  function scoreChunk(c, ms, phrase) {
    var total = 0;
    for (var i = 0; i < ms.length; i++) {
      var m = ms[i];
      if (m.start.test(c.th)) total += 3;
      else if (m.whole.test(c.nx)) total += 1;
      else return 0;
    }
    if (ms.length > 1 && (c.th.indexOf(phrase) >= 0 || c.nx.indexOf(phrase) >= 0)) total += 2;
    return total;
  }

  function search(q) {
    var phrase = norm(q).replace(/\s+/g, " ").trim();
    // "ratios" also finds "ratio"
    var words = phrase.split(" ").filter(Boolean).map(function (w) { return w.length > 4 ? w.replace(/s$/, "") : w; });
    var ms = matchers(words);
    var hits = {}, out = [];

    pages.forEach(function (e) {
      var s = scorePage(e, ms, phrase);
      if (s > 0) hits[e.r.u] = { page: e, score: s, sections: [] };
    });
    if (chunks) {
      chunks.forEach(function (c) {
        var page = byUrl[c.u];
        if (!page) return;
        // "Sharpe Ratio in Python or via the MCP" on the Sharpe Ratio page matches on its
        // text, not on repeating the page title
        if (c.th === undefined) {
          var lead = c.nh.indexOf(page.t) === 0 ? page.t : c.nh.indexOf(page.core) === 0 ? page.core : "";
          c.th = c.nh.slice(lead.length);
        }
        var s = scoreChunk(c, ms, phrase);
        if (!s) return;
        var hit = hits[c.u];
        if (!hit) hit = hits[c.u] = { page: byUrl[c.u], score: 0, sections: [] };
        hit.textScore = Math.max(hit.textScore || 0, s);
        if (c.a) hit.sections.push({ c: c, score: s, head: ms.some(function (m) { return m.start.test(c.th); }) });
        else if (!hit.intro) hit.intro = c;
      });
    }
    Object.keys(hits).forEach(function (u) {
      var hit = hits[u];
      // a page found only in its text ranks below every title hit; under a page found
      // on its title, only sections whose heading matches are worth a line of their own
      if (hit.score) hit.sections = hit.sections.filter(function (x) { return x.head; });
      else hit.score = hit.textScore;
      out.push({ kind: "page", hit: hit, score: hit.score });
      hit.sections.sort(function (a, b) { return b.score - a.score; }).slice(0, 2).forEach(function (s) {
        out.push({ kind: "section", hit: hit, c: s.c, score: Math.min(hit.score, s.score + 0.5) - 0.01 });
      });
    });
    out.sort(function (a, b) { return b.score - a.score; });
    // a section is shown right under its page when the page is listed
    var shown = [], seen = {};
    out.forEach(function (x) {
      if (x.kind === "page") {
        seen[x.hit.page.r.u] = true;
        shown.push(x);
        out.forEach(function (y) { if (y.kind === "section" && y.hit === x.hit) { y.done = true; shown.push(y); } });
      } else if (!x.done && !seen[x.hit.page.r.u]) {
        shown.push(x);
      }
    });
    return { list: shown.slice(0, MAX), words: words };
  }

  // the text around the first matched word, with every match marked
  function snippet(text, words, length) {
    var lower = norm(text), at = -1;
    for (var i = 0; i < words.length && at < 0; i++) {
      var m = new RegExp("(^|[^a-z0-9])" + escapeRe(words[i])).exec(lower);
      if (m) at = m.index + m[1].length;
    }
    var start = at > length / 3 ? text.lastIndexOf(" ", at - length / 3) + 1 : 0;
    var cut = text.slice(start, start + length);
    if (start + length < text.length) cut = cut.replace(/\s+\S*$/, "") + "…";
    return (start > 0 ? "…" : "") + cut;
  }

  function mark(node, text, words) {
    // matching runs on the normalised text, which keeps every character's position
    var lower = norm(text), ranges = [];
    words.forEach(function (w) {
      var re = new RegExp("(^|[^a-z0-9])(" + escapeRe(w) + ")", "g"), m;
      while ((m = re.exec(lower))) ranges.push([m.index + m[1].length, m.index + m[0].length]);
    });
    ranges.sort(function (a, b) { return a[0] - b[0]; });
    var pos = 0;
    ranges.forEach(function (r) {
      if (r[0] < pos) return;
      node.appendChild(document.createTextNode(text.slice(pos, r[0])));
      var em = document.createElement("mark");
      em.textContent = text.slice(r[0], r[1]);
      node.appendChild(em);
      pos = r[1];
    });
    node.appendChild(document.createTextNode(text.slice(pos)));
    return node;
  }

  function el(tag, cls) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    return n;
  }

  function render(result) {
    list.textContent = "";
    result.list.forEach(function (x, i) {
      var r = x.hit.page.r, li = el("li"), a = el("a", "site-search__item");
      a.id = "site-search-opt-" + i;
      a.setAttribute("role", "option");
      if (x.kind === "section") {
        a.href = (r.u || "/") + "#" + x.c.a;
        a.className += " site-search__item--section";
        var under = x.hit.page && result.list.some(function (y) { return y.kind === "page" && y.hit === x.hit; });
        if (!under) a.appendChild(mark(el("span", "site-search__section"), r.t, []));
        a.appendChild(mark(el("span", "site-search__title"), x.c.h, result.words));
        if (x.c.x) a.appendChild(mark(el("span", "site-search__desc"), snippet(x.c.x, result.words, 150), result.words));
        if (under) li.className = "site-search__sub";
      } else {
        a.href = r.u || "/";
        if (r.s) a.appendChild(el("span", "site-search__section")).textContent = r.s;
        a.appendChild(mark(el("span", "site-search__title"), r.t, result.words));
        // the description, or the passage of text that matched when the description doesn't say it
        var desc = r.d, intro = x.hit.intro;
        if (intro && !x.hit.page.d.split(" ").some(function (w) { return result.words.indexOf(w) >= 0; })) desc = snippet(intro.x, result.words, 160);
        if (desc) a.appendChild(mark(el("span", "site-search__desc"), desc, result.words));
      }
      li.appendChild(a);
      list.appendChild(li);
    });
  }

  function run() {
    var q = input.value.trim();
    active = -1;
    input.removeAttribute("aria-activedescendant");
    if (!q) { list.textContent = ""; say(IDLE); return; }
    if (failed && !pages) { list.textContent = ""; say("The search could not load. Please try again later."); return; }
    if (!pages) { say("Loading…"); return; }
    var result = search(q);
    render(result);
    input.setAttribute("aria-expanded", result.list.length ? "true" : "false");
    if (result.list.length) say("");
    else say(chunks || failed ? 'Nothing found for "' + q + '".' : "Searching the full text…");
  }

  function say(text) { hint.textContent = text; hint.hidden = !text; }

  function move(step) {
    var items = list.querySelectorAll(".site-search__item");
    if (!items.length) return;
    if (active >= 0) items[active].classList.remove("is-active");
    active = (active + step + items.length) % items.length;
    items[active].classList.add("is-active");
    items[active].scrollIntoView({ block: "nearest" });
    input.setAttribute("aria-activedescendant", items[active].id);
  }

  function open(text) {
    if (!dialog.open) {
      dialog.showModal();
      document.documentElement.classList.add("site-search-open");
    }
    if (typeof text === "string" && text) input.value = text;
    input.focus();
    input.select();
    load();
    run();
  }

  input.addEventListener("input", function () { clearTimeout(timer); timer = setTimeout(run, 60); });
  input.addEventListener("keydown", function (ev) {
    if (ev.key === "Escape") { ev.preventDefault(); dialog.close(); }
    else if (ev.key === "ArrowDown") { ev.preventDefault(); move(1); }
    else if (ev.key === "ArrowUp") { ev.preventDefault(); move(-1); }
    else if (ev.key === "Enter") {
      clearTimeout(timer); run();
      var items = list.querySelectorAll(".site-search__item");
      var target = items[active >= 0 ? active : 0];
      if (target) { ev.preventDefault(); dialog.close(); location.href = target.href; }
    }
  });
  // a result on the page already open only moves to the heading
  list.addEventListener("click", function (ev) { if (ev.target.closest("a")) dialog.close(); });
  dialog.addEventListener("close", function () { document.documentElement.classList.remove("site-search-open"); });
  // a click on the backdrop (the dialog itself, outside the box) closes it
  dialog.addEventListener("click", function (ev) { if (ev.target === dialog) dialog.close(); });
  dialog.querySelector(".site-search__close").addEventListener("click", function () { dialog.close(); });
  document.addEventListener("click", function (ev) {
    var b = ev.target.closest && ev.target.closest("[data-site-search]");
    if (b) { ev.preventDefault(); open(); }
  });
  document.addEventListener("keydown", function (ev) {
    var t = ev.target, typing = t && (t.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName));
    if ((ev.key === "k" && (ev.metaKey || ev.ctrlKey)) || (ev.key === "/" && !typing && !dialog.open)) {
      ev.preventDefault();
      open();
    }
  });
  // ?q=... opens the search with that text (the 404 page links to it)
  var q = new URLSearchParams(location.search).get("q");
  if (q) open(q);
  window.siteSearch = open;
})();
