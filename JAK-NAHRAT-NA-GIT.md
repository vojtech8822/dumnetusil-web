# Jak nahrát web na GitHub a aktivovat GitHub Pages

Krok za krokem návod, jak dostat tento web online. Trvá to ~15 minut.

## Co potřebuješ

- GitHub účet (nemáš? založ na [github.com/signup](https://github.com/signup))
- Tento adresář (`Web pro GIT/`) na disku
- Terminál (na Macu: Spotlight → "Terminal")
- Nainstalovaný Git (`git --version` v Terminálu, na Macu je už předinstalován)

---

## Varianta A — Nahráváš poprvé

### Krok 1: Vytvoř nový repo na GitHubu

1. Jdi na [github.com/new](https://github.com/new)
2. Vyplň:
   - **Repository name**: `dum-netusil-web` (nebo cokoli chceš)
   - **Description**: `Dům Netušil — marketing website`
   - **Public** (musí být veřejný, aby GitHub Pages mohl publikovat zdarma)
   - **NEZAŠKRTÁVEJ** "Add README", "Add .gitignore" ani "Choose a license" — chceš prázdný repo
3. Klikni **Create repository**

### Krok 2: Otevři Terminál v této složce

V Finderu pravým tlačítkem na složku `Web pro GIT` → **Služby** → **Nový terminál ve složce**.

Nebo přímo v Terminálu:
```bash
cd "/Users/vojtechhavranek/Desktop/_BH development/Netušilova - Husovice/Web pro GIT"
```

### Krok 3: Inicializuj Git, přidej soubory, pushni

Kopíruj a vlož do Terminálu **jeden řádek po druhém**:

```bash
# 1. Inicializovat Git v této složce
git init

# 2. Nastavit hlavní větev na 'main' (moderní standard místo 'master')
git branch -M main

# 3. Přidat všechny soubory
git add .

# 4. První commit
git commit -m "Initial commit: Dum Netusil web"

# 5. Připojit ke svému GitHub repu — NAHRAĎ 'TVOJE-USER' a 'NAZEV-REPA'
git remote add origin https://github.com/TVOJE-USER/NAZEV-REPA.git

# 6. Push na GitHub
git push -u origin main
```

GitHub si po `git push` vyžádá login. Pokud žádá password, vygeneruj si "Personal Access Token":

1. Jdi na [github.com/settings/tokens](https://github.com/settings/tokens)
2. **Generate new token (classic)**
3. Zaškrtni rozsah `repo`
4. **Generate token**
5. Zkopíruj token a vlož ho místo hesla v Terminálu

### Krok 4: Zapni GitHub Pages

1. V repu na GitHubu jdi do **Settings** (vpravo nahoře)
2. V levém menu klikni **Pages**
3. V sekci "Build and deployment":
   - **Source**: `Deploy from a branch`
   - **Branch**: `main`, složka `/ (root)`
4. **Save**
5. Počkej ~1 minutu, GitHub web nasadí
6. URL bude: `https://TVOJE-USER.github.io/NAZEV-REPA/`

### Krok 5: Custom doména (dumnetusil.cz)

Soubor `CNAME` už doménu připravil — stačí v DNS u registrátora přidat tyto záznamy:

| Typ | Hostname | Hodnota |
|---|---|---|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | TVOJE-USER.github.io. |

(IP adresy jsou GitHub Pages — fungují pro všechny.)

Po DNS propagaci (~1 hodina) bude web na **dumnetusil.cz** s automatickým HTTPS.

---

## Varianta B — Aktualizace existujícího repu

Tohle uděláš pokaždé, když ti od Claude přijde nová verze webu.

### Postup:

1. **Stáhni si nejnovější `Web pro GIT`** od Claude
2. **Otevři Terminál** v tvojí lokální repo složce (kde máš `.git/`)
3. **Smaž starý obsah** (kromě `.git/`):
   ```bash
   find . -mindepth 1 -maxdepth 1 ! -name '.git' -exec rm -rf {} +
   ```
4. **Zkopíruj nový obsah** ze složky `Web pro GIT` na místo (přes Finder nebo `cp -r`)
5. **Commit a push**:
   ```bash
   git add -A
   git commit -m "Aktualizace: nove ceny / statusy / opravy"
   git push
   ```

GitHub Pages se přepublikuje automaticky za ~30 sekund.

### Ještě jednodušší přes GitHub Desktop

Pokud nechceš Terminál, [GitHub Desktop](https://desktop.github.com/) je vizuální alternativa:

1. Stáhni a nainstaluj GitHub Desktop
2. Otevři tvůj repo
3. Přetáhni soubory ze `Web pro GIT` do okna GitHub Desktop
4. Napsat commit message
5. **Commit to main** → **Push origin**

---

## Co je ve složce a proč

| Soubor / Složka | K čemu slouží | Pushnout na Git? |
|---|---|---|
| `index.html`, `byty/*.html` | Stránky webu | ✅ ano |
| `styles.css`, `script.js` | Styly + JS | ✅ ano |
| `img/` | Obrázky (vizualizace, půdorysy) | ✅ ano |
| `ceny.json`, `status.json` | Konfigurace cen a dostupnosti | ✅ ano |
| `generate.py` | Generátor (pro Claude) | ✅ ano (volitelné) |
| `CNAME` | Custom doména pro GitHub Pages | ✅ ano |
| `.nojekyll` | Vypíná Jekyll processing | ✅ ano |
| `.htaccess` | Apache config (na GH Pages se nepoužije, nevadí) | ✅ ano |
| `404.html` | Vlastní 404 stránka | ✅ ano |
| `robots.txt`, `sitemap.xml` | SEO | ✅ ano |
| `README.md` | Dokumentace | ✅ ano |
| `.github/` | CI/CD workflow (volitelné) | ⚠️ pokud nechceš CI/CD, smaž před push |
| `__pycache__/` | Python cache | ❌ ne (`.gitignore` to řeší) |

---

## Časté problémy

**`git push` hlásí "Authentication failed"**  
GitHub od 2021 nepřijímá heslo z webu. Vygeneruj Personal Access Token na [github.com/settings/tokens](https://github.com/settings/tokens) a dej ho místo hesla.

**Pages mi nefunguje, vidím 404**  
GitHub Pages potřebuje ~1 minutu po prvním push. Pokud nefunguje, ověř v Settings → Pages, že je `Branch: main / (root)` nastaven.

**Custom doména nefunguje**  
DNS propagace trvá až 24 hodin. Otestuj zatím na `TVOJE-USER.github.io/NAZEV-REPA/`. Po propagaci v Settings → Pages → Custom domain zaškrtni **Enforce HTTPS**.

**Změnil jsem `ceny.json`, ale web zůstal stejný**  
`ceny.json` je jen zdroj dat. Aby se promítly do HTML, musíš spustit `python3 generate.py` (regeneruje HTML) a pushnout. Nebo to napiš Claude a vygeneruje ti to.

---

**Vytvořeno Claude pro projekt Dům Netušil · 2026**
