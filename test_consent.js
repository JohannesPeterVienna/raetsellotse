// Automatischer Test für assets/consent.js (node --test test_consent.js): AdSense-Loader nie doppelt,
// Consent-Default nicht wiederholt, Global Privacy Control hält Anzeigenanfragen an, Statistik nur mit Einwilligung,
// Übergangsfenster „Logbuch-Zettel“ (nur Statistik), wenn die Google-CMP nach 3 s nichts entscheidet.
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("fs");
const vm = require("vm");
const SRC = fs.readFileSync(__dirname + "/assets/consent.js", "utf8");
const LOADER = "https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7811071715414905";

// Mini-DOM: gerade genug für den Logbuch-Zettel (Elemente, Klicks, Tasten, Fokus)
function knoten(tag, doc) {
  const k = {
    tagName: tag.toUpperCase(), attr: {}, kinder: [], eltern: null, hoerer: {}, dataset: {}, style: {}, classList: { add() {}, remove() {} },
    setAttribute(n, v) { this.attr[n] = String(v); }, getAttribute(n) { return n in this.attr ? this.attr[n] : null; },
    hasAttribute(n) { return n in this.attr; },
    append(...xs) { xs.forEach(x => { if (typeof x === "object") x.eltern = this; this.kinder.push(x); }); },
    prepend(x) { x.eltern = this; this.kinder.unshift(x); },
    remove() { if (this.eltern) this.eltern.kinder = this.eltern.kinder.filter(c => c !== this); this.eltern = null; },
    contains(x) { for (let c = x; c; c = c.eltern) if (c === this) return true; return false; },
    closest(sel) { const namen = sel.split(",").map(t => t.replace(/[\[\]]/g, "")); for (let c = this; c && c.attr; c = c.eltern) if (namen.some(n => n in c.attr)) return c; return null; },
    addEventListener(t, f) { (this.hoerer[t] = this.hoerer[t] || []).push(f); },
    focus() { doc.activeElement = this; },
    get isConnected() { for (let c = this; c; c = c.eltern) if (c === doc.body) return true; return false; },
    get textContent() { return this.kinder.map(c => (typeof c === "string" ? c : c.textContent)).join(""); }
  };
  return k;
}
const alle = (k, f, out = []) => { if (k && typeof k === "object") { if (f(k)) out.push(k); k.kinder.forEach(c => alle(c, f, out)); } return out; };

// cm: Consent-Mode-Analyticswert der Google-CMP (0–4); us: US-Opt-out-Status (0–3), null = Schnittstelle fehlt
function seite({ statisch = true, kopfDefault = true, gpc = false, slots = [], tcfapi = true, ohneWerbung = false, hash = "",
                 speicher = {}, kekse = ["_ga=GA1.1.1", "_ga_T00HRG2YVF=GS1.1", "rl-andere=1"], jetzt = Date.now(), cm = 1, us = null } = {}) {
  const angehaengt = [], befehle = [];
  let tcf = null, uhr = 0;
  const timer = [];
  const jar = new Map(kekse.map(k => k.split("=")));
  const geloeschtAuf = [];
  const document = {
    head: { appendChild: s => angehaengt.push(s) },
    createElement: tag => Object.assign(knoten(tag, document), { offsetHeight: tag === "section" ? 300 : 0 }),
    querySelector: sel => (statisch && /adsbygoogle\.js/.test(sel) ? { src: LOADER } : null),
    querySelectorAll: () => slots,
    hoerer: {}, addEventListener(t, f) { (this.hoerer[t] = this.hoerer[t] || []).push(f); },
    activeElement: null,
    currentScript: ohneWerbung ? { hasAttribute: n => n === "data-ohne-werbung" } : null,
    get cookie() { return [...jar].map(([n, v]) => n + "=" + v).join("; "); },
    set cookie(s) {
      const [nv, ...rest] = s.split(";"); const [n, v] = nv.split("=");
      if (/max-age=0|expires=Thu, 01 Jan 1970/.test(rest.join(";"))) { jar.delete(n.trim()); geloeschtAuf.push(n.trim() + (rest.find(r => r.startsWith("domain=")) || "")); }
      else jar.set(n.trim(), v);
    }
  };
  document.body = knoten("body", document);
  const RealDate = Date;
  class FakeDate extends RealDate { constructor(...a) { super(...(a.length ? a : [jetzt + uhr])); } static now() { return jetzt + uhr; } }
  const store = new Map(Object.entries(speicher).map(([k, v]) => [k, JSON.stringify(v)]));
  const window = {
    document, navigator: { globalPrivacyControl: gpc }, Date: FakeDate, JSON, Number, Object, String,
    location: { hostname: "www.raetsellotse.de", hash },
    localStorage: { getItem: k => (store.has(k) ? store.get(k) : null), setItem: (k, v) => store.set(k, String(v)), removeItem: k => store.delete(k) },
    setTimeout: (f, ms = 0) => { timer.push({ f, bei: uhr + ms }); return timer.length; },
    googlefc: { callbackQueue: [], getGoogleConsentModeValues: () => ({ analyticsStoragePurposeConsentStatus: cm }) }
  };
  if (us !== null) window.googlefc.usstatesoptout = { getInitialUsStatesOptOutStatus: () => us };
  if (tcfapi) window.__tcfapi = (cmd, v, cb) => { if (cmd === "addEventListener") tcf = cb; };
  window.window = window;
  window.dataLayer = [];
  window.gtag = (...a) => befehle.push(a);
  if (kopfDefault) {   // wie das Inline-Skript im <head>
    window.gtag("consent", "default", { ad_storage: "denied", ad_user_data: "denied", ad_personalization: "denied", analytics_storage: "denied", wait_for_update: 500 });
    window["ga-disable-G-T00HRG2YVF"] = true; window.rlConsentDefault = true;
  }
  vm.runInContext(SRC, vm.createContext(window));
  const ticken = ms => {   // Uhr vorstellen, fällige Timer der Reihe nach ausführen
    const ziel = uhr + ms;
    for (;;) {
      timer.sort((a, b) => a.bei - b.bei);
      if (!timer.length || timer[0].bei > ziel) break;
      const t = timer.shift(); uhr = t.bei; t.f();
    }
    uhr = ziel;
  };
  const zettel = () => alle(document.body, k => k.hasAttribute("data-logbuch"))[0] || null;
  const knopf = wahl => alle(zettel(), k => k.getAttribute("data-logbuch-wahl") === wahl || (wahl === "zu" && k.hasAttribute("data-logbuch-zu")))[0];
  const klick = ziel => {   // Ereignis vom Ziel aus zum Zettel und zum Dokument hochreichen
    const e = { target: ziel, stopPropagation() { this.gestoppt = true; } };
    for (let c = ziel; c; c = c.eltern) (c.hoerer.click || []).forEach(f => f(e));
    (document.hoerer.click || []).forEach(f => f(e));
  };
  const taste = (ziel, key) => {
    const e = { target: ziel, key, gestoppt: false, stopPropagation() { this.gestoppt = true; } };
    for (let c = ziel; c && !e.gestoppt; c = c.eltern) (c.hoerer.keydown || []).forEach(f => f(e));
    return e;
  };
  const einstellungsKnopf = knoten("button", document); einstellungsKnopf.setAttribute("data-privacy-settings", "");
  document.body.append(einstellungsKnopf);
  return { window, document, angehaengt, befehle, tcf: d => tcf(d, true), ticken, zettel, knopf, klick, taste, jar, geloeschtAuf, store,
           einstellungsKnopf, gtm: () => angehaengt.filter(s => /googletagmanager/.test(s.src || "")).length,
           wahl: () => JSON.parse(store.get("rl-statistik-wahl") || "null") };
}
const defaults = b => b.filter(a => a[0] === "consent" && a[1] === "default");

test("statischer Loader vorhanden: consent.js lädt ihn nicht ein zweites Mal", () => {
  const p = seite();
  assert.equal(p.angehaengt.filter(s => /adsbygoogle\.js/.test(s.src || "")).length, 0);
});

test("Loader fehlt (Rückfall): consent.js lädt ihn genau einmal", () => {
  const p = seite({ statisch: false });
  assert.equal(p.angehaengt.filter(s => s.src === LOADER).length, 1);
});

test("Consent-Default wird nicht wiederholt, ohne Kopf-Skript aber gesetzt (alles denied)", () => {
  assert.equal(defaults(seite().befehle).length, 1);
  const q = seite({ kopfDefault: false });
  const d = defaults(q.befehle);
  assert.equal(d.length, 1);
  for (const k of ["ad_storage", "ad_user_data", "ad_personalization", "analytics_storage"]) assert.equal(d[0][2][k], "denied");
  assert.equal(q.window["ga-disable-G-T00HRG2YVF"], true);
});

test("Global Privacy Control: Anzeigenanfragen angehalten, kein Werbeplatz befüllt, keine Statistik", () => {
  const box = { dataset: { ad: "rect" }, classList: { add() { throw new Error("Werbeplatz befüllt"); } } };
  const p = seite({ gpc: true, statisch: false, slots: [box] });
  assert.equal(p.window.adsbygoogle.pauseAdRequests, 1);
  assert.equal(p.angehaengt.length, 0);
  p.tcf({ gdprApplies: true, eventStatus: "tcloaded", tcString: "CQ-ja", purpose: { consents: { 1: true } }, vendor: { consents: { 755: true } } });
  assert.equal(p.window["ga-disable-G-T00HRG2YVF"], true);
  assert.ok(!p.angehaengt.some(s => /googletagmanager/.test(s.src || "")));
});

test("DSGVO: Statistik nur mit Zweck 1 + Anbieter 755 + Consent Mode GRANTED; ohne Einwilligung bleibt sie aus", () => {
  const nein = seite();
  nein.tcf({ gdprApplies: true, eventStatus: "tcloaded", tcString: "CQ-nein", purpose: { consents: {} }, vendor: { consents: {} } });
  assert.equal(nein.window["ga-disable-G-T00HRG2YVF"], true);
  assert.ok(!nein.angehaengt.some(s => /googletagmanager/.test(s.src || "")));
  const ja = seite();
  ja.tcf({ gdprApplies: true, eventStatus: "useractioncomplete", purpose: { consents: { 1: true } }, vendor: { consents: { 755: true } } });
  assert.equal(ja.window["ga-disable-G-T00HRG2YVF"], false);
  assert.ok(ja.angehaengt.some(s => /googletagmanager/.test(s.src || "")));
});

/* ---------------- Logbuch-Zettel (Übergangsfenster nur für die Statistik) ---------------- */
const VERBORGEN = { gdprApplies: true, eventStatus: "tcloaded", tcString: "", displayStatus: "hidden", purpose: { consents: {} }, vendor: { consents: {} } };
const GOOGLE_JA = { gdprApplies: true, eventStatus: "useractioncomplete", tcString: "CQ-ja", displayStatus: "hidden", purpose: { consents: { 1: true } }, vendor: { consents: { 755: true } } };
const GOOGLE_NEIN = { gdprApplies: true, eventStatus: "useractioncomplete", tcString: "CQ-nein", displayStatus: "hidden", purpose: { consents: {} }, vendor: { consents: {} } };
const werbeUpdates = b => b.filter(a => a[0] === "consent" && a[1] === "update" && ["ad_storage", "ad_user_data", "ad_personalization"].some(k => k in a[2]));
const MONAT = 30.5 * 864e5;

test("kein __tcfapi: Zettel erst nach 3 s, vorher nichts; Zustimmen lädt gtag.js genau einmal, Werbe-Signale unberührt", () => {
  const p = seite({ tcfapi: false });
  p.ticken(2900);
  assert.equal(p.zettel(), null);
  p.ticken(200);
  assert.ok(p.zettel(), "Zettel nach 3 s");
  assert.equal(p.zettel().getAttribute("role"), "region");
  assert.equal(p.zettel().getAttribute("aria-labelledby"), "logbuch-titel");
  assert.equal(p.gtm(), 0, "vor Zustimmung kein googletagmanager");
  assert.equal(p.window["ga-disable-G-T00HRG2YVF"], true);
  p.klick(p.knopf("ja"));
  assert.equal(p.zettel(), null);
  assert.equal(p.gtm(), 1);
  assert.equal(p.window["ga-disable-G-T00HRG2YVF"], false);
  assert.ok(p.befehle.some(a => a[0] === "consent" && a[1] === "update" && a[2].analytics_storage === "granted"));
  const cfg = p.befehle.find(a => a[0] === "config");
  assert.equal(cfg[2].allow_google_signals, false); assert.equal(cfg[2].allow_ad_personalization_signals, false);
  assert.equal(werbeUpdates(p.befehle).length, 0, "ad_* nie durch den Zettel");
  assert.equal(p.wahl().wahl, "ja"); assert.equal(p.wahl().v, 1); assert.ok(Number.isFinite(p.wahl().zeit));
  p.ticken(20000); assert.equal(p.gtm(), 1, "nicht doppelt");
});

test("CMP meldet displayStatus hidden ohne Entscheidung: Zettel; Ablehnen → kein gtag.js, _ga-Cookies gelöscht", () => {
  const p = seite();
  p.tcf(VERBORGEN);
  assert.equal(p.zettel(), null, "nicht sofort");
  p.ticken(3000);
  assert.ok(p.zettel());
  p.klick(p.knopf("nein"));
  assert.equal(p.gtm(), 0);
  assert.equal(p.wahl().wahl, "nein");
  assert.ok(!p.jar.has("_ga") && !p.jar.has("_ga_T00HRG2YVF"), "GA-Cookies weg");
  assert.ok(p.jar.has("rl-andere"), "fremde Cookies bleiben");
  assert.ok(p.geloeschtAuf.includes("_gadomain=.raetsellotse.de"), "auch auf der Hauptdomain gelöscht");
  assert.ok(p.befehle.some(a => a[0] === "consent" && a[1] === "update" && a[2].analytics_storage === "denied"));
  assert.equal(werbeUpdates(p.befehle).length, 0);
});

test("Google-Meldung sichtbar: kein eigener Zettel", () => {
  const p = seite();
  p.tcf({ ...VERBORGEN, eventStatus: "cmpuishown", displayStatus: "visible" });
  p.ticken(5000);
  assert.equal(p.zettel(), null);
});

const AUSSEN = { gdprApplies: false, eventStatus: "tcloaded", tcString: "" };
const werbungFrei = p => p.befehle.some(a => a[0] === "consent" && a[2] && ["ad_storage", "ad_user_data", "ad_personalization"].some(k => a[2][k] === "granted"));

test("gdprApplies false + GRANTED ohne US-Opt-out: kein Zettel, Messung laut Google", () => {
  const p = seite({ us: 2 });
  p.tcf(AUSSEN); p.ticken(5000);
  assert.equal(p.zettel(), null); assert.equal(p.gtm(), 1); assert.equal(werbungFrei(p), false);
  const unbestaetigt = seite({ us: 0 });   // US-Status noch nicht gemeldet: keine Bestätigung → Zettel fragt
  unbestaetigt.tcf(AUSSEN); unbestaetigt.ticken(5000);
  assert.equal(unbestaetigt.gtm(), 0); assert.ok(unbestaetigt.zettel());
});

test("gdprApplies false + NOT_APPLICABLE: kein gtag ohne Klick; Zettel fragt nach 3 s; Zustimmen lädt gtag genau einmal", () => {
  const p = seite({ cm: 3, us: 1 });
  p.tcf(AUSSEN); p.ticken(2900);
  assert.equal(p.gtm(), 0, "NOT_APPLICABLE ist keine Einwilligung"); assert.equal(p.zettel(), null);
  p.ticken(200);
  assert.ok(p.zettel(), "Zettel erscheint auch außerhalb der DSGVO ohne gespeicherte Wahl"); assert.equal(p.gtm(), 0);
  p.klick(p.knopf("ja")); p.ticken(100);
  assert.equal(p.gtm(), 1); assert.equal(p.window["ga-disable-G-T00HRG2YVF"], false); assert.equal(p.wahl().wahl, "ja");
  p.tcf(AUSSEN); p.ticken(1000);
  assert.equal(p.gtm(), 1, "gtag nur einmal"); assert.equal(werbungFrei(p), false);
  const n = seite({ cm: 3, us: 1 }); n.tcf(AUSSEN); n.ticken(3100); n.klick(n.knopf("nein")); n.ticken(100);
  assert.equal(n.gtm(), 0); assert.equal(n.wahl().wahl, "nein"); assert.equal(n.jar.has("_ga"), false);
});

test("gdprApplies false + NOT_APPLICABLE: gespeichertes Ja misst ohne Zettel, gespeichertes Nein bleibt aus", () => {
  const ja = seite({ cm: 3, us: 2, speicher: { "rl-statistik-wahl": { v: 1, wahl: "ja", zeit: Date.now() - 864e5 } } });
  ja.tcf(AUSSEN); ja.ticken(5000);
  assert.equal(ja.zettel(), null); assert.equal(ja.gtm(), 1); assert.equal(ja.wahl().wahl, "ja", "eigene Wahl bleibt gespeichert");
  const nein = seite({ cm: 3, us: 2, speicher: { "rl-statistik-wahl": { v: 1, wahl: "nein", zeit: Date.now() } } });
  nein.tcf(AUSSEN); nein.ticken(5000);
  assert.equal(nein.zettel(), null); assert.equal(nein.gtm(), 0); assert.equal(nein.jar.has("_ga"), false);
});

test("gdprApplies false + DENIED oder US-Opt-out: kein gtag, kein Zettel, eigenes Ja zählt nicht", () => {
  for (const o of [{ cm: 2, us: 1 }, { cm: 1, us: 3 }, { cm: 3, us: 3 }]) {
    const p = seite(Object.assign({ speicher: { "rl-statistik-wahl": { v: 1, wahl: "ja", zeit: Date.now() } } }, o));
    p.tcf(AUSSEN); p.ticken(5000);
    assert.equal(p.gtm(), 0, JSON.stringify(o)); assert.equal(p.zettel(), null, JSON.stringify(o));
    assert.equal(p.wahl(), null, "eigene Wahl verworfen " + JSON.stringify(o));
  }
});

test("gdprApplies false ohne CMP-Schnittstellen: kein gtag, Zettel fragt", () => {
  const p = seite({ cm: 0 });
  p.tcf(AUSSEN); p.ticken(5000);
  assert.equal(p.gtm(), 0); assert.ok(p.zettel());
});

test("gdprApplies false: Zettel offen, dann meldet Google GRANTED → Zettel zu, Messung laut Google, Einstellungen bei Google", () => {
  const p = seite({ cm: 3, us: 1 });
  p.tcf(AUSSEN); p.ticken(3100);
  assert.ok(p.zettel());
  p.window.googlefc.getGoogleConsentModeValues = () => ({ analyticsStoragePurposeConsentStatus: 1 });
  p.tcf(Object.assign({}, AUSSEN, { eventStatus: "useractioncomplete", tcString: "CQx" })); p.ticken(500);
  assert.equal(p.zettel(), null); assert.equal(p.gtm(), 1);
  let gezeigt = 0; p.window.googlefc.showRevocationMessage = () => gezeigt++;
  p.klick(p.einstellungsKnopf); p.window.googlefc.callbackQueue.filter(f => typeof f === "function").forEach(f => f());
  assert.equal(gezeigt, 1); assert.equal(p.zettel(), null);
});

test("echte CMP-Entscheidung schlägt eigene Wahl: gespeichertes Ja wird ignoriert und gelöscht", () => {
  const p = seite({ speicher: { "rl-statistik-wahl": { v: 1, wahl: "ja", zeit: Date.now() - 864e5 } } });
  p.tcf(GOOGLE_NEIN);
  p.ticken(5000);
  assert.equal(p.zettel(), null);
  assert.equal(p.gtm(), 0, "eigenes Ja zählt nicht");
  assert.equal(p.wahl(), null, "eigene Wahl gelöscht");
  assert.ok(p.store.has("rl-einwilligung-google"));
});

test("CMP entscheidet nach dem Zettel: Zettel verschwindet, Google-Nein beendet eigene Messung und löscht Cookies", () => {
  const p = seite({ tcfapi: false });
  p.ticken(3000);
  p.klick(p.knopf("ja"));
  assert.equal(p.window["ga-disable-G-T00HRG2YVF"], false);
  p.window.__tcfapi = (cmd, v, cb) => { if (cmd === "addEventListener") cb(GOOGLE_NEIN, true); };
  p.ticken(2000);   // watchConsent fragt alle 250 ms
  assert.equal(p.window["ga-disable-G-T00HRG2YVF"], true);
  assert.ok(!p.jar.has("_ga"));
  assert.equal(p.wahl(), null);
  p.klick(p.einstellungsKnopf);
  assert.equal(p.zettel(), null, "Einstellungen gehen jetzt an Google");
  assert.ok(p.window.googlefc.callbackQueue.some(f => typeof f === "function"));
});

test("Zettel offen, Google-Ja kommt: Zettel zu, Messung laut Google", () => {
  const p = seite();
  p.tcf(VERBORGEN); p.ticken(3000);
  assert.ok(p.zettel());
  p.tcf(GOOGLE_JA);
  assert.equal(p.zettel(), null);
  assert.equal(p.gtm(), 1);
});

test("Global Privacy Control: Zettel drängt sich nicht auf, eigenes Ja zählt nicht; Einstellungen zeigen nur Hinweis", () => {
  const p = seite({ gpc: true, tcfapi: false, speicher: { "rl-statistik-wahl": { v: 1, wahl: "ja", zeit: Date.now() } } });
  p.ticken(5000);
  assert.equal(p.zettel(), null);
  assert.equal(p.gtm(), 0);
  p.klick(p.einstellungsKnopf);
  assert.equal(p.zettel().getAttribute("data-logbuch"), "gpc");
  assert.equal(p.knopf("ja"), undefined, "kein Zustimmen-Knopf bei GPC");
});

test("gespeicherte Wahl gilt beim Neuladen; nach 12 Monaten wird neu gefragt; falsche Fassung zählt nicht", () => {
  const ja = seite({ tcfapi: false, speicher: { "rl-statistik-wahl": { v: 1, wahl: "ja", zeit: Date.now() - 11 * MONAT } } });
  ja.ticken(3000);
  assert.equal(ja.zettel(), null); assert.equal(ja.gtm(), 1);
  const nein = seite({ tcfapi: false, speicher: { "rl-statistik-wahl": { v: 1, wahl: "nein", zeit: Date.now() } } });
  nein.ticken(3000);
  assert.equal(nein.zettel(), null); assert.equal(nein.gtm(), 0);
  const alt = seite({ tcfapi: false, speicher: { "rl-statistik-wahl": { v: 1, wahl: "ja", zeit: Date.now() - 12.1 * MONAT } } });
  alt.ticken(3000);
  assert.ok(alt.zettel(), "abgelaufen → neu fragen"); assert.equal(alt.gtm(), 0);
  const fassung = seite({ tcfapi: false, speicher: { "rl-statistik-wahl": { v: 0, wahl: "ja", zeit: Date.now() } } });
  fassung.ticken(3000);
  assert.ok(fassung.zettel()); assert.equal(fassung.gtm(), 0);
});

test("Widerruf über Datenschutz-Einstellungen: Zettel mit aktuellem Stand, Ablehnen schaltet ab und löscht Cookies, Fokus zurück", () => {
  const p = seite({ tcfapi: false, speicher: { "rl-statistik-wahl": { v: 1, wahl: "ja", zeit: Date.now() } } });
  p.ticken(3000);
  assert.equal(p.gtm(), 1);
  p.einstellungsKnopf.focus();
  p.klick(p.einstellungsKnopf);
  assert.ok(p.zettel());
  assert.match(p.zettel().textContent, /aktuelle Wahl: zugestimmt/);
  assert.equal(p.document.activeElement.getAttribute("id"), "logbuch-titel", "Fokus in den Zettel");
  p.knopf("nein").focus();
  p.klick(p.knopf("nein"));
  assert.equal(p.window["ga-disable-G-T00HRG2YVF"], true);
  assert.ok(!p.jar.has("_ga") && !p.jar.has("_ga_T00HRG2YVF"));
  assert.equal(p.document.activeElement, p.einstellungsKnopf, "Fokus zurück zum Knopf");
});

test("Tastatur: Escape schließt ohne Zustimmung, Tasten erreichen das Spiel nicht", () => {
  const p = seite({ tcfapi: false });
  p.ticken(3000);
  const e = p.taste(p.knopf("ja"), "Enter");
  assert.ok(e.gestoppt, "Enter bleibt im Zettel");
  p.taste(p.knopf("ja"), "Escape");
  assert.equal(p.zettel(), null);
  assert.equal(p.wahl(), null, "keine Wahl gespeichert");
  assert.equal(p.gtm(), 0);
  assert.equal(p.window["ga-disable-G-T00HRG2YVF"], true);
});

test("Zustimmen und Ablehnen sind gleichrangig (gleiche Klasse, gleiches Element, keine Vorauswahl)", () => {
  const p = seite({ tcfapi: false }); p.ticken(3000);
  const [a, b] = [p.knopf("ja"), p.knopf("nein")];
  assert.equal(a.tagName, b.tagName); assert.equal(a.getAttribute("class"), b.getAttribute("class"));
  assert.ok(!a.hasAttribute("autofocus") && !b.hasAttribute("autofocus"));
  assert.equal(p.document.activeElement, null, "automatisch gezeigt: kein Fokusraub");
});

test("Seite ohne Werbung: kein Loader, kein Zettel von selbst, keine Messung; Widerruf möglich; nach Google-Wahl Verweis auf Google-Dialog", () => {
  const p = seite({ ohneWerbung: true, statisch: false, speicher: { "rl-statistik-wahl": { v: 1, wahl: "ja", zeit: Date.now() } } });
  p.ticken(5000);
  assert.equal(p.angehaengt.length, 0, "weder AdSense noch gtag.js");
  assert.equal(p.zettel(), null);
  p.klick(p.einstellungsKnopf);
  assert.equal(p.zettel().getAttribute("data-logbuch"), "wahl");
  p.klick(p.knopf("nein"));
  assert.equal(p.wahl().wahl, "nein"); assert.ok(!p.jar.has("_ga")); assert.equal(p.angehaengt.length, 0);
  const g = seite({ ohneWerbung: true, statisch: false, speicher: { "rl-einwilligung-google": { v: 1, zeit: Date.now() } } });
  g.klick(g.einstellungsKnopf);
  assert.equal(g.zettel().getAttribute("data-logbuch"), "google");
  assert.ok(alle(g.zettel(), k => k.getAttribute("href") === "/#datenschutz-einstellungen").length === 1);
});

test("Anker #datenschutz-einstellungen öffnet nach der Prüfung Zettel bzw. Google-Widerruf", () => {
  const p = seite({ tcfapi: false, hash: "#datenschutz-einstellungen" });
  p.ticken(3000);
  assert.ok(p.zettel()); assert.equal(p.document.activeElement.getAttribute("id"), "logbuch-titel");
  const g = seite({ hash: "#datenschutz-einstellungen" });
  g.tcf(GOOGLE_JA); g.ticken(3000);
  assert.equal(g.zettel(), null);
  assert.ok(g.window.googlefc.callbackQueue.some(f => typeof f === "function"));
});

test("localStorage gesperrt: kein Absturz, Zettel erscheint trotzdem", () => {
  const p = seite({ tcfapi: false });
  p.window.localStorage.getItem = () => { throw new Error("blockiert"); };
  p.window.localStorage.setItem = () => { throw new Error("blockiert"); };
  p.ticken(3000);
  assert.ok(p.zettel());
  p.klick(p.knopf("ja"));
  assert.equal(p.gtm(), 1);
});

test("„×“ schließt ohne zu entscheiden; Freiraum unten nur, solange der Zettel offen ist; Titel ist h2", () => {
  const p = seite({ tcfapi: false });
  p.document.body.style.paddingBottom = "4px";
  p.ticken(3000);
  const titel = alle(p.zettel(), k => k.getAttribute("id") === "logbuch-titel")[0];
  assert.equal(titel.tagName, "H2");
  assert.equal(p.document.body.style.paddingBottom, "328px", "Seitenfuß bleibt erreichbar");
  const x = p.knopf("zu");
  assert.equal(x.getAttribute("aria-label"), "Schließen, ohne zu entscheiden");
  assert.notEqual(x.getAttribute("class"), p.knopf("ja").getAttribute("class"), "leiser als die Entscheidungsknöpfe");
  p.klick(x);
  assert.equal(p.zettel(), null);
  assert.equal(p.wahl(), null, "nichts gespeichert");
  assert.equal(p.gtm(), 0); assert.equal(p.window["ga-disable-G-T00HRG2YVF"], true);
  assert.equal(p.document.body.style.paddingBottom, "4px", "Freiraum zurückgesetzt");
});

test("Google-Dialog sichtbar, aber unentschieden: keine neue eigene Abfrage; bereits getroffene eigene Wahl gilt bis zur Google-Entscheidung", () => {
  const offen = seite();
  offen.tcf(VERBORGEN); offen.ticken(3000);
  assert.ok(offen.zettel());
  offen.tcf({ ...VERBORGEN, eventStatus: "cmpuishown", displayStatus: "visible" });
  assert.equal(offen.zettel(), null, "Zettel weicht dem Google-Dialog");
  offen.tcf(VERBORGEN); offen.ticken(5000);
  assert.equal(offen.zettel(), null, "keine neue Abfrage");
  assert.equal(offen.gtm(), 0);
  const ja = seite({ speicher: { "rl-statistik-wahl": { v: 1, wahl: "ja", zeit: Date.now() } } });
  ja.tcf(VERBORGEN); ja.ticken(3000);
  assert.equal(ja.window["ga-disable-G-T00HRG2YVF"], false);
  ja.tcf({ ...VERBORGEN, eventStatus: "cmpuishown", displayStatus: "visible" });
  assert.equal(ja.window["ga-disable-G-T00HRG2YVF"], false, "eigene Wahl gilt weiter");
  ja.tcf(GOOGLE_NEIN);
  assert.equal(ja.window["ga-disable-G-T00HRG2YVF"], true, "Google-Entscheidung hat Vorrang");
  const sofort = seite({ speicher: { "rl-statistik-wahl": { v: 1, wahl: "ja", zeit: Date.now() } } });
  sofort.tcf({ ...VERBORGEN, eventStatus: "cmpuishown", displayStatus: "visible" }); sofort.ticken(5000);
  assert.equal(sofort.gtm(), 0, "Dialog schon beim Aufruf sichtbar: Statistik bleibt aus");
  assert.equal(sofort.zettel(), null);
});

test("Zeichen: kein hebräisches Dalet (U+05D3) statt „×“ in den Quellen", () => {
  for (const f of ["assets/consent.js", "assets/style.css", "content/privacy_body.html", "templates/base.html", "build.py", "test_consent.js"]) {
    assert.ok(!fs.readFileSync(__dirname + "/" + f, "utf8").includes("\u05d3"), f);
  }
  assert.ok(SRC.includes("\u00d7"), "„×“ (U+00D7) im Zettel");
});

test("Google-Nein gleich beim Laden (Zettel nie aktiv): gespeichertes eigenes Ja verworfen, _ga-Cookies gelöscht", () => {
  const p = seite({ speicher: { "rl-statistik-wahl": { v: 1, wahl: "ja", zeit: Date.now() - 864e5 } } });
  p.tcf(GOOGLE_NEIN);
  assert.ok(!p.jar.has("_ga") && !p.jar.has("_ga_T00HRG2YVF"), "Cookies weg, ohne dass der Zettel aktiv war");
  assert.ok(p.jar.has("rl-andere"));
  assert.equal(p.wahl(), null);
  p.ticken(5000);
  assert.equal(p.zettel(), null); assert.equal(p.gtm(), 0);
  const ohneWahl = seite();   // nur alte Cookies, keine eigene Wahl
  ohneWahl.tcf(GOOGLE_NEIN);
  assert.ok(!ohneWahl.jar.has("_ga"));
});

test("Zeitstempel aus der Zukunft (> 1 Tag) wird verworfen: neu fragen, nicht messen", () => {
  const p = seite({ tcfapi: false, speicher: { "rl-statistik-wahl": { v: 1, wahl: "ja", zeit: Date.now() + 3 * 864e5 } } });
  p.ticken(3000);
  assert.ok(p.zettel()); assert.equal(p.gtm(), 0);
  const knapp = seite({ tcfapi: false, speicher: { "rl-statistik-wahl": { v: 1, wahl: "ja", zeit: Date.now() + 36e5 } } });
  knapp.ticken(3000);
  assert.equal(knapp.zettel(), null, "kleine Uhrabweichung (1 h) wird toleriert"); assert.equal(knapp.gtm(), 1);
});
