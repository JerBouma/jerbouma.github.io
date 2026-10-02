// Renders the share image (og:image) of every page listed in
// _site/assets/images/share/manifest.json (written by _plugins/share_images.rb)
// with the template in _scripts/share-banner.html. Runs in the deploy
// workflow after the Jekyll build, like build-cv-pdf.js.
//
// If an image can't be rendered, the default banner is copied in its place so
// no page ever points to a missing image.
const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");

const site = path.resolve(__dirname, "..", "_site");
const dir = path.join(site, "assets/images/share");
const fallback = path.join(site, "assets/images/default/share-banner.jpg");
const items = JSON.parse(fs.readFileSync(path.join(dir, "manifest.json"), "utf8"));
const photo = "data:image/jpeg;base64," + fs.readFileSync(path.join(site, "assets/images/default/bio-photo.jpg")).toString("base64");

(async () => {
  let rendered = 0, copied = 0;
  let browser;
  try {
    browser = await chromium.launch({ executablePath: process.env.CHROME || undefined, args: ["--no-sandbox"] });
    const page = await (await browser.newContext({ viewport: { width: 1200, height: 630 } })).newPage();
    await page.goto("file://" + path.join(__dirname, "share-banner.html"), { waitUntil: "networkidle" });
    await page.evaluate((src) => { document.getElementById("photo").src = src; }, photo);
    await page.evaluate(() => document.fonts.ready);
    for (const item of items) {
      const file = path.join(dir, `${item.key}.jpg`);
      try {
        await page.evaluate((i) => window.fill(i), item);
        await page.screenshot({ path: file, type: "jpeg", quality: 90 });
        rendered++;
      } catch (e) {
        fs.copyFileSync(fallback, file); copied++;
      }
    }
  } catch (e) {
    console.error("Rendering failed:", e.message);
  } finally {
    if (browser) await browser.close();
  }
  for (const item of items) {
    const file = path.join(dir, `${item.key}.jpg`);
    if (!fs.existsSync(file)) { fs.copyFileSync(fallback, file); copied++; }
  }
  console.log(`Share images: ${rendered} rendered, ${copied} default`);
})();
