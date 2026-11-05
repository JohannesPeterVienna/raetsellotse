/* Werbung und Statistik — beides läuft über Googles zertifizierte Einwilligungsverwaltung (TCF 2.2).
   Der AdSense-Loader steht statisch im <head>, direkt nach einem Inline-Skript mit dem Consent-Default (alles denied).
   Ablauf Statistik:
   1) Sofort, vor allen Google-Skripten (im <head>; hier nur als Rückfall): gtag-Warteschlange + consent default (alles denied, 500 ms), ga-disable an.
   2) Bei jeder Meldung der Google-CMP (TCF-Ereignis, CONSENT_MODE_DATA_READY, US-Status) wird neu entschieden.
      DSGVO-Zweig: messen nur bei TCF Zweck 1 + Anbieter 755 UND Consent Mode analytics GRANTED (1).
      Außerhalb der DSGVO (gdprApplies false): nur bei GRANTED (1) oder NOT_APPLICABLE (3) und wenn die CMP
      ausdrücklich keinen US-Opt-out meldet (Status 1/2). Fehlend/UNKNOWN (0)/DENIED (2)/NOT_CONFIGURED (4)/Schnittstellenfehler = nicht messen.
      Ein TCF-Nein entscheidet sofort, ohne die Consent-Mode-Schnittstelle zu fragen.
   3) Ablehnung oder Widerruf: consent update denied + ga-disable → keine weiteren Treffer.
   Statuswerte: developers.google.com/funding-choices/fc-api-docs. Signals/Werbepersonalisierung aus.

   Übergang (seit 4.11.2026), nur Statistik – der „Logbuch-Zettel“:
   Liefert die Google-CMP nach 3 s keine echte TCF-Entscheidung (kein __tcfapi oder TCData ohne
   „useractioncomplete“ bzw. „tcloaded“ mit tcString, Meldung nicht sichtbar) und meldet sie nicht gdprApplies false,
   fragt Rätsellotse selbst – nur nach Google Analytics. Zustimmen: analytics_storage granted + gtag.js.
   Ablehnen/Widerruf: analytics_storage denied, ga-disable, _ga-Cookies löschen. ad_storage, ad_user_data und
   ad_personalization fasst der Zettel nie an. Wahl in localStorage „rl-statistik-wahl“ (Version, Zeitpunkt), 12 Monate.
   Sobald Google echt entscheidet, gilt nur noch die Logik oben; der Zettel verschwindet, die eigene Wahl wird gelöscht.
   GPC: Statistik bleibt aus, der Zettel drängt sich nicht auf. Seiten ohne Werbung (Impressum, Datenschutz, Archiv, 404)
   laden dieses Skript mit data-ohne-werbung: keine Anzeigen, keine Messung, nur der Knopf „Datenschutz-Einstellungen“. */
(() => {
  const PUB = "ca-pub-7811071715414905";
  const GA = "G-T00HRG2YVF";
  const GOOGLE_VENDOR = 755;
  const SPERRE = "ga-disable-" + GA;
  const STATUS = { UNKNOWN: 0, GRANTED: 1, DENIED: 2, NOT_APPLICABLE: 3, NOT_CONFIGURED: 4 };
  const US_KEIN_OPTOUT = [1, 2];   // usstatesoptout: DOES_NOT_APPLY, NOT_OPTED_OUT; 0 UNKNOWN / 3 OPTED_OUT sperren

  window.dataLayer = window.dataLayer || [];
  const gtag = window.gtag = typeof window.gtag === "function" ? window.gtag : function(){ window.dataLayer.push(arguments); };
  window[SPERRE] = true;
  // Der Standard steht schon im <head> vor dem AdSense-Loader; nur ohne ihn (z. B. ältere Seiten im Cache) hier setzen.
  if (!window.rlConsentDefault) {
    gtag("consent", "default", { ad_storage: "denied", ad_user_data: "denied", ad_personalization: "denied", analytics_storage: "denied", wait_for_update: 500 });
    window.rlConsentDefault = true;
  }
  window.googlefc = window.googlefc || {};
  window.googlefc.callbackQueue = window.googlefc.callbackQueue || [];

  // Anzeigenblöcke: Block-IDs werden nach der AdSense-Freigabe hier eingetragen.
  // Gemeinsame AdSense-Blöcke „Themen-Websites – …“ (Konto pub-7811071715414905, angelegt 17.10. und 5.11.2026)
  const SLOTS = { billboard: "7497607759", rect: "1292301217", half: "1292301217", superbanner: "5774811012", sky: "5064364572", mbanner: "5396758258" };
  // Feste IAB-Formate: Superbanner 728×90, Wide Skyscraper 160×600. Die übrigen Plätze sind responsiv
  // (Billboard 970×250 / Leaderboard 728×90 / Mobile 320×100, Half Page 300×600, Medium Rectangle 300×250).
  const FIXED = { superbanner: [728, 90], sky: [160, 600], mbanner: [320, 100] };

  const gpc = navigator.globalPrivacyControl === true;
  const skript = document.currentScript;
  const ohneWerbung = !!(skript && skript.hasAttribute && skript.hasAttribute("data-ohne-werbung"));

  function loadAds(){
    if (gpc) { (window.adsbygoogle = window.adsbygoogle || []).pauseAdRequests = 1; return; }   // keine Anzeigenanfragen
    // Der Loader steht statisch im <head>; nur falls er fehlt, wird er hier nachgeladen – nie doppelt.
    if (!document.querySelector('script[src*="pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"]')) {
      const s = document.createElement("script");
      s.async = true; s.crossOrigin = "anonymous";
      s.src = `https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=${PUB}`;
      document.head.appendChild(s);
    }
    document.querySelectorAll(".ad[data-ad]").forEach(box => {
      const id = SLOTS[box.dataset.ad];
      if (!id) return;
      box.classList.add("on");
      if (box.offsetParent === null) { box.classList.remove("on"); return; }   // auf diesem Bildschirm ausgeblendet
      const ins = document.createElement("ins");
      ins.className = "adsbygoogle"; ins.dataset.adClient = PUB; ins.dataset.adSlot = id;
      const fixed = FIXED[box.dataset.ad];
      if (fixed) { ins.style.cssText = `display:inline-block;width:${fixed[0]}px;height:${fixed[1]}px`; }
      else {
        ins.style.display = "block";
        ins.dataset.adFormat = box.dataset.ad === "half" ? "vertical" : "auto";
        ins.dataset.fullWidthResponsive = "true";
      }
      box.appendChild(ins);
      aufAnzeigeWarten(box, ins);
      (window.adsbygoogle = window.adsbygoogle || []).push({});
    });
  }

  // Ohne :has() zeigt style.css Beschriftung und Abstände über .ad--belegt – gesetzt erst, wenn Google
  // data-ad-status="filled" oder "unfill-optimized" an das <ins> schreibt. Das <ins> selbst bleibt immer sichtbar.
  function aufAnzeigeWarten(box, ins){
    if (!(window.CSS && CSS.supports && CSS.supports("selector(:has(a))"))) document.documentElement.classList.add("kein-has");
    const status = () => box.classList.toggle("ad--belegt", ["filled", "unfill-optimized"].includes(ins.getAttribute("data-ad-status")));
    status();
    if (typeof MutationObserver === "function") new MutationObserver(status).observe(ins, { attributes: true, attributeFilter: ["data-ad-status"] });
  }

  const lage = { tc: null, misst: false, gesperrtGemeldet: false, tagDa: false };

  const zugestimmt = (liste, id) => !!(liste && liste.consents && liste.consents[id]);

  function statistikLautCmp(){
    const fc = window.googlefc;
    if (!fc || typeof fc.getGoogleConsentModeValues !== "function") return STATUS.UNKNOWN;
    try {
      const w = fc.getGoogleConsentModeValues().analyticsStoragePurposeConsentStatus;
      return Number.isInteger(w) ? w : STATUS.UNKNOWN;
    } catch (_) { return STATUS.UNKNOWN; }
  }

  function usOptOutGemeldet(){
    try {
      const u = window.googlefc && window.googlefc.usstatesoptout;
      return !(u && typeof u.getInitialUsStatesOptOutStatus === "function" && US_KEIN_OPTOUT.includes(u.getInitialUsStatesOptOutStatus()));
    } catch (_) { return true; }
  }

  // Echte TCF-Entscheidung: Nutzer hat im Google-Dialog gewählt, oder eine gespeicherte Wahl (tcString) wurde geladen
  const cmpEntschieden = tc => !!tc && (tc.eventStatus === "useractioncomplete" ||
    (tc.eventStatus === "tcloaded" && typeof tc.tcString === "string" && tc.tcString.length > 0));

  // "ja" | "nein" | "offen"
  function urteil(){
    const tc = lage.tc;
    if (gpc) return "nein";
    if (!tc) return "offen";
    if (tc.gdprApplies === false){
      const cm = statistikLautCmp();
      return (cm === STATUS.GRANTED || cm === STATUS.NOT_APPLICABLE) && !usOptOutGemeldet() ? "ja" : "nein";
    }
    if (!cmpEntschieden(tc)) return "offen";   // z. B. Meldung verborgen, tcloaded ohne tcString
    if (!zugestimmt(tc.purpose, 1) || !zugestimmt(tc.vendor, GOOGLE_VENDOR)) return "nein";   // ohne weitere CMP-Abfrage
    return statistikLautCmp() === STATUS.GRANTED ? "ja" : "nein";
  }

  function einschalten(){
    window[SPERRE] = false;
    gtag("consent", "update", { analytics_storage: "granted" });
    if (!lage.tagDa){
      lage.tagDa = true;
      gtag("js", new Date());
      const tag = document.createElement("script"); tag.async = true;
      tag.src = "https://www.googletagmanager.com/gtag/js?id=" + GA;
      document.head.appendChild(tag);
    }
    gtag("config", GA, { allow_google_signals: false, allow_ad_personalization_signals: false });
    lage.misst = true; lage.gesperrtGemeldet = false;
  }

  function ausschalten(){
    window[SPERRE] = true;
    const ohneSpeichern = !zugestimmt(lage.tc && lage.tc.purpose, 1);
    gtag("consent", "update", Object.assign({ analytics_storage: "denied" },
      ohneSpeichern ? { ad_storage: "denied", ad_user_data: "denied", ad_personalization: "denied" } : {}));
    lage.misst = false; lage.gesperrtGemeldet = true;
    analyseSpurenTilgen();   // auch bei Google-Nein gleich beim Laden: alte _ga-Cookies (z. B. aus einem früheren Ja) entfernen
  }

  /* ---------- Logbuch-Zettel: eigenes Übergangsfenster nur für die Statistik ---------- */
  const PRUEF_MS = 3000;
  const WAHL = "rl-statistik-wahl", GOOGLE_MERKER = "rl-einwilligung-google", FASSUNG = 1, MONATE = 12;
  const ANKER = "#datenschutz-einstellungen";
  const zettel = { aktiv: false, abgeloest: false, faellig: false, wunsch: false, el: null, zurueck: null };

  function lesen(schluessel){
    try {
      const w = JSON.parse(window.localStorage.getItem(schluessel));
      if (!w || w.v !== FASSUNG || !Number.isFinite(w.zeit)) return null;
      if (w.zeit > Date.now() + 864e5) return null;   // Zeitstempel aus der Zukunft (verstellte Uhr, Manipulation) gilt nicht
      const bis = new Date(w.zeit); bis.setMonth(bis.getMonth() + MONATE);
      return Date.now() < bis.getTime() ? w : null;   // nach 12 Monaten neu fragen
    } catch (_) { return null; }
  }
  function schreiben(schluessel, daten){
    try { window.localStorage.setItem(schluessel, JSON.stringify(Object.assign({ v: FASSUNG, zeit: Date.now() }, daten))); } catch (_) {}
  }
  function vergessen(schluessel){ try { window.localStorage.removeItem(schluessel); } catch (_) {} }
  function eigeneWahl(){ const w = lesen(WAHL); return w && (w.wahl === "ja" || w.wahl === "nein") ? w : null; }

  // _ga und _ga_<ID> auf allen Domain-Stufen löschen (GA setzt sie meist auf .raetsellotse.de)
  function analyseSpurenTilgen(){
    let namen = [];
    try { namen = document.cookie.split(";").map(k => k.split("=")[0].trim()).filter(n => /^_ga($|_)/.test(n)); } catch (_) { return; }
    const teile = String((window.location && window.location.hostname) || "").split(".");
    const domains = [""];
    for (let k = 0; k < teile.length - 1; k++){ const d = teile.slice(k).join("."); domains.push(";domain=" + d, ";domain=." + d); }
    namen.forEach(n => domains.forEach(d => { document.cookie = n + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT;max-age=0;path=/" + d; }));
  }

  function eigenAus(){
    window[SPERRE] = true;
    gtag("consent", "update", { analytics_storage: "denied" });   // Werbe-Signale bleiben, wie sie sind
    analyseSpurenTilgen();
    lage.misst = false;
  }

  function wahlTreffen(wahl){
    schreiben(WAHL, { wahl });
    if (!ohneWerbung && zettel.aktiv) { wahl === "ja" ? einschalten() : eigenAus(); }
    else if (wahl === "nein") eigenAus();   // Seiten ohne Werbung: nie messen, aber Widerruf sofort wirksam
    zettelWeg();
  }

  const datum = z => new Date(z).toLocaleDateString("de-AT", { day: "numeric", month: "long", year: "numeric" });

  function teil(tag, attr, ...kinder){
    const el = document.createElement(tag);
    Object.keys(attr || {}).forEach(k => el.setAttribute(k, attr[k]));
    if (kinder.length) el.append(...kinder);
    return el;
  }
  const datenschutzLink = () => teil("a", { href: "/privacy.html#statistik-uebergang" }, "Datenschutzerklärung");

  // art: "wahl" (Zustimmen/Ablehnen) | "gpc" (Hinweis) | "google" (Wahl liegt bei Google)
  function zettelZeigen(art, mitFokus){
    const vorher = document.activeElement;
    const warDrin = !!(zettel.el && zettel.el.contains && zettel.el.contains(vorher));
    zettelWeg(true);
    const knoepfe = [], text = [];
    if (art === "wahl"){
      text.push(teil("p", {}, "Wir würden mit Google Analytics (Google Ireland Ltd.) und Cookies zählen, welche Seiten besucht werden – nur Statistik, keine Werbung. Google kann Daten auch in den USA verarbeiten."));
      text.push(teil("p", { class: "logbuch__stand" }, "Widerruf jederzeit: „Datenschutz-Einstellungen“ im Seitenfuß · ", datenschutzLink()));
      const w = eigeneWahl();
      if (w) text.push(teil("p", { class: "logbuch__stand" }, `Deine aktuelle Wahl: ${w.wahl === "ja" ? "zugestimmt" : "abgelehnt"} am ${datum(w.zeit)}.`));
      if (ohneWerbung) text.push(teil("p", { class: "logbuch__stand" }, "Auf dieser Seite wird nie gemessen; deine Wahl gilt für die Rätsel- und Beitragsseiten."));
      knoepfe.push(teil("button", { type: "button", class: "logbuch__knopf", "data-logbuch-wahl": "ja" }, "Zustimmen"),
                   teil("button", { type: "button", class: "logbuch__knopf", "data-logbuch-wahl": "nein" }, "Ablehnen"));
    } else if (art === "gpc"){
      text.push(teil("p", {}, "Dein Browser sendet das Signal „Global Privacy Control“. Wir werten es als Nein: Die Besucherstatistik (Google Analytics) bleibt aus, und wir fragen nicht weiter nach. Mehr in der ", datenschutzLink(), "."));
      knoepfe.push(teil("button", { type: "button", class: "logbuch__knopf", "data-logbuch-zu": "" }, "Verstanden"));
    } else {
      text.push(teil("p", {}, "Deine Auswahl zu Werbung und Statistik hast du im Einwilligungsdialog von Google getroffen. Ändern oder widerrufen kannst du sie auf jeder Seite mit Rätseln oder Beiträgen – zum Beispiel auf der Startseite. Mehr in der ", datenschutzLink(), "."));
      knoepfe.push(teil("a", { class: "logbuch__knopf", href: "/" + ANKER }, "Zur Startseite und ändern"),
                   teil("button", { type: "button", class: "logbuch__knopf", "data-logbuch-zu": "" }, "Schließen"));
    }
    const titel = teil("h2", { class: "logbuch__titel", id: "logbuch-titel", tabindex: "-1" },
      art === "wahl" ? "Besuche ins Logbuch eintragen?" : "Deine Datenschutz-Einstellungen");
    // Neutrales „×“: nur wegklappen, nichts speichern – bewusst leiser als die zwei Entscheidungsknöpfe
    if (art === "wahl") knoepfe.push(teil("button", { type: "button", class: "logbuch__weg", "data-logbuch-zu": "", "aria-label": "Schließen, ohne zu entscheiden" }, "×"));
    const el = teil("section", { class: "logbuch", role: "region", "aria-labelledby": "logbuch-titel", "data-logbuch": art },
      teil("span", { class: "logbuch__boje", "aria-hidden": "true" }), titel, ...text, teil("div", { class: "logbuch__wahl" }, ...knoepfe));
    el.addEventListener("click", e => {
      const b = e.target.closest && e.target.closest("[data-logbuch-wahl],[data-logbuch-zu]");
      if (!b) return;
      if (b.hasAttribute("data-logbuch-wahl")) wahlTreffen(b.getAttribute("data-logbuch-wahl"));
      else zettelWeg();
    });
    // Tasten bleiben im Zettel (sonst würde z. B. Enter im Codeknacker einen Tipp abschicken).
    // Escape schließt nur für diesen Seitenaufruf – ohne Zustimmung, die Statistik bleibt aus.
    el.addEventListener("keydown", e => { e.stopPropagation(); if (e.key === "Escape") zettelWeg(); });
    const skip = document.querySelector(".skip");
    // Direkt hinter „Zum Inhalt“ einhängen: Tastatur erreicht den Zettel nach wenigen Tabs, sichtbar ist er am unteren Rand
    if (skip && skip.after) skip.after(el); else document.body.prepend(el);
    zettel.el = el;
    freiraumSetzen();
    if (mitFokus && !warDrin) zettel.zurueck = vorher;
    if (mitFokus || warDrin) titel.focus();
  }

  // Unten so viel Luft lassen, wie der Zettel hoch ist: Seitenfuß bleibt erreichbar, solange er offen ist
  let freiraumVorher = null;
  function freiraumSetzen(){
    const el = zettel.el, st = document.body && document.body.style;
    if (!el || !st || !el.offsetHeight) return;
    if (freiraumVorher === null) freiraumVorher = st.paddingBottom || "";
    st.paddingBottom = (el.offsetHeight + 28) + "px";
  }
  function freiraumWeg(){
    if (freiraumVorher === null || !document.body || !document.body.style) return;
    document.body.style.paddingBottom = freiraumVorher; freiraumVorher = null;
  }
  if (window.addEventListener) window.addEventListener("resize", freiraumSetzen);

  function zettelWeg(still){
    const el = zettel.el; if (!el) return;
    const fokusDrin = el.contains && el.contains(document.activeElement);
    el.remove(); zettel.el = null;
    if (!still) freiraumWeg();
    if (still) return;   // wird gleich neu aufgebaut
    const z = zettel.zurueck; zettel.zurueck = null;
    if (fokusDrin && z && z.focus && z.isConnected !== false) z.focus();
  }

  // Nach 3 s (oder früher auf Knopfdruck): Übergang nötig? Liefert true, wenn der Zettel zuständig ist.
  function uebergangPruefen(){
    if (zettel.aktiv) return true;
    if (ohneWerbung || gpc || zettel.abgeloest) return false;
    const tc = lage.tc;
    if (cmpEntschieden(tc) || (tc && tc.gdprApplies === false) || (tc && tc.displayStatus === "visible")) return false;
    zettel.aktiv = true;
    vergessen(GOOGLE_MERKER);
    const w = eigeneWahl();
    if (!w) zettelZeigen("wahl", false);
    else if (w.wahl === "ja") einschalten();
    else eigenAus();
    return true;
  }

  // Google hat entschieden (oder meldet gdprApplies false): ab jetzt nur noch die bestehende Logik
  function uebergangBeenden(){
    zettel.aktiv = false; zettel.abgeloest = true;
    zettelWeg();
    vergessen(WAHL);   // auch bei gdprApplies false: die eigene Wahl gilt nicht mehr
    lage.gesperrtGemeldet = false;   // damit ein Google-Nein vollständig angewendet wird
  }

  function googleWiderruf(){
    const fc = window.googlefc;
    fc.callbackQueue.push(() => { if (typeof fc.showRevocationMessage === "function") fc.showRevocationMessage(); });
  }

  function einstellungenOeffnen(){
    if (ohneWerbung) return zettelZeigen(gpc ? "gpc" : lesen(GOOGLE_MERKER) ? "google" : "wahl", true);
    if (gpc && !cmpEntschieden(lage.tc)) return zettelZeigen("gpc", true);
    if (uebergangPruefen()) return zettelZeigen("wahl", true);
    googleWiderruf();
  }

  function neuBewerten(){
    const u = urteil();
    if (cmpEntschieden(lage.tc)){   // Google hat Vorrang: eigene Wahl verwerfen; Merker für Seiten ohne Werbung
      schreiben(GOOGLE_MERKER, {}); vergessen(WAHL);
    }
    if (zettel.aktiv){
      if (u === "offen"){
        if (lage.tc && lage.tc.displayStatus === "visible") zettelWeg();   // Google zeigt seine Meldung doch noch
        return;   // sonst gilt die eigene Wahl
      }
      const gemessen = lage.misst;
      uebergangBeenden();
      if (u === "nein" && gemessen){ ausschalten(); return; }
    } else if (u === "offen" && zettel.faellig && !zettel.abgeloest) { uebergangPruefen(); return; }
    else if (u !== "offen") zettel.abgeloest = true;
    if (u === "ja" && !lage.misst) einschalten();
    else if (u === "nein" && !lage.gesperrtGemeldet) ausschalten();
    else if (u === "offen" && lage.misst) ausschalten();   // nach Widerruf ist die Einwilligung gelöscht
  }

  function watchConsent(tries = 0){
    if (typeof window.__tcfapi !== "function"){
      if (tries < 40) setTimeout(() => watchConsent(tries + 1), 250);
      return;
    }
    window.__tcfapi("addEventListener", 2, (tc, ok) => {
      if (!ok || !tc) return;
      lage.tc = tc;
      neuBewerten();
      setTimeout(neuBewerten, 300);   // Consent-Mode-Werte der CMP können nachziehen
    });
  }
  window.googlefc.callbackQueue.push({ CONSENT_MODE_DATA_READY: neuBewerten, INITIAL_US_STATES_OPT_OUT_DATA_READY: neuBewerten });

  // Knopf „Datenschutz-Einstellungen" im Seitenfuß: im Übergang der Logbuch-Zettel, sonst der Google-Widerrufsdialog
  document.addEventListener("click", e => {
    if (!e.target.closest || !e.target.closest("[data-privacy-settings]")) return;
    einstellungenOeffnen();
  });
  const mitAnker = !!(window.location && window.location.hash === ANKER);

  if (ohneWerbung) { if (mitAnker) einstellungenOeffnen(); return; }
  loadAds();
  watchConsent();
  zettel.wunsch = mitAnker;
  setTimeout(() => {
    zettel.faellig = true;
    const zustaendig = uebergangPruefen();
    if (!zettel.wunsch) return;
    zettel.wunsch = false;
    if (gpc && !cmpEntschieden(lage.tc)) zettelZeigen("gpc", true);
    else if (zustaendig) zettelZeigen("wahl", true);
    else googleWiderruf();
  }, PRUEF_MS);
})();
