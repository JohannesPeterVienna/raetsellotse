"""Anleitungen, Strategie- und Hintergrundartikel für Rätsellotse.

Jeder Eintrag in ARTICLES ist ein Dict mit slug, title, teaser, description (max. 160 Zeichen) und body (HTML).
Optional: published / modified (ISO-Datum) und related (Liste von Slugs für „Weiterlesen“).
Die Diagramme werden mit den Hilfsfunktionen unten als Inline-SVG erzeugt; Farben kommen aus style.css (.dg …),
damit sie im hellen und dunklen Modus funktionieren. Alle Beispiele (Sudoku-Ausschnitte, Codeknacker-Partie,
Nonogramme, Rechenwege) wurden beim Schreiben mit einem kleinen Skript nachgeprüft.
"""

# ---------------------------------------------------------------- Diagramm-Helfer

def _svg(w, h, inner, label):
    return (f'<svg class="dg" viewBox="0 0 {w} {h}" role="img" aria-label="{label}" '
            f'xmlns="http://www.w3.org/2000/svg">{inner}</svg>')


def _grid(R, C, ox=1, oy=1, s=34, box=3, givens=None, cands=None, strike=None, hl=(), hl2=(), target=None, lines=()):
    """Sudoku-Gitter (oder Ausschnitt). Zellen 1-basiert als (zeile, spalte)."""
    givens, cands, strike = givens or {}, cands or {}, strike or {}
    o = [f'<rect class="bg" x="{ox}" y="{oy}" width="{C*s}" height="{R*s}"/>']
    for cls, cells in (("h1", hl), ("h2", hl2)):
        for r, c in dict.fromkeys(cells):
            o.append(f'<rect class="{cls}" x="{ox+(c-1)*s}" y="{oy+(r-1)*s}" width="{s}" height="{s}"/>')
    for i in range(1, C):
        o.append(f'<line class="tl" x1="{ox+i*s}" y1="{oy}" x2="{ox+i*s}" y2="{oy+R*s}"/>')
    for j in range(1, R):
        o.append(f'<line class="tl" x1="{ox}" y1="{oy+j*s}" x2="{ox+C*s}" y2="{oy+j*s}"/>')
    for i in range(box, C, box):
        o.append(f'<line class="tk" x1="{ox+i*s}" y1="{oy}" x2="{ox+i*s}" y2="{oy+R*s}"/>')
    for j in range(box, R, box):
        o.append(f'<line class="tk" x1="{ox}" y1="{oy+j*s}" x2="{ox+C*s}" y2="{oy+j*s}"/>')
    o.append(f'<rect class="tk" x="{ox}" y="{oy}" width="{C*s}" height="{R*s}"/>')

    def ctr(r, c):
        return ox + (c - 0.5) * s, oy + (r - 0.5) * s
    for a, b in lines:
        (x1, y1), (x2, y2) = ctr(*a), ctr(*b)
        o.append(f'<line class="xw" x1="{x1:g}" y1="{y1:g}" x2="{x2:g}" y2="{y2:g}"/>')
    for (r, c), d in givens.items():
        x, y = ctr(r, c)
        o.append(f'<text class="gv" x="{x:g}" y="{y+7:g}" text-anchor="middle">{d}</text>')
    if target:
        x, y = ctr(target[0], target[1])
        o.append(f'<text class="tg" x="{x:g}" y="{y+7:g}" text-anchor="middle">{target[2]}</text>')

    def mini(r, c, d):
        return ox + (c - 1) * s + ((d - 1) % 3 + 0.5) * s / 3, oy + (r - 1) * s + ((d - 1) // 3 + 0.5) * s / 3
    for (r, c), ds in cands.items():
        for d in ds:
            x, y = mini(r, c, d)
            o.append(f'<text class="cd" x="{x:g}" y="{y+3.5:g}" text-anchor="middle">{d}</text>')
    for (r, c), ds in strike.items():
        for d in ds:
            x, y = mini(r, c, d)
            o.append(f'<text class="cs" x="{x:g}" y="{y+3.5:g}" text-anchor="middle">{d}</text>'
                     f'<line class="sl" x1="{x-5:g}" y1="{y+4:g}" x2="{x+5:g}" y2="{y-4:g}"/>')
    return "".join(o)


def _sudoku(label, **kw):
    return _svg(308, 308, _grid(9, 9, **kw), label)


def _nono_g(rc, cc, rows, ox=0, oy=0, s=26):
    """Nonogramm-Gitter. Zeichen: '#' gefüllt, '@' neu gefüllt, 'x' Kreuz, '+' neues Kreuz, '.' offen."""
    n, m = len(rows), len(rows[0])
    cw = 13 * max(len(c) for c in rc) + 8
    ch = 14 * max(len(c) for c in cc) + 6
    gx, gy = ox + cw, oy + ch
    o = [f'<rect class="bg" x="{gx}" y="{gy}" width="{m*s}" height="{n*s}"/>']
    for x, clue in enumerate(cc):
        for i, v in enumerate(clue):
            o.append(f'<text class="cl" x="{gx+x*s+s/2:g}" y="{gy-6-(len(clue)-1-i)*14}" text-anchor="middle">{v}</text>')
    for y, clue in enumerate(rc):
        for i, v in enumerate(clue):
            o.append(f'<text class="cl" x="{gx-6-(len(clue)-1-i)*13}" y="{gy+y*s+s/2+4:g}" text-anchor="end">{v}</text>')
    for y, row in enumerate(rows):
        for x, ch_ in enumerate(row):
            X, Y = gx + x * s, gy + y * s
            if ch_ in "#@":
                o.append(f'<rect class="{"f1" if ch_ == "#" else "f2"}" x="{X+2}" y="{Y+2}" width="{s-4}" height="{s-4}" rx="2"/>')
            elif ch_ in "x+":
                k = "x1" if ch_ == "x" else "x2"
                o.append(f'<line class="{k}" x1="{X+8}" y1="{Y+8}" x2="{X+s-8}" y2="{Y+s-8}"/>'
                         f'<line class="{k}" x1="{X+s-8}" y1="{Y+8}" x2="{X+8}" y2="{Y+s-8}"/>')
    for i in range(1, m):
        o.append(f'<line class="{"tk" if i % 5 == 0 else "tl"}" x1="{gx+i*s}" y1="{gy}" x2="{gx+i*s}" y2="{gy+n*s}"/>')
    for j in range(1, n):
        o.append(f'<line class="{"tk" if j % 5 == 0 else "tl"}" x1="{gx}" y1="{gy+j*s}" x2="{gx+m*s}" y2="{gy+j*s}"/>')
    o.append(f'<rect class="tk" x="{gx}" y="{gy}" width="{m*s}" height="{n*s}"/>')
    return "".join(o), cw + m * s + 2, ch + n * s + 2


def _nono_panels(label, rc, cc, panels, cols=2, s=24):
    """Mehrere Zustände eines Nonogramms mit Überschrift, in Spalten angeordnet."""
    _, w, h = _nono_g(rc, cc, panels[0][1], s=s)
    gap, head = 24, 22
    out = []
    for k, (title, rows) in enumerate(panels):
        ox, oy = (k % cols) * (w + gap), (k // cols) * (h + head + gap)
        g, _, _ = _nono_g(rc, cc, rows, ox, oy + head, s)
        out.append(f'<text class="lb" x="{ox}" y="{oy+14}">{title}</text>' + g)
    nrows = (len(panels) + cols - 1) // cols
    return _svg(cols * w + (cols - 1) * gap, nrows * (h + head) + (nrows - 1) * gap, "".join(out), label)


def _line_steps(label, clue, steps, s=26):
    """Eine Nonogramm-Zeile in mehreren Schritten untereinander."""
    out, y = [], 0
    for title, row in steps:
        g, w, h = _nono_g([clue], [[""]] * len(row), [row], 0, y + 14, s)
        out.append(f'<text class="lb" x="0" y="{y+14}">{title}</text>' + g)
        y += h + 20
    return _svg(w, y - 6, "".join(out), label)


# ---------------------------------------------------------------- Diagramme

FIG_NAKED_SINGLE = _sudoku(
    "Sudoku-Ausschnitt: Im markierten Feld in Zeile 5, Spalte 5 ist nur noch die 6 möglich",
    givens={(5, 1): 1, (5, 3): 3, (5, 8): 7, (1, 5): 2, (3, 5): 8, (8, 5): 4, (4, 4): 5, (6, 6): 9},
    hl=[(5, c) for c in range(1, 10)] + [(r, 5) for r in range(1, 10)] + [(r, c) for r in (4, 5, 6) for c in (4, 5, 6)],
    hl2=[(5, 5)], target=(5, 5, 6))

FIG_HIDDEN_SINGLE = _sudoku(
    "Sudoku-Ausschnitt: Im linken oberen Block passt die 7 nur noch in Zeile 3, Spalte 3",
    givens={(1, 6): 7, (2, 8): 7, (6, 1): 7, (3, 2): 4},
    hl2=[(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1)], hl=[(3, 3)], target=(3, 3, 7),
    lines=[((1, 6), (1, 1)), ((2, 8), (2, 1)), ((6, 1), (1, 1))])

FIG_POINTING = _sudoku(
    "Sudoku-Ausschnitt: Die 5 des linken oberen Blocks liegt sicher in Zeile 2 und kann im Rest der Zeile gestrichen werden",
    givens={(1, 1): 3, (1, 2): 9, (1, 3): 7, (3, 1): 6, (3, 2): 1, (3, 3): 2, (2, 2): 4},
    cands={(2, 1): [5], (2, 3): [5], (6, 5): [5], (8, 8): [5]},
    strike={(2, 5): [5], (2, 8): [5]}, hl=[(2, 1), (2, 3)], hl2=[(2, 5), (2, 8)])

FIG_PAIR = _svg(308, 124,
    '<text class="lb" x="1" y="14">Vorher</text>' +
    _grid(1, 9, oy=20, givens={(1, 2): 1, (1, 5): 5, (1, 9): 9}, hl=[(1, 3), (1, 6)],
          cands={(1, 1): [2, 3, 8], (1, 3): [3, 8], (1, 4): [2, 4, 6], (1, 6): [3, 8], (1, 7): [3, 4, 6, 7], (1, 8): [2, 7, 8]}) +
    '<text class="lb" x="1" y="82">Nachher</text>' +
    _grid(1, 9, oy=88, givens={(1, 2): 1, (1, 5): 5, (1, 9): 9}, hl=[(1, 3), (1, 6)],
          cands={(1, 1): [2], (1, 3): [3, 8], (1, 4): [2, 4, 6], (1, 6): [3, 8], (1, 7): [4, 6, 7], (1, 8): [2, 7]},
          strike={(1, 1): [3, 8], (1, 7): [3], (1, 8): [8]}),
    "Eine Sudoku-Zeile vor und nach dem Streichen eines nackten Paares 3 und 8")

FIG_XWING = _sudoku(
    "X-Wing für die Ziffer 4 in den Zeilen 2 und 7 und den Spalten 3 und 8",
    cands={(2, 3): [4], (2, 8): [4], (7, 3): [4], (7, 8): [4], (4, 5): [4], (5, 1): [4], (9, 6): [4]},
    strike={(4, 3): [4], (9, 3): [4], (5, 8): [4]},
    hl=[(2, 3), (2, 8), (7, 3), (7, 8)], hl2=[(4, 3), (9, 3), (5, 8)],
    lines=[((2, 3), (2, 8)), ((2, 8), (7, 8)), ((7, 8), (7, 3)), ((7, 3), (2, 3))])

FIG_NONO_LINE = _line_steps(
    "Eine Nonogramm-Zeile mit dem Hinweis 3 2 wird in vier Schritten gelöst", [3, 2],
    [("1 · Ausgangslage: Feld 3 ist ein Kreuz", "..x......."),
     ("2 · Lücke vor dem Kreuz ist zu klein", "++x......."),
     ("3 · Überlappung in den Feldern 4 bis 10", "xxx.@@..@."),
     ("4 · Feld 8 kommt aus der Spalte dazu", "xxx@##+##+")])

_H_RC, _H_CC = [[1, 1], [5], [5], [3], [1]], [[2], [4], [4], [4], [2]]
FIG_NONO_HEART = _nono_panels(
    "Ein 5-mal-5-Nonogramm in vier Durchgängen gelöst – es entsteht ein Herz", _H_RC, _H_CC,
    [("A · Zeilen", [".....", "@@@@@", "@@@@@", "..@..", "....."]),
     ("B · Spalten", ["+...+", "#####", "#####", "+@#@+", "+...+"]),
     ("C · Zeilen", ["x@+@x", "#####", "#####", "x###x", "x...x"]),
     ("D · Spalten", ["x#x#x", "#####", "#####", "x###x", "x+@+x"])])

_K_RC, _K_CC = [[1], [3], [5], [1, 1], [1, 1]], [[1], [4], [3], [4], [1]]
FIG_KIDS_NONO = _nono_panels(
    "Kinder-Nonogramm 5 mal 5 zum Lösen, daneben die Lösung: ein Haus", _K_RC, _K_CC,
    [("Zum Lösen", ["....."] * 5),
     ("Lösung", ["..#..", ".###.", "#####", ".#.#.", ".#.#."])], s=30)

FIG_KIDS_SUDOKU = _svg(
    316, 160,
    '<text class="lb" x="1" y="14">Mini-Sudoku 1</text>' +
    _grid(4, 4, oy=20, box=2, givens={(1, 1): 1, (1, 3): 3, (2, 2): 4, (2, 4): 2, (3, 1): 2, (3, 3): 4, (4, 2): 3, (4, 4): 1}) +
    '<text class="lb" x="171" y="14">Mini-Sudoku 2</text>' +
    _grid(4, 4, ox=171, oy=20, box=2, givens={(1, 2): 4, (2, 1): 1, (2, 4): 4, (3, 1): 4, (3, 4): 2, (4, 2): 2}),
    "Zwei Mini-Sudokus mit 4 mal 4 Feldern für Kinder")


def _src(items):
    return '<ol class="src">' + "".join(f"<li>{i}</li>" for i in items) + "</ol>"


# ---------------------------------------------------------------- Artikel

ARTICLES = [
{
"slug": "codeknacker-anleitung",
"title": "Codeknacker: Regeln und Strategie",
"teaser": "Was die Punkte bedeuten, eine Strategie in vier Schritten und eine Partie, bei der jeder Zug begründet ist.",
"description": "Codeknacker lernen: was orange und weiße Punkte verraten, eine Strategie in vier Schritten und eine komplett durchgerechnete Beispielpartie.",
"published": "2026-10-29", "modified": "2026-10-31",
"related": ["codeknacker-mathematik", "wie-unsere-raetsel-entstehen", "logikraetsel-mit-kindern"],
"body": """
<p>Gesucht ist ein Code aus vier <strong>verschiedenen</strong> Ziffern von 1 bis 6. Du hast zehn Versuche. Nach jedem Versuch bekommst du Hinweise – aber nicht, zu welcher Ziffer sie gehören. Hier findest du die Regeln, eine Strategie, die mit etwas Kopfarbeit und ohne Notizblock auskommt, und eine vollständige Beispielpartie, in der jeder Zug begründet ist.</p>
<h2>Die Hinweise</h2>
<ul><li><strong>Oranger Punkt:</strong> Eine deiner Ziffern ist richtig und steht an der richtigen Stelle.</li>
<li><strong>Weißer Punkt mit orangem Rand:</strong> Eine Ziffer kommt im Code vor, steht aber an einer anderen Stelle.</li>
<li><strong>Grauer Punkt:</strong> Eine Ziffer kommt nicht vor.</li></ul>
<p>Die Reihenfolge der Punkte verrät nicht, zu welcher Ziffer sie gehören. Weil sich im Code keine Ziffer wiederholt, gilt aber eine einfache Rechnung: <strong>Orange plus Weiß</strong> ergibt die Zahl der Ziffern, die dein Versuch mit dem Code gemeinsam hat.</p>
<div class="example"><strong>Gut zu wissen:</strong> Zwei Codes aus vier von sechs Ziffern haben immer mindestens zwei Ziffern gemeinsam – es fehlen ja nur zwei der sechs. Mehr als zwei graue Punkte siehst du deshalb nie. Und drei orange plus ein weißer Punkt sind unmöglich: Stehen drei Ziffern richtig und die vierte kommt im Code vor, bleibt für sie nur der letzte freie Platz – dann wäre sie ebenfalls orange.</div>
<h2>Eine Strategie in vier Schritten</h2>
<ol><li><strong>Ziffern zählen:</strong> Starte mit 1 2 3 4. Die Summe aus orangen und weißen Punkten sagt dir, wie viele dieser vier Ziffern im Code stecken. Bei zwei Punkten sind 5 und 6 sicher dabei, bei drei Punkten genau eine von beiden, bei vier Punkten keine.</li>
<li><strong>Gezielt austauschen:</strong> Kombiniere im nächsten Versuch die sicheren Ziffern mit der Hälfte der unsicheren. Ändert sich die Punktzahl, weißt du, welche Hälfte zählt.</li>
<li><strong>Stellen mitdenken:</strong> Jeder Versuch ohne orangen Punkt sagt dir viel: Keine der getippten Ziffern steht an der Stelle, an der du sie probiert hast. Wer das im Kopf (oder auf einem Zettel als kleine Tabelle Ziffer × Stelle) festhält, spart später Versuche.</li>
<li><strong>Nur mögliche Codes spielen:</strong> Wähle Versuche, die zu allen bisherigen Hinweisen passen. Dann kann jeder Versuch selbst schon die Lösung sein.</li></ol>
<h2>Eine Partie Schritt für Schritt</h2>
<p>Der gesuchte Code in diesem Beispiel lautet 4 6 1 5. Beim Spielen weiß man das natürlich nicht – wir zeigen nach jedem Versuch, was sich aus den Punkten schließen lässt. Wie viele Codes jeweils noch in Frage kommen, haben wir mit einem kleinen Programm nachgezählt.</p>
<div class="scroll"><table class="tbl"><thead><tr><th scope="col">Versuch</th><th scope="col">Tipp</th><th scope="col">Orange</th><th scope="col">Weiß</th><th scope="col">Noch möglich</th></tr></thead>
<tbody><tr><td>1</td><td>1 2 3 4</td><td>0</td><td>2</td><td>84 von 360</td></tr>
<tr><td>2</td><td>2 1 5 6</td><td>0</td><td>3</td><td>24</td></tr>
<tr><td>3</td><td>5 3 6 1</td><td>0</td><td>3</td><td>4</td></tr>
<tr><td>4</td><td>4 6 1 5</td><td>4</td><td>0</td><td>geknackt</td></tr></tbody></table></div>
<h3>Versuch 1: 1 2 3 4 – zwei weiße Punkte</h3>
<p>Genau zwei der Ziffern 1 bis 4 sind im Code. Weil der Code vier Ziffern hat, müssen 5 und 6 beide dabei sein. Und weil kein Punkt orange ist, steht keine getestete Ziffer an ihrer Stelle: Die 1 ist nicht vorne, die 2 nicht an zweiter, die 3 nicht an dritter und die 4 nicht an vierter Stelle.</p>
<h3>Versuch 2: 2 1 5 6 – drei weiße Punkte</h3>
<p>Die sicheren Ziffern 5 und 6 liefern zwei der drei Punkte. Von 1 und 2 ist also genau eine dabei – und folglich von 3 und 4 ebenfalls genau eine. Wieder kein Orange: Die 2 steht nicht vorne, die 1 nicht an zweiter Stelle, die 5 nicht an dritter, die 6 nicht an vierter. Dieser Versuch passte übrigens zu allem, was nach Versuch 1 bekannt war – er hätte selbst die Lösung sein können.</p>
<h3>Versuch 3: 5 3 6 1 – drei weiße Punkte</h3>
<p>Zwei Punkte kommen wieder von 5 und 6, also ist von 3 und 1 genau eine im Code. Jetzt hilft ein kurzer Fallvergleich:</p>
<ul><li><strong>Die 1 ist dabei.</strong> Dann fehlt die 2 (wegen Versuch 2) und die 3 (wegen Versuch 3), also ist die 4 dabei. Ziffern: 1, 4, 5, 6.</li>
<li><strong>Die 1 fehlt.</strong> Dann sind 2 und 3 dabei, die 4 fehlt. Ziffern: 2, 3, 5, 6.</li></ul>
<p>Nun zu den Stellen. Im ersten Fall darf die 1 weder an Stelle 1 noch 2 noch 4 stehen – sie muss an Stelle 3. An Stelle 4 sind 4 und 6 ausgeschlossen, die 1 ist vergeben, also steht dort die 5. Für die Stellen 1 und 2 bleiben 4 und 6 in beliebiger Reihenfolge: <strong>4 6 1 5</strong> oder <strong>6 4 1 5</strong>. Im zweiten Fall kann an Stelle 3 nur die 2 stehen (3, 5 und 6 waren dort schon), und es bleiben <strong>3 6 2 5</strong> und <strong>6 5 2 3</strong>. Aus 360 Möglichkeiten sind vier geworden.</p>
<h3>Versuch 4: 4 6 1 5 – vier orange Punkte</h3>
<p>Welchen der vier Kandidaten man jetzt spielt, ist nicht egal. 4 6 1 5 hat einen Vorteil: Gegen jeden der anderen drei ergäbe er eine andere Rückmeldung – zwei orange bei 3 6 2 5, zwei orange und zwei weiße bei 6 4 1 5, zwei weiße bei 6 5 2 3. Selbst wenn er falsch gewesen wäre, hätte man die Lösung danach sicher gekannt. Hier war er richtig: geknackt in vier Versuchen.</p>
<div class="example"><strong>Merksatz:</strong> Bleiben nur noch wenige Codes übrig, wähle einen, der die anderen voneinander unterscheidet. Mit 6 4 1 5 wäre das hier schiefgegangen: Sowohl 3 6 2 5 als auch 6 5 2 3 hätten darauf mit je einem orangen und einem weißen Punkt geantwortet – ein Versuch mehr.</div>
<h2>Typische Fehler</h2>
<ul><li><strong>Weiß als „falsch“ lesen:</strong> Ein weißer Punkt ist eine gute Nachricht. Die Ziffer gehört in den Code, nur an eine andere Stelle.</li>
<li><strong>Zu viel auf einmal ändern:</strong> Wer drei Ziffern gleichzeitig austauscht, weiß hinterher oft nicht, welche Änderung die Punkte verschoben hat.</li>
<li><strong>Die Stelleninformation vergessen:</strong> „Kein Orange“ schließt pro Versuch vier Kombinationen aus Ziffer und Stelle aus. In der Beispielpartie hat genau das am Ende die Positionen festgelegt.</li>
<li><strong>Bekanntes doppelt prüfen:</strong> Ein Versuch, der nur bestätigt, was du schon weißt, kostet einen Zug. Für Fortgeschrittene kann ein bewusst unmöglicher Tipp sinnvoll sein, wenn er mehr verrät – zum Einstieg ist die Regel „nur mögliche Codes“ aber die sicherere.</li></ul>
<h2>Wie viele Codes gibt es – und wie viele Versuche braucht man?</h2>
<p>Für die erste Stelle gibt es 6 Möglichkeiten, für die zweite 5, dann 4 und 3: 6 × 5 × 4 × 3 = 360 mögliche Codes. Wir haben alle durchgerechnet: Mit bestem Spiel lässt sich jeder Code in höchstens fünf Versuchen finden; vier reichen nicht in jedem Fall. Selbst die einfache Regel „spiel immer den kleinsten noch möglichen Code“ kommt im Schnitt mit gut vier Versuchen aus und braucht nie mehr als sechs. Zehn Versuche lassen also viel Spielraum für Umwege. Die ganze Rechnung steht im Beitrag <a href="/codeknacker-mathematik.html">Wie viele Versuche braucht man beim Codeknacker?</a></p>
<h2>Woher das Spiel kommt</h2>
<p>Codeknacker ist mit dem Brettspiel <a href="https://en.wikipedia.org/wiki/Mastermind_(board_game)" rel="noopener">Mastermind</a> verwandt, das Mordecai Meirowitz 1970 erfand und das die britische Firma Invicta herausbrachte. Dort gibt es Farben statt Ziffern, und Farben dürfen sich wiederholen. Noch älter ist das Papier-und-Bleistift-Spiel „Bulls and Cows“, bei dem ebenfalls Ziffern erraten werden.</p>
<p><a href="/codeknacker.html">Zum heutigen Codeknacker</a></p>
""",
},
{
"slug": "sudoku-strategien",
"title": "Sudoku-Strategien: von einfach bis schwer",
"teaser": "Sechs Techniken mit Diagrammen – vom einzigen Kandidaten bis zum X-Wing.",
"description": "Sudoku lösen ohne Raten: Naked Single, Hidden Single, Block-Zeile, Paare und X-Wing mit Diagrammen und einer bewährten Reihenfolge erklärt.",
"published": "2026-10-29", "modified": "2026-10-31",
"related": ["schweres-sudoku-erkennen", "sudoku-regeln-und-geschichte", "raetsel-ausdrucken-seniorenrunde-schule"],
"body": """
<p>Ein Sudoku mit genau einer Lösung lässt sich durch logisches Schließen lösen – die Frage ist nur, wie viel Aufwand es kostet. Leichte Rätsel brauchen nur die ersten beiden Techniken dieser Seite, schwere verlangen mehr. Zu jeder Technik zeigt ein Diagramm, worauf du achten musst.</p>
<p>Zur Orientierung: Wir zählen Zeilen von oben nach unten und Spalten von links nach rechts, jeweils 1 bis 9. „Zeile 3, Spalte 5“ ist also das fünfte Feld in der dritten Zeile. Ein <strong>Kandidat</strong> ist eine Ziffer, die in einem leeren Feld nach den bisherigen Regeln noch möglich ist.</p>
<h2>1. Einzige Möglichkeit im Feld (Naked Single)</h2>
<p>Streiche für ein leeres Feld alle Ziffern, die schon in derselben Zeile, Spalte oder im selben 3×3-Block stehen. Bleibt nur eine übrig, ist sie die Lösung.</p>
<figure>""" + FIG_NAKED_SINGLE + """<figcaption>Zeile 5 enthält 1, 3 und 7, Spalte 5 enthält 2, 8 und 4, der mittlere Block zusätzlich 5 und 9. Für das orange Feld bleibt nur die 6.</figcaption></figure>
<p>Am schnellsten findest du solche Felder dort, wo sich volle Zeilen, Spalten und Blöcke kreuzen. Ein Feld, das von drei fast vollen Einheiten „gesehen“ wird, hat oft nur noch einen Kandidaten.</p>
<h2>2. Einziger Platz für eine Ziffer (Hidden Single)</h2>
<p>Frag umgekehrt: Wo in dieser Zeile, Spalte oder in diesem Block kann die 7 noch stehen? Gibt es nur ein passendes Feld, gehört die 7 dorthin – auch wenn in diesem Feld rechnerisch noch andere Ziffern möglich wären.</p>
<figure>""" + FIG_HIDDEN_SINGLE + """<figcaption>Die 7 in Zeile 1, die 7 in Zeile 2 und die 7 in Spalte 1 sperren sieben Felder des linken oberen Blocks, ein weiteres ist mit der 4 belegt. Die 7 des Blocks muss in Zeile 3, Spalte 3 stehen.</figcaption></figure>
<p>Diese Technik ist bei den meisten Menschen die wichtigste. Ein bewährtes Vorgehen: Nimm dir eine Ziffer vor, etwa die 1, und prüfe Block für Block, wo sie noch hinpasst. Dann die 2, und so weiter.</p>
<h2>3. Block und Zeile (Pointing)</h2>
<p>Kann eine Ziffer innerhalb eines Blocks nur noch in einer einzigen Zeile stehen, weißt du zwar noch nicht, in welchem Feld – aber sicher, dass sie in dieser Zeile liegt. Dann darf sie in derselben Zeile außerhalb des Blocks nicht mehr vorkommen.</p>
<figure>""" + FIG_POINTING + """<figcaption>Eingezeichnet sind nur die Kandidaten für die 5. Im linken oberen Block sind die Zeilen 1 und 3 voll, in Zeile 2 steht schon die 4. Die 5 des Blocks liegt also in Zeile 2 – und kann in Zeile 2, Spalte 5 und Spalte 8 gestrichen werden. Die übrigen 5-Kandidaten bleiben.</figcaption></figure>
<p>Das funktioniert auch umgekehrt: Kann eine Ziffer in einer Zeile nur noch innerhalb eines Blocks stehen, streichst du sie in den übrigen Feldern dieses Blocks.</p>
<h2>4. Paare (Naked Pair)</h2>
<p>Haben zwei Felder einer Einheit genau dieselben zwei Kandidaten, etwa 3 und 8, müssen die 3 und die 8 in diesen beiden Feldern stehen – nur die Reihenfolge ist offen. In allen anderen Feldern der Einheit kannst du 3 und 8 streichen.</p>
<figure class="wide">""" + FIG_PAIR + """<figcaption>In der Zeile haben das dritte und das sechste Feld nur die Kandidaten 3 und 8. Nach dem Streichen bleibt im ersten Feld nur die 2 – ein neuer Naked Single, und damit fällt auch die 2 im achten Feld weg.</figcaption></figure>
<p>Dasselbe gilt für drei Felder, die zusammen nur drei Kandidaten haben (Tripel). Das ist schwerer zu sehen, weil nicht jedes der drei Felder alle drei Ziffern enthalten muss.</p>
<h2>5. Versteckte Paare (Hidden Pair)</h2>
<p>Das Gegenstück zum Paar: Kommen zwei Ziffern in einer Einheit nur in denselben zwei Feldern vor, gehören diese Felder den beiden Ziffern. Alle anderen Kandidaten in diesen zwei Feldern darfst du streichen. Ein Beispiel: In einem Block passen die 4 und die 9 nur noch in zwei bestimmte Felder, die außerdem die Kandidaten 1, 6 und 7 haben. Dann stehen 4 und 9 in diesen beiden Feldern, und 1, 6 und 7 fallen dort weg.</p>
<h2>6. X-Wing</h2>
<p>Kommt eine Ziffer in zwei Zeilen jeweils nur in denselben zwei Spalten in Frage, bilden diese vier Felder ein Rechteck. Die Ziffer steht dann in zwei gegenüberliegenden Ecken – welche, ist noch offen. Sicher ist aber: In diesen beiden Spalten ist sie in allen anderen Zeilen ausgeschlossen.</p>
<figure>""" + FIG_XWING + """<figcaption>Nur die Kandidaten für die 4 sind eingezeichnet. In Zeile 2 und Zeile 7 passt die 4 nur in Spalte 3 oder 8. Entweder steht sie oben links und unten rechts oder oben rechts und unten links – in beiden Fällen sind Spalte 3 und Spalte 8 belegt. Die drei orange markierten Kandidaten fallen weg.</figcaption></figure>
<p>Den X-Wing gibt es auch um 90 Grad gedreht: zwei Spalten, in denen die Ziffer nur in denselben zwei Zeilen möglich ist.</p>
<h2>Eine Reihenfolge, die sich bewährt</h2>
<ol><li>Zuerst alle Hidden Singles suchen, Ziffer für Ziffer – ganz ohne Notizen.</li>
<li>Sobald nichts mehr geht: Kandidaten in allen leeren Feldern notieren. Im <a href="/sudoku.html">Tagessudoku</a> schaltet die Taste N in den Notizmodus.</li>
<li>Naked Singles in den Notizen suchen, dann Block-Zeile, dann Paare.</li>
<li>Nach jeder neuen Ziffer sofort die Kandidaten in Zeile, Spalte und Block nachführen. Die meisten Fehler entstehen hier.</li>
<li>Erst wenn alles andere ausgeschöpft ist, nach X-Wings suchen.</li></ol>
<h2>Häufige Fehler</h2>
<ul><li><strong>Kandidaten nicht aktualisieren:</strong> Eine alte Notiz, die eigentlich schon gestrichen sein müsste, führt zu falschen Schlüssen.</li>
<li><strong>Raten statt schließen:</strong> Wer eine Ziffer „probeweise“ einträgt und weitermacht, merkt den Fehler oft erst viele Schritte später.</li>
<li><strong>Nur auf Zeilen schauen:</strong> Viele Hidden Singles verstecken sich in Blöcken und Spalten.</li></ul>
<h2>Wie oft braucht man welche Technik?</h2>
<p>Wir haben je 100 leichte und mittlere sowie 200 schwere Sudokus aus unserem Generator mit einem Löseprogramm geprüft, das die Techniken in der Reihenfolge dieser Seite anwendet. Alle leichten und mittleren gingen allein mit den Techniken 1 und 2 auf. Bei den schweren reichten diese beiden in gut der Hälfte der Fälle; bei den übrigen kamen Block-Zeile und Paare dazu, und ein Teil brauchte noch weitergehende Techniken. Die genauen Zahlen und was ein Sudoku wirklich schwer macht, erklärt der Beitrag <a href="/schweres-sudoku-erkennen.html">Woran man ein schweres Sudoku erkennt</a>.</p>
<div class="example"><strong>Tipp:</strong> Die Tipp-Funktion im <a href="/sudoku.html">Tagessudoku</a> zeigt zuerst falsche Einträge und erklärt sonst den nächsten logischen Schritt. Lieber auf Papier üben? Die <a href="/sudoku-zum-ausdrucken-leicht.html">leichten Sudokus zum Ausdrucken</a> eignen sich gut, um Hidden Singles zu trainieren.</div>
""",
},
{
"slug": "sudoku-regeln-und-geschichte",
"title": "Sudoku: Regeln, Herkunft und erstaunliche Zahlen",
"teaser": "Woher das Zahlenrätsel kommt, warum es eigentlich amerikanisch ist und warum 17 eine magische Zahl ist.",
"description": "Sudoku-Regeln einfach erklärt, die Geschichte von Number Place über Nikoli bis zur Times, erstaunliche Zahlen und beliebte Varianten.",
"published": "2026-10-29", "modified": "2026-10-31",
"related": ["sudoku-strategien", "schweres-sudoku-erkennen", "logikraetsel-mit-kindern"],
"body": """
<p>Ein Sudoku ist ein 9×9-Gitter, das in neun Blöcke zu 3×3 Feldern unterteilt ist. Ziel ist es, jedes leere Feld mit einer Ziffer von 1 bis 9 zu füllen – so, dass jede Ziffer in jeder Zeile, jeder Spalte und jedem Block genau einmal vorkommt. Mehr Regeln gibt es nicht. Gerade diese Schlichtheit hat das Rätsel in wenigen Jahren um die Welt getragen.</p>
<h2>Die wichtigsten Begriffe</h2>
<ul><li><strong>Vorgaben</strong> sind die Ziffern, die von Anfang an im Gitter stehen.</li>
<li><strong>Einheit</strong> nennt man jede Zeile, Spalte und jeden Block – insgesamt 27 Einheiten mit je neun Feldern.</li>
<li><strong>Kandidaten</strong> sind die Ziffern, die in einem leeren Feld noch möglich sind. Viele notieren sie klein am Rand des Feldes.</li>
<li><strong>Eindeutig</strong> ist ein Sudoku, wenn es genau eine Lösung gibt. Das ist bei veröffentlichten Rätseln der Standard.</li></ul>
<h2>Woher Sudoku kommt</h2>
<p>Trotz des japanischen Namens stammt das moderne Sudoku aus den USA. Zahlenrätsel mit ähnlicher Idee gab es schon im 19. Jahrhundert in französischen Zeitungen, die mit magischen Quadraten spielten. Die heutige Form entwarf der Architekt Howard Garns: Ab 1979 erschien sie in den Rätselheften des Verlags Dell unter dem Namen „Number Place“. Garns starb 1989 – den weltweiten Erfolg erlebte er nicht mehr.</p>
<p>Der japanische Rätselverlag Nikoli übernahm die Idee 1984. Der Name Sudoku ist eine Abkürzung des japanischen Satzes „Sūji wa dokushin ni kagiru“, sinngemäß: „Ziffern dürfen nur einzeln vorkommen“. Nikoli führte 1986 zwei Gestaltungsregeln ein, die viele Rätselmacher bis heute pflegen: höchstens 32 Vorgaben und eine symmetrische Anordnung der Vorgaben.</p>
<p>Nach Europa kam Sudoku über Umwege. Der neuseeländische Richter Wayne Gould, der in Hongkong arbeitete, entdeckte die Rätsel in Japan und schrieb über rund sechs Jahre ein Programm, das sie in großer Zahl erzeugen konnte. Ab dem 12. November 2004 druckte die britische Zeitung The Times täglich Sudokus, andere Zeitungen zogen rasch nach. Seit 2006 gibt es – mit einer Pause in den Pandemiejahren 2020 und 2021 – jährlich eine Sudoku-Weltmeisterschaft. Quelle für diese Daten ist die ausführliche <a href="https://en.wikipedia.org/wiki/Sudoku" rel="noopener">Wikipedia-Darstellung zur Geschichte des Sudoku</a>.</p>
<h2>Ein alter mathematischer Verwandter</h2>
<p>Jedes gelöste Sudoku ist ein sogenanntes <a href="https://de.wikipedia.org/wiki/Lateinisches_Quadrat" rel="noopener">lateinisches Quadrat</a>: ein Gitter, in dem jedes Symbol in jeder Zeile und Spalte genau einmal vorkommt. Mit solchen Quadraten beschäftigten sich Mathematiker wie Leonhard Euler schon im 18. Jahrhundert. Sudoku fügt nur eine Bedingung hinzu: die Blöcke. Das zeigt auch, dass Sudoku kein Rechenrätsel ist – die Ziffern sind bloß Symbole. Man könnte genauso neun Farben oder Buchstaben verwenden.</p>
<h2>Erstaunliche Zahlen</h2>
<ul><li><strong>6.670.903.752.021.072.936.960</strong> vollständig ausgefüllte Sudoku-Gitter gibt es, also rund 6,67 Trilliarden – eine Zahl mit 22 Stellen. Berechnet wurde sie 2005 von Bertram Felgenhauer und Frazer Jarvis.</li>
<li><strong>5.472.730.538</strong> davon sind „wesentlich verschieden“. Zählt man Gitter nicht doppelt, die durch Umbenennen der Ziffern, Spiegeln, Drehen oder erlaubtes Umordnen von Zeilen und Spalten auseinander hervorgehen, bleiben gut 5,4 Milliarden übrig.</li>
<li><strong>17 Vorgaben</strong> sind das Minimum für ein eindeutiges Sudoku. Gary McGuire, Bastian Tugemann und Gilles Civario zeigten 2012 mit einer aufwendigen Computersuche, dass es kein eindeutiges Sudoku mit 16 Vorgaben gibt (<a href="https://arxiv.org/abs/1201.0749" rel="noopener">Fachartikel auf arXiv</a>, <a href="https://www.sudokuwiki.org/17_clue_proof" rel="noopener">Erklärung bei SudokuWiki</a>).</li>
<li><strong>27 Einheiten, 81 Felder, 20 Nachbarn:</strong> Jedes Feld „sieht“ genau 20 andere Felder – acht in der Zeile, acht in der Spalte und vier weitere im Block.</li></ul>
<h2>Woran man ein gutes Sudoku erkennt</h2>
<p>Ein gutes Sudoku hat genau eine Lösung und lässt sich durch Schließen lösen, ohne dass man an einer Stelle raten muss. Die Anzahl der Vorgaben sagt dabei wenig über die Schwierigkeit: Entscheidend ist, welche Lösungstechniken man braucht. Wir haben das an unseren eigenen Rätseln nachgezählt – nachzulesen in <a href="/schweres-sudoku-erkennen.html">Woran man ein schweres Sudoku erkennt</a>. Die Techniken selbst erklären die <a href="/sudoku-strategien.html">Sudoku-Strategien</a> mit Diagrammen.</p>
<p>Die symmetrische Anordnung der Vorgaben, die Nikoli eingeführt hat, ist dagegen reine Ästhetik. Unsere computererzeugten Rätsel verzichten darauf: Das Programm entfernt Ziffern in zufälliger Reihenfolge und prüft nach jedem Schritt, ob die Lösung eindeutig bleibt.</p>
<h2>Beliebte Varianten</h2>
<ul><li><strong>Mini-Sudoku:</strong> 4×4 mit den Ziffern 1 bis 4 oder 6×6 mit 1 bis 6 – ideal für Kinder und zum Kennenlernen der Regeln. Zwei Beispiele zum Abmalen stehen im Beitrag <a href="/logikraetsel-mit-kindern.html">Logikrätsel mit Kindern lösen</a>.</li>
<li><strong>X-Sudoku:</strong> Zusätzlich müssen auch die beiden Diagonalen alle Ziffern genau einmal enthalten.</li>
<li><strong>Killer-Sudoku:</strong> Statt Vorgaben gibt es umrandete Feldgruppen mit einer Summe. Hier wird tatsächlich gerechnet.</li>
<li><strong>Samurai-Sudoku:</strong> Fünf Sudokus überlappen sich in den Eckblöcken.</li>
<li><strong>Puzzle-Sudoku (Jigsaw):</strong> Die Blöcke sind keine Quadrate, sondern unregelmäßige Formen aus je neun Feldern.</li></ul>
<h2>Selbst ausprobieren</h2>
<p>Auf Rätsellotse gibt es jeden Tag drei neue Sudokus: leicht, mittel und schwer. Jedes hat genau eine Lösung, und die Tipp-Funktion erklärt den nächsten logischen Schritt. Wer lieber mit Bleistift arbeitet, findet sechs Rätsel je Stufe mit Lösungen zum Ausdrucken: <a href="/sudoku-zum-ausdrucken-leicht.html">leicht</a>, <a href="/sudoku-zum-ausdrucken-mittel.html">mittel</a> und <a href="/sudoku-zum-ausdrucken-schwer.html">schwer</a>.</p>
<p><a href="/sudoku.html">Zum heutigen Sudoku</a></p>
""",
},
{
"slug": "zielzahl-tipps",
"title": "Zielzahl: Regeln und Tipps zum Kopfrechnen",
"teaser": "Mit großen Zahlen nah ran, mit kleinen fein justieren – plus Rechentricks und fünf durchgerechnete Beispiele.",
"description": "Zielzahl spielen: Regeln, fünf Strategien mit durchgerechneten Beispielen und Kopfrechen-Tricks, mit denen du die Zielzahl schneller triffst.",
"published": "2026-10-29", "modified": "2026-10-31",
"related": ["logikraetsel-mit-kindern", "raetsel-ausdrucken-seniorenrunde-schule", "wie-unsere-raetsel-entstehen"],
"body": """
<p>Aus sechs Zahlen sollst du mit den vier Grundrechenarten die Zielzahl erreichen. Jede Zahl darfst du höchstens einmal verwenden, du musst aber nicht alle benutzen. Teilen ist nur erlaubt, wenn es ohne Rest aufgeht, und Zwischenergebnisse dürfen nicht negativ werden. Klammern sind erlaubt.</p>
<h2>Welche Zahlen vorkommen</h2>
<p>Bei Rätsellotse bestehen die sechs Zahlen immer aus <strong>zwei großen</strong> aus 25, 50, 75 und 100 und <strong>vier kleinen</strong> zwischen 1 und 10 – eine kleine Zahl kann dabei auch doppelt vorkommen. Die Zielzahl liegt zwischen 101 und 999. Weil das Programm sie erzeugt, indem es die Zahlen des Tages selbst verrechnet, ist jede Zielzahl erreichbar. Oft gibt es aber einen kürzeren Weg als den des Programms.</p>
<h2>Fünf Strategien mit Beispielen</h2>
<h3>1. Erst grob, dann fein</h3>
<p>Suche mit einer großen Zahl ein Produkt nahe der Zielzahl und baue den Rest aus kleinen Zahlen.</p>
<div class="example">Zahlen: 100, 50, 9, 6, 4, 1 · Zielzahl: 637<br>100 × 6 = 600, es fehlen 37 = 4 × 9 + 1.<br>Lösung: 100 × 6 + 4 × 9 + 1 = 637</div>
<h3>2. Über das Ziel hinaus und zurück</h3>
<p>Liegt die Zielzahl knapp unter einem runden Wert, ist Abziehen oft leichter als Aufbauen.</p>
<div class="example">Zahlen: 100, 25, 7, 6, 3, 2 · Zielzahl: 693<br>7 × 100 = 700 ist nur 7 zu viel – und 7 = 6 + 3 − 2.<br>Lösung: 7 × 100 − (6 + 3 − 2) = 700 − 7 = 693</div>
<h3>3. Kleine Zahlen zu einem Faktor bündeln</h3>
<p>Zwei kleine Zahlen ergeben zusammen einen Multiplikator, den es sonst nicht gäbe: 9 + 2 = 11, 8 + 4 = 12, 3 × 4 = 12.</p>
<div class="example">Zahlen: 75, 25, 9, 8, 4, 2 · Zielzahl: 817<br>75 × 11 = 825 liegt 8 über dem Ziel, und die 8 ist noch frei.<br>Lösung: 75 × (9 + 2) − 8 = 825 − 8 = 817</div>
<h3>4. Von der Zielzahl aus denken</h3>
<p>Ist die Zielzahl durch eine der kleinen Zahlen teilbar, wird die Aufgabe oft kleiner. Teste die Teilbarkeit durch 2, 3, 5, 6 und 9 – dafür gibt es schnelle Regeln (siehe unten).</p>
<div class="example">Zahlen: 50, 25, 10, 9, 6, 3 · Zielzahl: 378<br>378 ist gerade und hat die Quersumme 18, ist also durch 6 teilbar: 378 = 6 × 63. Und 63 = 50 + 10 + 3.<br>Lösung: 6 × (50 + 10 + 3) = 378</div>
<h3>5. In 25er-Schritten denken</h3>
<p>Mit 25, 50, 75 und 100 erreichst du jedes Vielfache von 25. Suche das nächstgelegene Vielfache und gleiche die Differenz mit kleinen Zahlen aus.</p>
<div class="example">Zahlen: 100, 75, 8, 5, 4, 1 · Zielzahl: 461<br>Nächstes Vielfaches von 25: 475 = 4 × 100 + 75. Es sind 14 zu viel, und 14 = 8 + 5 + 1.<br>Lösung: 4 × 100 + 75 − (8 + 5 + 1) = 461 – alle sechs Zahlen verwendet.</div>
<h2>Kopfrechen-Tricks, die bei Zielzahl helfen</h2>
<div class="scroll"><table class="tbl"><thead><tr><th scope="col">Aufgabe</th><th scope="col">Trick</th><th scope="col">Beispiel</th></tr></thead><tbody>
<tr><td>× 25</td><td>mal 100, dann durch 4</td><td>36 × 25 = 3600 ÷ 4 = 900</td></tr>
<tr><td>× 75</td><td>× 25, dann × 3</td><td>8 × 75 = 200 × 3 = 600</td></tr>
<tr><td>× 50</td><td>mal 100, dann halbieren</td><td>13 × 50 = 1300 ÷ 2 = 650</td></tr>
<tr><td>× 9</td><td>mal 10, dann die Zahl abziehen</td><td>9 × 47 = 470 − 47 = 423</td></tr>
<tr><td>× 11</td><td>mal 10, dann die Zahl addieren</td><td>11 × 75 = 750 + 75 = 825</td></tr>
<tr><td>Halbieren/Verdoppeln</td><td>einen Faktor halbieren, den anderen verdoppeln</td><td>25 × 16 = 50 × 8 = 100 × 4 = 400</td></tr>
<tr><td>Teilbar durch 3 oder 9</td><td>Quersumme durch 3 bzw. 9 teilbar</td><td>567: 5 + 6 + 7 = 18, also durch 9 teilbar</td></tr>
<tr><td>Teilbar durch 4</td><td>die letzten zwei Ziffern durch 4 teilbar</td><td>716: 16 ist durch 4 teilbar</td></tr>
</tbody></table></div>
<p>Wer diese Tricks ein paar Tage bewusst anwendet, braucht sie bald nicht mehr nachzuschlagen. Es lohnt sich außerdem, die Vielfachen von 25 und 75 bis 1000 im Kopf zu haben – das spart bei fast jeder Aufgabe Zeit.</p>
<h2>Wenn du feststeckst</h2>
<ol><li><strong>Abstand notieren:</strong> Wie weit ist dein bester Versuch vom Ziel entfernt? Oft lässt sich genau dieser Abstand aus den übrigen Zahlen bauen.</li>
<li><strong>Andere große Zahl probieren:</strong> Statt 100 × 7 vielleicht 75 × 9 oder 50 × 13 (mit 13 = 10 + 3).</li>
<li><strong>Zwischenergebnis teilen:</strong> Ein Produkt, das zu groß ist, lässt sich manchmal durch eine kleine Zahl teilen.</li>
<li><strong>Nicht alle Zahlen erzwingen:</strong> Die meisten Lösungen kommen mit vier oder fünf Zahlen aus.</li></ol>
<p>Und wenn gar nichts geht: „Lösung zeigen“ verrät einen möglichen Weg. Der Tag zählt dann zwar nicht für deine Serie, aber man lernt aus fremden Lösungswegen erstaunlich viel.</p>
<h2>Woher das Spiel kommt</h2>
<p>Die Idee stammt aus der französischen Fernsehshow „Des chiffres et des lettres“. Sie begann 1965 als reines Wortspiel; das Zahlenspiel „Le compte est bon“ kam 1972 dazu (<a href="https://wiki.apterous.org/Des_chiffres_et_des_lettres" rel="noopener">Übersicht bei Apterous</a>). In Großbritannien wurde das Format ab 1982 als „Countdown“ bekannt. Dort wählen die Kandidaten selbst, wie viele große Zahlen sie nehmen, und haben 30 Sekunden Zeit (<a href="https://incoherency.co.uk/countdown/pages/numbers-game" rel="noopener">Regeln des Zahlenspiels</a>). Bei Rätsellotse gibt es keinen Zeitdruck – du kannst so lange tüfteln, wie du willst.</p>
<p><a href="/zielzahl.html">Zur heutigen Zielzahl</a></p>
""",
},
{
"slug": "nonogramm-anleitung",
"title": "Nonogramme lösen: Anleitung und Strategien",
"teaser": "Überlappung, Ränder, Kreuze – mit einer Zeile Schritt für Schritt und einem kompletten 5×5-Beispiel.",
"description": "Nonogramme lösen lernen: Überlappung, Randtechnik und Lücken mit Diagrammen, eine Zeile Schritt für Schritt und ein komplett gelöstes Beispiel.",
"published": "2026-10-29", "modified": "2026-10-31",
"related": ["logikraetsel-mit-kindern", "wie-unsere-raetsel-entstehen", "denksport-und-gehirn"],
"body": """
<p>Bei einem Nonogramm verraten Zahlen am Rand, wie viele zusammenhängende Felder in jeder Zeile und Spalte gefüllt sind – und in welcher Reihenfolge. „3 1“ bedeutet: zuerst ein Block aus drei gefüllten Feldern, dann mindestens ein leeres Feld, dann ein einzelnes gefülltes Feld. Aus diesen Angaben entsteht Feld für Feld ein Bild. Ein gutes Nonogramm lässt sich vollständig mit Logik lösen, ohne zu raten.</p>
<h2>1. Überlappung: der Einstieg</h2>
<p>Schiebe einen Block gedanklich so weit wie möglich nach links und so weit wie möglich nach rechts. Felder, die in beiden Lagen gefüllt sind, sind sicher gefüllt. In einer Zeile mit 10 Feldern und der Angabe 7 überlappen die Lagen 1–7 und 4–10 in den Feldern 4 bis 7.</p>
<p>Das funktioniert auch mit mehreren Blöcken: Bei „4 3“ in 10 Feldern liegen die Blöcke ganz links bei 1–4 und 6–8, ganz rechts bei 3–6 und 8–10. Der erste Block überlappt in den Feldern 3–4, der zweite in Feld 8. Wichtig ist, dass du immer <em>denselben</em> Block in beiden Lagen vergleichst.</p>
<div class="example"><strong>Faustregel:</strong> Zähle alle Blöcke plus je eine Lücke dazwischen zusammen und ziehe das von der Zeilenlänge ab. Dieser „Spielraum“ ist die Strecke, um die jeder Block wandern kann. Jeder Block, der länger ist als der Spielraum, bringt sichere Felder – genau so viele, wie er länger ist.</div>
<p>Für „4 3“ in 10 Feldern: 4 + 1 + 3 = 8, Spielraum 2. Der Viererblock ist um 2 länger, bringt also 2 sichere Felder; der Dreierblock bringt eines. Mit dieser Rechnung siehst du in Sekunden, wo sich das genaue Hinschauen lohnt.</p>
<h2>2. Kreuze setzen</h2>
<p>Genauso wichtig wie gefüllte Felder sind Felder, die sicher leer bleiben. Ist eine Zeile vollständig, kommen in alle übrigen Felder Kreuze. Und wenn ein Block schon seine volle Länge erreicht hat, sind die Felder direkt davor und danach leer.</p>
<h2>3. Vom Rand aus denken</h2>
<p>Ist das erste Feld einer Zeile gefüllt, muss dort der erste Block beginnen. Bei der Angabe „3 …“ sind dann die Felder 1 bis 3 gefüllt und Feld 4 leer. Gefüllte Felder nahe am Rand begrenzen außerdem, wie weit ein Block reichen kann: Ist Feld 2 gefüllt und der erste Block hat die Länge 4, reicht er höchstens bis Feld 5.</p>
<h2>4. Zu kleine Lücken ausschließen</h2>
<p>Liegen zwischen zwei Kreuzen – oder zwischen Rand und Kreuz – weniger freie Felder, als der kleinste noch passende Block braucht, bleibt diese Lücke leer. Gerade in späteren Phasen räumt diese Technik viele Felder ab.</p>
<h2>Eine Zeile Schritt für Schritt</h2>
<p>So greifen die Techniken ineinander. Die Zeile hat zehn Felder und den Hinweis „3 2“. Aus einer Spalte wissen wir bereits, dass Feld 3 leer bleibt (Kreuz). Neu gefundene Felder sind in den Diagrammen grün, neue Kreuze orange.</p>
<figure class="wide">""" + FIG_NONO_LINE + """<figcaption>Eine Zeile mit dem Hinweis 3 2: Aus einem Kreuz und einem Feld aus der Spalte wird in vier Schritten die vollständige Zeile.</figcaption></figure>
<ol><li><strong>Ausgangslage:</strong> Ohne das Kreuz brächte die Überlappung hier gar nichts – der Spielraum ist mit 4 größer als beide Blöcke.</li>
<li><strong>Lücke zu klein:</strong> Vor dem Kreuz liegen nur zwei Felder. Der erste Block braucht drei, passt also nicht hinein; der zweite muss nach dem ersten kommen. Die Felder 1 und 2 bleiben leer.</li>
<li><strong>Überlappung im Rest:</strong> Beide Blöcke liegen jetzt in den Feldern 4 bis 10 – sieben Felder für 3 + 1 + 2 = 6, also Spielraum 1. Der Dreierblock bringt die Felder 5 und 6, der Zweierblock Feld 9.</li>
<li><strong>Information aus der Spalte:</strong> Später zeigt eine Spalte, dass Feld 8 gefüllt ist. Die Felder 8 und 9 können nicht zum Dreierblock gehören, denn der enthält schon 5 und 6 und wäre dann zu lang. Also bilden 8 und 9 den Zweierblock, die Felder 7 und 10 bleiben leer – und der Dreierblock muss genau 4 bis 6 sein.</li></ol>
<h2>Ein komplettes Beispiel: 5 × 5</h2>
<p>Das folgende Nonogramm lässt sich in vier Durchgängen lösen – abwechselnd alle Zeilen, dann alle Spalten. Probiere es zuerst selbst: Zeilen 1 1 · 5 · 5 · 3 · 1, Spalten 2 · 4 · 4 · 4 · 2.</p>
<figure class="wide">""" + FIG_NONO_HEART + """<figcaption>Vier Durchgänge, abwechselnd Zeilen und Spalten. Grün sind die im jeweiligen Durchgang neu gefüllten Felder, orange die neuen Kreuze.</figcaption></figure>
<ul><li><strong>A · Zeilen:</strong> Die Zeilen 2 und 3 („5“) sind ganz gefüllt. In Zeile 4 („3“ in 5 Feldern) ergibt die Überlappung das mittlere Feld.</li>
<li><strong>B · Spalten:</strong> Spalte 1 und 5 („2“) sind mit den Zeilen 2 und 3 schon fertig – der Rest wird gekreuzt. In den Spalten 2 bis 4 („4“) überlappen die Lagen 1–4 und 2–5 in den Zeilen 2 bis 4.</li>
<li><strong>C · Zeilen:</strong> In Zeile 1 („1 1“) sind die Ränder gekreuzt. Für zwei Einzelfelder mit Lücke bleiben nur die Felder 2 und 4, das mittlere Feld bleibt leer.</li>
<li><strong>D · Spalten:</strong> Spalte 2 und 4 sind mit den Zeilen 1 bis 4 vollständig, also bleibt Zeile 5 dort leer. Spalte 3 ist oben gekreuzt, der Viererblock liegt daher in den Zeilen 2 bis 5. Fertig ist das Herz.</li></ul>
<h2>Zwischen Zeilen und Spalten wechseln</h2>
<p>Jede neue Markierung in einer Zeile gibt einer Spalte neue Information – und umgekehrt. Wer konsequent hin und her wechselt, kommt meist ohne komplizierte Techniken bis zum Ende. Genau so arbeitet auch unser Prüfprogramm: Es löst jedes Rätsel nur mit Zeile-für-Zeile-Logik, bevor es veröffentlicht wird. Bei großen Gittern hilft es, die Zeilen und Spalten mit den größten Zahlen zuerst anzuschauen.</p>
<h2>Woher Nonogramme kommen</h2>
<p>Die Rätselform entstand 1987 in Japan, und zwar zweimal unabhängig: Die Grafikerin Non Ishida entwickelte sie nach einem Wettbewerb, bei dem Bilder mit beleuchteten Fenstern eines Hochhauses gestaltet wurden; der Rätselautor Tetsuya Nishio veröffentlichte fast gleichzeitig dieselbe Idee. Der Name „Nonogramm“ verbindet „Non“ mit „Diagramm“. Ab 1990 erschienen die Rätsel wöchentlich in der britischen Zeitung The Sunday Telegraph; später wurden sie auch als „Griddler“, „Hanjie“ oder – durch Nintendo – als „Picross“ bekannt (<a href="https://en.wikipedia.org/wiki/Nonogram" rel="noopener">Wikipedia: Nonogram</a>).</p>
<p>Mathematisch sind Nonogramme übrigens anspruchsvoller, als sie aussehen: Ganz allgemein zu entscheiden, ob ein beliebiges Nonogramm lösbar ist, gilt als NP-vollständiges Problem. Für die Rätsel auf dieser Seite spielt das keine Rolle, weil wir nur solche veröffentlichen, die sich mit Zeilenlogik lösen lassen.</p>
<p><a href="/nonogramm.html">Zum heutigen Nonogramm</a></p>
""",
},
{
"slug": "wie-unsere-raetsel-entstehen",
"title": "Wie unsere Rätsel entstehen – und warum sie fair sind",
"teaser": "Ein Blick hinter die Kulissen: Zufall mit Datum, Eindeutigkeit, Prüfprogramme – und wo die Grenzen liegen.",
"description": "Wie Rätsellotse täglich Sudokus, Nonogramme, Codes und Zielzahlen erzeugt, wie wir Eindeutigkeit prüfen und was unsere eigene Auswertung zeigt.",
"published": "2026-10-29", "modified": "2026-10-31",
"related": ["schweres-sudoku-erkennen", "codeknacker-mathematik", "nonogramm-anleitung"],
"body": """
<p>Jeden Tag erscheinen auf Rätsellotse neue Rätsel – für alle dieselben. Niemand tippt sie von Hand ab, und trotzdem soll keines davon unfair sein. Hier erklären wir, wie die Rätsel entstehen, was unsere Prüfprogramme garantieren – und wo wir bei der Schwierigkeit selbst noch nachgemessen haben.</p>
<h2>Zufall, der vom Datum abhängt</h2>
<p>Unsere Rätsel werden von einem Programm erzeugt, das einen Zufallsgenerator verwendet. Der Startwert dieses Generators ergibt sich aus dem Datum (nach Wiener Zeit) und der Rätselart. Dadurch bekommen alle, die am selben Tag spielen, exakt dasselbe Rätsel – ohne dass ein Server Rätsel verteilen oder Spielstände speichern muss. Das ist auch der Grund, warum das Archiv funktioniert: Das Rätsel vom 3. März lässt sich jederzeit genau so wieder erzeugen, und zwar direkt in deinem Browser.</p>
<p>Diese Bauweise hat einen Nebeneffekt, der uns wichtig ist: Weil alles im Browser passiert, brauchen wir keine Daten über dich, um dir das richtige Rätsel zu zeigen.</p>
<h2>Sudoku: genau eine Lösung</h2>
<p>Ein Sudoku entsteht in zwei Schritten. Zuerst füllt das Programm ein vollständiges, gültiges Gitter mit zufälliger Ziffernfolge. Dann entfernt es Ziffern in zufälliger Reihenfolge. Nach jedem Schritt prüft ein Löser, ob das Rätsel noch <strong>genau eine</strong> Lösung hat. Hätte es zwei, wird die Ziffer zurückgelegt.</p>
<p>Die Stufen unterscheiden sich in zwei Punkten. Erstens in der Zielzahl an Vorgaben: 38 für leicht, 30 für mittel, 25 für schwer. Zweitens prüfen wir bei leicht und mittel nach jedem Entfernen zusätzlich, ob sich das Rätsel noch allein mit den zwei Grundtechniken lösen lässt – „einzige Möglichkeit im Feld“ und „einziger Platz für eine Ziffer“. Wäre das nicht mehr der Fall, bleibt die Ziffer stehen.</p>
<h3>Was wir bei den schweren Sudokus nachgemessen haben</h3>
<p>Bei schweren Sudokus garantiert das Programm die Eindeutigkeit, schreibt aber keine bestimmten Techniken vor. Wir wollten wissen, was das in der Praxis heißt, und haben 200 schwere Rätsel aus unserem Generator mit einem Löseprogramm geprüft, das typische menschliche Techniken anwendet. Ergebnis: Gut die Hälfte ging allein mit den Grundtechniken auf; rund ein Fünftel brauchte Block-Zeile, Paare oder ähnliche Techniken; und etwas mehr als ein Viertel verlangte Techniken, die über das hinausgehen, was wir in den <a href="/sudoku-strategien.html">Sudoku-Strategien</a> erklären. Die genauen Zahlen stehen in <a href="/schweres-sudoku-erkennen.html">Woran man ein schweres Sudoku erkennt</a>.</p>
<p>Für dich heißt das: Die Stufe „schwer“ schwankt stärker als die anderen beiden. Wenn ein schweres Sudoku sich ungewohnt zäh anfühlt, liegt das nicht an dir – manche davon sind wirklich deutlich anspruchsvoller als andere.</p>
<h2>Nonogramm: lösbar ohne Raten</h2>
<p>Für Nonogramme erzeugt das Programm zunächst ein zufälliges Muster, in dem gut die Hälfte der Felder gefüllt ist. Dann glättet es das Muster einmal: Jedes Feld übernimmt den Zustand, den die Mehrheit seiner Nachbarn hat. So entstehen zusammenhängende Formen statt Rauschen. Muster, die danach zu leer oder zu voll sind, werden verworfen.</p>
<p>Dann versucht ein Löser, das Rätsel nur mit Zeile-für-Zeile-Logik zu knacken – mit genau den Überlegungen aus der <a href="/nonogramm-anleitung.html">Nonogramm-Anleitung</a>. Gelingt das nicht vollständig, wird das Muster verworfen und ein neues erzeugt. Auch Rätsel, die in ganz wenigen Durchgängen aufgehen, sortiert das Programm aus. Erst wenn ein Rätsel alle Tests besteht, wird es zum Tagesrätsel. Weil Zeilenlogik ohne Raten auskommt, folgt daraus auch: Jedes veröffentlichte Nonogramm hat genau eine Lösung.</p>
<h2>Zielzahl: garantiert erreichbar</h2>
<p>Bei der Zielzahl gehen wir den umgekehrten Weg. Das Programm zieht zwei große Zahlen aus 25, 50, 75 und 100 sowie vier kleine aus 1 bis 10. Dann verrechnet es drei bis fünf Mal zufällig zwei Zahlen miteinander – mit Plus, Mal, Minus (immer die größere minus die kleinere) oder Geteilt, wenn es ohne Rest aufgeht. Liegt das Ergebnis zwischen 101 und 999, wird es zur Zielzahl. Sie ist damit nachweislich erreichbar. Oft gibt es zusätzlich ganz andere, elegantere Wege – Ideen dafür stehen in den <a href="/zielzahl-tipps.html">Zielzahl-Tipps</a>.</p>
<h2>Codeknacker: immer knackbar</h2>
<p>Der Code des Tages entsteht, indem das Programm die Ziffern 1 bis 6 mischt und die ersten vier nimmt. Es gibt 360 mögliche Codes. Wir haben alle durchgerechnet: Mit bestem Spiel lässt sich jeder davon in höchstens fünf Versuchen finden, und selbst einfache Strategien brauchen nie mehr als sechs. Zehn Versuche lassen also reichlich Spielraum. Die Rechnung dazu steht in <a href="/codeknacker-mathematik.html">Wie viele Versuche braucht man beim Codeknacker?</a></p>
<h2>Was ein Programm nicht kann</h2>
<p>Ein Generator prüft Regeln, aber er hat keinen Geschmack. Ein von Hand gestaltetes Nonogramm zeigt ein Motiv; unsere Bilder sind abstrakte Formen. Ein Sudoku-Autor kann einen „Aha-Moment“ bewusst einbauen; unser Programm findet so etwas höchstens zufällig. Dafür gibt es jeden Tag neue Rätsel, die für alle gleich sind und sich lückenlos nachspielen lassen. Wenn du ein Rätsel findest, das dir unfair vorkommt, schreib uns an <a href="mailto:office@adstern.com">office@adstern.com</a> – mit Datum und Rätselart können wir es exakt nachbauen.</p>
<h2>Was wir nicht tun</h2>
<p>Es gibt kein Konto, keine Bestenliste und keine Spielstände auf unseren Servern. Fortschritt und Statistik bleiben in deinem Browser. Werbung und Reichweitenmessung laufen nur, wenn du einwilligst. Mehr dazu auf der Seite <a href="/about.html">Über Rätsellotse</a>.</p>
""",
},
{
"slug": "codeknacker-mathematik",
"title": "Wie viele Versuche braucht man beim Codeknacker?",
"teaser": "360 Codes, 11 mögliche Antworten, höchstens 5 Versuche: die Mathematik hinter dem Zahlencode.",
"description": "Wir haben alle 360 Codes durchgerechnet: Wie viel verrät der erste Tipp, warum fünf Versuche immer reichen und wie gut einfache Strategien sind.",
"published": "2026-10-31",
"related": ["codeknacker-anleitung", "wie-unsere-raetsel-entstehen", "schweres-sudoku-erkennen"],
"body": """
<p>Vier verschiedene Ziffern von 1 bis 6, zehn Versuche: Ist das großzügig oder knapp? Um das zu beantworten, haben wir alle 360 möglichen Codes mit einem kleinen Programm durchgespielt. Dieser Beitrag zeigt, was dabei herauskam – und was du daraus für deine eigenen Partien mitnehmen kannst. Die Regeln selbst erklärt die <a href="/codeknacker-anleitung.html">Codeknacker-Anleitung</a>.</p>
<h2>360 Codes – und warum der erste Tipp egal ist</h2>
<p>Für die erste Stelle gibt es sechs Ziffern zur Auswahl, für die zweite fünf, dann vier und drei: 6 × 5 × 4 × 3 = 360 Codes. Für den ersten Versuch gilt eine überraschende Symmetrie: Es ist gleichgültig, welchen Code du zuerst tippst. Ob 1 2 3 4 oder 6 3 5 1 – durch Umbenennen der Ziffern und Vertauschen der Stellen lässt sich jeder erste Tipp in jeden anderen überführen. Alle ersten Tipps verraten im Schnitt gleich viel. Erst ab dem zweiten Versuch zählt die Wahl.</p>
<h2>Nur 11 mögliche Antworten</h2>
<p>Die Rückmeldung besteht aus orangen Punkten (richtige Ziffer, richtige Stelle) und weißen (richtige Ziffer, falsche Stelle). Weil jeder Code nur vier der sechs Ziffern enthält, haben zwei Codes immer mindestens zwei Ziffern gemeinsam. Orange plus Weiß ist also immer 2, 3 oder 4. Daraus ergeben sich nur elf mögliche Antworten – drei orange und ein weißer Punkt sind ausgeschlossen, denn die vierte Ziffer hätte nur noch ihren eigenen Platz frei.</p>
<p>So verteilen sich die 360 Codes auf die Antworten zum ersten Tipp 1 2 3 4:</p>
<div class="scroll"><table class="tbl"><thead><tr><th scope="col">Orange</th><th scope="col">Weiß</th><th scope="col">Codes</th><th scope="col">Warum genau so viele?</th></tr></thead><tbody>
<tr><td>0</td><td>2</td><td>84</td><td>zwei von 1–4 dabei, beide falsch platziert, dazu 5 und 6</td></tr>
<tr><td>0</td><td>3</td><td>88</td><td>die häufigste Antwort</td></tr>
<tr><td>0</td><td>4</td><td>9</td><td>1 2 3 4 so vertauscht, dass keine Ziffer an ihrem Platz bleibt</td></tr>
<tr><td>1</td><td>1</td><td>48</td><td></td></tr>
<tr><td>1</td><td>2</td><td>72</td><td></td></tr>
<tr><td>1</td><td>3</td><td>8</td><td>4 Wahlen für die feste Ziffer × 2 Arten, die übrigen drei zu verschieben</td></tr>
<tr><td>2</td><td>0</td><td>12</td><td>6 Wahlen für zwei feste Ziffern × 2 Anordnungen von 5 und 6</td></tr>
<tr><td>2</td><td>1</td><td>24</td><td></td></tr>
<tr><td>2</td><td>2</td><td>6</td><td>zwei Ziffern bleiben, die anderen zwei tauschen die Plätze</td></tr>
<tr><td>3</td><td>0</td><td>8</td><td>4 Wahlen für die falsche Stelle × 5 oder 6 dort</td></tr>
<tr><td>4</td><td>0</td><td>1</td><td>Volltreffer</td></tr></tbody></table></div>
<p>Die häufigsten Antworten – null orange und zwei oder drei weiße Punkte – lassen jeweils mehr als 80 Codes übrig. Ein erster Versuch reduziert die Auswahl also im ungünstigen Fall nur auf knapp ein Viertel. Gut zu wissen, wenn nach dem ersten Tipp „nur weiße Punkte“ kommen: Das ist der Normalfall, kein Pech.</p>
<h2>Eine Untergrenze aus der Informationstheorie</h2>
<p>Wie viele Versuche braucht man mindestens? Eine einfache Überlegung hilft: Jeder Versuch hat höchstens elf mögliche Antworten. Nach zwei Versuchen lassen sich die Codes also in höchstens 11 × 11 = 121 Gruppen aufteilen – zu wenig, um 360 Codes sicher auseinanderzuhalten. Ganz ohne Glück braucht man daher mindestens drei Versuche, um den Code zu kennen, und einen weiteren, um ihn einzugeben. In der Sprache der Informationstheorie: Der Code steckt in rund 8,5 Bit, eine Antwort liefert höchstens knapp 3,5 Bit.</p>
<h2>Fünf Versuche reichen immer – vier nicht</h2>
<p>Ob vier Versuche immer genügen, lässt sich nicht mit einer Überschlagsrechnung entscheiden. Deshalb haben wir es durchgerechnet: Das Programm hat für jede mögliche Antwort auf den ersten Tipp geprüft, ob es eine Folge von Versuchen gibt, die jeden verbleibenden Code spätestens im vierten Zug trifft. Für alle Antworten mit mindestens zwei orangen Punkten und für „vier weiße“ klappt das. Für die übrigen – null orange mit zwei oder drei weißen Punkten und alle Antworten mit genau einem orangen Punkt – gibt es keine solche Folge. Fünf Versuche dagegen reichen immer.</p>
<p>Ein Programm, das bei jedem Zug den Tipp wählt, dessen ungünstigste Antwort die wenigsten Codes übrig lässt, kam auf folgende Verteilung über alle 360 Codes:</p>
<div class="scroll"><table class="tbl"><thead><tr><th scope="col">Strategie</th><th scope="col">Durchschnitt</th><th scope="col">Höchstens</th><th scope="col">Bemerkung</th></tr></thead><tbody>
<tr><td>Programm (kleinste ungünstigste Restgruppe)</td><td>4,08</td><td>5</td><td>1 Code im 1., 3 im 2., 59 im 3., 200 im 4., 97 im 5. Versuch</td></tr>
<tr><td>Immer den kleinsten noch möglichen Code</td><td>4,15</td><td>6</td><td>leicht von Hand umzusetzen</td></tr>
<tr><td>Zufällig einen noch möglichen Code</td><td>4,13</td><td>6</td><td>Mittel aus 30 Durchläufen über alle Codes</td></tr></tbody></table></div>
<p>Bemerkenswert ist, wie nah die einfachen Strategien am Programm liegen. Wer konsequent nur Codes spielt, die zu allen bisherigen Hinweisen passen, verliert im Schnitt weniger als ein Zehntel eines Versuchs. Der eigentliche Gewinn der ausgeklügelten Strategie liegt im schlimmsten Fall: Sie braucht nie einen sechsten Versuch.</p>
<h2>Was heißt das für deine Partien?</h2>
<ul><li><strong>Vier oder fünf Versuche sind ein sehr gutes Ergebnis.</strong> Auch ein Computer mit perfekter Übersicht braucht in mehr als einem Viertel der Fälle fünf.</li>
<li><strong>Ein Treffer in höchstens drei Versuchen ist Glück.</strong> Das gelingt dem Programm nur bei 63 von 360 Codes.</li>
<li><strong>Zehn Versuche sind großzügig.</strong> Sie lassen Raum für Umwege, Denkfehler und Experimente – genau richtig für ein Tagesrätsel, das Spaß machen soll.</li>
<li><strong>Konsequenz schlägt Raffinesse.</strong> Der größte Fortschritt kommt nicht von cleveren Testcodes, sondern davon, nie einen Code zu spielen, der den bisherigen Hinweisen widerspricht.</li></ul>
<h2>Der Vergleich mit Mastermind</h2>
<p>Beim klassischen <a href="https://en.wikipedia.org/wiki/Mastermind_(board_game)" rel="noopener">Mastermind</a> mit sechs Farben und vier Stecklöchern dürfen sich Farben wiederholen. Dadurch gibt es 6 × 6 × 6 × 6 = 1296 Codes, mehr als dreimal so viele wie beim Codeknacker. Der Informatiker Donald Knuth zeigte 1976, dass man auch dort mit höchstens fünf Versuchen auskommt. Dass beide Varianten trotzdem dieselbe Obergrenze haben, liegt auch an den Antworten: Bei Mastermind sind 14 verschiedene Rückmeldungen möglich, beim Codeknacker nur 11 – jeder Versuch kann dort also etwas mehr verraten.</p>
<h2>So haben wir gerechnet</h2>
<p>Unser Programm erzeugt alle 360 Codes und berechnet für jedes Paar aus Tipp und Code die Rückmeldung so, wie es auch das Spiel tut. Die Aussage „vier Versuche reichen nicht immer“ beruht auf einer vollständigen Suche, nicht auf einer Stichprobe. Die Durchschnittswerte für die einfachen Strategien sind exakt; nur der Wert für „zufällig“ ist ein Mittel aus Simulationen. Wenn du nachrechnen willst: Die Tabelle oben lässt sich mit etwas Kombinatorik auch von Hand prüfen.</p>
<p><a href="/codeknacker.html">Zum heutigen Codeknacker</a></p>
""",
},
{
"slug": "schweres-sudoku-erkennen",
"title": "Woran man ein schweres Sudoku erkennt",
"teaser": "Die Zahl der Vorgaben täuscht. Entscheidend ist, welche Technik das Rätsel verlangt – mit Zahlen aus 400 geprüften Sudokus.",
"description": "Warum die Zahl der Vorgaben wenig über die Schwierigkeit sagt, welche Technikstufen es gibt und was unsere Auswertung von 400 Sudokus zeigt.",
"published": "2026-10-31",
"related": ["sudoku-strategien", "sudoku-regeln-und-geschichte", "wie-unsere-raetsel-entstehen"],
"body": """
<p>Leicht, mittel, schwer, teuflisch: Fast jedes Sudoku trägt ein Etikett. Aber was steckt dahinter? Viele glauben, die Zahl der vorgegebenen Ziffern entscheide. Das stimmt nur zum Teil. Ein Sudoku ist so schwer wie der schwierigste Gedankenschritt, den man zum Lösen braucht. Dieser Beitrag erklärt die Stufen, zeigt, woran man sie früh erkennt – und legt offen, wie sich unsere eigenen Rätsel verteilen.</p>
<h2>Warum die Vorgaben täuschen</h2>
<p>Die Zahl der Vorgaben ist eine grobe Richtschnur: Mit 38 Vorgaben ist ein Sudoku meist leichter als mit 25. Doch wie die Vorgaben verteilt sind, wiegt schwerer als ihre Anzahl. Zwei Rätsel mit gleich vielen Ziffern können sich anfühlen wie zwei verschiedene Spiele – das eine löst sich wie von selbst, beim anderen geht nach fünf Minuten nichts mehr.</p>
<p>Das zeigt sich auch an unseren eigenen Rätseln. Wir haben 200 schwere Sudokus aus unserem Generator ausgewertet, alle mit 25 bis 27 Vorgaben. Gut die Hälfte davon ließ sich mit denselben zwei Grundtechniken lösen wie ein leichtes Rätsel. Gleich viele Vorgaben, völlig unterschiedlicher Aufwand.</p>
<h2>Die Schwierigkeit steckt in den Techniken</h2>
<p>Rätselautoren und Bewertungsprogramme ordnen Lösungstechniken in Stufen. Ein Sudoku bekommt die Stufe der anspruchsvollsten Technik, ohne die es nicht weitergeht. Eine übliche Einteilung:</p>
<div class="scroll"><table class="tbl"><thead><tr><th scope="col">Stufe</th><th scope="col">Typische Techniken</th><th scope="col">Was man tun muss</th></tr></thead><tbody>
<tr><td>1 · Einstieg</td><td>Naked Single, Hidden Single</td><td>Ziffern direkt finden, oft ganz ohne Notizen</td></tr>
<tr><td>2 · Fortgeschritten</td><td>Block-Zeile, Paare, versteckte Paare</td><td>Kandidaten notieren und gezielt streichen</td></tr>
<tr><td>3 · Schwer</td><td>Tripel, X-Wing, Swordfish, XY-Wing</td><td>Muster über mehrere Einheiten hinweg erkennen</td></tr>
<tr><td>4 · Sehr schwer</td><td>Ketten und ähnliche Techniken</td><td>lange Folgerungen über viele Felder hinweg verfolgen</td></tr></tbody></table></div>
<p>Die Stufen 1 und 2 sowie den X-Wing erklären die <a href="/sudoku-strategien.html">Sudoku-Strategien</a> mit Diagrammen. Der Sprung von Stufe 1 zu Stufe 2 ist für die meisten Menschen der größte: Plötzlich findet man keine Ziffern mehr, sondern streicht Möglichkeiten, bis irgendwo eine Ziffer übrig bleibt.</p>
<h2>Was unsere Auswertung zeigt</h2>
<p>Für diesen Beitrag haben wir 100 leichte, 100 mittlere und 200 schwere Sudokus mit demselben Verfahren erzeugt wie die Rätsel auf dieser Seite. Ein Löseprogramm hat sie dann nur mit menschlichen Techniken bearbeitet – immer zuerst die einfachste, die noch weiterhilft. Notiert wurde die schwierigste Technik, die nötig war.</p>
<div class="scroll"><table class="tbl"><thead><tr><th scope="col">Stufe</th><th scope="col">Vorgaben</th><th scope="col">nur Grundtechniken</th><th scope="col">Block-Zeile</th><th scope="col">Paare, Tripel</th><th scope="col">XY-Wing</th><th scope="col">darüber hinaus</th></tr></thead><tbody>
<tr><td>leicht (100)</td><td>38</td><td>100 %</td><td>–</td><td>–</td><td>–</td><td>–</td></tr>
<tr><td>mittel (100)</td><td>30</td><td>100 %</td><td>–</td><td>–</td><td>–</td><td>–</td></tr>
<tr><td>schwer (200)</td><td>25–27</td><td>52 %</td><td>10,5 %</td><td>7 %</td><td>2 %</td><td>28,5 %</td></tr></tbody></table></div>
<p>Drei Dinge fallen auf. Erstens: Leichte Sudokus sind bei uns wirklich leicht – 91 der 100 ließen sich sogar allein mit „einzige Möglichkeit im Feld“ lösen. Mittlere brauchen öfter den Blick „wo kann diese Ziffer noch hin?“. Zweitens: In der Stufe schwer streuen die Rätsel enorm. Drittens: Mehr als ein Viertel der schweren Rätsel verlangte Techniken jenseits von Paaren, Tripeln, X-Wing, Swordfish und XY-Wing. Das sind die Rätsel, bei denen auch geübte Spielerinnen und Spieler ins Grübeln kommen. Einen X-Wing oder Swordfish als schwierigsten Schritt brauchte übrigens keines der 200 Rätsel – sie waren immer entweder nicht nötig oder nicht ausreichend.</p>
<h2>Fünf Anzeichen, die du schon am Anfang siehst</h2>
<ol><li><strong>Der erste Durchgang stockt früh.</strong> Wenn du nach einer Runde Hidden Singles (jede Ziffer einmal durch alle Blöcke) weniger als fünf neue Ziffern gefunden hast, wird es meist zäh.</li>
<li><strong>Eine Ziffer fehlt fast ganz.</strong> Kommt eine Ziffer unter den Vorgaben gar nicht oder nur einmal vor, fehlen für sie die Ansatzpunkte. Das ist kein Beweis für Schwierigkeit, aber ein häufiges Zeichen.</li>
<li><strong>Leere Blöcke oder Zeilen.</strong> Ein Block mit nur einer oder zwei Vorgaben lässt sich oft erst ganz am Ende füllen.</li>
<li><strong>Viele Felder mit drei oder mehr Kandidaten.</strong> Sobald du Notizen machst: Haben kaum Felder nur zwei Kandidaten, gibt es wenig Ansatzpunkte für Paare und Muster.</li>
<li><strong>Die Tipp-Funktion erklärt etwas Neues.</strong> Wenn der nächste Schritt eine Technik ist, die du noch nicht kennst, ist das Rätsel für dich gerade schwer – und eine gute Gelegenheit, sie zu lernen.</li></ol>
<h2>Was tun, wenn es nicht weitergeht?</h2>
<ul><li><strong>Kandidaten vollständig notieren.</strong> Viele „unlösbare“ Stellen sind in Wahrheit übersehene Kandidaten oder vergessene Streichungen.</li>
<li><strong>Systematisch nach Paaren suchen.</strong> Gehe jede Einheit durch und schau nur auf Felder mit genau zwei Kandidaten.</li>
<li><strong>Eine Ziffer über das ganze Gitter verfolgen.</strong> Markiere gedanklich alle Felder, in denen die 4 noch möglich ist. Rechtecke und Muster werden so sichtbar.</li>
<li><strong>Pause machen.</strong> Klingt banal, hilft aber: Mit frischem Blick fallen Hidden Singles auf, die vorher unsichtbar waren.</li></ul>
<h2>Und wie viele Vorgaben braucht es mindestens?</h2>
<p>Mathematisch steht fest: Ein Sudoku mit genau einer Lösung braucht mindestens 17 Vorgaben. Das zeigten Gary McGuire, Bastian Tugemann und Gilles Civario 2012 mit einer großen Computersuche (<a href="https://arxiv.org/abs/1201.0749" rel="noopener">arXiv</a>). Die Grenze sagt aber nichts über die Schwierigkeit – auch bei wenigen Vorgaben kann ein Rätsel freundlich sein, wenn sie gut verteilt sind. Mehr Hintergrund steht in <a href="/sudoku-regeln-und-geschichte.html">Sudoku: Regeln, Herkunft und erstaunliche Zahlen</a>.</p>
<h2>So haben wir gemessen</h2>
<p>Unser Löseprogramm kennt diese Techniken: einzige Möglichkeit im Feld, einziger Platz für eine Ziffer, Block-Zeile in beide Richtungen, offene und versteckte Paare und Tripel, X-Wing, Swordfish und XY-Wing. Jede Streichung wurde gegen die bekannte Lösung geprüft. Die Rätsel stammen aus demselben Generator wie die Druckseiten; die tägliche Online-Version arbeitet nach demselben Verfahren. Die Zahlen beschreiben unsere Rätsel, nicht Sudokus im Allgemeinen – andere Verlage und Apps setzen ihre Grenzen anders.</p>
<div class="example"><strong>Zum Ausprobieren:</strong> Auf der Seite <a href="/sudoku-zum-ausdrucken-schwer.html">Sudoku zum Ausdrucken – schwer</a> sind die Rätsel 1, 2 und 4 nach unserer Auswertung deutlich anspruchsvoller als 3, 5 und 6. Vergleiche selbst, ob du den Unterschied spürst.</div>
""",
},
{
"slug": "denksport-und-gehirn",
"title": "Denksport und Gehirn: Was Rätsel nachweislich bringen – und was nicht",
"teaser": "Was Studien zu Rätseln, Gehirntraining und Demenzvorbeugung wirklich zeigen – vorsichtig gelesen, mit Quellen.",
"description": "Halten Sudoku und Kreuzworträtsel das Gehirn fit? Was Studien und Übersichtsarbeiten tatsächlich zeigen – und welche Versprechen zu weit gehen.",
"published": "2026-10-31",
"related": ["raetsel-ausdrucken-seniorenrunde-schule", "logikraetsel-mit-kindern", "sudoku-strategien"],
"body": """
<p>„Rätseln hält das Gehirn jung“ – kaum ein Satz über Sudoku und Kreuzworträtsel wird so oft wiederholt. Als Rätselseite hätten wir allen Grund, ihn gern zu glauben. Gerade deshalb wollen wir genau hinschauen: Was zeigen Studien wirklich, was nicht, und was folgt daraus für den Alltag? Die Quellen sind am Ende verlinkt.</p>
<div class="example"><strong>Kurz gesagt:</strong> Wer regelmäßig rätselt, wird vor allem besser im Rätseln. Menschen, die oft knobeln, schneiden in Gedächtnistests im Schnitt besser ab – ob das Rätseln die Ursache ist, ist aber nicht belegt. Für Gehirntraining im engeren Sinn gibt es Hinweise auf kleine, begrenzte Effekte. Einen nachgewiesenen Schutz vor Demenz bietet Rätseln nicht. Wer es gern tut, sollte es tun – als Freude, nicht als Medizin.</div>
<h2>Was Beobachtungsstudien zeigen</h2>
<p>Die bekanntesten Ergebnisse stammen aus Beobachtungsstudien. Dabei werden Menschen gefragt, wie oft sie rätseln, und ihre geistige Leistung wird gemessen. 2019 veröffentlichte ein Team um Helen Brooker zwei solche Auswertungen aus der britischen Online-Studie PROTECT mit über 19.000 Teilnehmenden ab 50 Jahren. Wer häufiger Zahlenrätsel oder Worträtsel löste, schnitt in Tests zu Aufmerksamkeit, Schlussfolgern und Gedächtnis im Schnitt besser ab [1, 2]. Die Forschenden betonten selbst, dass sich daraus nicht ableiten lässt, Rätsel würden das Demenzrisiko senken [3].</p>
<p>Ähnlich vorsichtig muss man die Bronx Aging Study lesen. Dort wurden 488 anfangs gesunde ältere Menschen über Jahre begleitet; 101 erkrankten an Demenz. Bei denjenigen, die in ihrer Freizeit mehr geistig anregenden Tätigkeiten nachgingen – Lesen, Schreiben, Kreuzworträtsel, Brett- und Kartenspiele, Gruppendiskussionen, Musizieren –, setzte der beschleunigte Gedächtnisabbau später ein. Sobald er begann, verlief er bei ihnen allerdings schneller [4].</p>
<h3>Das Problem mit der Henne und dem Ei</h3>
<p>Beobachtungsstudien können Zusammenhänge zeigen, aber keine Ursachen. Es ist gut möglich, dass Menschen mit wacher geistiger Leistung einfach lieber rätseln – und nicht umgekehrt. Bildung, Beruf, Einkommen und Gesundheit hängen sowohl mit dem Freizeitverhalten als auch mit der geistigen Fitness zusammen. Studien versuchen, solche Faktoren herauszurechnen, ganz gelingt das nie.</p>
<h2>Was Trainingsstudien zeigen</h2>
<p>Um Ursachen zu prüfen, braucht man Experimente: Menschen werden zufällig einer Trainings- oder einer Vergleichsgruppe zugeteilt. Die größte Studie dieser Art ist ACTIVE aus den USA mit 2.832 älteren Menschen. Sie erhielten zehn Trainingseinheiten von 60 bis 70 Minuten zu Gedächtnis, logischem Denken oder Verarbeitungsgeschwindigkeit. Zehn Jahre später lagen die Gruppen für logisches Denken und Geschwindigkeit in den trainierten Fähigkeiten noch über der Vergleichsgruppe; beim Gedächtnistraining war kein Unterschied mehr messbar. Alle Trainingsgruppen berichteten weniger Schwierigkeiten im Alltag, objektive Alltagstests zeigten aber keinen Unterschied [5, 6].</p>
<p>Übersichtsarbeiten, die viele Studien zusammenfassen, zeichnen ein nüchternes Bild:</p>
<ul><li>Eine große Auswertung der Forschung zu kommerziellen Gehirntrainings kam 2016 zu dem Schluss: Man wird besser in den geübten Aufgaben, weniger in ähnlichen Aufgaben und kaum in anderen. Für eine Verbesserung der geistigen Leistung im Alltag fand sie sehr wenig Belege [7].</li>
<li>Eine Meta-Analyse zu Schach, Musikunterricht und Arbeitsgedächtnistraining fand 2017: Je sorgfältiger eine Studie angelegt war, desto kleiner war der Effekt auf allgemeine Fähigkeiten wie Intelligenz oder Schulleistung – in den besten Studien war er praktisch null [8].</li>
<li>Ein Cochrane-Review von 2020 zu mindestens zwölfwöchigem Computer-Gehirntraining bei gesunden älteren Menschen fand allenfalls kleine kurzfristige Effekte, ohne Beleg für eine anhaltende Wirkung nach einem Jahr. Die Vertrauenswürdigkeit der Ergebnisse stuften die Autorinnen und Autoren als niedrig bis sehr niedrig ein [9].</li></ul>
<p>Fachleute sprechen vom Problem des „Transfers“: Übung überträgt sich gut auf sehr ähnliche Aufgaben und schlecht auf entfernte. Wer täglich Sudoku löst, wird ein besserer Sudoku-Spieler. Dass man dadurch auch Termine besser behält oder schneller Auto fährt, ist nicht gezeigt.</p>
<h2>Was Fachgremien empfehlen</h2>
<p>Die Weltgesundheitsorganisation hat 2019 Leitlinien zur Verringerung des Risikos für geistigen Abbau und Demenz veröffentlicht. Kognitives Training „kann“ älteren Menschen angeboten werden – als bedingte Empfehlung, gestützt auf Belege von sehr niedriger bis niedriger Qualität [10]. Deutlich klarer fallen die Empfehlungen zu Bewegung und zum Rauchstopp aus.</p>
<p>Die Lancet-Kommission zur Demenz nannte 2024 vierzehn beeinflussbare Risikofaktoren, darunter geringe Bildung, Hörverlust, Bluthochdruck, Rauchen, Bewegungsmangel, Depression, soziale Isolation und unbehandelte Sehschwäche. Würden alle beseitigt, ließen sich nach ihrer Schätzung bis zu 45 Prozent der Demenzfälle verhindern oder hinauszögern [11, 12]. Ein „zu wenig gerätselt“ steht nicht auf der Liste; die Kommission empfiehlt aber ein körperlich, sozial und geistig aktives Leben.</p>
<h2>Wenn Werbung zu viel verspricht</h2>
<p>Wie heikel große Versprechen sind, zeigte 2016 ein Fall in den USA: Die Verbraucherschutzbehörde FTC warf dem Anbieter einer bekannten Gehirntraining-App vor, ohne ausreichende Belege mit besserer Leistung in Schule und Beruf und mit Schutz vor altersbedingtem Abbau geworben zu haben. Das Unternehmen zahlte im Vergleich zwei Millionen US-Dollar [13]. Wenn ein Rätselangebot „Demenzvorbeugung“ verspricht, ist Skepsis angebracht – auch bei uns.</p>
<h2>Was Rätsel trotzdem bringen</h2>
<p>Das heißt nicht, dass Rätseln wertlos wäre. Nur liegt sein Wert woanders als in Gesundheitsversprechen:</p>
<ul><li><strong>Es macht Freude.</strong> Ein gelöstes Rätsel ist ein kleines, verlässliches Erfolgserlebnis.</li>
<li><strong>Es ist eine Pause.</strong> Zehn Minuten volle Konzentration auf eine Aufgabe ohne Benachrichtigungen tun vielen Menschen gut.</li>
<li><strong>Es verbindet.</strong> Gemeinsam knobeln, Ergebnisse vergleichen, Lösungswege erklären – soziale Kontakte sind ein Faktor, den die Lancet-Kommission ausdrücklich nennt. Ideen dafür stehen in <a href="/raetsel-ausdrucken-seniorenrunde-schule.html">Rätsel ausdrucken für Seniorenrunde, Schule und Wartezimmer</a>.</li>
<li><strong>Man lernt etwas.</strong> Wer neue Techniken lernt, etwa die <a href="/sudoku-strategien.html">Sudoku-Strategien</a>, fordert sich anders als mit Routineaufgaben. Abwechslung zwischen Rätselarten schadet sicher nicht.</li></ul>
<p>Unser Fazit: Rätseln ist ein gutes Hobby, kein Medikament. Wer seinem Gehirn nach heutigem Wissen etwas Gutes tun will, bewegt sich regelmäßig, lässt Blutdruck, Hören und Sehen prüfen, pflegt Kontakte – und darf danach mit gutem Gewissen ein Sudoku lösen.</p>
<p class="small muted">Dieser Beitrag ersetzt keine ärztliche Beratung. Wenn du dir Sorgen um dein Gedächtnis oder das eines Angehörigen machst, sprich mit deiner Hausärztin oder deinem Hausarzt.</p>
<h2>Quellen</h2>
""" + _src([
    'Brooker H. et al. (2019): The relationship between the frequency of number-puzzle use and baseline cognitive function in a large online sample of adults aged 50 and over. International Journal of Geriatric Psychiatry 34, 932–940. <a href="https://doi.org/10.1002/gps.5085" rel="noopener">doi:10.1002/gps.5085</a>',
    'Brooker H. et al. (2019): An online investigation of the relationship between the frequency of word puzzle use and cognitive function in a large sample of older adults. International Journal of Geriatric Psychiatry 34, 921–931. <a href="https://doi.org/10.1002/gps.5033" rel="noopener">doi:10.1002/gps.5033</a>',
    'University of Exeter (2019): Pressemitteilung zu den PROTECT-Auswertungen. <a href="https://news-archive.exeter.ac.uk/2019/may/title_716265_en.html" rel="noopener">news-archive.exeter.ac.uk</a>',
    'Hall C. B. et al. (2009): Cognitive activities delay onset of memory decline in persons who develop dementia. Neurology 73, 356–361. <a href="https://doi.org/10.1212/WNL.0b013e3181b04ae3" rel="noopener">doi:10.1212/WNL.0b013e3181b04ae3</a>',
    'Rebok G. W. et al. (2014): Ten-Year Effects of the Advanced Cognitive Training for Independent and Vital Elderly Cognitive Training Trial on Cognition and Everyday Functioning in Older Adults. Journal of the American Geriatrics Society 62, 16–24. <a href="https://doi.org/10.1111/jgs.12607" rel="noopener">doi:10.1111/jgs.12607</a>',
    'National Institutes of Health (2014): Pressemitteilung zu den ACTIVE-Langzeitergebnissen. <a href="https://www.nih.gov/node/10476" rel="noopener">nih.gov</a>',
    'Simons D. J. et al. (2016): Do “Brain-Training” Programs Work? Psychological Science in the Public Interest 17, 103–186. <a href="https://doi.org/10.1177/1529100616661983" rel="noopener">doi:10.1177/1529100616661983</a>',
    'Sala G., Gobet F. (2017): Does Far Transfer Exist? Negative Evidence From Chess, Music, and Working Memory Training. Current Directions in Psychological Science 26, 515–520. <a href="https://doi.org/10.1177/0963721417712760" rel="noopener">doi:10.1177/0963721417712760</a>',
    'Gates N. J. et al. (2020): Computerised cognitive training for 12 or more weeks for maintaining cognitive function in cognitively healthy people in late life. Cochrane Database of Systematic Reviews. <a href="https://doi.org/10.1002/14651858.CD012277.pub3" rel="noopener">doi:10.1002/14651858.CD012277.pub3</a>',
    'Weltgesundheitsorganisation (2019): Risk reduction of cognitive decline and dementia: WHO guidelines. <a href="https://www.who.int/publications/i/item/9789241550543" rel="noopener">who.int</a>',
    'Livingston G. et al. (2024): Dementia prevention, intervention, and care: 2024 report of the Lancet standing Commission. The Lancet 404, 572–628. <a href="https://doi.org/10.1016/S0140-6736(24)01296-0" rel="noopener">doi:10.1016/S0140-6736(24)01296-0</a>',
    'Alzheimer Europe (2024): Zusammenfassung des Lancet-Berichts. <a href="https://www.alzheimer-europe.org/news/2024-lancet-commission-underscores-potential-dementia-risk-reduction-identifying-14-modifiable" rel="noopener">alzheimer-europe.org</a>',
    'Federal Trade Commission (2016): Lumosity to Pay $2 Million to Settle FTC Deceptive Advertising Charges for Its “Brain Training” Program. <a href="https://www.ftc.gov/news-events/press-releases/2016/01/lumosity-pay-2-million-settle-ftc-deceptive-advertising-charges" rel="noopener">ftc.gov</a>',
]),
},
{
"slug": "raetsel-ausdrucken-seniorenrunde-schule",
"title": "Rätsel ausdrucken für Seniorenrunde, Schule und Wartezimmer",
"teaser": "Welche Druckseite für wen passt, wie das Ausdrucken gut lesbar gelingt und wie eine Rätselrunde Spaß macht.",
"description": "Sudokus ausdrucken für Gruppen: welche Stufe für wen passt, Tipps für gut lesbaren Druck und Ideen für Seniorenrunde, Unterricht und Wartezimmer.",
"published": "2026-10-31",
"related": ["logikraetsel-mit-kindern", "denksport-und-gehirn", "sudoku-strategien"],
"body": """
<p>Ein Blatt Papier, ein Bleistift, ein Radiergummi – mehr braucht es nicht für eine gemeinsame Rätselrunde. Ausgedruckte Rätsel haben Vorteile, die ein Bildschirm nicht bietet: Man kann sie in die Mitte legen, gemeinsam darüber beugen, Notizen an den Rand schreiben und ohne Gerät mitnehmen. Dieser Beitrag hilft dir, die passenden Rätsel auszuwählen, sie gut lesbar auszudrucken und eine Runde so zu gestalten, dass alle mitkommen.</p>
<h2>Was es zum Ausdrucken gibt</h2>
<p>Auf Rätsellotse gibt es drei Druckseiten mit je sechs Sudokus und den Lösungen:</p>
<ul><li><a href="/sudoku-zum-ausdrucken-leicht.html">Sudoku zum Ausdrucken – leicht</a>: 38 Vorgaben. Nach unserer Auswertung lassen sich alle sechs allein mit der einfachsten Technik lösen – im leeren Feld nachsehen, welche Ziffer noch fehlt.</li>
<li><a href="/sudoku-zum-ausdrucken-mittel.html">Sudoku zum Ausdrucken – mittel</a>: 30 Vorgaben, weiterhin ohne Notizen lösbar, aber man muss öfter fragen: „Wo kann die 7 in diesem Block noch hin?“</li>
<li><a href="/sudoku-zum-ausdrucken-schwer.html">Sudoku zum Ausdrucken – schwer</a>: 25 bis 27 Vorgaben. Die Rätsel 3, 5 und 6 sind gut machbar; 1, 2 und 4 verlangen fortgeschrittene Techniken und sind eher etwas für erfahrene Rätselfreunde.</li></ul>
<p>Die Lösungen beginnen beim Drucken auf einer neuen Seite. So kannst du die Lösungsblätter getrennt aufbewahren oder erst am Ende austeilen.</p>
<h2>So druckst du gut lesbar</h2>
<ol><li><strong>Knopf „Drucken oder als PDF speichern“</strong> oben auf der Druckseite verwenden. Navigation und Werbung werden dabei automatisch ausgeblendet.</li>
<li><strong>Als PDF speichern</strong>, wenn du mehrere Kopien brauchst oder an einem anderen Drucker drucken willst – etwa im Copyshop oder im Sekretariat.</li>
<li><strong>Größer kopieren:</strong> Auf A4 stehen die Ziffern etwa in 12 bis 13 Punkt, also in normaler Lesegröße. Für Menschen mit eingeschränktem Sehvermögen lohnt es sich, das Blatt mit dem Kopierer von A4 auf A3 zu vergrößern (Einstellung 141 %). Die Ziffern liegen dann bei rund 18 Punkt. Zum Vergleich: Die Richtlinien der Europäischen Blindenunion für gut lesbare Drucksachen empfehlen 14 bis 18 Punkt, kontrastreiche Gestaltung und mattes Papier [1]; der britische Blindenverband RNIB bezeichnet 16 Punkt und mehr als Großdruck [2].</li>
<li><strong>Mattes Papier und kräftiger Druck:</strong> Glänzendes Papier spiegelt. Wenn der Drucker einen Sparmodus hat, besser ausschalten – die dünnen Linien im Gitter werden sonst blass.</li>
<li><strong>Bleistift statt Kuli:</strong> Beim Sudoku wird radiert. Ein weicher Bleistift (HB oder B) und ein guter Radiergummi ersparen Frust.</li></ol>
<h2>Die Seniorenrunde</h2>
<p>Viele Rätselrunden in Pensionistenklubs, Seniorentreffs oder Pflegeeinrichtungen leben weniger vom Rätsel als vom Miteinander. Ein paar Anregungen:</p>
<ul><li><strong>Mit „leicht“ beginnen</strong>, auch wenn einige mehr könnten. Ein gelöstes Rätsel motiviert mehr als ein halb gelöstes schweres.</li>
<li><strong>Zu zweit lösen lassen.</strong> Paare sprechen miteinander, erklären sich gegenseitig ihre Schritte und bleiben seltener stecken.</li>
<li><strong>Einen Schritt gemeinsam zeigen.</strong> Am Anfang ein großes Gitter auf Flipchart oder Tafel zeichnen und einen „einzigen Platz für eine Ziffer“ gemeinsam finden. Die Erklärung mit Diagrammen steht in den <a href="/sudoku-strategien.html">Sudoku-Strategien</a>.</li>
<li><strong>Kein Zeitdruck, keine Rangliste.</strong> Wer fertig ist, darf ein zweites Rätsel nehmen oder anderen helfen.</li>
<li><strong>Vom Erfolg erzählen lassen.</strong> „Wie bist du auf die 8 gekommen?“ ist die beste Frage einer Rätselrunde.</li></ul>
<p>Rätseln ist dabei vor allem eine schöne Beschäftigung in Gesellschaft. Was Studien zur geistigen Fitness tatsächlich sagen – und was nicht –, haben wir im Beitrag <a href="/denksport-und-gehirn.html">Denksport und Gehirn</a> zusammengefasst. Bitte versprich den Teilnehmenden keinen Schutz vor Demenz; dafür gibt es keine Belege.</p>
<h2>In der Schule</h2>
<p>Logikrätsel passen gut in den Unterricht, weil sie Begründen üben: Jede Ziffer im Sudoku muss sich erklären lassen. Einige Ideen:</p>
<ul><li><strong>Fünf-Minuten-Einstieg mit Zielzahl:</strong> Die <a href="/zielzahl.html">Zielzahl</a> des Tages an die Tafel schreiben, die Klasse in Gruppen rechnen lassen und Lösungswege vergleichen. Oft gibt es mehrere – eine schöne Gelegenheit, über Rechenwege zu sprechen. Rechentricks dazu stehen in den <a href="/zielzahl-tipps.html">Zielzahl-Tipps</a>.</li>
<li><strong>Codeknacker als Klassenspiel:</strong> Die Lehrkraft denkt sich einen Code aus vier verschiedenen Ziffern von 1 bis 6 aus, die Klasse tippt gemeinsam, die Lehrkraft gibt die Punkte an der Tafel. Jeder Vorschlag muss begründet werden – das trainiert genaues Schließen. Eine Beispielpartie steht in der <a href="/codeknacker-anleitung.html">Codeknacker-Anleitung</a>.</li>
<li><strong>Sudoku als Freiarbeit:</strong> Die leichte Stufe eignet sich zum Kennenlernen, die mittlere als Herausforderung. Lösungsblätter zur Selbstkontrolle auslegen.</li>
<li><strong>Für Jüngere:</strong> Mini-Sudokus mit 4×4 Feldern und kleine Nonogramme stehen in <a href="/logikraetsel-mit-kindern.html">Logikrätsel mit Kindern lösen</a>.</li></ul>
<h2>Im Wartezimmer</h2>
<p>Ein Rätselblatt auf dem Tisch ist eine freundliche Alternative zu alten Zeitschriften. Damit es gut funktioniert:</p>
<ul><li><strong>Laminieren und abwischbare Stifte</strong> auslegen. So lässt sich ein Blatt viele Male verwenden; ein Tuch zum Abwischen gehört dazu.</li>
<li><strong>Nur leicht und mittel</strong> auslegen. Die Wartezeit ist meist kürzer als ein schweres Sudoku.</li>
<li><strong>Die Lösungen</strong> in einer Mappe daneben legen, damit niemand frustriert gehen muss.</li>
<li><strong>Einen Hinweis auf die Online-Version</strong> dazulegen – wer mitten im Rätsel aufgerufen wird, kann das <a href="/sudoku.html">Tagessudoku</a> später auf dem Handy weiterspielen.</li></ul>
<h2>Checkliste für die Vorbereitung</h2>
<ul><li>Pro Person ein Rätsel der passenden Stufe plus eines als Reserve – wer schnell fertig ist, will weitermachen.</li>
<li>Lösungsblätter getrennt drucken und erst am Ende austeilen oder für die Leitung behalten.</li>
<li>Bleistifte, Radiergummis und für Brillenträger eventuell eine Lupe bereitlegen.</li>
<li>Ein vergrößertes Gitter für die gemeinsame Erklärung vorbereiten, auf Flipchart oder als A3-Kopie.</li>
<li>Vorher selbst ein Rätsel lösen: Wer weiß, wo man hängen bleibt, kann gezielter helfen.</li></ul>
<h2>Mehr als sechs Rätsel gesucht?</h2>
<p>Die Druckseiten enthalten derzeit je sechs feste Rätsel. Für Abwechslung sorgen die täglichen Online-Rätsel: <a href="/sudoku.html">Sudoku</a> in drei Stufen, <a href="/nonogramm.html">Nonogramm</a>, <a href="/zielzahl.html">Zielzahl</a> und <a href="/codeknacker.html">Codeknacker</a>. </p>
<h2>Nachdruck in Vereins-, Schul- und Pfarrblättern</h2>
<p>Du darfst unsere Druckrätsel ohne Anfrage kostenlos in nichtkommerziellen Blättern abdrucken – etwa in der Vereinszeitung, der Schülerzeitung, im Pfarr- oder Gemeindeblatt oder im Rundbrief einer Seniorenrunde. Einzige Bedingung: Gib unter dem Rätsel die Quelle an, zum Beispiel „Rätsel: raetsellotse.de“. Für kommerzielle Zeitschriften, Bücher oder Werbematerial gilt diese Erlaubnis nicht; dafür erreichst du uns unter <a href="mailto:office@adstern.com">office@adstern.com</a>.</p>
<h2>Quellen</h2>
""" + _src([
    'Europäische Blindenunion (EBU): Richtlinien für gut lesbaren Druck (deutsche Fassung, Stand 2016), bereitgestellt vom Blinden- und Sehbehindertenverband Österreich. <a href="https://www.blindenverband.at/media/file/82_EBU-clear-print-guidelines_DEUTSCH.pdf" rel="noopener">blindenverband.at (PDF)</a>',
    'RNIB: What are the different font sizes such as clear print, large print and giant print? <a href="https://help.rnib.org.uk/help/daily-living/large-print-size" rel="noopener">help.rnib.org.uk</a>',
]),
},
{
"slug": "logikraetsel-mit-kindern",
"title": "Logikrätsel mit Kindern lösen",
"teaser": "Mini-Sudokus, ein Nonogramm zum Abmalen und Spielideen ohne Bildschirm – mit Tipps, wie Knobeln Spaß macht.",
"description": "Logikrätsel für Kinder: Mini-Sudoku 4×4, ein 5×5-Nonogramm, Codeknacker als Familienspiel und Tipps, wie gemeinsames Knobeln gelingt.",
"published": "2026-10-31",
"related": ["raetsel-ausdrucken-seniorenrunde-schule", "nonogramm-anleitung", "denksport-und-gehirn"],
"body": """
<p>Kinder lieben Rätsel – solange sie sich lösen lassen. Ein 9×9-Sudoku mit 25 Vorgaben ist für die meisten Volksschul- und Grundschulkinder zu viel. Mit kleineren Formaten und etwas Begleitung entdecken aber schon junge Kinder, wie befriedigend es ist, etwas durch Nachdenken herauszufinden. Dieser Beitrag enthält zwei Mini-Sudokus und ein Nonogramm zum Abmalen oder Ausdrucken, Spielideen ohne Bildschirm und Tipps für die Begleitung.</p>
<h2>Der richtige Einstieg</h2>
<p>Für den Anfang zählt nicht das Alter, sondern was ein Kind schon kann. Ein paar Anhaltspunkte:</p>
<ul><li><strong>Kann das Kind sicher bis 4 zählen und Ziffern erkennen?</strong> Dann passt ein Mini-Sudoku mit 4×4 Feldern. Statt Ziffern gehen auch vier Farben, Tiere oder Formen.</li>
<li><strong>Kann es Felder abzählen und Kästchen ausmalen?</strong> Dann passt ein kleines Nonogramm mit 5×5 Feldern.</li>
<li><strong>Kann es Hinweise im Kopf behalten und vergleichen?</strong> Dann macht Codeknacker als Familienspiel Spaß – am besten zuerst mit drei Stellen.</li>
<li><strong>Rechnet es sicher im Zahlenraum bis 100?</strong> Dann kann es bei einer vereinfachten Zielzahl mitmachen.</li></ul>
<h2>Mini-Sudoku: 4 × 4</h2>
<p>Die Regeln sind dieselben wie beim großen Sudoku, nur kleiner: In jeder Zeile, jeder Spalte und jedem der vier dick umrandeten 2×2-Blöcke muss jede Ziffer von 1 bis 4 genau einmal vorkommen. Beide Rätsel haben genau eine Lösung – das haben wir mit einem Programm geprüft.</p>
<figure class="wide">""" + FIG_KIDS_SUDOKU + """<figcaption>Mini-Sudoku 1 (acht Vorgaben) ist zum Einstieg, Mini-Sudoku 2 (sechs Vorgaben) etwas kniffliger. Zum Abmalen auf Karopapier: je vier mal vier Kästchen, die Blöcke dick umranden.</figcaption></figure>
<p>So kannst du beim ersten Rätsel helfen, ohne die Lösung zu verraten: Zeig auf die erste Zeile. „Hier stehen schon die 1 und die 3. Welche Zahlen fehlen noch?“ – „Die 2 und die 4.“ – „Schau mal in die Spalte unter dem zweiten Feld. Ist da schon eine 4?“ So lernt das Kind, Zeile und Spalte gleichzeitig zu betrachten – die wichtigste Idee jedes Sudokus.</p>
<p class="small muted">Lösung 1: 1 2 3 4 · 3 4 1 2 · 2 1 4 3 · 4 3 2 1. Lösung 2: 2 4 1 3 · 1 3 2 4 · 4 1 3 2 · 3 2 4 1 (jeweils Zeile für Zeile).</p>
<h2>Nonogramm: ein Bild aus Zahlen</h2>
<p>Nonogramme sind für Kinder besonders reizvoll, weil am Ende ein Bild entsteht. Die Zahlen am Rand sagen, wie viele Kästchen in dieser Zeile oder Spalte nebeneinander ausgemalt werden. Stehen zwei Zahlen da, gibt es zwei Gruppen mit mindestens einem leeren Kästchen dazwischen.</p>
<figure class="wide">""" + FIG_KIDS_NONO + """<figcaption>Links das Rätsel, rechts die Lösung (am besten abdecken). Es lässt sich ohne Raten lösen.</figcaption></figure>
<p>Ein guter Startpunkt ist die Zeile mit der 5: Sie ist ganz voll. Danach helfen die Spalten mit der 4 – in fünf Kästchen muss ein Viererblock die mittleren drei Kästchen sicher abdecken. Erkläre dem Kind ruhig den Trick mit dem Hin- und Herschieben: Wenn ein Block ganz links und ganz rechts liegen kann, ist die Mitte immer dabei. Ältere Kinder können danach das 5×5-Tagesrätsel im <a href="/nonogramm.html">Nonogramm</a> probieren; die Anleitung mit einem weiteren Beispiel steht in <a href="/nonogramm-anleitung.html">Nonogramme lösen</a>.</p>
<h2>Codeknacker als Familienspiel</h2>
<p>Codeknacker funktioniert wunderbar mit Papier und Bleistift. Ein Erwachsener denkt sich einen Code aus und schreibt ihn verdeckt auf. Für den Einstieg reichen <strong>drei verschiedene Ziffern von 1 bis 4</strong> – das ergibt 24 mögliche Codes statt 360. Nach jedem Tipp gibt es Rückmeldung:</p>
<ul><li>ein Häkchen für jede Ziffer, die stimmt und am richtigen Platz steht,</li>
<li>einen Kreis für jede Ziffer, die vorkommt, aber woanders hingehört.</li></ul>
<p>Wichtig ist, nicht zu verraten, welche Ziffer gemeint ist – genau das macht das Rätsel aus. Wer den Code knackt, darf sich den nächsten ausdenken. Kinder lernen dabei schnell, dass jeder Tipp eine Frage ist: „Wenn ich die 4 weglasse und die Zahl der Kreise gleich bleibt, was heißt das?“ Später kann man auf vier Stellen wechseln und den <a href="/codeknacker.html">Codeknacker</a> des Tages gemeinsam spielen.</p>
<h2>Zielzahl in der Familienversion</h2>
<p>Für Kinder lässt sich die <a href="/zielzahl.html">Zielzahl</a> vereinfachen: Nehmt vier Zahlenkarten von 1 bis 10 und eine Zielzahl unter 50. Erlaubt sind zuerst nur Plus und Minus, später auch Mal. Beispiel: Mit 2, 5, 7 und 9 sollen 23 herauskommen – zum Beispiel 9 + 7 + 5 + 2 = 23, oder eleganter 2 × 9 + 5 = 23. Es gibt oft mehrere Wege, und genau darüber zu reden ist der eigentliche Gewinn.</p>
<h2>Sieben Tipps für die Begleitung</h2>
<ol><li><strong>Laut denken – du zuerst.</strong> Sag, was du überlegst: „Hier fehlt noch die 3, aber in dieser Spalte ist schon eine.“ Kinder übernehmen solche Denkweisen durch Zuhören.</li>
<li><strong>Fragen statt sagen.</strong> „Was weißt du schon sicher?“ hilft mehr als „Da gehört die 2 hin“.</li>
<li><strong>Fehler sind Information.</strong> Wenn eine Zeile nicht aufgeht, ist das kein Versagen, sondern ein Hinweis, wo man nachschauen muss. Ein Radiergummi gehört dazu.</li>
<li><strong>Kurz halten.</strong> Lieber ein Rätsel lösen und aufhören, solange es noch Spaß macht, als drei anfangen.</li>
<li><strong>Erfolg sichtbar machen.</strong> Gelöste Rätsel aufhängen oder in einer Mappe sammeln.</li>
<li><strong>Das Kind erklären lassen.</strong> Wer einen Lösungsweg erklären kann, hat ihn verstanden – und ist zu Recht stolz darauf.</li>
<li><strong>Nicht vergleichen.</strong> Geschwister lösen unterschiedlich schnell. Jedes Kind braucht sein eigenes Tempo und seine eigene Stufe.</li></ol>
<h2>Papier oder Bildschirm?</h2>
<p>Die Rätsel auf Rätsellotse lassen sich online spielen, aber gerade mit jüngeren Kindern spricht viel für Papier: Man sitzt nebeneinander, zeigt mit dem Finger und kann Notizen machen. Die deutsche Bundeszentrale für gesundheitliche Aufklärung empfiehlt als Richtwerte für alle Bildschirmmedien zusammen höchstens 30 Minuten pro Tag für Kinder von 3 bis 6 Jahren und höchstens 45 Minuten für Kinder von 6 bis 9 Jahren [1]. Ein ausgedrucktes Rätsel muss sich diese Zeit nicht teilen. Wie du unsere Sudokus gut lesbar druckst, steht in <a href="/raetsel-ausdrucken-seniorenrunde-schule.html">Rätsel ausdrucken für Seniorenrunde, Schule und Wartezimmer</a>.</p>
<p>Macht Rätseln Kinder klüger? Ehrlich gesagt: Dafür gibt es keine guten Belege. Gut belegt ist, dass man durch Übung besser in dem wird, was man übt – mehr dazu in <a href="/denksport-und-gehirn.html">Denksport und Gehirn</a>. Der Wert gemeinsamen Knobelns liegt woanders: in der Zeit miteinander, im Erlebnis „Ich habe es selbst herausgefunden“ und in der Erfahrung, dass sich Dranbleiben lohnt.</p>
<h2>Quelle</h2>
""" + _src([
    'Bundeszentrale für gesundheitliche Aufklärung (BZgA), kindergesundheit-info.de: Empfehlungen zur Dauer der Mediennutzung. <a href="https://www.kindergesundheit-info.de/fileadmin/user_upload/kindergesundheit-info.de/Download/Medienumgang/Empfehlungen-Dauer-Mediennutzung_BZgA_kindergesundheit-info.pdf" rel="noopener">kindergesundheit-info.de (PDF)</a>',
]),
},
]
