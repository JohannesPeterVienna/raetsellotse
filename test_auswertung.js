// Prüft content/tagessudoku.json gegen den Generator (assets/games.js) und den Löser (assets/solver.js):
// node --test test_auswertung.js – Stichproben werden neu erzeugt und bewertet, die Beispiel-Stellungen Schritt für Schritt nachgerechnet.
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("fs"), path = require("path");
const S = require("./assets/solver.js");
const A = require("./tools/auswertung.js");
const DATA = JSON.parse(fs.readFileSync(path.join(__dirname, "content", "tagessudoku.json"), "utf8"));

test("Zeitraum lückenlos, ein Eintrag je Tag", () => {
  assert.equal(DATA.tage[0].tag, DATA.von); assert.equal(DATA.tage.at(-1).tag, DATA.bis);
  for (let k = 1; k < DATA.tage.length; k++) assert.equal((new Date(DATA.tage[k].tag) - new Date(DATA.tage[k - 1].tag)) / 864e5, 1);
});

test("Stichprobe: jeder 9. Tag neu erzeugt und bewertet ergibt dieselben Werte", () => {
  for (let k = 0; k < DATA.tage.length; k += 9) {
    const row = DATA.tage[k];
    for (const level of ["leicht", "mittel", "schwer"]) {
      const b = A.bewerte(row.tag, level), e = row[level];
      assert.deepEqual([b.stufe, b.technik, b.schritte, b.vorgaben], [e.stufe, e.technik, e.schritte, e.vorgaben], `${row.tag} ${level}`);
      assert.equal(S.countSolutions(b.P.puzzle).count, 1, `${row.tag} ${level}: genau eine Lösung`);
    }
    assert.equal(S.stringify(A.puzzle(row.tag, "schwer").puzzle), row.schwer.s);
  }
});

test("Einstieg je Technik: nach den genannten Schritten ist genau diese Technik der nächste Schritt (jeder 5. Tag)", () => {
  for (let k = 0; k < DATA.tage.length; k += 5) {
    const s = DATA.tage[k].schwer;
    for (const [tech, n] of Object.entries(s.erst)) {
      const st = S.createState(S.parse(s.s));
      for (let j = 0; j < n; j++) S.applyStep(st, S.findStep(st));
      assert.equal(S.findStep(st).tech, tech, `${DATA.tage[k].tag} ${tech}`);
    }
  }
});

test("Beispiel-Stellungen der Strategie-Seite: Stand, Technik und Wirkung stimmen mit der eindeutigen Lösung überein", () => {
  const techs = Object.keys(S.TECH).filter(t => t !== "reveal");
  assert.deepEqual(Object.keys(DATA.beispiele).sort(), techs.sort(), "für jede Technik gibt es eine echte Stellung");
  for (const [tech, b] of Object.entries(DATA.beispiele)) {
    const g = S.parse(b.s), sol = S.countSolutions(g).solution, st = S.createState(g);
    for (let j = 0; j < b.schritt; j++) S.applyStep(st, S.findStep(st));
    assert.deepEqual(st.g, b.g); assert.deepEqual(st.c, b.c);
    const s = S.findStep(st);
    assert.equal(s.tech, tech); assert.equal(s.text, b.text); assert.deepEqual(s.elim, b.elim); assert.deepEqual(s.place, b.place);
    for (const [i, d] of s.place) assert.equal(sol[i], d);
    for (const [i, d] of s.elim) assert.notEqual(sol[i], d);
  }
});
