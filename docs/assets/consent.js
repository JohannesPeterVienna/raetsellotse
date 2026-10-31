/* Werbung und Statistik — beides läuft über Googles zertifizierte Einwilligungsverwaltung (TCF 2.2).
   Ablauf Statistik:
   1) Sofort, vor allen Google-Skripten: gtag-Warteschlange + consent default (alles denied, 500 ms).
   2) Bei jeder Meldung der Google-CMP (TCF-Ereignis, CONSENT_MODE_DATA_READY) wird neu entschieden.
      Messen nur, wenn TCF Zweck 1 + Anbieter 755 UND Consent Mode analytics_storage GRANTED melden.
      Unbekannt/fehlend = nicht messen. Außerhalb der DSGVO (gdprApplies false) ohne Ablehnung = messen.
   3) Ablehnung oder Widerruf: consent update denied + ga-disable → keine weiteren Treffer.
   Signals und Werbepersonalisierung sind in Analytics deaktiviert. */
(() => {
  const PUB = "ca-pub-7811071715414905";
  const GA = "G-T00HRG2YVF";
  const GOOGLE_VENDOR = 755;
  const SPERRE = "ga-disable-" + GA;
  const STATUS = { UNKNOWN: 0, GRANTED: 1, DENIED: 2 };

  window.dataLayer = window.dataLayer || [];
  const gtag = window.gtag = typeof window.gtag === "function" ? window.gtag : function(){ window.dataLayer.push(arguments); };
  window[SPERRE] = true;
  gtag("consent", "default", { ad_storage: "denied", ad_user_data: "denied", ad_personalization: "denied", analytics_storage: "denied", wait_for_update: 500 });
  window.googlefc = window.googlefc || {};
  window.googlefc.callbackQueue = window.googlefc.callbackQueue || [];

  // Anzeigenblöcke: Block-IDs werden nach der AdSense-Freigabe hier eingetragen.
  const SLOTS = { billboard: "", rect: "", half: "", superbanner: "", sky: "" };
  // Feste IAB-Formate: Superbanner 728×90, Wide Skyscraper 160×600. Die übrigen Plätze sind responsiv
  // (Billboard 970×250 / Leaderboard 728×90 / Mobile 320×100, Half Page 300×600, Medium Rectangle 300×250).
  const FIXED = { superbanner: [728, 90], sky: [160, 600] };

  const gpc = navigator.globalPrivacyControl === true;

  function loadAds(){
    if (gpc) return;
    const s = document.createElement("script");
    s.async = true; s.crossOrigin = "anonymous";
    s.src = `https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=${PUB}`;
    document.head.appendChild(s);
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
      (window.adsbygoogle = window.adsbygoogle || []).push({});
    });
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

  // "ja" | "nein" | "offen"
  function urteil(){
    const cm = statistikLautCmp(), tc = lage.tc;
    if (gpc || cm === STATUS.DENIED) return "nein";
    if (!tc) return "offen";
    if (tc.gdprApplies === false) return "ja";
    if (!["tcloaded", "useractioncomplete"].includes(tc.eventStatus)) return "offen";
    return zugestimmt(tc.purpose, 1) && zugestimmt(tc.vendor, GOOGLE_VENDOR) && cm === STATUS.GRANTED ? "ja" : "nein";
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
  }

  function neuBewerten(){
    const u = urteil();
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
  window.googlefc.callbackQueue.push({ CONSENT_MODE_DATA_READY: neuBewerten });

  // Link „Datenschutz-Einstellungen" im Seitenfuß öffnet den Google-Dialog erneut
  document.addEventListener("click", e => {
    if (!e.target.closest("[data-privacy-settings]")) return;
    const fc = window.googlefc;
    fc.callbackQueue.push(() => { if (typeof fc.showRevocationMessage === "function") fc.showRevocationMessage(); });
  });

  loadAds();
  watchConsent();
})();
