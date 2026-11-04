// Automatischer Test für assets/consent.js (node --test test_consent.js): AdSense-Loader nie doppelt,
// Consent-Default nicht wiederholt, Global Privacy Control hält Anzeigenanfragen an, Statistik nur mit Einwilligung.
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("fs");
const vm = require("vm");
const SRC = fs.readFileSync(__dirname + "/assets/consent.js", "utf8");
const LOADER = "https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7811071715414905";

function seite({ statisch = true, kopfDefault = true, gpc = false, slots = [] } = {}) {
  const angehaengt = [], befehle = [];
  let tcf = null;
  const document = {
    head: { appendChild: s => angehaengt.push(s) },
    createElement: () => ({ dataset: {}, style: {}, classList: { add() {}, remove() {} } }),
    querySelector: sel => (statisch && /adsbygoogle\.js/.test(sel) ? { src: LOADER } : null),
    querySelectorAll: () => slots,
    addEventListener() {}
  };
  const window = {
    document, navigator: { globalPrivacyControl: gpc }, setTimeout: () => 0, Date,
    googlefc: { callbackQueue: [], getGoogleConsentModeValues: () => ({ analyticsStoragePurposeConsentStatus: 1 }) },
    __tcfapi: (cmd, v, cb) => { if (cmd === "addEventListener") tcf = cb; }
  };
  window.window = window;
  window.dataLayer = [];
  window.gtag = (...a) => befehle.push(a);
  if (kopfDefault) {   // wie das Inline-Skript im <head>
    window.gtag("consent", "default", { ad_storage: "denied", ad_user_data: "denied", ad_personalization: "denied", analytics_storage: "denied", wait_for_update: 500 });
    window["ga-disable-G-T00HRG2YVF"] = true; window.rlConsentDefault = true;
  }
  vm.runInContext(SRC, vm.createContext(window));
  return { window, angehaengt, befehle, tcf: d => tcf(d, true) };
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
  p.tcf({ gdprApplies: true, eventStatus: "tcloaded", purpose: { consents: { 1: true } }, vendor: { consents: { 755: true } } });
  assert.equal(p.window["ga-disable-G-T00HRG2YVF"], true);
  assert.ok(!p.angehaengt.some(s => /googletagmanager/.test(s.src || "")));
});

test("DSGVO: Statistik nur mit Zweck 1 + Anbieter 755 + Consent Mode GRANTED; ohne Einwilligung bleibt sie aus", () => {
  const nein = seite();
  nein.tcf({ gdprApplies: true, eventStatus: "tcloaded", purpose: { consents: {} }, vendor: { consents: {} } });
  assert.equal(nein.window["ga-disable-G-T00HRG2YVF"], true);
  assert.ok(!nein.angehaengt.some(s => /googletagmanager/.test(s.src || "")));
  const ja = seite();
  ja.tcf({ gdprApplies: true, eventStatus: "useractioncomplete", purpose: { consents: { 1: true } }, vendor: { consents: { 755: true } } });
  assert.equal(ja.window["ga-disable-G-T00HRG2YVF"], false);
  assert.ok(ja.angehaengt.some(s => /googletagmanager/.test(s.src || "")));
});
