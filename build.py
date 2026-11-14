# -*- coding: utf-8 -*-
"""Składa index.html z szablon.html + plików tresc/*.json."""
import json, os, re, sys
SP = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, SP)
import bloki
def wczytaj(n): return json.load(open(os.path.join(SP, "tresc-" + n), encoding="utf-8"))
import glob
teksty = {}
for sciezka in sorted(glob.glob(os.path.join(SP, "tresc-*.json"))):
    nazwa = os.path.basename(sciezka)
    if nazwa in ("tresc-chor.json", "tresc-kadry-glow.json", "tresc-koncerty.json", "tresc-nagrania.json",
                 "tresc-galeria.json", "tresc-kalendarium.json", "tresc-repertuar.json"):
        continue
    teksty.update(json.load(open(sciezka, encoding="utf-8")))
chor = wczytaj("chor.json")
teksty.update({k: v for k, v in wczytaj("koncerty.json").items() if k.startswith("foto_")})
chor["kadry_glow"] = wczytaj("kadry-glow.json")          # dane techniczne, poza CMS
s = open(os.path.join(SP, "szablon.html"), encoding="utf-8").read()
c, dyr, glowy = bloki.chor_js(chor)
blok = {"CHOR": c, "DYR": dyr, "GLOWY": glowy,
        "KONCERTY": bloki.koncerty_html(wczytaj("koncerty.json")),
        "NAGRANIA": bloki.nagrania_html(wczytaj("nagrania.json")),
        "GALERIA": bloki.galeria_html(wczytaj("galeria.json")),
        "KALENDARIUM": bloki.kalendarium_html(wczytaj("kalendarium.json")),
        "REPERTUAR": bloki.repertuar_html(wczytaj("repertuar.json"))}
for k, v in blok.items(): s = s.replace("{{%s}}" % k, v)
for k, v in teksty.items():
    if k.startswith("foto_"): v = str(v).lstrip("/")      # CMS zapisuje /plik.jpg
    s = s.replace("{{%s}}" % k, v)
puste = re.findall(r'\{\{([A-Za-z_]+)\}\}', s)
if puste: sys.exit("BŁĄD: niewypełnione znaczniki: %s" % sorted(set(puste)))
wyjscie = sys.argv[1] if len(sys.argv) > 1 else os.path.join(SP, "index.html")
open(wyjscie, "w", encoding="utf-8").write(s)
print("zapisano %s (%d B)" % (wyjscie, len(s)))
