# Dům Netušil – web

Statický web pro projekt Dům Netušil (Netušilova 15, Brno-Husovice) – 14 komorních bytů v historickém měšťanském domě.

## 📌 Náš workflow (důležité)

```
┌─────────────────────────────────────────────────────────────┐
│  1. Úpravy děláme v Claude chatu                            │
│     (ceny, statusy, popisy bytů, layout, atd.)              │
│                          ↓                                  │
│  2. Stáhneš si finální verzi web-final/ k sobě na disk      │
│                          ↓                                  │
│  3. Pushneš obsah do tvého GitHub repa                      │
│                          ↓                                  │
│  4. GitHub Pages auto-deploy → web je živý                  │
└─────────────────────────────────────────────────────────────┘
```

**Klíčové:** Veškeré úpravy ceny.json, status.json i obsahu generujeme tady, ne v GitHub repu.
Tvůj Git repo je "zlatá kopie" toho, co je nasazené — nepřepisuj v něm nic ručně,
aby další iterace nepřišly o tvoje změny.

## Struktura

```
web-final/
├── index.html              # hlavní stránka
├── styles.css              # všechny styly (jeden soubor pro index i podstránky)
├── script.js               # JS (lightbox + filtr bytů)
├── sitemap.xml             # 15 URL pro vyhledávače
├── robots.txt              # crawler pravidla
├── .htaccess               # Apache - security headers, cache, friendly URLs
├── README.md               # tento soubor
├── generate.py             # generátor – upravuj data zde
│
├── byty/                   # 14 podstránek
│   ├── byt-01.html
│   ├── byt-02.html
│   └── ... byt-14.html
│
└── img/
    ├── pudorysy/           # 14 PNG půdorysů
    │   ├── byt-01.png
    │   └── ... byt-14.png
    └── vizualizace/        # 18 fotek/renderů
        ├── 1np-2kk.jpg
        ├── ext-1.jpg
        └── ...
```

## Co dělat při změnách

Veškerá data o bytech (popisy, ceny, plochy, místnosti) jsou v `generate.py` v poli `APARTMENTS`. Po úpravě:

```bash
python3 generate.py
```

Skript přepíše `index.html` + všech 14 `byty/byt-XX.html` + sitemap.

### Status bytů (k dispozici / rezervováno / prodáno)

V souboru `status.json` můžeš snadno měnit dostupnost jednotlivých bytů. Stačí upravit hodnotu `status` a spustit `python3 generate.py`.

**Povolené hodnoty:**

| status | Karta na indexu | Detail bytu | CTA tlačítko |
|---|---|---|---|
| `k dispozici` | Zelený badge "K dispozici" | Standardní zobrazení | "Sjednat prohlídku" – aktivní |
| `rezervovano` | Oranžový badge + razítko "REZERVOVÁNO" přes kartu | Oranžové razítko v hero + upravený text | "Rezervováno" – neaktivní (šedé) |
| `prodano` | Červený badge + razítko "PRODÁNO" + ztlumená karta + přeškrtnutá cena | Červené razítko v hero + grayscale + přeškrtnutá cena | "Prodáno" – neaktivní |

**Příklad** `status.json`:
```json
{
  "byty": {
    "01": { "status": "k dispozici" },
    "02": { "status": "rezervovano", "poznamka": "Rezervace do 31.7.2026" },
    "03": { "status": "prodano" }
  }
}
```

**Návštěvníci webu mají také filtr** v sekci "Výběr bytů":
- Volné (počet)
- Rezervované (počet)
- Prodané (počet)
- Vše

**Validace:** `generate.py` zkontroluje, jestli jsou všechny statusy mezi povolenými hodnotami (`k dispozici`, `rezervovano`, `prodano`). Jinak skončí s chybou a neaktualizuje web.

## Nasazení

### Apache (sdílený hosting jako Forpsi, WebHosting.cz)

Stačí nahrát celý obsah složky do `public_html/` nebo `www/`. `.htaccess` se aktivuje sám:

- security headers (X-Frame-Options, CSP, Referrer-Policy)
- gzip/deflate komprese
- 30denní cache pro obrázky
- friendly URLs (`/byt-01` → `/byty/byt-01.html`)

### Nginx (např. server, Vercel/Netlify)

`.htaccess` Nginx ignoruje. Ekvivalent v `nginx.conf`:

```nginx
add_header X-Content-Type-Options "nosniff" always;
add_header X-Frame-Options "SAMEORIGIN" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

gzip on;
gzip_types text/html text/css application/javascript image/svg+xml;

location ~* \.(jpg|jpeg|png|webp|svg)$ {
    expires 30d;
    add_header Cache-Control "public, immutable";
}

rewrite ^/byt-(\d{2})/?$ /byty/byt-$1.html last;
```

### Statický hosting (Netlify, Cloudflare Pages, GitHub Pages)

- Netlify: drag & drop celé složky `web-final/` do Netlify.app, nebo `netlify deploy --prod --dir=web-final`
- Cloudflare Pages: push do gitu, Pages auto-deploy
- GitHub Pages: push do `gh-pages` branch

Security headers nutno přidat přes `_headers` (Netlify) nebo `wrangler.toml` (Cloudflare):

**Netlify `_headers`:**
```
/*
  X-Frame-Options: SAMEORIGIN
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: geolocation=(), microphone=(), camera=()
  Strict-Transport-Security: max-age=31536000; includeSubDomains
```

## Doménová URL

V `generate.py` je `SITE_URL = "https://domnetusil.cz"` – pokud máš jinou doménu, uprav před deploy a přegeneruj.

## Bezpečnost

Web je čistě statický (HTML/CSS/JS, žádný backend, žádná data). Implementované ochrany:

- **CSP** – `Content-Security-Policy` v meta tagu blokuje libovolné externí skripty, jen vlastní zdroje + `data:` pro inline obrázky
- **XSS prevence** – všechen text generovaný z `APARTMENTS` jde přes `html.escape()`
- **Žádné inline event handlery** – `onclick=` neexistuje, vše přes `addEventListener`
- **Žádné externí závislosti** – žádné CDN, žádný jQuery, žádné fonty z Google, vše inline
- **HTTPS-only** – `.htaccess` má připravený force HTTPS (zakomentovaný, odkomentovat při ostrem deploy)
- **HSTS** – `Strict-Transport-Security` na 1 rok

## SEO

- `<meta name="description">` na každé stránce
- Open Graph + Twitter karty pro sociální sítě
- `schema.org/Apartment` JSON-LD strukturovaná data
- `<link rel="canonical">`
- `sitemap.xml` pro Google Search Console
- `robots.txt` povoluje indexaci, blokuje `.py` a `.md`
- Semantické HTML (`<header>`, `<section>`, `<nav>`, `<aside>`, `<footer>`)
- `alt` na všech obrázcích

## Výkon

- Žádné JS frameworky – stránka načte rychle i na slabém spojení
- `loading="lazy"` na obrázcích pod fold
- `preload` na hero obrázek
- 30denní browser cache na obrázky (přes `.htaccess`)
- Gzip komprese HTML/CSS/JS

## Stránky

| URL | Obsah |
|---|---|
| `/` | Hero, manifest, výběr 14 bytů s filtrem |
| `/byty/byt-01.html` ... `/byty/byt-14.html` | Detail bytu (hero, popis, plochy, půdorys, koupelna, cena) |
| `/sitemap.xml` | Mapa stránek pro vyhledávače |
| `/robots.txt` | Pravidla pro crawlery |

## Cenotvorba

Ceny **NEPOČÍTÁME** automaticky — jsou definované v souboru `ceny.json`. Zdroj: `20260508_Netusilova ekonomika.xlsx` (sheet "Ekonomika").

**Příklad** `ceny.json`:
```json
{
  "byty": {
    "01": {
      "cena_kc": 6572390,
      "cena_kc_m2": 149000,
      "cena_terasy_kc": 1862500
    },
    "02": {
      "cena_kc": 5066550,
      "cena_kc_m2": 139000
    }
  }
}
```

**Po úpravě cen** uprav `ceny.json` a spusť:

```bash
python3 generate.py
```

Generátor přepíše všechny stránky s novými cenami. Pokud zapomeneš na nějaký byt nebo zadáš neplatnou hodnotu, skript skončí s chybou.

## GitHub Pages deployment

Web je připraven na **GitHub Pages**. Stačí push do repa a GH Pages auto-deploy.

### Co je v balíčku pro GH Pages:

- **`.nojekyll`** — zakáže Jekyll processing (jinak by GH Pages přeskočil soubory začínající `_`)
- **`CNAME`** — custom doména (uprav podle své)
- **`404.html`** — GH Pages ji automaticky použije pro 404
- **Žádné absolute paths** — všechny odkazy fungují i při deployi do podsložky

### Jak nasadit poprvé:

1. **Vytvořit repo** na GitHubu (např. `dum-netusil`)
2. **Push** obsah složky `web-final/` do `main` branch (vše kromě `.github/`, viz níže)
3. V **Settings → Pages** zvolit branch `main` a složku `/ (root)`
4. Custom doména `dumnetusil.cz` se nastaví sama přes `CNAME` soubor
5. Počkat ~1 minutu, web naběhne na https://dumnetusil.cz

### Aktualizace později:

```bash
# Stáhni si finální verzi web-final/ z Claude chatu
# Rozbal do svého git working directory (nebo prostě nahraj soubory)
cd ~/projekty/dum-netusil
git add .
git commit -m "Aktualizace ceny / statusů / obsahu"
git push
# Hotovo, GitHub Pages přepublikuje za ~30s
```

### `.github/` složka

Generátor vyrobí `.github/workflows/build.yml` jako šablonu pro volitelný CI/CD pipeline.
**Pro náš workflow ho NEPOTŘEBUJEŠ** — můžeš ho před push smazat, nebo nechat (ale neaktivuj Actions ve tvém repu).

CI/CD by se hodilo, kdyby ses chtěl jednou rozhodnout, že budeš editovat `ceny.json` přímo na GitHubu přes web UI — pak by se HTML stránky regenerovaly automaticky. Pro náš workflow ale generujeme všechno tady a pushujeme finální produkt.

### ⚠ Co na GH Pages NEFUNGUJE:

- **`.htaccess`** — Apache pravidla, GitHub Pages je Nginx-based, ignoruje. Soubor zůstává jen pro lokální Apache nebo Forpsi-like hosting. **Security headers nutno nastavit jinak** (nebo akceptovat výchozí GH Pages, které jsou solidní). Bezpečnostní `<meta http-equiv>` v každé stránce kryjí většinu nepotřebných.
- **Friendly URLs** (`/byt-01` → `/byty/byt-01.html`) — GH Pages neumí rewrite. Vždy se musí používat plná cesta `byty/byt-XX.html` v odkazech (což už generátor dělá).
- **HTTPS redirect** — GH Pages už dělá automaticky, není potřeba řešit.

---

© BH Projects & Development – Dům Netušil
