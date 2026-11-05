"""Sudoku-Löser mit Lösungsweg: Bedienoberfläche und Erklärtext (eigene Seite /sudoku-loeser.html)."""

UI = """<div class="ltools no-print">
<label class="small">Beispiel laden <select data-beispiel><option value="">– wählen –</option><option value="stufe1">Stufe 1 · Einstieg</option><option value="stufe2">Stufe 2 · Fortgeschritten</option><option value="stufe3">Stufe 3 · Schwer (mit XY-Wing)</option><option value="stufe4">Stufe 4 · Sehr schwer</option></select></label>
</div>
<div class="sgrid lgrid" data-lgrid role="group" aria-label="Sudoku zum Lösen: 81 Eingabefelder, Pfeiltasten wechseln das Feld"></div>
<div class="pad">
<button type="button" class="btn" data-next>Nächster Schritt</button>
<button type="button" class="wide" data-all>Ganzer Lösungsweg</button>
<button type="button" class="wide" data-check>Prüfen &amp; Stufe</button>
<button type="button" class="wide" data-cands aria-pressed="false">Kandidaten</button>
<button type="button" class="wide" data-clear>Leeren</button>
</div>
<p class="msg" data-lmsg aria-live="polite"></p>
<details class="lpaste no-print"><summary>Sudoku als Zeichenkette einfügen oder als Link teilen</summary>
<p class="small muted">81 Zeichen, Zeile für Zeile von links oben: Ziffern 1–9, leere Felder als 0 oder Punkt. Leerzeichen und Zeilenumbrüche werden ignoriert.</p>
<textarea data-text rows="3" spellcheck="false" aria-label="Sudoku als Zeichenkette"></textarea>
<p><button type="button" class="btn small" data-load>Übernehmen</button> <button type="button" class="btn small ghost" data-link>Link zu diesem Sudoku kopieren</button></p>
</details>
<ol class="lsteps" data-steps aria-label="Lösungsweg"></ol>
<noscript><p>Für den Löser wird JavaScript benötigt. Die Techniken erklären die <a href="/sudoku-strategien.html">Sudoku-Strategien</a>.</p></noscript>
<script src="/assets/solver.js?v={v}" defer></script>"""

BODY = """<h2>So benutzt du den Sudoku-Löser</h2>
<p>Tippe die Vorgaben deines Sudokus in das Gitter: Feld anklicken, Ziffer eingeben, der Cursor springt weiter. Mit den Pfeiltasten wechselst du das Feld, mit der Rücktaste löschst du. Auf dem Handy öffnet sich automatisch die Zifferntastatur. Leere Felder bleiben einfach leer. Wer das Rätsel schon als Text hat, etwa aus einer anderen App, fügt es unter „Sudoku als Zeichenkette einfügen“ ein: 81 Zeichen, Zeile für Zeile, leere Felder als 0 oder Punkt.</p>
<p>Dann hast du drei Möglichkeiten. <strong>Nächster Schritt</strong> zeigt genau einen logischen Schritt und begründet ihn: welche Ziffer wohin gehört oder welche Kandidaten wegfallen – und warum. Die beteiligten Felder werden hervorgehoben, gestrichene Kandidaten erscheinen durchgestrichen in Orange. <strong>Ganzer Lösungsweg</strong> rechnet alle Schritte bis zum Ende durch und listet sie unter dem Gitter auf. <strong>Prüfen &amp; Stufe</strong> verrät nichts, sondern sagt nur, ob das Sudoku genau eine Lösung hat und wie schwer es ist.</p>
<p>Zur Orientierung: Zeilen zählen wir von oben nach unten, Spalten von links nach rechts, jeweils 1 bis 9. Im Lösungsweg kürzen wir Felder ab – „Z3/S5“ ist das fünfte Feld in der dritten Zeile. Die neun Blöcke sind wie beim Lesen nummeriert: Block 1 oben links, Block 3 oben rechts, Block 9 unten rechts. Vom Löser gesetzte Ziffern erscheinen blau, deine Vorgaben schwarz.</p>
<p>Über „Link zu diesem Sudoku kopieren“ kannst du ein Rätsel weitergeben: Wer den Link öffnet, sieht genau deine Vorgaben – praktisch, wenn in der Familie oder im Rätselclub alle am selben Zeitungs-Sudoku hängen.</p>

<h2>Lösungsweg statt Lösung: warum Schritt für Schritt?</h2>
<p>Die meisten Sudoku-Löser im Netz füllen das Gitter in einem Rutsch aus. Das ist schnell, aber man lernt nichts daraus – und das Rätsel ist verdorben. Unser Löser arbeitet so, wie ein Mensch mit Bleistift vorgeht: Er sucht immer zuerst den einfachsten Schritt, der noch weiterhilft, und erklärt ihn in Worten. Wer an einer Stelle festhängt, holt sich genau einen Hinweis und rätselt danach selbst weiter.</p>
<p>Technisch steckt dahinter kein Ausprobieren. Der Löser führt für jedes leere Feld eine Liste der Kandidaten, also der Ziffern, die dort nach den Regeln noch möglich sind. Jeder Schritt setzt entweder eine Ziffer, die sich zwingend ergibt, oder streicht Kandidaten, die nachweislich nicht in Frage kommen. Raten, Zurücknehmen und „mal sehen, ob es aufgeht“ gibt es im Lösungsweg nicht.</p>

<h2>Die Techniken im Lösungsweg</h2>
<p>Der Löser kennt zehn Lösungstechniken und probiert sie in dieser Reihenfolge. Die Einteilung in Stufen entspricht der in unserem Beitrag <a href="/schweres-sudoku-erkennen.html">Woran man ein schweres Sudoku erkennt</a>; Diagramme zu den wichtigsten Techniken findest du in den <a href="/sudoku-strategien.html">Sudoku-Strategien</a>.</p>
<div class="scroll"><table class="tbl"><thead><tr><th scope="col">Technik</th><th scope="col">Stufe</th><th scope="col">Was dabei passiert</th></tr></thead><tbody>
<tr><td>Einziger Platz (Hidden Single)</td><td>1</td><td>Eine Ziffer kann in einem Block, einer Zeile oder Spalte nur noch an einer Stelle stehen.</td></tr>
<tr><td>Einzige Möglichkeit (Naked Single)</td><td>1</td><td>In einem Feld ist nur noch eine Ziffer möglich.</td></tr>
<tr><td>Block-Zeile-Regel</td><td>2</td><td>Liegen alle Kandidaten einer Ziffer in einem Block auf einer Linie, fällt sie im Rest dieser Linie weg – und umgekehrt.</td></tr>
<tr><td>Paar (Naked Pair)</td><td>2</td><td>Zwei Felder einer Einheit haben dieselben zwei Kandidaten; diese Ziffern fallen in den übrigen Feldern weg.</td></tr>
<tr><td>Verstecktes Paar (Hidden Pair)</td><td>2</td><td>Zwei Ziffern passen nur in dieselben zwei Felder; alle anderen Kandidaten dort fallen weg.</td></tr>
<tr><td>Tripel und verstecktes Tripel</td><td>3</td><td>Dasselbe Prinzip mit drei Feldern und drei Ziffern.</td></tr>
<tr><td>X-Wing</td><td>3</td><td>Eine Ziffer ist in zwei Zeilen nur in denselben zwei Spalten möglich (oder umgekehrt) und fällt im Rest dieser Spalten weg.</td></tr>
<tr><td>Swordfish</td><td>3</td><td>Der große Bruder des X-Wing: drei Zeilen, drei Spalten.</td></tr>
<tr><td>XY-Wing</td><td>3</td><td>Drei Felder mit je zwei Kandidaten bilden eine Zange: Ein Feld, das beide Zangenenden sieht, kann die gemeinsame Ziffer nicht haben.</td></tr>
</tbody></table></div>
<p>Die Reihenfolge ist bewusst gewählt. Hidden Singles kommen vor Naked Singles, weil man sie ohne Notizen findet: Man fährt mit dem Blick eine Ziffer durch alle Blöcke. Erst wenn das nichts mehr bringt, lohnt es sich, Kandidaten zu notieren. Der Knopf „Kandidaten“ blendet sie im Gitter ein, so wie sie der Löser gerade sieht.</p>

<h2>Wie schwer ist mein Sudoku?</h2>
<p>Die Zahl der Vorgaben sagt wenig über die Schwierigkeit. Entscheidend ist die anspruchsvollste Technik, ohne die es nicht weitergeht. Genau so bewertet „Prüfen &amp; Stufe“ dein Rätsel: Stufe 1 heißt, dass die beiden Grundtechniken reichen. Stufe 2 verlangt Notizen und gezieltes Streichen. Stufe 3 braucht Muster über mehrere Einheiten wie X-Wing oder XY-Wing. Stufe 4 bedeutet: Mit den zehn Techniken dieser Seite geht es irgendwo nicht weiter.</p>
<p>Wie sich das in der Praxis verteilt, haben wir für diese Seite nachgezählt. Wir haben mit dem Generator unserer <a href="/sudoku.html">Tagessudokus</a> je 100 leichte und mittlere sowie 300 schwere Rätsel erzeugt und vom Löser bewerten lassen:</p>
<div class="scroll"><table class="tbl"><thead><tr><th scope="col">Rätsel</th><th scope="col">Stufe 1</th><th scope="col">Stufe 2</th><th scope="col">Stufe 3</th><th scope="col">Stufe 4</th></tr></thead><tbody>
<tr><td>leicht (100, 38 Vorgaben)</td><td>100 %</td><td>–</td><td>–</td><td>–</td></tr>
<tr><td>mittel (100, 30 Vorgaben)</td><td>100 %</td><td>–</td><td>–</td><td>–</td></tr>
<tr><td>schwer (300, rund 25 Vorgaben)</td><td>53 %</td><td>18 %</td><td>5 %</td><td>24 %</td></tr>
</tbody></table></div>
<p>Bei den schweren Rätseln der Stufe 2 war fast immer die Block-Zeile-Regel der schwierigste Schritt (53 von 54). In Stufe 3 gaben am häufigsten der XY-Wing (7 Rätsel) und der X-Wing (4) den Ausschlag, dazu Tripel (4). Knapp ein Viertel verlangte mehr, als dieser Löser erklären kann. Die Stichprobe ist eine andere als im Beitrag über schwere Sudokus, deshalb weichen die Anteile dort leicht ab; das Bild ist dasselbe: Leichte und mittlere Tagessudokus gehen allein mit Stufe-1-Techniken auf, schwere streuen stark.</p>

<h2>Wenn der Löser nicht weiterkommt</h2>
<p>Manche Sudokus lassen sich nur mit sogenannten Ketten-Techniken knacken: Man verfolgt eine Annahme über viele Felder hinweg, bis sie zu einem Widerspruch führt. Solche Schritte lassen sich schwer in zwei Sätzen erklären, deshalb macht unser Löser sie nicht. Er sagt dann offen, dass es mit den erklärten Techniken nicht weitergeht. Du kannst anschließend ein einzelnes Feld aufdecken lassen – der Löser wählt das Feld mit den wenigsten Kandidaten – oder dir die ganze Lösung zeigen lassen. Aufgedeckte Ziffern erscheinen in Orange, damit klar bleibt, was erklärt wurde und was nicht. Danach geht der Lösungsweg oft wieder mit einfachen Schritten weiter.</p>

<h2>„Keine Lösung“ oder „mehr als eine Lösung“?</h2>
<p>Bevor der Löser den ersten Schritt macht, prüft er dein Sudoku vollständig. Steht eine Ziffer doppelt in einer Zeile, Spalte oder einem Block, werden die Felder markiert. Hat das Rätsel gar keine Lösung, steckt fast immer ein Tippfehler in den Vorgaben: eine 6 statt einer 8, eine Ziffer eine Spalte zu weit rechts. Vergleiche die Eingabe dann Zeile für Zeile mit deiner Vorlage.</p>
<p>Hat es mehr als eine Lösung, fehlt meist eine Vorgabe. Ein ordentliches Sudoku hat genau eine Lösung, sonst müsste man an irgendeiner Stelle raten. Mit weniger als 17 Vorgaben ist das sogar mathematisch ausgeschlossen: Gary McGuire, Bastian Tugemann und Gilles Civario haben 2012 mit einer großen Computersuche gezeigt, dass es kein eindeutiges Sudoku mit 16 Vorgaben gibt. Mehr Zahlen rund um das Rätsel stehen in <a href="/sudoku-regeln-und-geschichte.html">Sudoku: Regeln und Geschichte</a>.</p>

<h2>Wie wir den Löser geprüft haben</h2>
<p>Ein Löser, der falsche Hinweise gibt, wäre schlimmer als gar keiner. Deshalb läuft vor jeder Veröffentlichung ein automatischer Test: Für mehr als 260 Rätsel mit 24 bis 38 Vorgaben wird zuerst per vollständiger Suche die einzige Lösung bestimmt. Danach geht der Test den erklärten Lösungsweg Schritt für Schritt durch und kontrolliert, dass jede gesetzte Ziffer mit dieser Lösung übereinstimmt und keine gestrichene Ziffer die richtige war. Jede der zehn Techniken kommt in den Testrätseln vor. Auch die Beispiele im Auswahlfeld oben sind so geprüft und haben die angegebene Stufe.</p>

<h2>Deine Daten</h2>
<p>Der Löser läuft vollständig in deinem Browser. Die eingegebenen Ziffern werden nicht an uns oder an Dritte übertragen und nicht gespeichert. Nur wenn du selbst einen Link kopierst, stehen die Vorgaben als Zeichenkette in der Adresse.</p>

<h2>Häufige Fragen</h2>
<h3>Ist das nicht Schummeln?</h3>
<p>Wenn du dir die Lösung zeigen lässt, ein bisschen. Wenn du dir einen Schritt erklären lässt und danach selbst weitermachst, ist es eher Nachhilfe. Viele lernen neue Techniken genau so: an der Stelle, an der sie selbst feststecken.</p>
<h3>Funktioniert der Löser mit Sudokus aus Zeitung und Rätselheft?</h3>
<p>Ja, mit jedem klassischen 9×9-Sudoku. Varianten wie Killer-Sudoku, Diagonal-Sudoku oder Sudokus mit Zusatzregeln kann er nicht lösen, weil dort andere Regeln gelten.</p>
<h3>Warum zeigt der Löser andere Schritte als mein Rätselheft?</h3>
<p>Meist führen mehrere Wege zum Ziel. Der Löser nimmt immer den einfachsten verfügbaren Schritt und sucht Hidden Singles zuerst in den Blöcken, dann in Zeilen und Spalten. Ein anderer Weg ist deshalb nicht falsch, nur anders.</p>
<h3>Kann ich das Ergebnis ausdrucken?</h3>
<p>Für Papier gibt es eigene Seiten: <a href="/sudoku-zum-ausdrucken-leicht.html">Sudokus zum Ausdrucken</a> mit Lösungen und das tägliche <a href="/raetselblatt.html">Rätselblatt</a>.</p>

<h2>Quellen</h2>
<ul class="small"><li>McGuire, Tugemann, Civario: <a href="https://arxiv.org/abs/1201.0749" rel="noopener">There is no 16-Clue Sudoku</a> (arXiv, 2012); verständliche Zusammenfassung bei <a href="https://www.sudokuwiki.org/17_clue_proof" rel="noopener">SudokuWiki</a>.</li>
<li>Überblick über menschliche und maschinelle Lösungsverfahren: <a href="https://en.wikipedia.org/wiki/Sudoku_solving_algorithms" rel="noopener">Sudoku solving algorithms</a> (Wikipedia, englisch).</li>
<li>Auswertung der Stufen: eigene Zählung mit dem Generator und dem Löser dieser Website, November 2026.</li></ul>"""
