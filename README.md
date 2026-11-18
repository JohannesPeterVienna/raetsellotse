# Rätsellotse

Statische Website für https://raetsellotse.de – tägliche Rätsel (Codeknacker, Sudoku, Zielzahl), Sudokus zum Ausdrucken, Strategie-Artikel.

- `assets/games.js` – alle drei Spiele, Aufgaben werden aus dem Datum (Wien) erzeugt
- `build.py` – erzeugt `docs/` inkl. geprüfter Druck-Sudokus
- `assets/solver.js` – Sudoku-Löser mit erklärtem Lösungsweg (`/sudoku-loeser.html`), Tests: `node --test test_solver.js`, Browser: `node test_loeser_browser.js` (Server auf Port 8765 mit `docs/`)

- `tools/auswertung.js` – bewertet alle Tagessudokus eines Zeitraums mit dem Löser und schreibt `content/tagessudoku.json` (Grundlage für `/sudoku-techniken-ueben.html`, die echten Stellungen in den Sudoku-Strategien und alle Zahlen zur Schwierigkeit). Neu erzeugen: `node tools/auswertung.js 2026-01-01 JJJJ-MM-TT`, danach die Zahlen in `content/` anpassen (build.py bricht sonst ab). Test: `node --test test_auswertung.js`

Bauen: `pip install jinja2 && python3 build.py`

Test Werbeplätze (nach dem Bauen, Playwright): `node --test test_werbeplaetze.js` – leere Werbeplätze bleiben unsichtbar, gefüllte erscheinen mit Abstand.
