"""Ausführliche Texte für die Spielseiten (Regeln, Strategie, Fragen)."""

CODE = """
<h2>So spielst du Codeknacker</h2>
<p>Gesucht ist ein Code aus vier <strong>verschiedenen</strong> Ziffern von 1 bis 6. Tippe vier Ziffern an und drücke „Prüfen“ – oder nutze die Tastatur: Ziffern 1 bis 6, Enter zum Prüfen, Rücktaste zum Löschen. Nach jedem Versuch zeigen dir Punkte, wie nah du dran bist:</p>
<ul><li><strong>Oranger Punkt:</strong> eine Ziffer stimmt und steht an der richtigen Stelle.</li>
<li><strong>Weißer Punkt mit orangem Rand:</strong> eine Ziffer kommt vor, steht aber woanders.</li>
<li><strong>Grauer Punkt:</strong> eine Ziffer kommt im Code nicht vor.</li></ul>
<p>Welche Ziffer welchen Punkt bekommt, verraten die Hinweise nicht – genau das macht den Reiz aus. Du hast zehn Versuche.</p>
<h2>Drei Tipps für den Einstieg</h2>
<ol><li><strong>Starte breit:</strong> 1 2 3 4 als erster Versuch zeigt, wie viele dieser vier Ziffern dabei sind. Da genau zwei der sechs Ziffern fehlen, sind es mindestens zwei.</li>
<li><strong>Ändere wenig auf einmal:</strong> Tauschst du nur eine Ziffer aus, erkennst du an der Veränderung der Punkte genau, was sie bewirkt hat.</li>
<li><strong>Spiele nur mögliche Codes:</strong> Jeder neue Versuch sollte zu allen bisherigen Hinweisen passen. Dann kann er selbst schon die Lösung sein.</li></ol>
<p>Die vollständige Strategie mit Rechenbeispiel steht in der <a href="/codeknacker-anleitung.html">Codeknacker-Anleitung</a>.</p>
<h2>Häufige Fragen</h2>
<p><strong>Ist der Code für alle gleich?</strong> Ja. Jeden Tag um Mitternacht (Wiener Zeit) gibt es einen neuen Code, der für alle Spielerinnen und Spieler gilt. So kannst du dein Ergebnis teilen, ohne die Lösung zu verraten – der Teilen-Knopf verschickt nur die Punkte.</p>
<p><strong>Kann ich frühere Tage nachspielen?</strong> Ja, über das Datumsfeld oben im Spiel oder in deiner <a href="/archiv.html">Statistik</a>. Nachgespielte Tage zählen allerdings nicht für die Serie.</p>
<p><strong>Wie viele Versuche braucht man im Schnitt?</strong> Mit systematischem Vorgehen schaffen es geübte Spieler meist in fünf bis sieben Versuchen. Es gibt 360 mögliche Codes – zehn Versuche reichen mit Logik immer aus.</p>
"""

SUDOKU = """
<h2>Regeln</h2>
<p>Fülle das 9×9-Gitter so, dass in jeder Zeile, jeder Spalte und jedem der neun 3×3-Blöcke jede Ziffer von 1 bis 9 genau einmal vorkommt. Die vorgegebenen Ziffern sind fett und lassen sich nicht ändern.</p>
<h2>Bedienung</h2>
<ul><li>Feld antippen, dann Ziffer wählen – oder Pfeiltasten und Zifferntasten verwenden.</li>
<li><strong>Notizen</strong> (Taste N) schaltet auf kleine Kandidaten-Ziffern um. So hältst du fest, welche Ziffern in einem Feld noch möglich sind.</li>
<li><strong>Tipp</strong> zeigt zuerst falsche Einträge. Ist alles richtig, erklärt er den nächsten logischen Schritt – etwa „In dieser Zeile kann die 7 nur noch hier stehen“.</li>
<li>Gleiche Ziffern werden hervorgehoben, Konflikte rot markiert.</li></ul>
<h2>Die drei Schwierigkeitsstufen</h2>
<p>Jedes Sudoku auf Rätsellotse hat <strong>genau eine Lösung</strong>. Das prüft unser Programm, bevor ein Rätsel erscheint. <strong>Leicht</strong> und <strong>mittel</strong> lassen sich allein mit den beiden Grundtechniken lösen: „einzige Möglichkeit im Feld“ und „einziger Platz für eine Ziffer“. Mittel hat dabei weniger Vorgaben. <strong>Schwer</strong> hat rund 25 Vorgaben und verlangt Techniken wie Paare oder die Wechselwirkung von Block und Zeile.</p>
<h2>So kommst du weiter, wenn du feststeckst</h2>
<ol><li>Gehe die Ziffern der Reihe nach durch: Wo kann die 1 in jedem Block noch stehen? Dann die 2, und so weiter.</li>
<li>Schau auf fast volle Zeilen, Spalten und Blöcke – dort fehlen nur wenige Ziffern.</li>
<li>Trage Notizen ein und suche Paare: Zwei Felder mit denselben zwei Kandidaten blockieren diese Ziffern für den Rest der Einheit.</li></ol>
<p>Alle Techniken mit Beispielen erklären die <a href="/sudoku-strategien.html">Sudoku-Strategien</a>. Lieber auf Papier? Dann probier die <a href="/sudoku-zum-ausdrucken-mittel.html">Sudokus zum Ausdrucken</a> mit Lösungen.</p>
<h2>Häufige Fragen</h2>
<p><strong>Wird mein Fortschritt gespeichert?</strong> Ja, automatisch in deinem Browser. Du kannst das Sudoku schließen und später weitermachen – auf demselben Gerät.</p>
<p><strong>Muss man raten?</strong> Nein. Jedes Sudoku hier ist so gebaut, dass jeder Schritt logisch begründbar ist.</p>
"""

ZIEL = """
<h2>Regeln</h2>
<p>Aus sechs Zahlen sollst du mit Plus, Minus, Mal und Geteilt die Zielzahl erreichen. Dabei gilt:</p>
<ul><li>Jede Zahl darf höchstens einmal verwendet werden. Du musst nicht alle benutzen.</li>
<li>Teilen ist nur erlaubt, wenn es ohne Rest aufgeht.</li>
<li>Zwischenergebnisse dürfen nicht negativ werden.</li>
<li>Klammern sind erlaubt – auch mehrfach verschachtelt.</li></ul>
<p>Jede Zielzahl ist garantiert erreichbar: Wir erzeugen sie, indem wir die Zahlen des Tages selbst zufällig verrechnen.</p>
<h2>So gibst du deine Rechnung ein</h2>
<p>Tippe die Zahlen an oder schreib die Rechnung direkt ins Feld, zum Beispiel <code>(75 + 25) × 6 − 9</code>. Statt × und ÷ kannst du auch * und / oder einen Doppelpunkt verwenden. Das Ergebnis erscheint sofort, ebenso dein bisher bestes Ergebnis. Kommst du nicht weiter, zeigt „Lösung zeigen“ einen möglichen Weg – dann zählt der Tag allerdings nicht für deine Serie.</p>
<h2>Strategie in drei Schritten</h2>
<ol><li><strong>Grob anpeilen:</strong> Suche mit den großen Zahlen ein Produkt nahe der Zielzahl. Bei 637 und den Zahlen 100 und 6: 600.</li>
<li><strong>Den Rest bauen:</strong> Die fehlenden 37 entstehen aus den kleinen Zahlen, etwa 4 × 9 + 1.</li>
<li><strong>Rückwärts denken:</strong> Ist die Zielzahl durch eine kleine Zahl teilbar? 637 = 7 × 91 – vielleicht ist 91 leichter zu erreichen.</li></ol>
<p>Weitere Kniffe stehen in den <a href="/zielzahl-tipps.html">Zielzahl-Tipps</a>.</p>
<h2>Warum Kopfrechnen Spaß machen kann</h2>
<p>Zielzahl verbindet Rechnen mit Knobeln: Es gibt fast immer mehrere Wege, und der eleganteste ist selten der erste, der einem einfällt. Wer regelmäßig spielt, erkennt Muster schneller – etwa, dass 25 × 4 = 100 ist oder dass sich Zahlen nahe einem Vielfachen von 25 gut anpeilen lassen.</p>
"""

NONO = """
<h2>So funktioniert ein Nonogramm</h2>
<p>Ein Nonogramm ist ein Logikrätsel, bei dem ein verstecktes Bild entsteht. Die Zahlen am Rand jeder Zeile und Spalte geben an, wie viele <strong>zusammenhängende Felder</strong> dort gefüllt sind – und in welcher Reihenfolge. „3 1“ bedeutet: zuerst ein Block aus drei gefüllten Feldern, dann mindestens ein leeres Feld, dann ein einzelnes gefülltes Feld. Eine „0“ heißt: Die ganze Reihe bleibt leer.</p>
<p>Nonogramme heißen auch Japanische Rätsel, Paint by Numbers, Griddler oder Picross. Erfunden wurden sie Ende der 1980er-Jahre in Japan.</p>
<h2>Bedienung</h2>
<ul><li><strong>Füllen</strong> (■) und <strong>Kreuz</strong> (✕) wählst du über die Knöpfe unter dem Gitter. Kreuze markieren Felder, die sicher leer bleiben – sie sind beim Lösen genauso wichtig wie gefüllte Felder.</li>
<li>Mit gedrückter Maus oder gedrücktem Finger kannst du mehrere Felder in einem Zug markieren.</li>
<li>Ist eine Zeile oder Spalte vollständig, werden ihre Zahlen ausgegraut.</li>
<li><strong>Prüfen</strong> zeigt falsch markierte Felder, <strong>Tipp</strong> deckt ein Feld auf, das sich logisch ableiten lässt – und erklärt, warum.</li></ul>
<h2>Drei Größen</h2>
<p>Jeden Tag gibt es drei Nonogramme: 5×5 zum Kennenlernen, 10×10 als Tagesrätsel und 15×15 für längere Knobelpausen. Alle sind <strong>eindeutig und ohne Raten lösbar</strong>: Unser Programm löst jedes Rätsel vor der Veröffentlichung allein mit Zeile-für-Zeile-Logik. Lässt es sich so nicht vollständig lösen, wird es verworfen.</p>
<h2>Der wichtigste Trick: Überlappung</h2>
<p>Steht in einer Zeile mit zehn Feldern die Zahl 8, ist sie fast voll. Schiebe den Block gedanklich ganz nach links (Felder 1 bis 8) und ganz nach rechts (Felder 3 bis 10): Die Felder 3 bis 8 sind in beiden Fällen gefüllt – also sicher. Mit diesem Trick beginnt fast jedes Nonogramm. Mehr Techniken erklärt die <a href="/nonogramm-anleitung.html">Nonogramm-Anleitung</a>.</p>
"""
