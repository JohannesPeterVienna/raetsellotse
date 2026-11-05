/* Rätsellotse – Sudoku-Löser mit Lösungsweg. Läuft vollständig im Browser; es wird nichts übertragen.
   Logik (Techniken, Prüfung) ist ohne DOM nutzbar und wird mit node --test test_solver.js geprüft. */
(function (global) {
  "use strict";
  /* ---------- Grundlagen ---------- */
  const ROWS = [], COLS = [], BOXES = [];
  for (let k = 0; k < 9; k++) {
    ROWS.push([...Array(9)].map((_, j) => k * 9 + j));
    COLS.push([...Array(9)].map((_, j) => j * 9 + k));
    const br = Math.floor(k / 3) * 3, bc = (k % 3) * 3;
    BOXES.push([...Array(9)].map((_, j) => (br + Math.floor(j / 3)) * 9 + bc + (j % 3)));
  }
  const UNITS = [...ROWS, ...COLS, ...BOXES];            // 0–8 Zeilen, 9–17 Spalten, 18–26 Blöcke
  const rowOf = i => Math.floor(i / 9), colOf = i => i % 9, boxOf = i => Math.floor(rowOf(i) / 3) * 3 + Math.floor(colOf(i) / 3);
  const PEERS = [...Array(81)].map((_, i) => { const s = new Set([...ROWS[rowOf(i)], ...COLS[colOf(i)], ...BOXES[boxOf(i)]]); s.delete(i); return [...s]; });
  const sees = (a, b) => a !== b && (rowOf(a) === rowOf(b) || colOf(a) === colOf(b) || boxOf(a) === boxOf(b));
  const ALL = 0x3FE, bit = d => 1 << d, has = (m, d) => (m >> d) & 1;
  const pc = m => { let n = 0; while (m) { m &= m - 1; n++; } return n; };
  const digs = m => { const r = []; for (let d = 1; d <= 9; d++) if (has(m, d)) r.push(d); return r; };
  const cellName = i => `Zeile ${rowOf(i) + 1}, Spalte ${colOf(i) + 1}`;
  const short = i => `Z${rowOf(i) + 1}/S${colOf(i) + 1}`;
  const unitName = u => u < 9 ? `Zeile ${u + 1}` : u < 18 ? `Spalte ${u - 8}` : `Block ${u - 17}`;
  const list = a => a.length < 2 ? a.join("") : a.slice(0, -1).join(", ") + " und " + a[a.length - 1];
  function combos(arr, n, start = 0, acc = [], out = []) {
    if (acc.length === n) { out.push(acc.slice()); return out; }
    for (let k = start; k < arr.length; k++) { acc.push(arr[k]); combos(arr, n, k + 1, acc, out); acc.pop(); }
    return out;
  }

  /* ---------- Einlesen und Prüfen ---------- */
  function parse(str) {
    const s = String(str || "").replace(/[\s|+\-]/g, "");
    if (s.length !== 81 || /[^0-9.]/.test(s)) return null;
    return [...s].map(ch => (ch === "." ? 0 : +ch));
  }
  const stringify = g => g.map(v => v || ".").join("");
  function conflicts(g) {
    const bad = new Set();
    for (let i = 0; i < 81; i++) if (g[i]) for (const p of PEERS[i]) if (g[p] === g[i]) { bad.add(i); bad.add(p); }
    return [...bad].sort((a, b) => a - b);
  }
  function countSolutions(g, limit = 2) {
    const a = g.slice(); let n = 0, first = null;
    if (conflicts(a).length) return { count: 0, solution: null };
    const cand = i => { let m = ALL; for (const p of PEERS[i]) m &= ~bit(a[p]); return m; };
    (function go() {
      if (n >= limit) return;
      let best = -1, bm = 0, bn = 10;
      for (let i = 0; i < 81; i++) if (!a[i]) { const m = cand(i), k = pc(m); if (!k) return; if (k < bn) { best = i; bm = m; bn = k; if (k === 1) break; } }
      if (best < 0) { n++; if (!first) first = a.slice(); return; }
      for (const d of digs(bm)) { a[best] = d; go(); if (n >= limit) break; }
      a[best] = 0;
    })();
    return { count: n, solution: first };
  }

  /* ---------- Zustand: Ziffern + Kandidaten (Bitmasken) ---------- */
  function createState(g) {
    const st = { g: g.slice(), c: Array(81).fill(0) };
    for (let i = 0; i < 81; i++) if (!st.g[i]) { let m = ALL; for (const p of PEERS[i]) m &= ~bit(st.g[p]); st.c[i] = m; }
    return st;
  }
  const cloneState = st => ({ g: st.g.slice(), c: st.c.slice() });
  function place(st, i, d) { st.g[i] = d; st.c[i] = 0; for (const p of PEERS[i]) st.c[p] &= ~bit(d); }
  function applyStep(st, step) {
    for (const [i, d] of step.place || []) place(st, i, d);
    for (const [i, d] of step.elim || []) st.c[i] &= ~bit(d);
  }

  /* ---------- Techniken (in der Reihenfolge, in der Menschen sie üblicherweise anwenden) ---------- */
  const TECH = {
    "hidden-single": { name: "Einziger Platz (Hidden Single)", level: 1 },
    "naked-single": { name: "Einzige Möglichkeit (Naked Single)", level: 1 },
    "pointing": { name: "Block-Zeile-Regel", level: 2 },
    "naked-pair": { name: "Paar (Naked Pair)", level: 2 },
    "hidden-pair": { name: "Verstecktes Paar (Hidden Pair)", level: 2 },
    "naked-triple": { name: "Tripel (Naked Triple)", level: 3 },
    "hidden-triple": { name: "Verstecktes Tripel (Hidden Triple)", level: 3 },
    "x-wing": { name: "X-Wing", level: 3 },
    "swordfish": { name: "Swordfish", level: 3 },
    "xy-wing": { name: "XY-Wing", level: 3 },
    "reveal": { name: "Aufgedeckt (ohne Begründung)", level: 4 }
  };
  const LEVELS = { 1: "Stufe 1 · Einstieg", 2: "Stufe 2 · Fortgeschritten", 3: "Stufe 3 · Schwer", 4: "Stufe 4 · Sehr schwer" };
  const mk = (tech, o) => Object.assign({ tech, name: TECH[tech].name, level: TECH[tech].level, place: [], elim: [], cells: [] }, o);

  function hiddenSingle(st) {
    for (const u of [18, 19, 20, 21, 22, 23, 24, 25, 26, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]) {
      const U = UNITS[u];
      for (let d = 1; d <= 9; d++) {
        if (U.some(i => st.g[i] === d)) continue;
        const pos = U.filter(i => has(st.c[i], d));
        if (pos.length === 1) {
          const i = pos[0];
          return mk("hidden-single", { place: [[i, d]], cells: U.filter(x => x !== i), unit: u,
            text: `Die ${d} kann in ${unitName(u)} nur noch an einer Stelle stehen: ${cellName(i)}. In allen anderen freien Feldern von ${unitName(u)} ist die ${d} durch Zeile, Spalte oder Block bereits ausgeschlossen.` });
        }
      }
    }
    return null;
  }
  function nakedSingle(st) {
    for (let i = 0; i < 81; i++) if (!st.g[i] && pc(st.c[i]) === 1) {
      const d = digs(st.c[i])[0];
      let basic = ALL; for (const p of PEERS[i]) basic &= ~bit(st.g[p]);
      const text = pc(basic) === 1
        ? `In ${cellName(i)} passt nur noch die ${d}: Alle anderen Ziffern stehen schon in derselben Zeile, Spalte oder im selben Block.`
        : `In ${cellName(i)} bleibt nach den bisherigen Streichungen nur noch der Kandidat ${d} übrig.`;
      return mk("naked-single", { place: [[i, d]], cells: PEERS[i].filter(p => st.g[p]), text });
    }
    return null;
  }
  function pointing(st) {
    for (let b = 0; b < 9; b++) {
      const B = BOXES[b];
      for (let d = 1; d <= 9; d++) {
        const pos = B.filter(i => has(st.c[i], d));
        if (pos.length < 2) continue;
        for (const [line, of, nm] of [[ROWS, rowOf, "Zeile"], [COLS, colOf, "Spalte"]]) {
          const k = of(pos[0]);
          if (!pos.every(i => of(i) === k)) continue;
          const elim = line[k].filter(i => boxOf(i) !== b && has(st.c[i], d)).map(i => [i, d]);
          if (elim.length) return mk("pointing", { elim, cells: pos,
            text: `In Block ${b + 1} kann die ${d} nur in ${nm} ${k + 1} stehen (${list(pos.map(short))}). Damit liegt die ${d} von ${nm} ${k + 1} sicher in diesem Block – in den übrigen Feldern von ${nm} ${k + 1} fällt sie weg: ${list(elim.map(e => short(e[0])))}.` });
        }
      }
    }
    for (let u = 0; u < 18; u++) {
      const U = UNITS[u];
      for (let d = 1; d <= 9; d++) {
        const pos = U.filter(i => has(st.c[i], d));
        if (pos.length < 2) continue;
        const b = boxOf(pos[0]);
        if (!pos.every(i => boxOf(i) === b)) continue;
        const elim = BOXES[b].filter(i => !U.includes(i) && has(st.c[i], d)).map(i => [i, d]);
        if (elim.length) return mk("pointing", { elim, cells: pos,
          text: `In ${unitName(u)} kann die ${d} nur innerhalb von Block ${b + 1} stehen (${list(pos.map(short))}). Also ist die ${d} dieses Blocks schon vergeben – in seinen übrigen Feldern fällt sie weg: ${list(elim.map(e => short(e[0])))}.` });
      }
    }
    return null;
  }
  function nakedSubset(st, n) {
    const tech = n === 2 ? "naked-pair" : "naked-triple";
    for (let u = 0; u < 27; u++) {
      const U = UNITS[u], free = U.filter(i => !st.g[i]);
      const small = free.filter(i => pc(st.c[i]) >= 2 && pc(st.c[i]) <= n);
      for (const set of combos(small, n)) {
        const m = set.reduce((a, i) => a | st.c[i], 0);
        if (pc(m) !== n) continue;
        const elim = [];
        for (const i of free) if (!set.includes(i)) for (const d of digs(st.c[i] & m)) elim.push([i, d]);
        if (elim.length) {
          const ds = digs(m);
          return mk(tech, { elim, cells: set, unit: u,
            text: `In ${unitName(u)} teilen sich ${list(set.map(short))} die Kandidaten ${list(ds.map(String))}. ${n === 2 ? "Diese zwei Ziffern müssen in diesen zwei Feldern" : "Diese drei Ziffern müssen in diesen drei Feldern"} stehen – nur die Reihenfolge ist offen. In den übrigen Feldern von ${unitName(u)} fallen sie weg: ${list(elim.map(e => `${e[1]} in ${short(e[0])}`))}.` });
        }
      }
    }
    return null;
  }
  function hiddenSubset(st, n) {
    const tech = n === 2 ? "hidden-pair" : "hidden-triple";
    for (let u = 0; u < 27; u++) {
      const U = UNITS[u];
      const open = [1, 2, 3, 4, 5, 6, 7, 8, 9].filter(d => !U.some(i => st.g[i] === d));
      const where = d => U.filter(i => has(st.c[i], d));
      const cand = open.filter(d => { const k = where(d).length; return k >= 1 && k <= n; });
      for (const ds of combos(cand, n)) {
        const cells = [...new Set(ds.flatMap(where))];
        if (cells.length !== n) continue;
        const keep = ds.reduce((a, d) => a | bit(d), 0), elim = [];
        for (const i of cells) for (const d of digs(st.c[i] & ~keep)) elim.push([i, d]);
        if (elim.length) return mk(tech, { elim, cells, unit: u,
          text: `In ${unitName(u)} kommen die Ziffern ${list(ds.map(String))} nur in ${list(cells.map(short))} vor. Diese Felder gehören also ${n === 2 ? "diesen beiden" : "diesen drei"} Ziffern – alle anderen Kandidaten dort fallen weg: ${list(elim.map(e => `${e[1]} in ${short(e[0])}`))}.` });
      }
    }
    return null;
  }
  function fish(st, n) {
    const tech = n === 2 ? "x-wing" : "swordfish";
    for (let d = 1; d <= 9; d++) for (const [base, cover, ofCover, bn, cn] of [[ROWS, COLS, colOf, "Zeile", "Spalte"], [COLS, ROWS, rowOf, "Spalte", "Zeile"]]) {
      const lines = [];
      for (let k = 0; k < 9; k++) { const pos = base[k].filter(i => has(st.c[i], d)); if (pos.length >= 2 && pos.length <= n) lines.push({ k, pos }); }
      for (const set of combos(lines, n)) {
        const cov = [...new Set(set.flatMap(l => l.pos.map(ofCover)))];
        if (cov.length !== n) continue;
        const ks = set.map(l => l.k), elim = [];
        for (const c of cov) for (const i of cover[c]) if (has(st.c[i], d) && !set.some(l => l.pos.includes(i))) elim.push([i, d]);
        if (elim.length) return mk(tech, { elim, cells: set.flatMap(l => l.pos), digit: d,
          text: `Die ${d} kann in ${bn} ${list(ks.map(k => String(k + 1)))} jeweils nur in ${cn} ${list(cov.sort((a, b) => a - b).map(c => String(c + 1)))} stehen. Wie auch immer sie sich verteilt: In diesen ${n === 2 ? "zwei" : "drei"} ${cn === "Spalte" ? "Spalten" : "Zeilen"} ist die ${d} damit schon untergebracht. Sie fällt deshalb in den übrigen Feldern dieser ${cn === "Spalte" ? "Spalten" : "Zeilen"} weg: ${list(elim.map(e => short(e[0])))}.` });
      }
    }
    return null;
  }
  function xyWing(st) {
    const bi = []; for (let i = 0; i < 81; i++) if (!st.g[i] && pc(st.c[i]) === 2) bi.push(i);
    for (const p of bi) {
      const [a, b] = digs(st.c[p]);
      const wings = bi.filter(w => sees(p, w) && pc(st.c[w] & st.c[p]) === 1);
      for (const x of wings) for (const y of wings) {
        if (x >= y) continue;
        const cx = st.c[x] & ~st.c[p], cy = st.c[y] & ~st.c[p];
        if (cx !== cy || pc(cx) !== 1) continue;
        if ((st.c[x] & st.c[p]) === (st.c[y] & st.c[p])) continue;   // einer muss a, der andere b teilen
        const z = digs(cx)[0], elim = [];
        for (let i = 0; i < 81; i++) if (i !== x && i !== y && i !== p && has(st.c[i], z) && sees(i, x) && sees(i, y)) elim.push([i, z]);
        if (elim.length) return mk("xy-wing", { elim, cells: [p, x, y],
          text: `${cellName(p)} hat nur die Kandidaten ${a} und ${b}. Es „sieht“ ${short(x)} (${list(digs(st.c[x]).map(String))}) und ${short(y)} (${list(digs(st.c[y]).map(String))}). Egal ob dort eine ${a} oder eine ${b} steht: Eines der beiden äußeren Felder muss die ${z} bekommen. Jedes Feld, das beide äußeren Felder sieht, kann deshalb keine ${z} sein: ${list(elim.map(e => short(e[0])))}.` });
      }
    }
    return null;
  }
  const FINDERS = [hiddenSingle, nakedSingle, pointing, st => nakedSubset(st, 2), st => hiddenSubset(st, 2), st => nakedSubset(st, 3), st => hiddenSubset(st, 3), st => fish(st, 2), st => fish(st, 3), xyWing];
  function findStep(st) {
    for (let i = 0; i < 81; i++) if (!st.g[i] && !st.c[i]) return { tech: "contradiction", cells: [i], text: `Widerspruch: In ${cellName(i)} ist keine Ziffer mehr möglich. Das Sudoku enthält einen Fehler.` };
    for (const f of FINDERS) { const s = f(st); if (s) return s; }
    return null;
  }
  function revealStep(st, solution) {
    let best = -1;
    for (let i = 0; i < 81; i++) if (!st.g[i] && (best < 0 || pc(st.c[i]) < pc(st.c[best]))) best = i;
    if (best < 0) return null;
    return mk("reveal", { place: [[best, solution[best]]], cells: [],
      text: `Mit den hier erklärten Techniken geht es nicht weiter. Aufgedeckt wurde ${cellName(best)}: ${solution[best]} (das Feld mit den wenigsten Kandidaten). Begründen ließe sich dieser Schritt nur mit Ketten-Techniken.` });
  }
  /* Kompletter Lösungsweg. Mit reveal=true werden Stellen ohne erklärbaren Schritt aufgedeckt. */
  function solvePath(g, opts = {}) {
    const st = createState(g), steps = []; let stuck = false;
    const sol = opts.solution || null;
    for (let guard = 0; guard < 2000 && st.g.includes(0); guard++) {
      let s = findStep(st);
      if (s && s.tech === "contradiction") { steps.push(s); stuck = true; break; }
      if (!s) { if (opts.reveal && sol) s = revealStep(st, sol); if (!s) { stuck = true; break; } }
      applyStep(st, s); steps.push(s);
    }
    const lv = steps.reduce((m, s) => Math.max(m, s.level || 0), 0);
    return { steps, state: st, stuck, solved: !st.g.includes(0), level: stuck ? 4 : lv };
  }
  function rate(g) {
    const r = solvePath(g), counts = {};
    for (const s of r.steps) counts[s.tech] = (counts[s.tech] || 0) + 1;
    const hardest = r.steps.reduce((h, s) => (!h || s.level > h.level ? s : h), null);
    return { level: r.stuck ? 4 : (r.level || 1), label: LEVELS[r.stuck ? 4 : (r.level || 1)], stuck: r.stuck, steps: r.steps.length, counts, hardest: hardest ? hardest.name : null, filled: r.state.g.filter(Boolean).length };
  }

  const EXAMPLES = {   // mit dem Generator der Website erzeugt; Stufe durch test_solver.js abgesichert
    stufe1: ".56..9.38.2...75......34276.381.6....47..2...2...43..9182..5.6.....2..8..7.498125",
    stufe2: "..7....5.2..3.....8....5.64..6.5.......68..27..4.....61...9..3.59.2......6....7.9",
    stufe3: "9.3..4.1........4.6...7.2.32......6...8..2..5..6..19...3.8.64.......9...7.9....5.",
    stufe4: "2.59....1....2......8...6...37...2...46.8...39.........7...45.......5.686.93...4."
  };
  const api = { EXAMPLES, ROWS, COLS, BOXES, UNITS, PEERS, TECH, LEVELS, parse, stringify, conflicts, countSolutions, createState, cloneState, applyStep, findStep, revealStep, solvePath, rate, digs, cellName };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  global.RLSolver = api;

  /* ---------- Oberfläche ---------- */
  if (typeof document === "undefined") return;
  function init(root) {
    const $ = s => root.querySelector(s);
    const gridEl = $("[data-lgrid]"), msg = $("[data-lmsg]"), stepsEl = $("[data-steps]"), text = $("[data-text]");
    const candBtn = $("[data-cands]");
    let st = null, origin = Array(81).fill(""), solution = null, showC = false, last = null, path = [];
    const cells = [];
    for (let i = 0; i < 81; i++) {
      const r = rowOf(i), c = colOf(i), d = document.createElement("div");
      d.className = "sc lc" + (c % 3 === 2 && c < 8 ? " br" : "") + (r % 3 === 2 && r < 8 ? " bb" : "");
      d.innerHTML = `<span class="notes" aria-hidden="true">${[1, 2, 3, 4, 5, 6, 7, 8, 9].map(() => "<i></i>").join("")}</span><input type="text" inputmode="numeric" maxlength="1" autocomplete="off" aria-label="Zeile ${r + 1}, Spalte ${c + 1}" data-i="${i}">`;
      gridEl.appendChild(d); cells.push(d);
    }
    const inputs = cells.map(d => d.querySelector("input"));
    const grid = () => inputs.map(x => (/^[1-9]$/.test(x.value) ? +x.value : 0));
    const say = (h, cls = "") => { msg.className = "msg " + cls; msg.innerHTML = h; };
    function setGrid(g, from = "given") { g.forEach((v, i) => { inputs[i].value = v || ""; origin[i] = v ? from : ""; }); }
    function reset(keepMsg) { st = null; solution = null; last = null; path = []; stepsEl.innerHTML = ""; if (!keepMsg) say(""); }
    function render() {
      const bad = new Set(conflicts(grid()));
      const elim = new Map(); if (last) for (const [i, d] of last.elim || []) elim.set(i * 10 + d, true);
      const cand = st ? st.c : createState(grid()).c;
      for (let i = 0; i < 81; i++) {
        const cl = cells[i].classList, v = inputs[i].value;
        cl.toggle("given", origin[i] === "given" && !!v); cl.toggle("solved", origin[i] === "step"); cl.toggle("shown", origin[i] === "reveal");
        cl.toggle("bad", bad.has(i)); cl.toggle("hl", !!(last && last.cells && last.cells.includes(i)));
        cl.toggle("tg", !!(last && ((last.place || []).some(p => p[0] === i) || (last.elim || []).some(e => e[0] === i))));
        const notes = cells[i].querySelectorAll(".notes i");
        for (let d = 1; d <= 9; d++) {
          const on = !v && showC && (has(cand[i], d) || elim.has(i * 10 + d));
          notes[d - 1].textContent = on ? d : ""; notes[d - 1].className = elim.has(i * 10 + d) ? "x" : "";
        }
      }
      candBtn.setAttribute("aria-pressed", showC);
    }
    function prepare() {
      if (st) return true;
      const g = grid(), n = g.filter(Boolean).length, bad = conflicts(g);
      inputs.forEach((x, i) => { origin[i] = x.value ? "given" : ""; });
      if (!n) { say("Trag zuerst die Vorgaben deines Sudokus ein – oder lade ein Beispiel."); return false; }
      if (bad.length) { render(); say(`Die markierten Felder widersprechen sich: Eine Ziffer steht doppelt in einer Zeile, Spalte oder einem Block (${list(bad.slice(0, 6).map(short))}${bad.length > 6 ? " …" : ""}). Bitte die Vorgaben prüfen.`, "warn"); return false; }
      const r = countSolutions(g, 2);
      if (r.count === 0) { say("Dieses Sudoku hat keine Lösung. Meist steckt ein Tippfehler in den Vorgaben – vergleiche sie noch einmal mit deiner Vorlage.", "warn"); return false; }
      if (r.count > 1) { say(`Dieses Sudoku hat mehr als eine Lösung${n < 17 ? " – mit weniger als 17 Vorgaben ist das immer so" : ""}. Ein Lösungsweg mit reiner Logik ist dann nicht möglich. Fehlt vielleicht eine Vorgabe?`, "warn"); return false; }
      solution = r.solution; st = createState(g); return true;
    }
    function next(silent) {
      if (!prepare()) return null;
      if (!st.g.includes(0)) { say("<strong>Gelöst.</strong> Alle Felder sind ausgefüllt."); return null; }
      const s = findStep(st);
      if (!s) {
        last = null; render();
        say(`Mit den hier erklärten Techniken geht es an dieser Stelle nicht weiter. Das Sudoku hat trotzdem genau eine Lösung – der nächste Schritt verlangt Ketten-Techniken (Stufe 4). <button type="button" class="btn small" data-reveal>Ein Feld aufdecken</button> <button type="button" class="btn small ghost" data-solution>Lösung zeigen</button>`, "warn");
        return null;
      }
      return apply(s, silent);
    }
    function apply(s, silent) {
      applyStep(st, s); path.push(s);
      for (const [i, d] of s.place || []) { inputs[i].value = d; origin[i] = s.tech === "reveal" ? "reveal" : "step"; }
      last = s; if ((s.elim || []).length) showC = true; render();
      const li = document.createElement("li");
      li.innerHTML = `<strong>${s.name}</strong> ${s.text}`; stepsEl.appendChild(li);
      if (!silent) say(`<strong>Schritt ${path.length}: ${s.name}.</strong> ${s.text}${st.g.includes(0) ? "" : " <strong>Damit ist das Sudoku gelöst.</strong>"}`);
      return s;
    }
    function all() {
      if (!prepare()) return;
      let n = 0; while (st.g.includes(0) && next(true)) n++;
      const lv = path.reduce((m, s) => Math.max(m, s.level), 0);
      if (!st.g.includes(0)) say(`<strong>Gelöst in ${path.length} Schritten.</strong> Schwierigste Technik: ${path.reduce((h, s) => (s.level > h.level ? s : h), path[0]).name} – ${LEVELS[lv]}. Der ganze Lösungsweg steht unten.`);
      stepsEl.scrollIntoView && n > 0 && window.matchMedia && !window.matchMedia("(prefers-reduced-motion: reduce)").matches && stepsEl.scrollIntoView({ behavior: "smooth", block: "nearest" });
    }
    function check() {
      const g = grid(), n = g.filter(Boolean).length;
      if (!n) return say("Trag zuerst die Vorgaben ein.");
      const bad = conflicts(g); if (bad.length) { render(); return say(`Widerspruch in den markierten Feldern (${list(bad.slice(0, 6).map(short))}).`, "warn"); }
      const r = countSolutions(g, 2);
      if (r.count === 0) return say("Keine Lösung möglich – vermutlich ein Tippfehler.", "warn");
      if (r.count > 1) return say(`Mehr als eine Lösung (${n} Vorgaben). Ein echtes Sudoku hat genau eine.`, "warn");
      const rt = rate(g);
      say(`<strong>Eindeutig lösbar</strong> (${n} Vorgaben). Schwierigkeit nach Lösungsweg: <strong>${rt.label}</strong>${rt.stuck ? " – verlangt Techniken jenseits von XY-Wing" : ` – schwierigste nötige Technik: ${rt.hardest}`}. Verraten wird dabei nichts.`);
    }
    function load(g) { reset(); setGrid(g); showC = false; render(); }
    function fromText(s) { const g = parse(s); if (!g) { say("Bitte genau 81 Zeichen einfügen: Ziffern 1–9, leere Felder als 0 oder Punkt.", "warn"); return; } load(g); history.replaceState(null, "", "?s=" + stringify(g)); say("Sudoku übernommen. Jetzt „Nächster Schritt“ oder „Prüfen“."); }

    gridEl.addEventListener("input", e => {
      const x = e.target, i = +x.dataset.i;
      const v = (x.value.match(/[1-9]/g) || []).pop() || ""; x.value = v;
      if (st) { inputs.forEach((y, k) => { if (origin[k] === "step" || origin[k] === "reveal") { y.value = ""; origin[k] = ""; } }); reset(true); say("Vorgaben geändert – der Lösungsweg beginnt neu."); }
      origin[i] = v ? "given" : ""; render();
      if (v && i < 80) inputs[i + 1].focus();
    });
    gridEl.addEventListener("keydown", e => {
      const i = +e.target.dataset.i; if (Number.isNaN(i)) return;
      const mv = { ArrowUp: -9, ArrowDown: 9, ArrowLeft: -1, ArrowRight: 1 }[e.key];
      if (mv) { inputs[(i + mv + 81) % 81].focus(); e.preventDefault(); }
      else if (e.key === "Backspace" && !inputs[i].value && i > 0) { inputs[i - 1].focus(); }
    });
    root.addEventListener("click", e => {
      const b = e.target.closest("button"); if (!b) return;
      if (b.hasAttribute("data-next")) next();
      else if (b.hasAttribute("data-all")) all();
      else if (b.hasAttribute("data-check")) check();
      else if (b.hasAttribute("data-cands")) { showC = !showC; render(); }
      else if (b.hasAttribute("data-clear")) { load(Array(81).fill(0)); history.replaceState(null, "", location.pathname); inputs[0].focus(); }
      else if (b.hasAttribute("data-reveal")) { if (st && solution) { const s = revealStep(st, solution); if (s) apply(s); } }
      else if (b.hasAttribute("data-solution")) { if (!prepare()) return; for (let i = 0; i < 81; i++) if (!st.g[i]) { inputs[i].value = solution[i]; origin[i] = "reveal"; } st = createState(solution); last = null; render(); say("Die vollständige Lösung ist eingetragen (orange: aufgedeckt, ohne Lösungsweg)."); }
      else if (b.hasAttribute("data-load")) fromText(text.value);
      else if (b.hasAttribute("data-link")) {
        const g = grid(); const url = location.origin + location.pathname + "?s=" + stringify(g); text.value = stringify(g);
        const ok = () => say("Link kopiert. Wer ihn öffnet, sieht genau diese Vorgaben.");
        if (navigator.clipboard) navigator.clipboard.writeText(url).then(ok, () => say("Link: " + url)); else say("Link: " + url);
      }
    });
    root.querySelector("[data-beispiel]").addEventListener("change", e => { const v = e.target.value; if (EXAMPLES[v]) { const nm = e.target.selectedOptions[0].textContent; load(parse(EXAMPLES[v])); say(`Beispiel „${nm}“ geladen. Tippe auf „Nächster Schritt“.`); } e.target.value = ""; });
    const q = new URLSearchParams(location.search).get("s");
    if (q && parse(q)) { load(parse(q)); say("Sudoku aus dem Link geladen."); } else render();
  }
  const go = () => document.querySelectorAll("[data-game=loeser]").forEach(init);
  document.readyState === "loading" ? document.addEventListener("DOMContentLoaded", go) : go();
})(typeof window !== "undefined" ? window : globalThis);
