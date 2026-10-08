#!/usr/bin/env python3
"""Génère assets/card-en.svg, assets/card-fr.svg et assets/signals.svg.

- Les cartes sont statiques (édite INFO ci-dessous puis relance le script).
- Le radar "signals" est calculé depuis l'API GitHub (langages de tes dépôts publics).
Aucune dépendance externe : Python 3.8+ suffit.
"""
import json
import math
import os
import random
import urllib.request
from collections import Counter
from html import escape

USER = os.environ.get("GH_USER", "Krisaff7")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------- CONTENU
INFO = {
    "en": {
        "title": "profile.sh — ~/krisaff7",
        "map": "VISUAL MAP",
        "sys": "SYSTEM INFO",
        "rows": [
            ("Subject", "AFFOKPON Mahouton Kris"),
            ("Role", "Fullstack Web & Mobile Developer"),
            ("Origin", "Abomey-Calavi, Bénin"),
            ("Education", "Software Eng. — IFRI / UAC (Year 3)"),
            ("Status", "Building · Learning · Shipping"),
            ("Agency", "Affo Dev (freelance)"),
            ("Core.Web", "Next.js · React · Tailwind"),
            ("Core.Mobile", "React Native · Expo"),
            ("Goal", "Master's in DevOps & Cloud"),
            ("Languages", "Français · English"),
        ],
        "footer": "ALL SYSTEMS NOMINAL",
    },
    "fr": {
        "title": "profile.sh — ~/krisaff7",
        "map": "CARTE VISUELLE",
        "sys": "INFOS SYSTÈME",
        "rows": [
            ("Sujet", "AFFOKPON Mahouton Kris"),
            ("Rôle", "Dév. Fullstack Web & Mobile"),
            ("Origine", "Abomey-Calavi, Bénin"),
            ("Formation", "Génie Logiciel — IFRI / UAC (L3)"),
            ("Statut", "Je construis · J'apprends · Je livre"),
            ("Agence", "Affo Dev (freelance)"),
            ("Core.Web", "Next.js · React · Tailwind"),
            ("Core.Mobile", "React Native · Expo"),
            ("Objectif", "Master DevOps & Cloud"),
            ("Langues", "Français · English"),
        ],
        "footer": "TOUS SYSTÈMES OPÉRATIONNELS",
    },
}

BG, PANEL, LINE = "#0a0f1a", "#0e1726", "#1c3556"
ACCENT, GREEN, TXT, MUTED = "#38bdf8", "#34d399", "#d6e2f0", "#7389a6"
FONT = "ui-monospace,SFMono-Regular,Menlo,Consolas,'DejaVu Sans Mono',monospace"


# ---------------------------------------------------------------- CARTE
def particles(cx, cy, rnd):
    """Nuage de points qui dessine un </> avec un peu de poussière autour."""
    shapes = [
        [(-40, -60), (-100, 0), (-40, 60)],  # <
        [(25, -68), (-5, 68)],               # /
        [(50, -60), (110, 0), (50, 60)],     # >
    ]
    pts = []
    for poly in shapes:
        for (x1, y1), (x2, y2) in zip(poly, poly[1:]):
            n = max(2, int(math.hypot(x2 - x1, y2 - y1) / 5))
            for i in range(n + 1):
                t = i / n
                pts.append((cx + x1 + (x2 - x1) * t + rnd.uniform(-3, 3),
                            cy + y1 + (y2 - y1) * t + rnd.uniform(-3, 3), 1.7))
    for _ in range(70):
        pts.append((cx + rnd.uniform(-135, 135), cy + rnd.uniform(-100, 100), 1.0))
    return pts


def build_card(lang):
    d = INFO[lang]
    rnd = random.Random(7)
    W, H = 860, 400
    cx, cy = 194, 218
    dots = []
    for x, y, r in particles(cx, cy, rnd):
        dur = rnd.uniform(2.2, 5.5)
        begin = rnd.uniform(0, 4)
        lo = rnd.uniform(0.1, 0.35)
        color = ACCENT if rnd.random() > 0.2 else "#a5b4fc"
        dots.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{color}" opacity="{lo:.2f}">'
            f'<animate attributeName="opacity" values="{lo:.2f};1;{lo:.2f}" '
            f'dur="{dur:.1f}s" begin="{begin:.1f}s" repeatCount="indefinite"/></circle>'
        )

    rows = []
    y = 98
    for k, v in d["rows"]:
        rows.append(
            f'<text x="406" y="{y}" fill="{MUTED}" font-size="12.5">{escape(k)}</text>'
            f'<text x="520" y="{y}" fill="{TXT}" font-size="12.5">{escape(v)}</text>'
        )
        y += 25

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">
<title>{escape(d["title"])}</title>
<defs>
  <linearGradient id="scan" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{ACCENT}" stop-opacity="0"/>
    <stop offset="1" stop-color="{ACCENT}" stop-opacity="0.18"/>
  </linearGradient>
  <clipPath id="mapclip"><rect x="24" y="56" width="340" height="300" rx="6"/></clipPath>
</defs>
<rect width="{W}" height="{H}" rx="12" fill="{BG}" stroke="{LINE}"/>
<rect width="{W}" height="38" rx="12" fill="#101b2d"/>
<rect y="26" width="{W}" height="12" fill="#101b2d"/>
<circle cx="24" cy="19" r="6" fill="#ff5f56"/><circle cx="46" cy="19" r="6" fill="#ffbd2e"/><circle cx="68" cy="19" r="6" fill="#27c93f"/>
<text x="{W/2}" y="23" text-anchor="middle" fill="{MUTED}" font-size="12">{escape(d["title"])}</text>

<rect x="24" y="56" width="340" height="300" rx="6" fill="{PANEL}" stroke="{LINE}"/>
<text x="38" y="78" fill="{ACCENT}" font-size="11" letter-spacing="2">{escape(d["map"])}</text>
<g clip-path="url(#mapclip)">
  <g>{"".join(dots)}
    <animateTransform attributeName="transform" type="translate" values="0 0;0 -5;0 0" dur="7s" repeatCount="indefinite"/>
  </g>
  <rect x="24" y="-60" width="340" height="60" fill="url(#scan)">
    <animate attributeName="y" values="-60;356" dur="5s" repeatCount="indefinite"/>
  </rect>
</g>

<rect x="384" y="56" width="452" height="300" rx="6" fill="{PANEL}" stroke="{LINE}"/>
<text x="406" y="78" fill="{ACCENT}" font-size="11" letter-spacing="2">{escape(d["sys"])}</text>
{"".join(rows)}

<circle cx="30" cy="378" r="4" fill="{GREEN}"><animate attributeName="opacity" values="1;0.25;1" dur="1.6s" repeatCount="indefinite"/></circle>
<text x="42" y="382" fill="{GREEN}" font-size="11" letter-spacing="1">{escape(d["footer"])}</text>
<text x="{W-24}" y="382" text-anchor="end" fill="{MUTED}" font-size="11">@{escape(USER)}</text>
</svg>'''


# ---------------------------------------------------------------- SIGNALS
def gh(url):
    req = urllib.request.Request(url, headers={"User-Agent": "profile-build"})
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def fetch_languages():
    try:
        repos = gh(f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner")
        total = Counter()
        for repo in repos:
            if repo.get("fork"):
                continue
            for lang, n in gh(repo["languages_url"]).items():
                total[lang] += n
        return total.most_common(6)
    except Exception as e:  # réseau, quota, etc.
        print("API GitHub indisponible :", e)
        return []


def build_signals(langs):
    placeholder = not langs
    if placeholder:
        langs = [("TypeScript", 1), ("JavaScript", 1), ("CSS", 1), ("HTML", 1), ("Python", 1), ("Java", 1)]
    while len(langs) < 3:
        langs.append(("—", 0))
    total = sum(n for _, n in langs) or 1
    vals = [n / total for _, n in langs]
    top = max(vals) or 1
    W, H, cx, cy, R = 520, 340, 260, 175, 110
    N = len(langs)

    def pt(i, f):
        a = -math.pi / 2 + 2 * math.pi * i / N
        return cx + R * f * math.cos(a), cy + R * f * math.sin(a)

    grid = ""
    for lvl in (0.25, 0.5, 0.75, 1):
        grid += '<polygon points="%s" fill="none" stroke="%s"/>' % (
            " ".join("%.1f,%.1f" % pt(i, lvl) for i in range(N)), LINE)
    axes = "".join('<line x1="%d" y1="%d" x2="%.1f" y2="%.1f" stroke="%s"/>' % ((cx, cy) + pt(i, 1) + (LINE,))
                   for i in range(N))
    shape = " ".join("%.1f,%.1f" % pt(i, max(v / top, 0.05)) for i, v in enumerate(vals))
    labels = ""
    for i, ((name, _), v) in enumerate(zip(langs, vals)):
        x, y = pt(i, 1.28)
        anchor = "middle" if abs(x - cx) < 8 else ("start" if x > cx else "end")
        labels += (f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" fill="{TXT}" font-size="12">'
                   f'{escape(name)} <tspan fill="{MUTED}">{v*100:.0f}%</tspan></text>')
    note = "sample data" if placeholder else "from public repos"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">
<title>Signals — languages</title>
<rect width="{W}" height="{H}" rx="12" fill="{BG}" stroke="{LINE}"/>
<text x="24" y="30" fill="{ACCENT}" font-size="11" letter-spacing="2">SIGNALS</text>
<text x="{W-24}" y="30" text-anchor="end" fill="{MUTED}" font-size="11">{note}</text>
{grid}{axes}
<polygon points="{shape}" fill="{ACCENT}" fill-opacity="0.22" stroke="{ACCENT}" stroke-width="2">
  <animate attributeName="fill-opacity" values="0.12;0.32;0.12" dur="4s" repeatCount="indefinite"/>
</polygon>
{labels}
</svg>'''


if __name__ == "__main__":
    for lang in ("en", "fr"):
        with open(os.path.join(OUT, f"card-{lang}.svg"), "w", encoding="utf-8") as f:
            f.write(build_card(lang))
    with open(os.path.join(OUT, "signals.svg"), "w", encoding="utf-8") as f:
        f.write(build_signals(fetch_languages()))
    print("OK — assets générés dans", os.path.abspath(OUT))
