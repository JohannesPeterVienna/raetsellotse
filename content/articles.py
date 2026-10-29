"""Anleitungen und Strategie-Artikel für Rätsellotse."""

ARTICLES = [
{
"slug": "codeknacker-anleitung",
"title": "Codeknacker: Regeln und Strategie",
"teaser": "Wie die Hinweise funktionieren und wie du den Code systematisch eingrenzt.",
"description": "Codeknacker spielen: Regeln, Bedeutung der orangen und weißen Punkte und eine Strategie, mit der du den Zahlencode systematisch knackst.",
"body": """
<p>Gesucht ist ein Code aus vier <strong>verschiedenen</strong> Ziffern von 1 bis 6. Du hast zehn Versuche. Nach jedem Versuch bekommst du Hinweise – aber nicht, welche Ziffer gemeint ist.</p>
<h2>Die Hinweise</h2>
<ul><li><strong>Oranger Punkt:</strong> Eine deiner Ziffern ist richtig und steht an der richtigen Stelle.</li>
<li><strong>Weißer Punkt mit orangem Rand:</strong> Eine Ziffer kommt im Code vor, steht aber an einer anderen Stelle.</li>
<li><strong>Grauer Punkt:</strong> Eine Ziffer kommt nicht vor.</li></ul>
<p>Die Reihenfolge der Punkte verrät nicht, zu welcher Ziffer sie gehören.</p>
<h2>Eine bewährte Strategie</h2>
<ol><li><strong>Ziffern finden:</strong> Weil vier von sechs Ziffern vorkommen, fehlen genau zwei. Ein erster Versuch mit 1 2 3 4 zeigt, wie viele davon dabei sind: mindestens zwei, höchstens vier.</li>
<li><strong>Austauschen:</strong> Tausche eine Ziffer gegen 5 oder 6. Ändert sich die Zahl der Punkte, weißt du, welche Ziffer rein- oder rausgefallen ist.</li>
<li><strong>Positionen klären:</strong> Sobald die vier Ziffern feststehen, verschiebst du sie gezielt. Jeder orange Punkt schließt viele Anordnungen aus.</li>
<li><strong>Jeden Versuch nutzen:</strong> Wähle nur Codes, die zu allen bisherigen Hinweisen passen. Dann ist jeder Versuch auch eine mögliche Lösung.</li></ol>
<h2>Wie viele Codes gibt es?</h2>
<p>Für die erste Stelle gibt es 6 Möglichkeiten, für die zweite 5, dann 4 und 3: 6 × 5 × 4 × 3 = 360 mögliche Codes. Ein guter erster Versuch teilt sie in kleine Gruppen auf – darum lohnt sich Systematik mehr als Raten.</p>
<p>Das Spiel ist mit dem Brettspiel „Mastermind“ verwandt, das in den 1970er-Jahren bekannt wurde. Dort gibt es Farben statt Ziffern.</p>
<p><a href="/codeknacker.html">Zum heutigen Codeknacker</a></p>
""",
},
{
"slug": "sudoku-strategien",
"title": "Sudoku-Strategien: von einfach bis schwer",
"teaser": "Fünf Techniken, mit denen du fast jedes Sudoku ohne Raten löst.",
"description": "Sudoku lösen ohne Raten: Naked Single, Hidden Single, Paare, Zeilen-Block-Wechselwirkung und X-Wing verständlich erklärt.",
"body": """
<p>Jedes gute Sudoku lässt sich ohne Raten lösen. Leichte Rätsel brauchen nur die ersten beiden Techniken, schwere die weiteren.</p>
<h2>1. Einzige Möglichkeit im Feld (Naked Single)</h2>
<p>Streiche für ein leeres Feld alle Ziffern, die schon in derselben Zeile, Spalte oder im selben 3×3-Block stehen. Bleibt nur eine übrig, ist sie die Lösung.</p>
<h2>2. Einziger Platz für eine Ziffer (Hidden Single)</h2>
<p>Frag umgekehrt: Wo in dieser Zeile, Spalte oder diesem Block kann die 7 noch stehen? Gibt es nur ein passendes Feld, gehört die 7 dorthin – auch wenn in diesem Feld rechnerisch noch andere Ziffern möglich wären.</p>
<h2>3. Paare (Naked Pair)</h2>
<p>Haben zwei Felder einer Zeile genau dieselben zwei Kandidaten, etwa 3 und 8, müssen die 3 und die 8 in diesen beiden Feldern stehen. In allen anderen Feldern dieser Zeile kannst du 3 und 8 als Kandidaten streichen.</p>
<h2>4. Block und Zeile (Pointing)</h2>
<p>Kann eine Ziffer innerhalb eines Blocks nur in einer bestimmten Zeile stehen, steht sie dort sicher. Dann darf sie in derselben Zeile außerhalb des Blocks nicht mehr vorkommen.</p>
<h2>5. X-Wing</h2>
<p>Kommt eine Ziffer in zwei Zeilen jeweils nur in denselben zwei Spalten in Frage, bilden diese vier Felder ein Rechteck. Die Ziffer steht dann in zwei gegenüberliegenden Ecken – und kann in diesen beiden Spalten aus allen anderen Zeilen gestrichen werden.</p>
<div class="example"><strong>Tipp für den Einstieg:</strong> Notiere Kandidaten mit dem Notizmodus (Taste N). Die Tipp-Funktion im <a href="/sudoku.html">Tagessudoku</a> erklärt immer, welche Regel gerade greift.</div>
""",
},
{
"slug": "sudoku-regeln-und-geschichte",
"title": "Sudoku: Regeln, Herkunft und erstaunliche Zahlen",
"teaser": "Woher das Zahlenrätsel kommt und warum 17 eine magische Zahl ist.",
"description": "Sudoku-Regeln einfach erklärt, die Geschichte von Number Place über Nikoli bis zur weltweiten Verbreitung und erstaunliche Fakten zu Sudoku.",
"body": """
<p>Ein Sudoku ist ein 9×9-Gitter, das in neun Blöcke zu 3×3 Feldern unterteilt ist. Ziel ist es, jedes leere Feld mit einer Ziffer von 1 bis 9 zu füllen – so, dass jede Ziffer in jeder Zeile, jeder Spalte und jedem Block genau einmal vorkommt.</p>
<h2>Woher Sudoku kommt</h2>
<p>Trotz des japanischen Namens stammt das Rätsel aus den USA. Der Architekt Howard Garns entwarf es; ab 1979 erschien es im Verlag Dell Magazines unter dem Namen „Number Place“. Der japanische Rätselverlag Nikoli übernahm die Idee 1984 und gab ihr den Namen Sudoku, kurz für „Ziffern dürfen nur einmal vorkommen“. Weltweit bekannt wurde es ab 2004, als die britische Zeitung The Times täglich Sudokus druckte.</p>
<h2>Erstaunliche Zahlen</h2>
<ul><li><strong>17 Vorgaben</strong> sind das Minimum: Ein Sudoku mit eindeutiger Lösung braucht mindestens 17 vorgegebene Ziffern. Das bewiesen Mathematiker um Gary McGuire 2012 mit einer aufwendigen Computersuche.</li>
<li><strong>Rund 6,67 Trilliarden</strong> vollständig ausgefüllte Sudoku-Gitter gibt es – eine Zahl mit 22 Stellen.</li>
<li><strong>Keine Mathematik nötig:</strong> Die Ziffern sind nur Symbole. Man könnte genauso neun Farben oder Buchstaben verwenden.</li></ul>
<h2>Woran man ein gutes Sudoku erkennt</h2>
<p>Ein gutes Sudoku hat genau eine Lösung und lässt sich ohne Raten lösen. Die Anzahl der Vorgaben sagt wenig über die Schwierigkeit: Entscheidend ist, welche Lösungstechniken man braucht. Unsere leichten und mittleren Rätsel lassen sich allein mit den einfachen Techniken aus den <a href="/sudoku-strategien.html">Sudoku-Strategien</a> lösen.</p>
""",
},
{
"slug": "zielzahl-tipps",
"title": "Zielzahl: Regeln und Tipps zum Kopfrechnen",
"teaser": "Mit großen Zahlen nah ran, mit kleinen fein justieren.",
"description": "Zielzahl spielen: die Regeln, Rechenstrategien für schnelles Kopfrechnen und Beispiele, wie man aus sechs Zahlen die Zielzahl trifft.",
"body": """
<p>Aus sechs Zahlen sollst du mit den vier Grundrechenarten die Zielzahl erreichen. Jede Zahl darfst du höchstens einmal verwenden, du musst aber nicht alle benutzen. Teilen ist nur erlaubt, wenn es ohne Rest aufgeht, und Zwischenergebnisse dürfen nicht negativ werden.</p>
<h2>Strategien</h2>
<ol><li><strong>Erst grob, dann fein:</strong> Suche mit den großen Zahlen eine Multiplikation, die nahe an die Zielzahl führt. Bei 637 etwa 100 × 6 = 600 – dann fehlen noch 37.</li>
<li><strong>Den Rest mit kleinen Zahlen bauen:</strong> 37 = 4 × 9 + 1, oder 25 + 10 + 2.</li>
<li><strong>Von der Zielzahl aus denken:</strong> Ist die Zielzahl durch eine der kleinen Zahlen teilbar? 637 = 7 × 91 – und 91 lässt sich vielleicht leichter bauen.</li>
<li><strong>Klammern nutzen:</strong> (75 − 3) × 9 ist oft eleganter als viele Einzelschritte.</li></ol>
<h2>Beispiel</h2>
<div class="example">Zahlen: 100, 50, 9, 6, 4, 1 · Zielzahl: 637<br>Lösung: 100 × 6 + 4 × 9 + 1 = 600 + 36 + 1 = 637</div>
<h2>Woher das Spiel kommt</h2>
<p>Die Idee stammt aus der französischen Fernsehshow „Des chiffres et des lettres“. In Großbritannien wurde sie ab 1982 als „Countdown“ bekannt.</p>
<p><a href="/zielzahl.html">Zur heutigen Zielzahl</a></p>
""",
},
]
