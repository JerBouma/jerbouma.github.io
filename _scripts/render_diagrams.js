// Draws the Mermaid diagrams of a local build once, in the dark and the light theme,
// into _includes/diagrams/<hash>-dark.svg and -light.svg (see _plugins/static_diagrams.rb).
// Rerun after changing a diagram, then rebuild: a diagram without SVGs still works, it
// is just drawn in the browser with Mermaid.
//
//   (cd <build dir> && python3 -m http.server 4123 -b 127.0.0.1) &
//   NODE_PATH=<dir with playwright> CHROME=<chrome binary> node _scripts/render_diagrams.js \
//     /articles/binomial-trees.html /modelling/structure-your-model.html ...
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const OUT = path.join(__dirname, '..', '_includes', 'diagrams');
const BASE = process.env.BASE || 'http://127.0.0.1:4123';

async function drawn(page) {
  await page.waitForFunction(() => {
    const blocks = [...document.querySelectorAll('.mermaid[data-diagram]:not(.mermaid--static)')];
    return blocks.length && blocks.every(b => b.querySelector('svg') && b.getAttribute('data-processed'));
  }, null, { timeout: 30000 });
  await page.waitForTimeout(500);
}

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch({ executablePath: process.env.CHROME, args: ['--no-sandbox'] });
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  let written = 0;
  for (const url of process.argv.slice(2)) {
    await page.goto(BASE + url, { waitUntil: 'networkidle' });
    if (!(await page.$('.mermaid[data-diagram]:not(.mermaid--static)'))) { console.log(url, 'nothing to draw'); continue; }
    for (const theme of ['dark', 'light']) {
      await drawn(page);
      // switch the theme (the page redraws on that), then draw once more and wait for it
      await page.evaluate(t => document.documentElement.setAttribute('data-theme', t), theme);
      await page.waitForTimeout(1500);
      await page.evaluate(() => _renderMermaid());
      await drawn(page);
      const svgs = await page.$$eval('.mermaid[data-diagram]:not(.mermaid--static)', blocks =>
        blocks.map(b => [b.getAttribute('data-diagram'), b.querySelector('svg').outerHTML, b.querySelector('svg').id]));
      for (const [hash, svg, id] of svgs) {
        // ids unique per diagram and theme, so the two copies on a page don't share styles
        const unique = id ? svg.split(id).join(`d${hash}-${theme}`) : svg;
        fs.writeFileSync(path.join(OUT, `${hash}-${theme}.svg`), unique);
        written++;
      }
    }
    console.log(url, 'drawn');
  }
  await browser.close();
  console.log(written, 'SVGs in', OUT);
})();
