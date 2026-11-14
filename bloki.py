# -*- coding: utf-8 -*-
"""Generatory fragmentów HTML z danych JSON. Wspólne dla build.py i testu."""
import json

DOMYSLNE = ("rot", "dy", "kolor", "grzebien", "odbicie", "skrzydlo")

def uzupelnij(o, i):
    """Brakujące parametry wyglądu liczone z pozycji — strona działa nawet bez nich."""
    w = dict(o)
    w.setdefault("foto", None)
    if w["foto"]: w["foto"] = str(w["foto"]).lstrip("/")
    w.setdefault("rot", round(((i * 37) % 9) * 0.6 - 2.4, 1))
    w.setdefault("dy", (i * 13) % 9 - 4)
    w.setdefault("kolor", i % 3)
    w.setdefault("grzebien", (i * 7) % 2)
    w.setdefault("odbicie", (i * 5) % 2)
    w.setdefault("skrzydlo", (i * 11) % 2)
    kolejnosc = list(o.keys()) + [k for k in ("imie", "glos", "foto") + DOMYSLNE if k not in o]
    return {k: w[k] for k in kolejnosc}

def chor_js(d):
    osoby = [uzupelnij(o, i) for i, o in enumerate(d["chor"])]
    linie = ",\n    ".join(json.dumps(o, ensure_ascii=False) for o in osoby)
    glowy = "{" + ",".join("'%s':[%s]" % (k, ",".join("%.3f" % x for x in v)) for k, v in d.get("kadry_glow", {}).items()) + "}"
    return ("var CHOR=[\n    " + linie + "\n  ];",
            "var DYR=" + json.dumps(d["dyrygentka"], ensure_ascii=False) + ";",
            "var GLOWY=" + glowy + ";")

def sciezka(x):
    return str(x or "").lstrip("/")

def koncerty_html(d):
    cz, wszystkie = [], [(r, k) for r in d["lata"] for k in r["koncerty"]]
    for rok in d["lata"]:
        cz.append('      <div class="aktual-date">%s</div>' % rok["rok"])
        for k in rok["koncerty"]:
            cz.append('      <div class="aktual-miejsce"><strong>%s</strong>%s</div>' % (k.get("kiedy", ""), k.get("opis", "")))
            if (rok, k) != wszystkie[-1]:
                cz.append('      <hr class="aktual-sep">')
    return "\n".join(cz)

def nagrania_html(d):
    cz = []
    for n, f in enumerate(d["filmy"]):
        cz.append('      <li><button type="button" class="pos-poz%s" data-yt="%s" data-tytul="%s" data-miejsce="%s"%s>'
                  '<span class="pos-poz-min"><img src="yt-%s.jpg" width="720" height="405" alt="" loading="lazy" decoding="async"></span>'
                  '<span class="pos-poz-txt"><b>%s</b><span>%s</span></span></button></li>'
                  % (" aktywny" if n == 0 else "", f.get("yt", ""),
                     f.get("tytul") or f.get("tytul_widoczny", ""),
                     f.get("miejsce_atrybut") or f.get("miejsce", ""),
                     ' aria-current="true"' if n == 0 else "", f.get("yt", ""),
                     f.get("tytul_widoczny") or f.get("tytul", ""), f.get("miejsce", "")))
    return "\n".join(cz)

def galeria_html(d):
    cz, i = [], 0
    for al in d["albumy"]:
        cz.append('  <div class="gl-rozdzial">')
        cz.append('    <p class="gl-etykieta"><b>%s</b><span>%s</span></p>' % (al["tytul"], al["podtytul"]))
        cz.append('    <div class="gl-siatka">')
        for z in al["zdjecia"]:
            cz.append('      <figure class="gl-el"><button type="button" class="gl-btn" data-i="%d" data-duze="%s" '
                      'data-opis="%s" data-miejsce="%s" aria-label="Powiększ: %s"><img src="%s" width="%d" height="%d" '
                      'alt="%s" loading="lazy" decoding="async"><span class="gl-podpis">%s</span></button></figure>'
                      % (i, sciezka(z.get("duzy") or z.get("maly")), z.get("opis", ""), z.get("miejsce", ""), z.get("opis", ""),
                         sciezka(z.get("maly") or z.get("duzy")), int(z.get("w") or 860), int(z.get("h") or 573), z.get("opis", ""), z.get("opis", "")))
            i += 1
        cz.append('    </div>')
        cz.append('  </div>')
        if al is not d["albumy"][-1]:
            cz.append('')
    return "\n".join(cz)

def kalendarium_html(d):
    cz = []
    for n, w in enumerate(d["wpisy"]):
        ost = n == len(d["wpisy"]) - 1
        duza, wyr, rok = w.get("duza_kropka", False), w.get("wyroznione", True), w.get("rok", "")
        rok_st = 'min-width:72px;font-family:Syne,sans-serif;font-size:10px;font-weight:700;color:var(--roz);padding-top:%dpx%s' % (
            2 if duza else 4, ';letter-spacing:.06em' if rok else '')
        if duza:
            kropka = ('<div style="width:14px;height:14px;border-radius:50%;background:var(--roz);margin-top:2px;'
                      'margin-right:22px;flex-shrink:0;position:relative;z-index:1;box-shadow:0 0 0 4px rgba(232,23,93,.2)"></div>')
        elif wyr:
            kropka = ('<div style="width:10px;height:10px;border-radius:50%;background:var(--roz);margin-top:4px;'
                      'margin-right:24px;flex-shrink:0;position:relative;z-index:1"></div>')
        else:
            kropka = ('<div style="width:10px;height:10px;border-radius:50%;background:#1f1f1f;border:1px solid #2a2a2a;'
                      'margin-top:4px;margin-right:24px;flex-shrink:0;position:relative;z-index:1"></div>')
        cz.append('    <div style="display:flex;gap:0;align-items:flex-start%s">' % ("" if ost else ";padding-bottom:40px"))
        cz.append('      <div style="%s">%s</div>' % (rok_st, rok))
        cz.append('      ' + kropka)
        cz.append('      <div><p style="font-family:\'Cormorant Garamond\',serif;font-size:18px;font-weight:600;color:#fff;'
                  'margin-bottom:5px">%s</p><p style="font-size:13px;color:#555;line-height:1.7">%s</p></div>' % (w.get("tytul", ""), w.get("opis", "")))
        cz.append('    </div>')
        cz.append('')
    return "\n".join(cz)

def repertuar_html(d):
    return "\n".join('    <div class="rep-item"><div class="rep-nr">%s</div><div class="rep-name">%s</div>'
                     '<div class="rep-desc">%s</div></div>' % (k.get("nr", ""), k.get("nazwa", ""), k.get("opis", "")) for k in d["karty"])
