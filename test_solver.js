// Automatischer Test für assets/solver.js (node --test test_solver.js):
// Jeder erklärte Schritt muss mit der (per Backtracking ermittelten) einzigen Lösung vereinbar sein,
// jede Technik wird an einem eigenen Beispiel ausgelöst, Fehlerfälle (Widerspruch, keine/mehrere Lösungen) werden erkannt.
const test = require("node:test");
const assert = require("node:assert/strict");
const S = require("./assets/solver.js");

// Generator der Website (wie in assets/games.js), damit die Prüfung an echten Rätsel-Stufen läuft
const hash = s => { let h1 = 0xdeadbeef, h2 = 0x41c6ce57; for (let i = 0; i < s.length; i++) { const c = s.charCodeAt(i); h1 = Math.imul(h1 ^ c, 2654435761); h2 = Math.imul(h2 ^ c, 1597334677); } h1 = Math.imul(h1 ^ (h1 >>> 16), 2246822507) ^ Math.imul(h2 ^ (h2 >>> 13), 3266489909); return h1 >>> 0; };
const rng = seed => () => { seed |= 0; seed = seed + 0x6D2B79F5 | 0; let t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
const shuffle = (a, r) => { for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(r() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
const cands = (g, i) => { if (g[i]) return []; const used = new Set(S.PEERS[i].map(p => g[p])); return [1, 2, 3, 4, 5, 6, 7, 8, 9].filter(d => !used.has(d)); };
function make(seed, target) {
  const r = rng(seed), g = Array(81).fill(0);
  (function fill(i) { if (i === 81) return true; for (const d of shuffle(cands(g, i), r)) { g[i] = d; if (fill(i + 1)) return true; } g[i] = 0; return false; })(0);
  let givens = 81;
  for (const i of shuffle([...Array(81).keys()], r)) { if (givens <= target) break; const v = g[i]; g[i] = 0; if (S.countSolutions(g).count !== 1) g[i] = v; else givens--; }
  return g;
}

function checkPath(g) {
  const { count, solution } = S.countSolutions(g, 2);
  assert.equal(count, 1);
  const st = S.createState(g); const seen = new Set();
  for (let k = 0; k < 500 && st.g.includes(0); k++) {
    let s = S.findStep(st);
    if (!s) s = S.revealStep(st, solution);
    assert.notEqual(s.tech, "contradiction", "logischer Schritt darf keinen Widerspruch erzeugen");
    for (const [i, d] of s.place) assert.equal(d, solution[i], `${s.tech}: falsche Ziffer in Feld ${i}`);
    for (const [i, d] of s.elim) assert.notEqual(d, solution[i], `${s.tech}: richtige Ziffer ${d} in Feld ${i} gestrichen`);
    assert.ok(s.place.length + s.elim.length > 0, "jeder Schritt bewirkt etwas");
    assert.ok(s.text && s.text.length > 40, "jeder Schritt ist erklärt");
    S.applyStep(st, s); seen.add(s.tech);
  }
  assert.deepEqual(st.g, solution);
  return seen;
}

test("parse und stringify", () => {
  const s = S.EXAMPLES.stufe1;
  assert.equal(S.stringify(S.parse(s)), s);
  assert.equal(S.parse(s.replace(/\./g, "0")).filter(Boolean).length, S.parse(s).filter(Boolean).length);
  assert.equal(S.parse("123"), null);
  assert.equal(S.parse("x".repeat(81)), null);
  assert.ok(S.parse(s.slice(0, 9) + "\n" + s.slice(9)), "Zeilenumbrüche werden ignoriert");
});

test("Fehlerfälle: Widerspruch, keine Lösung, mehrere Lösungen", () => {
  const g = Array(81).fill(0); g[0] = 5; g[1] = 5;
  assert.deepEqual(S.conflicts(g), [0, 1]);
  assert.equal(S.countSolutions(g).count, 0);
  assert.equal(S.countSolutions(Array(81).fill(0)).count, 2, "leeres Gitter: mehr als eine Lösung");
  // keine Lösung ohne direkten Widerspruch: Feld 0 hat keine Ziffer frei
  const h = Array(81).fill(0); [1, 2, 3, 4, 5, 6, 7, 8].forEach((d, k) => { h[k + 1] = d; }); h[9 * 4] = 9;
  assert.equal(S.conflicts(h).length, 0); assert.equal(S.countSolutions(h).count, 0);
  assert.equal(S.findStep(S.createState(h)).tech, "contradiction");
});

test("Beispiele: eindeutig und in der angegebenen Stufe", () => {
  const want = { stufe1: 1, stufe2: 2, stufe3: 3, stufe4: 4 };
  for (const [k, s] of Object.entries(S.EXAMPLES)) {
    const g = S.parse(s);
    assert.equal(S.countSolutions(g).count, 1, k);
    assert.equal(S.rate(g).level, want[k], k);
    checkPath(g);
  }
  assert.equal(S.rate(S.parse(S.EXAMPLES.stufe3)).counts["xy-wing"] > 0, true, "Beispiel schwer zeigt einen XY-Wing");
});

test("Jeder Schritt ist korrekt – 150 Rätsel mit 24 bis 32 Vorgaben, alle Techniken kommen vor", () => {
  const seen = new Set();
  for (let k = 0; k < 150; k++) for (const t of checkPath(make(hash("test-" + k), 24 + (k % 9)))) seen.add(t);
  for (const t of ["hidden-single", "naked-single", "pointing", "naked-pair", "hidden-pair", "x-wing", "xy-wing", "reveal"]) assert.ok(seen.has(t), "nicht ausgelöst: " + t);
});

test("Alle elf Techniken kommen an echten schweren Rätseln vor und sind dort korrekt", () => {
  const seen = new Set();
  for (let k = 0; k < 110; k++) for (const t of checkPath(make(hash("cov" + k), 25))) seen.add(t);
  for (const t of Object.keys(S.TECH)) assert.ok(seen.has(t), "nicht ausgelöst: " + t);
});

test("Lösungsweg mit Aufdecken endet immer gelöst", () => {
  const g = S.parse(S.EXAMPLES.stufe4); const sol = S.countSolutions(g).solution;
  const r = S.solvePath(g, { reveal: true, solution: sol });
  assert.equal(r.solved, true); assert.ok(r.steps.some(s => s.tech === "reveal"));
  const plain = S.solvePath(g); assert.equal(plain.stuck, true); assert.equal(plain.level, 4);
});
