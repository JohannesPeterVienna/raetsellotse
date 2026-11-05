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
<h2>Ein Spiel Schritt für Schritt</h2>
<p>So kann ein vollständiges Spiel aussehen. Der gesuchte Code lautet 5 3 1 6 – das weiß man natürlich erst am Ende. Orange zählt die Ziffern an der richtigen Stelle, Weiß die richtigen Ziffern an der falschen Stelle.</p>
<ol><li><strong>Versuch 1: 1 2 3 4 – kein oranger, zwei weiße Punkte.</strong> Zwei der Ziffern 1 bis 4 kommen vor, aber keine an ihrer Stelle. Weil der Code vier verschiedene Ziffern aus sechs enthält und nur zwei davon aus 1 bis 4 stammen, müssen <strong>die 5 und die 6 beide</strong> im Code stecken. Außerdem steht die 1 nicht vorn, die 2 nicht an zweiter, die 3 nicht an dritter und die 4 nicht an vierter Stelle. Von den 360 möglichen Codes passen jetzt noch 84.</li>
<li><strong>Versuch 2: 3 5 6 1 – kein oranger, vier weiße Punkte.</strong> Dieser Versuch passt zu allem, was wir wissen: 5 und 6 sind dabei, 3 und 1 stehen an neuen Stellen. Das Ergebnis verrät alle vier Ziffern – 1, 3, 5 und 6 –, nur steht jede an der falschen Stelle.</li>
<li><strong>Nachdenken statt raten.</strong> Die 1 darf weder an Stelle 1 (Versuch 1) noch an Stelle 4 (Versuch 2) stehen, bleibt also an 2 oder 3. Die 3 darf nicht an 3 und nicht an 1 stehen, bleibt also an 2 oder 4. Die 5 darf nicht an 2, die 6 nicht an 3. Spielt man die Fälle durch, bleiben genau vier Codes übrig: 5 3 1 6, 5 6 1 3, 6 1 5 3 und 6 3 1 5.</li>
<li><strong>Versuch 3: 5 6 1 3 – zwei orange, zwei weiße Punkte.</strong> Gespielt wird einer der vier Kandidaten, denn er könnte schon die Lösung sein. Er ist es nicht, aber die Antwort reicht: Nur 5 3 1 6 ergibt gegen 5 6 1 3 genau zwei orange und zwei weiße Punkte. 6 1 5 3 und 6 3 1 5 hätten einen orangen und drei weiße geliefert.</li>
<li><strong>Versuch 4: 5 3 1 6 – vier orange Punkte.</strong> Geknackt.</li></ol>
<p>Das Muster lässt sich auf jeden Tag übertragen: ein breiter Start, ein Versuch, der die fehlenden Ziffern ins Spiel bringt, dann eine kurze Fallunterscheidung – am besten auf einem Zettel. Warum mit bestem Spiel jeder Code in höchstens fünf Versuchen fällt, steht in <a href="/codeknacker-mathematik.html">Wie viele Versuche braucht man beim Codeknacker?</a></p>
<h2>Gibt es Schwierigkeitsstufen?</h2>
<p>Nein. Die Regeln sind jeden Tag gleich: vier verschiedene Ziffern aus 1 bis 6, zehn Versuche. Unterschiedlich ist nur, wie viel der erste Versuch verrät. Zeigt 1 2 3 4 vier Punkte, kennst du sofort alle Ziffern und suchst nur noch die Reihenfolge. Zeigt er zwei Punkte, weißt du immerhin sicher, dass 5 und 6 dabei sind – wie im Beispiel oben. Wer sich fordern möchte, setzt sich ein eigenes Limit, etwa höchstens sechs Versuche, oder spielt einen Tag aus dem Archiv ohne Zettel nur im Kopf.</p>
<h2>Typische Fehler</h2>
<ul><li><strong>Punkte einzelnen Stellen zuordnen:</strong> Die Punkte stehen nach Farbe sortiert, zuerst Orange, dann Weiß. Der erste orange Punkt gehört also nicht zur ersten Ziffer.</li>
<li><strong>Nur auf den letzten Versuch schauen:</strong> Ein neuer Versuch muss zu allen bisherigen Zeilen passen. Wer vor dem Prüfen kurz jede frühere Zeile gegenrechnet, verschenkt keine Versuche.</li>
<li><strong>Zu viel auf einmal ändern:</strong> Tauschst du drei Ziffern gleichzeitig, weißt du hinterher nicht, welche Änderung die Punkte verschoben hat.</li>
<li><strong>Zu schnell abschicken:</strong> Ein geprüfter Versuch lässt sich nicht zurücknehmen. Vor dem Prüfen entfernt „Löschen“ die zuletzt getippte Ziffer.</li></ul>
<p>Codeknacker trainiert vor allem das Arbeitsgedächtnis und sauberes Schließen. Was solche Rätsel nachweislich bewirken – und was nicht –, fasst <a href="/denksport-und-gehirn.html">Denksport und Gehirn</a> zusammen. Wie man Kinder an das Spiel heranführt, steht in <a href="/logikraetsel-mit-kindern.html">Logikrätsel mit Kindern lösen</a>.</p>
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
<p>Alle Techniken mit Beispielen erklären die <a href="/sudoku-strategien.html">Sudoku-Strategien</a>. Hängst du bei einem Sudoku aus Zeitung oder Heft fest, erklärt dir der <a href="/sudoku-loeser.html">Sudoku-Löser mit Lösungsweg</a> den nächsten Schritt. Lieber auf Papier? Dann probier die <a href="/sudoku-zum-ausdrucken-mittel.html">Sudokus zum Ausdrucken</a> mit Lösungen.</p>
<h2>Ein Beispiel Schritt für Schritt (4 × 4)</h2>
<p>Die beiden Grundtechniken lassen sich am kleinen Mini-Sudoku am besten zeigen. Hier stehen die Ziffern 1 bis 4 in einem 4×4-Gitter mit vier 2×2-Blöcken; jede Ziffer kommt in jeder Zeile, Spalte und jedem Block genau einmal vor. Vorgegeben sind nur vier Ziffern: Zeile 1 beginnt mit 1 und endet mit 4, in Zeile 4 stehen an zweiter und dritter Stelle die 3 und die 2. Das Rätsel hat genau eine Lösung; das haben wir mit einem Programm geprüft.</p>
<table class="tbl" aria-label="Mini-Sudoku 4 × 4, Ausgangslage"><tbody><tr><td>1</td><td></td><td></td><td>4</td></tr><tr><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td></tr><tr><td></td><td>3</td><td>2</td><td></td></tr></tbody></table>
<ol><li><strong>Zeile 1:</strong> Es fehlen 2 und 3. In Spalte 3 steht unten schon die 2, also kommt in Zeile 1, Spalte 3 die 3 – und daneben in Spalte 2 die 2. Das ist die Technik „einzige Möglichkeit im Feld“.</li>
<li><strong>Zeile 4:</strong> Es fehlen 1 und 4. Spalte 1 enthält oben schon die 1, also steht in Zeile 4, Spalte 1 die 4 und in Spalte 4 die 1.</li>
<li><strong>Wohin gehört die 3 in Spalte 1?</strong> Frei sind nur noch Zeile 2 und Zeile 3. Zeile 3 liegt im Block unten links, und dort steht bereits die 3. Also bleibt für die 3 nur Zeile 2. Das ist die zweite Technik, „einziger Platz für eine Ziffer“.</li>
<li><strong>Spalte 1 vervollständigen:</strong> 1, 3 und 4 sind eingetragen; in Zeile 3 fehlt die 2.</li>
<li><strong>Blöcke links:</strong> Im Block oben links fehlt nur noch die 4 (Zeile 2, Spalte 2), im Block unten links nur die 1 (Zeile 3, Spalte 2).</li>
<li><strong>Zeile 2:</strong> Es fehlen 1 und 2. Spalte 3 enthält schon die 2, also steht dort die 1, in Spalte 4 die 2.</li>
<li><strong>Zeile 3:</strong> Es fehlen 3 und 4. Spalte 4 enthält oben die 4, also kommt dort die 3 hin, in Spalte 3 die 4.</li></ol>
<p>Die Lösung lautet zeilenweise 1 2 3 4 · 3 4 1 2 · 2 1 4 3 · 4 3 2 1. Beim 9×9-Sudoku sind die Schritte genau dieselben, es gibt nur mehr davon. Bei leicht und mittel kommst du mit diesen beiden Fragen bis zum Ende: „Welche Ziffer passt in dieses Feld?“ und „Wo kann diese Ziffer in dieser Zeile, Spalte oder diesem Block noch stehen?“</p>
<h2>Typische Fehler</h2>
<ul><li><strong>Rot heißt nicht „falsch“, kein Rot heißt nicht „richtig“:</strong> Die rote Markierung zeigt nur, dass dieselbe Ziffer schon in Zeile, Spalte oder Block steht. Eine Ziffer kann falsch sein, ohne sofort einen Konflikt zu erzeugen. Der Tipp-Knopf meldet solche Felder zuerst.</li>
<li><strong>Aus dem Bauch eintragen:</strong> Eine geratene Ziffer fällt oft erst zehn Schritte später auf, und dann ist schwer zu sagen, wo der Fehler begann. Trage nur ein, was du begründen kannst; bei Zweifeln hilft eine Notiz.</li>
<li><strong>Nur nach Feldern suchen:</strong> Wer immer nur fragt, was in ein Feld passt, übersieht den „einzigen Platz“ – gerade bei mittel ist das oft der einzige Weg weiter.</li>
<li><strong>Notizen auf Papier nicht nachführen:</strong> Online verschwindet eine eingetragene Ziffer automatisch aus den Notizen in derselben Zeile, Spalte und demselben Block. Auf einem Ausdruck musst du sie selbst streichen.</li></ul>
<p>Wie man einem Sudoku seine Schwierigkeit ansieht, erklärt <a href="/schweres-sudoku-erkennen.html">Woran man ein schweres Sudoku erkennt</a>; Herkunft und Zahlen rund um das Rätsel stehen in <a href="/sudoku-regeln-und-geschichte.html">Sudoku: Regeln, Herkunft und erstaunliche Zahlen</a>.</p>
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
<h2>Ein Beispiel Schritt für Schritt</h2>
<p>Angenommen, die Zahlen des Tages sind <strong>100, 50, 9, 7, 4 und 2</strong>, und die Zielzahl lautet <strong>863</strong>.</p>
<ol><li><strong>Größenordnung finden:</strong> 863 liegt knapp unter 900, und 9 × 100 = 900 ist schnell gerechnet. Von dort fehlen 37 nach unten.</li>
<li><strong>Den Rest bauen:</strong> Die 37 muss aus 50, 7, 4 und 2 entstehen. 7 + 4 + 2 = 13, und 50 − 13 = 37. Zusammen: 9 × 100 − (50 − (7 + 4 + 2)) = 900 − 37 = 863. Jede Zahl ist genau einmal verwendet, alle Zwischenergebnisse (13, 37, 900) sind positiv – die Rechnung gilt.</li>
<li><strong>Einen kürzeren Weg suchen:</strong> 863 lässt sich auch zerlegen: 863 = 800 + 63. Die 800 ist 8 × 100, und die 8 entsteht aus 4 × 2. Die 63 ist 7 × 9. Ins Feld getippt: <code>4 × 2 × 100 + 7 × 9</code>. Die 50 bleibt übrig, und das ist erlaubt.</li></ol>
<p>Der Trick „Zielzahl durch eine kleine Zahl teilen“ aus der Strategie oben hilft hier übrigens nicht: 863 ist eine Primzahl und lässt sich durch keine der kleinen Zahlen teilen. Dann führen Anpeilen und Zerlegen in eine runde Zahl plus Rest zum Ziel.</p>
<h2>Wie schwer ist eine Aufgabe?</h2>
<p>Feste Stufen gibt es bei der Zielzahl nicht. Jeden Tag kommen zwei große Zahlen aus 25, 50, 75 und 100 und vier kleine aus 1 bis 10 dazu; eine kleine Zahl kann auch doppelt vorkommen, etwa zweimal die 5. Die Zielzahl liegt zwischen 101 und 999. Leicht wird eine Aufgabe, wenn die Zielzahl nahe an einem Vielfachen der großen Zahlen liegt oder sich glatt teilen lässt. Schwerer sind Zielzahlen weit weg von runden Werten, Primzahlen wie 863 und Tage mit vielen kleinen, gleichen Zahlen.</p>
<h2>Typische Fehler</h2>
<ul><li><strong>Punkt vor Strich vergessen:</strong> 100 + 6 × 4 ergibt 124, nicht 424. Wer zuerst addieren will, setzt Klammern: (100 + 6) × 4.</li>
<li><strong>Negative Zwischenschritte:</strong> 2 − 7 + 100 wird abgelehnt, weil zwischendurch −5 entsteht. Stelle die Rechnung um: 100 + 2 − 7.</li>
<li><strong>Teilen mit Rest:</strong> 50 ÷ 4 geht nicht auf und ist deshalb nicht erlaubt. Prüfe vor dem Teilen, ob das Ergebnis eine ganze Zahl ist.</li>
<li><strong>Eine Zahl zu oft verwenden:</strong> Steht die 7 nur einmal da, darf sie auch nur einmal vorkommen. Das Spiel meldet dann, welche Zahl nicht oft genug zur Verfügung steht.</li>
<li><strong>Zu früh aufgeben:</strong> Auch ein Ergebnis knapp daneben ist ein guter Ausgangspunkt. Das beste bisherige Ergebnis wird angezeigt; oft fehlt nur ein Tausch von zwei kleinen Zahlen.</li></ul>
<p>Warum sich regelmäßiges Kopfrechnen lohnt und welche Wirkungen von Denksport belegt sind, steht in <a href="/denksport-und-gehirn.html">Denksport und Gehirn</a>.</p>
<h2>Häufige Fragen</h2>
<p><strong>Gibt es nur eine richtige Rechnung?</strong> Nein. Meist führen mehrere Wege zur Zielzahl, wie das Beispiel oben zeigt. Jede Rechnung zählt, die die Regeln einhält und genau die Zielzahl ergibt.</p>
<p><strong>Warum ist die gezeigte Lösung manchmal umständlich?</strong> „Lösung zeigen“ durchsucht die Möglichkeiten der Reihe nach und zeigt den ersten Weg, den das Programm findet – nicht unbedingt den kürzesten. Es lohnt sich, danach selbst eine elegantere Rechnung zu suchen.</p>
<p><strong>Zählt der Tag für meine Serie, wenn ich die Lösung angesehen habe?</strong> Nein. Die Serie wächst nur, wenn du die Zielzahl am selben Tag selbst triffst, ohne vorher die Lösung anzeigen zu lassen.</p>
<p><strong>Sind Brüche oder Kommazahlen erlaubt?</strong> Nein. Es wird nur mit ganzen Zahlen gerechnet: Das Eingabefeld nimmt Ziffern, die vier Rechenzeichen und Klammern an, und jede Division muss ohne Rest aufgehen. Auch Hochzahlen oder Wurzeln gibt es nicht.</p>
<p><strong>Kann ich frühere Aufgaben nachrechnen?</strong> Ja, über das Datumsfeld oben im Spiel oder deine <a href="/archiv.html">Statistik</a>. Nachgespielte Tage zählen nicht für die Serie.</p>
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
<h2>Ein Beispiel Schritt für Schritt (5 × 5)</h2>
<p>Ein kleines Nonogramm mit fünf Zeilen und fünf Spalten. Die Zeilenhinweise lauten von oben nach unten <strong>1 1 · 5 · 5 · 3 · 1</strong>, die Spaltenhinweise von links nach rechts <strong>2 · 4 · 4 · 4 · 2</strong>. Unser Löseprogramm schafft es allein mit Zeile-für-Zeile-Logik; es hat also genau eine Lösung.</p>
<ol><li><strong>Volle Zeilen:</strong> Zeile 2 und Zeile 3 haben den Hinweis 5 – bei fünf Feldern sind sie komplett gefüllt.</li>
<li><strong>Überlappung in den Spalten 2 bis 4:</strong> Ein Viererblock in fünf Feldern liegt entweder in den Feldern 1 bis 4 oder 2 bis 5. In beiden Lagen sind die Felder 2, 3 und 4 gefüllt. Also sind in diesen drei Spalten die Zeilen 2 bis 4 sicher gefüllt.</li>
<li><strong>Zeile 4 (Hinweis 3):</strong> Die Felder in den Spalten 2, 3 und 4 sind schon gefüllt – das ist der ganze Dreierblock. Die Felder ganz links und ganz rechts bekommen ein Kreuz.</li>
<li><strong>Spalten 1 und 5 (Hinweis 2):</strong> Die Zeilen 2 und 3 sind gefüllt, der Zweierblock ist komplett. Zeile 1, 4 und 5 bleiben in diesen Spalten leer.</li>
<li><strong>Zeile 1 (Hinweis 1 1):</strong> Die Ecken sind leer, es bleiben die Felder in den Spalten 2, 3 und 4. Zwei Einzelfelder mit einer Lücke passen dort nur in die Spalten 2 und 4; Spalte 3 bleibt leer.</li>
<li><strong>Spalten 2 und 4 (Hinweis 4):</strong> Jetzt sind die Zeilen 1 bis 4 gefüllt – der Block ist vollständig, Zeile 5 bleibt leer.</li>
<li><strong>Zeile 5 (Hinweis 1):</strong> Übrig ist nur noch die Mitte. Damit hat auch Spalte 3 ihre vier gefüllten Felder in den Zeilen 2 bis 5. Fertig – das Bild ist ein Herz.</li></ol>
<p>Größere Rätsel funktionieren genauso, nur greifen die Schritte öfter ineinander: Ein Kreuz in einer Spalte macht eine Zeile lösbar, die wiederum zwei Spalten weiterhilft.</p>
<h2>Typische Fehler</h2>
<ul><li><strong>Die Reihenfolge der Blöcke ignorieren:</strong> „1 3“ ist nicht dasselbe wie „3 1“. Der Einzelblock kommt zuerst, von links beziehungsweise von oben gelesen.</li>
<li><strong>Keine Kreuze setzen:</strong> Wer nur füllt, verliert den Überblick, welche Felder schon geklärt sind. Kreuze sind halbe Arbeit, die man nicht zweimal machen will.</li>
<li><strong>Ausgegraute Zahlen für einen Beweis halten:</strong> Die Zahlen werden grau, sobald die gefüllten Felder einer Zeile zum Hinweis passen. Das heißt noch nicht, dass sie an der richtigen Stelle liegen – die Spalten müssen ebenfalls aufgehen.</li>
<li><strong>Falsch zählen:</strong> Bei 10 × 10 und 15 × 15 sind alle fünf Felder dickere Linien gezogen. Zähle in Fünfergruppen statt Feld für Feld.</li>
<li><strong>Raten, wenn es hakt:</strong> Jedes Tagesrätsel ist ohne Raten lösbar. Steckst du fest, such die Zeile oder Spalte mit dem geringsten Spielraum, oder lass dir mit „Tipp“ ein ableitbares Feld samt Begründung zeigen.</li></ul>
<p>Für den Einstieg mit Kindern eignet sich 5 × 5 besonders gut; Ideen dazu stehen in <a href="/logikraetsel-mit-kindern.html">Logikrätsel mit Kindern lösen</a>. Wer lieber auf Papier knobelt, findet Tipps für Rätselrunden im Beitrag <a href="/raetsel-ausdrucken-seniorenrunde-schule.html">Rätsel ausdrucken für Seniorenrunde, Schule und Wartezimmer</a>.</p>
<h2>Häufige Fragen</h2>
<p><strong>Was zeigt das fertige Bild?</strong> Unsere Nonogramme werden von einem Programm erzeugt. Die Bilder sind deshalb abstrakte, zusammenhängende Formen und keine gezeichneten Motive wie das Herz im Beispiel.</p>
<p><strong>Welche Größe zählt für die Serie?</strong> Jedes am selben Tag gelöste Nonogramm zählt, egal ob 5 × 5, 10 × 10 oder 15 × 15. In der Tabelle der letzten 30 Tage in deiner <a href="/archiv.html">Statistik</a> steht jeweils das 10×10-Rätsel.</p>
<p><strong>Was passiert bei „Neu beginnen“?</strong> Alle Markierungen des aktuellen Rätsels werden gelöscht, und du startest mit einem leeren Gitter. Die Zahl der bereits genutzten Tipps bleibt dabei gespeichert. Ein gelöstes Rätsel lässt sich nicht mehr zurücksetzen.</p>
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
