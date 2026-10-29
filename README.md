# Rätsellotse

Statische Website für https://raetsellotse.de – tägliche Rätsel (Codeknacker, Sudoku, Zielzahl), Sudokus zum Ausdrucken, Strategie-Artikel.

- `assets/games.js` – alle drei Spiele, Aufgaben werden aus dem Datum (Wien) erzeugt
- `build.py` – erzeugt `docs/` inkl. geprüfter Druck-Sudokus

Bauen: `pip install jinja2 && python3 build.py`
