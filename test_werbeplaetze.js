// Browser-Test für leere Werbeplätze (node --test test_werbeplaetze.js, nach python3 build.py).
// Playwright/Chromium lädt docs/ von einem lokalen Server; adsbygoogle.js ist ein Stub, der nie eine Anzeige liefert.
// Erwartet: ohne data-ad-status="filled" kein sichtbarer Werbeplatz (keine Höhe, kein Abstand, kein „Werbung“);
// mit "filled" erscheint der Platz samt Beschriftung und Abstand zum Fußzeilen-Knopf.
const test = require("node:test");
const assert = require("node:assert/strict");
const http = require("http");
const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");

const DOCS = path.join(__dirname, "docs");
const ARTEN = { ".html": "text/html; charset=utf-8", ".js": "text/javascript", ".css": "text/css", ".woff2": "font/woff2", ".svg": "image/svg+xml", ".png": "image/png" };
let server, browser, basis;

test.before(async () => {
  server = http.createServer((req, res) => {
    const datei = path.join(DOCS, decodeURIComponent(req.url.split("?")[0]).replace(/\/$/, "/index.html"));
    if (!datei.startsWith(DOCS) || !fs.existsSync(datei)) { res.writeHead(404); return res.end(); }
    res.writeHead(200, { "content-type": ARTEN[path.extname(datei)] || "application/octet-stream" });
    res.end(fs.readFileSync(datei));
  });
  await new Promise(r => server.listen(0, "127.0.0.1", r));
  basis = `http://127.0.0.1:${server.address().port}`;
  browser = await chromium.launch();
});
test.after(async () => { await browser.close(); server.close(); });

async function oeffne(breite, pfad) {
  const ctx = await browser.newContext({ viewport: { width: breite, height: 900 } });
  await ctx.route(/^https?:\/\/(?!127\.0\.0\.1)/, r => r.fulfill({ status: 200, contentType: "text/javascript", body: "/* Stub: keine Anzeige */" }));
  const seite = await ctx.newPage();
  const fehler = [];
  seite.on("pageerror", e => fehler.push(e.message));
  await seite.goto(basis + pfad);
  await seite.waitForFunction(() => document.querySelector(".ad.on ins.adsbygoogle"));
  return { ctx, seite, fehler };
}

function plaetze(seite) {
  return seite.$$eval(".ad", liste => liste.map(b => {
    const cs = getComputedStyle(b);
    if (cs.display === "none") return null;
    const hoehe = b.getBoundingClientRect().height;
    return { art: b.dataset.ad, hoehe, oben: parseFloat(cs.marginTop), unten: parseFloat(cs.marginBottom),
             beschriftung: hoehe > 0 && getComputedStyle(b, "::before").display !== "none" };
  }).filter(p => p && (p.hoehe > 0 || p.oben > 0 || p.unten > 0 || p.beschriftung)));
}

for (const breite of [390, 1366]) {
  for (const pfad of ["/", "/sudoku.html", "/sudoku-strategien.html"]) {
    test(`${breite} px ${pfad}: Stub liefert nichts → kein Werbeplatz sichtbar`, async () => {
      const { ctx, seite, fehler } = await oeffne(breite, pfad);
      assert.deepEqual(await plaetze(seite), []);
      assert.deepEqual(fehler, []);
      await ctx.close();
    });
  }
}

test("1366 px: data-ad-status=filled → Werbeplatz mit „Werbung“ und Abstand sichtbar", async () => {
  const { ctx, seite } = await oeffne(1366, "/");
  await seite.$$eval(".ad.on ins.adsbygoogle", l => l.forEach(i => i.setAttribute("data-ad-status", "filled")));
  const da = Object.fromEntries((await plaetze(seite)).map(p => [p.art, p]));
  assert.ok(da.superbanner && da.superbanner.hoehe >= 90 && da.superbanner.beschriftung);
  assert.equal(da.superbanner.unten, 120, "Abstand Superbanner – Fußzeilen-Knopf bleibt");
  assert.ok(da.rect && da.rect.hoehe >= 250);
  assert.ok(await seite.$$eval(".ad.on", l => l.every(b => b.classList.contains("ad--belegt"))), "Rückfall-Klasse gesetzt");
  await ctx.close();
});

test("390 px: unfilled bleibt zu, nur der gefüllte Platz erscheint", async () => {
  const { ctx, seite } = await oeffne(390, "/sudoku.html");
  await seite.$$eval(".ad.on ins.adsbygoogle", l => l.forEach(i => i.setAttribute("data-ad-status", "unfilled")));
  assert.deepEqual(await plaetze(seite), []);
  await seite.$eval('.ad.on[data-ad="rect"] ins.adsbygoogle', i => i.setAttribute("data-ad-status", "filled"));
  assert.deepEqual((await plaetze(seite)).map(p => p.art), ["rect"]);
  await ctx.close();
});
