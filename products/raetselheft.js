// Rätselheft (Premium-PDF): Sudokus in drei Stufen + Nonogramme, mit Lösungen. Generatoren = Website.
const fs = require("fs"), path = require("path");
const src = fs.readFileSync(path.join(__dirname, "../assets/games.js"), "utf8");
const body = src.slice(src.indexOf("(() => {") + 8, src.lastIndexOf("const init = () =>"));
global.document = { querySelector: () => null, querySelectorAll: () => [] };
global.localStorage = { getItem: () => null, setItem() {} };
const G = new Function(body + "; return { makeSudoku, makeNono, hash };")();
const { jsPDF } = require("/tmp/npmx/node_modules/jspdf/dist/jspdf.node.min.js");
const NR = 1, W = 210, H = 297, M = 15, INK = [16, 43, 42], BUOY = [232, 98, 42], SEA = [33, 120, 108], MUTED = [110, 128, 126];
const doc = new jsPDF({ unit: "mm", format: "a4", compress: true });
doc.setProperties({ title: `Rätsellotse Rätselheft Nr. ${NR}`, author: "Rätsellotse", creator: "raetsellotse.de" });
let page = 1;
const col = c => doc.setTextColor(...c), draw = c => doc.setDrawColor(...c), fill = c => doc.setFillColor(...c);
function footer() { doc.setFont("helvetica", "normal"); doc.setFontSize(7); col(MUTED); doc.text(`Rätsellotse · Rätselheft Nr. ${NR}`, M, H - 8); doc.text(String(page), W - M, H - 8, { align: "right" }); }
function newPage() { doc.addPage(); page++; }
function heading(t, sub) { doc.setFont("helvetica", "bold"); doc.setFontSize(18); col(INK); doc.text(t, M, M + 8); if (sub) { doc.setFontSize(9); col(BUOY); doc.text(sub, W - M, M + 8, { align: "right" }); } draw(BUOY); doc.setLineWidth(0.6); doc.line(M, M + 11, W - M, M + 11); }
function sudoku(g, x, y, s, small = false) {
  const c = s / 9; draw(INK);
  for (let i = 0; i <= 9; i++) { doc.setLineWidth(i % 3 ? 0.15 : 0.6); doc.line(x + i * c, y, x + i * c, y + s); doc.line(x, y + i * c, x + s, y + i * c); }
  doc.setFont("helvetica", small ? "normal" : "bold"); doc.setFontSize(small ? c * 1.9 : c * 2.1); col(INK);
  g.forEach((v, i) => { if (v) doc.text(String(v), x + (i % 9) * c + c / 2, y + Math.floor(i / 9) * c + c * 0.7, { align: "center" }); });
}
function nono(P, x, y, maxW, maxH, solution = false) {
  const n = P.n, rcW = Math.max(...P.rc.map(r => r.length)), ccH = Math.max(...P.cc.map(c => c.length));
  const c = Math.min(maxW / (n + rcW * 0.62), maxH / (n + ccH * 0.62)), gx = x + rcW * c * 0.62, gy = y + ccH * c * 0.62, fs = Math.min(9, c * 1.8);
  doc.setFont("helvetica", "bold"); doc.setFontSize(fs); col(INK);
  P.cc.forEach((cl, i) => cl.forEach((v, k) => doc.text(String(v), gx + i * c + c / 2, gy - (cl.length - k - 1) * c * 0.62 - c * 0.18, { align: "center" })));
  P.rc.forEach((rl, j) => doc.text(rl.join(" "), gx - c * 0.25, gy + j * c + c * 0.7, { align: "right" }));
  if (solution) { fill(INK); P.sol.forEach((v, i) => { if (v) doc.rect(gx + (i % n) * c, gy + Math.floor(i / n) * c, c, c, "F"); }); }
  draw(INK); for (let i = 0; i <= n; i++) { doc.setLineWidth(i % 5 ? 0.15 : 0.55); doc.line(gx + i * c, gy, gx + i * c, gy + n * c); doc.line(gx, gy + i * c, gx + n * c, gy + i * c); }
}
// ---------------- Inhalt erzeugen
const levels = [["leicht", 20], ["mittel", 20], ["schwer", 20]];
const sud = levels.flatMap(([lv, k]) => Array.from({ length: k }, (_, i) => ({ lv, ...G.makeSudoku(G.hash(`heft${NR}-${lv}-${i}`), lv) })));
const nonos = [...Array.from({ length: 12 }, (_, i) => G.makeNono(G.hash(`heft${NR}-n10-${i}`), 10)), ...Array.from({ length: 12 }, (_, i) => G.makeNono(G.hash(`heft${NR}-n15-${i}`), 15))];
// ---------------- Titelseite
fill([234, 242, 239]); doc.rect(0, 0, W, H, "F");
fill(BUOY); doc.circle(W / 2, 92, 22, "F"); doc.setFont("helvetica", "bold"); doc.setFontSize(26); col([255, 255, 255]); doc.text(String(NR), W / 2, 101, { align: "center" });
doc.setFontSize(40); col(INK); doc.text("Rätselheft", W / 2, 140, { align: "center" });
doc.setFont("helvetica", "normal"); doc.setFontSize(13); col(SEA); doc.text("60 Sudokus · 24 Nonogramme · mit allen Lösungen", W / 2, 152, { align: "center" });
doc.setFontSize(10); col(MUTED); doc.text("Jedes Rätsel hat genau eine Lösung und ist ohne Raten lösbar.", W / 2, 162, { align: "center" });
doc.text("Zum Ausdrucken – für dich, deine Familie oder den Unterricht.", W / 2, 168, { align: "center" });
doc.setFontSize(9); doc.text("raetsellotse.de", W / 2, H - 20, { align: "center" });
// ---------------- Anleitung
newPage(); heading("So geht's");
doc.setFont("helvetica", "normal"); doc.setFontSize(10.5); col(INK);
const guide = [["Sudoku", "Fülle das 9×9-Gitter so, dass jede Ziffer von 1 bis 9 in jeder Zeile, jeder Spalte und jedem 3×3-Block genau einmal vorkommt. Die leichten und mittleren Sudokus lassen sich allein mit zwei Grundtechniken lösen: einzige Möglichkeit im Feld und einziger Platz für eine Ziffer. Die schweren verlangen mehr Überblick."],
  ["Nonogramm", "Die Zahlen am Rand jeder Zeile und Spalte geben an, wie viele zusammenhängende Felder dort gefüllt sind – in dieser Reihenfolge. Zwischen zwei Blöcken bleibt mindestens ein Feld frei. Markiere sichere Leerfelder mit einem kleinen Kreuz. Aus den gefüllten Feldern entsteht ein Muster."],
  ["Tipp für Nonogramme", "Beginne mit großen Zahlen: Steht in einer Zeile mit 10 Feldern die 8, sind die Felder 3 bis 8 sicher gefüllt – egal, wie man den Block verschiebt."],
  ["Lösungen", "Alle Lösungen stehen am Ende des Heftes. Online gibt es jeden Tag neue Rätsel kostenlos auf raetsellotse.de."]];
let gy = M + 22; guide.forEach(([t, s]) => { doc.setFont("helvetica", "bold"); doc.setFontSize(12); col(BUOY); doc.text(t, M, gy); gy += 6; doc.setFont("helvetica", "normal"); doc.setFontSize(10.5); col(INK); const l = doc.splitTextToSize(s, W - 2 * M); doc.text(l, M, gy); gy += l.length * 5 + 7; });
footer();
// ---------------- Sudokus: 4 pro Seite
const S = 82;
for (let i = 0; i < sud.length; i += 4) {
  newPage(); const lv = sud[i].lv; heading(`Sudoku ${lv}`, `Nr. ${i + 1}–${Math.min(i + 4, sud.length)}`);
  sud.slice(i, i + 4).forEach((s, k) => { const x = M + (k % 2) * (S + 16), y = M + 24 + Math.floor(k / 2) * (S + 30); doc.setFont("helvetica", "bold"); doc.setFontSize(10); col(SEA); doc.text(`Sudoku ${i + k + 1}`, x, y - 3); sudoku(s.puzzle, x, y, S); });
  footer();
}
// ---------------- Nonogramme: 10×10 zwei pro Seite, 15×15 eines pro Seite
for (let i = 0; i < nonos.length;) {
  const n = nonos[i].n; newPage(); heading(`Nonogramm ${n}×${n}`, `Nr. ${i + 1}${n === 10 ? "–" + (i + 2) : ""}`);
  const per = n === 10 ? 2 : 1, h = (H - M * 2 - 30) / per;
  for (let k = 0; k < per && i < nonos.length; k++, i++) { doc.setFont("helvetica", "bold"); doc.setFontSize(10); col(SEA); doc.text(`Nonogramm ${i + 1}`, M, M + 22 + k * h); nono(nonos[i], M, M + 26 + k * h, W - 2 * M, h - 12); }
  footer();
}
// ---------------- Lösungen
for (let i = 0; i < sud.length; i += 12) {
  newPage(); heading("Lösungen Sudoku", `Nr. ${i + 1}–${Math.min(i + 12, sud.length)}`);
  sud.slice(i, i + 12).forEach((s, k) => { const sz = 52, x = M + (k % 3) * (sz + 12), y = M + 22 + Math.floor(k / 3) * (sz + 12); doc.setFont("helvetica", "bold"); doc.setFontSize(8); col(SEA); doc.text(`Nr. ${i + k + 1}`, x, y - 2); sudoku(s.sol, x, y, sz, true); });
  footer();
}
for (let i = 0; i < nonos.length; i += 6) {
  newPage(); heading("Lösungen Nonogramm", `Nr. ${i + 1}–${Math.min(i + 6, nonos.length)}`);
  nonos.slice(i, i + 6).forEach((p, k) => { const w = (W - 2 * M - 12) / 2, h = (H - 2 * M - 40) / 3, x = M + (k % 2) * (w + 12), y = M + 22 + Math.floor(k / 2) * (h + 6); doc.setFont("helvetica", "bold"); doc.setFontSize(8); col(SEA); doc.text(`Nr. ${i + k + 1}`, x, y); nono(p, x, y + 3, w, h - 6, true); });
  footer();
}
const out = path.join(__dirname, "out"); fs.mkdirSync(out, { recursive: true });
const f = path.join(out, `Raetsellotse-Raetselheft-Nr-${NR}.pdf`); fs.writeFileSync(f, Buffer.from(doc.output("arraybuffer")));
console.log(path.basename(f), page, "Seiten", Math.round(fs.statSync(f).size / 1024), "KB");
