/**
 * Client-side Jupyter Notebook renderer.
 *
 * Usage:
 *   <div id="notebook-container" data-notebook-src="/assets/notebooks/my.ipynb"></div>
 *   <script src="/assets/js/notebookRenderer.js"></script>
 *
 * Dependencies loaded from CDN:
 *   - marked.js   (Markdown → HTML)
 *   - KaTeX       (LaTeX math rendering)
 *
 * Python syntax highlighting is built-in and produces Rouge-compatible
 * CSS class names so the same VS Code Dark+ theme used for docs code
 * blocks also colours notebook cells identically.
 */

(function () {
  "use strict";

  /* ── helpers ───────────────────────────────────────────── */

  function escapeHtml(str) {
    var d = document.createElement("div");
    d.appendChild(document.createTextNode(str));
    return d.innerHTML;
  }

  /* ── Python → Rouge HTML tokenizer ─────────────────────── */

  var PY_KEYWORDS = {};
  "False None True and as assert async await break class continue def del elif else except finally for from global if import in is lambda nonlocal not or pass raise return try while with yield".split(" ").forEach(function (w) { PY_KEYWORDS[w] = 1; });

  var PY_BUILTINS = {};
  "abs all any ascii bin bool breakpoint bytearray bytes callable chr classmethod compile complex delattr dict dir divmod enumerate eval exec filter float format frozenset getattr globals hasattr hash help hex id input int isinstance issubclass iter len list locals map max memoryview min next object oct open ord pow print property range repr reversed round set setattr slice sorted staticmethod str sum super tuple type vars zip display __import__".split(" ").forEach(function (w) { PY_BUILTINS[w] = 1; });

  /** Wrap text in a Rouge-compatible <span>. */
  function w(cls, text) {
    return '<span class="' + cls + '">' + escapeHtml(text) + "</span>";
  }

  /**
   * Tokenize Python source and return HTML with Rouge CSS class names.
   * Produces the exact same classes as Jekyll's Rouge highlighter so the
   * existing .highlight token CSS rules apply without any extra overrides.
   */
  function highlightPython(src) {
    var out = "";
    var i = 0;
    var len = src.length;
    var prevKw = "";

    while (i < len) {
      var rest = src.slice(i);
      var m;

      // 1. Triple-quoted strings (with optional prefix)
      if ((m = rest.match(/^([brufBRUF]{0,2})("""|''')([\s\S]*?)\2/))) {
        if (m[1]) out += w("sa", m[1]);
        out += w("sd", m[2] + m[3] + m[2]);
        i += m[0].length; prevKw = "";
      }
      // 2. Single-line comments
      else if (rest[0] === "#" && (m = rest.match(/^#[^\n]*/))) {
        out += w("c1", m[0]);
        i += m[0].length;
      }
      // 3. Double-quoted strings (with optional prefix)
      else if ((m = rest.match(/^([brufBRUF]{0,2})"((?:\\.|[^"\n])*)"/))) {
        if (m[1]) out += w("sa", m[1]);
        out += w("sh", '"') + (m[2] ? w("s", m[2]) : "") + w("sh", '"');
        i += m[0].length; prevKw = "";
      }
      // 4. Single-quoted strings (with optional prefix)
      else if ((m = rest.match(/^([brufBRUF]{0,2})'((?:\\.|[^'\n])*)'/))) {
        if (m[1]) out += w("sa", m[1]);
        out += w("sh", "'") + (m[2] ? w("s", m[2]) : "") + w("sh", "'");
        i += m[0].length; prevKw = "";
      }
      // 5. Decorators
      else if (rest[0] === "@" && (m = rest.match(/^@[\w.]+/))) {
        out += w("nd", m[0]);
        i += m[0].length; prevKw = "";
      }
      // 6. Identifiers, keywords, builtins
      else if (/[A-Za-z_]/.test(rest[0]) && (m = rest.match(/^[A-Za-z_]\w*/))) {
        var word = m[0];
        i += word.length;
        if (PY_KEYWORDS[word]) {
          if (word === "True" || word === "False" || word === "None") {
            out += w("kc", word);
          } else if (word === "from" || word === "import") {
            out += w("kn", word);
          } else {
            out += w("k", word);
          }
          prevKw = word;
        } else if (word === "self" || word === "cls") {
          out += w("bp", word); prevKw = "";
        } else if (PY_BUILTINS[word]) {
          out += w("nb", word); prevKw = "";
        } else {
          // Context-aware classification
          var ahead = src.slice(i).match(/^\s*/)[0];
          var nextCh = src[i + ahead.length] || "";
          if (prevKw === "def") {
            out += w("nf", word);
          } else if (prevKw === "class") {
            out += w("nc", word);
          } else if (nextCh === "(") {
            out += w(word[0] >= "A" && word[0] <= "Z" ? "nc" : "nf", word);
          } else {
            out += w("n", word);
          }
          prevKw = "";
        }
      }
      // 7. Numbers
      else if (/\d/.test(rest[0]) && (m = rest.match(/^(?:0[xXoObB][\da-fA-F_]+|\d[\d_]*\.?[\d_]*(?:[eE][+-]?\d+)?j?)/))) {
        out += w(m[0].indexOf(".") >= 0 || /[eE]/.test(m[0]) ? "mf" : "mi", m[0]);
        i += m[0].length; prevKw = "";
      }
      // 8. Operators (but NOT dot — dot is punctuation per Rouge)
      else if ((m = rest.match(/^\*\*=?|^>>=?|^<<=?|^!=|^\/\/=?|^->|^[+\-*\/%&|^~<>=!]=?/))) {
        out += w("o", m[0]);
        i += m[0].length; prevKw = "";
      }
      // 9. Punctuation (including dot)
      else if (/[()[\]{},;:.]/.test(rest[0])) {
        out += w("p", rest[0]);
        i++; prevKw = "";
      }
      // 10. Whitespace (preserve, don't reset prevKw)
      else if (/\s/.test(rest[0])) {
        out += rest[0]; i++;
      }
      // 11. Anything else
      else {
        out += escapeHtml(rest[0]);
        i++; prevKw = "";
      }
    }

    return out;
  }

  /** Join multi-line source arrays into a single string. */
  function joinSource(source) {
    return Array.isArray(source) ? source.join("") : source || "";
  }

  /** Render LaTeX $...$ and $$...$$ using KaTeX if available. */
  function renderMath(html) {
    if (typeof katex === "undefined") return html;
    // Display math: $$...$$
    html = html.replace(/\$\$([\s\S]+?)\$\$/g, function (_, tex) {
      try {
        return katex.renderToString(tex.trim(), { displayMode: true, throwOnError: false });
      } catch (e) {
        return '<span class="nb-math-error">' + escapeHtml(tex) + "</span>";
      }
    });
    // Inline math: $...$  (but not $$)
    html = html.replace(/\$([^\$\n]+?)\$/g, function (_, tex) {
      try {
        return katex.renderToString(tex.trim(), { displayMode: false, throwOnError: false });
      } catch (e) {
        return '<span class="nb-math-error">' + escapeHtml(tex) + "</span>";
      }
    });
    return html;
  }

  /** Convert ANSI escape codes to styled spans (basic subset). */
  function ansiToHtml(text) {
    var colors = {
      30: "#4e4e4e", 31: "#f87171", 32: "#4ade80", 33: "#facc15",
      34: "#60a5fa", 35: "#c084fc", 36: "#22d3ee", 37: "#e2e8f0",
      90: "#6b7280", 91: "#fca5a5", 92: "#86efac", 93: "#fde68a",
      94: "#93c5fd", 95: "#d8b4fe", 96: "#67e8f9", 97: "#f8fafc"
    };
    var escaped = escapeHtml(text);
    return escaped.replace(/\x1b\[([0-9;]*)m/g, function (_, codes) {
      if (!codes || codes === "0") return "</span>";
      var parts = codes.split(";");
      var style = "";
      for (var i = 0; i < parts.length; i++) {
        var c = parseInt(parts[i], 10);
        if (c === 1) style += "font-weight:bold;";
        else if (c === 3) style += "font-style:italic;";
        else if (c === 4) style += "text-decoration:underline;";
        else if (colors[c]) style += "color:" + colors[c] + ";";
        else if (c >= 40 && c <= 47) style += "background:" + colors[c - 10] + ";";
      }
      return '<span style="' + style + '">';
    });
  }

  /* ── CDN dependency loader ─────────────────────────────── */

  var CDN_DEPS = [
    { id: "marked", test: function () { return typeof marked !== "undefined"; },
      src: "https://cdn.jsdelivr.net/npm/marked@15/marked.min.js" },
    { id: "katex-css", test: function () { return true; },
      href: "https://cdn.jsdelivr.net/npm/katex@0.16/dist/katex.min.css", rel: "stylesheet" },
    { id: "katex", test: function () { return typeof katex !== "undefined"; },
      src: "https://cdn.jsdelivr.net/npm/katex@0.16/dist/katex.min.js" }
  ];

  function loadDeps(callback) {
    var pending = CDN_DEPS.length;
    var loaded = {};

    function tick(id) {
      loaded[id] = true;
      // Process deps that depend on others
      CDN_DEPS.forEach(function (d) {
        if (d.after && loaded[d.after] && !loaded[d.id + "-started"]) {
          loaded[d.id + "-started"] = true;
          loadOne(d);
        }
      });
      pending--;
      if (pending <= 0) callback();
    }

    function loadOne(dep) {
      if (dep.after && !loaded[dep.after]) return; // wait
      if (dep.href) {
        // CSS
        if (!document.querySelector('link[href="' + dep.href + '"]')) {
          var link = document.createElement("link");
          link.rel = dep.rel || "stylesheet";
          link.href = dep.href;
          document.head.appendChild(link);
        }
        tick(dep.id);
        return;
      }
      if (dep.test()) { tick(dep.id); return; }
      var s = document.createElement("script");
      s.src = dep.src;
      s.onload = function () { tick(dep.id); };
      s.onerror = function () { tick(dep.id); }; // continue even if CDN fails
      document.head.appendChild(s);
    }

    CDN_DEPS.forEach(function (dep) {
      if (!dep.after) loadOne(dep);
    });
  }

  /* ── cell renderers ────────────────────────────────────── */

  function renderMarkdownCell(cell) {
    var src = joinSource(cell.source);
    if (!src.trim()) return "";
    var html = typeof marked !== "undefined" ? marked.parse(src) : "<p>" + escapeHtml(src) + "</p>";
    html = renderMath(html);
    return '<div class="nb-cell nb-markdown-cell">' + html + "</div>";
  }

  function renderCodeCell(cell) {
    var src = joinSource(cell.source);
    var execCount = cell.execution_count;
    var label = execCount != null ? "[" + execCount + "]" : "[ ]";

    // Highlight code with built-in Rouge-compatible Python tokenizer
    var highlighted = highlightPython(src);

    var html = '<div class="nb-cell nb-code-cell">';
    html += '<div class="nb-input">';
    html += '<div class="nb-prompt nb-input-prompt">' + escapeHtml(label) + "</div>";
    html += '<div class="nb-source highlight"><pre><code>' + highlighted + "</code></pre></div>";
    html += "</div>";

    // Outputs — wrapped in a collapsible details block
    if (cell.outputs && cell.outputs.length) {
      var outputsHtml = '';
      for (var i = 0; i < cell.outputs.length; i++) {
        outputsHtml += renderOutput(cell.outputs[i], execCount);
      }
      html += '<details class="nb-output-details">';
      html += '<summary class="nb-output-summary"><span class="nb-output-summary__icon"></span>Show output</summary>';
      html += '<div class="nb-output-area">' + outputsHtml + '</div>';
      html += '</details>';
    }

    html += "</div>";
    return html;
  }

  function renderOutput(output, execCount) {
    var html = "";

    if (output.output_type === "stream") {
      var text = joinSource(output.text);
      html += '<div class="nb-output nb-stream nb-stream-' + (output.name || "stdout") + '">';
      html += "<pre>" + ansiToHtml(text) + "</pre></div>";
      return html;
    }

    if (output.output_type === "error") {
      var tb = (output.traceback || []).join("\n");
      html += '<div class="nb-output nb-error"><pre>' + ansiToHtml(tb) + "</pre></div>";
      return html;
    }

    // execute_result or display_data
    var data = output.data || {};
    var label = "";

    if (output.output_type === "execute_result" && execCount != null) {
      label = '<div class="nb-prompt nb-output-prompt">[' + execCount + "]</div>";
    }

    // Priority order for mime types
    if (data["text/html"]) {
      // Strip embedded <style> tags (pandas DataFrames include scoped styles
      // that leak globally when injected into the page DOM)
      var rawHtml = joinSource(data["text/html"])
        .replace(/<style[^>]*>[\s\S]*?<\/style>/gi, "");
      html += '<div class="nb-output nb-html-output">' + label;
      html += '<div class="nb-output-content">' + rawHtml + "</div></div>";
    } else if (data["image/svg+xml"]) {
      var svg = joinSource(data["image/svg+xml"]);
      html += '<div class="nb-output nb-image-output">' + label;
      html += '<div class="nb-output-content">' + svg + "</div></div>";
    } else if (data["image/png"]) {
      var png = joinSource(data["image/png"]).replace(/\s/g, "");
      html += '<div class="nb-output nb-image-output">' + label;
      html += '<div class="nb-output-content"><img src="data:image/png;base64,' + png + '" alt="output"></div></div>';
    } else if (data["image/jpeg"]) {
      var jpg = joinSource(data["image/jpeg"]).replace(/\s/g, "");
      html += '<div class="nb-output nb-image-output">' + label;
      html += '<div class="nb-output-content"><img src="data:image/jpeg;base64,' + jpg + '" alt="output"></div></div>';
    } else if (data["application/javascript"]) {
      // Skip JS outputs for security
    } else if (data["text/plain"]) {
      var plain = joinSource(data["text/plain"]);
      html += '<div class="nb-output nb-text-output">' + label;
      html += '<div class="nb-output-content"><pre>' + ansiToHtml(plain) + "</pre></div></div>";
    }

    return html;
  }

  function renderRawCell(cell) {
    var src = joinSource(cell.source);
    if (!src.trim()) return "";
    return '<div class="nb-cell nb-raw-cell"><pre>' + escapeHtml(src) + "</pre></div>";
  }

  /* ── main render function ─────────────────────────────── */

  function renderNotebook(nb, container) {
    var cells = nb.cells || [];
    var parts = [];

    for (var i = 0; i < cells.length; i++) {
      var cell = cells[i];
      var type = cell.cell_type;
      if (type === "markdown") parts.push(renderMarkdownCell(cell));
      else if (type === "code") parts.push(renderCodeCell(cell));
      else if (type === "raw") parts.push(renderRawCell(cell));
    }

    container.innerHTML = '<div class="nb-notebook">' + parts.join("") + "</div>";
  }

  /* ── bootstrap ─────────────────────────────────────────── */

  function init() {
    var containers = document.querySelectorAll("[data-notebook-src]");
    if (!containers.length) return;

    loadDeps(function () {
      // Configure marked
      if (typeof marked !== "undefined") {
        marked.setOptions({ gfm: true, breaks: false });
      }

      containers.forEach(function (container) {
        var src = container.getAttribute("data-notebook-src");
        container.innerHTML = '<div class="nb-loading"><div class="nb-spinner"></div><span>Loading notebook…</span></div>';

        fetch(src)
          .then(function (r) {
            if (!r.ok) throw new Error("HTTP " + r.status);
            return r.json();
          })
          .then(function (nb) {
            renderNotebook(nb, container);
          })
          .catch(function (err) {
            container.innerHTML =
              '<div class="nb-error-msg"><i class="fas fa-exclamation-triangle"></i> ' +
              "Failed to load notebook: " + escapeHtml(err.message) + "</div>";
          });
      });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
