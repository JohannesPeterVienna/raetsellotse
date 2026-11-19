# Rätsellotse

Statische Website für https://raetsellotse.de – tägliche Rätsel (Codeknacker, Sudoku, Zielzahl), Sudokus zum Ausdrucken, Strategie-Artikel.

- `assets/games.js` – alle drei Spiele, Aufgaben werden aus dem Datum (Wien) erzeugt
- `build.py` – erzeugt `docs/` inkl. geprüfter Druck-Sudokus
- `assets/solver.js` – Sudoku-Löser mit erklärtem Lösungsweg (`/sudoku-loeser.html`), Tests: `node --test test_solver.js`, Browser: `node test_loeser_browser.js` (Server auf Port 8765 mit `docs/`)

- `tools/auswertung.js` – bewertet alle Tagessudokus eines Zeitraums mit dem Löser und schreibt `content/tagessudoku.json` (Grundlage für `/sudoku-techniken-ueben.html`, die echten Stellungen in den Sudoku-Strategien und alle Zahlen zur Schwierigkeit). Neu erzeugen: `node tools/auswertung.js 2026-01-01 JJJJ-MM-TT`, danach die Zahlen in `content/` anpassen (build.py bricht sonst ab). Test: `node --test test_auswertung.js`

Bauen: `pip install jinja2 && python3 build.py`

Test Werbeplätze (nach dem Bauen, Playwright): `node --test test_werbeplaetze.js` – leere Werbeplätze bleiben unsichtbar, gefüllte erscheinen mit Abstand.

Werbeplätze (Stand 19.11.2026): oben ein Streifen direkt unter der Kopfzeile (ab 768 px Superbanner 728×90, darunter Mobile Banner 320×100, unter 360 px keiner) – seine Höhe ist in `assets/style.css` von Anfang an reserviert, damit beim Füllen nichts springt; der frühere Platz vor der Fußzeile entfällt dafür. Im Text steht der responsive Platz erst nach dem ersten Inhaltsblock (`teile_text` in `build.py`, Marke `<!--PLATZ-->`), in der Seitenleiste folgen Half Page und Skyscraper auf den Link-Kasten. Auf Spielseiten gibt es keine Seitenleisten-Werbung. Der Test prüft je Seitentyp bei 1366×768 und 390×844: oberster Platz im ersten Bildschirm, ≥ 150 px zu Bedienelementen, ≥ 32 px zu Navigation, Überschrift sichtbar, kein Sprung (CLS), kein Überlauf, keine JS-Fehler über die Sitemap.
