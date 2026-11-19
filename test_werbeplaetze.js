// Browser-Test für leere Werbeplätze (node --test test_werbeplaetze.js, nach python3 build.py).
// Playwright/Chromium lädt docs/ von einem lokalen Server; adsbygoogle.js ist ein Stub, der nie eine Anzeige liefert.
// Erwartet (AdSense-Hilfe 10762946): ohne data-ad-status bleibt das <ins> sichtbar und ungeschnitten (Breite > 0,
// kein overflow:hidden), nur „Werbung“, Mindesthöhe und Abstände fehlen; "unfilled" → ins display:none;
// "filled"/"unfill-optimized" → Platz samt Beschriftung.
// Ausnahme oberster Platz (.ad--oben, Streifen unter der Kopfzeile): Seine Höhe ist von Anfang an reserviert, damit beim Füllen
// nichts springt; nur die Beschriftung erscheint erst bei "filled". Zweiter Teil: Lage, Abstände, Sprung (CLS), Sitemap.
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
    return { art: b.dataset.ad, reserviert: b.classList.contains("ad--oben"), hoehe, oben: parseFloat(cs.marginTop), unten: parseFloat(cs.marginBottom),
             beschriftung: hoehe > 0 && getComputedStyle(b, "::before").display !== "none" };
  }).filter(p => p && (p.hoehe > 0 || p.oben > 0 || p.unten > 0 || p.beschriftung)));
}

function inse(seite) {
  return seite.$$eval(".ad.on ins.adsbygoogle", l => l.map(i => {
    const b = i.parentElement, ci = getComputedStyle(i), cb = getComputedStyle(b), ri = i.getBoundingClientRect();
    return { art: b.dataset.ad, reserviert: b.classList.contains("ad--oben"), display: ci.display, sicht: ci.visibility, breite: ri.width, insH: ri.height,
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
      assert.ok(l.every(x => !x.beschriftung), "keine Beschriftung ohne Anzeige");
      assert.ok(l.filter(x => !x.reserviert).every(x => x.abstand === 0 && x.minH === "0px"), "kein Abstand, keine Mindesthöhe");
      assert.equal(l.filter(x => x.reserviert).length, 1, "genau ein reservierter Platz oben");
      assert.deepEqual((await plaetze(seite)).filter(p => !p.reserviert && (p.beschriftung || p.oben || p.unten)), []);
      assert.deepEqual(fehler, []);
      await ctx.close();
    });
  }
}

for (const status of ["filled", "unfill-optimized"]) {
  test(`1366 px: data-ad-status=${status} → Werbeplatz mit „Werbung“ und Abstand sichtbar`, async () => {
    const { ctx, seite } = await oeffne(1366, "/");
    const vorher = (await plaetze(seite)).find(p => p.art === "superbanner").hoehe;
    await seite.$$eval(".ad.on ins.adsbygoogle", (l, st) => l.forEach(i => i.setAttribute("data-ad-status", st)), status);
    const da = Object.fromEntries((await plaetze(seite)).map(p => [p.art, p]));
    assert.ok(da.superbanner && da.superbanner.hoehe >= 90 && da.superbanner.beschriftung);
    assert.equal(da.superbanner.hoehe, vorher, "oberster Platz: Höhe schon vor dem Füllen reserviert");
    assert.ok(da.rect && da.rect.hoehe >= 250 && da.rect.beschriftung);
    assert.ok(await seite.$$eval(".ad.on", l => l.every(b => b.classList.contains("ad--belegt"))), "Rückfall-Klasse gesetzt");
    await ctx.close();
  });
}

test("390 px: unfilled → ins display:none, kein Beiwerk; nur der gefüllte Platz erscheint", async () => {
  const { ctx, seite } = await oeffne(390, "/sudoku.html");
  await seite.$$eval(".ad.on ins.adsbygoogle", l => l.forEach(i => i.setAttribute("data-ad-status", "unfilled")));
  assert.ok((await inse(seite)).every(x => x.display === "none" && !x.beschriftung && (x.reserviert || x.boxH === 0)));
  assert.deepEqual((await plaetze(seite)).filter(p => !p.reserviert), []);
  await seite.$eval('.ad.on[data-ad="rect"] ins.adsbygoogle', i => i.setAttribute("data-ad-status", "filled"));
  const da = (await plaetze(seite)).filter(p => !p.reserviert);
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
  assert.ok(l.every(x => !x.beschriftung && (x.reserviert || x.abstand === 0)));
  await seite.$$eval(".ad.on ins.adsbygoogle", l => l.forEach(i => i.setAttribute("data-ad-status", "unfill-optimized")));
  l = await inse(seite);
  assert.ok(l.every(x => x.beschriftung));
  await ctx.close();
});

// ---------- Lage der Werbeplätze (19.11.2026): oberster Platz im ersten Bildschirm, Abstände, kein Sprung ----------
const GROESSE = { superbanner: [728, 90], mbanner: [320, 100], sky: [160, 600], half: [300, 600] };
const TYPEN = [["Startseite", "/"], ["Spiel", "/sudoku.html"], ["Spiel", "/codeknacker.html"], ["Spiel", "/zielzahl.html"], ["Spiel", "/nonogramm.html"],
               ["Löser", "/sudoku-loeser.html"], ["Rätselblatt", "/raetselblatt.html"], ["Beitrag", "/sudoku-strategien.html"],
               ["Übersicht", "/sudoku-techniken-ueben.html"], ["Druckseite", "/sudoku-zum-ausdrucken-leicht.html"], ["Über uns", "/about.html"]];

// Füllt alle Plätze wie Google: data-ad-status="filled", responsive Plätze bekommen ihr übliches Format.
function fuellen(seite) {
  return seite.evaluate(G => document.querySelectorAll(".ad.on ins.adsbygoogle").forEach(i => {
    const b = i.parentElement, k = b.dataset.ad, w = b.parentElement.getBoundingClientRect().width;
    let g = G[k];
    if (k === "billboard") g = w >= 970 ? [970, 250] : w >= 728 ? [728, 90] : [300, 250];
    if (k === "rect") g = w >= 336 && innerWidth > 800 ? [336, 280] : [300, 250];
    i.style.cssText = `display:inline-block;width:${g[0]}px;height:${g[1]}px`; i.setAttribute("data-ad-status", "filled");
  }), GROESSE);
}

function lage(seite) {
  return seite.evaluate(() => {
    const sichtbar = e => e.offsetParent !== null && !e.closest(".logbuch");
    const r = e => e.getBoundingClientRect();
    const abstand = (a, l) => Math.min(Infinity, ...l.map(b => Math.hypot(Math.max(b.left - a.right, a.left - b.right, 0), Math.max(b.top - a.bottom, a.top - b.bottom, 0))));
    // Bedienelemente der Werkzeuge und Schaltflächen im Inhalt samt Fußzeilen-Knopf; Navigation getrennt
    const bedien = [...document.querySelectorAll("main button, main input, main select, main textarea, main summary, main a.btn, main .tile, .foot button")].filter(sichtbar).map(r);
    const nav = [...document.querySelectorAll(".top a, .crumbs a, .side .box a")].filter(sichtbar).map(r);
    const main = r(document.querySelector("main"));
    const ads = [...document.querySelectorAll(".ad.on ins.adsbygoogle")].map(i => { const q = r(i), b = i.parentElement;
      return { art: b.dataset.ad, oben: q.top + scrollY, unten: q.bottom + scrollY, links: q.left, rechts: q.right, h: q.height, imText: !!b.closest("main") && !b.closest(".side"),
               bedien: abstand(q, bedien), nav: abstand(q, nav), label: getComputedStyle(b, "::before").content }; });
    const h1 = r(document.querySelector("h1")), spiel = document.querySelector("main .game"), text = document.querySelector("main .prose p, main .game");
    return { ads, h1Unten: h1.bottom + scrollY, spielOben: spiel ? r(spiel).top + scrollY : null, textOben: text ? r(text).top + scrollY : null,
             mainH: main.height, ueberlauf: document.documentElement.scrollWidth - innerWidth, breite: innerWidth, hoehe: innerHeight };
  });
}

async function oeffneMit(breite, hoehe, pfad) {
  const ctx = await browser.newContext({ viewport: { width: breite, height: hoehe } });
  await ctx.route(/^https?:\/\/(?!127\.0\.0\.1)/, r => r.fulfill({ status: 200, contentType: "text/javascript", body: "/* Stub */" }));
  const seite = await ctx.newPage();
  const fehler = [];
  seite.on("pageerror", e => fehler.push(e.message));
  seite.on("console", m => { if (m.type() === "error") fehler.push(m.text()); });
  await seite.goto(basis + pfad);
  return { ctx, seite, fehler };
}

for (const [breite, hoehe, oberster] of [[1366, 768, "superbanner"], [390, 844, "mbanner"]]) {
  for (const [typ, pfad] of TYPEN) {
    test(`${breite}×${hoehe} ${typ} ${pfad}: oberster Platz im ersten Bildschirm, Abstände, Überschrift sichtbar`, async () => {
      const { ctx, seite, fehler } = await oeffneMit(breite, hoehe, pfad);
      await seite.waitForFunction(() => document.querySelector(".ad.on ins.adsbygoogle"));
      await fuellen(seite);
      const l = await lage(seite);
      const top = l.ads.reduce((a, b) => (b.oben < a.oben ? b : a));
      assert.equal(top.art, oberster, "oberster Platz ist der Streifen unter der Kopfzeile");
      assert.ok(top.oben > 0 && top.unten <= hoehe, `oberster Platz vollständig im ersten Bildschirm (${top.oben}–${top.unten})`);
      assert.equal(top.h, GROESSE[oberster][1], "flaches Format oben");
      assert.ok(l.h1Unten <= hoehe, `Überschrift ohne Scrollen sichtbar (${l.h1Unten})`);
      assert.ok(l.textOben !== null && l.textOben < hoehe, `Inhalt bzw. Werkzeug beginnt im ersten Bildschirm (${l.textOben})`);
      if (l.spielOben !== null) assert.ok(l.spielOben < hoehe - 100, `Werkzeug beginnt im ersten Bildschirm (${l.spielOben})`);
      for (const a of l.ads) {
        assert.ok(a.bedien >= 150, `${a.art}: Abstand zu Bedienelementen ${Math.round(a.bedien)} px ≥ 150`);
        assert.ok(a.nav >= 32, `${a.art}: Abstand zu Navigation/Brotkrumen/Seitenleisten-Links ${Math.round(a.nav)} px ≥ 32`);
        assert.ok(a.links >= 0 && a.rechts <= l.breite, `${a.art}: ragt nicht aus dem Bildschirm`);
        assert.equal(a.label, '"Anzeige"', `${a.art}: Beschriftung „Anzeige“`);
        // Plätze im Text erst nach dem ersten Inhaltsblock; mobil außerdem erst unterhalb des ersten Bildschirms (kein Rechteck oben)
        if (a !== top && a.imText) {
          assert.ok(a.oben >= l.textOben + 100, `${a.art}: Platz im Text erst nach dem ersten Inhaltsblock (${a.oben}, Inhalt ab ${l.textOben})`);
          if (breite < 768) assert.ok(a.oben >= hoehe, `${a.art}: mobil erst unterhalb des ersten Bildschirms (${a.oben})`);
        }
      }
      if (breite < 768) {   // Better Ads Standards (mobil): Anzeigenhöhe höchstens 30 % der Höhe des Hauptinhalts
        const dichte = l.ads.reduce((s, a) => s + a.h, 0) / l.mainH;
        assert.ok(dichte < 0.3, `Anzeigendichte ${(dichte * 100).toFixed(1)} % < 30 %`);
        assert.ok(l.ads.every(a => a.art !== "half" && a.art !== "sky"), "mobil keine hohen Seitenleisten-Formate");
      }
      assert.equal(l.ueberlauf, 0, "kein horizontaler Überlauf");
      assert.deepEqual(fehler, []);
      await ctx.close();
    });
  }
}

for (const [breite, hoehe] of [[1366, 768], [390, 844]]) {
  test(`${breite}×${hoehe}: Füllen des obersten Platzes verschiebt nichts (CLS ≈ 0), leer bleibt nur Weißraum`, async () => {
    const { ctx, seite } = await oeffneMit(breite, hoehe, "/sudoku.html");
    await seite.waitForFunction(() => document.querySelector(".ad.on ins.adsbygoogle"));
    await seite.waitForTimeout(400);
    const y = () => seite.evaluate(() => [...document.querySelectorAll("h1, main .game")].map(e => e.getBoundingClientRect().top));
    const leer = await y();
    await seite.evaluate(() => { window.__cls = 0; new PerformanceObserver(l => { for (const e of l.getEntries()) window.__cls += e.value; }).observe({ type: "layout-shift", buffered: false }); });
    await seite.$eval(".ad--oben.on ins.adsbygoogle", i => i.setAttribute("data-ad-status", "filled"));
    await seite.waitForTimeout(300);
    assert.deepEqual(await y(), leer, "Überschrift und Spielfeld bleiben beim Füllen stehen");
    assert.ok(await seite.$eval(".ad--oben.on", b => getComputedStyle(b, "::before").display !== "none"), "Beschriftung erscheint");
    await seite.$eval(".ad--oben.on ins.adsbygoogle", i => i.setAttribute("data-ad-status", "unfilled"));
    await seite.waitForTimeout(300);
    assert.deepEqual(await y(), leer, "auch ohne Anzeige kein Sprung");
    assert.equal(await seite.$eval(".ad--oben.on ins.adsbygoogle", i => getComputedStyle(i).display), "none", "Googles Muster: unfilled → ins display:none");
    assert.ok(await seite.$eval(".ad--oben.on", b => getComputedStyle(b, "::before").display === "none"), "ohne Anzeige keine Beschriftung");
    const cls = await seite.evaluate(() => window.__cls);
    assert.ok(cls < 0.01, `CLS ${cls}`);
    await ctx.close();
  });
}

test("Ladevorgang: reservierter Streifen schon ohne Skript vorhanden; unter 360 px und bei Global Privacy Control kein Streifen", async () => {
  let ctx = await browser.newContext({ viewport: { width: 1366, height: 768 }, javaScriptEnabled: false });
  let seite = await ctx.newPage(); await seite.goto(basis + "/sudoku-strategien.html");
  assert.equal(await seite.$eval(".ad--superbanner", b => b.getBoundingClientRect().height), 112, "Höhe steht vor jedem Skript fest");
  await ctx.close();
  ({ ctx, seite } = await oeffneMit(340, 700, "/sudoku.html"));
  await seite.waitForFunction(() => document.querySelector(".ad.on ins.adsbygoogle"));
  assert.equal(await seite.$$eval(".ad--oben", l => l.filter(b => b.offsetParent !== null || b.querySelector("ins")).length), 0, "unter 360 px kein Streifen, keine Anfrage");
  assert.equal(await seite.evaluate(() => document.documentElement.scrollWidth - innerWidth), 0);
  await ctx.close();
  ctx = await browser.newContext({ viewport: { width: 390, height: 844 } });
  await ctx.route(/^https?:\/\/(?!127\.0\.0\.1)/, r => r.fulfill({ status: 200, contentType: "text/javascript", body: "" }));
  await ctx.addInitScript(() => Object.defineProperty(Navigator.prototype, "globalPrivacyControl", { get: () => true }));
  seite = await ctx.newPage(); await seite.goto(basis + "/sudoku.html"); await seite.waitForLoadState("load");
  assert.equal(await seite.$$eval(".ad", l => l.filter(b => b.offsetParent !== null || b.querySelector("ins")).length), 0, "GPC: kein Platz, kein Streifen");
  await ctx.close();
});

test("Seiten ohne Werbung bleiben ohne Werbeplatz", async () => {
  for (const pfad of ["/imprint.html", "/privacy.html", "/archiv.html", "/404.html"]) {
    const html = fs.readFileSync(path.join(DOCS, pfad), "utf8");
    assert.ok(!/class="ad /.test(html) && !html.includes("adsbygoogle"), pfad);
  }
});

test("Sitemap: jede Seite bei 1366 und 390 px ohne JS-Fehler, ohne Überlauf, Plätze mit Abstand", async () => {
  const pfade = [...fs.readFileSync(path.join(DOCS, "sitemap.xml"), "utf8").matchAll(/<loc>https:\/\/raetsellotse\.de([^<]*)<\/loc>/g)].map(m => m[1]);
  assert.ok(pfade.length >= 20);
  for (const [breite, hoehe] of [[1366, 768], [390, 844]]) for (const pfad of pfade) {
    const { ctx, seite, fehler } = await oeffneMit(breite, hoehe, pfad);
    await seite.waitForFunction(() => document.querySelector(".ad.on ins.adsbygoogle"));
    await fuellen(seite);
    const l = await lage(seite);
    assert.deepEqual(fehler, [], `${breite} ${pfad}`);
    assert.equal(l.ueberlauf, 0, `${breite} ${pfad}: Überlauf`);
    assert.ok(Math.min(...l.ads.map(a => a.oben)) < hoehe && l.h1Unten <= hoehe, `${breite} ${pfad}: oberster Platz und Überschrift im ersten Bildschirm`);
    for (const a of l.ads) assert.ok(a.bedien >= 150 && a.nav >= 32, `${breite} ${pfad} ${a.art}: Bedienelement ${Math.round(a.bedien)} px, Navigation ${Math.round(a.nav)} px`);
    await ctx.close();
  }
});
