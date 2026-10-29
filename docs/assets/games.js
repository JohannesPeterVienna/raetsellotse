/* Rätsellotse — tägliche Rätsel. Gleiche Aufgabe für alle am selben Tag (Datum in Wien), Fortschritt nur im Browser. */
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const store = {
    get(k, d) { try { const v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch { return d; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch {} }
  };
  const todayVienna = () => new Intl.DateTimeFormat("en-CA", { timeZone: "Europe/Vienna", year: "numeric", month: "2-digit", day: "2-digit" }).format(new Date());
  const fmtDate = iso => { const [y, m, d] = iso.split("-"); return `${+d}.${+m}.${y}`; };
  const hash = s => { let h1 = 0xdeadbeef, h2 = 0x41c6ce57; for (let i = 0; i < s.length; i++) { const c = s.charCodeAt(i); h1 = Math.imul(h1 ^ c, 2654435761); h2 = Math.imul(h2 ^ c, 1597334677); } h1 = Math.imul(h1 ^ (h1 >>> 16), 2246822507) ^ Math.imul(h2 ^ (h2 >>> 13), 3266489909); return h1 >>> 0; };
  const rng = seed => () => { seed |= 0; seed = seed + 0x6D2B79F5 | 0; let t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  const shuffle = (a, r) => { for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(r() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };

  function dayFromUrl() {
    const q = new URLSearchParams(location.search).get("tag");
    const t = todayVienna();
    return q && /^\d{4}-\d{2}-\d{2}$/.test(q) && q <= t && q >= "2026-01-01" ? q : t;
  }
  function streak(game, day, won) {
    const s = store.get(`rl-streak-${game}`, { last: null, n: 0, best: 0 });
    if (s.last === day) return s;
    if (won) {
      const y = new Date(day + "T12:00:00Z"); y.setUTCDate(y.getUTCDate() - 1);
      s.n = s.last === y.toISOString().slice(0, 10) ? s.n + 1 : 1; s.best = Math.max(s.best, s.n);
    } else s.n = 0;
    s.last = day; store.set(`rl-streak-${game}`, s); return s;
  }
  function share(text, btn) {
    const done = () => { const o = btn.textContent; btn.textContent = "Kopiert"; setTimeout(() => btn.textContent = o, 1600); };
    if (navigator.share && matchMedia("(pointer:coarse)").matches) navigator.share({ text }).catch(() => {});
    else navigator.clipboard?.writeText(text).then(done, () => prompt("Zum Kopieren:", text));
  }
  function dayNav(root, day, game) {
    const el = $("[data-daynav]", root); if (!el) return;
    const t = todayVienna();
    el.innerHTML = `<span>Rätsel vom <strong>${fmtDate(day)}</strong>${day === t ? " (heute)" : ""}</span>
      <label class="small">Archiv <input type="date" value="${day}" max="${t}" min="2026-01-01" data-pick></label>`;
    $("[data-pick]", el).addEventListener("change", e => { if (e.target.value) location.search = `?tag=${e.target.value}`; });
  }

  /* ================= Codeknacker ================= */
  function codeknacker(root) {
    const day = dayFromUrl(); dayNav(root, day);
    const r = rng(hash("code" + day));
    const code = shuffle([1, 2, 3, 4, 5, 6], r).slice(0, 4);
    const KEY = `rl-code-${day}`, MAX = 10;
    let st = store.get(KEY, { guesses: [], done: false });
    let cur = [];
    const board = $("[data-board]", root), pad = $("[data-pad]", root), msg = $("[data-msg]", root);
    const score = g => { let b = 0, w = 0; g.forEach((d, i) => { if (code[i] === d) b++; else if (code.includes(d)) w++; }); return [b, w]; };
    function render() {
      let h = "";
      for (let i = 0; i < MAX; i++) {
        const g = st.guesses[i], live = i === st.guesses.length && !st.done;
        const digits = g || (live ? cur : []);
        h += `<div class="crow${live ? " live" : ""}" aria-label="Versuch ${i + 1}"><span class="cn">${i + 1}</span>`;
        for (let k = 0; k < 4; k++) h += `<span class="cell">${digits[k] ?? ""}</span>`;
        if (g) { const [b, w] = score(g); h += `<span class="pegs" aria-label="${b} richtig platziert, ${w} richtige Ziffern an falscher Stelle">${"<i class=b></i>".repeat(b)}${"<i class=w></i>".repeat(w)}${"<i></i>".repeat(4 - b - w)}</span>`; }
        else h += `<span class="pegs"></span>`;
        h += `</div>`;
      }
      board.innerHTML = h;
      $$("button[data-d]", pad).forEach(btn => btn.disabled = st.done || cur.includes(+btn.dataset.d));
      $("[data-ok]", pad).disabled = st.done || cur.length !== 4;
      if (st.done) {
        const won = st.guesses.at(-1).join("") === code.join("");
        const s = store.get("rl-streak-code", { n: 0, best: 0 });
        msg.innerHTML = won ? `<strong>Geknackt in ${st.guesses.length} ${st.guesses.length === 1 ? "Versuch" : "Versuchen"}.</strong> Serie: ${s.n} Tag${s.n === 1 ? "" : "e"} (Rekord ${s.best}).`
          : `<strong>Diesmal nicht.</strong> Der Code war ${code.join(" ")}. Morgen gibt es einen neuen.`;
        msg.innerHTML += ` <button class="btn small" type="button" data-share>Ergebnis teilen</button>`;
        $("[data-share]", msg).onclick = e => share(`Rätsellotse Codeknacker ${fmtDate(day)} ${won ? st.guesses.length : "X"}/10\n` + st.guesses.map(g => { const [b, w] = score(g); return "🟠".repeat(b) + "⚪".repeat(w) + "▫️".repeat(4 - b - w); }).join("\n") + "\nraetsellotse.de/codeknacker.html", e.target);
      } else msg.textContent = `Noch ${MAX - st.guesses.length} Versuche. Vier verschiedene Ziffern von 1 bis 6.`;
    }
    function press(d) { if (st.done || cur.length >= 4 || cur.includes(d)) return; cur.push(d); render(); }
    function back() { cur.pop(); render(); }
    function submit() {
      if (cur.length !== 4 || st.done) return;
      st.guesses.push(cur); cur = [];
      const won = st.guesses.at(-1).join("") === code.join("");
      if (won || st.guesses.length >= MAX) { st.done = true; if (day === todayVienna()) streak("code", day, won); }
      store.set(KEY, st); render();
    }
    pad.addEventListener("click", e => { const b = e.target.closest("button"); if (!b) return; if (b.dataset.d) press(+b.dataset.d); if (b.hasAttribute("data-back")) back(); if (b.hasAttribute("data-ok")) submit(); });
    document.addEventListener("keydown", e => { if (e.target.closest("input,textarea")) return; if (/^[1-6]$/.test(e.key)) press(+e.key); if (e.key === "Backspace") back(); if (e.key === "Enter") submit(); });
    render();
  }

  /* ================= Sudoku ================= */
  const peers = (() => { const p = []; for (let i = 0; i < 81; i++) { const r = Math.floor(i / 9), c = i % 9, s = new Set(); for (let k = 0; k < 9; k++) { s.add(r * 9 + k); s.add(k * 9 + c); } const br = r - r % 3, bc = c - c % 3; for (let a = 0; a < 3; a++) for (let b = 0; b < 3; b++) s.add((br + a) * 9 + bc + b); s.delete(i); p.push([...s]); } return p; })();
  const units = (() => { const u = []; for (let k = 0; k < 9; k++) { u.push([...Array(9)].map((_, j) => k * 9 + j)); u.push([...Array(9)].map((_, j) => j * 9 + k)); const br = Math.floor(k / 3) * 3, bc = (k % 3) * 3; u.push([...Array(9)].map((_, j) => (br + Math.floor(j / 3)) * 9 + bc + j % 3)); } return u; })();
  const cands = (g, i) => { if (g[i]) return []; const used = new Set(peers[i].map(p => g[p])); return [1, 2, 3, 4, 5, 6, 7, 8, 9].filter(d => !used.has(d)); };
  function countSolutions(g, limit = 2) {
    let n = 0; const a = g.slice();
    (function go() {
      if (n >= limit) return;
      let best = -1, bc = null;
      for (let i = 0; i < 81; i++) if (!a[i]) { const c = cands(a, i); if (!c.length) return; if (!bc || c.length < bc.length) { best = i; bc = c; if (c.length === 1) break; } }
      if (best < 0) { n++; return; }
      for (const d of bc) { a[best] = d; go(); if (n >= limit) break; } a[best] = 0;
    })();
    return n;
  }
  function singlesSolvable(g) {
    const a = g.slice(); let prog = true;
    while (prog) {
      prog = false;
      for (let i = 0; i < 81; i++) if (!a[i]) { const c = cands(a, i); if (c.length === 1) { a[i] = c[0]; prog = true; } }
      for (const u of units) for (let d = 1; d <= 9; d++) { if (u.some(i => a[i] === d)) continue; const pos = u.filter(i => !a[i] && cands(a, i).includes(d)); if (pos.length === 1) { a[pos[0]] = d; prog = true; } }
    }
    return a.every(Boolean);
  }
  function makeSudoku(seed, level) {
    const r = rng(seed), g = Array(81).fill(0);
    (function fill(i) { if (i === 81) return true; if (g[i]) return fill(i + 1); for (const d of shuffle(cands(g, i), r)) { g[i] = d; if (fill(i + 1)) return true; } g[i] = 0; return false; })(0);
    const sol = g.slice(), target = { leicht: 38, mittel: 30, schwer: 25 }[level];
    let givens = 81;
    for (const i of shuffle([...Array(81).keys()], r)) {
      if (givens <= target) break;
      const v = g[i]; g[i] = 0;
      if (countSolutions(g) !== 1 || ((level === "leicht" || level === "mittel") && !singlesSolvable(g))) g[i] = v; else givens--;
    }
    return { puzzle: g, sol };
  }
  function sudoku(root) {
    const day = dayFromUrl(); dayNav(root, day);
    const levelSel = $("[data-level]", root);
    let level = new URLSearchParams(location.search).get("stufe") || store.get("rl-sudoku-level", "mittel");
    if (!["leicht", "mittel", "schwer"].includes(level)) level = "mittel";
    levelSel.value = level;
    const gridEl = $("[data-grid]", root), msg = $("[data-msg]", root), pad = $("[data-pad]", root);
    let P, KEY, st, sel = -1, notes = false;
    function load() {
      msg.textContent = "Sudoku wird erstellt …";
      setTimeout(() => {
        P = makeSudoku(hash(`sudoku${day}${level}`), level);
        KEY = `rl-sudoku-${day}-${level}`;
        st = store.get(KEY, { v: P.puzzle.slice(), n: Array(81).fill(0).map(() => []), done: false, t: 0, hints: 0 });
        sel = P.puzzle.indexOf(0); render();
      }, 10);
    }
    function conflicts(i) { const v = st.v[i]; return v && peers[i].some(p => st.v[p] === v); }
    function render() {
      let h = "";
      for (let i = 0; i < 81; i++) {
        const given = P.puzzle[i] !== 0, v = st.v[i], r = Math.floor(i / 9), c = i % 9;
        const rel = sel >= 0 && (peers[sel].includes(i));
        const same = sel >= 0 && v && st.v[sel] === v;
        const cls = ["sc", given ? "given" : "", i === sel ? "sel" : "", rel ? "rel" : "", same ? "same" : "", !given && conflicts(i) ? "bad" : "", c % 3 === 2 && c < 8 ? "br" : "", r % 3 === 2 && r < 8 ? "bb" : ""].join(" ");
        const inner = v ? v : `<span class="notes">${[1, 2, 3, 4, 5, 6, 7, 8, 9].map(d => `<i>${st.n[i].includes(d) ? d : ""}</i>`).join("")}</span>`;
        h += `<button type="button" class="${cls}" data-i="${i}" aria-label="Zeile ${r + 1}, Spalte ${c + 1}${v ? ", " + v : ", leer"}${given ? ", vorgegeben" : ""}">${inner}</button>`;
      }
      gridEl.innerHTML = h;
      $("[data-notes]", pad).setAttribute("aria-pressed", notes);
      if (st.done) msg.innerHTML = `<strong>Gelöst!</strong> ${st.hints ? `Mit ${st.hints} Tipp${st.hints > 1 ? "s" : ""}. ` : "Ohne Tipps. "}<button class="btn small" type="button" data-share>Ergebnis teilen</button>`;
      const sb = $("[data-share]", msg); if (sb) sb.onclick = e => share(`Rätsellotse Sudoku ${fmtDate(day)} (${level}) gelöst${st.hints ? ` mit ${st.hints} Tipp(s)` : " ohne Tipps"} ✅\nraetsellotse.de/sudoku.html`, e.target);
    }
    function put(d) {
      if (sel < 0 || P.puzzle[sel] || st.done) return;
      if (notes && d) { const n = st.n[sel]; const k = n.indexOf(d); k >= 0 ? n.splice(k, 1) : n.push(d); }
      else { st.v[sel] = d; st.n[sel] = []; if (d) peers[sel].forEach(p => { const k = st.n[p].indexOf(d); if (k >= 0) st.n[p].splice(k, 1); }); }
      if (st.v.every((v, i) => v === P.sol[i])) { st.done = true; if (day === todayVienna()) streak("sudoku-" + level, day, true); }
      store.set(KEY, st); msg.textContent = ""; render();
    }
    function hint() {
      if (st.done) return;
      // falsche Einträge zuerst melden
      const wrong = st.v.findIndex((v, i) => v && v !== P.sol[i]);
      if (wrong >= 0) { sel = wrong; render(); msg.textContent = `Das markierte Feld (Zeile ${Math.floor(wrong / 9) + 1}, Spalte ${wrong % 9 + 1}) stimmt nicht.`; return; }
      for (let i = 0; i < 81; i++) if (!st.v[i]) { const c = cands(st.v, i); if (c.length === 1) { sel = i; st.hints++; put(c[0]); msg.textContent = `Tipp: In Zeile ${Math.floor(i / 9) + 1}, Spalte ${i % 9 + 1} passt nur noch die ${c[0]} – alle anderen Ziffern stehen schon in derselben Zeile, Spalte oder im Block.`; return; } }
      const names = ["dieser Zeile", "dieser Spalte", "diesem Block"];
      for (let u = 0; u < units.length; u++) for (let d = 1; d <= 9; d++) {
        const U = units[u]; if (U.some(i => st.v[i] === d)) continue;
        const pos = U.filter(i => !st.v[i] && cands(st.v, i).includes(d));
        if (pos.length === 1) { const i = pos[0]; sel = i; st.hints++; put(d); msg.textContent = `Tipp: Die ${d} kann in ${names[u % 3]} nur an einer Stelle stehen: Zeile ${Math.floor(i / 9) + 1}, Spalte ${i % 9 + 1}.`; return; }
      }
      const i = st.v.findIndex(v => !v); sel = i; st.hints++; put(P.sol[i]); msg.textContent = `Hier hilft keine einfache Regel mehr – das Feld Zeile ${Math.floor(i / 9) + 1}, Spalte ${i % 9 + 1} wurde aufgedeckt.`;
    }
    gridEl.addEventListener("click", e => { const b = e.target.closest("[data-i]"); if (!b) return; sel = +b.dataset.i; render(); });
    pad.addEventListener("click", e => { const b = e.target.closest("button"); if (!b) return; if (b.dataset.d) put(+b.dataset.d); if (b.hasAttribute("data-erase")) put(0); if (b.hasAttribute("data-notes")) { notes = !notes; render(); } if (b.hasAttribute("data-hint")) hint(); });
    document.addEventListener("keydown", e => {
      if (e.target.closest("input,select,textarea") || !P) return;
      if (/^[1-9]$/.test(e.key)) { put(+e.key); e.preventDefault(); }
      else if (e.key === "Backspace" || e.key === "Delete" || e.key === "0") put(0);
      else if (e.key.toLowerCase() === "n") { notes = !notes; render(); }
      else if (e.key.startsWith("Arrow") && sel >= 0) { const d = { ArrowUp: -9, ArrowDown: 9, ArrowLeft: -1, ArrowRight: 1 }[e.key]; sel = (sel + d + 81) % 81; render(); e.preventDefault(); }
    });
    levelSel.addEventListener("change", () => { level = levelSel.value; store.set("rl-sudoku-level", level); load(); });
    load();
  }

  /* ================= Zielzahl ================= */
  function zielzahl(root) {
    const day = dayFromUrl(); dayNav(root, day);
    const r = rng(hash("ziel" + day));
    const big = shuffle([25, 50, 75, 100], r).slice(0, 2);
    const small = shuffle([1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10], r).slice(0, 4);
    const nums = [...big, ...small].sort((a, b) => b - a);
    // Zielzahl durch zufällige gültige Rechnung erzeugen (garantiert lösbar)
    let target = 0;
    for (let tries = 0; tries < 500 && !(target >= 101 && target <= 999); tries++) {
      let pool = shuffle(nums.slice(), r), k = 3 + Math.floor(r() * 3);
      while (pool.length > 1 && k-- > 0) {
        const a = pool.pop(), b = pool.pop(), op = Math.floor(r() * 4); let v;
        if (op === 0) v = a + b; else if (op === 1) v = a * b; else if (op === 2) v = Math.abs(a - b) || a + b; else v = (b && a % b === 0) ? a / b : a + b;
        pool.unshift(v);
      }
      target = pool[0];
    }
    const KEY = `rl-ziel-${day}`; let st = store.get(KEY, { best: null, expr: "", done: false, shown: false });
    $("[data-target]", root).textContent = target;
    $("[data-nums]", root).innerHTML = nums.map(n => `<span class="tile">${n}</span>`).join("");
    const input = $("[data-expr]", root), msg = $("[data-msg]", root);
    input.value = st.expr;
    function evaluate(src) {
      const toks = src.replace(/×/g, "*").replace(/÷|:/g, "/").replace(/−/g, "-").match(/\d+|[-+*/()]/g);
      if (!toks || toks.join("") !== src.replace(/\s/g, "").replace(/×/g, "*").replace(/÷|:/g, "/").replace(/−/g, "-")) throw "Nur Zahlen, + − × ÷ und Klammern verwenden.";
      let p = 0; const used = [];
      const peek = () => toks[p], eat = () => toks[p++];
      function prim() { const t = eat(); if (t === "(") { const v = expr(); if (eat() !== ")") throw "Eine Klammer ist nicht geschlossen."; return v; } if (/^\d+$/.test(t)) { used.push(+t); return +t; } throw "Die Rechnung ist unvollständig."; }
      function term() { let v = prim(); while (peek() === "*" || peek() === "/") { const o = eat(), b = prim(); if (o === "*") v *= b; else { if (b === 0 || v % b) throw "Teilen nur, wenn es ohne Rest aufgeht."; v /= b; } } return v; }
      function expr() { let v = term(); while (peek() === "+" || peek() === "-") { const o = eat(), b = term(); v = o === "+" ? v + b : v - b; if (v < 0) throw "Zwischenergebnisse dürfen nicht negativ sein."; } return v; }
      const v = expr(); if (p !== toks.length) throw "Die Rechnung ist nicht vollständig lesbar.";
      const pool = nums.slice(); for (const u of used) { const k = pool.indexOf(u); if (k < 0) throw `Die Zahl ${u} steht nicht (oft genug) zur Verfügung.`; pool.splice(k, 1); }
      return v;
    }
    function check() {
      st.expr = input.value.trim(); if (!st.expr) { msg.textContent = ""; return; }
      try {
        const v = evaluate(st.expr), diff = Math.abs(v - target);
        if (st.best === null || diff < Math.abs(st.best - target)) st.best = v;
        if (diff === 0 && !st.done) { st.done = true; if (day === todayVienna() && !st.shown) streak("ziel", day, true); }
        msg.innerHTML = diff === 0 ? `<strong>Genau ${target}!</strong> ${st.shown ? "" : "Volle Punktzahl."} <button class="btn small" type="button" data-share>Ergebnis teilen</button>` : `Ergebnis: <strong>${v}</strong> – noch ${diff} entfernt. Bestes Ergebnis bisher: ${st.best}.`;
        const sb = $("[data-share]", msg); if (sb) sb.onclick = e => share(`Rätsellotse Zielzahl ${fmtDate(day)}: ${target} getroffen 🎯\nraetsellotse.de/zielzahl.html`, e.target);
      } catch (err) { msg.textContent = typeof err === "string" ? err : "Diese Rechnung kann ich nicht lesen."; }
      store.set(KEY, st);
    }
    function solve() {
      let best = null;
      (function go(items) {
        for (const it of items) { const d = Math.abs(it.v - target); if (!best || d < Math.abs(best.v - target)) best = it; }
        if (best && best.v === target) return true;
        for (let i = 0; i < items.length; i++) for (let j = 0; j < items.length; j++) {
          if (i === j) continue; const a = items[i], b = items[j], rest = items.filter((_, k) => k !== i && k !== j);
          const opts = [];
          if (i < j) { opts.push({ v: a.v + b.v, s: `(${a.s} + ${b.s})` }); if (a.v > 1 && b.v > 1) opts.push({ v: a.v * b.v, s: `${a.s} × ${b.s}` }); }
          if (a.v > b.v) opts.push({ v: a.v - b.v, s: `(${a.s} − ${b.s})` });
          if (b.v > 1 && a.v % b.v === 0) opts.push({ v: a.v / b.v, s: `${a.s} ÷ ${b.s}` });
          for (const o of opts) if (go([...rest, o])) return true;
        }
        return false;
      })(nums.map(n => ({ v: n, s: String(n) })));
      return best;
    }
    $("[data-check]", root).addEventListener("click", check);
    input.addEventListener("keydown", e => { if (e.key === "Enter") check(); });
    $("[data-nums]", root).addEventListener("click", e => { const t = e.target.closest(".tile"); if (t) { input.value += t.textContent; input.focus(); } });
    $("[data-solve]", root).addEventListener("click", e => {
      e.target.disabled = true; e.target.textContent = "Rechne …";
      setTimeout(() => { const b = solve(); st.shown = true; store.set(KEY, st); $("[data-solution]", root).innerHTML = `Ein möglicher Weg: <strong>${b.s.replace(/^\((.*)\)$/, "$1")} = ${b.v}</strong>`; e.target.textContent = "Lösung gezeigt"; }, 20);
    });
    if (st.expr) check();
  }

  const games = { codeknacker, sudoku, zielzahl };
  const init = () => $$("[data-game]").forEach(el => games[el.dataset.game]?.(el));
  document.readyState === "loading" ? document.addEventListener("DOMContentLoaded", init) : init();
})();
