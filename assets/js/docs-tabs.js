/*
 * Tabs on the Finance Toolkit method pages: Chart and Table for the example's
 * result, Python and the MCP question for how to get it. The first panel shows;
 * a button shows its own panel and hides the others.
 */
(function () {
  Array.prototype.forEach.call(document.querySelectorAll('.docs-tabs'), function (box) {
    var buttons = box.querySelectorAll(':scope > .docs-tabs__bar > .docs-tabs__tab');
    var panels = box.querySelectorAll(':scope > .docs-tabs__panel');
    Array.prototype.forEach.call(buttons, function (button, i) {
      button.addEventListener('click', function () {
        Array.prototype.forEach.call(buttons, function (b, j) {
          b.classList.toggle('is-active', i === j);
          b.setAttribute('aria-selected', String(i === j));
        });
        Array.prototype.forEach.call(panels, function (p, j) { p.hidden = i !== j; });
      });
    });
  });
})();
