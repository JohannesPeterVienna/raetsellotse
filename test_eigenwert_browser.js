// Browser-Prüfung (Playwright, 390 und 1366 px) über alle Seiten der Sitemap plus Bedienung der Werkzeuge:
// node test_eigenwert_browser.js [Screenshot-Ordner]   (nach python3 build.py; startet einen lokalen Server nur für die Laufzeit des Tests)
const assert = require("node:assert/strict");
const http = require("http"), fs = require("fs"), path = require("path");
const { chromium } = require("playwright");
const DOCS = path.join(__dirname, "docs"), SHOTS = process.argv[2] || "";
const ARTEN = { ".html": "text/html; charset=utf-8", ".js": "text/javascript", ".css": "text/css", ".woff2": "font/woff2", ".svg": "image/svg+xml", ".png": "image/png", ".xml": "text/xml", ".txt": "text/plain" };
const DATA = JSON.parse(fs.readFileSync(path.join(__dirname, "content", "tagessudoku.json"), "utf8"));
(async () => {
  const server = http.createServer((req, res) => {
    const datei = path.join(DOCS, decodeURIComponent(req.url.split("?")[0]).replace(/\/$/, "/index.html"));
    if (!datei.startsWith(DOCS) || !fs.existsSync(datei)) { res.writeHead(404); return res.end(); }
    res.writeHead(200, { "content-type": ARTEN[path.extname(datei)] || "application/octet-stream" }); res.end(fs.readFileSync(datei));
  });
  await new Promise(r => server.listen(0, "127.0.0.1", r));
  const base = `http://127.0.0.1:${server.address().port}`;
  const pages = [...fs.readFileSync(path.join(DOCS, "sitemap.xml"), "utf8").matchAll(/<loc>https:\/\/raetsellotse\.de([^<]*)<\/loc>/g)].map(m => m[1]).concat(["/archiv.html", "/imprint.html", "/privacy.html", "/404.html"]);
  const browser = await chromium.launch();
  const errors = [];
  const open = async (width, url) => {
    const page = await browser.newPage({ viewport: { width, height: 900 } });
    page.on("pageerror", e => errors.push(`${url} @${width}: ${e.message}`));
    page.on("console", m => { if (m.type() === "error" && !/google|ERR_|Failed to load resource/i.test(m.text())) errors.push(`${url} @${width}: ${m.text()}`); });
    page.on("dialog", d => { errors.push(`${url}: Dialog ${d.message()}`); d.dismiss(); });
    await page.route(/googlesyndication|googletagmanager|google-analytics|fundingchoices|doubleclick/, r => r.abort());
    await page.goto(base + url); return page;
  };
  const links = new Set();
  for (const width of [390, 1366]) for (const p of pages) {
    const page = await open(width, p);
    await page.waitForTimeout(p === "/sudoku.html" || p === "/raetselblatt.html" || p === "/nonogramm.html" ? 900 : 150);
    const sw = await page.evaluate(() => document.documentElement.scrollWidth);
    assert.ok(sw <= width, `Überlauf ${p} bei ${width}px: ${sw}`);
    for (const h of await page.$$eval("a[href]", as => as.map(a => a.getAttribute("href")))) if (h.startsWith("/")) links.add(h);
    if (SHOTS && ["/", "/sudoku-strategien.html", "/sudoku-techniken-ueben.html", "/sudoku.html", "/sudoku-loeser.html"].includes(p)) await page.screenshot({ path: path.join(SHOTS, `${p.replace(/\W/g, "_")}-${width}.png`), fullPage: p !== "/sudoku-techniken-ueben.html" });
    await page.close();
  }
  for (const h of links) { const f = path.join(DOCS, h.split(/[?#]/)[0].replace(/\/$/, "/index.html")); assert.ok(fs.existsSync(f), "toter Link: " + h); }
  console.log(`${pages.length} Seiten × 2 Breiten ohne Überlauf, ${links.size} interne Links vorhanden`);

  for (const width of [390, 1366]) {
    // Startseite: Codeknacker direkt spielbar (Tastatur und Knöpfe)
    let page = await open(width, "/");
    assert.equal(await page.locator(".homegame [data-pad] button[data-d]").count(), 6);
    for (const d of [1, 2, 3]) await page.click(`.homegame [data-d="${d}"]`);
    await page.keyboard.press("4"); await page.keyboard.press("Enter");
    assert.equal(await page.evaluate(() => JSON.parse(localStorage.getItem(Object.keys(localStorage).find(k => k.startsWith("rl-code-")))).guesses.length), 1);
    await page.close();

    // Tagessudoku: Bewertung, Tipp mit Technikname, Vorarbeit mit Kandidaten, am Ende gelöst
    const tag = DATA.beispiele.pointing.tag;
    page = await open(width, `/sudoku.html?tag=${tag}&stufe=schwer`);
    await page.waitForFunction(() => document.querySelector("[data-rating]").textContent.includes("Bewertung"));
    assert.match(await page.textContent("[data-rating]"), /Stufe 2 · Fortgeschritten – schwierigste nötige Technik: Block-Zeile-Regel/);
    assert.equal(await page.getAttribute("[data-rating] a", "href"), "/sudoku-loeser.html?s=" + DATA.beispiele.pointing.s);
    await page.click("[data-notes]");   // Tipp muss auch im Notizmodus die Ziffer setzen
    let vorarbeit = 0, namen = 0;
    for (let k = 0; k < 80; k++) {
      await page.click("[data-hint]");
      const t = await page.textContent("[data-msg]");
      if (/Gelöst!/.test(t)) break;
      if (/Vorarbeit mit Kandidaten/.test(t)) { vorarbeit++; assert.match(t, /Block-Zeile-Regel:/); }
      if (/Tipp – (Einziger Platz|Einzige Möglichkeit)/.test(t)) namen++;
      assert.doesNotMatch(t, /ohne Begründung/);
    }
    assert.match(await page.textContent("[data-msg]"), /Gelöst!/); assert.ok(vorarbeit >= 1 && namen > 20, `Vorarbeit ${vorarbeit}, Namen ${namen}`);
    const sw = await page.evaluate(() => document.documentElement.scrollWidth); assert.ok(sw <= width, "Überlauf nach Tipps");
    await page.close();
    // Stufe 4: Tipp deckt erst auf, wenn keine Technik mehr greift
    const s4 = DATA.tage.find(t => t.schwer.stufe === 4).tag;
    page = await open(width, `/sudoku.html?tag=${s4}&stufe=schwer`);
    await page.waitForFunction(() => document.querySelector("[data-rating]").textContent.includes("Bewertung"));
    assert.match(await page.textContent("[data-rating]"), /Stufe 4/);
    let auf = 0; for (let k = 0; k < 80; k++) { await page.click("[data-hint]"); const t = await page.textContent("[data-msg]"); if (/Gelöst!/.test(t)) break; if (/ohne Begründung aufgedeckt/.test(t)) auf++; }
    assert.ok(auf >= 1); assert.match(await page.textContent("[data-msg]"), /Gelöst!/);
    await page.close();
    // falscher Eintrag wird vor jedem Tipp gemeldet; unsinnige Parameter fallen auf heute/mittel zurück
    page = await open(width, `/sudoku.html?tag=%3Cscript%3Ealert(1)%3C/script%3E&stufe=%22%3E%3Cimg%20src=x%20onerror=alert(1)%3E`);
    await page.waitForFunction(() => document.querySelector("[data-rating]").textContent.includes("Bewertung"));
    assert.equal(await page.locator("[data-game] img, [data-game] script").count(), 0);
    assert.equal(await page.inputValue("[data-level]"), "mittel");
    await page.close();

    // Löser: Stellung aus der Strategie-Seite (?s=…&bis=N) – nächster Schritt ist genau die Technik
    for (const [tech, b] of Object.entries(DATA.beispiele)) {
      page = await open(width, `/sudoku-loeser.html?s=${b.s}&bis=${b.schritt}`);
      assert.match(await page.textContent("[data-lmsg]"), b.schritt ? new RegExp(`Stand nach ${b.schritt} Schritten`) : /aus dem Link geladen/);
      assert.equal(await page.locator("[data-steps] li").count(), b.schritt);
      await page.click("[data-next]");
      const t = await page.textContent("[data-lmsg]");
      assert.ok(t.includes(`Schritt ${b.schritt + 1}: ${b.name}`) && t.includes(b.text), `${tech}: ${t}`);
      await page.close();
    }
    // Löser: Unsinn in der Adresse und im Textfeld, Drucken ohne Lösungsweg
    for (const q of ["?s=%3Cimg%20src=x%20onerror=alert(1)%3E", "?s=" + "9".repeat(81) + "&bis=999999", "?s=" + DATA.beispiele.pointing.s + "&bis=%3Cb%3E", "?s=" + "1".repeat(500), "?bis=5"]) {
      page = await open(width, "/sudoku-loeser.html" + q);
      assert.equal(await page.locator("[data-game=loeser] img, [data-game=loeser] b").count(), 0, q);
      await page.click("[data-next]"); await page.click("[data-all]"); await page.click("[data-check]"); await page.click("[data-print]");
      await page.close();
    }
    page = await open(width, "/sudoku-loeser.html");
    await page.click(".lpaste summary"); await page.fill("[data-text]", '<img src=x onerror=alert(1)>=1+1@SUM(A1)'); await page.click("[data-load]");
    assert.match(await page.textContent("[data-lmsg]"), /genau 81 Zeichen/); assert.equal(await page.locator("[data-game=loeser] img").count(), 0);
    await page.evaluate(() => { window.__p = 0; window.print = () => { window.__p++; }; });
    await page.click("[data-print]"); assert.equal(await page.evaluate(() => window.__p), 0); assert.match(await page.textContent("[data-lmsg]"), /Noch kein Lösungsweg/);
    await page.selectOption("[data-beispiel]", "stufe2"); await page.click("[data-all]"); await page.click("[data-print]");
    assert.equal(await page.evaluate(() => window.__p), 1);
    await page.emulateMedia({ media: "print" });
    assert.equal(await page.locator("[data-steps]").evaluate(e => getComputedStyle(e).maxHeight), "none");
    assert.equal(await page.locator(".top").evaluate(e => getComputedStyle(e).display), "none");
    assert.equal(await page.locator("[data-game=loeser] .pad").evaluate(e => getComputedStyle(e).display), "none");
    await page.close();

    // Technik-Liste: Filter, Zähler, Verweis in den Löser
    page = await open(width, "/sudoku-techniken-ueben.html");
    assert.equal(await page.locator("[data-ueben] tbody tr").count(), DATA.tage.length);
    await page.selectOption("[data-f-tech]", "xy-wing");
    const nXY = DATA.tage.filter(t => "xy-wing" in t.schwer.erst).length;
    assert.equal(await page.locator("[data-ueben] tbody tr:visible").count(), nXY);
    assert.equal(await page.textContent("[data-f-n]"), `${nXY} von ${DATA.tage.length} Rätseln`);
    await page.selectOption("[data-f-stufe]", "4");
    assert.equal(await page.locator("[data-ueben] tbody tr:visible").count(), DATA.tage.filter(t => "xy-wing" in t.schwer.erst && t.schwer.stufe === 4).length);
    assert.match(page.url(), /technik=xy-wing&stufe=4/);
    await page.close();
    page = await open(width, "/sudoku-techniken-ueben.html?technik=%3Cscript%3E&stufe=9");
    assert.equal(await page.locator("[data-ueben] tbody tr:visible").count(), DATA.tage.length);
    await page.close();
  }
  await browser.close(); server.close();
  assert.deepEqual(errors, []);
  console.log("Werkzeuge bei 390 und 1366 px durchgeklickt: ohne Fehler");
})().catch(e => { console.error(e); process.exit(1); });
