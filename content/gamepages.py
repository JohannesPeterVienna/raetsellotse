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
<li><strong>Tipp</strong> markiert zuerst ein falsch ausgefülltes Feld. Ist alles richtig, sucht er einen Schritt mit den beiden Grundtechniken, trägt die Ziffer ein und erklärt, warum – etwa „In dieser Zeile kann die 7 nur noch hier stehen“. Bei <strong>leicht</strong> und <strong>mittel</strong> reicht das immer bis zum Ende. Bei <strong>schwer</strong> kann es vorkommen, dass keine Grundtechnik mehr greift; dann deckt der Tipp ein Feld auf, ohne es zu begründen. Fortgeschrittene Techniken wie Paare erklärt die Tipp-Funktion nicht.</li>
<li>Gleiche Ziffern werden hervorgehoben, Konflikte rot markiert.</li></ul>
<h2>Die drei Schwierigkeitsstufen</h2>
<p>Jedes Sudoku auf Rätsellotse hat <strong>genau eine Lösung</strong>. Das prüft unser Programm, bevor ein Rätsel erscheint. <strong>Leicht</strong> und <strong>mittel</strong> lassen sich allein mit den beiden Grundtechniken lösen: „einzige Möglichkeit im Feld“ und „einziger Platz für eine Ziffer“. Mittel hat dabei weniger Vorgaben. <strong>Schwer</strong> hat rund 25 Vorgaben; hier prüft das Programm nur, dass es genau eine Lösung gibt, und schreibt keine Techniken vor. Manche schweren Rätsel gehen trotzdem mit den Grundtechniken auf, andere verlangen Paare, die Wechselwirkung von Block und Zeile oder noch weitergehende Schritte.</p>
<h2>So kommst du weiter, wenn du feststeckst</h2>
<ol><li>Gehe die Ziffern der Reihe nach durch: Wo kann die 1 in jedem Block noch stehen? Dann die 2, und so weiter.</li>
<li>Schau auf fast volle Zeilen, Spalten und Blöcke – dort fehlen nur wenige Ziffern.</li>
<li>Trage Notizen ein und suche Paare: Zwei Felder mit denselben zwei Kandidaten blockieren diese Ziffern für den Rest der Einheit.</li></ol>
<p>Alle Techniken mit Beispielen erklären die <a href="/sudoku-strategien.html">Sudoku-Strategien</a>. Lieber auf Papier? Dann probier die <a href="/sudoku-zum-ausdrucken-mittel.html">Sudokus zum Ausdrucken</a> mit Lösungen.</p>
<h2>Häufige Fragen</h2>
<p><strong>Wird mein Fortschritt gespeichert?</strong> Ja, automatisch in deinem Browser. Du kannst das Sudoku schließen und später weitermachen – auf demselben Gerät.</p>
<p><strong>Muss man raten?</strong> Nein. Jedes Sudoku hat genau eine Lösung, die sich durch Schließen finden lässt. Leicht und mittel kommen mit einfachen Techniken aus; schwere Rätsel können fortgeschrittene Techniken bis hin zu Ketten verlangen. An solchen Stellen kann die Tipp-Funktion nur noch ein Feld aufdecken, aber nicht erklären – mehr dazu in <a href="/schweres-sudoku-erkennen.html">Woran man ein schweres Sudoku erkennt</a>.</p>
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

# Texte der Druckseiten (Sudoku zum Ausdrucken). Aussagen zu Vorgaben/Techniken wurden für die festen Druck-Seeds nachgeprüft.
PRINT_TEXT = {
"leicht": ("""<h2>Was dich bei „leicht“ erwartet</h2>
<p>Jedes der sechs Sudokus auf dieser Seite hat 38 vorgegebene Ziffern – fast die Hälfte des Gitters ist also schon ausgefüllt. Unser Programm hat beim Erstellen geprüft, dass jedes Rätsel genau eine Lösung hat und sich allein mit den beiden Grundtechniken lösen lässt. Bei diesen sechs Rätseln reicht sogar die einfachere der beiden: Jede Ziffer findest du, indem du in einem leeren Feld nachsiehst, welche Zahl dort als einzige noch passt.</p>
<h2>So löst du ein leichtes Sudoku</h2>
<ol><li><strong>Fast volle Einheiten zuerst:</strong> Suche eine Zeile, Spalte oder einen Block, in dem nur noch ein oder zwei Felder frei sind. Welche Ziffer fehlt, siehst du dort sofort.</li>
<li><strong>Ein Feld, drei Blicke:</strong> Für ein leeres Feld streichst du im Kopf alle Ziffern, die schon in seiner Zeile, seiner Spalte oder seinem 3×3-Block stehen. Bleibt genau eine übrig, trägst du sie ein. Diese Technik heißt „einzige Möglichkeit im Feld“ oder Naked Single.</li>
<li><strong>Jede neue Ziffer hilft weiter:</strong> Nach jedem Eintrag lohnt der Blick auf die Felder in derselben Zeile, Spalte und demselben Block – oft passt dort jetzt auch nur noch eine Ziffer.</li></ol>
<p>Notizen brauchst du bei dieser Stufe nicht. Raten musst du nie: Wenn du bei einem Feld zwischen zwei Ziffern schwankst, nimm dir einfach ein anderes Feld vor und komm später zurück. Wer die zweite Grundtechnik üben möchte, findet sie in den <a href='/sudoku-strategien.html'>Sudoku-Strategien</a> erklärt.</p>""",
"""<h2>Tipps zum Ausdrucken</h2>
<p>Der Knopf oben druckt nur die Rätsel und die Lösungen – Navigation, Werbung und diese Erklärungen werden beim Drucken ausgeblendet. Die Lösungen beginnen auf einer neuen Seite. Wer die Blätter in einer Gruppe austeilt, behält die Lösungsseite einfach zurück. Für Kinder oder Menschen, die größere Ziffern brauchen, lohnt es sich, das Blatt am Kopierer von A4 auf A3 zu vergrößern. Weitere Ideen für Rätselrunden stehen im Beitrag <a href='/raetsel-ausdrucken-seniorenrunde-schule.html'>Rätsel ausdrucken für Seniorenrunde, Schule und Wartezimmer</a>.</p>"""),
"mittel": ("""<h2>Was „mittel“ von „leicht“ unterscheidet</h2>
<p>Die sechs Rätsel hier haben je 30 Vorgaben, acht weniger als in der leichten Stufe. Auch sie sind so erstellt, dass es genau eine Lösung gibt und die beiden Grundtechniken bis zum Ende reichen. Der Unterschied liegt darin, welche der beiden du brauchst: Bei fünf der sechs Rätsel kommst du irgendwann mit der Frage „Welche Ziffer passt in dieses Feld?“ allein nicht weiter. Dann hilft die umgekehrte Frage: „Wo kann diese Ziffer in dieser Zeile, Spalte oder diesem Block noch hin?“</p>
<h2>Die Technik: einziger Platz für eine Ziffer</h2>
<p>Nimm dir eine Ziffer vor, etwa die 4, und einen Block, in dem sie noch fehlt. Zieh gedanklich – oder mit dem Bleistift ganz leicht – Linien durch alle Zeilen und Spalten, in denen bereits eine 4 steht. Bleibt im Block nur ein freies Feld übrig, gehört die 4 dorthin. Diese Technik heißt „einziger Platz für eine Ziffer“ oder Hidden Single. Sie funktioniert genauso für Zeilen und Spalten.</p>
<h2>Eine Reihenfolge, die sich bewährt</h2>
<ol><li>Gehe die Ziffern von 1 bis 9 der Reihe nach durch und prüfe für jede alle neun Blöcke.</li>
<li>Trage jede gefundene Ziffer sofort ein – sie kann den nächsten Platz freilegen.</li>
<li>Steckst du fest, wechsle zur Feld-Methode der leichten Stufe und suche Felder, in die nur noch eine Ziffer passt.</li></ol>
<p>Notizen sind nicht zwingend nötig, helfen aber, den Überblick zu behalten. Raten musst du auch hier nie.</p>""",
"""<h2>Tipps zum Ausdrucken</h2>
<p>„Drucken oder als PDF speichern“ öffnet den Druckdialog deines Browsers. In den meisten Browsern kannst du dort statt eines Druckers „Als PDF speichern“ wählen – praktisch, wenn du die Rätsel aufs Tablet laden oder später mehrmals drucken möchtest. Ausgedruckt werden nur Rätsel und Lösungen; die Lösungen beginnen auf einer eigenen Seite. Für die Hilfslinien der Kreuzschraffur eignet sich ein weicher Bleistift, dessen Striche du danach wieder wegradierst.</p>"""),
"schwer": ("""<h2>Was „schwer“ hier bedeutet</h2>
<p>Die Rätsel dieser Seite haben 25 Vorgaben, Rätsel 2 hat 27. Unser Programm garantiert bei der schweren Stufe nur eines: Jedes Sudoku hat genau eine Lösung. Welche Techniken man braucht, schreibt es nicht vor – deshalb schwankt die Schwierigkeit stärker als bei leicht und mittel. Wir haben die sechs Rätsel mit einem Löseprogramm nachgeprüft: Die Sudokus 3, 5 und 6 lassen sich mit den beiden Grundtechniken lösen und verlangen vor allem Ausdauer. Bei den Sudokus 1, 2 und 4 reichen weder die Grundtechniken noch Block-Zeile und Paare bis zum Ende; hier sind weitergehende Techniken gefragt. Am besten beginnst du mit 3, 5 oder 6.</p>
<h2>Mit Notizen arbeiten</h2>
<p>Bei wenigen Vorgaben findest du nach dem ersten Durchgang oft keine Ziffer mehr direkt. Dann trägst du in jedes leere Feld klein die Ziffern ein, die dort noch möglich sind – die Kandidaten – und streichst gezielt:</p>
<ul><li><strong>Block-Zeile (Pointing):</strong> Liegen alle Kandidaten einer Ziffer in einem Block in derselben Zeile, kann die Ziffer im Rest dieser Zeile gestrichen werden. Das gilt genauso für Spalten.</li>
<li><strong>Nacktes Paar:</strong> Haben zwei Felder einer Einheit genau dieselben zwei Kandidaten, gehören diese zwei Ziffern in diese zwei Felder. In den übrigen Feldern der Einheit fallen sie weg.</li>
<li><strong>Verstecktes Paar:</strong> Kommen zwei Ziffern in einer Einheit nur in denselben zwei Feldern vor, dürfen dort alle anderen Kandidaten gestrichen werden.</li></ul>
<p>Nach jeder Streichung lohnt der Blick zurück auf die Grundtechniken. Diagramme zu allen Techniken zeigen die <a href='/sudoku-strategien.html'>Sudoku-Strategien</a>.</p>""",
"""<h2>Tipps zum Ausdrucken</h2>
<p>Mit zwei Rätseln nebeneinander auf A4 werden die Felder ungefähr einen Zentimeter breit – für Kandidaten-Notizen ist das knapp. Wer viel notiert, druckt besser vergrößert, etwa mit einer höheren Skalierung im Druckdialog oder am Kopierer von A4 auf A3. Nimm einen spitzen, weichen Bleistift und schreib jeden Kandidaten immer an dieselbe Stelle im Feld: die 1 links oben, die 9 rechts unten. So erkennst du Paare auf einen Blick. Die Lösungen beginnen auf einer eigenen Seite; nach einem Fehler kannst du dort gezielt eine einzelne Ziffer nachschlagen.</p>"""),
}
