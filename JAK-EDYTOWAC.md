# Jak edytować stronę CHWDK

Strona to **jeden plik `index.html`** + folder **`media/`** ze zdjęciami. Nie ma tu żadnego frameworka ani budowania — to, co zapiszesz, trafia na stronę.

## Jak to działa

1. Zmieniasz plik na GitHubie (ikona ołówka przy pliku albo klawisz `.` — otwiera edytor w przeglądarce) i klikasz **Commit changes**.
2. Netlify po ok. minucie sam publikuje nową wersję na **chwdk.netlify.app**.
3. Każda wersja jest zapisana. Gdy coś się rozsypie: Netlify → **Deploys** → wybierz poprzednią wersję → **Publish deploy** (natychmiastowy powrót), a potem spokojnie popraw kod.

**Bezpieczniejsza droga przy większych zmianach:** przy „Commit changes” wybierz *Create a new branch and start a pull request*. Netlify zrobi wtedy **podgląd pod osobnym adresem** (link pojawi się w pull requeście). Jeśli wszystko wygląda dobrze — *Merge* i zmiana idzie na stronę.

Po każdej zmianie zerknij na stronę także **na telefonie**.

## Mapa pliku `index.html`

Sekcje są oznaczone komentarzami — szukaj ich (Ctrl/Cmd+F):

| Komentarz | Co tam jest |
|---|---|
| `<!-- HERO -->` | zdjęcie główne, tytuł, przyciski |
| `<!-- MANIFEST -->` | „Kim jesteśmy” — krótkie przedstawienie |
| `<!-- KURNIK -->` | „Poznaj kurnik” — nagłówek; **skład chóru jest niżej w skrypcie**, na liście `CHOR` |
| `<!-- DYRYGENTKA -->` | „Za pulpitem” — Aleksandra Kopp |
| `<!-- POSŁUCHAJ NAS -->` | filmy z YouTube (odtwarzacz + lista) |
| `<!-- AKTUALNOŚCI -->` | kalendarz koncertów + plakat |
| `<!-- O NAS -->` | „Skąd przyszłyśmy” |
| `<!-- KALENDARIUM -->` | „Nasza droga” — oś czasu |
| `<!-- GALERIA ROZSZERZONA -->` | galeria zdjęć |
| `<!-- REPERTUAR -->` | „Co śpiewamy” |
| `<!-- ENGLISH -->` | wersja dla partnerów zagranicznych |
| `<!-- FORMULARZ -->` | „Zaproś nas” + formularz |
| `<!-- STOPKA -->` | stopka z linkami |

Zwykłe teksty zmieniasz po prostu w HTML-u. Polskich „sierotek” (a, i, o, u, w, z na końcu linii) nie trzeba pilnować — strona poprawia je sama.

## Częste zadania

### Nowy koncert
W `<!-- AKTUALNOŚCI -->` skopiuj linię koncertu i separator:
```html
<div class="aktual-miejsce"><strong>20.09</strong> · Milanówek, Sploty</div>
<hr class="aktual-sep">
```
Nowy miesiąc: `<div class="aktual-date">październik 2026</div>`.

### Osoba w kurniku
W skrypcie szukaj `var CHOR=[` — jedna osoba to jedna linia:
```js
{"imie": "Ela", "glos": "mezzosopran", "foto": null, "rot": 1.2, "dy": 2, "kolor": 1, "grzebien": 0, "odbicie": 1, "skrzydlo": 0},
```
- `glos`: `"sopran"`, `"mezzosopran"` albo `"alt"`
- `foto`: `null` = kura bez zdjęcia. **Zdjęcie do kurnika wymaga obróbki** (wycięcie tła, kadr 319×380 px z głową w tej samej skali co u innych, wpis w `GLOWY`) — zdjęcie prześlij do osoby, która przygotowuje wycinki.
- kolejność na liście = kolejność na grzędzie; rozmiar kur przelicza się sam.
- dyrygentka: `var DYR=` tuż pod listą.

### Zdjęcie w galerii
Potrzebne są **dwa pliki** w `media/`: miniatura `gal-NAZWA.jpg` (dłuższy bok 860 px) i duże `gal-NAZWA-d.jpg` (dłuższy bok 1600 px). Potem skopiuj istniejący `<figure class="gl-el">…</figure>` i zmień:
- `data-duze="media/gal-NAZWA-d.jpg"`, `src="media/gal-NAZWA.jpg"`
- `width` i `height` — **prawdziwe wymiary miniatury** (np. 860 i 645); od nich zależy układ rzędów
- `data-opis`, `alt`, `aria-label`, tekst w `gl-podpis` — podpis zdjęcia; `data-miejsce` — miejsce i data
- `data-i` — kolejny numer (dla porządku)

Galeria sama układa się w równe rzędy.

### Film z YouTube
W `<!-- POSŁUCHAJ NAS -->` skopiuj jedną pozycję listy `<li><button class="pos-poz" …>` i zmień `data-yt` (ID filmu — to, co jest po `v=` w linku), `data-tytul`, `data-miejsce` oraz teksty w `<b>` i `<span>`. Miniatura: `media/yt-ID.jpg` (720×405 px). Liczbę nagrań w nagłówku listy (`Wszystkie nagrania <span>7</span>`) popraw ręcznie.

## Czego nie ruszać

- **`id="…"` sekcji** (np. `id="galeria"`) — korzystają z nich linki w menu.
- **Formularz:** atrybuty `name="kontakt"`, `data-netlify`, `netlify-honeypot` i ukryte pola `form-name`, `temat`. Zmiana nazwy formularza = zgłoszenia przestaną trafiać do Netlify.
- **Bloki `<style>` i `<script>`** — tylko jeśli wiesz, co robisz (wyjątek: lista `CHOR`).
- **Nazwy klas** — od nich zależy wygląd.

## Podgląd u siebie (opcjonalnie)

Otwarcie `index.html` z dysku działa, ale filmy z YouTube i formularz wtedy nie ruszą. Lepiej uruchomić prosty serwer w folderze strony:
```
python3 -m http.server 8000
```
i wejść na http://localhost:8000. Formularz i tak działa tylko na Netlify.
