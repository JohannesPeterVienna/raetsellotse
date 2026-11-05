// Browsertest Sudoku-Löser (Playwright, 390 und 1366 px): node test_loeser_browser.js [Screenshot-Ordner]
// Erwartet einen Webserver auf http://127.0.0.1:8765 mit docs/ als Wurzel.
const { chromium } = require("playwright");
const assert = require("node:assert/strict");
const BASE = "http://127.0.0.1:8765/sudoku-loeser.html", OUT = process.argv[2] || "";
(async () => {
  const browser = await chromium.launch();
  for (const width of [390, 1366]) {
    const page = await browser.newPage({ viewport: { width, height: 900 } });
    const errors = []; page.on("pageerror", e => errors.push(e.message));
    page.on("console", m => { if (m.type() === "error" && !/googlesyndication|google|ERR_|403|Failed to load resource/i.test(m.text())) errors.push(m.text()); });
    await page.route(/googlesyndication|googletagmanager|google-analytics|fundingchoices/, r => r.abort());
    await page.goto(BASE);
    // kein horizontales Scrollen
    const sw = await page.evaluate(() => document.documentElement.scrollWidth);
    assert.ok(sw <= width, `horizontales Scrollen bei ${width}px: ${sw}`);
    assert.equal(await page.locator("[data-lgrid] input").count(), 81);
    // Beispiel Stufe 1 laden, einen Schritt erklären
    await page.selectOption("[data-beispiel]", "stufe1");
    await page.click("[data-next]");
    const m1 = await page.textContent("[data-lmsg]");
    assert.match(m1, /Schritt 1: Einziger Platz/);
    assert.equal(await page.locator(".lc.solved").count(), 1);
    // ganzer Lösungsweg
    await page.click("[data-all]");
    assert.match(await page.textContent("[data-lmsg]"), /Gelöst in \d+ Schritten/);
    assert.equal(await page.locator(".lc input").evaluateAll(xs => xs.filter(x => /^[1-9]$/.test(x.value)).length), 81);
    // Stufe 3 mit XY-Wing: Lösungsweg enthält XY-Wing, Prüfen nennt Stufe 3
    await page.selectOption("[data-beispiel]", "stufe3");
    await page.click("[data-check]");
    assert.match(await page.textContent("[data-lmsg]"), /Stufe 3/);
    await page.click("[data-all]");
    assert.match(await page.textContent("[data-steps]"), /XY-Wing/);
    // Stufe 4: Löser bleibt hängen und bietet Aufdecken an
    await page.selectOption("[data-beispiel]", "stufe4");
    for (let k = 0; k < 200; k++) { await page.click("[data-next]"); if (await page.locator("[data-reveal]").count()) break; }
    assert.ok(await page.locator("[data-reveal]").count(), "Aufdecken wird angeboten");
    await page.click("[data-reveal]");
    assert.equal(await page.locator(".lc.shown").count(), 1);
    if (OUT) await page.screenshot({ path: `${OUT}/loeser-${width}-schritt.png`, fullPage: false });
    // Fehler: doppelte Ziffer
    await page.click("[data-clear]");
    const inp = page.locator("[data-lgrid] input");
    await inp.nth(0).fill("5"); await inp.nth(1).fill("5");
    await page.click("[data-next]");
    assert.match(await page.textContent("[data-lmsg]"), /widersprechen sich/);
    assert.equal(await page.locator(".lc.bad").count(), 2);
    // zu wenige Vorgaben → mehrere Lösungen
    await page.click("[data-clear]"); await inp.nth(0).fill("1");
    await page.click("[data-next]");
    assert.match(await page.textContent("[data-lmsg]"), /mehr als eine Lösung/);
    // Link mit ?s= lädt das Rätsel
    await page.goto(BASE + "?s=" + "..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..");
    assert.equal(await inp.nth(2).inputValue(), "3");
    // Tastatur: Pfeil nach rechts wechselt Feld
    await inp.nth(0).focus(); await page.keyboard.press("ArrowRight");
    assert.equal(await page.evaluate(() => document.activeElement.dataset.i), "1");
    // Werbeflächen nicht neben dem Spielfeld (keine Seitenleisten-Werbung)
    assert.equal(await page.locator(".side .ad").count(), 0);
    if (OUT) await page.screenshot({ path: `${OUT}/loeser-${width}.png`, fullPage: true });
    assert.deepEqual(errors, []);
    console.log(`ok ${width}px`);
    await page.close();
  }
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
