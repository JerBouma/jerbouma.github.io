// Prints the CV page (/resume/cv, rendered from _data/resume.yml) to a PDF.
//
//   node _scripts/build-cv-pdf.js                 -> _site/assets/files/jeroen-bouma-cv.pdf
//   node _scripts/build-cv-pdf.js --update-repo   -> also refreshes the copy in assets/files/
//
// Run it after `jekyll build`. The deploy workflow does this on every push to
// main, so the PDF on the site always matches the resume; the copy committed
// in assets/files/ is only a fallback for when that step cannot run.
//
// Needs Playwright with Chromium (npm install playwright && npx playwright
// install chromium). Set CHROME to use a Chromium binary of your own.

const http = require("http");
const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");

const root = path.resolve(__dirname, "..");
const site = path.join(root, "_site");
const output = path.join(site, "assets", "files", "jeroen-bouma-cv.pdf");
const repoCopy = path.join(root, "assets", "files", "jeroen-bouma-cv.pdf");

const types = {
  ".html": "text/html; charset=utf-8", ".css": "text/css", ".js": "text/javascript",
  ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".svg": "image/svg+xml",
  ".webp": "image/webp", ".woff2": "font/woff2",
};

// a minimal static server for _site, with GitHub Pages' extensionless URLs
function serve() {
  const server = http.createServer((req, res) => {
    let file = path.join(site, decodeURIComponent(req.url.split("?")[0]));
    if (!file.startsWith(site)) { res.writeHead(403).end(); return; }
    // like GitHub Pages, /resume/cv is cv.html; the folder of the same name
    // only holds the trailing-slash redirect
    if (fs.existsSync(file + ".html")) file += ".html";
    else if (fs.existsSync(file) && fs.statSync(file).isDirectory()) file = path.join(file, "index.html");
    if (!fs.existsSync(file)) { res.writeHead(404).end(); return; }
    res.writeHead(200, { "Content-Type": types[path.extname(file)] || "application/octet-stream" });
    fs.createReadStream(file).pipe(res);
  });
  return new Promise((resolve) => server.listen(0, "127.0.0.1", () => resolve(server)));
}

(async () => {
  if (!fs.existsSync(path.join(site, "resume", "cv.html"))) {
    console.error("_site/resume/cv.html not found: run jekyll build first");
    process.exit(1);
  }
  const server = await serve();
  const { port } = server.address();
  const browser = await chromium.launch(process.env.CHROME ? { executablePath: process.env.CHROME } : {});
  try {
    const page = await browser.newPage();
    await page.goto(`http://127.0.0.1:${port}/resume/cv`, { waitUntil: "networkidle", timeout: 90000 });
    await page.evaluate(() => document.fonts.ready);
    fs.mkdirSync(path.dirname(output), { recursive: true });
    await page.pdf({ path: output, format: "A4", printBackground: true, preferCSSPageSize: true });
    console.log(`CV written to ${path.relative(root, output)}`);
    if (process.argv.includes("--update-repo")) {
      fs.mkdirSync(path.dirname(repoCopy), { recursive: true });
      fs.copyFileSync(output, repoCopy);
      console.log(`and copied to ${path.relative(root, repoCopy)}`);
    }
  } finally {
    await browser.close();
    server.close();
  }
})().catch((error) => { console.error(error); process.exit(1); });
