# Rätsellotse

Statische Website für https://raetsellotse.de – tägliche Rätsel (Codeknacker, Sudoku, Zielzahl), Sudokus zum Ausdrucken, Strategie-Artikel.

- `assets/games.js` – alle drei Spiele, Aufgaben werden aus dem Datum (Wien) erzeugt
- `build.py` – erzeugt `docs/` inkl. geprüfter Druck-Sudokus
- `assets/solver.js` – Sudoku-Löser mit erklärtem Lösungsweg (`/sudoku-loeser.html`), Tests: `node --test test_solver.js`, Browser: `node test_loeser_browser.js` (Server auf Port 8765 mit `docs/`)

Bauen: `pip install jinja2 && python3 build.py`
