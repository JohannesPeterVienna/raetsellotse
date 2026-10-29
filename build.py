"""Erzeugt Rätsellotse als statische Website in docs/ (GitHub Pages)."""
import random, shutil, sys
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
sys.path.insert(0, str(Path(__file__).parent))
from content.articles import ARTICLES

ROOT = Path(__file__).parent; OUT = ROOT / "docs"
SITE = "https://raetsellotse.de"; V = "20261029"; UPDATED = "Oktober 2026"
NAV = [("/", "Heute"), ("/codeknacker.html", "Codeknacker"), ("/sudoku.html", "Sudoku"), ("/zielzahl.html", "Zielzahl"),
       ("/sudoku-zum-ausdrucken-mittel.html", "Zum Ausdrucken")]
env = Environment(loader=FileSystemLoader(ROOT / "templates"), autoescape=True, trim_blocks=True, lstrip_blocks=True)
PAGES = []
BY = {a["slug"]: a for a in ARTICLES}
LEGAL_ADDR = "AdStern :: Agentur für digitales Marketing<br>Seilerstätte 8, 1010 Wien, Österreich<br>E-Mail: <a href='mailto:office@adstern.com'>office@adstern.com</a><br>Web: <a href='https://www.adstern.com'>www.adstern.com</a>"


def write(path, template, **ctx):
    base = dict(site=SITE, v=V, updated=UPDATED, nav=NAV, active=ctx.get("active", "/" + path), jsonld=[], ads=True, robots=None, og_title=None)
    base.update(ctx); base["path"] = "/" if path == "index.html" else "/" + path
    (OUT / path).write_text(env.get_template(template).render(**base), encoding="utf-8")
    if base.get("robots") is None: PAGES.append((base["path"], ctx.get("priority", 0.6)))


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
UI_ZIEL = """<div class="daynav" data-daynav></div>
<div class="small muted">Zielzahl</div><div class="target" data-target>…</div>
<div class="tiles" data-nums aria-label="Verfügbare Zahlen – antippen zum Einfügen"></div>
<input class="expr" data-expr inputmode="text" autocomplete="off" placeholder="z. B. (100 + 6) × 4 − 9" aria-label="Deine Rechnung">
<div class="pad"><button type="button" class="btn" data-check>Rechnen</button><button type="button" class="btn ghost" data-solve>Lösung zeigen</button></div>
<p class="msg" data-msg aria-live="polite"></p><p data-solution></p>"""


def main():
    if OUT.exists(): shutil.rmtree(OUT)
    (OUT / "assets").mkdir(parents=True)
    for f in (ROOT / "assets").iterdir(): shutil.copy(f, OUT / "assets" / f.name)

    write("index.html", "home.html", title="Rätsellotse – tägliche Rätsel: Codeknacker, Sudoku & Zielzahl",
          description="Jeden Tag drei neue Logikrätsel: Codeknacker, Sudoku in drei Stufen und Zielzahl. Kostenlos, ohne Anmeldung, mit Archiv und Serienzähler.",
          articles=ARTICLES, priority=1.0, active="/",
          jsonld=[{"@context": "https://schema.org", "@type": "WebSite", "name": "Rätsellotse", "url": SITE + "/", "inLanguage": "de"}])

    games = [
        ("codeknacker", "Codeknacker", "Codeknacker – das tägliche Logikrätsel mit Zahlencode",
         "Knacke jeden Tag einen neuen vierstelligen Zahlencode mit Logik: zehn Versuche, Hinweise nach jedem Tipp, Archiv und Serienzähler.",
         "Vier verschiedene Ziffern von 1 bis 6, zehn Versuche. Orange heißt: richtig platziert. Weiß: richtige Ziffer, falsche Stelle.",
         UI_CODE, ["codeknacker-anleitung"],
         "<h2>Kurz erklärt</h2><p>Tippe vier verschiedene Ziffern und drücke Prüfen – oder nutze die Tastatur (1–6, Enter, Rücktaste). Nach jedem Versuch zeigen die Punkte, wie nah du dran bist. Die ausführlichen Regeln und eine Strategie findest du in der <a href='/codeknacker-anleitung.html'>Anleitung</a>.</p><p>Jeden Tag gibt es einen neuen Code, für alle derselbe. Ältere Rätsel öffnest du über das Archiv oben im Spielfeld.</p>"),
        ("sudoku", "Sudoku", "Sudoku online – täglich neu, leicht bis schwer, mit Tipps",
         "Tägliches Sudoku online spielen: drei Schwierigkeitsstufen, Notizen, erklärte Tipps, Archiv – kostenlos und ohne Anmeldung.",
         "Jeden Tag drei neue Sudokus – leicht, mittel und schwer. Jedes hat genau eine Lösung, und die Tipps erklären den nächsten logischen Schritt.",
         UI_SUDOKU, ["sudoku-strategien", "sudoku-regeln-und-geschichte"],
         "<h2>Bedienung</h2><ul><li>Feld antippen, dann Ziffer wählen – oder Pfeiltasten und Zifferntasten.</li><li><strong>Notizen</strong> (Taste N) schaltet auf kleine Kandidaten-Ziffern um.</li><li><strong>Tipp</strong> zeigt zuerst falsche Einträge, sonst den nächsten logischen Schritt mit Erklärung.</li></ul><p>Leichte und mittlere Sudokus lassen sich nur mit den beiden einfachsten Techniken lösen; schwere haben weniger Vorgaben und verlangen mehr Überblick. Mehr dazu in den <a href='/sudoku-strategien.html'>Sudoku-Strategien</a>.</p>"),
        ("zielzahl", "Zielzahl", "Zielzahl – das tägliche Rechenrätsel mit sechs Zahlen",
         "Triff jeden Tag eine neue Zielzahl mit sechs Zahlen und den vier Grundrechenarten. Kopfrechnen trainieren – kostenlos, mit Lösungsweg.",
         "Erreiche die Zielzahl mit + − × ÷. Jede Zahl höchstens einmal, Teilen nur ohne Rest. Jede Aufgabe ist garantiert lösbar.",
         UI_ZIEL, ["zielzahl-tipps"],
         "<h2>So rechnest du</h2><p>Tippe die Zahlen an oder schreib die Rechnung direkt ins Feld, zum Beispiel (75 + 25) × 6 − 9. Klammern sind erlaubt, Malpunkt und Doppelpunkt ebenfalls. Kommst du nicht weiter, zeigt „Lösung zeigen“ einen möglichen Weg.</p><p>Strategien für schnelles Kopfrechnen findest du in den <a href='/zielzahl-tipps.html'>Zielzahl-Tipps</a>.</p>"),
    ]
    for slug, name, title, desc, lead, ui, rel, body in games:
        crumbs = [("/", "Rätsellotse"), (f"/{slug}.html", name)]
        ld = [crumbs_ld(crumbs), {"@context": "https://schema.org", "@type": "WebApplication", "name": f"{name} – Rätsellotse", "url": f"{SITE}/{slug}.html",
              "applicationCategory": "GameApplication", "operatingSystem": "Web", "inLanguage": "de", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"}}]
        write(f"{slug}.html", "game.html", title=f"{title} | Rätsellotse", description=desc, h1=name, lead=lead, ui=ui, game=slug,
              body=body, related=[BY[s] for s in rel], crumbs=crumbs, jsonld=ld, priority=0.9)

    for level, intro in (("leicht", "Für Einsteiger: viele Vorgaben, lösbar allein mit den beiden einfachsten Techniken."),
                         ("mittel", "Weniger Vorgaben, aber weiterhin ohne Raten mit einfachen Techniken lösbar."),
                         ("schwer", "Nur rund 25 Vorgaben – hier braucht es Überblick und fortgeschrittene Techniken.")):
        puzzles = [make(f"druck-{level}-2026-{k}", level) for k in range(6)]
        grid = "".join(f"<div><h3 style='margin:0 0 6px'>Sudoku {k+1}</h3>{table(p)}</div>" for k, (p, s) in enumerate(puzzles))
        sols = "".join(f"<div><h3 style='margin:0 0 6px;font-size:.9rem'>Lösung {k+1}</h3>{table(s, 'ps sol')}</div>" for k, (p, s) in enumerate(puzzles))
        others = " · ".join(f"<a href='/sudoku-zum-ausdrucken-{l}.html'>{l}</a>" for l in ("leicht", "mittel", "schwer") if l != level)
        body = (f"<p class='no-print'><button class='btn' type='button' onclick='print()'>Drucken oder als PDF speichern</button></p>"
                f"<div class='printgrid'>{grid}</div><h2 style='break-before:page'>Lösungen</h2><div class='printgrid'>{sols}</div>"
                f"<h2 class='no-print'>Andere Schwierigkeiten</h2><p class='no-print'>{others} · <a href='/sudoku.html'>Tagessudoku online spielen</a></p>"
                "<p class='small muted no-print'>Jedes Sudoku hat genau eine Lösung. Beim Drucken werden Navigation und Werbung ausgeblendet; Lösungen beginnen auf einer neuen Seite.</p>")
        crumbs = [("/", "Rätsellotse"), (f"/sudoku-zum-ausdrucken-{level}.html", f"Sudoku zum Ausdrucken ({level})")]
        write(f"sudoku-zum-ausdrucken-{level}.html", "page.html", title=f"Sudoku zum Ausdrucken – {level} (6 Rätsel mit Lösungen, PDF) | Rätsellotse",
              description=f"Sechs Sudokus zum Ausdrucken, Schwierigkeit {level}, mit Lösungen auf separater Seite. Kostenlos drucken oder als PDF speichern.",
              h1=f"Sudoku zum Ausdrucken: {level}", lead=intro, body=body, crumbs=crumbs, jsonld=[crumbs_ld(crumbs)],
              active="/sudoku-zum-ausdrucken-mittel.html", priority=0.8)

    for a in ARTICLES:
        crumbs = [("/", "Rätsellotse"), ("/" + a["slug"] + ".html", a["title"])]
        ld = [crumbs_ld(crumbs), {"@context": "https://schema.org", "@type": "Article", "headline": a["title"], "description": a["description"], "inLanguage": "de",
              "datePublished": "2026-10-29", "dateModified": "2026-10-29", "author": {"@type": "Organization", "name": "Redaktion Rätsellotse", "url": SITE + "/about.html"},
              "publisher": {"@type": "Organization", "name": "AdStern"}}]
        write(a["slug"] + ".html", "page.html", title=f"{a['title']} | Rätsellotse", description=a["description"], h1=a["title"], lead=a["teaser"],
              body=a["body"], crumbs=crumbs, related=[x for x in ARTICLES if x["slug"] != a["slug"]][:3], jsonld=ld, priority=0.7)

    write("about.html", "page.html", title="Über Rätsellotse", description="Wer hinter Rätsellotse steht und wie die Rätsel entstehen.",
          h1="Über Rätsellotse", lead="Täglich frische Rätsel – fair, eindeutig lösbar und ohne Anmeldung.", priority=0.3,
          body="""<p>Rätsellotse wird von AdStern in Wien betrieben. Jeden Tag erscheinen drei neue Rätsel, für alle Spielerinnen und Spieler dieselben.</p>
<h2>Wie die Rätsel entstehen</h2><p>Die Rätsel werden von einem Programm erzeugt und automatisch geprüft: Jedes Sudoku hat genau eine Lösung, leichte und mittlere Sudokus lassen sich ohne fortgeschrittene Techniken lösen, und jede Zielzahl ist nachweislich erreichbar. Der Code und die Zahlen eines Tages hängen nur vom Datum ab.</p>
<h2>Deine Daten</h2><p>Fortschritt und Serien speichern wir nur in deinem Browser. Es gibt kein Konto und keine Bestenliste mit persönlichen Daten. Werbung und Statistik laufen nur mit deiner Einwilligung; Details in der <a href="/privacy.html">Datenschutzerklärung</a>.</p>
<h2>Kontakt</h2><p><a href="mailto:office@adstern.com">office@adstern.com</a></p>""")
    write("imprint.html", "page.html", title="Impressum | Rätsellotse", description="Impressum von Rätsellotse.", h1="Impressum", ads=False, robots="noindex,follow",
          body=f"""<h2>Medieninhaber und Herausgeber</h2><p>{LEGAL_ADDR}</p>
<h2>Unternehmensangaben</h2><p>Unternehmensgegenstand: Werbeagentur<br>UID-Nummer: ATU54682507<br>Gewerbebehörde: Magistratisches Bezirksamt für den 1. Bezirk, Wien</p>
<p>Angaben nach § 5 E-Commerce-Gesetz und § 25 Mediengesetz.</p>
<h2>Grundlegende Richtung</h2><p>Rätsellotse ist eine unabhängige Unterhaltungsseite mit täglichen Logik- und Zahlenrätseln. Die Seite finanziert sich über Werbung.</p>""")
    body = (ROOT / "content" / "privacy_body.html").read_text(encoding="utf-8")
    import re
    body = re.sub(r"<h2>Werkzeuge</h2><p>.*?</p>", "<h2>Rätsel und Spielstand</h2><p>" + 
"Alle Rätsel laufen ausschließlich in deinem Browser. Damit du ein Rätsel später fortsetzen kannst und deine Serie sichtbar bleibt, speichern wir Spielstand, Serie und gewählte Schwierigkeit im lokalen Speicher deines Browsers (localStorage). Diese Speicherung ist für die von dir gewünschte Funktion erforderlich (§ 165 Abs. 3 TKG 2021); die Daten werden nicht an uns übertragen und lassen sich jederzeit über die Browser-Einstellungen löschen.</p>", body, flags=re.S)
    assert "Alle Rätsel laufen" in body
    write("privacy.html", "page.html", title="Datenschutz | Rätsellotse", description="Datenschutzerklärung von Rätsellotse.", h1="Datenschutzerklärung",
          lead="Stand: 29. Oktober 2026", ads=False, robots="noindex,follow", body=body)
    write("404.html", "page.html", title="Seite nicht gefunden | Rätsellotse", description="Diese Seite gibt es nicht.", h1="Diese Seite gibt es nicht",
          lead="Die heutigen Rätsel warten trotzdem.", ads=False, robots="noindex", body="<p><a href='/'>Zu den Tagesrätseln</a></p>")
    (OUT / "advertise.html").write_text(f'<!doctype html><html lang="de"><head><meta charset="utf-8"><title>Weiterleitung</title><meta name="robots" content="noindex"><link rel="canonical" href="{SITE}/about.html"><meta http-equiv="refresh" content="0; url=/about.html"></head><body><a href="/about.html">Weiter</a></body></html>', encoding="utf-8")

    (OUT / "assets" / "icon.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><circle cx="16" cy="16" r="14.5" fill="#21786C"/><path d="M16 6v14" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/><path d="M9 17a7 7 0 0 0 14 0" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/><circle cx="16" cy="8.5" r="3.2" fill="#E8622A" stroke="#fff" stroke-width="1.6"/></svg>')
    (OUT / "CNAME").write_text("raetsellotse.de\n"); (OUT / ".nojekyll").write_text("")
    (OUT / "ads.txt").write_text("google.com, pub-7811071715414905, DIRECT, f08c47fec0942fa0\n")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    urls = "".join(f"<url><loc>{SITE}{p}</loc><lastmod>2026-10-29</lastmod><priority>{pr}</priority></url>" for p, pr in PAGES)
    (OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    print(f"{len(PAGES)} indexierbare Seiten")


if __name__ == "__main__":
    main()
