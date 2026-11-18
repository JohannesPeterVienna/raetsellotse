// Bewertet alle Tagessudokus eines Zeitraums mit dem Löser der Website und schreibt content/tagessudoku.json.
// Aufruf: node tools/auswertung.js 2026-01-01 2026-11-18
// Die Rätsel entstehen wie im Browser aus dem Datum (assets/games.js), bewertet wird mit assets/solver.js:
// Stufe = anspruchsvollste Technik, ohne die der erklärte Lösungsweg nicht weiterkommt; 4 = der Löser bleibt stecken.
const fs = require("fs"), path = require("path");
const G = require("../assets/games.js"), S = require("../assets/solver.js");
const LEVELS = ["leicht", "mittel", "schwer"];
function puzzle(day, level) { return G.makeSudoku(G.hash(`sudoku${day}${level}`), level); }
function bewerte(day, level) {
  const P = puzzle(day, level), r = S.solvePath(P.puzzle);
  if (r.solved) for (let i = 0; i < 81; i++) if (r.state.g[i] !== P.sol[i]) throw new Error(`Lösungsweg weicht ab: ${day} ${level}`);
  const first = {}; let hardest = null;
  r.steps.forEach((s, k) => { if (!(s.tech in first)) first[s.tech] = k; if (!hardest || s.level > hardest.level) hardest = s; });
  return { P, r, stufe: r.stuck ? 4 : r.level, technik: r.stuck ? "stuck" : hardest.tech, schritte: r.steps.length, vorgaben: P.puzzle.filter(Boolean).length, first };
}
function tage(von, bis) { const out = []; for (let d = new Date(von + "T12:00:00Z"); d.toISOString().slice(0, 10) <= bis; d.setUTCDate(d.getUTCDate() + 1)) out.push(d.toISOString().slice(0, 10)); return out; }
function auswerten(von, bis) {
  const rows = [], beispiele = {};
  for (const day of tage(von, bis)) {
    const row = { tag: day };
    for (const level of LEVELS) {
      const b = bewerte(day, level);
      row[level] = { stufe: b.stufe, technik: b.technik, schritte: b.schritte, vorgaben: b.vorgaben };
      if (level !== "schwer") continue;
      row.schwer.erst = Object.fromEntries(Object.entries(b.first).filter(([t]) => S.TECH[t].level > 1));
      row.schwer.s = S.stringify(b.P.puzzle);
      // Beispiel je Technik: erstes vollständig erklärbares Rätsel des Zeitraums, in dem sie vorkommt (Stand vor dem Schritt)
      // (kommt eine Technik nur in Rätseln vor, die der Löser nicht zu Ende erklären kann, dient das erste davon als Beispiel)
      for (const [t, k] of Object.entries(b.first)) if (!beispiele[t] || (beispiele[t].offen && !b.r.stuck)) {
        const st = S.createState(b.P.puzzle); for (let j = 0; j < k; j++) S.applyStep(st, b.r.steps[j]);
        const s = b.r.steps[k];
        beispiele[t] = { tag: day, schritt: k, s: S.stringify(b.P.puzzle), g: st.g.slice(), c: st.c.slice(), offen: b.r.stuck,
          name: s.name, text: s.text, cells: s.cells, place: s.place, elim: s.elim };
      }
    }
    rows.push(row);
  }
  return { von, bis, tage: rows, beispiele };
}
module.exports = { puzzle, bewerte, auswerten };
if (require.main === module) {
  const [von = "2026-01-01", bis = "2026-11-18"] = process.argv.slice(2);
  const data = auswerten(von, bis);
  fs.writeFileSync(path.join(__dirname, "..", "content", "tagessudoku.json"), JSON.stringify(data) + "\n");
  const z = {}; for (const r of data.tage) for (const l of LEVELS) { const k = `${l} Stufe ${r[l].stufe} ${r[l].technik}`; z[k] = (z[k] || 0) + 1; }
  console.log(data.tage.length, "Tage"); for (const k of Object.keys(z).sort()) console.log(k, z[k]);
  console.log(Object.entries(data.beispiele).map(([t, b]) => `${t}: ${b.tag} Schritt ${b.schritt + 1}`).join("\n"));
}
