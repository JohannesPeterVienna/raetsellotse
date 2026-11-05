// Browser-Test für leere Werbeplätze (node --test test_werbeplaetze.js, nach python3 build.py).
// Playwright/Chromium lädt docs/ von einem lokalen Server; adsbygoogle.js ist ein Stub, der nie eine Anzeige liefert.
// Erwartet (AdSense-Hilfe 10762946): ohne data-ad-status bleibt das <ins> sichtbar und ungeschnitten (Breite > 0,
// kein overflow:hidden), nur „Werbung“, Mindesthöhe und Abstände fehlen; "unfilled" → ins display:none;
// "filled"/"unfill-optimized" → Platz samt Beschriftung und Abstand zum Fußzeilen-Knopf.
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

function inse(seite) {
  return seite.$$eval(".ad.on ins.adsbygoogle", l => l.map(i => {
    const b = i.parentElement, ci = getComputedStyle(i), cb = getComputedStyle(b), ri = i.getBoundingClientRect();
    return { art: b.dataset.ad, display: ci.display, sicht: ci.visibility, breite: ri.width, insH: ri.height,
             boxH: b.getBoundingClientRect().height, overflow: cb.overflowX + "/" + cb.overflowY, boxSicht: cb.visibility,
             beschriftung: getComputedStyle(b, "::before").display !== "none", abstand: parseFloat(cb.marginTop) + parseFloat(cb.marginBottom), minH: cb.minHeight };
  }));
}
function ungeschnitten(l) {
  assert.ok(l.length > 0, "aktive Werbeplätze vorhanden");
  for (const x of l) {
    assert.notEqual(x.display, "none", `${x.art}: ins nicht display:none`);
    assert.equal(x.sicht, "visible", `${x.art}: ins sichtbar`);
    assert.equal(x.boxSicht, "visible", `${x.art}: Platz sichtbar`);
    assert.ok(x.breite > 0, `${x.art}: ins hat Breite`);
    assert.equal(x.overflow, "visible/visible", `${x.art}: Platz schneidet nicht ab`);
    assert.ok(x.boxH >= x.insH, `${x.art}: Platz mindestens so hoch wie das ins`);
  }
}

for (const breite of [390, 1366]) {
  for (const pfad of ["/", "/sudoku.html", "/sudoku-strategien.html"]) {
    test(`${breite} px ${pfad}: ohne Status → ins sichtbar und ungeschnitten, kein Beiwerk`, async () => {
      const { ctx, seite, fehler } = await oeffne(breite, pfad);
      const l = await inse(seite);
      ungeschnitten(l);
      assert.ok(l.every(x => !x.beschriftung && x.abstand === 0 && x.minH === "0px"), "kein „Werbung“, kein Abstand, keine Mindesthöhe");
      assert.deepEqual((await plaetze(seite)).filter(p => p.beschriftung || p.oben || p.unten), []);
      assert.deepEqual(fehler, []);
      await ctx.close();
    });
  }
}

for (const status of ["filled", "unfill-optimized"]) {
  test(`1366 px: data-ad-status=${status} → Werbeplatz mit „Werbung“ und Abstand sichtbar`, async () => {
    const { ctx, seite } = await oeffne(1366, "/");
    await seite.$$eval(".ad.on ins.adsbygoogle", (l, st) => l.forEach(i => i.setAttribute("data-ad-status", st)), status);
    const da = Object.fromEntries((await plaetze(seite)).map(p => [p.art, p]));
    assert.ok(da.superbanner && da.superbanner.hoehe >= 90 && da.superbanner.beschriftung);
    assert.equal(da.superbanner.unten, 120, "Abstand Superbanner – Fußzeilen-Knopf bleibt");
    assert.ok(da.rect && da.rect.hoehe >= 250 && da.rect.beschriftung);
    assert.ok(await seite.$$eval(".ad.on", l => l.every(b => b.classList.contains("ad--belegt"))), "Rückfall-Klasse gesetzt");
    await ctx.close();
  });
}

test("390 px: unfilled → ins display:none, kein Beiwerk; nur der gefüllte Platz erscheint", async () => {
  const { ctx, seite } = await oeffne(390, "/sudoku.html");
  await seite.$$eval(".ad.on ins.adsbygoogle", l => l.forEach(i => i.setAttribute("data-ad-status", "unfilled")));
  assert.ok((await inse(seite)).every(x => x.display === "none" && !x.beschriftung && x.boxH === 0));
  assert.deepEqual(await plaetze(seite), []);
  await seite.$eval('.ad.on[data-ad="rect"] ins.adsbygoogle', i => i.setAttribute("data-ad-status", "filled"));
  const da = await plaetze(seite);
  assert.deepEqual(da.map(p => p.art), ["rect"]);
  assert.ok(da[0].beschriftung);
  await ctx.close();
});

test("ohne :has() (Rückfall-Klassen): leer → ins sichtbar ohne Beiwerk; unfill-optimized → Beschriftung", async () => {
  const { ctx, seite } = await oeffne(1366, "/");
  await seite.evaluate(() => {
    for (const sh of document.styleSheets) { try { for (let k = sh.cssRules.length - 1; k >= 0; k--) if (sh.cssRules[k].cssText.includes(":has(")) sh.deleteRule(k); } catch (e) {} }
    document.documentElement.classList.add("kein-has");
  });
  let l = await inse(seite);
  ungeschnitten(l);
  assert.ok(l.every(x => !x.beschriftung && x.abstand === 0));
  await seite.$$eval(".ad.on ins.adsbygoogle", l => l.forEach(i => i.setAttribute("data-ad-status", "unfill-optimized")));
  l = await inse(seite);
  assert.ok(l.every(x => x.beschriftung));
  await ctx.close();
});
