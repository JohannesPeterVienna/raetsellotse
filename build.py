"""Erzeugt Rätsellotse als statische Website in docs/ (GitHub Pages)."""
import random, shutil, sys
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
sys.path.insert(0, str(Path(__file__).parent))
from content.articles import ARTICLES
from content import gamepages as GP

ROOT = Path(__file__).parent; OUT = ROOT / "docs"
SITE = "https://raetsellotse.de"; V = "20261105d"; UPDATED = "Oktober 2026"
NAV = [("/", "Heute"), ("/codeknacker.html", "Codeknacker"), ("/sudoku.html", "Sudoku"), ("/zielzahl.html", "Zielzahl"), ("/nonogramm.html", "Nonogramm"),
       ("/raetselblatt.html", "Zum Ausdrucken"), ("/archiv.html", "Meine Statistik")]
env = Environment(loader=FileSystemLoader(ROOT / "templates"), autoescape=True, trim_blocks=True, lstrip_blocks=True)
PAGES = []
BY = {a["slug"]: a for a in ARTICLES}
REVIEWED = "2026-11-02"; REVIEWED_TEXT = "2. November 2026"   # letzte redaktionelle Prüfung aller Beiträge
CONTENT_UPDATED = "2026-11-04"   # letzte inhaltliche Änderung von Startseite, Spielseiten und „Über“ (sitemap lastmod)
LOADER = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7811071715414905" crossorigin="anonymous"></script>'
LEGAL_ADDR = "AdStern – Agentur für digitales Marketing<br>Seilerstätte 8/8, 1010 Wien, Österreich<br>E-Mail: <a href='mailto:office@adstern.com'>office@adstern.com</a><br>Web: <a href='https://www.adstern.com'>www.adstern.com</a>"


def write(path, template, **ctx):
    base = dict(site=SITE, v=V, updated=UPDATED, nav=NAV, active=ctx.get("active", "/" + path), jsonld=[], ads=True, robots=None, og_title=None)
    base.update(ctx); base["path"] = "/" if path == "index.html" else "/" + path
    (OUT / path).write_text(env.get_template(template).render(**base), encoding="utf-8")
    if base.get("robots") is None: PAGES.append((base["path"], ctx.get("priority", 0.6), ctx.get("lastmod", "2026-10-29")))


def crumbs_ld(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + h} for i, (h, n) in enumerate(items)]}


# ---------------- Sudoku-Generator (für Druckseiten) ----------------
PEERS = []
for i in range(81):
    r, c = divmod(i, 9); s = set()
    for k in range(9): s.add(r * 9 + k); s.add(k * 9 + c)
    br, bc = r - r % 3, c - c % 3
    for a in range(3):
        for b in range(3): s.add((br + a) * 9 + bc + b)
    s.discard(i); PEERS.append(sorted(s))
UNITS = [[k * 9 + j for j in range(9)] for k in range(9)] + [[j * 9 + k for j in range(9)] for k in range(9)] + \
        [[(br + j // 3) * 9 + bc + j % 3 for j in range(9)] for br in (0, 3, 6) for bc in (0, 3, 6)]


def cands(g, i):
    if g[i]: return []
    used = {g[p] for p in PEERS[i]}
    return [d for d in range(1, 10) if d not in used]


def count(g, limit=2):
    a = g[:]; n = [0]
    def go():
        if n[0] >= limit: return
        best, bc = -1, None
        for i in range(81):
            if not a[i]:
                c = cands(a, i)
                if not c: return
                if bc is None or len(c) < len(bc):
                    best, bc = i, c
                    if len(c) == 1: break
        if best < 0: n[0] += 1; return
        for d in bc:
            a[best] = d; go()
            if n[0] >= limit: break
        a[best] = 0
    go(); return n[0]


def singles(g):
    a = g[:]; prog = True
    while prog:
        prog = False
        for i in range(81):
            if not a[i]:
                c = cands(a, i)
                if len(c) == 1: a[i] = c[0]; prog = True
        for u in UNITS:
            for d in range(1, 10):
                if any(a[i] == d for i in u): continue
                pos = [i for i in u if not a[i] and d in cands(a, i)]
                if len(pos) == 1: a[pos[0]] = d; prog = True
    return all(a)


def make(seed, level):
    r = random.Random(seed); g = [0] * 81
    def fill(i):
        if i == 81: return True
        c = cands(g, i); r.shuffle(c)
        for d in c:
            g[i] = d
            if fill(i + 1): return True
        g[i] = 0; return False
    fill(0); sol = g[:]
    target = {"leicht": 38, "mittel": 30, "schwer": 25}[level]
    order = list(range(81)); r.shuffle(order); givens = 81
    for i in order:
        if givens <= target: break
        v = g[i]; g[i] = 0
        if count(g) != 1 or (level in ("leicht", "mittel") and not singles(g)): g[i] = v
        else: givens -= 1
    return g, sol


def table(g, cls="ps"):
    rows = "".join("<tr>" + "".join(f"<td>{g[r*9+c] or ''}</td>" for c in range(9)) + "</tr>" for r in range(9))
    return f'<table class="{cls}" aria-label="Sudoku">{rows}</table>'


# ---------------- Spiel-Oberflächen ----------------
UI_CODE = """<div class="daynav" data-daynav></div><div class="board" data-board></div>
<div class="pad" data-pad>""" + "".join(f'<button type="button" data-d="{d}" aria-label="Ziffer {d}">{d}</button>' for d in range(1, 7)) + \
"""<button type="button" class="wide" data-back>Löschen</button><button type="button" class="btn" data-ok>Prüfen</button></div>
<p class="msg" data-msg aria-live="polite"></p><noscript><p>Für das Spiel wird JavaScript benötigt.</p></noscript>"""
UI_SUDOKU = """<div class="daynav" data-daynav></div>
<label class="small no-print">Schwierigkeit <select data-level><option value="leicht">leicht</option><option value="mittel">mittel</option><option value="schwer">schwer</option></select></label>
<div class="sgrid" data-grid role="grid" aria-label="Sudoku" style="margin-top:12px"></div>
<div class="pad" data-pad>""" + "".join(f'<button type="button" data-d="{d}">{d}</button>' for d in range(1, 10)) + \
"""<button type="button" class="wide" data-notes aria-pressed="false">Notizen</button><button type="button" class="wide" data-erase>Löschen</button><button type="button" class="wide" data-hint>Tipp</button></div>
<p class="msg" data-msg aria-live="polite"></p><noscript><p>Für das Spiel wird JavaScript benötigt. <a href="/sudoku-zum-ausdrucken-mittel.html">Sudokus zum Ausdrucken</a></p></noscript>"""
UI_NONO = """<div class="daynav" data-daynav></div>
<label class="small no-print">Größe <select data-size><option value="5">5 × 5 (Einstieg)</option><option value="10">10 × 10</option><option value="15">15 × 15</option></select></label>
<div class="ngrid-wrap"><div class="ngrid" data-ngrid role="grid" aria-label="Nonogramm"></div></div>
<div class="pad"><button type="button" class="wide" data-mode="1" aria-pressed="true">■ Füllen</button><button type="button" class="wide" data-mode="2" aria-pressed="false">✕ Kreuz</button><button type="button" class="wide" data-ncheck>Prüfen</button><button type="button" class="wide" data-nhint>Tipp</button><button type="button" class="wide" data-nreset>Neu beginnen</button></div>
<p class="msg" data-msg aria-live="polite"></p><noscript><p>Für das Spiel wird JavaScript benötigt.</p></noscript>"""
UI_ZIEL = """<div class="daynav" data-daynav></div>
<div class="small muted">Zielzahl</div><div class="target" data-target>…</div>
<div class="tiles" data-nums aria-label="Verfügbare Zahlen – antippen zum Einfügen"></div>
<input class="expr" data-expr inputmode="text" autocomplete="off" placeholder="z. B. (100 + 6) × 4 − 9" aria-label="Deine Rechnung">
<div class="pad"><button type="button" class="btn" data-check>Rechnen</button><button type="button" class="btn ghost" data-solve>Lösung zeigen</button></div>
<p class="msg" data-msg aria-live="polite"></p><p data-solution></p>"""


def main():
    import subprocess
    subprocess.run(["node", "--test", str(ROOT / "test_consent.js")], check=True, capture_output=True)   # Einwilligung/Loader-Test
    if OUT.exists(): shutil.rmtree(OUT)
    (OUT / "assets").mkdir(parents=True)
    for f in (ROOT / "assets").iterdir(): shutil.copy(f, OUT / "assets" / f.name)

    write("index.html", "home.html", title="Rätsellotse – tägliche Rätsel: Sudoku, Nonogramm, Codeknacker & Zielzahl",
          description="Jeden Tag neue Logikrätsel: Sudoku in drei Stufen, Nonogramm, Codeknacker und Zielzahl. Kostenlos, ohne Anmeldung, mit Archiv, Statistik und erklärten Tipps.",
          articles=ARTICLES, priority=1.0, active="/", lastmod=CONTENT_UPDATED,
          jsonld=[{"@context": "https://schema.org", "@type": "WebSite", "name": "Rätsellotse", "url": SITE + "/", "inLanguage": "de"}])

    games = [
        ("codeknacker", "Codeknacker", "Codeknacker – das tägliche Logikrätsel mit Zahlencode",
         "Knacke jeden Tag einen neuen vierstelligen Zahlencode mit Logik: zehn Versuche, Hinweise nach jedem Tipp, Archiv und Serienzähler.",
         "Vier verschiedene Ziffern von 1 bis 6, zehn Versuche. Orange heißt: richtig platziert. Weiß: richtige Ziffer, falsche Stelle.",
         UI_CODE, ["codeknacker-anleitung"],
         "<h2>Kurz erklärt</h2><p>Tippe vier verschiedene Ziffern und drücke Prüfen – oder nutze die Tastatur (1–6, Enter, Rücktaste). Nach jedem Versuch zeigen die Punkte, wie nah du dran bist. Die ausführlichen Regeln und eine Strategie findest du in der <a href='/codeknacker-anleitung.html'>Anleitung</a>.</p><p>Jeden Tag gibt es einen neuen Code, für alle derselbe. Ältere Rätsel öffnest du über das Archiv oben im Spielfeld.</p>"),
        ("sudoku", "Sudoku", "Sudoku online – täglich neu, leicht bis schwer, mit Tipps",
         "Tägliches Sudoku online spielen: drei Schwierigkeitsstufen, Notizen, erklärte Tipps, Archiv – kostenlos und ohne Anmeldung.",
         "Jeden Tag drei neue Sudokus – leicht, mittel und schwer. Jedes hat genau eine Lösung, und die Tipps erklären den nächsten Schritt mit den Grundtechniken.",
         UI_SUDOKU, ["sudoku-strategien", "sudoku-regeln-und-geschichte"],
         "<h2>Bedienung</h2><ul><li>Feld antippen, dann Ziffer wählen – oder Pfeiltasten und Zifferntasten.</li><li><strong>Notizen</strong> (Taste N) schaltet auf kleine Kandidaten-Ziffern um.</li><li><strong>Tipp</strong> zeigt zuerst falsche Einträge, sonst einen Schritt mit den Grundtechniken samt Erklärung; bei schweren Sudokus deckt er notfalls ein Feld ohne Begründung auf.</li></ul><p>Leichte und mittlere Sudokus lassen sich mit den beiden einfachsten Techniken lösen; schwere haben weniger Vorgaben und können mehr verlangen. Mehr dazu in den <a href='/sudoku-strategien.html'>Sudoku-Strategien</a>.</p>"),
        ("zielzahl", "Zielzahl", "Zielzahl – das tägliche Rechenrätsel mit sechs Zahlen",
         "Triff jeden Tag eine neue Zielzahl mit sechs Zahlen und den vier Grundrechenarten. Kopfrechnen trainieren – kostenlos, mit Lösungsweg.",
         "Erreiche die Zielzahl mit + − × ÷. Jede Zahl höchstens einmal, Teilen nur ohne Rest. Jede Aufgabe ist garantiert lösbar.",
         UI_ZIEL, ["zielzahl-tipps"],
         "<h2>So rechnest du</h2><p>Tippe die Zahlen an oder schreib die Rechnung direkt ins Feld, zum Beispiel (75 + 25) × 6 − 9. Klammern sind erlaubt, Malpunkt und Doppelpunkt ebenfalls. Kommst du nicht weiter, zeigt „Lösung zeigen“ einen möglichen Weg.</p><p>Strategien für schnelles Kopfrechnen findest du in den <a href='/zielzahl-tipps.html'>Zielzahl-Tipps</a>.</p>"),
    ]
    games.append(("nonogramm", "Nonogramm", "Nonogramm online – tägliches Malrätsel (Picross) in drei Größen",
         "Jeden Tag ein neues Nonogramm online lösen: 5×5, 10×10 oder 15×15, eindeutig und ohne Raten lösbar, mit erklärten Tipps – kostenlos.",
         "Fülle die Felder so, dass die Zahlen am Rand stimmen – und ein Bild entsteht. Jeden Tag neu, garantiert ohne Raten lösbar.",
         UI_NONO, ["nonogramm-anleitung", "wie-unsere-raetsel-entstehen"], ""))
    BODY = {"codeknacker": GP.CODE, "sudoku": GP.SUDOKU, "zielzahl": GP.ZIEL, "nonogramm": GP.NONO}
    games = [(g[0], g[1], g[2], g[3], g[4], g[5], g[6] + (["wie-unsere-raetsel-entstehen"] if g[0] != "nonogramm" else []), BODY[g[0]]) for g in games]
    for slug, name, title, desc, lead, ui, rel, body in games:
        crumbs = [("/", "Rätsellotse"), (f"/{slug}.html", name)]
        ld = [crumbs_ld(crumbs), {"@context": "https://schema.org", "@type": "WebApplication", "name": f"{name} – Rätsellotse", "url": f"{SITE}/{slug}.html",
              "applicationCategory": "GameApplication", "operatingSystem": "Web", "inLanguage": "de", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"}}]
        write(f"{slug}.html", "game.html", title=(f"{title} | Rätsellotse" if len(title) < 50 else title), description=desc, h1=name, lead=lead, ui=ui, game=slug,
              body=body, related=[BY[s] for s in rel], crumbs=crumbs, jsonld=ld, priority=0.9, lastmod=CONTENT_UPDATED)

    for level, intro in (("leicht", "Für Einsteiger: viele Vorgaben, lösbar allein mit den beiden einfachsten Techniken."),
                         ("mittel", "Weniger Vorgaben, aber weiterhin ohne Raten mit einfachen Techniken lösbar."),
                         ("schwer", "Nur rund 25 Vorgaben – hier braucht es Überblick und teils fortgeschrittene Techniken.")):
        puzzles = [make(f"druck-{level}-2026-{k}", level) for k in range(6)]
        grid = "".join(f"<div><h3 style='margin:0 0 6px'>Sudoku {k+1}</h3>{table(p)}</div>" for k, (p, s) in enumerate(puzzles))
        sols = "".join(f"<div><h3 style='margin:0 0 6px;font-size:.9rem'>Lösung {k+1}</h3>{table(s, 'ps sol')}</div>" for k, (p, s) in enumerate(puzzles))
        others = " · ".join(f"<a href='/sudoku-zum-ausdrucken-{l}.html'>{l}</a>" for l in ("leicht", "mittel", "schwer") if l != level)
        before, after = GP.PRINT_TEXT[level]
        body = (f"<div class='no-print'>{before}</div>"
                f"<p class='no-print'><button class='btn' type='button' onclick='print()'>Drucken oder als PDF speichern</button></p>"
                f"<div class='printgrid'>{grid}</div><h2 style='break-before:page'>Lösungen</h2><div class='printgrid'>{sols}</div>"
                f"<h2 class='no-print'>Andere Schwierigkeiten</h2><p class='no-print'>{others} · <a href='/sudoku.html'>Tagessudoku online spielen</a></p>"
                f"<div class='no-print'>{after}</div>"
                "<p class='small muted no-print'>Jedes Sudoku hat genau eine Lösung. Beim Drucken werden Navigation, Werbung und Erklärungen ausgeblendet; Lösungen beginnen auf einer neuen Seite.</p>")
        crumbs = [("/", "Rätsellotse"), (f"/sudoku-zum-ausdrucken-{level}.html", f"Sudoku zum Ausdrucken ({level})")]
        write(f"sudoku-zum-ausdrucken-{level}.html", "page.html", title=f"Sudoku zum Ausdrucken – {level}: 6 Rätsel mit Lösungen",
              description=f"Sechs Sudokus zum Ausdrucken, Schwierigkeit {level}, mit Lösungen auf separater Seite. Kostenlos drucken oder als PDF speichern.",
              h1=f"Sudoku zum Ausdrucken: {level}", lead=intro, body=body, crumbs=crumbs, jsonld=[crumbs_ld(crumbs)],
              active="/raetselblatt.html", priority=0.8)

    for a in ARTICLES:
        crumbs = [("/", "Rätsellotse"), ("/" + a["slug"] + ".html", a["title"])]
        ld = [crumbs_ld(crumbs), {"@context": "https://schema.org", "@type": "Article", "headline": a["title"], "description": a["description"], "inLanguage": "de",
              "datePublished": a.get("published", "2026-10-29"), "dateModified": REVIEWED, "author": {"@type": "Organization", "name": "AdStern – Agentur für digitales Marketing", "url": SITE + "/about.html"},
              "publisher": {"@type": "Organization", "name": "AdStern – Agentur für digitales Marketing"}}]
        write(a["slug"] + ".html", "page.html", title=(f"{a['title']} | Rätsellotse" if len(a['title']) < 50 else a['title']), description=a["description"], h1=a["title"], lead=a["teaser"],
              reviewed=REVIEWED_TEXT,
              body=a["body"], crumbs=crumbs, related=[BY[s] for s in a.get("related", [])] or [x for x in ARTICLES if x["slug"] != a["slug"]][:3],
              jsonld=ld, priority=0.7, lastmod=REVIEWED)

    crumbs = [("/", "Rätsellotse"), ("/raetselblatt.html", "Rätselblatt")]
    write("raetselblatt.html", "game.html", title="Rätselblatt zum Ausdrucken – Sudoku, Nonogramm, Zielzahl",
          description="Jeden Tag ein neues Rätselblatt: Sudoku, Nonogramm und Zielzahl des Tages auf einer A4-Seite – kostenlos drucken oder als PDF speichern.",
          h1="Rätselblatt des Tages", lead="Sudoku, Nonogramm und Zielzahl von heute auf einem A4-Blatt – für Bleistift, Kaffee und die Zeitungsrunde.",
          ui="", game="blatt", body="<h2>So nutzt du das Rätselblatt</h2><p>Das Blatt entsteht jeden Tag neu aus denselben Aufgaben wie die Online-Rätsel. Drucke es aus oder speichere es über den Druckdialog als PDF. Die Lösungen findest du online beim jeweiligen Rätsel – so kannst du auf Papier rätseln und am Bildschirm vergleichen.</p><p>Über den Link „Link zu diesem Tag“ lässt sich jedes Blatt später wieder aufrufen, etwa für die Rätselrunde im Seniorenclub oder in der Schule.</p>",
          related=[BY[s] for s in ("raetsel-ausdrucken-seniorenrunde-schule", "sudoku-strategien") if s in BY], crumbs=crumbs, jsonld=[crumbs_ld(crumbs)], priority=0.8)
    write("archiv.html", "page.html", title="Meine Statistik & Rätsel-Archiv | Rätsellotse", description="Deine Serien, Erfolgsquoten und alle Rätsel der letzten 30 Tage zum Nachspielen.",
          h1="Meine Statistik & Archiv", lead="Serien, Quoten und die Rätsel der letzten 30 Tage – verpasste Tage einfach nachspielen.", ads=False, robots="noindex,follow",
          body="""<section data-game="archiv"><div class="stats" data-stats><p class="muted">Statistik wird geladen …</p></div>
<h2>Die letzten 30 Tage</h2><p class="small muted">✓ gelöst · ◐ begonnen · ✗ nicht gelöst · – noch offen. Antippen zum (Nach-)Spielen. Sudoku: leicht, mittel, schwer · Nonogramm: 10 × 10.</p>
<div class="scroll"><table class="tbl arch"><thead><tr><th scope="col">Tag</th><th scope="col">Code</th><th scope="col">Sudoku</th><th scope="col">Ziel</th><th scope="col">Nono</th></tr></thead><tbody data-days></tbody></table></div>
<p class="small muted" style="margin-top:18px">Alle Werte stehen nur in deinem Browser (lokaler Speicher) und werden nicht übertragen. Auf einem anderen Gerät beginnst du von vorn. <button type="button" class="linkbtn" data-reset>Statistik zurücksetzen</button></p></section>""")

    write("about.html", "page.html", title="Über Rätsellotse", description="Wer hinter Rätsellotse steht und wie die Rätsel entstehen.",
          h1="Über Rätsellotse", lead="Täglich frische Rätsel – fair, eindeutig lösbar und ohne Anmeldung.", priority=0.3, lastmod=CONTENT_UPDATED,
          body="""<p>Rätsellotse ist ein Projekt der Wiener Agentur AdStern. Jeden Tag erscheinen neue Rätsel – Codeknacker, Sudoku in drei Stufen, Zielzahl und Nonogramm in drei Größen –, für alle Spielerinnen und Spieler dieselben. Die Idee: eine kurze, faire Knobelpause, die man mit anderen vergleichen kann, ohne Konto und ohne Zeitdruck.</p>
<h2>Unsere Grundsätze</h2>
<ul><li><strong>Fair:</strong> Jedes Rätsel ist eindeutig lösbar. Nonogramme lassen sich ohne Raten lösen, Sudokus der Stufen leicht und mittel mit einfachen Techniken, schwere teils nur mit fortgeschrittenen Techniken; jede Zielzahl ist nachweislich erreichbar.</li>
<li><strong>Erklärt:</strong> Die Tipp-Funktionen verraten nicht einfach die Lösung, sondern begründen den nächsten logischen Schritt. Einzige Ausnahme: Kommt man bei einem schweren Sudoku mit den Grundtechniken nicht weiter, deckt der Tipp ein Feld auf, ohne es zu erklären.</li>
<li><strong>Ohne Anmeldung:</strong> Fortschritt, Serien und Statistik bleiben in deinem Browser.</li>
<li><strong>Für alle Geräte:</strong> Alle Rätsel funktionieren mit Maus, Tastatur und Touchscreen.</li></ul>
<h2>Wie die Rätsel entstehen</h2><p>Die Rätsel werden von einem Programm erzeugt und automatisch geprüft, bevor sie erscheinen. Der Zufall hängt vom Datum ab – deshalb bekommen alle am selben Tag dasselbe Rätsel, und das Archiv kann jeden vergangenen Tag exakt wiederherstellen. Die Details erklärt der Beitrag <a href="/wie-unsere-raetsel-entstehen.html">Wie unsere Rätsel entstehen</a>.</p>
<h2>KI-Werkzeuge und Prüfung</h2><p>Die Texte entstehen mit Unterstützung von KI-Werkzeugen; jedes Rätsel ist durch automatisierte Prüfprogramme abgesichert, und jeder Text wird vor der Veröffentlichung in einem eigenen Prüfdurchgang gegen die verlinkten Quellen geprüft. Ein Redaktionsteam gibt es nicht; verantwortlich ist AdStern.</p>
<h2>Deine Daten</h2><p>Fortschritt und Serien speichern wir nur in deinem Browser. Es gibt kein Konto und keine Bestenliste mit persönlichen Daten. Die Besucherstatistik (Google Analytics) läuft nur, wenn du im Einwilligungsfenster zustimmst. Auch personalisierte Anzeigen erscheinen nur mit deiner Einwilligung. Stimmst du nicht zu, kann Google eingeschränkte, nicht personalisierte Anzeigen ausliefern, die ohne Werbe-Cookies auskommen; ist in deinem Browser „Global Privacy Control“ aktiv, halten wir alle Anzeigenanfragen an und befüllen keine Werbeplätze. Was genau dabei passiert, erklärt die <a href="/privacy.html">Datenschutzerklärung</a>.</p>
<h2>Wer dahintersteht</h2><p>Betrieben wird Rätsellotse von AdStern – Agentur für digitales Marketing mit Sitz in der Seilerstätte 8/8 in 1010 Wien. AdStern entwickelt die Rätselprogramme, schreibt die Anleitungen und Beiträge und ist für alle Inhalte verantwortlich. Die vollständigen Angaben stehen im <a href="/imprint.html">Impressum</a>.</p>
<h2>Was es hier gibt</h2><p>Herzstück sind die vier Tagesrätsel. Dazu kommen drei Druckseiten mit je sechs Sudokus samt Lösungen in den Stufen <a href="/sudoku-zum-ausdrucken-leicht.html">leicht</a>, <a href="/sudoku-zum-ausdrucken-mittel.html">mittel</a> und <a href="/sudoku-zum-ausdrucken-schwer.html">schwer</a>, und eine Reihe von Beiträgen: Anleitungen und Strategien zu jedem Rätsel, Hintergrund zur Mathematik hinter dem Codeknacker und zu schweren Sudokus, ein nüchterner Blick auf die Forschung zu Denksport und Gehirn sowie praktische Tipps für Rätselrunden mit Kindern, in der Schule oder im Seniorentreff. Alle Beiträge sind über die <a href="/">Startseite</a> erreichbar.</p>
<h2>Wie wir Inhalte prüfen</h2><p>Für die Rätsel selbst übernehmen Prüfprogramme die Kontrolle: Sie stellen sicher, dass jedes Sudoku und jedes Nonogramm genau eine Lösung hat und jede Zielzahl erreichbar ist. Aussagen über bestimmte Rätsel – etwa welche Techniken die Sudokus auf den Druckseiten verlangen – haben wir mit einem Löseprogramm nachgeprüft, und die Beispielrätsel auf den Spielseiten sind vollständig nachgerechnet. Jeder Beitrag trägt das Datum seiner letzten Prüfung; wo wir uns auf Studien oder Fachstellen stützen, nennen wir die Quellen am Ende des Beitrags.</p>
<h2>Werbung auf Rätsellotse</h2><p>Rätsellotse ist kostenlos und finanziert sich über Anzeigen von Google. Werbeplätze sind mit „Werbung“ gekennzeichnet. Unsere festen Werbeplätze stehen nie neben dem Spielfeld oder den Bedienknöpfen, damit niemand beim Knobeln versehentlich auf eine Anzeige tippt. Zusätzlich kann Google Anzeigen automatisch platzieren. Die Rätsel, Tipps und Lösungen funktionieren unabhängig davon, ob du der Werbung zustimmst.</p>
<h2>Ergebnisse teilen, ohne zu spoilern</h2><p>Nach dem Lösen kannst du dein Ergebnis teilen. Verschickt wird nur, was nichts verrät: beim Codeknacker die farbigen Punkte deiner Versuche, beim Sudoku die Stufe und beim Nonogramm die Größe, jeweils mit der Zahl der genutzten Tipps, bei der Zielzahl, dass du sie getroffen hast. Die Lösung selbst und deine Rechnungen bleiben bei dir, so können Freunde dasselbe Rätsel noch unbefangen spielen.</p>
<h2>Bedienung</h2><p>Alle Rätsel lassen sich mit Maus, Finger oder Tastatur spielen: beim Codeknacker mit den Ziffern 1 bis 6, Enter und Rücktaste, beim Sudoku mit Pfeil- und Zifferntasten und der Taste N für Notizen, beim Nonogramm mit Leertaste oder Enter auf dem gewählten Feld. Die Felder sind für Bildschirmleser beschriftet. Wenn dir etwas umständlich vorkommt oder nicht funktioniert, freuen wir uns über einen Hinweis.</p>
<h2>Fehler oder Ideen?</h2><p>Hast du ein Rätsel gefunden, das sich nicht eindeutig lösen lässt, oder wünschst du dir eine neue Rätselart? Schreib uns – wir lesen jede Nachricht. Nenne dabei Datum und Rätselart, bei Sudoku und Nonogramm auch Stufe oder Größe: Weil jedes Rätsel aus dem Datum entsteht, können wir es damit exakt nachbauen und prüfen.</p>
<h2>Kontakt</h2><p><a href="mailto:office@adstern.com">office@adstern.com</a></p>""")
    write("imprint.html", "page.html", title="Impressum | Rätsellotse", description="Impressum von Rätsellotse.", h1="Impressum", ads=False, robots="noindex,follow",
          body=f"""<h2>Medieninhaber und Herausgeber</h2><p>{LEGAL_ADDR}</p>
<h2>Unternehmensangaben</h2><p>Unternehmensgegenstand: Werbeagentur<br>UID-Nummer: ATU54682507<br>Gewerbebehörde: Magistratisches Bezirksamt für den 1. und 8. Bezirk, Wien<br>Kammerzugehörigkeit: Wirtschaftskammer Wien, Fachgruppe Werbung und Marktkommunikation<br>Berufsbezeichnung: Werbeagentur (Gewerbe, verliehen in Österreich)<br>Anwendbare Rechtsvorschriften: Gewerbeordnung, abrufbar unter <a href="https://www.ris.bka.gv.at" rel="noopener">www.ris.bka.gv.at</a></p>
<p>Angaben nach § 5 E-Commerce-Gesetz und § 25 Mediengesetz.</p>
<h2>Grundlegende Richtung</h2><p>Rätsellotse ist eine unabhängige Unterhaltungsseite mit täglichen Logik- und Zahlenrätseln. Die Seite finanziert sich über Werbung.</p>""")
    body = (ROOT / "content" / "privacy_body.html").read_text(encoding="utf-8")
    import re
    body = re.sub(r"<h2>Werkzeuge</h2><p>.*?</p>", "<h2>Rätsel und Spielstand</h2><p>" + 
"Alle Rätsel laufen ausschließlich in deinem Browser. Damit du ein Rätsel später fortsetzen kannst und deine Serie sichtbar bleibt, speichern wir Spielstand, Serie und gewählte Schwierigkeit im lokalen Speicher deines Browsers (localStorage). Diese Speicherung ist für die von dir gewünschte Funktion erforderlich (§ 165 Abs. 3 TKG 2021); die Daten werden nicht an uns übertragen und lassen sich jederzeit über die Browser-Einstellungen löschen.</p>", body, flags=re.S)
    assert "Alle Rätsel laufen" in body
    write("privacy.html", "page.html", title="Datenschutz | Rätsellotse", description="Datenschutzerklärung von Rätsellotse.", h1="Datenschutzerklärung",
          lead="Stand: 4. November 2026", ads=False, robots="noindex,follow", body=body)
    write("404.html", "page.html", title="Seite nicht gefunden | Rätsellotse", description="Diese Seite gibt es nicht.", h1="Diese Seite gibt es nicht",
          lead="Die heutigen Rätsel warten trotzdem.", ads=False, robots="noindex", body="<p><a href='/'>Zu den Tagesrätseln</a></p>")

    (OUT / "assets" / "icon.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><circle cx="16" cy="16" r="14.5" fill="#21786C"/><path d="M16 6v14" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/><path d="M9 17a7 7 0 0 0 14 0" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/><circle cx="16" cy="8.5" r="3.2" fill="#E8622A" stroke="#fff" stroke-width="1.6"/></svg>')
    (OUT / "CNAME").write_text("raetsellotse.de\n"); (OUT / ".nojekyll").write_text("")
    (OUT / "google9bf1079fd4bf073e.html").write_text("google-site-verification: google9bf1079fd4bf073e.html")
    (OUT / "ads.txt").write_text("google.com, pub-7811071715414905, DIRECT, f08c47fec0942fa0\n")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    urls = "".join(f"<url><loc>{SITE}{p}</loc><lastmod>{lm}</lastmod><priority>{pr}</priority></url>" for p, pr, lm in PAGES)
    (OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    check_head()
    print(f"{len(PAGES)} indexierbare Seiten")


def check_head():
    """Indexierbare Seiten: Consent-Default → AdSense-Loader (genau einmal) → consent.js. noindex-Seiten: kein Loader.
    Jede Seite: Knopf „Datenschutz-Einstellungen“ (Widerruf) und consent.js; ohne Werbung mit data-ohne-werbung."""
    indexed = {("/index.html" if p == "/" else p) for p, _, _ in PAGES}
    for f in OUT.glob("*.html"):
        html = f.read_text(encoding="utf-8"); head = html.split("</head>", 1)[0]
        if "/" + f.name in indexed:
            d, l, c = head.find('gtag("consent","default"'), head.find(LOADER), head.find("/assets/consent.js")
            assert html.count("adsbygoogle.js") == 1 and -1 < d < l < c, f"Kopf falsch: {f.name}"
        else:
            assert "adsbygoogle" not in html, f"Loader auf nicht indexierbarer Seite: {f.name}"
        if f.name.startswith("google"): continue   # Bestätigungsdatei der Search Console
        assert html.count("data-privacy-settings") == 1, f"Knopf Datenschutz-Einstellungen fehlt: {f.name}"
        assert html.count("/assets/consent.js") == 1 and ("data-ohne-werbung" in head) == ("/" + f.name not in indexed), f"consent.js falsch: {f.name}"
        assert "googletagmanager" not in html, f"gtag.js statisch eingebunden: {f.name}"


if __name__ == "__main__":
    main()
